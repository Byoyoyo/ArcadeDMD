"""HD backdrops of the Neo Geo games done one by one (1.17): space (Blazing Star), bubbles (Puzzle Bobble),
the six Windjammers courts and a golf course (Neo Turf Masters). Everything is drawn by the program, no image
comes from a game. The backdrops register in hd_bg.BUILDERS when this module is imported.

Décors HD des jeux Neo Geo faits un par un (1.17) : espace, bulles, les six terrains de Windjammers, parcours
de golf. Tout est dessiné par le programme, aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from . import hd_bg
from .hd_bg import Sil, add_at, crowd_layers, mix, paint, palm, periodic, radial, vgrad


def _rgba(w, h):
    return Image.new("RGBA", (max(1, int(w)), max(1, int(h))), (0, 0, 0, 0))


def _soft(img, r):
    """Halo doux sous un dessin (étoiles, néons)."""
    return Image.alpha_composite(img.filter(ImageFilter.GaussianBlur(r)), img)


# ---------------------------------------------------------------------------- espace (Blazing Star)
def star_layer(W, h, s, rng, n, size, colors, glow=0.0):
    img = _rgba(W, h)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, h)
        r = rng.uniform(*size) * s
        c = rng.choice(colors) + (255,)
        if r < 0.9:
            d.point((x, y), fill=c)
        else:
            d.ellipse([x - r, y - r, x + r, y + r], fill=c)
    return _soft(img, glow * s) if glow else img


def streak_layer(W, h, s, rng, n, color):
    """Traits de vitesse (étoiles proches qui filent)."""
    img = _rgba(W, h)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, h)
        ln = rng.uniform(40, 140) * s
        for k in range(12):
            a = int(255 * (1 - k / 12) ** 1.5)
            d.line([(x + ln * k / 12, y), (x + ln * (k + 1) / 12, y)], fill=color + (a,), width=max(1, int(2 * s)))
    return img


def planet_cap(W, s, R, cap, dark, light, atm):
    """Big planet rising at the bottom of the screen: its visible cap and its glowing atmosphere (RGBA,
    a margin on top for the glow). / Grosse planète qui se lève en bas de l'écran, avec son atmosphère."""
    R, cap = R * s, cap * s
    m = int(50 * s)
    h = int(cap + m)
    cx, top = W / 2, m
    box = [cx - R, top, cx + R, top + 2 * R]
    glow = Image.new("L", (W, h), 0)                              # atmosphère autour du bord
    ImageDraw.Draw(glow).ellipse([box[0] - 16 * s, box[1] - 16 * s, box[2] + 16 * s, box[3] + 16 * s], fill=190)
    out = Image.new("RGBA", (W, h), atm + (0,))
    out.putalpha(glow.filter(ImageFilter.GaussianBlur(18 * s)))
    disk = Image.new("L", (W, h), 0)
    ImageDraw.Draw(disk).ellipse(box, fill=255)
    body = vgrad(W, h, [(0.0, light), (min(0.99, (m + 26 * s) / h), mix(light, dark, 0.55)), (1.0, dark)], noise=1.2)
    bd = ImageDraw.Draw(body)
    for k, tone in ((0.03, 0.18), (0.07, -0.12), (0.11, 0.12), (0.16, -0.1), (0.22, 0.08)):    # couches de nuages
        rr = R * (1 - k)
        c = mix(dark, light, 0.45 + tone) if tone > 0 else mix(dark, (0, 0, 0), -tone)
        bd.ellipse([cx - rr * 1.02, top + R * k * 1.4, cx + rr * 1.02, top + R * k * 1.4 + 2 * rr], outline=c,
                   width=max(2, int(R * 0.012)))
    body = body.filter(ImageFilter.GaussianBlur(1.5 * s))
    out.paste(body, (0, 0), disk)
    rim = Image.new("L", (W, h), 0)                               # liseré de lumière sur le bord
    ImageDraw.Draw(rim).ellipse(box, outline=255, width=max(2, int(5 * s)))
    rim = ImageChops.multiply(rim.filter(ImageFilter.GaussianBlur(3 * s)), disk)
    out.paste(Image.new("RGB", (W, h), mix(atm, (255, 255, 255), 0.5)), (0, 0), rim)
    return out


