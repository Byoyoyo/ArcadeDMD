"""The real look of a backdrop, drawn by the program with Pillow alone (1.39.3). A plane is drawn with its colours and,
beside them, what throws a shadow, where the wall is pierced, where it is stained, where it catches the light and where a
lamp burns. Passes of image then finish it: the stains and the grain of the plaster, soft shadows thrown by what sticks
out, the darkness of the hour and the pools of light of the lamps in it, the air between the planes, a grain of film.
No line is drawn round the shapes and no flat bright colour is laid.

Every picture is our own drawing. None comes from a game. The carved signs and the marks of the signboards are invented
and belong to no writing.

/ Le rendu réaliste d'un décor, dessiné par le programme avec Pillow seul. Un plan est dessiné avec ses couleurs et, à
côté, ce qui porte ombre, les percements, les salissures, les reflets et les lampes. Des passes d'image le finissent :
les taches et le grain de l'enduit, les ombres douces, l'obscurité de l'heure et les flaques de lumière des lampes,
l'air entre les plans, un grain de pellicule. Chaque image est notre dessin, aucune ne vient d'un jeu.
"""

import math

from PIL import Image, ImageChops, ImageDraw, ImageFilter

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


PLASTER = ((204, 180, 146), (190, 160, 124), (216, 198, 168), (178, 146, 112), (198, 172, 142), (224, 210, 186),
           (188, 152, 108), (170, 150, 128), (208, 176, 132))


WOOD = (98, 76, 56)


INSIDE = (24, 20, 22)


PAINT = ((88, 118, 118), (84, 98, 126), (122, 84, 64), (94, 114, 90), (136, 122, 96))


CLOTH = (((146, 58, 50), (208, 196, 172)), ((62, 86, 112), (202, 194, 174)), ((166, 128, 62), (210, 196, 166)),
         ((72, 100, 84), (204, 198, 176)), ((176, 168, 152), (122, 114, 102)))


BRICK = ((132, 78, 60), (120, 70, 56), (144, 90, 68), (112, 72, 62))


IRON = (48, 46, 48)


def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def grey3(m):
    return Image.merge("RGB", (m, m, m))


def amp(m, k):
    return m.point(lambda v: max(0, min(255, int(128 + (v - 128) * k))))


def relief(n, d=2, k=3.0):
    """A bumpy surface lit from the upper left. / Une surface bosselée éclairée d'en haut à gauche."""
    return ImageChops.subtract(n, ImageChops.offset(n, d, d), 1.0 / k, 128)


def lut(rgb, fr, fg, fb):
    return Image.merge("RGB", [ch.point(f) for ch, f in zip(rgb.split(), (fr, fg, fb))])


def grade_cine(rgb):
    g = rgb.convert("L")
    rgb = Image.blend(rgb, grey3(g), 0.10)
    s = lambda v: max(0, min(255, int(116 + (v - 116) * 1.24)))
    return lut(rgb, lambda v: min(255, int(s(v) * 1.04 + 3)), lambda v: int(s(v) * 0.97 + 1), lambda v: int(s(v) * 0.90 + 12))


def grade_tomb(rgb):
    s = lambda v: max(0, min(255, int(110 + (v - 110) * 1.22)))
    return lut(rgb, lambda v: min(255, int(s(v) * 1.05 + 2)), lambda v: int(s(v) * 0.96), lambda v: int(s(v) * 0.86 + 6))


MOODS = {}                               # the light of each place, by name / la lumière de chaque lieu


MOODS["cine"] = dict(sky=[(0.0, (12, 20, 52)), (0.13, (32, 40, 88)), (0.25, (98, 72, 104)), (0.35, (212, 118, 74)), (0.45, (252, 194, 110)), (0.60, (236, 160, 96)), (1.0, (92, 60, 54))],
                     sun=(0.47, 0.41), glare=(150, 86, 30), haze=(172, 106, 92), dust=(255, 190, 120), cast=(40, 8), soft=5.5,
                     shadow=(96, 84, 128), shadow_k=0.9, soot=(52, 44, 54), sunc=(255, 196, 128), rim=(255, 176, 96), lamps=0.4,
                     wall=(0.50, 0.42, 0.48), lampc=(255, 216, 164), pool_r=34, pool_k=1.7,
                     clouds=((255, 188, 128), (92, 80, 118), 0.92), grade=grade_cine, dim=1.0)


