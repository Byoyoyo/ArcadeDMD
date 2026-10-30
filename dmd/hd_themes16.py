"""Backdrops of the small Capcom CPS games done one by one (1.30), drawn by the program after screenshots of the games:
the castle and its flames of Quiz Tonosama no Yabou 2, the park at dusk of Quiz Nanairo Dreams, the mahjong tables of
Jyangokushi and Janpai Puzzle Choukou, the starry well of Gulun.Pa!, the pastel sky of Pnickies, the pond of Frog
Feast, the savanna of Pokonyan! Balloon, the fairy-tale town of Magical Pumpkin and the sea of Ganbare! Marine Kun.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported (by hd_games16).

Décors des petits jeux Capcom CPS faits un par un (1.30), dessinés par le programme d'après des captures des jeux : le
château et ses flammes, le parc au crépuscule, les tables de mahjong, le puits étoilé, le ciel pastel, la mare, la
savane, la ville de conte de fées et la mer. Aucune image ne vient d'un jeu.
"""

import math
import random

from . import hd_bg
from .hd_bg import mix, vgrad
from .hd_themes3 import _clump, _Pic, _rgba
from .hd_themes11 import MJ_LOOKS, QZ_PANEL, build_mahjong

BW_COLS, BW_ROWS, BW_CELL, BW_TOP = 6, 12, 30, 76     # the blob wells / les puits de bulles (colonnes, lignes, case, haut)
BW_WELLS = {"bw_space": (330, 1590), "bw_heaven": (960,)}     # centre x of each well / centre de chaque puits


def _quiz_base(W, H, s, top, bot):
    sky = vgrad(W, H, [(0.0, top), (0.55, bot), (1.0, mix(bot, (0, 0, 0), 0.5))])
    return sky, _Pic(W, H, 2, 4 * W), QZ_PANEL * s


def _quiz_done(sky, p, W, H, py, foot):
    p.poly([(0, py), (W, py), (W, H), (0, H)], _rgba(foot))                  # the foot of the panel / le pied du panneau
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_qz_castle(W, H, s, seed=1601):
    """Quiz Tonosama no Yabou 2: a castle of the warring lords against a red sky, flames below, war banners on each
    side. / Un château des seigneurs de guerre sur un ciel rouge, des flammes en bas, des bannières de chaque côté."""
    rng = random.Random(seed)
    sky, p, py = _quiz_base(W, H, s, (60, 10, 20), (230, 110, 40))
    cx = W * 0.5                                                          # the keep / le donjon
    y = py - 40 * s
    for bw, th in ((300, 52), (240, 46), (180, 42), (120, 38)):
        p.poly([(cx - bw / 2 * s, y), (cx + bw / 2 * s, y), (cx + bw / 2 * s, y - th * 0.6 * s), (cx - bw / 2 * s, y - th * 0.6 * s)], (60, 30, 30, 255))
        p.poly([(cx - (bw / 2 + 30) * s, y - th * 0.55 * s), (cx - bw * 0.3 * s, y - th * s), (cx + bw * 0.3 * s, y - th * s),
                (cx + (bw / 2 + 30) * s, y - th * 0.55 * s)], (30, 14, 18, 255))
        y -= th * s
    p.poly([(cx - 190 * s, py), (cx - 160 * s, py - 40 * s), (cx + 160 * s, py - 40 * s), (cx + 190 * s, py)], (50, 26, 26, 255))
    for side in (-1, 1):                                                  # the banners / les bannières
        for k in range(4):
            x = cx + side * (330 + k * 150) * s
            p.line([(x, py), (x, 40 * s)], (40, 24, 20, 255), 5 * s)
            col = ((230, 220, 200), (200, 40, 40), (40, 40, 40), (230, 200, 60))[k]
            p.poly([(x + 4 * s, 50 * s), (x + 60 * s, 50 * s), (x + 60 * s, 200 * s), (x + 4 * s, 200 * s)], _rgba(col), (30, 20, 20, 255), 2 * s)
            p.disc(x + 32 * s, 110 * s, 16 * s, _rgba(mix(col, (0, 0, 0), 0.5)))
    for _ in range(60):                                                   # the flames / les flammes
        x = rng.uniform(0, W)
        h = rng.uniform(40, 120) * s
        w = rng.uniform(20, 50) * s
        p.poly([(x - w, py), (x - w * 0.3, py - h * 0.6), (x, py - h), (x + w * 0.4, py - h * 0.5), (x + w, py)],
               _rgba(rng.choice(((250, 120, 30), (250, 180, 40), (220, 60, 20))), 210))
    return _quiz_done(sky, p, W, H, py, (60, 16, 16))


