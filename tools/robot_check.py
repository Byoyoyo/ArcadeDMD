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


CALLS = []                                                        # (game, two_from, a winner given) of each game played
FILMS = []                                                        # (the winner's hold, a film given, a journal given)
QUITS = []                                                        # the games at which ArcadeDMD was asked to quit


def run(script, off=(), closed=(), setup=None, runs=1, only=None, unseen=False, limit=4000, win=False, fights=(),
        deaf=(), restart=False, film=False, old=None):
    """script: what each game does (good, bad, nostart, boom, blind). off / closed: [(from, to)] in seconds of the tour
    during which the screen is off / ArcadeDMD is closed. win: the second tour; fights: the games that are fighting
    games; deaf: those that keep nothing of what is written. old: the ArcadeDMD that runs was started before these files
("quits": it quits when asked, "stays": it cannot be asked, "still": the one started after it is no newer).
Returns (code, robot.json, lines said, games started, folder).
    / script : ce que fait chaque jeu. off / closed : les moments où l'écran est éteint / ArcadeDMD fermé."""
    root = tempfile.mkdtemp(dir=TOP.name)
    for d in ("games", "runtime", "roms"):
        os.makedirs(os.path.join(root, d))
    games = names(*range(len(script)))
    for i, n in enumerate(games):
        with open(os.path.join(root, "games", n + ".json"), "w") as f:
            json.dump(dict({"memory": {"values": {}}}, **({"scene_from": "neogeo_combat"} if i in fights else {})), f)
        open(os.path.join(root, "roms", n + ".zip"), "w").close()
    with open(os.path.join(root, "games", "shared.json"), "w") as f:      # a shared file named like the BIOS's zip
        json.dump({"fallback": True, "memory": {"values": {}}, "scene_from": "neogeo_combat"}, f)
    open(os.path.join(root, "roms", "shared.zip"), "w").close()
    base = {"exe": "x", "core": "c", "rom_dir": os.path.join(root, "roms"), "ext": ".zip"}
    base.update(setup or {})
    with open(os.path.join(root, "runtime", "robot.json"), "w") as f:
        json.dump(base, f)
    what = dict(zip(games, script))
    cur, started = {}, []
    t0 = CLOCK[0]
    revived = []                                                  # when the robot started ArcadeDMD again
    stale, gone = [bool(old)], [False]                            # the one that runs is old / it was asked to quit

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
        assert rom != "shared", "the tour started a shared file, which is no game"
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
        if within(closed) and not revived:
            time.sleep(wait)
            return None
        return dict({"memory": True}, **({} if stale[0] else {"clock": True}))

    def engine_start(root):                                       # restart: the robot can start ArcadeDMD itself
        if not restart:
            raise OSError("no python")
        revived.append(CLOCK[0] - t0)
        if gone[0]:
            gone[0], stale[0] = False, old == "still"

    def engine_quit(root, wait=20.0):
        QUITS.append(cur.get("rom"))
        gone[0] = old != "stays"
        return gone[0]

    class Champ:                                                  # the winner's stand-in / la doublure du gagnant
        def __init__(self, *a, hold=0):
            hard = cur["rom"] in deaf
            self.ready, self.wins, self.rounds = True, 0 if hard else 24, 1 if hard else 24
            self.off = "refused" if hard else None
            self.hold = hold

    del CALLS[:]
    del FILMS[:]
    del QUITS[:]

    def play(client, seconds, rng, **k):
        CALLS.append((cur["rom"], k.get("two_from", 0.7), k.get("winner") is not None))
        FILMS.append((getattr(k.get("winner"), "hold", None), k.get("film") is not None, k.get("journal") is not None))
        cur["played"] = bool(cur["runs"])
        time.sleep(seconds if cur["runs"] else 5.0)
        if cur["runs"] and k.get("trace") is not None:
            k["trace"].extend((0 if what[cur["rom"]] == "blind" else i % 7, i * 296, i * 5.0) for i in range(70))
        return cur["played"]

    def close_game(*a, **k):
        cur["runs"] = False
        return True

    def result(root, rom, since, say, head="", sub="", journal=None):
        say(head + "rangé" + (" dans " + sub if sub else ""))
        return 2, 36, True, 639 if cur.get("played") else 3

    robot._client = lambda cfg: Client()
    robot.launch, robot.wait_playing, robot.acked, robot.play = launch, wait_playing, acked, play
    robot.close_game, robot._result = close_game, result
    robot.prober = lambda client, st, root: None
    robot.Winner = Champ
    robot.engine_runs = lambda: not gone[0] and (bool(revived) or not within(closed))
    robot.engine_start, robot.engine_quit = engine_start, engine_quit
    out, rc = [], None
    for _ in range(runs):
        rc = robot.tour(root, {}, minutes=6, out=out.append, only=only, unseen=unseen, win=win, film=film)
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


