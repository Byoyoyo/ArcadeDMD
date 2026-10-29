"""HD scenes of the Capcom CPS action, platform and puzzle games (1.30), each drawn after screenshots of its game:
Ghouls'n Ghosts, Strider, Mega Twins, Magic Sword, Willow, Nemo, Three Wonders, Dynasty Wars, Pang! 3, Mighty! Pang,
Super Puzzle Fighter II Turbo, Puzz Loop 2, Capcom Sports Club, Quiz & Dragons, Capcom World 2 and the others. Each game
has its own animated backdrop and reacts to the values read in its memory. The heroes, the enemies and the machines are
creations of the program in the spirit of the games, no picture comes from a game.

Scènes HD des jeux d'action, de plateforme et de réflexion Capcom CPS (1.30), chacune dessinée d'après des captures de
son jeu. Les héros, les ennemis et les machines sont des créations du programme dans l'esprit des jeux, aucune image
ne vient d'un jeu.
"""

import math

from .hd_games import AMBER, GOLD, P1C, P2C, WHITE, GameScene, _clamp, _mix, _n, draw_img
from .hd_games3 import _capsule
from .hd_games5 import fighter_draw
from .hd_themes14 import GG_FLOOR, MS_FLOOR, MT_FLOOR, PG_FLOOR, SPF_CELL, SPF_COLS, SPF_ROWS, SPF_TOP, ST_FLOOR
from .i18n import tr

DARKLINE = (24, 20, 26, 255)
SKIN = (240, 196, 160)


def _c(col, a=255):
    return tuple(col[:3]) + (a,)


# ============================================================================ the side-scrolling base / la base
class SideQuestScene(GameScene):
    """A side-scrolling action game: our hero walks to the right through the place of the game, the enemies come from
    the right (some on the ground, some flying), he strikes or throws at the nearest one. The points read in the game
    make an enemy fall, the health that goes down is a blow taken, a life lost a fall. Each game gives its hero, its
    enemies, what the hero throws and its top bar.
    / Un jeu d'action à défilement : notre héros avance vers la droite, les ennemis arrivent de la droite, à terre ou
    en vol, il frappe ou lance sur le plus proche. Chaque jeu donne son héros, ses ennemis, son arme et sa barre du haut."""
    FLOOR = 380                    # where the feet are, at s = 1 / où sont les pieds
    HERO_X = 0.3
    HERO = (150, 190)              # size of the hero's picture / taille de l'image du héros
    FOE = (130, 170)
    FLYER = (110, 80)
    FLY_Y = (170, 260)             # height of the flying enemies / hauteur des ennemis volants
    FLYERS = 0.35                  # share of flying enemies / part d'ennemis volants
    SHOT = "throw"                 # "throw" (a thing flies straight) or "slash" (a blow in front) / lancer ou frapper
    REACH = 0.62                   # how far the hero strikes, in screen widths / portée
    PACE = (1.1, 2.4)              # time between two enemies / temps entre deux ennemis
    MOVE = (0.4, 1.4)              # speed of the backdrop: nobody plays, playing / vitesse du décor
    HEALTH = "health"
    HEALTH_MAX = 100.0
    POINTS = ("100", "200", "500")
    SHADE = (90, 70)
    EXPLOSIONS = False

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.foes = []
        self.shots = []
        self.next_foe = 0.0
        self.strike = -99.0
        self.hurt = -99.0
        self.jump = None
        self.kills = 0                                    # (tests)
        self.blows = 0
        self.falls = 0
        self.warm = [(self.hero_img, (f,)) for f in range(4)] + [(self.foe_img, (k, f)) for k in range(2) for f in range(2)] + self.warm

    # ---------------------------------------------------------------- given by each game / donné par chaque jeu
    def hero_draw(self, frame):
        return fighter_draw("jacket", (60, 90, 160), (40, 40, 60), SKIN, (60, 40, 30), min(frame, 3))

    def foe_draw(self, kind, frame):
        return fighter_draw("thug", (90, 90, 100), (40, 40, 50), (200, 160, 120), (30, 30, 30), 1 + frame % 2)

    def shot_draw(self):
        def fn(d, W, H):
            d.ellipse([0, 0, W, H], fill=(255, 240, 160, 255))
        return fn

    def shot_size(self):
        return (60, 24)

    def status(self, screen, eng, vals, logo, now):
        self.top_bar(screen, eng, vals, logo, now)

    # ---------------------------------------------------------------- pictures / images
    def hero_img(self, frame):
        S = self.S
        return self.img(("sq_hero", self.hero_key(), frame), S(self.HERO[0]), S(self.HERO[1]), self.hero_draw(frame), ss=2)

    def hero_key(self):
        return 0

    def foe_img(self, kind, frame, left=True):
        S = self.S
        w, h = self.FLYER if kind == 1 else self.FOE
        return self.img(("sq_foe", kind, frame, left), S(w), S(h), self.foe_draw(kind, frame), ss=2, flip=left)

    def shot_img(self):
        S = self.S
        w, h = self.shot_size()
        return self.img(("sq_shot", self.shot_key()), S(w), S(h), self.shot_draw(), ss=2)

    def shot_key(self):
        return 0

    # ---------------------------------------------------------------- life / vie de la scène
    def floor(self):
        return self.S(self.FLOOR)

    def hero_xy(self, now):
        x, y = self.W * self.HERO_X, self.floor()
        if self.jump is not None:
            k = (now - self.jump) / 0.7
            if k >= 1:
                self.jump = None
            else:
                y -= math.sin(k * math.pi) * self.S(150)
        return x, y

    def move(self, vals, now, idle):
        return self.MOVE[0] if idle else self.MOVE[1]

    def restart(self, vals, now):
        self.foes, self.shots = [], []
        self.next_foe = now + 0.8

    def kill(self, f, now, points=None):
        if f.get("dead"):
            return
        f["dead"] = now
        self.kills += 1
        y = f["y"] - self.S(self.FOE[1] * 0.45 if f["kind"] == 0 else self.FLYER[1] * 0.5)
        self.fx.sparks(f["x"], y, 14, (255, 230, 150), (200, 600), (0, 360), (0.2, 0.5), 600, "front", 4, 16)
        self.fx.glow(f["x"], y, 20, 90, (255, 220, 140), 0.3, "front", 0.9, 0.0)
        self.popup(points or self.rng.choice(self.POINTS), f["x"], y - self.S(60), GOLD, 30)

    def attack(self, f, now):
        """The hero strikes or throws at f. / Le héros frappe ou lance sur f."""
        self.strike = now
        hx, hy = self.hero_xy(now)
        if self.SHOT == "slash":
            self.slash_fx(hx, hy, now)
            f["hp"] -= 2
            if f["hp"] <= 0:
                self.kill(f, now)
            return
        y = hy - self.S(self.HERO[1] * 0.55)
        self.shots.append({"x": hx + self.S(50), "y": y, "vx": self.S(1500), "t0": now})

    def slash_fx(self, hx, hy, now):
        S = self.S
        self.fx.glow(hx + S(110), hy - S(100), 30, 120, (160, 220, 255), 0.25, "front", 1.0, 0.0)

    def update(self, vals, now):
        S, rng, W = self.S, self.rng, self.W
        ch = self.changed(vals, self.HEALTH)
        if ch and ch[1] < ch[0]:                                       # a blow taken / un coup reçu
            self.hurt = now
            self.blows += 1
            hx, hy = self.hero_xy(now)
            self.fx.sparks(hx, hy - S(110), 10, (255, 120, 90), (200, 500), (180, 360), (0.2, 0.4), 700, "front", 4, 12)
            self.popup(f"-{max(1, int(round((ch[0] - ch[1]) * 100.0 / self.HEALTH_MAX)))}%", hx, hy - S(230), (255, 100, 80), 30)
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.fall(now)
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:
            live = [f for f in self.foes if not f.get("dead") and 0 < f["x"] < W]
            if live:
                self.kill(min(live, key=lambda f: f["x"]), now, str(int(ch[1] - ch[0])) if ch[1] - ch[0] < 100000 else None)
        if now >= self.next_foe and len([f for f in self.foes if not f.get("dead")]) < 5:
            self.next_foe = now + rng.uniform(*self.PACE)
            fly = rng.random() < self.FLYERS
            self.foes.append({"x": W + S(80), "y": S(rng.uniform(*self.FLY_Y)) if fly else self.floor(), "kind": 1 if fly else 0,
                              "v": rng.uniform(90, 160) * self.s * (1.6 if fly else 1.0), "ph": rng.uniform(0, 6), "hp": 2, "born": now})
        hx, hy = self.hero_xy(now)
        target = [f for f in self.foes if not f.get("dead") and hx + S(60) < f["x"] < hx + W * self.REACH]
        if target and now - self.strike > 0.75:
            self.attack(min(target, key=lambda f: f["x"]), now)
        flyers = [f for f in self.foes if not f.get("dead") and f["kind"] == 1 and abs(f["x"] - hx) < S(260)]
        if flyers and self.jump is None and rng.random() < 0.02:
            self.jump = now
        self.more(vals, now)

    def more(self, vals, now):
        """What a game adds to update. / Ce qu'un jeu ajoute."""

    def fall(self, now):
        hx, hy = self.hero_xy(now)
        self.falls += 1
        self.hurt = now
        self.fx.explosion(hx, hy - self.S(90), 0.7, False)
        self.popup(tr("-1 VIE", "-1 LIFE"), hx, hy - self.S(240), (255, 90, 70), 38)

    # ---------------------------------------------------------------- drawing / dessin
    def draw_foes(self, screen, now):
        S, dt = self.S, self.dt
        keep = []
        hx = self.W * self.HERO_X
        for f in self.foes:
            if f.get("dead") and now - f["dead"] > 0.35:
                continue
            if not f.get("dead") and (f["x"] > hx + S(120) or f["kind"] == 1):
                # it walks and the ground scrolls, at the hero it stands up to him / il marche et le sol défile, puis il fait face au héros
                f["x"] -= (f["v"] + self.bd.speed * (0.5 if f["kind"] == 1 else 1.0)) * dt
            if f["x"] < -S(150):
                continue
            keep.append(f)
            if f.get("dead") and int(now * 20) % 2:
                continue
            img = self.foe_img(f["kind"], int(now * 4 + f["ph"]) % 2)
            y = f["y"] + (math.sin(now * 3 + f["ph"]) * S(18) if f["kind"] == 1 else 0)
            self.blit_foe(screen, f, img, y, now)
        self.foes = keep

    def blit_foe(self, screen, f, img, y, now):
        if f["kind"] == 1:
            screen.blit(img, (int(f["x"] - img.get_width() / 2), int(y - img.get_height() / 2)))
        else:
            screen.blit(img, (int(f["x"] - img.get_width() / 2), int(y - img.get_height())))

    def draw_shots(self, screen, now):
        S, dt = self.S, self.dt
        keep = []
        img = self.shot_img()
        for sh in self.shots:
            sh["x"] += sh["vx"] * dt
            hit = None
            for f in self.foes:
                if f.get("dead"):
                    continue
                fy = f["y"] - (S(self.FOE[1] * 0.5) if f["kind"] == 0 else 0)
                if abs(f["x"] - sh["x"]) < S(60) and abs(fy - sh["y"]) < S(110):
                    hit = f
                    break
            if hit is not None:
                hit["hp"] -= 1
                self.fx.sparks(sh["x"], sh["y"], 6, (255, 240, 200), (150, 400), (120, 240), (0.15, 0.3), 500, "front", 3, 10)
                if hit["hp"] <= 0:
                    self.kill(hit, now)
                continue
            if sh["x"] > self.W + S(80):
                continue
            keep.append(sh)
            self.blit_shot(screen, sh, img, now)
        self.shots = keep

    def blit_shot(self, screen, sh, img, now):
        screen.blit(img, (int(sh["x"] - img.get_width() / 2), int(sh["y"] - img.get_height() / 2)))

    def draw_hero(self, screen, vals, now):
        if not self.p1_in(vals):
            return
        hx, hy = self.hero_xy(now)
        frame = 3 if now - self.strike < 0.22 else 1 + int(now * 6) % 2
        img = self.hero_img(frame)
        if now - self.hurt < 0.9 and int(now * 16) % 2:                # blinks when hit / clignote quand il est touché
            return
        screen.blit(img, (int(hx - img.get_width() / 2), int(hy - img.get_height())))

    def draw_hud(self, screen, eng, vals, logo, now):
        self.draw_foes(screen, now)
        self.draw_shots(screen, now)
        self.draw_hero(screen, vals, now)
        self.status(screen, eng, vals, logo, now)

    # ---------------------------------------------------------------- top bar helpers / barre du haut
    def side_score(self, screen, eng, vals, label, x, y, col, name="score", align="left", size=40):
        """A label and the score under it, as the arcade games show them. / Une étiquette et le score dessous."""
        S, hd = self.S, self.hd
        w = S(300)
        x0 = x if align == "left" else x - w
        self.pill(screen, x0, y, w, S(92), 150, radius=14)
        self.text(screen, label, x0 + S(18), y + S(24), 24, col, key="black", valign="middle")
        if _n(vals.get(name)) is not None:
            hd._score(screen, eng, name, x0 + w - S(18), y + S(40), "right", S(size))

    def gauge(self, screen, x, y, w, label, frac, col, label_col=(255, 230, 120), back=(50, 20, 24)):
        S = self.S
        self.pill(screen, x, y, w + S(130), S(44), 160, radius=12)
        self.text(screen, label, x + S(16), y + S(22), 22, label_col, key="black", valign="middle", glow=0)
        self.bar(screen, x + S(112), y + S(11), w, S(22), frac, col, back=back)

    def invite_right(self, screen, vals, now, y=None):
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, self.W - self.S(24), y or self.S(40), 30, col, align="right")


