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
from .hd_themes14 import GG_FLOOR, ST_FLOOR
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
            if not f.get("dead"):
                if f["x"] > hx + S(120) or f["kind"] == 1:
                    f["x"] -= f["v"] * dt
                else:
                    f["x"] -= self.bd.speed * dt                       # held at the hero / tenu devant le héros
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


SCENES = {"ghouls": GhoulsScene, "strider": StriderScene}
__all__ = ["SCENES", "SideQuestScene"]
_KEEP = (AMBER, P1C, P2C, draw_img)
