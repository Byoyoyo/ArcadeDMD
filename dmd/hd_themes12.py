"""Backdrops of the Capcom CPS beat'em ups (1.30), drawn by the program after screenshots of the games: the slum of
a big American city, a city of the future, a jungle town among ruins, a luxury mansion at night, a forest of huge
trees, a village of half-timbered houses, a forest of ancient China, a canyon, green hills with a far town, a ruined
industrial city, a hangar of war machines and an arena of the future. Everything is drawn by the program, no image
comes from a game. The backdrops register in hd_bg.BUILDERS when this module is imported (by hd_panels).

Décors des beat'em ups Capcom CPS (1.30), dessinés par le programme d'après des captures des jeux. Tout est dessiné
par le programme, aucune image ne vient d'un jeu.
"""

import math
import random

from . import hd_bg
from .hd_bg import mix, periodic, vgrad
from .hd_themes3 import _clump, _fit, _Pic, _rgba
from .hd_themes5 import BRAWL_FLOOR

INK = (30, 24, 28, 255)


def _rect(p, x0, y0, x1, y1, fill, outline=None, width=0):
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], _rgba(fill) if len(fill) == 3 else fill, outline, width)


def _bricks(p, x0, y0, x1, y1, s, col, row=14, brick=34):
    """Brick courses drawn as mortar lines on a wall. / Les rangs de briques, des joints sur un mur."""
    joint = _rgba(mix(col, (0, 0, 0), 0.28), 200)
    y, k = y0, 0
    while y < y1:
        p.line([(x0, y), (x1, y)], joint, 1.2 * s)
        x = x0 + (brick * s / 2 if k % 2 else 0)
        while x < x1:
            p.line([(x, y), (x, min(y1, y + row * s))], joint, 1.2 * s)
            x += brick * s
        y += row * s
        k += 1


def _sky_towers(rng, tw, H, s, col, win, base, hmin, hmax, wmin=60, wmax=140, gap=(10, 50), lit=0.25):
    """A row of far towers with their windows. / Une rangée de tours au loin et leurs fenêtres."""
    far = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw - wmin * s:
        w = min(rng.uniform(wmin, wmax) * s, tw - x - 2 * s)
        h = rng.uniform(hmin, hmax) * s
        _rect(far, x, base - h, x + w, base, col)
        if rng.random() < 0.4:                                          # une antenne ou un toit en gradins
            _rect(far, x + w * 0.3, base - h - 18 * s, x + w * 0.7, base - h, col)
        for wy in range(int(base - h + 8 * s), int(base - 6 * s), int(14 * s)):
            for wx in range(int(x + 6 * s), int(x + w - 8 * s), int(12 * s)):
                if rng.random() < lit:
                    _rect(far, wx, wy, wx + 6 * s, wy + 7 * s, win)
        x += w + rng.uniform(*gap) * s
    return far