def build_qz_park(W, H, s, seed=1602):
    """Quiz Nanairo Dreams: a town park at dusk, round trees, street lamps and a fountain, a faint rainbow.
    / Un parc de la ville au crépuscule, des arbres ronds, des réverbères, une fontaine et un arc-en-ciel pâle."""
    rng = random.Random(seed)
    sky, p, py = _quiz_base(W, H, s, (110, 120, 210), (250, 180, 200))
    for k, col in enumerate(((250, 150, 150), (250, 210, 150), (250, 250, 170), (170, 230, 170), (160, 200, 250), (200, 170, 240))):
        r = (620 - k * 18) * s                                            # the rainbow / l'arc-en-ciel
        pts = [(W / 2 + math.cos(math.pi + i * math.pi / 50) * r, py + math.sin(math.pi + i * math.pi / 50) * r * 0.55) for i in range(51)]
        p.line(pts, _rgba(col, 90), 14 * s)
    for k in range(9):                                                    # the trees / les arbres
        x = k * W / 8 + rng.uniform(-40, 40) * s
        p.poly([(x - 8 * s, py), (x - 5 * s, py - 120 * s), (x + 5 * s, py - 120 * s), (x + 8 * s, py)], (90, 60, 50, 255))
        _clump(p, x, py - 150 * s, 70 * s, rng, ((70, 150, 90), (100, 180, 110), (60, 120, 80)), n=7)
    for x in (W * 0.3, W * 0.7):                                          # street lamps / réverbères
        p.line([(x, py), (x, py - 200 * s)], (50, 50, 70, 255), 6 * s)
        p.disc(x, py - 206 * s, 16 * s, (255, 240, 180, 255), (50, 50, 70, 255), 3 * s)
    fx = W * 0.5                                                          # the fountain / la fontaine
    p.ellipse(fx - 150 * s, py - 30 * s, fx + 150 * s, py + 10 * s, (170, 170, 190, 255), (90, 90, 110, 255), 3 * s)
    p.ellipse(fx - 120 * s, py - 24 * s, fx + 120 * s, py + 2 * s, (120, 180, 230, 255))
    p.poly([(fx - 10 * s, py - 20 * s), (fx - 6 * s, py - 120 * s), (fx + 6 * s, py - 120 * s), (fx + 10 * s, py - 20 * s)], (170, 170, 190, 255))
    for k in range(7):
        a = math.pi * (0.15 + 0.7 * k / 6)
        p.line([(fx, py - 120 * s), (fx - math.cos(a) * 100 * s, py - 120 * s - math.sin(a) * 40 * s),
                (fx - math.cos(a) * 140 * s, py - 30 * s)], (200, 230, 255, 200), 3 * s)
    return _quiz_done(sky, p, W, H, py, (40, 50, 110))


