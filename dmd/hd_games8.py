"""HD scenes of the eighth batch of Neo Geo games done one by one (1.24), each drawn after screenshots of its game.
Each game has its own animated backdrop and reacts to the values read in its memory. The players are creations of the
program in the spirit of the games.

Scènes HD du huitième lot de jeux Neo Geo faits un par un (1.24), chacune dessinée d'après des captures de son jeu.
Les joueurs sont des créations du programme dans l'esprit des jeux.
"""

import math

from .hd_games import CREAM, GOLD, WHITE, GameScene, TurfMastersScene, _clamp, _n
from .hd_games2 import SoccerScene
from .hd_games3 import BaseballScene, _capsule
from .hd_games5 import _mixc
from .hd_games6 import portrait_draw
from .hd_games7 import flag_draw
from .hd_themes8 import FF_FIELD, PS_FLOOR                         # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr

DARKLINE = (24, 20, 26, 255)


def kits(a, b, ga=(250, 210, 60), gb=(70, 200, 120)):
    """Two teams and their keepers. / Deux équipes et leurs gardiens."""
    def k(shirt, shorts, socks=None):
        return {"shirt": shirt, "shorts": shorts, "socks": socks or shirt}
    return (k(*a), k(*b), k(ga, (30, 30, 30)), k(gb, (30, 30, 30)))


# ============================================================================ the football games / le football
class TecmoSoccerScene(SoccerScene):
    """Tecmo World Soccer '96 as in the game: the match in the stadium, the two flags at the top and the round clock
    between them. No value of the game is known yet: the match plays by itself.
    / Le match dans le stade, les deux drapeaux en haut et l'horloge ronde entre eux, comme dans le jeu."""
    THEME = "stadium_day"
    KITS = kits(((40, 90, 220), (250, 250, 250)), ((250, 250, 250), (40, 60, 160)))

    def scoreboard(self, screen, vals, now):
        S, W, pg = self.S, self.W, self.pg
        for side, x, kit in (("p1", S(30), self.KITS[0]), ("p2", W / 2 + S(330), self.KITS[1])):
            self.pill(screen, x - S(10), S(10), S(130), S(70), 160, radius=12)
            screen.blit(self.img(("twflag", side), S(90), S(52), flag_draw(kit), ss=1), (x + S(10), S(19)))
        cx, cy, r = W / 2 - S(330), S(46), S(28)                        # the round clock, its yellow part turns
        a = (now * 6) % 360
        pg.draw.circle(screen, (30, 40, 140), (int(cx), int(cy)), r)
        pts = [(cx, cy)] + [(cx + math.cos(math.radians(-90 + i)) * r, cy + math.sin(math.radians(-90 + i)) * r) for i in range(0, int(a) + 1, 6)]
        if len(pts) > 2:
            pg.draw.polygon(screen, (250, 220, 40), [(int(x), int(y)) for x, y in pts])
        pg.draw.circle(screen, WHITE, (int(cx), int(cy)), r, max(1, S(3)))


class Goal3Scene(SoccerScene):
    """Goal! Goal! Goal! as in the game: the match in the stadium, the flags and the goals in big yellow numbers at the
    top, the time with its moon. / Le match, les drapeaux et les buts en gros chiffres jaunes, le temps et sa lune."""
    THEME = "stadium_day"
    KITS = kits(((250, 220, 40), (40, 120, 60)), ((220, 40, 40), (250, 250, 250)))

    def scoreboard(self, screen, vals, now):
        S, hd = self.S, self.hd
        self.pill(screen, S(12), S(8), S(620), S(70), 160, radius=12)
        for side, name, x, kit in (("p1", "goals", S(24), self.KITS[0]), ("p2", "goals_p2", S(480), self.KITS[1])):
            screen.blit(self.img(("g3flag", side), S(70), S(46), flag_draw(kit), ss=1), (x, S(20)))
            v = _n(vals.get(name))
            if v is not None:
                k = now - self.gpop[name]
                hd.put_number(screen, f"{int(v):02d}", "stencil", S(46), WHITE if k < 1.0 and int(k * 8) % 2 == 0 else (250, 220, 40),
                              x + S(110), S(44), "center", "middle")
        t = _n(vals.get("time"))
        if t is not None:
            pg = self.pg                                               # the moon of the clock / la lune de l'horloge
            pg.draw.circle(screen, (250, 220, 40), (S(270), S(44)), S(16))
            pg.draw.circle(screen, (40, 40, 50), (S(278), S(38)), S(14))
            hd.put_number(screen, f"{int(t) // 60}:{int(t) % 60:02d}", "stencil", S(44), WHITE, S(360), S(44), "center", "middle")


