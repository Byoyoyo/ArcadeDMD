"""HD backdrops of the ninth batch of Neo Geo games done one by one (1.25), each drawn after screenshots of its game.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported.

Décors HD du neuvième lot (1.25), chacun dessiné d'après des captures de son jeu. Tout est dessiné par le programme,
aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image

from . import hd_bg
from .hd_bg import mix, vgrad
from .hd_themes3 import _clump, _fit, _Pic, _rgba
from .hd_themes4 import RALLY_LOOKS, build_rally, rally_road

BB_COURT = (118, 456)                 # Bang Bead: top and bottom of the street court at s = 1 / le terrain dans la rue
FS_COURT = (120, 446)                 # Battle Flip Shot: top and bottom of the arena / l'arène
HORSE_TRACK = (282, 432)              # horse races: far and near edge of the track / la piste des courses de chevaux
PZ_CELL = 22                          # Puzzled: one square of the well / une case du puits
PZ_WELLS = (560, 1360)                # Puzzled: the middle of each well / le milieu de chaque puits
PZ_COLS, PZ_ROWS, PZ_TOP = 10, 15, 96


def _star(p, x, y, r, fill, outline=None, width=0, n=5, inner=0.45, rot=-math.pi / 2):
    pts = []
    for i in range(2 * n):
        a = rot + i * math.pi / n
        rr = r if i % 2 == 0 else r * inner
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    p.poly(pts, fill, outline, width)


def _car_top(p, x, y, w, h, body, s):
    """A car parked along the street, seen from above. / Une voiture garée, vue du dessus."""
    dark = _rgba(mix(body, (0, 0, 0), 0.5))
    for wx in (0.18, 0.74):
        for wy in (-0.06, 0.92):
            p.poly([(x + w * wx, y + h * wy), (x + w * (wx + 0.12), y + h * wy), (x + w * (wx + 0.12), y + h * (wy + 0.14)),
                    (x + w * wx, y + h * (wy + 0.14))], (24, 24, 28, 255))
    p.poly([(x + w * 0.05, y + h * 0.1), (x + w * 0.95, y + h * 0.1), (x + w, y + h * 0.3), (x + w, y + h * 0.7), (x + w * 0.95, y + h * 0.9),
            (x + w * 0.05, y + h * 0.9), (x, y + h * 0.7), (x, y + h * 0.3)], _rgba(body), dark, 1.6 * s)
    p.poly([(x + w * 0.3, y + h * 0.18), (x + w * 0.66, y + h * 0.18), (x + w * 0.66, y + h * 0.82), (x + w * 0.3, y + h * 0.82)],
           _rgba(mix(body, (255, 255, 255), 0.25)), dark, 1.2 * s)
    p.poly([(x + w * 0.66, y + h * 0.2), (x + w * 0.78, y + h * 0.26), (x + w * 0.78, y + h * 0.74), (x + w * 0.66, y + h * 0.8)], (70, 100, 130, 255))
    p.poly([(x + w * 0.3, y + h * 0.2), (x + w * 0.22, y + h * 0.28), (x + w * 0.22, y + h * 0.72), (x + w * 0.3, y + h * 0.8)], (70, 100, 130, 255))


def build_bb_street(W, H, s, seed=401):
    """Bang Bead: the street court seen from above, as in the game: the grey asphalt and its stains, the white middle
    line with its manhole, the orange lane marks, the goal lines lit with yellow stars at both ends, the cars parked
    along the pavement at the top. / La rue vue du dessus : l'asphalte, la ligne du milieu et sa plaque d'égout, les
    marques orange, les lignes de but et leurs étoiles jaunes, les voitures garées le long du trottoir."""
    rng = random.Random(seed)
    sky = Image.new("RGB", (W, H), (84, 86, 92))
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(int(W * H / (500 * s * s))):                         # le grain de l'asphalte
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        p.disc(x, y, rng.uniform(1, 3) * s, _rgba(rng.choice(((96, 98, 104), (74, 76, 82), (104, 104, 110)))))
    for _ in range(12):                                                  # taches
        x, y = rng.uniform(0, W), rng.uniform(BB_COURT[0] + 20, BB_COURT[1]) * s
        r = rng.uniform(20, 46) * s
        p.ellipse(x - r, y - r * 0.6, x + r, y + r * 0.6, (70, 72, 78, 255))
    top, bot = (v * s for v in BB_COURT)
    p.poly([(0, 0), (W, 0), (W, top - 26 * s), (0, top - 26 * s)], (64, 66, 72, 255))     # la rue derrière
    p.poly([(0, top - 26 * s), (W, top - 26 * s), (W, top), (0, top)], (176, 172, 160, 255))        # le trottoir
    p.line([(0, top), (W, top)], (120, 116, 108, 255), 3 * s)
    x = 30 * s
    while x < W - 120 * s:                                               # les voitures garées
        w = rng.uniform(150, 180) * s
        _car_top(p, x, top - 104 * s, w, 70 * s, rng.choice(((40, 70, 160), (190, 40, 40), (230, 230, 230), (40, 130, 90), (230, 190, 40))), s)
        x += w + rng.uniform(30, 90) * s
    cx, cy = W / 2, (top + bot) / 2
    for y0 in range(int(top + 10 * s), int(bot), int(44 * s)):           # la ligne blanche du milieu
        p.poly([(cx - 5 * s, y0), (cx + 5 * s, y0), (cx + 5 * s, y0 + 26 * s), (cx - 5 * s, y0 + 26 * s)], (216, 216, 210, 255))
    for k in (1, 2):                                                     # les marques orange
        y = top + (bot - top) * k / 3
        for x0 in range(int(140 * s), int(W - 140 * s), int(120 * s)):
            if abs(x0 + 35 * s - cx) < 80 * s:
                continue
            p.poly([(x0, y - 5 * s), (x0 + 70 * s, y - 5 * s), (x0 + 70 * s, y + 5 * s), (x0, y + 5 * s)], (226, 140, 40, 255))
    p.disc(cx, cy, 44 * s, (60, 60, 64, 255), (40, 40, 44, 255), 4 * s)  # la plaque d'égout
    for k in range(5):
        p.line([(cx - 36 * s, cy - 24 * s + k * 12 * s), (cx + 36 * s, cy - 24 * s + k * 12 * s)], (90, 90, 96, 255), 3 * s)
    for side in (-1, 1):                                                 # les lignes de but, roses, et leurs étoiles
        gx = cx + side * (W / 2 - 60 * s)
        p.poly([(gx - 4 * s, top), (gx + 4 * s, top), (gx + 4 * s, bot), (gx - 4 * s, bot)], (230, 110, 230, 255))
        for k in range(7):
            y = top + 24 * s + k * (bot - top - 48 * s) / 6
            _star(p, gx - side * 26 * s, y, 15 * s, (250, 220, 40, 255), (150, 110, 20, 255), 1.5 * s)
        p.poly([(gx + side * 4 * s, top), (gx + side * 60 * s, top), (gx + side * 60 * s, bot), (gx + side * 4 * s, bot)], (70, 70, 80, 255))
    for _ in range(6):                                                   # fissures
        x, y = rng.uniform(200, W - 200), rng.uniform(top + 20 * s, bot - 20 * s)
        pts = [(x, y)]
        for _k in range(4):
            x += rng.uniform(-30, 30) * s
            y += rng.uniform(-14, 14) * s
            pts.append((x, y))
        p.line(pts, (58, 58, 62, 255), 1.6 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_fs_arena(W, H, s, seed=411):
    """Battle Flip Shot: the arena seen from above, as in the game: the teal metal floor and its panels, the circuit
    lines, the big orange target with its cross in the middle, the purple brackets, the walls in yellow and black
    stripes at the top and the bottom. / L'arène vue du dessus : le sol de métal bleu-vert, les circuits, la grande
    cible orange et sa croix, les crochets violets, les murs rayés jaune et noir."""
    rng = random.Random(seed)
    sky = Image.new("RGB", (W, H), (34, 84, 104))
    p = _Pic(W, H, 2, 4 * W)
    top, bot = (v * s for v in FS_COURT)
    for x in range(0, W + 1, int(64 * s)):                               # les panneaux du sol
        p.line([(x, top), (x, bot)], (44, 100, 120, 255), 2 * s)
    for y in range(int(top), int(bot) + 1, int(64 * s)):
        p.line([(0, y), (W, y)], (44, 100, 120, 255), 2 * s)
    for _ in range(46):                                                  # les lignes de circuit
        x, y = rng.uniform(80, W - 80), rng.uniform(top + 20 * s, bot - 20 * s)
        pts = [(x, y)]
        for _k in range(3):
            if rng.random() < 0.5:
                x += rng.choice((-1, 1)) * rng.uniform(30, 90) * s
            else:
                y += rng.choice((-1, 1)) * rng.uniform(20, 60) * s
            pts.append((x, y))
        p.line(pts, (60, 150, 170, 255), 2.4 * s)
        p.disc(pts[-1][0], pts[-1][1], 4 * s, (90, 200, 220, 255))
    cx, cy = W / 2, (top + bot) / 2
    for r, col, wdt in ((130, (230, 140, 30), 14), (98, (250, 180, 50), 8), (44, (230, 140, 30), 10)):     # la cible orange
        p.disc(cx, cy, r * s, None, _rgba(col), wdt * s)
    for a in (45, 135):
        dx, dy = math.cos(math.radians(a)) * 30 * s, math.sin(math.radians(a)) * 30 * s
        p.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], (250, 180, 50, 255), 9 * s)
    for side in (-1, 1):                                                 # les crochets violets
        for k in (-1, 1):
            x = cx + side * 250 * s
            y = cy + k * 70 * s
            p.line([(x - side * 50 * s, y), (x, y), (x, y - k * 40 * s)], (150, 90, 210, 255), 12 * s)
        x = cx + side * 160 * s
        p.line([(x, cy - 40 * s), (x + side * 26 * s, cy), (x, cy + 40 * s)], (230, 140, 30, 255), 10 * s)
    for y0, y1 in ((top - 36 * s, top), (bot, bot + 36 * s)):            # les murs rayés
        p.poly([(0, y0), (W, y0), (W, y1), (0, y1)], (40, 40, 46, 255))
        for x in range(-40, W + 40, int(48 * s)):
            p.poly([(x, y0 + 6 * s), (x + 22 * s, y0 + 6 * s), (x + 4 * s, y1 - 6 * s), (x - 18 * s, y1 - 6 * s)], (240, 200, 40, 255))
        for x in range(int(60 * s), W, int(160 * s)):
            p.disc(x, (y0 + y1) / 2, 6 * s, (120, 230, 255, 255), (30, 30, 36, 255), 2 * s)
    p.poly([(0, 0), (W, 0), (W, top - 36 * s), (0, top - 36 * s)], (24, 40, 56, 255))
    for side in (-1, 1):                                                 # les murs de but, derrière les cibles
        gx = cx + side * (W / 2 - 22 * s)
        p.poly([(gx - 22 * s, top), (gx + 22 * s, top), (gx + 22 * s, bot), (gx - 22 * s, bot)], (52, 60, 72, 255), (24, 28, 36, 255), 3 * s)
        for k in range(8):
            y = top + 20 * s + k * (bot - top - 40 * s) / 7
            p.disc(gx, y, 5 * s, (230, 110, 230, 255))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


RALLY_LOOKS.update({
    "ot_forest": ((58, 88, 40), (50, 78, 34), (150, 118, 78), (112, 86, 56), (128, 98, 64), "forest"),
    "ot_road": ((66, 104, 48), (58, 94, 42), (112, 112, 118), (240, 240, 240), (236, 236, 236), "town"),
})


def build_ot(W, H, s, name, seed=421):
    """Over Top: the stages seen from above, as in the game: a dirt track through the pine forest, a grey road between
    the fields with its white lines, the pines in their dark green crowns. / Les étapes vues du ciel : la piste de
    terre dans la forêt de pins, la route grise entre les champs, les pins."""
    b = build_rally(W, H, s, name)
    img = b["layers"][0]["img"]
    tw = b["tw"]
    rng = random.Random(seed + len(name))
    ry, half = rally_road(tw, H, s, name)
    p = _Pic(tw, H, 2, tw)
    for _ in range(int(tw / (30 * s))):                                   # les pins vus du dessus
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        if abs(y - ry(x)) < half + 40 * s:
            continue
        r = rng.uniform(16, 30) * s
        p.disc(x + r * 0.4, y + r * 0.5, r, (20, 30, 16, 120))
        _star(p, x, y, r, (30, 70, 34, 255), None, 0, n=8, inner=0.62, rot=rng.uniform(0, 1))
        _star(p, x - r * 0.1, y - r * 0.1, r * 0.66, (48, 100, 50, 255), None, 0, n=7, inner=0.6, rot=rng.uniform(0, 1))
        p.disc(x - r * 0.15, y - r * 0.15, r * 0.2, (80, 140, 70, 255))
    out = img.convert("RGBA")
    out.alpha_composite(p.done())
    b["layers"][0]["img"] = out.convert("RGB")
    return b


HORSE_LOOKS = {          # sky top, sky bottom, track, track stripe, infield, rail, kind / ciel, piste, intérieur, lisse, genre
    "sw_turf": ((90, 150, 230), (200, 226, 250), (70, 170, 60), (84, 184, 70), (60, 150, 60), (250, 250, 250), "japan"),
    "sw2_turf": ((110, 160, 230), (214, 232, 250), (64, 162, 58), (78, 178, 66), (56, 140, 54), (250, 250, 250), "longchamp"),
    "jgp_dirt": ((120, 170, 230), (220, 236, 250), (196, 160, 104), (186, 150, 96), (70, 160, 70), (60, 160, 90), "dirt"),
}


def build_horse(W, H, s, name, seed=431):
    """The horse races seen from the side, as in Stakes Winner, Stakes Winner 2 and Jockey Grand Prix: the sky, the
    grandstand and its crowd far away (a Japanese course, Longchamp and its windmill, a big stand with its roof), the
    infield and the far rail, the track (green turf and its mown stripes, or brown dirt), the near rail and its posts.
    / Les courses de chevaux vues de côté : la tribune et son public, l'intérieur, la piste de gazon ou de terre."""
    rng = random.Random(seed + len(name))
    top_c, bot_c, track, stripe, infield, rail, kind = HORSE_LOOKS[name]
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, top_c), (0.42, bot_c), (1.0, bot_c)])
    t0, t1 = (v * s for v in HORSE_TRACK)
    layers = []
    far = _Pic(tw, H, 2, tw)
    for _ in range(10):                                                  # nuages
        x, y = rng.uniform(0, tw), rng.uniform(20, 90) * s
        for k in range(5):
            far.disc(x + k * 26 * s, y + rng.uniform(-8, 8) * s, rng.uniform(18, 30) * s, (250, 252, 255, 255))
    hor = 196 * s
    for x in range(-40, int(tw) + 40, int(60 * s)):                      # arbres au loin
        _clump(far, x, hor - rng.uniform(4, 16) * s, rng.uniform(26, 40) * s, rng, ((50, 110, 60), (70, 140, 70)), n=4)
    far.poly([(0, hor), (tw, hor), (tw, H), (0, H)], _rgba(mix(infield, (40, 60, 40), 0.3)))
    x = 120 * s
    while x < tw - 200 * s:                                              # la tribune et son public
        w = rng.uniform(500, 760) * s
        y0 = hor - 70 * s
        if kind == "dirt":
            y0 = hor - 90 * s
        far.poly([(x, y0), (x + w, y0), (x + w, hor), (x, hor)], (226, 226, 230, 255), (120, 120, 130, 255), 2 * s)
        far.poly([(x - 20 * s, y0 - 18 * s), (x + w + 20 * s, y0 - 18 * s), (x + w, y0), (x, y0)],
                 (60, 90, 160, 255) if kind != "longchamp" else (70, 70, 80, 255))
        for row in range(3):
            yy = y0 + 14 * s + row * 16 * s
            xx = x + 8 * s
            while xx < x + w - 8 * s:
                far.disc(xx, yy, 4 * s, _rgba(rng.choice(((220, 60, 60), (60, 90, 200), (240, 220, 80), (250, 250, 250), (60, 60, 60)))))
                xx += rng.uniform(9, 14) * s
        for k in range(int(w / (90 * s)) + 1):
            far.line([(x + k * 90 * s, y0), (x + k * 90 * s, hor)], (150, 150, 160, 255), 2 * s)
        x += w + rng.uniform(300, 600) * s
    if kind == "longchamp":                                              # le moulin de Longchamp
        for mx in (tw * 0.42, tw * 0.92):
            far.poly([(mx - 18 * s, hor), (mx - 12 * s, hor - 80 * s), (mx + 12 * s, hor - 80 * s), (mx + 18 * s, hor)], (240, 236, 226, 255),
                     (120, 110, 100, 255), 1.5 * s)
            far.poly([(mx - 16 * s, hor - 80 * s), (mx, hor - 100 * s), (mx + 16 * s, hor - 80 * s)], (150, 70, 50, 255))
            for a in (20, 110, 200, 290):
                ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                far.line([(mx, hor - 84 * s), (mx + ca * 60 * s, hor - 84 * s + sa * 60 * s)], (110, 90, 70, 255), 5 * s)
    layers.append({"img": far.done(), "y": 0, "f": 0.12, "stage": "far"})
    mid = _Pic(tw, H, 2, tw)
    mid.poly([(0, hor + 10 * s), (tw, hor + 10 * s), (tw, t0), (0, t0)], _rgba(infield))         # l'intérieur de la piste
    for _ in range(40):                                                  # haies et massifs
        x = rng.uniform(0, tw)
        _clump(mid, x, hor + rng.uniform(18, 40) * s, rng.uniform(14, 24) * s, rng, ((40, 120, 50), (60, 150, 60), (230, 120, 160)), n=4)
    for x in range(0, int(tw), int(54 * s)):                              # la lisse du fond
        mid.line([(x, t0 - 26 * s), (x, t0 - 4 * s)], _rgba(mix(rail, (0, 0, 0), 0.15)), 3 * s)
    mid.poly([(0, t0 - 30 * s), (tw, t0 - 30 * s), (tw, t0 - 23 * s), (0, t0 - 23 * s)], _rgba(rail))
    for x in range(int(200 * s), int(tw), int(700 * s)):                  # poteaux de distance
        mid.poly([(x - 4 * s, t0 - 80 * s), (x + 4 * s, t0 - 80 * s), (x + 4 * s, t0 - 4 * s), (x - 4 * s, t0 - 4 * s)], (250, 250, 250, 255))
        mid.disc(x, t0 - 86 * s, 14 * s, (250, 250, 250, 255), (220, 40, 40, 255), 4 * s)
    layers.append({"img": mid.done(), "y": 0, "f": 0.45, "stage": "mid"})
    near = _Pic(tw, H, 2, tw)
    near.poly([(0, t0), (tw, t0), (tw, H), (0, H)], _rgba(track))      # la piste
    if kind == "dirt":
        for _ in range(int(tw / (6 * s))):                               # traces de sabots
            x, y = rng.uniform(0, tw), rng.uniform(t0, t1)
            near.ellipse(x - 4 * s, y - 1.6 * s, x + 4 * s, y + 1.6 * s, _rgba(mix(track, (60, 40, 20), 0.25)))
    else:
        for k in range(0, int(tw / (120 * s)) + 1, 2):                  # les bandes de tonte
            x = k * 120 * s
            near.poly([(x, t0), (x + 120 * s, t0), (x + 80 * s, t1), (x - 40 * s, t1)], _rgba(stripe))
    near.poly([(0, t1), (tw, t1), (tw, H), (0, H)], _rgba(mix(track, (0, 0, 0), 0.12)))
    for x in range(0, int(tw), int(120 * s)):                             # la lisse de devant et ses poteaux
        near.poly([(x - 4 * s, t1 - 6 * s), (x + 4 * s, t1 - 6 * s), (x + 4 * s, H), (x - 4 * s, H)], _rgba(mix(rail, (0, 0, 0), 0.1)))
    near.poly([(0, t1 - 10 * s), (tw, t1 - 10 * s), (tw, t1 + 2 * s), (0, t1 + 2 * s)], _rgba(rail))
    layers.append({"img": near.done(), "y": 0, "f": 1.0, "stage": "near"})
    return {"sky": sky, "layers": _fit(layers), "tw": tw, "amb": {}}


