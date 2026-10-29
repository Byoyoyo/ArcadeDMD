"""HD scenes of the seventh batch of Neo Geo games done one by one (1.23), each drawn after screenshots of its game.
Each game has its own animated backdrop and reacts to the values read in its memory. The characters, the creatures and
the machines are creations of the program in the spirit of the games.

Scènes HD du septième lot de jeux Neo Geo faits un par un (1.23), chacune dessinée d'après des captures de son jeu.
Les personnages, les créatures et les engins sont des créations du programme dans l'esprit des jeux.
"""

import math

from .hd_games import CREAM, GOLD, WHITE, GameScene, _clamp, _n
from .hd_games2 import TEAMS, SoccerScene
from .hd_games3 import _capsule
from .hd_games5 import CyberLipScene, _mixc
from .hd_games6 import PuzzleDePonScene, SengokuScene, portrait_draw
from .hd_themes7 import NMD, SM_FLOOR, ZP_ROWS                    # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr

DARKLINE = (24, 20, 26, 255)


# ============================================================================ Puzzle De Pon! R!
class PuzzleDePonRScene(PuzzleDePonScene):
    """Puzzle De Pon! R! as in the game: the same boards between their brick pillars and the star dial, under a pink sky
    full of stars. / Les mêmes plateaux et le cadran étoilé, sous un ciel rose étoilé, comme dans le jeu."""
    THEME = "pdpr_stars"


# ============================================================================ Spin Master
def spinner_draw(frame):
    """Our hero of the adventure, facing right: red spiky hair, a blue jacket, a yo-yo in hand. Frames 0 and 1 run,
    2 throw. / Notre héros de l'aventure, cheveux rouges en pointes, veste bleue, un yo-yo à la main."""
    def fn(d, W, H):
        dark = DARKLINE
        ow = max(1.0, W * 0.025)
        skin, jacket, jacket_d, pants = (250, 200, 160, 255), (50, 110, 220, 255), (30, 80, 170, 255), (230, 200, 120, 255)
        u = H
        cx = W * 0.42
        step = (0.12, -0.1) if frame == 0 else ((-0.1, 0.12) if frame == 1 else (0.08, -0.06))
        for i, dx in enumerate(step):
            k = (cx + dx * 0.5 * u, H * 0.8)
            f = (cx + dx * u, H * 0.96)
            _capsule(d, (cx, H * 0.6), k, 0.06 * u, 0.055 * u, pants, dark, ow)
            _capsule(d, k, f, 0.05 * u, 0.045 * u, pants, dark, ow)
            d.rounded_rectangle([f[0] - 0.06 * u, f[1] - 0.05 * u, f[0] + 0.09 * u, f[1] + 0.02 * u], radius=0.02 * u, fill=(200, 50, 40, 255), outline=dark)
        d.rounded_rectangle([cx - 0.12 * u, H * 0.34, cx + 0.12 * u, H * 0.62], radius=0.05 * u, fill=jacket, outline=dark, width=int(ow))
        hand = (cx + 0.3 * u, H * 0.4) if frame == 2 else (cx + 0.14 * u, H * 0.52)
        _capsule(d, (cx + 0.04 * u, H * 0.4), hand, 0.045 * u, 0.04 * u, jacket_d, dark, ow)
        d.ellipse([hand[0] - 0.035 * u, hand[1] - 0.035 * u, hand[0] + 0.035 * u, hand[1] + 0.035 * u], fill=skin, outline=dark)
        if frame != 2:                                                 # le yo-yo dans la main
            d.ellipse([hand[0] - 0.05 * u, hand[1] + 0.02 * u, hand[0] + 0.05 * u, hand[1] + 0.12 * u], fill=(240, 60, 40, 255), outline=dark)
        hx, hy, r = cx + 0.02 * u, H * 0.2, 0.13 * u
        d.ellipse([hx - r, hy - r, hx + r, hy + r * 1.05], fill=skin, outline=dark, width=int(ow))
        d.ellipse([hx + r * 0.3, hy - r * 0.15, hx + r * 0.6, hy + r * 0.2], fill=(255, 255, 255, 255), outline=dark)
        d.ellipse([hx + r * 0.42, hy - r * 0.05, hx + r * 0.56, hy + r * 0.12], fill=dark)
        for k in range(5):                                             # les cheveux en pointes
            a = math.pi * (1.05 + k * 0.18)
            bx, by = hx + math.cos(a) * r * 0.9, hy + math.sin(a) * r * 0.9
            tx, ty = hx + math.cos(a - 0.15) * r * 1.8, hy + math.sin(a - 0.15) * r * 1.8
            d.polygon([(bx - r * 0.25, by + r * 0.1), (tx, ty), (bx + r * 0.25, by)], fill=(230, 60, 30, 255), outline=dark)
        d.chord([hx - r * 1.02, hy - r * 1.05, hx + r * 0.95, hy + r * 0.2], 180, 360, fill=(230, 60, 30, 255))
    return fn


def grunt_side_draw(frame):
    """An enemy soldier of the adventure, facing left, a round helmet. / Un soldat ennemi de l'aventure, casque rond."""
    def fn(d, W, H):
        dark = DARKLINE
        ow = max(1.0, W * 0.025)
        u = H
        cx = W * 0.5
        step = (0.1, -0.08) if frame == 0 else (-0.08, 0.1)
        for i, dx in enumerate(step):
            f = (cx + dx * u, H * 0.96)
            _capsule(d, (cx, H * 0.6), f, 0.055 * u, 0.05 * u, (90, 110, 60, 255), dark, ow)
            d.ellipse([f[0] - 0.07 * u, f[1] - 0.05 * u, f[0] + 0.05 * u, f[1] + 0.02 * u], fill=(50, 40, 30, 255))
        d.ellipse([cx - 0.16 * u, H * 0.32, cx + 0.16 * u, H * 0.66], fill=(110, 130, 70, 255), outline=dark, width=int(ow))
        hx, hy, r = cx - 0.02 * u, H * 0.2, 0.13 * u
        d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(240, 196, 150, 255), outline=dark, width=int(ow))
        d.ellipse([hx - r * 0.7, hy - r * 0.2, hx - r * 0.2, hy + r * 0.3], fill=(255, 255, 255, 255), outline=dark)
        d.ellipse([hx - r * 0.6, hy - r * 0.05, hx - r * 0.35, hy + r * 0.2], fill=dark)
        d.chord([hx - r * 1.15, hy - r * 1.2, hx + r * 1.15, hy + r * 0.35], 180, 360, fill=(80, 100, 50, 255), outline=dark)
        _capsule(d, (cx - 0.04 * u, H * 0.42), (cx - 0.26 * u, H * 0.46), 0.04 * u, 0.035 * u, (110, 130, 70, 255), dark, ow)
    return fn