# ============================================================================ Ghouls'n Ghosts
GG_WEAPONS = {0: ("LANCE", "LANCE"), 1: ("DAGUE", "DAGGER"), 2: ("TORCHE", "TORCH"), 3: ("ÉPÉE", "SWORD"), 4: ("HACHE", "AXE"),
              5: ("BOUCLIER", "SHIELD"), 6: ("BOULE DE FEU", "FIREBALL")}


def knight_draw(armor, frame):
    """Our own knight seen from the side, facing right: a full armour (silver or gold) with its helmet and red plume,
    or, without armour, a blue tunic and a red headband. Frames 0 stand, 1 and 2 walk, 3 throw.
    / Notre chevalier à nous : armure complète (argent ou or), casque et plumet rouge, ou sans armure une tunique bleue."""
    def fn(d, W, H):
        ow = max(1.0, H * 0.012)
        dark = DARKLINE
        if armor == "gold":
            metal, metal_d, metal_l = (236, 190, 70), (150, 104, 30), (255, 240, 170)
        else:
            metal, metal_d, metal_l = (190, 198, 214), (100, 108, 130), (245, 248, 255)
        bare = armor == "none"
        leg = _c(SKIN) if bare else _c(metal)
        step = {1: 0.06, 2: -0.06}.get(frame, 0.0)
        for k, sx in ((0, -1), (1, 1)):                                # les jambes
            dx = sx * step * W
            _capsule(d, (W * (0.44 + 0.06 * k), H * 0.6), (W * (0.42 + 0.06 * k) + dx, H * 0.95), H * 0.075, H * 0.065, leg, dark, ow)
            d.rounded_rectangle([W * (0.36 + 0.06 * k) + dx, H * 0.92, W * (0.52 + 0.06 * k) + dx, H * 0.99], radius=H * 0.02,
                                fill=_c((90, 60, 40) if bare else metal_d), outline=dark, width=int(ow))
        if bare:                                                      # la tunique
            d.polygon([(W * 0.32, H * 0.36), (W * 0.66, H * 0.36), (W * 0.7, H * 0.66), (W * 0.3, H * 0.66)], fill=(60, 110, 200, 255), outline=dark)
            d.line([(W * 0.31, H * 0.56), (W * 0.69, H * 0.56)], fill=(130, 80, 40, 255), width=int(ow * 3))
        else:                                                         # la cuirasse
            d.rounded_rectangle([W * 0.3, H * 0.34, W * 0.68, H * 0.64], radius=H * 0.06, fill=_c(metal), outline=dark, width=int(ow))
            d.line([(W * 0.49, H * 0.36), (W * 0.49, H * 0.62)], fill=_c(metal_d), width=int(ow * 1.5))
            d.ellipse([W * 0.35, H * 0.38, W * 0.45, H * 0.46], fill=_c(metal_l))
            d.rounded_rectangle([W * 0.28, H * 0.56, W * 0.7, H * 0.66], radius=H * 0.03, fill=_c(metal_d), outline=dark, width=int(ow))
        arm_to = (W * 0.92, H * 0.36) if frame == 3 else (W * 0.66, H * 0.6)
        _capsule(d, (W * 0.5, H * 0.4), arm_to, H * 0.07, H * 0.06, _c(SKIN) if bare else _c(metal), dark, ow)
        d.ellipse([arm_to[0] - H * 0.035, arm_to[1] - H * 0.035, arm_to[0] + H * 0.035, arm_to[1] + H * 0.035], fill=_c((200, 150, 110)), outline=dark)
        hx, hy = W * 0.5, H * 0.2
        if bare:                                                      # la tête nue, le bandeau rouge
            d.ellipse([hx - H * 0.1, hy - H * 0.11, hx + H * 0.1, hy + H * 0.11], fill=_c(SKIN), outline=dark, width=int(ow))
            d.chord([hx - H * 0.1, hy - H * 0.12, hx + H * 0.1, hy + H * 0.08], 180, 360, fill=(110, 70, 40, 255))
            d.line([(hx - H * 0.1, hy - H * 0.03), (hx + H * 0.1, hy - H * 0.03)], fill=(220, 40, 40, 255), width=int(ow * 3))
            d.ellipse([hx + H * 0.04, hy - H * 0.01, hx + H * 0.07, hy + H * 0.03], fill=dark)
        else:                                                         # le casque, la visière, le plumet
            d.polygon([(hx - H * 0.02, hy - H * 0.1), (hx - H * 0.2, hy - H * 0.2), (hx - H * 0.24, hy - H * 0.06), (hx - H * 0.08, hy - H * 0.02)],
                      fill=(220, 40, 40, 255), outline=dark)
            d.rounded_rectangle([hx - H * 0.11, hy - H * 0.12, hx + H * 0.11, hy + H * 0.12], radius=H * 0.06, fill=_c(metal), outline=dark, width=int(ow))
            d.rectangle([hx - H * 0.01, hy - H * 0.02, hx + H * 0.11, hy + H * 0.02], fill=dark)
            d.line([(hx - H * 0.08, hy - H * 0.09), (hx + H * 0.04, hy - H * 0.09)], fill=_c(metal_l), width=int(ow * 2))
    return fn


