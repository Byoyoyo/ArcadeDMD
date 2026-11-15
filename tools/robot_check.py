"""Checks the robot's tour (dmd/robot.py): what it decides when a game cannot be played, when the screen goes off or
ArcadeDMD is closed, when an error nobody foresaw comes up. RetroArch, ArcadeDMD and the clock are stand-ins, so that
hours of tour and of waiting take no time. Then the stick and the speed read while a game is played, on a Neo Geo
memory. Run by the check of every pull request.

Vérifie le tour du robot : ce qu'il décide quand un jeu est injouable, quand l'écran s'éteint ou qu'ArcadeDMD est
fermé, quand une erreur imprévue arrive. RetroArch, ArcadeDMD et l'horloge sont joués par des doublures. Puis le stick
et la vitesse lus pendant qu'un jeu est joué, sur une mémoire Neo Geo.

usage: python tools/robot_check.py
"""
import json
import os
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dmd import robot  # noqa: E402
from dmd.i18n import set_language  # noqa: E402

set_language("fr")
CLOCK = [0.0]
time.sleep = lambda s: CLOCK.__setitem__(0, CLOCK[0] + s)
time.monotonic = lambda: CLOCK[0]
FAILS = []
TOP = tempfile.TemporaryDirectory(prefix="robot_check_")          # removed at the end / supprimé à la fin


def check(what, got, want):
    if got != want:
        FAILS.append(f"{what}: {got!r}, expected {want!r}")


def names(*i):
    return [f"g{k:02d}" for k in i]


def run(script, off=(), closed=(), setup=None, runs=1, only=None, unseen=False, limit=4000):
    """script: what each game does (good, bad, nostart, boom, blind). off / closed: [(from, to)] in seconds of the tour
    during which the screen is off / ArcadeDMD is closed. Returns (code, robot.json, lines said, games started, folder).
    / script : ce que fait chaque jeu. off / closed : les moments où l'écran est éteint / ArcadeDMD fermé."""
    root = tempfile.mkdtemp(dir=TOP.name)
    for d in ("games", "runtime", "roms"):
        os.makedirs(os.path.join(root, d))
    games = names(*range(len(script)))
    for n in games:
        with open(os.path.join(root, "games", n + ".json"), "w") as f:
            json.dump({"memory": {"values": {}}}, f)
        open(os.path.join(root, "roms", n + ".zip"), "w").close()
    base = {"exe": "x", "core": "c", "rom_dir": os.path.join(root, "roms"), "ext": ".zip"}
    base.update(setup or {})
    with open(os.path.join(root, "runtime", "robot.json"), "w") as f:
        json.dump(base, f)
    what = dict(zip(games, script))
    cur, started = {}, []
    t0 = CLOCK[0]

    def within(spans):
        return any(a <= CLOCK[0] - t0 < b for a, b in spans)

    class Proc:
        @staticmethod
        def poll():
            return None

    class Client:
        @staticmethod
        def status():
            return {"state": "PLAYING", "content": cur.get("rom"), "system": "arcade"} if cur.get("runs") else None

        @staticmethod
        def close():
            pass

    def launch(setup, rom, cfg):
        started.append(rom)
        if len(started) > limit:
            raise KeyboardInterrupt                               # a tour that never ends / un tour sans fin
        if what[rom] == "boom":
            raise OSError("no such program")
        cur.update(rom=rom, runs=what[rom] not in ("nostart", "bad") and not within(off), up=what[rom] != "nostart")
        return Proc()

    def wait_playing(client, timeout, proc=None):
        if not cur["up"]:
            time.sleep(timeout)
            return None
        return {"content": cur["rom"], "system": "arcade"}

    def acked(root, rom, since, wait=10.0):
        if within(closed):
            time.sleep(wait)
            return None
        return {"memory": True}

    def play(client, seconds, rng, **k):
        cur["played"] = bool(cur["runs"])
        time.sleep(seconds if cur["runs"] else 5.0)
        if cur["runs"] and k.get("trace") is not None:
            k["trace"].extend((0 if what[cur["rom"]] == "blind" else i % 7, i * 296, i * 5.0) for i in range(70))
        return cur["played"]

    def close_game(*a, **k):
        cur["runs"] = False
        return True

    def result(root, rom, since, say, head=""):
        say(head + "rangé")
        return 2, 36, True, 639 if cur.get("played") else 3

    robot._client = lambda cfg: Client()
    robot.launch, robot.wait_playing, robot.acked, robot.play = launch, wait_playing, acked, play
    robot.close_game, robot._result = close_game, result
    robot.prober = lambda client, st, root: None
    out, rc = [], None
    for _ in range(runs):
        rc = robot.tour(root, {}, minutes=6, out=out.append, only=only, unseen=unseen)
    with open(os.path.join(root, "runtime", "robot.json")) as f:
        return rc, json.load(f), out, started, root


def said(out, text):
    return sum(text in line for line in out)


