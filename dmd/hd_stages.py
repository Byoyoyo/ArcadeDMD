"""More HD backdrops, each with its own animations.

Fighting games (with a crowd in front): city at night, temple at dusk, harbor at sunset, ruins at night, and the
desert, jungle and snow backdrops with a crowd. Metal Slug: city at war, harbor, enemy base. Everything is drawn
by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this module is imported.

Décors supplémentaires de l'écran HD, chacun avec ses animations.

Pour les jeux de combat (avec du public devant) : ville la nuit (néons, métro aérien, vapeur),
temple au crépuscule (lanternes qui se balancent, pétales qui tombent), port au soleil couchant
(reflets sur l'eau, phare, mouettes), ruines la nuit (torches, braises, lucioles), et les décors
désert, jungle et neige repris avec du public.
Pour les Metal Slug : ville en guerre (incendies, fumée), port, base ennemie (gyrophares, cheminées, alerte).

Tout est dessiné par le programme (formes simples, dégradés), aucune image tirée d'un jeu.
Les décors s'enregistrent dans hd_bg.BUILDERS à l'import de ce module.
"""

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from . import hd_bg
from .hd_bg import Sil, add_at, crowd_layers, paint, periodic, radial, ruin, sandbags, vgrad, watchtower, wire_posts

NEON = ((255, 60, 200), (60, 230, 255), (255, 220, 60), (90, 255, 150), (255, 110, 60))


def stars_on(sky, rng, n, y_max, W):
    d = ImageDraw.Draw(sky)
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, y_max)
        b = int(rng.uniform(50, 200) * (1 - y / (y_max * 1.15)))
        if b > 15:
            d.point((x, y), fill=(b, b, min(255, b + 25)))
            if rng.random() < 0.15:
                out.append((x, y, rng.uniform(1.2, 3.0), rng.uniform(0, math.tau)))
    return out


def moon(sky, x, y, r, s, color=(232, 236, 220), glow=(40, 50, 70)):
    add_at(sky, radial(int(r * 9 * s), glow, 2.0), x, y)
    disk = Image.new("L", (int(2 * r * s) + 4, int(2 * r * s) + 4), 0)
    ImageDraw.Draw(disk).ellipse([2, 2, disk.width - 3, disk.height - 3], fill=255)
    disk = disk.filter(ImageFilter.GaussianBlur(1.2 * s))
    sky.paste(color, (int(x - disk.width / 2), int(y - disk.height / 2)), disk)


def windows_on(img, rects, s, rng, p=0.35, colors=((255, 214, 140), (255, 236, 190), (170, 210, 255))):
    """Fenêtres allumées sur des façades (dessinées une fois dans l'image du plan)."""
    d = ImageDraw.Draw(img)
    for (x, top, w, h) in rects:
        cols = max(1, int(w / (11 * s)))
        rows = max(1, int(h / (15 * s)))
        for i in range(cols):
            for j in range(rows):
                if rng.random() > p:
                    continue
                wx = x + (i + 0.5) * w / cols
                wy = top + 8 * s + j * 15 * s
                if wy > top + h - 8 * s:
                    continue
                c = rng.choice(colors)
                k = rng.uniform(0.5, 1.0)
                c = tuple(int(v * k) for v in c)
                d.rectangle([wx - 2.5 * s, wy - 3.5 * s, wx + 2.5 * s, wy + 3.5 * s], fill=c + (255,))


def skyline(c, tw, base, s, rng, hmin, hmax, wmin, wmax, broken=False):
    x, out, tops = -20 * s, [], []
    while x < tw:
        w, h = rng.uniform(wmin, wmax) * s, rng.uniform(hmin, hmax) * s
        top = base - h
        if broken and rng.random() < 0.6:
            pts = [(x, base), (x, top + rng.uniform(0, 20) * s)]
            for k in range(1, 5):
                pts.append((x + w * k / 5, top + rng.uniform(0, h * 0.35)))
            pts += [(x + w, top + rng.uniform(0, 30) * s), (x + w, base)]
            c.poly(pts)
        else:
            c.rect(x, top, x + w, base)
            r = rng.random()
            if r < 0.3:
                c.rect(x + w * 0.18, top - h * 0.07, x + w * 0.82, top)
            elif r < 0.45 and h > 150 * s:
                c.rect(x + w * 0.46, top - h * 0.22, x + w * 0.54, top)
                tops.append((x + w * 0.5, top - h * 0.22))
            elif r < 0.55:
                c.poly([(x, top), (x + w / 2, top - w * 0.45), (x + w, top)])
        out.append((x, top, w, h))
        x += w + rng.uniform(0, 14) * s
    return out, tops


def flame_points(n, rng, x0, x1, y):
    return [(rng.uniform(x0, x1), y) for _ in range(n)]


# ---------------------------------------------------------------------------- crochets d'ambiance
def _rot(b, key, angle, steps=16):
    cache = b.setdefault("_rot", {})
    a = int(round(angle / (360.0 / steps))) % steps
    k = (key, a)
    s = cache.get(k)
    if s is None:
        import pygame
        s = cache[k] = pygame.transform.rotozoom(b["imgs"][key], a * 360.0 / steps, 1.0)
    return s


def hook_neons(bd, screen, b, L, now, dt):
    """Néons des façades : allumés, avec de petits sauts de courant de temps en temps."""
    add = bd.pg.BLEND_RGB_ADD
    x0 = bd._layer_x(L, b["tw"])
    for i, (key, x, y, ph) in enumerate(L.get("neons", ())):
        flick = math.sin(now * 23 + ph * 7) + math.sin(now * 7.3 + ph * 3)
        if flick > 1.75:
            continue                                                # courte coupure
        img = b["imgs"][key if flick > -1.2 else key + "_dim"]
        screen.blit(img, (int(x0 + x - img.get_width() / 2), int(L["y"] + y - img.get_height() / 2)), special_flags=add)


def hook_train(bd, screen, b, L, now, dt):
    """Métro aérien qui passe de temps en temps."""
    st = bd.amb_state.setdefault("_train", {"t": now + 3.0, "x": None, "d": 1})
    img = b["imgs"]["train"]
    if st["x"] is None:
        if now < st["t"]:
            return
        st["d"] = -st["d"]
        st["x"] = -img.get_width() if st["d"] > 0 else bd.W
    st["x"] += st["d"] * 520 * bd.s * dt
    y = L["y"] + b["amb"]["train_y"] - img.get_height()
    im = img if st["d"] > 0 else _flip(b, "train")
    screen.blit(im, (int(st["x"]), int(y)))
    if st["x"] > bd.W + 10 or st["x"] < -img.get_width() - 10:
        st["x"] = None
        st["t"] = now + bd.rng.uniform(9, 15)


def _flip(b, key):
    cache = b.setdefault("_flip", {})
    s = cache.get(key)
    if s is None:
        import pygame
        s = cache[key] = pygame.transform.flip(b["imgs"][key], True, False)
    return s


