"""HD backdrops of the second batch of Neo Geo games done one by one (1.18): the six worlds of Pulstar (Earth front
line, underground water, fire prominence, space station, alien forest, dark nebula), a tarot night for Magical
Drop III and two football stadiums (day and night). Everything is drawn by the program, no image comes from a game.
The backdrops register in hd_bg.BUILDERS when this module is imported.

Décors HD du deuxième lot (1.18) : les six mondes de Pulstar, une nuit de tarot pour Magical Drop III et deux stades
de football (jour et nuit). Tout est dessiné par le programme, aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from . import hd_bg
from .hd_bg import Sil, add_at, mix, paint, periodic, radial, vgrad
from .hd_themes import _rgba, bubble_img, hook_bubbles, hook_comet, planet_cap, star_layer, streak_layer


def _stars_sky(sky, rng, n, W, H, y_max=1.0, lo=40, hi=150):
    d = ImageDraw.Draw(sky)
    twinkle = []
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H * y_max)
        v = rng.randint(lo, hi)
        d.point((x, y), fill=(v, v, min(255, v + 30)))
        if rng.random() < 0.06:
            twinkle.append((x, y, rng.uniform(1.5, 3.5), rng.uniform(0, math.tau)))
    return twinkle


def _band(W, h, s, rng, top, amp, n, base_y, jag=0.0):
    """Tileable band silhouette: a wavy edge (top=True: hanging from the top) with optional jagged spikes."""
    c = Sil(W, int(h), s)
    f = periodic(W, rng, n, 1.0)
    pts = []
    step = 12
    for x in range(0, int(W) + step, step):
        y = base_y + amp * f(x)
        if jag and rng.random() < 0.18:
            y += (jag if top else -jag) * rng.uniform(0.4, 1.0)
        pts.append((x, y))
    if top:
        c.poly([(0, 0)] + pts + [(W, 0)])
    else:
        c.poly([(0, h)] + pts + [(W, h)])
    return c


# ---------------------------------------------------------------------------- Pulstar
def build_pul_earth(W, H, s, seed=41):
    """Front line above the Earth: blue planet with clouds, sunrise on its edge."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (2, 4, 14)), (0.6, (6, 12, 34)), (1.0, (4, 10, 28))])
    for cx, cy, sz, col in ((0.2, 0.3, 800, (14, 30, 70)), (0.75, 0.2, 700, (30, 14, 56))):
        add_at(sky, radial(int(sz * s), col, 1.7), int(W * cx), int(H * cy))
    twinkle = _stars_sky(sky, rng, 300, W, H, 0.8)
    add_at(sky, radial(int(420 * s), (120, 70, 20), 2.2), int(W * 0.22), int(H - 120 * s))     # le soleil se lève derrière
    cap = planet_cap(W, s, 980, 112, (8, 26, 60), (70, 150, 230), (110, 190, 255))
    clouds = Image.new("L", cap.size, 0)                                                  # nuages sur la planète
    cd = ImageDraw.Draw(clouds)
    for _ in range(26):
        x, y = rng.uniform(0, W), rng.uniform(cap.height * 0.55, cap.height)
        w, h = rng.uniform(60, 180) * s, rng.uniform(5, 12) * s
        cd.ellipse([x - w, y - h, x + w, y + h], fill=rng.randint(60, 130))
    disk = Image.new("L", cap.size, 0)
    R, m = 980 * s, int(50 * s)
    ImageDraw.Draw(disk).ellipse([W / 2 - R + 6 * s, m + 6 * s, W / 2 + R - 6 * s, m + 2 * R], fill=255)
    clouds = ImageChops.multiply(clouds.filter(ImageFilter.GaussianBlur(4 * s)), disk)
    white = Image.new("RGBA", cap.size, (235, 245, 255, 0))
    white.putalpha(clouds)
    cap = Image.alpha_composite(cap, white)
    layers = [
        {"img": star_layer(W, H, s, rng, 240, (0.4, 0.9), [(140, 150, 200), (200, 210, 235)]), "y": 0, "f": 0.12, "stage": "far"},
        {"img": star_layer(W, H, s, rng, 80, (0.9, 1.7), [(190, 210, 255), (255, 255, 255)], glow=2.0), "y": 0, "f": 0.45, "stage": "mid"},
        {"img": cap, "y": H - cap.height, "f": 0.0, "stage": "mid"},
        {"img": streak_layer(W, H, s, rng, 18, (150, 190, 255)), "y": 0, "f": 1.8, "stage": "near"},
    ]
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"stars": twinkle, "hooks": {"far": [hook_comet]}}}


