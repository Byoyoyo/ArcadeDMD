"""The places of Metal Slug 2, missions 4 to 6, and the sky of its last boss (1.39.3). The same real look and the same
light of the cinema as dmd/hd_stages_ms.py, which tells the whole of it: a street of shops at nightfall, tunnels under
the ground, a mountain under the snow at the blue hour, a storm turning round an eye over a military base.

Every picture is our own drawing. None comes from a game. The marks of the signboards are invented and belong to no
writing, the flying machines are of our own drawing.

/ Les lieux de Metal Slug 2, missions 4 à 6, et le ciel de son dernier boss. Une rue commerçante à la tombée du jour, des
tunnels sous terre, une montagne sous la neige à l'heure bleue, un orage qui tourne autour d'un œil sur une base
militaire. Chaque image est notre dessin. Les marques des enseignes sont inventées, les engins volants aussi.
"""

import math
import random

from PIL import Image, ImageChops, ImageFilter, ImageOps

from . import hd_bg
from .hd_bg import vgrad
from .hd_real import (BRICK, FIRES, LIGHTS, MOODS, WOOD, Sheet, awning, cloud_layer, crate, drum, fractal, grade_cine,
                      lantern, lut, mountains, opening, pole, puff, rivets, sandbags, settled, shade, some, wheel, wires)


# ---------------------------------------------------------------------------- mission 4, a street of shops at nightfall / une rue commerçante


MOODS["rue"] = dict(sky=[(0.0, (14, 26, 58)), (0.14, (30, 52, 96)), (0.28, (70, 84, 124)), (0.40, (190, 120, 110)), (0.50, (246, 170, 110)), (0.62, (220, 140, 100)), (1.0, (80, 58, 60))],
                    sun=(0.62, 0.46), glare=(140, 80, 40), haze=(120, 98, 112), dust=(255, 200, 150), cast=(36, 10), soft=5.0,
                    shadow=(92, 84, 130), shadow_k=0.9, soot=(50, 44, 54), sunc=(255, 200, 140), rim=(255, 170, 110), lamps=0.5,
                    wall=(0.44, 0.40, 0.50), lampc=(255, 222, 172), pool_r=30, pool_k=1.7,
                    clouds=((255, 180, 130), (84, 80, 120), 0.9), grade=grade_cine, dim=1.0)


RENDER = ((170, 176, 158), (190, 162, 150), (176, 170, 140), (150, 164, 170), (196, 186, 164), (160, 150, 136))


BOARD = (((150, 40, 36), (232, 196, 110)), ((30, 80, 62), (236, 226, 196)), ((30, 26, 28), (214, 170, 70)), ((190, 150, 60), (120, 30, 30)),
         ((36, 60, 110), (236, 230, 210)), ((226, 216, 190), (150, 40, 36)))


def mark(sh, x, y, r, s, rng, col):
    """A mark for a sign, made of a few strokes in a square. It belongs to no writing.
    / Une marque d'enseigne, quelques traits dans un carré. Elle n'est d'aucune écriture."""
    w = max(1.4 * s, r * 0.2)
    for _ in range(rng.randint(2, 4)):
        k = rng.randint(0, 4)
        a, b = rng.uniform(-0.8, 0.8) * r, rng.uniform(-0.8, 0.8) * r
        if k == 0:
            sh.line([(x - r * 0.8, y + a), (x + r * 0.8, y + a)], col, w)
        elif k == 1:
            sh.line([(x + a, y - r * 0.8), (x + a, y + r * 0.8)], col, w)
        elif k == 2:
            sh.line([(x - r * 0.6, y + r * 0.7), (x + a * 0.4, y - r * 0.5)], col, w)
        elif k == 3:
            sh.line([(x + r * 0.6, y + r * 0.7), (x + a * 0.4, y - r * 0.2)], col, w)
        else:
            sh.rect(x + a * 0.5 - r * 0.3, y + b * 0.5 - r * 0.3, x + a * 0.5 + r * 0.3, y + b * 0.5 + r * 0.3, col)
            sh.rect(x + a * 0.5 - r * 0.3 + w, y + b * 0.5 - r * 0.3 + w, x + a * 0.5 + r * 0.3 - w, y + b * 0.5 + r * 0.3 - w, None)


def board(sh, x0, y0, x1, y1, s, rng, upright=False, lit=False):
    bg, fg = rng.choice(BOARD)
    sh.rect(x0 - 1.6 * s, y0 - 1.6 * s, x1 + 1.6 * s, y1 + 1.6 * s, (40, 34, 32), "cast")
    sh.rect(x0, y0, x1, y1, bg)
    if upright:
        r = (x1 - x0) * 0.36
        cy = y0 + r * 1.5
        while cy < y1 - r:
            mark(sh, (x0 + x1) / 2, cy, r, s, rng, fg)
            cy += r * 2.7
    else:
        r = (y1 - y0) * 0.34
        cx = x0 + r * 1.8
        while cx < x1 - r * 1.2:
            mark(sh, cx, (y0 + y1) / 2, r, s, rng, fg)
            cx += r * 2.8
    if lit:
        sh.rect(x0, y0, x1, y1, None, rng.choice(("glowR", "glowC", "lamp")), 150)
        sh.ellipse(x0 - 16 * s, y0 - 14 * s, x1 + 16 * s, y1 + 20 * s, None, "pool", 220)
        sh.lamps.append(((x0 + x1) / 2, (y0 + y1) / 2))


def paper_lamp(sh, x, y, s, k=1.0):
    sh.line([(x, y - 9 * s * k), (x, y - 5 * s * k)], (40, 34, 32), 0.9 * s)
    sh.ellipse(x - 6 * s * k, y - 6 * s * k, x + 6 * s * k, y + 7 * s * k, (226, 70, 44))
    sh.ellipse(x - 2.6 * s * k, y - 4 * s * k, x + 2.6 * s * k, y + 5 * s * k, (255, 196, 110))
    sh.rect(x - 3 * s * k, y - 7 * s * k, x + 3 * s * k, y - 5.4 * s * k, (190, 150, 60))
    sh.rect(x - 3 * s * k, y + 6 * s * k, x + 3 * s * k, y + 7.6 * s * k, (190, 150, 60))
    sh.ellipse(x - 12 * s * k, y - 12 * s * k, x + 12 * s * k, y + 13 * s * k, None, "glowR", 200)
    sh.ellipse(x - 40 * s * k, y - 30 * s * k, x + 40 * s * k, y + 50 * s * k, None, "pool", 200)
    sh.lamps.append((x, y))


def shophouse(sh, x, base, w, floors, s, rng, mood):
    """A narrow house over its shop. / Une maison étroite sur sa boutique."""
    brick = rng.random() < 0.45
    wall = rng.choice(BRICK if brick else RENDER)
    stone = (176, 168, 150)
    gf, fh = 100 * s, 80 * s
    top = base - gf - floors * fh - 16 * s
    sh.rect(x, top, x + w, base + 1, wall)
    if brick:
        yy = top
        while yy < base:
            sh.line([(x, yy), (x + w, yy)], shade(wall, 0.84), 0.7 * s)
            yy += 6 * s
    for px in (x, x + w - 10 * s):                                                                   # the piers at the edges
        sh.rect(px, top, px + 10 * s, base + 1, shade(stone, 0.92 if px > x else 1.0))
    sh.rect(x + w - 4 * s, top, x + w, base + 1, None, "dark", 170)
    for f in range(floors + 1):                                                                      # a string course at each floor
        yy = base - gf - f * fh
        sh.rect(x - 2 * s, yy - 6 * s, x + w + 2 * s, yy, stone, "cast")
        sh.rect(x - 2 * s, yy - 6 * s, x + w + 2 * s, yy - 4.4 * s, shade(stone, 1.14))
        sh.rect(x, yy, x + w, yy + 16 * s, None, "Dark", 90)
    q = rng.random()                                                                                 # the top of the front / le couronnement
    if q < 0.45:
        sh.d.chord([(x + w * 0.22) * 2, (top - 26 * s) * 2, (x + w * 0.78) * 2, (top + 26 * s) * 2], 180, 360, fill=shade(wall, 1.02))
        sh.md["cast"].chord([x + w * 0.22, top - 26 * s, x + w * 0.78, top + 26 * s], 180, 360, fill=255)
        sh.ellipse(x + w * 0.5 - 8 * s, top - 18 * s, x + w * 0.5 + 8 * s, top - 4 * s, shade(wall, 0.6))
    elif q < 0.8:
        bx = x + 12 * s
        while bx < x + w - 14 * s:                                                                   # balusters / des balustres
            sh.rect(bx, top - 14 * s, bx + 4 * s, top, stone)
            bx += 9 * s
        sh.rect(x, top - 17 * s, x + w, top - 13 * s, shade(stone, 1.1), "cast")
    for px in (x + 5 * s, x + w - 5 * s):
        sh.ellipse(px - 4 * s, top - 12 * s, px + 4 * s, top - 2 * s, stone)
    if rng.random() < 0.3:                                                                           # a tank on the roof
        tx = x + rng.uniform(0.2, 0.55) * w
        sh.rect(tx, top - 44 * s, tx + 30 * s, top - 14 * s, (96, 100, 100), "cast")
        sh.rect(tx + 20 * s, top - 44 * s, tx + 30 * s, top - 14 * s, None, "dark", 160)
    n = 2 if w < 190 * s else 3
    trim = stone if rng.random() < 0.6 else None
    for f in range(floors):
        sill = base - gf - f * fh - 22 * s
        for i in range(n):
            cx = x + 10 * s + (i + 0.5) * (w - 20 * s) / n
            opening(sh, cx, sill, 20 * s, 44 * s, s, rng, wall, mood, arch=rng.random() < 0.25, kind=rng.choice(("shutter", "shutter", "cloth", "void", "bars")),
                    soot=0.06, trim=trim)
        if rng.random() < 0.3:                                                                       # a pole of washing / une perche de linge
            sh.line([(x + 14 * s, sill + 8 * s), (x + w - 14 * s, sill + 8 * s)], (150, 130, 90), 1.4 * s, "cast")
            lx = x + 24 * s
            while lx < x + w - 28 * s:
                col = rng.choice(((200, 196, 186), (150, 66, 58), (74, 100, 130), (176, 150, 84), (84, 116, 104), (60, 60, 70)))
                ww, hh = rng.uniform(8, 13) * s, rng.uniform(14, 24) * s
                sh.rect(lx, sill + 9 * s, lx + ww, sill + 9 * s + hh, col, "cast")
                lx += ww + rng.uniform(4, 12) * s
        elif rng.random() < 0.3:                                                                     # plants on the ledge
            for _ in range(rng.randint(2, 4)):
                px = x + rng.uniform(16, w / s - 16) * s
                sh.rect(px - 4 * s, base - gf - f * fh - 12 * s, px + 4 * s, base - gf - f * fh - 6 * s, (130, 80, 56))
                sh.ellipse(px - 8 * s, base - gf - f * fh - 26 * s, px + 8 * s, base - gf - f * fh - 10 * s, shade((64, 96, 58), rng.uniform(0.8, 1.2)))
    if rng.random() < 0.5:                                                                           # a sign standing out from the wall
        sx = x + (6 * s if rng.random() < 0.5 else w - 24 * s)
        sy = base - gf - floors * fh + rng.uniform(10, 30) * s
        sh.rect(sx - 3 * s, sy - 4 * s, sx + 21 * s, sy - 1 * s, (40, 34, 32))
        board(sh, sx, sy, sx + 18 * s, sy + rng.uniform(70, 120) * s, s, rng, upright=True, lit=rng.random() < 0.5)
    sh.rect(x + 10 * s, base - gf + 2 * s, x + w - 10 * s, base - gf + 26 * s, None)                 # the board over the shop
    board(sh, x + 12 * s, base - gf + 3 * s, x + w - 12 * s, base - gf + 25 * s, s, rng, lit=rng.random() < 0.4)
    x0, x1, y0 = x + 16 * s, x + w - 16 * s, base - gf + 30 * s
    sh.rect(x0 - 3 * s, y0 - 3 * s, x1 + 3 * s, base, None, "hole")
    q = rng.random()
    if q < 0.55:                                                                                     # the shop is open / la boutique est ouverte
        sh.rect(x0, y0, x1, base + 1, (22, 18, 20))
        for row in (46, 26):
            gx = x0 + 9 * s
            while gx < x1 - 7 * s:
                col = rng.choice(((150, 92, 56), (176, 150, 92), (104, 118, 78), (150, 70, 58), (190, 180, 156), (72, 96, 116)))
                r = rng.uniform(4.0, 6.5) * s
                sh.ellipse(gx - r, base - row * s - r * 2, gx + r, base - row * s, shade(col, 0.8))
                gx += rng.uniform(12, 18) * s
            sh.line([(x0, base - row * s), (x1, base - row * s)], shade(WOOD, 0.9), 1.4 * s)
        sh.rect(x0, base - 20 * s, x1, base + 1, shade(WOOD, 1.1), "cast")
        sh.rect(x0, base - 20 * s, x1, base - 17 * s, shade(WOOD, 1.5))
        sh.rect(x0, y0, x1, base - 20 * s, None, "pool", 230)
        sh.rect(x0 - 10 * s, y0 - 4 * s, x1 + 10 * s, base, None, "pool", 120)
        paper_lamp(sh, x0 + (x1 - x0) * rng.uniform(0.25, 0.75), y0 + 12 * s, s)
    elif q < 0.85:                                                                                   # an iron shutter, down / un rideau de fer
        col = rng.choice(((104, 112, 108), (92, 104, 116), (120, 110, 96)))
        sh.rect(x0, y0, x1, base + 1, col)
        yy = y0
        while yy < base:
            sh.line([(x0, yy), (x1, yy)], shade(col, 0.72), 0.9 * s)
            yy += 4.5 * s
        sh.rect(x0, base - 30 * s, x1, base, None, "Dark", 130)
    else:                                                                                            # doors of wood, one ajar
        px = x0
        while px < x1:
            sh.rect(px, y0, min(x1, px + 9 * s), base + 1, shade(WOOD, rng.uniform(0.9, 1.3)))
            px += 9 * s
        gx = x0 + (x1 - x0) * rng.uniform(0.3, 0.6)
        sh.rect(gx, y0, gx + 16 * s, base + 1, (255, 200, 126))
        sh.rect(gx, y0, gx + 16 * s, base, None, "lamp")
        sh.ellipse(gx - 30 * s, y0 - 10 * s, gx + 46 * s, base + 10 * s, None, "pool", 220)
    if rng.random() < 0.5:                                                                           # a cloth over the shop
        awning(sh, x + 8 * s, x + w - 8 * s, base - gf + 28 * s, s, rng, base)
    sh.line([(x + w - 13 * s, top), (x + w - 13 * s, base)], (70, 70, 72), 2.2 * s, "cast")           # the drain pipe
    sh.rect(x, base - 22 * s, x + w, base + 1, None, "Dark", 120)
    return top


