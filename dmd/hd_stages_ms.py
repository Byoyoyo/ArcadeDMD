"""The places of Metal Slug 2 behind its scene, one per mission, drawn by the program with Pillow alone (1.39.3): a town of
the desert, ruins and pyramids, a railway in the mountains, a harbour town, a big city by night, a base in the snow. The
six Metal Slug used to share one round of backdrops (jungle, desert, snow, city, harbour, base) whatever the mission:
the first mission of Metal Slug 2, a town of the desert in broad daylight, played in front of a jungle at night.

Walls lit from the left with a side in the shade, a grain, windows, awnings, roofs, haze in the distance. Every picture
is our own drawing of that kind of place. None comes from a game. A game takes them through "stages" in its "hd" block
(games/mslug2.json), the others keep the round of dmd/hd_stages.py.

/ Les lieux de Metal Slug 2 derrière sa scène, un par mission, dessinés par le programme : une ville du désert, des
ruines et des pyramides, une voie ferrée en montagne, une ville portuaire, une grande ville la nuit, une base sous la
neige. Chaque image est notre dessin de ce genre d'endroit, aucune ne vient d'un jeu.
"""

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from . import hd_bg
from .hd_bg import periodic, vgrad

SS = 2                                   # everything is drawn twice as big, then made small / dessiné en double
FIRES = 2                                # fires burning in a place, each one costs at every image / feux par lieu
LIGHTS = 12                              # lights that flicker on a layer, the same / lumières qui vacillent par plan


def some(rng, things, n):
    """n of them at most, spread over the place. / n au plus, répartis sur le lieu."""
    things = list(things)
    return things if len(things) <= n else sorted(rng.sample(things, n))


