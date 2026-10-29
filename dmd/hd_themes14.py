"""Backdrops of the Capcom CPS action, platform and puzzle games (1.30), drawn by the program after screenshots of the
games. Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when
this module is imported (by hd_games14).

Décors des jeux d'action, de plateforme et de réflexion Capcom CPS (1.30), dessinés par le programme d'après des
captures des jeux. Tout est dessiné par le programme, aucune image ne vient d'un jeu.
"""

import math
import random

from . import hd_bg
from .hd_bg import periodic, vgrad
from .hd_themes3 import _fit, _Pic, _rgba

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


BUILDERS = {"gg_grave": build_gg_grave, "st_city": build_st_city}
hd_bg.BUILDERS.update(BUILDERS)
THEMES = tuple(BUILDERS)                 # names of the backdrops of this batch / noms des décors de ce lot