MOODS["tombe"] = dict(sky=[(0.0, (9, 6, 7)), (0.5, (22, 14, 11)), (1.0, (36, 22, 15))], sun=(0.5, 0.0), glare=(0, 0, 0), haze=(44, 26, 18),
                      dust=(255, 196, 130), cast=(10, 16), soft=4.0, shadow=(98, 82, 104), shadow_k=0.86, soot=(40, 30, 30),
                      sunc=(255, 216, 156), rim=None, lamps=0.0, wall=(0.30, 0.23, 0.21), lampc=(255, 214, 150), pool_r=46, pool_k=1.9,
                      clouds=None, grade=grade_tomb, dim=1.0)


class Sheet:
    """A plane being drawn: its colours, and beside them what throws a shadow, where the wall is pierced, where it is
    stained and where it catches the light. / Un plan en cours de dessin, avec ce qui porte ombre, les percements,
    les salissures et les reflets."""

    def __init__(self, tw, h, s):
        self.tw, self.h, self.s = tw, h, s
        self.im = Image.new("RGBA", (tw * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.m = {k: Image.new("L", (tw, h), 0) for k in ("cast", "hole", "dark", "light", "Dark", "Light", "lamp", "pool", "glowR", "glowC")}
        self.lamps = []
        self.md = {k: ImageDraw.Draw(v) for k, v in self.m.items()}

    def poly(self, pts, fill, mark=None, v=255):
        if fill is not None:
            self.d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill)
        if mark:
            self.md[mark].polygon(pts, fill=v)

    def rect(self, x0, y0, x1, y1, fill, mark=None, v=255):
        x0, x1, y0, y1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
        if fill is not None:
            self.d.rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=fill)
        if mark:
            self.md[mark].rectangle([x0, y0, x1, y1], fill=v)

    def ellipse(self, x0, y0, x1, y1, fill, mark=None, v=255):
        x0, x1, y0, y1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
        if fill is not None:
            self.d.ellipse([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=fill)
        if mark:
            self.md[mark].ellipse([x0, y0, x1, y1], fill=v)

    def line(self, pts, fill, width=1.0, mark=None):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=fill, width=max(1, int(round(width * SS))))
        if mark:
            self.md[mark].line(pts, fill=255, width=max(1, int(round(width))))

    def finish(self, rng, mood, depth=0.0, blur=0.0, tex=1.0, foot=0.0, bump_k=0.24):
        tw, h, s = self.tw, self.h, self.s
        c = lambda v: max(2, int(v * s))
        im = self.im.resize((tw, h), Image.LANCZOS)
        a = im.getchannel("A")
        rgb = im.convert("RGB")
        big = fractal(tw, h, rng, cells=(c(260), c(110), c(48), c(20)), contrast=1.2)
        streak = fractal(tw, max(4, h // 14), rng, cells=(c(40), c(14), c(6), c(3)), contrast=1.3).resize((tw, h), Image.BICUBIC)
        bump = relief(fractal(tw, h, rng, cells=(c(24), c(10), c(5), c(2)), contrast=1.2), max(1, int(1.6 * s)), 2.4)
        grain = fractal(tw, h, rng, cells=(4, 2, 1, 1), contrast=1.0)
        rgb = ImageChops.soft_light(rgb, grey3(ImageChops.add(amp(big, 0.60 * tex), amp(streak, 0.34 * tex), 1.0, -128)))
        rgb = ImageChops.overlay(rgb, grey3(amp(bump, bump_k * tex)))
        dx, dy = int(mood["cast"][0] * s), int(mood["cast"][1] * s)             # what sticks out throws a soft shadow
        sh = ImageChops.offset(self.m["cast"], dx, dy)
        ImageDraw.Draw(sh).rectangle([0, 0, tw, dy], fill=0)
        sh = ImageChops.subtract(sh.filter(ImageFilter.GaussianBlur(mood["soft"] * s)), self.m["cast"]).point(lambda v: int(v * mood["shadow_k"]))
        rgb = Image.composite(ImageChops.multiply(rgb, Image.new("RGB", rgb.size, mood["shadow"])), rgb, sh)
        ao = ImageChops.subtract(self.m["hole"].filter(ImageFilter.GaussianBlur(5 * s)), self.m["hole"]).point(lambda v: int(v * 0.55))
        rgb = Image.composite(ImageChops.multiply(rgb, Image.new("RGB", rgb.size, (150, 138, 140))), rgb, ao)
        for key, r, col, k in (("dark", 2.6, mood["shadow"], 0.9), ("Dark", 11, mood["soot"], 0.85)):
            m = self.m[key].filter(ImageFilter.GaussianBlur(r * s)).point(lambda v, k=k: int(v * k))
            rgb = Image.composite(ImageChops.multiply(rgb, Image.new("RGB", rgb.size, col)), rgb, m)
        for key, r, k in (("light", 2.6, 0.55), ("Light", 12, 0.40)):
            m = self.m[key].filter(ImageFilter.GaussianBlur(r * s)).point(lambda v, k=k: int(v * k))
            rgb = Image.composite(ImageChops.screen(rgb, Image.new("RGB", rgb.size, shade(mood["sunc"], 0.5))), rgb, m)
        g = Image.linear_gradient("L").resize((tw, h)).point(lambda v: 255 - int(v * 0.15))   # darker towards the ground
        rgb = ImageChops.multiply(rgb, grey3(g))
        pool = self.m["pool"]                                                  # the light of that hour, and the lamps in it
        if mood["wall"] != (1.0, 1.0, 1.0) or pool.getbbox():
            dark = ImageChops.multiply(rgb, Image.new("RGB", rgb.size, tuple(int(255 * k) for k in mood["wall"])))
            if pool.getbbox():
                pm = pool.filter(ImageFilter.GaussianBlur(mood.get("pool_r", 40) * s)).point(lambda v: min(255, int(v * mood.get("pool_k", 1.6))))
                rgb = Image.composite(ImageChops.multiply(rgb, Image.new("RGB", rgb.size, mood.get("lampc", (255, 216, 164)))), dark, pm)
            else:
                rgb = dark
        if mood["rim"] is not None:                                            # the low sun on the edges / le soleil rasant sur les arêtes
            edge = ImageChops.subtract(a, ImageChops.offset(a, int(4 * s) or 1, int(3 * s) or 1)).filter(ImageFilter.GaussianBlur(1.2 * s))
            rgb = Image.composite(ImageChops.screen(rgb, Image.new("RGB", rgb.size, mood["rim"])), rgb, edge.point(lambda v: int(v * 0.8)))
        lamp = self.m["lamp"].filter(ImageFilter.GaussianBlur(9 * s)).point(lambda v: int(v * 0.7))
        if lamp.getbbox():
            rgb = Image.composite(ImageChops.screen(rgb, Image.new("RGB", rgb.size, mood.get("lampglow", (255, 170, 84)))), rgb, lamp)
        for key, col in (("glowR", (255, 70, 56)), ("glowC", (70, 220, 255))):          # coloured lights / des lumières de couleur
            if self.m[key].getbbox():
                gm = self.m[key].filter(ImageFilter.GaussianBlur(8 * s)).point(lambda v: int(v * 0.8))
                rgb = Image.composite(ImageChops.screen(rgb, Image.new("RGB", rgb.size, col)), rgb, gm)
        if foot > 0:                                                           # dust at the foot / la poussière au pied
            f = Image.linear_gradient("L").resize((tw, h)).point(lambda v: max(0, int((v - 255 * (1 - 70 * s / h)) * (h / (70 * s)) * foot)))
            f = ImageChops.multiply(f, amp(big, 1.6).point(lambda v: min(255, v + 90)))
            rgb = Image.composite(Image.new("RGB", rgb.size, mood["dust"]), rgb, f)
        if depth > 0:
            rgb = Image.blend(rgb, Image.new("RGB", rgb.size, mood["haze"]), depth)
        if blur > 0:
            rgb = rgb.filter(ImageFilter.GaussianBlur(blur * s))
            a = a.filter(ImageFilter.GaussianBlur(blur * s * 0.7))
        rgb = ImageChops.overlay(rgb, grey3(amp(grain, 0.16)))                 # the grain of the film / le grain du film
        rgb = mood["grade"](rgb)
        rgb.putalpha(a)
        return rgb


# ---------------------------------------------------------------------------- the pieces shared by the places / les pièces communes aux lieux


def puff(img, shapes, col, blur, k=0.8):
    """Steam or smoke laid over a finished plane: soft heaps. / De la vapeur ou de la fumée posée sur un plan fini."""
    m = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(m)
    for x, y, r in shapes:
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * k))
    over = Image.new("RGBA", img.size, col + (0,))
    over.putalpha(m)
    img.alpha_composite(over)
    return img


