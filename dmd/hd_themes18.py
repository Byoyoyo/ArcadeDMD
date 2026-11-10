"""The nine stages of The King of Fighters '98 (1.32 test 9), drawn by the program from the pictures and the
descriptions of the stages: the street under the viaduct in Osaka, the boat on the river in China, the harbor in Korea, the
market in the Middle East, the Court of the Lions in Spain, the train yard and the wharf in the USA, the ruined dojo in the
forest in Japan, the Black Noah. Each changes with the rounds as in the game (the time of day, a fog, the cars, a wagon,
the light growing bluer) and has its own animations. They register in hd_bg.BUILDERS when this module is imported (by
hd_fight). No image comes from the game.

Les neuf décors de The King of Fighters '98, dessinés par le programme d'après les images et les descriptions des
stages. Chacun change avec les rounds comme dans le jeu (l'heure du jour, la brume, les voitures, un wagon, la lumière qui
bleuit) et a ses animations. Aucune image ne vient du jeu.
"""

import math
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from . import hd_bg
from .hd_bg import crowd_layers, mix, radial, add_at, vgrad
from .hd_stages import gull_img, hook_gulls, stars_on


# ---------------------------------------------------------------------------- drawing / dessin
# the look of the stages: "flat" (as drawn), or "cartoon", every shape inked with a dark outline, the colours brighter
# and bolder (1.33) / le style des décors : "flat", ou "cartoon", chaque forme cernée d'un trait sombre, les couleurs
# plus vives
STYLE = {"name": "cartoon", "ink": (30, 20, 34), "width": 3.6, "min": 12, "saturation": 1.3, "contrast": 1.06,
         "wobble": 0.7, "shade": 0.8, "shade_from": 0.62, "bands": 5}
# ink: the colour of the outline; width: its width (screen units); min: no outline on a shape smaller than this; wobble:
# the hand's unsteadiness on the outline; shade: the flat shadow on the lower part of a shape (darker by this), from
# shade_from of its height; bands: the flat bands of a sky / ink : la couleur du trait ; width : son épaisseur ; min :
# pas de trait sous cette taille ; wobble : le tremblement de la main ; shade : l'ombre en aplat sur le bas d'une forme,
# à partir de shade_from de sa hauteur ; bands : les bandes plates d'un ciel


class Pic:
    """A picture drawn twice as big then reduced (smooth edges), in units of the 1920 x 460 screen. wrap: the shapes that
    cross an edge come back on the other side (a layer that scrolls). / Une image dessinée deux fois plus grande puis
    réduite, en unités de l'écran 1920 x 460 ; wrap : ce qui dépasse d'un bord revient de l'autre côté."""

    def __init__(self, w, h, s, ss=2, wrap=False, ink=None):
        self.w, self.h, self.s, self.ss, self.wrap = w, h, s, ss, wrap
        self.k = s * ss
        self.img = Image.new("RGBA", (max(1, round(w * self.k)), max(1, round(h * self.k))), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        self.ink = (STYLE["name"] == "cartoon") if ink is None else ink   # outlines on this picture / cernés ici

    def _inked(self, xs, ys, fill):
        """Whether this shape gets its outline: big enough, and not see-through. / Si la forme est cernée."""
        if not self.ink or (len(fill) == 4 and fill[3] < 255):
            return False
        return max(xs) - min(xs) >= STYLE["min"] and max(ys) - min(ys) >= STYLE["min"]

    def _ink_w(self):
        return max(1, round(STYLE["width"] * self.k))

    def _wobbly(self, q):
        """The outline as a hand draws it: the vertices nudged a little, the long edges bent. / Le trait comme à la
        main : les sommets un peu décalés, les longs côtés fléchis."""
        w = STYLE["wobble"] * self.k
        if w <= 0:
            return q + [q[0]]
        rng = random.Random(int(q[0][0] * 7 + q[0][1] * 13 + len(q)))
        out = []
        n = len(q)
        for i in range(n + 1):
            x0, y0 = q[i % n]
            x1, y1 = q[(i + 1) % n]
            out.append((x0 + rng.uniform(-w, w), y0 + rng.uniform(-w, w)))
            d = math.hypot(x1 - x0, y1 - y0)
            steps = int(d / (40 * self.k))
            for j in range(1, steps + 1):
                t = j / (steps + 1)
                out.append((x0 + (x1 - x0) * t + rng.uniform(-w, w), y0 + (y1 - y0) * t + rng.uniform(-w, w)))
        return out

    def _outline(self, q):
        self.d.line(self._wobbly(q), fill=_c(STYLE["ink"]), width=self._ink_w(), joint="curve")

    def _shade(self, q, fill):
        """The flat shadow on the lower part of the shape. / L'ombre en aplat sur le bas de la forme."""
        if not STYLE.get("shade") or STYLE["shade"] >= 1 or (len(fill) == 4 and fill[3] < 255):
            return
        xs, ys = [p[0] for p in q], [p[1] for p in q]
        bx0, bx1 = max(0, int(min(xs)) - 1), min(self.img.width, int(max(xs)) + 2)
        by0, by1 = max(0, int(min(ys)) - 1), min(self.img.height, int(max(ys)) + 2)
        if bx1 <= bx0 or by1 <= by0:
            return
        top = min(ys) + (max(ys) - min(ys)) * STYLE["shade_from"]
        m = Image.new("L", (bx1 - bx0, by1 - by0), 0)
        md = ImageDraw.Draw(m)
        md.polygon([(x - bx0, y - by0) for x, y in q], fill=255)
        if top - by0 > 0:
            md.rectangle([0, 0, bx1 - bx0, top - by0], fill=0)
        self.img.paste(_c(shade(fill, STYLE["shade"])), (bx0, by0), m)

    def plain(self):
        """Textures (stones, plaster, lattices) are never inked. / Les textures ne sont jamais cernées."""
        return _Plain(self)

    def _dxs(self, xs):
        if not self.wrap:
            return (0,)
        lo, hi = min(xs), max(xs)
        return [dx for dx in (-self.w, 0, self.w) if hi + dx >= -2 and lo + dx <= self.w + 2]

    def _p(self, pts, dx):
        k = self.k
        return [((x + dx) * k, y * k) for x, y in pts]

    def poly(self, pts, fill):
        ink = self._inked([p[0] for p in pts], [p[1] for p in pts], fill)
        for dx in self._dxs([p[0] for p in pts]):
            q = self._p(pts, dx)
            self.d.polygon(q, fill=_c(fill))
            if ink:
                self._shade(q, fill)
                self._outline(q)

    def rect(self, x0, y0, x1, y1, fill):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill)

    def ellipse(self, x0, y0, x1, y1, fill):
        k = self.k
        ink = self._inked([x0, x1], [y0, y1], fill)
        for dx in self._dxs([x0, x1]):
            box = [(x0 + dx) * k, y0 * k, (x1 + dx) * k, y1 * k]
            self.d.ellipse(box, fill=_c(fill))
            if ink:
                cx, cy, rx, ry = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, (box[2] - box[0]) / 2, (box[3] - box[1]) / 2
                q = [(cx + rx * math.cos(a * math.tau / 36), cy + ry * math.sin(a * math.tau / 36)) for a in range(36)]
                self._shade(q, fill)
                self._outline(q)

    def line(self, pts, width, fill):
        for dx in self._dxs([p[0] for p in pts]):
            self.d.line(self._p(pts, dx), fill=_c(fill), width=max(1, round(width * self.k)), joint="curve")

    def arc_poly(self, cx, cy, rx, ry, a0, a1, n=24):
        """Points of an elliptic arc (degrees, 0 = right, 90 = down). / Points d'un arc."""
        return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
                for i in range(n + 1)]

    def gpoly(self, pts, stops, y0=None, y1=None):
        """A polygon filled with a vertical gradient, stops [(0..1, colour)] from y0 to y1 (its top and bottom by
        default). / Un polygone rempli d'un dégradé vertical."""
        ys = [p[1] for p in pts]
        y0 = min(ys) if y0 is None else y0
        y1 = max(ys) if y1 is None else y1
        if STYLE["name"] == "cartoon" and all(len(c) < 4 or c[3] >= 255 for _, c in stops):
            self.poly(pts, _stop(stops, 0.35)[:3])                  # a flat tone, its shadow below / un aplat, son ombre
            return
        for dx in self._dxs([p[0] for p in pts]):
            q = self._p(pts, dx)
            bx0 = max(0, int(min(p[0] for p in q)) - 1)
            bx1 = min(self.img.width, int(max(p[0] for p in q)) + 2)
            by0 = max(0, int(min(p[1] for p in q)) - 1)
            by1 = min(self.img.height, int(max(p[1] for p in q)) + 2)
            if bx1 <= bx0 or by1 <= by0:
                continue
            m = Image.new("L", (bx1 - bx0, by1 - by0), 0)
            ImageDraw.Draw(m).polygon([(x - bx0, y - by0) for x, y in q], fill=255)
            col = Image.new("RGBA", (1, by1 - by0))
            for yy in range(by1 - by0):
                yu = (yy + by0) / self.k
                t = 0.0 if y1 <= y0 else max(0.0, min(1.0, (yu - y0) / (y1 - y0)))
                col.putpixel((0, yy), _c(_stop(stops, t)))
            g = col.resize((bx1 - bx0, by1 - by0), Image.NEAREST)
            region = self.img.crop((bx0, by0, bx1, by1))
            if all(len(c) < 4 or c[3] >= 255 for _, c in stops):
                region.paste(g, (0, 0), m)                         # opaque: replaces / opaque : remplace
            else:                                                  # see-through: laid over / transparent : posé dessus
                a = Image.composite(g.getchannel("A"), Image.new("L", g.size, 0), m)
                g.putalpha(a)
                region = Image.alpha_composite(region, g)
            self.img.paste(region, (bx0, by0))
            if self._inked([p[0] for p in pts], ys, stops[0][1]):
                self._shade(q, stops[0][1])
                self._outline(q)

    def grect(self, x0, y0, x1, y1, stops):
        self.gpoly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], stops)

    def glow(self, cx, cy, r, color, strength=1.0):
        """Light added where the picture is already drawn (lamps, windows). / Une lumière ajoutée sur ce qui est dessiné."""
        size = max(4, int(2 * r * self.k))
        g = radial(size, color, 2.0, strength)
        a = self.img.getchannel("A")
        rgb = self.img.convert("RGB")
        add_at(rgb, g, cx * self.k, cy * self.k)
        self.img = Image.merge("RGBA", (*rgb.split(), a))
        self.d = ImageDraw.Draw(self.img)

    def blur(self, r):
        """Softens the whole picture (mist, glows). / Adoucit toute l'image (brume, halos)."""
        self.img = self.img.filter(ImageFilter.GaussianBlur(r * self.k))
        self.d = ImageDraw.Draw(self.img)

    def done(self):
        img = self.img.resize((max(1, round(self.w * self.s)), max(1, round(self.h * self.s))), Image.LANCZOS)
        return toon(img) if STYLE["name"] == "cartoon" else img


def toon(img):
    """The colours of the cartoon look: brighter, bolder. / Les couleurs du style cartoon : plus vives."""
    if STYLE["name"] != "cartoon":
        return img
    a = img.getchannel("A") if img.mode == "RGBA" else None
    rgb = ImageEnhance.Color(img.convert("RGB")).enhance(STYLE["saturation"])
    rgb = ImageEnhance.Contrast(rgb).enhance(STYLE["contrast"])
    return Image.merge("RGBA", (*rgb.split(), a)) if a is not None else rgb


class _Plain:
    def __init__(self, pic):
        self.pic = pic

    def __enter__(self):
        self.was = self.pic.ink
        self.pic.ink = False

    def __exit__(self, *a):
        self.pic.ink = self.was


def _c(c):
    return tuple(int(v) for v in c) if len(c) == 4 else tuple(int(v) for v in c) + (255,)


def _stop(stops, t):
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if p0 <= t <= p1:
            k = (t - p0) / max(1e-6, p1 - p0)
            a0 = c0[3] if len(c0) == 4 else 255
            a1 = c1[3] if len(c1) == 4 else 255
            return mix(c0, c1, k) + (int(a0 + (a1 - a0) * k),)
    c = stops[-1][1] if t >= stops[-1][0] else stops[0][1]
    return tuple(c[:3]) + ((c[3],) if len(c) == 4 else (255,))


def shade(c, k):
    """A colour darker (k < 1) or lighter (k > 1). / Une couleur plus sombre ou plus claire."""
    if k <= 1:
        return tuple(int(v * k) for v in c[:3])
    return tuple(int(v + (255 - v) * (k - 1)) for v in c[:3])


def layer(pic, stage, f=0.0, crop=True, **kw):
    """A layer of a stage from a picture, cut to what is drawn (the rows above and below it). / Une couche, coupée à ce
    qui est dessiné."""
    img = pic.done()
    y = 0
    if crop:
        box = img.getchannel("A").getbbox()
        if box:
            y = box[1]
            img = img.crop((0, box[1], img.width, box[3]))
    out = {"img": img, "y": y, "f": f, "stage": stage}
    out.update(kw)
    return out