def hook_comet(bd, screen, b, L, now, dt):
    """Comète qui traverse le ciel de temps en temps."""
    st = bd.amb_state.setdefault("_comet", {"t": now + 4.0, "p": None})
    s = bd.s
    if st["p"] is None:
        if now < st["t"]:
            return
        st["p"] = [bd.W + 60 * s, bd.rng.uniform(20, 160) * s, bd.rng.uniform(0.18, 0.35)]
    p = st["p"]
    p[0] -= 700 * s * dt
    p[1] += 700 * s * dt * p[2]
    sp = bd.fx.sp
    g = sp.streak(int(220 * s), int(5 * s), (170, 210, 255), -math.degrees(math.atan(p[2])) + 180, 10)
    screen.blit(g, (int(p[0]), int(p[1] - g.get_height() / 2)), special_flags=bd.pg.BLEND_RGB_ADD)
    h = sp.glow(8 * s, (220, 240, 255), 11, hot=0.9)
    screen.blit(h, (int(p[0] - h.get_width() / 2), int(p[1] - h.get_height() / 2)), special_flags=bd.pg.BLEND_RGB_ADD)
    if p[0] < -300 * s or p[1] > bd.H:
        st["p"] = None
        st["t"] = now + bd.rng.uniform(6, 12)


def build_space(W, H, s, seed=21):
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (2, 2, 12)), (0.5, (10, 6, 30)), (1.0, (6, 4, 18))])
    for cx, cy, sz, col in ((0.22, 0.45, 900, (60, 18, 86)), (0.62, 0.62, 1100, (8, 46, 74)), (0.9, 0.25, 700, (66, 12, 56)),
                            (0.45, 0.15, 600, (24, 26, 80))):
        add_at(sky, radial(int(sz * s), col, 1.6), int(W * cx), int(H * cy))
    d = ImageDraw.Draw(sky)
    twinkle = []
    for _ in range(340):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        v = rng.randint(40, 150)
        d.point((x, y), fill=(v, v, min(255, v + 30)))
        if rng.random() < 0.07:
            twinkle.append((x, y, rng.uniform(1.5, 3.5), rng.uniform(0, math.tau)))
    cap = planet_cap(W, s, 760, 118, (14, 16, 52), (96, 120, 220), (90, 170, 255))
    layers = [
        {"img": star_layer(W, H, s, rng, 260, (0.4, 0.9), [(140, 150, 200), (200, 200, 235), (255, 230, 200)]), "y": 0, "f": 0.12,
         "stage": "far"},
        {"img": star_layer(W, H, s, rng, 90, (0.9, 1.8), [(180, 200, 255), (255, 255, 255), (255, 220, 180)], glow=2.0), "y": 0,
         "f": 0.45, "stage": "mid"},
        {"img": cap, "y": H - cap.height, "f": 0.0, "stage": "mid"},          # devant les étoiles, derrière les traits de vitesse
        {"img": streak_layer(W, H, s, rng, 22, (140, 180, 255)), "y": 0, "f": 1.8, "stage": "near"},
    ]
    amb = {"stars": twinkle, "hooks": {"far": [hook_comet]}}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


# ---------------------------------------------------------------------------- bulles (Puzzle Bobble)
def bubble_img(r, s, color=(200, 230, 255)):
    R = max(3, int(r * s))
    size = 2 * R + 6
    img = _rgba(size, size)
    d = ImageDraw.Draw(img)
    c = size / 2
    d.ellipse([c - R, c - R, c + R, c + R], fill=color + (38,), outline=color + (150,), width=max(1, int(R * 0.08)))
    d.ellipse([c - R * 0.55, c - R * 0.62, c - R * 0.1, c - R * 0.3], fill=(255, 255, 255, 170))
    d.ellipse([c + R * 0.35, c + R * 0.3, c + R * 0.55, c + R * 0.5], fill=(255, 255, 255, 90))
    return img


