"""Backdrops of the Capcom CPS shoot'em ups (1.30), drawn by the program after screenshots of the games: the sea and its
battleships of 1944, the clouds of 19XX, the snowy coast of 1941, the base of Varth, the canyon of U.N. Squadron, the
city of Carrier Air Wing, the ruins of Forgotten Worlds, the lava of Giga Wing, the village of Progear, the base of Mars
Matrix, the magic sky of Dimahoo, the coast of Eco Fighters and the desert path of Mercs. Everything is drawn by the
program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this module is imported (by
hd_games13).

Décors des shoot'em ups Capcom CPS (1.30), dessinés par le programme d'après des captures des jeux : la mer et ses
cuirassés de 1944, les nuages de 19XX, la côte enneigée de 1941, la base de Varth, le canyon de U.N. Squadron, la ville de
Carrier Air Wing, les ruines de Forgotten Worlds, la lave de Giga Wing, le village de Progear, la base de Mars Matrix, le
ciel magique de Dimahoo, la côte d'Eco Fighters et la piste du désert de Mercs.
"""

import math
import random

from PIL import Image, ImageFilter

from . import hd_bg
from .hd_bg import vgrad
from .hd_themes3 import _blob, _clump, _fit, _Pic, _rgba

# where the ships, tanks and soldiers of the scenes go, in pixels at s = 1 / où passent navires, chars et soldats
SEA44_LANES = (178, 300)
SEA41_LANES = (190, 250, 300)
VT_LANES = (170, 236, 300)
GW_LANES = (186, 286)
MM_LANES = (176, 300)
MC_ROAD = (150, 404)


def _done(p):
    return p.done().convert("RGB")


def _bands(img, cut, f):
    """A layer cut in two bands at the row cut: two thin layers cost less to draw than one tall one.
    / Une couche coupée en deux bandes : deux couches minces coûtent moins à dessiner qu'une haute."""
    return [{"img": img.crop((0, 0, img.width, cut)), "y": 0, "f": f, "stage": "mid"},
            {"img": img.crop((0, cut, img.width, img.height)), "y": cut, "f": f, "stage": "mid"}]


def _ripples(p, rng, tw, H, s, n, light, dark):
    """Little waves of a sea seen from the sky. / Les vaguelettes d'une mer vue du ciel."""
    for _ in range(n):
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        w = rng.uniform(8, 22) * s
        col = light if rng.random() < 0.6 else dark
        p.line([(x, y), (x + w * 0.5, y - 2.5 * s), (x + w, y)], col, 1.6 * s)


# ---------------------------------------------------------------------------- 1944
def battleship(p, x, y, L, s, rng, wk=None):
    """A battleship seen from the sky, bow to the right: the wooden deck, the grey turrets and their guns, the
    superstructure in the middle, the white wake behind. / Un cuirassé vu du ciel, proue à droite."""
    h = L * 0.17
    line = (40, 36, 34, 255)
    if wk is not None:                                                 # the wake opens behind it / le sillage
        for k in range(40):
            t = k / 39
            r = h * 0.3 + h * 0.55 * t
            cx = x - L * 0.45 - t * L * 0.8
            wk.ellipse(cx - r, y - r * 0.6, cx + r, y + r * 0.6, (220, 234, 250, int(90 * (1 - t) + 16)))
        for k in range(30):                                            # foam / l'écume
            t = rng.uniform(0, 1)
            r = (3 + 8 * (1 - t)) * s
            wk.disc(x - L * 0.47 - t * L * 0.7, y + rng.uniform(-0.45, 0.45) * h * (0.5 + t), r, (240, 246, 255, int(150 * (1 - t)) + 20))
        for sgn in (1, -1):                                            # the bow waves / les vagues d'étrave
            wk.line([(x + L * 0.44, y + sgn * h * 0.12), (x + L * 0.3, y + sgn * h * 0.62), (x + L * 0.12, y + sgn * h * 0.86)], (210, 228, 250, 150),
                   3 * s)
    hull = [(x + L * 0.5, y), (x + L * 0.36, y - h * 0.5), (x - L * 0.42, y - h * 0.5), (x - L * 0.5, y - h * 0.3),
            (x - L * 0.5, y + h * 0.3), (x - L * 0.42, y + h * 0.5), (x + L * 0.36, y + h * 0.5)]
    p.poly(hull, (96, 100, 108, 255), line, 2 * s)
    deck = [(x + L * 0.46, y), (x + L * 0.34, y - h * 0.38), (x - L * 0.4, y - h * 0.38), (x - L * 0.46, y - h * 0.22),
            (x - L * 0.46, y + h * 0.22), (x - L * 0.4, y + h * 0.38), (x + L * 0.34, y + h * 0.38)]
    p.poly(deck, (176, 132, 84, 255))
    for k in range(1, 9):                                              # the planks / les lattes du pont
        yy = y - h * 0.38 + k * h * 0.76 / 9
        p.line([(x - L * 0.42, yy), (x + L * 0.36, yy)], (150, 110, 66, 255), 1.0 * s)
    p.poly([(x - L * 0.16, y - h * 0.32), (x + L * 0.1, y - h * 0.32), (x + L * 0.14, y), (x + L * 0.1, y + h * 0.32),
            (x - L * 0.16, y + h * 0.32)], (120, 124, 132, 255), line, 1.6 * s)          # superstructure / la superstructure
    p.disc(x - L * 0.03, y, h * 0.22, (150, 154, 160, 255), line, 1.4 * s)
    p.line([(x - L * 0.1, y), (x + L * 0.06, y)], (60, 60, 66, 255), 2.4 * s)
    for tx in (0.26, 0.17, -0.25, -0.34):                              # the turrets and their guns / les tourelles
        cx = x + L * tx
        aim = 1 if tx > 0 else -1
        for gy in (-0.08, 0.08):
            p.line([(cx, y + h * gy), (cx + aim * L * 0.09, y + h * gy)], (50, 50, 56, 255), 2.2 * s)
        p.disc(cx, y, h * 0.2, (128, 132, 140, 255), line, 1.4 * s)
        p.disc(cx - aim * h * 0.05, y, h * 0.08, (90, 94, 100, 255))
    for k in range(5):                                                 # little guns along the sides / petits canons
        xx = x - L * 0.3 + k * L * 0.14
        for sgn in (1, -1):
            p.disc(xx, y + sgn * h * 0.42, 2.2 * s, (70, 70, 76, 255))


