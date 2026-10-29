"""HD scenes of the ninth batch of Neo Geo games done one by one (1.25), each drawn after screenshots of its game.
Each game has its own animated backdrop and reacts to the values read in its memory. The players, the horses and the
little creatures are creations of the program in the spirit of the games.

Scènes HD du neuvième lot de jeux Neo Geo faits un par un (1.25), chacune dessinée d'après des captures de son jeu.
Les joueurs, les chevaux et les petites créatures sont des créations du programme dans l'esprit des jeux.
"""

import math

from .hd_games import CREAM, GOLD, P1C, P2C, WHITE, GameScene, PuzzleBobbleScene, _clamp, _n
from .hd_games3 import _capsule
from .hd_games4 import RallyScene, dodger_draw
from .hd_games5 import _mixc
from .hd_games6 import PuzzleBobble2Scene
from .hd_themes9 import BB_COURT, FS_COURT, HORSE_TRACK, PZ_CELL, PZ_COLS, PZ_ROWS, PZ_TOP, PZ_WELLS   # (and the backdrops)
from .i18n import tr

DARKLINE = (24, 20, 26, 255)


def _digits(vals, tens, units):
    """A number kept as two digits in two bytes. / Un nombre gardé en deux chiffres, un par octet."""
    t, u = _n(vals.get(tens)), _n(vals.get(units))
    if t is None or u is None:
        return None
    return int(t) % 10 * 10 + int(u) % 10