class NeoCup98Scene(SoccerScene):
    """Neo-Geo Cup '98 as in the game: the match in the stadium, the blue band at the top with the flags and the goals.
    / Le match dans le stade, le bandeau bleu en haut avec les drapeaux et les buts, comme dans le jeu."""
    THEME = "stadium_day"
    KITS = kits(((40, 80, 220), (250, 250, 250)), ((250, 250, 250), (30, 30, 40)))

    def scoreboard(self, screen, vals, now):
        S, pg, hd = self.S, self.pg, self.hd
        band = self.imgs.get("nc98band")
        if band is None:
            band = self.imgs["nc98band"] = pg.Surface((S(700), S(70)), pg.SRCALPHA)
            band.fill((20, 60, 200, 220))
        screen.blit(band, (S(10), S(10)))
        for side, name, x, kit in (("p1", "goals", S(24), self.KITS[0]), ("p2", "goals_p2", S(560), self.KITS[1])):
            screen.blit(self.img(("nc98flag", side), S(100), S(56), flag_draw(kit), ss=1), (x, S(17)))
            v = _n(vals.get(name))
            if v is not None:
                k = now - self.gpop[name]
                hd.put_number(screen, f"{int(v)}", "black", S(60), (255, 230, 120) if k < 1.0 and int(k * 8) % 2 == 0 else WHITE,
                              x + (S(150) if side == "p1" else -S(50)), S(45), "center", "middle")
        self.text(screen, "TIME", S(360), S(45), 30, WHITE, key="black", align="center", valign="middle")


class SoccerBrawlScene(SoccerScene):
    """Soccer Brawl as in the game: football of the future at night, the armoured players in metal colours, the POWER
    METER of each team at the top, the goals and TIME. / Le football du futur la nuit, les joueurs en armure, POWER METER."""
    THEME = "stadium_night"
    POWER = False
    KITS = kits(((230, 120, 40), (90, 90, 110)), ((150, 90, 200), (200, 200, 220)), (240, 240, 250), (240, 240, 250))

    def scoreboard(self, screen, vals, now):
        S, W, hd = self.S, self.W, self.hd
        for side, name, en, x, acc in (("p1", "goals", "energy", S(20), (230, 120, 40)), ("p2", "goals_p2", "energy_p2", W / 2 + S(250), (150, 90, 200))):
            self.pill(screen, x, S(8), S(360), S(64), 170, radius=10)
            v = _n(vals.get(name))
            if v is not None:
                k = now - self.gpop[name]
                hd.put_number(screen, f"{int(v):02d}", "stencil", S(40), WHITE if k < 1.0 and int(k * 8) % 2 == 0 else (250, 230, 120), x + S(46),
                              S(40), "center", "middle")
            self.text(screen, "POWER METER", x + S(96), S(24), 18, (120, 220, 255), key="black", valign="middle", glow=0)
            e = _n(vals.get(en))
            self.bar(screen, x + S(96), S(40), S(240), S(20), (e or 0) / 96.0, acc)
        tm, ts = _n(vals.get("time_min")), _n(vals.get("time_sec"))
        if tm is not None and ts is not None:
            self.label(screen, f"TIME {int(tm):02d}:{int(ts):02d}", W / 2, S(130), 30, (120, 220, 255), key="black", align="center")