def hook_steam(bd, screen, b, L, now, dt):
    """Vapeur qui sort des bouches d'égout."""
    for (x, y) in L.get("vents", ()):
        if bd.rng.random() < dt * 5:
            bd.fx.smoke(x, L["y"] + y, 1, (8, 14), 3.2, (1.4, 2.4), (25, 50), 6, (150, 150, 170), 70, "mid")


def hook_lanterns(bd, screen, b, L, now, dt):
    """Lanternes de papier qui se balancent sur leur corde."""
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    lamp = b["imgs"]["lantern"]
    x0 = bd._layer_x(L, b["tw"])
    for i, (x, y, rope, ph) in enumerate(L.get("lanterns", ())):
        a = math.sin(now * 1.4 + ph) * 0.16 + math.sin(now * 0.6 + ph * 2) * 0.05
        lx = x0 + x + math.sin(a) * rope
        ly = L["y"] + y + math.cos(a) * rope
        bd.pg.draw.line(screen, (30, 20, 30), (int(x0 + x), int(L["y"] + y)), (int(lx), int(ly)), max(1, int(bd.s * 1.5)))
        screen.blit(lamp, (int(lx - lamp.get_width() / 2), int(ly)))
        lv = 7 + 2 * math.sin(now * 3 + i)
        g = sp.glow(30 * bd.s, (255, 150, 60), lv, hot=0.2)
        screen.blit(g, (int(lx - g.get_width() / 2), int(ly + lamp.get_height() / 2 - g.get_height() / 2)), special_flags=add)


def hook_petals(bd, screen, b, L, now, dt):
    """Pétales de cerisier qui tombent en tourbillonnant."""
    st = bd.amb_state.setdefault("_petals", None)
    W, H, s = bd.W, bd.H, bd.s
    if st is None:
        st = bd.amb_state["_petals"] = [[bd.rng.uniform(0, W), bd.rng.uniform(-H, H), bd.rng.uniform(0.5, 1.0),
                                         bd.rng.uniform(0, 6), bd.rng.uniform(0, 360)] for _ in range(70)]
    for p in st:
        p[0] += (-30 - 40 * p[2] + math.sin(now * 1.2 + p[3]) * 30) * s * dt
        p[1] += (40 + 50 * p[2]) * s * dt
        p[4] += (120 + 200 * p[2]) * dt
        if p[1] > H + 10 or p[0] < -20:
            p[0], p[1] = bd.rng.uniform(0, W + 200 * s), -10
        img = _rot(b, "petal", p[4])
        screen.blit(img, (int(p[0]), int(p[1])))


def hook_glints(bd, screen, b, L, now, dt):
    """Reflets du soleil qui scintillent sur l'eau."""
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    amb = b["amb"]
    hz, sx = amb["horizon"], amb["sun_x"]
    slot = int(now * 10)
    for i in range(46):
        r = random.Random(slot * 131 + i)
        if i < 30:                                                    # colonne de reflet sous le soleil
            depth = r.uniform(0, 1) ** 1.6
            x = sx + r.uniform(-1, 1) * (30 + 220 * depth) * bd.s
        else:
            depth = r.uniform(0, 1)
            x = r.uniform(0, bd.W)
        y = hz + 4 * bd.s + depth * (bd.H - hz)
        lv = r.uniform(3, 10) if i < 30 else r.uniform(2, 5)
        g = sp.glow((3 + 4 * depth) * bd.s, (255, 220, 170), lv, hot=0.9)
        screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=add)