# ---------------------------------------------------------------------------- Final Fight
def build_ff_slum(W, H, s, seed=1201):
    """Final Fight: the slum of a big American city by day, as in the first stage: the towers of downtown far off in a
    pale blue sky, the old pinkish brick tenements with their dark doorways, broken and boarded windows, the iron fire
    escapes, posters and oil drums, the grey tiled sidewalk. / Le quartier pauvre d'une grande ville américaine de jour :
    les tours au loin, les vieux immeubles de briques rosées, portes sombres, fenêtres cassées, escaliers de secours."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (120, 170, 230)), (0.5, (190, 215, 240)), (1.0, (220, 225, 235))])
    layers = [{"img": _sky_towers(rng, tw, H, s, (150, 170, 200, 255), (210, 225, 245, 255), base - 40 * s, 120, 260).done(),
               "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw - 200 * s:
        w = min(rng.uniform(380, 560) * s, tw - x)
        top = rng.uniform(-20, 40) * s
        wall = rng.choice(((196, 150, 150), (178, 136, 140), (204, 168, 156), (170, 150, 160)))
        _rect(mid, x, top, x + w, base, wall, INK, 2 * s)
        _bricks(mid, x, top, x + w, base, s, wall)
        _rect(mid, x - 6 * s, top, x + w + 6 * s, top + 16 * s, mix(wall, (0, 0, 0), 0.35))      # la corniche
        door = x + w * rng.uniform(0.38, 0.5)
        _rect(mid, door, base - 150 * s, door + 92 * s, base, (36, 26, 30), INK, 2 * s)         # la porte sombre
        _rect(mid, door - 10 * s, base - 160 * s, door + 102 * s, base - 150 * s, mix(wall, (0, 0, 0), 0.4))
        for wx in (x + w * 0.1, x + w * 0.72):                           # fenêtres cassées ou condamnées
            for wy in (top + 40 * s, top + 140 * s):
                if wy + 70 * s > base - 60 * s:
                    continue
                _rect(mid, wx, wy, wx + 70 * s, wy + 74 * s, (60, 70, 90), INK, 2 * s)
                if rng.random() < 0.5:
                    for k in range(3):                                   # des planches clouées
                        yy = wy + 12 * s + k * 22 * s
                        mid.poly([(wx - 4 * s, yy + 6 * s), (wx + 74 * s, yy), (wx + 74 * s, yy + 12 * s), (wx - 4 * s, yy + 18 * s)],
                                 (150, 110, 70, 255), INK, 1.2 * s)
                else:                                                    # la vitre cassée, des éclats aux coins
                    _rect(mid, wx + 4 * s, wy + 4 * s, wx + 66 * s, wy + 70 * s, (30, 30, 44))
                    for cx_, cy_, dx_, dy_ in ((wx + 4 * s, wy + 4 * s, 1, 1), (wx + 66 * s, wy + 70 * s, -1, -1), (wx + 66 * s, wy + 4 * s, -1, 1)):
                        mid.poly([(cx_, cy_), (cx_ + dx_ * 30 * s, cy_), (cx_ + dx_ * 8 * s, cy_ + dy_ * 12 * s), (cx_, cy_ + dy_ * 26 * s)],
                                 (170, 200, 230, 255))
                _rect(mid, wx - 6 * s, wy + 74 * s, wx + 76 * s, wy + 82 * s, mix(wall, (255, 255, 255), 0.3))
        if rng.random() < 0.7:                                           # l'escalier de secours en fer
            ex = x + w * 0.62
            for k in range(3):
                ly = top + 120 * s + k * 70 * s
                if ly > base - 90 * s:
                    break
                mid.line([(ex, ly), (ex + 120 * s, ly)], (40, 36, 40, 255), 5 * s)
                mid.line([(ex + 6 * s, ly), (ex + 110 * s, ly + 60 * s)], (40, 36, 40, 255), 3 * s)
                for r in range(6):
                    mid.line([(ex + r * 22 * s, ly - 24 * s), (ex + r * 22 * s, ly)], (40, 36, 40, 255), 2 * s)
                mid.line([(ex, ly - 24 * s), (ex + 120 * s, ly - 24 * s)], (40, 36, 40, 255), 2 * s)
        for _ in range(rng.randint(1, 3)):                               # affiches collées
            px, py = x + rng.uniform(0.05, 0.85) * w, base - rng.uniform(70, 120) * s
            if abs(px - door) < 110 * s:
                continue
            col = rng.choice(((240, 200, 60), (220, 80, 70), (90, 150, 220), (240, 240, 230)))
            _rect(mid, px, py, px + 40 * s, py + 54 * s, col, INK, 1.2 * s)
            _rect(mid, px + 6 * s, py + 8 * s, px + 34 * s, py + 22 * s, mix(col, (0, 0, 0), 0.4))
        if rng.random() < 0.6:                                           # bidons et poubelles
            bx = x + w * rng.uniform(0.05, 0.3)
            for k in range(rng.randint(1, 2)):
                cx = bx + k * 48 * s
                _rect(mid, cx, base - 64 * s, cx + 40 * s, base, (90, 110, 140), INK, 2 * s)
                for yy in (base - 50 * s, base - 22 * s):
                    mid.line([(cx, yy), (cx + 40 * s, yy)], (60, 76, 100, 255), 2 * s)
        x += w + rng.uniform(0, 30) * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _rect(near, 0, base, tw, H, (176, 178, 186))                         # le trottoir de dalles grises
    for k in range(int(tw / (64 * s)) + 1):
        near.line([(k * 64 * s, base), (k * 64 * s - 80 * s, H)], (140, 142, 152, 255), 2 * s)
    for y in (base + 40 * s, base + 92 * s):
        near.line([(0, y), (tw, y)], (140, 142, 152, 255), 2 * s)
    _rect(near, 0, H - 22 * s, tw, H, (110, 112, 120))                   # la bordure
    for _ in range(int(tw / (90 * s))):
        cx, cy = rng.uniform(0, tw), rng.uniform(base + 10 * s, H - 30 * s)
        near.ellipse(cx - 10 * s, cy - 3 * s, cx + 10 * s, cy + 3 * s, (150, 150, 160, 200))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"window": (255, 230, 170)}}




def _ridge(p, tw, H, s, base, hmin, hmax, col, rng, n=5, rim=None):
    """Hills or mountains that loop over the width of the pattern. / Collines ou montagnes qui bouclent."""
    f = periodic(tw, rng, n, 1.0)
    xs = [k * 8 * s for k in range(int(tw / (8 * s)) + 2)]
    vals = [f(x) for x in xs]
    lo, hi = min(vals), max(vals)
    pts = [(x, base - (hmin + (hmax - hmin) * (v - lo) / max(1e-6, hi - lo)) * s) for x, v in zip(xs, vals)]
    p.poly([(0, H)] + pts + [(xs[-1], H)], _rgba(col))
    if rim is not None:
        p.line(pts, _rgba(rim), 3 * s)
    return pts


def _oak(p, x, base, h, s, rng, bark=(96, 70, 46), tones=((40, 90, 40), (70, 130, 50), (120, 170, 70))):
    """A huge old tree with a twisted trunk and roots. / Un vieil arbre immense au tronc tordu."""
    tw2 = 26 * s
    lean = rng.uniform(-30, 30) * s
    p.poly([(x - tw2 * 1.6, base), (x - tw2 * 0.7, base - h * 0.4), (x - tw2 + lean, base - h * 0.8), (x + tw2 + lean, base - h * 0.8),
            (x + tw2 * 0.8, base - h * 0.4), (x + tw2 * 1.7, base)], _rgba(bark), INK, 2 * s)
    for k in range(3):                                                    # l'écorce
        xx = x - tw2 * 0.5 + k * tw2 * 0.5
        p.line([(xx, base - 10 * s), (xx + lean * 0.5, base - h * 0.7)], _rgba(mix(bark, (0, 0, 0), 0.3)), 2 * s)
    for k in range(3):                                                    # les grosses branches
        a = -math.pi / 2 + rng.uniform(-1.0, 1.0)
        bx, by = x + lean, base - h * 0.75
        p.line([(bx, by), (bx + math.cos(a) * h * 0.35, by + math.sin(a) * h * 0.3)], _rgba(bark), 10 * s)
    for k in range(5):
        cx = x + lean + rng.uniform(-1, 1) * h * 0.4
        cy = base - h * rng.uniform(0.85, 1.15)
        _clump(p, cx, cy, h * rng.uniform(0.22, 0.32), rng, tones, n=8)


def _timber_house(p, x, base, w, h, s, rng, wall=(232, 216, 180), beam=(90, 56, 34), roof=(150, 120, 70)):
    """A half-timbered house with a thatched or tiled roof. / Une maison à colombages, toit de chaume ou de tuiles."""
    top = base - h
    p.poly([(x, top), (x + w, top), (x + w, base), (x, base)], _rgba(wall), INK, 2 * s)
    for k in range(int(w / (46 * s)) + 1):                                # les poutres
        bx = x + k * w / max(1, int(w / (46 * s)))
        p.line([(bx, top), (bx, base)], _rgba(beam), 6 * s)
    p.line([(x, top + h * 0.45), (x + w, top + h * 0.45)], _rgba(beam), 6 * s)
    for k in range(int(w / (92 * s))):
        bx = x + k * 92 * s
        p.line([(bx, top + h * 0.45), (bx + 46 * s, top)], _rgba(beam), 5 * s)
    for k in range(int(w / (110 * s))):                                   # fenêtres à petits carreaux
        wx = x + 30 * s + k * 110 * s
        p.poly([(wx, top + h * 0.55), (wx + 40 * s, top + h * 0.55), (wx + 40 * s, top + h * 0.8), (wx, top + h * 0.8)], (60, 50, 50, 255), INK, 2 * s)
        p.line([(wx + 20 * s, top + h * 0.55), (wx + 20 * s, top + h * 0.8)], _rgba(beam), 3 * s)
    p.poly([(x - 20 * s, top + 4 * s), (x + w / 2, top - h * 0.7), (x + w + 20 * s, top + 4 * s)], _rgba(roof), INK, 2 * s)
    for k in range(6):                                                    # les rangs du toit
        yy = top - h * 0.7 + (k + 1) * h * 0.7 / 7
        half = (yy - (top - h * 0.7)) / (h * 0.7) * (w / 2 + 20 * s)
        p.line([(x + w / 2 - half, yy), (x + w / 2 + half, yy)], _rgba(mix(roof, (0, 0, 0), 0.25)), 2 * s)


def _dirt_ground(p, tw, H, s, base, rng, col, specks, grass=None):
    p.poly([(0, base), (tw, base), (tw, H), (0, H)], _rgba(col))
    if grass is not None:                                                 # l'herbe au bord du chemin
        for k in range(int(tw / (6 * s))):
            x = k * 6 * s + rng.uniform(-2, 2) * s
            p.line([(x, base + 10 * s), (x + rng.uniform(-4, 4) * s, base - rng.uniform(4, 16) * s)], _rgba(rng.choice(grass)), 2 * s)
    for _ in range(int(tw * (H - base) / (260 * s * s))):
        x, y = rng.uniform(0, tw), rng.uniform(base + 6 * s, H)
        p.ellipse(x - 5 * s, y - 2 * s, x + 5 * s, y + 2 * s, _rgba(rng.choice(specks), 200))


def _tiles(p, tw, H, s, base, col, line, size=64):
    p.poly([(0, base), (tw, base), (tw, H), (0, H)], _rgba(col))
    for k in range(int(tw / (size * s)) + 2):
        p.line([(k * size * s, base), (k * size * s - 90 * s, H)], _rgba(line), 2 * s)
    y, step = base, 26 * s
    while y < H:
        p.line([(0, y), (tw, y)], _rgba(line), 2 * s)
        y += step
        step *= 1.25


# ---------------------------------------------------------------------------- Captain Commando
def build_cc_future(W, H, s, seed=1202):
    """Captain Commando: a city of the future by day, as in the game: white and blue towers with rounded tops far off,
    glass fronts with their neon strips, screens of colour, the light marble floor of the hall.
    / Une ville du futur de jour : tours blanches et bleues au loin, façades de verre et néons, sol de marbre clair."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (90, 150, 230)), (0.6, (200, 225, 250)), (1.0, (240, 240, 250))])
    far = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw - 80 * s:
        w = min(rng.uniform(50, 110) * s, tw - x - 2 * s)
        h = rng.uniform(140, 290) * s
        col = rng.choice(((220, 230, 245), (170, 200, 235), (200, 215, 240)))
        far.poly([(x, base - h + w / 2), (x + w, base - h + w / 2), (x + w, base), (x, base)], _rgba(col))
        far.ellipse(x, base - h, x + w, base - h + w, _rgba(col))         # le sommet arrondi
        for wy in range(int(base - h + w * 0.7), int(base - 10 * s), int(16 * s)):
            far.line([(x + 6 * s, wy), (x + w - 6 * s, wy)], _rgba(mix(col, (60, 110, 200), 0.4)), 2 * s)
        x += w + rng.uniform(20, 70) * s
    layers = [{"img": far.done(), "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    x = 0.0
    lights = []
    while x < tw - 200 * s:
        w = min(rng.uniform(320, 480) * s, tw - x)
        top = rng.uniform(0, 50) * s
        _rect(mid, x, top, x + w, base, (236, 232, 222), INK, 2 * s)      # la façade claire
        _rect(mid, x + 20 * s, top + 30 * s, x + w - 20 * s, base - 110 * s, (90, 160, 210), INK, 2 * s)  # la grande vitre
        for k in range(int((w - 40 * s) / (60 * s))):
            gx = x + 20 * s + k * 60 * s
            mid.line([(gx, top + 30 * s), (gx, base - 110 * s)], (220, 235, 245, 255), 3 * s)
            mid.line([(gx + 10 * s, top + 40 * s), (gx + 30 * s, top + 80 * s)], (200, 230, 250, 200), 4 * s)
        neon = rng.choice(((255, 60, 160), (60, 230, 255), (255, 210, 60)))
        _rect(mid, x + 20 * s, base - 104 * s, x + w - 20 * s, base - 96 * s, neon)
        lights.append((x + w / 2, base - 100 * s))
        sx = x + w * rng.uniform(0.15, 0.6)                               # un écran de couleur
        _rect(mid, sx, base - 86 * s, sx + 110 * s, base - 30 * s, (30, 34, 60), INK, 2 * s)
        for k in range(3):
            _rect(mid, sx + 10 * s + k * 34 * s, base - 76 * s, sx + 36 * s + k * 34 * s, base - 40 * s,
                  rng.choice(((255, 90, 90), (90, 220, 140), (90, 140, 255), (250, 220, 80))))
        if rng.random() < 0.7:                                            # bancs rouges
            bx = x + w * 0.75
            for k in range(2):
                cx = bx + k * 40 * s
                mid.ellipse(cx - 16 * s, base - 46 * s, cx + 16 * s, base - 22 * s, (210, 40, 50, 255), INK, 2 * s)
                mid.line([(cx, base - 24 * s), (cx, base)], (60, 60, 70, 255), 4 * s)
        x += w + rng.uniform(0, 20) * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid", "lights": lights})
    near = _Pic(tw, H, 2, tw)
    _tiles(near, tw, H, s, base, (222, 210, 188), (190, 176, 150), 96)
    for _ in range(int(tw / (120 * s))):
        cx, cy = rng.uniform(0, tw), rng.uniform(base + 10 * s, H - 10 * s)
        near.ellipse(cx - 30 * s, cy - 4 * s, cx + 30 * s, cy + 4 * s, (240, 236, 226, 160))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"window": (255, 120, 200)}}


