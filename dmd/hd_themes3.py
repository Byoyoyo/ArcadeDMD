"""HD backdrops of the third batch of Neo Geo games done one by one (1.19): the four planets of Top Hunter (forest,
ice, wind, fire) with their two lanes, a ballpark at dusk for Baseball Stars 2, a ruined city at night for Last
Resort, and seen from above, the sea and its islands for Aero Fighters 2 and the countryside for Aero Fighters 3.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported.

Décors HD du troisième lot (1.19) : les quatre planètes de Top Hunter (forêt, glace, vent, feu) avec leurs deux
voies, un stade de baseball au crépuscule pour Baseball Stars 2, une ville en ruine la nuit pour Last Resort, et vues
du ciel, la mer et ses îles pour Aero Fighters 2 et la campagne pour Aero Fighters 3. Tout est dessiné par le
programme, aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from . import hd_bg
from .hd_bg import Sil, add_at, aurora_img, mix, paint, periodic, radial, vgrad
from .hd_themes2 import _stars_sky, hook_embers

TH_GROUND = 160            # height of Top Hunter's lanes above the bottom of the screen (pixels at s = 1)
TH_HEAD = 90               # room above the lanes in the ground picture (stumps, signposts) / place au-dessus des voies
TH_FEET = (128, 22)        # feet of the characters above the bottom: back lane, front lane
TH_LANES = (6, 44, 60)     # in the ground picture, from the top of the lanes: back lane, face of the ledge, front lane


def _shifts(tw, x0, x1):
    """Where a shape from x0 to x1 has to be drawn again so that the picture repeats without a seam."""
    return [dx for dx in (-tw, 0, tw) if x1 + dx >= -2 and x0 + dx <= tw + 2]


def _blob(cx, cy, rx, ry, rng, n=28, rough=0.18):
    """Round shape with an uneven edge (island, bush, cloud). / Forme ronde au bord irrégulier."""
    waves = [(rng.randint(2, 5), rng.uniform(0, math.tau), rng.uniform(0.3, 1.0)) for _ in range(3)]
    pts = []
    for i in range(n):
        a = i * math.tau / n
        k = 1 + rough * sum(w * math.sin(f * a + p) for f, p, w in waves) / 2
        pts.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    return pts


# ---------------------------------------------------------------------------- Top Hunter
class _Pic:
    """A picture drawn k times bigger then reduced (smooth edges), that repeats every tw pixels.
    / Une image dessinée en plus grand puis réduite, qui se répète sans couture."""

    def __init__(self, W, h, k=2, tw=None):
        self.W, self.h, self.k, self.tw = W, int(h), k, tw or W
        self.img = Image.new("RGBA", (W * k, self.h * k), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def _xs(self, xs):
        return _shifts(self.tw, min(xs), max(xs))

    def poly(self, pts, fill, outline=None, width=0):
        k = self.k
        for dx in self._xs([p[0] for p in pts]):
            q = [((x + dx) * k, y * k) for x, y in pts]
            self.d.polygon(q, fill=fill)
            if outline is not None:
                self.d.line(q + [q[0]], fill=outline, width=max(1, int(width * k)), joint="curve")

    def ellipse(self, x0, y0, x1, y1, fill, outline=None, width=0):
        k = self.k
        for dx in self._xs([x0, x1]):
            self.d.ellipse([(x0 + dx) * k, y0 * k, (x1 + dx) * k, y1 * k], fill=fill, outline=outline,
                           width=max(1, int(width * k)) if outline is not None else 0)

    def disc(self, x, y, r, fill, outline=None, width=0):
        self.ellipse(x - r, y - r, x + r, y + r, fill, outline, width)

    def line(self, pts, fill, width):
        k = self.k
        for dx in self._xs([p[0] for p in pts]):
            self.d.line([((x + dx) * k, y * k) for x, y in pts], fill=fill, width=max(1, int(width * k)), joint="curve")

    def chord(self, x0, y0, x1, y1, a0, a1, fill):
        k = self.k
        for dx in self._xs([x0, x1]):
            self.d.chord([(x0 + dx) * k, y0 * k, (x1 + dx) * k, y1 * k], a0, a1, fill=fill)

    def done(self):
        return self.img.resize((self.W, self.h), Image.LANCZOS)


def _fit(layers):
    """Crops each layer to the rows it uses (cheaper to draw), its lights follow. / Recadre chaque couche sur ce qu'elle montre."""
    for L in layers:
        img = L.get("img")
        if img is None or img.mode != "RGBA":
            continue
        box = img.getchannel("A").getbbox()
        if not box or (box[1] == 0 and box[3] == img.height):
            continue
        top = box[1]
        L["img"] = img.crop((0, top, img.width, box[3]))
        L["y"] = L["y"] + top
        for key in ("lights", "blinks"):
            if L.get(key):
                L[key] = [(x, y - top) for x, y in L[key]]
    return layers


def _rgba(c, a=255):
    return tuple(c[:3]) + (a,)


def _clump(p, cx, cy, r, rng, tones, n=9, spread=(1.2, 0.8)):
    """Cartoon clump of leaves: dark balls, lighter balls a little higher, light spots on top.
    / Touffe de feuillage façon dessin animé : boules sombres, plus claires au-dessus, reflets."""
    balls = []
    for _ in range(n):
        a, dd = rng.uniform(0, math.tau), rng.uniform(0, 0.72) * r
        balls.append((cx + math.cos(a) * dd * spread[0], cy + math.sin(a) * dd * spread[1], rng.uniform(0.36, 0.6) * r))
    balls.sort(key=lambda b: b[1])
    passes = ((tones[0], 0.0, 0.0, 1.0), (tones[1], -0.1, -0.16, 0.84))
    if len(tones) > 2:
        passes += ((tones[2], -0.22, -0.32, 0.5),)
    for col, ox, oy, sc in passes:
        for bx, by, br in balls:
            p.disc(bx + ox * br, by + oy * br, br * sc, _rgba(col))
    return balls


def _leaf(p, x, y, ang, ln, wd, col, vein=None):
    """A pointed leaf from (x, y), turned ang degrees (0 = right, 90 = down). / Une feuille pointue."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    p.poly([(x, y), (x + ux * ln * 0.45 + nx * wd / 2, y + uy * ln * 0.45 + ny * wd / 2), (x + ux * ln, y + uy * ln),
            (x + ux * ln * 0.45 - nx * wd / 2, y + uy * ln * 0.45 - ny * wd / 2)], _rgba(col))
    if vein is not None:
        p.line([(x, y), (x + ux * ln * 0.8, y + uy * ln * 0.8)], _rgba(vein), max(1.0, wd * 0.1))


def _vine(p, x, y, ln, rng, s, col, leaf, light):
    """A vine hanging from (x, y), small leaves on both sides. / Une liane qui pend, avec des petites feuilles."""
    pts = []
    sway, ph = rng.uniform(4, 10) * s, rng.uniform(0, math.tau)
    for i in range(13):
        t = i / 12
        pts.append((x + math.sin(t * 5 + ph) * sway * t, y + ln * t))
    p.line(pts, _rgba(col), 2.4 * s)
    for i, (px, py) in enumerate(pts[1:-1]):
        side = 1 if i % 2 else -1
        _leaf(p, px, py, 90 - side * rng.uniform(40, 70), rng.uniform(9, 15) * s, rng.uniform(5, 8) * s, light if i % 3 == 0 else leaf)


def _cumulus(W, h, s, rng, n, tones, y0, y1, size=(70, 130)):
    """Big round clouds: shade underneath, white body, light on top. / Gros nuages ronds."""
    p = _Pic(W, h)
    for _ in range(n):
        cx, cy = rng.uniform(0, W), rng.uniform(y0, y1)
        w = rng.uniform(*size) * s
        balls = []
        x = cx - w
        while x < cx + w:
            r = rng.uniform(0.32, 0.55) * w * (1.0 - 0.5 * abs(x - cx) / w)
            balls.append((x, cy - r * 0.5, r))
            x += r * rng.uniform(0.7, 1.1)
        p.ellipse(cx - w * 1.05, cy - w * 0.12, cx + w * 1.05, cy + w * 0.16, _rgba(tones[2]))
        for col, oy, sc in ((tones[2], 0.12, 1.0), (tones[1], 0.0, 0.96), (tones[0], -0.1, 0.8)):
            for bx, by, br in balls:
                p.disc(bx - 0.06 * br * (sc < 0.9), by + oy * br, br * sc, _rgba(col))
    return p.done()


def _rock_isles(W, s, rng, y_top, n, rock, rock_d, grass, grass_l, leaves, water=True):
    """Floating rocks with grass and small trees on top, layers of rock underneath, a waterfall now and then.
    Returns the picture and its top. / Rochers qui flottent, herbe et petits arbres dessus, parfois une cascade."""
    y0 = int(y_top - 70 * s)
    p = _Pic(W, 260 * s)
    span = W / n
    for i in range(n):
        cx = span * (i + rng.uniform(0.2, 0.8))
        w = rng.uniform(80, 140) * s
        top = y_top + rng.uniform(-20, 30) * s - y0
        depth = w * rng.uniform(0.7, 1.0)
        tip = cx + rng.uniform(-0.25, 0.25) * w
        left, right = [], []
        for j in range(8):
            t = j / 7
            y = top + depth * t
            half = w * (1 - t ** 1.4) * rng.uniform(0.86, 1.04) if j < 7 else 0
            left.append((tip + (cx - w - tip) * (1 - t) + rng.uniform(-6, 6) * s * (0 < j < 7) if j < 7 else tip, y))
            right.append((tip + (cx + w - tip) * (1 - t) - rng.uniform(-6, 6) * s * (0 < j < 7) if j < 7 else tip, y))
            if j < 7:
                left[-1] = (min(left[-1][0], tip - half * 0.2), y)
                right[-1] = (max(right[-1][0], tip + half * 0.2), y)
        body = left + list(reversed(right))
        p.poly(body, _rgba(rock), (30, 24, 30, 255), 2.2 * s)
        p.poly([(tip + w * 0.15, top)] + [pt for pt in right] + [(tip, top + depth)], _rgba(rock_d))      # côté à l'ombre
        for j in range(1, 5):                                                    # couches de roche
            t = j / 5
            yy = top + depth * t * 0.9
            hw = w * (1 - t ** 1.4) * 0.9
            p.line([(tip - hw, yy), (tip - hw * 0.3, yy + 4 * s), (tip + hw * 0.4, yy - 2 * s), (tip + hw, yy + 3 * s)],
                   _rgba(rock_d if j % 2 else mix(rock_d, (0, 0, 0), 0.2)), 2.2 * s)
        p.ellipse(cx - w * 1.04, top - 9 * s, cx + w * 1.04, top + 11 * s, _rgba(grass))                  # herbe
        p.ellipse(cx - w * 0.96, top - 9 * s, cx + w * 0.9, top + 3 * s, _rgba(grass_l))
        for k in range(int(w / (9 * s))):                                        # herbe qui retombe
            x = cx - w + k * 18 * s + rng.uniform(-3, 3) * s
            if abs(x - cx) < w * 0.98:
                p.poly([(x - 5 * s, top + 6 * s), (x + 5 * s, top + 6 * s), (x + rng.uniform(-2, 2) * s, top + rng.uniform(12, 22) * s)],
                       _rgba(grass))
        for k in range(rng.randint(2, 3)):                                       # petits arbres
            tx = cx + rng.uniform(-0.7, 0.7) * w
            th = rng.uniform(18, 34) * s
            p.poly([(tx - 3 * s, top), (tx + 3 * s, top), (tx + 2 * s, top - th), (tx - 2 * s, top - th)], (110, 76, 46, 255))
            _clump(p, tx, top - th - 8 * s, rng.uniform(16, 26) * s, rng, leaves, n=6)
        if water and rng.random() < 0.6:                                         # cascade
            wx = cx + rng.choice((-1, 1)) * w * 0.7
            p.poly([(wx - 6 * s, top + 2 * s), (wx + 6 * s, top + 2 * s), (wx + 9 * s, top + 200 * s), (wx - 9 * s, top + 200 * s)],
                   (200, 236, 255, 150))
            p.line([(wx - 2 * s, top + 4 * s), (wx - 3 * s, top + 190 * s)], (255, 255, 255, 170), 2 * s)
    img = p.done()
    fade = Image.linear_gradient("L").resize((W, img.height))                    # la cascade se perd dans la brume
    fade = fade.point(lambda v: 255 if v < 150 else max(0, 255 - (v - 150) * 255 // 105))
    img.putalpha(ImageChops.multiply(img.getchannel("A"), fade))
    return img, y0


def _crowns(W, h, s, rng, y, tones, size=(40, 80)):
    """Far away trees: round crowns side by side, solid below. / Forêt lointaine : couronnes rondes serrées."""
    p = _Pic(W, h)
    p.poly([(0, y + 30 * s), (W, y + 30 * s), (W, h), (0, h)], _rgba(tones[0]))
    x = 0.0
    while x < W:
        r = rng.uniform(*size) * s
        cy = y + rng.uniform(-14, 18) * s
        p.disc(x, cy + r * 0.3, r, _rgba(tones[0]))
        p.disc(x - r * 0.18, cy + r * 0.1, r * 0.78, _rgba(tones[1]))
        p.disc(x - r * 0.3, cy - r * 0.05, r * 0.4, _rgba(tones[2]))
        x += r * rng.uniform(0.9, 1.4)
    return p.done()


def _trunks(W, H, s, rng, base, bark, leaves, vine, gap=(380, 560)):
    """Big jungle trees whose tops go up into the leaves at the top of the screen: bark, roots, a branch with leaves,
    vines. / Grands arbres de la jungle qui montent jusqu'au feuillage du haut."""
    p = _Pic(W, base + 30 * s)
    light, mid, dark = bark
    x = rng.uniform(0, 200) * s
    while x < W:
        w = rng.uniform(26, 38) * s
        bend, ph = rng.uniform(6, 16) * s, rng.uniform(0, math.tau)

        def cx(y):
            return x + math.sin(y / (H * 0.7) * math.pi + ph) * bend
        ys = [base - (base + 20 * s) * i / 12 for i in range(13)]
        left = [(cx(y) - w * (1 + 0.35 * (1 - (base - y) / base) ** 6), y) for y in ys]
        right = [(cx(y) + w * (1 + 0.35 * (1 - (base - y) / base) ** 6), y) for y in ys]
        for side in (-1, 1):                                                    # racines
            for k in range(2):
                rx = cx(base) + side * w * (0.6 + 0.5 * k)
                p.poly([(rx - 8 * s, base - 40 * s), (rx + 8 * s, base - 40 * s), (rx + side * (30 + 20 * k) * s, base + 4 * s),
                        (rx + side * (6 + 10 * k) * s, base + 4 * s)], _rgba(mid), (40, 26, 18, 255), 2 * s)
        p.poly(left + list(reversed(right)), _rgba(mid), (40, 26, 18, 255), 2.4 * s)
        p.poly([(px + w * 0.25, py) for px, py in left] + list(reversed([(px - w * 0.95, py) for px, py in right])), _rgba(light))
        p.poly([(px - w * 0.35, py) for px, py in right] + list(reversed(right)), _rgba(dark))
        for k in range(6):                                                      # écorce
            t = rng.uniform(-0.7, 0.7)
            y0 = rng.uniform(0.05, 0.9) * base
            ln = rng.uniform(40, 110) * s
            p.line([(cx(y0) + t * w, y0), (cx(y0 + ln / 2) + t * w + 2 * s, y0 + ln / 2), (cx(y0 + ln) + t * w, y0 + ln)], _rgba(dark),
                   2 * s)
        if rng.random() < 0.8:                                                  # une branche feuillue
            side = rng.choice((-1, 1))
            by = rng.uniform(0.35, 0.6) * base
            bx = cx(by) + side * w * 0.8
            ex, ey = bx + side * rng.uniform(70, 110) * s, by - rng.uniform(30, 60) * s
            p.line([(bx, by), ((bx + ex) / 2, by - 4 * s), (ex, ey)], _rgba(mid), 10 * s)
            _clump(p, ex, ey - 6 * s, rng.uniform(34, 48) * s, rng, leaves, n=8)
            _vine(p, ex + rng.uniform(-14, 14) * s, ey + 18 * s, rng.uniform(50, 110) * s, rng, s, vine[0], vine[1], vine[2])
        for k in range(rng.randint(0, 2)):                                      # une liane enroulée
            y0 = rng.uniform(0.2, 0.7) * base
            p.line([(cx(y0) - w, y0), (cx(y0) + w * 0.4, y0 + 14 * s), (cx(y0) + w, y0 + 30 * s)], _rgba(vine[0]), 4 * s)
        x += rng.uniform(*gap) * s
    return p.done()


