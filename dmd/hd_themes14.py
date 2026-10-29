"""Backdrops of the Capcom CPS action, platform and puzzle games (1.30), drawn by the program after screenshots of the
games. Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when
this module is imported (by hd_games14).

Décors des jeux d'action, de plateforme et de réflexion Capcom CPS (1.30), dessinés par le programme d'après des
captures des jeux. Tout est dessiné par le programme, aucune image ne vient d'un jeu.
"""

import math
import random

from . import hd_bg
from .hd_bg import mix, periodic, vgrad
from .hd_themes3 import _clump, _cumulus, _fit, _Pic, _rgba

GG_FLOOR = 386          # Ghouls'n Ghosts: the ground the knight walks on, at s = 1 / le sol où marche le chevalier
ST_FLOOR = 372          # Strider: the roof the ninja runs on / le toit où court le ninja


def _stars(img, W, H, s, rng, n, y1, cols=((255, 255, 255), (200, 220, 255), (255, 230, 190))):
    """Little stars painted in the sky. / De petites étoiles dans le ciel."""
    p = _Pic(W, H, 1)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, y1)
        r = rng.choice((0.8, 1.0, 1.2, 1.8)) * s
        p.disc(x, y, r, _rgba(rng.choice(cols), rng.randint(120, 255)))
    img = img.convert("RGBA")
    img.alpha_composite(p.done())
    return img.convert("RGB")