# ============================================================================ Bang Bead, Battle Flip Shot
def duel_ball_draw(c1, c2):
    """A ball in two colours, with its shine. / Un ballon de deux couleurs, et son reflet."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.06))
        d.ellipse([0, 0, W - 1, H - 1], fill=c1 + (255,))
        d.pieslice([0, 0, W - 1, H - 1], 200, 290, fill=c2 + (255,))
        d.pieslice([0, 0, W - 1, H - 1], 20, 110, fill=c2 + (255,))
        d.ellipse([W * 0.22, H * 0.16, W * 0.44, H * 0.34], fill=(255, 255, 255, 210))
        d.ellipse([0, 0, W - 1, H - 1], outline=DARKLINE, width=ow)
    return fn


def energy_ball_draw(d, W, H):
    """The glowing ball of Battle Flip Shot. / La balle lumineuse."""
    for i in range(10):
        k = i / 10
        r = W / 2 * (1 - k * 0.8)
        d.ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], fill=_mixc((240, 60, 140), (255, 255, 255), k))


def shield_draw(color):
    """A round-topped shield held in front. / Un bouclier arrondi tenu devant."""
    def fn(d, W, H):
        d.rounded_rectangle([W * 0.08, H * 0.02, W * 0.92, H * 0.98], radius=W * 0.42, fill=color + (255,), outline=DARKLINE,
                            width=max(1, int(W * 0.1)))
        d.rounded_rectangle([W * 0.34, H * 0.12, W * 0.62, H * 0.88], radius=W * 0.14, fill=_mixc(color, (255, 255, 255), 0.45))
        d.ellipse([W * 0.36, H * 0.42, W * 0.64, H * 0.58], fill=(250, 210, 60, 255), outline=DARKLINE)
    return fn


class CourtDuelScene(GameScene):
    """Two players face to face on a court seen from above, one ball goes from one to the other, off the walls; the one
    who misses lets it into his goal. / Deux joueurs face à face sur un terrain vu du dessus, une balle va de l'un à
    l'autre ; celui qui la rate la laisse entrer dans son but."""
    STATIC = True
    SHADE = (90, 0)
    PILLS = True
    COURT = BB_COURT
    LOOKS = {"p1": ((220, 50, 50), (40, 60, 140), (250, 220, 60), (240, 196, 160), (60, 40, 30), 0, 1.0),
             "p2": ((250, 200, 40), (40, 40, 50), (220, 60, 60), (200, 150, 110), (30, 30, 40), 1, 1.1)}
    REACH = 66
    SPEED = 880

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.top, self.bot = S(self.COURT[0]) + S(34), S(self.COURT[1]) - S(30)
        self.px = {"p1": S(240), "p2": self.W - S(240)}
        mid = (self.top + self.bot) / 2
        self.py = {"p1": mid, "p2": mid}
        self.vy = {"p1": 0.0, "p2": 0.0}
        self.hit_t = {"p1": -9.0, "p2": -9.0}
        self.ball = None
        self.wait = 0.0
        self.serve = "p1"
        self.goals = 0                                   # (tests)
        self.hits = 0
        self.supers = 0
        self.trail = []
        self.rally = 0

    def restart(self, vals, now):
        self.ball, self.trail = None, []
        self.wait = now + 0.6

    def fig_h(self):
        return self.S(150)

    def predict(self, b, x):
        """Where the ball will cross the line x, off the walls. / Où la balle croisera la ligne x, rebonds compris."""
        if b["vx"] == 0:
            return b["y"]
        t = (x - b["x"]) / b["vx"]
        if t < 0:
            return b["y"]
        y = b["y"] + b["vy"] * t
        lo, hi = self.top, self.bot
        span = hi - lo
        k = (y - lo) % (2 * span)
        return lo + (k if k <= span else 2 * span - k)

    def launch(self, frm, now, fire=False, miss=None, ty=None):
        """The ball leaves the player frm. miss: the other one will not reach it. / La balle part du joueur frm."""
        S = self.S
        d = 1 if frm == "p1" else -1
        x0, y0 = self.px[frm] + d * S(64), self.py[frm]
        x1 = self.px["p2" if frm == "p1" else "p1"]
        if ty is None:
            ty = self.rng.uniform(self.top + S(10), self.bot - S(10))
        speed = S(self.SPEED) * (1.5 if fire else self.rng.uniform(0.9, 1.15))
        dist = abs(x1 - x0)
        t = dist / speed
        if self.rng.random() < 0.45 and not fire:                       # off a wall / par un mur
            wall = self.top if self.rng.random() < 0.5 else self.bot
            vy = ((wall - y0) + (wall - ty)) / t
        else:
            vy = (ty - y0) / t
        if miss is None:                                                # never a rally of more than five / pas d'échange de plus de cinq
            miss = self.rally >= 4 or self.rng.random() < 0.16
        self.rally = 0 if miss else self.rally + 1
        self.ball = {"x": x0, "y": y0, "vx": d * speed, "vy": vy, "fire": fire, "to": "p2" if frm == "p1" else "p1", "miss": miss,
                     "from": frm}
        self.hit_t[frm] = now
        if fire:
            self.supers += 1

    def strike(self, frm, now, fire=False, ty=None):
        """A shot that goes in, for an event read in the game. / Un tir qui rentre, pour un événement lu dans le jeu."""
        self.launch(frm, now, fire, True, ty)

    def scored(self, scorer, x, y, now):
        """The ball went into the goal of the other one. / La balle est entrée dans le but de l'autre."""

    def update(self, vals, now):
        S, dt = self.S, self.dt
        b = self.ball
        if b is None and now >= self.wait:
            self.launch(self.serve, now)
            b = self.ball
        for side in ("p1", "p2"):                                        # the players go to the ball / les joueurs vont à la balle
            target = (self.top + self.bot) / 2
            if b is not None and b["to"] == side:
                target = self.predict(b, self.px[side])
                if b["miss"]:
                    target += S(self.REACH) * 2.2 * (1 if target < (self.top + self.bot) / 2 else -1)
            st = self.stick(vals, side)
            if st is not None and st[1]:
                target = self.py[side] + st[1] * S(200)
            v = _clamp((target - self.py[side]) * 6, -S(560), S(560))
            self.vy[side] = v
            self.py[side] = _clamp(self.py[side] + v * dt, self.top, self.bot)
        if b is None:
            return
        b["x"] += b["vx"] * dt
        b["y"] += b["vy"] * dt
        if b["y"] < self.top:
            b["y"], b["vy"] = 2 * self.top - b["y"], -b["vy"]
        if b["y"] > self.bot:
            b["y"], b["vy"] = 2 * self.bot - b["y"], -b["vy"]
        self.trail = (self.trail + [(b["x"], b["y"])])[-8:]
        to = b["to"]
        line = self.px[to] + (S(56) if to == "p1" else -S(56))
        crossed = b["x"] <= line if to == "p1" else b["x"] >= line
        if crossed and not b.get("past"):
            if not b["miss"] and abs(self.py[to] - b["y"]) < S(self.REACH):           # sent back / renvoyée
                self.hits += 1
                self.fx.glow(b["x"], b["y"], 16, 80, (120, 220, 255), 0.25, "front", 0.9, 0.0)
                self.fx.sparks(b["x"], b["y"], 10, (180, 240, 255), (200, 500), (0, 360), (0.15, 0.35), 0, "front", 3, 10)
                self.launch(to, now)
                return
            b["past"] = True
        goal_x = S(60) if to == "p1" else self.W - S(60)
        if (to == "p1" and b["x"] <= goal_x) or (to == "p2" and b["x"] >= goal_x):
            self.goals += 1
            scorer = "p2" if to == "p1" else "p1"
            self.scored(scorer, goal_x, b["y"], now)
            self.ball, self.trail = None, []
            self.serve = to
            self.wait = now + 1.3

    def player_img(self, side, now):
        S = self.S
        h = self.fig_h()
        shirt, pants, acc, skin, hair, style, build = self.LOOKS[side]
        b = self.ball
        if now - self.hit_t[side] < 0.22:
            frame = 4
        elif b is not None and b["to"] == side and abs(b["x"] - self.px[side]) < S(260):
            frame = 3
        elif abs(self.vy[side]) > S(90):
            frame = 1 + int(now * 8) % 2
        else:
            frame = 0
        return self.img(("duel", side, frame), int(h * 0.9), h, dodger_draw(shirt, pants, acc, skin, hair, style, build, frame), ss=2,
                        flip=side == "p2")

    def draw_extra(self, screen, side, x, y, now):
        """What the player holds. / Ce que tient le joueur."""

    def ball_img(self, fire):
        return self.img("duelball", self.S(40), self.S(40), duel_ball_draw((250, 220, 40), (40, 110, 230)))

    def draw_court(self, screen, vals, now):
        """The players and the ball, sorted by depth. / Les joueurs et la balle, dans l'ordre de profondeur."""
        S, pg = self.S, self.pg
        items = []
        for side in ("p1", "p2"):
            items.append((self.py[side], "p", side))
        b = self.ball
        if b is not None:
            items.append((b["y"], "b", None))
        h = self.fig_h()
        for y, kind, side in sorted(items, key=lambda it: it[0]):
            if kind == "p":
                x = self.px[side]
                sh = self.imgs.get("duelsh")
                if sh is None:
                    sh = self.imgs["duelsh"] = pg.Surface((S(90), S(26)), pg.SRCALPHA)
                    pg.draw.ellipse(sh, (0, 0, 0, 90), sh.get_rect())
                screen.blit(sh, (int(x - sh.get_width() / 2), int(y + h * 0.36)))
                img = self.player_img(side, now)
                screen.blit(img, (int(x - img.get_width() / 2), int(y - h * 0.5)))
                self.draw_extra(screen, side, x, y, now)
            else:
                for i, (tx, ty) in enumerate(self.trail[:-1]):
                    g = self.fx.sp.glow(S(14), (255, 170, 60) if b["fire"] else (200, 230, 255), 2 + i, hot=0.3)
                    screen.blit(g, (int(tx - g.get_width() / 2), int(ty - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
                img = self.ball_img(b["fire"])
                if b["fire"]:
                    self.fx.sparks(b["x"], b["y"], 2, (255, 160, 40), (60, 160), (0, 360), (0.2, 0.4), 0, "front", 5, 16)
                screen.blit(img, (int(b["x"] - img.get_width() / 2), int(b["y"] - img.get_height() / 2)))

    def time_box(self, screen, t, now):
        S, W = self.S, self.W
        if t is None:
            return
        low = t <= 10
        self.pill(screen, W / 2 - S(90), S(116), S(180), S(70), 170, radius=14)
        self.text(screen, "TIME", W / 2 - S(74), S(151), 22, (250, 210, 80), key="black", valign="middle", glow=0)
        self.hd.put_number(screen, f"{int(t):02d}", "black", S(52), (255, 80, 60) if low and int(now * 4) % 2 else WHITE, W / 2 + S(70), S(151),
                           "right", "middle")


class BangBeadScene(CourtDuelScene):
    """Bang Bead as in the game: the street court seen from above, the cars parked along the pavement, two players of
    our own hit the ball from one end to the other, the goal lines and their yellow stars light up at each goal. A
    'Miracle' power spent in the game is a shot on fire. PLAYER and the score, TIME in the middle, the power gauges at
    the bottom. / La rue vue du dessus, deux joueurs à nous se renvoient la balle, les lignes de but et leurs étoiles
    s'allument à chaque but, le pouvoir 'Miracle' dépensé dans le jeu est un tir en feu, comme dans le jeu."""
    THEME = "bb_street"
    COURT = BB_COURT
    BANNERS = GameScene.BANNERS + (("GOAL!", GOLD),)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.lit = {"p1": -9.0, "p2": -9.0}

    def update(self, vals, now):
        super().update(vals, now)
        for side, suf in (("p1", ""), ("p2", "_p2")):
            ch = self.changed(vals, "stock" + suf)
            if ch and ch[1] < ch[0]:                                     # a Miracle spent: a shot on fire
                self.strike(side, now, fire=True)
                self.popup("MIRACLE SHOT!", self.px[side], self.S(250), (255, 160, 60), 40)
            ch = self.changed(vals, "score" + suf)
            if ch and ch[1] > ch[0] and (self.ball is None or not self.ball["miss"]):
                self.strike(side, now)

    def scored(self, scorer, x, y, now):
        S = self.S
        self.lit[scorer] = now
        self.fx.glow(x, y, 30, 160, (255, 230, 120), 0.5, "front", 1.0, 0.0)
        self.fx.sparks(x, y, 30, (255, 220, 80), (250, 700), (90, 270) if x < self.W / 2 else (-90, 90), (0.3, 0.6), 400, "front", 4, 20)
        self.fx.shake(6, 0.3)
        self.popup("GOAL!", x + (S(160) if x < self.W / 2 else -S(160)), y, GOLD, 50)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        for scorer, gx in (("p1", W - S(60)), ("p2", S(60))):            # the goal line lights up / la ligne de but s'allume
            k = 1 - (now - self.lit[scorer]) / 0.9
            if k > 0:
                band = self.imgs.get("bbband")
                if band is None:
                    band = self.imgs["bbband"] = pg.Surface((S(70), int(self.bot - self.top + S(60)))).convert()
                band.fill((int(255 * k), int(200 * k), int(60 * k)))
                screen.blit(band, (int(gx - S(35)), int(self.top - S(30))), special_flags=pg.BLEND_RGB_ADD)
        self.draw_court(screen, vals, now)
        self.top_bar(screen, eng, vals, logo, now)
        self.time_box(screen, _digits(vals, "time_tens", "time_units"), now)
        for side, suf, x in (("p1", "", S(30)), ("p2", "_p2", W - S(370))):
            p = _n(vals.get("power" + suf))
            if p is None or (side == "p2" and not self.p2_in(vals)):
                continue
            self.pill(screen, x - S(10), self.H - S(54), S(360), S(46), 170, radius=12)
            self.text(screen, "POWER", x + S(4), self.H - S(31), 20, (250, 210, 80), key="black", valign="middle", glow=0)
            self.bar(screen, x + S(92), self.H - S(42), S(180), S(22), p / 128.0, (255, 110, 40))
            st = _n(vals.get("stock" + suf))
            if st is not None:
                for k in range(3):
                    col = (255, 220, 60) if k < st else (70, 60, 50)
                    cx, cy = x + S(296) + k * S(20), self.H - S(31)
                    pts = [(cx + math.cos(-math.pi / 2 + i * math.pi / 5) * (S(9) if i % 2 == 0 else S(4)),
                            cy + math.sin(-math.pi / 2 + i * math.pi / 5) * (S(9) if i % 2 == 0 else S(4))) for i in range(10)]
                    pg.draw.polygon(screen, col, [(int(a), int(b)) for a, b in pts])


class FlipShotScene(CourtDuelScene):
    """Battle Flip Shot as in the game: the arena of teal metal seen from above, the big orange target in the middle,
    two players of our own behind their shields send the glowing ball back, the six targets of each player along his
    wall crack and break. A target hit in the game is a shot on it. SCORE and TIME at the top.
    / L'arène de métal vue du dessus, deux joueurs à nous derrière leurs boucliers renvoient la balle lumineuse, les six
    cibles de chaque joueur le long de son mur se fissurent et cassent, comme dans le jeu."""
    THEME = "fs_arena"
    COURT = FS_COURT
    LOOKS = {"p1": ((60, 90, 200), (40, 40, 60), (250, 220, 60), (240, 196, 160), (250, 220, 120), 3, 1.0),
             "p2": ((230, 230, 240), (60, 60, 70), (220, 60, 60), (210, 160, 120), (40, 30, 30), 4, 1.05)}
    SPEED = 960
    BANNERS = GameScene.BANNERS + (("ROUND CLEAR", GOLD),)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.cracks = {"p1": [0] * 6, "p2": [0] * 6}
        self.broken = 0                                  # (tests)
        self.last_t = None

    def target_y(self, k):
        return self.top - self.S(10) + (k + 0.5) * (self.bot - self.top + self.S(20)) / 6

    def update(self, vals, now):
        super().update(vals, now)
        for side, suf, frm in (("p1", "", "p2"), ("p2", "_p2", "p1")):
            for k in range(6):
                ch = self.changed(vals, f"target{k + 1}{suf}")
                if ch:                                                   # a target hit in the game / une cible touchée
                    self.strike(frm, now, ty=self.target_y(k))
        t = _n(vals.get("time"))
        if t is not None and self.last_t is not None and t > self.last_t + 5:  # a new round: new targets
            self.cracks = {"p1": [0] * 6, "p2": [0] * 6}
        self.last_t = t

    def scored(self, scorer, x, y, now):
        S = self.S
        side = "p2" if scorer == "p1" else "p1"
        k = min(range(6), key=lambda i: abs(self.target_y(i) - y))
        cr = self.cracks[side]
        if cr[k] >= 3:
            k = min(range(6), key=lambda i: (cr[i] >= 3, abs(self.target_y(i) - y)))
        cr[k] = min(3, cr[k] + 1)
        tx = S(44) if side == "p1" else self.W - S(44)
        ty = self.target_y(k)
        self.fx.sparks(tx, ty, 18, (255, 120, 220), (200, 600), (0, 360), (0.2, 0.5), 300, "front", 4, 16)
        if cr[k] >= 3:
            self.broken += 1
            self.fx.glow(tx, ty, 24, 140, (255, 140, 230), 0.4, "front", 1.0, 0.0)
            self.fx.shake(5, 0.25)
            self.popup(tr("CIBLE !", "TARGET!"), tx + (S(170) if side == "p1" else -S(170)), ty, (255, 140, 230), 40)
            if all(c >= 3 for c in cr):
                self.slam("ROUND CLEAR", GOLD, now, 1.6)
                self.cracks = {"p1": [0] * 6, "p2": [0] * 6}

    def ball_img(self, fire):
        return self.img("fsball", self.S(36), self.S(36), energy_ball_draw)

    def draw_extra(self, screen, side, x, y, now):
        S = self.S
        sh = self.img(("fsshield", side), S(34), S(78), shield_draw((90, 130, 220) if side == "p1" else (200, 70, 70)), ss=2)
        d = 1 if side == "p1" else -1
        screen.blit(sh, (int(x + d * S(46) - sh.get_width() / 2), int(y - sh.get_height() / 2 - S(4))))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        for side, x in (("p1", S(44)), ("p2", W - S(44))):              # the targets along each wall / les cibles
            for k in range(6):
                c = self.cracks[side][k]
                y = self.target_y(k)
                if c >= 3:
                    pg.draw.rect(screen, (60, 50, 70), (int(x - S(16)), int(y - S(20)), S(32), S(40)), border_radius=S(6))
                    continue
                col = (190, 90, 230) if side == "p1" else (240, 140, 40)
                pg.draw.rect(screen, col, (int(x - S(16)), int(y - S(22)), S(32), S(44)), border_radius=S(6))
                pg.draw.rect(screen, (30, 20, 40), (int(x - S(16)), int(y - S(22)), S(32), S(44)), max(1, S(3)), border_radius=S(6))
                pg.draw.rect(screen, _mixc(col, (255, 255, 255), 0.5)[:3], (int(x - S(8)), int(y - S(16)), S(8), S(30)), border_radius=S(3))
                for j in range(c):                                       # the cracks / les fissures
                    a = j * 2.1 + 0.4
                    pg.draw.line(screen, (20, 10, 20), (int(x), int(y)), (int(x + math.cos(a) * S(15)), int(y + math.sin(a) * S(20))), max(1, S(3)))
        self.draw_court(screen, vals, now)
        self.top_bar(screen, eng, vals, logo, now)
        t = _n(vals.get("time"))
        if t is not None:
            self.time_box(screen, min(99, t), now)


# ============================================================================ Over Top
OT_MAP = [(0.1, 0.8), (0.1, 0.3), (0.3, 0.12), (0.6, 0.2), (0.62, 0.5), (0.85, 0.55), (0.9, 0.85), (0.5, 0.9), (0.1, 0.8)]


class OverTopScene(RallyScene):
    """Over Top as in the game: the stages seen from the sky, a dirt track through the pine forest, then a grey road
    between the fields, the red car among its rivals; the map in its little television at the top left, the time in
    big yellow numbers, the rank, the speedometer and the lap time. / Les étapes vues du ciel, la voiture rouge parmi
    ses rivales, la carte dans sa petite télévision, le temps en gros chiffres jaunes, le rang, le compteur, comme dans le jeu."""
    THEME = "ot_forest"
    THEMES = ("ot_forest", "ot_road")
    CARS = {"p1": ((220, 40, 40), (250, 250, 250)), "p2": ((40, 150, 220), (250, 250, 250))}
    RIVALS = (((40, 90, 200), (250, 250, 250)), ((240, 240, 240), (40, 40, 40)), ((250, 200, 30), (40, 40, 40)))
    DUST = (150, 120, 80)
    DUSTS = {"ot_forest": (150, 120, 80), "ot_road": (150, 150, 156)}
    NEW_STAGE = 25.0

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.overtakes = 0                               # (tests)

    def pace(self, vals):
        v = _n(vals.get("speed"))
        return 1.0 if v is None else 0.45 + _clamp(v / 255.0) * 0.8

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "rank")
        if ch and ch[1] < ch[0]:                                         # one place up: a rival overtaken
            self.overtakes += 1
            self.rivals.append({"x": self.W * 0.45, "lat": self.rng.choice((-0.45, 0.45)), "col": self.rng.choice(self.RIVALS), "v": 0.3})
            self.popup(tr("DÉPASSEMENT !", "OVERTAKE!"), self.W * 0.3, self.S(220), (255, 220, 60), 40)

    def status(self, screen, eng, vals, logo, now):
        S, W, H, hd, pg = self.S, self.W, self.H, self.hd, self.pg
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(92), now)
        tx, ty, tw, th = S(18), S(10), S(190), S(140)                    # the map in its little television
        pg.draw.rect(screen, (60, 60, 66), (tx, ty, tw, th), border_radius=S(18))
        pg.draw.rect(screen, (20, 20, 24), (tx, ty, tw, th), max(1, S(3)), border_radius=S(18))
        sx, sy, sw, sh = tx + S(14), ty + S(14), tw - S(40), th - S(28)
        pg.draw.rect(screen, (90, 170, 80), (sx, sy, sw, sh), border_radius=S(8))
        pts = [(int(sx + px * sw), int(sy + py * sh)) for px, py in OT_MAP]
        pg.draw.lines(screen, (230, 150, 50), False, pts, max(2, S(6)))
        k = (now * 0.05) % 1.0 * (len(OT_MAP) - 1)
        i = int(k)
        f = k - i
        cx = OT_MAP[i][0] + (OT_MAP[i + 1][0] - OT_MAP[i][0]) * f
        cy = OT_MAP[i][1] + (OT_MAP[i + 1][1] - OT_MAP[i][1]) * f
        pg.draw.circle(screen, (250, 60, 50), (int(sx + cx * sw), int(sy + cy * sh)), S(7))
        for k2 in range(3):
            pg.draw.circle(screen, (30, 30, 34), (int(tx + tw - S(13)), int(ty + S(40) + k2 * S(26))), S(6))
        t = self.secs(vals)
        if t is not None:                                                # the time, big yellow numbers
            low = t < 10
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(92), (255, 80, 60) if low and int(now * 4) % 2 else (255, 220, 40), S(330), S(60),
                          "center", "middle")
        r = _n(vals.get("rank"))
        if r is not None:                                                # RANK n/4
            self.pill(screen, S(440), S(14), S(150), S(92), 160, radius=14)
            self.text(screen, "RANK", S(515), S(36), 22, (120, 220, 255), key="black", align="center", valign="middle", glow=0)
            hd.put_number(screen, f"{int(r)}/4", "black", S(46), WHITE, S(515), S(76), "center", "middle")
        v = _n(vals.get("speed"))
        if v is not None:                                                # the speedometer
            cx, cy, rr = W - S(110), H - S(100), S(84)
            pg.draw.circle(screen, (20, 20, 24), (int(cx), int(cy)), rr + S(6))
            pg.draw.circle(screen, (240, 240, 236), (int(cx), int(cy)), rr)
            for k3 in range(11):
                a = math.radians(225 - k3 * 27)
                pg.draw.line(screen, (30, 30, 30), (int(cx + math.cos(a) * rr * 0.78), int(cy - math.sin(a) * rr * 0.78)),
                             (int(cx + math.cos(a) * rr * 0.94), int(cy - math.sin(a) * rr * 0.94)), max(1, S(3)))
            a = math.radians(225 - _clamp(v / 255.0) * 270)
            pg.draw.line(screen, (220, 40, 40), (int(cx), int(cy)), (int(cx + math.cos(a) * rr * 0.86), int(cy - math.sin(a) * rr * 0.86)), max(2, S(5)))
            pg.draw.circle(screen, (30, 30, 30), (int(cx), int(cy)), S(9))
            self.text(screen, f"{int(v * 300 / 255)}", cx, cy + S(40), 20, (30, 30, 30), key="black", align="center", valign="middle", glow=0)
        lm, ls, lc = (_n(vals.get(n)) for n in ("lap_min", "lap_sec", "lap_cs"))
        if lm is not None and ls is not None:                            # LAP TIME
            self.label(screen, f"LAP {int(lm)}'{int(ls):02d}\"{int(lc or 0):02d}", S(24), H - S(34), 26, WHITE, align="left")
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, W - S(200), S(44), 30, colw, align="center")


