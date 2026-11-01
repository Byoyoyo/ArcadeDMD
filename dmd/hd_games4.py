"""HD scenes of the fourth batch of Neo Geo games done one by one (1.20), each drawn after screenshots of its game:
Strikers 1945 Plus, Street Hoop, Super Dodge Ball... Each game has its own animated backdrop and reacts to the values
read in its memory. The characters, the planes of fiction and the robots are creations of the program in the spirit
of the games, the real planes are drawn after the real ones.

Scènes HD du quatrième lot de jeux Neo Geo faits un par un (1.20), chacune dessinée d'après des captures de son jeu.
Les personnages, les engins imaginaires et les robots sont des créations du programme dans l'esprit des jeux, les
vrais avions sont dessinés d'après les vrais.
"""

import math

from .hd_games import CREAM, GOLD, RED, WHITE, GameScene, _clamp, _mix, _n, draw_img
from .hd_games3 import DARK, AeroFightersScene, _capsule, _lerp, _shape, bomb_icon_draw, bomber_draw
from .hd_themes4 import (HOOP_X, LB_FAR, ML_FLOOR, NB_COLS, NB_ROWS, RH_HORIZON, dodge_y, hoop_y, lb_xy, nb_grid,
                          rally_road)                          # (and the backdrops of this batch into hd_bg.BUILDERS)
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
    PAINT = {1: (176, 182, 192), 2: (62, 84, 136), 3: (118, 128, 96), 4: (136, 142, 148), 5: (186, 186, 166), 6: (184, 164, 120),
             7: (170, 178, 190)}                      # each plane in its real colours / chaque avion dans ses vraies couleurs
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
        body = self.PAINT.get(kind, self.BODY[side])
        return s45_plane_draw(kind, body if side == "p1" else _mix(body, (60, 104, 190), 0.35), self.ACC[side] if side == "p1" else (255, 120, 60))

    def plane_surf(self, side, kind, shadow=False):
        """The planes a little bigger than in Aero Fighters, as in the game. / Les avions un peu plus grands."""
        S = self.S
        key = ("plane", side, kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            s = self.img(("planeimg", side, kind), S(186), S(168), self.plane_fn(side, kind))
            if shadow:
                s = self.shadow_of(self.pg, s, 80)
            self.imgs[key] = s
        return s

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
            if _n(vals.get("score" + suf)) is not None:                # the score next to the tag, as in the game
                hd._score(screen, eng, "score" + suf, x0 + S(200) if team == 0 else x0 + bw - S(80), S(10), "right", S(34))
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
# its own module since 1.30.1 / dans son propre module depuis la 1.30.1
from .hd_twinkle import TwinkleScene  # noqa: E402


# ============================================================================ Neo Drift Out, Thrash Rally
def rally_car_draw(body, stripe, number=(255, 255, 255)):
    """A rally car seen from above, nose to the right: a coupe with its wide wheels, the windscreen, a roof scoop, a
    spoiler, a livery of stripes and a white number disc. / Une voiture de rallye vue du dessus, nez à droite."""
    def fn(d, W, H):
        dark = (24, 24, 30, 255)
        ow = max(1.0, W * 0.012)
        for x in (0.22, 0.72):                                         # roues
            for y in (0.02, 0.8):
                d.rounded_rectangle([W * (x - 0.08), H * y, W * (x + 0.08), H * (y + 0.18)], radius=H * 0.05, fill=(30, 30, 34, 255))
        d.rounded_rectangle([W * 0.04, H * 0.12, W * 0.97, H * 0.88], radius=H * 0.24, fill=body + (255,), outline=dark, width=int(ow))
        d.polygon([(W * 0.1, H * 0.42), (W * 0.9, H * 0.36), (W * 0.9, H * 0.46), (W * 0.1, H * 0.52)], fill=stripe + (255,))
        d.polygon([(W * 0.1, H * 0.56), (W * 0.9, H * 0.52), (W * 0.9, H * 0.58), (W * 0.1, H * 0.62)], fill=_mix(stripe, (0, 200, 90), 0.6) + (255,))
        d.rounded_rectangle([W * 0.36, H * 0.2, W * 0.74, H * 0.8], radius=H * 0.12, fill=_mix(body, (255, 255, 255), 0.2) + (255,),
                            outline=dark, width=int(ow))                # le toit
        d.polygon([(W * 0.74, H * 0.22), (W * 0.86, H * 0.28), (W * 0.86, H * 0.72), (W * 0.74, H * 0.78)], fill=(60, 90, 120, 255), outline=dark)
        d.polygon([(W * 0.36, H * 0.24), (W * 0.3, H * 0.3), (W * 0.3, H * 0.7), (W * 0.36, H * 0.76)], fill=(60, 90, 120, 255), outline=dark)
        d.ellipse([W * 0.48, H * 0.36, W * 0.62, H * 0.64], fill=number + (255,), outline=dark, width=int(ow))
        d.rectangle([W * 0.02, H * 0.14, W * 0.07, H * 0.86], fill=_mix(body, (0, 0, 0), 0.3) + (255,), outline=dark)    # aileron
        for y in (0.2, 0.7):                                           # phares
            d.ellipse([W * 0.9, H * y, W * 0.97, H * (y + 0.1)], fill=(255, 250, 210, 255))
    return fn


class RallyScene(GameScene):
    """A rally stage seen from the sky, as in the game: the road winds through the countryside, the car drifts in the
    bends and throws dust or snow, a checkpoint arch goes by when time is added. The time read in the game is shown
    big, as in the game. / Une spéciale de rallye vue du ciel, comme dans le jeu."""
    THEME = "nd_dirt"
    THEMES = ("nd_dirt", "nd_tarmac")
    SHADE = (70, 70)
    PILLS = True
    CARS = {"p1": ((246, 246, 246), (220, 40, 40)), "p2": ((40, 90, 200), (250, 210, 40))}
    RIVALS = ()
    DUST, DUSTS, NEW_STAGE = (150, 140, 120), {}, 20.0
    BANNERS = GameScene.BANNERS + (("CHECKPOINT", GOLD),)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.bd.prebuild([n for n in self.THEMES if n != self.THEME])
        self.road = {}
        self.cars = {side: {"lat": 0.0 if side == "p1" else 0.5, "in": False, "x": 0.3 if side == "p1" else 0.22} for side in ("p1", "p2")}
        self.rivals = []
        self.gate = None                                  # checkpoint arch on the way / arche de contrôle qui arrive
        self.checkpoints = 0                              # (tests)
        self.stage_n = 0
        self.last_secs = None
        self.warm = [(self.car_img, (side,)) for side in ("p1", "p2")] + self.warm

    def road_fn(self):
        name = self.bd.theme
        r = self.road.get(name)
        if r is None:
            r = self.road[name] = rally_road(2 * self.W, self.H, self.s, name)
        return r

    def at(self, x):
        """Middle of the road and its slope at the screen x. / Milieu de la route et sa pente au x de l'écran."""
        ry, half = self.road_fn()
        tw = 2 * self.W
        wx = (x + self.bd.scroll) % tw
        y = ry(wx)
        return y, (ry(wx + 6) - ry(wx - 6)) / 12.0, (ry(wx + 12) - 2 * y + ry(wx - 12)) / 144.0, half

    def car_img(self, side, color=None):
        S = self.S
        body, stripe = color or self.CARS[side]
        return self.img(("rallycar", body, stripe), S(150), S(80), rally_car_draw(body, stripe), ss=2)

    def move(self, vals, now, idle):
        return 0.6 if idle else 5.2 * self.pace(vals)

    def pace(self, vals):
        return 1.0

    def secs(self, vals):
        """Time left, in seconds, or None. / Le temps qui reste, en secondes."""
        v = _n(vals.get("time"))
        return None if v is None else float(v)

    def next_stage(self, now):
        """A new stage: the other kind of road, shown once ready. / Une nouvelle spéciale : l'autre sorte de route."""
        self.stage_n += 1
        self.want = self.THEMES[self.stage_n % len(self.THEMES)]

    def always(self, vals, now):
        want = getattr(self, "want", None)
        if want and want != self.bd.theme and self.bd.ready(want) and self.bd.warm(want):
            self.bd.set_theme(want, now)
            self.DUST = self.DUSTS.get(want, self.DUST)
            self.want = None

    def restart(self, vals, now):
        self.rivals = []
        self.gate = None

    def update(self, vals, now):
        S = self.S
        for side in ("p1", "p2"):
            C = self.cars[side]
            C["in"] = self.p1_in(vals) if side == "p1" else self.p2_in(vals)
            st = self.stick(vals, side)
            if st is not None:
                C["lat"] = _clamp(C["lat"] + st[1] * self.dt * 1.2, -0.7, 0.7)
            else:
                C["lat"] += (math.sin(now * 0.7 + (0 if side == "p1" else 2)) * 0.45 - C["lat"]) * min(1.0, self.dt)
        sec = self.secs(vals)
        old = self.last_secs
        self.last_secs = sec
        if sec is not None and old is not None and sec > old + 1.5:   # time added: a checkpoint
            self.checkpoints += 1
            if sec > old + self.NEW_STAGE:
                self.next_stage(now)
            self.gate = {"x": self.W + S(80)}
            self.popup(tr("TEMPS EN PLUS", "EXTENDED TIME"), self.W * 0.5, S(200), (120, 230, 255), 44, 1.6, 50, "stencil")
        if self.RIVALS and len(self.rivals) < 2 and self.rng.random() < self.dt * 0.25:
            self.rivals.append({"x": self.W + S(100), "lat": self.rng.choice((-0.45, 0.45)), "col": self.rng.choice(self.RIVALS),
                                "v": self.rng.uniform(0.55, 0.8)})

    def draw_car(self, screen, img, x, lat, now, dust=True):
        S, pg = self.S, self.pg
        y, slope, curve, half = self.at(x)
        y += lat * half
        slip = _clamp(curve * 900, -24, 24)                            # drifts in the bends / dérape dans les virages
        ang = -math.degrees(math.atan(slope)) - slip
        rot = self.rotated(("car", id(img)), img, ang, 3)
        sh = self.imgs.get(("carsh", img.get_width()))
        if sh is None:
            sh = self.imgs[("carsh", img.get_width())] = pg.Surface((img.get_width(), img.get_height()), pg.SRCALPHA)
            pg.draw.rect(sh, (0, 0, 0, 80), sh.get_rect(), border_radius=S(16))
        screen.blit(sh, (int(x - sh.get_width() / 2 + S(6)), int(y - sh.get_height() / 2 + S(8))))
        screen.blit(rot, (int(x - rot.get_width() / 2), int(y - rot.get_height() / 2)))
        if dust and int(now * 30) % 2 == 0:                            # dust (or snow) behind
            col = self.DUST
            self.fx.smoke(x - S(56), y + S(10) * math.sin(now * 9), 1, (8, 16), 2.4, (0.4, 0.8), (0, 10), 14, col, 150, "back")

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        g = self.gate
        if g is not None:                                              # the checkpoint arch
            g["x"] -= self.bd.speed * self.dt
            if g["x"] < -S(100):
                self.gate = None
            else:
                y, slope, curve, half = self.at(g["x"])
                for side in (-1, 1):
                    pg.draw.circle(screen, (40, 40, 50), (int(g["x"]), int(y + side * (half + S(18)))), S(9))
                pg.draw.line(screen, (230, 50, 40), (int(g["x"]), int(y - half - S(18))), (int(g["x"]), int(y + half + S(18))), S(14))
                pg.draw.line(screen, (255, 255, 255), (int(g["x"]), int(y - half - S(18))), (int(g["x"]), int(y + half + S(18))), S(4))
        keep = []
        for r in self.rivals:                                          # other cars, overtaken
            r["x"] -= self.bd.speed * self.dt * (1 - r["v"])
            if r["x"] > -S(150):
                keep.append(r)
                self.draw_car(screen, self.car_img("rival", r["col"]), r["x"], r["lat"], now)
        self.rivals = keep
        for side in ("p2", "p1"):
            C = self.cars[side]
            if not C["in"]:
                continue
            self.draw_car(screen, self.car_img(side), self.W * C["x"], C["lat"], now)
        self.status(screen, eng, vals, logo, now)


class NeoDriftScene(RallyScene):
    """Neo Drift Out: a dirt road through the woods, a tarmac road in the countryside, the white rally car with its
    stripes; the TIME in big blue numbers with its hundredths, as in the game. / Le temps en gros chiffres bleus."""
    THEME = "nd_dirt"
    THEMES = ("nd_dirt", "nd_tarmac")
    DUST = (176, 140, 96)
    DUSTS = {"nd_dirt": (176, 140, 96), "nd_tarmac": (150, 150, 156)}
    NEW_STAGE = 15.0

    def secs(self, vals):
        s, cs = _n(vals.get("time_s")), _n(vals.get("time_cs"))
        return None if s is None else s + (cs or 0) / 100.0

    def status(self, screen, eng, vals, logo, now):
        S, W, hd = self.S, self.W, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(480), S(96), now)
        t = self.secs(vals)
        if t is not None:                                              # TIME, big blue numbers with the hundredths
            col = (255, 80, 60) if t < 10 and int(now * 4) % 2 else (70, 120, 255)
            self.pill(screen, W - S(420), S(10), S(400), S(108), 150, radius=16)
            self.text(screen, "TIME", W - S(52), S(30), 26, WHITE, key="black", align="right", valign="middle")
            cs = int(round(t * 100))
            hd.put_number(screen, f"{cs // 100:02d}.{cs % 100:02d}", "stencil", S(84), col, W - S(52), S(76), "right", "middle")
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, S(30), S(50), 30, colw)