def build_c44_sea(W, H, s, seed=301):
    """1944 seen from the sky, as in the game: the deep blue Pacific and its little waves, huge battleships with
    their wooden decks and their wakes, a small atoll now and then. / La mer bleu profond, d'énormes cuirassés et
    leur sillage, comme dans le jeu."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (40, 82, 160, 255))
    for _ in range(int(tw * H / (2600 * s * s))):                        # darker and lighter patches of the sea
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        r = rng.uniform(30, 90) * s
        p.ellipse(x - r * 1.6, y - r * 0.6, x + r * 1.6, y + r * 0.6, _rgba(rng.choice(((38, 79, 156), (43, 86, 165)))))
    _ripples(p, rng, tw, H, s, int(tw * H / (320 * s * s)), (120, 160, 225, 255), (28, 62, 130, 255))
    ships = [(tw * 0.2, 236 * s, 900 * s), (tw * 0.7, 250 * s, 980 * s)]
    wk = _Pic(tw, H, 2, tw)
    sh = _Pic(tw, H, 2, tw)
    for x, y, L in ships:
        battleship(sh, x, y, L, s, rng, wk)
    for x in (tw * 0.45, tw * 0.95):                                     # an atoll / un atoll
        y = rng.choice((90, 380)) * s
        pts = _blob(x, y, 90 * s, 46 * s, rng)
        p.poly(pts, (110, 190, 200, 255))
        p.poly(_blob(x, y, 66 * s, 30 * s, rng), (226, 210, 160, 255))
        for _ in range(7):
            _clump(p, x + rng.uniform(-40, 40) * s, y + rng.uniform(-14, 14) * s, rng.uniform(12, 20) * s, rng,
                   ((40, 110, 50), (70, 150, 60), (130, 190, 80)), n=6)
    img = p.done()
    img.alpha_composite(wk.done().filter(ImageFilter.GaussianBlur(3 * s)))
    img.alpha_composite(sh.done())
    return {"sky": Image.new("RGB", (W, H), (40, 82, 160)), "layers": [{"img": img.convert("RGB"), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw,
            "amb": {}}


# ---------------------------------------------------------------------------- 19XX
def build_c19_sky(W, H, s, seed=302):
    """19XX seen from high in the sky, as in the game: the sea far below with its islands, banks of white clouds that
    fly by faster above it. / La mer tout en bas et ses îles, des bancs de nuages blancs qui passent plus vite."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (44, 96, 176, 255))
    _ripples(p, rng, tw, H, s, int(tw * H / (700 * s * s)), (90, 140, 210, 255), (36, 84, 160, 255))
    for k in range(5):                                                   # islands far below / des îles tout en bas
        x, y = tw * (0.1 + 0.2 * k) + rng.uniform(-60, 60) * s, rng.uniform(70, H / s - 70) * s
        r = rng.uniform(50, 90) * s
        p.poly(_blob(x, y, r * 1.3, r * 0.8, rng), (90, 170, 190, 255))
        p.poly(_blob(x, y, r * 1.05, r * 0.6, rng), (110, 140, 70, 255))
        p.poly(_blob(x + r * 0.1, y - r * 0.05, r * 0.6, r * 0.32, rng), (76, 112, 52, 255))
    far = _done(p)
    c = _Pic(tw, H, 2, tw)                                               # the clouds above / les nuages au-dessus
    x = 0.0
    while x < tw:
        y = rng.uniform(40, H / s - 40) * s
        n = rng.randint(4, 7)
        for i in range(n):
            cx, cy = x + i * rng.uniform(40, 70) * s, y + rng.uniform(-40, 40) * s
            r = rng.uniform(50, 90) * s
            c.poly(_blob(cx + 8 * s, cy + 10 * s, r * 1.2, r * 0.75, rng), (150, 170, 200, 150))
        for i in range(n):
            cx, cy = x + i * rng.uniform(40, 70) * s, y + rng.uniform(-40, 40) * s
            r = rng.uniform(45, 80) * s
            c.poly(_blob(cx, cy, r * 1.2, r * 0.75, rng), (232, 238, 248, 235))
            c.poly(_blob(cx - r * 0.2, cy - r * 0.2, r * 0.7, r * 0.4, rng), (255, 255, 255, 240))
        x += rng.uniform(520, 820) * s
    return {"sky": Image.new("RGB", (W, H), (44, 96, 176)),
            "layers": _fit([{"img": far, "y": 0, "f": 0.6, "stage": "far"}, {"img": c.done(), "y": 0, "f": 1.5, "stage": "mid"}]),
            "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- 1941
def build_c41_coast(W, H, s, seed=303):
    """1941 seen from the sky, as in the game: a dark blue sea between two snowy rocky coasts, the white foam along
    the rocks. / Une mer bleu sombre entre deux côtes rocheuses enneigées, l'écume blanche le long des rochers."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (24, 52, 140, 255))
    for _ in range(int(tw * H / (1500 * s * s))):
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        r = rng.uniform(20, 60) * s
        p.ellipse(x - r * 2, y - r * 0.5, x + r * 2, y + r * 0.5, _rgba(rng.choice(((20, 44, 124), (34, 66, 160))), 140))
    _ripples(p, rng, tw, H, s, int(tw * H / (360 * s * s)), (80, 120, 210, 255), (16, 36, 100, 255))
    n = 48
    for top in (True, False):                                            # the two coasts / les deux côtes
        ph = rng.uniform(0, math.tau)
        pts = []
        for i in range(n + 1):
            x = tw * i / n
            d = (70 + 34 * math.sin(i / n * math.tau * 3 + ph) + 18 * math.sin(i / n * math.tau * 7 + ph * 2)) * s
            pts.append((x, d if top else H - d))
        edge = pts
        land = edge + ([(tw, 0), (0, 0)] if top else [(tw, H), (0, H)])
        p.line(edge, (236, 244, 255, 255), 10 * s)                        # foam / l'écume
        p.poly(land, (120, 122, 132, 255))
        for _ in range(int(tw / (26 * s))):                              # rocks and snow / rochers et neige
            x = rng.uniform(0, tw)
            i = min(n, int(x / tw * n))
            yy = edge[i][1]
            y = rng.uniform(0, yy - 6 * s) if top else rng.uniform(yy + 6 * s, H)
            r = rng.uniform(10, 26) * s
            p.poly(_blob(x, y, r, r * 0.7, rng, 12, 0.3), _rgba(rng.choice(((96, 98, 110), (140, 142, 152), (80, 82, 92)))))
            p.poly(_blob(x - r * 0.2, y - r * 0.25, r * 0.7, r * 0.4, rng, 10, 0.3), (240, 244, 252, 255))
    return {"sky": Image.new("RGB", (W, H), (24, 52, 140)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw,
            "amb": {}}


# ---------------------------------------------------------------------------- Varth
def build_vt_base(W, H, s, seed=304):
    """Varth seen from the sky, as in the game: a military base of teal metal plates, rows of rivets, hangars, round
    landing pads ringed with rose, the lines of the taxiways. / Une base militaire de plaques de métal bleu-vert,
    hangars et aires d'atterrissage rondes, comme dans le jeu."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (24, 104, 112, 255))
    step = 120 * s
    for i in range(int(tw / step) + 1):                                  # the plates / les plaques
        for j in range(int(H / step) + 1):
            x, y = i * step, j * step
            tone = rng.choice(((30, 118, 126), (22, 98, 106), (36, 128, 134)))
            p.poly([(x + 3 * s, y + 3 * s), (x + step - 3 * s, y + 3 * s), (x + step - 3 * s, y + step - 3 * s), (x + 3 * s, y + step - 3 * s)],
                   _rgba(tone), (14, 70, 76, 255), 2 * s)
            for k in range(4):
                p.disc(x + 10 * s + k * (step - 20 * s) / 3, y + 9 * s, 1.8 * s, (90, 170, 176, 255))
    for k in range(int(tw / (480 * s))):                                 # taxiways / les voies de circulation
        x = k * 480 * s + 120 * s
        p.poly([(x, 0), (x + 70 * s, 0), (x + 70 * s, H), (x, H)], (60, 70, 76, 255))
        for j in range(int(H / (40 * s))):
            p.line([(x + 35 * s, j * 40 * s + 6 * s), (x + 35 * s, j * 40 * s + 24 * s)], (230, 220, 120, 255), 3 * s)
    for k in range(int(tw / (640 * s))):                                 # hangars and pads / hangars et aires
        x = k * 640 * s + 330 * s
        y = rng.choice((90, 360)) * s
        p.poly([(x - 90 * s, y - 50 * s), (x + 90 * s, y - 50 * s), (x + 90 * s, y + 50 * s), (x - 90 * s, y + 50 * s)],
               (70, 84, 92, 255), (20, 30, 34, 255), 3 * s)
        for j in range(6):
            p.line([(x - 84 * s, y - 40 * s + j * 16 * s), (x + 84 * s, y - 40 * s + j * 16 * s)], (100, 116, 124, 255), 3 * s)
        cy = (460 - y / s) * s
        p.disc(x + 40 * s, cy, 54 * s, (200, 140, 150, 255), (40, 30, 34, 255), 3 * s)
        p.disc(x + 40 * s, cy, 38 * s, (60, 120, 126, 255))
        p.line([(x + 14 * s, cy), (x + 66 * s, cy)], (230, 230, 230, 255), 5 * s)
        p.line([(x + 40 * s, cy - 26 * s), (x + 40 * s, cy + 26 * s)], (230, 230, 230, 255), 5 * s)
    return {"sky": Image.new("RGB", (W, H), (24, 104, 112)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw,
            "amb": {}}


# ---------------------------------------------------------------------------- U.N. Squadron
def build_un_canyon(W, H, s, seed=305):
    """U.N. Squadron seen from the side, as in the game: a pale sky, mauve mesas far away, the towers and pipes of a
    refinery, the grey concrete ground where the tanks drive. / Un ciel pâle, des mesas mauves au loin, les tours
    d'une raffinerie, le sol de béton gris des chars."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (120, 170, 222)), (0.55, (196, 214, 236)), (1.0, (226, 226, 232))])
    far = _Pic(tw, H, 2, tw)
    base = 330 * s
    x = 0.0
    while x < tw:                                                        # the mesas / les mesas
        w = rng.uniform(260, 520) * s
        top = base - rng.uniform(110, 210) * s
        pts = [(x - 40 * s, base), (x + w * 0.1, top + 20 * s), (x + w * 0.25, top), (x + w * 0.6, top + rng.uniform(-10, 20) * s),
               (x + w * 0.8, top + 30 * s), (x + w + 40 * s, base)]
        far.poly(pts, (156, 116, 156, 255))
        far.poly([(x + w * 0.3, top + 6 * s), (x + w * 0.6, top + 10 * s), (x + w * 0.7, base), (x + w * 0.25, base)], (130, 92, 134, 255))
        for k in range(3):
            yy = top + (k + 1) * (base - top) / 4
            far.line([(x + w * 0.12, yy), (x + w * 0.86, yy + 4 * s)], (176, 136, 170, 255), 2 * s)
        x += w * rng.uniform(0.7, 1.0)
    mid = _Pic(tw, H, 2, tw)
    gb = 392 * s
    for k in range(int(tw / (300 * s))):                                 # the refinery / la raffinerie
        x = k * 300 * s + rng.uniform(0, 80) * s
        h = rng.uniform(150, 240) * s
        w = rng.uniform(18, 30) * s
        mid.poly([(x, gb), (x, gb - h), (x + w, gb - h), (x + w, gb)], (150, 152, 160, 255), (70, 70, 80, 255), 2 * s)
        for j in range(int(h / (26 * s))):
            mid.line([(x - 6 * s, gb - j * 26 * s - 10 * s), (x + w + 6 * s, gb - j * 26 * s - 10 * s)], (90, 92, 104, 255), 2 * s)
        mid.disc(x + w / 2, gb - h, 4 * s, (230, 80, 40, 255))
        tx = x + rng.uniform(60, 120) * s                                # a round tank / une cuve ronde
        r = rng.uniform(30, 46) * s
        mid.poly([(tx - r, gb), (tx - r, gb - r * 1.4), (tx + r, gb - r * 1.4), (tx + r, gb)], (176, 176, 184, 255), (80, 80, 90, 255), 2 * s)
        mid.ellipse(tx - r, gb - r * 1.4 - r * 0.3, tx + r, gb - r * 1.4 + r * 0.3, (196, 196, 204, 255), (80, 80, 90, 255), 2 * s)
        mid.line([(x + w, gb - h * 0.6), (tx, gb - r * 1.2)], (110, 110, 120, 255), 4 * s)
    near = _Pic(tw, H, 2, tw)
    near.poly([(0, gb), (tw, gb), (tw, H), (0, H)], (150, 150, 152, 255))
    near.poly([(0, gb), (tw, gb), (tw, gb + 8 * s), (0, gb + 8 * s)], (110, 110, 116, 255))
    for k in range(int(tw / (90 * s))):
        x = k * 90 * s
        near.line([(x, gb + 34 * s), (x + 46 * s, gb + 34 * s)], (230, 220, 150, 255), 4 * s)
        near.line([(x + 20 * s, gb + 10 * s), (x - 10 * s, H)], (136, 136, 140, 255), 2 * s)
    return {"sky": sky, "layers": _fit([{"img": far.done(), "y": 0, "f": 0.25, "stage": "far"}, {"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"},
                                         {"img": near.done(), "y": 0, "f": 1.0, "stage": "near"}]), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Carrier Air Wing
def build_ca_city(W, H, s, seed=306):
    """Carrier Air Wing seen from the side, as in the game: a blue sky with white clouds, and far below a whole
    city seen at an angle, blocks of buildings, green parks and avenues, hazy toward the horizon. / Un ciel bleu et
    ses nuages, et tout en bas une ville vue de biais, brumeuse vers l'horizon."""
    rng = random.Random(seed)
    tw = 2 * W
    hz = 236 * s                                                         # the horizon / l'horizon
    sky = vgrad(W, H, [(0.0, (70, 130, 210)), (hz / H * 0.98, (180, 206, 232)), (1.0, (150, 160, 150))])
    city = _Pic(tw, H, 2, tw)
    city.poly([(0, hz), (tw, hz), (tw, H), (0, H)], (124, 134, 120, 255))
    y = hz
    while y < H:                                                         # rows of blocks, bigger closer / rangées d'immeubles
        k = (y - hz) / (H - hz)
        bh = (4 + 26 * k) * rng.uniform(0.8, 1.2) * s
        x = rng.uniform(0, 20) * s
        while x < tw:
            bw = rng.uniform(10, 46) * (0.4 + k) * s
            r = rng.random()
            if r < 0.08:                                                 # an avenue / une avenue
                x += (8 + 22 * k) * s
                continue
            if r < 0.2:                                                  # a park / un parc
                city.poly([(x, y), (x + bw * 1.5, y), (x + bw * 1.5, y + bh), (x, y + bh)], (84, 130, 70, 255))
                for _ in range(3):
                    city.disc(x + rng.uniform(0, bw * 1.5), y + rng.uniform(0, bh), (2 + 4 * k) * s, (60, 104, 52, 255))
                x += bw * 1.5 + 2 * s
                continue
            col = rng.choice(((170, 170, 166), (150, 154, 150), (196, 190, 180), (120, 126, 130), (186, 176, 160), (210, 204, 196)))
            tall = bh * rng.uniform(0.0, 0.6) if rng.random() < 0.3 else 0
            city.poly([(x, y + bh * 0.25 - tall), (x + bw, y + bh * 0.25 - tall), (x + bw, y + bh), (x, y + bh)], _rgba(col))
            city.poly([(x, y - tall), (x + bw, y - tall), (x + bw, y + bh * 0.25 - tall), (x, y + bh * 0.25 - tall)],
                      _rgba(tuple(min(255, c + 34) for c in col)))
            city.poly([(x + bw, y + bh * 0.25 - tall), (x + bw + bw * 0.12, y + bh * 0.3 - tall), (x + bw + bw * 0.12, y + bh), (x + bw, y + bh)],
                      (70, 76, 80, 160))                                 # its shadow / son ombre
            x += bw + rng.uniform(1, 5) * (0.4 + k) * s
        y += bh + (2 + 5 * k) * s
    col = Image.new("RGBA", (1, H), (0, 0, 0, 0))                         # haze over the far city / brume au loin
    for yy in range(int(hz), H):
        col.putpixel((0, yy), (196, 210, 226, int(70 + 130 * max(0.0, 1 - (yy - hz) / (H - hz) * 1.6))))
    cimg = city.done()
    cimg.alpha_composite(col.resize((tw, H)))
    clouds = _Pic(tw, H, 2, tw)
    for _ in range(9):
        cx, cy = rng.uniform(0, tw), rng.uniform(30, hz / s - 20) * s
        for i in range(5):
            r = rng.uniform(26, 56) * s
            clouds.poly(_blob(cx + i * 40 * s, cy + rng.uniform(-14, 14) * s, r * 1.4, r * 0.6, rng), (250, 252, 255, 220))
    return {"sky": sky, "layers": _fit([{"img": cimg, "y": 0, "f": 0.5, "stage": "far"}, {"img": clouds.done(), "y": 0, "f": 1.2, "stage": "mid"}]),
            "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Forgotten Worlds
def build_fw_ruins(W, H, s, seed=307):
    """Forgotten Worlds seen from the side, as in the game: a black sky full of stars, a huge green planet, the
    broken towers of a dead city, a fallen highway, rubble on the ground. / Un ciel noir étoilé, une énorme planète
    verte, les tours brisées d'une ville morte, une autoroute effondrée."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (6, 6, 20)), (0.7, (20, 22, 46)), (1.0, (40, 40, 60))])
    planet = _Pic(W, H, 2, W)                                            # the green planet / la planète verte
    px, py, pr = W * 0.62, 120 * s, 96 * s
    planet.disc(px, py, pr * 1.18, (60, 120, 70, 50))
    planet.disc(px, py, pr, (110, 160, 90, 255))
    planet.chord(px - pr, py - pr, px + pr, py + pr, 120, 300, (80, 126, 70, 255))
    for _ in range(9):
        a, d = rng.uniform(0, math.tau), rng.uniform(0, 0.75) * pr
        r = rng.uniform(6, 16) * s
        planet.disc(px + math.cos(a) * d, py + math.sin(a) * d, r, (90, 136, 76, 255), (140, 186, 116, 255), 1.5 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(planet.done())
    sky = sky.convert("RGB")
    stars = [(rng.uniform(0, W), rng.uniform(0, 230 * s), rng.uniform(1.0, 3.0), rng.uniform(0, 6)) for _ in range(40)]
    far = _Pic(tw, H, 2, tw)
    base = 380 * s
    x = 0.0
    while x < tw:                                                        # broken towers / tours brisées
        w = rng.uniform(50, 110) * s
        h = rng.uniform(140, 290) * s
        top = base - h
        pts = [(x, base), (x, top + rng.uniform(0, 30) * s)]
        for k in range(4):
            pts.append((x + w * (k + 1) / 5, top + rng.uniform(-10, 40) * s))
        pts += [(x + w, top + rng.uniform(0, 40) * s), (x + w, base)]
        far.poly(pts, (66, 70, 86, 255), (30, 32, 44, 255), 2 * s)
        for j in range(int(h / (22 * s)) - 1):                           # dead windows / fenêtres mortes
            for i in range(int(w / (16 * s))):
                if rng.random() < 0.55:
                    wx, wy = x + 6 * s + i * 16 * s, top + 30 * s + j * 22 * s
                    far.poly([(wx, wy), (wx + 8 * s, wy), (wx + 8 * s, wy + 10 * s), (wx, wy + 10 * s)], (34, 36, 50, 255))
        x += w + rng.uniform(20, 90) * s
    mid = _Pic(tw, H, 2, tw)
    hy = 300 * s
    for k in range(int(tw / (700 * s))):                                 # the fallen highway / l'autoroute effondrée
        x = k * 700 * s + 100 * s
        L = rng.uniform(380, 520) * s
        drop = rng.uniform(20, 60) * s
        mid.poly([(x, hy), (x + L, hy + drop), (x + L, hy + drop + 22 * s), (x, hy + 22 * s)], (124, 108, 96, 255), (50, 40, 36, 255), 2 * s)
        for j in range(4):
            px_ = x + 40 * s + j * (L - 80 * s) / 3
            mid.poly([(px_ - 10 * s, hy + 20 * s + drop * j / 3), (px_ + 10 * s, hy + 20 * s + drop * j / 3), (px_ + 14 * s, base + 30 * s),
                      (px_ - 14 * s, base + 30 * s)], (100, 88, 80, 255), (50, 40, 36, 255), 2 * s)
        for j in range(8):                                               # bent girders / poutrelles tordues
            gx = x + L - 30 * s + j * 6 * s
            mid.line([(gx, hy + drop + 10 * s), (gx + 18 * s, hy + drop + 40 * s + j * 4 * s)], (90, 70, 60, 255), 2 * s)
    near = _Pic(tw, H, 2, tw)
    near.poly([(0, 404 * s), (tw, 404 * s), (tw, H), (0, H)], (70, 76, 96, 255))
    for _ in range(int(tw / (14 * s))):                                  # rubble / gravats
        x, y = rng.uniform(0, tw), rng.uniform(396, 460) * s
        r = rng.uniform(5, 16) * s
        near.poly(_blob(x, y, r * 1.3, r * 0.7, rng, 10, 0.35), _rgba(rng.choice(((96, 100, 120), (120, 120, 136), (60, 64, 80)))))
    return {"sky": sky, "layers": _fit([{"img": far.done(), "y": 0, "f": 0.3, "stage": "far"}, {"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"},
                                         {"img": near.done(), "y": 0, "f": 1.0, "stage": "near"}]), "tw": tw, "amb": {"stars": stars}}


# ---------------------------------------------------------------------------- Giga Wing
def build_gw_lava(W, H, s, seed=308):
    """Giga Wing seen from the sky, as in the game: an old fortress of grey steel plates, riveted, cut by winding
    channels of glowing lava, rails and green bunkers along them. / Une vieille forteresse de plaques d'acier grises,
    coupée de canaux de lave brûlante, comme dans le jeu."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (110, 102, 98, 255))
    step = 64 * s
    for i in range(int(tw / step) + 1):                                  # steel plates / plaques d'acier
        for j in range(int(H / step) + 1):
            x, y = i * step, j * step
            p.poly([(x + 2 * s, y + 2 * s), (x + step - 2 * s, y + 2 * s), (x + step - 2 * s, y + step - 2 * s), (x + 2 * s, y + step - 2 * s)],
                   _rgba(rng.choice(((116, 108, 104), (104, 96, 92), (124, 116, 110)))), (74, 68, 66, 255), 1.5 * s)
            p.disc(x + 8 * s, y + 8 * s, 2 * s, (150, 144, 140, 255))
    n = 60
    for lane, amp, ph in ((GW_LANES[0], 40, 0.0), (GW_LANES[1] + 60, 30, 2.0)):   # the lava channels / les canaux de lave
        pts = [(tw * i / n, (lane + amp * math.sin(i / n * math.tau * 3 + ph)) * s) for i in range(n + 1)]
        p.line(pts, (60, 50, 46, 255), 64 * s)
        p.line(pts, (210, 80, 20, 255), 48 * s)
        p.line(pts, (250, 150, 40, 255), 30 * s)
        p.line(pts, (255, 220, 120, 255), 10 * s)
        for i in range(0, n, 3):                                         # crust on the lava / croûte sur la lave
            x, y = pts[i]
            p.ellipse(x - 14 * s, y - 6 * s, x + 14 * s, y + 6 * s, (150, 50, 20, 255))
        for sgn in (1, -1):                                              # rails along / rails le long
            p.line([(x_, y_ + sgn * 40 * s) for x_, y_ in pts], (60, 56, 56, 255), 4 * s)
    for k in range(int(tw / (420 * s))):                                 # green bunkers / bunkers verts
        x, y = k * 420 * s + 200 * s, rng.choice((60, 236, 410)) * s
        p.poly([(x - 40 * s, y - 26 * s), (x + 40 * s, y - 26 * s), (x + 40 * s, y + 26 * s), (x - 40 * s, y + 26 * s)],
               (80, 110, 70, 255), (30, 40, 26, 255), 2.5 * s)
        for j in range(5):
            p.line([(x - 34 * s, y - 20 * s + j * 10 * s), (x + 34 * s, y - 20 * s + j * 10 * s)], (60, 86, 52, 255), 3 * s)
    return {"sky": Image.new("RGB", (W, H), (110, 102, 98)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw,
            "amb": {}}


# ---------------------------------------------------------------------------- Progear
def build_pg_village(W, H, s, seed=309):
    """Progear seen from the side, as in the game: a hazy golden sky, green hills, an old European town with stone
    houses and red roofs, a great stone aqueduct, the green treetops in front. / Un ciel doré et brumeux, des collines
    vertes, une vieille ville aux toits rouges, un grand aqueduc de pierre."""
    rng = random.Random(seed)
    tw = 2 * W
    sky = vgrad(W, H, [(0.0, (196, 196, 180)), (0.5, (232, 220, 186)), (1.0, (214, 206, 176))])
    far = _Pic(tw, H, 2, tw)
    n = 40
    pts = [(tw * i / n, (250 + 30 * math.sin(i / n * math.tau * 2) + 16 * math.sin(i / n * math.tau * 5)) * s) for i in range(n + 1)]
    far.poly(pts + [(tw, H), (0, H)], (128, 150, 106, 255))
    pts2 = [(tw * i / n, (300 + 24 * math.sin(i / n * math.tau * 3 + 1)) * s) for i in range(n + 1)]
    far.poly(pts2 + [(tw, H), (0, H)], (104, 132, 84, 255))
    mid = _Pic(tw, H, 2, tw)
    gb = 400 * s
    ay = 296 * s                                                         # the aqueduct / l'aqueduc
    for k in range(int(tw / (900 * s))):
        x0 = k * 900 * s + 420 * s
        span = 70 * s
        x1 = x0 + span * 6 + 12 * s
        mid.poly([(x0, ay - 30 * s), (x1, ay - 30 * s), (x1, gb), (x0, gb)], (184, 172, 150, 255), (90, 80, 70, 255), 2 * s)
        mid.line([(x0, ay - 22 * s), (x1, ay - 22 * s)], (150, 138, 118, 255), 2 * s)
        for j in range(6):
            ax = x0 + 12 * s + j * span
            w = span - 12 * s
            pts = [(ax, gb)] + [(ax + w / 2 - math.cos(a_ / 8 * math.pi) * w / 2, ay + 30 * s - math.sin(a_ / 8 * math.pi) * 26 * s)
                                for a_ in range(9)] + [(ax + w, gb)]
            mid.poly(pts, (112, 138, 92, 255), (90, 80, 70, 255), 2 * s)
    for k in range(int(tw / (150 * s))):                                 # the houses / les maisons
        x = k * 150 * s + rng.uniform(0, 40) * s
        if any(abs(x - (j * 900 * s + 420 * s + 210 * s)) < 260 * s for j in range(3)):
            continue
        w, h = rng.uniform(70, 110) * s, rng.uniform(70, 130) * s
        top = gb - h
        wall = rng.choice(((214, 200, 170), (196, 184, 160), (226, 214, 186)))
        mid.poly([(x, gb), (x, top), (x + w, top), (x + w, gb)], _rgba(wall), (90, 76, 60, 255), 2 * s)
        mid.poly([(x - 8 * s, top), (x + w / 2, top - rng.uniform(30, 50) * s), (x + w + 8 * s, top)], (150, 70, 50, 255), (80, 40, 30, 255), 2 * s)
        for j in range(int(h / (34 * s))):
            for i in range(int(w / (30 * s))):
                wx, wy = x + 10 * s + i * 30 * s, top + 12 * s + j * 34 * s
                mid.poly([(wx, wy), (wx + 12 * s, wy), (wx + 12 * s, wy + 18 * s), (wx, wy + 18 * s)], (70, 76, 90, 255))
    near = _Pic(tw, H, 2, tw)
    near.poly([(0, 418 * s), (tw, 418 * s), (tw, H), (0, H)], (60, 96, 50, 255))
    for _ in range(int(tw / (30 * s))):                                  # treetops / cimes d'arbres
        _clump(near, rng.uniform(0, tw), rng.uniform(410, 440) * s, rng.uniform(26, 44) * s, rng, ((44, 80, 40), (70, 112, 54), (120, 160, 80)), n=7)
    return {"sky": sky, "layers": _fit([{"img": far.done(), "y": 0, "f": 0.2, "stage": "far"}, {"img": mid.done(), "y": 0, "f": 0.55, "stage": "mid"},
                                         {"img": near.done(), "y": 0, "f": 1.0, "stage": "near"}]), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Mars Matrix
def build_mm_base(W, H, s, seed=310):
    """Mars Matrix seen from the sky, as in the game: a rust-red mechanical base, plates and seams, big round pads
    with a cross, pipes, yellow and black warning stripes. / Une base mécanique rouille, de grandes aires rondes à
    croix, des tuyaux, des bandes jaunes et noires."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (128, 64, 34, 255))
    step = 92 * s
    for i in range(int(tw / step) + 1):
        for j in range(int(H / step) + 1):
            x, y = i * step, j * step
            p.poly([(x + 3 * s, y + 3 * s), (x + step - 3 * s, y + 3 * s), (x + step - 3 * s, y + step - 3 * s), (x + 3 * s, y + step - 3 * s)],
                   _rgba(rng.choice(((150, 78, 40), (136, 70, 36), (164, 88, 46)))), (80, 36, 20, 255), 2 * s)
    for k in range(int(tw / (560 * s))):                                 # round pads / aires rondes
        x, y = k * 560 * s + 260 * s, rng.choice((150, 320)) * s
        p.disc(x, y, 92 * s, (90, 40, 24, 255), (40, 16, 10, 255), 3 * s)
        p.disc(x, y, 76 * s, (190, 110, 60, 255), (100, 50, 26, 255), 3 * s)
        p.disc(x, y, 50 * s, (160, 80, 44, 255))
        p.line([(x - 70 * s, y), (x + 70 * s, y)], (230, 200, 160, 255), 8 * s)
        p.line([(x, y - 70 * s), (x, y + 70 * s)], (230, 200, 160, 255), 8 * s)
    for k in range(int(tw / (380 * s))):                                 # pipes and stripes / tuyaux et bandes
        x = k * 380 * s + 80 * s
        p.line([(x, 0), (x, H)], (90, 46, 26, 255), 22 * s)
        p.line([(x - 5 * s, 0), (x - 5 * s, H)], (200, 120, 70, 255), 5 * s)
        y = rng.uniform(40, 420) * s
        for j in range(8):
            col = (240, 200, 40, 255) if j % 2 == 0 else (30, 24, 20, 255)
            p.poly([(x + 20 * s + j * 16 * s, y), (x + 36 * s + j * 16 * s, y), (x + 28 * s + j * 16 * s, y + 16 * s), (x + 12 * s + j * 16 * s, y + 16 * s)],
                   col)
    return {"sky": Image.new("RGB", (W, H), (128, 64, 34)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw,
            "amb": {}}


# ---------------------------------------------------------------------------- Dimahoo
def build_dh_clouds(W, H, s, seed=311):
    """Dimahoo seen from the sky, as in the game: a magic sky of violet and blue clouds, floating rocks with green
    tops passing above them, little lights. / Un ciel magique de nuages violets et bleus, des rochers flottants
    couverts d'herbe qui passent au-dessus."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (58, 62, 150, 255))
    cl = _Pic(tw, H, 2, tw)
    for _ in range(int(tw * H / (7000 * s * s))):                        # the clouds / les nuages
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        r = rng.uniform(60, 120) * s
        cl.poly(_blob(x, y, r * 1.6, r * 0.8, rng), _rgba(rng.choice(((96, 96, 196), (110, 104, 204), (86, 88, 186))), 170))
        cl.poly(_blob(x - r * 0.2, y - r * 0.2, r * 1.0, r * 0.45, rng), (150, 142, 226, 170))
        cl.poly(_blob(x - r * 0.35, y - r * 0.3, r * 0.5, r * 0.2, rng), (214, 206, 250, 170))
    base = p.done()
    base.alpha_composite(cl.done().filter(ImageFilter.GaussianBlur(5 * s)))
    far = base.convert("RGB")
    isl = _Pic(tw, H, 2, tw)                                             # floating rocks / rochers flottants
    for k in range(5):
        band = (90, 380)[k % 2]
        x, y = tw * (0.1 + 0.2 * k) + rng.uniform(-80, 80) * s, band * s + rng.uniform(-20, 20) * s
        r = rng.uniform(56, 84) * s
        isl.poly(_blob(x + 10 * s, y + 14 * s, r * 1.2, r * 0.8, rng), (30, 24, 60, 110))
        isl.poly(_blob(x, y, r * 1.2, r * 0.8, rng), (126, 100, 92, 255))
        isl.poly(_blob(x - r * 0.1, y - r * 0.1, r * 0.95, r * 0.6, rng), (80, 150, 76, 255))
        for _ in range(4):
            _clump(isl, x + rng.uniform(-0.5, 0.5) * r, y + rng.uniform(-0.3, 0.2) * r, rng.uniform(14, 22) * s, rng,
                   ((40, 100, 50), (70, 140, 60), (150, 200, 100)), n=6)
    stars = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.0, 2.6), rng.uniform(0, 6)) for _ in range(26)]
    return {"sky": Image.new("RGB", (W, H), (64, 66, 150)),
            "layers": _fit([{"img": far, "y": 0, "f": 0.7, "stage": "far"}] + _bands(isl.done(), H // 2, 1.3)),
            "tw": tw, "amb": {"stars": stars}}


# ---------------------------------------------------------------------------- Eco Fighters
def build_ef_coast(W, H, s, seed=312):
    """Eco Fighters seen from the side, as in the game: a bright blue sky and its clouds, the deep blue sea, tall
    ochre cliffs with a waterfall, green trees on top, the foam in front. / Un ciel bleu vif, la mer bleu profond,
    de hautes falaises ocre et leur cascade, comme dans le jeu."""
    rng = random.Random(seed)
    tw = 2 * W
    sea_y = 300 * s
    sky = vgrad(W, H, [(0.0, (40, 120, 220)), (sea_y / H, (170, 214, 250)), (sea_y / H + 0.001, (30, 80, 170)), (1.0, (16, 50, 130))])
    far = _Pic(tw, H, 2, tw)
    for _ in range(10):                                                  # clouds / nuages
        cx, cy = rng.uniform(0, tw), rng.uniform(30, 200) * s
        for i in range(4):
            r = rng.uniform(22, 44) * s
            far.poly(_blob(cx + i * 36 * s, cy + rng.uniform(-10, 10) * s, r * 1.4, r * 0.6, rng), (250, 252, 255, 230))
    for _ in range(int(tw / (40 * s))):                                  # the waves of the sea / les vagues
        x, y = rng.uniform(0, tw), rng.uniform(sea_y + 6 * s, H)
        far.line([(x, y), (x + 30 * s, y)], (90, 150, 220, 200), 2 * s)
    mid = _Pic(tw, H, 2, tw)
    for k in range(int(tw / (1100 * s))):                                # the cliffs / les falaises
        x = k * 1100 * s + 300 * s
        w = rng.uniform(300, 420) * s
        top = rng.uniform(60, 110) * s
        pts = [(x, H), (x + w * 0.05, top + 80 * s), (x + w * 0.2, top + 20 * s), (x + w * 0.45, top), (x + w * 0.7, top + 30 * s),
               (x + w * 0.9, top + 90 * s), (x + w, H)]
        mid.poly(pts, (196, 136, 76, 255), (110, 70, 40, 255), 3 * s)
        for j in range(7):                                               # rock strata / strates
            yy = top + 40 * s + j * 50 * s
            mid.line([(x + w * 0.1, yy), (x + w * 0.9, yy + rng.uniform(-10, 10) * s)], (160, 104, 56, 255), 3 * s)
        wx = x + w * 0.55                                                # the waterfall / la cascade
        mid.poly([(wx, top + 10 * s), (wx + 34 * s, top + 10 * s), (wx + 40 * s, H), (wx - 6 * s, H)], (170, 220, 250, 255))
        for j in range(5):
            mid.line([(wx + 6 * s + j * 6 * s, top + 14 * s), (wx + 4 * s + j * 7 * s, H)], (240, 250, 255, 255), 2 * s)
        for _ in range(6):
            _clump(mid, x + rng.uniform(0.15, 0.85) * w, top + rng.uniform(0, 30) * s, rng.uniform(20, 32) * s, rng,
                   ((40, 110, 50), (70, 150, 60), (140, 200, 90)), n=6)
    near = _Pic(tw, H, 2, tw)
    for _ in range(int(tw / (24 * s))):                                  # foam in front / l'écume devant
        x, y = rng.uniform(0, tw), rng.uniform(430, 456) * s
        near.poly(_blob(x, y, rng.uniform(14, 30) * s, rng.uniform(4, 8) * s, rng, 12, 0.3), (220, 240, 255, 220))
    return {"sky": sky, "layers": _fit([{"img": far.done(), "y": 0, "f": 0.3, "stage": "far"}, {"img": mid.done(), "y": 0, "f": 0.6, "stage": "mid"},
                                         {"img": near.done(), "y": 0, "f": 1.0, "stage": "near"}]), "tw": tw, "amb": {}}


# ---------------------------------------------------------------------------- Mercs
def build_mc_desert(W, H, s, seed=313):
    """Mercs seen from the sky, as in the game: a sandy track across the desert, tyre tracks, tufts of jungle grass
    and palms along the edges, old stone walls and sandbags. / Une piste de sable à travers le désert, des touffes
    d'herbe et des palmiers sur les bords, de vieux murs de pierre."""
    rng = random.Random(seed)
    tw = 2 * W
    p = _Pic(tw, H, 2, tw)
    p.poly([(0, 0), (tw, 0), (tw, H), (0, H)], (196, 176, 118, 255))
    for _ in range(int(tw * H / (900 * s * s))):                         # the sand / le sable
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        r = rng.uniform(6, 20) * s
        p.ellipse(x - r, y - r * 0.6, x + r, y + r * 0.6, _rgba(rng.choice(((206, 186, 128), (186, 166, 110), (214, 196, 140)))))
    n = 40
    for off in (-34, 34):                                                # tyre tracks / traces de pneus
        pts = [(tw * i / n, (277 + off + 14 * math.sin(i / n * math.tau * 2)) * s) for i in range(n + 1)]
        p.line(pts, (172, 152, 100, 255), 8 * s)
    for top in (True, False):                                            # the grass along the edges / l'herbe des bords
        for _ in range(int(tw / (22 * s))):
            x = rng.uniform(0, tw)
            y = rng.uniform(0, 110) * s if top else rng.uniform(420, 470) * s
            _clump(p, x, y, rng.uniform(18, 34) * s, rng, ((50, 90, 40), (76, 122, 52), (130, 170, 80)), n=6)
    for k in range(int(tw / (520 * s))):                                 # walls and sandbags / murs et sacs de sable
        x = k * 520 * s + rng.uniform(0, 200) * s
        y = rng.choice((112, 404)) * s
        for j in range(6):
            bx = x + j * 30 * s
            p.poly([(bx, y - 12 * s), (bx + 28 * s, y - 12 * s), (bx + 28 * s, y + 12 * s), (bx, y + 12 * s)], (150, 146, 136, 255),
                   (80, 76, 70, 255), 2 * s)
        sx = x + 260 * s
        for j in range(5):
            p.ellipse(sx + j * 22 * s, y - 10 * s, sx + j * 22 * s + 26 * s, y + 10 * s, (170, 150, 100, 255), (90, 76, 50, 255), 1.6 * s)
    return {"sky": Image.new("RGB", (W, H), (196, 176, 118)), "layers": [{"img": _done(p), "y": 0, "f": 1.0, "stage": "far"}], "tw": tw,
            "amb": {}}


THEMES = ("c44_sea", "c19_sky", "c41_coast", "vt_base", "un_canyon", "ca_city", "fw_ruins", "gw_lava", "pg_village", "mm_base", "dh_clouds",
          "ef_coast", "mc_desert")
hd_bg.BUILDERS.update({"c44_sea": build_c44_sea, "c19_sky": build_c19_sky, "c41_coast": build_c41_coast, "vt_base": build_vt_base,
                       "un_canyon": build_un_canyon, "ca_city": build_ca_city, "fw_ruins": build_fw_ruins, "gw_lava": build_gw_lava,
                       "pg_village": build_pg_village, "mm_base": build_mm_base, "dh_clouds": build_dh_clouds, "ef_coast": build_ef_coast,
                       "mc_desert": build_mc_desert})
