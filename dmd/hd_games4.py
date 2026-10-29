"""HD scenes of the fourth batch of Neo Geo games done one by one (1.20), each drawn after screenshots of its game:
Strikers 1945 Plus, Street Hoop, Super Dodge Ball... Each game has its own animated backdrop and reacts to the values
read in its memory. The characters, the planes of fiction and the robots are creations of the program in the spirit
of the games, the real planes are drawn after the real ones.

Scènes HD du quatrième lot de jeux Neo Geo faits un par un (1.20), chacune dessinée d'après des captures de son jeu.
Les personnages, les engins imaginaires et les robots sont des créations du programme dans l'esprit des jeux, les
vrais avions sont dessinés d'après les vrais.
"""

import math
import threading

from .hd_games import CREAM, GOLD, GREY, RED, WHITE, GameScene, _clamp, _mix, _n, draw_img
from .hd_games3 import DARK, AeroFightersScene, _capsule, _lerp, _shape, bomb_icon_draw, bomber_draw
from .hd_themes4 import HOOP_X, NB_COLS, NB_ROWS, dodge_y, hoop_y, nb_grid, ts_fields, ts_forest_tile                      # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr


# ============================================================================ Strikers 1945 Plus
def s45_plane_draw(kind, body, accent, dark=(26, 24, 22)):
    """The planes of Strikers 1945 Plus seen from above, nose to the right, drawn after the real ones: 1 P-38 Lightning
    (two booms), 2 F5U (a round wing, two big propellers), 3 Spitfire (elliptic wings), 4 Ta-152 (long wings), 5 Zero,
    6 Fiat G.56, 7 a canard plane with its propeller at the back. / Les avions vus du dessus, d'après les vrais."""
    def fn(d, W, H):
        line = dark + (255,)
        ow = max(1.0, W * 0.012)
        b, sh, lt = body + (255,), _mix(body, (0, 0, 0), 0.25) + (255,), _mix(body, WHITE, 0.35) + (255,)
        acc = accent + (255,)
        prop = (230, 230, 236, 90)

        def P(pts):
            return [(x * W, y * H) for x, y in pts]

        def disc(x, y, r):
            d.ellipse([(x - 0.02) * W, (y - r) * H, (x + 0.02) * W, (y + r) * H], fill=prop)
            d.ellipse([(x - 0.012) * W, (y - 0.028) * H, (x + 0.022) * W, (y + 0.028) * H], fill=(210, 190, 120, 255))

        def canopy(x, w=0.09):
            _shape(d, P([(x + w, 0.5), (x + w * 0.7, 0.468), (x, 0.47), (x, 0.53), (x + w * 0.7, 0.532)]), (90, 150, 200, 255), line, ow)
            d.polygon(P([(x + w * 0.8, 0.49), (x + w * 0.6, 0.477), (x + w * 0.2, 0.478), (x + w * 0.2, 0.49)]), fill=(200, 236, 255, 255))

        def fuselage(x0, x1, w):
            _shape(d, P([(x1, 0.5), (x1 - 0.07, 0.5 - w), (x0 + 0.05, 0.5 - w * 0.55), (x0, 0.5), (x0 + 0.05, 0.5 + w * 0.55),
                         (x1 - 0.07, 0.5 + w)]), b, line, ow)
            d.polygon(P([(x1 - 0.08, 0.5 - w * 0.5), (x0 + 0.08, 0.5 - w * 0.3), (x0 + 0.08, 0.5 - w * 0.05), (x1 - 0.08, 0.5 - w * 0.1)]), fill=lt)

        def wings(front, back, tip_f, tip_b, span, round_tip=False):
            for sgn in (1, -1):
                def m(y):
                    return 0.5 + sgn * (y - 0.5)
                pts = [(front, m(0.47)), (tip_f, m(0.5 - span)), (tip_b, m(0.5 - span)), (back, m(0.47))]
                if round_tip:
                    pts = [(front, m(0.47)), (tip_f, m(0.5 - span + 0.04)), ((tip_f + tip_b) / 2, m(0.5 - span)), (tip_b, m(0.5 - span + 0.04)),
                           (back, m(0.47))]
                _shape(d, P(pts), sh, line, ow)
                d.line(P([(front - 0.01, m(0.45)), (tip_f - 0.005, m(0.5 - span + 0.05))]), fill=lt, width=max(1, int(H * 0.012)))
                d.line(P([((tip_f + tip_b) / 2 - 0.02, m(0.5 - span + 0.07)), ((tip_f + tip_b) / 2 + 0.02, m(0.5 - span + 0.07))]), fill=acc,
                       width=max(2, int(H * 0.03)))

        def tail(x, span, w=0.08):
            for sgn in (1, -1):
                _shape(d, P([(x + w, 0.5 + sgn * 0.03), (x + w * 0.5, 0.5 + sgn * span), (x, 0.5 + sgn * span), (x, 0.5 + sgn * 0.03)]), sh, line, ow)
        k = kind if 1 <= kind <= 7 else 1
        if k == 1:                                                     # P-38 : deux poutres
            for y in (0.3, 0.7):
                _shape(d, P([(0.8, y), (0.74, y - 0.05), (0.1, y - 0.03), (0.06, y), (0.1, y + 0.03), (0.74, y + 0.05)]), b, line, ow)
                d.line(P([(0.06, y), (0.18, y)]), fill=line, width=max(2, int(H * 0.03)))
                disc(0.82, y, 0.15)
            _shape(d, P([(0.62, 0.02), (0.5, 0.02), (0.5, 0.98), (0.62, 0.98)]), sh, line, ow)
            _shape(d, P([(0.16, 0.26), (0.08, 0.26), (0.08, 0.74), (0.16, 0.74)]), sh, line, ow)
            fuselage(0.4, 0.9, 0.06)
            canopy(0.66)
            d.ellipse(P([(0.86, 0.48), (0.9, 0.52)])[0] + P([(0.86, 0.48), (0.9, 0.52)])[1], fill=(200, 230, 255, 255))
        elif k == 2:                                                   # F5U : aile ronde, deux grosses hélices
            d.ellipse(P([(0.22, 0.12), (0.84, 0.88)])[0] + P([(0.22, 0.12), (0.84, 0.88)])[1], fill=b, outline=line, width=int(ow))
            d.chord(P([(0.26, 0.16), (0.8, 0.84)])[0] + P([(0.26, 0.16), (0.8, 0.84)])[1], 200, 320, fill=lt)
            for y in (0.26, 0.74):
                disc(0.84, y, 0.22)
            for y in (0.42, 0.58):
                d.line(P([(0.08, y), (0.26, y)]), fill=line, width=max(2, int(H * 0.03)))
            _shape(d, P([(0.24, 0.44), (0.06, 0.44), (0.06, 0.56), (0.24, 0.56)]), sh, line, ow)
            canopy(0.6, 0.1)
        elif k == 7:                                                   # canard, hélice à l'arrière
            for sgn in (1, -1):
                def m(y):
                    return 0.5 + sgn * (y - 0.5)
                _shape(d, P([(0.42, m(0.46)), (0.2, m(0.06)), (0.12, m(0.06)), (0.18, m(0.46))]), sh, line, ow)
                d.line(P([(0.18, m(0.28)), (0.28, m(0.28))]), fill=line, width=max(2, int(H * 0.03)))
                _shape(d, P([(0.84, m(0.47)), (0.78, m(0.36)), (0.74, m(0.36)), (0.76, m(0.47))]), sh, line, ow)
            fuselage(0.08, 0.96, 0.06)
            canopy(0.62)
            disc(0.06, 0.5, 0.2)
        else:
            span = {3: 0.47, 4: 0.48, 5: 0.46, 6: 0.44}[k]
            if k == 3:
                wings(0.62, 0.42, 0.58, 0.48, span, round_tip=True)
                tail(0.06, 0.18)
            elif k == 4:
                wings(0.58, 0.48, 0.55, 0.5, span)
                tail(0.04, 0.16)
            elif k == 5:
                wings(0.6, 0.44, 0.56, 0.5, span, round_tip=True)
                tail(0.06, 0.17)
            else:
                wings(0.6, 0.44, 0.55, 0.49, span)
                tail(0.06, 0.16)
                d.rectangle(P([(0.42, 0.535), (0.56, 0.56)])[0] + P([(0.42, 0.535), (0.56, 0.56)])[1], fill=(50, 50, 50, 255))
            fuselage(0.04 if k == 4 else 0.06, 0.97 if k == 4 else 0.93, 0.065)
            canopy(0.56 if k != 4 else 0.52)
            disc(0.97 if k == 4 else 0.93, 0.5, 0.2)
    return fn


def s45_bomber_draw(d, W, H):
    """A friendly heavy bomber of the bomb, seen from above, nose to the right. / Un gros bombardier allié, vu du dessus."""
    bomber_draw(d, W, H)


