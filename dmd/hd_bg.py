"""Animated backdrops of the HD screen: sky, parallax layers and ambient animations.

Each backdrop is drawn once with Pillow (a sky and seamless silhouette layers), then the layers slide at
different speeds and the ambience is animated on top (stars, explosions, searchlights, plane, dust, rain,
fireflies, lightning, snow, aurora). Everything is drawn by the program, no image comes from a game.

Décors animés de l'écran HD : ciel, plans qui défilent à des vitesses différentes, ambiance.

Chaque décor (désert au crépuscule, jungle de nuit, montagne enneigée) est dessiné une seule fois
avec Pillow : un ciel fixe et trois plans en silhouette qui se répètent sans couture. À l'affichage,
les plans glissent à des vitesses différentes (effet de profondeur) et l'ambiance s'anime par-dessus :
étoiles qui scintillent, explosions à l'horizon, projecteurs, avion, poussière, pluie, lucioles,
éclairs, neige, aurore. Tout est dessiné par le programme, aucune image tirée d'un jeu.
"""

import math
import random
import threading

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from .hd_fx import FX, Particle

THEMES = ("desert", "jungle", "snow")


# ---------------------------------------------------------------------------- outils de dessin
def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


_NOISE = {}


def noise_rgb(w, h, sigma):
    """Light noise (RGB, around 128) made of a small tile repeated. Image.effect_noise on a whole screen keeps Python
    busy for 40 ms and stops the display while a backdrop is built in the background (1.18).
    / Bruit léger fait d'un petit carreau répété : sur tout l'écran, effect_noise bloque l'affichage 40 ms."""
    tile = _NOISE.get(sigma)
    if tile is None:
        tile = _NOISE[sigma] = Image.effect_noise((128, 128), sigma).convert("RGB")
    out = Image.new("RGB", (w, h))
    for y in range(0, h, 128):
        for x in range(0, w, 128):
            out.paste(tile, (x, y))
    return out


def vgrad(w, h, stops, noise=1.6):
    """Dégradé vertical. stops = [(position 0..1, couleur)], léger bruit pour éviter les bandes."""
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        k = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= k <= p1:
                c = mix(c0, c1, (k - p0) / max(1e-6, p1 - p0))
                break
        else:
            c = stops[-1][1] if k > stops[-1][0] else stops[0][1]
        d.line([0, y, w, y], fill=c)
    if noise:
        n = noise_rgb(w, h, noise)
        img = ImageChops.add(img, n, 1.0, -128)
    return img


