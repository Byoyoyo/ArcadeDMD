"""The show of a desperation move on the HD screen, as chosen on 9 November 2026 (mockups C and 1, 1.33 test 51).
The name of the move takes the whole marquee for a moment, then flies to the side of the player who does it and stays there
while the hits land, counting them; the bar of the one taking them jolts at each hit, its lost part turning white then red,
its outline lit red, and at its edge the spark of the hit with pieces of the bar flying off (mockup B, test 55). Two
desperation moves at once: no full screen, each name slams onto its own side, DOUBLE DM ! between them.
/ Le spectacle d'un coup désespéré sur l'écran HD, comme choisi (maquettes C et 1) : le nom du coup prend tout le
fronton un instant, puis file du côté du joueur qui le fait et y reste pendant les coups, en les comptant ; la barre de
celui qui les prend tressaute à chaque coup, sa part perdue blanche puis rouge, son contour allumé en rouge, et à son bord
l'étincelle du coup avec des morceaux de la barre qui volent (maquette B, test 55). Deux coups désespérés en même temps :
pas de plein écran, chaque nom claque de son côté, DOUBLE DM ! entre les deux."""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

FULL = 0.85          # the name over the whole marquee that long / le nom sur tout le fronton ce temps
FLY = 0.25           # then it flies to its side in that time / puis il file de son côté en ce temps
HOLD = 2.6           # on its side at least that long after it started / de son côté au moins ce temps après le début
AFTER = 0.9          # and that long after the last hit / et ce temps après le dernier coup
LONGEST = 7.0        # at the latest / au plus tard
FADE = 0.35
JOLT = 0.25          # the bar hit jolts that long / la barre touchée tressaute ce temps
WHITE = 0.09         # the part just lost white that long, then red / la part perdue blanche ce temps, puis rouge
EDGE = 0.4           # the outline lit red that long / le contour allumé en rouge ce temps
SPARK = 0.22         # the spark of a hit that long / l'étincelle d'un coup ce temps
SPARK_STEPS = 12     # drawn beforehand in that many pictures / dessinée d'avance en autant d'images
SPARK_R = 150        # at that size, then scaled to the hit / à cette taille, puis à celle du coup
SPARK_MAX = 200      # the biggest a hit makes it / la plus grosse qu'un coup la fait
CHIPS = 0.85         # pieces of the bar fly that long / des morceaux de la barre volent ce temps
CHIP_COLS = ((255, 236, 140), (255, 255, 255), (255, 200, 60), (230, 40, 30))
DOUBLE = 1.4         # DOUBLE DM ! shown that long / DOUBLE DM ! affiché ce temps
GOLD_TOP, GOLD_BOT, GOLD_GLOW = (255, 252, 222), (255, 140, 10), (255, 100, 0)
SDM_TOP, SDM_BOT, SDM_GLOW = (255, 238, 150), (232, 36, 20), (255, 30, 0)


def _ease(k):
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 3