def lantern(sh, x, y, s, pool=64):
    """A lamp that burns, and the pool of light around it. / Une lampe allumée et sa flaque de lumière."""
    sh.line([(x, y - 9 * s), (x, y - 4 * s)], (40, 34, 34), 1.0 * s)
    sh.rect(x - 3.4 * s, y - 4 * s, x + 3.4 * s, y + 5 * s, (48, 40, 38))
    sh.rect(x - 2.2 * s, y - 2.6 * s, x + 2.2 * s, y + 3.6 * s, (255, 228, 160))
    sh.ellipse(x - 5 * s, y - 5 * s, x + 5 * s, y + 6 * s, None, "lamp")
    sh.ellipse(x - pool * s, y - pool * 0.8 * s, x + pool * s, y + pool * 1.2 * s, None, "pool")
    sh.lamps.append((x, y))


def opening(sh, x, y, w, h, s, rng, wall, mood, arch=False, kind=None, soot=0.14, trim=None):
    """An opening sunk in the wall. Inside the air is dark; the right side and the sill catch the sun, the top and the
    left are in the shade. / Un percement en creux : le fond sombre, le côté droit et l'appui au soleil."""
    rv = 3.4 * s
    x0, x1, top = x - w / 2, x + w / 2, y - h
    if trim is not None:                                                                          # a painted surround / un entourage peint
        if arch:
            sh.ellipse(x0 - 5 * s, top - 5 * s, x1 + 5 * s, top + w + 5 * s, trim)
        sh.rect(x0 - 5 * s, top + (w / 2 if arch else -5 * s), x1 + 5 * s, y + 2 * s, trim)
    elif not arch:                                                                                # a lintel of wood / un linteau de bois
        sh.rect(x0 - 5 * s, top - 5 * s, x1 + 5 * s, top, shade(WOOD, 0.95), "cast")
    sh.rect(x0 - 3 * s, top - 3 * s, x1 + 3 * s, y + 2 * s, None, "hole")
    deep = shade(wall, 0.50)
    lit = rng.random() < mood["lamps"]
    inner = (255, 200, 126) if lit else INSIDE
    if arch:
        sh.ellipse(x0, top, x1, top + w, deep)
        sh.rect(x0, top + w / 2, x1, y, deep)
        sh.ellipse(x0 + rv, top + rv, x1 - rv * 0.4, top + w - rv * 0.2, inner)
        sh.rect(x0 + rv, top + w / 2, x1 - rv, y - rv * 0.8, inner)
        sh.rect(x1 - rv, top + w / 2, x1, y, shade(wall, 1.08))
    else:
        sh.rect(x0, top, x1, y, deep)
        sh.rect(x0 + rv, top + rv, x1 - rv, y - rv * 0.8, inner)
        sh.rect(x1 - rv, top + rv * 0.6, x1, y, shade(wall, 1.08))
    sh.rect(x0 + rv * 0.6, y - rv * 0.8, x1, y, shade(wall, 1.16))
    if lit:
        sh.rect(x0, top, x1, y, None, "lamp")
        sh.ellipse(x0 - 12 * s, top - 10 * s, x1 + 12 * s, y + 18 * s, None, "pool", 210)
    iy0 = top + (w / 2 if arch else rv)
    kind = kind or rng.choice(("bars", "shutter", "shutter", "cloth", "void", "board"))
    if kind == "bars" and not lit:
        n = max(2, int(w / (5 * s)))
        for i in range(1, n):
            sh.line([(x0 + rv + i * (w - 2 * rv) / n, iy0), (x0 + rv + i * (w - 2 * rv) / n, y - rv)], (58, 54, 56), 0.9 * s)
        sh.line([(x0 + rv, (iy0 + y) / 2), (x1 - rv, (iy0 + y) / 2)], (58, 54, 56), 0.9 * s)
    elif kind == "shutter":
        col = rng.choice(PAINT)
        half = rng.random() < 0.5
        xs = [(x0 + rv, x0 + w * (0.5 if half else 0.36))] + ([] if half else [(x1 - w * 0.36, x1 - rv)])
        for a0, a1 in xs:
            sh.rect(a0, iy0, a1, y - rv * 0.8, col, "cast")
            for j in range(1, 7):
                yy = iy0 + (y - rv - iy0) * j / 7
                sh.line([(a0, yy), (a1, yy)], shade(col, 0.72), 0.8 * s)
            sh.line([(a1, iy0), (a1, y - rv)], shade(col, 0.55), 1.0 * s)
    elif kind == "cloth" and not lit:
        col = rng.choice(CLOTH)[0]
        sh.poly([(x0 + rv, iy0), (x1 - rv, iy0), (x1 - rv - w * 0.2, y - rv), (x0 + rv, y - rv)], shade(col, 0.8))
        for i in range(1, 4):
            xx = x0 + rv + i * (w - 2 * rv) / 4
            sh.line([(xx, iy0), (xx - w * 0.05 * i, y - rv)], shade(col, 0.6), 1.0 * s)
    elif kind == "board":
        for j in range(3):
            yy = iy0 + (y - rv - iy0) * (0.2 + j * 0.3)
            sh.poly([(x0 - 2 * s, yy + rng.uniform(-3, 3) * s), (x1 + 2 * s, yy + rng.uniform(-3, 3) * s), (x1 + 2 * s, yy + 6 * s), (x0 - 2 * s, yy + 6 * s)],
                    shade(WOOD, rng.uniform(1.0, 1.5)), "cast")
    sh.rect(x0 - 4 * s, y, x1 + 4 * s, y + 3.5 * s, shade(wall, 1.14), "cast")                    # the sill / l'appui
    sh.poly([(x0, y + 4 * s), (x1, y + 4 * s), (x1 - w * 0.2, y + rng.uniform(26, 54) * s), (x0 + w * 0.3, y + rng.uniform(20, 40) * s)], None, "Dark", 80)
    if rng.random() < soot:                                                                       # it burnt in there / ça a brûlé
        sh.ellipse(x0 - 6 * s, top - rng.uniform(34, 70) * s, x1 + 8 * s, top + h * 0.3, None, "Dark", 190)


