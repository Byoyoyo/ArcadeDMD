"""Fight stages of the Capcom CPS fighting games (1.30), drawn by the program in the spirit of the places of the games.
They register in hd_bg.BUILDERS when this module is imported (by hd_fight) and the fighting games take them in
"hd": {"stages": [...]}, one per stage of the game (the "backdrop" value read in the game picks it): a castle roof in
Japan at night, a Chinese street market, a steel factory, a gothic manor under the moon, an Indian palace at sunset, a
golden temple in Thailand on its river, a laboratory, the air base. Each has its crowd in front and its animations
(lanterns, petals, furnaces and sparks, bats and lightning, torches, glints on the water, screens and tanks).

Décors de combat des jeux de combat Capcom CPS (1.30), dessinés par le programme dans l'esprit des lieux des jeux : toit
de château au Japon la nuit, marché chinois, aciérie, manoir gothique sous la lune, palais indien au couchant, temple d'or
en Thaïlande au bord du fleuve, laboratoire, base aérienne. Chacun a son public devant et ses animations. Aucune image
ne vient d'un jeu.
"""

import math
import random

from PIL import Image, ImageDraw

from . import hd_bg
from .hd_bg import Sil, add_at, palm, paint, periodic, radial, vgrad
from .hd_stages import (_img, gull_img, hook_fires, hook_glints, hook_gulls, hook_lanterns, hook_petals, hook_steam,
                        hook_torches, lantern_img, moon, petal_img, stars_on, with_crowd)


def _layer(tw, h, parts):
    """One picture made of several painted silhouettes, one over the other. / Plusieurs silhouettes peintes l'une sur l'autre."""
    img = Image.new("RGBA", (tw, h), (0, 0, 0, 0))
    for sil, stops, rim, rim_px in parts:
        img.alpha_composite(paint(sil.mask(), stops, rim=rim, rim_px=rim_px))
    return img


def _hills(tw, h, s, rng, base_y, amp, bumps, stops):
    c = Sil(tw, h, s)
    f = periodic(tw, rng, 5, amp * s)
    pts = [(x, h * base_y + f(x) - abs(math.sin(x / tw * math.pi * bumps)) * amp * 0.8 * s) for x in range(0, tw + 1, 6)]
    c.poly([(0, h)] + pts + [(tw, h)])
    return paint(c.mask(), stops)


def _clouds(sky, rng, n, y0, y1, color, alpha, s):
    """Long thin clouds drawn into the sky. / Longs nuages fins dans le ciel."""
    W, H = sky.size
    over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    for _ in range(n):
        x, y = rng.uniform(-100, W), rng.uniform(y0, y1)
        w = rng.uniform(180, 420) * s
        for k in range(5):
            dx = (k - 2) * w * 0.18
            d.ellipse([x + dx - w * 0.22, y - 9 * s - k % 2 * 4 * s, x + dx + w * 0.22, y + 9 * s], fill=color + (alpha,))
    sky.paste(over, (0, 0), over)


# ============================================================================ castle roof, Japan / toit de château
def keep(walls, roofs, stone, x, base, w, h, tiers, s, wins):
    """A Japanese castle keep: a stone base, white walls and curved roofs on each tier. / Donjon japonais."""
    bh = h * 0.22
    stone.poly([(x - w * 0.64, base), (x - w * 0.5, base - bh), (x + w * 0.5, base - bh), (x + w * 0.64, base)])
    y = base - bh
    th = (h - bh) / tiers
    for i in range(tiers):
        bw = w * (0.86 - i / tiers * 0.44)
        top = y - th * 0.6
        walls.rect(x - bw / 2, top, x + bw / 2, y)
        for k in range(max(2, int(bw / (26 * s)))):              # windows / fenêtres
            wx = x - bw / 2 + (k + 0.5) * bw / max(2, int(bw / (26 * s)))
            wins.append((wx, top + th * 0.3))
        rw = bw * 0.62 + 14 * s
        roofs.poly([(x - rw - 14 * s, top + 3 * s), (x - rw * 0.8, top - th * 0.14), (x - bw * 0.34, top - th * 0.36),
                    (x + bw * 0.34, top - th * 0.36), (x + rw * 0.8, top - th * 0.14), (x + rw + 14 * s, top + 3 * s),
                    (x + rw * 0.9, top + 8 * s), (x - rw * 0.9, top + 8 * s)])
        if i % 2 == 0:                                            # small gable in the middle / pignon
            roofs.poly([(x - bw * 0.2, top - th * 0.3), (x, top - th * 0.62), (x + bw * 0.2, top - th * 0.3)])
        y = top - th * 0.36
    roofs.rect(x - 3 * s, y - 16 * s, x + 3 * s, y)
    for d in (-1, 1):                                             # golden fish ornaments at the top / ornements
        roofs.ellipse(x + d * w * 0.14 - 5 * s, y - 14 * s, x + d * w * 0.14 + 5 * s, y)


