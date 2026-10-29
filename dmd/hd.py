"""Smooth HD display for an LCD screen (e.g. the 1920 x 460 marquee of a Vewlix): the scene is drawn at the
screen size with vector fonts, gradients, glowing texts and the game's logo from LaunchBox (Clear Logo).
Two layouts: fighting games, and all the other games.

Affichage HD lisse pour un écran LCD (le marquee 1920 x 460 d'une Vewlix par exemple).

La scène n'est plus dessinée en 128 x 32 puis agrandie. Elle est dessinée directement à la taille de l'écran,
avec des polices vectorielles (Inter, dossier fonts), des dégradés, une lueur sous les textes et le logo du jeu
pris dans les médias de LaunchBox et BigBox (Clear Logo). Sans logo trouvé, le titre du jeu le remplace.

Deux mises en page
- combat (King of Fighters, Samurai Shodown...) : score ou CHALLENGER et BEAT BY en haut, logo, barres de vie
  avec traînée des coups encaissés, chrono, nom des combattants, équipes des King of Fighters, crédits ;
- les autres jeux : logo, score de chaque joueur, puis vies, bombes, arme, crédits... en bas.

Rendu avec pygame. Les textes, dégradés et logos sont préparés une fois avec Pillow puis gardés en cache.
"""

import math
import os
import time
from collections import OrderedDict

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .hd_coin import CoinDoors
from .hd_fight import FightFX
from .hd_games import SCENES as _SCENES_117
from .hd_games2 import SCENES as _SCENES_118
from .hd_games3 import SCENES as _SCENES_119
from .hd_mslug import MetalSlugScene, family
from .i18n import tr

AMBER, RED, CREAM, LINE = (255, 168, 48), (255, 52, 30), (235, 225, 205), (168, 112, 30)
GREY, DIM = (150, 150, 165), (90, 90, 100)
BARS = {"g": ((48, 240, 160), (20, 150, 110)), "y": ((255, 214, 60), (190, 130, 20)), "r": ((255, 70, 50), (160, 30, 20))}
FONT_FILES = {"black": "Inter-Black.otf", "xbold": "Inter-ExtraBold.otf", "bold": "Inter-Bold.otf",
              "logo": "InterDisplay-BlackItalic.otf", "stencil": "BlackOpsOne-Regular.ttf"}