class ThrashRallyScene(RallyScene):
    """Thrash Rally: a dirt track between yellow and black barriers, then a snowy road with red and white kerbs, the
    red car among its rivals; TIME in yellow, SPEED in red, as in the game. / Le temps en jaune, la vitesse en rouge."""
    THEME = "tr_dirt"
    THEMES = ("tr_dirt", "tr_snow")
    CARS = {"p1": ((220, 40, 40), (250, 250, 250)), "p2": ((40, 150, 220), (250, 250, 250))}
    RIVALS = (((250, 200, 30), (40, 40, 40)), ((250, 250, 250), (40, 90, 200)), ((60, 160, 70), (250, 250, 250)))
    DUST = (120, 96, 60)
    DUSTS = {"tr_dirt": (120, 96, 60), "tr_snow": (240, 244, 250)}
    NEW_STAGE = 25.0

    def pace(self, vals):
        v = _n(vals.get("speed"))
        return 1.0 if v is None else 0.5 + _clamp(v / 1002.0) * 0.8

    def status(self, screen, eng, vals, logo, now):
        S, W, hd = self.S, self.W, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(480), S(96), now)
        t = _n(vals.get("time"))
        if t is not None:                                              # TIME, big yellow numbers, on the left
            self.pill(screen, S(16), S(10), S(250), S(108), 150, radius=16)
            self.text(screen, "TIME", S(36), S(30), 26, (255, 60, 40), key="black", valign="middle")
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(84), (255, 230, 40) if t >= 10 or int(now * 4) % 2 else (255, 80, 60), S(40),
                          S(76), "left", "middle")
        v = _n(vals.get("speed"))
        if v is not None:                                              # SPEED, in red, on the right
            self.pill(screen, W - S(330), S(10), S(310), S(84), 150, radius=16)
            self.text(screen, "SPEED", W - S(310), S(30), 26, (255, 60, 40), key="black", valign="middle")
            self.bar(screen, W - S(310), S(56), S(270), S(22), _clamp(v / 1002.0), (255, 120, 40))
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, W - S(180), S(130), 28, colw, align="center")