# ============================================================================ Stakes Winner, Stakes Winner 2, Jockey Grand Prix
# leg angles in degrees from straight down, + forward: front near, front far, hind near, hind far / angles des jambes
GALLOP = (((50, 75), (38, 62), (-48, -66), (-36, -54)),      # stretched / allongé
          ((-8, -78), (8, -40), (12, 26), (0, 14)),         # hind legs land / l'arrière se pose
          ((-26, -6), (-14, 10), (30, 8), (18, -4)),        # gathered / rassemblé
          ((26, -40), (40, -16), (-22, -42), (-10, -30)))   # push / poussée
BOUNCE = (-0.03, 0.0, 0.025, 0.0)
COATS = ((130, 72, 40), (170, 92, 44), (52, 40, 34), (186, 180, 176), (96, 56, 34), (150, 104, 60))
SILKS = (((230, 40, 40), (250, 250, 250), (230, 40, 40)), ((40, 90, 220), (250, 220, 40), (250, 220, 40)),
         ((250, 250, 250), (40, 40, 40), (40, 40, 40)), ((250, 200, 30), (40, 140, 70), (40, 140, 70)),
         ((40, 160, 80), (250, 250, 250), (250, 250, 250)), ((240, 120, 30), (40, 60, 160), (40, 60, 160)),
         ((160, 60, 200), (250, 220, 40), (160, 60, 200)), ((250, 130, 170), (40, 40, 40), (250, 250, 250)))


def horse_draw(coat, silk, sleeve, cap, frame, number=None, fontf=None):
    """A race horse and its jockey of our own seen from the side, galloping to the right: frames 0 to 3 of the gallop,
    the jockey crouched with his silks and cap, the saddle cloth and its number. / Un cheval de course et son jockey à
    nous, de profil, au galop vers la droite : quatre images du galop, le jockey et sa casaque, le tapis et son numéro."""
    def fn(d, W, H):
        ow = max(1.0, H * 0.012)
        dark = DARKLINE
        body, body_d = coat + (255,), _mixc(coat, (0, 0, 0), 0.3)
        mane = _mixc(coat, (0, 0, 0), 0.6)
        b = BOUNCE[frame] * H
        hip, sho = (W * 0.3, H * 0.5 + b), (W * 0.66, H * 0.5 + b)
        up, lo = H * 0.17, H * 0.18

        def leg(root, angles, far):
            a1, a2 = (math.radians(a) for a in angles)
            knee = (root[0] + math.sin(a1) * up, root[1] + math.cos(a1) * up)
            hoof = (knee[0] + math.sin(a2) * lo, knee[1] + math.cos(a2) * lo)
            col = body_d if far else body
            _capsule(d, root, knee, H * 0.075, H * 0.05, col, dark, ow)
            _capsule(d, knee, hoof, H * 0.04, H * 0.032, col, dark, ow)
            d.ellipse([hoof[0] - H * 0.024, hoof[1] - H * 0.016, hoof[0] + H * 0.03, hoof[1] + H * 0.024], fill=(40, 34, 30, 255))
        fn_, ff, hn, hf = GALLOP[frame]
        leg(sho, ff, True)
        leg(hip, hf, True)
        d.polygon([(W * 0.24, H * 0.44 + b), (W * 0.06, H * (0.5 + 0.06 * math.sin(frame * 1.6))) , (W * 0.1, H * 0.68 + b),
                   (W * 0.2, H * 0.56 + b)], fill=mane, outline=dark)                              # la queue
        d.ellipse([W * 0.18, H * 0.36 + b, W * 0.76, H * 0.64 + b], fill=body, outline=dark, width=int(ow))   # le corps
        d.polygon([(W * 0.6, H * 0.42 + b), (W * 0.8, H * 0.16 + b), (W * 0.88, H * 0.22 + b), (W * 0.76, H * 0.52 + b)], fill=body,
                  outline=dark)                                                                    # l'encolure
        d.polygon([(W * 0.8, H * 0.12 + b), (W * 0.9, H * 0.14 + b), (W * 0.99, H * 0.3 + b), (W * 0.95, H * 0.35 + b),
                   (W * 0.86, H * 0.28 + b)], fill=body, outline=dark)                             # la tête
        d.polygon([(W * 0.8, H * 0.13 + b), (W * 0.81, H * 0.04 + b), (W * 0.85, H * 0.12 + b)], fill=body, outline=dark)  # l'oreille
        d.ellipse([W * 0.87, H * 0.17 + b, W * 0.895, H * 0.2 + b], fill=dark)
        d.line([(W * 0.62, H * 0.4 + b), (W * 0.8, H * 0.13 + b)], fill=mane, width=max(1, int(H * 0.03)))   # la crinière
        d.line([(W * 0.94, H * 0.3 + b), (W * 0.76, H * 0.36 + b)], fill=(240, 240, 240, 255), width=max(1, int(H * 0.008)))   # les rênes
        d.rectangle([W * 0.4, H * 0.38 + b, W * 0.56, H * 0.53 + b], fill=(250, 250, 250, 255), outline=dark)   # le tapis
        if number is not None and fontf is not None:
            d.text((W * 0.48, H * 0.455 + b), str(number), font=fontf(max(8, int(H * 0.11))), fill=(20, 20, 30, 255), anchor="mm")
        _capsule(d, (W * 0.46, H * 0.36 + b), (W * 0.54, H * 0.28 + b), H * 0.06, H * 0.05, (250, 250, 250, 255), dark, ow)   # la jambe
        _capsule(d, (W * 0.54, H * 0.28 + b), (W * 0.5, H * 0.4 + b), H * 0.05, H * 0.04, (250, 250, 250, 255), dark, ow)
        d.ellipse([W * 0.46, H * 0.38 + b, W * 0.53, H * 0.43 + b], fill=(30, 30, 30, 255))      # la botte
        _capsule(d, (W * 0.44, H * 0.27 + b), (W * 0.62, H * 0.2 + b), H * 0.09, H * 0.08, silk + (255,), dark, ow)   # le buste
        _capsule(d, (W * 0.6, H * 0.21 + b), (W * 0.74, H * 0.3 + b), H * 0.045, H * 0.04, sleeve + (255,), dark, ow)  # le bras
        d.ellipse([W * 0.62, H * 0.1 + b, W * 0.71, H * 0.2 + b], fill=(240, 200, 170, 255), outline=dark)       # la tête
        d.chord([W * 0.615, H * 0.08 + b, W * 0.715, H * 0.18 + b], 180, 360, fill=cap + (255,), outline=dark)    # la toque
        d.line([(W * 0.7, H * 0.13 + b), (W * 0.75, H * 0.135 + b)], fill=cap + (255,), width=max(1, int(H * 0.02)))
        leg(hip, hn, False)
        leg(sho, fn_, False)
    return fn