class PleasureGoalScene(SoccerScene):
    """Pleasure Goal as in the game: futsal, five against five, a face of our own for each team beside the goals, the
    clock in the middle. / Le futsal, cinq contre cinq, un visage à nous par équipe à côté des buts, l'horloge au milieu."""
    THEME = "stadium_day"
    KITS = kits(((250, 250, 250), (40, 60, 160)), ((240, 120, 30), (250, 250, 250)))

    def scoreboard(self, screen, vals, now):
        S, W, hd = self.S, self.W, self.hd
        for side, name, x, face in (("p1", "goals", S(20), ((226, 176, 136), (60, 40, 30))), ("p2", "goals_p2", W / 2 + S(330),
                                                                                                ((210, 160, 120), (200, 160, 60)))):
            self.pill(screen, x, S(8), S(200), S(76), 170, radius=10)
            screen.blit(self.img(("pgface", side), S(60), S(60), portrait_draw(face[0], face[1], bg=(70, 120, 200)), ss=2), (x + S(8), S(16)))
            v = _n(vals.get(name))
            if v is not None:
                k = now - self.gpop[name]
                hd.put_number(screen, f"{int(v)}", "stencil", S(50), WHITE if k < 1.0 and int(k * 8) % 2 == 0 else (250, 220, 60), x + S(130),
                              S(46), "center", "middle")
        t = _n(vals.get("time"))
        if t is not None:
            self.label(screen, f"{int(t)}", W / 2 - S(330), S(46), 34, (250, 220, 60), key="stencil", align="center")


# ============================================================================ Football Frenzy
def gridiron_draw(color, trim, frame):
    """A player of American football seen from above at three quarters: a round helmet, big shoulder pads, facing right.
    Frames 0 and 1 run, 2 down. / Un joueur de football américain vu de trois quarts : casque rond, grosses épaulettes."""
    def fn(d, W, H):
        dark = DARKLINE
        u = H
        if frame == 2:
            d.ellipse([W * 0.1, H * 0.6, W * 0.9, H * 0.95], fill=color + (255,), outline=dark)
            d.ellipse([W * 0.02, H * 0.56, W * 0.34, H * 0.9], fill=_mixc(color, (255, 255, 255), 0.3), outline=dark)
            return
        cx = W * 0.5
        st = (0.1, -0.1) if frame == 0 else (-0.1, 0.1)
        for i, dx in enumerate(st):
            _capsule(d, (cx, H * 0.62), (cx + dx * u, H * 0.94), 0.07 * u, 0.06 * u, trim + (255,), dark, max(1, W * 0.03))
        d.ellipse([cx - 0.24 * u, H * 0.3, cx + 0.24 * u, H * 0.66], fill=color + (255,), outline=dark, width=max(1, int(W * 0.04)))
        d.ellipse([cx - 0.15 * u, H * 0.04, cx + 0.17 * u, H * 0.36], fill=_mixc(color, (255, 255, 255), 0.25), outline=dark,
                  width=max(1, int(W * 0.04)))
        d.line([(cx + 0.06 * u, H * 0.18), (cx + 0.2 * u, H * 0.22)], fill=(200, 200, 210, 255), width=max(1, int(W * 0.05)))
    return fn


