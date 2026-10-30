"""HD scenes of the Capcom CPS puzzle, sports and quiz games (1.30), each drawn after screenshots of its game: Super
Puzzle Fighter II Turbo, Puzz Loop 2, Capcom Sports Club, Quiz & Dragons and Capcom World 2. Each game has its own
animated backdrop and reacts to the values read in its memory. The action games and the platformers are shown with
player panels (hd_panels.py). No picture comes from a game.

Scènes HD des jeux de réflexion, de sport et de quiz Capcom CPS (1.30), chacune dessinée d'après des captures de son
jeu. Les jeux d'action et de plateformes sont montrés avec des panneaux de joueur (hd_panels.py). Aucune image ne vient
d'un jeu.
"""

import math

from .hd_games import GOLD, P1C, P2C, WHITE, GameScene, _clamp, _mix, _n
from .hd_games3 import _capsule
from .hd_games2 import SoccerScene
from .hd_games7 import flag_draw
from .hd_games8 import kits
from .hd_games11 import QuizScene
from .hd_themes14 import SPF_CELL, SPF_COLS, SPF_ROWS, SPF_TOP, pl_path

DARKLINE = (24, 20, 26, 255)


def _c(col, a=255):
    return tuple(col[:3]) + (a,)


def balloon_draw(col):
    """A shiny round balloon. / Un ballon rond et brillant."""
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=_c(_mix(col, (0, 0, 0), 0.35)))
        d.ellipse([W * 0.04, H * 0.02, W * 0.94, H * 0.92], fill=_c(col))
        d.ellipse([W * 0.16, H * 0.12, W * 0.5, H * 0.42], fill=_c(_mix(col, WHITE, 0.55)))
        d.ellipse([W * 0.22, H * 0.16, W * 0.36, H * 0.28], fill=(255, 255, 255, 255))
    return fn


# ============================================================================ Super Puzzle Fighter II Turbo
SPF_COLORS = ((230, 50, 60), (60, 200, 80), (60, 120, 240), (250, 210, 50))


def gem_draw(col, kind, n=0):
    """A gem of our own: a bevelled square, a round crash gem, or a counter gem with its number.
    / Une gemme à nous : un carré biseauté, une gemme qui fait exploser (ronde), ou une gemme à compteur et son nombre."""
    def fn(d, W, H):
        dark, light = _c(_mix(col, (0, 0, 0), 0.45)), _c(_mix(col, WHITE, 0.5))
        if kind == 1:                                                  # la gemme ronde
            d.ellipse([W * 0.04, H * 0.04, W * 0.96, H * 0.96], fill=dark)
            d.ellipse([W * 0.1, H * 0.08, W * 0.9, H * 0.88], fill=_c(col))
            d.ellipse([W * 0.22, H * 0.18, W * 0.5, H * 0.44], fill=light)
            d.polygon([(W * 0.5, H * 0.3), (W * 0.58, H * 0.48), (W * 0.76, H * 0.5), (W * 0.58, H * 0.56), (W * 0.5, H * 0.74),
                       (W * 0.42, H * 0.56), (W * 0.24, H * 0.5), (W * 0.42, H * 0.48)], fill=(255, 255, 255, 230))
            return
        d.rectangle([0, 0, W - 1, H - 1], fill=dark)
        d.polygon([(0, 0), (W, 0), (W * 0.82, H * 0.18), (W * 0.18, H * 0.18)], fill=light)
        d.polygon([(0, 0), (W * 0.18, H * 0.18), (W * 0.18, H * 0.82), (0, H)], fill=_c(_mix(col, WHITE, 0.25)))
        d.rectangle([W * 0.18, H * 0.18, W * 0.82, H * 0.82], fill=_c(col if kind == 0 else _mix(col, (0, 0, 0), 0.3)))
        if kind == 0:
            d.ellipse([W * 0.26, H * 0.24, W * 0.46, H * 0.42], fill=(255, 255, 255, 200))
        else:                                                          # le compteur / the counter
            k = H * 0.1
            segs = {1: ((0.5, 0.25, 0.5, 0.75),), 2: ((0.32, 0.27, 0.68, 0.27), (0.68, 0.27, 0.68, 0.5), (0.68, 0.5, 0.32, 0.5), (0.32, 0.5, 0.32, 0.73),
                                                         (0.32, 0.73, 0.68, 0.73)),
                    3: ((0.32, 0.27, 0.68, 0.27), (0.68, 0.27, 0.68, 0.73), (0.38, 0.5, 0.68, 0.5), (0.32, 0.73, 0.68, 0.73)),
                    4: ((0.32, 0.27, 0.32, 0.5), (0.32, 0.5, 0.68, 0.5), (0.62, 0.27, 0.62, 0.75)),
                    5: ((0.68, 0.27, 0.32, 0.27), (0.32, 0.27, 0.32, 0.5), (0.32, 0.5, 0.68, 0.5), (0.68, 0.5, 0.68, 0.73), (0.68, 0.73, 0.32, 0.73))}
            for x0, y0, x1, y1 in segs.get(max(1, min(5, n)), segs[1]):
                d.line([(W * x0, H * y0), (W * x1, H * y1)], fill=(255, 255, 255, 255), width=int(k))
    return fn