# ============================================================================ Riding Hero
RH_COLORS = (((230, 40, 40), (250, 250, 250)), ((60, 200, 60), (250, 250, 250)), ((250, 200, 30), (40, 40, 40)), ((40, 90, 220), (250, 250, 250)),
             ((250, 130, 30), (40, 40, 40)), ((150, 60, 200), (250, 250, 250)))


def rider_draw(main, second, number):
    """A road racing bike and its rider seen from behind, as in the game: the wide rear tyre, the tail and its number,
    the rider in leathers crouched on the tank, the helmet. / Une moto de course et son pilote vus de dos."""
    def fn(d, W, H):
        dark = (20, 20, 26, 255)
        ow = max(1.0, W * 0.02)
        m, m2, sc = main + (255,), _mix(main, (0, 0, 0), 0.3) + (255,), second + (255,)
        d.rounded_rectangle([W * 0.38, H * 0.66, W * 0.62, H * 0.99], radius=W * 0.08, fill=(30, 30, 34, 255), outline=dark, width=int(ow))  # pneu
        d.line([(W * 0.5, H * 0.7), (W * 0.5, H * 0.96)], fill=(70, 70, 80, 255), width=max(1, int(ow)))
        d.polygon([(W * 0.3, H * 0.62), (W * 0.7, H * 0.62), (W * 0.64, H * 0.74), (W * 0.36, H * 0.74)], fill=m2, outline=dark)    # carénage
        d.polygon([(W * 0.34, H * 0.48), (W * 0.66, H * 0.48), (W * 0.7, H * 0.64), (W * 0.3, H * 0.64)], fill=m, outline=dark)        # la selle
        d.rounded_rectangle([W * 0.42, H * 0.5, W * 0.58, H * 0.6], radius=W * 0.02, fill=(250, 250, 250, 255), outline=dark)          # le numéro
        d.ellipse([W * 0.44, H * 0.665, W * 0.56, H * 0.71], fill=(255, 60, 40, 255))                                                     # feu
        for sx in (0.14, 0.86):                                        # bras et poignées
            d.line([(W * 0.5, H * 0.3), (W * sx, H * 0.44)], fill=m, width=max(2, int(W * 0.09)))
            d.ellipse([W * (sx - 0.05), H * 0.4, W * (sx + 0.05), H * 0.48], fill=(30, 30, 34, 255))
        for sx in (0.28, 0.72):                                        # jambes repliées
            d.polygon([(W * 0.5, H * 0.46), (W * sx, H * 0.5), (W * (sx + (0.06 if sx < 0.5 else -0.06)), H * 0.66), (W * 0.5, H * 0.56)],
                      fill=m2, outline=dark)
        d.ellipse([W * 0.28, H * 0.22, W * 0.72, H * 0.52], fill=m, outline=dark, width=int(ow))                                         # le dos
        d.polygon([(W * 0.42, H * 0.26), (W * 0.58, H * 0.26), (W * 0.62, H * 0.48), (W * 0.38, H * 0.48)], fill=sc)
        d.ellipse([W * 0.36, H * 0.04, W * 0.64, H * 0.3], fill=sc, outline=dark, width=int(ow))                                         # le casque
        d.chord([W * 0.36, H * 0.04, W * 0.64, H * 0.3], 200, 340, fill=m)
    return fn