def tiered(sh, x, base, s, rng):
    """A tower with roofs one over the other, far away. / Une tour aux toits superposés, au loin."""
    w, y = 62 * s, base
    for i in range(5):
        hgt = (40 - i * 4) * s
        sh.rect(x - w / 2, y - hgt, x + w / 2, y, (120, 88, 70), "cast")
        sh.poly([(x - w / 2 - 16 * s, y - hgt + 4 * s), (x - w / 2 - 10 * s, y - hgt - 2 * s), (x + w / 2 + 10 * s, y - hgt - 2 * s), (x + w / 2 + 16 * s, y - hgt + 4 * s),
                 (x + w / 2, y - hgt - 12 * s), (x - w / 2, y - hgt - 12 * s)], (60, 66, 62), "cast")
        y -= hgt + 10 * s
        w *= 0.84
    sh.line([(x, y + 6 * s), (x, y - 22 * s)], (70, 62, 50), 2 * s)


def street(W, H, s, seed=134):
    """Mission 4. A street of shops at nightfall, its lamps and its signs. / Une rue commerçante à la tombée du jour."""
    mood = MOODS["rue"]
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.72)
    sky = vgrad(W, H, mood["sky"])
    sun = (int(W * mood["sun"][0]), int(H * mood["sun"][1]))
    hd_bg.add_at(sky, hd_bg.radial(int(1200 * s), mood["glare"], 2.2), *sun)
    white, grey, k = mood["clouds"]
    layers = [cloud_layer(tw, int(H * 0.5), rng, s, cover=132, white=white, grey=grey, k=k, stretch=2.6, f=0.02)]
    h = int(230 * s)
    layers.append(mountains(tw, h, rng, s, mood, (96, 110, 96), 0.5, int(96 * s), 0.05, rough=0.8))

    h = int(330 * s)                                                 # the town behind / la ville derrière
    sh = Sheet(tw, h, s)
    x = 0.0
    while x < tw - 80 * s:
        w, bh = rng.uniform(70, 150) * s, rng.uniform(120, 290) * s
        col = rng.choice(RENDER + BRICK)
        sh.rect(x, h - bh, x + w, h, col)
        sh.rect(x + w * 0.86, h - bh, x + w, h, None, "dark", 160)
        sh.rect(x - 2 * s, h - bh - 4 * s, x + w + 2 * s, h - bh, shade(col, 1.1), "cast")
        yy = h - bh + 16 * s
        while yy < h - 20 * s:
            cx = x + 10 * s
            while cx < x + w * 0.84 - 8 * s:
                lit = rng.random() < 0.22
                sh.rect(cx, yy, cx + 7 * s, yy + 12 * s, (255, 206, 130) if lit else (30, 28, 34))
                if lit:
                    sh.rect(cx - 2 * s, yy - 2 * s, cx + 9 * s, yy + 14 * s, None, "lamp", 170)
                    sh.ellipse(cx - 8 * s, yy - 8 * s, cx + 15 * s, yy + 20 * s, None, "pool", 200)
                cx += 16 * s
            yy += 26 * s
        if rng.random() < 0.3:
            sh.rect(x + w * 0.3, h - bh - 22 * s, x + w * 0.3 + 20 * s, h - bh - 4 * s, (90, 94, 96), "cast")
        x += w + rng.uniform(-10, 14) * s
    tiered(sh, tw * 0.3, h, s, rng)
    layers.append({"img": sh.finish(rng, mood, depth=0.42, blur=0.9, tex=0.7), "y": H - int(66 * s) - h, "f": 0.16, "stage": "far"})

    h = int(446 * s)                                                 # the street / la rue
    base = h - 1
    sh = Sheet(tw, h, s)
    x = 6 * s
    tops, fires = [], []
    while x < tw - 150 * s:
        w, floors = rng.uniform(150, 232) * s, rng.choice((2, 3, 3, 3))
        if x + w > tw - 150 * s:
            w = tw - 8 * s - x
        top = shophouse(sh, x, base, w, floors, s, rng, mood)
        tops.append((x, w, top))
        if rng.random() < 0.14:
            fires.append((x + w * rng.uniform(0.3, 0.7), top - 6 * s))
        x += w + (rng.uniform(26, 46) * s if rng.random() < 0.2 else 0)
    for (xa, wa, ta), (xb, wb, tb) in zip(tops, tops[1:]):          # lamps strung over the street / des lampions en travers
        if rng.random() < 0.45:
            y0, x0, x1 = base - 104 * s, xa + wa * 0.3, xb + wb * 0.7
            pts = [(x0 + (x1 - x0) * i / 12, y0 + 16 * s * 4 * (i / 12) * (1 - i / 12)) for i in range(13)]
            sh.line(pts, (40, 34, 32), 0.7 * s)
            for i in range(2, 11, 2):
                paper_lamp(sh, pts[i][0], pts[i][1] + 9 * s, s, 0.8)
    ps = [tw * (i + 0.4) / 5 for i in range(5)]
    for px in ps:
        pole(sh, px, base, 350 * s, s)
    wires(sh, ps, base, 350 * s, s, tw)
    layers.append({"img": sh.finish(rng, mood, depth=0.02, tex=0.8), "y": H - h - int(36 * s), "f": 0.38, "stage": "mid",
                   "fires": some(rng, fires, FIRES), "lights": some(rng, sh.lamps, LIGHTS)})

    h = int(108 * s)                                                 # the roadway / la chaussée
    sh = Sheet(tw, h, s)
    gy0 = h * 0.40
    sh.rect(0, gy0, tw, h, (112, 106, 104))
    sh.rect(0, gy0, tw, gy0 + 9 * s, (150, 144, 136))                # the kerb / le trottoir
    x = 0.0
    while x < tw:
        sh.line([(x, gy0), (x, gy0 + 9 * s)], (96, 92, 90), 1.0 * s)
        x += 36 * s
    for _ in range(int(tw / (160 * s))):                             # wet patches that catch the lamps / des flaques
        px, py = rng.uniform(0, tw), rng.uniform(gy0 + 20 * s, h * 0.9)
        rw = rng.uniform(40, 110) * s
        sh.ellipse(px - rw, py - 5 * s, px + rw, py + 6 * s, (100, 96, 106))
        sh.ellipse(px - rw * 0.8, py - 4 * s, px + rw * 0.6, py + 4 * s, None, "Light", 200)
        sh.ellipse(px - rw, py - 30 * s, px + rw, py + 30 * s, None, "pool", 200)
    x = 50 * s
    while x < tw - 200 * s:
        gy = gy0 + 8 * s
        q = rng.random()
        if q < 0.3:
            w = sandbags(sh, x, gy, s, rng, cols=((150, 140, 112), (136, 126, 100), (160, 150, 122)))
            sh.rect(x, gy - 30 * s, x + w, gy + 8 * s, None, "cast", 200)
        elif q < 0.6:                                                # baskets of goods / des paniers
            n = rng.randint(2, 4)
            for i in range(n):
                bx = x + i * 30 * s
                sh.poly([(bx, gy - 16 * s), (bx + 26 * s, gy - 16 * s), (bx + 22 * s, gy + 4 * s), (bx + 4 * s, gy + 4 * s)], (150, 118, 72), "cast")
                sh.ellipse(bx + 1 * s, gy - 24 * s, bx + 25 * s, gy - 12 * s, rng.choice(((170, 80, 50), (120, 140, 70), (200, 170, 80), (150, 60, 70))))
            w = n * 30 * s
        elif q < 0.8:                                                # a handcart / une charrette à bras
            sh.rect(x, gy - 26 * s, x + 74 * s, gy - 18 * s, (112, 88, 62), "cast")
            sh.rect(x, gy - 44 * s, x + 4 * s, gy - 18 * s, (96, 76, 54))
            sh.rect(x + 70 * s, gy - 44 * s, x + 74 * s, gy - 18 * s, (96, 76, 54))
            wheel(sh, x + 37 * s, gy + 6 * s, 16 * s, s, 8)
            sh.line([(x + 74 * s, gy - 22 * s), (x + 112 * s, gy - 30 * s)], (96, 76, 54), 2.4 * s)
            crate(sh, x + 10 * s, gy - 26 * s, 30 * s, 22 * s, s, (132, 106, 76))
            w = 114 * s
        else:
            for i in range(rng.randint(1, 3)):
                drum(sh, x + i * 24 * s, gy, s, rng.choice(((112, 70, 58), (84, 96, 76), (78, 90, 108))))
                sh.rect(x + i * 24 * s, gy - 30 * s, x + i * 24 * s + 20 * s, gy + 6 * s, None, "cast")
            w = 70 * s
        x += w + rng.uniform(120, 300) * s
    sh.rect(0, gy0 - 2 * s, tw, gy0 + 3 * s, None, "Dark", 120)
    sh.rect(0, h * 0.84, tw, h + 4, None, "Dark", 180)
    layers.append({"img": sh.finish(rng, mood, tex=0.7, bump_k=0.4, blur=0.5), "y": H - h, "f": 1.0, "stage": "near"})

    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": sun, "explosions": True, "plane": "heli", "plane_color": (50, 54, 66),
           "dust": mood["dust"], "window": (255, 160, 80), "hooks": {"mid": [hd_stages.hook_fires]}}
    sky = mood["grade"](sky)
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- mission 5, tunnels under the ground / des tunnels sous terre


