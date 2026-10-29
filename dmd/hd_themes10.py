"""HD backdrops of the tenth batch of Neo Geo games done one by one (1.26), each drawn after screenshots of its game.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported.

Décors HD du dixième lot (1.26), chacun dessiné d'après des captures de son jeu. Tout est dessiné par le programme,
aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image

from . import hd_bg
from .hd_bg import mix, vgrad
from .hd_themes3 import _clump, _fit, _Pic, _rgba
from .hd_themes5 import BRAWL_FLOOR
from .hd_themes9 import _star

ZT_COLS, ZT_ROWS, ZT_CELL, ZT_TOP = 8, 9, 34, 104      # Zintrick: the fields / les champs
ZT_FIELDS = (560, 1360)                                 # the middle of each field / le milieu de chaque champ
DM_COLS, DM_ROWS, DM_CELL, DM_X0, DM_Y0 = 40, 8, 40, 160, 104   # Digger Man: the mine / la mine
IM_PATH = ((120, 380), (420, 380), (420, 200), (760, 200), (760, 330), (1120, 330), (1120, 150), (1480, 150), (1480, 300), (1820, 300))
IM_HALF = 34                                            # The Irritating Maze: half width of the corridor / demi-largeur du couloir
B2B_ROWS = ((424, ((0, 1920),)), (330, ((120, 640), (1280, 1800))), (236, ((380, 1540),)), (148, ((60, 520), (1400, 1860))))


def build_zt_hills(W, H, s, seed=501):
    """Zintrick: the green mountains under a pale sky, as in the game, and the two fields in their purple frames with
    their green grids. / Les montagnes vertes sous un ciel pâle, et les deux champs dans leurs cadres violets."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (110, 170, 230)), (0.6, (210, 230, 250)), (1.0, (180, 220, 200))])
    p = _Pic(W, H, 2, 4 * W)
    for k, (col, y0, amp) in enumerate((((120, 160, 170), 200, 70), ((80, 130, 90), 260, 50), ((60, 110, 64), 330, 40))):
        pts = [(0, H)]
        for i in range(0, 61):
            x = i * W / 60
            pts.append((x, (y0 - amp * abs(math.sin(x / W * 7.3 + k * 1.3)) - rng.uniform(0, 8)) * s))
        pts.append((W, H))
        p.poly(pts, _rgba(col))
    c = ZT_CELL * s
    for cx in (v * s for v in ZT_FIELDS):
        w, h = ZT_COLS * c, ZT_ROWS * c
        x0, y0 = cx - w / 2, ZT_TOP * s
        p.poly([(x0 - 16 * s, y0 - 16 * s), (x0 + w + 16 * s, y0 - 16 * s), (x0 + w + 16 * s, y0 + h + 16 * s), (x0 - 16 * s, y0 + h + 16 * s)],
               (150, 110, 220, 255), (70, 40, 110, 255), 3 * s)
        for k in range(int((w + 32 * s) / (16 * s))):                     # le cadre en écailles
            p.disc(x0 - 8 * s + k * 16 * s, y0 - 8 * s, 6 * s, (190, 160, 240, 255))
            p.disc(x0 - 8 * s + k * 16 * s, y0 + h + 8 * s, 6 * s, (120, 190, 110, 255))
        p.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], (40, 120, 90, 255))
        for i in range(ZT_COLS + 1):
            p.line([(x0 + i * c, y0), (x0 + i * c, y0 + h)], (70, 160, 120, 255), 2 * s)
        for j in range(ZT_ROWS + 1):
            p.line([(x0, y0 + j * c), (x0 + w, y0 + j * c)], (70, 160, 120, 255), 2 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_dm_mine(W, H, s, seed=511):
    """Digger Man: the dark rock behind the mine, with its grey brick frame. / La roche sombre derrière la mine."""
    rng = random.Random(seed)
    sky = Image.new("RGB", (W, H), (26, 22, 24))
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(300):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(4, 14) * s
        p.disc(x, y, r, _rgba(rng.choice(((36, 30, 32), (44, 38, 40), (30, 26, 28)))))
    c = DM_CELL * s
    x0, y0 = DM_X0 * s, DM_Y0 * s
    w, h = DM_COLS * c, DM_ROWS * c
    for row in range(int((h + 40 * s) / (14 * s)) + 1):                 # le cadre de briques grises
        y = y0 - 20 * s + row * 14 * s
        off = (row % 2) * 14 * s
        for x in range(int(x0 - 20 * s - off), int(x0 + w + 20 * s), int(28 * s)):
            if y0 <= y < y0 + h and x0 <= x < x0 + w - 28 * s:
                continue
            p.poly([(x, y), (x + 27 * s, y), (x + 27 * s, y + 13 * s), (x, y + 13 * s)], (120, 120, 128, 255), (70, 70, 76, 255), 1.2 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_im_maze(W, H, s, seed=521):
    """The Irritating Maze: the red checkered floor, the corridor of the maze between its blue rails, a big arrow on the
    floor, a round bumper, a crate, and the map of the maze in its green frame at the bottom left. / Le sol en damier
    rouge, le couloir du labyrinthe entre ses rails bleus, une grande flèche, un butoir rond, la carte du labyrinthe."""
    rng = random.Random(seed)
    sky = Image.new("RGB", (W, H), (70, 14, 18))
    p = _Pic(W, H, 2, 4 * W)
    c = 24 * s
    for i in range(int(W / c) + 1):                                       # le damier rouge
        for j in range(int(H / c) + 1):
            if (i + j) % 2:
                p.poly([(i * c, j * c), ((i + 1) * c, j * c), ((i + 1) * c, (j + 1) * c), (i * c, (j + 1) * c)], (100, 24, 28, 255))
    pts = [(x * s, y * s) for x, y in IM_PATH]
    hw = IM_HALF * s
    for wdt, col in ((2 * hw + 26 * s, (40, 60, 150, 255)), (2 * hw + 14 * s, (170, 190, 230, 255)), (2 * hw, (30, 30, 40, 255))):
        p.line(pts, col, wdt)                                             # les rails et le couloir
        for x, y in pts:
            p.poly([(x - wdt / 2, y - wdt / 2), (x + wdt / 2, y - wdt / 2), (x + wdt / 2, y + wdt / 2), (x - wdt / 2, y + wdt / 2)], col)
    for k in range(len(pts) - 1):                                         # les pointillés du couloir
        (x0, y0), (x1, y1) = pts[k], pts[k + 1]
        n = int(math.hypot(x1 - x0, y1 - y0) / (30 * s))
        for i in range(n):
            t = (i + 0.5) / n
            p.disc(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 2.5 * s, (90, 90, 110, 255))
    ax, ay = 560 * s, 300 * s                                              # la grande flèche
    p.poly([(ax, ay + 60 * s), (ax + 30 * s, ay + 60 * s), (ax + 30 * s, ay + 10 * s), (ax + 60 * s, ay + 10 * s), (ax + 15 * s, ay - 40 * s),
            (ax - 30 * s, ay + 10 * s), (ax, ay + 10 * s)], (150, 160, 40, 255), (60, 60, 20, 255), 2 * s)
    p.disc(950 * s, 240 * s, 30 * s, (180, 180, 190, 255), (60, 60, 70, 255), 3 * s)    # le butoir
    p.disc(950 * s, 240 * s, 14 * s, (60, 60, 70, 255))
    p.poly([(1250 * s, 220 * s), (1340 * s, 210 * s), (1350 * s, 270 * s), (1260 * s, 280 * s)], (180, 110, 60, 255), (90, 50, 20, 255), 3 * s)  # la caisse
    p.line([(1255 * s, 225 * s), (1345 * s, 265 * s)], (120, 70, 30, 255), 4 * s)
    mx, my, mw, mh = 20 * s, 330 * s, 230 * s, 110 * s                    # la carte du labyrinthe
    p.poly([(mx, my), (mx + mw, my), (mx + mw, my + mh), (mx, my + mh)], (20, 30, 20, 255), (60, 220, 90, 255), 3 * s)
    mpts = [(mx + 15 * s + x / 1920 * (mw - 30 * s), my + 12 * s + (y - 120) / 300 * (mh - 24 * s)) for x, y in IM_PATH]
    p.line(mpts, (60, 220, 90, 255), 5 * s)
    p.line(mpts, (20, 30, 20, 255), 2 * s)
    for _ in range(30):                                                   # des rivets
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        p.disc(x, y, 3 * s, (140, 50, 50, 255))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def _rocks(p, tw, H, base, s, rng, cols, n=60, hmin=20, hmax=80):
    pts = [(0, H)]
    x = 0
    while x < tw:
        pts.append((x, base - rng.uniform(hmin, hmax) * s))
        x += rng.uniform(20, 60) * s
    pts += [(tw, base - 30 * s), (tw, H)]
    p.poly(pts, _rgba(cols[0]))
    for _ in range(n):
        x, y = rng.uniform(0, tw), rng.uniform(base - 20 * s, H)
        r = rng.uniform(6, 22) * s
        p.poly([(x - r, y), (x - r * 0.3, y - r * 0.9), (x + r * 0.6, y - r * 0.5), (x + r, y + r * 0.2)], _rgba(rng.choice(cols[1:])))


def build_ad_planet(W, H, s, seed=531):
    """Andro Dunos: space over a planet, as in the game: black sky and stars, the blue glow of the horizon, the rocky
    grey-blue ground below. / L'espace au-dessus d'une planète : le ciel noir et ses étoiles, la lueur bleue de
    l'horizon, le sol rocheux gris-bleu."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (2, 2, 10)), (0.6, (8, 10, 30)), (0.78, (40, 60, 130)), (1.0, (40, 60, 130))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    for _ in range(260):
        far.disc(rng.uniform(0, tw), rng.uniform(0, H * 0.7), rng.uniform(0.6, 1.8) * s, _rgba(rng.choice(((250, 250, 255), (180, 200, 255), (255, 230, 200)))))
    layers.append({"img": far.done(), "y": 0, "f": 0.1, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    _rocks(mid, tw, H, 372 * s, s, rng, ((70, 84, 110), (90, 104, 130), (60, 70, 96)), 40, 10, 40)
    layers.append({"img": mid.done(), "y": 0, "f": 0.4, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    _rocks(near, tw, H, 430 * s, s, rng, ((110, 120, 140), (140, 150, 170), (80, 90, 110), (200, 210, 225)), 80, 10, 60)
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


def build_ct_forest(W, H, s, seed=541):
    """Captain Tomaday: the forest seen from the sky, as in the game: the dark green trees, little houses with their
    red roofs, the railway and its steam train, a river. / La forêt vue du ciel : les arbres, les petites maisons et
    leurs toits rouges, la voie ferrée et son train à vapeur, une rivière."""
    rng = random.Random(seed)
    tw = 2 * W
    img = Image.new("RGB", (tw, H), (60, 110, 50))
    p = _Pic(tw, H, 2, tw)
    ry = 300 * s
    p.poly([(0, 60 * s), (tw, 120 * s), (tw, 160 * s), (0, 100 * s)], (60, 120, 190, 255))        # la rivière
    for x in range(0, int(tw), int(30 * s)):                                                       # la voie ferrée
        p.line([(x, ry - 16 * s), (x, ry + 16 * s)], (110, 80, 50, 255), 6 * s)
    p.line([(0, ry - 9 * s), (tw, ry - 9 * s)], (170, 170, 180, 255), 3 * s)
    p.line([(0, ry + 9 * s), (tw, ry + 9 * s)], (170, 170, 180, 255), 3 * s)
    tx = tw * 0.3                                                                                  # le train à vapeur
    for k in range(5):
        x = tx - k * 130 * s
        p.poly([(x, ry - 26 * s), (x + 120 * s, ry - 26 * s), (x + 120 * s, ry + 26 * s), (x, ry + 26 * s)],
               (50, 50, 60, 255) if k == 0 else (130, 60, 40, 255), (20, 20, 24, 255), 2 * s)
        if k == 0:
            p.disc(x + 96 * s, ry, 14 * s, (30, 30, 34, 255), (200, 170, 60, 255), 3 * s)
        else:
            p.poly([(x + 10 * s, ry - 18 * s), (x + 110 * s, ry - 18 * s), (x + 110 * s, ry + 18 * s), (x + 10 * s, ry + 18 * s)], (160, 90, 60, 255))
    for _ in range(int(tw / (90 * s))):                                                             # les maisons
        x, y = rng.uniform(0, tw), rng.choice((rng.uniform(170, 210), rng.uniform(340, 400))) * s
        w, h = rng.uniform(50, 80) * s, rng.uniform(40, 60) * s
        p.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], (200, 70, 50, 255), (90, 30, 20, 255), 2 * s)
        p.line([(x, y + h / 2), (x + w, y + h / 2)], (130, 40, 30, 255), 3 * s)
    for _ in range(int(tw * H / (2600 * s * s))):                                                   # les arbres
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        if abs(y - ry) < 50 * s or 40 * s < y - (60 + x / tw * 60) * s < 110 * s:
            continue
        r = rng.uniform(18, 34) * s
        p.disc(x + r * 0.3, y + r * 0.3, r, (20, 40, 20, 110))
        _clump(p, x, y, r, rng, ((30, 80, 40), (50, 110, 50), (90, 150, 70)), n=5)
    out = img.convert("RGBA")
    out.alpha_composite(p.done())
    return {"sky": Image.new("RGB", (W, H), (60, 110, 50)), "layers": [{"img": out.convert("RGB"), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw,
            "amb": {}}


def build_ic_sea(W, H, s, seed=551):
    """Ironclad: the sea at dusk, as in the game: the orange and purple sky, the clouds, the iron warships with their
    funnels on the horizon, the waves. / La mer au crépuscule : le ciel orange et violet, les cuirassés de fer et leurs
    cheminées à l'horizon, les vagues."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (60, 40, 90)), (0.35, (200, 100, 90)), (0.55, (250, 180, 110)), (0.6, (60, 80, 120)), (1.0, (30, 40, 70))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    for _ in range(14):
        x, y = rng.uniform(0, tw), rng.uniform(30, 160) * s
        for k in range(6):
            far.disc(x + k * 34 * s, y + rng.uniform(-8, 8) * s, rng.uniform(16, 30) * s, (240, 170, 150, 255))
            far.disc(x + k * 34 * s, y + 10 * s + rng.uniform(-6, 6) * s, rng.uniform(12, 22) * s, (170, 100, 120, 255))
    hor = 276 * s
    x = 100 * s
    while x < tw - 300 * s:                                               # les cuirassés à l'horizon
        w = rng.uniform(220, 340) * s
        far.poly([(x, hor - 10 * s), (x + w, hor - 10 * s), (x + w - 20 * s, hor + 6 * s), (x + 20 * s, hor + 6 * s)], (40, 36, 50, 255))
        far.poly([(x + w * 0.3, hor - 30 * s), (x + w * 0.7, hor - 30 * s), (x + w * 0.7, hor - 10 * s), (x + w * 0.3, hor - 10 * s)], (50, 44, 60, 255))
        for k in range(2):
            fx = x + w * (0.4 + 0.15 * k)
            far.poly([(fx, hor - 56 * s), (fx + 14 * s, hor - 56 * s), (fx + 14 * s, hor - 30 * s), (fx, hor - 30 * s)], (60, 50, 66, 255))
            far.disc(fx + 7 * s, hor - 66 * s, 10 * s, (110, 100, 110, 255))
        x += w + rng.uniform(400, 800) * s
    layers.append({"img": far.done(), "y": 0, "f": 0.15, "stage": "far"})
    near = _Pic(tw, H, 2, tw)
    for row in range(10):                                                 # les vagues
        y = (290 + row * 18) * s
        for x0 in range(0, int(tw), int(60 * s)):
            xx = x0 + (row % 2) * 30 * s
            near.line([(xx, y), (xx + 20 * s, y - 4 * s), (xx + 40 * s, y)], _rgba(mix((90, 120, 170), (250, 200, 160), 0.5 - row * 0.04)), 2 * s)
    layers.append({"img": near.done(), "y": 0, "f": 0.6, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


def build_lh_space(W, H, s, seed=561):
    """Last Hope: deep space, as in the game: the black of space full of blue and white stars, the nebulas, a big blue
    planet on the side. / L'espace profond : le noir plein d'étoiles bleues et blanches, les nébuleuses, une grosse
    planète bleue sur le côté."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = Image.new("RGB", (W, H), (2, 2, 8))
    layers = []
    far = _Pic(tw, H, 2, tw)
    for _ in range(10):                                                   # nébuleuses, plus claires au cœur
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        col = rng.choice(((60, 30, 100), (30, 50, 110), (80, 30, 80)))
        blobs = [(x + rng.uniform(-90, 90) * s, y + rng.uniform(-40, 40) * s, rng.uniform(30, 60) * s) for _k in range(7)]
        for k, sc in enumerate((1.0, 0.7, 0.4)):
            for bx, by, br in blobs:
                far.disc(bx, by, br * sc, _rgba(mix((8, 8, 20), col, 0.45 + 0.27 * k)))
    for _ in range(400):
        far.disc(rng.uniform(0, tw), rng.uniform(0, H), rng.uniform(0.6, 1.6) * s, _rgba(rng.choice(((250, 250, 255), (160, 190, 255), (200, 220, 255)))))
    for k in range(2):                                                    # la planète
        px, py, r = tw * (0.05 + 0.5 * k), 300 * s, 160 * s
        far.disc(px, py, r, (40, 60, 140, 255))
        far.disc(px + r * 0.2, py - r * 0.2, r * 0.8, (70, 100, 180, 255))
        far.disc(px + r * 0.35, py - r * 0.35, r * 0.5, (110, 140, 210, 255))
    layers.append({"img": far.done(), "y": 0, "f": 0.12, "stage": "far"})
    near = _Pic(tw, H, 2, tw)
    for _ in range(80):
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        _star(near, x, y, rng.uniform(3, 6) * s, (220, 230, 255, 255), n=4, inner=0.25)
    layers.append({"img": near.done(), "y": 0, "f": 0.6, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


def build_bbb_ice(W, H, s, seed=571):
    """Bang Bang Busters: the ice world, as in the game: the blue sky and its aurora, the snowy icebergs, the platforms
    of ice blocks. / Le monde de glace : le ciel bleu et son aurore, les icebergs enneigés, les plateformes de blocs."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (30, 90, 200)), (0.6, (110, 190, 250)), (1.0, (200, 240, 255))])
    p = _Pic(W, H, 2, 4 * W)
    for k, col in enumerate(((110, 240, 200), (240, 160, 230))):        # l'aurore
        pts = [(x * W / 40, (40 + 30 * k + 24 * math.sin(x / 40 * 6.3 + k)) * s) for x in range(41)]
        p.line(pts, _rgba(col), 18 * s)
    for k in range(9):                                                    # les icebergs
        x = k * W / 8 + rng.uniform(-60, 60) * s
        hgt = rng.uniform(80, 160) * s
        p.poly([(x - 140 * s, H), (x - 40 * s, H - hgt), (x + 30 * s, H - hgt - 20 * s), (x + 150 * s, H)], (220, 240, 255, 255), (150, 190, 230, 255), 2 * s)
        p.poly([(x - 40 * s, H - hgt), (x + 30 * s, H - hgt - 20 * s), (x + 10 * s, H - hgt + 30 * s)], (250, 252, 255, 255))
    for y, segs in B2B_ROWS:                                              # les plateformes de blocs de glace
        for x0, x1 in segs:
            x = x0 * s
            while x < x1 * s - 4 * s:
                p.poly([(x, y * s), (x + 40 * s, y * s), (x + 40 * s, y * s + 28 * s), (x, y * s + 28 * s)], (140, 210, 250, 255), (60, 130, 210, 255), 2 * s)
                p.poly([(x + 5 * s, y * s + 4 * s), (x + 22 * s, y * s + 4 * s), (x + 22 * s, y * s + 10 * s), (x + 5 * s, y * s + 10 * s)], (240, 250, 255, 255))
                x += 40 * s
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_cs_forest(W, H, s, seed=581):
    """Crossed Swords: the forest at night, as in the game: the tall dark trunks, the deep blue leaves, the path
    between them. / La forêt la nuit : les grands troncs sombres, le feuillage bleu profond, le chemin."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (16, 24, 60)), (0.55, (30, 46, 100)), (1.0, (20, 30, 40))])
    p = _Pic(W, H, 2, 4 * W)
    for k in range(3):                                                    # trois rangées de troncs
        tone = mix((30, 40, 80), (14, 18, 30), k / 2)
        for _ in range(14):
            x = rng.uniform(0, W)
            w = rng.uniform(20, 40) * s * (1 + k * 0.6)
            p.poly([(x, 0), (x + w, 0), (x + w * 1.2, H * 0.78), (x - w * 0.2, H * 0.78)], _rgba(tone))
        for _ in range(16):
            _clump(p, rng.uniform(0, W), rng.uniform(0, 120) * s, rng.uniform(50, 90) * s, rng,
                   (mix((30, 50, 110), (10, 16, 40), k / 2), mix((50, 70, 140), (20, 30, 60), k / 2)), n=5)
    p.poly([(0, H * 0.74), (W, H * 0.74), (W, H), (0, H)], (24, 40, 30, 255))   # le sol
    p.poly([(W * 0.4, H * 0.74), (W * 0.6, H * 0.74), (W * 0.8, H), (W * 0.2, H)], (70, 60, 50, 255))   # le chemin
    for _ in range(40):
        _clump(p, rng.uniform(0, W), rng.uniform(H * 0.76, H), rng.uniform(14, 30) * s, rng, ((20, 50, 30), (30, 70, 40)), n=4)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_em_city(W, H, s, seed=591):
    """Eight Man: the ruined city at sunset, as in the game: the golden sky, the broken towers, a fallen overpass, the
    street and its cracks. / La ville en ruine au coucher du soleil : le ciel doré, les tours cassées, la rue fissurée."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (250, 200, 100)), (0.45, (250, 160, 70)), (1.0, (180, 90, 50))])
    layers = []
    far = _Pic(tw, H, 2, tw)
    x = -20 * s
    while x < tw:                                                         # les tours au loin
        w = rng.uniform(60, 130) * s
        top = rng.uniform(60, 170) * s
        col = rng.choice(((200, 150, 80), (180, 130, 70), (220, 170, 100)))
        far.poly([(x, BRAWL_FLOOR * s), (x, top), (x + w * 0.6, top + rng.uniform(-20, 20) * s), (x + w, top + 30 * s), (x + w, BRAWL_FLOOR * s)],
                 _rgba(col))
        for wy in range(int(top + 14 * s), int(BRAWL_FLOOR * s - 20 * s), int(20 * s)):
            for wx in range(int(x + 8 * s), int(x + w - 12 * s), int(16 * s)):
                far.poly([(wx, wy), (wx + 8 * s, wy), (wx + 8 * s, wy + 10 * s), (wx, wy + 10 * s)], _rgba(mix(col, (60, 30, 20), 0.5)))
        x += w + rng.uniform(10, 40) * s
    layers.append({"img": far.done(), "y": 0, "f": 0.3, "stage": "far"})
    near = _Pic(tw, H, 2, tw)
    fy = BRAWL_FLOOR * s
    for k in range(2):                                                    # le pont effondré
        bx = tw * (0.2 + 0.5 * k)
        near.poly([(bx, fy - 120 * s), (bx + 400 * s, fy - 150 * s), (bx + 400 * s, fy - 126 * s), (bx, fy - 96 * s)], (150, 110, 70, 255),
                  (70, 50, 30, 255), 2 * s)
        for px in (bx + 60 * s, bx + 300 * s):
            near.poly([(px, fy - 110 * s), (px + 26 * s, fy - 114 * s), (px + 26 * s, fy), (px, fy)], (130, 96, 60, 255), (70, 50, 30, 255), 2 * s)
    near.poly([(0, fy), (tw, fy), (tw, H), (0, H)], (120, 100, 90, 255))  # la rue
    near.line([(0, fy + 2 * s), (tw, fy + 2 * s)], (200, 180, 150, 255), 4 * s)
    for _ in range(40):                                                   # fissures et gravats
        x, y = rng.uniform(0, tw), rng.uniform(fy + 20 * s, H)
        near.line([(x, y), (x + rng.uniform(-40, 40) * s, y + rng.uniform(-10, 10) * s), (x + rng.uniform(-60, 60) * s, y + rng.uniform(-14, 14) * s)],
                  (80, 66, 60, 255), 2 * s)
        near.disc(x + 30 * s, y, rng.uniform(3, 7) * s, (150, 130, 110, 255))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {"dust": (250, 200, 140)}}


hd_bg.BUILDERS.update({"zt_hills": build_zt_hills, "dm_mine": build_dm_mine, "im_maze": build_im_maze, "ad_planet": build_ad_planet,
                       "ct_forest": build_ct_forest, "ic_sea": build_ic_sea, "lh_space": build_lh_space, "bbb_ice": build_bbb_ice,
                       "cs_forest": build_cs_forest, "em_city": build_em_city})
