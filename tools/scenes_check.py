"""Plays a short made-up game of every game file on the HD screen, one player then two, and fails if the HD screen of a
game gives up (an error in its scene sends the marquee back to the LED display). The values of the game's file that
have an address go up and down so that the scene meets a power-up, a life lost, a bomb, a second player who joins, a
continue and a game over; the values without an address stay unknown, as on a cabinet. A game with the lively screen
("hd": {"dynamic": true}) plays a second one: the boss of its mission comes and is shot down, the mission ends, its show
is given, and the next mission begins before the show is over. Run by the check of every pull request.

Joue une courte partie inventée de chaque fichier de jeu sur l'écran HD, à un joueur puis à deux, et échoue si l'écran
HD d'un jeu abandonne (une erreur dans sa scène renvoie le marquee à l'affichage LED). Les valeurs du fichier montent
et descendent pour que la scène rencontre un bonus, une vie perdue, une bombe, un second joueur qui arrive, un
continue et un game over. Un jeu à l'écran vivant en joue une seconde : le boss de sa mission arrive et tombe, la
mission se termine, son spectacle est donné, et la mission suivante commence avant la fin du spectacle.

usage: python tools/scenes_check.py [game ...]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from dmd import app  # noqa: E402
from dmd.memvalues import derive, game_values, resolve_value  # noqa: E402
from dmd.outputs import PreviewOutput  # noqa: E402

W, H = 1920, 460
STEP, LENGTH = 0.25, 9.0
# what each player does during the made-up game: (from second, player 1's BIOS mode, player 2's)
# ce que fait chaque joueur : 1 joue, 2 continue ?, 3 partie finie
MODES = [(0.0, 1, 0), (3.0, 1, 1), (6.0, 2, 1), (7.0, 3, 1), (8.0, 1, 1)]


def shape(name, d, k):
    """The k-th value of a made-up game for one entry of the file. / La k-ième valeur d'une partie inventée."""
    top = d.get("max") if isinstance(d.get("max"), (int, float)) and d.get("max") > 0 else None
    low = d.get("min") if isinstance(d.get("min"), (int, float)) else 0
    base = name.split("_p2")[0].lstrip("_")
    if isinstance(d.get("count"), int):                        # a table of objects: a big one comes and is shot down
        row = [0] * d["count"]
        row[min(3, d["count"] - 1)] = (0, 600, 600, 450, 300, 150, 0, 120, 60, 0)[k % 10]
        return row
    if base.startswith("score"):
        return 100 * k * k
    if base.startswith("time"):
        return max(0, int(top or 60) - k)
    seq = (2, 2, 3, 3, 2, 1, 0, 1, 3, 2) if top is None else (top, top, top / 2, top, top / 4, 1, 0, top / 2, top, top - 1)
    v = seq[k % len(seq)]
    return max(low, int(v) if float(v).is_integer() or not isinstance(top, float) else v)


def play(eng, out, clock, game):
    """One made-up game; the error that stopped the HD screen, or None. / Une partie inventée ; l'erreur, ou None."""
    eng.start_demo(game)
    eng.sim, eng.demo_until = None, None
    for d in (eng.state.values, eng.state.prev, eng.state.changed_at, eng.state.hist):
        d.clear()                                              # what the demo put there: a real game starts with nothing
    eng.state.events.clear()
    g = eng.library.get(game) or {}
    # a value without an address is never read on a cabinet: the scene must do without it
    # une valeur sans adresse n'est jamais lue sur une borne : la scène doit s'en passer
    vals = {n: d for n, d in game_values(g, game, "").items() if isinstance(d, dict) and d.get("addr")}
    tag = g.get("tag") if isinstance(g.get("tag"), dict) else {}
    t, k, last = clock[0] + 1.0, 0, None
    end = t + LENGTH
    t0 = t
    while t < end:
        clock[0] = t
        mode = [m for m in MODES if m[0] <= t - t0][-1]
        if mode != last:
            eng.state.update("p1_mode", mode[1], t)
            eng.state.update("p2_mode", mode[2], t)
            last = mode
        if round((t - t0) / STEP) % 2 == 0:                    # every half second the values move / les valeurs bougent
            for name, d in vals.items():
                if not isinstance(d, dict) or name in ("p1_mode", "p2_mode") or name.startswith("bios_"):
                    continue
                if name in ("p1_input", "p2_input", "_in_p1", "_in_p2"):
                    eng.state.update(name, (0, 0x10, 0x18, 0x02, 0x24, 0x00)[k % 6], t)
                elif name == "credits":
                    eng.state.update(name, 2, t)
                else:
                    eng.state.update(name, shape(name, d, k), t)
            k += 1
        for name, spec in tag.items():
            v = resolve_value(spec, eng.state.values)
            if v is not None and eng.state.values.get(name) != v:
                eng.state.update(name, v, t, quiet=True)
        if eng.derived:
            for name, v in derive(eng.derived, eng.state.values).items():
                if eng.state.values.get(name) != v:
                    eng.state.update(name, v, t, quiet=True)
        frame = eng.step(t)
        out.hd_next = 0.0
        out.send(frame)
        if out.hd_view is None:
            return out.said[-1] if out.said else "the HD screen stopped"
        t = round(t + STEP, 4)
    clock[0] = t
    return None