def _bushes(W, h, s, rng, tones, flowers=None, size=(30, 52)):
    """A row of round bushes behind the back lane, flowers here and there. / Une rangée de buissons ronds."""
    p = _Pic(W, h)
    x = 0.0
    while x < W:
        r = rng.uniform(*size) * s
        balls = _clump(p, x, h - r * 0.75, r, rng, tones, n=7, spread=(1.3, 0.7))
        if flowers and rng.random() < 0.5:
            for bx, by, br in rng.sample(balls, min(3, len(balls))):
                col = rng.choice(flowers)
                fx_, fy_ = bx + rng.uniform(-0.4, 0.4) * br, by + rng.uniform(-0.4, 0.2) * br
                for j in range(5):
                    a = j * math.tau / 5
                    p.disc(fx_ + math.cos(a) * 3.2 * s, fy_ + math.sin(a) * 3.2 * s, 2.6 * s, _rgba(col))
                p.disc(fx_, fy_, 2 * s, (255, 230, 120, 255))
        x += r * rng.uniform(0.8, 1.2)
    return p.done()


def _mounds(W, h, s, rng, tones, size=(80, 200), tall=(18, 46), grass=None):
    """A row of smooth mounds (snow drifts, hills): shade at the bottom, light on top. / Bosses lisses : congères, collines."""
    p = _Pic(W, h)
    x = rng.uniform(0, 60) * s
    while x < W:
        w, hh = rng.uniform(*size) * s / 2, rng.uniform(*tall) * s
        y = h - rng.uniform(0, 10) * s
        p.chord(x - w, y - hh, x + w, y + hh, 180, 360, _rgba(tones[0]))
        p.chord(x - w * 0.94, y - hh * 0.96, x + w * 0.9, y + hh * 0.5, 180, 360, _rgba(tones[1]))
        p.chord(x - w * 0.7, y - hh * 0.9, x + w * 0.2, y - hh * 0.2, 180, 360, _rgba(tones[2]))
        if grass:
            for k in range(int(w / (7 * s))):
                gx = x - w * 0.9 + k * 14 * s
                t = (gx - x) / w
                gy = y - hh * math.sqrt(max(0.0, 1 - t * t)) + 2 * s
                p.poly([(gx - 2 * s, gy), (gx + 2 * s, gy), (gx - rng.uniform(6, 12) * s, gy - rng.uniform(6, 12) * s)], _rgba(rng.choice(grass)))
        x += w * rng.uniform(0.9, 1.5)
    return p.done()