def sky_img(W, H, stops, s, stars=0, seed=1, clouds=None):
    """A sky: a gradient, its stars, its clouds [(y0, y1, colour, alpha, n)]. / Un ciel."""
    cartoon = STYLE["name"] == "cartoon"
    if cartoon:                                                      # flat bands of colour / des bandes plates
        n = STYLE["bands"]
        sky = Image.new("RGB", (W, H))
        d = ImageDraw.Draw(sky)
        for i in range(n):
            d.rectangle([0, int(H * i / n), W, int(H * (i + 1) / n) + 1], fill=_stop(stops, (i + 0.5) / n)[:3])
    else:
        sky = vgrad(W, H, stops)
    rng = random.Random(seed)
    if stars:
        stars_on(sky, rng, stars, H * 0.45, W)
    for (y0, y1, col, alpha, n) in clouds or ():
        over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(over)
        if cartoon:                                                  # round clouds, inked / des nuages ronds, cernés
            pc = Pic(W / s, H / s, s, ink=True)
            for _ in range(n):
                x, y = rng.uniform(-100, W / s), rng.uniform(y0, y1)
                w = rng.uniform(120, 260)
                lobes = [(x + (k - 2) * w * 0.2, y - (14 if k % 2 else 4) - (k == 2) * 10, w * rng.uniform(0.12, 0.2)) for k in range(5)]
                pc.rect(x - w * 0.42, y - 6, x + w * 0.42, y + 14, col)
                for lx, ly, r in lobes:
                    pc.ellipse(lx - r, ly - r, lx + r, ly + r * 0.9, col)
                with pc.plain():                                     # the lobes joined, no inner lines / sans traits
                    pc.rect(x - w * 0.42, y - 4, x + w * 0.42, y + 11, col)
                    for lx, ly, r in lobes:
                        pc.ellipse(lx - r + 3, ly - r + 3, lx + r - 3, ly + r * 0.9 - 2, col)
            over = pc.img.resize((W, H), Image.LANCZOS)
            sky.paste(over, (0, 0), over)
            continue
        for _ in range(n):
            x, y = rng.uniform(-100 * s, W), rng.uniform(y0 * s, y1 * s)
            w = rng.uniform(140, 360) * s
            for k in range(7):
                dx = (k - 3) * w * 0.14
                r = w * rng.uniform(0.1, 0.2)
                d.ellipse([x + dx - r, y - r * 0.7 - (k % 3) * 3 * s, x + dx + r, y + r * 0.45], fill=col + (alpha,))
        over = over.filter(ImageFilter.GaussianBlur(2 * s))
        sky.paste(over, (0, 0), over)
    return toon(sky)


def fight_stage(builder):
    """The stage with its crowd in front, the layers kept where they are (the boat drifts by itself). / Le décor avec
    son public devant."""
    def build(W, H, s, seed=None):
        th = builder(W, H, s)
        th["layers"] += crowd_layers(th["tw"], H, s, random.Random(77))
        th["amb"] = dict(th["amb"], crowd=(H - 118 * s, H - 30 * s))
        return th
    return build


# ---------------------------------------------------------------------------- animations
_GLOWS = {}


def _glow(bd, r, color, lv):
    key = (int(r), color, int(lv * 4))
    g = _GLOWS.get(key)
    if g is None:
        g = _GLOWS[key] = bd.fx.sp.glow(r, color, lv, hot=0.4)
    return g


def hook_lamps(bd, screen, b, L, now, dt):
    """The lamps of the stage, lit in the looks that say it (at night), with a slight flicker. / Les lampes du décor,
    allumées dans les looks qui le disent (la nuit)."""
    amb = b["amb"]
    on = amb.get("lamps_on")
    look = bd.cur_look
    time = look.split("+")[0] if look else None
    lv = 1.0
    if on is not None:
        lv = 1.0 if time in on else 0.0
        if bd.look_prev is not None:
            prev = bd.look_prev.split("+")[0]
            lv = lv * bd.look_k + (1.0 if prev in on else 0.0) * (1 - bd.look_k)
    if lv <= 0.02:
        return
    add = bd.pg.BLEND_RGB_ADD
    s = bd.s
    for i, lamp in enumerate(amb.get("lamps", ())):
        x, y, r, col, strength = lamp[:5]
        w = lv
        if len(lamp) > 5:                                          # a lamp of some looks only (headlights...) / de certains looks
            w *= bd._shown({"only": lamp[5]}, look) * bd.look_k + (
                bd._shown({"only": lamp[5]}, bd.look_prev) * (1 - bd.look_k) if bd.look_prev is not None else 0.0)
            if w <= 0.02:
                continue
        fl = 1.0 + 0.06 * math.sin(now * 9 + i * 1.7) + 0.04 * math.sin(now * 23 + i)
        g = _glow(bd, r * s, col, 6 * strength * w * fl)
        screen.blit(g, (int(x * s - g.get_width() / 2), int(y * s - g.get_height() / 2)), special_flags=add)


def hook_fireflies(bd, screen, b, L, now, dt):
    """Fireflies floating in the looks that have them. / Des lucioles dans les looks qui en ont."""
    look = bd.cur_look or ""
    if look.split("+")[0] not in b["amb"].get("flies_on", ("night",)):
        return
    st = bd.amb_state.setdefault("_flies", None)
    W, H, s = bd.W, bd.H, bd.s
    rng = bd.rng
    if st is None:
        st = bd.amb_state["_flies"] = [[rng.uniform(0, W), rng.uniform(H * 0.25, H * 0.8), rng.uniform(0, 6), rng.uniform(0.5, 1.5)]
                                       for _ in range(30)]
    add = bd.pg.BLEND_RGB_ADD
    for f in st:
        f[0] += math.sin(now * 0.6 * f[3] + f[2]) * 20 * s * dt
        f[1] += math.cos(now * 0.8 * f[3] + f[2] * 2) * 14 * s * dt
        lv = max(0.0, math.sin(now * 1.9 * f[3] + f[2])) * 8
        if lv > 0.6:
            g = _glow(bd, 8 * s, (200, 255, 130), lv)
            screen.blit(g, (int(f[0] - g.get_width() / 2), int(f[1] - g.get_height() / 2)), special_flags=add)


def hook_sparkles(bd, screen, b, L, now, dt):
    """Little glints that come and go (copper pots, water). / De petits éclats qui vont et viennent (cuivres, eau)."""
    pts = b["amb"].get("sparkles")
    if not pts:
        return
    add = bd.pg.BLEND_RGB_ADD
    s = bd.s
    slot = int(now * 6)
    for i in range(min(8, len(pts))):
        r = random.Random(slot * 977 + i)
        x, y, col = pts[r.randrange(len(pts))]
        lv = r.uniform(2, 7) * (0.5 + 0.5 * math.sin((now * 6 - slot) * math.pi))
        if lv > 1:
            g = _glow(bd, 6 * s, col, lv)
            screen.blit(g, (int(x * s - g.get_width() / 2), int(y * s - g.get_height() / 2)), special_flags=add)


def _bush(p, x, y, r, rng, base):
    """A clump of leaves: small overlapping lobes, darker below, lighter above. / Une touffe de feuilles."""
    p.ellipse(x - r, y - r * 0.55, x + r, y + r * 0.6, shade(base, 0.72))
    for _ in range(9):
        a = rng.uniform(0, math.tau)
        d = rng.uniform(0, r * 0.7)
        cx, cy = x + math.cos(a) * d, y + math.sin(a) * d * 0.6
        rr = r * rng.uniform(0.3, 0.5)
        up = (y - cy) / max(1.0, r)
        p.ellipse(cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.7, shade(base, 0.9 + 0.35 * max(-0.4, up) + rng.uniform(-0.06, 0.06)))


# ============================================================================ Spain, the Court of the Lions / Espagne
def _arabesque(p, x0, y0, x1, y1, base, s, step=22):
    """The carved plaster of the Alhambra: a lattice of lobes and diamonds. / Le plâtre sculpté : losanges et lobes."""
    p.rect(x0, y0, x1, y1, base)
    hi, lo = shade(base, 1.25), shade(base, 0.62)
    y = y0
    row = 0
    was, p.ink = p.ink, False                                      # a texture / une texture
    while y < y1 + step:
        x = x0 - (step / 2 if row % 2 else 0)
        while x < x1 + step:
            p.poly([(x, y - step * 0.42), (x + step * 0.42, y), (x, y + step * 0.42), (x - step * 0.42, y)], lo)
            p.poly([(x, y - step * 0.3), (x + step * 0.3, y), (x, y + step * 0.3), (x - step * 0.3, y)], hi)
            p.ellipse(x - step * 0.12, y - step * 0.12, x + step * 0.12, y + step * 0.12, lo)
            x += step
        y += step / 2
        row += 1
    p.ink = was


def _fountain(p, cx, base, s):
    """The fountain of the lions: the basin on its ring of lions, the bowl, the column. / La fontaine aux lions."""
    marble, dark = (236, 232, 222), (170, 165, 150)
    for k in range(12):                                            # the lions around / les lions autour
        a = math.radians(180 + k * 15)
        x = cx + math.cos(a) * 80
        p.rect(x - 9, base - 22, x + 9, base, (214, 196, 160))
        p.ellipse(x - 9, base - 30, x + 9, base - 14, (214, 196, 160))
    p.gpoly([(cx - 96, base - 30), (cx + 96, base - 30), (cx + 84, base - 14), (cx - 84, base - 14)], [(0, marble), (1, dark)])
    p.ellipse(cx - 96, base - 38, cx + 96, base - 22, marble)
    p.ellipse(cx - 88, base - 35, cx + 88, base - 25, (150, 180, 200))      # the water in the basin / l'eau du bassin
    p.rect(cx - 8, base - 78, cx + 8, base - 34, marble)
    p.gpoly([(cx - 40, base - 84), (cx + 40, base - 84), (cx + 24, base - 72), (cx - 24, base - 72)], [(0, marble), (1, dark)])
    p.ellipse(cx - 40, base - 90, cx + 40, base - 80, marble)
    p.rect(cx - 4, base - 104, cx + 4, base - 88, marble)


def build_kof_spain(W, H, s, seed=81):
    """The Court of the Lions in the Alhambra: the carved hall, its arches and slender columns, the court in the sun and
    its fountain; day, then sunset at the third round, night from the fourth, the lanterns lit. / La cour des Lions de
    l'Alhambra : jour, coucher de soleil au troisième round, nuit à partir du quatrième, les lanternes allumées."""
    U, V = W / s, H / s
    cx = U / 2
    skies = {"day": sky_img(W, H, [(0, (96, 160, 222)), (0.5, (170, 205, 235)), (1, (220, 228, 230))], s,
                            clouds=[(30, 120, (255, 255, 255), 120, 5)]),
             "dusk": sky_img(W, H, [(0, (60, 52, 110)), (0.35, (200, 110, 110)), (0.6, (250, 170, 110)), (1, (255, 205, 150))], s,
                             clouds=[(40, 130, (255, 170, 140), 110, 5)]),
             "night": sky_img(W, H, [(0, (6, 10, 30)), (0.5, (18, 26, 60)), (1, (40, 46, 80))], s, stars=90, seed=seed)}
    layers = []
    # the court in the sun, beyond the arches / la cour au soleil, derrière les arcs
    p = Pic(U, V, s)
    p.grect(0, 150, U, 168, [(0, (150, 110, 90)), (1, (120, 92, 76))])            # the tiled roof / le toit de tuiles
    for x in range(0, int(U), 14):
        p.line([(x, 151), (x + 6, 167)], 1.5, (110, 84, 70))
    p.grect(0, 168, U, 300, [(0, (232, 220, 196)), (1, (214, 198, 170))])         # the far gallery / la galerie du fond
    x = 20
    while x < U:                                                                   # its arches / ses arcs
        p.poly([(x, 300)] + p.arc_poly(x + 26, 214, 26, 30, 180, 360, 12) + [(x + 52, 300)], (120, 100, 82))
        p.rect(x + 52, 200, x + 60, 300, (240, 232, 214))
        x += 60
    p.grect(0, 296, U, 345, [(0, (226, 210, 178)), (1, (206, 188, 152))])         # the gravel / le gravier
    for bx in (210, 560, 1360, 1720):                                             # the shrubs / les buissons
        for k in range(5):
            p.ellipse(bx - 34 + k * 6, 268 + (k % 2) * 6, bx + 10 + k * 6, 312, (54 + k * 8, 110 + k * 6, 46))
    _fountain(p, cx, 300, s)
    layers.append(layer(p, "far"))
    # the hall: the carved walls, the arches, the columns / la salle : les murs sculptés, les arcs, les colonnes
    p = Pic(U, V, s)
    wall = (112, 74, 44)
    _arabesque(p, 0, 0, U, 342, wall, s, step=30)
    for y in (26, 52):                                             # the friezes / les frises
        p.rect(0, y, U, y + 5, (150, 108, 62))
    gold, gold_d = (204, 158, 86), (140, 98, 50)
    clear = (0, 0, 0, 0)
    spans = []                                                     # the openings: (x0, x1, top of the arch) / les ouvertures
    for x0, x1, top in ((250, 560, 96), (1360, 1670, 96)):        # the big horseshoe arches / les grands arcs outrepassés
        r = (x1 - x0) / 2
        pts = [(x0, 342)] + p.arc_poly((x0 + x1) / 2, top + r * 0.9, r * 1.04, r * 0.95, 160, 380, 30) + [(x1, 342)]
        p.poly([(x0 - 14, 342)] + [(x + (x - (x0 + x1) / 2) * 0.06, y - 12) for x, y in pts[1:-1]] + [(x1 + 14, 342)], gold_d)
        p.poly(pts, clear)
        spans.append((x0, x1))
    # the middle: three bays with slender columns in pairs / le milieu : trois travées, colonnes par paires
    for x0, x1, top, lobes in ((610, 790, 128, 5), (790, U - 790, 64, 7), (U - 790, U - 610, 128, 5)):
        w = x1 - x0
        r = w / 2
        arc = p.arc_poly((x0 + x1) / 2, top + r * 0.75, r, r * 0.75, 180, 360, 28)
        p.poly([(x0 - 8, 342)] + [(x, y - 10) for x, y in arc] + [(x1 + 8, 342)], gold_d)
        p.poly([(x0, 342)] + arc + [(x1, 342)], clear)
        for k in range(lobes):                                     # the lobes of the arch, its cusps between them
            a = 180 + 180 * (k + 0.5) / lobes                      # les lobes de l'arc, ses pointes entre eux
            lx = (x0 + x1) / 2 + math.cos(math.radians(a)) * r
            ly = top + r * 0.75 + math.sin(math.radians(a)) * r * 0.75
            rr = w * 0.085
            p.ellipse(lx - rr - 3, ly - rr - 3, lx + rr + 3, ly + rr + 3, gold_d)
            p.ellipse(lx - rr, ly - rr, lx + rr, ly + rr, clear)
        spans.append((x0, x1))
    for x in (610, 790, U - 790, U - 610, 250, 560, 1360, 1670):   # the columns, in pairs / les colonnes, par paires
        for dx in (-13, 13):
            cxc = x + dx
            p.grect(cxc - 6, 150, cxc + 6, 330, [(0, gold), (0.5, (230, 190, 120)), (1, gold_d)])
            p.rect(cxc - 9, 140, cxc + 9, 152, gold_d)
            p.rect(cxc - 11, 328, cxc + 11, 342, gold_d)
        p.rect(x - 26, 128, x + 26, 142, (150, 104, 56))
    # the lanterns on the walls / les lanternes aux murs
    lamps = []
    for lx in (110, U - 110):
        p.line([(lx, 92), (lx, 128)], 3, (40, 30, 24))
        p.poly([(lx - 18, 128), (lx + 18, 128), (lx + 12, 176), (lx - 12, 176)], (58, 46, 36))
        p.rect(lx - 9, 136, lx + 9, 168, (230, 196, 120))
        p.poly([(lx - 22, 128), (lx, 110), (lx + 22, 128)], (48, 38, 30))
        lamps.append((lx, 152, 70, (255, 190, 110), 1.3))
    for x0, x1 in ((0, 250), (U - 250, U)):                          # the dark of the sides / les côtés plus sombres
        p.grect(x0, 0, x1, 342, [(0, (40, 22, 12, 90)), (1, (30, 16, 8, 60))])
    layers.append(layer(p, "mid"))
    # the polished floor and the reflections of the columns / le sol poli et le reflet des colonnes
    p = Pic(U, V, s)
    p.grect(0, 340, U, V, [(0, (96, 74, 58)), (1, (52, 38, 30))])
    for x in (610, 790, U - 790, U - 610, 250, 560, 1360, 1670):
        for dx in (-13, 13):
            p.grect(x + dx - 6, 342, x + dx + 6, 420, [(0, (150, 112, 64, 150)), (1, (96, 74, 58, 0))])
    for x0, x1 in spans:                                           # the light of the court on the floor / la lumière
        p.gpoly([(x0, 342), (x1, 342), (x1 + 40, 400), (x0 - 40, 400)], [(0, (250, 236, 200, 110)), (1, (250, 236, 200, 0))])
    layers.append(layer(p, "floor"))
    amb = {"horizon": int(300 * s), "skies": skies, "looks": ["day", "day", "dusk", "night"],
           "tints": {"dusk": (255, 196, 150), "night": (92, 100, 160)}, "lamps": lamps, "lamps_on": ("dusk", "night"),
           "fountain": (cx, 196), "images": {"cat": _cat_img(s)},
           "hooks": {"far": [hook_fountain], "front": [hook_lamps, hook_cat]}}
    return {"sky": skies["day"], "layers": layers, "tw": W, "amb": amb}


