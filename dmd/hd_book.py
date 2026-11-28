"""Trial: the book of moves of a fighter, in the fights without their stage.

In place of the desperation moves alone, the panel under a player's name lists every move of the fighter: the special
moves, each a card with its name over its command, and the desperation moves beside them. A move lights up arrow after
arrow as the stick does it. The desperation moves are pale until one can come out, then they come forward: wider and
bigger with two players, and bigger still when the player is alone, where they take the side nobody plays.
Turned on by ARCADEDMD_FIGHT_BOOK=1, to be shown before anything changes.

Essai : le carnet de coups d'un combattant, dans les combats sans décor. À la place des seuls coups désespérés, le
panneau sous le nom d'un joueur liste tous les coups du combattant : les coups spéciaux, chacun une carte avec son nom
au-dessus de sa commande, et les coups désespérés à côté. Un coup s'allume flèche après flèche quand le stick le fait.
Les coups désespérés sont pâles tant qu'aucun ne peut sortir, puis ils passent devant : plus larges et plus gros à deux
joueurs, et plus gros encore quand le joueur est seul, où ils prennent le côté sans joueur.
"""
import math

from .hd_moves import BTN_COL, CLASS, CREAM, GOLD, GREY, MIRROR, MISS, _plate, arrow, button, draw_panel
from .hd_specials import HOLD_COL, WHEN, _buttons, fighter_rows
from .hd_stick import progress, steps_of
from .i18n import tr

PALE = (150, 118, 70)             # a desperation move that cannot come out now / un coup désespéré pas possible


def _lerp(a, b, k):
    return a + (b - a) * k


def _width(slots, pluses, r, sp):
    return slots * (2 * r + sp) + pluses * (r * 1.6 + sp)


def _command(hd, screen, moves, x, y, r, sp, steps, groups, names, lit=0, states=None, held=(), bright=True, pulse=1.0):
    """A command on one line: its arrows, then its buttons. Returns where it ends. / Une commande sur une ligne."""
    pg = hd.pg
    for j, d in enumerate(steps):
        st = states[j] if states is not None and j < len(states) else ("ok" if j < lit else "dim")
        col = {"ok": GOLD, "miss": MISS}.get(st, HOLD_COL if j in held else (200, 205, 225))
        arrow(hd, screen, x + r, y, r, d, col, alpha=255 if st in ("ok", "miss") else 235 if bright else 120, moves=moves)
        if st == "miss":
            dd = r * 0.75
            pg.draw.line(screen, MISS, (x + r - dd, y - dd), (x + r + dd, y + dd), max(2, hd.S(3)))
            pg.draw.line(screen, MISS, (x + r - dd, y + dd), (x + r + dd, y - dd), max(2, hd.S(3)))
        x += 2 * r + sp
    for group in groups:
        hd.put(screen, hd.text("+", "black", max(hd.S(10), int(r * 1.4)), CREAM if bright else GREY, glow=0), x + r * 0.8, y,
               "center", "middle")
        x += r * 1.6 + sp
        for b in group:
            if b in BTN_COL:
                button(hd, screen, x + r, y, int(r * pulse), b, names, alpha=255 if bright else 120, moves=moves)
                x += 2 * r + sp
    return x


def _fit(hd, slots, pluses, room, r, least):
    """The biggest arrows that hold in the room, closer together when they must. / Les plus grosses flèches qui tiennent."""
    sp = hd.S(4)
    while r > least and _width(slots, pluses, r, sp) > room:
        r -= 1
    if _width(slots, pluses, r, sp) > room:
        sp = max(1, hd.S(2))
        while r > hd.S(6) and _width(slots, pluses, r, sp) > room:
            r -= 1
    return r, sp