# ============================================================================ Ghouls'n Ghosts
def build_gg_grave(W, H, s, seed=1401):
    """Ghouls'n Ghosts: the place of the executions of the first round, as in the game: a stormy sky, a ruined castle
    far away, walls of mossy stones fallen apart, the gibbets and their bones, the ladders, the green grass and the
    tombstones in front. / Le lieu des exécutions du premier niveau : ciel d'orage, château en ruine au loin, murs de
    pierres moussues effondrés, gibets et leurs os, échelles, herbe verte et tombes devant."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (22, 24, 48)), (0.45, (52, 50, 84)), (0.8, (96, 82, 96)), (1.0, (60, 50, 60))])
    layers = []
    far = _Pic(tw, H, 2, tw)                                             # les collines et le château au loin
    f = periodic(tw, rng, 5, 1.0)
    far.poly([(0, H)] + [(x, 250 * s + 26 * s * f(x)) for x in range(0, tw + 8, 8)] + [(tw, H)], (34, 36, 58, 255))
    for cx in (tw * 0.18, tw * 0.66):
        base = 250 * s
        far.poly([(cx - 150 * s, base), (cx + 150 * s, base), (cx + 150 * s, base - 70 * s), (cx - 150 * s, base - 70 * s)], (40, 40, 66, 255))
        for k, (dx, h) in enumerate(((-150, 150), (-60, 110), (40, 170), (130, 120))):
            x0 = cx + dx * s
            far.poly([(x0, base), (x0 + 34 * s, base), (x0 + 34 * s, base - h * s), (x0, base - h * s)], (40, 40, 66, 255))
            for j in range(3):                                        # les créneaux, certains tombés
                if rng.random() < 0.7:
                    far.poly([(x0 + j * 12 * s, base - h * s), (x0 + j * 12 * s + 8 * s, base - h * s), (x0 + j * 12 * s + 8 * s, base - h * s - 10 * s),
                              (x0 + j * 12 * s, base - h * s - 10 * s)], (40, 40, 66, 255))
            far.disc(x0 + 17 * s, base - h * s + 30 * s, 4 * s, (255, 200, 90, 160) if k % 2 else (60, 56, 80, 255))
    layers.append({"img": far.done(), "y": 0, "f": 0.18, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)                                             # murs effondrés, gibets, échelles
    stone = ((112, 120, 92), (98, 108, 82), (126, 132, 100), (90, 98, 76))
    x = 40 * s
    while x < tw - 200 * s:
        w = rng.uniform(260, 460) * s
        h = rng.uniform(120, 230) * s
        base = GG_FLOOR * s
        prof = periodic(int(w) + 1, rng, 3, 1.0)
        rows = int(h / (30 * s))
        for r in range(rows):                                         # les blocs, rangée par rangée, le haut éboulé
            y1 = base - r * 30 * s
            y0 = y1 - 30 * s
            off = (r % 2) * 26 * s
            bx = x - off
            while bx < x + w:
                bw = rng.uniform(44, 62) * s
                top_here = base - h + 40 * s * prof(bx - x) + (abs((bx - x) / w - 0.5) * 120 * s)
                if y0 > top_here and bx + bw > x:
                    p0, p1 = max(bx, x), min(bx + bw, x + w)
                    if p1 - p0 > 8 * s:
                        mid.poly([(p0, y0), (p1, y0), (p1, y1), (p0, y1)], _rgba(rng.choice(stone)), (46, 50, 40, 255), 2 * s)
                        if rng.random() < 0.3:                        # la mousse
                            mid.ellipse(p0, y0 - 4 * s, p0 + rng.uniform(16, 40) * s, y0 + 8 * s, (70, 120, 50, 255))
                bx += bw
        if rng.random() < 0.6:                                        # une échelle contre le mur
            lx = x + rng.uniform(0.2, 0.8) * w
            top = base - h * 0.7
            for side in (-14, 14):
                mid.line([(lx + side * s, top), (lx + side * s, base)], (120, 84, 44, 255), 5 * s)
            yy = top + 12 * s
            while yy < base:
                mid.line([(lx - 14 * s, yy), (lx + 14 * s, yy)], (140, 100, 54, 255), 4 * s)
                yy += 22 * s
        x += w + rng.uniform(120, 260) * s
    for k in range(9):                                                   # les gibets et leurs os
        gx = (k + 0.5) * tw / 9 + rng.uniform(-60, 60) * s
        top = rng.uniform(150, 200) * s
        mid.poly([(gx - 7 * s, GG_FLOOR * s), (gx + 7 * s, GG_FLOOR * s), (gx + 6 * s, top), (gx - 6 * s, top)], (92, 62, 38, 255), (40, 26, 16, 255), 2 * s)
        mid.poly([(gx - 6 * s, top), (gx + 56 * s, top), (gx + 56 * s, top + 10 * s), (gx - 6 * s, top + 10 * s)], (92, 62, 38, 255), (40, 26, 16, 255), 2 * s)
        mid.line([(gx + 6 * s, top + 40 * s), (gx + 36 * s, top + 10 * s)], (80, 54, 32, 255), 5 * s)
        hx = gx + 44 * s
        mid.line([(hx, top + 10 * s), (hx, top + 34 * s)], (170, 150, 120, 255), 2 * s)
        bone = (236, 232, 214, 255)
        mid.ellipse(hx - 9 * s, top + 34 * s, hx + 9 * s, top + 52 * s, bone)                 # le crâne
        mid.disc(hx - 3 * s, top + 42 * s, 2.2 * s, (40, 30, 30, 255))
        mid.disc(hx + 3 * s, top + 42 * s, 2.2 * s, (40, 30, 30, 255))
        mid.line([(hx, top + 52 * s), (hx, top + 92 * s)], bone, 4 * s)                         # la colonne
        for j in range(4):                                                                      # les côtes
            mid.line([(hx - 12 * s, top + (58 + j * 7) * s), (hx + 12 * s, top + (58 + j * 7) * s)], bone, 2.5 * s)
        mid.line([(hx, top + 92 * s), (hx - 9 * s, top + 122 * s)], bone, 3 * s)
        mid.line([(hx, top + 92 * s), (hx + 9 * s, top + 122 * s)], bone, 3 * s)
        mid.line([(hx, top + 58 * s), (hx - 14 * s, top + 84 * s)], bone, 2.5 * s)
        mid.line([(hx, top + 58 * s), (hx + 14 * s, top + 84 * s)], bone, 2.5 * s)
    for k in range(6):                                                   # arbres morts
        tx = rng.uniform(0, tw)
        b = GG_FLOOR * s
        mid.poly([(tx - 12 * s, b), (tx + 12 * s, b), (tx + 4 * s, b - 200 * s), (tx - 4 * s, b - 200 * s)], (50, 40, 46, 255))
        for _ in range(5):
            y = b - rng.uniform(100, 190) * s
            d = rng.choice((-1, 1))
            mid.line([(tx, y), (tx + d * rng.uniform(30, 70) * s, y - rng.uniform(20, 50) * s), (tx + d * rng.uniform(70, 110) * s, y - rng.uniform(40, 80) * s)],
                     (50, 40, 46, 255), 5 * s)
    layers.append({"img": mid.done(), "y": 0, "f": 0.55, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)                                            # l'herbe, les tombes, la terre
    fy = GG_FLOOR * s
    near.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (52, 40, 36, 255))
    g = periodic(tw, rng, 6, 1.0)
    near.poly([(0, fy + 16 * s)] + [(x, fy - 4 * s + 4 * s * g(x)) for x in range(0, tw + 8, 8)] + [(tw, fy + 16 * s)], (66, 130, 52, 255))
    for k in range(int(tw / (14 * s))):                                  # les brins d'herbe
        x = k * 14 * s + rng.uniform(-4, 4) * s
        near.line([(x, fy + 6 * s), (x + rng.uniform(-5, 5) * s, fy - rng.uniform(8, 18) * s)], (92, 168, 70, 255), 2.5 * s)
    for k in range(int(tw / (26 * s))):                                  # cailloux dans la terre
        near.disc(rng.uniform(0, tw), rng.uniform(fy + 24 * s, H), rng.uniform(2, 5) * s, (76, 62, 54, 255))
    for k in range(10):                                                  # tombes et croix
        x = rng.uniform(0, tw)
        y = fy + 2 * s
        if k % 3 == 0:
            near.poly([(x - 5 * s, y), (x + 5 * s, y), (x + 5 * s, y - 56 * s), (x - 5 * s, y - 56 * s)], (138, 136, 146, 255), (60, 58, 70, 255), 2 * s)
            near.poly([(x - 20 * s, y - 44 * s), (x + 20 * s, y - 44 * s), (x + 20 * s, y - 35 * s), (x - 20 * s, y - 35 * s)], (138, 136, 146, 255),
                      (60, 58, 70, 255), 2 * s)
        else:
            near.poly([(x - 24 * s, y), (x + 24 * s, y), (x + 24 * s, y - 40 * s), (x, y - 58 * s), (x - 24 * s, y - 40 * s)], (128, 126, 138, 255),
                      (60, 58, 70, 255), 2 * s)
            near.line([(x - 10 * s, y - 36 * s), (x + 10 * s, y - 36 * s)], (90, 88, 100, 255), 2 * s)
        near.ellipse(x - 30 * s, y - 6 * s, x + 30 * s, y + 6 * s, (60, 120, 46, 255))
    for k in range(7):                                                   # crânes dans l'herbe
        x = rng.uniform(0, tw)
        near.ellipse(x - 9 * s, fy - 6 * s, x + 9 * s, fy + 10 * s, (232, 226, 206, 255))
        near.disc(x - 3 * s, fy + 1 * s, 2 * s, (40, 30, 30, 255))
        near.disc(x + 3 * s, fy + 1 * s, 2 * s, (40, 30, 30, 255))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"rain": True, "lightning": True}}


# ============================================================================ Strider
def _bez(p0, p1, p2, p3, n=14):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def _onion(p, cx, base, r, h, col, dark, light, s):
    """An onion dome: round and wider than its foot, pointed at the top, its ribs and a light on its side.
    / Un bulbe : rond et plus large que son pied, pointu en haut, ses côtes et un reflet."""
    def side(k):
        return _bez((0.7 * r * k, 0), (1.3 * r * k, -0.3 * h), (0.55 * r * k, -0.62 * h), (0.0, -h))
    right = side(1.0)
    pts = [(cx + x, base + y) for x, y in right] + [(cx - x, base + y) for x, y in reversed(right)]
    p.poly(pts, _rgba(col), _rgba(dark) if dark else None, 2.5 * s if dark else 0)
    if dark:
        for k in (-0.55, 0.0, 0.55):                                  # les côtes
            p.line([(cx + x * k, base + y) for x, y in right], _rgba(dark), 2 * s)
    if light:
        p.line([(cx - x * 0.75, base + y) for x, y in right[2:9]], _rgba(light, 200), 6 * s)
    if dark:
        p.line([(cx, base - h), (cx, base - h - 26 * s)], _rgba(dark), 4 * s)
        p.disc(cx, base - h - 30 * s, 6 * s, _rgba(col))


def build_st_city(W, H, s, seed=1402):
    """Strider: the city of the first stage at night, as in the game: the starry sky, the golden onion domes on their red
    towers, the green roofs, the lit arches, and the long roof the ninja runs on. / La ville du premier niveau la nuit :
    ciel étoilé, bulbes dorés sur leurs tours rouges, toits verts, arcades éclairées, le long toit où court le ninja."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (4, 6, 20)), (0.6, (14, 18, 46)), (1.0, (40, 30, 60))])
    sky = _stars(sky, W, H, s, rng, 260, H * 0.7)
    layers = []
    far = _Pic(tw, H, 2, tw)                                             # la ville au loin, en silhouette
    x = 0
    while x < tw:
        w = rng.uniform(60, 140) * s
        h = rng.uniform(80, 170) * s
        base = 330 * s
        far.poly([(x, base), (x + w, base), (x + w, base - h), (x, base - h)], (26, 34, 60, 255))
        if rng.random() < 0.6:                                        # un petit bulbe
            r = min(w * 0.4, 34 * s)
            _onion(far, x + w / 2, base - h, r, r * 1.9, (30, 40, 70), None, None, s)
        for _ in range(int(w * h / (900 * s * s))):
            far.disc(x + rng.uniform(6, w - 6), base - rng.uniform(10, h - 10), 2 * s, (255, 200, 110, rng.randint(90, 200)))
        x += w + rng.uniform(10, 50) * s
    layers.append({"img": far.done(), "y": 0, "f": 0.15, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)                                             # les grands bulbes dorés et leurs tours
    gold, gold_d, gold_l = (226, 170, 54), (160, 104, 30), (255, 226, 130)
    red, red_d = (170, 52, 40), (96, 26, 24)
    green = (60, 140, 120)
    for k in range(5):
        cx = (k + 0.5) * tw / 5 + rng.uniform(-80, 80) * s
        base = ST_FLOOR * s
        tw_ = rng.uniform(120, 170) * s
        th = rng.uniform(110, 170) * s
        mid.poly([(cx - tw_ / 2, base), (cx + tw_ / 2, base), (cx + tw_ / 2, base - th), (cx - tw_ / 2, base - th)], _rgba(red), _rgba(red_d), 2 * s)
        for j in range(3):                                            # les arcades éclairées
            ax = cx - tw_ / 2 + (j + 0.5) * tw_ / 3
            mid.poly([(ax - 12 * s, base - 30 * s), (ax + 12 * s, base - 30 * s), (ax + 12 * s, base - th + 40 * s), (ax - 12 * s, base - th + 40 * s)],
                     (255, 196, 90, 255))
            mid.disc(ax, base - th + 40 * s, 12 * s, (255, 196, 90, 255))
        mid.poly([(cx - tw_ / 2 - 10 * s, base - th), (cx + tw_ / 2 + 10 * s, base - th), (cx + tw_ / 2, base - th - 18 * s),
                  (cx - tw_ / 2, base - th - 18 * s)], _rgba(green), (30, 70, 60, 255), 2 * s)
        top = base - th - 18 * s
        _onion(mid, cx, top, tw_ * 0.5, tw_ * 0.95, gold, gold_d, gold_l, s)
    layers.append({"img": mid.done(), "y": 0, "f": 0.45, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)                                            # le toit où court le ninja
    fy = ST_FLOOR * s
    near.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (70, 40, 44, 255))
    near.poly([(0, fy), (tw, fy), (tw, fy + 16 * s), (0, fy + 16 * s)], (120, 150, 140, 255), (40, 60, 56, 255), 2 * s)
    for k in range(int(tw / (36 * s))):                                  # les tuiles du toit
        x = k * 36 * s
        near.line([(x, fy + 18 * s), (x - 30 * s, H)], (96, 54, 56, 255), 3 * s)
    for k in range(int(tw / (240 * s))):                                 # les ornements dorés de la corniche
        x = k * 240 * s + 60 * s
        near.poly([(x - 18 * s, fy + 16 * s), (x + 18 * s, fy + 16 * s), (x, fy + 44 * s)], _rgba(gold), _rgba(gold_d), 2 * s)
        near.disc(x, fy + 8 * s, 6 * s, _rgba(gold_l))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ============================================================================ Pang! 3 and Mighty! Pang
PG_FLOOR = 392          # the floor of the balloons games, at s = 1 / le sol des jeux de ballons


def build_pg_temple(W, H, s, seed=1403):
    """Pang! 3: a stage of the game in Egypt, as in the game: a great painted wall of the temple, its sandstone blocks,
    the frieze of signs of our own, a huge eye in the middle, the columns at the sides and the floor of slabs.
    / Un niveau du jeu en Égypte : le grand mur peint du temple, la frise de signes à nous, un œil immense au milieu."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (120, 70, 40)), (1.0, (90, 50, 30))])
    p = _Pic(W, H, 2)
    sand, sand_d, paint = (196, 150, 90), (150, 106, 60), (40, 70, 140)
    for row in range(int(H / (46 * s)) + 1):                             # les blocs de grès
        off = (row % 2) * 60 * s
        for k in range(int(W / (120 * s)) + 2):
            x0 = k * 120 * s - off
            y0 = row * 46 * s
            tone = mix(sand, sand_d, rng.uniform(0, 0.35))
            p.poly([(x0, y0), (x0 + 118 * s, y0), (x0 + 118 * s, y0 + 44 * s), (x0, y0 + 44 * s)], _rgba(tone), _rgba(sand_d), 1.5 * s)
    for y in (40 * s, (PG_FLOOR - 50) * s):                              # les frises
        p.poly([(0, y), (W, y), (W, y + 30 * s), (0, y + 30 * s)], (60, 100, 170, 255), (30, 40, 80, 255), 2 * s)
        for k in range(int(W / (40 * s))):
            x = k * 40 * s + 20 * s
            sh = k % 4
            col = (240, 200, 70, 255) if sh % 2 == 0 else (200, 60, 50, 255)
            if sh == 0:
                p.disc(x, y + 15 * s, 8 * s, col)
            elif sh == 1:
                p.poly([(x - 9 * s, y + 24 * s), (x, y + 5 * s), (x + 9 * s, y + 24 * s)], col)
            elif sh == 2:
                p.line([(x - 9 * s, y + 15 * s), (x + 9 * s, y + 15 * s)], col, 4 * s)
                p.line([(x, y + 6 * s), (x, y + 24 * s)], col, 4 * s)
            else:
                p.poly([(x - 8 * s, y + 6 * s), (x + 8 * s, y + 6 * s), (x + 8 * s, y + 24 * s), (x - 8 * s, y + 24 * s)], col)
    cx, cy = W / 2, 200 * s                                              # l'œil immense
    p.ellipse(cx - 230 * s, cy - 80 * s, cx + 230 * s, cy + 80 * s, (240, 230, 200, 255), (30, 30, 60, 255), 10 * s)
    p.disc(cx, cy, 70 * s, _rgba(paint))
    p.disc(cx, cy, 32 * s, (20, 20, 30, 255))
    p.disc(cx - 22 * s, cy - 24 * s, 12 * s, (255, 255, 255, 255))
    p.line([(cx - 260 * s, cy - 110 * s), (cx, cy - 140 * s), (cx + 260 * s, cy - 110 * s)], (30, 30, 60, 255), 14 * s)
    p.line([(cx - 40 * s, cy + 78 * s), (cx - 40 * s, cy + 150 * s)], (30, 30, 60, 255), 12 * s)      # la larme et la spirale
    p.disc(cx - 40 * s, cy + 156 * s, 14 * s, (30, 30, 60, 255))
    spiral = [(cx + 80 * s + math.cos(a / 10) * (60 - a) * s * 0.9, cy + 120 * s + math.sin(a / 10) * (60 - a) * s * 0.6) for a in range(0, 50, 2)]
    p.line([(cx + 60 * s, cy + 70 * s)] + spiral, (30, 30, 60, 255), 10 * s)
    for side in (0, 1):                                                  # les colonnes
        x0 = 30 * s if side == 0 else W - 130 * s
        p.poly([(x0, 0), (x0 + 100 * s, 0), (x0 + 100 * s, PG_FLOOR * s), (x0, PG_FLOOR * s)], (210, 170, 110, 255), (120, 80, 40, 255), 3 * s)
        for k in range(4):
            p.line([(x0 + (20 + k * 20) * s, 0), (x0 + (20 + k * 20) * s, PG_FLOOR * s)], (170, 126, 76, 255), 3 * s)
        p.poly([(x0 - 14 * s, 0), (x0 + 114 * s, 0), (x0 + 100 * s, 36 * s), (x0, 36 * s)], (60, 120, 90, 255), (30, 60, 40, 255), 3 * s)
    for k in range(24):                                                  # oiseaux et signes peints
        x, y = rng.uniform(170 * s, W - 170 * s), rng.uniform(100, 290) * s
        if abs(x - cx) < 300 * s:
            continue
        p.ellipse(x - 18 * s, y - 10 * s, x + 18 * s, y + 10 * s, (40, 60, 120, 255))
        p.disc(x - 18 * s, y - 8 * s, 8 * s, (40, 60, 120, 255))
        p.poly([(x - 28 * s, y - 8 * s), (x - 40 * s, y - 4 * s), (x - 28 * s, y - 2 * s)], (240, 200, 70, 255))
        p.line([(x - 4 * s, y + 10 * s), (x - 8 * s, y + 28 * s)], (40, 60, 120, 255), 3 * s)
        p.line([(x + 6 * s, y + 10 * s), (x + 8 * s, y + 28 * s)], (40, 60, 120, 255), 3 * s)
    fy = PG_FLOOR * s                                                    # le sol de dalles
    p.poly([(0, fy), (W, fy), (W, H), (0, H)], (120, 84, 50, 255))
    for k in range(int(W / (80 * s)) + 1):
        p.line([(k * 80 * s, fy), (k * 80 * s - 20 * s, H)], (90, 60, 34, 255), 3 * s)
    p.line([(0, fy), (W, fy)], (230, 190, 120, 255), 4 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_pg_peak(W, H, s, seed=1404):
    """Mighty! Pang: the highest mountain of the world, as in the game: a deep blue sky, the great snowy peak and its
    ridges, the clouds below the summit, the snow on the ground. / La plus haute montagne du monde : ciel bleu profond,
    le grand pic enneigé et ses arêtes, les nuages sous le sommet, la neige au sol."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (16, 50, 140)), (0.6, (70, 130, 210)), (1.0, (170, 200, 240))])
    p = _Pic(W, H, 2)
    cx = W * 0.5
    peak = [(cx - 900 * s, PG_FLOOR * s), (cx - 420 * s, 220 * s), (cx - 250 * s, 160 * s), (cx - 120 * s, 110 * s), (cx, 30 * s),
            (cx + 90 * s, 90 * s), (cx + 260 * s, 140 * s), (cx + 520 * s, 230 * s), (cx + 1000 * s, PG_FLOOR * s)]
    p.poly(peak, (90, 96, 120, 255))
    p.poly([(cx, 30 * s), (cx + 90 * s, 90 * s), (cx + 260 * s, 140 * s), (cx + 520 * s, 230 * s), (cx + 1000 * s, PG_FLOOR * s),
            (cx + 200 * s, PG_FLOOR * s), (cx + 40 * s, 200 * s)], (64, 70, 96, 255))               # le flanc à l'ombre
    snow = [(cx - 420 * s, 220 * s), (cx - 250 * s, 160 * s), (cx - 120 * s, 110 * s), (cx, 30 * s), (cx + 90 * s, 90 * s), (cx + 260 * s, 140 * s),
            (cx + 300 * s, 200 * s), (cx + 160 * s, 170 * s), (cx + 60 * s, 210 * s), (cx - 40 * s, 150 * s), (cx - 140 * s, 220 * s),
            (cx - 260 * s, 210 * s), (cx - 330 * s, 260 * s)]
    p.poly(snow, (246, 248, 255, 255))
    for k in range(7):                                                   # les crevasses dans la neige
        x = cx + rng.uniform(-260, 220) * s
        y = rng.uniform(120, 190) * s
        p.line([(x, y), (x + rng.uniform(-30, 30) * s, y + rng.uniform(25, 50) * s)], (190, 200, 226, 255), 3 * s)
    for side in (-1, 1):                                                 # des sommets plus bas de chaque côté
        bx = cx + side * 760 * s
        p.poly([(bx - 300 * s, PG_FLOOR * s), (bx, 200 * s), (bx + 300 * s, PG_FLOOR * s)], (110, 120, 150, 255))
        p.poly([(bx - 80 * s, 250 * s), (bx, 200 * s), (bx + 80 * s, 250 * s), (bx + 20 * s, 240 * s)], (246, 248, 255, 255))
    for _ in range(8):                                                   # les nuages sous le sommet
        x, y = rng.uniform(0, W), rng.uniform(250, 330) * s
        for k in range(5):
            p.disc(x + (k - 2) * 34 * s, y + rng.uniform(-8, 8) * s, rng.uniform(26, 40) * s, (255, 255, 255, 210))
    fy = PG_FLOOR * s
    p.poly([(0, fy), (W, fy), (W, H), (0, H)], (236, 242, 252, 255))
    p.line([(0, fy), (W, fy)], (180, 196, 230, 255), 4 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {"snow": True}}


# ============================================================================ Super Puzzle Fighter II Turbo
SPF_CELL = 30           # a gem of the wells / une gemme des puits
SPF_TOP = 86            # top of the wells / haut des puits
SPF_ROWS, SPF_COLS = 12, 6


def build_spf_hall(W, H, s, seed=1405):
    """Super Puzzle Fighter II Turbo: the hall of the fights, as in the game: walls of dark wood and their pillars,
    paper doors lit from behind, red lanterns, the polished floor; the two wells of gems in their golden frames at the
    sides. / La salle des combats : murs de bois sombre et leurs piliers, portes de papier éclairées par derrière,
    lanternes rouges, parquet ciré ; les deux puits de gemmes dans leurs cadres dorés sur les côtés."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (60, 30, 20)), (1.0, (100, 56, 30))])
    p = _Pic(W, H, 2)
    for k in range(int(W / (160 * s)) + 1):                              # les portes de papier entre les piliers
        x0 = k * 160 * s
        p.poly([(x0 + 14 * s, 60 * s), (x0 + 146 * s, 60 * s), (x0 + 146 * s, 330 * s), (x0 + 14 * s, 330 * s)], (250, 220, 160, 255))
        for j in range(1, 4):
            p.line([(x0 + 14 * s + j * 33 * s, 60 * s), (x0 + 14 * s + j * 33 * s, 330 * s)], (120, 70, 40, 255), 3 * s)
        for j in range(1, 6):
            p.line([(x0 + 14 * s, 60 * s + j * 45 * s), (x0 + 146 * s, 60 * s + j * 45 * s)], (120, 70, 40, 255), 3 * s)
        p.poly([(x0 - 10 * s, 0), (x0 + 14 * s, 0), (x0 + 14 * s, 340 * s), (x0 - 10 * s, 340 * s)], (70, 36, 20, 255), (40, 20, 10, 255), 2 * s)
    p.poly([(0, 0), (W, 0), (W, 60 * s), (0, 60 * s)], (80, 40, 24, 255), (40, 20, 10, 255), 2 * s)        # la poutre du haut
    for k in range(int(W / (40 * s)) + 1):
        p.line([(k * 40 * s, 0), (k * 40 * s, 60 * s)], (60, 30, 18, 255), 2 * s)
    for k in range(6):                                                   # les lanternes rouges
        x = (k + 0.5) * W / 6
        p.line([(x, 60 * s), (x, 90 * s)], (40, 20, 10, 255), 3 * s)
        p.ellipse(x - 26 * s, 90 * s, x + 26 * s, 150 * s, (220, 50, 40, 255), (120, 20, 20, 255), 2 * s)
        p.ellipse(x - 14 * s, 100 * s, x + 6 * s, 136 * s, (255, 140, 90, 200))
        p.poly([(x - 14 * s, 146 * s), (x + 14 * s, 146 * s), (x + 10 * s, 156 * s), (x - 10 * s, 156 * s)], (40, 20, 10, 255))
    fy = 340 * s                                                         # le parquet
    p.poly([(0, fy), (W, fy), (W, H), (0, H)], (150, 90, 50, 255))
    for k in range(8):
        y = fy + (k + 1) * (H - fy) / 8
        p.line([(0, y), (W, y)], (120, 70, 36, 255), 2 * s)
    for k in range(40):
        x = rng.uniform(0, W)
        p.line([(x, fy + rng.uniform(0, H - fy)), (x + 60 * s, fy + rng.uniform(0, H - fy))], (170, 110, 64, 255), 2 * s)
    for side in (0, 1):                                                  # les puits dans leurs cadres dorés
        x0 = (150 if side == 0 else W / s - 150 - SPF_COLS * SPF_CELL) * s
        w, h = SPF_COLS * SPF_CELL * s, SPF_ROWS * SPF_CELL * s
        y0 = SPF_TOP * s
        p.poly([(x0 - 14 * s, y0 - 14 * s), (x0 + w + 14 * s, y0 - 14 * s), (x0 + w + 14 * s, y0 + h + 10 * s), (x0 - 14 * s, y0 + h + 10 * s)],
               (230, 180, 60, 255), (120, 80, 20, 255), 3 * s)
        p.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], (20, 16, 40, 255))
        for c in range(1, SPF_COLS):
            p.line([(x0 + c * SPF_CELL * s, y0), (x0 + c * SPF_CELL * s, y0 + h)], (36, 30, 64, 255), 1.5 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


# ============================================================================ Mega Twins
MT_FLOOR = 384          # the grass the twin walks on / l'herbe où marche le jumeau


def build_mt_forest(W, H, s, seed=1406):
    """Mega Twins: the forest of the first stage, as in the game: a bright blue sky and white clouds, little floating
    islands far away, big round trees with a kind face of their own, the green grass and its flowers.
    / La forêt du premier niveau : ciel bleu vif, nuages blancs, petites îles volantes, grands arbres ronds au visage
    gentil, herbe verte et fleurs."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (60, 130, 230)), (0.7, (140, 200, 250)), (1.0, (190, 230, 255))])
    layers = [{"img": _cumulus(tw, int(H * 0.6), s, rng, 9, ((255, 255, 255), (236, 244, 255), (200, 220, 245)), 40 * s, 170 * s), "y": 0, "f": 0.1,
               "stage": "clouds"}]
    far = _Pic(tw, H, 2, tw)                                             # les îles volantes au loin
    for k in range(6):
        x, y = rng.uniform(0, tw), rng.uniform(140, 230) * s
        w = rng.uniform(70, 130) * s
        far.poly([(x - w, y), (x + w, y), (x + w * 0.4, y + w * 0.7), (x, y + w), (x - w * 0.5, y + w * 0.6)], (150, 120, 90, 255))
        far.ellipse(x - w * 1.05, y - 14 * s, x + w * 1.05, y + 12 * s, (80, 180, 70, 255))
    layers.append({"img": far.done(), "y": 0, "f": 0.25, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)                                             # les grands arbres au visage gentil
    x = 80 * s
    while x < tw - 60 * s:
        r = rng.uniform(110, 150) * s
        base = MT_FLOOR * s
        tr = rng.uniform(46, 60) * s
        mid.poly([(x - tr, base), (x + tr, base), (x + tr * 0.8, base - 200 * s), (x - tr * 0.8, base - 200 * s)], (150, 100, 56, 255),
                 (90, 56, 30, 255), 2.5 * s)
        for side in (-1, 1):                                          # les racines
            mid.poly([(x + side * tr, base), (x + side * (tr + 26 * s), base), (x + side * tr * 0.6, base - 40 * s)], (150, 100, 56, 255))
        fy = base - 120 * s                                           # le visage
        for ex in (-0.4, 0.4):
            mid.ellipse(x + ex * tr - 9 * s, fy - 14 * s, x + ex * tr + 9 * s, fy + 14 * s, (255, 255, 255, 255), (60, 36, 20, 255), 2 * s)
            mid.disc(x + ex * tr + 2 * s, fy + 3 * s, 5 * s, (40, 24, 14, 255))
        mid.chord(x - 18 * s, fy + 14 * s, x + 18 * s, fy + 40 * s, 0, 180, (110, 40, 30, 255))
        cy = base - 200 * s - r * 0.55
        _clump(mid, x, cy, r, rng, ((40, 130, 50), (70, 180, 60), (150, 230, 110)), n=11, spread=(1.1, 0.75))
        x += r * 2 + rng.uniform(140, 320) * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.55, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)                                            # l'herbe et les fleurs
    fy = MT_FLOOR * s
    near.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (150, 100, 50, 255))
    g = periodic(tw, rng, 5, 1.0)
    near.poly([(0, fy + 20 * s)] + [(x, fy - 6 * s + 3 * s * g(x)) for x in range(0, tw + 8, 8)] + [(tw, fy + 20 * s)], (90, 190, 60, 255))
    near.line([(x, fy - 6 * s + 3 * s * g(x)) for x in range(0, tw + 8, 8)], (150, 230, 100, 255), 4 * s)
    for k in range(int(tw / (60 * s))):
        x = rng.uniform(0, tw)
        y = fy + rng.uniform(-2, 8) * s
        col = rng.choice(((255, 90, 120), (255, 230, 80), (255, 255, 255), (120, 160, 255)))
        for j in range(5):
            a = j * math.tau / 5
            near.disc(x + math.cos(a) * 4 * s, y + math.sin(a) * 4 * s, 3.2 * s, _rgba(col))
        near.disc(x, y, 2.4 * s, (255, 200, 60, 255))
    for k in range(int(tw / (40 * s))):                                  # cailloux dans la terre
        near.disc(rng.uniform(0, tw), rng.uniform(fy + 30 * s, H), rng.uniform(3, 6) * s, (120, 80, 40, 255))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ============================================================================ Magic Sword
