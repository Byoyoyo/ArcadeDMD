"""HD scenes of the eleventh batch of Neo Geo games done one by one (1.27), each drawn after screenshots of its game.
Each game has its own animated backdrop and reacts to the values read in its memory. The heroes, the hosts, the
players and the tiles are creations of the program in the spirit of the games, the quiz questions are our own.

Scènes HD du onzième lot de jeux Neo Geo faits un par un (1.27), chacune dessinée d'après des captures de son jeu.
Les héros, les présentateurs, les joueurs et les tuiles sont des créations du programme, les questions sont à nous.
"""

import math

from .hd_games import CREAM, GOLD, P1C, P2C, WHITE, GameScene, _clamp, _n
from .hd_games3 import _capsule
from .hd_games5 import _mixc
from .hd_games6 import portrait_draw
from .hd_games10 import BangBangBustersScene
from .hd_themes11 import ND_ROWS, QZ_PANEL, SH_CELL, SH_X0, SH_Y0          # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr

DARKLINE = (24, 20, 26, 255)


# ============================================================================ Nightmare in the Dark
def gravekeeper_draw(frame):
    """Our little gravekeeper of our own: a hood, a long coat, a lantern that throws fire. / Notre petit gardien de
    cimetière à nous : une capuche, un long manteau, une lanterne qui lance du feu."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.04))
        step = (frame % 2) * W * 0.05
        for x in (0.3 - step / W, 0.54 + step / W):
            d.rounded_rectangle([W * x, H * 0.76, W * (x + 0.16), H * 0.98], radius=W * 0.05, fill=(50, 40, 40, 255), outline=DARKLINE, width=ow)
        d.polygon([(W * 0.24, H * 0.4), (W * 0.76, H * 0.4), (W * 0.84, H * 0.84), (W * 0.16, H * 0.84)], fill=(70, 60, 120, 255), outline=DARKLINE)
        d.ellipse([W * 0.26, H * 0.08, W * 0.74, H * 0.5], fill=(70, 60, 120, 255), outline=DARKLINE, width=ow)    # la capuche
        d.ellipse([W * 0.34, H * 0.2, W * 0.66, H * 0.46], fill=(240, 210, 180, 255), outline=DARKLINE)
        for ex in (0.44, 0.58):
            d.ellipse([W * (ex - 0.03), H * 0.3, W * (ex + 0.03), H * 0.36], fill=DARKLINE)
        d.line([(W * 0.7, H * 0.5), (W * 0.9, H * 0.56)], fill=(70, 60, 120, 255), width=max(2, int(W * 0.1)))
        d.rounded_rectangle([W * 0.84, H * 0.5, W * 0.99, H * 0.68], radius=W * 0.03, fill=(250, 200, 80, 255), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.88, H * 0.54, W * 0.95, H * 0.64], fill=(255, 120, 40, 255))
    return fn


def zombie_draw(frame):
    """A little green zombie of our own, arms forward. / Un petit zombie vert à nous, les bras en avant."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.04))
        lift = 0.03 * frame
        for x in (0.3, 0.52):
            d.rounded_rectangle([W * x, H * (0.72 - lift), W * (x + 0.16), H * 0.98], radius=W * 0.05, fill=(60, 60, 110, 255), outline=DARKLINE, width=ow)
        d.rounded_rectangle([W * 0.26, H * 0.4, W * 0.72, H * 0.76], radius=W * 0.1, fill=(150, 90, 140, 255), outline=DARKLINE, width=ow)
        _capsule(d, (W * 0.6, H * 0.48), (W * 0.95, H * 0.46), W * 0.1, W * 0.08, (120, 190, 100, 255), DARKLINE, ow)
        d.ellipse([W * 0.28, H * 0.06, W * 0.7, H * 0.46], fill=(120, 190, 100, 255), outline=DARKLINE, width=ow)
        for ex in (0.42, 0.58):
            d.ellipse([W * (ex - 0.05), H * 0.2, W * (ex + 0.05), H * 0.3], fill=(255, 255, 200, 255), outline=DARKLINE)
        d.line([(W * 0.4, H * 0.38), (W * 0.6, H * 0.36)], fill=DARKLINE, width=ow)
    return fn


def sheet_ghost_draw(frame):
    """A little ghost of our own in its sheet. / Un petit fantôme à nous dans son drap."""
    def fn(d, W, H):
        pts = [(W * 0.2, H * 0.92)]
        for i in range(17):
            a = math.pi + i * math.pi / 16
            pts.append((W * 0.5 + math.cos(a) * W * 0.32, H * 0.42 + math.sin(a) * H * 0.36))
        pts.append((W * 0.8, H * 0.92))
        for i in range(5):
            pts.append((W * (0.8 - (i + 0.5) * 0.12), H * (0.98 if (i + frame) % 2 == 0 else 0.86)))
        d.polygon(pts, fill=(240, 240, 255, 255), outline=DARKLINE)
        for ex in (0.42, 0.58):
            d.ellipse([W * (ex - 0.05), H * 0.32, W * (ex + 0.05), H * 0.46], fill=DARKLINE)
        d.ellipse([W * 0.45, H * 0.5, W * 0.55, H * 0.6], fill=(60, 20, 40, 255))
    return fn


