"""Animated effects of the HD screen: particles, explosions, tracers, shell casings, screen shake, flashes.

Effect images are prepared once with Pillow and cached as pygame surfaces. Light effects are added
(BLEND_RGB_ADD), smoke and objects are blended with their transparency. Two layers, "back" and "front".

Effets animés de l'écran HD : particules, explosions, traçantes, douilles, secousses, éclairs.

Les images des effets (halos lumineux, fumée, douilles, éclats, étoiles de tir) sont préparées
une fois avec Pillow puis gardées en cache en surfaces pygame. Les effets lumineux s'ajoutent
à l'image (BLEND_RGB_ADD), la fumée et les objets se posent avec leur transparence.

Deux plans : « back » (derrière les panneaux, dans le décor) et « front » (devant tout).
"""

import math
import random
from collections import OrderedDict

from PIL import Image, ImageChops, ImageDraw, ImageFilter

RADII = (2, 3, 4, 5, 6, 8, 10, 13, 16, 20, 25, 32, 40, 50, 64, 80, 100, 128, 160, 200, 256, 320, 400)
LEVELS = 12

FIRE = (255, 150, 50)
FIRE_HOT = (255, 210, 120)
SPARK = (255, 200, 90)
WHITE = (255, 255, 255)
SMOKE = (58, 52, 62)


def bucket(r):
    for b in RADII:
        if r <= b:
            return b
    return RADII[-1]


def ease_out(k):
    return 1 - (1 - k) ** 3


class LRU(OrderedDict):
    """Cache d'images limité en octets : les moins utilisées partent d'abord."""

    def __init__(self, budget):
        super().__init__()
        self.budget = budget
        self.used = 0

    def get(self, key, default=None):
        v = OrderedDict.get(self, key)
        if v is None:
            return default
        self.move_to_end(key)
        return v

    def __setitem__(self, key, surf):
        if key in self:
            self.used -= self._size(OrderedDict.__getitem__(self, key))
        OrderedDict.__setitem__(self, key, surf)
        self.used += self._size(surf)
        while self.used > self.budget and len(self) > 1:
            _, old = self.popitem(last=False)
            self.used -= self._size(old)

    @staticmethod
    def _size(surf):
        try:
            return surf.get_width() * surf.get_height() * surf.get_bytesize()
        except AttributeError:
            return 0