class FootballFrenzyScene(GameScene):
    """Football Frenzy as in the game: the field seen from above with its yard lines and its end zones, two teams of our
    own line up, the ball is snapped, the runner breaks through until he is tackled. The points read in the game are
    touchdowns. The quarter, the points of both teams in big yellow numbers and the clock at the top.
    / Le terrain vu de haut, deux équipes à nous, la balle est mise en jeu, le porteur file jusqu'au plaquage."""
    THEME = "ff_field"
    STATIC = True
    SHADE = (60, 0)
    TEAMS = (((220, 50, 50), (250, 250, 250)), ((250, 250, 250), (50, 80, 200)))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.line = 50.0                                   # line of scrimmage, in yards from the left goal line
        self.off = 0                                       # team with the ball, 0 runs to the right
        self.players = []
        self.phase = ("set", 0.0)
        self.carrier = None
        self.td = 0                                        # touchdowns shown (tests)
        self.tackles = 0
        self.lineup(0.0)

    def yx(self, yards, lane):
        S = self.S
        x0, y0, x1, y1 = (S(v) for v in FF_FIELD)
        ez = S(100)
        return x0 + ez + (x1 - x0 - 2 * ez) * yards / 100.0, y0 + (y1 - y0) * lane

    def lineup(self, now):
        d = 1 if self.off == 0 else -1
        self.players = []
        for team in (0, 1):
            side = -d if team == self.off else d
            for i in range(6):
                lane = 0.15 + 0.7 * i / 5
                back = 1.5 + (4 if i in (2, 3) and team == self.off else 0)
                self.players.append({"team": team, "yd": self.line + side * back, "lane": lane, "to": None, "down": None, "ph": self.rng.uniform(0, 6)})
        self.carrier = None
        self.phase = ("set", now)

    def play(self, now, td=False):
        """The snap: the runner goes, the defence chases. / La mise en jeu : le porteur part, la défense le poursuit."""
        d = 1 if self.off == 0 else -1
        runners = [p for p in self.players if p["team"] == self.off]
        self.carrier = self.rng.choice(runners)
        gain = (110 if td else self.rng.uniform(3, 22))
        self.carrier["to"] = (_clamp(self.line + d * gain, -8, 108), self.carrier["lane"] + self.rng.uniform(-0.2, 0.2))
        for p in self.players:
            if p is self.carrier:
                continue
            if p["team"] == self.off:
                p["to"] = (p["yd"] + d * self.rng.uniform(2, 6), p["lane"])
            else:
                p["to"] = (self.carrier["to"][0] + d * self.rng.uniform(0, 4), self.carrier["to"][1] + self.rng.uniform(-0.1, 0.1))
        self.phase = ("run", now, td)

    def update(self, vals, now):
        dt = self.dt
        ph = self.phase
        for name, team in (("score", 0), ("score_p2", 1)):
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0]:                                   # points: a touchdown for this team
                self.off = team
                self.line = 70.0 if team == 0 else 30.0
                self.lineup(now)
                self.play(now, td=True)
                ph = self.phase
        if ph[0] == "set" and now - ph[1] > 1.6:
            self.play(now)
        elif ph[0] == "run":
            done = True
            for p in self.players:
                if p["to"] is None or p["down"] is not None:
                    continue
                ty, tl = p["to"]
                spd = 14.0 if p is self.carrier else 12.0
                p["yd"] += _clamp(ty - p["yd"], -spd * dt, spd * dt)
                p["lane"] += _clamp(tl - p["lane"], -0.3 * dt, 0.3 * dt)
                if abs(ty - p["yd"]) > 0.3:
                    done = False
            if done or now - ph[1] > 6:
                c = self.carrier
                if ph[2] or not (0 <= c["yd"] <= 100):
                    self.td += 1
                    self.slam("TOUCHDOWN!", GOLD, now, 1.6)
                    x, y = self.yx(_clamp(c["yd"], 0, 100), c["lane"])
                    for i in range(6):
                        self.fx.later(i * 0.15, self.fx.sparks, x + self.rng.uniform(-80, 80) * self.s, y - self.S(100), 24,
                                      self.rng.choice(((255, 80, 80), (255, 230, 80), (80, 160, 255))), (200, 500), (0, 360), (0.4, 0.8), 300,
                                      "front", 4, 12)
                    self.line = 50.0
                    self.off = 1 - self.off
                    self.phase = ("wait", now)
                else:
                    self.tackles += 1
                    c["down"] = now
                    self.line = _clamp(c["yd"], 5, 95)
                    self.phase = ("wait", now)
        elif ph[0] == "wait" and now - ph[1] > 1.4:
            self.lineup(now)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        x, _ = self.yx(self.line, 0)
        _, ya = self.yx(0, 0)
        _, yb = self.yx(0, 1)
        self.pg.draw.line(screen, (80, 160, 255), (int(x), int(ya)), (int(x), int(yb)), max(2, S(3)))
        for p in sorted(self.players, key=lambda p: p["lane"]):
            col, trim = self.TEAMS[p["team"]]
            moving = self.phase[0] == "run" and p["to"] is not None
            frame = 2 if p["down"] is not None else (int(now * 8 + p["ph"]) % 2 if moving else 0)
            face = (1 if self.off == 0 else -1) * (1 if p["team"] == self.off else -1)
            img = self.img(("ffpl", p["team"], frame, face < 0), S(56), S(64), gridiron_draw(col, trim, frame), ss=2, flip=face < 0)
            px, py = self.yx(p["yd"], p["lane"])
            screen.blit(img, (int(px - img.get_width() / 2), int(py - img.get_height())))
            if p is self.carrier and self.phase[0] == "run":
                self.pg.draw.ellipse(screen, (140, 80, 30), (int(px + face * S(14) - S(8)), int(py - S(40)), S(16), S(10)))
        self.hd.draw_logo(screen, logo, W / 2, S(4), S(360), S(64), now)
        self.pill(screen, S(12), S(6), S(520), S(100), 170, radius=12)
        self.text(screen, "1P", S(30), S(26), 24, (250, 80, 70), key="black", valign="middle")
        right = "2P" if self.p2_in(vals) else "COM"
        self.text(screen, right, S(500), S(26), 24, (90, 140, 255), key="black", align="right", valign="middle")
        for name, xx in (("score", S(110)), ("score_p2", S(410))):
            v = _n(vals.get(name))
            if v is not None:
                self.hd.put_number(screen, f"{int(v):02d}", "stencil", S(54), (250, 220, 40), xx, S(62), "center", "middle")
        tm, ts = _n(vals.get("time_min")), _n(vals.get("time_sec"))
        if tm is not None and ts is not None:
            self.text(screen, f"{int(tm):02d}:{int(ts):02d}", S(260), S(76), 28, WHITE, key="black", align="center", valign="middle")
        self.text(screen, tr("QUART-TEMPS", "QUARTER"), S(260), S(30), 20, (250, 230, 120), key="black", align="center", valign="middle", glow=0)
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