def ghoul_draw(frame):
    """A ghoul of our own that climbs out of the ground, arms forward, in its brown rags. / Une goule à nous qui sort de
    terre, les bras en avant, dans ses haillons bruns."""
    def fn(d, W, H):
        ow = max(1.0, H * 0.012)
        body, body_d = (140, 150, 190), (90, 96, 130)
        rags = (110, 80, 50, 255)
        for k, x in enumerate((0.4, 0.56)):
            lift = 0.03 * ((frame + k) % 2)
            _capsule(d, (W * x, H * 0.62), (W * x, H * (0.97 - lift)), H * 0.07, H * 0.06, _c(body_d), DARKLINE, ow)
        d.polygon([(W * 0.3, H * 0.34), (W * 0.66, H * 0.34), (W * 0.72, H * 0.7), (W * 0.62, H * 0.66), (W * 0.54, H * 0.74), (W * 0.44, H * 0.66),
                   (W * 0.34, H * 0.74), (W * 0.26, H * 0.68)], fill=rags, outline=DARKLINE)
        for y in (0.4, 0.48):
            _capsule(d, (W * 0.5, H * y), (W * 0.06, H * (y + 0.03 * (frame % 2))), H * 0.06, H * 0.05, _c(body), DARKLINE, ow)
        d.ellipse([W * 0.3, H * 0.08, W * 0.66, H * 0.38], fill=_c(body), outline=DARKLINE, width=int(ow))
        for ex in (0.38, 0.5):
            d.ellipse([W * ex, H * 0.18, W * (ex + 0.07), H * 0.24], fill=(255, 230, 80, 255))
        d.line([(W * 0.36, H * 0.31), (W * 0.52, H * 0.3)], fill=DARKLINE, width=int(ow * 2))
    return fn


def crow_draw(frame, body=(30, 28, 40), beak=(240, 180, 40)):
    """A black crow of our own, its wings up or down. / Un corbeau noir à nous, les ailes en haut ou en bas."""
    def fn(d, W, H):
        up = frame % 2 == 0
        d.ellipse([W * 0.3, H * 0.38, W * 0.72, H * 0.66], fill=_c(body), outline=DARKLINE)
        d.ellipse([W * 0.12, H * 0.3, W * 0.36, H * 0.54], fill=_c(body), outline=DARKLINE)
        d.polygon([(W * 0.12, H * 0.4), (W * 0.0, H * 0.46), (W * 0.13, H * 0.48)], fill=_c(beak))
        d.ellipse([W * 0.2, H * 0.36, W * 0.25, H * 0.42], fill=(255, 60, 40, 255))
        d.polygon([(W * 0.7, H * 0.48), (W * 0.98, H * 0.36), (W * 0.96, H * 0.62)], fill=_c(body), outline=DARKLINE)
        wing = [(W * 0.38, H * 0.46), (W * 0.62, H * 0.46), (W * 0.74, H * (0.02 if up else 0.94)), (W * 0.5, H * (0.12 if up else 0.84))]
        d.polygon(wing, fill=_c(_mix(body, WHITE, 0.15)), outline=DARKLINE)
    return fn


def gg_weapon_draw(kind):
    """What our knight throws: lance, dagger, torch, sword, axe, shield, fireball. / Ce que lance notre chevalier."""
    def fn(d, W, H):
        steel, steel_d, wood = (230, 234, 245, 255), (110, 116, 140, 255), (150, 100, 50, 255)
        if kind == 0:                                                 # la lance
            d.line([(W * 0.0, H * 0.5), (W * 0.78, H * 0.5)], fill=wood, width=int(H * 0.18))
            d.polygon([(W * 0.74, H * 0.2), (W * 1.0, H * 0.5), (W * 0.74, H * 0.8)], fill=steel, outline=steel_d)
        elif kind == 1:                                               # la dague
            d.polygon([(W * 0.3, H * 0.34), (W * 1.0, H * 0.5), (W * 0.3, H * 0.66)], fill=steel, outline=steel_d)
            d.rectangle([W * 0.04, H * 0.42, W * 0.3, H * 0.58], fill=wood)
            d.rectangle([W * 0.26, H * 0.2, W * 0.32, H * 0.8], fill=(220, 180, 60, 255))
        elif kind == 2:                                               # la torche
            d.line([(W * 0.0, H * 0.5), (W * 0.6, H * 0.5)], fill=wood, width=int(H * 0.2))
            d.ellipse([W * 0.52, H * 0.1, W * 1.0, H * 0.9], fill=(255, 120, 30, 255))
            d.ellipse([W * 0.62, H * 0.28, W * 0.92, H * 0.72], fill=(255, 230, 120, 255))
        elif kind == 3:                                               # l'épée
            d.polygon([(W * 0.24, H * 0.4), (W * 0.92, H * 0.4), (W * 1.0, H * 0.5), (W * 0.92, H * 0.6), (W * 0.24, H * 0.6)], fill=steel, outline=steel_d)
            d.rectangle([W * 0.2, H * 0.14, W * 0.26, H * 0.86], fill=(220, 180, 60, 255))
            d.rectangle([W * 0.0, H * 0.42, W * 0.2, H * 0.58], fill=wood)
        elif kind == 4:                                               # la hache
            d.line([(W * 0.1, H * 0.9), (W * 0.7, H * 0.2)], fill=wood, width=int(H * 0.12))
            d.chord([W * 0.4, H * 0.0, W * 1.0, H * 0.6], 300, 140, fill=steel, outline=steel_d)
        elif kind == 5:                                               # le bouclier
            d.ellipse([W * 0.15, H * 0.0, W * 0.85, H * 1.0], fill=(200, 60, 50, 255), outline=(240, 200, 80, 255), width=int(H * 0.08))
            d.line([(W * 0.5, H * 0.12), (W * 0.5, H * 0.88)], fill=(240, 200, 80, 255), width=int(H * 0.08))
            d.line([(W * 0.22, H * 0.5), (W * 0.78, H * 0.5)], fill=(240, 200, 80, 255), width=int(H * 0.08))
        else:                                                         # la boule de feu
            d.ellipse([W * 0.3, H * 0.0, W * 1.0, H * 1.0], fill=(90, 160, 255, 255))
            d.polygon([(W * 0.0, H * 0.5), (W * 0.45, H * 0.1), (W * 0.45, H * 0.9)], fill=(90, 160, 255, 180))
            d.ellipse([W * 0.48, H * 0.22, W * 0.9, H * 0.78], fill=(230, 245, 255, 255))
    return fn