def hook_bubbles(bd, screen, b, L, now, dt):
    """Bulles qui montent en ondulant."""
    st = bd.amb_state.setdefault("_bub", None)
    W, H, s = bd.W, bd.H, bd.s
    keys = ("bub_s", "bub_m", "bub_l")
    if st is None:
        st = bd.amb_state["_bub"] = [[bd.rng.uniform(0, W), bd.rng.uniform(0, H), bd.rng.randrange(3), bd.rng.uniform(0, 6)]
                                     for _ in range(16)]
    for p in st:
        k = p[2]
        p[1] -= (22 + 18 * k) * s * dt
        x = p[0] + math.sin(now * (0.8 + 0.3 * k) + p[3]) * 14 * s
        if p[1] < -60 * s:
            p[0], p[1], p[2] = bd.rng.uniform(0, W), H + 40 * s, bd.rng.randrange(3)
        img = b["imgs"][keys[k]]
        screen.blit(img, (int(x - img.get_width() / 2), int(p[1] - img.get_height() / 2)))


def build_bubbles(W, H, s, seed=22):
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (22, 34, 104)), (0.55, (62, 64, 156)), (1.0, (112, 72, 160))])
    for _ in range(9):
        add_at(sky, radial(int(rng.uniform(300, 700) * s), rng.choice(((60, 30, 70), (20, 50, 90), (70, 50, 20))), 1.8),
               int(rng.uniform(0, W)), int(rng.uniform(0, H)))
    d = ImageDraw.Draw(sky)
    for _ in range(60):                                         # étoiles scintillantes en fond
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        v = rng.randint(120, 220)
        d.point((x, y), fill=(v, v, 255))
    rings = _rgba(W, H)
    rd = ImageDraw.Draw(rings)
    for _ in range(7):                                          # grandes bulles lointaines
        r = rng.uniform(40, 110) * s
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        rd.ellipse([x - r, y - r, x + r, y + r], outline=(190, 210, 255, 46), width=max(2, int(3 * s)))
        rd.ellipse([x - r * 0.55, y - r * 0.62, x - r * 0.15, y - r * 0.32], fill=(255, 255, 255, 40))
    layers = [{"img": rings, "y": 0, "f": 0.05, "stage": "far"}]
    images = {"bub_s": bubble_img(9, s), "bub_m": bubble_img(16, s, (220, 200, 255)), "bub_l": bubble_img(26, s, (190, 255, 230))}
    amb = {"images": images, "hooks": {"front": [hook_bubbles]}, "stars": [(rng.uniform(0, W), rng.uniform(0, H * 0.7),
                                                                         rng.uniform(1.5, 3), rng.uniform(0, 6)) for _ in range(24)]}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


# ---------------------------------------------------------------------------- terrains de Windjammers
COURT = {   # sol (haut, bas), lignes, fond
    "beach": ((236, 210, 152), (210, 176, 118), (255, 255, 255)),
    "lawn": ((86, 168, 70), (58, 132, 50), (240, 250, 240)),
    "tiles": ((186, 214, 238), (140, 182, 220), (255, 255, 255)),
    "concrete": ((142, 142, 148), (104, 104, 112), (255, 214, 60)),
    "clay": ((214, 112, 60), (178, 84, 44), (255, 244, 230)),
    "stadium": ((40, 110, 66), (22, 70, 40), (230, 240, 230)),
}