def radial(size, color, power=2.0, strength=1.0):
    """Halo rond (RGB, noir autour) à ajouter à une image."""
    g = Image.radial_gradient("L").point(lambda v: int(255 * max(0.0, 1 - v / 181.0) ** power * strength))
    g = g.resize((size, size), Image.BILINEAR)
    return Image.merge("RGB", [g.point(lambda v, c=c: c * v // 255) for c in color])


def add_at(base, img, cx, cy):
    """Ajoute img (RGB) à base, centré en (cx, cy)."""
    w, h = img.size
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    box = (max(0, x0), max(0, y0), min(base.width, x0 + w), min(base.height, y0 + h))
    if box[2] <= box[0] or box[3] <= box[1]:
        return
    part = base.crop(box)
    src = img.crop((box[0] - x0, box[1] - y0, box[2] - x0, box[3] - y0))
    base.paste(ImageChops.add(part, src), box)


class Sil:
    """Silhouette dessinée deux fois plus grande puis réduite (bords lisses), répétée sans couture."""

    def __init__(self, tw, h, s, ss=2):
        self.tw, self.h, self.s, self.ss = tw, h, s, ss
        self.img = Image.new("L", (tw * ss, h * ss), 0)
        self.d = ImageDraw.Draw(self.img)

    def _p(self, pts, dx):
        k = self.ss
        return [((x + dx) * k, y * k) for x, y in pts]

    def _span(self, xs):
        lo, hi = min(xs), max(xs)
        return [dx for dx in (-self.tw, 0, self.tw) if hi + dx >= -2 and lo + dx <= self.tw + 2]

    def poly(self, pts, fill=255):
        for dx in self._span([p[0] for p in pts]):
            self.d.polygon(self._p(pts, dx), fill=fill)

    def ellipse(self, x0, y0, x1, y1, fill=255):
        k = self.ss
        for dx in self._span([x0, x1]):
            self.d.ellipse([(x0 + dx) * k, y0 * k, (x1 + dx) * k, y1 * k], fill=fill)

    def rect(self, x0, y0, x1, y1, fill=255):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill)

    def line(self, pts, width, fill=255):
        k = self.ss
        for dx in self._span([p[0] for p in pts]):
            self.d.line(self._p(pts, dx), fill=fill, width=max(1, int(width * k)), joint="curve")

    def mask(self):
        return self.img.resize((self.tw, self.h), Image.LANCZOS)


def paint(mask, stops, rim=None, rim_px=2, noise=0.0):
    """Remplit une silhouette d'un dégradé vertical, avec un liseré de lumière sur le dessus."""
    w, h = mask.size
    img = vgrad(w, h, stops, noise).convert("RGBA")
    if rim:
        shifted = Image.new("L", (w, h), 0)
        shifted.paste(mask.crop((0, 0, w, h - rim_px)), (0, rim_px))
        edge = ImageChops.subtract(mask, shifted)
        img.paste(Image.new("RGB", (w, h), rim), (0, 0), edge)
    img.putalpha(mask)
    return img


def periodic(tw, rng, n=4, amp=1.0):
    """Courbe qui boucle sur la largeur du motif (somme de sinus de périodes entières)."""
    waves = [(rng.randint(1, 3 + 2 * i), rng.uniform(0.3, 1.0) * amp / (1 + i * 0.6), rng.uniform(0, math.tau))
             for i in range(n)]

    def f(x):
        return sum(a * math.sin(x * math.tau * k / tw + ph) for k, a, ph in waves)
    return f


# ---------------------------------------------------------------------------- éléments de décor
def palm(c, x, base, h, s, rng, lean=None):
    lean = rng.uniform(-0.35, 0.35) if lean is None else lean
    top = (x + lean * h, base - h)
    pts = []
    for i in range(18):                                    # tronc courbé, de plus en plus fin
        k = i / 17
        px = x + lean * h * k * k
        py = base - h * k
        r = (7 - 4 * k) * s
        pts.append((px, py))
        c.ellipse(px - r, py - r, px + r, py + r)
    for j in range(8):                                      # palmes qui retombent
        a = -math.pi / 2 + (j - 3.5) * 0.42 + rng.uniform(-0.1, 0.1)
        ln = rng.uniform(55, 85) * s
        tip = []
        for i in range(10):
            k = i / 9
            ang = a + (1.3 * k * k) * (1 if math.cos(a) >= 0 else -1)
            tip.append((top[0] + math.cos(ang) * ln * k, top[1] + math.sin(ang) * ln * k + 22 * s * k * k))
        upper = [(px, py - (6 - 5 * (i / 9)) * s) for i, (px, py) in enumerate(tip)]
        lower = [(px, py + (6 - 5 * (i / 9)) * s) for i, (px, py) in enumerate(tip)]
        c.poly(upper + list(reversed(lower)))
    c.ellipse(top[0] - 9 * s, top[1] - 7 * s, top[0] + 9 * s, top[1] + 9 * s)


def ruin(c, x, base, w, h, s, rng, holes=True):
    """Immeuble en ruine : sommet cassé, fenêtres percées. Renvoie la place des fenêtres."""
    top = [(x, base - h * rng.uniform(0.75, 1.0))]
    n = rng.randint(3, 6)
    for i in range(1, n):
        top.append((x + w * i / n + rng.uniform(-6, 6) * s, base - h * rng.uniform(0.55, 1.0)))
    top.append((x + w, base - h * rng.uniform(0.6, 0.95)))
    c.poly([(x, base)] + top + [(x + w, base)])
    wins = []
    if holes:
        cols = max(1, int(w / (26 * s)))
        rows = max(1, int(h / (30 * s)))
        for i in range(cols):
            for j in range(rows):
                if rng.random() < 0.55:
                    continue
                wx = x + (i + 0.5) * w / cols
                wy = base - h * 0.12 - j * 30 * s
                if wy < base - h * 0.55:
                    continue
                ww, wh = 7 * s, 10 * s
                c.rect(wx - ww, wy - wh, wx + ww, wy + wh, fill=0)
                wins.append((wx, wy))
    return wins


def dome(c, x, base, w, h, s):
    c.rect(x, base - h, x + w, base)
    c.ellipse(x + w * 0.1, base - h - w * 0.45, x + w * 0.9, base - h + w * 0.35)
    c.rect(x + w / 2 - 2 * s, base - h - w * 0.62, x + w / 2 + 2 * s, base - h - w * 0.3)


def water_tower(c, x, base, h, s):
    w = 46 * s
    for lx in (x + 4 * s, x + w - 8 * s):
        c.rect(lx, base - h * 0.62, lx + 4 * s, base)
    c.line([(x + 6 * s, base - h * 0.1), (x + w - 6 * s, base - h * 0.45)], 2 * s)
    c.line([(x + w - 6 * s, base - h * 0.1), (x + 6 * s, base - h * 0.45)], 2 * s)
    c.rect(x - 2 * s, base - h, x + w + 2 * s, base - h * 0.62)
    c.poly([(x - 6 * s, base - h), (x + w / 2, base - h - 18 * s), (x + w + 6 * s, base - h)])


def mast(c, x, base, h, s):
    """Pylône radio en treillis. Renvoie la place de sa lampe."""
    w = 18 * s
    c.line([(x, base), (x + w / 2, base - h)], 3 * s)
    c.line([(x + w, base), (x + w / 2, base - h)], 3 * s)
    y = base
    i = 0
    while y > base - h + 10 * s:
        k = (base - y) / h
        half = w / 2 * (1 - k)
        c.line([(x + w / 2 - half, y), (x + w / 2 + half, y - 16 * s)], 1.5 * s)
        y -= 16 * s
        i += 1
    return (x + w / 2, base - h - 2 * s)


def sandbags(c, x, base, w, rows, s):
    bh, bw = 11 * s, 24 * s
    for r in range(rows):
        y = base - r * bh * 0.8
        off = (r % 2) * bw / 2 + r * bw * 0.5
        n = int((w - r * bw) / bw)
        for i in range(n):
            bx = x + off + i * bw
            c.ellipse(bx, y - bh, bx + bw * 1.05, y)


def wire_posts(c, x, base, w, s, rng):
    n = max(2, int(w / (60 * s)))
    pts = []
    for i in range(n + 1):
        px = x + i * w / n
        top = base - rng.uniform(34, 46) * s
        c.line([(px, base), (px + rng.uniform(-5, 5) * s, top)], 3 * s)
        pts.append((px, top))
    for row in (0.0, 0.45):
        prev = None
        for px, top in pts:
            y = top + (base - top) * row
            if prev:
                mid = []
                for j in range(8):                               # fil barbelé en zigzag
                    k = j / 7
                    mid.append((prev[0] + (px - prev[0]) * k, prev[1] + (y - prev[1]) * k + (3 * s if j % 2 else -3 * s) + 6 * s * math.sin(k * math.pi)))
                c.line(mid, 1.2 * s)
            prev = (px, y)


def hedgehog(c, x, base, s):
    h = 30 * s
    c.line([(x - 18 * s, base), (x + 16 * s, base - h)], 5 * s)
    c.line([(x + 18 * s, base), (x - 14 * s, base - h)], 5 * s)
    c.line([(x - 3 * s, base + 2 * s), (x + 3 * s, base - h - 6 * s)], 5 * s)


def truck(c, x, base, s, tilt=0.06):
    def T(px, py):                                            # léger basculement de l'épave
        return (x + px * s, base - py * s + px * s * tilt)
    c.poly([T(0, 14), T(120, 14), T(120, 52), T(84, 52), T(84, 68), T(58, 70), T(50, 52), T(0, 52)])
    c.poly([T(84, 52), T(118, 52), T(112, 64), T(88, 66)], fill=0)       # pare-brise vide
    for wx in (18, 96):
        cx, cy = T(wx, 12)
        r = 13 * s
        c.ellipse(cx - r, cy - r, cx + r, cy + r)
    c.line([T(10, 52), T(24, 74)], 3 * s)                                  # ridelle tordue
    c.line([T(30, 52), T(40, 70)], 3 * s)


def jungle_tree(c, x, base, h, s, rng):
    tw = rng.uniform(8, 14) * s
    c.poly([(x - tw, base), (x - tw * 0.45, base - h), (x + tw * 0.45, base - h), (x + tw, base)])
    for _ in range(rng.randint(2, 3)):                       # branches
        by = base - h * rng.uniform(0.45, 0.8)
        d = rng.choice((-1, 1))
        c.line([(x, by), (x + d * rng.uniform(30, 60) * s, by - rng.uniform(20, 40) * s)], 4 * s)
    cr = rng.uniform(38, 60) * s
    blobs = []
    for _ in range(rng.randint(8, 13)):
        bx = x + rng.uniform(-1.3, 1.3) * cr
        by = base - h - rng.uniform(-0.3, 0.9) * cr
        br = rng.uniform(0.35, 0.65) * cr
        c.ellipse(bx - br, by - br, bx + br, by + br)
        blobs.append((bx, by + br * 0.7))
    for bx, by in rng.sample(blobs, min(len(blobs), 4)):     # lianes qui pendent
        ln = rng.uniform(40, 110) * s
        c.line([(bx, by), (bx + rng.uniform(-6, 6) * s, by + ln * 0.5), (bx + rng.uniform(-10, 10) * s, by + ln)], 1.6 * s)


def watchtower(c, x, base, h, s):
    w = 54 * s
    for lx, rx in ((x, x + 8 * s), (x + w, x + w - 8 * s)):
        c.line([(lx, base), (rx, base - h * 0.7)], 4 * s)
    c.line([(x + 4 * s, base - h * 0.15), (x + w - 4 * s, base - h * 0.5)], 2 * s)
    c.line([(x + w - 4 * s, base - h * 0.15), (x + 4 * s, base - h * 0.5)], 2 * s)
    c.rect(x + 2 * s, base - h * 0.72, x + w - 2 * s, base - h * 0.66)
    c.rect(x + 6 * s, base - h * 0.9, x + 10 * s, base - h * 0.7)
    c.rect(x + w - 10 * s, base - h * 0.9, x + w - 6 * s, base - h * 0.7)
    c.poly([(x - 8 * s, base - h * 0.88), (x + w / 2, base - h), (x + w + 8 * s, base - h * 0.88)])
    return (x + w / 2, base - h * 0.8)


def fern(c, x, base, s, rng, size=1.0):
    for j in range(rng.randint(5, 8)):
        a = math.radians(rng.uniform(-160, -20))
        ln = rng.uniform(40, 80) * s * size
        pts = []
        for i in range(8):
            k = i / 7
            ang = a + 0.9 * k * k * (1 if math.cos(a) > 0 else -1)
            pts.append((x + math.cos(ang) * ln * k, base + math.sin(ang) * ln * k))
        up = [(px, py - (5 - 4 * (i / 7)) * s * size) for i, (px, py) in enumerate(pts)]
        lo = [(px, py + (5 - 4 * (i / 7)) * s * size) for i, (px, py) in enumerate(pts)]
        c.poly(up + list(reversed(lo)))


def bamboo(c, x, base, h, s, rng):
    w = rng.uniform(5, 8) * s
    lean = rng.uniform(-0.12, 0.12)
    y = base
    seg = rng.uniform(26, 40) * s
    while y > base - h:
        cx = x + lean * (base - y)
        c.rect(cx - w / 2, y - seg + 2 * s, cx + w / 2, y)
        c.rect(cx - w / 2 - 1.5 * s, y - 2 * s, cx + w / 2 + 1.5 * s, y)
        if rng.random() < 0.4:
            d = rng.choice((-1, 1))
            c.poly([(cx, y - 4 * s), (cx + d * 30 * s, y - 14 * s), (cx + d * 34 * s, y - 10 * s), (cx, y - 1 * s)])
        y -= seg


def pine(c, x, base, h, s, rng):
    tiers = rng.randint(4, 6)
    w = h * rng.uniform(0.36, 0.46)
    c.rect(x - 3 * s, base - h * 0.15, x + 3 * s, base)
    for i in range(tiers):
        k = i / tiers
        ty = base - h * 0.12 - k * h * 0.88
        tw = w * (1 - k * 0.8)
        th = h * 0.88 / tiers * 1.7
        c.poly([(x - tw / 2, ty), (x + rng.uniform(-2, 2) * s, ty - th), (x + tw / 2, ty)])


def cabin(c, x, base, s):
    w, h = 70 * s, 34 * s
    c.rect(x, base - h, x + w, base)
    c.poly([(x - 8 * s, base - h), (x + w / 2, base - h - 26 * s), (x + w + 8 * s, base - h)])
    c.rect(x + w * 0.72, base - h - 30 * s, x + w * 0.72 + 9 * s, base - h - 8 * s)
    c.rect(x + 14 * s, base - h + 10 * s, x + 28 * s, base - h + 22 * s, fill=0)
    return (x + 21 * s, base - h + 16 * s)


def plane_img(s, color, kind="bomber"):
    """Silhouette d'avion vue de côté, tournée vers la gauche (RGBA)."""
    k = 4
    w, h = int(150 * s), int(46 * s)
    img = Image.new("L", (w * k, h * k), 0)
    d = ImageDraw.Draw(img)

    def P(pts):
        return [(px * s * k, py * s * k) for px, py in pts]
    if kind == "heli":
        d.ellipse(P([(36, 14), (96, 40)]), fill=255)
        d.polygon(P([(90, 22), (146, 24), (146, 28), (92, 32)]), fill=255)
        d.polygon(P([(140, 14), (148, 14), (146, 30), (140, 30)]), fill=255)
        d.rectangle(P([(62, 8), (66, 14)]), fill=255)
        d.rectangle(P([(10, 6), (120, 8)]), fill=255)
        d.line(P([(44, 44), (90, 44)]), fill=255, width=2 * k)
        d.line(P([(52, 40), (52, 44)]), fill=255, width=2 * k)
        d.line(P([(82, 40), (82, 44)]), fill=255, width=2 * k)
    else:
        d.polygon(P([(4, 26), (14, 20), (120, 18), (146, 8), (150, 10), (140, 26), (120, 30), (14, 32)]), fill=255)
        d.polygon(P([(52, 26), (84, 26), (106, 40), (96, 41)]), fill=255)
        d.polygon(P([(56, 22), (82, 22), (98, 12), (90, 11)]), fill=255)
        d.polygon(P([(126, 22), (142, 20), (150, 30), (144, 30)]), fill=255)
        for ex in (60, 76):
            d.ellipse(P([(ex - 6, 21), (ex + 4, 29)]), fill=255)
    m = img.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), color + (0,))
    out.putalpha(m)
    return out