def door(sh, x, base, w, h, s, rng, wall, mood, arch=True):
    rv = 4 * s
    x0, x1, top = x - w / 2, x + w / 2, base - h
    sh.rect(x0 - 3 * s, top - 3 * s, x1 + 3 * s, base, None, "hole")
    deep = shade(wall, 0.5)
    if arch:
        sh.ellipse(x0, top, x1, top + w, deep)
        sh.rect(x0, top + w / 2, x1, base, deep)
        sh.ellipse(x0 + rv, top + rv, x1 - rv * 0.4, top + w - rv * 0.2, INSIDE)
        sh.rect(x0 + rv, top + w / 2, x1 - rv, base, INSIDE)
        y0 = top + w / 2
    else:
        sh.rect(x0, top, x1, base, deep)
        sh.rect(x0 + rv, top + rv, x1 - rv, base, INSIDE)
        y0 = top + rv
    sh.rect(x1 - rv, y0, x1, base, shade(wall, 1.08))
    lw = (w - 2 * rv) * rng.choice((0.5, 0.5, 1.0, 0.72))                                        # the leaf, more or less open
    col = rng.choice((WOOD, shade(WOOD, 1.2), (86, 96, 100), (104, 84, 70)))
    n = max(2, int(lw / (7 * s)))
    for i in range(n):
        pc = shade(col, rng.uniform(0.86, 1.14))
        sh.rect(x0 + rv + i * lw / n, y0, x0 + rv + (i + 1) * lw / n - 0.8 * s, base, pc)
    for k in (0.2, 0.78):
        sh.rect(x0 + rv, y0 + (base - y0) * k, x0 + rv + lw, y0 + (base - y0) * k + 3 * s, shade(col, 0.6))
    sh.rect(x0 - 6 * s, base - 5 * s, x1 + 6 * s, base + 1, mix(wall, (200, 196, 188), 0.5), "cast")   # the step / la marche
    if mood["lamps"] > 0 and rng.random() < 0.45:
        lantern(sh, x1 + 12 * s, top + 4 * s, s, 54)
    if rng.random() < 0.12:
        sh.ellipse(x0 - 6 * s, top - rng.uniform(40, 80) * s, x1 + 8 * s, top + h * 0.3, None, "Dark", 190)


