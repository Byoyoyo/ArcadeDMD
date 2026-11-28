"""The book of moves of the fighters (1.41), checked three ways. Every fighter of the games that list their desperation
moves has special moves to show, and they hold in the panel: alone, with two players, and once the desperation moves
have come forward, with arrows and letters a player can read. A recorded game of The King of Fighters '98 and one of
'97 with two players are then played on the HD screen: the book is drawn, the desperation moves come forward when one
can come out, and the setting of the window turns the book off. Run by the check of every pull request.

Le carnet de coups des combattants, contrôlé de trois façons. Chaque combattant des jeux qui listent leurs coups
désespérés a des coups spéciaux à montrer, et ils tiennent dans le panneau : seul, à deux joueurs, et quand les coups
désespérés sont passés devant, avec des flèches et des lettres lisibles. Une partie enregistrée de The King of
Fighters '98 et une de '97 à deux joueurs sont ensuite jouées sur l'écran HD : le carnet est dessiné, les coups
désespérés passent devant quand l'un d'eux peut sortir, et le réglage de la fenêtre coupe le carnet.

usage: python tools/book_check.py
"""
import glob
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ["ARCADEDMD_LANG"] = "fr"
os.environ.pop("ARCADEDMD_FIGHT_BOOK", None)          # the settings decide here / ici les réglages décident
os.environ.pop("ARCADEDMD_FIGHT_STAGE", None)

from dmd import app, gui_setup, hd_book  # noqa: E402
from dmd.capture import read_capture  # noqa: E402
from dmd.hd_specials import fighter_rows  # noqa: E402
from dmd.memvalues import derive, resolve_value  # noqa: E402
from dmd.outputs import PreviewOutput  # noqa: E402

W, H = 1920, 470
CAPTURES = os.path.join(ROOT, "tests", "captures")
# the panel of a player as hd.draw_fight gives it to hd_book.draw_book: its width, and the height left for the cards
PANEL, HEIGHT = 748, 163


def games():
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "games", "*.json"))):
        with open(path, encoding="utf-8") as f:
            g = json.load(f)
        if isinstance(g.get("moves"), dict):
            out.append((os.path.basename(path)[:-5], g))
    return out


def check_layout():
    import pygame
    from dmd.hd import HDRenderer
    pygame.init()
    pygame.display.set_mode((1, 1))
    hd = HDRenderer(pygame, (W, H), ROOT, {"logos": False}, lambda *a: None, logos=None)
    S, seen, wider = hd.S, 0, {}
    found = games()
    assert len(found) >= 3, "the games that list their desperation moves"

    def held(where, cards, room, least_r, least_size, whole):
        ch, stacked, per, places = hd_book._layout(hd, cards, room, HEIGHT)
        assert len(places) == len(cards) and per * ch <= HEIGHT + 1, where
        for (_, _, groups, slots, title), (c, k, left, cw, text, size, r, sp) in zip(cards, places):
            assert r >= S(least_r) and size >= S(least_size), f"{where}: {title} too small to read ({r}, {size})"
            assert left + cw <= room + 1 and k < per, where
            cmd, wide = hd_book._width(slots, len(groups), r, sp), hd_book._wide(hd, text, size)
            assert (max(cmd, wide) if stacked else cmd + S(10) + wide) <= cw - S(6), f"{where}: {title} out of its card"
            assert text == title or (not whole and len(text) >= 13), f"{where}: {title} cut down to {text}"

    for key, g in found:
        fighters = [n for n, v in g["moves"].items() if isinstance(v, list)]
        assert fighters, key
        for name in fighters:
            cards = hd_book._deck(fighter_rows(g, name)[0], False)
            assert cards, f"{key} {name}: no special move to show"
            held(f"{key} {name}, alone", cards, S(PANEL - 16), 11, 15, True)
            span = S(PANEL - 24)
            held(f"{key} {name}, two players", cards, span - S(hd_book.BESIDE), 9, 12, False)
            wd = hd_book.forward_width(hd, cards, span, HEIGHT)
            wider[(key, name)] = wd
            if wd > S(hd_book.BESIDE):                            # his desperation moves widen: his special moves still read
                held(f"{key} {name}, desperation moves forward", cards, span - wd, 9, 12, False)
            seen += 1
    most = sum(1 for wd in wider.values() if wd >= S(hd_book.FORWARD[0]))
    assert most * 2 > seen, f"the desperation moves come forward at their widest for most fighters ({most} of {seen})"
    assert wider[("kof98", "ROBERT")] == S(350) and wider[("kof97", "KIM")] == S(350), "the fighters of the recorded games"
    pygame.quit()
    return seen, most