class NightmareScene(BangBangBustersScene):
    """Nightmare in the Dark as in the game: the graveyard at night under a huge full moon, the platforms of mossy stones;
    our little gravekeeper of our own sets the zombies and the ghosts on fire with his lantern and kicks the balls of
    fire away. 1UP and the score, TIME in yellow and 2UP at the top, the lives read in the game.
    / Le cimetière la nuit sous une énorme pleine lune ; notre petit gardien à nous enflamme les zombies et les fantômes
    avec sa lanterne et chasse les boules de feu, comme dans le jeu."""
    THEME = "nd_grave"
    ROWS = ND_ROWS

    def hero_img(self, frame, d):
        S = self.S
        return self.img(("ndkeeper", frame, d), S(70), S(84), gravekeeper_draw(frame), ss=2, flip=d < 0)

    def foe_img(self, kind, frame):
        S = self.S
        return self.img(("ndfoe", kind, frame), S(66), S(70), (zombie_draw if kind == 0 else sheet_ghost_draw)(frame), ss=2)

    def trap(self, f, now):
        super().trap(f, now)
        self.fx.glow(f["x"], self.row_y(f["row"]) - self.S(36), 20, 80, (255, 140, 40), 0.3, "front", 0.9, 0.0)

    def draw_trapped(self, screen, f, y, now):
        """The monster burns, a ball of fire. / Le monstre brûle, une boule de feu."""
        S, pg = self.S, self.pg
        r = S(40) + math.sin(now * 9) * S(3)
        pg.draw.circle(screen, (230, 80, 30), (int(f["x"]), int(y - S(32))), int(r))
        pg.draw.circle(screen, (255, 190, 60), (int(f["x"] - r * 0.2), int(y - S(36))), int(r * 0.6))
        if int(now * 20) % 2:
            self.fx.sparks(f["x"], y - S(60), 2, (255, 160, 40), (60, 160), (240, 300), (0.2, 0.4), -200, "front", 4, 10)

    def status(self, screen, eng, vals, logo, now):
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(4), S(380), S(70), now)
        self.pill(screen, S(12), S(6), S(420), S(84), 160, radius=14)
        self.text(screen, "1UP", S(28), S(30), 26, (255, 90, 80), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(410), S(10), "right", S(40))
        lives = _n(vals.get("lives"))
        if lives is not None:
            for k in range(int(min(lives, 6))):
                pg.draw.circle(screen, (220, 40, 40), (S(40) + k * S(30), S(68)), S(11))
                pg.draw.circle(screen, (60, 20, 20), (S(40) + k * S(30), S(68)), S(11), max(1, S(2)))
        t = _n(vals.get("time"))
        if t is not None:
            self.label(screen, f"TIME {int(t)}s", W / 2, S(98), 30, (255, 230, 60), key="black", align="center")
        if self.p2_in(vals):
            self.text(screen, "2UP", W - S(400), S(30), 26, P2C, key="black", valign="middle")
        else:
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


# ============================================================================ The Super Spy
def spy_foe_draw(mask, suit, frame):
    """A masked fighter of our own facing us, his knives in his hands: frame 0 guard, 1 strike, 2 hurt.
    / Un combattant masqué à nous, face à nous, ses couteaux à la main."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.012))
        lean = (0.0, 0.03, -0.05)[frame]
        cx = W * (0.5 + lean)
        d.polygon([(cx - W * 0.26, H * 0.36), (cx + W * 0.26, H * 0.36), (cx + W * 0.2, H * 1.0), (cx - W * 0.2, H * 1.0)], fill=suit + (255,),
                  outline=DARKLINE)
        d.ellipse([cx - W * 0.13, H * 0.08, cx + W * 0.13, H * 0.4], fill=mask + (255,), outline=DARKLINE, width=ow)
        d.rectangle([cx - W * 0.09, H * 0.2, cx + W * 0.09, H * 0.25], fill=(250, 250, 240, 255))
        for ex in (-0.045, 0.045):
            d.ellipse([cx + W * (ex - 0.02), H * 0.205, cx + W * (ex + 0.02), H * 0.245], fill=DARKLINE)
        for side in (-1, 1):
            up = frame == 1 and side == 1
            hand = (cx + side * W * (0.3 if not up else 0.16), H * (0.42 if not up else 0.3))
            _capsule(d, (cx + side * W * 0.22, H * 0.42), hand, W * 0.09, W * 0.07, suit + (255,), DARKLINE, ow)
            d.ellipse([hand[0] - W * 0.04, hand[1] - W * 0.04, hand[0] + W * 0.04, hand[1] + W * 0.04], fill=(230, 190, 150, 255), outline=DARKLINE)
            d.line([hand, (hand[0] + side * W * 0.02, hand[1] - H * 0.16)], fill=(220, 225, 235, 255), width=max(2, int(W * 0.015)))
    return fn


def fist_draw(left, frame):
    """Our fist and forearm in a white sleeve, from below. / Notre poing et son avant-bras dans une manche blanche."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.02))
        reach = 0.1 if frame == 1 else 0.5
        d.polygon([(W * 0.2, H), (W * 0.8, H), (W * 0.66, H * reach + H * 0.2), (W * 0.3, H * reach + H * 0.2)], fill=(240, 240, 236, 255), outline=DARKLINE)
        d.rounded_rectangle([W * 0.24, H * reach, W * 0.76, H * reach + H * 0.26], radius=W * 0.12, fill=(230, 180, 140, 255), outline=DARKLINE, width=ow)
        for k in range(3):
            x = W * (0.36 + k * 0.12)
            d.line([(x, H * reach + H * 0.03), (x, H * reach + H * 0.12)], fill=(170, 120, 90, 255), width=ow)
    return fn