MS_FLOOR = 382          # the floor of the tower / le sol de la tour


def build_ms_tower(W, H, s, seed=1407):
    """Magic Sword: a floor of the tower, as in the game: the great wall of grey stones, the arched windows on the night,
    the statues of monsters in their niches, the torches, the floor of flagstones. / Un étage de la tour : le grand mur
    de pierres grises, les fenêtres en arc sur la nuit, les statues de monstres dans leurs niches, les torches, le dallage."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (40, 44, 60)), (1.0, (60, 62, 76))])
    layers = []
    wall = _Pic(tw, H, 2, tw)
    stone = ((100, 104, 120), (88, 92, 108), (112, 116, 130), (80, 84, 98))
    for row in range(int(MS_FLOOR * s / (36 * s)) + 1):                  # le mur de blocs
        off = (row % 2) * 40 * s
        y0 = row * 36 * s
        for k in range(int(tw / (80 * s)) + 2):
            x0 = k * 80 * s - off
            wall.poly([(x0, y0), (x0 + 78 * s, y0), (x0 + 78 * s, y0 + 34 * s), (x0, y0 + 34 * s)], _rgba(rng.choice(stone)), (50, 52, 64, 255), 1.5 * s)
    for k in range(4):                                                   # fenêtres en arc et niches
        cx = (k + 0.5) * tw / 4
        if k % 2 == 0:
            wall.poly([(cx - 60 * s, 130 * s), (cx + 60 * s, 130 * s), (cx + 60 * s, 300 * s), (cx - 60 * s, 300 * s)], (20, 24, 50, 255))
            wall.disc(cx, 130 * s, 60 * s, (20, 24, 50, 255))
            for j in range(6):
                wall.disc(cx + rng.uniform(-50, 50) * s, rng.uniform(100, 290) * s, 1.6 * s, (230, 230, 255, 255))
            wall.disc(cx + 24 * s, 150 * s, 16 * s, (240, 236, 200, 255))
            wall.line([(cx, 70 * s), (cx, 300 * s)], (70, 60, 50, 255), 6 * s)
            wall.line([(cx - 60 * s, 200 * s), (cx + 60 * s, 200 * s)], (70, 60, 50, 255), 6 * s)
        else:                                                         # une niche et sa statue de monstre
            wall.poly([(cx - 70 * s, 110 * s), (cx + 70 * s, 110 * s), (cx + 70 * s, 320 * s), (cx - 70 * s, 320 * s)], (50, 52, 64, 255))
            wall.disc(cx, 110 * s, 70 * s, (50, 52, 64, 255))
            st, st_d = (150, 150, 140, 255), (90, 90, 86, 255)
            wall.poly([(cx - 40 * s, 320 * s), (cx + 40 * s, 320 * s), (cx + 30 * s, 200 * s), (cx - 30 * s, 200 * s)], st, st_d, 2 * s)
            wall.ellipse(cx - 30 * s, 130 * s, cx + 30 * s, 210 * s, st, st_d, 2 * s)
            for side in (-1, 1):                                      # cornes et ailes de pierre
                wall.poly([(cx + side * 20 * s, 140 * s), (cx + side * 44 * s, 96 * s), (cx + side * 30 * s, 150 * s)], st, st_d, 2 * s)
                wall.poly([(cx + side * 30 * s, 210 * s), (cx + side * 66 * s, 150 * s), (cx + side * 60 * s, 250 * s)], st, st_d, 2 * s)
            for ex in (-12, 12):
                wall.disc(cx + ex * s, 168 * s, 6 * s, (255, 60, 40, 255))
        tx = cx + tw / 8                                              # une torche entre les deux
        wall.poly([(tx - 8 * s, 200 * s), (tx + 8 * s, 200 * s), (tx + 5 * s, 250 * s), (tx - 5 * s, 250 * s)], (110, 70, 40, 255))
        wall.ellipse(tx - 16 * s, 160 * s, tx + 16 * s, 206 * s, (255, 130, 40, 255))
        wall.ellipse(tx - 8 * s, 176 * s, tx + 8 * s, 204 * s, (255, 230, 120, 255))
    fy = MS_FLOOR * s                                                    # le dallage
    wall.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (70, 66, 74, 255))
    for k in range(int(tw / (70 * s)) + 1):
        wall.line([(k * 70 * s, fy), (k * 70 * s - 30 * s, H)], (50, 46, 54, 255), 3 * s)
    wall.line([(0, fy), (tw, fy)], (140, 140, 150, 255), 4 * s)
    layers.append({"img": wall.done(), "y": 0, "f": 1.0, "stage": "wall"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"dust": (255, 180, 100)}}


# ============================================================================ Willow
WL_FLOOR = 384          # the cobbles of the village / les pavés du village


def build_wl_village(W, H, s, seed=1408):
    """Willow: the village of the first stage, as in the game: the houses of timber and white plaster, their wooden
    balconies and red roofs, the stone walls below, a great old tree, the cobbled street. / Le village du premier niveau :
    maisons à colombages, balcons de bois et toits rouges, murs de pierre en bas, un grand vieil arbre, la rue pavée."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (110, 170, 230)), (1.0, (200, 225, 245))])
    layers = [{"img": _cumulus(tw, int(H * 0.5), s, rng, 7, ((255, 255, 255), (236, 244, 255), (205, 220, 240)), 40 * s, 140 * s), "y": 0, "f": 0.1,
               "stage": "clouds"}]
    mid = _Pic(tw, H, 2, tw)
    x = 0.0
    beam, plaster, stone = (96, 60, 34), (236, 226, 196), ((140, 136, 126), (124, 120, 112), (156, 150, 138))
    while x < tw:
        w = rng.uniform(260, 380) * s
        base = WL_FLOOR * s
        top = base - rng.uniform(230, 300) * s
        mid.poly([(x, base), (x + w, base), (x + w, base - 90 * s), (x, base - 90 * s)], (130, 126, 118, 255))     # le soubassement de pierre
        for row in range(3):
            for k in range(int(w / (44 * s)) + 1):
                bx = x + k * 44 * s + (row % 2) * 22 * s
                if bx + 40 * s > x + w:
                    continue
                y0 = base - (row + 1) * 30 * s
                mid.poly([(bx, y0), (bx + 40 * s, y0), (bx + 40 * s, y0 + 28 * s), (bx, y0 + 28 * s)], _rgba(rng.choice(stone)), (80, 76, 70, 255), 1.5 * s)
        mid.poly([(x, base - 90 * s), (x + w, base - 90 * s), (x + w, top), (x, top)], _rgba(plaster), _rgba(beam), 3 * s)   # le colombage
        for k in range(int(w / (70 * s)) + 1):
            mid.line([(x + k * 70 * s, base - 90 * s), (x + k * 70 * s, top)], _rgba(beam), 7 * s)
        mid.line([(x, (base - 90 * s + top) / 2), (x + w, (base - 90 * s + top) / 2)], _rgba(beam), 7 * s)
        for k in range(int(w / (140 * s))):
            cx0 = x + k * 140 * s
            mid.line([(cx0, base - 90 * s), (cx0 + 70 * s, (base - 90 * s + top) / 2)], _rgba(beam), 5 * s)
        wy = (base - 90 * s + top) / 2 - 70 * s
        for k in range(int(w / (110 * s))):                           # les fenêtres et leur balcon
            wx = x + 40 * s + k * 110 * s
            mid.poly([(wx, wy), (wx + 46 * s, wy), (wx + 46 * s, wy + 56 * s), (wx, wy + 56 * s)], (60, 50, 50, 255), _rgba(beam), 3 * s)
            mid.poly([(wx - 14 * s, wy + 56 * s), (wx + 60 * s, wy + 56 * s), (wx + 60 * s, wy + 64 * s), (wx - 14 * s, wy + 64 * s)], (120, 76, 40, 255))
            for j in range(6):
                mid.line([(wx - 10 * s + j * 13 * s, wy + 64 * s), (wx - 10 * s + j * 13 * s, wy + 92 * s)], (120, 76, 40, 255), 3 * s)
            mid.line([(wx - 14 * s, wy + 92 * s), (wx + 60 * s, wy + 92 * s)], (120, 76, 40, 255), 4 * s)
        mid.poly([(x - 20 * s, top + 4 * s), (x + w + 20 * s, top + 4 * s), (x + w * 0.5, top - 110 * s)], (180, 70, 50, 255), (100, 36, 26, 255), 3 * s)
        for k in range(8):                                            # les tuiles du toit
            t = (k + 1) / 9
            mid.line([(x - 20 * s + (w * 0.5 + 20 * s) * t, top + 4 * s - 114 * s * t), (x + w + 20 * s - (w * 0.5 + 20 * s) * t, top + 4 * s - 114 * s * t)],
                     (150, 56, 40, 255), 2 * s)
        x += w + rng.uniform(40, 160) * s
        if rng.random() < 0.4 and x < tw - 200 * s:                   # un grand vieil arbre entre deux maisons
            tx = x + 60 * s
            mid.poly([(tx - 40 * s, base), (tx + 40 * s, base), (tx + 26 * s, base - 260 * s), (tx - 26 * s, base - 260 * s)], (110, 80, 50, 255),
                     (60, 40, 24, 255), 2 * s)
            _clump(mid, tx, base - 300 * s, 120 * s, rng, ((50, 110, 50), (80, 150, 60), (140, 200, 90)), n=10)
            x += 160 * s
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)                                            # la rue pavée
    fy = WL_FLOOR * s
    near.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (120, 110, 100, 255))
    for row in range(4):
        y0 = fy + row * 20 * s
        for k in range(int(tw / (36 * s)) + 1):
            bx = k * 36 * s + (row % 2) * 18 * s
            near.ellipse(bx, y0 + 2 * s, bx + 32 * s, y0 + 18 * s, _rgba(rng.choice(((150, 140, 128), (136, 126, 116), (164, 154, 140)))))
    near.line([(0, fy), (tw, fy)], (90, 84, 76, 255), 4 * s)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ============================================================================ Nemo