def play(game, capture, start, stops, cfg=None):
    """Replays a recorded game on the HD screen and gives what the book holds at the seconds asked.
    / Rejoue une partie enregistrée sur l'écran HD et donne ce que le carnet contient aux secondes demandées."""
    clock, said = [0.0], []
    log = app.Logger(None, echo=False)
    conf = dict(app.load_config(ROOT, log), retroarch={"enabled": False}, textfiles={"enabled": False})
    out = PreviewOutput(dict({"enabled": True, "x": 0, "y": 0, "width": W, "height": H, "mode": "always", "style": "hd",
                              "logos": False}, **(cfg or {})), said.append)
    out.hd_view.clock = lambda: clock[0]
    eng = app.Engine(ROOT, conf, [out], log, demo_game=game)
    eng.sim = None
    eng.demo_until = None
    _, rows = read_capture(os.path.join(CAPTURES, capture))
    g = eng.library.get(game) or {}
    tag = g.get("tag") if isinstance(g.get("tag"), dict) else {}
    i, t, got, stops = 0, 0.0, [], sorted(stops)
    while stops:
        clock[0] = t
        while i < len(rows) and rows[i][0] <= t + 1e-9:
            _, name, value = rows[i]
            i += 1
            if name != "_end":
                eng.state.update(name, value, t)
        for k, spec in tag.items():
            v = resolve_value(spec, eng.state.values)
            if v is not None and eng.state.values.get(k) != v:
                eng.state.update(k, v, t, quiet=True)
        if eng.derived:
            for k, v in derive(eng.derived, eng.state.values).items():
                if eng.state.values.get(k) != v:
                    eng.state.update(k, v, t, quiet=True)
        frame = eng.step(t)
        if t >= start:                                            # the screen drawn from there on / l'écran dessiné à partir de là
            out.hd_next = 0.0
            out.send(frame)
            assert out.hd_view is not None and out.hd_off is None, f"{game}: the HD screen gave up at {t:.1f} s ({said[-1:]})"
        if t >= stops[0] - 1e-9:
            hd = out.hd_view
            got.append(({s: round(v[0], 2) for s, v in hd.book_k.items()}, len(hd.book_lay), out.screen.copy()))
            stops.pop(0)
        t += 0.08 if t >= start - 2 else 0.25
    out.close()
    return got


def lit(surface, x0, x1, y0, y1):
    """Whether something is drawn in a part of the screen. / Si quelque chose est dessiné dans une partie de l'écran."""
    return any(sum(surface.get_at((x, y))[:3]) > 90 for x in range(x0, x1, 7) for y in range(y0, y1, 5))


def check_screen():
    # a player alone: his special moves under his name, his desperation moves on the side nobody plays
    quiet, stock = play("kof98", "kof98-20261109-165045.log", 26.0, (36.0, 44.0))
    assert quiet[1] >= 1 and quiet[0] == {"p1": 0.0}, f"alone, no stock: the book drawn, the desperation moves pale ({quiet[:2]})"
    assert stock[0]["p1"] > 0.9, f"a stock: the desperation moves come forward ({stock[0]})"
    assert lit(quiet[2], 1160, 1860, 320, 455) and lit(quiet[2], 60, 760, 300, 455), "both halves hold the book"
    assert lit(quiet[2], 1500, 1890, 4, 44), "PRESS START small in the top row, above the desperation moves"
    # two players: a book each, the desperation moves of the one who can do one come forward
    both, one = play("kof97", "kof97-20261109-131539.log", 276.0, (282.0, 289.0))
    assert both[0] == {"p1": 0.0, "p2": 0.0} and both[1] >= 2, f"two players: a book each ({both[:2]})"
    assert one[0]["p2"] > 0.9 and one[0]["p1"] < 0.1, f"only the player who can do one sees his come forward ({one[0]})"
    # "fight_book": false gives the panel of the desperation moves alone back, PRESS START big on the side nobody plays
    off, = play("kof98", "kof98-20261109-165045.log", 34.0, (36.0,), {"fight_book": False})
    assert off[0] == {} and off[1] == 0, f"turned off: no book ({off[:2]})"
    assert lit(off[2], 1160, 1860, 340, 450) and not lit(off[2], 1500, 1890, 4, 44), "PRESS START big, none in the top row"


def check_window():
    with tempfile.TemporaryDirectory() as tmp:
        routes = gui_setup.Setup(tmp, lambda *_: None).routes()
        get, save = routes[("GET", "/api/screens")], routes[("POST", "/api/screens")]
        assert get({})["preview"]["fight_book"] is not False, "on until told otherwise"
        assert save({"preview": {"fight_book": False}})["ok"] is True
        with open(os.path.join(tmp, "config.json"), encoding="utf-8") as f:
            assert json.load(f)["outputs"]["preview"]["fight_book"] is False, "saved in config.json"
        assert get({})["preview"]["fight_book"] is False, "read back by the window"
        assert save({"preview": {"fight_book": True}})["ok"] is True and get({})["preview"]["fight_book"] is True, "and on again"


def main():
    n, most = check_layout()
    print(f"ok  layout ({n} fighters, the desperation moves at their widest for {most})")
    check_screen()
    print("ok  screen")
    check_window()
    print("ok  window")
    return 0


if __name__ == "__main__":
    sys.exit(main())