class Sprites:
    """Images des effets, préparées à la demande et gardées en cache."""

    BUDGET = 80 * 1024 * 1024            # mémoire maximale des images en cache

    def __init__(self, hd):
        self.hd, self.pg, self.s = hd, hd.pg, hd.s
        self.cache = LRU(self.BUDGET)
        self.base = {}
        self.ring_buf = None
        g = Image.radial_gradient("L")                         # 256 x 256, noir au centre, 181 au milieu des bords
        self.radial = g.point(lambda v: max(0, 255 - v * 255 // 181))     # blanc au centre, noir dès le bord du cercle

    # -- halos lumineux (s'additionnent à l'image)
    def glow(self, r, color, level=LEVELS, hot=0.35):
        r = bucket(max(2, r))
        level = max(1, min(LEVELS, int(level)))
        if r >= 128:                                             # grands halos : 4 niveaux suffisent
            level = max(3, (level + 1) // 3 * 3)
        elif r >= 64:
            level = max(2, level // 2 * 2)
        key = ("g", r, color, level, hot)
        s = self.cache.get(key)
        if s is None:
            size = 2 * r + 1
            base = self.radial.resize((size, size), Image.BILINEAR)
            k = level / LEVELS
            chans = []
            for c in color:
                lut = []
                for v in range(256):
                    x = v / 255.0
                    i = x ** 2.2 * 0.85
                    h = (x ** 9) * hot
                    lut.append(min(255, int((c * i + 255 * h) * k)))
                chans.append(base.point(lut))
            s = self.hd._surf(Image.merge("RGB", chans))
            self.cache[key] = s
        return s

    # -- fumée (transparente)
    def puff(self, r, color, variant=0):
        r = bucket(max(3, r))
        key = ("p", r, color, variant % 3)
        s = self.cache.get(key)
        if s is None:
            size = 2 * r + 1
            base = self.radial.resize((size, size), Image.BILINEAR).point(lambda v: int(255 * (v / 255.0) ** 1.3))
            rng = random.Random(variant * 7 + r)
            tex = Image.new("L", (size, size), 0)
            td = ImageDraw.Draw(tex)
            for _ in range(9):                                  # quelques boules pour un nuage irrégulier
                cx, cy = rng.uniform(0.3, 0.7) * size, rng.uniform(0.3, 0.7) * size
                rr = rng.uniform(0.18, 0.36) * size
                td.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=rng.randint(150, 255))
            tex = tex.filter(ImageFilter.GaussianBlur(max(1, size / 10)))
            alpha = Image.composite(tex, Image.new("L", (size, size), 0), base)
            alpha = alpha.point(lambda v: int(v * 0.8))
            img = Image.new("RGBA", (size, size), tuple(color) + (0,))
            shade = Image.new("RGB", (size, size), tuple(color))
            hi = tuple(min(255, int(c * 1.35) + 12) for c in color)
            sd = ImageDraw.Draw(shade)
            for y in range(size):                               # éclairé par le haut
                k = y / max(1, size - 1)
                sd.line([0, y, size, y], fill=tuple(int(hi[j] * (1 - k) + color[j] * k) for j in range(3)))
            img = shade.convert("RGBA")
            img.putalpha(alpha)
            s = self.hd._surf(img)
            self.cache[key] = s
        return s

    # -- traînée lumineuse orientée (traçante, étincelle)
    def streak(self, length, width, color, angle, level=LEVELS):
        length = max(6, int(round(length / 6.0)) * 6)
        width = max(2, int(width))
        level = max(1, min(LEVELS, int(level)))
        a = int(round(angle / 3.0)) * 3 % 360
        key = ("s", length, width, color, a, level)
        s = self.cache.get(key)
        if s is None:
            bkey = ("sb", length, width, color, level)
            b = self.base.get(bkey)
            if b is None:
                w, h = length + width * 2, width * 4 + 2
                img = Image.new("RGB", (w, h))
                d = ImageDraw.Draw(img)
                k = level / LEVELS
                for i in range(w):                               # queue froide, tête chaude
                    x = i / max(1, w - 1)
                    glowc = tuple(int(c * (0.15 + 0.85 * x) * k) for c in color)
                    d.line([i, h // 2 - width, i, h // 2 + width], fill=glowc)
                img = img.filter(ImageFilter.GaussianBlur(max(1, width * 0.6)))
                d = ImageDraw.Draw(img)
                core = tuple(int(min(255, 255 * (0.3 + 0.7 * k))) for _ in range(3))
                d.line([w * 0.45, h // 2, w - width, h // 2], fill=core, width=max(1, width // 2))
                b = self.hd._surf(img)
                self.base[bkey] = b
            s = self.pg.transform.rotozoom(b, -a, 1.0)
            self.cache[key] = s
        return s

    # -- faisceau de projecteur (cône doux, part de l'extrémité gauche)
    def beam(self, length, width, color, angle, level=LEVELS):
        length = max(20, int(round(length / 10.0)) * 10)
        width = max(8, int(width))
        level = max(1, min(LEVELS, int(level)))
        a = int(round(angle / 2.0)) * 2 % 360
        key = ("bm", length, width, color, a, level)
        s = self.cache.get(key)
        if s is None:
            bkey = ("bmb", length, width, color, level)
            b = self.base.get(bkey)
            if b is None:
                h = width + 12
                m = Image.new("L", (length, h), 0)
                ImageDraw.Draw(m).polygon([(0, h / 2 - 1.5), (length, 6), (length, h - 6), (0, h / 2 + 1.5)], fill=255)
                fade = Image.new("L", (length, h), 0)
                fd = ImageDraw.Draw(fade)
                for i in range(length):
                    fd.line([i, 0, i, h], fill=int(255 * (1 - i / length) ** 1.3))
                m = ImageChops.multiply(m, fade).filter(ImageFilter.GaussianBlur(max(2, width / 7)))
                k = level / LEVELS
                b = self.hd._surf(Image.merge("RGB", [m.point(lambda v, c=c: int(c * v / 255 * k)) for c in color]))
                self.base[bkey] = b
            s = self.pg.transform.rotozoom(b, -a, 1.0)
            self.cache[key] = s
        return s

    # -- étoile de tir (bouche du canon)
    def star(self, r, color, variant=0, points=5):
        r = bucket(max(4, r))
        key = ("st", r, color, variant % 4, points)
        s = self.cache.get(key)
        if s is None:
            size = 2 * r + 1
            rng = random.Random(variant * 13 + r)
            big = Image.new("L", (size * 2, size * 2), 0)
            d = ImageDraw.Draw(big)
            c = size
            n = points * 2
            rot = rng.uniform(0, math.pi)
            pts = []
            for i in range(n):
                rr = size * 0.98 * rng.uniform(0.7, 1.0) if i % 2 == 0 else size * 0.28
                a = rot + i * math.pi * 2 / n
                pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
            d.polygon(pts, fill=255)
            core = big.resize((size, size), Image.LANCZOS)
            glow = core.filter(ImageFilter.GaussianBlur(max(2, size / 10)))
            out = Image.merge("RGB", [glow.point(lambda v, cc=cc: min(255, cc * v // 255)) for cc in color])
            out = ImageChops.add(out, Image.merge("RGB", (core, core, core.point(lambda v: v * 4 // 5))))
            s = self.hd._surf(out)
            self.cache[key] = s
        return s

    # -- objets qui tournent (douille, éclat, casque, grenade...)
    def register(self, name, img):
        """Image Pillow RGBA d'un objet, prête à tourner."""
        self.base[("obj", name)] = self.hd._surf(img)

    def obj(self, name, angle, steps=24):
        a = int(round(angle / (360.0 / steps))) % steps
        key = ("o", name, a, steps)
        s = self.cache.get(key)
        if s is None:
            b = self.base.get(("obj", name))
            if b is None:
                return None
            s = self.pg.transform.rotozoom(b, a * 360.0 / steps, 1.0)
            self.cache[key] = s
        return s

    def draw_ring(self, screen, x, y, r, width, color, k):
        """Onde de choc : trois cercles de plus en plus fins et clairs, ajoutés à l'image."""
        pg = self.pg
        r, width = int(r), max(2, int(width))
        size = 2 * (r + width * 2) + 4
        if self.ring_buf is None or self.ring_buf.get_width() < size:
            self.ring_buf = pg.Surface((max(size, int(1200 * self.s)),) * 2).convert()
        buf = self.ring_buf
        area = pg.Rect(0, 0, size, size)
        buf.fill((0, 0, 0), area)
        c = size // 2
        for rr, ww, f in ((r + width, width * 2 + 1, 0.3), (r + width // 2, width + 1, 0.6), (r, max(2, width // 3), 1.0)):
            col = tuple(min(255, int(v * k * f)) for v in color)
            if rr > ww:
                pg.draw.circle(buf, col, (c, c), rr, ww)
        screen.blit(buf, (int(x - c), int(y - c)), area=area, special_flags=pg.BLEND_RGB_ADD)


class Particle:
    __slots__ = ("kind", "x", "y", "vx", "vy", "ay", "drag", "t0", "life", "r0", "r1", "col", "a0", "a1",
                 "rot", "vrot", "floor", "bounce", "layer", "name", "data", "dead", "trail", "on_end", "lag", "wob")

    def __init__(self, kind, x, y, t0, life, layer="front"):
        self.kind, self.x, self.y, self.t0, self.life, self.layer = kind, x, y, t0, life, layer
        self.vx = self.vy = self.ay = self.drag = 0.0
        self.r0 = self.r1 = 4.0
        self.col = WHITE
        self.a0, self.a1 = 1.0, 0.0
        self.rot = self.vrot = 0.0
        self.floor = None
        self.bounce = 0.4
        self.name = None
        self.data = None
        self.dead = False
        self.trail = 0.0
        self.on_end = None
        self.lag = 0.0
        self.wob = 0.0


class FX:
    """Toutes les particules en cours, les secousses de l'écran et les éclairs."""

    MAX = 900

    def __init__(self, hd, rng=None):
        self.hd, self.pg, self.s = hd, hd.pg, hd.s
        self.sp = Sprites(hd)
        self.rng = rng or random.Random()
        self.parts = []
        self.timers = []
        self.shakes = []
        self.flashes = []
        self.now = 0.0
        self.last = None
        self.flash_surf = None

    # ------------------------------------------------------------ temps
    def update(self, now):
        dt = 0.0 if self.last is None else max(0.0, min(0.1, now - self.last))
        self.last = self.now = now
        if self.timers:
            due = [t for t in self.timers if t[0] <= now]
            if due:
                self.timers = [t for t in self.timers if t[0] > now]
                for _, fn, args in sorted(due, key=lambda t: t[0]):
                    fn(*args)
        alive = []
        for p in self.parts:
            age = now - p.t0
            if age < 0:
                alive.append(p)
                continue
            if age >= p.life or p.dead:
                if p.on_end is not None:
                    fn, args = p.on_end
                    p.on_end = None
                    fn(*args)
                continue
            if p.drag:
                f = max(0.0, 1.0 - p.drag * dt)
                p.vx *= f
                p.vy *= f
            p.vy += p.ay * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            if p.wob:                                                    # confettis qui flottent
                p.x += math.sin(age * 5.0 + p.t0 * 7.0) * p.wob * dt
            p.rot += p.vrot * dt
            if p.floor is not None and p.y > p.floor and p.vy > 0:
                p.y = p.floor
                p.vy = -p.vy * p.bounce
                p.vx *= 0.55
                p.vrot *= 0.5
                if abs(p.vy) < 60 * self.s:
                    p.vy = 0.0
                    p.ay = 0.0
            if p.trail and p.kind in ("proj", "rocket"):
                p.lag += dt
                while p.lag >= p.trail:
                    p.lag -= p.trail
                    self._trail(p, now)
            alive.append(p)
        if len(alive) > self.MAX:
            alive = alive[-self.MAX:]
        self.parts = alive
        self.shakes = [sh for sh in self.shakes if now - sh[0] < sh[2]]
        self.flashes = [f for f in self.flashes if now - f[0] < f[2]]

    def later(self, delay, fn, *args):
        self.timers.append((self.now + delay, fn, args))

    def add(self, p):
        self.parts.append(p)
        return p

    # ------------------------------------------------------------ écran qui tremble, éclairs
    def shake(self, amp, dur):
        self.shakes.append((self.now, amp * self.s, dur))

    def offset(self):
        if not self.shakes:
            return 0, 0
        a = 0.0
        for t0, amp, dur in self.shakes:
            k = 1 - (self.now - t0) / dur
            a += amp * k * k
        n = self.now
        return int(round(a * math.sin(n * 71.0) * 0.9)), int(round(a * math.cos(n * 53.0) * 0.6))

    def flash(self, color, strength, dur):
        """Toute l'image s'éclaire un instant (strength : 0 à 1)."""
        self.flashes.append((self.now, color, dur, strength))

    def draw_flash(self, screen):
        if not self.flashes:
            return
        r = g = b = 0.0
        for t0, color, dur, st in self.flashes:
            k = (1 - (self.now - t0) / dur) ** 2 * st
            r += color[0] * k
            g += color[1] * k
            b += color[2] * k
        c = (min(255, int(r)), min(255, int(g)), min(255, int(b)))
        if c == (0, 0, 0):
            return
        if self.flash_surf is None or self.flash_surf.get_size() != screen.get_size():
            self.flash_surf = self.pg.Surface(screen.get_size()).convert()
        self.flash_surf.fill(c)
        screen.blit(self.flash_surf, (0, 0), special_flags=self.pg.BLEND_RGB_ADD)

    # ------------------------------------------------------------ dessin
    def draw(self, screen, layer):
        pg, sp, now = self.pg, self.sp, self.now
        add = pg.BLEND_RGB_ADD
        W, H = screen.get_size()
        for p in self.parts:
            if p.layer != layer or p.dead:
                continue
            age = now - p.t0
            if age < 0:
                continue
            k = min(1.0, age / p.life)
            kind = p.kind
            if p.x < -400 or p.x > W + 400 or p.y < -400 or p.y > H + 400:
                p.dead = True
                continue
            if kind == "glow":
                r = p.r0 + (p.r1 - p.r0) * ease_out(k)
                lv = (p.a0 + (p.a1 - p.a0) * k) * LEVELS
                if lv < 0.5:
                    continue
                s = sp.glow(r, p.col, lv, hot=p.data if p.data is not None else 0.35)
                screen.blit(s, (int(p.x - s.get_width() / 2), int(p.y - s.get_height() / 2)), special_flags=add)
            elif kind == "puff":
                r = p.r0 + (p.r1 - p.r0) * ease_out(k)
                a = p.a0 + (p.a1 - p.a0) * k
                if a <= 2:
                    continue
                s = sp.puff(r, p.col, p.data or 0)
                s.set_alpha(int(a))
                screen.blit(s, (int(p.x - s.get_width() / 2), int(p.y - s.get_height() / 2)))
            elif kind == "spark":
                sp_ = math.hypot(p.vx, p.vy)
                ln = max(6.0, min(p.r1, sp_ * 0.045)) * (1 - 0.5 * k)
                lv = (p.a0 + (p.a1 - p.a0) * k) * LEVELS
                if lv < 0.5:
                    continue
                ang = math.degrees(math.atan2(p.vy, p.vx))
                s = sp.streak(ln, p.r0, p.col, ang, lv)
                screen.blit(s, (int(p.x - s.get_width() / 2), int(p.y - s.get_height() / 2)), special_flags=add)
            elif kind == "tracer":
                lv = (p.a0 + (p.a1 - p.a0) * k) * LEVELS
                ln = p.r1 * (1 - 0.6 * k)
                ang = math.degrees(math.atan2(p.vy, p.vx))
                s = sp.streak(ln, max(2, p.r0 * (1 - 0.5 * k)), p.col, ang, lv)
                screen.blit(s, (int(p.x - s.get_width() / 2), int(p.y - s.get_height() / 2)), special_flags=add)
            elif kind == "star":
                lv = (p.a0 + (p.a1 - p.a0) * k) * LEVELS
                r = p.r0 + (p.r1 - p.r0) * k
                if lv < 0.5:
                    continue
                s = sp.star(r, p.col, p.data or 0)
                if lv < LEVELS:
                    s = s.copy()
                    s.fill((int(255 * lv / LEVELS),) * 3, special_flags=pg.BLEND_RGB_MULT)
                screen.blit(s, (int(p.x - s.get_width() / 2), int(p.y - s.get_height() / 2)), special_flags=add)
            elif kind in ("obj", "proj", "rocket"):
                s = sp.obj(p.name, p.rot, 24 if kind != "rocket" else 72)
                if s is None:
                    continue
                fade = 1.0 if k < 0.75 or kind != "obj" else (1 - k) / 0.25
                if fade < 1.0:
                    s.set_alpha(int(255 * fade))
                screen.blit(s, (int(p.x - s.get_width() / 2), int(p.y - s.get_height() / 2)))
                if fade < 1.0:
                    s.set_alpha(255)
            elif kind == "ring":
                r = p.r0 + (p.r1 - p.r0) * ease_out(k)
                lv = (p.a0 + (p.a1 - p.a0) * k) * LEVELS
                if lv < 0.5:
                    continue
                sp.draw_ring(screen, p.x, p.y, r, p.data or 6 * self.s, p.col, lv / LEVELS)
            elif kind == "text":
                self._draw_text(screen, p, k)

    def _draw_text(self, screen, p, k):
        hd = self.hd
        text, key, size, color, align = p.data
        pop = 1.0 + 0.45 * max(0.0, 1 - k / 0.12)
        fade = 1.0 if k < 0.6 else max(0.0, 1 - (k - 0.6) / 0.4)
        if fade <= 0.02:
            return
        if pop <= 1.0:                                           # ombre portée : lisible sur un décor clair
            off = max(2, int(3 * self.s))
            hd.put(screen, hd.text(text, key, size, (0, 0, 0), glow=0), p.x + off, p.y + off, align, "middle",
                   alpha=0.75 * fade)
        hd.put(screen, hd.text(text, key, size, color, glow=0.6), p.x, p.y, align, "middle", scale=pop, alpha=fade)

    # ------------------------------------------------------------ effets prêts à l'emploi
    def _trail(self, p, now):
        rng = self.rng
        if p.kind == "rocket":
            q = self.add(Particle("puff", p.x - p.vx * 0.012, p.y - p.vy * 0.012, now, rng.uniform(0.5, 0.9), "back"))
            q.r0, q.r1 = 7 * self.s, rng.uniform(22, 34) * self.s
            q.a0, q.a1 = 150, 0
            q.col = (150, 140, 140)
            q.vy = -rng.uniform(5, 20) * self.s
            q.data = rng.randint(0, 2)
            g = self.add(Particle("glow", p.x, p.y, now, 0.12, "back"))
            g.r0, g.r1, g.col, g.a0, g.a1 = 10 * self.s, 16 * self.s, FIRE, 0.9, 0.0
        else:
            q = self.add(Particle("puff", p.x, p.y, now, 0.4, p.layer))
            q.r0, q.r1 = 3 * self.s, 9 * self.s
            q.a0, q.a1 = 70, 0
            q.col = (120, 115, 110)
            q.data = rng.randint(0, 2)

    def glow(self, x, y, r0, r1, color, life, layer="front", a0=1.0, a1=0.0, delay=0.0, hot=0.35):
        p = self.add(Particle("glow", x, y, self.now + delay, life, layer))
        p.r0, p.r1, p.col, p.a0, p.a1, p.data = r0 * self.s, r1 * self.s, color, a0, a1, hot
        return p

    def sparks(self, x, y, n, color=SPARK, speed=(300, 900), angle=(0, 360), life=(0.2, 0.6), gravity=900,
               layer="front", width=3, length=40):
        rng, s = self.rng, self.s
        for _ in range(n):
            a = math.radians(rng.uniform(*angle))
            v = rng.uniform(*speed) * s
            p = self.add(Particle("spark", x, y, self.now, rng.uniform(*life), layer))
            p.vx, p.vy = math.cos(a) * v, math.sin(a) * v
            p.ay = gravity * s
            p.drag = 2.0
            p.r0, p.r1 = width * s, length * s
            p.col = color
            p.a0, p.a1 = 1.0, 0.0

    def smoke(self, x, y, n, r=(14, 30), grow=2.6, life=(0.8, 1.6), rise=(20, 60), spread=40, color=SMOKE,
              alpha=170, layer="back", delay=0.0):
        rng, s = self.rng, self.s
        for _ in range(n):
            p = self.add(Particle("puff", x + rng.uniform(-spread, spread) * s, y + rng.uniform(-spread, spread) * 0.5 * s,
                                  self.now + delay + rng.uniform(0, 0.15), rng.uniform(*life), layer))
            r0 = rng.uniform(*r)
            p.r0, p.r1 = r0 * s, r0 * grow * s
            p.vx = rng.uniform(-25, 25) * s
            p.vy = -rng.uniform(*rise) * s
            p.drag = 0.6
            p.a0, p.a1 = alpha, 0
            p.col = color
            p.data = rng.randint(0, 2)

    def explosion(self, x, y, size=1.0, layer_back=True):
        """Grosse explosion : éclair, boule de feu, onde de choc, braises, fumée, débris, secousse."""
        rng, s, now = self.rng, self.s, self.now
        back = "back" if layer_back else "front"
        self.glow(x, y, 40 * size, 230 * size, (255, 130, 50), 0.5, "front", 0.75, 0.0, hot=0.2)
        self.glow(x, y, 20 * size, 90 * size, (255, 236, 190), 0.16, "front", 0.9, 0.0, hot=0.8)
        for i in range(7):                                       # boule de feu qui gonfle
            ang = rng.uniform(0, math.tau)
            d = rng.uniform(0, 45) * size
            self.glow(x + math.cos(ang) * d * s, y + math.sin(ang) * d * 0.7 * s, 30 * size, rng.uniform(70, 120) * size,
                      rng.choice((FIRE, FIRE_HOT, (255, 110, 40))), rng.uniform(0.45, 0.8), back, 1.0, 0.0, delay=i * 0.02)
        r = self.add(Particle("ring", x, y, now, 0.55, "front"))
        r.r0, r.r1, r.col, r.a0, r.a1, r.data = 20 * s * size, 330 * s * size, (255, 220, 160), 0.9, 0.0, 10 * s
        r = self.add(Particle("ring", x, y, now + 0.05, 0.7, "front"))
        r.r0, r.r1, r.col, r.a0, r.a1, r.data = 10 * s * size, 220 * s * size, (255, 140, 60), 0.6, 0.0, 6 * s
        self.sparks(x, y, int(34 * size), FIRE_HOT, (300, 1300), (190, 350), (0.4, 1.1), 1100, "front", 3, 46)
        self.sparks(x, y, int(16 * size), (255, 120, 40), (150, 600), (0, 360), (0.3, 0.8), 700, "front", 4, 30)
        for _ in range(int(9 * size)):                           # débris qui retombent
            a = math.radians(rng.uniform(200, 340))
            v = rng.uniform(350, 900) * s
            p = self.add(Particle("obj", x, y, now, rng.uniform(0.9, 1.5), "front"))
            p.name = "chunk%d" % rng.randint(0, 2)
            p.vx, p.vy = math.cos(a) * v, math.sin(a) * v
            p.ay = 1500 * s
            p.vrot = rng.uniform(-720, 720)
        self.smoke(x, y - 10 * s, int(10 * size), (26, 44), 2.4, (1.4, 2.6), (30, 90), 50 * size, SMOKE, 190, back, 0.12)
        self.smoke(x, y, int(5 * size), (20, 30), 2.0, (0.6, 1.0), (40, 120), 30 * size, (120, 70, 40), 140, back, 0.05)
        self.shake(13 * size, 0.55)
        self.flash((255, 170, 100), 0.13 * size, 0.16)

    def small_blast(self, x, y, size=1.0, layer="back"):
        self.glow(x, y, 16 * size, 90 * size, FIRE_HOT, 0.32, layer, 1.0, 0.0, hot=0.6)
        for _ in range(3):
            self.glow(x + self.rng.uniform(-14, 14) * self.s, y + self.rng.uniform(-10, 10) * self.s, 14 * size, 50 * size,
                      FIRE, self.rng.uniform(0.3, 0.5), layer)
        self.sparks(x, y, int(10 * size), FIRE_HOT, (200, 700), (180, 360), (0.25, 0.6), 900, layer, 2, 26)
        self.smoke(x, y, int(4 * size), (12, 20), 2.2, (0.7, 1.3), (20, 60), 18 * size, SMOKE, 150, layer)

    def text(self, text, x, y, color, size, key="stencil", life=1.1, rise=90, align="center", delay=0.0, layer="front"):
        p = self.add(Particle("text", x, y, self.now + delay, life, layer))
        p.vy = -rise * self.s
        p.drag = 1.6
        p.data = (text, key, int(size * self.s), color, align)
        return p

    def obj(self, name, x, y, vx, vy, gravity=1400, vrot=0.0, life=1.4, floor=None, bounce=0.35, layer="front", rot=0.0):
        p = self.add(Particle("obj", x, y, self.now, life, layer))
        p.name, p.vx, p.vy, p.ay, p.vrot, p.floor, p.bounce, p.rot = name, vx * self.s, vy * self.s, gravity * self.s, vrot, floor, bounce, rot
        return p

    def muzzle(self, x, y, direction, size=1.0, color=FIRE_HOT):
        rng = self.rng
        p = self.add(Particle("star", x + direction * 10 * size * self.s, y, self.now, 0.07, "front"))
        p.r0, p.r1 = 30 * size * self.s, 44 * size * self.s
        p.col, p.a0, p.a1, p.data = color, 1.0, 0.3, rng.randint(0, 3)
        self.glow(x + direction * 8 * self.s, y, 20 * size, 60 * size, color, 0.09, "front", 0.9, 0.0)

    def tracer(self, x, y, tx, ty, speed=2600, color=SPARK, width=4, length=120, layer="front", impact=True, life=None):
        d = math.hypot(tx - x, ty - y)
        v = speed * self.s
        t = life or max(0.05, d / v)
        p = self.add(Particle("tracer", x, y, self.now, t, layer))
        p.vx, p.vy = (tx - x) / t, (ty - y) / t
        p.r0, p.r1 = width * self.s, length * self.s
        p.col, p.a0, p.a1 = color, 1.0, 0.35
        if impact:
            p.on_end = (self._impact, (tx, ty))
        return p

    def _impact(self, x, y):
        self.glow(x, y, 6, 26, FIRE_HOT, 0.16, "back", 0.8, 0.0)
        self.sparks(x, y, 3, SPARK, (80, 260), (200, 340), (0.15, 0.3), 600, "back", 2, 12)

    def projectile(self, name, x0, y0, x1, y1, dur, arc, on_end, spin=540.0, kind="proj", trail=0.03, layer="front"):
        """Objet lancé en cloche de (x0, y0) à (x1, y1) en dur secondes, puis on_end(x1, y1)."""
        p = self.add(Particle(kind, x0, y0, self.now, dur, layer))
        p.name = name
        g = 2 * arc * self.s / (dur / 2) ** 2                  # hauteur de la cloche : arc pixels
        p.vx = (x1 - x0) / dur
        p.vy = (y1 - y0) / dur - g * dur / 2
        p.ay = g
        p.vrot = spin
        p.trail = trail
        p.on_end = (on_end, (x1, y1))
        return p