class GhoulsScene(SideQuestScene):
    """Ghouls'n Ghosts as in the game: the place of the executions under the storm, the walls of mossy stones, the
    gibbets, the tombstones; our knight of our own throws what the game says he holds (lance, dagger, torch, sword, axe,
    shield, fireball) at the ghouls that climb out of the ground and the crows. His armour follows the game: silver,
    gold, or lost and he goes on in his tunic. PLAYER-1 and the score, the TIME in its orange frame, the weapon in its
    frame at the bottom, as in the game. / Le lieu des exécutions sous l'orage ; notre chevalier lance ce que le jeu dit
    qu'il tient sur les goules qui sortent de terre et les corbeaux. Son armure suit le jeu : argent, or ou perdue."""
    THEME = "gg_grave"
    FLOOR = GG_FLOOR
    HERO = (150, 200)
    FOE = (120, 170)
    FLYER = (110, 70)
    FLY_Y = (180, 250)
    POINTS = ("100", "100", "200")
    SHADE = (100, 40)
    BANNERS = GameScene.BANNERS + (("ARMURE PERDUE !", (255, 200, 60)), ("ARMOUR LOST!", (255, 200, 60)))

    def __init__(self, hd, rng=None):
        self.armor, self.weapon = "silver", 0
        super().__init__(hd, rng)
        self.lost = 0                                     # (tests)

    def hero_key(self):
        return self.armor

    def hero_draw(self, frame):
        return knight_draw(self.armor, frame)

    def foe_draw(self, kind, frame):
        return crow_draw(frame) if kind == 1 else ghoul_draw(frame)

    def shot_key(self):
        return self.weapon

    def shot_size(self):
        return {0: (110, 26), 1: (60, 24), 2: (70, 36), 3: (100, 30), 4: (60, 60), 5: (56, 56), 6: (80, 46)}.get(self.weapon, (100, 26))

    def shot_draw(self):
        return gg_weapon_draw(self.weapon)

    def blit_shot(self, screen, sh, img, now):
        if self.weapon in (4, 5):                                       # the axe and the shield spin / tournent
            img = self.rotated(("ggspin", self.weapon), img, -(now - sh["t0"]) * 900, 15)
        screen.blit(img, (int(sh["x"] - img.get_width() / 2), int(sh["y"] - img.get_height() / 2)))

    def blit_foe(self, screen, f, img, y, now):
        if f["kind"] == 0 and not f.get("dead"):                        # the ghoul climbs out of the ground / sort de terre
            k = _clamp((now - f["born"]) / 0.8)
            h = int(img.get_height() * k)
            if h <= 0:
                return
            screen.blit(img, (int(f["x"] - img.get_width() / 2), int(y - h)), (0, 0, img.get_width(), h))
            return
        super().blit_foe(screen, f, img, y, now)

    def always(self, vals, now):
        a, b = _n(vals.get("armor")), _n(vals.get("armor_kind"))
        armor = self.armor
        if a is not None and b is not None:
            armor = "none" if int(b) <= 1 or int(a) == 0 else ("gold" if int(b) >= 3 else "silver")
        if armor != self.armor:
            if armor == "none" and self.p1_in(vals) and not self.nobody(vals):
                self.lost += 1
                hx, hy = self.hero_xy(now)
                for i in range(6):                                      # the pieces of armour fly away / les pièces s'envolent
                    self.fx.sparks(hx, hy - self.S(100), 3, (210, 216, 230), (300, 700), (200 + i * 25, 230 + i * 25), (0.4, 0.8), 1400, "front", 6, 14)
                self.slam(tr("ARMURE PERDUE !", "ARMOUR LOST!"), (255, 200, 60), now, 1.3)
            elif armor == "gold":
                hx, hy = self.hero_xy(now)
                self.fx.glow(hx, hy - self.S(100), 40, 220, (255, 220, 120), 0.6, "front", 1.0, 0.0)
            self.armor = armor
        w = _n(vals.get("weapon"))
        if w is not None and int(w) in GG_WEAPONS and int(w) != self.weapon:
            self.weapon = int(w)
            if self.p1_in(vals) and not self.nobody(vals):
                hx, hy = self.hero_xy(now)
                self.popup(tr(*GG_WEAPONS[self.weapon]), hx, hy - self.S(250), (120, 220, 255), 34)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: PLAYER-1 and the score, the TIME in its orange frame, the weapon in its frame at the bottom.
        / Comme dans le jeu : PLAYER-1 et le score, le TIME dans son cadre orange, l'arme dans son cadre en bas."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(440), S(84), now)
        self.side_score(screen, eng, vals, "PLAYER-1", S(14), S(6), (255, 255, 255))
        t = _n(vals.get("time"))
        if t is not None:
            t = int(t)
            pg.draw.rect(screen, (8, 8, 16), (S(330), S(12), S(150), S(80)), border_radius=S(8))
            pg.draw.rect(screen, (255, 150, 40), (S(330), S(12), S(150), S(80)), max(2, S(4)), border_radius=S(8))
            self.text(screen, "TIME", S(405), S(32), 22, (255, 150, 40), key="black", align="center", valign="middle", glow=0)
            hd.put_number(screen, f"{t // 60}:{t % 60:02d}" if t >= 60 else f"{t:02d}", "black", S(36), WHITE, S(405), S(66), "center", "middle")
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.label(screen, f"x{int(lives)}", S(80), H - S(36), 30, (255, 220, 120), align="center")
        bx = W / 2 - S(60)                                             # the weapon frame / le cadre de l'arme
        pg.draw.rect(screen, (10, 10, 20), (int(bx), H - S(80), S(120), S(70)), border_radius=S(6))
        pg.draw.rect(screen, (220, 190, 90), (int(bx), H - S(80), S(120), S(70)), max(2, S(4)), border_radius=S(6))
        img = self.shot_img()
        k = min(1.0, S(100) / max(1, img.get_width()))
        if k < 1:
            img = self.pg.transform.smoothscale(img, (max(1, int(img.get_width() * k)), max(1, int(img.get_height() * k))))
        screen.blit(img, (int(W / 2 - img.get_width() / 2), int(H - S(45) - img.get_height() / 2)))
        if self.p2_in(vals):
            self.side_score(screen, eng, vals, "PLAYER-2", W - S(14), S(6), (255, 255, 255), "score_p2", align="right")
        else:
            self.invite_right(screen, vals, now)


# ============================================================================ Strider
def drone_draw(frame):
    """A little flying robot of our own: a round body, one red eye, a rotor. / Un petit robot volant à nous."""
    def fn(d, W, H):
        ow = max(1.0, H * 0.03)
        d.ellipse([W * 0.2, H * 0.3, W * 0.8, H * 0.95], fill=(150, 160, 170, 255), outline=DARKLINE, width=int(ow))
        d.ellipse([W * 0.26, H * 0.5, W * 0.46, H * 0.74], fill=(255, 60, 40, 255), outline=DARKLINE)
        d.line([(W * 0.5, H * 0.3), (W * 0.5, H * 0.14)], fill=DARKLINE, width=int(ow * 1.5))
        span = 0.45 if frame % 2 else 0.22
        d.ellipse([W * (0.5 - span), H * 0.06, W * (0.5 + span), H * 0.18], fill=(200, 210, 220, 200), outline=DARKLINE)
    return fn