def hook_lighthouse(bd, screen, b, L, now, dt):
    sp = bd.fx.sp
    lx, ly = L["lamp"]
    x = bd._layer_x(L, b["tw"]) + lx
    y = L["y"] + ly
    a = now * 0.9
    facing = math.cos(a)                                           # faisceau vers la gauche ou la droite
    ang = 180 if facing < 0 else 0
    lv = 2 + 7 * abs(facing) ** 2
    ln = int((260 + 260 * abs(facing)) * bd.s)
    g = sp.beam(ln, int(70 * bd.s), (255, 240, 200), ang, lv)
    cx = x + math.cos(math.radians(ang)) * ln / 2
    screen.blit(g, (int(cx - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=bd.pg.BLEND_RGB_ADD)
    h = sp.glow(18 * bd.s, (255, 240, 200), 6 + 5 * abs(facing), hot=0.9)
    screen.blit(h, (int(x - h.get_width() / 2), int(y - h.get_height() / 2)), special_flags=bd.pg.BLEND_RGB_ADD)


def hook_gulls(bd, screen, b, L, now, dt):
    """Mouettes qui planent et battent des ailes."""
    st = bd.amb_state.setdefault("_gulls", None)
    W, s = bd.W, bd.s
    if st is None:
        st = bd.amb_state["_gulls"] = [[bd.rng.uniform(0, W), bd.rng.uniform(60, 200) * s, bd.rng.uniform(0.6, 1.0),
                                        bd.rng.uniform(0, 6)] for _ in range(6)]
    for g in st:
        g[0] += (35 + 30 * g[2]) * s * dt
        if g[0] > W + 40 * s:
            g[0], g[1] = -40 * s, bd.rng.uniform(60, 200) * s
        flap = math.sin(now * 7 * g[2] + g[3])
        img = b["imgs"]["gull_up" if flap > 0.2 else "gull_down"]
        y = g[1] + math.sin(now * 0.8 + g[3]) * 10 * s
        screen.blit(img, (int(g[0]), int(y)))


def hook_torches(bd, screen, b, L, now, dt):
    """Torches : flammes qui dansent, lueur, braises qui montent."""
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    x0 = bd._layer_x(L, b["tw"])
    for i, (x, y) in enumerate(L.get("torches", ())):
        tx, ty = x0 + x, L["y"] + y
        f1 = math.sin(now * 13 + i * 1.7) + math.sin(now * 21 + i)
        for j, (dy, r, col, lv) in enumerate(((0, 34, (255, 110, 30), 6), (-6, 16, (255, 170, 60), 10),
                                                (-14 - f1 * 2, 9, (255, 230, 150), 11))):
            g = sp.glow((r + f1 * 2) * bd.s, col, lv + f1, hot=0.4)
            screen.blit(g, (int(tx - g.get_width() / 2 + (f1 if j == 2 else 0)), int(ty + dy * bd.s - g.get_height() / 2)),
                        special_flags=add)
        if bd.rng.random() < dt * 3:
            p = bd.fx.glow(tx, ty - 10 * bd.s, 2, 4, (255, 160, 60), bd.rng.uniform(0.8, 1.6), "near", 1.0, 0.0, hot=0.9)
            p.vx, p.vy = bd.rng.uniform(-15, 15) * bd.s, -bd.rng.uniform(40, 80) * bd.s


def hook_fires(bd, screen, b, L, now, dt):
    """Incendies dans les ruines : flammes, lueur sur les murs, colonnes de fumée."""
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    x0 = bd._layer_x(L, b["tw"])
    for i, (x, y) in enumerate(L.get("fires", ())):
        for dx in (0, b["tw"]):
            fx_ = x0 + x + dx
            if not (-80 < fx_ < bd.W + 80):
                continue
            fy = L["y"] + y
            f1 = math.sin(now * 11 + i * 2.3) + math.sin(now * 17 + i)
            g = sp.glow((60 + 6 * f1) * bd.s, (255, 90, 20), 7 + f1, hot=0.2)
            screen.blit(g, (int(fx_ - g.get_width() / 2), int(fy - g.get_height() / 2)), special_flags=add)
            g = sp.glow((22 + 4 * f1) * bd.s, (255, 190, 80), 10, hot=0.6)
            screen.blit(g, (int(fx_ - g.get_width() / 2 + f1 * 2), int(fy - 6 * bd.s - g.get_height() / 2)), special_flags=add)
            if bd.rng.random() < dt * 2.5:
                bd.fx.smoke(fx_, fy - 20 * bd.s, 1, (12, 20), 3.5, (2.5, 4.0), (25, 45), 10, (40, 30, 34), 150, "mid")


def hook_stacks(bd, screen, b, L, now, dt):
    x0 = bd._layer_x(L, b["tw"])
    for (x, y) in L.get("stacks", ()):
        if bd.rng.random() < dt * 3:
            bd.fx.smoke(x0 + x, L["y"] + y, 1, (10, 16), 3.0, (2.5, 4.0), (20, 40), 4, (90, 90, 100), 120, "mid")


def hook_beacons(bd, screen, b, L, now, dt):
    """Gyrophares rouges qui tournent, et alerte de temps en temps."""
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    x0 = bd._layer_x(L, b["tw"])
    for i, (x, y) in enumerate(L.get("beacons", ())):
        k = max(0.0, math.cos(now * 5 + i * 1.3))
        if k < 0.05:
            continue
        g = sp.glow(40 * bd.s, (255, 40, 30), 2 + 9 * k, hot=0.6)
        screen.blit(g, (int(x0 + x - g.get_width() / 2), int(L["y"] + y - g.get_height() / 2)), special_flags=add)
    st = bd.amb_state.setdefault("_alarm", {"t": now + 6.0})
    if now >= st["t"]:
        st["t"] = now + bd.rng.uniform(9, 15)
        for j in range(3):
            bd.fx.later(j * 0.5, bd.fx.flash, (120, 0, 0), 0.35, 0.3)


# ---------------------------------------------------------------------------- petits dessins (Pillow)
def _img(w, h, fn, ss=4):
    big = Image.new("RGBA", (int(w * ss), int(h * ss)), (0, 0, 0, 0))
    fn(ImageDraw.Draw(big), big.width, big.height)
    return big.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS)


def neon_img(w, h, color, level, s, kind):
    """Enseigne au néon (RGB, à ajouter à l'image) : contour lumineux et barres de « texte »."""
    pad = int(14 * s)
    W, H = int(w + 2 * pad), int(h + 2 * pad)
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    lw = max(2, int(2.5 * s))
    if kind == 0:
        d.rounded_rectangle([pad, pad, W - pad, H - pad], radius=int(6 * s), outline=255, width=lw)
        x = pad + 8 * s
        while x < W - pad - 12 * s:
            ww = random.Random(int(x)).uniform(8, 18) * s
            d.line([x, H / 2, x + ww, H / 2], fill=255, width=lw)
            x += ww + 6 * s
    elif kind == 1:
        d.ellipse([pad, pad, W - pad, H - pad], outline=255, width=lw)
        d.line([W / 2, pad + 6 * s, W / 2, H - pad - 6 * s], fill=255, width=lw)
    else:
        d.line([pad, H - pad, W / 2, pad, W - pad, H - pad], fill=255, width=lw)
        d.line([pad + 10 * s, H - pad - 10 * s, W - pad - 10 * s, H - pad - 10 * s], fill=255, width=lw)
    glow = m.filter(ImageFilter.GaussianBlur(5 * s))
    rgb = Image.merge("RGB", [glow.point(lambda v, c=c: min(255, int(c * v / 255 * 1.6 * level))) for c in color])
    hot = m.point(lambda v: int(v * 0.85 * level))
    return ImageChops.add(rgb, Image.merge("RGB", (hot, hot, hot)))


def train_img(s):
    w, h = int(700 * s), int(36 * s)

    def fn(d, W, H):
        k = W / 700
        for car in range(3):
            x0 = car * 234 * k
            d.rounded_rectangle([x0, H * 0.08, x0 + 226 * k, H * 0.92], radius=6 * k, fill=(22, 24, 40, 255))
            d.line([x0 + 4 * k, H * 0.2, x0 + 222 * k, H * 0.2], fill=(70, 74, 110, 255), width=max(1, int(2 * k)))
            for i in range(9):
                wx = x0 + 12 * k + i * 23.5 * k
                d.rectangle([wx, H * 0.32, wx + 14 * k, H * 0.62], fill=(255, 226, 150, 255))
            if car < 2:
                d.rectangle([x0 + 226 * k, H * 0.4, x0 + 234 * k, H * 0.6], fill=(16, 16, 26, 255))
    return _img(w, h, fn)


def lantern_img(s):
    def fn(d, W, H):
        d.rectangle([W * 0.35, 0, W * 0.65, H * 0.12], fill=(40, 24, 20, 255))
        d.ellipse([0, H * 0.1, W, H * 0.9], fill=(230, 80, 40, 255))
        for k in (0.3, 0.5, 0.7):
            d.line([W * 0.08, H * k, W * 0.92, H * k], fill=(190, 50, 30, 255), width=max(1, int(W * 0.05)))
        d.ellipse([W * 0.2, H * 0.2, W * 0.5, H * 0.5], fill=(255, 170, 110, 255))
        d.rectangle([W * 0.35, H * 0.88, W * 0.65, H], fill=(40, 24, 20, 255))
    return _img(18 * s, 26 * s, fn)


def petal_img(s):
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=(255, 176, 206, 230))
        d.ellipse([W * 0.25, H * 0.2, W * 0.6, H * 0.6], fill=(255, 220, 236, 255))
    return _img(9 * s, 6 * s, fn)


def gull_img(s, up):
    def fn(d, W, H):
        lw = max(2, int(W * 0.07))
        if up:
            d.line([0, H * 0.2, W * 0.3, H * 0.75, W * 0.5, H * 0.55, W * 0.7, H * 0.75, W, H * 0.2], fill=(28, 24, 36, 255),
                   width=lw, joint="curve")
        else:
            d.line([0, H * 0.8, W * 0.3, H * 0.45, W * 0.5, H * 0.6, W * 0.7, H * 0.45, W, H * 0.8], fill=(28, 24, 36, 255),
                   width=lw, joint="curve")
    return _img(28 * s, 12 * s, fn)


