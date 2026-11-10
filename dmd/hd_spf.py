"""Super Puzzle Fighter II Turbo on the HD screen (1.34): the two wells of the game, read in its memory gem by gem, face to
face in the middle with VS and the next pairs between them, each player's panel outside (name, score, rounds, chains).
Everything moves with the game. A gem that lands drops into place, a burst throws the pieces of each gem with the screen
shaking as hard as the burst is big, a power gem that forms or grows is swept by a golden shine and announced, the
counter gems fly from one well to the other and crash down there, a counter that runs out turns its gem over. The more a
well fills, the more its side warns, a slow amber glow, then a red heartbeat faster and faster, DANGER and its half of
the marquee turning red, as the music of the game speeds up. The losing well collapses at the end of a round, and two
humans see the matches each one won. Everything is drawn by the program, no picture comes from the game.

Super Puzzle Fighter II Turbo sur l'écran HD : les deux puits du jeu lus gemme par gemme dans sa mémoire, face à face au
milieu avec le VS et les paires suivantes entre eux, le panneau de chaque joueur dehors. Tout bouge avec le jeu : une
gemme qui se pose tombe à sa place, une explosion projette les morceaux de chaque gemme et l'écran tremble d'autant plus
qu'elle est grosse, une gemme de puissance qui se forme ou grandit est balayée d'un éclat doré et annoncée, les gemmes à
compteur volent d'un puits à l'autre et s'y écrasent, un compteur à zéro retourne sa gemme. Plus un puits se remplit,
plus son côté s'affole, lueur ambre lente puis battement rouge de plus en plus rapide, DANGER, sa moitié du marquee qui
rougit, comme la musique du jeu qui accélère. Le puits perdant s'effondre en fin de manche, et deux humains voient les
matchs gagnés par chacun. Tout est dessiné par le programme.

The memory (games/spf2t.json): each well 14 rows of 8 words, a wall, the 6 cells, a wall; row 0 hidden. A cell, low
byte L and high byte H: 1 to 4 a gem (blue, yellow, green, red), 9 to 12 a crash gem, 5 the diamond, L & 15 = 7 a
counter gem (colour H >> 4, count H & 15), 6 a counter at 0 turning into a gem of colour H >> 4, L & 0x80 a power gem
(colour L & 7, its neighbours in H: 0x10 up, 0x20 right, 0x40 down, 0x80 left), 0x1x 0x2x 0x6x 0x7x a gem bursting.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFilter

from . import hd_bg
from .hd_games import GOLD, RED, WHITE, GameScene, _clamp, _mix, _n
from .hd_credits import credits_word
from .hd_fx import Particle
from .hd_mslug import CREAM
from .i18n import tr
from .spfcodes import COLORS, decode, grid_of
from .spfcodes import danger as well_danger

# ------------------------------------------------------------------ the layout, in units of a 1920 x 460 screen
CELL = 31                       # a gem / une gemme
ROWS, COLS = 13, 6              # the visible well / le puits visible
TOP = (460 - ROWS * CELL) / 2   # the wells take the whole height / les puits prennent toute la hauteur
GAP = 156                       # between the two wells: NEXT, VS, the rounds / entre les deux puits
P1C, P2C = (255, 140, 50), (70, 190, 255)
CHAIN_COLS = {2: (90, 220, 255), 3: (150, 255, 110), 4: (255, 200, 60), 5: (255, 110, 60)}
VS_FORGET = 90.0                # seconds without two humans before their matches are forgotten / avant d'oublier
LAND = 0.14                     # a gem dropping into place / une gemme qui se pose
FLIP = 0.3                      # a counter gem turning over / une gemme à compteur qui se retourne


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ------------------------------------------------------------------ gems of our own / nos propres gemmes
def _facets(d, x0, y0, x1, y1, col, r):
    dark, light, mid = mix(col, (0, 0, 0), 0.5), mix(col, WHITE, 0.55), mix(col, WHITE, 0.2)
    d.rounded_rectangle([x0, y0, x1, y1], radius=max(2, r // 2), fill=dark + (255,))
    d.polygon([(x0, y0), (x1, y0), (x1 - r, y0 + r), (x0 + r, y0 + r)], fill=light + (255,))
    d.polygon([(x0, y0), (x0 + r, y0 + r), (x0 + r, y1 - r), (x0, y1)], fill=mid + (255,))
    d.polygon([(x1, y0), (x1, y1), (x1 - r, y1 - r), (x1 - r, y0 + r)], fill=mix(col, (0, 0, 0), 0.3) + (255,))
    d.polygon([(x0, y1), (x1, y1), (x1 - r, y1 - r), (x0 + r, y1 - r)], fill=mix(col, (0, 0, 0), 0.62) + (255,))
    d.rectangle([x0 + r, y0 + r, x1 - r, y1 - r], fill=col + (255,))
    tw, th = x1 - x0 - 2 * r, y1 - y0 - 2 * r
    d.polygon([(x0 + r, y0 + r), (x0 + r + tw * 0.45, y0 + r), (x0 + r, y0 + r + th * 0.45)], fill=mix(col, WHITE, 0.35) + (255,))
    e = min(tw, th)
    d.ellipse([x0 + r + e * 0.12, y0 + r + e * 0.1, x0 + r + e * 0.32, y0 + r + e * 0.3], fill=(255, 255, 255, 255))


def _star(d, cx, cy, R, fill=(255, 255, 255, 255)):
    d.polygon([(cx, cy - R), (cx + R * 0.2, cy - R * 0.2), (cx + R, cy), (cx + R * 0.2, cy + R * 0.2), (cx, cy + R),
               (cx - R * 0.2, cy + R * 0.2), (cx - R, cy), (cx - R * 0.2, cy - R * 0.2)], fill=fill)


def gem_draw(col):
    def fn(d, W, H):
        p = W * 0.06
        _facets(d, p, p, W - p, H - p, col, W * 0.2)
    return fn


def crash_draw(col):
    def fn(d, W, H):
        p = W * 0.07
        x0, y0, x1, y1 = p, p, W - p, H - p
        for k in range(14, 0, -1):                                  # a sphere in rings / une sphère en anneaux
            t = k / 14
            cc = mix(col, (0, 0, 0), 0.55 * t) if t > 0.5 else mix(col, WHITE, (0.5 - t))
            inset = (1 - t) * (x1 - x0) * 0.42
            off = (1 - t) * (x1 - x0) * -0.12
            d.ellipse([x0 + inset + off, y0 + inset + off, x1 - inset + off, y1 - inset + off], fill=cc + (255,))
        _star(d, x0 + (x1 - x0) * 0.36, y0 + (y1 - y0) * 0.34, (x1 - x0) * 0.2)
    return fn


def counter_draw(col, n, font):
    def fn(d, W, H):
        p = W * 0.06
        x0, y0, x1, y1 = p, p, W - p, H - p
        d.rounded_rectangle([x0, y0, x1, y1], radius=W * 0.14, fill=mix(col, (0, 0, 0), 0.55) + (255,))
        d.rounded_rectangle([x0 + W * 0.06, y0 + W * 0.06, x1 - W * 0.06, y1 - W * 0.09], radius=W * 0.12, fill=mix(col, (40, 40, 40), 0.35) + (255,))
        if font is not None and n:
            d.text((W / 2, H / 2), str(n), font=font, fill=(255, 255, 255, 255), anchor="mm", stroke_width=max(1, int(W * 0.06)),
                   stroke_fill=(0, 0, 0, 255))
    return fn


def diamond_draw():
    def fn(d, W, H):
        cx, cy, r = W / 2, H / 2, W * 0.44
        d.polygon([(cx, cy - r), (cx + r, cy - r * 0.15), (cx, cy + r), (cx - r, cy - r * 0.15)], fill=(200, 230, 255, 255))
        rainbow = [(255, 120, 140), (255, 220, 120), (140, 240, 170), (130, 190, 255), (210, 150, 255)]
        for k, cc in enumerate(rainbow):
            a, b = cx - r + 2 * r * k / 5, cx - r + 2 * r * (k + 1) / 5
            d.polygon([(a, cy - r * 0.15), (b, cy - r * 0.15), (cx, cy + r)], fill=cc + (255,))
        d.polygon([(cx - r * 0.5, cy - r * 0.15), (cx, cy - r), (cx + r * 0.5, cy - r * 0.15)], fill=(255, 255, 255, 255))
    return fn


def power_draw(col, w, h):
    def fn(d, W, H):
        c = W / w
        p = c * 0.06
        _facets(d, p, p, W - p, H - p, col, c * 0.34)
        d.rounded_rectangle([p, p, W - p, H - p], radius=c * 0.2, outline=mix(col, WHITE, 0.75) + (255,), width=max(2, int(c * 0.07)))
        for k in range(max(2, min(5, w * h // 2))):                    # sparkles / étincelles
            sx = p + (W - 2 * p) * (0.22 + 0.56 * ((k * 0.37) % 1))
            sy = p + (H - 2 * p) * (0.25 + 0.5 * ((k * 0.61) % 1))
            _star(d, sx, sy, c * 0.12)
    return fn


def shard_draw(col):
    def fn(d, W, H):
        d.polygon([(0.1 * W, 0.2 * H), (0.9 * W, 0.0), (0.7 * W, 1.0 * H)], fill=col + (255,))
        d.line([(0.1 * W, 0.2 * H), (0.9 * W, 0.0)], fill=mix(col, WHITE, 0.6) + (255,), width=max(1, int(W * 0.15)))
    return fn


def chunk_draw(col):
    """A big faceted piece of a power gem. / Un gros morceau taillé d'une gemme de puissance."""
    def fn(d, W, H):
        pts = [(0.08 * W, 0.3 * H), (0.55 * W, 0.04 * H), (0.96 * W, 0.42 * H), (0.7 * W, 0.96 * H), (0.18 * W, 0.8 * H)]
        d.polygon(pts, fill=mix(col, (0, 0, 0), 0.35) + (255,))
        d.polygon([pts[0], pts[1], (0.55 * W, 0.45 * H)], fill=mix(col, WHITE, 0.55) + (255,))
        d.polygon([pts[1], pts[2], (0.55 * W, 0.45 * H)], fill=mix(col, WHITE, 0.2) + (255,))
        d.polygon([pts[0], (0.55 * W, 0.45 * H), pts[4]], fill=col + (255,))
        d.line(pts + [pts[0]], fill=mix(col, WHITE, 0.75) + (255,), width=max(1, int(W * 0.06)))
    return fn