class StrikersScene(AeroFightersScene):
    """Strikers 1945 Plus as in the game: the plane chosen by the player over war-torn ground, its shots, the super shot,
    the bomb that brings a formation of bombers. On the sides, the game's panels: the score, the lives, the bombs and
    the super shot gauge. / Comme dans le jeu : l'avion choisi au-dessus d'un sol ravagé, les panneaux sur les côtés."""
    THEME = "s45_ground"
    SHADE = (60, 60)
    PROP = True
    ACC = {"p1": (250, 220, 120), "p2": (250, 250, 250)}
    BODY = {"p1": (170, 62, 50), "p2": (60, 104, 190)}
    SHOT = {"p1": (255, 236, 130), "p2": (170, 226, 255)}
    SHOT_SIZE = ((6, 64), (9, 90))
    BOMB = ((200, 60, 50), (200, 160, 90))
    ODD = "bomber"
    PANEL = 236                                         # width of the side panels / largeur des panneaux de côté
    ZONE = (150, 330)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.supers = 0                                 # super shots shown (tests)
        self.raids = 0                                  # bombs shown as a formation of bombers (tests)

    def kind(self, vals, side):
        v = _n(vals.get("plane" if side == "p1" else "plane_p2"))
        return int(v) if v is not None and 1 <= v <= 7 else 1

    def plane_fn(self, side, kind):
        return s45_plane_draw(kind, self.BODY[side], self.ACC[side])

    def pos(self, side, now):
        P, S = self.ships[side], self.S
        bx = S(self.PANEL + 80) + P["x"] * S(620)
        by = S(self.ZONE[0]) + P["y"] * S(self.ZONE[1] - self.ZONE[0])
        k = (now - P["t_spawn"]) / 0.8                               # comes back in from the left
        if 0 <= k < 1:
            bx = -S(200) + (bx + S(200)) * (1 - (1 - k) ** 3)
        return bx, by

    def power_max(self, vals, side):
        return 4

    def update(self, vals, now):
        super().update(vals, now)
        for side, suf in (("p1", ""), ("p2", "_p2")):
            P = self.ships[side]
            if not P["in"]:
                continue
            ch = self.changed(vals, "super" + suf)
            if ch and ch[1] < ch[0] and now - P["t_dead"] > 1.2:
                self.super_shot(side, now)

    def super_shot(self, side, now):
        """The super shot: a long blast of light in front of the plane, everything in its way blows up.
        / Le super tir : un long trait de lumière devant l'avion, tout ce qui est sur son chemin saute."""
        x, y = self.pos(side, now)
        S, fx = self.S, self.fx
        self.supers += 1
        col = (255, 220, 120) if side == "p1" else (150, 220, 255)
        for i in range(5):
            fx.later(i * 0.05, fx.tracer, x + S(80), y + (i - 2) * S(10), self.W + S(100), y + (i - 2) * S(10), 3600, col, 16, 600, "front", False)
        fx.glow(x + S(90), y, 30, 160, col, 0.5, "front", 1.0, 0.0, hot=0.7)
        fx.flash(col, 0.18, 0.25)
        self.popup("SUPER SHOT !", x, max(self.S(176), y - self.S(80)), col, 38)
        for e in self.enemies:
            if not e.get("dead") and e["x"] > x and abs(e.get("yy", e["y"]) - y) < S(110):
                fx.later(0.15 + (e["x"] - x) / (3600 * self.s), self._boom, e)

    def bomb(self, side, now):
        """The bomb of Strikers: a formation of bombers flies over and everything below blows up. / Une formation de
        bombardiers passe et tout saute dessous."""
        fx, S, rng = self.fx, self.S, self.rng
        x, y = self.pos(side, now)
        self.bombs += 1
        self.raids += 1
        self.bpop[side] = now
        self.popup(tr("BOMBE !", "BOMB!"), x, max(S(176), y - S(80)), (255, 170, 80), 40)
        self.raid = (now, side)
        for i in range(14):                                             # le tapis de bombes
            bx = S(self.PANEL) + (self.W - 2 * S(self.PANEL)) * (i + rng.uniform(0.2, 0.8)) / 14
            fx.later(0.5 + i * 0.07, fx.explosion, bx, S(rng.uniform(170, 330)), rng.uniform(0.5, 0.8), False)
        fx.later(0.6, self._carpet, x + S(500), y, 0.0)
        for e in self.enemies:
            if not e.get("dead"):
                fx.later(0.6 + rng.uniform(0, 0.4), self._boom, e)
        for g in self.ground:
            if not g.get("dead") and self.gx(g) > S(self.PANEL):
                fx.later(0.7 + rng.uniform(0, 0.3), self._ground_boom, g)

    def draw_hud(self, screen, eng, vals, logo, now):
        raid = getattr(self, "raid", None)
        super().draw_hud(screen, eng, vals, logo, now)
        if raid is not None and now - raid[0] < 1.6:                    # the formation crosses the screen
            S = self.S
            img = self.img("s45_bomber", S(170), S(200), bomber_draw, flip=True)
            k = (now - raid[0]) / 1.6
            for i in range(3):
                bx = -S(260) + (self.W + S(520)) * k - i * S(150)
                by = S(160 + i * 90)
                sh = self.imgs.get("s45_bsh")
                if sh is None:
                    sh = self.imgs["s45_bsh"] = self.shadow_of(self.pg, img, 70)
                screen.blit(sh, (int(bx + S(60) - sh.get_width() / 2), int(by + S(46) - sh.get_height() / 2)))
                screen.blit(img, (int(bx - img.get_width() / 2), int(by - img.get_height() / 2)))
            self.status(screen, eng, vals, logo, now)                  # the panels stay above the formation

    def panel(self, screen, x, w):
        """A metal plate with rivets, as the panels of the game. / Une plaque de métal rivetée, comme les panneaux du jeu."""
        S, pg = self.S, self.pg
        key = ("s45_panel", int(w))
        s = self.imgs.get(key)
        if s is None:
            s = pg.Surface((int(w), self.H)).convert()
            for y in range(self.H):
                v = 70 + int(14 * math.sin(y * 0.05)) + (y * 7 % 5)
                pg.draw.line(s, (v + 34, v + 26, v + 12), (0, y), (w, y))
            pg.draw.rect(s, (40, 32, 22), s.get_rect(), max(2, S(4)))
            for yy in range(S(14), self.H, S(60)):
                for xx in (S(12), int(w) - S(12)):
                    pg.draw.circle(s, (150, 136, 110), (xx, yy), S(4))
                    pg.draw.circle(s, (60, 50, 36), (xx + 1, yy + 1), S(4), 1)
            self.imgs[key] = s
        screen.blit(s, (int(x), 0))

    def status(self, screen, eng, vals, logo, now):
        """The two panels of the game on the sides: SCORE, the planes left, BOMB, the SUPER SHOT gauge; the logo above
        the middle. / Les deux panneaux du jeu sur les côtés : SCORE, les avions, BOMB, la jauge SUPER SHOT."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        pw = S(self.PANEL)
        hd.draw_logo(screen, logo, W / 2, S(8), S(520), S(100), now)
        for side in ("p1", "p2"):
            x0 = 0 if side == "p1" else W - pw
            self.panel(screen, x0, pw)
            cx = x0 + pw / 2
            if side == "p2" and not self.p2_in(vals):                  # the right panel invites
                word, col = self.invite(vals, now)
                for i, w_ in enumerate(word.split()):
                    self.text(screen, w_, cx, S(60) + i * S(48), 40, col, key="stencil", align="center", valign="middle")
                for i, ch in enumerate("STRIKERS"):                    # the name in big embossed letters, as on the game's panel
                    y = S(146) + i * S(38)
                    self.text(screen, ch, cx + S(3), y + S(3), 46, (70, 60, 44), key="stencil", align="center", valign="middle", glow=0)
                    self.text(screen, ch, cx, y, 46, (214, 204, 182), key="stencil", align="center", valign="middle", glow=0)
                continue
            suf = "" if side == "p1" else "_p2"
            self.box(screen, x0 + S(14), S(14), pw - S(28), S(92), (60, 46, 30), fill=(30, 22, 12, 230), radius=8)
            self.text(screen, "SCORE", x0 + S(26), S(34), 26, (255, 170, 60), key="black", valign="middle", glow=0.2)
            sc = _n(vals.get("score" + suf))
            if sc is not None:
                hd._score(screen, eng, "score" + suf, x0 + pw - S(26), S(52), "right", S(44))
            lives = _n(vals.get("lives" + suf))
            if lives is not None:                                      # the plane and how many are left
                self.box(screen, x0 + S(14), S(116), pw - S(28), S(64), (60, 46, 30), fill=(30, 22, 12, 230), radius=8)
                icon = self.life_icon(side, vals)
                screen.blit(icon, (int(x0 + S(30)), S(130)))
                self.text(screen, str(int(lives)), x0 + pw - S(40), S(148), 44, (255, 170, 60), key="stencil", align="right", valign="middle")
            bombs = _n(vals.get("bombs" + suf))
            if bombs is not None:                                      # BOMB
                self.box(screen, x0 + S(14), S(190), pw - S(28), S(76), (60, 46, 30), fill=(30, 22, 12, 230), radius=8)
                self.text(screen, "BOMB", x0 + S(26), S(210), 26, (255, 170, 60), key="black", valign="middle", glow=0.2)
                bimg = self.img(("bombicon", self.BOMB), S(26), S(40), bomb_icon_draw(*self.BOMB))
                k = max(0.0, 1 - (now - self.bpop[side]) / 0.5)
                screen.blit(bimg, (int(x0 + S(40)), S(224) - int(S(6) * k)))
                self.text(screen, str(int(bombs)), x0 + pw - S(40), S(244), 44, (255, 170, 60), key="stencil", align="right", valign="middle")
            sup = _n(vals.get("super" + suf))
            if sup is not None:                                        # SUPER SHOT, a column of segments
                self.box(screen, x0 + S(14), S(276), pw - S(28), S(170), (60, 46, 30), fill=(30, 22, 12, 230), radius=8)
                self.text(screen, "SUPER", x0 + S(26), S(296), 24, (255, 170, 60), key="black", valign="middle", glow=0.2)
                self.text(screen, "SHOT", x0 + S(26), S(322), 24, (255, 170, 60), key="black", valign="middle", glow=0.2)
                n = int(_clamp(sup, 0, 8))
                for i in range(8):
                    on = i < n
                    yy = S(430) - i * S(13)
                    pg.draw.rect(screen, (255, 176, 40) if on else (70, 50, 20), (int(x0 + pw - S(90)), yy, S(56), S(9)), border_radius=S(2))
            pwr = _n(vals.get("power" + suf))
            if pwr is not None:                                        # the power of the shots, next to the super shot gauge
                self.text(screen, "POW", x0 + S(26), S(368), 20, CREAM, key="bold", valign="middle", glow=0)
                for i in range(4):
                    on = i < int(pwr)
                    pg.draw.rect(screen, (255, 210, 70) if on else (58, 46, 26), (int(x0 + S(28) + i * S(22)), S(386), S(16), S(46)), border_radius=S(3))
        plane = vals.get("plane_name")
        if isinstance(plane, str) and plane and self.p1_in(vals):
            self.label(screen, plane, W / 2, S(420), 26, GOLD, key="xbold", align="center", alpha=130)


# ============================================================================ Street Hoop
TEAM_KITS = (((70, 160, 90), (214, 50, 50)), ((70, 130, 220), (120, 84, 200)))        # P1: green vest, red shorts / P2: blue, purple
SKIN = ((236, 196, 160), (214, 160, 120), (170, 116, 80), (120, 80, 56))


def hooper_draw(shirt, shorts, skin, frame, hair):
    """A street basketball player seen from the side, facing right: a vest, long shorts, sneakers. Frames 0 run A,
    1 run B, 2 dribble, 3 shoot (arms up), 4 dunk (high up), 5 guard (arms out). / Un joueur de basket de rue de profil."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, W * 0.025)
        sk, sh_, st = skin + (255,), shirt + (255,), shorts + (255,)
        sk_d = _mix(skin, (0, 0, 0), 0.25) + (255,)
        u = H / 1.0
        cx = W * 0.5

        def P(x, y):
            return cx + x * u, y * u
        legs = {0: (((-0.06, 0.74), (-0.16, 0.97)), ((0.08, 0.72), (0.14, 0.97))), 1: (((0.06, 0.74), (0.12, 0.97)), ((-0.06, 0.72), (-0.14, 0.9))),
                2: (((-0.08, 0.75), (-0.1, 0.97)), ((0.08, 0.75), (0.1, 0.97))), 3: (((-0.04, 0.76), (-0.06, 0.97)), ((0.05, 0.76), (0.06, 0.97))),
                4: (((-0.06, 0.7), (-0.14, 0.82)), ((0.08, 0.68), (0.04, 0.84))),
                5: (((-0.1, 0.75), (-0.14, 0.97)), ((0.1, 0.75), (0.14, 0.97)))}[frame]
        hip = P(0, 0.55)
        for i, (knee, foot) in enumerate(legs):
            k, f = P(*knee), P(*foot)
            _capsule(d, hip, k, 0.075 * u, 0.06 * u, sk_d if i == 0 else sk, dark, ow)
            _capsule(d, k, f, 0.055 * u, 0.05 * u, sk_d if i == 0 else sk, dark, ow)
            d.rounded_rectangle([f[0] - 0.05 * u, f[1] - 0.045 * u, f[0] + 0.09 * u, f[1] + 0.012 * u], radius=0.02 * u, fill=(250, 250, 250, 255),
                                outline=dark, width=int(ow))
            d.line([(f[0] - 0.04 * u, f[1] - 0.005 * u), (f[0] + 0.08 * u, f[1] - 0.005 * u)], fill=(200, 60, 50, 255), width=max(1, int(ow)))
        d.polygon([P(-0.11, 0.48), P(0.11, 0.48), P(0.14, 0.72), P(0.01, 0.72), P(0.0, 0.62), P(-0.01, 0.72), P(-0.14, 0.72)], fill=st, outline=dark)
        d.polygon([P(-0.1, 0.23), P(0.1, 0.23), P(0.12, 0.5), P(-0.12, 0.5)], fill=sh_, outline=dark)                  # débardeur
        d.line([P(-0.06, 0.24), P(0.0, 0.32), P(0.07, 0.24)], fill=_mix(shirt, (0, 0, 0), 0.35) + (255,), width=max(1, int(ow)))
        d.line([P(-0.11, 0.47), P(0.11, 0.47)], fill=_mix(shirt, (255, 255, 255), 0.4) + (255,), width=max(1, int(ow * 1.4)))
        arms = {0: ((-0.12, 0.42), (0.14, 0.38)), 1: ((0.12, 0.42), (-0.12, 0.4)), 2: ((-0.1, 0.4), (0.2, 0.5)), 3: ((0.04, 0.02), (0.1, 0.0)),
                4: ((0.04, -0.02), (0.14, -0.04)), 5: ((-0.12, 0.06), (0.26, 0.2))}[frame]
        for i, hand in enumerate(arms):
            s = P(-0.08 if i == 0 else 0.08, 0.27)
            h = P(*hand)
            el = ((s[0] + h[0]) / 2 - 0.03 * u, (s[1] + h[1]) / 2 + 0.02 * u)
            _capsule(d, s, el, 0.055 * u, 0.048 * u, sk_d if i == 0 else sk, dark, ow)
            _capsule(d, el, h, 0.048 * u, 0.044 * u, sk_d if i == 0 else sk, dark, ow)
        hx, hy = P(0.02, 0.14)
        r = 0.075 * u
        d.rectangle([hx - r * 0.35, hy + r * 0.7, hx + r * 0.35, hy + r * 1.4], fill=sk_d)
        d.ellipse([hx - r, hy - r, hx + r, hy + r * 1.1], fill=sk, outline=dark, width=int(ow))
        d.polygon([(hx + r * 0.9, hy), (hx + r * 1.15, hy + r * 0.3), (hx + r * 0.9, hy + r * 0.4)], fill=sk)
        d.ellipse([hx + r * 0.3, hy - r * 0.2, hx + r * 0.55, hy + r * 0.1], fill=dark)
        if hair == 0:                                                  # casquette à l'envers
            d.chord([hx - r * 1.05, hy - r * 1.1, hx + r * 1.0, hy + r * 0.25], 180, 360, fill=(40, 40, 50, 255))
            d.rectangle([hx - r * 1.5, hy - r * 0.25, hx - r * 0.4, hy - r * 0.05], fill=(40, 40, 50, 255))
        elif hair == 1:                                                # bandeau
            d.chord([hx - r, hy - r * 1.05, hx + r, hy + r * 0.2], 180, 360, fill=(30, 24, 20, 255))
            d.rectangle([hx - r, hy - r * 0.38, hx + r, hy - r * 0.16], fill=_mix(shirt, (255, 255, 255), 0.3) + (255,))
        else:                                                          # cheveux courts clairs, en brosse
            d.chord([hx - r, hy - r * 1.2, hx + r, hy + r * 0.3], 180, 360, fill=(220, 190, 110, 255))
    return fn


def ball_draw(d, W, H):
    d.ellipse([0, 0, W - 1, H - 1], fill=(230, 110, 40, 255), outline=(60, 30, 14, 255), width=max(1, int(W * 0.06)))
    d.line([(W * 0.5, 0), (W * 0.5, H)], fill=(60, 30, 14, 255), width=max(1, int(W * 0.05)))
    d.line([(0, H * 0.5), (W, H * 0.5)], fill=(60, 30, 14, 255), width=max(1, int(W * 0.05)))
    d.arc([-W * 0.4, H * 0.1, W * 0.5, H * 0.9], -60, 60, fill=(60, 30, 14, 255), width=max(1, int(W * 0.05)))
    d.arc([W * 0.5, H * 0.1, W * 1.4, H * 0.9], 120, 240, fill=(60, 30, 14, 255), width=max(1, int(W * 0.05)))
    d.ellipse([W * 0.2, H * 0.16, W * 0.42, H * 0.34], fill=(255, 190, 140, 200))


