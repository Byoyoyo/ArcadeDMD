"""Replays a capture (runtime/captures/<game>-<date>.log, 1.33) through the fight engine and prints what the HD screen
would have shown, second by second: the select screens, ROUND n, FIGHT !, the hits, K.O., WIN, TIME UP, VICTOIRE, the
next fighter, VS. The same engine as on the cabinet, with the game's file as it is now, so a fix in the file shows at
once. Used to tune a fighting game from one match played, and as a test afterwards.

Rejoue une capture dans le moteur de combat et écrit ce que l'écran HD aurait montré, seconde par seconde. Le même
moteur que sur la borne, avec le fichier du jeu tel qu'il est maintenant.

usage: python tools/replay_capture.py CAPTURE [--values] [--json OUT] [--frames T1,T2,...] [--out DIR]
  --values   also prints the changes of the main values (health, timer, round, screen, state) / les valeurs aussi
  --json     writes the timeline as JSON, for the tests / la chronologie en JSON
  --frames   draws the HD screen at these seconds of the capture, <capture>-<T>.png beside it or in --out
             / dessine l'écran HD à ces secondes de la capture
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


def replay(path, show_values=False, step=1 / 60, frames=(), out_dir=None):
    import pygame
    from dmd.canvas import Canvas
    from dmd.capture import read_capture
    from dmd.hd import GAME_SCENES, HDRenderer
    from dmd.hd_fight import FightFX
    from dmd.hd_mslug import family
    from dmd.memvalues import derive, resolve_value
    from dmd.scene import Ctx, GameState

    pygame.init()
    screen = pygame.display.set_mode((1920, 460))
    head, rows = read_capture(path)
    key = head.get("game") or ""
    game = json.load(open(os.path.join(ROOT, "games", f"{key}.json"), encoding="utf-8"))
    renames = game.get("capture_renames") if isinstance(game.get("capture_renames"), dict) else {}
    if renames:                                                      # values renamed since the capture (probes confirmed)
        rows = [(t, renames.get(n, n), v) for t, n, v in rows]       # / valeurs renommées depuis la capture
    derived = game.get("derived") or {}
    tag = game.get("tag") if isinstance(game.get("tag"), dict) else {}
    hd = HDRenderer(pygame, (1920, 460), ROOT, {"logos": False}, lambda *a: None, logos=None)
    # a game with a scene of its own (Windjammers, Metal Slug...): its scene is drawn at every image, as on the cabinet,
    # the fight screen otherwise / un jeu avec sa propre scène : elle est dessinée à chaque image, comme sur la borne
    scene_name = (game.get("hd") or {}).get("scene") if isinstance(game.get("hd"), dict) else None
    own_scene = scene_name in GAME_SCENES or bool(family(key))
    frames = sorted(float(f) for f in frames)
    out_dir = out_dir or os.path.dirname(os.path.abspath(path))
    stem = os.path.splitext(os.path.basename(path))[0]
    lines = []
    hd.log = lambda m: lines.append((T[0], str(m)))
    fx = FightFX(hd, rng=random.Random(1))
    hd.fight = fx
    st = GameState()
    st.reset({"game": key, "system": head.get("system") or key, "title": head.get("title") or key})
    T = [0.0]
    out = []
    state = {"select": False, "round_show": -99.0, "fight_t": -99.0, "ko": None, "win": None, "banner": None, "out": None,
             "next": {"p1": -99.0, "p2": -99.0}, "hold": {"p1": None, "p2": None}, "chars": {}, "pick": {}, "scene": {}}

    class _Lib:
        def get(self, k):
            return game if k == key else None

    class _Eng:                                                      # what the HD screen reads of the engine
        def __init__(self):
            self.state = st
            self.derived = derived
            self.library = _Lib()
            self.cfg = {"coin_symbol": "€"}
            self.ctx = Ctx(Canvas(), ROOT)
            self.ctx.t = 0.0
            self.mode = "game"
            self.intro_serial = 0
            self.coin_guess = None

    eng = _Eng()
    hd.clock = lambda: 1000.0 + T[0]

    def frame(now):
        """The HD screen as it was at now / l'écran HD tel qu'il était"""
        eng.ctx.t = now
        if not own_scene:
            v = dict(st.values)
            fx.bd.draw(screen, now)
            target = fx.begin(screen, now)
            hd.draw_fight(target, eng, v, None, now)
            fx.end(screen, target, now)
        name = os.path.join(out_dir, f"{stem}-{now - 1000.0:.1f}.png")
        pygame.image.save(screen, name)
        return name

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
        for k, spec in tag.items():                                 # the tags, from the raw values as the app does them
            v = resolve_value(spec, st.values)                      # (the capture holds those of its day) / les tags
            if v is not None and st.values.get(k) != v:
                st.update(k, v, t, quiet=True)
        vals = dict(st.values)
        vals.update(derive(derived, vals))
        for k, v in derive(derived, vals).items():
            if st.values.get(k) != v:
                st.update(k, v, t, quiet=True)
        T[0] = t
        eng.ctx.t = 1000.0 + t
        try:
            if own_scene:
                hd.render(screen, eng)                               # the scene sees every change / la scène voit tout
            else:
                fx.update(vals, 1000.0 + t, key, game, idle=HDRenderer._nobody(vals), hist=st.hist)
            if frames and t + 1e-9 >= frames[0]:
                frames.pop(0)
                note(t, "  image : " + frame(1000.0 + t))
        except Exception as e:                                       # noqa: BLE001
            note(t, f"ERREUR {e!r}")
            break
        if own_scene:                                                # its scene: the points, where its disc or hero is
            sc = hd.game_scene[1] if hd.game_scene else hd.mslug
            for name in ("set_points", "set_points_p2", "sets", "sets_p2", "lives", "score", "score_p2", "wins", "wins_p2", "round"):
                v = vals.get(name)
                if name in vals and v != state["scene"].get(name):
                    state["scene"][name] = v
                    track = getattr(sc, "track", None)
                    where = f" (disque HD à {int(track[0])},{int(track[1])})" if track else ""
                    note(t, f"  {name} = {v}{where}")
            for pside, suf in (("p1", ""), ("p2", "_p2")):            # Puzzle Bobble: the bubble in the launcher, the next
                if "bubble" + suf in vals:                             # / la bulle du lanceur, la suivante
                    pair = (vals.get("bubble" + suf), vals.get("bubble_next" + suf))
                    if pair != state["scene"].get(("bubble", pside)) and pair[0] is not None:
                        state["scene"][("bubble", pside)] = pair
                        note(t, f"  {pside} bulle {pair[0]}, suivante {pair[1]}")
            shots = getattr(sc, "shots", None)                       # the bubbles shot on the HD screen / les tirs
            if shots is not None and shots != state["scene"].get("_shots"):
                state["scene"]["_shots"] = shots
                note(t, "  tir")
            sup = getattr(sc, "super", None)                         # Windjammers: the supers, the charges (1.33)
            sup = sup[0] if isinstance(sup, tuple) else None
            if sup != state["scene"].get("_super"):
                state["scene"]["_super"] = sup
                if sup:
                    note(t, f"SUPER {sup.upper()}")
            for side, t0 in (getattr(sc, "charge", None) or {}).items():
                on = t0 is not None
                if on != state["scene"].get("_charge_" + side, False):
                    state["scene"]["_charge_" + side] = on
                    note(t, f"  {side} {'charge son super' if on else 'fin de la charge'}")
            if hasattr(sc, "continue_shown"):                        # CONTINUE ? shown or hidden (1.33 test 20)
                for side in ("p1", "p2"):
                    shown = vals.get(side + "_mode") == 2 and sc.banner is None and sc.continue_shown(side, vals, 1000.0 + t)
                    if shown != state["scene"].get("_cont_" + side, False):
                        state["scene"]["_cont_" + side] = shown
                        note(t, f"  CONTINUE ? {side} {'affiché' if shown else 'caché'}")
            wins = getattr(sc, "wins", None)
            if wins and (wins["p1"], wins["p2"]) != state["scene"].get("_wins", (0, 0)):
                state["scene"]["_wins"] = (wins["p1"], wins["p2"])
                note(t, f"MATCHS {wins['p1']} - {wins['p2']}")
            players = getattr(sc, "players", None)                   # Metal Slug: the soldiers, the vehicles, the boss
            if isinstance(players, dict) and hasattr(sc, "soldier"):  # / les soldats, les véhicules, le boss (test 21)
                for side, P in players.items():
                    name = sc.soldier(side, vals) if sc.playing(P) else None
                    if name != state["scene"].get("_name_" + side):
                        state["scene"]["_name_" + side] = name
                        if name:
                            note(t, f"  {side} {name}")
                    ride = P.ride if P.tank else None
                    if ride != state["scene"].get("_ride_" + side):
                        state["scene"]["_ride_" + side] = ride
                        note(t, f"  {side} {'monte dans ' + ride.upper() if ride else 'descend du véhicule'}")
                    code = vals.get("weapon" if side == "p1" else "weapon_p2")
                    wpn = sc.weapon(side, code)[0] if sc.playing(P) and isinstance(code, int) else None
                    if wpn != state["scene"].get("_wpn_" + side):
                        state["scene"]["_wpn_" + side] = wpn
                        if wpn:
                            note(t, f"  {side} arme : {wpn}")
                    pr = vals.get("prisoners" if side == "p1" else "prisoners_p2")
                    if pr != state["scene"].get("_pr_" + side) and sc.playing(P):
                        state["scene"]["_pr_" + side] = pr
                        note(t, f"  {side} prisonniers = {pr}")
                for pside, P in getattr(sc, "players", {}).items():      # the helmets shown, or LAST LIFE / les casques
                    nl = P.seen.get("lives") if getattr(P, "seen", None) else None
                    quiet = 1000.0 + t < P.sync_until                      # the scene's clock runs 1000 s ahead / l'horloge
                    unknown = nl is not None and nl <= 0 and not getattr(P, "lives_known", True) and 1000.0 + t - getattr(P, "lives_t0", P.join_t) < 12
                    last = nl is not None and nl <= 0 and P.mode == 1 and not quiet and not unknown
                    shown = "dernière vie" if last else (None if nl is None or quiet or unknown else f"{int(nl)} casque(s)")
                    if shown is not None and shown != state["scene"].get(("lives", pside)):
                        state["scene"][("lives", pside)] = shown
                        note(t, f"  {pside} vies : {shown}")
                for key, word in (("thrown", "grenade lancée"), ("booms", "grenade explose")):   # the grenades / les grenades
                    cnt = getattr(sc, key, None)
                    if cnt is not None and cnt != state["scene"].get(key, 0):
                        state["scene"][key] = cnt
                        note(t, f"  {word}")
                bph = (sc.boss or {}).get("phase") if isinstance(getattr(sc, "boss", None), dict) else None
                if bph != state["scene"].get("_phase"):                  # the boss's phases / les phases du boss
                    state["scene"]["_phase"] = bph
                    if bph and bph > 1:
                        note(t, f"BOSS {sc.boss.get('name')} phase {bph}")
                ct = getattr(sc, "complete_t", None)                     # MISSION COMPLETE, when the scene showed it
                if ct is not None and ct > 0 and ct != state["scene"].get("_complete"):   # / le bandeau de fin de mission
                    state["scene"]["_complete"] = ct
                    note(t, "MISSION COMPLETE")
                boss = getattr(sc, "boss", None)
                bkey = (boss["name"], boss["down"] is not None, bool(boss.get("minor"))) if boss else None
                if bkey != state["scene"].get("_boss"):
                    state["scene"]["_boss"] = bkey
                    what = "ENNEMI" if boss and boss.get("minor") else "BOSS"     # a big enemy or the boss / un gros ennemi ou le boss
                    if boss and boss["down"] is None:
                        note(t, f"{what} {boss['name'] or '?'} arrive (vie {boss['top']})")
                    elif boss:
                        note(t, f"{what} {boss['name'] or '?'} détruit")
                    else:
                        note(t, "  boss parti")
            t = round(t + step, 5)
            continue
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
        for side in ("p1", "p2"):                                    # the select screens: the picks shown (1.33)
            pick = hd.select_pick(eng, side) if fx.select and fx.sel_phase else None
            if pick != state["pick"].get(side):
                state["pick"][side] = pick
                if pick and pick[0]:
                    team = " ".join(n + ("*" if st_ == "now" else "") for n, st_ in (pick[1] or []))
                    note(t, f"  {side} à la sélection : {pick[0]} [{team}]")
                elif fx.select:
                    note(t, f"  {side} à la sélection : rien")
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
    ap.add_argument("--frames", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    head, out = replay(args.capture, args.values, frames=[f for f in args.frames.split(",") if f.strip()], out_dir=args.out or None)
    print(f"{head.get('game')} {head.get('title')} {head.get('date')} (ArcadeDMD {head.get('version')})")
    for t, what in out:
        print(f"{t:8.2f}  {what}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"head": head, "events": out}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
