"""Fighting game effects on the HD screen.

Stage backdrop (city at night, temple, harbor, ruins, arena, desert, snow, jungle...) that follows the game's
stage when its address is known ("backdrop" picks the theme, "stage" numbers it), with a wipe and the place name.
Sparks and shards on every hit, combo counter, first attack, super move (the screen darkens, light rays),
danger when health is low (red heartbeat), exploding K.O., DOUBLE K.O., TIME UP, PERFECT, confetti for the
winner, next King of Fighters fighter, "FIGHT !". Everything comes from the health bars, the timer, the
fighters' names and the stage values.

Effets des jeux de combat sur l'écran HD.

Décor du stage (ville la nuit, temple, port, ruines, arène, désert, neige, jungle), qui change avec le stage
du jeu quand son adresse est connue (valeur « stage »), avec un volet et le nom du stage.
Étincelles et éclats à chaque coup, compteur de combo, premier coup du round, super coup (l'écran s'assombrit,
rayons de lumière), danger quand il reste peu de vie (battement de cœur rouge), K.O. qui explose, DOUBLE K.O.,
TIME UP, PERFECT, confettis pour le vainqueur, combattant suivant des King of Fighters, « FIGHT ! ».

Tout se déduit des barres de vie (health, health_p2), du chrono, du nom des combattants et du stage.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFilter

from . import hd_stages
from .hd_bg import Backdrop
from .hd_fx import FX, Particle
from .hd_themes15 import CPS_STAGES
from .i18n import tr

GOLD = (255, 214, 120)
WHITE = (255, 255, 255)
RED = (255, 64, 44)
CREAM = (238, 228, 208)
CONFETTI = ((255, 80, 80), (255, 210, 60), (80, 220, 255), (120, 255, 140), (255, 120, 220), (255, 255, 255))

# place shown under STAGE n, for each theme ("fight_city" uses "city") / nom du lieu sous STAGE n
STAGE_NAMES = {"arena": ("ARÈNE", "ARENA"), "city": ("VILLE", "CITY"), "temple": ("TEMPLE", "TEMPLE"),
               "harbor": ("PORT", "HARBOR"), "ruins": ("RUINES", "RUINS"), "desert": ("DÉSERT", "DESERT"),
               "snow": ("MONTAGNE", "MOUNTAIN"), "jungle": ("JUNGLE", "JUNGLE"), "base": ("BASE", "BASE"),
               "city_war": ("CHAMP DE BATAILLE", "BATTLEFIELD"), "castle": ("CHÂTEAU", "CASTLE"), "market": ("MARCHÉ", "MARKET"),
               "factory": ("ACIÉRIE", "STEEL MILL"), "gothic": ("MANOIR", "MANOR"), "palace": ("PALAIS", "PALACE"),
               "thai": ("TEMPLE D'OR", "GOLDEN TEMPLE"), "lab": ("LABORATOIRE", "LABORATORY")}


def stage_name(theme):
    fr, en = STAGE_NAMES.get(theme) or STAGE_NAMES.get(theme.replace("fight_", ""), ("", ""))
    return tr(fr, en)


def _n(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def shard_img(color, s):
    w, h = max(6, int(16 * s)), max(4, int(9 * s))
    k = 4
    img = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(w * k * 0.2, 0), (w * k, 0), (w * k * 0.8, h * k), (0, h * k)], fill=color + (255,))
    d.line([(w * k * 0.22, 2 * k), (w * k * 0.95, 2 * k)], fill=(255, 255, 255, 200), width=k)
    return img.resize((w, h), Image.LANCZOS)


def confetti_img(color, s):
    w, h = max(4, int(12 * s)), max(3, int(7 * s))
    img = Image.new("RGBA", (w, h), color + (255,))
    ImageDraw.Draw(img).line([(0, 0), (w, 0)], fill=(255, 255, 255, 160), width=1)
    return img


def stable_index(text, n):
    return sum(ord(c) * (i + 1) for i, c in enumerate(text or "")) % max(1, n)


class FightFX:
    def __init__(self, hd, rng=None):
        self.hd, self.pg, self.s = hd, hd.pg, hd.s
        self.W, self.H = hd.W, hd.H
        self.rng = rng or random.Random()
        self.fx = FX(hd, random.Random(self.rng.random()))
        self.bd = Backdrop(hd, "arena", random.Random(self.rng.random()), threaded=False)
        self.bd.static = True
        self.buf = None
        self.dark = None
        self.key = None
        self._reset(-99.0)
        for name, col in (("shard_g", (48, 240, 160)), ("shard_y", (255, 214, 60)), ("shard_r", (255, 70, 50))):
            self.fx.sp.register(name, shard_img(col, self.s))
        for i, col in enumerate(CONFETTI):
            self.fx.sp.register(f"conf{i}", confetti_img(col, self.s))
        self.danger_imgs = {}
        self.idle = False
        self.rays = None
        self._rays()                                                  # préparés d'avance : pas d'à-coup au premier super
        self.warm = self._warm_list()

    def _warm_list(self):
        """Textes et halos préparés petit à petit pendant les moments calmes (pas d'à-coup au premier coup)."""
        hd, S, sp, s = self.hd, self.hd.S, self.fx.sp, self.s
        out = []
        for text, size in (("FIGHT !", 112), ("PERFECT !", 112), ("TIME UP", 112), ("DOUBLE K.O.", 112), ("WIN !", 72)):
            out.append((hd.text, (text, "stencil", S(size), GOLD if "K.O." not in text else RED, 0.8 if size > 100 else 0.6)))
        for n in range(2, 13):
            out.append((hd.text, (f"{n} HITS", "stencil", S(58 + min(20, n * 3)), GOLD, 0.6)))
        out.append((hd.text, (tr("PREMIER COUP", "FIRST ATTACK"), "stencil", S(44), (255, 240, 200), 0.6)))
        out.append((hd.text, (tr("ENTRE EN SCÈNE", "NEXT FIGHTER"), "bold", S(26), GOLD, 0)))
        for side in ("p1", "p2"):
            for lv in range(1, 7):
                out.append((self._danger_img, (side, lv)))
        for color, rmax in (((255, 245, 220), 200), ((255, 130, 50), 320), ((255, 236, 190), 128), ((255, 150, 50), 160),
                            ((255, 210, 120), 160), ((255, 110, 40), 160)):
            for r in (16, 20, 25, 32, 40, 50, 64, 80, 100, 128, 160, 200, 256, 320):
                if r > rmax:
                    break
                for lv in range(12, 0, -1):
                    out.append((sp.glow, (r * s, color, lv, 0.8 if color == (255, 245, 220) else 0.35)))
        return out

    def _warm_step(self, budget):
        import time as _t
        end = _t.perf_counter() + budget
        while self.warm and _t.perf_counter() < end:
            fn, args = self.warm.pop(0)
            try:
                fn(*args)
            except Exception:
                self.warm = []

    def _reset(self, now):
        self.prev = {}
        self.combo = {"p1": [0, -99.0], "p2": [0, -99.0]}
        self.combo_txt = {"p1": None, "p2": None}
        self.ko_t = -99.0
        self.fight_t = -99.0
        self.first = False
        self.stage_v = None
        self.stage_t = -99.0
        self.stage_changed = set()
        self.stage_label = None
        self.chars = {"p1": None, "p2": None}
        self.next_t = {"p1": -99.0, "p2": -99.0}
        self.next_name = {"p1": "", "p2": ""}
        self.win = None              # [côté, moment, PERFECT ?, déjà fêté ?]
        self.banner = None           # (texte, couleur, début, durée)
        self.super_t = -99.0
        self.super_xy = (0, 0)
        self.health = {"p1": None, "p2": None}
        self.prev_time = None

    def stages(self, game):
        """Themes of the game's stages, indexed by the "backdrop" value; an unknown theme becomes the arena, so that the
        places keep their index. / Thèmes des décors du jeu ; un thème inconnu devient l'arène."""
        lst = ((game or {}).get("hd") or {}).get("stages")
        if lst:
            return [s if s in hd_stages.hd_bg.BUILDERS else "arena" for s in lst]
        return list(hd_stages.FIGHT_STAGES) + (list(CPS_STAGES) if (game or {}).get("cps") else [])   # Capcom: their stages too

    @staticmethod
    def place(game, pick, theme):
        """Place shown under STAGE n: the game's own ("hd" "places", [french, english] by backdrop value, the countries of
        Street Fighter II for example), else the theme's. / Le lieu du jeu (pays de Street Fighter II...), sinon celui du thème."""
        places = ((game or {}).get("hd") or {}).get("places")
        if isinstance(places, list) and places:
            p = places[int(pick) % len(places)]
            if isinstance(p, list) and len(p) == 2 and all(isinstance(x, str) for x in p):
                return tr(p[0], p[1])
            if isinstance(p, str):
                return p
        return stage_name(theme)

    def geom(self):
        """Place des barres de vie, comme dans HDRenderer.draw_fight."""
        S, W = self.hd.S, self.W
        cx = W / 2
        bw = int(cx - S(160) - S(40))
        return {"p1": (S(40), S(176), bw, S(50)), "p2": (int(cx + S(160)), S(176), bw, S(50)), "cx": cx}

    # ------------------------------------------------------------ ce qui a changé
    def update(self, vals, now, key, game=None, idle=False):
        """idle: nobody plays, the game's own demo runs behind the attract screen. Its fights change the health
        bars, but no spark, banner or K.O. is shown for them. / Personne ne joue : pas d'effet pour la démo du jeu."""
        stages = self.stages(game)
        if key != self.key:
            self.key = key
            self._reset(now)
            self.bd.set_theme(stages[stable_index(key, len(stages))], now, wipe=0)
            self.bd.prebuild(stages)                                  # les autres stages se préparent en arrière-plan
        self.fx.update(now)
        self.idle = idle
        if idle:
            self._idle(vals, stages)
            return
        # "stage": match number in the run, from 0 (cheat "Select Current Round"), shown as STAGE n.
        # "backdrop": backdrop of the fight (cheat "Select Backdrop"), picks the theme in the game's "hd" list.
        stage = _n(vals.get("stage"))
        back = _n(vals.get("backdrop"))
        pick = back if back is not None else stage
        sig = (stage, back)
        if pick is not None and sig != self.stage_v:
            theme = stages[int(pick) % len(stages)]
            place = self.place(game, pick, theme)
            label = (f"STAGE {int(stage) + 1}", place) if stage is not None else (place, "")
            changed = {i for i in (0, 1) if self.stage_v is None or sig[i] != self.stage_v[i]}
            if self.stage_v is None:
                self.bd.set_theme(theme, now, wipe=0)
            elif now - self.stage_t < 1.5 and not (changed & self.stage_changed):
                if theme != self.bd.theme:               # the other value of the same change (round, then backdrop)
                    self.bd.set_theme(theme, now)
                self.stage_label = label
                self.stage_changed |= changed
            else:
                self.bd.set_theme(theme, now)
                self.stage_t = now
                self.stage_label = label
                self.stage_changed = changed
            self.stage_v = sig
        for side in ("p1", "p2"):                                     # combattant suivant (équipes des KOF)
            name = vals.get(side + "_char")
            if isinstance(name, str) and name:
                old = self.chars.get(side)
                if old and name != old and now - self.stage_t > 2.5:     # pas au changement de stage (nouvelle équipe)
                    self.next_t[side] = now
                    self.next_name[side] = name
                self.chars[side] = name
        h1, h2 = _n(vals.get("health")), _n(vals.get("health_p2"))
        self.health = {"p1": h1, "p2": h2}
        t = _n(vals.get("time"))
        for side, h in (("p1", h1), ("p2", h2)):
            old = self.prev.get(side)
            if h is not None and old is not None:
                if h < old:
                    self._hit(side, old, h, now)
                elif old <= 0 < h and now - self.fight_t > 2.0:     # combattant suivant ou nouveau round
                    self._fight(now)
        if h1 is not None and h2 is not None and self.prev.get("p1") is None and h1 >= 100 and h2 >= 100 and (t is None or t >= 50):
            self._fight(now)                                          # début de round vu en arrivant (ou barres qui apparaissent)
        if t is not None and self.prev_time is not None and t <= 0 < self.prev_time and (h1 or 0) > 0 and (h2 or 0) > 0:
            self.banner = ("TIME UP", GOLD, now, 1.6)                 # chrono à zéro sans K.O.
            if h1 != h2:
                self.win = ["p1" if h1 > h2 else "p2", now + 1.0, False, False]
        self.prev_time = t
        if self.win is not None and not self.win[3] and now >= self.win[1]:
            self._celebrate(*self.win[:3])
            self.win[3] = True
        self.prev["p1"], self.prev["p2"] = h1, h2

    def _idle(self, vals, stages):
        """Attract screen: the values are only followed (backdrop of the demo's stage, last health, names),
        so that nothing goes off when the game starts."""
        stage, back = _n(vals.get("stage")), _n(vals.get("backdrop"))
        pick = back if back is not None else stage
        if pick is not None and (stage, back) != self.stage_v:
            theme = stages[int(pick) % len(stages)]
            if self.stage_v is None:
                self.bd.set_theme(theme, self.fx.now, wipe=0)
            else:
                self.bd.set_theme(theme, self.fx.now)                   # the demo changes stage: wipe, no banner
            self.stage_v = (stage, back)
        self.stage_label = None
        self.banner = None
        self.win = None
        for side in ("p1", "p2"):
            name = vals.get(side + "_char")
            if isinstance(name, str) and name:
                self.chars[side] = name
        h1, h2 = _n(vals.get("health")), _n(vals.get("health_p2"))
        self.health = {"p1": h1, "p2": h2}
        self.prev["p1"], self.prev["p2"] = h1, h2
        self.prev_time = _n(vals.get("time"))

    def _hit(self, victim, old, new, now):
        fx, rng, S = self.fx, self.rng, self.hd.S
        g = self.geom()
        x, y, w, h = g[victim]
        d = old - new
        f = max(0.0, new / 100.0)
        ex = x + w * (1 - f) if victim == "p1" else x + w * f      # bord de la vie qui vient de partir
        ey = y + h / 2
        fx.glow(ex, ey, 16, 50 + d * 3, (255, 245, 220), 0.22, "front", 1.0, 0.0, hot=0.8)
        fx.sparks(ex, ey, int(8 + d * 1.4), (255, 230, 150), (250, 900), (190, 350), (0.25, 0.6), 1100, "front", 3, 34)
        col = "shard_g" if f > 0.5 else ("shard_y" if f > 0.25 else "shard_r")
        for _ in range(int(2 + d / 4)):                             # éclats de la barre qui tombent
            fx.obj(col, ex + rng.uniform(-10, 10) * self.s, ey, rng.uniform(-260, 260), -rng.uniform(250, 520), gravity=1600,
                   vrot=rng.uniform(-700, 700), life=0.9, rot=rng.uniform(0, 360))
        fx.shake(min(9.0, 1.5 + d * 0.35), 0.25)
        self.bd.excite(0.05 + d * 0.025)
        attacker = "p2" if victim == "p1" else "p1"
        ax, ay, aw, _ = g[attacker]
        if not self.first and now - self.fight_t < 60:              # premier coup du round
            self.first = True
            old_t = self.combo_txt.get(attacker)
            if old_t is not None:
                old_t.dead = True
            self.combo_txt[attacker] = fx.text(tr("PREMIER COUP", "FIRST ATTACK"), ax + aw * 0.5, S(132), (255, 240, 200), 44,
                                               life=1.2, rise=10)
        if d >= 25:                                                 # super coup : l'écran s'assombrit, rayons de lumière
            self.super_t = now
            self.super_xy = (ex, ey)
            fx.shake(12, 0.5)
            fx.flash((255, 255, 255), 0.25, 0.15)
            self.bd.excite(1.2)
        if d >= 15:                                                 # gros coup : onde de choc
            r = fx.add(Particle("ring", ex, ey, now, 0.4, "front"))
            r.r0, r.r1, r.col, r.a0, r.a1, r.data = 10 * self.s, 170 * self.s, (255, 235, 200), 0.9, 0.0, 6 * self.s
            fx.flash((255, 240, 220), 0.1, 0.12)
            self.bd.excite(0.5)
        c = self.combo[attacker]
        c[0] = c[0] + 1 if now - c[1] < 0.7 else 1
        c[1] = now
        if c[0] >= 2:
            old_t = self.combo_txt.get(attacker)
            if old_t is not None:
                old_t.dead = True
            self.combo_txt[attacker] = fx.text(f"{c[0]} HITS", ax + aw * 0.5, S(132), GOLD, 58 + min(20, c[0] * 3), life=1.1, rise=15)
        if new <= 0:
            self.ko_t = now
            fx.explosion(x + w / 2, ey, 1.25, layer_back=False)
            fx.flash((255, 220, 200), 0.25, 0.25)
            fx.shake(14, 0.6)
            self.bd.excite(2.5)
            other = self.health.get(attacker)
            if other is not None and other <= 0:
                self.banner = ("DOUBLE K.O.", RED, now + 0.5, 1.6)
            else:
                perfect = other is not None and other >= 99
                self.win = [attacker, now + 0.8, perfect, False]

    def _celebrate(self, side, t, perfect):
        """Le vainqueur : confettis au-dessus de son côté, WIN, PERFECT si aucun coup reçu."""
        fx, rng, S = self.fx, self.rng, self.hd.S
        x, y, w, h = self.geom()[side]
        for i in range(70):
            p = fx.obj(f"conf{rng.randint(0, len(CONFETTI) - 1)}", x + rng.uniform(0, w), -rng.uniform(10, 120) * self.s,
                       rng.uniform(-60, 60), rng.uniform(80, 200), gravity=60, vrot=rng.uniform(-500, 500), life=rng.uniform(2.6, 3.6),
                       rot=rng.uniform(0, 360))
            p.wob = rng.uniform(40, 90) * self.s
            p.drag = 0.4
        old_t = self.combo_txt.get(side)
        if old_t is not None:
            old_t.dead = True
        fx.text("WIN !", x + w / 2, S(140), GOLD, 72, life=1.8, rise=12)
        self.bd.excite(1.5)
        if perfect:
            self.banner = ("PERFECT !", GOLD, self.fx.now + 0.2, 1.6)

    def _fight(self, now):
        # pas en même temps que le bandeau du stage ou le nom du combattant suivant
        busy = max([self.stage_t + 1.95 if now - self.stage_t < 2.0 else -99.0] +
                   [t + 1.75 for t in self.next_t.values() if -0.1 <= now - t < 1.75 or 0 < t - now < 2.5])
        self.fight_t = max(now, busy)
        self.first = False
        self.win = None
        self.bd.excite(0.8)
        cx, cy = self.W / 2, self.hd.S(240)
        r = self.fx.add(Particle("ring", cx, cy, now + 0.12, 0.5, "front"))
        r.r0, r.r1, r.col, r.a0, r.a1, r.data = 30 * self.s, 520 * self.s, (255, 220, 150), 0.8, 0.0, 8 * self.s

    def ko_scale(self, now):
        k = (now - self.ko_t) / 0.22
        if k >= 1 or k < 0:
            return 1.0
        return 2.6 - 1.6 * (1 - (1 - k) ** 3)

    # ------------------------------------------------------------ dessin
    def begin(self, screen, now):
        ox, oy = self.fx.offset()
        target = screen
        if ox or oy:
            if self.buf is None or self.buf.get_size() != screen.get_size():
                self.buf = self.pg.Surface(screen.get_size()).convert()
            target = self.buf
        self.bd.draw(target, now, 0.0)
        k = (now - self.super_t) / 0.5
        if 0 <= k < 1:                                               # super coup : décor assombri, rayons
            if self.dark is None:
                self.dark = self.pg.Surface(screen.get_size()).convert()
                self.dark.fill((0, 0, 0))
            self.dark.set_alpha(int(170 * (1 - k)))
            target.blit(self.dark, (0, 0))
            rays = self._rays()
            lv = 1 - k
            r2 = rays.copy()
            r2.fill((int(255 * lv),) * 3, special_flags=self.pg.BLEND_RGB_MULT)
            x, y = self.super_xy
            target.blit(r2, (int(x - r2.get_width() / 2), int(y - r2.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
        self.fx.draw(target, "back")
        return target

    def _rays(self):
        if self.rays is None:
            size = int(900 * self.s)
            m = Image.new("L", (size, size), 0)
            d = ImageDraw.Draw(m)
            rng = random.Random(9)
            c = size / 2
            for i in range(44):
                a = i * math.tau / 44 + rng.uniform(-0.03, 0.03)
                w = rng.uniform(0.008, 0.02)
                d.polygon([(c, c), (c + math.cos(a - w) * c, c + math.sin(a - w) * c), (c + math.cos(a + w) * c, c + math.sin(a + w) * c)],
                          fill=rng.randint(90, 200))
            fade = Image.radial_gradient("L").resize((size, size)).point(lambda v: max(0, 255 - v * 255 // 181))
            from PIL import ImageChops
            m = ImageChops.multiply(m, fade).filter(ImageFilter.GaussianBlur(2 * self.s))
            self.rays = self.hd._surf(Image.merge("RGB", (m, m.point(lambda v: v * 9 // 10), m.point(lambda v: v * 7 // 10))))
        return self.rays

    def end(self, screen, target, now):
        if not getattr(self, "idle", False):                         # no health bar on the attract screen
            self._danger(target, now)
        self.fx.draw(target, "front")
        self._next_fighter(target, now)
        self._banners(target, now)
        self.fx.draw_flash(target)
        if target is not screen:
            ox, oy = self.fx.offset()
            screen.fill((0, 0, 0))
            screen.blit(target, (ox, oy))
        if self.warm and len(self.fx.parts) < 60:
            self._warm_step(0.004)

    def _danger_img(self, side, level):
        key = (side, level)
        s = self.danger_imgs.get(key)
        if s is None:
            x, y, w, h = self.geom()[side]
            pad = int(40 * self.s)
            m = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
            ImageDraw.Draw(m).rounded_rectangle([pad - 6, pad - 6, pad + w + 6, pad + h + 6], radius=int(12 * self.s), outline=255,
                                                width=max(3, int(8 * self.s)))
            m = m.filter(ImageFilter.GaussianBlur(10 * self.s))
            k = level / 6
            s = self.danger_imgs[key] = self.hd._surf(Image.merge("RGB", (m.point(lambda v: int(v * k)), m.point(lambda v: int(v * 0.12 * k)),
                                                                          m.point(lambda v: int(v * 0.08 * k)))))
        return s

    def _danger(self, screen, now):
        """Moins de 20 % de vie : la barre bat en rouge comme un cœur."""
        p = (now % 0.9) / 0.9
        env = math.exp(-((p - 0.05) / 0.06) ** 2) + 0.7 * math.exp(-((p - 0.25) / 0.06) ** 2)
        lvl = int(round(min(1.0, env) * 6))
        if lvl <= 0:
            return
        for side, h in self.health.items():
            if h is None or not (0 < h <= 20):
                continue
            x, y, w, hh = self.geom()[side]
            img = self._danger_img(side, lvl)
            pad = int(40 * self.s)
            screen.blit(img, (x - pad, y - pad), special_flags=self.pg.BLEND_RGB_ADD)

    def _slam(self, screen, text, color, t0, dur, now, size=112, y=240):
        k = now - t0
        if k < 0 or k > dur:
            return
        hd, S, W = self.hd, self.hd.S, self.W
        start = max(1.2, min(2.4, W * 0.96 / max(1, hd.text_width(text, "stencil", S(size)))))
        scale = start - (start - 1.0) * min(1.0, k / 0.16)
        alpha = 1.0 if k < dur - 0.25 else max(0.0, (dur - k) / 0.25)
        bar = self.pg.Surface((W, S(130))).convert()
        bar.fill((0, 0, 0))
        bar.set_alpha(int(215 * alpha))
        screen.blit(bar, (0, S(y - 65)))
        hd.put(screen, hd.text(text, "stencil", S(size), color, glow=0.8), W / 2, S(y), "center", "middle", scale=scale, alpha=alpha)

    def _banners(self, screen, now):
        if self.stage_label is not None and 0 <= now - self.stage_t - 0.3 <= 1.6:
            k = now - self.stage_t - 0.3
            title, place = self.stage_label
            self._slam(screen, title, CREAM, self.stage_t + 0.3, 1.6, now, size=96, y=228)
            a = 1.0 if k < 1.35 else max(0.0, (1.6 - k) / 0.25)
            if k > 0.12 and place:
                self.hd.put(screen, self.hd.text(place, "stencil", self.hd.S(36), GOLD, glow=0.5), self.W / 2, self.hd.S(282),
                            "center", "middle", alpha=a)
        self._slam(screen, "FIGHT !", GOLD, self.fight_t + 0.1, 1.15, now)
        if self.banner is not None:
            text, col, t0, dur = self.banner
            self._slam(screen, text, col, t0, dur, now)

    def _next_fighter(self, screen, now):
        """Combattant suivant : son nom arrive de son côté de l'écran."""
        hd, S, W = self.hd, self.hd.S, self.W
        for side in ("p1", "p2"):
            k = now - self.next_t[side]
            if k < 0 or k > 1.7:
                continue
            slide = min(1.0, k / 0.25) if k < 1.45 else max(0.0, (1.7 - k) / 0.25)
            e = 1 - (1 - slide) ** 3
            bw = int(W * 0.46)
            x = -bw + bw * e if side == "p1" else W - bw * e
            band = self.pg.Surface((bw, S(120))).convert()
            band.fill((8, 6, 14))
            band.set_alpha(225)
            screen.blit(band, (int(x), S(236)))
            self.pg.draw.rect(screen, GOLD, (int(x), S(236), bw, max(2, S(3))))
            self.pg.draw.rect(screen, GOLD, (int(x), S(353), bw, max(2, S(3))))
            name = self.next_name[side]
            size = hd.fit_size(name, "stencil", S(84), bw - S(80), S(30))
            cx = x + bw / 2
            hd.put(screen, hd.text(tr("ENTRE EN SCÈNE", "NEXT FIGHTER"), "bold", S(26), GOLD, glow=0), cx, S(258), "center", "middle")
            hd.put(screen, hd.text(name, "stencil", size, RED, glow=0.6), cx, S(306), "center", "middle")