def grade_tunnel(rgb):
    f = lambda v: max(0, min(255, int(108 + (v - 108) * 1.22)))
    return lut(rgb, lambda v: int(f(v) * 0.93), lambda v: min(255, f(v) + 2), lambda v: min(255, int(f(v) * 0.97 + 4)))


MOODS["tunnel"] = dict(sky=[(0.0, (8, 12, 12)), (1.0, (18, 24, 22))], sun=(0.5, 0.0), glare=(0, 0, 0), haze=(20, 30, 28), dust=(190, 240, 220),
                       cast=(8, 14), soft=4.0, shadow=(90, 96, 104), shadow_k=0.86, soot=(34, 36, 36), sunc=(226, 255, 240), rim=None,
                       lamps=0.0, wall=(0.25, 0.30, 0.29), lampc=(226, 255, 238), lampglow=(170, 255, 214), pool_r=44, pool_k=1.9,
                       clouds=None, grade=grade_tunnel, dim=1.0)


CONCRETE = ((132, 134, 126), (120, 124, 118), (142, 142, 132), (112, 116, 112))


STEEL = (84, 96, 92)


def panels(sh, x0, y0, x1, y1, s, rng, cols, bw, bh):
    y, j = y0, 0
    while y < y1:
        yb = min(y1, y + bh * s)
        x = x0 - (j % 2) * bw * 0.5 * s
        while x < x1:
            w = bw * s * rng.uniform(0.9, 1.1)
            xa, xb = max(x0, x), min(x1, x + w)
            if xb > xa:
                col = shade(rng.choice(cols), rng.uniform(0.92, 1.06))
                sh.rect(xa, y, xb, yb, col)
                sh.rect(xb - 1.4 * s, y, xb, yb, shade(col, 0.6))
                sh.rect(xa, yb - 1.4 * s, xb, yb, shade(col, 0.55))
            x += w
        y, j = yb, j + 1


def pipe(sh, x0, x1, y, r, s, col, step=180):
    sh.rect(x0, y - r, x1, y + r, col, "cast")
    sh.rect(x0, y + r * 0.2, x1, y + r, None, "dark", 190)
    sh.rect(x0, y - r * 0.7, x1, y - r * 0.3, None, "light", 140)
    x = x0 + step * s * 0.5
    while x < x1:
        sh.rect(x - 3 * s, y - r - 2.5 * s, x + 3 * s, y + r + 2.5 * s, shade(col, 0.8), "cast")       # a flange / une bride
        sh.rect(x + 40 * s, y - r - 9 * s, x + 44 * s, y - r, (50, 54, 54))                           # a hanger / un collier
        x += step * s


def cage_lamp(sh, x, y, s, pool=120):
    sh.rect(x - 8 * s, y - 5 * s, x + 8 * s, y + 6 * s, (224, 255, 238))
    for dx in (-8, -3, 3, 8):
        sh.line([(x + dx * s, y - 6 * s), (x + dx * s, y + 7 * s)], (40, 46, 44), 0.9 * s)
    sh.rect(x - 10 * s, y - 9 * s, x + 10 * s, y - 5 * s, (60, 66, 64), "cast")
    sh.ellipse(x - 16 * s, y - 12 * s, x + 16 * s, y + 14 * s, None, "lamp")
    sh.ellipse(x - pool * s, y - pool * 0.6 * s, x + pool * s, y + pool * 1.6 * s, None, "pool")
    sh.lamps.append((x, y))


def hazard(sh, x0, y0, x1, y1, s):
    sh.rect(x0, y0, x1, y1, (196, 160, 40))
    x = x0 - (y1 - y0)
    while x < x1:
        pts = [(x, y1), (x + (y1 - y0), y0), (x + (y1 - y0) + 8 * s, y0), (x + 8 * s, y1)]
        pts = [(max(x0, min(x1, px)), py) for px, py in pts]
        sh.poly(pts, (30, 30, 30))
        x += 16 * s


def mouth(sh, x, base, w, h, s):
    """The mouth of a tunnel and its ribs. / La bouche d'un tunnel et ses cintres."""
    sh.rect(x - w / 2 - 14 * s, base - h - 14 * s, x + w / 2 + 14 * s, base, None, "hole")
    for i, k in enumerate((1.0, 0.86, 0.72, 0.58)):
        col = shade((70, 76, 72), 1.0 - i * 0.22)
        ww, hh = w * k, h * k
        sh.ellipse(x - ww / 2, base - hh, x + ww / 2, base - hh + ww, col)
        sh.rect(x - ww / 2, base - hh + ww / 2, x + ww / 2, base, col)
    sh.ellipse(x - w * 0.24, base - h * 0.50, x + w * 0.24, base - h * 0.5 + w * 0.48, (6, 8, 8))
    sh.rect(x - w * 0.24, base - h * 0.5 + w * 0.24, x + w * 0.24, base, (6, 8, 8))
    for dx in (-1, 1):                                                                               # the rails run in / les rails s'enfoncent
        sh.line([(x + dx * w * 0.30, base), (x + dx * w * 0.07, base - h * 0.22)], (120, 126, 120), 1.6 * s)
    sh.ellipse(x + w * 0.10, base - h * 0.42, x + w * 0.10 + 7 * s, base - h * 0.42 + 7 * s, (255, 80, 60))
    sh.ellipse(x + w * 0.10 - 6 * s, base - h * 0.42 - 6 * s, x + w * 0.10 + 13 * s, base - h * 0.42 + 13 * s, None, "glowR")
    hazard(sh, x - w / 2 - 14 * s, base - h - 30 * s, x + w / 2 + 14 * s, base - h - 14 * s, s)


def girder(sh, x, base, w, top, s, rng):
    """A column of riveted steel. / Un poteau d'acier riveté."""
    sh.rect(x - w / 2, top, x + w / 2, base, STEEL, "cast")
    sh.rect(x - w / 2, top, x - w / 2 + 5 * s, base, shade(STEEL, 1.3))
    sh.rect(x + w / 2 - 5 * s, top, x + w / 2, base, shade(STEEL, 0.6))
    sh.rect(x - w * 0.16, top, x + w * 0.5 - 5 * s, base, None, "dark", 120)
    y = top + 10 * s
    while y < base - 50 * s:
        for dx in (-w / 2 + 2.5 * s, w / 2 - 2.5 * s):
            sh.ellipse(x + dx - 1.1 * s, y - 1.1 * s, x + dx + 1.1 * s, y + 1.1 * s, (40, 46, 44))
        y += 13 * s
    hazard(sh, x - w / 2, base - 46 * s, x + w / 2, base - 6 * s, s)
    sh.rect(x - w / 2 - 8 * s, base - 6 * s, x + w / 2 + 8 * s, base + 2, shade(STEEL, 0.9), "cast")
    for yy in (top + 90 * s, top + 96 * s):                                                          # rust runs down / la rouille coule
        sh.poly([(x - 6 * s, yy), (x + 4 * s, yy), (x + 1 * s, yy + rng.uniform(60, 140) * s)], None, "Dark", 120)


