"""Backdrops of DoDonPachi's six stages (1.31), seen from the sky, after the maps of the stages Seb sent and numbered: the dark
forest crossed by giant branches, the base on the red cratered ground, the blue peaks under the clouds, the base then the ruined city,
the great grey machine and its green channels, the orange and purple hive and its honeycomb grates. The game scrolls up,
the marquee to the right: what lies along a stage lies along the screen. The same places, colours and mood, drawn by the
program: no image comes from the game. The backdrops register in hd_bg.BUILDERS when this module is imported (by hd_cave).

Décors des six niveaux de DoDonPachi (1.31), vus du ciel, d'après les cartes des niveaux envoyées et numérotées par Seb : la
forêt sombre traversée de branches géantes, la base sur le sol rouge et ses cratères, les pics bleus sous les nuages, la base puis la
ville en ruines, la grande machine grise et ses canaux verts, la ruche orange et violette et ses grilles en alvéoles. Les
mêmes lieux, couleurs et ambiance, dessinés par le programme : aucune image ne vient du jeu.
"""

import math
import random

from PIL import Image

from . import hd_bg
from .hd_themes3 import _clump, _Pic, _rgba

# where the tanks drive in each stage, in pixels at s = 1 / où roulent les chars dans chaque niveau
BASE_ROAD = (214, 236, 258, 280)
FOREST_BRANCH = (238, 262)
PEAK_VALLEY = (236, 266)
RUIN_ROAD = (226, 262)
STATION_CHANNELS = (206, 266)
NEST_LANES = (204, 268)


def _done(p):
    return p.done().convert("RGB")


def _rect(p, x0, y0, x1, y1, fill, outline=None, width=0):
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, outline, width)


def _dark(c, k=0.3):
    return tuple(int(v * (1 - k)) for v in c[:3])


def _light(c, k=0.3):
    return tuple(int(v + (255 - v) * k) for v in c[:3])