# ============================================================================ Baseball Stars Professional, 2020 Super Baseball
class BaseballStarsProScene(BaseballScene):
    """Baseball Stars Professional as in the game: the field seen from behind home plate, the box with the inning, the
    count B S O in lights, the clock. The balls, strikes and outs read in the game make the pitches.
    / Le terrain vu de derrière le marbre, la manche, le compte B S O en voyants, comme dans le jeu."""

    def scoreboard(self, screen, vals, now):
        S, W, pg = self.S, self.W, self.pg
        x, y = W / 2 + S(320), S(10)
        self.box(screen, x, y, S(300), S(110), (240, 240, 240), fill=(20, 20, 30, 230), radius=8, width=3)
        inn = _n(vals.get("inning"))
        right = "2P" if self.p2_in(vals) else "CPU"
        self.text(screen, f"1P - {right}", x + S(150), y + S(30), 30, (250, 90, 90), key="black", align="center", valign="middle")
        if inn is not None:
            self.text(screen, f"{'TOP' if self.bat == 0 else 'BOT'} {int(inn)}", x + S(150), y + S(76), 32, WHITE, key="black", align="center",
                      valign="middle")
        bx, by = S(20), S(10)
        self.box(screen, bx, by, S(200), S(130), (240, 240, 240), fill=(20, 20, 30, 230), radius=8, width=3)
        for row, (lab, name, n, col) in enumerate((("B", "balls", 3, (70, 230, 90)), ("S", "strikes", 2, (255, 210, 60)), ("O", "outs", 2, (255, 80, 60)))):
            v = _n(vals.get(name))
            ry = by + S(28) + row * S(38)
            self.text(screen, lab, bx + S(24), ry, 28, CREAM, key="black", valign="middle", glow=0)
            for i in range(n):
                on = v is not None and i < int(v)
                pg.draw.circle(screen, col if on else (60, 60, 70), (int(bx + S(80) + i * S(40)), int(ry)), S(13))
        t = _n(vals.get("time"))
        if t is not None:
            self.label(screen, f"0:{int(t):02d}", S(120), S(170), 30, WHITE, key="black", align="center")


