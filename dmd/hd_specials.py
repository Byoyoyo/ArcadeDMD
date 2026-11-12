"""Special moves and supers under a human player's name, for every fighting game (1.38).

The moves of each fighter come from "specials" in the game file (made from MAME's command list by tools/command_dat.py):
the special moves, always possible, and the supers, possible when the game says (its gauge full, its POW at MAX...).
Under the name, a panel as the one of The King of Fighters '98: the badge says what can come out, the gauge as the game
fills it when it is read, and one move after another, its name, its arrows (facing the other fighter) and its buttons.
When the gauge allows a super, only the supers, in gold. A game whose gauge is not read shows its supers among the others.

Les coups spéciaux et les supers sous le nom d'un joueur humain, pour tous les jeux de combat. Sous le nom, un panneau
comme celui de King of Fighters '98 : la pastille dit ce qui peut sortir, la jauge comme le jeu la remplit quand elle est
lue, et un coup après l'autre, son nom, ses flèches (tournées vers l'autre combattant) et ses boutons. Quand la jauge
permet un super, seulement les supers, en or. Un jeu dont la jauge n'est pas lue montre ses supers parmi les autres."""
import math

from .hd_moves import BTN_COL, CREAM, GOLD, GREY, MIRROR, _icon, _plate, arrow, button
from .i18n import tr

TURN = 2.8                # each move shown this long / chaque coup montré ce temps
FADE = 0.25               # its arrival and departure / son arrivée et son départ
HOLD_COL = (90, 200, 255)     # a direction held (charge) / une direction tenue (charge)
PUNCH_COL = (60, 120, 235)
KICK_COL = (225, 70, 55)
OTHER_COL = (120, 128, 150)
WHEN = {"close": ("PRÈS", "CLOSE"), "far": ("LOIN", "FAR"), "air": ("EN L'AIR", "IN THE AIR"), "run": ("EN COURANT", "RUNNING"),
        "crouch": ("ACCROUPI", "CROUCHING")}


