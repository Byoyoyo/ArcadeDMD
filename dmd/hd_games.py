"""HD scenes of the Neo Geo games done one by one (1.17): Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers,
Neo Turf Masters. Each game has its own animated backdrop and reacts to the values read in its memory: the ship
fires and explodes, the bubble leaves the launcher, the disc flies into the goal, the grenade blows up, the ball
flies to the green. When the player's stick and buttons can be read (Neo Geo BIOS), the ship and the launcher
follow them. Nobody playing: the game's logo and the coin doors. Everything is drawn by the program.

Scènes HD des jeux Neo Geo faits un par un (1.17). Chaque jeu a son décor animé et réagit aux valeurs lues
dans sa mémoire. Quand le stick et les boutons du joueur se lisent (BIOS Neo Geo), le vaisseau et le lanceur
les suivent. Personne ne joue : le logo du jeu et les monnayeurs. Tout est dessiné par le programme.
"""

import math
import random
import time

from PIL import Image, ImageDraw

from . import hd_themes
from .hd_bg import Backdrop
from .hd_coin import CoinDoors
from .hd_fx import FIRE, FIRE_HOT, FX
from .i18n import tr

GOLD = (255, 214, 120)
AMBER = (255, 168, 48)
WHITE = (255, 255, 255)
CREAM = (238, 228, 208)
RED = (255, 64, 44)
GREY = (150, 156, 170)
P1C, P2C = (255, 120, 60), (70, 170, 255)
UP, DOWN, LEFT, RIGHT, BTN_A, BTN_B = 0x01, 0x02, 0x04, 0x08, 0x10, 0x20     # BIOS_P1CURRENT / BIOS_P2CURRENT


def _n(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def _clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else (hi if v > hi else v)


def draw_img(w, h, fn, ss=3):
    """Pillow drawing made three times bigger then reduced (smooth edges). / Dessin fait en grand puis réduit."""
    W_, H_ = max(1, int(w * ss)), max(1, int(h * ss))
    img = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    fn(ImageDraw.Draw(img), W_, H_)
    return img.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS)


def chunk_draw(color):
    def fn(d, W, H):
        d.polygon([(0.1 * W, 0.3 * H), (0.6 * W, 0.0), (W, 0.45 * H), (0.7 * W, H), (0.2 * W, 0.85 * H)], fill=color + (255,))
        d.line([(0.1 * W, 0.3 * H), (0.6 * W, 0.0), (W, 0.45 * H)], fill=_mix(color, WHITE, 0.4) + (255,), width=max(1, int(W * 0.12)))
    return fn