def _crags(W, h, s, rng, tones, rim, glow=None):
    """A row of jagged rocks with a hot rim, lava glowing at their foot. / Rochers déchiquetés, lave au pied."""
    p = _Pic(W, h)
    x = rng.uniform(0, 60) * s
    while x < W:
        w, hh = rng.uniform(30, 70) * s, rng.uniform(26, 70) * s
        base = h - rng.uniform(0, 8) * s
        n = rng.randint(4, 6)
        pts = [(x - w, base)]
        for i in range(1, n):
            t = i / n
            pts.append((x - w + 2 * w * t + rng.uniform(-6, 6) * s, base - hh * (0.45 + 0.55 * math.sin(t * math.pi)) * rng.uniform(0.75, 1.1)))
        pts.append((x + w, base))
        p.poly(pts, _rgba(tones[0]), _rgba(tones[2]), 2 * s)
        p.poly(pts[:max(2, n // 2 + 1)] + [(x - w * 0.2, base)], _rgba(tones[1]))
        p.line(pts[1:-1], _rgba(rim), 1.8 * s)
        if glow:
            p.line([(x - w * 0.8, base - 2 * s), (x + w * 0.8, base - 2 * s)], _rgba(glow), 4 * s)
        x += w * rng.uniform(1.0, 1.7)
    return p.done()


def th_ground(W, s, rng, back, face, front, lip, specks, deco=None):
    """The two lanes seen from the side, with room above for the things standing on the back lane: the back lane on a
    ledge, the face of the ledge, the front lane below. back, face, front: (top color, bottom color).
    / Les deux voies : celle du fond sur une corniche, la face de la corniche, celle de devant."""
    head = TH_HEAD * s
    h = int((TH_GROUND + TH_HEAD) * s)
    out = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    bands = [(head + y * s, a * s, c) for y, a, c in zip(TH_LANES, (3, 2.5, 2), (back, face, front))]
    for i, (top, amp, (c0, c1)) in enumerate(bands):
        c = Sil(W, h, s)
        f = periodic(W, rng, 4, 1.0)
        c.poly([(0, h)] + [(x, top + amp * f(x)) for x in range(0, W + 12, 12)] + [(W, h)])
        end = bands[i + 1][0] if i + 1 < len(bands) else h
        out = Image.alpha_composite(out, paint(c.mask(), [(0, c0), (top / h, c0), (end / h, c1), (1, c1)], rim=lip,
                                               rim_px=max(1, int(3 * s))))
    d = ImageDraw.Draw(out)
    for _ in range(int(W / (5 * s))):                                     # petits cailloux et touffes sur les deux voies
        lane = rng.random() < 0.4
        y = head + (rng.uniform(12, 40) if lane else rng.uniform(70, TH_GROUND - 4)) * s
        x = rng.uniform(0, W)
        r = rng.uniform(1.0, 3.2) * s * (0.8 if lane else 1.0)
        col = rng.choice(specks) + (255,)
        for dx in _shifts(W, x - r, x + r):
            d.ellipse([x + dx - r * 1.6, y - r * 0.6, x + dx + r * 1.6, y + r * 0.6], fill=col)
    if deco:
        p = _Pic(W, h)
        deco(p, W, h, head, s, rng)
        out = Image.alpha_composite(out, p.done())
    return out


def _tufts(p, W, y0, s, rng, cols, k=1.0, gap=(40, 140), bend=0.0):
    """Tufts of grass along a line. / Touffes d'herbe le long d'une ligne."""
    x = rng.uniform(0, 40) * s
    while x < W:
        for i in range(rng.randint(3, 6)):
            xx = x + i * 3.2 * s
            hh = rng.uniform(6, 14) * s * k
            lean = rng.uniform(-4, 4) * s + bend * hh
            p.poly([(xx - 2.2 * s, y0 + 2 * s), (xx + lean, y0 - hh), (xx + 2.2 * s, y0 + 2 * s)], _rgba(mix(cols[0], cols[1], rng.random())))
        x += rng.uniform(*gap) * s


def _stump(p, x, y, s, rng, wood, cut, dark):
    w, hh = rng.uniform(17, 24) * s, rng.uniform(16, 30) * s
    for side in (-1, 1):
        p.poly([(x + side * w * 0.6, y - 10 * s), (x + side * (w + 12 * s), y + 3 * s), (x + side * w * 0.4, y + 3 * s)], _rgba(wood), _rgba(dark), 1.6 * s)
    p.poly([(x - w, y - hh), (x + w, y - hh), (x + w, y), (x - w, y)], _rgba(wood), _rgba(dark), 1.8 * s)
    p.poly([(x + w * 0.35, y - hh), (x + w, y - hh), (x + w, y), (x + w * 0.35, y)], _rgba(mix(wood, (0, 0, 0), 0.25)))
    p.ellipse(x - w, y - hh - w * 0.32, x + w, y - hh + w * 0.32, _rgba(cut), _rgba(dark), 1.6 * s)
    p.ellipse(x - w * 0.55, y - hh - w * 0.17, x + w * 0.55, y - hh + w * 0.17, None, _rgba(mix(cut, dark, 0.4)), 1.4 * s)


def _log(p, x, y, s, rng, wood, cut, dark):
    ln, r = rng.uniform(60, 100) * s, rng.uniform(10, 14) * s
    p.poly([(x - ln / 2, y - 2 * r), (x + ln / 2, y - 2 * r), (x + ln / 2, y), (x - ln / 2, y)], _rgba(wood), _rgba(dark), 1.6 * s)
    p.line([(x - ln / 2 + 4 * s, y - r * 1.4), (x + ln / 2 - 10 * s, y - r * 1.5)], _rgba(mix(wood, (255, 255, 255), 0.25)), 2 * s)
    p.line([(x - ln / 2 + 8 * s, y - r * 0.6), (x + ln / 2 - 14 * s, y - r * 0.5)], _rgba(dark), 1.4 * s)
    p.ellipse(x + ln / 2 - r * 0.6, y - 2 * r, x + ln / 2 + r * 0.6, y, _rgba(cut), _rgba(dark), 1.6 * s)
    p.ellipse(x + ln / 2 - r * 0.3, y - r * 1.4, x + ln / 2 + r * 0.3, y - r * 0.6, None, _rgba(mix(cut, dark, 0.4)), 1.2 * s)


def _rock(p, x, y, s, rng, col, light, dark, size=1.0):
    w, hh = rng.uniform(16, 30) * s * size, rng.uniform(12, 22) * s * size
    pts = [(x - w, y), (x - w * 0.8, y - hh * 0.6), (x - w * 0.3, y - hh), (x + w * 0.4, y - hh * 0.9), (x + w, y - hh * 0.3), (x + w * 0.9, y)]
    p.poly(pts, _rgba(col), _rgba(dark), 1.6 * s)
    p.poly([(x - w * 0.7, y - hh * 0.55), (x - w * 0.3, y - hh * 0.9), (x + w * 0.2, y - hh * 0.85), (x - w * 0.2, y - hh * 0.5)], _rgba(light))


def _sign(p, x, y, s, wood, dark, paint_col):
    p.poly([(x - 4 * s, y + 2 * s), (x + 4 * s, y + 2 * s), (x + 4 * s, y - 62 * s), (x - 4 * s, y - 62 * s)], _rgba(wood), _rgba(dark), 1.6 * s)
    p.poly([(x - 34 * s, y - 70 * s), (x + 26 * s, y - 70 * s), (x + 40 * s, y - 58 * s), (x + 26 * s, y - 46 * s), (x - 34 * s, y - 46 * s)],
           _rgba(mix(wood, (255, 255, 255), 0.15)), _rgba(dark), 1.8 * s)
    p.line([(x - 30 * s, y - 58 * s), (x + 22 * s, y - 58 * s)], _rgba(mix(wood, (0, 0, 0), 0.2)), 1.2 * s)
    p.poly([(x - 22 * s, y - 61 * s), (x + 6 * s, y - 61 * s), (x + 6 * s, y - 66 * s), (x + 20 * s, y - 58 * s), (x + 6 * s, y - 50 * s),
            (x + 6 * s, y - 55 * s), (x - 22 * s, y - 55 * s)], _rgba(paint_col))                       # flèche peinte
    for nx in (-28, 18):
        p.disc(x + nx * s, y - 58 * s, 1.6 * s, _rgba(dark))


def _mushroom(p, x, y, s, rng, cap):
    r = rng.uniform(6, 10) * s
    p.poly([(x - r * 0.35, y), (x + r * 0.35, y), (x + r * 0.28, y - r * 1.2), (x - r * 0.28, y - r * 1.2)], (240, 232, 214, 255), (60, 40, 30, 255), 1.2 * s)
    p.chord(x - r, y - r * 2.1, x + r, y - r * 0.5, 180, 360, _rgba(cap))
    for dx_, dy_ in ((-0.45, -1.55), (0.2, -1.75), (0.55, -1.45)):
        p.disc(x + dx_ * r, y + dy_ * r, r * 0.16, (255, 255, 255, 255))


def _deco_forest(p, W, h, head, s, rng):
    """Grass along the lanes, stumps, logs, rocks, mushrooms and a signpost on the back lane.
    / Herbe au bord des voies ; souches, troncs, rochers, champignons et un panneau sur la voie du fond."""
    _tufts(p, W, head + (TH_LANES[0] + 4) * s, s, rng, ((60, 160, 50), (150, 222, 90)), 0.9)
    _tufts(p, W, head + (TH_LANES[2] + 4) * s, s, rng, ((60, 160, 50), (150, 222, 90)), 1.0)
    _tufts(p, W, h - 2 * s, s, rng, ((50, 140, 44), (120, 200, 80)), 1.6, gap=(60, 160))
    wood, cut, dark = (126, 84, 50), (214, 170, 110), (46, 30, 22)
    things = ["sign"] + ["stump", "log", "rock", "rock", "mush", "stump", "mush"]
    rng.shuffle(things)
    x = rng.uniform(40, 120) * s
    for t in things:
        if x > W - 60 * s:
            break
        y = head + rng.uniform(12, 22) * s
        if t == "stump":
            _stump(p, x, y, s, rng, wood, cut, dark)
        elif t == "log":
            _log(p, x, y, s, rng, wood, cut, dark)
        elif t == "rock":
            _rock(p, x, y, s, rng, (130, 128, 120), (176, 176, 166), (50, 48, 50))
        elif t == "mush":
            for k in range(rng.randint(2, 3)):
                _mushroom(p, x + k * 12 * s, y + rng.uniform(-2, 2) * s, s, rng, (220, 50, 40))
        else:
            _sign(p, x, y, s, wood, dark, (250, 240, 220))
        x += rng.uniform(180, 300) * s


def _canopy(W, s, rng, tones, h=280, vines=True, leaf_cols=None, vine_cols=None):
    """Leaves across the top of the screen, as in the game: big clumps hanging, pointed leaves at their edge, vines.
    / Le feuillage en haut de l'écran comme dans le jeu : grosses touffes, feuilles pointues, lianes."""
    p = _Pic(W, h * s)
    p.poly([(0, 0), (W, 0), (W, 26 * s), (0, 26 * s)], _rgba(tones[0]))
    bottoms = []
    x = rng.uniform(0, 30) * s
    while x < W:
        r = rng.uniform(42, 76) * s
        cy = rng.uniform(4, 40) * s
        balls = _clump(p, x, cy, r, rng, tones, n=9, spread=(1.25, 0.6))
        bottoms += [(bx, by + br * 0.8) for bx, by, br in balls if by > cy]
        x += r * rng.uniform(0.75, 1.15)
    lc = leaf_cols or (tones[1], tones[2], tones[0])
    for bx, by in bottoms:                                                    # feuilles pointues sous les touffes
        for _ in range(rng.randint(1, 3)):
            _leaf(p, bx + rng.uniform(-10, 10) * s, by - 4 * s, rng.uniform(60, 120), rng.uniform(20, 36) * s, rng.uniform(10, 15) * s,
                  rng.choice(lc), vein=mix(lc[2], (0, 0, 0), 0.2))
    if vines:
        vc = vine_cols or ((40, 96, 40), tones[1], tones[2])
        for bx, by in rng.sample(bottoms, max(1, len(bottoms) // 9)):
            _vine(p, bx, by - 6 * s, rng.uniform(60, h * s - by - 10 * s), rng, s, vc[0], vc[1], vc[2])
    return p.done()


def build_th_forest(W, H, s, seed=51):
    """Forest planet as in the game: a bright blue sky with big clouds, floating rocks, giant trees, a row of bushes,
    grassy lanes with stumps and a signpost, leaves and vines across the top. / La planète forêt comme dans le jeu."""
    rng = random.Random(seed)
    gy = H - (TH_GROUND + TH_HEAD) * s                                         # haut de l'image du sol
    sky = vgrad(W, H, [(0.0, (26, 96, 204)), (0.45, (76, 160, 232)), (0.8, (160, 214, 240)), (1.0, (196, 232, 236))])
    clouds = _cumulus(W, int(H * 0.7), s, rng, 6, ((255, 255, 255), (226, 238, 250), (178, 204, 232)), 90 * s, 220 * s)
    isles, iy = _rock_isles(W, s, rng, 150 * s, 2, (150, 118, 108), (104, 80, 82), (86, 166, 60), (140, 206, 86),
                            ((40, 110, 50), (70, 150, 60), (120, 190, 80)))
    far = _crowns(W, int(H * 0.5), s, rng, 50 * s, ((70, 140, 120), (96, 168, 136), (140, 200, 156)))
    trees = _trunks(W, H, s, rng, int(H - TH_GROUND * s + 10 * s), ((176, 128, 82), (132, 90, 56), (84, 56, 36)),
                    ((30, 90, 40), (54, 136, 52), (110, 186, 74)), ((44, 100, 40), (58, 140, 56), (110, 190, 80)))
    bushes = _bushes(W, int(110 * s), s, rng, ((26, 92, 40), (46, 136, 52), (100, 184, 70)), [(255, 120, 150), (255, 220, 90), (250, 250, 255)])
    ground = th_ground(W, s, rng, ((104, 186, 66), (74, 144, 48)), ((116, 80, 48), (82, 54, 32)), ((150, 120, 74), (118, 92, 58)),
                       (186, 240, 130), [(80, 150, 60), (120, 96, 60), (150, 190, 90), (176, 146, 96)], _deco_forest)
    canopy = _canopy(W, s, rng, ((20, 70, 36), (40, 120, 48), (96, 176, 66)), 270, leaf_cols=((52, 140, 56), (90, 172, 70), (34, 100, 44)))
    layers = [
        {"img": clouds, "y": 0, "f": 0.03, "stage": "sky"},
        {"img": isles, "y": iy, "f": 0.07, "stage": "sky"},
        {"img": far, "y": int(H * 0.5), "f": 0.14, "stage": "mid"},
        {"img": trees, "y": 0, "f": 0.3, "stage": "mid"},
        {"img": bushes, "y": int(gy + TH_HEAD * s - 100 * s), "f": 0.55, "stage": "mid"},
        {"img": ground, "y": int(gy), "f": 1.0, "stage": "near"},
        {"img": canopy, "y": 0, "f": 1.12, "stage": "near"},
    ]
    _fit(layers)
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"dust": (220, 255, 160)}}


def _peaks(W, H, s, rng, y, n, hmin, hmax, slope, body, cap=None, cap_px=30, rim=None, snow_line=None):
    """Mountain range with sharp peaks (tileable), snow on the ridges and above the snow line.
    / Montagnes à pics, neige sur les crêtes et au-dessus de la limite des neiges."""
    peaks = [(rng.uniform(0, W), rng.uniform(hmin, hmax) * s, rng.uniform(0.8, 1.25) * slope) for _ in range(n)]
    f = periodic(W, rng, 6, 1.0)

    def top(x):
        best = 0.0
        for px, ph, sl in peaks:
            dd = abs(x - px)
            dd = min(dd, W - dd)
            best = max(best, ph - dd * sl)
        return y - best + 5 * s * f(x)
    c = Sil(W, H, s)
    c.poly([(0, H)] + [(x, top(x)) for x in range(0, W + 6, 6)] + [(W, H)])
    mask = c.mask()
    img = paint(mask, body, rim=rim)
    if cap:
        k = int(cap_px * s)
        shifted = Image.new("L", mask.size, 0)
        shifted.paste(mask.crop((0, 0, W, H - k)), (0, k))
        snow = ImageChops.subtract(mask, shifted)
        if snow_line is not None:                                        # au-dessus de la limite : tout est blanc, bord irrégulier
            above = Image.new("L", mask.size, 0)
            g = periodic(W, rng, 5, 1.0)
            ImageDraw.Draw(above).polygon([(0, 0)] + [(x, snow_line + 14 * s * g(x)) for x in range(0, W + 8, 8)] + [(W, 0)], fill=255)
            snow = ImageChops.lighter(snow, ImageChops.multiply(mask, above))
        snow = snow.filter(ImageFilter.GaussianBlur(2 * s)).point(lambda v: 255 if v > 110 else 0)
        img.paste(cap, (0, 0), snow)
    return img


def _ice_ceiling(W, s, rng, h=210):
    """A roof of ice at the top: blue ice with frost, long icicles hanging. / Un plafond de glace, de longues stalactites."""
    p = _Pic(W, h * s)
    f = periodic(W, rng, 5, 1.0)
    edge = [(x, 34 * s + 12 * s * f(x)) for x in range(0, W + 10, 10)]
    p.poly([(0, 0), (W, 0)] + list(reversed(edge)), (40, 70, 120, 255))
    p.poly([(0, 0), (W, 0)] + [(x, y - 12 * s) for x, y in reversed(edge)], (70, 120, 180, 255))
    p.poly([(0, 0), (W, 0)] + [(x, y * 0.4) for x, y in reversed(edge)], (30, 54, 100, 255))
    x = 0.0
    while x < W:                                                               # stalactites de glace
        y = 34 * s + 12 * s * f(x) - 4 * s
        w = rng.uniform(8, 20) * s
        ln = rng.uniform(30, 150 if rng.random() < 0.3 else 70) * s
        p.poly([(x - w, y), (x + w, y), (x + w * 0.1, y + ln)], (150, 210, 245, 235), (40, 70, 120, 255), 1.4 * s)
        p.poly([(x - w * 0.6, y + 2 * s), (x - w * 0.1, y + 2 * s), (x - w * 0.05, y + ln * 0.8)], (230, 250, 255, 255))
        x += rng.uniform(14, 44) * s
    for _ in range(int(W / (60 * s))):                                         # givre
        x0, y0 = rng.uniform(0, W), rng.uniform(4, 30) * s
        p.line([(x0, y0), (x0 + rng.uniform(10, 26) * s, y0 + rng.uniform(-4, 4) * s)], (200, 236, 255, 200), 1.6 * s)
    return p.done()


def _deco_ice(p, W, h, head, s, rng):
    """Icicles under the ledge, snow drifts, ice blocks and a frozen signpost on the back lane.
    / Glaçons sous la corniche, congères, blocs de glace et un panneau gelé sur la voie du fond."""
    x = 0.0
    yf = head + (TH_LANES[1] + 1) * s
    while x < W:
        w, ln = rng.uniform(4, 9) * s, rng.uniform(8, 22) * s
        p.poly([(x - w / 2, yf), (x + w / 2, yf), (x, yf + ln)], (200, 236, 255, 235))
        x += rng.uniform(10, 40) * s
    for lane, k in ((TH_LANES[0] + 6, 0.8), (TH_LANES[2] + 4, 1.0)):
        x = rng.uniform(0, 80) * s
        while x < W:
            w = rng.uniform(20, 46) * s * k
            y = head + lane * s
            p.chord(x - w, y - w * 0.32, x + w, y + w * 0.32, 180, 360, (244, 250, 255, 255))
            x += rng.uniform(90, 220) * s
    things = ["sign", "block", "rock", "block", "rock", "block"]
    rng.shuffle(things)
    x = rng.uniform(60, 140) * s
    for t in things:
        if x > W - 60 * s:
            break
        y = head + rng.uniform(12, 22) * s
        if t == "block":
            w, hh = rng.uniform(16, 26) * s, rng.uniform(22, 40) * s
            p.poly([(x - w, y), (x - w * 0.9, y - hh), (x + w * 0.2, y - hh * 1.1), (x + w, y - hh * 0.8), (x + w, y)], (140, 200, 240, 240),
                   (40, 70, 120, 255), 1.6 * s)
            p.poly([(x - w * 0.7, y - hh * 0.9), (x - w * 0.3, y - hh), (x - w * 0.4, y - hh * 0.3)], (230, 250, 255, 255))
        elif t == "rock":
            _rock(p, x, y, s, rng, (120, 130, 150), (170, 180, 200), (40, 44, 60))
            p.chord(x - 22 * s, y - 26 * s, x + 18 * s, y - 10 * s, 180, 360, (248, 252, 255, 255))
        else:
            _sign(p, x, y, s, (110, 90, 80), (40, 34, 40), (240, 250, 255))
            p.chord(x - 38 * s, y - 76 * s, x + 30 * s, y - 64 * s, 180, 360, (248, 252, 255, 255))


def build_th_ice(W, H, s, seed=52):
    """Ice planet: polar night with an aurora, white peaks, ice spires, snow drifts, snowy lanes, a roof of ice with
    icicles at the top. / La planète de glace : nuit polaire, aurore, pics, aiguilles, plafond de glace."""
    rng = random.Random(seed)
    gy = H - (TH_GROUND + TH_HEAD) * s
    sky = vgrad(W, H, [(0.0, (8, 16, 44)), (0.55, (34, 62, 112)), (1.0, (96, 136, 176))])
    twinkle = _stars_sky(sky, rng, 180, W, H, 0.5)
    peaks = _peaks(W, H, s, rng, H * 0.66, 9, 120, 200, 0.75, [(0, (120, 150, 196)), (0.6, (96, 126, 172)), (1, (70, 96, 140))],
                   cap=(236, 246, 255), cap_px=10, rim=(255, 255, 255), snow_line=H * 0.44)
    p = _Pic(W, H)                                                             # aiguilles de glace, faces claires et sombres
    x = 0.0
    base = H - TH_GROUND * s + 10 * s
    while x < W:
        for _ in range(rng.randint(1, 3)):
            w, hh = rng.uniform(18, 40) * s, rng.uniform(120, 240) * s
            xx = x + rng.uniform(-30, 30) * s
            tip = (xx + rng.uniform(-0.3, 0.3) * w, base - hh)
            p.poly([(xx - w, base), tip, (xx + w, base)], (110, 170, 220, 255), (30, 60, 110, 255), 2 * s)
            p.poly([(xx - w, base), tip, (xx - w * 0.15, base)], (176, 222, 250, 255))
            p.line([tip, (xx - w * 0.15, base)], (230, 250, 255, 255), 1.6 * s)
        x += rng.uniform(160, 320) * s
    spires = p.done()
    drifts = _mounds(W, int(80 * s), s, rng, ((150, 186, 222), (212, 232, 250), (250, 253, 255)), size=(110, 240), tall=(20, 44))
    ground = th_ground(W, s, rng, ((236, 246, 255), (190, 214, 240)), ((110, 170, 220), (60, 110, 170)), ((214, 230, 246), (170, 196, 226)),
                       (255, 255, 255), [(200, 220, 240), (170, 196, 226), (255, 255, 255)], _deco_ice)
    roof = _ice_ceiling(W, s, rng)
    layers = [
        {"img": None, "aurora": aurora_img(W, int(220 * s), s, rng), "y": 0, "f": 0.03, "stage": "sky"},
        {"img": peaks, "y": H - peaks.height, "f": 0.06, "stage": "far"},
        {"img": spires, "y": 0, "f": 0.25, "stage": "mid"},
        {"img": drifts, "y": int(gy + TH_HEAD * s - 70 * s), "f": 0.55, "stage": "mid"},
        {"img": ground, "y": int(gy), "f": 1.0, "stage": "near"},
        {"img": roof, "y": 0, "f": 1.12, "stage": "near"},
    ]
    _fit(layers)
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"stars": twinkle, "snow": True}}


def hook_wind(bd, screen, b, L, now, dt):
    """Gusts of wind: long light streaks crossing the sky fast. / Rafales : de longues traînées claires."""
    st = bd.amb_state.setdefault("_wind", None)
    W, H, s = bd.W, bd.H, bd.s
    if st is None:
        st = bd.amb_state["_wind"] = [[bd.rng.uniform(0, W), bd.rng.uniform(H * 0.2, H * 0.7), bd.rng.uniform(0.4, 1.0)] for _ in range(14)]
    sp, add = bd.fx.sp, bd.pg.BLEND_RGB_ADD
    for p in st:
        p[0] -= (700 + 900 * p[2]) * s * dt + bd.speed * dt
        if p[0] < -400 * s:
            p[0], p[1], p[2] = W + bd.rng.uniform(0, 600) * s, bd.rng.uniform(H * 0.2, H * 0.7), bd.rng.uniform(0.4, 1.0)
        g = sp.streak(int((120 + 200 * p[2]) * s), max(2, int(2 * s)), (200, 220, 240), 180, 3 + 3 * p[2])
        screen.blit(g, (int(p[0]), int(p[1] - g.get_height() / 2)), special_flags=add)


def _isles(W, H, s, rng):
    """Floating rock islands with grass on top, roots below and a windmill. / Îles de roche qui flottent, avec un moulin."""
    p = _Pic(W, H)
    x = rng.uniform(0, 200) * s
    while x < W:
        w = rng.uniform(60, 140) * s
        y = rng.uniform(0.3, 0.44) * H
        depth = w * rng.uniform(0.7, 1.0)
        bottom = []
        n = 9
        for i in range(n + 1):
            t = i / n
            yy = y + depth * math.sin(t * math.pi) ** 0.7 * (rng.uniform(0.75, 1.05) if 0 < i < n else 0)
            bottom.append((x + w - 2 * w * t, yy))
        p.poly([(x - w, y), (x + w, y)] + bottom, (128, 104, 84, 255), (50, 38, 34, 255), 2 * s)
        p.poly([(x - w * 0.2, y)] + [pt for pt in bottom if pt[0] < x + w * 0.3] + [(x - w, y)], (104, 82, 66, 255))
        for _ in range(4):                                                      # racines
            rx = x + rng.uniform(-w, w) * 0.6
            ry = y + depth * 0.6 * math.sin((1 - abs(rx - x) / w) * math.pi / 2)
            p.line([(rx, ry), (rx + rng.uniform(-6, 6) * s, ry + rng.uniform(16, 40) * s)], (70, 56, 46, 255), 2 * s)
        p.ellipse(x - w * 1.04, y - 7 * s, x + w * 1.04, y + 9 * s, (110, 170, 80, 255))
        p.ellipse(x - w * 0.95, y - 7 * s, x + w * 0.9, y + 2 * s, (150, 200, 100, 255))
        if rng.random() < 0.65:                                                 # un moulin à vent
            M = x + rng.uniform(-w, w) * 0.4
            p.poly([(M - 7 * s, y - 1 * s), (M + 7 * s, y - 1 * s), (M + 4 * s, y - 46 * s), (M - 4 * s, y - 46 * s)], (236, 230, 214, 255),
                   (60, 50, 44, 255), 1.4 * s)
            p.poly([(M - 6 * s, y - 46 * s), (M + 6 * s, y - 46 * s), (M, y - 56 * s)], (170, 70, 50, 255))
            a0 = rng.uniform(0, math.pi)
            for j in range(4):
                a = a0 + j * math.pi / 2
                cx, cy = M, y - 48 * s
                p.poly([(cx, cy), (cx + math.cos(a) * 30 * s - math.sin(a) * 4 * s, cy + math.sin(a) * 30 * s + math.cos(a) * 4 * s),
                        (cx + math.cos(a) * 30 * s, cy + math.sin(a) * 30 * s)], (250, 246, 236, 255))
        x += rng.uniform(300, 520) * s
    return p.done()


def _island_roof(W, s, rng, h=220):
    """The underside of a huge floating island at the top: layers of rock, roots and grass hanging over the edge.
    / Le dessous d'une immense île flottante en haut : couches de roche, racines et herbe qui pendent."""
    p = _Pic(W, h * s)
    f = periodic(W, rng, 5, 1.0)
    edge = [(x, 48 * s + 16 * s * f(x)) for x in range(0, W + 10, 10)]
    p.poly([(0, 0), (W, 0)] + list(reversed(edge)), (118, 90, 70, 255))
    for k, col in ((0.75, (140, 108, 82)), (0.45, (100, 76, 60)), (0.2, (84, 64, 52))):
        p.poly([(0, 0), (W, 0)] + [(x, y * k) for x, y in reversed(edge)], _rgba(col))
    x = 0.0
    while x < W:                                                               # pointes de roche
        y = 48 * s + 16 * s * f(x) - 6 * s
        w, ln = rng.uniform(10, 26) * s, rng.uniform(16, 50) * s
        p.poly([(x - w, y), (x + w, y), (x + rng.uniform(-0.3, 0.3) * w, y + ln)], (96, 72, 58, 255), (50, 36, 30, 255), 1.6 * s)
        x += rng.uniform(30, 90) * s
    for _ in range(int(W / (130 * s))):                                        # racines qui pendent
        x0 = rng.uniform(0, W)
        y0 = 48 * s + 16 * s * f(x0)
        pts = [(x0, y0)]
        for i in range(rng.randint(4, 7)):
            px, py = pts[-1]
            pts.append((px + rng.uniform(-7, 7) * s, py + rng.uniform(10, 20) * s))
        p.line(pts, (64, 48, 38, 255), rng.uniform(4, 6) * s)
        p.line([(px - 1.5 * s, py) for px, py in pts[:-1]], (110, 86, 64, 255), 1.4 * s)
    for _ in range(int(W / (30 * s))):                                         # herbe qui retombe
        x0 = rng.uniform(0, W)
        y0 = 48 * s + 16 * s * f(x0) - 2 * s
        p.poly([(x0 - 5 * s, y0), (x0 + 5 * s, y0), (x0 + rng.uniform(-6, 6) * s, y0 + rng.uniform(14, 34) * s)],
               _rgba(mix((90, 160, 60), (160, 210, 100), rng.random())))
    return p.done()


def _deco_wind(p, W, h, head, s, rng):
    """Grass bent by the wind, rocks and a signpost. / Herbe couchée par le vent, rochers et un panneau."""
    _tufts(p, W, head + (TH_LANES[0] + 4) * s, s, rng, ((150, 170, 80), (210, 220, 130)), 1.0, bend=-0.9)
    _tufts(p, W, head + (TH_LANES[2] + 4) * s, s, rng, ((150, 170, 80), (210, 220, 130)), 1.1, bend=-0.9)
    things = ["sign", "rock", "rock", "stump", "rock"]
    rng.shuffle(things)
    x = rng.uniform(60, 140) * s
    for t in things:
        if x > W - 60 * s:
            break
        y = head + rng.uniform(12, 22) * s
        if t == "rock":
            _rock(p, x, y, s, rng, (160, 130, 100), (206, 180, 140), (60, 44, 34), 1.2)
        elif t == "stump":
            _stump(p, x, y, s, rng, (140, 100, 66), (220, 186, 130), (50, 36, 26))
        else:
            _sign(p, x, y, s, (140, 100, 66), (50, 36, 26), (250, 240, 220))
        x += rng.uniform(220, 380) * s


def build_th_wind(W, H, s, seed=53):
    """Wind planet: bright sky, banks of clouds, floating islands with windmills, rocky lanes, the underside of a huge
    floating island at the top, gusts of wind. / La planète du vent : îles flottantes, moulins, rafales."""
    rng = random.Random(seed)
    gy = H - (TH_GROUND + TH_HEAD) * s
    sky = vgrad(W, H, [(0.0, (60, 120, 214)), (0.55, (160, 196, 238)), (1.0, (242, 222, 186))])
    add_at(sky, radial(int(700 * s), (90, 80, 40), 1.8), int(W * 0.85), int(H * 0.25))
    clouds = _cumulus(W, int(H * 0.8), s, rng, 7, ((255, 252, 246), (240, 230, 220), (206, 196, 200)), 120 * s, 260 * s, size=(80, 150))
    isles = _isles(W, H, s, rng)
    hills = _mounds(W, int(90 * s), s, rng, ((150, 150, 80), (190, 186, 100), (226, 220, 146)), size=(140, 300), tall=(26, 56),
                    grass=((150, 170, 80), (200, 210, 120), (120, 150, 70)))
    ground = th_ground(W, s, rng, ((206, 180, 120), (170, 140, 90)), ((140, 104, 70), (100, 72, 48)), ((190, 160, 110), (160, 128, 86)),
                       (250, 236, 190), [(170, 140, 96), (130, 104, 70), (220, 200, 150)], _deco_wind)
    roof = _island_roof(W, s, rng)
    layers = [
        {"img": clouds, "y": 0, "f": 0.05, "stage": "far"},
        {"img": isles, "y": 0, "f": 0.18, "stage": "mid"},
        {"img": hills, "y": int(gy + TH_HEAD * s - 80 * s), "f": 0.5, "stage": "mid"},
        {"img": ground, "y": int(gy), "f": 1.0, "stage": "near"},
        {"img": roof, "y": 0, "f": 1.12, "stage": "near"},
    ]
    _fit(layers)
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"dust": (250, 230, 190), "hooks": {"mid": [hook_wind]}}}