class SpinMasterScene(CyberLipScene):
    """Spin Master as in the game: the desert of the pyramids, our hero of our own throws his yo-yo at the soldiers and
    the birds that come. 1P and the score, the health gauge in orange segments, the bombs B, the lives at the bottom.
    / Le désert des pyramides, notre héros lance son yo-yo sur les soldats et les oiseaux, comme dans le jeu."""
    THEME = "sm_desert"
    SHADE = (60, 60)
    EXPLOSIONS = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.throws = 0                                   # (tests)
        self.bombs_used = 0

    def hero(self, frame):
        S = self.S
        return self.img(("smhero", frame), S(120), S(150), spinner_draw(frame), ss=2)

    def foe(self, frame):
        S = self.S
        return self.img(("smgrunt", frame), S(110), S(130), grunt_side_draw(frame), ss=2)

    def flyer(self, now):
        S = self.S
        return self.img("smbird", S(100), S(70), bird_draw, ss=2)

    def floor(self):
        return self.S(SM_FLOOR) + self.S(20)

    def move(self, vals, now, idle):
        return 0.2 if idle else 0.8

    def update(self, vals, now):
        S, rng = self.S, self.rng
        if now >= self.next_foe:
            self.next_foe = now + rng.uniform(0.6, 1.3)
            fly = rng.random() < 0.3
            self.foes.append({"x": self.W + S(80), "y": S(rng.uniform(170, 260)) if fly else self.floor(), "fly": fly, "hp": 2,
                              "v": rng.uniform(110, 180) * self.s, "ph": rng.uniform(0, 6), "t0": now})
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.hurt = now
            self.popup(tr("-1 VIE", "-1 LIFE"), self.W * 0.3, self.floor() - S(200), (255, 90, 70), 38)
        ch = self.changed(vals, "energy")
        if ch and ch[1] < ch[0]:
            self.hurt = now
            self.fx.shake(5, 0.2)
        ch = self.changed(vals, "bombs")
        if ch and ch[1] < ch[0]:                                       # a bomb: everything on screen blows up
            self.bombs_used += 1
            self.fx.flash((255, 230, 180), 0.25, 0.3)
            for f in self.foes:
                if not f.get("dead") and f["x"] < self.W:
                    self.fx.later(rng.uniform(0.05, 0.4), self.kill, f, now)
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:
            live = [f for f in self.foes if not f.get("dead") and self.W * 0.35 < f["x"] < self.W * 0.9]
            if live:
                self.kill(min(live, key=lambda f: f["x"]), now)
        if now >= self.fire_t and any(not f.get("dead") and self.W * 0.35 < f["x"] < self.W * 0.85 for f in self.foes):
            self.fire_t = now + rng.uniform(0.5, 0.9)
            self.fire(now)

    def fire(self, now):
        """The yo-yo flies to the nearest enemy and comes back. / Le yo-yo file vers l'ennemi le plus proche et revient."""
        S, fx = self.S, self.fx
        x0, y0 = self.W * 0.3 + S(40), self.floor() - S(90)
        live = [f for f in self.foes if not f.get("dead") and f["x"] > x0]
        tgt = min(live, key=lambda f: f["x"]) if live else None
        tx, ty = (tgt["x"], tgt["y"] - (S(50) if not tgt["fly"] else 0)) if tgt else (self.W * 0.7, y0)
        self.throws += 1
        fx.tracer(x0, y0, tx, ty, 2600, (240, 70, 50), 14, 20, "front", False)
        fx.later(abs(tx - x0) / (2600 * self.s), fx.tracer, tx, ty, x0, y0, 2600, (240, 70, 50), 14, 20, "front", False)
        if tgt is not None:
            tgt["hp"] -= 1
            if tgt["hp"] <= 0:
                fx.later(abs(tx - x0) / (2600 * self.s), self.kill, tgt, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score, the health gauge in orange segments, the bombs B; the lives at the bottom left.
        / Comme dans le jeu : 1P et le score, la vie en segments orange, les bombes B ; les vies en bas à gauche."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(460), S(112), 160, radius=14)
        self.text(screen, "1P", S(28), S(28), 28, (255, 230, 80), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(440), S(10), "right", S(40))
        e = _n(vals.get("energy"))
        if e is not None:
            for i in range(5):
                c = (250, 140, 30) if i < int(e) else (60, 40, 30)
                pg.draw.rect(screen, c, (S(28) + i * S(64), S(50), S(60), S(20)))
            pg.draw.rect(screen, (250, 250, 250), (S(26), S(48), S(324), S(24)), max(1, S(2)))
        b = _n(vals.get("bombs"))
        if b is not None:
            for i in range(min(6, int(b))):
                pg.draw.rect(screen, (220, 60, 30), (S(28) + i * S(40), S(80), S(34), S(30)), border_radius=S(4))
                self.text(screen, "B", S(45) + i * S(40), S(95), 22, WHITE, key="black", align="center", valign="middle", glow=0)
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.label(screen, f"={int(lives):02d}", S(80), H - S(34), 30, (255, 230, 120), align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


def bird_draw(d, W, H):
    """A big bird of the desert, facing left, wings up. / Un grand oiseau du désert, face à gauche."""
    dark = DARKLINE
    d.polygon([(W * 0.3, H * 0.5), (W * 0.6, H * 0.0), (W * 0.75, H * 0.45)], fill=(150, 100, 60, 255), outline=dark)
    d.ellipse([W * 0.2, H * 0.4, W * 0.85, H * 0.8], fill=(190, 140, 80, 255), outline=dark, width=max(1, int(W * 0.03)))
    d.ellipse([W * 0.05, H * 0.36, W * 0.32, H * 0.62], fill=(230, 220, 200, 255), outline=dark)
    d.polygon([(W * 0.08, H * 0.5), (W * 0.0, H * 0.56), (W * 0.1, H * 0.58)], fill=(240, 190, 50, 255))
    d.ellipse([W * 0.12, H * 0.44, W * 0.18, H * 0.5], fill=dark)
    d.polygon([(W * 0.8, H * 0.6), (W * 1.0, H * 0.5), (W * 0.98, H * 0.72)], fill=(150, 100, 60, 255), outline=dark)


# ============================================================================ Ganryu
class GanryuScene(SengokuScene):
    """Ganryu as in the game: a street of old Japan at night, wooden houses and their crested curtains, our swordsman of
    our own fights the ninjas of the night. PLAYER_1 and the score, the yellow gauge, TIME in big numbers, a face of our
    own for each life, the weapon and its count. / Une rue du vieux Japon la nuit, notre sabreur face aux ninjas."""
    THEME = "gr_town"
    HERO = ("jacket", (60, 70, 120), (220, 210, 190), (226, 176, 136), (90, 50, 30), "sword")
    FOES = (("ninja", (40, 44, 70), (30, 34, 54), (210, 180, 150), (0, 0, 0), "sword"), ("ninja", (70, 40, 60), (50, 30, 44), (210, 180, 150),
                                                                                          (0, 0, 0), "sword"))
    ENERGY_MAX = 6

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.thrown = 0                                   # (tests)

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "ammo")
        if ch and ch[1] < ch[0]:                                       # a shuriken thrown / un shuriken lancé
            self.thrown += 1
            S = self.S
            h = self.hero
            f = self.nearest()
            tx = f["x"] if f else h["x"] + h["face"] * S(600)
            ty = (self.ground(f["z"]) if f else self.ground(h["z"])) - S(150)
            self.fx.tracer(h["x"], self.ground(h["z"]) - S(160), tx, ty, 2400, (220, 230, 255), 6, 30, "front", True)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: PLAYER_1 and the score, the yellow gauge, TIME, a face for each life, the weapon and its count.
        / Comme dans le jeu : PLAYER_1 et le score, la jauge jaune, TIME, un visage par vie, l'arme et son nombre."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(380), S(70), now)
        self.pill(screen, S(12), S(6), S(470), S(120), 160, radius=14)
        self.text(screen, "PLAYER_1", S(28), S(26), 26, (250, 210, 120), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(460), S(30), "right", S(36))
        hit = max(0.0, 1 - (now - self.hero["hurt"]) / 3.0)
        self.bar(screen, S(28), S(68), S(330), S(18), 1 - 0.3 * hit, (250, 220, 40))
        lives = _n(vals.get("lives"))
        if lives is not None:
            face = self.img("grface", S(30), S(30), portrait_draw((226, 176, 136), (90, 50, 30), (200, 40, 40), bg=(160, 40, 40)), ss=2)
            for i in range(min(6, int(lives))):
                screen.blit(face, (S(28) + i * S(34), S(92)))
        t = _n(vals.get("time"))
        if t is not None:
            self.pill(screen, W / 2 + S(210), S(6), S(150), S(110), 160, radius=14)
            self.text(screen, "TIME", W / 2 + S(285), S(26), 26, (250, 210, 120), key="black", align="center", valign="middle")
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(60), (255, 230, 60), W / 2 + S(285), S(76), "center", "middle")
        a = _n(vals.get("ammo"))
        w = _n(vals.get("weapon"))
        if a is not None:
            self.pill(screen, S(12), H - S(64), S(220), S(54), 160, radius=12)
            col = (180, 200, 255) if w == 2 else (250, 140, 60)
            self.text(screen, "✦" if w == 2 else "/", S(40), H - S(37), 30, col, key="black", align="center", valign="middle")
            self.text(screen, f"x{int(a)}", S(70), H - S(37), 30, WHITE, key="black", valign="middle")
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, colw, align="right")