class HorseRaceScene(GameScene):
    """A horse race seen from the side: eight horses of our own gallop, the backdrop runs past, the player's horse
    wears its 1P; after a while the finish post comes, the winner is shown, a new race starts.
    / Une course vue de côté : huit chevaux à nous galopent, le cheval du joueur porte son 1P, l'arrivée, le vainqueur."""
    THEME = "sw_turf"
    SHADE = (60, 0)
    PILLS = True
    N = 8
    RUN = 22.0
    NUMBERS = False
    MARK = True
    BANNERS = GameScene.BANNERS + (("GOAL!", GOLD),)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.horses = []
        self.phase = "run"
        self.t0 = 0.0
        self.post = None
        self.dash = -9.0
        self.finishes = 0                                # (tests)
        self.dashes = 0
        self.winner = None
        self.new_race(0.0)
        self.warm += [(self.horse_img, (h, f, self.hsize(h))) for h in self.horses for f in range(4)]

    LANES = (4, 0, 6, 2, 7, 1, 5, 3)

    def new_race(self, now):
        rng = self.rng
        self.horses = []
        for i in range(self.N):                                           # each horse keeps its lane / chaque cheval garde son couloir
            self.horses.append({"n": i + 1, "z": self.LANES[i] / (self.N - 1), "pos": rng.uniform(-0.7, 0.5), "v": rng.uniform(0.9, 1.1),
                                "ph": rng.uniform(0, 4), "coat": COATS[i % len(COATS)], "silk": SILKS[i % len(SILKS)]})
        self.phase, self.t0, self.post, self.winner = "run", now, None, None

    def restart(self, vals, now):
        self.new_race(now)

    def move(self, vals, now, idle):
        return 0.6 if idle else (3.6 if self.phase != "pause" else 1.0)

    def surge(self, now, text):
        """The player's horse speeds up. / Le cheval du joueur accélère."""
        self.dash = now
        self.dashes += 1
        self.popup(text, self.W * 0.45, self.S(200), (255, 200, 60), 44)

    def update(self, vals, now):
        dt = self.dt
        for i, h in enumerate(self.horses):                              # the race: the horses close up and drift
            boost = 0.9 if i == 0 and now - self.dash < 1.6 else 0.0
            h["v"] += (self.rng.uniform(0.85, 1.15) - h["v"]) * dt * 0.6
            h["pos"] += (h["v"] - 1.0 + boost) * dt * 0.25
            h["pos"] = _clamp(h["pos"], -1.0, 1.0)
        if self.phase == "run" and now - self.t0 > self.RUN:
            self.phase = "finish"
            self.post = self.W + self.S(60)
        if self.phase == "finish":
            self.post -= self.bd.speed * dt * 1.0
            lead = max(self.horses, key=lambda h: h["pos"])
            if self.winner is None and self.post < self.hx(lead) + self.S(90):
                self.winner = lead["n"]
                self.finishes += 1
                self.slam("GOAL!", GOLD, now, 1.6, sub=f"No. {lead['n']}")
                self.fx.later(2.6, self._pause, now)
        if self.phase == "pause" and now - self.t0 > 1.4:
            self.new_race(now)

    def _pause(self, now):
        self.phase = "pause"
        self.t0 = self.fx.now

    def hx(self, h):
        return self.W * 0.48 + h["pos"] * self.W * 0.3

    def hy(self, h):
        t0, t1 = (self.S(v) for v in HORSE_TRACK)
        return t0 + self.S(30) + h["z"] * (t1 - t0 - self.S(46))

    def hsize(self, h):
        return int(self.S(150) * (0.82 + 0.26 * h["z"]) / 4) * 4

    def horse_img(self, h, frame, size):
        coat, (silk, sleeve, cap) = h["coat"], h["silk"]
        w, hh = int(size * 1.22), int(size)
        fontf = (lambda n: self.hd.font("black", n)) if self.NUMBERS else None
        return self.img(("horse", h["n"], frame, int(size)), w, hh,
                        horse_draw(coat, silk, sleeve, cap, frame, h["n"] if self.NUMBERS else None, fontf), ss=2)

    def draw_horses(self, screen, now):
        S, pg = self.S, self.pg
        speed = 2.6 if self.phase != "pause" else 1.2
        for h in sorted(self.horses, key=lambda h: h["z"]):
            x, y = self.hx(h), self.hy(h)
            size = self.hsize(h)
            frame = int(now * speed * 4 + h["ph"] * 4) % 4
            img = self.horse_img(h, frame, size)
            sh = self.imgs.get(("hsh", size))
            if sh is None:
                sh = self.imgs[("hsh", size)] = pg.Surface((int(size * 0.9), int(size * 0.14)), pg.SRCALPHA)
                pg.draw.ellipse(sh, (0, 0, 0, 70), sh.get_rect())
            screen.blit(sh, (int(x - sh.get_width() / 2), int(y - sh.get_height() / 2)))
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() * 0.9)))
            if int(now * 20) % 3 == 0 and self.phase != "pause":
                self.fx.smoke(x - img.get_width() * 0.3, y, 1, (4, 9), 1.8, (0.3, 0.6), (0, 10), 6, self.DUST, 120, "front")
            if h["n"] == 1 and self.MARK:                                # the player's horse / le cheval du joueur
                top = y - img.get_height() * 0.95
                pg.draw.polygon(screen, (255, 80, 60), [(int(x - S(18)), int(top - S(26))), (int(x + S(18)), int(top - S(26))), (int(x), int(top - S(4)))])
                self.label(screen, "1P", x, top - S(46), 30, (255, 230, 80), key="black", align="center", alpha=170)
                if now - self.dash < 1.0:
                    for k in range(5):
                        yy = top + S(30) + k * S(16)
                        pg.draw.line(screen, (255, 255, 255), (int(x - img.get_width() * 0.6 - S(40)), int(yy)),
                                     (int(x - img.get_width() * 0.45), int(yy)), max(1, S(3)))
        if self.post is not None and -self.S(40) < self.post < self.W + self.S(80):   # the finish post / le poteau d'arrivée
            t0, t1 = (self.S(v) for v in HORSE_TRACK)
            x = self.post
            pg.draw.rect(screen, (250, 250, 250), (int(x - S(6)), int(t0 - S(120)), S(12), int(t1 - t0 + S(120))))
            pg.draw.rect(screen, (220, 40, 40), (int(x - S(40)), int(t0 - S(140)), S(80), S(30)))
            self.text(screen, "GOAL", x, t0 - S(125), 20, WHITE, key="black", align="center", valign="middle", glow=0)

    DUST = (120, 150, 90)

    def race_clock(self, now):
        t = max(0.0, now - self.t0) if self.phase == "run" else self.RUN
        return f"{int(t) // 60}:{int(t) % 60:02d}"


def stat_pips(scene, screen, x, y, label, v, vmax, col):
    S, pg = scene.S, scene.pg
    scene.text(screen, label, x, y, 18, CREAM, key="black", valign="middle", glow=0)
    for k in range(int(vmax)):
        on = v is not None and k < v
        pg.draw.circle(screen, col if on else (60, 60, 70), (int(x + S(64) + k * S(16)), int(y)), S(6))


class StakesWinnerScene(HorseRaceScene):
    """Stakes Winner as in the game: a Japanese racecourse, the green turf and its white rails, eight horses of our own
    gallop, the player's horse wears its 1P; the race clock at the top left, the horse head and its power gauge at
    the bottom, the speed, stamina and strength of the horse read in the game. / Un hippodrome japonais, le gazon et ses
    lisses blanches, huit chevaux à nous, le chrono de la course, la jauge du cheval et ses qualités lues dans le jeu."""
    THEME = "sw_turf"
    VENUE = "SAPPORO"
    STATS = (("speed", "SPD", 8), ("stamina", "STM", 8), ("strength", "STR", 8))
    DUST = (110, 150, 80)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.stamina = 1.0

    def update(self, vals, now):
        super().update(vals, now)
        self.stamina = max(0.15, self.stamina - self.dt * 0.03) if self.phase == "run" else 1.0
        for name, label, _vmax in self.STATS:
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0]:
                self.surge(now, f"{label} UP!")
        self.power_events(vals, now)

    def power_events(self, vals, now):
        """Stakes Winner: nothing more. / Rien de plus."""

    def gauge(self, vals):
        return self.stamina

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, H = self.S, self.W, self.H
        self.draw_horses(screen, now)
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(92), now)
        self.pill(screen, S(16), S(12), S(170), S(64), 150, radius=12)                  # the race clock / le chrono
        self.hd.put_number(screen, self.race_clock(now), "black", S(44), WHITE, S(101), S(44), "center", "middle")
        self.label(screen, self.VENUE, S(100), S(108), 24, (250, 230, 120), align="center")
        x, y = S(24), H - S(52)                                          # the horse head and its gauge
        self.pill(screen, x - S(8), y - S(8), S(330), S(52), 170, radius=12)
        self.text(screen, "1P", x + S(8), y + S(18), 26, (255, 120, 60), key="black", valign="middle")
        self.bar(screen, x + S(60), y + S(8), S(250), S(20), self.gauge(vals), (240, 60, 60), back=(40, 60, 160))
        stats = [(n, lab, vm) for n, lab, vm in self.STATS if _n(vals.get(n)) is not None]
        if stats:                                                        # the horse's qualities / les qualités du cheval
            bx = W - S(250)
            self.pill(screen, bx - S(14), S(10), S(240), S(24 + 30 * len(stats)), 160, radius=12)
            for k, (n, lab, vm) in enumerate(stats):
                stat_pips(self, screen, bx, S(34) + k * S(30), lab, _n(vals.get(n)), vm, (255, 200, 60))
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, W - S(140), H - S(30), 28, colw, align="center")


class StakesWinner2Scene(StakesWinnerScene):
    """Stakes Winner 2 as in the game: Longchamp, its grandstand and its windmill, the green turf, the horses of our
    own; POWER at the bottom read in the game, power spent is a dash of the player's horse; its speed, stamina and
    burst. / Longchamp, sa tribune et son moulin, POWER lu dans le jeu, la puissance dépensée fait foncer le cheval."""
    THEME = "sw2_turf"
    VENUE = "LONGCHAMP"
    STATS = (("speed", "SPD", 7), ("stamina", "STM", 7), ("burst", "BRS", 7))

    def power_events(self, vals, now):
        ch = self.changed(vals, "power")
        if ch and ch[1] < ch[0] - 20:
            self.surge(now, "DASH!")

    def gauge(self, vals):
        p = _n(vals.get("power"))
        return self.stamina if p is None else _clamp(p / 234.0)


