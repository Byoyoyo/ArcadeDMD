"""HD scenes of the fifth batch of Neo Geo games done one by one (1.21), each drawn after screenshots of its game.
Each game has its own animated backdrop and reacts to the values read in its memory. The characters, the soldiers
and the machines are creations of the program in the spirit of the games.

Scènes HD du cinquième lot de jeux Neo Geo faits un par un (1.21), chacune dessinée d'après des captures de son jeu.
Les personnages, les soldats et les engins sont des créations du programme dans l'esprit des jeux.
"""

import math

from .hd_games import CREAM, GOLD, P1C, P2C, RED, WHITE, BlazingStarScene, GameScene, Machines, _clamp, _n, draw_img, drone_draw
from .hd_games3 import DARK, AeroFightersScene, _capsule, bomber_draw, heli_draw, lr_ship_draw
from .hd_themes5 import BRAWL_FLOOR, CL_FLOOR, GP_LANES, NAM_ROAD, ST2_ROAD                    # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr


# ============================================================================ NAM-1975
NAM_WEAPONS = {0: ("FUSIL", "RIFLE"), 1: ("MITRAILLEUSE", "MACHINE GUN"), 2: ("LANCE-FLAMMES", "FLAMETHROWER"), 8: ("BAZOOKA", "BAZOOKA")}


def trooper_back_draw(frame, shirt=(86, 110, 56), helmet=(70, 96, 50)):
    """Our soldier seen from behind, as the hero of the game is: green helmet, olive shirt, the straps of his pack,
    the rifle held up in front of him. Frames 0 aim, 1 fire, 2 throw. / Notre soldat vu de dos, comme le héros du jeu."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, W * 0.02)
        olive, olive_d = shirt + (255,), tuple(int(c * 0.7) for c in shirt) + (255,)
        skin = (214, 160, 120, 255)
        for i, x in enumerate((0.36, 0.64)):                           # jambes, bottes
            _capsule(d, (W * 0.5 + (x - 0.5) * W * 0.5, H * 0.62), (W * x, H * 0.92), W * 0.09, W * 0.08, olive_d if i == 0 else olive, dark, ow)
            d.rounded_rectangle([W * x - W * 0.09, H * 0.9, W * x + W * 0.09, H * 0.99], radius=W * 0.04, fill=(40, 34, 28, 255), outline=dark)
        d.rounded_rectangle([W * 0.24, H * 0.3, W * 0.76, H * 0.66], radius=W * 0.1, fill=olive, outline=dark, width=int(ow))   # le dos
        d.rounded_rectangle([W * 0.34, H * 0.34, W * 0.66, H * 0.56], radius=W * 0.05, fill=(110, 96, 60, 255), outline=dark)  # le sac
        for x in (0.36, 0.64):
            d.line([(W * x, H * 0.3), (W * x, H * 0.36)], fill=(70, 56, 36, 255), width=max(2, int(W * 0.03)))
        if frame == 2:                                                 # bras levé pour lancer
            _capsule(d, (W * 0.7, H * 0.34), (W * 0.84, H * 0.08), W * 0.07, W * 0.06, olive, dark, ow)
            d.ellipse([W * 0.78, H * 0.02, W * 0.9, H * 0.12], fill=(70, 100, 50, 255), outline=dark)
            _capsule(d, (W * 0.3, H * 0.34), (W * 0.4, H * 0.24), W * 0.07, W * 0.06, olive_d, dark, ow)
        else:                                                          # les deux mains sur le fusil, levé devant
            up = 0.02 if frame == 1 else 0.0
            for sx in (0.3, 0.7):
                _capsule(d, (W * sx, H * 0.36), (W * 0.52, H * (0.2 + up)), W * 0.07, W * 0.06, olive if sx > 0.5 else olive_d, dark, ow)
            d.line([(W * 0.5, H * (0.3 + up)), (W * 0.56, H * (0.02 + up))], fill=(40, 40, 44, 255), width=max(3, int(W * 0.06)))
        d.ellipse([W * 0.4, H * 0.24, W * 0.6, H * 0.34], fill=skin, outline=dark)                                           # la nuque
        d.chord([W * 0.3, H * 0.1, W * 0.7, H * 0.36], 180, 360, fill=helmet + (255,), outline=dark, width=int(ow))          # le casque
        d.rectangle([W * 0.3, H * 0.22, W * 0.7, H * 0.25], fill=tuple(int(c * 0.78) for c in helmet) + (255,))
    return fn


def grunt_draw(frame):
    """An enemy soldier running to the right: khaki, a cap, a rifle. Frames 0 and 1 run, 2 falls.
    / Un soldat ennemi qui court vers la droite, kaki, casquette, fusil."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, W * 0.025)
        kh, kh_d = (176, 150, 96, 255), (130, 108, 66, 255)
        skin = (200, 150, 110, 255)
        if frame == 2:
            d.ellipse([W * 0.1, H * 0.7, W * 0.9, H * 0.96], fill=kh, outline=dark, width=int(ow))
            d.ellipse([W * 0.72, H * 0.66, W * 0.96, H * 0.88], fill=skin, outline=dark)
            return
        step = (0.16, -0.12) if frame == 0 else (-0.14, 0.14)
        for i, dx in enumerate(step):
            k = (W * (0.5 + dx * 0.6), H * 0.78)
            _capsule(d, (W * 0.5, H * 0.56), k, W * 0.08, W * 0.07, kh_d if i == 0 else kh, dark, ow)
            _capsule(d, k, (W * (0.5 + dx), H * 0.97), W * 0.07, W * 0.06, kh_d if i == 0 else kh, dark, ow)
        d.rounded_rectangle([W * 0.34, H * 0.26, W * 0.66, H * 0.58], radius=W * 0.08, fill=kh, outline=dark, width=int(ow))
        _capsule(d, (W * 0.56, H * 0.32), (W * 0.84, H * 0.42), W * 0.06, W * 0.05, kh, dark, ow)
        d.line([(W * 0.6, H * 0.44), (W * 0.98, H * 0.38)], fill=(40, 40, 40, 255), width=max(2, int(W * 0.05)))
        d.ellipse([W * 0.38, H * 0.06, W * 0.66, H * 0.3], fill=skin, outline=dark, width=int(ow))
        d.chord([W * 0.36, H * 0.03, W * 0.68, H * 0.22], 180, 360, fill=(110, 96, 60, 255))
        d.rectangle([W * 0.5, H * 0.12, W * 0.78, H * 0.15], fill=(110, 96, 60, 255))
    return fn


def tank_side_draw(d, W, H):
    """A green tank seen from the side, gun to the right. / Un char vert de profil, canon à droite."""
    dark = (24, 28, 20, 255)
    d.rounded_rectangle([W * 0.04, H * 0.62, W * 0.9, H * 0.98], radius=H * 0.16, fill=(50, 54, 44, 255), outline=dark, width=max(1, int(H * 0.03)))
    for k in range(7):
        x = W * (0.1 + k * 0.12)
        d.ellipse([x - H * 0.1, H * 0.7, x + H * 0.1, H * 0.92], fill=(90, 92, 80, 255), outline=dark)
    d.polygon([(W * 0.06, H * 0.62), (W * 0.12, H * 0.42), (W * 0.84, H * 0.42), (W * 0.92, H * 0.62)], fill=(90, 120, 60, 255), outline=dark)
    d.rounded_rectangle([W * 0.3, H * 0.16, W * 0.66, H * 0.44], radius=H * 0.08, fill=(100, 130, 66, 255), outline=dark, width=max(1, int(H * 0.03)))
    d.rectangle([W * 0.64, H * 0.24, W * 0.99, H * 0.31], fill=(70, 90, 50, 255), outline=dark)
    d.line([(W * 0.36, H * 0.24), (W * 0.6, H * 0.24)], fill=(150, 176, 110, 255), width=max(1, int(H * 0.03)))


class NamScene(GameScene):
    """NAM-1975 as in the game: our soldier seen from behind at the bottom of the screen shoots into the burning city
    (then the jungle and its river), the enemies run along the road, tanks and helicopters cross. The bullets, the
    grenades and the weapon read in the game are shown, a grenade blows up where the crosshair is.
    / Notre soldat vu de dos tire dans la ville en feu, comme dans le jeu."""
    CREDITS = (-420, None)                                # our soldier is in the middle / notre soldat est au milieu
    THEME = "nam_city"
    SHADE = (90, 60)
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.bd.prebuild(["nam_jungle"])
        self.foes = []
        self.next_foe = 0.0
        self.aim = [self.W * 0.5, self.S(NAM_ROAD) - self.S(30)]
        self.target = None
        self.fire_t = 0.0
        self.burst = 0
        self.throw_t = -99.0
        self.throw_t2, self.fire_t2 = -99.0, 0.0          # the second soldier / le second soldat
        self.kills = 0                                    # (tests)
        self.grenades = 0
        self.fx.sp.register("namgren", draw_img(self.S(26), self.S(30), lambda d, W, H: (
            d.ellipse([W * 0.1, H * 0.25, W * 0.9, H - 1], fill=(70, 100, 50, 255), outline=(24, 34, 16, 255)),
            d.rectangle([W * 0.36, 0, W * 0.64, H * 0.3], fill=(150, 150, 150, 255)))))
        self.warm = [(self.trooper, (f,)) for f in range(3)] + [(self.grunt, (f, False)) for f in range(3)] + self.warm

    def trooper(self, frame, side="p1"):
        S = self.S
        if side == "p2":                                               # the second soldier, in blue as in the game
            return self.img(("namtrooper", frame, side), S(150), S(210), trooper_back_draw(frame, (60, 90, 170), (50, 76, 150)), ss=2)
        return self.img(("namtrooper", frame), S(150), S(210), trooper_back_draw(frame), ss=2)

    def stand(self, side):
        """Where a soldier stands, from the middle of the screen. / Où se tient un soldat."""
        return self.W * (0.44 if side == "p1" else 0.56)

    def grunt(self, frame, left):
        S = self.S
        return self.img(("namgrunt", frame, left), S(92), S(144), grunt_draw(frame), ss=2, flip=left)

    def move(self, vals, now, idle):
        return 0.2 if idle else 0.5

    def restart(self, vals, now):
        self.foes = []
        self.next_foe = now + 0.8

    def update(self, vals, now):
        S, rng, dt = self.S, self.rng, self.dt
        road = S(NAM_ROAD)
        if now >= self.next_foe:                                       # enemies run along the road, tanks and helicopters cross
            self.next_foe = now + rng.uniform(0.3, 0.8)
            left = rng.random() < 0.5
            kind = rng.choices(("grunt", "tank", "heli"), (8, 1, 1))[0]
            y = road + rng.uniform(-S(14), S(16)) if kind != "heli" else S(rng.uniform(80, 150))
            self.foes.append({"kind": kind, "x": -S(80) if left else self.W + S(80), "y": y, "v": (1 if left else -1) * rng.uniform(140, 240) * self.s
                              * (0.4 if kind == "tank" else 1.0), "hp": {"grunt": 3, "tank": 8, "heli": 6}[kind], "ph": rng.uniform(0, 6),
                              "t0": now})
        live = [f for f in self.foes if not f.get("dead") and 0 < f["x"] < self.W]
        if self.target not in live:
            self.target = min(live, key=lambda f: abs(f["x"] - self.W / 2)) if live else None
        if self.target is not None:                                    # the crosshair follows the target
            tx, ty = self.target["x"], self.target["y"] - S(40)
        else:
            tx, ty = self.W / 2 + math.sin(now * 0.7) * S(300), road - S(40)
        self.aim[0] += (tx - self.aim[0]) * min(1.0, dt * 5)
        self.aim[1] += (ty - self.aim[1]) * min(1.0, dt * 5)
        suf = ""
        w = int(_n(vals.get("weapon" + suf)) or 0)
        ch = self.changed(vals, "ammo")
        if ch and ch[1] < ch[0]:
            for i in range(min(3, int(ch[0] - ch[1]))):
                self.fx.later(i * 0.07, self.shoot, w, now)
        elif now >= self.fire_t and self.target is not None:           # bursts at the target
            if self.burst <= 0:
                self.burst = rng.randint(3, 7)
            self.shoot(w, now)
            self.burst -= 1
            self.fire_t = now + (0.1 if self.burst > 0 else rng.uniform(0.4, 1.0))
        ch = self.changed(vals, "grenades")
        if ch and ch[1] < ch[0]:                                       # a grenade where the crosshair is
            self.grenades += 1
            self.throw_t = now
            x0, y0 = self.W * 0.42, self.H - S(180)
            self.fx.projectile("namgren", x0, y0, self.aim[0], self.aim[1] + S(30), 0.8, 200, self.blast, spin=600)
        ch = self.changed(vals, "weapon")
        if ch:
            self.popup(tr(*NAM_WEAPONS.get(int(ch[1]), NAM_WEAPONS[0])) + " !", self.W * 0.42, S(300), GOLD, 40)
        if self.p2_in(vals):                                           # the second soldier: his gun, his grenades
            w2 = int(_n(vals.get("weapon_p2")) or 0)
            ch = self.changed(vals, "ammo_p2")
            if ch and ch[1] < ch[0]:
                for i in range(min(3, int(ch[0] - ch[1]))):
                    self.fx.later(i * 0.07, self.shoot, w2, now, "p2")
            elif now >= self.fire_t2 and self.target is not None:
                self.shoot(w2, now, "p2")
                self.fire_t2 = now + rng.uniform(0.12, 0.7)
            ch = self.changed(vals, "grenades_p2")
            if ch and ch[1] < ch[0]:
                self.throw_t2 = now
                self.fx.projectile("namgren", self.stand("p2") + S(20), self.H - S(180), self.aim[0], self.aim[1] + S(30), 0.8, 200,
                                   self.blast, spin=600)
            ch = self.changed(vals, "weapon_p2")
            if ch:
                self.popup(tr(*NAM_WEAPONS.get(int(ch[1]), NAM_WEAPONS[0])) + " !", self.stand("p2"), S(300), GOLD, 40)
        for side, suf2 in (("p1", ""), ("p2", "_p2")):                 # a life lost / une vie perdue
            ch = self.changed(vals, "lives" + suf2)
            if ch and ch[1] < ch[0] and (self.p1_in(vals) if side == "p1" else self.p2_in(vals)):
                self.fx.explosion(self.stand(side), self.H - S(120), 0.8, False)
                self.fx.shake(8, 0.4)
                self.popup(tr("-1 VIE", "-1 LIFE"), self.stand(side), S(300), (255, 90, 70), 38)
        ch = self.changed(vals, "score")
        t = self.target
        if ch and ch[1] > ch[0] and t is not None and now - t["t0"] > 1.0 and S(60) < t["x"] < self.W - S(60):
            self.kill(t, now)                                          # points: the enemy in the crosshair falls
        keep = []
        for f in self.foes:
            if f.get("dead") and now - f["dead"] > 1.2:
                continue
            if not f.get("dead"):
                f["x"] += f["v"] * dt
            if -S(200) < f["x"] < self.W + S(200):
                keep.append(f)
        self.foes = keep

    def shoot(self, w, now, side="p1"):
        S, fx = self.S, self.fx
        x0, y0 = self.stand(side), self.H - S(214)
        ax, ay = self.aim
        if w == 2:                                                     # flamethrower
            fx.sparks(x0, y0, 12, (255, 160, 60), (500, 900), (250, 290), (0.3, 0.5), -200, "front", 10, 40)
        elif w == 8:                                                   # bazooka
            fx.tracer(x0, y0, ax, ay, 1600, (255, 200, 120), 10, 70, "front", False)
            fx.later(0.25, fx.explosion, ax, ay, 0.6, False)
        else:
            fx.tracer(x0, y0, ax + self.rng.uniform(-S(20), S(20)), ay + self.rng.uniform(-S(14), S(14)), 3200, (255, 240, 170), 4, 60, "front", True)
        fx.muzzle(x0, y0, 0, 0.5)
        t = self.target
        if t is not None and not t.get("dead") and self.rng.random() < 0.45:
            t["hp"] -= 2 if w in (2, 8) else 1
            if t["hp"] <= 0 and self.rng.random() < 0.6:
                self.kill(t, now)

    def kill(self, f, now):
        if f.get("dead"):
            return
        f["dead"] = now
        self.kills += 1
        if f["kind"] != "grunt":
            self.fx.explosion(f["x"], f["y"] - self.S(30), 0.9, False)

    def blast(self, x, y):
        S = self.S
        self.fx.explosion(x, y, 1.1, False)
        self.fx.shake(8, 0.4)
        for f in self.foes:
            if not f.get("dead") and abs(f["x"] - x) < S(220):
                self.kill(f, self.fx.now)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        for f in sorted(self.foes, key=lambda f: f["y"]):
            if f["kind"] == "grunt":
                img = self.grunt(2 if f.get("dead") else int(now * 8 + f["ph"]) % 2, f["v"] < 0)
                screen.blit(img, (int(f["x"] - img.get_width() / 2), int(f["y"] - img.get_height())))
            elif f["kind"] == "tank":
                img = self.img(("namtank", f["v"] < 0), S(220), S(110), tank_side_draw, flip=f["v"] < 0)
                if not f.get("dead") or int(now * 10) % 2:
                    screen.blit(img, (int(f["x"] - img.get_width() / 2), int(f["y"] - img.get_height() + S(10))))
            else:                                                      # helicopter, from the Aero Fighters
                img = self.img(("namheli", f["v"] < 0), S(150), S(90), heli_draw, flip=f["v"] > 0)
                if not f.get("dead"):
                    screen.blit(img, (int(f["x"] - img.get_width() / 2), int(f["y"] - img.get_height() / 2)))
        ax, ay = self.aim                                              # the green crosshair
        r = S(30)
        col = (80, 255, 120)
        for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            pg.draw.line(screen, col, (int(ax + sx * r), int(ay + sy * r)), (int(ax + sx * r * 0.45), int(ay + sy * r)), S(3))
            pg.draw.line(screen, col, (int(ax + sx * r), int(ay + sy * r)), (int(ax + sx * r), int(ay + sy * r * 0.45)), S(3))
        sway = math.sin(now * 1.3) * S(30) + (self.aim[0] - self.W / 2) * 0.08
        if self.p1_in(vals):
            frame = 2 if now - self.throw_t < 0.4 else (1 if now < self.fire_t - 0.05 else 0)
            img = self.trooper(frame)
            screen.blit(img, (int(self.stand("p1") - img.get_width() / 2 + sway), int(self.H - img.get_height() + S(6))))
        if self.p2_in(vals):
            frame = 2 if now - self.throw_t2 < 0.4 else (1 if now < self.fire_t2 - 0.05 else 0)
            img = self.trooper(frame, "p2")
            screen.blit(img, (int(self.stand("p2") - img.get_width() / 2 + sway), int(self.H - img.get_height() + S(6))))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P, the lives and the score at the top, the grenades below, the weapon and its bullets; the
        second player has the same on the right. / Comme dans le jeu : 1P, les vies et le score en haut, les grenades
        dessous, l'arme et ses balles ; le second joueur a la même chose à droite."""
        S, W, hd = self.S, self.W, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        for side, suf, tag, col in (("p1", "", "1P", (255, 230, 120)), ("p2", "_p2", "2P", (130, 190, 255))):
            if side == "p2" and not self.p2_in(vals):                  # the INSERT COIN box, as in the game
                word, colw = self.invite(vals, now)
                self.box(screen, W - S(300), S(10), S(280), S(80), (230, 120, 40), fill=(10, 10, 20, 200), radius=6, width=3)
                self.text(screen, word, W - S(160), S(50), 30, colw, key="stencil", align="center", valign="middle")
                continue
            if side == "p1" and not self.p1_in(vals):
                continue
            X, near, far = self.mirror(side)
            self.pill(screen, X(16, 420), S(10), S(420), S(64), 150)
            tw = self.text(screen, tag, X(36), S(42), 32, col, key="black", align=near, valign="middle")
            lives = _n(vals.get("lives" + suf))
            if lives is not None:                                      # the small figure by the helmet / le chiffre près du casque
                lx = X(36) + (tw + S(12) if side == "p1" else -tw - S(12))
                self.text(screen, f"x{int(lives)}", lx, S(44), 24, WHITE, key="black", align=near, valign="middle", glow=0)
            if _n(vals.get("score" + suf)) is not None:
                hd._score(screen, eng, "score" + suf, X(410), S(16), far, S(48))
            g = _n(vals.get("grenades" + suf))
            if g is not None:
                self.pill(screen, X(16, 170), S(84), S(170), S(56), 150)
                icon = self.fx.sp.obj("namgren", 0)
                screen.blit(icon, (X(30, 26), S(96)))
                self.text(screen, f"{int(g):02d}", X(160), S(112), 34, WHITE, key="black", align=far, valign="middle")
            w = _n(vals.get("weapon" + suf))
            a = _n(vals.get("ammo" + suf))
            if w is not None and int(w) in NAM_WEAPONS and int(w) != 0:
                self.label(screen, tr(*NAM_WEAPONS[int(w)]) + (f"  {int(a):02d}" if a is not None else ""), X(250), S(112), 26, GOLD,
                           align=near)