# ============================================================================ Super Sidekicks, Super Sidekicks 2
def flag_draw(kit):
    """A flag in the colours of the team. / Un drapeau aux couleurs de l'équipe."""
    def fn(d, W, H):
        d.rectangle([0, 0, W - 1, H - 1], fill=kit["shirt"] + (255,))
        d.rectangle([W / 3, 0, W * 2 / 3, H - 1], fill=kit["shorts"] + (255,))
        d.rectangle([0, 0, W - 1, H - 1], outline=(30, 30, 30, 255), width=max(1, int(W * 0.04)))
    return fn


class SuperSidekicksScene(SoccerScene):
    """Super Sidekicks as in the game: the match on the green pitch, the two flags with the goals in their orange boxes,
    TIME on its panel at the top. / Le match sur la pelouse verte, les drapeaux et les buts, TIME en haut, comme dans le jeu."""
    THEME = "stadium_day"

    def scoreboard(self, screen, vals, now):
        S, W, hd = self.S, self.W, self.hd
        for side, name, x, kit in (("p1", "goals", S(40), TEAMS[0]), ("p2", "goals_p2", W / 2 + S(320), TEAMS[1])):
            self.pill(screen, x - S(10), S(10), S(240), S(76), 160, radius=12)
            screen.blit(self.img(("ssflag", side), S(90), S(56), flag_draw(kit), ss=1), (x, S(20)))
            v = _n(vals.get(name))
            if v is not None:
                self.box(screen, x + S(120), S(16), S(80), S(64), (250, 200, 60), fill=(200, 60, 20, 230), radius=8, width=3)
                k = now - self.gpop[name]
                hd.put_number(screen, f"{int(v)}", "black", S(50), WHITE if k < 1.0 and int(k * 8) % 2 == 0 else (255, 230, 120), x + S(160), S(48),
                              "center", "middle")
        tm, ts = _n(vals.get("time_min")), _n(vals.get("time_sec"))
        if tm is not None and ts is not None:
            cx = W / 2 - S(380)
            self.box(screen, cx - S(80), S(100), S(160), S(70), (200, 200, 210), fill=(30, 30, 36, 230), radius=8, width=3)
            self.text(screen, "TIME", cx, S(114), 20, CREAM, key="black", align="center", valign="middle", glow=0)
            hd.put_number(screen, f"{int(tm)}:{int(ts):02d}", "stencil", S(36), (255, 220, 60), cx, S(146), "center", "middle")


class SuperSidekicks2Scene(SoccerScene):
    """Super Sidekicks 2 as in the game: the match seen from the side of the stadium, the blue band at the top with
    the two flags and the goals in big white numbers. / Le match, le bandeau bleu en haut avec les drapeaux et les buts."""
    THEME = "stadium_day"

    def scoreboard(self, screen, vals, now):
        S, pg, hd = self.S, self.pg, self.hd
        band = self.imgs.get("ss2band")
        if band is None:
            band = self.imgs["ss2band"] = pg.Surface((S(700), S(70)), pg.SRCALPHA)
            band.fill((20, 60, 200, 220))
        screen.blit(band, (S(10), S(10)))
        for side, name, x, kit in (("p1", "goals", S(24), TEAMS[0]), ("p2", "goals_p2", S(560), TEAMS[1])):
            screen.blit(self.img(("ss2flag", side), S(100), S(56), flag_draw(kit), ss=1), (x, S(17)))
            v = _n(vals.get(name))
            if v is not None:
                k = now - self.gpop[name]
                hd.put_number(screen, f"{int(v)}", "black", S(60), (255, 230, 120) if k < 1.0 and int(k * 8) % 2 == 0 else WHITE,
                              x + (S(150) if side == "p1" else -S(50)), S(45), "center", "middle")
        self.text(screen, "TIME", S(360), S(45), 30, WHITE, key="black", align="center", valign="middle")


# ============================================================================ Panic Bomber
PB_COLORS = ((250, 250, 250), (240, 60, 50), (60, 120, 240), (60, 200, 90))
BOMB_KIND = 4


def head_draw(k):
    """A round little robot head of our own with a helmet in its colour; kind 4 is a bomb with its fuse.
    / Une petite tête ronde de robot à nous, casque de sa couleur ; le genre 4 est une bombe et sa mèche."""
    def fn(d, W, H):
        dark = DARKLINE
        if k == BOMB_KIND:
            d.ellipse([W * 0.08, H * 0.16, W * 0.92, H * 0.98], fill=(40, 40, 50, 255), outline=dark)
            d.ellipse([W * 0.24, H * 0.3, W * 0.42, H * 0.46], fill=(140, 140, 160, 255))
            d.line([(W * 0.6, H * 0.2), (W * 0.78, H * 0.04)], fill=(200, 170, 120, 255), width=max(1, int(W * 0.08)))
            d.ellipse([W * 0.7, H * 0.0, W * 0.9, H * 0.16], fill=(255, 200, 60, 255))
            return
        col = PB_COLORS[k % len(PB_COLORS)] + (255,)
        d.ellipse([W * 0.06, H * 0.08, W * 0.94, H * 0.96], fill=col, outline=dark, width=max(1, int(W * 0.05)))
        d.rounded_rectangle([W * 0.2, H * 0.36, W * 0.8, H * 0.76], radius=W * 0.12, fill=(250, 220, 190, 255), outline=dark)
        for ex in (0.38, 0.62):
            d.ellipse([W * (ex - 0.06), H * 0.44, W * (ex + 0.06), H * 0.62], fill=dark)
        d.ellipse([W * 0.44, H * 0.0, W * 0.56, H * 0.14], fill=(250, 120, 160, 255), outline=dark)
    return fn


class BombField:
    """A field of six columns where the pieces of three heads fall and stack; three of a colour in a line burst, a bomb
    blows up in a cross. / Un champ de six colonnes où tombent les pièces de trois têtes ; une bombe saute en croix."""
    COLS, ROWS = 6, 10

    def __init__(self, scene, x0):
        self.sc, self.rng = scene, scene.rng
        self.C = scene.S(36)
        self.x0, self.y0 = x0, scene.S(96)
        self.grid = [[None] * self.ROWS for _ in range(self.COLS)]           # [col][row from the bottom]
        self.piece = None
        self.next = self.new_piece()
        self.landed = 0                                                      # (tests)
        for c in range(self.COLS):                                           # a few heads already there
            for r in range(self.rng.randint(1, 3)):
                self.grid[c][r] = self.rng.choice((0, 1, 2, 3, 3, BOMB_KIND))

    def new_piece(self):
        return [self.rng.choice((0, 1, 2, 3)) for _ in range(2)] + [self.rng.choice((0, 1, 2, 3, BOMB_KIND))]

    def xy(self, c, r):
        return self.x0 + (c + 0.5) * self.C, self.y0 + (self.ROWS - r - 0.5) * self.C

    def height(self, c):
        col = self.grid[c]
        return max([r + 1 for r in range(self.ROWS) if col[r] is not None] or [0])

    def step(self, dt, now):
        if self.piece is None:
            c = self.rng.randrange(self.COLS)
            self.piece = {"c": c, "y": self.y0 - 3 * self.C, "cells": self.next}
            self.next = self.new_piece()
        p = self.piece
        p["y"] += self.sc.S(260) * dt
        h = self.height(p["c"])
        land = self.y0 + (self.ROWS - h) * self.C - 3 * self.C
        if p["y"] >= land:
            for i, k in enumerate(reversed(p["cells"])):
                r = h + i
                if r < self.ROWS:
                    self.grid[p["c"]][r] = k
            self.piece = None
            self.landed += 1
            self.resolve(now)
            if max(self.height(c) for c in range(self.COLS)) >= self.ROWS - 1:
                self.clear()

    def resolve(self, now):
        gone = set()
        for c in range(self.COLS):
            for r in range(self.ROWS):
                k = self.grid[c][r]
                if k is None or k == BOMB_KIND:
                    continue
                for dc, dr in ((1, 0), (0, 1)):
                    run = [(c, r)]
                    cc, rr = c + dc, r + dr
                    while cc < self.COLS and rr < self.ROWS and self.grid[cc][rr] == k:
                        run.append((cc, rr))
                        cc, rr = cc + dc, rr + dr
                    if len(run) >= 3:
                        gone.update(run)
        for c, r in gone:
            x, y = self.xy(c, r)
            self.sc.burst(x, y, self.grid[c][r])
            self.grid[c][r] = None
        if gone:
            self.sc.popped += len(gone)
            self.fall()

    def fall(self):
        for c in range(self.COLS):
            col = [k for k in self.grid[c] if k is not None]
            self.grid[c] = col + [None] * (self.ROWS - len(col))

    def blast(self, now, big=False):
        """A bomb of the field blows up in a cross. / Une bombe du champ saute en croix."""
        bombs = [(c, r) for c in range(self.COLS) for r in range(self.ROWS) if self.grid[c][r] == BOMB_KIND]
        if not bombs:
            c = self.rng.randrange(self.COLS)
            r = max(0, self.height(c) - 1)
        else:
            c, r = self.rng.choice(bombs)
        reach = 6 if big else 2
        cells = {(c, r)} | {(c + i, r) for i in range(-reach, reach + 1) if 0 <= c + i < self.COLS} | \
            {(c, r + i) for i in range(-reach, reach + 1) if 0 <= r + i < self.ROWS}
        x, y = self.xy(c, r)
        fx = self.sc.fx
        x0, _ = self.xy(max(0, c - reach), r)
        x1, _ = self.xy(min(self.COLS - 1, c + reach), r)
        _, y0 = self.xy(c, min(self.ROWS - 1, r + reach))
        _, y1 = self.xy(c, max(0, r - reach))
        for a, b in (((x, y), (x0, y)), ((x, y), (x1, y)), ((x, y), (x, y0)), ((x, y), (x, y1))):
            fx.tracer(a[0], a[1], b[0], b[1], 1600, (255, 160, 40), 26, 200, "front", False)
            fx.tracer(a[0], a[1], b[0], b[1], 1600, (255, 240, 170), 10, 160, "front", False)
        fx.glow(x, y, 30, 120, (255, 200, 80), 0.4, "front", 1.0, 0.0)
        fx.shake(6 if big else 3, 0.25)
        for cc, rr in cells:
            if self.grid[cc][rr] is not None:
                self.grid[cc][rr] = None
                self.sc.popped += 1
        self.sc.blasts += 1
        self.fall()

    def clear(self):
        for c in range(self.COLS):
            for r in range(self.ROWS):
                if self.grid[c][r] is not None:
                    x, y = self.xy(c, r)
                    self.sc.fx.later(0.01 * (c + r * self.COLS), self.sc.burst, x, y, self.grid[c][r])
        self.grid = [[None] * self.ROWS for _ in range(self.COLS)]