def hoop_draw(rim, board, pole, rim_w):
    """The street hoop on the right of the court: its padded pole, the arm, the backboard seen a little from the side,
    the orange rim on the court side and its net. Positions are fractions of the picture. / Le panier de rue."""
    def fn(d, W, H):
        dark = (30, 30, 34, 255)
        steel, steel_l = (96, 108, 128, 255), (150, 160, 180, 255)
        rx, ry = rim[0] * W, rim[1] * H
        bx, btop, bbot = board[0] * W, board[1] * H, board[2] * H
        px, ptop = pole[0] * W, pole[1] * H
        rw = rim_w * W
        d.rectangle([px - W * 0.035, ptop, px + W * 0.035, H], fill=steel, outline=dark, width=max(1, int(W * 0.008)))
        d.line([(px - W * 0.015, ptop), (px - W * 0.015, H)], fill=steel_l, width=max(1, int(W * 0.01)))
        d.rectangle([px - W * 0.05, H * 0.72, px + W * 0.05, H], fill=(40, 70, 150, 255), outline=dark, width=max(1, int(W * 0.008)))
        d.line([(px, ptop + H * 0.02), (bx + W * 0.02, ptop + H * 0.02)], fill=steel, width=max(2, int(H * 0.035)))
        d.line([(px, ptop + H * 0.1), (bx + W * 0.02, ptop + H * 0.02)], fill=steel, width=max(2, int(H * 0.02)))
        bw = W * 0.08                                                  # le panneau, un peu de biais
        d.polygon([(bx - bw, btop + H * 0.03), (bx + bw * 0.3, btop), (bx + bw * 0.3, bbot - H * 0.03), (bx - bw, bbot)], fill=(244, 246, 250, 255),
                  outline=dark)
        d.polygon([(bx - bw * 0.62, btop + H * 0.17), (bx - bw * 0.05, btop + H * 0.15), (bx - bw * 0.05, bbot - H * 0.1),
                   (bx - bw * 0.62, bbot - H * 0.09)], outline=(220, 60, 40, 255))
        d.line([(bx - bw * 0.7, ry), (rx + rw / 2, ry)], fill=(240, 110, 40, 255), width=max(2, int(H * 0.012)))
        for k in range(8):                                             # le filet
            t = k / 7
            x0 = rx - rw / 2 + rw * t
            x1 = rx - rw * 0.3 + rw * 0.6 * t
            d.line([(x0, ry), (x1, ry + H * 0.17)], fill=(250, 250, 250, 230), width=max(1, int(W * 0.005)))
        for k in range(1, 4):
            yy = ry + H * 0.17 * k / 4
            half = rw / 2 - (rw * 0.2) * k / 4
            d.line([(rx - half, yy), (rx + half, yy)], fill=(250, 250, 250, 180), width=max(1, int(W * 0.004)))
        d.ellipse([rx - rw / 2, ry - H * 0.022, rx + rw / 2, ry + H * 0.022], outline=(240, 110, 40, 255), width=max(2, int(H * 0.013)))
    return fn


class StreetHoopScene(GameScene):
    """Street basketball as in the game: three against three on a half court in a park, both teams attack the hoop on
    the right. The ball goes from hand to hand, the points read in the game are baskets (shots from far for three
    points, dunks), the other team then takes the ball back. The points of both teams at the top, the clock in its
    orange box at the bottom between the two SUPER SHOT gauges, 1P above the player's man.
    / Le basket de rue comme dans le jeu : trois contre trois sur un demi-terrain, le panier à droite."""
    THEME = "hoop_park"
    STATIC = True
    SHADE = (60, 70)
    PILLS = True
    BANNERS = GameScene.BANNERS + (("SUPER SHOT !", GOLD), ("DUNK !", GOLD), ("2E MI-TEMPS", GOLD), ("2ND HALF", GOLD))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.rx, self.ry = self.W - S(HOOP_X), hoop_y(0.5, self.H, self.s) - self.size(0.5) * 1.32
        self.players = []
        for team in (0, 1):
            for i in range(3):
                self.players.append({"team": team, "x": self.W * (0.25 + 0.15 * i + 0.05 * team), "z": (0.2, 0.55, 0.85)[i] + 0.06 * team,
                                     "tx": None, "tz": None, "ph": self.rng.uniform(0, 6), "hair": (i + team) % 3, "skin": SKIN[(i * 3 + team) % 4],
                                     "left": False})
        self.attack = 0                                   # team that has the ball / l'équipe qui a la balle
        self.holder = 0
        self.ball = None                                  # a pass, a shot, a dunk or a miss in the air
        self.queue = []
        self.next = 0.0
        self.last_shot = 0.0                              # when the last shot left / dernier tir
        self.super_t = None
        self.baskets = 0                                  # baskets shown (tests)
        self.supers = 0
        self.dunks = 0
        self.misses = 0
        self.fx.sp.register("hball", draw_img(S(30), S(30), ball_draw))
        self.warm = [(self.fig, (p, f)) for p in self.players for f in range(6)] + [(self.hoop_img, ())] + self.warm

    def restart(self, vals, now):
        self.queue = []
        self.ball = None
        self.next = now + 0.8
        self.last_shot = now

    # ------------------------------------------------------------ outils
    def ground(self, z):
        """y of the court at the depth z (0 far, 1 near). / Le sol à la profondeur z."""
        return hoop_y(z, self.H, self.s)

    def size(self, z):
        return self.S(180) * (0.82 + 0.3 * z)

    def fig(self, p, frame):
        h = int(self.size(p["z"]) / 4) * 4
        kit = TEAM_KITS[p["team"]]
        return self.img(("hooper", p["team"], p["hair"], p["skin"], frame, h, p["left"]), h * 0.62, h,
                        hooper_draw(kit[0], kit[1], p["skin"], frame, p["hair"]), ss=2, flip=p["left"])

    def hoop_img(self):
        """The hoop in one picture, placed so that its rim is at (rx, ry). / Le panier, son cercle en (rx, ry)."""
        S = self.S
        x0, x1 = self.rx - S(80), self.W - S(10)
        y0, y1 = self.ry - S(130), self.ground(0.42)
        w, h = x1 - x0, y1 - y0
        fn = hoop_draw(((self.rx - x0) / w, (self.ry - y0) / h), ((self.rx + S(80) - x0) / w, S(10) / h, S(160) / h),
                       ((self.W - S(56) - x0) / w, S(20) / h), S(96) / w)
        return self.img("hoop", w, h, fn), (x0, y0)

    def depth_order(self):
        return sorted(range(len(self.players)), key=lambda i: self.players[i]["z"])

    # ------------------------------------------------------------ ce qui arrive
    def update(self, vals, now):
        for name, team in (("points", 0), ("points_p2", 1)):
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0]:
                self.queue.append((team, int(ch[1] - ch[0])))
        for name, team in (("super", 0), ("super_p2", 1)):
            ch = self.changed(vals, name)
            if ch and ch[1] < ch[0] - 20:                              # the full gauge is spent: a super shot
                self.super_t = (now, team)
        ch = self.changed(vals, "half")
        if ch and ch[1] > ch[0]:
            self.slam(tr("2E MI-TEMPS", "2ND HALF"), GOLD, now, 1.8)
        if self.ball is None and now >= self.next:
            if self.queue:
                team, pts = self.queue.pop(0)
                self.shoot(team, pts, now)
            elif now - self.last_shot > 7.0:                                # nobody scores: a shot off the rim
                self.shoot(self.attack, 0, now)
            else:                                                      # in between, the ball goes from hand to hand
                self.next = now + self.rng.uniform(0.8, 1.6)
                mates = [i for i, p in enumerate(self.players) if p["team"] == self.attack and i != self.holder]
                if mates and self.rng.random() < 0.75:
                    self.ball = {"kind": "pass", "t0": now, "dur": 0.35, "from": self.holder, "to": self.rng.choice(mates)}
        self.move_players(now)

    def shoot(self, team, pts, now):
        """A basket for the team: from beyond the line for 3 points, a dunk or a jump shot for 2, or a shot that misses.
        / Un panier pour l'équipe : de loin pour 3 points, un smash ou un tir pour 2, ou un tir raté."""
        S = self.S
        if team != self.attack:                                        # a steal first
            self.attack = team
            self.holder = min((i for i, p in enumerate(self.players) if p["team"] == team),
                              key=lambda i: abs(self.players[i]["x"] - self.W * 0.5))
        p = self.players[self.holder]
        dunk = pts == 2 and self.rng.random() < 0.55
        if dunk:                                                       # runs to the rim and flies
            p["tx"], p["tz"] = self.rx - S(70), 0.5
            self.ball = {"kind": "dunk", "t0": now + 0.75, "dur": 0.5, "team": team, "pts": pts}
        else:
            far = S(740) if pts >= 3 else S(self.rng.uniform(300, 480))
            p["tx"] = self.rx - far
            p["tz"] = self.rng.uniform(0.25, 0.8)
            self.ball = {"kind": "shot" if pts else "miss", "t0": now + 0.7, "dur": 0.95 if pts >= 3 else 0.8, "team": team, "pts": pts}
        self.next = now + 2.6
        self.last_shot = now

    def scored(self, b):
        now, S, fx = self.fx.now, self.S, self.fx
        rx, ry = self.rx, self.ry
        if b["kind"] == "miss":                                        # off the rim, someone takes the rebound
            self.misses += 1
            fx.sparks(rx, ry, 8, (255, 200, 120), (120, 300), (200, 340), (0.2, 0.4), 600, "front", 2, 14)
            self.popup(tr("RATÉ", "MISSED"), rx - S(60), ry - S(30), CREAM, 34)
            reb = self.rng.choice(range(len(self.players)))
            self.ball = {"kind": "pass", "t0": now, "dur": 0.5, "from": None, "to": reb, "x0": rx, "y0": ry}
            self.attack = self.players[reb]["team"]
            return
        self.baskets += 1
        fx.sparks(rx, ry + S(30), 26, (255, 230, 150), (200, 600), (30, 150), (0.3, 0.6), 600, "front", 3, 22)
        st = self.super_t
        if st is not None and now - st[0] < 5.0 and st[1] == b["team"]:
            self.supers += 1
            self.popup("SUPER SHOT !", rx - S(260), ry + S(10), GOLD, 64, 1.6, 50, "stencil")
            fx.explosion(rx, ry + S(10), 0.7, False)
            fx.shake(8, 0.4)
            self.super_t = None
        elif b["kind"] == "dunk":
            self.dunks += 1
            self.popup("DUNK !", rx - S(220), ry + S(10), GOLD, 64, 1.4, 50, "stencil")
            fx.shake(6, 0.3)
        else:
            self.popup(f"{b['pts']} POINTS" if b["pts"] > 1 else "1 POINT", rx - S(80), ry - S(40), GOLD, 44, key="stencil")
        self.attack = 1 - b["team"]                                    # the other team takes the ball back at the top
        self.holder = min((i for i, p in enumerate(self.players) if p["team"] == self.attack), key=lambda i: self.players[i]["x"])
        self.ball = {"kind": "pass", "t0": now + 0.2, "dur": 0.5, "from": None, "to": self.holder, "x0": rx, "y0": ry + S(60)}
        for i, p in enumerate(self.players):                           # everybody walks back out
            p["tx"] = None

    def move_players(self, now):
        S, dt, rng = self.S, self.dt, self.rng
        b = self.ball
        for i, p in enumerate(self.players):
            busy = b is not None and b["kind"] in ("shot", "dunk", "miss") and i == self.holder
            if not busy and (p["tx"] is None or (abs(p["tx"] - p["x"]) < S(6) and rng.random() < dt * 0.8)):
                if p["team"] == self.attack:                           # attackers around the line, the holder drives
                    p["tx"] = self.rx - rng.uniform(S(240), S(1250))
                    p["tz"] = rng.uniform(0.1, 0.95)
                else:                                                  # defenders between their man and the hoop
                    mates = [q for q in self.players if q["team"] == self.attack]
                    man = mates[(i % 3) % len(mates)]
                    p["tx"] = _lerp(man["x"], self.rx, 0.22) + rng.uniform(-S(20), S(20))
                    p["tz"] = _clamp(man["z"] + rng.uniform(-0.08, 0.08), 0.05, 1.0)
            step = S(360) * dt
            dx = p["tx"] - p["x"]
            dz = (p["tz"] if p["tz"] is not None else p["z"]) - p["z"]
            p["moving"] = abs(dx) > S(6) or abs(dz) > 0.02
            if p["moving"]:
                p["x"] += max(-step, min(step, dx))
                p["z"] += max(-dt * 0.9, min(dt * 0.9, dz))
                if abs(dx) > S(6):
                    p["left"] = dx < 0
            if p["team"] != self.attack and not p["moving"]:
                p["left"] = False if p["x"] < self.players[self.holder]["x"] else True
        if b is not None and now >= b["t0"] + b["dur"]:
            if b["kind"] in ("shot", "dunk", "miss"):
                self.ball = None
                self.scored(b)
            elif b["kind"] == "pass":
                self.holder = b["to"]
                self.ball = None

    # ------------------------------------------------------------ dessin
    def hand(self, i):
        p = self.players[i]
        h = self.size(p["z"])
        return p["x"] + (-h * 0.14 if p["left"] else h * 0.14), self.ground(p["z"]) - h * 0.5

    def ball_xy(self, b, now):
        """Where the ball in the air is. / Où est la balle en l'air."""
        S = self.S
        k = _clamp((now - b["t0"]) / b["dur"])
        if b["kind"] == "pass":
            x0, y0 = (b["x0"], b["y0"]) if b.get("from") is None else self.hand(b["from"])
            x1, y1 = self.hand(b["to"])
            return _lerp(x0, x1, k), _lerp(y0, y1, k) - math.sin(k * math.pi) * S(50)
        p = self.players[self.holder]
        h = self.size(p["z"])
        x0, y0 = p["x"], self.ground(p["z"]) - h * (1.05 if b["kind"] != "dunk" else 1.6)
        if b["kind"] == "dunk":
            return _lerp(x0 + S(30), self.rx, k), _lerp(y0, self.ry - S(10), k) - math.sin(k * math.pi) * S(30)
        arc = S(170 + 90 * (b["pts"] >= 3))
        return _lerp(x0, self.rx, k), _lerp(y0, self.ry - S(6), k) - math.sin(k * math.pi) * arc

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        hoop, (hx0, hy0) = self.hoop_img()
        screen.blit(hoop, (int(hx0), int(hy0)))
        sh = self.imgs.get("hsh")
        if sh is None:
            sh = self.imgs["hsh"] = pg.Surface((S(84), S(18)), pg.SRCALPHA)
            pg.draw.ellipse(sh, (0, 0, 0, 90), sh.get_rect())
        b = self.ball
        me = self.holder if self.attack == 0 else min((i for i, p in enumerate(self.players) if p["team"] == 0),
                                                      key=lambda i: abs(self.players[i]["x"] - self.players[self.holder]["x"]))
        for i in self.depth_order():
            p = self.players[i]
            y = self.ground(p["z"])
            screen.blit(sh, (int(p["x"] - sh.get_width() / 2), int(y - sh.get_height() / 2)))
            frame, lift = 0, 0.0
            if b is not None and b["kind"] in ("shot", "dunk", "miss") and i == self.holder and now >= b["t0"] - 0.3:
                k = _clamp((now - (b["t0"] - 0.3)) / (0.6 if b["kind"] == "dunk" else 0.5))
                frame = 4 if b["kind"] == "dunk" else 3
                lift = math.sin(k * math.pi) * S(150 if b["kind"] == "dunk" else 50)
            elif i == self.holder and b is None:
                frame = 2 if not p.get("moving") or int(now * 6) % 3 else 0
            elif p.get("moving"):
                frame = int(now * 8 + p["ph"]) % 2
            elif p["team"] != self.attack:
                frame = 5
            img = self.fig(p, frame)
            screen.blit(img, (int(p["x"] - img.get_width() / 2), int(y - img.get_height() - lift)))
            if i == me and self.p1_in(vals):                           # 1P above the player's man, as in the game
                tag = self.img("tag1p", S(56), S(44), tag_draw)
                ty = y - img.get_height() - lift - S(48) + S(4) * math.sin(now * 6)
                screen.blit(tag, (int(p["x"] - tag.get_width() / 2), int(ty)))
                self.text(screen, "1P", p["x"], ty + S(15), 22, WHITE, key="black", align="center", valign="middle", glow=0)
            if i == self.holder and b is None:                         # the ball bounces at his side
                hx, hy = self.hand(i)
                gy = y - S(10)
                self.draw_ball(screen, hx, gy - abs(math.sin(now * 7 + p["ph"])) * (gy - hy))
        if b is not None and now >= b["t0"]:
            x, y = self.ball_xy(b, now)
            st = self.super_t
            if b["kind"] in ("shot", "dunk") and st is not None and st[1] == b["team"]:      # a super shot: the ball burns
                g = self.fx.sp.glow(S(56), (255, 140, 40), 10, hot=0.6)
                screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
                if int(now * 50) % 2 == 0:
                    self.fx.sparks(x, y, 3, (255, 170, 60), (40, 120), (0, 360), (0.2, 0.4), 0, "front", 3, 10)
            self.draw_ball(screen, x, y)
        self.status(screen, eng, vals, logo, now)

    def draw_ball(self, screen, x, y):
        img = self.fx.sp.obj("hball", 0)
        if img is not None:
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the points of both teams in big letters at the top on each side of the logo, red on the left
        and blue on the right, the clock in its orange box at the bottom between the two SUPER SHOT gauges.
        / Comme dans le jeu : les points des deux équipes en haut, l'horloge en bas entre les deux jauges SUPER SHOT."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(92), now)
        a, b = _n(vals.get("points")), _n(vals.get("points_p2"))
        right = "P2" if self.p2_in(vals) else "CPU"
        for txt, pts, x, align, col in (("P1", a, W / 2 - S(250), "right", (255, 80, 60)), (right, b, W / 2 + S(250), "left", (90, 140, 255))):
            w = hd.text(f"{txt} 00", "stencil", S(60), WHITE)["w"]
            self.pill(screen, x - w - S(26) if align == "right" else x - S(26), S(10), w + S(52), S(80), 150)
            num = f"{int(pts):02d}" if pts is not None else "--"
            if align == "right":
                nw = self.text(screen, num, x, S(50), 60, WHITE, key="stencil", align="right", valign="middle")
                self.text(screen, txt, x - nw - S(16), S(50), 60, col, key="stencil", align="right", valign="middle")
            else:
                nw = self.text(screen, num, x, S(50), 60, WHITE, key="stencil", valign="middle")
                self.text(screen, txt, x + nw + S(16), S(50), 60, col, key="stencil", valign="middle")
        if not self.p2_in(vals):                                       # under the right team, as in the game
            word, col = self.invite(vals, now)
            self.label(screen, word, W / 2 + S(410), S(118), 30, col, align="center")
        m, sec = _n(vals.get("time_min")), _n(vals.get("time_sec"))
        if m is not None and sec is not None:                          # the clock, m:ss, in its orange box
            self.box(screen, W / 2 - S(88), H - S(80), S(176), S(70), (250, 150, 40), fill=(16, 10, 6, 235), radius=6, width=4)
            hd.put_number(screen, f"{int(m)}:{int(sec):02d}", "stencil", S(54), (255, 176, 60), W / 2, H - S(45), "center", "middle")
        for name, x0, dd in (("super", W / 2 - S(130), -1), ("super_p2", W / 2 + S(130), 1)):
            v = _n(vals.get(name))
            if v is None:
                continue
            gw = S(330)
            x = x0 - gw if dd < 0 else x0
            self.pill(screen, x - S(14), H - S(82), gw + S(28), S(74), 160, radius=10)
            self.text(screen, "SUPER", x + (gw - S(4) if dd < 0 else S(4)), H - S(66), 22, CREAM, key="black", align="right" if dd < 0 else "left",
                      valign="middle", glow=0)
            self.text(screen, "SHOT", x + (gw - S(4) if dd < 0 else S(4)), H - S(42), 22, CREAM, key="black", align="right" if dd < 0 else "left",
                      valign="middle", glow=0)
            frac = _clamp(v / 192.0)
            full = frac >= 1.0
            bx = x if dd < 0 else x + S(96)
            bw = gw - S(96)
            pg.draw.rect(screen, (34, 24, 16), (int(bx), H - S(66), int(bw), S(34)), border_radius=S(3))
            n = int(frac * 14)
            col = _mix((255, 200, 60), WHITE, 0.5 + 0.5 * math.sin(now * 12)) if full else (255, 140, 30)
            seg = (bw - S(8)) / 14
            for i in range(n):                                         # fills toward the clock, as in the game
                xx = bx + bw - S(4) - (i + 1) * seg if dd < 0 else bx + S(4) + i * seg
                pg.draw.rect(screen, col, (int(xx), H - S(62), max(1, int(seg - S(3))), S(26)))


