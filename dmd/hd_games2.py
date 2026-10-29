"""HD scenes of the second batch of Neo Geo games done one by one (1.18): Pulstar, Magical Drop III, Super Sidekicks 3,
The Ultimate 11, Sengoku 3. Same idea as the first batch (hd_games): each game has its own animated backdrop and
reacts to the values read in its memory. Everything is drawn by the program, no image or character comes from a game.

Scènes HD du deuxième lot de jeux Neo Geo faits un par un (1.18). Même principe que le premier lot : chaque jeu a son
décor animé et réagit aux valeurs lues dans sa mémoire. Tout est dessiné par le programme, aucune image ni aucun
personnage tiré d'un jeu.
"""

import colorsys
import math

from .hd_fight import CONFETTI, confetti_img          # (hd_fight brings the temple of hd_stages into hd_bg.BUILDERS)
from .hd_games import (BTN_A, BTN_B, CREAM, GOLD, GREY, P1C, P2C, RED, WHITE, BlazingStarScene, GameScene, _clamp, _mix, _n, draw_img,
                       drone_draw)
from .hd_themes2 import PULSTAR, SKIN, pitch_geom, pitch_x, pitch_y    # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr

DARK = (20, 16, 34)


def _poly(d, pts, W, H, fill, outline=None, width=0):
    d.polygon([(x * W, y * H) for x, y in pts], fill=fill, outline=outline, width=width)


# ============================================================================ Pulstar
def pul_ship_draw(accent, body=(212, 220, 236), dark=(24, 28, 50)):
    """Long-nosed fighter seen from the side, a big engine at the back, nose to the right.
    / Chasseur au long nez vu de profil, gros réacteur à l'arrière."""
    def fn(d, W, H):
        ow = max(2, int(H * 0.035))
        line = dark + (255,)
        _poly(d, [(0.24, 0.36), (0.1, 0.02), (0.2, 0.02), (0.46, 0.36)], W, H, accent + (255,), line, ow)        # dérive
        _poly(d, [(0.0, 0.28), (0.2, 0.22), (0.28, 0.5), (0.2, 0.78), (0.0, 0.72)], W, H, (74, 80, 106, 255), line, ow)
        hull = [(0.14, 0.34), (0.48, 0.28), (0.76, 0.38), (1.0, 0.52), (0.76, 0.6), (0.48, 0.7), (0.14, 0.66)]
        _poly(d, hull, W, H, body + (255,))
        _poly(d, [(0.15, 0.52), (0.99, 0.52), (0.76, 0.6), (0.48, 0.69), (0.15, 0.65)], W, H, _mix(body, (70, 80, 120), 0.45) + (255,))
        d.line([(0.18 * W, 0.47 * H), (0.84 * W, 0.5 * H)], fill=accent + (255,), width=max(2, int(H * 0.05)))
        d.ellipse([0.5 * W, 0.32 * H, 0.74 * W, 0.47 * H], fill=(255, 170, 70, 255), outline=line, width=ow)         # verrière
        d.ellipse([0.55 * W, 0.35 * H, 0.64 * W, 0.39 * H], fill=(255, 240, 210, 255))
        d.line([(x * W, y * H) for x, y in hull + [hull[0]]], fill=line, width=ow, joint="curve")
        _poly(d, [(0.4, 0.62), (0.27, 0.98), (0.37, 0.98), (0.58, 0.62)], W, H, _mix(accent, (0, 0, 0), 0.28) + (255,), line, ow)
        d.ellipse([0.02 * W, 0.4 * H, 0.1 * W, 0.6 * H], fill=(140, 225, 255, 255))                                   # tuyère
    return fn


def pod_draw(color):
    """Round pod with a ring, lit from the top left. / Module rond avec un anneau."""
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=_mix(color, (0, 0, 0), 0.5) + (255,))
        for i in range(10):
            k = i / 10
            r = (W / 2) * (0.92 - k * 0.6)
            cx, cy = W / 2 - W * 0.12 * k, H / 2 - H * 0.12 * k
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_mix(color, WHITE, k * 0.6) + (255,))
        d.ellipse([W * 0.22, H * 0.16, W * 0.44, H * 0.34], fill=(255, 255, 255, 220))
        d.arc([W * 0.02, H * 0.3, W * 0.98, H * 0.72], 0, 180, fill=(36, 36, 60, 255), width=max(2, int(W * 0.09)))
        d.ellipse([0, 0, W - 1, H - 1], outline=(30, 30, 50, 255), width=max(1, int(W * 0.05)))
    return fn


def shield_draw(d, W, H):
    """Front protection: a crescent of light in front of the ship. / Protection avant : un croissant de lumière."""
    d.ellipse([-W * 0.9, 0, W - 1, H - 1], fill=(130, 220, 255, 170))
    d.ellipse([-W * 1.3, H * 0.1, W * 0.6, H * 0.9], fill=(0, 0, 0, 0))
    d.arc([-W * 0.9, 0, W - 1, H - 1], -80, 80, fill=(230, 250, 255, 255), width=max(2, int(W * 0.08)))


def spore_draw(color):
    """Spiky living spore with one eye. / Spore vivante à piquants, un œil."""
    def fn(d, W, H):
        cx, cy, r = W / 2, H / 2, W * 0.3
        dark = _mix(color, (0, 0, 0), 0.6) + (255,)
        for i in range(9):
            a = i * math.tau / 9 + 0.2
            d.polygon([(cx + math.cos(a - 0.24) * r * 0.9, cy + math.sin(a - 0.24) * r * 0.9),
                       (cx + math.cos(a) * W * 0.49, cy + math.sin(a) * H * 0.49),
                       (cx + math.cos(a + 0.24) * r * 0.9, cy + math.sin(a + 0.24) * r * 0.9)], fill=dark)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (255,), outline=dark, width=max(2, int(W * 0.04)))
        d.ellipse([cx - r * 0.7, cy - r * 0.8, cx + r * 0.1, cy - r * 0.2], fill=_mix(color, WHITE, 0.45) + (255,))
        d.ellipse([cx - r * 0.46, cy - r * 0.46, cx + r * 0.46, cy + r * 0.46], fill=(255, 222, 96, 255), outline=dark,
                  width=max(1, int(W * 0.03)))
        d.ellipse([cx - r * 0.16, cy - r * 0.32, cx + r * 0.16, cy + r * 0.32], fill=(30, 10, 10, 255))
    return fn


