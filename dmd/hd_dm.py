"""The show of a desperation move on the HD screen, as Seb chose it on 9 November 2026 (mockups C and 1, 1.33 test 51).
The name of the move takes the whole marquee for a moment, then flies to the side of the player who does it and stays there
while the hits land, counting them; the bar of the one taking them jolts at each hit, its lost part turning white then red,
a star of impact at its edge and its outline lit red. Two desperation moves at once: no full screen, each name slams onto
its own side, DOUBLE DM ! between them.
/ Le spectacle d'un coup désespéré sur l'écran HD, comme Seb l'a choisi (maquettes C et 1) : le nom du coup prend tout le
fronton un instant, puis file du côté du joueur qui le fait et y reste pendant les coups, en les comptant ; la barre de
celui qui les prend tressaute à chaque coup, sa part perdue blanche puis rouge, une étoile d'impact à son bord et son contour
allumé en rouge. Deux coups désespérés en même temps : pas de plein écran, chaque nom claque de son côté, DOUBLE DM ! entre
les deux."""
import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

FULL = 0.85          # the name over the whole marquee that long / le nom sur tout le fronton ce temps
FLY = 0.25           # then it flies to its side in that time / puis il file de son côté en ce temps
HOLD = 2.6           # on its side at least that long after it started / de son côté au moins ce temps après le début
AFTER = 0.9          # and that long after the last hit / et ce temps après le dernier coup
LONGEST = 7.0        # at the latest / au plus tard
FADE = 0.35
JOLT = 0.25          # the bar hit jolts that long / la barre touchée tressaute ce temps
WHITE = 0.09         # the part just lost white that long, then red / la part perdue blanche ce temps, puis rouge
EDGE = 0.4           # the outline lit red that long / le contour allumé en rouge ce temps
STAR = 0.2           # the star of impact that long / l'étoile d'impact ce temps
DOUBLE = 1.4         # DOUBLE DM ! shown that long / DOUBLE DM ! affiché ce temps
GOLD_TOP, GOLD_BOT, GOLD_GLOW = (255, 252, 222), (255, 140, 10), (255, 100, 0)
SDM_TOP, SDM_BOT, SDM_GLOW = (255, 238, 150), (232, 36, 20), (255, 30, 0)


def _ease(k):
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 3