class SuperSpyScene(GameScene):
    """The Super Spy as in the game: the corridor of the building and its doors with the red IN sign, a masked fighter of
    our own faces us, our fists strike from below. The energy read in the game drops when he hits us, a bullet spent
    is a shot. 1P and the score, the floor and its arrows, the energy, the weapon and its ammunition.
    / Le couloir de l'immeuble, un combattant masqué à nous face à nous, nos poings frappent d'en bas ; l'énergie lue
    dans le jeu baisse quand il nous touche, une balle dépensée est un tir, comme dans le jeu."""
    THEME = "ss_corridor"
    STATIC = True
    SHADE = (60, 40)
    FOES = (((200, 170, 70), (60, 50, 110)), ((150, 40, 60), (90, 40, 100)), ((60, 60, 70), (40, 80, 60)))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.foe = 0
        self.fhp = 1.0
        self.punch = (-9.0, 0)
        self.foe_act = -9.0
        self.next_punch = 0.8
        self.floor = 1
        self.hurt = -9.0
        self.punches = 0                                  # (tests)
        self.shots = 0
        self.down = None

    def update(self, vals, now):
        ch = self.changed(vals, "energy")                                   # the values first, every image / les valeurs d'abord
        if ch and ch[1] < ch[0]:
            self.hurt = now
            self.foe_act = now
            self.fx.shake(7, 0.3)
        for name in ("ammo", "ammo_mg"):
            ch = self.changed(vals, name)
            if ch and ch[1] < ch[0]:                                        # a shot / un tir
                self.shots += 1
                x, y = self.W * 0.68, self.H - self.S(150)
                self.fx.glow(x, y, 20, 100, (255, 220, 120), 0.2, "front", 1.0, 0.0)
                self.fx.tracer(x, y, self.W / 2, self.S(200), 3000, (255, 230, 150), 6, 120, "front", True)
                if self.down is None:
                    self.fhp -= 0.15
                    if self.fhp <= 0:
                        self.down = now
                        self.popup(tr("ÉTAGE SUIVANT", "NEXT FLOOR"), self.W / 2, self.S(180), GOLD, 40)
        if self.down is not None:
            if now - self.down > 1.5:
                self.down = None
                self.foe = (self.foe + 1) % len(self.FOES)
                self.fhp = 1.0
                self.floor += 1
            return
        if now >= self.next_punch:                                          # a punch, left or right / un coup de poing
            self.next_punch = now + self.rng.uniform(0.35, 0.7)
            side = self.rng.randrange(2)
            self.punch = (now, side)
            self.punches += 1
            if self.rng.random() < 0.7:
                self.fhp -= self.rng.uniform(0.06, 0.12)
                self.fx.sparks(self.W / 2 + (-1 if side == 0 else 1) * self.S(40), self.S(200), 12, (255, 240, 200), (200, 500), (0, 360), (0.15, 0.3),
                               0, "front", 3, 10)
            else:
                self.foe_act = now
            if self.fhp <= 0:
                self.down = now
                self.popup(tr("ÉTAGE SUIVANT", "NEXT FLOOR"), self.W / 2, self.S(180), GOLD, 40)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, H, pg = self.S, self.W, self.H, self.pg
        mask, suit = self.FOES[self.foe]
        frame = 2 if now - self.punch[0] < 0.2 and self.fhp < 1.0 else (1 if now - self.foe_act < 0.3 else 0)
        if self.down is None or int(now * 10) % 2 == 0:
            img = self.img(("ssfoe", self.foe, frame), S(330), S(360), spy_foe_draw(mask, suit, frame), ss=2)
            y = S(90) if self.down is None else S(90) + (now - self.down) * S(200)
            screen.blit(img, (int(W / 2 - img.get_width() / 2), int(y)))
        t0, side = self.punch                                               # our fists / nos poings
        for k in range(2):
            out = 1 if (k == side and now - t0 < 0.15) else 0
            img = self.img(("ssfist", k, out), S(200), S(260), fist_draw(k == 0, out), ss=2, flip=k == 1)
            x = W / 2 + (-1 if k == 0 else 1) * S(150)
            screen.blit(img, (int(x - img.get_width() / 2), int(H - img.get_height() + S(40))))
        if now - self.hurt < 0.25:
            veil = self.imgs.get("ssred")
            if veil is None:
                veil = self.imgs["ssred"] = pg.Surface((W, H)).convert()
                veil.fill((120, 0, 0))
            screen.blit(veil, (0, 0), special_flags=pg.BLEND_RGB_ADD)
        self.hd.draw_logo(screen, logo, W / 2, S(4), S(380), S(70), now)
        self.pill(screen, S(12), S(6), S(520), S(112), 170, radius=14)
        self.text(screen, "1P-", S(28), S(30), 26, (255, 230, 120), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            self.hd._score(screen, eng, "score", S(330), S(10), "right", S(40))
        e = _n(vals.get("energy"))
        if e is not None:
            self.text(screen, "EX", S(28), S(70), 20, (255, 100, 80), key="black", valign="middle", glow=0)
            for k in range(8):
                pg.draw.rect(screen, (250, 210, 60) if k < e else (60, 50, 40), (S(70) + k * S(32), S(60), S(26), S(20)), border_radius=S(3))
        wpn = _n(vals.get("weapon"))
        ammo = _n(vals.get("ammo_mg" if wpn else "ammo"))
        if wpn is not None:
            name = "M.GUN" if wpn else tr("PISTOLET", "PISTOL")
            self.text(screen, f"{name} {int(ammo) if ammo is not None else ''}", S(28), S(100), 20, CREAM, key="black", valign="middle", glow=0)
        bx = W - S(250)                                                     # the floor and its arrows / l'étage
        pg.draw.polygon(screen, (40, 60, 160), [(bx, S(90)), (bx + S(60), S(20)), (bx + S(170), S(20)), (bx + S(230), S(90))])
        self.text(screen, f"{self.floor}F", bx + S(115), S(58), 34, WHITE, key="black", align="center", valign="middle")
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, W - S(140), S(120), 26, colw, align="center")


# ============================================================================ the quizzes / les quiz
QUESTIONS = (
    (("Quelle planète est la plus grande ?", "Which planet is the biggest?"),
     (("Mars", "Mars"), ("Jupiter", "Jupiter"), ("Vénus", "Venus"), ("Mercure", "Mercury")), 1),
    (("Combien de pattes a une araignée ?", "How many legs does a spider have?"), (("Six", "Six"), ("Dix", "Ten"), ("Huit", "Eight"), ("Quatre", "Four")), 2),
    (("Quelle planète est la plus proche du Soleil ?", "Which planet is the closest to the Sun?"),
     (("Mercure", "Mercury"), ("Saturne", "Saturn"), ("Neptune", "Neptune"), ("Uranus", "Uranus")), 0),
    (("Quelle couleur donnent le bleu et le jaune ?", "What colour do blue and yellow make?"),
     (("Rouge", "Red"), ("Violet", "Purple"), ("Orange", "Orange"), ("Vert", "Green")), 3),
    (("Combien de minutes dans une heure ?", "How many minutes in an hour?"), (("Cent", "A hundred"), ("Soixante", "Sixty"), ("Trente", "Thirty"),
                                                                              ("Douze", "Twelve")), 1),
    (("Lequel de ces animaux est le plus rapide ?", "Which of these animals is the fastest?"),
     (("Le guépard", "The cheetah"), ("L'escargot", "The snail"), ("La tortue", "The tortoise"), ("Le koala", "The koala")), 0),
    (("Où se lève le soleil ?", "Where does the sun rise?"), (("À l'ouest", "In the west"), ("Au nord", "In the north"), ("À l'est", "In the east"),
                                                              ("Au sud", "In the south")), 2),
    (("Combien de joueurs dans une équipe de football ?", "How many players in a football team?"),
     (("Neuf", "Nine"), ("Sept", "Seven"), ("Douze", "Twelve"), ("Onze", "Eleven")), 3),
)


