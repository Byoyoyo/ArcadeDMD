"""HD backdrops of the fourth batch of Neo Geo games done one by one (1.20), each drawn after screenshots of its game:
the war-torn ground seen from the sky of Strikers 1945 Plus, the street courts of Street Hoop, the schoolyard of Super
Dodge Ball. Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS
when this module is imported.

Décors HD du quatrième lot (1.20), chacun dessiné d'après des captures de son jeu : le sol ravagé vu du ciel de
Strikers 1945 Plus, les terrains de rue de Street Hoop, la cour d'école de Super Dodge Ball. Tout est dessiné par le
programme, aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from . import hd_bg
from .hd_bg import mix, noise_rgb, vgrad
from .hd_themes3 import _Pic, _clump, _rgba


# ---------------------------------------------------------------------------- Strikers 1945 Plus
def _rail(p, tw, y, s, wood=(70, 54, 38), steel=(160, 156, 148)):
    """A railway along the ground: its bed of gravel, its sleepers and two rails. / Une voie ferrée, ballast et rails."""
    p.poly([(0, y - 14 * s), (tw, y - 14 * s), (tw, y + 14 * s), (0, y + 14 * s)], (124, 118, 104, 255))
    p.line([(0, y + 14 * s), (tw, y + 14 * s)], (70, 64, 52, 200), 2 * s)
    for x in range(0, int(tw), max(2, int(8 * s))):
        p.poly([(x, y - 9 * s), (x + 3.4 * s, y - 9 * s), (x + 3.4 * s, y + 9 * s), (x, y + 9 * s)], _rgba(wood))
    for k in (-5, 5):
        p.line([(0, y + k * s), (tw, y + k * s)], _rgba(steel), 1.8 * s)


def _house(p, x, y, w, h, s, rng, roof):
    """A house seen from high above: its long shadow, a gable roof of tiles lit from the top, now and then broken by a
    bomb, its beams showing. / Une maison vue de haut : ombre, toit de tuiles à deux pans, parfois crevé."""
    sh = 0.55 * h + 6 * s
    p.poly([(x + w, y), (x + w + sh, y + sh * 0.7), (x + w + sh, y + h + sh * 0.7), (x + sh, y + h + sh * 0.7), (x, y + h)], (24, 20, 16, 150))
    lit, dark = mix(roof, (255, 236, 200), 0.18), mix(roof, (0, 0, 0), 0.3)
    p.poly([(x, y), (x + w, y), (x + w, y + h / 2), (x, y + h / 2)], _rgba(lit))
    p.poly([(x, y + h / 2), (x + w, y + h / 2), (x + w, y + h), (x, y + h)], _rgba(dark))
    for k in range(1, int(h / (4 * s))):                                  # rangs de tuiles
        yy = y + k * 4 * s
        if abs(yy - (y + h / 2)) > 1.5 * s:
            p.line([(x + 1 * s, yy), (x + w - 1 * s, yy)], _rgba(mix(roof, (0, 0, 0), 0.42), 150), 0.9 * s)
    p.line([(x, y + h / 2), (x + w, y + h / 2)], _rgba(mix(roof, (255, 255, 255), 0.35)), 1.6 * s)
    p.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], None, (36, 28, 22, 255), 1.2 * s)
    if rng.random() < 0.55:                                               # crevé par une bombe
        hx, hy = x + rng.uniform(0.15, 0.55) * w, y + rng.uniform(0.1, 0.45) * h
        hw, hh = rng.uniform(0.25, 0.42) * w, rng.uniform(0.35, 0.5) * h
        pts = [(hx, hy + hh * 0.2), (hx + hw * 0.3, hy), (hx + hw * 0.7, hy + hh * 0.1), (hx + hw, hy + hh * 0.4),
               (hx + hw * 0.8, hy + hh), (hx + hw * 0.3, hy + hh * 0.85)]
        p.poly(pts, (28, 22, 18, 255), (70, 50, 36, 255), 1.0 * s)
        for k in range(2):
            bx = hx + hw * (0.3 + 0.35 * k)
            p.line([(bx, hy + hh * 0.05), (bx + hw * 0.08, hy + hh * 0.95)], (110, 80, 50, 255), 1.6 * s)
        for _ in range(5):                                                # gravats autour
            gx, gy = x + rng.uniform(-0.2, 1.2) * w, y + h + rng.uniform(0, 10) * s
            p.disc(gx, gy, rng.uniform(1.5, 3.2) * s, _rgba(rng.choice(((140, 126, 108), (150, 84, 60), (110, 100, 86)))))


def _stone(p, x, y, w, h, s, rng):
    """A building with a flat stone roof and its parapet, or only its walls when it burnt. / Un bâtiment de pierre."""
    sh = 0.5 * h + 8 * s
    p.poly([(x + w, y), (x + w + sh, y + sh * 0.7), (x + w + sh, y + h + sh * 0.7), (x + sh, y + h + sh * 0.7), (x, y + h)], (24, 20, 16, 150))
    ruin = rng.random() < 0.4
    inside = (46, 40, 32, 255) if ruin else (138, 132, 118, 255)
    p.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], inside, (172, 166, 150, 255), 3.2 * s)
    p.poly([(x + 3 * s, y + 3 * s), (x + w - 3 * s, y + 3 * s), (x + w - 3 * s, y + h - 3 * s), (x + 3 * s, y + h - 3 * s)], None,
           (96, 90, 78, 255), 1.0 * s)
    if ruin:
        for _ in range(6):
            p.disc(x + rng.uniform(0.15, 0.85) * w, y + rng.uniform(0.15, 0.85) * h, rng.uniform(2, 4) * s, (120, 112, 98, 255))
    else:
        for _ in range(2):                                                # cheminées, bouches d'aération
            cx, cy = x + rng.uniform(0.2, 0.8) * w, y + rng.uniform(0.2, 0.8) * h
            p.poly([(cx, cy), (cx + 5 * s, cy), (cx + 5 * s, cy + 5 * s), (cx, cy + 5 * s)], (90, 86, 78, 255))


def _trees(p, x, y, n, spread, s, rng, tones=((34, 50, 26), (52, 70, 36), (72, 94, 46))):
    """A copse of dark trees with their shadows, seen from above. / Un bosquet d'arbres sombres et leurs ombres."""
    pts = [(x + rng.gauss(0, spread[0]), y + rng.gauss(0, spread[1]), rng.uniform(5, 10) * s) for _ in range(n)]
    for tx, ty, r in pts:
        p.disc(tx + r * 0.6, ty + r * 0.5, r, (20, 18, 14, 150))
    for col, ox, oy, sc in ((tones[0], 0, 0, 1.0), (tones[1], -0.15, -0.2, 0.78), (tones[2], -0.3, -0.36, 0.42)):
        for tx, ty, r in pts:
            p.disc(tx + ox * r, ty + oy * r, r * sc, _rgba(col))