def _court_floor(sky, W, H, hz, s, kind, rng):
    top, bot, line = COURT[kind]
    floor = vgrad(W, H - hz, [(0.0, top), (1.0, bot)], noise=2.4 if kind in ("beach", "clay", "concrete") else 1.2)
    d = ImageDraw.Draw(floor)
    fh = H - hz
    if kind == "lawn":                                          # bandes de tonte
        for i in range(12):
            if i % 2:
                x0 = W * i / 12
                d.rectangle([x0, 0, x0 + W / 12, fh], fill=mix(top, bot, 0.25))
    elif kind == "tiles":                                       # carrelage
        step = 46 * s
        y = 0.0
        while y < fh:
            x = 0.0
            while x < W:
                if (int(x / step) + int(y / step)) % 2:
                    d.rectangle([x, y, x + step, y + step], fill=mix(top, (255, 255, 255), 0.35))
                x += step
            y += step
        for x in range(0, int(W), int(step)):
            d.line([(x, 0), (x, fh)], fill=(120, 150, 180), width=1)
        for y in range(0, int(fh), int(step)):
            d.line([(0, y), (W, y)], fill=(120, 150, 180), width=1)
    elif kind == "concrete":                                    # fissures
        for _ in range(16):
            x, y = rng.uniform(0, W), rng.uniform(0, fh)
            pts = [(x, y)]
            for _ in range(5):
                x += rng.uniform(-40, 40) * s
                y += rng.uniform(-14, 14) * s
                pts.append((x, y))
            d.line(pts, fill=(80, 80, 86), width=max(1, int(2 * s)))
    elif kind == "stadium":
        for i in range(10):
            if i % 2:
                x0 = W * i / 10
                d.rectangle([x0, 0, x0 + W / 10, fh], fill=mix(top, bot, 0.3))
    lw = max(2, int(5 * s))                                     # lignes du terrain
    m = 40 * s
    d.rectangle([m, 10 * s, W - m, fh - 6 * s], outline=line, width=lw)
    d.line([(W / 2, 10 * s), (W / 2, fh - 6 * s)], fill=line, width=lw)
    d.ellipse([W / 2 - 60 * s, fh / 2 - 26 * s, W / 2 + 60 * s, fh / 2 + 26 * s], outline=line, width=lw)
    for gx in (m, W - m):                                       # buts : 3 points en haut et en bas, 5 au milieu
        third = (fh - 16 * s) / 3
        for j, col in enumerate(((255, 206, 40), (255, 60, 40), (255, 206, 40))):
            y0 = 10 * s + j * third
            d.rectangle([gx - 9 * s, y0, gx + 9 * s, y0 + third - 4 * s], fill=col)
    sky.paste(floor, (0, hz))