def cabinet(sh, x, base, s, rng):
    w, h = rng.uniform(60, 90) * s, rng.uniform(96, 130) * s
    col = (92, 104, 100)
    sh.rect(x, base - h, x + w, base, col, "cast")
    sh.rect(x + w * 0.86, base - h, x + w, base, None, "dark", 160)
    sh.line([(x + w * 0.5, base - h), (x + w * 0.5, base)], shade(col, 0.6), 1.2 * s)
    blinks = []
    for i in range(rng.randint(3, 6)):
        lx, ly = x + 10 * s + (i % 3) * 14 * s, base - h + 14 * s + (i // 3) * 14 * s
        kind = rng.choice(("glowR", "glowC", "lamp"))
        sh.ellipse(lx - 2.6 * s, ly - 2.6 * s, lx + 2.6 * s, ly + 2.6 * s, {"glowR": (255, 80, 60), "glowC": (90, 230, 255), "lamp": (255, 220, 140)}[kind])
        sh.ellipse(lx - 6 * s, ly - 6 * s, lx + 6 * s, ly + 6 * s, None, kind, 200)
        if kind == "glowR" and not blinks:
            blinks.append((lx, ly))
    for i in range(4):                                                                               # dials / des cadrans
        dx = x + w * 0.5 + 10 * s + (i % 2) * 16 * s
        dy = base - h + 18 * s + (i // 2) * 18 * s
        if dx + 6 * s < x + w * 0.86:
            sh.ellipse(dx - 6 * s, dy - 6 * s, dx + 6 * s, dy + 6 * s, (196, 200, 186))
            sh.line([(dx, dy), (dx + rng.uniform(-4, 4) * s, dy - 4 * s)], (30, 30, 30), 0.8 * s)
    return w, blinks


def tunnels(W, H, s, seed=135):
    """Mission 5. Under the ground: concrete, steel, pipes, the lamps of the works. / Sous terre."""
    mood = MOODS["tunnel"]
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    sky = vgrad(W, H, mood["sky"])
    layers = []

    h = H                                                            # the wall at the back / la paroi du fond
    floor_y = H - int(86 * s)
    sh = Sheet(tw, h, s)
    panels(sh, 0, 0, tw, floor_y, s, rng, CONCRETE, 150, 74)
    sh.rect(0, 196 * s, tw, 262 * s, (150, 158, 148))                # a band of tiles / un bandeau de carreaux
    x = 0.0
    while x < tw:
        sh.line([(x, 196 * s), (x, 262 * s)], (104, 112, 106), 0.8 * s)
        x += 16 * s
    for yy in (196, 212, 228, 244, 262):
        sh.line([(0, yy * s), (tw, yy * s)], (104, 112, 106), 0.8 * s)
    sh.rect(0, 226 * s, tw, 234 * s, (44, 92, 78))
    xs = []
    x = rng.uniform(180, 320) * s
    while x < tw - 260 * s:
        mouth(sh, x, floor_y, 250 * s, 240 * s, s)
        xs.append(x)
        x += rng.uniform(720, 900) * s
    pipe(sh, 0, tw, 52 * s, 9 * s, s, (104, 84, 62))
    pipe(sh, 0, tw, 78 * s, 6 * s, s, (84, 100, 104), 140)
    pipe(sh, 0, tw, 100 * s, 4 * s, s, (120, 120, 110), 110)
    for a, b in zip(xs, xs[1:] + [xs[0] + tw]):                       # between the mouths: lamps, doors, boards
        span = b - a - 290 * s
        n = max(1, int(span / (230 * s)))
        for k in range(n):
            cx = (a + 145 * s + span * (k + 0.5) / n) % tw
            cage_lamp(sh, cx, 150 * s, s)
            q = rng.random()
            if q < 0.4:                                               # a steel door / une porte d'acier
                sh.rect(cx - 30 * s, floor_y - 118 * s, cx + 30 * s, floor_y, None, "hole")
                sh.rect(cx - 27 * s, floor_y - 114 * s, cx + 27 * s, floor_y, (74, 90, 84))
                sh.rect(cx - 27 * s, floor_y - 114 * s, cx + 27 * s, floor_y - 110 * s, (110, 124, 116))
                sh.ellipse(cx - 9 * s, floor_y - 70 * s, cx + 9 * s, floor_y - 52 * s, (50, 56, 54))
                sh.ellipse(cx - 5 * s, floor_y - 66 * s, cx + 5 * s, floor_y - 56 * s, (74, 90, 84))
                rivets(sh, cx - 24 * s, cx + 26 * s, floor_y - 104 * s, s, 8)
                rivets(sh, cx - 24 * s, cx + 26 * s, floor_y - 8 * s, s, 8)
            elif q < 0.75:                                            # a board with marks / un panneau
                board(sh, cx - 46 * s, 274 * s, cx + 46 * s, 298 * s, s, rng)
            else:                                                     # a grille / une grille d'aération
                sh.rect(cx - 30 * s, 290 * s, cx + 30 * s, 330 * s, (40, 46, 44))
                for j in range(1, 7):
                    sh.line([(cx - 30 * s, 290 * s + j * 5.7 * s), (cx + 30 * s, 290 * s + j * 5.7 * s)], (96, 104, 98), 1.2 * s)
                sh.poly([(cx - 24 * s, 330 * s), (cx + 24 * s, 330 * s), (cx + 10 * s, floor_y), (cx - 14 * s, floor_y)], None, "Dark", 130)
    for _ in range(26):                                              # water has run down the wall / des coulures
        cx, cy = rng.uniform(0, tw), rng.uniform(110, 190) * s
        sh.poly([(cx, cy), (cx + rng.uniform(4, 12) * s, cy), (cx + rng.uniform(-2, 6) * s, cy + rng.uniform(60, 190) * s)], None, "Dark", rng.randint(70, 140))
    x = 0.0
    while x < tw:                                                    # cables / des câbles
        x1 = x + rng.uniform(160, 260) * s
        for dy in (118, 124):
            sh.line([(x + (x1 - x) * i / 8, dy * s + 8 * s * 4 * (i / 8) * (1 - i / 8)) for i in range(9)], (30, 34, 34), 1.2 * s)
        x = x1
    sh.rect(0, floor_y - 24 * s, tw, floor_y + 2, None, "Dark", 140)
    sh.rect(0, floor_y, tw, h, (104, 108, 102))                      # the platform / le quai
    sh.rect(0, floor_y + 8 * s, tw, floor_y + 14 * s, (190, 160, 50))
    layers.append({"img": sh.finish(rng, mood, depth=0.08, blur=0.6, tex=1.0, bump_k=0.2), "y": 0, "f": 0.16, "stage": "far",
                   "lights": some(rng, sh.lamps, LIGHTS)})

    h = H - int(34 * s)                                              # the steel in front of it / l'acier devant
    base = h - 32 * s
    sh = Sheet(tw, h, s)
    sh.rect(0, 0, tw, 8 * s, STEEL, "cast")                          # a lattice beam overhead / une poutre en treillis
    sh.rect(0, 40 * s, tw, 48 * s, STEEL, "cast")
    x = 0.0
    while x < tw:
        sh.line([(x, 8 * s), (x + 40 * s, 40 * s)], shade(STEEL, 0.9), 3 * s)
        sh.line([(x + 40 * s, 40 * s), (x + 80 * s, 8 * s)], shade(STEEL, 0.76), 3 * s)
        x += 80 * s
    stacks, blinks = [], []
    x = rng.uniform(80, 180) * s
    while x < tw - 170 * s:
        girder(sh, x, base, 38 * s, 0, s, rng)
        gap = rng.uniform(330, 450) * s
        mx = x + gap * 0.5
        sh.line([(mx, 48 * s), (mx, 92 * s)], (30, 34, 34), 1.4 * s)   # a lamp hung from the beam / une lampe suspendue
        sh.poly([(mx - 18 * s, 106 * s), (mx - 6 * s, 92 * s), (mx + 6 * s, 92 * s), (mx + 18 * s, 106 * s)], (56, 66, 62), "cast")
        sh.ellipse(mx - 7 * s, 102 * s, mx + 7 * s, 114 * s, (232, 255, 240))
        sh.ellipse(mx - 18 * s, 96 * s, mx + 18 * s, 124 * s, None, "lamp")
        sh.poly([(mx - 14 * s, 106 * s), (mx + 14 * s, 106 * s), (mx + 170 * s, base + 10 * s), (mx - 170 * s, base + 10 * s)], None, "pool", 230)
        sh.lamps.append((mx, 108 * s))
        q = rng.random()
        px = x + 50 * s
        if q < 0.34:
            w, bl = cabinet(sh, px + rng.uniform(0, 40) * s, base, s, rng)
            blinks += bl
        elif q < 0.6:                                                 # a valve and its leak / une vanne qui fuit
            vx = px + rng.uniform(20, 60) * s
            pipe(sh, vx - 40 * s, vx + 90 * s, base - 40 * s, 8 * s, s, (104, 84, 62), 400)
            sh.rect(vx - 44 * s, base - 40 * s, vx - 32 * s, base, (96, 78, 58), "cast")
            sh.rect(vx + 82 * s, base - 40 * s, vx + 94 * s, base, (96, 78, 58), "cast")
            sh.ellipse(vx + 10 * s, base - 72 * s, vx + 38 * s, base - 44 * s, (150, 50, 40), "cast")
            sh.ellipse(vx + 16 * s, base - 66 * s, vx + 32 * s, base - 50 * s, (60, 66, 64))
            stacks.append((vx + 60 * s, base - 50 * s))
        elif q < 0.85:
            for i in range(rng.randint(2, 4)):
                drum(sh, px + i * 24 * s, base - 6 * s, s, rng.choice(((112, 70, 58), (84, 96, 76), (150, 130, 50), (78, 90, 108))))
                sh.rect(px + i * 24 * s, base - 36 * s, px + i * 24 * s + 20 * s, base, None, "cast")
        else:
            crate(sh, px, base, 46 * s, 36 * s, s, (118, 104, 82))
            crate(sh, px + 50 * s, base, 34 * s, 28 * s, s, (132, 112, 84))
            sh.rect(px, base - 36 * s, px + 84 * s, base, None, "cast", 220)
        x += gap
    img = sh.finish(rng, dict(mood, wall=(0.34, 0.40, 0.38)), tex=0.9, bump_k=0.2)
    for vx, vy in stacks:                                            # the steam of a leak / la vapeur d'une fuite
        puff(img, [(vx + i * 6 * s, vy - i * 22 * s, (12 + i * 7) * s) for i in range(6)], (200, 236, 222), 9 * s, 0.4)
    layers.append({"img": img, "y": 0, "f": 0.38, "stage": "mid", "stacks": stacks[:2], "blinks": blinks[:6],
                   "lights": some(rng, sh.lamps, 6)})

    h = int(104 * s)                                                 # the floor and the rails / le sol et les rails
    sh = Sheet(tw, h, s)
    gy = h * 0.34
    sh.rect(0, gy, tw, h, (104, 108, 102))
    x = 0.0
    while x < tw:
        sh.rect(x, gy + 26 * s, x + 16 * s, gy + 58 * s, (60, 54, 48))   # the sleepers / les traverses
        x += 40 * s
    for yy in (gy + 30 * s, gy + 52 * s):
        sh.rect(0, yy, tw, yy + 4 * s, (70, 74, 74), "cast")
        sh.rect(0, yy, tw, yy + 1.4 * s, (170, 180, 176))
    for _ in range(int(tw / (150 * s))):                             # water on the floor / de l'eau au sol
        px, py = rng.uniform(0, tw), rng.uniform(gy + 4 * s, gy + 22 * s)
        rw = rng.uniform(30, 90) * s
        sh.ellipse(px - rw, py - 4 * s, px + rw, py + 4 * s, (86, 96, 94))
        sh.ellipse(px - rw * 0.8, py - 3 * s, px + rw * 0.6, py + 3 * s, None, "Light", 190)
    for _ in range(7):
        px = rng.uniform(0, tw)
        sh.ellipse(px - 170 * s, gy - 30 * s, px + 170 * s, gy + 70 * s, None, "pool", 210)
    sh.rect(0, gy - 2 * s, tw, gy + 6 * s, None, "Dark", 150)
    sh.rect(0, h * 0.8, tw, h + 4, None, "Dark", 190)
    layers.append({"img": sh.finish(rng, mood, tex=0.8, bump_k=0.4, blur=0.5), "y": H - h, "f": 1.0, "stage": "near"})

    from . import hd_stages
    amb = {"stars": (), "horizon": int(H * 0.84), "sun": (W // 2, 0), "explosions": False, "dust": mood["dust"], "window": (190, 255, 220),
           "blink": (255, 40, 30), "hooks": {"mid": [hd_stages.hook_stacks]}}
    return {"sky": mood["grade"](sky), "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- mission 6, a mountain under the snow / une montagne sous la neige


def grade_snow(rgb):
    f = lambda v: max(0, min(255, int(116 + (v - 116) * 1.2)))
    return lut(rgb, lambda v: int(f(v) * 0.96), lambda v: min(255, int(f(v) * 1.0 + 2)), lambda v: min(255, int(f(v) * 1.06 + 8)))


MOODS["neige"] = dict(sky=[(0.0, (20, 34, 62)), (0.24, (46, 68, 104)), (0.46, (104, 128, 156)), (0.60, (176, 176, 180)), (0.70, (214, 190, 170)), (1.0, (120, 130, 150))],
                      sun=(0.70, 0.58), glare=(70, 50, 34), haze=(130, 150, 176), dust=(230, 240, 255), cast=(30, 12), soft=5.0,
                      shadow=(96, 112, 160), shadow_k=0.86, soot=(40, 44, 56), sunc=(226, 236, 255), rim=(200, 220, 255), lamps=0.6,
                      wall=(0.50, 0.58, 0.74), lampc=(255, 220, 168), pool_r=36, pool_k=1.8,
                      clouds=((220, 226, 236), (92, 108, 138), 0.9), grade=grade_snow, dim=1.0)


SNOW = (236, 242, 250)


TIMBER = ((112, 86, 62), (98, 76, 56), (124, 96, 68), (90, 70, 54))


def snow_on(sh, x0, x1, y, s, rng, thick=7):
    """Snow lying on a ledge, heavier in the middle. / De la neige posée sur un rebord."""
    n = max(3, int((x1 - x0) / (14 * s)))
    pts = [(x0 - 3 * s, y)]
    for i in range(n + 1):
        k = i / n
        pts.append((x0 + (x1 - x0) * k, y - thick * s * (0.5 + 0.5 * math.sin(math.pi * k)) - rng.uniform(0, 2.5) * s))
    pts.append((x1 + 3 * s, y))
    for i in range(n, -1, -1):                                                                       # it hangs a little / elle déborde
        k = i / n
        pts.append((x0 + (x1 - x0) * k, y + rng.uniform(0.5, 3.5) * s))
    sh.poly(pts, SNOW, "cast")
    sh.poly([(x0, y - 1 * s), (x1, y - 1 * s), (x1, y + 3 * s), (x0, y + 3 * s)], None, "dark", 70)


def fir(sh, x, base, h, s, rng):
    w = h * 0.34
    sh.rect(x - 2.4 * s, base - h * 0.14, x + 2.4 * s, base, (60, 46, 38))
    for i in range(5):
        y0 = base - h * (0.10 + i * 0.17)
        ww = w * (1 - i * 0.17)
        col = shade((44, 78, 62), rng.uniform(0.86, 1.1))
        sh.poly([(x - ww, y0), (x, y0 - h * 0.30), (x + ww, y0)], col, "cast")
        sh.poly([(x, y0 - h * 0.30), (x + ww, y0), (x + ww * 0.2, y0)], None, "dark", 120)
        sh.poly([(x - ww * 0.7, y0 - h * 0.09), (x, y0 - h * 0.30), (x + ww * 0.5, y0 - h * 0.12), (x + ww * 0.1, y0 - h * 0.16), (x - ww * 0.3, y0 - h * 0.08)], SNOW)


def planks(sh, x0, y0, x1, y1, s, rng, upright=True):
    col = rng.choice(TIMBER)
    if upright:
        px = x0
        while px < x1:
            sh.rect(px, y0, min(x1, px + 9 * s), y1, shade(col, rng.uniform(0.84, 1.12)))
            px += 9 * s
    else:
        py = y0
        while py < y1:
            sh.rect(x0, py, x1, min(y1, py + 8 * s), shade(col, rng.uniform(0.84, 1.12)))
            py += 8 * s
    sh.rect(x0, y0, x1, y1, None, "cast")
    return col


def cabin(sh, x, base, w, h, s, rng, mood):
    """A hut of logs under its snow, a lamp at the door. / Une cabane de rondins sous sa neige."""
    col = planks(sh, x, base - h, x + w, base, s, rng, upright=False)
    sh.rect(x + w * 0.88, base - h, x + w, base, None, "dark", 150)
    sh.poly([(x - 14 * s, base - h + 2 * s), (x + w * 0.5, base - h - w * 0.28), (x + w + 14 * s, base - h + 2 * s)], shade(col, 0.72), "cast")
    sh.poly([(x - 16 * s, base - h + 2 * s), (x + w * 0.5, base - h - w * 0.28 - 9 * s), (x + w + 16 * s, base - h + 2 * s), (x + w + 10 * s, base - h + 6 * s),
             (x + w * 0.5, base - h - w * 0.28 + 2 * s), (x - 10 * s, base - h + 6 * s)], SNOW, "cast")
    opening(sh, x + w * 0.28, base - 26 * s, 24 * s, 30 * s, s, rng, col, dict(mood, lamps=1.0), kind="void", soot=0)
    opening(sh, x + w * 0.70, base, 26 * s, 56 * s, s, rng, col, mood, kind="void", soot=0)
    lantern(sh, x + w * 0.70 + 22 * s, base - 62 * s, s, 70)
    cx = x + w * rng.uniform(0.2, 0.4)                                                               # a stove pipe / un tuyau de poêle
    sh.rect(cx - 4 * s, base - h - w * 0.22 - 26 * s, cx + 4 * s, base - h - w * 0.12, (52, 50, 54), "cast")
    snow_on(sh, x - 6 * s, x + w + 6 * s, base + 1, s, rng, 5)
    return (cx, base - h - w * 0.22 - 30 * s)


def tower(sh, x, base, h, s, rng, mood):
    """A lookout of timber. / Un mirador de bois."""
    for dx in (-30, 30):
        sh.line([(x + dx * s, base), (x + dx * 0.7 * s, base - h)], (84, 66, 50), 5 * s, "cast")
    for k in (0.25, 0.55):
        sh.line([(x - 30 * s * (1 - k * 0.3), base - h * k), (x + 30 * s * (1 - (k + 0.28) * 0.3), base - h * (k + 0.28))], (76, 60, 46), 2.6 * s)
        sh.line([(x + 30 * s * (1 - k * 0.3), base - h * k), (x - 30 * s * (1 - (k + 0.28) * 0.3), base - h * (k + 0.28))], (76, 60, 46), 2.6 * s)
    planks(sh, x - 36 * s, base - h - 44 * s, x + 36 * s, base - h, s, rng)
    sh.rect(x - 24 * s, base - h - 36 * s, x + 24 * s, base - h - 18 * s, (255, 204, 130))
    sh.rect(x - 24 * s, base - h - 36 * s, x + 24 * s, base - h - 18 * s, None, "lamp", 190)
    sh.ellipse(x - 70 * s, base - h - 80 * s, x + 70 * s, base - h + 40 * s, None, "pool", 220)
    sh.lamps.append((x, base - h - 27 * s))
    sh.poly([(x - 46 * s, base - h - 44 * s), (x, base - h - 70 * s), (x + 46 * s, base - h - 44 * s)], (70, 56, 46), "cast")
    sh.poly([(x - 48 * s, base - h - 44 * s), (x, base - h - 78 * s), (x + 48 * s, base - h - 44 * s), (x + 40 * s, base - h - 42 * s), (x, base - h - 68 * s),
             (x - 40 * s, base - h - 42 * s)], SNOW, "cast")
    for i in range(1, int(h / (18 * s))):                                                            # a ladder / une échelle
        sh.line([(x + 34 * s, base - i * 18 * s), (x + 44 * s, base - i * 18 * s)], (70, 56, 44), 1.4 * s)
    for lx in (x + 34 * s, x + 44 * s):
        sh.line([(lx, base), (lx, base - h)], (70, 56, 44), 1.6 * s)


def gantry(sh, x, base, w, h, s, rng):
    """Scaffolding of the works, a hoist on top. / L'échafaudage du chantier, un treuil dessus."""
    n = max(2, int(w / (70 * s)))
    for i in range(n + 1):
        px = x + i * w / n
        sh.line([(px, base), (px, base - h)], (90, 70, 52), 5 * s, "cast")
    for k in (0.34, 0.68, 1.0):
        y = base - h * k
        sh.rect(x - 8 * s, y - 6 * s, x + w + 8 * s, y, (110, 86, 62), "cast")
        sh.rect(x - 8 * s, y - 6 * s, x + w + 8 * s, y - 4.4 * s, (144, 116, 84))
        snow_on(sh, x - 8 * s, x + w + 8 * s, y - 6 * s, s, rng, 4)
    for i in range(n):
        xa, xb = x + i * w / n, x + (i + 1) * w / n
        sh.line([(xa, base - h * 0.34), (xb, base)], (82, 64, 48), 2.6 * s)
        sh.line([(xb, base - h * 0.68), (xa, base - h * 0.34 - 6 * s)], (82, 64, 48), 2.6 * s)
    sh.line([(x + w * 0.3, base - h), (x + w + 70 * s, base - h - 40 * s)], (90, 70, 52), 5 * s, "cast")   # the jib / la flèche
    sh.line([(x + w * 0.3, base - h - 44 * s), (x + w + 70 * s, base - h - 40 * s)], (40, 40, 44), 1.0 * s)
    sh.line([(x + w * 0.3, base - h), (x + w * 0.3, base - h - 44 * s)], (90, 70, 52), 4 * s)
    hx = x + w + 66 * s
    sh.line([(hx, base - h - 40 * s), (hx, base - h * 0.4)], (40, 40, 44), 1.0 * s)                  # the cable and its load
    crate(sh, hx - 18 * s, base - h * 0.4 + 30 * s, 36 * s, 30 * s, s, (128, 100, 70))
    lantern(sh, x + w * 0.5, base - h * 0.68 + 14 * s, s, 90)


def footbridge(sh, x0, x1, y, s, rng):
    """A bridge of rope and boards between two rocks. / Une passerelle de corde et de planches."""
    n = 18
    pts = [(x0 + (x1 - x0) * i / n, y + 34 * s * 4 * (i / n) * (1 - i / n)) for i in range(n + 1)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        sh.poly([(ax, ay), (bx, by), (bx, by + 4 * s), (ax, ay + 4 * s)], shade(TIMBER[0], rng.uniform(0.8, 1.15)), "cast")
    sh.line([(px, py - 26 * s) for px, py in pts], (60, 52, 46), 1.4 * s)
    for i in range(0, n + 1, 2):
        sh.line([pts[i], (pts[i][0], pts[i][1] - 26 * s)], (60, 52, 46), 1.0 * s)
    for px in (x0, x1):
        sh.line([(px, y + 6 * s), (px, y - 44 * s)], (84, 66, 50), 5 * s, "cast")


def crag(sh, x, base, w, h, s, rng):
    """A rock with snow on its shoulders. / Un rocher, de la neige sur les épaules."""
    col = rng.choice(((104, 108, 116), (92, 98, 108), (116, 118, 122)))
    n = 9
    top = []
    for i in range(n + 1):
        k = i / n
        step = rng.choice((0.0, 0.0, 0.12, -0.10))                                                   # ledges, not a dome / des ressauts
        top.append((x + w * k + rng.uniform(-10, 10) * s, base - h * max(0.12, 0.25 + 0.75 * math.sin(math.pi * k) ** 1.6 + step) + rng.uniform(-8, 8) * s))
    sh.poly([(x - w * 0.12, base)] + top + [(x + w * 1.12, base)], col, "cast")
    for i in range(1, n, 2):                                                                         # faces of the rock / des pans
        ax, ay = top[i]
        sh.poly([(ax, ay), (ax + w * 0.10, ay + h * 0.2), (ax + w * 0.04, base), (ax - w * 0.08, base)], None, "dark", rng.randint(60, 120))
        sh.poly([(ax, ay), (ax - w * 0.09, ay + h * 0.16), (ax - w * 0.12, base - h * 0.1)], None, "light", rng.randint(50, 90))
    for (ax, ay), (bx, by) in zip(top, top[1:]):
        if by > ay:                                                                                  # the faces turned from the light
            sh.poly([(ax, ay), (bx, by), (bx - 6 * s, base), (ax + 16 * s, base)], None, "dark", 130)
        sh.poly([(ax, ay), (bx, by), (bx, by + rng.uniform(8, 20) * s), ((ax + bx) / 2, (ay + by) / 2 + rng.uniform(12, 30) * s), (ax, ay + rng.uniform(8, 20) * s)], SNOW)
    for _ in range(5):
        cx, cy = x + rng.uniform(0.1, 0.9) * w, base - rng.uniform(0.1, 0.5) * h
        sh.line([(cx, cy), (cx + rng.uniform(-10, 10) * s, cy + rng.uniform(14, 34) * s)], shade(col, 0.6), 1.2 * s)
    return top


def snow_mine(W, H, s, seed=146):
    """Mission 6. A mountain under the snow at the blue hour: huts, a lookout, the timber of a works, lamps.
    / Une montagne sous la neige à l'heure bleue : des cabanes, un mirador, les bois d'un chantier, des lampes."""
    mood = MOODS["neige"]
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.72)
    sky = vgrad(W, H, mood["sky"])
    sun = (int(W * mood["sun"][0]), int(H * mood["sun"][1]))
    hd_bg.add_at(sky, hd_bg.radial(int(1000 * s), mood["glare"], 2.2), *sun)
    white, grey, k = mood["clouds"]
    layers = [cloud_layer(tw, int(H * 0.5), rng, s, cover=128, white=white, grey=grey, k=k, stretch=2.8, f=0.02)]
    h = int(260 * s)
    far = mountains(tw, h, rng, s, mood, (150, 160, 178), 0.50, int(40 * s), 0.05, rough=1.0)
    snowcap = Image.new("RGBA", far["img"].size, (0, 0, 0, 0))                                       # snow on the heights / la neige des sommets
    a = far["img"].getchannel("A")
    cap = ImageChops.subtract(a, ImageChops.offset(a, 0, int(46 * s))).filter(ImageFilter.GaussianBlur(3 * s))
    snowcap.paste((222, 230, 244, 255), (0, 0), cap.point(lambda v: int(v * 0.8)))
    far["img"].alpha_composite(snowcap)
    layers.append(far)
    h = int(210 * s)
    layers.append(mountains(tw, h, rng, s, mood, (132, 142, 160), 0.30, int(132 * s), 0.10, rough=0.7))

    h = int(280 * s)                                                 # the forest / la forêt
    sh = Sheet(tw, h, s)
    base = h - 1
    sh.poly([(0, h)] + [(x, base - 30 * s + math.sin(x / (210 * s)) * 9 * s) for x in range(0, tw + 1, 12)] + [(tw, h)], SNOW)
    x = rng.uniform(10, 40) * s
    while x < tw - 30 * s:
        fir(sh, x, base - 24 * s + rng.uniform(-6, 6) * s, rng.uniform(110, 230) * s, s, rng)
        x += rng.uniform(34, 96) * s
    layers.append({"img": sh.finish(rng, mood, depth=0.34, blur=0.8, tex=0.5), "y": H - int(62 * s) - h, "f": 0.16, "stage": "far"})

    h = int(420 * s)                                                 # the works on the mountain / le chantier sur la montagne
    sh = Sheet(tw, h, s)
    base = h - 1
    fn = hd_bg.periodic(tw, rng, 4, 10 * s)
    gy = lambda x: base - 40 * s + fn(x)
    sh.poly([(0, h)] + [(x, gy(x)) for x in range(0, tw + 1, 8)] + [(tw, h)], SNOW)
    stacks, fires = [], []
    x = 30 * s
    order = ["cabin", "crag", "bridge", "gantry", "tower", "cabin", "crag", "gantry", "cabin", "tower", "crag"]
    for kind in order:
        if x > tw - 330 * s:
            break
        g = gy(x)
        if kind == "cabin":
            w = rng.uniform(150, 200) * s
            stacks.append(cabin(sh, x, g + 6 * s, w, rng.uniform(84, 104) * s, s, rng, mood))
            if rng.random() < 0.6:                                   # a fire in a drum outside / un feu dans un bidon
                dx = x + w + 34 * s
                drum(sh, dx, gy(dx) + 2 * s, s, (70, 60, 56))
                sh.ellipse(dx - 70 * s, gy(dx) - 110 * s, dx + 90 * s, gy(dx) + 40 * s, None, "pool", 230)
                fires.append((dx + 10 * s, gy(dx) - 34 * s))
                w += 70 * s
        elif kind == "crag":
            w = rng.uniform(190, 280) * s
            crag(sh, x, g + 10 * s, w, rng.uniform(90, 150) * s, s, rng)
        elif kind == "bridge":
            w = 420 * s
            a = crag(sh, x, g + 10 * s, 150 * s, 130 * s, s, rng)
            b = crag(sh, x + 290 * s, gy(x + 290 * s) + 10 * s, 150 * s, 130 * s, s, rng)
            footbridge(sh, x + 80 * s, x + 360 * s, min(a[4][1], b[5][1]) + 10 * s, s, rng)
        elif kind == "gantry":
            w = rng.uniform(190, 250) * s
            gantry(sh, x, g + 6 * s, w, rng.uniform(190, 260) * s, s, rng)
            w += 90 * s
        else:
            w = 110 * s
            tower(sh, x + 50 * s, g + 6 * s, rng.uniform(170, 220) * s, s, rng, mood)
        x += w + rng.uniform(30, 90) * s
    for _ in range(int(tw / (60 * s))):                              # drifts / des congères
        px = rng.uniform(0, tw)
        sh.ellipse(px - rng.uniform(30, 90) * s, gy(px) - 4 * s, px + rng.uniform(30, 90) * s, gy(px) + 16 * s, None, "light", 90)
        sh.ellipse(px - 40 * s, gy(px) + 10 * s, px + 70 * s, gy(px) + 26 * s, None, "dark", 60)
    layers.append({"img": sh.finish(rng, mood, depth=0.02, tex=0.5, bump_k=0.14), "y": H - h - int(30 * s), "f": 0.38, "stage": "mid",
                   "fires": some(rng, fires, FIRES), "stacks": stacks[:2], "lights": some(rng, sh.lamps, LIGHTS)})

    h = int(96 * s)                                                  # the snow in front / la neige devant
    sh = Sheet(tw, h, s)
    fn = hd_bg.periodic(tw, rng, 4, 6 * s)
    gy0 = h * 0.40
    sh.poly([(0, h)] + [(x, gy0 + fn(x)) for x in range(0, tw + 1, 8)] + [(tw, h)], SNOW)
    for band in (0.62, 0.82):                                        # tracks in the snow / des traces
        sh.rect(0, h * band, tw, h * band + 6 * s, None, "dark", 90)
    x = 60 * s
    while x < tw - 200 * s:
        g = gy0 + fn(x)
        q = rng.random()
        if q < 0.4:
            w = sandbags(sh, x, g, s, rng, cols=((140, 140, 130), (126, 126, 118), (152, 152, 142)), cap=SNOW)
            sh.rect(x, g - 30 * s, x + w, g + 8 * s, None, "cast", 180)
        elif q < 0.7:
            crate(sh, x, g + 6 * s, 40 * s, 30 * s, s, (122, 98, 72))
            snow_on(sh, x - 2 * s, x + 42 * s, g - 24 * s, s, rng, 5)
            w = 50 * s
        else:                                                        # logs / des rondins
            for j in range(3):
                for i in range(3 - j):
                    cx, cy = x + (i + j * 0.5) * 24 * s + 12 * s, g + 4 * s - j * 20 * s - 10 * s
                    sh.ellipse(cx - 11 * s, cy - 11 * s, cx + 11 * s, cy + 11 * s, shade(TIMBER[0], rng.uniform(0.8, 1.1)), "cast")
                    sh.ellipse(cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s, (150, 122, 88))
            snow_on(sh, x + 20 * s, x + 54 * s, g - 56 * s, s, rng, 4)
            w = 80 * s
        x += w + rng.uniform(160, 380) * s
    for _ in range(5):
        px = rng.uniform(0, tw)
        sh.ellipse(px - 150 * s, gy0 - 30 * s, px + 150 * s, gy0 + 50 * s, None, "pool", 200)
    sh.rect(0, h * 0.86, tw, h + 4, None, "Dark", 120)
    layers.append({"img": sh.finish(rng, mood, tex=0.4, bump_k=0.2, blur=0.5), "y": H - h, "f": 1.0, "stage": "near"})

    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": sun, "explosions": True, "snow": True, "plane": "heli", "plane_color": (50, 58, 72),
           "window": (255, 170, 80), "hooks": {"mid": [hd_stages.hook_fires]}}
    sky = mood["grade"](sky)
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- the last boss, a base under a storm / le dernier boss, une base sous l'orage


def grade_storm(rgb):
    f = lambda v: max(0, min(255, int(112 + (v - 112) * 1.24)))
    return lut(rgb, lambda v: min(255, int(f(v) * 1.0 + 2)), lambda v: int(f(v) * 0.99), lambda v: min(255, int(f(v) * 1.03 + 5)))


MOODS["orage"] = dict(sky=None, sun=(0.5, 0.2), glare=(0, 0, 0), haze=(60, 68, 80), dust=(255, 170, 90), cast=(10, 14), soft=4.0,
                      shadow=(84, 90, 112), shadow_k=0.86, soot=(30, 30, 34), sunc=(214, 228, 240), rim=(255, 140, 70), lamps=0.3,
                      wall=(0.34, 0.38, 0.44), lampc=(234, 242, 255), lampglow=(200, 222, 255), pool_r=40, pool_k=1.8,
                      clouds=None, grade=grade_storm, dim=1.0)


def storm_sky(W, H, s, rng, cx, cy):
    """Clouds turning round an eye, fires under the horizon. / Des nuages qui tournent autour d'un œil."""
    NW, NH = 1024, 256
    n = fractal(NW, NH, rng, cells=(170, 70, 28, 11), contrast=1.6)
    src = Image.new("L", (NW * 3, NH))
    for i in range(3):
        src.paste(n, (i * NW, 0))
    cell = 32

    def uv(x, y):
        dx, dy = x - cx, (y - cy) * 2.7
        r = math.hypot(dx, dy)
        return math.atan2(dy, dx) / math.tau * NW + r * 0.85, min(NH - 1.0, (r / (W * 0.8)) ** 0.7 * NH)
    mesh = []
    for gy in range(0, H, cell):
        for gx in range(0, W, cell):
            uvs = [uv(*c) for c in ((gx, gy), (gx, gy + cell), (gx + cell, gy + cell), (gx + cell, gy))]
            u0 = uvs[0][0]
            us = []
            for u, v in uvs:
                while u - u0 > NW / 2:
                    u -= NW
                while u - u0 < -NW / 2:
                    u += NW
                us.append(u)
            shift = NW - math.floor(min(us) / NW) * NW
            quad = []
            for u, (_, v) in zip(us, uvs):
                quad += [u + shift, v]
            mesh.append(((gx, gy, min(W, gx + cell), min(H, gy + cell)), quad))
    swirl = src.transform((W, H), Image.MESH, mesh, Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.4 * s))
    sky = ImageOps.colorize(swirl, (10, 16, 24), (150, 170, 172), mid=(46, 62, 76))
    hd_bg.add_at(sky, hd_bg.radial(int(520 * s), (120, 150, 140), 1.6), cx, cy)                      # the eye / l'œil
    hd_bg.add_at(sky, hd_bg.radial(int(150 * s), (150, 170, 150), 2.0), cx, cy)
    glow = vgrad(W, H, [(0.0, (0, 0, 0)), (0.42, (0, 0, 0)), (0.62, (150, 60, 16)), (0.70, (230, 110, 30)), (0.78, (120, 44, 14)), (1.0, (0, 0, 0))], 0)
    return ImageChops.add(sky, glow)


def craft(sh, x, y, w, s):
    """A flying machine of our own drawing: a lens, a dome, a ring of lights. / Un engin volant de notre dessin."""
    hgt = w * 0.16
    sh.ellipse(x - w * 0.22, y - hgt * 1.5, x + w * 0.22, y + hgt * 0.2, (70, 84, 92))                # the dome
    sh.ellipse(x - w / 2, y - hgt * 0.6, x + w / 2, y + hgt * 0.6, (52, 62, 72))                      # the hull
    sh.ellipse(x - w * 0.46, y - hgt * 0.58, x + w * 0.3, y - hgt * 0.05, (84, 98, 106))
    sh.ellipse(x - w * 0.3, y + hgt * 0.1, x + w * 0.3, y + hgt * 0.9, (30, 38, 46))                  # the belly
    n = max(5, int(w / (12 * s)))
    for i in range(n):
        lx = x - w * 0.42 + i * w * 0.84 / (n - 1)
        sh.ellipse(lx - 1.6 * s, y - 1.2 * s, lx + 1.6 * s, y + 1.8 * s, (150, 240, 255))
        sh.ellipse(lx - 4 * s, y - 4 * s, lx + 4 * s, y + 4 * s, None, "glowC", 190)
    sh.ellipse(x - w * 0.18, y + hgt * 0.3, x + w * 0.18, y + hgt * 0.9, (120, 230, 255))
    sh.ellipse(x - w * 0.26, y + hgt * 0.1, x + w * 0.26, y + hgt * 1.3, None, "glowC", 230)
    sh.ellipse(x - w * 0.6, y - hgt * 2.2, x + w * 0.6, y + hgt * 2.2, None, "pool", 150)


def hangar(sh, x, base, w, h, s, rng, mood, open_=True):
    col = (104, 110, 108)
    sh.d.chord([x * 2, (base - h) * 2, (x + w) * 2, (base + h) * 2], 180, 360, fill=col)
    sh.md["cast"].chord([x, base - h, x + w, base + h], 180, 360, fill=255)
    rx = x + 10 * s
    while rx < x + w - 6 * s:                                                                        # the ribs of the iron / les ondes de la tôle
        k = (rx - x) / w
        top = base - h * math.sin(math.acos(max(-1.0, min(1.0, 2 * k - 1))))
        sh.line([(rx, top + 2 * s), (rx, base)], shade(col, 0.8), 0.8 * s)
        rx += 9 * s
    sh.md["dark"].chord([x + w * 0.5, base - h, x + w, base + h], 180, 360, fill=120)
    sh.md["light"].chord([x + w * 0.08, base - h * 0.94, x + w * 0.5, base + h], 200, 290, fill=90)
    dw, dh = w * 0.56, h * 0.72
    dx = x + (w - dw) / 2
    sh.rect(dx - 3 * s, base - dh - 3 * s, dx + dw + 3 * s, base, None, "hole")
    sh.rect(dx, base - dh, dx + dw, base, (64, 72, 74))
    px = dx
    while px < dx + dw:
        sh.line([(px, base - dh), (px, base)], (44, 50, 52), 1.0 * s)
        px += 12 * s
    if open_:                                                                                        # the doors ajar, light inside
        gx = dx + dw * rng.uniform(0.3, 0.5)
        gw = dw * rng.uniform(0.2, 0.34)
        sh.rect(gx, base - dh, gx + gw, base, (236, 244, 255))
        sh.rect(gx, base - dh, gx + gw, base, None, "lamp", 200)
        sh.poly([(gx, base - dh), (gx + gw, base - dh), (gx + gw + 60 * s, base + 10 * s), (gx - 60 * s, base + 10 * s)], None, "pool", 240)
        sh.poly([(gx + gw * 0.2, base), (gx + gw * 0.36, base - dh * 0.5), (gx + gw * 0.7, base - dh * 0.56), (gx + gw * 0.8, base)], (30, 36, 40))   # something stands in there
        sh.lamps.append((gx + gw / 2, base - dh * 0.6))
    sh.rect(x, base - 14 * s, x + w, base + 1, None, "Dark", 120)


def mast(sh, x, base, h, s, blinks):
    for i in range(int(h / (26 * s))):                                                               # a lattice mast / un pylône en treillis
        y0, y1 = base - i * 26 * s, base - (i + 1) * 26 * s
        k0, k1 = 1 - i * 26 * s / h * 0.7, 1 - (i + 1) * 26 * s / h * 0.7
        sh.line([(x - 12 * s * k0, y0), (x + 12 * s * k1, y1)], (64, 70, 72), 1.2 * s)
        sh.line([(x + 12 * s * k0, y0), (x - 12 * s * k1, y1)], (64, 70, 72), 1.2 * s)
    sh.line([(x - 12 * s, base), (x - 3.6 * s, base - h)], (64, 70, 72), 1.6 * s, "cast")
    sh.line([(x + 12 * s, base), (x + 3.6 * s, base - h)], (64, 70, 72), 1.6 * s, "cast")
    sh.ellipse(x - 3 * s, base - h - 6 * s, x + 3 * s, base - h, (255, 70, 50))
    blinks.append((x, base - h - 3 * s))


def floodlight(sh, x, base, h, s, to=1):
    sh.line([(x, base), (x, base - h)], (70, 76, 78), 3 * s, "cast")
    sh.rect(x - 16 * s, base - h - 6 * s, x + 16 * s, base - h, (60, 66, 68), "cast")
    for dx in (-11, 0, 11):
        sh.ellipse(x + dx * s - 4.4 * s, base - h - 2 * s, x + dx * s + 4.4 * s, base - h + 7 * s, (236, 244, 255))
    sh.ellipse(x - 22 * s, base - h - 12 * s, x + 22 * s, base - h + 16 * s, None, "lamp")
    sh.poly([(x - 14 * s, base - h + 4 * s), (x + 14 * s, base - h + 4 * s), (x + to * 260 * s + 110 * s, base + 10 * s), (x + to * 260 * s - 150 * s, base + 10 * s)],
            None, "pool", 220)
    sh.lamps.append((x, base - h + 2 * s))


def truck(sh, x, base, s, rng):
    col = rng.choice(((82, 92, 72), (90, 94, 84), (74, 84, 80)))
    for cx in (x + 30 * s, x + 118 * s, x + 146 * s):
        wheel(sh, cx, base, 15 * s, s, 6)
    sh.rect(x + 4 * s, base - 44 * s, x + 172 * s, base - 24 * s, (44, 46, 46), "cast")
    sh.rect(x + 6 * s, base - 92 * s, x + 56 * s, base - 30 * s, col, "cast")                         # the cab / la cabine
    sh.rect(x + 12 * s, base - 84 * s, x + 46 * s, base - 62 * s, (30, 38, 44))
    sh.poly([(x + 62 * s, base - 44 * s), (x + 62 * s, base - 96 * s), (x + 76 * s, base - 108 * s), (x + 160 * s, base - 108 * s), (x + 172 * s, base - 96 * s),
             (x + 172 * s, base - 44 * s)], shade(col, 0.86), "cast")                                 # the cover / la bâche
    for rx in (x + 90 * s, x + 118 * s, x + 146 * s):
        sh.line([(rx, base - 106 * s), (rx, base - 46 * s)], shade(col, 0.62), 1.0 * s)
    sh.rect(x + 120 * s, base - 108 * s, x + 172 * s, base - 44 * s, None, "dark", 130)
    return 176 * s


def flak(sh, x, base, s):
    """A gun pointed at the sky behind its sandbags. / Un canon pointé vers le ciel."""
    sh.rect(x - 16 * s, base - 22 * s, x + 16 * s, base, (74, 80, 76), "cast")
    sh.poly([(x - 10 * s, base - 22 * s), (x + 10 * s, base - 22 * s), (x + 6 * s, base - 44 * s), (x - 6 * s, base - 44 * s)], (84, 90, 84), "cast")
    for dx in (-4, 4):
        sh.line([(x + dx * s, base - 40 * s), (x + dx * s + 46 * s, base - 124 * s)], (56, 60, 60), 3.4 * s, "cast")
    sh.poly([(x - 22 * s, base - 30 * s), (x - 6 * s, base - 60 * s), (x - 2 * s, base - 30 * s)], (70, 76, 72), "cast")


def storm_base(W, H, s, seed=136):
    """Mission 6. A military base under a turning sky, fires on the horizon. / Une base sous un ciel qui tourne."""
    mood = MOODS["orage"]
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    eye = (int(W * 0.5), int(H * 0.2))
    sky = storm_sky(W, H, s, rng, *eye)
    layers = []

    h = int(H * 0.62)                                                # machines in the sky / des engins dans le ciel
    sh = Sheet(tw, h, s)
    for cx, cy, cw in ((W * 0.24, H * 0.20, 150 * s), (W * 0.70, H * 0.13, 96 * s), (W * 0.86, H * 0.30, 60 * s), (W * 0.08, H * 0.34, 46 * s)):
        craft(sh, cx, cy, cw, s)
    img = sh.finish(rng, dict(mood, rim=None), depth=0.30, blur=0.8, tex=0.5)
    puff(img, [(W * 0.24, H * 0.20 + 30 * s + i * 22 * s, (14 + i * 5) * s) for i in range(7)], (130, 230, 255), 12 * s, 0.22)   # a beam under the big one
    layers.append({"img": img, "y": 0, "f": 0.03, "stage": "sky"})

    h = int(240 * s)                                                 # the base far away / la base au loin
    sh = Sheet(tw, h, s)
    blinks_far, stacks = [], []
    x = rng.uniform(10, 80) * s
    while x < tw - 220 * s:
        q = rng.random()
        if q < 0.36:
            w = rng.uniform(150, 230) * s
            hangar(sh, x, h, w, w * rng.uniform(0.34, 0.42), s * 0.6, rng, mood, open_=rng.random() < 0.4)
        elif q < 0.52:                                               # a control tower / une tour de contrôle
            w = 30 * s
            th = rng.uniform(130, 170) * s
            sh.rect(x, h - th, x + w, h, (96, 102, 100), "cast")
            sh.rect(x - 14 * s, h - th - 26 * s, x + w + 14 * s, h - th, (84, 90, 90), "cast")
            sh.rect(x - 11 * s, h - th - 21 * s, x + w + 11 * s, h - th - 8 * s, (236, 244, 255))
            sh.rect(x - 11 * s, h - th - 21 * s, x + w + 11 * s, h - th - 8 * s, None, "lamp", 170)
            sh.ellipse(x - 40 * s, h - th - 50 * s, x + w + 40 * s, h - th + 30 * s, None, "pool", 200)
            mast(sh, x + w / 2, h - th - 26 * s, 50 * s, s * 0.7, blinks_far)
            w += 30 * s
        elif q < 0.7:                                                # fuel tanks / des cuves
            w = 0
            for i in range(rng.randint(2, 3)):
                tx = x + i * 62 * s
                sh.rect(tx, h - 56 * s, tx + 54 * s, h, (104, 106, 100), "cast")
                sh.ellipse(tx, h - 64 * s, tx + 54 * s, h - 48 * s, (120, 122, 116))
                sh.rect(tx + 36 * s, h - 56 * s, tx + 54 * s, h, None, "dark", 170)
                w = (i + 1) * 62 * s
            if rng.random() < 0.5:
                stacks.append((x + 27 * s, h - 66 * s))
        elif q < 0.85:                                               # a dish / une antenne parabolique
            w = 70 * s
            sh.line([(x + 35 * s, h), (x + 35 * s, h - 70 * s)], (80, 86, 88), 5 * s, "cast")
            sh.d.chord([(x) * 2, (h - 120 * s) * 2, (x + 70 * s) * 2, (h - 50 * s) * 2], 20, 200, fill=(120, 126, 126))
            sh.md["cast"].chord([x, h - 120 * s, x + 70 * s, h - 50 * s], 20, 200, fill=255)
            sh.line([(x + 35 * s, h - 86 * s), (x + 62 * s, h - 118 * s)], (70, 76, 78), 1.6 * s)
        else:
            w = 30 * s
            mast(sh, x + 15 * s, h, rng.uniform(150, 210) * s, s, blinks_far)
        x += w + rng.uniform(40, 130) * s
    sh.rect(0, h - 10 * s, tw, h, (60, 64, 66))
    layers.append({"img": sh.finish(rng, mood, depth=0.40, blur=0.9, tex=0.7), "y": H - int(70 * s) - h, "f": 0.16, "stage": "far",
                   "blinks": blinks_far[:6], "stacks": stacks[:3]})

    h = int(380 * s)                                                 # the base, close / la base, de près
    base = h - 1
    sh = Sheet(tw, h, s)
    fires, blinks = [], []
    x = 20 * s
    order = ["hangar", "truck", "flood", "bunker", "flak", "tower", "wreck", "hangar", "truck", "flood", "flak", "bunker", "mast", "wreck"]
    rng.shuffle(order)
    for kind in order:
        if x > tw - 320 * s:
            break
        if kind == "hangar":
            w = rng.uniform(300, 380) * s
            hangar(sh, x, base, w, w * 0.36, s, rng, mood)
        elif kind == "truck":
            w = truck(sh, x, base, s, rng)
        elif kind == "flood":
            w = 40 * s
            floodlight(sh, x + 20 * s, base, rng.uniform(230, 280) * s, s, rng.choice((-1, 1)))
        elif kind == "bunker":
            w = rng.uniform(190, 250) * s
            col = rng.choice(CONCRETE)
            sh.poly([(x, base), (x + 26 * s, base - 84 * s), (x + w - 26 * s, base - 84 * s), (x + w, base)], col, "cast")
            sh.poly([(x + w * 0.7, base - 84 * s), (x + w - 26 * s, base - 84 * s), (x + w, base), (x + w * 0.78, base)], None, "dark", 140)
            sh.rect(x + w * 0.24, base - 62 * s, x + w * 0.66, base - 50 * s, (10, 12, 14))            # the slit / la meurtrière
            sh.rect(x + w * 0.22, base - 66 * s, x + w * 0.68, base - 62 * s, shade(col, 1.16), "cast")
            bw = sandbags(sh, x + 36 * s, base - 92 * s, s, rng, cols=((132, 128, 112), (120, 116, 100), (142, 138, 122)))
            sh.rect(x + 36 * s, base - 122 * s, x + 36 * s + bw, base - 84 * s, None, "cast", 180)
            for _ in range(3):
                cx = x + rng.uniform(0.2, 0.8) * w
                sh.poly([(cx, base - 84 * s), (cx + 8 * s, base - 84 * s), (cx + 4 * s, base - rng.uniform(20, 60) * s)], None, "Dark", 130)
        elif kind == "flak":
            w = 130 * s
            flak(sh, x + 50 * s, base, s)
            bw = sandbags(sh, x, base - 8 * s, s, rng, cols=((132, 128, 112), (120, 116, 100), (142, 138, 122)))
            sh.rect(x, base - 38 * s, x + bw, base, None, "cast", 180)
        elif kind == "tower":                                        # a watchtower / un mirador
            w = 90 * s
            for dx in (10, 80):
                sh.line([(x + dx * s, base), (x + (45 + (dx - 45) * 0.6) * s, base - 190 * s)], (86, 78, 66), 4 * s, "cast")
            sh.line([(x + 14 * s, base - 30 * s), (x + 68 * s, base - 150 * s)], (78, 70, 60), 2.2 * s)
            sh.line([(x + 76 * s, base - 30 * s), (x + 22 * s, base - 150 * s)], (78, 70, 60), 2.2 * s)
            sh.rect(x + 8 * s, base - 240 * s, x + 82 * s, base - 190 * s, (96, 88, 72), "cast")
            sh.rect(x + 16 * s, base - 232 * s, x + 74 * s, base - 212 * s, (20, 24, 28))
            sh.poly([(x, base - 240 * s), (x + 45 * s, base - 262 * s), (x + 90 * s, base - 240 * s)], (60, 62, 60), "cast")
            sh.ellipse(x + 60 * s, base - 228 * s, x + 74 * s, base - 214 * s, (236, 244, 255))
            sh.ellipse(x + 52 * s, base - 236 * s, x + 82 * s, base - 206 * s, None, "lamp")
            sh.poly([(x + 70 * s, base - 226 * s), (x + 70 * s, base - 216 * s), (x + 420 * s, base - 40 * s), (x + 420 * s, base - 200 * s)], None, "pool", 150)
            sh.lamps.append((x + 67 * s, base - 221 * s))
        elif kind == "mast":
            w = 40 * s
            mast(sh, x + 20 * s, base, rng.uniform(260, 320) * s, s, blinks)
        else:                                                        # what is left of a machine, burning / une carcasse qui brûle
            w = 150 * s
            sh.poly([(x, base), (x + 14 * s, base - 30 * s), (x + 44 * s, base - 50 * s), (x + 70 * s, base - 34 * s), (x + 104 * s, base - 62 * s),
                     (x + 126 * s, base - 28 * s), (x + 150 * s, base)], (36, 34, 36), "cast")
            sh.line([(x + 60 * s, base - 30 * s), (x + 30 * s, base - 84 * s)], (44, 42, 44), 3 * s)
            sh.line([(x + 96 * s, base - 50 * s), (x + 136 * s, base - 90 * s)], (44, 42, 44), 2.4 * s)
            sh.ellipse(x + 20 * s, base - 130 * s, x + 150 * s, base + 30 * s, None, "pool", 210)
            sh.ellipse(x + 50 * s, base - 70 * s, x + 110 * s, base - 20 * s, None, "lamp", 200)
            fires.append((x + 80 * s, base - 50 * s))
        x += w + rng.uniform(40, 120) * s
    px = 0.0
    while px < tw:                                                   # the fence / la clôture
        sh.line([(px, base), (px, base - 60 * s)], (70, 74, 76), 1.6 * s)
        sh.line([(px, base - 60 * s), (px + 8 * s, base - 70 * s)], (70, 74, 76), 1.4 * s)
        px += 70 * s
    for yy in (18, 34, 50, 66):
        sh.line([(0, base - yy * s), (tw, base - yy * s)], (60, 64, 66), 0.6 * s)
    layers.append({"img": sh.finish(rng, dict(mood, lampc=(255, 196, 140)) if False else mood, depth=0.03, tex=0.8), "y": H - h - int(36 * s), "f": 0.38,
                   "stage": "mid", "fires": some(rng, fires, FIRES), "blinks": blinks[:4], "lights": some(rng, sh.lamps, 8)})

    h = int(108 * s)                                                 # the tarmac / le tarmac
    sh = Sheet(tw, h, s)
    gy0 = h * 0.40
    sh.rect(0, gy0, tw, h, (92, 96, 100))
    x = 0.0
    while x < tw:                                                    # a faded line / une ligne passée
        sh.rect(x, gy0 + 40 * s, x + 80 * s, gy0 + 45 * s, (160, 146, 80))
        x += 150 * s
    for _ in range(int(tw / (130 * s))):                             # water that holds the sky / de l'eau qui garde le ciel
        px, py = rng.uniform(0, tw), rng.uniform(gy0 + 8 * s, h * 0.9)
        rw = rng.uniform(40, 120) * s
        sh.ellipse(px - rw, py - 5 * s, px + rw, py + 6 * s, (84, 96, 108))
        sh.ellipse(px - rw * 0.8, py - 4 * s, px + rw * 0.6, py + 4 * s, None, "Light", 190)
        sh.ellipse(px - rw, py - 30 * s, px + rw, py + 30 * s, None, "pool", 170)
    x = 60 * s
    while x < tw - 200 * s:
        gy = gy0 + 8 * s
        q = rng.random()
        if q < 0.35:
            w = sandbags(sh, x, gy, s, rng, cols=((132, 128, 112), (120, 116, 100), (142, 138, 122)))
            sh.rect(x, gy - 30 * s, x + w, gy + 8 * s, None, "cast", 200)
        elif q < 0.6:                                                # concrete blocks / des blocs de béton
            w = 0
            for i in range(rng.randint(2, 3)):
                bx = x + i * 56 * s
                sh.poly([(bx, gy + 6 * s), (bx + 8 * s, gy - 8 * s), (bx + 14 * s, gy - 30 * s), (bx + 34 * s, gy - 30 * s), (bx + 40 * s, gy - 8 * s), (bx + 48 * s, gy + 6 * s)],
                        (132, 134, 126), "cast")
                hazard(sh, bx + 14 * s, gy - 28 * s, bx + 34 * s, gy - 20 * s, s)
                w = (i + 1) * 56 * s
        else:
            w = 0
            for i in range(rng.randint(2, 3)):
                drum(sh, x + i * 24 * s, gy, s, rng.choice(((112, 70, 58), (84, 96, 76), (78, 90, 108))))
                sh.rect(x + i * 24 * s, gy - 30 * s, x + i * 24 * s + 20 * s, gy + 6 * s, None, "cast")
                w = (i + 1) * 24 * s
        x += w + rng.uniform(150, 360) * s
    sh.rect(0, gy0 - 2 * s, tw, gy0 + 5 * s, None, "Dark", 130)
    sh.rect(0, h * 0.84, tw, h + 4, None, "Dark", 180)
    layers.append({"img": sh.finish(rng, mood, tex=0.7, bump_k=0.4, blur=0.5), "y": H - h, "f": 1.0, "stage": "near"})

    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": eye, "explosions": True, "lightning": True, "searchlights": [(0.26, 1.0), (0.74, 0.8)],
           "plane": "heli", "plane_color": (40, 46, 56), "dust": mood["dust"], "window": (220, 235, 255), "blink": (255, 40, 30),
           "hooks": {"mid": [hd_stages.hook_fires], "far": [hd_stages.hook_stacks]}}
    sky = mood["grade"](sky)
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}