def fractal(w, h, rng, cells=(96, 48, 24, 12), contrast=1.0):
    """Soft noise that loops over its width (L, around 128). / Bruit doux qui boucle sur sa largeur."""
    out = Image.new("L", (w, h), 128)
    weight = 0.5
    for cell in cells:
        cw, ch = max(3, w // cell), max(2, h // cell + 1)
        first = Image.frombytes("L", (cw, ch), rng.randbytes(cw * ch))
        if contrast != 1.0:
            first = first.point(lambda v, c=contrast: max(0, min(255, int(128 + (v - 128) * c))))
        small = Image.new("L", (cw + 1, ch))
        small.paste(first, (0, 0))
        small.paste(first.crop((0, 0, 1, ch)), (cw, 0))                     # the last column is the first: it loops
        big = small.resize((w + max(1, w // cw), h), Image.BICUBIC).crop((0, 0, w, h))
        out = ImageChops.add(out, big.point(lambda v, k=weight: int(128 + (v - 128) * k)), 1.0, -128)
        weight *= 0.55
    return out


def settled(sky, layers, W, slow=0.05):
    """What hardly moves is painted into the sky once: the clouds and the farthest crest slid by a few points over a whole
    mission, and each of them cost a wide transparent picture to lay at every image. The rest keeps its own speed.
    / Ce qui bouge à peine est peint dans le ciel une fois : les nuages et la crête la plus lointaine."""
    sky = sky.convert("RGBA")
    kept = []
    for L in layers:
        if L["stage"] == "sky" and L["f"] <= slow and len(L) == 4:
            sky.alpha_composite(L["img"].crop((0, 0, min(W, L["img"].width), L["img"].height)), (0, L["y"]))
        else:
            kept.append(L)
    return sky.convert("RGB"), kept


def shade(col, k):
    return tuple(max(0, min(255, int(c * k))) for c in col)


class Canvas:
    """An RGBA layer drawn twice as big. / Un plan RGBA dessiné en double."""

    def __init__(self, tw, h):
        self.tw, self.h = tw, h
        self.im = Image.new("RGBA", (tw * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def poly(self, pts, fill):
        self.d.polygon(self.P(pts), fill=fill)

    def rect(self, x0, y0, x1, y1, fill):
        self.d.rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=fill)

    def ellipse(self, x0, y0, x1, y1, fill):
        self.d.ellipse([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=fill)

    def chord(self, x0, y0, x1, y1, a0, a1, fill):
        self.d.chord([x0 * SS, y0 * SS, x1 * SS, y1 * SS], a0, a1, fill=fill)

    def line(self, pts, fill, width=1.0):
        self.d.line(self.P(pts), fill=fill, width=max(1, int(width * SS)))

    def soft(self, pts, fill, blur):
        """A soft shape laid over what is drawn (a shadow, a stain). / Une forme douce posée par-dessus."""
        box = [min(p[0] for p in pts) - blur * 3, min(p[1] for p in pts) - blur * 3,
               max(p[0] for p in pts) + blur * 3, max(p[1] for p in pts) + blur * 3]
        x0, y0 = int(box[0] * SS), int(box[1] * SS)
        w, h = max(2, int((box[2] - box[0]) * SS)), max(2, int((box[3] - box[1]) * SS))
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).polygon([(x * SS - x0, y * SS - y0) for x, y in pts], fill=fill[3])
        m = m.filter(ImageFilter.GaussianBlur(blur * SS))
        part = Image.new("RGBA", (w, h), fill[:3] + (0,))
        part.putalpha(m)
        region = self.im.crop((x0, y0, x0 + w, y0 + h))
        alpha = region.getchannel("A")
        region = Image.alpha_composite(region, part)
        region.putalpha(alpha)                                # only on what is there / seulement sur ce qui existe
        self.im.paste(region, (x0, y0))

    def done(self, texture=None, amount=0.22, haze=None, haze_k=0.0):
        im = self.im.resize((self.tw, self.h), Image.LANCZOS)
        a = im.getchannel("A")
        rgb = im.convert("RGB")
        if texture is not None:                               # the grain of the walls / le grain des murs
            t = texture.point(lambda v: int(255 * (1 - amount) + (v - 128) * 2 * amount + 255 * amount * 0.5))
            rgb = ImageChops.multiply(rgb, Image.merge("RGB", (t, t, t)))
        if haze is not None and haze_k > 0:                   # the air between here and there / l'air entre ici et là-bas
            rgb = Image.blend(rgb, Image.new("RGB", rgb.size, haze), haze_k)
        rgb.putalpha(a)
        return rgb


WALLS = ((226, 196, 150), (214, 178, 128), (232, 208, 170), (204, 160, 116), (222, 184, 146), (236, 214, 184), (198, 150, 110))
SHUTTERS = ((52, 118, 124), (64, 96, 150), (122, 70, 46), (70, 120, 84), (150, 60, 50))
CLOTH = (((196, 52, 44), (240, 226, 200)), ((44, 96, 150), (236, 228, 208)), ((214, 150, 40), (240, 226, 190)), ((60, 120, 90), (236, 230, 206)))


def window(c, x, y, w, h, s, rng, wall, arch=True):
    dark = (34, 26, 28)
    c.rect(x - w / 2 - 2 * s, y - h - 2 * s, x + w / 2 + 2 * s, y + 2 * s, shade(wall, 1.1))        # frame / encadrement
    if arch:
        c.ellipse(x - w / 2 - 2 * s, y - h - w / 2 - 2 * s, x + w / 2 + 2 * s, y - h + w / 2 + 2 * s, shade(wall, 1.1))
        c.ellipse(x - w / 2, y - h - w / 2, x + w / 2, y - h + w / 2, dark)
    c.rect(x - w / 2, y - h, x + w / 2, y, dark)
    c.poly([(x - w / 2, y - h), (x + w / 2, y - h), (x - w / 2, y - h * 0.55)], (58, 46, 52))      # a little sky in the glass
    c.rect(x - w / 2 - 3 * s, y, x + w / 2 + 3 * s, y + 3 * s, shade(wall, 1.16))                   # sill / appui
    c.rect(x - w / 2 - 3 * s, y + 3 * s, x + w / 2 + 3 * s, y + 5 * s, shade(wall, 0.7))
    r = rng.random()
    if r < 0.45:                                                                                   # shutters / volets
        col = rng.choice(SHUTTERS)
        for sx in (-1, 1):
            x0 = x + sx * (w / 2 + 1 * s)
            x1 = x0 + sx * w * 0.5
            c.rect(min(x0, x1), y - h, max(x0, x1), y, col)
            for j in range(1, 5):
                yy = y - h + j * h / 5
                c.line([(min(x0, x1), yy), (max(x0, x1), yy)], shade(col, 0.7), 0.6)
    elif r < 0.6:                                                                                  # a grille / une grille
        for j in range(1, 4):
            xx = x - w / 2 + j * w / 4
            c.line([(xx, y - h), (xx, y)], (16, 12, 14), 0.8)
        c.line([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2)], (16, 12, 14), 0.8)
    c.soft([(x - w / 2 - 2 * s, y + 5 * s), (x + w / 2 + 2 * s, y + 5 * s), (x + w / 2, y + 30 * s), (x - w / 2, y + 26 * s)],
           shade(wall, 0.62) + (70,), 2.5 * s)                                                     # a stain under it / coulure


def awning(c, x, y, w, s, rng):
    a, b = rng.choice(CLOTH)
    drop, out = 16 * s, 8 * s
    n = max(4, int(w / (9 * s)))
    for i in range(n):
        x0, x1 = x + i * w / n, x + (i + 1) * w / n
        c.poly([(x0, y), (x1, y), (x1 + out * (2 * (i + 1) / n - 1), y + drop), (x0 + out * (2 * i / n - 1), y + drop)],
               a if i % 2 == 0 else b)
    c.rect(x - out, y + drop, x + w + out, y + drop + 3 * s, shade(a, 0.7))
    c.soft([(x - out, y + drop + 3 * s), (x + w + out, y + drop + 3 * s), (x + w + out, y + drop + 30 * s), (x - out, y + drop + 30 * s)],
           (20, 14, 22, 110), 4 * s)                                                               # its shade / son ombre


def house(c, x, base, w, h, s, rng, lit=1.0):
    """A flat-roofed house, lit from the left. / Une maison à toit plat, éclairée par la gauche."""
    wall = shade(rng.choice(WALLS), lit)
    side = w * rng.uniform(0.10, 0.16)
    top = base - h
    c.rect(x, top, x + w, base, wall)
    c.rect(x + w - side, top, x + w, base, shade(wall, 0.72))                                      # the side in the shade
    c.rect(x - 2 * s, top - 5 * s, x + w + 2 * s, top + 3 * s, shade(wall, 1.1))                   # parapet
    c.rect(x - 2 * s, top + 3 * s, x + w + 2 * s, top + 5 * s, shade(wall, 0.66))
    c.soft([(x, base - 26 * s), (x + w, base - 26 * s), (x + w, base), (x, base)], (40, 26, 30, 120), 7 * s)   # the foot
    c.soft([(x, top + 5 * s), (x + w - side, top + 5 * s), (x + w - side, top + 16 * s), (x, top + 14 * s)],
           (60, 40, 40, 70), 3 * s)                                                                # under the parapet
    floors = max(1, int((h - 30 * s) / (52 * s)))
    cols = max(1, int((w - side - 16 * s) / (38 * s)))
    arch = rng.random() < 0.6
    for f in range(floors):
        y = base - 30 * s - f * 52 * s - (14 * s if f else 0)
        for i in range(cols):
            wx = x + 8 * s + (i + 0.5) * (w - side - 16 * s) / cols
            if f == 0:
                if i == cols // 2 or rng.random() < 0.3:                                           # a door / une porte
                    dw, dh = 20 * s, 40 * s
                    c.ellipse(wx - dw / 2 - 2 * s, base - dh - dw / 2 - 2 * s, wx + dw / 2 + 2 * s, base - dh + dw / 2 + 2 * s, shade(wall, 1.1))
                    c.rect(wx - dw / 2 - 2 * s, base - dh, wx + dw / 2 + 2 * s, base, shade(wall, 1.1))
                    c.ellipse(wx - dw / 2, base - dh - dw / 2, wx + dw / 2, base - dh + dw / 2, (30, 22, 24))
                    c.rect(wx - dw / 2, base - dh, wx + dw / 2, base, (30, 22, 24))
                    if rng.random() < 0.5:
                        awning(c, wx - dw * 0.9, base - dh - dw / 2 - 12 * s, dw * 1.8, s, rng)
                    continue
                if rng.random() < 0.4:
                    continue
            if rng.random() < 0.14:
                continue
            window(c, wx, y, 14 * s, 22 * s, s, rng, wall, arch)
    for _ in range(rng.randint(1, 3)):                                                             # cracks / fissures
        cx, cy = x + rng.uniform(0.1, 0.8) * w, top + rng.uniform(0.1, 0.8) * h
        pts = [(cx, cy)]
        for _ in range(rng.randint(3, 6)):
            cx, cy = cx + rng.uniform(-7, 7) * s, cy + rng.uniform(5, 14) * s
            pts.append((cx, min(cy, base)))
        c.line(pts, shade(wall, 0.55), 0.7)
    if rng.random() < 0.55:                                                                        # bullet holes / impacts
        cx, cy = x + rng.uniform(0.15, 0.7) * w, top + rng.uniform(0.25, 0.75) * h
        for _ in range(rng.randint(5, 11)):
            px, py, r = cx + rng.gauss(0, 14) * s, cy + rng.gauss(0, 9) * s, rng.uniform(0.7, 1.5) * s
            c.ellipse(px - r * 1.6, py - r * 1.6, px + r * 1.6, py + r * 1.6, shade(wall, 0.8))
            c.ellipse(px - r, py - r, px + r, py + r, (44, 32, 32))
    if rng.random() < 0.3:                                                                         # a corner shot away
        k = rng.choice((0, 1))
        bx = x - 3 * s if k == 0 else x + w + 3 * s
        sg = 1 if k == 0 else -1
        bw, bh = rng.uniform(24, 46) * s, rng.uniform(26, 52) * s
        pts = [(bx, top - 8 * s), (bx + sg * bw, top - 8 * s)]
        n = 5
        for i in range(n + 1):
            pts.append((bx + sg * bw * (1 - i / n) + rng.uniform(-3, 3) * s, top + bh * i / n + rng.uniform(-2, 2) * s))
        c.poly(pts, (0, 0, 0, 0))
    r = rng.random()
    if r < 0.28:                                                                                   # a dome / un dôme
        dw = min(w * 0.6, rng.uniform(46, 80) * s)
        dx = x + (w - side) * 0.5
        c.chord(dx - dw / 2, top - 5 * s - dw * 0.48, dx + dw / 2, top - 5 * s + dw * 0.48, 180, 360, shade(wall, 0.98))
        c.chord(dx - dw / 2, top - 5 * s - dw * 0.48, dx + dw / 2 - dw * 0.28, top - 5 * s + dw * 0.48, 180, 360, shade(wall, 1.12))
        c.rect(dx - 1 * s, top - 5 * s - dw * 0.48 - 10 * s, dx + 1 * s, top - 5 * s - dw * 0.48, (70, 56, 50))
    elif r < 0.52:                                                                                 # a tank / une citerne
        tx = x + rng.uniform(0.2, 0.6) * w
        c.rect(tx, top - 26 * s, tx + 22 * s, top - 6 * s, (120, 126, 128))
        c.rect(tx + 15 * s, top - 26 * s, tx + 22 * s, top - 6 * s, (84, 90, 96))
        c.rect(tx - 1 * s, top - 28 * s, tx + 23 * s, top - 25 * s, (150, 156, 158))
    elif r < 0.75:                                                                                 # washing / du linge
        x0, x1 = x + 0.12 * w, x + 0.8 * w
        c.line([(x0, top - 5 * s), (x0, top - 26 * s)], (70, 50, 40), 1.2)
        c.line([(x1, top - 5 * s), (x1, top - 26 * s)], (70, 50, 40), 1.2)
        c.line([(x0, top - 25 * s), ((x0 + x1) / 2, top - 21 * s), (x1, top - 25 * s)], (60, 50, 50), 0.6)
        n = rng.randint(3, 5)
        for i in range(n):
            lx = x0 + (i + 0.6) * (x1 - x0) / (n + 0.4)
            col = rng.choice(((236, 232, 220), (196, 60, 50), (70, 110, 160), (220, 180, 70)))
            c.rect(lx - 5 * s, top - 22 * s, lx + 5 * s, top - 9 * s, col)
            c.rect(lx + 2 * s, top - 22 * s, lx + 5 * s, top - 9 * s, shade(col, 0.8))
    if rng.random() < 0.35:                                                                        # an aerial / une antenne
        ax = x + rng.uniform(0.1, 0.9) * (w - side)
        c.line([(ax, top - 5 * s), (ax, top - 44 * s)], (50, 44, 48), 0.9)
        c.line([(ax - 8 * s, top - 38 * s), (ax + 8 * s, top - 38 * s)], (50, 44, 48), 0.7)
        c.line([(ax - 6 * s, top - 32 * s), (ax + 6 * s, top - 32 * s)], (50, 44, 48), 0.7)


def palm(c, x, base, h, s, rng, lit=1.0):
    lean = rng.uniform(-0.18, 0.18)
    trunk = shade((112, 84, 58), lit)
    pts = [(x + lean * h * (i / 8) ** 1.6, base - h * i / 8) for i in range(9)]
    for i in range(8):
        w = (5 - i * 0.3) * s
        c.line([pts[i], pts[i + 1]], trunk if i % 2 else shade(trunk, 0.82), w)
    tx, ty = pts[-1]
    for i in range(9):
        a = math.pi * (0.08 + i / 8 * 0.84) + rng.uniform(-0.1, 0.1)
        L = rng.uniform(34, 52) * s
        leaf = [(tx, ty)]
        for j in range(1, 7):
            k = j / 6
            leaf.append((tx - math.cos(a) * L * k, ty - math.sin(a) * L * k * 0.55 + (k ** 2) * L * 0.6))
        col = shade((70, 124, 62) if i % 2 else (52, 100, 54), lit)
        c.line(leaf, col, 3.2 * s)
        c.line(leaf[:4], shade(col, 1.25), 1.2 * s)


def build_town(W, H, s, seed=21):
    """Mission 1. A town of the desert at war, in broad daylight. / Une ville du désert en guerre, en plein jour."""
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    haze = (232, 214, 186)
    sky = vgrad(W, H, [(0.0, (30, 84, 160)), (0.30, (78, 142, 206)), (0.55, (150, 192, 222)), (0.68, haze),
                       (0.74, (226, 200, 160)), (1.0, (188, 150, 104))])
    sun = (int(W * 0.24), int(H * 0.16))
    hd_bg.add_at(sky, hd_bg.radial(int(1100 * s), (44, 40, 26), 2.4), *sun)
    hd_bg.add_at(sky, hd_bg.radial(int(240 * s), (90, 84, 64), 1.8), *sun)
    layers = []

    # clouds lit from above / des nuages éclairés par le haut
    h = int(H * 0.56)
    n = fractal(tw, h, rng, cells=(int(260 * s) or 2, int(120 * s) or 2, int(56 * s) or 2, int(26 * s) or 2), contrast=1.1)
    fade = Image.new("L", (1, h))
    fade.putdata([int(255 * max(0.0, min(1.0, (1 - y / h) * 1.5)) * (0.35 + 0.65 * min(1.0, y / (h * 0.25)))) for y in range(h)])
    m = n.point(lambda v: max(0, min(255, int((v - 138) * 5.0))))
    m = ImageChops.multiply(m.filter(ImageFilter.GaussianBlur(3 * s)), fade.resize((tw, h)))
    under = ImageChops.offset(m, 0, -int(7 * s)).filter(ImageFilter.GaussianBlur(5 * s))
    cloud = Image.new("RGB", (tw, h), (252, 248, 240))
    cloud.paste((176, 190, 212), (0, 0), ImageChops.subtract(m, under))                            # their grey undersides
    cloud.putalpha(m.point(lambda v: int(v * 0.86)))
    layers.append({"img": cloud, "y": 0, "f": 0.03, "stage": "sky"})

    # two lines of dunes in the haze / deux lignes de dunes dans la brume
    for (hh, amp, c0, c1, k, f, dy) in ((120, 26, (224, 196, 150), (206, 172, 124), 0.62, 0.05, 30),
                                        (104, 20, (226, 190, 136), (196, 154, 104), 0.40, 0.09, 6)):
        h = int(hh * s)
        c = Canvas(tw, h)
        fn = periodic(tw, rng, 4, amp * s)
        c.poly([(0, h)] + [(x, h * 0.5 + fn(x)) for x in range(0, tw + 1, 8)] + [(tw, h)], c0 + (255,))
        img = c.done()
        g = vgrad(tw, h, [(0, c0), (1, c1)], 0)
        lit = Image.new("L", (tw, h), 0)                                                           # slopes facing the sun
        ld = ImageDraw.Draw(lit)
        for x in range(0, tw, 6):
            slope = fn(x + 6) - fn(x)
            if slope > 0.3 * s:
                ld.rectangle([x, 0, x + 6, h], fill=min(255, int(slope / s * 110)))
        lit = lit.filter(ImageFilter.GaussianBlur(10 * s))
        g = Image.composite(Image.new("RGB", (tw, h), shade(c0, 0.8)), g, lit)
        g = Image.blend(g, Image.new("RGB", (tw, h), haze), k)
        g.putalpha(img.getchannel("A"))
        layers.append({"img": g, "y": hz - int(h * 0.62) - int(dy * s), "f": f, "stage": "sky"})

    wall_tex = fractal(tw, int(300 * s), rng, cells=(int(90 * s) or 2, int(34 * s) or 2, int(12 * s) or 2, int(5 * s) or 2))

    # the town far away, pale / la ville au loin, pâle
    h = int(230 * s)
    c = Canvas(tw, h)
    x = 10 * s
    while x < tw - 150 * s:
        w, bh = rng.uniform(70, 150) * s, rng.uniform(60, 150) * s
        house(c, x, h, w, bh, s * 0.72, rng)
        if rng.random() < 0.16:                                                                    # a tower / une tour
            tx = x + w + 14 * s
            c.rect(tx, h - 190 * s, tx + 16 * s, h, (226, 204, 170))
            c.rect(tx + 11 * s, h - 190 * s, tx + 16 * s, h, (176, 150, 120))
            c.rect(tx - 4 * s, h - 164 * s, tx + 20 * s, h - 158 * s, (236, 216, 186))
            c.poly([(tx - 2 * s, h - 190 * s), (tx + 8 * s, h - 216 * s), (tx + 18 * s, h - 190 * s)], (150, 164, 160))
            x += 34 * s
        x += w + rng.uniform(-10, 40) * s
    far = c.done(wall_tex.resize((tw, h)), 0.16, haze, 0.50)
    smoke = [(rng.uniform(0.1, 0.9) * tw, h - rng.uniform(70, 130) * s) for _ in range(3)]
    layers.append({"img": far, "y": hz - h + int(26 * s), "f": 0.16, "stage": "far", "stacks": smoke})

    # the street, near / la rue, proche
    h = int(300 * s)
    base = h - 1
    c = Canvas(tw, h)
    x = 14 * s
    fires, palms = [], []
    while x < tw - 190 * s:
        w, bh = rng.uniform(120, 220) * s, rng.uniform(120, 250) * s
        if rng.random() < 0.3:
            palms.append((x - 16 * s, rng.uniform(120, 190) * s))
        house(c, x, base, w, bh, s, rng)
        if rng.random() < 0.22:
            fires.append((x + w * rng.uniform(0.3, 0.7), base - bh - 6 * s))
        x += w + rng.uniform(26, 90) * s
    for px, ph in palms:
        palm(c, px, base, ph, s, rng)
    c.soft([(0, base - 10 * s), (tw, base - 10 * s), (tw, base + 4), (0, base + 4)], (50, 34, 36, 120), 5 * s)
    mid = c.done(wall_tex.resize((tw, h)), 0.24, haze, 0.12)
    layers.append({"img": mid, "y": H - h - int(40 * s), "f": 0.38, "stage": "mid", "fires": some(rng, fires, FIRES)})

    def props(c, x, gy):                                                         # what lies in the street / ce qui traîne
        r = rng.random()
        if r < 0.34:
            return sandbags(c, x, gy, s, rng)
        if r < 0.6:                                                              # rubble / des gravats
            for _ in range(rng.randint(4, 8)):
                rr, rx = rng.uniform(6, 18) * s, x + rng.uniform(0, 110) * s
                col = rng.choice(((176, 150, 120), (150, 128, 108), (196, 170, 136)))
                c.poly([(rx - rr, gy + 8 * s), (rx - rr * 0.5, gy - rr * 0.7), (rx + rr * 0.5, gy - rr), (rx + rr, gy + 8 * s)], col)
                c.poly([(rx + rr * 0.1, gy - rr * 0.9), (rx + rr * 0.5, gy - rr), (rx + rr, gy + 8 * s), (rx + rr * 0.3, gy + 8 * s)], shade(col, 0.66))
            return 120 * s
        if r < 0.8:
            for i in range(rng.randint(1, 3)):
                drum(c, x + i * 24 * s, gy, s, rng.choice(((150, 60, 44), (84, 104, 70), (70, 96, 130))))
            return 80 * s
        ww, wh = rng.uniform(70, 120) * s, rng.uniform(24, 40) * s                # a low wall, broken / un muret cassé
        col = (212, 180, 136)
        pts = [(x, gy + 8 * s), (x, gy - wh)]
        for i in range(1, 6):
            pts.append((x + ww * i / 6, gy - wh * rng.uniform(0.45, 1.0)))
        pts += [(x + ww, gy - wh * 0.4), (x + ww, gy + 8 * s)]
        c.poly(pts, col)
        for j in range(3):
            c.line([(x, gy - j * 11 * s), (x + ww, gy - j * 11 * s)], shade(col, 0.72), 0.7)
        return ww + 20 * s
    layers.append(ground_layer(tw, H, s, rng, (222, 188, 136), props))

    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": sun, "explosions": True, "plane": "bomber", "plane_color": (60, 70, 84),
           "dust": (255, 236, 200), "hooks": {"mid": [hd_stages.hook_fires], "far": [hd_stages.hook_stacks]}}
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- pieces shared by the places / pièces communes
def cloud_layer(tw, h, rng, s, cover=138, white=(252, 248, 240), grey=(176, 190, 212), k=0.86, stretch=1.0, f=0.03):
    """Clouds lit from above, their undersides grey. / Des nuages éclairés par le haut, le dessous gris."""
    nw = max(8, int(tw / stretch))
    n = fractal(nw, h, rng, cells=(int(260 * s) or 2, int(120 * s) or 2, int(56 * s) or 2, int(26 * s) or 2), contrast=1.1)
    if nw != tw:
        n = n.resize((tw, h), Image.BICUBIC)
    fade = Image.new("L", (1, h))
    fade.putdata([int(255 * max(0.0, min(1.0, (1 - y / h) * 1.5)) * (0.35 + 0.65 * min(1.0, y / (h * 0.25)))) for y in range(h)])
    m = n.point(lambda v: max(0, min(255, int((v - cover) * 5.0))))
    m = ImageChops.multiply(m.filter(ImageFilter.GaussianBlur(3 * s)), fade.resize((tw, h)))
    under = ImageChops.offset(m, 0, -int(7 * s)).filter(ImageFilter.GaussianBlur(5 * s))
    cloud = Image.new("RGB", (tw, h), white)
    cloud.paste(grey, (0, 0), ImageChops.subtract(m, under))
    cloud.putalpha(m.point(lambda v: int(v * k)))
    return {"img": cloud, "y": 0, "f": f, "stage": "sky"}


def ridge_layer(tw, h, rng, s, amp, c0, c1, haze, k, y, f, peaks=0, snow=None, lit=0.8, waves=4):
    """A line of dunes, hills or mountains, its slopes facing the sun lighter, the air over it.
    / Une ligne de dunes, de collines ou de montagnes, les pentes au soleil plus claires."""
    fn = periodic(tw, rng, waves, amp * s)
    tops = sorted(rng.uniform(0, tw) for _ in range(peaks))
    hs = [rng.uniform(0.5, 1.0) for _ in tops]

    def top(x):
        v = h * 0.5 + fn(x)
        for tx, th in zip(tops, hs):
            d = min(abs(x - tx), tw - abs(x - tx))
            v -= max(0.0, 1 - d / (150 * s * th)) * amp * s * 1.7 * th          # a sharp peak / un pic
        return v
    c = Canvas(tw, h)
    line = [(x, top(x)) for x in range(0, tw + 1, 6)]
    c.poly([(0, h)] + line + [(tw, h)], c0 + (255,))
    mask = c.done().getchannel("A")
    g = vgrad(tw, h, [(0, c0), (1, c1)], 0)
    sun = Image.new("L", (tw, h), 0)
    ld = ImageDraw.Draw(sun)
    for x in range(0, tw, 6):
        slope = top(x + 6) - top(x)
        if slope > 0.3 * s:
            ld.rectangle([x, 0, x + 6, h], fill=min(255, int(slope / s * 110)))
    sun = sun.filter(ImageFilter.GaussianBlur(8 * s))
    g = Image.composite(Image.new("RGB", (tw, h), shade(c0, lit)), g, sun)
    if snow is not None:                                                         # snow down from the crest / de la neige
        sm = Image.new("L", (tw, h), 0)
        sd = ImageDraw.Draw(sm)
        depth, jag = snow[1] * s, periodic(tw, rng, 9, snow[1] * s * 0.45)
        sd.polygon(line + [(x, top(x) + depth + jag(x)) for x in range(tw, -1, -6)], fill=255)
        g = Image.composite(Image.composite(Image.new("RGB", (tw, h), shade(snow[0], 0.86)), Image.new("RGB", (tw, h), snow[0]), sun), g, sm)
    g = Image.blend(g, Image.new("RGB", (tw, h), haze), k)
    g.putalpha(mask)
    return {"img": g, "y": y, "f": f, "stage": "sky"}


def pine(c, x, base, h, s, rng, col=(44, 84, 62), snow=None):
    w = h * 0.36
    c.rect(x - 2 * s, base - h * 0.16, x + 2 * s, base, (74, 54, 40))
    for i in range(4):
        y0 = base - h * (0.14 + i * 0.2)
        ww = w * (1 - i * 0.2)
        c.poly([(x - ww, y0), (x, y0 - h * 0.34), (x + ww, y0)], col)
        c.poly([(x, y0 - h * 0.34), (x + ww, y0), (x + ww * 0.25, y0)], shade(col, 0.74))
        if snow is not None:
            c.poly([(x - ww * 0.55, y0 - h * 0.14), (x, y0 - h * 0.34), (x + ww * 0.5, y0 - h * 0.16), (x, y0 - h * 0.2)], snow)


def crate(c, x, gy, w, h, s, col=(170, 128, 78)):
    c.rect(x, gy - h, x + w, gy, col)
    c.rect(x + w * 0.78, gy - h, x + w, gy, shade(col, 0.68))
    for k in (0.0, 0.5, 1.0):
        c.line([(x, gy - h + k * (h - 2 * s) + 1 * s), (x + w, gy - h + k * (h - 2 * s) + 1 * s)], shade(col, 0.6), 0.9)
    c.line([(x + 2 * s, gy - h + 2 * s), (x + w * 0.76, gy - 2 * s)], shade(col, 0.72), 1.0)


def drum(c, x, gy, s, col):
    c.rect(x, gy - 30 * s, x + 20 * s, gy + 6 * s, col)
    c.rect(x + 13 * s, gy - 30 * s, x + 20 * s, gy + 6 * s, shade(col, 0.62))
    c.rect(x + 2 * s, gy - 30 * s, x + 5 * s, gy + 6 * s, shade(col, 1.3))
    for yy in (-22, -10, 0):
        c.line([(x, gy + yy * s), (x + 20 * s, gy + yy * s)], shade(col, 0.5), 1.0)
    c.ellipse(x, gy - 33 * s, x + 20 * s, gy - 27 * s, shade(col, 1.1))


def sandbags(c, x, gy, s, rng, cols=((158, 146, 104), (146, 134, 94), (170, 156, 112)), cap=None):
    rows, n0 = rng.randint(2, 3), rng.randint(4, 6)
    for j in range(rows):
        for i in range(n0 - j):
            bx, by = x + (i + j * 0.5) * 26 * s, gy + 8 * s - j * 13 * s
            col = rng.choice(cols)
            c.d.rounded_rectangle([bx * SS, (by - 13 * s) * SS, (bx + 25 * s) * SS, by * SS], radius=int(5 * s * SS), fill=col)
            c.d.rounded_rectangle([bx * SS, (by - 5 * s) * SS, (bx + 25 * s) * SS, by * SS], radius=int(4 * s * SS), fill=shade(col, 0.72))
            if cap is not None and j == rows - 1:
                c.d.rounded_rectangle([bx * SS, (by - 16 * s) * SS, (bx + 25 * s) * SS, (by - 9 * s) * SS], radius=int(4 * s * SS), fill=cap)
    return n0 * 26 * s


def ground_layer(tw, H, s, rng, col, props, h=120, tex=0.12, shade_k=(96, 62, 44, 60), edge=(120, 84, 60, 60)):
    """The ground in front, with what lies on it. props(c, x, gy) draws one thing and says how wide it was.
    / Le sol devant, avec ce qui traîne dessus."""
    h = int(h * s)
    c = Canvas(tw, h)
    fn = periodic(tw, rng, 4, 7 * s)
    c.poly([(0, h)] + [(x, h * 0.42 + fn(x)) for x in range(0, tw + 1, 8)] + [(tw, h)], col + (255,))
    x = 40 * s
    while x < tw - 170 * s:
        x += props(c, x, h * 0.42 + fn(x)) + rng.uniform(60, 170) * s
    c.soft([(0, h * 0.42 - 12 * s), (tw, h * 0.42 - 12 * s), (tw, h * 0.42 + 16 * s), (0, h * 0.42 + 16 * s)], edge, 6 * s)
    c.soft([(0, h * 0.8), (tw, h * 0.8), (tw, h + 6), (0, h + 6)], shade_k, 12 * s)
    img = c.done(fractal(tw, h, rng, cells=(int(34 * s) or 2, int(12 * s) or 2, int(5 * s) or 2, int(2 * s) or 2)), tex)
    return {"img": img, "y": H - h, "f": 1.0, "stage": "near"}


# ---------------------------------------------------------------------------- mission 2, ruins and pyramids
STONE = ((226, 200, 152), (214, 186, 136), (232, 210, 166))


def column(c, x, base, h, w, s, rng, col, broken=False):
    """A column of drums with its capital, lit from the left. / Une colonne à tambours et son chapiteau."""
    top = base - h
    c.rect(x - w / 2, top, x + w / 2, base, col)
    c.rect(x - w / 2, top, x - w / 2 + w * 0.2, base, shade(col, 1.1))
    c.rect(x + w / 2 - w * 0.3, top, x + w / 2, base, shade(col, 0.7))
    for yy in range(int(22 * s), int(h), int(22 * s)):
        c.line([(x - w / 2, base - yy), (x + w / 2, base - yy)], shade(col, 0.62), 0.8)
    c.rect(x - w * 0.62, base - 8 * s, x + w * 0.62, base, shade(col, 0.9))
    if broken:
        pts = [(x - w / 2 - 2 * s, top - 2 * s), (x + w / 2 + 2 * s, top - 2 * s)]
        for i in range(6):
            pts.append((x + w / 2 - i * w / 5, top + rng.uniform(4, 22) * s))
        c.poly(pts, (0, 0, 0, 0))
    else:
        c.poly([(x - w / 2, top), (x + w / 2, top), (x + w * 0.78, top - 16 * s), (x - w * 0.78, top - 16 * s)], shade(col, 1.04))
        c.poly([(x + w * 0.2, top), (x + w / 2, top), (x + w * 0.78, top - 16 * s), (x + w * 0.3, top - 16 * s)], shade(col, 0.74))
        c.rect(x - w * 0.84, top - 22 * s, x + w * 0.84, top - 16 * s, shade(col, 1.1))


def stone_wall(c, x, base, w, h, s, rng, col):
    """A wall of big blocks with a band of cut patterns of our own. / Un mur de gros blocs, une frise de motifs à nous."""
    top = base - h
    c.rect(x, top, x + w, base, col)
    c.rect(x + w * 0.9, top, x + w, base, shade(col, 0.72))
    for j in range(1, int(h / (18 * s)) + 1):
        yy = base - j * 18 * s
        c.line([(x, yy), (x + w, yy)], shade(col, 0.66), 0.8)
        for bx in range(int(x + (j % 2) * 16 * s), int(x + w), int(32 * s)):
            c.line([(bx, yy), (bx, yy + 18 * s)], shade(col, 0.7), 0.7)
    fy = top + 10 * s
    c.rect(x + 4 * s, fy, x + w * 0.9 - 4 * s, fy + 16 * s, shade(col, 0.84))
    i = 0
    for fx in range(int(x + 10 * s), int(x + w * 0.9 - 12 * s), int(14 * s)):                       # the band / la frise
        if i % 3 == 0:
            c.rect(fx, fy + 4 * s, fx + 6 * s, fy + 12 * s, shade(col, 0.58))
        elif i % 3 == 1:
            c.poly([(fx, fy + 12 * s), (fx + 4 * s, fy + 4 * s), (fx + 8 * s, fy + 12 * s)], shade(col, 0.6))
        else:
            c.ellipse(fx, fy + 5 * s, fx + 7 * s, fy + 12 * s, shade(col, 0.6))
        i += 1
    if rng.random() < 0.5:                                                                          # its top broken / cassé
        pts = [(x - 2 * s, top - 2 * s), (x + w + 2 * s, top - 2 * s), (x + w + 2 * s, top + rng.uniform(10, 30) * s)]
        for i in range(1, 7):
            pts.append((x + w - i * w / 7, top + rng.uniform(0, 12) * s * (1 - i / 9)))
        c.poly(pts, (0, 0, 0, 0))


def tent(c, x, base, w, h, s, col=(226, 214, 182)):
    c.poly([(x, base), (x + w * 0.5, base - h), (x + w, base)], col)
    c.poly([(x + w * 0.5, base - h), (x + w, base), (x + w * 0.62, base)], shade(col, 0.74))
    c.poly([(x + w * 0.4, base), (x + w * 0.5, base - h * 0.6), (x + w * 0.56, base)], (60, 44, 36))
    c.line([(x + w * 0.5, base - h), (x - 10 * s, base)], (90, 70, 50), 0.6)
    c.line([(x + w * 0.5, base - h), (x + w + 10 * s, base)], (90, 70, 50), 0.6)


def build_ruins(W, H, s, seed=22):
    """Mission 2. Ruins and pyramids in the sand, a dig left in a hurry. / Des ruines et des pyramides dans le sable."""
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    haze = (238, 222, 188)
    sky = vgrad(W, H, [(0.0, (34, 104, 186)), (0.34, (104, 166, 220)), (0.58, (188, 212, 218)), (0.68, haze),
                       (0.74, (232, 206, 156)), (1.0, (198, 160, 106))])
    sun = (int(W * 0.72), int(H * 0.13))
    hd_bg.add_at(sky, hd_bg.radial(int(1100 * s), (46, 42, 26), 2.4), *sun)
    hd_bg.add_at(sky, hd_bg.radial(int(240 * s), (96, 90, 66), 1.8), *sun)
    layers = [cloud_layer(tw, int(H * 0.5), rng, s, cover=150, k=0.7)]
    layers.append(ridge_layer(tw, int(120 * s), rng, s, 24, (226, 200, 152), (206, 174, 124), haze, 0.62, hz - int(104 * s), 0.05))

    h = int(260 * s)                                                             # the pyramids / les pyramides
    c = Canvas(tw, h)
    for cx, b, hg in ((tw * 0.20, 250 * s, 205 * s), (tw * 0.47, 170 * s, 140 * s), (tw * 0.78, 300 * s, 240 * s)):
        apex, ridge = (cx - b * 0.1, h - hg), cx + b * 0.3
        c.poly([apex, (cx - b, h), (ridge, h)], (238, 210, 156))
        c.poly([apex, (ridge, h), (cx + b, h)], (188, 150, 106))
        for j in range(1, int(hg / (7 * s))):
            yy = h - j * 7 * s
            k = j * 7 * s / hg
            c.line([(cx - b + (apex[0] - cx + b) * k, yy), (cx + b + (apex[0] - cx - b) * k, yy)], (170, 136, 96, 90), 0.5)
    layers.append({"img": c.done(None, 0, haze, 0.46), "y": hz - h + int(16 * s), "f": 0.07, "stage": "sky"})
    layers.append(ridge_layer(tw, int(100 * s), rng, s, 18, (228, 194, 140), (198, 158, 108), haze, 0.36, hz - int(60 * s), 0.10))

    tex = fractal(tw, int(300 * s), rng, cells=(int(90 * s) or 2, int(34 * s) or 2, int(12 * s) or 2, int(5 * s) or 2))
    h = int(230 * s)                                                             # a temple far away / un temple au loin
    c = Canvas(tw, h)
    x = 30 * s
    while x < tw - 260 * s:
        kind = rng.random()
        col = rng.choice(STONE)
        if kind < 0.3:                                                           # a gate between two towers / un pylône
            for sx in (0, 1):
                tx = x + sx * 120 * s
                c.poly([(tx, h), (tx + 12 * s, h - 150 * s), (tx + 78 * s, h - 150 * s), (tx + 90 * s, h)], col)
                c.poly([(tx + 62 * s, h - 150 * s), (tx + 78 * s, h - 150 * s), (tx + 90 * s, h), (tx + 70 * s, h)], shade(col, 0.72))
                c.rect(tx + 8 * s, h - 158 * s, tx + 82 * s, h - 150 * s, shade(col, 1.1))
            c.rect(x + 84 * s, h - 96 * s, x + 126 * s, h - 80 * s, shade(col, 0.9))
            c.rect(x + 90 * s, h - 80 * s, x + 120 * s, h, (70, 52, 44))
            x += 250 * s
        elif kind < 0.72:                                                        # a row of columns / une colonnade
            n = rng.randint(3, 6)
            for i in range(n):
                column(c, x + i * 44 * s, h, rng.uniform(90, 110) * s, 18 * s, s * 0.8, rng, col, broken=rng.random() < 0.3)
            if rng.random() < 0.6:
                c.rect(x - 16 * s, h - 132 * s, x + (n - 1) * 44 * s * rng.uniform(0.4, 1.0) + 16 * s, h - 118 * s, shade(col, 1.04))
            x += n * 44 * s + 30 * s
        else:                                                                    # an obelisk / un obélisque
            c.poly([(x, h), (x + 6 * s, h - 170 * s), (x + 20 * s, h - 170 * s), (x + 26 * s, h)], col)
            c.poly([(x + 14 * s, h - 170 * s), (x + 20 * s, h - 170 * s), (x + 26 * s, h), (x + 17 * s, h)], shade(col, 0.72))
            c.poly([(x + 6 * s, h - 170 * s), (x + 13 * s, h - 190 * s), (x + 20 * s, h - 170 * s)], shade(col, 1.1))
            x += 60 * s
        x += rng.uniform(30, 120) * s
    far = c.done(tex.resize((tw, h)), 0.16, haze, 0.44)
    layers.append({"img": far, "y": hz - h + int(26 * s), "f": 0.16, "stage": "far",
                   "stacks": [(rng.uniform(0.1, 0.9) * tw, h - rng.uniform(60, 110) * s) for _ in range(2)]})

    h = int(300 * s)                                                             # the dig / le chantier de fouilles
    base = h - 1
    c = Canvas(tw, h)
    x = 20 * s
    fires = []
    while x < tw - 240 * s:
        kind = rng.random()
        col = rng.choice(STONE)
        if kind < 0.34:
            n = rng.randint(2, 4)
            for i in range(n):
                column(c, x + 20 * s + i * 76 * s, base, rng.uniform(150, 240) * s, 34 * s, s, rng, col, broken=rng.random() < 0.45)
            x += n * 76 * s
        elif kind < 0.62:
            w = rng.uniform(150, 260) * s
            stone_wall(c, x, base, w, rng.uniform(90, 170) * s, s, rng, col)
            if rng.random() < 0.5:                                               # a scaffold against it / un échafaudage
                sx, sh = x + w * 0.2, rng.uniform(110, 190) * s
                for px in (sx, sx + 60 * s):
                    c.line([(px, base), (px, base - sh)], (120, 86, 52), 1.6)
                for yy in range(int(40 * s), int(sh), int(44 * s)):
                    c.rect(sx - 6 * s, base - yy - 3 * s, sx + 66 * s, base - yy, (150, 110, 68))
                c.line([(sx, base), (sx + 60 * s, base - 44 * s)], (110, 80, 50), 0.9)
            if rng.random() < 0.3:
                fires.append((x + w * 0.5, base - 100 * s))
            x += w
        elif kind < 0.82:
            tent(c, x, base, rng.uniform(110, 150) * s, rng.uniform(70, 96) * s, s)
            crate(c, x + 150 * s, base, 34 * s, 28 * s, s)
            crate(c, x + 176 * s, base, 26 * s, 22 * s, s, (150, 112, 70))
            x += 210 * s
        else:
            palm(c, x + 20 * s, base, rng.uniform(130, 190) * s, s, rng)
            palm(c, x + 70 * s, base, rng.uniform(100, 150) * s, s, rng)
            x += 100 * s
        x += rng.uniform(30, 100) * s
    c.soft([(0, base - 10 * s), (tw, base - 10 * s), (tw, base + 4), (0, base + 4)], (60, 40, 36, 120), 5 * s)
    layers.append({"img": c.done(tex.resize((tw, h)), 0.26, haze, 0.10), "y": H - h - int(40 * s), "f": 0.38, "stage": "mid", "fires": some(rng, fires, FIRES)})

    def props(c, x, gy):
        r = rng.random()
        if r < 0.3:                                                              # a column fallen / une colonne tombée
            col = rng.choice(STONE)
            for i in range(rng.randint(2, 4)):
                bx = x + i * 44 * s
                c.rect(bx, gy - 22 * s, bx + 40 * s, gy + 6 * s, col)
                c.rect(bx, gy - 4 * s, bx + 40 * s, gy + 6 * s, shade(col, 0.7))
                c.ellipse(bx + 32 * s, gy - 22 * s, bx + 46 * s, gy + 6 * s, shade(col, 0.82))
            return 180 * s
        if r < 0.55:
            crate(c, x, gy + 6 * s, 36 * s, 30 * s, s)
            crate(c, x + 40 * s, gy + 6 * s, 28 * s, 24 * s, s, (150, 112, 70))
            return 80 * s
        if r < 0.8:
            return sandbags(c, x, gy, s, rng)
        for _ in range(rng.randint(3, 6)):                                       # blocks / des blocs
            bw, bh, bx = rng.uniform(16, 34) * s, rng.uniform(10, 20) * s, x + rng.uniform(0, 100) * s
            col = rng.choice(STONE)
            c.rect(bx, gy + 6 * s - bh, bx + bw, gy + 6 * s, col)
            c.rect(bx + bw * 0.74, gy + 6 * s - bh, bx + bw, gy + 6 * s, shade(col, 0.68))
        return 130 * s
    layers.append(ground_layer(tw, H, s, rng, (226, 192, 138), props))
    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": sun, "explosions": True, "plane": "bomber", "plane_color": (70, 74, 84),
           "dust": (255, 238, 200), "hooks": {"mid": [hd_stages.hook_fires], "far": [hd_stages.hook_stacks]}}
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- mission 3, a railway in the mountains
def wagon(c, x, base, s, rng, kind):
    """A goods wagon on its wheels, seen from the side. Returns its length. / Un wagon de marchandises, vu de côté."""
    L, floor = 150 * s, base - 16 * s
    for wx in (x + 22 * s, x + 46 * s, x + L - 46 * s, x + L - 22 * s):                             # wheels / roues
        c.ellipse(wx - 9 * s, base - 18 * s, wx + 9 * s, base, (34, 32, 36))
        c.ellipse(wx - 4 * s, base - 13 * s, wx + 4 * s, base - 5 * s, (86, 84, 88))
    c.rect(x, floor - 6 * s, x + L, floor, (48, 44, 46))
    c.rect(x - 8 * s, floor - 5 * s, x, floor - 1 * s, (40, 38, 40))
    c.rect(x + L, floor - 5 * s, x + L + 8 * s, floor - 1 * s, (40, 38, 40))
    if kind == "box":
        col = rng.choice(((142, 62, 46), (96, 84, 62), (74, 96, 82)))
        c.rect(x + 3 * s, floor - 70 * s, x + L - 3 * s, floor - 6 * s, col)
        c.rect(x + L - 20 * s, floor - 70 * s, x + L - 3 * s, floor - 6 * s, shade(col, 0.7))
        for px in range(int(x + 12 * s), int(x + L - 20 * s), int(11 * s)):
            c.line([(px, floor - 68 * s), (px, floor - 8 * s)], shade(col, 0.78), 0.7)
        c.rect(x + L * 0.38, floor - 62 * s, x + L * 0.62, floor - 8 * s, shade(col, 0.86))
        c.line([(x + L * 0.38, floor - 62 * s), (x + L * 0.62, floor - 8 * s)], shade(col, 0.6), 1.0)
        c.poly([(x, floor - 70 * s), (x + 8 * s, floor - 78 * s), (x + L - 8 * s, floor - 78 * s), (x + L, floor - 70 * s)], shade(col, 0.56))
        c.line([(x + 8 * s, floor - 78 * s), (x + L - 8 * s, floor - 78 * s)], shade(col, 1.2), 0.8)
    elif kind == "tank":
        col = (120, 126, 130)
        c.d.rounded_rectangle([(x + 8 * s) * SS, (floor - 58 * s) * SS, (x + L - 8 * s) * SS, (floor - 8 * s) * SS], radius=int(24 * s * SS), fill=col)
        c.d.rounded_rectangle([(x + 8 * s) * SS, (floor - 30 * s) * SS, (x + L - 8 * s) * SS, (floor - 8 * s) * SS], radius=int(20 * s * SS), fill=shade(col, 0.66))
        c.rect(x + 14 * s, floor - 54 * s, x + L - 14 * s, floor - 50 * s, shade(col, 1.24))
        c.rect(x + L * 0.44, floor - 68 * s, x + L * 0.56, floor - 56 * s, shade(col, 0.9))
        for px in (x + L * 0.25, x + L * 0.75):
            c.line([(px, floor - 58 * s), (px, floor - 8 * s)], shade(col, 0.5), 1.2)
    elif kind == "flat":
        for i in range(rng.randint(2, 4)):
            w, hh = rng.uniform(26, 40) * s, rng.uniform(22, 36) * s
            crate(c, x + 10 * s + i * 34 * s, floor - 6 * s, w, hh, s, rng.choice(((170, 128, 78), (124, 132, 92), (150, 112, 70))))
        c.rect(x + L - 44 * s, floor - 34 * s, x + L - 8 * s, floor - 6 * s, (96, 110, 80))            # a tarpaulin / une bâche
        c.poly([(x + L - 44 * s, floor - 34 * s), (x + L - 26 * s, floor - 44 * s), (x + L - 8 * s, floor - 34 * s)], (110, 124, 92))
    else:                                                                                             # an armoured wagon / blindé
        col = (92, 104, 78)
        c.poly([(x + 4 * s, floor - 6 * s), (x + 12 * s, floor - 56 * s), (x + L - 12 * s, floor - 56 * s), (x + L - 4 * s, floor - 6 * s)], col)
        c.poly([(x + L - 34 * s, floor - 56 * s), (x + L - 12 * s, floor - 56 * s), (x + L - 4 * s, floor - 6 * s), (x + L - 28 * s, floor - 6 * s)], shade(col, 0.7))
        c.rect(x + L * 0.36, floor - 78 * s, x + L * 0.64, floor - 56 * s, shade(col, 0.92))
        c.rect(x + L * 0.64, floor - 72 * s, x + L * 0.94, floor - 66 * s, (50, 54, 48))             # its gun / son canon
        for px in range(int(x + 18 * s), int(x + L - 30 * s), int(14 * s)):
            c.ellipse(px, floor - 50 * s, px + 3 * s, floor - 47 * s, shade(col, 0.6))
        c.rect(x + 24 * s, floor - 40 * s, x + 44 * s, floor - 34 * s, (30, 34, 30))
    return L + 12 * s


def build_rail(W, H, s, seed=23):
    """Mission 3. A railway in the mountains, wagons left on the tracks, the wind. / Une voie ferrée en montagne."""
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    haze = (206, 220, 226)
    sky = vgrad(W, H, [(0.0, (36, 92, 168)), (0.38, (112, 164, 214)), (0.62, (196, 216, 228)), (0.70, haze),
                       (0.76, (170, 186, 160)), (1.0, (120, 132, 100))])
    sun = (int(W * 0.30), int(H * 0.14))
    hd_bg.add_at(sky, hd_bg.radial(int(1000 * s), (40, 40, 30), 2.4), *sun)
    layers = [cloud_layer(tw, int(H * 0.58), rng, s, cover=128, stretch=2.6, k=0.8)]             # clouds drawn out by the wind
    layers.append(ridge_layer(tw, int(230 * s), rng, s, 44, (112, 132, 164), (140, 160, 180), haze, 0.5, hz - int(196 * s), 0.04,
                              peaks=7, snow=((244, 248, 252), 26), waves=5))
    layers.append(ridge_layer(tw, int(140 * s), rng, s, 26, (92, 126, 104), (120, 148, 116), haze, 0.4, hz - int(104 * s), 0.08, waves=5))
    tex = fractal(tw, int(300 * s), rng, cells=(int(90 * s) or 2, int(34 * s) or 2, int(12 * s) or 2, int(5 * s) or 2))

    h = int(230 * s)                                                             # a viaduct and pines / un viaduc, des sapins
    c = Canvas(tw, h)
    deck = h - 120 * s
    stone = (176, 168, 156)
    x0, x1 = tw * 0.12, tw * 0.62
    c.rect(x0, deck, x1, h, stone)
    c.rect(x0 - 10 * s, deck - 8 * s, x1 + 10 * s, deck, shade(stone, 1.1))
    c.rect(x0 - 10 * s, deck, x1 + 10 * s, deck + 4 * s, shade(stone, 0.66))
    n = 9
    span = (x1 - x0) / n
    for i in range(n):                                                           # its arches / ses arches
        ax = x0 + i * span + 12 * s
        aw = span - 24 * s
        c.ellipse(ax, deck + 16 * s, ax + aw, deck + 16 * s + aw, (0, 0, 0, 0))
        c.rect(ax, deck + 16 * s + aw / 2, ax + aw, h + 2, (0, 0, 0, 0))
        c.rect(ax + aw, deck + 4 * s, ax + aw + 5 * s, h, shade(stone, 0.74))
    for px in range(int(x0), int(x1), int(26 * s)):
        c.line([(px, deck - 8 * s), (px, deck - 20 * s)], (70, 66, 64), 0.7)
    c.line([(x0 - 10 * s, deck - 20 * s), (x1 + 10 * s, deck - 20 * s)], (70, 66, 64), 0.8)
    for _ in range(46):
        px = rng.uniform(0, tw)
        if x0 - 20 * s < px < x1 + 20 * s:
            continue
        pine(c, px, h, rng.uniform(60, 120) * s, s, rng, rng.choice(((48, 92, 70), (40, 80, 62), (58, 104, 76))))
    tx = tw * 0.80                                                               # a water tower / un château d'eau
    for lx in (tx, tx + 44 * s):
        c.line([(lx, h), (lx + (10 * s if lx == tx else -10 * s), h - 90 * s)], (96, 70, 50), 1.6)
    c.line([(tx, h - 40 * s), (tx + 44 * s, h - 70 * s)], (96, 70, 50), 0.8)
    c.rect(tx - 4 * s, h - 150 * s, tx + 48 * s, h - 90 * s, (150, 96, 62))
    c.rect(tx + 32 * s, h - 150 * s, tx + 48 * s, h - 90 * s, (104, 66, 46))
    c.poly([(tx - 8 * s, h - 150 * s), (tx + 22 * s, h - 172 * s), (tx + 52 * s, h - 150 * s)], (96, 60, 44))
    far = c.done(tex.resize((tw, h)), 0.14, haze, 0.40)
    layers.append({"img": far, "y": hz - h + int(26 * s), "f": 0.16, "stage": "far",
                   "stacks": [(tw * 0.34, deck - 26 * s)]})

    h = int(300 * s)                                                             # the yard / la gare de triage
    base = h - 1
    track = base - 6 * s
    c = Canvas(tw, h)
    fires = []
    for px in range(0, tw, int(170 * s)):                                        # the telegraph / le télégraphe
        c.line([(px + 20 * s, base), (px + 20 * s, base - 190 * s)], (86, 64, 46), 1.6)
        c.line([(px + 6 * s, base - 178 * s), (px + 34 * s, base - 178 * s)], (86, 64, 46), 1.2)
        c.line([(px + 20 * s, base - 178 * s), (px + 105 * s, base - 160 * s), (px + 190 * s, base - 178 * s)], (40, 40, 44), 0.5)
    x = 20 * s
    while x < tw - 520 * s:
        r = rng.random()
        if r < 0.62:                                                             # a rake of wagons / une rame
            for _ in range(rng.randint(2, 3)):
                kind = rng.choice(("box", "box", "tank", "flat", "armour"))
                if kind == "armour" and rng.random() < 0.5:
                    fires.append((x + 75 * s, track - 80 * s))
                x += wagon(c, x, track, s, rng, kind)
        elif r < 0.8:                                                            # the station / la gare
            col, w, hh = (206, 190, 160), 220 * s, 96 * s
            c.rect(x, base - hh, x + w, base, col)
            c.rect(x + w - 26 * s, base - hh, x + w, base, shade(col, 0.72))
            c.poly([(x - 14 * s, base - hh), (x + w * 0.5, base - hh - 54 * s), (x + w + 14 * s, base - hh)], (126, 70, 52))
            c.poly([(x + w * 0.5, base - hh - 54 * s), (x + w + 14 * s, base - hh), (x + w * 0.62, base - hh)], (96, 54, 42))
            c.rect(x + 30 * s, base - hh - 62 * s, x + 46 * s, base - hh - 22 * s, (150, 96, 80))
            for i in range(4):
                window(c, x + 28 * s + i * 46 * s, base - 30 * s, 16 * s, 26 * s, s, rng, col, arch=False)
            c.rect(x - 30 * s, base - hh + 24 * s, x + w + 30 * s, base - hh + 30 * s, (110, 80, 56))       # its canopy / sa marquise
            for px in (x - 26 * s, x + w + 26 * s):
                c.line([(px, base - hh + 30 * s), (px, base)], (86, 64, 46), 1.4)
            x += w + 40 * s
        else:                                                                    # a signal and pines / un signal, des sapins
            c.line([(x + 10 * s, base), (x + 10 * s, base - 150 * s)], (60, 60, 64), 1.8)
            c.poly([(x + 10 * s, base - 150 * s), (x + 58 * s, base - 132 * s), (x + 58 * s, base - 122 * s), (x + 10 * s, base - 138 * s)], (200, 50, 44))
            c.rect(x + 40 * s, base - 137 * s, x + 48 * s, base - 124 * s, (240, 236, 226))
            for i in range(rng.randint(2, 4)):
                pine(c, x + 60 * s + i * 44 * s, base, rng.uniform(110, 200) * s, s, rng)
            x += 240 * s
        x += rng.uniform(20, 80) * s
    c.rect(0, track, tw, track + 3 * s, (70, 70, 76))                            # the rail / le rail
    for px in range(0, tw, int(18 * s)):
        c.rect(px, track + 3 * s, px + 10 * s, track + 7 * s, (74, 56, 42))
    layers.append({"img": c.done(tex.resize((tw, h)), 0.18, haze, 0.08), "y": H - h - int(40 * s), "f": 0.38, "stage": "mid", "fires": some(rng, fires, FIRES)})

    def props(c, x, gy):
        r = rng.random()
        if r < 0.3:
            crate(c, x, gy + 6 * s, 36 * s, 30 * s, s, (124, 132, 92))
            crate(c, x + 40 * s, gy + 6 * s, 30 * s, 22 * s, s)
            return 80 * s
        if r < 0.55:
            for i in range(rng.randint(1, 3)):
                drum(c, x + i * 24 * s, gy, s, rng.choice(((150, 60, 44), (84, 104, 70), (70, 96, 130))))
            return 80 * s
        if r < 0.75:
            return sandbags(c, x, gy, s, rng)
        for _ in range(rng.randint(4, 8)):                                       # rocks / des rochers
            rr, rx = rng.uniform(6, 18) * s, x + rng.uniform(0, 110) * s
            col = rng.choice(((150, 146, 140), (128, 124, 122), (170, 164, 154)))
            c.poly([(rx - rr, gy + 8 * s), (rx - rr * 0.5, gy - rr * 0.7), (rx + rr * 0.5, gy - rr), (rx + rr, gy + 8 * s)], col)
            c.poly([(rx + rr * 0.1, gy - rr * 0.9), (rx + rr * 0.5, gy - rr), (rx + rr, gy + 8 * s), (rx + rr * 0.3, gy + 8 * s)], shade(col, 0.66))
        return 120 * s
    layers.append(ground_layer(tw, H, s, rng, (150, 144, 132), props, shade_k=(60, 58, 60, 100), edge=(70, 66, 62, 70)))
    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": sun, "explosions": True, "plane": "heli", "plane_color": (56, 64, 60),
           "dust": (236, 236, 226), "hooks": {"mid": [hd_stages.hook_fires], "far": [hd_stages.hook_stacks]}}
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- mission 4, a harbour town
SHOPS = ((206, 222, 196), (232, 198, 190), (226, 208, 150), (196, 214, 226), (236, 226, 204), (214, 190, 160))
BOARDS = ((196, 44, 40), (232, 190, 50), (44, 110, 84), (40, 80, 150), (236, 232, 220))


def shophouse(c, x, base, w, floors, s, rng):
    """A narrow house over its shop: balconies, washing on poles, boards hung out, with marks of our own for writing.
    / Une maison étroite sur sa boutique : balcons, linge aux perches, enseignes en drapeau."""
    col = rng.choice(SHOPS)
    fh = 44 * s
    h = 58 * s + floors * fh
    top = base - h
    c.rect(x, top, x + w, base, col)
    c.rect(x + w - 9 * s, top, x + w, base, shade(col, 0.72))
    c.rect(x - 2 * s, top - 6 * s, x + w + 2 * s, top + 2 * s, shade(col, 1.08))
    for f in range(floors):
        y = base - 58 * s - f * fh
        n = max(2, int(w / (30 * s)))
        for i in range(n):
            wx = x + (i + 0.5) * (w - 9 * s) / n
            c.rect(wx - 8 * s, y - 34 * s, wx + 8 * s, y - 8 * s, (40, 44, 52))
            c.rect(wx - 8 * s, y - 34 * s, wx + 8 * s, y - 28 * s, (70, 84, 96))
            c.line([(wx, y - 34 * s), (wx, y - 8 * s)], shade(col, 0.9), 0.7)
            if rng.random() < 0.22:                                              # a cooler / un climatiseur
                c.rect(wx - 7 * s, y - 8 * s, wx + 7 * s, y + 1 * s, (196, 198, 196))
                c.rect(wx + 2 * s, y - 8 * s, wx + 7 * s, y + 1 * s, (140, 144, 144))
        if rng.random() < 0.6:                                                   # a balcony / un balcon
            c.rect(x + 2 * s, y - 6 * s, x + w - 10 * s, y - 3 * s, shade(col, 0.6))
            for bx in range(int(x + 4 * s), int(x + w - 10 * s), int(5 * s)):
                c.line([(bx, y - 18 * s), (bx, y - 4 * s)], (60, 70, 72), 0.5)
            c.line([(x + 2 * s, y - 18 * s), (x + w - 10 * s, y - 18 * s)], (60, 70, 72), 0.8)
        if rng.random() < 0.45:                                                  # washing on a pole / du linge
            px = x + rng.uniform(0.2, 0.6) * w
            c.line([(px, y - 24 * s), (px + 40 * s, y - 28 * s)], (150, 130, 90), 0.8)
            for i in range(3):
                lc = rng.choice(((236, 232, 220), (196, 60, 50), (70, 110, 160), (220, 180, 70), (120, 170, 130)))
                c.rect(px + 6 * s + i * 11 * s, y - 27 * s, px + 14 * s + i * 11 * s, y - 13 * s, lc)
    c.rect(x + 3 * s, base - 46 * s, x + w - 12 * s, base, (36, 32, 36))                              # the shop / la boutique
    if rng.random() < 0.5:
        for yy in range(int(6 * s), int(44 * s), int(5 * s)):
            c.line([(x + 3 * s, base - yy), (x + w - 12 * s, base - yy)], (96, 100, 104), 0.7)       # its shutter / son rideau
    else:
        c.rect(x + 8 * s, base - 40 * s, x + w - 17 * s, base - 12 * s, (232, 196, 120))
        c.rect(x + 8 * s, base - 22 * s, x + w - 17 * s, base - 12 * s, (150, 110, 70))
    awning(c, x + 1 * s, base - 56 * s, w - 12 * s, s, rng)
    for _ in range(rng.randint(1, 2)):                                           # boards hung out / enseignes en drapeau
        bc = rng.choice(BOARDS)
        ink = (30, 24, 24) if sum(bc) > 420 else (244, 236, 210)
        bx, by, bh = x + rng.choice((-12, w - 2 * s / s)) * 1.0 if False else x + rng.uniform(0.05, 0.75) * w, top + rng.uniform(16, 60) * s, rng.uniform(46, 84) * s
        c.rect(bx, by, bx + 16 * s, by + bh, bc)
        c.rect(bx + 12 * s, by, bx + 16 * s, by + bh, shade(bc, 0.74))
        c.line([(bx - 4 * s, by + 2 * s), (bx + 16 * s, by + 2 * s)], (50, 50, 54), 0.8)
        for k in range(int(bh / (16 * s))):                                      # marks of our own, not writing / des marques à nous
            my = by + 6 * s + k * 16 * s
            c.rect(bx + 3 * s, my, bx + 10 * s, my + 2 * s, ink)
            c.rect(bx + 5 * s, my + 4 * s, bx + 7 * s, my + 10 * s, ink)
            if k % 2:
                c.rect(bx + 3 * s, my + 8 * s, bx + 10 * s, my + 10 * s, ink)
    return h


def build_port(W, H, s, seed=24):
    """Mission 4. A harbour town under green hills: narrow shop houses, towers, cranes and boats.
    / Une ville portuaire au pied de collines vertes : maisons étroites, tours, grues et bateaux."""
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    haze = (216, 228, 226)
    sky = vgrad(W, H, [(0.0, (48, 116, 188)), (0.42, (140, 190, 222)), (0.64, (214, 228, 228)), (0.70, haze),
                       (0.72, (96, 150, 160)), (0.82, (70, 124, 140)), (1.0, (60, 100, 116))])       # the sea under the horizon
    sun = (int(W * 0.56), int(H * 0.12))
    hd_bg.add_at(sky, hd_bg.radial(int(1000 * s), (44, 42, 30), 2.4), *sun)
    layers = [cloud_layer(tw, int(H * 0.52), rng, s, cover=134, k=0.82)]
    layers.append(ridge_layer(tw, int(260 * s), rng, s, 50, (70, 122, 96), (96, 140, 110), haze, 0.48, hz - int(210 * s), 0.04, peaks=4, waves=3))
    tex = fractal(tw, int(300 * s), rng, cells=(int(90 * s) or 2, int(34 * s) or 2, int(12 * s) or 2, int(5 * s) or 2))

    h = int(250 * s)                                                             # towers, cranes, boats / tours, grues, bateaux
    c = Canvas(tw, h)
    x = 10 * s
    while x < tw - 120 * s:
        r = rng.random()
        if r < 0.66:                                                             # a tower block / une tour d'habitation
            w, bh = rng.uniform(46, 90) * s, rng.uniform(110, 220) * s
            col = rng.choice(((214, 214, 204), (200, 190, 176), (190, 206, 210), (222, 204, 186)))
            c.rect(x, h - bh, x + w, h, col)
            c.rect(x + w - 10 * s, h - bh, x + w, h, shade(col, 0.72))
            for yy in range(int(10 * s), int(bh - 6 * s), int(11 * s)):
                for xx in range(int(5 * s), int(w - 14 * s), int(9 * s)):
                    c.rect(x + xx, h - bh + yy, x + xx + 5 * s, h - bh + yy + 6 * s, (74, 92, 104) if rng.random() < 0.85 else (236, 226, 190))
            if rng.random() < 0.5:
                c.rect(x + w * 0.3, h - bh - 12 * s, x + w * 0.6, h - bh, (120, 126, 128))
            x += w + rng.uniform(4, 30) * s
        elif r < 0.84:                                                           # a crane of the docks / une grue du port
            col = (196, 80, 50)
            for lx in (x, x + 40 * s):
                c.line([(lx, h), (lx + 6 * s, h - 130 * s)], col, 2.2)
            c.line([(x, h - 60 * s), (x + 44 * s, h - 60 * s)], col, 1.4)
            c.rect(x - 4 * s, h - 140 * s, x + 52 * s, h - 128 * s, shade(col, 0.9))
            c.line([(x + 20 * s, h - 140 * s), (x + 150 * s, h - 190 * s)], col, 2.0)
            c.line([(x + 20 * s, h - 168 * s), (x + 150 * s, h - 190 * s)], shade(col, 0.7), 0.8)
            c.line([(x + 150 * s, h - 190 * s), (x + 150 * s, h - 110 * s)], (50, 50, 54), 0.5)
            x += 170 * s
        else:                                                                    # a boat under sail / un bateau à voile
            hull = (96, 64, 46)
            c.poly([(x, h - 14 * s), (x + 110 * s, h - 14 * s), (x + 96 * s, h), (x + 14 * s, h)], hull)
            c.poly([(x + 84 * s, h - 14 * s), (x + 110 * s, h - 30 * s), (x + 110 * s, h - 14 * s)], shade(hull, 1.2))
            for mx, mh in ((x + 36 * s, 96 * s), (x + 76 * s, 70 * s)):
                c.line([(mx, h - 14 * s), (mx, h - 14 * s - mh)], (60, 44, 36), 1.2)
                sail = (176, 84, 56)
                c.poly([(mx + 2 * s, h - 20 * s), (mx + 2 * s, h - 12 * s - mh), (mx + mh * 0.42, h - 10 * s - mh * 0.84), (mx + mh * 0.5, h - 24 * s)], sail)
                for k in range(1, 5):
                    c.line([(mx + 2 * s, h - 20 * s - k * mh * 0.17), (mx + mh * 0.47, h - 24 * s - k * mh * 0.15)], shade(sail, 0.7), 0.5)
            x += 150 * s
    far = c.done(tex.resize((tw, h)), 0.10, haze, 0.42)
    layers.append({"img": far, "y": hz - h + int(26 * s), "f": 0.16, "stage": "far",
                   "stacks": [(rng.uniform(0.1, 0.9) * tw, h - rng.uniform(120, 180) * s) for _ in range(2)]})

    h = int(300 * s)                                                             # the street on the quay / la rue du quai
    base = h - 1
    c = Canvas(tw, h)
    x = 12 * s
    fires = []
    while x < tw - 230 * s:
        if rng.random() < 0.16:                                                  # a gate under tiles / un portique à tuiles
            w, red = 150 * s, (176, 46, 40)
            for px in (x + 14 * s, x + w - 26 * s):
                c.rect(px, base - 120 * s, px + 12 * s, base, red)
                c.rect(px + 8 * s, base - 120 * s, px + 12 * s, base, shade(red, 0.7))
            c.rect(x + 4 * s, base - 110 * s, x + w - 4 * s, base - 98 * s, shade(red, 0.9))
            for k, (yy, ex) in enumerate(((122, 26), (146, 12))):
                roof = (58, 120, 96)
                c.poly([(x - ex * s, base - yy * s), (x + w + ex * s, base - yy * s), (x + w + (ex - 14) * s, base - (yy + 18) * s),
                        (x - (ex - 14) * s, base - (yy + 18) * s)], roof)
                c.poly([(x - ex * s, base - yy * s), (x - (ex + 12) * s, base - (yy + 10) * s), (x - (ex - 14) * s, base - (yy + 18) * s)], shade(roof, 1.2))
                c.poly([(x + w + ex * s, base - yy * s), (x + w + (ex + 12) * s, base - (yy + 10) * s), (x + w + (ex - 14) * s, base - (yy + 18) * s)], shade(roof, 0.8))
                for tx in range(int(x - (ex - 10) * s), int(x + w + (ex - 10) * s), int(8 * s)):
                    c.line([(tx, base - yy * s), (tx + 3 * s, base - (yy + 18) * s)], shade(roof, 0.74), 0.6)
            for i in range(5):                                                   # lanterns / des lanternes
                lx = x + 30 * s + i * 22 * s
                c.ellipse(lx, base - 96 * s, lx + 10 * s, base - 82 * s, (226, 60, 44))
                c.rect(lx + 3 * s, base - 82 * s, lx + 7 * s, base - 78 * s, (236, 190, 60))
            x += w + 20 * s
            continue
        w = rng.uniform(84, 130) * s
        hh = shophouse(c, x, base, w, rng.randint(2, 4), s, rng)
        if rng.random() < 0.16:
            fires.append((x + w * 0.5, base - hh - 6 * s))
        x += w + rng.choice((0, 0, 4, 26)) * s
    c.soft([(0, base - 10 * s), (tw, base - 10 * s), (tw, base + 4), (0, base + 4)], (40, 40, 50, 120), 5 * s)
    layers.append({"img": c.done(tex.resize((tw, h)), 0.14, haze, 0.08), "y": H - h - int(40 * s), "f": 0.38, "stage": "mid", "fires": some(rng, fires, FIRES)})

    def props(c, x, gy):
        r = rng.random()
        if r < 0.3:                                                              # a bollard and its rope / une bitte d'amarrage
            c.rect(x, gy - 18 * s, x + 14 * s, gy + 6 * s, (60, 62, 68))
            c.ellipse(x - 4 * s, gy - 24 * s, x + 18 * s, gy - 12 * s, (84, 86, 92))
            c.d.ellipse([(x + 30 * s) * SS, (gy - 6 * s) * SS, (x + 62 * s) * SS, (gy + 8 * s) * SS], outline=(170, 150, 110), width=int(3 * s * SS))
            return 80 * s
        if r < 0.6:
            crate(c, x, gy + 6 * s, 38 * s, 32 * s, s)
            crate(c, x + 42 * s, gy + 6 * s, 30 * s, 24 * s, s, (124, 132, 92))
            crate(c, x + 14 * s, gy - 26 * s, 30 * s, 24 * s, s, (150, 112, 70))
            return 84 * s
        if r < 0.8:
            for i in range(rng.randint(2, 3)):
                drum(c, x + i * 24 * s, gy, s, rng.choice(((150, 60, 44), (84, 104, 70), (70, 96, 130))))
            return 80 * s
        return sandbags(c, x, gy, s, rng)
    layers.append(ground_layer(tw, H, s, rng, (156, 156, 152), props, shade_k=(50, 56, 66, 110), edge=(60, 62, 70, 70)))
    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "sun": sun, "explosions": True, "plane": "heli", "plane_color": (60, 70, 76),
           "hooks": {"mid": [hd_stages.hook_fires], "far": [hd_stages.hook_stacks]}}
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- mission 5, a big city by night
def night_block(c, x, base, w, h, s, rng, col, lights, lit=0.3, sign=True):
    """A building at night, some windows lit. The lit ones are remembered, they flicker. / Un immeuble la nuit."""
    top = base - h
    c.rect(x, top, x + w, base, col)
    c.rect(x + w - w * 0.12, top, x + w, base, shade(col, 0.7))
    c.rect(x - 2 * s, top - 4 * s, x + w + 2 * s, top + 2 * s, shade(col, 1.3))
    for yy in range(int(14 * s), int(h - 50 * s), int(26 * s)):
        for xx in range(int(8 * s), int(w * 0.86 - 12 * s), int(20 * s)):
            wx, wy = x + xx, top + yy
            r = rng.random()
            if r < lit:
                glow = rng.choice(((255, 214, 130), (255, 196, 110), (190, 220, 255)))
                c.rect(wx, wy, wx + 11 * s, wy + 15 * s, glow)
                c.rect(wx, wy + 9 * s, wx + 11 * s, wy + 15 * s, shade(glow, 0.8))
                if rng.random() < 0.3:
                    lights.append((wx + 5 * s, wy + 7 * s))
            else:
                c.rect(wx, wy, wx + 11 * s, wy + 15 * s, shade(col, 0.5))
                c.rect(wx, wy, wx + 11 * s, wy + 4 * s, shade(col, 0.8))
    if sign and rng.random() < 0.5:                                              # a lit board, nothing written / un panneau éclairé
        bc = rng.choice(((60, 220, 200), (255, 80, 150), (255, 190, 60), (110, 150, 255)))
        bw, bh = min(w * 0.7, rng.uniform(50, 90) * s), rng.uniform(18, 28) * s
        bx, by = x + (w * 0.88 - bw) / 2, top + rng.uniform(0.25, 0.6) * (h - 80 * s)
        c.soft([(bx - 8 * s, by - 8 * s), (bx + bw + 8 * s, by - 8 * s), (bx + bw + 8 * s, by + bh + 8 * s), (bx - 8 * s, by + bh + 8 * s)], bc + (90,), 6 * s)
        c.rect(bx, by, bx + bw, by + bh, shade(bc, 0.5))
        c.d.rectangle([bx * SS, by * SS, (bx + bw) * SS, (by + bh) * SS], outline=bc, width=int(2 * s * SS))
        for k in range(3):
            c.rect(bx + bw * (0.14 + k * 0.27), by + bh * 0.36, bx + bw * (0.32 + k * 0.27), by + bh * 0.64, bc)