# ============================================================================ Cyber-Lip
CL_WEAPONS = (("ammo_auto", "AUTO", (255, 230, 120)), ("ammo_wide", "WIDE", (120, 220, 255)), ("ammo_fire", "FIRE", (255, 140, 60)),
              ("ammo_bazooka", "BAZOOKA", (255, 200, 140)), ("ammo_grenade", "GRENADE", (160, 230, 120)))


def gunner_draw(frame, vest_c=(130, 140, 156)):
    """Our hero of the city, seen from the side, facing right: a red bandana, a grey armoured vest, brown trousers,
    a big gun held at the hip. Frames 0 and 1 run, 2 fire. / Notre héros de la ville, de profil, face à droite."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, W * 0.025)
        skin = (226, 176, 136, 255)
        vest, vest_d = vest_c + (255,), tuple(int(c * 0.7) for c in vest_c) + (255,)
        pants, pants_d = (120, 84, 50, 255), (90, 62, 36, 255)
        u = H
        cx = W * 0.44
        step = (0.13, -0.11) if frame == 0 else ((-0.11, 0.13) if frame == 1 else (0.08, -0.06))
        for i, dx in enumerate(step):
            k = (cx + dx * 0.55 * u, H * 0.77)
            f = (cx + dx * u, H * 0.96)
            _capsule(d, (cx, H * 0.56), k, 0.06 * u, 0.055 * u, pants_d if i == 0 else pants, dark, ow)
            _capsule(d, k, f, 0.05 * u, 0.045 * u, pants_d if i == 0 else pants, dark, ow)
            d.rounded_rectangle([f[0] - 0.05 * u, f[1] - 0.04 * u, f[0] + 0.07 * u, f[1] + 0.02 * u], radius=0.02 * u, fill=(40, 34, 30, 255),
                                outline=dark)
        d.rounded_rectangle([cx - 0.1 * u, H * 0.27, cx + 0.11 * u, H * 0.58], radius=0.04 * u, fill=vest, outline=dark, width=int(ow))
        d.rectangle([cx - 0.1 * u, H * 0.44, cx + 0.11 * u, H * 0.48], fill=vest_d)
        d.rounded_rectangle([cx - 0.14 * u, H * 0.26, cx - 0.02 * u, H * 0.36], radius=0.03 * u, fill=vest_d, outline=dark)       # épaulière
        gy = H * (0.44 if frame != 2 else 0.42)
        d.rounded_rectangle([cx - 0.02 * u, gy - 0.04 * u, cx + 0.4 * u, gy + 0.04 * u], radius=0.02 * u, fill=(60, 64, 76, 255), outline=dark,
                            width=int(ow))                              # le gros fusil
        d.rectangle([cx + 0.36 * u, gy - 0.02 * u, cx + 0.46 * u, gy + 0.02 * u], fill=(40, 40, 46, 255))
        d.rectangle([cx + 0.08 * u, gy + 0.03 * u, cx + 0.14 * u, gy + 0.1 * u], fill=(60, 64, 76, 255), outline=dark)
        _capsule(d, (cx + 0.03 * u, H * 0.32), (cx + 0.16 * u, gy), 0.045 * u, 0.04 * u, skin, dark, ow)
        hx, hy = cx + 0.02 * u, H * 0.15                               # la tête
        r = 0.085 * u
        d.ellipse([hx - r, hy - r, hx + r, hy + r * 1.1], fill=skin, outline=dark, width=int(ow))
        d.ellipse([hx + r * 0.35, hy - r * 0.15, hx + r * 0.6, hy + r * 0.1], fill=dark)
        d.chord([hx - r * 1.02, hy - r * 1.08, hx + r * 0.98, hy + r * 0.2], 180, 360, fill=(40, 30, 26, 255))                     # cheveux
        d.rectangle([hx - r, hy - r * 0.42, hx + r * 0.95, hy - r * 0.2], fill=(210, 40, 40, 255))                                # bandana
        d.polygon([(hx - r, hy - r * 0.4), (hx - r * 1.7, hy - r * 0.1), (hx - r * 1.6, hy + r * 0.2), (hx - r * 0.95, hy - r * 0.22)],
                  fill=(210, 40, 40, 255))
    return fn


def walker_draw(frame):
    """A small walking robot of the city, facing left: a round body, one red eye, two legs.
    / Un petit robot marcheur de la ville, face à gauche, un œil rouge."""
    def fn(d, W, H):
        dark = (20, 22, 30, 255)
        ow = max(1.0, W * 0.03)
        body, body_d = (150, 156, 170, 255), (100, 106, 120, 255)
        step = (0.1, -0.1) if frame == 0 else (-0.1, 0.1)
        for i, dx in enumerate(step):
            _capsule(d, (W * 0.5, H * 0.6), (W * (0.5 + dx), H * 0.96), W * 0.07, W * 0.06, body_d if i == 0 else body, dark, ow)
        d.ellipse([W * 0.18, H * 0.16, W * 0.84, H * 0.66], fill=body, outline=dark, width=int(ow))
        d.chord([W * 0.18, H * 0.16, W * 0.84, H * 0.66], 200, 340, fill=(190, 196, 210, 255))
        d.ellipse([W * 0.2, H * 0.32, W * 0.44, H * 0.5], fill=(40, 10, 10, 255), outline=dark)
        d.ellipse([W * 0.24, H * 0.36, W * 0.38, H * 0.46], fill=(255, 60, 40, 255))
        d.line([(W * 0.2, H * 0.52), (W * 0.02, H * 0.5)], fill=(60, 64, 76, 255), width=max(2, int(W * 0.07)))
        d.line([(W * 0.6, H * 0.16), (W * 0.66, H * 0.04)], fill=dark, width=max(1, int(W * 0.03)))
        d.ellipse([W * 0.62, H * 0.0, W * 0.7, H * 0.06], fill=(255, 220, 80, 255))
    return fn


class CyberLipScene(GameScene):
    """Cyber-Lip as in the game: our hero runs down the city at night, past the theater and the shops, and shoots the
    walking robots and the drones that come. The weapon whose ammo goes down in the game is the one he fires (auto,
    wide, fire, bazooka, grenade). TIME and the score at the top, the weapon and its ammo in the blue bar at the bottom.
    / Notre héros parcourt la ville la nuit et tire sur les robots, comme dans le jeu."""
    THEME = "cl_city"
    SHADE = (90, 90)
    EXPLOSIONS = True
    TWO = True                                            # the second player's hero is drawn; a scene built on this one
                                                          # with a hero of its own says False until it draws two

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.foes = []
        self.next_foe = 0.0
        self.weapon = None                                # (name, colour) of the weapon in use / l'arme utilisée
        self.fire_t = 0.0
        self.hurt = -99.0
        self.weapon2, self.fire_t2, self.hurt2 = None, 0.0, -99.0     # the second player's / ceux du second joueur
        self.kills = 0                                    # (tests)
        self.shots = {}
        self.warm = [(self.hero, (f,)) for f in range(3)] + [(self.foe, (f,)) for f in range(2)] + self.warm

    def hero(self, frame, side="p1"):
        S = self.S
        if side == "p2":                                               # the second hero, in red as his half of the bar
            return self.img(("clhero", frame, side), S(170), S(200), gunner_draw(frame, (170, 70, 60)), ss=2)
        return self.img(("clhero", frame), S(170), S(200), gunner_draw(frame), ss=2)

    def hx(self, side):
        return self.W * (0.3 if side == "p1" else 0.2)

    def foe(self, frame):
        S = self.S
        return self.img(("clfoe", frame), S(100), S(120), walker_draw(frame), ss=2)

    def flyer(self, now):
        S = self.S
        return self.img("cldrone", S(90), S(60), drone_draw)

    def floor(self):
        return self.S(CL_FLOOR) + self.S(30)

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.5

    def restart(self, vals, now):
        self.foes = []
        self.next_foe = now + 0.6

    def update(self, vals, now):
        S, rng = self.S, self.rng
        if now >= self.next_foe:
            self.next_foe = now + rng.uniform(0.6, 1.4)
            fly = rng.random() < 0.3
            self.foes.append({"x": self.W + S(80), "y": S(rng.uniform(170, 260)) if fly else self.floor(), "fly": fly, "hp": 3,
                              "v": rng.uniform(80, 160) * self.s, "ph": rng.uniform(0, 6), "t0": now})
        for key, name, col in CL_WEAPONS:                              # the weapon whose ammo goes down
            ch = self.changed(vals, key)
            if ch and ch[1] < ch[0]:
                if self.weapon is None or self.weapon[0] != name:
                    self.popup(name + " !", self.W * 0.3, self.floor() - S(240), col, 40)
                self.weapon = (name, col)
                self.shots[name] = self.shots.get(name, 0) + 1
                self.fire(now)
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.hurt = now
            self.fx.explosion(self.W * 0.3, self.floor() - S(90), 0.8, False)
            self.popup(tr("-1 VIE", "-1 LIFE"), self.W * 0.3, self.floor() - S(240), (255, 90, 70), 38)
        if self.p2_in(vals):                                           # the second hero: his weapon, his lives
            for key, name, col in CL_WEAPONS:
                ch = self.changed(vals, key + "_p2")
                if ch and ch[1] < ch[0]:
                    if self.weapon2 is None or self.weapon2[0] != name:
                        self.popup(name + " !", self.hx("p2"), self.floor() - S(240), col, 40)
                    self.weapon2 = (name, col)
                    self.fire(now, "p2")
            ch = self.changed(vals, "lives_p2")
            if ch and ch[1] < ch[0]:
                self.hurt2 = now
                self.fx.explosion(self.hx("p2"), self.floor() - S(90), 0.8, False)
                self.popup(tr("-1 VIE", "-1 LIFE"), self.hx("p2"), self.floor() - S(240), (255, 90, 70), 38)
            if now >= self.fire_t2 and any(not f.get("dead") and self.W * 0.35 < f["x"] < self.W for f in self.foes):
                self.fire_t2 = now + rng.uniform(0.25, 0.6)
                self.fire(now, "p2")
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:
            live = [f for f in self.foes if not f.get("dead") and self.W * 0.35 < f["x"] < self.W * 0.95]
            if live:
                self.kill(min(live, key=lambda f: f["x"]), now)
        if now >= self.fire_t and any(not f.get("dead") and self.W * 0.35 < f["x"] < self.W for f in self.foes):
            self.fire_t = now + rng.uniform(0.25, 0.6)
            self.fire(now)

    def fire(self, now, side="p1"):
        S, fx = self.S, self.fx
        x0, y0 = self.hx(side) + S(80), self.floor() - S(110)
        name, col = (self.weapon if side == "p1" else self.weapon2) or ("NORMAL", (255, 240, 200))
        live = [f for f in self.foes if not f.get("dead") and f["x"] > x0]
        tgt = min(live, key=lambda f: f["x"]) if live else None
        tx, ty = (tgt["x"], tgt["y"] - (S(60) if not tgt["fly"] else 0)) if tgt else (self.W + S(50), y0)
        if name == "WIDE":
            for a in (-1, 0, 1):
                fx.tracer(x0, y0, tx, ty + a * S(60), 3000, col, 6, 80, "front", False)
        elif name == "FIRE":
            fx.sparks(x0, y0, 14, col, (700, 1100), (-12, 12), (0.25, 0.4), 0, "front", 10, 40)
        elif name in ("BAZOOKA", "GRENADE"):
            fx.tracer(x0, y0, tx, ty, 1500, col, 10, 60, "front", False)
            fx.later(abs(tx - x0) / (1500 * self.s), fx.explosion, tx, ty, 0.6, False)
        else:
            fx.tracer(x0, y0, tx, ty, 3200, col, 5, 90, "front", True)
        fx.muzzle(x0, y0, 1, 0.6)
        if tgt is not None:
            tgt["hp"] -= 3 if name in ("BAZOOKA", "GRENADE", "FIRE") else 1
            if tgt["hp"] <= 0:
                fx.later(0.1, self.kill, tgt, now)

    def kill(self, f, now):
        if f.get("dead"):
            return
        f["dead"] = now
        self.kills += 1
        self.fx.explosion(f["x"], f["y"] - (self.S(60) if not f["fly"] else 0), 0.55, False)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, dt = self.S, self.dt
        keep = []
        for f in self.foes:
            if f.get("dead"):
                continue
            f["x"] -= (f["v"] + self.bd.speed) * dt
            if f["x"] < self.W * 0.3 + S(70) and not f["fly"]:          # robots stop at the hero
                f["x"] = self.W * 0.3 + S(70)
            if f["x"] < -S(100):
                continue
            keep.append(f)
            if f["fly"]:
                img = self.flyer(now)
                yy = f["y"] + math.sin(now * 3 + f["ph"]) * S(16)
                screen.blit(img, (int(f["x"] - img.get_width() / 2), int(yy - img.get_height() / 2)))
            else:
                img = self.foe(int(now * 5 + f["ph"]) % 2)
                screen.blit(img, (int(f["x"] - img.get_width() / 2), int(f["y"] - img.get_height())))
        self.foes = keep
        if self.TWO and self.p2_in(vals) and not (now - self.hurt2 < 1.0 and int(now * 16) % 2):
            frame = 2 if now < self.fire_t2 - 0.15 else int(now * 8 + 1) % 2
            img = self.hero(frame, "p2")
            screen.blit(img, (int(self.hx("p2") - img.get_width() / 2), int(self.floor() - img.get_height())))
        if self.p1_in(vals) and not (now - self.hurt < 1.0 and int(now * 16) % 2):
            frame = 2 if now < self.fire_t - 0.15 else int(now * 8) % 2
            img = self.hero(frame)
            screen.blit(img, (int(self.W * 0.3 - img.get_width() / 2), int(self.floor() - img.get_height())))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score, TIME in blue at the top; at the bottom the blue bar with the weapon and its
        ammo, and P= with the lives. The second player has his score by the time and his half of the bar, in red.
        / Comme dans le jeu : TIME en bleu en haut, la barre bleue de l'arme en bas ; le second joueur a son score près
        du temps et sa moitié de barre, en rouge."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(4), S(440), S(80), now)
        self.pill(screen, S(16), S(8), S(440), S(60), 150)
        self.text(screen, "1P", S(34), S(38), 30, (90, 160, 255), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(430), S(14), "right", S(46))
        two = self.p2_in(vals)
        if two:                                                        # 2P and his score, left of the time
            self.pill(screen, W - S(636), S(8), S(320), S(60), 150)
            self.text(screen, "2P", W - S(618), S(38), 30, (255, 110, 100), key="black", valign="middle")
            if _n(vals.get("score_p2")) is not None:
                hd._score(screen, eng, "score_p2", W - S(330), S(16), "right", S(42))
        t = _n(vals.get("time"))
        if t is not None:
            self.pill(screen, W - S(300), S(8), S(280), S(60), 150)
            self.text(screen, "TIME", W - S(280), S(38), 30, (120, 190, 255), key="black", valign="middle")
            m = _n(vals.get("time_min"))                               # TIME 1:59 as in the game / comme dans le jeu
            shown = f"{int(t):02d}" if m is None else f"{int(m)}:{int(t):02d}"
            hd.put_number(screen, shown, "stencil", S(48), (160, 220, 255), W - S(44), S(38), "right", "middle")
        bar = self.imgs.get(("clbar", two))
        if bar is None:                                                # the blue bar at the bottom, its right half red
            bar = self.imgs[("clbar", two)] = pg.Surface((W, S(48)), pg.SRCALPHA)
            bar.fill((20, 40, 160, 220))
            if two:
                bar.fill((160, 30, 30, 220), (W // 2, 0, W - W // 2, S(48)))
            pg.draw.line(bar, (120, 160, 255), (0, 0), (W, 0), S(3))
        screen.blit(bar, (0, H - S(48)))
        for side, suf, weapon in (("p1", "", self.weapon), ("p2", "_p2", self.weapon2)):
            if side == "p2" and not two:
                word, colw = self.invite(vals, now)
                self.text(screen, word, W - S(40), H - S(24), 28, colw, key="black", align="right", valign="middle")
                continue
            X, near, far = self.mirror(side)
            name, col = weapon or ("NORMAL", WHITE)
            self.box(screen, X(20, 240), H - S(46), S(240), S(44), (200, 220, 255), fill=(10, 20, 80, 230), radius=4, width=2)
            self.text(screen, name, X(20, 240) + S(120), H - S(24), 30, col, key="stencil", align="center", valign="middle")
            key = {n: k for k, n, _c in CL_WEAPONS}.get(name)
            a = _n(vals.get(key + suf)) if key else None
            self.text(screen, f"{int(a):04d}" if a is not None else "----", X(300), H - S(24), 32, (255, 120, 120), key="stencil", align=near,
                      valign="middle")
            lives = _n(vals.get("lives" + suf))
            if lives is not None:
                self.label(screen, f"P={int(lives):02d}", X(70), H - S(78), 26, (255, 210, 120), align="center")


# ============================================================================ Ghost Pilots, Alpha Mission II
def radial_plane_draw(body, cowl, dark=(24, 26, 34)):
    """A stubby fighter with a big radial engine, seen from above, nose to the right: round cowl ring, straight wings
    with rounded tips, a bubble canopy. / Un chasseur trapu à gros moteur en étoile, vu du dessus, nez à droite."""
    def fn(d, W, H):
        line = dark + (255,)
        ow = max(1.0, W * 0.012)
        b, sh, lt = body + (255,), _mixc(body, (0, 0, 0), 0.25), _mixc(body, (255, 255, 255), 0.35)
        for sg in (1, -1):                                             # ailes
            def m(y):
                return 0.5 + sg * (y - 0.5)
            d.polygon([(0.62 * W, m(0.46) * H), (0.58 * W, m(0.06) * H), (0.5 * W, m(0.03) * H), (0.42 * W, m(0.08) * H), (0.4 * W, m(0.46) * H)],
                      fill=sh, outline=line)
            d.line([(0.56 * W, m(0.12) * H), (0.6 * W, m(0.42) * H)], fill=lt, width=max(1, int(H * 0.015)))
            d.polygon([(0.16 * W, m(0.47) * H), (0.12 * W, m(0.3) * H), (0.06 * W, m(0.3) * H), (0.06 * W, m(0.47) * H)], fill=sh, outline=line)
        d.polygon([(0.86 * W, 0.4 * H), (0.86 * W, 0.6 * H), (0.3 * W, 0.56 * H), (0.04 * W, 0.52 * H), (0.04 * W, 0.48 * H), (0.3 * W, 0.44 * H)],
                  fill=b, outline=line)
        d.line([(0.1 * W, 0.47 * H), (0.82 * W, 0.44 * H)], fill=lt, width=max(1, int(H * 0.015)))
        d.ellipse([0.48 * W, 0.45 * H, 0.64 * W, 0.55 * H], fill=(140, 200, 240, 255), outline=line)                    # verrière
        d.ellipse([0.82 * W, 0.37 * H, 0.94 * W, 0.63 * H], fill=cowl + (255,), outline=line, width=int(ow))          # le capot rond
        d.ellipse([0.86 * W, 0.44 * H, 0.92 * W, 0.56 * H], fill=(60, 60, 64, 255))
        d.ellipse([0.92 * W, 0.12 * H, 0.97 * W, 0.88 * H], fill=(230, 230, 236, 90))                                 # l'hélice
    return fn


def _mixc(c, k, a):
    return tuple(int(c[i] + (k[i] - c[i]) * a) for i in range(3)) + (255,)


def star_fighter_draw(body, stripe, dark=(20, 22, 34)):
    """A space fighter of our own seen from above, nose to the right: a pointed hull, swept wings with red tips, twin
    engines glowing at the back. / Un chasseur spatial à nous, vu du dessus, nez à droite."""
    def fn(d, W, H):
        line = dark + (255,)
        b, sh = body + (255,), _mixc(body, (0, 0, 0), 0.3)
        for sg in (1, -1):
            def m(y):
                return 0.5 + sg * (y - 0.5)
            d.polygon([(0.62 * W, m(0.44) * H), (0.24 * W, m(0.04) * H), (0.14 * W, m(0.06) * H), (0.3 * W, m(0.44) * H)], fill=sh, outline=line)
            d.polygon([(0.24 * W, m(0.04) * H), (0.14 * W, m(0.06) * H), (0.18 * W, m(0.14) * H), (0.27 * W, m(0.1) * H)], fill=stripe + (255,))
            d.rounded_rectangle([0.06 * W, m(0.32) * H - 0.06 * H, 0.36 * W, m(0.32) * H + 0.06 * H], radius=0.04 * H, fill=(90, 96, 110, 255),
                                outline=line)                           # les réacteurs
            d.ellipse([0.0, m(0.32) * H - 0.05 * H, 0.08 * W, m(0.32) * H + 0.05 * H], fill=(120, 200, 255, 255))
        d.polygon([(0.98 * W, 0.5 * H), (0.6 * W, 0.4 * H), (0.12 * W, 0.42 * H), (0.12 * W, 0.58 * H), (0.6 * W, 0.6 * H)], fill=b, outline=line)
        d.line([(0.2 * W, 0.5 * H), (0.9 * W, 0.5 * H)], fill=stripe + (255,), width=max(2, int(H * 0.04)))
        d.ellipse([0.56 * W, 0.44 * H, 0.74 * W, 0.56 * H], fill=(60, 140, 220, 255), outline=line)
    return fn


def saucer_draw(d, W, H):
    """An enemy saucer seen from above: a grey disc, a red dome, lights around. / Une soucoupe ennemie vue de haut."""
    d.ellipse([0, H * 0.1, W - 1, H * 0.9], fill=(130, 136, 150, 255), outline=(30, 30, 40, 255), width=max(1, int(W * 0.04)))
    d.ellipse([W * 0.3, H * 0.3, W * 0.7, H * 0.7], fill=(200, 50, 60, 255), outline=(60, 10, 20, 255))
    for k in range(8):
        a = k / 8 * math.tau
        d.ellipse([W * (0.5 + 0.38 * math.cos(a)) - W * 0.04, H * (0.5 + 0.32 * math.sin(a)) - W * 0.04,
                   W * (0.5 + 0.38 * math.cos(a)) + W * 0.04, H * (0.5 + 0.32 * math.sin(a)) + W * 0.04], fill=(255, 220, 90, 255))


class GhostPilotsScene(AeroFightersScene):
    """Ghost Pilots seen from the sky, as in the game: the brown earth and its jungle, then the deep blue sea, our
    fighter with its big radial engine, red enemy fighters and bombers, tanks on the ground. At the bottom left, as
    in the game, the planes left, B= the bombs and the stars. / Vu du ciel, comme dans le jeu."""
    THEME = "gp_world"
    SHADE = (60, 60)
    PROP = True
    ACC = {"p1": (240, 140, 40), "p2": (250, 250, 250)}
    SHOT = {"p1": (255, 220, 120), "p2": (170, 230, 255)}
    SHOT_SIZE = ((6, 50), (9, 76))
    BOMB = ((230, 60, 50), (240, 200, 80))
    ODD = "bomber"

    def plane_fn(self, side, kind):
        return radial_plane_draw((70, 110, 190) if side == "p1" else (170, 176, 190), (240, 130, 40) if side == "p1" else (60, 140, 220))

    def lane_y(self):
        return self.S(self.rng.choice(GP_LANES))

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            if kind == "bomber":
                s = self.img(("enemyimg", kind), S(150), S(176), bomber_draw)
            else:                                                      # the red enemy fighters of the game
                s = self.img(("enemyimg", "gpred"), S(96), S(90), radial_plane_draw((200, 40, 40), (240, 220, 200)), flip=True)
            if shadow:
                s = self.shadow_of(self.pg, s, 70)
            self.imgs[key] = s
        return s

    def power_max(self, vals, side):
        return 4

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1-PLAYER and the score at the top, at the bottom the planes left, B= the bombs, the stars; the
        second player has the same on the right. / Comme dans le jeu : 1-PLAYER et le score, les avions, B= et les
        étoiles en bas ; le second joueur a la même chose à droite."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        for side, suf, tag in (("p1", "", "1-PLAYER"), ("p2", "_p2", "2-PLAYER")):
            if side == "p2" and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, W - S(24), S(44), 32, col, align="right")
                continue
            if side == "p1" and not self.p1_in(vals):
                continue
            X, near, far = self.mirror(side)
            self.pill(screen, X(16, 380), S(8), S(380), S(84), 150)
            self.text(screen, tag, X(34), S(30), 26, (255, 230, 120), key="black", align=near, valign="middle")
            if _n(vals.get("score" + suf)) is not None:
                hd._score(screen, eng, "score" + suf, X(370), S(42), far, S(44))
            rows = []
            lives, bombs, stars = _n(vals.get("lives" + suf)), _n(vals.get("bombs" + suf)), _n(vals.get("stars" + suf))
            if lives is not None:
                rows.append(("plane", lives))
            if bombs is not None:
                rows.append(("B", bombs))
            if stars is not None:
                rows.append(("star", stars))
            y = H - S(40) * len(rows) - S(10)
            ox = 0 if side == "p1" else W - S(232)                     # the same block on the right, icon first as in the game
            if rows:
                self.pill(screen, ox + S(16), y - S(8), S(200), S(40) * len(rows) + S(12), 150, radius=12)
            cx = ox + S(45)
            for kind, v in rows:
                if kind == "plane":
                    icon = self.life_icon(side, vals)
                    screen.blit(icon, (ox + S(28), int(y)))
                elif kind == "B":
                    pg.draw.rect(screen, (200, 40, 40), (ox + S(30), int(y + S(4)), S(30), S(30)))
                    pg.draw.rect(screen, (255, 230, 200), (ox + S(30), int(y + S(4)), S(30), S(30)), max(1, S(2)))
                    self.text(screen, "B", cx, y + S(19), 22, WHITE, key="black", align="center", valign="middle", glow=0)
                else:
                    pts = [(cx + math.cos(-math.pi / 2 + i * math.pi / 5) * (S(17) if i % 2 == 0 else S(7)),
                            y + S(19) + math.sin(-math.pi / 2 + i * math.pi / 5) * (S(17) if i % 2 == 0 else S(7))) for i in range(10)]
                    pg.draw.polygon(screen, (255, 210, 40), pts)
                self.text(screen, f"={int(v)}", ox + S(80), y + S(19), 30, WHITE, key="black", valign="middle")
                y += S(40)


class AlphaMission2Scene(AeroFightersScene):
    """Alpha Mission II as in the game: our fighter flies over a huge fortress in deep space, saucers come, the
    turrets of the fortress blow up. The ships left at the top, G= the gold at the bottom, and the energy of the armour
    while one is worn. / Notre chasseur survole une immense forteresse dans l'espace, comme dans le jeu."""
    THEME = "am_fortress"
    SHADE = (40, 40)
    ACC = {"p1": (230, 60, 60), "p2": (60, 140, 230)}
    SHOT = {"p1": (140, 220, 255), "p2": (255, 200, 140)}
    SHOT_SIZE = ((6, 70), (9, 100))
    ODD = "heli"

    def plane_fn(self, side, kind):
        return star_fighter_draw((236, 236, 244), (220, 50, 50) if side == "p1" else (50, 120, 220))

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            s = self.img(("enemyimg", "saucer", kind == "heli"), S(110 if kind == "heli" else 84), S(96 if kind == "heli" else 74), saucer_draw)
            if shadow:
                s = self.shadow_of(self.pg, s, 60)
            self.imgs[key] = s
        return s

    def lane_y(self):
        return self.S(self.rng.uniform(150, 330))

    def power_max(self, vals, side):
        return 4

    def power_pop(self, x, y, lit, total, size=40):
        """The value that goes up here is the energy of an armour put on. / Ici c'est l'énergie d'une armure enfilée."""
        self.popup(tr("ARMURE !", "ARMOR!"), x, y, (120, 220, 255), size)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the ships left =02 and the score at the top, G= the gold at the bottom, written 02= and
        0001=G on player 2's side; the energy of the armour next to the gold while one is worn.
        / Comme dans le jeu : les vaisseaux =02 et le score en haut, G= l'or en bas, écrits 02= et 0001=G du côté du
        joueur 2 ; l'énergie de l'armure à côté de l'or tant qu'il en porte une."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        for side, suf in (("p1", ""), ("p2", "_p2")):
            if side == "p2" and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, W - S(24), S(40), 30, col, align="right")
                continue
            if side == "p1" and not self.p1_in(vals):
                continue
            X, near, far = self.mirror(side)
            self.pill(screen, X(16, 460), S(8), S(460), S(64), 150)
            icon = self.life_icon(side, vals)
            screen.blit(icon, (X(30, 40), S(20)))
            lives = _n(vals.get("lives" + suf))
            if lives is not None:
                self.text(screen, f"={int(lives):02d}" if side == "p1" else f"{int(lives):02d}=", X(80), S(40), 30, WHITE, key="black",
                          align=near, valign="middle")
            if _n(vals.get("score" + suf)) is not None:
                hd._score(screen, eng, "score" + suf, X(450), S(16), far, S(46))
            g = _n(vals.get("gold" + suf))
            y = H - S(64)
            if g is not None:
                self.pill(screen, X(16, 270), y, S(270), S(54), 150)
                pg.draw.rect(screen, (40, 80, 200), (X(30, 36), H - S(56), S(36), S(38)), border_radius=S(4))
                self.text(screen, "G", X(30, 36) + S(18), H - S(37), 26, (255, 230, 80), key="black", align="center", valign="middle", glow=0)
                self.text(screen, f"={int(g):04d}" if side == "p1" else f"{int(g):04d}=", X(80), H - S(37), 32, WHITE, key="black",
                          align=near, valign="middle")
            pw = _n(vals.get("power" + suf))
            if pw:                                                     # an armour is worn: its energy, 24 when put on
                x0 = 300 if g is not None else 16                      # / une armure est portée : son énergie
                self.pill(screen, X(x0, 330), y, S(330), S(54), 150)
                self.text(screen, tr("ARMURE", "ARMOR"), X(x0 + 20), H - S(37), 24, CREAM, key="black", align=near, valign="middle", glow=0)
                self.bar(screen, X(x0 + 150, 160), H - S(46), S(160), S(18), pw / 24, (120, 220, 255) if pw > 6 else RED)