class PulstarScene(BlazingStarScene):
    """The ship and its pods follow the player's stick, the charge glows on the nose and leaves as a beam, the
    backdrop follows the stage. / Le vaisseau, ses modules, la charge qui part en rayon, le décor suit le stage."""
    THEME = "pul_earth"
    SHADE = (110, 130)
    PILLS = True                                               # the fire world is bright: dark pills under the top texts
    BANNERS = GameScene.BANNERS + tuple((f"STAGE {n}", GOLD) for n in range(1, 8)) + (("FINAL STAGE", RED), ("STAGE FINAL", RED))
    ACC = {"p1": (255, 150, 60), "p2": (80, 190, 255)}
    MECA = (1, 4, 6)                                           # stages with machines, the others with spores
    SPORE = {2: (60, 170, 160), 3: (220, 100, 50), 5: (120, 180, 60), 7: (180, 70, 150), 8: (180, 70, 150), 9: (210, 60, 80)}

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.world = None
        self.charge = 0.0                                      # charge shown, follows the value smoothly
        self.pods = 0

    def ship_surf(self, side):
        return self.img("pship_" + side, self.S(180), self.S(76), pul_ship_draw(self.ACC[side]))

    def always(self, vals, now):
        st = _n(vals.get("stage"))
        if st is None:
            return
        name = PULSTAR.get(int(st), "pul_earth")
        if name == self.bd.theme:
            return
        if name != self.world:                                         # the new world is built in the background
            self.world = name
            self.bd.prebuild([name])
        if self.bd.ready(name):
            old = self.bd.theme
            self.bd.set_theme(name, now, wipe=0 if self.bd.last is None else 1.1)
            with self.bd.lock:                                         # only one world kept in memory
                self.bd.raw.pop(old, None)
            self.bd.built.pop(old, None)

    def move(self, vals, now, idle):
        sp = _n(vals.get("speed"))
        return 0.15 if idle else 0.5 + 0.08 * (3 if sp is None else _clamp(sp, 0, 7))

    def pod_xy(self, bit, x, y, now):
        S = self.S
        if bit == 1:
            return x + S(112), y
        d = -1 if bit == 2 else 1
        return x - S(14) + S(8) * math.sin(now * 3 + d), y + d * S(58) + S(4) * math.sin(now * 4.2 + d)

    def restart(self, vals, now):
        super().restart(vals, now)
        self.charge = 0.0

    def update(self, vals, now):
        self.pods = int(_n(vals.get("pods")) or 0) & 7
        super().update(vals, now)                                      # ships, lives, score, enemies (as Blazing Star)
        fx, S = self.fx, self.S
        alive = self.ships["p1"]["in"] and now - self.ships["p1"]["t_dead"] > 1.2
        ch = self.changed(vals, "charge")
        if ch and alive and ch[0] >= 100 and ch[1] < ch[0] - 60:     # the button is let go: the charged shot leaves
            self._release("p1", ch[0] / 255.0, now)
        ch = self.changed(vals, "pods")
        if ch and alive:
            old, new = int(ch[0]) & 7, int(ch[1]) & 7
            x, y = self.pos("p1", now)
            for bit in (1, 2, 4):
                px, py = self.pod_xy(bit, x, y, now)
                if new & bit and not old & bit:
                    fx.glow(px, py, 16, 110, (120, 220, 255), 0.4, "front", 1.0, 0.0)
                    fx.sparks(px, py, 14, (160, 230, 255), (200, 520), (0, 360), (0.25, 0.5), 0, "front", 3, 20)
                elif old & bit and not new & bit:
                    fx.small_blast(px, py, 0.6, "front")
            gained = new & ~old
            if gained:
                self.popup(tr("BOUCLIER", "SHIELD") if gained == 1 else "POD +", x, max(S(176), y - S(74)), (140, 220, 255), 36)
        ch = self.changed(vals, "stage")
        if ch and ch[1] >= 1:
            n = int(ch[1])
            name = vals.get("stage_name") if isinstance(vals.get("stage_name"), str) else None
            if n >= 8:
                self.slam(tr("STAGE FINAL", "FINAL STAGE"), RED, now, 2.2, sub=name)
            else:
                self.slam(f"STAGE {n}", GOLD, now, 2.0, sub=name)
            self.boost = (3.0, now + 1.8)
            fx.flash((140, 200, 255), 0.25, 0.4)

    def _fire(self, side, pw, now):
        super()._fire(side, 0, now)
        if side != "p1" or not self.pods & 6:
            return
        x, y = self.pos(side, now)
        for bit, d in ((2, -1), (4, 1)):                               # the pods fire too
            if self.pods & bit:
                px, py = self.pod_xy(bit, x, y, now)
                self.fx.tracer(px + self.S(22), py, self.W + self.S(60), py + d * self.S(30), speed=3200, color=(120, 220, 255),
                               width=3, length=90, impact=False)

    def _release(self, side, level, now):
        """Charged shot: a thick beam, the enemies in its way blow up. / Tir chargé : un gros rayon."""
        fx, S = self.fx, self.S
        x, y = self.pos(side, now)
        mx = x + S(96)
        level = _clamp(level, 0.4, 1.0)
        fx.glow(mx, y, 30, 200 * level, (255, 190, 110), 0.35, "front", 1.0, 0.0, hot=0.7)
        for dy, w, ln, delay in ((0, 26 * level + 8, 560, 0.0), (-S(13), 8, 300, 0.03), (S(13), 8, 300, 0.05)):
            fx.later(delay, fx.tracer, mx, y + dy, self.W + S(300), y + dy, 5200, (255, 214, 150), int(w), int(ln * (0.6 + 0.4 * level)),
                     "front", False)
        fx.shake(3 + 6 * level, 0.25)
        band = S(36 + 50 * level)
        for e in self.enemies:
            if not e.get("dead") and e["x"] > mx and abs(e.get("yy", e["y"]) - y) < band:
                fx.later((e["x"] - mx) / (5200 * self.s), self._boom, e)
        if level > 0.8:
            self.popup(tr("TIR CHARGÉ", "CHARGED SHOT"), x, max(S(176), y - S(74)), (255, 200, 120), 34)

    def enemy_img(self, st):
        S = self.S
        if st in self.MECA or st not in self.SPORE:
            return self.img("drone", S(74), S(50), drone_draw), False
        col = self.SPORE[st]
        return self.img(("spore", col), S(66), S(66), spore_draw(col)), True

    def draw_pods(self, screen, x, y, now):
        S, sp, add = self.S, self.fx.sp, self.pg.BLEND_RGB_ADD
        if self.pods & 1:                                              # front protection
            sx, sy = self.pod_xy(1, x, y, now)
            g = sp.glow(S(50), (80, 170, 255), 5 + 2 * math.sin(now * 6), hot=0.2)
            screen.blit(g, (int(sx - g.get_width() / 2), int(sy - g.get_height() / 2)), special_flags=add)
            sh = self.img("shield", S(44), S(118), shield_draw)
            screen.blit(sh, (int(sx - sh.get_width() / 2), int(sy - sh.get_height() / 2)))
        pod = self.img("pod", S(34), S(34), pod_draw((90, 170, 230)))
        for bit in (2, 4):
            if self.pods & bit:
                px, py = self.pod_xy(bit, x, y, now)
                g = sp.glow(S(28), (120, 210, 255), 6 + 2 * math.sin(now * 8 + bit), hot=0.4)
                screen.blit(g, (int(px - g.get_width() / 2), int(py - g.get_height() / 2)), special_flags=add)
                screen.blit(pod, (int(px - pod.get_width() / 2), int(py - pod.get_height() / 2)))

    def draw_charge(self, screen, vals, x, y, now):
        c = _n(vals.get("charge"))
        if c is None:
            return
        self.charge += (_clamp(c / 255.0) - self.charge) * min(1.0, self.dt * 14)
        k = self.charge
        if k < 0.06:
            return
        S, sp = self.S, self.fx.sp
        nx = x + S(96)
        full = c >= 250
        r = S(8 + 34 * k) + (S(5) * math.sin(now * 30) if full else 0)
        g = sp.glow(r, _mix((255, 140, 50), (255, 240, 200), k), 4 + 7 * k, hot=0.4 + 0.5 * k)
        screen.blit(g, (int(nx - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
        if full:                                                       # full: rings and sparks
            ph = (now * 2.5) % 1.0
            sp.draw_ring(screen, nx, y, S(30) + S(40) * ph, S(5), (255, 214, 150), 0.7 * (1 - ph))
            if self.rng.random() < 0.3:
                self.fx.sparks(nx, y, 1, (255, 220, 160), (150, 420), (0, 360), (0.15, 0.3), 0, "front", 2, 14)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg, dt, sp = self.S, self.W, self.pg, self.dt, self.fx.sp
        add = pg.BLEND_RGB_ADD
        st = int(_n(vals.get("stage")) or 1)
        enemy, organic = self.enemy_img(st)
        keep = []
        for e in self.enemies:                                         # enemies coming from the right
            if e.get("dead"):
                continue
            e["x"] -= e["v"] * dt
            if e["x"] < -S(100):
                continue
            e["yy"] = e["y"] + math.sin(now * 2.4 + e["ph"]) * S(16)
            keep.append(e)
            img = self.rotated(("spore", st), enemy, (now * 40 + e["ph"] * 50) % 360, 6) if organic else enemy
            screen.blit(img, (int(e["x"] - img.get_width() / 2), int(e["yy"] - img.get_height() / 2)))
            ex = e["x"] if organic else e["x"] - S(13)
            g = sp.glow(S(22), (255, 200, 80) if organic else (255, 70, 50), 6 + 3 * math.sin(now * 8 + e["ph"]), hot=0.5)
            screen.blit(g, (int(ex - g.get_width() / 2), int(e["yy"] - g.get_height() / 2)), special_flags=add)
            if now - e["hit"] < 0.06:
                h = sp.glow(S(40), (255, 255, 255), 8, hot=0.6)
                screen.blit(h, (int(e["x"] - h.get_width() / 2), int(e["yy"] - h.get_height() / 2)), special_flags=add)
        self.enemies = keep
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"] or now - P["t_dead"] < 1.2 or now < P["t_spawn"]:
                continue
            if now - P["t_spawn"] < 1.6 and int(now * 14) % 2 == 0:    # blinking after coming back
                continue
            x, y = self.pos(side, now)
            spd = _n(vals.get("speed")) if side == "p1" else None
            spd = 3 if spd is None else _clamp(spd, 0, 7)
            flame = (255, 170, 80) if side == "p2" else (110, 200, 255)
            fl = sp.streak(S(30 + 12 * spd) + S(6) * math.sin(now * 40), S(9), flame, 0, 10)      # the engine: longer when fast
            screen.blit(fl, (int(x - S(84) - fl.get_width()), int(y - fl.get_height() / 2)), special_flags=add)
            g = sp.glow(S(16) + S(3) * math.sin(now * 40), flame, 10, hot=0.8)
            screen.blit(g, (int(x - S(86) - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=add)
            ship = self.rotated("pship_" + side, self.ship_surf(side), _clamp(-P["vy"] * 6, -10, 10))
            screen.blit(ship, (int(x - ship.get_width() / 2), int(y - ship.get_height() / 2)))
            if side == "p1":
                self.draw_pods(screen, x, y, now)
                self.draw_charge(screen, vals, x, y, now)
        self.top_bar(screen, eng, vals, logo, now)
        x0 = S(36)
        c = _n(vals.get("charge"))
        if c is not None and self.p1_in(vals):                         # charge gauge, MAX when full
            full = c >= 250
            self.text(screen, "CHARGE", x0, S(352), 26, CREAM, key="bold", glow=0)
            self.bar(screen, x0 + S(126), S(350), S(220), S(28), c / 255.0, (255, 236, 170) if full else (255, 150, 60), back=(44, 26, 14))
            if full:
                self.text(screen, "MAX", x0 + S(236), S(364), 22, (90, 40, 0), key="black", align="center", valign="middle", glow=0,
                          scale=1 + 0.08 * math.sin(now * 10))
        spd = _n(vals.get("speed"))
        if spd is not None and self.p1_in(vals):                       # speed: seven pips
            sx = x0 + S(420)
            tw = self.text(screen, tr("VITESSE", "SPEED"), sx, S(352), 26, CREAM, key="bold", glow=0)
            for i in range(7):
                on = i < int(spd)
                pg.draw.rect(screen, (110, 200, 255) if on else (30, 44, 60), (int(sx + tw + S(16) + i * S(24)), S(350), S(18), S(28)),
                             border_radius=S(4))
        for side, xx, d in (("p1", x0, 1), ("p2", W - x0, -1)):
            if side == "p2" and not self.p2_in(vals):
                continue
            lives = _n(vals.get("lives" if side == "p1" else "lives_p2"))
            if lives is not None:                                      # lives: small ships
                icon = self.img("plife_" + side, S(60), S(26), pul_ship_draw(self.ACC[side]))
                n = int(lives)
                for i in range(min(7, n)):
                    screen.blit(icon, (int(xx + i * S(66) if d > 0 else xx - (i + 1) * S(66)), S(398)))
                if n > 7:
                    self.text(screen, f"+{n - 7}", xx + d * 7 * S(66), S(400), 28, CREAM, align="left" if d > 0 else "right")
        if st >= 1 and _n(vals.get("stage")) is not None:              # stage and its name
            name = vals.get("stage_name") if isinstance(vals.get("stage_name"), str) else ""
            txt = (tr("STAGE FINAL", "FINAL STAGE") if st >= 8 else f"STAGE {st}") + (f"  ·  {name}" if name else "")
            self.label(screen, txt, W / 2, S(412), 30, GOLD, key="xbold", align="center", alpha=130)


# ============================================================================ Magical Drop III
DROP_RGB = ((255, 76, 84), (70, 210, 104), (84, 140, 255), (255, 212, 64))
ROMAN = ("0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII",
         "XIX", "XX", "XXI", "?", "?")
SYMBOL = ("star", "wand", "moon", "crown", "crown", "key", "heart", "wheel", "flame", "lantern", "wheel", "scales", "hourglass",
          "hourglass", "cup", "flame", "tower", "star", "moon", "sun", "wings", "globe", "mask", "flame")


def drop_draw(color):
    """Shiny round drop. / Goutte ronde et brillante."""
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=_mix(color, (0, 0, 0), 0.5) + (255,))
        for i in range(12):
            k = i / 12
            r = (W / 2) * (0.94 - k * 0.62)
            cx, cy = W / 2 - W * 0.1 * k, H / 2 - H * 0.1 * k
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_mix(color, WHITE, k * 0.45) + (255,))
        d.ellipse([W * 0.24, H * 0.14, W * 0.48, H * 0.32], fill=(255, 255, 255, 230))
        d.ellipse([W * 0.62, H * 0.64, W * 0.74, H * 0.74], fill=(255, 255, 255, 110))
        d.ellipse([0, 0, W - 1, H - 1], outline=_mix(color, (0, 0, 0), 0.7) + (255,), width=max(1, int(W * 0.04)))
    return fn


def jester_draw(color):
    """Jester's cap with three bells: the player's place under the drops. / Bonnet de fou à trois grelots."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(2, int(W * 0.03))
        c2 = _mix(color, (255, 255, 255), 0.35) + (255,)
        _poly(d, [(0.5, 0.66), (0.06, 0.12), (0.34, 0.66)], W, H, color + (255,), dark, ow)
        _poly(d, [(0.5, 0.66), (0.94, 0.12), (0.66, 0.66)], W, H, color + (255,), dark, ow)
        _poly(d, [(0.36, 0.66), (0.5, 0.04), (0.64, 0.66)], W, H, c2, dark, ow)
        d.rounded_rectangle([W * 0.2, H * 0.62, W * 0.8, H * 0.86], radius=W * 0.06, fill=(250, 214, 90, 255), outline=dark, width=ow)
        for x, y in ((0.06, 0.12), (0.94, 0.12), (0.5, 0.04)):
            d.ellipse([(x - 0.07) * W, (y - 0.04) * H, (x + 0.07) * W, (y + 0.1) * H], fill=(255, 226, 100, 255), outline=dark, width=ow)
    return fn


def _symbol(d, kind, cx, cy, r, col, bg):
    """Tarot symbol drawn with simple shapes. / Symbole de tarot en formes simples."""
    c, light = col + (255,), _mix(col, WHITE, 0.55) + (255,)
    w = max(2, int(r * 0.09))
    if kind == "sun":
        for i in range(12):
            a = i * math.tau / 12
            d.polygon([(cx + math.cos(a - 0.13) * r * 0.6, cy + math.sin(a - 0.13) * r * 0.6), (cx + math.cos(a) * r, cy + math.sin(a) * r),
                       (cx + math.cos(a + 0.13) * r * 0.6, cy + math.sin(a + 0.13) * r * 0.6)], fill=c)
        d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=light)
    elif kind == "moon":
        d.ellipse([cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8], fill=light)
        d.ellipse([cx - r * 0.42, cy - r * 0.95, cx + r * 1.0, cy + r * 0.6], fill=bg)
    elif kind == "star":
        pts = []
        for i in range(16):
            a = -math.pi / 2 + i * math.tau / 16
            rr = r if i % 2 == 0 else r * 0.42
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        d.polygon(pts, fill=light)
    elif kind == "crown":
        d.polygon([(cx - r * 0.85, cy + r * 0.45), (cx - r * 0.85, cy - r * 0.5), (cx - r * 0.42, cy), (cx, cy - r * 0.75),
                   (cx + r * 0.42, cy), (cx + r * 0.85, cy - r * 0.5), (cx + r * 0.85, cy + r * 0.45)], fill=c)
        d.rectangle([cx - r * 0.85, cy + r * 0.3, cx + r * 0.85, cy + r * 0.55], fill=light)
        for x in (-0.85, 0.0, 0.85):
            yy = cy - (r * 0.75 if x == 0 else r * 0.5)
            d.ellipse([cx + x * r - r * 0.13, yy - r * 0.13, cx + x * r + r * 0.13, yy + r * 0.13], fill=light)
    elif kind == "heart":
        d.ellipse([cx - r * 0.85, cy - r * 0.6, cx + r * 0.02, cy + r * 0.25], fill=c)
        d.ellipse([cx - r * 0.02, cy - r * 0.6, cx + r * 0.85, cy + r * 0.25], fill=c)
        d.polygon([(cx - r * 0.8, cy - r * 0.05), (cx + r * 0.8, cy - r * 0.05), (cx, cy + r * 0.85)], fill=c)
        d.ellipse([cx - r * 0.55, cy - r * 0.42, cx - r * 0.28, cy - r * 0.18], fill=light)
    elif kind == "wheel":
        d.ellipse([cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85], outline=light, width=w * 2)
        for i in range(8):
            a = i * math.tau / 8
            d.line([(cx, cy), (cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8)], fill=c, width=w)
        d.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2], fill=light)
    elif kind == "flame":
        for k, colr in ((1.0, c), (0.62, light)):
            d.polygon([(cx, cy - r * k), (cx + r * 0.55 * k, cy + r * 0.2 * k), (cx + r * 0.3 * k, cy + r * 0.7 * k),
                       (cx - r * 0.3 * k, cy + r * 0.7 * k), (cx - r * 0.55 * k, cy + r * 0.2 * k)], fill=colr)
    elif kind == "lantern":
        d.rectangle([cx - r * 0.42, cy - r * 0.5, cx + r * 0.42, cy + r * 0.6], fill=c)
        d.rectangle([cx - r * 0.28, cy - r * 0.35, cx + r * 0.28, cy + r * 0.45], fill=light)
        d.polygon([(cx - r * 0.55, cy - r * 0.5), (cx, cy - r * 0.9), (cx + r * 0.55, cy - r * 0.5)], fill=c)
        d.rectangle([cx - r * 0.5, cy + r * 0.6, cx + r * 0.5, cy + r * 0.75], fill=c)
    elif kind == "scales":
        d.line([(cx, cy - r * 0.85), (cx, cy + r * 0.75)], fill=light, width=w)
        d.line([(cx - r * 0.85, cy - r * 0.5), (cx + r * 0.85, cy - r * 0.5)], fill=light, width=w)
        for x in (-0.65, 0.65):
            d.line([(cx + x * r, cy - r * 0.5), (cx + x * r - r * 0.25, cy + r * 0.05)], fill=c, width=max(1, w // 2))
            d.line([(cx + x * r, cy - r * 0.5), (cx + x * r + r * 0.25, cy + r * 0.05)], fill=c, width=max(1, w // 2))
            d.chord([cx + x * r - r * 0.32, cy - r * 0.15, cx + x * r + r * 0.32, cy + r * 0.25], 0, 180, fill=c)
        d.rectangle([cx - r * 0.35, cy + r * 0.72, cx + r * 0.35, cy + r * 0.84], fill=light)
    elif kind == "hourglass":
        d.rectangle([cx - r * 0.6, cy - r * 0.85, cx + r * 0.6, cy - r * 0.72], fill=c)
        d.rectangle([cx - r * 0.6, cy + r * 0.72, cx + r * 0.6, cy + r * 0.85], fill=c)
        d.polygon([(cx - r * 0.48, cy - r * 0.72), (cx + r * 0.48, cy - r * 0.72), (cx, cy)], fill=light)
        d.polygon([(cx - r * 0.48, cy + r * 0.72), (cx + r * 0.48, cy + r * 0.72), (cx, cy)], fill=light)
        d.polygon([(cx - r * 0.3, cy + r * 0.72), (cx + r * 0.3, cy + r * 0.72), (cx, cy + r * 0.3)], fill=c)
    elif kind == "tower":
        d.rectangle([cx - r * 0.38, cy - r * 0.5, cx + r * 0.38, cy + r * 0.85], fill=c)
        for i in range(3):
            x = cx - r * 0.38 + i * r * 0.3
            d.rectangle([x, cy - r * 0.7, x + r * 0.16, cy - r * 0.5], fill=c)
        d.rectangle([cx - r * 0.1, cy + r * 0.4, cx + r * 0.1, cy + r * 0.85], fill=bg)
        d.line([(cx + r * 0.85, cy - r * 0.95), (cx + r * 0.42, cy - r * 0.5), (cx + r * 0.66, cy - r * 0.42), (cx + r * 0.2, cy - r * 0.02)],
               fill=light, width=w)
    elif kind == "cup":
        d.chord([cx - r * 0.7, cy - r * 0.9, cx + r * 0.7, cy + r * 0.3], 0, 180, fill=c)
        d.rectangle([cx - r * 0.7, cy - r * 0.32, cx + r * 0.7, cy - r * 0.26], fill=light)
        d.rectangle([cx - r * 0.09, cy + r * 0.25, cx + r * 0.09, cy + r * 0.66], fill=c)
        d.ellipse([cx - r * 0.45, cy + r * 0.6, cx + r * 0.45, cy + r * 0.82], fill=light)
    elif kind == "wings":
        for sgn in (-1, 1):
            for k in range(4):
                a = math.radians(-60 + k * 22)
                ex, ey = cx + sgn * math.cos(a) * r, cy + math.sin(a) * r * 0.9
                d.line([(cx + sgn * r * 0.1, cy + r * 0.1), (ex, ey)], fill=light if k % 2 else c, width=w * 2)
        d.ellipse([cx - r * 0.16, cy - r * 0.1, cx + r * 0.16, cy + r * 0.3], fill=light)
    elif kind == "globe":
        d.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82], fill=c)
        d.ellipse([cx - r * 0.35, cy - r * 0.82, cx + r * 0.35, cy + r * 0.82], outline=light, width=w)
        d.line([(cx - r * 0.82, cy), (cx + r * 0.82, cy)], fill=light, width=w)
        d.arc([cx - r * 0.82, cy - r * 0.5, cx + r * 0.82, cy + r * 0.2], 200, 340, fill=light, width=max(1, w // 2))
    elif kind == "mask":
        d.polygon([(cx - r * 0.9, cy - r * 0.2), (cx - r * 0.3, cy - r * 0.55), (cx, cy - r * 0.3), (cx + r * 0.3, cy - r * 0.55),
                   (cx + r * 0.9, cy - r * 0.2), (cx + r * 0.5, cy + r * 0.35), (cx, cy + r * 0.2), (cx - r * 0.5, cy + r * 0.35)], fill=c)
        for x in (-0.38, 0.38):
            d.ellipse([cx + x * r - r * 0.17, cy - r * 0.2, cx + x * r + r * 0.17, cy + r * 0.02], fill=bg)
        d.polygon([(cx, cy + r * 0.45), (cx + r * 0.12, cy + r * 0.62), (cx, cy + r * 0.8), (cx - r * 0.12, cy + r * 0.62)], fill=light)
    elif kind == "wand":
        d.line([(cx - r * 0.7, cy + r * 0.8), (cx + r * 0.35, cy - r * 0.3)], fill=c, width=w * 2)
        _symbol(d, "star", cx + r * 0.45, cy - r * 0.42, r * 0.45, col, bg)
    elif kind == "key":
        d.ellipse([cx - r * 0.4, cy - r * 0.9, cx + r * 0.4, cy - r * 0.15], outline=light, width=w * 2)
        d.line([(cx, cy - r * 0.15), (cx, cy + r * 0.85)], fill=light, width=w * 2)
        for y in (0.5, 0.75):
            d.line([(cx, cy + r * y), (cx + r * 0.35, cy + r * y)], fill=c, width=w * 2)


def card_draw(hd, idx, scale):
    """Tarot card: gold border, the roman numeral and a symbol. / Carte de tarot : bord doré, chiffre romain, symbole."""
    hue = (idx * 0.137) % 1.0
    acc = tuple(int(v * 255) for v in colorsys.hsv_to_rgb(hue, 0.55, 1.0))
    bg = (40, 24, 74)

    def fn(d, W, H):
        ow = max(2, int(W * 0.02))
        gold = (236, 196, 100, 255)
        d.rounded_rectangle([0, 0, W - 1, H - 1], radius=W * 0.08, fill=bg + (255,), outline=gold, width=ow * 2)
        d.rounded_rectangle([W * 0.07, H * 0.045, W * 0.93, H * 0.955], radius=W * 0.05, outline=(236, 196, 100, 170), width=ow)
        mid = _mix(acc, bg, 0.62)
        d.ellipse([W * 0.14, H * 0.24, W * 0.86, H * 0.71], fill=mid + (255,))
        d.ellipse([W * 0.14, H * 0.24, W * 0.86, H * 0.71], outline=(236, 196, 100, 150), width=ow)
        _symbol(d, SYMBOL[idx % len(SYMBOL)], W * 0.5, H * 0.475, W * 0.27, acc, mid + (255,))
        f = hd.font("stencil", max(8, int(H * 0.1)))
        d.text((W * 0.5, H * 0.135), ROMAN[idx % len(ROMAN)], font=f, fill=(242, 214, 130, 255), anchor="mm")
        for x in (0.22, 0.5, 0.78):                                    # petites étoiles en bas
            _symbol(d, "star", W * x, H * 0.85, W * 0.05, (242, 214, 130), bg + (255,))
    return fn


class DropField:
    """Seven columns of drops hanging from the top, the jester under them. Popped drops leave from the bottom, new rows
    push down from the top. / Sept colonnes de gouttes accrochées en haut, le fou dessous."""
    COLS = 7
    MAXR = 7

    def __init__(self, scene, x0):
        self.sc, self.rng = scene, scene.rng
        S = scene.S
        self.D, self.RH = S(48), S(42)
        self.x0, self.top = x0, S(110)
        self.cols = [[] for _ in range(self.COLS)]
        self.clown, self.target, self.next = 3.0, 3, 0.0
        self.held = []                                         # colours held by the jester
        self.fill(4)

    def x(self, c):
        return self.x0 + self.D * (c + 0.5)

    def y(self, r):
        return self.top + self.RH * (r + 0.5)

    def fill(self, rows):
        self.cols = []
        for c in range(self.COLS):
            n = max(1, rows + self.rng.choice((0, 0, 1, -1)))
            col = []
            for r in range(n):
                k = col[-1][0] if col and self.rng.random() < 0.4 else self.rng.randrange(len(DROP_RGB))
                col.append([k, -self.RH * (n + 1)])                 # they come down from above
            self.cols.append(col)

    def push(self):
        """A new row comes down from the top. / Une nouvelle rangée descend du haut."""
        for c, col in enumerate(self.cols):
            for dr in col:
                dr[1] -= self.RH
            col.insert(0, [self.rng.randrange(len(DROP_RGB)), -self.RH])
            while len(col) > self.MAXR:                                # full column: the lowest drop bursts
                k = col.pop()[0]
                self.sc.burst(self.x(c), self.y(len(col)), k, 6)

    def pop(self, c, n):
        """Takes up to n drops at the bottom of column c, then of its neighbours: [(x, y, colour)]."""
        out = []
        for cc in sorted(range(self.COLS), key=lambda k: (abs(k - c), k)):
            col = self.cols[cc]
            while col and len(out) < n:
                out.append((self.x(cc), self.y(len(col) - 1) + col[-1][1], col.pop()[0]))
            if len(out) >= n:
                break
        return out

    def count(self):
        return sum(len(col) for col in self.cols)

    def longest(self):
        return max(len(col) for col in self.cols)

    def step(self, dt):
        v = self.sc.S(700) * dt
        for col in self.cols:
            for dr in col:
                dr[1] = min(0.0, dr[1] + v) if dr[1] < 0 else max(0.0, dr[1] - v)
        self.clown += _clamp(self.target - self.clown, -14 * dt, 14 * dt)


class MagicalDropScene(GameScene):
    """Two fields of drops under a tarot sky, the cards of the two players in the middle. The quota going down pops
    drops, the level rising pushes a row, the card shown flips. / Deux champs de gouttes, les cartes au milieu."""
    THEME = "tarot"
    STATIC = True
    SHADE = (140, 70)
    PILLS = True
    CARD = (150, 236)
    FIELD_BOX = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.fields = {"p1": DropField(self, S(70)), "p2": DropField(self, self.W - S(70) - S(48) * 7)}
        self.flip = {"p1": (-99.0, None), "p2": (-99.0, None)}       # (start, card shown before)
        self.qpop = {"p1": -99.0, "p2": -99.0}
        self.shots = []
        self.push_t = {"p1": 0.0, "p2": 0.0}
        self.rep = {"p1": 0.0, "p2": 0.0}
        self.btn = {"p1": 0, "p2": 0}
        self.warm += [(self.drop, (k, size)) for size in (46, 40, 26) for k in range(len(DROP_RGB))]

    def drop(self, k, size):
        S = self.S
        return self.img(("drop", int(k) % len(DROP_RGB), size), S(size), S(size), drop_draw(DROP_RGB[int(k) % len(DROP_RGB)]))

    def card(self, idx):
        w, h = self.CARD
        return self.img(("card", int(idx) % 24), self.S(w), self.S(h), card_draw(self.hd, int(idx) % 24, self.s), ss=2)

    def jester(self, side):
        S = self.S
        return self.img(("jester", side), S(78), S(70), jester_draw((230, 70, 150) if side == "p1" else (70, 150, 240)))

    def right_on(self, vals):
        cpu = _n(vals.get("cpu_p2"))
        return self.p2_in(vals) or cpu is None or cpu >= 1

    def restart(self, vals, now):
        self.shots = []
        for side, f in self.fields.items():
            f.fill(4)
            self.push_t[side] = now + self.rng.uniform(4, 7)

    def burst(self, x, y, k, n=12):
        col = DROP_RGB[int(k) % len(DROP_RGB)]
        self.fx.sparks(x, y, n, _mix(col, WHITE, 0.35), (200, 520), (0, 360), (0.25, 0.55), 500, "front", 4, 16)
        self.fx.glow(x, y, 12, 64, _mix(col, WHITE, 0.4), 0.25, "front", 0.9, 0.0)

    def _clear(self, f, now):
        """The whole field pops, then new drops come down. / Tout le champ éclate, puis de nouvelles gouttes."""
        i = 0
        for c, col in enumerate(f.cols):
            for r, (k, off) in enumerate(col):
                self.fx.later(0.015 * i, self.burst, f.x(c), f.y(r) + off, k, 6)
                i += 1
        f.cols = [[] for _ in range(f.COLS)]
        self.fx.later(0.8, f.fill, 4)

    def _throw(self, side, n, now):
        """The jester throws a drop up: the column pops n drops. / Le fou lance une goutte : n gouttes éclatent."""
        f, S = self.fields[side], self.S
        c = int(round(f.clown))
        if not f.cols[c]:
            full = [i for i in range(f.COLS) if f.cols[i]]
            c = min(full, key=lambda i: abs(i - c)) if full else c
            f.target = c
        col = f.cols[c]
        y1 = f.y(len(col) - 1) if col else f.top
        k = col[-1][0] if col else self.rng.randrange(len(DROP_RGB))
        self.shots.append({"x": f.x(c), "y0": S(420), "y1": y1, "t0": now, "dur": 0.13, "k": k})
        self.fx.later(0.13, self._pop, side, c, n)

    def _pop(self, side, c, n):
        f, S = self.fields[side], self.S
        got = f.pop(c, n)
        for i, (x, y, k) in enumerate(got):
            self.fx.later(0.035 * i, self.burst, x, y, k)
        if n >= 6:                                                     # big group: a chain
            x = f.x(c)
            self.popup(tr(f"CHAÎNE ×{n // 3}", f"CHAIN ×{n // 3}"), x, S(250), GOLD, 40, life=1.3)
            self.fx.flash((255, 120, 220), 0.12, 0.25)
        if f.count() < 10:                                             # nearly empty: new rows come down
            self.fx.later(0.4, f.push)
            self.fx.later(0.7, f.push)

    def _grab(self, f, now):
        c = int(round(f.clown))
        col = f.cols[c]
        if not col or len(f.held) >= 4:
            return
        k = col[-1][0]
        while col and col[-1][0] == k and len(f.held) < 4:             # the drops of the same colour at the bottom
            col.pop()
            f.held.append(k)

    def _put(self, f, now):
        c = int(round(f.clown))
        col = f.cols[c]
        while f.held and len(col) < f.MAXR:                            # thrown back up, they climb to their place
            col.append([f.held.pop(), self.S(420) - f.y(len(col))])
        f.held = []

    def update(self, vals, now):
        dt = self.dt
        for side, suf in (("p1", ""), ("p2", "_p2")):
            f = self.fields[side]
            ch = self.changed(vals, "quota" + suf)
            if ch:
                old, new = ch
                if new < old:
                    self._throw(side, int(old - new), now)
                    self.qpop[side] = now
                    if new <= 0:
                        self.popup(tr("CLEAR !", "CLEAR!"), f.x(3), self.S(260), GOLD, 56, life=1.6)
                        self.fx.later(0.5, self._clear, f, now)
                elif new > old + 4:                                    # a new round: new fields
                    self._clear(f, now)
            ch = self.changed(vals, "card" + suf)
            if ch:
                self.flip[side] = (now, int(ch[0]))
            st = self.stick(vals, side)
            if st is not None:                                         # the player's stick and buttons (BIOS)
                dx, _, btn = st
                if dx and now >= self.rep[side]:
                    f.target = int(_clamp(f.target + dx, 0, f.COLS - 1))
                    self.rep[side] = now + 0.14
                elif not dx:
                    self.rep[side] = 0.0
                press = btn & ~self.btn[side]
                if press & BTN_A:
                    self._grab(f, now)
                if press & BTN_B:
                    self._put(f, now)
                self.btn[side] = btn
            elif now >= f.next:                                        # autopilot: moves, grabs, throws back
                f.next = now + self.rng.uniform(0.35, 0.9)
                r = self.rng.random()
                if f.held and r < 0.6:
                    self._put(f, now)
                elif r < 0.3:
                    self._grab(f, now)
                else:
                    f.target = self.rng.randrange(f.COLS)
            if now >= self.push_t[side]:                               # a new row now and then
                self.push_t[side] = now + self.rng.uniform(5.5, 9.0)
                if f.longest() < 6:
                    f.push()
            f.step(dt)
        ch = self.changed(vals, "level")
        if ch and ch[1] > ch[0]:                                       # survival: the level rises, a row comes down
            f = self.fields["p1"]
            f.push()
            self.popup(f"LV {int(ch[1])}", f.x(3), self.S(300), (255, 160, 230), 40)

    def draw_field(self, screen, side, vals, now):
        f, S, pg = self.fields[side], self.S, self.pg
        acc = P1C if side == "p1" else P2C
        w = f.D * f.COLS
        if self.FIELD_BOX:                                             # (a backdrop of its own may draw the fields itself)
            self.box(screen, f.x0 - S(14), S(98), w + S(28), S(356), acc, fill=(10, 6, 26, 170), radius=16)
        top_clip = pg.Rect(int(f.x0 - S(10)), S(102), int(w + S(20)), S(348))
        old_clip = screen.get_clip()
        screen.set_clip(top_clip)
        for c, col in enumerate(f.cols):
            for r, (k, off) in enumerate(col):
                img = self.drop(k, 46)
                screen.blit(img, (int(f.x(c) - img.get_width() / 2), int(f.y(r) + off - img.get_height() / 2)))
        screen.set_clip(old_clip)
        if f.longest() >= 6:                                           # danger: the drops reach the jester
            k = 0.5 + 0.5 * math.sin(now * 8)
            g = self.fx.sp.glow(S(60), (255, 60, 60), 3 + 4 * k, hot=0.1)
            for c in range(f.COLS):
                if len(f.cols[c]) >= 6:
                    screen.blit(g, (int(f.x(c) - g.get_width() / 2), int(f.y(6) - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        x = f.x0 + f.D * (f.clown + 0.5)
        jester = self.jester(side)
        bob = math.sin(now * 5 + (0 if side == "p1" else 1.5)) * S(3)
        screen.blit(jester, (int(x - jester.get_width() / 2), int(S(414) - jester.get_height() / 2 + bob)))
        for i, k in enumerate(f.held[:4]):                              # the drops in its hands
            img = self.drop(k, 26)
            screen.blit(img, (int(x - S(30) + i * S(20) - img.get_width() / 2), int(S(372) - img.get_height() / 2)))

    def draw_card(self, screen, side, vals, now, cx):
        S, pg = self.S, self.pg
        idx = _n(vals.get("card" if side == "p1" else "card_p2"))
        if idx is None:
            return
        t0, before = self.flip[side]
        k = (now - t0) / 0.45
        shown = int(idx) if k >= 0.5 or before is None else before
        card = self.card(shown)
        sx = abs(math.cos(min(1.0, max(0.0, k)) * math.pi)) if 0 <= k < 1 else 1.0
        bob = math.sin(now * 1.6 + (0 if side == "p1" else 2.0)) * S(5)
        cy = S(250) + bob
        g = self.fx.sp.glow(S(150), (180, 100, 255) if side == "p1" else (100, 160, 255), 4, hot=0.1)
        screen.blit(g, (int(cx - g.get_width() / 2), int(cy - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        if sx < 0.999:
            w = max(2, int(card.get_width() * sx))
            card = pg.transform.smoothscale(card, (w, card.get_height()))
        screen.blit(card, (int(cx - card.get_width() / 2), int(cy - card.get_height() / 2)))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        right = self.right_on(vals)
        for side in ("p1", "p2"):
            if side == "p2" and not right:
                continue
            self.draw_field(screen, side, vals, now)
        keep = []
        for sh in self.shots:                                          # drops thrown up by the jesters
            k = (now - sh["t0"]) / sh["dur"]
            if k >= 1.0:
                continue
            keep.append(sh)
            img = self.drop(sh["k"], 40)
            y = sh["y0"] + (sh["y1"] - sh["y0"]) * k
            screen.blit(img, (int(sh["x"] - img.get_width() / 2), int(y - img.get_height() / 2)))
        self.shots = keep
        self.top_bar(screen, eng, vals, logo, now)
        cx1, cx2 = W / 2 - S(260), W / 2 + S(260)
        self.draw_card(screen, "p1", vals, now, cx1)
        if right:
            self.draw_card(screen, "p2", vals, now, cx2)
            self.text(screen, "VS", W / 2, S(256), 64, GOLD, key="stencil", align="center", valign="middle", glow=0.7)
        for side, cx, suf, acc in (("p1", cx1, "", P1C), ("p2", cx2, "_p2", P2C)):
            if side == "p2" and not right:
                continue
            name = vals.get("card_name" + suf)
            who = "P1" if side == "p1" else ("P2" if self.p2_in(vals) else "CPU")
            if isinstance(name, str) and name:
                size = self.hd.fit_size(name, "xbold", S(30), S(300), S(16))
                self.label(screen, name, cx, S(392), size / self.s, _mix(acc, WHITE, 0.25), key="xbold", align="center", alpha=150)
            q = _n(vals.get("quota" + suf))
            if q is not None:
                k = max(0.0, 1 - (now - self.qpop[side]) / 0.35)
                self.label(screen, f"{who}  ·  QUOTA {int(q)}", cx, S(436), 30, _mix(WHITE, GOLD, k), key="black", align="center",
                           alpha=160, scale=1 + 0.18 * k)
        lv = _n(vals.get("level"))
        if lv is not None and lv > 0:
            self.label(screen, f"LV {int(lv)}", W / 2, S(372), 30, (255, 170, 235), key="black", align="center", alpha=150)


# ============================================================================ football
TEAMS = ({"shirt": (232, 76, 52), "shorts": (245, 245, 245), "socks": (232, 76, 52)},
         {"shirt": (60, 130, 232), "shorts": (24, 34, 70), "socks": (60, 130, 232)},
         {"shirt": (250, 210, 60), "shorts": (30, 30, 30), "socks": (250, 210, 60)},           # gardiens
         {"shirt": (70, 200, 120), "shorts": (30, 30, 30), "socks": (70, 200, 120)})
HAIR = ((30, 22, 18), (70, 46, 26), (20, 20, 24), (150, 110, 60), (200, 170, 110))


def footballer_draw(kit, skin, hair, frame):
    """Footballer seen from the side, facing right. Frames 0 stand, 1 and 2 run, 3 kick, 4 jump with the arms up.
    / Footballeur de profil, tourné vers la droite."""
    def fn(d, W, H):
        dark = (20, 20, 28, 255)
        ow = max(1, int(W * 0.035))
        sk, sh, so = skin + (255,), kit["shirt"] + (255,), kit["socks"] + (255,)
        cx = W * 0.5
        hip = (cx, H * 0.6)
        feet = {0: ((-0.1, 0.97), (0.08, 0.97)), 1: ((-0.3, 0.94), (0.28, 0.92)), 2: ((-0.12, 0.97), (0.14, 0.88)),
                3: ((-0.1, 0.97), (0.44, 0.78)), 4: ((-0.16, 0.9), (0.14, 0.9))}[frame]
        for i, (fx_, fy) in enumerate(feet):
            foot = (cx + fx_ * W, fy * H)
            knee = ((hip[0] + foot[0]) / 2 + W * 0.06, (hip[1] + foot[1]) / 2 - H * 0.01)
            d.line([hip, knee], fill=sk, width=max(2, int(W * 0.14)))
            d.line([knee, foot], fill=so, width=max(2, int(W * 0.13)))
            d.ellipse([foot[0] - W * 0.1, foot[1] - H * 0.035, foot[0] + W * 0.16, foot[1] + H * 0.02], fill=dark)
        d.rounded_rectangle([cx - W * 0.21, H * 0.49, cx + W * 0.2, H * 0.65], radius=W * 0.05, fill=kit["shorts"] + (255,), outline=dark,
                            width=ow)
        arms = (((-0.2, 0.3), (-0.34, 0.06)), ((0.18, 0.3), (0.34, 0.06))) if frame == 4 else \
            (((-0.16, 0.3), (-0.3, 0.5)), ((0.14, 0.3), (0.3, 0.48)))
        for (ax, ay), (bx, by) in arms:
            d.line([(cx + ax * W, ay * H), (cx + bx * W, by * H)], fill=sk, width=max(2, int(W * 0.11)))
        d.rounded_rectangle([cx - W * 0.23, H * 0.25, cx + W * 0.21, H * 0.54], radius=W * 0.1, fill=sh, outline=dark, width=ow)
        d.line([(cx - W * 0.2, H * 0.34), (cx + W * 0.18, H * 0.34)], fill=_mix(kit["shirt"], WHITE, 0.6) + (255,), width=max(1, int(H * 0.025)))
        d.ellipse([cx - W * 0.16, H * 0.03, cx + W * 0.18, H * 0.25], fill=sk, outline=dark, width=ow)
        d.chord([cx - W * 0.17, H * 0.02, cx + W * 0.19, H * 0.2], 180, 360, fill=hair + (255,))
        d.ellipse([cx + W * 0.08, H * 0.11, cx + W * 0.12, H * 0.14], fill=dark)
    return fn


def soccer_ball_draw(d, W, H):
    d.ellipse([0, 0, W - 1, H - 1], fill=(250, 250, 250, 255), outline=(90, 90, 100, 255), width=max(1, int(W * 0.05)))
    cx, cy, r = W / 2, H / 2, W * 0.17

    def penta(x, y, rr, rot):
        d.polygon([(x + math.cos(rot + i * math.tau / 5) * rr, y + math.sin(rot + i * math.tau / 5) * rr) for i in range(5)], fill=(24, 24, 30, 255))
    penta(cx, cy, r, -math.pi / 2)
    for i in range(5):
        a = -math.pi / 2 + i * math.tau / 5
        penta(cx + math.cos(a) * W * 0.43, cy + math.sin(a) * H * 0.43, r * 0.8, a)
    d.ellipse([W * 0.2, H * 0.12, W * 0.42, H * 0.3], fill=(255, 255, 255, 200))


def goal_draw(pts, bulge):
    """Goal in perspective from its corners (posts in front, net behind). pts are divided by the picture width.
    bulge 0 to 1: the back of the net pushed out by the ball. / But en perspective : poteaux devant, filet derrière."""
    def fn(d, W, H):
        P = {n: (x * W, y * W) for n, (x, y) in pts.items()}
        out = P["out"][0]
        net = (236, 240, 250, 150)
        nw = max(1, int(W * 0.0035))

        def lerp(a, b, t):
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

        def back(ta, tb):
            """Point of the back net: ta from post a to post b, tb from the top to the ground."""
            p = lerp(lerp(P["bta"], P["btb"], ta), lerp(P["ba"], P["bb"], ta), tb)
            push = bulge * math.sin(ta * math.pi) * (0.35 + 0.65 * math.sin(tb * math.pi))
            return (p[0] + out * push, p[1])
        for i in range(9):                                             # filet du fond
            d.line([back(i / 8, j / 6) for j in range(7)], fill=net, width=nw)
        for j in range(6):
            d.line([back(i / 8, j / 5) for i in range(9)], fill=net, width=nw)
        for side, ta in (("a", 0.0), ("b", 1.0)):                      # côtés
            for j in range(5):
                t = j / 4
                d.line([lerp(P["f" + side], P["ft" + side], t), back(ta, 1 - t)], fill=net, width=nw)
        for i in range(9):                                             # toit
            t = i / 8
            d.line([lerp(P["fta"], P["ftb"], t), back(t, 0.0)], fill=net, width=nw)
        pw = max(3, int(W * 0.03))
        for a, b in (("fa", "fta"), ("fta", "ftb"), ("ftb", "fb")):     # poteaux et barre
            d.line([P[a], P[b]], fill=(60, 64, 80, 255), width=pw + max(2, pw // 2))
            d.line([P[a], P[b]], fill=(250, 250, 252, 255), width=pw)
    return fn


class SoccerScene(GameScene):
    """Football seen by the TV camera: the two teams pass the ball, shoot, the keeper saves. When the goals read in
    memory go up, the ball goes into the net: GOAL, confetti, the crowd jumps. / Le match vu par la télévision."""
    THEME = "stadium_day"
    STATIC = True
    SHADE = (100, 0)
    PILLS = True
    POWER = False
    BANNERS = GameScene.BANNERS + (("GOAL!", GOLD), ("BUT !", GOLD))
    FORM = (("gk", 0.03, 0.46), ("def", 0.2, 0.3), ("mid", 0.33, 0.6), ("fwd", 0.44, 0.42))
    MOUTH = (0.37, 0.55)                                       # the goal mouth, in depth / l'entrée du but
    STEPS = (0.74, 0.8, 0.87, 0.93, 1.0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.g = pitch_geom(self.W, self.H, self.s)
        for i, col in enumerate(CONFETTI):
            self.fx.sp.register(f"conf{i}", confetti_img(col, self.s))
        self.players = []
        for team in (0, 1):
            for role, u, v in self.FORM:
                self.players.append({"team": team, "role": role, "u": u if team == 0 else 1 - u, "v": v, "face": 1 if team == 0 else -1,
                                     "run": self.rng.uniform(0, 1), "moving": 0.0, "kick": -99.0, "skin": self.rng.choice(SKIN),
                                     "hair": self.rng.choice(HAIR), "dive": None})
        self.ball = {"u": 0.5, "v": 0.45, "h": 0.0, "rot": 0.0}
        self.owner = None
        self.flight = None
        self.mode = "reset"
        self.until = 0.0
        self.kick_team = 0
        self.next_t = 0.0
        self.scorer = None
        self.pending = []
        self.net = [(-99.0, 0.0), (-99.0, 0.0)]
        self.gpop = {"goals": -99.0, "goals_p2": -99.0}
        self.full_t = {"p1": -99.0, "p2": -99.0}
        self.super_wait = set()                               # teams waiting for the ball to fire their super shot
        self.supers = 0                                       # super shots fired (tests)
        for p in self.players:                                # the players' pictures, prepared during the calm moments
            kit = p["team"] if p["role"] != "gk" else 2 + p["team"]
            self.warm += [(self.player_img, (kit, f, i, fl, p["skin"], p["hair"])) for f in (0, 1, 2, 3, 4) for i in range(len(self.STEPS))
                          for fl in (False, True)]
        self.warm = [(self.goal_img, (side, lvl)) for side in (0, 1) for lvl in range(4)] + self.warm + \
            [(self.ball_img, (i, a)) for i in range(len(self.STEPS)) for a in range(0, 360, 15)]

    # ------------------------------------------------------------ terrain
    def xy(self, u, v):
        y = pitch_y(self.g, v)
        return pitch_x(self.g, self.W, u, y), y

    def step_of(self, v):
        k = 0.74 + 0.26 * _clamp((v - 0.05) / 0.7)
        return min(range(len(self.STEPS)), key=lambda i: abs(self.STEPS[i] - k))

    def player_img(self, kit, frame, step, flip, skin=SKIN[0], hair=HAIR[0]):
        S = self.S
        sc = self.STEPS[step]
        return self.img(("pl", kit, frame, step, skin, hair), S(54 * sc), S(100 * sc), footballer_draw(TEAMS[kit], skin, hair, frame), flip=flip)

    def ball_img(self, step, angle):
        S, sc = self.S, self.STEPS[step]
        return self.rotated(("ball", step), self.img(("ball", step), S(22 * sc), S(22 * sc), soccer_ball_draw), angle, 15)

    def goal_pts(self, side):
        S = self.S
        u0, out = (0.0, -1) if side == 0 else (1.0, 1)
        pts = {}
        for name, v in (("a", self.MOUTH[0]), ("b", self.MOUTH[1])):
            sc = self.STEPS[self.step_of(v)]
            fx_, fy = self.xy(u0, v)
            bx, by = self.xy(u0 + out * 0.026, v)
            h = S(124) * sc
            pts["f" + name], pts["ft" + name] = (fx_, fy), (fx_, fy - h)
            pts["b" + name], pts["bt" + name] = (bx, by), (bx + out * S(4), by - h * 0.82)
        pts["out"] = (out * S(26), 0)
        return pts

    def goal_img(self, side, bulge):
        """Goal picture (four bulge levels kept) and where to put it. / Image du but et sa place."""
        key = ("goal", side, bulge)
        hit = self.imgs.get(key)
        if hit is None:
            pts = self.goal_pts(side)
            xs = [p[0] for n, p in pts.items() if n != "out"]
            ys = [p[1] for n, p in pts.items() if n != "out"]
            m = self.S(40)
            x0, y0 = min(xs) - m, min(ys) - m
            w, h = max(xs) - x0 + m, max(ys) - y0 + m
            local = {n: ((p[0] - x0) / w, (p[1] - y0) / w) if n != "out" else (p[0] / w, 0.0) for n, p in pts.items()}
            hit = self.imgs[key] = (self.hd._surf(draw_img(w, h, goal_draw(local, bulge / 3.0))), int(x0), int(y0))
        return hit

    # ------------------------------------------------------------ le jeu
    def team_players(self, team):
        return [p for p in self.players if p["team"] == team]

    def keeper(self, team):
        return next(p for p in self.players if p["team"] == team and p["role"] == "gk")

    def kick_off(self, team, now, delay=1.6):
        self.mode, self.until, self.kick_team = "reset", now + delay, team
        self.flight, self.owner = None, None
        self.ball.update(u=0.5, v=0.45, h=0.0)

    def restart(self, vals, now):
        self.pending = []
        self.kick_off(0, now, 0.8)

    def give(self, p, now):
        self.owner, self.flight = p, None
        self.next_t = now + self.rng.uniform(0.6, 1.3)
        if p["team"] in self.super_wait and p["role"] != "gk" and self.mode == "play":
            self.super_wait.discard(p["team"])
            self.super_shot(p["team"], now)

    def kick(self, p, to_u, to_v, now, kind="pass", target=None, goal=False, fire=False):
        S = self.S
        b = self.ball
        dist = math.hypot((to_u - b["u"]) * 2.4, to_v - b["v"])
        if kind == "shot":                                              # from far away: a lob
            far = _clamp((dist - 0.6) / 0.8)
            dur = min(0.95, (0.26 if fire else 0.34) + 0.3 * dist + 0.2 * far)
            arc = S(18) + S(130) * far
        elif kind == "long":
            dur, arc = 0.9 + 0.4 * dist, S(110)
        else:
            dur, arc = 0.35 + 0.7 * dist, (S(40) if self.rng.random() < 0.3 else 0)
        self.flight = {"u0": b["u"], "v0": b["v"], "u1": to_u, "v1": to_v, "t0": now, "dur": dur, "arc": arc, "kind": kind,
                       "to": target, "goal": goal, "fire": fire, "team": p["team"]}
        self.owner = None
        p["kick"] = now
        if fire:
            self.fx.glow(*self.xy(b["u"], b["v"]), 20, 120, (255, 150, 60), 0.3, "front", 1.0, 0.0)

    def shoot(self, team, now, goal, fire=False, p=None):
        p = p or self.owner or min(self.team_players(team), key=lambda q: abs(q["u"] - self.ball["u"]) + abs(q["v"] - self.ball["v"]))
        lo, hi = self.MOUTH
        if goal:
            v1 = self.rng.uniform(lo + 0.025, hi - 0.025)
        else:
            v1 = self.rng.uniform(lo + 0.02, hi - 0.02)
        u1 = 1.012 if team == 0 else -0.012
        self.kick(p, u1, v1, now, "shot", goal=goal, fire=fire)
        self.mode = "shot"
        gk = self.keeper(1 - team)
        dive_v = (lo + hi - v1) if goal else v1                       # the keeper dives the wrong way, or to the ball
        gk["dive"] = (now + 0.12, gk["v"], _clamp(dive_v, lo - 0.04, hi + 0.04))

    def goal_event(self, team, now):
        """The goals read in memory went up: the ball has to end in the net. / Le ballon doit finir au fond du filet."""
        f = self.flight
        if self.mode == "shot" and f and f["kind"] == "shot" and f["team"] == team:
            if not f["goal"]:                                           # the shot in flight goes in after all
                f["goal"] = True
                lo, hi = self.MOUTH
                f["v1"] = self.rng.uniform(lo + 0.03, hi - 0.03)
                gk = self.keeper(1 - team)
                gk["dive"] = (now, gk["v"], _clamp(lo + hi - f["v1"], lo - 0.04, hi + 0.04))
            return
        if self.mode != "play":
            self.pending.append(team)
            return
        mates = [p for p in self.team_players(team) if p["role"] != "gk"]
        b = self.ball
        p = self.owner if self.owner is not None and self.owner["team"] == team and self.owner["role"] != "gk" else \
            min(mates, key=lambda q: abs(q["u"] - b["u"]) * 2.4 + abs(q["v"] - b["v"]))
        self.flight = None                                              # the nearest player strikes the ball where it is
        self.shoot(team, now, True, p=p)

    def scored(self, team, now):
        S = self.S
        side = 1 if team == 0 else 0
        self.net[side] = (now, 1.0)
        self.mode, self.until, self.scorer = "celebrate", now + 2.3, team
        self.slam(tr("BUT !", "GOAL!"), GOLD, now, 1.9)
        self.fx.flash((255, 240, 200), 0.25, 0.3)
        self.fx.shake(6, 0.35)
        self.bd.excite(2.2)
        x, y = self.xy(1.0 if team == 0 else 0.0, sum(self.MOUTH) / 2)
        self.fx.sparks(x, y - S(30), 26, (255, 240, 200), (300, 800), (150, 210) if team == 0 else (-30, 30), (0.3, 0.6), 500, "front", 3, 24)
        rng = self.rng
        x0 = self.W * (0.55 if team == 0 else 0.0)
        for i in range(80):                                            # confettis du côté du buteur
            p = self.fx.obj(f"conf{rng.randint(0, len(CONFETTI) - 1)}", x0 + rng.uniform(0, self.W * 0.45), -rng.uniform(10, 140) * self.s,
                            rng.uniform(-60, 60), rng.uniform(80, 200), gravity=60, vrot=rng.uniform(-500, 500), life=rng.uniform(2.6, 3.6),
                            rot=rng.uniform(0, 360))
            p.wob = rng.uniform(40, 90) * self.s
            p.drag = 0.4

    def saved(self, team, now):
        gk = self.keeper(1 - team)
        x, y = self.xy(gk["u"], gk["v"])
        self.fx.sparks(x, y - self.S(40), 10, (255, 255, 255), (200, 500), (0, 360), (0.2, 0.4), 400, "front", 3, 18)
        self.popup(tr("ARRÊT !", "SAVE!"), x + (-1 if team == 0 else 1) * self.S(60), y - self.S(110), CREAM, 34)
        self.mode = "play"
        self.give(gk, now)
        if self.pending:
            self.goal_event(self.pending.pop(0), now)

    def super_shot(self, team, now):
        o = self.owner
        if self.mode != "play" or self.flight is not None or o is None or o["team"] != team or o["role"] == "gk":
            self.super_wait.add(team)                                   # fired as soon as the team has the ball
            if self.mode == "play" and self.flight is None and o is not None and (o["team"] != team or o["role"] == "gk"):
                mates = [q for q in self.team_players(team) if q["role"] != "gk"]
                q = min(mates, key=lambda q: abs(q["u"] - o["u"]) * 2.4 + abs(q["v"] - o["v"]))
                self.kick(o, q["u"], q["v"], now, "long" if o["role"] == "gk" else "pass", target=q)   # the ball comes to the team
            return
        x, y = self.xy(o["u"], o["v"])
        self.supers += 1
        self.popup(tr("SUPER TIR !", "SUPER SHOT!"), x, y - self.S(120), (255, 170, 80), 40, life=1.3)
        self.shoot(team, now, False, fire=True, p=o)

    def decide(self, now):
        p = self.owner
        team = p["team"]
        rng = self.rng
        prog = p["u"] if team == 0 else 1 - p["u"]
        mates = [q for q in self.team_players(team) if q is not p and q["role"] != "gk"]
        foes = [q for q in self.team_players(1 - team) if q["role"] != "gk"]
        r = rng.random()
        if p["role"] == "gk":                                          # the keeper kicks far up the pitch
            q = max(mates, key=lambda q: q["u"] if team == 0 else 1 - q["u"])
            self.kick(p, q["u"], q["v"], now, "long", target=q)
        elif prog > 0.72 and r < 0.5:
            self.shoot(team, now, False)
        elif r < 0.72 and mates:
            ahead = [q for q in mates if (q["u"] - p["u"]) * (1 if team == 0 else -1) > -0.05] or mates
            q = rng.choice(ahead)
            self.kick(p, q["u"], q["v"], now, "pass", target=q)
        else:                                                          # an opponent wins the ball
            q = min(foes, key=lambda q: abs(q["u"] - p["u"]) + abs(q["v"] - p["v"]))
            self.kick(p, q["u"], q["v"], now, "pass", target=q)
        self.next_t = now + rng.uniform(0.7, 1.4)

    def targets(self, now):
        b = self.ball
        for p in self.players:
            team, d = p["team"], (1 if p["team"] == 0 else -1)
            base = next((u, v) for role, u, v in self.FORM if role == p["role"])
            bu = base[0] if team == 0 else 1 - base[0]
            if self.mode == "reset":
                tu, tv = bu, base[1]
                if p["role"] == "fwd" and team == self.kick_team:
                    tu = 0.5 - d * 0.01
                    tv = 0.45
            elif self.mode == "celebrate":
                if team == self.scorer and p["role"] != "gk":
                    tu, tv = (0.86 if team == 0 else 0.14), 0.2 + 0.12 * ("def", "mid", "fwd").index(p["role"])
                else:
                    tu, tv = bu, base[1]
            elif p["role"] == "gk":
                lo, hi = self.MOUTH
                tu, tv = bu, _clamp(b["v"], lo, hi)
            elif p is self.owner:
                tu, tv = p["u"] + d * 0.3, p["v"] + math.sin(now * 1.3 + p["run"] * 6) * 0.12
            else:
                attack = self.owner is not None and self.owner["team"] == team
                push = (b["u"] - 0.5) * 0.7 + (d * 0.12 if attack else -d * 0.08)
                tu, tv = bu + push, base[1] * 0.7 + b["v"] * 0.3
            p["tu"], p["tv"] = _clamp(tu, 0.02, 0.98), _clamp(tv, 0.12, 0.7)
        if self.mode in ("play", "shot") and self.owner is not None:     # the nearest opponent goes for the ball
            o = self.owner
            foes = [q for q in self.team_players(1 - o["team"]) if q["role"] != "gk"]
            q = min(foes, key=lambda q: abs(q["u"] - o["u"]) + abs(q["v"] - o["v"]))
            q["tu"], q["tv"] = o["u"] + 0.03 * o["face"], o["v"]

    def update_game(self, now):
        dt, b = self.dt, self.ball
        if self.mode == "reset" and now >= self.until:
            p = next(q for q in self.players if q["team"] == self.kick_team and q["role"] == "fwd")
            self.mode = "play"
            self.give(p, now)
            if self.pending:
                self.goal_event(self.pending.pop(0), now)
        elif self.mode == "celebrate" and now >= self.until:
            self.kick_off(1 - self.scorer, now, 0.5 if self.pending else 1.3)
        elif self.mode == "play" and self.owner is not None and now >= self.next_t:
            self.decide(now)
        self.targets(now)
        for p in self.players:                                         # everybody runs to their place
            du = _clamp(p["tu"] - p["u"], -0.17 * dt, 0.17 * dt)
            dv = _clamp(p["tv"] - p["v"], -0.42 * dt, 0.42 * dt)
            if p["dive"] is not None:                                  # the keeper's dive
                t0, v0, v1 = p["dive"]
                k = (now - t0) / 0.3
                if k >= 1.6:
                    p["dive"] = None
                elif k >= 0:
                    p["v"] = v0 + (v1 - v0) * min(1.0, k)
                    dv = 0.0
            p["u"] += du
            p["v"] += dv
            sp = math.hypot(du * 2.4, dv) / max(1e-6, dt)
            p["moving"] = sp
            p["run"] += dt * (2.5 + 9 * min(1.0, sp / 0.3))
            if self.owner is p:
                p["face"] = 1 if p["team"] == 0 else -1
            elif abs(du) > 0.02 * dt:
                p["face"] = 1 if du > 0 else -1
            else:
                p["face"] = 1 if b["u"] > p["u"] else -1
        f = self.flight
        if f is not None:                                              # ball in the air or rolling to a player
            k = (now - f["t0"]) / f["dur"]
            if k >= 1.0:
                b.update(u=f["u1"], v=f["v1"], h=0.0)
                self.flight = None
                if f["kind"] == "shot":
                    if f["goal"]:
                        self.scored(f["team"], now)
                    else:
                        self.saved(f["team"], now)
                elif f["to"] is not None:
                    self.give(f["to"], now)
            else:
                to = f["to"]
                if to is not None:                                     # the receiver keeps running: the ball follows him
                    f["u1"], f["v1"] = to["u"] + 0.012 * to["face"], to["v"] + 0.004
                b["u"] = f["u0"] + (f["u1"] - f["u0"]) * k
                b["v"] = f["v0"] + (f["v1"] - f["v0"]) * k
                b["h"] = math.sin(k * math.pi) * f["arc"]
                b["rot"] -= dt * 900 * (1 if f["u1"] > f["u0"] else -1)
        elif self.owner is not None:                                   # at the feet of the player who has it
            o = self.owner
            b.update(u=o["u"] + 0.012 * o["face"], v=o["v"] + 0.004, h=0.0)
            b["rot"] -= dt * 420 * o["face"] * min(1.0, o["moving"] / 0.2)

    def update(self, vals, now):
        for name, team in (("goals", 0), ("goals_p2", 1)):
            ch = self.changed(vals, name)
            if ch:
                self.gpop[name] = now
                if ch[1] > ch[0]:
                    self.goal_event(team, now)
        if self.POWER:
            for side, name, team in (("p1", "power", 0), ("p2", "power_p2", 1)):
                ch = self.changed(vals, name)
                if not ch:
                    continue
                if ch[0] >= 88 and ch[1] < 40:                         # the full gauge is spent: super shot
                    self.super_shot(team, now)
                elif ch[1] >= 95 > ch[0]:
                    self.full_t[side] = now
        self.update_game(now)

    # ------------------------------------------------------------ dessin
    def draw_ball(self, screen, now):
        S, b, pg = self.S, self.ball, self.pg
        x, y = self.xy(b["u"], b["v"])
        sc = self.STEPS[self.step_of(b["v"])]
        sh = self.imgs.get("bsh")
        if sh is None:
            sh = self.imgs["bsh"] = pg.Surface((S(26), S(9)), pg.SRCALPHA)
            pg.draw.ellipse(sh, (0, 0, 0, 90), sh.get_rect())
        screen.blit(sh, (int(x - sh.get_width() / 2), int(y - sh.get_height() / 2)))
        f = self.flight
        if f is not None and f.get("fire"):                            # the super shot burns
            k = (now - f["t0"]) / f["dur"]
            kk = max(0.0, k - 0.12)
            tx, ty = self.xy(f["u0"] + (f["u1"] - f["u0"]) * kk, f["v0"] + (f["v1"] - f["v0"]) * kk)
            ty -= math.sin(kk * math.pi) * f["arc"] + S(10)
            bx, by = x, y - b["h"] - S(10)
            ln = math.hypot(bx - tx, by - ty)
            if ln > 4:
                ang = math.degrees(math.atan2(by - ty, bx - tx))
                for w, col, lv in ((S(22), (255, 110, 30), 9), (S(10), (255, 220, 140), 11)):
                    st = self.fx.sp.streak(ln + S(20), w, col, ang, lv)
                    screen.blit(st, (int((bx + tx) / 2 - st.get_width() / 2), int((by + ty) / 2 - st.get_height() / 2)),
                                special_flags=pg.BLEND_RGB_ADD)
            g = self.fx.sp.glow(S(30), (255, 160, 60), 10, hot=0.6)
            screen.blit(g, (int(bx - g.get_width() / 2), int(by - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        ball = self.ball_img(self.step_of(b["v"]), b["rot"])
        screen.blit(ball, (int(x - ball.get_width() / 2), int(y - b["h"] - S(10) * sc - ball.get_height() / 2)))

    def draw_players(self, screen, now):
        S, pg = self.S, self.pg
        sh = self.imgs.get("psh")
        if sh is None:
            sh = self.imgs["psh"] = pg.Surface((S(40), S(12)), pg.SRCALPHA)
            pg.draw.ellipse(sh, (0, 0, 0, 80), sh.get_rect())
        items = [(p["v"], 0, p) for p in self.players] + [(self.ball["v"] + 0.001, 1, None)]
        for v, kind, p in sorted(items, key=lambda t: t[0]):
            if kind == 1:
                self.draw_ball(screen, now)
                continue
            x, y = self.xy(p["u"], p["v"])
            step = self.step_of(p["v"])
            jump = 0.0
            if self.mode == "celebrate" and p["team"] == self.scorer and p["role"] != "gk":
                frame = 4
                jump = abs(math.sin(now * 7 + p["run"])) * S(18)
            elif now - p["kick"] < 0.22:
                frame = 3
            elif p["moving"] > 0.05:
                frame = 1 + int(p["run"] * 2) % 2
            else:
                frame = 0
            kit = p["team"] if p["role"] != "gk" else 2 + p["team"]
            screen.blit(sh, (int(x - sh.get_width() / 2), int(y - sh.get_height() / 2)))
            if p["dive"] is not None and 0 <= now - p["dive"][0] < 0.7:      # the keeper dives, arms up
                img = self.player_img(kit, 4, step, p["face"] < 0, p["skin"], p["hair"])
                k = min(1.0, (now - p["dive"][0]) / 0.3)
                ang = (25 if p["dive"][2] < p["dive"][1] else -25) * (1 if p["team"] == 0 else -1)
                img = self.rotated(("dive", kit, step, p["face"] < 0, p["skin"], p["hair"]), img, ang, 5)
                screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() - math.sin(k * math.pi) * S(26))))
                continue
            img = self.player_img(kit, frame, step, p["face"] < 0, p["skin"], p["hair"])
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() - jump + S(3))))

    def draw_goals(self, screen, now):
        for side in (0, 1):
            t0, st = self.net[side]
            k = now - t0
            lvl = 0
            if k < 1.2:                                                # the net bulges then settles
                lvl = int(round(3 * st * max(0.0, math.cos(k * 9) * (1 - k / 1.2))))
                lvl = max(0, lvl)
            surf, x0, y0 = self.goal_img(side, lvl)
            screen.blit(surf, (x0, y0))

    def scoreboard(self, screen, vals, now):
        hd, S = self.hd, self.S
        bx, by, bw, bh = S(24), S(12), S(440), S(84)
        self.box(screen, bx, by, bw, bh, (220, 224, 236), fill=(8, 10, 22, 214), radius=14)
        right = "P2" if self.p2_in(vals) else "CPU"
        self.text(screen, "P1", bx + S(26), by + bh / 2, 36, P1C, valign="middle")
        self.text(screen, right, bx + bw - S(26), by + bh / 2, 36, P2C, align="right", valign="middle")
        for name, x, col, align in (("goals", bx + bw / 2 - S(30), P1C, "right"), ("goals_p2", bx + bw / 2 + S(30), P2C, "left")):
            v = _n(vals.get(name))
            if v is None:
                continue
            k = now - self.gpop[name]
            hd.put_number(screen, f"{int(v)}", "black", S(64), WHITE if k < 1.0 and int(k * 8) % 2 == 0 else col, x, by + bh / 2, align,
                          "middle", scale=1.0 + 0.35 * max(0.0, 1 - k / 0.4))
        self.text(screen, "-", bx + bw / 2, by + bh / 2, 48, GREY, align="center", valign="middle", glow=0)

    def power_bars(self, screen, vals, now):
        S, W = self.S, self.W
        for side, name, x0, d, acc in (("p1", "power", S(30), 1, P1C), ("p2", "power_p2", W - S(30), -1, P2C)):
            if side == "p2" and not self.p2_in(vals):
                continue
            p = _n(vals.get(name))
            if p is None:
                continue
            full = p >= 95
            bw = S(300)
            x = x0 if d > 0 else x0 - bw
            self.pill(screen, x - S(14), S(374), bw + S(28), S(78), 150, radius=14)
            lab = tr("SUPER TIR !", "SUPER SHOT!") if full else tr("PUISSANCE", "POWER")
            k = 0.5 + 0.5 * math.sin(now * 10)
            self.text(screen, lab, x, S(382), 24, _mix(GOLD, WHITE, k) if full else CREAM, key="black" if full else "bold", glow=0.5 if full else 0)
            self.bar(screen, x, S(414), bw, S(26), p / 95.0, (255, 220, 120) if full else (255, 170, 60), back=(46, 32, 10))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        self.draw_goals(screen, now)
        self.draw_players(screen, now)
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(560), S(104), now)
        self.scoreboard(screen, vals, now)
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(54), 34, col, align="right")
        if self.POWER:
            self.power_bars(screen, vals, now)


class SuperSidekicks3Scene(SoccerScene):
    THEME = "stadium_day"


class Ultimate11Scene(SoccerScene):
    THEME = "stadium_night"
    POWER = True


# ============================================================================ Sengoku 3
THROWN = (("SHURIKEN", "SHURIKEN"), ("KUNAI", "KUNAI"), ("BOMBE", "BOMB"), ("DISQUE", "SAUCER"))


def ninja_draw(frame):
    """Shadow warrior seen from the side, facing left, red eyes, a sword. Frames 0 and 1 walk, 2 hit, 3 strike.
    / Guerrier de l'ombre de profil, tourné vers la gauche."""
    def fn(d, W, H):
        body = (22, 18, 34, 255)
        edge = (170, 140, 210, 255)
        cx = W * 0.55
        hip = (cx, H * 0.62)
        legs = {0: ((-0.16, 1.0), (0.14, 1.0)), 1: ((-0.04, 1.0), (0.04, 1.0)), 2: ((0.06, 1.0), (0.3, 0.96)),
                3: ((-0.3, 1.0), (0.18, 1.0))}[frame]
        lean = {0: 0.0, 1: 0.0, 2: 0.1, 3: -0.12}[frame]
        for fx_, fy in legs:
            foot = (cx + fx_ * W, fy * H - H * 0.015)
            knee = ((hip[0] + foot[0]) / 2 - W * 0.05, (hip[1] + foot[1]) / 2)
            d.line([hip, knee, foot], fill=body, width=max(2, int(W * 0.15)), joint="curve")
        tx = lean * W
        d.polygon([(cx - W * 0.2 + tx, H * 0.3), (cx + W * 0.18 + tx, H * 0.28), (cx + W * 0.16, H * 0.64), (cx - W * 0.16, H * 0.64)], fill=body,
                  outline=edge)
        d.ellipse([cx - W * 0.2 + tx, H * 0.08, cx + W * 0.14 + tx, H * 0.32], fill=body, outline=edge)
        d.rectangle([cx - W * 0.2 + tx, H * 0.16, cx + W * 0.02 + tx, H * 0.205], fill=(70, 20, 30, 255))
        d.ellipse([cx - W * 0.17 + tx, H * 0.165, cx - W * 0.1 + tx, H * 0.2], fill=(255, 70, 50, 255))
        d.polygon([(cx + W * 0.08 + tx, H * 0.26), (cx + W * 0.45 + tx, H * 0.2 + math.sin(frame) * H * 0.03), (cx + W * 0.4 + tx, H * 0.3),
                   (cx + W * 0.1 + tx, H * 0.33)], fill=(190, 30, 44, 255))
        hand = (cx - W * 0.34 + tx, H * 0.46) if frame != 3 else (cx - W * 0.42 + tx, H * 0.36)
        tip = (hand[0] - W * 0.2, hand[1] - H * 0.3) if frame != 3 else (hand[0] - W * 0.4, hand[1] + H * 0.04)
        d.line([(cx - W * 0.04 + tx, H * 0.36), hand], fill=body, width=max(2, int(W * 0.12)))
        d.line([hand, tip], fill=(210, 214, 226, 255), width=max(2, int(W * 0.05)))
        d.line([hand, (hand[0] + (tip[0] - hand[0]) * 0.18, hand[1] + (tip[1] - hand[1]) * 0.18)], fill=(120, 30, 30, 255),
               width=max(2, int(W * 0.07)))
    return fn


def shuriken_draw(d, W, H):
    c = W / 2
    pts = []
    for i in range(8):
        a = i * math.pi / 4
        r = W * 0.49 if i % 2 == 0 else W * 0.16
        pts.append((c + math.cos(a) * r, c + math.sin(a) * r))
    d.polygon(pts, fill=(196, 204, 220, 255), outline=(40, 44, 60, 255))
    d.ellipse([c - W * 0.08, c - W * 0.08, c + W * 0.08, c + W * 0.08], fill=(30, 30, 40, 255))


def kunai_draw(d, W, H):
    d.polygon([(W * 0.42, H * 0.5), (W * 0.66, H * 0.18), (W, H * 0.5), (W * 0.66, H * 0.82)], fill=(206, 212, 228, 255), outline=(40, 44, 60, 255))
    d.rectangle([W * 0.14, H * 0.38, W * 0.44, H * 0.62], fill=(110, 40, 40, 255))
    d.ellipse([0, H * 0.24, W * 0.18, H * 0.76], outline=(196, 204, 220, 255), width=max(2, int(H * 0.12)))


def bomb_draw(d, W, H):
    d.ellipse([W * 0.06, H * 0.2, W * 0.86, H - 1], fill=(30, 30, 40, 255), outline=(90, 90, 110, 255), width=max(1, int(W * 0.05)))
    d.ellipse([W * 0.2, H * 0.32, W * 0.4, H * 0.5], fill=(120, 120, 140, 255))
    d.line([(W * 0.6, H * 0.26), (W * 0.8, H * 0.04)], fill=(200, 170, 110, 255), width=max(2, int(W * 0.08)))
    d.ellipse([W * 0.74, 0, W * 0.94, H * 0.16], fill=(255, 210, 90, 255))


def saucer_draw(d, W, H):
    d.ellipse([0, H * 0.18, W - 1, H * 0.82], fill=(220, 180, 70, 255), outline=(110, 80, 20, 255), width=max(1, int(W * 0.04)))
    d.ellipse([W * 0.3, H * 0.36, W * 0.7, H * 0.64], fill=(250, 226, 140, 255), outline=(110, 80, 20, 255), width=max(1, int(W * 0.03)))


THROWN_DRAW = (shuriken_draw, kunai_draw, bomb_draw, saucer_draw)


def slash_draw(color):
    """Crescent of a sword stroke. / Croissant d'un coup de sabre."""
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=color + (230,))
        d.ellipse([W * 0.16, -H * 0.02, W * 1.08, H * 0.94], fill=(0, 0, 0, 0))
    return fn


class SengokuScene(GameScene):
    """Shadow warriors come out of the temple, the throwing weapons fly when their count goes down, the health and the
    magic of each fighter in a panel, the magic sweeps the screen. / Les guerriers de l'ombre sortent du temple."""
    THEME = "temple"
    SHADE = (120, 150)
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS + (("MAGIE !", (150, 200, 255)), ("MAGIC!", (150, 200, 255)))
    PW = 600

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        for name, fn in zip(("shuriken", "kunai", "bomb", "saucer"), THROWN_DRAW):
            w, h = (S(44), S(44)) if name in ("shuriken", "saucer") else ((S(60), S(24)) if name == "kunai" else (S(38), S(40)))
            self.fx.sp.register(name, draw_img(w, h, fn))
        self.enemies = []
        self.next_enemy = 0.0
        self.hurt = {"p1": -99.0, "p2": -99.0}
        self.wpop = {"p1": -99.0, "p2": -99.0}
        self.mpop = {"p1": -99.0, "p2": -99.0}
        self.slash_t = {"p1": 0.0, "p2": 0.0}
        self.btn = {"p1": 0, "p2": 0}
        self.slashes = []
        self.cuts = 0                                          # sword strokes given (tests)

    def move(self, vals, now, idle):
        return 0.1 if idle else 0.35

    def panel_x(self, side):
        return self.S(28) if side == "p1" else self.W - self.S(28) - self.S(self.PW)

    def hand(self, side):
        S = self.S
        x0 = self.panel_x(side)
        return (x0 + S(self.PW) - S(30), S(272)) if side == "p1" else (x0 + S(30), S(272))

    def restart(self, vals, now):
        self.enemies = []
        self.next_enemy = now + 0.3

    def alive(self):
        return [e for e in self.enemies if e["dead"] is None]

    def spawn(self, now):
        S, W = self.S, self.W
        n = len(self.alive())
        e = {"x": W + S(70), "stop": S(1180) - n * S(120) + self.rng.uniform(-S(20), S(20)), "hp": 2, "hit": -99.0, "dead": None,
             "ph": self.rng.uniform(0, 6), "strike": -99.0, "v": self.rng.uniform(480, 600) * self.s}
        self.enemies.append(e)

    def target(self, side, arrived=False):
        """The warrior the player aims at: one that has arrived first, else the nearest on the screen. / Le guerrier visé."""
        here = [e for e in self.alive() if e["x"] <= e["stop"] + 1]
        alive = here if (here or arrived) else ([e for e in self.alive() if e["x"] < self.W - self.S(90)] or self.alive())
        if not alive:
            return None
        return min(alive, key=lambda e: e["x"]) if side == "p1" else max(alive, key=lambda e: e["x"])

    def hit(self, e, dmg=1, kind="cut"):
        if e is None or e["dead"] is not None:
            return
        fx, S = self.fx, self.S
        e["hp"] -= dmg
        e["hit"] = fx.now
        x, y = e["x"], S(380)
        fx.sparks(x, y, 10, (255, 220, 200), (200, 600), (0, 360), (0.15, 0.35), 500, "front", 3, 20)
        if e["hp"] <= 0:                                               # defeated: smoke and red sparks
            e["dead"] = fx.now
            fx.smoke(x, y, 6, (14, 26), 2.2, (0.6, 1.1), (20, 60), 24, (40, 34, 50), 190, "front")
            fx.sparks(x, y, 16, (255, 80, 60), (200, 700), (180, 360), (0.3, 0.6), 700, "front", 3, 26)
            self.bd.excite(0.4)

    def throw(self, side, weapon, now):
        fx, S = self.fx, self.S
        e = self.target(side)
        hx, hy = self.hand(side)
        tx, ty = (e["x"], S(372)) if e is not None else (self.W / 2 + self.rng.uniform(-S(200), S(200)), S(360))
        w = int(weapon) % 4
        name = ("shuriken", "kunai", "bomb", "saucer")[w]
        if w == 1:                                                     # kunai: straight, pointing where it flies
            ang = -math.degrees(math.atan2(ty - hy, tx - hx))
            p = fx.projectile(name, hx, hy, tx, ty, 0.28, 0, lambda x, y, e=e: self.hit(e, 2), spin=0.0, trail=0)
            p.rot = ang
        elif w == 2:                                                   # bomb: arc and explosion
            def boom(x, y):
                fx.explosion(x, y, 0.6, layer_back=False)
                for o in self.alive():
                    if abs(o["x"] - x) < S(160):
                        self.hit(o, 3)
            fx.projectile(name, hx, hy, tx, ty + S(20), 0.6, 150, boom, spin=360.0, trail=0.04)
        elif w == 3:                                                   # saucer: goes and comes back
            def back(x, y, e=e):
                self.hit(e, 2)
                fx.projectile("saucer", x, y, hx, hy, 0.4, 30, lambda a, b: None, spin=1440.0, trail=0)
            fx.projectile(name, hx, hy, tx, ty, 0.4, 30, back, spin=1440.0, trail=0)
        else:
            fx.projectile(name, hx, hy, tx, ty, 0.3, 14, lambda x, y, e=e: self.hit(e, 1), spin=1440.0, trail=0)

    def slash(self, side, now, dmg=1):
        e = self.target(side, arrived=True)
        if e is None:
            return
        S = self.S
        self.cuts += 1
        self.slashes.append((e["x"], S(366), now, 1 if side == "p1" else -1))
        self.fx.glow(e["x"], S(366), 30, 130, (200, 220, 255), 0.18, "front", 0.9, 0.0, hot=0.6)
        self.fx.sparks(e["x"], S(366), 12, (230, 240, 255), (300, 800), (-60, 60) if side == "p1" else (120, 240), (0.15, 0.35), 300,
                       "front", 3, 30)
        self.fx.later(0.06, self.hit, e, dmg)

    def magic(self, side, level, now):
        """The magic sweeps the screen: a crescent of light, every warrior falls. / La magie balaie l'écran."""
        S, fx = self.S, self.fx
        hx, hy = self.hand(side)
        d = 1 if side == "p1" else -1
        for i in range(5):
            fx.later(i * 0.05, fx.tracer, hx, S(330) + (i - 2) * S(36), hx + d * self.W, S(330) + (i - 2) * S(36), 3600, (170, 210, 255), 22,
                     520, "front", False)
        fx.glow(hx, hy, 40, 260 * level, (150, 190, 255), 0.5, "front", 1.0, 0.0, hot=0.6)
        fx.flash((120, 160, 255), 0.3 * level, 0.4)
        fx.shake(6, 0.4)
        for e in self.alive():
            fx.later(abs(e["x"] - hx) / (3600 * self.s), self.hit, e, 9)
        self.slam(tr("MAGIE !", "MAGIC!"), (150, 200, 255), now, 1.3)
        self.mpop[side] = now

    def update(self, vals, now):
        S, fx = self.S, self.fx
        for side, suf in (("p1", ""), ("p2", "_p2")):
            playing = self.p1_in(vals) if side == "p1" else self.p2_in(vals)
            if not playing:
                continue
            ch = self.changed(vals, "stars" + suf)
            if ch and ch[1] < ch[0]:                                   # a throwing weapon flies
                w = _n(vals.get("weapon" + suf)) or 0
                for i in range(min(3, int(ch[0] - ch[1]))):
                    fx.later(i * 0.12, self.throw, side, w, now)
            ch = self.changed(vals, "weapon" + suf)
            if ch:
                self.wpop[side] = now
                x0 = self.panel_x(side)
                self.popup(tr(*THROWN[int(ch[1]) % 4]) + tr(" !", "!"), x0 + S(self.PW) / 2, S(222), GOLD, 38, life=1.3, key="stencil")
            ch = self.changed(vals, "magic" + suf)
            if ch and ch[1] < ch[0] - 10:                              # the magic gauge empties: magic attack
                self.magic(side, _clamp((ch[0] - ch[1]) / 56.0, 0.3, 1.0), now)
            elif ch and ch[1] >= 56 > ch[0]:
                self.mpop[side] = now
            ch = self.changed(vals, "health" + suf)
            if ch and ch[1] < ch[0]:                                   # hit by a warrior
                self.hurt[side] = now
                fx.shake(5 + (ch[0] - ch[1]) * 0.1, 0.3)
                fx.flash((150, 0, 0), 0.12, 0.25)
                x0 = self.panel_x(side)
                fx.sparks(x0 + S(self.PW) / 2, S(300), 14, (255, 120, 90), (200, 600), (200, 340), (0.2, 0.5), 600, "front", 3, 20)
                e = self.target(side)
                if e is not None:
                    e["strike"] = now
                if ch[1] <= 0:
                    self.popup("K.O.", x0 + S(self.PW) / 2, S(230), RED, 56, life=1.4, key="stencil")
            ch = self.changed(vals, "score" + suf)
            if ch and ch[1] > ch[0]:                                   # points: a warrior falls under the sword
                self.slash(side, now, 2)
            st = self.stick(vals, side)
            if st is not None:                                         # button A: a sword stroke
                press = st[2] & ~self.btn[side]
                self.btn[side] = st[2]
                if press & BTN_A:
                    self.slash(side, now)
            elif _n(vals.get("score" + suf)) is None and now >= self.slash_t[side]:     # score not known: strokes now and then
                self.slash_t[side] = now + self.rng.uniform(1.1, 2.4)
                self.slash(side, now)
        if now >= self.next_enemy:
            self.next_enemy = now + self.rng.uniform(1.0, 2.2)
            if len(self.alive()) < 4:
                self.spawn(now)

    def draw_enemies(self, screen, now):
        S, dt = self.S, self.dt
        keep = []
        for e in self.enemies:
            if e["dead"] is not None:
                k = (now - e["dead"]) / 0.5
                if k >= 1:
                    continue
            keep.append(e)
            if e["dead"] is None and e["x"] > e["stop"]:
                e["x"] -= e["v"] * dt
                walking = True
            else:
                walking = False
            if now - e["strike"] < 0.3:
                frame = 3
            elif now - e["hit"] < 0.18 or e["dead"] is not None:
                frame = 2
            elif walking:
                frame = int(now * 6 + e["ph"]) % 2
            else:
                frame = int(now * 1.5 + e["ph"]) % 2
            img = self.img(("ninja", frame), S(96), S(144), ninja_draw(frame))
            y = S(448) - img.get_height()
            x = e["x"] - img.get_width() / 2
            if e["dead"] is None:                                      # a faint glow behind: readable on the dark ground
                g = self.fx.sp.glow(S(70), (90, 50, 120), 4, hot=0.0)
                screen.blit(g, (int(e["x"] - g.get_width() / 2), int(S(372) - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
            if e["dead"] is not None:                                  # falls back and fades
                k = (now - e["dead"]) / 0.5
                x += S(60) * k
                img.set_alpha(int(255 * (1 - k)))
                screen.blit(img, (int(x), int(y + S(20) * k)))
                img.set_alpha(255)
                continue
            screen.blit(img, (int(x), int(y)))
            if now - e["hit"] < 0.08:
                g = self.fx.sp.glow(S(50), (255, 255, 255), 7, hot=0.6)
                screen.blit(g, (int(e["x"] - g.get_width() / 2), int(S(380) - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
        self.enemies = keep

    def draw_slashes(self, screen, now):
        S = self.S
        keep = []
        for x, y, t0, d in self.slashes:
            k = (now - t0) / 0.22
            if k >= 1:
                continue
            keep.append((x, y, t0, d))
            img = self.img(("slash", d), S(210), S(270), slash_draw((235, 245, 255)), flip=d < 0)
            sc = 0.7 + 0.5 * k
            surf = self.pg.transform.smoothscale(img, (int(img.get_width() * sc), int(img.get_height() * sc)))
            surf.set_alpha(int(255 * (1 - k)))
            screen.blit(surf, (int(x - surf.get_width() / 2), int(y - surf.get_height() / 2)))
        self.slashes = keep

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        self.draw_enemies(screen, now)
        self.draw_slashes(screen, now)
        sp, add = self.fx.sp, self.pg.BLEND_RGB_ADD
        for p in self.fx.parts:                                        # a glow under the throwing weapons in flight
            if p.kind == "proj" and p.name in ("shuriken", "kunai", "bomb", "saucer") and p.t0 <= now:
                g = sp.glow(S(30), (255, 210, 150) if p.name == "bomb" else (190, 220, 255), 6, hot=0.4)
                screen.blit(g, (int(p.x - g.get_width() / 2), int(p.y - g.get_height() / 2)), special_flags=add)
        self.top_bar(screen, eng, vals, logo, now, right=self.p2_in(vals))
        t = _n(vals.get("time"))
        if t is not None:                                              # timer under the logo
            low = t <= 10
            pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
            self.box(screen, W / 2 - S(76), S(126), S(152), S(80), RED if low else (230, 120, 120))
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
        if hurt:                                                       # hit: the panel flashes red, a cut across it
            red = self.imgs.get("hurt")
            if red is None:
                red = self.imgs["hurt"] = pg.Surface((pw - S(8), ph - S(8))).convert()
            red.fill((int(70 * hurt), 0, 0))
            screen.blit(red, (x0 + S(4), y0 + S(4)), special_flags=pg.BLEND_RGB_ADD)
            cut = self.fx.sp.streak(S(380), S(8), (255, 90, 70), -24 if side == "p1" else 24, 11 * hurt)
            screen.blit(cut, (int(x0 + pw / 2 - cut.get_width() / 2), int(y0 + ph / 2 - cut.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        left = side == "p1"
        tx = x0 + S(24) if left else x0 + pw - S(24)
        al = "left" if left else "right"
        name = vals.get("fighter_name" + suf)
        if isinstance(name, str) and name:
            size = hd.fit_size(name, "stencil", S(40), S(300), S(22))
            hd.put(screen, hd.text(name, "stencil", size, GOLD, 0.4), tx, y0 + S(36), al, "middle")
        w = _n(vals.get("weapon" + suf))
        n = _n(vals.get("stars" + suf))
        if w is not None:                                              # throwing weapon and how many are left
            wi = int(w) % 4
            k = max(0.0, 1 - (now - self.wpop[side]) / 0.5)
            icon = self.fx.sp.base.get(("obj", ("shuriken", "kunai", "bomb", "saucer")[wi]))
            ix = x0 + pw - S(200) if left else x0 + S(110)
            if icon is not None:
                sc = 1.3 + 0.4 * k
                ic = pg.transform.smoothscale(icon, (int(icon.get_width() * sc), int(icon.get_height() * sc)))
                screen.blit(ic, (int(ix - ic.get_width() / 2), int(y0 + S(36) - ic.get_height() / 2)))
            if n is not None:
                self.text(screen, f"× {int(n)}", ix + S(36), y0 + S(36), 30, WHITE, key="black", valign="middle")
        for row, (lab, name, mx, col, back) in enumerate(((tr("VIE", "HEALTH"), "health", 100.0, None, (40, 14, 14)),
                                                          (tr("MAGIE", "MAGIC"), "magic", 56.0, (90, 150, 255), (14, 20, 46)))):
            v = _n(vals.get(name + suf))
            if v is None:
                continue
            y = y0 + S(92) + row * S(56)
            frac = v / mx
            if col is None:
                col = (90, 240, 90) if frac > 0.4 else ((255, 200, 60) if frac > 0.2 else RED)
            full = name == "magic" and v >= mx
            if full:                                                   # full magic: the gauge shines
                col = _mix((150, 200, 255), WHITE, 0.5 + 0.5 * math.sin(now * 8))
            self.text(screen, lab, tx, y, 22, CREAM, key="bold", align=al, valign="middle", glow=0)
            bx = x0 + S(150) if left else x0 + S(24)
            self.bar(screen, bx, y - S(14), pw - S(174), S(28), frac, col, back=back)
            if full:
                k = max(0.0, 1 - (now - self.mpop[side]) / 0.6)
                self.text(screen, "MAX", bx + (pw - S(174)) / 2, y, 22, (16, 26, 80), key="black", align="center", valign="middle", glow=0,
                          scale=1 + 0.3 * k)


SCENES = {"pulstar": PulstarScene, "magdrop3": MagicalDropScene, "ssideki3": SuperSidekicks3Scene, "ssideki4": Ultimate11Scene,
          "sengoku3": SengokuScene}