def build_pul_water(W, H, s, seed=42):
    """Underground water vein: cave with stalactites, rocks, light shafts and rising bubbles."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (2, 14, 22)), (0.5, (4, 40, 56)), (1.0, (2, 18, 30))])
    for _ in range(6):
        add_at(sky, radial(int(rng.uniform(300, 600) * s), (6, 50, 60), 1.8), int(rng.uniform(0, W)), int(rng.uniform(0, H)))
    d = ImageDraw.Draw(sky)
    for _ in range(5):                                                   # puits de lumière
        x = rng.uniform(0, W)
        shaft = Image.new("L", (W, H), 0)
        ImageDraw.Draw(shaft).polygon([(x - 30 * s, 0), (x + 30 * s, 0), (x + 160 * s, H), (x + 40 * s, H)], fill=26)
        sky.paste((120, 220, 230), (0, 0), shaft.filter(ImageFilter.GaussianBlur(20 * s)))
    for _ in range(40):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        d.point((x, y), fill=(60, 140, 150))
    far = _band(W, 120 * s, s, rng, True, 18 * s, 4, 70 * s)             # voûte lointaine
    far_b = _band(W, 110 * s, s, rng, False, 16 * s, 4, 50 * s)
    near = Sil(W, int(150 * s), s)                                       # stalactites
    x = -20 * s
    while x < W:
        w, h = rng.uniform(26, 70) * s, rng.uniform(40, 140) * s
        near.poly([(x, 0), (x + w, 0), (x + w * 0.55, h), (x + w * 0.45, h)])
        x += w * rng.uniform(0.7, 1.4)
    near.rect(-10, 0, W + 10, 22 * s)
    rocks = _band(W, 120 * s, s, rng, False, 28 * s, 5, 66 * s, jag=20 * s)
    layers = [
        {"img": paint(far.mask(), [(0, (8, 40, 50)), (1, (10, 52, 64))]), "y": 0, "f": 0.2, "stage": "far"},
        {"img": paint(far_b.mask(), [(0, (10, 52, 64)), (1, (6, 34, 44))]), "y": H - int(110 * s), "f": 0.2, "stage": "far"},
        {"img": paint(near.mask(), [(0, (2, 12, 18)), (1, (6, 30, 40))], rim=(60, 150, 160)), "y": 0, "f": 0.9, "stage": "near"},
        {"img": paint(rocks.mask(), [(0, (6, 30, 40)), (1, (2, 10, 16))], rim=(70, 170, 180)), "y": H - int(120 * s), "f": 0.9,
         "stage": "near"},
    ]
    images = {"bub_s": bubble_img(7, s, (160, 240, 255)), "bub_m": bubble_img(12, s, (150, 230, 240)), "bub_l": bubble_img(18, s, (170, 255, 240))}
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"images": images, "hooks": {"front": [hook_bubbles]}}}


def hook_embers(bd, screen, b, L, now, dt):
    """Embers drifting up from the fire. / Braises qui montent."""
    st = bd.amb_state.setdefault("_emb", None)
    W, H, s = bd.W, bd.H, bd.s
    if st is None:
        st = bd.amb_state["_emb"] = [[bd.rng.uniform(0, W), bd.rng.uniform(0, H), bd.rng.uniform(0.4, 1.0), bd.rng.uniform(0, 6)]
                                     for _ in range(40)]
    sp, add = bd.fx.sp, bd.pg.BLEND_RGB_ADD
    for p in st:
        p[0] -= (40 + 80 * p[2]) * s * dt + bd.speed * 0.5 * p[2] * dt
        p[1] -= (20 + 40 * p[2]) * s * dt
        if p[1] < -10 or p[0] < -10:
            p[0], p[1] = bd.rng.uniform(0, W + 200 * s), H + 10
        lv = 4 + 5 * p[2] * (0.6 + 0.4 * math.sin(now * 6 + p[3]))
        g = sp.glow(3 * s + 3 * p[2] * s, (255, 150, 60), lv, hot=0.6)
        screen.blit(g, (int(p[0] - g.get_width() / 2), int(p[1] - g.get_height() / 2)), special_flags=add)


def build_pul_fire(W, H, s, seed=43):
    """Fire prominence: a huge sun on the right with its flaming loops, red space, burning rocks, embers."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (20, 2, 4)), (0.5, (50, 8, 6)), (1.0, (24, 4, 4))])
    _stars_sky(sky, rng, 120, W, H, 1.0, 50, 110)
    cx, cy, R = W * 1.02, H * 0.5, 330 * s
    add_at(sky, radial(int(R * 4.2), (150, 50, 10), 1.4), int(cx), int(cy))
    D = int(2 * R)                                                       # le soleil : plus clair au centre, bords sombres
    g = Image.radial_gradient("L").resize((D, D), Image.BILINEAR)
    lut = [mix((255, 238, 176), (236, 104, 30), min(1.0, v / 128.0) ** 2.2) for v in range(256)]
    body = Image.merge("RGB", [g.point([c[i] for c in lut]) for i in range(3)])
    grain = Image.effect_noise((D // 3, D // 3), 60).resize((D, D), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.2 * s)).convert("RGB")
    body = Image.blend(body, ImageChops.multiply(body, grain.point(lambda v: min(255, 120 + v))), 0.35)
    bdr = ImageDraw.Draw(body)
    for _ in range(5):                                                   # taches sombres
        a, r = rng.uniform(2.0, 4.3), rng.uniform(0.35, 0.85) * R
        x, y = R + math.cos(a) * r, R + math.sin(a) * r
        w = rng.uniform(6, 16) * s
        bdr.ellipse([x - w, y - w * 0.7, x + w, y + w * 0.7], fill=(150, 50, 14))
    disk = Image.new("L", (D, D), 0)
    ImageDraw.Draw(disk).ellipse([0, 0, D - 1, D - 1], fill=255)
    sky.paste(body.filter(ImageFilter.GaussianBlur(0.8 * s)), (int(cx - R), int(cy - R)), disk.filter(ImageFilter.GaussianBlur(2 * s)))
    loops = Image.new("L", (W, H), 0)                                    # protubérances : des boucles qui sortent du bord
    ad = ImageDraw.Draw(loops)
    for _ in range(11):
        a = math.radians(rng.uniform(118, 242))
        size = rng.uniform(34, 96) * s
        r0 = R - size * 0.45
        bx, by = cx + math.cos(a) * r0, cy + math.sin(a) * r0
        ad.ellipse([bx - size, by - size, bx + size, by + size], outline=rng.randint(130, 230), width=max(2, int(rng.uniform(4, 9) * s)))
    outside = Image.new("L", (W, H), 255)
    ImageDraw.Draw(outside).ellipse([cx - R + 2 * s, cy - R + 2 * s, cx + R - 2 * s, cy + R - 2 * s], fill=0)
    loops = ImageChops.multiply(loops, outside)
    sky.paste((255, 120, 40), (0, 0), loops.filter(ImageFilter.GaussianBlur(5 * s)))
    sky.paste((255, 200, 120), (0, 0), loops.filter(ImageFilter.GaussianBlur(1.2 * s)))
    debris = Sil(W, int(110 * s), s)                                     # rochers en feu au premier plan
    x = 0.0
    while x < W:
        r = rng.uniform(10, 34) * s
        y = rng.uniform(30, 90) * s
        debris.poly([(x + r * math.cos(t) * rng.uniform(0.7, 1.1), y + r * 0.7 * math.sin(t)) for t in [i * math.tau / 7 for i in range(7)]])
        x += rng.uniform(90, 260) * s
    layers = [
        {"img": star_layer(W, H, s, rng, 90, (0.6, 1.4), [(255, 180, 140), (255, 220, 200)], glow=1.5), "y": 0, "f": 0.4, "stage": "mid"},
        {"img": paint(debris.mask(), [(0, (60, 14, 8)), (1, (24, 6, 4))], rim=(255, 140, 60)), "y": H - int(110 * s), "f": 1.2,
         "stage": "near"},
    ]
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"hooks": {"front": [hook_embers]}}}


