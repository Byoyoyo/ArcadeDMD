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

PALE = (176, 138, 82)             # a desperation move that cannot come out now / un coup désespéré pas possible


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
        arrow(hd, screen, x + r, y, r, d, col, alpha=255 if st in ("ok", "miss") else 235 if bright else 150, moves=moves)
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
                button(hd, screen, x + r, y, int(r * pulse), b, names, alpha=255 if bright else 150, moves=moves)
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


def _wide(hd, text, size):
    """The width of a name at a size, kept. / La largeur d'un nom à une taille, gardée."""
    key = (text, size)
    w = hd.book_w.get(key)
    if w is None:
        if len(hd.book_w) > 4000:
            hd.book_w.clear()
        l, _, r, _ = hd.font("xbold", size).getbbox(text) if text else (0, 0, 0, 0)
        w = hd.book_w[key] = r - l
    return w


def _name(hd, text, size, room, least):
    """A name that holds in its room: smaller down to the least size a player still reads, then cut short.
    / Un nom qui tient dans sa place : plus petit jusqu'à la plus petite taille lisible, puis coupé."""
    while size > least and _wide(hd, text, size) > room:
        size -= 1
    if _wide(hd, text, size) > room:
        cut = text
        while len(cut) > 3 and _wide(hd, cut.rstrip() + "…", size) > room:
            cut = cut[:-1]
        text = cut.rstrip() + "…"
    return text, size


def _columns(hd, cards, room, height):
    """One, two or three columns: the count that leaves the cards their biggest arrows and letters. A column is as
    wide as its longest card asks, and the room is shared when they ask for more than there is. Returns the height of
    a card and, for each card, its column, its row, its left edge, its width, its name, the size of its letters, the
    radius of its arrows and their gap.
    / Une, deux ou trois colonnes : le nombre qui laisse aux cartes leurs plus grosses flèches et leurs plus grosses
    lettres. Une colonne est aussi large que sa carte la plus longue le demande, et la place est partagée quand elles
    en demandent trop."""
    S, n, best = hd.S, len(cards), None
    for cols in (1, 2, 3):
        per = int(math.ceil(n / cols))
        if cols > 1 and per * (cols - 1) >= n:                    # a column would stay empty / une colonne resterait vide
            continue
        ch = min(S(56), height / per)
        nf = max(S(11), min(S(21), int(ch * 0.38)))
        r0 = min(S(16), int(ch * 0.27))
        need = [max(max(_wide(hd, title, nf), _width(slots, len(groups), r0, S(4)))
                    for _, _, groups, slots, title in cards[c * per:(c + 1) * per]) + S(18) for c in range(cols)]
        wide = [w * room / sum(need) for w in need] if sum(need) > room else [w + (room - sum(need)) / cols for w in need]
        out, cut = [], False
        for i, (_, _, groups, slots, title) in enumerate(cards):
            c, k = divmod(i, per)
            cw = int(wide[c])
            r, sp = _fit(hd, slots, len(groups), cw - S(16), r0, S(8))
            text, size = _name(hd, title, nf, cw - S(16), S(12))
            cut = cut or text != title
            out.append((c, k, sum(wide[:c]), cw, text, size, r, sp))
        score = 1.5 * min(o[6] for o in out) + min(o[5] for o in out) - (3 if cut else 0)
        if best is None or score > best[0] + 0.5:
            best = (score, ch, nf, per, out)
    return best[1:]