class RidingHeroScene(GameScene):
    """Riding Hero as in the game: the road seen from behind the bike rushes towards the horizon with its red and white
    kerbs, the bends sweep it left and right and the rider leans into them, the other riders are passed or come back.
    The rank, the time and the turbos read in the game are shown, a turbo spent is a burst of speed.
    / La route vue de derrière la moto file vers l'horizon, comme dans le jeu."""
    THEME = "rh_circuit"
    STATIC = True
    SHADE = (60, 70)
    PILLS = True
    BANNERS = GameScene.BANNERS + (("TURBO !", GOLD),)
    ORD = {1: "ST", 2: "ND", 3: "RD"}

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.hy = int(self.H * RH_HORIZON)
        n = self.H - self.hy
        self.rows = [(y, (y - self.hy + 1) / n) for y in range(self.hy, self.H, 2)]
        self.z = 0.0
        self.curve, self.tcurve, self.next_bend = 0.0, 0.0, 0.0
        self.burst = 0.0
        self.riders = []                                  # rivals: distance ahead, lane, colour / rivaux : distance, voie, couleur
        self.passes = 0                                   # (tests)
        self.turbos = 0
        self.warm = [(self.bike, (k, 0)) for k in range(len(RH_COLORS))] + self.warm

    def bike(self, k, size):
        """The rider k at a size (0: full size). The far ones are scaled down from the full picture, which is cheap.
        / Le pilote k à une taille ; ceux de loin sont réduits depuis la grande image."""
        S = self.S
        main, second = RH_COLORS[k % len(RH_COLORS)]
        base = self.img(("rider", k), S(118), S(190), rider_draw(main, second, k + 1), ss=2)
        if size == 0 or size == 1.0:
            return base
        key = ("riders", k, round(size * 20))
        s = self.imgs.get(key)
        if s is None:
            f = max(0.05, round(size * 20) / 20)
            s = self.imgs[key] = self.pg.transform.smoothscale(base, (max(2, int(base.get_width() * f)), max(2, int(base.get_height() * f))))
        return s

    def restart(self, vals, now):
        self.riders = [{"d": self.rng.uniform(3, 30), "lane": self.rng.uniform(-0.6, 0.6), "k": 1 + i, "v": self.rng.uniform(-0.6, 0.4)}
                       for i in range(3)]

    def speed(self, vals):
        v = _n(vals.get("speed"))
        base = 0.7 + 0.5 * _clamp((v or 0) / 199.0) if v is not None else 1.0
        return base + self.burst

    def update(self, vals, now):
        dt, rng, S = self.dt, self.rng, self.S
        if now >= self.next_bend:                                      # the bends of the circuit
            self.next_bend = now + rng.uniform(2.0, 4.0)
            self.tcurve = rng.choice((-1.0, -0.6, 0.0, 0.0, 0.6, 1.0))
        self.curve += (self.tcurve - self.curve) * min(1.0, dt * 0.9)
        self.burst = max(0.0, self.burst - dt * 0.3)
        self.z += dt * 40 * self.speed(vals)
        ch = self.changed(vals, "turbo")
        if ch and ch[1] < ch[0]:                                       # a turbo spent: a burst of speed
            self.turbos += 1
            self.burst = 0.8
            self.popup("TURBO !", self.W / 2, S(250), GOLD, 54, 1.2, 50, "stencil")
            self.fx.flash((255, 240, 200), 0.12, 0.25)
        ch = self.changed(vals, "rank")
        if ch and ch[1] < ch[0]:                                       # a rider passed
            self.passes += 1
            ahead = [r for r in self.riders if 0 < r["d"] < 12]
            r = min(ahead, key=lambda r: r["d"]) if ahead else {"d": 4.0, "lane": rng.uniform(-0.5, 0.5), "k": rng.randint(1, 5), "v": 0.0}
            if r not in self.riders:
                self.riders.append(r)
            r["v"] = -3.0                                              # it falls back past us
            self.popup(f"{int(ch[1])}{self.ORD.get(int(ch[1]), 'TH')}", self.W / 2, S(200), (120, 255, 140), 48, 1.2, 40, "stencil")
        elif ch and ch[1] > ch[0]:                                     # passed by a rider
            self.riders.append({"d": -2.0, "lane": rng.uniform(-0.5, 0.5), "k": rng.randint(1, 5), "v": 2.5})
        ch = self.changed(vals, "time")
        if ch and ch[1] > ch[0] + 5:
            self.popup(tr("TEMPS EN PLUS", "EXTENDED TIME"), self.W / 2, S(200), (120, 230, 255), 44, 1.6, 50, "stencil")
        keep = []
        for r in self.riders:
            r["d"] += r["v"] * dt
            if r["v"] < -1 and r["d"] < -1.5:
                continue
            if r["v"] > 1 and r["d"] > 8:
                r["v"] = rng.uniform(-0.3, 0.3)
            if -2.5 < r["d"] < 40:
                keep.append(r)
        self.riders = keep
        if len(self.riders) < 3 and rng.random() < dt * 0.3:
            self.riders.append({"d": 38.0, "lane": rng.uniform(-0.6, 0.6), "k": rng.randint(1, 5), "v": rng.uniform(-1.2, -0.4)})

    def road_x(self, k):
        """Middle of the road at the depth k (0 horizon, 1 bottom). / Le milieu de la route à la profondeur k."""
        return self.W / 2 + self.curve * self.W * 0.45 * (1 - k) ** 2

    def draw_road(self, screen):
        S, W, pg = self.S, self.W, self.pg
        for y, k in self.rows:
            zrow = 1.0 / max(0.02, k)
            band = int(zrow * 6 + self.z) % 2
            cx = self.road_x(k)
            half = W * 0.27 * k + S(6)
            pg.draw.rect(screen, (70, 150, 60) if band else (60, 136, 52), (0, y, W, 2))
            pg.draw.rect(screen, (112, 116, 124) if band else (104, 108, 116), (int(cx - half), y, int(2 * half), 2))
            kerb = max(1, int(half * 0.09))
            col = (230, 40, 40) if band else (250, 250, 250)
            pg.draw.rect(screen, col, (int(cx - half - kerb), y, kerb, 2))
            pg.draw.rect(screen, col, (int(cx + half), y, kerb, 2))
            if band:
                lw = max(1, int(half * 0.025))
                pg.draw.rect(screen, (236, 236, 236), (int(cx - lw / 2), y, lw, 2))

    def draw_attract(self, screen, eng, vals, logo, now):
        self.z += self.dt * 20                                         # the road rolls on behind the logo
        self.draw_road(screen)
        super().draw_attract(screen, eng, vals, logo, now)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        self.draw_road(screen)
        for r in sorted(self.riders, key=lambda r: -r["d"]):            # the other riders, far ones first
            if r["d"] <= 0.2:
                continue
            k = 1.0 / (1.0 + r["d"] * 0.35)
            y = self.hy + k * (self.H - self.hy) * 0.9
            x = self.road_x(k) + r["lane"] * self.W * 0.27 * k
            img = self.bike(r["k"], round(k * 20) / 20)
            lean = -self.curve * 14
            img = self.rotated(("rr", r["k"], img.get_height()), img, lean, 4)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height())))
        if self.p1_in(vals):                                            # the player's bike, big, at the bottom
            img = self.bike(0, 0)
            lean = -self.curve * 22 + math.sin(now * 3) * 2
            rot = self.rotated(("rp",), img, lean, 2)
            x = self.W / 2 - self.curve * S(90)
            screen.blit(rot, (int(x - rot.get_width() / 2), int(self.H - S(8) - rot.get_height())))
            if self.burst > 0.1:                                       # the turbo's flame
                g = self.fx.sp.glow(S(26) + S(10) * math.sin(now * 40), (120, 180, 255), 10, hot=0.8)
                screen.blit(g, (int(x - g.get_width() / 2), int(self.H - S(20) - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        for r in self.riders:                                           # riders right behind, passing us
            if -2.5 < r["d"] <= 0.2:
                k = 1.0
                img = self.bike(r["k"], 1.1)
                x = self.road_x(1.0) + r["lane"] * self.W * 0.3
                screen.blit(img, (int(x - img.get_width() / 2), int(self.H + r["d"] * S(60) - img.get_height() * 0.5)))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the speed at the top left, the time, the turbos at the bottom left, the rank at the bottom
        right. / Comme dans le jeu : la vitesse, le temps, les turbos, le classement."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(480), S(96), now)
        v = _n(vals.get("speed"))
        if v is not None:
            self.pill(screen, S(16), S(12), S(380), S(56), 150)
            self.text(screen, "SPEED", S(36), S(40), 28, (255, 230, 80), key="black", valign="middle")
            self.bar(screen, S(150), S(30), S(230), S(20), _clamp(v / 199.0), (255, 200, 60))
        t = _n(vals.get("time"))
        if t is not None:
            self.pill(screen, W - S(260), S(10), S(240), S(100), 150, radius=14)
            self.text(screen, "TIME", W - S(140), S(30), 26, (255, 230, 80), key="black", align="center", valign="middle")
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(64), (255, 90, 200), W - S(140), S(74), "center", "middle")
        tb = _n(vals.get("turbo"))
        if tb is not None:
            self.pill(screen, S(16), H - S(66), S(330), S(56), 150)
            self.text(screen, "TURBO", S(36), H - S(38), 28, (255, 230, 80), key="black", valign="middle")
            for i in range(4):
                on = i < int(tb)
                pg.draw.rect(screen, (255, 80, 40) if on else (60, 30, 20), (S(160) + i * S(44), H - S(52), S(36), S(28)), border_radius=S(4))
        rk = _n(vals.get("rank"))
        if rk is not None and rk >= 1:
            self.pill(screen, W - S(300), H - S(76), S(280), S(66), 150)
            self.text(screen, "RANK", W - S(280), H - S(43), 28, (255, 230, 80), key="black", valign="middle")
            self.text(screen, f"{int(rk)}{self.ORD.get(int(rk), 'TH')}", W - S(40), H - S(43), 52, (255, 90, 200), key="stencil", align="right",
                      valign="middle")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, S(220), S(110), 26, col, align="center")


# ============================================================================ League Bowling
PIN_SPOTS = [(0, 0)] + [(x, 1) for x in (-6, 6)] + [(x, 2) for x in (-12, 0, 12)] + [(x, 3) for x in (-18, -6, 6, 18)]


def pin_draw(d, W, H):
    """A bowling pin: white, its two red rings at the neck. / Une quille blanche et ses deux anneaux rouges."""
    dark = (60, 50, 50, 255)
    d.ellipse([W * 0.08, H * 0.42, W * 0.92, H * 0.98], fill=(250, 250, 248, 255), outline=dark, width=max(1, int(W * 0.05)))
    d.polygon([(W * 0.3, H * 0.46), (W * 0.36, H * 0.2), (W * 0.64, H * 0.2), (W * 0.7, H * 0.46)], fill=(250, 250, 248, 255))
    d.ellipse([W * 0.26, H * 0.0, W * 0.74, H * 0.22], fill=(250, 250, 248, 255), outline=dark, width=max(1, int(W * 0.05)))
    for y in (0.24, 0.3):
        d.rectangle([W * 0.34, H * y, W * 0.66, H * (y + 0.03)], fill=(220, 40, 40, 255))
    d.ellipse([W * 0.2, H * 0.52, W * 0.42, H * 0.8], fill=(255, 255, 255, 255))


def bowler_draw(shirt, trim, frame):
    """A bowler of our own seen from behind: a two-tone bowling shirt, dark trousers, a cap, the ball in his right hand.
    Frames 0 ready, 1 swing back, 2 release, 3 watching. / Un joueur de bowling à nous, vu de dos."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, W * 0.018)
        sk = (232, 186, 150, 255)
        sh, tr_ = shirt + (255,), trim + (255,)
        legs = {0: ((0.42, 0.98), (0.58, 0.98)), 1: ((0.4, 0.98), (0.62, 0.9)), 2: ((0.34, 0.98), (0.66, 0.94)), 3: ((0.36, 0.98), (0.64, 0.96))}[frame]
        for x, y in legs:
            _capsule(d, (W * 0.5 + (x - 0.5) * W * 0.4, H * 0.6), (W * x, H * y), W * 0.07, W * 0.06, (40, 40, 60, 255), dark, ow)
            d.ellipse([W * x - W * 0.07, H * y - H * 0.03, W * x + W * 0.07, H * y + H * 0.01], fill=(240, 240, 240, 255), outline=dark)
        d.rounded_rectangle([W * 0.3, H * 0.28, W * 0.7, H * 0.64], radius=W * 0.08, fill=sh, outline=dark, width=int(ow))   # la chemise
        d.rectangle([W * 0.3, H * 0.28, W * 0.7, H * 0.36], fill=tr_)
        d.line([(W * 0.5, H * 0.36), (W * 0.5, H * 0.64)], fill=tr_, width=max(1, int(W * 0.03)))
        arms = {0: ((0.24, 0.56), (0.74, 0.5)), 1: ((0.22, 0.5), (0.86, 0.66)), 2: ((0.18, 0.42), (0.6, 0.2)), 3: ((0.2, 0.46), (0.66, 0.12))}[frame]
        ball = None
        for i, (x, y) in enumerate(arms):
            sx = 0.32 if i == 0 else 0.68
            _capsule(d, (W * sx, H * 0.32), (W * x, H * y), W * 0.06, W * 0.05, sh if i == 0 else sh, dark, ow)
            d.ellipse([W * x - W * 0.04, H * y - W * 0.04, W * x + W * 0.04, H * y + W * 0.04], fill=sk, outline=dark)
            if i == 1 and frame in (0, 1):
                ball = (W * x, H * y + W * 0.06)
        d.ellipse([W * 0.35, H * 0.17, W * 0.4, H * 0.23], fill=sk, outline=dark)                                              # oreilles
        d.ellipse([W * 0.6, H * 0.17, W * 0.65, H * 0.23], fill=sk, outline=dark)
        d.ellipse([W * 0.38, H * 0.1, W * 0.62, H * 0.3], fill=(70, 44, 30, 255), outline=dark, width=int(ow))                 # la tête, de dos
        d.rectangle([W * 0.44, H * 0.27, W * 0.56, H * 0.3], fill=sk)                                                           # la nuque
        d.chord([W * 0.37, H * 0.08, W * 0.63, H * 0.24], 180, 360, fill=tr_)                                                  # la casquette
        d.rectangle([W * 0.37, H * 0.16, W * 0.63, H * 0.2], fill=tr_)
        d.rectangle([W * 0.45, H * 0.2, W * 0.55, H * 0.23], fill=_mix(trim, (0, 0, 0), 0.3) + (255,))
        if ball is not None:
            r = W * 0.09
            d.ellipse([ball[0] - r, ball[1] - r, ball[0] + r, ball[1] + r], fill=(40, 60, 160, 255), outline=dark, width=int(ow))
            d.ellipse([ball[0] - r * 0.5, ball[1] - r * 0.6, ball[0] - r * 0.1, ball[1] - r * 0.2], fill=(140, 170, 255, 255))
    return fn


class LeagueBowlingScene(GameScene):
    """League Bowling as in the game: the lane seen from behind the bowler, the pins at the far end, the lanes next door
    with their own pins. Each time the game's shot clock starts again, the bowler throws: the ball hooks down the lane
    and the pins fly, STRIKE! or SPARE! now and then. TIME and the score at the top, as in the game.
    / Le bowling comme dans le jeu : la piste vue de derrière le joueur, les quilles au fond, STRIKE !"""
    THEME = "lb_lanes"
    STATIC = True
    SHADE = (60, 40)
    PILLS = True
    BANNERS = GameScene.BANNERS + (("STRIKE !", GOLD), ("SPARE !", GOLD))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.pins = [{"x": x * 14.5, "z": LB_FAR - 0.2 + r * 0.06, "up": True, "fly": None} for x, r in PIN_SPOTS]
        self.throw_t = None
        self.ball = None
        self.next = 0.0
        self.second = False                               # second ball of the frame / deuxième boule
        self.throws = 0                                   # (tests)
        self.strikes = 0
        self.warm = [(self.pin_img, (z,)) for z in (2, 3)] + [(self.bowler, (f,)) for f in range(4)] + self.warm

    def pin_img(self, q):
        S = self.S
        return self.img(("pin", q), S(16) * q / 2 + S(6), S(40) * q / 2 + S(14), pin_draw)

    def bowler(self, frame):
        S = self.S
        return self.img(("bowler", frame), S(230), S(300), bowler_draw((60, 120, 210), (250, 210, 60), frame), ss=2)

    def xy(self, lane_x, z):
        return lb_xy(self.W, self.H, self.s, lane_x, z)

    def restart(self, vals, now):
        self.next = now + 1.5
        self.reset_pins()

    def reset_pins(self):
        for p in self.pins:
            p["up"], p["fly"] = True, None
        self.second = False

    def update(self, vals, now):
        ch = self.changed(vals, "time")
        if ch and ch[1] > ch[0] + 2 and self.throw_t is None:          # the shot clock starts again: a throw
            self.throw(now)
        elif self.throw_t is None and now >= self.next and _n(vals.get("time")) is None:
            self.throw(now)
        if self.throw_t is not None:
            k = now - self.throw_t
            if self.ball is None and k > 0.75:                         # release
                hook = self.rng.uniform(-0.6, 0.6)
                self.ball = {"t0": now, "dur": 1.5, "x0": self.rng.uniform(40, 120), "hook": hook}
            if k > 4.2:
                self.throw_t = None
                self.next = now + self.rng.uniform(2.0, 3.5)
                if self.second or all(not p["up"] for p in self.pins):
                    self.reset_pins()
                else:
                    self.second = True
        b = self.ball
        if b is not None and now - b["t0"] >= b["dur"]:
            self.ball = None
            self.hit(now, b)

    def throw(self, now):
        self.throw_t = now
        self.throws += 1

    def hit(self, now, b):
        """The ball reaches the pins: some fly, all of them for a strike. / La boule arrive : des quilles volent."""
        S, rng = self.S, self.rng
        up = [p for p in self.pins if p["up"]]
        if not up:
            return
        if not self.second:
            n = len(up) if rng.random() < 0.4 else rng.randint(5, 9)
        else:
            n = len(up) if rng.random() < 0.5 else rng.randint(0, len(up) - 1)
        aim = b["x0"] * 0.2 + b["hook"] * 40
        for p in sorted(up, key=lambda p: abs(p["x"] - aim))[:n]:
            p["up"] = False
            p["fly"] = (now + rng.uniform(0, 0.25), rng.uniform(-1, 1), rng.uniform(0.6, 1.2))
        x, y = self.xy(aim, LB_FAR - 0.15)
        self.fx.sparks(x, y, 14, (255, 250, 220), (100, 300), (180, 360), (0.2, 0.5), 400, "front", 2, 12)
        self.fx.shake(3, 0.2)
        if all(not p["up"] for p in self.pins):
            if not self.second:
                self.strikes += 1
                self.slam("STRIKE !", GOLD, now + 0.2, 1.6)
            else:
                self.slam("SPARE !", GOLD, now + 0.2, 1.4)
        elif n:
            self.popup(str(n), x, max(self.S(170), y - S(40)), CREAM, 40)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        for k in (-2, -1, 1, 2):                                       # pins standing on the lanes next door
            for x, r in PIN_SPOTS:
                z = LB_FAR - 0.2 + r * 0.06
                px, py = self.xy(k * 760 + x * 14.5, z)
                img = self.pin_img(2)
                screen.blit(img, (int(px - img.get_width() / 2), int(py - img.get_height())))
        for p in sorted(self.pins, key=lambda p: p["z"], reverse=True):
            px, py = self.xy(p["x"], p["z"])
            img = self.pin_img(3)
            if p["up"]:
                screen.blit(img, (int(px - img.get_width() / 2), int(py - img.get_height())))
            elif p["fly"] is not None and now >= p["fly"][0]:
                k = now - p["fly"][0]
                if k < 0.9:
                    rot = self.rotated(("pinr",), img, p["fly"][1] * k * 720, 20)
                    fx_ = px + p["fly"][1] * S(60) * k
                    fy_ = py - img.get_height() / 2 - S(90) * p["fly"][2] * math.sin(min(1.0, k / 0.9) * math.pi)
                    screen.blit(rot, (int(fx_ - rot.get_width() / 2), int(fy_ - rot.get_height() / 2)))
            elif p["fly"] is not None:
                screen.blit(img, (int(px - img.get_width() / 2), int(py - img.get_height())))
        b = self.ball
        if b is not None:                                              # the ball hooks down the lane
            k = _clamp((now - b["t0"]) / b["dur"])
            z = 1.15 + (LB_FAR - 0.3 - 1.15) * k ** 0.8
            lx = b["x0"] * (1 - k) + b["hook"] * 120 * math.sin(k * math.pi * 0.9)
            x, y = self.xy(lx, z)
            r = max(S(4), int(S(46) / z))
            pg.draw.circle(screen, (20, 14, 10), (int(x + r * 0.2), int(y)), r)
            pg.draw.circle(screen, (40, 60, 160), (int(x), int(y - r)), r)
            pg.draw.circle(screen, (140, 170, 255), (int(x - r * 0.35), int(y - r * 1.35)), max(1, r // 3))
        frame = 0
        if self.throw_t is not None:
            k = now - self.throw_t
            frame = 1 if k < 0.45 else (2 if k < 1.2 else 3)
        if self.p1_in(vals):
            img = self.bowler(frame)
            x = self.W / 2 + S(70) + (S(30) if frame in (1, 2) else 0)
            screen.blit(img, (int(x - img.get_width() / 2), int(self.H - img.get_height() + S(10))))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: TIME in its little box at the top left, the score next to it. / TIME et le score en haut."""
        S, W, hd = self.S, self.W, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(480), S(80), now)
        t = _n(vals.get("time"))
        if t is not None:
            self.box(screen, S(20), S(10), S(170), S(110), (200, 80, 220), fill=(10, 10, 30, 230), radius=8, width=3)
            self.text(screen, "TIME", S(105), S(30), 24, (255, 220, 120), key="black", align="center", valign="middle")
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(64), (255, 220, 60), S(105), S(78), "center", "middle")
        sc = _n(vals.get("score"))
        if sc is not None:
            self.pill(screen, S(210), S(26), S(300), S(70), 150)
            hd._score(screen, eng, "score", S(490), S(34), "right", S(54))
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(50), 30, col, align="right")