# ============================================================================ Viewpoint
VP_BOMBS = {1: ("PLASMA", (90, 160, 255)), 2: ("FIRE", (255, 90, 60)), 3: ("HOMING", (90, 230, 120))}


def hover_draw(d, W, H):
    """Our little hover-ship seen at an angle, nose to the right: a white hull, red fins, a blue glass bubble, its
    engine glowing at the back. / Notre petit vaisseau vu de biais, nez à droite."""
    dark = (24, 26, 40, 255)
    ow = max(1.0, W * 0.02)
    d.polygon([(0.2 * W, 0.2 * H), (0.42 * W, 0.0), (0.5 * W, 0.0), (0.4 * W, 0.34 * H)], fill=(220, 50, 50, 255), outline=dark)
    d.polygon([(0.06 * W, 0.5 * H), (0.5 * W, 0.24 * H), (0.98 * W, 0.5 * H), (0.62 * W, 0.86 * H), (0.12 * W, 0.78 * H)], fill=(236, 236, 244, 255),
              outline=dark)
    d.polygon([(0.06 * W, 0.5 * H), (0.62 * W, 0.62 * H), (0.98 * W, 0.5 * H), (0.62 * W, 0.86 * H), (0.12 * W, 0.78 * H)], fill=(170, 176, 196, 255),
              outline=dark)
    d.polygon([(0.24 * W, 0.7 * H), (0.36 * W, 1.0 * H), (0.46 * W, 0.98 * H), (0.42 * W, 0.74 * H)], fill=(200, 40, 40, 255), outline=dark)
    d.ellipse([0.46 * W, 0.3 * H, 0.72 * W, 0.6 * H], fill=(60, 120, 230, 255), outline=dark, width=int(ow))
    d.ellipse([0.52 * W, 0.34 * H, 0.6 * W, 0.42 * H], fill=(200, 230, 255, 255))
    d.ellipse([0.0, 0.5 * H, 0.12 * W, 0.7 * H], fill=(120, 220, 255, 255))