def chibi_draw(skin, hair, top, pants, frame, girl=False):
    """A little fighter of our own with a big head: guard, attack (arm and leg forward) or hurt.
    / Un petit combattant à nous à grosse tête : en garde, attaque ou touché."""
    def fn(d, W, H):
        ow = max(1.0, H * 0.014)
        lean = {1: 0.05, 2: -0.06}.get(frame, 0.0) * W
        for k, x in enumerate((0.4, 0.56)):
            fx = W * x + (W * 0.12 if frame == 1 and k == 1 else 0)
            _capsule(d, (W * x + lean, H * 0.7), (fx, H * 0.95), H * 0.07, H * 0.06, _c(pants), DARKLINE, ow)
        d.rounded_rectangle([W * 0.32 + lean, H * 0.5, W * 0.66 + lean, H * 0.76], radius=W * 0.08, fill=_c(top), outline=DARKLINE, width=int(ow))
        arm = (W * 0.92, H * 0.56) if frame == 1 else (W * 0.66 + lean, H * 0.7)
        _capsule(d, (W * 0.56 + lean, H * 0.56), arm, H * 0.055, H * 0.05, _c(skin), DARKLINE, ow)
        d.ellipse([arm[0] - H * 0.04, arm[1] - H * 0.04, arm[0] + H * 0.04, arm[1] + H * 0.04], fill=_c(skin), outline=DARKLINE)
        hx, hy, r = W * 0.5 + lean, H * 0.3, W * 0.25
        if girl:                                                       # la queue de cheval / ponytail
            d.ellipse([hx - r * 1.4, hy - r * 0.6, hx - r * 0.5, hy + r * 0.9], fill=_c(hair), outline=DARKLINE, width=int(ow))
        d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=_c(skin), outline=DARKLINE, width=int(ow))
        d.chord([hx - r * 1.04, hy - r * 1.08, hx + r * 1.04, hy + r * 0.5], 180, 360, fill=_c(hair), outline=DARKLINE)
        if not girl:                                                   # des mèches en pointe / spiky hair
            for k in range(4):
                bx = hx - r * 0.8 + k * r * 0.5
                d.polygon([(bx, hy - r * 0.6), (bx + r * 0.25, hy - r * 1.35), (bx + r * 0.5, hy - r * 0.6)], fill=_c(hair), outline=DARKLINE)
        ey = hy + r * 0.12
        for ex in (0.32, 0.72):
            x = hx - r + 2 * r * ex
            if frame == 2:
                d.line([(x - r * 0.1, ey - r * 0.08), (x + r * 0.1, ey + r * 0.08)], fill=DARKLINE, width=int(ow * 2))
                d.line([(x - r * 0.1, ey + r * 0.08), (x + r * 0.1, ey - r * 0.08)], fill=DARKLINE, width=int(ow * 2))
            else:
                d.ellipse([x - r * 0.1, ey - r * 0.16, x + r * 0.1, ey + r * 0.16], fill=DARKLINE)
                d.ellipse([x - r * 0.04, ey - r * 0.12, x + r * 0.03, ey - r * 0.03], fill=(255, 255, 255, 255))
        d.arc([hx - r * 0.25, hy + r * 0.3, hx + r * 0.25, hy + r * 0.62], 20, 160, fill=DARKLINE, width=int(ow * 1.5))
    return fn