def build_court(kind):
    def build(W, H, s, seed=None):
        rng = random.Random(30 + list(COURT).index(kind))
        hz = int(H * 0.42)
        amb = {"horizon": hz}
        layers = []
        if kind == "beach":
            sky = vgrad(W, H, [(0.0, (70, 150, 230)), (0.35, (160, 210, 245)), (0.42, (200, 230, 250)), (1.0, (200, 230, 250))])
            sea = vgrad(W, int(40 * s), [(0.0, (30, 110, 190)), (1.0, (60, 160, 210))])
            sky.paste(sea, (0, hz - int(40 * s)))
            add_at(sky, radial(int(500 * s), (90, 80, 40), 2.0), int(W * 0.72), int(H * 0.1))
            c = Sil(W, int(240 * s), s)
            for x in (0.04, 0.11, 0.9, 0.97):
                palm(c, W * x, 240 * s, rng.uniform(170, 220) * s, s, rng)
            layers.append({"img": paint(c.mask(), [(0, (30, 70, 40)), (1, (20, 50, 30))]), "y": hz - int(200 * s), "f": 0.0,
                           "stage": "far"})
            amb.update(sun_x=W * 0.72, hooks={"sky": [hook_waves]})
        elif kind == "lawn":
            sky = vgrad(W, H, [(0.0, (90, 160, 230)), (0.42, (190, 220, 240)), (1.0, (190, 220, 240))])
            c = Sil(W, int(150 * s), s)
            x = 0.0
            while x < W:
                r = rng.uniform(40, 80) * s
                c.ellipse(x - r, 150 * s - r * 2.2, x + r, 150 * s)
                x += r * 1.2
            layers.append({"img": paint(c.mask(), [(0, (50, 110, 60)), (1, (30, 80, 40))], rim=(110, 170, 100)), "y": hz - int(150 * s),
                           "f": 0.0, "stage": "far"})
        elif kind == "tiles":
            sky = vgrad(W, H, [(0.0, (200, 220, 236)), (0.42, (226, 238, 246)), (1.0, (226, 238, 246))])
            d = ImageDraw.Draw(sky)
            for i in range(8):                                  # baies vitrées
                x = W * (i + 0.5) / 8
                d.rectangle([x - 70 * s, 30 * s, x + 70 * s, hz - 40 * s], fill=(150, 200, 240))
                d.rectangle([x - 70 * s, 30 * s, x + 70 * s, hz - 40 * s], outline=(240, 246, 252), width=max(2, int(6 * s)))
                d.line([(x, 30 * s), (x, hz - 40 * s)], fill=(240, 246, 252), width=max(2, int(4 * s)))
            d.rectangle([0, hz - 30 * s, W, hz], fill=(170, 196, 220))
        elif kind == "concrete":
            sky = vgrad(W, H, [(0.0, (40, 30, 70)), (0.3, (150, 80, 90)), (0.42, (230, 150, 100)), (1.0, (230, 150, 100))])
            c = Sil(W, int(220 * s), s)
            x = -20 * s
            while x < W:
                w, h = rng.uniform(60, 150) * s, rng.uniform(80, 210) * s
                c.rect(x, 220 * s - h, x + w, 220 * s)
                x += w * rng.uniform(0.8, 1.1)
            layers.append({"img": paint(c.mask(), [(0, (40, 30, 50)), (1, (24, 18, 30))], rim=(120, 80, 90)), "y": hz - int(220 * s),
                           "f": 0.0, "stage": "far"})
            fence = _rgba(W, int(70 * s))                       # grillage
            fd = ImageDraw.Draw(fence)
            step = 18 * s
            x = -70 * s
            while x < W + 70 * s:
                fd.line([(x, 0), (x + 70 * s, 70 * s)], fill=(60, 60, 70, 150), width=max(1, int(2 * s)))
                fd.line([(x + 70 * s, 0), (x, 70 * s)], fill=(60, 60, 70, 150), width=max(1, int(2 * s)))
                x += step
            layers.append({"img": fence, "y": hz - int(70 * s), "f": 0.0, "stage": "mid"})
        elif kind == "clay":
            sky = vgrad(W, H, [(0.0, (120, 170, 220)), (0.42, (240, 220, 190)), (1.0, (240, 220, 190))])
            c = Sil(W, int(130 * s), s)
            for k in range(5):                                  # tribunes en gradins
                y = 130 * s - k * 22 * s
                c.rect(-10, y - 22 * s, W + 10, y)
            img = paint(c.mask(), [(0, (150, 60, 40)), (1, (100, 40, 30))], rim=(220, 140, 100))
            layers.append({"img": img, "y": hz - int(130 * s), "f": 0.0, "stage": "far"})
            layers += [dict(L, y=hz - int(118 * s) + int(30 * s) * i, bob=1.5) for i, L in enumerate(crowd_layers(W, H, s, rng, scale=0.5))]
        else:                                                   # stade la nuit
            sky = vgrad(W, H, [(0.0, (4, 6, 18)), (0.42, (20, 26, 50)), (1.0, (20, 26, 50))])
            c = Sil(W, int(150 * s), s)
            c.rect(-10, 40 * s, W + 10, 150 * s)
            lights = []
            for x in (0.06, 0.3, 0.7, 0.94):
                c.rect(W * x - 5 * s, -10, W * x + 5 * s, 60 * s)
                c.rect(W * x - 40 * s, 0, W * x + 40 * s, 22 * s)
                lights.append((W * x, 10 * s))
            layers.append({"img": paint(c.mask(), [(0, (24, 26, 40)), (1, (14, 14, 24))], rim=(80, 90, 130)), "y": hz - int(150 * s),
                           "f": 0.0, "stage": "far", "lights": lights})
            layers += [dict(L, y=hz - int(100 * s) + int(26 * s) * i) for i, L in enumerate(crowd_layers(W, H, s, rng, scale=0.6))]
            amb.update(window=(255, 250, 220), crowd=(hz - 90 * s, hz))
        _court_floor(sky, W, H, hz, s, kind, rng)
        return {"sky": sky, "layers": layers, "tw": W, "amb": amb}
    return build