class PanicBomberScene(GameScene):
    """Panic Bomber as in the game: two fields on the green checkerboard, the pieces of three little heads fall and
    stack, three of a colour burst, the bombs blow up in a cross of flames. The points read in the game set the bombs
    off, the power going up is a big blast. SCORE and NEXT above each field.
    / Deux champs sur le damier vert, les pièces de trois têtes tombent, les bombes sautent en croix, comme dans le jeu."""
    THEME = "pbm_check"
    STATIC = True
    SHADE = (60, 0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S, W = self.S, self.W
        fw = BombField.COLS * S(36)
        self.fields = {"p1": BombField(self, W / 2 - S(330) - fw / 2), "p2": BombField(self, W / 2 + S(330) - fw / 2)}
        self.popped = 0                                   # (tests)
        self.blasts = 0
        self.warm += [(self.head, (k, 36)) for k in range(5)]

    def head(self, k, size):
        S = self.S
        return self.img(("pbhead", k, size), S(size), S(size), head_draw(k), ss=2)

    def burst(self, x, y, k):
        col = PB_COLORS[k % len(PB_COLORS)] if k != BOMB_KIND else (255, 160, 40)
        self.fx.sparks(x, y, 10, col, (200, 500), (0, 360), (0.2, 0.4), 400, "front", 4, 12)

    def update(self, vals, now):
        for side, suf in (("p1", ""), ("p2", "_p2")):
            if side == "p2" and not self.p2_in(vals):
                continue
            f = self.fields[side]
            f.step(self.dt, now)
            ch = self.changed(vals, "power" + suf)
            if ch and ch[1] > ch[0]:
                f.blast(now, big=True)
                x, _ = f.xy(2.5, 5)
                self.popup("POWER UP !", x, self.S(250), GOLD, 40)
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:
            self.fields["p1"].blast(now)
            x, _ = self.fields["p1"].xy(2.5, 5)
            self.popup(f"{int(ch[1] - ch[0])} Pts.", x, self.S(220), WHITE, 40)

    def draw_hud(self, screen, eng, vals, logo, now):
        S = self.S
        self.hd.draw_logo(screen, logo, self.W / 2, S(8), S(440), S(84), now)
        for side, f in self.fields.items():
            if side == "p2" and not self.p2_in(vals):
                x, _ = f.xy(2.5, 5)
                word, col = self.invite(vals, now)
                self.label(screen, word, x, S(280), 34, col, align="center")
                continue
            w, h = f.C * f.COLS, f.C * f.ROWS
            self.box(screen, f.x0 - S(8), f.y0 - S(8), w + S(16), h + S(14), (250, 230, 60), fill=(30, 40, 90, 230), radius=6, width=4)
            for c in range(f.COLS):
                for r in range(f.ROWS):
                    k = f.grid[c][r]
                    if k is not None:
                        img = self.head(k, 36)
                        x, y = f.xy(c, r)
                        screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
            if f.piece is not None:
                p = f.piece
                for i, k in enumerate(p["cells"]):
                    y = p["y"] + (i + 0.5) * f.C
                    if y < f.y0:
                        continue
                    img = self.head(k, 36)
                    x, _ = f.xy(p["c"], 0)
                    screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
            nx = f.x0 + w + S(30)                                        # NEXT, as in the game
            self.box(screen, nx - S(6), f.y0 - S(8), S(60), S(124), (60, 220, 250), fill=(20, 30, 120, 230), radius=6, width=3)
            for i, k in enumerate(f.next):
                img = self.head(k, 32)
                screen.blit(img, (int(nx + S(8)), int(f.y0 + i * S(36))))
            sc_name = "score" if side == "p1" else "score_p2"
            self.box(screen, f.x0 - S(8), S(36), w + S(16), S(50), (250, 120, 200), fill=(20, 30, 90, 230), radius=6, width=3)
            self.text(screen, "SCORE", f.x0 + S(4), S(61), 20, (250, 230, 120), key="black", valign="middle", glow=0)
            v = _n(vals.get(sc_name))
            if v is not None:
                self.hd.put_number(screen, f"{int(v)}", "black", S(28), WHITE, f.x0 + w, S(61), "right", "middle")
            pw = _n(vals.get("power" if side == "p1" else "power_p2"))
            if pw is not None:
                self.text(screen, f"POWER {int(pw)}", nx, f.y0 + S(140), 20, (250, 230, 120), key="black", glow=0)


# ============================================================================ Pop 'n Bounce
POP_COLORS = ((240, 60, 50), (60, 120, 240), (250, 200, 40), (60, 190, 80))


def blob_draw(k):
    """A soft round creature of our own, in its colour, with two eyes. / Une créature ronde et molle à nous, deux yeux."""
    def fn(d, W, H):
        col = POP_COLORS[k % len(POP_COLORS)]
        d.ellipse([W * 0.04, H * 0.14, W * 0.96, H * 0.96], fill=col + (255,), outline=DARKLINE, width=max(1, int(W * 0.05)))
        d.ellipse([W * 0.14, H * 0.2, W * 0.5, H * 0.46], fill=_mixc(col, (255, 255, 255), 0.4))
        for ex in (0.36, 0.64):
            d.ellipse([W * (ex - 0.1), H * 0.36, W * (ex + 0.1), H * 0.62], fill=(255, 255, 255, 255), outline=DARKLINE)
            d.ellipse([W * (ex - 0.04), H * 0.44, W * (ex + 0.04), H * 0.56], fill=DARKLINE)
    return fn


class PopBounceScene(GameScene):
    """Pop 'n Bounce as in the game: two fields at dusk in the jungle, the soft creatures piled up at the top, the bar at
    the bottom sends the ball back, a creature hit bursts with the ones of its colour that touch it. The lives and BALL
    between the fields. / Deux champs, les créatures entassées en haut, la barre renvoie la balle, comme dans le jeu."""
    THEME = "pnb_jungle"
    STATIC = True
    SHADE = (60, 0)
    COLS, ROWS = 10, 6

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S, W = self.S, self.W
        self.FW = S(52) * self.COLS
        self.sides = {}
        for side, x0 in (("p1", S(60)), ("p2", W - S(60) - self.FW)):
            self.sides[side] = {"x0": x0, "grid": {}, "ball": [x0 + self.FW / 2, S(380), S(360), -S(420)], "bar": x0 + self.FW / 2}
            self.fill(side, 4)
        self.popped = 0                                   # (tests)
        self.warm += [(self.blob, (k,)) for k in range(4)]

    def blob(self, k):
        S = self.S
        return self.img(("pnbblob", k), S(50), S(48), blob_draw(k), ss=2)

    def fill(self, side, rows):
        g = self.sides[side]["grid"]
        for r in range(rows):
            for c in range(self.COLS):
                if (c, r) not in g:
                    g[(c, r)] = self.rng.randrange(4)

    def cell_xy(self, side, c, r):
        S = self.S
        return self.sides[side]["x0"] + (c + 0.5) * S(52), S(96) + (r + 0.5) * S(44)

    def pop_group(self, side, c, r):
        g = self.sides[side]["grid"]
        k = g.get((c, r))
        if k is None:
            return 0
        todo, seen = [(c, r)], set()
        while todo:
            cc, rr = todo.pop()
            if (cc, rr) in seen or g.get((cc, rr)) != k:
                continue
            seen.add((cc, rr))
            todo += [(cc + 1, rr), (cc - 1, rr), (cc, rr + 1), (cc, rr - 1)]
        for cc, rr in seen:
            x, y = self.cell_xy(side, cc, rr)
            del g[(cc, rr)]
            self.fx.sparks(x, y, 8, POP_COLORS[k], (200, 450), (0, 360), (0.2, 0.4), 400, "front", 4, 12)
        self.popped += len(seen)
        return len(seen)

    def update(self, vals, now):
        S, dt = self.S, self.dt
        for side, sd in self.sides.items():
            if side == "p2" and not self.p2_in(vals):
                continue
            b = sd["ball"]
            b[0] += b[2] * dt
            b[1] += b[3] * dt
            x0, x1 = sd["x0"] + S(12), sd["x0"] + self.FW - S(12)
            if b[0] < x0 or b[0] > x1:
                b[2] = -b[2]
                b[0] = _clamp(b[0], x0, x1)
            if b[1] < S(90):
                b[3] = abs(b[3])
            sd["bar"] += _clamp(b[0] - sd["bar"], -S(900) * dt, S(900) * dt)
            if b[1] > S(410) and b[3] > 0:                                # the bar sends the ball back
                b[3] = -abs(b[3])
                b[2] = (b[0] - sd["bar"]) * 6 + self.rng.uniform(-S(60), S(60))
                if abs(b[2]) < S(120):
                    b[2] = S(120) if b[2] >= 0 else -S(120)
            c = int((b[0] - sd["x0"]) / S(52))
            r = int((b[1] - S(96)) / S(44))
            if (c, r) in sd["grid"]:
                self.pop_group(side, c, r)
                b[3] = abs(b[3])
            if len(sd["grid"]) < 14:
                g = {(cc, rr + 1): k for (cc, rr), k in sd["grid"].items() if rr + 1 < self.ROWS}
                sd["grid"] = g
                self.fill(side, 1)
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0] and self.sides["p1"]["grid"]:
            c, r = self.rng.choice(list(self.sides["p1"]["grid"]))
            self.pop_group("p1", c, r)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(420), S(80), now)
        for side, sd in self.sides.items():
            if side == "p2" and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, sd["x0"] + self.FW / 2, S(260), 34, col, align="center")
                continue
            self.box(screen, sd["x0"] - S(8), S(60), self.FW + S(16), S(392), (200, 160, 80), fill=(80, 90, 160, 110), radius=6, width=4)
            self.text(screen, "ATTACK", sd["x0"] + self.FW / 2, S(76), 26, (60, 90, 40), key="stencil", align="center", valign="middle", glow=0)
            for (c, r), k in sd["grid"].items():
                img = self.blob(k)
                x, y = self.cell_xy(side, c, r)
                screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
            pg.draw.rect(screen, (60, 70, 140), (int(sd["bar"] - S(46)), S(418), S(92), S(16)), border_radius=S(6))
            pg.draw.rect(screen, (200, 210, 255), (int(sd["bar"] - S(46)), S(418), S(92), S(16)), max(1, S(2)), border_radius=S(6))
            b = sd["ball"]
            pg.draw.circle(screen, (255, 230, 120), (int(b[0]), int(b[1])), S(9))
        self.pill(screen, W / 2 - S(80), S(150), S(160), S(220), 160, radius=14)
        self.text(screen, "1P", W / 2, S(176), 28, (250, 90, 70), key="black", align="center", valign="middle")
        v = _n(vals.get("score"))
        if v is not None:
            self.text(screen, f"{int(v)}", W / 2, S(214), 30, WHITE, key="black", align="center", valign="middle")
        lv = _n(vals.get("lives"))
        if lv is not None:
            self.text(screen, f"x{int(lv)}", W / 2, S(262), 30, (255, 230, 120), key="black", align="center", valign="middle")
        self.text(screen, "BALL", W / 2, S(320), 28, (250, 200, 60), key="stencil", align="center", valign="middle")