class StriderScene(SideQuestScene):
    """Strider as in the game: the city of the first stage at night, the golden onion domes, the long roof; our ninja of
    our own runs and cuts the soldiers and the little flying robots with the bright crescent of his blade. 1-PLAYER and
    the score, the TIME, the lives, as in the game. / La ville du premier niveau la nuit, les bulbes dorés, le long
    toit ; notre ninja à nous court et coupe les soldats et les petits robots volants d'un croissant de lumière."""
    THEME = "st_city"
    FLOOR = ST_FLOOR
    HERO = (170, 200)
    FOE = (150, 190)
    FLYER = (90, 80)
    FLY_Y = (170, 250)
    SHOT = "slash"
    REACH = 0.22
    MOVE = (0.6, 2.2)
    PACE = (0.8, 1.8)
    SHADE = (110, 30)

    def hero_draw(self, frame):
        return fighter_draw("ninja", (40, 90, 200), (30, 40, 90), SKIN, (30, 30, 40), {1: 1, 2: 2, 3: 3}.get(frame, 0), "sword")

    def foe_draw(self, kind, frame):
        if kind == 1:
            return drone_draw(frame)
        return fighter_draw("cyborg", (90, 110, 70), (60, 70, 50), (200, 160, 120), (40, 40, 40), 1 + frame % 2)

    def slash_fx(self, hx, hy, now):
        """The crescent of light of the blade. / Le croissant de lumière de la lame."""
        S = self.S
        cx, cy = hx + S(70), hy - S(120)
        for i in range(7):
            a = math.radians(-70 + i * 22)
            self.fx.later(i * 0.012, self.fx.glow, cx + math.cos(a) * S(120), cy + math.sin(a) * S(120), 10, 46, (150, 220, 255), 0.2, "front",
                          1.0, 0.0, 0.0, 0.7)
        self.fx.sparks(cx + S(100), cy, 8, (200, 240, 255), (200, 600), (-60, 60), (0.15, 0.3), 200, "front", 3, 18)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1-PLAYER and the score, the lives, the TIME. / 1-PLAYER et le score, les vies, le TIME."""
        S, W, hd = self.S, self.W, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(440), S(84), now)
        self.side_score(screen, eng, vals, "1-PLAYER", S(14), S(6), (255, 255, 255))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.label(screen, f"1-UP={int(lives):02d}", S(330), S(52), 26, (120, 255, 160))
        t = _n(vals.get("time"))
        if t is not None:
            self.pill(screen, W / 2 + S(250), S(14), S(200), S(76), 150, radius=14)
            self.text(screen, "TIME", W / 2 + S(270), S(52), 24, (255, 230, 120), key="black", valign="middle")
            hd.put_number(screen, f"{int(t)}", "black", S(42), WHITE, W / 2 + S(430), S(52), "right", "middle")
        if self.p2_in(vals):
            self.side_score(screen, eng, vals, "2-PLAYER", W - S(14), S(6), (255, 255, 255), "score_p2", align="right")
        else:
            self.invite_right(screen, vals, now)


# ============================================================================ Pang! 3 and Mighty! Pang
def hunter_draw(frame, coat=(230, 200, 120), hat=(250, 250, 240)):
    """Our own little balloon hunter: a pith helmet, a coat, the harpoon gun held up when he fires.
    / Notre petit chasseur de ballons à nous : un casque colonial, une veste, le fusil à harpon levé quand il tire."""
    def fn(d, W, H):
        ow = max(1.0, H * 0.025)
        step = {1: 0.05, 2: -0.05}.get(frame, 0.0) * W
        for x in (0.36, 0.54):
            d.rounded_rectangle([W * x + step * (1 if x < 0.5 else -1), H * 0.72, W * (x + 0.12) + step * (1 if x < 0.5 else -1), H * 0.98],
                                radius=W * 0.04, fill=(70, 60, 50, 255), outline=DARKLINE, width=int(ow))
        d.rounded_rectangle([W * 0.28, H * 0.42, W * 0.72, H * 0.78], radius=W * 0.1, fill=_c(coat), outline=DARKLINE, width=int(ow))
        d.line([(W * 0.5, H * 0.44), (W * 0.5, H * 0.76)], fill=_c(_mix(coat, (0, 0, 0), 0.3)), width=int(ow))
        if frame == 3:                                                 # le fusil levé / the gun held up
            d.rectangle([W * 0.6, H * 0.04, W * 0.7, H * 0.46], fill=(90, 90, 100, 255), outline=DARKLINE)
            _capsule(d, (W * 0.62, H * 0.48), (W * 0.65, H * 0.3), H * 0.07, H * 0.06, _c(SKIN), DARKLINE, ow)
        else:
            d.rectangle([W * 0.66, H * 0.46, W * 0.94, H * 0.54], fill=(90, 90, 100, 255), outline=DARKLINE)
            _capsule(d, (W * 0.6, H * 0.5), (W * 0.74, H * 0.56), H * 0.07, H * 0.06, _c(SKIN), DARKLINE, ow)
        d.ellipse([W * 0.32, H * 0.16, W * 0.68, H * 0.46], fill=_c(SKIN), outline=DARKLINE, width=int(ow))
        for ex in (0.44, 0.56):
            d.ellipse([W * (ex - 0.025), H * 0.28, W * (ex + 0.025), H * 0.34], fill=DARKLINE)
        d.chord([W * 0.26, H * 0.02, W * 0.74, H * 0.36], 180, 360, fill=_c(hat), outline=DARKLINE)
        d.rectangle([W * 0.2, H * 0.18, W * 0.8, H * 0.22], fill=_c(hat), outline=DARKLINE)
    return fn


def balloon_draw(col):
    """A shiny round balloon. / Un ballon rond et brillant."""
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=_c(_mix(col, (0, 0, 0), 0.35)))
        d.ellipse([W * 0.04, H * 0.02, W * 0.94, H * 0.92], fill=_c(col))
        d.ellipse([W * 0.16, H * 0.12, W * 0.5, H * 0.42], fill=_c(_mix(col, WHITE, 0.55)))
        d.ellipse([W * 0.22, H * 0.16, W * 0.36, H * 0.28], fill=(255, 255, 255, 255))
    return fn


class BalloonScene(GameScene):
    """A balloon game as Pang: big balloons bounce in the place of the game, our hunter of our own walks under them and
    fires his harpoon straight up; a balloon hit splits in two smaller ones, the smallest burst. The points read in the
    game burst a balloon, a life lost is a balloon that falls on the hunter, all burst is the next level. The bar at the
    bottom as in the game. / Un jeu de ballons comme Pang : de gros ballons rebondissent, notre chasseur tire son harpon
    droit vers le haut, un ballon touché se coupe en deux plus petits, les plus petits éclatent."""
    THEME = "pg_temple"
    STATIC = True
    SHADE = (70, 110)
    FLOOR = PG_FLOOR
    SIZES = (78, 50, 30, 17)                       # radius of each size / rayon de chaque taille
    BOUNCE = (330, 270, 210, 150)                  # height of the bounce / hauteur du rebond
    COLORS = ((230, 40, 40),)
    POINTS = (50, 100, 150, 200)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.balls = []
        self.hero = {"x": self.W * 0.5, "dir": 1, "fire": -99.0, "hit": -99.0}
        self.wire = None
        self.level = 1
        self.bursts = 0                                   # (tests)
        self.hits = 0
        self.warm = [(self.ball_img, (k, c)) for k in range(4) for c in range(len(self.COLORS))] + [(self.hero_img, (f,)) for f in range(4)] + self.warm

    def ball_img(self, size, col):
        r = self.S(self.SIZES[size])
        return self.img(("pgball", size, col), 2 * r, 2 * r, balloon_draw(self.COLORS[col % len(self.COLORS)]), ss=2)

    def hero_img(self, frame):
        S = self.S
        return self.img(("pghero", frame), S(80), S(100), hunter_draw(frame), ss=2)

    def floor(self):
        return self.S(self.FLOOR)

    def new_level(self, now):
        S, rng = self.S, self.rng
        self.balls = []
        for k in range(2 + min(2, self.level // 3)):
            x = rng.uniform(self.W * 0.1, self.W * 0.9)
            self.balls.append({"x": x, "y": S(rng.uniform(140, 220)), "vx": rng.choice((-1, 1)) * S(rng.uniform(150, 240)), "vy": 0.0, "size": 0,
                               "col": rng.randrange(len(self.COLORS))})

    def restart(self, vals, now):
        self.wire = None
        self.new_level(now)

    def burst(self, b, now, points=None):
        if b not in self.balls:
            return
        S = self.S
        self.balls.remove(b)
        self.bursts += 1
        col = self.COLORS[b["col"] % len(self.COLORS)]
        self.fx.sparks(b["x"], b["y"], 10 + 4 * (3 - b["size"]), _mix(col, WHITE, 0.3), (200, 600), (0, 360), (0.2, 0.5), 400, "front", 4, 14)
        self.fx.glow(b["x"], b["y"], 20, S(self.SIZES[b["size"]]) / self.s * 1.6, (255, 240, 200), 0.25, "front", 0.9, 0.0)
        if points:                                                      # the points read in the game / les points lus dans le jeu
            self.popup(str(points), b["x"], b["y"] - S(40), GOLD, 26)
        if b["size"] < 3:                                               # two smaller balloons / deux plus petits
            for d in (-1, 1):
                self.balls.append({"x": b["x"], "y": b["y"], "vx": d * S(200), "vy": -S(420), "size": b["size"] + 1, "col": b["col"]})

    def update(self, vals, now):
        S, h = self.S, self.hero
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0] and self.balls:                         # the smallest balloon near the hunter / le plus petit
            self.burst(min(self.balls, key=lambda b: (-b["size"], abs(b["x"] - h["x"]))), now, int(ch[1] - ch[0]) if ch[1] - ch[0] < 100000 else None)
        for name in ("lives", "lives_p2"):
            ch = self.changed(vals, name)
            if ch and ch[1] < ch[0]:                                    # a balloon falls on the hunter / un ballon tombe sur lui
                self.hits += 1
                h["hit"] = now
                self.fx.shake(10, 0.3)
                self.popup(tr("-1 VIE", "-1 LIFE"), h["x"], self.floor() - S(160), (255, 90, 70), 36)
                for b in self.balls:
                    b["vy"] = -S(500)
        if not self.balls:                                              # all burst: the next level / niveau suivant
            self.level += 1
            self.slam(f"LEVEL {self.level:02d}", (120, 220, 255), now, 1.2)
            self.new_level(now)
        if now - h["hit"] < 1.2:
            return
        target = min(self.balls, key=lambda b: abs(b["x"] - h["x"]) + (S(200) if b["y"] > self.floor() - S(150) else 0))
        dx = target["x"] - h["x"]
        if abs(dx) > S(30):
            h["dir"] = 1 if dx > 0 else -1
            h["x"] += h["dir"] * S(260) * self.dt
        elif self.wire is None and now - h["fire"] > 1.1:
            h["fire"] = now
            self.wire = {"x": h["x"] + S(4), "top": self.floor() - S(90)}
        h["x"] = _clamp(h["x"], S(60), self.W - S(60))
        if self.wire is not None:                                       # the harpoon wire climbs / le fil monte
            w = self.wire
            w["top"] -= S(900) * self.dt
            for b in list(self.balls):
                r = S(self.SIZES[b["size"]])
                if abs(b["x"] - w["x"]) < r and b["y"] + r > w["top"]:
                    self.burst(b, now)
                    self.wire = None
                    break
            if self.wire is not None and w["top"] < S(20):
                self.wire = None

    def physics(self):
        S, dt, fl = self.S, self.dt, self.floor()
        for b in self.balls:
            r = S(self.SIZES[b["size"]])
            b["vy"] += S(700) * dt
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
            if b["y"] + r > fl:                                         # the bounce always reaches its height / le rebond
                b["y"] = fl - r
                b["vy"] = -math.sqrt(2 * S(700) * S(self.BOUNCE[b["size"]]))
            if b["x"] - r < 0 or b["x"] + r > self.W:
                b["vx"] = -b["vx"]
                b["x"] = _clamp(b["x"], r, self.W - r)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        self.physics()
        if self.wire is not None:
            w = self.wire
            y0 = self.floor() - S(60)
            for k in range(int((y0 - w["top"]) / S(14)) + 1):         # the twisted wire / le fil torsadé
                y = y0 - k * S(14)
                pg.draw.line(screen, (230, 230, 240), (int(w["x"] - S(5)), int(y)), (int(w["x"] + S(5)), int(y - S(7))), max(2, S(3)))
                pg.draw.line(screen, (150, 150, 170), (int(w["x"] + S(5)), int(y - S(7))), (int(w["x"] - S(5)), int(y - S(14))), max(2, S(3)))
            pg.draw.polygon(screen, (240, 240, 250), [(int(w["x"]), int(w["top"] - S(18))), (int(w["x"] - S(10)), int(w["top"])),
                                                      (int(w["x"] + S(10)), int(w["top"]))])
        for b in self.balls:
            img = self.ball_img(b["size"], b["col"])
            screen.blit(img, (int(b["x"] - img.get_width() / 2), int(b["y"] - img.get_height() / 2)))
        h = self.hero
        if self.p1_in(vals) and not (now - h["hit"] < 1.2 and int(now * 14) % 2):
            frame = 3 if now - h["fire"] < 0.25 else (1 + int(now * 7) % 2 if self.wire is None else 0)
            img = self.hero_img(frame)
            if h["dir"] < 0 and frame != 3:
                img = self.pg.transform.flip(img, True, False)
            screen.blit(img, (int(h["x"] - img.get_width() / 2), int(self.floor() - img.get_height())))
        self.status(screen, eng, vals, logo, now)

    def lives_icons(self, screen, x, y, n, col=(250, 250, 240)):
        S, pg = self.S, self.pg
        for k in range(int(min(n, 6))):
            cx = x + k * S(30)
            pg.draw.circle(screen, (240, 196, 160), (int(cx), int(y + S(4))), S(10))
            pg.draw.ellipse(screen, col, (int(cx - S(13)), int(y - S(12)), S(26), S(14)))

    def status(self, screen, eng, vals, logo, now):
        """The bar at the bottom as in the game: 1P and the score, the lives, LEVEL, the time; player 2 or the invitation
        on the right. / La barre du bas comme dans le jeu : 1P et le score, les vies, LEVEL, le temps."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(80), now)
        y = H - S(46)
        self.pill(screen, S(12), y - S(30), S(620), S(60), 170, radius=12)
        self.text(screen, "1P", S(30), y, 30, P1C, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(330), y - S(22), "right", S(40))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.lives_icons(screen, S(370), y, lives)
        self.label(screen, f"LEVEL {self.level:02d}", W / 2, y, 34, (255, 230, 60), key="black", align="center")
        t = _n(vals.get("time"))
        if t is not None:
            self.label(screen, f"TIME {int(t):03d}", W / 2 + S(280), y, 30, WHITE, key="black", align="center")
        if self.p2_in(vals):
            self.pill(screen, W - S(420), y - S(30), S(408), S(60), 170, radius=12)
            self.text(screen, "2P", W - S(400), y, 30, P2C, key="black", valign="middle")
            if _n(vals.get("score_p2")) is not None:
                hd._score(screen, eng, "score_p2", W - S(30), y - S(22), "right", S(40))
        else:
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), y, 30, col, align="right")