def build_castle(W, H, s, seed=31):
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.66)
    sky = vgrad(W, H, [(0.0, (8, 10, 30)), (0.4, (26, 30, 70)), (0.62, (70, 60, 110)), (0.72, (120, 90, 120)), (1.0, (30, 24, 40))])
    stars = stars_on(sky, rng, 70, H * 0.4, W)
    _clouds(sky, rng, 6, H * 0.1, H * 0.36, (60, 60, 100), 90, s)
    moon(sky, int(W * 0.8), int(H * 0.2), 54, s, color=(248, 240, 214), glow=(60, 60, 90))
    layers = [{"img": _hills(tw, int(200 * s), s, rng, 0.55, 46, 3, [(0, (40, 44, 86)), (1, (60, 56, 100))]),
               "y": hz - int(150 * s), "f": 0.0, "stage": "far"}]
    h = int(330 * s)
    base = h - 4
    walls, roofs, stone = Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s)
    wins = []
    keep(walls, roofs, stone, tw * 0.3, base, 330 * s, 300 * s, 4, s, wins)
    keep(walls, roofs, stone, tw * 0.74, base, 190 * s, 190 * s, 3, s, wins)
    stone.rect(-10, base - 30 * s, tw + 10, h)                    # the castle wall / la muraille
    for x in range(0, tw, int(60 * s)):
        roofs.poly([(x, base - 30 * s), (x + 30 * s, base - 40 * s), (x + 60 * s, base - 30 * s), (x + 60 * s, base - 26 * s), (x, base - 26 * s)])
    img = _layer(tw, h, [(stone, [(0, (70, 72, 96)), (1, (40, 40, 58))], (150, 150, 190), max(1, int(2 * s))),
                         (walls, [(0, (214, 214, 230)), (1, (150, 152, 180))], None, 1),
                         (roofs, [(0, (30, 34, 56)), (1, (20, 22, 38))], (160, 170, 220), max(1, int(2 * s)))])
    d = ImageDraw.Draw(img)
    for (wx, wy) in wins:
        d.rectangle([wx - 4 * s, wy - 6 * s, wx + 4 * s, wy + 6 * s], fill=(40, 34, 40, 255))
    lights = [(wx, wy) for (wx, wy) in wins if rng.random() < 0.45]
    layers.append({"img": img, "y": H - h - int(60 * s), "f": 0.0, "stage": "mid", "lights": lights})
    h = int(90 * s)
    c = Sil(tw, h, s)                                             # the roof where they fight / le toit du combat
    c.rect(-10, h * 0.42, tw + 10, h)
    x = 0
    while x < tw:
        c.ellipse(x, h * 0.34, x + 24 * s, h * 0.52)
        x += 24 * s
    layers.append({"img": paint(c.mask(), [(0, (34, 30, 52)), (1, (16, 14, 26))], rim=(170, 170, 220), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(70 * s), "f": 0.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "window": (255, 200, 120), "images": {"petal": petal_img(s)}, "hooks": {"front": [hook_petals]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ============================================================================ Chinese street market / marché chinois
def build_market(W, H, s, seed=32):
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.6)
    sky = vgrad(W, H, [(0.0, (70, 110, 170)), (0.45, (190, 160, 150)), (0.62, (250, 190, 130)), (1.0, (120, 70, 50))])
    _clouds(sky, rng, 5, H * 0.08, H * 0.3, (255, 230, 210), 110, s)
    far = Sil(tw, int(160 * s), s)                                # tiled roofs far away / toits au loin
    x = 0
    while x < tw:
        w = rng.uniform(120, 200) * s
        top = rng.uniform(30, 80) * s
        far.rect(x, top + 20 * s, x + w, 160 * s)
        far.poly([(x - 14 * s, top + 24 * s), (x + w * 0.2, top), (x + w * 0.8, top), (x + w + 14 * s, top + 24 * s)])
        x += w + rng.uniform(4, 30) * s
    layers = [{"img": paint(far.mask(), [(0, (150, 110, 110)), (1, (120, 90, 96))]), "y": hz - int(130 * s), "f": 0.0, "stage": "far"}]
    h = int(320 * s)
    base = h - 2
    walls, roofs, red, gold = Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s)
    lights, signs = [], []
    x = 0
    while x < tw:                                                 # two-storey shops / boutiques à étage
        w = rng.uniform(170, 240) * s
        top = base - rng.uniform(190, 240) * s
        walls.rect(x + 4 * s, top, x + w - 4 * s, base)
        roofs.poly([(x - 16 * s, top + 6 * s), (x + 10 * s, top - 18 * s), (x + w - 10 * s, top - 18 * s), (x + w + 16 * s, top + 6 * s),
                    (x + w, top + 12 * s), (x, top + 12 * s)])
        mid = top + (base - top) * 0.45
        roofs.poly([(x - 8 * s, mid + 4 * s), (x + 6 * s, mid - 8 * s), (x + w - 6 * s, mid - 8 * s), (x + w + 8 * s, mid + 4 * s)])
        for k in range(3):                                        # upstairs windows / fenêtres de l'étage
            wx = x + w * (0.22 + 0.28 * k)
            lights.append((wx, top + (mid - top) * 0.55))
        sx = x + w * rng.uniform(0.2, 0.7)                        # a hanging sign / une enseigne verticale
        red.rect(sx, mid + 10 * s, sx + 26 * s, mid + 110 * s)
        signs.append((sx, mid + 10 * s))
        for k in range(rng.randint(5, 8)):                        # awning stripes / store rayé
            ax = x + 10 * s + k * (w - 20 * s) / 8
            (red if k % 2 == 0 else gold).poly([(ax, base - 96 * s), (ax + (w - 20 * s) / 8, base - 96 * s),
                                                (ax + (w - 20 * s) / 8 + 6 * s, base - 70 * s), (ax + 6 * s, base - 70 * s)])
        x += w
    gx = tw * 0.5                                                 # the gate in the middle / le portique
    for px in (gx - 110 * s, gx + 110 * s):
        red.rect(px - 9 * s, base - 260 * s, px + 9 * s, base)
    red.rect(gx - 130 * s, base - 236 * s, gx + 130 * s, base - 222 * s)
    roofs.poly([(gx - 170 * s, base - 252 * s), (gx - 130 * s, base - 282 * s), (gx + 130 * s, base - 282 * s), (gx + 170 * s, base - 252 * s),
                (gx + 150 * s, base - 246 * s), (gx - 150 * s, base - 246 * s)])
    gold.rect(gx - 60 * s, base - 218 * s, gx + 60 * s, base - 186 * s)
    img = _layer(tw, h, [(walls, [(0, (196, 150, 120)), (1, (130, 90, 70))], None, 1),
                         (roofs, [(0, (60, 90, 80)), (1, (36, 56, 50))], (140, 200, 170), max(1, int(2 * s))),
                         (red, [(0, (200, 40, 40)), (1, (150, 24, 30))], (255, 130, 100), max(1, int(1 * s))),
                         (gold, [(0, (240, 200, 90)), (1, (200, 150, 50))], None, 1)])
    d = ImageDraw.Draw(img)
    for (sx, sy) in signs:                                        # golden strokes on the signs (no real letters) / traits dorés
        for k in range(4):
            yy = sy + 12 * s + k * 23 * s
            d.rectangle([sx + 7 * s, yy, sx + 19 * s, yy + 3 * s], fill=(250, 210, 90, 255))
            d.rectangle([sx + 11 * s, yy - 6 * s, sx + 15 * s, yy + 10 * s], fill=(250, 210, 90, 255))
    for k in range(5):
        d.rectangle([gx - 50 * s + k * 22 * s, base - 210 * s, gx - 38 * s + k * 22 * s, base - 194 * s], fill=(150, 30, 30, 255))
    lanterns = [(tw * k + rng.uniform(-10, 10) * s, 50 * s + math.sin(k * 7) * 10 * s, rng.uniform(20, 30) * s, rng.uniform(0, 6))
                for k in (0.05, 0.12, 0.2, 0.3, 0.38, 0.62, 0.7, 0.8, 0.88, 0.95)]
    vents = [(tw * k, h - 90 * s) for k in (0.18, 0.66, 0.92)]
    layers.append({"img": img, "y": H - h - int(40 * s), "f": 0.0, "stage": "mid", "lights": lights, "lanterns": lanterns, "vents": vents})
    h = int(110 * s)
    c = Sil(tw, h, s)                                             # stalls, baskets and bicycles / étals, paniers, vélos
    x = 20 * s
    while x < tw:
        kind = rng.random()
        if kind < 0.4:
            c.rect(x, h * 0.4, x + 70 * s, h)
            c.rect(x - 6 * s, h * 0.34, x + 76 * s, h * 0.42)
        elif kind < 0.7:
            for k in range(3):
                c.ellipse(x + k * 22 * s, h * 0.5, x + k * 22 * s + 26 * s, h * 0.8)
            c.rect(x, h * 0.66, x + 70 * s, h)
        else:
            for wx in (x, x + 46 * s):
                c.ellipse(wx, h * 0.46, wx + 30 * s, h * 0.76)
            c.line([(x + 15 * s, h * 0.61), (x + 34 * s, h * 0.36), (x + 61 * s, h * 0.61)], 4 * s)
            c.line([(x + 34 * s, h * 0.36), (x + 54 * s, h * 0.36)], 4 * s)
        x += rng.uniform(110, 170) * s
    layers.append({"img": paint(c.mask(), [(0, (70, 40, 34)), (1, (36, 20, 18))], rim=(255, 190, 140), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(30 * s), "f": 0.0, "stage": "near"})
    amb = {"horizon": hz, "window": (255, 220, 150), "images": {"lantern": lantern_img(s)}, "hooks": {"mid": [hook_lanterns, hook_steam]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ============================================================================ steel factory / aciérie
def hook_sparks(bd, screen, b, L, now, dt):
    """Sparks falling from the ladle, the molten stream glowing. / Étincelles qui tombent de la poche, coulée qui luit."""
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    x0 = bd._layer_x(L, b["tw"])
    for i, (x, y, y1) in enumerate(L.get("pours", ())):
        for k in range(6):
            yy = L["y"] + y + (y1 - y) * k / 5
            g = sp.glow((14 + 3 * math.sin(now * 9 + k)) * bd.s, (255, 150, 40), 8, hot=0.7)
            screen.blit(g, (int(x0 + x - g.get_width() / 2), int(yy - g.get_height() / 2)), special_flags=add)
        if bd.rng.random() < dt * 20:
            p = bd.fx.glow(x0 + x, L["y"] + y1, 2, 3, (255, 200, 90), bd.rng.uniform(0.5, 1.1), "mid", 1.0, 0.0, hot=1.0)
            p.vx, p.vy = bd.rng.uniform(-160, 160) * bd.s, -bd.rng.uniform(60, 200) * bd.s


def build_factory(W, H, s, seed=33):
    tw = W
    hz = int(H * 0.7)
    sky = vgrad(W, H, [(0.0, (14, 16, 24)), (0.5, (40, 36, 40)), (0.8, (90, 54, 34)), (1.0, (40, 24, 18))])
    back = Sil(tw, H, s)                                          # back wall windows and trusses / verrières et poutres
    frames = Sil(tw, H, s)
    for x in range(0, tw, int(160 * s)):
        back.rect(x + 20 * s, 40 * s, x + 140 * s, 200 * s)
        for k in range(1, 4):
            frames.line([(x + 20 * s + k * 30 * s, 40 * s), (x + 20 * s + k * 30 * s, 200 * s)], 3 * s)
        frames.line([(x + 20 * s, 120 * s), (x + 140 * s, 120 * s)], 3 * s)
    for x in range(0, tw, int(120 * s)):
        frames.line([(x, 20 * s), (x + 60 * s, 0)], 5 * s)
        frames.line([(x + 60 * s, 0), (x + 120 * s, 20 * s)], 5 * s)
    frames.rect(-10, 18 * s, tw + 10, 26 * s)
    sky.paste(paint(back.mask(), [(0, (80, 90, 110)), (1, (60, 60, 70))]), (0, 0), back.mask())
    sky.paste(paint(frames.mask(), [(0, (24, 24, 30)), (1, (30, 28, 32))]), (0, 0), frames.mask())
    layers = []
    h = int(340 * s)
    base = h - 2
    steel, dark, hot = Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s)
    fires, pours, vents, blinks = [], [], [], []
    for fx in (tw * 0.2, tw * 0.72):                              # blast furnaces / hauts fourneaux
        steel.poly([(fx - 90 * s, base), (fx - 70 * s, base - 230 * s), (fx + 70 * s, base - 230 * s), (fx + 90 * s, base)])
        steel.rect(fx - 40 * s, base - 300 * s, fx + 40 * s, base - 226 * s)
        hot.ellipse(fx - 40 * s, base - 120 * s, fx + 40 * s, base - 60 * s)
        fires.append((fx, base - 90 * s))
        for k in range(4):
            dark.rect(fx - 72 * s, base - 200 * s + k * 44 * s, fx + 72 * s, base - 194 * s + k * 44 * s)
        vents.append((fx, base - 300 * s))
    lx = tw * 0.46                                                # the ladle on its chains / la poche sur ses chaînes
    for cx in (lx - 50 * s, lx + 50 * s):
        dark.line([(cx, 0), (lx + (cx - lx) * 0.4, base - 230 * s)], 4 * s)
    steel.poly([(lx - 70 * s, base - 236 * s), (lx + 70 * s, base - 236 * s), (lx + 54 * s, base - 160 * s), (lx - 54 * s, base - 160 * s)])
    hot.rect(lx - 62 * s, base - 240 * s, lx + 62 * s, base - 230 * s)
    pours.append((lx + 50 * s, base - 170 * s, base - 70 * s))
    hot.poly([(lx - 10 * s, base - 70 * s), (lx + 110 * s, base - 70 * s), (lx + 130 * s, base - 40 * s), (lx - 30 * s, base - 40 * s)])
    for gx in (tw * 0.04, tw * 0.94):                             # big gears / grands engrenages
        r = 70 * s
        for k in range(12):
            a = k * math.tau / 12
            steel.poly([(gx + math.cos(a - 0.12) * r, base - 160 * s + math.sin(a - 0.12) * r),
                        (gx + math.cos(a - 0.08) * (r + 18 * s), base - 160 * s + math.sin(a - 0.08) * (r + 18 * s)),
                        (gx + math.cos(a + 0.08) * (r + 18 * s), base - 160 * s + math.sin(a + 0.08) * (r + 18 * s)),
                        (gx + math.cos(a + 0.12) * r, base - 160 * s + math.sin(a + 0.12) * r)])
        steel.ellipse(gx - r, base - 160 * s - r, gx + r, base - 160 * s + r)
        dark.ellipse(gx - 20 * s, base - 180 * s, gx + 20 * s, base - 140 * s)
    for x in range(0, tw, int(240 * s)):                          # pipes and warning lamps / tuyaux et voyants
        dark.rect(x, base - 40 * s, x + 12 * s, base)
        blinks.append((x + 6 * s, base - 46 * s))
    dark.rect(-10, base - 18 * s, tw + 10, base - 10 * s)
    img = _layer(tw, h, [(steel, [(0, (90, 86, 90)), (1, (50, 46, 50))], (255, 150, 80), max(1, int(2 * s))),
                         (dark, [(0, (30, 28, 32)), (1, (20, 18, 22))], None, 1),
                         (hot, [(0, (255, 200, 90)), (1, (255, 110, 30))], None, 1)])
    layers.append({"img": img, "y": H - h - int(60 * s), "f": 0.0, "stage": "mid", "fires": fires, "pours": pours, "vents": vents,
                   "blinks": blinks})
    h = int(80 * s)
    c = Sil(tw, h, s)                                             # catwalk railing / garde-corps de la passerelle
    c.rect(-10, h * 0.2, tw + 10, h * 0.3)
    c.rect(-10, h * 0.62, tw + 10, h * 0.7)
    for x in range(0, tw, int(40 * s)):
        c.rect(x, h * 0.2, x + 5 * s, h)
    layers.append({"img": paint(c.mask(), [(0, (60, 56, 60)), (1, (30, 28, 30))], rim=(255, 160, 90), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(84 * s), "f": 0.0, "stage": "near"})
    amb = {"horizon": hz, "blink": (255, 60, 30), "hooks": {"mid": [hook_fires, hook_sparks, hook_steam]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ============================================================================ gothic manor under the moon / manoir gothique
def bat_img(s, up):
    def fn(d, W, H):
        col = (16, 10, 22, 255)
        d.ellipse([W * 0.42, H * 0.3, W * 0.58, H * 0.75], fill=col)
        wy = H * (0.05 if up else 0.85)
        for side in (-1, 1):
            cx = W / 2
            pts = [(cx, H * 0.45), (cx + side * W * 0.18, wy), (cx + side * W * 0.5, H * 0.3 if up else H * 0.6),
                   (cx + side * W * 0.38, H * 0.5), (cx + side * W * 0.28, H * 0.42), (cx + side * W * 0.16, H * 0.6)]
            d.polygon(pts, fill=col)
    return _img(34 * s, 16 * s, fn)


def hook_bats(bd, screen, b, L, now, dt):
    """Bats flying in loops in front of the moon. / Chauves-souris qui tournent devant la lune."""
    st = bd.amb_state.setdefault("_bats", None)
    W, s = bd.W, bd.s
    if st is None:
        st = bd.amb_state["_bats"] = [[bd.rng.uniform(0, W), bd.rng.uniform(40, 170) * s, bd.rng.uniform(0.6, 1.2), bd.rng.uniform(0, 6)]
                                      for _ in range(9)]
    for bt in st:
        bt[0] += (60 + 50 * bt[2]) * s * dt
        if bt[0] > W + 40 * s:
            bt[0], bt[1] = -40 * s, bd.rng.uniform(40, 170) * s
        flap = math.sin(now * 14 * bt[2] + bt[3])
        img = b["imgs"]["bat_up" if flap > 0 else "bat_down"]
        y = bt[1] + math.sin(now * 2.1 * bt[2] + bt[3]) * 22 * s
        screen.blit(img, (int(bt[0]), int(y)))


def build_gothic(W, H, s, seed=34):
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.68)
    sky = vgrad(W, H, [(0.0, (10, 6, 22)), (0.45, (40, 20, 60)), (0.66, (90, 40, 90)), (1.0, (30, 12, 34))])
    stars = stars_on(sky, rng, 60, H * 0.4, W)
    moon(sky, int(W * 0.5), int(H * 0.26), 78, s, color=(250, 236, 200), glow=(90, 50, 90))
    _clouds(sky, rng, 5, H * 0.08, H * 0.42, (40, 20, 50), 160, s)
    layers = [{"img": _hills(tw, int(180 * s), s, rng, 0.5, 40, 2, [(0, (36, 20, 50)), (1, (26, 14, 36))]),
               "y": hz - int(130 * s), "f": 0.0, "stage": "far"}]
    h = int(330 * s)
    base = h - 2
    c = Sil(tw, h, s)
    glass = Sil(tw, h, s)
    lights = []
    for (mx, w, top, n) in ((tw * 0.18, 220 * s, 250 * s, 3), (tw * 0.82, 200 * s, 230 * s, 2)):
        c.rect(mx - w / 2, base - top * 0.7, mx + w / 2, base)
        for k in range(n):                                        # spires / flèches
            sx = mx - w / 2 + (k + 0.5) * w / n
            c.rect(sx - 16 * s, base - top, sx + 16 * s, base - top * 0.66)
            c.poly([(sx - 22 * s, base - top), (sx, base - top - 90 * s), (sx + 22 * s, base - top)])
        for k in range(4):                                        # pointed windows / fenêtres en ogive
            wx = mx - w * 0.36 + k * w * 0.24
            glass.rect(wx - 9 * s, base - top * 0.52, wx + 9 * s, base - top * 0.3)
            glass.poly([(wx - 9 * s, base - top * 0.52), (wx, base - top * 0.6), (wx + 9 * s, base - top * 0.52)])
            lights.append((wx, base - top * 0.42))
        glass.ellipse(mx - 24 * s, base - top * 0.68 - 24 * s, mx + 24 * s, base - top * 0.68 + 24 * s)
    for x in (tw * 0.36, tw * 0.62):                              # dead trees / arbres morts
        c.line([(x, base), (x + 6 * s, base - 150 * s)], 12 * s)
        for k in range(5):
            y = base - (70 + k * 18) * s
            d_ = 1 if k % 2 else -1
            c.line([(x + 4 * s, y), (x + d_ * rng.uniform(40, 80) * s, y - rng.uniform(30, 60) * s)], 4 * s)
    img = _layer(tw, h, [(c, [(0, (24, 14, 32)), (1, (14, 8, 20))], (150, 110, 170), max(1, int(2 * s))),
                         (glass, [(0, (255, 190, 90)), (1, (200, 90, 140))], None, 1)])
    layers.append({"img": img, "y": H - h - int(50 * s), "f": 0.0, "stage": "mid", "lights": lights})
    h = int(100 * s)
    c = Sil(tw, h, s)                                             # iron fence and graves / grille et tombes
    c.rect(-10, h * 0.5, tw + 10, h * 0.56)
    for x in range(0, tw, int(26 * s)):
        c.rect(x, h * 0.3, x + 4 * s, h)
        c.poly([(x - 4 * s, h * 0.32), (x + 2 * s, h * 0.18), (x + 8 * s, h * 0.32)])
    for x in (tw * 0.1, tw * 0.3, tw * 0.55, tw * 0.75, tw * 0.9):
        c.rect(x, h * 0.42, x + 30 * s, h)
        c.ellipse(x, h * 0.3, x + 30 * s, h * 0.56)
    layers.append({"img": paint(c.mask(), [(0, (30, 20, 40)), (1, (12, 8, 16))], rim=(170, 130, 190), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(70 * s), "f": 0.0, "stage": "near"})
    amb = {"stars": stars, "horizon": hz, "window": (255, 170, 90), "lightning": True,
           "images": {"bat_up": bat_img(s, True), "bat_down": bat_img(s, False)}, "hooks": {"front": [hook_bats]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ============================================================================ Indian palace at sunset / palais indien
def elephant(c, x, base, s, d=1):
    """A big elephant seen from the side, trunk down. / Un éléphant de profil, la trompe pendante."""
    c.ellipse(x - 84 * s, base - 156 * s, x + 70 * s, base - 54 * s)                       # body / corps
    for lx in (-62, -34, 24, 50):
        c.rect(x + d * lx * s - 13 * s, base - 84 * s, x + d * lx * s + 13 * s, base)
    hx = x + d * 78 * s
    c.ellipse(hx - 40 * s, base - 176 * s, hx + 40 * s, base - 100 * s)                    # head / tête
    c.line([(hx + d * 30 * s, base - 128 * s), (hx + d * 46 * s, base - 84 * s), (hx + d * 44 * s, base - 40 * s),
            (hx + d * 54 * s, base - 26 * s)], 15 * s)                                      # trunk / trompe
    c.poly([(hx - d * 10 * s, base - 168 * s), (hx - d * 46 * s, base - 160 * s), (hx - d * 50 * s, base - 110 * s),
            (hx - d * 14 * s, base - 102 * s)])                                             # ear / oreille
    c.line([(x - d * 84 * s, base - 120 * s), (x - d * 98 * s, base - 80 * s)], 5 * s)     # tail / queue


def build_palace(W, H, s, seed=35):
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.66)
    sky = vgrad(W, H, [(0.0, (60, 40, 110)), (0.4, (200, 90, 110)), (0.6, (255, 160, 90)), (0.7, (255, 200, 120)), (1.0, (120, 60, 50))])
    add_at(sky, radial(int(380 * s), (110, 60, 20), 2.0), int(W * 0.5), int(hz - 30 * s))
    sun = Image.new("L", (int(120 * s), int(120 * s)), 0)
    ImageDraw.Draw(sun).ellipse([0, 0, sun.width - 1, sun.height - 1], fill=255)
    sky.paste((255, 226, 160), (int(W * 0.5 - 60 * s), int(hz - 110 * s)), sun)
    far = Sil(tw, int(200 * s), s)
    for x in range(0, tw, int(140 * s)):
        palm(far, x + rng.uniform(0, 80) * s, 200 * s, rng.uniform(110, 170) * s, s, rng)
    layers = [{"img": paint(far.mask(), [(0, (90, 40, 60)), (1, (70, 30, 50))]), "y": hz - int(170 * s), "f": 0.0, "stage": "far"}]
    h = int(330 * s)
    base = h - 2
    stone, domes, cloth, dark = Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s)
    torches = []
    px = tw * 0.5
    stone.rect(px - 260 * s, base - 170 * s, px + 260 * s, base)
    domes.ellipse(px - 110 * s, base - 300 * s, px + 110 * s, base - 140 * s)          # the big onion dome / le grand bulbe
    domes.poly([(px - 18 * s, base - 296 * s), (px, base - 330 * s), (px + 18 * s, base - 296 * s)])
    for mx in (px - 210 * s, px + 210 * s):                       # small pavilions / petits kiosques
        stone.rect(mx - 26 * s, base - 240 * s, mx + 26 * s, base - 160 * s)
        domes.ellipse(mx - 34 * s, base - 286 * s, mx + 34 * s, base - 226 * s)
    for k in range(7):                                            # arches / arcades
        ax = px - 225 * s + k * 75 * s
        dark.rect(ax - 20 * s, base - 110 * s, ax + 20 * s, base)
        dark.ellipse(ax - 20 * s, base - 130 * s, ax + 20 * s, base - 90 * s)
        torches.append((ax + 37 * s, base - 120 * s))
    grey = Sil(tw, h, s)
    for (ex, d) in ((tw * 0.13, 1), (tw * 0.87, -1)):
        elephant(grey, ex, base, s, d)
        cloth.poly([(ex - 46 * s, base - 146 * s), (ex + 40 * s, base - 146 * s), (ex + 34 * s, base - 96 * s), (ex - 40 * s, base - 96 * s)])
        cloth.rect(ex - 22 * s, base - 170 * s, ex + 16 * s, base - 146 * s)
        cloth.poly([(ex - 26 * s, base - 170 * s), (ex - 3 * s, base - 196 * s), (ex + 20 * s, base - 170 * s)])
    img = _layer(tw, h, [(stone, [(0, (230, 190, 160)), (1, (170, 120, 100))], (255, 230, 190), max(1, int(2 * s))),
                         (domes, [(0, (250, 236, 220)), (1, (220, 180, 160))], (255, 250, 230), max(1, int(2 * s))),
                         (dark, [(0, (80, 40, 40)), (1, (50, 24, 30))], None, 1),
                         (grey, [(0, (128, 116, 126)), (1, (86, 76, 86))], (255, 200, 170), max(1, int(2 * s))),
                         (cloth, [(0, (200, 40, 80)), (1, (150, 20, 60))], (255, 210, 90), max(1, int(3 * s)))])
    layers.append({"img": img, "y": H - h - int(128 * s), "f": 0.0, "stage": "mid", "torches": torches})
    h = int(80 * s)
    c = Sil(tw, h, s)                                             # balustrade
    c.rect(-10, h * 0.2, tw + 10, h * 0.32)
    c.rect(-10, h * 0.8, tw + 10, h)
    for x in range(0, tw, int(30 * s)):
        c.ellipse(x, h * 0.3, x + 16 * s, h * 0.84)
    layers.append({"img": paint(c.mask(), [(0, (200, 150, 120)), (1, (120, 80, 70))], rim=(255, 220, 170), rim_px=max(1, int(2 * s))),
                   "y": H - h - int(46 * s), "f": 0.0, "stage": "near"})
    amb = {"horizon": hz, "images": {"gull_up": gull_img(s, True), "gull_down": gull_img(s, False)},
           "hooks": {"mid": [hook_torches], "front": [hook_gulls]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ============================================================================ golden temple on the river, Thailand / temple d'or
def chedi(c, x, base, w, h, s):
    """A bell-shaped golden tower with its spire. / Une tour dorée en cloche et sa flèche."""
    c.rect(x - w * 0.5, base - h * 0.12, x + w * 0.5, base)
    c.rect(x - w * 0.4, base - h * 0.2, x + w * 0.4, base - h * 0.1)
    c.poly([(x - w * 0.36, base - h * 0.2), (x - w * 0.3, base - h * 0.38), (x - w * 0.16, base - h * 0.48), (x + w * 0.16, base - h * 0.48),
            (x + w * 0.3, base - h * 0.38), (x + w * 0.36, base - h * 0.2)])
    for k in range(6):
        y = base - h * (0.5 + k * 0.07)
        r = w * (0.12 - k * 0.016)
        c.ellipse(x - r, y - h * 0.04, x + r, y + h * 0.02)
    c.poly([(x - w * 0.03, base - h * 0.88), (x, base - h), (x + w * 0.03, base - h * 0.88)])


def sky_lantern_img(s):
    def fn(d, W, H):
        d.polygon([(W * 0.12, 0), (W * 0.88, 0), (W, H * 0.85), (0, H * 0.85)], fill=(255, 196, 110, 255))
        d.polygon([(W * 0.3, H * 0.1), (W * 0.7, H * 0.1), (W * 0.78, H * 0.75), (W * 0.22, H * 0.75)], fill=(255, 236, 170, 255))
        d.rectangle([W * 0.2, H * 0.85, W * 0.8, H], fill=(120, 60, 30, 255))
    return _img(16 * s, 20 * s, fn)


def hook_sky_lanterns(bd, screen, b, L, now, dt):
    """Paper lanterns rising slowly into the evening sky. / Lanternes de papier qui montent lentement dans le ciel du soir."""
    st = bd.amb_state.setdefault("_skyl", None)
    W, H, s = bd.W, bd.H, bd.s
    if st is None:
        st = bd.amb_state["_skyl"] = [[bd.rng.uniform(0, W), bd.rng.uniform(40, H * 0.6), bd.rng.uniform(0.5, 1.0), bd.rng.uniform(0, 6)]
                                      for _ in range(14)]
    img = b["imgs"]["sky_lantern"]
    add = bd.pg.BLEND_RGB_ADD
    for p in st:
        p[1] -= (8 + 10 * p[2]) * s * dt
        p[0] += math.sin(now * 0.5 + p[3]) * 6 * s * dt
        if p[1] < -30 * s:
            p[0], p[1] = bd.rng.uniform(0, W), H * 0.62
        k = max(0.35, min(1.0, p[1] / (H * 0.5)))
        x, y = int(p[0]), int(p[1])
        g = bd.fx.sp.glow(16 * s * p[2], (255, 150, 60), 5 + 3 * math.sin(now * 3 + p[3]), hot=0.3)
        screen.blit(g, (x - g.get_width() // 2 + img.get_width() // 2, y - g.get_height() // 2 + img.get_height() // 2), special_flags=add)
        if k > 0.4:
            screen.blit(img, (x, y))


def build_thai(W, H, s, seed=36):
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.62)
    sky = vgrad(W, H, [(0.0, (40, 30, 90)), (0.35, (150, 70, 120)), (0.55, (255, 150, 90)), (0.62, (255, 210, 130)), (0.63, (120, 70, 90)),
                       (1.0, (40, 30, 60))])
    sun_x = int(W * 0.7)
    add_at(sky, radial(int(300 * s), (120, 60, 20), 2.0), sun_x, hz - int(40 * s))
    sun = Image.new("L", (int(90 * s), int(90 * s)), 0)
    ImageDraw.Draw(sun).ellipse([0, 0, sun.width - 1, sun.height - 1], fill=255)
    sky.paste((255, 230, 170), (int(sun_x - 45 * s), int(hz - 110 * s)), sun)
    far = Sil(tw, int(180 * s), s)
    for x in range(0, tw, int(170 * s)):
        palm(far, x + rng.uniform(0, 90) * s, 180 * s, rng.uniform(90, 150) * s, s, rng)
    layers = [{"img": paint(far.mask(), [(0, (70, 40, 80)), (1, (50, 30, 60))]), "y": hz - int(160 * s), "f": 0.0, "stage": "far"}]
    h = int(300 * s)
    base = h - int(40 * s)
    gold, roofs, white = Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s)
    for (x, w, ch) in ((tw * 0.3, 150 * s, 270 * s), (tw * 0.15, 90 * s, 170 * s), (tw * 0.45, 90 * s, 170 * s), (tw * 0.86, 110 * s, 210 * s)):
        chedi(gold, x, base, w, ch, s)
    tx = tw * 0.66                                                # the temple hall and its steep roofs / la salle et ses toits
    white.rect(tx - 120 * s, base - 90 * s, tx + 120 * s, base)
    for k, (rw, ry) in enumerate(((150, 90), (120, 140), (84, 186))):
        roofs.poly([(tx - rw * s, base - (ry - 14) * s), (tx, base - (ry + 50) * s), (tx + rw * s, base - (ry - 14) * s)])
        gold.line([(tx - rw * s, base - (ry - 14) * s), (tx, base - (ry + 50) * s), (tx + rw * s, base - (ry - 14) * s)], 4 * s)
        for d in (-1, 1):                                         # horn finials / cornes dorées
            gold.line([(tx + d * rw * s, base - (ry - 14) * s), (tx + d * (rw + 14) * s, base - (ry + 6) * s)], 4 * s)
    gold.poly([(tx - 4 * s, base - 236 * s), (tx, base - 280 * s), (tx + 4 * s, base - 236 * s)])
    for k in range(5):
        white.rect(tx - 100 * s + k * 50 * s, base - 80 * s, tx - 92 * s + k * 50 * s, base)
    white.rect(-10, base, tw + 10, base + 10 * s)
    img = _layer(tw, h, [(white, [(0, (240, 220, 200)), (1, (190, 160, 150))], None, 1),
                         (roofs, [(0, (190, 40, 40)), (1, (130, 20, 30))], None, 1),
                         (gold, [(0, (255, 220, 110)), (1, (220, 150, 50))], (255, 250, 200), max(1, int(2 * s)))])
    reflect = img.crop((0, 0, tw, base)).transpose(Image.FLIP_TOP_BOTTOM).resize((tw, int(base * 0.35)))
    rf = Image.new("RGBA", reflect.size, (0, 0, 0, 0))
    rf = Image.blend(rf, reflect, 0.32)
    img.alpha_composite(rf, (0, base + int(10 * s)))
    layers.append({"img": img, "y": hz - base, "f": 0.0, "stage": "mid"})
    amb = {"horizon": hz, "sun_x": sun_x, "images": {"sky_lantern": sky_lantern_img(s), "gull_up": gull_img(s, True),
                                                     "gull_down": gull_img(s, False)},
           "hooks": {"far": [hook_glints], "sky": [hook_sky_lanterns], "front": [hook_gulls]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ============================================================================ laboratory / laboratoire
def hook_tanks(bd, screen, b, L, now, dt):
    """Bubbles rising in the glowing tanks, screens that flicker. / Bulles dans les cuves, écrans qui clignotent."""
    add = bd.pg.BLEND_RGB_ADD
    sp = bd.fx.sp
    x0 = bd._layer_x(L, b["tw"])
    for i, (x, y0, y1) in enumerate(L.get("tanks", ())):
        for k in range(5):
            ph = (now * (0.35 + 0.1 * k) + k * 0.23 + i * 0.37) % 1.0
            yy = L["y"] + y1 - (y1 - y0) * ph
            xx = x0 + x + math.sin(now * 3 + k * 2 + i) * 10 * bd.s
            g = sp.glow((5 + k % 3 * 2) * bd.s, (140, 255, 190), 7, hot=0.8)
            screen.blit(g, (int(xx - g.get_width() / 2), int(yy - g.get_height() / 2)), special_flags=add)
    for i, (x, y, w) in enumerate(L.get("screens", ())):
        lv = 3 + 2 * math.sin(now * 7 + i * 2) + (3 if int(now * 4 + i) % 9 == 0 else 0)
        g = sp.glow(w * 0.5, (80, 200, 255), lv, hot=0.1)
        screen.blit(g, (int(x0 + x - g.get_width() / 2), int(L["y"] + y - g.get_height() / 2)), special_flags=add)


def build_lab(W, H, s, seed=37):
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.7)
    sky = vgrad(W, H, [(0.0, (8, 14, 26)), (0.5, (16, 40, 60)), (1.0, (10, 20, 30))])
    d = ImageDraw.Draw(sky)
    r = 40 * s                                                    # hexagon wall / mur d'hexagones
    for j in range(int(H * 0.7 / (r * 1.5)) + 1):
        for i in range(int(W / (r * 1.74)) + 2):
            cx = i * r * 1.74 + (j % 2) * r * 0.87
            cy = j * r * 1.5
            pts = [(cx + math.cos(math.radians(60 * k + 30)) * r * 0.92, cy + math.sin(math.radians(60 * k + 30)) * r * 0.92) for k in range(6)]
            lv = rng.random()
            d.polygon(pts, outline=(30, 90, 120) if lv > 0.2 else (60, 160, 200), fill=(14, 34, 50) if lv > 0.08 else (30, 80, 110))
    layers = []
    h = int(330 * s)
    base = h - 2
    metal, glass, dark, screen_s = Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s)
    tanks, screens, blinks, lights = [], [], [], []
    for x in (tw * 0.12, tw * 0.3, tw * 0.7, tw * 0.88):          # glass tanks / cuves de verre
        metal.rect(x - 50 * s, base - 40 * s, x + 50 * s, base)
        metal.rect(x - 50 * s, base - 250 * s, x + 50 * s, base - 226 * s)
        glass.rect(x - 40 * s, base - 226 * s, x + 40 * s, base - 40 * s)
        tanks.append((x, base - 220 * s, base - 50 * s))
        blinks.append((x - 30 * s, base - 20 * s))
    for k in range(3):                                            # screens in the middle / écrans au milieu
        sx = tw * 0.42 + k * 100 * s
        metal.rect(sx - 46 * s, base - 260 * s, sx + 46 * s, base - 170 * s)
        screen_s.rect(sx - 40 * s, base - 254 * s, sx + 40 * s, base - 176 * s)
        screens.append((sx, base - 215 * s, 160 * s))
    metal.rect(tw * 0.38, base - 120 * s, tw * 0.62 + 30 * s, base)
    for k in range(10):
        lights.append((tw * 0.4 + k * 26 * s, base - 100 * s))
    for x in range(0, tw, int(180 * s)):                          # pipes on the ceiling / tuyaux au plafond
        dark.rect(x, 0, x + 16 * s, base - 260 * s)
    dark.rect(-10, 0, tw + 10, 26 * s)
    img = _layer(tw, h, [(metal, [(0, (90, 110, 130)), (1, (50, 60, 76))], (160, 230, 255), max(1, int(2 * s))),
                         (glass, [(0, (40, 160, 120)), (1, (20, 90, 80))], (200, 255, 230), max(1, int(2 * s))),
                         (dark, [(0, (20, 30, 40)), (1, (14, 20, 30))], None, 1),
                         (screen_s, [(0, (30, 90, 140)), (1, (20, 60, 100))], None, 1)])
    dd = ImageDraw.Draw(img)
    for (sx, sy, w) in screens:                                   # curves on the screens / courbes sur les écrans
        pts = [(sx - 36 * s + k * 6 * s, sy + math.sin(k * 0.9 + sx) * 18 * s) for k in range(13)]
        dd.line(pts, fill=(140, 255, 200, 255), width=max(1, int(2 * s)))
    layers.append({"img": img, "y": H - h - int(60 * s), "f": 0.0, "stage": "mid", "tanks": tanks, "screens": screens, "blinks": blinks,
                   "lights": lights})
    h = int(70 * s)
    c = Sil(tw, h, s)                                             # yellow and black edge of the floor / bord du sol rayé
    c.rect(-10, h * 0.3, tw + 10, h)
    stripes = Sil(tw, h, s)
    for x in range(0, tw, int(40 * s)):
        stripes.poly([(x, h * 0.3), (x + 20 * s, h * 0.3), (x + 34 * s, h * 0.5), (x + 14 * s, h * 0.5)])
    layers.append({"img": _layer(tw, h, [(c, [(0, (50, 60, 70)), (1, (24, 28, 34))], (160, 230, 255), max(1, int(2 * s))),
                                         (stripes, [(0, (240, 200, 40)), (1, (200, 160, 30))], None, 1)]),
                   "y": H - h - int(84 * s), "f": 0.0, "stage": "near"})
    amb = {"horizon": hz, "window": (120, 220, 255), "blink": (255, 60, 40), "hooks": {"mid": [hook_tanks]}}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


# ============================================================================ air base at dusk / base aérienne au crépuscule
def jet(c, x, base, s, d=1):
    """A fighter jet of our own seen from the side, on the tarmac. / Un avion de chasse à nous, de profil, sur le tarmac."""
    c.poly([(x - d * 150 * s, base - 46 * s), (x + d * 120 * s, base - 52 * s), (x + d * 170 * s, base - 44 * s), (x + d * 120 * s, base - 34 * s),
            (x - d * 150 * s, base - 30 * s)])                                              # fuselage
    c.poly([(x + d * 100 * s, base - 50 * s), (x + d * 70 * s, base - 64 * s), (x + d * 40 * s, base - 50 * s)])   # canopy / verrière
    c.poly([(x - d * 40 * s, base - 40 * s), (x - d * 110 * s, base - 40 * s), (x - d * 70 * s, base - 22 * s)])   # wing / aile
    c.poly([(x - d * 110 * s, base - 46 * s), (x - d * 150 * s, base - 46 * s), (x - d * 160 * s, base - 100 * s), (x - d * 136 * s, base - 100 * s)])
    for wx in (x + d * 90 * s, x - d * 70 * s):                                            # wheels / roues
        c.line([(wx, base - 32 * s), (wx, base - 8 * s)], 4 * s)
        c.ellipse(wx - 8 * s, base - 14 * s, wx + 8 * s, base)


def build_airbase(W, H, s, seed=38):
    rng = random.Random(seed)
    tw = W
    hz = int(H * 0.64)
    sky = vgrad(W, H, [(0.0, (30, 40, 90)), (0.4, (90, 100, 150)), (0.58, (250, 160, 110)), (0.66, (255, 200, 140)), (1.0, (70, 60, 70))])
    _clouds(sky, rng, 6, H * 0.08, H * 0.4, (255, 190, 170), 120, s)
    layers = [{"img": _hills(tw, int(160 * s), s, rng, 0.6, 30, 2, [(0, (90, 80, 120)), (1, (70, 64, 96))]),
               "y": hz - int(110 * s), "f": 0.0, "stage": "far"}]
    h = int(300 * s)
    base = h - 2
    hangar, doors, metal = Sil(tw, h, s), Sil(tw, h, s), Sil(tw, h, s)
    lights, blinks = [], []
    for hx in (tw * 0.14, tw * 0.4, tw * 0.86):                   # hangars with round roofs / hangars au toit rond
        hangar.ellipse(hx - 150 * s, base - 200 * s, hx + 150 * s, base + 100 * s)
        doors.rect(hx - 90 * s, base - 110 * s, hx + 90 * s, base)
        for k in range(5):
            lights.append((hx - 72 * s + k * 36 * s, base - 120 * s))
    tx = tw * 0.62                                                # control tower / tour de contrôle
    metal.rect(tx - 16 * s, base - 200 * s, tx + 16 * s, base)
    metal.poly([(tx - 46 * s, base - 200 * s), (tx + 46 * s, base - 200 * s), (tx + 36 * s, base - 250 * s), (tx - 36 * s, base - 250 * s)])
    metal.rect(tx - 40 * s, base - 260 * s, tx + 40 * s, base - 250 * s)
    metal.line([(tx, base - 260 * s), (tx, base - 296 * s)], 3 * s)
    blinks.append((tx, base - 296 * s))
    for k in range(4):
        lights.append((tx - 27 * s + k * 18 * s, base - 226 * s))
    jet(metal, tw * 0.26, base, s, 1)
    jet(metal, tw * 0.74, base, s, -1)
    metal.rect(-10, base - 8 * s, tw + 10, base)
    for x in range(int(30 * s), tw, int(120 * s)):
        blinks.append((x, base - 12 * s))
    img = _layer(tw, h, [(hangar, [(0, (110, 110, 120)), (1, (70, 70, 80))], (255, 200, 150), max(1, int(2 * s))),
                         (doors, [(0, (40, 40, 48)), (1, (24, 24, 30))], None, 1),
                         (metal, [(0, (96, 104, 104)), (1, (54, 60, 62))], (255, 210, 160), max(1, int(2 * s)))])
    layers.append({"img": img, "y": H - h - int(104 * s), "f": 0.0, "stage": "mid", "lights": lights, "blinks": blinks})
    amb = {"horizon": hz, "window": (255, 220, 160), "blink": (255, 70, 40), "plane": "bomber", "plane_color": (40, 40, 60)}
    return {"sky": sky, "layers": layers, "tw": tw, "amb": amb}


LOOKS = {"castle": build_castle, "market": build_market, "factory": build_factory, "gothic": build_gothic, "palace": build_palace,
         "thai": build_thai, "lab": build_lab, "airbase": build_airbase}
hd_bg.BUILDERS.update(LOOKS)
for _name in LOOKS:
    hd_bg.BUILDERS["fight_" + _name] = with_crowd(LOOKS[_name])
hd_bg.BUILDERS["fight_base"] = hd_bg.BUILDERS["fight_airbase"]           # the air base of the fights / la base des combats

CPS_STAGES = tuple("fight_" + n for n in LOOKS)                    # names of these fight stages / noms de ces décors de combat