def _specials(hd, screen, moves, sd, rows, mirrored, names, xa, xb, top, bottom, now):
    """The special moves, cards in columns: the name over its command. / Les coups spéciaux, en cartes."""
    S = hd.S
    if not rows:
        return
    cards = []
    for row in rows:
        steps = steps_of(row)
        if mirrored:
            steps = [MIRROR[d] for d in steps]
        groups = _buttons(row.get("btn", ""))
        cards.append((row, steps, groups, len(steps) + sum(len(g) for g in groups), str(row.get("name", ""))))
    key = (tuple(c[4] for c in cards), mirrored, int(xb - xa), int(bottom - top))
    lay = hd.book_lay.get(key)
    if lay is None:
        if len(hd.book_lay) > 400:
            hd.book_lay.clear()
        lay = hd.book_lay[key] = _columns(hd, cards, int(xb - xa), bottom - top)
    ch, nf, per, places = lay
    top += max(0, (bottom - top - per * ch) / 2)                  # fewer rows than the room: in its middle / au milieu
    for (row, steps, groups, slots, _), (c, k, left, cw, title, size, r, sp) in zip(cards, places):
        x, y = xa + left + S(6), top + k * ch
        held = set(row.get("hold") or [])
        lit = 0 if held or len(steps) < 2 else progress(steps, sd.dirs, now)
        when = WHEN.get(row.get("when"))
        hd.put(screen, hd.text(title, "xbold", size, GOLD if lit >= 2 else CREAM, glow=0), x, y + ch * 0.26, "left", "middle")
        ready = lit >= len(steps) > 1
        end = _command(hd, screen, moves, x, y + ch * 0.70, r, sp, steps, groups, names, lit=lit, held=held,
                       pulse=1.0 + 0.12 * math.sin(now * 16) if ready else 1.0)
        if when:                                                  # in the air, close: after its buttons / après ses boutons
            wt = hd.text(tr(*when), "xbold", max(S(9), int(nf * 0.66)), GREY, glow=0)
            if end + S(8) + wt["w"] <= xa + left + cw - S(4):
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
    nf = int(_lerp(S(15), S(19), k))
    for i, (nm, steps, states, tag, tcol, groups) in enumerate(lines):
        x, y = xa + S(8), top + i * ch
        lit = tag is not None or any(st == "ok" for st in states)
        if avail:                                                 # one can come out: the card comes forward / passe devant
            beat = 0.5 + 0.5 * math.sin(now * 5.0 + i)
            plate = _plate(moves, hd, int(xb - xa), int(ch - S(4)), GOLD, S(10), fill=(255, 214, 120, 26))
            plate.set_alpha(int(150 + 90 * beat * k))
            screen.blit(plate, (int(xa), int(y + S(2))))
        col = (GOLD if maxed or lit else CREAM) if avail else PALE
        nm, size = _name(hd, nm, nf, int(xb - xa) - (S(70) if tag else S(18)), S(12))
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
    # the names take the room of the longest, no more, so a long command keeps big arrows
    # les noms prennent la place du plus long, pas plus, pour qu'une longue commande garde de grosses flèches
    nroom = min(S(280), max(_wide(hd, nm, nf) for nm, *_ in lines) + S(4))
    tagw, fits = S(86), []
    for nm, steps, states, tag, tcol, groups in lines:
        slots = len(steps) + sum(len(g) for g in groups)
        r, sp = _fit(hd, slots, len(groups), x1 - x0 - nroom - S(44) - tagw, min(int(_lerp(S(11), S(20), k)), int(ch * 0.42)), S(8))
        fits.append((r, sp, _width(slots, len(groups), r, sp)))
    xn = x0 + S(16) + nroom + max(0, (x1 - x0 - S(44) - nroom - tagw - max(f[2] for f in fits)) / 2)   # in the middle of the plate
    for i, (nm, steps, states, tag, tcol, groups) in enumerate(lines):
        y = top + (i + 0.5) * ch
        lit = tag is not None or any(st == "ok" for st in states)
        col = (GOLD if maxed or lit else CREAM) if avail else PALE
        nm, size = _name(hd, nm, nf, nroom, S(12))
        hd.put(screen, hd.text(nm, "xbold", size, col, glow=0.35 if avail else 0), xn, y, "right", "middle")
        r, sp, _ = fits[i]
        x = _command(hd, screen, moves, xn + S(12), y, r, sp, steps, groups, names, states=states, bright=avail)
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