class JockeyGPScene(HorseRaceScene):
    """Jockey Grand Prix as in the game: the dirt track and its green rail, eight numbered horses of our own, the odds
    board at the top with the race numbers, WAGER and CREDIT; the winner's number lights up on the board. No value of
    the game is known yet: the races run by themselves. / La piste en terre, huit chevaux numérotés à nous, le tableau
    des cotes, WAGER et CREDIT ; le numéro du vainqueur s'allume, comme dans le jeu."""
    THEME = "jgp_dirt"
    NUMBERS = True
    MARK = False
    DUST = (200, 170, 120)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.odds = [round(self.rng.uniform(1.5, 40.0), 1) for _ in range(self.N)]

    def new_race(self, now):
        super().new_race(now)
        self.odds = [round(self.rng.uniform(1.5, 40.0), 1) for _ in range(self.N)]

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, H, pg = self.S, self.W, self.H, self.pg
        self.draw_horses(screen, now)
        self.hd.draw_logo(screen, logo, S(260), S(8), S(440), S(84), now)
        bx, by, bw, bh = W - S(760), S(8), S(740), S(110)               # the odds board / le tableau des cotes
        pg.draw.rect(screen, (10, 20, 90), (bx, by, bw, bh), border_radius=S(8))
        pg.draw.rect(screen, (120, 160, 255), (bx, by, bw, bh), max(1, S(3)), border_radius=S(8))
        cw = bw / self.N
        for i in range(self.N):
            x = bx + cw * (i + 0.5)
            lit = self.winner == i + 1 and int(now * 4) % 2 == 0
            self.text(screen, str(i + 1), x, by + S(30), 30, (255, 230, 60) if lit else WHITE, key="black", align="center", valign="middle", glow=0)
            self.text(screen, f"{self.odds[i]:.1f}", x, by + S(76), 24, (120, 230, 255), key="black", align="center", valign="middle", glow=0)
        cr = _n(vals.get("credits"))
        for k, (lab, v) in enumerate((("WAGER", 0), ("CREDIT", cr))):
            x = S(30) + k * S(270)
            self.pill(screen, x - S(10), H - S(52), S(250), S(44), 170, radius=10)
            self.text(screen, lab, x, H - S(30), 22, (250, 220, 80), key="black", valign="middle", glow=0)
            self.text(screen, f"{int(v or 0):06d}", x + S(226), H - S(30), 24, WHITE, key="black", align="right", valign="middle", glow=0)


# ============================================================================ Gururin
GR_COLORS = ((250, 150, 190), (250, 220, 60), (170, 100, 230), (240, 70, 60), (170, 170, 180), (80, 200, 90), (70, 130, 240))


def gururin_draw(k):
    """A little round fellow of our own in his colour: a round face, a cap of his colour, two eyes, a smile.
    / Un petit bonhomme rond à nous, de sa couleur : un visage rond, un bonnet, deux yeux, un sourire."""
    def fn(d, W, H):
        col = GR_COLORS[k % len(GR_COLORS)]
        ow = max(1, int(W * 0.05))
        d.ellipse([W * 0.12, H * 0.5, W * 0.88, H * 0.98], fill=col + (255,), outline=DARKLINE, width=ow)   # le corps
        d.ellipse([W * 0.14, H * 0.12, W * 0.86, H * 0.8], fill=(252, 224, 196, 255), outline=DARKLINE, width=ow)   # le visage
        d.chord([W * 0.1, H * 0.02, W * 0.9, H * 0.66], 180, 360, fill=col + (255,), outline=DARKLINE, width=ow)   # le bonnet
        d.ellipse([W * 0.42, H * 0.0, W * 0.58, H * 0.14], fill=_mixc(col, (255, 255, 255), 0.5), outline=DARKLINE)
        for ex in (0.36, 0.64):
            d.ellipse([W * (ex - 0.06), H * 0.42, W * (ex + 0.06), H * 0.56], fill=DARKLINE)
        d.arc([W * 0.38, H * 0.48, W * 0.62, H * 0.7], 20, 160, fill=DARKLINE, width=ow)
    return fn


class GururinBoard:
    """A square board of 8 by 8; the trios fall, the fellows settle, four of a colour that touch leave; now and then
    the board turns a quarter and everything falls the other way. / Un plateau carré de 8 sur 8 ; les trios tombent,
    quatre de la même couleur qui se touchent s'en vont ; de temps en temps le plateau tourne d'un quart."""
    N = 8

    def __init__(self, scene, cx, cy):
        self.sc, self.rng = scene, scene.rng
        self.C = scene.S(38)
        self.cx, self.cy = cx, cy
        self.grid = [[None] * self.N for _ in range(self.N)]               # [row][col], row 0 at the top
        self.drop = {}
        self.piece = None
        self.next = [self.rng.randrange(7) for _ in range(3)]
        self.turn = None                                                   # (start, direction) / (début, sens)
        self.next_turn = 9.0
        for c in range(self.N):
            for r in range(self.rng.randint(0, 2)):
                self.grid[self.N - 1 - r][c] = self.rng.randrange(7)

    def xy(self, r, c):
        n = self.N
        return self.cx + (c - n / 2 + 0.5) * self.C, self.cy + (r - n / 2 + 0.5) * self.C

    def spawn(self, colors=None):
        cols = colors or self.next
        self.next = [self.rng.randrange(7) for _ in range(3)]
        self.piece = {"c": self.rng.randint(0, self.N - 3), "y": -1.0, "cells": list(cols)}

    def settle(self):
        """Everything falls down its column. / Tout tombe dans sa colonne."""
        for c in range(self.N):
            col = [self.grid[r][c] for r in range(self.N) if self.grid[r][c] is not None]
            new = [None] * (self.N - len(col)) + col
            for r in range(self.N):
                self.grid[r][c] = new[r]

    def resolve(self, now):
        seen, gone = set(), []
        for r in range(self.N):
            for c in range(self.N):
                k = self.grid[r][c]
                if k is None or (r, c) in seen:
                    continue
                grp, todo = {(r, c)}, [(r, c)]
                while todo:
                    rr, cc = todo.pop()
                    for nr, nc in ((rr + 1, cc), (rr - 1, cc), (rr, cc + 1), (rr, cc - 1)):
                        if 0 <= nr < self.N and 0 <= nc < self.N and (nr, nc) not in grp and self.grid[nr][nc] == k:
                            grp.add((nr, nc))
                            todo.append((nr, nc))
                seen |= grp
                if len(grp) >= 4:
                    gone += list(grp)
        for r, c in gone:
            x, y = self.xy(r, c)
            self.sc.burst(x, y, self.grid[r][c])
            self.grid[r][c] = None
        if gone:
            self.sc.popped += len(gone)
            self.settle()
        return len(gone)

    def rotate(self, now, cw=True):
        """The board turns a quarter: the grid turns with it, then all falls. / Le plateau tourne d'un quart."""
        n = self.N
        g = self.grid
        self.grid = [[g[n - 1 - c][r] if cw else g[c][n - 1 - r] for c in range(n)] for r in range(n)]
        self.piece = None
        self.turn = (now, 1 if cw else -1)
        self.sc.turns += 1

    def step(self, dt, now):
        if self.turn is not None:
            if now - self.turn[0] > 0.6:
                self.turn = None
                self.settle()
                self.resolve(now)
            return
        if now >= self.next_turn:
            self.next_turn = now + self.rng.uniform(8, 12)
            self.rotate(now, self.rng.random() < 0.5)
            return
        if self.piece is None:
            self.spawn()
        p = self.piece
        p["y"] += dt * 5.0
        c0 = p["c"]
        r = math.floor(p["y"])
        row = r + 1
        blocked = row >= self.N or (row >= 0 and any(self.grid[row][c0 + i] is not None for i in range(3)))
        if blocked:
            if r < 0:                                                        # full: the board empties / plein : il se vide
                self.clear()
                return
            for i, k in enumerate(p["cells"]):
                self.grid[r][c0 + i] = k
            self.piece = None
            self.settle()
            self.resolve(now)

    def clear(self):
        for r in range(self.N):
            for c in range(self.N):
                if self.grid[r][c] is not None:
                    x, y = self.xy(r, c)
                    self.sc.fx.later(0.01 * (r * self.N + c), self.sc.burst, x, y, self.grid[r][c])
        self.grid = [[None] * self.N for _ in range(self.N)]
        self.piece = None


def gr_frame_draw(d, W, H):
    """The golden frame of the board and its corner jewels. / Le cadre doré du plateau et ses joyaux."""
    gold, dark = (232, 186, 80, 255), (120, 80, 24, 255)
    t = W * 0.05
    d.rectangle([0, 0, W - 1, H - 1], outline=dark, width=int(t + 4))
    d.rectangle([2, 2, W - 3, H - 3], outline=gold, width=int(t))
    for x, y in ((0, 0), (W, 0), (0, H), (W, H)):
        d.ellipse([x - t * 1.4, y - t * 1.4, x + t * 1.4, y + t * 1.4], fill=(220, 60, 80, 255), outline=dark, width=2)