# ============================================================================ Super Bubble Pop
class SuperBubblePopScene(GameScene):
    """Super Bubble Pop as in the game: the magenta swirl, the white board seen at an angle where the bubbles fall, our
    little robot of our own at the bottom shoots its bubble up a column, three of a colour burst.
    / Le tourbillon magenta, le plateau blanc vu de biais, notre petit robot tire ses bulles, comme dans le jeu."""
    THEME = "sbp_swirl"
    STATIC = True
    SHADE = (60, 0)
    COLS, ROWS = 8, 8

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.cells = {}
        self.col = 3.0
        self.target = 3
        self.next_t = 0.0
        self.shot = None
        self.popped = 0                                   # (tests)
        for _ in range(14):
            self.cells[(self.rng.randrange(self.COLS), self.rng.randrange(3))] = self.rng.randrange(4)

    def corner(self, u, v):
        S, W = self.S, self.W
        top, bot = S(120), S(380)
        half = S(250) + (S(380) - S(250)) * v
        return W / 2 + (u - 0.5) * 2 * half, top + (bot - top) * v

    def cell_xy(self, c, r):
        return self.corner((c + 0.5) / self.COLS, (r + 0.5) / self.ROWS)

    def bubble(self, k, size):
        S = self.S
        return self.img(("sbpbub", k, size), S(size), S(size), blob_draw(k), ss=2)

    def update(self, vals, now):
        dt, rng = self.dt, self.rng
        self.col += _clamp(self.target - self.col, -6 * dt, 6 * dt)
        if now >= self.next_t:                                           # a bubble falls on the board, the robot aims
            self.next_t = now + rng.uniform(0.8, 1.6)
            c = rng.randrange(self.COLS)
            r = 0
            while (c, r) in self.cells and r < self.ROWS - 2:
                r += 1
            self.cells[(c, r)] = rng.randrange(4)
            self.target = rng.randrange(self.COLS)
            if abs(self.target - self.col) < 0.5 and self.shot is None:
                self.shoot(now)
        if self.shot is None and abs(self.target - self.col) < 0.05 and rng.random() < dt * 2:
            self.shoot(now)
        if self.shot is not None and now >= self.shot["t1"]:
            c, r, k = self.shot["c"], self.shot["r"], self.shot["k"]
            self.cells[(c, r)] = k
            self.shot = None
            self.match(c, r)
        if len(self.cells) > self.COLS * (self.ROWS - 2):
            self.cells = {}
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0] and self.cells:
            c, r = rng.choice(list(self.cells))
            self.match(c, r, force=True)

    def shoot(self, now):
        c = int(round(self.target))
        r = self.ROWS - 2
        while r > 0 and (c, r - 1) not in self.cells:
            r -= 1
        if (c, r) in self.cells:
            return
        k = self.cells.get((c, r - 1), self.rng.randrange(4)) if self.rng.random() < 0.6 else self.rng.randrange(4)
        self.shot = {"c": c, "r": r, "k": k, "t0": now, "t1": now + 0.25}

    def match(self, c, r, force=False):
        k = self.cells.get((c, r))
        if k is None:
            return
        todo, seen = [(c, r)], set()
        while todo:
            cc, rr = todo.pop()
            if (cc, rr) in seen or self.cells.get((cc, rr)) != k:
                continue
            seen.add((cc, rr))
            todo += [(cc + 1, rr), (cc - 1, rr), (cc, rr + 1), (cc, rr - 1)]
        if len(seen) >= 3 or force:
            for cc, rr in seen:
                x, y = self.cell_xy(cc, rr)
                del self.cells[(cc, rr)]
                self.fx.sparks(x, y, 8, POP_COLORS[k], (200, 450), (0, 360), (0.2, 0.4), 300, "front", 4, 12)
            self.popped += len(seen)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        pts = [self.corner(0, 0), self.corner(1, 0), self.corner(1, 1), self.corner(0, 1)]
        pg.draw.polygon(screen, (236, 236, 244), [(int(x), int(y)) for x, y in pts])
        for i in range(self.COLS + 1):
            a, b = self.corner(i / self.COLS, 0), self.corner(i / self.COLS, 1)
            pg.draw.line(screen, (190, 190, 206), (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), max(1, S(2)))
        for j in range(self.ROWS + 1):
            a, b = self.corner(0, j / self.ROWS), self.corner(1, j / self.ROWS)
            pg.draw.line(screen, (190, 190, 206), (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), max(1, S(2)))
        for (c, r), k in self.cells.items():
            x, y = self.cell_xy(c, r)
            img = self.bubble(k, 40 + r * 2)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() * 0.75)))
        bx, by = self.corner((self.col + 0.5) / self.COLS, 1)
        if self.shot is not None:
            k = _clamp((self.fx.now - self.shot["t0"]) / 0.25)
            tx, ty = self.cell_xy(self.shot["c"], self.shot["r"])
            img = self.bubble(self.shot["k"], 40)
            screen.blit(img, (int(bx + (tx - bx) * k - img.get_width() / 2), int(by + (ty - by) * k - img.get_height() / 2)))
        robot = self.img("sbprobot", S(70), S(80), robot_draw, ss=2)
        screen.blit(robot, (int(bx - robot.get_width() / 2), int(by + S(4))))
        self.hd.draw_logo(screen, logo, W / 2, S(4), S(420), S(80), now)
        self.pill(screen, S(40), S(20), S(300), S(56), 170, radius=28)
        v = _n(vals.get("score"))
        self.hd.put_number(screen, f"{int(v or 0):07d}", "black", S(36), (120, 160, 255), S(190), S(48), "center", "middle")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