def build_bw_space(W, H, s, seed=1603):
    """Gulun.Pa!: a starry purple sky with its planets, golden pillars around the two wells.
    / Un ciel violet étoilé et ses planètes, des colonnes dorées autour des deux puits."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (30, 20, 70)), (0.6, (60, 30, 90)), (1.0, (20, 10, 40))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(220):
        p.disc(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.8, 2.4) * s, _rgba(rng.choice(((255, 255, 255), (200, 200, 255), (255, 230, 180)))))
    for (x, y, r, col) in ((W * 0.5, H * 0.3, 70, (230, 120, 80)), (W * 0.42, H * 0.75, 30, (120, 200, 230)), (W * 0.6, H * 0.62, 44, (200, 160, 240))):
        p.disc(x, y, r * s, _rgba(col), _rgba(mix(col, (0, 0, 0), 0.4)), 3 * s)
        p.ellipse(x - r * 1.7 * s, y - r * 0.25 * s, x + r * 1.7 * s, y + r * 0.25 * s, (0, 0, 0, 0), _rgba(mix(col, (255, 255, 255), 0.4)), 3 * s)
    c = BW_CELL * s
    for wx in BW_WELLS["bw_space"]:                                       # the wells and their pillars / les puits et leurs colonnes
        x0, x1 = wx * s - BW_COLS * c / 2, wx * s + BW_COLS * c / 2
        y0, y1 = BW_TOP * s, BW_TOP * s + BW_ROWS * c
        p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (20, 14, 40, 235))
        for px in (x0 - 22 * s, x1 + 4 * s):
            p.poly([(px, y0 - 30 * s), (px + 18 * s, y0 - 30 * s), (px + 18 * s, y1), (px, y1)], (220, 170, 60, 255), (120, 80, 20, 255), 2 * s)
            for k in range(8):
                yy = y0 + k * (y1 - y0) / 8
                p.line([(px, yy), (px + 18 * s, yy)], (150, 100, 30, 255), 2 * s)
        p.poly([(x0 - 22 * s, y0 - 40 * s), (x1 + 22 * s, y0 - 40 * s), (x1 + 22 * s, y0 - 20 * s), (x0 - 22 * s, y0 - 20 * s)],
               (220, 170, 60, 255), (120, 80, 20, 255), 2 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_bw_heaven(W, H, s, seed=1604):
    """Pnickies: a pastel sky between heaven and the underworld, an angel of our own on the left (wings and halo), a
    little imp on the right (horns and tail), the well in the middle. / Un ciel pastel, un ange à nous à gauche, un
    petit diablotin à droite, le puits au milieu."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (170, 140, 230)), (0.5, (250, 200, 240)), (1.0, (120, 80, 170))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(10):
        x, y = rng.uniform(0, W), rng.uniform(40, 420) * s
        for k in range(5):
            p.disc(x + k * 30 * s, y + rng.uniform(-10, 10) * s, rng.uniform(20, 34) * s, (255, 250, 255, 200))
    ax, ay = W * 0.22, H * 0.52                                           # the angel / l'ange
    for side in (-1, 1):
        p.poly([(ax, ay - 20 * s), (ax + side * 160 * s, ay - 120 * s), (ax + side * 190 * s, ay - 40 * s), (ax + side * 120 * s, ay + 40 * s)],
               (255, 255, 255, 255), (180, 160, 220, 255), 3 * s)
    p.poly([(ax - 50 * s, ay + 160 * s), (ax - 30 * s, ay - 10 * s), (ax + 30 * s, ay - 10 * s), (ax + 50 * s, ay + 160 * s)],
           (250, 230, 250, 255), (180, 160, 220, 255), 3 * s)
    p.disc(ax, ay - 50 * s, 40 * s, (255, 220, 190, 255), (180, 140, 140, 255), 3 * s)
    p.ellipse(ax - 50 * s, ay - 118 * s, ax + 50 * s, ay - 98 * s, (0, 0, 0, 0), (255, 220, 80, 255), 6 * s)
    p.chord(ax - 44 * s, ay - 96 * s, ax + 44 * s, ay - 14 * s, 180, 360, (250, 210, 110, 255))
    ix, iy = W * 0.78, H * 0.55                                           # the imp / le diablotin
    for side in (-1, 1):
        p.poly([(ix, iy - 10 * s), (ix + side * 140 * s, iy - 100 * s), (ix + side * 120 * s, iy - 20 * s), (ix + side * 150 * s, iy + 30 * s)],
               (120, 50, 140, 255), (60, 20, 70, 255), 3 * s)
    p.poly([(ix - 50 * s, iy + 160 * s), (ix - 30 * s, iy), (ix + 30 * s, iy), (ix + 50 * s, iy + 160 * s)], (90, 40, 110, 255), (50, 20, 60, 255), 3 * s)
    p.disc(ix, iy - 40 * s, 40 * s, (210, 150, 220, 255), (90, 40, 110, 255), 3 * s)
    for side in (-1, 1):
        p.poly([(ix + side * 18 * s, iy - 74 * s), (ix + side * 34 * s, iy - 112 * s), (ix + side * 34 * s, iy - 66 * s)], (250, 240, 220, 255))
    p.line([(ix + 40 * s, iy + 140 * s), (ix + 110 * s, iy + 120 * s), (ix + 120 * s, iy + 80 * s)], (90, 40, 110, 255), 6 * s)
    p.poly([(ix + 112 * s, iy + 84 * s), (ix + 130 * s, iy + 60 * s), (ix + 134 * s, iy + 88 * s)], (90, 40, 110, 255))
    c = BW_CELL * s
    wx = BW_WELLS["bw_heaven"][0] * s                                     # the well and its pink frame / le puits et son cadre rose
    x0, x1 = wx - BW_COLS * c / 2, wx + BW_COLS * c / 2
    y0, y1 = BW_TOP * s, BW_TOP * s + BW_ROWS * c
    p.poly([(x0 - 16 * s, y0 - 16 * s), (x1 + 16 * s, y0 - 16 * s), (x1 + 16 * s, y1 + 8 * s), (x0 - 16 * s, y1 + 8 * s)],
           (240, 120, 190, 255), (150, 60, 120, 255), 3 * s)
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (40, 20, 70, 240))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