def tag_draw(d, W, H):
    """The red 1P tag with its arrow, above the player's man. / L'étiquette rouge 1P et sa flèche."""
    d.rounded_rectangle([W * 0.06, 0, W * 0.94, H * 0.66], radius=H * 0.16, fill=(230, 40, 40, 255), outline=(255, 255, 255, 255), width=max(1, int(W * 0.05)))
    d.polygon([(W * 0.36, H * 0.62), (W * 0.64, H * 0.62), (W * 0.5, H * 0.98)], fill=(230, 40, 40, 255))


# ============================================================================ Super Dodge Ball
DODGE_TEAMS = (                                     # (shirt, trousers, accent) of each team / maillot, pantalon, liseré
    ((236, 236, 240), (40, 46, 90), (220, 50, 40)),
    ((60, 150, 80), (230, 222, 200), (250, 210, 60)),
)
DODGE_LOOKS = ((0, (236, 196, 160), (30, 26, 30), 1.0), (1, (214, 160, 120), (120, 70, 30), 1.25), (2, (236, 196, 160), (240, 210, 120), 0.95),
               (3, (200, 150, 110), (20, 20, 24), 1.0), (4, (236, 196, 160), (60, 40, 30), 1.1), (0, (170, 116, 80), (30, 26, 30), 1.2))
HP_COLS = ((60, 220, 255), (255, 220, 40), (60, 220, 80))             # the three players' colours on the bars / couleurs des barres