def play_boss(eng, out, clock, game):
    """The second made-up game of a game with the lively screen: the boss of the mission comes (WARNING, the small cards,
    its wide bar), takes hits while a life is lost and a weapon picked up, falls; the game's end-of-mission screens begin
    (the show, its three parts); then mission 2 begins and cuts the show short. The error that stopped the HD screen, or
    None. / La seconde partie inventée d'un jeu à l'écran vivant : le boss arrive, encaisse, tombe ; la fin de mission
    (le spectacle, ses trois temps) ; puis la mission 2 commence et coupe le spectacle."""
    g = eng.library.get(game) or {}
    hd = g.get("hd") if isinstance(g.get("hd"), dict) else {}
    if not hd.get("dynamic"):
        return None
    eng.start_demo(game)
    eng.sim, eng.demo_until = None, None
    for d in (eng.state.values, eng.state.prev, eng.state.changed_at, eng.state.hist):
        d.clear()
    eng.state.events.clear()
    vals = {n: d for n, d in game_values(g, game, "").items() if isinstance(d, dict) and d.get("addr")}
    slots = [s for s in (hd.get("boss_slots") or ["boss_hp"]) if s in vals]
    lives = [v for v in (hd.get("boss_life") or {}).values() if isinstance(v, (int, float))]
    full = int(max(lives + [hd.get("boss_min") or 0, 3000]))
    flag = hd.get("boss_flag") if hd.get("boss_flag") in vals else None    # the game says when its boss is fought
    step = 0.1
    t0 = t = clock[0] + 1.0

    def boss(life):
        for s in slots[:1]:
            n = vals[s].get("count")
            eng.state.update(s, [life if i == min(3, n - 1) else 0 for i in range(n)] if isinstance(n, int) else life, t)

    while t < t0 + 23.0:
        clock[0] = t
        k = t - t0
        if k == 0:
            for name, d in vals.items():
                if name.startswith("bios_") or name in slots:
                    continue
                if name in ("p1_mode", "p2_mode", "mission"):
                    eng.state.update(name, 1, t)
                elif name in ("p1_input", "p2_input", "_in_p1", "_in_p2"):
                    eng.state.update(name, 0, t)
                else:
                    eng.state.update(name, [0] * d["count"] if isinstance(d.get("count"), int) else shape(name, d, 0), t)
            boss(0)
        elif k < 0.5:
            pass
        elif k < 3.5:
            boss(full)                                         # it comes: WARNING, then the small cards and its bar
        elif k < 5.0:
            boss(int(full * (5.0 - k) / 1.5))                  # it takes hits / il encaisse
        else:
            boss(0)                                            # it falls / il tombe
        if flag:
            eng.state.update(flag, 1 if 0.4 <= k < 5.5 else 0, t)
        for name, at, v in (("lives", 3.7, 1), ("weapon_p2", 3.9, 3), ("ammo_p2", 3.9, 200), ("lives", 4.3, 0), ("score", 4.5, 5000),
                            ("mission", 18.5, 2), ("mission", 21.5, 3)):
            if name in vals and abs(k - at) < step / 2:
                eng.state.update(name, v, t)
        tag = g.get("tag") if isinstance(g.get("tag"), dict) else {}
        for name, spec in tag.items():
            v = resolve_value(spec, eng.state.values)
            if v is not None and eng.state.values.get(name) != v:
                eng.state.update(name, v, t, quiet=True)
        if eng.derived:
            for name, v in derive(eng.derived, eng.state.values).items():
                if eng.state.values.get(name) != v:
                    eng.state.update(name, v, t, quiet=True)
        ending = 1 if 6.0 <= k < 18.5 or 20.0 <= k < 21.5 else 0   # the game's end-of-mission screens / ses écrans de fin
        if eng.state.values.get("mission_ending") != ending:
            eng.state.update("mission_ending", ending, t, quiet=True)
        frame = eng.step(t)
        out.hd_next = 0.0
        out.send(frame)
        if out.hd_view is None:
            return out.said[-1] if out.said else "the HD screen stopped"
        t = round(t + step, 4)
    clock[0] = t
    return None


def screen(clock):
    said = []
    out = PreviewOutput({"enabled": True, "x": 0, "y": 0, "width": W, "height": H, "mode": "always", "style": "hd", "logos": False}, said.append)
    out.said = said
    out.hd_view.clock = lambda: clock[0]
    return out


def main(argv):
    log = app.Logger(None, echo=False)
    cfg = dict(app.load_config(ROOT, log), retroarch={"enabled": False}, textfiles={"enabled": False})
    clock = [0.0]
    out = screen(clock)
    eng = app.Engine(ROOT, cfg, [out], log, demo_game="_idle")
    games = argv or sorted(k for k in eng.library.games if not k.startswith("_"))
    fails = []
    for game in games:
        try:
            err = play(eng, out, clock, game) or play_boss(eng, out, clock, game)
        except Exception as e:                                 # the engine itself / le moteur lui-même
            err = repr(e)
        if err:
            fails.append(f"{game}: {err}")
            if out.hd_view is None:                            # a new screen for the games that follow / un écran neuf
                out.close()
                out = screen(clock)
                eng.outputs[:] = [out]
                out.attach(eng)
    out.close()
    for f in fails:
        print(f)
    print(f"scenes: {len(games) - len(fails)} of {len(games)} games ok" if fails else f"scenes: ok ({len(games)} games)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