NM_FLOOR = 380          # the floor of the palace of dreams / le sol du palais des rêves


def build_nm_dream(W, H, s, seed=1409):
    """Nemo: the palace of the land of dreams, as in the game: a sky of lilac and stars, a great crescent moon, the long
    gallery of pale blue arches and their columns, the domes, the striped floor like a sweet. / Le palais du pays des
    rêves : ciel lilas étoilé, grand croissant de lune, la longue galerie d'arcades bleu pâle, les dômes, le sol rayé."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (70, 60, 140)), (0.6, (170, 140, 210)), (1.0, (240, 200, 230))])
    sky = _stars(sky, W, H, s, rng, 120, H * 0.5, ((255, 255, 230), (255, 230, 250)))
    layers = []
    far = _Pic(tw, H, 2, tw)
    for k in range(3):                                                   # la lune et les dômes au loin
        cx = (k + 0.3) * tw / 3
        far.disc(cx, 90 * s, 50 * s, (255, 246, 200, 255))
        far.disc(cx + 22 * s, 80 * s, 46 * s, (0, 0, 0, 0))
    for k in range(7):
        cx = rng.uniform(0, tw)
        r = rng.uniform(40, 70) * s
        far.poly([(cx - r, 300 * s), (cx + r, 300 * s), (cx + r, 200 * s), (cx - r, 200 * s)], (190, 180, 230, 255))
        far.chord(cx - r, 200 * s - r, cx + r, 200 * s + r, 180, 360, (210, 200, 245, 255))
        far.line([(cx, 200 * s - r), (cx, 200 * s - r - 30 * s)], (190, 180, 230, 255), 4 * s)
    layers.append({"img": far.done(), "y": 0, "f": 0.2, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)                                             # la galerie d'arcades
    base = NM_FLOOR * s
    span = 150 * s
    top = 150 * s
    mid.poly([(0, top - 40 * s), (tw, top - 40 * s), (tw, top), (0, top)], (170, 196, 236, 255), (110, 130, 190, 255), 2 * s)
    for k in range(int(tw / span) + 1):
        x0 = k * span
        mid.poly([(x0, top), (x0 + 26 * s, top), (x0 + 26 * s, base), (x0, base)], (226, 236, 255, 255), (120, 140, 200, 255), 2 * s)   # la colonne
        mid.poly([(x0 - 8 * s, base - 16 * s), (x0 + 34 * s, base - 16 * s), (x0 + 34 * s, base), (x0 - 8 * s, base)], (200, 214, 250, 255))
        mid.poly([(x0 - 8 * s, top), (x0 + 34 * s, top), (x0 + 34 * s, top + 16 * s), (x0 - 8 * s, top + 16 * s)], (200, 214, 250, 255))
        mid.chord(x0 + 26 * s, top + 16 * s, x0 + span, top + 16 * s + (span - 26 * s), 180, 360, (170, 196, 236, 255))
        mid.chord(x0 + 40 * s, top + 30 * s, x0 + span - 14 * s, top + 30 * s + (span - 54 * s), 180, 360, (0, 0, 0, 0))
        for j in range(5):                                            # les fanions
            fx = x0 + 30 * s + j * 24 * s
            mid.poly([(fx, top - 40 * s), (fx + 20 * s, top - 40 * s), (fx + 10 * s, top - 18 * s)], _rgba(((255, 120, 160), (255, 220, 90),
                                                                                                         (120, 200, 255))[j % 3]))
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)                                            # le sol rayé comme un bonbon
    fy = NM_FLOOR * s
    near.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (250, 240, 250, 255))
    for k in range(int(tw / (40 * s)) + 1):
        x0 = k * 40 * s
        near.poly([(x0, fy), (x0 + 20 * s, fy), (x0 - 10 * s, H), (x0 - 30 * s, H)], (240, 110, 150, 255))
    near.line([(0, fy), (tw, fy)], (150, 90, 160, 255), 5 * s)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


# ============================================================================ Three Wonders
TW_FLOOR = 382          # the grass of the forest / l'herbe de la forêt


def build_tw_woods(W, H, s, seed=1410):
    """Three Wonders (Midnight Wanderers): the forest of the first stage, as in the game: orange rocks and cliffs at the
    back, tall thin trees, ledges of grass, the mossy ground. / La forêt du premier niveau : rochers et falaises orange
    au fond, grands arbres minces, corniches d'herbe, sol moussu."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (60, 30, 30)), (0.5, (140, 70, 40)), (1.0, (90, 50, 30))])
    layers = []
    far = _Pic(tw, H, 2, tw)                                             # falaises orange
    f = periodic(tw, rng, 6, 1.0)
    far.poly([(0, H)] + [(x, 120 * s + 60 * s * f(x)) for x in range(0, tw + 8, 8)] + [(tw, H)], (180, 96, 46, 255))
    g = periodic(tw, rng, 6, 1.0)
    far.poly([(0, H)] + [(x, 220 * s + 40 * s * g(x)) for x in range(0, tw + 8, 8)] + [(tw, H)], (150, 76, 38, 255))
    for _ in range(40):                                                  # les cassures de la roche
        x, y = rng.uniform(0, tw), rng.uniform(150, 360) * s
        far.line([(x, y), (x + rng.uniform(-20, 20) * s, y + rng.uniform(20, 50) * s)], (120, 60, 30, 255), 3 * s)
    layers.append({"img": far.done(), "y": 0, "f": 0.2, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)                                             # les grands arbres minces et les corniches
    for k in range(int(tw / (150 * s))):
        x = k * 150 * s + rng.uniform(-40, 40) * s
        w = rng.uniform(16, 26) * s
        mid.poly([(x - w, TW_FLOOR * s), (x + w, TW_FLOOR * s), (x + w * 0.7, 0), (x - w * 0.7, 0)], (70, 44, 30, 255), (40, 24, 16, 255), 2 * s)
        mid.line([(x - w * 0.2, TW_FLOOR * s), (x - w * 0.1, 0)], (100, 66, 44, 255), 3 * s)
        if rng.random() < 0.6:
            by = rng.uniform(120, 260) * s
            mid.line([(x, by), (x + rng.choice((-1, 1)) * rng.uniform(40, 80) * s, by - 30 * s)], (70, 44, 30, 255), 6 * s)
    for _ in range(5):                                                   # corniches d'herbe
        x, y = rng.uniform(0, tw), rng.uniform(200, 300) * s
        w = rng.uniform(120, 220) * s
        mid.poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2 - 20 * s, y + 30 * s), (x - w / 2 + 20 * s, y + 30 * s)], (110, 70, 40, 255))
        mid.ellipse(x - w / 2 - 6 * s, y - 10 * s, x + w / 2 + 6 * s, y + 10 * s, (60, 150, 60, 255))
    layers.append({"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    fy = TW_FLOOR * s
    near.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (90, 56, 34, 255))
    h = periodic(tw, rng, 5, 1.0)
    near.poly([(0, fy + 16 * s)] + [(x, fy - 4 * s + 4 * s * h(x)) for x in range(0, tw + 8, 8)] + [(tw, fy + 16 * s)], (70, 140, 50, 255))
    for k in range(int(tw / (16 * s))):
        x = k * 16 * s
        near.line([(x, fy + 4 * s), (x + rng.uniform(-6, 6) * s, fy - rng.uniform(8, 16) * s)], (100, 180, 70, 255), 3 * s)
    for _ in range(int(tw / (120 * s))):                                 # des champignons qui luisent
        x = rng.uniform(0, tw)
        near.poly([(x - 3 * s, fy + 2 * s), (x + 3 * s, fy + 2 * s), (x + 3 * s, fy - 12 * s), (x - 3 * s, fy - 12 * s)], (240, 230, 210, 255))
        near.chord(x - 10 * s, fy - 22 * s, x + 10 * s, fy - 4 * s, 180, 360, (255, 120, 80, 255))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"fireflies": True}}