class DMShow:
    """Owned by the fight scene: start() when the panel tells a DM ! or an SDM ! of a human, hit() at each health lost,
    bar() for the drawing of each health bar, draw() over the scene. / Tenu par la scène de combat."""

    def __init__(self, fight):
        self.f = fight
        self.hd, self.pg, self.s = fight.hd, fight.pg, fight.s
        self.W, self.H = fight.W, fight.H
        self.imgs = {}
        self.reset()

    def reset(self):
        self.on = {}                 # side -> the move shown / le coup affiché
        self.hits = {}               # victim -> (t, old, new) the last hit taken in a move / le dernier coup pris
        self.double_t = -99.0

    def log(self, fr, en):
        log = getattr(self.hd, "log", None)
        if callable(log):
            from .i18n import tr
            log(tr(fr, en))

    # ------------------------------------------------------------------ what happens / ce qui se passe
    def start(self, side, move, fighter, sdm, now):
        other = "p2" if side == "p1" else "p1"
        od = self.on.get(other)
        double = od is not None and now < self.end(od)
        self.on[side] = {"t": now, "move": move or "", "fighter": fighter or "", "sdm": bool(sdm), "last": now, "n": 0,
                         "full": not double, "fly": None, "ko": None}
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

    def _star(self, r):
        key = ("star", r)
        img = self.imgs.get(key)
        if img is None:
            size = int(r * 3.4) + 8
            c = size / 2
            im = Image.new("RGBA", (size, size), (255, 236, 160, 0))
            m = Image.new("L", (size, size), 0)
            d = ImageDraw.Draw(m)
            rng = random.Random(r)
            pts = []
            for i in range(24):
                ang = i * math.tau / 24
                rr = r * (1.0 if i % 2 == 0 else 0.32) * rng.uniform(0.75, 1.2)
                pts.append((c + math.cos(ang) * rr * 1.5, c + math.sin(ang) * rr * 0.62))
            d.polygon(pts, fill=255)
            soft = m.filter(ImageFilter.GaussianBlur(max(2, r * 0.12)))
            im.putalpha(ImageChops.lighter(m, soft))
            core = Image.new("RGBA", (size, size), (255, 255, 255, 0))
            cm = Image.new("L", (size, size), 0)
            ImageDraw.Draw(cm).ellipse((c - r * 0.3, c - r * 0.22, c + r * 0.3, c + r * 0.22), fill=255)
            core.putalpha(cm.filter(ImageFilter.GaussianBlur(max(1, r * 0.06))))
            im.alpha_composite(core)
            img = self.imgs[key] = self.hd._surf(im)
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
            surf.set_alpha(None)

    # ------------------------------------------------------------------ drawing / dessin
    def side_x(self, side):
        x, y, w, h = self.f.geom()[side]
        return x + w * (0.54 if side == "p1" else 0.46), w

    def draw(self, screen, now):
        """Over the scene, under the banners (K.O., WIN). / Par-dessus la scène, sous les bandeaux."""
        if not self.on:
            return
        hd, S = self.hd, self.hd.S
        W = self.W
        # the bar hit: its outline lit red, the star at its edge / la barre touchée : son contour rouge, l'étoile au bord
        for victim, h in self.hits.items():
            dt = now - h[0]
            if 0 <= dt < EDGE:
                lv = int(round(6 * (1 - dt / EDGE)))
                if lv > 0:
                    x, y, w, hh = self.f.geom()[victim]
                    pad = int(40 * self.s)
                    screen.blit(self.f._danger_img(victim, lv), (x - pad, y - pad), special_flags=self.pg.BLEND_RGB_ADD)
            if 0 <= dt < STAR:
                x, y, w, hh = self.f.geom()[victim]
                f = max(0.0, min(1.0, h[2] / 100.0))
                ex = x + w * (1 - f) if victim == "p1" else x + w * f
                dmg = max(0.0, h[1] - h[2])
                r = int((42 + dmg * 7) * self.s * (0.6 + 0.4 * _ease(dt / 0.08)))
                r = max(8, r // 4 * 4)
                self._blit(screen, {"surf": self._star(r)}, ex, y + hh / 2, alpha=1 - dt / STAR)
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
            r2 = rays.copy()
            lv = 0.9
            r2.fill((int(255 * lv),) * 3, special_flags=self.pg.BLEND_RGB_MULT)
            screen.blit(r2, (int(W / 2 - r2.get_width() / 2), int(self.H / 2 - r2.get_height() / 2)),
                        special_flags=self.pg.BLEND_RGB_ADD)
            cap = (d["fighter"] + "  —  " if d["fighter"] else "") + ("SUPER DESPERATION MOVE" if d["sdm"] else "DESPERATION MOVE")
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
            plate.set_alpha(None)
        self._blit(screen, img, cx, cy, scale=sc, alpha=a)
        if k >= 1:
            tag = ("SUPER DESPERATION MOVE" if d["sdm"] else "DESPERATION MOVE") + (f"  ·  {d['n']} HITS" if d["n"] >= 2 else "")
            if d["fighter"] and self.running("p2" if side == "p1" else "p1", now):   # two at once: whose is whose
                tag = d["fighter"] + "  ·  " + tag                                     # deux à la fois : à qui
            col = (255, 214, 200) if d["sdm"] else (255, 240, 220)
            hd.put(screen, hd.text(tag, "black", S(24), col, glow=0.7, outline=(40, 10, 0), stroke=max(2, S(3))), sx, S(72),
                   "center", "middle", alpha=a)