# ------------------------------------------------------------------ the night of the fights / la nuit des combats
def build_spf_night(W, H, s, seed=1501):
    """A violet night, a big pink moon in the middle (behind the VS), hills, a fan pattern, two red lanterns, a lacquer
    frieze. / Une nuit violette, une grosse lune rose au milieu, des collines, des éventails, deux lanternes, une frise."""
    rng = random.Random(seed)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=mix((54, 16, 70), (12, 6, 26), t) + (255,))
    pat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pat)
    R = 46 * s
    for row in range(int(H / R) + 2):
        for col in range(int(W / (2 * R)) + 2):
            cx = col * 2 * R + (R if row % 2 else 0)
            pd.arc([cx - R, row * R - R, cx + R, row * R + R], 180, 360, fill=(90, 30, 120, 34), width=max(1, int(2 * s)))
    img.alpha_composite(pat)
    for _ in range(int(140 * W / 1920)):                                # a few stars / quelques étoiles
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.55)
        a = rng.randint(60, 170)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 240, 255, a))
    moon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(moon)
    mx, my, R = W / 2, 250 * s, 150 * s
    for k in range(30, 0, -1):
        t = k / 30
        md.ellipse([mx - R * t * 1.9, my - R * t * 1.9, mx + R * t * 1.9, my + R * t * 1.9], fill=(255, 80, 150, int(10 * (1 - t) + 2)))
    md.ellipse([mx - R, my - R, mx + R, my + R], fill=(250, 120, 170, 200))
    md.ellipse([mx - R * 0.92, my - R * 0.95, mx + R * 0.88, my + R * 0.86], fill=(255, 150, 190, 200))
    img.alpha_composite(moon)
    hills = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd_ = ImageDraw.Draw(hills)
    for col, base, amp, ph in (((70, 24, 80), 330, 60, 0.0), ((44, 14, 56), 370, 50, 1.7), ((26, 8, 36), 410, 34, 3.1)):
        pts = [(0, H)]
        for x in range(0, int(W / s) + 40, 40):
            y = base - amp * (0.5 + 0.5 * math.sin(x / 210 + ph)) - 18 * math.sin(x / 67 + ph * 2)
            pts.append((x * s, y * s))
        pts.append((W, H))
        hd_.polygon(pts, fill=col + (255,))
    img.alpha_composite(hills)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for lx in (W * 0.27, W * 0.73):                                    # two lanterns / deux lanternes
        gd.ellipse([lx - 60 * s, -30 * s, lx + 60 * s, 90 * s], fill=(255, 120, 40, 70))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(1, 24 * s))))
    for lx in (W * 0.27, W * 0.73):
        d.line([(lx, 0), (lx, 18 * s)], fill=(40, 20, 10, 255), width=max(1, int(2 * s)))
        d.rounded_rectangle([lx - 16 * s, 18 * s, lx + 16 * s, 58 * s], radius=12 * s, fill=(220, 50, 40, 255))
        for k in range(3):
            d.line([(lx - 16 * s, (26 + k * 10) * s), (lx + 16 * s, (26 + k * 10) * s)], fill=(160, 20, 20, 255), width=max(1, int(s)))
        d.rectangle([lx - 8 * s, 56 * s, lx + 8 * s, 62 * s], fill=GOLD + (255,))
    for y0, h in ((0, 7), (460 - 7, 7)):
        d.rectangle([0, y0 * s, W, (y0 + h) * s], fill=(150, 26, 34, 255))
        yl = (y0 + (h if y0 == 0 else 0)) * s
        d.line([(0, yl), (W, yl)], fill=(236, 190, 92, 255), width=max(1, int(2 * s)))
    return {"sky": img.convert("RGB"), "layers": [], "tw": W, "amb": {}}


hd_bg.BUILDERS["spf_night"] = build_spf_night