# ============================================================================ Dynasty Wars
DW_FLOOR = 390          # the plain of the battle / la plaine de la bataille


def build_dw_field(W, H, s, seed=1411):
    """Dynasty Wars: the field of battle of the first round, as in the game: a hazy sky, blue mountains far away, grey
    and brown cliffs, the dusty plain and its tufts of dry grass, the banners of the armies. / Le champ de bataille du
    premier niveau : ciel brumeux, montagnes bleues au loin, falaises grises et brunes, plaine poussiéreuse, bannières."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (150, 170, 190)), (0.6, (210, 200, 170)), (1.0, (200, 180, 140))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    f = periodic(tw, rng, 6, 1.0)
    far.poly([(0, H)] + [(x, 150 * s + 70 * s * f(x)) for x in range(0, tw + 8, 8)] + [(tw, H)], (140, 156, 184, 255))
    g = periodic(tw, rng, 7, 1.0)
    far.poly([(0, H)] + [(x, 220 * s + 40 * s * g(x)) for x in range(0, tw + 8, 8)] + [(tw, H)], (112, 128, 150, 255))
    layers.append({"img": far.done(), "y": 0, "f": 0.12, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)                                             # les falaises
    x = 0.0
    while x < tw:
        w = rng.uniform(220, 420) * s
        h = rng.uniform(150, 250) * s
        base = DW_FLOOR * s
        pts = [(x, base)]
        n = 6
        for i in range(n + 1):
            pts.append((x + w * i / n + rng.uniform(-10, 10) * s, base - h * (0.7 + 0.3 * math.sin(i / n * math.pi)) + rng.uniform(-20, 20) * s))
        pts.append((x + w, base))
        mid.poly(pts, (130, 116, 96, 255), (80, 70, 56, 255), 2 * s)
        lit = [pts[0]] + pts[1:4] + [(pts[3][0] - 30 * s, base)]       # la face éclairée / the lit face
        mid.poly(lit, (160, 146, 120, 255))
        for px_, py_ in pts[1:-1]:                                    # des pins sur la crête / pines on the ridge
            if rng.random() < 0.5:
                mid.poly([(px_ - 14 * s, py_ + 4 * s), (px_ + 14 * s, py_ + 4 * s), (px_, py_ - 40 * s)], (50, 90, 50, 255))
                mid.poly([(px_ - 10 * s, py_ - 14 * s), (px_ + 10 * s, py_ - 14 * s), (px_, py_ - 52 * s)], (60, 106, 56, 255))
        for k in range(6):                                            # les strates
            y = base - h * rng.uniform(0.2, 0.8)
            mid.line([(x + w * rng.uniform(0.05, 0.3), y), (x + w * rng.uniform(0.6, 0.95), y + rng.uniform(-8, 8) * s)], (104, 92, 76, 255), 3 * s)
        x += w + rng.uniform(80, 260) * s
    for k in range(6):                                                   # les bannières
        bx = rng.uniform(0, tw)
        b = DW_FLOOR * s
        mid.line([(bx, b), (bx, b - 220 * s)], (90, 60, 36, 255), 5 * s)
        col = rng.choice(((200, 50, 40), (240, 200, 60), (60, 90, 170)))
        mid.poly([(bx, b - 220 * s), (bx + 60 * s, b - 214 * s), (bx + 56 * s, b - 140 * s), (bx, b - 146 * s)], _rgba(col), (60, 30, 20, 255), 2 * s)
    layers.append({"img": mid.done(), "y": 0, "f": 0.5, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)                                            # la plaine poussiéreuse
    fy = DW_FLOOR * s
    near.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (184, 156, 110, 255))
    for _ in range(int(tw / (30 * s))):
        x = rng.uniform(0, tw)
        y = rng.uniform(fy, H)
        for j in range(4):
            near.line([(x, y), (x + rng.uniform(-8, 8) * s, y - rng.uniform(8, 18) * s)], (140, 140, 70, 255), 2 * s)
    for _ in range(int(tw / (50 * s))):
        near.disc(rng.uniform(0, tw), rng.uniform(fy + 10 * s, H), rng.uniform(2, 5) * s, (150, 126, 90, 255))
    near.line([(0, fy), (tw, fy)], (160, 130, 90, 255), 3 * s)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"dust": (230, 200, 150)}}


BUILDERS = {"gg_grave": build_gg_grave, "st_city": build_st_city, "pg_temple": build_pg_temple, "pg_peak": build_pg_peak, "spf_hall": build_spf_hall, "mt_forest": build_mt_forest, "ms_tower": build_ms_tower, "wl_village": build_wl_village, "nm_dream": build_nm_dream,
            "tw_woods": build_tw_woods, "dw_field": build_dw_field}
hd_bg.BUILDERS.update(BUILDERS)
THEMES = tuple(BUILDERS)                 # names of the backdrops of this batch / noms des décors de ce lot