# ============================================================================ Magician Lord
ML_FORMS = {1: "mage", 13: "ninja", 9: "water", 14: "samurai", 5: "dragon", 10: "sea", 15: "thunder"}
ML_LOOK = {          # robe, dark, skin, trim / robe, ombre, peau, liseré
    "mage": ((40, 120, 80), (20, 70, 46), (236, 196, 160), (240, 200, 80)),
    "ninja": ((40, 40, 50), (20, 20, 26), (236, 196, 160), (200, 40, 40)),
    "water": ((50, 130, 200), (30, 80, 140), (120, 200, 220), (220, 250, 255)),
    "samurai": ((190, 40, 40), (110, 20, 20), (236, 196, 160), (240, 200, 80)),
    "dragon": ((60, 150, 60), (30, 90, 30), (180, 220, 120), (250, 220, 90)),
    "sea": ((210, 170, 60), (140, 100, 30), (236, 196, 160), (60, 160, 220)),
    "thunder": ((110, 60, 170), (60, 30, 110), (236, 196, 160), (250, 230, 80)),
}


def hero_draw(form, frame):
    """The hero of our own and his transformations, seen from the side, facing right: a young mage with a hooded
    cloak and a staff, or a ninja, a merman, a samurai, a dragon warrior, a sea warrior with a trident, a thunder god
    with his ring of drums. Frames 0 and 1 walk, 2 cast. / Notre héros et ses transformations, de profil."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, W * 0.02)
        robe, shade, skin, trim = (c + (255,) for c in ML_LOOK.get(form, ML_LOOK["mage"]))
        u = H
        cx = W * 0.46
        step = (0.07, -0.07) if frame == 0 else ((-0.07, 0.07) if frame == 1 else (-0.04, 0.05))
        for i, dx in enumerate(step):                                  # jambes et bottes
            f = (cx + dx * u, H * 0.97)
            _capsule(d, (cx, H * 0.6), f, 0.06 * u, 0.05 * u, shade if i == 0 else robe, dark, ow)
            d.rounded_rectangle([f[0] - 0.05 * u, f[1] - 0.05 * u, f[0] + 0.07 * u, f[1] + 0.01 * u], radius=0.02 * u, fill=(60, 40, 30, 255),
                                outline=dark)
        if form in ("mage", "thunder", "sea"):                         # la cape
            d.polygon([(cx - 0.02 * u, H * 0.26), (cx - 0.2 * u, H * (0.86 if frame != 2 else 0.8)), (cx + 0.02 * u, H * 0.7)], fill=shade, outline=dark)
        d.polygon([(cx - 0.1 * u, H * 0.3), (cx + 0.1 * u, H * 0.3), (cx + 0.12 * u, H * 0.66), (cx - 0.12 * u, H * 0.66)], fill=robe, outline=dark)
        d.line([(cx - 0.11 * u, H * 0.5), (cx + 0.11 * u, H * 0.5)], fill=trim, width=max(2, int(0.025 * u)))
        if form == "thunder":                                          # l'anneau de tambours
            d.arc([cx - 0.3 * u, H * 0.02, cx + 0.14 * u, H * 0.46], 100, 300, fill=(150, 100, 40, 255), width=max(2, int(0.03 * u)))
            for a in (130, 170, 210, 250, 290):
                rx = cx - 0.08 * u + math.cos(math.radians(a)) * 0.22 * u
                ry = H * 0.24 + math.sin(math.radians(a)) * 0.22 * u
                d.ellipse([rx - 0.04 * u, ry - 0.04 * u, rx + 0.04 * u, ry + 0.04 * u], fill=(220, 160, 60, 255), outline=dark)
        hand = (cx + 0.2 * u, H * (0.36 if frame == 2 else 0.46))
        _capsule(d, (cx + 0.04 * u, H * 0.34), hand, 0.045 * u, 0.04 * u, robe, dark, ow)
        d.ellipse([hand[0] - 0.035 * u, hand[1] - 0.035 * u, hand[0] + 0.035 * u, hand[1] + 0.035 * u], fill=skin, outline=dark)
        weapon = {"mage": "staff", "sea": "trident", "samurai": "sword", "ninja": "sword", "dragon": "sword"}.get(form)
        if weapon == "staff":
            d.line([(hand[0], hand[1] + 0.3 * u), (hand[0], hand[1] - 0.28 * u)], fill=(120, 80, 40, 255), width=max(2, int(0.03 * u)))
            d.ellipse([hand[0] - 0.05 * u, hand[1] - 0.36 * u, hand[0] + 0.05 * u, hand[1] - 0.26 * u], fill=(120, 220, 255, 255), outline=dark)
        elif weapon == "trident":
            d.line([(hand[0], hand[1] + 0.3 * u), (hand[0], hand[1] - 0.3 * u)], fill=(230, 200, 80, 255), width=max(2, int(0.025 * u)))
            for dx in (-0.05, 0, 0.05):
                d.line([(hand[0] + dx * u, hand[1] - 0.3 * u), (hand[0] + dx * u, hand[1] - 0.4 * u)], fill=(230, 200, 80, 255), width=max(2, int(0.02 * u)))
        elif weapon == "sword":
            d.line([(hand[0], hand[1]), (hand[0] + 0.26 * u, hand[1] - 0.2 * u)], fill=(220, 226, 236, 255), width=max(2, int(0.025 * u)))
        hx, hy = cx + 0.02 * u, H * 0.18                               # la tête
        r = 0.085 * u
        d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=skin, outline=dark, width=int(ow))
        d.ellipse([hx + r * 0.3, hy - r * 0.2, hx + r * 0.6, hy + r * 0.1], fill=dark)
        if form == "mage":                                             # capuche pointue
            d.polygon([(hx - r * 1.3, hy + r * 0.4), (hx - r * 0.9, hy - r * 1.4), (hx - r * 0.2, hy - r * 2.6), (hx + r * 0.9, hy - r * 1.0),
                       (hx + r * 1.0, hy - r * 0.3), (hx - r * 0.4, hy - r * 0.6)], fill=robe, outline=dark)
        elif form == "ninja":
            d.rectangle([hx - r, hy - r * 0.2, hx + r, hy + r], fill=robe)
            d.chord([hx - r, hy - r * 1.05, hx + r, hy + r * 0.2], 180, 360, fill=robe)
            d.rectangle([hx - r * 1.4, hy - r * 0.45, hx - r * 0.6, hy - r * 0.3], fill=trim)
        elif form == "samurai":                                        # casque à cornes plates
            d.chord([hx - r * 1.1, hy - r * 1.2, hx + r * 1.1, hy + r * 0.5], 180, 360, fill=shade, outline=dark)
            d.polygon([(hx - r * 0.6, hy - r * 1.0), (hx - r * 0.9, hy - r * 2.0), (hx - r * 0.3, hy - r * 1.1)], fill=trim)
            d.polygon([(hx + r * 0.6, hy - r * 1.0), (hx + r * 0.9, hy - r * 2.0), (hx + r * 0.3, hy - r * 1.1)], fill=trim)
        elif form == "dragon":                                         # heaume de dragon
            d.chord([hx - r * 1.1, hy - r * 1.2, hx + r * 1.2, hy + r * 0.5], 180, 360, fill=robe, outline=dark)
            d.polygon([(hx - r * 0.8, hy - r * 0.9), (hx - r * 1.8, hy - r * 1.8), (hx - r * 0.4, hy - r * 1.1)], fill=trim, outline=dark)
            d.polygon([(hx + r * 0.9, hy - r * 0.2), (hx + r * 1.7, hy + r * 0.1), (hx + r * 0.9, hy + r * 0.3)], fill=robe, outline=dark)
        elif form == "water":                                          # crête de nageoire
            d.polygon([(hx - r * 0.8, hy - r * 0.6), (hx - r * 0.2, hy - r * 1.8), (hx + r * 0.5, hy - r * 0.9)], fill=trim, outline=dark)
        elif form == "sea":                                            # couronne
            for k in range(5):
                bx = hx - r * 0.9 + k * r * 0.45
                d.polygon([(bx, hy - r * 0.6), (bx + r * 0.2, hy - r * 1.4), (bx + r * 0.4, hy - r * 0.6)], fill=(240, 200, 80, 255), outline=dark)
        elif form == "thunder":
            d.chord([hx - r * 1.05, hy - r * 1.1, hx + r, hy + r * 0.2], 180, 360, fill=(240, 240, 240, 255), outline=dark)
            d.polygon([(hx - r * 0.2, hy - r * 1.0), (hx, hy - r * 1.9), (hx + r * 0.2, hy - r * 1.0)], fill=trim, outline=dark)
    return fn


def skeleton_draw(frame):
    """An undead warrior walking left: pale blue bones, a rusty blade, red joints. / Un guerrier mort-vivant."""
    def fn(d, W, H):
        dark = (20, 24, 40, 255)
        bone, bone_d = (170, 190, 230, 255), (110, 130, 180, 255)
        ow = max(1.0, W * 0.025)
        u = H
        cx = W * 0.5
        step = (0.07, -0.06) if frame == 0 else (-0.06, 0.07)
        for i, dx in enumerate(step):
            k = (cx + dx * 0.5 * u, H * 0.78)
            f = (cx + dx * u, H * 0.97)
            _capsule(d, (cx, H * 0.58), k, 0.03 * u, 0.025 * u, bone_d if i == 0 else bone, dark, ow)
            _capsule(d, k, f, 0.025 * u, 0.025 * u, bone_d if i == 0 else bone, dark, ow)
            d.ellipse([k[0] - 0.03 * u, k[1] - 0.03 * u, k[0] + 0.03 * u, k[1] + 0.03 * u], fill=(200, 50, 50, 255))
        for k in range(4):                                             # les côtes
            y = H * (0.34 + 0.05 * k)
            d.arc([cx - 0.11 * u, y - 0.03 * u, cx + 0.11 * u, y + 0.05 * u], 180, 360, fill=bone, width=max(2, int(0.022 * u)))
        d.line([(cx, H * 0.28), (cx, H * 0.6)], fill=bone, width=max(2, int(0.03 * u)))
        hand = (cx - 0.2 * u, H * 0.44)
        _capsule(d, (cx - 0.02 * u, H * 0.32), hand, 0.025 * u, 0.025 * u, bone, dark, ow)
        d.line([(hand[0], hand[1]), (hand[0] - 0.22 * u, hand[1] - 0.12 * u)], fill=(160, 120, 80, 255), width=max(2, int(0.03 * u)))
        hx, hy = cx - 0.02 * u, H * 0.18
        r = 0.09 * u
        d.ellipse([hx - r, hy - r, hx + r, hy + r * 1.1], fill=bone, outline=dark, width=int(ow))
        d.ellipse([hx - r * 0.7, hy - r * 0.3, hx - r * 0.2, hy + r * 0.2], fill=(30, 20, 40, 255))
        d.ellipse([hx - r * 0.55, hy - r * 0.15, hx - r * 0.35, hy + r * 0.05], fill=(255, 60, 40, 255))
        d.polygon([(hx - r * 0.6, hy + r * 0.6), (hx + r * 0.2, hy + r * 0.6), (hx - r * 0.2, hy + r * 1.05)], fill=bone_d)
    return fn


class MagicianLordScene(GameScene):
    """Magician Lord as in the game, with a hero of our own: he walks the walkways of the villages in the giant trees,
    then the temples, throws his magic at the undead that come, takes the shape of the warrior read in the game. HP and
    POW in their gauges at the bottom, as in the game. / Notre héros parcourt les villages dans les arbres géants."""
    THEME = "ml_jungle"
    SHADE = (70, 80)
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS + (("TRANSFORMATION !", GOLD),)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.bd.prebuild(["ml_temple"])
        self.foes = []
        self.next_foe = 0.0
        self.cast = -99.0
        self.hurt = -99.0
        self.form = "mage"
        self.transforms = 0                               # (tests)
        self.kills = 0
        self.fx.sp.register("mlbolt", draw_img(self.S(40), self.S(22), lambda d, W, H: (
            d.ellipse([0, H * 0.1, W * 0.8, H * 0.9], fill=(120, 220, 255, 255)), d.ellipse([W * 0.2, H * 0.3, W * 0.7, H * 0.7], fill=(250, 255, 255, 255)))))
        self.warm = [(self.hero, ("mage", f)) for f in range(3)] + [(self.foe_img, (f,)) for f in range(2)] + self.warm

    def hero(self, form, frame):
        S = self.S
        return self.img(("mlhero", form, frame), S(150), S(190), hero_draw(form, frame), ss=2)

    def foe_img(self, frame):
        S = self.S
        return self.img(("mlfoe", frame), S(130), S(180), skeleton_draw(frame), ss=2)

    def move(self, vals, now, idle):
        return 0.4 if idle else 1.4

    def restart(self, vals, now):
        self.foes = []
        self.next_foe = now + 1.0

    def floor(self):
        return self.S(ML_FLOOR) + self.S(4)

    def always(self, vals, now):
        v = _n(vals.get("form"))
        form = ML_FORMS.get(int(v), "mage") if v is not None else "mage"
        if form != self.form:
            self.form = form
            self.transforms += 1
            self.slam("TRANSFORMATION !", GOLD, now, 1.3)
            x = self.W * 0.3
            self.fx.glow(x, self.floor() - self.S(90), 40, 200, (255, 240, 160), 0.6, "front", 1.0, 0.0)
            self.fx.flash((255, 250, 220), 0.2, 0.3)

    def update(self, vals, now):
        S, rng = self.S, self.rng
        ch = self.changed(vals, "energy")
        if ch and ch[1] < ch[0]:                                       # hit
            self.hurt = now
            self.popup("-1", self.W * 0.3, self.floor() - S(200), (255, 90, 70), 34)
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.fx.explosion(self.W * 0.3, self.floor() - S(90), 0.8, False)
            self.popup(tr("-1 VIE", "-1 LIFE"), self.W * 0.3, self.floor() - S(220), (255, 90, 70), 38)
            self.hurt = now
        ch = self.changed(vals, "power")
        if ch and ch[1] > ch[0]:
            self.popup("POW UP", self.W * 0.3, self.floor() - S(220), GOLD, 38)
        if now >= self.next_foe:                                       # the undead come from the right
            self.next_foe = now + rng.uniform(1.4, 2.8)
            self.foes.append({"x": self.W + S(40), "v": rng.uniform(110, 170) * self.s, "ph": rng.uniform(0, 6), "hp": 3})
        target = [f for f in self.foes if not f.get("dead") and self.W * 0.36 < f["x"] < self.W * 0.8]
        if target and now - self.cast > 0.7:                           # magic at the nearest one
            f = min(target, key=lambda f: f["x"])
            self.cast = now
            pw = int(_n(vals.get("power")) or 0)
            hx, hy = self.W * 0.3 + S(40), self.floor() - S(120)
            self.fx.tracer(hx, hy, f["x"], self.floor() - S(90), 2200, (120, 220, 255), 8 + 5 * pw, 90, "front", True)
            f["hp"] -= 1 + pw
            if f["hp"] <= 0:
                f["dead"] = now
                self.kills += 1
                self.fx.later(0.12, self.fx.explosion, f["x"], self.floor() - S(90), 0.5, False)
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:                                       # points: the nearest undead on screen falls
            live = [f for f in self.foes if not f.get("dead") and f["x"] < self.W * 0.9]
            if live:
                f = min(live, key=lambda f: f["x"])
                f["dead"] = now
                self.kills += 1
                self.fx.explosion(f["x"], self.floor() - S(90), 0.5, False)
        theme = "ml_temple" if (int(now / 40) % 2 and self.bd.ready("ml_temple")) else "ml_jungle"
        if theme != self.bd.theme and self.bd.warm(theme):
            self.bd.set_theme(theme, now)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, dt = self.S, self.dt
        fy = self.floor()
        keep = []
        for f in self.foes:
            if f.get("dead") and now - f["dead"] > 0.3:
                continue
            if not f.get("dead") and f["x"] > self.W * 0.3 + S(110):
                f["x"] -= f["v"] * dt
            elif not f.get("dead"):
                f["x"] -= self.bd.speed * dt                           # held at the hero, pushed back by the scroll
            if f["x"] < -S(100):
                continue
            keep.append(f)
            img = self.foe_img(int(now * 4 + f["ph"]) % 2)
            if f.get("dead") and int(now * 20) % 2:
                continue
            screen.blit(img, (int(f["x"] - img.get_width() / 2), int(fy - img.get_height())))
        self.foes = keep
        if self.p1_in(vals):
            frame = 2 if now - self.cast < 0.25 else int(now * 5) % 2
            img = self.hero(self.form, frame)
            if not (now - self.hurt < 0.8 and int(now * 16) % 2):     # blinks when hit
                screen.blit(img, (int(self.W * 0.3 - img.get_width() / 2), int(fy - img.get_height())))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1UP and the score, the lives at the top; HP and POW at the bottom. / 1UP, vies, HP et POW."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(480), S(90), now)
        self.pill(screen, S(16), S(10), S(460), S(64), 150)
        self.text(screen, "1UP", S(36), S(42), 30, (255, 220, 120), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(330), S(18), "right", S(48))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.text(screen, f"x{int(lives)}", S(456), S(42), 30, (120, 200, 255), key="black", align="right", valign="middle")
        hp = _n(vals.get("energy"))
        if hp is not None:                                             # HP, blue segments
            self.pill(screen, S(16), H - S(60), S(360), S(50), 160)
            self.text(screen, "HP", S(34), H - S(35), 28, (255, 220, 120), key="black", valign="middle")
            for i in range(5):
                on = i < int(hp)
                pg.draw.rect(screen, (60, 160, 255) if on else (24, 40, 70), (S(90) + i * S(54), H - S(48), S(46), S(26)), border_radius=S(4))
        pw = _n(vals.get("power"))
        if pw is not None:                                             # POW, green to yellow
            self.pill(screen, W - S(376), H - S(60), S(360), S(50), 160)
            self.text(screen, "POW", W - S(356), H - S(35), 28, (255, 220, 120), key="black", valign="middle")
            for i in range(3):
                on = i <= int(pw)
                pg.draw.rect(screen, ((80, 220, 80), (220, 230, 60), (255, 150, 40))[i] if on else (40, 40, 30),
                             (W - S(270) + i * S(80), H - S(48), S(70), S(26)), border_radius=S(4))
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(42), 30, col, align="right")


SCENES = {"s1945p": StrikersScene, "strhoop": StreetHoopScene, "sdodgeb": DodgeBallScene, "neobombe": NeoBombermanScene,
          "twinspri": TwinkleScene, "neodrift": NeoDriftScene, "trally": ThrashRallyScene, "ridhero": RidingHeroScene,
          "lbowling": LeagueBowlingScene, "maglord": MagicianLordScene}