def awning(sh, x0, x1, y0, s, rng, base):
    a, b = rng.choice(CLOTH)
    drop, out = rng.uniform(24, 32) * s, 12 * s
    n = max(4, int((x1 - x0) / (13 * s)))
    sag = [rng.uniform(0, 4) * s for _ in range(n + 1)]
    for i in range(n):
        xa, xb = x0 + i * (x1 - x0) / n, x0 + (i + 1) * (x1 - x0) / n
        ka, kb = 2 * i / n - 1, 2 * (i + 1) / n - 1
        col = shade(a if i % 2 == 0 else b, rng.uniform(0.92, 1.06))
        sh.poly([(xa, y0), (xb, y0), (xb + out * kb, y0 + drop + sag[i + 1]), (xa + out * ka, y0 + drop + sag[i])], col, "cast")
        sh.poly([(xa + out * ka, y0 + drop + sag[i]), (xb + out * kb, y0 + drop + sag[i + 1]), (xb + out * kb, y0 + drop + sag[i + 1] + 6 * s),
                 (xa + out * ka, y0 + drop + sag[i] + 6 * s)], shade(col, 0.74))
        if i % 2:
            sh.poly([(xa, y0), (xa + 3 * s, y0), (xa + out * ka + 3 * s, y0 + drop), (xa + out * ka, y0 + drop)], None, "dark", 110)   # a fold
    sh.poly([(x0, y0), (x1, y0), (x1 + out, y0 + drop * 0.6), (x0 - out, y0 + drop * 0.6)], None, "light", 70)
    sh.poly([(x0 - out, y0 + drop + 8 * s), (x1 + out, y0 + drop + 8 * s), (x1 + out + 18 * s, min(base, y0 + drop + 52 * s)),
             (x0 - out + 22 * s, min(base, y0 + drop + 52 * s))], None, "dark", 190)                # its shade on the wall
    for px in (x0 - out + 2 * s, x1 + out - 2 * s):
        sh.line([(px, y0 + drop), (px, base)], shade(WOOD, 0.9), 1.6 * s, "cast")