def street_lamp(c, x, base, s, lights):
    c.line([(x, base), (x, base - 120 * s)], (50, 54, 66), 1.8)
    c.line([(x, base - 120 * s), (x + 26 * s, base - 126 * s)], (50, 54, 66), 1.4)
    c.soft([(x + 26 * s, base - 122 * s), (x + 82 * s, base), (x - 30 * s, base)], (255, 220, 150, 46), 8 * s)       # its light / sa lumière
    c.ellipse(x + 20 * s, base - 130 * s, x + 32 * s, base - 120 * s, (255, 236, 180))
    lights.append((x + 26 * s, base - 125 * s))


def build_city(W, H, s, seed=25):
    """Mission 5. The streets of a big city by night: lit windows, boards, lamps, the way down to the underground.
    / Les rues d'une grande ville la nuit : fenêtres éclairées, enseignes, réverbères, une bouche de métro."""
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    haze = (60, 58, 110)
    sky = vgrad(W, H, [(0.0, (6, 8, 30)), (0.40, (18, 24, 66)), (0.62, (48, 44, 100)), (0.70, (96, 66, 110)),
                       (0.76, (60, 44, 80)), (1.0, (22, 20, 40))])
    moon = (int(W * 0.80), int(H * 0.16))
    hd_bg.add_at(sky, hd_bg.radial(int(520 * s), (40, 46, 70), 2.0), *moon)
    d = ImageDraw.Draw(sky)
    d.ellipse([moon[0] - 22 * s, moon[1] - 22 * s, moon[0] + 22 * s, moon[1] + 22 * s], fill=(236, 238, 226))
    d.ellipse([moon[0] - 8 * s, moon[1] - 10 * s, moon[0] + 2 * s, moon[1]], fill=(214, 218, 210))
    stars = []
    for _ in range(140):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.46)
        b = int(rng.uniform(70, 210) * (1 - y / (H * 0.6)))
        d.point((x, y), fill=(b, b, min(255, b + 24)))
        if rng.random() < 0.16:
            stars.append((x, y, rng.uniform(1.5, 4.0), rng.uniform(0, 6.28)))
    layers = [cloud_layer(tw, int(H * 0.5), rng, s, cover=146, white=(70, 70, 120), grey=(30, 32, 70), k=0.6)]

    h = int(280 * s)                                                             # the towers, far / les tours au loin
    c = Canvas(tw, h)
    blinks = []
    x = 0.0
    while x < tw - 60 * s:
        w, bh = rng.uniform(50, 110) * s, rng.uniform(120, 260) * s
        col = rng.choice(((24, 28, 62), (30, 34, 72), (20, 24, 54)))
        c.rect(x, h - bh, x + w, h, col)
        c.rect(x + w * 0.86, h - bh, x + w, h, shade(col, 0.74))
        for yy in range(int(8 * s), int(bh), int(9 * s)):
            for xx in range(int(4 * s), int(w * 0.84), int(7 * s)):
                if rng.random() < 0.2:
                    c.rect(x + xx, h - bh + yy, x + xx + 3 * s, h - bh + yy + 4 * s, rng.choice(((255, 220, 140), (200, 226, 255))))
        if rng.random() < 0.4:
            c.line([(x + w * 0.5, h - bh), (x + w * 0.5, h - bh - 30 * s)], (40, 44, 80), 0.8)
            blinks.append((x + w * 0.5, h - bh - 30 * s))
        x += w + rng.uniform(-8, 26) * s
    layers.append({"img": c.done(None, 0, haze, 0.30), "y": hz - h + int(40 * s), "f": 0.07, "stage": "sky", "blinks": blinks})

    h = int(240 * s)
    c = Canvas(tw, h)
    lights = []
    x = 6 * s
    while x < tw - 130 * s:
        w, bh = rng.uniform(90, 170) * s, rng.uniform(110, 220) * s
        night_block(c, x, h, w, bh, s * 0.8, rng, rng.choice(((36, 40, 78), (44, 44, 84), (40, 50, 86))), lights, lit=0.34)
        if rng.random() < 0.3:                                                   # a water tank / un réservoir
            c.rect(x + w * 0.3, h - bh - 26 * s, x + w * 0.3 + 24 * s, h - bh - 4 * s, (40, 40, 66))
            c.poly([(x + w * 0.3 - 3 * s, h - bh - 26 * s), (x + w * 0.3 + 12 * s, h - bh - 38 * s), (x + w * 0.3 + 27 * s, h - bh - 26 * s)], (30, 30, 54))
        x += w + rng.uniform(0, 24) * s
    layers.append({"img": c.done(None, 0, haze, 0.18), "y": hz - h + int(26 * s), "f": 0.16, "stage": "far", "lights": some(rng, lights, LIGHTS),
                   "stacks": [(rng.uniform(0.1, 0.9) * tw, h - rng.uniform(140, 200) * s) for _ in range(2)]})

    tex = fractal(tw, int(300 * s), rng, cells=(int(90 * s) or 2, int(34 * s) or 2, int(12 * s) or 2, int(5 * s) or 2))
    h = int(300 * s)                                                             # the street / la rue
    base = h - 1
    c = Canvas(tw, h)
    lights, fires = [], []
    x = 10 * s
    while x < tw - 260 * s:
        if rng.random() < 0.14:                                                  # the way down to the underground / une bouche de métro
            w = 150 * s
            c.rect(x + 10 * s, base - 30 * s, x + w - 10 * s, base, (24, 22, 32))
            for i in range(6):
                c.line([(x + 14 * s, base - 4 * s - i * 5 * s), (x + w - 14 * s, base - 4 * s - i * 5 * s)], (70, 70, 84), 0.6)
            for px in (x, x + w - 6 * s):
                c.rect(px, base - 52 * s, px + 6 * s, base, (70, 96, 84))
            c.rect(x, base - 52 * s, x + w, base - 46 * s, (70, 96, 84))
            c.rect(x + w * 0.2, base - 84 * s, x + w * 0.8, base - 60 * s, (30, 60, 52))
            c.d.rectangle([(x + w * 0.2) * SS, (base - 84 * s) * SS, (x + w * 0.8) * SS, (base - 60 * s) * SS], outline=(110, 230, 170), width=int(2 * s * SS))
            c.ellipse(x + w * 0.44, base - 78 * s, x + w * 0.56, base - 66 * s, (110, 230, 170))
            for px in (x + 3 * s, x + w - 3 * s):
                c.ellipse(px - 7 * s, base - 70 * s, px + 7 * s, base - 56 * s, (150, 255, 190))
                lights.append((px, base - 63 * s))
            x += w + 30 * s
            continue
        w, bh = rng.uniform(150, 250) * s, rng.uniform(150, 270) * s
        col = rng.choice(((70, 56, 70), (58, 62, 86), (84, 62, 58), (62, 70, 80)))
        night_block(c, x, base, w, bh, s, rng, col, lights, lit=0.3)
        sw = w * 0.86                                                            # its shop, lit from inside / sa boutique éclairée
        c.rect(x + 8 * s, base - 46 * s, x + sw - 8 * s, base, (30, 26, 34))
        if rng.random() < 0.6:
            c.rect(x + 14 * s, base - 40 * s, x + sw - 40 * s, base - 8 * s, (255, 210, 130))
            c.rect(x + 14 * s, base - 20 * s, x + sw - 40 * s, base - 8 * s, (214, 160, 96))
            c.soft([(x + 8 * s, base - 4 * s), (x + sw - 30 * s, base - 4 * s), (x + sw, base + 6 * s), (x - 10 * s, base + 6 * s)], (255, 210, 130, 70), 6 * s)
            lights.append((x + sw * 0.4, base - 26 * s))
        if rng.random() < 0.45:                                                  # a fire escape / un escalier de secours
            fx = x + rng.uniform(0.15, 0.5) * w
            for k in range(int((bh - 80 * s) / (52 * s))):
                fy = base - 70 * s - k * 52 * s
                c.rect(fx, fy, fx + 56 * s, fy + 3 * s, (30, 30, 40))
                c.line([(fx, fy), (fx, fy - 16 * s)], (30, 30, 40), 0.7)
                c.line([(fx + 56 * s, fy), (fx + 56 * s, fy - 16 * s)], (30, 30, 40), 0.7)
                c.line([(fx, fy - 16 * s), (fx + 56 * s, fy - 16 * s)], (30, 30, 40), 0.7)
                c.line([(fx + 8 * s, fy), (fx + 48 * s, fy + 52 * s)], (30, 30, 40), 1.0)
        if rng.random() < 0.2:
            fires.append((x + w * 0.5, base - bh - 6 * s))
        x += w + rng.choice((0, 6, 40)) * s
    for px in range(int(90 * s), tw - int(60 * s), int(330 * s)):
        street_lamp(c, px, base, s, lights)
    c.soft([(0, base - 8 * s), (tw, base - 8 * s), (tw, base + 4), (0, base + 4)], (8, 8, 20, 130), 5 * s)
    layers.append({"img": c.done(tex.resize((tw, h)), 0.14), "y": H - h - int(40 * s), "f": 0.38, "stage": "mid", "fires": some(rng, fires, FIRES), "lights": some(rng, lights, LIGHTS)})

    def props(c, x, gy):
        r = rng.random()
        if r < 0.28:                                                             # a wreck of a car / une voiture abandonnée
            col = rng.choice(((60, 66, 96), (96, 50, 50), (70, 84, 70)))
            c.poly([(x, gy + 4 * s), (x + 4 * s, gy - 12 * s), (x + 26 * s, gy - 14 * s), (x + 40 * s, gy - 30 * s), (x + 84 * s, gy - 30 * s),
                    (x + 100 * s, gy - 14 * s), (x + 122 * s, gy - 10 * s), (x + 124 * s, gy + 4 * s)], col)
            c.poly([(x + 42 * s, gy - 27 * s), (x + 62 * s, gy - 27 * s), (x + 62 * s, gy - 15 * s), (x + 32 * s, gy - 15 * s)], (26, 30, 46))
            c.poly([(x + 66 * s, gy - 27 * s), (x + 83 * s, gy - 27 * s), (x + 94 * s, gy - 15 * s), (x + 66 * s, gy - 15 * s)], (26, 30, 46))
            for wx in (x + 26 * s, x + 98 * s):
                c.ellipse(wx - 11 * s, gy - 8 * s, wx + 11 * s, gy + 12 * s, (16, 16, 22))
                c.ellipse(wx - 5 * s, gy - 2 * s, wx + 5 * s, gy + 6 * s, (70, 70, 80))
            return 130 * s
        if r < 0.5:                                                              # a barrier / une barrière
            for i in range(2):
                bx = x + i * 62 * s
                c.rect(bx, gy - 22 * s, bx + 56 * s, gy - 12 * s, (230, 226, 214))
                for k in range(4):
                    c.poly([(bx + k * 14 * s, gy - 22 * s), (bx + k * 14 * s + 7 * s, gy - 22 * s), (bx + k * 14 * s + 1 * s, gy - 12 * s),
                            (bx + k * 14 * s - 6 * s, gy - 12 * s)], (214, 60, 44))
                c.line([(bx + 6 * s, gy - 12 * s), (bx + 2 * s, gy + 8 * s)], (60, 60, 70), 1.2)
                c.line([(bx + 50 * s, gy - 12 * s), (bx + 54 * s, gy + 8 * s)], (60, 60, 70), 1.2)
            return 124 * s
        if r < 0.72:
            return sandbags(c, x, gy, s, rng, cols=((92, 90, 80), (84, 82, 72), (100, 98, 86)))
        c.rect(x, gy - 26 * s, x + 12 * s, gy + 6 * s, (170, 50, 44))                                # a hydrant, bins / une borne, des poubelles
        c.ellipse(x - 2 * s, gy - 32 * s, x + 14 * s, gy - 20 * s, (190, 60, 50))
        for i in range(2):
            bx = x + 36 * s + i * 30 * s
            c.rect(bx, gy - 30 * s, bx + 22 * s, gy + 6 * s, (70, 76, 90))
            c.rect(bx - 2 * s, gy - 34 * s, bx + 24 * s, gy - 29 * s, (96, 102, 116))
        return 100 * s
    layers.append(ground_layer(tw, H, s, rng, (44, 44, 60), props, shade_k=(6, 6, 16, 140), edge=(10, 10, 24, 80)))
    from . import hd_stages
    amb = {"stars": stars, "horizon": hz, "explosions": True, "searchlights": [(0.24, 0.9), (0.66, 1.2)], "plane": "heli",
           "plane_color": (10, 12, 26), "window": (255, 214, 130), "blink": (255, 40, 30),
           "hooks": {"mid": [hd_stages.hook_fires], "far": [hd_stages.hook_stacks]}}
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---------------------------------------------------------------------------- mission 6, a base in the snow
SNOW = (240, 246, 252)
SNOW_SHADE = (190, 206, 228)