def _wrap_rect(d, x0, y0, x1, y1, fill, W):
    for dx in (-W, 0, W):
        if x1 + dx >= 0 and x0 + dx <= W:
            d.rectangle([x0 + dx, y0, x1 + dx, y1], fill=fill)


def build_pul_station(W, H, s, seed=44):
    """Space station: hull plates above and below with their lit windows and seams, girders far behind, blinking lights."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (4, 6, 14)), (0.5, (10, 14, 30)), (1.0, (4, 6, 14))])
    for cx, col in ((0.3, (20, 30, 60)), (0.8, (30, 20, 50))):
        add_at(sky, radial(int(700 * s), col, 1.8), int(W * cx), int(H * 0.5))
    twinkle = _stars_sky(sky, rng, 220, W, H)
    far = Sil(W, int(H), s)                                              # structure lointaine
    for i in range(7):
        x = (i + 0.5) * W / 7 + rng.uniform(-40, 40) * s
        far.rect(x - 8 * s, 60 * s, x + 8 * s, H - 60 * s)
        for y in range(int(80 * s), int(H - 80 * s), int(46 * s)):
            far.rect(x - 40 * s, y, x + 40 * s, y + 5 * s)
    hh = int(110 * s)
    top, bot = Sil(W, hh, s), Sil(W, hh, s)
    blinks_t, blinks_b, lights, plates = [], [], [], []
    x = 0.0
    while x < W - 100 * s:                                                # plaques de coque, poutres, tuyaux
        w = min(rng.uniform(120, 260) * s, W - x)
        h1, h2 = rng.uniform(30, 70) * s, rng.uniform(26, 64) * s
        top.rect(x, 0, x + w - 6 * s, h1)
        top.rect(x + w * 0.2, h1, x + w * 0.3, h1 + 24 * s)
        bot.rect(x, hh - h2, x + w - 6 * s, hh)
        bot.rect(x + w * 0.6, hh - h2 - 20 * s, x + w * 0.7, hh - h2)
        blinks_t.append((x + w * 0.5, h1 - 6 * s))
        blinks_b.append((x + w * 0.4, hh - h2 + 6 * s))
        lights.append((x + w * 0.85, h1 * 0.5))
        plates.append((x, w, h1, h2))
        x += w
    top.rect(-10, 0, W + 10, 14 * s)
    bot.rect(-10, 96 * s, W + 10, hh)
    top_img = paint(top.mask(), [(0, (30, 36, 52)), (1, (60, 70, 92))], rim=(140, 160, 200))
    bot_img = paint(bot.mask(), [(0, (60, 70, 92)), (1, (24, 28, 40))], rim=(140, 160, 200))
    dt, db = ImageDraw.Draw(top_img), ImageDraw.Draw(bot_img)
    for x, w, h1, h2 in plates:                                          # coutures et hublots éclairés
        for k in range(1, int(w / (46 * s))):
            _wrap_rect(dt, x + k * 46 * s, 16 * s, x + k * 46 * s + max(1, s), h1 - 3 * s, (22, 26, 38, 255), W)
            _wrap_rect(db, x + k * 46 * s, hh - h2 + 3 * s, x + k * 46 * s + max(1, s), hh - 16 * s, (18, 20, 30, 255), W)
        if h1 > 44 * s:
            y = h1 - 18 * s
            for k in range(int((w - 30 * s) / (22 * s))):
                if rng.random() < 0.75:
                    _wrap_rect(dt, x + 14 * s + k * 22 * s, y, x + 26 * s + k * 22 * s, y + 6 * s,
                               rng.choice(((150, 210, 255, 255), (110, 170, 230, 255), (255, 210, 140, 255))), W)
        if h2 > 40 * s:
            y = hh - h2 + 10 * s
            for k in range(int((w - 30 * s) / (30 * s))):
                if rng.random() < 0.5:
                    _wrap_rect(db, x + 14 * s + k * 30 * s, y, x + 30 * s + k * 30 * s, y + 5 * s, (130, 190, 240, 255), W)
    layers = [
        {"img": paint(far.mask(), [(0, (20, 26, 44)), (1, (14, 18, 32))]), "y": 0, "f": 0.25, "stage": "far"},
        {"img": top_img, "y": 0, "f": 1.0, "stage": "near", "blinks": blinks_t, "lights": lights},
        {"img": bot_img, "y": H - hh, "f": 1.0, "stage": "near", "blinks": blinks_b},
    ]
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"stars": twinkle, "window": (120, 200, 255), "blink": (255, 60, 40)}}


def build_pul_forest(W, H, s, seed=45):
    """Dangerous forest: alien plants with glowing bulbs, a canopy with hanging tendrils, fireflies."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (8, 4, 20)), (0.55, (24, 10, 40)), (1.0, (10, 20, 18))])
    for _ in range(7):
        add_at(sky, radial(int(rng.uniform(300, 600) * s), rng.choice(((40, 10, 60), (10, 50, 40))), 1.8),
               int(rng.uniform(0, W)), int(rng.uniform(0, H)))
    _stars_sky(sky, rng, 80, W, H, 0.5)
    bulbs = []
    ph = int(240 * s)
    plants = Sil(W, ph, s)                                               # tiges à bulbes, parfois deux
    x = 0.0
    while x < W:
        h = rng.uniform(80, 220) * s
        lean = rng.uniform(-30, 30) * s
        plants.line([(x, ph), (x + lean * 0.5, ph - h * 0.5), (x + lean, ph - h)], rng.uniform(4, 9) * s)
        r = rng.uniform(9, 20) * s
        plants.ellipse(x + lean - r, ph - h - r, x + lean + r, ph - h + r)
        bulbs.append((x + lean, ph - h))
        if rng.random() < 0.35:
            bx, by = x + lean * 0.5 + rng.choice((-1, 1)) * 30 * s, ph - h * 0.55
            plants.line([(x + lean * 0.5, ph - h * 0.45), (bx, by)], 4 * s)
            plants.ellipse(bx - 8 * s, by - 8 * s, bx + 8 * s, by + 8 * s)
            bulbs.append((bx, by))
        for _ in range(2):                                               # feuilles au pied
            fx = x + rng.uniform(-30, 30) * s
            plants.ellipse(fx - 20 * s, ph - rng.uniform(10, 30) * s, fx + 20 * s, ph + 10 * s)
        x += rng.uniform(50, 120) * s
    ground = _band(W, 70 * s, s, rng, False, 12 * s, 4, 30 * s)
    ch = int(170 * s)
    canopy = Sil(W, ch, s)                                               # voûte de feuillage et vrilles qui pendent
    f = periodic(W, rng, 4, 1.0)
    canopy.poly([(0, 0)] + [(x, 34 * s + 12 * s * f(x)) for x in range(0, W + 12, 12)] + [(W, 0)])
    tips = []
    x = 0.0
    while x < W:
        base = 30 * s + 12 * s * f(x)
        h = rng.uniform(40, 125) * s
        sway = rng.uniform(-30, 30) * s
        pts = [(x + sway * (k / 6) ** 2, base + h * k / 6) for k in range(7)]
        canopy.line(pts, rng.uniform(4, 8) * s)
        for k in range(1, 6, 2):                                         # petites feuilles le long
            px, py = pts[k]
            d = 1 if k % 4 == 1 else -1
            canopy.ellipse(px + d * 2 * s - 9 * s * (d < 0), py - 3 * s, px + d * 2 * s + 9 * s * (d > 0), py + 4 * s)
        tx, ty = pts[-1]
        canopy.ellipse(tx - 6 * s, ty - 2 * s, tx + 6 * s, ty + 10 * s)
        tips.append((tx, ty + 5 * s))
        x += rng.uniform(55, 130) * s
    far = _band(W, 160 * s, s, rng, False, 30 * s, 4, 70 * s)
    layers = [
        {"img": paint(far.mask(), [(0, (30, 16, 50)), (1, (16, 10, 30))]), "y": H - int(160 * s), "f": 0.3, "stage": "far"},
        {"img": paint(plants.mask(), [(0, (20, 60, 50)), (1, (8, 24, 22))], rim=(120, 255, 180)), "y": H - ph, "f": 0.8,
         "stage": "mid", "lights": bulbs},
        {"img": paint(ground.mask(), [(0, (14, 30, 24)), (1, (4, 10, 8))]), "y": H - int(70 * s), "f": 1.1, "stage": "near"},
        {"img": paint(canopy.mask(), [(0, (4, 10, 10)), (1, (16, 44, 36))], rim=(90, 200, 140)), "y": 0, "f": 1.1, "stage": "near",
         "lights": tips},
    ]
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"fireflies": True, "window": (180, 255, 120)}}


