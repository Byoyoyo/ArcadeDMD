"""HD backdrops of the seventh batch of Neo Geo games done one by one (1.23), each drawn after screenshots of its game.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported.

Décors HD du septième lot (1.23), chacun dessiné d'après des captures de son jeu. Tout est dessiné par le programme,
aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image

from . import hd_bg
from .hd_bg import mix, vgrad
from .hd_themes3 import _Pic, _rgba
from .hd_themes5 import BRAWL_FLOOR
from .hd_themes6 import build_pdp_stars

SM_FLOOR = 372                  # top of the sand of Spin Master / haut du sable
ZP_ROWS = ((140, ((260, 780), (1140, 1660))), (228, ((60, 640), (860, 1060), (1280, 1860))), (316, ((200, 860), (1060, 1720))),
           (404, ((0, 1920),)))                                   # Zupapa! platforms: (y, [(x0, x1)]) at s = 1 / plateformes
NMD = (180, 96, 40, 39, 9)       # Neo Mr. Do! field: x0, y0, cell, columns, rows at s = 1 / le champ : coin, case, colonnes, rangées


def build_pdpr_stars(W, H, s, seed=201):
    """Puzzle De Pon! R!: the same sky of big soft stars, in pink, as in the game. / Le même ciel étoilé, en rose."""
    raw = build_pdp_stars(W, H, s, seed)
    img = raw["sky"]
    r, g, b = img.split()
    raw["sky"] = Image.merge("RGB", (b.point(lambda v: min(255, v + 10)), g.point(lambda v: max(0, v - 6)), r.point(lambda v: min(255, v + 55))))
    return raw


def build_pbm_check(W, H, s, seed=211):
    """Panic Bomber: the green checkerboard behind the two fields, as in the game. / Le damier vert derrière les deux champs."""
    sky = Image.new("RGB", (W, H), (60, 170, 90))
    p = _Pic(W, H, 2, 4 * W)
    c = 40 * s
    for row in range(int(H / c) + 1):
        for k in range(int(W / c) + 1):
            if (row + k) % 2:
                p.poly([(k * c, row * c), (k * c + c, row * c), (k * c + c, row * c + c), (k * c, row * c + c)], (80, 196, 110, 255))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_pnb_jungle(W, H, s, seed=221):
    """Pop 'n Bounce: the jungle at dusk behind the fields, as in the game: a lilac sky, tall tree trunks and their
    carved tops, big ferns at the bottom. / La jungle au crépuscule : ciel lilas, grands troncs, fougères."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (110, 110, 180)), (0.5, (170, 150, 200)), (1.0, (200, 170, 190))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(14):                                                  # les troncs
        x = rng.uniform(0, W)
        w = rng.uniform(14, 30) * s
        top = rng.uniform(120, 220) * s
        p.poly([(x - w / 2, H), (x - w / 2, top), (x + w / 2, top), (x + w / 2, H)], (150, 100, 50, 255), (80, 50, 20, 255), 1.5 * s)
        p.ellipse(x - w * 0.7, top - w * 0.9, x + w * 0.7, top + w * 0.2, (200, 150, 70, 255), (80, 50, 20, 255), 1.5 * s)
    for _ in range(int(W / (30 * s))):                                   # les fougères
        x = rng.uniform(0, W)
        base = H + 10 * s
        for i in range(5):
            a = math.pi * (0.15 + 0.7 * i / 4)
            ex, ey = x - math.cos(a) * 120 * s, base - math.sin(a) * 150 * s
            p.poly([(x, base), (ex - 14 * s, ey), (ex + 14 * s, ey)], rng.choice(((40, 120, 40, 255), (60, 150, 50, 255), (30, 100, 40, 255))))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_sbp_swirl(W, H, s, seed=231):
    """Super Bubble Pop: the magenta swirl and its lilac bubbles around, as in the game. / Le tourbillon magenta et ses bulles."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (160, 20, 120)), (0.5, (230, 60, 170)), (1.0, (150, 20, 110))])
    p = _Pic(W, H, 2, 4 * W)
    cx, cy = W / 2, H / 2
    for k in range(60):                                                  # le tourbillon
        a = k * 0.35
        r = 20 * s + k * 16 * s
        p.ellipse(cx + math.cos(a) * r - 40 * s, cy + math.sin(a) * r * 0.4 - 12 * s, cx + math.cos(a) * r + 40 * s, cy + math.sin(a) * r * 0.4 + 12 * s,
                  (250, 120, 210, 255) if k % 2 else (200, 40, 150, 255))
    for _ in range(140):                                                 # les bulles lilas du bord
        x = rng.choice((rng.uniform(0, 260 * s), rng.uniform(W - 260 * s, W), rng.uniform(0, W)))
        y = rng.uniform(0, H) if x < 260 * s or x > W - 260 * s else rng.choice((rng.uniform(0, 40 * s), rng.uniform(H - 40 * s, H)))
        r = rng.uniform(10, 34) * s
        p.disc(x, y, r, (200, 180, 230, 255), (120, 100, 160, 255), 1.5 * s)
        p.disc(x - r * 0.35, y - r * 0.35, r * 0.25, (250, 246, 255, 255))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_sm_desert(W, H, s, seed=241):
    """Spin Master: the desert of the pyramids, as in the game: a deep blue sky, big pyramids, a great stone sphinx,
    dunes, a wall of stone blocks and the sand. / Le désert des pyramides : ciel bleu, pyramides, sphinx, dunes, sable."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (60, 110, 220)), (0.6, (130, 180, 240)), (1.0, (200, 220, 240))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    for k in range(5):                                                   # les pyramides
        x = tw * (0.08 + 0.2 * k) + rng.uniform(-40, 40) * s
        w = rng.uniform(260, 420) * s
        h = w * 0.62
        base = 300 * s
        far.poly([(x - w / 2, base), (x, base - h), (x + w / 2, base)], (226, 190, 120, 255))
        far.poly([(x, base - h), (x + w / 2, base), (x + w * 0.1, base)], (196, 156, 90, 255))
        for i in range(1, 8):
            yy = base - h * i / 8
            far.line([(x - w / 2 * (1 - i / 8), yy), (x + w / 2 * (1 - i / 8), yy)], (176, 140, 80, 255), 1.5 * s)
    sx = tw * 0.62                                                        # le sphinx
    far.poly([(sx - 150 * s, 300 * s), (sx - 150 * s, 250 * s), (sx + 60 * s, 240 * s), (sx + 70 * s, 300 * s)], (210, 170, 100, 255),
             (130, 100, 60, 255), 2 * s)
    far.poly([(sx + 20 * s, 250 * s), (sx + 20 * s, 170 * s), (sx + 50 * s, 150 * s), (sx + 90 * s, 160 * s), (sx + 100 * s, 250 * s)],
             (220, 180, 110, 255), (130, 100, 60, 255), 2 * s)
    far.poly([(sx + 14 * s, 170 * s), (sx + 30 * s, 150 * s), (sx + 70 * s, 140 * s), (sx + 106 * s, 160 * s), (sx + 110 * s, 220 * s),
              (sx + 96 * s, 200 * s), (sx + 40 * s, 196 * s)], (60, 80, 150, 255))
    layers.append({"img": far.done(), "y": 0, "f": 0.2, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    pts = [(0, H)]
    for i in range(41):                                                  # les dunes
        pts.append((tw * i / 40, (300 + 20 * math.sin(i * 0.9) + 10 * math.sin(i * 2.3)) * s))
    pts.append((tw, H))
    mid.poly(pts, (230, 196, 130, 255))
    for k in range(3):                                                   # un mur de blocs de pierre
        x0 = tw * (0.1 + 0.33 * k)
        for r in range(4):
            for c in range(8):
                x = x0 + c * 50 * s + (r % 2) * 25 * s
                y = (SM_FLOOR - 40 - r * 30) * s
                mid.poly([(x, y), (x + 48 * s, y), (x + 48 * s, y + 28 * s), (x, y + 28 * s)], (200, 160, 100, 255), (130, 100, 60, 255), 1.5 * s)
    layers.append({"img": mid.done(), "y": 0, "f": 0.5, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    gy = SM_FLOOR * s
    near.poly([(0, gy), (tw, gy), (tw, H), (0, H)], (236, 206, 140, 255))                   # le sable
    for i in range(int(tw / (40 * s))):
        x = i * 40 * s
        near.line([(x, gy + 20 * s), (x + 30 * s, gy + 14 * s), (x + 60 * s, gy + 20 * s)], (210, 176, 110, 255), 3 * s)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": layers, "tw": tw, "amb": {}}


def build_gr_town(W, H, s, seed=251):
    """Ganryu: a street of old Japan at night, as in the game: a violet sky, wooden houses under their dark tiled roofs,
    curtains with a round crest, lanterns, the beaten earth and the stone wall in front.
    / Une rue du vieux Japon la nuit : maisons de bois, toits de tuiles, rideaux au blason rond, lanternes, mur de pierre."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (30, 20, 60)), (0.5, (70, 40, 100)), (1.0, (110, 60, 120))])
    p = _Pic(tw, H, 2, tw)
    lights = []
    x = 0
    base = BRAWL_FLOOR * s
    while x < tw:                                                        # les maisons de bois
        w = rng.uniform(260, 380) * s
        top = rng.uniform(90, 130) * s
        p.poly([(x, base), (x, top + 40 * s), (x + w, top + 40 * s), (x + w, base)], (70, 50, 40, 255), (30, 20, 16, 255), 2 * s)
        for k in range(int(w / (30 * s))):                               # les lattes
            p.line([(x + k * 30 * s, top + 60 * s), (x + k * 30 * s, base)], (50, 34, 28, 255), 2 * s)
        p.poly([(x - 20 * s, top + 44 * s), (x + 30 * s, top), (x + w - 30 * s, top), (x + w + 20 * s, top + 44 * s)], (40, 44, 60, 255),
               (20, 20, 30, 255), 2 * s)                                 # le toit de tuiles
        for k in range(int(w / (16 * s))):
            p.line([(x + k * 16 * s, top + 4 * s), (x - 10 * s + k * 16 * s, top + 42 * s)], (60, 66, 86, 255), 2 * s)
        cx = x + w * 0.35                                                # le rideau et son blason
        p.poly([(cx - 70 * s, top + 70 * s), (cx + 70 * s, top + 70 * s), (cx + 70 * s, base - 60 * s), (cx - 70 * s, base - 60 * s)],
               (70, 90, 100, 255))
        p.disc(cx, top + 120 * s, 34 * s, (30, 40, 50, 255))
        p.disc(cx, top + 120 * s, 26 * s, (70, 90, 100, 255))
        p.line([(cx - 26 * s, top + 120 * s), (cx + 26 * s, top + 120 * s)], (30, 40, 50, 255), 5 * s)
        p.line([(cx, top + 94 * s), (cx, top + 146 * s)], (30, 40, 50, 255), 5 * s)
        lx = x + w * 0.78                                                # une lanterne
        p.ellipse(lx - 16 * s, top + 60 * s, lx + 16 * s, top + 100 * s, (240, 200, 120, 255), (90, 50, 20, 255), 2 * s)
        lights.append((lx, top + 80 * s))
        x += w + rng.uniform(10, 40) * s
    p.poly([(0, base), (tw, base), (tw, H), (0, H)], (110, 70, 40, 255))                   # la terre battue
    for _ in range(int(tw / (10 * s))):
        xx, yy = rng.uniform(0, tw), rng.uniform(base, H - 60 * s)
        p.disc(xx, yy, rng.uniform(2, 5) * s, (130, 90, 56, 255))
    for k in range(int(tw / (110 * s)) + 1):                             # le mur de pierre devant
        xx = k * 110 * s
        p.poly([(xx, H - 56 * s), (xx + 104 * s, H - 60 * s), (xx + 108 * s, H), (xx - 4 * s, H)], (70, 76, 70, 255), (30, 34, 30, 255), 2 * s)
    return {"sky": sky, "layers": [{"img": p.done(), "y": 0, "f": 1.0, "stage": "mid", "lights": lights}], "tw": tw,
            "amb": {"window": (255, 200, 120)}}


def build_zp_cave(W, H, s, seed=261):
    """Zupapa!: the blue cave and its old stone statues, the platforms striped orange and blue, as in the game.
    / La grotte bleue et ses vieilles statues, les plateformes rayées orange et bleu, comme dans le jeu."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (30, 50, 120)), (1.0, (50, 70, 150))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(240):                                                 # la roche
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.uniform(10, 30) * s
        p.ellipse(x - r, y - r * 0.6, x + r, y + r * 0.6, rng.choice(((40, 64, 140, 255), (60, 90, 170, 255), (30, 50, 110, 255))))
    for k in range(4):                                                   # les statues de pierre
        x = W * (0.12 + 0.25 * k)
        p.ellipse(x - 60 * s, 120 * s, x + 60 * s, 250 * s, (80, 90, 120, 255), (40, 44, 70, 255), 2 * s)
        p.disc(x - 22 * s, 170 * s, 12 * s, (40, 44, 70, 255))
        p.disc(x + 22 * s, 170 * s, 12 * s, (40, 44, 70, 255))
        p.poly([(x - 80 * s, 250 * s), (x + 80 * s, 250 * s), (x + 100 * s, 400 * s), (x - 100 * s, 400 * s)], (70, 80, 110, 255), (40, 44, 70, 255),
               2 * s)
    for y, segs in ZP_ROWS:                                              # les plateformes rayées
        for x0, x1 in segs:
            a, b = x0 * s, x1 * s
            yy = y * s
            p.poly([(a, yy), (b, yy), (b, yy + 18 * s), (a, yy + 18 * s)], (230, 110, 40, 255), (90, 40, 10, 255), 1.5 * s)
            xx = a
            while xx < b:
                p.poly([(xx, yy), (min(b, xx + 10 * s), yy), (min(b, xx + 4 * s), yy + 18 * s), (xx - 6 * s, yy + 18 * s)], (60, 120, 230, 255))
                xx += 26 * s
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def nmd_tile_draw(p, x, y, c, s, rng):
    """One tile of the field of Neo Mr. Do!: a coloured frame and a little toy or tool. / Une case du champ."""
    col = rng.choice(((230, 120, 150), (120, 190, 230), (240, 210, 90), (150, 220, 140), (200, 150, 230), (250, 170, 90)))
    p.poly([(x + 1 * s, y + 1 * s), (x + c - 1 * s, y + 1 * s), (x + c - 1 * s, y + c - 1 * s), (x + 1 * s, y + c - 1 * s)], _rgba(col),
           _rgba(mix(col, (0, 0, 0), 0.35)), 1.5 * s)
    kind = rng.randrange(5)
    cx, cy = x + c / 2, y + c / 2
    ink = _rgba(mix(col, (0, 0, 0), 0.5))
    if kind == 0:                                                        # une tasse
        p.poly([(cx - 9 * s, cy - 6 * s), (cx + 7 * s, cy - 6 * s), (cx + 5 * s, cy + 8 * s), (cx - 7 * s, cy + 8 * s)], (250, 250, 250, 255), ink, 1 * s)
    elif kind == 1:                                                      # un marteau
        p.line([(cx - 8 * s, cy + 8 * s), (cx + 6 * s, cy - 6 * s)], ink, 3 * s)
        p.poly([(cx + 2 * s, cy - 12 * s), (cx + 12 * s, cy - 2 * s), (cx + 8 * s, cy + 2 * s), (cx - 2 * s, cy - 8 * s)], (160, 160, 170, 255), ink, 1 * s)
    elif kind == 2:                                                      # un réveil
        p.disc(cx, cy, 10 * s, (250, 250, 250, 255), ink, 1.5 * s)
        p.line([(cx, cy), (cx, cy - 7 * s)], ink, 2 * s)
        p.line([(cx, cy), (cx + 5 * s, cy)], ink, 2 * s)
    elif kind == 3:                                                      # un bonbon
        p.ellipse(cx - 8 * s, cy - 6 * s, cx + 8 * s, cy + 6 * s, (250, 120, 160, 255), ink, 1 * s)
        p.poly([(cx - 8 * s, cy), (cx - 14 * s, cy - 6 * s), (cx - 14 * s, cy + 6 * s)], (250, 120, 160, 255))
        p.poly([(cx + 8 * s, cy), (cx + 14 * s, cy - 6 * s), (cx + 14 * s, cy + 6 * s)], (250, 120, 160, 255))
    else:                                                                # une fleur
        for i in range(5):
            a = i * 1.257
            p.disc(cx + math.cos(a) * 6 * s, cy + math.sin(a) * 6 * s, 4 * s, (250, 250, 250, 255))
        p.disc(cx, cy, 4 * s, (250, 200, 60, 255))


def build_nmd_field(W, H, s, seed=271):
    """Neo Mr. Do!: the field of coloured tiles with their toys and tools inside a frame of red and orange stars, as in
    the game. / Le champ de cases colorées et leurs jouets et outils, dans un cadre d'étoiles rouges et orange."""
    rng = random.Random(seed)
    sky = Image.new("RGB", (W, H), (220, 60, 30))
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(60):                                                  # le cadre d'étoiles
        cx, cy = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.uniform(20, 50) * s
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        p.poly(pts, rng.choice(((250, 140, 40, 255), (240, 90, 30, 255), (250, 190, 60, 255))))
    x0, y0, c, cols, rows = NMD
    p.poly([(x0 * s - 8 * s, y0 * s - 8 * s), ((x0 + c * cols) * s + 8 * s, y0 * s - 8 * s), ((x0 + c * cols) * s + 8 * s, (y0 + c * rows) * s + 8 * s),
            (x0 * s - 8 * s, (y0 + c * rows) * s + 8 * s)], (60, 40, 90, 255))
    for r in range(rows):
        for k in range(cols):
            nmd_tile_draw(p, (x0 + k * c) * s, (y0 + r * c) * s, c * s, s, rng)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


hd_bg.BUILDERS.update({"pdpr_stars": build_pdpr_stars, "pbm_check": build_pbm_check, "pnb_jungle": build_pnb_jungle, "sbp_swirl": build_sbp_swirl,
                       "sm_desert": build_sm_desert, "gr_town": build_gr_town, "zp_cave": build_zp_cave, "nmd_field": build_nmd_field})