def snow_cap(c, x0, x1, y, s, rng, thick=7):
    """Snow lying on a roof, a drip here and there. / De la neige posée sur un toit."""
    pts = [(x0 - 3 * s, y + 1 * s)]
    n = max(3, int((x1 - x0) / (16 * s)))
    for i in range(n + 1):
        pts.append((x0 - 3 * s + i * (x1 - x0 + 6 * s) / n, y - (thick + rng.uniform(-2, 3)) * s))
    pts.append((x1 + 3 * s, y + 1 * s))
    c.poly(pts, SNOW)
    c.rect(x0 - 3 * s, y - 1 * s, x1 + 3 * s, y + 2 * s, SNOW_SHADE)


def build_base(W, H, s, seed=26):
    """Mission 6. A base in the snow under the mountains: bunkers, hangars, aerials, fences, snow falling.
    / Une base sous la neige au pied des montagnes : casemates, hangars, antennes, clôtures, la neige qui tombe."""
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.70)
    haze = (220, 228, 236)
    sky = vgrad(W, H, [(0.0, (74, 98, 134)), (0.40, (138, 160, 188)), (0.64, (206, 216, 226)), (0.71, haze),
                       (0.76, (232, 238, 244)), (1.0, (210, 220, 232))])
    layers = [cloud_layer(tw, int(H * 0.6), rng, s, cover=112, white=(226, 232, 240), grey=(150, 164, 186), k=0.86, stretch=1.6)]
    layers.append(ridge_layer(tw, int(250 * s), rng, s, 50, (104, 120, 150), (150, 166, 190), haze, 0.42, hz - int(214 * s), 0.04,
                              peaks=8, snow=(SNOW, 60), waves=5))
    h = int(150 * s)                                                             # the forest / la forêt
    c = Canvas(tw, h)
    for _ in range(150):
        pine(c, rng.uniform(0, tw), h, rng.uniform(50, 110) * s, s, rng, rng.choice(((40, 70, 64), (34, 62, 58), (48, 80, 70))), snow=SNOW)
    layers.append({"img": c.done(None, 0, haze, 0.36), "y": hz - h + int(16 * s), "f": 0.09, "stage": "sky"})
    tex = fractal(tw, int(300 * s), rng, cells=(int(90 * s) or 2, int(34 * s) or 2, int(12 * s) or 2, int(5 * s) or 2))

    h = int(240 * s)                                                             # hangars, a dish, masts / hangars, parabole, mâts
    c = Canvas(tw, h)
    stacks, blinks = [], []
    x = 10 * s
    while x < tw - 240 * s:
        r = rng.random()
        if r < 0.4:                                                              # a hangar under its round roof / un hangar
            w, hh = rng.uniform(150, 220) * s, rng.uniform(60, 84) * s
            col = (128, 138, 146)
            c.chord(x, h - hh * 2, x + w, h + hh * 0.1, 180, 360, col)
            c.chord(x + w * 0.5, h - hh * 2, x + w, h + hh * 0.1, 270, 360, shade(col, 0.76))
            c.rect(x + w * 0.3, h - hh * 0.9, x + w * 0.7, h, (60, 66, 74))
            for i in range(1, 4):
                c.line([(x + w * 0.3 + i * w * 0.1, h - hh * 0.9), (x + w * 0.3 + i * w * 0.1, h)], (84, 90, 98), 0.6)
            c.chord(x + w * 0.08, h - hh * 2 - 5 * s, x + w * 0.92, h - hh * 0.9, 200, 340, SNOW)
            x += w
        elif r < 0.62:                                                           # a dish on its tower / une parabole
            for lx in (x, x + 34 * s):
                c.line([(lx, h), (x + 17 * s, h - 120 * s)], (90, 96, 104), 1.2)
            for k in range(1, 5):
                c.line([(x + k * 3.4 * s, h - k * 24 * s), (x + 34 * s - k * 3.4 * s, h - k * 24 * s)], (90, 96, 104), 0.7)
            c.chord(x - 16 * s, h - 176 * s, x + 54 * s, h - 110 * s, 300, 120, (196, 202, 206))
            c.chord(x - 4 * s, h - 168 * s, x + 54 * s, h - 118 * s, 300, 120, (140, 148, 156))
            c.line([(x + 20 * s, h - 143 * s), (x - 14 * s, h - 160 * s)], (60, 64, 70), 0.8)
            blinks.append((x + 17 * s, h - 122 * s))
            x += 70 * s
        elif r < 0.8:                                                            # a mast and its stays / un mât haubané
            c.line([(x + 30 * s, h), (x + 30 * s, h - 200 * s)], (80, 84, 92), 1.2)
            for k in (60, 120, 180):
                c.line([(x + 30 * s, h - k * s), (x, h)], (70, 74, 82), 0.4)
                c.line([(x + 30 * s, h - k * s), (x + 60 * s, h)], (70, 74, 82), 0.4)
            blinks.append((x + 30 * s, h - 200 * s))
            x += 70 * s
        else:                                                                    # a boiler house / une chaufferie
            w, hh = 110 * s, 70 * s
            col = (150, 144, 138)
            c.rect(x, h - hh, x + w, h, col)
            c.rect(x + w * 0.86, h - hh, x + w, h, shade(col, 0.7))
            c.rect(x + w * 0.6, h - hh - 60 * s, x + w * 0.74, h - hh, (120, 110, 104))
            snow_cap(c, x, x + w, h - hh, s, rng)
            stacks.append((x + w * 0.67, h - hh - 62 * s))
            x += w
        x += rng.uniform(30, 110) * s
    layers.append({"img": c.done(tex.resize((tw, h)), 0.10, haze, 0.34), "y": hz - h + int(26 * s), "f": 0.16, "stage": "far",
                   "stacks": stacks, "blinks": blinks})

    h = int(300 * s)                                                             # the camp / le camp
    base = h - 1
    c = Canvas(tw, h)
    fires = []
    for px in range(0, tw, int(70 * s)):                                         # the fence / la clôture
        c.line([(px + 10 * s, base), (px + 10 * s, base - 84 * s)], (70, 74, 80), 1.4)
        c.line([(px + 10 * s, base - 84 * s), (px + 22 * s, base - 96 * s)], (70, 74, 80), 1.0)
    for k in (30, 52, 74):
        c.line([(0, base - k * s), (tw, base - k * s)], (96, 100, 108), 0.4)
    c.line([(0, base - 92 * s), (tw, base - 92 * s)], (96, 100, 108), 0.5)
    x = 16 * s
    while x < tw - 280 * s:
        r = rng.random()
        if r < 0.36:                                                             # a bunker / une casemate
            w, hh = rng.uniform(170, 260) * s, rng.uniform(80, 130) * s
            col = rng.choice(((150, 152, 150), (136, 140, 140), (160, 158, 150)))
            c.poly([(x, base), (x + 14 * s, base - hh), (x + w - 14 * s, base - hh), (x + w, base)], col)
            c.poly([(x + w - 44 * s, base - hh), (x + w - 14 * s, base - hh), (x + w, base), (x + w - 34 * s, base)], shade(col, 0.72))
            c.rect(x + w * 0.2, base - hh * 0.62, x + w * 0.66, base - hh * 0.5, (26, 28, 34))       # its slit / sa meurtrière
            c.rect(x + w * 0.2, base - hh * 0.5, x + w * 0.66, base - hh * 0.46, shade(col, 1.14))
            c.rect(x + w * 0.38, base - 44 * s, x + w * 0.52, base, (50, 54, 60))
            for _ in range(3):
                cx, cy = x + rng.uniform(0.15, 0.7) * w, base - rng.uniform(0.2, 0.9) * hh
                c.line([(cx, cy), (cx + rng.uniform(-8, 8) * s, cy + rng.uniform(10, 24) * s)], shade(col, 0.6), 0.7)
            snow_cap(c, x + 14 * s, x + w - 14 * s, base - hh, s, rng, 9)
            if rng.random() < 0.3:
                fires.append((x + w * 0.5, base - hh - 10 * s))
            x += w
        elif r < 0.56:                                                           # a lorry under its cover / un camion bâché
            col = (84, 100, 76)
            c.rect(x, base - 62 * s, x + 110 * s, base - 16 * s, shade(col, 1.1))
            c.rect(x + 86 * s, base - 62 * s, x + 110 * s, base - 16 * s, shade(col, 0.8))
            for k in range(1, 5):
                c.line([(x + k * 22 * s, base - 62 * s), (x + k * 22 * s, base - 16 * s)], shade(col, 0.8), 0.6)
            c.poly([(x + 114 * s, base - 16 * s), (x + 114 * s, base - 50 * s), (x + 140 * s, base - 50 * s), (x + 156 * s, base - 30 * s),
                    (x + 156 * s, base - 16 * s)], col)
            c.poly([(x + 120 * s, base - 46 * s), (x + 138 * s, base - 46 * s), (x + 150 * s, base - 32 * s), (x + 120 * s, base - 32 * s)], (40, 50, 60))
            for wx in (x + 24 * s, x + 80 * s, x + 136 * s):
                c.ellipse(wx - 13 * s, base - 26 * s, wx + 13 * s, base, (26, 26, 30))
                c.ellipse(wx - 5 * s, base - 18 * s, wx + 5 * s, base - 8 * s, (90, 90, 96))
            snow_cap(c, x, x + 110 * s, base - 62 * s, s, rng, 6)
            x += 170 * s
        elif r < 0.72:                                                           # tanks of fuel / des cuves
            for i in range(rng.randint(1, 2)):
                tx = x + i * 84 * s
                col = (170, 176, 180)
                c.rect(tx, base - 90 * s, tx + 72 * s, base, col)
                c.rect(tx + 50 * s, base - 90 * s, tx + 72 * s, base, shade(col, 0.7))
                c.rect(tx + 4 * s, base - 90 * s, tx + 12 * s, base, shade(col, 1.12))
                for k in (30, 60):
                    c.line([(tx, base - k * s), (tx + 72 * s, base - k * s)], shade(col, 0.6), 0.8)
                c.ellipse(tx, base - 98 * s, tx + 72 * s, base - 82 * s, SNOW)
            x += 170 * s
        elif r < 0.86:                                                           # a watchtower / un mirador
            for lx in (x, x + 50 * s):
                c.line([(lx, base), (lx + (8 * s if lx == x else -8 * s), base - 150 * s)], (96, 76, 56), 1.8)
            c.line([(x, base - 50 * s), (x + 50 * s, base - 100 * s)], (96, 76, 56), 0.9)
            c.line([(x + 50 * s, base - 50 * s), (x, base - 100 * s)], (96, 76, 56), 0.9)
            c.rect(x - 4 * s, base - 186 * s, x + 54 * s, base - 150 * s, (120, 96, 70))
            c.rect(x + 2 * s, base - 180 * s, x + 48 * s, base - 164 * s, (30, 32, 40))
            c.poly([(x - 12 * s, base - 186 * s), (x + 25 * s, base - 206 * s), (x + 62 * s, base - 186 * s)], (84, 66, 52))
            c.poly([(x - 8 * s, base - 188 * s), (x + 25 * s, base - 208 * s), (x + 58 * s, base - 188 * s), (x + 25 * s, base - 196 * s)], SNOW)
            x += 80 * s
        else:
            for i in range(rng.randint(2, 4)):
                pine(c, x + i * 50 * s, base, rng.uniform(120, 210) * s, s, rng, (44, 78, 68), snow=SNOW)
            x += 180 * s
        x += rng.uniform(30, 90) * s
    c.soft([(0, base - 12 * s), (tw, base - 12 * s), (tw, base + 4), (0, base + 4)], (120, 140, 170, 120), 5 * s)
    layers.append({"img": c.done(tex.resize((tw, h)), 0.12, haze, 0.08), "y": H - h - int(40 * s), "f": 0.38, "stage": "mid", "fires": some(rng, fires, FIRES)})

    def props(c, x, gy):
        r = rng.random()
        if r < 0.3:                                                              # steel against tanks / des hérissons
            for i in range(rng.randint(2, 3)):
                bx = x + i * 50 * s
                for (a, b) in (((bx, gy + 6 * s), (bx + 34 * s, gy - 26 * s)), ((bx + 34 * s, gy + 6 * s), (bx, gy - 26 * s)),
                               ((bx + 17 * s, gy + 8 * s), (bx + 17 * s, gy - 30 * s))):
                    c.line([a, b], (70, 72, 80), 3.0)
                    c.line([(a[0] - 1 * s, a[1] - 1 * s), (b[0] - 1 * s, b[1] - 1 * s)], (130, 134, 142), 0.8)
            return 150 * s
        if r < 0.55:
            return sandbags(c, x, gy, s, rng, cols=((150, 150, 140), (138, 140, 132), (160, 160, 150)), cap=SNOW)
        if r < 0.78:
            for i in range(rng.randint(1, 3)):
                drum(c, x + i * 24 * s, gy, s, rng.choice(((150, 60, 44), (84, 104, 70), (70, 96, 130))))
                c.ellipse(x + i * 24 * s, gy - 36 * s, x + i * 24 * s + 20 * s, gy - 27 * s, SNOW)
            return 80 * s
        crate(c, x, gy + 6 * s, 38 * s, 30 * s, s, (124, 132, 92))
        c.rect(x - 2 * s, gy - 28 * s, x + 40 * s, gy - 23 * s, SNOW)
        return 60 * s
    layers.append(ground_layer(tw, H, s, rng, (236, 242, 250), props, tex=0.07, shade_k=(150, 170, 204, 110), edge=(150, 170, 204, 90)))
    from . import hd_stages
    amb = {"stars": (), "horizon": hz, "snow": True, "explosions": True, "plane": "heli", "plane_color": (60, 66, 76),
           "blink": (255, 40, 30), "hooks": {"mid": [hd_stages.hook_fires], "far": [hd_stages.hook_stacks]}}
    sky, layers = settled(sky, layers, W)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ---- BUILDERS (at the end of the module / à la fin du module)
PLACES = {"ms_town": build_town, "ms_ruins": build_ruins, "ms_rail": build_rail, "ms_port": build_port, "ms_city": build_city,
          "ms_base": build_base}
hd_bg.BUILDERS.update(PLACES)