# ============================================================================ base commune
class GameScene:
    """Backdrop, effects, the attract screen with the coin doors, the top bar, banners, labels on a dark pill."""
    THEME = "space"
    FPS = 50
    STATIC = False                # True: the backdrop does not scroll / le décor ne défile pas
    SHADE = (120, 120)            # dark veil at the top and the bottom (0 to 255): texts readable on a bright backdrop
    EXPLOSIONS = False            # True: explosion glows prepared during the calm moments
    BANNERS = (("GAME OVER", RED),)                          # banner texts prepared in advance
    PILLS = False                 # True: dark pills under the texts of the top bar (bright backdrop)

    def __init__(self, hd, rng=None):
        self.hd, self.pg, self.S, self.s = hd, hd.pg, hd.S, hd.s
        self.W, self.H = hd.W, hd.H
        self.rng = rng or random.Random()
        self.fx = FX(hd, random.Random(self.rng.random()))
        self.bd = Backdrop(hd, self.THEME, random.Random(self.rng.random()), threaded=False)
        self.bd.static = self.STATIC
        self.bd.prebuild([self.THEME])                       # built in the background: no jolt when the game starts
        self.made = time.monotonic()
        self.prev = {}
        self.imgs = {}
        self.pills = {}
        self.shades = {}
        self.buf = None
        self.banner = None
        self.pops = []                                       # texts that pop up on a dark pill
        self.key = None
        self.was_idle = True
        self.boost = (0.0, -99.0)                            # (backdrop speed added, until)
        self.last = None
        self.dt = 0.0
        self.touched = set()                                 # players who touched their stick or buttons
        self.modes = {}                                      # BIOS player modes seen at the previous image
        for i, col in enumerate(((120, 124, 138), (88, 90, 102), (150, 120, 90))):
            self.fx.sp.register(f"chunk{i}", draw_img(self.S(14 + 5 * i), self.S(12 + 4 * i), chunk_draw(col)))
        self.warm = self._warm_list()

    # ------------------------------------------------------------ préparé d'avance
    def _warm_list(self):
        hd, S, sp, s = self.hd, self.S, self.fx.sp, self.s
        out = [(hd.text, (text, "stencil", S(100), col, 0.8)) for text, col in self.BANNERS]
        if self.EXPLOSIONS:
            for color, rmax in (((255, 130, 50), 256), (FIRE, 128), (FIRE_HOT, 128), ((255, 110, 40), 128), ((255, 236, 190), 100)):
                for r in (16, 20, 25, 32, 40, 50, 64, 80, 100, 128, 160, 200, 256):
                    if r > rmax:
                        break
                    for lv in range(12, 0, -1):
                        out.append((sp.glow, (r * s, color, lv, 0.35)))
            for color in ((58, 52, 62), (120, 70, 40), (150, 140, 140)):
                for r in (13, 16, 20, 25, 32, 40, 50, 64, 80, 100):
                    for v in range(3):
                        out.append((sp.puff, (r * s, color, v)))
        return out

    def _warm_step(self, budget):
        end = time.perf_counter() + budget
        while self.warm and time.perf_counter() < end:
            fn, args = self.warm.pop(0)
            try:
                fn(*args)
            except Exception:
                self.warm = []

    # ------------------------------------------------------------ outils
    def img(self, key, w, h, fn, ss=3, flip=False):
        s = self.imgs.get(key)
        if s is None:
            im = draw_img(w, h, fn, ss)
            s = self.imgs[key] = self.hd._surf(im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im)
        return s

    def rotated(self, key, surf, angle, step=2):
        """Picture turned, kept by steps of a few degrees. / Image tournée, gardée en cache."""
        a = int(round(angle / step)) * step
        k = ("rot", key, a)
        r = self.imgs.get(k)
        if r is None:
            r = self.imgs[k] = surf if a == 0 else self.pg.transform.rotozoom(surf, a, 1.0)
        return r

    def changed(self, vals, name):
        """(before, after) when the value changed since the previous image, else None."""
        new, old = _n(vals.get(name)), _n(self.prev.get(name))
        if new is None or old is None or new == old:
            return None
        return old, new

    @staticmethod
    def nobody(vals):
        p1m, p2m = vals.get("p1_mode"), vals.get("p2_mode")
        return p1m is not None and p1m not in (1, 2) and p2m not in (1, 2)

    @staticmethod
    def p2_in(vals):
        return vals.get("p2_mode") in (1, 2)

    @staticmethod
    def p1_in(vals):
        return vals.get("p1_mode") in (1, 2) or vals.get("p1_mode") is None

    def stick(self, vals, side):
        """(dx, dy, buttons) from the Neo Geo BIOS (p1_input / p2_input). None while the player has not touched them
        yet (game demo, or a game that does not use the BIOS for its inputs): the scene then plays by itself.
        / Stick et boutons du joueur ; tant qu'il n'y a pas touché, la scène joue toute seule."""
        v = _n(vals.get("p1_input" if side == "p1" else "p2_input"))
        if v is None:
            return None
        v = int(v)
        if v:
            self.touched.add(side)
        if side not in self.touched:
            return None
        return (1 if v & RIGHT else 0) - (1 if v & LEFT else 0), (1 if v & DOWN else 0) - (1 if v & UP else 0), v & 0xF0

    def text(self, screen, txt, x, y, size, color, key="black", align="left", valign="top", glow=0.5, scale=1.0, alpha=1.0):
        hd = self.hd
        return hd.put(screen, hd.text(str(txt), key, self.S(size), color, glow), x, y, align, valign, scale=scale, alpha=alpha)

    def pill(self, screen, x, y, w, h, alpha=150, radius=None):
        w = (int(w) + 7) // 8 * 8
        key = (w, int(h), alpha, radius)
        s = self.pills.get(key)
        if s is None:
            if len(self.pills) > 300:                            # widths follow the texts: the cache stays small
                self.pills.clear()
            s = self.pg.Surface((w, int(h)), self.pg.SRCALPHA)
            self.pg.draw.rect(s, (6, 8, 18, alpha), s.get_rect(), border_radius=int(h / 2) if radius is None else self.S(radius))
            self.pills[key] = s
        screen.blit(s, (int(x), int(y)))
        return w

    def label(self, screen, txt, x, y, size, color, key="xbold", align="left", glow=0.4, alpha=150, scale=1.0, fade=1.0):
        """Text on a dark pill, y = middle of the text. Returns the width of the pill."""
        hd, S = self.hd, self.S
        t = hd.text(str(txt), key, S(size), color, glow)
        px = S(size * 0.5)
        w, h = (t["w"] + 2 * px) * scale, (t["h"] + S(size * 0.62)) * scale
        x0 = x if align == "left" else (x - w / 2 if align == "center" else x - w)
        self.pill(screen, x0, y - h / 2, w, h, int(alpha * fade) // 10 * 10)
        hd.put(screen, t, x0 + w / 2, y, "center", "middle", scale=scale, alpha=fade)
        return w

    def popup(self, text, x, y, color, size=40, life=1.2, rise=60, key="black"):
        """Text that pops up, rises and fades, on a dark pill (readable on any backdrop)."""
        self.pops.append((text, x, y, color, size, self.fx.now, life, rise, key))

    def draw_pops(self, screen, now):
        keep = []
        for p in self.pops:
            text, x, y, color, size, t0, life, rise, key = p
            k = (now - t0) / life
            if k >= 1.0:
                continue
            keep.append(p)
            if k < 0:
                continue
            yy = y - rise * self.s * (1 - (1 - k) ** 2)
            pop = 1.0 + 0.45 * max(0.0, 1 - k / 0.12)
            fade = 1.0 if k < 0.7 else max(0.0, (1 - k) / 0.3)
            self.label(screen, text, x, yy, size, color, key=key, align="center", glow=0.5, alpha=170, scale=round(pop * 20) / 20,
                       fade=fade)
        self.pops = keep

    def box(self, screen, x, y, w, h, border, fill=(8, 10, 22, 196), radius=18, width=3):
        key = ("box", int(w), int(h), border, fill, radius)
        s = self.imgs.get(key)
        if s is None:
            S = self.S
            s = self.pg.Surface((int(w), int(h)), self.pg.SRCALPHA)
            self.pg.draw.rect(s, fill, s.get_rect(), border_radius=S(radius))
            self.pg.draw.rect(s, border + (230,), s.get_rect(), max(1, S(width)), border_radius=S(radius))
            self.imgs[key] = s
        screen.blit(s, (int(x), int(y)))

    def bar(self, screen, x, y, w, h, frac, color, back=(30, 20, 30)):
        pg = self.pg
        frac = _clamp(frac)
        r = max(2, int(h / 2))
        pg.draw.rect(screen, back, (int(x), int(y), int(w), int(h)), border_radius=r)
        if frac > 0:
            fw = max(int(h), int(w * frac))
            pg.draw.rect(screen, color, (int(x), int(y), fw, int(h)), border_radius=r)
            pg.draw.rect(screen, _mix(color, WHITE, 0.45), (int(x) + r, int(y) + max(1, int(h * 0.16)), max(1, fw - 2 * r),
                                                            max(1, int(h * 0.22))), border_radius=r)
        pg.draw.rect(screen, _mix(back, WHITE, 0.35), (int(x), int(y), int(w), int(h)), max(1, self.S(2)), border_radius=r)

    def shade(self, screen):
        """Dark veil at the top and the bottom, so the texts stay readable on a bright backdrop."""
        for where, a in zip(("top", "bottom"), self.SHADE):
            if a <= 0:
                continue
            surf = self.shades.get(where)
            if surf is None:                                     # multiplied: cheaper than an alpha blend
                h = self.S(170 if where == "top" else 150)
                col = Image.new("RGB", (1, h))
                for y in range(h):
                    k = y / max(1, h - 1)
                    k = 1 - k if where == "top" else k
                    v = 255 - int(a * k ** 1.5)
                    col.putpixel((0, y), (v, v, v))
                surf = self.shades[where] = self.hd._surf(col.resize((self.W, h)))
            screen.blit(surf, (0, 0 if where == "top" else self.H - surf.get_height()), special_flags=self.pg.BLEND_RGB_MULT)

    def slam(self, text, color, now, dur=1.4):
        self.banner = (text, color, now, dur)

    def draw_banner(self, screen, now):
        if self.banner is None:
            return
        text, color, t0, dur = self.banner
        k = now - t0
        if k > dur:
            self.banner = None
            return
        if k < 0:
            return
        hd, S, W = self.hd, self.S, self.W
        scale = 2.0 - min(1.0, k / 0.16)
        alpha = 1.0 if k < dur - 0.25 else max(0.0, (dur - k) / 0.25)
        band = self.imgs.get("_band")
        if band is None:
            band = self.imgs["_band"] = self.pg.Surface((W, S(124))).convert()
            band.fill((0, 0, 0))
        band.set_alpha(int(190 * alpha))
        screen.blit(band, (0, S(240) - band.get_height() // 2))
        hd.put(screen, hd.text(text, "stencil", S(100), color, glow=0.8), W / 2, S(240), "center", "middle", scale=scale, alpha=alpha)

    def invite(self, vals, now):
        return self.hd._invite(vals, now)

    def top_bar(self, screen, eng, vals, logo, now, right=True):
        """Top: P1 and the score on the left, the logo in the middle, player 2 or the invitation on the right."""
        hd, S, W = self.hd, self.S, self.W
        hd.draw_logo(screen, logo, W / 2, S(8), S(560), S(112), now)
        for side, name, col in (("p1", "score", P1C), ("p2", "score_p2", P2C)):
            if side == "p2" and (not right or not self.p2_in(vals)):
                continue
            sc = _n(vals.get(name))
            tag = "P1" if side == "p1" else "P2"
            w = hd.text(tag, "black", S(50), col)["w"] + (S(22) + hd.text(str(sc), "black", S(64), AMBER)["w"] if sc is not None else 0)
            x = S(30) if side == "p1" else W - S(30) - w
            if self.PILLS:
                self.pill(screen, x - S(18), S(6), w + S(36), S(80), 140)
            x += self.text(screen, tag, x, S(16), 50, col) + S(22)
            if sc is not None:
                hd._score(screen, eng, name, x, S(8), "left", S(64))
        if right and not self.p2_in(vals):
            word, col = self.invite(vals, now)
            if self.PILLS:
                self.label(screen, word, W - S(24), S(44), 36, col, align="right")
            else:
                self.text(screen, word, W - S(30), S(22), 40, col, key="xbold", align="right")

    # ------------------------------------------------------------ à chaque image (complété par chaque jeu)
    def always(self, vals, now):
        """Every image, even on the attract screen."""

    def restart(self, vals, now):
        """A game starts (or the attract screen ends): nothing fires for the values already there."""

    def update(self, vals, now):
        """Reacts to the values that change (only while somebody plays)."""

    def move(self, vals, now, idle):
        return 0.0

    def draw_hud(self, screen, eng, vals, logo, now):
        self.top_bar(screen, eng, vals, logo, now)

    def draw_attract(self, screen, eng, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        hd.draw_logo(screen, logo, W / 2, S(190), S(1000), S(220), now, valign="middle")
        if hd.coins_on:
            if hd.coins is None:
                hd.coins = CoinDoors(hd)
            hd.coins.draw(screen, vals, now, self.fx, (getattr(eng, "cfg", None) or {}).get("coin_symbol", "€"), hd.enter)
        else:
            word, col = self.invite(vals, now)
            self.label(screen, word, W / 2, S(372), 56, col, align="center")

    def render(self, screen, eng, now, logo):
        vals = eng.state.values
        key = eng.state.meta.get("game") or ""
        if key != self.key:
            self.key, self.prev, self.banner, self.was_idle, self.pops = key, {}, None, True, []
        self.dt = 0.0 if self.last is None else max(0.0, min(0.1, now - self.last))
        self.last = now
        self.fx.update(now)
        idle = self.nobody(vals)
        for side in ("p1", "p2"):                              # GAME OVER when a player's game ends
            m = vals.get(side + "_mode")
            if m == 3 and self.modes.get(side) in (1, 2):
                self.slam("GAME OVER", RED, now, 2.2)
            self.modes[side] = m
        self.always(vals, now)
        if not idle:
            if self.was_idle:
                self.prev = {k: v for k, v in vals.items() if _n(v) is not None}
                self.restart(vals, now)
            self.update(vals, now)
        self.was_idle = idle
        self.prev = {k: v for k, v in vals.items() if _n(v) is not None}
        ox, oy = self.fx.offset()
        target = screen
        if ox or oy:
            if self.buf is None or self.buf.get_size() != screen.get_size():
                self.buf = self.pg.Surface(screen.get_size()).convert()
            target = self.buf
        if self.bd.ready(self.bd.theme) or time.monotonic() - self.made > 4.0:
            mv = self.move(vals, now, idle)
            if now < self.boost[1]:
                mv += self.boost[0]
            self.bd.draw(target, now, mv)
        else:                                                  # backdrop still being built: the logo intro covers it
            target.fill((4, 4, 10))
        self.fx.draw(target, "back")
        self.shade(target)
        if idle:
            self.draw_attract(target, eng, vals, logo, now)
        else:
            self.draw_hud(target, eng, vals, logo, now)
            for side, x in (("p1", self.W * 0.27), ("p2", self.W * 0.73)):     # continue countdown of the game
                if vals.get(side + "_mode") == 2:
                    k = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(now * 6))
                    self.label(target, "CONTINUE ?", x, self.S(236), 60, GOLD, key="stencil", align="center", alpha=190, fade=k)
        self.fx.draw(target, "front")
        self.draw_pops(target, now)
        self.draw_banner(target, now)
        self.fx.draw_flash(target)
        if target is not screen:
            screen.fill((0, 0, 0))
            screen.blit(target, (ox, oy))
        if self.warm and len(self.fx.parts) < 100:
            self._warm_step(0.004)


# ============================================================================ Blazing Star
def ship_draw(accent, body=(226, 232, 246), dark=(28, 34, 62)):
    """Fighter seen from the side, nose to the right. / Chasseur de profil, nez à droite."""
    def fn(d, W, H):
        ow = max(2, int(H * 0.03))

        def P(pts, fill, outline=True):
            d.polygon([(x * W, y * H) for x, y in pts], fill=fill + (255,), outline=dark + (255,) if outline else None,
                      width=ow if outline else 0)
        P([(0.58, 0.42), (0.34, 0.05), (0.21, 0.05), (0.28, 0.42)], accent)                             # aile du fond
        P([(0.17, 0.42), (0.07, 0.18), (0.0, 0.18), (0.04, 0.44)], _mix(accent, (0, 0, 0), 0.15))        # dérive
        hull = [(0.02, 0.38), (0.6, 0.34), (0.86, 0.42), (1.0, 0.5), (0.86, 0.58), (0.6, 0.66), (0.02, 0.62)]
        P(hull, body, outline=False)
        P([(0.03, 0.5), (0.99, 0.5), (0.86, 0.575), (0.6, 0.65), (0.03, 0.61)], _mix(body, (70, 80, 120), 0.45), outline=False)
        d.line([(0.06 * W, 0.47 * H), (0.82 * W, 0.47 * H)], fill=accent + (255,), width=max(2, int(H * 0.045)))
        d.ellipse([0.56 * W, 0.355 * H, 0.82 * W, 0.5 * H], fill=(80, 200, 255, 255), outline=dark + (255,), width=ow)
        d.ellipse([0.62 * W, 0.38 * H, 0.72 * W, 0.42 * H], fill=(225, 250, 255, 255))
        d.line([(x * W, y * H) for x, y in hull + [hull[0]]], fill=dark + (255,), width=ow, joint="curve")
        P([(0.56, 0.58), (0.3, 0.95), (0.17, 0.95), (0.26, 0.58)], _mix(accent, (0, 0, 0), 0.28))       # aile de devant
        d.rectangle([0, 0.42 * H, 0.05 * W, 0.58 * H], fill=(70, 76, 96, 255), outline=dark + (255,), width=ow)
    return fn


def drone_draw(d, W, H):
    """Enemy drone coming from the right, its red eye in front. / Drone ennemi, l'œil rouge devant."""
    dark = (36, 22, 52, 255)
    ow = max(2, int(H * 0.05))
    d.polygon([(0.55 * W, 0.06 * H), (W, 0.28 * H), (0.72 * W, 0.5 * H), (W, 0.72 * H), (0.55 * W, 0.94 * H)],
              fill=(104, 58, 140, 255), outline=dark, width=ow)
    d.ellipse([0.04 * W, 0.16 * H, 0.8 * W, 0.84 * H], fill=(140, 136, 168, 255), outline=dark, width=ow)
    d.ellipse([0.14 * W, 0.22 * H, 0.68 * W, 0.48 * H], fill=(196, 192, 222, 255))
    d.ellipse([0.1 * W, 0.34 * H, 0.38 * W, 0.66 * H], fill=(255, 64, 44, 255), outline=dark, width=ow)
    d.ellipse([0.16 * W, 0.4 * H, 0.24 * W, 0.48 * H], fill=(255, 220, 200, 255))


class BlazingStarScene(GameScene):
    THEME = "space"
    SHADE = (110, 120)
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS + tuple((f"ROUND {n}", GOLD) for n in range(1, 8))
    ZONE = (150, 318)                                   # band where the ships fly / bande où volent les vaisseaux
    ACC = {"p1": (60, 170, 255), "p2": (255, 150, 50)}

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.ships = {side: {"x": 0.25, "y": 0.3 if side == "p1" else 0.75, "tx": 0.3, "ty": 0.5, "next": 0.0, "vy": 0.0,
                             "t_dead": -99.0, "t_spawn": -99.0, "fire": 0.0, "in": False} for side in ("p1", "p2")}
        self.enemies = []
        self.next_enemy = 0.0

    def ship_surf(self, side):
        return self.img("ship_" + side, self.S(176), self.S(78), ship_draw(self.ACC[side]))

    def restart(self, vals, now):
        self.enemies = []
        self.next_enemy = now + 1.0
        for P in self.ships.values():
            P["in"] = False

    def move(self, vals, now, idle):
        return 0.15 if idle else 0.8

    def pos(self, side, now):
        P, S = self.ships[side], self.S
        bx = S(170) + P["x"] * S(640)
        by = S(self.ZONE[0]) + P["y"] * S(self.ZONE[1] - self.ZONE[0])
        k = (now - P["t_spawn"]) / 0.8                               # comes back in from the left
        if 0 <= k < 1:
            bx = -S(200) + (bx + S(200)) * (1 - (1 - k) ** 3)
        return bx, by

    def _steer(self, side, vals, now, dt):
        P = self.ships[side]
        st = self.stick(vals, side)
        old = P["y"]
        if st is not None:                                            # the player's stick (Neo Geo BIOS)
            dx, dy, btn = st
            P["x"] = _clamp(P["x"] + dx * dt * 0.6)
            P["y"] = _clamp(P["y"] + dy * dt * 1.1)
            firing = bool(btn & BTN_A)
        else:                                                         # autopilot / pilote automatique
            if now >= P["next"]:
                P["tx"], P["ty"] = self.rng.uniform(0.0, 0.75), self.rng.uniform(0.0, 1.0)
                P["next"] = now + self.rng.uniform(1.2, 2.6)
            P["x"] += (P["tx"] - P["x"]) * min(1.0, dt * 1.5)
            P["y"] += (P["ty"] - P["y"]) * min(1.0, dt * 1.8)
            firing = (now % 2.4) < 1.5
        P["vy"] = (P["y"] - old) / dt if dt > 0 else 0.0
        return firing

    def update(self, vals, now):
        fx, S, dt = self.fx, self.S, self.dt
        for side, suf in (("p1", ""), ("p2", "_p2")):
            P = self.ships[side]
            playing = self.p1_in(vals) if side == "p1" else self.p2_in(vals)
            if not playing:
                P["in"] = False
                continue
            if not P["in"]:                                           # the ship flies in
                P["in"], P["t_spawn"] = True, now
            firing = self._steer(side, vals, now, dt)
            alive = now - P["t_dead"] > 1.2 and now >= P["t_spawn"]
            ch = self.changed(vals, "lives" + suf)
            if ch and ch[1] < ch[0] and alive:                        # a life lost: the ship explodes
                x, y = self.pos(side, now)
                fx.explosion(x, y, 0.9, layer_back=False)
                self.popup(tr("-1 VIE", "-1 LIFE"), x, y - S(70), RED, 36)
                P["t_dead"], P["t_spawn"] = now, now + 1.2
                alive = False
            elif ch and ch[1] > ch[0]:
                x, y = self.pos(side, now)
                self.popup("1UP !", x, y - S(70), (140, 255, 150), 40)
            ch = self.changed(vals, "power" + suf)
            if ch and ch[1] > ch[0] and alive:
                x, y = self.pos(side, now)
                self.popup("POWER UP", x, y - S(64), GOLD, 40)
                fx.glow(x, y, 30, 170, (120, 220, 255), 0.5, "front", 0.9, 0.0)
                fx.sparks(x, y, 18, (160, 230, 255), (200, 600), (0, 360), (0.3, 0.6), 0, "front", 3, 24)
            pw = int(_n(vals.get("power" + suf)) or 0)
            if alive and firing and now >= P["fire"]:
                P["fire"] = now + (0.075 if pw >= 3 else 0.11)
                self._fire(side, pw, now)
        for name in ("score", "score_p2"):                            # points scored: the enemy in front blows up
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0]:
                ahead = [e for e in self.enemies if S(420) < e["x"] < self.W * 0.78 and not e.get("dead")]
                if ahead:
                    self._boom(min(ahead, key=lambda e: e["x"]))
        ch = self.changed(vals, "round")
        if ch:
            self.slam(f"ROUND {int(ch[1])}", GOLD, now, 1.6)
            self.boost = (3.0, now + 1.8)
            self.fx.flash((140, 200, 255), 0.25, 0.4)
        if now >= self.next_enemy:                                    # enemies alone or in a line of three
            self.next_enemy = now + self.rng.uniform(1.0, 2.2)
            y, v, ph = self.rng.uniform(S(self.ZONE[0]), S(self.ZONE[1])), self.rng.uniform(230, 330) * self.s, self.rng.uniform(0, 6)
            for i in range(self.rng.choice((1, 1, 3))):
                self.enemies.append({"x": self.W + S(60) + i * S(110), "y": y, "ph": ph + i * 0.5, "v": v, "hp": 3, "hit": -99.0})

    def _fire(self, side, pw, now):
        x, y = self.pos(side, now)
        fx, S = self.fx, self.S
        col = (130, 230, 255) if side == "p1" else (255, 200, 120)
        mx = x + S(84)
        end = self.W + S(60)
        fx.muzzle(mx, y, 1, 0.55, col)
        lanes = (0,) if pw <= 0 else ((-1, 1) if pw == 1 else (-1, 0, 1))
        width, length = (6, 170) if pw >= 3 else (4, 110)
        for k in lanes:
            sy = y + k * S(9)
            ty = sy + (k * S(70) if pw >= 2 else 0)
            target = None
            for e in self.enemies:                                    # an enemy in the line of fire is hit
                if e.get("dead") or e["x"] <= mx:
                    continue
                ly = sy + (ty - sy) * (e["x"] - mx) / max(1, end - mx)
                if abs(e.get("yy", e["y"]) - ly) < S(26) and (target is None or e["x"] < target["x"]):
                    target = e
            if target is not None:
                fx.tracer(mx, sy, target["x"], target.get("yy", target["y"]), speed=3400, color=col, width=width, length=length)
                target["hp"] -= 1
                target["hit"] = now
                if target["hp"] <= 0:
                    fx.later(0.12, self._boom, target)
            else:
                fx.tracer(mx, sy, end, ty, speed=3400, color=col, width=width, length=length, impact=False)

    def _boom(self, e):
        if e.get("dead"):
            return
        e["dead"] = True
        self.fx.explosion(e["x"], e.get("yy", e["y"]), 0.55, layer_back=False)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg, dt = self.S, self.W, self.pg, self.dt
        drone = self.img("drone", S(74), S(50), drone_draw)
        keep = []
        for e in self.enemies:                                         # enemies coming from the right
            if e.get("dead"):
                continue
            e["x"] -= e["v"] * dt
            if e["x"] < -S(100):
                continue
            e["yy"] = e["y"] + math.sin(now * 2.4 + e["ph"]) * S(16)
            keep.append(e)
            screen.blit(drone, (int(e["x"] - drone.get_width() / 2), int(e["yy"] - drone.get_height() / 2)))
            g = self.fx.sp.glow(S(22), (255, 70, 50), 6 + 3 * math.sin(now * 8 + e["ph"]), hot=0.5)
            screen.blit(g, (int(e["x"] - S(13) - g.get_width() / 2), int(e["yy"] - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            if now - e["hit"] < 0.06:
                h = self.fx.sp.glow(S(40), (255, 255, 255), 8, hot=0.6)
                screen.blit(h, (int(e["x"] - h.get_width() / 2), int(e["yy"] - h.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        self.enemies = keep
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"] or now - P["t_dead"] < 1.2 or now < P["t_spawn"]:
                continue
            if now - P["t_spawn"] < 1.6 and int(now * 14) % 2 == 0:    # blinking after coming back
                continue
            x, y = self.pos(side, now)
            ship = self.rotated("ship_" + side, self.ship_surf(side), _clamp(-P["vy"] * 6, -10, 10))
            fl = self.fx.sp.glow(S(18) + S(4) * math.sin(now * 40), self.ACC[side], 10, hot=0.8)
            screen.blit(fl, (int(x - S(92) - fl.get_width() / 2), int(y - fl.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            screen.blit(ship, (int(x - ship.get_width() / 2), int(y - ship.get_height() / 2)))
        self.top_bar(screen, eng, vals, logo, now)
        for side, x0, d in (("p1", S(36), 1), ("p2", W - S(36), -1)):
            if side == "p2" and not self.p2_in(vals):
                continue
            suf = "" if side == "p1" else "_p2"
            pw = _n(vals.get("power" + suf))
            if pw is not None:                                         # power: four pips
                lx = x0 if d > 0 else x0 - S(332)
                self.text(screen, "POWER", lx, S(352), 26, CREAM, key="bold", glow=0)
                for i in range(4):
                    on = i <= int(pw)
                    pg.draw.rect(screen, (255, 210, 60) if on else (58, 48, 30), (lx + S(124) + i * S(52), S(350), S(44), S(28)),
                                 border_radius=S(6))
                    if on:
                        pg.draw.rect(screen, (255, 244, 190), (lx + S(130) + i * S(52), S(354), S(32), S(6)), border_radius=S(3))
            lives = _n(vals.get("lives" + suf))
            if lives is not None:                                      # lives: small ships
                icon = self.img("life_" + side, S(58), S(26), ship_draw(self.ACC[side]))
                n = int(lives)
                for i in range(min(7, n)):
                    xx = x0 + i * S(64) if d > 0 else x0 - (i + 1) * S(64)
                    screen.blit(icon, (int(xx), S(398)))
                if n > 7:
                    self.text(screen, f"+{n - 7}", x0 + d * 7 * S(64), S(400), 28, CREAM, align="left" if d > 0 else "right")
        rnd = _n(vals.get("round"))
        if rnd is not None:
            self.text(screen, f"ROUND {int(rnd)}", W / 2, S(404), 46, GOLD, key="stencil", align="center", valign="middle")


# ============================================================================ Puzzle Bobble
BUBBLE_RGB = ((48, 108, 255), (255, 58, 48), (255, 212, 0), (48, 210, 74), (176, 80, 255), (255, 138, 26), (66, 66, 78),
              (200, 200, 210))


def bubble_draw(color):
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=_mix(color, (0, 0, 0), 0.45) + (255,))
        for i in range(12):
            k = i / 12
            r = (W / 2) * (0.94 - k * 0.6)
            cx, cy = W / 2 - W * 0.1 * k, H / 2 - H * 0.1 * k
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_mix(color, WHITE, k * 0.5) + (255,))
        d.ellipse([W * 0.2, H * 0.14, W * 0.44, H * 0.34], fill=(255, 255, 255, 230))
        d.ellipse([W * 0.62, H * 0.66, W * 0.72, H * 0.74], fill=(255, 255, 255, 110))
        d.ellipse([0, 0, W - 1, H - 1], outline=_mix(color, (0, 0, 0), 0.65) + (255,), width=max(1, int(W * 0.03)))
    return fn


def arrow_draw(d, W, H):
    """Arrow of the launcher pointing up, the pivot in the middle of the image (it turns around it)."""
    cx, piv = W / 2, H / 2
    sw, hw, head = W * 0.17, W * 0.48, W * 1.1
    pts = [(cx - sw, piv + W * 0.3), (cx - sw, head), (cx - hw, head + W * 0.1), (cx, 0), (cx + hw, head + W * 0.1), (cx + sw, head),
           (cx + sw, piv + W * 0.3)]
    d.polygon(pts, fill=(252, 252, 255, 255))
    d.polygon([(cx, 0), (cx + hw, head + W * 0.1), (cx + sw, head), (cx + sw, piv + W * 0.3), (cx, piv + W * 0.3)], fill=(196, 202, 222, 255))
    d.line(pts + [pts[0]], fill=(30, 34, 60, 255), width=max(2, int(W * 0.07)), joint="curve")


def gear_draw(d, W, H):
    c, R = W / 2, W / 2 * 0.98
    r = R * 0.8
    n = 12
    pts = []
    for i in range(n * 4):
        a = i / (n * 4) * math.tau
        rr = R if i % 4 in (1, 2) else r
        pts.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
    dark = (104, 70, 20, 255)
    d.polygon(pts, fill=(214, 166, 58, 255), outline=dark, width=max(2, int(W * 0.025)))
    d.ellipse([c - r * 0.78, c - r * 0.78, c + r * 0.78, c + r * 0.78], fill=(240, 198, 92, 255), outline=dark, width=max(2, int(W * 0.02)))
    for i in range(5):
        a = i / 5 * math.tau
        hx, hy, hr = c + math.cos(a) * r * 0.48, c + math.sin(a) * r * 0.48, r * 0.14
        d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(150, 108, 34, 255))
    d.ellipse([c - r * 0.2, c - r * 0.2, c + r * 0.2, c + r * 0.2], fill=(70, 48, 16, 255))


def base_draw(d, W, H):
    d.ellipse([0, 0, W - 1, H - 1], fill=(28, 36, 76, 255), outline=(160, 180, 236, 255), width=max(2, int(W * 0.045)))
    d.ellipse([W * 0.14, H * 0.14, W * 0.86, H * 0.86], fill=(38, 50, 104, 255))
    d.arc([W * 0.06, H * 0.06, W * 0.94, H * 0.94], 200, 320, fill=(220, 230, 255, 255), width=max(2, int(W * 0.03)))


class Board:
    """Little bubble board above a launcher: the shot bubbles stick, three of a colour or more pop, the ones left
    hanging fall. / Petit plateau de bulles : les bulles tirées collent, trois de la même couleur éclatent."""
    COLS = 13

    def __init__(self, scene, cx):
        S = scene.S
        self.sc, self.rng = scene, scene.rng
        self.D = S(44)
        self.RH = self.D * 0.866
        self.x0 = cx - self.D * self.COLS / 2
        self.x1 = cx + self.D * self.COLS / 2
        self.top = S(112)
        self.cells = {}
        self.falling = []
        self.fill(3)

    def cols(self, row):
        return self.COLS if row % 2 == 0 else self.COLS - 1

    def xy(self, row, col):
        return self.x0 + self.D / 2 + col * self.D + (self.D / 2 if row % 2 else 0), self.top + self.D / 2 + row * self.RH

    def fill(self, rows):
        self.cells = {}
        for r in range(rows):
            for c in range(self.cols(r)):
                if r < rows - 1 or self.rng.random() > 0.35:
                    self.cells[(r, c)] = self.rng.randrange(6)

    def neighbours(self, r, c):
        if r % 2 == 0:
            cand = ((r, c - 1), (r, c + 1), (r - 1, c - 1), (r - 1, c), (r + 1, c - 1), (r + 1, c))
        else:
            cand = ((r, c - 1), (r, c + 1), (r - 1, c), (r - 1, c + 1), (r + 1, c), (r + 1, c + 1))
        return [(rr, cc) for rr, cc in cand if rr >= 0 and 0 <= cc < self.cols(rr)]

    def hits(self, x, y):
        """True when a flying bubble at (x, y) touches the board or the ceiling."""
        if y - self.D / 2 <= self.top:
            return True
        lim = (self.D * 0.9) ** 2
        for r, c in self.cells:
            bx, by = self.xy(r, c)
            if (bx - x) ** 2 + (by - y) ** 2 < lim:
                return True
        return False

    def group(self, start, same):
        seen, todo = {start}, [start]
        while todo:
            for n in self.neighbours(*todo.pop()):
                if n not in seen and n in self.cells and (not same or self.cells[n] == self.cells[start]):
                    seen.add(n)
                    todo.append(n)
        return seen

    def stick(self, x, y, color):
        """Puts the bubble in the nearest free cell. Returns the positions and colours of the bubbles that pop."""
        best, bd = None, None
        guess = int(round((y - self.top - self.D / 2) / self.RH))
        for r in range(max(0, guess - 1), guess + 2):
            for c in range(self.cols(r)):
                if (r, c) in self.cells or (r > 0 and not any(n in self.cells for n in self.neighbours(r, c))):
                    continue
                bx, by = self.xy(r, c)
                d = (bx - x) ** 2 + (by - y) ** 2
                if bd is None or d < bd:
                    best, bd = (r, c), d
        if best is None:
            return []
        self.cells[best] = int(color) % len(BUBBLE_RGB)
        same = self.group(best, True)
        popped = []
        if len(same) >= 3:
            for cell in same:
                popped.append(self.xy(*cell) + (self.cells.pop(cell),))
            hanging = set()
            for cell in [c for c in self.cells if c[0] == 0]:
                hanging |= self.group(cell, False)
            for cell in [c for c in self.cells if c not in hanging]:
                x, y = self.xy(*cell)
                self.falling.append([x, y, -self.sc.rng.uniform(80, 260) * self.sc.s, self.cells.pop(cell)])
        return popped

    def low(self):
        return max((r for r, _ in self.cells), default=0)


class PuzzleBobbleScene(GameScene):
    THEME = "bubbles"
    STATIC = True
    SHADE = (120, 60)
    PILLS = True
    BANNERS = GameScene.BANNERS + tuple((f"ROUND {n}", GOLD) for n in range(1, 10))
    R = 26                                                     # bubble in the launcher / bulle dans le lanceur

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.flying = []
        self.slide = {"p1": -99.0, "p2": -99.0}
        self.angle = {"p1": 0.0, "p2": 0.0}
        self.boards = {side: Board(self, self.launcher_xy(side)[0]) for side in ("p1", "p2")}

    def bub(self, i, r):
        S = self.S
        i = int(i) % len(BUBBLE_RGB)
        r = int(round(r))
        return self.img(("bub", i, r), S(2 * r), S(2 * r), bubble_draw(BUBBLE_RGB[i]))

    def launcher_xy(self, side):
        return (self.S(400), self.S(398)) if side == "p1" else (self.W - self.S(400), self.S(398))

    def restart(self, vals, now):
        self.flying = []
        for b in self.boards.values():
            b.fill(3)
            b.falling = []

    def _clear(self, board, now, refill=3):
        """The whole board pops, then new rows come down. / Tout le plateau éclate, puis de nouvelles rangées."""
        for i, ((r, c), col) in enumerate(sorted(board.cells.items())):
            x, y = board.xy(r, c)
            self.fx.later(0.012 * i, self._burst, x, y, col, 8)
        board.cells = {}
        self.fx.later(0.7, board.fill, refill)

    def update(self, vals, now):
        dt = self.dt
        for side, suf in (("p1", ""), ("p2", "_p2")):
            st = self.stick(vals, side)
            if st is not None:                                         # left / right turn the arrow
                self.angle[side] = _clamp(self.angle[side] + st[0] * 75 * dt, -72.0, 72.0)
            else:
                self.angle[side] = 52 * math.sin(now * 0.8 + (0 if side == "p1" else 2.0))
            ch = self.changed(vals, "bubble" + suf)
            if ch:                                                     # the bubble leaves the launcher
                x, y = self.launcher_xy(side)
                a = math.radians(self.angle[side])
                v = 1700 * self.s
                self.flying.append({"c": ch[0], "x": x, "y": y, "vx": math.sin(a) * v, "vy": -math.cos(a) * v, "t0": now, "side": side})
                self.slide[side] = now
        ch = self.changed(vals, "round")
        if ch:                                                         # new round: new boards
            self.slam(f"ROUND {int(ch[1])}", GOLD, now, 1.6)
            for b in self.boards.values():
                self._clear(b, now, 3 + min(3, int(ch[1]) // 8))

    def _burst(self, x, y, c, n=14):
        col = BUBBLE_RGB[int(c) % len(BUBBLE_RGB)]
        self.fx.sparks(x, y, n, _mix(col, WHITE, 0.35), (200, 520), (0, 360), (0.25, 0.55), 500, "front", 4, 16)
        self.fx.glow(x, y, 12, 60, _mix(col, WHITE, 0.4), 0.25, "front", 0.9, 0.0)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, H, dt = self.S, self.W, self.H, self.dt
        for side, board in self.boards.items():                        # the boards, the bubbles that fall
            if side == "p2" and not self.p2_in(vals):
                continue
            for (r, c), col in board.cells.items():
                x, y = board.xy(r, c)
                b = self.bub(col, 22)
                screen.blit(b, (int(x - b.get_width() / 2), int(y - b.get_height() / 2)))
            for f in board.falling:
                f[2] += 2600 * self.s * dt
                f[1] += f[2] * dt
                b = self.bub(f[3], 22)
                screen.blit(b, (int(f[0] - b.get_width() / 2), int(f[1] - b.get_height() / 2)))
            board.falling = [f for f in board.falling if f[1] < H + S(40)]
        keep = []
        for f in self.flying:                                          # shot bubbles bounce on the side walls, then stick
            board = self.boards[f["side"]]
            f["x"] += f["vx"] * dt
            f["y"] += f["vy"] * dt
            lo, hi = board.x0 + board.D / 2, board.x1 - board.D / 2
            if (f["x"] < lo and f["vx"] < 0) or (f["x"] > hi and f["vx"] > 0):
                f["vx"] = -f["vx"]
                f["x"] = _clamp(f["x"], lo, hi)
            if board.hits(f["x"], f["y"]) or now - f["t0"] > 1.6:
                for i, (x, y, c) in enumerate(board.stick(f["x"], f["y"], f["c"])):
                    self.fx.later(0.03 * i, self._burst, x, y, c)
                if board.low() >= 6:                                   # the board reached the launcher: it clears
                    self._clear(board, now)
                continue
            b = self.bub(f["c"], 22)
            screen.blit(b, (int(f["x"] - b.get_width() / 2), int(f["y"] - b.get_height() / 2)))
            keep.append(f)
        self.flying = keep
        self.top_bar(screen, eng, vals, logo, now, right=False)
        for side, suf, d in (("p1", "", -1), ("p2", "_p2", 1)):
            if side == "p2" and not self.p2_in(vals):                  # player 2 is invited in its own place
                word, col = self.invite(vals, now)
                self.label(screen, word, self.launcher_xy("p2")[0], S(392), 44, col, align="center")
                continue
            cur, nxt = _n(vals.get("bubble" + suf)), _n(vals.get("bubble_next" + suf))
            x, y = self.launcher_xy(side)
            gear = self.rotated("gear", self.img("gear", S(96), S(96), gear_draw), -self.angle[side] * 2.5, 3)
            screen.blit(gear, (int(x - d * S(96) - gear.get_width() / 2), int(y + S(18) - gear.get_height() / 2)))
            base = self.img("base", S(118), S(118), base_draw)
            screen.blit(base, (int(x - base.get_width() / 2), int(y - base.get_height() / 2)))
            arrow = self.rotated("arrow", self.img("arrow", S(40), S(330), arrow_draw), -self.angle[side], 2)
            screen.blit(arrow, (int(x - arrow.get_width() / 2), int(y - arrow.get_height() / 2)))
            nx, ny = x + d * S(150), S(418)
            if cur is not None:
                k = _clamp((now - self.slide[side]) / 0.2)               # the next bubble rolls into the launcher
                cx, cy = nx + (x - nx) * k, ny + (y - ny) * k - math.sin(k * math.pi) * S(40)
                b = self.bub(cur, 22 + (self.R - 22) * k)
                screen.blit(b, (int(cx - b.get_width() / 2), int(cy - b.get_height() / 2)))
            if nxt is not None and now - self.slide[side] > 0.2:
                pop = _clamp((now - self.slide[side] - 0.2) / 0.15)
                b = self.bub(nxt, 22 * (0.4 + 0.6 * pop))
                screen.blit(b, (int(nx - b.get_width() / 2), int(ny - b.get_height() / 2)))
            if nxt is not None:
                self.label(screen, tr("SUIVANTE", "NEXT"), nx, S(370), 18, CREAM, key="bold", align="center", glow=0, alpha=120)
        rnd = _n(vals.get("round"))
        if rnd is not None:
            self.label(screen, f"ROUND {int(rnd)}", W / 2, S(404), 52, GOLD, key="stencil", align="center")


# ============================================================================ Windjammers
NATIONS = (("JAPON", "JAPAN"), ("ESPAGNE", "SPAIN"), ("USA", "USA"), ("CORÉE", "KOREA"), ("ITALIE", "ITALY"), ("ALLEMAGNE", "GERMANY"))
COURTS = (("PLAGE", "BEACH"), ("GAZON", "LAWN"), ("CARRELAGE", "TILES"), ("BÉTON", "CONCRETE"), ("TERRE BATTUE", "CLAY"),
          ("STADE", "STADIUM"))


def disc_draw(d, W, H):
    d.ellipse([0, H * 0.24, W - 1, H * 0.94], fill=(166, 104, 18, 255))
    d.ellipse([0, H * 0.06, W - 1, H * 0.78], fill=(255, 210, 60, 255), outline=(150, 96, 20, 255), width=max(1, int(H * 0.06)))
    d.ellipse([W * 0.2, H * 0.2, W * 0.8, H * 0.64], outline=(255, 110, 40, 255), width=max(1, int(H * 0.08)))
    d.ellipse([W * 0.32, H * 0.26, W * 0.6, H * 0.42], fill=(255, 246, 200, 255))


class WindjammersScene(GameScene):
    THEME = "court_beach"
    STATIC = True
    SHADE = (150, 0)
    PILLS = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.flights = []
        self.pop = {"set_points": -99.0, "set_points_p2": -99.0}
        self.goal = None                                     # goal zone lit up / zone de but éclairée
        self.rally = None
        self.pause = 0.0
        self.court = None

    def always(self, vals, now):
        court = _n(vals.get("court"))
        if court is None:
            return
        name = hd_themes.COURTS[int(court) % len(hd_themes.COURTS)]
        if name == self.bd.theme:
            return
        if name != self.court:                                         # the new court is built in the background
            self.court = name
            self.bd.prebuild([name])
        if self.bd.ready(name):
            old = self.bd.theme
            self.bd.set_theme(name, now, wipe=0 if self.bd.last is None else 1.1)
            with self.bd.lock:                                         # only one court kept in memory
                self.bd.raw.pop(old, None)
            self.bd.built.pop(old, None)

    def floor(self):
        return int(self.H * 0.42) + self.S(10), self.H - self.S(6)     # top and bottom walls of the court

    def restart(self, vals, now):
        self.flights, self.rally, self.goal = [], None, None

    def update(self, vals, now):
        S, W = self.S, self.W
        top, bot = self.floor()
        for name, x0, x1 in (("set_points", S(400), W - S(48)), ("set_points_p2", W - S(400), S(48))):
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0]:
                pts = int(ch[1] - ch[0])
                if pts == 2:                                           # 2 points: the disc falls on the other side
                    x1 = W - S(300) if x1 > W / 2 else S(300)
                    self.flights.append({"x0": x0, "y0": S(350), "x1": x1, "y1": self.rng.uniform(S(320), S(420)), "t0": now,
                                         "dur": 0.9, "pts": pts, "name": name, "zone": None})
                else:                                                  # goal: the disc flies into the other goal
                    third = (bot - top) / 3
                    zone = 1 if pts >= 5 else self.rng.choice((0, 2))
                    self.flights.append({"x0": x0, "y0": S(350), "x1": x1, "y1": top + third * (zone + 0.5), "t0": now, "dur": 0.5,
                                         "pts": pts, "name": name, "zone": (top + third * zone, top + third * (zone + 1))})
                self.rally = None
                self.pause = now + 1.4

    def _rally(self, now):
        """Easy exchange between the two players: straight, off a wall, or a lob. / Échange entre les joueurs."""
        S, W = self.S, self.W
        bot = self.floor()[1]
        r = self.rally
        if r is None or now - r["t0"] >= r["dur"]:
            x0 = r["x1"] if r else S(420)
            y0 = r["y1"] if r else S(350)
            x1 = W - S(420) if x0 < W / 2 else S(420)
            y1 = self.rng.uniform(S(300), bot - S(40))
            kind = self.rng.choice(("line", "wall", "wall", "lob"))
            wall = bot - S(12)
            self.rally = r = {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "t0": now, "kind": kind, "wall": wall,
                              "dur": 1.1 if kind == "lob" else self.rng.uniform(0.55, 0.8)}
        k = (now - r["t0"]) / r["dur"]
        x = r["x0"] + (r["x1"] - r["x0"]) * k
        h = 0.0
        if r["kind"] == "wall":                                        # off the wall halfway
            ym = r["wall"]
            y = r["y0"] + (ym - r["y0"]) * (k * 2) if k < 0.5 else ym + (r["y1"] - ym) * ((k - 0.5) * 2)
        else:
            y = r["y0"] + (r["y1"] - r["y0"]) * k
            if r["kind"] == "lob":
                h = math.sin(k * math.pi) * S(70)
        return x, y, h

    def draw_disc(self, screen, x, y, h, now):
        S = self.S
        sh = self.imgs.get("disc_shadow")
        if sh is None:
            sh = self.pg.Surface((S(70), S(22)), self.pg.SRCALPHA)
            self.pg.draw.ellipse(sh, (0, 0, 0, 90), sh.get_rect())
            self.imgs["disc_shadow"] = sh
        screen.blit(sh, (int(x - sh.get_width() / 2), int(y + S(8) - sh.get_height() / 2)))
        disc = self.rotated("disc", self.img("disc", S(70), S(32), disc_draw), math.sin(now * 9) * 8, 4)
        sc = 1.0 + h / S(400)
        if sc > 1.01:
            disc = self.pg.transform.smoothscale(disc, (int(disc.get_width() * sc), int(disc.get_height() * sc)))
        screen.blit(disc, (int(x - disc.get_width() / 2), int(y - h - disc.get_height() / 2)))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg, fx = self.S, self.W, self.pg, self.fx
        if self.goal is not None:                                      # the goal zone lights up
            gx, (gy0, gy1), t0 = self.goal
            k = 1 - (now - t0) / 0.8
            if k > 0:
                key = ("goal", int(gy1 - gy0))
                lit = self.imgs.get(key)
                if lit is None:
                    lit = self.imgs[key] = self.pg.Surface((S(40), int(gy1 - gy0))).convert()
                lit.fill((int(255 * k), int(230 * k), int(140 * k)))
                screen.blit(lit, (int(gx - S(20)), int(gy0)), special_flags=pg.BLEND_RGB_ADD)
            else:
                self.goal = None
        keep = []
        for f in self.flights:
            k = (now - f["t0"]) / f["dur"]
            if k >= 1.0 and f["zone"] is None:                         # the disc lands: dust, +2
                fx.smoke(f["x1"], f["y1"] + S(8), 6, (10, 18), 2.2, (0.5, 0.9), (10, 30), 30, (236, 220, 180), 170, "front")
                self.popup(f"+{f['pts']}", f["x1"], f["y1"] - S(60), GOLD, 56, life=1.2)
                self.pop[f["name"]] = now
                continue
            if k >= 1.0:
                right = f["x1"] > W / 2
                fx.glow(f["x1"], f["y1"], 24, 170, (255, 240, 180), 0.45, "front", 1.0, 0.0)
                fx.sparks(f["x1"], f["y1"], 34, (255, 220, 120), (250, 760), (100, 260) if right else (-80, 80), (0.3, 0.7), 600,
                          "front", 4, 26)
                self.popup(f"+{f['pts']}", f["x1"] + (-S(120) if right else S(120)), f["y1"], GOLD if f["pts"] < 5 else (255, 130, 80), 64,
                           life=1.3)
                fx.shake(7, 0.3)
                self.pop[f["name"]] = now
                self.goal = (f["x1"], f["zone"], now)
                continue
            x = f["x0"] + (f["x1"] - f["x0"]) * k
            y = f["y0"] + (f["y1"] - f["y0"]) * k
            if f["zone"] is None:                                       # a lob that nobody catches
                self.draw_disc(screen, x, y, math.sin(k * math.pi) * S(90), now)
                keep.append(f)
                continue
            for j in range(1, 7):                                       # fiery trail of the smash
                kk = max(0.0, k - j * 0.03)
                g = fx.sp.glow(S(16), (255, 200, 90), 9 - j, hot=0.3)
                screen.blit(g, (int(f["x0"] + (f["x1"] - f["x0"]) * kk - g.get_width() / 2),
                                int(f["y0"] + (f["y1"] - f["y0"]) * kk - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            self.draw_disc(screen, x, y, 0, now)
            keep.append(f)
        self.flights = keep
        if not self.flights and now >= self.pause:
            self.draw_disc(screen, *self._rally(now), now)
        self.scoreboard(screen, vals, logo, now)

    def scoreboard(self, screen, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        hd.draw_logo(screen, logo, W / 2, S(6), S(500), S(92), now)
        bw, bh = S(720), S(164)
        bx, by = W / 2 - bw / 2, S(104)
        self.box(screen, bx, by, bw, bh, (255, 214, 90))
        p2 = self.p2_in(vals)
        cpu = _n(vals.get("cpu_team"))
        right = "P2" if p2 else (tr(*NATIONS[int(cpu) % 6]) if cpu is not None else "CPU")
        self.text(screen, "P1", bx + S(34), by + S(16), 32, P1C)
        self.text(screen, right, bx + bw - S(34), by + S(16), 32, P2C, align="right")
        for name, x, col, align in (("set_points", W / 2 - S(110), P1C, "right"), ("set_points_p2", W / 2 + S(110), P2C, "left")):
            v = _n(vals.get(name))
            if v is None:
                continue
            k = now - self.pop[name]
            hd.put_number(screen, f"{int(v):02d}", "black", S(96), WHITE if k < 0.35 else col, x, by + S(88), align, "middle",
                          scale=1.0 + 0.3 * max(0.0, 1 - k / 0.35))
        t = _n(vals.get("time"))
        if t is not None:
            low = t <= 10
            pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
            hd.put_number(screen, f"{int(t)}", "black", S(58), RED if low else GOLD, W / 2, by + S(86), "center", "middle",
                          scale=1 + 0.12 * pulse)
        info = []
        court = _n(vals.get("court"))
        if court is not None:
            info.append(tr(*COURTS[int(court) % 6]))
        tw = _n(vals.get("to_win"))
        if tw is not None:
            info.append(tr(f"{int(tw)} POINTS POUR GAGNER", f"{int(tw)} POINTS TO WIN"))
        if info:
            self.text(screen, "  ·  ".join(info), W / 2, by + bh - S(26), 22, (200, 196, 180), key="bold", align="center",
                      valign="middle", glow=0)
        if not p2:
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(44), 34, col, align="right")


# ============================================================================ Shock Troopers
GUN_NAMES = (("FUSIL", "NORMAL GUN"), ("FUSIL LOURD", "HEAVY GUN"), ("VULCAN", "VULCAN GUN"), ("TIR TRIPLE", "3-WAY GUN"),
             ("BUSTER", "BUSTER GUN"), ("LANCE-FLAMMES", "FLAME GUN"), ("ROQUETTES", "ROCKET GUN"), ("MISSILES", "MISSILE GUN"),
             ("HYPER", "HYPER GUN"))
SPECIAL_NAMES = (("GRENADE", "GRENADE"), ("FUMIGÈNE", "SMOKE CAN"), ("BIDON", "CAN GUN"), ("BOOMERANG", "BOOMERANG"),
                 ("MISSILES", "MISSILE L."), ("ARC", "BOW"), ("CHIMIQUE", "CHEMICAL"), ("BAZOOKA", "BAZOOKA"))
GUN_TINT = ((90, 96, 84), (70, 74, 66), (110, 112, 120), (96, 110, 80), (120, 90, 140), (170, 90, 40), (90, 110, 70),
            (110, 120, 140), (200, 170, 60))


def rifle_draw(tint):
    """Rifle seen from the side, muzzle to the right. / Fusil de profil, canon à droite."""
    def fn(d, W, H):
        dark = (16, 18, 14, 255)
        body = tint + (255,)
        ow = max(2, int(H * 0.05))
        d.polygon([(0, 0.34 * H), (0.27 * W, 0.3 * H), (0.29 * W, 0.62 * H), (0.04 * W, 0.8 * H)], fill=body, outline=dark, width=ow)
        d.polygon([(0.42 * W, 0.56 * H), (0.53 * W, 0.56 * H), (0.5 * W, 0.97 * H), (0.38 * W, 0.97 * H)],
                  fill=_mix(tint, (0, 0, 0), 0.3) + (255,), outline=dark, width=ow)
        d.rectangle([0.25 * W, 0.28 * H, 0.75 * W, 0.58 * H], fill=body, outline=dark, width=ow)
        d.rectangle([0.73 * W, 0.36 * H, W - 1, 0.47 * H], fill=(52, 54, 52, 255), outline=dark, width=ow)
        d.polygon([(0.6 * W, 0.56 * H), (0.69 * W, 0.56 * H), (0.67 * W, 0.8 * H), (0.6 * W, 0.8 * H)], fill=body, outline=dark, width=ow)
        d.rectangle([0.4 * W, 0.16 * H, 0.62 * W, 0.28 * H], fill=(44, 46, 44, 255), outline=dark, width=ow)
        d.line([(0.3 * W, 0.35 * H), (0.7 * W, 0.35 * H)], fill=_mix(tint, WHITE, 0.45) + (255,), width=ow)
    return fn


def grenade_draw(d, W, H):
    d.ellipse([W * 0.1, H * 0.26, W * 0.9, H - 1], fill=(70, 100, 50, 255), outline=(24, 34, 16, 255), width=max(1, int(W * 0.06)))
    d.rectangle([W * 0.34, 0, W * 0.66, H * 0.3], fill=(150, 150, 150, 255), outline=(60, 60, 60, 255), width=max(1, int(W * 0.05)))
    d.ellipse([W * 0.28, H * 0.4, W * 0.48, H * 0.6], fill=(140, 180, 110, 255))


class ShockTroopersScene(GameScene):
    THEME = "jungle"
    SHADE = (120, 150)
    EXPLOSIONS = True
    PW = 600                                                   # player panel width / largeur d'un panneau

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.fx.sp.register("grenade", draw_img(S(24), S(30), grenade_draw))
        self.hurt = {"p1": -99.0, "p2": -99.0}
        self.wpop = {"p1": -99.0, "p2": -99.0}
        self.recoil = {"p1": -99.0, "p2": -99.0}
        self.burst = {"p1": [0.0, 0], "p2": [0.0, 0]}       # autopilot: [next shot, shots left in the burst]
        self.fire_t = {"p1": 0.0, "p2": 0.0}

    def move(self, vals, now, idle):
        return 0.1 if idle else 0.45

    def panel_x(self, side):
        return self.S(28) if side == "p1" else self.W - self.S(28) - self.S(self.PW)

    def muzzle(self, side):
        S = self.S
        x0 = self.panel_x(side)
        return (x0 + S(self.PW) + S(26), S(292)) if side == "p1" else (x0 - S(26), S(292))

    def restart(self, vals, now):
        for side in ("p1", "p2"):
            self.burst[side] = [now + 1.0, 0]

    def _shoot(self, side, weapon, now):
        fx, S = self.fx, self.S
        mx, my = self.muzzle(side)
        d = 1 if side == "p1" else -1
        tx = self.W / 2 + d * self.rng.uniform(-S(100), S(500))
        ty = self.rng.uniform(S(150), S(330))
        if weapon == 5:                                                # flame gun
            fx.sparks(mx, my, 10, (255, 160, 60), (600, 1000), (-14, 14) if d > 0 else (166, 194), (0.25, 0.45), 0, "front", 10, 50)
            fx.glow(mx + d * S(60), my, 20, 70, FIRE, 0.2, "front", 0.8, 0.0)
        elif weapon in (6, 7):                                         # rockets, missiles
            fx.tracer(mx, my, tx, ty, speed=1500, color=(255, 200, 120), width=9, length=70, impact=False)
            fx.later(abs(tx - mx) / (1500 * self.s), fx.small_blast, tx, ty, 0.8, "back")
        else:
            fx.tracer(mx, my, tx, ty, speed=3000, color=(255, 230, 150), width=5 if weapon in (1, 4, 8) else 4, length=130)
            if weapon == 3:                                            # 3-way
                for a in (-1, 1):
                    fx.tracer(mx, my, tx, ty + a * S(90), speed=3000, color=(255, 230, 150), width=4, length=110)
        fx.muzzle(mx, my, d, 0.7)
        self.recoil[side] = self.fx.now

    def update(self, vals, now):
        fx, S = self.fx, self.S
        for side, suf in (("p1", ""), ("p2", "_p2")):
            playing = self.p1_in(vals) if side == "p1" else self.p2_in(vals)
            if not playing:
                continue
            w = int(_n(vals.get("weapon" + suf)) or 0)
            mx, my = self.muzzle(side)
            d = 1 if side == "p1" else -1
            st = self.stick(vals, side)
            ch = self.changed(vals, "ammo" + suf)
            if ch and ch[1] < ch[0]:                                   # one shot per bullet gone (up to 3 at once)
                for i in range(min(3, int(ch[0] - ch[1]))):
                    fx.later(i * 0.06, self._shoot, side, w, now)
            elif st is not None:                                       # button A held: the gun fires
                if st[2] & BTN_A and now >= self.fire_t[side]:
                    self.fire_t[side] = now + 0.09
                    self._shoot(side, w, now)
            elif w == 0:                                               # autopilot: bursts with the normal gun
                b = self.burst[side]
                if now >= b[0]:
                    if b[1] <= 0:
                        b[1] = self.rng.randint(4, 8)
                    self._shoot(side, w, now)
                    b[1] -= 1
                    b[0] = now + (0.09 if b[1] > 0 else self.rng.uniform(1.2, 2.8))
            ch = self.changed(vals, "bombs" + suf)
            if ch and ch[1] < ch[0]:                                   # special weapon: a grenade into the jungle
                tx = self.W / 2 + d * self.rng.uniform(-S(200), S(300))
                ty = self.rng.uniform(S(280), S(320))
                fx.projectile("grenade", mx, my - S(10), tx, ty, 0.75, 170, self._grenade_boom)
            ch = self.changed(vals, "energy" + suf)
            if ch and ch[1] < ch[0]:
                self.hurt[side] = now
                fx.shake(5 + (ch[0] - ch[1]) * 0.08, 0.3)
                fx.flash((150, 0, 0), 0.12, 0.25)
                x0 = self.panel_x(side)
                fx.sparks(x0 + S(self.PW) / 2, S(300), 14, (255, 120, 90), (200, 600), (200, 340), (0.2, 0.5), 600, "front", 3, 20)
            ch = self.changed(vals, "weapon" + suf)
            if ch:
                self.wpop[side] = now
                name = tr(*GUN_NAMES[int(ch[1]) % len(GUN_NAMES)])
                x0 = self.panel_x(side)
                self.popup(name + " !", x0 + S(self.PW) / 2, S(222), GOLD, 40, life=1.4, key="stencil")

    def _grenade_boom(self, x, y):
        self.fx.explosion(x, y, 0.85, layer_back=True)
        self.bd.excite(0.6)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        self.top_bar(screen, eng, vals, logo, now, right=self.p2_in(vals))
        t = _n(vals.get("time"))
        if t is not None:                                              # timer under the logo
            low = t <= 10
            pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
            self.box(screen, W / 2 - S(76), S(126), S(152), S(80), RED if low else (190, 200, 120))
            self.hd.put_number(screen, f"{int(t):02d}", "stencil", S(54), RED if low else GOLD, W / 2, S(166), "center", "middle",
                               scale=1 + 0.1 * pulse)
        for side, suf, acc in (("p1", "", P1C), ("p2", "_p2", P2C)):
            if side == "p2" and not self.p2_in(vals):
                x0 = self.panel_x(side)
                word, col = self.invite(vals, now)
                self.label(screen, word, x0 + S(self.PW) / 2, S(380), 40, col, align="center")
                continue
            self.panel(screen, side, suf, acc, vals, now)

    def panel(self, screen, side, suf, acc, vals, now):
        S, pg, hd = self.S, self.pg, self.hd
        x0, y0, pw, ph = self.panel_x(side), S(258), S(self.PW), S(192)
        hurt = max(0.0, 1 - (now - self.hurt[side]) / 0.45)
        x0 += int(math.sin(now * 80) * S(6) * hurt) if hurt else 0
        self.box(screen, x0, y0, pw, ph, _mix(acc, RED, math.ceil(hurt * 4) / 4))
        if hurt:                                                       # hit: the panel flashes red
            red = self.imgs.get("hurt")
            if red is None:
                red = self.imgs["hurt"] = pg.Surface((pw - S(8), ph - S(8))).convert()
            red.fill((int(70 * hurt), 0, 0))
            screen.blit(red, (x0 + S(4), y0 + S(4)), special_flags=pg.BLEND_RGB_ADD)
        left = side == "p1"
        tx = x0 + S(24) if left else x0 + pw - S(24)
        al = "left" if left else "right"
        e = _n(vals.get("energy" + suf))
        if e is not None:                                              # energy
            frac = e / 128.0
            col = (90, 240, 90) if frac > 0.4 else ((255, 200, 60) if frac > 0.2 else RED)
            self.text(screen, tr("ÉNERGIE", "ENERGY"), tx, y0 + S(18), 22, CREAM, key="bold", align=al, glow=0)
            bx = x0 + S(150) if left else x0 + S(24)
            self.bar(screen, bx, y0 + S(16), pw - S(174), S(28), frac, col)
        w = _n(vals.get("weapon" + suf))
        if w is not None:                                              # gun: picture, name, ammo
            wi = int(w) % len(GUN_NAMES)
            k = max(0.0, 1 - (now - self.wpop[side]) / 0.5)
            name = tr(*GUN_NAMES[wi])
            size = hd.fit_size(name, "stencil", S(40), S(330), S(22))
            hd.put(screen, hd.text(name, "stencil", size, _mix(GOLD, WHITE, k), 0.4), tx, y0 + S(84), al, "middle", scale=1 + 0.15 * k)
            rifle = self.img(("rifle", wi, side), S(170), S(60), rifle_draw(GUN_TINT[wi]), flip=not left)
            kick = max(0.0, 1 - (now - self.recoil[side]) / 0.07) * S(8)
            rx = x0 + pw - S(186) - kick if left else x0 + S(16) + kick
            screen.blit(rifle, (int(rx), int(y0 + S(56))))
            a = _n(vals.get("ammo" + suf))
            if a is not None and wi > 0:
                self.text(screen, f"× {int(a)}", tx, y0 + S(126), 30, WHITE, key="black", align=al, valign="middle")
            elif wi == 0:
                self.text(screen, "∞", tx, y0 + S(126), 38, GREY, key="black", align=al, valign="middle", glow=0)
        b = _n(vals.get("bombs" + suf))
        sp = _n(vals.get("special")) if left else None
        if b is not None:                                              # special weapon and what is left
            name = tr(*SPECIAL_NAMES[int(sp) % len(SPECIAL_NAMES)]) if sp is not None else tr("SPÉCIAL", "SPECIAL")
            self.text(screen, name, tx, y0 + S(166), 24, CREAM, key="bold", align=al, valign="middle", glow=0)
            icon = self.img("gren", S(20), S(26), grenade_draw)
            for i in range(min(12, int(b))):
                gx = x0 + S(210) + i * S(24) if left else x0 + pw - S(210) - (i + 1) * S(24)
                screen.blit(icon, (int(gx), int(y0 + S(153))))


# ============================================================================ Neo Turf Masters
CLUBS = ("1W", "3W", "4W", "1I", "3I", "4I", "5I", "6I", "7I", "8I", "9I", "PW", "SW", "PT")
YARDS = (260, 240, 230, 220, 200, 190, 180, 170, 160, 150, 140, 120, 100, 28)
GOLFERS = (("USA", "USA"), ("BRÉSIL", "BRAZIL"), ("ALLEMAGNE", "GERMANY"), ("JAPON", "JAPAN"), ("AUSTRALIE", "AUSTRALIA"),
           ("ANGLETERRE", "ENGLAND"))


def ball_draw(d, W, H):
    d.ellipse([0, 0, W - 1, H - 1], fill=(200, 202, 210, 255))
    d.ellipse([W * 0.1, H * 0.06, W * 0.86, H * 0.82], fill=(255, 255, 255, 255))


class TurfMastersScene(GameScene):
    THEME = "golf"
    STATIC = True
    SHADE = (130, 120)
    PILLS = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.shots = []
        self.needle = None
        self.cpop = -99.0
        self.spop = -99.0

    def flag(self):
        if self.bd.ready("golf"):
            return self.bd._get("golf")["amb"]["flag"]
        return self.W * 0.62 + self.S(40), self.H * 0.46 + self.S(64)

    def restart(self, vals, now):
        self.shots = []

    def always(self, vals, now):
        w, d = _n(vals.get("wind")), _n(vals.get("wind_dir"))
        if w is not None and d is not None:                            # clouds and flag go with the wind
            self.bd.amb_state["wind"] = math.sin(math.radians(d * 22.5)) * (6 + w * 4)

    def update(self, vals, now):
        S = self.S
        for name in ("strokes", "strokes_p2"):
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0]:                                   # a stroke: the ball flies to the flag
                self.spop = now
                hx, hy = self.flag()
                p = _n(vals.get("power")) or 80
                reach = _clamp(p / 100.0, 0.35, 1.0)
                tx = S(380) + (hx - S(380)) * reach + self.rng.uniform(-S(80), S(80))
                ty = S(450) + (hy - S(450)) * reach + self.rng.uniform(-S(8), S(10))
                self.shots.append({"x0": S(380), "y0": S(450), "x1": tx, "y1": ty, "t0": now, "dur": 1.7, "h": S(240) * reach + S(60)})
                self.fx.glow(S(380), S(450), 10, 60, (255, 255, 230), 0.25, "front", 0.9, 0.0)
        if self.changed(vals, "club"):
            self.cpop = now

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg, fx = self.S, self.W, self.pg, self.fx
        ball = self.img("ball", S(28), S(28), ball_draw)
        keep = []
        for b in self.shots:                                           # ball in flight, its shadow on the grass
            k = (now - b["t0"]) / b["dur"]
            if k >= 1.0:
                fx.smoke(b["x1"], b["y1"], 3, (5, 10), 2.0, (0.4, 0.8), (5, 15), 8, (230, 236, 210), 150, "front")
                continue
            e = 1 - (1 - k) ** 1.5
            x = b["x0"] + (b["x1"] - b["x0"]) * e
            gy = b["y0"] + (b["y1"] - b["y0"]) * e
            y = gy - math.sin(k * math.pi) * b["h"]
            sh = self.imgs.get("ball_sh")
            if sh is None:
                sh = self.pg.Surface((S(24), S(9)), self.pg.SRCALPHA)
                self.pg.draw.ellipse(sh, (0, 0, 0, 80), sh.get_rect())
                self.imgs["ball_sh"] = sh
            screen.blit(sh, (int(x - sh.get_width() / 2), int(gy - sh.get_height() / 2)))
            for j in range(1, 6):                                       # white trail
                kk = max(0.0, k - j * 0.025)
                ee = 1 - (1 - kk) ** 1.5
                g = fx.sp.glow(S(12), (255, 255, 255), 8 - j, hot=0.3)
                screen.blit(g, (int(b["x0"] + (b["x1"] - b["x0"]) * ee - g.get_width() / 2),
                                int(b["y0"] + (b["y1"] - b["y0"]) * ee - math.sin(kk * math.pi) * b["h"] - g.get_height() / 2)),
                            special_flags=pg.BLEND_RGB_ADD)
            sc = 1.0 - 0.55 * e
            bs = pg.transform.smoothscale(ball, (max(3, int(ball.get_width() * sc)), max(3, int(ball.get_height() * sc))))
            screen.blit(bs, (int(x - bs.get_width() / 2), int(y - bs.get_height() / 2)))
            keep.append(b)
        self.shots = keep
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(560), S(112), now)
        g = _n(vals.get("golfer"))
        name = tr(*GOLFERS[int(g) % 6]) if g is not None else ""
        tw = self.hd.text("P1", "black", S(50), P1C)["w"] + (S(18) + self.hd.text(name, "xbold", S(30), CREAM, 0)["w"] if name else 0)
        self.pill(screen, S(12), S(6), tw + S(36), S(80), 140)
        x = S(30) + self.text(screen, "P1", S(30), S(16), 50, P1C) + S(18)
        if name:
            self.text(screen, name, x, S(46), 30, CREAM, key="xbold", valign="middle", glow=0)
        st = _n(vals.get("strokes"))
        if st is not None:
            k = max(0.0, 1 - (now - self.spop) / 0.4)
            self.label(screen, tr(f"COUP {int(st)}", f"STROKE {int(st)}"), W - S(30), S(44), 40, GOLD, key="black", align="right",
                       scale=1 + 0.2 * k)
        c = _n(vals.get("club"))
        if c is not None:                                              # club in hand
            k = max(0.0, 1 - (now - self.cpop) / 0.4)
            self.box(screen, S(30), S(282), S(236), S(160), (200, 240, 200))
            ci = int(c) % len(CLUBS)
            self.text(screen, CLUBS[ci], S(148), S(346), 88, _mix(WHITE, GOLD, k), key="black", align="center", valign="middle",
                      scale=1 + 0.2 * k)
            self.text(screen, f"{YARDS[ci]} Y", S(148), S(414), 28, CREAM, key="bold", align="center", valign="middle", glow=0)
        p = _n(vals.get("power"))
        if p is not None:                                              # power gauge
            bx, by, bw, bh = S(300), S(404), W - S(600), S(34)
            over = p > 100
            self.bar(screen, bx, by, bw, bh, p / 100.0, (255, 130, 60) if over else (90, 230, 90), back=(16, 40, 16))
            for q in (0.25, 0.5, 0.75):
                pg.draw.line(screen, (230, 255, 230), (int(bx + bw * q), int(by + bh)), (int(bx + bw * q), int(by + bh + S(8))), max(1, S(2)))
            txt = "MAX !" if over else tr(f"PUISSANCE {int(p)} %", f"POWER {int(p)} %")
            self.label(screen, txt, bx, by - S(30), 26, (255, 150, 80) if over else CREAM, key="bold", glow=0)
        wd, ws = _n(vals.get("wind_dir")), _n(vals.get("wind"))
        if wd is not None:                                             # wind: compass and strength
            cx, cy, r = W - S(142), S(340), S(56)
            self.box(screen, W - S(254), S(246), S(224), S(200), (200, 240, 200))
            pg.draw.circle(screen, (30, 60, 34), (int(cx), int(cy)), r)
            pg.draw.circle(screen, (200, 240, 200), (int(cx), int(cy)), r, max(2, S(3)))
            for i in range(8):
                a = i * math.pi / 4
                r0 = r * (0.78 if i % 2 else 0.68)
                pg.draw.line(screen, (150, 200, 150), (int(cx + math.sin(a) * r0), int(cy - math.cos(a) * r0)),
                             (int(cx + math.sin(a) * r * 0.92), int(cy - math.cos(a) * r * 0.92)), max(1, S(2)))
            self.text(screen, "N", cx, cy - r - S(14), 20, WHITE, key="black", align="center", valign="middle", glow=0)
            target = wd * 22.5
            if self.needle is None:
                self.needle = target
            self.needle += ((target - self.needle + 540) % 360 - 180) * min(1.0, self.dt * 6)
            a = math.radians(self.needle)
            tip = (cx + math.sin(a) * r * 0.82, cy - math.cos(a) * r * 0.82)
            tail = (cx - math.sin(a) * r * 0.55, cy + math.cos(a) * r * 0.55)
            pg.draw.line(screen, (255, 90, 70), (int(tail[0]), int(tail[1])), (int(tip[0]), int(tip[1])), max(3, S(8)))
            for sd in (-1, 1):
                b = a + math.pi + sd * 0.55
                pg.draw.line(screen, (255, 90, 70), (int(tip[0]), int(tip[1])),
                             (int(tip[0] + math.sin(b) * r * 0.36), int(tip[1] - math.cos(b) * r * 0.36)), max(3, S(8)))
            pg.draw.circle(screen, WHITE, (int(cx), int(cy)), max(3, S(6)))
            if ws is not None:
                self.text(screen, tr(f"VENT {int(ws)}", f"WIND {int(ws)}"), cx, S(420), 28, WHITE, key="black", align="center",
                          valign="middle", glow=0)


SCENES = {"blazstar": BlazingStarScene, "pbobblen": PuzzleBobbleScene, "wjammers": WindjammersScene, "shocktro": ShockTroopersScene,
          "turfmast": TurfMastersScene}
