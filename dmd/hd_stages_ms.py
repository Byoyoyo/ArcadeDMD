"""The places of Metal Slug 2 behind its scene, one per mission, in the real look of dmd/hd_real.py and the light of the
cinema (1.39.3): a backdrop rather dark, one marked source of light, warm points that live. Missions 1 to 3 are here,
missions 4 to 6 and the sky of the last boss in dmd/hd_stages_ms2.py.

1 a street of the desert at nightfall, 2 inside a tomb lit by fire, 3 a military train in wooded country at the golden
hour (a halt, a bridge of timber over a river, a depot of brick), 4 a street of shops at nightfall, 5 tunnels under the
ground, 6 a mountain under the snow at the blue hour. A storm turning round an eye comes with the boss of the last mission
("boss_stages" in the game's "hd" block).

The six Metal Slug used to share one round of backdrops whatever the mission. A game takes these places through "stages"
in its "hd" block (games/mslug2.json), the others keep the round of dmd/hd_stages.py. Every picture is our own drawing.
None comes from a game.

/ Les lieux de Metal Slug 2 derrière sa scène, un par mission, dans le rendu réaliste de dmd/hd_real.py et en lumière de
cinéma : un fond plutôt sombre, une source de lumière marquée, des points chauds qui vivent. Les missions 1 à 3 sont
ici, les missions 4 à 6 et le ciel du dernier boss dans dmd/hd_stages_ms2.py. Chaque image est notre dessin.
"""

import math
import random

from . import hd_bg
from .hd_bg import vgrad
from .hd_real import (BRICK, FIRES, IRON, LIGHTS, MOODS, PAINT, PLASTER, WOOD, Sheet, balcony, bricks, cloud_layer,
                      crate, dome, door, drum, grade_cine, lantern, mix, mountains, opening, pole, puff, rivets,
                      sandbags, settled, shade, some, stall, wheel, wires)


# ---------------------------------------------------------------------------- mission 1, a street of the desert / une rue du désert