class QuizScene(GameScene):
    """A quiz as in the Neo Geo quizzes: the set at the top with two faces of our own, the question panel below with its
    four answers A B C D, the time that runs, the answer chosen lights up, then a big circle when it is right or a big
    cross when it is wrong. The lives and the score read in the game decide right or wrong. The questions are our own.
    / Un quiz : le décor en haut et deux visages à nous, le panneau de la question et ses quatre réponses, le temps qui
    passe, un grand rond si c'est juste, une grande croix si c'est faux. Les questions sont à nous."""
    THEME = "qz_arena"
    STATIC = True
    SHADE = (40, 0)
    FACES = (((230, 180, 140), (40, 30, 30), (220, 40, 40), None, (60, 80, 160)), ((210, 160, 120), (200, 170, 60), None, None, (160, 60, 80)))
    PANEL = (40, 60, 200)
    QTIME = 6.0

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.q = self.rng.randrange(len(QUESTIONS))
        self.t0 = 0.0
        self.pick = None
        self.verdict = None
        self.asked = 0                                    # (tests)
        self.right = 0
        self.wrong = 0

    def restart(self, vals, now):
        self.t0 = now

    def next_question(self, now):
        self.q = (self.q + 1 + self.rng.randrange(len(QUESTIONS) - 1)) % len(QUESTIONS)
        self.t0, self.pick, self.verdict = now, None, None
        self.asked += 1

    def answer(self, now, good):
        q = QUESTIONS[self.q]
        if self.verdict is not None:
            return
        self.pick = q[2] if good else (q[2] + 1 + self.rng.randrange(3)) % 4
        self.verdict = (now, good)
        if good:
            self.right += 1
        else:
            self.wrong += 1

    def update(self, vals, now):
        if self.t0 == 0.0:
            self.t0 = now
        el = now - self.t0
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:
            self.answer(now, True)
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.answer(now, False)
        if self.verdict is None and el > self.QTIME:
            self.answer(now, self.rng.random() < 0.7)
        if self.verdict is not None and now - self.verdict[0] > 1.6:
            self.next_question(now)

    def draw_faces(self, screen, now):
        S, W = self.S, self.W
        for k, (skin, hair, band, hood, bg) in enumerate(self.FACES):
            x = S(60) if k == 0 else W - S(60) - S(190)
            img = self.img(("qzface", k), S(190), S(220), portrait_draw(skin, hair, band, hood, bg), ss=2)
            screen.blit(img, (int(x), S(30)))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        self.draw_faces(screen, now)
        lang = 0 if tr("fr", "en") == "fr" else 1
        qtext, answers, good = QUESTIONS[self.q]
        py = S(QZ_PANEL)
        pg.draw.rect(screen, self.PANEL, (S(40), py + S(6), W - S(80), S(60)), border_radius=S(8))     # la question
        pg.draw.rect(screen, (250, 250, 250), (S(40), py + S(6), W - S(80), S(60)), max(1, S(3)), border_radius=S(8))
        self.text(screen, "Q", S(70), py + S(36), 34, (255, 230, 60), key="black", valign="middle")
        self.text(screen, qtext[lang], S(120), py + S(36), 32, WHITE, key="xbold", valign="middle", glow=0)
        for i, ans in enumerate(answers):                                   # les quatre réponses
            x = S(40) + (i % 2) * (W - S(80)) / 2
            y = py + S(76) + (i // 2) * S(56)
            lit = self.pick == i
            col = (250, 210, 60) if lit else self.PANEL
            pg.draw.rect(screen, col, (int(x), int(y), int((W - S(80)) / 2 - S(10)), S(50)), border_radius=S(8))
            pg.draw.rect(screen, (250, 250, 250), (int(x), int(y), int((W - S(80)) / 2 - S(10)), S(50)), max(1, S(2)), border_radius=S(8))
            self.text(screen, "ABCD"[i], x + S(28), y + S(25), 30, (250, 80, 80), key="black", valign="middle")
            self.text(screen, ans[lang], x + S(70), y + S(25), 28, (30, 30, 40) if lit else WHITE, key="xbold", valign="middle", glow=0)
            if self.verdict is not None and lit:                            # a mark on the answer, a big one in the middle / une marque sur la réponse, une grande au milieu
                bx, by = x + (W - S(80)) / 2 - S(44), y + S(25)
                for cx, my, r, wd in ((bx, by, S(17), max(2, S(5))), (W / 2, S(176), S(70), max(2, S(14)))):
                    if self.verdict[1]:
                        pg.draw.circle(screen, (240, 50, 50), (int(cx), int(my)), r, wd)
                    else:
                        d = r * 0.86
                        for a in (1, -1):
                            pg.draw.line(screen, (60, 120, 250), (int(cx - d), int(my - a * d)), (int(cx + d), int(my + a * d)), wd + max(1, S(2)))
        if self.verdict is None:                                            # le temps qui reste
            left = max(0.0, self.QTIME - (now - self.t0))
            self.label(screen, f"TIME {int(math.ceil(left))}", W / 2, py - S(30), 34, (255, 230, 60), key="black", align="center")
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(440), S(84), now)
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        self.pill(screen, S(300), S(110), S(330), S(56), 170, radius=12)
        self.text(screen, "P1", S(318), S(138), 26, P1C, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            self.hd._score(screen, eng, "score", S(616), S(114), "right", S(40))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.pill(screen, S(300), S(172), S(330), S(44), 150, radius=12)
            self.text(screen, "LIFE", S(318), S(194), 20, (255, 120, 120), key="black", valign="middle", glow=0)
            for k in range(int(min(lives, 6))):
                cx, cy = S(400) + k * S(34), S(194)
                pg.draw.circle(screen, (240, 50, 70), (int(cx - S(7)), int(cy - S(4))), S(9))
                pg.draw.circle(screen, (240, 50, 70), (int(cx + S(7)), int(cy - S(4))), S(9))
                pg.draw.polygon(screen, (240, 50, 70), [(int(cx - S(15)), int(cy)), (int(cx + S(15)), int(cy)), (int(cx), int(cy + S(15)))])
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(470), S(246), 28, col, align="center")       # under the set / sous le décor