FF_PADS = ((0.36, 0.73), (0.64, 0.73))      # the two lily pads (x, y in screen parts) / les deux nénuphars
FF_BANKS = ((0.14, 0.86), (0.86, 0.86))     # where each frog waits on the bank / où chaque grenouille attend sur la rive


def build_ff_pond(W, H, s, seed=1605):
    """Frog Feast: a blue pond between two tall pines, its two lily pads, the grass of the banks under a blue sky.
    / Une mare bleue entre deux grands sapins, ses deux nénuphars, l'herbe des rives sous un ciel bleu."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (80, 140, 240)), (0.55, (170, 210, 250)), (0.56, (60, 160, 60)), (1.0, (40, 120, 40))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(7):
        x, y = rng.uniform(0, W), rng.uniform(20, 120) * s
        for k in range(4):
            p.disc(x + k * 28 * s, y + rng.uniform(-6, 6) * s, rng.uniform(18, 28) * s, (255, 255, 255, 240))
    for x in (W * 0.12, W * 0.88):                                        # the pines / les sapins
        p.poly([(x - 12 * s, H * 0.6), (x - 10 * s, H * 0.3), (x + 10 * s, H * 0.3), (x + 12 * s, H * 0.6)], (110, 70, 40, 255))
        for k in range(5):
            y = H * 0.08 + k * 34 * s
            w = (40 + k * 26) * s
            p.poly([(x, y), (x + w, y + 70 * s), (x - w, y + 70 * s)], _rgba(((40, 120, 50), (50, 140, 60))[k % 2]), (20, 70, 30, 255), 2 * s)
    p.ellipse(W * 0.22, H * 0.6, W * 0.78, H * 0.98, (40, 90, 200, 255), (30, 60, 140, 255), 4 * s)      # the pond / la mare
    for _ in range(26):
        x, y = rng.uniform(W * 0.3, W * 0.7), rng.uniform(H * 0.66, H * 0.92)
        p.line([(x, y), (x + 24 * s, y - 3 * s), (x + 48 * s, y)], (120, 170, 250, 255), 2 * s)
    for (px, py) in FF_PADS:
        p.ellipse(W * px - 90 * s, H * py - 26 * s, W * px + 90 * s, H * py + 26 * s, (90, 190, 80, 255), (40, 110, 40, 255), 3 * s)
        p.poly([(W * px, H * py), (W * px + 80 * s, H * py - 10 * s), (W * px + 80 * s, H * py + 10 * s)], (40, 90, 200, 255))
    for (bx, by) in FF_BANKS:                                             # the wooden posts of the scores / les poteaux des scores
        p.poly([(W * bx - 26 * s, H), (W * bx - 22 * s, H * by - 40 * s), (W * bx + 22 * s, H * by - 40 * s), (W * bx + 26 * s, H)], (170, 110, 50, 255),
               (90, 50, 20, 255), 3 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def _band(W, h, s, draw, seed):
    p = _Pic(W, h, 2, W)
    draw(p, random.Random(seed))
    return p.done()


def build_pk_savanna(W, H, s, seed=1606):
    """Pokonyan! Balloon: the savanna seen from above the trees, far blue hills, acacias, a round hut, the yellow grass
    and its paths; it scrolls under the balloon. / La savane, les collines bleues, les acacias, une case ronde,
    l'herbe jaune et ses chemins ; elle défile sous le ballon."""
    sky = vgrad(W, H, [(0.0, (120, 190, 250)), (0.5, (220, 240, 250)), (1.0, (230, 220, 160))])
    hz = int(H * 0.42)

    def hills(p, rng):
        pts = [(x, 70 * s - abs(math.sin(x / W * math.pi * 3)) * 50 * s - math.sin(x / W * math.tau * 5) * 8 * s) for x in range(0, W + 1, 8)]
        p.poly([(0, 120 * s)] + pts + [(W, 120 * s)], (130, 170, 210, 255))

    def ground(p, rng):
        p.poly([(0, 0), (W, 0), (W, H), (0, H)], (210, 190, 90, 255))
        for _ in range(26):                                               # green patches / taches vertes
            x, y = rng.uniform(0, W), rng.uniform(10, H - hz) * 1.0
            _clump(p, x, y, rng.uniform(40, 90) * s, rng, ((120, 170, 60), (150, 190, 70)), n=5)
        for k in range(3):                                                # paths / chemins
            y = (40 + k * 80) * s
            p.line([(x, y + math.sin(x / W * math.tau * 2 + k) * 20 * s) for x in range(0, W + 1, 20)], (230, 210, 150, 255), 10 * s)
        for _ in range(9):                                                # acacias
            x, y = rng.uniform(0, W), rng.uniform(30, H - hz - 30) * 1.0
            p.line([(x, y + 40 * s), (x, y)], (100, 70, 40, 255), 6 * s)
            p.ellipse(x - 50 * s, y - 16 * s, x + 50 * s, y + 8 * s, (70, 130, 50, 255), (40, 90, 30, 255), 2 * s)
        x, y = rng.uniform(0, W), (H - hz) * 0.5                          # a round hut / une case ronde
        p.ellipse(x - 34 * s, y - 10 * s, x + 34 * s, y + 30 * s, (190, 150, 90, 255), (110, 80, 40, 255), 2 * s)
        p.poly([(x - 44 * s, y), (x, y - 44 * s), (x + 44 * s, y)], (150, 110, 50, 255), (90, 60, 30, 255), 2 * s)
    layers = [{"img": _band(W, int(120 * s), s, hills, seed), "y": hz - int(100 * s), "f": 0.1, "stage": "far"},
              {"img": _band(W, H - hz, s, ground, seed + 1), "y": hz, "f": 0.6, "stage": "near"}]
    return {"sky": sky, "layers": layers, "tw": W, "amb": {}}