def stall(sh, x, base, w, s, rng, wall, mood):
    h, rv = 58 * s, 3.4 * s
    sh.rect(x - 3 * s, base - h - 3 * s, x + w + 3 * s, base, None, "hole")
    sh.rect(x, base - h, x + w, base, shade(wall, 0.5))
    sh.rect(x + rv, base - h + rv, x + w - rv, base, INSIDE)
    sh.rect(x + w - rv, base - h + rv * 0.6, x + w, base, shade(wall, 1.08))
    sh.line([(x + rv, base - 40 * s), (x + w - rv, base - 40 * s)], shade(WOOD, 0.8), 1.4 * s)
    for row in (40, 20):
        gx = x + 10 * s
        while gx < x + w - 8 * s:
            col = rng.choice(((150, 92, 56), (176, 150, 92), (104, 118, 78), (150, 70, 58), (190, 180, 156), (72, 96, 116)))
            r = rng.uniform(4.0, 6.0) * s
            sh.ellipse(gx - r, base - row * s - r * 2.1, gx + r, base - row * s, shade(col, 0.62))
            sh.ellipse(gx - r * 0.7, base - row * s - r * 1.8, gx + r * 0.2, base - row * s - r * 0.6, None, "light", 120)
            gx += rng.uniform(13, 19) * s
    sh.rect(x - 4 * s, base - 20 * s, x + w + 4 * s, base + 1, shade(WOOD, 1.1), "cast")           # the counter / le comptoir
    sh.rect(x - 4 * s, base - 20 * s, x + w + 4 * s, base - 17 * s, shade(WOOD, 1.5))
    i = 1
    while x + i * 13 * s < x + w:
        sh.line([(x + i * 13 * s, base - 17 * s), (x + i * 13 * s, base)], shade(WOOD, 0.7), 0.9 * s)
        i += 1
    awning(sh, x - 6 * s, x + w + 6 * s, base - h - 16 * s, s, rng, base)
    if mood["lamps"] > 0 and rng.random() < 0.8:
        lantern(sh, x + w * rng.uniform(0.3, 0.7), base - h + 9 * s, s)