class Pang3Scene(BalloonScene):
    """Pang! 3 as in the game: the painted wall of the temple in Egypt, the huge eye, the frieze; red balloons that our
    hunter of our own cuts down with his harpoon. 1P and the score, the lives, LEVEL and the time at the bottom.
    / Le mur peint du temple en Égypte, l'œil immense ; des ballons rouges que notre chasseur coupe de son harpon."""
    THEME = "pg_temple"


class MightyPangScene(BalloonScene):
    """Mighty! Pang as in the game: the highest mountain of the world under a deep blue sky, the snow that falls;
    balloons of three colours, our hunter of our own and his harpoon. SCORE, the lives, LEVEL at the bottom.
    / La plus haute montagne du monde sous un ciel bleu profond, la neige qui tombe ; des ballons de trois couleurs."""
    THEME = "pg_peak"
    SHADE = (40, 100)
    COLORS = ((230, 40, 40), (40, 120, 240), (40, 190, 80))


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


# ============================================================================ Mega Twins
def twin_draw(frame):
    """Our own little twin hero: a big head, a green pointed cap and its red feather, a green tunic, a short sword.
    / Notre petit héros jumeau à nous : grosse tête, bonnet vert pointu et sa plume rouge, tunique verte, épée courte."""
    base = chibi_draw(SKIN, (230, 150, 60), (60, 170, 80), (50, 90, 50), 1 if frame == 3 else 0, False)

    def fn(d, W, H):
        base(d, W, H)
        ow = max(1.0, H * 0.014)
        hx, hy, r = W * 0.5, H * 0.3, W * 0.25
        d.polygon([(hx - r * 1.08, hy - r * 0.3), (hx + r * 1.08, hy - r * 0.3), (hx + r * 0.2, hy - r * 1.7), (hx - r * 0.5, hy - r * 1.2)],
                  fill=(60, 170, 80, 255), outline=DARKLINE)
        d.polygon([(hx + r * 0.6, hy - r * 0.9), (hx + r * 1.5, hy - r * 1.6), (hx + r * 0.9, hy - r * 0.7)], fill=(230, 50, 50, 255), outline=DARKLINE)
        hand = (W * 0.92, H * 0.56) if frame == 3 else (W * 0.66, H * 0.7)
        tip = (hand[0] + W * 0.08, hand[1] - H * 0.3) if frame != 3 else (hand[0] + W * 0.06, hand[1] - H * 0.02)
        d.line([hand, tip], fill=(230, 236, 250, 255), width=int(ow * 5))
        d.line([(hand[0] - W * 0.05, hand[1]), (hand[0] + W * 0.05, hand[1])], fill=(220, 180, 60, 255), width=int(ow * 4))
    return fn