FALLBACK_FONTS = ("C:\\Windows\\Fonts\\arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
# étiquettes (français, anglais) : tr() au moment du dessin, la langue est choisie après l'import
CHIPS = (("lives", ("VIES", "LIVES")), ("lives_p2", ("VIES J2", "LIVES P2")), ("bombs", ("BOMBES", "BOMBS")),
         ("bombs_p2", ("BOMBES J2", "BOMBS P2")), ("prisoners", ("PRISONNIERS", "PRISONERS")), ("rings", ("ANNEAUX", "RINGS")),
         ("time", ("TEMPS", "TIME")), ("record", ("RECORD", "HI-SCORE")), ("credits", ("CRÉDITS", "CREDITS")))
GAME_SCENES = dict(_SCENES_117, **_SCENES_118, **_SCENES_119)     # Neo Geo games done one by one, the three batches
MSLUG_WEAPONS = {0: ("PISTOLET", "HANDGUN"), 1: ("FUSIL À POMPE", "SHOTGUN"), 2: ("LANCE-FLAMMES", "FLAMETHROWER"),
                 3: ("LANCE-ROQUETTES", "ROCKET LAUNCHER"), 4: ("MITRAILLETTE", "MACHINE GUN")}


def _num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    return None


class HDRenderer:
    FPS = 40

    def __init__(self, pg, size, root, cfg=None, log=print, logos=None):
        self.pg = pg
        self.W, self.H = size
        self.s = min(self.W / 1920.0, self.H / 460.0)
        self.root = root
        self.log = log
        self.fonts = {}
        self.fits = {}
        self.metrics = {}
        self.scaled = OrderedDict()
        self.cache = OrderedDict()
        self.bars = {}
        self.trails = {}
        self.logo_key = None
        self.logo = None
        self.logo_file = False
        self.logo_retry = 0.0
        self.fitted = {}
        if logos is None and (cfg or {}).get("logos", True):
            from .launchbox import LogoFinder
            logos = LogoFinder(root, cfg, log)
        self.logos = logos
        self.bg = self._background()
        self.badge = self._badge()
        self.clock = time.monotonic           # remplacé par une horloge simulée pour les vidéos de démo
        self.themed = (cfg or {}).get("themes", True)
        self.mslug = None
        self.fight = None
        self.game_scene = None        # (key, scene) of the game played, games done one by one (hd_games)
        self.coins_on = (cfg or {}).get("coins", True)   # fighting games: coin doors on the attract screen
        self.coins = None
        self.intro_serial = 0         # game logo when a game starts (the engine counts the starts)
        self.intro_t0 = None
        self.intro_len = 2.6
        self.logo_alpha = 1.0         # logo of the scene, hidden during the intro
        self.logo_rect = None         # where the scene drew its logo
        self.enter = 1.0              # attract screen coming in after the intro
        self.veil = None
        self.flash_glow = None

    # ------------------------------------------------------------ outils
    def S(self, v):
        return int(round(v * self.s))

    def _surf(self, img):
        pg = self.pg
        fn = getattr(pg.image, "frombytes", None) or pg.image.fromstring
        surf = fn(img.tobytes(), img.size, img.mode)
        try:
            return surf.convert_alpha() if img.mode == "RGBA" else surf.convert()
        except pg.error:                         # pas encore de fenêtre (tests)
            return surf

    def font(self, key, size):
        k = (key, size)
        f = self.fonts.get(k)
        if f is None:
            paths = [os.path.join(self.root, "fonts", FONT_FILES.get(key, FONT_FILES["black"]))] + list(FALLBACK_FONTS)
            for p in paths:
                try:
                    f = ImageFont.truetype(p, size)
                    break
                except OSError:
                    continue
            if f is None:
                f = ImageFont.load_default()
            self.fonts[k] = f
        return f

    def text(self, text, key, size, color, glow=0.5):
        """Texte prêt à poser (surface, lueur), gardé en cache."""
        ck = (text, key, size, color, glow)
        hit = self.cache.get(ck)
        if hit is not None:
            self.cache.move_to_end(ck)
            return hit
        f = self.font(key, size)
        l, t, r, b = f.getbbox(text) if text else (0, 0, 1, 1)
        pad = int(size * 0.45) + 4 if glow else 2
        w, h = max(1, r - l) + 2 * pad, max(1, b - t) + 2 * pad
        alpha = Image.new("L", (w, h), 0)
        ImageDraw.Draw(alpha).text((pad - l, pad - t), text, font=f, fill=255)
        img = Image.new("RGBA", (w, h), tuple(color) + (0,))
        img.putalpha(alpha)
        out = {"surf": self._surf(img), "w": r - l, "h": b - t, "pad": pad, "key": ck}
        if glow:
            gl = Image.new("RGB", (w, h))
            gl.paste(tuple(int(c * glow) for c in color), (0, 0, w, h), alpha.filter(ImageFilter.MaxFilter(3)))
            out["glow"] = self._surf(gl.filter(ImageFilter.GaussianBlur(max(2, size * 0.16))))
        self.cache[ck] = out
        while len(self.cache) > 400:
            self.cache.popitem(last=False)
        return out

    def put(self, screen, t, x, y, align="left", valign="top", scale=1.0, alpha=1.0):
        """Pose un texte. (x, y) vise le bord ou le centre des lettres elles-mêmes. Renvoie la largeur.
        alpha < 1 : texte transparent (sa lueur disparaît sous 0,55)."""
        pg = self.pg
        surf, glow = t["surf"], t.get("glow")
        if scale != 1.0:
            scale = round(scale * 50) / 50.0                     # tailles gardées en cache (pas de 2 %)
            size = (max(1, int(surf.get_width() * scale)), max(1, int(surf.get_height() * scale)))
            if size[0] * size[1] > 250000:                       # très grand texte qui grossit (bandeau) : rapide
                surf = pg.transform.scale(surf, size)
                glow = pg.transform.scale(glow, size) if glow is not None else None
            else:
                sk = (t.get("key"), scale)
                hit = self.scaled.get(sk) if sk[0] is not None else None
                if hit is None:
                    hit = (pg.transform.smoothscale(surf, size), pg.transform.smoothscale(glow, size) if glow is not None else None)
                    if sk[0] is not None:
                        self.scaled[sk] = hit
                        while len(self.scaled) > 300:
                            self.scaled.popitem(last=False)
                surf, glow = hit
        w, h, pad = t["w"] * scale, t["h"] * scale, t["pad"] * scale
        ix = x if align == "left" else (x - w / 2 if align == "center" else x - w)
        iy = y if valign == "top" else (y - h / 2 if valign == "middle" else y - h)
        pos = (int(ix - pad), int(iy - pad))
        if glow is not None and alpha > 0.55:
            screen.blit(glow, pos, special_flags=pg.BLEND_RGB_ADD)
        if alpha < 1.0:
            surf.set_alpha(max(0, int(255 * alpha)))
            screen.blit(surf, pos)
            surf.set_alpha(255)
        else:
            screen.blit(surf, pos)
        return w

    def fit_size(self, text, key, size, max_w, min_size=10):
        """Taille de police pour que le texte tienne dans max_w pixels (mémorisée)."""
        ck = (text, key, size, max_w, min_size)
        hit = self.fits.get(ck)
        if hit is not None:
            return hit
        s0 = size
        while size > min_size:
            l, _, r, _ = self.font(key, size).getbbox(text)
            if r - l <= max_w:
                break
            size = int(size * 0.9)
        if len(self.fits) > 2000:
            self.fits.clear()
        self.fits[(text, key, s0, max_w, min_size)] = size
        return size

    def _glyph(self, key, size, c):
        """Mesures d'un caractère : (décalage gauche, haut de l'encre, avance, bas de l'encre)."""
        k = (key, size, c)
        m = self.metrics.get(k)
        if m is None:
            f = self.font(key, size)
            l, t, r, b = f.getbbox(c) if c.strip() else (0, 0, 0, 0)
            m = self.metrics[k] = (l, t, f.getlength(c), b, r)
        return m

    def text_width(self, text, key, size):
        """Largeur de l'encre, du premier au dernier caractère."""
        if not text:
            return 0
        return sum(self._glyph(key, size, c)[2] for c in text[:-1]) + self._glyph(key, size, text[-1])[4]

    def put_number(self, screen, text, key, size, color, x, y, align="left", valign="top", scale=1.0, glow=0.5):
        """Nombre posé chiffre par chiffre : un score qui défile ne redessine aucun texte."""
        total = self.text_width(text, key, size) * scale
        x0 = x if align == "left" else (x - total / 2 if align == "center" else x - total)
        _, top, _, bottom, _ = self._glyph(key, size, "0")
        if valign == "middle":
            y -= (bottom - top) * scale / 2
        elif valign == "bottom":
            y -= (bottom - top) * scale
        pen = 0.0
        for c in text:
            l, t, adv, _, _ = self._glyph(key, size, c)
            if c.strip():
                self.put(screen, self.text(c, key, size, color, glow), x0 + (pen + l) * scale, y + (t - top) * scale,
                         scale=scale)
            pen += adv * scale
        return total

    # ------------------------------------------------------------ éléments fixes
    def _background(self):
        W, H = self.W, self.H
        bg = Image.new("RGB", (W, H))
        d = ImageDraw.Draw(bg)
        for y in range(H):
            k = y / max(1, H)
            d.line([0, y, W, y], fill=(int(7 + 9 * k), int(9 + 5 * k), int(22 + 16 * k)))
        streak = Image.new("L", (W, H), 0)
        sd = ImageDraw.Draw(streak)
        step, wd, sl = max(40, self.S(140)), max(10, self.S(46)), self.S(200)
        for i, x in enumerate(range(-sl * 2, W + sl * 2, step)):      # rayures obliques très discrètes
            sd.polygon([(x, 0), (x + wd, 0), (x + wd - sl, H), (x - sl, H)], fill=10 + (i % 3) * 4)
        bg = Image.composite(Image.new("RGB", (W, H), (60, 90, 170)), bg, streak)
        vign = Image.new("L", (W, H), 0)
        ImageDraw.Draw(vign).ellipse([-W // 6, -H // 2, W + W // 6, H + H // 2], fill=255)
        vign = vign.filter(ImageFilter.GaussianBlur(max(20, self.S(120))))
        return self._surf(Image.composite(bg, Image.new("RGB", (W, H)), vign))

    def _badge(self):
        w, h = self.S(200), self.S(160)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(img).rounded_rectangle([0, 0, w - 1, h - 1], radius=self.S(26), fill=(14, 16, 34, 235),
                                              outline=CREAM + (255,), width=max(2, self.S(4)))
        return self._surf(img)

    def _bar(self, w, h, side):
        key = (w, h, side)
        b = self.bars.get(key)
        if b is not None:
            return b
        sl = self.S(26)
        shape = [(sl, 0), (w - 1, 0), (w - 1 - sl, h - 1), (0, h - 1)] if side == "left" else \
                [(0, 0), (w - 1 - sl, 0), (w - 1, h - 1), (sl, h - 1)]
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).polygon(shape, fill=255)

        def solid(color):
            img = Image.new("RGBA", (w, h), tuple(color) + (0,))
            img.putalpha(mask)
            return self._surf(img)

        def gradient(top, bottom):
            img = Image.new("RGB", (w, h))
            d = ImageDraw.Draw(img)
            for i in range(h):
                k = i / max(1, h - 1)
                d.line([0, i, w, i], fill=tuple(int(top[j] * (1 - k) + bottom[j] * k) for j in range(3)))
            hi = max(1, self.S(3))
            d.line([0, hi, w, hi], fill=(235, 255, 248))
            img = img.convert("RGBA")
            img.putalpha(mask)
            return self._surf(img)

        line = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(line).line(shape + [shape[0]], fill=CREAM + (255,), width=max(2, self.S(4)))
        b = {"back": solid((70, 12, 14)), "trail": solid((255, 235, 235)), "line": self._surf(line),
             "fill": {k: gradient(*v) for k, v in BARS.items()}}
        self.bars[key] = b
        return b

    def draw_bar(self, screen, x, y, w, h, frac, trail, side):
        pg = self.pg
        b = self._bar(w, h, side)
        screen.blit(b["back"], (x, y))

        def span(f):
            n = int(round(w * max(0.0, min(1.0, f))))
            return (w - n, n) if side == "left" else (0, n)

        tx, tw = span(trail)
        if tw > 0:
            screen.blit(b["trail"], (x + tx, y), area=pg.Rect(tx, 0, tw, h))
        fx, fw = span(frac)
        if fw > 0:
            col = "g" if frac > 0.5 else ("y" if frac > 0.25 else "r")
            screen.blit(b["fill"][col], (x + fx, y), area=pg.Rect(fx, 0, fw, h))
        screen.blit(b["line"], (x, y))

    def trail(self, side, frac, now):
        """Traînée des dégâts : reste 0,3 s sur l'ancienne vie, puis la rattrape en 0,5 s."""
        st = self.trails.get(side)
        if st is None or frac > st["hp"] + 0.005:          # nouveau round, vie remplie
            self.trails[side] = {"hp": frac, "from": frac, "t": now}
            return frac
        if frac < st["hp"] - 0.0001:
            st["from"] = max(self._trail_at(st, now), st["hp"])
            st["hp"], st["t"] = frac, now
        return self._trail_at(st, now)

    @staticmethod
    def _trail_at(st, now):
        dt = now - st["t"]
        if dt < 0.3:
            return st["from"]
        if dt < 0.8:
            return st["from"] - (st["from"] - st["hp"]) * (dt - 0.3) / 0.5
        return st["hp"]

    # ------------------------------------------------------------ logo du jeu
    def _title_logo(self, title):
        """Titre du jeu en métal, quand LaunchBox n'a pas de logo."""
        text = (title or "ARCADE").upper()
        size = self.fit_size(text, "logo", self.S(96), self.S(1100), self.S(30))
        f = self.font("logo", size)
        l, t, r, b = f.getbbox(text)
        pad = self.S(14) + 4
        w, h = r - l + 2 * pad, b - t + 2 * pad
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).text((pad - l, pad - t), text, font=f, fill=255)
        grad = Image.new("RGB", (w, h))
        gd = ImageDraw.Draw(grad)
        for y in range(h):
            k = y / max(1, h - 1)
            if k < 0.45:
                c = (255 - int(40 * k), 255 - int(30 * k), 255)
            elif k < 0.55:
                c = (120, 140, 190)
            else:
                c = (190 + int(40 * (k - 0.55)), 200 + int(30 * (k - 0.55)), 240)
            gd.line([0, y, w, y], fill=c)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        img.paste((20, 24, 60, 255), (0, 0, w, h), mask.filter(ImageFilter.MaxFilter(max(3, (self.S(9) // 2) * 2 + 1))))
        img.paste(grad, (0, 0), mask)
        return img

    def _logo_image(self, path):
        img = Image.open(path)
        img.load()
        img = img.convert("RGBA")
        box = img.getchannel("A").getbbox()
        return img.crop(box) if box else img

    def logo_for(self, meta, title):
        key = (meta.get("system") or "", meta.get("parent") or "", title)
        now = time.monotonic()
        if key != self.logo_key:
            self.logo_key, self.logo, self.logo_file, self.logo_retry, self.fitted = key, None, False, 0.0, {}
        if not self.logo_file and now >= self.logo_retry:
            path = self.logos.find([key[0], key[1]], title) if self.logos is not None else None
            if path:
                try:
                    self.logo, self.logo_file, self.fitted = self._logo_image(path), True, {}
                except OSError as e:
                    self.log(tr(f"écran HD : logo illisible {path} ({e})", f"HD screen: unreadable logo {path} ({e})"))
            done = self.logos is None or self.logos.ready
            self.logo_retry = float("inf") if (self.logo_file or done) else now + 1.0
            if self.logo is None:
                self.logo = self._title_logo(title)
        return self.logo

    def fit_logo(self, img, max_w, max_h):
        """Logo brought to the size of its box, with its light band (kept until the logo changes)."""
        key = (max_w, max_h)
        fit = self.fitted.get(key)
        if fit is None:
            k = min(max_w / img.width, max_h / img.height, 1.6)
            size = (max(1, int(img.width * k)), max(1, int(img.height * k)))
            small = img.resize(size, Image.LANCZOS)
            white = Image.new("RGBA", size, (255, 255, 255, 0))
            white.putalpha(small.getchannel("A"))
            band_w = max(8, size[1] // 2)
            band = Image.new("RGBA", (band_w * 3, size[1]), (255, 255, 255, 0))
            bd = ImageDraw.Draw(band)
            for i in range(band_w * 3):                   # bande de lumière en biais, bords doux
                a = int(150 * max(0.0, 1 - abs(i - band_w * 1.5) / (band_w * 0.9)))
                bd.line([(i + size[1] // 3, 0), (i - size[1] // 3, size[1])], fill=(255, 255, 255, a), width=2)
            fit = {"surf": self._surf(small), "mask": self._surf(white), "band": self._surf(band), "w": size[0], "h": size[1]}
            self.fitted[key] = fit
        return fit

    def shine(self, screen, fit, x, top, ph, alpha=1.0):
        """Light band across the logo (ph from 0 to 1)."""
        pg = self.pg
        bw = fit["band"].get_width()
        tmp = pg.Surface((fit["w"], fit["h"]), pg.SRCALPHA)
        tmp.blit(fit["band"], (int(-bw + (fit["w"] + bw) * ph), 0))
        tmp.blit(fit["mask"], (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        if alpha < 0.99:
            tmp.set_alpha(int(255 * alpha))
        screen.blit(tmp, (x, top))

    def draw_logo(self, screen, img, cx, y, max_w, max_h, now, valign="top"):
        if img is None:
            return 0
        fit = self.fit_logo(img, max_w, max_h)
        x = int(cx - fit["w"] / 2)
        top = int(y - fit["h"] / 2) if valign == "middle" else int(y)
        self.logo_rect = (x, top, fit["w"], fit["h"])      # where the logo intro ends
        a = self.logo_alpha                                # 0 during the game's logo intro
        if a <= 0.01:
            return fit["h"]
        if a < 0.99:
            fit["surf"].set_alpha(int(255 * a))
            screen.blit(fit["surf"], (x, top))
            fit["surf"].set_alpha(255)
        else:
            screen.blit(fit["surf"], (x, top))
        ph = (now % 4.5) / 0.9                             # reflet toutes les 4,5 s
        if ph <= 1.0:
            self.shine(screen, fit, x, top, ph, a)
        return fit["h"]

    # ------------------------------------------------------------ dessin d'une image
    def render(self, screen, eng):
        now = self.clock()
        if eng.mode != "game":
            screen.fill((0, 0, 0))
            self.FPS = HDRenderer.FPS
            self.intro_t0 = None
            return
        lt = self._intro_time(eng, now)
        cross = 1.0 if lt is None else max(0.0, min(1.0, (lt - (self.intro_len - 0.45)) / 0.45))
        self.logo_alpha = 1.0 if lt is None else 0.0       # the intro's logo goes to the scene's logo at the end
        self.enter = cross
        self.logo_rect = None
        self._render_scene(screen, eng, now)
        self.logo_alpha = self.enter = 1.0
        if lt is not None:
            self._draw_intro(screen, now, lt, cross)

    # ------------------------------------------------------------ logo du jeu au lancement
    def _intro_time(self, eng, now):
        """Seconds since the game started, while its logo intro is on, otherwise None."""
        serial = getattr(eng, "intro_serial", 0)
        if serial != self.intro_serial:
            self.intro_serial = serial
            self.intro_t0 = now
            try:
                self.intro_len = max(1.0, min(10.0, float((getattr(eng, "intro_cfg", None) or {}).get("seconds", 2.6))))
            except (TypeError, ValueError):
                self.intro_len = 2.6
        if self.intro_t0 is None:
            return None
        lt = now - self.intro_t0
        if lt < 0 or lt >= self.intro_len:
            self.intro_t0 = None
            return None
        return lt

    def _draw_intro(self, screen, now, lt, cross):
        """The logo comes in big on a dark screen, with a white flash and a light sweep, then takes its place."""
        pg, W, S = self.pg, self.W, self.S
        fade = min(1.0, lt / 1.6)
        dark = int(255 * (1 - fade) * 0.95)
        if dark > 0:
            if self.veil is None or self.veil.get_size() != screen.get_size():
                self.veil = pg.Surface(screen.get_size()).convert()
                self.veil.fill((0, 0, 0))
            self.veil.set_alpha(dark)
            screen.blit(self.veil, (0, 0))
        if 0.45 < lt < 1.2:                                          # white flash when it lands
            k = max(0.0, 1 - abs(lt - 0.6) / 0.6) * 0.35
            if self.flash_glow is None:                              # soft ellipse, blurred small then enlarged (quick)
                gw, gh = S(1040) + S(240), S(260) + S(240)
                q = 4
                m = Image.new("L", (max(4, gw // q), max(4, gh // q)), 0)
                ImageDraw.Draw(m).ellipse([S(120) / q, S(120) / q, (gw - S(120)) / q, (gh - S(120)) / q], fill=255)
                m = m.filter(ImageFilter.GaussianBlur(max(1, S(60) / q))).resize((gw, gh), Image.BILINEAR)
                self.flash_glow = self._surf(Image.merge("RGB", (m, m, m)))
            g = self.flash_glow.copy()
            v = int(255 * k)
            g.fill((v, v, v), special_flags=pg.BLEND_RGB_MULT)
            screen.blit(g, (int(W / 2 - g.get_width() / 2), int(S(190) - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        logo = self.logo
        if logo is None:
            return
        a = min(1.0, lt / 0.3)
        fit = self.fit_logo(logo, S(1000), S(220))
        sc = 0.55 + 0.45 * min(1.0, lt / 0.5) ** 0.5
        sc *= 1.0 + 0.04 * max(0.0, 1 - abs(lt - 0.55) / 0.25)
        w, h, cx, cy = fit["w"] * sc, fit["h"] * sc, W / 2, S(190)
        if cross > 0:                                                # glides to the scene's own logo
            dest = self.logo_rect
            if dest is None:
                a *= 1.0 - cross
            else:
                e = cross * cross * (3 - 2 * cross)
                dx, dy, dw, dh = dest
                cx, cy = cx + (dx + dw / 2 - cx) * e, cy + (dy + dh / 2 - cy) * e
                w, h = w + (dw - w) * e, h + (dh - h) * e
        if a <= 0.01:
            return
        size = (max(1, int(round(w))), max(1, int(round(h))))
        surf = fit["surf"]
        if size != (fit["w"], fit["h"]):
            surf = pg.transform.smoothscale(surf, size)
        x, top = int(cx - size[0] / 2), int(cy - size[1] / 2)
        surf.set_alpha(int(255 * a))
        screen.blit(surf, (x, top))
        surf.set_alpha(255)
        if surf is fit["surf"] and lt >= 0.8:                       # light sweeps across the logo
            ph = ((lt - 0.8) % 1.0) / 0.9
            if ph <= 1.0:
                self.shine(screen, fit, x, top, ph, a)

    def _render_scene(self, screen, eng, now):
        st = eng.state
        vals, meta = st.values, st.meta
        key = meta.get("game") or ""
        title = meta.get("title") or ""
        g = eng.library.get(key) or {}
        if self.themed and family(key):                       # Metal Slug : décor animé et effets
            if self.mslug is None:
                self.mslug = MetalSlugScene(self)
            self.FPS = MetalSlugScene.FPS
            self.mslug.render(screen, eng, now, self.logo_for(meta, title))
            return
        scene = (g.get("hd") or {}).get("scene") if isinstance(g.get("hd"), dict) else None
        if self.themed and scene in GAME_SCENES:              # Neo Geo games done one by one (1.17): a scene of their own
            if self.game_scene is None or self.game_scene[0] != scene:
                self.game_scene = (scene, GAME_SCENES[scene](self))
            self.FPS = GAME_SCENES[scene].FPS
            self.game_scene[1].render(screen, eng, now, self.logo_for(meta, title))
            return
        self.FPS = HDRenderer.FPS
        fight = (g.get("scene_from") or key) == "neogeo_combat" or ("health" in vals and "health_p2" in vals)
        logo = self.logo_for(meta, title)
        if fight and self.themed:                             # combat : salle de tournoi, étincelles, combos, K.O.
            if self.fight is None:
                self.fight = FightFX(self)
            self.FPS = MetalSlugScene.FPS
            self.fight.update(vals, now, key, g, idle=self._nobody(vals))
            target = self.fight.begin(screen, now)
            self.draw_fight(target, eng, vals, logo, now)
            self.fight.end(screen, target, now)
            return
        screen.blit(self.bg, (0, 0))
        if fight:
            self.draw_fight(screen, eng, vals, logo, now)
        else:
            self.draw_generic(screen, eng, vals, logo, now, key)
        self.pg.draw.rect(screen, LINE, (0, self.S(444), self.W, max(2, self.S(8))))

    @staticmethod
    def _nobody(vals):
        """Nobody plays (the game's demo runs): attract screen. / Personne ne joue : écran d'attente."""
        p1m, p2m = vals.get("p1_mode"), vals.get("p2_mode")
        return p1m is not None and p1m not in (1, 2) and p2m not in (1, 2)

    def _pulse(self, now, period=1.2):
        a = 0.55 + 0.45 * (0.5 + 0.5 * math.cos(now * 2 * math.pi / period))
        return round(a * 8) / 8                               # 8 niveaux : textes gardés en cache

    def _invite(self, vals, now):
        credits = _num(vals.get("credits"))
        word = "PRESS START" if credits and credits > 0 else "INSERT COIN"
        return word, tuple(int(c * self._pulse(now)) for c in AMBER)

    def _score(self, screen, eng, name, x, y, align, size):
        v = eng.state.values.get(name)
        if v is None:
            return
        pop = 0.0
        t = eng.state.changed_at.get(name)
        if t is not None:
            dt = eng.ctx.t - t
            if 0 <= dt < 0.25:
                pop = 1 - dt / 0.25
        self.put(screen, self.text(str(v), "black", size, AMBER), x, y, align, scale=1 + 0.2 * pop)

    # ------------------------------------------------------------ jeux de combat
    def draw_fight(self, screen, eng, vals, logo, now):
        W, S = self.W, self.S
        p1m, p2m = vals.get("p1_mode"), vals.get("p2_mode")
        known = p1m is not None
        p1_in = p1m in (1, 2) or not known
        p2_in = p2m in (1, 2)
        if known and not p1_in and not p2_in:                 # personne ne joue : démo du jeu
            self.draw_logo(screen, logo, W / 2, S(190), S(1000), S(220), now, valign="middle")
            if self.coins_on:                                 # monnayeurs, pièces, crédits, boutons START
                if self.coins is None:
                    self.coins = CoinDoors(self)
                fx = self.fight.fx if self.fight is not None else None
                self.coins.draw(screen, vals, now, fx, (getattr(eng, "cfg", None) or {}).get("coin_symbol", "€"), self.enter)
                return
            word, col = self._invite(vals, now)
            credits = _num(vals.get("credits"))
            msg = tr(f"CRÉDITS {int(credits):02d}", f"CREDITS {int(credits):02d}") if credits else word
            self.put(screen, self.text(msg, "xbold", S(56), col if not credits else AMBER), W / 2, S(372), "center", "middle")
            return
        # en haut : score de chaque joueur, ou CHALLENGER et BEAT BY en match VS
        b1, b2 = _num(vals.get("beat")), _num(vals.get("beat_p2"))
        vs = p1m == 1 and p2m == 1 and b1 is not None and b2 is not None and (b1 > 0 or b2 > 0)
        for side, x, align in (("p1", S(30), "left"), ("p2", W - S(30), "right")):
            human = p1_in if side == "p1" else p2_in
            if vs:
                b = b1 if side == "p1" else b2
                txt = f"BEAT BY {int(b):02d}" if b else "CHALLENGER"
                self.put(screen, self.text(txt, "black", S(54), RED if not b else AMBER), x, S(22), align)
            elif human:
                self._score(screen, eng, "score" if side == "p1" else "score_p2", x, S(14), align, S(64))
            else:
                word, col = self._invite(vals, now)
                self.put(screen, self.text(word, "xbold", S(40), col), x, S(24), align)
        wide = not self.logo_file                       # titre écrit à la place du logo : plus de place en largeur
        self.draw_logo(screen, logo, W / 2, S(8), S(900 if wide else 640), S(124), now)
        # au milieu : barres de vie et chrono
        h1, h2 = _num(vals.get("health")), _num(vals.get("health_p2"))
        cx = W / 2
        bw = int(cx - S(160) - S(40))
        if h1 is not None and h2 is not None:
            f1, f2 = h1 / 100.0, h2 / 100.0
            self.draw_bar(screen, S(40), S(176), bw, S(50), f1, self.trail("p1", f1, now), "left")
            self.draw_bar(screen, int(cx + S(160)), S(176), bw, S(50), f2, self.trail("p2", f2, now), "right")
        screen.blit(self.badge, (int(cx - self.badge.get_width() / 2), S(140)))
        ko = h1 is not None and h2 is not None and (h1 <= 0 or h2 <= 0)
        t = _num(vals.get("time"))
        if ko:
            ks = self.fight.ko_scale(now) if self.fight is not None else 1.0
            self.put(screen, self.text("KO", "black", S(120), (255, 48, 32)), cx, S(220), "center", "middle", scale=ks)
        elif t is not None and h1 is not None:
            low = t <= 10 and self.fight is not None                 # chrono sous 10 : rouge qui bat
            pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
            self.put(screen, self.text(str(int(t)), "black", S(130), RED if low else AMBER), cx, S(220), "center", "middle",
                     scale=1 + 0.1 * pulse)
        else:
            self.put(screen, self.text("VS", "black", S(110), AMBER), cx, S(220), "center", "middle")
        # en bas : qui joue, le combattant en cours, les équipes des King of Fighters
        room = cx - S(120) - S(40)
        for side in ("p1", "p2"):
            human = p1_in if side == "p1" else p2_in
            tag = ("P1" if side == "p1" else "P2") if human else "CPU"
            name = vals.get(side + "_char")
            tsize = S(76)
            tw = self.text(tag, "black", tsize, AMBER)["w"]
            nsize = self.fit_size(str(name), "black", S(76), room - tw - S(40), S(30)) if name else tsize
            if side == "p1":
                self.put(screen, self.text(tag, "black", tsize, AMBER), S(40), S(268))
                if name:
                    self.put(screen, self.text(str(name), "black", nsize, RED), S(40) + tw + S(40), S(268 + (76 - nsize / self.s) * 0.8))
            else:
                self.put(screen, self.text(tag, "black", tsize, AMBER), W - S(40), S(268), "right")
                if name:
                    self.put(screen, self.text(str(name), "black", nsize, RED), W - S(40) - tw - S(40),
                             S(268 + (76 - nsize / self.s) * 0.8), "right")
            team = self.team(eng, side)
            if team:
                self.draw_team(screen, team, S(44) if side == "p1" else W - S(44), S(372), side, room)
        credits = _num(vals.get("credits"))
        if credits is not None:
            self.put(screen, self.text(tr(f"CRÉDITS {int(credits):02d}", f"CREDITS {int(credits):02d}"), "bold", S(30),
                                       (200, 170, 120), glow=0), cx, S(335), "center", "middle")

    def team(self, eng, side):
        """Équipe King of Fighters dans l'ordre de passage : [(nom, état)], état « done », « now » ou « next »."""
        vals = eng.state.values
        names = ((eng.derived or {}).get(side + "_char") or {}).get("names")
        if not isinstance(names, dict):
            return None
        chars = [vals.get(f"_{side}_ch{i}") for i in range(4)]
        orders = [vals.get(f"_{side}_ord{i}") for i in range(3)]
        lost = _num(vals.get(f"_{side}_lost"))
        if lost is None or any(o is None for o in orders):
            return None
        out = []
        for k, o in enumerate(orders):
            c = chars[int(o)] if 0 <= int(o) < len(chars) else None
            n = names.get(str(c)) if c is not None else None
            if n is None:
                return None
            out.append((n, "done" if k < lost else ("now" if k == lost else "next")))
        return out

    def draw_team(self, screen, team, x, y, side, room):
        size = self.S(30)
        gap = self.S(30)
        while size > self.S(16):
            total = sum(self.text(n, "bold", size, GREY, glow=0)["w"] for n, _ in team) + gap * (len(team) - 1)
            if total <= room:
                break
            size = int(size * 0.9)
        items = team if side == "p1" else list(reversed(team))
        cx = x
        for n, state in items:
            col = AMBER if state == "now" else (DIM if state == "done" else GREY)
            t = self.text(n, "bold", size, col, glow=0)
            if side == "p1":
                self.put(screen, t, cx, y)
                left = cx
                cx += t["w"] + gap
            else:
                self.put(screen, t, cx, y, "right")
                left = cx - t["w"]
                cx -= t["w"] + gap
            if state == "done":
                ly = y + t["h"] // 2
                self.pg.draw.line(screen, (200, 60, 50), (left - 4, ly), (left + t["w"] + 4, ly), max(2, self.S(4)))

    # ------------------------------------------------------------ autres jeux
    def draw_generic(self, screen, eng, vals, logo, now, key):
        W, S = self.W, self.S
        self.draw_logo(screen, logo, W / 2, S(10), S(760), S(150), now)
        p2m = vals.get("p2_mode")
        p2_in = p2m in (1, 2) or (p2m is None and vals.get("score_p2") not in (None, 0))
        if vals.get("score") is not None:
            w = self.put(screen, self.text("P1", "black", S(64), RED), S(40), S(196))
            self._score(screen, eng, "score", S(40) + w + S(30), S(186), "left", S(96))
        if p2_in and vals.get("score_p2") is not None:
            w = self.put(screen, self.text("P2", "black", S(64), RED), W - S(40), S(196), "right")
            self._score(screen, eng, "score_p2", W - S(40) - w - S(30), S(186), "right", S(96))
        elif p2m is not None:
            word, col = self._invite(vals, now)
            self.put(screen, self.text(word, "xbold", S(44), col), W - S(40), S(210), "right")
        chips = []
        if key.startswith("mslug"):
            for wk, ak, label in (("weapon", "ammo", ("ARME", "WEAPON")), ("weapon_p2", "ammo_p2", ("ARME J2", "WEAPON P2"))):
                wv = vals.get(wk)
                if wv is None or (wk.endswith("_p2") and not p2_in):
                    continue
                name = tr(*MSLUG_WEAPONS.get(wv, ("ARME", "WEAPON")))
                ammo = vals.get(ak)
                chips.append((tr(*label), name + (f" {ammo}" if ammo and wv != 0 else "")))
        for k, label in CHIPS:
            v = vals.get(k)
            if v is None or (k.endswith("_p2") and not p2_in):       # rien du joueur 2 s'il ne joue pas
                continue
            chips.append((tr(*label), str(v)))
        chips = chips[:6]
        if not chips:
            return
        size = S(40)
        gap = S(60)

        def width(sz):
            return sum(self.text(lab, "bold", sz, CREAM, glow=0)["w"] + S(16) + self.text(val, "black", sz, AMBER)["w"]
                       for lab, val in chips) + gap * (len(chips) - 1)

        while size > S(20) and width(size) > W - S(80):
            size = int(size * 0.9)
        x = (W - width(size)) / 2
        y = S(348)
        for lab, val in chips:
            x += self.put(screen, self.text(lab, "bold", size, CREAM, glow=0), x, y, valign="middle") + S(16)
            x += self.put(screen, self.text(val, "black", size, AMBER), x, y, valign="middle") + gap