def _specials(hd, screen, moves, sd, rows, mirrored, names, xa, xb, top, bottom, now):
    """The special moves, cards in one or two columns: the name over its command. / Les coups spéciaux, en cartes."""
    S, n = hd.S, len(rows)
    if not n:
        return
    cols = 2 if n > 4 else 1
    per = int(math.ceil(n / cols))
    cw, ch = (xb - xa) / cols, min(S(50), (bottom - top) / per)
    nf = max(S(11), min(S(20), int(ch * 0.38)))
    for i, row in enumerate(rows):
        c, k = divmod(i, per)
        x, y = xa + c * cw + S(6), top + k * ch
        steps = steps_of(row)
        if mirrored:
            steps = [MIRROR[d] for d in steps]
        held = set(row.get("hold") or [])
        lit = 0 if held or len(steps) < 2 else progress(steps, sd.dirs, now)
        groups = _buttons(row.get("btn", ""))
        slots = len(steps) + sum(len(g) for g in groups)
        r, sp = _fit(hd, slots, len(groups), cw - S(16), min(S(16), int(ch * 0.27)), S(8))
        title = str(row.get("name", ""))
        when = WHEN.get(row.get("when"))
        size = hd.fit_size(title, "xbold", nf, cw - S(16), S(9))
        hd.put(screen, hd.text(title, "xbold", size, GOLD if lit >= 2 else CREAM, glow=0), x, y + ch * 0.26, "left", "middle")
        ready = lit >= len(steps) > 1
        end = _command(hd, screen, moves, x, y + ch * 0.70, r, sp, steps, groups, names, lit=lit, held=held,
                       pulse=1.0 + 0.12 * math.sin(now * 16) if ready else 1.0)
        if when:                                                  # in the air, close: after its buttons / après ses boutons
            wt = hd.text(tr(*when), "xbold", max(S(9), int(nf * 0.66)), GREY, glow=0)
            if end + S(8) + wt["w"] <= xa + (c + 1) * cw - S(4):
                hd.put(screen, wt, end + S(8), y + ch * 0.70, "left", "middle")


def _states(moves, side, rows, avail, now):
    out = []
    for k, (nm, cmd, btn) in enumerate(rows):
        states, tag, tcol, mir = moves.row_states(side, k, len(cmd), now)
        if not avail:                                             # none can come out now: nothing lit / rien d'allumé
            states, tag = ["dim"] * len(cmd), None
        steps = [MIRROR[c] for c in cmd] if mir else list(cmd)
        out.append((nm, steps, states, tag, tcol, [[b for b in CLASS.get(btn, btn) if b in BTN_COL]]))
    return out


def _cards(hd, screen, moves, lines, avail, maxed, names, xa, xb, top, bottom, now, k):
    """The desperation moves beside the special moves, each a card. / Les coups désespérés à côté, chacun une carte."""
    S, n = hd.S, len(lines)
    ch = min(S(62), (bottom - top) / n)
    nf = int(_lerp(S(14), S(19), k))
    for i, (nm, steps, states, tag, tcol, groups) in enumerate(lines):
        x, y = xa + S(8), top + i * ch
        lit = tag is not None or any(st == "ok" for st in states)
        if avail:                                                 # one can come out: the card comes forward / passe devant
            beat = 0.5 + 0.5 * math.sin(now * 5.0 + i)
            plate = _plate(moves, hd, int(xb - xa), int(ch - S(4)), GOLD, S(10), fill=(255, 214, 120, 26))
            plate.set_alpha(int(150 + 90 * beat * k))
            screen.blit(plate, (int(xa), int(y + S(2))))
        col = (GOLD if maxed or lit else CREAM) if avail else PALE
        size = hd.fit_size(nm, "xbold", nf, xb - xa - S(70), S(9))
        w = hd.put(screen, hd.text(nm, "xbold", size, col, glow=0.3 if avail else 0), x, y + ch * 0.28, "left", "middle")
        if tag:
            hd.put(screen, hd.text(tag, "black", S(18), tcol, glow=0.4), x + w + S(10), y + ch * 0.28, "left", "middle")
        slots = len(steps) + sum(len(g) for g in groups)
        r, sp = _fit(hd, slots, len(groups), xb - xa - S(18), min(int(_lerp(S(11), S(17), k)), int(ch * 0.27)), S(7))
        _command(hd, screen, moves, x, y + ch * 0.70, r, sp, steps, groups, names, states=states, bright=avail)