def _lava_ceiling(W, s, rng, h=200):
    """A roof of black rock at the top: stalactites, cracks glowing with lava, drops of lava. Returns the picture and the
    places that glow. / Un plafond de roche noire : stalactites, fissures de lave qui brillent."""
    p = _Pic(W, h * s)
    f = periodic(W, rng, 5, 1.0)
    edge = [(x, 40 * s + 14 * s * f(x)) for x in range(0, W + 10, 10)]
    p.poly([(0, 0), (W, 0)] + list(reversed(edge)), (54, 26, 24, 255))
    p.poly([(0, 0), (W, 0)] + [(x, y * 0.55) for x, y in reversed(edge)], (36, 16, 16, 255))
    lights = []
    x = 0.0
    while x < W:                                                               # stalactites
        y = 40 * s + 14 * s * f(x) - 4 * s
        w = rng.uniform(10, 24) * s
        ln = rng.uniform(26, 110 if rng.random() < 0.3 else 60) * s
        tip = x + rng.uniform(-0.2, 0.2) * w
        p.poly([(x - w, y), (x + w, y), (tip, y + ln)], (62, 30, 26, 255), (24, 10, 10, 255), 1.6 * s)
        p.poly([(x + w * 0.2, y), (x + w, y), (tip, y + ln)], (40, 18, 16, 255))
        if rng.random() < 0.25:                                                 # une goutte de lave au bout
            p.disc(tip, y + ln + 3 * s, 3.2 * s, (255, 150, 50, 255))
            lights.append((tip, y + ln + 3 * s))
        x += rng.uniform(24, 60) * s
    for _ in range(int(W / (110 * s))):                                         # fissures de lave
        x0, y0 = rng.uniform(0, W), rng.uniform(8, 30) * s
        pts = [(x0, y0)]
        for _ in range(rng.randint(3, 6)):
            px, py = pts[-1]
            pts.append((px + rng.uniform(10, 26) * s, py + rng.uniform(-5, 5) * s))
        p.line(pts, (255, 110, 30, 255), 3.2 * s)
        p.line(pts, (255, 220, 140, 255), 1.2 * s)
        lights.append(pts[len(pts) // 2])
    return p.done(), lights


def _deco_fire(p, W, h, head, s, rng):
    """Glowing lava cracks across the two lanes, black rocks. / Fissures de lave qui brillent, rochers noirs."""
    for _ in range(int(W / (70 * s))):
        lane = rng.random() < 0.4
        x, y = rng.uniform(0, W), head + (rng.uniform(16, 40) if lane else rng.uniform(70, TH_GROUND - 8)) * s
        pts = [(x, y)]
        for _ in range(rng.randint(3, 7)):
            x, y = x + rng.uniform(10, 30) * s, y + rng.uniform(-5, 5) * s
            pts.append((x, y))
        p.line(pts, (255, 90, 20, 200), rng.uniform(3, 5) * s)
        p.line(pts, (255, 210, 120, 255), 1.4 * s)
    x = rng.uniform(60, 140) * s
    while x < W - 60 * s:
        _rock(p, x, head + rng.uniform(12, 22) * s, s, rng, (54, 34, 32), (96, 60, 50), (20, 10, 10), rng.uniform(1.0, 1.6))
        x += rng.uniform(200, 360) * s


def build_th_fire(W, H, s, seed=54):
    """Fire planet: red sky, volcanoes with lava flows, basalt spires, dark rocks, lanes cracked with lava, a roof of
    black rock with stalactites and glowing cracks, embers. / La planète de feu : volcans, plafond de roche, braises."""
    rng = random.Random(seed)
    gy = H - (TH_GROUND + TH_HEAD) * s
    sky = vgrad(W, H, [(0.0, (26, 6, 12)), (0.45, (96, 24, 14)), (0.75, (200, 80, 26)), (1.0, (250, 150, 50))])
    far = Sil(W, int(H * 0.82), s)                                             # volcans
    h = int(H * 0.82)
    craters = []
    x = 0.0
    while x < W:
        w, hh = rng.uniform(220, 360) * s, rng.uniform(260, 340) * s
        pts = []
        for i in range(31):
            t = -1 + 2 * i / 30
            hgt = min(hh * (1 - abs(t)) ** 1.8, hh * 0.86) - (6 * s if abs(t) < 0.05 else 0)
            pts.append((x + t * w, h - hgt))
        far.poly([(x - w, h)] + pts + [(x + w, h)])
        craters.append((x, h - hh * 0.86))
        x += rng.uniform(380, 640) * s
    volc = paint(far.mask(), [(0, (60, 18, 16)), (1, (34, 10, 10))], rim=(220, 80, 30))
    flows = Image.new("L", volc.size, 0)
    fd = ImageDraw.Draw(flows)
    for cx, cy in craters:
        for _ in range(2):
            pts = [(cx + rng.uniform(-10, 10) * s, cy + 4 * s)]
            for _ in range(6):
                px, py = pts[-1]
                pts.append((px + rng.uniform(-22, 22) * s, py + rng.uniform(14, 26) * s))
            for dx in _shifts(W, cx - 200 * s, cx + 200 * s):
                fd.line([(px + dx, py) for px, py in pts], fill=255, width=max(2, int(4 * s)))
    flows = ImageChops.multiply(flows, volc.getchannel("A"))
    volc.paste((255, 110, 30), (0, 0), flows.filter(ImageFilter.GaussianBlur(3 * s)))
    volc.paste((255, 220, 140), (0, 0), flows)
    p = _Pic(W, H)                                                             # aiguilles de basalte
    x = 0.0
    base = H - TH_GROUND * s + 10 * s
    while x < W:
        for i in range(rng.randint(2, 4)):
            w, hh = rng.uniform(18, 34) * s, rng.uniform(90, 200) * s
            xx = x + i * rng.uniform(20, 40) * s
            tip = xx + rng.uniform(-0.3, 0.3) * w
            pts = [(xx - w, base)]
            for k in range(1, 6):
                t = k / 6
                pts.append((xx - w + (tip - xx + w) * t + rng.uniform(-3, 3) * s, base - hh * t))
            pts.append((tip, base - hh))
            for k in range(5, 0, -1):
                t = k / 6
                pts.append((xx + w - (xx + w - tip) * t + rng.uniform(-3, 3) * s, base - hh * t))
            p.poly(pts + [(xx + w, base)], (50, 20, 18, 255), (20, 8, 8, 255), 2 * s)
            p.poly([(tip, base - hh)] + [(px, py) for px, py in pts[1:6]] + [(xx - w * 0.4, base)], (70, 30, 26, 255))
            p.line([(tip, base - hh), (xx - w * 0.6, base - hh * 0.3)], (255, 110, 50, 180), 1.6 * s)
        x += rng.uniform(240, 420) * s
    spires = p.done()
    rocks = _crags(W, int(80 * s), s, rng, ((44, 18, 16), (70, 30, 24), (16, 6, 6)), (255, 120, 50), (255, 150, 40))
    ground = th_ground(W, s, rng, ((70, 40, 36), (46, 26, 24)), ((40, 22, 20), (26, 14, 14)), ((60, 34, 30), (40, 22, 20)),
                       (200, 90, 50), [(90, 50, 40), (30, 18, 16), (110, 60, 40)], _deco_fire)
    roof, glows = _lava_ceiling(W, s, rng)
    layers = [
        {"img": volc, "y": H - volc.height, "f": 0.05, "stage": "far", "lights": [(cx, cy - 4 * s) for cx, cy in craters]},
        {"img": spires, "y": 0, "f": 0.3, "stage": "mid"},
        {"img": rocks, "y": int(gy + TH_HEAD * s - 76 * s), "f": 0.55, "stage": "mid"},
        {"img": ground, "y": int(gy), "f": 1.0, "stage": "near"},
        {"img": roof, "y": 0, "f": 1.12, "stage": "near", "lights": glows},
    ]
    _fit(layers)
    return {"sky": sky, "layers": layers, "tw": W, "amb": {"window": (255, 120, 40), "explosions": True, "horizon": H * 0.55,
                                                           "hooks": {"front": [hook_embers]}}}


TH_WORLDS = ("th_forest", "th_ice", "th_wind", "th_fire")


# ---------------------------------------------------------------------------- Baseball Stars 2
def bb_geom(W, H, s):
    """The field seen as in the game's batting view: a camera 12 feet high, 54 feet behind home plate, looking down at
    49 degrees. The plate at the bottom, the mound in the middle, the outfield at the top. / La caméra de la vue de
    frappe du jeu : le marbre en bas, le monticule au milieu, le champ extérieur en haut."""
    th = math.radians(49.0)
    return {"cx": W / 2.0, "cy": H + 832.8 * s, "f": 1143.8 * s, "zc": 54.0, "hc": 12.0, "cos": math.cos(th), "sin": math.sin(th)}


def bb_xy(g, x, z, h=0.0):
    """Screen point of the field point x feet to the right, z feet towards center field, h feet high."""
    dz, dh = z + g["zc"], h - g["hc"]
    depth = max(1.0, dz * g["cos"] - dh * g["sin"])
    up = dz * g["sin"] + dh * g["cos"]
    return g["cx"] + g["f"] * x / depth, g["cy"] - g["f"] * up / depth


def bb_px(g, z):
    """Pixels per foot of height at the depth z. / Pixels par pied de hauteur à la profondeur z."""
    return (bb_xy(g, 0.0, z, 0.0)[1] - bb_xy(g, 0.0, z, 6.0)[1]) / 6.0


FENCE = 330.0                     # wall at the foul poles, 400 in center field / mur à 330 pieds, 400 au centre


def bb_fence(a):
    """Distance of the wall in the direction a (radians, 0 = center field, +/- pi/4 = foul lines)."""
    return FENCE + (400.0 - FENCE) * math.cos(min(1.0, abs(a) / (math.pi / 4)) * math.pi / 2)


def build_ballpark(W, H, s, seed=55):
    """The field in daylight as in the game's batting view: bright green grass mown in stripes, the orange dirt of the
    infield and of the mound, the white lines and the bases, the outfield wall at the top.
    / Le terrain en plein jour comme dans la vue de frappe du jeu : herbe vive tondue en bandes, terre orange, lignes."""
    rng = random.Random(seed)
    g = bb_geom(W, H, s)
    k = 2
    img = Image.new("RGB", (W * k, H * k), (60, 146, 52))
    d = ImageDraw.Draw(img)

    def P(x, z, h=0.0):
        X, Y = bb_xy(g, x, z, h)
        return X * k, Y * k

    def ring(cx, cz, r, n=48, a0=0.0, a1=math.tau):
        return [P(cx + math.cos(a0 + (a1 - a0) * i / n) * r, cz + math.sin(a0 + (a1 - a0) * i / n) * r) for i in range(n + 1)]
    light, dark = (98, 190, 70), (78, 166, 56)
    for i in range(0, 30):                                               # bandes de tonte en arcs autour du marbre
        r0, r1 = 14 + i * 20, 14 + (i + 1) * 20
        band = ring(0, 0, r1, 64, math.radians(-30), math.radians(210)) + list(reversed(ring(0, 0, r0, 64, math.radians(-30), math.radians(210))))
        d.polygon(band, fill=light if i % 2 else dark)
    dirt, dirt_l, dirt_d, chalk = (222, 150, 76), (238, 176, 102), (190, 120, 58), (250, 250, 244)
    t0 = math.radians(71.8)                                              # la terre du champ intérieur, arc de 95 pieds autour du monticule
    skin = [P(0, 0)] + [P(95 * math.sin(t0 - 2 * t0 * i / 60), 60.5 + 95 * math.cos(t0 - 2 * t0 * i / 60)) for i in range(61)]
    d.polygon(skin, fill=dirt)
    d.line(skin[1:], fill=dirt_d, width=max(2, int(4 * s * k)))
    infield = [P(0, 6), P(57, 63.6), P(0, 120), P(-57, 63.6)]            # l'herbe du losange, en bandes elle aussi
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon(infield, fill=255)
    stripes = Image.new("RGB", img.size, dark)
    sd = ImageDraw.Draw(stripes)
    for i in range(0, 20):
        z0, z1 = i * 8, i * 8 + 4
        sd.polygon([P(-80, z0), P(80, z0), P(80, z1), P(-80, z1)], fill=light)
    img.paste(stripes, (0, 0), mask)
    d.polygon(ring(0, 0, 13), fill=dirt)                                 # cercle autour du marbre
    d.line(ring(0, 0, 13), fill=dirt_d, width=max(2, int(3 * s * k)))
    d.polygon(ring(0, 60.5, 9), fill=dirt)                               # le monticule
    d.polygon(ring(-0.8, 59.5, 6), fill=dirt_l)
    d.polygon([P(-1, 60.2), P(1, 60.2), P(1, 60.8), P(-1, 60.8)], fill=chalk)
    for side in (-1, 1):                                                 # lignes de fausse balle, rectangles des frappeurs
        d.line([P(side * 3, 3), P(side * 300, 300)], fill=chalk, width=max(3, int(4 * s * k)))
        bx = side * 1.5
        box = [P(bx, -3), P(bx + side * 4, -3), P(bx + side * 4, 3), P(bx, 3), P(bx, -3)]
        d.line(box, fill=chalk, width=max(2, int(4 * s * k)), joint="curve")
        oc = ring(side * 36, -18, 2.6)                                   # cercles d'attente
        d.polygon(oc, fill=dirt_d)
    d.line([P(-1.5, -3), P(-1.5, -9), P(1.5, -9), P(1.5, -3)], fill=chalk, width=max(2, int(3 * s * k)))
    d.polygon([P(-0.7, 0), P(0.7, 0), P(0.7, -0.7), P(0, -1.4), P(-0.7, -0.7)], fill=chalk)        # le marbre
    for bx, bz in ((63.6, 63.6), (0, 127.3), (-63.6, 63.6)):             # les bases
        d.polygon([P(bx - 1.3, bz), P(bx, bz + 1.3), P(bx + 1.3, bz), P(bx, bz - 1.3)], fill=chalk)
    for a in (-1, 1):                                                    # chemins des bases plus sombres
        d.line([P(a * 4, 4), P(a * 60, 60)], fill=dirt_d, width=max(1, int(2 * s * k)))
    track = [P(math.sin(a) * bb_fence(a), math.cos(a) * bb_fence(a)) for a in (math.radians(-60 + i * 2) for i in range(61))]
    track_in = [P(math.sin(a) * (bb_fence(a) - 14), math.cos(a) * (bb_fence(a) - 14)) for a in (math.radians(-60 + i * 2) for i in range(61))]
    d.polygon(track + list(reversed(track_in)), fill=(196, 140, 84))     # piste d'avertissement
    wall_top = [P(math.sin(a) * bb_fence(a), math.cos(a) * bb_fence(a), 9) for a in (math.radians(-60 + i * 2) for i in range(61))]
    d.polygon(wall_top + list(reversed(track)), fill=(40, 90, 170))      # le mur bleu du fond
    d.polygon([(0, 0), (W * k, 0)] + list(reversed(wall_top)), fill=(30, 40, 70))
    d.line(wall_top, fill=(250, 220, 70), width=max(2, int(3 * s * k)))
    for _ in range(int(W / (14 * s))):                                   # petites touffes dans l'herbe
        x, y = rng.uniform(0, W * k), rng.uniform(H * 0.3 * k, H * k)
        d.line([(x, y), (x + 3 * s * k, y - 2 * s * k)], fill=(110, 200, 80), width=max(1, int(s * k)))
    sky = img.resize((W, H), Image.LANCZOS)
    return {"sky": sky, "layers": [], "tw": W, "amb": {"ballpark": g}}


# ---------------------------------------------------------------------------- Last Resort
def _towers(W, H, s, rng, top, wide, body, edge, lit, unlit, p_lit, win=(5, 7, 3, 4), blinks=None, roofs=True):
    """A row of skyscrapers from the bottom of the picture, their faces covered with windows, most of them lit (pixel
    art, drawn at full size). / Une rangée de gratte-ciel couverts de fenêtres, presque toutes allumées."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ww, wh, gx, gy = [v * s for v in win]
    x = rng.uniform(-40, 0) * s
    while x < W:
        w = rng.uniform(*wide) * s
        y0 = rng.uniform(*top) * s
        b0, b1 = body
        shade = rng.uniform(-0.12, 0.12)
        c0 = mix(b0, (0, 0, 0) if shade < 0 else (255, 255, 255), abs(shade) * 0.6)
        c1 = mix(b1, (0, 0, 0) if shade < 0 else (255, 255, 255), abs(shade) * 0.6)
        steps = [(x, y0, x + w)]
        if roofs and rng.random() < 0.5:                                   # étages en retrait au sommet
            inset = w * rng.uniform(0.12, 0.3)
            steps.insert(0, (x + inset, y0 - rng.uniform(20, 60) * s, x + w - inset))
        for dx in _shifts(W, x - 2, x + w + 2):
            for sx0, sy0, sx1 in steps:
                d.rectangle([sx0 + dx, sy0, sx1 + dx, H], fill=c0 + (255,))
                d.rectangle([sx0 + dx, sy0 + (H - sy0) * 0.45, sx1 + dx, H], fill=mix(c0, c1, 0.5) + (255,))
                d.rectangle([sx0 + dx, sy0 + (H - sy0) * 0.75, sx1 + dx, H], fill=c1 + (255,))
                d.rectangle([sx1 + dx - max(2, w * 0.08), sy0, sx1 + dx, H], fill=mix(c0, (0, 0, 0), 0.3) + (255,))
                d.line([sx0 + dx, sy0, sx1 + dx, sy0], fill=edge + (255,), width=max(1, int(2 * s)))
                yy = sy0 + gy * 1.5
                while yy < H - wh:
                    xx = sx0 + gx
                    k = (yy - sy0) / max(1.0, H - sy0)
                    while xx < sx1 - ww - max(2, w * 0.08):
                        if rng.random() < p_lit * (0.75 + 0.35 * k):
                            col = mix(lit[0], lit[1], rng.random())
                        else:
                            col = unlit
                        d.rectangle([xx + dx, yy, xx + dx + ww - 1, yy + wh - 1], fill=col + (255,))
                        xx += ww + gx
                    yy += wh + gy
            if roofs and rng.random() < 0.35:                               # antenne
                ax = x + w * rng.uniform(0.3, 0.7) + dx
                d.line([ax, steps[0][1], ax, steps[0][1] - rng.uniform(20, 50) * s], fill=edge + (255,), width=max(1, int(2 * s)))
                if blinks is not None and dx == 0:
                    blinks.append((ax, steps[0][1] - 50 * s))
        x += w + rng.uniform(-8, 26) * s
    return img


def hook_cars(bd, screen, b, L, now, dt):
    """Cars driving on the road below the highway, headlights in front, red lights behind. / Des voitures sur la route."""
    st = bd.amb_state.setdefault("_cars", None)
    W, H, s = bd.W, bd.H, bd.s
    lanes = (H - 78 * s, H - 30 * s)
    if st is None:
        st = bd.amb_state["_cars"] = [[bd.rng.uniform(0, W), i % 2, bd.rng.choice(("car0", "car1", "car2", "car3")),
                                       bd.rng.uniform(-60, 160) * s] for i in range(7)]
    sp, add = bd.fx.sp, bd.pg.BLEND_RGB_ADD
    for c in st:
        c[0] -= (bd.speed + c[3]) * dt
        if c[0] < -120 * s:
            c[0], c[2], c[3] = W + bd.rng.uniform(40, 500) * s, bd.rng.choice(("car0", "car1", "car2", "car3")), bd.rng.uniform(-60, 160) * s
        elif c[0] > W + 600 * s:
            c[0] = -100 * s
        img = b["imgs"][c[2]]
        y = lanes[c[1]]
        screen.blit(img, (int(c[0] - img.get_width() / 2), int(y - img.get_height())))
        g = sp.glow(10 * s, (255, 240, 200), 7, hot=0.6)                    # phares à l'avant (à droite), feux rouges derrière
        screen.blit(g, (int(c[0] + img.get_width() * 0.5 - g.get_width() / 2), int(y - img.get_height() * 0.45 - g.get_height() / 2)),
                    special_flags=add)
        r = sp.glow(7 * s, (255, 40, 30), 6, hot=0.5)
        screen.blit(r, (int(c[0] - img.get_width() * 0.5 - r.get_width() / 2), int(y - img.get_height() * 0.5 - r.get_height() / 2)),
                    special_flags=add)


def lr_car(color, s):
    """A small car seen from the side, nose to the right. / Une petite voiture de profil."""
    w, h = int(64 * s), int(24 * s)
    p = _Pic(w, h, 3)
    dark = (24, 18, 30, 255)
    p.poly([(2 * s, 20 * s), (2 * s, 12 * s), (14 * s, 10 * s), (22 * s, 3 * s), (44 * s, 3 * s), (52 * s, 10 * s), (62 * s, 12 * s),
            (62 * s, 20 * s)], _rgba(color), dark, 1.4 * s)
    p.poly([(16 * s, 10 * s), (23 * s, 5 * s), (32 * s, 5 * s), (32 * s, 10 * s)], (150, 190, 230, 255))
    p.poly([(35 * s, 10 * s), (35 * s, 5 * s), (43 * s, 5 * s), (49 * s, 10 * s)], (150, 190, 230, 255))
    p.line([(4 * s, 14 * s), (60 * s, 14 * s)], _rgba(mix(color, (255, 255, 255), 0.4)), 1.2 * s)
    for cx in (14 * s, 50 * s):
        p.disc(cx, 20 * s, 4.5 * s, dark)
        p.disc(cx, 20 * s, 2 * s, (140, 140, 150, 255))
    return p.done()


def build_lr_city(W, H, s, seed=56):
    """The city of Last Resort at night, as in the game: a red sky behind giant towers lit with orange windows, purple
    buildings with pink windows in front, an elevated road on its pillars, the highway with its fence and street lamps,
    cars driving on it. / La ville de Last Resort : tours géantes aux fenêtres orange, immeubles violets, autoroute."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (36, 4, 14)), (0.35, (96, 14, 20)), (0.7, (176, 46, 24)), (1.0, (230, 96, 36))])
    add_at(sky, radial(int(900 * s), (90, 30, 0), 1.4), int(W * 0.5), int(H * 0.9))
    blinks = []
    far = _towers(W, H, s, rng, (-40, 60), (90, 190), ((150, 38, 26), (214, 84, 30)), (255, 150, 70),
                  ((255, 170, 70), (255, 226, 140)), (126, 34, 22), 0.62)
    mid = _towers(W, H, s, rng, (110, 220), (70, 150), ((96, 30, 78), (150, 56, 110)), (230, 120, 190),
                  ((255, 140, 200), (255, 200, 230)), (74, 22, 60), 0.42, win=(5, 6, 4, 5), blinks=blinks)
    p = _Pic(W, int(190 * s))                                              # route surélevée sur ses piliers
    f = periodic(W, rng, 3, 1.0)
    deck = [(x, 70 * s + 34 * s * f(x)) for x in range(0, W + 8, 8)]
    for x in range(0, W, int(150 * s)):
        y = 70 * s + 34 * s * f(x)
        p.poly([(x - 9 * s, y), (x + 9 * s, y), (x + 12 * s, 190 * s), (x - 12 * s, 190 * s)], (70, 26, 66, 255))
        p.poly([(x - 9 * s, y), (x - 3 * s, y), (x - 4 * s, 190 * s), (x - 12 * s, 190 * s)], (104, 44, 92, 255))
    p.poly(deck + [(x, y + 16 * s) for x, y in reversed(deck)], (120, 48, 104, 255))
    p.line(deck, (250, 160, 220, 255), 2.4 * s)
    p.line([(x, y + 16 * s) for x, y in deck], (60, 20, 52, 255), 2 * s)
    ramp = p.done()
    hy = int(150 * s)                                                      # haut de l'autoroute dans son image
    p = _Pic(W, hy + int(130 * s))
    lamps = []
    for x in range(int(60 * s), W, int(260 * s)):                          # réverbères
        p.poly([(x - 2.5 * s, hy + 10 * s), (x + 2.5 * s, hy + 10 * s), (x + 2.5 * s, hy - 96 * s), (x - 2.5 * s, hy - 96 * s)], (40, 30, 60, 255))
        p.line([(x, hy - 96 * s), (x + 8 * s, hy - 104 * s), (x + 26 * s, hy - 104 * s)], (40, 30, 60, 255), 4 * s)
        p.poly([(x + 18 * s, hy - 106 * s), (x + 36 * s, hy - 106 * s), (x + 32 * s, hy - 99 * s), (x + 20 * s, hy - 99 * s)], (230, 230, 240, 255))
        lamps.append((x + 27 * s, hy - 98 * s))
    p.poly([(0, hy - 6 * s), (W, hy - 6 * s), (W, hy + 14 * s), (0, hy + 14 * s)], (60, 44, 88, 255))     # grillage
    for x in range(0, W, int(12 * s)):
        p.line([(x, hy - 22 * s), (x + 12 * s, hy + 2 * s)], (110, 96, 150, 150), 1 * s)
        p.line([(x + 12 * s, hy - 22 * s), (x, hy + 2 * s)], (110, 96, 150, 150), 1 * s)
    for x in range(0, W, int(48 * s)):
        p.poly([(x - 1.5 * s, hy - 26 * s), (x + 1.5 * s, hy - 26 * s), (x + 1.5 * s, hy + 6 * s), (x - 1.5 * s, hy + 6 * s)], (40, 30, 60, 255))
    p.line([(0, hy - 24 * s), (W, hy - 24 * s)], (150, 130, 190, 255), 2.4 * s)
    p.line([(0, hy - 6 * s), (W, hy - 6 * s)], (150, 130, 190, 255), 1.6 * s)
    p.poly([(0, hy + 14 * s), (W, hy + 14 * s), (W, hy + 130 * s), (0, hy + 130 * s)], (66, 50, 92, 255))  # la route
    p.poly([(0, hy + 14 * s), (W, hy + 14 * s), (W, hy + 22 * s), (0, hy + 22 * s)], (110, 92, 140, 255))
    p.poly([(0, hy + 90 * s), (W, hy + 90 * s), (W, hy + 130 * s), (0, hy + 130 * s)], (54, 40, 78, 255))
    for x in range(0, W, int(90 * s)):                                     # marquage
        p.poly([(x, hy + 66 * s), (x + 46 * s, hy + 66 * s), (x + 46 * s, hy + 70 * s), (x, hy + 70 * s)], (170, 150, 200, 255))
    for _ in range(int(W / (110 * s))):                                    # reflets des lumières sur la chaussée
        x, y = rng.uniform(0, W), hy + rng.uniform(30, 110) * s
        p.ellipse(x - 40 * s, y - 2 * s, x + 40 * s, y + 2 * s, (130, 100, 150, 70))
    road = p.done()
    images = {f"car{i}": lr_car(c, s) for i, c in enumerate(((220, 50, 40), (60, 90, 200), (220, 180, 50), (230, 230, 236)))}
    layers = _fit([
        {"img": far, "y": 0, "f": 0.05, "stage": "far"},
        {"img": mid, "y": 0, "f": 0.16, "stage": "mid", "blinks": blinks},
        {"img": ramp, "y": H - int(250 * s), "f": 0.4, "stage": "mid"},
        {"img": road, "y": H - road.height, "f": 1.0, "stage": "near", "lights": lamps},
    ])
    amb = {"window": (255, 230, 170), "blink": (255, 60, 40), "searchlights": [(0.22, 0.8), (0.7, 1.1)], "horizon": H * 0.62,
           "images": images, "hooks": {"near": [hook_cars]}}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


# ---------------------------------------------------------------------------- Aero Fighters : vu du ciel
def _clouds_layer(W, H, s, rng, n, size, alpha):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0.05, 0.95) * H
        for _ in range(rng.randint(3, 6)):
            w, hh = rng.uniform(0.5, 1.0) * size * s, rng.uniform(0.35, 0.7) * size * s
            ox, oy = rng.uniform(-size, size) * s, rng.uniform(-size, size) * 0.4 * s
            for dx in _shifts(W, x + ox - w, x + ox + w):
                d.ellipse([x + ox + dx - w, y + oy - hh, x + ox + dx + w, y + oy + hh], fill=(255, 255, 255, alpha))
    return img.filter(ImageFilter.GaussianBlur(size * 0.18 * s))


def _speckle(img, rng, n, colors, size, W, H, s):
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.uniform(*size) * s
        col = rng.choice(colors)
        for dx in _shifts(W, x - r, x + r):
            d.ellipse([x + dx - r, y - r * 0.6, x + dx + r, y + r * 0.6], fill=col)


def _city(d, x0, y0, w, h, s, rng, W):
    """Blocks of a city seen from above: streets, roofs and their shadows. / Une ville vue du ciel."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(120, 124, 128))
    bx = x0 + 6 * s
    while bx < x0 + w - 20 * s:
        bw = rng.uniform(40, 80) * s
        by = y0 + 6 * s
        while by < y0 + h - 20 * s:
            bh = rng.uniform(34, 70) * s
            d.rectangle([bx, by, bx + bw, by + bh], fill=(150, 152, 150))
            for _ in range(rng.randint(1, 3)):                           # immeubles sur l'îlot
                rw, rh = rng.uniform(12, bw * 0.6), rng.uniform(10, bh * 0.6)
                rx, ry = bx + rng.uniform(2 * s, bw - rw - 2 * s), by + rng.uniform(2 * s, bh - rh - 2 * s)
                tall = rng.uniform(3, 9) * s
                d.rectangle([rx + tall, ry + tall, rx + rw + tall, ry + rh + tall], fill=(70, 74, 80))
                roof = rng.choice(((210, 206, 196), (180, 186, 196), (196, 120, 90), (160, 170, 150), (230, 230, 224)))
                d.rectangle([rx, ry, rx + rw, ry + rh], fill=roof)
                d.line([(rx, ry), (rx + rw, ry)], fill=mix(roof, (255, 255, 255), 0.4), width=max(1, int(s)))
            if rng.random() < 0.15:                                      # un parc
                d.rectangle([bx + 3 * s, by + 3 * s, bx + bw - 3 * s, by + bh - 3 * s], fill=(80, 150, 70))
                for _ in range(5):
                    tx, ty = bx + rng.uniform(6 * s, bw - 6 * s), by + rng.uniform(6 * s, bh - 6 * s)
                    d.ellipse([tx - 5 * s, ty - 5 * s, tx + 5 * s, ty + 5 * s], fill=(50, 110, 50))
            by += bh + 8 * s
        bx += bw + 8 * s


AF_AVENUES = (103, 323)        # the two avenues across the city, in pixels at s = 1 (the scene puts its tanks there)


def af_car(color, s):
    """A small car seen from above, nose to the right. / Une petite voiture vue du dessus."""
    p = _Pic(int(30 * s), int(15 * s), 3)
    p.poly([(2 * s, 2 * s), (26 * s, 2 * s), (29 * s, 5 * s), (29 * s, 10 * s), (26 * s, 13 * s), (2 * s, 13 * s), (1 * s, 10 * s), (1 * s, 5 * s)],
           _rgba(color), (20, 20, 26, 255), 1 * s)
    p.poly([(18 * s, 3.5 * s), (22 * s, 3.5 * s), (22 * s, 11.5 * s), (18 * s, 11.5 * s)], (40, 54, 80, 255))
    p.poly([(5 * s, 4 * s), (8 * s, 4 * s), (8 * s, 11 * s), (5 * s, 11 * s)], (40, 54, 80, 255))
    p.poly([(9 * s, 4 * s), (17 * s, 4 * s), (17 * s, 11 * s), (9 * s, 11 * s)], _rgba(mix(color, (255, 255, 255), 0.3)))
    return p.done()


def _roof(d, x, y, w, h, s, rng, pal, W):
    """A flat roof seen from above with its shadow, parapet and what stands on it. / Un toit plat vu du ciel."""
    tall = rng.uniform(4, 14) * s
    roof = rng.choice(pal["roofs"])
    for dx in _shifts(W, x - 2, x + w + tall + 2):
        X = x + dx
        d.rectangle([X + tall, y + tall, X + w + tall, y + h + tall], fill=pal["shadow"])               # ombre portée
        d.rectangle([X, y, X + w, y + h], fill=roof)
        d.line([(X, y + h), (X, y), (X + w, y)], fill=mix(roof, (255, 255, 255), 0.35), width=max(1, int(2 * s)))
        d.line([(X + w, y), (X + w, y + h), (X, y + h)], fill=mix(roof, (0, 0, 0), 0.35), width=max(1, int(2 * s)))
    things = []
    for _ in range(rng.randint(0, 4)):
        kind = rng.random()
        if kind < 0.45 and w > 26 * s and h > 20 * s:                   # climatiseur
            uw, uh = rng.uniform(8, 16) * s, rng.uniform(6, 10) * s
            ux, uy = x + rng.uniform(4 * s, w - uw - 4 * s), y + rng.uniform(4 * s, h - uh - 4 * s)
            things.append(("box", ux, uy, uw, uh))
        elif kind < 0.7 and w > 24 * s and h > 24 * s:                  # château d'eau
            r = rng.uniform(4, 7) * s
            things.append(("tank", x + rng.uniform(r + 4 * s, w - r - 4 * s), y + rng.uniform(r + 4 * s, h - r - 4 * s), r, 0))
        elif kind < 0.76 and w > 70 * s and h > 70 * s and rng.random() < 0.35:     # hélistation, rare
            things.append(("pad", x + w / 2, y + h / 2, min(w, h) * 0.32, 0))
        elif w > 20 * s and h > 16 * s:                                 # cage d'escalier
            things.append(("stair", x + rng.uniform(3 * s, w - 14 * s), y + rng.uniform(3 * s, h - 12 * s), 11 * s, 9 * s))
    for kind, a, b, c, e in things:
        for dx in _shifts(W, a - 30 * s, a + 30 * s):
            if kind == "box":
                d.rectangle([a + dx + 2 * s, b + 2 * s, a + dx + c + 2 * s, b + e + 2 * s], fill=mix(roof, (0, 0, 0), 0.4))
                d.rectangle([a + dx, b, a + dx + c, b + e], fill=pal["unit"])
                for k in range(1, int(c / (3 * s))):
                    d.line([(a + dx + k * 3 * s, b + 1 * s), (a + dx + k * 3 * s, b + e - 1 * s)], fill=mix(pal["unit"], (0, 0, 0), 0.3), width=1)
            elif kind == "tank":
                d.ellipse([a + dx - c + 2 * s, b - c + 2 * s, a + dx + c + 2 * s, b + c + 2 * s], fill=mix(roof, (0, 0, 0), 0.4))
                d.ellipse([a + dx - c, b - c, a + dx + c, b + c], fill=pal["unit"], outline=mix(pal["unit"], (0, 0, 0), 0.35))
                d.ellipse([a + dx - c * 0.4, b - c * 0.4, a + dx + c * 0.4, b + c * 0.4], fill=mix(pal["unit"], (255, 255, 255), 0.3))
            elif kind == "pad":
                d.ellipse([a + dx - c, b - c, a + dx + c, b + c], fill=pal["pad"], outline=(240, 240, 240), width=max(1, int(2 * s)))
                k = c * 0.45
                for xx in (a - k * 0.6, a + k * 0.6):
                    d.line([(xx + dx, b - k), (xx + dx, b + k)], fill=(240, 240, 240), width=max(2, int(3 * s)))
                d.line([(a + dx - k * 0.6, b), (a + dx + k * 0.6, b)], fill=(240, 240, 240), width=max(2, int(3 * s)))
            else:
                d.rectangle([a + dx, b, a + dx + c, b + e], fill=mix(roof, (0, 0, 0), 0.2), outline=mix(roof, (0, 0, 0), 0.45))


def _lot(img, d, x, y, w, h, s, rng, pal, W, cars):
    """A car park: white lines and parked cars. / Un parking : lignes blanches et voitures garées."""
    for dx in _shifts(W, x - 2, x + w + 2):
        d.rectangle([x + dx, y, x + dx + w, y + h], fill=pal["lot"])
    rows = max(1, int(h / (34 * s)))
    for r in range(rows):
        ry = y + 4 * s + r * 34 * s
        sx = x + 4 * s
        while sx + 16 * s < x + w - 4 * s:
            for dx in _shifts(W, sx - 2, sx + 20 * s):
                d.line([(sx + dx, ry), (sx + dx, ry + 28 * s)], fill=pal["paint"], width=max(1, int(s)))
            if rng.random() < 0.7:
                car = rng.choice(cars)
                cw, ch = car.size
                rot = car.rotate(90 if rng.random() < 0.5 else 270, expand=True)
                for dx in _shifts(W, sx, sx + 16 * s):
                    img.paste(rot, (int(sx + dx + 1 * s), int(ry + 1 * s)), rot)
            sx += 17 * s


def _park(d, x, y, w, h, s, rng, pal, W):
    """A small park: grass, a path, round trees with their shadows. / Un petit parc, des arbres ronds."""
    for dx in _shifts(W, x - 2, x + w + 2):
        d.rectangle([x + dx, y, x + dx + w, y + h], fill=pal["grass"])
        d.line([(x + dx, y + h * 0.6), (x + dx + w, y + h * 0.4)], fill=pal["path"], width=max(2, int(5 * s)))
    for _ in range(int(w * h / (380 * s * s))):
        tx, ty = x + rng.uniform(6 * s, w - 6 * s), y + rng.uniform(6 * s, h - 6 * s)
        r = rng.uniform(5, 10) * s
        for dx in _shifts(W, tx - r, tx + r + 4 * s):
            d.ellipse([tx + dx - r + 3 * s, ty - r + 3 * s, tx + dx + r + 3 * s, ty + r + 3 * s], fill=pal["shadow"])
            d.ellipse([tx + dx - r, ty - r, tx + dx + r, ty + r], fill=rng.choice(pal["trees"]))
            d.ellipse([tx + dx - r * 0.6, ty - r * 0.7, tx + dx + r * 0.1, ty - r * 0.1], fill=mix(pal["trees"][0], (255, 255, 255), 0.25))


def _topdown_city(tw, H, s, rng, pal, river=None):
    """A city seen from high above: two avenues along the way, streets across, blocks of roofs, car parks and parks,
    crossings, a river with its bridges if asked. Returns the picture, the street lamps and the red lights on the roofs.
    / Une ville vue du ciel : deux avenues, des rues, des toits, des parkings, des parcs, une rivière et ses ponts."""
    img = Image.new("RGB", (tw, H), pal["street"])
    d = ImageDraw.Draw(img)
    cars = [af_car(c, s) for c in pal["cars"]]
    lamps, blinks = [], []
    av = [a * s for a in AF_AVENUES]
    aw = 46 * s
    rows = [(0, av[0] - aw / 2), (av[0] + aw / 2, av[1] - aw / 2), (av[1] + aw / 2, H)]
    xs = []
    x = 0.0
    while x < tw - 160 * s:
        xs.append(x)
        x += rng.uniform(220, 380) * s
    xs.append(tw)
    sw = 26 * s                                                          # rues en travers
    for r, (y0, y1) in enumerate(rows):
        if river is not None and r == river:                             # la rivière, ses quais, ses berges plantées et ses ponts
            m = (y1 - y0) * 0.2
            d.rectangle([0, y0, tw, y1], fill=pal["grass"])
            for _ in range(int(tw / (9 * s))):                           # arbres sur les berges
                tx = rng.uniform(0, tw)
                ty = rng.uniform(y0 + 4 * s, y0 + m - 8 * s) if rng.random() < 0.5 else rng.uniform(y1 - m + 8 * s, y1 - 4 * s)
                rr = rng.uniform(4, 8) * s
                d.ellipse([tx - rr + 2 * s, ty - rr + 2 * s, tx + rr + 2 * s, ty + rr + 2 * s], fill=pal["shadow"])
                d.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], fill=rng.choice(pal["trees"]))
            d.rectangle([0, y0 + m, tw, y1 - m], fill=pal["quay"])
            d.rectangle([0, y0 + m + 6 * s, tw, y1 - m - 6 * s], fill=pal["water"])
            for _ in range(int(tw / (14 * s))):
                wx, wy = rng.uniform(0, tw), rng.uniform(y0 + m + 10 * s, y1 - m - 10 * s)
                d.line([(wx, wy), (wx + rng.uniform(8, 20) * s, wy)], fill=mix(pal["water"], (255, 255, 255), 0.18), width=max(1, int(s)))
            for bx in xs[:-1]:
                d.rectangle([bx - 4 * s, y0, bx + sw + 4 * s, y1], fill=pal["bridge"])
                d.rectangle([bx + 2 * s, y1 - m - 6 * s, bx + sw + 10 * s, y1 - m + 2 * s], fill=pal["shadow"])
                d.line([(bx - 4 * s, y0), (bx - 4 * s, y1)], fill=mix(pal["bridge"], (255, 255, 255), 0.3), width=max(1, int(2 * s)))
                d.line([(bx + sw + 4 * s, y0), (bx + sw + 4 * s, y1)], fill=mix(pal["bridge"], (0, 0, 0), 0.3), width=max(1, int(2 * s)))
                for k in range(int((y1 - y0) / (16 * s))):
                    d.line([(bx + sw / 2, y0 + k * 16 * s + 4 * s), (bx + sw / 2, y0 + k * 16 * s + 10 * s)], fill=pal["paint"], width=max(1, int(s)))
            continue
        for i in range(len(xs) - 1):
            bx0, bx1 = xs[i] + sw, xs[i + 1]
            d.rectangle([bx0, y0 + 2 * s, bx1, y1 - 2 * s], fill=pal["walk"])                         # trottoir
            ix0, iy0, ix1, iy1 = bx0 + 6 * s, y0 + 8 * s, bx1 - 6 * s, y1 - 8 * s
            if ix1 - ix0 < 30 * s or iy1 - iy0 < 20 * s:
                continue
            what = rng.random()
            if what < 0.14:
                _park(d, ix0, iy0, ix1 - ix0, iy1 - iy0, s, rng, pal, tw)
            elif what < 0.3:
                _lot(img, d, ix0, iy0, ix1 - ix0, iy1 - iy0, s, rng, pal, tw, cars)
            else:                                                        # des immeubles
                x0 = ix0
                while x0 < ix1 - 24 * s:
                    w = min(ix1 - x0, rng.uniform(40, 120) * s)
                    y0b = iy0
                    while y0b < iy1 - 18 * s:
                        h = min(iy1 - y0b, rng.uniform(30, 110) * s)
                        _roof(d, x0 + 2 * s, y0b + 2 * s, w - 16 * s, h - 16 * s, s, rng, pal, tw)
                        if rng.random() < 0.12:
                            blinks.append((x0 + w * 0.4, y0b + h * 0.4))
                        y0b += h
                    x0 += w
    for a in av:                                                         # les avenues
        d.rectangle([0, a - aw / 2, tw, a + aw / 2], fill=pal["street"])
        d.line([(0, a - 1.5 * s), (tw, a - 1.5 * s)], fill=pal["yellow"], width=max(1, int(2 * s)))
        d.line([(0, a + 1.5 * s), (tw, a + 1.5 * s)], fill=pal["yellow"], width=max(1, int(2 * s)))
        for lane in (a - aw / 4, a + aw / 4):
            for x in range(0, tw, int(40 * s)):
                d.line([(x, lane), (x + 20 * s, lane)], fill=pal["paint"], width=max(1, int(2 * s)))
        for x in range(int(60 * s), tw, int(160 * s)):                    # réverbères
            lamps.append((x, a - aw / 2 - 3 * s))
            lamps.append((x + 80 * s, a + aw / 2 + 3 * s))
    for bx in xs[:-1]:                                                   # passages piétons aux carrefours
        for a in av:
            for k in range(6):
                yy = a - aw / 2 + 4 * s + k * 7 * s
                d.rectangle([bx - 12 * s, yy, bx - 4 * s, yy + 4 * s], fill=pal["paint"])
                d.rectangle([bx + sw + 4 * s, yy, bx + sw + 12 * s, yy + 4 * s], fill=pal["paint"])
    return img, lamps, blinks


def hook_traffic(bd, screen, b, L, now, dt):
    """Cars driving along the two avenues, both ways. / Des voitures qui roulent sur les deux avenues."""
    st = bd.amb_state.setdefault("_traffic", None)
    W, s = bd.W, bd.s
    lanes = [(a + k * 11.5) * s for a in AF_AVENUES for k in (-1, 1)]
    if st is None:
        st = bd.amb_state["_traffic"] = [[bd.rng.uniform(0, W), i % 4, bd.rng.choice(("car0", "car1", "car2", "car3")),
                                          bd.rng.uniform(40, 120) * s] for i in range(12)]
    for c in st:
        way = -1 if c[1] % 2 == 0 else 1                                 # sens de la voie
        c[0] += (way * c[3] - bd.speed) * dt
        if c[0] < -60 * s:
            c[0] = W + bd.rng.uniform(20, 400) * s
        elif c[0] > W + 500 * s:
            c[0] = -50 * s
        img = b["imgs"][c[2] + ("l" if way < 0 else "")]
        screen.blit(img, (int(c[0] - img.get_width() / 2), int(lanes[c[1]] - img.get_height() / 2)))


def _af_pal(night):
    if not night:
        return {"street": (84, 88, 96), "walk": (150, 152, 156), "paint": (226, 226, 222), "yellow": (230, 190, 60),
                "roofs": ((128, 134, 146), (150, 150, 156), (110, 118, 132), (170, 166, 156), (138, 144, 130), (100, 106, 118), (186, 182, 170)),
                "shadow": (52, 54, 62), "unit": (196, 198, 204), "pad": (70, 80, 70), "lot": (96, 100, 106), "grass": (88, 140, 76),
                "path": (190, 180, 150), "trees": ((54, 110, 56), (64, 124, 60), (46, 98, 50)),
                "cars": ((210, 60, 50), (60, 100, 200), (230, 230, 230), (220, 190, 60)),
                "water": (50, 96, 150), "quay": (150, 146, 136), "bridge": (120, 120, 126)}
    return {"street": (62, 56, 84), "walk": (110, 100, 130), "paint": (200, 196, 214), "yellow": (210, 170, 80),
            "roofs": ((92, 84, 120), (110, 100, 134), (80, 74, 106), (124, 112, 140), (98, 96, 120), (70, 66, 96)),
            "shadow": (34, 30, 50), "unit": (150, 144, 170), "pad": (60, 70, 70), "lot": (70, 64, 92), "grass": (56, 92, 70),
            "path": (130, 120, 140), "trees": ((40, 80, 60), (48, 92, 66), (34, 70, 54)),
            "cars": ((200, 60, 60), (70, 100, 190), (210, 210, 220), (210, 180, 70)),
            "water": (36, 44, 92), "quay": (100, 92, 120), "bridge": (96, 90, 116)}


def build_af_city(W, H, s, seed=57):
    """Aero Fighters 2: a city seen from high above in daylight, as in the game: grey roofs and their shadows, avenues
    with their cars, streets, car parks, parks. / Une ville vue du ciel en plein jour, comme dans le jeu."""
    rng = random.Random(seed)
    tw = 2 * W
    pal = _af_pal(False)
    ground, lamps, blinks = _topdown_city(tw, H, s, rng, pal)
    images = {}
    for i, c in enumerate(pal["cars"]):
        car = af_car(c, s)
        images[f"car{i}"], images[f"car{i}l"] = car, car.transpose(Image.FLIP_LEFT_RIGHT)
    layers = [{"img": ground.convert("RGBA"), "y": 0, "f": 1.0, "stage": "far"}]
    return {"sky": Image.new("RGB", (W, H), pal["street"]), "layers": layers, "tw": tw, "amb": {"images": images, "hooks": {"far": [hook_traffic]}}}


def build_af_night(W, H, s, seed=58):
    """Aero Fighters 3: a city by a river at nightfall, as in the game: purple roofs, a river with its quays and bridges,
    lamps along the avenues, red lights on the roofs, cars. / Une ville au bord d'un fleuve à la tombée de la nuit."""
    rng = random.Random(seed)
    tw = 2 * W
    pal = _af_pal(True)
    ground, lamps, blinks = _topdown_city(tw, H, s, rng, pal, river=1)
    images = {}
    for i, c in enumerate(pal["cars"]):
        car = af_car(c, s)
        images[f"car{i}"], images[f"car{i}l"] = car, car.transpose(Image.FLIP_LEFT_RIGHT)
    layers = [{"img": ground.convert("RGBA"), "y": 0, "f": 1.0, "stage": "far", "lights": lamps, "blinks": blinks}]
    return {"sky": Image.new("RGB", (W, H), pal["street"]), "layers": layers, "tw": tw,
            "amb": {"images": images, "window": (255, 220, 150), "blink": (255, 50, 40), "hooks": {"far": [hook_traffic]}}}


hd_bg.BUILDERS.update({"th_forest": build_th_forest, "th_ice": build_th_ice, "th_wind": build_th_wind, "th_fire": build_th_fire,
                       "ballpark": build_ballpark, "lr_city": build_lr_city, "af_city": build_af_city, "af_night": build_af_night})