def hook_fountain(bd, screen, b, L, now, dt):
    """The jets of the fountain, lower at sunset and at night (the fountain stops to a gush). / Les jets de la fontaine,
    plus bas au coucher du soleil et la nuit."""
    cx, top = b["amb"]["fountain"]
    s = bd.s
    look = (bd.cur_look or "day").split("+")[0]
    hgt = 1.0 if look == "day" else 0.45
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    for i in range(14):
        ph = (now * 1.6 + i / 14) % 1.0
        a = math.radians(-90 + (i - 6.5) * 9)
        v = 70 * hgt
        x = cx + math.cos(a) * v * ph * 1.6
        y = top - (math.sin(-a) * v * ph * 1.4 - 60 * ph * ph * 1.6) + 10
        g = sp.glow(4 * s, (220, 236, 255), 5 * (1 - ph) + 2, hot=0.6)
        screen.blit(g, (int(x * s - g.get_width() / 2), int(y * s - g.get_height() / 2)), special_flags=add)


def _cat_img(s):
    def fn(d, W, H):
        k = W / 48
        col = (246, 244, 238, 255)
        d.ellipse([10 * k, 8 * k, 38 * k, 22 * k], fill=col)                     # body / le corps
        d.ellipse([34 * k, 2 * k, 46 * k, 14 * k], fill=col)                      # head / la tête
        d.polygon([(36 * k, 4 * k), (37 * k, -1 * k), (40 * k, 3 * k)], fill=col)
        d.polygon([(41 * k, 3 * k), (44 * k, -1 * k), (45 * k, 5 * k)], fill=col)
        for lx in (13, 18, 30, 35):
            d.rectangle([lx * k, 18 * k, (lx + 3) * k, 26 * k], fill=col)
        d.line([(11 * k, 12 * k), (3 * k, 6 * k), (1 * k, 1 * k)], fill=col, width=max(1, int(2.5 * k)), joint="curve")
    from .hd_stages import _img
    return _img(48 * s, 27 * s, fn)


def hook_cat(bd, screen, b, L, now, dt):
    """The white cat that crosses the hall now and then. / Le chat blanc qui traverse la salle de temps en temps."""
    st = bd.amb_state.setdefault("_cat", {"t": now + 6.0, "x": None})
    s = bd.s
    img = b["imgs"].get("cat")
    if img is None:
        return
    if st["x"] is None:
        if now < st["t"]:
            return
        st["x"] = -img.get_width()
    st["x"] += 70 * s * dt
    if st["x"] > bd.W:
        st["x"], st["t"] = None, now + bd.rng.uniform(18, 30)
        return
    step = int(now * 6) % 2
    screen.blit(img, (int(st["x"]), int(bd.H - (128 + step) * s)))


# ============================================================================ the Middle East, the market / Moyen-Orient
def _window(p, x, y, w, h, frame=(244, 238, 226), pane=(46, 40, 44), arch=True):
    """A window of the tower houses: white frame, dark pane, a round light above. / Une fenêtre des maisons-tours."""
    p.rect(x - w / 2 - 3, y - 3, x + w / 2 + 3, y + h + 3, frame)
    p.rect(x - w / 2, y, x + w / 2, y + h, pane)
    p.line([(x, y), (x, y + h)], 1.5, frame)
    if arch:
        p.ellipse(x - w / 2 - 3, y - w * 0.9 - 3, x + w / 2 + 3, y + 3, frame)
        p.ellipse(x - w / 2 + 2, y - w * 0.9 + 2, x + w / 2 - 2, y - 1, (90, 150, 190))


def _tower(p, x0, x1, top, base, col, rng, rows=5):
    """A tower house of the old towns of Arabia: sandstone, white friezes, windows. / Une maison-tour : grès, frises blanches."""
    p.gpoly([(x0, top), (x1, top), (x1, base), (x0, base)], [(0, shade(col, 1.08)), (1, shade(col, 0.86))])
    p.rect(x0 - 4, top - 6, x1 + 4, top, shade(col, 0.8))
    h = (base - top) / rows
    for r in range(rows):
        y = top + 14 + r * h
        p.rect(x0, y + h - 10, x1, y + h - 6, (236, 228, 212))                # the white frieze / la frise blanche
        for k in range(0, int(x1 - x0) - 10, 12):
            p.poly([(x0 + k, y + h - 10), (x0 + k + 6, y + h - 16), (x0 + k + 12, y + h - 10)], (236, 228, 212))
        n = max(1, int((x1 - x0) / 46))
        for k in range(n):
            if rng.random() < 0.82:
                _window(p, x0 + (k + 0.5) * (x1 - x0) / n, y + 14, 14, max(14, h * 0.32), arch=rng.random() < 0.6)


def build_kof_mideast(W, H, s, seed=82):
    """The market of an old Arab town: tower houses in sandstone with white friezes, the stalls under their canopies,
    copper pots, carpets, fruit, the people in their robes, the paving stones; in the sun. / Le marché d'une vieille ville
    arabe, au soleil."""
    U, V = W / s, H / s
    rng = random.Random(seed)
    sky = sky_img(W, H, [(0, (58, 118, 204)), (0.45, (130, 182, 230)), (0.75, (204, 220, 232)), (1, (224, 228, 228))], s,
                  clouds=[(20, 90, (255, 255, 255), 90, 4)])
    layers = []
    p = Pic(U, V, s)                                                # the town / la ville
    for x0, x1, top in ((330, 420, 150), (410, 520, 120), (520, 600, 160)):     # far away, in the haze / au loin
        p.rect(x0, top, x1, 300, (196, 196, 196))
        for k in range(int((x1 - x0) / 22)):
            p.rect(x0 + 8 + k * 22, top + 20, x0 + 16 + k * 22, top + 32, (170, 172, 176))
    _tower(p, 590, 760, 60, 330, (204, 170, 120), rng, 5)
    _tower(p, 760, 1000, 10, 330, (212, 176, 124), rng, 6)
    _tower(p, 1000, 1190, 70, 330, (196, 160, 112), rng, 5)
    _tower(p, 1190, 1460, 0, 330, (190, 152, 104), rng, 6)
    _tower(p, 1460, 1920, -20, 330, (176, 140, 96), rng, 7)
    p.gpoly([(0, -10), (340, -10), (340, 330), (0, 330)], [(0, (206, 198, 182)), (1, (176, 166, 148))])   # the near wall
    with p.plain():
        for _ in range(140):                                        # its worn plaster / son enduit usé
            x, y = rng.uniform(0, 330), rng.uniform(0, 320)
            r = rng.uniform(4, 16)
            p.ellipse(x - r, y - r * 0.6, x + r, y + r * 0.6, shade((196, 186, 168), rng.uniform(0.86, 1.08)))
    for x, y in ((90, 40), (220, 40), (90, 150)):
        _window(p, x, y, 18, 34, frame=(214, 206, 190), arch=False)
    layers.append(layer(p, "far"))
    p = Pic(U, V, s)                                                # the stalls / les étals
    sparkles = []
    tan, tan_d = (214, 176, 116), (150, 116, 70)
    p.gpoly([(0, 104), (660, 146), (650, 182), (0, 160)], [(0, tan), (1, tan_d)])            # the left canopy / l'auvent
    for k in range(0, 660, 30):
        p.poly([(k, 160 + k * 0.033), (k + 15, 172 + k * 0.033), (k + 30, 160 + k * 0.033)], tan_d)
    p.line([(0, 160), (650, 182)], 3, (120, 90, 54))
    p.gpoly([(560, 112), (650, 104), (780, 146), (740, 168), (650, 136), (560, 150)], [(0, (60, 96, 196)), (1, (30, 54, 140))])  # the blue cloth
    for k in range(13):                                             # the copper pots hanging / les cuivres suspendus
        x = 40 + k * 46
        y = 178 + k * 1.6 + (k % 2) * 16
        r = 15 + (k % 3) * 4
        p.line([(x, y - r - 14), (x, y - r)], 1.5, (90, 60, 30))
        p.ellipse(x - r, y - r, x + r, y + r * 0.9, (176, 92, 40))
        p.ellipse(x - r * 0.75, y - r * 0.8, x + r * 0.2, y + r * 0.1, (226, 140, 72))
        p.ellipse(x - r * 0.5, y - r * 0.6, x - r * 0.15, y - r * 0.25, (255, 214, 150))
        sparkles.append((x - r * 0.3, y - r * 0.4, (255, 220, 160)))
    for row, y in enumerate((236, 278)):                            # the shelves of pots and jugs / les étagères
        p.rect(20, y + 26, 560, y + 32, (110, 74, 40))
        for k in range(14):
            x = 40 + k * 37 + row * 12
            h = 20 + (k * 7 % 3) * 6
            col = ((180, 96, 44), (196, 160, 90), (150, 70, 40))[k % 3]
            p.ellipse(x - 11, y + 26 - h, x + 11, y + 26, col)
            p.rect(x - 4, y + 26 - h - 8, x + 4, y + 26 - h + 2, shade(col, 0.8))
            if k % 3 == 0:
                sparkles.append((x - 4, y + 14 - h / 2, (255, 210, 150)))
    p.gpoly([(150, 296), (430, 296), (440, 336), (140, 336)], [(0, (200, 44, 40)), (1, (140, 24, 24))])   # the red cloth
    for bx in (30, 100):                                            # the fruit baskets / les paniers de fruits
        p.gpoly([(bx - 34, 286), (bx + 34, 286), (bx + 26, 336), (bx - 26, 336)], [(0, (206, 166, 92)), (1, (150, 112, 56))])
        for k in range(16):
            fx = bx - 28 + (k % 8) * 8
            fy = 282 - (k // 8) * 7
            p.ellipse(fx - 5, fy - 5, fx + 5, fy + 5, ((204, 52, 40), (120, 176, 60), (236, 196, 60))[(k + bx) % 3])
    for k, (x, col, h) in enumerate(((640, (236, 232, 222), 124), (690, (198, 176, 144), 116), (742, (140, 96, 62), 108),
                                     (842, (236, 232, 222), 128), (880, (170, 70, 56), 112), (930, (226, 220, 206), 120),
                                     (1004, (190, 160, 120), 110), (1070, (236, 232, 222), 124))):
        base = 334
        p.poly([(x - 16, base - h + 24), (x + 16, base - h + 24), (x + 22, base), (x - 22, base)], col)   # the robe / la robe
        p.ellipse(x - 9, base - h, x + 9, base - h + 22, (176, 128, 92))                                # the face / le visage
        p.poly([(x - 12, base - h + 10), (x - 10, base - h - 4), (x + 10, base - h - 4), (x + 12, base - h + 10),
                (x + 6, base - h + 2), (x - 6, base - h + 2)], (240, 236, 226) if k % 2 == 0 else (60, 50, 44))
    cream, cream_d = (240, 230, 196), (196, 178, 136)
    p.line([(1160, 186), (1160, 334)], 6, (96, 70, 44))             # the parasols / les parasols
    p.gpoly([(984, 196), (1160, 150), (1336, 196), (1320, 212), (1000, 212)], [(0, cream), (1, cream_d)])
    p.line([(1700, 70), (1700, 334)], 8, (96, 70, 44))
    p.gpoly([(1430, 120), (1700, 40), (1920, 64), (1920, 128), (1450, 138)], [(0, cream), (1, cream_d)])
    for k in range(0, 500, 26):
        p.poly([(1440 + k, 136 - k * 0.02), (1453 + k, 146 - k * 0.02), (1466 + k, 136 - k * 0.02)], cream_d)
    p.line([(1490, 150), (1900, 150)], 3, (90, 66, 40))             # the carpets hanging / les tapis suspendus
    for k, (x0, col, edge) in enumerate(((1500, (170, 34, 34), (230, 190, 90)), (1574, (40, 96, 130), (220, 210, 170)),
                                         (1648, (186, 70, 36), (240, 220, 160)), (1722, (110, 30, 60), (220, 180, 90)))):
        p.rect(x0, 150, x0 + 64, 290 - k * 6, edge)
        p.rect(x0 + 5, 155, x0 + 59, 285 - k * 6, col)
        for j in range(4):
            cy = 175 + j * 28
            p.poly([(x0 + 32, cy - 10), (x0 + 44, cy), (x0 + 32, cy + 10), (x0 + 20, cy)], edge)
    for j in range(9):                                              # the carpets stacked / les tapis empilés
        y = 330 - j * 10
        col = ((180, 40, 40), (60, 130, 90), (40, 80, 160), (220, 180, 60), (130, 60, 120))[j % 5]
        p.rect(1790 - j * 2, y - 10, 1920, y, col)
        p.line([(1790 - j * 2, y - 5), (1920, y - 5)], 1.5, shade(col, 1.3))
    layers.append(layer(p, "mid"))
    p = Pic(U, V, s)                                                # the paving stones / les pavés
    p.grect(0, 328, U, V, [(0, (214, 190, 146)), (1, (170, 146, 104))])
    y, hh = 332, 8
    with p.plain():
        while y < V:
            x = -rng.uniform(0, 30)
            while x < U:
                w = rng.uniform(26, 44) * (1 + (y - 330) / 140)
                p.ellipse(x + 2, y + 1, x + w - 2, y + hh - 1, shade((212, 188, 144), rng.uniform(0.86, 1.06)))
                x += w
            y += hh
            hh *= 1.18
    layers.append(layer(p, "floor"))
    amb = {"horizon": int(330 * s), "sparkles": sparkles, "hooks": {"front": [hook_sparkles]}}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}