def robot_draw(d, W, H):
    """Our little white and red robot that shoots the bubbles. / Notre petit robot blanc et rouge qui tire les bulles."""
    dark = DARKLINE
    d.rounded_rectangle([W * 0.2, H * 0.3, W * 0.8, H * 0.8], radius=W * 0.1, fill=(240, 240, 248, 255), outline=dark, width=max(1, int(W * 0.04)))
    d.rectangle([W * 0.3, H * 0.44, W * 0.7, H * 0.56], fill=(220, 40, 50, 255))
    d.ellipse([W * 0.3, H * 0.02, W * 0.7, H * 0.34], fill=(240, 240, 248, 255), outline=dark)
    d.ellipse([W * 0.42, H * 0.12, W * 0.58, H * 0.24], fill=(60, 140, 240, 255))
    for x in (0.26, 0.6):
        d.rectangle([W * x, H * 0.8, W * (x + 0.14), H * 0.98], fill=(220, 40, 50, 255), outline=dark)


# ============================================================================ Zupapa!
def zupa_draw(frame):
    """Our little round green hero with big eyes and red gloves, facing right; frame 2 punches.
    / Notre petit héros rond et vert, grands yeux, gants rouges ; l'image 2 frappe."""
    def fn(d, W, H):
        dark = DARKLINE
        u = H
        st = (0.06, -0.06) if frame == 0 else (-0.06, 0.06)
        for i, dx in enumerate(st):
            d.ellipse([W * (0.34 + dx) - 0.08 * u + i * 0.2 * u, H * 0.84, W * (0.34 + dx) + 0.08 * u + i * 0.2 * u, H * 0.98], fill=(240, 160, 40, 255),
                      outline=dark)
        d.ellipse([W * 0.14, H * 0.18, W * 0.86, H * 0.9], fill=(80, 200, 90, 255), outline=dark, width=max(1, int(W * 0.04)))
        d.ellipse([W * 0.26, H * 0.56, W * 0.74, H * 0.86], fill=(220, 250, 200, 255))
        for ex in (0.42, 0.64):
            d.ellipse([W * (ex - 0.1), H * 0.26, W * (ex + 0.1), H * 0.5], fill=(255, 255, 255, 255), outline=dark)
            d.ellipse([W * (ex - 0.02), H * 0.32, W * (ex + 0.06), H * 0.44], fill=dark)
        gx = 0.98 if frame == 2 else 0.84
        d.ellipse([W * (gx - 0.14), H * 0.5, W * gx, H * 0.7], fill=(230, 40, 40, 255), outline=dark)
        d.polygon([(W * 0.46, H * 0.18), (W * 0.5, H * 0.02), (W * 0.58, H * 0.2)], fill=(240, 220, 60, 255), outline=dark)
    return fn


def goblin_draw(kind, frame):
    """A round monster of the cave, facing left: a purple one with teeth, or a bony grey one.
    / Un monstre rond de la grotte, face à gauche : violet à dents, ou gris osseux."""
    def fn(d, W, H):
        dark = DARKLINE
        body = (150, 70, 170) if kind == 0 else (200, 200, 190)
        st = 0.05 if frame else -0.05
        d.ellipse([W * (0.2 + st), H * 0.84, W * (0.4 + st), H * 0.98], fill=_mixc(body, (0, 0, 0), 0.3))
        d.ellipse([W * (0.6 - st), H * 0.84, W * (0.8 - st), H * 0.98], fill=_mixc(body, (0, 0, 0), 0.3))
        d.ellipse([W * 0.1, H * 0.16, W * 0.9, H * 0.9], fill=body + (255,), outline=dark, width=max(1, int(W * 0.04)))
        for ex in (0.3, 0.52):
            d.ellipse([W * (ex - 0.08), H * 0.3, W * (ex + 0.08), H * 0.48], fill=(255, 240, 80, 255) if kind == 0 else (40, 40, 50, 255), outline=dark)
        d.rectangle([W * 0.2, H * 0.6, W * 0.62, H * 0.7], fill=(255, 255, 255, 255), outline=dark)
        for k in range(4):
            d.line([(W * (0.24 + k * 0.1), H * 0.6), (W * (0.24 + k * 0.1), H * 0.7)], fill=dark, width=1)
        if kind == 0:
            d.polygon([(W * 0.3, H * 0.2), (W * 0.36, H * 0.0), (W * 0.44, H * 0.18)], fill=(250, 200, 60, 255), outline=dark)
    return fn