def build_mp_town(W, H, s, seed=1607):
    """Magical Pumpkin: a fairy-tale town of round pastel houses, a pink castle far away, a candy road and a blue
    river below; it scrolls behind the pumpkin carriage. / Une ville de conte de fées aux maisons rondes pastel, un
    château rose au loin, une route en bonbon et une rivière bleue ; elle défile derrière le carrosse citrouille."""
    sky = vgrad(W, H, [(0.0, (130, 200, 250)), (0.6, (230, 240, 255)), (1.0, (200, 220, 250))])

    def castle(p, rng):
        for k in range(3):
            x = W * (0.2 + k * 0.33)
            p.poly([(x - 90 * s, 160 * s), (x - 90 * s, 70 * s), (x + 90 * s, 70 * s), (x + 90 * s, 160 * s)], (250, 200, 220, 255))
            for tx in (-80, -10, 60):
                p.poly([(x + tx * s, 80 * s), (x + tx * s, 20 * s), (x + (tx + 24) * s, 20 * s), (x + (tx + 24) * s, 80 * s)], (250, 180, 210, 255))
                p.poly([(x + (tx - 6) * s, 22 * s), (x + (tx + 12) * s, -20 * s), (x + (tx + 30) * s, 22 * s)], (120, 120, 230, 255))

    def houses(p, rng):
        x = 0
        while x < W:
            w = rng.uniform(80, 140) * s
            h = rng.uniform(70, 130) * s
            col = rng.choice(((250, 220, 120), (250, 170, 190), (170, 220, 250), (190, 240, 170), (240, 200, 250)))
            p.poly([(x, 200 * s), (x, 200 * s - h), (x + w, 200 * s - h), (x + w, 200 * s)], _rgba(col), _rgba(mix(col, (0, 0, 0), 0.4)), 2 * s)
            p.chord(x - 10 * s, 200 * s - h - w * 0.5, x + w + 10 * s, 200 * s - h + w * 0.4, 180, 360,
                    _rgba(rng.choice(((240, 90, 90), (120, 120, 230), (250, 150, 60)))))
            p.disc(x + w / 2, 200 * s - h * 0.45, 12 * s, (255, 250, 210, 255), _rgba(mix(col, (0, 0, 0), 0.4)), 2 * s)
            x += w + rng.uniform(10, 40) * s

    def road(p, rng):
        p.poly([(0, 0), (W, 0), (W, 40 * s), (0, 40 * s)], (250, 230, 240, 255))
        for k in range(int(W / (60 * s)) + 1):
            p.poly([(k * 60 * s, 0), (k * 60 * s + 30 * s, 0), (k * 60 * s + 30 * s, 40 * s), (k * 60 * s, 40 * s)], (250, 150, 190, 255))
        p.poly([(0, 40 * s), (W, 40 * s), (W, 160 * s), (0, 160 * s)], (90, 160, 240, 255))
        for _ in range(30):
            x, y = rng.uniform(0, W), rng.uniform(60, 150) * s
            p.line([(x, y), (x + 30 * s, y - 3 * s), (x + 60 * s, y)], (220, 240, 255, 255), 3 * s)
    layers = [{"img": _band(W, int(170 * s), s, castle, seed), "y": int(40 * s), "f": 0.08, "stage": "far"},
              {"img": _band(W, int(210 * s), s, houses, seed + 1), "y": int(150 * s), "f": 0.3, "stage": "mid"},
              {"img": _band(W, int(160 * s), s, road, seed + 2), "y": H - int(110 * s), "f": 1.0, "stage": "near"}]
    return {"sky": sky, "layers": layers, "tw": W, "amb": {}}