def hook_waves(bd, screen, b, L, now, dt):
    """Reflets qui scintillent sur la mer."""
    sp = bd.fx.sp
    hz = b["amb"]["horizon"]
    slot = int(now * 8)
    for i in range(28):
        r = random.Random(slot * 97 + i)
        x = r.uniform(0, bd.W)
        y = hz - r.uniform(4, 38) * bd.s
        g = sp.glow(r.uniform(3, 6) * bd.s, (255, 255, 230), r.uniform(3, 8), hot=0.9)
        screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=bd.pg.BLEND_RGB_ADD)


# ---------------------------------------------------------------------------- golf (Neo Turf Masters)
def cloud_img(w, h, s, rng):
    W_, H_ = int(w * s), int(h * s)
    m = Image.new("L", (W_ + 40, H_ + 40), 0)
    d = ImageDraw.Draw(m)
    for _ in range(9):
        r = rng.uniform(0.25, 0.45) * H_
        x = rng.uniform(r, W_ - r) + 20
        y = rng.uniform(H_ * 0.35, H_ * 0.7) + 20
        d.ellipse([x - r * 1.4, y - r, x + r * 1.4, y + r], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(6 * s))
    img = Image.new("RGBA", m.size, (255, 255, 255, 0))
    img.putalpha(m.point(lambda v: int(v * 0.85)))
    return img


def hook_clouds(bd, screen, b, L, now, dt):
    """Nuages qui avancent avec le vent du trou (bd.amb_state["wind"], pixels par seconde)."""
    st = bd.amb_state.setdefault("_clouds", None)
    W, s = bd.W, bd.s
    if st is None:
        st = bd.amb_state["_clouds"] = [[bd.rng.uniform(0, W), bd.rng.uniform(10, 120) * s, i % 3] for i in range(6)]
    wind = bd.amb_state.get("wind", 12.0)
    for c in st:
        img = b["imgs"][f"cloud{c[2]}"]
        c[0] += wind * s * dt * (0.6 + 0.2 * c[2])
        if c[0] > W + 20:
            c[0] = -img.get_width()
        elif c[0] < -img.get_width() - 20:
            c[0] = W
        screen.blit(img, (int(c[0]), int(c[1])))


def hook_flag(bd, screen, b, L, now, dt):
    """Drapeau du trou qui flotte dans le sens du vent."""
    fx_, fy = b["amb"]["flag"]
    s = bd.s
    wind = bd.amb_state.get("wind", 12.0)
    side = 1 if wind >= 0 else -1
    pg = bd.pg
    top = fy - 120 * s
    pg.draw.line(screen, (235, 235, 235), (int(fx_), int(fy)), (int(fx_), int(top)), max(2, int(4 * s)))
    pts = []
    n = 8
    for i in range(n + 1):
        k = i / n
        x = fx_ + side * k * 70 * s
        y = top + 4 * s + math.sin(now * 7 + k * 4) * 5 * s * k
        pts.append((x, y))
    for i in range(n, -1, -1):
        k = i / n
        x = fx_ + side * k * 70 * s
        y = top + 4 * s + 38 * s + math.sin(now * 7 + k * 4 + 0.6) * 5 * s * k
        pts.append((x, y))
    pg.draw.polygon(screen, (230, 40, 40), [(int(x), int(y)) for x, y in pts])


def tree(d, x, base, h, s, dark=(34, 84, 40), light=(78, 150, 62), trunk=(96, 66, 40)):
    """Leafy tree: trunk, four round clumps, light from the upper left. / Arbre feuillu."""
    tw = max(2, h * 0.08)
    d.rectangle([x - tw / 2, base - h * 0.5, x + tw / 2, base], fill=trunk + (255,))
    blobs = ((0.0, -0.62, 0.27), (-0.2, -0.5, 0.21), (0.2, -0.48, 0.21), (0.04, -0.8, 0.2))
    for bx, by, br in blobs:
        r = h * br
        d.ellipse([x + bx * h - r, base + by * h - r, x + bx * h + r, base + by * h + r], fill=dark + (255,))
    for bx, by, br in blobs:
        r = h * br * 0.66
        cx, cy = x + bx * h - h * 0.05, base + by * h - h * 0.06
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=light + (255,))