def crawler_draw(d, W, H):
    """An enemy crawler of the floor: a purple and cream shell on claws, a green eye. / Un rampant ennemi."""
    dark = (30, 20, 40, 255)
    for k in range(3):                                                 # pattes
        x = W * (0.25 + 0.25 * k)
        d.line([(x, H * 0.6), (x - W * 0.1, H * 0.95)], fill=(90, 160, 90, 255), width=max(2, int(W * 0.04)))
    d.ellipse([W * 0.04, H * 0.2, W * 0.96, H * 0.8], fill=(220, 200, 150, 255), outline=dark, width=max(1, int(W * 0.03)))
    d.chord([W * 0.04, H * 0.2, W * 0.96, H * 0.8], 180, 360, fill=(140, 90, 190, 255))
    for k in range(3):
        d.line([(W * (0.3 + 0.2 * k), H * 0.22), (W * (0.3 + 0.2 * k), H * 0.5)], fill=(100, 60, 150, 255), width=max(2, int(W * 0.04)))
    d.ellipse([W * 0.06, H * 0.38, W * 0.24, H * 0.6], fill=(80, 230, 120, 255), outline=dark)


def ring_mine_draw(d, W, H):
    """A floating ring mine, red and white, seen at an angle. / Une mine en anneau, rouge et blanche, vue de biais."""
    d.ellipse([0, H * 0.2, W - 1, H * 0.8], fill=(220, 60, 60, 255), outline=(60, 10, 10, 255), width=max(1, int(W * 0.05)))
    d.ellipse([W * 0.25, H * 0.35, W * 0.75, H * 0.65], fill=(30, 20, 30, 255), outline=(240, 240, 240, 255), width=max(1, int(W * 0.05)))
    d.ellipse([W * 0.4, H * 0.42, W * 0.6, H * 0.58], fill=(255, 220, 220, 255))