class ZupapaScene(GameScene):
    """Zupapa! as in the game: the blue cave and its old statues, the platforms striped orange and blue, our little round
    hero of our own walks the platforms and boots the monsters, who fly off in a shower of stars. P1, the score and the
    lives at the top. / La grotte bleue, les plateformes rayées, notre petit héros rond chasse les monstres."""
    THEME = "zp_cave"
    STATIC = True
    SHADE = (60, 0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.hero = {"row": 3, "x": self.W * 0.3, "dir": 1, "punch": -99.0, "jump": None}
        self.foes = []
        self.flying = []
        self.next_foe = 0.0
        self.boots = 0                                    # (tests)
        self.warm += [(self.zimg, (f,)) for f in range(3)] + [(self.gimg, (k, f)) for k in range(2) for f in range(2)]

    def zimg(self, frame):
        S = self.S
        return self.img(("zupa", frame), S(84), S(84), zupa_draw(frame), ss=2)

    def gimg(self, kind, frame):
        S = self.S
        return self.img(("zgob", kind, frame), S(78), S(78), goblin_draw(kind, frame), ss=2)

    def row_y(self, row):
        return self.S(ZP_ROWS[row][0])

    def seg_of(self, row, x):
        for x0, x1 in ZP_ROWS[row][1]:
            if self.S(x0) <= x <= self.S(x1):
                return self.S(x0), self.S(x1)
        return None

    def restart(self, vals, now):
        self.foes = []
        self.next_foe = now + 0.5

    def update(self, vals, now):
        S, dt, rng = self.S, self.dt, self.rng
        if now >= self.next_foe and len(self.foes) < 7:
            self.next_foe = now + rng.uniform(0.5, 1.1)
            row = rng.randrange(len(ZP_ROWS))
            x0, x1 = rng.choice(ZP_ROWS[row][1])
            self.foes.append({"row": row, "x": S(rng.uniform(x0 + 20, x1 - 20)), "dir": rng.choice((-1, 1)), "kind": rng.randrange(2),
                              "ph": rng.uniform(0, 6)})
        for f in self.foes:                                              # the monsters walk their platform
            seg = self.seg_of(f["row"], f["x"])
            f["x"] += f["dir"] * S(90) * dt
            if seg and not (seg[0] + S(20) < f["x"] < seg[1] - S(20)):
                f["dir"] = -f["dir"]
                f["x"] = _clamp(f["x"], seg[0] + S(20), seg[1] - S(20))
        h = self.hero
        if h["jump"] is not None:                                        # a jump to another platform
            j = h["jump"]
            k = (now - j["t0"]) / 0.6
            if k >= 1:
                h["row"], h["x"], h["jump"] = j["row"], j["x"], None
        else:
            same = [f for f in self.foes if f["row"] == h["row"]]
            if same:
                tgt = min(same, key=lambda f: abs(f["x"] - h["x"]))
                h["dir"] = 1 if tgt["x"] > h["x"] else -1
                if abs(tgt["x"] - h["x"]) < S(90):
                    self.boot(tgt, now)
                else:
                    h["x"] += h["dir"] * S(160) * dt
            elif rng.random() < dt * 0.8 and self.foes:                   # nobody here: jump to a monster's platform
                tgt = rng.choice(self.foes)
                seg = self.seg_of(tgt["row"], tgt["x"]) or (tgt["x"] - S(50), tgt["x"] + S(50))
                h["jump"] = {"t0": now, "row": tgt["row"], "x": _clamp(tgt["x"] - S(120) * rng.choice((-1, 1)), seg[0] + S(30), seg[1] - S(30)),
                             "x0": h["x"], "y0": self.row_y(h["row"])}
            seg = self.seg_of(h["row"], h["x"])
            if seg:
                h["x"] = _clamp(h["x"], seg[0] + S(30), seg[1] - S(30))
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0] and self.foes:
            self.boot(min(self.foes, key=lambda f: abs(f["x"] - h["x"]) + abs(f["row"] - h["row"]) * S(300)), now)
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.popup(tr("-1 VIE", "-1 LIFE"), h["x"], self.row_y(h["row"]) - S(120), (255, 90, 70), 36)

    def boot(self, f, now):
        """A kick: the monster flies off in a shower of stars. / Un coup de pied : le monstre s'envole en étoiles."""
        if f not in self.foes:
            return
        self.foes.remove(f)
        self.boots += 1
        h = self.hero
        h["punch"] = now
        d = 1 if f["x"] >= h["x"] else -1
        self.flying.append({"x": f["x"], "y": self.row_y(f["row"]) - self.S(40), "vx": d * self.S(700), "vy": -self.S(600), "kind": f["kind"],
                            "t0": now})
        self.fx.sparks(f["x"], self.row_y(f["row"]) - self.S(40), 14, (255, 230, 80), (200, 500), (0, 360), (0.3, 0.6), 300, "front", 5, 10)
        self.popup("100", f["x"], self.row_y(f["row"]) - self.S(90), GOLD, 30)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, dt = self.S, self.W, self.dt
        for f in self.foes:
            img = self.gimg(f["kind"], int(now * 5 + f["ph"]) % 2)
            y = self.row_y(f["row"])
            screen.blit(img, (int(f["x"] - img.get_width() / 2), int(y - img.get_height())))
        keep = []
        for f in self.flying:                                            # booted monsters spin away
            f["vy"] += S(1400) * dt
            f["x"] += f["vx"] * dt
            f["y"] += f["vy"] * dt
            if f["y"] < self.H + S(80):
                keep.append(f)
                img = self.rotated(("zspin", f["kind"]), self.gimg(f["kind"], 0), (now - f["t0"]) * 720, 12)
                screen.blit(img, (int(f["x"] - img.get_width() / 2), int(f["y"] - img.get_height() / 2)))
        self.flying = keep
        h = self.hero
        if self.p1_in(vals):
            if h["jump"] is not None:
                j = h["jump"]
                k = _clamp((now - j["t0"]) / 0.6)
                x = j["x0"] + (j["x"] - j["x0"]) * k
                y = j["y0"] + (self.row_y(j["row"]) - j["y0"]) * k - math.sin(k * math.pi) * S(120)
            else:
                x, y = h["x"], self.row_y(h["row"])
            frame = 2 if now - h["punch"] < 0.2 else int(now * 6) % 2
            img = self.zimg(frame)
            if h["dir"] < 0:
                img = self.img(("zupaL", frame), S(84), S(84), zupa_draw(frame), ss=2, flip=True)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height())))
        self.hd.draw_logo(screen, logo, W / 2, S(4), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(420), S(84), 160, radius=14)
        self.text(screen, "P1", S(28), S(30), 28, (250, 120, 160), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            self.hd._score(screen, eng, "score", S(410), S(10), "right", S(40))
        lives = _n(vals.get("lives"))
        if lives is not None:
            screen.blit(self.img("zupaicon", S(30), S(30), zupa_draw(0), ss=2), (S(160), S(54)))
            self.text(screen, f"x{int(lives)}", S(196), S(70), 26, WHITE, key="black", valign="middle")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


# ============================================================================ Neo Mr. Do!
def digger_draw(d, W, H):
    """Our little digger of our own: a yellow helmet and its lamp, a red suit, a shovel. / Notre petit mineur à nous."""
    dark = DARKLINE
    d.ellipse([W * 0.2, H * 0.4, W * 0.8, H * 0.95], fill=(220, 50, 50, 255), outline=dark, width=max(1, int(W * 0.05)))
    d.ellipse([W * 0.24, H * 0.12, W * 0.76, H * 0.6], fill=(250, 210, 170, 255), outline=dark)
    d.chord([W * 0.2, H * 0.04, W * 0.8, H * 0.5], 180, 360, fill=(250, 210, 40, 255), outline=dark)
    d.ellipse([W * 0.44, H * 0.12, W * 0.56, H * 0.24], fill=(255, 255, 200, 255), outline=dark)
    for ex in (0.4, 0.6):
        d.ellipse([W * (ex - 0.04), H * 0.34, W * (ex + 0.04), H * 0.42], fill=dark)
    d.line([(W * 0.8, H * 0.3), (W * 0.92, H * 0.9)], fill=(140, 100, 60, 255), width=max(2, int(W * 0.06)))
    d.polygon([(W * 0.84, H * 0.84), (W * 1.0, H * 0.84), (W * 0.96, H * 1.0), (W * 0.86, H * 1.0)], fill=(170, 170, 180, 255), outline=dark)


def cherry_draw(d, W, H):
    dark = DARKLINE
    d.line([(W * 0.3, H * 0.6), (W * 0.55, H * 0.1)], fill=(60, 120, 40, 255), width=max(1, int(W * 0.06)))
    d.line([(W * 0.72, H * 0.6), (W * 0.55, H * 0.1)], fill=(60, 120, 40, 255), width=max(1, int(W * 0.06)))
    for x in (0.28, 0.72):
        d.ellipse([W * (x - 0.22), H * 0.5, W * (x + 0.22), H * 0.94], fill=(220, 30, 50, 255), outline=dark)
        d.ellipse([W * (x - 0.12), H * 0.58, W * (x - 0.02), H * 0.68], fill=(255, 200, 200, 255))


def creep_draw(d, W, H):
    """A little blue horned monster of the tunnels. / Un petit monstre bleu à cornes des tunnels."""
    dark = DARKLINE
    d.ellipse([W * 0.1, H * 0.2, W * 0.9, H * 0.95], fill=(70, 90, 210, 255), outline=dark, width=max(1, int(W * 0.05)))
    for x in (0.22, 0.66):
        d.polygon([(W * x, H * 0.3), (W * (x + 0.06), H * 0.02), (W * (x + 0.14), H * 0.28)], fill=(250, 250, 250, 255), outline=dark)
    for ex in (0.38, 0.62):
        d.ellipse([W * (ex - 0.1), H * 0.36, W * (ex + 0.1), H * 0.58], fill=(255, 255, 255, 255), outline=dark)
        d.ellipse([W * (ex - 0.04), H * 0.42, W * (ex + 0.04), H * 0.52], fill=dark)
    d.arc([W * 0.34, H * 0.58, W * 0.66, H * 0.8], 20, 160, fill=dark, width=max(1, int(W * 0.04)))


class NeoMrDoScene(GameScene):
    """Neo Mr. Do! as in the game: the field of coloured tiles and their toys and tools, our little digger of our own
    digs his tunnels, picks the cherries, the monsters follow him in the tunnels and fall to his power ball. 1P- and
    the score, the lives, EXTRA at the top. / Le champ de cases colorées, notre petit mineur creuse et ramasse les cerises."""
    THEME = "nmd_field"
    STATIC = True
    SHADE = (60, 0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        x0, y0, c, cols, rows = NMD
        self.cols, self.rows = cols, rows
        self.dug = {(k, rows // 2) for k in range(cols)} | {(cols // 4, r) for r in range(rows)} | {(3 * cols // 4, r) for r in range(rows)}
        self.pos = [cols // 2, rows // 2]
        self.at = [float(cols // 2), float(rows // 2)]
        self.goal = None
        self.cherries = set()
        self.creeps = []
        self.next_creep = 0.0
        self.extra = 0
        self.ball_t = 0.0
        self.picked = 0                                   # (tests)
        self.kills = 0
        self.plant()

    def cell(self, c, r):
        S = self.S
        x0, y0, cs, _, _ = NMD
        return S(x0) + (c + 0.5) * S(cs), S(y0) + (r + 0.5) * S(cs)

    def plant(self):
        rng = self.rng
        for _ in range(3):
            c, r = rng.randrange(self.cols - 4), rng.randrange(self.rows - 2)
            for dc in range(4):
                for dr in range(2):
                    if (c + dc, r + dr) not in self.dug:
                        self.cherries.add((c + dc, r + dr))

    def update(self, vals, now):
        dt, rng = self.dt, self.rng
        if self.goal is None or tuple(self.pos) == self.goal:            # the digger picks a goal: cherries, or anywhere
            self.goal = rng.choice(sorted(self.cherries)) if self.cherries and rng.random() < 0.8 else (rng.randrange(self.cols), rng.randrange(self.rows))
        if abs(self.at[0] - self.pos[0]) < 0.05 and abs(self.at[1] - self.pos[1]) < 0.05:
            gx, gy = self.goal
            if gx != self.pos[0]:
                self.pos[0] += 1 if gx > self.pos[0] else -1
            elif gy != self.pos[1]:
                self.pos[1] += 1 if gy > self.pos[1] else -1
            here = tuple(self.pos)
            self.dug.add(here)
            if here in self.cherries:
                self.cherries.discard(here)
                self.picked += 1
                x, y = self.cell(*here)
                self.fx.sparks(x, y, 8, (255, 80, 100), (100, 300), (0, 360), (0.2, 0.4), 0, "front", 3, 8)
                if not self.cherries:
                    self.plant()
        for i in range(2):
            self.at[i] += _clamp(self.pos[i] - self.at[i], -5 * dt, 5 * dt)
        if now >= self.next_creep and len(self.creeps) < 5:              # the monsters come out of their nest
            self.next_creep = now + rng.uniform(1.2, 2.5)
            self.creeps.append({"at": [0.0, float(self.rows // 2)], "pos": [0, self.rows // 2]})
        for m in self.creeps:                                            # they follow the tunnels toward the digger
            if abs(m["at"][0] - m["pos"][0]) < 0.05 and abs(m["at"][1] - m["pos"][1]) < 0.05:
                opts = [(m["pos"][0] + dc, m["pos"][1] + dr) for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (m["pos"][0] + dc, m["pos"][1] + dr) in self.dug]
                if opts:
                    nxt = min(opts, key=lambda p: abs(p[0] - self.pos[0]) + abs(p[1] - self.pos[1]) + rng.uniform(0, 3))
                    m["pos"] = list(nxt)
            for i in range(2):
                m["at"][i] += _clamp(m["pos"][i] - m["at"][i], -2.6 * dt, 2.6 * dt)
        ch = self.changed(vals, "score")
        near = [m for m in self.creeps if abs(m["at"][0] - self.at[0]) + abs(m["at"][1] - self.at[1]) < 8]
        if ch and ch[1] > ch[0] and near and now >= self.ball_t:         # the power ball takes the nearest monster
            self.ball_t = now + 2.0
            m = min(near, key=lambda m: abs(m["at"][0] - self.at[0]) + abs(m["at"][1] - self.at[1]))
            self.creeps.remove(m)
            self.kills += 1
            self.extra = min(5, self.extra + 1)
            x0, y0 = self.cell(*self.at)
            x1, y1 = self.cell(*m["at"])
            self.fx.tracer(x0, y0, x1, y1, 1800, (255, 240, 120), 12, 40, "front", False)
            self.fx.later(0.15, self.fx.sparks, x1, y1, 16, (120, 160, 255), (200, 500), (0, 360), (0.3, 0.5), 200, "front", 4, 12)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        cs = S(NMD[2])
        for c, r in self.dug:                                            # the tunnels / les tunnels
            x, y = self.cell(c, r)
            pg.draw.rect(screen, (24, 20, 70), (int(x - cs / 2), int(y - cs / 2), int(cs) + 1, int(cs) + 1))
        ch = self.img("nmdcherry", S(30), S(30), cherry_draw, ss=2)
        for c, r in self.cherries:
            x, y = self.cell(c, r)
            screen.blit(ch, (int(x - ch.get_width() / 2), int(y - ch.get_height() / 2)))
        cr = self.img("nmdcreep", S(36), S(36), creep_draw, ss=2)
        for m in self.creeps:
            x, y = self.cell(*m["at"])
            screen.blit(cr, (int(x - cr.get_width() / 2), int(y - cr.get_height() / 2)))
        if self.p1_in(vals):
            dg = self.img("nmddigger", S(38), S(38), digger_draw, ss=2)
            x, y = self.cell(*self.at)
            screen.blit(dg, (int(x - dg.get_width() / 2), int(y - dg.get_height() / 2)))
        self.hd.draw_logo(screen, logo, W / 2, S(4), S(360), S(64), now)
        self.pill(screen, S(12), S(6), S(380), S(80), 170, radius=14)
        self.text(screen, "1P-", S(28), S(28), 26, WHITE, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            self.hd._score(screen, eng, "score", S(370), S(8), "right", S(36))
        lives = _n(vals.get("lives"))
        if lives is not None:
            screen.blit(self.img("nmdlife", S(26), S(26), digger_draw, ss=2), (S(28), S(50)))
            self.text(screen, f"x{int(lives)}", S(60), S(64), 24, WHITE, key="black", valign="middle")
        for i, ch_ in enumerate("EXTRA"):                                # EXTRA, lit letter by letter
            on = i < self.extra
            x = W / 2 + S(220) + i * S(44)
            pg.draw.circle(screen, (240, 80, 160) if on else (90, 60, 110), (int(x), S(40)), S(20))
            self.text(screen, ch_, x, S(40), 24, WHITE if on else (170, 150, 190), key="black", align="center", valign="middle", glow=0)
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


SCENES = {"puzzldpr": PuzzleDePonRScene, "panicbom": PanicBomberScene, "popbounc": PopBounceScene, "sbp": SuperBubblePopScene,
          "spinmast": SpinMasterScene, "ganryu": GanryuScene, "zupapa": ZupapaScene, "neomrdo": NeoMrDoScene, "ssideki": SuperSidekicksScene,
          "ssideki2": SuperSidekicks2Scene}