class Baseball2020Scene(BaseballScene):
    """2020 Super Baseball as in the game: baseball of the future on its bright field, the blue box with the inning,
    the score and the time. The outs counted in the game make the plays; between them the game plays by itself.
    / Le baseball du futur, la boîte bleue avec la manche, le score et le temps, comme dans le jeu."""

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.auto = 0.0

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "outs_total")
        if ch and ch[1] > ch[0]:
            self.queue.append(("out", {}))
        elif now >= self.auto and not self.queue and self.play is None:  # the game goes on by itself
            self.auto = now + self.rng.uniform(2.5, 4.5)
            self.queue.append((self.rng.choice(("ball", "strike", "strike", "hit", "out")), {}))

    def scoreboard(self, screen, vals, now):
        S = self.S
        x, y = S(20), S(10)
        self.box(screen, x, y, S(220), S(140), (250, 220, 60), fill=(20, 40, 160, 230), radius=8, width=4)
        self.text(screen, f"1 {'TOP' if self.bat == 0 else 'BOT'}", x + S(110), y + S(28), 28, (250, 230, 120), key="black", align="center", valign="middle")
        self.text(screen, "1P - CPU", x + S(110), y + S(66), 26, WHITE, key="black", align="center", valign="middle")
        t = _n(vals.get("time"))
        if t is not None:
            self.text(screen, f"01:{int(t):02d}", x + S(110), y + S(108), 28, (250, 230, 120), key="stencil", align="center", valign="middle")


# ============================================================================ Top Player's Golf
class TopPlayersGolfScene(TurfMastersScene):
    """Top Player's Golf as in the game: the course, the ball flies to the flag at each stroke read in the game, the blue
    framed boxes with HOLE, STROKE and the time. / Le parcours, la balle vole vers le drapeau à chaque coup, comme dans le jeu."""

    def draw_hud(self, screen, eng, vals, logo, now):
        super().draw_hud(screen, eng, vals, logo, now)
        S, H = self.S, self.H
        holes = _n(vals.get("holes"))
        self.box(screen, S(20), S(110), S(330), S(56), (120, 160, 255), fill=(20, 40, 140, 230), radius=6, width=4)
        self.text(screen, f"HOLE {int(holes) if holes is not None else 1}", S(40), S(138), 30, WHITE, key="black", valign="middle")
        self.text(screen, "PAR 4", S(330), S(138), 30, WHITE, key="black", align="right", valign="middle")
        t = _n(vals.get("time"))
        if t is not None:
            self.box(screen, S(20), H - S(70), S(200), S(56), (120, 160, 255), fill=(20, 40, 140, 230), radius=6, width=4)
            self.text(screen, f"0:{int(t):02d}", S(120), H - S(42), 30, WHITE, key="black", align="center", valign="middle")