def aurora_img(w, h, s, rng):
    """Rubans d'aurore polaire (RGB, à ajouter au ciel)."""
    img = Image.new("RGB", (w, h))
    for band in range(3):
        m = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(m)
        f = periodic(w, rng, 3, 1.0)
        base = h * (0.3 + band * 0.18)
        for x in range(0, w, 2):
            y = base + f(x) * h * 0.18
            top = y - h * rng.uniform(0.18, 0.3)
            d.line([(x, top), (x, y)], fill=int(90 + 60 * (0.5 + 0.5 * math.sin(x * 0.01 + band))), width=2)
        m = m.filter(ImageFilter.GaussianBlur(10 * s))
        col = ((60, 255, 170), (40, 200, 255), (140, 110, 255))[band]
        layer = Image.merge("RGB", [m.point(lambda v, c=c: c * v // 255) for c in col])
        img = ImageChops.add(img, layer)
    return img


# ---------------------------------------------------------------------------- les décors
def build_desert(W, H, s, seed=1):
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.725)
    sky = vgrad(W, H, [(0.0, (8, 10, 34)), (0.30, (40, 24, 70)), (0.52, (120, 52, 88)), (0.64, (214, 102, 82)),
                       (0.72, (250, 168, 96)), (0.80, (170, 92, 70)), (1.0, (80, 40, 50))])
    d = ImageDraw.Draw(sky)
    stars = []
    for _ in range(170):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.34) ** 1.15 / (H * 0.34) ** 0.15
        b = int(rng.uniform(70, 220) * (1 - y / (H * 0.42)))
        if b > 20:
            d.point((x, y), fill=(b, b, min(255, b + 20)))
            if rng.random() < 0.18:
                stars.append((x, y, rng.uniform(1.2, 3.2), rng.uniform(0, math.tau)))
    sun = (int(W * 0.5), int(hz - 4 * s))
    add_at(sky, radial(int(1100 * s), (120, 50, 20), 2.2), *sun)
    add_at(sky, radial(int(420 * s), (200, 110, 50), 2.0), *sun)
    disk = Image.new("L", (int(150 * s), int(150 * s)), 0)
    ImageDraw.Draw(disk).ellipse([4, 4, disk.width - 5, disk.height - 5], fill=255)
    disk = disk.filter(ImageFilter.GaussianBlur(2 * s))
    sky.paste((255, 224, 168), (sun[0] - disk.width // 2, sun[1] - disk.height // 2), disk)
    pad = int(50 * s)                                               # brume chaude sur l'horizon
    haze = Image.new("L", (int(1300 * s) + 2 * pad, int(50 * s) + 2 * pad), 0)
    ImageDraw.Draw(haze).ellipse([pad, pad, haze.width - pad, haze.height - pad], fill=120)
    haze = haze.filter(ImageFilter.GaussianBlur(14 * s))
    sky.paste((236, 132, 92), (sun[0] - haze.width // 2, int(hz - haze.height * 0.55)), haze)
    layers = []
    # nuages longs éclairés par en dessous
    for (y0, y1, n, a, top, bot, factor) in ((int(40 * s), int(230 * s), 7, 120, (70, 40, 84), (255, 150, 112), 0.05),
                                              (int(90 * s), int(290 * s), 5, 150, (52, 28, 64), (210, 100, 92), 0.09)):
        h = y1 - y0
        m = Image.new("L", (tw, h), 0)
        md = ImageDraw.Draw(m)
        for _ in range(n):
            cx, cy = rng.uniform(0, tw), rng.uniform(0.25, 0.75) * h
            lw, lh = rng.uniform(220, 520) * s, rng.uniform(10, 26) * s
            for dx in (-tw, 0, tw):
                for j in range(5):
                    ox = rng.uniform(-0.4, 0.4) * lw
                    md.ellipse([cx + dx + ox - lw / 2, cy - lh / 2 + rng.uniform(-6, 6) * s,
                                cx + dx + ox + lw / 2, cy + lh / 2], fill=a)
        m = m.filter(ImageFilter.GaussianBlur(9 * s))
        layers.append({"img": paint(m, [(0, top), (0.7, mix(top, bot, 0.6)), (1, bot)]), "y": y0, "f": factor, "stage": "sky"})
    # mesas lointaines, puis la plaine éclairée par le soleil couchant
    h = int(220 * s)
    base = int(150 * s)
    c = Sil(tw, h, s)
    x = 0
    while x < tw:
        kind = rng.random()
        if kind < 0.45:
            w, mh = rng.uniform(120, 300) * s, rng.uniform(50, 110) * s
            sl = rng.uniform(20, 50) * s
            c.poly([(x, base), (x + sl, base - mh), (x + sl + w * 0.3, base - mh), (x + sl + w * 0.35, base - mh * 0.9),
                    (x + sl + w, base - mh * 0.9), (x + 2 * sl + w, base)])
            x += w + 2 * sl + rng.uniform(-40, 80) * s
        elif kind < 0.7:
            w, mh = rng.uniform(30, 60) * s, rng.uniform(70, 130) * s
            c.poly([(x, base), (x + 10 * s, base - mh), (x + w, base - mh), (x + w + 14 * s, base)])
            x += w + rng.uniform(40, 160) * s
        else:
            w, mh = rng.uniform(200, 400) * s, rng.uniform(20, 45) * s
            pts = [(x + w * i / 10, base - mh * math.sin(math.pi * i / 10) ** 0.8) for i in range(11)]
            c.poly([(x, base)] + pts + [(x + w, base)])
            x += w * 0.8
    c.rect(-10, base - 3 * s, tw + 10, h)
    k = base / h
    layers.append({"img": paint(c.mask(), [(0, (78, 38, 70)), (k * 0.7, (118, 58, 82)), (k, (166, 86, 90)), (k + 0.012, (226, 130, 96)),
                                           (k + 0.12, (150, 74, 76)), (1, (70, 34, 52))], rim=(236, 140, 104), rim_px=max(1, int(2 * s))),
                   "y": hz - base, "f": 0.12, "stage": "far"})
    # ville en ruine, palmiers, pylône
    h = int(230 * s)
    base = h - 1
    c = Sil(tw, h, s)
    lights, blinks = [], []
    x = rng.uniform(0, 60) * s
    while x < tw - 60 * s:
        r = rng.random()
        if r < 0.36:
            w, bh = rng.uniform(60, 150) * s, rng.uniform(60, 150) * s
            for wx, wy in ruin(c, x, base, w, bh, s, rng):
                if rng.random() < 0.3:
                    lights.append((wx, wy))
            x += w + rng.uniform(4, 40) * s
        elif r < 0.5:
            w, bh = rng.uniform(70, 110) * s, rng.uniform(40, 80) * s
            dome(c, x, base, w, bh, s)
            x += w + rng.uniform(10, 50) * s
        elif r < 0.62:
            palm(c, x + 10 * s, base, rng.uniform(80, 130) * s, s, rng)
            x += rng.uniform(40, 90) * s
        elif r < 0.7:
            water_tower(c, x, base, rng.uniform(90, 130) * s, s)
            x += 70 * s
        elif r < 0.76:
            blinks.append(mast(c, x, base, rng.uniform(150, 200) * s, s))
            x += 40 * s
        else:
            w = rng.uniform(40, 120) * s
            pts = [(x + w * i / 6, base - rng.uniform(8, 34) * s) for i in range(7)]
            c.poly([(x, base)] + pts + [(x + w, base)])
            x += w + rng.uniform(10, 40) * s
    c.rect(-10, base - 6 * s, tw + 10, h)
    layers.append({"img": paint(c.mask(), [(0, (28, 14, 34)), (1, (44, 22, 40))], rim=(140, 70, 70), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(36 * s), "f": 0.38, "stage": "mid", "lights": lights, "blinks": blinks})
    # premier plan : dunes, sacs de sable, barbelés, épave
    h = int(120 * s)
    c = Sil(tw, h, s)
    f = periodic(tw, rng, 4, 14 * s)
    pts = [(x, h * 0.62 + f(x)) for x in range(0, tw + 1, max(4, int(8 * s)))]
    c.poly([(0, h)] + pts + [(tw, h)])
    x = rng.uniform(40, 120) * s
    while x < tw - 100 * s:
        gy = h * 0.62 + f(x)
        r = rng.random()
        if r < 0.3:
            w = rng.uniform(90, 170) * s
            sandbags(c, x, gy + 4 * s, w, rng.randint(2, 4), s)
            x += w + rng.uniform(60, 160) * s
        elif r < 0.55:
            w = rng.uniform(120, 240) * s
            wire_posts(c, x, gy + 4 * s, w, s, rng)
            x += w + rng.uniform(60, 140) * s
        elif r < 0.75:
            hedgehog(c, x, gy + 6 * s, s)
            x += rng.uniform(80, 200) * s
        elif r < 0.85:
            truck(c, x, gy + 8 * s, s)
            x += 220 * s
        else:
            rr = rng.uniform(10, 22) * s
            c.ellipse(x - rr * 1.6, gy - rr, x + rr * 1.6, gy + rr)
            x += rng.uniform(60, 160) * s
    layers.append({"img": paint(c.mask(), [(0, (18, 10, 20)), (1, (8, 5, 10))], rim=(110, 56, 60), rim_px=max(1, int(2 * s))),
                   "y": H - h, "f": 1.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "sun": sun, "explosions": True, "searchlights": [(0.30, 1.1), (0.62, 0.8)],
           "plane": "bomber", "plane_color": (30, 16, 38), "dust": (255, 196, 150), "window": (255, 150, 60), "blink": (255, 40, 30)}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def build_jungle(W, H, s, seed=2):
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    sky = vgrad(W, H, [(0.0, (3, 8, 18)), (0.4, (8, 24, 38)), (0.68, (22, 56, 60)), (0.75, (40, 84, 74)), (1.0, (10, 26, 24))])
    d = ImageDraw.Draw(sky)
    stars = []
    for _ in range(90):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.4)
        b = int(rng.uniform(40, 160) * (1 - y / (H * 0.45)))
        if b > 15:
            d.point((x, y), fill=(b, b + 10, b + 10))
            if rng.random() < 0.15:
                stars.append((x, y, rng.uniform(1, 2.5), rng.uniform(0, math.tau)))
    moon = (int(W * 0.24), int(H * 0.26))
    add_at(sky, radial(int(520 * s), (40, 70, 70), 2.0), *moon)
    disk = Image.new("L", (int(76 * s), int(76 * s)), 0)
    ImageDraw.Draw(disk).ellipse([2, 2, disk.width - 3, disk.height - 3], fill=255)
    disk = disk.filter(ImageFilter.GaussianBlur(1.2 * s))
    sky.paste((226, 238, 214), (moon[0] - disk.width // 2, moon[1] - disk.height // 2), disk)
    craters = Image.new("L", disk.size, 0)
    cd = ImageDraw.Draw(craters)
    for _ in range(6):
        cx, cy, r = rng.uniform(0.25, 0.75) * disk.width, rng.uniform(0.25, 0.75) * disk.height, rng.uniform(3, 9) * s
        cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=60)
    craters = ImageChops.multiply(craters, disk).filter(ImageFilter.GaussianBlur(1.5 * s))
    sky.paste((170, 186, 170), (moon[0] - disk.width // 2, moon[1] - disk.height // 2), craters)
    layers = []
    h = int(160 * s)
    m = Image.new("L", (tw, h), 0)
    md = ImageDraw.Draw(m)
    for _ in range(6):
        cx, cy = rng.uniform(0, tw), rng.uniform(0.2, 0.7) * h
        lw, lh = rng.uniform(300, 600) * s, rng.uniform(12, 30) * s
        for dx in (-tw, 0, tw):
            md.ellipse([cx + dx - lw / 2, cy - lh / 2, cx + dx + lw / 2, cy + lh / 2], fill=110)
    m = m.filter(ImageFilter.GaussianBlur(12 * s))
    layers.append({"img": paint(m, [(0, (30, 50, 60)), (1, (60, 90, 90))]), "y": int(30 * s), "f": 0.05, "stage": "sky"})
    # collines couvertes de forêt
    h = int(170 * s)
    base = h - 1
    c = Sil(tw, h, s)
    f = periodic(tw, rng, 4, 34 * s)
    prof = [(x, base - 80 * s + f(x)) for x in range(0, tw + 1, max(4, int(8 * s)))]
    c.poly([(0, base)] + prof + [(tw, base)])
    for x, y in prof[::2]:
        r = rng.uniform(8, 20) * s
        c.ellipse(x - r, y - r * 0.9, x + r, y + r)
    layers.append({"img": paint(c.mask(), [(0, (16, 44, 44)), (0.6, (26, 64, 60)), (1, (44, 92, 80))], rim=(70, 120, 110), rim_px=max(1, int(2 * s))),
                   "y": hz - h + int(24 * s), "f": 0.12, "stage": "far"})
    h = int(130 * s)                                              # brume qui flotte entre les arbres
    m = Image.new("L", (tw, h), 0)
    md = ImageDraw.Draw(m)
    for _ in range(9):
        cx, cy = rng.uniform(0, tw), rng.uniform(0.35, 0.65) * h
        lw, lh = rng.uniform(300, 700) * s, rng.uniform(22, 44) * s
        for dx in (-tw, 0, tw):
            md.ellipse([cx + dx - lw / 2, cy - lh / 2, cx + dx + lw / 2, cy + lh / 2], fill=80)
    m = m.filter(ImageFilter.GaussianBlur(16 * s))
    layers.append({"img": paint(m, [(0, (120, 170, 160)), (1, (90, 140, 130))]), "y": hz - int(70 * s), "f": 0.22, "stage": "haze"})
    # grands arbres, lianes, mirador
    h = int(300 * s)
    base = h - 1
    c = Sil(tw, h, s)
    lights, blinks = [], []
    x = rng.uniform(0, 80) * s
    while x < tw - 60 * s:
        r = rng.random()
        if r < 0.62:
            jungle_tree(c, x, base, rng.uniform(120, 220) * s, s, rng)
            x += rng.uniform(70, 160) * s
        elif r < 0.72:
            lights.append(watchtower(c, x, base, rng.uniform(150, 190) * s, s))
            x += 120 * s
        else:
            palm(c, x, base, rng.uniform(120, 190) * s, s, rng)
            x += rng.uniform(50, 100) * s
    c.rect(-10, base - 10 * s, tw + 10, h)
    layers.append({"img": paint(c.mask(), [(0, (6, 20, 18)), (1, (12, 34, 28))], rim=(40, 80, 64), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(30 * s), "f": 0.38, "stage": "mid", "lights": lights, "blinks": blinks})
    # fougères et bambous
    h = int(170 * s)
    c = Sil(tw, h, s)
    f = periodic(tw, rng, 3, 10 * s)
    pts = [(x, h * 0.78 + f(x)) for x in range(0, tw + 1, max(4, int(8 * s)))]
    c.poly([(0, h)] + pts + [(tw, h)])
    x = rng.uniform(20, 80) * s
    while x < tw - 60 * s:
        gy = h * 0.78 + f(x)
        if rng.random() < 0.6:
            fern(c, x, gy + 4 * s, s, rng, rng.uniform(0.9, 1.5))
            x += rng.uniform(50, 120) * s
        else:
            for j in range(rng.randint(2, 4)):
                bamboo(c, x + j * 14 * s, gy + 4 * s, rng.uniform(90, 160) * s, s, rng)
            x += rng.uniform(80, 160) * s
    layers.append({"img": paint(c.mask(), [(0, (4, 14, 10)), (1, (2, 8, 6))], rim=(30, 60, 44), rim_px=max(1, int(2 * s))),
                   "y": H - h, "f": 1.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "rain": True, "fireflies": True, "lightning": True, "mist": (120, 170, 160),
           "window": (255, 190, 90), "blink": (255, 60, 40)}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def build_snow(W, H, s, seed=3):
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    sky = vgrad(W, H, [(0.0, (6, 10, 30)), (0.35, (16, 30, 66)), (0.62, (52, 82, 132)), (0.72, (120, 150, 196)), (1.0, (60, 80, 120))])
    d = ImageDraw.Draw(sky)
    stars = []
    for _ in range(150):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.45)
        b = int(rng.uniform(60, 220) * (1 - y / (H * 0.5)))
        if b > 15:
            d.point((x, y), fill=(b, b, min(255, b + 30)))
            if rng.random() < 0.15:
                stars.append((x, y, rng.uniform(1.2, 3.0), rng.uniform(0, math.tau)))
    layers = [{"img": None, "aurora": aurora_img(tw, int(240 * s), s, rng), "y": 0, "f": 0.03, "stage": "sky"}]
    # sommets enneigés
    h = int(220 * s)
    base = h - 1
    rock = Sil(tw, h, s)
    snow = Sil(tw, h, s)
    x = -40 * s
    while x < tw:
        w, ph = rng.uniform(160, 320) * s, rng.uniform(110, 200) * s
        px = x + w * rng.uniform(0.4, 0.6)
        pts = [(x, base)]
        n = 7
        for i in range(1, n):
            k = i / n
            pts.append((x + (px - x) * k + rng.uniform(-6, 6) * s, base - ph * k + rng.uniform(-8, 8) * s))
        pts.append((px, base - ph))
        for i in range(1, n):
            k = i / n
            pts.append((px + (x + w - px) * k + rng.uniform(-6, 6) * s, base - ph * (1 - k) + rng.uniform(-8, 8) * s))
        pts.append((x + w, base))
        rock.poly(pts)
        cap = [p for p in pts if p[1] < base - ph * 0.55]
        if len(cap) >= 3:
            lo = base - ph * 0.55
            jag = []
            a, b = cap[0][0], cap[-1][0]
            for i in range(9):
                jag.append((b - (b - a) * i / 8, lo + rng.uniform(-10, 14) * s))
            snow.poly(cap + jag)
        x += w * rng.uniform(0.45, 0.75)
    rock.rect(-10, base - 4 * s, tw + 10, h)
    rimg = paint(rock.mask(), [(0, (66, 82, 122)), (0.7, (88, 108, 150)), (1, (128, 150, 190))])
    simg = paint(snow.mask(), [(0, (236, 242, 255)), (1, (170, 190, 226))])
    rimg.alpha_composite(simg)
    layers.append({"img": rimg, "y": hz - h + int(16 * s), "f": 0.12, "stage": "far"})
    # forêt de sapins, chalet
    h = int(230 * s)
    base = h - 1
    c = Sil(tw, h, s)
    lights, blinks = [], []
    x = rng.uniform(0, 40) * s
    while x < tw - 40 * s:
        r = rng.random()
        if r < 0.86:
            pine(c, x, base, rng.uniform(60, 170) * s, s, rng)
            x += rng.uniform(18, 50) * s
        elif r < 0.93:
            lights.append(cabin(c, x, base, s))
            x += 100 * s
        else:
            blinks.append(mast(c, x, base, rng.uniform(140, 190) * s, s))
            x += 40 * s
    c.rect(-10, base - 8 * s, tw + 10, h)
    layers.append({"img": paint(c.mask(), [(0, (18, 26, 52)), (1, (30, 42, 72))], rim=(120, 140, 190), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(40 * s), "f": 0.38, "stage": "mid", "lights": lights, "blinks": blinks})
    # congères et piquets
    h = int(110 * s)
    c = Sil(tw, h, s)
    f = periodic(tw, rng, 4, 12 * s)
    pts = [(x, h * 0.55 + f(x)) for x in range(0, tw + 1, max(4, int(8 * s)))]
    c.poly([(0, h)] + pts + [(tw, h)])
    snowbank = paint(c.mask(), [(0, (200, 214, 238)), (0.35, (120, 140, 180)), (1, (60, 76, 110))])
    c2 = Sil(tw, h, s)
    x = rng.uniform(40, 100) * s
    while x < tw - 60 * s:
        gy = h * 0.55 + f(x)
        if rng.random() < 0.6:
            for j in range(rng.randint(3, 7)):
                px = x + j * 26 * s
                c2.line([(px, gy + 10 * s), (px + rng.uniform(-3, 3) * s, gy - rng.uniform(24, 36) * s)], 4 * s)
            c2.line([(x, gy - 18 * s), (x + 26 * s * 6, gy - 16 * s)], 1.5 * s)
            x += rng.uniform(220, 360) * s
        else:
            bx = x
            c2.line([(bx, gy + 8 * s), (bx + 4 * s, gy - 70 * s)], 5 * s)
            for j in range(4):
                by = gy - (20 + j * 14) * s
                d_ = rng.choice((-1, 1))
                c2.line([(bx + 2 * s, by), (bx + d_ * 26 * s, by - 16 * s)], 2.5 * s)
            x += rng.uniform(140, 260) * s
    posts = paint(c2.mask(), [(0, (20, 24, 40)), (1, (12, 14, 26))])
    posts.alpha_composite(snowbank, (0, 0))
    layers.append({"img": posts, "y": H - h, "f": 1.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "snow": True, "searchlights": [(0.7, 0.7)], "plane": "heli",
           "plane_color": (14, 18, 34), "window": (255, 190, 110), "blink": (255, 50, 40)}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def build_arena(W, H, s, seed=4):
    """Salle de tournoi : rampe de projecteurs, faisceaux, public en silhouette (rien ne défile)."""
    rng = random.Random(seed)
    tw = W
    sky = vgrad(W, H, [(0.0, (4, 4, 14)), (0.45, (14, 8, 30)), (0.8, (30, 12, 44)), (1.0, (16, 6, 24))])
    for x in (0.1, 0.3, 0.5, 0.7, 0.9):
        add_at(sky, radial(int(520 * s), (36, 26, 84), 2.0), int(W * x), int(30 * s))
    for _ in range(46):                                               # lumières floues au loin
        add_at(sky, radial(int(rng.uniform(18, 60) * s), rng.choice(((50, 24, 80), (24, 36, 90), (80, 24, 66), (70, 50, 20))), 1.2, 0.7),
               rng.uniform(0, W), rng.uniform(H * 0.25, H * 0.78))
    layers = []
    h = int(60 * s)
    c = Sil(tw, h, s)
    c.rect(-10, 8 * s, tw + 10, 12 * s)
    c.rect(-10, 30 * s, tw + 10, 34 * s)
    x = 0.0
    while x < tw:
        c.line([(x, 10 * s), (x + 14 * s, 32 * s)], 2 * s)
        c.line([(x + 14 * s, 32 * s), (x + 28 * s, 10 * s)], 2 * s)
        x += 28 * s
    spots = []
    for i in range(7):
        x = (i + 0.5) * tw / 7 + rng.uniform(-30, 30) * s
        c.poly([(x - 9 * s, 34 * s), (x + 9 * s, 34 * s), (x + 13 * s, 54 * s), (x - 13 * s, 54 * s)])
        spots.append((x, 52 * s, rng.uniform(0.6, 1.3), rng.uniform(0, math.tau)))
    layers.append({"img": paint(c.mask(), [(0, (34, 34, 50)), (1, (16, 16, 26))], rim=(100, 100, 140), rim_px=max(1, int(2 * s))),
                   "y": 0, "f": 0.0, "stage": "far"})
    layers += crowd_layers(tw, H, s, rng)
    amb = {"arena": True, "spots": spots, "crowd": (H - 118 * s, H - 30 * s)}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


CROWD = ((((38, 20, 58), (24, 12, 36)), (100, 70, 150)), (((14, 8, 22), (8, 4, 12)), (70, 46, 104)))


def crowd_layers(tw, H, s, rng, colors=CROWD, scale=1.0):
    """Deux rangées de public en silhouette, devant tout le reste. Elles sautent quand ça cogne."""
    out = []
    for row, ((top_c, bot_c), rim) in enumerate(colors):
        hh = int((124 if row == 0 else 84) * s * scale)
        c = Sil(tw, hh, s)
        x = -10 * s
        while x < tw:
            w = rng.uniform(22, 34) * s * (1.25 if row else 1.0) * scale
            top = rng.uniform(0.16, 0.42) * hh
            c.ellipse(x + w * 0.25, top, x + w * 0.75, top + w * 0.55)
            c.ellipse(x, top + w * 0.45, x + w, hh + 20 * s)
            if rng.random() < 0.18:                                    # bras levés
                d = rng.choice((-1, 1))
                c.line([(x + w / 2 + d * w * 0.3, top + w * 0.6), (x + w / 2 + d * w * 0.6, top - w * 0.5)], 5 * s * scale)
            x += w * rng.uniform(0.72, 0.95)
        out.append({"img": paint(c.mask(), [(0, top_c), (1, bot_c)], rim=rim, rim_px=max(1, int(2 * s))), "y": H - hh, "f": 0.0,
                    "stage": "crowd", "bob": 3.0 if row == 0 else 4.5, "phase": row * 1.7})
    return out


BUILDERS = {"desert": build_desert, "jungle": build_jungle, "snow": build_snow, "arena": build_arena}


# ---------------------------------------------------------------------------- à l'écran
class Backdrop:
    """Décor animé derrière la scène. draw() chaque image, set_theme() pour changer de décor (volet)."""

    def __init__(self, hd, theme="desert", rng=None, threaded=True):
        self.hd, self.pg, self.s = hd, hd.pg, hd.s
        self.W, self.H = hd.W, hd.H
        self.rng = rng or random.Random()
        self.fx = FX(hd, random.Random(self.rng.random()))
        self.raw = {}                 # décors dessinés (Pillow), prêts à convertir
        self.built = {}               # décors convertis en surfaces pygame
        self.lock = threading.Lock()
        self.theme = theme
        self.scroll = 0.0
        self.speed = 0.0
        self.last = None
        self.wipe = None
        self.amb_state = {}
        self.exc = 0.3                # excitation du public (salle de tournoi), monte avec les coups
        self.static = False           # True : le décor ne défile pas (jeux de combat)
        if threaded:                                         # les autres décors se préparent en arrière-plan
            self.prebuild(THEMES)

    def prebuild(self, names):
        names = [n for n in names if n in BUILDERS]
        threading.Thread(target=self._prebuild, args=(names,), daemon=True).start()

    def _prebuild(self, names):
        for name in names:
            with self.lock:
                if name in self.raw:
                    continue
            try:
                img = BUILDERS[name](self.W, self.H, self.s)
            except Exception:
                continue
            with self.lock:
                self.raw.setdefault(name, img)

    def ready(self, name):
        with self.lock:
            return name in self.raw or name in self.built

    def _get(self, name):
        b = self.built.get(name)
        if b is not None:
            return b
        with self.lock:
            raw = self.raw.get(name)
        if raw is None:
            raw = BUILDERS[name](self.W, self.H, self.s)
            with self.lock:
                self.raw[name] = raw
        hd = self.hd
        layers = []
        for L in raw["layers"]:
            item = dict(L)
            if L.get("aurora") is not None:
                item["surf"] = hd._surf(L["aurora"])
                item["kind"] = "aurora"
            else:
                img = L["img"]
                item["surf"] = hd._surf(img)
                item["kind"] = "layer"
                if img.mode == "RGBA" and img.getchannel("A").histogram()[0] >= 0.65 * img.width * img.height:
                    try:                                      # mostly empty layer (stars...): its empty runs are skipped (1.17)
                        item["surf"].set_alpha(255, self.pg.RLEACCEL)
                    except (AttributeError, self.pg.error):
                        pass
            item["img"] = item["aurora"] = None
            layers.append(item)
        b = {"sky": hd._surf(raw["sky"]), "layers": layers, "tw": raw["tw"], "amb": raw["amb"],
             "imgs": {k: hd._surf(v) for k, v in (raw["amb"].get("images") or {}).items()}}
        if raw["amb"].get("plane"):
            b["plane"] = hd._surf(plane_img(self.s, raw["amb"]["plane_color"], raw["amb"]["plane"]))
        self.built[name] = b
        return b

    def set_theme(self, name, now, wipe=1.1):
        if name not in BUILDERS or name == self.theme:
            return
        if not wipe or wipe <= 0.02 or self.last is None:          # tout de suite, sans volet
            self.theme = name
            self.wipe = None
            self.amb_state = {}
            return
        old = self.pg.Surface((self.W, self.H)).convert()
        self._draw_theme(old, self.theme, now, 0.0)
        self.wipe = (old, now, wipe)
        self.theme = name
        self.amb_state = {}

    # -- dessin
    def draw(self, screen, now, move=0.0):
        """move : -1 (recule) à 1 (avance), 0 : le décor dérive doucement."""
        dt = 0.0 if self.last is None else max(0.0, min(0.1, now - self.last))
        self.last = now
        target = 0.0 if self.static else (0.25 + 1.25 * max(0.0, move) - 0.35 * max(0.0, -move)) * 70 * self.s
        self.speed += (target - self.speed) * min(1.0, dt * 2.5)
        self.scroll += self.speed * dt
        self.exc = 0.3 + (self.exc - 0.3) * max(0.0, 1 - dt * 0.7)
        self.fx.update(now)
        self._draw_theme(screen, self.theme, now, dt)
        if self.wipe is not None:
            old, t0, dur = self.wipe
            k = (now - t0) / dur
            if k >= 1.0:
                self.wipe = None
            else:
                x = int(self.W * (k * k * (3 - 2 * k)))
                screen.blit(old, (x, 0), area=self.pg.Rect(x, 0, self.W - x, self.H))
                g = self.fx.sp.streak(int(self.H * 1.1), int(10 * self.s), (255, 200, 120), 90, 12)
                screen.blit(g, (x - g.get_width() // 2, self.H // 2 - g.get_height() // 2), special_flags=self.pg.BLEND_RGB_ADD)

    def _layer_x(self, L, tw):
        return -((self.scroll * L["f"]) % tw)

    def _draw_theme(self, screen, name, now, dt):
        b = self._get(name)
        screen.blit(b["sky"], (0, 0))
        amb = b["amb"]
        st = self.amb_state.setdefault(name, {"next_boom": now + 1.5, "next_plane": now + 4.0, "plane": None,
                                              "bolt": None, "next_bolt": now + 6.0, "drops": None, "flies": None,
                                              "flakes": None, "dust": None})
        self._stars(screen, amb, now)
        hooks = amb.get("hooks") or {}
        for fn in hooks.get("sky", ()):
            fn(self, screen, b, None, now, dt)
        tw = b["tw"]
        for L in b["layers"]:
            stage = L["stage"]
            if stage == "far":
                self._plane(screen, b, st, now, dt)
            surf = L["surf"]
            x = self._layer_x(L, tw)
            if L["kind"] == "aurora":
                self._aurora(screen, surf, x, tw, now)
            else:
                w = surf.get_width()
                y = L["y"]
                if L.get("bob"):                                     # le public bouge, plus fort quand ça cogne
                    y += int(abs(math.sin(now * 6.5 + L.get("phase", 0))) * L["bob"] * self.s * min(2.0, self.exc))
                screen.blit(surf, (int(x), y))
                if x + w < self.W:
                    screen.blit(surf, (int(x + w), y))
            if stage == "far":
                self._lights(screen, amb, L, tw, now)
                self._horizon(screen, amb, st, now, L, tw)
                if amb.get("arena"):
                    self._beams(screen, amb, now)
                self.fx.draw(screen, "far")
            elif stage == "mid":
                self._lights(screen, amb, L, tw, now)
                self._searchlights(screen, amb, now)
                self.fx.draw(screen, "mid")
            elif stage != "crowd":
                self._lights(screen, amb, L, tw, now)
            for fn in hooks.get(stage, ()):
                fn(self, screen, b, L, now, dt)
        for fn in hooks.get("front", ()):
            fn(self, screen, b, None, now, dt)
        self._weather(screen, amb, st, now, dt)
        if amb.get("crowd"):
            self._flashes(amb, now, dt)
        self.fx.draw(screen, "near")

    # -- salle de tournoi
    def excite(self, amount):
        self.exc = min(2.5, self.exc + amount)

    def _beams(self, screen, amb, now):
        sp = self.fx.sp
        cols = ((130, 130, 150), (70, 100, 220), (170, 70, 170), (130, 130, 150), (70, 100, 220), (170, 70, 170), (130, 130, 150))
        lv = min(11, 4 + 2.5 * self.exc)
        for i, (x, y, speed, ph) in enumerate(amb["spots"]):
            ang = 90 + 26 * math.sin(now * 0.45 * speed * (1 + 0.6 * min(1.5, self.exc)) + ph)
            ln = int(560 * self.s)
            g = sp.beam(ln, int(170 * self.s), cols[i % len(cols)], ang, lv)
            cx = x + math.cos(math.radians(ang)) * ln / 2
            cy = y + math.sin(math.radians(ang)) * ln / 2
            screen.blit(g, (int(cx - g.get_width() / 2), int(cy - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
            # no bright dot on the lamps any more: the beams alone (1.16) / plus de point lumineux sur les lampes

    def _flashes(self, amb, now, dt):
        """Flashs d'appareils photo dans le public."""
        rate = 0.8 + 14 * max(0.0, self.exc - 0.4) ** 1.5
        y0, y1 = amb["crowd"]
        n = int(rate * dt + self.rng.random())
        for _ in range(min(6, n)):
            x, y = self.rng.uniform(0, self.W), self.rng.uniform(y0, y1)
            self.fx.glow(x, y, 4, self.rng.uniform(10, 18), (255, 255, 255), 0.09, "near", 1.0, 0.0, hot=1.0)

    # -- ambiance
    def _stars(self, screen, amb, now):
        sp = self.fx.sp
        add = self.pg.BLEND_RGB_ADD
        for x, y, sp_, ph in amb.get("stars", ()):
            lv = 0.5 + 0.5 * math.sin(now * sp_ + ph)
            if lv < 0.25:
                continue
            g = sp.glow(4 * self.s, (200, 210, 255), lv * 7, hot=0.5)
            screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=add)

    def _aurora(self, screen, surf, x, tw, now):
        lv = 0.55 + 0.25 * math.sin(now * 0.7) + 0.1 * math.sin(now * 1.9)
        w = surf.get_width()
        tmp = self.amb_state.setdefault("_aur", {}).get("tmp")
        if tmp is None or tmp.get_size() != (self.W, surf.get_height()):
            tmp = self.pg.Surface((self.W, surf.get_height())).convert()
            self.amb_state["_aur"]["tmp"] = tmp
        tmp.blit(surf, (int(x), 0))
        if x + w < self.W:
            tmp.blit(surf, (int(x + w), 0))
        v = int(255 * max(0.0, min(1.0, lv)))
        tmp.fill((v, v, v), special_flags=self.pg.BLEND_RGB_MULT)
        screen.blit(tmp, (0, 0), special_flags=self.pg.BLEND_RGB_ADD)

    def _plane(self, screen, b, st, now, dt):
        if "plane" not in b:
            return
        p = st.get("plane")
        if p is None and now >= st["next_plane"]:
            d = self.rng.choice((-1, 1))
            y = self.rng.uniform(60, 140) * self.s
            p = st["plane"] = {"x": self.W + 160 * self.s if d < 0 else -160 * self.s, "y": y, "d": d, "t0": now,
                               "flak": now + 1.0}
        if p is None:
            return
        p["x"] += p["d"] * 95 * self.s * dt
        img = b["plane"]
        if p["d"] > 0:
            key = "_flip"
            fl = b.get(key)
            if fl is None:
                fl = b[key] = self.pg.transform.flip(img, True, False)
            img = fl
        bob = math.sin((now - p["t0"]) * 1.3) * 4 * self.s
        screen.blit(img, (int(p["x"] - img.get_width() / 2), int(p["y"] + bob - img.get_height() / 2)))
        if int(now * 2.5) % 2 == 0:
            g = self.fx.sp.glow(5 * self.s, b["amb"].get("blink", (255, 40, 30)), 10)
            screen.blit(g, (int(p["x"] - g.get_width() / 2 + p["d"] * 30 * self.s), int(p["y"] + bob - g.get_height() / 2)),
                        special_flags=self.pg.BLEND_RGB_ADD)
        if now >= p["flak"] and b["amb"].get("explosions"):
            p["flak"] = now + self.rng.uniform(0.4, 1.2)
            fx = self.fx
            fxx = p["x"] + self.rng.uniform(-120, 120) * self.s
            fxy = p["y"] + self.rng.uniform(-40, 50) * self.s
            fx.glow(fxx, fxy, 4, 22, (255, 190, 120), 0.25, "far", 0.8, 0.0)
            fx.smoke(fxx, fxy, 2, (6, 10), 2.0, (1.0, 1.8), (2, 8), 6, (40, 30, 40), 160, "far")
        if p["x"] < -260 * self.s or p["x"] > self.W + 260 * self.s:
            st["plane"] = None
            st["next_plane"] = now + self.rng.uniform(10, 18)

    def _horizon(self, screen, amb, st, now, L, tw):
        if not amb.get("explosions") or now < st["next_boom"]:
            return
        st["next_boom"] = now + self.rng.uniform(2.0, 4.5)
        x = self.rng.uniform(0.05, 0.95) * self.W
        y = amb["horizon"] - self.rng.uniform(0, 6) * self.s
        fx = self.fx
        big = self.rng.uniform(0.6, 1.2)
        fx.glow(x, y, 20 * big, 110 * big, (255, 150, 70), 0.7, "far", 0.9, 0.0)
        fx.glow(x, y, 8 * big, 40 * big, (255, 230, 170), 0.25, "far", 1.0, 0.0)
        for i in range(int(7 * big)):
            p = fx.add(Particle("puff", x + self.rng.uniform(-10, 10) * self.s, y, now + i * 0.12, self.rng.uniform(3.5, 5.5), "far"))
            r0 = self.rng.uniform(10, 18)
            p.r0, p.r1 = r0 * self.s, r0 * 3.2 * self.s
            p.vx = -self.speed * L["f"] - self.rng.uniform(4, 12) * self.s
            p.vy = -self.rng.uniform(14, 26) * self.s
            p.a0, p.a1 = 150, 0
            p.col = (64, 40, 56)
            p.data = self.rng.randint(0, 2)

    def _lights(self, screen, amb, L, tw, now):
        sp = self.fx.sp
        add = self.pg.BLEND_RGB_ADD
        x0 = self._layer_x(L, tw)
        y0 = L["y"]
        col = amb.get("window", (255, 150, 60))
        for i, (lx, ly) in enumerate(L.get("lights", ())):
            for dx in (0, tw):
                x = x0 + lx + dx
                if -40 < x < self.W + 40:
                    lv = 5 + 3 * math.sin(now * (3 + i % 5) + i) + 2 * math.sin(now * 11 + i * 3)
                    g = sp.glow(16 * self.s, col, lv, hot=0.2)
                    screen.blit(g, (int(x - g.get_width() / 2), int(y0 + ly - g.get_height() / 2)), special_flags=add)
        on = int(now * 1.2) % 2 == 0
        for i, (lx, ly) in enumerate(L.get("blinks", ())):
            if not on:
                continue
            for dx in (0, tw):
                x = x0 + lx + dx
                if -40 < x < self.W + 40:
                    g = sp.glow(10 * self.s, amb.get("blink", (255, 40, 30)), 11, hot=0.6)
                    screen.blit(g, (int(x - g.get_width() / 2), int(y0 + ly - g.get_height() / 2)), special_flags=add)

    def _searchlights(self, screen, amb, now):
        beams = amb.get("searchlights")
        if not beams:
            return
        sp = self.fx.sp
        for i, (fx, speed) in enumerate(beams):
            ang = -90 + 32 * math.sin(now * 0.35 * speed + i * 2.1)
            ln = int(440 * self.s)
            g = sp.beam(ln, int(110 * self.s), (120, 118, 96), ang, 5)
            bx = fx * self.W
            by = amb["horizon"] + 30 * self.s
            cx = bx + math.cos(math.radians(ang)) * ln / 2
            cy = by + math.sin(math.radians(ang)) * ln / 2
            screen.blit(g, (int(cx - g.get_width() / 2), int(cy - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)

    def _weather(self, screen, amb, st, now, dt):
        rng, s, W, H = self.rng, self.s, self.W, self.H
        sp = self.fx.sp
        add = self.pg.BLEND_RGB_ADD
        if amb.get("dust"):
            if st["dust"] is None:
                st["dust"] = [[rng.uniform(0, W), rng.uniform(H * 0.55, H), rng.uniform(0.4, 1.0), rng.uniform(0, 6)] for _ in range(46)]
            col = amb["dust"]
            for d in st["dust"]:
                d[0] -= (20 + 60 * d[2]) * s * dt + self.speed * 0.6 * d[2] * dt
                if d[0] < -10:
                    d[0], d[1] = W + 10, rng.uniform(H * 0.55, H)
                y = d[1] + math.sin(now * 1.3 + d[3]) * 6 * s
                g = sp.glow(3 * s + 3 * d[2] * s, col, 2 + 3 * d[2], hot=0.1)
                screen.blit(g, (int(d[0]), int(y)), special_flags=add)
        if amb.get("rain"):
            if st["drops"] is None:
                st["drops"] = [[rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.5, 1.0)] for _ in range(110)]
            for d in st["drops"]:
                v = (900 + 600 * d[2]) * s
                d[0] -= v * 0.25 * dt
                d[1] += v * dt
                if d[1] > H:
                    d[0], d[1] = rng.uniform(0, W + 200 * s), -20 * s
                g = sp.streak(int(28 * s * d[2]) + 6, 2, (90, 120, 130), 104, 4 + 4 * d[2])
                screen.blit(g, (int(d[0]), int(d[1])), special_flags=add)
        if amb.get("fireflies"):
            if st["flies"] is None:
                st["flies"] = [[rng.uniform(0, W), rng.uniform(H * 0.45, H * 0.95), rng.uniform(0, 6), rng.uniform(0.5, 1.5)] for _ in range(26)]
            for f in st["flies"]:
                f[0] += math.sin(now * 0.7 * f[3] + f[2]) * 22 * s * dt - self.speed * 0.4 * dt
                f[1] += math.cos(now * 0.9 * f[3] + f[2] * 2) * 16 * s * dt
                if f[0] < -20:
                    f[0] = W + 20
                lv = max(0.0, math.sin(now * 2.2 * f[3] + f[2])) * 9
                if lv > 0.5:
                    g = sp.glow(9 * s, (190, 255, 120), lv, hot=0.7)
                    screen.blit(g, (int(f[0] - g.get_width() / 2), int(f[1] - g.get_height() / 2)), special_flags=add)
        if amb.get("lightning"):
            if now >= st["next_bolt"]:
                st["next_bolt"] = now + rng.uniform(7, 14)
                self.fx.flash((120, 140, 170), 0.55, 0.12)
                self.fx.later(0.18, self.fx.flash, (150, 170, 200), 0.75, 0.22)
        if amb.get("snow"):
            if st["flakes"] is None:
                st["flakes"] = [[rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.3, 1.0), rng.uniform(0, 6)] for _ in range(150)]
            wind = 40 + 30 * math.sin(now * 0.3)
            for f in st["flakes"]:
                f[0] -= (wind * f[2] + self.speed * 0.5 * f[2]) * s * dt - math.sin(now + f[3]) * 10 * s * dt
                f[1] += (30 + 70 * f[2]) * s * dt
                if f[1] > H or f[0] < -10:
                    f[0], f[1] = rng.uniform(0, W + 100 * s), -10
                g = sp.glow(2 * s + 4 * f[2] * s, (220, 230, 255), 3 + 6 * f[2], hot=0.3)
                screen.blit(g, (int(f[0]), int(f[1])), special_flags=add)
        if amb.get("mist"):
            pass
        self.fx.draw_flash(screen)
