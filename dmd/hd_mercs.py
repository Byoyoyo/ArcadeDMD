"""Mercs (Capcom, CPS1, 1990): a scene of its own, laid out like Metal Slug (1.36).

Each player's panel: energy at the top, the score in the middle of its band, the weapon held drawn on its card with its
power (the POW picked up), the mega crashes and the four weapons of the game at the bottom. In the middle: the mission,
the timer, and the boss when it comes, announced, with its life bar. Every kill fires the weapon of the card and blows
up in the middle; a mega crash sets the whole marquee on fire.

Mercs, une scène à lui, disposée comme Metal Slug : l'énergie en haut de chaque panneau, le score au milieu de sa bande,
l'arme tenue dessinée sur sa carte avec sa puissance (les POW ramassés), les méga crashs et les quatre armes du jeu en
bas. Au milieu, la mission, le chrono, et le boss quand il arrive, annoncé, avec sa barre de vie. Chaque ennemi abattu
fait tirer l'arme de la carte et exploser le milieu ; un méga crash embrase tout le marquee."""
import math

from .hd_fx import Particle
from .hd_games import GameScene, _n
from .hd_mslug import ACCENT, CREAM, GOLD, GREY, PH, PW, RED, TIP, panel_img, weapon_img
from .i18n import tr

# the game's weapons by its code (games/mercs.json), drawn like those of Metal Slug / les armes du jeu par leur code
KINDS = {0: "mg", 1: "flame", 2: "shotgun", 3: "rocket"}
NAMES = {0: ("FUSIL D'ASSAUT", "ASSAULT RIFLE"), 1: ("LANCE-FLAMMES", "FLAMETHROWER"), 2: ("FUSIL À POMPE", "SHOTGUN"),
         3: ("LANCE-GRENADES", "GRENADE LAUNCHER")}
SHOT = {"mg": (255, 220, 120), "flame": (255, 150, 60), "shotgun": (120, 255, 140), "rocket": (255, 190, 90)}   # the
# colour of each one's shots, the shotgun's green as in the game / la couleur des tirs, le vert du fusil à pompe
ARMOUR = 9000           # a life of 9000 or more is a boss coming in, still armoured: 10000 at mission 2, 9999 at mission 3,
                        # the game's bar shows full; it then gives the life of each part of the boss in the same entry
                        # (the recording of 12 November) / une vie de 9000 ou plus est un boss qui arrive, encore blindé
BOSS_MIN = 350          # without armour, a life of at least that much is the boss: 400 for the jet of mission 1; the guns of
                        # mission 3 have 300 and the game shows no bar for them / sans blindage, le boss a au moins ça
GONE = 1.0              # seconds at 0 before a boss whose parts are not known is counted down: one part can fall to 0 just
                        # before the next comes in (mission 3) / secondes à 0 avant de compter tombé un boss aux parties inconnues
PIPS = 5                # power cases shown, more when the power goes beyond / cases de puissance montrées
GREEN = (90, 230, 110)


def _clamp(v, a=0.0, b=1.0):
    return a if v < a else b if v > b else v


def _fmt(n):
    return f"{int(n):,}".replace(",", " ")


class Side:
    """What the scene remembers of one player. / Ce que la scène retient d'un joueur."""

    def __init__(self):
        self.score_disp = None
        self.score_t = -99.0
        self.hit_t = -99.0
        self.heal_t = -99.0
        self.weapon_t = -99.0
        self.power_t = -99.0
        self.crash_t = -99.0
        self.recoil_t = -99.0
        self.energy = None          # the bar drawn, following the game's value / la barre dessinée