# ---------------------------------------------------------------------------- Cadillacs and Dinosaurs
def build_cd_ruins(W, H, s, seed=1203):
    """Cadillacs and Dinosaurs: a town swallowed by the jungle, as in the game: the hot sky, far volcanoes, the broken
    stone columns of an old hall taken by vines, palms and ferns, a big old car left on the dusty road.
    / Une ville avalée par la jungle : ciel chaud, volcans au loin, colonnes brisées couvertes de lianes, vieille voiture."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (230, 150, 80)), (0.45, (250, 200, 130)), (1.0, (230, 210, 160))])
    far = _Pic(tw, H, 2, tw)
    _ridge(far, tw, H, s, base - 30 * s, 40, 150, (150, 110, 100), rng, 4)
    for k in range(3):                                                    # les volcans fumants
        vx = (k + 0.3) * tw / 3
        far.poly([(vx - 160 * s, base - 30 * s), (vx - 26 * s, base - 230 * s), (vx + 26 * s, base - 230 * s), (vx + 160 * s, base - 30 * s)],
                 (120, 86, 80, 255))
        for j in range(4):
            far.disc(vx + j * 18 * s, base - 250 * s - j * 26 * s, (20 + j * 8) * s, (200, 180, 170, 150))
    layers = [{"img": far.done(), "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw - 160 * s:
        kind = rng.choice(("columns", "columns", "palms", "car"))
        if kind == "columns":                                             # les colonnes de pierre brisées
            w = 360 * s
            _rect(mid, x, base - 40 * s, x + w, base - 20 * s, (150, 130, 110), INK, 2 * s)
            for k in range(3):
                cx = x + 40 * s + k * 130 * s
                h = rng.uniform(150, 280) * s
                _rect(mid, cx, base - h, cx + 50 * s, base - 20 * s, (196, 176, 150), INK, 2 * s)
                for j in range(3):
                    mid.line([(cx + 12 * s + j * 13 * s, base - h + 10 * s), (cx + 12 * s + j * 13 * s, base - 24 * s)], (150, 130, 110, 255), 2 * s)
                mid.poly([(cx - 4 * s, base - h), (cx + 20 * s, base - h - 18 * s), (cx + 40 * s, base - h - 6 * s), (cx + 54 * s, base - h)],
                         (196, 176, 150, 255), INK, 2 * s)                 # la cassure
                for j in range(5):                                        # les lianes
                    vy = base - h + j * h / 5
                    mid.line([(cx - 6 * s, vy), (cx + 25 * s, vy + 26 * s), (cx + 56 * s, vy + 8 * s)], (60, 120, 50, 255), 4 * s)
                _clump(mid, cx + 25 * s, base - h - 10 * s, 34 * s, rng, ((40, 100, 40), (70, 140, 50)), n=5)
        elif kind == "palms":
            w = 260 * s
            for k in range(2):
                px = x + 60 * s + k * 120 * s
                h = rng.uniform(180, 260) * s
                mid.line([(px, base), (px + 20 * s, base - h * 0.5), (px + 10 * s, base - h)], (120, 90, 60, 255), 12 * s)
                for a in range(6):
                    ang = math.radians(-160 + a * 28)
                    mid.line([(px + 10 * s, base - h), (px + 10 * s + math.cos(ang) * 110 * s, base - h + math.sin(ang) * 50 * s + 40 * s)],
                             (50, 130, 60, 255), 9 * s)
            for k in range(4):                                            # les fougères
                fx = x + rng.uniform(0, w)
                for a in range(5):
                    ang = math.radians(-150 + a * 30)
                    mid.line([(fx, base - 4 * s), (fx + math.cos(ang) * 50 * s, base - 4 * s + math.sin(ang) * 40 * s)], (60, 140, 60, 255), 6 * s)
        else:                                                             # une grande vieille voiture abandonnée
            w = 340 * s
            cy = base - 30 * s
            mid.poly([(x + 20 * s, cy), (x + 40 * s, cy - 50 * s), (x + 110 * s, cy - 56 * s), (x + 150 * s, cy - 100 * s), (x + 250 * s, cy - 100 * s),
                      (x + 290 * s, cy - 56 * s), (x + 330 * s, cy - 50 * s), (x + 336 * s, cy)], (200, 60, 50, 255), INK, 3 * s)
            mid.poly([(x + 160 * s, cy - 92 * s), (x + 240 * s, cy - 92 * s), (x + 270 * s, cy - 58 * s), (x + 140 * s, cy - 58 * s)], (150, 200, 220, 255),
                     INK, 2 * s)
            mid.line([(x + 30 * s, cy - 30 * s), (x + 330 * s, cy - 30 * s)], (230, 230, 220, 255), 4 * s)
            for wx in (x + 90 * s, x + 270 * s):
                mid.disc(wx, cy, 30 * s, (30, 30, 34, 255), INK, 2 * s)
                mid.disc(wx, cy, 13 * s, (200, 200, 200, 255))
        x += w + rng.uniform(10, 60) * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _dirt_ground(near, tw, H, s, base, rng, (196, 160, 110), ((170, 130, 90), (220, 190, 140), (150, 120, 80)),
                 grass=((80, 140, 60), (110, 160, 70), (60, 110, 50)))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"dust": (120, 100, 70)}}


# ---------------------------------------------------------------------------- The Punisher
def build_pn_mansion(W, H, s, seed=1204):
    """The Punisher: the hall of a mobster's mansion at night, as in the game: purple walls with gold trims, columns,
    tall windows on the night, chandeliers, a grand staircase, potted plants, the red carpet on the marble.
    / Le hall d'une villa de gangster la nuit : murs violets à moulures d'or, colonnes, lustres, escalier, tapis rouge."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (60, 30, 70)), (1.0, (110, 60, 110))])
    mid = _Pic(tw, H, 2, tw)
    _rect(mid, 0, 0, tw, base, (120, 60, 120))
    lights = []
    x = 0.0
    while x < tw - 100 * s:
        w = min(rng.uniform(300, 420) * s, tw - x)
        kind = rng.choice(("window", "window", "stairs"))
        _rect(mid, x, 30 * s, x + 40 * s, base, (200, 160, 200), INK, 2 * s)            # la colonne
        _rect(mid, x - 8 * s, 30 * s, x + 48 * s, 46 * s, (230, 190, 80), INK, 2 * s)
        _rect(mid, x - 8 * s, base - 16 * s, x + 48 * s, base, (230, 190, 80), INK, 2 * s)
        if kind == "window":                                              # grande fenêtre sur la nuit
            wx = x + w * 0.35
            _rect(mid, wx, 70 * s, wx + 120 * s, base - 40 * s, (20, 24, 60), (230, 190, 80, 255), 4 * s)
            mid.line([(wx + 60 * s, 70 * s), (wx + 60 * s, base - 40 * s)], (230, 190, 80, 255), 3 * s)
            for k in range(6):
                mid.disc(wx + rng.uniform(8, 112) * s, rng.uniform(80, 170) * s, 1.6 * s, (240, 240, 255, 255))
            mid.poly([(wx - 20 * s, 60 * s), (wx + 20 * s, 60 * s), (wx + 10 * s, base - 40 * s), (wx - 26 * s, base - 40 * s)], (170, 30, 60, 255))  # rideaux
            mid.poly([(wx + 100 * s, 60 * s), (wx + 140 * s, 60 * s), (wx + 146 * s, base - 40 * s), (wx + 110 * s, base - 40 * s)], (170, 30, 60, 255))
        else:                                                             # l'escalier d'honneur
            sx = x + w * 0.3
            for k in range(8):
                _rect(mid, sx + k * 26 * s, base - 30 * s - k * 22 * s, sx + 200 * s, base - 8 * s - k * 22 * s, (200, 170, 200), INK, 1.5 * s)
            mid.line([(sx, base - 70 * s), (sx + 200 * s, base - 240 * s)], (230, 190, 80, 255), 5 * s)
        cx = x + w * 0.62                                                 # le lustre
        mid.line([(cx, 0), (cx, 40 * s)], (230, 190, 80, 255), 2 * s)
        mid.poly([(cx - 40 * s, 40 * s), (cx + 40 * s, 40 * s), (cx + 20 * s, 66 * s), (cx - 20 * s, 66 * s)], (240, 210, 120, 255), INK, 2 * s)
        for k in range(5):
            mid.disc(cx - 36 * s + k * 18 * s, 40 * s, 5 * s, (255, 250, 200, 255))
            lights.append((cx - 36 * s + k * 18 * s, 40 * s))
        px = x + w * 0.85                                                 # une plante en pot
        _rect(mid, px, base - 50 * s, px + 36 * s, base, (180, 120, 60), INK, 2 * s)
        _clump(mid, px + 18 * s, base - 80 * s, 40 * s, rng, ((40, 110, 50), (70, 150, 60)), n=6)
        x += w
    _rect(mid, 0, 18 * s, tw, 30 * s, (230, 190, 80))                     # la moulure du haut
    layers = [{"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid", "lights": lights}]
    near = _Pic(tw, H, 2, tw)
    _tiles(near, tw, H, s, base, (200, 190, 200), (160, 150, 170), 120)
    _rect(near, 0, base + 40 * s, tw, base + 110 * s, (170, 30, 50))       # le tapis rouge
    near.line([(0, base + 44 * s), (tw, base + 44 * s)], (230, 190, 80, 255), 3 * s)
    near.line([(0, base + 106 * s), (tw, base + 106 * s)], (230, 190, 80, 255), 3 * s)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"window": (255, 240, 180)}}