class GemWell:
    """A well of gems: pairs fall, land, a round gem bursts the gems of its colour that touch it and sends counter gems
    to the other well. / Un puits de gemmes : des paires tombent, une gemme ronde fait éclater les gemmes de sa couleur
    qui la touchent et envoie des gemmes à compteur dans l'autre puits."""

    def __init__(self, rng):
        self.rng = rng
        self.grid = [[None] * SPF_ROWS for _ in range(SPF_COLS)]       # grid[col][row], row 0 at the bottom
        self.pair = None
        self.next = self.new_pair()
        self.pending = 0
        self.crashes = 0
        self.flash = []                                                # (col, row, color, t) gems that burst / qui éclatent

    def new_pair(self):
        r = self.rng
        return [(r.randrange(4), 1 if r.random() < 0.25 else 0), (r.randrange(4), 1 if r.random() < 0.12 else 0)]

    def height(self, c):
        for r in range(SPF_ROWS):
            if self.grid[c][r] is None:
                return r
        return SPF_ROWS

    def drop(self, now):
        c = self.rng.randrange(SPF_COLS)
        self.pair = {"col": c, "gems": self.next, "t0": now, "land": self.height(c)}
        self.next = self.new_pair()

    def land(self, now):
        p = self.pair
        self.pair = None
        c, h = p["col"], self.height(p["col"])
        for k, g in enumerate(p["gems"]):
            if h + k < SPF_ROWS:
                self.grid[c][h + k] = (g[0], g[1], 0)
        sent = 0
        for k in range(2):
            if h + k < SPF_ROWS:
                sent += self.crash(c, h + k, now)
        if self.height(c) >= SPF_ROWS - 1 or max(self.height(x) for x in range(SPF_COLS)) >= SPF_ROWS:
            self.clear(now)
        return sent

    def crash(self, c, r, now, force=False):
        """Bursts the gems of the colour of the round gem at (c, r) that touch it. / Fait éclater les gemmes."""
        g = self.grid[c][r]
        if g is None or (g[1] != 1 and not force):
            return 0
        col = g[0]
        todo, seen = [(c, r)], set()
        while todo:
            x, y = todo.pop()
            if (x, y) in seen or not (0 <= x < SPF_COLS and 0 <= y < SPF_ROWS):
                continue
            q = self.grid[x][y]
            if q is None or q[0] != col or q[1] == 2:
                continue
            seen.add((x, y))
            todo += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        if len(seen) < 2 and not force:
            return 0
        for x, y in seen:
            self.flash.append((x, y, col, now))
            self.grid[x][y] = None
        self.settle()
        self.crashes += 1
        return len(seen) // 2

    def settle(self):
        for c in range(SPF_COLS):
            col = [g for g in self.grid[c] if g is not None]
            self.grid[c] = col + [None] * (SPF_ROWS - len(col))

    def receive(self, n):
        """Counter gems fall on the top of the well. / Des gemmes à compteur tombent en haut du puits."""
        for _ in range(n):
            c = self.rng.randrange(SPF_COLS)
            h = self.height(c)
            if h < SPF_ROWS:
                self.grid[c][h] = (self.rng.randrange(4), 2, 5)

    def tick(self):
        """The counters go down, at 0 the gem is an ordinary gem. / Les compteurs baissent, à 0 la gemme est ordinaire."""
        for c in range(SPF_COLS):
            for r in range(SPF_ROWS):
                g = self.grid[c][r]
                if g is not None and g[1] == 2:
                    self.grid[c][r] = (g[0], 2, g[2] - 1) if g[2] > 1 else (g[0], 0, 0)

    def clear(self, now):
        for c in range(SPF_COLS):
            for r in range(SPF_ROWS):
                if self.grid[c][r] is not None:
                    self.flash.append((c, r, self.grid[c][r][0], now))
        self.grid = [[None] * SPF_ROWS for _ in range(SPF_COLS)]