def blob_draw(frame, col):
    """A little round blob of our own that hops, its big eyes. / Une petite boule à nous qui sautille, ses grands yeux."""
    def fn(d, W, H):
        sq = 0.08 if frame % 2 else 0.0
        d.ellipse([W * (0.1 - sq), H * (0.3 + sq), W * (0.9 + sq), H * 0.98], fill=_c(col), outline=DARKLINE, width=max(1, int(H * 0.03)))
        d.ellipse([W * 0.24, H * (0.4 + sq), W * 0.46, H * (0.6 + sq)], fill=_c(_mix(col, WHITE, 0.5)))
        for ex in (0.36, 0.6):
            d.ellipse([W * ex, H * (0.52 + sq), W * (ex + 0.12), H * (0.7 + sq)], fill=(255, 255, 255, 255), outline=DARKLINE)
            d.ellipse([W * (ex + 0.04), H * (0.58 + sq), W * (ex + 0.09), H * (0.66 + sq)], fill=DARKLINE)
    return fn


def bee_draw(frame):
    """A big bee of our own, its wings beating. / Une grosse abeille à nous, ses ailes qui battent."""
    def fn(d, W, H):
        d.ellipse([W * 0.2, H * 0.36, W * 0.86, H * 0.86], fill=(250, 200, 40, 255), outline=DARKLINE, width=max(1, int(H * 0.03)))
        for x in (0.42, 0.6):
            d.line([(W * x, H * 0.38), (W * (x - 0.04), H * 0.84)], fill=DARKLINE, width=max(2, int(W * 0.06)))
        d.ellipse([W * 0.08, H * 0.4, W * 0.34, H * 0.7], fill=(250, 200, 40, 255), outline=DARKLINE)
        d.ellipse([W * 0.13, H * 0.48, W * 0.2, H * 0.56], fill=DARKLINE)
        up = frame % 2 == 0
        d.ellipse([W * 0.36, H * (0.0 if up else 0.12), W * 0.66, H * (0.42 if up else 0.5)], fill=(230, 245, 255, 200), outline=DARKLINE)
        d.polygon([(W * 0.86, H * 0.6), (W * 1.0, H * 0.64), (W * 0.86, H * 0.68)], fill=DARKLINE)
    return fn