def spark_picture(seed, r, k):
    """One picture of the spark of a hit, k from 0 (the hit) to 1 (gone): yellow and orange spikes round a blue-white
    heart, stretched sideways, breaking into little sparks. An own drawing in the spirit of the games' hit sparks, chosen on
    9 November (mockup B). / Une image de l'étincelle d'un coup : des pointes jaunes et orange autour d'un cœur
    bleuté, étirées en largeur, qui éclatent en petites étincelles. Un dessin à nous, dans l'esprit des étincelles du jeu."""
    rng = random.Random(seed)
    size = int(r * 3.2)
    c = size / 2
    rot = rng.uniform(0, math.tau)
    spikes = [(rot + i * math.tau / 13 + rng.uniform(-0.15, 0.15), rng.uniform(0.5, 1.0)) for i in range(13)]
    grow = 0.55 + 0.6 * min(1.0, k / 0.22)
    thin = max(0.25, 1.0 - max(0.0, k - 0.22) * 1.1)
    fade = 1.0 if k < 0.45 else max(0.0, 1 - (k - 0.45) / 0.55)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    def star(scale, inner, width, col, alpha):
        pts = []
        for ang, ln in spikes:
            L = r * ln * grow * scale
            a0, a1 = ang - width, ang + width
            pts.append((c + math.cos(a0) * r * inner * scale * 1.35, c + math.sin(a0) * r * inner * scale * 0.8))
            pts.append((c + math.cos(ang) * L * 1.35, c + math.sin(ang) * L * 0.8))
            pts.append((c + math.cos(a1) * r * inner * scale * 1.35, c + math.sin(a1) * r * inner * scale * 0.8))
        lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon(pts, fill=col + (int(255 * alpha),))
        return lay

    half = max(1, size // 2)                       # the glow: a mask blurred at half size, quicker / le halo, plus vite
    m = Image.new("L", (half, half), 0)
    pts = []
    for ang, ln in spikes:
        L, w = r * ln * grow * 1.05, 0.22 * thin
        for a, rr in ((ang - w, r * 0.48 * 1.05), (ang, L), (ang + w, r * 0.48 * 1.05)):
            pts.append(((c + math.cos(a) * rr * 1.35) / 2, (c + math.sin(a) * rr * 0.8) / 2))
    ImageDraw.Draw(m).polygon(pts, fill=int(255 * 0.9 * fade))
    glow = Image.new("RGBA", (size, size), (255, 120, 20, 0))
    glow.putalpha(m.filter(ImageFilter.GaussianBlur(max(1, r * 0.05))).resize((size, size), Image.BILINEAR))
    img.alpha_composite(glow)
    img.alpha_composite(star(1.0, 0.46, 0.19 * thin, (255, 132, 24), fade))
    img.alpha_composite(star(0.78, 0.42, 0.17 * thin, (255, 222, 70), fade))
    img.alpha_composite(star(0.50, 0.36, 0.15 * thin, (255, 255, 236), fade))
    if k < 0.4:                                    # the blue-white heart of the hit / le cœur bleuté du coup
        cr = r * 0.32 * (1.0 - k)
        m = int(cr * 1.35 + 3 * max(1, r * 0.04)) + 2                     # only round the heart / juste autour du cœur
        x0, y0 = int(c) - m, int(c) - m
        core = Image.new("RGBA", (2 * m, 2 * m), (0, 0, 0, 0))
        ImageDraw.Draw(core).ellipse((c - x0 - cr * 1.35, c - y0 - cr * 0.8, c - x0 + cr * 1.35, c - y0 + cr * 0.8),
                                     fill=(190, 228, 255, int(255 * (1 - k / 0.4))))
        img.alpha_composite(core.filter(ImageFilter.GaussianBlur(max(1, r * 0.04))), (x0, y0))
    if k > 0.3:                                    # it breaks into little sparks / il éclate en petites étincelles
        d = ImageDraw.Draw(img)
        for i in range(8):
            ang = rng.uniform(0, math.tau)
            dist = r * (0.7 + 1.1 * (k - 0.3))
            x, y = c + math.cos(ang) * dist * 1.35, c + math.sin(ang) * dist * 0.8
            x2, y2 = c + math.cos(ang) * (dist - r * 0.25) * 1.35, c + math.sin(ang) * (dist - r * 0.25) * 0.8
            d.line([(x2, y2), (x, y)], fill=(255, 230, 120, int(255 * fade)), width=max(2, int(r * 0.05)))
    return img


class DMShow:
    """Owned by the fight scene: start() when the panel tells a DM ! or an SDM ! of a human, hit() at each health lost,
    bar() for the drawing of each health bar, draw() over the scene. / Tenu par la scène de combat."""

    def __init__(self, fight):
        self.f = fight
        self.hd, self.pg, self.s = fight.hd, fight.pg, fight.s
        self.W, self.H = fight.W, fight.H
        self.imgs = {}
        self.sparks_todo = []        # the pictures of the spark still to draw beforehand / les images de l'étincelle à faire
        self.reset()

    def reset(self):
        self.todo = []               # the names of the moves to draw before they come / les noms à dessiner avant
        self.on = {}                 # side -> the move shown / le coup affiché
        self.hits = {}               # victim -> (t, old, new) the last hit taken in a move / le dernier coup pris
        self.double_t = -99.0

    def log(self, fr, en):
        log = getattr(self.hd, "log", None)
        if callable(log):
            from .i18n import tr
            log(tr(fr, en))

    # ------------------------------------------------------------------ what happens / ce qui se passe
    def start(self, side, move, fighter, sdm, now, kind=None):
        """kind: the name the game gives its supers, in place of DESPERATION MOVE (X-Men: HYPER X, 1.36). / le nom que le
        jeu donne à ses supers."""
        other = "p2" if side == "p1" else "p1"
        od = self.on.get(other)
        double = od is not None and now < self.end(od)
        self.on[side] = {"t": now, "move": move or "", "fighter": fighter or "", "sdm": bool(sdm), "last": now, "n": 0,
                         "full": not double, "fly": None, "ko": None, "kind": kind}
        if double:
            self.double_t = now
            if od["full"] and now - od["t"] < FULL:             # the first one leaves the full screen at once / tout de suite
                od["fly"] = now
            self.f.fx.flash((255, 255, 255), 0.35, 0.12)
        else:
            self.f.fx.flash((255, 255, 255), 0.8, 0.12)
        self.f.fx.shake(6, 0.3)
        self.log(f"Combat, {side.upper()} {'SDM' if sdm else 'DM'} à l'écran : {move}" + (" (double)" if double else ""),
                 f"Fight, {side.upper()} {'SDM' if sdm else 'DM'} on screen: {move}" + (" (double)" if double else ""))

    @staticmethod
    def _kind(d):
        """"" when the title already says it (HYPER COMBO, 1.36). / vide quand le titre le dit déjà."""
        if d.get("kind") is not None:
            return d["kind"]
        return "SUPER DESPERATION MOVE" if d["sdm"] else "DESPERATION MOVE"

    def upgrade(self, side, now):
        """The move found to be an SDM a moment later (2002: the flag, then the stock in MAX). / Un SDM finalement."""
        d = self.on.get(side)
        if d is not None and not d["sdm"]:
            d["sdm"] = True

    def hit(self, victim, old, new, now):
        """Health lost by victim: counted for the move of the other side if it runs. True when it was one of its hits.
        / De la vie perdue : comptée pour le coup de l'autre côté s'il est en cours."""
        attacker = "p2" if victim == "p1" else "p1"
        d = self.on.get(attacker)
        if d is None or now >= self.end(d) or now < d["t"]:
            return False
        d["n"] += 1
        d["last"] = now
        self.hits[victim] = (now, old, new)
        return True

    def ko(self, now):
        """A K.O.: the names go, the K.O. and WIN take the screen. / Un K.O. : les noms s'en vont."""
        for d in self.on.values():
            if d["ko"] is None and now < self.end(d):
                d["ko"] = now

    def end(self, d):
        e = min(d["t"] + LONGEST, max(d["t"] + HOLD, d["last"] + AFTER))
        if d["ko"] is not None:
            e = min(e, d["ko"] + 0.15)
        return e

    def running(self, side, now):
        d = self.on.get(side)
        return d is not None and d["t"] <= now < self.end(d) + FADE

    # ------------------------------------------------------------------ the health bar / la barre de vie
    def bar(self, side, now):
        """How to draw the health bar of side: None, or {"dx", "dy", "red", "white": (from, to) or None, "edge": 0 to 1}.
        / Comment dessiner la barre de vie de ce côté."""
        attacker = "p2" if side == "p1" else "p1"
        d = self.on.get(attacker)
        h = self.hits.get(side)
        if d is None or now > self.end(d) + 0.8:
            return None
        out = {"dx": 0, "dy": 0, "red": True, "white": None, "edge": 0.0}
        if h is not None and 0 <= now - h[0]:
            dt = now - h[0]
            dmg = max(0.0, h[1] - h[2])
            if dt < JOLT:
                amp = (6 + dmg * 1.6) * (1 - dt / JOLT) * self.s
                out["dx"] = int(amp * math.cos(dt * 90))
                out["dy"] = int(amp * 0.4 * math.sin(dt * 70))
            if dt < WHITE:
                out["white"] = (h[2] / 100.0, h[1] / 100.0)
            if dt < EDGE:
                out["edge"] = 1 - dt / EDGE
        return out

    # ------------------------------------------------------------------ pictures / images
    def _title(self, text, size, sdm):
        """The name of the move: a gradient in its letters, a dark outline, a glow. / Le nom du coup en dégradé."""
        key = ("t", text, size, sdm)
        img = self.imgs.get(key)
        if img is not None:
            return img
        f = self.hd.font("logo", size)
        l, t, r, b = f.getbbox(text) if text else (0, 0, 1, 1)
        stroke = max(2, int(size * 0.05))
        pad = int(size * 0.35) + stroke
        w, h = max(1, r - l) + 2 * pad, max(1, b - t) + 2 * pad
        org = (pad - l, pad - t)
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).text(org, text, font=f, fill=255)
        outer = Image.new("L", (w, h), 0)
        ImageDraw.Draw(outer).text(org, text, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
        wide = Image.new("L", (w, h), 0)
        ImageDraw.Draw(wide).text(org, text, font=f, fill=255, stroke_width=stroke * 3, stroke_fill=255)
        top, bot, glow = (SDM_TOP, SDM_BOT, SDM_GLOW) if sdm else (GOLD_TOP, GOLD_BOT, GOLD_GLOW)
        out = Image.new("RGBA", (w, h), glow + (0,))
        out.putalpha(wide.filter(ImageFilter.GaussianBlur(max(3, size * 0.16))).point(lambda v: int(v * 0.9)))
        dark = Image.new("RGBA", (w, h), (24, 8, 0, 0))
        dark.putalpha(outer)
        out.alpha_composite(dark)
        grad = Image.new("RGBA", (w, h))
        gd = ImageDraw.Draw(grad)
        y0, y1 = pad, h - pad
        for y in range(h):
            k = max(0.0, min(1.0, (y - y0) / max(1, y1 - y0)))
            gd.line([(0, y), (w, y)], fill=tuple(int(a + (c - a) * k) for a, c in zip(top, bot)) + (255,))
        grad.putalpha(mask)
        out.alpha_composite(grad)
        img = {"surf": self.hd._surf(out), "w": r - l, "h": b - t}
        self.imgs[key] = img
        return img

    def _fit(self, text, size, room):
        f = self.hd.font("logo", size)
        while size > self.hd.S(40) and f.getlength(text) > room:
            size -= max(1, self.hd.S(3))
            f = self.hd.font("logo", size)
        return size

    def _plate(self, w, h):
        """A soft dark plate under a name on its side (the fight's own n HITS hidden). / Une plaque sombre et douce."""
        key = ("plate", w, h)
        img = self.imgs.get(key)
        if img is None:
            pad = int(30 * self.s)
            m = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
            ImageDraw.Draw(m).rounded_rectangle((pad, pad, pad + w, pad + h), int(40 * self.s), fill=235)
            m = m.filter(ImageFilter.GaussianBlur(14 * self.s))
            im = Image.new("RGBA", m.size, (6, 8, 14, 0))
            im.putalpha(m)
            img = self.imgs[key] = self.hd._surf(im)
        return img

    def _spark(self, seed, i):
        """Picture i of spark seed, cropped: (surface, x and y of its heart). / Une image de l'étincelle, rognée."""
        key = ("spark", seed, i)
        img = self.imgs.get(key)
        if img is None:
            im = spark_picture(seed, int(SPARK_R * self.s), i / SPARK_STEPS)
            c = im.size[0] / 2
            box = im.getbbox() or (0, 0, 1, 1)
            img = self.imgs[key] = (self.hd._surf(im.crop(box)), c - box[0], c - box[1])
        return img

    def _dark(self):
        img = self.imgs.get("dark")
        if img is None or img.get_size() != (self.W, self.H):
            img = self.pg.Surface((self.W, self.H)).convert()
            img.fill((0, 0, 0))
            self.imgs["dark"] = img
        return img

    def _blit(self, screen, img, cx, cy, scale=1.0, alpha=1.0):
        surf = img["surf"]
        if abs(scale - 1.0) > 0.01:
            scale = round(scale * 50) / 50.0
            key = ("sc", id(surf), scale)
            s2 = self.imgs.get(key)
            if s2 is None:
                s2 = self.pg.transform.smoothscale(surf, (max(1, int(surf.get_width() * scale)), max(1, int(surf.get_height() * scale))))
                self.imgs[key] = s2
                if len(self.imgs) > 260:                          # the scaled ones go first / les mises à l'échelle d'abord
                    for k in [k for k in self.imgs if isinstance(k, tuple) and k[0] == "sc"][:120]:
                        del self.imgs[k]
            surf = s2
        if alpha < 0.999:
            surf.set_alpha(int(255 * max(0.0, alpha)))
        screen.blit(surf, (int(cx - surf.get_width() / 2), int(cy - surf.get_height() / 2)))
        if alpha < 0.999:
            surf.set_alpha(255)                                   # not None: None makes a picture with transparent
            # pixels opaque for good, the glow became an orange rectangle on the cabinet the second time a move came
            # (1.33 test 53) / pas None : None rend opaque pour de bon une image transparente par endroits

    # ------------------------------------------------------------------ drawing / dessin
    def side_x(self, side):
        x, y, w, h = self.f.geom()[side]
        return x + w * (0.54 if side == "p1" else 0.46), w

    def prepare(self, names):
        """The names of the moves a human can do now: drawn a frame at a time beforehand, so a move starts without a
        wait. / Les noms des coups qu'un humain peut faire : dessinés d'avance, une image à la fois."""
        for n in names:
            if n and ("t", n) not in self.imgs and n not in self.todo:
                self.todo.append(n)
        if names and not self.sparks_todo and ("spark", 0, 0) not in self.imgs:   # then the spark / puis l'étincelle
            self.sparks_todo = [(seed, i) for seed in (0, 1) for i in range(SPARK_STEPS)]

    def _warm(self):
        n = self.todo.pop(0)
        S = self.hd.S
        self._title(n, self._fit(n, S(168), self.W - S(160)), False)
        w = self.side_x("p1")[1]
        self._title(n, self._fit(n, S(96), w - S(40)), False)
        self._plate(int(w - S(20)), S(92))
        self.imgs[("t", n)] = True

    def draw(self, screen, now):
        """Over the scene, under the banners (K.O., WIN). / Par-dessus la scène, sous les bandeaux."""
        if (self.todo or self.sparks_todo) and not any(now < self.end(d) + FADE for d in self.on.values()):
            if self.todo:                                         # one a frame, never during a move / une par image
                self._warm()
            else:
                self._spark(*self.sparks_todo.pop(0))
        if not self.on:
            return
        hd, S = self.hd, self.hd.S
        W = self.W
        # the bar hit: its outline lit red / la barre touchée : son contour rouge
        for victim, h in self.hits.items():
            dt = now - h[0]
            if 0 <= dt < EDGE:
                lv = int(round(6 * (1 - dt / EDGE)))
                if lv > 0:
                    x, y, w, hh = self.f.geom()[victim]
                    pad = int(40 * self.s)
                    screen.blit(self.f._danger_img(victim, lv), (x - pad, y - pad), special_flags=self.pg.BLEND_RGB_ADD)
        full = [(s, d) for s, d in self.on.items() if d["full"] and now - d["t"] < FULL and d["fly"] is None
                and now < self.end(d) and d["ko"] is None]
        if full:                                                  # the whole marquee / tout le fronton
            side, d = full[0]
            dt = now - d["t"]
            dark = self._dark()
            dark.set_alpha(int(255 * 0.78))
            screen.blit(dark, (0, 0))
            e = _ease(dt / 0.15)
            bar_h = int(S(70) * e)
            if bar_h > 0:
                screen.fill((0, 0, 0), (0, 0, W, bar_h))
                screen.fill((0, 0, 0), (0, self.H - bar_h, W, bar_h))
            rays = self.f._rays()
            r2 = self.imgs.get(("rays", id(rays)))
            if r2 is None:                                        # made once / fait une fois
                r2 = rays.copy()
                r2.fill((int(255 * 0.9),) * 3, special_flags=self.pg.BLEND_RGB_MULT)
                self.imgs[("rays", id(rays))] = r2
            screen.blit(r2, (int(W / 2 - r2.get_width() / 2), int(self.H / 2 - r2.get_height() / 2)),
                        special_flags=self.pg.BLEND_RGB_ADD)
            cap = "  —  ".join(x for x in (d["fighter"], self._kind(d)) if x)
            hd.put(screen, hd.text(cap, "black", S(30), (255, 236, 210), glow=0.6, outline=(40, 10, 0), stroke=max(2, S(3))),
                   W / 2, S(132), "center", "middle")
            size = self._fit(d["move"], S(168), W - S(160))
            sc = 1.0 + 0.4 * (1 - _ease(dt / 0.2))
            self._blit(screen, self._title(d["move"], size, d["sdm"]), W / 2, S(248), scale=sc)
        for side, d in self.on.items():
            if full and full[0][0] == side:
                continue
            self._draw_side(screen, side, d, now)
        k = now - self.double_t
        if 0 <= k < DOUBLE:                                       # DOUBLE DM ! between the two / entre les deux
            a = 1.0 if k < DOUBLE - 0.3 else (DOUBLE - k) / 0.3
            hd.put(screen, hd.text("DOUBLE DM !", "stencil", S(38), (255, 214, 120), glow=0.9), W / 2, S(60), "center", "middle",
                   scale=1 + 0.5 * (1 - _ease(k / 0.15)), alpha=a)
        self._impacts(screen, now)

    def _impacts(self, screen, now):
        """At the edge of the bar hit, the spark of the hit, bigger when it hurts more, and pieces of the bar flying off,
        over everything (the choice B, 9 November). / Au bord de la barre touchée, l'étincelle du coup, plus grosse quand
        il fait mal, et des morceaux de la barre qui volent, par-dessus tout (choix B)."""
        pg, s = self.pg, self.s
        for victim, h in self.hits.items():
            dt = now - h[0]
            if not 0 <= dt < max(SPARK, CHIPS):
                continue
            x, y, w, hh = self.f.geom()[victim]
            f = max(0.0, min(1.0, h[2] / 100.0))
            ex = x + w * (1 - f) if victim == "p1" else x + w * f
            dmg = max(0.0, h[1] - h[2])
            seed = int(round(h[0] * 1000))
            if dt < SPARK:
                surf, ox, oy = self._spark(seed % 2, min(SPARK_STEPS - 1, int(dt / SPARK * SPARK_STEPS)))
                sc = min(70 + dmg * 9, SPARK_MAX) / SPARK_R
                if abs(sc - 1) > 0.02:
                    surf = pg.transform.smoothscale(surf, (max(1, int(surf.get_width() * sc)), max(1, int(surf.get_height() * sc))))
                    ox, oy = ox * sc, oy * sc
                fx, fy = bool(seed & 2), bool(seed & 4)           # eight looks from two drawings / huit allures
                if fx or fy:
                    surf = pg.transform.flip(surf, fx, fy)
                    ox = surf.get_width() - ox if fx else ox
                    oy = surf.get_height() - oy if fy else oy
                screen.blit(surf, (int(ex - ox), int(y + hh / 2 - oy)))
            if dt < CHIPS:                                        # pieces of the bar fly off / des morceaux volent
                rng = random.Random(seed + 7)
                k = dt / CHIPS
                f0 = max(0.0, min(1.0, h[1] / 100.0))
                a = max(0, int(255 * (1 - k)))
                big = int(20 * s) + 3
                chip = self.imgs.get("chip")
                if chip is None or chip.get_width() < 2 * big:
                    chip = self.imgs["chip"] = pg.Surface((2 * big, 2 * big), pg.SRCALPHA)
                for i in range(min(60, int(16 + dmg * 3))):
                    u = rng.uniform(f, f0)
                    px = x + w * (1 - u) if victim == "p1" else x + w * u
                    py = y + rng.uniform(0.2, 0.8) * hh
                    vx = rng.uniform(-380, 380) * s
                    vy = -rng.uniform(200, 560) * s
                    qx, qy = px + vx * dt, py + vy * dt + 1300 * s * dt * dt
                    sz = rng.uniform(9, 20) * s
                    col = rng.choice(CHIP_COLS)
                    ang = rng.uniform(0, math.tau) + dt * rng.uniform(-14, 14)
                    pts = [(sz + math.cos(ang + j * math.tau / 4) * sz * (1.0 if j % 2 else 0.5),
                            sz + math.sin(ang + j * math.tau / 4) * sz * (1.0 if j % 2 else 0.5)) for j in range(4)]
                    cs = int(sz * 2) + 2
                    chip.fill((0, 0, 0, 0), (0, 0, cs, cs))
                    pg.draw.polygon(chip, col + (a,), pts)
                    screen.blit(chip, (int(qx - sz), int(qy - sz)), (0, 0, cs, cs))

    def _draw_side(self, screen, side, d, now):
        hd, S = self.hd, self.hd.S
        end = self.end(d)
        if now >= end + FADE or now < d["t"]:
            return
        a = 1.0 if now < end else 1 - (now - end) / FADE
        sx, w = self.side_x(side)
        size = self._fit(d["move"], S(96), w - S(40))
        img = self._title(d["move"], size, d["sdm"])
        plate = self._plate(int(w - S(20)), S(92))
        if d["full"]:
            t_fly = d["fly"] if d["fly"] is not None else d["t"] + FULL
            k = _ease((now - t_fly) / (0.2 if d["fly"] is not None else FLY))
            cx = self.W / 2 + (sx - self.W / 2) * k
            cy = S(248) + (S(126) - S(248)) * k
            big = self._fit(d["move"], S(168), self.W - S(160)) / max(1, size)
            sc = 1 + (big - 1) * (1 - k)
            if k < 1:
                dark = self._dark()
                dark.set_alpha(int(255 * 0.78 * (1 - k) * a))
                screen.blit(dark, (0, 0))
        else:                                                     # slammed onto its side (two at once) / plaqué de son côté
            k = 1.0
            cx, cy = sx, S(126)
            sc = 1 + 0.15 * (1 - _ease((now - d["t"]) / 0.18))
        if k >= 1:
            plate.set_alpha(int(255 * a))
            screen.blit(plate, (int(sx - plate.get_width() / 2), int(S(126) - plate.get_height() / 2)))
            plate.set_alpha(255)
        self._blit(screen, img, cx, cy, scale=sc, alpha=a)
        if k >= 1:
            tag = "  ·  ".join(x for x in (self._kind(d), f"{d['n']} HITS" if d["n"] >= 2 else "") if x)
            if d["fighter"] and (self.running("p2" if side == "p1" else "p1", now) or not tag):   # two at once: whose
                tag = "  ·  ".join(x for x in (d["fighter"], tag) if x)                         # is whose / à qui
            col = (255, 214, 200) if d["sdm"] else (255, 240, 220)
            if tag:
                hd.put(screen, hd.text(tag, "black", S(24), col, glow=0.7, outline=(40, 10, 0), stroke=max(2, S(3))), sx, S(72),
                       "center", "middle", alpha=a)