def _result(p, sky, lights=None, amb=None, tw=None):
    layer = {"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}
    if lights:
        layer["lights"] = lights
    return {"sky": Image.new("RGB", (p.W // 2 if tw is None else p.W // 2, p.h), sky), "layers": [layer], "tw": p.W, "amb": amb or {}}


# ---------------------------------------------------------------------------- 2 the base / la base
def build_ddp_base(W, H, s, seed=3101):
    """Stage 2: a military base on a red planet. Concrete pads and hangars with red, yellow and lilac roofs, a wide
    runway along the screen with its cyan guide line and arrows, a great gate; then the rust-red ground and its craters,
    landing pads with teal rims, a sunken blue dock. / Niveau 2 : une base militaire sur une planète rouge, hangars, piste
    et sa ligne cyan, un grand portail, puis le sol rouille et ses cratères, des pistes rondes et un bassin bleu."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    red = (172, 80, 52)
    _rect(p, 0, 0, tw, H, _rgba(red))
    for _ in range(int(tw * H / (900 * s * s))):                      # grain of the ground / grain du sol
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        p.disc(x, y, rng.uniform(1, 3) * s, _rgba(rng.choice(((186, 92, 60), (156, 70, 46), (194, 106, 70)))))
    base = 0.46 * tw                                                  # the base, then the craters / la base, puis les cratères
    for _ in range(int((tw - base) / (70 * s))):                      # craters / cratères
        x, y, r = rng.uniform(base + 40 * s, tw - 20 * s), rng.uniform(10, H / s - 10) * s, rng.uniform(10, 46) * s
        p.disc(x, y, r * 1.16, _rgba(_light(red, 0.16)))                # the raised rim / le rebord
        p.disc(x, y, r, _rgba(_light(red, 0.26)), _rgba(_dark(red, 0.3)), 1.4 * s)   # the lit far wall / la paroi éclairée
        p.disc(x - r * 0.12, y - r * 0.12, r * 0.9, _rgba(_dark(red, 0.42)))  # the shadowed near wall / la paroi à l'ombre
        p.disc(x + r * 0.05, y + r * 0.05, r * 0.72, _rgba(_dark(red, 0.2)))  # the floor / le fond
    for k in range(int((tw - base) / (520 * s))):                     # landing pads / pistes rondes
        x = base + 260 * s + k * 520 * s + rng.uniform(-60, 60) * s
        y = rng.choice((110, 360)) * s
        p.disc(x, y, 62 * s, (40, 120, 116, 255), (20, 40, 40, 255), 3 * s)
        p.disc(x, y, 50 * s, (70, 160, 150, 255))
        p.disc(x, y, 34 * s, (60, 70, 76, 255), (200, 220, 210, 255), 2 * s)
        p.line([(x - 22 * s, y), (x + 22 * s, y)], (220, 230, 220, 255), 3 * s)
    dx = base + rng.uniform(300, 600) * s                               # the sunken dock / le bassin bleu
    _rect(p, dx, 140 * s, dx + 300 * s, 330 * s, (40, 70, 170, 255), (24, 30, 60, 255), 4 * s)
    for i in range(1, 6):
        p.line([(dx + i * 50 * s, 146 * s), (dx + i * 50 * s, 324 * s)], (70, 110, 210, 255), 1.6 * s)
    for i in range(1, 4):
        p.line([(dx + 6 * s, (140 + i * 48) * s), (dx + 294 * s, (140 + i * 48) * s)], (70, 110, 210, 255), 1.6 * s)
    _rect(p, dx + 110 * s, 200 * s, dx + 190 * s, 270 * s, (200, 204, 210, 255), (40, 44, 50, 255), 2.5 * s)
    # the base: concrete, hangars, the runway / la base : béton, hangars, la piste
    edge = [(base, 0)] + [(base + rng.uniform(-30, 30) * s, y * s) for y in range(40, int(H / s), 60)] + [(base, H)]
    p.poly([(0, 0)] + edge + [(0, H)], (138, 146, 140, 255))
    p.line(edge, (90, 96, 92, 255), 5 * s)
    for i in range(int(base / (160 * s))):                             # concrete slabs / dalles
        p.line([(i * 160 * s, 0), (i * 160 * s, H)], (122, 130, 124, 255), 1.6 * s)
    roofs = ((196, 64, 60), (206, 190, 96), (156, 150, 204), (82, 164, 172), (170, 172, 176))
    x = 40 * s
    while x < base - 200 * s:                                          # hangars above and below the runway / hangars
        for y0, y1 in ((24, 180), (318, 444)):
            w = rng.uniform(90, 150) * s
            roof = rng.choice(roofs)
            _rect(p, x, y0 * s, x + w, y1 * s, _rgba(roof), (36, 38, 40, 255), 3 * s)
            for j in range(int((y1 - y0) / 14)):
                p.line([(x + 6 * s, (y0 + 8 + j * 14) * s), (x + w - 6 * s, (y0 + 8 + j * 14) * s)], _rgba(_dark(roof, 0.2)), 2 * s)
            p.line([(x + 4 * s, y0 * s + 4 * s), (x + w - 4 * s, y0 * s + 4 * s)], _rgba(_light(roof, 0.4)), 2 * s)
        x += rng.uniform(160, 230) * s
    top, bot = BASE_ROAD[0] - 18, BASE_ROAD[-1] + 18
    _rect(p, 0, (top - 6) * s, base, (bot + 6) * s, (106, 112, 108, 255))
    _rect(p, 0, top * s, base, bot * s, (74, 78, 78, 255))
    mid = (top + bot) / 2 * s
    p.line([(0, mid), (base, mid)], (40, 200, 220, 255), 6 * s)
    for k in range(int(base / (360 * s))):                             # arrows of the guide line / flèches de la ligne
        ax = k * 360 * s + 180 * s
        p.poly([(ax, mid - 18 * s), (ax + 40 * s, mid), (ax, mid + 18 * s), (ax + 10 * s, mid)], (60, 230, 240, 255), (20, 60, 70, 255), 1.6 * s)
    for yy in (top + 4, bot - 4):
        p.line([(0, yy * s), (base, yy * s)], (230, 232, 226, 255), 2.4 * s)
    gx = base - 170 * s                                                # the great gate / le grand portail
    _rect(p, gx, 0, gx + 120 * s, H, (60, 120, 116, 255), (24, 40, 40, 255), 4 * s)
    for j in range(int(H / (10 * s))):
        p.line([(gx + 8 * s, j * 10 * s), (gx + 112 * s, j * 10 * s)], (44, 96, 94, 255), 2 * s)
    p.poly([(gx + 20 * s, 150 * s), (gx + 60 * s, 90 * s), (gx + 100 * s, 150 * s), (gx + 76 * s, 150 * s), (gx + 76 * s, 330 * s),
            (gx + 44 * s, 330 * s), (gx + 44 * s, 150 * s)], (200, 50, 46, 255), (60, 20, 20, 255), 2 * s)
    _rect(p, gx - 14 * s, (top - 10) * s, gx + 134 * s, (top - 2) * s, (230, 170, 40, 255))
    _rect(p, gx - 14 * s, (bot + 2) * s, gx + 134 * s, (bot + 10) * s, (230, 170, 40, 255))
    return {"sky": Image.new("RGB", (W, H), red), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- 1 the forest / la forêt
def _branch(p, pts, width, s, rng):
    """A giant branch: its shadow on the trees, the pale wood, a lighter ridge, streaks of bark. / Une branche géante."""
    shadow = [(x + 16 * s, y + 18 * s) for x, y in pts]
    p.line(shadow, (14, 22, 28, 255), width * 1.05)
    p.line(pts, (60, 66, 48, 255), width + 6 * s)
    p.line(pts, (146, 154, 112, 255), width)
    p.line([(x, y - width * 0.18) for x, y in pts], (176, 182, 136, 255), width * 0.32)
    for k in (-0.3, 0.06, 0.32):
        p.line([(x, y + width * k) for x, y in pts], (120, 128, 92, 255), 1.6 * s)


def build_ddp_forest(W, H, s, seed=3102):
    """Stage 1: a dark forest seen from the sky, a deep canopy of blue-green trees, giant pale branches crossing it, the
    long one along the screen where the tanks go, the shadows they cast, wrecks lost under the leaves. / Niveau 1 : une
    forêt sombre vue du ciel, des branches géantes qui la traversent, leurs ombres, des épaves sous les feuilles."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    _rect(p, 0, 0, tw, H, (22, 36, 46, 255))
    tones = ((26, 44, 54), (40, 64, 72), (60, 88, 90))
    for _ in range(int(tw * H / (2600 * s * s))):                      # the canopy / la canopée
        _clump(p, rng.uniform(0, tw), rng.uniform(0, H), rng.uniform(22, 44) * s, rng, tones, n=7, spread=(1.0, 1.3))
    for _ in range(int(tw / (900 * s))):                               # wrecks under the leaves / épaves
        x, y = rng.uniform(0, tw), rng.choice((80, 380)) * s
        p.poly([(x, y), (x + 60 * s, y - 26 * s), (x + 150 * s, y - 20 * s), (x + 120 * s, y + 24 * s), (x + 30 * s, y + 30 * s)],
               (52, 56, 60, 200), (30, 32, 36, 220), 2 * s)
        p.line([(x + 40 * s, y - 4 * s), (x + 110 * s, y + 2 * s)], (70, 74, 78, 200), 4 * s)
    for k in range(int(tw / (640 * s))):                               # branches across / branches en travers
        x = k * 640 * s + rng.uniform(0, 260) * s
        lean = rng.uniform(140, 300) * s * rng.choice((-1, 1))
        pts = [(x + lean * (i / 6) + rng.uniform(-14, 14) * s, -40 * s + i * (H + 80 * s) / 6) for i in range(7)]
        _branch(p, pts, rng.uniform(46, 70) * s, s, rng)
    mid = sum(FOREST_BRANCH) / 2                                       # the long branch / la longue branche
    pts = [(i * tw / 24, (mid + 14 * math.sin(i * math.tau / 24 * 3) + 6 * math.sin(i * 1.7)) * s) for i in range(25)]
    _branch(p, pts, 70 * s, s, rng)
    for k in range(int(tw / (260 * s))):                                # knots on it / des nœuds
        x = k * 260 * s + rng.uniform(0, 120) * s
        y = (mid + 14 * math.sin(x / tw * math.tau * 3)) * s
        p.disc(x, y + rng.uniform(-14, 14) * s, rng.uniform(5, 9) * s, (110, 116, 84, 255), (70, 74, 54, 255), 1.4 * s)
    return {"sky": Image.new("RGB", (W, H), (22, 36, 46)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}],
            "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- 3 the peaks / les pics
def _crag(p, x, y, r, rng, tones, s):
    """A rocky peak seen from above: a jagged dark base, a lit facet toward the top left, a bright ridge.
    / Un pic rocheux vu du dessus : une base dentelée sombre, une face éclairée vers le haut à gauche, une arête claire."""
    n = rng.randint(7, 10)
    pts = []
    for i in range(n):
        a = i / n * math.tau + rng.uniform(-0.25, 0.25)
        k = rng.uniform(0.62, 1.0)
        pts.append((math.cos(a) * r * k * 1.35, math.sin(a) * r * k * 0.95))
    p.poly([(x + a + 8 * s, y + b + 10 * s) for a, b in pts], (36, 40, 74, 150))
    p.poly([(x + a, y + b) for a, b in pts], _rgba(tones[0]), (30, 32, 60, 255), 1.6 * s)
    p.poly([(x + a * 0.72 - r * 0.16, y + b * 0.72 - r * 0.14) for a, b in pts], _rgba(tones[1]))
    p.poly([(x + a * 0.36 - r * 0.3, y + b * 0.36 - r * 0.26) for a, b in pts], _rgba(tones[2]))
    p.line([(x - r * 0.9, y + r * 0.1), (x - r * 0.3, y - r * 0.26), (x + r * 0.5, y - r * 0.05)], _rgba(tones[2]), 2 * s)


def build_ddp_peaks(W, H, s, seed=3103):
    """Stage 3: high above rocky peaks of blue and lilac, tan clouds and sand between them, a long valley along the
    screen, round ruined towers here and there. / Niveau 3 : très haut au-dessus de pics rocheux bleus et lilas, des
    nuages fauves et du sable entre eux, une longue vallée, des tours rondes en ruine."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    sand = (176, 138, 104)
    _rect(p, 0, 0, tw, H, _rgba(sand))
    for _ in range(int(tw * H / (1800 * s * s))):                      # the sand and its ripples / le sable
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        p.line([(x, y), (x + rng.uniform(10, 26) * s, y + rng.uniform(-3, 3) * s)], _rgba(rng.choice(((190, 152, 116), (160, 122, 92)))), 2 * s)
    rocks = ((52, 58, 112), (80, 86, 146), (116, 112, 174))
    v0, v1 = (PEAK_VALLEY[0] - 30) * s, (PEAK_VALLEY[1] + 30) * s
    for _ in range(int(tw * H / (1500 * s * s))):                      # the rocks, thin in the valley / les rochers
        x, y = rng.uniform(0, tw), rng.uniform(-20, H / s + 20) * s
        if v0 < y < v1 and rng.random() < 0.85:
            continue
        _crag(p, x, y, rng.uniform(22, 50) * s, rng, rocks, s)
    for k in range(int(tw / (1100 * s))):                              # ruined towers / tours en ruine
        x, y = k * 1100 * s + rng.uniform(200, 700) * s, rng.choice((96, 384)) * s
        p.disc(x + 10 * s, y + 12 * s, 54 * s, (40, 44, 80, 160))
        p.disc(x, y, 52 * s, (150, 140, 150, 255), (60, 56, 70, 255), 3 * s)
        p.disc(x, y, 36 * s, (96, 90, 110, 255), (60, 56, 70, 255), 2 * s)
        for a in range(10):
            ang = a * math.tau / 10
            p.disc(x + math.cos(ang) * 44 * s, y + math.sin(ang) * 44 * s, 4 * s, (176, 168, 176, 255))
    for _ in range(int(tw / (60 * s))):                                # light streaks of sand in the valleys / traînées de sable
        x, y = rng.uniform(0, tw), rng.uniform(v0 / s - 20, v1 / s + 20) * s
        p.line([(x, y), (x + rng.uniform(40, 90) * s, y + rng.uniform(-4, 4) * s)], (200, 166, 128, 255), rng.uniform(2, 4) * s)
    return {"sky": Image.new("RGB", (W, H), sand), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- 4 the ruins / les ruines
def build_ddp_ruins(W, H, s, seed=3104):
    """Stage 4: a base on teal ground, its hangars, red and blue markings and an elevated highway with orange arrows;
    then a ruined city, broken blocks with their empty windows, rubble, dirt, the cracked road going on.
    / Niveau 4 : une base sur sol vert-bleu, ses hangars, ses marquages, une autoroute surélevée et ses flèches orange ;
    puis une ville en ruines, immeubles brisés, gravats, terre, la route fissurée qui continue."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    dirt = (80, 76, 54)
    _rect(p, 0, 0, tw, H, _rgba(dirt))
    base = 0.4 * tw
    _rect(p, 0, 0, base, H, (54, 92, 84, 255))
    for i in range(int(base / (80 * s)) + 1):                          # the base's grid / la grille de la base
        p.line([(i * 80 * s, 0), (i * 80 * s, H)], (46, 80, 72, 255), 1.4 * s)
    for j in range(int(H / (80 * s)) + 1):
        p.line([(0, j * 80 * s), (base, j * 80 * s)], (46, 80, 72, 255), 1.4 * s)
    for k in range(int(base / (420 * s))):                             # markings and hangars / marquages et hangars
        x = k * 420 * s + 60 * s
        p.line([(x, 60 * s), (x + 200 * s, 60 * s), (x + 200 * s, 150 * s)], (40, 70, 200, 255), 12 * s)
        p.line([(x + 30 * s, 84 * s), (x + 170 * s, 84 * s)], (200, 60, 40, 255), 8 * s)
        _rect(p, x + 230 * s, 330 * s, x + 380 * s, 430 * s, (100, 128, 124, 255), (30, 40, 40, 255), 3 * s)
        for j in range(6):
            p.line([(x + 236 * s, (338 + j * 15) * s), (x + 374 * s, (338 + j * 15) * s)], (80, 104, 100, 255), 2 * s)
    for _ in range(int((tw - base) * H / (2200 * s * s))):             # rubble / gravats
        x, y = rng.uniform(base, tw), rng.uniform(0, H)
        _clump(p, x, y, rng.uniform(10, 26) * s, rng, ((44, 60, 58), (66, 86, 82), (96, 112, 104)), n=5, spread=(1.3, 1.0))
    for _ in range(int((tw - base) / (150 * s))):                     # broken blocks / immeubles brisés
        x, y = rng.uniform(base + 40 * s, tw - 60 * s), rng.choice((rng.uniform(20, 170), rng.uniform(300, 440))) * s
        w, h = rng.uniform(50, 110) * s, rng.uniform(40, 90) * s
        cut = rng.uniform(0.2, 0.6)
        pts = [(x, y), (x + w, y), (x + w, y + h * cut), (x + w * 0.6, y + h), (x, y + h)]
        p.poly([(a + 8 * s, b + 10 * s) for a, b in pts], (30, 36, 34, 200))
        p.poly(pts, (94, 112, 106, 255), (34, 42, 40, 255), 2.5 * s)
        for i in range(1, int(w / (14 * s))):
            p.line([(x + i * 14 * s, y + 4 * s), (x + i * 14 * s, y + h * min(1.0, cut + 0.3) - 4 * s)], (54, 66, 62, 255), 3 * s)
    for _ in range(int((tw - base) / (260 * s))):                     # skeletons of buildings / squelettes d'immeubles
        x = rng.uniform(base + 60 * s, tw - 200 * s)
        y = rng.choice((rng.uniform(16, 90), rng.uniform(300, 360))) * s
        w, h = rng.uniform(110, 190) * s, rng.uniform(70, 96) * s
        p.poly([(x + 10 * s, y + 12 * s), (x + w + 10 * s, y + 12 * s), (x + w + 10 * s, y + h + 12 * s), (x + 10 * s, y + h + 12 * s)],
               (26, 30, 28, 190))
        _rect(p, x, y, x + w, y + h, (70, 92, 88, 255), (30, 38, 36, 255), 3 * s)
        cell = 16 * s
        for i in range(int(w / cell)):
            for j in range(int(h / cell)):
                if rng.random() < 0.12:
                    continue
                cx, cy = x + 3 * s + i * cell, y + 3 * s + j * cell
                _rect(p, cx + 2 * s, cy + 2 * s, cx + cell - 2 * s, cy + cell - 2 * s, (30, 40, 38, 255))
        cut = rng.choice(((x + w, y), (x + w, y + h), (x, y + h)))           # a broken corner / un coin brisé
        p.poly([cut, (cut[0] + (-1 if cut[0] > x else 1) * w * 0.4, cut[1]), (cut[0], cut[1] + (1 if cut[1] == y else -1) * h * 0.6)],
               _rgba(dirt))
    top, bot = RUIN_ROAD[0] - 20, RUIN_ROAD[-1] + 20                    # the highway, then the cracked road / l'autoroute
    _rect(p, 0, (top - 8) * s, base, (bot + 8) * s, (40, 44, 52, 255))
    _rect(p, 0, top * s, base, bot * s, (150, 152, 162, 255))
    for yy in (top + 3, bot - 3):
        p.line([(0, yy * s), (base, yy * s)], (210, 60, 46, 255), 3 * s)
    for k in range(int(base / (150 * s))):
        ax, my = k * 150 * s + 40 * s, (top + bot) / 2 * s
        p.poly([(ax, my - 14 * s), (ax + 30 * s, my), (ax, my + 14 * s), (ax + 10 * s, my)], (240, 140, 40, 255))
    _rect(p, base, top * s, tw, bot * s, (88, 88, 84, 255))
    for k in range(int((tw - base) / (90 * s))):                       # cracks and debris / fissures et débris
        x = base + k * 90 * s + rng.uniform(0, 60) * s
        y = rng.uniform(top + 6, bot - 6) * s
        p.line([(x, y), (x + rng.uniform(10, 30) * s, y + rng.uniform(-10, 10) * s), (x + rng.uniform(30, 60) * s, y + rng.uniform(-14, 14) * s)],
               (50, 50, 48, 255), 2 * s)
        if rng.random() < 0.4:
            p.disc(x, rng.uniform(top, bot) * s, rng.uniform(4, 9) * s, (66, 84, 80, 255), (34, 40, 40, 255), 1.4 * s)
    return {"sky": Image.new("RGB", (W, H), dirt), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- 5 the station / la station
def build_ddp_station(W, H, s, seed=3105):
    """Stage 5: a great grey machine seen from the sky, the same above and below its spine: two green channels along the
    screen, blocks of beige metal and their panels, pipes, vents, lilac bridges across, red sections, rows of lamps.
    / Niveau 5 : une grande machine grise, pareille de part et d'autre de son axe, deux canaux verts, des blocs de métal
    beige, des tuyaux, des grilles, des ponts lilas, des parties rouges, des rangées de lampes."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    metal = (128, 126, 110)
    _rect(p, 0, 0, tw, H, _rgba(metal))
    cy = sum(STATION_CHANNELS) / 2 * s
    lights = []
    x = 0.0
    while x < tw:                                                      # blocks, mirrored / blocs en miroir
        w = rng.uniform(60, 160) * s
        y = 0.0
        while y < cy - 70 * s:
            h = rng.uniform(30, 80) * s
            h = min(h, cy - 70 * s - y)
            tone = rng.choice(((150, 146, 128), (124, 120, 104), (170, 166, 146), (104, 102, 90)))
            red = rng.random() < 0.06
            col = (176, 54, 50) if red else tone
            for yy0, yy1 in ((y, y + h), (2 * cy - y - h, 2 * cy - y)):
                _rect(p, x + 3 * s, yy0 + 3 * s, x + w - 3 * s, yy1 - 3 * s, _rgba(col), (52, 52, 46, 255), 2 * s)
                p.line([(x + 6 * s, yy0 + 6 * s), (x + w - 6 * s, yy0 + 6 * s)], _rgba(_light(col, 0.3)), 1.6 * s)
                if rng.random() < 0.3:                                 # a vent / une grille
                    for k in range(int((yy1 - yy0) / (8 * s)) - 1):
                        p.line([(x + 12 * s, yy0 + (6 + k * 8) * s), (x + w - 12 * s, yy0 + (6 + k * 8) * s)], (60, 60, 54, 255), 2.4 * s)
            y += h
        x += w
    for k in range(int(tw / (220 * s))):                               # pipes / tuyaux
        x = k * 220 * s + rng.uniform(0, 100) * s
        for sgn in (-1, 1):
            p.line([(x, cy + sgn * 70 * s), (x, cy + sgn * (H / 2 + 10 * s))], (70, 70, 62, 255), 9 * s)
            p.line([(x - 2 * s, cy + sgn * 70 * s), (x - 2 * s, cy + sgn * (H / 2 + 10 * s))], (170, 168, 150, 255), 2.4 * s)
    _rect(p, 0, cy - 70 * s, tw, cy + 70 * s, (92, 92, 84, 255))         # the spine and its channels / l'axe et ses canaux
    for ch in STATION_CHANNELS:
        _rect(p, 0, (ch - 16) * s, tw, (ch + 16) * s, (30, 104, 82, 255), (24, 40, 34, 255), 3 * s)
        for k in range(int(tw / (28 * s))):
            p.line([(k * 28 * s, (ch - 12) * s), (k * 28 * s + 14 * s, (ch - 12) * s)], (70, 170, 130, 255), 2 * s)
    _rect(p, 0, cy - 12 * s, tw, cy + 12 * s, (150, 146, 128, 255), (60, 60, 54, 255), 2 * s)
    for k in range(int(tw / (120 * s))):                               # lamps on the spine / lampes sur l'axe
        lx = k * 120 * s + 60 * s
        p.disc(lx, cy, 5 * s, (255, 200, 90, 255))
        lights.append((lx, cy))
    for k in range(int(tw / (640 * s))):                               # lilac bridges / ponts lilas
        x = k * 640 * s + rng.uniform(100, 400) * s
        _rect(p, x, 0, x + 64 * s, H, (150, 150, 186, 255), (50, 50, 70, 255), 3 * s)
        for j in range(int(H / (12 * s))):
            p.line([(x + 6 * s, j * 12 * s), (x + 58 * s, j * 12 * s)], (122, 122, 160, 255), 2 * s)
        p.line([(x + 4 * s, 0), (x + 4 * s, H)], (196, 196, 226, 255), 2 * s)
    return {"sky": Image.new("RGB", (W, H), metal), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far", "lights": lights}],
            "tw": tw, "amb": {"window": (255, 200, 90)}}


# ---------------------------------------------------------------------------- 6 the hive / la ruche
def _honeycomb(p, x0, y0, x1, y1, r, s):
    """A grate of hexagonal cells in a frame. / Une grille d'alvéoles hexagonales dans un cadre."""
    _rect(p, x0, y0, x1, y1, (44, 40, 50, 255), (30, 20, 16, 255), 3 * s)
    dx, dy = r * 1.5, r * math.sqrt(3)
    i = 0
    x = x0 + r
    while x < x1 - r * 0.5:
        y = y0 + r + (dy / 2 if i % 2 else 0)
        while y < y1 - r * 0.6:
            p.poly([(x + r * 0.86 * math.cos(a * math.pi / 3), y + r * 0.86 * math.sin(a * math.pi / 3)) for a in range(6)],
                   (92, 90, 104, 255), (150, 150, 166, 255), 1.4 * s)
            y += dy
        x += dx
        i += 1


def build_ddp_nest(W, H, s, seed=3106):
    """Stage 6: the hive. Orange metal floors and their sunken frames, bands of honeycomb grates, cells lit red in
    rows; then lilac-grey plates crossed by thick purple pipes, rusty round tanks, red lamps. / Niveau 6 : la ruche,
    sols de métal orange et leurs cadres, des bandes de grilles en alvéoles, des cellules allumées en rouge ; puis des
    plaques gris-lilas, de gros tuyaux violets, des cuves rondes rouillées, des lampes rouges."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    orange = (206, 112, 52)
    _rect(p, 0, 0, tw, H, _rgba(orange))
    half = 0.52 * tw
    lights = []
    for i in range(int(half / (120 * s))):                             # orange plates / plaques orange
        for j in range(int(H / (115 * s)) + 1):
            x, y = i * 120 * s, j * 115 * s
            _rect(p, x + 4 * s, y + 4 * s, x + 116 * s, y + 111 * s, _rgba(rng.choice(((206, 112, 52), (196, 104, 46), (214, 122, 60)))),
                  (150, 74, 32, 255), 2 * s)
            if rng.random() < 0.25:
                _rect(p, x + 22 * s, y + 22 * s, x + 98 * s, y + 92 * s, None, (236, 150, 86, 255), 2 * s)
    for k in range(int(half / (700 * s))):                             # honeycomb bands / bandes d'alvéoles
        x = k * 700 * s + 60 * s
        _honeycomb(p, x, 40 * s, x + 380 * s, 150 * s, 12 * s, s)
        _honeycomb(p, x + 200 * s, 320 * s, x + 600 * s, 430 * s, 12 * s, s)
    for k in range(int(half / (560 * s))):                             # cells lit in red / cellules rouges
        x, y = k * 560 * s + 440 * s, rng.choice((60, 330)) * s
        _rect(p, x, y, x + 90 * s, y + 90 * s, (60, 40, 50, 255), (30, 16, 16, 255), 3 * s)
        for a in range(2):
            for b in range(4):
                cx, cy = x + (24 + a * 42) * s, y + (14 + b * 20) * s
                p.disc(cx, cy, 6 * s, (230, 56, 50, 255), (90, 20, 20, 255), 1.4 * s)
                lights.append((cx, cy))
    _rect(p, half, 0, tw, H, (140, 136, 166, 255))                       # the lilac-grey half / la moitié gris-lilas
    for i in range(int((tw - half) / (90 * s)) + 1):
        for j in range(int(H / (60 * s)) + 1):
            x, y = half + i * 90 * s, j * 60 * s
            _rect(p, x + 3 * s, y + 3 * s, x + 87 * s, y + 57 * s, _rgba(rng.choice(((140, 136, 166), (124, 120, 150), (154, 150, 178)))),
                  (80, 76, 100, 255), 1.6 * s)
    for k in range(int((tw - half) / (300 * s))):                      # rusty tanks / cuves rouillées
        x, y = half + k * 300 * s + rng.uniform(40, 200) * s, rng.choice((90, 380)) * s
        p.disc(x + 6 * s, y + 8 * s, 34 * s, (60, 50, 60, 200))
        p.disc(x, y, 32 * s, (176, 104, 60, 255), (70, 40, 24, 255), 3 * s)
        p.disc(x, y, 20 * s, (196, 128, 80, 255), (120, 70, 40, 255), 2 * s)
        p.disc(x - 8 * s, y - 8 * s, 6 * s, (236, 180, 130, 255))
    for yy in (40, 150, 330, 430):                                      # purple pipes / tuyaux violets
        p.line([(half, yy * s), (tw, yy * s)], (50, 26, 50, 255), 26 * s)
        p.line([(half, yy * s), (tw, yy * s)], (110, 62, 110, 255), 20 * s)
        p.line([(half, (yy - 5) * s), (tw, (yy - 5) * s)], (168, 116, 168, 255), 4 * s)
    for ch in NEST_LANES:                                               # the lanes all along / les voies
        _rect(p, 0, (ch - 14) * s, tw, (ch + 14) * s, (70, 64, 80, 255), (34, 26, 30, 255), 2.5 * s)
        for k in range(int(tw / (60 * s))):
            p.line([(k * 60 * s, ch * s), (k * 60 * s + 26 * s, ch * s)], (230, 170, 60, 255), 2 * s)
    p.line([(half, 0), (half, H)], (60, 40, 50, 255), 10 * s)
    return {"sky": Image.new("RGB", (W, H), orange), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far", "lights": lights}],
            "tw": tw, "amb": {"window": (255, 70, 60)}}


THEMES = ("ddp_forest", "ddp_base", "ddp_peaks", "ddp_ruins", "ddp_station", "ddp_nest")      # stages 1 to 6 / niveaux 1 à 6
LANES = {"ddp_base": BASE_ROAD, "ddp_forest": FOREST_BRANCH, "ddp_peaks": PEAK_VALLEY, "ddp_ruins": RUIN_ROAD,
         "ddp_station": STATION_CHANNELS, "ddp_nest": NEST_LANES}
hd_bg.BUILDERS.update({"ddp_base": build_ddp_base, "ddp_forest": build_ddp_forest, "ddp_peaks": build_ddp_peaks,
                       "ddp_ruins": build_ddp_ruins, "ddp_station": build_ddp_station, "ddp_nest": build_ddp_nest})