def build_gm_sea(W, H, s, seed=1608):
    """Ganbare! Marine Kun: the open sea under a blue sky, white clouds and rocky stacks with their green tops.
    / La pleine mer sous un ciel bleu, des nuages blancs et des pitons rocheux coiffés de vert."""
    rng = random.Random(seed)
    hz = int(H * 0.5)
    sky = vgrad(W, H, [(0.0, (60, 120, 230)), (0.49, (190, 225, 255)), (0.5, (40, 120, 200)), (1.0, (10, 50, 120))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(8):
        x, y = rng.uniform(0, W), rng.uniform(30, hz - 80 * s)
        for k in range(5):
            p.disc(x + k * 30 * s, y + rng.uniform(-8, 8) * s, rng.uniform(20, 32) * s, (255, 255, 255, 235))
    for x in (W * 0.1, W * 0.3, W * 0.72, W * 0.92):                      # rocky stacks / pitons rocheux
        w = rng.uniform(50, 90) * s
        h = rng.uniform(120, 200) * s
        p.poly([(x - w, hz + 20 * s), (x - w * 0.7, hz - h), (x + w * 0.6, hz - h * 0.9), (x + w, hz + 20 * s)], (110, 100, 120, 255), (60, 50, 70, 255), 3 * s)
        _clump(p, x, hz - h, w * 0.8, rng, ((60, 140, 70), (80, 170, 80)), n=5)
    for _ in range(60):                                                   # waves / vagues
        x, y = rng.uniform(0, W), rng.uniform(hz + 10 * s, H)
        p.line([(x, y), (x + 30 * s, y - 4 * s), (x + 60 * s, y)], (180, 220, 255, 220), 2 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {"horizon": hz}}


MJ_LOOKS.update({"mj_kingdom": ((24, 96, 60), (34, 112, 70), (170, 40, 30)),       # Jyangokushi: red lacquer frame / cadre laqué rouge
                 "mj_redsilk": ((150, 24, 24), (170, 34, 30), (210, 170, 70))})   # Choukou: red silk, gold frame / soie rouge, cadre doré
LOOKS = {"qz_castle": build_qz_castle, "qz_park": build_qz_park, "bw_space": build_bw_space, "bw_heaven": build_bw_heaven,
         "ff_pond": build_ff_pond, "pk_savanna": build_pk_savanna, "mp_town": build_mp_town, "gm_sea": build_gm_sea}
hd_bg.BUILDERS.update(LOOKS)
hd_bg.BUILDERS.update({name: (lambda W, H, s, n=name: build_mahjong(W, H, s, n)) for name in ("mj_kingdom", "mj_redsilk")})
THEMES = tuple(LOOKS) + ("mj_kingdom", "mj_redsilk")     # names of the backdrops of this batch / noms des décors de ce lot