def hook_nebula(bd, screen, b, L, now, dt):
    """Lightning inside the clouds of the nebula: a pink or violet glow lights up here and there.
    / Éclairs dans les nuages de la nébuleuse."""
    st = bd.amb_state.setdefault("_neb", {"t": now + 1.0})
    if now < st["t"]:
        return
    rng = bd.rng
    st["t"] = now + rng.uniform(0.5, 1.8)
    x, y = rng.uniform(0.04, 0.96) * bd.W, rng.uniform(0.08, 0.92) * bd.H
    col = rng.choice(((255, 110, 190), (190, 110, 255), (255, 140, 140)))
    big = rng.uniform(0.7, 1.4)
    bd.fx.glow(x, y, 40 * big, 190 * big, col, rng.uniform(0.18, 0.32), "far", 0.75, 0.0)
    if rng.random() < 0.5:                                               # deuxième lueur juste après, un peu plus loin
        bd.fx.glow(x + rng.uniform(-90, 90) * bd.s, y + rng.uniform(-40, 40) * bd.s, 20 * big, 120 * big, col, 0.2, "far", 0.6,
                   0.0, delay=0.09)


def build_pul_nebula(W, H, s, seed=46):
    """Dark nebula: red and violet clouds, lightning inside, the core glowing far away."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (6, 0, 10)), (0.5, (20, 2, 20)), (1.0, (6, 0, 8))])
    for _ in range(16):
        add_at(sky, radial(int(rng.uniform(200, 700) * s), rng.choice(((70, 10, 40), (40, 6, 60), (90, 20, 20), (20, 10, 50))), 1.6),
               int(rng.uniform(0, W)), int(rng.uniform(0, H)))
    add_at(sky, radial(int(500 * s), (160, 60, 120), 2.6), int(W * 0.7), int(H * 0.45))       # le cœur, au loin
    twinkle = _stars_sky(sky, rng, 160, W, H, 1.0, 40, 120)
    wisps = _rgba(W, H)                                                  # filaments
    wd = ImageDraw.Draw(wisps)
    for _ in range(14):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        pts = [(x, y)]
        for _ in range(6):
            x += rng.uniform(40, 120) * s
            y += rng.uniform(-30, 30) * s
            pts.append((x, y))
        wd.line(pts, fill=(220, 90, 160, 70), width=max(2, int(rng.uniform(3, 8) * s)), joint="curve")
    wisps = wisps.filter(ImageFilter.GaussianBlur(5 * s))
    layers = [
        {"img": star_layer(W, H, s, rng, 200, (0.4, 0.9), [(180, 140, 170), (220, 200, 230)]), "y": 0, "f": 0.12, "stage": "far"},
        {"img": wisps, "y": 0, "f": 0.3, "stage": "mid"},
        {"img": streak_layer(W, H, s, rng, 14, (255, 140, 200)), "y": 0, "f": 1.8, "stage": "near"},
    ]
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"stars": twinkle, "hooks": {"far": [hook_nebula]}}}


PULSTAR = {1: "pul_earth", 2: "pul_water", 3: "pul_fire", 4: "pul_station", 5: "pul_forest", 6: "pul_station", 7: "pul_nebula",
           8: "pul_nebula", 9: "pul_nebula"}


# ---------------------------------------------------------------------------- tarot (Magical Drop III)
def build_tarot(W, H, s, seed=47):
    """Tarot night: indigo sky, a large arcane circle, soft veils, twinkling stars."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (14, 6, 40)), (0.5, (36, 14, 70)), (1.0, (18, 8, 44))])
    for _ in range(8):
        add_at(sky, radial(int(rng.uniform(300, 700) * s), rng.choice(((60, 20, 80), (20, 30, 90), (80, 30, 60))), 1.8),
               int(rng.uniform(0, W)), int(rng.uniform(0, H)))
    twinkle = _stars_sky(sky, rng, 220, W, H, 1.0, 80, 200)
    ring = Image.new("L", (W, H), 0)                                     # cercle arcane, très doux
    rd = ImageDraw.Draw(ring)
    cx, cy = W / 2, H * 0.62
    for r, wdt, v in ((330, 3, 70), (300, 2, 50), (220, 2, 60), (140, 2, 45)):
        r *= s
        rd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=v, width=max(1, int(wdt * s)))
    for i in range(48):                                                  # graduations
        a = i * math.tau / 48
        r0, r1 = 300 * s, (316 if i % 4 == 0 else 308) * s
        rd.line([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * r1, cy + math.sin(a) * r1)], fill=60,
                width=max(1, int(2 * s)))
    pts = [(cx + math.cos(-math.pi / 2 + i * 4 * math.pi / 5) * 220 * s, cy + math.sin(-math.pi / 2 + i * 4 * math.pi / 5) * 220 * s)
           for i in range(6)]
    rd.line(pts, fill=55, width=max(1, int(2 * s)))
    for i in range(12):                                                  # petits symboles autour
        a = i * math.tau / 12
        x, y = cx + math.cos(a) * 260 * s, cy + math.sin(a) * 260 * s
        r = 9 * s
        if i % 3 == 0:
            rd.ellipse([x - r, y - r, x + r, y + r], outline=70, width=max(1, int(2 * s)))
        elif i % 3 == 1:
            rd.polygon([(x, y - r), (x + r, y + r), (x - r, y + r)], outline=70)
        else:
            rd.line([(x - r, y), (x + r, y)], fill=70, width=max(1, int(2 * s)))
            rd.line([(x, y - r), (x, y + r)], fill=70, width=max(1, int(2 * s)))
    sky.paste((230, 200, 255), (0, 0), ring.filter(ImageFilter.GaussianBlur(1.2 * s)))
    sky.paste((200, 150, 255), (0, 0), ring.filter(ImageFilter.GaussianBlur(8 * s)).point(lambda v: v // 2))
    veil = _rgba(W, H)                                                   # voiles de brume
    vd = ImageDraw.Draw(veil)
    for _ in range(6):
        x, y = rng.uniform(0, W), rng.uniform(H * 0.5, H)
        w, h = rng.uniform(200, 400) * s, rng.uniform(20, 40) * s
        vd.ellipse([x - w, y - h, x + w, y + h], fill=(200, 160, 255, 26))
    veil = veil.filter(ImageFilter.GaussianBlur(14 * s))
    layers = [{"img": veil, "y": 0, "f": 0.05, "stage": "far"}]
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"stars": twinkle}}


