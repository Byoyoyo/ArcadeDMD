"""HD scenes of the sixth batch of Neo Geo games done one by one (1.22), each drawn after screenshots of its game.
Each game has its own animated backdrop and reacts to the values read in its memory. The characters, the monsters
and the machines are creations of the program in the spirit of the games.

Scènes HD du sixième lot de jeux Neo Geo faits un par un (1.22), chacune dessinée d'après des captures de son jeu.
Les personnages, les monstres et les engins sont des créations du programme dans l'esprit des jeux.
"""

import math

from .hd_games import CREAM, GOLD, WHITE, PuzzleBobbleScene, _clamp, _n, draw_img
from .hd_games2 import DROP_RGB, MagicalDropScene
from .hd_games3 import _capsule
from .hd_games5 import BrawlerScene, CyberLipScene, ShockTroopers2Scene, _mixc, fighter_draw
from .hd_themes6 import BJ_FLOOR, NCM_ROAD                         # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr


def portrait_draw(skin, hair, band=None, hood=None, bg=(60, 90, 160)):
    """A face of our own for the corner of the screen: hair or a hood, a headband. / Un visage à nous pour le coin de l'écran."""
    def fn(d, W, H):
        dark = (24, 20, 20, 255)
        d.rectangle([0, 0, W - 1, H - 1], fill=bg + (255,))
        d.ellipse([W * 0.18, H * 0.16, W * 0.82, H * 0.96], fill=skin + (255,), outline=dark, width=max(1, int(W * 0.03)))
        if hood:
            d.chord([W * 0.12, H * 0.02, W * 0.88, H * 1.1], 180, 360, fill=hood + (255,))
            d.rectangle([W * 0.12, H * 0.62, W * 0.88, H * 0.98], fill=hood + (255,))
            d.rectangle([W * 0.2, H * 0.44, W * 0.8, H * 0.6], fill=skin + (255,))
        else:
            d.chord([W * 0.14, H * 0.04, W * 0.86, H * 0.66], 180, 360, fill=hair + (255,))
        if band:
            d.rectangle([W * 0.16, H * 0.3, W * 0.84, H * 0.38], fill=band + (255,))
        for ex in (0.36, 0.64):
            d.ellipse([W * (ex - 0.06), H * 0.48, W * (ex + 0.06), H * 0.58], fill=dark)
        if not hood:
            d.line([(W * 0.42, H * 0.78), (W * 0.58, H * 0.78)], fill=dark, width=max(1, int(W * 0.03)))
        d.rectangle([0, 0, W - 1, H - 1], outline=(250, 250, 250, 255), width=max(2, int(W * 0.05)))
    return fn