# ============================================================================ Korea, the harbor / Corée, le port
def _pavilion(p, x, base, w, h, roof=(64, 78, 76), post=(150, 56, 40)):
    """A pavilion with its curved roofs on two tiers. / Un pavillon aux toits recourbés sur deux niveaux."""
    for dx in (-w * 0.32, -w * 0.11, w * 0.11, w * 0.32):
        p.rect(x + dx - 3, base - h * 0.46, x + dx + 3, base, post)
    for k, (ww, y) in enumerate(((w, base - h * 0.46), (w * 0.62, base - h * 0.82))):
        p.poly([(x - ww * 0.62, y + 4), (x - ww * 0.5, y - h * 0.08), (x - ww * 0.26, y - h * 0.2), (x + ww * 0.26, y - h * 0.2),
                (x + ww * 0.5, y - h * 0.08), (x + ww * 0.62, y + 4), (x + ww * 0.42, y), (x - ww * 0.42, y)], roof)
        if k == 0:
            p.rect(x - w * 0.24, y - h * 0.36, x + w * 0.24, y - h * 0.2, post)
    p.rect(x - 2, base - h - 10, x + 2, base - h * 0.98, roof)


def _house(p, x0, x1, top, base, wall, floors, awning=None, rng=None, sign=None):
    """A harbor house: its floors, its white windows, an awning over the shop. / Une maison du port."""
    p.gpoly([(x0, top), (x1, top), (x1, base), (x0, base)], [(0, shade(wall, 1.06)), (1, shade(wall, 0.88))])
    p.rect(x0 - 6, top - 8, x1 + 6, top, shade(wall, 0.7))
    fh = (base - 46 - top) / floors
    for f in range(floors):
        y = top + 12 + f * fh
        n = max(1, int((x1 - x0) / 56))
        for k in range(n):
            x = x0 + (k + 0.5) * (x1 - x0) / n
            p.rect(x - 16, y, x + 16, y + fh * 0.58, (246, 244, 236))
            p.rect(x - 12, y + 4, x + 12, y + fh * 0.58 - 4, (70, 96, 110))
            p.line([(x, y + 4), (x, y + fh * 0.58 - 4)], 2, (246, 244, 236))
            p.line([(x - 12, y + fh * 0.3), (x + 12, y + fh * 0.3)], 2, (246, 244, 236))
    p.rect(x0, base - 46, x1, base, (58, 46, 40))                   # the shop below / la boutique en bas
    if awning:
        a, b = awning
        k = 0
        x = x0 - 6
        while x < x1 + 6:
            p.poly([(x, base - 62), (x + 22, base - 62), (x + 22, base - 40), (x, base - 40)], a if k % 2 == 0 else b)
            k += 1
            x += 22
    if sign:                                                         # a signboard with marks (no words) / une enseigne
        sx0, sy0, sx1, sy1, sc = sign
        p.rect(sx0, sy0, sx1, sy1, sc)
        for k in range(int((sx1 - sx0) / 30)):
            cx = sx0 + 18 + k * 30
            if k % 2:                                              # marks like letters, no words / des signes
                p.ellipse(cx - 9, sy0 + 7, cx + 3, sy0 + 19, (246, 236, 210))
                p.ellipse(cx - 6, sy0 + 10, cx, sy0 + 16, (110, 70, 40))
                p.line([(cx + 7, sy0 + 6), (cx + 7, sy1 - 8)], 3, (246, 236, 210))
            else:
                p.rect(cx - 9, sy0 + 7, cx + 9, sy1 - 10, (246, 236, 210))
                p.rect(cx - 6, sy0 + 10, cx + 6, sy1 - 13, (110, 70, 40))