class PuzzleFighterScene(GameScene):
    """Super Puzzle Fighter II Turbo as in the game: the hall of the fights, the two wells of gems at the sides; pairs of
    gems of our own fall, a round gem bursts the gems of its colour and sends counter gems to the other side, the two
    little fighters of our own in the middle fight with each crash. The names of the characters read in the game,
    NEXT and the score above the wells. / La salle des combats, les deux puits de gemmes ; des paires de gemmes à nous
    tombent, une gemme ronde fait éclater celles de sa couleur et envoie des gemmes à compteur de l'autre côté, nos deux
    petits combattants au milieu se battent à chaque explosion. Les noms des personnages lus dans le jeu."""
    THEME = "spf_hall"
    STATIC = True
    SHADE = (60, 30)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.wells = [GemWell(self.rng), GemWell(self.rng)]
        self.next_drop = [0.0, 0.4]
        self.next_tick = 0.0
        self.act = [(-99.0, 0), (-99.0, 0)]                             # (time, frame) of each fighter / de chaque combattant
        self.attacks = 0                                               # (tests)
        self.warm = [(self.gem_img, (c, k, n)) for c in range(4) for k, n in ((0, 0), (1, 0), (2, 5))] + [(self.fighter, (i, f)) for i in range(2)
                                                                                                         for f in range(3)] + self.warm

    def cell(self):
        return self.S(SPF_CELL)

    def well_x(self, side):
        return self.S(150) if side == 0 else self.W - self.S(150) - SPF_COLS * self.cell()

    def gem_img(self, col, kind, n):
        c = self.cell()
        return self.img(("spfgem", col, kind, n), c, c, gem_draw(SPF_COLORS[col], kind, n), ss=3)

    GIRLS = (0, 1, 4, 6, 7, 8)                                         # the characters that are girls / les personnages filles
    LOOKS = (((40, 30, 60), (250, 200, 40)), ((60, 40, 30), (60, 110, 220)), ((30, 30, 30), (240, 240, 240)), ((200, 160, 60), (220, 60, 50)),
             ((30, 30, 60), (150, 80, 200)), ((230, 230, 230), (60, 60, 70)), ((120, 60, 160), (90, 200, 220)), ((90, 50, 30), (250, 140, 180)),
             ((220, 120, 40), (120, 120, 140)), ((160, 30, 30), (70, 50, 60)), ((60, 40, 30), (250, 150, 180)))

    def fighter(self, side, frame, who=None):
        """Our own little fighter for the character read in the game: a girl or a boy, colours of our own.
        / Notre petit combattant pour le personnage lu dans le jeu : fille ou garçon, couleurs à nous."""
        S = self.S
        who = (2, 0)[side] if who is None else who
        hair, top = self.LOOKS[who % len(self.LOOKS)]
        return self.img(("spfchibi", side, frame, who), S(160), S(200), chibi_draw((240, 196, 160), hair, top, (60, 60, 80), frame, who in self.GIRLS),
                        ss=2, flip=side == 1)

    def restart(self, vals, now):
        self.next_drop = [now + 0.3, now + 0.7]

    def attack(self, side, n, now):
        """A crash: the fighter of that side strikes, counter gems fall on the other side. / Une explosion : il frappe."""
        self.attacks += 1
        self.act[side] = (now, 1)
        self.act[1 - side] = (now + 0.15, 2)
        self.wells[1 - side].receive(min(6, max(1, n)))
        S = self.S
        x = self.W / 2 + (S(100) if side == 0 else -S(100))
        self.fx.sparks(x, S(300), 14, (255, 240, 160), (300, 700), (0, 360), (0.2, 0.4), 300, "front", 4, 16)
        self.fx.glow(x, S(300), 20, 90, (255, 220, 140), 0.3, "front", 0.9, 0.0)

    def update(self, vals, now):
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:                                       # points: player 1 bursts a group / des points
            w = self.wells[0]
            for c in range(SPF_COLS):
                h = w.height(c)
                if h:
                    n = w.crash(c, h - 1, now, force=True)
                    self.attack(0, max(1, n), now)
                    break

    def always(self, vals, now):
        if now >= self.next_tick:
            self.next_tick = now + 1.0
            for w in self.wells:
                w.tick()
        for side, w in enumerate(self.wells):
            if w.pair is None and now >= self.next_drop[side]:
                w.drop(now)
            elif w.pair is not None and now - w.pair["t0"] >= 0.55:
                sent = w.land(now)
                if sent:
                    self.attack(side, sent, now)
                self.next_drop[side] = now + self.rng.uniform(0.2, 0.6)

    def draw_well(self, screen, side, now):
        w, c = self.wells[side], self.cell()
        x0, y0 = self.well_x(side), self.S(SPF_TOP)
        bottom = y0 + SPF_ROWS * c
        for col in range(SPF_COLS):
            for row in range(SPF_ROWS):
                g = w.grid[col][row]
                if g is not None:
                    screen.blit(self.gem_img(g[0], g[1], g[2] if g[1] == 2 else 0), (int(x0 + col * c), int(bottom - (row + 1) * c)))
        if w.pair is not None:                                         # the pair falls / la paire tombe
            p = w.pair
            k = _clamp((now - p["t0"]) / 0.55)
            land_y = bottom - (w.height(p["col"]) + 1) * c
            y = y0 - c + (land_y - (y0 - c)) * k
            for i, g in enumerate(p["gems"]):
                screen.blit(self.gem_img(g[0], g[1], 0), (int(x0 + p["col"] * c), int(y - i * c)))
        keep = []
        for col, row, color, t0 in w.flash:                            # the gems that burst / les gemmes qui éclatent
            k = (now - t0) / 0.35
            if k >= 1:
                continue
            keep.append((col, row, color, t0))
            r = int(c * (0.5 + k))
            self.pg.draw.circle(screen, _mix(SPF_COLORS[color], WHITE, 0.6), (int(x0 + (col + 0.5) * c), int(bottom - (row + 0.5) * c)), r,
                                max(1, int(c * 0.2 * (1 - k))))
        w.flash = keep

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        for side in (0, 1):
            self.draw_well(screen, side, now)
        for side in (0, 1):                                            # the two little fighters / les deux petits combattants
            t0, f = self.act[side]
            frame = f if 0 <= now - t0 < 0.4 else 0
            who = _n(vals.get("_p1_chr" if side == 0 else "_p2_chr"))
            img = self.fighter(side, frame, int(who) if who is not None else None)
            bob = math.sin(now * 4 + side) * S(4) if frame == 0 else 0
            x = W / 2 - S(150) if side == 0 else W / 2 + S(150)
            screen.blit(img, (int(x - img.get_width() / 2), int(S(430) - img.get_height() + bob)))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """NEXT and the score above each well, the names of the characters under the fighters. / NEXT, score et noms."""
        S, W, hd, c = self.S, self.W, self.hd, self.cell()
        hd.draw_logo(screen, logo, W / 2, S(6), S(420), S(80), now)
        for side in (0, 1):
            x0 = self.well_x(side)
            nx = x0 - S(110) if side == 0 else x0 + SPF_COLS * c + S(20)
            self.pill(screen, nx, S(SPF_TOP - 4), S(90), S(124), 170, radius=12)
            self.text(screen, "NEXT", nx + S(45), S(SPF_TOP + 16), 22, (255, 230, 120), key="black", align="center", valign="middle")
            for i, g in enumerate(self.wells[side].next):
                screen.blit(self.gem_img(g[0], g[1], 0), (int(nx + S(30)), int(S(SPF_TOP + 76) - i * c)))
            name = vals.get("p1_char" if side == 0 else "p2_char")
            if isinstance(name, str) and name:
                self.label(screen, name, W / 2 + (-S(150) if side == 0 else S(150)), S(440), 26, P1C if side == 0 else P2C, align="center")
        self.pill(screen, S(40), S(8), S(330), S(62), 170, radius=12)
        self.text(screen, "SCORE", S(58), S(39), 22, P1C, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(356), S(16), "right", S(36))
        if self.p2_in(vals) and _n(vals.get("score_p2")) is not None:
            self.pill(screen, W - S(370), S(8), S(330), S(62), 170, radius=12)
            self.text(screen, "SCORE", W - S(352), S(39), 22, P2C, key="black", valign="middle")
            hd._score(screen, eng, "score_p2", W - S(54), S(16), "right", S(36))
        elif not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 28, col, align="right")


