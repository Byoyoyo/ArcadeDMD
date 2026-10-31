"""Twinkle Star Sprites on the HD screen (1.30.1), redone with Seb for a friend who plays it in competitions: two fields
side by side as in the game, a header that reads from afar (the name on a plate in the character's colours, the score,
five big hearts with the half ones, POW 1 2 MAX, the bombs) and big moments for what the game does: chains, fireballs
crossing the column, charged shots, bombs, boss attacks, hearts lost or given back, K.O. The witches, the puffballs and
the boss creature are creations of the program in the spirit of the game.

Twinkle Star Sprites sur l'écran HD (1.30.1), refait avec Seb pour un ami qui y joue en compétition : deux terrains côte
à côte comme dans le jeu, un bandeau lisible de loin et de grands moments pour ce que fait le jeu. Les sorcières, les
boules et la créature du boss sont des créations du programme dans l'esprit du jeu.
"""

import math
import os
import threading

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .hd_games import AMBER, WHITE, GameScene, _clamp, _mix, _n, draw_img
from .hd_themes4 import ts_fields, ts_forest_tile


TS_LOOKS = (((70, 90, 220), (150, 90, 210), (250, 220, 120)), ((230, 80, 80), (250, 170, 60), (120, 70, 40)),
            ((60, 150, 90), (240, 240, 240), (230, 200, 120)), ((240, 120, 170), (250, 210, 230), (60, 40, 30)),
            ((90, 70, 140), (60, 60, 90), (240, 240, 240)), ((40, 170, 200), (250, 230, 120), (250, 140, 60)))


def witch_draw(hat, dress, hair, frame):
    """A little witch of our own on her broom, seen from above as she flies up the field: a big pointed hat with a
    star, a cape that flutters, the broom and its bristles. / Une petite sorcière à nous sur son balai, vue de haut."""
    def fn(d, W, H):
        dark = (30, 20, 40, 255)
        ow = max(1.0, W * 0.025)
        d.line([(W * 0.5, H * 0.18), (W * 0.5, H * 0.86)], fill=(150, 100, 50, 255), width=max(2, int(W * 0.07)))     # le balai
        d.polygon([(W * 0.5, H * 0.78), (W * 0.3, H * 0.99), (W * 0.7, H * 0.99)], fill=(230, 190, 90, 255), outline=dark)
        for k in (0.38, 0.5, 0.62):
            d.line([(W * 0.5, H * 0.8), (W * k, H * 0.98)], fill=(180, 130, 50, 255), width=max(1, int(ow)))
        flap = 0.05 if frame == 1 else 0.0
        d.polygon([(W * 0.5, H * 0.34), (W * (0.12 - flap), H * 0.8), (W * 0.5, H * 0.7), (W * (0.88 + flap), H * 0.8)],
                  fill=_mix(dress, (0, 0, 0), 0.3) + (255,), outline=dark)          # la cape
        d.ellipse([W * 0.3, H * 0.36, W * 0.7, H * 0.7], fill=dress + (255,), outline=dark, width=int(ow))                     # la robe
        for sx in (0.22, 0.78):                                        # les mains sur le manche
            d.ellipse([W * (sx - 0.08), H * 0.42, W * (sx + 0.08), H * 0.52], fill=(250, 220, 190, 255), outline=dark, width=int(ow))
        d.ellipse([W * 0.32, H * 0.22, W * 0.68, H * 0.46], fill=hair + (255,), outline=dark, width=int(ow))                  # la tête
        d.ellipse([W * 0.1, H * 0.2, W * 0.9, H * 0.36], fill=hat + (255,), outline=dark, width=int(ow))                      # le chapeau
        d.polygon([(W * 0.3, H * 0.28), (W * 0.7, H * 0.28), (W * 0.58, H * 0.02)], fill=hat + (255,), outline=dark)
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = (0.09 if i % 2 == 0 else 0.04) * W
            pts.append((W * 0.5 + math.cos(a) * rr, H * 0.25 + math.sin(a) * rr))
        d.polygon(pts, fill=(255, 230, 90, 255))
    return fn


def puff_draw(color):
    """A puffball of the sky with little wings. / Une boule duveteuse du ciel, à petites ailes."""
    def fn(d, W, H):
        dark = (40, 30, 60, 255)
        for sx in (0.12, 0.88):
            d.ellipse([W * (sx - 0.14), H * 0.26, W * (sx + 0.14), H * 0.56], fill=(250, 250, 255, 255), outline=dark, width=max(1, int(W * 0.03)))
        d.ellipse([W * 0.14, H * 0.12, W * 0.86, H * 0.9], fill=color + (255,), outline=dark, width=max(1, int(W * 0.04)))
        d.ellipse([W * 0.26, H * 0.2, W * 0.48, H * 0.36], fill=_mix(color, (255, 255, 255), 0.6) + (255,))
        for x in (0.38, 0.62):
            d.ellipse([W * (x - 0.07), H * 0.42, W * (x + 0.07), H * 0.62], fill=dark)
            d.ellipse([W * (x - 0.03), H * 0.44, W * x, H * 0.5], fill=(255, 255, 255, 255))
        d.arc([W * 0.4, H * 0.56, W * 0.6, H * 0.74], 20, 160, fill=dark, width=max(1, int(W * 0.03)))
    return fn


def boss_draw(d, W, H):
    """The big creature of a boss attack: a giant crowned cloud with a grin. / Le gros nuage couronné d'une attaque."""
    dark = (40, 20, 60, 255)
    for cx, cy, r in ((0.3, 0.55, 0.26), (0.7, 0.55, 0.26), (0.5, 0.45, 0.34), (0.5, 0.7, 0.28)):
        d.ellipse([W * (cx - r), H * (cy - r), W * (cx + r), H * (cy + r)], fill=(190, 150, 240, 255), outline=dark, width=max(1, int(W * 0.015)))
    d.polygon([(W * 0.32, H * 0.16), (W * 0.38, H * 0.02), (W * 0.44, H * 0.12), (W * 0.5, H * 0.0), (W * 0.56, H * 0.12), (W * 0.62, H * 0.02),
               (W * 0.68, H * 0.16)], fill=(255, 210, 60, 255), outline=dark)
    for x in (0.4, 0.6):
        d.ellipse([W * (x - 0.06), H * 0.38, W * (x + 0.06), H * 0.56], fill=(255, 255, 255, 255), outline=dark, width=max(1, int(W * 0.01)))
        d.ellipse([W * (x - 0.025), H * 0.44, W * (x + 0.03), H * 0.54], fill=dark)
    d.chord([W * 0.36, H * 0.52, W * 0.64, H * 0.76], 0, 180, fill=(120, 30, 60, 255), outline=dark)