class QuizKOFScene(QuizScene):
    """Quiz King of Fighters as in the game: a stage in the city at night, two fighters of our own face to face, the
    question panel and its four answers. / Une scène dans la ville la nuit, deux combattants à nous face à face."""
    THEME = "qz_arena"
    FACES = (((230, 180, 140), (40, 30, 30), (220, 40, 40), None, (60, 80, 160)), ((210, 160, 120), (240, 220, 200), (40, 40, 40), None, (160, 60, 80)))


class QuizDaisousaScene(QuizScene):
    """Quiz Daisousa Sen as in the game: the wire fence in front of the city at dusk, a detective of our own in his cap,
    the question panel. / Le grillage devant la ville au crépuscule, un détective à nous et sa casquette."""
    THEME = "qz_fence"
    FACES = (((220, 170, 120), (60, 50, 40), None, (60, 120, 100), (90, 110, 90)), ((230, 190, 150), (30, 30, 30), None, None, (80, 80, 120)))


class QuizMeitanteiScene(QuizScene):
    """Quiz Meitantei Neo & Geo as in the game: a detective's office, its shelves and its window, an old detective of
    our own and his young assistant. / Le bureau d'un détective, un vieux détective à nous et son jeune assistant."""
    THEME = "qz_office"
    FACES = (((230, 190, 160), (220, 220, 220), None, None, (110, 70, 50)), ((220, 170, 130), (40, 30, 30), None, None, (60, 100, 140)))


class DeluxeQuizScene(QuizScene):
    """The Deluxe Quiz as in the game: a television studio, its lights and its rainbow, two children of our own on the
    set. / Un studio de télévision, ses projecteurs et son arc-en-ciel, deux enfants à nous sur le plateau."""
    THEME = "qz_studio"
    PANEL = (90, 40, 120)
    FACES = (((250, 210, 180), (40, 30, 30), (250, 120, 160), None, (250, 200, 80)), ((250, 210, 180), (120, 70, 40), None, None, (120, 200, 250)))


