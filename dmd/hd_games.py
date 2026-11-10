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
import os
import random
import time

from PIL import Image, ImageDraw

from . import hd_themes
from .hd_bg import Backdrop
from .hd_coin import CoinDoors, coin_rates
from .hd_credits import CreditsBar
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
    CREDITS = "bottom"            # the credits as in Metal Slug while somebody plays: "bottom" in the middle at the bottom,
                                  # (x, y) a place of the scene's own, None not shown. x: a fraction of the width (0 to 1),
                                  # else from the left edge, or from the right edge when below 0; y: None at the bottom
    CREDITS_K = 0.85              # their size, 1 as in Metal Slug / leur taille
    CONTINUE_Y = 236              # where CONTINUE ? blinks (middle of the text) / où clignote CONTINUE ?

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
        self.power_pips = []                                 # the level cases under a POWER UP / les cases sous un POWER UP
        self.powered = {"p1": -99.0, "p2": -99.0}            # when each player's shot last grew / quand le tir a grandi
        self.tops = {}                                       # the top of each value, "max" of the game file / le maximum
        self.key = None
        self.was_idle = True
        self.boost = (0.0, -99.0)                            # (backdrop speed added, until)
        self.last = None
        self.dt = 0.0
        self.touched = set()                                 # players who touched their stick or buttons
        self.hd_opts = {}                                    # the game file's "hd" block (1.33 test 47) / le bloc hd du jeu
        self.modes = {}                                      # BIOS player modes seen at the previous image
        self.cbar = CreditsBar(hd, self.fx)                  # the credits as in Metal Slug / les crédits comme dans Metal Slug
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
        a = int(round(angle / step)) * step % 360              # wrapped: a spinning picture keeps a bounded cache
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
        """Text that pops up, rises and fades, on a dark pill (readable on any backdrop). Never over the top bar.
        / Texte qui surgit, monte et s'efface, jamais sur la barre du haut."""
        self.pops.append((text, x, max(y, self.S(150)), color, size, self.fx.now, life, rise, key))

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
        self.draw_power_pips(screen, now)

    # ------------------------------------------------------------ the level of the shot / le niveau du tir
    @staticmethod
    def value_tops(eng, key):
        """The top of each value the game file gives ("max"), the shot level for example. / Le maximum de chaque valeur."""
        g = GameScene.game_file(eng, key)
        vals = (g.get("memory") or {}).get("values")
        if not isinstance(vals, dict):
            return {}
        return {k: v["max"] for k, v in vals.items() if isinstance(v, dict) and _n(v.get("max")) is not None}

    @staticmethod
    def game_file(eng, key):
        """The game's file, {} when there is none. / Le fichier du jeu, {} sinon."""
        lib = getattr(eng, "library", None)
        try:
            g = lib.get(key) if lib is not None and key else None
        except Exception:
            g = None
        return g if isinstance(g, dict) else {}

    @staticmethod
    def game_hd(eng, key):
        """The "hd" block of the game's file (1.33 test 47): what the scene reads of the game's picture, the fields of
        Twinkle Star Sprites for example. / Le bloc "hd" du fichier du jeu : les terrains de Twinkle Star Sprites."""
        hd = GameScene.game_file(eng, key).get("hd")
        return hd if isinstance(hd, dict) else {}

    def power_cases(self, vals, side, v):
        """(cases lit, cases) of a shot level as the scene shows it: as many cases lit as the value, as many cases as the
        top the game file gives (None when it does not say it). / (cases allumées, cases) d'un niveau de tir."""
        top = _n(self.tops.get("power" + ("" if side == "p1" else "_p2")))
        return max(0, int(v)), (int(top) if top is not None and top > 0 else None)

    def power_pop(self, x, y, lit, total, size=40):
        """POWER UP where the ship took the item and the level reached under it, a case per level, lit up to it. POWER MAX
        and every case lit at the top. Too many levels for cases (Guwange, Air Gallet): LV 12/14.
        / POWER UP là où le vaisseau a pris l'objet et le niveau atteint dessous, une case par niveau. POWER MAX en haut."""
        S = self.S
        top = total is not None and lit >= total
        y = max(y, S(196))                                   # it rises, stopping under the HUD / il monte, sous le HUD
        self.popup("POWER MAX" if top else "POWER UP", x, y, GOLD, size + (6 if top else 0), life=1.6)
        if total is not None and 0 < total <= 12:
            self.power_pips.append((x, y + S(size * 0.95), min(lit, total), total, self.fx.now, 1.6, 60))
        elif total is not None and not top:
            self.popup(f"LV {lit}/{total}", x, y + S(size * 0.95), CREAM, max(22, size - 12), life=1.6)
        elif lit > 0:
            self.popup(f"LV {lit}", x, y + S(size * 0.95), CREAM, max(22, size - 12), life=1.6)

    def draw_power_pips(self, screen, now):
        """The cases of the POWER UP, rising and fading with it. / Les cases du POWER UP, qui montent et s'effacent avec lui."""
        if not self.power_pips:
            return
        S, pg = self.S, self.pg
        keep = []
        for p in self.power_pips:
            x, y, lit, total, t0, life, rise = p
            k = (now - t0) / life
            if k >= 1.0:
                continue
            keep.append(p)
            if k < 0:
                continue
            yy = y - rise * self.s * (1 - (1 - k) ** 2)
            fade = 1.0 if k < 0.7 else max(0.0, (1 - k) / 0.3)
            cw, ch, gap = S(30 if total <= 6 else 22), S(20), S(8)
            w = total * cw + (total - 1) * gap
            self.pill(screen, x - w / 2 - S(12), yy - ch / 2 - S(8), w + S(24), ch + S(16), int(170 * fade) // 10 * 10)
            full = lit >= total
            for i in range(total):
                on = i < lit
                newest = on and i == lit - 1 and k < 0.5 and int(now * 16) % 2 == 0
                col = WHITE if newest else ((255, 214, 70) if on else (60, 48, 28))
                if full and on:
                    col = _mix(GOLD, WHITE, 0.5 + 0.5 * math.sin(now * 12))
                col = _mix((10, 12, 26), col, fade)
                cx = x - w / 2 + i * (cw + gap)
                pg.draw.rect(screen, col, (int(cx), int(yy - ch / 2), cw, ch), border_radius=S(5))
                if on and fade > 0.5:
                    pg.draw.rect(screen, _mix(col, WHITE, 0.6), (int(cx) + S(5), int(yy - ch / 2) + S(3), cw - S(10), S(5)),
                                 border_radius=S(2))
        self.power_pips = keep

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

    def slam(self, text, color, now, dur=1.4, sub=None):
        """Big banner across the screen, with an optional line under it (1.18). / Bandeau, avec une ligne dessous."""
        self.banner = (text, color, now, dur, sub)

    def draw_banner(self, screen, now):
        if self.banner is None:
            return
        text, color, t0, dur, sub = self.banner
        k = now - t0
        if k > dur:
            self.banner = None
            return
        if k < 0:
            return
        hd, S, W = self.hd, self.S, self.W
        scale = 2.0 - min(1.0, k / 0.16)
        alpha = 1.0 if k < dur - 0.25 else max(0.0, (dur - k) / 0.25)
        bh = S(160) if sub else S(124)
        band = self.imgs.get(("_band", bh))
        if band is None:
            band = self.imgs[("_band", bh)] = self.pg.Surface((W, bh)).convert()
            band.fill((0, 0, 0))
        band.set_alpha(int(190 * alpha))
        cy = S(240)
        screen.blit(band, (0, cy - bh // 2))
        y = cy - S(24) if sub else cy
        hd.put(screen, hd.text(text, "stencil", S(100), color, glow=0.8), W / 2, y, "center", "middle", scale=scale, alpha=alpha)
        if sub:
            sk = min(1.0, max(0.0, (k - 0.12) / 0.2))
            hd.put(screen, hd.text(sub, "xbold", S(34), CREAM, 0.3), W / 2, cy + S(48), "center", "middle", alpha=alpha * sk)

    def invite(self, vals, now):
        return self.hd._invite(vals, now)

    def credits_at(self, vals):
        """Middle of the credits pill, or None. / Le milieu de la pastille des crédits, ou None."""
        at = self.CREDITS
        if at is None:
            return None
        if at == "bottom":
            return self.W / 2, self.H - self.S(44)
        x, y = at
        x = self.W * x if 0 < x <= 1 else (self.W + self.S(x) if x < 0 else self.S(x))
        return x, (self.H - self.S(44) if y is None else self.S(y))

    def continue_shown(self, side, vals, now):
        """Whether CONTINUE ? is shown while the game says the player may continue; a scene may know better (the game
        went on with the player while the BIOS still says it). / Si CONTINUE ? s'affiche ; une scène peut savoir mieux."""
        return True

    def draw_credits(self, screen, eng, vals, now):
        """The coin (€) and CRÉDITS 07 in their pill, as in Metal Slug; the coins put in fall onto it.
        / La pièce et CRÉDITS 07 dans leur pastille, comme dans Metal Slug ; les pièces mises tombent dessus."""
        c = _n(vals.get("credits"))
        at = self.credits_at(vals)
        if c is None or at is None:
            return
        self.cbar.set_symbol((getattr(eng, "cfg", None) or {}).get("coin_symbol", "€"))
        self.cbar.draw(screen, c, at[0], at[1], now, self.CREDITS_K)

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
            hd.coins.draw(screen, vals, now, self.fx, (getattr(eng, "cfg", None) or {}).get("coin_symbol", "€"), hd.enter,
                          coin_rates(eng))
        else:
            word, col = self.invite(vals, now)
            self.label(screen, word, W / 2, S(372), 56, col, align="center")

    def render(self, screen, eng, now, logo):
        vals = eng.state.values
        key = eng.state.meta.get("game") or ""
        if key != self.key:
            self.key, self.prev, self.banner, self.was_idle, self.pops = key, {}, None, True, []
            self.power_pips, self.tops = [], self.value_tops(eng, key)
            self.hd_opts = self.game_hd(eng, key)
        self.dt = 0.0 if self.last is None else max(0.0, min(0.1, now - self.last))
        self.last = now
        self.fx.update(now)
        idle = self.nobody(vals)
        self.cbar.watch(_n(vals.get("credits")), now, drop=not idle)   # the coin doors show them on the attract screen
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
            self.draw_credits(target, eng, vals, now)
            for side, x in (("p1", self.W * 0.27), ("p2", self.W * 0.73)):     # continue countdown of the game
                if vals.get(side + "_mode") == 2 and self.banner is None and self.continue_shown(side, vals, now):
                    k = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(now * 6))
                    self.label(target, "CONTINUE ?", x, self.S(self.CONTINUE_Y), 60, GOLD, key="stencil", align="center", alpha=190, fade=k)
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
    MAX_FOES = 6                                        # at most on the screen, they only die when the game says so

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.ships = {side: {"x": 0.25, "y": 0.3 if side == "p1" else 0.75, "tx": 0.3, "ty": 0.5, "next": 0.0, "vy": 0.0,
                             "t_dead": -99.0, "t_spawn": -99.0, "fire": 0.0, "in": False} for side in ("p1", "p2")}
        self.enemies = []
        self.next_enemy = 0.0
        # When the score is read, the enemies of the screen only blow up when the game says so: the points scored, a
        # bomb or a special weapon of the game. Our shots still hit them, they flash. / Quand le score est lu, les
        # ennemis de l'écran n'explosent que quand le jeu le dit : les points marqués, une bombe, une arme spéciale.
        self.real_kills = False
        self.free_kills = -99.0
        self.gains = []
        self.tally = {side: {"times": [], "total": 0, "last": -9.0} for side in ("p1", "p2")}
        self.last_points = -9.0
        self.score_kills = 0                              # (tests)
        self.big_kills = 0
        self.booms = 0
        self.spared = 0
        self.tallies = 0
        boom = self._boom

        def guarded(e, *a, **k):
            if self.real_kills and not e.pop("doomed", False) and self.fx.now > self.free_kills:
                e["hit"] = self.fx.now                    # hit, not destroyed / touché, pas détruit
                self.spared += 1
                return None
            if not e.get("dead"):
                self.booms += 1
            return boom(e, *a, **k)
        self._boom = guarded
        for name in ("bomb", "super_shot", "_release"):    # the game's own weapons destroy what they hit
            real = getattr(self, name, None)
            if callable(real):
                setattr(self, name, self._weapon(real))

    def _weapon(self, real):
        def fire(*a, **k):
            self.weapon_window(self.fx.now)
            return real(*a, **k)
        return fire

    def weapon_window(self, now, dur=1.8):
        """A bomb or a weapon of the game: what it hits may blow up for a moment. / Une bombe ou une arme du jeu."""
        self.free_kills = max(self.free_kills, now + dur)

    def power_cases(self, vals, side, v):
        """Blazing Star shows four cases, the first one lit from the start (its level 0); the scenes built on it that draw
        their own HUD count as the game file says. / Blazing Star montre quatre cases, la première allumée dès le départ."""
        lit, top = super().power_cases(vals, side, v)
        if type(self).draw_hud is BlazingStarScene.draw_hud:
            return lit + 1, (top if top is not None else 3) + 1
        return lit, top

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
        self.real_kills = any(_n(vals.get(n)) is not None for n in ("score", "score_p2"))
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
            if ch and ch[1] > ch[0] and alive:                       # POWER UP and the level reached / et le niveau atteint
                x, y = self.pos(side, now)
                lit, total = self.power_cases(vals, side, ch[1])
                self.power_pop(x, y - S(64), lit, total)
                self.powered[side] = now
                top = total is not None and lit >= total
                fx.glow(x, y, 30 if not top else 44, 170, (120, 220, 255) if not top else (255, 220, 120), 0.5, "front", 0.9, 0.0)
                fx.sparks(x, y, 18 if not top else 36, (160, 230, 255) if not top else (255, 226, 140), (200, 600), (0, 360),
                          (0.3, 0.6), 0, "front", 3, 24)
            pw = int(_n(vals.get("power" + suf)) or 0)
            if alive and firing and now >= P["fire"]:
                P["fire"] = now + (0.075 if pw >= 3 else 0.11)
                self._fire(side, pw, now)
        self.score_events(vals, now)                                 # points scored: an enemy blows up
        ch = self.changed(vals, "round")
        if ch:
            self.slam(f"ROUND {int(ch[1])}", GOLD, now, 1.6)
            self.boost = (3.0, now + 1.8)
            self.fx.flash((140, 200, 255), 0.25, 0.4)
        if now >= self.next_enemy and len([e for e in self.enemies if not e.get("dead")]) >= self.MAX_FOES:
            self.next_enemy = now + 0.4                               # enough enemies on the screen / assez d'ennemis
        if now >= self.next_enemy:                                    # enemies alone or in a line of three
            self.next_enemy = now + self.rng.uniform(1.0, 2.2)
            y, v, ph = self.rng.uniform(S(self.ZONE[0]), S(self.ZONE[1])), self.rng.uniform(230, 330) * self.s, self.rng.uniform(0, 6)
            for i in range(self.rng.choice((1, 1, 3))):
                self.enemies.append({"x": self.W + S(60) + i * S(110), "y": y, "ph": ph + i * 0.5, "v": v, "hp": 3, "hit": -99.0})

    def score_events(self, vals, now):
        """Points scored in the game: an enemy of the screen blows up, the bigger the gain the bigger the blast. A quick
        count of points (the bonus at the end of a stage) is shown as a bonus, not as enemies.
        / Des points marqués : un ennemi explose, d'autant plus fort que le gain est gros. Un décompte rapide de points
        (le bonus de fin de niveau) s'affiche en bonus."""
        for name, side in (("score", "p1"), ("score_p2", "p2")):
            T = self.tally[side]
            ch = self.changed(vals, name)
            if not ch or ch[1] <= ch[0]:
                continue
            gain = ch[1] - ch[0]
            T["times"] = [t for t in T["times"] if now - t < 0.8] + [now]
            if len(T["times"]) > 6:                                      # the game counts a bonus / le jeu compte un bonus
                if now - T["last"] > 1.4:
                    T["total"] = 0
                    self.tallies += 1
                T["total"] += gain
                T["last"] = now
                continue
            self.score_kill(side, gain, self.gain_ratio(gain), now)

    def draw_pops(self, screen, now):
        """The popups, and the bonus that the game counts, in one counter. / Les bulles, et le bonus compté par le jeu."""
        super().draw_pops(screen, now)
        both = self.ships["p1"]["in"] and self.ships["p2"]["in"]
        for side, T in self.tally.items():
            k = now - T["last"]
            if T["total"] <= 0 or k > 1.4:
                continue
            if now - T.get("shown_at", -9.0) > 0.2 or k > 0.3:            # the counter moves five times a second / cinq fois par seconde
                T["shown"], T["shown_at"] = T["total"], now
            x = self.W * ((0.3 if side == "p1" else 0.7) if both else 0.5)
            fade = 1.0 if k < 1.0 else max(0.0, (1.4 - k) / 0.4)
            self.label(screen, f"BONUS +{int(T['shown'])}", x, self.S(212), 54, GOLD, key="black", align="center", glow=0.6, alpha=190,
                       fade=fade)

    def play_band(self):
        """Where the enemies can be seen, between the side panels of the game if it has some.
        / Où l'on voit les ennemis, entre les panneaux de côté du jeu s'il en a."""
        panel = getattr(self, "PANEL", 0)
        if isinstance(panel, (int, float)) and panel:
            return self.S(panel) + self.S(20), self.W - self.S(panel) - self.S(30)
        return -self.S(40), self.W - self.S(20)

    def gain_ratio(self, gain):
        """How big a gain is next to the usual gains of the game. / La taille d'un gain à côté des gains habituels."""
        past = sorted(self.gains)
        self.gains = (self.gains + [gain])[-24:]
        if len(past) < 3:
            return 1.0
        return gain / max(1e-6, past[len(past) // 2])

    def kill_target(self, side, now):
        """The enemy that the points scored blow up: one our shots just hit, else the nearest one ahead.
        / L'ennemi que les points font exploser : un que nos tirs viennent de toucher, sinon le plus proche devant."""
        x0, x1 = self.play_band()
        alive = [e for e in self.enemies if not e.get("dead") and x0 < e["x"] < x1]
        if not alive:
            return None
        x, y = self.pos(side, now) if self.ships[side]["in"] else (self.W * 0.3, self.H * 0.55)
        hot = [e for e in alive if now - e.get("hit", -99.0) < 0.6]
        ahead = [e for e in alive if e["x"] > x]
        return min(hot or ahead or alive, key=lambda e: abs(e.get("yy", e["y"]) - y) * 2.0 + abs(e["x"] - x) * 0.5)

    def no_target_kill(self, side, now):
        """No enemy on the screen: the blast where one would be, ahead of the ship. / Pas d'ennemi : l'explosion devant."""
        if not self.ships[side]["in"]:
            return None
        x, y = self.pos(side, now)
        tx = min(self.play_band()[1] - self.S(100), x + self.S(self.rng.uniform(420, 760)))
        ty = y + self.S(self.rng.uniform(-50, 50))
        self.fx.explosion(tx, ty, 0.5, False)
        return tx, ty

    def score_kill(self, side, gain, ratio, now):
        fx, S, rng = self.fx, self.S, self.rng
        e = self.kill_target(side, now)
        if e is not None:
            e["doomed"] = True
            self._boom(e)
            x, y = e["x"], e.get("yy", e["y"])
        else:
            spot = self.no_target_kill(side, now)
            if spot is None:
                return
            x, y = spot
        self.score_kills += 1
        big = ratio >= 2.5
        if big:                                                          # a big enemy: more blasts, the screen shakes
            self.big_kills += 1
            n = 2 if ratio < 6 else 4
            for i in range(n):
                fx.later(0.07 * (i + 1), fx.explosion, x + rng.uniform(-S(60), S(60)), y + rng.uniform(-S(40), S(40)), 0.45 + 0.1 * i, False)
            fx.shake(3 + min(7.0, ratio * 0.6), 0.3 + 0.05 * n)
            if ratio >= 6:
                fx.flash((255, 230, 190), 0.18, 0.3)
        if big or now - self.last_points > 0.25:                         # the points scored / les points marqués
            self.last_points = now
            self.popup(f"+{int(gain)}", x, y - S(50), GOLD if big else CREAM, 34 if big else 24)

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
            self.text(screen, f"ROUND {int(rnd)}", W / 2, S(336), 46, GOLD, key="stencil", align="center", valign="middle")


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


def trophy_draw(lit):
    """A trophy of our own, gold when its game is won, dark when not yet. / Un trophée à nous, doré quand gagné."""
    def fn(d, W, H):
        k = W / 40.0
        gold, light, dark = ((250, 196, 52), (255, 236, 150), (150, 96, 10)) if lit else ((70, 76, 96), (104, 110, 130), (40, 44, 58))
        line = max(1, int(2 * k))
        d.arc([1 * k, 6 * k, 15 * k, 22 * k], 90, 270, fill=dark + (255,), width=max(2, int(3 * k)))          # the handles
        d.arc([25 * k, 6 * k, 39 * k, 22 * k], 270, 90, fill=dark + (255,), width=max(2, int(3 * k)))
        d.pieslice([6 * k, -10 * k, 34 * k, 30 * k], 0, 180, fill=gold + (255,), outline=dark + (255,), width=line)
        d.rectangle([6 * k, 4 * k, 34 * k, 10 * k], fill=gold + (255,), outline=dark + (255,), width=line)
        d.ellipse([11 * k, 6 * k, 16 * k, 18 * k], fill=light + (255,))                                            # its shine
        d.rectangle([17 * k, 29 * k, 23 * k, 37 * k], fill=gold + (255,), outline=dark + (255,), width=max(1, int(1.5 * k)))
        d.rounded_rectangle([9 * k, 37 * k, 31 * k, 46 * k], int(3 * k), fill=gold + (255,), outline=dark + (255,), width=line)
    return fn


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
    TURN = 360 / 256                                           # the game turns its arrow by 256 steps per turn / 256 pas par tour
    SWING = 60 * TURN                                          # as far as the game turns it (84 degrees) / aussi loin que le jeu

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.flying = []
        self.slide = {"p1": -99.0, "p2": -99.0}
        self.angle = {"p1": 0.0, "p2": 0.0}                  # the arrow drawn / la flèche dessinée
        self.aim = {"p1": None, "p2": None}                  # the game's arrow when it is read / la flèche du jeu, lue
        self.boards = {side: Board(self, self.launcher_xy(side)[0]) for side in ("p1", "p2")}
        self.win_t = {"p1": -99.0, "p2": -99.0}               # when each player last won a VS match / dernière victoire
        self.matches = 0                                     # (tests)

    @staticmethod
    def vs(vals):
        """A VS game between two players: the game mode read in the game (vs_mode, Puzzle Bobble), both of them playing.
        / Une partie VS à deux : le mode lu dans le jeu, les deux joueurs en jeu."""
        return vals.get("vs_mode") == 1 and vals.get("p1_mode") in (1, 2) and vals.get("p2_mode") in (1, 2)

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
            aim = _n(vals.get("angle" + suf))
            if aim is not None and abs(aim) <= 64:                     # the game's own arrow (1.31), 256 steps per turn
                self.aim[side] = aim * self.TURN
                k = 1.0 - math.exp(-dt / 0.06)                         # read a few times a second: it glides there
                self.angle[side] += (self.aim[side] - self.angle[side]) * k
            elif st is not None:                                       # left / right turn the arrow
                self.aim[side] = None
                self.angle[side] = _clamp(self.angle[side] + st[0] * 75 * dt, -self.SWING, self.SWING)
            else:
                self.aim[side] = None
                self.angle[side] = 52 * math.sin(now * 0.8 + (0 if side == "p1" else 2.0))
            ch = self.changed(vals, "bubble" + suf)
            if ch:                                                     # the bubble leaves the launcher, where the game aims
                x, y = self.launcher_xy(side)
                a = math.radians(self.angle[side] if self.aim[side] is None else self.aim[side])
                v = 1700 * self.s
                self.flying.append({"c": ch[0], "x": x, "y": y, "vx": math.sin(a) * v, "vy": -math.cos(a) * v, "t0": now, "side": side})
                self.slide[side] = now
        vs = self.vs(vals)
        ch = self.changed(vals, "round")
        if ch and not vs:                                              # new round: new boards (VS: no rounds)
            self.slam(f"ROUND {int(ch[1])}", GOLD, now, 1.6)
            for b in self.boards.values():
                self._clear(b, now, 3 + min(3, int(ch[1]) // 8))
        for side, name in (("p1", "wins"), ("p2", "wins_p2")):
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0] and vs:                            # a VS match won: the banner, the score, new boards
                self.win_t[side] = now
                self.matches += 1
                w1, w2 = int(_n(vals.get("wins")) or 0), int(_n(vals.get("wins_p2")) or 0)
                self.slam(tr("J1 GAGNE !", "P1 WINS!") if side == "p1" else tr("J2 GAGNE !", "P2 WINS!"), P1C if side == "p1" else P2C,
                          now, 2.0, sub=f"{w1}  -  {w2}")
                x, y = self.launcher_xy(side)
                self.fx.sparks(x, y - self.S(120), 40, GOLD, (300, 900), (200, 340), (0.5, 1.1), 900, "front", 3, 28)
                self.fx.glow(x, y - self.S(120), 30, 220, _mix(GOLD, WHITE, 0.3), 0.5, "front", 0.8, 0.0)
                for b in self.boards.values():
                    self.fx.later(0.5, self._clear, b, now + 0.5, 3)

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
            if board.hits(f["x"], f["y"]) or now - f["t0"] > 3.0:     # aimed far to the side, it climbs slowly
                for i, (x, y, c) in enumerate(board.stick(f["x"], f["y"], f["c"])):
                    self.fx.later(0.03 * i, self._burst, x, y, c)
                if board.low() >= 6:                                   # the board reached the launcher: it clears
                    self._clear(board, now)
                continue
            b = self.bub(f["c"], 22)
            screen.blit(b, (int(f["x"] - b.get_width() / 2), int(f["y"] - b.get_height() / 2)))
            keep.append(f)
        self.flying = keep
        self.top_bar(screen, eng, vals, logo, now, right=self.p2_in(vals))  # player 2's score; the invitation at its launcher
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
            nx, ny = x + d * S(228), S(418)                         # clear of the arrow aimed far to the side
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
        if self.vs(vals):
            self.draw_vs(screen, vals, now)
            return
        rnd = _n(vals.get("round"))
        if rnd is not None:                                            # above the credits / au-dessus des crédits
            self.label(screen, f"ROUND {int(rnd)}", W / 2, S(300), 52, GOLD, key="stencil", align="center")

    def draw_vs(self, screen, vals, now):
        """VS between the boards, the matches won by each player in big on each side, the last one won jumping and glowing.
        When the game's TOTAL is read (the games won whatever the match, Puzzle Bobble 2), it is the big number, and the
        trophies of the match under it (the choice A, 10 November 2026: the match's count goes back to 0 at each match).
        / VS entre les plateaux, les victoires de chaque joueur en gros de chaque côté, la dernière qui saute et brille ;
        le TOTAL du jeu quand il est lu, les trophées du match dessous (choix A)."""
        hd, S, W = self.hd, self.S, self.W
        cx, cy = W / 2, S(246)
        w1, w2 = _n(vals.get("wins")), _n(vals.get("wins_p2"))
        t1, t2 = _n(vals.get("total_wins")), _n(vals.get("total_wins_p2"))
        if None not in (w1, w2, t1, t2):
            self.draw_total(screen, (w1, w2), (t1, t2), now)
            return
        known = w1 is not None and w2 is not None
        pw, ph = (S(400), S(176)) if known else (S(200), S(120))
        self.box(screen, cx - pw / 2, cy - ph / 2, pw, ph, GOLD, fill=(8, 10, 22, 205), radius=28, width=3)
        hd.put(screen, hd.text("VS", "stencil", S(70), GOLD, glow=0.6), cx, cy, "center", "middle")
        if not known:
            return
        for side, v, col, d in (("p1", w1, P1C, -1), ("p2", w2, P2C, 1)):
            k = max(0.0, 1 - (now - self.win_t[side]) / 0.6)
            x = cx + d * S(126)
            hd.put_number(screen, str(int(v)), "black", S(120), _mix(col, WHITE, 0.5 * k), x, cy - S(6), "center", "middle",
                          scale=1 + 0.35 * k, glow=0.4 + 0.4 * k)
            tag = tr("J1", "P1") if side == "p1" else tr("J2", "P2")
            hd.put(screen, hd.text(tag, "xbold", S(24), CREAM, glow=0), x, cy + S(62), "center", "middle")

    def draw_total(self, screen, wins, totals, now, label="TOTAL", pops=None):
        """The game's TOTAL in big on each side, the last one won jumping, two trophies of the match under it, lit as the
        game's own at the top of its screen, TOTAL between them. label and pops: another count in big (the VS wins kept
        by Puzzle Bobble 2, 1.34) and when each one went up. / Le TOTAL du jeu en gros, les trophées du match dessous ;
        label et pops, un autre compte en gros et quand chacun a monté."""
        hd, S, W = self.hd, self.S, self.W
        pops = pops or self.win_t
        cx, cy = W / 2, S(246)
        pw, ph = S(420), S(196)
        self.box(screen, cx - pw / 2, cy - ph / 2, pw, ph, GOLD, fill=(8, 10, 22, 205), radius=28, width=3)
        hd.put(screen, hd.text("VS", "stencil", S(70), GOLD, glow=0.6), cx, cy - S(16), "center", "middle")
        for side, w, t, col, d in (("p1", wins[0], totals[0], P1C, -1), ("p2", wins[1], totals[1], P2C, 1)):
            k = max(0.0, 1 - (now - pops[side]) / 0.6)
            x = cx + d * S(132)
            hd.put_number(screen, str(int(t)), "black", S(120), _mix(col, WHITE, 0.5 * k), x, cy - S(22), "center", "middle",
                          scale=1 + 0.35 * k, glow=0.4 + 0.4 * k)
            for i in range(2):                                         # a match is won with two games / deux parties
                lit = i < int(w)
                cup = self.img(("trophy", lit), S(40), S(46), trophy_draw(lit))
                screen.blit(cup, (int(x + (i - 0.5) * S(50) - cup.get_width() / 2), int(cy + S(56) - cup.get_height() / 2)))
        hd.put(screen, hd.text(label, "xbold", S(22), CREAM, glow=0), cx, cy + S(58), "center", "middle")


# ============================================================================ Windjammers
# the courts by the game's index (the FinalBurn Neo cheats; the photo of 2026-11-04, the beach at 0)
COURTS = (("PLAGE", "BEACH"), ("GAZON", "LAWN"), ("CARRELAGE", "TILES"), ("BÉTON", "CONCRETE"), ("TERRE BATTUE", "CLAY"),
          ("STADE", "STADIUM"))
# the players by the game's code (RetroAchievements 0x31c, 0x31e, divided by 4; the capture of 2026-11-04 19:51), as the
# game's select screen names them. The fourth is Beeho Yoo of Korea outside Japan (the cabinet, a Europe BIOS) and
# Steve Miller of England on a Japanese BIOS (MobyGames: the export versions replaced him) / les joueurs
PLAYERS = ("G. SCOTT", "J. COSTA", "K. WESSEL", "B. YOO", "L. BIAGGI", "H. MITA")
FIGURES = ("scott", "costa", "wessel", "yoo", "biaggi", "mita")                        # sprites/wjammers/<name>.png
NATIONS = (("USA", "USA"), ("ESPAGNE", "SPAIN"), ("ALLEMAGNE", "GERMANY"), ("CORÉE", "KOREA"), ("ITALIE", "ITALY"), ("JAPON", "JAPAN"))
SUPERS = ("MISSILE THROW", "ROCKET DIAGONAL", "BLITZKRIEG", "SIDEBURNER", "THUNDER LOOP", "FIRE SNAKE")   # each one's super shot


def flag_draw(nation):
    """A nation's flag, plain and small (own drawing of the well-known designs). / Un drapeau, simple et petit."""
    def draw(d, W, H):
        if nation == "JAPAN":
            d.rectangle([0, 0, W, H], fill=(255, 255, 255))
            r = H * 0.3
            d.ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], fill=(188, 0, 45))
        elif nation == "SPAIN":
            d.rectangle([0, 0, W, H], fill=(198, 11, 30))
            d.rectangle([0, H * 0.25, W, H * 0.75], fill=(255, 196, 0))
        elif nation == "GERMANY":
            d.rectangle([0, 0, W, H / 3], fill=(0, 0, 0))
            d.rectangle([0, H / 3, W, 2 * H / 3], fill=(221, 0, 0))
            d.rectangle([0, 2 * H / 3, W, H], fill=(255, 206, 0))
        elif nation == "ITALY":
            d.rectangle([0, 0, W / 3, H], fill=(0, 146, 70))
            d.rectangle([W / 3, 0, 2 * W / 3, H], fill=(255, 255, 255))
            d.rectangle([2 * W / 3, 0, W, H], fill=(206, 43, 55))
        elif nation == "USA":
            d.rectangle([0, 0, W, H], fill=(255, 255, 255))
            for i in range(0, 13, 2):
                d.rectangle([0, H * i / 13, W, H * (i + 1) / 13], fill=(178, 34, 52))
            d.rectangle([0, 0, W * 0.4, H * 7 / 13], fill=(60, 59, 110))
            for j in range(3):
                for i in range(4):
                    x, y = W * 0.4 * (i + 0.5 + (j % 2) * 0.5) / 4.5, H * 7 / 13 * (j + 0.5) / 3
                    d.ellipse([x - W * 0.018, y - W * 0.018, x + W * 0.018, y + W * 0.018], fill=(255, 255, 255))
        elif nation == "ENGLAND":                                   # the Union Jack / l'Union Jack
            d.rectangle([0, 0, W, H], fill=(1, 33, 105))
            lw = max(1, int(H * 0.16))
            d.line([(0, 0), (W, H)], fill=(255, 255, 255), width=lw)
            d.line([(W, 0), (0, H)], fill=(255, 255, 255), width=lw)
            d.line([(0, 0), (W, H)], fill=(200, 16, 46), width=max(1, lw // 3))
            d.line([(W, 0), (0, H)], fill=(200, 16, 46), width=max(1, lw // 3))
            d.rectangle([W / 2 - H * 0.16, 0, W / 2 + H * 0.16, H], fill=(255, 255, 255))
            d.rectangle([0, H / 2 - H * 0.16, W, H / 2 + H * 0.16], fill=(255, 255, 255))
            d.rectangle([W / 2 - H * 0.1, 0, W / 2 + H * 0.1, H], fill=(200, 16, 46))
            d.rectangle([0, H / 2 - H * 0.1, W, H / 2 + H * 0.1], fill=(200, 16, 46))
        elif nation == "KOREA":                                     # the Taegukgi, simplified / le Taegukgi, simplifié
            d.rectangle([0, 0, W, H], fill=(255, 255, 255))
            r = H * 0.26
            cx, cy = W / 2, H / 2
            d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(205, 46, 58))
            d.pieslice([cx - r, cy - r, cx + r, cy + r], 0, 180, fill=(0, 71, 160))
            d.ellipse([cx - r / 2 - r * 0.5, cy - r / 2, cx - r * 0.5 + r / 2, cy + r / 2], fill=(205, 46, 58))
            d.ellipse([cx + r * 0.5 - r / 2, cy - r / 2, cx + r * 0.5 + r / 2, cy + r / 2], fill=(0, 71, 160))
            bw, bh = W * 0.16, max(1, int(H * 0.045))
            for (fx, fy) in ((0.17, 0.2), (0.83, 0.2), (0.17, 0.8), (0.83, 0.8)):
                for k in (-1, 0, 1):
                    d.rectangle([W * fx - bw / 2, H * fy + k * bh * 2.2 - bh / 2, W * fx + bw / 2, H * fy + k * bh * 2.2 + bh / 2],
                                fill=(0, 0, 0))
        d.rectangle([0, 0, W - 1, H - 1], outline=(20, 16, 24), width=max(1, int(H * 0.06)))
    return draw


def athlete_draw(col, dark, skin=(238, 198, 160)):
    """A player seen from above and a little ahead, ArcadeDMD's own drawing: cap and jersey in his colour, arms out.
    / Un joueur vu de dessus et d'un peu devant, dessin maison : casquette et maillot à sa couleur, bras écartés."""
    def draw(d, W, H):
        lw = max(2, int(W * 0.09))
        d.rounded_rectangle([W * 0.3, H * 0.74, W * 0.46, H * 0.98], radius=W * 0.06, fill=dark)          # legs / jambes
        d.rounded_rectangle([W * 0.54, H * 0.74, W * 0.7, H * 0.98], radius=W * 0.06, fill=dark)
        d.line([(W * 0.22, H * 0.5), (W * 0.04, H * 0.66)], fill=skin, width=lw)                          # arms / bras
        d.line([(W * 0.78, H * 0.5), (W * 0.96, H * 0.66)], fill=skin, width=lw)
        d.ellipse([W * 0.0, H * 0.6, W * 0.12, H * 0.72], fill=skin)
        d.ellipse([W * 0.88, H * 0.6, W * 1.0, H * 0.72], fill=skin)
        d.ellipse([W * 0.16, H * 0.38, W * 0.84, H * 0.84], fill=col, outline=dark, width=max(1, int(W * 0.03)))   # jersey
        d.rectangle([W * 0.42, H * 0.46, W * 0.58, H * 0.8], fill=tuple(min(255, c + 60) for c in col))             # stripe
        r = H * 0.19
        d.ellipse([W / 2 - r, H * 0.08, W / 2 + r, H * 0.08 + 2 * r], fill=skin)                           # head / tête
        d.chord([W / 2 - r, H * 0.08, W / 2 + r, H * 0.08 + 2 * r], 180, 360, fill=dark)                   # cap / casquette
        d.rectangle([W / 2 - r, H * 0.08 + r * 0.9, W / 2 + r, H * 0.08 + r * 1.15], fill=col)             # band / bandeau
    return draw


def disc_draw(d, W, H):
    d.ellipse([0, H * 0.24, W - 1, H * 0.94], fill=(166, 104, 18, 255))
    d.ellipse([0, H * 0.06, W - 1, H * 0.78], fill=(255, 210, 60, 255), outline=(150, 96, 20, 255), width=max(1, int(H * 0.06)))
    d.ellipse([W * 0.2, H * 0.2, W * 0.8, H * 0.64], outline=(255, 110, 40, 255), width=max(1, int(H * 0.08)))
    d.ellipse([W * 0.32, H * 0.26, W * 0.6, H * 0.42], fill=(255, 246, 200, 255))


class WindjammersScene(GameScene):
    """The court as a live map (1.33, the captures): the disc and the two players where the game has them, read at
    every image, the lobs in the air, the super shots burning, the points bursting on the goal lines; the scoreboard
    with the players' names. / Le terrain en carte vivante : le disque et les deux joueurs là où le jeu les met."""
    THEME = "court_beach"
    STATIC = True
    SHADE = (150, 0)
    PILLS = True
    CREDITS = (150, 120)                                 # top left, off the court: the disc serves at the bottom middle
    CONTINUE_Y = 330                                     # in the court, under the board / dans le terrain, sous le tableau
    DISC_X = (8, 311)                                    # the disc's x in the game, goal line to goal line
    DISC_Y = (57, 208)                                   # its y, the top wall to the bottom one
    DISC_H = 90                                          # the top of a lob
    CHARGING = 0x14                                      # the player's action word, high byte, while he charges his super

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.flights = []                                    # bursts and simulated flights / éclats et vols simulés
        self.pop = {"set_points": -99.0, "set_points_p2": -99.0}
        self.goal = None                                     # goal zone lit up / zone de but éclairée
        self.rally = None
        self.pause = 0.0
        self.court = None
        self.track = None                                    # (x, y, h) the disc's last reading / la dernière lecture
        self.shown = None                                    # (x, y, h, when drawn) the HD disc, eased / lissé
        self.tokens = {"p1": None, "p2": None}               # (x, y, when drawn) the players' tokens, eased / les jetons
        self.charge = {"p1": None, "p2": None}               # when the player began charging his super, or None
        self.super = None                                    # (side, t0) a super shot flying / un super en vol
        self.super_end = -99.0
        self.super_side_last = None
        self.trail = []                                      # the disc's last places during a super / la traînée
        self.wake = []                                       # the disc's last places, its speed streak / son sillage
        self.slams = []                                      # WIN, SUPER !: big words on a side, slammed in / claqués
        self.own = {}                                        # the owner's pictures of the players, or False / ses images
        # CONTINUE ? (1.33 test 20): the game keeps the BIOS word at 2 through the character and court selects
        # once the player has continued; the word stays shown until the game moves on / le mot du BIOS reste à 2
        self.cont = {"p1": None, "p2": None}                 # (chars, court, time) when CONTINUE began, or None
        self.cont_done = {"p1": False, "p2": False}
        # the matches won by two humans, as the fighting games count them (1.33 test 20) / les matchs gagnés
        self.wins = {"p1": 0, "p2": 0}
        self.p2_left = None                                  # when everybody left, the wins forgotten later / partis

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
        self.track = self.shown = None
        self.tokens = {"p1": None, "p2": None}
        self.charge = {"p1": None, "p2": None}
        self.super, self.super_end, self.trail, self.wake, self.slams = None, -99.0, [], [], []
        self.cont, self.cont_done = {"p1": None, "p2": None}, {"p1": False, "p2": False}
        self.wins, self.p2_left = {"p1": 0, "p2": 0}, None

    # ------------------------------------------------------------------ the court's geometry / la géométrie du terrain
    def court_pos(self, gx, gy):
        """A game position on the HD court. / Une position du jeu sur le terrain HD."""
        S, W = self.S, self.W
        top, bot = self.floor()
        kx = (gx - self.DISC_X[0]) / (self.DISC_X[1] - self.DISC_X[0])
        ky = (gy - self.DISC_Y[0]) / (self.DISC_Y[1] - self.DISC_Y[0])
        return S(48) + (W - 2 * S(48)) * min(1.2, max(-0.2, kx)), top + S(10) + (bot - top - S(20)) * min(1.1, max(-0.1, ky))

    disc_pos = court_pos

    def side_of(self, vals):
        """Who threw or holds the disc, by the game's word (12 player 1, 8 player 2). / Qui a lancé le disque."""
        last = _n(vals.get("disc_last"))
        if last is None:
            return self.super_side_last or "p1"
        return "p1" if int(last) & 4 else "p2"

    def tracking(self, now):
        """The HD disc where the game's is, eased over a few images (a reading at every image, a serve is a jump).
        Le disque HD là où est celui du jeu, lissé sur quelques images (une lecture par image, un service est un saut)."""
        if self.track is None:
            self.shown = None
            return None
        x1, y1, h1 = self.track
        if self.shown is None or abs(x1 - self.shown[0]) + abs(y1 - self.shown[1]) > self.S(500):
            self.shown = (x1, y1, h1, now)
            return x1, y1, h1
        x0, y0, h0, t0 = self.shown
        k = 1 - math.exp(-max(0.0, now - t0) / 0.045)
        self.shown = (x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, h0 + (h1 - h0) * k, now)
        return self.shown[0], self.shown[1], self.shown[2]

    def token_pos(self, side, vals, now):
        """The player's token on the HD court, eased, or None. / Le jeton du joueur sur le terrain HD, lissé."""
        gx, gy = _n(vals.get(side + "_x")), _n(vals.get(side + "_y"))
        if gx is None or gy is None or not (0 < gx < 400 and 0 < gy < 300):
            self.tokens[side] = None
            return None
        x1, y1 = self.court_pos(gx, gy)
        tk = self.tokens[side]
        if tk is None or abs(x1 - tk[0]) + abs(y1 - tk[1]) > self.S(500):
            self.tokens[side] = (x1, y1, now)
            return x1, y1
        k = 1 - math.exp(-max(0.0, now - tk[2]) / 0.08)
        self.tokens[side] = (tk[0] + (x1 - tk[0]) * k, tk[1] + (y1 - tk[1]) * k, now)
        return self.tokens[side][0], self.tokens[side][1]

    # ------------------------------------------------------------------ what the game does / ce que fait le jeu
    def update(self, vals, now):
        S, W = self.S, self.W
        top, bot = self.floor()
        gx, gy = _n(vals.get("disc_x")), _n(vals.get("disc_y"))
        if gx is not None and gy is not None:
            # (0, 0), x or y at 0: no disc on the court (title, court intro, between sets) / pas de disque
            if 0 < gx < 400 and 0 < gy < 300:
                h = _n(vals.get("disc_h")) or 0
                x, y = self.court_pos(gx, gy)
                self.track = (x, y, S(160) * min(1.3, max(0.0, h / self.DISC_H)))
            else:
                self.track = None
        live = self.tracking(now)
        for side in ("p1", "p2"):
            if vals.get(side + "_mode") != 2:
                self.cont[side] = None
        # two humans: their wins kept as long as somebody plays, even while one of them sits a match out against the
        # computer (test 21), forgotten 20 s after the cabinet is back on its title screen
        # / leurs victoires gardées tant que quelqu'un joue, même si l'un d'eux laisse passer un match contre l'ordinateur
        if not self.nobody(vals):
            self.p2_left = None
        elif self.p2_left is None:
            self.p2_left = now
        elif now - self.p2_left > 20.0 and (self.wins["p1"] or self.wins["p2"]):
            self.wins = {"p1": 0, "p2": 0}
        for side in ("p1", "p2"):                                       # the players charging their super
            st = _n(vals.get(side + "_state"))
            charging = st is not None and (int(st) >> 8) & 0xFF == self.CHARGING
            if charging and self.charge[side] is None:
                self.charge[side] = now
                tk = self.tokens[side]
                if tk is not None:
                    self.fx.glow(tk[0], tk[1], 20, 140, (255, 200, 90), 0.5, "front", 0.9, 0.0)
                    self.fx.sparks(tk[0], tk[1], 16, (255, 210, 110), (120, 360), (200, 340), (0.3, 0.6), -300, "front", 3, 22)
            elif not charging:
                self.charge[side] = None
        ds = _n(vals.get("disc_state"))
        if ds is not None:                                              # a super shot flying / un super en vol
            flying = bool(int(ds) & 0x800)
            if flying and self.super is None:
                side = self.side_of(vals)
                self.super = (side, now)
                self.super_side_last = side
                self.super_start(side, now, live, vals)
            elif not flying and self.super is not None:
                self.super = None
                self.super_end = now
        for name, x0, x1 in (("set_points", S(400), W - S(48)), ("set_points_p2", W - S(400), S(48))):
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0]:
                pts = int(ch[1] - ch[0])
                if live is not None:
                    # the real disc is there: the burst where it is, a goal on its goal line (the reading is a little
                    # behind the game) / le vrai disque est là : l'éclat où il est, un but sur sa ligne de but
                    third = (bot - top) / 3
                    zone = min(2, max(0, int((live[1] - top) / third)))
                    gx1 = live[0] if pts == 2 else x1
                    self.flights.append({"x0": gx1, "y0": live[1], "x1": gx1, "y1": live[1], "t0": now, "dur": 0.01, "pts": pts,
                                         "name": name, "zone": None if pts == 2 else (top + third * zone, top + third * (zone + 1))})
                    self.rally = None
                    self.pause = now + 1.4
                    continue
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
        won = []                                                        # a set won, the match won / un set, le match
        for name, side in (("sets", "p1"), ("sets_p2", "p2")):
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0] and ch[1] <= 3:
                won.append((int(ch[1]), side))
        if len(won) == 2:                                               # both at once (the game writes the lost set late,
            won = [max(won)]                                            # the capture of 22:14): the higher count won
        for n, side in won:
            self.set_won(side, n, vals, now)

    def continue_shown(self, side, vals, now):
        """CONTINUE ? until the game moves on (a character or the court chosen again, the timer set): the player has
        continued even if the BIOS word still says 2 (the capture of 22:14, 28 s). / Jusqu'à ce que le jeu avance."""
        snap = (_n(vals.get("p1_chr")), _n(vals.get("p2_chr")), _n(vals.get("court")), _n(vals.get("time")))
        if self.cont[side] is None:
            self.cont[side] = snap
            self.cont_done[side] = False
        elif snap != self.cont[side]:
            self.cont_done[side] = True
        return not self.cont_done[side]

    def player_name(self, vals, side):
        """The player's name as the game has it, else P1 / P2 / CPU. / Le nom du joueur, sinon P1, P2, CPU."""
        c = _n(vals.get(side + "_chr"))
        if c is not None and 0 <= int(c) < len(PLAYERS):
            if int(c) == 3 and _n(vals.get("bios_country")) == 0:       # Japanese BIOS: Steve Miller of England
                return "S. MILLER"
            return PLAYERS[int(c)]
        return "P1" if side == "p1" else ("P2" if self.p2_in(vals) else "CPU")

    def player_nation(self, vals, side):
        c = _n(vals.get(side + "_chr"))
        if c is None or not 0 <= int(c) < len(NATIONS):
            return ""
        if int(c) == 3 and _n(vals.get("bios_country")) == 0:
            return tr("ANGLETERRE", "ENGLAND")
        return tr(*NATIONS[int(c)])

    def flag(self, vals, side):
        """The player's flag, drawn by ArcadeDMD, or None. / Le drapeau du joueur, ou None."""
        c = _n(vals.get(side + "_chr"))
        if c is None or not 0 <= int(c) < len(NATIONS):
            return None
        nation = "ENGLAND" if int(c) == 3 and _n(vals.get("bios_country")) == 0 else NATIONS[int(c)][1]
        return self.img(("flag", nation), self.S(42), self.S(28), flag_draw(nation), ss=4)

    # ------------------------------------------------------------------ the big words / les grands mots
    def side_slam(self, text, sub, side, col, now, size=110, dur=1.5, delay=0.0):
        """A big word slammed in on a player's side of the court, a line under it. / Un grand mot claqué d'un côté."""
        top, bot = self.floor()
        self.slams.append({"text": text, "sub": sub, "x": self.W * (0.25 if side == "p1" else 0.75), "y": (top + bot) / 2,
                           "col": col, "t0": now + delay, "dur": dur, "size": size})

    def draw_slams(self, screen, now):
        hd, S = self.hd, self.S
        keep = []
        for sl in self.slams:
            k = (now - sl["t0"]) / sl["dur"]
            if k >= 1.0:
                continue
            keep.append(sl)
            if k < 0:
                continue
            e = min(1.0, k * sl["dur"] / 0.16)                        # the slam: big, then its size, overshooting
            scale = 2.4 - 1.4 * e if e < 1 else 1.0 + 0.18 * math.sin(min(1.0, (k * sl["dur"] - 0.16) / 0.22) * math.pi)
            fade = 1.0 if k < 0.78 else max(0.0, (1 - k) / 0.22)
            t = hd.text(sl["text"], "black", S(sl["size"]), sl["col"], 0.7 if e < 1 else 0.45)
            sub = hd.text(sl["sub"], "xbold", S(sl["size"] * 0.34), WHITE, 0.3) if sl["sub"] else None
            w = max(t["w"], sub["w"] if sub else 0) * scale + S(60)
            h = (t["h"] + (sub["h"] + S(8) if sub else 0)) * scale + S(30)
            self.pill(screen, sl["x"] - w / 2, sl["y"] - h / 2, w, h, int(170 * fade) // 10 * 10)
            y = sl["y"] - (sub["h"] * scale / 2 + S(4) if sub else 0)
            hd.put(screen, t, sl["x"], y, "center", "middle", scale=scale, alpha=fade)
            if sub:
                hd.put(screen, sub, sl["x"], y + (t["h"] + sub["h"]) * scale / 2 + S(8), "center", "middle", scale=scale, alpha=fade)
        self.slams = keep

    def confetti(self, x, y, col, n=40):
        """Confetti in the player's colour and gold, up then down. / Des confettis à sa couleur et en or."""
        fx = self.fx
        for c in (col, GOLD, WHITE, col):
            fx.sparks(x, y, n // 4, c, (200, 620), (210, 330), (1.0, 1.9), 420, "front", 7, 9)

    def set_won(self, side, sets, vals, now):
        """A set won: WIN slammed on the winner's side with the sets, confetti, the image kicked his way; the second set
        ends the match: VICTOIRE, DÉFAITE against the computer, or the winner's name between two players.
        / Un set gagné : WIN claqué de son côté, des confettis ; le second set finit le match : VICTOIRE ou DÉFAITE."""
        S, W, fx = self.S, self.W, self.fx
        col = P1C if side == "p1" else P2C
        who = self.player_name(vals, side)
        s1, s2 = int(_n(vals.get("sets")) or 0), int(_n(vals.get("sets_p2")) or 0)
        top, bot = self.floor()
        self.side_slam("WIN", tr(f"SET  {s1} - {s2}", f"SET  {s1} - {s2}"), side, col, now, 120, 1.9)
        x = W * (0.25 if side == "p1" else 0.75)
        self.confetti(x, (top + bot) / 2, col, 48)
        fx.glow(x, (top + bot) / 2, 60, 520, col, 0.7, "front", 0.7, 0.0, hot=0.4)
        fx.flash(col, 0.3, 0.4)
        fx.kick(S(14) if side == "p1" else -S(14), 0, 0.45)
        fx.shake(8, 0.4)
        if sets >= 2:                                                  # the match / le match
            p2 = self.p2_in(vals)
            if not p2 and side == "p2":
                text, sub, c = tr("DÉFAITE", "DEFEAT"), tr(f"{who} GAGNE LE MATCH", f"{who} WINS THE MATCH"), RED
            elif not p2:
                text, sub, c = tr("VICTOIRE", "VICTORY"), tr(f"{who} GAGNE LE MATCH", f"{who} WINS THE MATCH"), col
            else:
                self.wins[side] += 1
                text = who
                sub = tr(f"GAGNE LE MATCH   {self.wins['p1']} - {self.wins['p2']}", f"WINS THE MATCH   {self.wins['p1']} - {self.wins['p2']}")
                c = col
            self.slam(text, c, now + 1.6, 3.0, sub=sub)
            if c is not RED:
                for i in range(8):                                     # confetti rain for the winner / pluie de confettis
                    fx.later(1.6 + i * 0.3, self.confetti, self.rng.uniform(S(200), W - S(200)), S(120), col, 36)
                fx.later(1.6, fx.flash, col, 0.4, 0.5)
            else:
                fx.later(1.6, fx.shake, 10, 0.5)

    # ------------------------------------------------------------------ the super shot / le super
    def super_start(self, side, now, live, vals):
        """A super shot begins: SUPER ! and the player's own shot slammed on his side, a burst and a ring of light at the
        disc, the screen flashes his colour and is kicked the way of the throw. / Un super commence : SUPER ! et le nom
        du tir claqués de son côté, un éclat, un anneau de lumière, un flash, l'image poussée dans le sens du lancer."""
        S, W, fx = self.S, self.W, self.fx
        top, bot = self.floor()
        col = P1C if side == "p1" else P2C
        c = _n(vals.get(side + "_chr"))
        name = SUPERS[int(c)] if c is not None and 0 <= int(c) < len(SUPERS) else ""
        self.side_slam("SUPER !", name, side, col, now, 100, 1.4)
        tk = self.tokens[side]
        px, py = live[:2] if live is not None else (tk[:2] if tk else (W * (0.25 if side == "p1" else 0.75), (top + bot) / 2))
        fx.sparks(px, py, 60, col, (400, 1100), (0, 360), (0.3, 0.8), 500, "front", 3, 34)
        fx.sparks(px, py, 24, WHITE, (200, 600), (0, 360), (0.2, 0.5), 300, "front", 2, 20)
        fx.glow(px, py, 30, 420, col, 0.55, "front", 1.0, 0.0, hot=0.5)
        fx.glow(px, py, 10, 160, WHITE, 0.3, "front", 1.0, 0.0, hot=0.8)
        fx.flash(col, 0.3, 0.3)
        fx.kick(S(10) if side == "p1" else -S(10), 0, 0.4)
        fx.shake(6, 0.3)
        self.trail = []

    def super_side(self, now):
        """The side whose super is burning, while it lasts and 0.7 s after. / Le côté dont le super brûle."""
        if self.super is not None:
            return self.super[0]
        if now - self.super_end < 0.7:
            return self.super_side_last
        return None

    def draw_trail(self, screen, x, y, side, now):
        """The disc's fiery trail in the player's colour and its halo. / La traînée de feu et le halo du disque."""
        S, pg, fx = self.S, self.pg, self.fx
        col = (255, 150, 70) if side == "p1" else (110, 190, 255)
        if self.trail and (abs(x - self.trail[-1][0]) + abs(y - self.trail[-1][1])) > S(40):
            lx, ly, lt = self.trail[-1]                               # a long step: a glow halfway too / un pas long
            self.trail.append(((lx + x) / 2, (ly + y) / 2, (lt + now) / 2))
        self.trail.append((x, y, now))
        self.trail = [t for t in self.trail if now - t[2] < 0.4][-40:]
        for tx, ty, tt in self.trail:
            k = 1 - (now - tt) / 0.4
            g = fx.sp.glow(S(22 + 18 * k), col, max(2, int(12 * k)), hot=0.45)
            screen.blit(g, (int(tx - g.get_width() / 2), int(ty - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        halo = fx.sp.glow(S(64), col, 9 + int(3 * (0.5 + 0.5 * math.sin(now * 18))), hot=0.5)
        screen.blit(halo, (int(x - halo.get_width() / 2), int(y - halo.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)

    def draw_wake(self, screen, x, y, now):
        """The disc's streak when it flies fast, white hot. / Le sillage du disque quand il file, blanc chaud."""
        S, pg, fx = self.S, self.pg, self.fx
        self.wake.append((x, y, now))
        self.wake = [w for w in self.wake if now - w[2] < 0.14][-16:]
        if len(self.wake) < 3:
            return
        (x0, y0, t0), (x1, y1, t1) = self.wake[0], self.wake[-1]
        speed = math.hypot(x1 - x0, y1 - y0) / max(0.016, t1 - t0)
        if speed < S(700):
            return
        k0 = min(1.0, (speed - S(700)) / S(1400))
        for wx, wy, wt in self.wake[:-1]:
            k = (1 - (now - wt) / 0.14) * k0
            g = fx.sp.glow(S(10 + 14 * k), (255, 236, 200), max(1, int(8 * k)), hot=0.3)
            screen.blit(g, (int(wx - g.get_width() / 2), int(wy - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)

    # ------------------------------------------------------------------ drawing / le dessin
    FIGURE_BOX = (84, 100)                                   # the owner's picture of a player fits in it / son image

    def own_figure(self, name):
        """The owner's picture of a player (sprites/wjammers/<name>.png), fitted, its plain background cleared, or None.
        / L'image du joueur déposée par le propriétaire, ajustée, son fond uni enlevé, ou None."""
        s = self.own.get(name)
        if s is not None:
            return s or None
        path = os.path.join(getattr(self.hd, "root", "") or "", "sprites", "wjammers", name + ".png")
        s = False
        if os.path.isfile(path):
            try:
                from .hd_mslug import clear_background
                img = Image.open(path).convert("RGBA")
                w, h = self.S(self.FIGURE_BOX[0]), self.S(self.FIGURE_BOX[1])
                img.thumbnail((w * 3, h * 3), Image.LANCZOS)
                if img.getchannel("A").getextrema()[0] == 255:
                    clear = clear_background(img)
                    img = clear if clear.getchannel("A").getbbox() else img
                box = img.getchannel("A").point(lambda v: 255 if v > 16 else 0).getbbox()
                if box is not None:
                    img = img.crop(box)
                    k = min(w / img.width, h / img.height)
                    img = img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.LANCZOS)
                    s = self.hd._surf(img)
            except Exception as e:                                    # a picture it cannot read: the drawing
                log = getattr(self.hd, "log", None)
                if callable(log):
                    log(f"sprites/wjammers/{name}.png: {e}")
                s = False
        self.own[name] = s
        return s or None

    def figure(self, side, vals):
        """The player's picture: the owner's, else ArcadeDMD's athlete in his colour. / Son image, sinon le dessin."""
        c = _n(vals.get(side + "_chr"))
        own = self.own_figure(FIGURES[int(c)]) if c is not None and 0 <= int(c) < len(FIGURES) else None
        if own is None and c is not None and int(c) == 3:
            own = self.own_figure("miller")                          # the same player under his other name
        if own is not None:
            if side == "p2":
                key = ("own_flip", int(c))
                f = self.imgs.get(key)
                if f is None:
                    f = self.imgs[key] = self.pg.transform.flip(own, True, False)
                return f, True
            return own, True
        col, dark = (P1C, (150, 50, 20)) if side == "p1" else (P2C, (20, 70, 150))
        return self.img(("athlete", side), self.S(64), self.S(80), athlete_draw(col, dark), flip=side == "p2"), False

    def draw_token(self, screen, side, x, y, vals, now):
        """A player on the court: his picture or the athlete in his colour, his tag at his feet, a shadow; in flames
        while he charges his super. (x, y) is where the game has him, his feet. / Un joueur sur le terrain : son image
        ou l'athlète à sa couleur, son étiquette à ses pieds, une ombre ; en flammes tant qu'il charge son super."""
        S, pg, fx = self.S, self.pg, self.fx
        fig, own = self.figure(side, vals)
        sh = self.imgs.get("token_shadow")
        if sh is None:
            sh = self.pg.Surface((S(64), S(22)), self.pg.SRCALPHA)
            self.pg.draw.ellipse(sh, (0, 0, 0, 80), sh.get_rect())
            self.imgs["token_shadow"] = sh
        screen.blit(sh, (int(x - sh.get_width() / 2), int(y + S(18) - sh.get_height() / 2)))
        cy = y - S(16)                                                 # the middle of the body / le milieu du corps
        if self.charge[side] is not None:                                   # charging: the ring of flames
            k = now - self.charge[side]
            for i in range(12):
                a = now * 5 + i * math.pi / 6
                rr = S(40) + S(7) * math.sin(now * 9 + i * 1.7)
                g = fx.sp.glow(S(13 + 7 * (0.5 + 0.5 * math.sin(now * 13 + i))), (255, 170, 60) if i % 2 else (255, 230, 120),
                               10 if k < 0.3 else 8, hot=0.45)
                screen.blit(g, (int(x + math.cos(a) * rr - g.get_width() / 2), int(cy + S(10) + math.sin(a) * rr * 0.7 - g.get_height() / 2)),
                            special_flags=pg.BLEND_RGB_ADD)
        screen.blit(fig, (int(x - fig.get_width() / 2), int(y + S(18) - fig.get_height())))
        tag = "P1" if side == "p1" else ("P2" if self.p2_in(vals) else "CPU")
        self.label(screen, tag, x, y + S(32), 15, P1C if side == "p1" else P2C, key="black", align="center", glow=0, alpha=150)

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

    def draw_disc(self, screen, x, y, h, now, held=False):
        """The disc and its shadow on the floor; in the air it grows and its shadow fades. / Le disque et son ombre."""
        S = self.S
        sh = self.imgs.get("disc_shadow")
        if sh is None:
            sh = self.pg.Surface((S(70), S(22)), self.pg.SRCALPHA)
            self.pg.draw.ellipse(sh, (0, 0, 0, 90), sh.get_rect())
            self.imgs["disc_shadow"] = sh
        if h > S(4) and not held:                                      # in the air: a target on the floor / en l'air
            k = min(1.0, h / S(160))
            sh.set_alpha(int(255 * (1 - 0.6 * k)))
            ring = self.imgs.get("disc_ring")
            if ring is None:
                ring = self.pg.Surface((S(90), S(30)), self.pg.SRCALPHA)
                self.pg.draw.ellipse(ring, (255, 255, 255, 150), ring.get_rect(), max(1, S(3)))
                self.imgs["disc_ring"] = ring
            ring.set_alpha(int(90 + 120 * (0.5 + 0.5 * math.sin(now * 12))))
            screen.blit(ring, (int(x - ring.get_width() / 2), int(y + S(8) - ring.get_height() / 2)))
        else:
            sh.set_alpha(255)
        screen.blit(sh, (int(x - sh.get_width() / 2), int(y + S(8) - sh.get_height() / 2)))
        disc = self.rotated("disc", self.img("disc", S(70), S(32), disc_draw), math.sin(now * 9) * 8, 4)
        sc = 1.0 + h / S(400)
        if sc > 1.01:
            disc = self.pg.transform.smoothscale(disc, (int(disc.get_width() * sc), int(disc.get_height() * sc)))
        screen.blit(disc, (int(x - disc.get_width() / 2), int(y - h - disc.get_height() / 2)))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg, fx = self.S, self.W, self.pg, self.fx
        self.scoreboard(screen, vals, logo, now)                       # first: a lob flies over it / un lob passe devant
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
            col = P1C if f["name"] == "set_points" else P2C
            if k >= 1.0 and f["zone"] is None:                         # the disc lands: dust, +2
                fx.smoke(f["x1"], f["y1"] + S(8), 8, (12, 22), 2.4, (0.5, 0.9), (10, 30), 40, (236, 220, 180), 170, "front")
                fx.glow(f["x1"], f["y1"], 20, 160, col, 0.4, "front", 0.8, 0.0)
                self.popup(f"+{f['pts']}", f["x1"], f["y1"] - S(60), col, 72, life=1.3, key="xbold")
                fx.shake(4, 0.25)
                self.pop[f["name"]] = now
                continue
            if k >= 1.0:                                               # a goal: the flash, the shock wave, the sparks
                right = f["x1"] > W / 2
                fx.flash(col, 0.3 if f["pts"] < 5 else 0.42, 0.3)
                fx.glow(f["x1"], f["y1"], 30, 520, col, 0.65, "front", 1.0, 0.0, hot=0.5)
                fx.glow(f["x1"], f["y1"], 16, 260, (255, 250, 220), 0.35, "front", 1.0, 0.0, hot=0.7)
                fx.sparks(f["x1"], f["y1"], 70, (255, 230, 150), (300, 1100), (100, 260) if right else (-80, 80), (0.4, 0.9), 700,
                          "front", 4, 34)
                fx.sparks(f["x1"], f["y1"], 30, col, (200, 700), (0, 360), (0.4, 0.8), 500, "front", 3, 20)
                self.popup(f"+{f['pts']}", f["x1"] + (-S(150) if right else S(150)), f["y1"], col, 96 if f["pts"] >= 5 else 80,
                           life=1.5, rise=50, key="xbold")
                fx.kick(S(22) if right else -S(22), 0, 0.5)             # the disc into the back wall: the image moves
                fx.shake(8 if f["pts"] < 5 else 12, 0.4)
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
        live = self.tracking(now)
        for side in ("p1", "p2"):                                       # the players' tokens / les jetons des joueurs
            tp = self.token_pos(side, vals, now)
            if tp is not None:
                self.draw_token(screen, side, tp[0], tp[1], vals, now)
        burning = self.super_side(now)
        pos = live if live is not None else (self._rally(now) if not self.flights and now >= self.pause else None)
        held = False
        if pos is not None and pos[2] < S(4):                           # held: lifted over the player / tenu : levé
            for tk in self.tokens.values():
                if tk is not None and abs(pos[0] - tk[0]) < S(40) and abs(pos[1] - tk[1]) < S(40):
                    pos, held = (pos[0], pos[1], S(52)), True
        if pos is not None:
            if burning:                                                 # a super shot: the trail under the disc
                self.draw_trail(screen, pos[0], pos[1], burning, now)
            else:
                self.trail = []
                self.draw_wake(screen, pos[0], pos[1], now)
            self.draw_disc(screen, pos[0], pos[1], pos[2], now, held)
        else:
            self.wake = []
        self.draw_slams(screen, now)

    def scoreboard(self, screen, vals, logo, now):
        """The board over the court (1.33): each player's name, nation and score on his side, the points of the set
        big in his colour with his sets won under them, the timer and the court between them, the points to win at the
        top right. / Le tableau au-dessus du terrain : nom, pays et score de chacun, les points du set en grand."""
        hd, S, W = self.hd, self.S, self.W
        hd.draw_logo(screen, logo, W / 2, S(4), S(440), S(84), now)
        bw, bh = S(1180), S(104)
        bx, by = W / 2 - bw / 2, S(96)
        self.box(screen, bx, by, bw, bh, (255, 214, 90))
        p2 = self.p2_in(vals)
        numw = hd.text_width("00", "black", S(76))
        for side, name, col, x, align, d in (("p1", "set_points", P1C, bx + S(26), "left", 1), ("p2", "set_points_p2", P2C, bx + bw - S(26), "right", -1)):
            tag = "P1" if side == "p1" else ("P2" if p2 else "CPU")
            who = self.player_name(vals, side)
            flag = self.flag(vals, side)
            y = by + S(12)
            xx = x
            if flag is not None:                                        # the flag first, by the edge / le drapeau au bord
                screen.blit(flag, (int(xx if d > 0 else xx - flag.get_width()), int(y + S(4))))
                xx += d * (flag.get_width() + S(12))
            if who != tag:                                              # the tag small, then the name / l'étiquette, le nom
                tw = self.text(screen, tag, xx, y + S(10), 18, col, key="black", align=align, glow=0)
                xx += d * (tw + S(8))
                self.text(screen, who, xx, y, 30, col, key="black", align=align, glow=0.3)
            else:
                self.text(screen, tag, xx, y, 30, col, key="black", align=align, glow=0.3)
            sc = _n(vals.get("score" if side == "p1" else "score_p2"))  # his score under, small / son score
            if sc is not None:
                self.text(screen, f"{int(sc):,}".replace(",", " "), x, by + S(60), 22, (235, 232, 215), key="bold", align=align, glow=0)
            nx = W / 2 - d * S(150)                                     # the points of the set, big / les points du set
            v = _n(vals.get(name))
            if v is not None:
                k = now - self.pop[name]
                hd.put_number(screen, f"{int(v):02d}", "black", S(76), WHITE if k < 0.35 else col, nx, by + S(40),
                              "right" if side == "p1" else "left", "middle", scale=1.0 + 0.3 * max(0.0, 1 - k / 0.35))
            n = _n(vals.get("sets" if side == "p1" else "sets_p2"))      # his sets won, gold discs under them / ses sets
            if n is not None:
                cx0 = nx - d * numw / 2
                for i in range(2):
                    cx, cy = int(cx0 + (i - 0.5) * S(30)), int(by + S(88))
                    if i < int(n):
                        self.pg.draw.circle(screen, (255, 214, 90), (cx, cy), S(9))
                        self.pg.draw.circle(screen, (120, 80, 10), (cx, cy), S(9), max(1, S(2)))
                    else:
                        self.pg.draw.circle(screen, (70, 64, 50), (cx, cy), S(9), max(1, S(2)))
        t = _n(vals.get("time"))
        if t is not None:
            low = t <= 10
            pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
            hd.put_number(screen, f"{int(t)}", "black", S(50), RED if low else GOLD, W / 2, by + S(34), "center", "middle",
                          scale=1 + 0.12 * pulse)
        court = _n(vals.get("court"))
        if court is not None:                                           # the court under the timer / le terrain
            self.text(screen, tr(*COURTS[int(court) % 6]), W / 2, by + S(80), 18, (200, 196, 180), key="bold", align="center",
                      valign="middle", glow=0)
        tw = _n(vals.get("to_win"))
        if tw is not None:                                              # the points to win, top right / les points
            self.text(screen, tr(f"{int(tw)} POINTS POUR GAGNER", f"{int(tw)} POINTS TO WIN"), W - S(24), S(100), 18, (200, 196, 180),
                      key="bold", align="right", glow=0)
        if p2:                                                          # two humans: the matches won, top right
            x = W - S(24)
            x -= self.text(screen, str(self.wins["p2"]), x, S(28), 34, P2C, key="black", align="right", glow=0.3) + S(10)
            x -= self.text(screen, "-", x, S(28), 34, (200, 196, 180), key="black", align="right", glow=0) + S(10)
            x -= self.text(screen, str(self.wins["p1"]), x, S(28), 34, P1C, key="black", align="right", glow=0.3) + S(16)
            self.text(screen, tr("MATCHS", "MATCHES"), x, S(36), 20, (200, 196, 180), key="bold", align="right", glow=0)
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
        hurt = _clamp(1 - (now - self.hurt[side]) / 0.45)
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
    CREDITS = (0.5, 350)                                  # over the power gauge / au-dessus de la jauge de puissance
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