class ViewpointScene(BlazingStarScene):
    """Viewpoint as in the game: the floor of slate tiles seen at an angle slides by, our hover-ship flies over it with
    its shadow, crawlers and ring mines come, the bomb read in the game (plasma, fire, homing) sweeps the screen. 1UP,
    the score and the three bomb lights at the bottom, as in the game. / Le sol de dalles vu de biais, comme dans le jeu."""
    THEME = "vp_floor"
    SHADE = (40, 90)
    ZONE = (140, 330)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.bombs = 0                                    # (tests)
        self.bpop = -99.0

    def ship_surf(self, side):
        S = self.S
        return self.img(("vpship", side), S(120), S(84), hover_draw)

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.0

    def update(self, vals, now):
        super().update(vals, now)
        for e in self.enemies:
            if "kind" not in e:
                e["kind"] = "mine" if self.rng.random() < 0.35 else "crawler"
        ch = self.changed(vals, "bomb_type")
        if ch and ch[0] and not ch[1] and self.ships["p1"]["in"]:     # the bomb carried is spent / la bombe portée part
            self.bomb(vals, now, int(ch[0]))
        elif ch and ch[1]:
            name, col = VP_BOMBS.get(int(ch[1]), ("BOMB", GOLD))
            x, y = self.pos("p1", now)
            self.popup(name, x, max(self.S(170), y - self.S(70)), col, 36)

    def bomb(self, vals, now, kind):
        """The bomb of the game sweeps the screen in its colour. / La bombe balaie l'écran dans sa couleur."""
        S, fx = self.S, self.fx
        self.bombs += 1
        self.bpop = now
        name, col = VP_BOMBS.get(kind, VP_BOMBS[1])
        x, y = self.pos("p1", now)
        for i in range(8):
            fx.later(i * 0.05, fx.glow, x + S(120) + i * S(160), y + math.sin(i) * S(40), 30, 160, col, 0.5, "front", 1.0, 0.0)
        fx.flash(col, 0.25, 0.3)
        for e in self.enemies:
            if not e.get("dead"):
                fx.later(0.3 + self.rng.uniform(0, 0.3), self._boom, e)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg, dt = self.S, self.pg, self.dt
        keep = []
        for e in self.enemies:
            if e.get("dead"):
                continue
            e["x"] -= e["v"] * dt
            if e["x"] < -S(100):
                continue
            e["yy"] = e["y"] + math.sin(now * 2.0 + e["ph"]) * S(12)
            keep.append(e)
            kind = e.get("kind", "crawler")
            img = self.img(("vpfoe", kind), S(110) if kind == "crawler" else S(80), S(70) if kind == "crawler" else S(46),
                           crawler_draw if kind == "crawler" else ring_mine_draw)
            sh = self.imgs.get(("vpsh", kind))
            if sh is None:
                sh = self.imgs[("vpsh", kind)] = pg.Surface((img.get_width(), img.get_height() // 2), pg.SRCALPHA)
                pg.draw.ellipse(sh, (0, 0, 0, 90), sh.get_rect())
            if kind == "mine":
                screen.blit(sh, (int(e["x"] - sh.get_width() / 2 + S(30)), int(e["yy"] + S(40))))
            screen.blit(img, (int(e["x"] - img.get_width() / 2), int(e["yy"] - img.get_height() / 2)))
            if now - e["hit"] < 0.06:
                h = self.fx.sp.glow(S(40), (255, 255, 255), 8, hot=0.6)
                screen.blit(h, (int(e["x"] - h.get_width() / 2), int(e["yy"] - h.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        self.enemies = keep
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"] or now - P["t_dead"] < 1.2 or now < P["t_spawn"]:
                continue
            if now - P["t_spawn"] < 1.6 and int(now * 14) % 2 == 0:
                continue
            x, y = self.pos(side, now)
            sh = self.imgs.get("vpshadow")
            if sh is None:
                sh = self.imgs["vpshadow"] = pg.Surface((S(100), S(30)), pg.SRCALPHA)
                pg.draw.ellipse(sh, (0, 0, 0, 100), sh.get_rect())
            screen.blit(sh, (int(x - S(30)), int(y + S(60))))                # its shadow on the floor, below and behind
            ship = self.rotated(("vps", side), self.ship_surf(side), _clamp(-P["vy"] * 6, -10, 10))
            screen.blit(ship, (int(x - ship.get_width() / 2), int(y - ship.get_height() / 2)))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: at the bottom 1UP in yellow, the score, the three bomb lights; 2UP the same on the right.
        / Comme dans le jeu : en bas 1UP en jaune, le score, les trois voyants de bombe ; 2UP pareil à droite."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        for side, suf, tag in (("p1", "", "1UP"), ("p2", "_p2", "2UP")):
            if side == "p2" and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.text(screen, word, W - S(40), H - S(40), 30, col, key="black", align="right", valign="middle")
                continue
            if side == "p1" and not self.p1_in(vals):
                continue
            X, near, far = self.mirror(side)
            self.pill(screen, X(16, 560), H - S(70), S(560), S(60), 160)
            self.text(screen, tag, X(34), H - S(40), 32, (255, 230, 60), key="black", align=near, valign="middle")
            if _n(vals.get("score" + suf)) is not None:
                hd._score(screen, eng, "score" + suf, X(330), H - S(64), far, S(46))
            cur = int(_n(vals.get("bomb_type" + suf)) or 0)
            n = _n(vals.get("bombs" + suf))
            for i, k in enumerate((2, 3, 1)):                          # red, green, blue as in the game
                col = VP_BOMBS[k][1]
                on = k == cur
                pg.draw.circle(screen, col if on else _mixc(col, (0, 0, 0), 0.6)[:3], (X(370 + i * 44), H - S(40)), S(14 if on else 11))
            if n is not None:
                self.text(screen, f"x{int(n)}", X(510), H - S(40), 28, WHITE, key="black", align=near, valign="middle")
            lives = _n(vals.get("lives" + suf))
            if lives is not None:
                self.label(screen, f"{int(lives)}", X(60), H - S(100), 26, (255, 230, 60), align="center")


# ============================================================================ Zed Blade, Prehistoric Isle 2
def side_heli_draw(body, accent, dark=(24, 26, 30)):
    """A helicopter seen from the side, nose to the right: a slim fuselage, the glass canopy, the tail boom and its
    rotor, skids, the blur of the main rotor. / Un hélicoptère de profil, nez à droite."""
    def fn(d, W, H):
        line = dark + (255,)
        b = body + (255,)
        sh = _mixc(body, (0, 0, 0), 0.3)
        d.ellipse([0.02 * W, 0.06 * H, 0.98 * W, 0.2 * H], fill=(220, 220, 230, 70))                     # rotor principal
        d.rectangle([0.46 * W, 0.12 * H, 0.52 * W, 0.3 * H], fill=(60, 60, 66, 255))
        d.polygon([(0.04 * W, 0.42 * H), (0.36 * W, 0.4 * H), (0.36 * W, 0.52 * H), (0.04 * W, 0.5 * H)], fill=sh, outline=line)      # poutre
        d.polygon([(0.02 * W, 0.24 * H), (0.1 * W, 0.24 * H), (0.12 * W, 0.46 * H), (0.04 * W, 0.46 * H)], fill=b, outline=line)      # dérive
        d.ellipse([0.0, 0.22 * H, 0.08 * W, 0.52 * H], fill=(220, 220, 230, 90))
        d.polygon([(0.3 * W, 0.34 * H), (0.62 * W, 0.28 * H), (0.88 * W, 0.4 * H), (0.96 * W, 0.56 * H), (0.84 * W, 0.7 * H), (0.36 * W, 0.68 * H)],
                  fill=b, outline=line)
        d.polygon([(0.66 * W, 0.32 * H), (0.86 * W, 0.42 * H), (0.92 * W, 0.56 * H), (0.7 * W, 0.52 * H)], fill=(120, 200, 240, 255), outline=line)
        d.line([(0.36 * W, 0.56 * H), (0.84 * W, 0.56 * H)], fill=accent + (255,), width=max(2, int(H * 0.05)))
        d.rectangle([0.44 * W, 0.64 * H, 0.64 * W, 0.72 * H], fill=(60, 64, 70, 255), outline=line)          # nacelle d'armes
        for x in (0.4, 0.74):
            d.line([(x * W, 0.7 * H), (x * W, 0.86 * H)], fill=line, width=max(1, int(W * 0.012)))
        d.line([(0.3 * W, 0.86 * H), (0.86 * W, 0.86 * H)], fill=line, width=max(2, int(W * 0.016)))
    return fn


def ptero_draw(frame):
    """A flying reptile of the island, facing left: a long beak, a crest, leathery wings up or down.
    / Un reptile volant de l'île, face à gauche."""
    def fn(d, W, H):
        dark = (40, 20, 30, 255)
        skin, wing = (200, 70, 90, 255), (150, 50, 110, 255)
        up = frame == 0
        d.polygon([(0.5 * W, 0.5 * H), (0.7 * W, 0.0 if up else 0.92 * H), (0.98 * W, 0.08 * H if up else 0.98 * H), (0.62 * W, 0.56 * H)],
                  fill=wing, outline=dark)
        d.polygon([(0.38 * W, 0.5 * H), (0.48 * W, 0.04 * H if up else 0.96 * H), (0.62 * W, 0.12 * H if up else 0.9 * H), (0.56 * W, 0.56 * H)],
                  fill=_mixc((150, 50, 110), (0, 0, 0), 0.25), outline=dark)
        d.ellipse([0.3 * W, 0.42 * H, 0.74 * W, 0.62 * H], fill=skin, outline=dark)
        d.polygon([(0.74 * W, 0.5 * H), (0.98 * W, 0.46 * H), (0.98 * W, 0.54 * H)], fill=skin, outline=dark)                    # la queue
        d.ellipse([0.18 * W, 0.36 * H, 0.36 * W, 0.54 * H], fill=skin, outline=dark)                                                # la tête
        d.polygon([(0.2 * W, 0.44 * H), (0.0, 0.5 * H), (0.2 * W, 0.5 * H)], fill=(230, 200, 120, 255), outline=dark)               # le bec
        d.polygon([(0.3 * W, 0.4 * H), (0.42 * W, 0.26 * H), (0.36 * W, 0.42 * H)], fill=(250, 200, 60, 255))                       # la crête
        d.ellipse([0.23 * W, 0.41 * H, 0.27 * W, 0.45 * H], fill=(255, 240, 60, 255))
    return fn


class SideShooterScene(BlazingStarScene):
    """A shoot'em up seen from the side with a ship and enemies of its own (Zed Blade, Prehistoric Isle 2).
    / Un shoot'em up de profil avec son vaisseau et ses ennemis à lui."""
    SHADE = (70, 70)
    ZONE = (150, 340)
    SHIP = (190, 100)
    FOE = (130, 90)
    FLIP_FOE = False                                  # the enemy drawing faces right: turn it / le dessin regarde à droite

    def ship_fn(self, side):
        return lr_ship_draw(self.ACC[side])

    def foe_fn(self, frame):
        return lambda d, W, H: None

    def ship_surf(self, side):
        S = self.S
        return self.img(("sship", side), S(self.SHIP[0]), S(self.SHIP[1]), self.ship_fn(side))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg, dt = self.S, self.pg, self.dt
        keep = []
        for e in self.enemies:
            if e.get("dead"):
                continue
            e["x"] -= e["v"] * dt
            if e["x"] < -S(120):
                continue
            e["yy"] = e["y"] + math.sin(now * 2.2 + e["ph"]) * S(18)
            keep.append(e)
            fr = int(now * 6 + e["ph"]) % 2
            img = self.img(("sfoe", fr), S(self.FOE[0]), S(self.FOE[1]), self.foe_fn(fr), flip=self.FLIP_FOE)
            screen.blit(img, (int(e["x"] - img.get_width() / 2), int(e["yy"] - img.get_height() / 2)))
            if now - e["hit"] < 0.06:
                h = self.fx.sp.glow(S(44), (255, 255, 255), 8, hot=0.6)
                screen.blit(h, (int(e["x"] - h.get_width() / 2), int(e["yy"] - h.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        self.enemies = keep
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"] or now - P["t_dead"] < 1.2 or now < P["t_spawn"]:
                continue
            if now - P["t_spawn"] < 1.6 and int(now * 14) % 2 == 0:
                continue
            x, y = self.pos(side, now)
            ship = self.rotated(("ss", side), self.ship_surf(side), _clamp(-P["vy"] * 5, -8, 8))
            screen.blit(ship, (int(x - ship.get_width() / 2), int(y - ship.get_height() / 2)))
        self.status(screen, eng, vals, logo, now)


class ZedBladeScene(SideShooterScene):
    """Zed Blade as in the game: our fighter flies over a valley at dawn, mountains, forest, stone pillars, the enemy
    helicopters come in packs. 1P- and the score in red, 2P- in blue at the top, the bombs at the bottom left.
    / Notre chasseur survole une vallée à l'aube, les hélicoptères ennemis arrivent par groupes."""
    THEME = "zb_valley"
    ACC = {"p1": (220, 50, 60), "p2": (60, 120, 230)}
    FOE = (150, 90)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.bombs = 0                                    # (tests)

    FLIP_FOE = True

    def foe_fn(self, frame):
        return side_heli_draw((60, 90, 60), (200, 200, 60))

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.2

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "bombs")
        if ch and ch[1] < ch[0] and self.ships["p1"]["in"]:
            S, fx = self.S, self.fx
            self.bombs += 1
            self.weapon_window(now)
            x, y = self.pos("p1", now)
            for i in range(6):
                fx.later(i * 0.08, fx.explosion, x + S(200) + i * S(220), y + self.rng.uniform(-S(80), S(80)), 0.7, False)
            for e in self.enemies:
                if not e.get("dead"):
                    fx.later(0.4, self._boom, e)
        ch = self.changed(vals, "shot_level")
        if ch and ch[1] > ch[0] and self.ships["p1"]["in"]:                    # the shot goes up a level / le tir monte d'un niveau
            x, y = self.pos("p1", now)
            top = _n(self.tops.get("shot_level"))
            self.power_pop(x, y - self.S(64), int(ch[1]) + 1, int(top) + 1 if top is not None else 4)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P- in red and the score, 2P- in blue, the ships left under each score, the bombs at the bottom,
        player 2's on the right. / Comme dans le jeu : 1P- en rouge et le score, 2P- en bleu, les vaisseaux qui restent
        sous chaque score, les bombes en bas, celles du joueur 2 à droite."""
        S, W, H, pg, hd = self.S, self.W, self.H, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(440), S(84), now)
        self.pill(screen, S(16), S(8), S(440), S(60), 150)
        self.text(screen, "1P-", S(34), S(38), 32, (255, 60, 60), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(430), S(14), "right", S(46))
        two = self.p2_in(vals)
        if two:
            self.pill(screen, W - S(456), S(8), S(440), S(60), 150)
            self.text(screen, "2P-", W - S(436), S(38), 32, (80, 140, 255), key="black", valign="middle")
            if _n(vals.get("score_p2")) is not None:
                hd._score(screen, eng, "score_p2", W - S(40), S(14), "right", S(46))
        else:
            word, col = self.invite(vals, now)
            self.text(screen, "2P-", W - S(436), S(38), 32, (80, 140, 255), key="black", valign="middle")
            self.label(screen, word, W - S(200), S(38), 30, col, align="center")
        for side, suf in (("p1", ""), ("p2", "_p2")):
            if side == "p2" and not two or side == "p1" and not self.p1_in(vals):
                continue
            X = self.mirror(side)[0]
            n = _n(vals.get("lives" + suf))
            if n:                                                      # the ships left under the score, as in the game
                icon = self.img(("zblife", side), S(56), S(30), self.ship_fn(side))
                for i in range(min(5, int(n))):
                    screen.blit(icon, (X(26 + i * 62, 56), S(76)))
            b = _n(vals.get("bombs" + suf))
            for i in range(min(6, int(b or 0))):                       # blue capsules at the bottom, as in the game
                x = X(30 + i * 44, 36)
                pg.draw.ellipse(screen, (40, 80, 220), (x, H - S(52), S(36), S(42)))
                pg.draw.ellipse(screen, (180, 210, 255), (x + S(8), H - S(46), S(12), S(16)))
                pg.draw.ellipse(screen, (250, 200, 60), (x + S(10), H - S(26), S(16), S(10)))
        lv = _n(vals.get("shot_level"))
        if lv is not None:                                             # the shot's level (LEVEL-4 on the game's screen is its difficulty)
            self.label(screen, tr("TIR", "SHOT") + f" {int(lv) + 1}", S(30), H - S(96), 26, WHITE, align="left")


class PrehistoricIsle2Scene(SideShooterScene):
    """Prehistoric Isle 2 as in the game: our helicopter flies over the sea by the island, stone pillars rise from the
    waves, the flying reptiles come. PLAYER 1 and the score at the top, the helicopters left, the weapon level, the
    bombs at the bottom left. / Notre hélicoptère survole la mer au bord de l'île, les reptiles volants arrivent."""
    THEME = "pi_sea"
    ACC = {"p1": (230, 200, 60), "p2": (230, 80, 60)}
    SHIP = (200, 110)
    FOE = (150, 100)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.bombs = 0                                    # (tests)

    def ship_fn(self, side):
        return side_heli_draw((50, 110, 190) if side == "p1" else (200, 70, 50), self.ACC[side])

    def foe_fn(self, frame):
        return ptero_draw(frame)

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.0

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "bombs")
        if ch and ch[1] < ch[0] and self.ships["p1"]["in"]:
            S, fx = self.S, self.fx
            self.bombs += 1
            self.weapon_window(now)
            x, y = self.pos("p1", now)
            fx.flash((255, 240, 200), 0.3, 0.3)
            fx.explosion(x + S(500), y, 1.4, False)
            for e in self.enemies:
                if not e.get("dead"):
                    fx.later(0.3, self._boom, e)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: PLAYER 1 and the score at the top, the helicopters left; at the bottom the weapon level, the
        bombs and the stars. The second player has the same on the right. / Comme dans le jeu : PLAYER 1 et le score en
        haut, le niveau de l'arme, les bombes et les étoiles en bas ; le second joueur a la même chose à droite."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(440), S(84), now)
        for side, suf, tag, col in (("p1", "", "PLAYER 1", (120, 220, 240)), ("p2", "_p2", "PLAYER 2", (255, 170, 120))):
            if side == "p2" and not self.p2_in(vals):
                word, colw = self.invite(vals, now)
                self.label(screen, word, W - S(24), S(44), 32, colw, align="right")
                continue
            if side == "p1" and not self.p1_in(vals):
                continue
            X, near, far = self.mirror(side)
            self.pill(screen, X(16, 480), S(8), S(480), S(104), 150, radius=14)
            self.text(screen, tag, X(34), S(30), 26, col, key="black", align=near, valign="middle")
            sc = _n(vals.get("score" + suf))
            if sc is not None:
                hd.put_number(screen, f"{int(sc):010d}", "black", S(40), col, X(34), S(70), near, "middle")
            lives = _n(vals.get("lives" + suf))
            if lives is not None:
                icon = self.img(("pilife", side), S(60), S(34), self.ship_fn(side))
                screen.blit(icon, (X(330, 60), S(54)))
                self.text(screen, f"={int(lives)}", X(400), S(72), 30, (255, 230, 120), key="black", align=near, valign="middle")
            lv, b, st = _n(vals.get("power" + suf)), _n(vals.get("bombs" + suf)), _n(vals.get("stars" + suf))
            if lv is not None or b is not None:
                self.pill(screen, X(16, 300), H - S(100), S(300), S(90), 150, radius=14)
            if lv is not None:
                self.text(screen, f"Lv{int(lv)}", X(36), H - S(76), 30, col, key="black", align=near, valign="middle")
            if b is not None:
                self.text(screen, f"B x{int(b)}", X(36), H - S(34), 30, (255, 230, 120), key="black", align=near, valign="middle")
            if st is not None:                                         # the stars, as by the star of the game
                self.text(screen, f"★ x{int(st)}", X(170), H - S(34), 30, (255, 210, 60), key="black", align=near, valign="middle")


# ============================================================================ Shock Troopers 2nd Squad
ST2_WEAPONS = {0: ("NORMAL", (255, 240, 170)), 4: ("FIRE", (255, 140, 60)), 8: ("ROUND", (120, 220, 255)), 12: ("MISSILE", (255, 200, 140)),
               16: ("BOOMERANG", (170, 255, 140))}


def soldier_draw(vest, pants, hair, band, frame, helmet=False, skin=(226, 176, 136)):
    """A soldier seen from above at three quarters, facing right, a rifle in his hands: our commando (a bandana) or an
    enemy (a helmet). Frames 0 and 1 run, 2 fire, 3 down. / Un soldat vu de trois quarts, face à droite, fusil en main."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, W * 0.022)
        sk = skin + (255,)
        vs, vs_d = vest + (255,), _mixc(vest, (0, 0, 0), 0.28)
        pt, pt_d = pants + (255,), _mixc(pants, (0, 0, 0), 0.28)
        u = H
        if frame == 3:                                                 # down, on his back
            y = H * 0.9
            _capsule(d, (W * 0.3, y - 0.06 * u), (W * 0.66, y - 0.06 * u), 0.09 * u, 0.09 * u, vs, dark, ow)
            _capsule(d, (W * 0.66, y - 0.05 * u), (W * 0.95, y - 0.02 * u), 0.06 * u, 0.055 * u, pt, dark, ow)
            d.ellipse([W * 0.08, y - 0.17 * u, W * 0.3, y + 0.03 * u], fill=sk if not helmet else hair + (255,), outline=dark, width=int(ow))
            return
        cx = W * 0.4
        step = (0.12, -0.1) if frame == 0 else ((-0.1, 0.12) if frame == 1 else (0.07, -0.07))
        for i, dx in enumerate(step):                                  # les jambes, raccourcies par la vue d'en haut
            k = (cx + dx * 0.5 * u, H * 0.8)
            f = (cx + dx * u, H * 0.96)
            _capsule(d, (cx, H * 0.62), k, 0.065 * u, 0.06 * u, pt_d if i == 0 else pt, dark, ow)
            _capsule(d, k, f, 0.055 * u, 0.05 * u, pt_d if i == 0 else pt, dark, ow)
            d.rounded_rectangle([f[0] - 0.05 * u, f[1] - 0.04 * u, f[0] + 0.07 * u, f[1] + 0.02 * u], radius=0.02 * u, fill=(36, 30, 26, 255),
                                outline=dark)
        d.rounded_rectangle([cx - 0.13 * u, H * 0.3, cx + 0.13 * u, H * 0.64], radius=0.06 * u, fill=vs, outline=dark, width=int(ow))
        d.rectangle([cx - 0.12 * u, H * 0.5, cx + 0.12 * u, H * 0.55], fill=vs_d)                                  # la ceinture
        for k in range(3):                                             # les poches du gilet
            d.rectangle([cx - 0.1 * u + k * 0.07 * u, H * 0.4, cx - 0.05 * u + k * 0.07 * u, H * 0.47], fill=vs_d)
        gy = H * (0.47 if frame != 2 else 0.45)
        d.rounded_rectangle([cx - 0.04 * u, gy - 0.035 * u, cx + 0.42 * u, gy + 0.035 * u], radius=0.015 * u, fill=(56, 58, 66, 255),
                            outline=dark, width=int(ow))                # le fusil
        d.rectangle([cx + 0.4 * u, gy - 0.018 * u, cx + 0.5 * u, gy + 0.018 * u], fill=(36, 36, 40, 255))
        d.rectangle([cx + 0.1 * u, gy + 0.03 * u, cx + 0.15 * u, gy + 0.1 * u], fill=(56, 58, 66, 255), outline=dark)
        _capsule(d, (cx + 0.02 * u, H * 0.35), (cx + 0.2 * u, gy), 0.05 * u, 0.045 * u, sk, dark, ow)
        _capsule(d, (cx - 0.08 * u, H * 0.36), (cx + 0.06 * u, gy + 0.01 * u), 0.05 * u, 0.045 * u, _mixc(skin, (0, 0, 0), 0.2), dark, ow)
        hx, hy = cx + 0.02 * u, H * 0.17                               # la tête, grande vue d'en haut
        r = 0.11 * u
        d.ellipse([hx - r, hy - r, hx + r, hy + r * 1.05], fill=sk, outline=dark, width=int(ow))
        d.ellipse([hx + r * 0.38, hy - r * 0.05, hx + r * 0.62, hy + r * 0.2], fill=dark)
        if helmet:                                                     # le casque de l'ennemi
            d.chord([hx - r * 1.12, hy - r * 1.2, hx + r * 1.1, hy + r * 0.5], 180, 360, fill=hair + (255,), outline=dark)
            d.rectangle([hx - r * 1.1, hy - r * 0.4, hx + r * 1.12, hy - r * 0.28], fill=_mixc(hair, (0, 0, 0), 0.3))
        else:                                                          # cheveux et bandeau de notre commando
            d.chord([hx - r * 1.04, hy - r * 1.14, hx + r * 0.98, hy + r * 0.3], 180, 360, fill=hair + (255,))
            d.polygon([(hx - r * 0.9, hy - r * 0.6), (hx - r * 1.5, hy - r * 0.2), (hx - r * 0.9, hy - r * 0.1)], fill=hair + (255,))
            d.rectangle([hx - r, hy - r * 0.46, hx + r * 0.96, hy - r * 0.26], fill=band + (255,))
            d.polygon([(hx - r, hy - r * 0.44), (hx - r * 1.7, hy - r * 0.1), (hx - r * 1.6, hy + r * 0.2), (hx - r * 0.95, hy - r * 0.26)],
                      fill=band + (255,))
    return fn


def jeep_draw(d, W, H):
    """An enemy jeep seen from above at three quarters, facing left, a gun on its back. / Une jeep ennemie vue de trois quarts."""
    dark = (24, 24, 20, 255)
    ow = max(1, int(H * 0.025))
    for x in (0.2, 0.74):                                              # les roues
        d.rounded_rectangle([W * (x - 0.08), H * 0.66, W * (x + 0.08), H * 0.98], radius=H * 0.05, fill=(30, 30, 30, 255))
        d.rounded_rectangle([W * (x - 0.08), H * 0.08, W * (x + 0.08), H * 0.3], radius=H * 0.05, fill=(30, 30, 30, 255))
    d.rounded_rectangle([W * 0.04, H * 0.2, W * 0.96, H * 0.86], radius=H * 0.1, fill=(150, 140, 96, 255), outline=dark, width=ow)
    d.rounded_rectangle([W * 0.04, H * 0.66, W * 0.96, H * 0.86], radius=H * 0.06, fill=(116, 108, 72, 255), outline=dark, width=ow)
    d.polygon([(W * 0.24, H * 0.24), (W * 0.34, H * 0.24), (W * 0.3, H * 0.66), (W * 0.2, H * 0.66)], fill=(60, 80, 100, 255), outline=dark)
    d.rectangle([W * 0.06, H * 0.3, W * 0.2, H * 0.6], fill=(170, 160, 110, 255), outline=dark)                       # le capot
    d.rounded_rectangle([W * 0.6, H * 0.3, W * 0.78, H * 0.5], radius=H * 0.04, fill=(70, 70, 66, 255), outline=dark)  # la mitrailleuse
    d.line([(W * 0.6, H * 0.4), (W * 0.42, H * 0.38)], fill=dark, width=max(2, int(H * 0.06)))
    d.ellipse([W * 0.84, H * 0.3, W * 0.98, H * 0.58], fill=(40, 40, 40, 255), outline=dark)                          # la roue de secours


def tank34_draw(d, W, H):
    """An enemy tank seen from above at three quarters, facing left. / Un char ennemi vu de trois quarts, face à gauche."""
    dark = (22, 24, 18, 255)
    ow = max(1, int(H * 0.025))
    d.rounded_rectangle([W * 0.02, H * 0.62, W * 0.98, H * 0.98], radius=H * 0.12, fill=(56, 56, 48, 255), outline=dark, width=ow)
    for k in range(9):
        x = W * (0.07 + k * 0.107)
        d.ellipse([x - H * 0.07, H * 0.7, x + H * 0.07, H * 0.9], fill=(96, 96, 84, 255), outline=dark)
    d.rounded_rectangle([W * 0.04, H * 0.2, W * 0.96, H * 0.72], radius=H * 0.08, fill=(176, 150, 70, 255), outline=dark, width=ow)
    d.rectangle([W * 0.04, H * 0.2, W * 0.96, H * 0.3], fill=(196, 172, 90, 255), outline=dark)
    d.rounded_rectangle([W * 0.34, H * 0.04, W * 0.76, H * 0.5], radius=H * 0.1, fill=(160, 136, 60, 255), outline=dark, width=ow)
    d.rectangle([W * 0.0, H * 0.2, W * 0.36, H * 0.3], fill=(110, 96, 50, 255), outline=dark)                          # le canon
    d.ellipse([W * 0.5, H * 0.1, W * 0.62, H * 0.24], fill=(90, 80, 40, 255), outline=dark)


# the four soldiers of the 2nd Squad in the order of the game's SOLDIER SELECT screen, and our commando in the colours
# of each: (vest, trousers, hair, bandana) / les quatre soldats dans l'ordre de l'écran SOLDIER SELECT, et notre
# commando aux couleurs de chacun
ST2_SOLDIERS = ("LEON", "ANGEL", "LULU", "TOY")
ST2_LOOKS = (((44, 52, 96), (70, 64, 56), (62, 44, 34), (150, 150, 160)),
             ((232, 234, 240), (60, 104, 170), (240, 208, 104), (60, 104, 170)),
             ((204, 44, 44), (226, 226, 230), (124, 66, 38), (204, 44, 44)),
             ((56, 132, 72), (70, 64, 56), (234, 120, 40), (56, 132, 72)))
ST2_SHOT = {1: "FRONT", 2: "WIDE"}     # the normal gun as the game names it, for the two soldiers seen with theirs


def face_icon_draw(d, W, H, hair=(110, 60, 30), band=(210, 40, 40)):
    """Our commando's face for the corner of the screen: brown hair, a red bandana. / Le visage de notre commando."""
    dark = (24, 20, 20, 255)
    d.rectangle([0, 0, W - 1, H - 1], fill=(60, 90, 160, 255))
    d.ellipse([W * 0.18, H * 0.16, W * 0.82, H * 0.96], fill=(232, 184, 144, 255), outline=dark, width=max(1, int(W * 0.03)))
    d.chord([W * 0.14, H * 0.04, W * 0.86, H * 0.66], 180, 360, fill=hair + (255,))
    d.rectangle([W * 0.16, H * 0.3, W * 0.84, H * 0.38], fill=band + (255,))
    for ex in (0.36, 0.64):
        d.ellipse([W * (ex - 0.06), H * 0.48, W * (ex + 0.06), H * 0.58], fill=dark)
    d.line([(W * 0.42, H * 0.78), (W * 0.58, H * 0.78)], fill=dark, width=max(1, int(W * 0.03)))
    d.rectangle([0, 0, W - 1, H - 1], outline=(250, 250, 250, 255), width=max(2, int(W * 0.05)))


class ShockTroopers2Scene(Machines, GameScene):
    """Shock Troopers 2nd Squad as in the game: the city street seen from above, our commando goes up the road and
    shoots the soldiers, the jeeps and the tanks that come. The weapon read in the game is the one he fires (normal,
    fire, round, missile, boomerang), a grenade spent is thrown, a life lost blows up next to him. At the top the face,
    1P- and the score, the soldier's name and his energy, TIME in big yellow numbers; at the bottom the grenades, the
    weapon box and LV. The second player has his commando and his own corners; a big machine being shot at gets its
    life bar under the logo. / La rue vue du dessus : notre commando remonte la route et tire sur les soldats et les
    engins, comme dans le jeu, avec le nom du soldat, son énergie, le second joueur et la barre des gros engins."""
    THEME = "st2_street"
    SHADE = (90, 60)
    EXPLOSIONS = True
    TITLE = "Shock Troopers 2nd Squad"
    SQUAD = True                                          # the soldiers of the 2nd Squad, their energy, the machines
    TWO = True                                            # the second player has his commando / le second joueur a le sien
    BOSS_MIN = None                                       # no boss announced: the life of this game's bosses is not known
    BIG_MIN = 150                                         # a machine with that much life and hit three times: its bar
    MACHINE_HITS = 3
    MACHINE_BOX = (560, 60, 88)
    FULL = 64                                             # a soldier's full energy / l'énergie pleine d'un soldat
    HERO = ((60, 96, 170), (70, 64, 56), (110, 60, 30), (210, 40, 40))
    FOE = ((150, 130, 80), (110, 96, 60), (96, 104, 60), (0, 0, 0))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.fx.sp.register("grenade_st2", draw_img(S(22), S(26), lambda d, W, H: (
            d.ellipse([0, H * 0.2, W, H], fill=(60, 90, 50, 255), outline=(20, 20, 20, 255)),
            d.rectangle([W * 0.35, 0, W * 0.65, H * 0.3], fill=(90, 90, 90, 255)))))
        self.foes = []
        self.next_foe = 0.0
        self.next_car = 0.0
        self.fire_t = 0.0
        self.hurt = -99.0
        self.lv = None
        self.kills = 0                                    # (tests)
        self.grenades_thrown = 0
        self.specials = 0
        self.hz = 0.5
        self.look = {"p1": None, "p2": None}              # the soldier of each player / le soldat de chaque joueur
        self.hz2, self.fire_t2, self.hurt2, self.lv2 = 0.7, 0.0, -99.0, None      # the second player's commando
        self.epop = {"p1": -99.0, "p2": -99.0}            # when each energy last fell / l'énergie qui baisse
        self.machines_reset()
        self.warm = ([(self.hero, (f,)) for f in range(3)] + [(self.foe, (f,)) for f in range(4)] +
                     [(self.car, (k,)) for k in ("jeep", "tank")] + self.warm)

    def soldier(self, vals, side):
        """The soldier of a player, 0 to 3, or None. / Le soldat d'un joueur."""
        v = _n(vals.get("soldier" if side == "p1" else "soldier_p2")) if self.SQUAD else None
        return int(v) if v is not None and 0 <= v < len(ST2_SOLDIERS) else None

    def hero(self, frame, side="p1"):
        S = self.S
        who = self.look.get(side)
        vest, pants, hair, band = ST2_LOOKS[who] if who is not None else self.HERO
        return self.img(("st2hero", frame, who), S(150), S(170), soldier_draw(vest, pants, hair, band, frame), ss=2)

    def foe(self, frame):
        S = self.S
        vest, pants, hair, band = self.FOE
        return self.img(("st2foe", frame), S(130), S(148), soldier_draw(vest, pants, hair, band, frame, helmet=True, skin=(214, 164, 124)),
                        ss=2, flip=True)

    def car(self, kind):
        S = self.S
        if kind == "tank":
            return self.img("st2tank", S(300), S(170), tank34_draw, ss=2)
        return self.img("st2jeep", S(230), S(130), jeep_draw, ss=2)

    def road(self, z):
        S = self.S
        return S(ST2_ROAD[0]) + S(70) + z * (S(ST2_ROAD[1]) - S(ST2_ROAD[0]) - S(64))

    def hx(self):
        return self.W * 0.24

    def move(self, vals, now, idle):
        return 0.15 if idle else 0.5

    def hx2(self):
        return self.W * 0.15

    def restart(self, vals, now):
        self.foes = []
        self.next_foe = now + 0.5
        self.next_car = now + 6.0
        self.machines_reset()

    def weapon(self, vals, suf=""):
        w = _n(vals.get("weapon" + suf))
        return ST2_WEAPONS.get(int(w) if w is not None else 0, ST2_WEAPONS[0])

    def second(self, vals, now):
        """The second player's commando: his stick, his gun, his grenades, his lives. / Le commando du second joueur."""
        S, rng, fx = self.S, self.rng, self.fx
        st = self.stick(vals, "p2")
        if st is not None:
            self.hz2 = _clamp(self.hz2 + st[1] * self.dt * 0.8)
        else:
            self.hz2 = 0.5 + 0.4 * math.sin(now * 0.3 + 2.0)
        x0, y0 = self.hx2(), self.road(self.hz2)
        ch = self.changed(vals, "weapon_p2")
        if ch:
            name, col = self.weapon(vals, "_p2")
            self.popup(name + " !", x0, y0 - S(200), col, 40, key="stencil")
        ch = self.changed(vals, "ammo_p2")
        if ch and ch[1] < ch[0]:
            for i in range(min(3, int(ch[0] - ch[1]))):
                fx.later(i * 0.07, self.fire, vals, now, True, "p2")
        elif st is not None and st[2] & 16:
            if now >= self.fire_t2:
                self.fire_t2 = now + 0.1
                self.fire(vals, now, False, "p2")
        elif st is None and now >= self.fire_t2 and any(not f.get("dead") and f["x"] < self.W * 0.8 for f in self.foes):
            self.fire_t2 = now + rng.uniform(0.3, 0.7)
            self.fire(vals, now, False, "p2")
        ch = self.changed(vals, "grenades_p2")
        if ch and ch[1] < ch[0]:
            live = [f for f in self.foes if not f.get("dead") and f["x"] < self.W * 0.95]
            tgt = rng.choice(live) if live else None
            tx = tgt["x"] if tgt else self.W * rng.uniform(0.5, 0.8)
            ty = self.road(tgt["z"]) - S(30) if tgt else self.road(rng.random())
            fx.projectile("grenade_st2", x0, y0 - S(110), tx, ty, 0.7, 160, lambda x, y: self.grenade_boom(x, y, now), spin=720)
        ch = self.changed(vals, "lives_p2")
        if ch and ch[1] < ch[0]:
            self.hurt2 = now
            fx.explosion(x0, y0 - S(60), 0.8, False)
            self.popup(tr("-1 VIE", "-1 LIFE"), x0, y0 - S(220), (255, 90, 70), 38)
        p = _n(vals.get("power_p2"))
        if p is not None:
            lv = 1 + min(2, int(p) // 12)
            if self.lv2 is not None and lv > self.lv2:
                self.popup("LV UP !", x0, y0 - S(200), GOLD, 42, key="stencil")
            self.lv2 = lv

    def update(self, vals, now):
        S, rng, fx = self.S, self.rng, self.fx
        if self.SQUAD:
            for side, suf, x in (("p1", "", self.hx()), ("p2", "_p2", self.hx2())):
                who = self.soldier(vals, side)
                if who is not None:
                    self.look[side] = who
                ch = self.changed(vals, "energy" + suf)
                if ch and ch[1] < ch[0] < 128:                         # hit: the energy falls
                    self.epop[side] = now
                    fx.shake(4 + (ch[0] - ch[1]) * 0.1, 0.25)
                    fx.sparks(x, self.road(self.hz if side == "p1" else self.hz2) - S(90), 12, (255, 120, 90), (200, 600),
                              (200, 340), (0.2, 0.5), 600, "front", 3, 18)
            self.machines(vals, now, self.p1_in(vals) or self.p2_in(vals))
        if self.TWO and self.p2_in(vals):
            self.second(vals, now)
        st = self.stick(vals, "p1")
        if st is not None:
            self.hz = _clamp(self.hz + st[1] * self.dt * 0.8)
        else:
            self.hz = 0.5 + 0.4 * math.sin(now * 0.35)
        if now >= self.next_foe:
            self.next_foe = now + rng.uniform(0.5, 1.2)
            self.foes.append({"kind": "man", "x": self.W + S(60), "z": rng.uniform(0.0, 1.0), "hp": 3, "v": rng.uniform(110, 170) * self.s,
                              "stop": self.hx() + S(rng.uniform(280, 700)), "ph": rng.uniform(0, 6), "shot": now + rng.uniform(1, 3)})
        if now >= self.next_car and not any(f["kind"] != "man" and not f.get("dead") for f in self.foes):
            self.next_car = now + rng.uniform(9, 16)
            kind = rng.choice(("jeep", "tank"))
            self.foes.append({"kind": kind, "x": self.W + S(200), "z": rng.uniform(0.15, 0.85), "hp": 10 if kind == "jeep" else 18,
                              "v": (120 if kind == "jeep" else 60) * self.s, "stop": self.W * rng.uniform(0.6, 0.8), "ph": 0.0,
                              "shot": now + 2.0})
        name, col = self.weapon(vals)
        ch = self.changed(vals, "weapon")
        if ch:
            self.popup(name + " !", self.hx(), self.road(self.hz) - S(200), col, 40, key="stencil")
        ch = self.changed(vals, "ammo")
        if ch and ch[1] < ch[0]:                                       # a special shot per bullet gone (up to 3)
            for i in range(min(3, int(ch[0] - ch[1]))):
                fx.later(i * 0.07, self.fire, vals, now, True)
        elif st is not None and st[2] & 16:
            if now >= self.fire_t:
                self.fire_t = now + 0.1
                self.fire(vals, now, False)
        elif now >= self.fire_t and any(not f.get("dead") and f["x"] < self.W * 0.8 for f in self.foes):
            self.fire_t = now + rng.uniform(0.3, 0.7)
            self.fire(vals, now, False)
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:
            live = [f for f in self.foes if not f.get("dead") and f["kind"] == "man" and f["x"] < self.W * 0.85]
            if live:
                self.kill(min(live, key=lambda f: f["x"]), now)
        ch = self.changed(vals, "grenades")
        if ch and ch[1] < ch[0]:
            self.grenades_thrown += 1
            live = [f for f in self.foes if not f.get("dead") and f["x"] < self.W * 0.95]
            tgt = rng.choice(live) if live else None
            tx = tgt["x"] if tgt else self.W * rng.uniform(0.5, 0.8)
            ty = self.road(tgt["z"]) - S(30) if tgt else self.road(rng.random())
            x0, y0 = self.hx(), self.road(self.hz) - S(110)
            fx.projectile("grenade_st2", x0, y0, tx, ty, 0.7, 160, lambda x, y: self.grenade_boom(x, y, now), spin=720)
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.hurt = now
            fx.explosion(self.hx(), self.road(self.hz) - S(60), 0.8, False)
            self.popup(tr("-1 VIE", "-1 LIFE"), self.hx(), self.road(self.hz) - S(220), (255, 90, 70), 38)
        p = _n(vals.get("power"))
        if p is not None:
            lv = 1 + min(2, int(p) // 12)
            if self.lv is not None and lv > self.lv:
                self.popup("LV UP !", self.hx(), self.road(self.hz) - S(200), GOLD, 42, key="stencil")
            self.lv = lv

    def fire(self, vals, now, special, side="p1"):
        S, fx = self.S, self.fx
        name, col = self.weapon(vals, "" if side == "p1" else "_p2") if special else ST2_WEAPONS[0]
        if special:
            self.specials += 1
        hz = self.hz if side == "p1" else self.hz2
        x0, y0 = (self.hx() if side == "p1" else self.hx2()) + S(70), self.road(hz) - S(90)
        live = [f for f in self.foes if not f.get("dead") and x0 < f["x"] < self.W * 0.85]
        tgt = min(live, key=lambda f: abs(f["x"] - x0) + abs(f["z"] - hz) * S(300)) if live else None
        tx, ty = (tgt["x"], self.road(tgt["z"]) - (S(70) if tgt["kind"] == "man" else S(60))) if tgt else (self.W + S(40), y0)
        if name == "FIRE":
            fx.sparks(x0, y0, 16, col, (700, 1100), (-10, 10), (0.25, 0.45), 0, "front", 10, 40)
            fx.glow(x0 + S(80), y0, 20, 70, col, 0.2, "front", 0.8, 0.0)
        elif name == "ROUND":
            for a in (-1, 0, 1):
                fx.tracer(x0, y0, tx, ty + a * S(50), 2600, col, 9, 18, "front", False)
        elif name == "MISSILE":
            fx.tracer(x0, y0, tx, ty, 1400, col, 10, 70, "front", False)
            fx.later(abs(tx - x0) / (1400 * self.s), fx.small_blast, tx, ty)
        elif name == "BOOMERANG":
            fx.tracer(x0, y0, tx, ty - S(40), 2200, col, 8, 30, "front", False)
        else:
            fx.tracer(x0, y0, tx, ty, 3200, col, 5, 80, "front", True)
        fx.muzzle(x0, y0, 1, 0.5)
        if tgt is not None:
            tgt["hp"] -= 3 if special else 1
            tgt["hit"] = now
            if tgt["hp"] <= 0:
                fx.later(0.08, self.kill, tgt, now)

    def grenade_boom(self, x, y, now):
        self.fx.explosion(x, y, 0.9, False)
        self.fx.shake(6, 0.3)
        for f in self.foes:
            if not f.get("dead") and abs(f["x"] - x) < self.S(180) and abs(self.road(f["z"]) - y) < self.S(140):
                f["hp"] -= 6
                if f["hp"] <= 0:
                    self.kill(f, now)

    def kill(self, f, now):
        if f.get("dead"):
            return
        f["dead"] = now
        self.kills += 1
        if f["kind"] != "man":
            self.fx.explosion(f["x"], self.road(f["z"]) - self.S(60), 1.1, False)
            self.fx.shake(8, 0.4)
        else:
            self.fx.sparks(f["x"], self.road(f["z"]) - self.S(70), 10, (255, 230, 160), (200, 500), (0, 360), (0.2, 0.4), 0, "front", 3, 14)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, dt, rng = self.S, self.dt, self.rng
        items = []
        keep = []
        for f in self.foes:
            dead = f.get("dead")
            if dead is not None:
                if f["kind"] != "man" or now - dead > 1.2:
                    continue
            else:
                speed = f["v"] if f["x"] > f["stop"] else 0.0
                f["x"] -= (speed + self.bd.speed * 0.6) * dt
                if f["x"] < -S(200):
                    continue
                if f["kind"] == "man" and now >= f["shot"] and f["x"] < self.W:     # enemy fire
                    f["shot"] = now + rng.uniform(1.5, 3.5)
                    self.fx.tracer(f["x"] - S(50), self.road(f["z"]) - S(80), self.hx(), self.road(self.hz) - S(80), 900, (255, 90, 80), 6, 16,
                                   "front", False)
            keep.append(f)
            y = self.road(f["z"])
            if f["kind"] == "man":
                if dead is not None:
                    img = self.foe(3)
                    if int(now * 14) % 2 and now - dead > 0.7:
                        continue
                else:
                    img = self.foe(int(now * 7 + f["ph"]) % 2 if f["x"] > f["stop"] else 2)
            else:
                img = self.car(f["kind"])
                if now - f.get("hit", -9) < 0.06:
                    continue
            items.append((y, img, f["x"], y))
        self.foes = keep
        if self.p1_in(vals) and not (now - self.hurt < 1.0 and int(now * 16) % 2):
            frame = 2 if now < self.fire_t - 0.05 else int(now * 8) % 2
            y = self.road(self.hz)
            items.append((y, self.hero(frame), self.hx(), y))
        if self.TWO and self.p2_in(vals) and not (now - self.hurt2 < 1.0 and int(now * 16) % 2):
            frame = 2 if now < self.fire_t2 - 0.05 else int(now * 8 + 1) % 2
            y = self.road(self.hz2)
            items.append((y, self.hero(frame, "p2"), self.hx2(), y))
        for _z, img, x, y in sorted(items, key=lambda it: it[0]):
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height())))
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the face, 1P- and the score, the soldier's name and his energy, TIME in big yellow numbers; at
        the bottom the grenades, the weapon box and LV with its gauge. The second player has the same on the right.
        / Comme dans le jeu : le visage, 1P- et le score, le nom du soldat et son énergie, TIME en gros chiffres jaunes ;
        en bas les grenades, l'arme et LV. Le second joueur a la même chose à droite."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(4), S(420), S(76), now)
        t = _n(vals.get("time"))
        for side, suf, col in (("p1", "", P1C), ("p2", "_p2", P2C)):
            left = side == "p1"
            if not left and not self.p2_in(vals):
                word, colw = self.invite(vals, now)
                self.label(screen, word, W - S(24), S(40), 30, colw, align="right")
                continue
            if left and not self.p1_in(vals):
                continue

            def X(x, w=0):                                             # mirrored for the second player / en miroir
                return S(x) if left else W - S(x) - S(w)
            al, ar = ("left", "right") if left else ("right", "left")
            self.pill(screen, X(10, 620), S(6), S(620), S(84), 160, radius=12)
            who = self.look.get(side) if self.SQUAD else None
            hair, band = (ST2_LOOKS[who][2], ST2_LOOKS[who][3]) if who is not None else ((110, 60, 30), (210, 40, 40))
            face = self.img(("st2face", who), S(70), S(70), lambda d, w, h: face_icon_draw(d, w, h, hair, band), ss=2)
            screen.blit(face, (X(18, 70), S(12)))
            self.text(screen, "1P-" if left else "-2P", X(100), S(30), 28, (230, 200, 255), key="black", align=al, valign="middle")
            name = "score" + suf
            if _n(vals.get(name)) is not None:
                hd._score(screen, eng, name, X(440), S(12), ar, S(40))
            lives = _n(vals.get("lives" + suf))
            if lives is not None:
                self.text(screen, f"x{int(lives)}", X(100), S(66), 26, (255, 230, 120), key="black", align=al, valign="middle")
            if who is not None:                                        # the soldier's name and his energy, as in the game
                self.text(screen, ST2_SOLDIERS[who], X(150), S(66), 26, WHITE, key="black", align=al, valign="middle", glow=0.3)
            e = _n(vals.get("energy" + suf)) if self.SQUAD else None
            if e is not None:
                frac = 0.0 if e >= 128 else _clamp(e / float(self.FULL))
                hit = _clamp(1 - (now - self.epop[side]) / 0.3)
                bx = S(258) if left else W - S(258) - S(182)
                self.bar(screen, bx, S(56), S(182), S(20), frac, (255, 255, 255) if hit > 0.5 else
                         ((250, 220, 40) if frac > 0.34 else (255, 80, 60)))
            if left and t is not None:
                self.text(screen, "TIME", S(470), S(26), 24, (255, 220, 60), key="black", valign="middle")
                hd.put_number(screen, f"{int(t):02d}", "stencil", S(54), (255, 220, 40) if t > 10 else (255, 80, 60), S(540), S(62),
                              "center", "middle")
            y0 = H - S(56)
            self.pill(screen, X(10, 660), y0 - S(6), S(660), S(58), 160, radius=12)
            g = _n(vals.get("grenades" + suf))
            if g is not None:
                screen.blit(self.img("st2gren", S(30), S(36), lambda d, w, h: (
                    d.ellipse([0, h * 0.2, w, h], fill=(60, 120, 60, 255), outline=(250, 250, 250, 255), width=2),
                    d.rectangle([w * 0.35, 0, w * 0.65, h * 0.3], fill=(150, 150, 150, 255)))), (X(20, 30), y0))
                self.text(screen, f"{int(g)}", X(58), y0 + S(18), 30, WHITE, key="black", align=al, valign="middle")
            wname, wcol = self.weapon(vals, suf)
            self.box(screen, X(100, 200), y0, S(200), S(46), (230, 230, 255), fill=(20, 40, 150, 230), radius=4, width=2)
            shot = ST2_SHOT.get(who) if self.SQUAD else "FRONT"         # the normal gun's own name, when seen in the game
            bx = X(100, 200) + S(100)
            self.text(screen, wname, bx, y0 + (S(14) if shot else S(23)), 22, WHITE, key="black", align="center", valign="middle",
                      glow=0)
            if shot:
                self.text(screen, shot, bx, y0 + S(34), 18, (200, 220, 255), key="black", align="center", valign="middle", glow=0)
            p = _n(vals.get("power" + suf))
            if p is not None:
                lv = (self.lv if left else self.lv2) or 1
                self.text(screen, f"LV{lv}", X(316), y0 + S(22), 28, (255, 220, 60), key="black", align=al, valign="middle")
                self.bar(screen, X(390, 170), y0 + S(10), S(170), S(24), p / 36.0, (255, 210, 60))
            a = _n(vals.get("ammo" + suf))
            if a is not None and int(_n(vals.get("weapon" + suf)) or 0):
                self.text(screen, f"{int(a)}", X(650), y0 + S(22), 30, (255, 140, 120), key="black", align=ar, valign="middle")
        if self.SQUAD:
            self.draw_machine(screen, now)


# ============================================================================ Brawlers: Robo Army, Burning Fight
SWORD_ANGLE = {0: -62, 1: -32, 2: -40, 3: 4, 4: -128, 5: 64}            # angle of the blade per frame / angle de la lame


def fighter_draw(style, top, pants, skin, hair, frame, weapon=None):
    """A street fighter of our own seen from the side, facing right. style: "brawler" (a tank top, jeans), "thug"
    (a jacket, a cap, dark glasses), "jacket" (a jacket, short hair), "ninja" (a hood), "samurai" (an armour and a
    helmet with its crest), "mutant" (a bulky creature), "cyborg" (an armoured body, a visor), "robot" (a grey robot,
    one eye). weapon: "sword" (a katana in the front hand). Frames 0 guard, 1 and 2 walk, 3 punch or slash, 4 kick,
    5 hurt, 6 down. / Un combattant de rue à nous, de profil, face à droite, avec ou sans sabre."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, H * 0.009)
        metal = style in ("cyborg", "robot")
        bulk = 1.3 if style == "mutant" else 1.0
        tp, tp_d = top + (255,), _mixc(top, (0, 0, 0), 0.25)
        pt, pt_d = pants + (255,), _mixc(pants, (0, 0, 0), 0.25)
        sk, sk_d = (skin + (255,), _mixc(skin, (0, 0, 0), 0.22)) if not metal else (tp, tp_d)
        u = H
        if frame == 6:                                                 # down, lying on the ground
            y = H * 0.93
            _capsule(d, (W * 0.24, y - 0.03 * u), (W * 0.62, y - 0.03 * u), 0.07 * u * bulk, 0.07 * u * bulk, tp, dark, ow)
            _capsule(d, (W * 0.62, y - 0.02 * u), (W * 0.95, y), 0.05 * u, 0.045 * u, pt, dark, ow)
            head = tp if style == "ninja" else (hair + (255,) if style == "samurai" else sk)
            d.ellipse([W * 0.06, y - 0.12 * u, W * 0.24, y + 0.02 * u], fill=head, outline=dark, width=int(ow))
            return
        cx = W * 0.5
        lean = {3: 0.04, 4: -0.03, 5: -0.07}.get(frame, 0.0)

        def P(x, y):
            return cx + (x + lean * (0.62 - y) / 0.62) * u, y * u
        hip = P(0, 0.56)
        legs = {0: ((-0.06, 0.76, -0.1, 0.97), (0.07, 0.76, 0.1, 0.97)), 1: ((-0.08, 0.76, -0.14, 0.96), (0.08, 0.75, 0.13, 0.97)),
                2: ((0.05, 0.77, 0.03, 0.97), (-0.03, 0.75, -0.1, 0.92)), 3: ((-0.1, 0.76, -0.16, 0.97), (0.08, 0.76, 0.12, 0.97)),
                4: ((-0.08, 0.77, -0.12, 0.97), (0.2, 0.52, 0.36, 0.5)), 5: ((-0.1, 0.77, -0.16, 0.97), (0.04, 0.77, 0.02, 0.97))}[frame]
        for i, (kx, ky, fx_, fy_) in enumerate(legs):
            k, f = P(kx, ky), (cx + fx_ * u, fy_ * u)
            _capsule(d, hip, k, 0.06 * u * bulk, 0.05 * u * bulk, pt_d if i == 0 else pt, dark, ow)
            _capsule(d, k, f, 0.05 * u * bulk, 0.042 * u * bulk, pt_d if i == 0 else pt, dark, ow)
            shoe = (60, 60, 70, 255) if metal else ((30, 30, 36, 255) if style in ("ninja", "samurai") else (40, 32, 28, 255))
            d.rounded_rectangle([f[0] - 0.04 * u, f[1] - 0.035 * u, f[0] + 0.07 * u, f[1] + 0.012 * u], radius=0.015 * u, fill=shoe, outline=dark)
        tw = 0.11 * bulk
        d.polygon([P(-tw, 0.27), P(tw, 0.27), P(0.1, 0.58), P(-0.1, 0.58)], fill=tp, outline=dark)          # le torse
        if style == "brawler":
            d.polygon([P(-0.05, 0.27), P(0.05, 0.27), P(0.04, 0.4), P(-0.04, 0.4)], fill=sk)                     # le débardeur
        elif style in ("thug", "jacket"):
            d.line([P(0.0, 0.27), P(0.0, 0.58)], fill=_mixc(top, (0, 0, 0), 0.5), width=max(1, int(ow * 2)))
            if style == "jacket":                                      # le col ouvert
                d.polygon([P(-0.04, 0.27), P(0.05, 0.27), P(0.0, 0.36)], fill=(240, 240, 240, 255))
        elif style == "samurai":                                       # l'armure à lamelles
            for k in range(5):
                y = 0.32 + k * 0.05
                d.line([P(-0.1, y), P(0.1, y)], fill=_mixc(top, (0, 0, 0), 0.45), width=max(1, int(ow * 1.5)))
        elif style == "ninja":                                         # la ceinture nouée
            d.polygon([P(-0.1, 0.5), P(0.1, 0.5), P(0.1, 0.54), P(-0.1, 0.54)], fill=_mixc(top, (255, 255, 255), 0.3))
        elif metal:
            d.polygon([P(-0.08, 0.3), P(0.09, 0.3), P(0.07, 0.44), P(-0.06, 0.44)], fill=_mixc(top, (255, 255, 255), 0.35), outline=dark)
            d.ellipse([P(0.0, 0.33)[0] - 0.03 * u, P(0.0, 0.33)[1], P(0.0, 0.33)[0] + 0.03 * u, P(0.0, 0.33)[1] + 0.06 * u],
                      fill=hair + (255,))
        if style != "ninja":
            d.rectangle([P(-0.1, 0.54)[0], P(-0.1, 0.54)[1], P(0.1, 0.58)[0], P(0.1, 0.58)[1]], fill=(40, 36, 30, 255))         # la ceinture
        hands = {0: ((0.14, 0.34), (0.2, 0.3)), 1: ((0.12, 0.38), (0.06, 0.42)), 2: ((-0.04, 0.42), (0.14, 0.38)),
                 3: ((0.1, 0.36), (0.36, 0.26)), 4: ((-0.12, 0.34), (0.08, 0.3)), 5: ((-0.14, 0.24), (-0.02, 0.2))}[frame]
        front = None
        for i, (hx, hy) in enumerate(hands):
            s0 = P((-0.07 if i == 0 else 0.07) * bulk, 0.3)
            h = (cx + hx * u, hy * u)
            el = ((s0[0] + h[0]) / 2 - 0.02 * u, max(s0[1], h[1]) + 0.05 * u)
            bare = style in ("brawler", "mutant")
            arm = tp if metal else (sk if bare else tp)
            arm_d = tp_d if metal else (sk_d if bare else tp_d)
            _capsule(d, s0, el, 0.045 * u * bulk, 0.04 * u * bulk, arm_d if i == 0 else arm, dark, ow)
            _capsule(d, el, h, 0.04 * u * bulk, 0.036 * u * bulk, arm_d if i == 0 else arm, dark, ow)
            if style == "samurai" and i == 1:                          # l'épaulière
                d.rectangle([s0[0] - 0.06 * u, s0[1] - 0.02 * u, s0[0] + 0.05 * u, s0[1] + 0.07 * u], fill=_mixc(top, (0, 0, 0), 0.2), outline=dark)
            if i == 1:
                front = h
            else:
                d.ellipse([h[0] - 0.035 * u, h[1] - 0.035 * u, h[0] + 0.035 * u, h[1] + 0.035 * u], fill=sk_d, outline=dark, width=int(ow))
        if weapon == "sword" and front is not None:                    # le sabre dans la main de devant
            a = math.radians(SWORD_ANGLE[frame])
            ln = (0.5 if frame == 3 else 0.42) * u
            tip = (front[0] + math.cos(a) * ln, front[1] + math.sin(a) * ln)
            back = (front[0] - math.cos(a) * 0.1 * u, front[1] - math.sin(a) * 0.1 * u)
            d.line([back, front], fill=(40, 30, 30, 255), width=max(2, int(0.03 * u)))
            d.line([front, tip], fill=dark, width=max(3, int(0.03 * u)))
            d.line([front, tip], fill=(226, 232, 240, 255), width=max(2, int(0.018 * u)))
            d.ellipse([front[0] - 0.022 * u, front[1] - 0.022 * u, front[0] + 0.022 * u, front[1] + 0.022 * u], fill=(200, 170, 60, 255), outline=dark)
        if front is not None:
            d.ellipse([front[0] - 0.035 * u, front[1] - 0.035 * u, front[0] + 0.035 * u, front[1] + 0.035 * u], fill=sk, outline=dark,
                      width=int(ow))
        hx, hy = P(0.02, 0.15)
        r = 0.075 * u * (0.9 if style == "mutant" else 1.0)
        if style == "robot":                                           # tête de robot, un œil
            d.rounded_rectangle([hx - r, hy - r, hx + r, hy + r], radius=r * 0.3, fill=tp, outline=dark, width=int(ow))
            d.rectangle([hx - r * 0.2, hy - r * 0.3, hx + r, hy + r * 0.1], fill=(30, 30, 40, 255))
            d.ellipse([hx + r * 0.3, hy - r * 0.25, hx + r * 0.8, hy + r * 0.05], fill=(255, 60, 40, 255))
            return
        d.ellipse([hx - r, hy - r, hx + r, hy + r * 1.1], fill=sk, outline=dark, width=int(ow))
        if style == "cyborg":                                          # casque à visière
            d.chord([hx - r * 1.05, hy - r * 1.1, hx + r * 1.0, hy + r * 0.5], 180, 360, fill=tp, outline=dark)
            d.rectangle([hx, hy - r * 0.3, hx + r * 1.02, hy + r * 0.1], fill=hair + (255,))
            return
        if style == "ninja":                                           # la cagoule, une fente pour les yeux
            d.ellipse([hx - r, hy - r, hx + r, hy + r * 1.1], fill=tp, outline=dark, width=int(ow))
            d.rectangle([hx - r * 0.1, hy - r * 0.3, hx + r * 0.95, hy + r * 0.05], fill=sk)
            d.ellipse([hx + r * 0.4, hy - r * 0.22, hx + r * 0.62, hy], fill=dark)
            d.polygon([(hx - r * 0.9, hy - r * 0.2), (hx - r * 1.8, hy - r * 0.5), (hx - r * 1.7, hy + r * 0.1)], fill=tp_d)
            return
        d.ellipse([hx + r * 0.35, hy - r * 0.2, hx + r * 0.6, hy + r * 0.05], fill=dark)
        if frame == 5:
            d.line([(hx + r * 0.3, hy - r * 0.3), (hx + r * 0.7, hy)], fill=dark, width=max(1, int(ow * 2)))
        if style == "thug":                                            # casquette et lunettes noires
            d.chord([hx - r * 1.05, hy - r * 1.1, hx + r * 1.0, hy + r * 0.2], 180, 360, fill=hair + (255,))
            d.rectangle([hx, hy - r * 0.3, hx + r * 1.5, hy - r * 0.12], fill=hair + (255,))
            d.rectangle([hx + r * 0.2, hy - r * 0.15, hx + r * 0.95, hy + r * 0.12], fill=(20, 20, 24, 255))
        elif style == "samurai":                                       # le casque et son cimier
            d.chord([hx - r * 1.15, hy - r * 1.2, hx + r * 1.1, hy + r * 0.4], 180, 360, fill=hair + (255,), outline=dark)
            d.rectangle([hx - r * 1.3, hy - r * 0.45, hx + r * 1.2, hy - r * 0.3], fill=_mixc(hair, (0, 0, 0), 0.3))
            d.line([(hx, hy - r * 0.9), (hx - r * 0.6, hy - r * 1.9)], fill=(230, 190, 60, 255), width=max(2, int(r * 0.2)))
            d.line([(hx, hy - r * 0.9), (hx + r * 0.6, hy - r * 1.9)], fill=(230, 190, 60, 255), width=max(2, int(r * 0.2)))
            d.rectangle([hx + r * 0.1, hy + r * 0.3, hx + r * 0.9, hy + r * 0.8], fill=(60, 40, 40, 255))                 # le masque
        elif style == "mutant":                                        # des pointes sur le crâne
            for k in range(4):
                bx = hx - r * 0.8 + k * r * 0.5
                d.polygon([(bx, hy - r * 0.7), (bx + r * 0.25, hy - r * 1.6), (bx + r * 0.5, hy - r * 0.7)], fill=hair + (255,), outline=dark)
        else:                                                          # cheveux en brosse
            d.chord([hx - r * 1.04, hy - r * 1.25, hx + r * 0.96, hy + r * 0.3], 160, 360, fill=hair + (255,), outline=dark)
    return fn


def slash_draw(d, W, H):
    """The bright crescent left by a blade. / Le croissant de lumière laissé par une lame."""
    for k, (col, wd) in enumerate((((90, 170, 255, 150), 0.12), ((190, 230, 255, 220), 0.06), ((255, 255, 255, 255), 0.025))):
        d.arc([W * 0.1, H * 0.1, W * 0.9, H * 0.9], -70, 70, fill=col, width=max(2, int(W * wd)))


class BrawlerScene(GameScene):
    """A beat'em up seen from the side: our hero in the middle of the street, enemies come from both sides; the points
    read in the game are blows that land, the health that goes down is a blow taken, a life lost a fall.
    / Un beat'em up de profil : notre héros au milieu de la rue, les ennemis arrivent des deux côtés."""
    SHADE = (90, 60)
    EXPLOSIONS = False
    HERO = ("brawler", (240, 240, 240), (60, 90, 160), (226, 176, 136), (60, 40, 30))
    FOES = (("thug", (70, 70, 80), (40, 40, 50), (214, 160, 120), (30, 30, 34)),)
    ENERGY_MAX = 255
    ENERGY = "energy"
    HERO2 = None                                          # the second player's fighter; None: the hero in another colour
    TWO = True                                            # the second player fights beside the first; False for a game
                                                          # where the players take turns / False quand ils jouent tour à tour

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.hero = {"x": self.W * 0.42, "z": 0.5, "face": 1, "act": None, "hurt": -99.0, "down": -99.0, "auto": 0.0}
        self.hero2 = {"x": self.W * 0.57, "z": 0.85, "face": -1, "act": None, "hurt": -99.0, "down": -99.0, "auto": 0.0}
        self.lead = self.hero                             # the one the enemies come to / celui vers qui viennent les ennemis
        self.foes = []
        self.next_foe = 0.0
        self.slashes = []
        self.blows = 0                                    # (tests)
        self.knocked = 0
        self.hits = 0
        self.warm = [(self.fig, (self.HERO, f, False)) for f in range(7)] + [(self.fig, (fo, f, True)) for fo in self.FOES for f in (0, 1, 2, 5, 6)] + self.warm

    def fig(self, look, frame, left):
        S = self.S
        style, top, pants, skin, hair = look[:5]
        weapon = look[5] if len(look) > 5 else None
        return self.img(("brawl", look, frame, left), S(420 if weapon else 170), S(250), fighter_draw(style, top, pants, skin, hair, frame, weapon),
                        ss=2, flip=left)

    def look2(self):
        """The second player's fighter: HERO2, or the hero in blue (in red when the hero is blue).
        / Le combattant du second joueur : HERO2, ou le héros en bleu (en rouge quand le héros est bleu)."""
        if self.HERO2 is not None:
            return self.HERO2
        style, top, pants = self.HERO[:3]
        col = (210, 50, 50) if top[2] > top[0] + 40 else (50, 100, 220)
        suit = max(abs(a - b) for a, b in zip(top, pants)) < 90             # one colour from head to toe: all of it changes
        return (style, col, tuple(int(c * 0.82) for c in col) if suit else pants) + tuple(self.HERO[3:])

    def fighters(self, vals):
        """(side, suffix of its values, fighter, look) of each player in the game. / Chaque joueur en jeu."""
        out = []
        if self.p1_in(vals):
            out.append(("p1", "", self.hero, self.HERO))
        if self.TWO and self.p2_in(vals):
            out.append(("p2", "_p2", self.hero2, self.look2()))
        return out

    def ground(self, z):
        return self.S(BRAWL_FLOOR) + self.S(30) + z * (self.H - self.S(BRAWL_FLOOR) - self.S(50))

    def move(self, vals, now, idle):
        return 0.15 if idle else 0.35

    def restart(self, vals, now):
        self.foes = []
        self.next_foe = now + 0.5

    def nearest(self, h=None):
        h = h or self.hero
        live = [f for f in self.foes if f["hp"] > 0]
        return min(live, key=lambda f: abs(f["x"] - h["x"])) if live else None

    def strike(self, now, dmg=1, h=None):
        """A fighter (the hero unless told) hits the enemy nearest to him. / Un combattant frappe l'ennemi le plus proche."""
        S, fx = self.S, self.fx
        h = h or self.hero
        f = self.nearest(h)
        if f is None:
            return
        h["face"] = 1 if f["x"] > h["x"] else -1
        sword = len(self.HERO) > 5 and self.HERO[5] == "sword"
        h["act"] = (now, 3 if sword else self.rng.choice((3, 3, 4)))
        self.blows += 1
        if sword:                                                      # the blade leaves a trail of light
            self.slashes.append((h["x"] + h["face"] * S(60), self.ground(h["z"]) - S(150), now, h["face"]))
        f["hp"] -= dmg
        f["hurt"] = now
        x = (h["x"] + f["x"]) / 2
        y = self.ground(f["z"]) - S(170)
        fx.sparks(x, y, 16, (255, 240, 180), (300, 700), (0, 360), (0.15, 0.35), 0, "front", 3, 18)
        fx.glow(x, y, 16, 70, (255, 250, 220), 0.18, "front", 1.0, 0.0)
        if f["hp"] <= 0:
            self.knocked += 1
            f["down"] = now
            f["vx"] = h["face"] * S(420)
            fx.shake(5, 0.2)

    def update(self, vals, now):
        S, rng = self.S, self.rng
        if now >= self.next_foe and len([f for f in self.foes if f["hp"] > 0]) < 4:
            self.next_foe = now + rng.uniform(1.2, 2.6)
            side = rng.choice((-1, 1))
            self.foes.append({"x": (-S(120) if side < 0 else self.W + S(120)), "z": rng.uniform(0.15, 0.95), "hp": rng.randint(2, 4), "hurt": -99.0,
                              "down": None, "vx": 0.0, "look": rng.choice(self.FOES), "ph": rng.uniform(0, 6), "punch": -99.0,
                              "stop": rng.uniform(S(110), S(170))})
        who = self.fighters(vals)
        self.lead = who[0][2] if who else self.hero
        for _side, suf, h, _look in who:
            ch = self.changed(vals, "score" + suf)
            if ch and ch[1] > ch[0]:
                self.strike(now, 1, h)
                h["auto"] = now + 1.5
            elif now >= h["auto"]:                                     # nobody scores: the fight goes on
                h["auto"] = now + rng.uniform(0.9, 1.8)
                self.strike(now, 1, h)
            ch = self.changed(vals, self.ENERGY + suf)
            if ch and ch[1] < ch[0]:                                   # a blow taken
                self.hits += 1
                h["hurt"] = now
                f = self.nearest(h)
                if f is not None:
                    f["punch"] = now
                    h["face"] = 1 if f["x"] > h["x"] else -1
                self.fx.shake(6, 0.25)
                self.fx.sparks(h["x"], self.ground(h["z"]) - S(180), 14, (255, 140, 120), (200, 500), (0, 360), (0.2, 0.4), 0, "front", 3, 18)
            ch = self.changed(vals, "lives" + suf)
            if ch and ch[1] < ch[0]:
                h["down"] = now
                self.popup(tr("-1 VIE", "-1 LIFE"), h["x"], self.ground(h["z"]) - S(300), (255, 90, 70), 40)
        self.walk(now)

    def walk(self, now):
        S, dt = self.S, self.dt
        h = self.lead
        for f in self.foes:
            if f["down"] is not None:
                f["x"] += f["vx"] * dt
                f["vx"] *= max(0.0, 1 - dt * 3)
                continue
            target = h["x"] + (f["stop"] if f["x"] > h["x"] else -f["stop"])
            dx = target - f["x"]
            f["moving"] = abs(dx) > S(6)
            if f["moving"]:
                f["x"] += max(-S(170) * dt, min(S(170) * dt, dx))
            f["z"] += (h["z"] - f["z"]) * min(1.0, dt * 0.3)
        self.foes = [f for f in self.foes if f["down"] is None or now - f["down"] < 1.6]

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg = self.S, self.pg
        h = self.lead
        items = []
        for f in self.foes:
            if f["down"] is not None:
                k = now - f["down"]
                frame = 5 if k < 0.35 else 6
                if k > 1.0 and int(now * 16) % 2:
                    continue
            elif now - f["hurt"] < 0.3:
                frame = 5
            elif now - f["punch"] < 0.3:
                frame = 3
            elif f.get("moving"):
                frame = 1 + int(now * 6 + f["ph"]) % 2
            else:
                frame = 0
            items.append((f["z"], self.fig(f["look"], frame, f["x"] > h["x"]), f["x"], f["z"]))
        for _side, _suf, h, look in self.fighters(vals):
            if now - h["down"] < 1.2:
                frame = 6
            elif now - h["hurt"] < 0.35:
                frame = 5
            elif h["act"] is not None and now - h["act"][0] < 0.28:
                frame = h["act"][1]
            else:
                frame = 0
            if not (now - h["down"] > 1.2 and now - h["down"] < 2.4 and int(now * 14) % 2):
                items.append((h["z"], self.fig(look, frame, h["face"] < 0), h["x"], h["z"]))
        sh = self.imgs.get("brsh")
        if sh is None:
            sh = self.imgs["brsh"] = pg.Surface((S(110), S(22)), pg.SRCALPHA)
            pg.draw.ellipse(sh, (0, 0, 0, 100), sh.get_rect())
        for z, img, x, zz in sorted(items, key=lambda it: it[0]):
            y = self.ground(zz)
            screen.blit(sh, (int(x - sh.get_width() / 2), int(y - sh.get_height() / 2)))
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height())))
        keep = []
        for sx, sy, t0, face in self.slashes:                           # sword trails / traînées du sabre
            k = (now - t0) / 0.22
            if k >= 1:
                continue
            keep.append((sx, sy, t0, face))
            img = self.img(("slash", face < 0), S(240), S(240), slash_draw, ss=2, flip=face < 0)
            img.set_alpha(int(255 * (1 - k)))
            screen.blit(img, (int(sx - img.get_width() / 2), int(sy - img.get_height() / 2)))
        self.slashes = keep
        self.status(screen, eng, vals, logo, now)


class RoboArmyScene(BrawlerScene):
    """Robo Army as in the game: a cyborg of our own fights the robots at the edge of the town at dusk. The LIFE gauge,
    1P- and the score, the lives and the POW orbs at the top. / Un cyborg à nous combat les robots, comme dans le jeu."""
    THEME = "ra_town"
    HERO = ("cyborg", (190, 40, 40), (120, 30, 30), (226, 176, 136), (255, 220, 60))
    FOES = (("robot", (150, 160, 190), (90, 96, 120), (0, 0, 0), (0, 0, 0)), ("robot", (180, 170, 150), (110, 100, 90), (0, 0, 0), (0, 0, 0)))
    ENERGY_MAX = 10

    def status(self, screen, eng, vals, logo, now):
        """As in the game: LIFE in blue, 1P- and the score, x and the lives, the POW orbs; the same panel on the right for
        the second player. / LIFE, 1P-, les vies, POW ; le même panneau à droite pour le second joueur."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        cols = ((60, 220, 80), (60, 220, 80), (250, 140, 40), (250, 140, 40), (240, 60, 60), (230, 60, 160))
        for side, suf, ox in self.panels(screen, vals, now, 640):
            self.pill(screen, ox + S(12), S(6), S(640), S(104), 160, radius=14)
            e = _n(vals.get("energy" + suf))
            self.text(screen, "LIFE", ox + S(30), S(30), 26, (90, 200, 255), key="black", valign="middle")
            if e is not None:
                self.bar(screen, ox + S(110), S(18), S(300), S(24), e / float(self.ENERGY_MAX), (80, 180, 255))
            self.text(screen, "1P-" if side == "p1" else "2P-", ox + S(440), S(30), 26, (255, 230, 120), key="black", valign="middle")
            if _n(vals.get("score" + suf)) is not None:
                hd._score(screen, eng, "score" + suf, ox + S(636), S(10), "right", S(40))
            lives = _n(vals.get("lives" + suf))
            if lives is not None:
                self.text(screen, f"x{int(lives)}", ox + S(30), S(80), 28, (255, 230, 120), key="black", valign="middle")
            self.text(screen, "POW", ox + S(96), S(80), 26, (255, 230, 120), key="black", valign="middle")
            b = _n(vals.get("bombs" + suf))
            for i in range(6):
                on = b is not None and i < int(b)
                c = cols[i] if on else (60, 60, 70)
                pg.draw.circle(screen, c, (ox + S(190) + i * S(40), S(80)), S(15))
                pg.draw.circle(screen, (240, 240, 240) if on else (90, 90, 100), (ox + S(190) + i * S(40), S(80)), S(15), max(1, S(2)))


class BurningFightScene(BrawlerScene):
    """Burning Fight as in the game: our street fighter in a street of small Japanese shops at night, the thugs come
    from both sides. 1UP and the score, the yellow health gauge, TIME in big yellow numbers in the middle, the lives at
    the bottom left. / Notre combattant dans une rue de petites boutiques la nuit, comme dans le jeu."""
    THEME = "bf_street"
    HERO = ("brawler", (250, 250, 250), (60, 90, 160), (226, 176, 136), (60, 40, 30))
    FOES = (("thug", (60, 60, 70), (40, 40, 52), (214, 160, 120), (30, 30, 34)), ("thug", (150, 40, 40), (50, 50, 60), (200, 150, 110), (240, 240, 240)),
            ("brawler", (230, 230, 230), (70, 110, 180), (190, 140, 100), (30, 26, 24)))

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1UP and the score, the yellow gauge, TIME in the middle, P= the lives at the bottom left; 2UP
        and the same on the right. / Comme dans le jeu : 1UP et le score, la jauge jaune, TIME au milieu, P= et les vies
        en bas à gauche ; 2UP et la même chose à droite."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(4), S(360), S(64), now)
        for side, suf, ox in self.panels(screen, vals, now, 520):
            self.pill(screen, ox + S(12), S(6), S(520), S(84), 160, radius=14)
            self.text(screen, "1UP" if side == "p1" else "2UP", ox + S(30), S(28), 26, (255, 220, 60), key="black", valign="middle")
            if _n(vals.get("score" + suf)) is not None:
                hd._score(screen, eng, "score" + suf, ox + S(500), S(8), "right", S(40))
            e = _n(vals.get("energy" + suf))
            if e is not None:
                self.bar(screen, ox + S(30), S(56), S(480), S(22), e / 255.0, (255, 220, 40), back=(60, 20, 20))
            lives = _n(vals.get("lives" + suf))
            if lives is not None:
                self.label(screen, f"P={int(lives)}", ox + (S(70) if side == "p1" else S(474)), H - S(34), 30, (255, 220, 60), align="center")
        t = _n(vals.get("time"))
        if t is not None:
            self.pill(screen, W / 2 - S(80), S(70), S(160), S(104), 170, radius=14)
            self.text(screen, "TIME", W / 2, S(86), 30, (255, 220, 60), key="stencil", align="center", valign="middle")
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(70), (255, 230, 60), W / 2, S(134), "center", "middle")


SCENES = {"nam1975": NamScene, "cyberlip": CyberLipScene, "gpilots": GhostPilotsScene, "alpham2": AlphaMission2Scene,
          "viewpoin": ViewpointScene, "zedblade": ZedBladeScene, "preisle2": PrehistoricIsle2Scene, "roboarmy": RoboArmyScene,
          "burningf": BurningFightScene}                        # Shock Troopers 2nd Squad has its own scene (hd_squad); the class
# ShockTroopers2Scene above stays as the base of Ninja Commando / reste la base de Ninja Commando