class BossAlert:
    """The boss of a shoot'em up announced and followed (Mercs, then Strikers 1945 Plus, 1.36): ALERTE ! with the sirens
    and red edges, its bar with BOSS over it. The scene keeps "alarm" (when it was announced). / Le boss annoncé et suivi :
    ALERTE ! avec les sirènes et les bords rouges, sa barre avec BOSS dessus."""
    alarm = -99.0

    def announce(self, now):
        self.alarm = now
        self.slam(tr("ALERTE !", "WARNING!"), RED, now, 2.4, sub=tr("UN BOSS ARRIVE", "A BOSS IS COMING"))
        self.fx.shake(8, 0.6)
        for i in range(4):                                          # the sirens on both edges / les sirènes des deux bords
            for x in (self.S(30), self.W - self.S(30)):
                self.fx.glow(x, self.H / 2, 60, 420, (255, 30, 30), 0.35, "back", 0.8, 0.0, delay=i * 0.6, hot=0.2)

    def draw_alarm(self, screen, now):
        if now - self.alarm < 3.0:                                  # red stripes on the edges while the alarm rings
            k = 0.5 + 0.5 * math.sin((now - self.alarm) * 12)
            for x in (0, self.W - self.S(10)):
                self.pg.draw.rect(screen, (int(140 + 115 * k), 20, 20), (x, 0, self.S(10), self.H))

    def draw_boss(self, screen, B, cx, y, now):
        hd, S, pg = self.hd, self.S, self.pg
        if B["down"] is not None:
            return
        k = now - B["t0"]
        blink = k < 3.0 and int(k * 6) % 2 == 0
        hd.put(screen, hd.text("BOSS", "stencil", S(34), (255, 236, 220) if blink else RED, glow=0.6, outline=(60, 0, 0), stroke=max(2, S(4))),
               cx, y + S(8), "center", "middle")
        bw, bh = S(540), S(20)
        r = pg.Rect(int(cx - bw / 2), int(y + S(30)), bw, bh)
        pg.draw.rect(screen, (30, 10, 14), r, border_radius=S(6))
        frac = self.boss_left(B) if "armour" in B else _clamp(B["hp"] / max(1, B["top"]))
        grow = _clamp(k / 0.8)                                       # the bar fills as it comes / la barre se remplit
        hit = max(0.0, 1 - (now - B["hit_t"]) / 0.25)
        fill = pg.Rect(r.x + S(3), r.y + S(3), max(0, int((bw - S(6)) * frac * grow)), bh - S(6))
        if fill.width:
            c = (255, 255, 230) if hit > 0.5 else ((255, 70, 50) if frac > 0.3 else (255, 150, 40))
            pg.draw.rect(screen, c, fill, border_radius=S(4))
        pg.draw.rect(screen, (255, 120, 110) if blink else (150, 60, 60), r, max(1, S(2)), border_radius=S(6))