def house(sh, x, base, w, h, s, rng, mood, detail=True, shadow=0.0):
    """A house of plaster seen from the street. / Une maison enduite vue de la rue."""
    wall = rng.choice(PLASTER)
    top = base - h
    side = min(30 * s, w * rng.uniform(0.07, 0.12))
    uw = w - side
    n = max(2, int(w / (40 * s)))                                                                  # a roof line that is not ruled
    roof = [(x + i * w / n, top + rng.uniform(-2.2, 2.2) * s) for i in range(n + 1)]
    bite = rng.random() < 0.24                                                                     # a corner shot away / un angle emporté
    if bite:
        k = rng.randint(1, max(1, n // 3))
        for i in range(k + 1):
            roof[i] = (roof[i][0], top + (rng.uniform(18, 60) * s) * (1 - i / (k + 0.5)) + rng.uniform(-4, 4) * s)
    sh.poly([(x, base + 1)] + roof + [(x + w, base + 1)], wall)
    trim = (228, 222, 208) if rng.random() < 0.34 else None
    if rng.random() < 0.38:                                                                        # the foot painted, faded / le bas peint, passé
        dh = rng.uniform(56, 96) * s
        dc = mix(wall, rng.choice(PAINT), rng.uniform(0.4, 0.62))
        sh.rect(x, base - dh, x + w, base + 1, dc)
        sh.rect(x, base - dh - 2 * s, x + w, base - dh, shade(dc, 0.82))
    if shadow > 0:                                                                                 # the taller neighbour on the left / le voisin plus haut
        sh.poly([(x, top - 3 * s), (x + shadow, top - 3 * s), (x + shadow + (base - top) * 0.3, base), (x, base)], None, "dark", 150)
    sh.poly([(x + uw, top - 3 * s), (x + w, top - 3 * s), (x + w, base + 1), (x + uw, base + 1)], None, "dark", 190)   # the side in the shade
    sh.poly([(x, top - 3 * s), (x + uw * 0.5, top - 3 * s), (x + uw * 0.2, base - h * 0.4), (x, base - h * 0.3)], None, "Light", 90)
    for (ax, ay), (bx, by) in zip(roof, roof[1:]):                                                 # the lip of the roof in the sun
        sh.poly([(ax, ay), (bx, by), (bx, by + 3 * s), (ax, ay + 3 * s)], shade(wall, 1.16))
        sh.poly([(ax, ay + 3 * s), (bx, by + 3 * s), (bx, by + 9 * s), (ax, ay + 9 * s)], None, "dark", 120)
    sh.rect(x, base - 26 * s, x + w, base + 1, None, "Dark", 130)                                   # the foot, dirty / le pied, sali
    vy = top + rng.uniform(22, 30) * s
    if not bite and rng.random() < 0.6:                                                            # the ends of the beams
        bx = x + rng.uniform(10, 16) * s
        while bx < x + uw - 8 * s:
            sh.ellipse(bx - 3 * s, vy - 3 * s, bx + 3 * s, vy + 3 * s, shade(WOOD, 0.9), "cast")
            sh.ellipse(bx - 2.4 * s, vy - 2.4 * s, bx + 0.6 * s, vy + 0.6 * s, None, "light", 120)
            bx += rng.uniform(20, 27) * s
    for _ in range(rng.randint(0, 2)):
        bricks(sh, x + rng.uniform(0.06, 0.6) * uw, vy + 22 * s + rng.uniform(0.0, 0.3) * h, rng.uniform(40, 86) * s, rng.uniform(24, 44) * s, s, rng)
    for _ in range(rng.randint(1, 3)):                                                             # patches of another plaster
        px, py, pw, ph = x + rng.uniform(0.05, 0.7) * uw, top + rng.uniform(0.15, 0.7) * h, rng.uniform(40, 110) * s, rng.uniform(30, 80) * s
        sh.ellipse(px, py, px + pw, py + ph, None, *rng.choice((("Light", rng.randint(50, 110)), ("Dark", rng.randint(26, 60)))))
    slots = max(1, int((uw - 16 * s) / (74 * s)))
    sw = (uw - 16 * s) / slots
    door_at = rng.randrange(slots)
    arch = rng.random() < 0.6
    for i in range(slots):
        cx = x + 8 * s + (i + 0.5) * sw
        q = rng.random()
        if i == door_at:
            door(sh, cx, base, rng.uniform(34, 44) * s, rng.uniform(72, 86) * s, s, rng, wall, mood, arch)
        elif q < 0.42 and detail:
            stall(sh, cx - sw * 0.40, base, sw * 0.80, s, rng, wall, mood)
        elif q < 0.9:
            opening(sh, cx, base - 40 * s, rng.uniform(20, 28) * s, rng.uniform(36, 44) * s, s, rng, wall, mood, arch, trim=trim)
    y, fl = base - 150 * s, 0
    while y - 44 * s > vy + 12 * s:
        for i in range(slots):
            cx = x + 8 * s + (i + 0.5) * sw + rng.uniform(-6, 6) * s
            q = rng.random()
            if q < 0.08 or (bite and cx < x + w * 0.4 and y - 60 * s < top + 70 * s):
                continue
            if q < 0.32 and fl == 0 and detail:
                balcony(sh, cx, y + 6 * s, s, rng, wall, mood)
            else:
                opening(sh, cx, y, rng.uniform(18, 24) * s, rng.uniform(32, 40) * s, s, rng, wall, mood, arch, trim=trim)
        y -= 80 * s
        fl += 1
    if fl == 0 and h > 186 * s:
        for i in range(slots * 2):
            if rng.random() < 0.75:
                opening(sh, x + 8 * s + (i + 0.5) * sw / 2 + rng.uniform(-4, 4) * s, vy + 52 * s, 14 * s, 26 * s, s, rng, wall, mood, arch, trim=trim)
    for _ in range(rng.randint(1, 3)):                                                             # cracks / fissures
        cx, cy = x + rng.uniform(0.1, 0.8) * uw, top + rng.uniform(0.15, 0.7) * h
        pts = [(cx, cy)]
        for _ in range(rng.randint(4, 8)):
            cx, cy = cx + rng.uniform(-7, 7) * s, cy + rng.uniform(5, 13) * s
            pts.append((cx, min(cy, base)))
        sh.line(pts, shade(wall, 0.56), 0.8 * s)
    for _ in range(rng.randint(0, 2)):                                                             # bullet holes / impacts
        cx, cy = x + rng.uniform(0.15, 0.7) * uw, top + rng.uniform(0.25, 0.7) * h
        for _ in range(rng.randint(5, 12)):
            px, py, rr = cx + rng.gauss(0, 16) * s, cy + rng.gauss(0, 9) * s, rng.uniform(0.9, 1.9) * s
            sh.ellipse(px - rr * 1.9, py - rr * 1.7, px + rr * 1.6, py + rr * 1.8, shade(wall, 1.12))
            sh.ellipse(px - rr, py - rr, px + rr, py + rr, (48, 40, 40))
    if bite:
        return wall
    q = rng.random()
    if q < 0.26:
        dome(sh, x + uw * rng.uniform(0.35, 0.6), top, min(uw * 0.5, rng.uniform(60, 96) * s), s, wall)
    elif q < 0.5:                                                                                  # a tank and a pipe / une citerne
        tx = x + rng.uniform(0.15, 0.6) * uw
        sh.rect(tx, top - 30 * s, tx + 26 * s, top, (126, 128, 124), "cast")
        sh.rect(tx + 17 * s, top - 30 * s, tx + 26 * s, top, None, "dark", 170)
        sh.rect(tx + 3 * s, top - 30 * s, tx + 7 * s, top, None, "light", 120)
        sh.rect(tx - 1 * s, top - 33 * s, tx + 27 * s, top - 29 * s, (150, 150, 144))
        sh.line([(tx + 34 * s, top), (tx + 34 * s, top - 22 * s)], (64, 58, 56), 1.6 * s)
    elif q < 0.72:                                                                                 # a room on the roof
        rw, rh = rng.uniform(56, 84) * s, rng.uniform(40, 54) * s
        rx = x + rng.uniform(0.1, 0.5) * uw
        w2 = rng.choice(PLASTER)
        sh.rect(rx, top - rh, rx + rw, top + 1, w2, "cast")
        sh.rect(rx + rw * 0.82, top - rh, rx + rw, top + 1, None, "dark", 150)
        sh.rect(rx, top - rh, rx + rw, top - rh + 3 * s, shade(w2, 1.14))
        opening(sh, rx + rw * 0.4, top, 15 * s, 28 * s, s, rng, w2, mood, True, "void", 0.0)
    if rng.random() < 0.3:                                                                         # washing / du linge
        x0, x1 = x + 0.1 * uw, x + 0.9 * uw
        for px in (x0, x1):
            sh.line([(px, top), (px, top - 30 * s)], (70, 62, 58), 1.4 * s)
        sh.line([(x0, top - 29 * s), ((x0 + x1) / 2, top - 24 * s), (x1, top - 29 * s)], (60, 56, 56), 0.7 * s)
        k = rng.randint(3, 6)
        for i in range(k):
            lx = x0 + (i + 0.6) * (x1 - x0) / (k + 0.4)
            col = rng.choice(((214, 210, 198), (150, 66, 58), (74, 100, 130), (176, 150, 84), (84, 116, 104), (196, 190, 176)))
            ww = rng.uniform(4.5, 7) * s
            sh.rect(lx - ww, top - 26 * s, lx + ww, top - rng.uniform(8, 13) * s, col)
            sh.rect(lx + ww * 0.3, top - 26 * s, lx + ww, top - 9 * s, None, "dark", 110)
    if rng.random() < 0.4:                                                                         # an aerial / une antenne
        ax = x + rng.uniform(0.1, 0.9) * uw
        sh.line([(ax, top), (ax, top - 46 * s)], (56, 52, 54), 0.9 * s)
        for dy in (40, 34, 28):
            sh.line([(ax - 8 * s, top - dy * s), (ax + 8 * s, top - dy * s)], (56, 52, 54), 0.7 * s)
    return wall


def palm(sh, x, base, h, s, rng):
    lean = rng.uniform(-0.14, 0.14)
    pts = [(x + lean * h * (i / 14) ** 1.7, base - h * i / 14) for i in range(15)]
    for i in range(14):
        w = (9 - i * 0.32) * s
        col = shade((122, 100, 76), rng.uniform(0.82, 1.1))
        sh.line([pts[i], pts[i + 1]], col, w, "cast")
        sh.line([(pts[i][0] - w * 0.5, pts[i][1]), (pts[i][0] + w * 0.5, pts[i][1])], shade(col, 0.6), 0.8 * s)
        sh.line([(pts[i][0] + w * 0.28, pts[i][1]), (pts[i + 1][0] + w * 0.28, pts[i + 1][1])], (60, 50, 44), w * 0.4)
    tx, ty = pts[-1]
    greens = ((74, 98, 54), (92, 110, 60), (60, 84, 50), (108, 118, 68), (80, 104, 62))
    order = list(range(15))
    rng.shuffle(order)
    for i in order:
        dead = i in (0, 14) or rng.random() < 0.1
        a = math.pi * (-0.16 + i / 14 * 1.32) + rng.uniform(-0.08, 0.08)
        L = rng.uniform(56, 88) * s * (0.8 if dead else 1.0)
        up = 0.55 + 0.5 * math.sin(a) ** 2
        droop = (0.95 if dead else 0.74 - 0.36 * math.sin(a) ** 2)
        rib = [(tx - math.cos(a) * L * k, ty - math.sin(a) * L * k * up + (k ** 2.3) * L * droop) for k in [j / 12 for j in range(13)]]
        col = (128, 108, 70) if dead else rng.choice(greens)
        sh.line(rib, shade(col, 0.8), 1.4 * s)
        for j in range(1, 13):
            px, py = rib[j]
            qx, qy = rib[j - 1]
            ux, uy = px - qx, py - qy
            n = math.hypot(ux, uy) or 1.0
            ux, uy = ux / n, uy / n
            ll = L * 0.26 * math.sin(math.pi * min(1.0, j / 12 + 0.08)) ** 0.7 + 3 * s
            for sgn in (-1, 1):
                ex = px + (ux * 0.55 - sgn * uy * 0.7) * ll
                ey = py + (uy * 0.55 + sgn * ux * 0.7) * ll + ll * 0.35
                sh.line([(px, py), (ex, ey)], shade(col, rng.uniform(0.74, 1.18) * (0.8 if sgn > 0 else 1.0)), 1.3 * s)
    sh.ellipse(tx - 8 * s, ty - 2 * s, tx + 8 * s, ty + 12 * s, (84, 70, 50))


def ground(tw, H, s, rng, mood):
    h = int(112 * s)
    sh = Sheet(tw, h, s)
    fn = hd_bg.periodic(tw, rng, 4, 5 * s)
    gy0 = h * 0.40
    sh.poly([(0, h)] + [(x, gy0 + fn(x)) for x in range(0, tw + 1, 8)] + [(tw, h)], (180, 160, 130))
    for band in (0.58, 0.80):                                                                      # the ruts / les ornières
        sh.rect(0, h * band, tw, h * band + 9 * s, None, "Dark", 90)
        sh.rect(0, h * band - 6 * s, tw, h * band - 2 * s, None, "Light", 70)
    for _ in range(int(tw / (26 * s))):                                                            # stones / des cailloux
        px, py, r = rng.uniform(0, tw), rng.uniform(gy0 + 14 * s, h), rng.uniform(1.4, 4.2) * s
        col = shade((168, 152, 130), rng.uniform(0.76, 1.12))
        sh.ellipse(px - r * 1.3, py - r * 0.8, px + r * 1.3, py + r * 0.8, col, "cast")
        sh.ellipse(px - r, py - r * 0.7, px + r * 0.2, py, None, "light", 110)
    x = 40 * s
    while x < tw - 170 * s:
        gy = gy0 + fn(x)
        q = rng.random()
        if q < 0.3:
            w = sandbags(sh, x, gy, s, rng, cols=((156, 144, 112), (142, 130, 100), (168, 156, 124)))
            sh.rect(x, gy - 30 * s, x + w, gy + 8 * s, None, "cast", 200)
            sh.rect(x, gy - 34 * s, x + w, gy - 22 * s, None, "light", 60)
        elif q < 0.52:
            k = rng.randint(1, 3)
            for i in range(k):
                col = rng.choice(((112, 70, 58), (84, 96, 76), (78, 90, 108), (120, 112, 96)))
                drum(sh, x + i * 24 * s, gy, s, col)
                sh.rect(x + i * 24 * s, gy - 30 * s, x + i * 24 * s + 20 * s, gy + 6 * s, None, "cast")
                sh.rect(x + i * 24 * s + 12 * s, gy - 30 * s, x + i * 24 * s + 20 * s, gy + 6 * s, None, "dark", 120)
            w = k * 24 * s
        elif q < 0.72:
            crate(sh, x, gy + 6 * s, 40 * s, 32 * s, s, (136, 110, 80))
            crate(sh, x + 44 * s, gy + 6 * s, 30 * s, 24 * s, s, (150, 122, 88))
            sh.rect(x, gy - 26 * s, x + 74 * s, gy + 6 * s, None, "cast", 220)
            w = 80 * s
        else:                                                                                      # rubble / des gravats
            for _ in range(rng.randint(5, 10)):
                rr, rx = rng.uniform(5, 17) * s, x + rng.uniform(0, 120) * s
                col = shade(rng.choice(PLASTER), rng.uniform(0.7, 0.95))
                pts = [(rx - rr, gy + 8 * s), (rx - rr * rng.uniform(0.4, 0.8), gy - rr * rng.uniform(0.5, 0.9)), (rx + rr * rng.uniform(0.2, 0.6), gy - rr),
                       (rx + rr, gy + 8 * s)]
                sh.poly(pts, col, "cast")
                sh.poly([pts[2], pts[3], (rx + rr * 0.2, gy + 8 * s)], None, "dark", 150)
            w = 120 * s
        x += w + rng.uniform(70, 190) * s
    if mood["lamps"] > 0.35:                                                                       # the lamps reach the ground
        for _ in range(6):
            px = rng.uniform(0, tw)
            sh.ellipse(px - 130 * s, gy0 - 30 * s, px + 130 * s, gy0 + 46 * s, None, "pool", 190)
    sh.rect(0, gy0 - 4 * s, tw, gy0 + 10 * s, None, "Dark", 120)                                    # the shade at the foot of the walls
    sh.rect(0, gy0 + 16 * s, tw, gy0 + 34 * s, None, "Light", 80)
    sh.rect(0, h * 0.86, tw, h + 4, None, "Dark", 150)
    return {"img": sh.finish(rng, mood, tex=0.8, bump_k=0.5, blur=0.5), "y": H - h, "f": 1.0, "stage": "near"}


def town(W, H, s, seed=131):
    """Mission 1. A street of a town of the desert at nightfall, its lamps and its lit windows.
    / Une rue d'une ville du désert à la tombée du jour, ses lampes et ses fenêtres allumées."""
    mood = MOODS["cine"]
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.72)
    sky = vgrad(W, H, mood["sky"])
    sun = (int(W * mood["sun"][0]), int(H * mood["sun"][1]))
    hd_bg.add_at(sky, hd_bg.radial(int(1300 * s), mood["glare"], 2.2), *sun)
    hd_bg.add_at(sky, hd_bg.radial(int(300 * s), (255, 232, 180), 3.0), *sun)
    white, grey, k = mood["clouds"]
    layers = [cloud_layer(tw, int(H * 0.52), rng, s, cover=131, white=white, grey=grey, k=min(1.0, k * 1.1), stretch=2.4, f=0.02),
              cloud_layer(tw, int(H * 0.40), rng, s, cover=150, white=white, grey=grey, k=k * 0.7, stretch=5.0, f=0.02)]
    h = int(250 * s)
    layers.append(mountains(tw, h, rng, s, mood, (176, 150, 128), 0.58, int(30 * s), 0.05, rough=0.9))
    h = int(210 * s)
    layers.append(mountains(tw, h, rng, s, mood, (170, 138, 104), 0.34, int(118 * s), 0.10, rough=0.7))

    h = int(260 * s)                                                 # the town behind / la ville derrière
    sh = Sheet(tw, h, s)
    x = 6 * s
    while x < tw - 130 * s:
        w, bh = rng.uniform(90, 170) * s, rng.uniform(90, 200) * s
        house(sh, x, h, w, bh, s * 0.6, rng, mood, detail=False)
        if rng.random() < 0.18:                                      # a tower / une tour
            tx, th = x + w + 10 * s, rng.uniform(200, 240) * s
            col = rng.choice(PLASTER)
            sh.rect(tx, h - th, tx + 22 * s, h, col)
            sh.rect(tx + 15 * s, h - th, tx + 22 * s, h, None, "dark", 160)
            sh.rect(tx - 5 * s, h - th + 30 * s, tx + 27 * s, h - th + 36 * s, shade(col, 1.08), "cast")
            dome(sh, tx + 11 * s, h - th, 26 * s, s * 0.7, col)
            x += 40 * s
        x += w + rng.uniform(-14, 30) * s
    smoke = [(rng.uniform(0.1, 0.9) * tw, h - rng.uniform(90, 150) * s) for _ in range(3)]
    layers.append({"img": sh.finish(rng, mood, depth=0.40, blur=0.9, tex=0.8), "y": H - int(66 * s) - h, "f": 0.16, "stage": "far", "stacks": smoke})

    h = int(440 * s)                                                 # the street / la rue
    base = h - 1
    sh = Sheet(tw, h, s)
    x = 10 * s
    fires, palms = [], []
    last, joined = 0.0, False
    while x < tw - 230 * s:
        w, bh = rng.uniform(200, 380) * s, rng.choice((rng.uniform(190, 250), rng.uniform(280, 390))) * s
        house(sh, x, base, w, bh, s, rng, mood, shadow=max(0.0, min(w * 0.45, (last - bh) * 0.55)) if joined else 0.0)
        last = bh
        if rng.random() < 0.2:
            fires.append((x + w * rng.uniform(0.3, 0.7), base - bh - 6 * s))
        gap = rng.choice((0, 0, rng.uniform(50, 150))) * s
        joined = gap == 0
        if gap > 40 * s:
            palms.append((x + w + gap * 0.5, rng.uniform(250, 340) * s))
        x += w + gap - (4 * s if gap == 0 else 0)
    for px, ph in palms:
        palm(sh, px, base, ph, s, rng)
    ps = [tw * (i + 0.3) / 4 + rng.uniform(-60, 60) * s for i in range(4)]
    for px in ps:
        pole(sh, px, base, 330 * s, s)
    wires(sh, ps, base, 330 * s, s, tw)
    layers.append({"img": sh.finish(rng, mood, depth=0.03, foot=0.25), "y": H - h - int(36 * s), "f": 0.38,
                   "stage": "mid", "fires": some(rng, fires, FIRES), "lights": some(rng, sh.lamps, LIGHTS)})
    layers.append(ground(tw, H, s, rng, mood))

    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": sun, "explosions": True, "plane": "bomber", "plane_color": (60, 66, 74),
           "dust": mood["dust"], "window": (255, 170, 80), "hooks": {"mid": [hd_stages.hook_fires], "far": [hd_stages.hook_stacks]}}
    sky = mood["grade"](sky)
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- mission 2, inside a tomb / dans un tombeau