# ---------------------------------------------------------------------------- The King of Dragons
def build_kd_forest(W, H, s, seed=1205):
    """The King of Dragons: a forest of huge old trees in the sun, as in the first stage: blue mountains far off, the
    twisted trunks and their thick leaves, the green meadow and its flowers.
    / Une forêt d'arbres immenses au soleil : montagnes bleues au loin, troncs tordus, épais feuillage, prairie fleurie."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (120, 180, 240)), (0.6, (210, 230, 245)), (1.0, (230, 240, 230))])
    far = _Pic(tw, H, 2, tw)
    _ridge(far, tw, H, s, base - 40 * s, 60, 170, (130, 160, 200), rng, 5, rim=(220, 230, 245))
    _ridge(far, tw, H, s, base - 10 * s, 20, 70, (110, 150, 120), rng, 4)
    layers = [{"img": far.done(), "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    x = 60.0 * s
    while x < tw - 150 * s:
        _oak(mid, x, base + 6 * s, rng.uniform(250, 330) * s, s, rng)
        x += rng.uniform(300, 460) * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _dirt_ground(near, tw, H, s, base, rng, (110, 160, 70), ((90, 140, 60), (140, 190, 90), (240, 230, 120), (240, 140, 160)),
                 grass=((70, 130, 50), (100, 160, 60), (60, 110, 40)))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Knights of the Round
def build_kn_village(W, H, s, seed=1206):
    """Knights of the Round: a village of half-timbered houses, as in the first stage: the castle on the hill far off,
    the houses with their beams and their thatched roofs, stone walls, the dirt road edged with grass.
    / Un village de maisons à colombages : le château sur la colline, les toits de chaume, murets de pierre, chemin de terre."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (110, 160, 220)), (0.7, (220, 220, 210)), (1.0, (230, 220, 190))])
    far = _Pic(tw, H, 2, tw)
    pts = _ridge(far, tw, H, s, base - 20 * s, 30, 110, (120, 150, 110), rng, 4)
    for k in range(2):                                                    # le château sur la colline
        cx = (k + 0.4) * tw / 2
        hy = min(y for x, y in pts if abs(x - cx) < 60 * s) if any(abs(x - cx) < 60 * s for x, y in pts) else base - 80 * s
        _rect(far, cx - 70 * s, hy - 70 * s, cx + 70 * s, hy + 10 * s, (170, 170, 180))
        for tx in (cx - 80 * s, cx + 50 * s):
            _rect(far, tx, hy - 110 * s, tx + 30 * s, hy + 10 * s, (160, 160, 172))
            far.poly([(tx - 6 * s, hy - 110 * s), (tx + 15 * s, hy - 150 * s), (tx + 36 * s, hy - 110 * s)], (130, 70, 70, 255))
    layers = [{"img": far.done(), "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw - 200 * s:
        if rng.random() < 0.75:
            w = rng.uniform(230, 320) * s
            _timber_house(mid, x + 20 * s, base - 4 * s, w, rng.uniform(120, 170) * s, s, rng,
                          roof=rng.choice(((150, 120, 70), (170, 140, 80), (140, 80, 60))))
            x += w + 40 * s
        else:                                                             # un muret de pierre et un arbre
            w = 220 * s
            for k in range(int(w / (30 * s))):
                for j in range(2):
                    _rect(mid, x + k * 30 * s + (j % 2) * 15 * s, base - 50 * s + j * 22 * s, x + k * 30 * s + 28 * s + (j % 2) * 15 * s,
                          base - 30 * s + j * 22 * s, rng.choice(((170, 160, 140), (150, 140, 125), (185, 175, 150))), INK, 1.2 * s)
            _oak(mid, x + w * 0.6, base - 40 * s, 200 * s, s, rng)
            x += w + 30 * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _dirt_ground(near, tw, H, s, base, rng, (170, 140, 90), ((150, 120, 80), (200, 170, 120), (130, 110, 70)),
                 grass=((90, 140, 60), (120, 160, 70)))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Warriors of Fate
def build_wf_forest(W, H, s, seed=1207):
    """Warriors of Fate: a forest of ancient China, as in the first stage: misty green mountains with sharp peaks far
    off, tall trees, the wooden palisade of a camp with its banners, barrels, the earth road.
    / Une forêt de la Chine ancienne : montagnes pointues dans la brume, grands arbres, palissade et bannières, tonneaux."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (170, 200, 190)), (0.6, (230, 230, 210)), (1.0, (220, 210, 170))])
    far = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw:                                                         # les pics dans la brume
        w = rng.uniform(80, 160) * s
        h = rng.uniform(120, 240) * s
        far.poly([(x - w * 0.2, base - 20 * s), (x + w * 0.45, base - h), (x + w * 0.55, base - h), (x + w * 1.2, base - 20 * s)],
                 _rgba(rng.choice(((120, 160, 140), (140, 175, 155), (110, 150, 130)))))
        x += w * rng.uniform(0.5, 0.9)
    layers = [{"img": far.done(), "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw - 200 * s:
        if rng.random() < 0.55:                                           # la palissade et ses bannières
            w = rng.uniform(300, 420) * s
            for k in range(int(w / (22 * s))):
                px = x + k * 22 * s
                mid.poly([(px, base - 150 * s), (px + 10 * s, base - 166 * s), (px + 20 * s, base - 150 * s), (px + 20 * s, base), (px, base)],
                         (150, 100, 56, 255), INK, 1.5 * s)
            mid.line([(x, base - 110 * s), (x + w, base - 110 * s)], (100, 66, 36, 255), 6 * s)
            for k in range(2):
                bx = x + w * (0.25 + 0.5 * k)
                mid.line([(bx, base - 260 * s), (bx, base - 150 * s)], (90, 60, 30, 255), 5 * s)
                col = rng.choice(((200, 40, 40), (230, 190, 50), (40, 80, 170)))
                mid.poly([(bx + 2 * s, base - 256 * s), (bx + 60 * s, base - 252 * s), (bx + 54 * s, base - 196 * s), (bx + 2 * s, base - 200 * s)],
                         _rgba(col), INK, 2 * s)
                mid.disc(bx + 30 * s, base - 226 * s, 13 * s, (250, 240, 220, 255))
            for k in range(rng.randint(1, 2)):                            # les tonneaux
                tx = x + w * rng.uniform(0.1, 0.8)
                mid.ellipse(tx, base - 70 * s, tx + 60 * s, base, (170, 120, 60, 255), INK, 2 * s)
                for yy in (base - 54 * s, base - 16 * s):
                    mid.line([(tx + 4 * s, yy), (tx + 56 * s, yy)], (90, 60, 30, 255), 3 * s)
            x += w + 30 * s
        else:
            _oak(mid, x + 100 * s, base, rng.uniform(260, 330) * s, s, rng, bark=(80, 60, 44), tones=((50, 90, 50), (80, 120, 60), (120, 150, 80)))
            x += 260 * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _dirt_ground(near, tw, H, s, base, rng, (176, 150, 96), ((150, 126, 80), (200, 176, 120), (120, 100, 70)),
                 grass=((90, 130, 60), (120, 150, 70)))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Dungeons & Dragons: Shadow over Mystara
def build_ds_canyon(W, H, s, seed=1208):
    """Shadow over Mystara: a canyon of warm sandstone, as in the game: the far cliffs and a dark castle on a peak,
    the layered rock walls, a few dead trees, the stony path.
    / Un canyon de grès chaud : falaises au loin et château sombre sur un pic, parois en strates, arbres morts, sentier."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (110, 150, 210)), (0.6, (230, 210, 180)), (1.0, (240, 200, 150))])
    far = _Pic(tw, H, 2, tw)
    pts = _ridge(far, tw, H, s, base - 60 * s, 50, 140, (190, 140, 110), rng, 5, rim=(230, 190, 150))
    for cx in (tw * 0.3, tw * 0.8):                                       # le château sombre sur un pic
        hy = min(y for x, y in pts if abs(x - cx) < 50 * s) + 10 * s
        _rect(far, cx - 26 * s, hy - 56 * s, cx + 26 * s, hy + 10 * s, (80, 64, 84))
        for tx in (cx - 34 * s, cx + 20 * s):
            _rect(far, tx, hy - 84 * s, tx + 14 * s, hy, (70, 56, 76))
            far.poly([(tx - 4 * s, hy - 84 * s), (tx + 7 * s, hy - 106 * s), (tx + 18 * s, hy - 84 * s)], (70, 56, 76, 255))
    layers = [{"img": far.done(), "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw - 60 * s:                                                # les parois de la falaise, des pitons de grès
        w = min(rng.uniform(110, 220) * s, tw - x)
        h = rng.uniform(110, 230) * s
        col = rng.choice(((200, 140, 90), (186, 128, 84), (214, 156, 104)))
        top = [(x + w * k / 6, base - h * rng.uniform(0.82, 1.0) - (14 * s if k in (2, 3) else 0)) for k in range(7)]
        mid.poly([(x - 10 * s, base)] + top + [(x + w + 10 * s, base)], _rgba(col), (130, 84, 56, 255), 2 * s)
        mid.poly([(x + w * 0.66, top[4][1] + 6 * s), (x + w, top[6][1] + 4 * s), (x + w + 10 * s, base), (x + w * 0.7, base)],
                 _rgba(mix(col, (60, 30, 30), 0.25)))                   # le côté à l'ombre
        for k in range(int(h / (24 * s))):                                # les strates, des traits courts
            yy = base - h + 22 * s + k * 24 * s
            x0 = x + rng.uniform(0.0, 0.4) * w
            mid.line([(x0, yy), (x0 + rng.uniform(0.25, 0.5) * w, yy + rng.uniform(-3, 3) * s)], _rgba(mix(col, (0, 0, 0), 0.2)), 2.5 * s)
        x += w - 20 * s
    for k in range(4):                                                    # arbres morts
        tx = rng.uniform(0, tw)
        mid.line([(tx, base), (tx + 6 * s, base - 120 * s)], (90, 70, 60, 255), 8 * s)
        for j in range(3):
            a = math.radians(-150 + j * 50)
            mid.line([(tx + 4 * s, base - 80 * s - j * 14 * s), (tx + 4 * s + math.cos(a) * 50 * s, base - 80 * s - j * 14 * s + math.sin(a) * 40 * s)],
                     (90, 70, 60, 255), 4 * s)
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _dirt_ground(near, tw, H, s, base, rng, (200, 160, 110), ((170, 130, 90), (220, 186, 140), (140, 110, 80), (120, 100, 90)))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"dust": (130, 100, 70)}}


# ---------------------------------------------------------------------------- Dungeons & Dragons: Tower of Doom
def build_dt_hills(W, H, s, seed=1209):
    """Tower of Doom: green hills in the golden light, as in the first stage: a walled town far off, the rolling hills,
    a wooden signpost, a treasure chest, the grass and the path. / Collines vertes dans la lumière dorée : une ville
    fortifiée au loin, panneau de bois, coffre au trésor, l'herbe et le chemin."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (230, 200, 120)), (0.6, (250, 230, 170)), (1.0, (240, 230, 180))])
    far = _Pic(tw, H, 2, tw)
    pts = _ridge(far, tw, H, s, base - 40 * s, 40, 120, (150, 160, 90), rng, 4)
    for k in range(2):                                                    # la ville fortifiée
        cx = (k + 0.6) * tw / 2
        hy = min(y for x, y in pts if abs(x - cx) < 80 * s)
        _rect(far, cx - 120 * s, hy - 30 * s, cx + 120 * s, hy + 10 * s, (180, 160, 120))
        for j in range(6):
            tx = cx - 110 * s + j * 44 * s
            _rect(far, tx, hy - 60 * s, tx + 16 * s, hy - 30 * s, (180, 160, 120))
            far.poly([(tx - 4 * s, hy - 60 * s), (tx + 8 * s, hy - 80 * s), (tx + 20 * s, hy - 60 * s)], (150, 80, 60, 255))
    layers = [{"img": far.done(), "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    _ridge(mid, tw, H, s, base + 10 * s, 20, 80, (120, 150, 60), rng, 5, rim=(160, 190, 90))
    x = 120.0 * s
    while x < tw - 200 * s:
        kind = rng.choice(("sign", "chest", "tree", "tree"))
        if kind == "sign":
            mid.line([(x, base), (x, base - 110 * s)], (110, 76, 46, 255), 8 * s)
            mid.poly([(x - 50 * s, base - 110 * s), (x + 50 * s, base - 116 * s), (x + 60 * s, base - 96 * s), (x - 46 * s, base - 88 * s)],
                     (160, 110, 64, 255), INK, 2 * s)
        elif kind == "chest":
            _rect(mid, x, base - 40 * s, x + 64 * s, base, (150, 90, 40), INK, 2 * s)
            mid.chord(x, base - 62 * s, x + 64 * s, base - 22 * s, 180, 360, (170, 104, 50, 255))
            _rect(mid, x + 26 * s, base - 46 * s, x + 38 * s, base - 30 * s, (240, 200, 70), INK, 1.5 * s)
        else:
            _oak(mid, x, base, rng.uniform(160, 230) * s, s, rng, tones=((70, 110, 40), (110, 150, 50), (160, 190, 80)))
        x += rng.uniform(260, 420) * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _dirt_ground(near, tw, H, s, base, rng, (150, 170, 80), ((130, 150, 70), (180, 190, 100), (200, 170, 100)),
                 grass=((110, 150, 60), (140, 170, 70)))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Alien vs. Predator
def build_av_ruins(W, H, s, seed=1210):
    """Alien vs. Predator: a ruined industrial city at dusk, as in the game: the broken towers in a green haze, the big
    pipes, the wreck of a hover tank, the steel plates of the street, the smoke.
    / Une ville industrielle en ruine au crépuscule : tours brisées dans une brume verte, gros tuyaux, épave, plaques d'acier."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (40, 60, 60)), (0.6, (110, 130, 110)), (1.0, (150, 150, 120))])
    far = _sky_towers(rng, tw, H, s, (70, 90, 90, 255), (200, 220, 150, 255), base - 30 * s, 120, 260, lit=0.08)
    for _ in range(14):                                                   # les cassures des tours
        x = rng.uniform(0, tw)
        far.poly([(x, base - 300 * s), (x + 40 * s, base - 250 * s), (x + 80 * s, base - 300 * s)], (0, 0, 0, 0))
    layers = [{"img": far.done(), "y": 0, "f": 0.15, "stage": "far"}]
    mid = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw - 200 * s:
        kind = rng.choice(("pipes", "wall", "tank"))
        if kind == "pipes":
            w = 340 * s
            for k in range(3):
                py = base - 60 * s - k * 46 * s
                mid.line([(x, py), (x + w, py)], (60, 80, 76, 255), 26 * s)
                mid.line([(x, py - 8 * s), (x + w, py - 8 * s)], (110, 140, 130, 255), 5 * s)
                for j in range(4):
                    _rect(mid, x + j * w / 4, py - 16 * s, x + j * w / 4 + 14 * s, py + 16 * s, (90, 110, 100), INK, 1.5 * s)
        elif kind == "wall":
            w = 300 * s
            mid.poly([(x, base), (x, base - 200 * s), (x + 60 * s, base - 230 * s), (x + 140 * s, base - 180 * s), (x + 220 * s, base - 240 * s),
                      (x + w, base - 160 * s), (x + w, base)], (100, 110, 100, 255), INK, 2 * s)
            for k in range(4):
                _rect(mid, x + 30 * s + k * 64 * s, base - 140 * s, x + 70 * s + k * 64 * s, base - 90 * s, (30, 40, 40), INK, 1.5 * s)
            mid.line([(x + 40 * s, base - 200 * s), (x + 90 * s, base - 120 * s), (x + 70 * s, base - 40 * s)], (60, 70, 66, 255), 3 * s)
        else:                                                             # l'épave d'un char flottant
            w = 360 * s
            mid.poly([(x + 20 * s, base - 10 * s), (x + 60 * s, base - 90 * s), (x + 300 * s, base - 100 * s), (x + 340 * s, base - 20 * s)],
                     (80, 96, 70, 255), INK, 3 * s)
            mid.poly([(x + 120 * s, base - 96 * s), (x + 150 * s, base - 150 * s), (x + 250 * s, base - 150 * s), (x + 270 * s, base - 98 * s)],
                     (90, 110, 80, 255), INK, 3 * s)
            mid.line([(x + 250 * s, base - 130 * s), (x + 360 * s, base - 170 * s)], (60, 70, 60, 255), 12 * s)
            for k in range(3):
                mid.disc(x + 200 * s + k * 30 * s, base - 190 * s - k * 30 * s, (24 + 10 * k) * s, (90, 96, 90, 120))
        x += w + rng.uniform(20, 70) * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _tiles(near, tw, H, s, base, (110, 120, 112), (80, 90, 84), 110)
    for _ in range(int(tw / (70 * s))):
        cx, cy = rng.uniform(0, tw), rng.uniform(base + 8 * s, H - 8 * s)
        near.disc(cx, cy, 3 * s, (150, 160, 150, 255))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"dust": (80, 100, 80), "window": (200, 255, 160)}}