def balcony(sh, x, y, s, rng, wall, mood):
    w = rng.uniform(52, 66) * s
    opening(sh, x, y, 20 * s, 42 * s, s, rng, wall, mood, arch=True, kind="void", soot=0.05)
    sh.rect(x - w / 2, y, x + w / 2, y + 6 * s, shade(wall, 0.92), "cast")
    sh.rect(x - w / 2, y, x + w / 2, y + 2 * s, shade(wall, 1.16))
    for bx in (x - w / 2 + 7 * s, x + w / 2 - 7 * s):
        sh.poly([(bx - 2 * s, y + 6 * s), (bx + 2 * s, y + 6 * s), (bx + 2 * s, y + 18 * s)], shade(wall, 0.7))
    px = x - w / 2 + 3 * s
    while px < x + w / 2:
        sh.line([(px, y - 18 * s), (px, y)], (60, 54, 54), 1.2 * s)
        px += 6 * s
    sh.rect(x - w / 2, y - 20 * s, x + w / 2, y - 17.5 * s, (70, 62, 60), "cast")
    if rng.random() < 0.7:                                                                         # something drying / du linge
        a, b = rng.choice(CLOTH)
        cx = x - w / 2 + rng.uniform(4, 24) * s
        sh.rect(cx, y - 19 * s, cx + 20 * s, y + 20 * s, a, "cast")
        for k in (0.2, 0.5, 0.8):
            sh.rect(cx, y - 19 * s + 39 * s * k, cx + 20 * s, y - 19 * s + 39 * s * k + 3 * s, b)
        sh.rect(cx + 14 * s, y - 19 * s, cx + 20 * s, y + 20 * s, None, "dark", 120)
    sh.poly([(x - w / 2, y + 7 * s), (x + w / 2, y + 7 * s), (x + w / 2 + 14 * s, y + 34 * s), (x - w / 2 + 18 * s, y + 34 * s)], None, "dark", 170)


def bricks(sh, x, y, w, h, s, rng):
    """Where the plaster fell. / Là où l'enduit est tombé."""
    bw, bh = 12 * s, 6 * s
    for j in range(int(h / bh)):
        for i in range(int(w / bw) + 1):
            bx, by = x + (i - (j % 2) * 0.5) * bw, y + j * bh
            dx, dy = (bx + bw / 2 - (x + w / 2)) / (w / 2), (by + bh / 2 - (y + h / 2)) / (h / 2)
            if dx * dx + dy * dy < rng.uniform(0.5, 1.05):
                sh.rect(bx - 1.2 * s, by - 1.2 * s, bx + bw, by + bh, (96, 80, 70))
                sh.rect(bx, by, bx + bw - 1.3 * s, by + bh - 1.3 * s, shade((156, 100, 74), rng.uniform(0.8, 1.12)))
    sh.ellipse(x - 4 * s, y - 4 * s, x + w + 4 * s, y + h + 4 * s, None, "hole", 90)


def dome(sh, x, y, w, s, wall):
    hg = w * 0.52
    sh.d.chord([(x - w / 2) * SS, (y - hg) * SS, (x + w / 2) * SS, (y + hg) * SS], 180, 360, fill=wall)
    sh.md["dark"].chord([x + w * 0.10, y - hg, x + w / 2, y + hg], 180, 360, fill=200)
    sh.md["light"].ellipse([x - w * 0.36, y - hg * 0.86, x - w * 0.04, y - hg * 0.3], fill=170)
    sh.md["cast"].chord([x - w / 2, y - hg, x + w / 2, y + hg], 180, 360, fill=255)
    sh.rect(x - w / 2 - 3 * s, y - 4 * s, x + w / 2 + 3 * s, y + 1, shade(wall, 1.06), "cast")
    sh.line([(x, y - hg), (x, y - hg - 12 * s)], (70, 62, 58), 1.4 * s)