STONE = ((188, 126, 72), (172, 110, 62), (200, 140, 84), (162, 102, 60), (180, 120, 76))


FADED = ((70, 112, 110), (160, 70, 50), (204, 164, 84), (214, 196, 160))


def blocks(sh, x0, y0, x1, y1, s, rng, bw=92, bh=46, tone=1.0):
    """Courses of cut stone. / Des assises de pierre taillée."""
    y, j = y0, 0
    while y < y1:
        yb = min(y1, y + bh * s)
        x = x0 - (j % 2) * bw * 0.5 * s
        while x < x1:
            w = bw * s * rng.uniform(0.78, 1.26)
            xa, xb = max(x0, x), min(x1, x + w)
            if xb > xa:
                col = shade(rng.choice(STONE), rng.uniform(0.9, 1.08) * tone)
                sh.rect(xa, y, xb, yb, col)
                sh.rect(xa, y, xb, y + 1.3 * s, shade(col, 1.16))
                sh.rect(xb - 1.5 * s, y, xb, yb, shade(col, 0.58))
                sh.rect(xa, yb - 1.5 * s, xb, yb, shade(col, 0.52))
                if rng.random() < 0.12:                                     # a chipped corner / un coin éclaté
                    sh.poly([(xa, y), (xa + 12 * s, y), (xa, y + 9 * s)], shade(col, 0.5))
            x += w
        y, j = yb, j + 1


def sign(sh, x, y, r, s, rng, stone):
    """A carved sign that belongs to no writing: a hollow in the shade, its lower lip in the light.
    / Un signe gravé qui n'est d'aucune écriture : un creux à l'ombre, sa lèvre basse dans la lumière."""
    dk, lt = shade(stone, 0.44), shade(stone, 1.22)
    k = rng.randint(0, 6)
    for o, c in ((1.2 * s, lt), (0.0, dk)):
        if k == 0:
            sh.rect(x - r * 0.22 + o, y - r + o, x + r * 0.22 + o, y + r + o, c)
        elif k == 1:
            sh.ellipse(x - r * 0.7 + o, y - r * 0.7 + o, x + r * 0.7 + o, y + r * 0.7 + o, c)
        elif k == 2:
            sh.poly([(x - r * 0.8 + o, y + r * 0.8 + o), (x + o, y - r + o), (x + r * 0.8 + o, y + r * 0.8 + o)], c)
        elif k == 3:
            sh.line([(x - r + o, y + o), (x - r * 0.4 + o, y - r * 0.6 + o), (x + r * 0.2 + o, y + r * 0.4 + o), (x + r * 0.9 + o, y - r * 0.5 + o)], c, 2.4 * s)
        elif k == 4:
            for dy in (-0.7, 0.0, 0.7):
                sh.rect(x - r * 0.8 + o, y + dy * r - r * 0.12 + o, x + r * 0.8 + o, y + dy * r + r * 0.12 + o, c)
        elif k == 5:
            sh.ellipse(x - r * 0.8 + o, y - r * 0.9 + o, x - r * 0.3 + o, y - r * 0.4 + o, c)
            sh.ellipse(x + r * 0.3 + o, y - r * 0.9 + o, x + r * 0.8 + o, y - r * 0.4 + o, c)
            sh.rect(x - r * 0.8 + o, y + r * 0.3 + o, x + r * 0.8 + o, y + r * 0.6 + o, c)
        else:
            sh.line([(x + math.cos(a) * r * 0.8 + o, y + math.sin(a) * r * 0.8 + o) for a in [math.pi * (1 + i / 8) for i in range(9)]], c, 2.4 * s)
            sh.rect(x - r * 0.12 + o, y + o, x + r * 0.12 + o, y + r * 0.9 + o, c)
    if k == 1:
        sh.ellipse(x - r * 0.36, y - r * 0.36, x + r * 0.36, y + r * 0.36, shade(stone, 0.92))


def carved_band(sh, x0, x1, y, hgt, s, rng, stone):
    sh.rect(x0, y, x1, y + hgt, shade(stone, 0.9))
    sh.rect(x0, y, x1, y + 1.6 * s, shade(stone, 0.55))
    sh.rect(x0, y + hgt - 1.6 * s, x1, y + hgt, shade(stone, 1.18))
    cx = x0 + hgt * 0.5
    while cx < x1 - hgt * 0.4:
        sign(sh, cx, y + hgt / 2, hgt * 0.32, s, rng, stone)
        cx += hgt * rng.uniform(0.66, 0.84)


def torch(sh, x, y, s, pool=110):
    """A torch on the wall. / Une torche au mur."""
    sh.poly([(x - 2 * s, y + 26 * s), (x + 2 * s, y + 26 * s), (x + 5 * s, y), (x - 5 * s, y)], (58, 44, 36), "cast")
    sh.rect(x - 7 * s, y - 3 * s, x + 7 * s, y + 2 * s, (84, 64, 44))
    sh.ellipse(x - 4.5 * s, y - 15 * s, x + 4.5 * s, y - 2 * s, (255, 176, 80))
    sh.ellipse(x - 2.6 * s, y - 11 * s, x + 2.6 * s, y - 3 * s, (255, 236, 170))
    sh.ellipse(x - 12 * s, y - 30 * s, x + 12 * s, y + 4 * s, None, "lamp")
    sh.ellipse(x - pool * s, y - pool * 0.9 * s, x + pool * s, y + pool * 1.5 * s, None, "pool")
    sh.ellipse(x - 9 * s, y - 70 * s, x + 11 * s, y - 20 * s, None, "Dark", 150)                   # the soot above
    sh.lamps.append((x, y - 10 * s))


