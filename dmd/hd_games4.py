"""HD scenes of the fourth batch of Neo Geo games done one by one (1.20), each drawn after screenshots of its game:
Strikers 1945 Plus, Street Hoop, Super Dodge Ball... Each game has its own animated backdrop and reacts to the values
read in its memory. The characters, the planes of fiction and the robots are creations of the program in the spirit
of the games, the real planes are drawn after the real ones.

Scènes HD du quatrième lot de jeux Neo Geo faits un par un (1.20), chacune dessinée d'après des captures de son jeu.
Les personnages, les engins imaginaires et les robots sont des créations du programme dans l'esprit des jeux, les
vrais avions sont dessinés d'après les vrais.
"""

import math

from .hd_games import CREAM, GOLD, WHITE, GameScene, _clamp, _mix, _n, draw_img
from .hd_games3 import DARK, AeroFightersScene, _capsule, _lerp, _shape, bomb_icon_draw, bomber_draw
from .hd_themes4 import HOOP_X, hoop_y                      # (and the backdrops of this batch into hd_bg.BUILDERS)
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
        self.last = 0.0
        self.super_t = None
        self.baskets = 0                                  # baskets shown (tests)
        self.supers = 0
        self.dunks = 0
        self.fx.sp.register("hball", draw_img(S(30), S(30), ball_draw))
        self.warm = [(self.fig, (p, f)) for p in self.players for f in range(6)] + [(self.hoop_img, ())] + self.warm

    def restart(self, vals, now):
        self.queue = []
        self.ball = None
        self.next = now + 0.8
        self.last = now

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
            elif now - self.last > 7.0:                                # nobody scores: a shot off the rim
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
        self.last = now

    def scored(self, b):
        now, S, fx = self.fx.now, self.S, self.fx
        rx, ry = self.rx, self.ry
        if b["kind"] == "miss":                                        # off the rim, someone takes the rebound
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


SCENES = {"s1945p": StrikersScene, "strhoop": StreetHoopScene}