# ============================================================================ mahjong
def tile_draw(kind, n, back=None):
    """A mahjong tile of our own: dots, bamboo, numbers in red, winds and dragons as plain marks, or its back in its
    colour. / Une tuile de mahjong à nous : ronds, bambous, chiffres rouges, vents et dragons en signes simples, ou son dos."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.05))
        if back is not None:
            d.rounded_rectangle([0, 0, W - 1, H - 1], radius=W * 0.14, fill=back + (255,), outline=DARKLINE, width=ow)
            d.rounded_rectangle([W * 0.1, H * 0.06, W * 0.9, H * 0.2], radius=W * 0.05, fill=_mixc(back, (255, 255, 255), 0.3))
            return
        d.rounded_rectangle([0, H * 0.06, W - 1, H - 1], radius=W * 0.14, fill=(220, 200, 150, 255), outline=DARKLINE, width=ow)
        d.rounded_rectangle([0, 0, W - 1, H * 0.92], radius=W * 0.14, fill=(250, 248, 236, 255), outline=DARKLINE, width=ow)
        if kind == 0:                                                       # ronds / dots
            cols = ((40, 90, 200), (220, 50, 50), (40, 150, 70))
            pos = [(0.5, 0.46)] if n == 1 else [((0.3 + 0.4 * (i % 2)), 0.2 + 0.52 * (i // 2) / max(1, (n - 1) // 2)) for i in range(n)]
            for i, (px, py) in enumerate(pos[:9]):
                r = W * (0.24 if n == 1 else 0.13)
                d.ellipse([W * px - r, H * py - r, W * px + r, H * py + r], fill=cols[i % 3] + (255,), outline=DARKLINE)
        elif kind == 1:                                                     # bambous / bamboo
            for i in range(n):
                x = W * (0.2 + 0.6 * ((i % 3) / 2.0))
                y = H * (0.14 + 0.3 * (i // 3))
                d.rounded_rectangle([x - W * 0.06, y, x + W * 0.06, y + H * 0.24], radius=W * 0.04, fill=(40, 150, 70, 255), outline=DARKLINE)
        elif kind == 2:                                                     # chiffres / numbers (the number is written by the scene)
            d.rectangle([W * 0.26, H * 0.56, W * 0.74, H * 0.8], fill=(200, 40, 40, 255))
        else:                                                               # vents et dragons / winds and dragons
            if n < 4:
                pass                                                         # the wind letter is written by the scene
            elif n == 4:
                d.rectangle([W * 0.24, H * 0.2, W * 0.76, H * 0.72], outline=(220, 40, 40, 255), width=max(2, int(W * 0.08)))
            elif n == 5:
                d.ellipse([W * 0.2, H * 0.2, W * 0.8, H * 0.72], fill=(40, 150, 70, 255))
            else:
                d.rectangle([W * 0.2, H * 0.18, W * 0.8, H * 0.74], outline=(40, 90, 200, 255), width=max(2, int(W * 0.06)))
    return fn


class MahjongScene(GameScene):
    """A game of mahjong as in the Neo Geo mahjong games: the felt of the table, the hidden hand of the opponent at the
    top, the tiles thrown in the middle, our hand of thirteen tiles at the bottom; a tile is drawn, a tile is thrown,
    and now and then a hand wins. The points and the time read in the game where they are known.
    / Une partie de mahjong : le tapis, la main cachée de l'adversaire en haut, les tuiles jetées au milieu, notre main de
    treize tuiles en bas ; une tuile est piochée, une tuile est jetée, et de temps en temps une main gagne."""
    THEME = "mj_green"
    STATIC = True
    SHADE = (0, 0)
    BACK = (240, 180, 40)
    TW, TH = 54, 74

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.deal(0.0)
        self.points = [25000, 25000]
        self.wins = 0                                     # (tests)
        self.throws = 0

    def tile(self):
        r = self.rng.random()
        if r < 0.27:
            return (0, self.rng.randint(1, 9))
        if r < 0.54:
            return (1, self.rng.randint(1, 9))
        if r < 0.8:
            return (2, self.rng.randint(1, 9))
        return (3, self.rng.randrange(7))

    def deal(self, now):
        self.hand = sorted(self.tile() for _ in range(13))
        self.river = [[], []]
        self.drawn = None
        self.turn = 0
        self.next_t = now + 0.8
        self.fly = None

    def timg(self, t, scale=1.0):
        S = self.S
        w, h = int(S(self.TW) * scale), int(S(self.TH) * scale)
        if t is None:
            return self.img(("mjback", w), w, h, tile_draw(0, 0, self.BACK), ss=2)
        kind, n = t
        key = ("mjtile", kind, n, w)
        s = self.imgs.get(key)
        if s is None:
            hd = self.hd
            font = hd.font("black", max(8, int(h * 2 * 0.42)))

            def fn(d, W, H):
                tile_draw(kind, n)(d, W, H)
                if kind == 2:
                    d.text((W * 0.5, H * 0.3), str(n), font=font, fill=(30, 30, 40, 255), anchor="mm")
                elif kind == 3 and n < 4:
                    d.rectangle([W * 0.15, H * 0.15, W * 0.85, H * 0.8], fill=(250, 248, 236, 255))
                    d.text((W * 0.5, H * 0.46), "ESWN"[n], font=font, fill=(30, 30, 60, 255), anchor="mm")
            s = self.img(key, w, h, fn, ss=2)
        return s

    def update(self, vals, now):
        if now < self.next_t:
            return
        self.next_t = now + 0.7
        if self.turn == 0:                                                  # we draw, then throw / on pioche puis on jette
            if self.drawn is None:
                self.drawn = self.tile()
                return
            i = self.rng.randrange(14)
            hand = self.hand + [self.drawn]
            out = hand.pop(i)
            self.hand = sorted(hand)
            self.drawn = None
            self.river[0].append(out)
            self.throws += 1
        else:
            self.river[1].append(self.tile())
            self.throws += 1
        self.turn = 1 - self.turn
        if sum(len(r) for r in self.river) >= 20 or (self.throws > 6 and self.rng.random() < 0.06):
            self.win(now, self.rng.random() < 0.6)

    def win(self, now, ours):
        """A hand wins: RON or TSUMO and the points. / Une main gagne : RON ou TSUMO et les points."""
        self.wins += 1
        pts = self.rng.choice((1000, 2000, 3900, 8000, 12000))
        self.points[0 if ours else 1] += pts
        self.points[1 if ours else 0] -= pts
        self.slam(self.rng.choice(("RON!", "TSUMO!")), GOLD if ours else (120, 200, 255), now, 1.4, sub=f"{pts} P")
        self.next_t = now + 1.8
        self.fx.later(1.7, self.deal, now)

    def draw_table(self, screen, vals, now):
        S, W, H = self.S, self.W, self.H
        back = self.timg(None, 0.8)                                         # la main de l'adversaire
        x0 = W / 2 - 13 * back.get_width() / 2
        for i in range(13):
            screen.blit(back, (int(x0 + i * back.get_width()), S(20)))
        for side, row_y in ((1, S(130)), (0, S(214))):                      # les tuiles jetées
            tiles = self.river[side]
            for i, t in enumerate(tiles[-14:]):
                img = self.timg(t, 0.62)
                screen.blit(img, (int(W / 2 - 7 * img.get_width() + i * img.get_width()), int(row_y)))
        tw = S(self.TW)
        x0 = W / 2 - 14 * tw / 2                                             # notre main
        for i, t in enumerate(self.hand):
            img = self.timg(t)
            screen.blit(img, (int(x0 + i * tw), int(H - img.get_height() - S(12))))
        if self.drawn is not None:
            img = self.timg(self.drawn)
            screen.blit(img, (int(x0 + 13 * tw + S(14)), int(H - img.get_height() - S(22))))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        self.draw_table(screen, vals, now)
        self.hd.draw_logo(screen, logo, S(220), S(24), S(380), S(76), now)
        for k, (lab, y) in enumerate((("CPU", S(130)), ("P1", S(214)))):     # les points
            self.box(screen, W - S(320), y, S(280), S(64), (250, 200, 80), fill=(10, 10, 20, 220), radius=8, width=3)
            self.text(screen, lab, W - S(300), y + S(32), 22, (250, 200, 80), key="black", valign="middle", glow=0)
            self.hd.put_number(screen, f"{self.points[1 - k]}P", "black", S(36), WHITE, W - S(56), y + S(32), "right", "middle")
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        S = self.S
        t = _n(vals.get("time"))
        if t is not None:
            self.label(screen, tr(f"TEMPS {int(t)}", f"TIME {int(t)}"), S(220), S(150), 26, (255, 230, 120), align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, S(220), S(210), 26, col, align="center")


class MahjongKyoScene(MahjongScene):
    """Mahjong Kyo Retsuden as in the game: the green felt, the yellow tile backs, the point boxes on the right.
    / Le tapis vert, les dos de tuiles jaunes, les cases des points à droite, comme dans le jeu."""
    THEME = "mj_green"
    BACK = (240, 190, 40)


class JanshinScene(MahjongScene):
    """Janshin Densetsu as in the game: the purple felt, the green tile backs, the panel of the hero with HP, MP, WEAPON
    and SHIELD read in the game. / Le tapis violet, les dos verts, le panneau du héros avec HP, MP, WEAPON et SHIELD."""
    THEME = "mj_purple"
    BACK = (50, 150, 120)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.hits = 0                                     # (tests)

    def update(self, vals, now):
        ch = self.changed(vals, "hp")                                       # HP that drops / les HP qui baissent
        if ch and ch[1] < ch[0]:
            self.hits += 1
            self.popup(f"HP -{int(ch[0] - ch[1])}", self.S(470), self.S(330), (255, 90, 70), 30)
            self.fx.shake(6, 0.3)
        super().update(vals, now)

    def status(self, screen, eng, vals, logo, now):
        S = self.S
        rows = [(lab, _n(vals.get(name))) for lab, name in (("HP", "hp"), ("MP", "mp"), ("WEAPON", "weapon"), ("SHIELD", "shield"))]
        rows = [(lab, v) for lab, v in rows if v is not None]
        if rows:
            self.box(screen, S(40), S(238), S(330), S(34) * len(rows) + S(20), (220, 170, 90), fill=(60, 40, 30, 230), radius=8, width=3)
            for k, (lab, v) in enumerate(rows):
                y = S(262) + k * S(34)
                self.text(screen, lab, S(60), y, 22, (250, 220, 150), key="black", valign="middle", glow=0)
                self.text(screen, f"{int(v)}", S(350), y, 24, WHITE, key="black", align="right", valign="middle", glow=0)
        super().status(screen, eng, vals, logo, now)


class BakatonoScene(MahjongScene):
    """Bakatonosama Mahjong Manyuuki as in the game: the olive felt, the orange tile backs. / Le tapis olive, les dos
    de tuiles orange, comme dans le jeu."""
    THEME = "mj_olive"
    BACK = (240, 150, 40)


class FinalRomanceScene(MahjongScene):
    """Idol Mahjong Final Romance 2 as in the game: the green felt in its wooden frame, the orange tile backs.
    / Le tapis vert dans son cadre de bois, les dos de tuiles orange, comme dans le jeu."""
    THEME = "mj_wood"
    BACK = (240, 120, 40)


class MinasanScene(MahjongScene):
    """Minasan no Okagesamadesu! as in the game: the blue table and its mahjong game, and the board game it is part of:
    the steps read in the game roll a die. / La table bleue et sa partie de mahjong, et le jeu de plateau : les pas lus
    dans le jeu lancent un dé, comme dans le jeu."""
    THEME = "mj_blue"
    BACK = (240, 200, 60)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.die = (1, -9.0)
        self.rolls = 0                                    # (tests)

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "steps")
        if ch and ch[1] > 0:
            self.die = (int(ch[1]), now)
            self.rolls += 1
            self.popup(tr(f"{int(ch[1])} PAS", f"{int(ch[1])} STEPS"), self.S(270), self.S(330), GOLD, 36)

    def status(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        n, t0 = self.die
        k = now - t0
        face = n if k > 0.8 else 1 + int(now * 20) % 6
        cx, cy, r = S(120), S(300), S(44)
        ang = (1 - _clamp(k / 0.8)) * 360 * 2
        sq = self.imgs.get("mndie")
        if sq is None:
            sq = self.imgs["mndie"] = pg.Surface((2 * r, 2 * r), pg.SRCALPHA)
        sq.fill((0, 0, 0, 0))
        pg.draw.rect(sq, (250, 250, 250), (0, 0, 2 * r, 2 * r), border_radius=S(14))
        pg.draw.rect(sq, (40, 40, 40), (0, 0, 2 * r, 2 * r), max(1, S(3)), border_radius=S(14))
        pips = {1: ((1, 1),), 2: ((0, 0), (2, 2)), 3: ((0, 0), (1, 1), (2, 2)), 4: ((0, 0), (2, 0), (0, 2), (2, 2)),
                5: ((0, 0), (2, 0), (1, 1), (0, 2), (2, 2)), 6: ((0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2))}
        for px, py in pips[max(1, min(6, face))]:
            pg.draw.circle(sq, (200, 30, 30) if face == 1 else (30, 30, 30), (int(r * 0.45 + px * r * 0.55), int(r * 0.45 + py * r * 0.55)), S(7))
        rot = pg.transform.rotozoom(sq, ang, 1.0) if ang else sq
        screen.blit(rot, (int(cx - rot.get_width() / 2), int(cy - rot.get_height() / 2)))
        super().status(screen, eng, vals, logo, now)


# ============================================================================ Shogi no Tatsujin
SH_START = ("LNSGKGSNL", ".R.....B.", "PPPPPPPPP", ".........", ".........", ".........", "ppppppppp", ".b.....r.", "lnsgkgsnl")


def shogi_piece_draw(letter, ours, promoted=False):
    """A shogi piece of our own: the pentagon of wood and its letter (K, R, B, G, S, N, L, P), red when promoted.
    / Une pièce de shogi à nous : le pentagone de bois et sa lettre, rouge quand elle est promue."""
    def fn(d, W, H):
        pts = [(W * 0.5, H * 0.04), (W * 0.84, H * 0.22), (W * 0.94, H * 0.96), (W * 0.06, H * 0.96), (W * 0.16, H * 0.22)]
        if not ours:
            pts = [(x, H - y) for x, y in pts]
        d.polygon(pts, fill=(240, 210, 150, 255), outline=(90, 60, 30, 255))
    return fn


class ShogiScene(GameScene):
    """Shogi no Tatsujin as in the game: the rocky coast by the sea, the wooden board and its two stands; the pieces of
    our own move one by one, a piece taken goes to the stand of the one who took it, each player's clock runs.
    / La côte rocheuse, le plateau de bois et ses deux supports ; nos pièces avancent une à une, une pièce prise va sur
    le support de celui qui l'a prise, la pendule de chaque joueur tourne, comme dans le jeu."""
    THEME = "sh_coast"
    STATIC = True
    SHADE = (0, 0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.reset(0.0)
        self.moves = 0                                    # (tests)
        self.captures = 0

    def reset(self, now):
        self.board = {}
        for r, row in enumerate(SH_START):
            for c, ch in enumerate(row):
                if ch != ".":
                    self.board[(c, r)] = (ch.upper(), ch.isupper())          # majuscules : l'adversaire en haut
        self.hands = {True: [], False: []}
        self.side = False                                                    # False: us, at the bottom / nous, en bas
        self.next_t = now + 1.0
        self.moved = None
        self.clock = [0.0, 0.0]

    def cell_xy(self, c, r):
        S = self.S
        C = S(SH_CELL)
        return S(SH_X0) + (c + 0.5) * C, S(SH_Y0) + (r + 0.5) * C

    def update(self, vals, now):
        self.clock[0 if not self.side else 1] += self.dt
        if now < self.next_t:
            return
        self.next_t = now + self.rng.uniform(1.0, 1.8)
        d = -1 if not self.side else 1                                       # forward / en avant
        mine = [(pos, p) for pos, p in self.board.items() if p[1] == self.side]
        self.rng.shuffle(mine)
        moves = []
        for (c, r), (letter, top) in mine:
            steps = [(0, d)] if letter in "PL" else ([(0, d), (1, d), (-1, d)] if letter in "SGK" else [(0, d), (1, 0), (-1, 0), (0, d * 2)])
            if letter == "N":
                steps = [(1, 2 * d), (-1, 2 * d)]
            for dc, dr in steps:
                nc, nr = c + dc, r + dr
                if 0 <= nc < 9 and 0 <= nr < 9 and (self.board.get((nc, nr)) or (None, None))[1] != self.side:
                    moves.append(((c, r), letter, (nc, nr)))
        takes = [m for m in moves if m[2] in self.board]
        if takes and self.rng.random() < 0.8:                               # a piece to take is taken / une prise d'abord
            moves = takes
        if not moves:
            self.side = not self.side
            return
        (c, r), letter, (nc, nr) = moves[0]
        tgt = self.board.get((nc, nr))
        if tgt is not None:
            self.hands[self.side].append(tgt[0])
            self.captures += 1
            x, y = self.cell_xy(nc, nr)
            self.fx.sparks(x, y, 10, (255, 230, 150), (150, 400), (0, 360), (0.2, 0.4), 200, "front", 3, 10)
        del self.board[(c, r)]
        self.board[(nc, nr)] = (letter, self.side)
        self.moved = ((c, r), (nc, nr), now)
        self.moves += 1
        self.side = not self.side
        if tgt is not None and tgt[0] == "K":                                 # the king is taken, a new game / le roi est pris
            self.slam(tr("ÉCHEC ET MAT", "CHECKMATE"), GOLD, now, 1.6)
            self.next_t = now + 99.0
            self.fx.later(1.8, self.reset, now + 1.8)
        elif self.moves % 120 == 0:
            self.reset(now)

    def pimg(self, letter, top):
        S = self.S
        key = ("shpiece", letter, top)
        s = self.imgs.get(key)
        if s is None:
            font = self.hd.font("black", max(8, int(S(SH_CELL) * 2 * 0.5)))

            def fn(d, W, H):
                shogi_piece_draw(letter, not top)(d, W, H)
                d.text((W * 0.5, H * (0.58 if not top else 0.44)), letter, font=font, fill=(30, 20, 20, 255), anchor="mm")
            s = self.img(key, S(SH_CELL) - S(4), S(SH_CELL) - S(2), fn, ss=2)
            if top:
                s = self.pg.transform.rotate(s, 180)
                self.imgs[key] = s
        return s

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        moving = self.moved if self.moved and now - self.moved[2] < 0.3 else None
        for (c, r), (letter, top) in self.board.items():
            x, y = self.cell_xy(c, r)
            if moving and (c, r) == moving[1]:
                k = (now - moving[2]) / 0.3
                x0, y0 = self.cell_xy(*moving[0])
                x, y = x0 + (x - x0) * k, y0 + (y - y0) * k
            img = self.pimg(letter, top)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        if self.moved:                                                         # the last move / le dernier coup
            x, y = self.cell_xy(*self.moved[1])
            C = S(SH_CELL)
            pg.draw.rect(screen, (255, 80, 60), (int(x - C / 2), int(y - C / 2), C, C), max(1, S(3)))
        for top, (sx, sy) in ((True, (S(SH_X0) - S(230), S(SH_Y0))), (False, (S(SH_X0) + S(9 * SH_CELL) + S(40), S(SH_Y0) + S(9 * SH_CELL) - S(200)))):
            for i, letter in enumerate(self.hands[top][:12]):                 # the pieces taken, on the stand of the taker / les pièces prises
                img = self.pimg(letter, top)
                screen.blit(img, (int(sx + S(8) + (i % 4) * S(45)), int(sy + S(8) + (i // 4) * S(48))))
        self.hd.draw_logo(screen, logo, S(260), S(10), S(400), S(80), now)
        for k, (lab, x, y) in enumerate(((tr("ADVERSAIRE", "OPPONENT"), S(SH_X0) - S(135), S(SH_Y0) + S(228)),
                                         (tr("VOUS", "YOU"), S(SH_X0) + S(9 * SH_CELL) + S(135), S(SH_Y0) + S(9 * SH_CELL) - S(228)))):
            t = self.clock[1 - k]
            self.label(screen, f"{lab} {int(t) // 60}:{int(t) % 60:02d}", x, y, 22, CREAM, align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(200), S(300), 26, col, align="center")


SCENES = {"nitd": NightmareScene, "superspy": SuperSpyScene, "quizkof": QuizKOFScene, "quizdais": QuizDaisousaScene, "quizdai2": QuizMeitanteiScene,
          "marukodq": DeluxeQuizScene, "minasan": MinasanScene, "mahretsu": MahjongKyoScene, "janshin": JanshinScene, "bakatono": BakatonoScene,
          "froman2b": FinalRomanceScene, "moshougi": ShogiScene}
