"""HD backdrops of the fifth batch of Neo Geo games done one by one (1.21), each drawn after screenshots of its game.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported.

Décors HD du cinquième lot (1.21), chacun dessiné d'après des captures de son jeu. Tout est dessiné par le programme,
aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image

from . import hd_bg
from .hd_bg import mix, vgrad
from .hd_themes3 import _Pic, _clump, _fit, _rgba


# ---------------------------------------------------------------------------- NAM-1975
NAM_ROAD = 236           # middle of the road where the enemies run, at s = 1 / milieu de la route où courent les ennemis


def _ruin(p, x, base, w, h, s, rng, col, holes=True):
    """A tall building broken by the war: a jagged top, black windows, holes. / Un immeuble cassé par la guerre."""
    top = base - h
    pts = [(x, base), (x, top + rng.uniform(0, 20) * s)]
    k = 6
    for i in range(1, k):
        pts.append((x + w * i / k, top + rng.uniform(0, 40) * s))
    pts += [(x + w, top + rng.uniform(0, 30) * s), (x + w, base)]
    p.poly(pts, _rgba(col))
    for wy in range(int(top + 40 * s), int(base - 10 * s), int(18 * s)):
        for wx in range(int(x + 6 * s), int(x + w - 10 * s), int(14 * s)):
            if rng.random() < 0.75:
                lit = rng.random() < 0.08
                p.poly([(wx, wy), (wx + 7 * s, wy), (wx + 7 * s, wy + 9 * s), (wx, wy + 9 * s)], (255, 170, 60, 255) if lit else _rgba(mix(col, (0, 0, 0), 0.5)))
    if holes:
        for _ in range(2):
            hx, hy = x + rng.uniform(0.2, 0.7) * w, top + rng.uniform(0.2, 0.6) * h
            r = rng.uniform(8, 18) * s
            p.ellipse(hx - r, hy - r * 0.8, hx + r, hy + r * 0.8, _rgba(mix(col, (0, 0, 0), 0.6)))


def build_nam_city(W, H, s, seed=81):
    """NAM-1975: the burning city of the first stage, as in the game: a smoky dusk sky, broken towers in black and brown,
    a steel bridge, the road where the enemies run, rubble in front. / La ville en feu du premier niveau."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (70, 60, 70)), (0.35, (150, 110, 90)), (0.6, (200, 150, 100)), (1.0, (90, 70, 60))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    for _ in range(14):                                                  # fumées au loin
        x, y = rng.uniform(0, tw), rng.uniform(40, 140) * s
        _clump(far, x, y, rng.uniform(40, 90) * s, rng, ((120, 110, 110), (150, 140, 136)), n=6)
    x = -20 * s
    while x < tw:                                                        # la ville cassée, au loin
        w = rng.uniform(50, 110) * s
        _ruin(far, x, 196 * s, w, rng.uniform(70, 150) * s, s, rng, (50, 44, 50), holes=False)
        x += w + rng.uniform(4, 20) * s
    layers.append({"img": far.done(), "y": 0, "f": 0.2, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    x = -20 * s
    while x < tw:                                                        # les immeubles en ruine, plus près
        w = rng.uniform(80, 150) * s
        _ruin(mid, x, 206 * s, w, rng.uniform(80, 170) * s, s, rng, rng.choice(((44, 34, 30), (60, 46, 38), (36, 30, 30))))
        x += w + rng.uniform(30, 140) * s
    for bx in (tw * 0.08, tw * 0.58):                                    # un pont d'acier
        for k in range(6):
            x0 = bx + k * 40 * s
            mid.line([(x0, 206 * s), (x0 + 20 * s, 150 * s), (x0 + 40 * s, 206 * s)], (110, 40, 30, 255), 4 * s)
        mid.line([(bx, 150 * s), (bx + 240 * s, 150 * s)], (110, 40, 30, 255), 5 * s)
    layers.append({"img": mid.done(), "y": 0, "f": 0.45, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    ry = NAM_ROAD * s
    near.poly([(0, 206 * s), (tw, 206 * s), (tw, ry - 26 * s), (0, ry - 26 * s)], (70, 58, 50, 255))
    near.poly([(0, ry - 26 * s), (tw, ry - 26 * s), (tw, ry + 26 * s), (0, ry + 26 * s)], (66, 68, 76, 255))         # la route
    for k in range(int(tw / (90 * s))):
        near.line([(k * 90 * s, ry), (k * 90 * s + 44 * s, ry)], (220, 220, 200, 255), 3 * s)
    near.line([(0, ry + 22 * s), (tw, ry + 22 * s)], (200, 130, 40, 255), 3 * s)
    near.poly([(0, ry + 26 * s), (tw, ry + 26 * s), (tw, H), (0, H)], (104, 80, 60, 255))                         # les gravats
    for _ in range(int(tw * (H - ry) / (300 * s * s))):
        x, y = rng.uniform(0, tw), rng.uniform(ry + 30 * s, H)
        r = rng.uniform(3, 9) * s
        near.poly([(x - r, y), (x - r * 0.3, y - r * 0.8), (x + r, y - r * 0.3), (x + r * 0.6, y + r * 0.5)],
                  _rgba(rng.choice(((80, 62, 48), (130, 104, 80), (60, 50, 44), (150, 120, 96)))))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"dust": (220, 170, 120)}}


def build_nam_jungle(W, H, s, seed=82):
    """NAM-1975: the jungle and its river, as in the game: green hills, a dark hillside, the dirt bank where the enemies
    run, the river below with its wooden walkway. / La jungle et sa rivière, comme dans le jeu."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (120, 150, 120)), (0.5, (170, 180, 130)), (1.0, (90, 100, 70))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    pts = [(x, 120 * s - 60 * s * abs(math.sin(x / tw * math.tau * 3))) for x in range(0, tw + 20, 20)]
    far.poly(pts + [(tw, 210 * s), (0, 210 * s)], (70, 80, 50, 255))                                              # la colline
    for _ in range(int(tw / (30 * s))):
        x = rng.uniform(0, tw)
        y = 120 * s - 60 * s * abs(math.sin(x / tw * math.tau * 3)) + rng.uniform(0, 70) * s
        far.line([(x, y), (x, y - 14 * s)], (50, 50, 30, 255), 2 * s)
        far.disc(x, y - 14 * s, 5 * s, (60, 70, 40, 255))
    layers.append({"img": far.done(), "y": 0, "f": 0.25, "stage": "far"})
    near = _Pic(tw, H, 2, tw)
    ry = NAM_ROAD * s
    near.poly([(0, 196 * s), (tw, 196 * s), (tw, ry + 40 * s), (0, ry + 40 * s)], (170, 120, 50, 255))           # la berge de terre
    for row in range(5):
        for k in range(int(tw / (60 * s))):
            x, y = k * 60 * s + (row % 2) * 30 * s, 204 * s + row * 14 * s
            near.ellipse(x, y, x + 50 * s, y + 10 * s, (150, 100, 40, 255))
    near.poly([(0, ry + 40 * s), (tw, ry + 40 * s), (tw, ry + 110 * s), (0, ry + 110 * s)], (30, 150, 160, 255))  # la rivière
    for _ in range(int(tw / (40 * s))):
        x, y = rng.uniform(0, tw), rng.uniform(ry + 46 * s, ry + 104 * s)
        near.line([(x, y), (x + 24 * s, y)], (140, 220, 230, 255), 2 * s)
    near.poly([(0, ry + 110 * s), (tw, ry + 110 * s), (tw, H), (0, H)], (130, 90, 40, 255))                       # le ponton
    for k in range(int(tw / (30 * s))):
        near.line([(k * 30 * s, ry + 112 * s), (k * 30 * s, H)], (90, 60, 26, 255), 2 * s)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Cyber-Lip
CL_FLOOR = 388           # the street where the hero runs, at s = 1 / la rue où court le héros


def _facade(p, x, w, top, base, s, rng, kind):
    """A shop front of the city at night, as in the game: a theater with its glowing sign, a shop, a tall green
    building, a brick wall with a broken window. / Une façade de la ville la nuit, comme dans le jeu."""
    if kind == "theater":
        p.poly([(x, top), (x + w, top), (x + w, base), (x, base)], (110, 70, 34, 255), (50, 30, 14, 255), 2 * s)
        p.poly([(x + 10 * s, top + 20 * s), (x + w - 10 * s, top + 20 * s), (x + w - 10 * s, top + 110 * s), (x + 10 * s, top + 110 * s)],
               (70, 40, 20, 255))
        cx, cy = x + w / 2, top + 64 * s                                 # l'enseigne au néon, une écriture qui serpente
        pts = [(cx - 150 * s + i * 6 * s, cy + math.sin(i * 0.55) * 18 * s - (14 * s if i % 9 == 4 else 0)) for i in range(51)]
        p.line(pts, (255, 200, 60, 120), 12 * s)
        p.line(pts, (255, 240, 150, 255), 4 * s)
        for k in range(int((w - 20 * s) / (28 * s))):                    # les ampoules du fronton
            p.disc(x + 24 * s + k * 28 * s, top + 120 * s, 5 * s, (255, 220, 120, 255))
        for k in range(3):                                               # les portes vitrées
            dx = x + 30 * s + k * (w - 60 * s) / 3
            p.poly([(dx, base - 110 * s), (dx + (w - 90 * s) / 3, base - 110 * s), (dx + (w - 90 * s) / 3, base), (dx, base)], (30, 40, 90, 255),
                   (140, 100, 40, 255), 3 * s)
            p.chord(dx, base - 140 * s, dx + (w - 90 * s) / 3, base - 80 * s, 180, 360, (40, 60, 120, 255))
    elif kind == "green":
        p.poly([(x, top - 60 * s), (x + w, top - 60 * s), (x + w, base), (x, base)], (30, 90, 70, 255), (10, 40, 30, 255), 2 * s)
        for k in range(int(w / (50 * s))):                               # piliers et lampes
            px = x + 20 * s + k * 50 * s
            p.poly([(px, top), (px + 14 * s, top), (px + 14 * s, base), (px, base)], (50, 120, 96, 255))
            p.disc(px + 7 * s, top + 40 * s, 6 * s, (140, 220, 255, 255))
        for k in range(3):
            dx = x + 40 * s + k * (w - 80 * s) / 3
            p.poly([(dx, base - 90 * s), (dx + (w - 120 * s) / 3, base - 90 * s), (dx + (w - 120 * s) / 3, base), (dx, base)], (10, 30, 30, 255),
                   (90, 200, 170, 255), 2 * s)
    elif kind == "brick":
        p.poly([(x, top + 40 * s), (x + w, top + 40 * s), (x + w, base), (x, base)], (60, 110, 60, 255), (20, 50, 20, 255), 2 * s)
        for row in range(int((base - top - 40 * s) / (12 * s))):
            yy = top + 40 * s + row * 12 * s
            off = (row % 2) * 16 * s
            for k in range(int(w / (32 * s)) + 1):
                bx = x + off + k * 32 * s
                if bx < x + w - 4 * s:
                    p.line([(bx, yy), (bx, yy + 12 * s)], (40, 80, 40, 255), 1.4 * s)
            p.line([(x, yy), (x + w, yy)], (40, 80, 40, 255), 1.4 * s)
        wx, wy = x + w * 0.4, top + 80 * s
        p.poly([(wx, wy), (wx + 60 * s, wy), (wx + 60 * s, wy + 60 * s), (wx, wy + 60 * s)], (30, 30, 40, 255), (200, 200, 200, 255), 3 * s)
        p.line([(wx + 10 * s, wy + 10 * s), (wx + 30 * s, wy + 40 * s), (wx + 50 * s, wy + 20 * s)], (200, 210, 230, 255), 2 * s)
    else:                                                                # boutique
        col = rng.choice(((90, 60, 40), (70, 56, 50), (100, 80, 50)))
        p.poly([(x, top + 20 * s), (x + w, top + 20 * s), (x + w, base), (x, base)], _rgba(col), (30, 20, 14, 255), 2 * s)
        p.poly([(x + 14 * s, base - 120 * s), (x + w - 14 * s, base - 120 * s), (x + w - 14 * s, base - 20 * s), (x + 14 * s, base - 20 * s)],
               (255, 200, 110, 255), (40, 30, 20, 255), 3 * s)                                      # la vitrine éclairée
        for k in range(3):
            p.line([(x + 14 * s + k * (w - 28 * s) / 3, base - 120 * s), (x + 14 * s + k * (w - 28 * s) / 3, base - 20 * s)], (40, 30, 20, 255), 2 * s)
        stripes = rng.choice((((200, 50, 50), (240, 240, 240)), ((40, 120, 60), (240, 240, 240)), ((40, 70, 150), (240, 220, 120))))
        for k in range(int(w / (20 * s))):                               # le store rayé
            p.poly([(x + k * 20 * s, base - 150 * s), (x + (k + 1) * 20 * s, base - 150 * s), (x + (k + 1) * 20 * s + 6 * s, base - 128 * s),
                    (x + k * 20 * s + 6 * s, base - 128 * s)], _rgba(stripes[k % 2]))


def build_cl_city(W, H, s, seed=83):
    """Cyber-Lip: the city at night of the first stage, as in the game: dark blue towers far off, a theater with its
    glowing sign, shops with striped awnings, a tall green building, a brick wall, the street in front.
    / La ville la nuit du premier niveau, comme dans le jeu : théâtre et son enseigne, boutiques, immeuble vert."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (10, 14, 40)), (0.6, (30, 40, 90)), (1.0, (40, 30, 60))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw:
        w = rng.uniform(60, 140) * s
        h = rng.uniform(120, 260) * s
        far.poly([(x, 300 * s - h), (x + w, 300 * s - h), (x + w, 300 * s), (x, 300 * s)], (24, 34, 74, 255))
        for wy in range(int(300 * s - h + 10 * s), int(300 * s), int(16 * s)):
            for wx in range(int(x + 6 * s), int(x + w - 8 * s), int(12 * s)):
                if rng.random() < 0.25:
                    far.poly([(wx, wy), (wx + 5 * s, wy), (wx + 5 * s, wy + 7 * s), (wx, wy + 7 * s)], (120, 160, 230, 255))
        x += w + rng.uniform(4, 30) * s
    layers.append({"img": far.done(), "y": 0, "f": 0.2, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    base = CL_FLOOR * s
    kinds = ["theater", "shop", "green", "shop", "brick", "shop", "theater", "green", "shop", "brick"]
    x = 0.0
    k = 0
    signs = []
    while x < tw - 100 * s:
        kind = kinds[k % len(kinds)]
        w = {"theater": 420, "green": 340, "brick": 300}.get(kind, 220) * s
        w = min(w, tw - x)
        top = base - rng.uniform(250, 300) * s
        _facade(mid, x, w, top, base, s, rng, kind)
        if kind == "theater":
            signs.append((x + w / 2, top + 64 * s))
        x += w
        k += 1
    layers.append({"img": mid.done(), "y": 0, "f": 0.55, "stage": "mid", "lights": signs})
    near = _Pic(tw, H, 2, tw)
    near.poly([(0, base), (tw, base), (tw, base + 14 * s), (0, base + 14 * s)], (120, 120, 130, 255))           # le trottoir
    for k in range(int(tw / (60 * s))):
        near.line([(k * 60 * s, base), (k * 60 * s, base + 14 * s)], (80, 80, 90, 255), 2 * s)
    near.poly([(0, base + 14 * s), (tw, base + 14 * s), (tw, H), (0, H)], (44, 44, 54, 255))                   # la rue
    for k in range(int(tw / (160 * s))):
        near.line([(k * 160 * s, base + 50 * s), (k * 160 * s + 80 * s, base + 50 * s)], (200, 190, 120, 255), 4 * s)
    for k in range(int(tw / (400 * s))):                                 # réverbères
        lx = k * 400 * s + 200 * s
        near.line([(lx, base), (lx, base - 230 * s), (lx + 30 * s, base - 240 * s)], (60, 60, 70, 255), 5 * s)
        near.disc(lx + 34 * s, base - 236 * s, 8 * s, (255, 240, 200, 255))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near", "lights": [(k * 400 * s + 234 * s, base - 236 * s)
                                                                                   for k in range(int(tw / (400 * s)))]})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"window": (255, 220, 140)}}