def portal(sh, x, base, w, h, s, rng):
    """A doorway to a darker room. / Une porte vers une salle plus sombre."""
    stone = rng.choice(STONE)
    j = 26 * s
    sh.rect(x - w / 2 - j - 4 * s, base - h - j - 4 * s, x + w / 2 + j + 4 * s, base, None, "hole")
    sh.rect(x - w / 2 - j, base - h - j, x + w / 2 + j, base, shade(stone, 1.08), "cast")           # the jambs and the lintel
    sh.rect(x - w / 2 - j - 12 * s, base - h - j - 16 * s, x + w / 2 + j + 12 * s, base - h - j, shade(stone, 1.14), "cast")
    sh.rect(x - w / 2 - j - 12 * s, base - h - j - 16 * s, x + w / 2 + j + 12 * s, base - h - j - 12 * s, shade(stone, 1.3))
    carved_band(sh, x - w / 2 - j + 6 * s, x + w / 2 + j - 6 * s, base - h - j + 3 * s, j - 7 * s, s, rng, stone)
    sh.rect(x - w / 2, base - h, x + w / 2, base, (12, 8, 8))
    sh.rect(x - w / 2 + 14 * s, base - h + 14 * s, x + w / 2 - 14 * s, base, (26, 16, 12))           # a second frame, deeper
    sh.rect(x - w / 2 + 24 * s, base - h + 26 * s, x + w / 2 - 24 * s, base, (8, 5, 6))
    sh.rect(x + w / 2 - 5 * s, base - h, x + w / 2, base, shade(stone, 0.9))
    for i in range(3):                                                                              # the steps / les marches
        sh.rect(x - w / 2 - i * 8 * s, base - (3 - i) * 6 * s, x + w / 2 + i * 8 * s, base, shade(stone, 1.0 + i * 0.05), "cast")


def column(sh, x, base, w, top, s, rng):
    stone = rng.choice(STONE)
    sh.rect(x - w / 2, top, x + w / 2, base, stone, "cast")
    y = top + rng.uniform(40, 70) * s
    while y < base - 30 * s:                                                                        # the drums / les tambours
        sh.rect(x - w / 2, y, x + w / 2, y + 1.6 * s, shade(stone, 0.56))
        sh.rect(x - w / 2, y + 1.6 * s, x + w / 2, y + 3 * s, shade(stone, 1.14))
        y += rng.uniform(58, 76) * s
    for k, hgt in ((0.30, 30), (0.62, 24)):
        yy = top + (base - top) * k
        carved_band(sh, x - w / 2, x + w / 2, yy, hgt * s, s, rng, stone)
    yy = top + (base - top) * 0.14                                                                  # rings of faded paint
    for i, col in enumerate((FADED[1], FADED[3], FADED[0], FADED[2])):
        sh.rect(x - w / 2, yy + i * 7 * s, x + w / 2, yy + i * 7 * s + 5 * s, mix(stone, col, 0.6))
    sh.rect(x + w * 0.16, top, x + w / 2, base, None, "dark", 200)                                  # it is round
    sh.rect(x - w * 0.42, top, x - w * 0.26, base, None, "light", 120)
    sh.poly([(x - w / 2, base - 14 * s), (x + w / 2, base - 14 * s), (x + w / 2 + 12 * s, base), (x - w / 2 - 12 * s, base)], shade(stone, 0.96), "cast")
    sh.rect(x - w / 2 - 12 * s, base - 5 * s, x + w / 2 + 12 * s, base + 2, shade(stone, 1.1))


def brazier(sh, x, base, s, pool=200):
    """A bowl of fire on three legs. / Une vasque de feu sur trois pieds."""
    for dx in (-13, 0, 13):
        sh.line([(x + dx * s, base), (x + dx * 0.3 * s, base - 46 * s)], (44, 34, 30), 2.4 * s, "cast")
    sh.poly([(x - 20 * s, base - 58 * s), (x + 20 * s, base - 58 * s), (x + 11 * s, base - 44 * s), (x - 11 * s, base - 44 * s)], (70, 52, 38), "cast")
    sh.rect(x - 21 * s, base - 61 * s, x + 21 * s, base - 57 * s, (120, 86, 50))
    sh.ellipse(x - 13 * s, base - 82 * s, x + 13 * s, base - 58 * s, (255, 170, 70))
    sh.ellipse(x - 7 * s, base - 74 * s, x + 7 * s, base - 59 * s, (255, 236, 170))
    sh.ellipse(x - 26 * s, base - 112 * s, x + 26 * s, base - 50 * s, None, "lamp")
    sh.ellipse(x - pool * s, base - 62 * s - pool * s, x + pool * s, base - 62 * s + pool * 0.9 * s, None, "pool")
    return (x, base - 66 * s)


def chest(sh, x, base, s, rng):
    """A stone coffer with its lid. / Un coffre de pierre et son couvercle."""
    stone = rng.choice(STONE)
    w, h = rng.uniform(120, 160) * s, rng.uniform(44, 56) * s
    sh.rect(x, base - h, x + w, base, stone, "cast")
    sh.rect(x + w * 0.9, base - h, x + w, base, None, "dark", 170)
    carved_band(sh, x + 8 * s, x + w * 0.88, base - h + 10 * s, 20 * s, s, rng, stone)
    lean = rng.uniform(-5, 5) * s
    sh.poly([(x - 8 * s, base - h + lean), (x + w + 8 * s, base - h - lean), (x + w + 4 * s, base - h - 14 * s - lean), (x - 4 * s, base - h - 14 * s + lean)],
            shade(stone, 1.12), "cast")
    return w


def jars(sh, x, base, s, rng):
    n = rng.randint(2, 4)
    for i in range(n):
        jx, r = x + i * rng.uniform(26, 34) * s, rng.uniform(9, 14) * s
        col = rng.choice(((150, 92, 56), (132, 78, 50), (168, 112, 70)))
        sh.ellipse(jx - r, base - r * 2.6, jx + r, base, col, "cast")
        sh.rect(jx - r * 0.5, base - r * 2.6 - 6 * s, jx + r * 0.5, base - r * 2.3, col)
        sh.ellipse(jx + r * 0.1, base - r * 2.5, jx + r, base - r * 0.1, None, "dark", 170)
        sh.ellipse(jx - r * 0.7, base - r * 2.1, jx - r * 0.2, base - r * 1.2, None, "light", 150)
    return n * 32 * s


def scaffold(sh, x, base, s, rng):
    """The gear of those who dig here: poles, planks, a lamp. / Le matériel de ceux qui fouillent."""
    w, h = rng.uniform(110, 150) * s, rng.uniform(150, 210) * s
    for px in (x, x + w):
        sh.line([(px, base), (px, base - h)], (104, 80, 56), 4 * s, "cast")
    for k in (0.42, 0.86):
        sh.rect(x - 8 * s, base - h * k - 5 * s, x + w + 8 * s, base - h * k, (126, 98, 66), "cast")
        sh.rect(x - 8 * s, base - h * k - 5 * s, x + w + 8 * s, base - h * k - 3.6 * s, (158, 126, 88))
    sh.line([(x, base - h * 0.42), (x + w, base)], (92, 70, 50), 2.4 * s)
    sh.line([(x + w, base - h * 0.42), (x, base)], (92, 70, 50), 2.4 * s)
    lantern(sh, x + w * 0.5, base - h * 0.42 + 12 * s, s, 90)
    crate(sh, x + w * 0.2, base, 36 * s, 28 * s, s, (128, 100, 70))
    return w