# ---------------------------------------------------------------------------- stades de football
def pitch_geom(W, H, s):
    """Pitch seen by the TV camera: top touchline, bottom touchline (below the screen) and how far in from the screen
    edges the goal lines are at the top and at the bottom (perspective). / Terrain vu par la caméra de télévision."""
    return {"top": int(H * 0.5), "bot": H + int(40 * s), "inset_top": 250 * s, "inset_bot": 40 * s}


def pitch_x(g, W, u, y):
    """x on the screen of the point at u (0 left goal line, 1 right goal line) and height y."""
    k = (y - g["top"]) / max(1, g["bot"] - g["top"])
    inset = g["inset_top"] + (g["inset_bot"] - g["inset_top"]) * k
    return inset + (W - 2 * inset) * u


def pitch_y(g, v):
    """y on the screen of the depth v (0 far touchline, 1 near touchline). / Profondeur vers y."""
    return g["top"] + (g["bot"] - g["top"]) * v


SKIN = ((236, 196, 160), (214, 160, 120), (170, 116, 80), (120, 80, 56), (250, 214, 180))


def fans_layer(W, hh, s, rng, palette, dark=0.0, ss=2):
    """A row of fans, colourful shirts, some with their arms up or a scarf. Seamless. / Une rangée de supporters."""
    img = Image.new("RGBA", (W * ss, hh * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    k = ss

    def C(c):
        return mix(c, (0, 0, 0), dark) + (255,)
    x = -6.0 * s
    while x < W:
        w = rng.uniform(16, 22) * s * hh / (60 * s)
        top = rng.uniform(0.04, 0.2) * hh
        shirt = rng.choice(palette)
        skin = rng.choice(SKIN)
        for dx in (-W, 0, W):                                            # répété sans couture
            X = x + dx
            if X + w < -2 or X > W + 2:
                continue
            if rng.random() < 0.16:                                      # bras levés, ou une écharpe
                side = rng.choice((-1, 1))
                d.line([((X + w / 2 + side * w * 0.3) * k, (top + w * 0.7) * k), ((X + w / 2 + side * w * 0.55) * k, (top - w * 0.2) * k)],
                       fill=C(skin), width=max(1, int(w * 0.18 * k)))
            d.ellipse([X * k, (top + w * 0.55) * k, (X + w) * k, (hh + w) * k], fill=C(shirt))
            d.ellipse([(X + w * 0.24) * k, top * k, (X + w * 0.76) * k, (top + w * 0.56) * k], fill=C(skin))
            if rng.random() < 0.3:
                d.rectangle([(X + w * 0.1) * k, (top + w * 0.62) * k, (X + w * 0.9) * k, (top + w * 0.78) * k],
                            fill=C(mix(shirt, (255, 255, 255), 0.6)))
        x += w * rng.uniform(0.62, 0.86)
    return img.resize((W, hh), Image.LANCZOS)


def build_stadium(night):
    def build(W, H, s, seed=None):
        rng = random.Random(48 if night else 49)
        g = pitch_geom(W, H, s)
        top = g["top"]
        if night:
            sky = vgrad(W, H, [(0.0, (2, 4, 14)), (0.3, (10, 14, 30)), (1.0, (10, 14, 30))])
            _stars_sky(sky, rng, 60, W, H, 0.12)
        else:
            sky = vgrad(W, H, [(0.0, (80, 150, 230)), (0.25, (170, 210, 245)), (1.0, (170, 210, 245))])
        d = ImageDraw.Draw(sky)
        stand_top = int(40 * s)
        boards = top - 20 * s
        for i in range(9):                                               # gradins
            y0 = stand_top + (boards - stand_top) * i / 9
            y1 = stand_top + (boards - stand_top) * (i + 1) / 9
            col = mix((70, 76, 96), (40, 44, 60), i / 9) if not night else mix((26, 30, 46), (16, 18, 30), i / 9)
            d.rectangle([0, y0, W, y1], fill=col)
            d.line([(0, y1), (W, y1)], fill=mix(col, (0, 0, 0), 0.3), width=max(1, int(2 * s)))
        d.rectangle([0, stand_top - 14 * s, W, stand_top], fill=(30, 34, 44) if not night else (14, 16, 24))   # toit
        ads = ((200, 40, 40), (30, 90, 200), (240, 200, 40), (30, 160, 80), (240, 240, 240), (120, 40, 160))
        x, i = 0.0, 0
        while x < W:                                                     # panneaux autour du terrain
            w = rng.uniform(140, 220) * s
            c = ads[i % len(ads)]
            d.rectangle([x, boards, x + w - 3 * s, top - 2 * s], fill=mix(c, (0, 0, 0), 0.25 if not night else 0.1))
            d.rectangle([x + 10 * s, boards + 5 * s, x + w - 14 * s, boards + 9 * s], fill=mix(c, (255, 255, 255), 0.5))
            x += w
            i += 1
        grass_a, grass_b = ((70, 150, 60), (60, 134, 52)) if not night else ((40, 110, 50), (34, 96, 44))
        d.rectangle([0, top, W, H], fill=mix(grass_a, (0, 0, 0), 0.12))
        d.polygon([(pitch_x(g, W, 0, top), top), (pitch_x(g, W, 1, top), top), (pitch_x(g, W, 1, g["bot"]), g["bot"]),
                   (pitch_x(g, W, 0, g["bot"]), g["bot"])], fill=grass_a)
        n = 14
        for i in range(0, n, 2):                                         # bandes de tonte, en perspective
            u0, u1 = i / n, (i + 1) / n
            d.polygon([(pitch_x(g, W, u0, top), top), (pitch_x(g, W, u1, top), top), (pitch_x(g, W, u1, g["bot"]), g["bot"]),
                       (pitch_x(g, W, u0, g["bot"]), g["bot"])], fill=grass_b)
        lw = max(2, int(4 * s))
        line = (240, 245, 240)
        d.line([(pitch_x(g, W, 0, top), top), (pitch_x(g, W, 1, top), top)], fill=line, width=lw)
        for u in (0.0, 0.5, 1.0):                                        # lignes de but et ligne médiane
            d.line([(pitch_x(g, W, u, top), top), (pitch_x(g, W, u, g["bot"]), g["bot"])], fill=line, width=lw)
        cy = pitch_y(g, 0.45)
        rx, ry = 120 * s, 40 * s
        d.ellipse([W / 2 - rx, cy - ry, W / 2 + rx, cy + ry], outline=line, width=lw)
        d.ellipse([W / 2 - 5 * s, cy - 3 * s, W / 2 + 5 * s, cy + 3 * s], fill=line)
        for u_line, u_in, u_six in ((0.0, 0.15, 0.055), (1.0, 0.85, 0.945)):   # surfaces de réparation et de but
            for uu, v0, v1 in ((u_in, 0.16, 0.74), (u_six, 0.32, 0.58)):
                y0, y1 = pitch_y(g, v0), pitch_y(g, v1)
                d.line([(pitch_x(g, W, u_line, y0), y0), (pitch_x(g, W, uu, y0), y0), (pitch_x(g, W, uu, y1), y1),
                        (pitch_x(g, W, u_line, y1), y1)], fill=line, width=lw)
        layers = []
        palette = tuple(mix(c, (120, 120, 130), 0.3) for c in ((230, 70, 50), (250, 140, 60), (240, 240, 240), (60, 120, 230),
                                                               (90, 170, 255), (250, 210, 60), (40, 160, 90), (130, 70, 170), (30, 34, 50)))
        rows = 5                                                         # le public, du haut des gradins vers le bas
        for i in range(rows):
            k = i / (rows - 1)
            hh = int((34 + 26 * k) * s)
            img = fans_layer(W, hh, s, rng, palette, dark=(0.74 - 0.22 * k) if night else (0.5 - 0.3 * k))
            y = int(stand_top + 4 * s + (boards - 6 * s - stand_top) * (i + 1) / rows - hh)
            layers.append({"img": img, "y": y, "f": 0.0, "stage": "crowd", "bob": 1.4 + 0.6 * i, "phase": i * 1.3})
        if night:                                                        # projecteurs
            lights = []
            c = Sil(W, int(90 * s), s)
            for x in (0.04, 0.32, 0.68, 0.96):
                c.rect(W * x - 4 * s, 20 * s, W * x + 4 * s, 90 * s)
                c.rect(W * x - 46 * s, 0, W * x + 46 * s, 22 * s)
                for k in range(4):
                    lights.append((W * x - 33 * s + k * 22 * s, 11 * s))
            layers.insert(0, {"img": paint(c.mask(), [(0, (40, 44, 60)), (1, (20, 22, 32))]), "y": 0, "f": 0.0, "stage": "far",
                              "lights": lights})
            for x in (0.04, 0.32, 0.68, 0.96):                           # flaques de lumière sur la pelouse
                add_at(sky, radial(int(700 * s), (30, 40, 26), 2.0), int(W * x), int(H * 0.9))
        amb = {"crowd": (stand_top + 20 * s, boards - 10 * s), "window": (255, 250, 220), "pitch": g}
        return {"sky": sky, "layers": layers, "tw": W, "amb": amb}
    return build


hd_bg.BUILDERS.update({"pul_earth": build_pul_earth, "pul_water": build_pul_water, "pul_fire": build_pul_fire,
                       "pul_station": build_pul_station, "pul_forest": build_pul_forest, "pul_nebula": build_pul_nebula,
                       "tarot": build_tarot, "stadium_day": build_stadium(False), "stadium_night": build_stadium(True)})