def build_gr_hall(W, H, s, seed=441):
    """Gururin: the hall of the board, as in the game: the blue and purple checkerboard, the golden pillars and their
    round medallions, the golden arches at the top. / La salle : le damier bleu et violet, les piliers dorés et leurs
    médaillons, les arcades dorées en haut."""
    sky = Image.new("RGB", (W, H), (60, 52, 140))
    p = _Pic(W, H, 2, 4 * W)
    c = 46 * s
    for i in range(int(W / c) + 1):                                       # le damier
        for j in range(int(H / c) + 1):
            if (i + j) % 2:
                p.poly([(i * c, j * c), ((i + 1) * c, j * c), ((i + 1) * c, (j + 1) * c), (i * c, (j + 1) * c)], (104, 84, 190, 255))
    gold, dark = (230, 186, 80, 255), (130, 90, 30, 255)
    for k in range(9):                                                    # les arcades dorées
        x = k * W / 8
        pts = [(x + math.cos(math.pi * i / 24) * 110 * s, 26 * s + math.sin(math.pi * i / 24) * 70 * s) for i in range(25)]
        p.line(pts, dark, 18 * s)
        p.line(pts, gold, 12 * s)
    p.poly([(0, 0), (W, 0), (W, 26 * s), (0, 26 * s)], gold, dark, 2 * s)
    for x in (W * 0.06, W * 0.5, W * 0.94):                               # les piliers et leurs médaillons
        p.poly([(x - 34 * s, 26 * s), (x + 34 * s, 26 * s), (x + 34 * s, H), (x - 34 * s, H)], gold, dark, 2 * s)
        for k in range(4):
            p.line([(x - 22 * s + k * 15 * s, 40 * s), (x - 22 * s + k * 15 * s, H)], (200, 150, 60, 255), 3 * s)
        p.disc(x, H * 0.56, 46 * s, gold, dark, 3 * s)
        p.disc(x, H * 0.56, 30 * s, (250, 220, 120, 255), dark, 2 * s)
        for a in range(0, 360, 45):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            p.line([(x, H * 0.56), (x + ca * 26 * s, H * 0.56 + sa * 26 * s)], dark, 3 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_gl_street(W, H, s, seed=451):
    """Ghostlop: a city street at night, as in the game: the shop fronts and their lit windows, the signs, the
    pavement, a car parked in front, the street lamps. / Une rue de la ville la nuit : vitrines éclairées, enseignes,
    trottoir, une voiture garée, les réverbères."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (14, 16, 40)), (0.5, (36, 36, 70)), (1.0, (50, 46, 60))])
    p = _Pic(W, H, 2, 4 * W)
    x = -20 * s
    base = 360 * s
    while x < W:                                                          # les immeubles et les boutiques
        w = rng.uniform(150, 260) * s
        hgt = rng.uniform(230, 330) * s
        col = rng.choice(((70, 60, 70), (90, 80, 76), (60, 64, 80), (100, 90, 84), (80, 70, 60)))
        p.poly([(x, base - hgt), (x + w, base - hgt), (x + w, base), (x, base)], _rgba(col), _rgba(mix(col, (0, 0, 0), 0.4)), 2 * s)
        for wy in range(int(base - hgt + 16 * s), int(base - 120 * s), int(34 * s)):
            for wx in range(int(x + 12 * s), int(x + w - 26 * s), int(36 * s)):
                lit = rng.random() < 0.45
                p.poly([(wx, wy), (wx + 20 * s, wy), (wx + 20 * s, wy + 22 * s), (wx, wy + 22 * s)],
                       (250, 210, 120, 255) if lit else _rgba(mix(col, (0, 0, 20), 0.5)))
        p.poly([(x + 10 * s, base - 100 * s), (x + w - 10 * s, base - 100 * s), (x + w - 10 * s, base - 10 * s), (x + 10 * s, base - 10 * s)],
               (250, 230, 170, 255), (40, 36, 40, 255), 3 * s)                 # la vitrine
        for k in range(int((w - 20 * s) / (40 * s))):
            p.line([(x + 30 * s + k * 40 * s, base - 100 * s), (x + 30 * s + k * 40 * s, base - 10 * s)], (120, 100, 80, 255), 2 * s)
        sign = rng.choice(((220, 60, 60), (60, 160, 230), (250, 200, 60), (90, 200, 120)))
        p.poly([(x + 20 * s, base - 130 * s), (x + w - 20 * s, base - 130 * s), (x + w - 20 * s, base - 106 * s), (x + 20 * s, base - 106 * s)],
               _rgba(sign), (30, 30, 30, 255), 2 * s)
        x += w + rng.uniform(4, 16) * s
    p.poly([(0, base), (W, base), (W, base + 26 * s), (0, base + 26 * s)], (130, 126, 120, 255))   # le trottoir
    p.poly([(0, base + 26 * s), (W, base + 26 * s), (W, H), (0, H)], (44, 44, 50, 255))           # la rue
    for lx in (W * 0.1, W * 0.5, W * 0.9):                               # les réverbères
        p.poly([(lx - 4 * s, base + 20 * s), (lx + 4 * s, base + 20 * s), (lx + 4 * s, 110 * s), (lx - 4 * s, 110 * s)], (40, 44, 50, 255))
        p.line([(lx, 112 * s), (lx + 40 * s, 104 * s)], (40, 44, 50, 255), 6 * s)
        p.disc(lx + 44 * s, 108 * s, 12 * s, (255, 240, 180, 255))
    for cx in (W * 0.24, W * 0.76):                                       # voitures garées
        p.poly([(cx - 150 * s, base + 60 * s), (cx - 110 * s, base + 18 * s), (cx + 60 * s, base + 18 * s), (cx + 120 * s, base + 50 * s),
                (cx + 160 * s, base + 60 * s), (cx + 160 * s, base + 92 * s), (cx - 150 * s, base + 92 * s)], (30, 30, 36, 255), (70, 70, 80, 255), 2 * s)
        p.poly([(cx - 96 * s, base + 26 * s), (cx + 50 * s, base + 26 * s), (cx + 92 * s, base + 52 * s), (cx - 120 * s, base + 52 * s)], (70, 90, 110, 255))
        for wx in (-90, 100):
            p.disc(cx + wx * s, base + 92 * s, 22 * s, (14, 14, 16, 255), (90, 90, 96, 255), 4 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def _bear(p, x, y, r, s, fur=(196, 178, 160), dark=(120, 100, 86)):
    """A big plush bear of our own, sitting. / Un gros ours en peluche à nous, assis."""
    ol, ow = _rgba(dark), 3 * s
    p.ellipse(x - r * 0.9, y + r * 0.3, x + r * 0.9, y + r * 2.0, _rgba(fur), ol, ow)            # le corps
    p.ellipse(x - r * 0.5, y + r * 0.7, x + r * 0.5, y + r * 1.7, _rgba(mix(fur, (255, 255, 255), 0.35)))
    for side in (-1, 1):
        p.ellipse(x + side * r * 0.95 - r * 0.3, y + r * 0.5, x + side * r * 0.95 + r * 0.3, y + r * 1.4, _rgba(fur), ol, ow)    # bras
        p.ellipse(x + side * r * 0.6 - r * 0.38, y + r * 1.7, x + side * r * 0.6 + r * 0.38, y + r * 2.25, _rgba(fur), ol, ow)  # pieds
        p.disc(x + side * r * 0.7, y - r * 0.75, r * 0.32, _rgba(fur), ol, ow)                                            # oreilles
        p.disc(x + side * r * 0.7, y - r * 0.75, r * 0.17, _rgba(mix(fur, (255, 200, 200), 0.3)))
    p.disc(x, y, r, _rgba(fur), ol, ow)                                                                                  # la tête
    p.ellipse(x - r * 0.4, y + r * 0.1, x + r * 0.4, y + r * 0.6, _rgba(mix(fur, (255, 255, 255), 0.45)), ol, 2 * s)
    p.ellipse(x - r * 0.12, y + r * 0.14, x + r * 0.12, y + r * 0.3, (60, 40, 40, 255))
    for side in (-1, 1):
        p.disc(x + side * r * 0.36, y - r * 0.12, r * 0.1, (30, 24, 24, 255))
    p.poly([(x - r * 0.3, y + r * 0.86), (x + r * 0.3, y + r * 0.86), (x + r * 0.16, y + r * 1.04), (x - r * 0.16, y + r * 1.04)], (220, 80, 110, 255))


def build_pn_forest(W, H, s, seed=461):
    """Pochi and Nyaa: the green forest of the game with its soft lights, and a big plush bear of our own sitting on
    the right. / La forêt verte du jeu et ses lumières douces, un gros ours en peluche à nous assis à droite."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (30, 70, 50)), (0.5, (50, 100, 64)), (1.0, (30, 60, 40))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(26):                                                   # feuillages sombres
        _clump(p, rng.uniform(0, W), rng.uniform(0, H), rng.uniform(60, 120) * s, rng, ((30, 70, 44), (44, 90, 56), (70, 120, 70)), n=6)
    for _ in range(40):                                                   # taches de lumière
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(6, 18) * s
        p.disc(x, y, r, (200, 230, 150, 255))
    for k in range(5):                                                    # rayons
        x = rng.uniform(0, W)
        p.poly([(x, 0), (x + 40 * s, 0), (x - 120 * s, H), (x - 200 * s, H)], (90, 140, 90, 255))
    _bear(p, W - 210 * s, 150 * s, 92 * s, s)
    _bear(p, 190 * s, 190 * s, 70 * s, s, (236, 236, 240), (130, 130, 150))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_pz_tower(W, H, s, seed=471):
    """Puzzled: the green hills under a blue sky with white clouds, as on the title of the game, and the two brick
    towers whose wells hold the game, their stone arches and battlements. / Les collines vertes sous le ciel bleu, et
    les deux tours de briques dont les puits tiennent le jeu, leurs arches et leurs créneaux."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (90, 150, 230)), (0.55, (190, 220, 250)), (1.0, (190, 220, 250))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(9):                                                    # nuages
        x, y = rng.uniform(0, W), rng.uniform(20, 120) * s
        for k in range(6):
            p.disc(x + k * 24 * s, y + rng.uniform(-10, 10) * s, rng.uniform(18, 30) * s, (252, 252, 255, 255))
    for k, (col, y0) in enumerate((((96, 160, 80), 250), ((80, 140, 64), 300), ((64, 120, 52), 350))):    # les collines
        pts = [(0, H)]
        for i in range(0, 41):
            x = i * W / 40
            pts.append((x, (y0 + 30 * math.sin(x / W * 6.3 * (k + 1) + k * 1.7)) * s))
        pts.append((W, H))
        p.poly(pts, _rgba(col))
    c = PZ_CELL * s
    for cx in (v * s for v in PZ_WELLS):                                  # les tours de briques
        w = PZ_COLS * c
        x0, x1 = cx - w / 2 - 34 * s, cx + w / 2 + 34 * s
        y0 = PZ_TOP * s - 40 * s
        p.poly([(x0, y0), (x1, y0), (x1, H), (x0, H)], (150, 120, 96, 255), (80, 60, 48, 255), 3 * s)
        for row in range(int((H - y0) / (14 * s)) + 1):
            y = y0 + row * 14 * s
            p.line([(x0, y), (x1, y)], (110, 86, 68, 255), 1.6 * s)
            off = (row % 2) * 14 * s
            for x in range(int(x0 + off), int(x1), int(28 * s)):
                p.line([(x, y), (x, y + 14 * s)], (110, 86, 68, 255), 1.6 * s)
        for k in range(int((x1 - x0) / (30 * s)) + 1):                    # les créneaux
            if k % 2 == 0:
                bx = x0 + k * 30 * s
                p.poly([(bx, y0 - 26 * s), (bx + 30 * s, y0 - 26 * s), (bx + 30 * s, y0), (bx, y0)], (150, 120, 96, 255), (80, 60, 48, 255), 3 * s)
        p.poly([(cx - w / 2 - 6 * s, PZ_TOP * s - 6 * s), (cx + w / 2 + 6 * s, PZ_TOP * s - 6 * s), (cx + w / 2 + 6 * s, (PZ_TOP + PZ_ROWS * PZ_CELL) * s + 6 * s),
                (cx - w / 2 - 6 * s, (PZ_TOP + PZ_ROWS * PZ_CELL) * s + 6 * s)], (40, 34, 44, 255), (230, 210, 150, 255), 4 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


hd_bg.BUILDERS.update({"bb_street": build_bb_street, "fs_arena": build_fs_arena, "gr_hall": build_gr_hall, "gl_street": build_gl_street,
                       "pn_forest": build_pn_forest, "pz_tower": build_pz_tower})
hd_bg.BUILDERS.update({name: (lambda W, H, s, n=name: build_ot(W, H, s, n)) for name in ("ot_forest", "ot_road")})
hd_bg.BUILDERS.update({name: (lambda W, H, s, n=name: build_horse(W, H, s, n)) for name in HORSE_LOOKS})