# ---------------------------------------------------------------------------- Ghost Pilots
GP_LANES = (120, 330)    # where boats and tanks go, at s = 1 / où passent bateaux et chars


def build_gp_world(W, H, s, seed=84):
    """Ghost Pilots seen from the sky, as in the game: brown earth spotted with dark green trees and rocks, then the
    deep blue sea with its waves and a jungle coast, in one long loop. / Vu du ciel, comme dans le jeu : terre brune
    piquée d'arbres, puis la mer bleu profond et une côte de jungle."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    sea0, sea1 = tw * 0.55, tw * 0.95                                    # where the sea is / la mer
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (120, 80, 40, 255))
    for _ in range(int(tw * H / (500 * s * s))):                          # la terre et ses taches
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        r = rng.uniform(6, 20) * s
        p.ellipse(x - r, y - r * 0.7, x + r, y + r * 0.7, _rgba(rng.choice(((108, 70, 36), (132, 90, 46), (100, 66, 34)))))
    coast = [(sea0 + 60 * s * math.sin(y / H * math.tau * 1.3) + 20 * s * math.sin(y / H * math.tau * 4), y) for y in range(-10, H + 20, 10)]
    coast2 = [(sea1 + 50 * s * math.sin(y / H * math.tau * 1.1 + 1) + 16 * s * math.sin(y / H * math.tau * 5), y) for y in range(-10, H + 20, 10)]
    p.poly(coast + coast2[::-1], (24, 50, 130, 255))                        # la mer
    for _ in range(int((sea1 - sea0) * H / (300 * s * s))):
        x, y = rng.uniform(sea0, sea1), rng.uniform(0, H)
        p.line([(x, y), (x + 10 * s, y - 3 * s), (x + 20 * s, y)], (60, 100, 190, 255), 2 * s)
    for side in (coast, coast2):                                         # l'écume
        p.line(side, (200, 220, 250, 255), 4 * s)
    for _ in range(int(tw / (30 * s))):                                  # bosquets de jungle
        x, y = rng.uniform(0, sea0 - 40 * s), rng.uniform(0, H)
        _clump(p, x, y, rng.uniform(26, 52) * s, rng, ((44, 70, 26), (62, 92, 34), (96, 128, 52)), n=8)
    for _ in range(int(tw / (6 * s))):                                   # arbres sombres, denses au bord de la mer
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        if sea0 - 40 * s < x < sea1 + 40 * s and not (x > sea1 + 30 * s):
            if not (abs(x - sea0) < 70 * s or abs(x - sea1) < 70 * s):
                continue
        r = rng.uniform(6, 13) * s
        p.disc(x + r * 0.4, y + r * 0.4, r, (40, 30, 16, 140))
        p.disc(x, y, r, _rgba(rng.choice(((50, 80, 30), (64, 96, 36), (40, 66, 26)))))
        p.disc(x - r * 0.3, y - r * 0.3, r * 0.5, (100, 140, 60, 255))
    for _ in range(int(tw / (120 * s))):                                 # rochers gris
        x, y = rng.uniform(0, sea0 - 60 * s), rng.uniform(0, H)
        r = rng.uniform(14, 30) * s
        p.poly([(x - r, y), (x - r * 0.4, y - r * 0.8), (x + r * 0.6, y - r * 0.6), (x + r, y + r * 0.2), (x + r * 0.2, y + r * 0.7)],
               (90, 84, 90, 255), (50, 46, 50, 255), 1.4 * s)
    img = p.done().convert("RGB")
    return {"sky": Image.new("RGB", (W, H), (120, 80, 40)), "layers": [{"img": img, "y": 0, "f": 1.0, "stage": "far"}], "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Alpha Mission II
def build_am_fortress(W, H, s, seed=85):
    """Alpha Mission II: deep space and its stars, a huge mechanical fortress seen from above, as in the game:
    green-grey plates, pipes, vents, red lights, the dark bays between its arms. / L'espace et une immense forteresse
    mécanique vue de haut, comme dans le jeu : plaques gris-vert, tuyaux, grilles, voyants rouges."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (4, 4, 12, 255))
    for _ in range(int(tw * H / (900 * s * s))):                          # les étoiles
        p.disc(rng.uniform(0, tw), rng.uniform(0, H), rng.uniform(0.6, 1.6) * s, _rgba(rng.choice(((200, 200, 255), (255, 240, 200), (150, 160, 220)))))
    x = 0.0
    while x < tw:                                                        # les modules de la forteresse
        w = rng.uniform(260, 520) * s
        y0 = rng.uniform(40, 110) * s
        y1 = H - rng.uniform(40, 110) * s
        p.poly([(x + 30 * s, y0), (x + w - 30 * s, y0), (x + w, y0 + 30 * s), (x + w, y1 - 30 * s), (x + w - 30 * s, y1), (x + 30 * s, y1),
                (x, y1 - 30 * s), (x, y0 + 30 * s)], (58, 74, 70, 255), (24, 30, 30, 255), 3 * s)
        for k in range(int((y1 - y0) / (36 * s))):                       # plaques
            yy = y0 + 18 * s + k * 36 * s
            p.line([(x + 14 * s, yy), (x + w - 14 * s, yy)], (40, 52, 50, 255), 2 * s)
        for k in range(int(w / (60 * s))):
            xx = x + 30 * s + k * 60 * s
            p.line([(xx, y0 + 10 * s), (xx, y1 - 10 * s)], (44, 56, 54, 255), 2 * s)
        p.poly([(x + w * 0.3, y0 + 50 * s), (x + w * 0.7, y0 + 50 * s), (x + w * 0.7, y1 - 50 * s), (x + w * 0.3, y1 - 50 * s)],
               (120, 136, 130, 255), (40, 50, 48, 255), 2 * s)           # le pont central, plus clair
        for k in range(int((y1 - y0 - 100 * s) / (24 * s))):
            yy = y0 + 60 * s + k * 24 * s
            p.line([(x + w * 0.32, yy), (x + w * 0.68, yy)], (90, 104, 100, 255), 1.4 * s)
        for _ in range(4):                                               # tuyaux
            yy = rng.uniform(y0 + 20 * s, y1 - 20 * s)
            p.line([(x, yy), (x + w * 0.28, yy)], (100, 90, 50, 255), 6 * s)
            p.line([(x, yy - 2 * s), (x + w * 0.28, yy - 2 * s)], (170, 150, 80, 255), 2 * s)
        for _ in range(3):                                               # voyants rouges
            p.disc(x + rng.uniform(0.1, 0.9) * w, rng.uniform(y0 + 20 * s, y1 - 20 * s), 6 * s, (220, 40, 40, 255), (60, 10, 10, 255), 1.6 * s)
        x += w + rng.uniform(80, 200) * s
    img = p.done().convert("RGB")
    return {"sky": Image.new("RGB", (W, H), (4, 4, 12)), "layers": [{"img": img, "y": 0, "f": 1.0, "stage": "far"}], "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Viewpoint
def build_vp_floor(W, H, s, seed=86):
    """Viewpoint: the floor of the game seen at an angle, as in the game: slate tiles laid in diamonds, raised pipes
    running across, green trenches, round hatches. / Le sol du jeu vu de biais : dalles d'ardoise en losanges, gros
    tuyaux, tranchées vertes, trappes rondes."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (44, 52, 66, 255))
    tw_, th_ = 120 * s, 60 * s                                           # un losange
    for row in range(-1, int(H / (th_ / 2)) + 2):
        for col in range(-1, int(tw / tw_) + 2):
            cx = col * tw_ + (row % 2) * tw_ / 2
            cy = row * th_ / 2
            pts = [(cx, cy - th_ / 2), (cx + tw_ / 2, cy), (cx, cy + th_ / 2), (cx - tw_ / 2, cy)]
            shade = rng.choice(((56, 66, 82), (60, 70, 86), (52, 62, 78)))
            p.poly(pts, _rgba(shade), (30, 36, 46, 255), 2 * s)
            p.line([pts[3], pts[0], pts[1]], (86, 98, 116, 255), 1.4 * s)
    for k in range(int(tw / (700 * s)) + 1):                              # tranchées vertes en biais
        x = k * 700 * s + rng.uniform(0, 200) * s
        pts = [(x, 0), (x + 90 * s, 0), (x + 90 * s + H * 1.4, H), (x + H * 1.4, H)]
        p.poly(pts, (30, 60, 34, 255))
        for j in range(5):
            o = 14 * s + j * 16 * s
            p.line([(x + o, 0), (x + o + H * 1.4, H)], (60, 120, 60, 255), 4 * s)
    for k in range(int(tw / (520 * s)) + 1):                              # gros tuyaux en biais
        x = k * 520 * s + 300 * s
        for o, col in ((0, (90, 76, 60)), (6 * s, (140, 120, 90)), (14 * s, (70, 60, 48))):
            p.line([(x + o, H), (x + o + H * 1.4, 0)], _rgba(col), (22 - o / s) * s if o else 26 * s)
    for _ in range(int(tw / (260 * s))):                                 # trappes rondes rouges
        x, y = rng.uniform(0, tw), rng.uniform(40, H - 40) * 1.0
        p.ellipse(x - 34 * s, y - 16 * s, x + 34 * s, y + 16 * s, (90, 40, 40, 255), (200, 60, 60, 255), 4 * s)
        p.ellipse(x - 18 * s, y - 8 * s, x + 18 * s, y + 8 * s, (40, 20, 20, 255), (230, 230, 230, 255), 2 * s)
    img = p.done().convert("RGB")
    return {"sky": Image.new("RGB", (W, H), (44, 52, 66)), "layers": [{"img": img, "y": 0, "f": 1.0, "stage": "far"}], "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Zed Blade
def build_zb_valley(W, H, s, seed=87):
    """Zed Blade: a valley at dawn, as in the game: a deep blue sky, violet mountains, a band of white mist, the forest
    in green and autumn orange, the rocky ground and its stone pillars. / Une vallée à l'aube, comme dans le jeu."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (40, 60, 200)), (0.45, (90, 110, 230)), (0.62, (220, 230, 250)), (1.0, (120, 150, 90))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    pts = [(x, 210 * s - 70 * s * abs(math.sin(x / tw * math.tau * 3)) - 34 * s * abs(math.sin(x / tw * math.tau * 9 + 1))
            - 14 * s * abs(math.sin(x / tw * math.tau * 23))) for x in range(0, tw + 10, 10)]
    far.poly(pts + [(tw, 260 * s), (0, 260 * s)], (70, 70, 170, 255))
    far.line(pts, (150, 150, 230, 255), 3 * s)
    far.poly([(0, 228 * s), (tw, 228 * s), (tw, 262 * s), (0, 262 * s)], (236, 240, 252, 200))                    # la brume
    layers.append({"img": far.done(), "y": 0, "f": 0.12, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    mid.poly([(0, 260 * s), (tw, 260 * s), (tw, 340 * s), (0, 340 * s)], (60, 100, 50, 255))
    for _ in range(int(tw / (26 * s))):                                  # la forêt, vert et orange
        x, y = rng.uniform(0, tw), rng.uniform(262, 330) * s
        tones = rng.choice((((40, 90, 40), (60, 120, 50), (100, 160, 70)), ((170, 90, 30), (210, 130, 40), (240, 180, 80)),
                            ((50, 100, 46), (80, 130, 56), (130, 170, 80))))
        _clump(mid, x, y, rng.uniform(16, 30) * s, rng, tones, n=6)
    layers.append({"img": mid.done(), "y": 0, "f": 0.35, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    near.poly([(0, 380 * s), (tw, 380 * s), (tw, H), (0, H)], (130, 100, 70, 255))
    for _ in range(int(tw / (18 * s))):                                  # le sol de pierre
        x, y = rng.uniform(0, tw), rng.uniform(385, H) * 1.0
        r = rng.uniform(6, 18) * s
        near.poly([(x - r, y), (x - r * 0.5, y - r * 0.7), (x + r * 0.6, y - r * 0.5), (x + r, y + r * 0.3)],
                  _rgba(rng.choice(((150, 120, 84), (110, 84, 60), (170, 140, 100)))))
    for k in range(int(tw / (600 * s))):                                 # piliers de pierre
        x = k * 600 * s + rng.uniform(100, 400) * s
        w, h = rng.uniform(60, 110) * s, rng.uniform(70, 150) * s
        near.poly([(x, 390 * s), (x + w * 0.1, 390 * s - h), (x + w * 0.9, 390 * s - h - 10 * s), (x + w, 390 * s)], (150, 110, 70, 255),
                  (70, 50, 30, 255), 2 * s)
        for j in range(4):
            near.line([(x + w * (0.2 + 0.2 * j), 390 * s - h), (x + w * (0.25 + 0.2 * j), 390 * s)], (110, 80, 50, 255), 2 * s)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Prehistoric Isle 2
def build_pi_sea(W, H, s, seed=88):
    """Prehistoric Isle 2: the sea by the island, as in the game: a pale sky, the cliff far off, stone pillars rising
    from the blue sea, the waves breaking at their feet. / La mer au bord de l'île, comme dans le jeu."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (120, 170, 220)), (0.35, (190, 214, 236)), (0.4, (40, 120, 200)), (1.0, (20, 70, 150))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    for k in range(3):                                                   # falaises au loin
        x = k * tw / 3 + rng.uniform(0, 200) * s
        far.poly([(x, 160 * s), (x + 60 * s, 90 * s), (x + 300 * s, 80 * s), (x + 420 * s, 120 * s), (x + 460 * s, 165 * s)], (150, 130, 100, 255),
                 (90, 70, 50, 255), 2 * s)
        far.poly([(x + 60 * s, 90 * s), (x + 300 * s, 80 * s), (x + 300 * s, 100 * s), (x + 70 * s, 110 * s)], (90, 130, 70, 255))
    layers.append({"img": far.done(), "y": 0, "f": 0.1, "stage": "far"})
    sea = _Pic(tw, H, 2, tw)
    for _ in range(int(tw * (H - 170 * s) / (500 * s * s))):             # vagues
        x, y = rng.uniform(0, tw), rng.uniform(175, H) * 1.0
        k = (y - 170 * s) / (H - 170 * s)
        sea.line([(x, y), (x + (14 + 30 * k) * s, y - 2 * s), (x + (28 + 60 * k) * s, y)], (120, 190, 240, 200), (1.2 + 2 * k) * s)
    for _ in range(int(tw / (300 * s))):                                 # piliers de pierre et leur écume
        x = rng.uniform(0, tw)
        base = rng.uniform(250, 440) * s
        w = rng.uniform(50, 96) * s
        h = rng.uniform(100, 200) * s
        side = [(x - w / 2 + rng.uniform(-6, 6) * s, base - h * k / 6) for k in range(7)]
        side2 = [(x + w / 2 + rng.uniform(-6, 6) * s, base - h * k / 6) for k in range(7)]
        sea.poly(side + side2[::-1], (130, 110, 80, 255), (70, 56, 40, 255), 2 * s)
        sea.poly([(x - w / 2 - 6 * s, base - h + 4 * s), (x + w / 2 + 6 * s, base - h - 2 * s), (x + w / 2 + 2 * s, base - h + 16 * s),
                  (x - w / 2 - 2 * s, base - h + 18 * s)], (160, 140, 100, 255), (70, 56, 40, 255), 2 * s)
        for j in range(3):
            sea.line([(x - w / 2 + (j + 1) * w / 4, base - h + 20 * s), (x - w / 2 + (j + 1) * w / 4 + 2 * s, base)], (100, 84, 60, 255), 2 * s)
        sea.ellipse(x - w, base - 8 * s, x + w, base + 8 * s, (240, 250, 255, 220))
    layers.append({"img": sea.done(), "y": 0, "f": 0.8, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Brawlers: Robo Army, Burning Fight
BRAWL_FLOOR = 300        # top of the ground where the fighters walk, at s = 1 / haut du sol où marchent les combattants


def build_ra_town(W, H, s, seed=89):
    """Robo Army: the edge of the town at dusk, as in the game: a purple sky, the city far off with its orange lights,
    a long wooden fence, wire fences, a small concrete house with cracked walls, the ground of dry grass.
    / Le bord de la ville au crépuscule, comme dans le jeu : ciel violet, palissade, grillage, maison de béton fissurée."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (40, 30, 80)), (0.35, (110, 70, 130)), (0.55, (200, 120, 110)), (1.0, (120, 90, 60))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    x = 0.0
    while x < tw:                                                        # la ville au loin
        w = rng.uniform(30, 80) * s
        h = rng.uniform(30, 110) * s
        far.poly([(x, 230 * s - h), (x + w, 230 * s - h), (x + w, 230 * s), (x, 230 * s)], (60, 40, 80, 255))
        for wy in range(int(230 * s - h + 6 * s), int(230 * s), int(10 * s)):
            for wx in range(int(x + 4 * s), int(x + w - 4 * s), int(8 * s)):
                if rng.random() < 0.3:
                    far.poly([(wx, wy), (wx + 3 * s, wy), (wx + 3 * s, wy + 4 * s), (wx, wy + 4 * s)], (255, 170, 80, 255))
        x += w + rng.uniform(2, 14) * s
    layers.append({"img": far.done(), "y": 0, "f": 0.15, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    base = BRAWL_FLOOR * s
    x = 0.0
    while x < tw:
        kind = rng.choice(("fence", "fence", "wire", "house", "tree"))
        if kind == "fence":                                              # palissade de planches
            w = rng.uniform(300, 500) * s
            for k in range(int(w / (16 * s))):
                bx = x + k * 16 * s
                mid.poly([(bx, base - 90 * s), (bx + 15 * s, base - 90 * s), (bx + 15 * s, base), (bx, base)], (150, 90, 50, 255),
                         (80, 44, 22, 255), 1.4 * s)
            mid.poly([(x, base - 70 * s), (x + w, base - 70 * s), (x + w, base - 62 * s), (x, base - 62 * s)], (110, 60, 30, 255))
        elif kind == "wire":                                             # grillage
            w = rng.uniform(200, 320) * s
            for k in range(int(w / (60 * s)) + 1):
                mid.line([(x + k * 60 * s, base - 150 * s), (x + k * 60 * s, base)], (120, 120, 130, 255), 4 * s)
            for k in range(int(w / (10 * s))):
                mid.line([(x + k * 10 * s, base - 150 * s), (x + k * 10 * s + 40 * s, base)], (170, 170, 180, 140), 1.2 * s)
                mid.line([(x + k * 10 * s + 40 * s, base - 150 * s), (x + k * 10 * s, base)], (170, 170, 180, 140), 1.2 * s)
        elif kind == "house":                                            # maison de béton fissurée
            w = rng.uniform(260, 360) * s
            mid.poly([(x, base - 170 * s), (x + w, base - 170 * s), (x + w, base), (x, base)], (220, 200, 150, 255), (100, 80, 50, 255), 2 * s)
            mid.poly([(x - 10 * s, base - 180 * s), (x + w + 10 * s, base - 180 * s), (x + w + 10 * s, base - 168 * s), (x - 10 * s, base - 168 * s)],
                     (160, 140, 100, 255))
            for k in range(2):
                wx = x + w * (0.2 + 0.4 * k)
                mid.poly([(wx, base - 140 * s), (wx + 70 * s, base - 140 * s), (wx + 70 * s, base - 80 * s), (wx, base - 80 * s)], (40, 30, 30, 255),
                         (90, 70, 50, 255), 3 * s)
                for j in range(4):
                    mid.line([(wx + 10 * s + j * 16 * s, base - 140 * s), (wx + 10 * s + j * 16 * s, base - 80 * s)], (150, 150, 160, 255), 2 * s)
            mid.line([(x + w * 0.1, base - 160 * s), (x + w * 0.16, base - 120 * s), (x + w * 0.12, base - 90 * s)], (120, 100, 70, 255), 2 * s)
            mid.poly([(x + w * 0.62, base - 20 * s), (x + w * 0.75, base - 50 * s), (x + w * 0.9, base - 30 * s), (x + w * 0.85, base)],
                     (180, 160, 120, 255))                               # gravats
        else:                                                            # un arbre
            w = 200 * s
            mid.poly([(x + 80 * s, base), (x + 92 * s, base - 150 * s), (x + 108 * s, base - 150 * s), (x + 120 * s, base)], (90, 70, 40, 255))
            _clump(mid, x + 100 * s, base - 190 * s, 80 * s, rng, ((50, 70, 30), (80, 100, 40), (130, 140, 60)), n=9)
        x += w + rng.uniform(0, 60) * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    near.poly([(0, base), (tw, base), (tw, H), (0, H)], (170, 150, 80, 255))           # l'herbe sèche
    for _ in range(int(tw * (H - base) / (200 * s * s))):
        x, y = rng.uniform(0, tw), rng.uniform(base, H)
        near.line([(x, y), (x + rng.uniform(-3, 3) * s, y - rng.uniform(4, 10) * s)], _rgba(rng.choice(((130, 120, 50), (200, 180, 100), (110, 100, 40)))),
                  1.6 * s)
    for _ in range(int(tw / (50 * s))):
        x, y = rng.uniform(0, tw), rng.uniform(base + 10 * s, H)
        near.ellipse(x - 30 * s, y - 6 * s, x + 30 * s, y + 6 * s, (120, 100, 60, 200))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"window": (255, 170, 80)}}


def build_bf_street(W, H, s, seed=90):
    """Burning Fight: a street of small Japanese shops at night, as in the game: wooden fronts, paper lanterns, glowing
    signs in squares, a vending machine, the shop window full of dishes, the paved street in front.
    / Une rue de petites boutiques japonaises la nuit, comme dans le jeu : lanternes, enseignes, distributeur, pavés."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (16, 12, 24)), (1.0, (40, 30, 40))])
    p = _Pic(tw, H, 2, tw)
    base = BRAWL_FLOOR * s
    x = 0.0
    lights = []
    while x < tw:
        kind = rng.choice(("shop", "shop", "vending", "restaurant"))
        w = {"vending": 120, "restaurant": 380}.get(kind, 300) * s
        top = rng.uniform(10, 40) * s
        wood = rng.choice(((110, 70, 40), (90, 60, 36), (130, 90, 50)))
        p.poly([(x, top), (x + w, top), (x + w, base), (x, base)], _rgba(wood), (40, 24, 14, 255), 2 * s)
        for k in range(int(w / (60 * s))):                               # les enseignes carrées
            sx = x + 14 * s + k * 60 * s
            col = rng.choice(((240, 240, 230), (240, 220, 120), (230, 70, 60)))
            p.poly([(sx, top + 14 * s), (sx + 50 * s, top + 14 * s), (sx + 50 * s, top + 64 * s), (sx, top + 64 * s)], _rgba(col), (40, 24, 14, 255),
                   2 * s)
            p.line([(sx + 12 * s, top + 26 * s), (sx + 38 * s, top + 26 * s)], (40, 30, 30, 255), 4 * s)
            p.line([(sx + 25 * s, top + 26 * s), (sx + 25 * s, top + 54 * s)], (40, 30, 30, 255), 4 * s)
            p.line([(sx + 14 * s, top + 44 * s), (sx + 36 * s, top + 44 * s)], (40, 30, 30, 255), 3 * s)
        if kind == "vending":                                            # distributeur de boissons
            p.poly([(x + 10 * s, base - 200 * s), (x + w - 10 * s, base - 200 * s), (x + w - 10 * s, base), (x + 10 * s, base)], (230, 230, 240, 255),
                   (60, 60, 70, 255), 2 * s)
            p.poly([(x + 20 * s, base - 186 * s), (x + w - 20 * s, base - 186 * s), (x + w - 20 * s, base - 90 * s), (x + 20 * s, base - 90 * s)],
                   (120, 190, 240, 255))
            for r in range(3):
                for c in range(4):
                    p.poly([(x + 26 * s + c * 18 * s, base - 178 * s + r * 30 * s), (x + 38 * s + c * 18 * s, base - 178 * s + r * 30 * s),
                            (x + 38 * s + c * 18 * s, base - 156 * s + r * 30 * s), (x + 26 * s + c * 18 * s, base - 156 * s + r * 30 * s)],
                           _rgba(rng.choice(((220, 60, 60), (60, 120, 220), (240, 200, 60), (80, 180, 90)))))
            lights.append((x + w / 2, base - 140 * s))
        else:
            gx0, gx1 = x + 30 * s, x + w - 30 * s                        # la vitrine éclairée et ses plats
            p.poly([(gx0, base - 150 * s), (gx1, base - 150 * s), (gx1, base - 50 * s), (gx0, base - 50 * s)], (255, 210, 130, 255), (60, 36, 20, 255),
                   3 * s)
            for k in range(int((gx1 - gx0) / (40 * s))):
                dx = gx0 + 10 * s + k * 40 * s
                p.ellipse(dx, base - 90 * s, dx + 28 * s, base - 80 * s, (240, 240, 230, 255))
                p.ellipse(dx + 6 * s, base - 96 * s, dx + 22 * s, base - 86 * s, _rgba(rng.choice(((230, 120, 80), (240, 200, 160), (200, 80, 60)))))
            if kind == "restaurant":                                     # le rideau à l'entrée
                for k in range(5):
                    cx = x + w * 0.35 + k * 22 * s
                    p.poly([(cx, base - 170 * s), (cx + 20 * s, base - 170 * s), (cx + 20 * s, base - 120 * s), (cx, base - 120 * s)], (40, 50, 110, 255),
                           (20, 20, 40, 255), 1 * s)
            lights.append(((gx0 + gx1) / 2, base - 100 * s))
        for k in range(2):                                               # lanternes de papier
            lx = x + w * (0.25 + 0.5 * k)
            p.line([(lx, top + 70 * s), (lx, top + 84 * s)], (40, 30, 20, 255), 2 * s)
            p.ellipse(lx - 16 * s, top + 84 * s, lx + 16 * s, top + 124 * s, (240, 70, 50, 255), (90, 30, 20, 255), 2 * s)
            lights.append((lx, top + 104 * s))
        x += w + rng.uniform(4, 20) * s
    p.poly([(0, base), (tw, base), (tw, H), (0, H)], (90, 80, 80, 255))                   # les pavés
    for row in range(int((H - base) / (20 * s)) + 1):
        y = base + row * 20 * s
        p.line([(0, y), (tw, y)], (60, 54, 56, 255), 2 * s)
        for k in range(int(tw / (40 * s)) + 1):
            xx = k * 40 * s + (row % 2) * 20 * s
            p.line([(xx, y), (xx, y + 20 * s)], (60, 54, 56, 255), 2 * s)
    img = p.done()
    sky = sky.convert("RGBA")
    return {"sky": Image.new("RGB", (W, H), (16, 12, 24)), "layers": [{"img": img, "y": 0, "f": 1.0, "stage": "mid", "lights": lights}], "tw": tw,
            "amb": {"window": (255, 190, 120)}}


# ---------------------------------------------------------------------------- Shock Troopers 2nd Squad
ST2_ROAD = (206, 414)    # top and bottom of the road at s = 1 / haut et bas de la route


def _wreck(p, x, y, w, h, s, rng):
    """A burnt car seen from above. / Une voiture brûlée vue du dessus."""
    body = rng.choice(((70, 60, 52), (88, 70, 50), (60, 62, 66)))
    p.poly([(x + 5 * s, y + h * 0.9), (x + w + 8 * s, y + h * 0.9), (x + w + 8 * s, y + h + 8 * s), (x + 5 * s, y + h + 8 * s)], (66, 70, 66, 255))
    for wx in (x + w * 0.18, x + w * 0.78):                              # les roues
        for wy in (y - 3 * s, y + h - 6 * s):
            p.poly([(wx - 8 * s, wy), (wx + 8 * s, wy), (wx + 8 * s, wy + 9 * s), (wx - 8 * s, wy + 9 * s)], (24, 22, 22, 255))
    p.poly([(x, y + 4 * s), (x + w, y + 4 * s), (x + w, y + h - 2 * s), (x, y + h - 2 * s)], _rgba(body), (24, 20, 18, 255), 1.5 * s)
    p.poly([(x + w * 0.3, y + 8 * s), (x + w * 0.66, y + 8 * s), (x + w * 0.66, y + h - 6 * s), (x + w * 0.3, y + h - 6 * s)],
           (30, 28, 30, 255))                                            # l'habitacle brûlé
    for _ in range(4):
        cx, cy = x + rng.uniform(0.1, 0.9) * w, y + rng.uniform(0.2, 0.8) * h
        p.disc(cx, cy, rng.uniform(3, 7) * s, (120, 60, 30, 255))       # la rouille


def build_st2_street(W, H, s, seed=91):
    """Shock Troopers 2nd Squad: the city street seen from above, as in the game: a garden and a cracked stone wall
    with stains of paint at the top, the white tiled pavement and its lamp posts, the grey road full of cracks with
    its yellow middle line and its white dashes, burnt cars, the pavement at the bottom.
    / La rue de la ville vue du dessus, comme dans le jeu : jardin et mur fissuré, trottoir blanc carrelé et ses
    lampadaires, route grise fissurée et sa ligne jaune, voitures brûlées."""
    rng = random.Random(seed)
    tw = 2 * W
    r0, r1 = ST2_ROAD[0] * s, ST2_ROAD[1] * s
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, 74 * s), (0, 74 * s)], (54, 70, 46, 255))                   # le jardin
    for _ in range(int(tw / (40 * s))):
        _clump(p, rng.uniform(0, tw), rng.uniform(0, 62) * s, rng.uniform(22, 44) * s, rng, ((30, 62, 30), (56, 100, 46), (104, 150, 74)), n=6)
    wy0, wy1 = 66 * s, 112 * s                                           # le mur de pierre
    p.poly([(0, wy0), (tw, wy0), (tw, wy1), (0, wy1)], (150, 150, 138, 255))
    p.poly([(0, wy1 - 6 * s), (tw, wy1 - 6 * s), (tw, wy1), (0, wy1)], (110, 110, 100, 255))
    for row in range(3):
        y = wy0 + row * 14 * s
        p.line([(0, y), (tw, y)], (112, 112, 102, 255), 1.5 * s)
        x = (row % 2) * 22 * s
        while x < tw:
            p.line([(x, y), (x, y + 14 * s)], (112, 112, 102, 255), 1.5 * s)
            x += 44 * s
    for _ in range(int(tw / (160 * s))):                                 # taches de peinture sur le mur
        x = rng.uniform(0, tw)
        col = rng.choice(((200, 60, 50), (70, 90, 200), (230, 200, 60), (60, 160, 90)))
        pts = [(x + i * 9 * s, wy0 + rng.uniform(8, 34) * s) for i in range(rng.randint(4, 9))]
        p.line(pts, _rgba(col), rng.uniform(3, 6) * s)
    for _ in range(int(tw / (120 * s))):                                 # fissures et trous du mur
        x = rng.uniform(0, tw)
        p.line([(x, wy0), (x + rng.uniform(-10, 10) * s, wy0 + 20 * s), (x + rng.uniform(-14, 14) * s, wy1)], (70, 70, 64, 255), 1.5 * s)
    py0, py1 = wy1, r0 - 8 * s                                           # le trottoir blanc carrelé
    p.poly([(0, py0), (tw, py0), (tw, py1), (0, py1)], (206, 210, 202, 255))
    for k in range(int(tw / (28 * s)) + 1):
        for j in range(int((py1 - py0) / (18 * s)) + 1):
            if rng.random() < 0.12:
                x, y = k * 28 * s, py0 + j * 18 * s
                p.poly([(x, y), (x + 28 * s, y), (x + 28 * s, min(py1, y + 18 * s)), (x, min(py1, y + 18 * s))],
                       rng.choice(((186, 190, 182, 255), (176, 178, 170, 255), (218, 220, 214, 255))))
    y = py0
    while y < py1:
        p.line([(0, y), (tw, y)], (164, 168, 160, 255), 1.2 * s)
        y += 18 * s
    for k in range(int(tw / (28 * s)) + 1):
        p.line([(k * 28 * s, py0), (k * 28 * s, py1)], (164, 168, 160, 255), 1.2 * s)
    for k in range(int(tw / (300 * s))):                                 # les lampadaires et leur ombre
        x = k * 300 * s + 120 * s
        p.line([(x, py1 - 10 * s), (x + 60 * s, py1 - 40 * s)], (160, 164, 156, 255), 6 * s)
        p.line([(x, py1 - 10 * s), (x, py1 - 70 * s)], (40, 42, 46, 255), 6 * s)
        p.disc(x, py1 - 10 * s, 7 * s, (50, 52, 56, 255))
        p.ellipse(x - 14 * s, py1 - 82 * s, x + 14 * s, py1 - 66 * s, (230, 230, 200, 255), (40, 42, 46, 255), 2 * s)
    p.poly([(0, py1), (tw, py1), (tw, r0), (0, r0)], (128, 130, 124, 255))                    # la bordure
    p.poly([(0, r0), (tw, r0), (tw, r1), (0, r1)], (98, 104, 98, 255))                        # la route
    for _ in range(int(tw / (14 * s))):                                  # le grain de l'asphalte
        x, y = rng.uniform(0, tw), rng.uniform(r0, r1)
        r = rng.uniform(8, 30) * s
        p.ellipse(x - r, y - r * 0.5, x + r, y + r * 0.5, rng.choice(((92, 98, 92, 255), (104, 110, 104, 255), (94, 99, 94, 255))))
    mid = (r0 + r1) / 2
    p.line([(0, mid - 4 * s), (tw, mid - 4 * s)], (220, 190, 40, 255), 4 * s)                 # la ligne jaune
    p.line([(0, mid + 4 * s), (tw, mid + 4 * s)], (220, 190, 40, 255), 4 * s)
    for ly in (r0 + (mid - r0) / 2, mid + (r1 - mid) / 2):              # les pointillés blancs
        x = 0
        while x < tw:
            p.line([(x, ly), (x + 70 * s, ly)], (220, 222, 214, 255), 4 * s)
            x += 150 * s
    for _ in range(int(tw / (60 * s))):                                  # les fissures
        x, y = rng.uniform(0, tw), rng.uniform(r0, r1)
        pts = [(x, y)]
        for _i in range(rng.randint(3, 6)):
            x += rng.uniform(-24, 24) * s
            y += rng.uniform(-14, 14) * s
            pts.append((x, min(r1, max(r0, y))))
        p.line(pts, (54, 58, 54, 255), rng.uniform(1.2, 2.4) * s)
    for _ in range(int(tw / (220 * s))):                                 # flaques d'huile et trous
        x, y = rng.uniform(0, tw), rng.uniform(r0 + 20 * s, r1 - 20 * s)
        p.ellipse(x - 26 * s, y - 10 * s, x + 26 * s, y + 10 * s, (74, 78, 76, 255))
    for k in range(int(tw / (700 * s))):                                 # voitures brûlées au bord de la route
        x = k * 700 * s + rng.uniform(100, 400) * s
        y = rng.choice((r0 + 8 * s, r1 - 60 * s))
        _wreck(p, x, y, 100 * s, 50 * s, s, rng)
    p.poly([(0, r1), (tw, r1), (tw, r1 + 8 * s), (0, r1 + 8 * s)], (128, 130, 124, 255))      # bordure et trottoir du bas
    p.poly([(0, r1 + 8 * s), (tw, r1 + 8 * s), (tw, H), (0, H)], (200, 204, 196, 255))
    y = r1 + 8 * s
    while y < H:
        p.line([(0, y), (tw, y)], (164, 168, 160, 255), 1.2 * s)
        y += 18 * s
    for k in range(int(tw / (28 * s)) + 1):
        p.line([(k * 28 * s, r1 + 8 * s), (k * 28 * s, H)], (164, 168, 160, 255), 1.2 * s)
    img = p.done().convert("RGB")
    return {"sky": Image.new("RGB", (W, H), (98, 104, 98)), "layers": [{"img": img, "y": 0, "f": 1.0, "stage": "mid"}], "tw": tw, "amb": {}}


hd_bg.BUILDERS.update({"nam_city": build_nam_city, "nam_jungle": build_nam_jungle})
hd_bg.BUILDERS.update({"ra_town": build_ra_town, "bf_street": build_bf_street})
hd_bg.BUILDERS.update({"zb_valley": build_zb_valley, "pi_sea": build_pi_sea})
hd_bg.BUILDERS.update({"vp_floor": build_vp_floor})
hd_bg.BUILDERS.update({"gp_world": build_gp_world, "am_fortress": build_am_fortress})
hd_bg.BUILDERS.update({"cl_city": build_cl_city})
hd_bg.BUILDERS.update({"st2_street": build_st2_street})