# ============================================================================ Power Spikes II
def volley_draw(shirt, frame):
    """A volleyball player of our own seen from the side, facing right. Frames 0 ready, 1 jump with the arm up, 2 dig.
    / Un joueur de volley à nous, de profil. Images 0 prêt, 1 saut bras levé, 2 manchette."""
    def fn(d, W, H):
        dark = DARKLINE
        u = H
        skin = (226, 176, 136, 255)
        cx = W * 0.5
        legs = ((-0.06, 0.97), (0.08, 0.97)) if frame != 1 else ((-0.04, 0.9), (0.06, 0.86))
        for i, (dx, fy) in enumerate(legs):
            _capsule(d, (cx, H * 0.58), (cx + dx * u, H * 0.78), 0.05 * u, 0.045 * u, skin, dark, max(1, W * 0.02))
            _capsule(d, (cx + dx * u, H * 0.78), (cx + dx * u * 1.2, fy * H), 0.045 * u, 0.04 * u, skin, dark, max(1, W * 0.02))
        d.rectangle([cx - 0.08 * u, H * 0.5, cx + 0.08 * u, H * 0.62], fill=(30, 30, 40, 255))
        d.rounded_rectangle([cx - 0.09 * u, H * 0.26, cx + 0.09 * u, H * 0.54], radius=0.03 * u, fill=shirt + (255,), outline=dark)
        if frame == 1:
            _capsule(d, (cx + 0.04 * u, H * 0.3), (cx + 0.14 * u, H * 0.02), 0.04 * u, 0.035 * u, skin, dark, max(1, W * 0.02))
        elif frame == 2:
            _capsule(d, (cx + 0.02 * u, H * 0.32), (cx + 0.18 * u, H * 0.5), 0.04 * u, 0.035 * u, skin, dark, max(1, W * 0.02))
        else:
            _capsule(d, (cx + 0.02 * u, H * 0.32), (cx + 0.16 * u, H * 0.3), 0.04 * u, 0.035 * u, skin, dark, max(1, W * 0.02))
        r = 0.07 * u
        d.ellipse([cx - r, H * 0.1, cx + r, H * 0.1 + 2 * r], fill=skin, outline=dark)
        d.chord([cx - r * 1.05, H * 0.1 - r * 0.1, cx + r, H * 0.1 + r * 1.1], 180, 360, fill=(60, 40, 30, 255))
    return fn