prober = robot.prober                                             # the real ones, run() puts stand-ins in their place
WINNER = robot.Winner
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
check("it cannot be started here: said once, not at each game",
      (said(out, "ArcadeDMD n'est pas lancé"), said(out, "ArcadeDMD ne démarre pas")), (1, 1))

rc, st, out, la, _ = run(["good"] * 6, closed=[(400, 10 ** 6)], restart=True)
check("ArcadeDMD closed for good, the robot starts it itself: every game recorded, none tried twice",
      (rc, st["done"], st["aside"], len(la), said(out, "je le lance"), said(out, "J'attends")),
      (0, names(*range(6)), [], 6, 1, 0))

rc, st, out, la, _ = run(["good"] * 4, closed=[(0, 10 ** 6)], restart=True)
check("ArcadeDMD not running when the tour starts (the PC started again): started before the first game",
      (rc, st["done"], len(la), said(out, "je le lance")), (0, names(*range(4)), 4, 1))

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

# ---------------------------------------------------------------------- the second tour
rc, st, out, la, _ = run(["good"] * 5, fights=(0, 2, 3), win=True, setup={"done": names(0, 1, 2, 3, 4)})
check("the second tour takes the fighting games alone, with its own list",
      (rc, la, st["won"], st["done"]), (0, names(0, 2, 3), names(0, 2, 3), names(0, 1, 2, 3, 4)))
check("player 1 is made to win, no second player comes", [c[1:] for c in CALLS], [(2.0, True)] * 3)
check("its files are kept apart from the first tour's", said(out, "rangé dans win"), 3)
rc, st, out, la, _ = run(["good"] * 6, fights=range(6), win=True, deaf=names(0, 1, 2, 3, 4, 5))
check("three games that keep no write: the tour goes on with two players, writing nothing",
      (rc, [c[1:] for c in CALLS], said(out, "à deux joueurs, sans rien écrire")),
      (0, [(2.0, True)] * 3 + [(0.0, False)] * 3, 1))
rc, st, out, la, _ = run(["good"] * 6, fights=range(6), win=True, deaf=names(0, 1, 3))
check("two that keep no write, then one that does: the tour keeps writing", [c[2] for c in CALLS], [True] * 6)
rc, st, out, la, _ = run(["good", "bad", "good"], fights=range(3), win=True, setup={"aside": names(0)})
check("a game left aside by the second tour is its own business",
      (st["won"], st["aside_won"], st["aside"]), (names(0, 2), names(1), names(0)))

check("the first two tours film nothing, and leave no round alone", set(FILMS), {(0, False, True)})

# ---------------------------------------------------------------------- the third tour
rc, st, out, la, _ = run(["good"] * 5, fights=(0, 2, 3), film=True, setup={"done": names(0, 1, 2, 3, 4), "won": names(0, 2, 3)})
check("the third tour takes the fighting games alone, with its own list",
      (rc, la, st["filmed"], st["won"], st["done"]), (0, names(0, 2, 3), names(0, 2, 3), names(0, 2, 3), names(0, 1, 2, 3, 4)))
check("player 1 wins there too, each round left alone at its start and filmed",
      ([c[1:] for c in CALLS], set(FILMS)), ([(2.0, True)] * 3, {(robot.FILM_HOLD, True, True)}))
check("its files are kept apart from the other tours'", said(out, "rangé dans film"), 3)
check("it says what it is", said(out, "Troisième tour, le robot filme le début de chaque round"), 1)
rc, st, out, la, _ = run(["good", "bad", "good"], fights=range(3), film=True, setup={"aside": names(0), "aside_won": names(2)})
check("a game left aside by the third tour is its own business",
      (st["filmed"], st["aside_filmed"], st["aside_won"], st["aside"]), (names(0, 2), names(1), names(2), names(0)))