# ---------------------------------------------------------------------------- les décors
def build_city(W, H, s, seed=11):
    """Ville la nuit : gratte-ciel, néons, métro aérien, réverbères, vapeur."""
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.74)
    sky = vgrad(W, H, [(0.0, (6, 6, 22)), (0.45, (20, 14, 46)), (0.74, (70, 32, 84)), (1.0, (26, 12, 36))])
    add_at(sky, radial(int(1400 * s), (70, 30, 60), 1.6), W // 2, H)
    stars = stars_on(sky, rng, 60, H * 0.3, W)
    moon(sky, int(W * 0.82), int(H * 0.18), 26, s)
    layers = []
    h = int(320 * s)
    c = Sil(tw, h, s)
    rects, tops = skyline(c, tw, h, s, rng, 120, 300, 50, 130)
    img = paint(c.mask(), [(0, (16, 16, 38)), (1, (30, 24, 56))], rim=(90, 70, 130), rim_px=max(1, int(2 * s)))
    windows_on(img, rects, s, rng, 0.3)
    layers.append({"img": img, "y": hz - h + int(10 * s), "f": 0.0, "stage": "far", "blinks": tops})
    h = int(260 * s)
    c = Sil(tw, h, s)
    rects2, _ = skyline(c, tw, h, s, rng, 70, 190, 90, 190)
    track_y = h * 0.34
    c.rect(-10, track_y, tw + 10, track_y + 12 * s)                        # viaduc du métro
    x = 40 * s
    while x < tw:
        c.rect(x - 7 * s, track_y, x + 7 * s, h)
        x += 180 * s
    img = paint(c.mask(), [(0, (12, 10, 28)), (1, (20, 14, 34))], rim=(130, 70, 140), rim_px=max(1, int(2 * s)))
    windows_on(img, rects2, s, rng, 0.14)
    neons, images = [], {}
    for i, (x, top, w, hh) in enumerate(rects2):
        if rng.random() < 0.7 and w > 100 * s:
            nw, nh = rng.uniform(60, min(150, w / s - 20)) * s, rng.uniform(22, 44) * s
            nx, ny = x + w / 2, max(top + 30 * s, track_y + 40 * s)
            if ny + nh > h - 30 * s:
                continue
            col = rng.choice(NEON)
            key = f"neon{i}"
            kind = rng.choice((0, 0, 1, 2))
            images[key] = neon_img(nw, nh, col, 1.0, s, kind)
            images[key + "_dim"] = neon_img(nw, nh, col, 0.45, s, kind)
            neons.append((key, nx, ny + nh / 2, rng.uniform(0, 6)))
    layers.append({"img": img, "y": H - h - int(38 * s), "f": 0.0, "stage": "mid", "neons": neons})
    h = int(120 * s)
    c = Sil(tw, h, s)
    c.rect(-10, h * 0.72, tw + 10, h)
    lights, vents = [], []
    x = 60 * s
    while x < tw:
        c.rect(x - 3 * s, h * 0.12, x + 3 * s, h)                              # réverbère
        c.line([(x, h * 0.14), (x + 22 * s, h * 0.08)], 3 * s)
        c.rect(x + 18 * s, h * 0.06, x + 34 * s, h * 0.12)
        lights.append((x + 26 * s, h * 0.13))
        if rng.random() < 0.5:
            vents.append((x + rng.uniform(80, 200) * s, h * 0.72))
        x += rng.uniform(260, 380) * s
    layers.append({"img": paint(c.mask(), [(0, (10, 8, 18)), (1, (6, 4, 10))], rim=(90, 60, 110), rim_px=max(1, int(2 * s))),
                   "y": H - h, "f": 0.0, "stage": "near", "lights": lights, "vents": vents})
    images["train"] = train_img(s)
    amb = {"stars": stars, "horizon": hz, "window": (255, 230, 170), "blink": (255, 40, 30), "images": images,
           "train_y": track_y, "hooks": {"mid": [hook_neons, hook_train], "near": [hook_steam]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def pagoda(c, x, base, w, h, tiers, s):
    c.rect(x - w * 0.56, base - h * 0.05, x + w * 0.56, base)
    tier_h = h * 0.84 / tiers
    for i in range(tiers):
        k = i / tiers
        bw = w * (1 - k * 0.5)
        y0 = base - h * 0.05 - i * tier_h
        c.rect(x - bw * 0.33, y0 - tier_h * 0.72, x + bw * 0.33, y0)
        rw = bw * 0.62
        ry = y0 - tier_h * 0.72
        c.poly([(x - rw - 8 * s, ry - 5 * s), (x - rw * 0.75, ry - tier_h * 0.08), (x - rw * 0.5, ry - tier_h * 0.36),
                (x + rw * 0.5, ry - tier_h * 0.36), (x + rw * 0.75, ry - tier_h * 0.08), (x + rw + 8 * s, ry - 5 * s),
                (x + rw * 0.8, ry + 3 * s), (x - rw * 0.8, ry + 3 * s)])
    c.rect(x - 2 * s, base - h - 18 * s, x + 2 * s, base - h * 0.86)
    for k in range(4):
        c.ellipse(x - 5 * s, base - h - 12 * s + k * 7 * s, x + 5 * s, base - h - 6 * s + k * 7 * s)


def gate(c, x, base, w, h, s):
    """Portique de temple à deux poteaux et deux traverses."""
    for px in (x - w * 0.36, x + w * 0.36):
        c.poly([(px - 7 * s, base), (px - 5 * s, base - h), (px + 5 * s, base - h), (px + 7 * s, base)])
    c.poly([(x - w * 0.58, base - h - 4 * s), (x - w * 0.5, base - h - 16 * s), (x + w * 0.5, base - h - 16 * s),
            (x + w * 0.58, base - h - 4 * s), (x + w * 0.5, base - h + 6 * s), (x - w * 0.5, base - h + 6 * s)])
    c.rect(x - w * 0.46, base - h * 0.78, x + w * 0.46, base - h * 0.72)


def stone_lantern(c, x, base, s):
    c.rect(x - 10 * s, base - 8 * s, x + 10 * s, base)
    c.rect(x - 4 * s, base - 30 * s, x + 4 * s, base - 8 * s)
    c.rect(x - 9 * s, base - 46 * s, x + 9 * s, base - 30 * s)
    c.poly([(x - 16 * s, base - 46 * s), (x, base - 60 * s), (x + 16 * s, base - 46 * s)])


def build_temple(W, H, s, seed=12):
    """Temple au crépuscule : montagnes dans la brume, pagode, portique, lanternes, cerisiers."""
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.7)
    sky = vgrad(W, H, [(0.0, (12, 10, 36)), (0.42, (52, 28, 80)), (0.66, (190, 96, 120)), (0.74, (236, 150, 124)), (1.0, (60, 30, 60))])
    stars = stars_on(sky, rng, 50, H * 0.28, W)
    moon(sky, int(W * 0.17), int(H * 0.22), 48, s, color=(250, 236, 214), glow=(70, 50, 70))
    layers = []
    for i, (amp, base_y, top_c, bot_c) in enumerate(((60, 0.55, (96, 66, 120), (170, 110, 140)), (44, 0.7, (70, 44, 92), (130, 80, 112)))):
        h = int(220 * s)
        c = Sil(tw, h, s)
        f = periodic(tw, rng, 5, amp * s)
        pts = [(x, h * base_y + f(x) - (abs(math.sin(x / tw * math.pi * (3 + i * 2))) * 50 * s)) for x in range(0, tw + 1, 6)]
        c.poly([(0, h)] + pts + [(tw, h)])
        layers.append({"img": paint(c.mask(), [(0, top_c), (1, bot_c)]), "y": hz - h + int((20 + i * 25) * s), "f": 0.0,
                       "stage": "far" if i == 0 else "far2"})
    h = int(300 * s)
    base = h - 2
    c = Sil(tw, h, s)
    bloom = Sil(tw, h, s)
    pagoda(c, tw * 0.64, base, 150 * s, 250 * s, 5, s)
    pagoda(c, tw * 0.9, base, 100 * s, 160 * s, 3, s)
    gate(c, tw * 0.3, base, 190 * s, 150 * s, s)
    for x in (tw * 0.22, tw * 0.38, tw * 0.55, tw * 0.73):
        stone_lantern(c, x, base, s)
    for x in (tw * 0.06, tw * 0.46, tw * 0.8):                           # cerisiers
        th = rng.uniform(90, 130) * s
        c.poly([(x - 7 * s, base), (x - 3 * s, base - th), (x + 3 * s, base - th), (x + 8 * s, base)])
        for _ in range(4):
            d = rng.choice((-1, 1))
            by = base - th * rng.uniform(0.5, 0.9)
            c.line([(x, by), (x + d * rng.uniform(30, 60) * s, by - rng.uniform(20, 40) * s)], 4 * s)
        for _ in range(16):
            bx, by = x + rng.uniform(-85, 85) * s, base - th - rng.uniform(-40, 50) * s
            r = rng.uniform(18, 34) * s
            bloom.ellipse(bx - r, by - r * 0.8, bx + r, by + r * 0.8)
    c.rect(-10, base - 6 * s, tw + 10, h)
    img = paint(c.mask(), [(0, (28, 16, 34)), (1, (40, 22, 40))], rim=(220, 130, 130), rim_px=max(1, int(2 * s)))
    pink = paint(bloom.mask().point(lambda v: v * 210 // 255), [(0, (255, 170, 200)), (1, (220, 120, 160))])
    img.alpha_composite(pink)
    rope_y = 70 * s
    lanterns = [(tw * k, rope_y + math.sin(k * math.pi * 3) * 6 * s, rng.uniform(26, 40) * s, rng.uniform(0, 6))
                for k in (0.12, 0.2, 0.42, 0.5, 0.58, 0.78, 0.86, 0.94)]
    layers.append({"img": img, "y": H - h - int(30 * s), "f": 0.0, "stage": "mid", "lanterns": lanterns})
    h = int(100 * s)
    c = Sil(tw, h, s)
    c.rect(-10, h * 0.45, tw + 10, h)
    x = 0
    while x < tw:                                                            # muret à tuiles
        c.poly([(x, h * 0.45), (x + 20 * s, h * 0.36), (x + 40 * s, h * 0.45)])
        x += 40 * s
    layers.append({"img": paint(c.mask(), [(0, (24, 14, 26)), (1, (12, 6, 14))], rim=(160, 90, 110), rim_px=max(1, int(2 * s))),
                   "y": H - h, "f": 0.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "images": {"lantern": lantern_img(s), "petal": petal_img(s)},
           "hooks": {"mid": [hook_lanterns], "front": [hook_petals]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def crane(c, x, base, h, s, d=1):
    c.line([(x, base), (x + 24 * s, base - h)], 6 * s)
    c.line([(x + 60 * s, base), (x + 36 * s, base - h)], 6 * s)
    c.line([(x + 6 * s, base - h * 0.35), (x + 54 * s, base - h * 0.35)], 4 * s)
    c.rect(x + 10 * s, base - h - 26 * s, x + 50 * s, base - h)
    c.line([(x + 30 * s, base - h - 20 * s), (x + 30 * s + d * 240 * s, base - h - 20 * s)], 7 * s)
    c.line([(x + 30 * s, base - h - 70 * s), (x + 30 * s + d * 200 * s, base - h - 22 * s)], 2 * s)
    c.line([(x + 30 * s, base - h - 70 * s), (x + 30 * s - d * 60 * s, base - h - 22 * s)], 2 * s)
    c.rect(x + 26 * s, base - h - 80 * s, x + 34 * s, base - h - 20 * s)
    c.line([(x + 30 * s + d * 170 * s, base - h - 20 * s), (x + 30 * s + d * 170 * s, base - h * 0.5)], 1.5 * s)


def build_harbor(W, H, s, seed=13):
    """Port au soleil couchant : mer qui scintille, phare, grues, conteneurs, mouettes."""
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.62)
    sky = vgrad(W, H, [(0.0, (22, 26, 66)), (0.32, (92, 62, 116)), (0.52, (222, 126, 104)), (0.62, (255, 186, 112)),
                       (0.621, (110, 70, 90)), (1.0, (18, 20, 42))])
    sun_x = int(W * 0.3)
    add_at(sky, radial(int(900 * s), (120, 60, 30), 2.0), sun_x, hz)
    d = ImageDraw.Draw(sky)
    d.ellipse([sun_x - 46 * s, hz - 52 * s, sun_x + 46 * s, hz + 40 * s], fill=(255, 226, 170))
    sea = vgrad(W, H - hz, [(0.0, (120, 74, 92)), (0.25, (64, 46, 80)), (1.0, (16, 18, 40))], noise=1.0)
    col = Image.new("L", (W, H - hz), 0)                                   # reflet du soleil, en tirets
    cd = ImageDraw.Draw(col)
    for y in range(0, H - hz, max(2, int(3 * s))):
        k = y / (H - hz)
        half = (40 + 200 * k) * s
        x = sun_x - half
        while x < sun_x + half:
            ln = rng.uniform(6, 40) * s * (0.5 + k)
            if rng.random() < 0.7 - 0.3 * abs(x - sun_x) / half:
                cd.line([(x, y), (x + ln, y)], fill=int(170 * (1 - k * 0.6)), width=max(1, int(1.4 * s)))
            x += ln + rng.uniform(4, 20) * s
    col = col.filter(ImageFilter.GaussianBlur(1.2 * s))
    sea.paste((255, 180, 120), (0, 0), col)
    sd = ImageDraw.Draw(sea)
    for _ in range(140):                                                    # vaguelettes
        y = rng.uniform(4, H - hz) * 1.0
        k = y / (H - hz)
        x = rng.uniform(0, W)
        ln = rng.uniform(20, 90) * s * (0.4 + k)
        sd.line([(x, y), (x + ln, y)], fill=(150, 110, 140) if k < 0.4 else (60, 60, 100), width=max(1, int(s)))
    sky.paste(sea, (0, hz))
    stars = stars_on(sky, rng, 30, H * 0.2, W)
    layers = []
    h = int(140 * s)
    c = Sil(tw, h, s)
    base = h - 1
    for x in (tw * 0.1, tw * 0.45):                                          # bateaux au loin
        L_ = rng.uniform(80, 130) * s
        c.poly([(x, base - 8 * s), (x + L_, base - 8 * s), (x + L_ * 0.9, base), (x + L_ * 0.08, base)])
        c.rect(x + L_ * 0.55, base - 22 * s, x + L_ * 0.75, base - 8 * s)
        c.rect(x + L_ * 0.62, base - 34 * s, x + L_ * 0.66, base - 22 * s)
    lx = tw * 0.86
    c.poly([(lx - 140 * s, base), (lx - 60 * s, base - 50 * s), (lx + 30 * s, base - 62 * s), (lx + 160 * s, base - 30 * s),
            (tw + 20, base - 20 * s), (tw + 20, base)])
    c.poly([(lx - 12 * s, base - 58 * s), (lx - 7 * s, base - 128 * s), (lx + 7 * s, base - 128 * s), (lx + 12 * s, base - 58 * s)])
    c.rect(lx - 10 * s, base - 140 * s, lx + 10 * s, base - 128 * s)
    c.poly([(lx - 12 * s, base - 140 * s), (lx, base - 152 * s), (lx + 12 * s, base - 140 * s)])
    layers.append({"img": paint(c.mask(), [(0, (40, 30, 56)), (1, (60, 40, 66))], rim=(240, 150, 120), rim_px=max(1, int(2 * s))),
                   "y": hz - h + int(2 * s), "f": 0.0, "stage": "far", "lamp": (lx, base - 134 * s)})
    h = int(320 * s)
    base = h - 1
    c = Sil(tw, h, s)
    boxes = Sil(tw, h, s)
    crane(c, tw * 0.52, base, 190 * s, s, -1)
    crane(c, tw * 0.74, base, 210 * s, s, 1)
    x = tw * 0.02
    while x < tw * 0.98:                                                      # piles de conteneurs
        if tw * 0.5 < x < tw * 0.6 or tw * 0.72 < x < tw * 0.8:
            x += 40 * s
            continue
        cols = rng.randint(1, 3)
        for j in range(rng.randint(1, 3)):
            for k in range(cols):
                bx = x + k * 64 * s
                by = base - (j + 1) * 26 * s
                boxes.rect(bx, by, bx + 62 * s, by + 25 * s)
        x += cols * 64 * s + rng.uniform(30, 90) * s
    c.rect(-10, base - 8 * s, tw + 10, h)
    img = paint(c.mask(), [(0, (24, 18, 34)), (1, (30, 22, 40))], rim=(230, 140, 110), rim_px=max(1, int(2 * s)))
    bm = boxes.mask()
    cont = paint(bm, [(0, (92, 46, 46)), (1, (50, 34, 50))], rim=(200, 120, 100), rim_px=max(1, int(2 * s)))
    ridge = Image.new("L", (tw, h), 0)                                       # nervures des conteneurs
    rd = ImageDraw.Draw(ridge)
    for x in range(0, tw, max(3, int(8 * s))):
        rd.line([(x, 0), (x, h)], fill=70, width=1)
    cont.paste((10, 6, 12), (0, 0), ImageChops.multiply(ridge, bm))
    img.alpha_composite(cont)
    layers.append({"img": img, "y": H - h - int(100 * s), "f": 0.0, "stage": "mid"})
    h = int(80 * s)
    c = Sil(tw, h, s)
    c.rect(-10, h * 0.5, tw + 10, h)
    x = 80 * s
    while x < tw:
        c.ellipse(x - 12 * s, h * 0.3, x + 12 * s, h * 0.55)
        c.rect(x - 9 * s, h * 0.42, x + 9 * s, h * 0.6)
        x += rng.uniform(220, 340) * s
    layers.append({"img": paint(c.mask(), [(0, (26, 18, 30)), (1, (12, 8, 16))], rim=(200, 120, 100), rim_px=max(1, int(2 * s))),
                   "y": H - h, "f": 0.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "sun_x": sun_x, "images": {"gull_up": gull_img(s, True), "gull_down": gull_img(s, False)},
           "hooks": {"sky": [hook_glints], "far": [hook_lighthouse, hook_gulls]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def build_ruins(W, H, s, seed=14):
    """Ruines la nuit : pyramide au loin, colonnes, torches, lucioles."""
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.68)
    sky = vgrad(W, H, [(0.0, (4, 8, 20)), (0.5, (10, 26, 42)), (0.72, (28, 56, 60)), (1.0, (8, 18, 20))])
    stars = stars_on(sky, rng, 120, H * 0.45, W)
    moon(sky, int(W * 0.72), int(H * 0.2), 40, s, glow=(30, 60, 60))
    layers = []
    h = int(200 * s)
    base = h - 1
    c = Sil(tw, h, s)
    f = periodic(tw, rng, 4, 26 * s)
    prof = [(x, base - 60 * s + f(x)) for x in range(0, tw + 1, 8)]
    c.poly([(0, base)] + prof + [(tw, base)])
    for x, y in prof[::3]:
        r = rng.uniform(8, 18) * s
        c.ellipse(x - r, y - r, x + r, y + r)
    px = tw * 0.42
    for i in range(8):                                                         # grande pyramide à degrés
        w = (420 - i * 46) * s
        c.rect(px - w / 2, base - 30 * s - (i + 1) * 20 * s, px + w / 2, base - 30 * s - i * 20 * s)
    c.rect(px - 34 * s, base - 30 * s - 8 * 20 * s - 34 * s, px + 34 * s, base - 30 * s - 8 * 20 * s)
    c.rect(px - 10 * s, base - 30 * s - 8 * 20 * s, px + 10 * s, base - 30 * s)
    top_fire = (px, base - 30 * s - 8 * 20 * s - 40 * s)
    layers.append({"img": paint(c.mask(), [(0, (18, 40, 44)), (1, (34, 64, 62))], rim=(80, 130, 120), rim_px=max(1, int(2 * s))),
                   "y": hz - h + int(30 * s), "f": 0.0, "stage": "far", "torches": [top_fire]})
    h = int(300 * s)
    base = h - 1
    c = Sil(tw, h, s)
    torches = []
    x = 30 * s
    while x < tw:
        r = rng.random()
        if r < 0.5:                                                            # colonne, parfois brisée
            ch = rng.uniform(150, 230) * s
            top = base - ch
            if rng.random() < 0.35:
                c.poly([(x - 18 * s, base), (x - 16 * s, top + 30 * s), (x - 4 * s, top + rng.uniform(0, 30) * s),
                        (x + 8 * s, top + rng.uniform(10, 40) * s), (x + 16 * s, top + 20 * s), (x + 18 * s, base)])
            else:
                c.rect(x - 16 * s, top, x + 16 * s, base)
                c.rect(x - 24 * s, top - 10 * s, x + 24 * s, top)
                c.rect(x - 22 * s, base - 14 * s, x + 22 * s, base)
                c.poly([(x - 9 * s, top - 10 * s), (x + 9 * s, top - 10 * s), (x + 5 * s, top - 2 * s), (x - 5 * s, top - 2 * s)])
                torches.append((x, top - 16 * s))
            x += rng.uniform(90, 150) * s
        elif r < 0.72:                                                         # arche
            aw = rng.uniform(120, 180) * s
            c.rect(x, base - 160 * s, x + 24 * s, base)
            c.rect(x + aw - 24 * s, base - 160 * s, x + aw, base)
            c.ellipse(x, base - 220 * s, x + aw, base - 100 * s)
            c.ellipse(x + 24 * s, base - 190 * s, x + aw - 24 * s, base - 120 * s, fill=0)
            c.rect(x + 24 * s, base - 160 * s, x + aw - 24 * s, base, fill=0)
            x += aw + rng.uniform(40, 100) * s
        else:                                                                  # façade de temple à fronton
            fw = rng.uniform(170, 230) * s
            c.poly([(x - 10 * s, base - 170 * s), (x + fw / 2, base - 220 * s), (x + fw + 10 * s, base - 170 * s)])
            c.rect(x - 10 * s, base - 172 * s, x + fw + 10 * s, base - 160 * s)
            for k in range(5):
                cx = x + 8 * s + k * (fw - 16 * s) / 4
                c.rect(cx - 8 * s, base - 160 * s, cx + 8 * s, base)
            c.rect(x - 14 * s, base - 14 * s, x + fw + 14 * s, base)
            torches.append((x - 26 * s, base - 120 * s))
            torches.append((x + fw + 26 * s, base - 120 * s))
            for tx in (x - 26 * s, x + fw + 26 * s):                          # torchères
                c.rect(tx - 3 * s, base - 116 * s, tx + 3 * s, base)
                c.poly([(tx - 9 * s, base - 116 * s), (tx + 9 * s, base - 116 * s), (tx + 5 * s, base - 108 * s), (tx - 5 * s, base - 108 * s)])
            x += fw + rng.uniform(70, 120) * s
    c.rect(-10, base - 12 * s, tw + 10, h)
    layers.append({"img": paint(c.mask(), [(0, (14, 26, 26)), (1, (22, 36, 34))], rim=(170, 120, 80), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(60 * s), "f": 0.0, "stage": "mid", "torches": torches})
    h = int(90 * s)
    c = Sil(tw, h, s)
    for k in range(3):                                                          # marches de pierre
        c.rect(-10, h * (0.4 + k * 0.2), tw + 10, h)
    layers.append({"img": paint(c.mask(), [(0, (20, 26, 24)), (1, (8, 12, 12))], rim=(150, 110, 80), rim_px=max(1, int(2 * s))),
                   "y": H - h, "f": 0.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "fireflies": True, "hooks": {"far": [hook_torches], "mid": [hook_torches]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def build_city_war(W, H, s, seed=15):
    """Ville en guerre la nuit (Metal Slug) : immeubles éventrés, incendies, fumée, explosions au loin."""
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.72)
    sky = vgrad(W, H, [(0.0, (10, 6, 12)), (0.45, (36, 16, 22)), (0.72, (120, 46, 30)), (1.0, (30, 12, 14))])
    add_at(sky, radial(int(1300 * s), (90, 30, 10), 1.8), W // 2, hz)
    stars = stars_on(sky, rng, 30, H * 0.25, W)
    layers = []
    h = int(260 * s)
    c = Sil(tw, h, s)
    rects, _ = skyline(c, tw, h, s, rng, 100, 240, 60, 140, broken=True)
    img = paint(c.mask(), [(0, (26, 14, 20)), (1, (44, 22, 26))], rim=(200, 90, 50), rim_px=max(1, int(2 * s)))
    windows_on(img, rects, s, rng, 0.08, colors=((255, 140, 50), (255, 100, 30)))
    fires_far = [(x + w * rng.uniform(0.2, 0.8), h - hh + rng.uniform(10, 40) * s) for (x, top, w, hh) in rects if rng.random() < 0.25]
    layers.append({"img": img, "y": hz - h + int(8 * s), "f": 0.12, "stage": "far", "fires": fires_far})
    h = int(230 * s)
    base = h - 1
    c = Sil(tw, h, s)
    fires = []
    x = 20 * s
    while x < tw - 60 * s:
        w, bh = rng.uniform(70, 160) * s, rng.uniform(80, 170) * s
        ruin(c, x, base, w, bh, s, rng)
        if rng.random() < 0.55:
            fires.append((x + w * rng.uniform(0.2, 0.8), base - bh * rng.uniform(0.5, 0.9)))
        x += w + rng.uniform(10, 60) * s
    c.rect(-10, base - 6 * s, tw + 10, h)
    layers.append({"img": paint(c.mask(), [(0, (20, 10, 16)), (1, (34, 16, 22))], rim=(220, 100, 50), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(34 * s), "f": 0.38, "stage": "mid", "fires": fires})
    h = int(110 * s)
    c = Sil(tw, h, s)
    f = periodic(tw, rng, 4, 10 * s)
    c.poly([(0, h)] + [(x, h * 0.66 + f(x)) for x in range(0, tw + 1, 8)] + [(tw, h)])
    x = 50 * s
    while x < tw - 100 * s:
        gy = h * 0.66 + f(x)
        if rng.random() < 0.5:
            sandbags(c, x, gy + 4 * s, rng.uniform(90, 160) * s, rng.randint(2, 3), s)
        else:
            for _ in range(5):                                                  # gravats
                r = rng.uniform(6, 16) * s
                rx = x + rng.uniform(0, 80) * s
                c.poly([(rx - r, gy + 4 * s), (rx - r * 0.4, gy - r), (rx + r * 0.6, gy - r * 0.7), (rx + r, gy + 4 * s)])
        x += rng.uniform(200, 320) * s
    layers.append({"img": paint(c.mask(), [(0, (16, 8, 12)), (1, (8, 4, 6))], rim=(150, 70, 40), rim_px=max(1, int(2 * s))),
                   "y": H - h, "f": 1.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "explosions": True, "searchlights": [(0.28, 0.9), (0.74, 1.2)], "plane": "bomber",
           "plane_color": (20, 10, 16), "dust": (255, 150, 90), "window": (255, 140, 50), "blink": (255, 40, 30),
           "hooks": {"far": [hook_fires], "mid": [hook_fires]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def build_base(W, H, s, seed=16):
    """Base ennemie la nuit (Metal Slug) : hangars, tour de contrôle, cuves, cheminées, gyrophares, alerte."""
    rng = random.Random(seed)
    tw = int(W + 600 * s)
    hz = int(H * 0.7)
    sky = vgrad(W, H, [(0.0, (4, 6, 14)), (0.5, (16, 20, 34)), (0.74, (46, 42, 56)), (1.0, (14, 14, 20))])
    stars = stars_on(sky, rng, 110, H * 0.4, W)
    layers = []
    h = int(180 * s)
    base = h - 1
    c = Sil(tw, h, s)
    f = periodic(tw, rng, 4, 40 * s)
    c.poly([(0, base)] + [(x, base - 70 * s + f(x) - abs(math.sin(x / 180)) * 30 * s) for x in range(0, tw + 1, 8)] + [(tw, base)])
    for x in (tw * 0.2, tw * 0.62):                                            # paraboles radar
        c.rect(x - 3 * s, base - 120 * s, x + 3 * s, base - 60 * s)
        c.ellipse(x - 30 * s, base - 150 * s, x + 30 * s, base - 110 * s)
    layers.append({"img": paint(c.mask(), [(0, (20, 22, 34)), (1, (32, 32, 44))], rim=(90, 96, 130), rim_px=max(1, int(2 * s))),
                   "y": hz - h + int(20 * s), "f": 0.12, "stage": "far"})
    h = int(250 * s)
    base = h - 1
    c = Sil(tw, h, s)
    lights, blinks, stacks, beacons = [], [], [], []
    x = 30 * s
    while x < tw - 80 * s:
        r = rng.random()
        if r < 0.3:
            w = rng.uniform(180, 260) * s                                       # hangar
            c.ellipse(x, base - w * 0.55, x + w, base + w * 0.45)
            c.rect(x + w * 0.3, base - w * 0.32, x + w * 0.7, base, fill=0)
            c.rect(x + w * 0.32, base - w * 0.3, x + w * 0.68, base)
            lights.append((x + w * 0.5, base - w * 0.36))
            x += w + rng.uniform(20, 60) * s
        elif r < 0.45:
            tx = x + 30 * s                                                     # tour de contrôle
            c.rect(tx - 14 * s, base - 170 * s, tx + 14 * s, base)
            c.poly([(tx - 40 * s, base - 170 * s), (tx + 40 * s, base - 170 * s), (tx + 32 * s, base - 200 * s), (tx - 32 * s, base - 200 * s)])
            c.rect(tx - 34 * s, base - 196 * s, tx + 34 * s, base - 184 * s, fill=0)
            c.rect(tx - 2 * s, base - 226 * s, tx + 2 * s, base - 200 * s)
            beacons.append((tx, base - 230 * s))
            lights.append((tx, base - 190 * s))
            x += 100 * s
        elif r < 0.65:
            for k in range(rng.randint(1, 3)):                                  # cuves
                cx = x + k * 70 * s
                c.rect(cx, base - 90 * s, cx + 60 * s, base)
                c.ellipse(cx, base - 104 * s, cx + 60 * s, base - 76 * s)
            x += rng.randint(2, 3) * 70 * s
        elif r < 0.8:
            c.rect(x, base - 200 * s, x + 18 * s, base)                          # cheminée
            c.rect(x - 4 * s, base - 206 * s, x + 22 * s, base - 196 * s)
            stacks.append((x + 9 * s, base - 210 * s))
            blinks.append((x + 9 * s, base - 214 * s))
            x += 70 * s
        else:
            watchtower(c, x, base, rng.uniform(150, 190) * s, s)
            beacons.append((x + 27 * s, base - 186 * s))
            x += 110 * s
    c.rect(-10, base - 6 * s, tw + 10, h)
    layers.append({"img": paint(c.mask(), [(0, (14, 16, 24)), (1, (24, 26, 34))], rim=(110, 120, 150), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(34 * s), "f": 0.38, "stage": "mid", "lights": lights, "blinks": blinks, "stacks": stacks,
                   "beacons": beacons})
    h = int(110 * s)
    c = Sil(tw, h, s)
    c.rect(-10, h * 0.7, tw + 10, h)
    x = 30 * s
    while x < tw - 100 * s:
        if rng.random() < 0.5:
            wire_posts(c, x, h * 0.72, rng.uniform(160, 260) * s, s, rng)
        else:
            for k in range(rng.randint(2, 4)):                                   # fûts
                bx = x + k * 26 * s
                c.rect(bx, h * 0.42, bx + 22 * s, h * 0.72)
        x += rng.uniform(240, 360) * s
    layers.append({"img": paint(c.mask(), [(0, (12, 12, 18)), (1, (6, 6, 10))], rim=(80, 90, 120), rim_px=max(1, int(2 * s))),
                   "y": H - h, "f": 1.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "explosions": True, "searchlights": [(0.2, 1.0), (0.5, 0.7), (0.8, 1.3)],
           "plane": "heli", "plane_color": (12, 12, 18), "window": (255, 220, 160), "blink": (255, 40, 30),
           "hooks": {"mid": [hook_stacks, hook_beacons]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


def with_crowd(builder):
    """Même décor, figé, avec du public devant (jeux de combat)."""
    def build(W, H, s, seed=None):
        th = builder(W, H, s)
        rng = random.Random(77)
        for L in th["layers"]:
            L["f"] = 0.0
        th["layers"] += crowd_layers(th["tw"], H, s, rng)
        th["amb"] = dict(th["amb"], crowd=(H - 118 * s, H - 30 * s))
        th["amb"].pop("explosions", None)
        return th
    return build


hd_bg.BUILDERS.update({
    "city": build_city, "temple": build_temple, "harbor": build_harbor, "ruins": build_ruins,
    "city_war": build_city_war, "base": build_base,
})
for _name in ("city", "temple", "harbor", "ruins", "desert", "jungle", "snow"):
    hd_bg.BUILDERS["fight_" + _name] = with_crowd(hd_bg.BUILDERS[_name])

FIGHT_STAGES = ("arena", "fight_city", "fight_temple", "fight_harbor", "fight_ruins", "fight_desert", "fight_snow", "fight_jungle")
MISSION_STAGES = ("jungle", "desert", "snow", "city_war", "harbor", "base")