# ------------------------------------------------------------------ one well as the game has it / un puits
class Well:
    """The cells of one well as last read, and what is moving in it. / Les cases d'un puits et ce qui y bouge."""

    def __init__(self):
        self.grid = None                     # 14 x 6 words
        self.land = {}                       # (r, k): when it dropped into place / quand elle s'est posée
        self.flip = {}                       # (r, k): (old colour, when) a counter turning over / qui se retourne
        self.tick = {}                       # (r, k): when its count went down / quand son compte a baissé
        self.shine = {}                      # (r, k, w, h): when its power gem formed or grew / quand elle s'est formée
        self.blocks = []                     # [(r, k, w, h, colour)] power gems / gemmes de puissance
        self.danger = 0.0                    # 0 to 1, smoothed / lissé
        self._last_blocks = []
        self.phase = 0.0                     # of the heartbeat / du battement
        self.hidden_until = -99.0            # the well collapsed at the end of a round / effondré
        self.collapsed = False               # until the game empties it for the next round / jusqu'à la manche suivante
        self.thud = -99.0                    # counter gems crashed down / gemmes à compteur écrasées

    def find_blocks(self):
        """The power gems: from each top-left corner, as far as their neighbours go. / Les gemmes de puissance."""
        g, out = self.grid, []
        for r in range(14):
            for k in range(COLS):
                c = decode(g[r][k])
                if not c or c[0] != "power" or (c[2] & 0x10) or (c[2] & 0x80):
                    continue
                w = 1
                while k + w < COLS and (decode(g[r][k + w - 1]) or ("", 0, 0))[2] & 0x20 and (decode(g[r][k + w]) or ("",))[0] == "power":
                    w += 1
                h = 1
                while r + h < 14 and (decode(g[r + h - 1][k]) or ("", 0, 0))[2] & 0x40 and (decode(g[r + h][k]) or ("",))[0] == "power":
                    h += 1
                if w >= 2 and h >= 2:
                    out.append((r, k, w, h, c[1]))
        return out