class GururinScene(GameScene):
    """Gururin as in the game: the blue and purple checkerboard, the golden pillars, the boards in their golden frames;
    the little round fellows of our own fall three by three, four of a colour that touch leave, and the board turns
    a quarter now and then, everything falling the other way. The pieces and the next ones come from the game when
    it shows them, LEVEL at the top. / Le damier, les piliers dorés, les plateaux dans leurs cadres dorés ; les petits
    bonshommes ronds à nous tombent par trois, et le plateau tourne d'un quart, comme dans le jeu."""
    THEME = "gr_hall"
    STATIC = True
    SHADE = (60, 0)
    PILLS = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S, W = self.S, self.W
        self.boards = {"p1": GururinBoard(self, W / 2 - S(430), S(282)), "p2": GururinBoard(self, W / 2 + S(430), S(282))}
        self.boards["p2"].next_turn = 14.0
        self.popped = 0                                   # (tests)
        self.turns = 0
        self.warm += [(self.fellow, (k, 38)) for k in range(7)]

    def fellow(self, k, size):
        S = self.S
        return self.img(("gr", k, size), S(size), S(size), gururin_draw(k), ss=2)

    def burst(self, x, y, k):
        self.fx.sparks(x, y, 10, GR_COLORS[k % 7], (200, 480), (0, 360), (0.2, 0.4), 300, "front", 4, 12)

    def colors(self, vals, suf, which):
        names = [f"{which}_{p}{suf}" for p in ("l", "c", "r")]
        vs = [_n(vals.get(n)) for n in names]
        if any(v is None for v in vs):
            return None
        return [(int(v) - 1) % 7 for v in vs]

    def update(self, vals, now):
        for side, suf in (("p1", ""), ("p2", "_p2")):
            if side == "p2" and not self.p2_in(vals):
                continue
            b = self.boards[side]
            cur = self.colors(vals, suf, "cur")
            ch = any(self.changed(vals, f"cur_{p}{suf}") for p in ("l", "c", "r"))
            if cur is not None and ch and b.turn is None:                 # a new piece in the game / une nouvelle pièce
                b.spawn(cur)
            nxt = self.colors(vals, suf, "next")
            if nxt is not None:
                b.next = nxt
            b.step(self.dt, now)
        ch = self.changed(vals, "level")
        if ch and ch[1] > ch[0]:
            self.slam(f"LEVEL {int(ch[1])}", GOLD, now, 1.4)

    def draw_board(self, screen, b, now):
        S, pg = self.S, self.pg
        n, C = b.N, b.C
        size = int(n * C + S(24))
        surf = self.imgs.get(("grsurf", id(b)))
        if surf is None:
            surf = self.imgs[("grsurf", id(b))] = pg.Surface((size, size), pg.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        pg.draw.rect(surf, (40, 30, 70, 230), (S(12), S(12), n * C, n * C))
        for i in range(n + 1):                                            # the bars of the board / les barreaux
            pg.draw.line(surf, (110, 80, 50), (S(12) + i * C, S(12)), (S(12) + i * C, S(12) + n * C), max(1, S(2)))
            pg.draw.line(surf, (110, 80, 50), (S(12), S(12) + i * C), (S(12) + n * C, S(12) + i * C), max(1, S(2)))
        ox, oy = b.cx - size / 2, b.cy - size / 2
        for r in range(n):
            for c in range(n):
                k = b.grid[r][c]
                if k is not None:
                    x, y = b.xy(r, c)
                    img = self.fellow(k, 36)
                    surf.blit(img, (int(x - ox - img.get_width() / 2), int(y - oy - img.get_height() / 2)))
        if b.piece is not None:
            p = b.piece
            for i, k in enumerate(p["cells"]):
                x, _ = b.xy(0, p["c"] + i)
                y = b.cy + (p["y"] - n / 2 + 0.5) * C
                if y - oy < S(12):
                    continue
                img = self.fellow(k, 36)
                surf.blit(img, (int(x - ox - img.get_width() / 2), int(y - oy - img.get_height() / 2)))
        frame = self.img(("grframe", size), size, size, gr_frame_draw, ss=1)
        surf.blit(frame, (0, 0))
        if b.turn is not None:                                            # the board turns / le plateau tourne
            k = _clamp((now - b.turn[0]) / 0.6)
            ang = (1 - k * k * (3 - 2 * k)) * 90 * b.turn[1]
            rot = pg.transform.rotozoom(surf, ang, 1.0)
            screen.blit(rot, (int(b.cx - rot.get_width() / 2), int(b.cy - rot.get_height() / 2)))
        else:
            screen.blit(surf, (int(ox), int(oy)))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        self.top_bar(screen, eng, vals, logo, now, right=False)
        for side, b in self.boards.items():
            if side == "p2" and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, b.cx, S(280), 36, col, align="center")
                continue
            self.draw_board(screen, b, now)
            nx = b.cx + (S(250) if side == "p1" else -S(250))             # NEXT
            self.box(screen, nx - S(60), S(140), S(120), S(84), (250, 210, 90), fill=(40, 30, 80, 220), radius=10, width=3)
            self.text(screen, "NEXT", nx, S(156), 18, (250, 200, 80), key="black", align="center", valign="middle", glow=0)
            for i, k in enumerate(b.next):
                img = self.fellow(k, 30)
                screen.blit(img, (int(nx - S(48) + i * S(33)), S(176)))
        lv = _n(vals.get("level"))
        if lv is not None:
            self.label(screen, f"LEVEL {int(lv)}", W / 2, S(420), 30, WHITE, key="black", align="center")


# ============================================================================ Ghostlop
GL_COLORS = ((70, 140, 250), (250, 150, 40), (240, 60, 60), (80, 200, 90), (170, 90, 230), (250, 210, 50), (120, 120, 140), (230, 230, 240))


def ghost_draw(color):
    """A little round ghost of our own in its colour, with its wavy hem, two eyes and a grin. / Un petit fantôme rond à
    nous, de sa couleur, avec son bas ondulé, deux yeux et un sourire."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.05))
        light = _mixc(color, (255, 255, 255), 0.35)
        pts = [(W * 0.08, H * 0.5)]
        for i in range(17):
            a = math.pi + i * math.pi / 16
            pts.append((W / 2 + math.cos(a) * W * 0.42, H * 0.5 + math.sin(a) * H * 0.44))
        pts.append((W * 0.92, H * 0.88))
        for i in range(4):
            pts.append((W * (0.92 - (i + 0.5) * 0.21), H * (0.96 if i % 2 == 0 else 0.84)))
        pts.append((W * 0.08, H * 0.88))
        d.polygon(pts, fill=color + (255,), outline=DARKLINE)
        d.ellipse([W * 0.2, H * 0.14, W * 0.5, H * 0.36], fill=light)
        for ex in (0.36, 0.64):
            d.ellipse([W * (ex - 0.1), H * 0.32, W * (ex + 0.1), H * 0.56], fill=(255, 255, 255, 255), outline=DARKLINE, width=ow)
            d.ellipse([W * (ex - 0.04), H * 0.4, W * (ex + 0.04), H * 0.52], fill=DARKLINE)
        d.chord([W * 0.3, H * 0.5, W * 0.7, H * 0.8], 0, 180, fill=(60, 20, 30, 255), outline=DARKLINE)
    return fn


def hunter_draw(suit, frame):
    """A little ghost hunter of our own seen from behind, his vacuum gun up: a cap, a backpack tank.
    / Un petit chasseur de fantômes à nous, vu de dos, son aspirateur levé : une casquette, un réservoir sur le dos."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.03))
        dark = DARKLINE
        bob = H * 0.02 * frame
        d.ellipse([W * 0.2, H * 0.92, W * 0.8, H * 1.0], fill=(0, 0, 0, 90))
        for x in (0.34, 0.56):
            d.rounded_rectangle([W * x, H * 0.66, W * (x + 0.12), H * 0.95], radius=W * 0.04, fill=(50, 50, 70, 255), outline=dark, width=ow)
        d.rounded_rectangle([W * 0.26, H * 0.38 + bob, W * 0.74, H * 0.72], radius=W * 0.12, fill=suit + (255,), outline=dark, width=ow)
        d.rounded_rectangle([W * 0.32, H * 0.42 + bob, W * 0.68, H * 0.66], radius=W * 0.08, fill=(150, 160, 170, 255), outline=dark, width=ow)
        d.ellipse([W * 0.32, H * 0.14 + bob, W * 0.68, H * 0.44 + bob], fill=(90, 60, 40, 255), outline=dark, width=ow)
        d.chord([W * 0.3, H * 0.1 + bob, W * 0.7, H * 0.36 + bob], 180, 360, fill=(220, 60, 60, 255), outline=dark)
        d.line([(W * 0.62, H * 0.5), (W * 0.82, H * 0.3)], fill=(110, 110, 120, 255), width=int(W * 0.08))
        d.rounded_rectangle([W * 0.74, H * 0.1, W * 0.92, H * 0.34], radius=W * 0.04, fill=(200, 200, 210, 255), outline=dark, width=ow)
    return fn


class GhostlopScene(PuzzleBobble2Scene):
    """Ghostlop as in the game: a city street at night, the two fields full of little ghosts of our own in their
    colours, a little ghost hunter below each field shoots the ghosts up, three of a colour that touch vanish. In the
    middle, PLAYER 1 and its score, TIME in big numbers, PLAYER 2 or COMPUTER. / Une rue la nuit, les deux champs pleins
    de petits fantômes à nous, un petit chasseur sous chaque champ, TIME au milieu, comme dans le jeu."""
    THEME = "gl_street"
    FRAME = None

    def bub(self, i, r):
        S = self.S
        i = int(i) % 6
        r = int(round(r))
        return self.img(("ghost", i, r), S(2 * r), S(2 * r), ghost_draw(GL_COLORS[i]))

    def update(self, vals, now):
        PuzzleBobbleScene.update(self, vals, now)                       # the computer plays the other field / l'ordinateur joue l'autre champ
        for side, suf in (("p1", ""), ("p2", "_p2")):
            if vals.get("bubble" + suf) is not None:
                continue
            if now >= self.auto[side]:
                self.auto[side] = now + self.rng.uniform(1.2, 2.4)
                self.shoot(side, self.rng.randrange(6), now)

    def _burst(self, x, y, c, n=14):
        col = GL_COLORS[int(c) % 6]
        self.fx.sparks(x, y, n, _mixc(col, (255, 255, 255), 0.35)[:3], (200, 520), (0, 360), (0.25, 0.55), 500, "front", 4, 16)
        self.fx.glow(x, y, 12, 60, _mixc(col, (255, 255, 255), 0.4)[:3], 0.25, "front", 0.9, 0.0)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, H, dt, pg = self.S, self.W, self.H, self.dt, self.pg
        for side, board in self.boards.items():
            w = board.x1 - board.x0
            self.box(screen, board.x0 - S(10), board.top - S(10), w + S(20), H - board.top + S(4), (120, 140, 220), fill=(10, 14, 40, 170), radius=8,
                     width=3)
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
            x, y = self.launcher_xy(side)                                 # the hunter and his aim / le chasseur et sa visée
            a = math.radians(self.angle[side])
            for k in range(1, 7):
                pg.draw.circle(screen, (200, 220, 255), (int(x + math.sin(a) * S(40) * k), int(y - S(30) - math.cos(a) * S(40) * k)), max(1, S(3)))
            hunter = self.img(("hunter", side, int(now * 4) % 2), S(84), S(96), hunter_draw((60, 90, 200) if side == "p1" else (200, 70, 60),
                                                                                         int(now * 4) % 2), ss=2)
            screen.blit(hunter, (int(x - hunter.get_width() / 2), int(H - hunter.get_height())))
            nxt = _n(vals.get("bubble" + ("" if side == "p1" else "_p2")))
            if nxt is not None:
                b = self.bub(nxt, 20)
                screen.blit(b, (int(x - S(90)), int(H - S(56))))
        keep = []
        for f in self.flying:                                             # the ghosts shot up / les fantômes tirés
            board = self.boards[f["side"]]
            f["x"] += f["vx"] * dt
            f["y"] += f["vy"] * dt
            lo, hi = board.x0 + board.D / 2, board.x1 - board.D / 2
            if (f["x"] < lo and f["vx"] < 0) or (f["x"] > hi and f["vx"] > 0):
                f["vx"] = -f["vx"]
                f["x"] = _clamp(f["x"], lo, hi)
            if board.hits(f["x"], f["y"]) or now - f["t0"] > 1.6:
                for i, (x, y, c) in enumerate(board.stick(f["x"], f["y"], f["c"])):
                    self.fx.later(0.03 * i, self._burst, x, y, c)
                if board.low() >= 6:
                    self._clear(board, now)
                continue
            b = self.bub(f["c"], 22)
            screen.blit(b, (int(f["x"] - b.get_width() / 2), int(f["y"] - b.get_height() / 2)))
            keep.append(f)
        self.flying = keep
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(400), S(80), now)
        cx = W / 2                                                        # the middle column / la colonne du milieu
        for k, (lab, name, col) in enumerate((("PLAYER 1", "score", P1C), ("PLAYER 2" if self.p2_in(vals) else "COMPUTER", "score_p2", P2C))):
            y = S(100) + k * S(196)
            self.box(screen, cx - S(130), y, S(260), S(72), col, fill=(10, 14, 40, 200), radius=10, width=3)
            self.text(screen, lab, cx, y + S(18), 22, col, key="black", align="center", valign="middle", glow=0)
            v = _n(vals.get(name))
            if v is not None and (k == 0 or self.p2_in(vals) or v):
                self.hd.put_number(screen, f"{int(v)}", "black", S(34), WHITE, cx, y + S(49), "center", "middle")
        t = _n(vals.get("time"))
        if t is not None:
            t = int(t)
            self.pill(screen, cx - S(80), S(180), S(160), S(108), 170, radius=14)
            self.text(screen, "TIME", cx, S(200), 22, (250, 210, 80), key="black", align="center", valign="middle", glow=0)
            self.hd.put_number(screen, f"{t:02d}", "black", S(60), (255, 80, 60) if t <= 10 and int(now * 4) % 2 else WHITE, cx, S(246),
                               "center", "middle")
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, cx, H - S(40), 30, colw, align="center")


