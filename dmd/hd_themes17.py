"""Backdrops of the Cave shoot'em ups (1.31), seen from the sky, drawn by the program in the spirit of the games: the
green countryside and its highway, the harbour and its docks, the steel fortress and the honeycomb hive of DoDonPachi
and DonPachi, the feudal village of Guwange, the neon floor of Dangun Feveron. Everything is drawn by the program, no
image comes from a game. The backdrops register in hd_bg.BUILDERS when this module is imported (by hd_cave).

Décors des shoot'em ups Cave (1.31), vus du ciel, dessinés par le programme dans l'esprit des jeux : la campagne verte et
son autoroute, le port et ses quais, la forteresse d'acier et la ruche d'alvéoles de DoDonPachi et DonPachi, le village
féodal de Guwange, la piste au néon de Dangun Feveron. Aucune image ne vient d'un jeu.
"""

import math
import random

from PIL import Image

from . import hd_bg
from .hd_themes3 import _clump, _Pic, _rgba

# where the tanks and the trucks drive, in pixels at s = 1 / où roulent les chars et les camions
DDP_ROAD = (214, 236, 258, 280)
DOCK_ROAD = (300, 330)
HIVE_LANES = (170, 300)
VILLAGE_PATHS = (196, 318)
NEON_LANES = (180, 300)


def _done(p):
    return p.done().convert("RGB")


def _rect(p, x0, y0, x1, y1, fill, outline=None, width=0):
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, outline, width)