class MegaTwinsScene(SideQuestScene):
    """Mega Twins as in the game: the bright forest of the first stage, its big round trees with their kind faces, the
    floating islands; our little twin hero of our own cuts the hopping blobs and the bees with his short sword. VITAL in
    its blue gauge, the time, the score and the lives, as in the game. / La forêt du premier niveau, ses grands arbres au
    visage gentil ; notre petit héros jumeau à nous coupe les boules qui sautillent et les abeilles de son épée courte."""
    THEME = "mt_forest"
    FLOOR = MT_FLOOR
    HERO = (130, 160)
    FOE = (90, 80)
    FLYER = (90, 70)
    FLY_Y = (200, 270)
    SHOT = "slash"
    REACH = 0.16
    PACE = (0.9, 1.9)
    MOVE = (0.5, 1.6)
    SHADE = (80, 40)
    HEALTH_MAX = 100.0

    def hero_draw(self, frame):
        return twin_draw(frame)

    def foe_draw(self, kind, frame):
        return bee_draw(frame) if kind == 1 else blob_draw(frame, ((240, 110, 160), (120, 120, 240))[frame // 2 % 2])

    def slash_fx(self, hx, hy, now):
        S = self.S
        self.fx.glow(hx + S(90), hy - S(70), 16, 70, (255, 255, 220), 0.2, "front", 1.0, 0.0)
        self.fx.sparks(hx + S(90), hy - S(70), 6, (255, 250, 200), (150, 400), (-60, 60), (0.12, 0.25), 200, "front", 3, 12)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: VITAL in its blue gauge and the time at the top, SCORE and the lives at the bottom.
        / VITAL dans sa jauge bleue et le temps en haut, SCORE et les vies en bas."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(440), S(84), now)
        hp = _n(vals.get("health"))
        if hp is not None:
            self.gauge(screen, S(14), S(14), S(300), "VITAL", hp / 100.0, (60, 150, 255), back=(20, 30, 60))
        t = _n(vals.get("time"))
        if t is not None:
            self.label(screen, f"TIME-{int(t)}", W / 2 + S(330), S(40), 30, (255, 255, 255), key="black", align="center")
        self.pill(screen, S(14), H - S(70), S(420), S(58), 160, radius=12)
        self.text(screen, "SCORE", S(32), H - S(41), 24, (255, 230, 120), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(420), H - S(62), "right", S(38))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.label(screen, f"x{int(lives)}", S(480), H - S(41), 30, (120, 255, 160), align="center")
        if self.p2_in(vals):
            hp2 = _n(vals.get("health_p2"))
            if hp2 is not None:
                self.gauge(screen, W - S(444), S(14), S(300), "VITAL", hp2 / 100.0, (60, 150, 255), back=(20, 30, 60))
        else:
            self.invite_right(screen, vals, now, S(110))


# ============================================================================ Magic Sword
MS_PARTNERS = {0: ("NINJA", "NINJA", "ninja", (60, 60, 80)), 2: ("BIGFOOT", "BIGFOOT", "mutant", (150, 110, 70)),
               4: ("PRÊTRE", "PRIEST", "jacket", (230, 230, 240)), 6: ("MAGICIEN", "MAGICIAN", "ninja", (120, 60, 160)),
               8: ("AMAZONE", "AMAZON", "brawler", (60, 140, 80)), 10: ("CHEVALIER", "KNIGHT", "samurai", (170, 176, 190)),
               12: ("VOLEUR", "THIEF", "thug", (90, 70, 50)), 14: ("HOMME-LÉZARD", "LIZARDMAN", "mutant", (90, 160, 80))}


def swordsman_draw(frame):
    """Our own sword hero of the tower: red hair and a headband, a silver breastplate, a red cape, a great sword held
    up or swung forward. / Notre héros à l'épée : cheveux roux et bandeau, cuirasse d'argent, cape rouge, grande épée."""
    def fn(d, W, H):
        ow = max(1.0, H * 0.012)
        d.polygon([(W * 0.36, H * 0.34), (W * 0.48, H * 0.34), (W * 0.3, H * 0.86), (W * 0.1, H * 0.8)], fill=(190, 40, 40, 255), outline=DARKLINE)
        step = {1: 0.06, 2: -0.06}.get(frame, 0.0)
        for k, sx in ((0, -1), (1, 1)):
            dx = sx * step * W
            _capsule(d, (W * (0.44 + 0.06 * k), H * 0.62), (W * (0.42 + 0.06 * k) + dx, H * 0.95), H * 0.07, H * 0.06, (120, 80, 50, 255), DARKLINE, ow)
            d.rounded_rectangle([W * (0.36 + 0.06 * k) + dx, H * 0.92, W * (0.52 + 0.06 * k) + dx, H * 0.99], radius=H * 0.02, fill=(90, 56, 30, 255),
                                outline=DARKLINE, width=int(ow))
        d.rounded_rectangle([W * 0.32, H * 0.34, W * 0.64, H * 0.64], radius=H * 0.05, fill=(196, 202, 216, 255), outline=DARKLINE, width=int(ow))
        d.rectangle([W * 0.32, H * 0.56, W * 0.64, H * 0.62], fill=(120, 80, 40, 255))
        hand = (W * 0.86, H * 0.42) if frame == 3 else (W * 0.62, H * 0.5)
        _capsule(d, (W * 0.5, H * 0.4), hand, H * 0.07, H * 0.06, _c(SKIN), DARKLINE, ow)
        tip = (hand[0] + W * 0.14, hand[1] + H * 0.02) if frame == 3 else (hand[0] + W * 0.1, hand[1] - H * 0.44)
        d.line([hand, tip], fill=(236, 240, 252, 255), width=int(ow * 6))
        d.line([hand, tip], fill=(160, 170, 200, 255), width=int(ow * 2))
        perp = (tip[1] - hand[1], hand[0] - tip[0])
        ln = math.hypot(*perp) or 1
        px, py = perp[0] / ln * W * 0.07, perp[1] / ln * W * 0.07
        d.line([(hand[0] - px, hand[1] - py), (hand[0] + px, hand[1] + py)], fill=(220, 180, 60, 255), width=int(ow * 4))
        hx, hy = W * 0.48, H * 0.21
        d.ellipse([hx - H * 0.1, hy - H * 0.11, hx + H * 0.1, hy + H * 0.11], fill=_c(SKIN), outline=DARKLINE, width=int(ow))
        d.chord([hx - H * 0.11, hy - H * 0.13, hx + H * 0.1, hy + H * 0.06], 160, 360, fill=(200, 70, 30, 255))
        d.polygon([(hx - H * 0.11, hy - H * 0.04), (hx - H * 0.2, hy + H * 0.08), (hx - H * 0.08, hy + H * 0.04)], fill=(200, 70, 30, 255))
        d.line([(hx - H * 0.1, hy - H * 0.04), (hx + H * 0.1, hy - H * 0.04)], fill=(60, 100, 220, 255), width=int(ow * 3))
        d.ellipse([hx + H * 0.03, hy - H * 0.01, hx + H * 0.06, hy + H * 0.03], fill=DARKLINE)
    return fn


def bat_draw(frame):
    """A purple bat of our own. / Une chauve-souris violette à nous."""
    def fn(d, W, H):
        up = frame % 2 == 0
        for side in (-1, 1):
            tipy = H * (0.05 if up else 0.85)
            d.polygon([(W * 0.5, H * 0.45), (W * (0.5 + side * 0.48), tipy), (W * (0.5 + side * 0.36), H * 0.6), (W * (0.5 + side * 0.2), H * 0.5)],
                      fill=(110, 60, 140, 255), outline=DARKLINE)
        d.ellipse([W * 0.38, H * 0.3, W * 0.62, H * 0.72], fill=(90, 50, 120, 255), outline=DARKLINE)
        for ex in (0.44, 0.53):
            d.ellipse([W * ex, H * 0.42, W * (ex + 0.05), H * 0.5], fill=(255, 220, 60, 255))
    return fn


class MagicSwordScene(SideQuestScene):
    """Magic Sword as in the game: a floor of the tower, the grey stones, the windows on the night, the statues of monsters
    in their niches, the torches; our sword hero of our own and his partner read in the game (ninja, priest, knight,
    thief...) cut down the orcs and the bats. 1PLAYER and the score, VITAL, the keys and the floor. / Un étage de la tour,
    les statues de monstres dans leurs niches ; notre héros à l'épée et le compagnon lu dans le jeu abattent les orques
    et les chauves-souris."""
    THEME = "ms_tower"
    FLOOR = MS_FLOOR
    HERO = (170, 200)
    FOE = (160, 190)
    FLYER = (100, 70)
    SHOT = "slash"
    REACH = 0.2
    PACE = (1.0, 2.2)
    MOVE = (0.3, 1.0)
    SHADE = (90, 60)
    BANNERS = GameScene.BANNERS + tuple((f"FLOOR {k}", (255, 220, 120)) for k in range(1, 6))

    def __init__(self, hd, rng=None):
        self.partner = 0
        super().__init__(hd, rng)
        self.floors = 0                                   # (tests)

    def hero_draw(self, frame):
        return swordsman_draw(frame)

    def foe_draw(self, kind, frame):
        if kind == 1:
            return bat_draw(frame)
        return fighter_draw("mutant", (90, 120, 60), (70, 50, 40), (110, 160, 80), (40, 60, 30), 1 + frame % 2)

    def partner_img(self, frame):
        S = self.S
        fr, en, style, col = MS_PARTNERS.get(self.partner, MS_PARTNERS[0])
        return self.img(("mspartner", self.partner, frame), S(130), S(160), fighter_draw(style, col, _mix(col, (0, 0, 0), 0.4), SKIN, (50, 40, 30),
                                                                                            frame), ss=2)

    def slash_fx(self, hx, hy, now):
        S = self.S
        for i in range(6):
            a = math.radians(-60 + i * 24)
            self.fx.later(i * 0.015, self.fx.glow, hx + S(60) + math.cos(a) * S(110), hy - S(110) + math.sin(a) * S(110), 10, 40, (255, 240, 200),
                          0.18, "front", 1.0, 0.0, 0.0, 0.6)

    def always(self, vals, now):
        v = _n(vals.get("partner"))
        if v is not None and int(v) in MS_PARTNERS and int(v) != self.partner:
            self.partner = int(v)
            if self.p1_in(vals) and not self.nobody(vals):
                self.popup(tr(*MS_PARTNERS[self.partner][:2]), self.W * self.HERO_X - self.S(130), self.floor() - self.S(200), (120, 220, 255), 30)
        ch = self.changed(vals, "floor")
        if ch and ch[1] > ch[0] and not self.nobody(vals):
            self.floors += 1
            self.slam(f"FLOOR {int(ch[1]) + 1}", (255, 220, 120), now, 1.2)

    def draw_hero(self, screen, vals, now):
        if self.p1_in(vals):
            img = self.partner_img(1 + int(now * 6 + 1) % 2)
            hx, hy = self.hero_xy(now)
            screen.blit(img, (int(hx - self.S(140) - img.get_width() / 2), int(self.floor() - img.get_height())))
        super().draw_hero(screen, vals, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1PLAYER and the score, VITAL in segments, the keys, the floor. / 1PLAYER, VITAL, clés, étage."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(440), S(84), now)
        self.side_score(screen, eng, vals, "1PLAYER", S(14), S(6), (255, 255, 255))
        hp = _n(vals.get("health"))
        if hp is not None:
            self.pill(screen, S(14), S(104), S(300), S(44), 160, radius=12)
            self.text(screen, "VITAL", S(30), S(126), 22, (255, 230, 120), key="black", valign="middle", glow=0)
            for i in range(8):                                          # VITAL in segments / en segments
                on = i < int(math.ceil(hp / 12.5))
                pg.draw.rect(screen, (250, 200, 50) if on else (60, 50, 30), (S(124) + i * S(22), S(114), S(18), S(24)), border_radius=S(3))
        floor = _n(vals.get("floor"))
        if floor is not None:
            self.label(screen, f"FLOOR {int(floor) + 1}", W / 2 + S(330), S(40), 30, (255, 220, 120), key="black", align="center")
        keys = _n(vals.get("keys"))
        if keys is not None:
            self.label(screen, f"KEY x{int(keys)}", W / 2 + S(330), S(100), 26, (250, 210, 80), align="center")
        if self.p2_in(vals):
            self.side_score(screen, eng, vals, "2PLAYER", W - S(14), S(6), (255, 255, 255), "score_p2", align="right")
        else:
            self.invite_right(screen, vals, now)


SCENES = {"ghouls": GhoulsScene, "strider": StriderScene, "pang3": Pang3Scene, "mpang": MightyPangScene, "spf2t": PuzzleFighterScene, "mtwins": MegaTwinsScene, "msword": MagicSwordScene}
__all__ = ["SCENES", "SideQuestScene"]
_KEEP = (AMBER, P1C, P2C, draw_img)
