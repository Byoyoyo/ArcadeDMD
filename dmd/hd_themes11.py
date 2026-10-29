"""HD backdrops of the eleventh batch of Neo Geo games done one by one (1.27), each drawn after screenshots of its game.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported.

Décors HD du onzième lot (1.27), chacun dessiné d'après des captures de son jeu. Tout est dessiné par le programme,
aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image

from . import hd_bg
from .hd_bg import mix, vgrad
from .hd_themes3 import _clump, _Pic, _rgba

ND_ROWS = ((432, ((0, 1920),)), (338, ((60, 600), (860, 1100), (1340, 1880))), (244, ((240, 840), (1100, 1700))),
           (152, ((20, 420), (700, 1240), (1500, 1900))))
QZ_PANEL = 270                     # the quizzes: top of the question panel / le haut du panneau des questions
SH_CELL, SH_X0, SH_Y0 = 46, 753, 24   # Shogi no Tatsujin: the board / le plateau


def build_nd_grave(W, H, s, seed=601):
    """Nightmare in the Dark: the graveyard at night, as in the game: the pink sky, the huge full moon, the dead trees,
    the tombstones and the crosses, the platforms of mossy stones. / Le cimetière la nuit : le ciel rose, l'énorme
    pleine lune, les arbres morts, les tombes et les croix, les plateformes de pierres moussues."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (110, 30, 90)), (0.5, (190, 60, 120)), (1.0, (80, 30, 70))])
    p = _Pic(W, H, 2, 4 * W)
    p.disc(W * 0.5, 170 * s, 170 * s, (250, 220, 150, 255))              # la pleine lune
    for _ in range(9):
        p.disc(W * 0.5 + rng.uniform(-110, 110) * s, 170 * s + rng.uniform(-110, 110) * s, rng.uniform(12, 30) * s, (230, 196, 130, 255))
    for k in range(7):                                                    # les arbres morts
        x = rng.uniform(0, W)
        base = H
        p.poly([(x - 14 * s, base), (x + 14 * s, base), (x + 6 * s, base - 260 * s), (x - 6 * s, base - 260 * s)], (60, 20, 60, 255))
        for _b in range(6):
            y = base - rng.uniform(120, 250) * s
            d = rng.choice((-1, 1))
            p.line([(x, y), (x + d * rng.uniform(40, 90) * s, y - rng.uniform(20, 60) * s), (x + d * rng.uniform(80, 130) * s, y - rng.uniform(50, 90) * s)],
                   (60, 20, 60, 255), 5 * s)
    for _ in range(14):                                                   # tombes et croix
        x, y = rng.uniform(0, W), rng.uniform(380, 440) * s
        if rng.random() < 0.5:
            p.poly([(x - 22 * s, y), (x + 22 * s, y), (x + 22 * s, y - 40 * s), (x, y - 56 * s), (x - 22 * s, y - 40 * s)], (120, 110, 130, 255), (60, 50, 70, 255), 2 * s)
        else:
            p.poly([(x - 5 * s, y), (x + 5 * s, y), (x + 5 * s, y - 60 * s), (x - 5 * s, y - 60 * s)], (120, 110, 130, 255))
            p.poly([(x - 20 * s, y - 46 * s), (x + 20 * s, y - 46 * s), (x + 20 * s, y - 38 * s), (x - 20 * s, y - 38 * s)], (120, 110, 130, 255))
    for y, segs in ND_ROWS:                                               # les plateformes de pierres moussues
        for x0, x1 in segs:
            x = x0 * s
            while x < x1 * s - 4 * s:
                w = rng.uniform(24, 34) * s
                p.poly([(x, y * s), (x + w, y * s), (x + w, y * s + 22 * s), (x, y * s + 22 * s)], _rgba(rng.choice(((150, 130, 100), (130, 112, 90),
                                                                                                                       (160, 142, 110)))), (70, 56, 50, 255), 1.5 * s)
                x += w
            p.line([(x0 * s, y * s), (x1 * s, y * s)], (70, 160, 60, 255), 6 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_ss_corridor(W, H, s, seed=611):
    """The Super Spy: the corridor of the building, as in the game: the grey-green walls, the pipes under the ceiling
    and their lamps, the doors with their red IN sign, the tiled floor. / Le couloir de l'immeuble : murs gris-vert,
    tuyaux et lampes au plafond, portes et leur panneau IN rouge, sol carrelé."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (60, 70, 70)), (1.0, (90, 100, 96))])
    p = _Pic(W, H, 2, 4 * W)
    cx, vy = W / 2, 200 * s                                               # le point de fuite
    p.poly([(0, 0), (W, 0), (cx + 260 * s, vy - 110 * s), (cx - 260 * s, vy - 110 * s)], (70, 76, 74, 255))      # le plafond
    p.poly([(0, H), (W, H), (cx + 260 * s, vy + 110 * s), (cx - 260 * s, vy + 110 * s)], (120, 126, 120, 255))   # le sol
    for k in range(1, 12):                                                # les carreaux du sol
        t = k / 12
        y = vy + 110 * s + (H - vy - 110 * s) * t * t
        half = 260 * s + (W / 2 - 260 * s) * t * t
        p.line([(cx - half, y), (cx + half, y)], (100, 106, 100, 255), 2 * s)
    for k in range(-6, 7):
        p.line([(cx + k * 40 * s, vy + 110 * s), (cx + k * 300 * s, H)], (100, 106, 100, 255), 2 * s)
    p.poly([(cx - 260 * s, vy - 110 * s), (cx + 260 * s, vy - 110 * s), (cx + 260 * s, vy + 110 * s), (cx - 260 * s, vy + 110 * s)], (50, 56, 56, 255))
    for side in (-1, 1):                                                  # les murs et leurs portes
        p.poly([(cx + side * 260 * s, vy - 110 * s), (cx + side * W / 2, 0), (cx + side * W / 2, H), (cx + side * 260 * s, vy + 110 * s)], (96, 110, 100, 255))
        for k, t in enumerate((0.25, 0.6)):
            x0 = cx + side * (260 * s + (W / 2 - 260 * s) * t)
            x1 = cx + side * (260 * s + (W / 2 - 260 * s) * (t + 0.18))
            h0, h1 = 90 * s + 200 * s * t, 90 * s + 200 * s * (t + 0.18)
            p.poly([(x0, vy + 110 * s * (0.5 + t) - h0 * 0.2), (x1, vy + 110 * s * (0.5 + t + 0.18) - h1 * 0.2), (x1, vy + 110 * s + (H - vy) * (t + 0.18) * 0.6),
                    (x0, vy + 110 * s + (H - vy) * t * 0.6)], (40, 40, 44, 255), (150, 150, 150, 255), 2 * s)
            sx = (x0 + x1) / 2
            p.poly([(sx - 16 * s, vy - 60 * s + t * 40 * s), (sx + 16 * s, vy - 60 * s + t * 40 * s), (sx + 16 * s, vy - 30 * s + t * 40 * s),
                    (sx - 16 * s, vy - 30 * s + t * 40 * s)], (200, 40, 30, 255))
    for k in range(3):                                                    # les tuyaux et les lampes
        y = (14 + k * 16) * s
        p.line([(0, y), (cx - 200 * s, vy - 100 * s + k * 10 * s), (cx + 200 * s, vy - 100 * s + k * 10 * s), (W, y)], (130, 140, 140, 255), 7 * s)
    for t in (0.15, 0.45, 0.8):
        x = cx + (W / 2) * t * 0.9
        p.poly([(x - 40 * s, 30 * s), (x + 40 * s, 30 * s), (x + 30 * s, 44 * s), (x - 30 * s, 44 * s)], (240, 240, 220, 255))
        x = cx - (W / 2) * t * 0.9
        p.poly([(x - 40 * s, 30 * s), (x + 40 * s, 30 * s), (x + 30 * s, 44 * s), (x - 30 * s, 44 * s)], (240, 240, 220, 255))
    for _ in range(20):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        p.disc(x, y, 2 * s, (80, 86, 84, 255))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


QZ_LOOKS = {     # sky top, sky bottom, kind / ciel, genre
    "qz_arena": ((20, 30, 70), (90, 60, 120), "arena"),
    "qz_fence": ((60, 80, 130), (200, 150, 120), "fence"),
    "qz_office": ((110, 80, 60), (160, 120, 90), "office"),
    "qz_studio": ((90, 40, 160), (250, 140, 200), "studio"),
}


def build_quiz(W, H, s, name, seed=621):
    """The quiz sets, as in the games: a stage between the city lights (Quiz King of Fighters), a wire fence in front
    of the city at dusk (Quiz Daisousa Sen), a detective's office (Quiz Meitantei Neo & Geo), a television studio and
    its rainbow (the Deluxe Quiz); the question panel below. / Les décors des quiz : une scène dans la ville, un
    grillage devant la ville au crépuscule, un bureau de détective, un studio de télévision et son arc-en-ciel."""
    rng = random.Random(seed + len(name))
    top, bot, kind = QZ_LOOKS[name]
    sky = vgrad(W, H, [(0.0, top), (0.55, bot), (1.0, mix(bot, (0, 0, 0), 0.5))])
    p = _Pic(W, H, 2, 4 * W)
    py = QZ_PANEL * s
    if kind in ("arena", "fence"):                                        # la ville
        x = -20 * s
        while x < W:
            w = rng.uniform(60, 140) * s
            h = rng.uniform(80, 220) * s
            col = mix(top, (10, 10, 20), 0.4)
            p.poly([(x, py), (x, py - h), (x + w, py - h), (x + w, py)], _rgba(col))
            for wy in range(int(py - h + 10 * s), int(py - 10 * s), int(18 * s)):
                for wx in range(int(x + 6 * s), int(x + w - 10 * s), int(14 * s)):
                    if rng.random() < 0.4:
                        p.poly([(wx, wy), (wx + 7 * s, wy), (wx + 7 * s, wy + 9 * s), (wx, wy + 9 * s)], (250, 220, 120, 255))
            x += w + rng.uniform(4, 20) * s
    if kind == "arena":                                                   # néons et public
        for k in range(8):
            x = rng.uniform(0, W)
            p.poly([(x, 30 * s), (x + 120 * s, 30 * s), (x + 120 * s, 60 * s), (x, 60 * s)], _rgba(rng.choice(((250, 60, 160), (60, 220, 250), (250, 220, 60)))))
        for _ in range(300):
            p.disc(rng.uniform(0, W), rng.uniform(py - 40 * s, py), rng.uniform(5, 8) * s, _rgba(rng.choice(((40, 40, 60), (60, 50, 70), (80, 60, 60)))))
    if kind == "fence":                                                   # le grillage
        for k in range(-20, int(W / (30 * s)) + 20):
            x = k * 30 * s
            p.line([(x, 0), (x + py, py)], (150, 160, 170, 255), 2 * s)
            p.line([(x, 0), (x - py, py)], (150, 160, 170, 255), 2 * s)
        p.line([(0, 6 * s), (W, 6 * s)], (120, 130, 140, 255), 6 * s)
    if kind == "office":                                                  # le bureau : boiseries, fenêtre, étagères
        for k in range(int(W / (60 * s)) + 1):
            p.line([(k * 60 * s, 0), (k * 60 * s, py)], (90, 64, 46, 255), 3 * s)
        wx = W * 0.62
        p.poly([(wx, 30 * s), (wx + 360 * s, 30 * s), (wx + 360 * s, 220 * s), (wx, 220 * s)], (180, 210, 230, 255), (60, 40, 30, 255), 6 * s)
        for k in range(10):
            p.line([(wx, (40 + k * 18) * s), (wx + 360 * s, (40 + k * 18) * s)], (230, 230, 220, 255), 6 * s)
        for row in range(3):
            y = (40 + row * 70) * s
            p.line([(W * 0.05, y + 60 * s), (W * 0.32, y + 60 * s)], (70, 46, 30, 255), 6 * s)
            x = W * 0.05
            while x < W * 0.32:
                w = rng.uniform(10, 22) * s
                p.poly([(x, y + 10 * s), (x + w, y + 10 * s), (x + w, y + 58 * s), (x, y + 58 * s)], _rgba(rng.choice(((150, 40, 40), (40, 80, 140), (60, 120, 60),
                                                                                                                        (200, 160, 60)))))
                x += w + 2 * s
    if kind == "studio":                                                  # l'arc-en-ciel et les projecteurs
        for k, col in enumerate(((240, 60, 60), (250, 150, 40), (250, 230, 60), (80, 200, 90), (60, 140, 240), (150, 80, 220))):
            r = (360 - k * 24) * s
            pts = [(W / 2 + math.cos(math.pi + i * math.pi / 40) * r, py + math.sin(math.pi + i * math.pi / 40) * r * 0.7) for i in range(41)]
            p.line(pts, _rgba(col), 22 * s)
        for k in range(12):
            x = k * W / 11
            p.disc(x, 40 * s, 20 * s, (250, 250, 200, 255), (120, 80, 160, 255), 4 * s)
        for k in range(30):
            x, y = rng.uniform(0, W), rng.uniform(80, 250) * s
            p.disc(x, y, rng.uniform(3, 6) * s, _rgba(rng.choice(((250, 250, 250), (250, 220, 80), (120, 220, 255)))))
    p.poly([(0, py), (W, py), (W, H), (0, H)], (20, 30, 90, 255))       # le pied du panneau
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


MJ_LOOKS = {     # felt, felt light, frame / tapis, tapis clair, cadre
    "mj_green": ((30, 120, 50), (40, 140, 60), None),
    "mj_purple": ((80, 50, 100), (96, 64, 116), None),
    "mj_olive": ((90, 100, 50), (106, 118, 60), None),
    "mj_wood": ((30, 100, 50), (40, 120, 60), (200, 160, 100)),
    "mj_blue": ((30, 40, 200), (44, 56, 220), None),
}


def build_mahjong(W, H, s, name, seed=631):
    """The mahjong tables, as in the games: the felt in its colour (green, purple, olive, blue), with its soft weave,
    a wooden frame for Final Romance 2. / Les tables de mahjong : le tapis de sa couleur et sa trame, un cadre de bois."""
    rng = random.Random(seed + len(name))
    felt, light, frame = MJ_LOOKS[name]
    sky = Image.new("RGB", (W, H), felt)
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(int(W * H / (900 * s * s))):                           # la trame du tapis
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        p.disc(x, y, rng.uniform(1, 2.5) * s, _rgba(light if rng.random() < 0.5 else mix(felt, (0, 0, 0), 0.12)))
    if frame:                                                             # le cadre de bois
        for k, col in enumerate((frame, mix(frame, (0, 0, 0), 0.3))):
            m = (24 - k * 8) * s
            p.poly([(0, 0), (W, 0), (W, m), (0, m)], _rgba(col))
            p.poly([(0, H - m), (W, H - m), (W, H), (0, H)], _rgba(col))
            p.poly([(0, 0), (m * 2, 0), (m * 2, H), (0, H)], _rgba(col))
            p.poly([(W - m * 2, 0), (W, 0), (W, H), (W - m * 2, H)], _rgba(col))
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_sh_coast(W, H, s, seed=641):
    """Shogi no Tatsujin: the rocky coast by the sea, as in the game, under a blue sky; the wooden board in the middle
    and its two piece stands. / La côte rocheuse au bord de la mer sous un ciel bleu ; le plateau de bois au milieu."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (90, 160, 230)), (0.45, (200, 230, 250)), (0.46, (40, 110, 170)), (1.0, (20, 70, 120))])
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(8):
        x, y = rng.uniform(0, W), rng.uniform(20, 120) * s
        for k in range(5):
            p.disc(x + k * 26 * s, y + rng.uniform(-8, 8) * s, rng.uniform(16, 26) * s, (252, 252, 255, 255))
    for k in range(30):                                                   # les vagues
        x, y = rng.uniform(0, W), rng.uniform(220, 440) * s
        p.line([(x, y), (x + 30 * s, y - 4 * s), (x + 60 * s, y)], (230, 240, 250, 255), 2 * s)
    for side in (-1, 1):                                                  # les rochers de la côte
        for _ in range(10):
            x = W / 2 + side * rng.uniform(420, 980) * s
            y = rng.uniform(300, 470) * s
            r = rng.uniform(40, 110) * s
            p.poly([(x - r, y + r * 0.6), (x - r * 0.6, y - r * 0.5), (x + r * 0.2, y - r * 0.8), (x + r, y - r * 0.1), (x + r * 0.8, y + r * 0.6)],
                   _rgba(rng.choice(((90, 80, 70), (110, 100, 86), (70, 62, 56)))), (40, 36, 30, 255), 2 * s)
        _clump(p, W / 2 + side * 900 * s, 200 * s, 80 * s, rng, ((40, 90, 50), (60, 120, 60)), n=6)
    c = SH_CELL * s
    x0, y0 = SH_X0 * s, SH_Y0 * s                                          # le plateau de bois
    w = 9 * c
    p.poly([(x0 - 14 * s, y0 - 14 * s), (x0 + w + 14 * s, y0 - 14 * s), (x0 + w + 14 * s, y0 + w + 14 * s), (x0 - 14 * s, y0 + w + 14 * s)],
           (190, 140, 70, 255), (100, 70, 30, 255), 3 * s)
    p.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + w), (x0, y0 + w)], (230, 190, 110, 255))
    for i in range(10):
        p.line([(x0 + i * c, y0), (x0 + i * c, y0 + w)], (60, 40, 20, 255), 2 * s)
        p.line([(x0, y0 + i * c), (x0 + w, y0 + i * c)], (60, 40, 20, 255), 2 * s)
    for i, j in ((3, 3), (6, 3), (3, 6), (6, 6)):
        p.disc(x0 + i * c, y0 + j * c, 4 * s, (60, 40, 20, 255))
    for side in (-1, 1):                                                  # les supports des pièces prises
        sx = x0 - 230 * s if side < 0 else x0 + w + 40 * s
        sy = y0 + (0 if side < 0 else w - 200 * s)                       # as in the game: theirs at the top left, ours at the bottom right
        p.poly([(sx, sy), (sx + 190 * s, sy), (sx + 190 * s, sy + 200 * s), (sx, sy + 200 * s)], (210, 160, 90, 255), (100, 70, 30, 255), 3 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


hd_bg.BUILDERS.update({"nd_grave": build_nd_grave, "ss_corridor": build_ss_corridor, "sh_coast": build_sh_coast})
hd_bg.BUILDERS.update({name: (lambda W, H, s, n=name: build_quiz(W, H, s, n)) for name in QZ_LOOKS})
hd_bg.BUILDERS.update({name: (lambda W, H, s, n=name: build_mahjong(W, H, s, n)) for name in MJ_LOOKS})