class PowerSpikes2Scene(GameScene):
    """Power Spikes II as in the game: the indoor arena, its lamps and its stands, three players on each side of the
    net, the ball flies from one side to the other, jumps and spikes. A super shot spent in the game is a spike on fire.
    Time at the top, the power gauges at the bottom. / La salle, trois joueurs de chaque côté du filet, smashs, comme dans le jeu."""
    THEME = "ps2_arena"
    STATIC = True
    SHADE = (60, 0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.side = 0
        self.ball = None
        self.next_t = 0.0
        self.spikes = 0                                    # (tests)
        self.supers = 0
        self.jump = {}
        self.calm = 0                                      # passes since the last spike / passes depuis le dernier smash

    def court_x(self, side, k):
        return self.W / 2 + (-1 if side == 0 else 1) * self.S(120 + 220 * k)

    def hit(self, now, fire=False):
        """The ball goes to the other side: a pass, or a spike. / La balle passe de l'autre côté : une passe, ou un smash."""
        S = self.S
        to = 1 - self.side
        x0 = self.court_x(self.side, self.rng.choice((0, 1, 2)))
        x1 = self.court_x(to, self.rng.uniform(0.2, 2.2))
        spike = fire or self.calm >= 2 or self.rng.random() < 0.4         # never more than two passes in a row
        self.calm = 0 if spike else self.calm + 1
        if spike:
            self.spikes += 1
            self.jump[(self.side, 0)] = now
            x0 = self.court_x(self.side, 0)
        self.ball = {"x0": x0, "y0": S(PS_FLOOR) - S(260 if spike else 150), "x1": x1, "y1": S(PS_FLOOR) - S(40), "t0": now,
                     "dur": 0.45 if spike else 1.1, "arc": S(20) if spike else S(220), "fire": fire}
        self.side = to
        self.next_t = now + self.ball["dur"] + 0.25

    def update(self, vals, now):
        if now >= self.next_t:
            self.hit(now)
        for suf in ("", "_p2"):
            ch = self.changed(vals, "power" + suf)
            if ch and ch[1] < ch[0] - 8:                                # the power spent: a spike on fire
                self.supers += 1
                self.popup("POWER SPIKE!", self.W / 2, self.S(200), (255, 150, 60), 40)
                self.hit(now, fire=True)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        net_top = S(PS_FLOOR) - S(190)
        pg.draw.rect(screen, (230, 230, 230), (int(W / 2 - S(3)), int(net_top), S(6), S(190)))
        for k in range(8):
            y = net_top + S(6) + k * S(12)
            pg.draw.line(screen, (200, 200, 210), (int(W / 2 - S(4)), int(y)), (int(W / 2 + S(4)), int(y)), 1)
        for side, shirt in ((0, (250, 250, 250)), (1, (220, 50, 50))):
            for k in range(3):
                x = self.court_x(side, k)
                j = self.jump.get((side, k), -99.0)
                jumping = now - j < 0.5
                frame = 1 if jumping else (2 if self.side == side and k == 2 else 0)
                img = self.img(("vb", side, frame), S(90), S(170), volley_draw(shirt, frame), ss=2, flip=side == 1)
                lift = math.sin(_clamp((now - j) / 0.5) * math.pi) * S(80) if jumping else 0
                screen.blit(img, (int(x - img.get_width() / 2), int(S(PS_FLOOR) - img.get_height() - lift)))
        b = self.ball
        if b is not None:
            k = _clamp((now - b["t0"]) / b["dur"])
            x = b["x0"] + (b["x1"] - b["x0"]) * k
            y = b["y0"] + (b["y1"] - b["y0"]) * k - math.sin(k * math.pi) * b["arc"]
            if b["fire"]:
                self.fx.sparks(x, y, 3, (255, 160, 40), (60, 160), (0, 360), (0.2, 0.4), 0, "front", 6, 20)
            pg.draw.circle(screen, (250, 250, 240), (int(x), int(y)), S(12))
            pg.draw.circle(screen, (60, 120, 220), (int(x), int(y)), S(12), max(1, S(3)))
        self.hd.draw_logo(screen, logo, W / 2, S(4), S(360), S(64), now)
        tm, ts = _n(vals.get("time_min")), _n(vals.get("time_sec"))
        if tm is not None and ts is not None:
            self.label(screen, f"Time {int(tm):02d}'{int(ts):02d}\"", W / 2, S(130), 34, (250, 230, 60), key="black", align="center")
        for side, name, x0 in (("p1", "power", S(30)), ("p2", "power_p2", W - S(330))):
            p = _n(vals.get(name))
            if p is None or (side == "p2" and not self.p2_in(vals)):
                continue
            self.pill(screen, x0 - S(10), S(10), S(320), S(56), 160, radius=12)
            self.text(screen, "POWER", x0, S(38), 22, CREAM, key="black", valign="middle", glow=0)
            self.bar(screen, x0 + S(96), S(28), S(200), S(20), p / 48.0, (255, 170, 60))
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


SCENES = {"twsoc96": TecmoSoccerScene, "goalx3": Goal3Scene, "neocup98": NeoCup98Scene, "socbrawl": SoccerBrawlScene, "fbfrenzy": FootballFrenzyScene,
          "pgoal": PleasureGoalScene, "bstars": BaseballStarsProScene, "2020bb": Baseball2020Scene, "tpgolf": TopPlayersGolfScene,
          "pspikes2": PowerSpikes2Scene}