# ---------------------------------------------------------------------------- pictures of the new header and effects
TS_PLATES = (((70, 110, 250), (140, 80, 230)), ((250, 140, 40), (250, 210, 60)), ((70, 120, 255), (150, 80, 230)),
             ((230, 60, 60), (250, 150, 60)), ((40, 170, 110), (40, 190, 190)), ((240, 90, 170), (160, 80, 230)),
             ((30, 170, 200), (90, 220, 240)), ((170, 100, 50), (240, 160, 60)), ((255, 90, 150), (255, 160, 70)),
             ((250, 200, 60), (250, 110, 170)), ((90, 40, 130), (40, 30, 80)), ((150, 160, 190), (80, 120, 220)),
             ((210, 200, 240), (150, 130, 230)))
TS_FONTS = {"logo": "InterDisplay-BlackItalic.otf", "black": "Inter-Black.otf"}
TS_FALLBACK = ("C:\\Windows\\Fonts\\arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
TS_INK = (34, 10, 44, 255)            # outline of the big texts / contour des grands textes


def ts_font(root, key, size):
    for p in [os.path.join(root or "", "fonts", TS_FONTS.get(key, TS_FONTS["black"]))] + list(TS_FALLBACK):
        try:
            return ImageFont.truetype(p, max(6, int(size)))
        except OSError:
            continue
    return ImageFont.load_default()


def ts_banner(root, text, size, top, bottom, stroke, glow=None, key="logo"):
    """A big text with a gradient from top to bottom, a dark outline and a soft glow, in a tight picture.
    / Un grand texte en dégradé, contour sombre, halo doux."""
    f = ts_font(root, key, size)
    pad = stroke + (max(4, int(size * 0.3)) if glow else 4)
    l, t, r, b = f.getbbox(text, stroke_width=stroke)
    w, h = int(r - l + 2 * pad), int(b - t + 2 * pad)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    xy = (pad - l, pad - t)
    if glow:
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text(xy, text, font=f, fill=glow, stroke_width=stroke + max(2, int(size / 12)), stroke_fill=glow)
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(max(2, size / 10))))
    ImageDraw.Draw(img).text(xy, text, font=f, fill=TS_INK, stroke_width=stroke, stroke_fill=TS_INK)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text(xy, text, font=f, fill=255)
    box = mask.getbbox() or (0, 0, w, h)
    grad = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(grad)
    for y in range(h):
        k = _clamp((y - box[1]) / max(1, box[3] - box[1]))
        gd.line([(0, y), (w, y)], fill=tuple(int(a + (c - a) * k) for a, c in zip(top, bottom)) + (255,))
    img.paste(grad, (0, 0), mask)
    return img


def ts_heart_pts(cx, cy, r):
    pts = []
    for i in range(48):
        a = i / 48 * math.tau
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * r / 17, cy + y * r / 17))
    return pts


def ts_heart(r, kind):
    """A heart of the header: "full", "half" or "empty". / Un cœur du bandeau : plein, demi ou vide."""
    def fn(d, W, H):
        rr = W * 0.42
        pts = ts_heart_pts(W / 2, H * 0.5, rr)
        d.polygon(pts, fill=(70, 40, 76, 255))
        if kind == "full":
            d.polygon(pts, fill=(255, 60, 110, 255))
        elif kind == "half":
            d.polygon([p for p in pts if p[0] <= W / 2] + [(W / 2, H * 0.5 + rr * 0.95), (W / 2, H * 0.5 - rr * 0.3)], fill=(255, 60, 110, 255))
        if kind != "empty":
            d.ellipse([W / 2 - rr * 0.55, H * 0.5 - rr * 0.52, W / 2 - rr * 0.2, H * 0.5 - rr * 0.2], fill=(255, 220, 230, 235))
        d.polygon(pts, outline=(60, 10, 30, 255), width=max(2, int(W * 0.06)))
    return fn


def ts_orb(live):
    """A bomb of the header, a blue B orb (grey once used). / Une bombe du bandeau, une boule B bleue."""
    def fn(d, W, H):
        d.ellipse([W * 0.04, H * 0.04, W * 0.96, H * 0.96], fill=(40, 70, 220, 255) if live else (44, 44, 64, 220),
                  outline=(220, 235, 255, 255) if live else (120, 120, 140, 220), width=max(2, int(W * 0.07)))
        if live:
            d.ellipse([W * 0.22, H * 0.16, W * 0.5, H * 0.38], fill=(150, 190, 255, 255))
    return fn


