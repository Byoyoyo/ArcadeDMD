"""HD backdrops of the sixth batch of Neo Geo games done one by one (1.22), each drawn after screenshots of its game.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported.

Décors HD du sixième lot (1.22), chacun dessiné d'après des captures de son jeu. Tout est dessiné par le programme,
aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image, ImageDraw

from . import hd_bg
from .hd_bg import mix, vgrad
from .hd_themes3 import _Pic, _clump, _rgba
from .hd_themes5 import BRAWL_FLOOR

MD_FIELDS = (70, 1514)          # left edge of the two Magical Drop fields at s = 1 (W = 1920) / bord gauche des champs
NCM_ROAD = (196, 412)           # top and bottom of the path of Ninja Commando / haut et bas du chemin
BJ_FLOOR = 336                  # top of the grass of Blue's Journey / haut de l'herbe


def _windows(p, x, y0, w, h, s, rng, lit=(255, 214, 120), dark=(40, 44, 60), step=(16, 20), p_lit=0.2):
    """A grid of windows on a facade. / Une grille de fenêtres sur une façade."""
    sx, sy = step[0] * s, step[1] * s
    yy = y0 + 6 * s
    while yy < y0 + h - sy * 0.6:
        xx = x + 5 * s
        while xx < x + w - sx * 0.6:
            col = lit if rng.random() < p_lit else dark
            p.poly([(xx, yy), (xx + sx * 0.6, yy), (xx + sx * 0.6, yy + sy * 0.55), (xx, yy + sy * 0.55)], _rgba(col))
            xx += sx
        yy += sy


# ---------------------------------------------------------------------------- Mutation Nation
def build_mn_city(W, H, s, seed=101):
    """Mutation Nation: the ruined city, as in the game: blue towers under a violet sky, old stone buildings with
    broken windows on both sides of the street, piles of rubble, a wrecked car, the cracked concrete road.
    / La ville en ruine, comme dans le jeu : tours bleues, vieux immeubles aux vitres cassées, gravats, épave."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (70, 70, 150)), (0.5, (110, 110, 190)), (1.0, (150, 140, 200))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    x = -10 * s
    while x < tw:                                                        # les tours bleues au loin
        w = rng.uniform(50, 110) * s
        h = rng.uniform(150, 260) * s
        base = 250 * s
        col = rng.choice(((80, 90, 170), (96, 104, 186), (70, 76, 150), (110, 110, 196)))
        far.poly([(x, base), (x, base - h), (x + w, base - h), (x + w, base)], _rgba(col))
        for k in range(int(w / (9 * s))):                                # bandes verticales des vitres
            far.line([(x + 4 * s + k * 9 * s, base - h + 6 * s), (x + 4 * s + k * 9 * s, base)], _rgba(mix(col, (190, 200, 255), 0.3)), 2 * s)
        if rng.random() < 0.4:
            far.line([(x + w / 2, base - h), (x + w / 2, base - h - 30 * s)], (60, 60, 110, 255), 3 * s)
        x += w + rng.uniform(0, 30) * s
    layers.append({"img": far.done(), "y": 0, "f": 0.15, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    x = -20 * s
    while x < tw:                                                        # les vieux immeubles de pierre
        w = rng.uniform(150, 260) * s
        h = rng.uniform(170, 280) * s
        base = (BRAWL_FLOOR + 8) * s
        col = rng.choice(((178, 168, 150), (160, 150, 136), (190, 180, 160), (140, 134, 126)))
        top = base - h
        mid.poly([(x, base), (x, top), (x + w, top), (x + w, base)], _rgba(col), (60, 56, 52, 255), 2 * s)
        mid.poly([(x - 4 * s, top - 8 * s), (x + w + 4 * s, top - 8 * s), (x + w + 4 * s, top + 4 * s), (x - 4 * s, top + 4 * s)],
                 _rgba(mix(col, (0, 0, 0), 0.25)))                       # la corniche
        _windows(mid, x + 6 * s, top + 12 * s, w - 12 * s, h - 40 * s, s, rng, lit=(150, 170, 210), dark=(56, 60, 76), step=(30, 36), p_lit=0.35)
        for _ in range(3):                                               # des trous dans la façade
            cx, cy = x + rng.uniform(0.15, 0.85) * w, top + rng.uniform(0.2, 0.7) * h
            r = rng.uniform(8, 18) * s
            mid.poly([(cx - r, cy), (cx - r * 0.3, cy - r * 0.8), (cx + r, cy - r * 0.3), (cx + r * 0.6, cy + r * 0.7), (cx - r * 0.5, cy + r * 0.6)],
                     (50, 46, 46, 255))
        x += w + rng.uniform(60, 200) * s
    for _ in range(int(tw / (160 * s))):                                 # les tas de gravats
        x = rng.uniform(0, tw)
        y = (BRAWL_FLOOR + 6) * s
        for _i in range(9):
            r = rng.uniform(6, 16) * s
            cx = x + rng.uniform(-40, 40) * s
            cy = y - rng.uniform(0, 26) * s
            mid.poly([(cx - r, cy), (cx - r * 0.2, cy - r), (cx + r, cy - r * 0.4), (cx + r * 0.6, cy + r * 0.4)],
                     rng.choice(((150, 140, 124, 255), (120, 112, 100, 255), (176, 168, 150, 255))), (60, 56, 50, 255), 1 * s)
    layers.append({"img": mid.done(), "y": 0, "f": 0.5, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    gy = BRAWL_FLOOR * s
    near.poly([(0, gy), (tw, gy), (tw, H), (0, H)], (146, 144, 138, 255))              # la route de béton
    near.poly([(0, gy), (tw, gy), (tw, gy + 8 * s), (0, gy + 8 * s)], (110, 108, 104, 255))
    for _ in range(int(tw / (20 * s))):
        x, y = rng.uniform(0, tw), rng.uniform(gy + 10 * s, H)
        r = rng.uniform(10, 40) * s
        near.ellipse(x - r, y - r * 0.3, x + r, y + r * 0.3, rng.choice(((138, 136, 130, 255), (154, 152, 146, 255), (130, 128, 122, 255))))
    for _ in range(int(tw / (50 * s))):                                  # les fissures
        x, y = rng.uniform(0, tw), rng.uniform(gy + 12 * s, H)
        pts = [(x, y)]
        for _i in range(rng.randint(3, 6)):
            x += rng.uniform(-30, 30) * s
            y += rng.uniform(-8, 8) * s
            pts.append((x, max(gy + 10 * s, min(H, y))))
        near.line(pts, (84, 82, 80, 255), rng.uniform(1.5, 3) * s)
    for k in range(2):                                                   # l'épave d'une voiture
        x = tw * (0.3 + 0.5 * k)
        y = gy - 20 * s
        near.poly([(x, y + 60 * s), (x + 20 * s, y + 10 * s), (x + 90 * s, y - 10 * s), (x + 170 * s, y), (x + 210 * s, y + 40 * s),
                   (x + 210 * s, y + 66 * s), (x, y + 66 * s)], (110, 100, 140, 255), (40, 36, 54, 255), 2.5 * s)
        near.poly([(x + 40 * s, y + 14 * s), (x + 90 * s, y), (x + 150 * s, y + 6 * s), (x + 160 * s, y + 34 * s), (x + 46 * s, y + 36 * s)],
                  (50, 50, 60, 255))
        for wx in (x + 40 * s, x + 170 * s):
            near.disc(wx, y + 66 * s, 16 * s, (30, 30, 34, 255))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": layers, "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Sengoku
def _castle(p, cx, base, s, rng):
    """A castle tower of three roofs. / Un donjon à trois toits."""
    for k, (w, h) in enumerate(((120, 44), (90, 38), (60, 34))):
        y1 = base - sum(hh for _ww, hh in ((120, 44), (90, 38), (60, 34))[:k]) * s
        y0 = y1 - h * s
        p.poly([(cx - w / 2 * s, y1), (cx - w / 2 * s, y0 + 14 * s), (cx + w / 2 * s, y0 + 14 * s), (cx + w / 2 * s, y1)], (226, 226, 220, 255),
               (60, 60, 70, 255), 1.5 * s)
        p.poly([(cx - (w / 2 + 22) * s, y0 + 18 * s), (cx - (w / 2 - 6) * s, y0), (cx + (w / 2 - 6) * s, y0), (cx + (w / 2 + 22) * s, y0 + 18 * s)],
               (40, 70, 70, 255), (20, 30, 34, 255), 1.5 * s)
        for i in range(int(w / 20)):
            xx = cx - w / 2 * s + (10 + i * 20) * s
            p.poly([(xx - 4 * s, y1 - 18 * s), (xx + 4 * s, y1 - 18 * s), (xx + 4 * s, y1 - 8 * s), (xx - 4 * s, y1 - 8 * s)], (40, 40, 50, 255))


def build_sg1_field(W, H, s, seed=111):
    """Sengoku: the end of the world at sunset, as in the game: a blood-red and orange sky, a floating island with its
    castle, the dark violet ruins and banners of a village, the golden field and the grey mist on the ground.
    / Le crépuscule rouge et orange, une île flottante et son château, le village en ruine, le champ doré, la brume."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (90, 14, 8)), (0.3, (190, 50, 16)), (0.55, (240, 110, 30)), (0.66, (250, 150, 50)), (1.0, (200, 120, 60))])
    d = ImageDraw.Draw(sky)
    mx, my, mr = W * 0.78, H * 0.16, 30 * s                              # la lune rousse
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(150, 70, 40))
    d.ellipse([mx - mr * 0.6, my - mr * 0.5, mx - mr * 0.1, my], fill=(170, 86, 50))
    layers = []
    isl = _Pic(tw, H, 2, tw)
    for cx in (tw * 0.22, tw * 0.72):                                    # l'île flottante et son château
        top = 120 * s
        pts = [(cx - 150 * s, top)]
        for i in range(1, 12):
            pts.append((cx - 150 * s + i * 300 * s / 12, top + rng.uniform(40, 120) * s * math.sin(i / 12 * math.pi) + 10 * s))
        pts.append((cx + 150 * s, top))
        isl.poly(pts, (70, 50, 40, 255), (30, 20, 16, 255), 2 * s)
        isl.poly([(cx - 150 * s, top), (cx + 150 * s, top), (cx + 130 * s, top + 16 * s), (cx - 130 * s, top + 16 * s)], (60, 90, 50, 255))
        for _ in range(6):
            _clump(isl, cx + rng.uniform(-120, 120) * s, top + 6 * s, rng.uniform(12, 20) * s, rng, ((30, 60, 30), (50, 90, 40)), n=4)
        _castle(isl, cx, top + 4 * s, s * 0.6, rng)
        for _ in range(5):                                               # une lueur bleue autour du château
            gx, gy = cx + rng.uniform(-60, 60) * s, top - rng.uniform(10, 60) * s
            isl.line([(gx, gy), (gx + rng.uniform(-8, 8) * s, gy - 30 * s)], (140, 200, 255, 255), 2 * s)
    layers.append({"img": isl.done(), "y": 0, "f": 0.04, "stage": "far"})
    vil = _Pic(tw, H, 2, tw)
    x = 0
    base = 236 * s
    while x < tw:                                                        # le village en ruine, en ombres violettes
        w = rng.uniform(20, 60) * s
        h = rng.uniform(12, 40) * s
        vil.poly([(x, base), (x, base - h), (x + w / 2, base - h - 10 * s), (x + w, base - h), (x + w, base)], (110, 60, 110, 255))
        if rng.random() < 0.35:                                          # bannières
            px = x + w / 2
            vil.line([(px, base - h), (px, base - h - 50 * s)], (80, 40, 80, 255), 2 * s)
            vil.poly([(px, base - h - 50 * s), (px + 18 * s, base - h - 48 * s), (px + 18 * s, base - h - 20 * s), (px, base - h - 22 * s)],
                     (130, 70, 120, 255))
        x += w + rng.uniform(0, 20) * s
    layers.append({"img": vil.done(), "y": 0, "f": 0.25, "stage": "far"})
    fld = _Pic(tw, H, 2, tw)
    y0, y1 = 232 * s, (BRAWL_FLOOR + 6) * s
    fld.poly([(0, y0), (tw, y0), (tw, y1), (0, y1)], (190, 150, 40, 255))              # le champ doré
    for _ in range(int(tw / (3 * s))):
        x = rng.uniform(0, tw)
        y = rng.uniform(y0, y1)
        fld.line([(x, y), (x + rng.uniform(-3, 3) * s, y - rng.uniform(8, 22) * s)],
                 rng.choice(((240, 200, 70, 255), (160, 110, 30, 255), (220, 170, 50, 255))), 1.5 * s)
    layers.append({"img": fld.done(), "y": 0, "f": 0.6, "stage": "mid"})
    mist = _Pic(tw, H, 2, tw)
    gy = BRAWL_FLOOR * s
    mist.poly([(0, gy), (tw, gy), (tw, H), (0, H)], (196, 194, 210, 255))              # la brume grise
    for _ in range(int(tw / (12 * s))):
        x, y = rng.uniform(0, tw), rng.uniform(gy, H)
        r = rng.uniform(20, 70) * s
        mist.ellipse(x - r, y - r * 0.18, x + r, y + r * 0.18, rng.choice(((214, 212, 226, 255), (180, 178, 196, 255), (206, 204, 218, 255))))
    layers.append({"img": mist.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": layers, "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Sengoku 2
def build_sg2_bridge(W, H, s, seed=121):
    """Sengoku 2: under the great wooden bridge at dusk, as in the game: a violet and orange sky, dark mountains, the
    roofs of a village in the mist, the huge arch of the bridge on its stone pier, the sand and its stones.
    / Sous le grand pont de bois au crépuscule, comme dans le jeu : montagnes, village dans la brume, l'arche, le sable."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (70, 64, 130)), (0.35, (150, 110, 160)), (0.55, (240, 170, 130)), (1.0, (220, 190, 170))])
    layers = []
    mnt = _Pic(tw, H, 2, tw)
    for k, (col, base, amp) in enumerate((((90, 80, 120), 230, 80), ((60, 70, 90), 250, 60))):
        pts = [(0, H)]
        for i in range(0, 41):
            x = tw * i / 40
            pts.append((x, (base - amp * (0.5 + 0.5 * math.sin(i * 1.3 + k * 2) * math.cos(i * 0.4))) * s))
        pts.append((tw, H))
        mnt.poly(pts, _rgba(col))
    layers.append({"img": mnt.done(), "y": 0, "f": 0.1, "stage": "far"})
    vil = _Pic(tw, H, 2, tw)
    for _ in range(int(tw / (220 * s))):                                 # les toits du village dans la brume
        x = rng.uniform(0, tw)
        y = rng.uniform(236, 250) * s
        w = rng.uniform(40, 70) * s
        vil.poly([(x, y), (x + w, y), (x + w, y + 14 * s), (x, y + 14 * s)], (200, 180, 170, 255))
        vil.poly([(x - 10 * s, y + 2 * s), (x + w / 2, y - 16 * s), (x + w + 10 * s, y + 2 * s)], (160, 60, 50, 255))
    for _ in range(int(tw / (30 * s))):                                  # la brume
        x, y = rng.uniform(0, tw), rng.uniform(250, 290) * s
        r = rng.uniform(40, 100) * s
        vil.ellipse(x - r, y - r * 0.2, x + r, y + r * 0.2, rng.choice(((236, 226, 236, 255), (220, 210, 226, 255), (244, 236, 240, 255))))
    layers.append({"img": vil.done(), "y": 0, "f": 0.3, "stage": "far"})
    br = _Pic(tw, H, 2, tw)
    for k in range(2):                                                   # l'arche du pont sur sa pile de pierre
        x0 = tw * (0.08 + 0.5 * k)
        span = 900 * s
        top_y = -60 * s
        pts_o, pts_i = [], []
        for i in range(31):
            t = i / 30
            x = x0 + span * t
            y = 250 * s - (250 * s - top_y) * math.sin(t * math.pi)
            pts_o.append((x, y))
            pts_i.append((x, y + 70 * s))
        br.poly(pts_o + pts_i[::-1], (90, 60, 40, 255), (40, 26, 18, 255), 2 * s)
        for i in range(0, 31, 2):
            br.line([pts_o[i], pts_i[i]], (60, 40, 26, 255), 2.5 * s)
        for i in range(1, 30, 3):                                        # les poutres sous l'arche
            br.line([pts_i[i], (pts_i[i][0], pts_i[i][1] + 30 * s)], (70, 46, 30, 255), 4 * s)
        px = x0 + span                                                   # la pile de pierre
        br.poly([(px - 70 * s, 210 * s), (px + 70 * s, 210 * s), (px + 90 * s, 296 * s), (px - 90 * s, 296 * s)], (200, 186, 150, 255),
                (110, 96, 70, 255), 2 * s)
        for r in range(4):
            yy = 210 * s + r * 22 * s
            br.line([(px - 75 * s - r * 5 * s, yy), (px + 75 * s + r * 5 * s, yy)], (150, 136, 104, 255), 2 * s)
    layers.append({"img": br.done(), "y": 0, "f": 0.5, "stage": "mid"})
    gnd = _Pic(tw, H, 2, tw)
    gy = BRAWL_FLOOR * s
    gnd.poly([(0, gy - 6 * s), (tw, gy - 6 * s), (tw, H), (0, H)], (224, 206, 176, 255))   # le sable
    for _ in range(int(tw / (14 * s))):
        x, y = rng.uniform(0, tw), rng.uniform(gy, H)
        r = rng.uniform(10, 40) * s
        gnd.ellipse(x - r, y - r * 0.25, x + r, y + r * 0.25, rng.choice(((214, 196, 166, 255), (232, 216, 188, 255))))
    for _ in range(int(tw / (90 * s))):                                  # les pierres
        x, y = rng.uniform(0, tw), rng.uniform(gy + 10 * s, H)
        r = rng.uniform(6, 16) * s
        gnd.poly([(x - r, y), (x - r * 0.4, y - r * 0.8), (x + r * 0.7, y - r * 0.6), (x + r, y + r * 0.2), (x, y + r * 0.4)], (150, 150, 150, 255),
                 (90, 90, 96, 255), 1 * s)
    layers.append({"img": gnd.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": layers, "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Ninja Combat
def build_nc_park(W, H, s, seed=131):
    """Ninja Combat: a park at night, as in the game: a deep blue sky, dark trees, lamp posts with white globes, a gate
    of gold and blue pillars under its roof, the fence and the grey paving stones.
    / Un parc la nuit, comme dans le jeu : arbres sombres, lampadaires, portique aux piliers or et bleu, pavés gris."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (8, 14, 50)), (0.5, (30, 46, 110)), (1.0, (40, 60, 120))])
    layers = []
    trees = _Pic(tw, H, 2, tw)
    for _ in range(int(tw / (28 * s))):                                  # les arbres sombres
        _clump(trees, rng.uniform(0, tw), rng.uniform(90, 200) * s, rng.uniform(40, 80) * s, rng, ((14, 40, 24), (24, 64, 34), (40, 90, 46)), n=7)
    trees.poly([(0, 200 * s), (tw, 200 * s), (tw, 250 * s), (0, 250 * s)], (14, 40, 24, 255))
    layers.append({"img": trees.done(), "y": 0, "f": 0.3, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    lights = []
    for k in range(int(tw / (340 * s))):                                 # les lampadaires
        x = k * 340 * s + 170 * s
        mid.line([(x, 250 * s), (x, 120 * s)], (40, 50, 60, 255), 5 * s)
        mid.disc(x, 112 * s, 12 * s, (240, 246, 255, 255), (60, 70, 80, 255), 1.5 * s)
        lights.append((x, 112 * s))
    for gx in (tw * 0.15, tw * 0.65):                                    # le portique aux piliers or et bleu
        for px in (gx, gx + 360 * s):
            for i in range(6):
                col = (230, 190, 60, 255) if i % 2 == 0 else (70, 90, 200, 255)
                mid.poly([(px - 28 * s, 100 * s + i * 30 * s), (px + 28 * s, 100 * s + i * 30 * s), (px + 28 * s, 130 * s + i * 30 * s),
                          (px - 28 * s, 130 * s + i * 30 * s)], col, (40, 30, 20, 255), 1.5 * s)
        mid.poly([(gx - 70 * s, 100 * s), (gx + 430 * s, 100 * s), (gx + 400 * s, 70 * s), (gx - 40 * s, 70 * s)], (160, 40, 40, 255),
                 (60, 20, 20, 255), 2 * s)
        mid.poly([(gx - 50 * s, 70 * s), (gx + 410 * s, 70 * s), (gx + 380 * s, 48 * s), (gx - 20 * s, 48 * s)], (40, 110, 70, 255),
                 (20, 40, 30, 255), 2 * s)
        for i in range(10):
            mid.disc(gx - 20 * s + i * 44 * s, 60 * s, 4 * s, (250, 210, 80, 255))
        mid.poly([(gx + 30 * s, 280 * s), (gx + 330 * s, 280 * s), (gx + 330 * s, 286 * s), (gx + 30 * s, 286 * s)], (110, 110, 120, 255))
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid", "lights": lights})
    near = _Pic(tw, H, 2, tw)
    gy = BRAWL_FLOOR * s
    near.poly([(0, 240 * s), (tw, 240 * s), (tw, gy), (0, gy)], (24, 30, 34, 255))           # la grille du parc
    for k in range(int(tw / (14 * s))):
        x = k * 14 * s
        near.line([(x, 236 * s), (x, gy)], (120, 90, 50, 255), 2.5 * s)
    near.line([(0, 244 * s), (tw, 244 * s)], (140, 104, 60, 255), 4 * s)
    near.line([(0, 276 * s), (tw, 276 * s)], (140, 104, 60, 255), 4 * s)
    near.poly([(0, gy), (tw, gy), (tw, H), (0, H)], (88, 98, 100, 255))                     # les pavés gris
    y = gy
    row = 0
    while y < H:
        near.line([(0, y), (tw, y)], (60, 68, 70, 255), 2 * s)
        x = (row % 2) * 24 * s
        while x < tw:
            near.line([(x, y), (x, y + 20 * s)], (60, 68, 70, 255), 2 * s)
            x += 48 * s
        y += 20 * s
        row += 1
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": layers, "tw": tw, "amb": {"window": (230, 240, 255)}}


# ---------------------------------------------------------------------------- Ninja Commando
def build_ncm_jungle(W, H, s, seed=141):
    """Ninja Commando: the jungle seen from above, as in the game: a winding dirt path between thick green bushes,
    purple boulders, a river crossed by a wooden bridge. / La jungle vue du dessus : chemin de terre, rochers, rivière."""
    rng = random.Random(seed)
    tw = 2 * W
    r0, r1 = NCM_ROAD[0] * s, NCM_ROAD[1] * s
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (40, 96, 40, 255))                          # la jungle
    for _ in range(int(tw / (10 * s))):
        _clump(p, rng.uniform(0, tw), rng.choice((rng.uniform(0, r0), rng.uniform(r1, H))), rng.uniform(16, 36) * s, rng,
               ((24, 70, 30), (44, 120, 44), (90, 170, 70)), n=5)
    top, bot = [], []
    for i in range(81):                                                  # le chemin qui serpente
        x = tw * i / 80
        w = math.sin(i / 80 * math.tau * 3) * 18 * s
        top.append((x, r0 + w + rng.uniform(-4, 4) * s))
        bot.append((x, r1 + w + rng.uniform(-4, 4) * s))
    p.poly(top + bot[::-1], (196, 140, 76, 255))
    for _ in range(int(tw / (8 * s))):
        x, y = rng.uniform(0, tw), rng.uniform(r0 + 10 * s, r1 - 10 * s)
        r = rng.uniform(4, 16) * s
        p.ellipse(x - r, y - r * 0.5, x + r, y + r * 0.5, rng.choice(((180, 124, 64, 255), (210, 156, 90, 255), (170, 116, 60, 255))))
    for _ in range(int(tw / (120 * s))):                                 # les rochers violets
        x = rng.uniform(0, tw)
        y = rng.choice((r0 + rng.uniform(-10, 20) * s, r1 + rng.uniform(-20, 10) * s))
        r = rng.uniform(16, 30) * s
        p.ellipse(x - r + 6 * s, y - r * 0.6 + 8 * s, x + r + 6 * s, y + r * 0.6 + 8 * s, (30, 60, 30, 255))
        p.ellipse(x - r, y - r * 0.7, x + r, y + r * 0.7, (120, 110, 150, 255), (50, 44, 70, 255), 1.5 * s)
        p.ellipse(x - r * 0.6, y - r * 0.6, x + r * 0.1, y - r * 0.1, (170, 160, 200, 255))
    for k in range(2):                                                   # la rivière et son pont de bois
        x = tw * (0.35 + 0.5 * k)
        pts_l = [(x + math.sin(i / 10 * 3) * 16 * s, H * i / 10) for i in range(11)]
        pts_r = [(px + 110 * s, py) for px, py in pts_l]
        p.poly(pts_l + pts_r[::-1], (50, 100, 150, 255))
        for i in range(10):
            yy = H * (i + 0.5) / 10
            p.line([(x + 20 * s, yy), (x + 60 * s, yy)], (120, 170, 220, 255), 2 * s)
        p.poly([(x - 20 * s, r0 + 20 * s), (x + 130 * s, r0 + 20 * s), (x + 130 * s, r1 - 20 * s), (x - 20 * s, r1 - 20 * s)], (140, 96, 50, 255),
               (70, 44, 20, 255), 2 * s)
        yy = r0 + 20 * s
        while yy < r1 - 20 * s:
            p.line([(x - 20 * s, yy), (x + 130 * s, yy)], (90, 60, 30, 255), 2 * s)
            yy += 14 * s
    img = p.done().convert("RGB")
    return {"sky": Image.new("RGB", (W, H), (40, 96, 40)), "layers": [{"img": img, "y": 0, "f": 1.0, "stage": "mid"}], "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Blue's Journey
def build_bj_jungle(W, H, s, seed=151):
    """Blue's Journey: the land of giant plants, as in the game: long green leaves striped with yellow hang from the
    top, a blue tree, red leaves, a huge clay pot, pink buds, the grass and its tufts over the golden soil.
    / Le pays des plantes géantes : longues feuilles rayées de jaune, arbre bleu, grand pot de terre, herbe et terre dorée."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (18, 70, 30)), (0.6, (40, 110, 50)), (1.0, (60, 130, 60))])
    layers = []
    back = _Pic(tw, H, 2, tw)
    for _ in range(int(tw / (60 * s))):                                  # les grandes plantes au fond
        _clump(back, rng.uniform(0, tw), rng.uniform(140, 300) * s, rng.uniform(50, 100) * s, rng, ((30, 90, 40), (50, 120, 50), (80, 150, 60)), n=6)
    for k in range(3):                                                   # l'arbre bleu et les feuilles rouges
        x = tw * (0.1 + 0.33 * k)
        _clump(back, x, 170 * s, 110 * s, rng, ((20, 80, 110), (40, 130, 160), (90, 190, 210)), n=10)
        for i in range(5):
            a = -math.pi * (0.15 + 0.7 * i / 4)
            cx, cy = x + 260 * s + math.cos(a) * 90 * s, 280 * s + math.sin(a) * 60 * s
            back.poly([(x + 260 * s, 290 * s), (cx - 40 * s, cy), (cx, cy - 30 * s), (cx + 40 * s, cy)], (210, 50, 70, 255), (120, 20, 40, 255), 2 * s)
    for k in range(2):                                                   # le grand pot de terre
        x = tw * (0.25 + 0.5 * k)
        y = BJ_FLOOR * s
        back.poly([(x - 120 * s, y), (x - 140 * s, y - 90 * s), (x - 150 * s, y - 120 * s), (x + 150 * s, y - 120 * s), (x + 140 * s, y - 90 * s),
                   (x + 120 * s, y)], (210, 140, 50, 255), (110, 66, 20, 255), 3 * s)
        back.ellipse(x - 150 * s, y - 140 * s, x + 150 * s, y - 100 * s, (220, 160, 60, 255), (110, 66, 20, 255), 3 * s)
        back.ellipse(x - 120 * s, y - 134 * s, x + 120 * s, y - 106 * s, (40, 24, 10, 255))
        back.line([(x - 140 * s, y - 70 * s), (x + 140 * s, y - 70 * s)], (170, 100, 30, 255), 4 * s)
    for _ in range(int(tw / (200 * s))):                                 # les boutons roses
        x = rng.uniform(0, tw)
        back.ellipse(x - 14 * s, (BJ_FLOOR - 40) * s, x + 14 * s, (BJ_FLOOR - 10) * s, (240, 150, 190, 255), (150, 60, 100, 255), 1.5 * s)
        back.line([(x, (BJ_FLOOR - 10) * s), (x, BJ_FLOOR * s)], (40, 120, 40, 255), 3 * s)
    layers.append({"img": back.done(), "y": 0, "f": 0.4, "stage": "mid"})
    top = _Pic(tw, H, 2, tw)
    for _ in range(int(tw / (36 * s))):                                  # les longues feuilles qui pendent du haut
        x = rng.uniform(0, tw)
        ln = rng.uniform(80, 160) * s
        bend = rng.uniform(-60, 60) * s
        pts_l = [(x + bend * (i / 8) ** 2 - 14 * s * math.sin(i / 8 * math.pi), ln * i / 8) for i in range(9)]
        pts_r = [(px + 28 * s * math.sin(i / 8 * math.pi), py) for i, (px, py) in enumerate(pts_l)]
        top.poly(pts_l + pts_r[::-1], (40, 140, 60, 255), (20, 70, 30, 255), 1.5 * s)
        top.line(pts_r, (230, 210, 60, 255), 3 * s)
    layers.append({"img": top.done(), "y": 0, "f": 0.7, "stage": "near"})
    gnd = _Pic(tw, H, 2, tw)
    gy = BJ_FLOOR * s
    gnd.poly([(0, gy + 10 * s), (tw, gy + 10 * s), (tw, H), (0, H)], (150, 100, 30, 255))   # la terre dorée et son quadrillage
    k = 0
    while k * 16 * s < tw + H:
        x = k * 16 * s
        gnd.line([(x, gy + 10 * s), (x - (H - gy), H)], (210, 160, 50, 255), 2 * s)
        gnd.line([(x - (H - gy), gy + 10 * s), (x, H)], (120, 76, 20, 255), 2 * s)
        k += 1
    gnd.poly([(0, gy - 4 * s), (tw, gy - 4 * s), (tw, gy + 16 * s), (0, gy + 16 * s)], (80, 190, 60, 255))
    for i in range(int(tw / (18 * s))):                                  # les touffes d'herbe
        x = i * 18 * s + rng.uniform(-4, 4) * s
        gnd.poly([(x - 10 * s, gy + 14 * s), (x, gy - 16 * s), (x + 10 * s, gy + 14 * s)], (60, 170, 50, 255), (30, 100, 30, 255), 1 * s)
    layers.append({"img": gnd.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": layers, "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Puzzle Bobble 2
def build_pb2_beach(W, H, s, seed=161):
    """Puzzle Bobble 2: the beach of the first rounds, as in the game: a deep blue sky with big white clouds, palm
    trees, the turquoise sea and a sailing boat, the white sand. / La plage : ciel bleu, gros nuages, palmiers, voilier."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (30, 80, 200)), (0.6, (80, 150, 230)), (1.0, (150, 200, 240))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(14):                                                  # les gros nuages
        cx, cy = rng.uniform(0, W), rng.uniform(20, 220) * s
        for _i in range(7):
            r = rng.uniform(26, 60) * s
            p.disc(cx + rng.uniform(-80, 80) * s, cy + rng.uniform(-20, 20) * s, r, (250, 252, 255, 255))
        p.ellipse(cx - 90 * s, cy + 10 * s, cx + 90 * s, cy + 40 * s, (220, 230, 245, 255))
    sea = 300 * s
    p.poly([(0, sea), (W, sea), (W, 370 * s), (0, 370 * s)], (40, 160, 190, 255))           # la mer
    for _ in range(40):
        x, y = rng.uniform(0, W), rng.uniform(sea + 6 * s, 366 * s)
        p.line([(x, y), (x + rng.uniform(20, 60) * s, y)], (150, 220, 240, 255), 2 * s)
    bx = W * 0.62                                                        # le voilier
    p.poly([(bx - 50 * s, 330 * s), (bx + 60 * s, 330 * s), (bx + 40 * s, 346 * s), (bx - 36 * s, 346 * s)], (250, 250, 250, 255), (90, 90, 100, 255), 1.5 * s)
    p.poly([(bx, 326 * s), (bx, 220 * s), (bx + 56 * s, 326 * s)], (250, 250, 250, 255), (120, 120, 130, 255), 1.5 * s)
    p.poly([(bx - 4 * s, 326 * s), (bx - 4 * s, 240 * s), (bx - 44 * s, 326 * s)], (240, 240, 244, 255), (120, 120, 130, 255), 1.5 * s)
    p.poly([(0, 370 * s), (W, 370 * s), (W, H), (0, H)], (240, 230, 200, 255))             # le sable
    for _ in range(80):
        x, y = rng.uniform(0, W), rng.uniform(372 * s, H)
        p.disc(x, y, rng.uniform(1, 3) * s, (220, 206, 170, 255))
    for px in (W * 0.03, W * 0.47, W * 0.95):                            # les palmiers
        base = 420 * s
        topx, topy = px + rng.uniform(-60, 60) * s, 130 * s
        pts = [(px + (topx - px) * t * t - 8 * s, base + (topy - base) * t) for t in [i / 10 for i in range(11)]]
        pts2 = [(x + 16 * s - 8 * s * i / 10, y) for i, (x, y) in enumerate(pts)]
        p.poly(pts + pts2[::-1], (150, 100, 50, 255), (80, 50, 20, 255), 1.5 * s)
        for i in range(8):
            a = math.tau * i / 8 + 0.3
            ex, ey = topx + math.cos(a) * 130 * s, topy + math.sin(a) * 50 * s + 40 * s
            p.poly([(topx, topy), (topx + (ex - topx) * 0.5 + 12 * s, topy + (ey - topy) * 0.5 - 22 * s), (ex, ey),
                    (topx + (ex - topx) * 0.5 - 6 * s, topy + (ey - topy) * 0.5 + 6 * s)], (50, 140, 50, 255), (20, 70, 24, 255), 1.5 * s)
    img = p.done()
    sky = sky.convert("RGBA")
    sky.alpha_composite(img)
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


# ---------------------------------------------------------------------------- Puzzle De Pon!
def build_pdp_stars(W, H, s, seed=171):
    """Puzzle De Pon!: the pale blue sky full of big soft stars, as in the game. / Le ciel bleu pâle plein d'étoiles."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (170, 206, 240)), (1.0, (190, 220, 246))])
    p = _Pic(W, H, 2, 4 * W)
    for row in range(5):
        for k in range(12):
            cx = (k + 0.5 * (row % 2)) * 170 * s
            cy = row * 110 * s + 30 * s
            r = 46 * s
            pts = []
            for i in range(10):
                a = -math.pi / 2 + i * math.pi / 5
                rr = r if i % 2 == 0 else r * 0.45
                pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
            p.poly(pts, (200, 226, 250, 255))
    for _ in range(300):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        p.disc(x, y, rng.uniform(1, 2.5) * s, (226, 240, 255, 255))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


# ---------------------------------------------------------------------------- Magical Drop II
def build_md2_bricks(W, H, s, seed=181):
    """Magical Drop II: the orange brick wall and the pale marble columns around the two fields, the fields of deep
    teal with soft patterns, as in the game. / Le mur de briques orange, les colonnes de marbre, les champs bleu-vert."""
    rng = random.Random(seed)
    sky = Image.new("RGB", (W, H), (230, 130, 40))
    p = _Pic(W, H, 2, 4 * W)
    y = 0
    row = 0
    while y < H:                                                         # les briques
        x = -(row % 2) * 30 * s
        while x < W:
            col = rng.choice(((236, 140, 50), (226, 128, 40), (244, 156, 66)))
            p.poly([(x + 2 * s, y + 2 * s), (x + 58 * s, y + 2 * s), (x + 58 * s, y + 22 * s), (x + 2 * s, y + 22 * s)], _rgba(col))
            x += 60 * s
        y += 24 * s
        row += 1
    fw = 48 * 7 * s
    for x0 in MD_FIELDS:
        fx0 = x0 * s if x0 < W / s / 2 else W - (W / s - x0) * s
        p.poly([(fx0 - 14 * s, 96 * s), (fx0 + fw + 14 * s, 96 * s), (fx0 + fw + 14 * s, H), (fx0 - 14 * s, H)], (70, 120, 140, 255),
               (30, 50, 60, 255), 3 * s)
        for _ in range(26):                                              # motifs doux en relief
            cx, cy = fx0 + rng.uniform(0, fw), rng.uniform(110, 440) * s
            r = rng.uniform(16, 40) * s
            p.ellipse(cx - r, cy - r * 0.5, cx + r, cy + r * 0.5, (86, 136, 156, 255))
            p.ellipse(cx - r * 0.6, cy - r * 0.3, cx + r * 0.6, cy + r * 0.3, (70, 120, 140, 255))
        for cx in (fx0 - 36 * s, fx0 + fw + 36 * s):                     # les colonnes de marbre
            p.poly([(cx - 22 * s, 120 * s), (cx + 22 * s, 120 * s), (cx + 22 * s, H), (cx - 22 * s, H)], (230, 236, 210, 255), (120, 130, 100, 255), 2 * s)
            for k in range(4):
                p.line([(cx - 14 * s + k * 9 * s, 130 * s), (cx - 14 * s + k * 9 * s, H)], (200, 210, 180, 255), 2 * s)
            p.poly([(cx - 32 * s, 96 * s), (cx + 32 * s, 96 * s), (cx + 26 * s, 124 * s), (cx - 26 * s, 124 * s)], (236, 240, 214, 255),
                   (120, 130, 100, 255), 2 * s)
            p.disc(cx - 20 * s, 108 * s, 8 * s, (220, 226, 196, 255), (120, 130, 100, 255), 1.5 * s)
            p.disc(cx + 20 * s, 108 * s, 8 * s, (220, 226, 196, 255), (120, 130, 100, 255), 1.5 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


# ---------------------------------------------------------------------------- Money Puzzle Exchanger
def build_mpe_pastel(W, H, s, seed=191):
    """Money Puzzle Exchanger: the pastel diamonds of blue, white and lilac, as in the game, the two fields framed in
    pink. / Les losanges pastel bleus, blancs et lilas, les deux champs encadrés de rose."""
    rng = random.Random(seed)
    sky = Image.new("RGB", (W, H), (190, 214, 246))
    p = _Pic(W, H, 2, 4 * W)
    dw, dh = 60 * s, 40 * s
    for row in range(int(H / dh) + 2):
        for k in range(int(W / dw) + 2):
            cx = k * dw + (row % 2) * dw / 2
            cy = row * dh / 2 * 2 - dh / 2
            col = rng.choice(((170, 200, 244), (226, 236, 252), (200, 190, 240), (160, 210, 240), (236, 210, 240)))
            p.poly([(cx, cy - dh / 2), (cx + dw / 2, cy), (cx, cy + dh / 2), (cx - dw / 2, cy)], _rgba(col))
    fw = 48 * 7 * s
    for x0 in MD_FIELDS:
        fx0 = x0 * s if x0 < W / s / 2 else W - (W / s - x0) * s
        p.poly([(fx0 - 14 * s, 96 * s), (fx0 + fw + 14 * s, 96 * s), (fx0 + fw + 14 * s, H), (fx0 - 14 * s, H)], (250, 120, 190, 255))
        p.poly([(fx0 - 6 * s, 104 * s), (fx0 + fw + 6 * s, 104 * s), (fx0 + fw + 6 * s, H), (fx0 - 6 * s, H)], (120, 140, 220, 255))
        for row in range(10):
            for k in range(7):
                cx, cy = fx0 + (k + 0.5) * 48 * s, (126 + row * 40) * s
                p.poly([(cx, cy - 16 * s), (cx + 22 * s, cy), (cx, cy + 16 * s), (cx - 22 * s, cy)], (134, 152, 228, 255))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


hd_bg.BUILDERS.update({"mn_city": build_mn_city, "sg1_field": build_sg1_field, "sg2_bridge": build_sg2_bridge, "nc_park": build_nc_park,
                       "ncm_jungle": build_ncm_jungle, "bj_jungle": build_bj_jungle, "pb2_beach": build_pb2_beach, "pdp_stars": build_pdp_stars,
                       "md2_bricks": build_md2_bricks, "mpe_pastel": build_mpe_pastel})