# ============================================================================ Pochi and Nyaa
PN_COLORS = ((90, 160, 250), (250, 210, 60), (250, 130, 170), (110, 210, 110), (250, 150, 60), (180, 120, 240))


def pet_block_draw(k):
    """A soft square block with a little cat face (even colours) or dog face (odd colours) of our own.
    / Un bloc carré tout doux avec une petite tête de chat ou de chien à nous."""
    def fn(d, W, H):
        col = PN_COLORS[k % len(PN_COLORS)]
        ow = max(1, int(W * 0.05))
        d.rounded_rectangle([W * 0.03, H * 0.03, W * 0.97, H * 0.97], radius=W * 0.22, fill=col + (255,), outline=DARKLINE, width=ow)
        d.rounded_rectangle([W * 0.12, H * 0.08, W * 0.6, H * 0.3], radius=W * 0.1, fill=_mixc(col, (255, 255, 255), 0.4))
        if k % 2 == 0:                                                   # cat: pointed ears, whiskers / chat
            for x0 in (0.16, 0.6):
                d.polygon([(W * x0, H * 0.34), (W * (x0 + 0.12), H * 0.12), (W * (x0 + 0.24), H * 0.34)], fill=_mixc(col, (0, 0, 0), 0.2), outline=DARKLINE)
            for sgn in (-1, 1):
                for dy in (0.62, 0.7):
                    d.line([(W * (0.5 + sgn * 0.14), H * dy), (W * (0.5 + sgn * 0.36), H * (dy - 0.04))], fill=DARKLINE, width=ow)
        else:                                                            # dog: floppy ears / chien
            for x0 in (0.06, 0.74):
                d.ellipse([W * x0, H * 0.26, W * (x0 + 0.2), H * 0.62], fill=_mixc(col, (0, 0, 0), 0.25), outline=DARKLINE)
        for ex in (0.36, 0.64):
            d.ellipse([W * (ex - 0.06), H * 0.42, W * (ex + 0.06), H * 0.56], fill=DARKLINE)
        d.ellipse([W * 0.45, H * 0.56, W * 0.55, H * 0.64], fill=(80, 40, 40, 255))
    return fn


class PetField:
    """A field of six columns where pairs of pet blocks fall; four of a colour that touch leave, the ones above fall,
    a chain counts. / Un champ de six colonnes où tombent des paires de blocs ; quatre de la même couleur partent."""
    COLS, ROWS = 6, 11

    def __init__(self, scene, x0):
        self.sc, self.rng = scene, scene.rng
        self.C = scene.S(32)
        self.x0, self.y0 = x0, scene.S(92)
        self.grid = [[None] * self.ROWS for _ in range(self.COLS)]           # [col][row from the bottom]
        self.piece = None
        self.next = self.new_pair()
        self.chain = 0
        self.best = 0
        for c in range(self.COLS):
            for r in range(self.rng.randint(1, 4)):
                self.grid[c][r] = self.rng.randrange(6)

    def new_pair(self):
        return [self.rng.randrange(6), self.rng.randrange(6)]

    def xy(self, c, r):
        return self.x0 + (c + 0.5) * self.C, self.y0 + (self.ROWS - r - 0.5) * self.C

    def height(self, c):
        col = self.grid[c]
        return max([r + 1 for r in range(self.ROWS) if col[r] is not None] or [0])

    def step(self, dt, now):
        if self.piece is None:
            c = min(range(self.COLS), key=lambda i: (self.height(i) + self.rng.random() * 3))
            self.piece = {"c": c, "y": self.y0 - 2 * self.C, "cells": self.next}
            self.next = self.new_pair()
        p = self.piece
        p["y"] += self.sc.S(240) * dt
        h = self.height(p["c"])
        land = self.y0 + (self.ROWS - h) * self.C - 2 * self.C
        if p["y"] >= land:
            for i, k in enumerate(reversed(p["cells"])):
                if h + i < self.ROWS:
                    self.grid[p["c"]][h + i] = k
            self.piece = None
            self.chain = 0
            self.sc.fx.later(0.15, self.resolve, now)
            if max(self.height(c) for c in range(self.COLS)) >= self.ROWS - 1:
                self.clear()

    def resolve(self, now=None):
        seen, gone = set(), []
        for c in range(self.COLS):
            for r in range(self.ROWS):
                k = self.grid[c][r]
                if k is None or (c, r) in seen:
                    continue
                grp, todo = {(c, r)}, [(c, r)]
                while todo:
                    cc, rr = todo.pop()
                    for nc, nr in ((cc + 1, rr), (cc - 1, rr), (cc, rr + 1), (cc, rr - 1)):
                        if 0 <= nc < self.COLS and 0 <= nr < self.ROWS and (nc, nr) not in grp and self.grid[nc][nr] == k:
                            grp.add((nc, nr))
                            todo.append((nc, nr))
                seen |= grp
                if len(grp) >= 4:
                    gone += list(grp)
        if not gone:
            return
        for c, r in gone:
            x, y = self.xy(c, r)
            self.sc.burst(x, y, self.grid[c][r])
            self.grid[c][r] = None
        self.sc.popped += len(gone)
        self.chain += 1
        self.best = max(self.best, self.chain)
        if self.chain >= 2:
            x, y = self.xy(2.5, 6)
            self.sc.popup(f"{self.chain} CHAIN!", x, y, GOLD, 34)
        for c in range(self.COLS):
            col = [k for k in self.grid[c] if k is not None]
            self.grid[c] = col + [None] * (self.ROWS - len(col))
        self.sc.fx.later(0.3, self.resolve)

    def clear(self):
        for c in range(self.COLS):
            for r in range(self.ROWS):
                if self.grid[c][r] is not None:
                    x, y = self.xy(c, r)
                    self.sc.fx.later(0.01 * (c + r * self.COLS), self.sc.burst, x, y, self.grid[c][r])
        self.grid = [[None] * self.ROWS for _ in range(self.COLS)]


class PochiNyaaScene(GameScene):
    """Pochi and Nyaa as in the game: the green forest and its soft lights, the fields of soft blocks with the little
    faces of cats and dogs of our own, the pairs fall, four of a colour that touch leave and the chains count; NEXT at
    the top, the score and the best chain in the middle, a big plush bear of our own beside. / La forêt verte, les
    champs de blocs tout doux aux petites têtes de chats et de chiens à nous, quatre de la même couleur partent, les
    chaînes comptent, NEXT en haut, comme dans le jeu."""
    THEME = "pn_forest"
    STATIC = True
    SHADE = (60, 0)
    PILLS = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S, W = self.S, self.W
        fw = PetField.COLS * S(32)
        self.fields = {"p1": PetField(self, W / 2 - S(250) - fw / 2), "p2": PetField(self, W / 2 + S(250) - fw / 2)}
        self.popped = 0                                   # (tests)
        self.warm += [(self.block, (k, 32)) for k in range(6)]

    def block(self, k, size):
        S = self.S
        return self.img(("pn", k, size), S(size), S(size), pet_block_draw(k), ss=2)

    def burst(self, x, y, k):
        self.fx.sparks(x, y, 10, PN_COLORS[k % 6], (200, 480), (0, 360), (0.2, 0.4), 300, "front", 4, 12)

    def update(self, vals, now):
        for side in ("p1", "p2"):
            if side == "p2" and not self.p2_in(vals):
                continue
            self.fields[side].step(self.dt, now)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(400), S(80), now)
        for side, f in self.fields.items():
            if side == "p2" and not self.p2_in(vals):
                x, _ = f.xy(2.5, 5)
                word, col = self.invite(vals, now)
                self.label(screen, word, x, S(280), 34, col, align="center")
                continue
            w, h = f.C * f.COLS, f.C * f.ROWS
            self.box(screen, f.x0 - S(8), f.y0 - S(8), w + S(16), h + S(14), (250, 250, 250), fill=(20, 40, 30, 200), radius=10, width=3)
            for c in range(f.COLS):
                for r in range(f.ROWS):
                    k = f.grid[c][r]
                    if k is not None:
                        img = self.block(k, 32)
                        x, y = f.xy(c, r)
                        screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
            if f.piece is not None:
                p = f.piece
                for i, k in enumerate(p["cells"]):
                    y = p["y"] + (i + 0.5) * f.C
                    if y < f.y0:
                        continue
                    img = self.block(k, 32)
                    x, _ = f.xy(p["c"], 0)
                    screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
            nx = f.x0 + (w + S(20) if side == "p1" else -S(70))           # NEXT
            self.box(screen, nx, f.y0 - S(8), S(52), S(96), (250, 250, 250), fill=(20, 40, 30, 200), radius=8, width=2)
            for i, k in enumerate(f.next):
                img = self.block(k, 30)
                screen.blit(img, (int(nx + S(11)), int(f.y0 + S(4) + i * S(40))))
            sc = _n(vals.get("score" if side == "p1" else "score_p2"))
            cx = f.x0 + w / 2
            self.label(screen, f"{int(sc)}" if sc is not None else ("1P" if side == "p1" else "2P"), cx, S(64), 28, P1C if side == "p1" else P2C,
                       key="black", align="center")
            lx = f.x0 + w + S(46) if side == "p1" else f.x0 - S(44)
            self.text(screen, tr("CHAÎNE", "CHAIN"), lx, S(214), 18, CREAM, key="black", align="center", valign="middle", glow=0)
            self.text(screen, f"{f.best}", lx, S(244), 30, GOLD, key="black", align="center", valign="middle", glow=0)


# ============================================================================ Puzzled
TETRO = {0: ((0, 0), (1, 0), (1, 1), (2, 1)),            # red Z / rouge
         1: ((0, 0), (1, 0), (2, 0), (1, 1)),            # purple T / violet
         2: ((0, 0), (1, 0), (2, 0), (2, -1)),           # orange L
         3: ((0, -1), (0, 0), (1, 0), (2, 0)),           # blue J / bleu
         4: ((0, 0), (1, 0), (0, 1), (1, 1)),            # yellow O / jaune
         5: ((1, 0), (2, 0), (0, 1), (1, 1)),            # green S / vert
         6: ((0, 0), (1, 0), (2, 0), (3, 0))}            # cyan I