def _plate_dm(hd, screen, moves, lines, avail, maxed, names, who, color, x0, x1, y0, y1, now, k):
    """A player alone: his desperation moves on the side nobody plays, bigger when one can come out.
    / Un joueur seul : ses coups désespérés du côté sans joueur, plus gros quand l'un d'eux peut sortir."""
    S, n = hd.S, len(lines)
    edge = GOLD if avail else (120, 90, 40)
    screen.blit(_plate(moves, hd, int(x1 - x0), int(y1 - y0), edge, S(18)), (int(x0), int(y0)))
    word = tr(f"COUPS DÉSESPÉRÉS DE {who}", f"DESPERATION MOVES OF {who}")
    t = hd.text(word, "black", S(18), (10, 14, 28), glow=0)
    bw, bh = int(t["w"] + S(22)), S(26)
    screen.blit(_plate(moves, hd, bw, bh, color, bh // 2, fill=(*color, 255)), (int(x0 + S(14)), int(y0 - bh / 2)))
    hd.put(screen, t, x0 + S(14) + bw / 2, y0, "center", "middle")
    top, bottom = y0 + S(18), y1 - S(6)
    ch = (bottom - top) / n
    nf = int(_lerp(S(16), S(30), k))
    nroom = S(280)
    for i, (nm, steps, states, tag, tcol, groups) in enumerate(lines):
        y = top + (i + 0.5) * ch
        lit = tag is not None or any(st == "ok" for st in states)
        col = (GOLD if maxed or lit else CREAM) if avail else PALE
        size = hd.fit_size(nm, "xbold", nf, nroom, S(11))
        hd.put(screen, hd.text(nm, "xbold", size, col, glow=0.35 if avail else 0), x0 + S(16) + nroom, y, "right", "middle")
        slots = len(steps) + sum(len(g) for g in groups)
        tagw = S(86)
        r, sp = _fit(hd, slots, len(groups), x1 - x0 - nroom - S(44) - tagw, min(int(_lerp(S(11), S(20), k)), int(ch * 0.42)), S(8))
        x = _command(hd, screen, moves, x0 + S(28) + nroom, y, r, sp, steps, groups, names, states=states, bright=avail)
        if tag:
            hd.put(screen, hd.text(tag, "black", S(24), tcol, glow=0.4), x + S(8), y, "left", "middle")


def draw_book(hd, header, screen, moves, side, vals, game, name, x0, x1, y0, y1, now, lost, health, free=None, color=CREAM):
    """The panel of a player with every move of his fighter. header: the marquee as draw_panel must see it to draw
    the badge, the gauge and the inputs alone, on the top edge. free: (x0, x1, y0, y1) the room on the side nobody
    plays, or None with two players. / Le panneau d'un joueur avec tous les coups de son combattant."""
    S = hd.S
    book = {"h": y1 - y0}
    header.book = book
    draw_panel(header, screen, moves, side, vals, game, name, x0, x1, y0, now, lost, health)
    if "rows" not in book:                                        # no move known for this fighter: the panel as it was
        return
    rows, avail, maxed, names, sd = book["rows"], book["avail"], book["maxed"], book["names"], book["sd"]
    ease = hd.book_k.setdefault(side, [0.0, now])                 # the desperation moves come forward in a third of a second
    ease[0] += ((1.0 if avail else 0.0) - ease[0]) * min(1.0, max(0.0, now - ease[1]) * 9.0)
    ease[1] = now
    k = ease[0]
    lines = _states(moves, side, rows, avail, now)
    mirrored = moves.row_states(side, len(rows) + 1, 1, now)[3] if not sd.live and not sd.attempt else side == "p2"
    specials, _ = fighter_rows(game, name)
    top, bottom = y0 + S(24), y1 - S(6)
    if free is None:
        wd = _lerp(S(252), S(350), k)
        _cards(hd, screen, moves, lines, avail, maxed, names, x1 - S(8) - wd, x1 - S(8), top, bottom, now, k)
        _specials(hd, screen, moves, sd, specials, mirrored, names, x0 + S(8), x1 - S(16) - wd, top, bottom, now)
    else:
        _specials(hd, screen, moves, sd, specials, mirrored, names, x0 + S(8), x1 - S(8), top, bottom, now)
        _plate_dm(hd, screen, moves, lines, avail, maxed, names, str(name).upper(), color, free[0], free[1], free[2], free[3], now, k)