def build_kof_korea(W, H, s, seed=83):
    """A pier of a harbor town in Korea, in the sun: the houses and their shops on the left, the stone quay, the boats on
    the water, the red bridge to the rocky hill and its pavilion, the wooden pole and its wires, the gulls. / Un quai d'un
    port en Corée, au soleil."""
    U, V = W / s, H / s
    rng = random.Random(seed)
    sky = sky_img(W, H, [(0, (52, 108, 196)), (0.4, (120, 172, 226)), (0.7, (196, 216, 232)), (1, (226, 230, 230))], s,
                  clouds=[(30, 140, (255, 255, 255), 150, 7), (150, 230, (236, 240, 246), 110, 4)])
    layers = []
    p = Pic(U, V, s)                                                # the hills and the pavilion / les collines, le pavillon
    p.gpoly([(1000, 300)] + [(1000 + k * 46, 220 - 40 * math.sin(k * 0.7) - 30 * math.sin(k * 1.9)) for k in range(21)] + [(1920, 300)],
            [(0, (128, 150, 170)), (1, (170, 186, 196))])
    rock = [(1180, 310), (1230, 230), (1290, 190), (1360, 150), (1420, 120), (1500, 108), (1580, 126), (1650, 150),
            (1720, 196), (1800, 236), (1880, 280), (1920, 300), (1920, 320), (1180, 320)]
    p.gpoly(rock, [(0, (196, 186, 164)), (1, (150, 140, 120))])
    with p.plain():
        for _ in range(26):                                          # the rocks and their shadows / les rochers
            x, y = rng.uniform(1220, 1880), rng.uniform(150, 300)
            p.poly([(x, y), (x + rng.uniform(20, 40), y - rng.uniform(10, 30)), (x + rng.uniform(40, 70), y + 4)],
                   shade((160, 150, 128), rng.uniform(0.8, 1.1)))
    for _ in range(30):                                              # the trees / les arbres
        x, y = rng.uniform(1200, 1900), rng.uniform(130, 290)
        if y < 330 - (x - 1180) * 0.0 and abs(x - 1500) > 60 or y > 180:
            r = rng.uniform(14, 28)
            p.ellipse(x - r, y - r * 0.8, x + r, y + r * 0.6, (rng.randint(50, 80), rng.randint(104, 136), rng.randint(50, 70)))
    _pavilion(p, 1500, 112, 150, 92)
    layers.append(layer(p, "far"))
    p = Pic(U, V, s)                                                # the water / l'eau
    p.grect(0, 284, U, 350, [(0, (40, 96, 168)), (1, (24, 62, 128))])
    for _ in range(90):
        x, y = rng.uniform(0, U), rng.uniform(290, 346)
        p.line([(x, y), (x + rng.uniform(16, 40), y)], 2, (110, 160, 214))
    layers.append(layer(p, "water"))
    boats = Pic(U, V, s)                                            # the boats, in front of the quay / devant le quai
    for x0, hull, roof in ((360, (74, 150, 96), (130, 92, 60)), (640, (232, 230, 222), (180, 180, 176))):
        boats.gpoly([(x0, 306), (x0 + 200, 306), (x0 + 184, 334), (x0 + 16, 334)], [(0, hull), (1, shade(hull, 0.7))])
        boats.rect(x0 + 30, 262, x0 + 36, 306, (110, 80, 50))
        boats.rect(x0 + 164, 262, x0 + 170, 306, (110, 80, 50))
        boats.poly([(x0 + 10, 266), (x0 + 100, 252), (x0 + 190, 266), (x0 + 186, 272), (x0 + 14, 272)], roof)
        if x0 == 640:
            boats.rect(x0 + 90, 286, x0 + 176, 306, (236, 190, 60))  # the yellow tarp / la bâche jaune
    boats.rect(1290, 186, 1294, 300, (60, 40, 30))                  # a mast / un mât
    boats.poly([(1294, 192), (1330, 230), (1294, 236)], (70, 110, 190))
    p = Pic(U, V, s)                                                # the town, the bridge, the pole / la ville, le pont
    _house(p, 0, 270, 70, 300, (150, 184, 170), 3, awning=((60, 140, 90), (236, 236, 214)))
    _house(p, 270, 540, 30, 300, (228, 208, 166), 4, rng=rng, sign=(300, 160, 510, 200, (110, 70, 40)))
    _house(p, 540, 720, 110, 300, (218, 152, 122), 2)
    _house(p, 720, 820, 150, 300, (176, 196, 214), 2)
    p.gpoly([(0, 270), (1180, 270), (1180, 292), (0, 292)], [(0, (164, 158, 146)), (1, (120, 116, 108))])   # the quay / le quai
    with p.plain():
        for y in (275, 283):
            for x in range(int(y % 3) * 10, 1180, 34):
                p.rect(x, y, x + 30, y + 6, (150, 146, 136))
    pts = [(1060 + k * 34, 270 - 54 * math.sin(math.pi * k / 20)) for k in range(21)]   # the red bridge / le pont rouge
    p.line(pts, 10, (196, 86, 48))
    p.line([(x, y - 20) for x, y in pts], 4, (210, 100, 56))
    for x, y in pts[::2]:
        p.line([(x, y), (x, y - 20)], 4, (180, 76, 42))
    for x, y in pts[2::6]:
        p.line([(x, y), (x, 300)], 6, (150, 64, 40))
    _house(p, 1770, 1920, 40, 300, (222, 132, 92), 3)               # the house on the right / la maison de droite
    p.gpoly([(1760, 200), (1920, 200), (1920, 330), (1760, 330)], [(0, (150, 144, 134)), (1, (110, 106, 98))])
    with p.plain():
        for y in range(206, 330, 18):
            for x in range(1764 + (y // 18 % 2) * 14, 1920, 28):
                p.rect(x, y, x + 24, y + 14, (166, 160, 148))
    p.rect(1820, 30, 1866, 190, (40, 80, 176))                      # the blue sign / l'enseigne bleue
    for k in range(4):
        y = 44 + k * 36
        p.ellipse(1830, y, 1846, y + 16, (246, 246, 246))
        p.ellipse(1834, y + 4, 1842, y + 12, (40, 80, 176))
        p.line([(1854, y - 2), (1854, y + 22)], 4, (246, 246, 246))
        p.line([(1830, y + 22), (1848, y + 22)], 3, (246, 246, 246))
    p.line([(1150, -10), (1146, 336)], 12, (104, 76, 52))           # the wooden pole and its wires / le poteau
    p.rect(1110, 36, 1186, 44, (90, 66, 46))
    for x in (1118, 1178):
        p.rect(x - 3, 26, x + 3, 36, (220, 220, 214))
    for dy, sag in ((0, 38), (8, 30)):
        p.line([(1118, 30 + dy)] + [(1118 - k * 56, 30 + dy + sag * math.sin(math.pi * k / 20)) for k in range(1, 21)], 2, (34, 30, 30))
        p.line([(1178, 30 + dy)] + [(1178 + k * 38, 30 + dy + sag * 0.7 * math.sin(math.pi * k / 20)) for k in range(1, 21)], 2, (34, 30, 30))
    layers.append(layer(p, "mid"))
    layers.append(layer(boats, "boats"))
    p = Pic(U, V, s)
    p.grect(0, 340, U, V, [(0, (214, 204, 182)), (1, (176, 164, 140))])    # the concrete of the pier / le béton du quai
    for _ in range(18):
        x, y = rng.uniform(0, U), rng.uniform(346, 440)
        p.line([(x, y), (x + rng.uniform(-30, 30), y + rng.uniform(10, 30)), (x + rng.uniform(-50, 50), y + rng.uniform(20, 50))],
               1.5, (150, 140, 120))
    layers.append(layer(p, "floor"))
    sparkles = [(rng.uniform(0, 1150), rng.uniform(296, 344), (255, 255, 240)) for _ in range(40)]
    amb = {"horizon": int(290 * s), "sparkles": sparkles,
           "images": {"gull_up": gull_img(s, True), "gull_down": gull_img(s, False)},
           "hooks": {"far": [hook_gulls], "front": [hook_sparkles]}}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}

# ============================================================================ China, the boat on the river / la Chine
def _peak(p, x, base, w, h, col, top_col=None, rng=None):
    """A karst pillar of Wulingyuan: steep sides, a rounded top. / Un pilier karstique : flancs raides, sommet arrondi."""
    pts = [(x - w / 2, base)]
    for k in range(9):
        t = k / 8
        pts.append((x - w / 2 + w * 0.08 * math.sin(t * 7) + w * 0.06 * t, base - h * t))
    pts += p.arc_poly(x, base - h, w * 0.44, w * 0.32, 180, 360, 12)
    for k in range(8, -1, -1):
        t = k / 8
        pts.append((x + w / 2 - w * 0.07 * math.sin(t * 5 + 1) - w * 0.05 * t, base - h * t))
    pts.append((x + w / 2, base))
    p.gpoly(pts, [(0, top_col or col), (0.4, col), (1, shade(col, 1.08))], base - h - w * 0.3, base)


def build_kof_china(W, H, s, seed=84):
    """The boat on the river among the stone pillars of Wulingyuan: the deck where they fight, the boatmen, the cliffs
    and their trees going by. A temple at the first round, the rocks and a waterfall at the second, a mountain in the
    fog at the third and the last. / Le bateau sur la rivière entre les piliers de pierre de Wulingyuan : un temple au
    premier round, une cascade au deuxième, une montagne dans la brume au troisième et au dernier."""
    U, V = W / s, H / s
    rng = random.Random(seed)
    sky = sky_img(W, H, [(0, (150, 196, 212)), (0.45, (196, 222, 226)), (0.7, (222, 234, 228)), (1, (226, 236, 230))], s)
    layers = []
    p = Pic(U, V, s, wrap=True)                                     # the far pillars / les piliers au loin
    for k in range(16):
        x = k * U / 16 + rng.uniform(-30, 30)
        _peak(p, x, 290, rng.uniform(50, 110), rng.uniform(120, 230), (172, 202, 208), (150, 186, 196), rng)
    p.grect(0, 230, U, 300, [(0, (214, 230, 228, 0)), (1, (214, 230, 228, 255))])
    layers.append(layer(p, "far", f=0.12))
    p = Pic(U, V, s, wrap=True)                                     # the mountain in the fog / la montagne dans la brume
    p.gpoly([(U * 0.2, 300), (U * 0.38, 110), (U * 0.46, 60), (U * 0.55, 90), (U * 0.68, 170), (U * 0.85, 300)],
            [(0, (150, 176, 186)), (1, (200, 218, 220))])
    for y in (150, 205, 250):
        for k in range(6):
            x = rng.uniform(0, U)
            p.ellipse(x - 260, y - 20, x + 260, y + 22, (236, 242, 240, 150))
    p.blur(10)
    layers.append(layer(p, "far2", f=0.12, only="fog"))
    p = Pic(U, V, s, wrap=True)                                     # nearer pillars, green tops / des piliers plus près
    for k in range(9):
        x = k * U / 9 + rng.uniform(-40, 40)
        w, h = rng.uniform(80, 140), rng.uniform(150, 250)
        _peak(p, x, 300, w, h, (110, 140, 132), (70, 110, 80), rng)
        for j in range(4):
            tx, ty = x + rng.uniform(-w * 0.4, w * 0.4), 300 - h + rng.uniform(-10, 60)
            _bush(p, tx, ty, rng.uniform(12, 22), rng, (70 + j * 6, 116 + j * 5, 80))
    p.grect(0, 262, U, 304, [(0, (200, 222, 220, 0)), (1, (200, 222, 220, 230))])
    layers.append(layer(p, "far3", f=0.3))
    p = Pic(U, V, s)                                                # the river / la rivière
    p.grect(0, 272, U, 336, [(0, (132, 178, 166)), (1, (78, 126, 114))])
    for _ in range(80):
        x, y = rng.uniform(0, U), rng.uniform(278, 334)
        p.line([(x, y), (x + rng.uniform(20, 60), y)], 1.5, (170, 210, 198))
    layers.append(layer(p, "water"))
    p = Pic(U, V, s, wrap=True)                                     # the cliffs and their trees / les falaises et leurs arbres
    rock, rock_d = (132, 124, 108), (88, 82, 72)
    for x0, x1, top in ((-60, 420, -40), (700, 1240, -60), (1480, 1920, -30)):
        pts = [(x0, 300)]
        for k in range(11):
            t = k / 10
            pts.append((x0 + (x1 - x0) * t, top + 40 * math.sin(t * 6 + x0) + 30 * rng.random()))
        pts.append((x1, 300))
        p.gpoly(pts, [(0, (150, 142, 124)), (0.6, rock), (1, rock_d)], top, 300)
        for _ in range(int((x1 - x0) / 18)):                         # the cracks / les fissures
            x = rng.uniform(x0 + 10, x1 - 10)
            y = rng.uniform(top + 30, 290)
            p.line([(x, y), (x + rng.uniform(-6, 6), y + rng.uniform(20, 50))], 2, rock_d)
    for x0, x1, top in ((-60, 420, -40), (700, 1240, -60), (1480, 1920, -30)):   # the foliage, over all the rocks
        for _ in range(int((x1 - x0) / 14)):                         # le feuillage, sur tous les rochers
            x = rng.uniform(x0 - 20, x1 + 20)
            y = rng.uniform(top - 20, 250) if rng.random() < 0.6 else rng.uniform(top - 20, 90)
            _bush(p, x, y, rng.uniform(22, 44), rng, rng.choice(((44, 108, 48), (58, 126, 56), (36, 92, 42), (76, 140, 62))))
    layers.append(layer(p, "mid", f=0.75))
    p = Pic(U, V, s, wrap=True)                                     # the temple on its rock / le temple sur son rocher
    p.gpoly([(470, 300), (500, 236), (560, 222), (640, 230), (680, 300)], [(0, (150, 142, 124)), (1, (100, 94, 82))])
    for dx in (-36, -12, 12, 36):
        p.rect(575 + dx - 3, 176, 575 + dx + 3, 228, (170, 50, 36))
    p.poly([(505, 182), (530, 160), (575, 146), (620, 160), (645, 182), (630, 176), (520, 176)], (40, 44, 48))
    p.poly([(530, 150), (548, 132), (575, 122), (602, 132), (620, 150), (606, 146), (544, 146)], (40, 44, 48))
    p.rect(573, 106, 577, 124, (40, 44, 48))
    layers.append(layer(p, "temple", f=0.75, only="temple"))
    p = Pic(U, V, s, wrap=True)                                     # the waterfall / la cascade
    for k in range(9):
        x = 1290 + k * 7
        p.line([(x, 20), (x + 2, 150), (x + 4, 290)], 4, (236, 244, 246, 200 if k % 2 else 150))
    p.ellipse(1250, 262, 1380, 300, (240, 246, 246, 190))
    layers.append(layer(p, "falls", f=0.75, only="falls", falls=(1318, 20, 290)))
    p = Pic(U, V, s)                                                # the deck of the boat / le pont du bateau
    wood, wood_d = (168, 118, 64), (108, 72, 38)
    p.gpoly([(0, 322), (U, 322), (U, V), (0, V)], [(0, wood), (1, wood_d)])
    for x in range(0, int(U), 64):
        p.line([(x, 322), (x - 30, V)], 2, (96, 62, 32))
    p.rect(0, 296, U, 306, (196, 156, 84))                          # the railing / la rambarde
    p.rect(0, 318, U, 324, (150, 110, 56))
    for x in range(30, int(U), 120):
        p.rect(x - 4, 296, x + 4, 324, (176, 136, 70))
    p.line([(70, 120), (150, 330)], 5, (120, 84, 44))                # the boatman and his pole / le batelier et sa perche
    p.poly([(52, 196), (88, 196), (94, 268), (46, 268)], (60, 100, 170))
    p.rect(52, 268, 64, 312, (40, 50, 70))
    p.rect(76, 268, 88, 312, (40, 50, 70))
    p.ellipse(60, 172, 82, 196, (200, 150, 110))
    p.poly([(44, 178), (71, 160), (98, 178)], (220, 196, 130))
    p.poly([(1820, 290), (1876, 290), (1884, 318), (1812, 318)], (60, 100, 170))   # the man sitting at the bow / à la proue
    p.ellipse(1836, 262, 1858, 284, (200, 150, 110))
    p.poly([(1812, 272), (1847, 246), (1882, 272)], (220, 196, 130))
    layers.append(layer(p, "near"))
    sparkles = [(rng.uniform(0, U), rng.uniform(276, 332), (255, 255, 240)) for _ in range(30)]
    amb = {"horizon": int(300 * s), "drift": 24, "sparkles": sparkles,
           "looks": ["day+temple", "day+falls", "day+fog", "day", "day+fog"],
           "hooks": {"falls": [hook_falls], "front": [hook_sparkles]}}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


def hook_falls(bd, screen, b, L, now, dt):
    """The water falling down the waterfall. / L'eau qui tombe de la cascade."""
    if not bd._shown(L, bd.cur_look) and not (bd.look_prev and bd._shown(L, bd.look_prev)):
        return
    fx, top, bot = L["falls"]
    s = bd.s
    x0 = bd._layer_x(L, b["tw"]) + fx * s
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    for dx in (0, b["tw"]):
        x = x0 + dx
        if not -60 < x < bd.W + 60:
            continue
        for i in range(10):
            ph = (now * 0.9 + i / 10) % 1.0
            y = (top + (bot - top) * ph) * s
            g = sp.streak(int(26 * s), max(2, int(3 * s)), (230, 240, 255), 90, 6)
            screen.blit(g, (int(x + (i % 4) * 7 * s - 10 * s), int(y)), special_flags=add)

# ============================================================================ Japan, the street in Osaka / Japon, Osaka
def _car(p, x, base, w, body, kind="car", lamps=None, flag=None):
    """A car seen from the front, its headlights lit. / Une voiture vue de face, ses phares allumés."""
    h = {"car": 0.5, "van": 0.78, "truck": 1.0, "round": 0.6}[kind] * w
    dark = shade(body, 0.62)
    if kind == "round":
        p.ellipse(x - w / 2, base - h, x + w / 2, base + h * 0.25, body)
        p.ellipse(x - w * 0.3, base - h * 0.95, x + w * 0.3, base - h * 0.45, (40, 48, 60))
    else:
        roof = base - h
        p.gpoly([(x - w / 2, base - h * 0.45), (x + w / 2, base - h * 0.45), (x + w / 2, base), (x - w / 2, base)],
                [(0, body), (1, dark)])
        top = 0.36 if kind == "car" else 0.12
        p.poly([(x - w * 0.42, base - h * 0.45), (x - w * (0.42 - top * 0.3), roof), (x + w * (0.42 - top * 0.3), roof),
                (x + w * 0.42, base - h * 0.45)], body)
        p.poly([(x - w * 0.36, base - h * 0.5), (x - w * 0.3, roof + h * 0.08), (x + w * 0.3, roof + h * 0.08),
                (x + w * 0.36, base - h * 0.5)], (40, 48, 62))
        if kind == "truck":
            p.rect(x - w / 2, roof - h * 0.1, x + w / 2, roof + h * 0.04, shade(body, 1.1))
    p.rect(x - w * 0.46, base - h * 0.08, x + w * 0.46, base + 2, (30, 30, 34))                       # the bumper
    p.rect(x - w * 0.18, base - h * 0.3, x + w * 0.18, base - h * 0.14, (50, 50, 56))                 # the grille
    for d in (-1, 1):
        hx = x + d * w * 0.34
        p.ellipse(hx - w * 0.07, base - h * 0.3, hx + w * 0.07, base - h * 0.16, (255, 246, 210))
        if lamps is not None:
            lamps.append((hx, base - h * 0.23, w * 0.42, (255, 236, 190), 0.8, flag))
    for d in (-1, 1):                                               # the tyres / les pneus
        p.rect(x + d * w * 0.38 - w * 0.07, base, x + d * w * 0.38 + w * 0.07, base + h * 0.12, (20, 20, 22))


def build_kof_osaka(W, H, s, seed=85):
    """Under the viaduct by the station, in Osaka at night: the steel girders lit from below, the concrete pillars, the
    street lit far away, the cars in the jam with their headlights, the crossing and the people watching. Cars at the
    first round, some passing at the second, the jam from the third. / Sous le viaduc près de la gare, à Osaka la nuit :
    des voitures au premier round, quelques-unes qui passent au deuxième, l'embouteillage à partir du troisième."""
    U, V = W / s, H / s
    rng = random.Random(seed)
    sky = sky_img(W, H, [(0, (8, 10, 26)), (0.3, (16, 22, 48)), (0.5, (40, 38, 66)), (0.62, (130, 76, 64)), (0.7, (70, 46, 50)),
                         (1, (24, 18, 24))], s)
    layers = []
    lamps = []
    p = Pic(U, V, s)                                                # the street lit far away / la rue éclairée au loin
    cx = U / 2
    for side in (-1, 1):
        x = cx + side * 60
        while 0 <= x <= U:
            d = abs(x - cx) / (U / 2)                                # 0 at the end of the street, 1 at the edge
            w = 40 + 160 * d
            top = 230 - 170 * d - rng.uniform(0, 40)
            x0, x1 = (x, x + w) if side > 0 else (x - w, x)
            col = (rng.randint(26, 40), rng.randint(26, 36), rng.randint(40, 56))
            p.gpoly([(x0, top), (x1, top), (x1, 310), (x0, 310)], [(0, col), (1, shade(col, 0.7))])
            for wy in range(int(top) + 8, 270, 14):
                for wx in range(int(x0) + 6, int(x1) - 8, 12):
                    if rng.random() < 0.38:
                        p.rect(wx, wy, wx + 6, wy + 7, rng.choice(((255, 214, 140), (255, 236, 190), (170, 210, 255), (255, 170, 110))))
            if rng.random() < 0.8:                                   # a shop sign, small and still / une petite enseigne
                sw = min(w * 0.7, 26 + 50 * d)
                sx = (x0 + x1) / 2
                sy = 276 - 10 * d
                col = rng.choice(((230, 60, 60), (250, 200, 60), (60, 200, 220), (240, 120, 200), (120, 230, 120)))
                p.rect(sx - sw / 2, sy, sx + sw / 2, sy + 10 + 6 * d, col)
                p.rect(sx - sw / 2 + 3, sy + 3, sx + sw / 2 - 3, sy + 7 + 6 * d, shade(col, 1.4))
            x += side * w
    p.grect(0, 300, U, 340, [(0, (60, 50, 56)), (1, (40, 36, 42))])
    layers.append(layer(p, "far"))
    p = Pic(U, V, s)                                                # the viaduct / le viaduc
    vx, vy = cx, 310
    p.gpoly([(0, 0), (U, 0), (U, 104), (0, 104)], [(0, (30, 20, 20)), (1, (56, 36, 32))])
    for xt in (-500, 0, 450, 960, 1470, 1920, 2420):                # the girders along / les poutres en long
        x_at = lambda y, xt=xt: xt + (vx - xt) * (y / vy)
        p.poly([(x_at(0) - 14, 0), (x_at(0) + 14, 0), (x_at(104) + 6, 104), (x_at(104) - 6, 104)], (98, 44, 30))
    y, th = 0.0, 16.0
    while y < 92 and th > 3:                                         # the girders across, lit from below / en travers
        p.rect(0, y, U, y + th * 0.6, (122, 56, 36))
        p.rect(0, y + th * 0.6, U, y + th * 0.6 + max(1.5, th * 0.12), (232, 128, 66))
        y += th
        th *= 0.82
    p.gpoly([(0, 96), (U, 96), (U, 112), (0, 112)], [(0, (84, 84, 92)), (1, (60, 60, 68))])   # its edge / son rebord
    for x in range(60, int(U), 150):
        p.rect(x - 10, 112, x + 10, 118, (255, 220, 160))
        lamps.append((x, 118, 60, (255, 170, 90), 1.0))
    for x0, x1, top in ((690, 740, 112), (1180, 1230, 112)):         # the far pillars / les piliers du fond
        p.gpoly([(x0, top), (x1, top), (x1, 310), (x0, 310)], [(0, (50, 58, 66)), (1, (34, 38, 44))])
    for x0, x1, side in ((30, 150, 1), (1600, 1724, 1)):             # the big pillars / les gros piliers
        p.gpoly([(x0, 104), (x1, 104), (x1, 340), (x0, 340)], [(0, (96, 128, 132)), (1, (58, 82, 88))])
        p.gpoly([(x1, 104), (x1 + 40, 110), (x1 + 40, 340), (x1, 340)], [(0, (52, 72, 78)), (1, (32, 46, 50))])
        for _ in range(10):
            sx, sy = rng.uniform(x0 + 8, x1 - 8), rng.uniform(140, 320)
            p.line([(sx, sy), (sx + rng.uniform(-3, 3), sy + rng.uniform(10, 40))], 2, (70, 96, 100))
    layers.append(layer(p, "mid"))
    p = Pic(U, V, s)                                                 # the road, the crossing, the people / la route
    p.gpoly([(0, 310), (U, 310), (U, V), (0, V)], [(0, (46, 46, 54)), (1, (24, 24, 30))])
    for k in range(-6, 7):
        x = cx + k * 120
        p.poly([(cx + k * 14 - 3, 312), (cx + k * 14 + 3, 312), (x + 10, V), (x - 10, V)], (60, 60, 68))
    for k in range(7):                                               # the crossing / le passage piéton
        y0 = 320 + k * 18
        p.poly([(1200 + k * 12, y0), (1500 + k * 22, y0), (1506 + k * 22, y0 + 9), (1194 + k * 12, y0 + 9)], (220, 220, 214))
    for k, (x, top, shirt, legs) in enumerate(((1270, 214, (190, 40, 50), (40, 50, 80)), (1306, 220, (60, 110, 190), (30, 30, 40)),
                                              (1344, 208, (30, 30, 36), (30, 30, 36)), (1380, 222, (36, 40, 90), (36, 40, 90)),
                                              (1416, 220, (36, 40, 90), (36, 40, 90)), (1500, 214, (230, 226, 216), (60, 60, 60)),
                                              (1534, 208, (30, 30, 36), (30, 30, 36)))):
        p.ellipse(x - 9, top, x + 9, top + 20, (210, 160, 120))                     # the people watching / les gens
        p.ellipse(x - 10, top - 3, x + 10, top + 9, (24, 20, 20))
        p.poly([(x - 14, top + 22), (x + 14, top + 22), (x + 16, top + 70), (x - 16, top + 70)], shirt)
        if shirt == (36, 40, 90):                                    # the school uniforms / les uniformes
            p.poly([(x - 10, top + 22), (x + 10, top + 22), (x, top + 36)], (240, 240, 236))
        p.rect(x - 10, top + 70, x - 3, top + 112, legs)
        p.rect(x + 3, top + 70, x + 10, top + 112, legs)
    layers.append(layer(p, "near"))
    p = Pic(U, V, s)                                                 # the cars / les voitures
    for x, base, w, body, kind in ((70, 330, 170, (196, 30, 30), "car"), (250, 318, 150, (226, 186, 40), "car"),
                                   (430, 300, 170, (220, 220, 214), "truck"), (610, 312, 180, (110, 124, 150), "van"),
                                   (830, 318, 120, (236, 190, 40), "round"), (1830, 330, 190, (150, 150, 156), "car")):
        _car(p, x, base, w, body, kind, lamps, "cars")
    layers.append(layer(p, "cars", only="cars"))
    p = Pic(U, V, s)                                                 # the jam / l'embouteillage
    for x, base, w, body, kind in ((960, 304, 110, (60, 60, 70), "van"), (1060, 312, 120, (236, 236, 236), "car"),
                                   (720, 330, 160, (40, 90, 60), "car"), (1700, 316, 150, (196, 120, 40), "van")):
        _car(p, x, base, w, body, kind, lamps, "jam")
    layers.append(layer(p, "jam", only="jam"))
    amb = {"horizon": int(310 * s), "lamps": lamps, "looks": ["night+cars", "night+passing", "night+cars+jam"],
           "hooks": {"far": [hook_traffic], "front": [hook_lamps]}}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


def hook_traffic(bd, screen, b, L, now, dt):
    """Cars passing far down the street, their lights. / Des voitures qui passent au fond de la rue, leurs feux."""
    look = bd.cur_look or ""
    if "passing" not in look.split("+") and "jam" not in look.split("+"):
        return
    s, W = bd.s, bd.W
    add = bd.pg.BLEND_RGB_ADD
    for i in range(3):
        period = 7.0 + i * 2.3
        ph = ((now + i * 3.1) % period) / period
        d = 1 if i % 2 == 0 else -1
        x = (ph if d > 0 else 1 - ph) * (W + 200 * s) - 100 * s
        y = (288 + i * 8) * s
        col = (255, 236, 190) if d > 0 else (255, 60, 40)
        for dx in (-10, 10):
            g = _glow(bd, 14 * s, col, 6)
            screen.blit(g, (int(x + dx * s - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=add)

# ============================================================================ USA, the train yard / le dépôt de trains
def _letters(p, x, y, size, text, col, vertical=True):
    """Block letters drawn with strokes (M O T E L...). / Des lettres bâton dessinées en traits."""
    w = size * 0.7
    shapes = {"M": [[(0, 1), (0, 0), (0.5, 0.5), (1, 0), (1, 1)]], "O": "o", "T": [[(0, 0), (1, 0)], [(0.5, 0), (0.5, 1)]],
              "E": [[(1, 0), (0, 0), (0, 1), (1, 1)], [(0, 0.5), (0.8, 0.5)]], "L": [[(0, 0), (0, 1), (1, 1)]],
              "A": [[(0, 1), (0.5, 0), (1, 1)], [(0.25, 0.55), (0.75, 0.55)]], "R": [[(0, 1), (0, 0), (0.9, 0.05), (0.9, 0.45), (0, 0.5), (1, 1)]],
              "K": [[(0, 0), (0, 1)], [(1, 0), (0, 0.55), (1, 1)]], "P": [[(0, 1), (0, 0), (0.9, 0.05), (0.9, 0.45), (0, 0.5)]]}
    for i, ch in enumerate(text):
        ox, oy = (x, y + i * size * 1.25) if vertical else (x + i * w * 1.35, y)
        sh = shapes.get(ch)
        if sh == "o":
            p.ellipse(ox, oy, ox + w, oy + size, col)
            p.ellipse(ox + w * 0.24, oy + size * 0.2, ox + w * 0.76, oy + size * 0.8, (0, 0, 0, 0))
            continue
        for stroke in sh or ():
            p.line([(ox + a * w, oy + b * size) for a, b in stroke], size * 0.18, col)


def _boxcar(p, x0, x1, top, base, col):
    p.gpoly([(x0, top), (x1, top), (x1, base - 16), (x0, base - 16)], [(0, col), (1, shade(col, 0.7))])
    p.rect(x0 - 4, top - 6, x1 + 4, top, shade(col, 0.6))
    for k in range(1, 6):
        x = x0 + (x1 - x0) * k / 6
        p.line([(x, top), (x, base - 16)], 2, shade(col, 0.75))
    p.rect((x0 + x1) / 2 - (x1 - x0) * 0.12, top + (base - top) * 0.15, (x0 + x1) / 2 + (x1 - x0) * 0.12, base - 20, shade(col, 0.8))
    for x in (x0 + (x1 - x0) * 0.15, x1 - (x1 - x0) * 0.15):
        p.ellipse(x - 14, base - 22, x + 14, base + 6, (30, 28, 28))


def build_kof_yard(W, H, s, seed=86):
    """A train yard in the USA: the brick buildings and the MOTEL sign, the signal post, a diesel locomotive facing us,
    the streamlined steam engines, the rails on the paving stones. A wagon from the second round, nearer at the third,
    gone at the fourth, back at the last; the sunset from the third round. / Un dépôt de trains aux États-Unis : un wagon
    à partir du deuxième round, plus près au troisième, parti au quatrième, revenu au dernier ; le couchant au troisième."""
    U, V = W / s, H / s
    rng = random.Random(seed)
    skies = {"day": sky_img(W, H, [(0, (92, 146, 206)), (0.5, (170, 200, 226)), (1, (214, 220, 222))], s,
                            clouds=[(30, 160, (255, 255, 255), 130, 6)]),
             "dusk": sky_img(W, H, [(0, (70, 64, 120)), (0.3, (200, 110, 110)), (0.55, (244, 150, 110)), (0.75, (252, 196, 140)),
                                    (1, (255, 214, 170))], s, clouds=[(40, 170, (255, 170, 150), 140, 7)])}
    layers = []
    lamps = []
    p = Pic(U, V, s)                                                # the town / la ville
    for x0, x1, top, col in ((300, 470, 60, (150, 150, 158)), (470, 640, 110, (170, 160, 150)), (640, 760, 170, (160, 150, 146)),
                             (1060, 1180, 190, (150, 146, 150))):
        p.rect(x0, top, x1, 300, col)
        for wy in range(int(top) + 12, 290, 22):
            for wx in range(int(x0) + 10, int(x1) - 12, 20):
                p.rect(wx, wy, wx + 10, wy + 12, shade(col, 0.7))
    for x0, x1, top, col in ((0, 170, -10, (130, 70, 52)), (170, 330, 30, (112, 98, 92))):    # the near buildings / les proches
        p.gpoly([(x0, top), (x1, top), (x1, 320), (x0, 320)], [(0, col), (1, shade(col, 0.7))])
        for wy in range(int(top) + 20, 300, 40):
            for wx in range(int(x0) + 16, int(x1) - 20, 36):
                p.rect(wx, wy, wx + 20, wy + 26, (54, 50, 56))
                p.rect(wx, wy, wx + 20, wy + 4, shade(col, 1.2))
    p.rect(118, 40, 162, 250, (40, 120, 130))                       # the MOTEL sign / l'enseigne MOTEL
    p.rect(122, 44, 158, 246, (24, 80, 90))
    _letters(p, 128, 54, 30, "MOTEL", (236, 70, 60))
    p.rect(0, 250, 760, 300, (90, 84, 80))                          # the fence / la clôture
    for x in range(0, 760, 8):
        p.line([(x, 250), (x + 8, 300)], 1, (130, 124, 118))
        p.line([(x + 8, 250), (x, 300)], 1, (130, 124, 118))
    p.rect(380, 240, 520, 300, (200, 160, 60))                       # the crates / les caisses
    p.rect(388, 248, 512, 292, (220, 180, 76))
    layers.append(layer(p, "far"))
    p = Pic(U, V, s)                                                # the wagon of some rounds, far / le wagon, au loin
    _boxcar(p, 420, 650, 230, 312, (120, 60, 40))
    layers.append(layer(p, "wagon", only="wagon"))
    p = Pic(U, V, s)                                                # the rails and the paving stones / les rails, les pavés
    vx = 960
    p.gpoly([(0, 300), (U, 300), (U, V), (0, V)], [(0, (110, 104, 100)), (1, (70, 66, 64))])
    with p.plain():
        for y in range(304, int(V), 9):
            for x in range(-(y % 2) * 12, int(U), 24):
                p.ellipse(x, y, x + 22, y + 8, shade((112, 106, 100), rng.uniform(0.8, 1.1)))
    for bx in (-900, -300, 260, 760, 1160, 1660, 2260, 2860):        # the rails converging / les rails qui convergent
        for d in (-18, 18):
            x_end = bx + d * 6
            p.line([(vx + (x_end - vx) * 0.2, 300), (x_end, V)], 4, (140, 96, 70))
            p.line([(vx + (x_end - vx) * 0.2, 300), (x_end, V)], 1.5, (210, 200, 190))
    layers.append(layer(p, "floor"))
    p = Pic(U, V, s)                                                # the signal and the engines / le signal, les locomotives
    p.rect(756, 60, 764, 330, (30, 30, 34))                         # the signal post / le poteau du signal
    p.rect(730, 70, 790, 78, (30, 30, 34))
    for k, col in enumerate(((220, 40, 30), (240, 200, 60))):
        cy = 96 + k * 34
        p.ellipse(744, cy - 14, 776, cy + 14, (24, 24, 26))
        p.ellipse(750, cy - 8, 770, cy + 8, col)
        lamps.append((760, cy, 26, col, 0.9))
    cx = 970                                                        # the diesel engine facing us / la diesel de face
    p.gpoly([(cx - 74, 150), (cx + 74, 150), (cx + 80, 250), (cx - 80, 250)], [(0, (214, 200, 150)), (1, (180, 166, 118))])
    p.rect(cx - 58, 166, cx - 6, 206, (50, 56, 64))
    p.rect(cx + 6, 166, cx + 58, 206, (50, 56, 64))
    p.gpoly([(cx - 80, 250), (cx + 80, 250), (cx + 84, 316), (cx - 84, 316)], [(0, (200, 74, 40)), (1, (130, 40, 24))])
    for y in (262, 280, 298):
        p.line([(cx - 80, y), (cx + 80, y)], 3, (236, 196, 70))
    p.ellipse(cx - 12, 226, cx + 12, 246, (255, 246, 210))
    lamps.append((cx, 236, 60, (255, 236, 190), 1.0))
    p.rect(cx - 90, 316, cx + 90, 330, (40, 38, 38))
    p.gpoly([(1160, 330), (1170, 200), (1220, 140), (1300, 112), (1400, 104), (1520, 108), (1640, 120), (1640, 330)],
            [(0, (214, 214, 208)), (0.5, (176, 176, 172)), (1, (120, 120, 118))])                    # the streamliner / le profilé
    p.ellipse(1176, 150, 1330, 300, (200, 200, 196))
    p.ellipse(1196, 170, 1310, 280, (170, 170, 166))
    p.rect(1170, 214, 1640, 226, (60, 64, 70))                        # its dark band / sa bande sombre
    p.ellipse(1236, 196, 1268, 226, (255, 246, 210))
    lamps.append((1252, 211, 50, (255, 236, 190), 0.8))
    for x in range(1320, 1640, 70):
        p.ellipse(x - 30, 280, x + 30, 340, (40, 40, 44))
        p.ellipse(x - 12, 298, x + 12, 322, (120, 120, 124))
    p.gpoly([(1650, 330), (1650, 140), (1920, 120), (1920, 330)], [(0, (60, 60, 64)), (1, (30, 30, 34))])   # the black engine
    p.ellipse(1690, 140, 1880, 330, (44, 44, 48))
    p.ellipse(1720, 170, 1850, 300, (30, 30, 34))
    p.rect(1770, 92, 1800, 150, (30, 30, 34))                         # its chimney / sa cheminée
    p.ellipse(1772, 186, 1798, 212, (255, 246, 210))
    lamps.append((1785, 199, 46, (255, 236, 190), 0.8))
    layers.append(layer(p, "mid", crop=False, vents=[(1785 * s, 92 * s)]))
    p = Pic(U, V, s)                                                # the wagon nearer / le wagon plus près
    _boxcar(p, 160, 600, 150, 330, (130, 64, 42))
    layers.append(layer(p, "wagon2", only="wagon_near"))
    amb = {"horizon": int(300 * s), "skies": skies, "lamps": lamps, "tints": {"dusk": (255, 206, 176)},
           "looks": ["day", "day+wagon", "dusk+wagon_near", "dusk", "dusk+wagon"],
           "hooks": {"mid": [hook_chimney], "front": [hook_lamps]}}
    return {"sky": skies["day"], "layers": layers, "tw": W, "amb": amb}


def hook_chimney(bd, screen, b, L, now, dt):
    """Steam out of the black engine's chimney. / La vapeur de la cheminée de la locomotive noire."""
    for (x, y) in L.get("vents", ()):
        if bd.rng.random() < dt * 4:
            bd.fx.smoke(x, L["y"] + y, 1, (10, 18), 3.0, (1.6, 2.6), (20, 40), 8, (210, 210, 214), 90, "mid")

# ============================================================================ Japan, the ruined dojo / le dojo en ruine
def build_kof_dojo(W, H, s, seed=87):
    """The dojo of the masters, half in ruins, in the forest: the broken roof above, the pillars and their banners, the
    gate and the fence broken, the shrubs, a stone lantern, the trunks of the forest behind, the fireflies. Night until
    the second round, dawn at the third, morning at the fourth (the fireflies gone), day at the fifth. / Le dojo des
    maîtres, à moitié en ruine, dans la forêt : nuit jusqu'au deuxième round, aube au troisième, matin au quatrième (les
    lucioles parties), jour au cinquième."""
    U, V = W / s, H / s
    rng = random.Random(seed)
    skies = {"night": sky_img(W, H, [(0, (8, 16, 40)), (0.6, (20, 40, 74)), (1, (34, 56, 90))], s, stars=40, seed=seed),
             "dawn": sky_img(W, H, [(0, (40, 46, 96)), (0.45, (170, 120, 140)), (0.8, (246, 180, 140)), (1, (250, 210, 170))], s),
             "morning": sky_img(W, H, [(0, (120, 170, 214)), (0.6, (200, 222, 230)), (1, (236, 236, 222))], s),
             "day": sky_img(W, H, [(0, (90, 150, 214)), (0.6, (170, 204, 230)), (1, (214, 226, 230))], s)}
    layers = []
    p = Pic(U, V, s)                                                # the forest: far trunks in the haze / la forêt
    for depth, (n, col, wmin, wmax) in enumerate(((40, (150, 160, 150), 10, 18), (30, (104, 110, 98), 16, 26), (18, (70, 70, 60), 24, 40))):
        for _ in range(n):
            x = rng.uniform(-20, U + 20)
            w = rng.uniform(wmin, wmax)
            p.gpoly([(x - w / 2, -10), (x + w / 2, -10), (x + w * 0.6, 320), (x - w * 0.6, 320)],
                    [(0, shade(col, 0.9)), (1, shade(col, 1.05))])
        for _ in range(n // 2):                                      # their foliage high up / leur feuillage en haut
            _bush(p, rng.uniform(0, U), rng.uniform(-30, 60), rng.uniform(40, 80), rng, shade((70, 104, 70), 0.9 + depth * 0.1))
    p.grect(0, 200, U, 320, [(0, (180, 190, 180, 0)), (1, (180, 190, 180, 160))])   # the mist at their feet / la brume
    layers.append(layer(p, "far"))
    p = Pic(U, V, s)                                                # the dojo / le dojo
    wood, wood_d = (132, 112, 84), (84, 70, 52)
    for x in range(0, int(U), 34):                                  # the fence / la palissade
        if rng.random() < 0.85:
            h = rng.uniform(40, 70)
            p.rect(x, 300 - h, x + 26, 304, shade((150, 136, 108), rng.uniform(0.8, 1.05)))
    p.rect(0, 254, U, 262, (120, 108, 86))
    for _ in range(26):                                              # the shrubs / les buissons
        _bush(p, rng.uniform(0, U), rng.uniform(286, 312), rng.uniform(26, 46), rng, (58, 100, 52))
    gx = U / 2                                                       # the broken gate / le portail cassé
    for dx in (-150, 150):
        p.gpoly([(gx + dx - 12, 110), (gx + dx + 12, 110), (gx + dx + 14, 320), (gx + dx - 14, 320)], [(0, wood), (1, wood_d)])
    p.rect(gx - 190, 96, gx + 190, 114, wood)
    p.rect(gx - 170, 134, gx + 170, 146, wood_d)
    for k in range(9):                                               # its planks, some fallen / ses planches, certaines tombées
        x = gx - 128 + k * 32
        if k in (2, 6):
            p.poly([(x, 200), (x + 26, 196), (x + 60, 300), (x + 34, 306)], shade(wood, 0.9))
            continue
        p.rect(x, 150 + (k % 3) * 18, x + 26, 318, shade(wood, 0.82 + (k % 4) * 0.06))
    banner = (214, 92, 40)
    for px in (U * 0.3, U * 0.7):                                    # the pillars and their banners / piliers et bannières
        p.gpoly([(px - 20, 0), (px + 20, 0), (px + 22, 320), (px - 22, 320)], [(0, (92, 66, 44)), (1, (60, 42, 28))])
        p.gpoly([(px - 15, 30), (px + 15, 30), (px + 15, 250), (px, 266), (px - 15, 250)], [(0, banner), (1, shade(banner, 0.75))])
        for k in range(7):                                           # marks like brush strokes, no words / des traits
            y = 44 + k * 28
            ink = (60, 20, 10)
            if k % 3 == 0:
                p.line([(px - 7, y + 2), (px + 5, y - 2), (px + 2, y + 9), (px - 6, y + 16)], 3, ink)
                p.ellipse(px + 3, y + 11, px + 8, y + 16, ink)
            elif k % 3 == 1:
                p.line([(px - 6, y), (px - 3, y + 16)], 3, ink)
                p.line([(px + 1, y + 3), (px + 7, y + 1), (px + 4, y + 15)], 3, ink)
            else:
                p.line([(px - 7, y + 6), (px + 7, y + 4)], 3, ink)
                p.line([(px - 2, y - 2), (px + 3, y + 8), (px - 5, y + 16)], 3, ink)
    p.poly([(-20, 0), (U + 20, 0), (U + 20, 40), (U * 0.78, 60), (U * 0.62, 44), (U * 0.5, 70), (U * 0.36, 48), (U * 0.2, 64),
            (-20, 40)], (44, 36, 30))                                 # the broken roof / le toit cassé
    for x in range(0, int(U), 46):                                  # its rafters / ses chevrons
        y_end = 40 + 26 * abs(math.sin(x * 0.013)) + (12 if rng.random() < 0.3 else 0)
        p.line([(x, 0), (x + 10, y_end)], 7, (70, 56, 44))
    for x0 in (0, U * 0.84):                                         # the fallen beams / les poutres tombées
        p.poly([(x0 + 10, 270), (x0 + 200, 236), (x0 + 210, 250), (x0 + 20, 286)], (100, 84, 64))
    lx, ly = U * 0.92, 300                                           # the stone lantern / la lanterne de pierre
    p.rect(lx - 16, ly - 14, lx + 16, ly, (120, 120, 116))
    p.rect(lx - 7, ly - 54, lx + 7, ly - 14, (128, 128, 124))
    p.rect(lx - 16, ly - 84, lx + 16, ly - 54, (120, 120, 116))
    p.rect(lx - 8, ly - 78, lx + 8, ly - 62, (255, 214, 140))
    p.poly([(lx - 28, ly - 84), (lx, ly - 106), (lx + 28, ly - 84)], (100, 100, 96))
    layers.append(layer(p, "mid"))
    p = Pic(U, V, s)                                                 # the wooden floor of the dojo / le plancher du dojo
    p.gpoly([(0, 318), (U, 318), (U, V), (0, V)], [(0, (150, 140, 116)), (1, (96, 88, 70))])
    for y in range(324, int(V), 14):
        p.line([(0, y), (U, y)], 1.5, (110, 100, 80))
    p.poly([(U / 2 - 260, 336), (U / 2 + 260, 336), (U / 2 + 300, 380), (U / 2 - 300, 380)], (170, 160, 130))
    layers.append(layer(p, "floor"))
    amb = {"horizon": int(320 * s), "skies": skies, "looks": ["night", "night", "dawn", "morning", "day"],
           "tints": {"night": (70, 96, 156), "dawn": (210, 170, 176), "morning": (238, 234, 224)},
           "lamps": [(lx, ly - 70, 44, (255, 190, 110), 1.0)], "lamps_on": ("night", "dawn"),
           "flies_on": ("night", "dawn"), "hooks": {"front": [hook_lamps, hook_fireflies]}}
    return {"sky": skies["night"], "layers": layers, "tw": W, "amb": amb}

# ============================================================================ USA, the wharf / le quai
def build_kof_wharf(W, H, s, seed=88):
    """The old wharf of the American team, a junkyard now: the wooden wall and its basketball hoop, the scrawls, the
    wrecked van and car, the drums and the tyres, the edge of the pier and its stripes, the city across the water. Sunset
    at the first round, night at the second and third, a fog from the fourth. / Le vieux quai de l'équipe américaine,
    devenu une casse : coucher de soleil au premier round, nuit aux deuxième et troisième, brume à partir du quatrième."""
    U, V = W / s, H / s
    rng = random.Random(seed)
    skies = {"dusk": sky_img(W, H, [(0, (52, 50, 100)), (0.35, (180, 100, 110)), (0.6, (240, 150, 100)), (0.75, (250, 190, 130)),
                                    (1, (220, 170, 130))], s, clouds=[(40, 150, (250, 160, 140), 120, 6)]),
             "night": sky_img(W, H, [(0, (6, 16, 34)), (0.45, (16, 52, 84)), (0.7, (40, 110, 140)), (1, (20, 60, 80))], s,
                              stars=60, seed=seed)}
    layers = []
    p = Pic(U, V, s)                                                # the city across the water / la ville de l'autre côté
    x = 560
    while x < U:
        w, top = rng.uniform(30, 70), rng.uniform(150, 250)
        p.rect(x, top, x + w, 290, (40, 70, 100))
        for wy in range(int(top) + 6, 286, 9):
            for wx in range(int(x) + 4, int(x + w) - 4, 7):
                if rng.random() < 0.3:
                    p.rect(wx, wy, wx + 3, wy + 4, rng.choice(((160, 220, 255), (255, 230, 170))))
        x += w + rng.uniform(0, 12)
    p.grect(560, 276, U, 300, [(0, (60, 110, 140, 0)), (1, (60, 110, 140, 200))])
    layers.append(layer(p, "far"))
    p = Pic(U, V, s)                                                # the yard / la casse
    wood, wood_d = (160, 92, 50), (96, 52, 28)
    p.gpoly([(0, -10), (560, -10), (560, 320), (0, 320)], [(0, wood), (1, wood_d)])            # the wall / le mur
    for x in range(0, 560, 30):
        p.line([(x, -10), (x, 320)], 2, shade(wood, 0.7))
    p.rect(400, -10, 560, 320, shade(wood, 0.8))
    p.line([(560, -10), (560, 320)], 6, (60, 34, 20))
    p.rect(470, 0, 478, 320, (70, 60, 56))                          # the drainpipe / la gouttière
    for k in range(6):                                              # the scrawls, no words / des gribouillis
        cx, cy = rng.uniform(150, 520), rng.uniform(60, 260)
        col = rng.choice(((200, 40, 40), (236, 230, 220), (220, 200, 60)))
        p.line([(cx + rng.uniform(-40, 40), cy + rng.uniform(-20, 20)) for _ in range(6)], 4, col)
    p.rect(30, 20, 150, 110, (236, 236, 230))                       # the backboard / le panneau de basket
    p.rect(36, 26, 144, 104, (40, 40, 44))
    p.rect(66, 56, 114, 92, (236, 236, 230))
    p.rect(70, 60, 110, 88, (40, 40, 44))
    p.ellipse(56, 104, 124, 120, (230, 100, 30))                    # the hoop and its net / le cercle et le filet
    p.ellipse(62, 107, 118, 117, (0, 0, 0, 0))
    for k in range(7):
        x = 62 + k * 9
        p.line([(x, 112), (90 + (x - 90) * 0.6, 150)], 1.5, (236, 236, 230))
    p.rect(150, 60, 160, 66, (60, 56, 56))
    for x0, y0 in ((0, 250), (60, 270), (20, 214)):                 # the crates / les caisses
        p.rect(x0, y0, x0 + 70, y0 + 60, (170, 120, 70))
        p.line([(x0, y0), (x0 + 70, y0 + 60)], 3, (120, 80, 44))
    p.poly([(820, 200), (900, 60), (930, 70), (880, 220)], (190, 196, 206))       # a sheet of metal up / une tôle dressée
    p.poly([(880, 210), (980, 100), (1000, 120), (930, 230)], (60, 90, 150))
    vx0, vx1 = 700, 1010                                             # the wrecked van / le van épave
    p.gpoly([(vx0, 230), (vx0 + 40, 190), (vx1 - 20, 186), (vx1, 220), (vx1, 300), (vx0, 300)],
            [(0, (226, 220, 206)), (1, (170, 150, 130))])
    p.rect(vx0, 250, vx1, 300, (180, 120, 70))
    for k in range(4):
        x = vx0 + 50 + k * 64
        p.rect(x, 200, x + 50, 238, (50, 56, 62))
    p.line([(vx0 + 60, 210), (vx0 + 100, 236)], 2, (200, 210, 220))
    for x in (vx0 + 60, vx1 - 60):
        p.ellipse(x - 26, 282, x + 26, 330, (30, 30, 30))
    p.ellipse(1040, 236, 1220, 330, (214, 206, 186))                 # the wrecked car / la voiture épave
    p.rect(1040, 290, 1220, 330, (214, 206, 186))
    p.ellipse(1080, 246, 1180, 290, (60, 66, 72))
    for x in (1070, 1190):
        p.ellipse(x - 20, 300, x + 20, 340, (30, 30, 30))
    for k, x in enumerate((1250, 1290, 1330)):                       # the drums / les fûts
        p.gpoly([(x - 18, 262 - k % 2 * 10), (x + 18, 262 - k % 2 * 10), (x + 18, 324), (x - 18, 324)],
                [(0, (170, 90, 40)), (1, (110, 56, 26))])
        p.line([(x - 18, 280), (x + 18, 280)], 2, (90, 44, 20))
    for k in range(4):                                               # the tyres / les pneus
        p.ellipse(590 + k * 10, 300 - k * 14, 650 + k * 10, 316 - k * 14, (26, 26, 28))
    p.gpoly([(1360, 296), (U, 296), (U, 312), (1360, 312)], [(0, (150, 150, 150)), (1, (110, 110, 110))])   # the edge
    for x in range(1360, int(U), 40):                                # its stripes / ses rayures
        p.poly([(x, 296), (x + 20, 296), (x + 10, 312), (x - 10, 312)], (230, 190, 40))
    mx = 1840                                                        # a man watching / un homme qui regarde
    p.rect(mx - 12, 230, mx + 12, 280, (70, 50, 40))
    p.ellipse(mx - 9, 212, mx + 9, 230, (190, 140, 100))
    p.rect(mx - 10, 280, mx - 3, 300, (40, 36, 40))
    p.rect(mx + 3, 280, mx + 10, 300, (40, 36, 40))
    p.gpoly([(0, 316), (U, 300), (U, V), (0, V)], [(0, (130, 110, 70)), (1, (80, 66, 40))])   # the ground / le sol
    for _ in range(9):                                               # the puddles / les flaques
        x, y = rng.uniform(300, U), rng.uniform(320, 380)
        w = rng.uniform(40, 120)
        p.ellipse(x - w, y - 6, x + w, y + 6, (70, 120, 160))
    layers.append(layer(p, "mid"))
    p = Pic(U, V, s)                                                 # the fog of the last rounds / la brume des derniers rounds
    for y in (200, 250, 300, 350):
        for k in range(6):
            x = rng.uniform(0, U)
            p.ellipse(x - 300, y - 30, x + 300, y + 34, (190, 206, 190, 110))
    p.blur(18)
    layers.append(layer(p, "fog", only="fog"))
    amb = {"horizon": int(300 * s), "skies": skies, "looks": ["dusk", "night", "night", "night+fog"],
           "tints": {"dusk": (255, 214, 190), "night": (110, 150, 196)},
           "lamps": [(1300, 120, 90, (120, 200, 255), 0.6)], "lamps_on": ("night",), "hooks": {"front": [hook_lamps]}}
    return {"sky": skies["dusk"], "layers": layers, "tw": W, "amb": amb}

# ============================================================================ the Black Noah / le Black Noah
def _tube(p, pts, w, col, hi):
    """A pipe or a cable of the ship: dark, lit along its top. / Un tuyau ou un câble du vaisseau."""
    p.line(pts, w, col)
    p.line([(x, y - w * 0.28) for x, y in pts], max(1.5, w * 0.22), hi)


def _sea_img(W, H, s, seed):
    """The sea behind the window: the light from above, the wreck of another ship. / La mer derrière la vitre."""
    sky = vgrad(W, H, [(0, (30, 120, 112)), (0.5, (40, 150, 128)), (0.8, (18, 84, 76)), (1, (8, 40, 40))])
    over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    rng = random.Random(seed)
    for _ in range(9):                                               # rays of light / des rayons de lumière
        x = rng.uniform(0.3, 0.7) * W
        w = rng.uniform(20, 60) * s
        d.polygon([(x, 0), (x + w, 0), (x + w * 3 + 120 * s, H), (x + 120 * s, H)], fill=(170, 240, 220, 30))
    cx = W / 2                                                       # the wreck / l'épave
    d.polygon([(cx - 260 * s, H * 0.62), (cx - 120 * s, H * 0.48), (cx + 200 * s, H * 0.5), (cx + 300 * s, H * 0.6),
               (cx + 260 * s, H * 0.66), (cx - 240 * s, H * 0.68)], fill=(10, 56, 54, 220))
    d.rectangle([cx - 30 * s, H * 0.36, cx + 40 * s, H * 0.5], fill=(10, 56, 54, 220))
    d.line([(cx + 10 * s, H * 0.36), (cx + 6 * s, H * 0.24)], fill=(10, 56, 54, 220), width=max(1, int(6 * s)))
    over = over.filter(ImageFilter.GaussianBlur(3 * s))
    sky.paste(over, (0, 0), over)
    return sky


def build_kof_noah(W, H, s, seed=89):
    """The Black Noah under the sea: the dark hall of pipes and ribs, its two lamps, the frames on the walls, the pool of
    blood under the great window, the red carpet and its grating, the sea behind the glass with the wreck of another
    ship, sharks and jellyfish. The light grows bluer at each round. / Le Black Noah sous la mer : la lumière bleuit à
    chaque round."""
    U, V = W / s, H / s
    rng = random.Random(seed)
    sea = _sea_img(W, H, s, seed)
    layers = []
    p = Pic(U, V, s)
    p.grect(0, 0, U, 330, [(0, (40, 30, 30)), (0.6, (28, 20, 20)), (1, (16, 10, 10))])
    for _ in range(26):                                              # the ribs on the walls / les côtes des murs
        x = rng.uniform(0, U)
        if abs(x - U / 2) < 300:
            continue
        p.line([(x, 0), (x + rng.uniform(-30, 30), 120), (x + rng.uniform(-20, 20), 320)], rng.uniform(8, 16), (58, 44, 40))
        p.line([(x - 3, 0), (x + rng.uniform(-30, 30) - 3, 120)], 2, (96, 78, 70))
    for _ in range(18):                                              # the pipes and cables / tuyaux et câbles
        y0 = rng.uniform(20, 290)
        x0 = rng.uniform(-100, U)
        amp, ph, slope = rng.uniform(10, 30), rng.uniform(0, 6), rng.uniform(-0.25, 0.25)
        pts = [(x0 + k * 20, y0 + math.sin(k * 0.25 + ph) * amp + k * 20 * slope) for k in range(rng.randint(10, 30))]
        _tube(p, pts, rng.uniform(9, 18), (52, 42, 40), (112, 94, 86))
    wx0, wx1, wtop, wbot = U / 2 - 280, U / 2 + 280, 70, 300          # the great window / la grande vitre
    arc = p.arc_poly(U / 2, wtop + 120, 280, 120, 180, 360, 30)
    frame = [(wx0 - 30, wbot + 20)] + [(x + (x - U / 2) * 0.11, y - 26) for x, y in arc] + [(wx1 + 30, wbot + 20)]
    p.poly(frame, (66, 52, 46))
    for k in range(31):                                              # its vertebrae / ses vertèbres
        a = math.radians(180 + k * 6)
        x = U / 2 + math.cos(a) * 296
        y = wtop + 120 + math.sin(a) * 134
        p.ellipse(x - 11, y - 9, x + 11, y + 9, (88, 72, 64))
        p.ellipse(x - 6, y - 7, x + 4, y - 1, (130, 112, 100))
    for x in (wx0 - 16, wx1 + 16):
        for y in range(int(wtop + 120), int(wbot + 10), 20):
            p.ellipse(x - 11, y - 9, x + 11, y + 9, (88, 72, 64))
    p.poly([(wx0, wbot)] + arc + [(wx1, wbot)], (0, 0, 0, 0))
    for fx in (470, U - 470):                                        # the frames on the walls / les cadres aux murs
        p.rect(fx - 56, 100, fx + 56, 214, (120, 96, 60))
        p.rect(fx - 46, 110, fx + 46, 204, (60, 10, 14))
        p.ellipse(fx - 18, 136, fx + 18, 178, (90, 22, 26))
    for lx in (300, U - 300):                                        # the lamps / les lampes
        p.ellipse(lx - 26, 56, lx + 26, 96, (90, 80, 70))
        p.ellipse(lx - 16, 62, lx + 16, 90, (255, 250, 220))
    p.ellipse(U / 2 - 210, 250, U / 2 + 210, 316, (70, 54, 48))     # the pool of blood / le bassin de sang
    p.ellipse(U / 2 - 190, 258, U / 2 + 190, 306, (120, 10, 16))
    p.ellipse(U / 2 - 120, 266, U / 2 + 60, 286, (170, 30, 34))
    layers.append(layer(p, "mid"))
    p = Pic(U, V, s)                                                 # the carpet and the grating / le tapis et la grille
    p.gpoly([(0, 316), (U, 316), (U, V), (0, V)], [(0, (112, 20, 24)), (1, (60, 8, 10))])
    with p.plain():
        for y in range(330, int(V), 18):
            for x in range(0, int(U), 36):
                p.poly([(x, y), (x + 9, y - 6), (x + 18, y), (x + 9, y + 6)], (50, 6, 8))
    p.poly([(U / 2 - 150, 316), (U / 2 + 150, 316), (U / 2 + 260, V), (U / 2 - 260, V)], (60, 60, 64))
    for k in range(12):
        t = k / 11
        p.line([(U / 2 - 150 + 300 * t, 316), (U / 2 - 260 + 520 * t, V)], 2, (110, 110, 116))
    layers.append(layer(p, "floor"))
    lamps = [(300, 76, 110, (255, 240, 200), 1.2), (U - 300, 76, 110, (255, 240, 200), 1.2)]
    amb = {"horizon": int(300 * s), "lamps": lamps, "looks": ["r0", "r1", "r2", "r3", "r4"],
           "tints": {"r1": (222, 228, 255), "r2": (194, 208, 255), "r3": (170, 192, 255), "r4": (146, 174, 255)},
           "sea": (wx0, wtop, wx1, wbot), "hooks": {"sky": [hook_sea], "front": [hook_lamps]}}
    return {"sky": sea, "layers": layers, "tw": W, "amb": amb}


def hook_sea(bd, screen, b, L, now, dt):
    """Sharks and jellyfish behind the window, bubbles going up. / Requins et méduses derrière la vitre, des bulles."""
    s = bd.s
    x0, y0, x1, y1 = b["amb"]["sea"]
    pg = bd.pg
    for i in range(2):                                               # the sharks / les requins
        period = 14.0 + i * 5
        ph = ((now + i * 6) % period) / period
        d = 1 if i == 0 else -1
        x = (x0 - 120 + (x1 - x0 + 240) * (ph if d > 0 else 1 - ph)) * s
        y = (y0 + 60 + i * 70 + math.sin(now * 0.7 + i) * 8) * s
        body = [(x - 60 * s * d, y), (x - 20 * s * d, y - 12 * s), (x + 40 * s * d, y - 6 * s), (x + 60 * s * d, y),
                (x + 40 * s * d, y + 8 * s), (x - 20 * s * d, y + 10 * s)]
        pg.draw.polygon(screen, (12, 50, 52), body)
        pg.draw.polygon(screen, (12, 50, 52), [(x, y - 10 * s), (x + 10 * s * d, y - 30 * s), (x + 22 * s * d, y - 8 * s)])
        pg.draw.polygon(screen, (12, 50, 52), [(x - 56 * s * d, y), (x - 76 * s * d, y - 18 * s), (x - 70 * s * d, y + 16 * s)])
    add = pg.BLEND_RGB_ADD
    for i in range(3):                                               # the jellyfish / les méduses
        ph = ((now * 0.05 + i * 0.37) % 1.0)
        x = (x0 + 80 + i * 170 + math.sin(now * 0.4 + i) * 20) * s
        y = (y1 - (y1 - y0 + 40) * ph) * s
        g = _glow(bd, 16 * s, (200, 150, 220), 5)
        screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=add)
        for k in range(3):
            pg.draw.line(screen, (120, 110, 150), (int(x + (k - 1) * 5 * s), int(y)),
                         (int(x + (k - 1) * 5 * s + math.sin(now * 2 + k) * 4 * s), int(y + 26 * s)), max(1, int(s)))
    for i in range(10):                                              # the bubbles / les bulles
        ph = ((now * 0.12 + i * 0.13) % 1.0)
        x = (x0 + 40 + (i * 53) % (x1 - x0 - 80) + math.sin(now * 2 + i) * 4) * s
        y = (y1 - (y1 - y0) * ph) * s
        g = _glow(bd, 4 * s, (180, 240, 230), 4)
        screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=add)

# ---------------------------------------------------------------------------- registration / enregistrement
LOOKS = {"kof_noah": build_kof_noah, "kof_wharf": build_kof_wharf, "kof_dojo": build_kof_dojo, "kof_yard": build_kof_yard, "kof_osaka": build_kof_osaka, "kof_china": build_kof_china, "kof_korea": build_kof_korea, "kof_mideast": build_kof_mideast, "kof_spain": build_kof_spain}
for _name, _fn in LOOKS.items():
    hd_bg.BUILDERS[_name] = _fn
    hd_bg.BUILDERS["fight_" + _name] = fight_stage(_fn)
KOF98_STAGES = tuple("fight_" + n for n in LOOKS)