TETRO_RGB = ((230, 50, 50), (170, 70, 210), (250, 150, 40), (50, 90, 230), (250, 220, 40), (60, 200, 80), (60, 210, 230))
PZ_LAYOUT = ("....##....", "...####...", "..######..", ".########.")


def _turn(cells, n):
    out = cells
    for _ in range(n % 4):
        out = tuple((-y, x) for x, y in out)
    mx, my = min(x for x, _ in out), min(y for _, y in out)
    return tuple((x - mx, y - my) for x, y in out)


def balloon_draw(d, W, H):
    """A little kid of our own hanging from his balloon. / Un petit enfant à nous accroché à son ballon."""
    d.ellipse([W * 0.2, 0, W * 0.8, H * 0.5], fill=(240, 70, 120, 255), outline=DARKLINE, width=max(1, int(W * 0.04)))
    d.ellipse([W * 0.3, H * 0.06, W * 0.44, H * 0.18], fill=(255, 220, 230, 255))
    d.line([(W * 0.5, H * 0.5), (W * 0.5, H * 0.66)], fill=DARKLINE, width=max(1, int(W * 0.03)))
    d.ellipse([W * 0.36, H * 0.6, W * 0.64, H * 0.8], fill=(250, 220, 190, 255), outline=DARKLINE)
    d.rounded_rectangle([W * 0.36, H * 0.78, W * 0.64, H * 0.98], radius=W * 0.06, fill=(60, 120, 230, 255), outline=DARKLINE)


class PuzzleWell:
    """The well of a tower: the pieces fall where a little helper of ours puts them best, the full lines leave; when the
    blocks of the stage are gone, the kid's balloon floats up and a new stage comes. / Le puits d'une tour : les pièces
    tombent, les lignes pleines partent ; quand les blocs de l'étape sont partis, le ballon s'envole."""

    def __init__(self, scene, cx):
        self.sc, self.rng = scene, scene.rng
        S = scene.S
        self.C = S(PZ_CELL)
        self.x0 = cx - PZ_COLS * self.C / 2
        self.y0 = S(PZ_TOP)
        self.piece = None
        self.next = self.rng.randrange(7)
        self.float = None
        self.flash = None
        self.new_stage()

    def new_stage(self):
        self.grid = [[None] * PZ_COLS for _ in range(PZ_ROWS)]             # [row][col], row 0 at the top
        for i, line in enumerate(PZ_LAYOUT):
            r = PZ_ROWS - len(PZ_LAYOUT) + i
            for c, ch in enumerate(line):
                if ch == "#":
                    self.grid[r][c] = 7                                      # the bricks of the stage / les briques de l'étape
        self.float = None

    def fits(self, cells, c, r):
        for x, y in cells:
            cc, rr = c + x, r + y
            if cc < 0 or cc >= PZ_COLS or rr >= PZ_ROWS or (rr >= 0 and self.grid[rr][cc] is not None):
                return False
        return True

    def best(self, kind):
        """Where the piece fits best: low, no holes, full lines. / Où la pièce va le mieux : bas, sans trous, lignes pleines."""
        best, score = None, None
        for rot in range(4):
            cells = _turn(TETRO[kind], rot)
            for c in range(PZ_COLS):
                if not self.fits(cells, c, 0):
                    continue
                r = 0
                while self.fits(cells, c, r + 1):
                    r += 1
                g = [row[:] for row in self.grid]
                for x, y in cells:
                    if 0 <= r + y < PZ_ROWS:
                        g[r + y][c + x] = kind
                lines = sum(1 for row in g if all(v is not None for v in row))
                holes = 0
                for cc in range(PZ_COLS):
                    seen = False
                    for rr in range(PZ_ROWS):
                        if g[rr][cc] is not None:
                            seen = True
                        elif seen:
                            holes += 1
                top = min([rr for rr in range(PZ_ROWS) for cc in range(PZ_COLS) if g[rr][cc] is not None] or [PZ_ROWS])
                sc = lines * 8 - holes * 3 + r * 0.6 + top * 0.3 + self.rng.random() * 0.5
                if score is None or sc > score:
                    best, score = (cells, c, r), sc
        return best

    def step(self, dt, now):
        if self.float is not None:
            if now - self.float > 2.2:
                self.new_stage()
            return
        if self.flash is not None:
            rows, t0 = self.flash
            if now - t0 > 0.3:
                for r in sorted(rows):
                    del self.grid[r]
                    self.grid.insert(0, [None] * PZ_COLS)
                self.flash = None
                self.sc.lines += len(rows)
                if not any(v == 7 for row in self.grid for v in row):          # the stage is clear / l'étape est finie
                    self.float = now
                    self.sc.stages += 1
                    x = self.x0 + PZ_COLS * self.C / 2
                    self.sc.popup(tr("ÉTAPE FINIE !", "STAGE CLEAR!"), x, self.sc.S(240), GOLD, 36)
            return
        if self.piece is None:
            kind = self.next
            self.next = self.rng.randrange(7)
            spot = self.best(kind)
            if spot is None:                                                 # full / plein
                self.new_stage()
                return
            cells, c, r = spot
            self.piece = {"kind": kind, "cells": cells, "c": c, "y": -2.0, "r": r}
        p = self.piece
        p["y"] += dt * 7.0
        if p["y"] >= p["r"]:
            for x, y in p["cells"]:
                if 0 <= p["r"] + y < PZ_ROWS:
                    self.grid[p["r"] + y][p["c"] + x] = p["kind"]
            self.piece = None
            full = [r for r in range(PZ_ROWS) if all(v is not None for v in self.grid[r])]
            if full:
                self.flash = (full, now)


class PuzzledScene(GameScene):
    """Puzzled as in the game: the green hills and the white clouds, the brick towers and their wells; the pieces fall
    and fill the lines, the full lines leave, and when the bricks of the stage are gone the kid's balloon floats away.
    NEXT in its colour read in the game, the score, STAGE and the balloons left in the middle.
    / Les collines vertes, les tours de briques et leurs puits, les lignes pleines partent, le ballon s'envole quand
    l'étape est finie ; NEXT dans sa couleur lue dans le jeu, le score, STAGE et les ballons qui restent, comme dans le jeu."""
    THEME = "pz_tower"
    STATIC = True
    SHADE = (40, 0)
    PILLS = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.wells = {"p1": PuzzleWell(self, S(PZ_WELLS[0])), "p2": PuzzleWell(self, S(PZ_WELLS[1]))}
        self.lines = 0                                    # (tests)
        self.stages = 0

    def update(self, vals, now):
        for side, suf in (("p1", ""), ("p2", "_p2")):
            if side == "p2" and not self.p2_in(vals):
                continue
            wl = self.wells[side]
            nx = _n(vals.get("next" + suf))
            if nx is not None:
                wl.next = int(nx) % 7
            wl.step(self.dt, now)

    def cell(self, screen, x, y, kind, C):
        pg = self.pg
        col = TETRO_RGB[kind] if kind < 7 else (200, 60, 50)
        pg.draw.rect(screen, col, (int(x), int(y), int(C) - 1, int(C) - 1))
        pg.draw.rect(screen, _mixc(col, (255, 255, 255), 0.45)[:3], (int(x), int(y), int(C) - 1, max(1, int(C * 0.18))))
        pg.draw.rect(screen, _mixc(col, (0, 0, 0), 0.4)[:3], (int(x), int(y), int(C) - 1, int(C) - 1), max(1, int(C * 0.08)))
        if kind == 7:
            pg.draw.line(screen, (120, 30, 30), (int(x), int(y + C / 2)), (int(x + C), int(y + C / 2)), max(1, int(C * 0.08)))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        for side, wl in self.wells.items():
            if side == "p2" and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, S(PZ_WELLS[1]), S(270), 30, col, align="center")
                continue
            C = wl.C
            for r in range(PZ_ROWS):
                if wl.flash is not None and r in wl.flash[0] and int(now * 20) % 2:
                    self.pg.draw.rect(screen, (255, 255, 255), (int(wl.x0), int(wl.y0 + r * C), int(PZ_COLS * C), int(C)))
                    continue
                for c in range(PZ_COLS):
                    k = wl.grid[r][c]
                    if k is not None:
                        self.cell(screen, wl.x0 + c * C, wl.y0 + r * C, k, C)
            p = wl.piece
            if p is not None:
                for x, y in p["cells"]:
                    yy = p["y"] + y
                    if yy >= 0:
                        self.cell(screen, wl.x0 + (p["c"] + x) * C, wl.y0 + yy * C, p["kind"], C)
            bx = wl.x0 + PZ_COLS * C / 2                                  # the kid and his balloon / l'enfant et son ballon
            by = wl.y0 + PZ_ROWS * C - S(60)
            if wl.float is not None:
                by -= (now - wl.float) * S(260)
            img = self.img("pzballoon", S(40), S(60), balloon_draw, ss=2)
            if by > -S(60):
                screen.blit(img, (int(bx - img.get_width() / 2), int(by)))
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(320), S(70), now)
        cx = W / 2                                                         # the middle column / la colonne du milieu
        self.box(screen, cx - S(120), S(86), S(240), S(110), (240, 220, 160), fill=(30, 26, 40, 220), radius=8, width=3)
        self.text(screen, "NEXT", cx, S(104), 20, (250, 220, 120), key="black", align="center", valign="middle", glow=0)
        kind = self.wells["p1"].next
        cells = TETRO[kind]
        C = S(20)
        mw = (max(x for x, _ in cells) + 1) * C
        miny = min(y for _, y in cells)
        for x, y in cells:
            self.cell(screen, cx - mw / 2 + x * C, S(132) + (y - miny) * C, kind, C)
        sc = _n(vals.get("score"))
        self.box(screen, cx - S(120), S(206), S(240), S(150), (240, 220, 160), fill=(30, 26, 40, 220), radius=8, width=3)
        self.text(screen, "1P SCORE", cx, S(226), 20, P1C, key="black", align="center", valign="middle", glow=0)
        if sc is not None:
            self.hd.put_number(screen, f"{int(sc)}", "black", S(30), WHITE, cx, S(258), "center", "middle")
        self.text(screen, f"STAGE {self.stages + 1}", cx, S(296), 22, (250, 220, 120), key="black", align="center", valign="middle", glow=0)
        bl = _n(vals.get("balloons"))
        if bl is not None:
            img = self.img("pzballoon_s", S(20), S(30), balloon_draw, ss=2)
            n = int(min(bl, 9))
            for k in range(n):
                screen.blit(img, (int(cx - n * S(11) + k * S(22)), S(316)))


SCENES = {"bangbead": BangBeadScene, "flipshot": FlipShotScene, "overtop": OverTopScene, "stakwin": StakesWinnerScene,
          "stakwin2": StakesWinner2Scene, "jockeygp": JockeyGPScene, "gururin": GururinScene, "ghostlop": GhostlopScene,
          "pnyaa": PochiNyaaScene, "joyjoy": PuzzledScene}