class MercsScene(BossAlert, GameScene):
    THEME = "mc_desert"
    SHADE = (60, 90)
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS + (("ALERTE !", RED), ("BOSS DÉTRUIT !", GOLD), ("MÉGA CRASH !", GOLD)) + \
        tuple((f"MISSION {n}", GOLD) for n in range(1, 8))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        s = hd.s
        self.panels = {side: hd._surf(panel_img(side, s, ACCENT[side])) for side in ("p1", "p2")}
        self.sides = {"p1": Side(), "p2": Side()}
        self.guns = {}
        self.boss = None            # {"hp", "top", "part", "parts", "armour", "t0", "hit_t", "down"} of the mission
        self.boss_seen = None       # the mission whose boss was announced / la mission dont le boss a été annoncé
        self.mission = None
        self.alarm = -99.0          # when the boss was announced: the sirens / quand le boss a été annoncé : les sirènes

    # ------------------------------------------------------------ places / emplacements
    def x0(self, side):
        return self.S(18) if side == "p1" else self.W - self.S(18 + PW)

    def X(self, side, lx, w=0):
        """x of something lx from the outer edge of the panel. / x d'un élément à lx du bord extérieur."""
        x0 = self.x0(side)
        return x0 + self.S(lx) if side == "p1" else x0 + self.S(PW) - self.S(lx) - self.S(w)

    def slot(self, side):
        return self.X(side, PW - 222, 190), self.S(14 + 195)

    def tip(self, side, kind):
        sx, sy = self.slot(side)
        tx, ty = TIP.get(kind, TIP["mg"])
        if side == "p2":
            tx = 1 - tx
        return sx + tx * self.S(190), sy + ty * self.S(108)

    def gun(self, kind, side, w=190, h=108):
        key = (kind, side, w, h)
        g = self.guns.get(key)
        if g is None:
            from PIL import ImageOps
            img = weapon_img(kind, self.S(w), self.S(h))
            if side == "p2":
                img = ImageOps.mirror(img)
            g = self.guns[key] = self.hd._surf(img)
        return g

    @staticmethod
    def v(vals, side, name):
        return _n(vals.get(name if side == "p1" else name + "_p2"))

    def playing(self, vals, side):
        return self.p1_in(vals) if side == "p1" else self.p2_in(vals)

    @staticmethod
    def p1_in(vals):
        return vals.get("p1_mode") in (1, 2)

    # ------------------------------------------------------------ what happens / ce qui se passe
    def always(self, vals, now):
        m = _n(vals.get("mission"))
        if m is not None and m != self.mission:
            if self.mission is not None and m > self.mission:
                self.slam(f"MISSION {int(m)}", GOLD, now, 1.8)
            self.mission = m
            self.boss = None
        self.track_boss(vals, now)

    def restart(self, vals, now):
        for P in self.sides.values():
            P.score_disp = None

    def update(self, vals, now):
        for side in ("p1", "p2"):
            if not self.playing(vals, side):
                continue
            P = self.sides[side]
            suf = "" if side == "p1" else "_p2"
            ch = self.changed(vals, "score" + suf)
            if ch and ch[1] > ch[0]:
                self.kill(side, ch[1] - ch[0], vals, now)
            ch = self.changed(vals, "health" + suf)
            if ch and ch[1] < ch[0] and ch[1] > 0:
                P.hit_t = now
                self.fx.shake(4 + min(10, (ch[0] - ch[1]) * 0.4), 0.3)
            elif ch and ch[1] > ch[0] and ch[0] > 0:
                P.heal_t = now
                x, y = self.X(side, 330), self.S(14 + 40)
                self.fx.sparks(x, y, 24, GREEN, (150, 500), (200, 340), (0.4, 0.9), 300, "front", 3, 24)
                self.popup(tr("+ ÉNERGIE", "+ ENERGY"), x, self.S(110), GREEN, 34, 1.2, 50)
            ch = self.changed(vals, "weapon" + suf)
            if ch:
                P.weapon_t = now
                name = NAMES.get(int(ch[1]), ("?", "?"))
                sx, sy = self.slot(side)
                self.fx.glow(sx + self.S(95), sy + self.S(54), 30, 170, GOLD, 0.45, "front", 0.9, 0.0, hot=0.6)
                self.fx.sparks(sx + self.S(95), sy + self.S(54), 30, GOLD, (200, 700), (0, 360), (0.3, 0.8), 400, "front", 3, 24)
                self.popup(tr(name[0], name[1]) + " !", sx + self.S(95), self.S(14 + 300), GOLD, 30, 1.3, 50)
            ch = self.changed(vals, "weapon_level" + suf)
            if ch and ch[1] > ch[0]:
                self.power_up(side, int(ch[1]), now)
            ch = self.changed(vals, "bombs" + suf)
            if ch and ch[1] < ch[0]:
                self.mega_crash(side, now)

    def kill(self, side, gain, vals, now):
        """Points scored: the weapon of the card fires, the shot blows up in the middle, as big as the points.
        / Des points : l'arme de la carte tire, le tir explose au milieu, aussi gros que les points."""
        P = self.sides[side]
        P.score_t = now
        rng, S = self.rng, self.S
        if self.boss and self.boss.get("down") is not None:      # the boss fell: the bonus is counted, no more shots
            x = self.W / 2 + rng.uniform(-120, 120) * self.s     # / le boss est tombé : le bonus se compte
            self.fx.text(f"+{_fmt(gain)}", x, S(330), GOLD, 40, life=1.0, rise=80)
            return
        code = self.v(vals, side, "weapon")
        kind = KINDS.get(int(code) if code is not None else 0, "mg")
        # on the player's side of the middle, clear of the timer / du côté du joueur, à l'écart du chrono
        d0 = rng.uniform(150, 290) * self.s
        tx = self.W / 2 - d0 if side == "p1" else self.W / 2 + d0
        ty = S(rng.uniform(250, 390))
        x, y = self.tip(side, kind)
        P.recoil_t = now
        d = 1 if side == "p1" else -1
        self.fx.muzzle(x, y, d, 1.2, SHOT[kind])
        if kind == "flame":
            for i in range(6):
                k = (i + 1) / 6
                self.fx.glow(x + (tx - x) * k * 0.5, y + (ty - y) * k * 0.5, 16, 40 + 30 * k, (255, 140 - 40 * k, 50), 0.35, "front", 0.9, 0.0,
                             delay=i * 0.03, hot=0.5)
        elif kind == "shotgun":
            for a in (-18, 0, 18):
                self.fx.tracer(x, y, tx, ty + S(a), 2400, SHOT[kind], 5, 90)
        elif kind == "rocket":
            self.fx.tracer(x, y, tx, ty, 1600, SHOT[kind], 7, 70)
        else:
            for i in range(3):
                self.fx.tracer(x, y, tx + S(rng.uniform(-20, 20)), ty + S(rng.uniform(-14, 14)), 2600, SHOT[kind], 4, 140)
        delay = 0.12
        if gain >= 300:                                          # a vehicle, a gun: a real explosion / une vraie explosion
            self.fx.later(delay, self.fx.explosion, tx, ty, min(1.1, 0.55 + gain / 2500), True)
        else:                                                    # a soldier: a blast, sparks and smoke / un soldat
            self.fx.later(delay, self.fx.small_blast, tx, ty, 1.6, "front")
            self.fx.later(delay, self.fx.glow, tx, ty, 20, 120, (255, 200, 120), 0.3, "front", 0.9, 0.0)
            self.fx.later(delay, self.fx.shake, 3, 0.15)
        if gain >= 100:
            self.fx.text(f"+{_fmt(gain)}", tx, ty - S(50), GOLD, 30 if gain < 1000 else 42, delay=delay, life=0.9, rise=70)

    def power_up(self, side, level, now):
        """A POW picked up: the cases of the power light one more, the weapon shines. / Un POW ramassé."""
        P = self.sides[side]
        P.power_t = now
        sx, sy = self.slot(side)
        self.fx.glow(sx + self.S(95), sy + self.S(54), 30, 200, (255, 236, 160), 0.5, "front", 1.0, 0.0, hot=0.8)
        r = self.fx.add(Particle("ring", sx + self.S(95), sy + self.S(54), now, 0.5, "front"))
        r.r0, r.r1, r.col, r.a0, r.a1, r.data = 20 * self.s, 160 * self.s, GOLD, 0.9, 0.0, 6 * self.s
        self.popup(tr("PUISSANCE +1 !", "POWER UP!"), sx + self.S(95), self.S(14 + 300), GOLD, 30, 1.3, 50)

    def mega_crash(self, side, now):
        """A mega crash: the whole marquee blows up, from the player's side to the other. / Tout le marquee explose."""
        self.sides[side].crash_t = now
        self.slam(tr("MÉGA CRASH !", "MEGA CRASH!"), GOLD, now, 1.4)
        self.fx.flash((255, 240, 210), 0.55, 0.3)
        xs = [0.12, 0.3, 0.5, 0.7, 0.88]
        if side == "p2":
            xs = xs[::-1]
        for i, f in enumerate(xs):
            self.fx.later(0.08 * i, self.fx.explosion, self.W * f, self.S(self.rng.uniform(200, 360)), 0.9, True)
        self.fx.shake(22, 1.0)

    # ------------------------------------------------------------ the boss / le boss
    def boss_parts(self):
        """How many parts the boss of this mission has, from the game file ("hd": "boss_parts"), None when not known.
        Le nombre de parties du boss de cette mission, d'après le fichier du jeu, None s'il ne le dit pas."""
        parts = (getattr(self, "hd_opts", None) or {}).get("boss_parts")
        if not isinstance(parts, dict) or self.mission is None:
            return None
        n = _n(parts.get(str(int(self.mission))))
        return int(n) if n is not None and n >= 1 else None

    def find_boss(self, hps):
        """(entry, life, armoured) of the boss in the enemy table, None when it is not there. An armoured one first.
        (case, vie, blindé) du boss dans la table des ennemis, None s'il n'y est pas. Un blindé d'abord."""
        lives = [(int(h), i) for i, h in enumerate(hps) if isinstance(h, (int, float))]
        armour = [(h, i) for h, i in lives if ARMOUR <= h <= 10050]
        if armour:
            h, i = max(armour)
            return i, h, True
        big = [(h, i) for h, i in lives if BOSS_MIN <= h < ARMOUR]
        if big:
            h, i = max(big)
            return i, h, False
        return None

    def track_boss(self, vals, now):
        """The boss: announced when it comes, its bar for the whole boss, every part of it in turn, it blows up when the
        last one falls. The game keeps the boss in one entry of its table: armoured as it comes in (the bar full), then the
        life of each part, the next one coming in as the one before falls. / Le boss : annoncé, sa barre pour tout le boss,
        chacune de ses parties à son tour, son explosion quand la dernière tombe."""
        hps = vals.get("_hps")
        if not isinstance(hps, (list, tuple)):
            return
        B = self.boss
        if B is None or (not B["armoured"] and B["down"] is None):
            found = self.find_boss(hps) if not self.nobody(vals) else None
            if found is not None and (B is None or (found[2] and not B["armoured"])):   # an armoured boss after a big
                i, hp, armour = found                                                     # enemy: the real one
                self.boss = {"i": i, "hp": hp, "top": hp, "armour": armour, "armoured": armour, "part": 0,
                             "parts": self.boss_parts(), "t0": now, "hit_t": -99.0, "down": None, "zero_t": None}
                if self.boss_seen != self.mission or (armour and B is not None):
                    self.boss_seen = self.mission
                    self.announce(now)
                return
            if B is None:
                return
        if B["down"] is not None:
            return
        h = hps[B["i"]] if B["i"] < len(hps) else None              # its own entry, whatever its life now / sa propre case
        hp = int(h) if isinstance(h, (int, float)) and 0 <= h <= 10050 else 0
        if B["armour"]:
            if hp >= ARMOUR:                                         # still armoured: the shots only scratch it
                if hp < B["hp"]:
                    self.boss_hit(B, now)
                B["hp"] = hp
                return
            B["armour"] = False                                      # its first part / sa première partie
            if hp > 0:
                B["hp"] = B["top"] = hp
                return
        if hp > B["hp"] + 5 and B["hp"] < B["top"]:                 # the next part comes in / la partie suivante arrive
            self.part_down(B, now)
            B["part"] += 1
            B["hp"] = B["top"] = hp
            B["zero_t"] = None
            return
        if hp < B["hp"]:
            self.boss_hit(B, now)
        B["hp"] = hp
        if hp > 0:
            B["zero_t"] = None
            return
        if B["zero_t"] is None:
            B["zero_t"] = now
        last = B["parts"] is not None and B["part"] + 1 >= B["parts"]
        if last or now - B["zero_t"] >= (GONE if B["parts"] is None else 3.0):
            B["down"] = now
            self.boss_down(now)

    def boss_left(self, B):
        """What is left of the whole boss, 0 to 1: its parts not fallen yet and the life of the one fighting. Without the
        number of parts, the life of the one fighting. / Ce qui reste de tout le boss, de 0 à 1."""
        if B["armour"]:
            return 1.0
        part = _clamp(B["hp"] / max(1, B["top"]))
        n = B["parts"]
        if not n:
            return part
        return _clamp((max(0, n - B["part"] - 1) + part) / n)

    def boss_hit(self, B, now):
        B["hit_t"] = now
        left = self.boss_left(B)
        self.fx.sparks(self.W / 2 + self.S((left - 0.5) * 520), self.S(300), 12, (255, 220, 160), (150, 500), (180, 360), (0.2, 0.5),
                       600, "front", 2, 20)

    def part_down(self, B, now):
        """A part of the boss falls: it blows up on its bar. / Une partie du boss tombe : elle explose sur sa barre."""
        x = self.W / 2 + self.S((self.boss_left(B) - 0.5) * 520)
        self.fx.explosion(x, self.S(296), 0.7, True)
        self.fx.shake(10, 0.4)

    def boss_down(self, now):
        cx = self.W / 2
        for i in range(7):
            x = cx + self.rng.uniform(-260, 260) * self.s
            y = self.S(self.rng.uniform(180, 360))
            self.fx.later(0.12 * i, self.fx.explosion, x, y, 1.0 if i < 6 else 1.4, True)
        self.fx.later(0.9, self.fx.flash, (255, 250, 230), 0.6, 0.35)
        self.fx.later(0.9, self.slam, tr("BOSS DÉTRUIT !", "BOSS DESTROYED!"), GOLD, now + 0.9, 2.0)
        if self.mission is not None:
            m = int(self.mission)
            self.fx.later(3.2, self.slam, tr(f"MISSION {m} ACCOMPLIE !", f"MISSION {m} COMPLETE!"), GOLD, now + 3.2, 2.4)

    # ------------------------------------------------------------ drawing / dessin
    def draw_hud(self, screen, eng, vals, logo, now):
        self.draw_center(screen, vals, logo, now)
        for side in ("p1", "p2"):
            self.draw_panel(screen, side, vals, now)
        self.draw_alarm(screen, now)

    def draw_center(self, screen, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        cx = W / 2
        hd.draw_logo(screen, logo, cx, S(8), S(560), S(104), now)
        m = _n(vals.get("mission"))
        if m is not None:
            t = hd.text(f"MISSION {int(m)}", "stencil", S(34), CREAM, glow=0.3)
            hd.put(screen, t, cx, S(128), "center", "middle")
            for d, col in ((-1, ACCENT["p1"]), (1, ACCENT["p2"])):
                hd.put(screen, hd.text("‹‹‹" if d < 0 else "›››", "black", S(30), col, glow=0.3), cx + d * (t["w"] / 2 + S(34)), S(128),
                       "center", "middle")
        tm = _n(vals.get("time"))
        B = self.boss
        by = S(236) if B is not None and (B["down"] is None or now - B["down"] < 3.0) else None
        if tm is not None:
            low = tm < 30
            blink = low and int(now * 4) % 2 == 0
            col = RED if low else GOLD
            bw, bh = S(170), S(84)
            y = S(152)
            self.box(screen, cx - bw / 2, y, bw, bh, (255, 120, 100) if blink else (255, 240, 220), fill=(8, 10, 22, 210), radius=14, width=3)
            hd.put(screen, hd.text(tr("TEMPS", "TIME"), "bold", S(18), CREAM, glow=0), cx, y + S(14), "center", "middle")
            hd.put_number(screen, str(int(tm)), "stencil", S(50), col, cx, y + S(52), "center", "middle")
        if by is not None:
            self.draw_boss(screen, B, cx, by + S(14), now)

    def draw_panel(self, screen, side, vals, now):
        hd, S, pg = self.hd, self.S, self.pg
        P = self.sides[side]
        acc = ACCENT[side]
        hit = max(0.0, 1 - (now - P.hit_t) / 0.4)
        x0 = self.x0(side) + (int(math.sin(now * 90) * S(6) * hit) if hit else 0)
        y0 = S(14)
        screen.blit(self.panels[side], (x0, y0))
        chip = pg.Rect(self.X(side, 18, 84), y0 + S(10), S(84), S(48))
        pg.draw.rect(screen, acc, chip, border_radius=S(8))
        hd.put(screen, hd.text(tr("J1", "P1") if side == "p1" else tr("J2", "P2"), "stencil", S(36), (24, 14, 8), glow=0), chip.centerx,
               chip.centery, "center", "middle")
        if not self.playing(vals, side):
            credits = _n(vals.get("credits"))
            word = tr("APPUIE SUR START", "PRESS START") if credits is None or credits > 0 else "INSERT COIN"
            col = ACCENT[side] if credits is None or credits > 0 else GOLD
            hd.put(screen, hd.text(word, "stencil", S(46), col, glow=0.5), x0 + S(PW) / 2, S(230), "center", "middle", scale=1 + 0.04 * hd._pulse(now))
            if credits is None or credits > 0:
                hd.put(screen, hd.text(tr("POUR REJOINDRE LA PARTIE", "TO JOIN THE GAME"), "bold", S(22), GREY, glow=0), x0 + S(PW) / 2, S(290),
                       "center", "middle")
            return
        self.draw_energy(screen, side, vals, now, chip)
        # the score in the middle of its band / le score au milieu de sa bande
        score = self.v(vals, side, "score")
        if score is not None:
            if P.score_disp is None or score < P.score_disp:
                P.score_disp = score
            else:
                gap = score - P.score_disp
                P.score_disp = min(score, P.score_disp + max(1, int(gap * 0.18) + 1)) if gap else score
            pop = max(0.0, 1 - (now - P.score_t) / 0.22)
            hd.put_number(screen, _fmt(P.score_disp), "stencil", S(86), GOLD, x0 + S(PW) / 2, y0 + S(128), "center", "middle",
                          scale=1 + 0.12 * pop)
        self.draw_weapon(screen, side, vals, now)
        self.draw_bottom(screen, side, vals, now)
        if hit:
            red = pg.Surface((S(PW), S(PH))).convert()
            red.fill((int(110 * hit), 0, 0))
            screen.blit(red, (x0, y0), special_flags=pg.BLEND_RGB_ADD)

    def draw_energy(self, screen, side, vals, now, chip):
        hd, S, pg = self.hd, self.S, self.pg
        P = self.sides[side]
        e = self.v(vals, side, "health")
        if e is None:
            return
        top = self.v(vals, side, "health_top")                       # the player's top life grows in the game (1.37)
        f = _clamp(e / (top if top and top > 0 else 100.0))          # / le maximum du joueur grandit dans le jeu
        P.energy = f if P.energy is None else P.energy + (f - P.energy) * 0.15
        bw, bh = S(390), S(30)
        bx = self.X(side, 124, 390)
        by = chip.centery - bh // 2
        low = f < 0.25
        heal = max(0.0, 1 - (now - P.heal_t) / 0.6)
        pg.draw.rect(screen, (40, 14, 18), (bx, by, bw, bh), border_radius=S(8))
        w = int((bw - S(6)) * P.energy)
        if w > 0:
            col = (255, 70, 50) if low and int(now * 5) % 2 == 0 else ((255, 190, 60) if f < 0.5 else GREEN)
            if heal:
                col = tuple(int(c + (255 - c) * heal * 0.6) for c in col)
            x = bx + S(3) if side == "p1" else bx + bw - S(3) - w
            pg.draw.rect(screen, col, (x, by + S(3), w, bh - S(6)), border_radius=S(6))
        pg.draw.rect(screen, (255, 255, 255), (bx, by, bw, bh), max(1, S(2)), border_radius=S(8))
        lab = hd.text(tr("ÉNERGIE", "ENERGY"), "xbold", S(16), (20, 20, 26) if w > S(120) else CREAM, glow=0)
        hd.put(screen, lab, bx + S(14) if side == "p1" else bx + bw - S(14), by + bh / 2, "left" if side == "p1" else "right", "middle")

    def draw_weapon(self, screen, side, vals, now):
        hd, S, pg = self.hd, self.S, self.pg
        P = self.sides[side]
        code = self.v(vals, side, "weapon")
        if code is None:
            return
        code = int(code)
        kind = KINDS.get(code, "mg")
        name = tr(*NAMES.get(code, ("?", "?")))
        wt = now - P.weapon_t
        sx, sy = self.slot(side)
        img = self.gun(kind, side)
        kick = max(0.0, 1 - (now - P.recoil_t) / 0.08) * S(6) * (-1 if side == "p1" else 1)
        pop = max(0.0, 1 - wt / 0.35) + 0.6 * max(0.0, 1 - (now - P.power_t) / 0.4)
        if pop:
            k = 1 + 0.3 * pop
            img = pg.transform.smoothscale(img, (int(img.get_width() * k), int(img.get_height() * k)))
        screen.blit(img, (int(sx + S(95) - img.get_width() / 2 + kick), int(sy + S(54) - img.get_height() / 2)))
        slide = max(0.0, 1 - wt / 0.3)
        nx = self.X(side, 36) + (-1 if side == "p1" else 1) * S(60) * slide
        size = hd.fit_size(name, "stencil", S(40), S(360), S(20))
        hd.put(screen, hd.text(name, "stencil", size, (255, 226, 170), glow=0.35), nx, S(14 + 194), "left" if side == "p1" else "right")
        # the power: one case per POW picked up / la puissance : une case par POW ramassé
        lv = self.v(vals, side, "weapon_level")
        lv = int(lv) if lv is not None else 0
        n = max(PIPS, lv)
        hd.put(screen, hd.text(tr("PUISSANCE", "POWER"), "bold", S(18), GREY, glow=0), self.X(side, 36), S(14 + 262),
               "left" if side == "p1" else "right", "middle")
        pw, gap = S(30), S(8)
        x = self.X(side, 150)
        fresh = max(0.0, 1 - (now - P.power_t) / 0.6)
        for i in range(n):
            j = i if side == "p1" else -i - 1
            r = pg.Rect(int(x + j * (pw + gap)), S(14 + 248), pw, S(28))
            lit = i < lv
            c = (255, 214, 90) if lit else (40, 42, 56)
            if lit and i == lv - 1 and fresh:
                c = (255, 255, 230)
            pg.draw.rect(screen, c, r, border_radius=S(4))
            if lit:
                pg.draw.rect(screen, (120, 80, 20), r, max(1, S(2)), border_radius=S(4))

    def draw_bottom(self, screen, side, vals, now):
        """The mega crashes, and the four weapons of the game with the one held lit. / Les méga crashs et les quatre armes."""
        hd, S = self.hd, self.S
        P = self.sides[side]
        y = S(14 + 370)
        b = self.v(vals, side, "bombs")
        if b is not None:
            hd.put(screen, hd.text(tr("MÉGA CRASH", "MEGA CRASH"), "bold", S(16), GREY, glow=0), self.X(side, 36), y - S(22),
                   "left" if side == "p1" else "right", "middle")
            fresh = max(0.0, 1 - (now - P.crash_t) / 0.5)
            for i in range(int(b)):
                self.draw_crash(screen, self.X(side, 52 + i * 52), y + S(14), 1 + 0.2 * fresh)
        code = self.v(vals, side, "weapon")
        held = int(code) if code is not None else 0
        pg = self.pg
        acc = ACCENT[side]
        for i in range(4):
            kind = KINDS[i]
            cw, ch = S(76), S(52)
            cx = self.X(side, 290 + i * 80, 76)
            r = pg.Rect(int(cx), int(y - ch / 2 + S(4)), cw, ch)
            on = i == held
            pg.draw.rect(screen, (40, 44, 60) if on else (16, 18, 28), r, border_radius=S(8))
            pg.draw.rect(screen, acc if on else (60, 64, 80), r, max(1, S(3 if on else 2)), border_radius=S(8))
            img = self.gun(kind, side, 72, 42)
            g = img if on else self.dim(img, (kind, side))
            screen.blit(g, (int(r.centerx - g.get_width() / 2), int(r.centery - g.get_height() / 2)))

    def dim(self, img, key):
        k = ("dim",) + key
        g = self.guns.get(k)
        if g is None:
            g = img.copy()
            g.fill((120, 120, 140, 150), special_flags=self.pg.BLEND_RGBA_MULT)
            self.guns[k] = g
        return g

    def draw_crash(self, screen, cx, cy, k=1.0):
        """A mega crash: a little round bomb with its fuse. / Une petite bombe ronde et sa mèche."""
        S, pg = self.S, self.pg
        r = int(S(15) * k)
        pg.draw.circle(screen, (30, 32, 40), (int(cx), int(cy)), r + S(2))
        pg.draw.circle(screen, (226, 70, 40), (int(cx), int(cy)), r)
        pg.draw.circle(screen, (255, 170, 120), (int(cx - r * 0.35), int(cy - r * 0.35)), max(2, r // 3))
        pg.draw.line(screen, (230, 200, 120), (int(cx + r * 0.5), int(cy - r * 0.8)), (int(cx + r), int(cy - r * 1.3)), max(2, S(3)))


SCENES = {"mercs": MercsScene}