def _crater(p, x, y, r, s):
    p.ellipse(x - r * 1.25, y - r, x + r * 1.25, y + r, (64, 56, 44, 255))
    p.ellipse(x - r, y - r * 0.78, x + r, y + r * 0.78, (34, 30, 24, 255))
    p.chord(x - r, y - r * 0.78, x + r, y + r * 0.78, 20, 160, (82, 74, 58, 255))
    p.ellipse(x - r * 0.4, y - r * 0.3, x + r * 0.3, y + r * 0.2, (46, 40, 32, 255))


def build_s45_ground(W, H, s, seed=61):
    """Strikers 1945 Plus: war-torn ground seen from high above, as in the game: grey-brown earth, villages of houses
    with tiled roofs broken by the bombs and their long shadows, stone buildings, a railway and its train, a muddy
    river with its bridges, fields, copses of dark trees, craters. / Le sol ravagé vu du ciel, comme dans le jeu :
    villages aux toits de tuiles crevés et leurs longues ombres, voie ferrée et son train, rivière, bosquets, cratères."""
    rng = random.Random(seed)
    tw = 2 * W
    k8 = 8
    lw, lh = tw // k8, max(2, H // k8)
    low = Image.new("RGB", (lw * 3, lh), (100, 92, 74))                  # les grandes variations de la terre, très douces
    dl = ImageDraw.Draw(low)
    for _ in range(int(lw / 3)):
        x, y = rng.uniform(0, lw), rng.uniform(0, lh)
        r = rng.uniform(2, 7)
        col = rng.choice(((94, 86, 68), (106, 98, 78), (96, 92, 70), (110, 100, 80), (90, 84, 66)))
        for dx in (0, lw, 2 * lw):
            dl.ellipse([x + dx - r, y - r * 0.7, x + dx + r, y + r * 0.7], fill=col)
    low = low.filter(ImageFilter.GaussianBlur(2.5)).crop((lw, 0, 2 * lw, lh))
    img = low.resize((tw, H), Image.BILINEAR)
    img = ImageChops.add(img, noise_rgb(tw, H, 9), 1.0, -128)            # le grain de la terre
    p = _Pic(tw, H, 2, tw)
    ry, rv, road = H * 0.17, H * 0.74, H * 0.47
    fields = []
    x = rng.uniform(0, 200) * s
    while x < tw - 200 * s:                                              # champs, vert sombre ou brun, labourés
        w, h = rng.uniform(160, 300) * s, rng.uniform(60, 110) * s
        y = rng.choice((ry + 24 * s, road + 16 * s, rv + 36 * s))
        col = rng.choice(((84, 96, 58), (96, 100, 62), (104, 90, 62), (76, 88, 52)))
        p.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], _rgba(col))
        for kk in range(1, int(h / (6 * s))):
            p.line([(x + 2 * s, y + kk * 6 * s), (x + w - 2 * s, y + kk * 6 * s)], _rgba(mix(col, (0, 0, 0), 0.2), 200), 1.2 * s)
        fields.append((x, y, w, h))
        x += w + rng.uniform(500, 900) * s
    for _ in range(int(tw / (40 * s))):                                  # taches brûlées, terre retournée
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        r = rng.uniform(14, 40) * s
        p.ellipse(x - r, y - r * 0.6, x + r, y + r * 0.6, rng.choice(((40, 34, 26, 46), (70, 62, 46, 50), (124, 112, 90, 40))))
    river = [(xx, rv + math.sin(xx / tw * math.tau * 2) * 18 * s + math.sin(xx / tw * math.tau * 5 + 1) * 6 * s) for xx in range(0, tw + 8, 8)]
    p.line(river, (82, 96, 58, 255), 54 * s)                             # berges herbeuses
    p.line(river, (90, 80, 62, 255), 40 * s)
    p.line(river, (52, 64, 70, 255), 30 * s)                             # l'eau boueuse
    p.line([(px, py - 7 * s) for px, py in river], (84, 100, 104, 255), 2.4 * s)
    p.line([(0, road), (tw, road)], (124, 112, 90, 255), 18 * s)          # la route de terre
    p.line([(0, road - 9 * s), (tw, road - 9 * s)], (88, 78, 62, 255), 1.4 * s)
    p.line([(0, road + 9 * s), (tw, road + 9 * s)], (88, 78, 62, 255), 1.4 * s)
    towns = [tw * f for f in (0.12, 0.45, 0.78)]
    for tx in towns:                                                     # chaque village : une rue qui descend jusqu'au pont
        p.line([(tx, ry + 14 * s), (tx, H)], (124, 112, 90, 255), 14 * s)
        by = rv + math.sin(tx / tw * math.tau * 2) * 18 * s + math.sin(tx / tw * math.tau * 5 + 1) * 6 * s
        p.poly([(tx - 14 * s, by - 30 * s), (tx + 14 * s, by - 30 * s), (tx + 14 * s, by + 30 * s), (tx - 14 * s, by + 30 * s)],
               (150, 142, 124, 255), (70, 62, 50, 255), 2 * s)           # pont de pierre
        p.poly([(tx + 14 * s, by - 26 * s), (tx + 24 * s, by - 20 * s), (tx + 24 * s, by + 36 * s), (tx + 14 * s, by + 30 * s)], (30, 26, 22, 140))
    _rail(p, tw, ry, s)
    for tx in towns:                                                     # les maisons, de part et d'autre des rues
        for row in (ry + 22 * s, road - 70 * s, road + 16 * s, rv - 86 * s):
            x = tx - rng.uniform(260, 340) * s
            end = tx + rng.uniform(240, 330) * s
            while x < end:
                w, h = rng.uniform(26, 52) * s, rng.uniform(26, 44) * s
                if x < tx + 12 * s and x + w > tx - 12 * s:                     # pas sur la rue
                    x = tx + 12 * s
                    continue
                y = row + rng.uniform(0, 10) * s
                if rng.random() < 0.8:
                    if rng.random() < 0.78:
                        _house(p, x, y, w, h, s, rng, rng.choice(((150, 78, 54), (140, 70, 50), (160, 92, 64), (124, 66, 50), (120, 104, 90))))
                    else:
                        _stone(p, x, y, w * 1.3, h * 1.2, s, rng)
                x += w + rng.uniform(4, 16) * s
        for _ in range(5):
            _crater(p, tx + rng.uniform(-300, 300) * s, rng.uniform(ry + 30 * s, rv - 40 * s), rng.uniform(7, 14) * s, s)
    for _ in range(int(tw / (22 * s))):                                  # arbres isolés
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        if abs(y - ry) < 18 * s or abs(y - road) < 14 * s:
            continue
        _trees(p, x, y, 1, (0, 0), s, rng)
    for _ in range(int(tw / (85 * s))):                                  # bosquets
        x, y = rng.uniform(0, tw), rng.choice((rng.uniform(ry + 30 * s, road - 30 * s), rng.uniform(road + 30 * s, rv - 40 * s),
                                                rng.uniform(rv + 40 * s, H), rng.uniform(0, ry - 20 * s)))
        if any(abs(x - tx) < 330 * s for tx in towns) and rng.random() < 0.7:
            continue
        _trees(p, x, y, rng.randint(6, 16), (rng.uniform(16, 40) * s, rng.uniform(8, 18) * s), s, rng)
    for _ in range(int(tw / (240 * s))):                                 # cratères isolés
        _crater(p, rng.uniform(0, tw), rng.uniform(0, H), rng.uniform(6, 12) * s, s)
    over = p.done()
    img = img.convert("RGBA")
    img.alpha_composite(over)
    train = _Pic(int(420 * s), int(30 * s), 3)                           # un train sur la voie
    for i in range(6):
        x0 = i * 68 * s
        col = (52, 58, 50) if i else (34, 34, 38)
        train.poly([(x0 + 2 * s, 5 * s), (x0 + 64 * s, 5 * s), (x0 + 64 * s, 25 * s), (x0 + 2 * s, 25 * s)], _rgba(col), (16, 16, 16, 255), 1.2 * s)
        train.poly([(x0 + 6 * s, 9 * s), (x0 + 60 * s, 9 * s), (x0 + 60 * s, 21 * s), (x0 + 6 * s, 21 * s)], _rgba(mix(col, (255, 255, 255), 0.14)))
        if i == 0:
            train.disc(x0 + 14 * s, 15 * s, 5 * s, (60, 60, 64, 255), (16, 16, 16, 255), 1 * s)
        elif i % 2:
            for kk in range(3):
                train.poly([(x0 + (10 + kk * 17) * s, 10 * s), (x0 + (22 + kk * 17) * s, 10 * s), (x0 + (22 + kk * 17) * s, 20 * s),
                            (x0 + (10 + kk * 17) * s, 20 * s)], (120, 96, 60, 255), (40, 30, 20, 255), 0.8 * s)
    tr_img = train.done()
    img.alpha_composite(tr_img, (int(tw * 0.62), int(ry - 15 * s)))
    layers = [{"img": img.convert("RGB"), "y": 0, "f": 1.0, "stage": "far"}]
    return {"sky": Image.new("RGB", (W, H), (100, 92, 74)), "layers": layers, "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Street Hoop
HOOP_FLOOR = 300          # top of the court in the picture, at s = 1 / haut du terrain dans l'image
HOOP_X = 250              # the rim, this far from the right edge, at s = 1 / le cercle, à cette distance du bord droit


def hoop_y(z, H, s):
    """y of the court at the depth z, 0 far, 1 near: the scene uses the same. / Le sol à la profondeur z."""
    return (HOOP_FLOOR + 26) * s + z * (H - (HOOP_FLOOR + 40) * s)


def _sitter(p, cx, seat, s, rng, shirt, skin, hair, legs=(50, 60, 90)):
    """A spectator sitting on a bench, seen from the front. / Un spectateur assis sur un banc, vu de face."""
    out = (40, 30, 30, 255)
    for dx in (-7, 7):                                                   # jambes : genoux puis tibias
        p.poly([(cx + (dx - 6) * s, seat - 2 * s), (cx + (dx + 6) * s, seat - 2 * s), (cx + (dx + 5) * s, seat + 8 * s), (cx + (dx - 5) * s, seat + 8 * s)],
               _rgba(legs), out, 1.2 * s)
        p.poly([(cx + (dx - 4) * s, seat + 8 * s), (cx + (dx + 4) * s, seat + 8 * s), (cx + (dx + 4) * s, seat + 30 * s), (cx + (dx - 4) * s, seat + 30 * s)],
               _rgba(legs), out, 1.2 * s)
        p.poly([(cx + (dx - 5) * s, seat + 28 * s), (cx + (dx + 6) * s, seat + 28 * s), (cx + (dx + 6) * s, seat + 33 * s), (cx + (dx - 5) * s, seat + 33 * s)],
               (236, 236, 236, 255), out, 1.0 * s)
    p.poly([(cx - 14 * s, seat), (cx + 14 * s, seat), (cx + 12 * s, seat - 32 * s), (cx - 12 * s, seat - 32 * s)], _rgba(shirt), out, 1.4 * s)
    for dx in (-1, 1):                                                   # bras posés sur les cuisses
        p.line([(cx + dx * 12 * s, seat - 28 * s), (cx + dx * 15 * s, seat - 8 * s), (cx + dx * 8 * s, seat - 2 * s)], _rgba(shirt), 6 * s)
        p.disc(cx + dx * 8 * s, seat - 2 * s, 3.4 * s, _rgba(skin))
    p.disc(cx, seat - 42 * s, 10 * s, _rgba(skin), out, 1.2 * s)
    p.chord(cx - 10 * s, seat - 53 * s, cx + 10 * s, seat - 38 * s, 180, 360, _rgba(hair))


def _stander(p, cx, foot, s, rng, shirt, skin, hair, legs=(60, 70, 110)):
    """A spectator standing, hands in the pockets of his hoodie. / Un spectateur debout, mains dans les poches."""
    out = (40, 30, 30, 255)
    for dx in (-6, 6):
        p.poly([(cx + (dx - 5) * s, foot - 44 * s), (cx + (dx + 5) * s, foot - 44 * s), (cx + (dx + 4) * s, foot - 4 * s), (cx + (dx - 4) * s, foot - 4 * s)],
               _rgba(legs), out, 1.2 * s)
        p.poly([(cx + (dx - 5) * s, foot - 5 * s), (cx + (dx + 7) * s, foot - 5 * s), (cx + (dx + 7) * s, foot), (cx + (dx - 5) * s, foot)],
               (240, 240, 240, 255), out, 1.0 * s)
    p.poly([(cx - 17 * s, foot - 42 * s), (cx + 17 * s, foot - 42 * s), (cx + 15 * s, foot - 86 * s), (cx - 15 * s, foot - 86 * s)], _rgba(shirt),
           out, 1.4 * s)
    p.poly([(cx - 10 * s, foot - 60 * s), (cx + 10 * s, foot - 60 * s), (cx + 10 * s, foot - 50 * s), (cx - 10 * s, foot - 50 * s)],
           _rgba(mix(shirt, (0, 0, 0), 0.2)))
    p.disc(cx, foot - 96 * s, 11 * s, _rgba(skin), out, 1.2 * s)
    p.chord(cx - 11 * s, foot - 108 * s, cx + 11 * s, foot - 92 * s, 180, 360, _rgba(hair))


def build_hoop_park(W, H, s, seed=62):
    """Street Hoop: a half court in a park, as in the game: trees, a wooden fence, people sitting on the benches or
    standing, a bike lying on the grass, bags, then the painted asphalt court in blue and brick red, its white lines,
    the key and the three-point line in front of the hoop on the right. / Un demi-terrain dans un parc, comme dans le
    jeu : arbres, barrière de bois, spectateurs, vélo couché, puis l'asphalte peint, la raquette et la ligne à trois points."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (120, 180, 230)), (0.4, (170, 210, 236)), (1.0, (200, 226, 236))])
    p = _Pic(W, H, 2, tw=4 * W)                                          # fixed backdrop: nothing repeats / rien ne se répète
    for _ in range(int(W / (52 * s))):                                   # les arbres du parc
        x = rng.uniform(0, W)
        r = rng.uniform(50, 90) * s
        y = rng.uniform(50, 120) * s
        p.poly([(x - 8 * s, y + r * 0.6), (x + 8 * s, y + r * 0.6), (x + 10 * s, 200 * s), (x - 10 * s, 200 * s)], (90, 66, 46, 255))
        _clump(p, x, y, r, rng, ((40, 96, 40), (62, 132, 52), (110, 176, 80)), n=10)
    p.poly([(0, 186 * s), (W, 186 * s), (W, HOOP_FLOOR * s), (0, HOOP_FLOOR * s)], (98, 150, 70, 255))      # la pelouse
    for _ in range(int(W / (6 * s))):
        x, y = rng.uniform(0, W), rng.uniform(190, HOOP_FLOOR - 4) * s
        p.line([(x, y), (x + 1.5 * s, y - 4 * s)], (70, 120, 52, 255), 1.2 * s)
    for x in range(0, W + int(80 * s), int(80 * s)):                     # la barrière de bois
        p.poly([(x - 4 * s, 168 * s), (x + 4 * s, 168 * s), (x + 4 * s, 212 * s), (x - 4 * s, 212 * s)], (150, 110, 70, 255), (70, 50, 34, 255), 1.4 * s)
    for y in (176, 194):
        p.poly([(0, y * s), (W, y * s), (W, (y + 7) * s), (0, (y + 7) * s)], (176, 132, 84, 255), (70, 50, 34, 255), 1.4 * s)
    skins = ((236, 190, 150), (200, 150, 110), (150, 100, 70), (110, 74, 50))
    hairs = ((40, 30, 24), (90, 60, 30), (200, 170, 90), (30, 30, 34))
    shirts = ((220, 70, 60), (70, 120, 220), (240, 200, 70), (90, 170, 90), (240, 240, 240), (150, 90, 170), (90, 150, 210))
    for bx in (W * 0.05, W * 0.52):                                      # bancs, des gens assis, des sacs
        seat = 262 * s
        p.poly([(bx, seat - 26 * s), (bx + 250 * s, seat - 26 * s), (bx + 250 * s, seat - 18 * s), (bx, seat - 18 * s)], (150, 110, 70, 255),
               (60, 40, 30, 255), 1.5 * s)
        for lx in (bx + 12 * s, bx + 238 * s):
            p.poly([(lx - 3 * s, seat), (lx + 3 * s, seat), (lx + 3 * s, seat + 28 * s), (lx - 3 * s, seat + 28 * s)], (90, 66, 46, 255))
        p.poly([(bx, seat - 6 * s), (bx + 250 * s, seat - 6 * s), (bx + 250 * s, seat + 2 * s), (bx, seat + 2 * s)], (170, 128, 80, 255),
               (60, 40, 30, 255), 1.5 * s)
        for k in range(4):
            cx = bx + 30 * s + k * 52 * s
            if k == 2 and bx > W * 0.3:                                  # un sac de sport à la place
                p.poly([(cx - 22 * s, seat - 4 * s), (cx + 22 * s, seat - 4 * s), (cx + 18 * s, seat - 26 * s), (cx - 18 * s, seat - 26 * s)],
                       (60, 70, 140, 255), (30, 30, 50, 255), 1.4 * s)
                p.line([(cx - 10 * s, seat - 26 * s), (cx, seat - 34 * s), (cx + 10 * s, seat - 26 * s)], (30, 30, 50, 255), 2 * s)
                continue
            _sitter(p, cx, seat, s, rng, rng.choice(shirts), rng.choice(skins), rng.choice(hairs))
    for x in (W * 0.33, W * 0.39, W * 0.86):                             # des gens debout
        _stander(p, x, 288 * s, s, rng, rng.choice(shirts), rng.choice(skins), rng.choice(hairs))
    bx, by = W * 0.44, 282 * s                                           # un vélo couché dans l'herbe
    for wx in (bx, bx + 50 * s):
        p.ellipse(wx - 15 * s, by - 9 * s, wx + 15 * s, by + 9 * s, None, (40, 40, 44, 255), 2.6 * s)
    p.line([(bx, by), (bx + 18 * s, by - 6 * s), (bx + 36 * s, by - 6 * s), (bx + 50 * s, by), (bx + 26 * s, by + 2 * s), (bx + 18 * s, by - 6 * s)],
           (220, 60, 50, 255), 3 * s)
    p.line([(bx + 36 * s, by - 6 * s), (bx + 40 * s, by - 14 * s)], (40, 40, 44, 255), 2.4 * s)
    fy = HOOP_FLOOR * s                                                  # le terrain
    p.poly([(0, fy), (W, fy), (W, H), (0, H)], (196, 104, 80, 255))
    y0, y1 = hoop_y(-0.12, H, s), hoop_y(1.06, H, s)
    xb0, xb1 = W - 110 * s, W - 70 * s                                   # la ligne de fond, sous le panier, à droite
    court = [(-10 * s, y0), (xb0, y0), (xb1, y1), (-10 * s, y1)]
    p.poly(court, (78, 124, 168, 255))
    white = (246, 246, 240, 255)
    rx = W - HOOP_X * s
    ym = hoop_y(0.5, H, s)
    def bx_at(y):
        return xb0 + (xb1 - xb0) * (y - y0) / (y1 - y0)
    ka, kb = hoop_y(0.24, H, s), hoop_y(0.76, H, s)                      # la raquette, peinte
    kx = rx - 330 * s
    p.poly([(kx, ka), (bx_at(ka), ka), (bx_at(kb), kb), (kx, kb)], (186, 92, 70, 255), white, 3 * s)
    p.ellipse(kx - 70 * s, ka, kx + 70 * s, kb, None, white, 3 * s)        # le cercle de la ligne des lancers
    p.chord(kx - 70 * s, ka, kx + 70 * s, kb, 90, 270, (78, 124, 168, 255))
    p.ellipse(kx - 70 * s, ka, kx + 70 * s, kb, None, white, 3 * s)
    p.poly([(kx, ka), (bx_at(ka), ka), (bx_at(kb), kb), (kx, kb)], None, white, 3 * s)
    arc = []                                                             # la ligne à trois points
    for i in range(41):
        a = math.radians(90 + 180 * i / 40)
        x = rx + math.cos(a) * 640 * s
        y = ym - math.sin(a) * (y1 - y0) * 0.5 * 0.92
        arc.append((x, y))
    p.line(arc, white, 3 * s)
    p.line([(arc[0][0], arc[0][1]), (bx_at(arc[0][1]), arc[0][1])], white, 3 * s)
    p.line([(arc[-1][0], arc[-1][1]), (bx_at(arc[-1][1]), arc[-1][1])], white, 3 * s)
    p.poly(court, None, white, 3 * s)                                    # le tour du terrain
    p.ellipse(-150 * s, hoop_y(0.25, H, s), 150 * s, hoop_y(0.75, H, s), None, white, 3 * s)      # le rond central, coupé
    for _ in range(int(W / (5 * s))):                                    # grain de l'asphalte
        x, y = rng.uniform(0, W), rng.uniform(fy, H)
        p.disc(x, y, rng.uniform(0.6, 1.4) * s, (255, 255, 255, 26))
    for _ in range(int(W / (40 * s))):
        x, y = rng.uniform(0, W), rng.uniform(fy, H)
        p.line([(x, y), (x + rng.uniform(8, 30) * s, y + rng.uniform(-3, 3) * s)], (40, 50, 70, 40), 1.4 * s)
    court_img = p.done()
    sky.paste(court_img, (0, 0), court_img)
    return {"sky": sky, "layers": [], "tw": W, "amb": {}}


# ---------------------------------------------------------------------------- Super Dodge Ball
DODGE_FLOOR = 250        # top of the court in the picture, at s = 1 / haut du terrain dans l'image


def build_dodge_yard(W, H, s, seed=63):
    """Super Dodge Ball: a schoolyard court at the end of the afternoon, as in the game: a wooden fence and the school
    behind, spectators, a ground of gravel with cans lying about, the white lines and the middle line.
    / Une cour d'école en fin d'après-midi, comme dans le jeu : palissade, spectateurs, gravier, boîtes de conserve."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (240, 170, 100)), (0.3, (250, 200, 130)), (1.0, (250, 210, 150))])
    p = _Pic(W, H, 2)
    p.poly([(0, 40 * s), (W, 40 * s), (W, 150 * s), (0, 150 * s)], (190, 150, 110, 255))        # le mur de l'école
    for x in range(0, W, int(140 * s)):                                  # fenêtres
        p.poly([(x + 20 * s, 56 * s), (x + 110 * s, 56 * s), (x + 110 * s, 120 * s), (x + 20 * s, 120 * s)], (120, 150, 170, 255), (90, 70, 50, 255), 2 * s)
        p.line([(x + 65 * s, 56 * s), (x + 65 * s, 120 * s)], (90, 70, 50, 255), 2 * s)
        p.line([(x + 20 * s, 88 * s), (x + 110 * s, 88 * s)], (90, 70, 50, 255), 2 * s)
    p.poly([(0, 30 * s), (W, 30 * s), (W, 44 * s), (0, 44 * s)], (120, 70, 50, 255))
    for x in range(0, W, int(26 * s)):                                   # la palissade
        top = 150 * s - (8 * s if (x // int(26 * s)) % 2 else 0)
        p.poly([(x + 1 * s, top), (x + 24 * s, top), (x + 24 * s, DODGE_FLOOR * s), (x + 1 * s, DODGE_FLOOR * s)], (150, 100, 60, 255), (70, 44, 26, 255), 1.5 * s)
        p.line([(x + 6 * s, top + 10 * s), (x + 6 * s, DODGE_FLOOR * s - 6 * s)], (176, 124, 80, 255), 1.5 * s)
    for k in range(int(W / (52 * s))):                                   # spectateurs derrière la palissade
        cx = 26 * s + k * 52 * s + rng.uniform(-8, 8) * s
        top = rng.uniform(150, 166) * s
        shirt = rng.choice(((60, 80, 150), (240, 240, 240), (200, 60, 50), (60, 120, 70), (40, 40, 50)))
        p.poly([(cx - 18 * s, top + 40 * s), (cx + 18 * s, top + 40 * s), (cx + 16 * s, top + 16 * s), (cx - 16 * s, top + 16 * s)], _rgba(shirt))
        p.disc(cx, top + 4 * s, 13 * s, _rgba(rng.choice(((236, 190, 150), (214, 160, 120), (190, 140, 100)))), (60, 40, 30, 255), 1.4 * s)
        p.chord(cx - 13 * s, top - 9 * s, cx + 13 * s, top + 8 * s, 180, 360, _rgba(rng.choice(((30, 26, 24), (60, 40, 26), (20, 20, 24)))))
    p.poly([(0, 168 * s), (W, 168 * s), (W, 176 * s), (0, 176 * s)], (110, 70, 40, 255))           # la traverse
    fy = DODGE_FLOOR * s                                                 # le sol de gravier
    p.poly([(0, fy), (W, fy), (W, H), (0, H)], (176, 156, 124, 255))
    for _ in range(int(W * (H - fy) / (60 * s * s))):
        x, y = rng.uniform(0, W), rng.uniform(fy, H)
        r = rng.uniform(1.5, 4) * s
        p.ellipse(x - r, y - r * 0.7, x + r, y + r * 0.7, _rgba(rng.choice(((150, 132, 104), (196, 178, 146), (130, 116, 92), (210, 196, 166)))))
    for _ in range(int(W / (90 * s))):                                   # boîtes de conserve qui traînent au bord
        x = rng.uniform(0, W)
        y = rng.choice((fy + 6 * s, H - 8 * s))
        col = rng.choice(((200, 60, 50), (60, 120, 200), (230, 200, 70), (90, 170, 90)))
        p.poly([(x - 6 * s, y - 4 * s), (x + 6 * s, y - 4 * s), (x + 6 * s, y + 4 * s), (x - 6 * s, y + 4 * s)], _rgba(col), (40, 30, 30, 255), 1 * s)
    p.line([(W * 0.04, fy + 14 * s), (W * 0.96, fy + 14 * s)], (250, 250, 244, 255), 3 * s)        # les lignes du terrain
    p.line([(W * 0.02, H - 14 * s), (W * 0.98, H - 14 * s)], (250, 250, 244, 255), 3 * s)
    p.line([(W * 0.5, fy + 14 * s), (W * 0.5, H - 14 * s)], (250, 250, 244, 255), 4 * s)
    for side in (-1, 1):
        x = W * 0.5 + side * W * 0.31
        p.line([(x, fy + 14 * s), (x + side * 10 * s, H - 14 * s)], (250, 250, 244, 200), 2 * s)
    yard = p.done()
    sky.paste(yard, (0, 0), yard)
    return {"sky": sky, "layers": [], "tw": W, "amb": {}}


hd_bg.BUILDERS.update({"s45_ground": build_s45_ground, "hoop_park": build_hoop_park, "dodge_yard": build_dodge_yard})