# ---------------------------------------------------------------------------- the countryside / la campagne
def build_ddp_country(W, H, s, seed=1701):
    """DoDonPachi's first stage in spirit, seen from the sky: fields of green and wheat with their furrows, hedges
    between them, a wide highway along the screen with its white lanes, side roads, small houses and their gardens,
    clumps of trees, a winding river. / La campagne vue du ciel : les champs et leurs sillons, les haies, une large
    autoroute et ses voies, des routes, des maisons, des bosquets, une rivière."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    _rect(p, 0, 0, tw, H, (70, 118, 56, 255))
    tones = ((86, 136, 62), (104, 150, 70), (150, 156, 80), (176, 164, 92), (72, 124, 58), (120, 142, 66))
    x = 0.0
    while x < tw:                                                   # the fields in strips / les champs en bandes
        w = rng.uniform(150, 300) * s
        y = 0.0
        while y < H:
            h = rng.uniform(90, 170) * s
            col = rng.choice(tones)
            _rect(p, x + 3 * s, y + 3 * s, x + w - 3 * s, y + h - 3 * s, _rgba(col))
            dark = tuple(max(0, c - 16) for c in col) + (255,)
            if rng.random() < 0.6:                                  # the furrows / les sillons
                step = rng.uniform(7, 11) * s
                k = y + 8 * s
                while k < y + h - 8 * s:
                    p.line([(x + 8 * s, k), (x + w - 8 * s, k)], dark, 1.4 * s)
                    k += step
            y += h
        x += w
    for _ in range(int(tw / (110 * s))):                            # hedges and clumps / haies et bosquets
        cx, cy = rng.uniform(0, tw), rng.uniform(0, H)
        _clump(p, cx, cy, rng.uniform(14, 26) * s, rng, ((34, 74, 36), (52, 100, 44), (88, 138, 64)), n=7)
    # the river / la rivière
    pts = []
    for i in range(41):
        xx = i * tw / 40
        pts.append((xx, (70 + 30 * math.sin(i * math.tau / 40 * 2) + 14 * math.sin(i * 0.9)) * s))
    p.line(pts, (40, 70, 52, 255), 40 * s)
    p.line(pts, (64, 116, 150, 255), 30 * s)
    p.line([(xx, yy - 6 * s) for xx, yy in pts], (110, 160, 196, 255), 3 * s)
    # the highway / l'autoroute
    top, bot = DDP_ROAD[0] - 16, DDP_ROAD[-1] + 16
    _rect(p, 0, (top - 8) * s, tw, (bot + 8) * s, (150, 146, 128, 255))
    _rect(p, 0, top * s, tw, bot * s, (70, 72, 78, 255))
    mid = (top + bot) / 2
    _rect(p, 0, (mid - 3) * s, tw, (mid + 3) * s, (120, 124, 112, 255))
    for yy in (DDP_ROAD[0] + 11, DDP_ROAD[2] + 11):                 # dashed lanes / voies en pointillés
        k = 0.0
        while k < tw:
            p.line([(k, yy * s), (k + 30 * s, yy * s)], (230, 230, 220, 255), 2.4 * s)
            k += 64 * s
    for yy in (top + 3, bot - 3):
        p.line([(0, yy * s), (tw, yy * s)], (236, 226, 150, 255), 2 * s)
    # side roads, houses and their gardens / routes, maisons et jardins
    for k in range(int(tw / (560 * s))):
        x = k * 560 * s + rng.uniform(80, 300) * s
        _rect(p, x - 14 * s, 0, x + 14 * s, (top - 8) * s, (120, 116, 100, 255))
        _rect(p, x - 14 * s, (bot + 8) * s, x + 14 * s, H, (120, 116, 100, 255))
        for side in (-1, 1):
            for j in range(3):
                hy = rng.uniform(20, top - 60) * s if j % 2 == 0 else rng.uniform(bot + 30, 440) * s
                hx = x + side * rng.uniform(40, 120) * s
                hw, hh = rng.uniform(26, 44) * s, rng.uniform(22, 34) * s
                _rect(p, hx - hw / 2 - 8 * s, hy - hh / 2 - 8 * s, hx + hw / 2 + 8 * s, hy + hh / 2 + 8 * s, (96, 140, 72, 255))
                roof = rng.choice(((170, 60, 50), (70, 90, 130), (150, 150, 150), (180, 120, 60)))
                _rect(p, hx - hw / 2, hy - hh / 2, hx + hw / 2, hy + hh / 2, _rgba(roof), (40, 34, 30, 255), 1.6 * s)
                p.line([(hx - hw / 2, hy), (hx + hw / 2, hy)], tuple(max(0, c - 40) for c in roof) + (255,), 2 * s)
    return {"sky": Image.new("RGB", (W, H), (70, 118, 56)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}],
            "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- the harbour / le port
def build_ddp_dock(W, H, s, seed=1702):
    """A harbour seen from the sky, in the spirit of the games: the dark sea at the top with its waves, the quays of
    concrete and their bollards, piers, cranes and their long arms, stacks of containers in many colours, warehouses
    with their ridged roofs, the roads of the docks. / Le port vu du ciel : la mer sombre, les quais, les jetées, les
    grues, les conteneurs, les entrepôts et les routes des docks."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    shore = 190 * s
    _rect(p, 0, 0, tw, H, (124, 126, 124, 255))
    _rect(p, 0, 0, tw, shore, (28, 64, 96, 255))
    for _ in range(int(tw * shore / (300 * s * s))):                # waves / vaguelettes
        x, y = rng.uniform(0, tw), rng.uniform(0, shore - 10 * s)
        w = rng.uniform(8, 20) * s
        p.line([(x, y), (x + w * 0.5, y - 2 * s), (x + w, y)], (70, 120, 160, 255) if rng.random() < 0.6 else (20, 46, 72, 255), 1.5 * s)
    p.line([(0, shore), (tw, shore)], (200, 200, 190, 255), 6 * s)
    for k in range(int(tw / (420 * s))):                            # piers and moored ships / jetées et navires à quai
        x = k * 420 * s + rng.uniform(60, 200) * s
        _rect(p, x, 40 * s, x + 46 * s, shore, (150, 150, 146, 255), (60, 60, 60, 255), 2 * s)
        L = rng.uniform(160, 260) * s
        sx, sy = x + 60 * s, rng.uniform(60, 120) * s
        p.poly([(sx, sy), (sx + L * 0.85, sy), (sx + L, sy + 18 * s), (sx + L * 0.85, sy + 36 * s), (sx, sy + 36 * s)],
               rng.choice(((90, 40, 36, 255), (40, 60, 90, 255), (60, 70, 60, 255))), (20, 20, 24, 255), 2 * s)
        for j in range(int(L / (34 * s)) - 1):                      # deck cargo / chargement sur le pont
            _rect(p, sx + 10 * s + j * 30 * s, sy + 8 * s, sx + 34 * s + j * 30 * s, sy + 28 * s,
                  _rgba(rng.choice(((200, 80, 40), (40, 120, 180), (220, 180, 60), (90, 150, 80)))))
    # containers, warehouses, cranes / conteneurs, entrepôts, grues
    for _ in range(int(tw / (90 * s))):
        x = rng.uniform(0, tw)
        y = rng.uniform(shore + 20 * s, H - 30 * s)
        if DOCK_ROAD[0] - 24 < y / s < DOCK_ROAD[1] + 24:
            continue
        col = rng.choice(((196, 70, 46), (46, 110, 170), (220, 176, 56), (70, 140, 80), (150, 60, 120), (220, 220, 220)))
        n = rng.randint(2, 5)
        for j in range(n):
            _rect(p, x, y + j * 13 * s, x + 54 * s, y + j * 13 * s + 11 * s, _rgba(col), (30, 30, 30, 255), 1.2 * s)
    for k in range(int(tw / (700 * s))):
        x = k * 700 * s + rng.uniform(100, 400) * s
        y = rng.choice((222, 380)) * s
        _rect(p, x, y - 30 * s, x + 170 * s, y + 30 * s, (96, 104, 112, 255), (30, 34, 40, 255), 2.5 * s)
        for j in range(7):
            p.line([(x + 6 * s, y - 24 * s + j * 8 * s), (x + 164 * s, y - 24 * s + j * 8 * s)], (126, 134, 140, 255), 2.4 * s)
    for k in range(int(tw / (520 * s))):                            # cranes and their arms over the sea / grues
        x = k * 520 * s + rng.uniform(0, 200) * s
        _rect(p, x - 16 * s, shore + 6 * s, x + 16 * s, shore + 38 * s, (220, 150, 40, 255), (40, 30, 20, 255), 2 * s)
        p.line([(x, shore + 20 * s), (x, shore - 120 * s)], (40, 30, 20, 255), 9 * s)
        p.line([(x, shore + 20 * s), (x, shore - 120 * s)], (236, 168, 50, 255), 6 * s)
    for yy in DOCK_ROAD:                                            # the roads of the docks / les routes des docks
        _rect(p, 0, (yy - 13) * s, tw, (yy + 13) * s, (78, 80, 84, 255))
        k = 0.0
        while k < tw:
            p.line([(k, yy * s), (k + 24 * s, yy * s)], (230, 210, 120, 255), 2 * s)
            k += 56 * s
    return {"sky": Image.new("RGB", (W, H), (124, 126, 124)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}],
            "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- the fortress / la forteresse