rc, st, out, la, _ = run(["good"] * 3, unseen=True)
check("no screenshot with the screen off: no journal of them", set(FILMS), {(None, False, False)})
rc, st, out, la, _ = run(["good"] * 3, fights=range(3), film=True, old="quits", restart=True)
check("an ArcadeDMD started before these files: closed and started again by the robot, the game taken again",
      (rc, la, st["filmed"], QUITS, said(out, "datait d'avant cette version"), said(out, "je le lance")),
      (0, names(0, 0, 1, 2), names(0, 1, 2), names(0), 1, 1))
check("and that game is not held to have failed", (said(out, "réessayé"), st["aside_filmed"]), (0, []))
rc, st, out, la, _ = run(["good"] * 3, fights=range(3), film=True, old="stays", restart=True)
check("one that cannot be asked to quit: the tour stops and says what to do, nothing is filmed",
      (rc, la, st.get("filmed") or [], said(out, "clic droit, Quitter"), len(FILMS)), (1, names(0), [], 1, 0))
rc, st, out, la, _ = run(["good"] * 3, fights=range(3), film=True, old="still", restart=True)
check("the one started in its place is no newer: asked to quit once, not for ever",
      (rc, la, QUITS, said(out, "clic droit, Quitter")), (1, names(0, 0), names(0), 1))
rc, st, out, la, _ = run(["good"] * 3, fights=range(3), win=True, old="quits", restart=True)
check("the first two tours ask nothing of an older ArcadeDMD", (rc, la, st["won"], QUITS), (0, names(0, 1, 2), names(0, 1, 2), []))


# ---------------------------------------------------------------------- the journal of the screenshots, the film
class Wire:                                                       # RetroArch's stand-in: counts what is asked
    def __init__(self, deaf=False):
        self.sent, self.deaf = [], deaf

    def send(self, text):
        self.sent.append(text)
        return not self.deaf


def shot_file(folder, name):
    open(os.path.join(folder, name), "w").close()


sdir = tempfile.mkdtemp(dir=TOP.name)
shot_file(sdir, "old-261117-100000.png")                          # left by the game before / laissée par le jeu d'avant
wire = Wire()
book = robot.Shots(wire, sdir)
check("a screenshot is asked and written down", (book.ask(10.0, "tick"), len(wire.sent), book.log[0]["why"]), (True, 1, "tick"))
check("never a second one in the same second", (book.ask(10.0 + robot.SHOT_GAP - 0.1, "round"), len(wire.sent)), (False, 1))
check("the next one a little later, with what the robot knew", (book.ask(10.01 + robot.SHOT_GAP, "round", round=2, clock=60),
                                                               book.log[1]["round"], book.log[1]["clock"]), (True, 2, 60))
book.look(11.3)
check("no file yet: no name", [e["name"] for e in book.log], [None, None])
shot_file(sdir, "game-261117-100010.png")
shot_file(sdir, "game-261117-100011.png")
book.look(11.5)
check("the files that appear go to the requests in their order, the old one to none",
      [e["name"] for e in book.log], ["game-261117-100010", "game-261117-100011"])
check("each with the clock's instant", all(isinstance(e["t"], float) and e["t"] > 1.7e9 for e in book.log), True)
book.ask(20.0, "tick")
book.look(26.0)
shot_file(sdir, "game-261117-100030.png")
book.look(27.0)
check("a file that comes after its request was given up names nothing", book.log[2]["name"], None)
check("RetroArch that does not take the request: nothing written down", (robot.Shots(Wire(True), sdir).ask(1.0, "tick"),), (False,))


class Round:                                                      # what the film reads of the winner
    def __init__(self, ready=True):
        self.on, self.rounds, self.t_top, self.t_prev = False, 0, None, None
        self.ready, self.off, self.clock = ready, None, 0

    def peek_clock(self):
        return self.clock


class Fixed:
    @staticmethod
    def uniform(a, b):
        return 0.5


wire = Wire()
book = robot.Shots(wire, sdir)
reel, rnd = robot.Film(book, Fixed()), Round()
for i in range(100):                                              # ten seconds between two rounds
    reel.step(100.0 + i * 0.1, rnd)