class SpfScene(GameScene):
    """Super Puzzle Fighter II Turbo, the wells of the game face to face, everything moving with it."""
    THEME = "spf_night"
    STATIC = True
    SHADE = (0, 40)
    CREDITS = None                  # drawn between the wells, at the bottom (draw_credit) / entre les puits, en bas
    BANNERS = (("GAME OVER", RED), ("WIN", GOLD))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.wells = [Well(), Well()]
        self.chain = [(0, -99.0), (0, -99.0)]          # (chain, when) shown in each panel / montré dans chaque panneau
        self.power = [None, None]                      # (w, h, when) the last power gem announced / la dernière annoncée
        self.atk = [0, 0]
        self.wins = [0, 0]                             # rounds of the match / manches du match
        self.vs = [0, 0]                               # matches won by each of two humans / matchs gagnés
        self.vs_pop = [-99.0, -99.0]
        self.vs_t = -999.0
        self.win_side = (None, -99.0)
        self.fall = [None, None]                       # the falling pair drawn: (x, y) smoothed / la paire qui tombe
        for col, rgb in COLORS.items():
            self.fx.sp.register(f"spf_sh{col}", self._shard(rgb))
            self.fx.sp.register(f"spf_gm{col}", self._pil(gem_draw(rgb), CELL))
            self.fx.sp.register(f"spf_ct{col}", self._pil(counter_draw(rgb, 5, None), CELL * 0.8))
        for col, rgb in COLORS.items():
            self.fx.sp.register(f"spf_bk{col}", self._pil(chunk_draw(rgb), CELL * 0.72))
        self.fx.sp.register("spf_sh0", self._shard((235, 245, 255)))
        self.fx.sp.register("spf_gm0", self._pil(diamond_draw(), CELL))
        self.warm = [(self.gem, (kind, col, n)) for col in COLORS for kind, n in (("gem", 0), ("crash", 0), ("counter", 5), ("counter", 4),
                                                                                   ("counter", 3))] + self.warm

    # ------------------------------------------------------------ pictures / images
    def _pil(self, fn, size):
        from .hd_games import draw_img
        return draw_img(self.S(size), self.S(size), fn)

    def _shard(self, rgb):
        from .hd_games import draw_img
        return draw_img(self.S(CELL * 0.5), self.S(CELL * 0.5), shard_draw(rgb))

    def ring(self, x, y, r0, r1, col, life, width=8, a0=0.9, delay=0.0, layer="front"):
        """A shock wave from (x, y). / Une onde de choc."""
        s = self.fx.s
        p = self.fx.add(Particle("ring", x, y, self.fx.now + delay, life, layer))
        p.r0, p.r1, p.col, p.a0, p.a1, p.data = r0 * s, r1 * s, col, a0, 0.0, width * s

    def cell(self):
        return self.S(CELL)

    def gem(self, kind, col, n=0):
        c = self.cell()
        if kind == "crash":
            return self.img(("spf", "crash", col), c, c, crash_draw(COLORS.get(col, WHITE)))
        if kind == "counter":
            f = self.hd.font("black", int(c * 0.62 * 3))
            return self.img(("spf", "cnt", col, n), c, c, counter_draw(COLORS.get(col, WHITE), n, f))
        if kind == "diamond":
            return self.img(("spf", "dia"), c, c, diamond_draw())
        return self.img(("spf", "gem", col), c, c, gem_draw(COLORS.get(col, WHITE)))

    def block(self, col, w, h):
        c = self.cell()
        return self.img(("spf", "pow", col, w, h), c * w, c * h, power_draw(COLORS.get(col, WHITE), w, h), ss=2)

    def metal(self, text, size, side, key="logo"):
        """A name in metal letters, the player's colour at the bottom. / Un nom en lettres de métal."""
        k = ("spf", "metal", text, size, side, key)
        s = self.imgs.get(k)
        if s is not None:
            return s
        f = self.hd.font(key, self.S(size))
        top, bottom, stroke = {0: ((255, 244, 214), P1C, (60, 18, 0)), 1: ((236, 250, 255), P2C, (0, 26, 60)),
                               "vs": ((255, 240, 240), (225, 40, 60), (60, 0, 10)),
                               "gold": ((255, 248, 220), (226, 160, 50), (60, 30, 0))}.get(side, ((255, 255, 255), GOLD, (40, 20, 0)))
        if isinstance(side, tuple):
            top, bottom, stroke = WHITE, side, mix(side, (0, 0, 0), 0.8)
        sw = max(2, self.S(4))
        box = f.getbbox(text, stroke_width=sw)
        w, h = box[2] - box[0] + 2 * sw + self.S(8), box[3] - box[1] + 2 * sw + self.S(10)
        ox, oy = -box[0] + sw + self.S(4), -box[1] + sw + self.S(3)
        out = Image.new("L", (w, h), 0)
        ImageDraw.Draw(out).text((ox, oy), text, font=f, fill=255, stroke_width=sw)
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).text((ox, oy), text, font=f, fill=255)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 255))
        sh.putalpha(out.filter(ImageFilter.GaussianBlur(max(1, self.S(4)))).point(lambda v: int(v * 0.7)))
        img.alpha_composite(sh, (0, 0))
        st = Image.new("RGBA", (w, h), stroke + (255,))
        st.putalpha(out)
        img.alpha_composite(st)
        grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(grad)
        b = mask.getbbox() or (0, 0, w, h)
        for y in range(b[1], b[3] + 1):
            t = (y - b[1]) / max(1, b[3] - b[1])
            c = mix(top, bottom, min(1, t * 1.25)) if t < 0.55 else mix(bottom, mix(bottom, WHITE, 0.25), (t - 0.55) / 0.45)
            gd.line([(0, y), (w, y)], fill=c + (255,))
        grad.putalpha(mask)
        img.alpha_composite(grad)
        s = self.imgs[k] = self.hd._surf(img)
        return s

    def blit_c(self, screen, surf, x, y, scale=1.0, alpha=1.0):
        """A picture centred on (x, y), scaled and faded. / Une image centrée, agrandie et estompée."""
        if scale != 1.0:
            w, h = surf.get_size()
            surf = self.pg.transform.smoothscale(surf, (max(1, int(w * scale)), max(1, int(h * scale))))
        if alpha < 1.0:
            surf = surf.copy()
            surf.set_alpha(int(255 * _clamp(alpha)))
        screen.blit(surf, (int(x - surf.get_width() / 2), int(y - surf.get_height() / 2)))

    # ------------------------------------------------------------ geometry / géométrie
    def well_x(self, side):
        return self.S(960 - GAP / 2 - COLS * CELL) if side == 0 else self.S(960 + GAP / 2)

    def panel_x(self, side):
        x1, x2 = 960 - GAP / 2 - COLS * CELL, 960 + GAP / 2 + COLS * CELL
        return self.S((x1 - 30) / 2 + 6) if side == 0 else self.S((x2 + 30 + 1920) / 2 - 6)

    def cell_xy(self, side, r, k):
        """Top-left of the cell of row r (1 to 13 visible) and column k. / Coin haut gauche d'une case."""
        return self.well_x(side) + k * self.cell(), self.S(TOP) + (r - 1) * self.cell()

    # ------------------------------------------------------------ what the game does / ce que fait le jeu
    def restart(self, vals, now):
        for w in self.wells:
            w.grid = None
        self.atk = [_n(vals.get("atk1")) or 0, _n(vals.get("atk2")) or 0]
        self.wins = [_n(vals.get("wins1")) or 0, _n(vals.get("wins2")) or 0]

    @staticmethod
    def hidden(w, now):
        return now < w.hidden_until or w.collapsed

    def humans(self, vals):
        return vals.get("p1_mode") in (1, 2) and vals.get("p2_mode") in (1, 2)

    def always(self, vals, now):
        dt = self.dt
        for side, w in enumerate(self.wells):
            g = grid_of(vals.get("well1" if side == 0 else "well2"))
            if g is not None:
                if w.collapsed and sum(1 for r in range(1, 14) for k in range(COLS) if decode(g[r][k])) <= 4:
                    w.collapsed = False                                # the next round / la manche suivante
                if w.grid is not None and not self.hidden(w, now):
                    self.compare(side, w, w.grid, g, now)
                elif w.grid is None:                                   # the first reading: nothing new yet
                    w.grid = g                                         # / la première lecture : rien de nouveau
                    w._last_blocks = w.find_blocks()
                w.grid = g
                w.blocks = w.find_blocks()
                target = well_danger(g)
            else:
                target = 0.0
            if self.nobody(vals) or self.hidden(w, now):
                target = 0.0
            w.danger += (target - w.danger) * min(1.0, dt * 3.0)
            period = 1.45 - 1.1 * w.danger                             # the heart beats faster / le coeur bat plus vite
            old = w.phase
            w.phase = (w.phase + dt / period) % 1.0
            if w.danger > 0.45:
                for p0, k in ((0.03, 1.0), (0.25, 0.65)):              # the two thumps / les deux coups
                    if old < p0 <= w.phase or (w.phase < old and (p0 > old or p0 <= w.phase)):
                        self.thump(side, w.danger * k)
        if self.humans(vals):
            self.vs_t = now
        elif now - self.vs_t > VS_FORGET and any(self.vs):
            self.vs = [0, 0]
            self.hd.log(tr("Puzzle Fighter, matchs VS remis à zéro (un joueur est parti)", "Puzzle Fighter, VS matches back to 0 (a player left)"))

    def thump(self, side, k):
        """A heartbeat: a red wave behind the panel and the well of that side. / Un battement : une vague rouge."""
        S = self.S
        px, wx = self.panel_x(side), self.well_x(side) + COLS * self.cell() / 2
        cy = self.H / 2
        self.fx.glow(px, cy, 160, 520, (255, 24, 30), 0.42, "back", 0.25 + 0.6 * k, 0.0, hot=0.15)
        self.fx.glow(wx, cy, 90, 300, (255, 40, 30), 0.36, "back", 0.2 + 0.5 * k, 0.0, hot=0.2)
        if k > 0.6:
            self.ring(px, S(194), 60, 380, (255, 60, 50), 0.45, 9, 0.35 + 0.5 * k, layer="back")

    def compare(self, side, w, old, new, now):
        """What changed in a well since the last reading: gems landing, bursts, counters, gems crashing down."""
        bursts, counters_in = [], 0
        for r in range(14):
            for k in range(COLS):
                a, b = decode(old[r][k]), decode(new[r][k])
                if a == b:
                    continue
                if b and b[0] != "burst" and (not a or a[0] == "burst"):
                    if r >= 1:
                        w.land[(r, k)] = now
                    if b[0] == "counter":
                        counters_in += 1
                elif a and a[0] not in ("burst",) and (not b or b[0] == "burst") and r >= 1:
                    bursts.append((r, k, a))
                elif a and b and a[0] == "counter" and b[0] == "counter" and b[2] < a[2]:
                    w.tick[(r, k)] = now
                elif a and b and a[0] == "counter" and b[0] == "gem":
                    w.flip[(r, k)] = (a[1], now)
        if bursts:
            self.burst(side, bursts, now)
        if counters_in >= 3:                                          # an attack crashes down / une attaque s'écrase
            w.thud = now
            self.fx.kick(0, 6 + min(10, counters_in * 0.5), 0.35)
            x = self.well_x(side) + COLS * self.cell() / 2
            y = self.S(TOP) + self.cell() * 2
            self.fx.smoke(x, y, 10, (14, 26), 2.2, (0.4, 0.8), (10, 40), COLS * CELL / 2, (120, 90, 140), 120, "front")
        before = {(b[0], b[1], b[2], b[3]) for b in w._last_blocks}
        now_blocks = w.find_blocks()
        for blk in now_blocks:
            key = blk[:4]
            if key in before:
                continue
            grew = [b for b in w._last_blocks if b[0] <= blk[0] + blk[3] - 1 and blk[0] <= b[0] + b[3] - 1
                    and b[1] <= blk[1] + blk[2] - 1 and blk[1] <= b[1] + b[2] - 1]
            if grew and max(b[2] * b[3] for b in grew) >= blk[2] * blk[3]:
                continue
            w.shine[key] = now
            self.power[side] = (blk[2], blk[3], now)
            x, y = self.cell_xy(side, blk[0], blk[1])
            cx, cy = x + blk[2] * self.cell() / 2, y + blk[3] * self.cell() / 2
            self.fx.glow(cx, cy, 20, 30 + 12 * blk[2] * blk[3], GOLD, 0.45, "front", 0.9, 0.0)
            self.fx.sparks(cx, cy, 10 + 2 * blk[2] * blk[3], (255, 236, 160), (150, 520), (0, 360), (0.25, 0.6), 300, "front", 3, 18)
        w._last_blocks = now_blocks

    def burst(self, side, cells, now):
        """The gems that burst: each one breaks into pieces of its colour, a power gem into big chunks, a shock wave of
        the burst's colour, a flash, and the screen shakes as hard as the burst is big. / Chaque gemme éclate en morceaux
        de sa couleur, une gemme de puissance en gros morceaux, une onde de choc, un éclair, l'écran tremble."""
        c = self.cell()
        rng = self.rng
        n = len(cells)
        power = sum(1 for _, _, a in cells if a[0] == "power")
        many = n > 30
        cols = [a[1] if a[0] != "diamond" else 0 for _, _, a in cells]
        main = max(set(cols), key=cols.count)
        mrgb = COLORS.get(main, (235, 245, 255))
        xs, ys, pxs, pys = [], [], [], []
        for (r, k, a), col in zip(cells, cols):
            x, y = self.cell_xy(side, r, k)
            x, y = x + c / 2, y + c / 2
            xs.append(x)
            ys.append(y)
            rgb = COLORS.get(col, (235, 245, 255))
            for _ in range(2 if many else 5):
                ang = rng.uniform(0, 2 * math.pi)
                v = rng.uniform(220, 660)
                self.fx.obj(f"spf_sh{col}", x, y, math.cos(ang) * v, math.sin(ang) * v - 340, gravity=1500, vrot=rng.uniform(-900, 900),
                            life=rng.uniform(0.7, 1.2), rot=rng.uniform(0, 360))
            if a[0] == "power":
                pxs.append(x)
                pys.append(y)
                if not many:
                    for _ in range(2):
                        ang = rng.uniform(math.pi * 1.1, math.pi * 1.9)
                        v = rng.uniform(260, 620)
                        self.fx.obj(f"spf_bk{col}", x, y, math.cos(ang) * v, math.sin(ang) * v - 200, gravity=1700,
                                    vrot=rng.uniform(-600, 600), life=rng.uniform(1.0, 1.5), rot=rng.uniform(0, 360))
            if not many or rng.random() < 0.3:
                self.fx.glow(x, y, 12, 70, mix(rgb, WHITE, 0.55), 0.32, "front", 1.0, 0.0, hot=0.6)
            if a[0] == "diamond":
                self.fx.sparks(x, y, 30, (255, 255, 255), (200, 700), (0, 360), (0.3, 0.7), 400, "front", 3, 20)
        cx, cy = sum(xs) / n, sum(ys) / n
        big = min(1.0, n / 16)
        self.ring(cx, cy, 16, min(460, 110 + n * 16 + power * 10), mix(mrgb, WHITE, 0.4), 0.5 + 0.3 * big, 8 + 6 * big)
        self.fx.glow(cx, cy, 30, min(340, 80 + n * 12), mrgb, 0.45, "front", 0.85, 0.0, hot=0.5)
        self.fx.sparks(cx, cy, min(70, 10 + n * 3), mix(mrgb, WHITE, 0.5), (300, 1100), (0, 360), (0.3, 0.8), 900, "front", 3, 34)
        if pxs:                                                        # a power gem: gold on top / de l'or en plus
            bx, by = sum(pxs) / len(pxs), sum(pys) / len(pys)
            self.ring(bx, by, 24, min(560, 200 + power * 22), GOLD, 0.75, 16, 1.0, delay=0.05)
            self.fx.glow(bx, by, 50, min(380, 150 + power * 16), (255, 236, 160), 0.4, "front", 1.0, 0.0, hot=0.8)
            self.fx.sparks(bx, by, min(90, 30 + power * 4), (255, 236, 160), (400, 1400), (190, 350), (0.5, 1.1), 1100, "front", 4, 46)
        amp = min(20.0, 5.0 + n * 0.8 + power * 0.6)
        self.fx.shake(amp, 0.35 + min(0.6, n * 0.03))
        if n >= 6:
            self.fx.flash(mix(mrgb, WHITE, 0.45), min(0.45, 0.06 + n * 0.017 + power * 0.012), 0.32)
        if n >= 4:
            self.fx.text(f"{n}", cx, cy, mix(mrgb, WHITE, 0.6), 44 + min(76, n * 2.8), key="black", life=1.2, rise=100)

    def update(self, vals, now):
        for side, name in ((0, "chain1"), (1, "chain2")):
            ch = self.changed(vals, name)
            if ch and ch[1] >= 2 and ch[1] > ch[0]:
                self.chain[side] = (ch[1], now)
                self.fx.shake(4 + 2 * ch[1], 0.3)
                self.fx.flash(CHAIN_COLS.get(min(5, ch[1]), WHITE), 0.15, 0.2)
        for side, name in ((0, "atk1"), (1, "atk2")):
            v = _n(vals.get(name)) or 0
            if v > self.atk[side]:
                self.fly(side, v - self.atk[side], now)
            self.atk[side] = v
        for side, name in ((0, "wins1"), (1, "wins2")):
            v = _n(vals.get(name))
            if v is None:
                continue
            if v > self.wins[side]:
                self.round_won(side, v, vals, now)
            self.wins[side] = v

    def fly(self, side, n, now):
        """Counter gems fly from this well to the other one, in an arc over the middle. / Elles volent vers l'autre puits."""
        c = self.cell()
        x0 = self.well_x(side) + COLS * c / 2
        x1 = self.well_x(1 - side) + COLS * c / 2
        y = self.S(TOP) + c
        for i in range(min(6, max(1, n))):
            col = self.rng.randint(1, 4)
            dx = (i - 2.5) * c * 0.5
            self.fx.projectile(f"spf_ct{col}", x0 + dx, y + c * 2, x1 + dx, y, 0.55 + 0.04 * i, 110.0,
                               lambda a, b: self.fx.sparks(a, b, 5, (255, 240, 180), (120, 360), (0, 360), (0.15, 0.3), 300, "front", 3, 12),
                               spin=300.0, trail=0.0)

    def round_won(self, side, v, vals, now):
        """A round won: WIN over the winner, the other well collapses. / WIN chez le gagnant, l'autre puits s'effondre."""
        self.win_side = (side, now)
        loser = self.wells[1 - side]
        c, rng = self.cell(), self.rng
        if loser.grid is not None:
            for r in range(1, 14):
                for k in range(COLS):
                    g = decode(loser.grid[r][k])
                    if not g:
                        continue
                    x, y = self.cell_xy(1 - side, r, k)
                    col = g[1] if g[0] != "diamond" else 0
                    name = f"spf_gm{col}" if g[0] != "counter" else f"spf_ct{col}"
                    self.fx.obj(name, x + c / 2, y + c / 2, rng.uniform(-160, 160), rng.uniform(-420, -80) - (13 - r) * 12,
                                gravity=1500, vrot=rng.uniform(-400, 400), life=1.6)
            loser.hidden_until = now + 1.8
            loser.collapsed = True
        self.fx.shake(10, 0.6)
        x = self.well_x(side) + COLS * c / 2
        for k in range(3):
            self.fx.sparks(x, self.S(200), 40, GOLD, (300, 900), (200, 340), (0.4, 0.9), 700, "front", 3, 24)
        target = {1: 1, 2: 2, 3: 3}.get(_n(vals.get("_rounds_vs")) or 2, 2)
        if self.humans(vals) and v >= target:
            self.vs[side] += 1
            self.vs_pop[side] = now
            self.hd.log(tr(f"Puzzle Fighter, matchs VS : J1 {self.vs[0]}, J2 {self.vs[1]}",
                           f"Puzzle Fighter, VS matches: P1 {self.vs[0]}, P2 {self.vs[1]}"))

    # ------------------------------------------------------------ drawing / dessin
    def draw_hud(self, screen, eng, vals, logo, now):
        for side in (0, 1):
            self.draw_danger(screen, side, now)
        for side in (0, 1):
            self.draw_well(screen, side, vals, now)
        self.draw_middle(screen, vals, now)
        self.draw_credit(screen, eng, vals, now)
        for side in (0, 1):
            self.draw_panel(screen, eng, side, vals, now)
        side, t0 = self.win_side
        if side is not None and now - t0 < 2.2:
            dt = now - t0
            sc = 2.2 - 1.2 * min(1.0, dt / 0.22) + 0.08 * math.sin(dt * 9)
            a = 1.0 if dt < 1.8 else 1 - (dt - 1.8) / 0.4
            x = self.well_x(side) + COLS * self.cell() / 2
            self.blit_c(screen, self.metal("WIN", 84, "gold"), x, self.S(190), sc, a)

    def beat(self, w):
        """The heartbeat, two thumps, 0 to 1. / Le battement, deux coups."""
        p = w.phase
        return math.exp(-((p - 0.05) / 0.07) ** 2) + 0.65 * math.exp(-((p - 0.27) / 0.07) ** 2)

    def draw_danger(self, screen, side, now):
        """The more the well fills, the redder its half of the marquee beats. / Plus le puits monte, plus sa moitié rougit."""
        w = self.wells[side]
        if w.danger < 0.05:
            return
        a = _clamp(w.danger ** 0.8 * (0.16 + 0.84 * _clamp(self.beat(w))))
        key = ("spf", "veil2", side)
        veil = self.imgs.get(key)
        if veil is None:
            vw, vh = self.W // 2, self.H
            im = Image.new("RGBA", (vw, vh), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            for x in range(vw):
                t = x / vw if side == 1 else 1 - x / vw
                d.line([(x, 0), (x, vh)], fill=(255, 16, 26, int(230 * (0.25 + 0.75 * t ** 1.1))))
            for y in range(self.S(26)):                                # the top and bottom edges burn / les bords brûlent
                al = int(160 * (1 - y / self.S(26)) ** 2)
                d.line([(0, y), (vw, y)], fill=(255, 60, 40, al))
                d.line([(0, vh - 1 - y), (vw, vh - 1 - y)], fill=(255, 60, 40, al))
            veil = self.imgs[key] = self.hd._surf(im)
        veil.set_alpha(int(255 * a * (0.6 if w.danger < 0.6 else 1.0)))
        screen.blit(veil, (0 if side == 0 else self.W // 2, 0))

    def heat(self, w):
        """(danger step 0 to 8, beat step 0 to 3): the bezel and its glow are kept by steps. / Par paliers."""
        return int(round(w.danger * 8)), int(round(_clamp(self.beat(w)) * 3))

    @staticmethod
    def bezel_color(q, b):
        d, k = q / 8, b / 3
        base = (236, 190, 92)
        if d < 0.35:
            return base
        hot = mix((255, 150, 40), (255, 40, 40), _clamp((d - 0.55) / 0.35))
        return mix(base, mix(hot, WHITE, 0.3 * k), _clamp((d - 0.35) / 0.3) * (0.6 + 0.4 * k))

    def draw_well(self, screen, side, vals, now):
        pg, S, c = self.pg, self.S, self.cell()
        w = self.wells[side]
        x0, y0 = self.well_x(side), S(TOP)
        jx = jy = 0
        if w.danger > 0.7:                                             # the well trembles / le puits tremble
            jx = int(math.sin(now * 61) * S(4) * (w.danger - 0.7) / 0.3)
            jy = int(math.cos(now * 47) * S(2) * (w.danger - 0.7) / 0.3)
        if now - w.thud < 0.35:
            jy += int(S(8) * (1 - (now - w.thud) / 0.35) ** 2)
        x0 += jx
        y0 += jy
        ww, hh = COLS * c, ROWS * c
        pad = S(10)
        q, b = self.heat(w)
        col = self.bezel_color(q, b)
        glow_a = 70 + int(185 * (q / 8) * (b / 3))
        gkey = ("spf", "wglow", q, b)
        gl = self.imgs.get(gkey)
        if gl is None:
            gw, gh = ww + 2 * pad + S(40), hh + 2 * pad + S(40)
            im = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
            ImageDraw.Draw(im).rounded_rectangle([S(20) - S(6), S(20) - S(6), gw - S(20) + S(6), gh - S(20) + S(6)], radius=S(18),
                                                 fill=col + (glow_a,))
            gl = self.imgs[gkey] = self.hd._surf(im.filter(ImageFilter.GaussianBlur(S(12))))
        screen.blit(gl, (x0 - pad - S(20), y0 - pad - S(20)))
        pg.draw.rect(screen, (30, 22, 18), (x0 - pad, y0 - pad, ww + 2 * pad, hh + 2 * pad), border_radius=S(14))
        pg.draw.rect(screen, col, (x0 - pad, y0 - pad, ww + 2 * pad, hh + 2 * pad), width=max(2, S(4 + 4 * (q / 8) * (b / 3))),
                     border_radius=S(14))
        pg.draw.rect(screen, (12, 14, 34), (x0 - S(3), y0 - S(3), ww + S(6), hh + S(6)), border_radius=S(8))
        dot = (40, 46, 90)
        for r in range(ROWS):
            for k in range(COLS):
                pg.draw.rect(screen, dot, (x0 + k * c + c // 2 - 1, y0 + r * c + c // 2 - 1, 2, 2))
        if w.grid is None or self.hidden(w, now):
            return
        done = set()
        for r0, k0, bw, bh, bcol in w.blocks:                         # the power gems / les gemmes de puissance
            for a in range(bh):
                for b in range(bw):
                    done.add((r0 + a, k0 + b))
            r1 = max(r0, 1)
            vh = bh - (r1 - r0)
            if vh <= 0:
                continue
            surf = self.block(bcol, bw, vh)
            x, y = x0 + k0 * c, y0 + (r1 - 1) * c
            lt = max((w.land.get((r0 + a, k0 + b), -99.0) for a in range(bh) for b in range(bw)), default=-99.0)
            if now - lt < LAND:
                y -= int(c * 0.5 * (1 - (now - lt) / LAND) ** 2)
            screen.blit(surf, (x, y))
            st = w.shine.get((r0, k0, bw, bh))
            if st is not None and now - st < 0.9:
                self.sweep(screen, x, y, bw * c, vh * c, (now - st) / 0.9)
        for r in range(1, 14):
            for k in range(COLS):
                if (r, k) in done:
                    continue
                g = decode(w.grid[r][k])
                if not g:
                    continue
                x, y = x0 + k * c, y0 + (r - 1) * c
                lt = w.land.get((r, k))
                if lt is not None and now - lt < LAND:
                    y -= int(c * 0.6 * (1 - (now - lt) / LAND) ** 2)
                kind = g[0]
                if kind == "burst":
                    k2 = 0.5 + 0.5 * math.sin(now * 40)
                    pg.draw.rect(screen, mix(COLORS.get(g[1], WHITE), WHITE, 0.5 + 0.5 * k2), (x + S(3), y + S(3), c - S(6), c - S(6)),
                                 border_radius=S(6))
                    continue
                if kind == "power":
                    surf = self.gem("gem", g[1])
                elif kind == "counter":
                    surf = self.gem("counter", g[1], g[2])
                else:
                    surf = self.gem(kind, g[1])
                fl = w.flip.get((r, k))
                if fl is not None and now - fl[1] < FLIP:
                    t = (now - fl[1]) / FLIP
                    if t < 0.5:
                        surf = self.gem("counter", fl[0], 1)
                    sx = abs(math.cos(math.pi * t))
                    s2 = self.pg.transform.smoothscale(surf, (max(1, int(c * sx)), c))
                    screen.blit(s2, (x + (c - s2.get_width()) // 2, y))
                    continue
                tk = w.tick.get((r, k))
                if tk is not None and now - tk < 0.25:
                    sc = 1 + 0.18 * math.sin(math.pi * (now - tk) / 0.25)
                    self.blit_c(screen, surf, x + c / 2, y + c / 2, sc)
                    continue
                screen.blit(surf, (x, y))
        self.draw_fall(screen, side, vals, x0, y0, now)
        atk = self.atk[1 - side]                                       # the attack coming to this well / qui arrive
        if atk > 0:
            self.draw_incoming(screen, x0, y0, atk, now)

    def sweep(self, screen, x, y, w, h, t):
        """A golden shine sweeping a power gem that formed. / Un éclat doré qui balaie une gemme de puissance."""
        key = ("spf", "band", h)
        band = self.imgs.get(key)
        if band is None:
            bw = max(4, self.S(46))
            im = Image.new("RGBA", (bw + h, h), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            for i in range(bw):
                a = int(200 * math.sin(math.pi * i / bw))
                d.line([(i + h, 0), (i, h)], fill=(255, 246, 200, a))
            band = self.imgs[key] = self.hd._surf(im)
        old = screen.get_clip()
        screen.set_clip(self.pg.Rect(x, y, w, h).clip(old))
        bx = x - band.get_width() + (w + band.get_width()) * t
        screen.blit(band, (int(bx), y))
        screen.set_clip(old)
        if t < 0.25:
            self.pg.draw.rect(screen, (255, 240, 180), (x, y, w, h), width=max(2, self.S(4)), border_radius=self.S(8))

    def draw_fall(self, screen, side, vals, x0, y0, now):
        """The pair that falls, where the game has it, gliding from one row to the next. / La paire qui tombe."""
        pair = vals.get("pair1" if side == 0 else "pair2")
        x, y = _n(vals.get("x1" if side == 0 else "x2")), _n(vals.get("y1" if side == 0 else "y2"))
        if not isinstance(pair, list) or len(pair) < 2 or x is None or y is None or not 3 <= y <= 15 or not 0 <= x < COLS:
            self.fall[side] = None
            return
        rot = _n(vals.get("rot1" if side == 0 else "rot2")) or 0
        f = self.fall[side]
        if f is None or abs(f[0] - x) > 2 or abs(f[1] - y) > 3:
            f = (float(x), float(y))
        k = min(1.0, self.dt * 18)
        f = (f[0] + (x - f[0]) * k, f[1] + (y - f[1]) * k)
        self.fall[side] = f
        c = self.cell()
        # the pivot (first gem) at (x, y), the other one around it: above, right, below, left with the turns, as the
        # pairs landed in two recorded games / le pivot à (x, y), l'autre autour selon la rotation
        a, b = decode(pair[0] & 0xFF), decode(pair[1] & 0xFF)
        dx, dy = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}.get(rot, (0, -1))
        for g, (ox, oy) in ((a, (0, 0)), (b, (dx, dy))):
            if not g:
                continue
            r = f[1] - 1 + oy
            if r < 1:
                continue
            surf = self.gem(g[0] if g[0] in ("crash", "diamond") else "gem", g[1])
            screen.blit(surf, (int(x0 + (f[0] + ox) * c), int(y0 + (r - 1) * c)))

    def draw_incoming(self, screen, x0, y0, n, now):
        """The counter gems about to fall here, lined up at the top as the game warns. / En attente en haut du puits."""
        S, c = self.S, self.cell()
        k = 0.6 + 0.4 * math.sin(now * 9)
        band = self.imgs.get(("spf", "inband"))
        if band is None:
            im = Image.new("RGBA", (COLS * c + S(8), int(c * 0.9) + S(8)), (0, 0, 0, 0))
            ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=S(8), fill=(140, 0, 24, 190))
            band = self.imgs[("spf", "inband")] = self.hd._surf(im)
        band.set_alpha(int(255 * k))
        screen.blit(band, (x0 - S(4), y0 - S(4)))
        cc = self.S(CELL * 0.72)
        for i in range(min(4, n)):
            surf = self.img(("spf", "mini", i % 4 + 1), cc, cc, counter_draw(COLORS[i % 4 + 1], 5, self.hd.font("black", int(cc * 0.62 * 3))))
            screen.blit(surf, (x0 + S(4) + i * (cc + S(3)), y0 + S(1)))
        t = self.hd.text(f"+{n}", "black", S(26), WHITE, glow=0, outline=(90, 0, 0), stroke=max(2, S(3)))
        self.hd.put(screen, t, x0 + COLS * c - S(6), y0 + c * 0.42, "right", "middle")

    def draw_middle(self, screen, vals, now):
        """Between the wells: the next pairs, VS, the rounds won. / Entre les puits : les paires suivantes, VS, les manches."""
        pg, S, c, hd = self.pg, self.S, self.cell(), self.hd
        cx = self.W / 2
        y0 = S(TOP)
        box = (int(cx - S(62)), int(y0 - S(2)), S(124), int(2 * c + S(48)))
        dia = any(isinstance(p, list) and len(p) >= 4 and 5 in (p[2] & 0xFF, p[3] & 0xFF) for p in (vals.get("pair1"), vals.get("pair2")))
        if dia:                                                       # a diamond is coming / un diamant arrive
            k = 0.5 + 0.5 * math.sin(now * 6)
            for i, rgb in enumerate(((255, 120, 140), (255, 220, 120), (140, 240, 170), (130, 190, 255))):
                pg.draw.rect(screen, rgb, (box[0] - S(3 + i * 2) - int(k * S(2)), box[1] - S(3 + i * 2), box[2] + S(6 + i * 4) + int(2 * k * S(2)),
                                           box[3] + S(6 + i * 4)), width=max(1, S(2)), border_radius=S(14))
        pg.draw.rect(screen, (16, 10, 26), box, border_radius=S(12))
        pg.draw.rect(screen, GOLD, box, width=max(1, S(2)), border_radius=S(12))
        hd.put(screen, hd.text("NEXT", "xbold", S(17), GOLD, glow=0), cx, y0 + S(14), "center", "middle")
        for side, px in ((0, cx - c - S(10)), (1, cx + S(10))):
            p = vals.get("pair1" if side == 0 else "pair2")
            if not isinstance(p, list) or len(p) < 4:
                continue
            for i, v in enumerate((p[3] & 0xFF, p[2] & 0xFF)):         # the top one first / celle du haut d'abord
                g = decode(v)
                if g:
                    screen.blit(self.gem(g[0] if g[0] in ("crash", "diamond") else "gem", g[1]), (int(px), int(y0 + S(30) + i * c)))
        vs_y = y0 + 2 * c + S(104)
        k = 1.0 + 0.04 * math.sin(now * 3)
        self.blit_c(screen, self.metal("VS", 76, "vs"), cx, vs_y, k)
        for side in (0, 1):                                            # the rounds won / les manches gagnées
            won = self.wins[side]
            col = P1C if side == 0 else P2C
            for i in range(2):
                x = cx - S(34) if side == 0 else cx + S(34)
                y = vs_y + S(50) + i * S(36)
                if i < won:
                    pulse = 1.0
                    if self.win_side[0] == side and now - self.win_side[1] < 0.6 and i == won - 1:
                        pulse = 1 + 0.6 * (1 - (now - self.win_side[1]) / 0.6)
                    self.blit_c(screen, self.img(("spf", "pip", side), S(30), S(30), gem_draw(col)), x, y, pulse)
                else:
                    r = S(13)
                    pg.draw.polygon(screen, _mix(col, (60, 40, 60), 0.35), [(x, y - r), (x + r, y), (x, y + r), (x - r, y)], max(2, S(3)))
        if self.humans(vals) or any(self.vs):                          # the matches of two humans / les matchs
            y = vs_y + S(146)
            hd.put(screen, hd.text(tr("MATCHS", "MATCHES"), "xbold", S(15), GOLD, glow=0), cx, y - S(22), "center", "middle")
            for side in (0, 1):
                pop = self.vs_pop[side]
                sc = 1 + 0.7 * max(0.0, 1 - (now - pop) / 0.5)
                t = hd.text(str(self.vs[side]), "black", S(34), P1C if side == 0 else P2C, glow=0, outline=(10, 6, 16), stroke=max(2, S(3)))
                hd.put(screen, t, cx + (-S(32) if side == 0 else S(32)), y + S(6), "center", "middle", scale=sc)
            hd.put(screen, hd.text("-", "black", S(30), WHITE, glow=0), cx, y + S(4), "center", "middle")

    def draw_credit(self, screen, eng, vals, now):
        """The credits at the bottom between the wells, small enough to fit there: CRÉDITS, the coin and the number.
        The coins put in fall onto that coin. / Les crédits en bas entre les puits : CRÉDITS, la pièce et le nombre ;
        les pièces mises tombent sur cette pièce."""
        c = _n(vals.get("credits"))
        if c is None:
            return
        S, hd, cb = self.S, self.hd, self.cbar
        cb.set_symbol((getattr(eng, "cfg", None) or {}).get("coin_symbol", "€"))
        cx = self.W / 2
        y = S(TOP) + ROWS * self.cell() - S(22)
        size = S(34)
        key = ("spf", "coin", cb.symbol, size)
        ic = self.imgs.get(key)
        if ic is None:
            ic = self.imgs[key] = self.pg.transform.smoothscale(cb.icon, (size, size))
        bump = max(0.0, 1 - (now - cb.coin_t) / 0.35)
        n, t = cb.said
        if now - t < 1.3:                                     # +1 CRÉDIT in place of the word, no room above / à la place du mot
            hd.put(screen, hd.text(credits_word(n), "stencil", S(16), GOLD, glow=0.5), cx, y - S(30), "center", "middle")
        else:
            hd.put(screen, hd.text(tr("CRÉDITS", "CREDITS"), "stencil", S(16), CREAM, glow=0), cx, y - S(30), "center", "middle")
        ix = cx - S(26)
        screen.blit(ic, (int(ix - size / 2), int(y - size / 2 - bump * S(6))))
        cb.xy, cb.box = (ix, y), None
        hd.put_number(screen, f"{int(c):02d}", "stencil", S(34), GOLD, cx + S(22), y, "center", "middle", scale=1 + 0.3 * bump, glow=0.45)

    def draw_score(self, screen, eng, name, x, y, size):
        """The score centred on its digits in its box, popping as it changes. / Le score centré sur ses chiffres."""
        v = eng.state.values.get(name)
        if v is None:
            return
        pop = 0.0
        t = eng.state.changed_at.get(name)
        if t is not None and 0 <= eng.ctx.t - t < 0.25:
            pop = 1 - (eng.ctx.t - t) / 0.25
        self.hd.put(screen, self.hd.text(str(v), "black", size, (255, 232, 170)), x, y, "center", "middle", scale=1 + 0.2 * pop)

    def draw_panel(self, screen, eng, side, vals, now):
        """A player's panel: the name, the score, the chains, the power gems, DANGER. / Le panneau d'un joueur."""
        pg, S, hd = self.pg, self.S, self.hd
        w = self.wells[side]
        px = self.panel_x(side)
        name = vals.get("p1_char" if side == 0 else "p2_char")
        playing = vals.get("p1_mode" if side == 0 else "p2_mode") in (1, 2)
        if isinstance(name, str) and name:
            ws = self.win_side
            sc = 1.0
            if ws[0] == side and now - ws[1] < 0.5:
                sc = 1 + 0.25 * math.sin(math.pi * (now - ws[1]) / 0.5)
            self.blit_c(screen, self.metal(name, 78, side), px, S(80), sc)
        if not playing and vals.get("p1_mode") in (1, 2):
            hd.put(screen, hd.text("CPU", "xbold", S(22), (190, 190, 210), glow=0), px, S(126), "center", "middle")
        col = P1C if side == 0 else P2C
        bw, bh = S(400), S(100)
        bx, by = int(px - bw / 2), S(144)
        k = _clamp(self.beat(w)) if w.danger >= 0.5 else 0.0
        bcol = mix(col, (255, 40, 40), k)
        pg.draw.rect(screen, mix((12, 8, 22), (90, 0, 10), 0.6 * k), (bx, by, bw, bh), border_radius=S(16))
        pg.draw.rect(screen, _mix(bcol, (0, 0, 0), 0.25 * (1 - k)), (bx, by, bw, bh), width=max(2, S(3 + 3 * k)), border_radius=S(16))
        self.draw_score(screen, eng, "score" if side == 0 else "score_p2", px, by + bh / 2, S(84))
        # DANGER, beating with the heart / DANGER, au rythme du coeur
        if w.danger > 0.55:
            k = _clamp(self.beat(w))
            t = hd.text("DANGER", "black", S(58), mix((255, 60, 40), WHITE, 0.55 * k), glow=0, outline=(70, 0, 0), stroke=max(2, S(5)))
            hd.put(screen, t, px, S(282), "center", "middle", scale=1 + 0.22 * k)
        # the chain / la chaîne
        n, t0 = self.chain[side]
        if n >= 2 and now - t0 < 1.8:
            dt = now - t0
            sc = 1.7 - 0.7 * min(1, dt / 0.16) + (0.12 * math.sin(dt * 30) * max(0, 1 - dt / 0.5))
            a = 1.0 if dt < 1.4 else 1 - (dt - 1.4) / 0.4
            ccol = CHAIN_COLS.get(min(5, n), (255, 110, 60))
            self.blit_c(screen, self.metal(f"{n} CHAIN !", 58 + 6 * min(4, n), ccol), px, S(338), sc, a)
        # the last power gem / la dernière gemme de puissance
        p = self.power[side]
        if p is not None and now - p[2] < 2.2:
            dt = now - p[2]
            a = 1.0 if dt < 1.8 else 1 - (dt - 1.8) / 0.4
            self.blit_c(screen, self.metal(f"POWER GEM {p[0]}x{p[1]}", 34, "gold", key="black"), px, S(404), 1 + 0.3 * max(0, 1 - dt / 0.2), a)
        else:
            pcs = _n(vals.get("pcs1" if side == 0 else "pcs2"))
            if pcs is not None and playing:
                left = 25 - pcs % 25
                screen.blit(self.gem("diamond", 0), (int(px - S(130)), S(392)))
                t = hd.text(tr(f"DIAMANT DANS {left}", f"DIAMOND IN {left}"), "xbold", S(26), (226, 238, 255), glow=0)
                hd.put(screen, t, px - S(88), S(408), "left", "middle")


SCENES = {"spf2t": SpfScene}