def dodger_draw(shirt, pants, accent, skin, hair_col, style, build, frame):
    """A dodgeball player seen from the side, facing right, a big head on a short body: a sports shirt, trousers or
    shorts, sneakers. style: 0 spiky hair, 1 flat top, 2 shaved with a headband, 3 ponytail, 4 hair over the eyes.
    Frames 0 stand, 1 and 2 run, 3 arm back, 4 throw, 5 catch, 6 hit, 7 down. / Un joueur de balle aux prisonniers."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, H * 0.012)
        sk, sk_d = skin + (255,), _mix(skin, (0, 0, 0), 0.22) + (255,)
        sh, sh_d = shirt + (255,), _mix(shirt, (0, 0, 0), 0.2) + (255,)
        pt, pt_d = pants + (255,), _mix(pants, (0, 0, 0), 0.25) + (255,)
        acc = accent + (255,)
        u = H
        bw = build
        if frame == 7:                                                 # down, lying on the ground
            y = H * 0.9
            _capsule(d, (W * 0.3, y), (W * 0.62, y - H * 0.02), H * 0.09 * bw, H * 0.09 * bw, sh, dark, ow)
            _capsule(d, (W * 0.62, y), (W * 0.92, y + H * 0.02), H * 0.06, H * 0.05, pt, dark, ow)
            d.ellipse([W * 0.04, y - H * 0.16, W * 0.3, y + H * 0.08], fill=sk, outline=dark, width=int(ow))
            d.chord([W * 0.04, y - H * 0.16, W * 0.3, y + H * 0.08], 90, 270, fill=hair_col + (255,))
            d.line([(W * 0.17, y - H * 0.06), (W * 0.21, y - H * 0.02)], fill=dark, width=int(ow * 2))
            d.line([(W * 0.21, y - H * 0.06), (W * 0.17, y - H * 0.02)], fill=dark, width=int(ow * 2))
            return
        cx = W * 0.5
        lean = {6: -0.08, 3: -0.03, 4: 0.06}.get(frame, 0.0)

        def P(x, y):
            return cx + (x + lean * (0.62 - y) / 0.62) * u, y * u
        hip = P(0, 0.64)
        legs = {0: ((-0.06, 0.8, -0.08, 0.97), (0.06, 0.8, 0.08, 0.97)), 1: ((-0.1, 0.79, -0.16, 0.95), (0.1, 0.78, 0.14, 0.97)),
                2: ((0.06, 0.8, 0.04, 0.97), (-0.04, 0.78, -0.12, 0.9)), 3: ((-0.1, 0.8, -0.16, 0.97), (0.08, 0.8, 0.12, 0.97)),
                4: ((-0.12, 0.79, -0.2, 0.95), (0.1, 0.8, 0.16, 0.97)), 5: ((-0.08, 0.8, -0.12, 0.97), (0.08, 0.8, 0.12, 0.97)),
                6: ((-0.1, 0.8, -0.16, 0.97), (0.04, 0.8, 0.0, 0.97))}[frame]
        for i, (kx, ky, fx_, fy_) in enumerate(legs):
            k, f = P(kx, ky), (cx + fx_ * u, fy_ * u)
            _capsule(d, hip, k, 0.07 * u * bw, 0.06 * u, pt_d if i == 0 else pt, dark, ow)
            _capsule(d, k, f, 0.055 * u, 0.05 * u, pt_d if i == 0 else pt, dark, ow)
            d.rounded_rectangle([f[0] - 0.05 * u, f[1] - 0.04 * u, f[0] + 0.08 * u, f[1] + 0.015 * u], radius=0.02 * u, fill=(246, 246, 246, 255),
                                outline=dark, width=int(ow))
        sw = 0.15 * bw
        d.polygon([P(-sw, 0.42), P(sw, 0.42), P(sw * 1.05, 0.66), P(-sw * 1.05, 0.66)], fill=sh, outline=dark)          # maillot
        d.line([P(-sw * 1.02, 0.6), P(sw * 1.02, 0.6)], fill=acc, width=max(1, int(u * 0.022)))
        d.polygon([P(-sw * 0.3, 0.42), P(sw * 0.3, 0.42), P(0, 0.48)], fill=acc)
        hands = {0: ((-0.14, 0.62), (0.16, 0.6)), 1: ((0.16, 0.56), (-0.14, 0.58)), 2: ((-0.14, 0.56), (0.16, 0.58)),
                 3: ((-0.12, 0.6), (-0.3, 0.36)), 4: ((-0.16, 0.58), (0.36, 0.44)), 5: ((0.26, 0.5), (0.28, 0.58)),
                 6: ((-0.2, 0.36), (0.2, 0.34))}[frame]
        for i, hand in enumerate(hands):
            s = P(-sw * 0.8 if i == 0 else sw * 0.8, 0.45)
            h = (cx + hand[0] * u, hand[1] * u)
            el = ((s[0] + h[0]) / 2 - 0.02 * u, (s[1] + h[1]) / 2 + 0.03 * u)
            _capsule(d, s, el, 0.055 * u * bw, 0.05 * u, sh_d if i == 0 else sh, dark, ow)
            _capsule(d, el, h, 0.045 * u, 0.042 * u, sk_d if i == 0 else sk, dark, ow)
            d.ellipse([h[0] - 0.045 * u, h[1] - 0.045 * u, h[0] + 0.045 * u, h[1] + 0.045 * u], fill=sk_d if i == 0 else sk, outline=dark,
                      width=int(ow))
        hx, hy = P(0.03, 0.24)                                         # la grosse tête
        r = 0.17 * u
        d.ellipse([hx - r, hy - r, hx + r, hy + r * 1.05], fill=sk, outline=dark, width=int(ow * 1.4))
        d.ellipse([hx + r * 0.62, hy + r * 0.02, hx + r * 1.08, hy + r * 0.4], fill=sk, outline=dark, width=int(ow))     # nez
        d.ellipse([hx + r * 0.66, hy + r * 0.08, hx + r * 1.02, hy + r * 0.36], fill=sk)
        ex, ey = hx + r * 0.44, hy - r * 0.12                          # œil, sourcil, bouche
        if frame == 6:
            d.line([(ex - r * 0.14, ey - r * 0.12), (ex + r * 0.14, ey + r * 0.12)], fill=dark, width=int(ow * 2.4))
            d.line([(ex - r * 0.14, ey + r * 0.12), (ex + r * 0.14, ey - r * 0.12)], fill=dark, width=int(ow * 2.4))
            d.ellipse([hx + r * 0.36, hy + r * 0.5, hx + r * 0.66, hy + r * 0.82], fill=(120, 30, 30, 255), outline=dark)
        else:
            d.ellipse([ex - r * 0.16, ey - r * 0.2, ex + r * 0.16, ey + r * 0.2], fill=(255, 255, 255, 255), outline=dark, width=int(ow))
            d.ellipse([ex + r * 0.0, ey - r * 0.1, ex + r * 0.14, ey + r * 0.12], fill=dark)
            d.line([(ex - r * 0.2, ey - r * 0.34), (ex + r * 0.22, ey - r * 0.2)], fill=dark, width=int(ow * 2.4))
            d.line([(hx + r * 0.4, hy + r * 0.62), (hx + r * 0.7, hy + r * 0.58)], fill=dark, width=int(ow * 1.8))
        d.ellipse([hx - r * 0.3, hy + r * 0.0, hx - r * 0.06, hy + r * 0.34], fill=sk_d, outline=dark, width=int(ow))   # oreille
        hc = hair_col + (255,)
        if style == 0:                                                 # cheveux en pointes
            pts = [(hx - r * 1.05, hy + r * 0.1), (hx - r * 1.35, hy - r * 0.3), (hx - r * 0.85, hy - r * 0.6), (hx - r * 1.0, hy - r * 1.15),
                   (hx - r * 0.35, hy - r * 0.95), (hx - r * 0.2, hy - r * 1.4), (hx + r * 0.25, hy - r * 1.0), (hx + r * 0.6, hy - r * 1.25),
                   (hx + r * 0.7, hy - r * 0.75), (hx + r * 1.05, hy - r * 0.62), (hx + r * 0.75, hy - r * 0.38), (hx - r * 0.2, hy - r * 0.45),
                   (hx - r * 0.45, hy + r * 0.05)]
            d.polygon(pts, fill=hc, outline=dark)
        elif style == 1:                                               # brosse plate
            d.rounded_rectangle([hx - r * 1.0, hy - r * 1.35, hx + r * 0.9, hy - r * 0.4], radius=r * 0.2, fill=hc, outline=dark, width=int(ow))
            d.polygon([(hx - r * 1.0, hy - r * 0.6), (hx - r * 1.0, hy + r * 0.2), (hx - r * 0.5, hy - r * 0.4)], fill=hc)
        elif style == 2:                                               # crâne rasé et bandeau
            d.chord([hx - r, hy - r, hx + r, hy + r * 1.05], 180, 360, fill=_mix(hair_col, skin, 0.7) + (255,))
            d.polygon([(hx - r * 0.98, hy - r * 0.42), (hx + r * 0.96, hy - r * 0.52), (hx + r * 0.98, hy - r * 0.3), (hx - r, hy - r * 0.18)],
                      fill=acc, outline=dark)
            d.polygon([(hx - r * 0.98, hy - r * 0.3), (hx - r * 1.5, hy - r * 0.1), (hx - r * 1.4, hy + r * 0.1)], fill=acc, outline=dark)
        elif style == 3:                                               # queue de cheval
            d.chord([hx - r * 1.04, hy - r * 1.08, hx + r * 0.96, hy + r * 0.4], 160, 360, fill=hc, outline=dark)
            d.ellipse([hx - r * 1.6, hy - r * 0.7, hx - r * 0.8, hy + r * 0.6], fill=hc, outline=dark, width=int(ow))
            d.ellipse([hx - r * 1.0, hy - r * 0.62, hx - r * 0.74, hy - r * 0.3], fill=acc)
        else:                                                          # mèche sur les yeux
            d.chord([hx - r * 1.04, hy - r * 1.1, hx + r * 1.0, hy + r * 0.3], 150, 360, fill=hc, outline=dark)
            d.polygon([(hx + r * 0.2, hy - r * 0.6), (hx + r * 1.0, hy - r * 0.4), (hx + r * 0.7, hy - r * 0.05), (hx + r * 0.4, hy - r * 0.3)],
                      fill=hc, outline=dark)
    return fn


def dodgeball_draw(d, W, H):
    """The volleyball-like ball of dodgeball: white with coloured panels. / Le ballon, blanc à panneaux de couleur."""
    d.ellipse([0, 0, W - 1, H - 1], fill=(246, 246, 240, 255), outline=(40, 40, 50, 255), width=max(1, int(W * 0.06)))
    d.chord([0, 0, W - 1, H - 1], 200, 300, fill=(250, 200, 40, 255))
    d.chord([0, 0, W - 1, H - 1], 20, 120, fill=(50, 90, 200, 255))
    d.arc([W * 0.15, -H * 0.3, W * 1.3, H * 0.9], 100, 200, fill=(40, 40, 50, 255), width=max(1, int(W * 0.05)))
    d.arc([-W * 0.3, H * 0.1, W * 0.85, H * 1.3], 280, 20, fill=(40, 40, 50, 255), width=max(1, int(W * 0.05)))
    d.ellipse([W * 0.22, H * 0.16, W * 0.42, H * 0.32], fill=(255, 255, 255, 220))


class DodgeBallScene(GameScene):
    """Super Dodge Ball as in the game: two teams of three on a cobbled lot, the ball flies from one side to the
    other. When a player's health goes down in the game, he takes the ball full in the face and falls, at zero he is
    out; the full POW gauge that empties is a power shot on fire. At the top, the health bars of both teams in three
    colours with the names, TIME in the middle; POW at the bottom. / La balle aux prisonniers comme dans le jeu."""
    THEME = "dodge_yard"
    STATIC = True
    SHADE = (90, 60)
    PILLS = True
    EXPLOSIONS = True
    POW_MAX = 0x8FFF
    BANNERS = GameScene.BANNERS + (("POWER SHOT !", GOLD), ("OUT !", GOLD))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.players = []
        for team in (0, 1):
            for i in range(3):
                look = DODGE_LOOKS[team * 3 + i]
                self.players.append({"team": team, "slot": i, "style": look[0], "skin": look[1], "hair": look[2], "build": look[3],
                                     "x": 0.0, "z": (0.2, 0.55, 0.88)[i], "tx": None, "tz": None, "ph": self.rng.uniform(0, 6),
                                     "out": False, "hurt": -99.0, "anim": None})
                self.home(self.players[-1])
        self.ball = None                                  # the ball in the air / la balle en l'air
        self.holder = 0
        self.queue = []                                   # hits to show / coups à montrer
        self.next = 0.0
        self.power_t = None
        self.hits = 0                                     # hits shown (tests)
        self.outs = 0
        self.powers = 0
        self.fx.sp.register("dball", draw_img(self.S(34), self.S(34), dodgeball_draw))
        self.warm = [(self.fig, (p, f)) for p in self.players for f in range(8)] + self.warm

    def home(self, p):
        """A spot on the player's own half. / Une place dans sa moitié de terrain."""
        W, S = self.W, self.S
        lo, hi = (W * 0.08, W * 0.44) if p["team"] == 0 else (W * 0.56, W * 0.92)
        p["x"] = p["x"] or self.rng.uniform(lo, hi)
        p["tx"] = self.rng.uniform(lo + S(40), hi - S(40))
        p["tz"] = _clamp(p["z"] + self.rng.uniform(-0.15, 0.15), 0.05, 0.98)

    def restart(self, vals, now):
        self.queue = []
        self.ball = None
        self.next = now + 0.8
        for p in self.players:
            p["out"] = False

    def ground(self, z):
        return dodge_y(z, self.H, self.s)

    def size(self, p):
        return self.S(196) * (0.8 + 0.32 * p["z"]) * (1 + 0.12 * (p["build"] - 1))

    def fig(self, p, frame):
        h = int(self.size(p) / 4) * 4
        kit = DODGE_TEAMS[p["team"]]
        return self.img(("dodger", p["team"], p["slot"], frame, h), h * 0.9, h,
                        dodger_draw(kit[0], kit[1], kit[2], p["skin"], p["hair"], p["style"], p["build"], frame), ss=2, flip=p["team"] == 1)

    def hand(self, i):
        p = self.players[i]
        h = self.size(p)
        return p["x"] + h * (0.2 if p["team"] == 0 else -0.2), self.ground(p["z"]) - h * 0.52

    # ------------------------------------------------------------ ce qui arrive
    def update(self, vals, now):
        for team, suf in ((0, ""), (1, "_p2")):
            for k in range(3):
                ch = self.changed(vals, f"hp{k + 1}{suf}")
                i = team * 3 + k
                if ch and ch[1] < ch[0]:                               # hit: the ball comes from the other side
                    self.queue.append((i, ch[1] <= 0))
                elif ch and ch[1] > ch[0] and self.players[i]["out"]:  # back for a new round
                    self.players[i]["out"] = False
                    self.players[i]["x"] = 0.0
                    self.home(self.players[i])
            ch = self.changed(vals, "power" + suf)
            if ch and ch[0] >= self.POW_MAX * 0.9 and ch[1] < ch[0] * 0.5:
                self.power_t = (now, team)
        if self.ball is None and now >= self.next:
            if self.queue:
                target, out = self.queue.pop(0)
                self.throw(target, now, hit=True, out=out)
            else:                                                      # in between, the ball crosses and is caught
                alive = [i for i, p in enumerate(self.players) if not p["out"] and p["team"] != self.players[self.holder]["team"]]
                if alive:
                    self.throw(self.rng.choice(alive), now, hit=False)
        self.move_players(now)

    def throw(self, target, now, hit, out=False):
        """The holder (or a player of the other team) throws at the target. / Le lanceur vise la cible."""
        team = 1 - self.players[target]["team"]
        if self.players[self.holder]["team"] != team or self.players[self.holder]["out"]:
            mates = [i for i, p in enumerate(self.players) if p["team"] == team and not p["out"]] or [i for i, p in enumerate(self.players)
                                                                                                    if p["team"] == team]
            self.holder = self.rng.choice(mates)
        st = self.power_t
        power = st is not None and st[1] == team and now - st[0] < 4.0
        self.ball = {"t0": now + 0.45, "dur": 0.32 if not power else 0.55, "from": self.holder, "to": target, "hit": hit or power,
                     "out": out, "power": power}
        self.players[self.holder]["anim"] = (now, "throw")
        if power:
            self.power_t = None
            self.powers += 1
            self.slam("POWER SHOT !", GOLD, now + 0.3, 1.2)
        self.next = now + (1.5 if hit else self.rng.uniform(1.0, 1.8))

    def landed(self, b, now):
        S, fx = self.S, self.fx
        p = self.players[b["to"]]
        x, y = self.hand(b["to"])
        if b["hit"]:                                                   # full in the face
            self.hits += 1
            p["hurt"] = now
            p["anim"] = (now, "hit")
            fx.sparks(x, y - S(30), 20, (255, 240, 180), (300, 800), (0, 360), (0.2, 0.5), 400, "front", 3, 20)
            fx.glow(x, y - S(30), 20, 120, (255, 240, 200), 0.3, "front", 1.0, 0.0)
            fx.shake(7 if b["power"] else 4, 0.3)
            if b["power"]:
                fx.explosion(x, y - S(20), 0.8, False)
            p["tx"] = p["x"] + (-S(90) if p["team"] == 0 else S(90))  # knocked back
            if b["out"]:
                p["out"] = True
                self.outs += 1
                self.popup("OUT !", p["x"], y - self.size(p), GOLD, 46, 1.4, 60, "stencil")
            mates = [i for i, q in enumerate(self.players) if q["team"] == p["team"] and not q["out"]]
            self.holder = self.rng.choice(mates) if mates else b["to"]  # the ball rolls to a mate
        else:                                                          # caught
            p["anim"] = (now, "catch")
            self.holder = b["to"]

    def move_players(self, now):
        S, dt = self.S, self.dt
        for i, p in enumerate(self.players):
            if p["out"]:
                continue
            if p["tx"] is None or (abs(p["tx"] - p["x"]) < S(6) and self.rng.random() < dt * 0.6):
                self.home(p)
            step = S(300) * dt * (2.0 if now - p["hurt"] < 0.4 else 1.0)
            dx = p["tx"] - p["x"]
            dz = p["tz"] - p["z"]
            p["moving"] = abs(dx) > S(6) or abs(dz) > 0.02
            if p["moving"]:
                p["x"] += max(-step, min(step, dx))
                p["z"] += max(-dt * 0.8, min(dt * 0.8, dz))
        b = self.ball
        if b is not None and now >= b["t0"] + b["dur"]:
            self.ball = None
            self.landed(b, now)

    # ------------------------------------------------------------ dessin
    def frame_of(self, i, now):
        p = self.players[i]
        if p["out"] and now - p["hurt"] > 0.5:
            return 7
        a = p.get("anim")
        if a is not None:
            k = now - a[0]
            if a[1] == "throw" and k < 0.75:
                return 3 if k < 0.42 else 4
            if a[1] == "hit" and k < 0.7:
                return 6
            if a[1] == "catch" and k < 0.4:
                return 5
        b = self.ball
        if b is not None and i == b["to"] and now > b["t0"] and not b["hit"]:
            return 5
        if p.get("moving"):
            return 1 + int(now * 8 + p["ph"]) % 2
        return 0

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        sh = self.imgs.get("dsh")
        if sh is None:
            sh = self.imgs["dsh"] = pg.Surface((S(90), S(20)), pg.SRCALPHA)
            pg.draw.ellipse(sh, (0, 0, 0, 100), sh.get_rect())
        b = self.ball
        for i in sorted(range(len(self.players)), key=lambda j: self.players[j]["z"]):
            p = self.players[i]
            y = self.ground(p["z"])
            frame = self.frame_of(i, now)
            if frame == 7 and int(now * 8) % 2 and now - p["hurt"] > 2.0:     # an out player blinks
                continue
            screen.blit(sh, (int(p["x"] - sh.get_width() / 2), int(y - sh.get_height() / 2)))
            img = self.fig(p, frame)
            jump = 0.0
            screen.blit(img, (int(p["x"] - img.get_width() / 2), int(y - img.get_height() - jump)))
            if i == self.holder and b is None and not p["out"]:          # the ball in his hands
                hx, hy = self.hand(i)
                self.draw_ball(screen, hx, hy - S(10), now, False)
        if b is not None:
            x0, y0 = self.hand(b["from"])
            x1, y1 = self.hand(b["to"])
            y1 -= self.size(self.players[b["to"]]) * (0.28 if b["hit"] else 0.0)
            if now < b["t0"]:                                          # wound up behind the thrower
                self.draw_ball(screen, x0 + (-S(40) if self.players[b["from"]]["team"] == 0 else S(40)), y0 - S(40), now, b["power"])
            else:
                k = _clamp((now - b["t0"]) / b["dur"])
                x, y = _lerp(x0, x1, k), _lerp(y0, y1, k) - math.sin(k * math.pi) * S(30 if b["hit"] else 70)
                if b["power"]:                                         # a power shot zigzags on fire
                    y += math.sin(k * 18) * S(26)
                self.draw_ball(screen, x, y, now, b["power"])
        self.status(screen, eng, vals, logo, now)

    def draw_ball(self, screen, x, y, now, burning):
        S, pg = self.S, self.pg
        if burning:
            g = self.fx.sp.glow(S(60), (255, 120, 40), 10, hot=0.6)
            screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            if int(now * 50) % 2 == 0:
                self.fx.sparks(x, y, 3, (255, 160, 60), (40, 160), (0, 360), (0.2, 0.4), 0, "front", 3, 10)
        img = self.fx.sp.obj("dball", (now * 900) % 360, 24)
        screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))

    def status(self, screen, eng, vals, logo, now):
        """As in the game: at the top the health bars of both teams, three colours for the three players, their names
        below, TIME in the middle under the logo; the POW gauges at the bottom.
        / Comme dans le jeu : les barres de vie des deux équipes en haut, TIME au milieu, les jauges POW en bas."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(78), now)
        bw = S(700)
        for team, suf, x0 in ((0, "", S(20)), (1, "_p2", W - S(20) - bw)):
            vals_hp = [_n(vals.get(f"hp{k + 1}{suf}")) for k in range(3)]
            if all(v is None for v in vals_hp):
                continue
            self.pill(screen, x0 - S(10), S(4), bw + S(20), S(100), 160, radius=12)
            tag = ("1P" if team == 0 else ("2P" if self.p2_in(vals) else "CPU"))
            self.text(screen, tag, x0 + (S(4) if team == 0 else bw - S(4)), S(26), 30, (255, 90, 70) if team == 0 else (90, 150, 255), key="black",
                      align="left" if team == 0 else "right", valign="middle", glow=0.3)
            seg = (bw - S(12)) / 3
            for k in range(3):                                         # three players, three colours
                v = vals_hp[k] if vals_hp[k] is not None else 0
                kk = k if team == 0 else 2 - k
                sx = x0 + S(6) + kk * seg
                pg.draw.rect(screen, (20, 20, 30), (int(sx), S(46), int(seg - S(4)), S(22)))
                frac = _clamp(v / 255.0)
                if frac > 0:
                    fw = int((seg - S(8)) * frac)
                    fx0 = sx + S(2) if team == 0 else sx + seg - S(6) - fw
                    pg.draw.rect(screen, HP_COLS[k], (int(fx0), S(48), fw, S(18)))
                    pg.draw.rect(screen, _mix(HP_COLS[k], WHITE, 0.5), (int(fx0), S(49), fw, S(4)))
                name = vals.get(f"name{k + 1}{suf}")
                if isinstance(name, str) and name:
                    self.text(screen, name, sx + (seg - S(4)) / 2, S(86), 22, CREAM if v > 0 else (130, 120, 110), key="black", align="center",
                              valign="middle", glow=0.2)
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(380), S(132), 30, col, align="center")
        t = _n(vals.get("time"))
        if t is not None:                                              # TIME under the logo, big numbers
            self.pill(screen, W / 2 - S(130), S(84), S(260), S(72), 170, radius=12)
            self.text(screen, "TIME", W / 2 - S(24), S(120), 30, (255, 220, 80), key="black", align="right", valign="middle")
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(66), (120, 230, 90) if t > 10 else RED, W / 2 - S(8), S(120), "left", "middle")
        for team, suf, x0 in ((0, "", S(24)), (1, "_p2", W - S(24) - S(360))):
            v = _n(vals.get("power" + suf))
            if v is None:
                continue
            self.pill(screen, x0 - S(10), H - S(54), S(380), S(46), 160, radius=10)
            self.text(screen, "POW", x0 + (S(4) if team == 0 else S(356)), H - S(31), 30, (255, 170, 40), key="stencil",
                      align="left" if team == 0 else "right", valign="middle")
            gx = x0 + (S(90) if team == 0 else S(4))
            frac = _clamp(v / float(self.POW_MAX))
            full = frac >= 0.99
            pg.draw.rect(screen, (40, 28, 14), (int(gx), H - S(42), S(260), S(22)), border_radius=S(4))
            if frac > 0:
                col = _mix((255, 210, 60), WHITE, 0.5 + 0.5 * math.sin(now * 12)) if full else (255, 150, 30)
                fw = int(S(256) * frac)
                pg.draw.rect(screen, col, (int(gx + S(2) if team == 0 else gx + S(258) - fw), H - S(40), fw, S(18)), border_radius=S(3))


# ============================================================================ Neo Bomberman
NB_WORLDS = ("nb_ruins", "nb_water", "nb_factory", "nb_castle")
NB_BOTS = (((255, 140, 40), (255, 220, 60)), ((60, 140, 255), (120, 230, 255)))       # body, visor of each player's robot


def miner_draw(body, visor, frame):
    """A little miner robot of our own, seen from above at three quarters: a square body, a yellow hard hat with its
    lamp, a glowing visor, short legs. Frames 0 stand, 1 and 2 walk, 3 hit. / Un petit robot mineur à nous."""
    def fn(d, W, H):
        dark = (24, 22, 30, 255)
        ow = max(1.0, W * 0.035)
        b, bd = body + (255,), _mix(body, (0, 0, 0), 0.3) + (255,)
        step = {0: (0, 0), 1: (-0.06, 0.04), 2: (0.06, -0.04), 3: (0, 0)}[frame]
        for i, dy in enumerate(step):                                  # pieds
            x = W * (0.32 + 0.36 * i)
            d.rounded_rectangle([x - W * 0.12, H * (0.84 + dy), x + W * 0.12, H * (0.98 + dy)], radius=W * 0.05, fill=(50, 50, 60, 255),
                                outline=dark, width=int(ow))
        d.rounded_rectangle([W * 0.16, H * 0.48, W * 0.84, H * 0.88], radius=W * 0.1, fill=b, outline=dark, width=int(ow))      # corps
        d.rounded_rectangle([W * 0.3, H * 0.58, W * 0.7, H * 0.78], radius=W * 0.05, fill=bd)
        d.ellipse([W * 0.44, H * 0.62, W * 0.56, H * 0.74], fill=(255, 80, 60, 255) if frame != 3 else (255, 255, 255, 255))
        for sx in (0.12, 0.88):                                        # bras
            d.ellipse([W * (sx - 0.09), H * 0.58, W * (sx + 0.09), H * 0.76], fill=bd, outline=dark, width=int(ow))
        d.rounded_rectangle([W * 0.14, H * 0.16, W * 0.86, H * 0.54], radius=W * 0.16, fill=(236, 236, 240, 255), outline=dark, width=int(ow))
        d.rounded_rectangle([W * 0.22, H * 0.3, W * 0.78, H * 0.46], radius=W * 0.06, fill=(20, 30, 40, 255))      # la visière
        glow = visor if frame != 3 else (255, 255, 255)
        d.rounded_rectangle([W * 0.27, H * 0.33, W * 0.47, H * 0.43], radius=W * 0.03, fill=glow + (255,))
        d.rounded_rectangle([W * 0.53, H * 0.33, W * 0.73, H * 0.43], radius=W * 0.03, fill=glow + (255,))
        d.chord([W * 0.1, H * 0.02, W * 0.9, H * 0.36], 180, 360, fill=(250, 200, 40, 255), outline=dark, width=int(ow))     # le casque
        d.rectangle([W * 0.06, H * 0.17, W * 0.94, H * 0.22], fill=(230, 170, 30, 255), outline=dark, width=int(ow))
        d.ellipse([W * 0.4, H * 0.04, W * 0.6, H * 0.18], fill=(255, 250, 200, 255), outline=dark, width=int(ow))         # la lampe
    return fn


def nb_bomb_draw(d, W, H):
    """A round black bomb with its fuse. / Une bombe ronde et sa mèche."""
    d.ellipse([W * 0.08, H * 0.2, W * 0.92, H * 0.98], fill=(30, 30, 44, 255), outline=(10, 10, 16, 255), width=max(1, int(W * 0.04)))
    d.ellipse([W * 0.24, H * 0.32, W * 0.44, H * 0.5], fill=(150, 150, 190, 255))
    d.rectangle([W * 0.42, H * 0.1, W * 0.58, H * 0.26], fill=(80, 80, 96, 255))
    d.line([(W * 0.5, H * 0.12), (W * 0.62, H * 0.02)], fill=(200, 170, 120, 255), width=max(1, int(W * 0.05)))


def crate_draw(color):
    """A breakable block seen from above at three quarters: a wooden crate, a bush or a barrel depending on the world.
    / Un bloc qui casse, vu de haut : caisse, buisson ou tonneau selon le monde."""
    def fn(d, W, H):
        dark = (30, 22, 16, 255)
        c, cd, cl = color + (255,), _mix(color, (0, 0, 0), 0.32) + (255,), _mix(color, (255, 255, 255), 0.3) + (255,)
        d.rectangle([0, H * 0.3, W - 1, H - 1], fill=cd, outline=dark, width=max(1, int(W * 0.04)))
        d.rectangle([0, 0, W - 1, H * 0.34], fill=c, outline=dark, width=max(1, int(W * 0.04)))
        for k in (0.33, 0.66):
            d.line([(W * k, H * 0.34), (W * k, H)], fill=dark, width=max(1, int(W * 0.03)))
        d.line([(W * 0.08, H * 0.08), (W * 0.92, H * 0.26)], fill=cl, width=max(1, int(W * 0.05)))
        d.line([(W * 0.08, H * 0.26), (W * 0.92, H * 0.08)], fill=cl, width=max(1, int(W * 0.05)))
    return fn


def blob_draw(color):
    """A wandering blob of the maze with big eyes. / Une boule errante du labyrinthe, aux grands yeux."""
    def fn(d, W, H):
        dark = (20, 20, 30, 255)
        d.ellipse([W * 0.06, H * 0.14, W * 0.94, H * 0.98], fill=color + (255,), outline=dark, width=max(1, int(W * 0.05)))
        d.ellipse([W * 0.2, H * 0.24, W * 0.42, H * 0.38], fill=_mix(color, (255, 255, 255), 0.5) + (255,))
        for x in (0.36, 0.62):
            d.ellipse([W * (x - 0.1), H * 0.4, W * (x + 0.1), H * 0.66], fill=(255, 255, 255, 255), outline=dark, width=max(1, int(W * 0.03)))
            d.ellipse([W * (x - 0.04), H * 0.48, W * (x + 0.05), H * 0.62], fill=dark)
    return fn


CRATES = {"nb_ruins": (176, 120, 70), "nb_water": (90, 170, 120), "nb_factory": (170, 120, 60), "nb_castle": (140, 90, 70)}


class NeoBombermanScene(GameScene):
    """Neo Bomberman as in the game, with robots of our own: the maze seen from above, its stone pillars and the blocks
    that break, the players' robots walk the corridors and drop bombs whose flames run in a cross. The bombs read in
    the game are dropped and blow up, the fire and the speed go up with the items, a life lost is a robot caught in
    the blast. At the top, as in the game, a coloured band with the lives and the stage. / Le labyrinthe vu de haut."""
    THEME = "nb_ruins"
    STATIC = True
    SHADE = (0, 0)
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS + tuple((f"STAGE {w}-{s}", GOLD) for w in range(1, 5) for s in range(1, 9))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.gx0, self.gy0, self.T = nb_grid(self.W, self.H, self.s)
        self.hard = {(c, r) for c in range(1, NB_COLS, 2) for r in range(1, NB_ROWS, 2)}
        self.soft = set()
        self.bombs = []                                   # {c, r, t0, owner, fire}
        self.flames = []                                  # {cells, t0}
        self.bots = {side: {"c": 0.0 if side == "p1" else float(NB_COLS - 1), "r": 0.0 if side == "p1" else float(NB_ROWS - 1),
                            "path": [], "in": False, "dead": -99.0, "spawn": -99.0, "next_bomb": 0.0, "walk": 0.0}
                     for side in ("p1", "p2")}
        self.blobs = []
        self.world = 0
        self.dropped = 0                                  # bombs shown (tests)
        self.blasts = 0
        self.fx.sp.register("nbomb", draw_img(S(46), S(46), nb_bomb_draw))
        self.warm = [(self.bot_img, (side, f)) for side in ("p1", "p2") for f in range(4)] + self.warm
        self.bd.prebuild([n for n in NB_WORLDS if n != self.THEME])     # the other worlds get ready in the background
        self.fill_soft(0.34)

    # ------------------------------------------------------------ la grille
    def cell_xy(self, c, r):
        """Middle of a cell on the screen. / Milieu d'une case à l'écran."""
        return self.gx0 + (c + 0.5) * self.T, self.gy0 + (r + 0.5) * self.T

    def free(self, c, r, bombs=True):
        if not (0 <= c < NB_COLS and 0 <= r < NB_ROWS) or (c, r) in self.hard or (c, r) in self.soft:
            return False
        return not (bombs and any(b["c"] == c and b["r"] == r for b in self.bombs))

    def near_bot(self, c, r, d=3):
        return any(abs(B["c"] - c) + abs(B["r"] - r) <= d for B in self.bots.values())

    def fill_soft(self, density, limit=None):
        cells = [(c, r) for c in range(NB_COLS) for r in range(NB_ROWS) if (c, r) not in self.hard and (c, r) not in self.soft
                 and not self.near_bot(c, r)]
        self.rng.shuffle(cells)
        n = int(len(cells) * density) if limit is None else min(limit, len(cells))
        for cell in cells[:n]:
            self.soft.add(cell)

    def bot_img(self, side, frame):
        S = self.S
        body, visor = NB_BOTS[0 if side == "p1" else 1]
        return self.img(("miner", side, frame), S(58), S(64), miner_draw(body, visor, frame), ss=2)

    def restart(self, vals, now):
        self.bombs, self.flames = [], []
        for side, B in self.bots.items():
            B["in"] = False

    def always(self, vals, now):
        w = _n(vals.get("world"))
        if w is not None:                                              # one look per world, as in the game
            name = NB_WORLDS[(int(w) - 1) % len(NB_WORLDS)]
            if name != self.bd.theme and self.bd.warm(name):
                self.bd.set_theme(name, now)
                self.soft = set()
                self.fill_soft(0.34)

    # ------------------------------------------------------------ ce qui arrive
    def update(self, vals, now):
        S, fx = self.S, self.fx
        for side, suf in (("p1", ""), ("p2", "_p2")):
            B = self.bots[side]
            playing = self.p1_in(vals) if side == "p1" else self.p2_in(vals)
            if not playing:
                B["in"] = False
                continue
            if not B["in"]:
                B["in"], B["spawn"] = True, now
                B["c"], B["r"] = (0.0, 0.0) if side == "p1" else (float(NB_COLS - 1), float(NB_ROWS - 1))
                B["path"] = []
            alive = now - B["dead"] > 1.4
            ch = self.changed(vals, "lives" + suf)
            if ch and ch[1] < ch[0] and alive:                         # caught in a blast
                x, y = self.cell_xy(B["c"], B["r"])
                fx.explosion(x, y - S(10), 0.7, False)
                self.popup(tr("-1 VIE", "-1 LIFE"), x, y - S(60), (255, 90, 70), 34)
                B["dead"] = now
                B["spawn"] = now + 1.4
            elif ch and ch[1] > ch[0]:
                x, y = self.cell_xy(B["c"], B["r"])
                self.popup("1UP !", x, y - S(60), (140, 255, 150), 36)
            for name, label, col in (("fire", "FIRE UP", (255, 140, 40)), ("speed", "SPEED UP", (90, 200, 255))):
                ch = self.changed(vals, name + suf)
                if ch and ch[1] > ch[0] and alive:
                    x, y = self.cell_xy(B["c"], B["r"])
                    self.popup(label, x, y - S(60), col, 34)
                    fx.sparks(x, y, 16, col, (150, 400), (0, 360), (0.3, 0.6), 0, "front", 3, 18)
            ch = self.changed(vals, "bombs" + suf)
            if ch and ch[1] > ch[0] and alive:                         # a bomb dropped in the game
                self.drop(side, vals, now)
            elif ch and ch[1] < ch[0]:                                  # a bomb of the game blew up
                mine = [b for b in self.bombs if b["owner"] == side]
                if mine:
                    self.blast(min(mine, key=lambda b: b["t0"]), now)
            if alive and now >= B["next_bomb"] and _n(vals.get("bombs" + suf)) is None:
                self.drop(side, vals, now)                             # without the value, the robots play by themselves
            if alive and now >= B["spawn"]:
                self.walk(B, now)
        for name in ("stage",):
            ch = self.changed(vals, name)
            if ch:
                w = int(_n(vals.get("world")) or 1)
                self.slam(f"STAGE {w}-{int(ch[1])}", GOLD, now, 1.6)
                self.soft = set()
                self.fill_soft(0.34)
        for b in list(self.bombs):                                     # a bomb blows up after its time
            if now - b["t0"] > 2.4:
                self.blast(b, now)
        self.flames = [f for f in self.flames if now - f["t0"] < 0.55]
        if len(self.soft) < 40 and self.rng.random() < self.dt * 1.5:  # blocks come back
            self.fill_soft(0.0, 1)
        self.move_blobs(now)

    def drop(self, side, vals, now):
        B = self.bots[side]
        c, r = int(round(B["c"])), int(round(B["r"]))
        B["next_bomb"] = now + self.rng.uniform(2.6, 4.2)
        if any(b["c"] == c and b["r"] == r for b in self.bombs):
            return
        suf = "" if side == "p1" else "_p2"
        fire = int(_n(vals.get("fire" + suf)) or 2)
        self.bombs.append({"c": c, "r": r, "t0": now, "owner": side, "fire": max(1, min(6, fire))})
        self.dropped += 1
        B["path"] = self.escape(c, r, max(1, min(6, fire)))

    def danger(self, c, r, fire):
        cells = {(c, r)}
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for k in range(1, fire + 1):
                cc, rr = c + dc * k, r + dr * k
                if not (0 <= cc < NB_COLS and 0 <= rr < NB_ROWS) or (cc, rr) in self.hard:
                    break
                cells.add((cc, rr))
                if (cc, rr) in self.soft:
                    break
        return cells

    def escape(self, c, r, fire):
        """A short way out of the cross of the bomb just dropped. / Un court chemin hors de la croix de la bombe."""
        bad = self.danger(c, r, fire)
        prev = {(c, r): None}
        todo = [(c, r)]
        while todo:
            cur = todo.pop(0)
            if cur not in bad:
                path = []
                while cur != (c, r):
                    path.append(cur)
                    cur = prev[cur]
                return path[::-1]
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (cur[0] + dc, cur[1] + dr)
                if nxt not in prev and self.free(*nxt) and len(prev) < 200:
                    prev[nxt] = cur
                    todo.append(nxt)
        return []

    def route(self, c, r):
        """A way to a cell further off, next to a block to break if possible. / Un chemin vers une case plus loin."""
        prev = {(c, r): None}
        todo = [(c, r)]
        while todo and len(prev) < 260:
            cur = todo.pop(0)
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (cur[0] + dc, cur[1] + dr)
                if nxt not in prev and self.free(*nxt):
                    prev[nxt] = cur
                    todo.append(nxt)
        cells = [k for k in prev if k != (c, r)]
        if not cells:
            return []
        near = [k for k in cells if any((k[0] + dc, k[1] + dr) in self.soft for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        goal = self.rng.choice(near if near and self.rng.random() < 0.7 else cells)
        path = []
        while goal != (c, r):
            path.append(goal)
            goal = prev[goal]
        return path[::-1][:12]

    def walk(self, B, now):
        """Along the corridors, one cell at a time. / Dans les couloirs, case par case."""
        dt = self.dt
        if not B["path"]:
            B["path"] = self.route(int(round(B["c"])), int(round(B["r"])))
            if not B["path"]:
                return
        tc, tr = B["path"][0]
        if not self.free(tc, tr) and (tc, tr) != (int(round(B["c"])), int(round(B["r"]))):
            B["path"] = []                                             # a block or a bomb in the way
            return
        speed = 3.2 * dt
        dc, dr = tc - B["c"], tr - B["r"]
        if abs(dc) + abs(dr) <= speed:
            B["c"], B["r"] = float(tc), float(tr)
            B["path"].pop(0)
        else:
            B["c"] += max(-speed, min(speed, dc))
            B["r"] += max(-speed, min(speed, dr))
        B["walk"] += dt

    def blast(self, b, now):
        """The flames run in a cross, blocks break, blobs caught in them pop. / Les flammes partent en croix."""
        if b not in self.bombs:
            return
        self.bombs.remove(b)
        self.blasts += 1
        cells = self.danger(b["c"], b["r"], b["fire"])
        for cell in cells:
            if cell in self.soft:
                self.soft.discard(cell)
                x, y = self.cell_xy(*cell)
                self.fx.small_blast(x, y, 0.8, "front")
        self.flames.append({"cells": cells, "t0": now, "c": b["c"], "r": b["r"]})
        x, y = self.cell_xy(b["c"], b["r"])
        self.fx.glow(x, y, 30, 140, (255, 200, 120), 0.35, "front", 1.0, 0.0)
        self.fx.shake(4, 0.2)
        for other in list(self.bombs):                                 # chain reaction
            if (other["c"], other["r"]) in cells:
                self.fx.later(0.08, self.blast, other, now)
        for e in self.blobs:
            if (int(round(e["c"])), int(round(e["r"]))) in cells and not e.get("dead"):
                e["dead"] = now
                ex, ey = self.cell_xy(e["c"], e["r"])
                self.popup("100", ex, ey - self.S(30), CREAM, 28)

    def move_blobs(self, now):
        dt, rng = self.dt, self.rng
        self.blobs = [e for e in self.blobs if not e.get("dead") or now - e["dead"] < 0.6]
        if len([e for e in self.blobs if not e.get("dead")]) < 4 and rng.random() < dt * 0.5:
            cells = [(c, r) for c in range(NB_COLS) for r in range(NB_ROWS) if self.free(c, r) and not self.near_bot(c, r, 6)]
            if cells:
                c, r = rng.choice(cells)
                self.blobs.append({"c": float(c), "r": float(r), "to": None, "col": rng.choice(((90, 150, 255), (255, 120, 160), (120, 220, 120))),
                                   "ph": rng.uniform(0, 6)})
        for e in self.blobs:
            if e.get("dead"):
                continue
            if e["to"] is None:
                c, r = int(round(e["c"])), int(round(e["r"]))
                opts = [(c + dc, r + dr) for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)) if self.free(c + dc, r + dr)]
                e["to"] = rng.choice(opts) if opts else (c, r)
            tc, tr = e["to"]
            sp = 1.6 * dt
            dc, dr = tc - e["c"], tr - e["r"]
            if abs(dc) + abs(dr) <= sp:
                e["c"], e["r"], e["to"] = float(tc), float(tr), None
            else:
                e["c"] += max(-sp, min(sp, dc))
                e["r"] += max(-sp, min(sp, dr))

    # ------------------------------------------------------------ dessin
    def draw_hud(self, screen, eng, vals, logo, now):
        S, T, pg = self.S, self.T, self.pg
        add = pg.BLEND_RGB_ADD
        crate = self.img(("crate", self.bd.theme), T, T * 1.12, crate_draw(CRATES.get(self.bd.theme, (176, 120, 70))))
        items = []
        for c, r in self.soft:
            x, y = self.cell_xy(c, r)
            items.append((y, 0, crate, x - T / 2, y + T / 2 - crate.get_height()))
        bomb = self.fx.sp.obj("nbomb", 0)
        for b in self.bombs:
            x, y = self.cell_xy(b["c"], b["r"])
            k = 1 + 0.12 * math.sin((now - b["t0"]) * (8 + 10 * (now - b["t0"])))
            img = pg.transform.smoothscale(bomb, (int(bomb.get_width() * k), int(bomb.get_height() * k))) if abs(k - 1) > 0.02 else bomb
            items.append((y, 1, img, x - img.get_width() / 2, y + T * 0.42 - img.get_height()))
        for e in self.blobs:
            x, y = self.cell_xy(e["c"], e["r"])
            img = self.img(("blob", e["col"]), S(44), S(42), blob_draw(e["col"]))
            hop = abs(math.sin(now * 5 + e["ph"])) * S(6)
            if e.get("dead"):
                if int(now * 20) % 2:
                    continue
            items.append((y, 2, img, x - img.get_width() / 2, y + T * 0.42 - img.get_height() - hop))
        for side, B in self.bots.items():
            if not B["in"] or now < B["spawn"] and now - B["dead"] > 0.5:
                continue
            if now < B["spawn"]:                                       # caught: it blinks white
                frame = 3
            else:
                frame = 0 if not B["path"] else 1 + int(B["walk"] * 7) % 2
                if now - B["spawn"] < 1.5 and int(now * 14) % 2:
                    continue
            x, y = self.cell_xy(B["c"], B["r"])
            img = self.bot_img(side, frame)
            items.append((y + 1, 3, img, x - img.get_width() / 2, y + T * 0.46 - img.get_height()))
        sh = self.imgs.get("nbsh")
        if sh is None:
            sh = self.imgs["nbsh"] = pg.Surface((int(T * 0.8), int(T * 0.3)), pg.SRCALPHA)
            pg.draw.ellipse(sh, (0, 0, 0, 80), sh.get_rect())
        for y, kind, img, x, top in sorted(items, key=lambda it: (it[0], it[1])):
            if kind >= 1:
                screen.blit(sh, (int(x + img.get_width() / 2 - sh.get_width() / 2), int(y + T * 0.42 - sh.get_height() / 2)))
            screen.blit(img, (int(x), int(top)))
            if kind == 1:                                              # the fuse burns
                g = self.fx.sp.glow(S(10) + S(3) * math.sin(now * 30), (255, 200, 80), 9, hot=0.8)
                screen.blit(g, (int(x + img.get_width() * 0.62 - g.get_width() / 2), int(top - g.get_height() / 2)), special_flags=add)
        for f in self.flames:                                          # the cross of flames
            k = (now - f["t0"]) / 0.55
            for c, r in f["cells"]:
                x, y = self.cell_xy(c, r)
                g = self.fx.sp.glow(T * (0.62 - 0.2 * k), (255, 150, 50), 12 * (1 - k) + 2, hot=0.7)
                screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=add)
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: a coloured band at the top, the robot's head and the lives of each player, the stage, the
        bombs and the fire. / Comme dans le jeu : une bande de couleur en haut, les vies, le stage, les bombes, le feu."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        band = self.imgs.get("nbband")
        if band is None:
            band = self.imgs["nbband"] = pg.Surface((W, S(72)), pg.SRCALPHA)
            for y in range(S(72)):
                k = y / S(72)
                pg.draw.line(band, _mix((255, 150, 40), (200, 90, 20), k) + (235,), (0, y), (W, y))
            pg.draw.line(band, (90, 40, 10, 255), (0, S(70)), (W, S(70)), S(3))
        screen.blit(band, (0, 0))
        hd.draw_logo(screen, logo, W / 2, S(4), S(360), S(64), now)
        for side, suf, x0 in (("p1", "", S(20)), ("p2", "_p2", W / 2 + S(220))):
            if side == "p2" and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, W - S(200), S(36), 32, col, align="center")
                continue
            self.box(screen, x0, S(8), S(600) if side == "p1" else S(600), S(56), (90, 40, 10), fill=(30, 16, 8, 220), radius=10)
            self.text(screen, "1P" if side == "p1" else "2P", x0 + S(14), S(36), 30, WHITE, key="black", valign="middle")
            head = self.bot_img(side, 0)
            screen.blit(pg.transform.smoothscale(head, (S(40), S(45))), (int(x0 + S(66)), S(12)))
            lives = _n(vals.get("lives" + suf))
            if lives is not None:
                self.text(screen, str(int(lives)), x0 + S(118), S(36), 34, (255, 230, 120), key="stencil", valign="middle")
            sc = _n(vals.get("score" + suf))
            if sc is not None:
                hd._score(screen, eng, "score" + suf, x0 + S(330), S(14), "right", S(44))
            fire = _n(vals.get("fire" + suf))
            if fire is not None:                                       # the fire, as flames
                for i in range(min(6, int(fire))):
                    g = self.fx.sp.glow(S(14), (255, 150, 50), 11, hot=0.8)
                    screen.blit(g, (int(x0 + S(360) + i * S(22) - g.get_width() / 2), int(S(36) - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            stg, wld = _n(vals.get("stage")), _n(vals.get("world"))
            if side == "p1" and stg is not None and wld is not None:
                self.text(screen, f"{int(wld)}-{int(stg)}", x0 + S(560), S(36), 30, (255, 230, 120), key="stencil", align="right", valign="middle")


# ============================================================================ Twinkle Star Sprites
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


class TwinkleScene(GameScene):
    """Twinkle Star Sprites as in the game: two fields side by side, each with a forest seen from above that scrolls
    down, separated by the ornate column; in each one a little witch of our own shoots the puffballs that come down.
    Chains of puffballs send fireballs to the other field, the attacks read in the game (level 1, 2 and boss) cross
    over, a heart lost makes the witch spin, a bomb clears her field. At the top the name and the hearts, at the
    bottom Pow 1 2 Max and the bombs. / Deux terrains côte à côte, comme dans le jeu."""
    THEME = "ts_frame"
    STATIC = True
    SHADE = (60, 60)
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS + (("KO CHANCE !", GOLD),)
    ATTACKS = {1: "LV1", 2: "LV2", 3: "BOSS"}

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.fields = ts_fields(self.W, self.s)
        self.tile = None                                  # the forest, built in the background / la forêt, préparée à côté
        self.tile_img = None
        threading.Thread(target=self._build_tile, daemon=True).start()
        self.scroll = 0.0
        self.side = {side: {"x": 0.5, "tx": 0.5, "next": 0.0, "hit": -99.0, "fire": 0.0, "enemies": [], "balls": [], "boss": None,
                            "next_row": 0.0, "chain": 0, "bomb": -99.0} for side in ("p1", "p2")}
        self.attacks = 0                                  # attacks sent (tests)
        self.bombs = 0
        self.hits = 0
        self.fx.sp.register("tsball", draw_img(S(34), S(34), lambda d, W, H: (d.ellipse([0, 0, W - 1, H - 1], fill=(255, 140, 40, 255)),
                                                                              d.ellipse([W * 0.2, H * 0.2, W * 0.6, H * 0.6], fill=(255, 230, 140, 255)))))
        self.warm = [(self.witch, ("p1", 0, f)) for f in range(2)] + [(self.witch, ("p2", 0, f)) for f in range(2)] + self.warm

    def _build_tile(self):
        try:
            w = max(f[1] for f in self.fields)
            self.tile_img = ts_forest_tile(w, self.H, self.s)
        except Exception:
            self.tile_img = None

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

    def fxy(self, side, fx_, fy_):
        """A point of a field, from fractions of its width and of the height. / Un point d'un terrain."""
        x0, w = self.fields[0 if side == "p1" else 1]
        return x0 + fx_ * w, fy_ * self.H

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
            if ch and ch[1] < ch[0]:                                   # a heart lost
                st["hit"] = now
                self.hits += 1
                x, y = self.fxy(side, st["x"], 0.82)
                self.fx.sparks(x, y, 20, (255, 120, 160), (200, 500), (0, 360), (0.3, 0.7), 0, "front", 3, 20)
                self.popup("-1", x, y - S(70), (255, 110, 150), 36)
            ch = self.changed(vals, "bombs" + suf)
            if ch and ch[1] < ch[0]:                                   # a bomb clears the field
                self.bomb(side, now)
            ch = self.changed(vals, "attack" + suf)
            if ch and ch[1] > 0:
                lvl = max(1, min(3, int(ch[1]) // 16))
                self.send(side, other, lvl, now)
            ch = self.changed(vals, "power" + suf)
            if ch and ch[1] < ch[0] and ch[0] >= 0x1000:               # a charged shot leaves
                x, y = self.fxy(side, st["x"], 0.78)
                self.fx.tracer(x, y - S(40), x, S(-60), 2600, (255, 230, 140), 22, 300, "front", False)
                self.fx.glow(x, y - S(40), 30, 140, (255, 230, 140), 0.4, "front", 1.0, 0.0)
                for e in st["enemies"]:
                    x0, w = self.fields[0 if side == "p1" else 1]
                    if abs(x0 + e["x"] * w - x) < S(80) and not e.get("dead"):
                        e["dead"] = now
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

    def pop(self, side, e, now):
        """A puffball pops; the ones of the same row follow in a chain. / Une boule éclate, sa rangée suit en chaîne."""
        st = self.side[side]
        n = 0
        for f in st["enemies"]:
            if not f.get("dead") and f["col"] == e["col"] and abs(f["y"] - e["y"]) < 0.08:
                f["dead"] = now + 0.08 * n
                n += 1
        st["chain"] += n
        x0, w = self.fields[0 if side == "p1" else 1]
        if n >= 3:
            self.popup(f"{n} HIT", x0 + e["x"] * w, max(self.S(170), e["y"] * self.H), GOLD, 34, 1.0, 40, "stencil")

    def send(self, side, other, lvl, now):
        """Fireballs (or the big boss creature) go over to the other field. / Des boules de feu passent de l'autre côté."""
        so = self.side[other]
        if lvl >= 3:                                                   # boss attack
            so["boss"] = {"t0": now + 0.3, "x": self.rng.uniform(0.3, 0.7)}
            self.attacks += 1
            self.popup("BOSS ATTACK !", *self.fxy(other, 0.5, 0.42), (255, 120, 200), 48, 1.6, 40, "stencil")
            return
        n = (1, 2, 4)[lvl] if lvl else 2
        for i in range(n):
            so["balls"].append({"x": self.rng.uniform(0.1, 0.9), "y": -0.08 - 0.1 * i, "vx": self.rng.uniform(-0.15, 0.15),
                                "v": self.rng.uniform(0.35, 0.5) * (1.3 if lvl == 2 else 1.0)})
        if lvl:
            self.attacks += 1
            self.popup(f"LV{lvl} ATTACK", *self.fxy(other, 0.5, 0.38), (255, 170, 80), 40, 1.3, 40, "stencil")
        x, y = self.fxy(side, 1.0 if side == "p1" else 0.0, 0.3)          # the fire crosses the column
        x1, y1 = self.fxy(other, 0.0 if side == "p1" else 1.0, 0.1)
        self.fx.tracer(x, y, x1, y1, 1800, (255, 160, 60), 10, 120, "front", False)

    def bomb(self, side, now):
        st = self.side[side]
        self.bombs += 1
        st["bomb"] = now
        x, y = self.fxy(side, 0.5, 0.5)
        x0, w = self.fields[0 if side == "p1" else 1]
        for i in range(12):
            a = i / 12 * math.tau
            self.fx.later(0.03 * i, self.fx.glow, x + math.cos(a) * w * 0.3, y + math.sin(a) * self.H * 0.3, 20, 110, (255, 240, 180), 0.5, "front",
                          1.0, 0.0)
        self.fx.flash((255, 250, 220), 0.18, 0.3)
        for e in st["enemies"]:
            e["dead"] = e.get("dead") or now
        st["balls"] = []
        self.popup("BOMB !", x, y - self.S(60), (255, 240, 160), 48)

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
            screen.set_clip(None)
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
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        look = self.look(vals, side)
        hit = now - st["hit"] < 1.0
        if not (hit and int(now * 16) % 2):
            img = self.witch(side, look, int(now * 6) % 2)
            if hit:
                img = self.rotated(("witchspin", look), img, (now - st["hit"]) * 720, 15)
            x, y = self.fxy(side, st["x"], 0.82)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))

    def status(self, screen, eng, vals, logo, now):
        """As in the game: at the top of each field the score, the name and the hearts, at the bottom Pow 1 2 Max and
        the bombs; the logo above the column. / Comme dans le jeu : score, nom, cœurs en haut, Pow et bombes en bas."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(4), S(380), S(76), now)
        for k, (side, suf) in enumerate((("p1", ""), ("p2", "_p2"))):
            x0, w = self.fields[k]
            right = k == 1
            ax = x0 + w - S(16) if right else x0 + S(16)
            al = "right" if right else "left"
            if right and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, ax, S(30), 30, col, align=al)
            else:
                sc = _n(vals.get("score" + suf))
                tag = "2P" if right else "1P"
                self.pill(screen, (ax - S(330)) if right else ax - S(8), S(6), S(338), S(50), 150)
                self.text(screen, tag, ax - S(300) if right else ax, S(31), 30, (255, 220, 90), key="black", valign="middle")
                if sc is not None:
                    hd._score(screen, eng, "score" + suf, ax if right else ax + S(300), S(10), "right", S(40))
            name = vals.get("name" + suf)
            hearts = _n(vals.get("lives" + suf))
            row_y = S(74)
            if isinstance(name, str) and name:
                self.text(screen, name, ax, row_y, 26, WHITE, key="black", align=al, valign="middle", glow=0.4)
            if hearts is not None or not right:
                n = int(hearts) if hearts is not None else 5
                nw = hd.text(name, "black", S(26), WHITE)["w"] if isinstance(name, str) and name else 0
                for i in range(5):                                     # the hearts, as in the game
                    hx = (ax - nw - S(30) - i * S(30)) if right else (ax + nw + S(24) + i * S(30))
                    col = (240, 50, 80) if i < n else (90, 60, 80)
                    pg.draw.circle(screen, col, (int(hx - S(5)), int(row_y - S(3))), S(7))
                    pg.draw.circle(screen, col, (int(hx + S(5)), int(row_y - S(3))), S(7))
                    pg.draw.polygon(screen, col, [(hx - S(12), row_y), (hx + S(12), row_y), (hx, row_y + S(13))])
            pw = _n(vals.get("power" + suf))
            if pw is not None:                                         # Pow 1 2 Max
                gx = x0 + w - S(380) if right else x0 + S(20)
                self.pill(screen, gx - S(10), H - S(58), S(370), S(50), 150)
                self.text(screen, "Pow", gx, H - S(44), 22, (255, 220, 90), key="black", valign="middle", glow=0)
                for lab, k_ in (("1", 1), ("2", 2), ("Max", 3)):
                    self.text(screen, lab, gx + S(60) + k_ * S(86) - S(20), H - S(44), 20, (255, 220, 90) if pw >= k_ * 0x1000 else GREY,
                              key="black", valign="middle", glow=0)
                frac = _clamp(pw / float(0x3000))
                pg.draw.rect(screen, (40, 20, 30), (int(gx + S(50)), H - S(30), S(300), S(14)), border_radius=S(3))
                if frac > 0:
                    pg.draw.rect(screen, (250, 60, 90) if frac < 1 else _mix((255, 220, 90), WHITE, 0.5 + 0.5 * math.sin(now * 12)),
                                 (int(gx + S(52)), H - S(28), int(S(296) * frac), S(10)), border_radius=S(3))
            bombs = _n(vals.get("bombs" + suf))
            if bombs is not None:                                      # B bombs, blue balls
                bx = x0 + w - S(410) if right else x0 + S(410)
                for i in range(min(5, int(bombs))):
                    cx = bx - i * S(42) if right else bx + i * S(42)
                    pg.draw.circle(screen, (40, 60, 200), (int(cx), H - S(33)), S(18))
                    pg.draw.circle(screen, (200, 220, 255), (int(cx), H - S(33)), S(18), max(1, S(3)))
                    self.text(screen, "B", cx, H - S(33), 22, WHITE, key="black", align="center", valign="middle", glow=0)


SCENES = {"s1945p": StrikersScene, "strhoop": StreetHoopScene, "sdodgeb": DodgeBallScene, "neobombe": NeoBombermanScene,
          "twinspri": TwinkleScene}