check("nothing filmed outside a round", len(wire.sent), 0)
rnd.on, rnd.rounds, rnd.t_top, rnd.t_prev = True, 1, 60, 60
t, asked = 110.0, []
while t < 116.0:                                                  # the announcement: the clock set, not counting
    if reel.step(t, rnd):
        asked.append(round(t - 110.0, 1))
    t += 0.1
gaps = [round(b - a, 1) for a, b in zip(asked, asked[1:])]
check("a round begins: filmed from its random delay on, a screenshot every SHOT_GAP, never closer",
      (0.5 <= asked[0] <= 0.6, len(asked) in (4, 5), all(robot.SHOT_GAP <= g <= robot.SHOT_GAP + 0.15 for g in gaps)),
      (True, True, True))
rnd.t_prev = 60 - robot.WIN_COUNT
check("the clock has counted its seconds: the film stops", (reel.step(116.5, rnd), reel.step(118.0, rnd)), (False, False))
rnd.on = False
reel.step(119.0, rnd)
rnd.on, rnd.rounds, rnd.t_top, rnd.t_prev = True, 2, 60, 60
n = len(wire.sent)
t = 130.0
while t < 130.0 + robot.FILM_FOR + 10:                            # a clock that never starts
    reel.step(t, rnd)
    t += 0.1
check("a round that never starts is not filmed for ever",
      abs(len(wire.sent) - n - (robot.FILM_FOR - 0.5) / robot.SHOT_GAP) <= 1.5, True)
check("the film counts its screenshots, each written down as a round's", (reel.count, {e["why"] for e in book.log}), (len(wire.sent), {"round"}))
wire = Wire()
book = robot.Shots(wire, sdir)
reel, rnd = robot.Film(book, Fixed()), Round(ready=False)         # life bars the file does not know: by the clock
seen = []
for i in range(400):
    t = 200.0 + i * 0.1
    rnd.clock = 0 if t < 205 else 60 if t < 209 else max(40, 60 - int(t - 209)) if t < 229 else 0 if t < 233 else 60
    if reel.step(t, rnd):
        seen.append((book.log[-1]["round"], book.log[-1]["clock"]))
check("where the winner cannot tell, the clock set again is the round: filmed until it has counted, and the next one too",
      (sorted({r for r, _ in seen}), min(c for _, c in seen) > 60 - robot.WIN_COUNT, len([1 for r, _ in seen if r == 1]) in (4, 5, 6)),
      ([1, 2], True, True))

# ---------------------------------------------------------------------- the robot that wins
from dmd.retroarch import Layout, layout_for, swap16  # noqa: E402

H1, H2, CLK, P1PTR, P2PTR = 0x100489, 0x100589, 0x105680, 0x105094, 0x105098