def build_golf(W, H, s, seed=24):
    rng = random.Random(seed)
    hz = int(H * 0.46)
    sky = vgrad(W, H, [(0.0, (66, 136, 228)), (0.46, (192, 224, 246)), (1.0, (192, 224, 246))])
    add_at(sky, radial(int(640 * s), (96, 86, 44), 2.0), int(W * 0.1), 0)
    f = periodic(W, rng, 4, 1.0)                                  # collines au loin
    c = Sil(W, int(110 * s), s)
    c.poly([(0, 110 * s)] + [(x, (52 + 28 * f(x)) * s) for x in range(0, int(W) + 20, 20)] + [(W, 110 * s)])
    layers = [{"img": paint(c.mask(), [(0, (134, 172, 182)), (1, (106, 150, 146))]), "y": hz - int(104 * s), "f": 0.0, "stage": "far"}]
    row = _rgba(W, int(70 * s))                                   # rangée d'arbres à l'horizon
    rd = ImageDraw.Draw(row)
    x = -10 * s
    while x < W + 20 * s:
        h = rng.uniform(40, 66) * s
        tree(rd, x, 70 * s, h, s, dark=(52, 104, 70), light=(84, 140, 92), trunk=(80, 76, 60))
        x += rng.uniform(22, 46) * s
    layers.append({"img": row, "y": hz - int(66 * s), "f": 0.0, "stage": "far"})
    d = ImageDraw.Draw(sky)                                       # fairway en perspective, bandes de tonte
    vx, vy = W * 0.62, hz - 40 * s
    d.rectangle([0, hz, W, H], fill=(82, 160, 66))
    n = 18
    for i in range(n):
        x0 = -W * 0.6 + (W * 2.2) * i / n
        x1 = -W * 0.6 + (W * 2.2) * (i + 1) / n
        col = (88, 170, 70) if i % 2 else (74, 150, 60)
        k0 = (hz - vy) / (H - vy)
        d.polygon([(vx + (x0 - vx) * k0, hz), (vx + (x1 - vx) * k0, hz), (x1, H), (x0, H)], fill=col)
    gx, gy = W * 0.62, hz + 62 * s                                 # le green, le bunker, le trou
    d.ellipse([gx - 210 * s, gy - 36 * s, gx + 210 * s, gy + 36 * s], fill=(70, 150, 60))
    d.ellipse([gx - 190 * s, gy - 30 * s, gx + 190 * s, gy + 30 * s], fill=(128, 214, 112))
    d.ellipse([gx - 330 * s, gy + 6 * s, gx - 210 * s, gy + 34 * s], fill=(236, 216, 160))
    d.ellipse([gx - 322 * s, gy + 9 * s, gx - 218 * s, gy + 28 * s], fill=(246, 230, 184))
    hole = (gx + 40 * s, gy + 2 * s)
    d.ellipse([hole[0] - 9 * s, hole[1] - 4 * s, hole[0] + 9 * s, hole[1] + 4 * s], fill=(20, 34, 20))
    side = _rgba(W, int(300 * s))                                 # grands arbres sur les bords
    sd = ImageDraw.Draw(side)
    for x, h in ((-30 * s, 280 * s), (70 * s, 200 * s), (W + 30 * s, 290 * s), (W - 80 * s, 210 * s)):
        tree(sd, x, 300 * s, h, s, dark=(26, 70, 34), light=(60, 120, 50))
    layers.append({"img": side, "y": H - int(300 * s) + int(40 * s), "f": 0.0, "stage": "near"})
    images = {f"cloud{i}": cloud_img(rng.uniform(220, 340), rng.uniform(60, 90), s, rng) for i in range(3)}
    amb = {"images": images, "flag": hole, "horizon": hz, "hooks": {"sky": [hook_clouds], "front": [hook_flag]}}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


hd_bg.BUILDERS.update({"space": build_space, "bubbles": build_bubbles, "golf": build_golf})
for _k in COURT:
    hd_bg.BUILDERS["court_" + _k] = build_court(_k)
COURTS = tuple("court_" + k for k in COURT)