def tomb(W, H, s, seed=132):
    """Mission 2. A hall cut in the rock, lit by fire. / Une salle taillée dans la roche, éclairée par le feu."""
    mood = MOODS["tombe"]
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    sky = vgrad(W, H, mood["sky"])
    layers = []

    h = H                                                            # the wall at the back / le mur du fond
    floor_y = H - int(86 * s)
    sh = Sheet(tw, h, s)
    blocks(sh, 0, 58 * s, tw, floor_y, s, rng)
    sh.rect(0, 0, tw, 26 * s, shade(STONE[3], 0.8))                  # the ceiling beam and its frieze
    sh.rect(0, 26 * s, tw, 58 * s, shade(STONE[2], 1.0), "cast")
    x, i = 0.0, 0
    while x < tw:
        col = mix(STONE[2], FADED[i % 4], 0.62)
        sh.rect(x + 2 * s, 30 * s, x + 30 * s, 54 * s, col)
        if i % 2:
            sh.poly([(x + 6 * s, 52 * s), (x + 16 * s, 32 * s), (x + 26 * s, 52 * s)], mix(STONE[2], FADED[(i + 2) % 4], 0.6))
        x, i = x + 34 * s, i + 1
    carved_band(sh, 0, tw, 150 * s, 40 * s, s, rng, STONE[0])
    carved_band(sh, 0, tw, 232 * s, 26 * s, s, rng, STONE[1])
    xs = []
    x = rng.uniform(120, 260) * s
    while x < tw - 220 * s:
        portal(sh, x, floor_y, rng.uniform(96, 126) * s, rng.uniform(210, 250) * s, s, rng)
        xs.append(x)
        x += rng.uniform(520, 700) * s
    for a, b in zip(xs, xs[1:] + [xs[0] + tw]):                       # torches between the doors
        n = 2 if b - a > 560 * s else 1
        for k in range(n):
            torch(sh, (a + (b - a) * (k + 1) / (n + 1)) % tw, rng.uniform(250, 280) * s, s)
    for _ in range(3):                                               # the day comes down through the roof / le jour tombe du plafond
        bx = rng.uniform(0, tw - 400 * s)
        pts = [(bx, 0), (bx + 60 * s, 0), (bx + 300 * s, floor_y), (bx + 150 * s, floor_y)]
        sh.poly(pts, None, "Light", 150)
        sh.poly(pts, None, "pool", 170)
    for _ in range(14):                                              # cracks, stains / fissures, coulures
        cx, cy = rng.uniform(0, tw), rng.uniform(70, 300) * s
        pts = [(cx, cy)]
        for _ in range(rng.randint(4, 9)):
            cx, cy = cx + rng.uniform(-9, 9) * s, cy + rng.uniform(8, 18) * s
            pts.append((cx, min(cy, floor_y)))
        sh.line(pts, (70, 44, 30), 1.0 * s)
    sh.rect(0, floor_y - 30 * s, tw, floor_y + 2, None, "Dark", 140)
    sh.rect(0, floor_y, tw, h, (120, 84, 54))                         # the floor seen far away
    layers.append({"img": sh.finish(rng, mood, depth=0.10, blur=0.6, tex=1.1, bump_k=0.34), "y": 0, "f": 0.16, "stage": "far",
                   "lights": some(rng, sh.lamps, LIGHTS)})

    h = H - int(34 * s)                                              # the columns / les colonnes
    base = h - 32 * s
    sh = Sheet(tw, h, s)
    fires = []
    x = rng.uniform(60, 160) * s
    while x < tw - 160 * s:
        cw = rng.uniform(78, 98) * s
        column(sh, x, base, cw, -6 * s, s, rng)
        gap = rng.uniform(300, 430) * s
        q = rng.random()
        mx = x + cw / 2 + 40 * s
        if q < 0.36:
            fires.append(brazier(sh, x + gap * 0.5, base, s))
        elif q < 0.58:
            chest(sh, mx + rng.uniform(0, 40) * s, base, s, rng)
        elif q < 0.78:
            scaffold(sh, mx + rng.uniform(0, 30) * s, base, s, rng)
        else:
            jars(sh, mx + rng.uniform(10, 60) * s, base, s, rng)
        x += gap
    layers.append({"img": sh.finish(rng, dict(mood, wall=(0.44, 0.33, 0.29)), tex=1.0, bump_k=0.34), "y": 0, "f": 0.38, "stage": "mid", "fires": some(rng, fires, FIRES),
                   "lights": some(rng, sh.lamps, 4)})

    h = int(104 * s)                                                 # the floor in front / le sol devant
    sh = Sheet(tw, h, s)
    gy = h * 0.34
    sh.rect(0, gy, tw, h, (150, 106, 66))
    x = 0.0
    while x < tw:                                                    # flagstones under the sand / des dalles sous le sable
        w = rng.uniform(90, 170) * s
        sh.line([(x, gy), (x - 30 * s, h)], (96, 64, 40), 1.4 * s)
        x += w
    for yy in (gy + 22 * s, gy + 52 * s):
        sh.line([(0, yy), (tw, yy)], (100, 68, 42), 1.2 * s)
    for _ in range(int(tw / (120 * s))):                             # sand blown in / du sable entré
        px, py = rng.uniform(0, tw), rng.uniform(gy + 6 * s, h)
        sh.ellipse(px - rng.uniform(40, 110) * s, py - 6 * s, px + rng.uniform(40, 110) * s, py + 8 * s, None, "Light", 110)
    x = 60 * s
    while x < tw - 200 * s:
        q = rng.random()
        if q < 0.5:                                                  # fallen blocks / des blocs tombés
            for _ in range(rng.randint(1, 3)):
                bw_, bh_ = rng.uniform(34, 70) * s, rng.uniform(22, 40) * s
                bx, tilt = x + rng.uniform(0, 80) * s, rng.uniform(-8, 8) * s
                col = shade(rng.choice(STONE), rng.uniform(0.86, 1.04))
                sh.poly([(bx, gy + 14 * s), (bx + tilt, gy + 14 * s - bh_), (bx + bw_ + tilt, gy + 14 * s - bh_ + tilt * 0.4), (bx + bw_, gy + 14 * s)], col, "cast")
                sh.poly([(bx + bw_ * 0.7 + tilt, gy + 14 * s - bh_ + tilt * 0.3), (bx + bw_ + tilt, gy + 14 * s - bh_ + tilt * 0.4), (bx + bw_, gy + 14 * s),
                         (bx + bw_ * 0.7, gy + 14 * s)], None, "dark", 170)
            x += 150 * s
        elif q < 0.75:
            x += jars(sh, x, gy + 16 * s, s, rng)
        else:                                                        # a drum of column lying / un tambour de colonne couché
            r = rng.uniform(22, 30) * s
            col = rng.choice(STONE)
            sh.rect(x, gy + 16 * s - r * 2, x + r * 2.6, gy + 16 * s, col, "cast")
            sh.ellipse(x - r * 0.5, gy + 16 * s - r * 2, x + r * 0.5, gy + 16 * s, shade(col, 1.1))
            sh.ellipse(x + r * 2.1, gy + 16 * s - r * 2, x + r * 3.1, gy + 16 * s, shade(col, 0.7))
            sh.rect(x, gy + 16 * s - r * 0.7, x + r * 2.6, gy + 16 * s, None, "dark", 150)
            x += r * 3
        x += rng.uniform(160, 380) * s
    sh.rect(0, gy - 2 * s, tw, gy + 8 * s, None, "Dark", 150)
    sh.rect(0, h * 0.8, tw, h + 4, None, "Dark", 190)
    for _ in range(4):                                               # where a fire reaches the floor / là où un feu éclaire le sol
        px = rng.uniform(0, tw)
        sh.ellipse(px - 170 * s, gy - 30 * s, px + 170 * s, gy + 60 * s, None, "pool", 200)
    layers.append({"img": sh.finish(rng, mood, tex=0.9, bump_k=0.5, blur=0.5), "y": H - h, "f": 1.0, "stage": "near"})

    from . import hd_stages
    amb = {"stars": (), "horizon": int(H * 0.82), "sun": (W // 2, 0), "explosions": False, "dust": mood["dust"], "window": (255, 160, 70),
           "hooks": {"mid": [hd_stages.hook_fires]}}
    return {"sky": mood["grade"](sky), "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- mission 3, a train at the golden hour / un train à l'heure dorée


MOODS["dore"] = dict(sky=[(0.0, (50, 68, 112)), (0.18, (106, 108, 136)), (0.32, (212, 158, 112)), (0.44, (255, 216, 136)), (0.58, (250, 190, 110)), (1.0, (118, 82, 58))],
                     sun=(0.30, 0.42), glare=(190, 130, 50), haze=(236, 182, 122), dust=(255, 212, 140), cast=(46, 10), soft=5.0,
                     shadow=(110, 92, 120), shadow_k=0.9, soot=(56, 46, 46), sunc=(255, 216, 150), rim=(255, 204, 124), lamps=0.25,
                     wall=(0.60, 0.48, 0.44), lampc=(255, 226, 172), pool_r=34, pool_k=1.7,
                     clouds=((255, 216, 152), (140, 110, 120), 0.9), grade=grade_cine, dim=1.0)


def locomotive(sh, x, ry, s, rng):
    """A steam engine seen from the side, its nose to the right. / Une locomotive à vapeur vue de côté."""
    L = 334 * s
    body = (58, 68, 58)
    for cx in (x + 262 * s, x + 294 * s):
        wheel(sh, cx, ry, 13 * s, s, 6)
    wheel(sh, x + 58 * s, ry, 15 * s, s, 6)
    sh.rect(x + 10 * s, ry - 50 * s, x + L - 18 * s, ry - 40 * s, IRON, "cast")                    # the frame / le châssis
    for cx in (x + 142 * s, x + 196 * s):                                                          # the domes / les dômes
        sh.ellipse(cx - 15 * s, ry - 134 * s, cx + 15 * s, ry - 100 * s, body)
        sh.ellipse(cx - 11 * s, ry - 132 * s, cx - 2 * s, ry - 118 * s, None, "light", 120)
    sh.rect(x + L - 68 * s, ry - 158 * s, x + L - 50 * s, ry - 110 * s, IRON, "cast")              # the chimney / la cheminée
    sh.rect(x + L - 73 * s, ry - 164 * s, x + L - 45 * s, ry - 156 * s, (62, 58, 56), "cast")
    sh.rect(x + 96 * s, ry - 114 * s, x + L - 42 * s, ry - 50 * s, body, "cast")                    # the boiler / la chaudière
    sh.rect(x + L - 76 * s, ry - 116 * s, x + L - 40 * s, ry - 48 * s, (40, 40, 42))
    sh.ellipse(x + L - 48 * s, ry - 116 * s, x + L - 32 * s, ry - 48 * s, (52, 50, 52))
    sh.rect(x + 96 * s, ry - 84 * s, x + L - 40 * s, ry - 50 * s, None, "dark", 190)                 # it is round
    sh.rect(x + 96 * s, ry - 108 * s, x + L - 44 * s, ry - 98 * s, None, "light", 150)
    bx = x + 118 * s
    while bx < x + L - 84 * s:                                                                      # brass bands / des cercles de laiton
        sh.rect(bx, ry - 114 * s, bx + 3 * s, ry - 50 * s, (150, 122, 66))
        bx += 46 * s
    sh.rect(x + 30 * s, ry - 138 * s, x + 100 * s, ry - 46 * s, (66, 74, 62), "cast")               # the cab / la cabine
    sh.rect(x + 22 * s, ry - 146 * s, x + 110 * s, ry - 137 * s, (40, 40, 40), "cast")
    sh.rect(x + 46 * s, ry - 128 * s, x + 84 * s, ry - 98 * s, (255, 196, 110))
    sh.rect(x + 46 * s, ry - 128 * s, x + 84 * s, ry - 98 * s, None, "lamp")
    sh.ellipse(x + 20 * s, ry - 160 * s, x + 110 * s, ry - 60 * s, None, "pool", 200)
    sh.line([(x + 65 * s, ry - 128 * s), (x + 65 * s, ry - 98 * s)], (40, 40, 40), 1.6 * s)
    rivets(sh, x + 34 * s, x + 98 * s, ry - 90 * s, s)
    rivets(sh, x + 34 * s, x + 98 * s, ry - 52 * s, s)
    for cx in (x + 112 * s, x + 164 * s, x + 216 * s):                                              # the driving wheels
        wheel(sh, cx, ry, 25 * s, s, 9)
    sh.rect(x + L - 112 * s, ry - 58 * s, x + L - 70 * s, ry - 28 * s, (52, 52, 54), "cast")        # the cylinder
    sh.line([(x + 112 * s, ry - 16 * s), (x + 216 * s, ry - 16 * s)], (128, 120, 112), 4.4 * s)     # the rods / les bielles
    sh.line([(x + 216 * s, ry - 16 * s), (x + L - 90 * s, ry - 42 * s)], (112, 106, 100), 3.6 * s)
    sh.poly([(x + L - 40 * s, ry - 44 * s), (x + L - 4 * s, ry - 6 * s), (x + L - 40 * s, ry - 6 * s)], (48, 46, 46), "cast")   # the cowcatcher
    for i in range(1, 5):
        sh.line([(x + L - 40 * s, ry - 44 * s + i * 8 * s), (x + L - 40 * s + i * 8 * s, ry - 6 * s)], (86, 80, 76), 1.0 * s)
    hx, hy = x + L - 38 * s, ry - 126 * s                                                           # the lamp at the front
    sh.rect(hx - 8 * s, hy - 7 * s, hx + 4 * s, hy + 7 * s, (44, 42, 42))
    sh.ellipse(hx + 1 * s, hy - 5 * s, hx + 8 * s, hy + 5 * s, (255, 238, 180))
    sh.ellipse(hx - 4 * s, hy - 12 * s, hx + 18 * s, hy + 12 * s, None, "lamp")
    sh.poly([(hx + 6 * s, hy - 8 * s), (hx + 230 * s, hy - 60 * s), (hx + 230 * s, hy + 90 * s), (hx + 6 * s, hy + 8 * s)], None, "pool", 150)
    sh.line([(x + 100 * s, ry - 122 * s), (x + L - 80 * s, ry - 122 * s)], (120, 112, 100), 1.0 * s)   # a handrail
    sh.lamps.append((hx + 4 * s, hy))
    return L, (x + L - 59 * s, ry - 166 * s)


def tender(sh, x, ry, s, rng):
    w = 150 * s
    for cx in (x + 28 * s, x + 75 * s, x + 122 * s):
        wheel(sh, cx, ry, 17 * s, s, 6)
    sh.rect(x + 8 * s, ry - 26 * s, x + w - 8 * s, ry - 16 * s, (44, 42, 42), "cast")
    sh.rect(x + 2 * s, ry - 46 * s, x + w - 2 * s, ry - 32 * s, IRON, "cast")
    sh.rect(x + 6 * s, ry - 108 * s, x + w - 6 * s, ry - 44 * s, (60, 68, 58), "cast")
    sh.poly([(x + 14 * s, ry - 108 * s), (x + 40 * s, ry - 124 * s), (x + 76 * s, ry - 118 * s), (x + 104 * s, ry - 128 * s), (x + w - 14 * s, ry - 108 * s)], (30, 28, 30))
    sh.rect(x + 6 * s, ry - 76 * s, x + w - 6 * s, ry - 44 * s, None, "dark", 120)
    sh.rect(x + 6 * s, ry - 96 * s, x + w - 6 * s, ry - 90 * s, (120, 104, 70))                      # a faded band / une bande passée
    rivets(sh, x + 10 * s, x + w - 8 * s, ry - 104 * s, s)
    rivets(sh, x + 10 * s, x + w - 8 * s, ry - 48 * s, s)
    return w


def bogies(sh, x, ry, w, s):
    for cx in (x + 30 * s, x + 64 * s, x + w - 64 * s, x + w - 30 * s):
        wheel(sh, cx, ry, 16 * s, s, 6)
    for bx in (x + 12 * s, x + w - 82 * s):                                                          # the frame of the bogie
        sh.rect(bx, ry - 24 * s, bx + 70 * s, ry - 14 * s, (44, 42, 42), "cast")
    sh.rect(x + 2 * s, ry - 42 * s, x + w - 2 * s, ry - 30 * s, IRON, "cast")
    sh.rect(x + w * 0.5 - 30 * s, ry - 30 * s, x + w * 0.5 + 30 * s, ry - 16 * s, (40, 38, 40), "cast")   # the gear under the floor
    sh.line([(x + 84 * s, ry - 30 * s), (x + w * 0.5, ry - 12 * s), (x + w - 84 * s, ry - 30 * s)], (40, 38, 40), 1.6 * s)
    sh.rect(x - 6 * s, ry - 38 * s, x + 2 * s, ry - 34 * s, (70, 66, 64))                            # the coupling / l'attelage
    sh.rect(x + w - 2 * s, ry - 38 * s, x + w + 6 * s, ry - 34 * s, (70, 66, 64))


def boxcar(sh, x, ry, s, rng):
    w = 214 * s
    bogies(sh, x, ry, w, s)
    col = rng.choice(((104, 86, 62), (88, 92, 70), (112, 78, 60), (96, 96, 84)))
    px = x + 6 * s
    while px < x + w - 6 * s:                                                                       # planks / des planches
        sh.rect(px, ry - 122 * s, min(x + w - 6 * s, px + 9 * s), ry - 42 * s, shade(col, rng.uniform(0.86, 1.1)))
        px += 9 * s
    sh.rect(x + 6 * s, ry - 122 * s, x + w - 6 * s, ry - 42 * s, None, "cast")
    sh.rect(x, ry - 130 * s, x + w, ry - 120 * s, (52, 50, 50), "cast")                               # the roof / le toit
    sh.rect(x, ry - 130 * s, x + w, ry - 127 * s, None, "light", 120)
    dx = x + w * 0.5 - 34 * s                                                                        # the sliding door / la porte
    sh.rect(dx, ry - 116 * s, dx + 68 * s, ry - 44 * s, shade(col, 0.84 if rng.random() < 0.7 else 0.3))
    sh.line([(dx, ry - 116 * s), (dx + 68 * s, ry - 44 * s)], shade(col, 0.6), 2.0 * s)
    sh.line([(dx, ry - 116 * s), (dx + 68 * s, ry - 116 * s), (dx + 68 * s, ry - 44 * s), (dx, ry - 44 * s), (dx, ry - 116 * s)], shade(col, 0.56), 1.6 * s)
    sh.rect(x + 6 * s, ry - 70 * s, x + w - 6 * s, ry - 42 * s, None, "Dark", 110)
    for _ in range(rng.randint(2, 5)):                                                               # rain has run down / des coulures
        cx = x + rng.uniform(10, 200) * s
        sh.poly([(cx, ry - 120 * s), (cx + 5 * s, ry - 120 * s), (cx + 3 * s, ry - rng.uniform(60, 100) * s)], None, "dark", 110)
    return w


def armoured(sh, x, ry, s, rng):
    w = 226 * s
    bogies(sh, x, ry, w, s)
    col = (84, 92, 84)
    sh.poly([(x + 4 * s, ry - 42 * s), (x + 22 * s, ry - 116 * s), (x + w - 22 * s, ry - 116 * s), (x + w - 4 * s, ry - 42 * s)], col, "cast")
    sh.poly([(x + w - 60 * s, ry - 116 * s), (x + w - 22 * s, ry - 116 * s), (x + w - 4 * s, ry - 42 * s), (x + w - 40 * s, ry - 42 * s)], None, "dark", 130)
    for yy in (ry - 108 * s, ry - 80 * s, ry - 50 * s):
        rivets(sh, x + 26 * s, x + w - 26 * s, yy, s, 11)
    for sx in (x + 50 * s, x + 110 * s, x + 170 * s):                                                # slits / des meurtrières
        sh.rect(sx - 12 * s, ry - 96 * s, sx + 12 * s, ry - 90 * s, (14, 14, 16))
        sh.rect(sx - 14 * s, ry - 100 * s, sx + 14 * s, ry - 97 * s, shade(col, 1.2), "cast")
    tx = x + w * 0.5                                                                                 # a turret / une tourelle
    sh.poly([(tx - 34 * s, ry - 116 * s), (tx - 26 * s, ry - 144 * s), (tx + 26 * s, ry - 144 * s), (tx + 34 * s, ry - 116 * s)], shade(col, 0.96), "cast")
    sh.line([(tx + 20 * s, ry - 132 * s), (tx + 96 * s, ry - 140 * s)], (56, 60, 58), 5 * s, "cast")
    sh.rect(tx + 92 * s, ry - 144 * s, tx + 100 * s, ry - 136 * s, (44, 46, 46))
    sh.rect(tx - 20 * s, ry - 146 * s, tx + 4 * s, ry - 143 * s, None, "light", 130)
    return w


def flatcar(sh, x, ry, s, rng, load):
    w = 220 * s
    bogies(sh, x, ry, w, s)
    sh.rect(x, ry - 48 * s, x + w, ry - 40 * s, (92, 76, 58), "cast")
    top = ry - 48 * s
    if load == "tarp":                                                                               # something under a sheet
        col = rng.choice(((92, 96, 78), (104, 98, 80), (84, 90, 84)))
        pts = [(x + 14 * s, top), (x + 24 * s, top - 38 * s), (x + 60 * s, top - 62 * s), (x + 104 * s, top - 70 * s), (x + 132 * s, top - 52 * s),
               (x + 178 * s, top - 46 * s), (x + 204 * s, top - 22 * s), (x + 208 * s, top)]
        pts = [(px, py + rng.uniform(-4, 4) * s if 0 < i < 7 else py) for i, (px, py) in enumerate(pts)]
        sh.poly(pts, col, "cast")
        for i in range(1, 7):                                                                        # folds, then ropes / des plis, des cordes
            sh.poly([pts[i], (pts[i][0] + 7 * s, pts[i][1] + 3 * s), (pts[i][0] + 12 * s, top), (pts[i][0] + 2 * s, top)], None, "dark", 100)
        for rx in (x + 50 * s, x + 110 * s, x + 170 * s):
            sh.line([(rx, top - 66 * s), (rx + 4 * s, top)], (150, 138, 110), 0.9 * s)
        sh.poly([pts[1], pts[2], pts[3], (pts[3][0] - 10 * s, pts[3][1] + 12 * s), (pts[1][0] + 8 * s, pts[1][1] + 10 * s)], None, "light", 90)
    else:                                                                                            # crates and drums
        cx = x + 12 * s
        while cx < x + w - 50 * s:
            cw, ch = rng.uniform(34, 52) * s, rng.uniform(28, 46) * s
            if rng.random() < 0.3:
                for i in range(2):
                    drum(sh, cx + i * 22 * s, top - 6 * s, s, rng.choice(((96, 64, 54), (76, 88, 70), (72, 82, 98))))
                sh.rect(cx, top - 36 * s, cx + 42 * s, top, None, "cast")
                cx += 50 * s
                continue
            crate(sh, cx, top, cw, ch, s, rng.choice(((132, 106, 76), (118, 98, 72), (146, 120, 86))))
            sh.rect(cx, top - ch, cx + cw, top, None, "cast")
            if rng.random() < 0.4:
                crate(sh, cx + 4 * s, top - ch, cw * 0.8, ch * 0.7, s, (124, 100, 72))
            cx += cw + rng.uniform(2, 10) * s
    for px in (x + 6 * s, x + w - 8 * s):                                                            # stakes / des ranchers
        sh.rect(px, top - 26 * s, px + 3 * s, top, (60, 54, 50))
    return w


def tankcar(sh, x, ry, s, rng):
    w = 206 * s
    bogies(sh, x, ry, w, s)
    col = rng.choice(((74, 70, 66), (86, 78, 64), (66, 74, 72)))
    sh.rect(x + 22 * s, ry - 110 * s, x + w - 22 * s, ry - 46 * s, col, "cast")
    sh.ellipse(x + 6 * s, ry - 110 * s, x + 38 * s, ry - 46 * s, col, "cast")
    sh.ellipse(x + w - 38 * s, ry - 110 * s, x + w - 6 * s, ry - 46 * s, shade(col, 0.8), "cast")
    sh.rect(x + 8 * s, ry - 76 * s, x + w - 8 * s, ry - 46 * s, None, "dark", 190)
    sh.rect(x + 16 * s, ry - 104 * s, x + w - 20 * s, ry - 95 * s, None, "light", 150)
    for bx in (x + 56 * s, x + w * 0.5, x + w - 56 * s):
        sh.rect(bx - 1.5 * s, ry - 110 * s, bx + 1.5 * s, ry - 46 * s, shade(col, 0.6))
    sh.rect(x + w * 0.5 - 14 * s, ry - 122 * s, x + w * 0.5 + 14 * s, ry - 108 * s, shade(col, 1.1), "cast")
    for lx in (x + w * 0.5 + 24 * s, x + w * 0.5 + 34 * s):                                          # a ladder / une échelle
        sh.line([(lx, ry - 112 * s), (lx, ry - 44 * s)], (50, 48, 48), 1.0 * s)
    for i in range(6):
        sh.line([(x + w * 0.5 + 24 * s, ry - 106 * s + i * 11 * s), (x + w * 0.5 + 34 * s, ry - 106 * s + i * 11 * s)], (50, 48, 48), 0.9 * s)
    sh.poly([(x + 60 * s, ry - 100 * s), (x + 72 * s, ry - 100 * s), (x + 68 * s, ry - 52 * s), (x + 62 * s, ry - 60 * s)], None, "Dark", 150)   # a leak
    return w


def leafy(sh, x, base, h, s, rng):
    """A tree in leaf, its crown in heaps. / Un arbre en feuilles, sa cime en masses."""
    trunk = (66, 52, 40)
    sh.line([(x, base), (x + rng.uniform(-5, 5) * s, base - h * 0.55)], trunk, 6 * s, "cast")
    for a in (-0.5, 0.5):
        sh.line([(x, base - h * 0.4), (x + a * h * 0.3, base - h * 0.7)], trunk, 3 * s)
    greens = ((50, 118, 54), (66, 136, 58), (40, 98, 50), (84, 148, 62))
    for _ in range(16):
        cx, cy = x + rng.gauss(0, h * 0.2), base - h * rng.uniform(0.5, 1.0)
        r = rng.uniform(0.10, 0.2) * h
        col = shade(rng.choice(greens), rng.uniform(0.86, 1.12))
        sh.ellipse(cx - r, cy - r * 0.8, cx + r, cy + r * 0.8, col, "cast")
        sh.ellipse(cx - r * 0.8, cy - r * 0.8, cx + r * 0.1, cy - r * 0.1, None, "light", 80)
        sh.ellipse(cx - r * 0.2, cy, cx + r, cy + r * 0.8, None, "dark", 90)


def depot(sh, x, ry, w, s, rng, mood):
    """A depot of brick behind the track, its arched windows lit. / Un dépôt de brique, ses fenêtres en arc allumées."""
    wall = rng.choice(BRICK)
    stone = (150, 140, 124)
    top = ry - 250 * s
    sh.rect(x, top, x + w, ry, wall, "cast")
    yy = top
    while yy < ry:
        sh.line([(x, yy), (x + w, yy)], shade(wall, 0.84), 0.7 * s)
        yy += 6 * s
    sh.rect(x - 4 * s, top - 8 * s, x + w + 4 * s, top, stone, "cast")
    sh.rect(x, top + 118 * s, x + w, top + 124 * s, stone, "cast")
    px = x
    while px < x + w - 4 * s:                                                                        # piers between the bays
        sh.rect(px, top, px + 12 * s, ry, shade(wall, 0.9))
        px += 104 * s
    cx = x + 58 * s
    while cx < x + w - 40 * s:
        for sill, hgt in ((top + 104 * s, 70 * s), (ry - 40 * s, 76 * s)):
            lit = dict(mood, lamps=1.0 if rng.random() < 0.55 else 0.0)
            opening(sh, cx, sill, 44 * s, hgt, s, rng, wall, lit, arch=True, kind=rng.choice(("bars", "void", "void")), soot=0.08, trim=stone)
        cx += 104 * s
    sh.rect(x, ry - 20 * s, x + w, ry, None, "Dark", 130)
    for _ in range(4):
        cx = x + rng.uniform(0.05, 0.95) * w
        sh.poly([(cx, top), (cx + 8 * s, top), (cx + 3 * s, top + rng.uniform(60, 140) * s)], None, "Dark", 110)


def trestle(sh, x0, x1, ry, base, s, rng, mood):
    """A bridge of timber over a river. / Un pont de bois sur une rivière."""
    wy = ry + 56 * s                                                                                  # the water / l'eau
    sh.rect(x0, wy, x1, base + 2, (150, 150, 140))
    sh.rect(x0, wy, x1, base + 2, None, "pool", 235)
    sh.rect(x0 - 30 * s, ry + 2 * s, x1 + 30 * s, wy, None, "pool", 150)
    for _ in range(int((x1 - x0) / (9 * s))):                                                        # the sky lies on the water
        px, py = rng.uniform(x0, x1), rng.uniform(wy + 2 * s, base)
        rw = rng.uniform(14, 70) * s
        sh.rect(px - rw, py, px + rw, py + 1.8 * s, rng.choice(((255, 214, 140), (236, 176, 108), (96, 104, 112))))
    sh.rect(x0, wy, x1, wy + 4 * s, None, "Dark", 110)
    sh.rect(x0 - 8 * s, ry + 2 * s, x1 + 8 * s, ry + 16 * s, (84, 64, 48), "cast")                    # the deck / le tablier
    sh.rect(x0 - 8 * s, ry + 2 * s, x1 + 8 * s, ry + 5 * s, (124, 98, 70))
    px = x0 + 30 * s
    while px < x1 - 20 * s:                                                                          # the bents / les palées
        for dx in (-16, 0, 16):
            sh.line([(px + dx * 0.4 * s, ry + 16 * s), (px + dx * s, base)], (72, 56, 42), 4.4 * s, "cast")
        for yy in (ry + 34 * s, ry + 52 * s):
            sh.rect(px - 20 * s, yy, px + 20 * s, yy + 4 * s, (92, 72, 52))
        sh.line([(px - 16 * s, ry + 52 * s), (px + 14 * s, ry + 18 * s)], (80, 62, 46), 2.4 * s)
        sh.poly([(px - 18 * s, wy), (px + 18 * s, wy), (px + 24 * s, base), (px - 12 * s, base)], None, "dark", 120)   # its shadow in the water
        px += 96 * s
    for bx, sg in ((x0, -1), (x1, 1)):                                                               # the banks / les berges
        sh.poly([(bx, ry + 2 * s), (bx - sg * 50 * s, wy + 10 * s), (bx - sg * 84 * s, base + 2), (bx + sg * 20 * s, base + 2), (bx + sg * 20 * s, ry + 2 * s)], (96, 104, 66))
        for _ in range(9):
            gx = bx - sg * rng.uniform(10, 70) * s
            sh.line([(gx, wy + 12 * s), (gx + rng.uniform(-5, 5) * s, wy - rng.uniform(8, 22) * s)], (120, 132, 70), 1.2 * s)


def rail(W, H, s, seed=143):
    """Mission 3. A military train in wooded country at the golden hour: a halt, a bridge over a river, a depot of
    brick. / Un train militaire en pays boisé à l'heure dorée : une halte, un pont sur une rivière, un dépôt de brique."""
    mood = MOODS["dore"]
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    sky = vgrad(W, H, mood["sky"])
    sun = (int(W * mood["sun"][0]), int(H * mood["sun"][1]))
    hd_bg.add_at(sky, hd_bg.radial(int(1400 * s), mood["glare"], 2.0), *sun)
    hd_bg.add_at(sky, hd_bg.radial(int(260 * s), (255, 240, 196), 3.0), *sun)
    white, grey, k = mood["clouds"]
    layers = [cloud_layer(tw, int(H * 0.5), rng, s, cover=134, white=white, grey=grey, k=k, stretch=3.0, f=0.02)]
    h = int(230 * s)
    layers.append(mountains(tw, h, rng, s, mood, (132, 136, 116), 0.56, int(60 * s), 0.05, rough=0.8))

    h = int(300 * s)                                                 # the woods, and a town on the far bank / les bois, une ville au loin
    sh = Sheet(tw, h, s)
    base = h - 1
    sh.poly([(0, h)] + [(x, base - 30 * s + math.sin(x / (190 * s)) * 7 * s) for x in range(0, tw + 1, 12)] + [(tw, h)], (104, 116, 70))
    town0, town1 = tw * 0.50, tw * 0.74
    x = town0
    while x < town1:                                                 # roofs and domes in the haze / des toits et des dômes
        w, bh = rng.uniform(50, 110) * s, rng.uniform(50, 130) * s
        col = rng.choice(PLASTER)
        sh.rect(x, base - 28 * s - bh, x + w, base - 20 * s, col, "cast")
        sh.rect(x + w * 0.8, base - 28 * s - bh, x + w, base - 20 * s, None, "dark", 150)
        if rng.random() < 0.3:
            sh.d.chord([(x + w * 0.2) * 2, (base - 28 * s - bh - w * 0.3) * 2, (x + w * 0.8) * 2, (base - 28 * s - bh + w * 0.3) * 2], 180, 360, fill=(120, 132, 124))
        else:
            sh.poly([(x - 4 * s, base - 28 * s - bh), (x + w * 0.5, base - 28 * s - bh - 18 * s), (x + w + 4 * s, base - 28 * s - bh)], (120, 84, 64), "cast")
        cx = x + 8 * s
        while cx < x + w * 0.76:
            if rng.random() < 0.3:
                sh.rect(cx, base - 28 * s - bh * 0.6, cx + 5 * s, base - 28 * s - bh * 0.6 + 9 * s, (255, 206, 130))
                sh.rect(cx - 2 * s, base - 30 * s - bh * 0.6, cx + 7 * s, base - 17 * s - bh * 0.6, None, "lamp", 160)
            cx += 14 * s
        x += w + rng.uniform(-6, 10) * s
    x = rng.uniform(20, 90) * s
    while x < tw - 60 * s:
        if not (town0 - 40 * s < x < town1 + 40 * s) or rng.random() < 0.2:
            leafy(sh, x, base - 24 * s, rng.uniform(150, 250) * s, s, rng)
        x += rng.uniform(70, 190) * s
    layers.append({"img": sh.finish(rng, dict(mood, wall=(0.74, 0.70, 0.58)), depth=0.18, blur=0.8, tex=0.6), "y": H - int(150 * s) - h, "f": 0.16,
                   "stage": "far"})

    h = int(400 * s)                                                 # the track, the train, what it passes / la voie, le train
    sh = Sheet(tw, h, s)
    base = h - 1
    ry = base - 112 * s
    b0, b1 = tw * 0.24, tw * 0.24 + 560 * s                          # where the bridge is / où est le pont
    d0 = tw * 0.56                                                   # where the depot is / où est le dépôt
    depot(sh, d0, ry, 540 * s, s, rng, mood)
    hx = 70 * s                                                      # the hut of the halt and its signal
    col = (132, 104, 76)
    sh.rect(hx, ry - 92 * s, hx + 150 * s, ry, col, "cast")
    i = 1
    while i * 10 * s < 150 * s:
        sh.line([(hx + i * 10 * s, ry - 92 * s), (hx + i * 10 * s, ry)], shade(col, 0.72), 1.0 * s)
        i += 1
    sh.poly([(hx - 14 * s, ry - 90 * s), (hx + 60 * s, ry - 122 * s), (hx + 164 * s, ry - 90 * s)], (84, 62, 50), "cast")
    opening(sh, hx + 40 * s, ry - 28 * s, 26 * s, 34 * s, s, rng, col, dict(mood, lamps=1.0), kind="void", soot=0)
    opening(sh, hx + 108 * s, ry, 28 * s, 62 * s, s, rng, col, mood, kind="void", soot=0)
    lantern(sh, hx + 158 * s, ry - 70 * s, s, 80)
    sx = hx + 230 * s
    sh.line([(sx, ry), (sx, ry - 190 * s)], (70, 66, 62), 3.4 * s, "cast")
    sh.poly([(sx, ry - 186 * s), (sx + 46 * s, ry - 176 * s), (sx + 46 * s, ry - 166 * s), (sx, ry - 176 * s)], (150, 60, 44), "cast")
    sh.ellipse(sx - 5 * s, ry - 164 * s, sx + 5 * s, ry - 154 * s, (255, 96, 70))
    sh.ellipse(sx - 9 * s, ry - 168 * s, sx + 9 * s, ry - 150 * s, None, "glowR")
    sh.poly([(0, ry + 2 * s), (tw, ry + 2 * s), (tw, h), (0, h)], (132, 150, 84))                    # the bank under the track, in grass
    sh.rect(0, ry + 20 * s, tw, ry + 60 * s, None, "Light", 110)
    sh.poly([(0, ry + 2 * s), (tw, ry + 2 * s), (tw, ry + 20 * s), (0, ry + 20 * s)], (112, 100, 88))
    for _ in range(int(tw / (10 * s))):
        gx, gy = rng.uniform(0, tw), rng.uniform(ry + 22 * s, base)
        if not (b0 - 90 * s < gx < b1 + 90 * s):
            cg = shade((122, 134, 72), rng.uniform(0.7, 1.15))
            sh.line([(gx, gy), (gx + rng.uniform(-5, 5) * s, gy - rng.uniform(8, 18) * s)], cg, 1.0 * s)
    trestle(sh, b0, b1, ry, base, s, rng, mood)
    x = sx + 70 * s
    stack = None
    for kind in ("box", "tarp", "armour", "tank", "box", "crates", "armour", "tender", "loco"):
        if kind == "box":
            x += boxcar(sh, x, ry, s, rng)
        elif kind == "armour":
            x += armoured(sh, x, ry, s, rng)
        elif kind == "tank":
            x += tankcar(sh, x, ry, s, rng)
        elif kind == "tender":
            x += tender(sh, x, ry, s, rng)
        elif kind == "loco":
            L, stack = locomotive(sh, x, ry, s, rng)
            x += L
        else:
            x += flatcar(sh, x, ry, s, rng, kind)
        x += 8 * s
    bx = 0.0
    while bx < tw:                                                   # the sleepers, the rail / les traverses, le rail
        sh.rect(bx, ry + 2 * s, bx + 12 * s, ry + 8 * s, (62, 50, 42))
        bx += 24 * s
    sh.rect(0, ry - 2.2 * s, tw, ry + 2 * s, (58, 54, 54))
    sh.rect(0, ry - 2.2 * s, tw, ry - 1.0 * s, (186, 170, 150))
    img = sh.finish(rng, mood, depth=0.02, tex=0.8)
    if stack:
        cx, cy = stack
        puff(img, [(cx - i * 46 * s + rng.uniform(-8, 8) * s, max(64 * s, cy - 8 * s - i * 7 * s), min(30, 10 + i * 4) * s) for i in range(13)], (255, 226, 176), 10 * s, 0.78)
    layers.append({"img": img, "y": H - h - int(30 * s), "f": 0.38, "stage": "mid", "stacks": [stack] if stack else [],
                   "lights": some(rng, sh.lamps, LIGHTS)})

    h = int(70 * s)                                                  # reeds and grass in front, over land as over water
    sh = Sheet(tw, h, s)
    fn = hd_bg.periodic(tw, rng, 5, 6 * s)
    sh.poly([(0, h)] + [(x, h * 0.55 + fn(x)) for x in range(0, tw + 1, 8)] + [(tw, h)], (70, 80, 52))
    for _ in range(int(tw / (5 * s))):
        gx = rng.uniform(0, tw)
        gy = h * 0.55 + fn(gx) + rng.uniform(0, 14) * s
        cg = shade((104, 118, 64), rng.uniform(0.6, 1.2))
        sh.line([(gx, gy), (gx + rng.uniform(-8, 8) * s, gy - rng.uniform(14, 40) * s)], cg, 1.2 * s)
        if rng.random() < 0.08:                                      # a reed mace / une massette
            sh.line([(gx, gy), (gx, gy - 44 * s)], (96, 104, 60), 1.2 * s)
            sh.rect(gx - 1.8 * s, gy - 52 * s, gx + 1.8 * s, gy - 40 * s, (84, 60, 42))
    sh.rect(0, h * 0.8, tw, h + 4, None, "Dark", 170)
    layers.append({"img": sh.finish(rng, mood, tex=0.7, bump_k=0.3, blur=0.5), "y": H - h, "f": 1.0, "stage": "near"})

    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": sun, "explosions": True, "plane": "bomber", "plane_color": (60, 60, 66),
           "dust": mood["dust"], "window": (255, 180, 90), "hooks": {"mid": [hd_stages.hook_stacks]}}
    sky = mood["grade"](sky)
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# missions 4 to 6 and the sky of the last boss, then all of them add themselves to the builders
# / les missions 4 à 6 et le ciel du dernier boss, puis tous s'ajoutent aux décors
from . import hd_stages_ms2  # noqa: E402

PLACES = {"ms_town": town, "ms_ruins": tomb, "ms_rail": rail, "ms_port": hd_stages_ms2.street, "ms_city": hd_stages_ms2.tunnels,
          "ms_base": hd_stages_ms2.snow_mine}
BOSS_PLACES = {"ms_storm": hd_stages_ms2.storm_base}     # not a mission: the sky of a boss / pas une mission : le ciel d'un boss
hd_bg.BUILDERS.update(PLACES)
hd_bg.BUILDERS.update(BOSS_PLACES)