# ---------------------------------------------------------------------------- Armored Warriors
def build_aw_hangar(W, H, s, seed=1211):
    """Armored Warriors: the hangar of the war machines, as in the game: teal steel walls, shutters, hazard stripes,
    a crane over the bays, the big window on the desert, the plated floor.
    / Le hangar des machines de guerre : parois d'acier bleu-vert, rideaux de fer, bandes de danger, grue, sol en plaques."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (230, 190, 120)), (1.0, (240, 220, 170))])
    mid = _Pic(tw, H, 2, tw)
    _rect(mid, 0, 0, tw, base, (60, 110, 120))
    lights = []
    x = 0.0
    while x < tw - 100 * s:
        w = min(rng.uniform(320, 440) * s, tw - x)
        kind = rng.choice(("shutter", "window", "shutter"))
        if kind == "shutter":                                             # le rideau de fer
            sx = x + w * 0.2
            _rect(mid, sx, 80 * s, sx + w * 0.6, base, (110, 130, 130), INK, 3 * s)
            for k in range(int((base - 80 * s) / (14 * s))):
                mid.line([(sx, 80 * s + k * 14 * s), (sx + w * 0.6, 80 * s + k * 14 * s)], (80, 100, 100, 255), 2 * s)
            for k in range(int(w * 0.6 / (30 * s))):                      # la bande de danger
                bx = sx + k * 30 * s
                mid.poly([(bx, 60 * s), (bx + 15 * s, 60 * s), (bx + 30 * s, 80 * s), (bx + 15 * s, 80 * s)], (250, 200, 40, 255))
        else:                                                             # la grande baie sur le désert
            sx = x + w * 0.15
            _rect(mid, sx, 60 * s, sx + w * 0.7, base - 80 * s, (0, 0, 0, 0), (40, 60, 70, 255), 8 * s)
            for k in range(1, 4):
                mid.line([(sx + k * w * 0.7 / 4, 60 * s), (sx + k * w * 0.7 / 4, base - 80 * s)], (40, 60, 70, 255), 6 * s)
        _rect(mid, x, 0, x + 24 * s, base, (40, 80, 90), INK, 2 * s)      # le pilier
        lights.append((x + 12 * s, 40 * s))
        x += w
    _rect(mid, 0, 20 * s, tw, 36 * s, (40, 70, 80))                      # le rail de la grue
    layers = [{"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid", "lights": lights}]
    near = _Pic(tw, H, 2, tw)
    _tiles(near, tw, H, s, base, (70, 140, 150), (40, 100, 110), 128)
    for k in range(int(tw / (128 * s)) + 1):
        near.disc(k * 128 * s + 8 * s, base + 12 * s, 3 * s, (150, 200, 200, 255))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"window": (255, 200, 120)}}


# ---------------------------------------------------------------------------- Battle Circuit
def build_bc_arena(W, H, s, seed=1212):
    """Battle Circuit: an arena of the future, as in the game: the night sky with neon beams, the stands of strange
    fans behind the railing, the blue tiles of the floor. / Une arène du futur : ciel de nuit et néons, gradins de drôles de
    supporters derrière la rambarde, dalles bleues."""
    rng = random.Random(seed)
    tw = 2 * W
    base = BRAWL_FLOOR * s
    sky = vgrad(W, H, [(0.0, (30, 20, 70)), (0.7, (90, 50, 130)), (1.0, (140, 80, 150))])
    mid = _Pic(tw, H, 2, tw)
    _rect(mid, 0, base - 190 * s, tw, base - 40 * s, (60, 40, 90))       # les gradins
    blinks = []
    for row in range(3):
        y0 = base - 180 * s + row * 46 * s
        x = rng.uniform(0, 30) * s
        while x < tw - 30 * s:
            col = rng.choice(((240, 120, 90), (120, 220, 120), (250, 220, 90), (120, 180, 255), (230, 120, 220), (240, 240, 240)))
            skin = rng.choice(((240, 190, 150), (120, 200, 120), (180, 140, 220), (230, 170, 120)))
            mid.ellipse(x, y0 + 10 * s, x + 30 * s, y0 + 50 * s, _rgba(col))
            mid.disc(x + 15 * s, y0 + 6 * s, 11 * s, _rgba(skin), INK, 1.2 * s)
            if rng.random() < 0.25:                                       # des bras levés
                mid.line([(x + 4 * s, y0 + 18 * s), (x - 6 * s, y0 - 8 * s)], _rgba(skin), 5 * s)
            x += rng.uniform(32, 44) * s
    _rect(mid, 0, base - 46 * s, tw, base, (40, 50, 110))                 # la rambarde
    for k in range(int(tw / (40 * s)) + 1):
        mid.line([(k * 40 * s, base - 46 * s), (k * 40 * s, base)], (200, 210, 240, 255), 4 * s)
    mid.line([(0, base - 46 * s), (tw, base - 46 * s)], (230, 240, 255, 255), 6 * s)
    for k in range(int(tw / (200 * s))):
        blinks.append((k * 200 * s + 100 * s, base - 210 * s))
    layers = [{"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid", "blinks": blinks}]
    near = _Pic(tw, H, 2, tw)
    _tiles(near, tw, H, s, base, (80, 120, 230), (50, 80, 180), 100)
    for k in range(int(tw / (100 * s)) + 1):
        near.line([(k * 100 * s + 10 * s, base + 8 * s), (k * 100 * s + 50 * s, base + 8 * s)], (170, 200, 255, 255), 3 * s)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw,
            "amb": {"searchlights": [(0.22, 1.0), (0.78, 0.8)], "horizon": base - 230 * s, "blink": (255, 80, 220)}}


BACKDROPS = {"ff_slum": build_ff_slum, "cc_future": build_cc_future, "cd_ruins": build_cd_ruins, "pn_mansion": build_pn_mansion,
             "kd_forest": build_kd_forest, "kn_village": build_kn_village, "wf_forest": build_wf_forest, "ds_canyon": build_ds_canyon,
             "dt_hills": build_dt_hills, "av_ruins": build_av_ruins, "aw_hangar": build_aw_hangar, "bc_arena": build_bc_arena}
hd_bg.BUILDERS.update(BACKDROPS)

THEMES = tuple(BACKDROPS)            # names of the backdrops of this batch / noms des décors de ce lot