def pole(sh, x, base, h, s):
    sh.line([(x, base), (x, base - h)], (74, 62, 52), 3.4 * s, "cast")
    sh.line([(x + 1.2 * s, base), (x + 1.2 * s, base - h)], (50, 42, 38), 1.0 * s)
    sh.line([(x - 16 * s, base - h + 12 * s), (x + 16 * s, base - h + 12 * s)], (70, 58, 50), 2.4 * s, "cast")
    for dx in (-14, -5, 5, 14):
        sh.rect(x + dx * s - 1 * s, base - h + 7 * s, x + dx * s + 1 * s, base - h + 12 * s, (150, 150, 144))


def wires(sh, poles, base, h, s, tw):
    ps = poles + [poles[0] + tw]
    for a, b in zip(ps, ps[1:]):
        for dx, sag in ((-14, 26), (-5, 30), (5, 28), (14, 24)):
            pts = []
            for i in range(25):
                t = i / 24
                pts.append((a + dx * s + (b - a) * t, base - h + 7 * s + sag * s * 4 * t * (1 - t)))
            for off in (0, -tw):
                sh.line([(px + off, py) for px, py in pts], (44, 40, 42), 0.6 * s)


def mountains(tw, h, rng, s, mood, col, depth, y, f, rough=1.0):
    """A range of bare rock, its gullies in the shade. / Une chaîne de roche nue, ses ravines à l'ombre."""
    c = lambda v: max(2, int(v * s))
    line = fractal(tw, 2, rng, cells=(c(520), c(210), c(90), c(34)), contrast=1.5).filter(ImageFilter.GaussianBlur(1.2))
    row = list(line.crop((0, 0, tw, 1)).getdata())
    mask = Image.new("L", (tw, h), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(0, h)] + [(x, h * 0.46 + (row[x] - 128) / 128 * h * 0.5 * rough) for x in range(0, tw, 2)] + [(tw, h)], fill=255)
    rock = fractal(tw, h, rng, cells=(c(150), c(60), c(22), c(8)), contrast=1.4)
    gully = fractal(max(8, tw // 3), h, rng, cells=(c(30), c(12), c(5), c(2)), contrast=1.4).resize((tw, h), Image.BICUBIC)
    lightmap = ImageChops.add(amp(relief(rock, max(2, int(3 * s)), 3.2), 0.9), amp(relief(gully, max(1, int(2 * s)), 2.0), 0.5), 1.0, -128)
    rgb = Image.new("RGB", (tw, h), tuple(int(v * k) for v, k in zip(col, mood["wall"])))
    rgb = ImageChops.overlay(rgb, grey3(lightmap))
    rgb = ImageChops.soft_light(rgb, grey3(amp(rock, 0.6)))
    g = Image.linear_gradient("L").resize((tw, h)).point(lambda v: 255 - int(v * 0.18))
    rgb = ImageChops.multiply(rgb, grey3(g))
    rgb = Image.blend(rgb, Image.new("RGB", rgb.size, mood["haze"]), depth)
    rgb = mood["grade"](rgb.filter(ImageFilter.GaussianBlur(0.6 * s)))
    rgb.putalpha(mask.filter(ImageFilter.GaussianBlur(0.7 * s)))
    return {"img": rgb, "y": y, "f": f, "stage": "sky"}


def wheel(sh, cx, ry, r, s, spokes=8):
    sh.ellipse(cx - r, ry - 2 * r, cx + r, ry, (40, 36, 36), "cast")
    sh.ellipse(cx - r * 0.8, ry - r * 1.8, cx + r * 0.8, ry - r * 0.2, (74, 54, 48))
    for i in range(spokes):
        a = math.pi * i / spokes
        sh.line([(cx - math.cos(a) * r * 0.8, ry - r - math.sin(a) * r * 0.8), (cx + math.cos(a) * r * 0.8, ry - r + math.sin(a) * r * 0.8)], (40, 36, 36), 1.6 * s)
    sh.ellipse(cx - r * 0.24, ry - r * 1.24, cx + r * 0.24, ry - r * 0.76, (96, 88, 82))
    sh.ellipse(cx - r * 0.9, ry - r * 1.95, cx + r * 0.1, ry - r * 1.2, None, "light", 70)


def rivets(sh, x0, x1, y, s, step=9):
    x = x0
    while x < x1:
        sh.ellipse(x - 0.9 * s, y - 0.9 * s, x + 0.9 * s, y + 0.9 * s, (40, 40, 40))
        x += step * s