# ============================================================================ Mutation Nation
class MutationNationScene(BrawlerScene):
    """Mutation Nation as in the game: our street fighter in the ruined city, the mutants come from both sides. 1P and
    the score, the LIFE gauge in rainbow segments, B and the attack items at the top left.
    / Notre combattant dans la ville en ruine, les mutants arrivent des deux côtés, comme dans le jeu."""
    THEME = "mn_city"
    HERO = ("jacket", (40, 40, 48), (60, 90, 170), (226, 176, 136), (200, 40, 40))
    FOES = (("mutant", (170, 40, 60), (120, 60, 140), (196, 150, 220), (90, 40, 110)), ("mutant", (60, 120, 70), (70, 60, 50), (150, 200, 120),
                                                                                          (40, 70, 30)),
            ("thug", (120, 60, 140), (60, 60, 70), (200, 160, 120), (30, 30, 34)))
    ENERGY_MAX = 64

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "bombs")
        if ch and ch[1] < ch[0]:                                       # an attack item: the screen is swept
            S, fx = self.S, self.fx
            h = self.hero
            fx.flash((255, 230, 160), 0.2, 0.3)
            for i in range(8):
                fx.later(i * 0.04, fx.glow, h["x"] + math.cos(i * 0.8) * S(200), self.ground(h["z"]) - S(140) + math.sin(i * 0.8) * S(80), 30, 140,
                         (255, 220, 120), 0.4, "front", 1.0, 0.0)
            for f in self.foes:
                if f["hp"] > 0 and abs(f["x"] - h["x"]) < self.W * 0.45:
                    f["hp"] = 0
                    f["down"] = now
                    f["vx"] = (1 if f["x"] > h["x"] else -1) * S(500)
                    self.knocked += 1
            self.popup(tr("ATTAQUE !", "ATTACK!"), h["x"], self.ground(h["z"]) - S(300), GOLD, 42)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score, LIFE in rainbow segments, B and the attack items. / LIFE en arc-en-ciel."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(560), S(110), 160, radius=14)
        self.text(screen, "1P", S(30), S(30), 28, (255, 230, 120), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(380), S(10), "right", S(40))
        e = _n(vals.get("energy"))
        self.text(screen, "LIFE", S(30), S(70), 22, (120, 200, 255), key="black", valign="middle")
        if e is not None:
            cols = ((230, 40, 40), (250, 120, 30), (250, 210, 40), (90, 210, 60), (50, 160, 250), (120, 90, 240))
            n = 16
            on = int(round(_clamp(e / 64.0) * n))
            for i in range(n):
                c = cols[i * len(cols) // n] if i < on else (50, 50, 60)
                pg.draw.rect(screen, c, (S(96) + i * S(16), S(60), S(13), S(22)))
        b = _n(vals.get("bombs"))
        if b is not None:
            pg.draw.rect(screen, (220, 40, 40), (S(390), S(54), S(34), S(34)), border_radius=S(4))
            pg.draw.rect(screen, (250, 250, 250), (S(390), S(54), S(34), S(34)), max(1, S(2)), border_radius=S(4))
            self.text(screen, "B", S(407), S(71), 24, WHITE, key="black", align="center", valign="middle", glow=0)
            self.text(screen, f"{int(b)}", S(436), S(71), 28, (255, 230, 120), key="black", valign="middle")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


# ============================================================================ Sengoku, Sengoku 2
SG_SPHERES = {1: ("RED", (240, 60, 50)), 2: ("BLUE", (60, 120, 250)), 3: ("PURPLE", (170, 80, 230)), 4: ("YELLOW", (250, 210, 50))}
SG2_SPHERES = {1: ("BLUE", (60, 120, 250)), 2: ("PINK", (250, 110, 190)), 3: ("YELLOW", (250, 210, 50))}


class SengokuScene(BrawlerScene):
    """Sengoku as in the game: our swordsman at the end of the world, a blood-red sunset, a castle floating in the sky,
    the armoured ghost warriors come from both sides. SCORE- and the score, a face of our own, the lives and the six
    LIFE boxes, as in the game. / Notre sabreur sous un coucher de soleil rouge, les guerriers fantômes en armure."""
    THEME = "sg1_field"
    HERO = ("jacket", (200, 40, 40), (240, 200, 40), (226, 176, 136), (40, 30, 26), "sword")
    FOES = (("samurai", (150, 156, 170), (80, 84, 96), (210, 190, 170), (60, 60, 70), "sword"),
            ("ninja", (90, 60, 120), (60, 40, 90), (210, 180, 150), (0, 0, 0), "sword"))
    ENERGY_MAX = 6
    SPHERES = SG_SPHERES
    FACE = ((232, 184, 144), (40, 30, 26), (220, 40, 40))
    LABEL = "SCORE-"

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "weapon")
        if ch and ch[1]:                                               # a sphere taken: the blade glows in its colour
            name, col = self.SPHERES.get(int(ch[1]), ("POWER", GOLD))
            h = self.hero
            self.popup(name + " !", h["x"], self.ground(h["z"]) - self.S(300), col, 40)
            self.fx.glow(h["x"], self.ground(h["z"]) - self.S(140), 30, 160, col, 0.5, "front", 1.0, 0.0)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: SCORE- (1P-) and the score, the face, x and the lives, LIFE and its six boxes.
        / Comme dans le jeu : le score, le visage, les vies, LIFE et ses six cases."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(520), S(116), 160, radius=14)
        self.text(screen, self.LABEL, S(28), S(28), 26, WHITE, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(510), S(10), "right", S(40))
        skin, hair, band = self.FACE
        screen.blit(self.img(("sgface", self.THEME), S(60), S(60), portrait_draw(skin, hair, band, bg=(40, 140, 80)), ss=2), (S(24), S(54)))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.text(screen, f"x{int(lives)}", S(96), S(84), 30, WHITE, key="black", valign="middle")
        self.text(screen, "LIFE", S(160), S(66), 22, (255, 230, 120), key="black", valign="middle")
        e = _n(vals.get("energy"))
        if e is not None:
            for i in range(6):
                on = i < int(e)
                c = ((240, 60, 40) if i < 2 else (250, 170, 40)) if on else (40, 30, 30)
                pg.draw.rect(screen, c, (S(160) + i * S(34), S(84), S(28), S(24)))
                pg.draw.rect(screen, (250, 240, 220), (S(160) + i * S(34), S(84), S(28), S(24)), max(1, S(2)))
        w = _n(vals.get("weapon"))
        if w:
            name, col = self.SPHERES.get(int(w), ("POWER", GOLD))
            pg.draw.circle(screen, col, (S(400), S(96)), S(14))
            self.text(screen, name, S(422), S(96), 20, col, key="black", valign="middle")
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, colw, align="right")


class Sengoku2Scene(SengokuScene):
    """Sengoku 2 as in the game: under the great wooden bridge at dusk, then the castle walls, our swordsman fights the
    dark armoured warriors. 1P- and the score, the face, the lives and the LIFE boxes.
    / Sous le grand pont de bois au crépuscule, notre sabreur affronte les guerriers en armure sombre."""
    THEME = "sg2_bridge"
    HERO = ("jacket", (150, 80, 190), (240, 140, 40), (226, 176, 136), (110, 50, 30), "sword")
    FOES = (("samurai", (60, 64, 76), (50, 50, 60), (200, 170, 150), (40, 40, 50), "sword"),
            ("samurai", (170, 90, 50), (90, 60, 40), (200, 170, 150), (120, 40, 30), "sword"),
            ("ninja", (40, 40, 52), (30, 30, 40), (210, 180, 150), (0, 0, 0), "sword"))
    SPHERES = SG2_SPHERES
    FACE = ((232, 184, 144), (110, 50, 30), (210, 40, 120))
    LABEL = "1P-"


# ============================================================================ Ninja Combat
NC_NAMES = ("JOE", "HAYABUSA", "MUSASHI", "GEMBU", "SHOMA")