def build_ddp_fortress(W, H, s, seed=1703):
    """A fortress of the future seen from the sky, in the spirit of the games: dark steel plates and their seams,
    grilles, round hatches, the bases of the big guns, trenches with hazard stripes, orange lamps in the slits.
    / Une forteresse du futur vue du ciel : plaques d'acier sombres, grilles, trappes rondes, socles des gros canons,
    tranchées rayées de danger, lampes orange dans les fentes."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    _rect(p, 0, 0, tw, H, (46, 54, 66, 255))
    step = 96 * s
    for i in range(int(tw / step) + 1):                             # the plates / les plaques
        for j in range(int(H / step) + 1):
            x, y = i * step, j * step
            tone = rng.choice(((54, 62, 76), (48, 56, 70), (60, 70, 84), (44, 50, 62)))
            _rect(p, x + 2 * s, y + 2 * s, x + step - 2 * s, y + step - 2 * s, _rgba(tone), (24, 28, 36, 255), 2 * s)
            p.line([(x + 4 * s, y + 4 * s), (x + step - 4 * s, y + 4 * s)], (84, 94, 110, 255), 1.4 * s)
            if rng.random() < 0.18:                                 # a grille / une grille
                for k in range(6):
                    p.line([(x + 16 * s, y + 18 * s + k * 10 * s), (x + step - 16 * s, y + 18 * s + k * 10 * s)], (30, 34, 44, 255), 3 * s)
    lights = []
    for k in range(int(tw / (380 * s))):                            # gun bases and hatches / socles de canons et trappes
        x = k * 380 * s + rng.uniform(40, 200) * s
        y = rng.choice((96, 380)) * s
        p.disc(x, y, 50 * s, (70, 80, 96, 255), (20, 24, 30, 255), 3 * s)
        p.disc(x, y, 36 * s, (40, 46, 58, 255), (90, 100, 116, 255), 2 * s)
        p.disc(x, y, 14 * s, (24, 26, 32, 255))
        for a in range(8):
            ang = a * math.tau / 8
            p.disc(x + math.cos(ang) * 43 * s, y + math.sin(ang) * 43 * s, 3 * s, (120, 130, 146, 255))
    for yy in (150, 316):                                           # trenches with hazard stripes / tranchées rayées
        y0, y1 = (yy - 12) * s, (yy + 12) * s
        _rect(p, 0, y0, tw, y1, (26, 28, 34, 255))
        k = 0.0
        while k < tw:
            p.poly([(k, y0), (k + 12 * s, y0), (k + 24 * s, y0 + 6 * s), (k + 12 * s, y0 + 6 * s)], (230, 170, 40, 255))
            p.poly([(k, y1 - 6 * s), (k + 12 * s, y1 - 6 * s), (k + 24 * s, y1), (k + 12 * s, y1)], (230, 170, 40, 255))
            k += 24 * s
        for k in range(int(tw / (240 * s))):                        # lamps in the slits / lampes dans les fentes
            lx = k * 240 * s + 60 * s
            _rect(p, lx - 10 * s, yy * s - 3 * s, lx + 10 * s, yy * s + 3 * s, (255, 150, 60, 255))
            lights.append((lx, yy * s))
    return {"sky": Image.new("RGB", (W, H), (46, 54, 66)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far", "lights": lights}],
            "tw": tw, "amb": {"window": (255, 140, 50)}}


# ---------------------------------------------------------------------------- the hive / la ruche
def build_ddp_hive(W, H, s, seed=1704):
    """The honeycomb fortress, in the spirit of DoDonPachi's last stages: a floor of hexagonal plates of amber metal,
    raised rims, cells that glow like honey, thick pipes between them, the great hexagonal hatches.
    / La forteresse en alvéoles : un sol de plaques hexagonales de métal ambré, des alvéoles qui luisent comme du miel,
    de gros tuyaux, les grandes trappes hexagonales."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    _rect(p, 0, 0, tw, H, (60, 40, 22, 255))
    r = 34 * s
    dx, dy = r * 1.5, r * math.sqrt(3)
    lights = []
    cols = int(tw / dx) + 2
    if cols % 2:
        cols += 1                                                   # the tile repeats without a seam / sans couture
    dx = tw / cols
    for i in range(cols):
        for j in range(int(H / dy) + 2):
            cx = i * dx
            cy = j * dy + (dy / 2 if i % 2 else 0)
            hexa = [(cx + r * math.cos(a * math.pi / 3), cy + r * math.sin(a * math.pi / 3)) for a in range(6)]
            tone = rng.choice(((150, 100, 40), (136, 90, 36), (164, 112, 48), (120, 80, 32)))
            p.poly(hexa, _rgba(tone), (54, 34, 16, 255), 3 * s)
            inner = [(cx + r * 0.7 * math.cos(a * math.pi / 3), cy + r * 0.7 * math.sin(a * math.pi / 3)) for a in range(6)]
            k = rng.random()
            if k < 0.12:                                            # a glowing cell / une alvéole qui luit
                p.poly(inner, (255, 196, 70, 255), (120, 70, 20, 255), 2 * s)
                p.poly([(cx + r * 0.36 * math.cos(a * math.pi / 3), cy + r * 0.36 * math.sin(a * math.pi / 3)) for a in range(6)],
                       (255, 236, 160, 255))
                lights.append((cx % tw, cy))
            elif k < 0.5:
                p.poly(inner, tuple(max(0, c - 30) for c in tone) + (255,))
            p.line([(cx - r * 0.5, cy - dy / 2 + 3 * s), (cx + r * 0.5, cy - dy / 2 + 3 * s)], (196, 146, 70, 255), 1.6 * s)
    for yy in HIVE_LANES:                                           # thick pipes / gros tuyaux
        p.line([(0, yy * s), (tw, yy * s)], (40, 26, 14, 255), 22 * s)
        p.line([(0, yy * s), (tw, yy * s)], (110, 90, 70, 255), 16 * s)
        p.line([(0, (yy - 4) * s), (tw, (yy - 4) * s)], (170, 150, 120, 255), 3 * s)
        for k in range(int(tw / (160 * s))):
            x = k * 160 * s
            _rect(p, x - 5 * s, (yy - 11) * s, x + 5 * s, (yy + 11) * s, (70, 56, 40, 255), (30, 20, 10, 255), 1.4 * s)
    for k in range(int(tw / (900 * s))):                            # the great hatches / les grandes trappes
        x, y = k * 900 * s + rng.uniform(150, 500) * s, rng.choice((96, 388)) * s
        R = 70 * s
        p.poly([(x + R * math.cos(a * math.pi / 3), y + R * math.sin(a * math.pi / 3)) for a in range(6)], (70, 50, 30, 255),
               (30, 18, 8, 255), 4 * s)
        for a in range(3):
            ang = a * math.pi / 3
            p.line([(x - math.cos(ang) * R * 0.86, y - math.sin(ang) * R * 0.86), (x + math.cos(ang) * R * 0.86, y + math.sin(ang) * R * 0.86)],
                   (40, 28, 16, 255), 4 * s)
        p.disc(x, y, 16 * s, (255, 180, 60, 255), (90, 50, 10, 255), 3 * s)
        lights.append((x, y))
    return {"sky": Image.new("RGB", (W, H), (60, 40, 22)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far", "lights": lights}],
            "tw": tw, "amb": {"window": (255, 190, 80)}}


# ---------------------------------------------------------------------------- Guwange
def build_gu_village(W, H, s, seed=1705):
    """Guwange's Japan of old, in the spirit of the game, seen from the sky at dusk: dark tiled roofs and their ridges,
    the dirt paths between the houses, rice fields full of water, pines, stone lanterns, a river and its wooden bridge.
    / Le Japon d'autrefois au crépuscule vu du ciel : toits de tuiles sombres, chemins de terre, rizières, pins,
    lanternes de pierre, une rivière et son pont de bois."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    _rect(p, 0, 0, tw, H, (78, 82, 56, 255))
    for _ in range(int(tw / (160 * s))):                            # rice fields / rizières
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        w, h = rng.uniform(80, 160) * s, rng.uniform(50, 90) * s
        _rect(p, x, y, x + w, y + h, (82, 110, 100, 255), (60, 54, 36, 255), 3 * s)
        for k in range(int(w / (14 * s))):
            p.line([(x + 6 * s + k * 14 * s, y + 6 * s), (x + 6 * s + k * 14 * s, y + h - 6 * s)], (96, 132, 92, 255), 1.4 * s)
    for yy in VILLAGE_PATHS:                                        # the paths / les chemins
        pts = [(i * tw / 30, (yy + 10 * math.sin(i * 0.8)) * s) for i in range(31)]
        p.line(pts, (150, 126, 88, 255), 34 * s)
        p.line(pts, (176, 152, 110, 255), 26 * s)
    pts = [(i * tw / 30, (40 + 18 * math.sin(i * math.tau / 30 * 3)) * s) for i in range(31)]
    p.line(pts, (40, 54, 60, 255), 46 * s)                         # the river / la rivière
    p.line(pts, (60, 86, 104, 255), 36 * s)
    for k in range(int(tw / (900 * s))):                            # wooden bridges / ponts de bois
        x = k * 900 * s + 300 * s
        _rect(p, x - 18 * s, 0, x + 18 * s, 90 * s, (126, 70, 40, 255), (50, 26, 14, 255), 2 * s)
        for j in range(8):
            p.line([(x - 16 * s, 6 * s + j * 11 * s), (x + 16 * s, 6 * s + j * 11 * s)], (90, 48, 26, 255), 1.6 * s)
    for _ in range(int(tw / (46 * s))):                             # houses and their roofs / maisons et leurs toits
        x, y = rng.uniform(0, tw), rng.uniform(84, 450) * s
        if any(abs(y / s - yy) < 40 for yy in VILLAGE_PATHS):
            continue
        w, h = rng.uniform(70, 130) * s, rng.uniform(44, 70) * s
        roof = rng.choice(((60, 66, 80), (70, 70, 74), (88, 70, 60), (54, 60, 70)))
        _rect(p, x - w / 2 - 4 * s, y - h / 2 - 4 * s, x + w / 2 + 4 * s, y + h / 2 + 4 * s, (40, 32, 26, 255))
        p.poly([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2 - 10 * s, y), (x - w / 2 + 10 * s, y)],
               tuple(min(255, c + 16) for c in roof) + (255,))
        p.poly([(x - w / 2 + 10 * s, y), (x + w / 2 - 10 * s, y), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)], _rgba(roof))
        for k in range(int(w / (8 * s))):                           # the rows of tiles / les rangs de tuiles
            xx = x - w / 2 + 4 * s + k * 8 * s
            p.line([(xx, y - h / 2 + 2 * s), (xx, y + h / 2 - 2 * s)], tuple(max(0, c - 18) for c in roof) + (255,), 1.2 * s)
        p.line([(x - w / 2 + 10 * s, y), (x + w / 2 - 10 * s, y)], (30, 30, 34, 255), 4 * s)
    lights = []
    for _ in range(int(tw / (150 * s))):                            # pines and stone lanterns / pins et lanternes
        x, y = rng.uniform(0, tw), rng.uniform(60, 450) * s
        _clump(p, x, y, rng.uniform(16, 26) * s, rng, ((28, 52, 36), (42, 72, 46), (70, 100, 60)), n=8)
        lx, ly = x + rng.uniform(30, 60) * s, y + rng.uniform(-20, 20) * s
        p.disc(lx, ly, 6 * s, (150, 146, 136, 255), (60, 56, 50, 255), 1.6 * s)
        p.disc(lx, ly, 2.6 * s, (255, 200, 110, 255))
        lights.append((lx, ly))
    return {"sky": Image.new("RGB", (W, H), (78, 82, 56)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far", "lights": lights}],
            "tw": tw, "amb": {"window": (255, 170, 80)}}


# ---------------------------------------------------------------------------- Dangun Feveron
def build_fv_neon(W, H, s, seed=1706):
    """Dangun Feveron's night of fever, in the spirit of the game: a deep blue floor of tiles seen from above, lines of
    neon in pink and cyan, round dance floors, lights that wink, stars of glitter. / Une piste de nuit vue du dessus :
    carreaux bleu nuit, néons roses et cyan, pistes de danse rondes, lumières qui clignotent."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    _rect(p, 0, 0, tw, H, (16, 14, 40, 255))
    step = 64 * s
    for i in range(int(tw / step) + 1):                             # the tiles / les carreaux
        for j in range(int(H / step) + 1):
            x, y = i * step, j * step
            tone = (24, 20, 58) if (i + j) % 2 else (30, 24, 70)
            _rect(p, x + 2 * s, y + 2 * s, x + step - 2 * s, y + step - 2 * s, _rgba(tone))
    blinks = []
    for yy in NEON_LANES:                                           # neon lines / lignes de néon
        for col, off in (((255, 60, 180), -14), ((60, 230, 255), 14)):
            p.line([(0, (yy + off) * s), (tw, (yy + off) * s)], _rgba(col, 90), 10 * s)
            p.line([(0, (yy + off) * s), (tw, (yy + off) * s)], _rgba(col), 3 * s)
    for k in range(int(tw / (480 * s))):                            # dance floors / pistes de danse
        x, y = k * 480 * s + rng.uniform(80, 300) * s, rng.choice((90, 380)) * s
        for ring, col in ((70, (255, 60, 180)), (54, (255, 220, 80)), (38, (60, 230, 255))):
            p.disc(x, y, ring * s, _rgba(col, 80), _rgba(col), 3 * s)
        for a in range(10):
            ang = a * math.tau / 10
            blinks.append((x + math.cos(ang) * 62 * s, y + math.sin(ang) * 62 * s))
    for _ in range(int(tw / (30 * s))):                             # glitter / paillettes
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        p.disc(x, y, rng.uniform(0.8, 2) * s, (255, 255, 255, rng.randint(80, 200)))
    return {"sky": Image.new("RGB", (W, H), (16, 14, 40)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far", "blinks": blinks}],
            "tw": tw, "amb": {"blink": (255, 80, 200)}}


THEMES = ("ddp_country", "ddp_dock", "ddp_fortress", "ddp_hive", "gu_village", "fv_neon")
hd_bg.BUILDERS.update({"ddp_country": build_ddp_country, "ddp_dock": build_ddp_dock, "ddp_fortress": build_ddp_fortress,
                       "ddp_hive": build_ddp_hive, "gu_village": build_gu_village, "fv_neon": build_fv_neon})