def ts_plate(root, w, h, c1, c2, name, tag, right):
    """The name plate of a player: a ribbon in his character's colours, a gold edge, the 1P or 2P medal and the name
    in big white letters. / La plaque du nom : un ruban aux couleurs du personnage, le médaillon 1P ou 2P, le nom."""
    ss = 2
    W, H = w * ss, h * ss
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band = Image.new("RGBA", (W, H))
    bd = ImageDraw.Draw(band)
    for x in range(W):
        k = x / max(1, W - 1)
        k = 1 - k if right else k
        bd.line([(x, 0), (x, H)], fill=tuple(int(a + (b - a) * k) for a, b in zip(c1, c2)) + (238,))
    mask = Image.new("L", (W, H), 0)
    top, bot = int(H * 0.06), int(H * 0.94)
    ImageDraw.Draw(mask).rounded_rectangle([0, top, W - 1, bot], radius=(bot - top) // 2, fill=255)
    img.paste(band, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, top, W - 1, bot], radius=(bot - top) // 2, outline=(255, 214, 80, 255), width=3 * ss)
    r = H * 0.5
    cx = W - r if right else r
    d.ellipse([cx - r + ss, ss, cx + r - ss, H - ss], fill=(255, 226, 110, 255), outline=(120, 60, 10, 255), width=3 * ss)
    f = ts_font(root, "black", H * (0.42 if len(tag) <= 2 else 0.3))
    d.text((cx, H / 2), tag, font=f, fill=(90, 30, 10, 255), anchor="mm")
    room = W - 2 * r - 40 * ss
    size = H * 0.6
    f = ts_font(root, "black", size)
    while f.getlength(name) > room and size > H * 0.3:                 # a long name shrinks / un long nom rapetisse
        size *= 0.92
        f = ts_font(root, "black", size)
    nx = (W - 2 * r - 14 * ss) if right else (2 * r + 14 * ss)
    d.text((nx, H / 2), name, font=f, fill=(255, 255, 255, 255), anchor="rm" if right else "lm", stroke_width=max(2, int(size / 9)),
           stroke_fill=(30, 10, 40, 255))
    return img.resize((w, h), Image.LANCZOS)


def ts_beam(w, h):
    """The light of a charged shot, from the witch up to the sky. / La lumière d'un tir chargé, de la sorcière au ciel."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(w * 0.38, h), (w * 0.62, h), (w * 0.9, 0), (w * 0.1, 0)], fill=(255, 250, 210, 210))
    d.polygon([(w * 0.46, h), (w * 0.54, h), (w * 0.62, 0), (w * 0.38, 0)], fill=(255, 255, 255, 255))
    return img.filter(ImageFilter.GaussianBlur(max(2, w / 16)))


def ts_burst(r, outer, inner, n=12):
    """A starburst behind a chain counter. / L'éclat derrière un compteur de chaîne."""
    def fn(d, W, H):
        for col, k, rot in ((outer, 1.0, 0.0), (inner, 0.76, math.pi / n)):
            pts = []
            for i in range(n * 2):
                a = rot + i * math.pi / n
                rr = (W / 2) * k * (1.0 if i % 2 == 0 else 0.62)
                pts.append((W / 2 + math.cos(a) * rr, H / 2 + math.sin(a) * rr))
            d.polygon(pts, fill=col + (235,))
    return fn


def ts_star_pts(cx, cy, r, rot=0.0, inner=0.45):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + rot + i * math.pi / 5
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


class TwinkleScene(GameScene):
    """Twinkle Star Sprites as in the game: two fields side by side, each with a forest seen from above that scrolls
    down, separated by the ornate column; in each one a little witch of our own shoots the puffballs that come down.
    At the top of each field the name in big letters on a plate in the character's colours, the score, five big hearts
    (half ones too, the game's energy); at the bottom POW 1 2 MAX and the bombs. Big moments, from the values read in
    the game: chains that grow, fireballs that cross the column (with !! where they land), the charged shot that leaves
    as a beam of light (1, 2 or MAX !), a bomb that flashes the field with rings of stars and BOMB !, a boss attack
    that darkens the other field with BOSS ATTACK !, a heart that breaks or comes back, K.O. and WIN ! with fireworks.
    / Deux terrains côte à côte, comme dans le jeu, et les grands moments lus dans le jeu."""
    THEME = "ts_frame"
    STATIC = True
    SHADE = (150, 130)
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS
    ATTACKS = {1: "LV1", 2: "LV2", 3: "BOSS"}
    BIG = (("bomb", "BOMB !", 128, (255, 255, 255), (255, 200, 90), (255, 120, 200, 170)),
           ("boss", "BOSS ATTACK !", 88, (255, 255, 255), (255, 110, 200), (255, 60, 160, 170)),
           ("ko", "K.O.", 170, (255, 240, 200), (255, 60, 60), (255, 40, 40, 170)),
           ("win", "WIN !", 140, (255, 255, 230), (255, 190, 50), (255, 200, 60, 170)),
           ("max", "MAX !", 70, (255, 255, 255), (255, 214, 80), (255, 200, 80, 150)),
           ("lv1", "LV 1", 64, (255, 255, 255), (255, 150, 170), (255, 100, 140, 150)),
           ("lv2", "LV 2", 64, (255, 255, 255), (255, 190, 90), (255, 160, 60, 150)),
           ("att1", "LV1 ATTACK", 54, (255, 255, 255), (255, 170, 80), (255, 120, 40, 150)),
           ("att2", "LV2 ATTACK", 54, (255, 255, 255), (255, 120, 80), (255, 70, 40, 150)),
           ("chain", "CHAIN !", 34, (255, 255, 255), (255, 220, 120), None))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.fields = ts_fields(self.W, self.s)
        self.root = getattr(hd, "root", "") or ""
        self.tile = None                                  # the forest, built in the background / la forêt, préparée à côté
        self.tile_img = None
        threading.Thread(target=self._build_tile, daemon=True).start()
        self.scroll = 0.0
        self.side = {side: {"x": 0.5, "tx": 0.5, "next": 0.0, "hit": -99.0, "fire": 0.0, "enemies": [], "balls": [], "boss": None,
                            "next_row": 0.0, "chain": 0, "bomb": -99.0, "chain_n": 0, "chain_t": -99.0, "warn": (-99.0, 1),
                            "beam": (-99.0, 0), "red": -99.0, "ko": -99.0, "win": -99.0, "orb": (-99.0, 0), "hearts": [],
                            "boss_t": -99.0} for side in ("p1", "p2")}
        self.comets = []                                  # fireballs crossing the column / boules de feu qui traversent
        self.big = {}                                     # big texts and pictures of the effects / grands textes, images
        self.attacks = 0                                  # attacks sent (tests)
        self.bombs = 0
        self.hits = 0
        self.kos = 0
        self.beams = 0
        self.fx.sp.register("tsball", draw_img(S(34), S(34), lambda d, W, H: (d.ellipse([0, 0, W - 1, H - 1], fill=(255, 140, 40, 255)),
                                                                              d.ellipse([W * 0.2, H * 0.2, W * 0.6, H * 0.6], fill=(255, 230, 140, 255)))))
        self.warm = ([(self.witch, ("p1", 0, f)) for f in range(2)] + [(self.witch, ("p2", 0, f)) for f in range(2)]
                     + [(self.big_text, (k,)) for k, *_ in self.BIG] + [(self.chain_img, (n,)) for n in range(3, 13)]
                     + [(self.heart_img, (k,)) for k in ("full", "half", "empty")] + [(self.beam_img, ())]
                     + [(self.flash_img, (self.fields[0][1] * 1.1, self.H * 1.3, lv)) for lv in range(6, 0, -1)] + self.warm)

    def _build_tile(self):
        try:
            w = max(f[1] for f in self.fields)
            self.tile_img = ts_forest_tile(w, self.H, self.s)
        except Exception:
            self.tile_img = None

    # ------------------------------------------------------------ pictures, made once / images, faites une fois
    def _big(self, key, make):
        s = self.big.get(key)
        if s is None:
            if len(self.big) > 120:                       # names and chains vary: the cache stays bounded / borné
                self.big.clear()
            s = self.big[key] = make()
        return s

    def big_text(self, key):
        for k, text, size, top, bottom, glow in self.BIG:
            if k == key:
                return self._big(("bn", k), lambda: self.hd._surf(ts_banner(self.root, text, self.S(size), top, bottom,
                                                                           max(3, self.S(size / 13)), glow)))
        return None

    def chain_img(self, n):
        """N HIT on its starburst, bigger as the chain grows. / N HIT sur son éclat, plus gros quand la chaîne grandit."""
        def make():
            S = self.S
            size = min(76, 44 + 3 * n)
            txt = ts_banner(self.root, f"{n} HIT", S(size), (255, 255, 230), (255, 190, 60), max(3, S(size / 12)), (255, 140, 40, 140))
            r = int(max(txt.width, txt.height) * 0.62)
            burst = draw_img(2 * r, 2 * r, ts_burst(r, (255, 214, 80), (255, 120, 60)))
            img = Image.new("RGBA", (max(2 * r, txt.width), max(2 * r, txt.height)), (0, 0, 0, 0))
            img.alpha_composite(burst, ((img.width - burst.width) // 2, (img.height - burst.height) // 2))
            img.alpha_composite(txt, ((img.width - txt.width) // 2, (img.height - txt.height) // 2))
            return self.hd._surf(img)
        return self._big(("chain", min(n, 40)), make)

    def heart_img(self, kind):
        r = self.S(21)
        return self.img(("tsheart", kind), 2 * r + self.S(4), 2 * r + self.S(4), ts_heart(r, kind), ss=3)

    def orb_img(self, live):
        r = self.S(22)
        return self.img(("tsorb", live), 2 * r, 2 * r, ts_orb(live), ss=3)

    def plate_img(self, side, name, char, tag=None):
        c1, c2 = TS_PLATES[int(char) % len(TS_PLATES)] if char is not None else ((90, 90, 120), (60, 60, 90))
        tag = tag or ("2P" if side == "p2" else "1P")
        return self._big(("plate", side, name, c1, c2, tag), lambda: self.hd._surf(
            ts_plate(self.root, self.S(470), self.S(52), c1, c2, name, tag, side == "p2")))

    def column_box(self, top, big):
        """The box of the column, as in the game: VERSUS and VS between two players, STAGE and its number against the
        computer. / Le cadre de la colonne : VERSUS VS à deux, STAGE et son numéro contre l'ordinateur."""
        def make():
            S = self.S
            w, h = S(150), S(112)
            img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle([0, 0, w - 1, h - 1], radius=S(14), fill=(90, 14, 24, 235), outline=(250, 206, 80, 255), width=max(2, S(4)))
            d.rounded_rectangle([S(7), S(7), w - 1 - S(7), h - 1 - S(7)], radius=S(9), outline=(140, 80, 20, 255), width=max(1, S(2)))
            f = ts_font(self.root, "black", S(19))
            d.text((w / 2, S(25)), top, font=f, fill=(255, 220, 110, 255), anchor="mm", stroke_width=max(1, S(2)), stroke_fill=(50, 10, 10, 255))
            red = big == "VS"
            num = ts_banner(self.root, big, S(56 if red else 60), (255, 250, 220) if not red else (255, 240, 200),
                            (255, 190, 60) if not red else (255, 50, 50), max(3, S(4)))
            img.alpha_composite(num, ((w - num.width) // 2, int(S(70) - num.height / 2)))
            return self.hd._surf(img)
        return self._big(("box", top, big), make)

    def tint(self, color, alpha, w, h):
        key = ("tint", color, int(w), int(h))
        s = self.big.get(key)
        if s is None:
            s = self.big[key] = self.pg.Surface((int(w), int(h))).convert()
            s.fill(color)
        s.set_alpha(int(_clamp(alpha / 255.0) * 255))
        return s

    def flash_img(self, w, h, level):
        def make():
            g = Image.radial_gradient("L").point(lambda v: max(0, 255 - v * 255 // 181)).resize((int(w), int(h)), Image.BILINEAR)
            k = level / 6.0
            rgb = Image.merge("RGB", [g.point(lambda v, c=c: int(v * c * k / 255)) for c in (255, 250, 225)])
            return self.hd._surf(rgb)
        return self._big(("flash", int(w), int(h), level), make)

    def beam_img(self):
        return self._big("beam", lambda: self.hd._surf(ts_beam(self.S(170), self.S(330))))

    def look(self, vals, side):
        v = _n(vals.get("char" if side == "p1" else "char_p2"))
        if v is None:
            return 0 if side == "p1" else 3
        return int(v) % len(TS_LOOKS)

    def witch(self, side, look, frame):
        S = self.S
        hat, dress, hair = TS_LOOKS[look]
        return self.img(("witch", look, frame), S(104), S(124), witch_draw(hat, dress, hair, frame), ss=2)

    def restart(self, vals, now):
        for st in self.side.values():
            st["enemies"], st["balls"], st["boss"] = [], [], None
            st["next_row"] = now + 0.8
            st["ko"] = st["win"] = -99.0
        self.comets = []

    def fxy(self, side, fx_, fy_):
        """A point of a field, from fractions of its width and of the height. / Un point d'un terrain."""
        x0, w = self.fields[0 if side == "p1" else 1]
        return x0 + fx_ * w, fy_ * self.H

    def heart_xy(self, side, i):
        x0, w = self.fields[0 if side == "p1" else 1]
        S = self.S
        return (x0 + w - S(40) - i * S(46)) if side == "p2" else (x0 + S(40) + i * S(46)), S(92)

    # ------------------------------------------------------------ ce qui arrive
    def update(self, vals, now):
        S, dt, rng = self.S, self.dt, self.rng
        for side, suf in (("p1", ""), ("p2", "_p2")):
            st = self.side[side]
            other = "p2" if side == "p1" else "p1"
            stick = self.stick(vals, side)
            if stick is not None:                                      # the player's stick (Neo Geo BIOS)
                st["x"] = _clamp(st["x"] + stick[0] * dt * 0.8, 0.08, 0.92)
            else:
                if now >= st["next"]:
                    st["tx"], st["next"] = rng.uniform(0.12, 0.88), now + rng.uniform(0.8, 2.0)
                st["x"] += (st["tx"] - st["x"]) * min(1.0, dt * 2.0)
            ch = self.changed(vals, "lives" + suf)
            if ch:
                self.hearts_changed(side, other, ch[0], ch[1], now, vals)
            ch = self.changed(vals, "bombs" + suf)
            if ch and ch[1] < ch[0]:                                   # a bomb clears the field
                st["orb"] = (now, int(max(0, ch[1])))
                self.bomb(side, now)
            ch = self.changed(vals, "attack" + suf)
            if ch and ch[1] > 0:
                lvl = max(1, min(3, int(ch[1]) // 16))
                self.send(side, other, lvl, now)
            ch = self.changed(vals, "hits" + suf)
            if ch and ch[1] >= 2 and ch[1] > ch[0]:                     # the chain the game counts (N HIT)
                st["chain_n"], st["chain_t"] = int(ch[1]), now
                st["chain_xy"] = (st["x"], 0.46)
            elif ch and ch[1] < 2:
                st["chain_t"] = min(st["chain_t"], now - 1.0)          # it ends: the counter goes / il s'efface
            ch = self.changed(vals, "power" + suf)
            if ch and ch[1] < ch[0] and ch[0] >= 0x1000:               # a charged shot leaves
                self.charge(side, min(3, int(ch[0]) // 0x1000), now)
            if now >= st["next_row"]:                                  # a row of puffballs comes down
                st["next_row"] = now + rng.uniform(1.1, 2.0)
                col = rng.choice(((120, 180, 255), (255, 150, 200), (255, 220, 100), (150, 230, 140)))
                n = rng.choice((3, 4, 5))
                fx0 = rng.uniform(0.15, 0.85 - 0.12 * (n - 1))
                for i in range(n):
                    st["enemies"].append({"x": fx0 + 0.12 * i, "y": -0.1 - 0.02 * i, "col": col, "ph": rng.uniform(0, 6), "v": rng.uniform(0.12, 0.2)})
            if now >= st["fire"]:                                      # star shots
                st["fire"] = now + 0.12
                x, y = self.fxy(side, st["x"], 0.76)
                self.fx.tracer(x, y - S(30), x, S(-40), 2200, (255, 250, 200), 6, 50, "front", False)
                x0, w = self.fields[0 if side == "p1" else 1]
                ahead = [e for e in st["enemies"] if not e.get("dead") and abs(x0 + e["x"] * w - x) < S(36) and e["y"] > 0.0]
                if ahead and rng.random() < 0.3:
                    e = max(ahead, key=lambda e: e["y"])
                    self.pop(side, e, now)
            if st["chain"] >= 4:                                       # a chain: fireballs go over to the other side
                self.send(side, other, 0, now)
                st["chain"] = 0
            self.move_field(side, now)
        for c in self.comets:                                          # fireballs that reach the other field
            if not c.get("landed") and now - c["t0"] >= c["dur"]:
                c["landed"] = True
                so = self.side[c["to"]]
                x0, w = self.fields[0 if c["to"] == "p1" else 1]
                so["balls"].append({"x": _clamp((c["x1"] - x0) / w, 0.05, 0.95), "y": c["y1"] / self.H, "vx": self.rng.uniform(-0.15, 0.15),
                                    "v": self.rng.uniform(0.35, 0.5) * c["speed"]})
        self.comets = [c for c in self.comets if now - c["t0"] < c["dur"] + 0.05]

    def hearts_changed(self, side, other, old, new, now, vals):
        """A heart lost breaks, one given back fills up; none left is K.O. (and WIN ! on the other side).
        / Un cœur perdu éclate, un cœur rendu se remplit ; plus rien, c'est K.O."""
        st = self.side[side]
        if new < old:
            st["hit"] = now
            st["red"] = now
            self.hits += 1
            x, y = self.fxy(side, st["x"], 0.82)
            self.fx.sparks(x, y, 20, (255, 120, 160), (200, 500), (0, 360), (0.3, 0.7), 0, "front", 3, 20)
            for i in range(int(math.ceil(new - 0.01)), int(math.ceil(old - 0.01))):
                st["hearts"].append(("break", i, now))
                hx, hy = self.heart_xy(side, i)
                self.fx.sparks(hx, hy, 12, (255, 80, 130), (120, 360), (180, 360), (0.4, 0.8), 900, "front", 3, 12)
            if new <= 0 < old:
                st["ko"] = now
                self.kos += 1
                self.fx.shake(6, 0.35)
                os_ = self.side[other]
                if self.p1_in(vals) if other == "p1" else (self.p2_in(vals) or self.p1_in(vals)):     # the computer too
                    os_["win"] = now
                    for k in range(8):                                 # fireworks for the winner / feu d'artifice
                        self.fx.later(0.2 + k * 0.28, self.firework, other)
        else:
            for i in range(int(math.floor(old + 0.01)), int(math.ceil(new - 0.01))):
                st["hearts"].append(("fill", i, now))
            if old <= 0 < new:
                st["ko"] = self.side[other]["win"] = -99.0          # a new round / une nouvelle manche
        st["hearts"] = [h for h in st["hearts"] if now - h[2] < 1.0]

    def firework(self, side):
        x0, w = self.fields[0 if side == "p1" else 1]
        x, y = x0 + self.rng.uniform(0.15, 0.85) * w, self.rng.uniform(0.3, 0.7) * self.H
        col = self.rng.choice(((255, 214, 80), (255, 120, 200), (120, 220, 255), (180, 255, 140)))
        self.fx.sparks(x, y, 34, col, (200, 520), (0, 360), (0.5, 1.0), 220, "front", 3, 18)
        self.fx.glow(x, y, 20, 90, col, 0.5, "front", 0.9, 0.0)

    def pop(self, side, e, now):
        """A puffball pops; the ones of the same row follow in a chain, and the chain counter grows.
        / Une boule éclate, sa rangée suit en chaîne, le compteur de chaîne grandit."""
        st = self.side[side]
        n = 0
        for f in st["enemies"]:
            if not f.get("dead") and f["col"] == e["col"] and abs(f["y"] - e["y"]) < 0.08:
                f["dead"] = now + 0.08 * n
                n += 1
        st["chain"] += n

    def send(self, side, other, lvl, now):
        """Fireballs (or the big boss creature) go over to the other field, across the column, with !! where they
        land. / Des boules de feu passent de l'autre côté, par-dessus la colonne, avec !! là où elles arrivent."""
        so = self.side[other]
        if lvl >= 3:                                                   # boss attack
            so["boss"] = {"t0": now + 0.5, "x": self.rng.uniform(0.35, 0.65)}
            so["boss_t"] = now + 0.5
            self.attacks += 1
            self.fx.later(0.5, self.fx.shake, 7, 0.45)
            self.comet(side, other, now, (220, 120, 255), 0.5, 1.2, big=True)
            return
        for i in range({0: 2, 1: 2, 2: 3}[lvl]):
            self.comet(side, other, now + 0.08 * i, (255, 150, 50), 0.7, 1.3 if lvl == 2 else 1.0)
        if lvl:                                                        # LV1 / LV2 ATTACK where they land (the game's
            self.attacks += 1                                          # "!!" announces its Fever, not used here)
            so["warn"] = (now + 0.55, lvl)

    def comet(self, side, other, t0, color, dur, speed, big=False):
        x, y = self.fxy(side, 0.92 if side == "p1" else 0.08, self.rng.uniform(0.3, 0.5))
        x1, y1 = self.fxy(other, self.rng.uniform(0.2, 0.8), self.rng.uniform(0.25, 0.55))
        self.comets.append({"t0": t0, "x0": x, "y0": y, "x1": x1, "y1": y1, "col": color, "dur": dur, "to": other, "speed": speed,
                            "big": big, "landed": big})

    def charge(self, side, lvl, now):
        """The charged shot leaves as a beam of light, 1, 2 or MAX !, and clears what is in front of it.
        / Le tir chargé part en rayon de lumière et nettoie ce qui est devant."""
        st, S = self.side[side], self.S
        st["beam"] = (now, lvl)
        self.beams += 1
        x, y = self.fxy(side, st["x"], 0.78)
        self.fx.glow(x, y - S(40), 30, 160, (255, 230, 140), 0.5, "front", 1.0, 0.0)
        x0, w = self.fields[0 if side == "p1" else 1]
        for e in st["enemies"]:
            if abs(x0 + e["x"] * w - x) < S(90) and not e.get("dead"):
                e["dead"] = now

    def bomb(self, side, now):
        """A bomb, the big show: the whole screen shakes (and once more, smaller), flashes white, a shockwave and sparks
        burst from the middle of the field. / Une bombe, le grand spectacle : tout l'écran tremble, flashe, onde de choc."""
        st = self.side[side]
        self.bombs += 1
        st["bomb"] = now
        x, y = self.fxy(side, 0.5, 0.5)
        self.fx.shake(16, 0.75)
        self.fx.later(0.3, self.fx.shake, 9, 0.45)
        self.fx.flash((255, 250, 235), 0.45, 0.28)
        bx, by = self.fxy(side, 0.5, 0.55)
        for col, n, sp in (((255, 255, 255), 50, (500, 1300)), ((255, 220, 120), 40, (300, 900)), ((255, 140, 210), 30, (200, 700))):
            self.fx.sparks(bx, by, n, col, sp, (0, 360), (0.4, 0.9), 300, "front", 4, 22)
        x0, w = self.fields[0 if side == "p1" else 1]
        for i in range(12):
            a = i / 12 * math.tau
            self.fx.later(0.03 * i, self.fx.glow, x + math.cos(a) * w * 0.3, y + math.sin(a) * self.H * 0.3, 20, 110, (255, 240, 180), 0.5, "front",
                          1.0, 0.0)
        for e in st["enemies"]:
            e["dead"] = e.get("dead") or now
        st["balls"] = []
        self.comets = [c for c in self.comets if c["to"] != side or c["big"]]     # what was on its way goes too

    def move_field(self, side, now):
        dt, st = self.dt, self.side[side]
        keep = []
        for e in st["enemies"]:
            if e.get("dead") and now - e["dead"] > 0.4:
                if now - e["dead"] < 0.5:
                    x, y = self.fxy(side, e["x"], e["y"])
                    self.fx.sparks(x, y, 10, (255, 250, 200), (100, 300), (0, 360), (0.2, 0.5), 0, "front", 3, 14)
                continue
            if not e.get("dead"):
                e["y"] += e["v"] * dt
            if e["y"] < 1.1:
                keep.append(e)
        st["enemies"] = keep
        balls = []
        for b in st["balls"]:
            b["y"] += b["v"] * dt
            b["x"] = _clamp(b["x"] + b["vx"] * dt, 0.05, 0.95)
            if b["y"] < 1.1:
                balls.append(b)
        st["balls"] = balls
        if st["boss"] is not None and now - st["boss"]["t0"] > 4.0:
            st["boss"] = None

    # ------------------------------------------------------------ dessin
    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg, H = self.S, self.pg, self.H
        if self.tile is None and self.tile_img is not None:
            self.tile = self.hd._surf(self.tile_img)
            self.tile_img = None
        self.scroll += self.dt * S(60)
        for k, side in enumerate(("p1", "p2")):
            x0, w = self.fields[k]
            screen.set_clip(pg.Rect(int(x0), 0, int(w), H))
            if self.tile is not None:                                  # the forest scrolls down
                th = self.tile.get_height()
                off = (self.scroll + k * th * 0.37) % th
                screen.blit(self.tile, (int(x0), int(off - th)))
                screen.blit(self.tile, (int(x0), int(off)))
            else:
                pg.draw.rect(screen, (110, 176, 90), (int(x0), 0, int(w), H))
            self.draw_field(screen, vals, side, now)
            self.draw_moments(screen, vals, side, now)
            screen.set_clip(None)
        self.draw_comets(screen, now)
        self.status(screen, eng, vals, logo, now)

    def draw_field(self, screen, vals, side, now):
        S, pg = self.S, self.pg
        st = self.side[side]
        x0, w = self.fields[0 if side == "p1" else 1]
        for e in st["enemies"]:
            if e.get("dead") and now >= e["dead"]:
                continue
            img = self.img(("puff", e["col"]), S(70), S(60), puff_draw(e["col"]))
            x = x0 + (e["x"] + 0.03 * math.sin(now * 2 + e["ph"])) * w
            y = e["y"] * self.H
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        ball = self.fx.sp.obj("tsball", 0)
        for b in st["balls"]:                                          # fireballs from the other side
            x, y = x0 + b["x"] * w, b["y"] * self.H
            g = self.fx.sp.glow(S(30), (255, 120, 30), 9, hot=0.6)
            screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            screen.blit(ball, (int(x - ball.get_width() / 2), int(y - ball.get_height() / 2)))
        bo = st["boss"]
        if bo is not None and now >= bo["t0"]:
            k = (now - bo["t0"]) / 4.0
            img = self.img("tsboss", S(300), S(260), boss_draw)
            x = x0 + bo["x"] * w + math.sin(k * 6) * w * 0.15
            y = -img.get_height() / 2 + k * (self.H + img.get_height())
            g = self.fx.sp.glow(S(170), (200, 120, 255), 6)
            screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        look = self.look(vals, side)
        hit = now - st["hit"] < 1.0
        x, y = self.fxy(side, st["x"], 0.82)
        pw = _n(vals.get("power" if side == "p1" else "power_p2"))
        if pw is not None and pw >= 0x3000:                            # MAX: an aura around the witch / une aura
            g = self.fx.sp.glow(S(70 + 8 * math.sin(now * 8)), (255, 236, 140), 7)
            screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        if not (hit and int(now * 16) % 2):
            img = self.witch(side, look, int(now * 6) % 2)
            if hit:
                img = self.rotated(("witchspin", look), img, (now - st["hit"]) * 720, 15)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        kb = now - st["bomb"]
        if 0 <= kb < 2.6 and int(now * 20) % 4:                        # invincible after a bomb: a rainbow shield
            for i, col in enumerate(((255, 120, 200), (120, 200, 255), (255, 240, 120))):
                r = S(70 + i * 6 + 4 * math.sin(now * 10 + i))
                pg.draw.ellipse(screen, col, (int(x - r), int(y - r * 1.08), int(2 * r), int(2 * r * 1.08)), max(2, S(4)))

    def put_big(self, screen, surf, x, y, scale=1.0, alpha=1.0, dx=0):
        if surf is None or alpha <= 0.02:
            return
        if abs(scale - 1.0) > 0.02:
            surf = self.pg.transform.smoothscale(surf, (max(1, int(surf.get_width() * scale)), max(1, int(surf.get_height() * scale))))
        if alpha < 0.98:
            surf = surf.copy()
            surf.set_alpha(int(alpha * 255))
        screen.blit(surf, (int(x - surf.get_width() / 2 + dx), int(y - surf.get_height() / 2)))

    def draw_moments(self, screen, vals, side, now):
        """The big moments of a field, drawn over it and under the header. / Les grands moments d'un terrain."""
        S, pg, H = self.S, self.pg, self.H
        st = self.side[side]
        x0, w = self.fields[0 if side == "p1" else 1]
        cx = x0 + w / 2
        kr = now - st["red"]                                           # a heart lost: the field flashes red
        if 0 <= kr < 0.35:
            screen.blit(self.tint((255, 40, 70), 110 * (1 - kr / 0.35), w, H), (int(x0), 0))
        kb = now - st["boss_t"]                                        # a boss attack received: the field darkens
        if 0 <= kb < 4.2:
            a = min(1.0, kb / 0.3) * (1.0 if kb < 3.6 else max(0.0, (4.2 - kb) / 0.6))
            screen.blit(self.tint((40, 0, 60), 140 * a, w, H), (int(x0), 0))
        ko = now - st["ko"]
        if 0 <= ko < 6.0:
            screen.blit(self.tint((16, 16, 26), 140 * min(1.0, ko / 0.4), w, H), (int(x0), 0))
        kb = now - st["bomb"]                                          # a bomb: flash, rings of stars, BOMB !
        if 0 <= kb < 1.3:
            bx, by = self.fxy(side, 0.5, 0.55)
            lvl = max(0, min(6, int(round(6 * (1 - kb / 1.3) ** 1.5))))
            if lvl:
                fl = self.flash_img(w * 1.1, H * 1.3, lvl)
                screen.blit(fl, (int(bx - fl.get_width() / 2), int(by - fl.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            if kb < 0.55:                                              # the shockwave / l'onde de choc
                rw = 1 - kb / 0.55
                rad = int(S(40) + kb / 0.55 * w * 0.75)
                pg.draw.ellipse(screen, (255, 255, 255), (int(bx - rad), int(by - rad * 0.62), 2 * rad, int(2 * rad * 0.62)),
                                max(2, int(S(26) * rw)))
                pg.draw.ellipse(screen, (255, 230, 150), (int(bx - rad * 0.8), int(by - rad * 0.5), int(1.6 * rad), int(rad)),
                                max(1, int(S(10) * rw)))
            for ring, (n, size, col, speed) in enumerate(((10, 20, (255, 255, 255), 1.0), (16, 16, (255, 236, 140), 1.25),
                                                          (22, 12, (255, 170, 220), 1.5))):
                rad = S(60) + kb * speed * S(330)
                if rad > w:
                    continue
                for i in range(n):
                    a = i / n * math.tau + ring * 0.3 + kb * 0.8
                    pg.draw.polygon(screen, col, ts_star_pts(bx + math.cos(a) * rad * 1.25, by + math.sin(a) * rad * 0.6, S(size), a))
            self.put_big(screen, self.big_text("bomb"), bx, by - S(10), 1.0 + 0.7 * max(0.0, 1 - kb / 0.15),
                         1.0 if kb < 1.0 else (1.3 - kb) / 0.3)
        kb = now - st["boss_t"]
        if 0 <= kb < 2.2:                                              # BOSS ATTACK !, shaking / qui tremble
            sh = S(6) * math.sin(now * 60) if kb < 1.2 else 0
            self.put_big(screen, self.big_text("boss"), cx, H * 0.76, 1.0 + 0.6 * max(0.0, 1 - kb / 0.15), 1.0 if kb < 1.8 else (2.2 - kb) / 0.4, sh)
            for k in range(9):
                yy = S(140) + k * S(26)
                pg.draw.line(screen, (255, 255, 255), (int(x0 + S(10)), yy), (int(x0 + S(60)), yy - S(6)), max(1, S(3)))
                pg.draw.line(screen, (255, 255, 255), (int(x0 + w - S(60)), yy), (int(x0 + w - S(10)), yy - S(6)), max(1, S(3)))
        t0, lvl = st["beam"]                                           # the charged shot: a beam of light, 1 2 MAX !
        kc = now - t0
        if 0 <= kc < 0.9:
            wx, wy = self.fxy(side, st["x"], 0.80)
            b = self.beam_img().copy()
            b.set_alpha(int(255 * (1 - kc / 0.9)))
            screen.blit(b, (int(wx - b.get_width() / 2), int(wy - S(40) - b.get_height())))
            for i in range(6):
                sy = wy - S(60) - ((kc * S(500) + i * S(55)) % (wy - S(120)))
                pg.draw.polygon(screen, (255, 255, 255), ts_star_pts(wx + math.sin(i * 2.1) * S(40), sy, S(9 + i % 3 * 3), kc * 4 + i))
            lab = self.big_text({1: "lv1", 2: "lv2"}.get(lvl, "max"))
            off = S(180) if st["x"] < 0.6 else -S(180)
            self.put_big(screen, lab, wx + off, H * 0.5, 1.0 + 0.6 * max(0.0, 1 - kc / 0.12), 1.0 if kc < 0.7 else (0.9 - kc) / 0.2)
        t_w, lv_w = st["warn"]                                         # LV1 / LV2 ATTACK where the fireballs land
        kw = now - t_w
        if 0 <= kw < 1.2:
            self.put_big(screen, self.big_text("att2" if lv_w >= 2 else "att1"), cx, H * 0.34, 1.0 + 0.5 * max(0.0, 1 - kw / 0.12),
                         1.0 if kw < 0.9 else (1.2 - kw) / 0.3)
        kch = now - st["chain_t"]                                      # the chain counter / le compteur de chaîne
        calm = not (0 <= now - st["bomb"] < 1.3 or 0 <= now - st["boss_t"] < 2.2 or 0 <= ko < 6.0 or 0 <= now - st["win"] < 6.0
                    or 0 <= now - st["beam"][0] < 0.9)
        if calm and st["chain_n"] >= 2 and 0 <= kch < 1.3:
            fx_, fy_ = st.get("chain_xy", (0.5, 0.5))
            px, py = self.fxy(side, _clamp(fx_, 0.25, 0.75), fy_)
            img = self.chain_img(st["chain_n"])
            self.put_big(screen, img, px, py, 1.0 + 0.5 * max(0.0, 1 - kch / 0.12), 1.0 if kch < 1.0 else (1.3 - kch) / 0.3)
            self.put_big(screen, self.big_text("chain"), px, py + img.get_height() * 0.36, 1.0, 1.0 if kch < 1.0 else (1.3 - kch) / 0.3)
        if 0 <= ko < 6.0:                                              # K.O. / WIN !
            self.put_big(screen, self.big_text("ko"), cx, H * 0.53, 1.0 + 0.8 * max(0.0, 1 - ko / 0.18))
        kwn = now - st["win"]
        if 0 <= kwn < 6.0:
            self.put_big(screen, self.big_text("win"), cx, H * 0.54, 1.0 + 0.8 * max(0.0, 1 - kwn / 0.18) + 0.03 * math.sin(now * 6))

    def draw_comets(self, screen, now):
        """Fireballs crossing the column with their trail. / Les boules de feu qui traversent la colonne."""
        pg, S = self.pg, self.S
        for c in self.comets:
            k = (now - c["t0"]) / c["dur"]
            if k < 0 or k > 1.0:
                continue
            for i in range(10):
                kk = max(0.0, k - i * 0.035)
                x = c["x0"] + (c["x1"] - c["x0"]) * kk
                y = c["y0"] + (c["y1"] - c["y0"]) * kk - math.sin(kk * math.pi) * S(70)
                g = self.fx.sp.glow(S((26 if c["big"] else 18) * (1 - i * 0.07)), c["col"], max(1, 9 - i))
                screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            x = c["x0"] + (c["x1"] - c["x0"]) * k
            y = c["y0"] + (c["y1"] - c["y0"]) * k - math.sin(k * math.pi) * S(70)
            pg.draw.circle(screen, (255, 245, 200), (int(x), int(y)), S(12 if c["big"] else 9))

    def status(self, screen, eng, vals, logo, now):
        """At the top of each field the name plate, the score and five big hearts; at the bottom POW 1 2 MAX and the
        bombs; the logo above the column. / En haut la plaque du nom, le score, cinq gros cœurs ; en bas POW et bombes."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(4), S(380), S(76), now)
        stage = _n(vals.get("stage"))
        if self.p2_in(vals) and self.p1_in(vals):                     # the box of the column, as in the game
            box = self.column_box("VERSUS", "VS")
        elif stage is not None and stage >= 1:
            box = self.column_box("STAGE", str(int(stage)))
        else:
            box = None
        if box is not None:
            screen.blit(box, (int(W / 2 - box.get_width() / 2), int(H * 0.66 - box.get_height() / 2)))
        for k, (side, suf) in enumerate((("p1", ""), ("p2", "_p2"))):
            st = self.side[side]
            x0, w = self.fields[k]
            right = k == 1
            cpu = right and not self.p2_in(vals)                       # against the computer: its side, as in the game
            name = vals.get("name" + suf)
            char = _n(vals.get("char" + suf))
            plate = self.plate_img(side, name if isinstance(name, str) and name else ("CPU" if cpu else ("2P" if right else "1P")), char,
                                   "CPU" if cpu else None)
            px = x0 + w - S(14) - plate.get_width() if right else x0 + S(14)
            screen.blit(plate, (int(px), S(8)))
            sc = _n(vals.get("score" + suf))
            if cpu:                                                    # a second player can come in: the invitation
                word, col = self.invite(vals, now)
                self.label(screen, word, px - S(18), S(36), 26, col, align="right")
            elif sc is not None:                                       # the score, between the plate and the logo
                txt = hd.text(str(vals.get("score" + suf)), "black", S(50), AMBER)
                pw_ = txt["w"] + S(36)
                pcx = (px - S(14) - pw_ / 2) if right else (px + plate.get_width() + S(14) + pw_ / 2)
                self.pill(screen, pcx - pw_ / 2, S(8), pw_, S(52), 150)
                pop = 0.0
                t_ch = eng.state.changed_at.get("score" + suf)
                if t_ch is not None and 0 <= eng.ctx.t - t_ch < 0.25:
                    pop = 1 - (eng.ctx.t - t_ch) / 0.25
                hd.put(screen, txt, pcx, S(34), "center", "middle", scale=1 + 0.2 * pop)
            hearts = _n(vals.get("lives" + suf))
            if hearts is not None:                                     # five big hearts, half ones too
                fx_ = {h[1]: h for h in st["hearts"]}
                for i in range(5):
                    kind = "full" if hearts >= i + 1 else ("half" if hearts >= i + 0.5 else "empty")
                    img = self.heart_img(kind)
                    hx, hy = self.heart_xy(side, i)
                    h = fx_.get(i)
                    scale = 1.0
                    if h is not None:
                        kk = now - h[2]
                        if h[0] == "break" and kk < 0.5:
                            scale = 1.0 + 0.6 * (1 - kk / 0.5)
                            img = self.heart_img("full") if int(now * 20) % 2 else img
                        elif h[0] == "fill" and kk < 0.6:
                            scale = 1.0 + 0.5 * math.sin(kk / 0.6 * math.pi)
                            g = self.fx.sp.glow(S(34), (255, 200, 230), 6)
                            screen.blit(g, (int(hx - g.get_width() / 2), int(hy - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
                    self.put_big(screen, img, hx, hy, scale)
            pw = _n(vals.get("power" + suf))
            gx = x0 + w - S(24) - S(420) if right else x0 + S(24)
            if pw is not None:                                         # POW 1 2 MAX, three big segments, as in the game
                self.text(screen, "POW", gx, H - S(34), 30, (255, 214, 80), key="black", valign="middle", glow=0.3)
                level = pw / float(0x1000)
                for j in range(3):
                    sx = gx + S(86) + j * S(110)
                    box = pg.Rect(int(sx), H - S(50), S(100), S(32))
                    pg.draw.rect(screen, (40, 20, 50), box, border_radius=S(10))
                    fill = _clamp(level - j)
                    if fill > 0:
                        col = ((255, 90, 120), (255, 170, 60), (255, 236, 120))[j]
                        if level >= 3:
                            col = _mix((255, 196, 60), (255, 246, 170), 0.5 + 0.5 * math.sin(now * 12))
                            g = self.fx.sp.glow(S(46), (255, 230, 120), 5)
                            screen.blit(g, (int(sx + S(50) - g.get_width() / 2), int(H - S(34) - g.get_height() / 2)),
                                        special_flags=pg.BLEND_RGB_ADD)
                        pg.draw.rect(screen, col, (int(sx + S(2)), H - S(48), max(S(6), int(S(96) * fill)), S(28)), border_radius=S(8))
                    pg.draw.rect(screen, (255, 255, 255), box, max(1, S(2)), border_radius=S(10))
                    self.text(screen, ("1", "2", "MAX")[j], sx + S(50), H - S(34), 22 if j < 2 else 20,
                              (60, 20, 50) if fill >= 0.5 else (255, 255, 255), key="black", align="center", valign="middle", glow=0)
                if level >= 3:
                    pg.draw.polygon(screen, (255, 255, 255), ts_star_pts(gx + S(86) + S(320), H - S(50), S(16), now * 2))
            bombs = _n(vals.get("bombs" + suf))
            if bombs is not None:                                      # the bombs, blue B orbs
                bx = gx - S(70) if right else gx + S(420) + S(70)
                t_orb, used = st["orb"]
                for i in range(2):
                    ox = bx - i * S(56) if right else bx + i * S(56)
                    live = i < bombs
                    if not live and i == used and now - t_orb < 0.5:  # the one just used shatters / celle qui vient de partir
                        kk = (now - t_orb) / 0.5
                        for a in range(8):
                            ang = a / 8 * math.tau
                            rr = S(10) + kk * S(40)
                            pg.draw.circle(screen, (120, 170, 255), (int(ox + math.cos(ang) * rr), int(H - S(34) + math.sin(ang) * rr)),
                                           max(1, int(S(7) * (1 - kk))))
                        continue
                    img = self.orb_img(bool(live))
                    screen.blit(img, (int(ox - img.get_width() / 2), int(H - S(34) - img.get_height() / 2)))
                    self.text(screen, "B", ox, H - S(34), 26, WHITE if live else (150, 150, 170), key="black", align="center", valign="middle",
                              glow=0)