class NinjaCombatScene(BrawlerScene):
    """Ninja Combat as in the game: a park at night, a gate of gold and blue pillars, our red ninja faces the black,
    red and purple ninjas. At the bottom as in the game a face of our own, POW and LIFE, TIME in minutes and seconds,
    the lives. / Un parc la nuit, notre ninja rouge face aux ninjas noirs, rouges et violets, comme dans le jeu."""
    THEME = "nc_park"
    HERO = ("ninja", (210, 40, 40), (190, 30, 30), (226, 176, 136), (0, 0, 0))
    FOES = (("ninja", (40, 40, 48), (30, 30, 36), (210, 180, 150), (0, 0, 0), "sword"), ("ninja", (96, 100, 110), (70, 74, 84), (210, 180, 150),
                                                                                          (0, 0, 0), "sword"),
            ("ninja", (120, 100, 160), (90, 70, 130), (210, 180, 150), (0, 0, 0), "sword"))
    ENERGY_MAX = 32

    def status(self, screen, eng, vals, logo, now):
        """As in the game, at the bottom: the face, POW and LIFE, TIME, the lives; 1P and the score at the top.
        / Comme dans le jeu, en bas : le visage, POW et LIFE, TIME, les vies ; 1P et le score en haut."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(420), S(58), 160, radius=14)
        self.text(screen, "1P", S(30), S(34), 28, (240, 60, 50), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(410), S(12), "right", S(40))
        bar = self.imgs.get("ncbar")
        if bar is None:
            bar = self.imgs["ncbar"] = pg.Surface((S(640), S(92)), pg.SRCALPHA)
            bar.fill((0, 0, 0, 200))
        y0 = H - S(96)
        screen.blit(bar, (S(10), y0))
        screen.blit(self.img("ncface", S(76), S(76), portrait_draw((226, 176, 136), (0, 0, 0), hood=(200, 40, 40), bg=(40, 50, 120)), ss=2),
                    (S(20), y0 + S(8)))
        self.text(screen, "POW", S(110), y0 + S(20), 22, (240, 80, 70), key="black", valign="middle")
        p = _n(vals.get("power"))
        self.bar(screen, S(180), y0 + S(10), S(200), S(20), (p or 0) / 2.0, (250, 200, 60))
        self.text(screen, "LIFE", S(110), y0 + S(48), 22, (240, 80, 70), key="black", valign="middle")
        e = _n(vals.get("energy"))
        if e is not None:
            self.bar(screen, S(180), y0 + S(38), S(200), S(20), e / 32.0, (240, 60, 50))
        t = _n(vals.get("time"))
        self.text(screen, "TIME", S(110), y0 + S(76), 22, (240, 80, 70), key="black", valign="middle")
        if t is not None:
            sec = int(t) // 60
            self.text(screen, f"{sec // 60:02d}:{sec % 60:02d}", S(180), y0 + S(76), 26, WHITE, key="black", valign="middle")
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.text(screen, f"x{int(lives)}", S(420), y0 + S(28), 30, (255, 230, 120), key="black", valign="middle")
        c = _n(vals.get("char"))
        if c is not None:
            self.text(screen, NC_NAMES[int(c) % len(NC_NAMES)], S(420), y0 + S(66), 24, CREAM, key="black", valign="middle")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


# ============================================================================ Ninja Commando
class NinjaCommandoScene(ShockTroopers2Scene):
    """Ninja Commando as in the game: the jungle seen from above, our blue ninja runs up the dirt path and throws fire
    dragons at the enemy ninjas that come. At the bottom as in the game a face of our own, LIFE in yellow, TIME in
    minutes and seconds. / La jungle vue du dessus, notre ninja bleu lance des dragons de feu, comme dans le jeu."""
    THEME = "ncm_jungle"
    NINJA = ("ninja", (50, 70, 170), (40, 50, 130), (226, 176, 136), (0, 0, 0))
    ENEMY = ("ninja", (110, 60, 140), (80, 40, 100), (210, 180, 150), (0, 0, 0), "sword")

    def hero(self, frame):
        S = self.S
        f = {0: 1, 1: 2, 2: 3, 3: 6}[frame]
        style, top, pants, skin, hair = self.NINJA
        return self.img(("ncmhero", frame), S(130), S(190), fighter_draw(style, top, pants, skin, hair, f), ss=2)

    def foe(self, frame):
        S = self.S
        f = {0: 1, 1: 2, 2: 0, 3: 6}[frame]
        style, top, pants, skin, hair, weapon = self.ENEMY
        return self.img(("ncmfoe", frame), S(300), S(170), fighter_draw(style, top, pants, skin, hair, f, weapon), ss=2, flip=True)

    def road(self, z):
        S = self.S
        return S(NCM_ROAD[0]) + S(70) + z * (S(NCM_ROAD[1]) - S(NCM_ROAD[0]) - S(64))

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "energy")
        if ch and ch[1] < ch[0]:
            self.hurt = now
            self.fx.shake(6, 0.25)

    def fire(self, vals, now, special):
        """A fire dragon from the hands of the ninja. / Un dragon de feu des mains du ninja."""
        S, fx = self.S, self.fx
        x0, y0 = self.hx() + S(50), self.road(self.hz) - S(110)
        live = [f for f in self.foes if not f.get("dead") and x0 < f["x"] < self.W * 0.85]
        tgt = min(live, key=lambda f: abs(f["x"] - x0) + abs(f["z"] - self.hz) * S(300)) if live else None
        tx, ty = (tgt["x"], self.road(tgt["z"]) - S(80)) if tgt else (self.W + S(40), y0)
        fx.tracer(x0, y0, tx, ty, 1800, (255, 150, 40), 16, 140, "front", False)
        fx.tracer(x0, y0, tx, ty, 1800, (255, 240, 160), 6, 100, "front", False)
        fx.later(abs(tx - x0) / (1800 * self.s), fx.small_blast, tx, ty)
        fx.glow(x0, y0, 20, 70, (255, 170, 60), 0.2, "front", 1.0, 0.0)
        if tgt is not None:
            tgt["hp"] -= 2
            tgt["hit"] = now
            if tgt["hp"] <= 0:
                fx.later(0.1, self.kill, tgt, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game, at the bottom: the face, LIFE in yellow, TIME; 1P and the score at the top.
        / Comme dans le jeu, en bas : le visage, LIFE en jaune, TIME ; 1P et le score en haut."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(420), S(58), 160, radius=14)
        self.text(screen, "1P", S(30), S(34), 28, WHITE, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(410), S(12), "right", S(40))
        bar = self.imgs.get("ncmbar")
        if bar is None:
            bar = self.imgs["ncmbar"] = pg.Surface((S(560), S(70)), pg.SRCALPHA)
            bar.fill((0, 0, 0, 210))
        y0 = H - S(74)
        screen.blit(bar, (S(10), y0))
        screen.blit(self.img("ncmface", S(60), S(60), portrait_draw((226, 176, 136), (0, 0, 0), hood=(50, 70, 170), bg=(30, 30, 60)), ss=2),
                    (S(18), y0 + S(5)))
        self.text(screen, "LIFE", S(90), y0 + S(20), 24, (120, 160, 255), key="black", valign="middle")
        e = _n(vals.get("energy"))
        self.bar(screen, S(170), y0 + S(10), S(240), S(22), (e if e is not None else 2) / 2.0, (250, 220, 40))
        self.text(screen, "TIME", S(90), y0 + S(50), 24, (120, 160, 255), key="black", valign="middle")
        t = _n(vals.get("time"))
        if t is not None:
            self.text(screen, f"{int(t) // 60}:{int(t) % 60:02d}", S(170), y0 + S(50), 28, WHITE, key="black", valign="middle")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


# ============================================================================ Blue's Journey
def sprout_draw(frame):
    """Our little hero of the land of plants, facing right: a big round head, an orange cap with a leaf, a green tunic.
    Frames 0 and 1 walk, 2 throw. / Notre petit héros du pays des plantes, grosse tête ronde, casquette orange."""
    def fn(d, W, H):
        dark = (30, 24, 30, 255)
        ow = max(1.0, W * 0.025)
        skin, tunic, tunic_d = (250, 210, 170, 255), (60, 170, 80, 255), (40, 120, 60, 255)
        u = H
        cx = W * 0.45
        step = (0.1, -0.08) if frame == 0 else ((-0.08, 0.1) if frame == 1 else (0.06, -0.04))
        for i, dx in enumerate(step):
            f = (cx + dx * u, H * 0.95)
            _capsule(d, (cx, H * 0.7), f, 0.05 * u, 0.045 * u, tunic_d if i == 0 else tunic, dark, ow)
            d.ellipse([f[0] - 0.06 * u, f[1] - 0.05 * u, f[0] + 0.08 * u, f[1] + 0.02 * u], fill=(200, 60, 40, 255), outline=dark)
        d.ellipse([cx - 0.15 * u, H * 0.48, cx + 0.15 * u, H * 0.8], fill=tunic, outline=dark, width=int(ow))
        hand = (cx + 0.24 * u, H * 0.5) if frame == 2 else (cx + 0.12 * u, H * 0.66)
        _capsule(d, (cx + 0.06 * u, H * 0.56), hand, 0.04 * u, 0.035 * u, skin, dark, ow)
        hx, hy, r = cx + 0.02 * u, H * 0.3, 0.2 * u
        d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=skin, outline=dark, width=int(ow))
        d.ellipse([hx + r * 0.25, hy - r * 0.1, hx + r * 0.5, hy + r * 0.25], fill=dark)
        d.ellipse([hx + r * 0.32, hy - r * 0.04, hx + r * 0.4, hy + r * 0.06], fill=(255, 255, 255, 255))
        d.arc([hx, hy + r * 0.2, hx + r * 0.6, hy + r * 0.6], 20, 160, fill=dark, width=max(1, int(ow)))
        d.chord([hx - r * 1.05, hy - r * 1.1, hx + r * 1.05, hy + r * 0.3], 180, 360, fill=(250, 140, 40, 255), outline=dark)
        d.polygon([(hx + r * 0.5, hy - r * 0.45), (hx + r * 1.5, hy - r * 0.3), (hx + r * 0.6, hy - r * 0.15)], fill=(240, 120, 30, 255),
                  outline=dark)
        d.polygon([(hx - r * 0.1, hy - r * 1.05), (hx - r * 0.5, hy - r * 1.7), (hx + r * 0.3, hy - r * 1.4)], fill=(80, 200, 80, 255), outline=dark)
    return fn


def snail_draw(frame):
    """A big snail with a striped shell, facing left. / Un gros escargot à coquille rayée, face à gauche."""
    def fn(d, W, H):
        dark = (40, 24, 30, 255)
        ow = max(1.0, W * 0.025)
        st = 0.03 * W if frame else 0.0
        d.rounded_rectangle([W * 0.05 - st, H * 0.66, W * 0.95, H * 0.96], radius=H * 0.12, fill=(170, 210, 90, 255), outline=dark, width=int(ow))
        d.line([(W * 0.16 - st, H * 0.68), (W * 0.06 - st, H * 0.4)], fill=dark, width=max(1, int(ow)))
        d.line([(W * 0.24 - st, H * 0.68), (W * 0.2 - st, H * 0.38)], fill=dark, width=max(1, int(ow)))
        d.ellipse([W * 0.02 - st, H * 0.32, W * 0.12 - st, H * 0.44], fill=(255, 255, 255, 255), outline=dark)
        d.ellipse([W * 0.16 - st, H * 0.3, W * 0.26 - st, H * 0.42], fill=(255, 255, 255, 255), outline=dark)
        d.ellipse([W * 0.32, H * 0.1, W * 0.92, H * 0.84], fill=(220, 120, 60, 255), outline=dark, width=int(ow))
        for k in range(3):
            r = (0.26 - k * 0.08) * W
            cx, cy = W * 0.62, H * 0.47
            d.arc([cx - r, cy - r, cx + r, cy + r], 0, 300, fill=(150, 70, 30, 255), width=max(2, int(W * 0.03)))
    return fn


def bee_draw(d, W, H):
    """A round striped bee, facing left. / Une abeille ronde rayée, face à gauche."""
    dark = (30, 24, 20, 255)
    d.ellipse([W * 0.3, H * 0.0, W * 0.62, H * 0.42], fill=(220, 240, 255, 200), outline=dark)
    d.ellipse([W * 0.12, H * 0.28, W * 0.9, H * 0.94], fill=(250, 210, 40, 255), outline=dark, width=max(1, int(W * 0.03)))
    for k in range(2):
        x = W * (0.42 + k * 0.18)
        d.line([(x, H * 0.32), (x, H * 0.9)], fill=dark, width=max(2, int(W * 0.07)))
    d.ellipse([W * 0.16, H * 0.46, W * 0.28, H * 0.6], fill=dark)
    d.polygon([(W * 0.9, H * 0.6), (W * 1.0, H * 0.64), (W * 0.9, H * 0.7)], fill=dark)


def leaf_draw(d, W, H):
    d.ellipse([0, H * 0.2, W - 1, H * 0.8], fill=(70, 200, 70, 255), outline=(20, 90, 30, 255), width=max(1, int(W * 0.06)))
    d.line([(W * 0.1, H * 0.5), (W * 0.9, H * 0.5)], fill=(20, 90, 30, 255), width=max(1, int(W * 0.05)))


def flower_icon_draw(d, W, H):
    for a in range(5):
        x = W * 0.5 + math.cos(a * 1.257) * W * 0.26
        y = H * 0.5 + math.sin(a * 1.257) * H * 0.26
        d.ellipse([x - W * 0.2, y - H * 0.2, x + W * 0.2, y + H * 0.2], fill=(250, 90, 140, 255))
    d.ellipse([W * 0.36, H * 0.36, W * 0.64, H * 0.64], fill=(255, 220, 60, 255))


def heart_draw(full):
    def fn(d, W, H):
        col = (240, 40, 60, 255) if full else (70, 40, 50, 255)
        d.ellipse([0, 0, W * 0.56, H * 0.56], fill=col)
        d.ellipse([W * 0.44, 0, W, H * 0.56], fill=col)
        d.polygon([(W * 0.02, H * 0.36), (W * 0.98, H * 0.36), (W * 0.5, H * 0.98)], fill=col)
    return fn


class BluesJourneyScene(CyberLipScene):
    """Blue's Journey as in the game: the land of giant plants, long leaves hanging from the top, a huge clay pot, our
    little hero of our own walks the grass and throws leaves at the snails and the bees. 1P= and the score, the lives,
    TIME=, LIFE and its hearts at the top, the flowers at the bottom left, as in the game.
    / Le pays des plantes géantes, notre petit héros lance des feuilles aux escargots et aux abeilles, comme dans le jeu."""
    THEME = "bj_jungle"
    SHADE = (60, 60)
    EXPLOSIONS = False

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.fx.sp.register("bjleaf", draw_img(S(40), S(26), leaf_draw))
        self.throws = 0                                   # (tests)

    def hero(self, frame):
        S = self.S
        return self.img(("bjhero", frame), S(110), S(130), sprout_draw(frame), ss=2)

    def foe(self, frame):
        S = self.S
        return self.img(("bjsnail", frame), S(110), S(90), snail_draw(frame), ss=2)

    def flyer(self, now):
        S = self.S
        return self.img("bjbee", S(80), S(64), bee_draw, ss=2)

    def floor(self):
        return self.S(BJ_FLOOR) + self.S(6)

    def move(self, vals, now, idle):
        return 0.2 if idle else 0.8

    def update(self, vals, now):
        S, rng = self.S, self.rng
        if now >= self.next_foe:
            self.next_foe = now + rng.uniform(0.6, 1.2)
            fly = rng.random() < 0.3
            self.foes.append({"x": self.W + S(80), "y": S(rng.uniform(180, 260)) if fly else self.floor(), "fly": fly, "hp": 2,
                              "v": rng.uniform(110, 180) * self.s, "ph": rng.uniform(0, 6), "t0": now})
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.hurt = now
            self.popup(tr("-1 VIE", "-1 LIFE"), self.W * 0.3, self.floor() - S(200), (255, 90, 70), 38)
        ch = self.changed(vals, "energy")
        if ch and ch[1] < ch[0]:
            self.hurt = now
            self.fx.sparks(self.W * 0.3, self.floor() - S(80), 12, (255, 120, 140), (200, 400), (0, 360), (0.2, 0.4), 0, "front", 3, 14)
        ch = self.changed(vals, "money")
        if ch and ch[1] > ch[0]:
            self.popup(f"+{int(ch[1] - ch[0])}", self.W * 0.3, self.floor() - S(200), (255, 120, 170), 34)
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:
            live = [f for f in self.foes if not f.get("dead") and self.W * 0.35 < f["x"] < self.W * 0.9]
            if live:
                self.kill(min(live, key=lambda f: f["x"]), now)
        if now >= self.fire_t and any(not f.get("dead") and self.W * 0.35 < f["x"] < self.W * 0.85 for f in self.foes):
            self.fire_t = now + rng.uniform(0.5, 1.0)
            self.fire(now)

    def fire(self, now):
        """A leaf thrown at the nearest creature. / Une feuille lancée sur la créature la plus proche."""
        S = self.S
        x0, y0 = self.W * 0.3 + S(40), self.floor() - S(80)
        live = [f for f in self.foes if not f.get("dead") and f["x"] > x0]
        tgt = min(live, key=lambda f: f["x"]) if live else None
        tx, ty = (tgt["x"], tgt["y"] - (S(40) if not tgt["fly"] else 0)) if tgt else (self.W + S(50), y0)
        self.throws += 1

        def hit(x, y):
            if tgt is not None and not tgt.get("dead"):
                tgt["hp"] -= 1
                if tgt["hp"] <= 0:
                    self.kill(tgt, now)
        self.fx.projectile("bjleaf", x0, y0, tx, ty, 0.3, 30, hit, spin=900)

    def kill(self, f, now):
        if f.get("dead"):
            return
        f["dead"] = now
        self.kills += 1
        y = f["y"] - (self.S(40) if not f["fly"] else 0)
        self.fx.sparks(f["x"], y, 18, (255, 150, 200), (200, 500), (0, 360), (0.3, 0.6), 300, "front", 4, 10)
        self.fx.sparks(f["x"], y, 10, (255, 230, 90), (100, 300), (0, 360), (0.3, 0.6), 200, "front", 3, 8)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P= and the score, the lives, TIME=, LIFE and its hearts at the top, the flowers at the bottom
        left. / Comme dans le jeu : 1P= et le score, les vies, TIME=, LIFE et ses cœurs, les fleurs en bas à gauche."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(620), S(104), 160, radius=14)
        self.text(screen, "1P=", S(28), S(30), 28, WHITE, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(330), S(10), "right", S(40))
        lives = _n(vals.get("lives"))
        if lives is not None:
            screen.blit(self.img("bjflower", S(30), S(30), flower_icon_draw, ss=2), (S(346), S(16)))
            self.text(screen, f"x{int(lives)}", S(380), S(30), 28, WHITE, key="black", valign="middle")
        t = _n(vals.get("time"))
        if t is not None:
            self.text(screen, f"TIME={int(t) // 60}", S(440), S(30), 28, (190, 210, 255), key="black", valign="middle")
        self.text(screen, "LIFE", S(28), S(76), 24, WHITE, key="black", valign="middle")
        e = _n(vals.get("energy"))
        if e is not None:
            for i in range(5):
                img = self.img(("bjheart", i < int(e)), S(30), S(28), heart_draw(i < int(e)), ss=2)
                screen.blit(img, (S(100) + i * S(36), S(62)))
        m = _n(vals.get("money"))
        if m is not None:
            self.pill(screen, S(12), H - S(62), S(200), S(52), 160, radius=12)
            screen.blit(self.img("bjflower", S(30), S(30), flower_icon_draw, ss=2), (S(26), H - S(52)))
            self.text(screen, f"= {int(m)}", S(66), H - S(36), 30, WHITE, key="black", valign="middle")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


# ============================================================================ Puzzle Bobble 2, Puzzle De Pon!
def pillar_frame_draw(style):
    """The frame of a bubble board: metal pillars for Puzzle Bobble 2, brick pillars around a starry night for
    Puzzle De Pon!. / Le cadre d'un plateau de bulles : piliers de métal, ou de briques autour d'une nuit étoilée."""
    def fn(d, W, H):
        k = W / 640.0
        if style == "bricks":
            d.rectangle([40 * k, 40 * k, W - 40 * k, H], fill=(16, 22, 60, 255))
            for i in range(60):
                x, y = (37 * i * 7919) % int(W - 100 * k) + 50 * k, (53 * i * 104729) % int(H - 60 * k) + 50 * k
                d.ellipse([x - 2 * k, y - 2 * k, x + 2 * k, y + 2 * k], fill=(200, 210, 255, 255))
            for x0 in (0, W - 40 * k):
                d.rectangle([x0, 0, x0 + 40 * k, H], fill=(200, 140, 60, 255))
                y = 0
                row = 0
                while y < H:
                    d.line([(x0, y), (x0 + 40 * k, y)], fill=(120, 70, 30, 255), width=max(1, int(2 * k)))
                    xm = x0 + (20 * k if row % 2 else 0)
                    d.line([(xm, y), (xm, y + 14 * k)], fill=(120, 70, 30, 255), width=max(1, int(2 * k)))
                    y += 14 * k
                    row += 1
            d.rectangle([0, 0, W, 40 * k], fill=(200, 140, 60, 255), outline=(120, 70, 30, 255), width=max(1, int(2 * k)))
        else:
            d.rectangle([40 * k, 40 * k, W - 40 * k, H], fill=(20, 30, 90, 70))
            for x0 in (0, W - 40 * k):
                d.rectangle([x0, 0, x0 + 40 * k, H], fill=(190, 196, 206, 255), outline=(90, 96, 110, 255), width=max(1, int(3 * k)))
                d.line([(x0 + 12 * k, 0), (x0 + 12 * k, H)], fill=(240, 244, 250, 255), width=max(1, int(4 * k)))
                for y in range(int(60 * k), int(H), int(90 * k)):
                    d.ellipse([x0 + 14 * k, y, x0 + 26 * k, y + 12 * k], fill=(120, 126, 140, 255))
            d.rectangle([0, 0, W, 40 * k], fill=(190, 196, 206, 255), outline=(90, 96, 110, 255), width=max(1, int(3 * k)))
    return fn


class PuzzleBobble2Scene(PuzzleBobbleScene):
    """Puzzle Bobble 2 as in the game: the beach of the first rounds, the boards in their metal frames, the launcher
    and its next bubble. The bubbles are shot when the game's shot timer starts again, or by themselves.
    / La plage des premiers rounds, les plateaux dans leurs cadres de métal, comme dans le jeu."""
    THEME = "pb2_beach"
    FRAME = "metal"

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.auto = {"p1": 0.0, "p2": 0.0}
        self.shots = 0                                    # (tests)

    def shoot(self, side, c, now):
        x, y = self.launcher_xy(side)
        a = math.radians(self.angle[side])
        v = 1700 * self.s
        self.flying.append({"c": c, "x": x, "y": y, "vx": math.sin(a) * v, "vy": -math.cos(a) * v, "t0": now, "side": side})
        self.slide[side] = now
        self.shots += 1

    def update(self, vals, now):
        before = len(self.flying)
        super().update(vals, now)
        if len(self.flying) > before:
            self.shots += len(self.flying) - before
        for side, suf in (("p1", ""), ("p2", "_p2")):
            if side == "p2" and not self.p2_in(vals):
                continue
            if vals.get("bubble" + suf) is not None:
                continue
            ch = self.changed(vals, "time" + suf)
            if (ch and ch[1] > ch[0]) or now >= self.auto[side]:          # the shot timer starts again: a bubble left
                self.auto[side] = now + self.rng.uniform(1.4, 2.6)
                self.shoot(side, self.rng.randrange(6), now)

    def draw_hud(self, screen, eng, vals, logo, now):
        S = self.S
        for side, board in self.boards.items():
            if side == "p2" and not self.p2_in(vals):
                continue
            w = board.x1 - board.x0
            fr = self.img(("pbframe", self.FRAME), int(w + S(80)), S(340), pillar_frame_draw(self.FRAME), ss=1)
            screen.blit(fr, (int(board.x0 - S(40)), int(board.top - S(40))))
        super().draw_hud(screen, eng, vals, logo, now)


def compass_draw(d, W, H):
    """The star dial of Puzzle De Pon!, pink and white in its golden rays. / Le cadran étoilé, rose et blanc."""
    for i in range(8):
        a = i * math.pi / 4
        d.polygon([(W / 2 + math.cos(a) * W * 0.5, H / 2 + math.sin(a) * H * 0.5), (W / 2 + math.cos(a + 0.3) * W * 0.3, H / 2 + math.sin(a + 0.3) * H * 0.3),
                   (W / 2 + math.cos(a - 0.3) * W * 0.3, H / 2 + math.sin(a - 0.3) * H * 0.3)], fill=(250, 200, 60, 255))
    d.ellipse([W * 0.14, H * 0.14, W * 0.86, H * 0.86], fill=(250, 250, 250, 255), outline=(200, 150, 40, 255), width=max(2, int(W * 0.03)))
    d.pieslice([W * 0.16, H * 0.16, W * 0.84, H * 0.84], -90, 0, fill=(250, 160, 200, 255))
    d.pieslice([W * 0.16, H * 0.16, W * 0.84, H * 0.84], 90, 180, fill=(250, 160, 200, 255))
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = W * (0.22 if i % 2 == 0 else 0.1)
        pts.append((W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r))
    d.polygon(pts, fill=(250, 130, 190, 255))


class PuzzleDePonScene(PuzzleBobble2Scene):
    """Puzzle De Pon! as in the game: the pale blue sky full of stars, the boards between brick pillars around a starry
    night, the star dial whose hand turns with the time left. The bubble shot and the next one come from the game.
    / Le ciel bleu pâle étoilé, les plateaux entre leurs piliers de briques, le cadran étoilé, comme dans le jeu."""
    THEME = "pdp_stars"
    FRAME = "bricks"

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        super().draw_hud(screen, eng, vals, logo, now)
        t = _n(vals.get("time"))
        if t is not None and not self.p2_in(vals):                     # the star dial and its hand
            cx, cy, r = W / 2, S(280), S(110)
            dial = self.img("pdpdial", int(2 * r), int(2 * r), compass_draw, ss=2)
            screen.blit(dial, (int(cx - r), int(cy - r)))
            a = -math.pi / 2 + _clamp(t / 120.0) * math.tau
            self.pg.draw.line(screen, (30, 40, 120), (int(cx), int(cy)), (int(cx + math.cos(a) * r * 0.62), int(cy + math.sin(a) * r * 0.62)),
                              max(2, S(8)))
            self.pg.draw.circle(screen, (30, 40, 120), (int(cx), int(cy)), S(10))
        lv = _n(vals.get("level"))
        if lv is not None:
            self.label(screen, f"LEVEL-{int(lv) + 2}", W / 2, S(424), 32, WHITE, key="black", align="center")


# ============================================================================ Magical Drop II, Money Puzzle Exchanger
class MagicalDrop2Scene(MagicalDropScene):
    """Magical Drop II as in the game: the orange brick wall and its marble columns, the deep teal fields, the jester
    below, LEVEL at the top. The quota going down pops drops, the level rising pushes a row.
    / Le mur de briques orange et ses colonnes de marbre, les champs bleu-vert, LEVEL en haut, comme dans le jeu."""
    THEME = "md2_bricks"
    FIELD_BOX = False

    def draw_hud(self, screen, eng, vals, logo, now):
        super().draw_hud(screen, eng, vals, logo, now)
        lv = _n(vals.get("level"))
        if lv is not None:
            self.label(screen, f"LEVEL {int(lv)}", self.fields["p1"].x(3), self.S(76), 34, (250, 240, 200), key="stencil", align="center")


COINS = (("10", (200, 120, 60), (120, 60, 20)), ("50", (210, 214, 224), (110, 116, 130)), ("100", (226, 230, 238), (120, 126, 140)),
         ("500", (250, 200, 60), (150, 100, 20)))


def coin_draw(hd, k):
    """A coin with its value. / Une pièce et sa valeur."""
    label, face, edge = COINS[k % len(COINS)]

    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=edge + (255,))
        d.ellipse([W * 0.06, H * 0.06, W * 0.94, H * 0.94], fill=face + (255,))
        d.ellipse([W * 0.16, H * 0.16, W * 0.84, H * 0.84], outline=_mixc(face, (0, 0, 0), 0.25), width=max(1, int(W * 0.04)))
        f = hd.font("black", int(H * (0.42 if len(label) < 3 else 0.32)))
        d.text((W / 2, H * 0.52), label, font=f, fill=_mixc(edge, (0, 0, 0), 0.3), anchor="mm")
    return fn


def piggy_draw(color):
    """A little piggy bank who throws the coins, under each field. / Une petite tirelire qui lance les pièces."""
    def fn(d, W, H):
        dark = (40, 24, 30, 255)
        d.ellipse([W * 0.12, H * 0.2, W * 0.88, H * 0.86], fill=(250, 170, 190, 255), outline=dark, width=max(1, int(W * 0.03)))
        d.ellipse([W * 0.72, H * 0.42, W * 0.96, H * 0.64], fill=(240, 140, 170, 255), outline=dark)
        d.ellipse([W * 0.82, H * 0.48, W * 0.86, H * 0.56], fill=dark)
        d.ellipse([W * 0.6, H * 0.34, W * 0.68, H * 0.44], fill=dark)
        d.rectangle([W * 0.4, H * 0.18, W * 0.56, H * 0.24], fill=dark)
        for x in (0.26, 0.66):
            d.rectangle([W * x, H * 0.8, W * (x + 0.1), H * 0.98], fill=(240, 140, 170, 255), outline=dark)
        d.polygon([(W * 0.3, H * 0.24), (W * 0.36, H * 0.06), (W * 0.44, H * 0.22)], fill=color + (255,), outline=dark)
    return fn


class MoneyPuzzleScene(MagicalDropScene):
    """Money Puzzle Exchanger as in the game: the pastel diamonds, the fields framed in pink full of coins of 10, 50,
    100 and 500, a little piggy bank of our own under each field. A chain read in the game pops coins, the level going
    up pushes a row. STAGE, the level and the chains between the fields.
    / Les losanges pastel, les champs pleins de pièces, une tirelire à nous sous chaque champ, comme dans le jeu."""
    THEME = "mpe_pastel"
    FIELD_BOX = False

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.chains = 0                                   # (tests)

    def drop(self, k, size):
        S = self.S
        return self.img(("coin", int(k) % len(DROP_RGB), size), S(size), S(size), coin_draw(self.hd, int(k)), ss=2)

    def jester(self, side):
        S = self.S
        return self.img(("piggy", side), S(74), S(62), piggy_draw((250, 220, 60) if side == "p1" else (120, 200, 250)), ss=2)

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "chain")
        if ch and ch[1] > ch[0]:
            self.chains += 1
            self._throw("p1", 3 + int(ch[1]), now)
            self.popup(f"{int(ch[1])} CHAIN", self.fields["p1"].x(3), self.S(240), (250, 120, 190), 40)
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0] and not (self.changed(vals, "chain")):
            self._throw("p1", 3, now)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        super().draw_hud(screen, eng, vals, logo, now)
        lv = _n(vals.get("level"))
        if lv is not None:
            self.label(screen, f"STAGE {int(lv) + 1}", W / 2, S(150), 40, (250, 110, 180), key="stencil", align="center")
        mc = _n(vals.get("max_chain"))
        if mc is not None:
            self.label(screen, f"MAX CHAIN {int(mc)}", W / 2, S(210), 28, (90, 200, 120), key="black", align="center")


SCENES = {"mutnat": MutationNationScene, "sengoku": SengokuScene, "sengoku2": Sengoku2Scene, "ncombat": NinjaCombatScene,
          "ncommand": NinjaCommandoScene, "bjourney": BluesJourneyScene, "pbobbl2n": PuzzleBobble2Scene, "magdrop2": MagicalDrop2Scene,
          "miexchng": MoneyPuzzleScene, "puzzledp": PuzzleDePonScene}
