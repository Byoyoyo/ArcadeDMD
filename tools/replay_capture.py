"""Replays a capture (runtime/captures/<game>-<date>.log, 1.33) through the fight engine and prints what the HD screen
would have shown, second by second: the select screens, ROUND n, FIGHT !, the hits, K.O., WIN, TIME UP, VICTOIRE, the
next fighter, VS. The same engine as on the cabinet, with the game's file as it is now, so a fix in the file shows at
once. Used to tune a fighting game from one match played, and as a test afterwards.

Rejoue une capture dans le moteur de combat et écrit ce que l'écran HD aurait montré, seconde par seconde. Le même
moteur que sur la borne, avec le fichier du jeu tel qu'il est maintenant.

usage: python tools/replay_capture.py CAPTURE [--values] [--json OUT]
  --values   also prints the changes of the main values (health, timer, round, screen, state) / les valeurs aussi
  --json     writes the timeline as JSON, for the tests / la chronologie en JSON
"""
import argparse
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("ARCADEDMD_LANG", "fr")

MAIN = ("health", "health_p2", "time", "round", "_screen", "_fight_state", "p1_mode", "p2_mode", "_p1_lost", "_p2_lost",
        "select", "p1_char", "p2_char", "credits", "_stock", "_stock_p2", "_maxv", "_maxv_p2", "_pmode", "_pmode_p2")


def replay(path, show_values=False, step=1 / 60):
    import pygame
    from dmd.capture import read_capture
    from dmd.hd import HDRenderer
    from dmd.hd_fight import FightFX
    from dmd.memvalues import derive
    from dmd.scene import GameState

    pygame.init()
    pygame.display.set_mode((1920, 460))
    head, rows = read_capture(path)
    key = head.get("game") or ""
    game = json.load(open(os.path.join(ROOT, "games", f"{key}.json"), encoding="utf-8"))
    derived = game.get("derived") or {}
    hd = HDRenderer(pygame, (1920, 460), ROOT, {"logos": False}, lambda *a: None, logos=None)
    lines = []
    hd.log = lambda m: lines.append((T[0], str(m)))
    fx = FightFX(hd, rng=random.Random(1))
    hd.fight = fx
    st = GameState()
    st.reset({"game": key, "system": head.get("system") or key, "title": head.get("title") or key})
    T = [0.0]
    out = []
    state = {"select": False, "round_show": -99.0, "fight_t": -99.0, "ko": None, "win": None, "banner": None, "out": None,
             "next": {"p1": -99.0, "p2": -99.0}, "hold": {"p1": None, "p2": None}, "chars": {}}

    def note(t, what):
        out.append((round(t, 2), what))

    i = 0
    n = len(rows)
    end = rows[-1][0] if rows else 0.0
    t = 0.0
    while t <= end + 1.0:
        while i < n and rows[i][0] <= t + 1e-9:
            _, name, value = rows[i]
            if name == "_end":
                i += 1
                continue
            st.update(name, value, t, at=1000.0 + rows[i][0])
            if show_values and name in MAIN:
                note(t, f"  {name} = {value}")
            i += 1
        vals = dict(st.values)
        vals.update(derive(derived, vals))
        for k, v in derive(derived, vals).items():
            if st.values.get(k) != v:
                st.update(k, v, t, quiet=True)
        T[0] = t
        try:
            fx.update(vals, 1000.0 + t, key, game, idle=HDRenderer._nobody(vals), hist=st.hist)
        except Exception as e:                                       # noqa: BLE001
            note(t, f"ERREUR {e!r}")
            break
        # the events / les événements
        if fx.select != state["select"]:
            state["select"] = fx.select
            note(t, "écran de sélection (VS)" if fx.select else "fin de l'écran de sélection")
        if fx.round_show != state["round_show"] and fx.round_show > -90:
            state["round_show"] = fx.round_show
            note(fx.round_show - 1000.0, f"ROUND {int(fx.round_v) + 1 if fx.round_v is not None else '?'}"
                 + (f" ({fx.round_sub})" if getattr(fx, 'round_sub', '') else ""))
        if fx.fight_t != state["fight_t"] and fx.fight_t > -90 and fx.fight_wait is None:
            state["fight_t"] = fx.fight_t
            note(fx.fight_t - 1000.0, f"FIGHT ! ({fx.fight_why or 'tout de suite'})")
        if fx.ko_side != state["ko"]:
            state["ko"] = fx.ko_side
            if fx.ko_side is not None:
                note(t, f"K.O. de {fx.ko_side[0].upper()}")
        w = tuple(fx.win[:3]) if fx.win else None
        if w != state["win"]:
            state["win"] = w
            if w:
                note(t, f"WIN {w[0].upper()}" + (" PERFECT" if w[2] else ""))
        b = fx.banner[0] if fx.banner else None
        if b != state["banner"]:
            state["banner"] = b
            if b:
                note(t, b)
        if fx.out != state["out"]:
            state["out"] = fx.out
            if fx.out:
                note(fx.out[2] - 1000.0, f"VICTOIRE {fx.out[0].upper()} ({fx.out[1].upper()} éliminé)")
        for side in ("p1", "p2"):
            nt = fx.next_t.get(side, -99.0)
            if nt != state["next"][side] and nt > -90 and nt <= 1000.0 + t + 0.1:
                state["next"][side] = nt
                note(nt - 1000.0, f"{side.upper()} ENTRE EN SCÈNE {fx.next_name.get(side, '')}")
            name = vals.get(side + "_char")
            if name != state["chars"].get(side):
                state["chars"][side] = name
                note(t, f"  {side} {name}")
        t = round(t + step, 5)
    for lt, m in lines:
        out.append((round(lt, 2), f"  journal : {m}"))
    out.sort(key=lambda e: e[0])
    return head, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("capture")
    ap.add_argument("--values", action="store_true")
    ap.add_argument("--json", default="")
    args = ap.parse_args()
    head, out = replay(args.capture, args.values)
    print(f"{head.get('game')} {head.get('title')} {head.get('date')} (ArcadeDMD {head.get('version')})")
    for t, what in out:
        print(f"{t:8.2f}  {what}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"head": head, "events": out}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