# ---------------------------------------------------------------------- the stick and the speed read while playing
def readings():
    """prober and judged on a Neo Geo memory played by a stand-in. / Sur une mémoire Neo Geo jouée par une doublure."""
    st = {"content": "kof98", "system": "arcade"}
    lay = robot._layout(st, ROOT)

    class Memory:
        def __init__(self, dead):
            self.cpu = bytearray(lay.size)
            self.dead = dead

        def poke(self, addr, data):
            self.cpu[addr - lay.base:addr - lay.base + len(data)] = data

        def read(self, pos, n):
            return None if self.dead else lay._unswap(bytes(self.cpu))[pos:pos + n]

    def night(stick_from, fps, reset_at=None, n=72, dead=False):
        mem = Memory(dead)
        probe = prober(mem, st, ROOT)
        trace, frames = [], 5000
        for i in range(n):
            CLOCK[0] += 5.0
            frames = 12 if reset_at == i else frames + int(fps * 5)     # the BIOS sets its counter again
            mem.poke(0x10FE88, frames.to_bytes(4, "big"))
            mem.poke(0x10FD96, bytes([(i * 37) & 0xFF if i >= stick_from else 0]))
            got = probe()
            if got is not None:
                trace.append(got)
        stick, speed = robot.judged(trace)
        return stick, None if speed is None else round(speed)

    check("a game as it should be", night(0, 59.2), (True, 59))
    check("a game that reads its stick after forty seconds", night(8, 59.2), (True, 59))
    check("the BIOS sets its counter again during the start", night(0, 59.2, reset_at=2), (True, 59))
    check("RetroArch flat out", night(0, 900.0), (True, 900))
    check("a stick the game never shows", night(999, 59.2), (False, 59))
    check("memory that cannot be read: nothing is said", night(0, 59.2, dead=True), (None, None))
    check("a game cut after twenty seconds: nothing is said", night(0, 59.2, n=4), (None, None))


prober = robot.prober                                             # the real one, run() puts a stand-in in its place
readings()

# ---------------------------------------------------------------------- the tour
rc, st, out, la, _ = run(["good"] * 3)
check("three good games", (rc, st["done"], st["aside"]), (0, names(0, 1, 2), []))

rc, st, out, la, _ = run(["blind"] * 5)
check("a stick the game does not show never stops the tour", (rc, st["done"]), (0, names(0, 1, 2, 3, 4)))
check("it is said on the game's line", said(out, "stick du robot pas vu"), 5)

rc, st, out, la, _ = run(["good", "bad", "good", "good"])
check("a game that cannot be played: once more at the end, then left aside",
      (rc, st["done"], st["aside"], la), (0, names(0, 2, 3), names(1), names(0, 1, 2, 3, 1)))
rc, st, out, la, _ = run(["good", "bad", "good", "good"], runs=2)
check("started again, only that game, once", la[5:], names(1))

rc, st, out, la, _ = run(["good", "bad", "bad", "bad", "good", "good"])
check("three bad games in a row, the rest in order: no waiting",
      (rc, st["done"], st["aside"], said(out, "J'attends")), (0, names(0, 4, 5), names(1, 2, 3), 0))
check("a game recorded before was started to tell", la[4], "g00")

rc, st, out, la, _ = run(["good"] * 8, off=[(400, 5000)])
check("the screen off for an hour: waits, then takes the games again by itself",
      (rc, st["done"], st["aside"]), (0, names(*range(8)), []))
check("said once, and said when it works again", (said(out, "J'attends"), said(out, "ça remarche. Je reprends")), (1, 1))

rc, st, out, la, _ = run(["good"] * 6, closed=[(400, 3000)])
check("ArcadeDMD closed for a while: the same", (rc, st["done"], st["aside"]), (0, names(*range(6)), []))

rc, st, out, la, _ = run(["good"] * 6, off=[(0, 30000)], setup={"done": ["g05"]})
check("the screen off from the start, a game known: waits as long as it takes",
      (rc, st["done"], st["aside"]), (0, names(*range(6)), []))

rc, st, out, la, _ = run(["good"] * 6, off=[(0, 10 ** 6)], limit=400)
check("the screen off for good, no game known: two waits, the games left aside, and an end",
      (rc, st.get("done"), len(st["aside"]), said(out, "J'attends")), (0, [], 6, 2))

rc, st, out, la, _ = run(["bad", "bad", "bad", "good", "good"])
check("three bad games first, none known: two waits, then the tour goes on",
      (rc, st["done"], st["aside"], said(out, "J'attends")), (0, names(3, 4), names(0, 1, 2), 2))

rc, st, out, la, root = run(["good", "boom", "good"])
check("an error nobody foresaw costs one game", (rc, st["done"], st["aside"]), (0, names(0, 2), names(1)))
with open(os.path.join(root, "runtime", "robot_crash.log")) as f:
    check("and is kept in robot_crash.log", "OSError" in f.read(), True)

rc, st, out, la, _ = run(["good", "good", "nostart", "bad"], off=[(760, 3000)], limit=300)
check("the screen off while the last games are tried again: no game twice in the line",
      (rc, st["done"], st["aside"], la[-5:]), (0, names(0, 1), names(2, 3), names(2, 3, 2, 1, 3)))

rc, st, out, la, _ = run(["good"] * 3, setup={"done": names(0, 1, 2)})
check("everything done: a new tour", (rc, st["done"], la), (0, names(0, 1, 2), names(0, 1, 2)))

rc, st, out, la, _ = run(["good", "bad", "good"], setup={"done": names(0, 2), "aside": names(1)})
check("everything done but a game left aside: it alone, once",
      (rc, st["done"], st["aside"], la), (0, names(0, 2), names(1), names(1)))

rc, st, out, la, _ = run(["good"] * 3, setup={"aside": names(0)})
check("a game left aside comes last, and comes back when it works",
      (rc, st["done"], st["aside"], la), (0, names(0, 1, 2), [], names(1, 2, 0)))

rc, st, out, la, _ = run(["good", "bad", "good"], only=["g01", "g02"], setup={"done": names(0)})
check("games asked by name leave the lists alone",
      (rc, st["done"], st.get("aside"), la), (0, names(0), None, names(1, 2, 1)))

rc, st, out, la, _ = run(["good"] * 4, setup={"done": names(0)}, unseen=True)
check("the tour for a screen that is off keeps its own list", (rc, st["done"], st["unseen"]), (0, names(0), names(1, 2, 3)))

TOP.cleanup()
if FAILS:
    print("\n".join(FAILS))
    sys.exit(1)
print("robot: ok")