def _n(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def fighter_rows(game, name):
    """(specials, supers) of the fighter, from "specials" in the game file. / Les coups du combattant."""
    sp = (game or {}).get("specials") if isinstance(game, dict) else None
    if not isinstance(sp, dict) or not isinstance(name, str) or not name:
        return [], []
    rows = sp.get(name.upper().lstrip("#")) or []
    rows = [r for r in rows if isinstance(r, dict) and r.get("btn")]
    return [r for r in rows if r.get("kind") != "super"], [r for r in rows if r.get("kind") == "super"]


def hyper_rows(game, name, level):
    """The supers of a game whose gauge has levels ("hyper", 1.36), those its level allows. / Ceux que le niveau permet."""
    hy = (game or {}).get("hyper") if isinstance(game, dict) else None
    moves = hy.get("moves") if isinstance(hy, dict) else None
    if not isinstance(moves, dict) or not isinstance(name, str):
        return []
    out = []
    for m in moves.get(name.upper()) or []:
        if isinstance(m, dict) and m.get("cmd") and (level is None or (_n(m.get("lv")) or 1) <= level):
            btn = m.get("btn", "")
            out.append({"name": m.get("name", ""), "cmd": m.get("cmd"), "label": tr(*btn) if isinstance(btn, list) else btn,
                        "kind": "super"})
    return out


def power_label(game):
    """The gauge's name in the game ("power_label" in hd: POW in Samurai Shodown), else SUPER. / Le nom de la jauge."""
    hd = (game or {}).get("hd") if isinstance(game, dict) else None
    v = hd.get("power_label") if isinstance(hd, dict) else None
    if isinstance(v, list) and len(v) == 2:
        return tr(*v)
    return v if isinstance(v, str) and v else "SUPER"


def timer_name(game):
    """The value of the game's MAX timer ("power_timer" in hd: "_powmax"), or None. / La valeur du chrono du MAX."""
    hd = (game or {}).get("hd") if isinstance(game, dict) else None
    v = hd.get("power_timer") if isinstance(hd, dict) else None
    return v if isinstance(v, str) and v else None


class Specials:
    """What the panel of each side needs between two images: the MAX timer at its start. / Le chrono du MAX à son début."""

    def __init__(self):
        self.peak = {"p1": None, "p2": None}
        self.ready_t = {"p1": -99.0, "p2": -99.0}
        self.was = {"p1": False, "p2": False}

    def gauge(self, vals, side, game, top=None):
        """(fill 0..1 or None, ready True/False/None, level text). / Le remplissage, si un super peut sortir, le niveau."""
        suf = "" if side == "p1" else "_p2"
        p = _n(vals.get("power" + suf))
        lv = _n(vals.get("power_level" + suf))
        tn = timer_name(game)
        tv = _n(vals.get(tn + suf)) if tn else None
        if tv is not None and tv > 0:                             # MAX: its timer in the bar, as the game shows it
            pk = self.peak.get(side)                              # le MAX : son chrono dans la barre, comme le jeu
            if pk is None or tv > pk:
                self.peak[side] = pk = tv
            return max(0.0, min(1.0, tv / pk)), True, None
        self.peak[side] = None
        if p is None:
            return None, None, None
        f = max(0.0, min(1.0, p / 100.0))
        hy = (game or {}).get("hyper") if isinstance(game, dict) else None
        frm = _n(hy.get("from")) if isinstance(hy, dict) else None
        if lv is not None and top and lv >= top:
            f = 1.0                                               # the top level: full / le niveau le plus haut : pleine
        if frm is not None and lv is not None:
            ready = lv >= frm
        else:
            ready = f >= 0.999 and (lv is None or not top or lv >= top)
        level = None if lv is None else ("MAX" if top and lv >= top else str(int(lv)))
        return f, ready, level


def _family(label):
    u = label.upper()
    if "K" in u and "P" not in u:
        return KICK_COL
    if "P" in u:
        return PUNCH_COL
    return OTHER_COL


def chip(hd, surf, cx, cy, r, label, alpha, cache):
    """A button that is not a Neo Geo letter: P, K, LP, PPP... in a disc of its family's colour. / Un bouton d'un autre jeu."""
    pg = hd.pg
    c = r + 2

    def make():
        col = _family(label)
        tmp = pg.Surface((2 * r + 4, 2 * r + 4), pg.SRCALPHA)
        pg.draw.circle(tmp, (*col, 255), (c, c), r)
        pg.draw.circle(tmp, (255, 255, 255, 200), (c, c), r, max(2, hd.S(2)))
        t = hd.text(label, "black", int(r * (1.2 if len(label) == 1 else 0.95 if len(label) == 2 else 0.72)), (255, 255, 255), glow=0)
        hd.put(tmp, t, c, c + 1, "center", "middle")
        return tmp
    tmp = _icon(cache, ("c", label, r), make) if cache is not None else make()
    tmp.set_alpha(alpha)
    surf.blit(tmp, (int(cx - c), int(cy - c)))


def _buttons(btn):
    """'A/B' -> [['A', 'B']], 'B+C' -> [['B'], ['C']]: the groups pressed together, each its alternatives.
    / Les groupes appuyés ensemble, chacun avec ses possibilités."""
    return [[x for x in g.split("/") if x] for g in str(btn).split("+") if g]


def draw_specials(hd, screen, cache, state, side, vals, game, name, x0, x1, y0, now, top=None):
    """The panel under a human's name. Returns its height, 0 when the fighter has no move known.
    / Le panneau sous le nom d'un humain. Renvoie sa hauteur, 0 quand le combattant n'a aucun coup connu."""
    pg, S = hd.pg, hd.S
    specials, supers = fighter_rows(game, name)
    fill, ready, level = state.gauge(vals, side, game, top)
    lv = _n(vals.get("power_level" + ("" if side == "p1" else "_p2")))
    hyper = hyper_rows(game, name, lv)
    if ready and not state.was.get(side):
        state.ready_t[side] = now                                 # the super just came: the panel flashes / il vient
    state.was[side] = bool(ready)
    if ready:
        rows = hyper or supers or specials
    elif ready is None:
        rows = specials + supers                                  # no gauge read: all of them / sans jauge lue : tous
    else:
        rows = specials or supers
    if not rows:
        return 0
    n = len(rows)
    i, ph = int(now // TURN) % n, now % TURN
    a = 1.0 if n == 1 else max(0.0, min(1.0, ph / FADE, (TURN - ph) / FADE))
    row = rows[i]
    sup = row.get("kind") == "super"
    gold = bool(ready) or sup
    h = S(64)
    k = 0.5 + 0.5 * math.sin(now * 7)
    flash = max(0.0, 1.0 - (now - state.ready_t.get(side, -99.0)) / 0.8)
    edge = GOLD if ready else (120, 90, 40)
    screen.blit(_plate(cache, hd, int(x1 - x0), int(h), edge, S(18)), (int(x0), int(y0)))
    if ready:                                                     # MAX: the edge glows / le MAX : le bord brille
        glow = _plate(cache, hd, int(x1 - x0 + S(10)), int(h + S(10)), GOLD, S(22), fill=(255, 214, 120, 40))
        glow.set_alpha(int(110 + 100 * k + 120 * flash))
        screen.blit(glow, (int(x0 - S(5)), int(y0 - S(5))))
    # the badge: what can come out / la pastille : ce qui peut sortir
    plabel = power_label(game)
    if ready:
        word = f"{plabel} MAX" if plabel != "SUPER" else ("POWER MAX" if level == "MAX" else "SUPER")
    elif sup:
        word = "SUPER"
    else:
        word = tr("COUP SPÉCIAL", "SPECIAL MOVE")
    bcol, ink = (GOLD, (40, 24, 0)) if gold else (CREAM, (10, 14, 28))
    t = hd.text(word, "black", S(20), ink, glow=0)
    bw, bh = int(t["w"] + S(20)), S(26)
    screen.blit(_plate(cache, hd, bw, bh, bcol, bh // 2, fill=(*bcol, 255)), (int(x0 + S(14)), int(y0 - bh / 2)))
    hd.put(screen, t, x0 + S(14) + bw / 2, y0, "center", "middle")
    y = y0 + S(36)
    x = x0 + S(20)
    if fill is not None:                                          # the gauge as the game fills it / la jauge du jeu
        gbw, gbh = S(150), S(18)
        pg.draw.rect(screen, (24, 26, 40), (x, y - gbh / 2, gbw, gbh), border_radius=S(3))
        fw = int(gbw * fill)
        if fw > 0:
            col = (255, int(190 + 50 * k), int(40 + 80 * k)) if ready else (255, 110, 30)
            pg.draw.rect(screen, col, (x, y - gbh / 2, fw, gbh), border_radius=S(3))
            for j in range(1, 6):
                sx = x + j * gbw / 6
                if sx < x + fw:
                    pg.draw.line(screen, (150, 110, 40) if ready else (120, 40, 10), (sx, y - gbh / 2 + 2), (sx, y + gbh / 2 - 2), 1)
        pg.draw.rect(screen, (150, 170, 210), (x, y - gbh / 2, gbw, gbh), max(1, S(2)), border_radius=S(3))
        x += gbw + S(10)
        if level is not None and level != "MAX":                  # its level (Marvel, X-Men) / son niveau
            x += hd.put(screen, hd.text(f"LV {level}", "xbold", S(17), CREAM, glow=0), x, y, "left", "middle")
        x += S(14)
    # the move: its name, its arrows, its buttons / le coup : son nom, ses flèches, ses boutons
    names = (game or {}).get("buttons") if isinstance(game, dict) else None
    names = names if isinstance(names, dict) else {}
    cmd = [int(c) for c in str(row.get("cmd", "")) if c.isdigit() and c not in "05"]
    if side == "p2":                                              # P2 on the right faces left / P2 regarde à gauche
        cmd = [MIRROR[c] for c in cmd]
    held = set(row.get("hold") or [])
    label = row.get("label")
    groups = [] if label else _buttons(row.get("btn", ""))
    when = WHEN.get(row.get("when"))
    dots_w = n * S(14) + S(8) if n > 1 else 0
    room = x1 - S(16) - dots_w - x
    r, sp = S(16), S(5)

    def needs(r, nsize):
        w = hd.text_width(str(row.get("name", "")), "xbold", nsize) + S(16)
        if when:
            w += hd.text_width(tr(*when), "xbold", S(15)) + S(10)
        w += len(cmd) * (2 * r + sp) + (r * 1.4 + S(4) if cmd else 0)
        if label:
            w += hd.text_width(label, "xbold", S(19))
        else:
            for g in groups:
                w += len(g) * (2 * r + sp) + (len(g) - 1) * S(10) + r * 1.4
        if row.get("rapid"):
            w += hd.text_width(tr("RAPIDE", "RAPID"), "xbold", S(15)) + S(8)
        return w
    nsize = S(23)
    while nsize > S(13) and needs(r, nsize) > room:
        nsize -= 1
    while r > S(9) and needs(r, nsize) > room:
        r -= 1
    alpha = int(255 * a)
    dy = (1 - a) * S(6)                                           # it rises a little as it comes / il monte en arrivant
    yy = y + dy
    ncol = (255, int(214 + 30 * k), 120) if gold else CREAM
    x += hd.put(screen, hd.text(str(row.get("name", "")), "xbold", nsize, ncol, glow=0), x, yy, "left", "middle", alpha=a) + S(16)
    if when:
        x += hd.put(screen, hd.text(tr(*when), "xbold", S(15), GREY, glow=0), x, yy, "left", "middle", alpha=a) + S(10)
    for j, d in enumerate(cmd):
        col = HOLD_COL if j in held else (GOLD if gold else (200, 205, 225))
        arrow(hd, screen, x + r, yy, r, d, col, alpha=alpha, moves=cache)
        if j in held:                                             # held: two dots under it / tenue : deux points dessous
            for q in (-1, 1):
                pg.draw.circle(screen, HOLD_COL, (int(x + r + q * S(5)), int(yy + r + S(5))), max(2, S(2)))
        x += 2 * r + sp
    if cmd:
        hd.put(screen, hd.text("+", "black", max(S(12), int(r * 1.45)), CREAM, glow=0), x + r * 0.5, yy, "center", "middle", alpha=a)
        x += r * 1.4 + S(4)
    if label:                                                     # "+ 3 PUNCHES" as the game file says / comme le dit le fichier
        x += hd.put(screen, hd.text(str(label).lstrip("+ ").strip(), "xbold", S(19), CREAM, glow=0), x, yy, "left", "middle", alpha=a)
    for gi, g in enumerate(groups):
        if gi:
            hd.put(screen, hd.text("+", "black", max(S(12), int(r * 1.3)), CREAM, glow=0), x + r * 0.45, yy, "center", "middle", alpha=a)
            x += r * 1.4
        for bi, b in enumerate(g):
            if bi:                                                # either one / l'un ou l'autre
                hd.put(screen, hd.text("/", "xbold", max(S(12), int(r * 1.1)), GREY, glow=0), x + S(2), yy, "center", "middle", alpha=a)
                x += S(10)
            if b in BTN_COL:
                button(hd, screen, x + r, yy, r, b, names, alpha=alpha, moves=cache)
            else:
                chip(hd, screen, x + r, yy, r, b, alpha, cache)
            x += 2 * r + sp
    if row.get("rapid"):
        x += hd.put(screen, hd.text(tr("RAPIDE", "RAPID"), "xbold", S(15), GREY, glow=0), x + S(4), yy, "left", "middle", alpha=a)
    if n > 1:                                                     # a dot per move, the one shown lit / un point par coup
        for j in range(n):
            cx = x1 - S(16) - (n - 1 - j) * S(14)
            on = j == i
            c = (GOLD if rows[j].get("kind") == "super" or ready else CREAM) if on else (90, 96, 120)
            pg.draw.circle(screen, c, (int(cx), int(y)), S(4) if on else S(3))
    return h