# ============================================================================ Puzz Loop 2
PL_COLORS = ((230, 60, 60), (60, 120, 240), (250, 210, 50), (60, 190, 90), (190, 80, 220))


class PuzzLoopScene(GameScene):
    """Puzz Loop 2 as in the game: the sky of purple clouds, the carved track; a chain of coloured balls rolls toward
    the hole, the launcher in the middle turns and fires a ball into the chain, three of a colour together burst and the
    chain closes up. The points read in the game burst a group; the chain that reaches the hole starts again. BALLS and
    the score. / Le ciel de nuages violets, le chemin sculpté ; une chaîne de boules roule vers le trou, le lanceur au
    milieu tourne et tire une boule dans la chaîne, trois de la même couleur ensemble éclatent et la chaîne se resserre."""
    THEME = "pl_cosmos"
    STATIC = True
    SHADE = (60, 20)
    R = 22                          # radius of a ball / rayon d'une boule

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        pts = pl_path(self.W, self.H, self.s)
        self.path, self.cum = pts, [0.0]
        for a, b in zip(pts, pts[1:]):
            self.cum.append(self.cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        self.length = self.cum[-1]
        self.center = (self.W / 2, self.S((168 + 340) / 2))
        self.chain = []                                                # colours, head first / couleurs, la tête d'abord
        self.head = 0.0
        self.shot = None
        self.aim = 0.0
        self.next_shot = 0.0
        self.balls_n = 0
        self.pops_n = 0                                                # (tests)
        self.resets = 0
        self.fill(0.0)
        self.warm = [(self.ball_img, (c,)) for c in range(len(PL_COLORS))] + self.warm

    def ball_img(self, col):
        r = self.S(self.R)
        return self.img(("plball", col), 2 * r, 2 * r, balloon_draw(PL_COLORS[col]), ss=2)

    def fill(self, now):
        """A new chain whose head is halfway to the hole, its tail at the start of the track. / Une nouvelle chaîne."""
        self.head = self.length * 0.6
        self.chain = [self.rng.randrange(4) for _ in range(int(self.head / (self.S(self.R) * 2)) + 2)]

    def at(self, d):
        """The point of the track at distance d. / Le point du chemin à la distance d."""
        if d <= 0:
            return self.path[0]
        lo, hi = 0, len(self.cum) - 1
        while lo < hi - 1:
            mid = (lo + hi) // 2
            if self.cum[mid] <= d:
                lo = mid
            else:
                hi = mid
        a, b = self.path[lo], self.path[hi]
        k = (d - self.cum[lo]) / max(1e-6, self.cum[hi] - self.cum[lo])
        return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k

    def burst_at(self, i, now, need=3):
        """Bursts the run of one colour around i if it is long enough. / Fait éclater la suite d'une couleur autour de i."""
        if not 0 <= i < len(self.chain):
            return 0
        c = self.chain[i]
        a = b = i
        while a > 0 and self.chain[a - 1] == c:
            a -= 1
        while b < len(self.chain) - 1 and self.chain[b + 1] == c:
            b += 1
        n = b - a + 1
        if n < need:
            return 0
        sp = self.S(self.R) * 2
        for k in range(a, b + 1):
            x, y = self.at(self.head - k * sp)
            self.fx.sparks(x, y, 6, _mix(PL_COLORS[c], WHITE, 0.4), (150, 450), (0, 360), (0.2, 0.4), 300, "front", 3, 12)
        x, y = self.at(self.head - (a + b) / 2 * sp)
        self.fx.glow(x, y, 20, 90, (255, 240, 200), 0.3, "front", 0.9, 0.0)
        del self.chain[a:b + 1]
        self.head -= n * sp * 0.5                                      # the chain closes up / la chaîne se resserre
        self.pops_n += 1
        self.balls_n += n
        return n

    def update(self, vals, now):
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0] and self.chain:                        # points: a group bursts / des points : un groupe éclate
            i = self.rng.randrange(len(self.chain))
            if not self.burst_at(i, now, 2):
                self.chain[i + 1:i + 1] = [self.chain[i]] * 2
                self.burst_at(i, now)
            self.popup(str(int(ch[1] - ch[0])) if ch[1] - ch[0] < 100000 else "BURST", self.center[0], self.center[1] - self.S(90), GOLD, 30)

    def always(self, vals, now):
        S, rng, dt = self.S, self.rng, self.dt
        sp = S(self.R) * 2
        self.head += S(30) * dt
        if self.head >= self.length:                                   # the chain reaches the hole: it starts again
            self.resets += 1
            self.fx.flash((200, 120, 255), 0.3, 0.3)
            self.fill(now)
        while len(self.chain) < 90 and self.head - len(self.chain) * sp > -sp:      # the chain keeps coming in / elle continue d'entrer
            self.chain.append(rng.randrange(4))
        if self.shot is None and now >= self.next_shot and self.chain:
            vis = [k for k in range(len(self.chain)) if self.head - k * sp > 0]
            if vis:
                k = rng.choice(vis)
                tx, ty = self.at(self.head - k * sp)
                col = self.chain[k] if rng.random() < 0.7 else rng.randrange(4)
                self.aim = math.atan2(ty - self.center[1], tx - self.center[0])
                self.shot = {"x": self.center[0], "y": self.center[1], "k": k, "col": col, "t0": now, "tx": tx, "ty": ty}
        if self.shot is not None:
            sh = self.shot
            dist = math.hypot(sh["tx"] - sh["x"], sh["ty"] - sh["y"])
            step = S(1400) * dt
            if dist <= step:                                           # in the chain / dans la chaîne
                k = min(sh["k"], len(self.chain))
                self.chain.insert(k, sh["col"])
                self.burst_at(k, now)
                self.shot = None
                self.next_shot = now + rng.uniform(0.4, 0.9)
            else:
                sh["x"] += (sh["tx"] - sh["x"]) / dist * step
                sh["y"] += (sh["ty"] - sh["y"]) / dist * step

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        sp = S(self.R) * 2
        for k, c in enumerate(self.chain):
            d = self.head - k * sp
            if d < 0:
                break
            img = self.ball_img(c)
            x, y = self.at(d)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        cx, cy = self.center                                           # the launcher turns / le lanceur tourne
        ex, ey = cx + math.cos(self.aim) * S(60), cy + math.sin(self.aim) * S(60)
        pg.draw.line(screen, (240, 220, 140), (int(cx), int(cy)), (int(ex), int(ey)), max(3, S(14)))
        pg.draw.circle(screen, (120, 80, 170), (int(cx), int(cy)), S(34))
        pg.draw.circle(screen, (240, 220, 140), (int(cx), int(cy)), S(34), max(2, S(4)))
        if self.shot is not None:
            img = self.ball_img(self.shot["col"])
            screen.blit(img, (int(self.shot["x"] - img.get_width() / 2), int(self.shot["y"] - img.get_height() / 2)))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the count of the balls burst at the top left, the score at the top right. / Le compte des
        boules éclatées en haut à gauche, le score en haut à droite."""
        S, W, hd = self.S, self.W, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(420), S(80), now)
        self.pill(screen, S(14), S(8), S(300), S(70), 170, radius=12)
        self.text(screen, "BALLS", S(32), S(43), 24, (255, 200, 120), key="black", valign="middle")
        hd.put_number(screen, f"{self.balls_n:04d}", "black", S(40), WHITE, S(300), S(43), "right", "middle")
        if _n(vals.get("score")) is not None:
            self.pill(screen, W - S(334), S(8), S(320), S(70), 170, radius=12)
            self.text(screen, "SCORE", W - S(316), S(43), 24, (255, 200, 120), key="black", valign="middle")
            hd._score(screen, eng, "score", W - S(30), S(16), "right", S(40))
        elif not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 28, col, align="right")


# ============================================================================ Capcom Sports Club
class SportsClubScene(SoccerScene):
    """Capcom Sports Club as in the game: the football match in the stadium in the late afternoon, the flags on the roof;
    the two flags of the teams of our own at the top and the time of the match between them, as in the game.
    / Le match de football dans le stade en fin d'après-midi, les drapeaux sur le toit ; les deux drapeaux des
    équipes à nous en haut et le temps du match entre eux, comme dans le jeu."""
    THEME = "cs_pitch"
    KITS = kits(((60, 120, 230), (250, 250, 250)), ((250, 250, 250), (40, 60, 160)))

    def scoreboard(self, screen, vals, now):
        S = self.S
        for side, x, kit in (("p1", S(30), self.KITS[0]), ("p2", S(330), self.KITS[1])):
            self.pill(screen, x - S(10), S(10), S(130), S(70), 160, radius=12)
            screen.blit(self.img(("csflag", side), S(90), S(52), flag_draw(kit), ss=1), (x + S(10), S(19)))
        t = _n(vals.get("time"))
        if t is not None:
            t = int(t)
            self.label(screen, f"{t // 60}'{t % 60:02d}\"" if t >= 60 else f"{t:02d}\"", S(270), S(45), 32, WHITE, key="black", align="center")


# ============================================================================ the quizzes / les quiz
class QuizDragonsScene(QuizScene):
    """Quiz & Dragons as in the game: the hall of the dungeon and its red dragon painted on the wall, a knight and a
    wizard of our own, the green panel and its four answers; a good answer is a big circle, a wrong one a big cross
    and a life lost. The questions are our own. / La salle du donjon et son dragon rouge peint au mur, un chevalier et
    un magicien à nous, le panneau vert et ses quatre réponses. Les questions sont à nous."""
    THEME = "qd_dungeon"
    PANEL = (30, 110, 60)
    FACES = (((230, 190, 150), (90, 60, 40), None, (150, 156, 170), (70, 70, 90)), ((236, 200, 170), (230, 230, 230), None, (110, 60, 160),
                                                                                    (60, 40, 90)))


class CapcomWorldScene(QuizScene):
    """Capcom World 2 as in the game: the board of the adventure, its lands, its sea and its path of squares, two little
    adventurers of our own, the blue panel and its four answers. The questions are our own. / Le plateau de
    l'aventure, ses terres, sa mer et son chemin de cases, deux petits aventuriers à nous, le panneau bleu."""
    THEME = "cw_board"
    PANEL = (40, 60, 190)
    FACES = (((250, 210, 180), (220, 80, 40), (250, 220, 60), None, (250, 140, 60)), ((250, 214, 180), (40, 40, 60), None, (60, 160, 90), (90, 180, 240)))


SCENES = {"spf2t": PuzzleFighterScene, "pzloop2": PuzzLoopScene, "csclub": SportsClubScene, "qad": QuizDragonsScene,
          "cworld2j": CapcomWorldScene}