class Arcade:
    """A fighting game in 64 KB of Neo Geo memory, as RetroArch would serve it: rounds with a clock, a robot that
    takes a blow every 0.8 s and lands one every 2.5 s, best of three, the next opponent after a win, the same one
    after a loss. Its lives and its clock live in the memory, so what is written there counts. moving: the fighters
    are objects that change place at each round, found through two pointers. refuse: writes are not taken.
    / Un jeu de combat dans 64 Ko de mémoire Neo Geo. Ses vies et son chrono vivent dans la mémoire, donc ce qui y
    est écrit compte. moving : les combattants changent de place à chaque round. refuse : les écritures sont refusées."""

    def __init__(self, moving=False, refuse=False, demo=False):
        self.lay = Layout(0x100000, 0x10000, True)
        self.cpu = bytearray(0x10000)
        self.moving, self.refuse = moving, refuse
        self.state, self.t = "title", 0.0
        self.beaten = self.lost = self.rounds = 0
        self.score = [0, 0]
        self.slot = 0
        self.writes = []                                          # (state, address) of every write taken
        self.poke(0x10FDB6, 0 if demo else 1)
        self.poke(0x10FDAF, 1 if demo else 2)

    # the memory, in the processor's order, served in RetroArch's / la mémoire
    def poke(self, a, v):
        self.cpu[a - 0x100000] = v & 0xFF

    def peek(self, a):
        return self.cpu[a - 0x100000]

    def read(self, pos, n):
        return swap16(bytes(self.cpu))[pos:pos + n]

    def read_many(self, reqs):
        return {pos: self.read(pos, n) for pos, n in reqs}

    def write(self, pos, data):
        for i, b in enumerate(data):
            a = 0x100000 + ((pos + i) ^ 1)
            self.writes.append((self.state, a))
            if not self.refuse:
                self.poke(a, b)
        return True

    def bar(self, k):
        if not self.moving:
            return (H1, H2)[k]
        base = int.from_bytes(self.cpu[(P1PTR, P2PTR)[k] - 0x100000:(P1PTR, P2PTR)[k] - 0x100000 + 4], "big")
        return base + 0x56 if base else None

    def life(self, k):
        v = self.peek(self.bar(k))
        return v - 256 if v >= 0xB0 else v

    def begin(self):
        self.state, self.t, self.hit1, self.hit2, self.sec = "intro", 0.0, 0.8, 2.5, 1.0
        self.rounds += 1
        if self.moving:
            self.slot = (self.slot + 3) % 20
            for k, cell in enumerate((P1PTR, P2PTR)):
                self.cpu[cell - 0x100000:cell - 0x100000 + 4] = (0x100800 + 0x100 * (self.slot + k)).to_bytes(4, "big")
        for k in (0, 1):
            self.poke(self.bar(k), 0x60)
        self.poke(CLK, 0x60)

    def step(self, dt):
        self.t += dt
        if self.state == "title":
            if self.t >= 2.0:
                self.begin()
        elif self.state == "intro":
            if self.t >= 3.0:
                self.state, self.t = "fight", 0.0
        elif self.state == "fight":
            for k, attr, every, hurt in ((0, "hit1", 0.8, 12), (1, "hit2", 2.5, 6)):
                if self.t >= getattr(self, attr):
                    setattr(self, attr, getattr(self, attr) + every)
                    self.poke(self.bar(k), self.life(k) - hurt)
            if self.t >= self.sec:
                self.sec += 1.0
                c = self.peek(CLK)
                c = (c >> 4) * 10 + (c & 15)
                c = max(0, c - 1)
                self.poke(CLK, (c // 10) << 4 | c % 10)
            if self.life(0) <= 0 or self.life(1) <= 0 or self.peek(CLK) == 0:
                self.score[0 if self.life(0) > self.life(1) else 1] += 1
                self.state, self.t = "pose", 0.0
        elif self.state == "pose":
            if self.t >= 3.0:
                if self.moving:
                    for cell in (P1PTR, P2PTR):
                        self.cpu[cell - 0x100000:cell - 0x100000 + 4] = bytes(4)
                self.poke(CLK, 0)
                if max(self.score) >= 2:
                    if self.score[0] > self.score[1]:
                        self.beaten += 1
                    else:
                        self.lost += 1
                    self.score = [0, 0]
                    self.state, self.t = "title", 0.0
                else:
                    self.begin()


FILE = {"memory": {"values": {
    "_hp": {"addr": "0x100489", "type": "u8", "mult": 1.041667, "min": 0, "max": 100, "zero_from": "0xB0"},
    "_hp_vs": {"addr": "0x100489", "type": "u8", "mult": 0.833333, "min": 0, "max": 100, "zero_from": "0xBC"},
    "health_p2": {"addr": "0x100589", "type": "u8", "mult": 1.041667, "min": 0, "max": 100, "zero_from": "0xB0"},
    "time": {"addr": "0x105680", "type": "bcd", "bytes": 1}}},
    "tag": {"health": {"pick": ["_hp", "_hp_vs"], "at": {"eq": ["p2_mode", 1]}}}}
MOVING = {"memory": {"values": {
    "health": {"ptr": "0x105094", "ptr_range": ["0x100000", "0x10FFFF"], "addr": "0x56", "type": "u8", "mult": 1.041667,
               "min": 0, "max": 100, "zero_from": "0xB0"},
    "health_p2": {"ptr": "0x105098", "ptr_range": ["0x100000", "0x10FFFF"], "addr": "0x56", "type": "u8",
                  "mult": 1.041667, "min": 0, "max": 100, "zero_from": "0xB0"},
    "time": {"addr": "0x105680", "type": "bcd", "bytes": 1}}}}
NO_CLOCK = {"memory": {"values": {k: v for k, v in FILE["memory"]["values"].items() if k != "time"}}, "tag": FILE["tag"]}
NO_BARS = {"memory": {"values": {"time": {"addr": "0x105680", "type": "bcd", "bytes": 1}}}}


def six_minutes(game_file, with_winner=True, hold=0, **kind):
    game = Arcade(**kind)
    champ = WINNER(game, game.lay, game_file, hold=hold) if with_winner else None
    t = 0.0
    while t < 360.0:
        game.step(0.1)
        t += 0.1
        if champ is not None and round(t * 10) % 3 == 0:
            champ.tick(t)
    return game, champ


game, _ = six_minutes(FILE, with_winner=False)
check("the robot alone beats nobody", (game.beaten, game.lost > 3), (0, True))
game, champ = six_minutes(FILE)
check("made to win, it goes through the opponents", (game.beaten >= 12, game.lost, champ.off), (True, 0, None))
check("it counts the rounds it won", champ.wins >= 2 * game.beaten, True)
check("nothing is written outside a round", sorted({st for st, _ in game.writes}), ["fight", "intro"])
check("only the two lives and the clock are written", sorted({a for _, a in game.writes}), [H1, H2, CLK])
game, champ = six_minutes(MOVING, moving=True)
check("fighters that change place at every round", (game.beaten >= 12, game.lost, champ.off), (True, 0, None))
check("written where the pointers lead, nowhere else",
      all(a == CLK or (a & 0xFF) == 0x56 for _, a in game.writes), True)
game, champ = six_minutes(NO_CLOCK)
check("a game whose clock the file does not know: won by the blows that land", (game.beaten >= 6, game.lost), (True, 0))
game, champ = six_minutes(FILE, refuse=True)
check("writes that are not taken: said, and the game played as it is", (game.beaten, bool(champ.off)), (0, True))
check("it stopped asking", len(game.writes) < 80, True)
game, champ = six_minutes(NO_BARS)
check("life bars the file does not know: nothing written", (champ.ready, len(game.writes)), (False, 0))
game, champ = six_minutes(FILE, demo=True)
check("a demo the BIOS does not call a game: nothing written", len(game.writes), 0)
game, champ = six_minutes(FILE, hold=2)
check("a filmed round is left alone until its clock has counted two seconds, and still won",
      (sorted({st for st, _ in game.writes}), game.beaten >= 10, game.lost, champ.off), (["fight"], True, 0, None))


def picked(name, **modes):
    """Where the winner would write the two lives of a real game file, for what the BIOS says of the players."""
    with open(os.path.join(ROOT, "games", name + ".json"), encoding="utf-8") as f:
        g = json.load(f)
    w = WINNER(None, layout_for(g, name), g, name)
    return w.ready, [b and (b["ptr"], b["addr"]) for b in w._pick(modes)]


for name in ("aodk", "ragnagrd"):
    with open(os.path.join(ROOT, "games", name + ".json"), encoding="utf-8") as f:
        g = json.load(f)
    check(name + ": a timer read but not shown is the round's clock for the robot too",
          (WINNER(None, layout_for(g, name), g, name).clock or {}).get("addr"), g["memory"]["values"]["_time"]["addr"])
check("Fatal Fury against the computer: the computer's own life",
      picked("fatfury1", p1_mode=1, p2_mode=2), (True, [(None, 0x1003B8), (None, 0x1005B8)]))
check("Fatal Fury with a second player: player 2's",
      picked("fatfury1", p1_mode=1, p2_mode=1), (True, [(None, 0x1003B8), (None, 0x1004B8)]))
check("King of the Monsters, the computer in player 2's place",
      picked("kotm", p1_mode=1, p2_mode=1), (True, [(None, 0x10206B), (None, 0x10216B)]))
check("Kabuki Klash: through the pointers",
      picked("kabukikl", p1_mode=1, p2_mode=0), (True, [(0x105094, 0x56), (0x105098, 0x56)]))
check("a life counted as damage taken is left alone", picked("doubledr", p1_mode=1, p2_mode=0)[0], False)

TOP.cleanup()
if FAILS:
    print("\n".join(FAILS))
    sys.exit(1)
print("robot: ok")
