"""Shock Troopers 2nd Squad on the HD screen, laid out like Metal Slug and Mercs (1.39.2).

Each player's panel: the soldier chosen and the lives in reserve at the top, the energy under them, the score in the
middle of its band, the weapon held drawn on its card with its power as the game shows it (Lv and three P, one lit for
each P item picked up, a level for three of them), the grenades at the bottom. In the middle: the timer, and the life
bar of a big machine being shot at. The gun of the card fires when the player does, what he kills blows up in the
middle, a grenade flies from the panel.

Shock Troopers 2nd Squad, disposé comme Metal Slug et Mercs. Dans le panneau de chaque joueur : le soldat choisi et les
vies en réserve en haut, l'énergie dessous, le score au milieu de sa bande, l'arme tenue dessinée sur sa carte avec sa
puissance comme le jeu la montre (Lv et trois P, un allumé par bonus P ramassé, un niveau tous les trois), les grenades
en bas. Au milieu, le chrono, et la barre de vie d'un gros engin sur lequel on tire. L'arme de la carte tire quand le
joueur tire, ce qu'il abat explose au milieu, une grenade part du panneau."""
import math

from .hd_fx import Particle
from .hd_games import BTN_A, WHITE, GameScene, Machines, _clamp, _mix, _n
from .hd_mslug import ACCENT, CREAM, GOLD, GREY, PH, PW, RED, TIP, grenade_img, helmet_img, panel_img, weapon_img
from .i18n import tr

SOLDIERS = ("LEON", "ANGEL", "LULU", "TOY")     # in the order of the game's SOLDIER SELECT screen / dans l'ordre de l'écran
SHOT = {1: "FRONT", 2: "WIDE"}                  # the normal gun as the game names it, for the two soldiers seen with theirs
# the weapons of the game by its code: (name, the drawing of its card, the colour of its shots)
# les armes du jeu par leur code : le nom, le dessin de sa carte, la couleur de ses tirs
WEAPONS = {0: ("NORMAL", "mg", (255, 230, 150)), 4: ("FIRE", "flame", (255, 150, 60)), 8: ("ROUND", "shotgun", (120, 220, 255)),
           12: ("MISSILE", "rocket", (255, 190, 110)), 16: ("BOOMERANG", "laser", (170, 255, 140))}
FULL = 64               # a soldier's full energy / l'énergie pleine d'un soldat
P_STEP = 4              # what one P item adds to the game's power / ce qu'un bonus P ajoute à la puissance du jeu
P_TOP = 36              # the top of the power: Lv3 and its three P / le maximum : Lv3 et ses trois P
GREEN = (90, 230, 110)


def power_steps(p):
    """(level 1 to 3, P lit 0 to 3) of the game's power. A P item adds 4 and the game lights one more P; three of them are
    a level, 36 is the top (Lv3, three P). Lv1 with one and two P is read on a recorded game, the rest follows from the
    top. / (niveau 1 à 3, P allumés 0 à 3). Un bonus P ajoute 4 et le jeu allume un P de plus ; trois font un niveau, 36
    est le maximum. Lv1 avec un et deux P est lu sur une partie enregistrée, le reste découle du maximum."""
    n = max(0, int(p)) // P_STEP
    if n >= P_TOP // P_STEP:
        return 3, 3
    return 1 + n // 3, n % 3


def _fmt(n):
    return f"{int(n):,}".replace(",", " ")


class Side:
    """What the scene remembers of one player. / Ce que la scène retient d'un joueur."""

    def __init__(self):
        self.score_disp = None
        self.score_t = -99.0
        self.hit_t = -99.0
        self.down_t = -99.0
        self.weapon_t = -99.0
        self.power_t = -99.0
        self.level_t = -99.0
        self.name_t = -99.0
        self.recoil_t = -99.0
        self.grenade_t = -99.0
        self.energy = None          # the bar drawn, following the game's value / la barre dessinée
        self.who = None             # the soldier last seen / le dernier soldat vu
        self.fire_t = 0.0           # next shot of a held button / prochain tir d'un bouton tenu
        self.burst = [0.0, 0]       # autopilot: [next shot, shots left in the burst] / pilote automatique
        self.aim = None             # where the last shot landed / où le dernier tir est tombé


class SecondSquadScene(Machines, GameScene):
    THEME = "desert"
    SHADE = (60, 90)
    EXPLOSIONS = True
    TITLE = "Shock Troopers 2nd Squad"
    BANNERS = GameScene.BANNERS + (("LEVEL 2", GOLD), ("LEVEL 3", GOLD))
    BOSS_MIN = None                                            # the life of this game's bosses is not known yet
    BIG_MIN = 150                                              # an object that comes with that much life is a big machine
    MACHINE_HITS = 3                                           # its bar comes once it has been hit that many times
    MACHINE_BOX = (560, 64, 252)                               # width, height, top of the bar's box, between the panels

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        s, S = hd.s, self.S
        self.panels = {side: hd._surf(panel_img(side, s, ACCENT[side])) for side in ("p1", "p2")}
        self.sides = {"p1": Side(), "p2": Side()}
        self.guns = {}
        self.helmet = hd._surf(helmet_img(S(40)))
        self.helmet_off = self.helmet.copy()
        self.helmet_off.fill((70, 70, 90, 130), special_flags=self.pg.BLEND_RGBA_MULT)
        self.grenade = hd._surf(grenade_img(S(24), S(30)))
        self.fx.sp.register("grenade", grenade_img(S(34), S(42)))
        self.machines_reset()

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

    def continue_shown(self, side, vals, now):
        return False                                           # written in the panel, in place of the score / dans le panneau

    def weapon(self, vals, side):
        code = self.v(vals, side, "weapon")
        return WEAPONS.get(int(code) if code is not None else 0, WEAPONS[0])

    # ------------------------------------------------------------ what happens / ce qui se passe
    def restart(self, vals, now):
        for P in self.sides.values():
            P.score_disp = None
            P.burst = [now + 1.0, 0]
        self.machines_reset()

    def update(self, vals, now):
        fx, S = self.fx, self.S
        anyone = False
        for side in ("p1", "p2"):
            P = self.sides[side]
            suf = "" if side == "p1" else "_p2"
            if vals.get(side + "_mode") != 1:                           # not in the game, or at the CONTINUE countdown
                continue
            anyone = True
            who = self.v(vals, side, "soldier")
            who = int(who) if who is not None and 0 <= who < len(SOLDIERS) else P.who
            if who is not None and who != P.who:
                P.name_t = now
            P.who = who
            # the gun: the player's button, or bursts while his stick is not read / l'arme : le bouton du joueur
            st = self.stick(vals, side)
            if st is not None:
                if st[2] & BTN_A and now >= P.fire_t:
                    P.fire_t = now + 0.1
                    self.shoot(side, vals, now)
            elif now >= P.burst[0]:
                if P.burst[1] <= 0:
                    P.burst[1] = self.rng.randint(4, 8)
                self.shoot(side, vals, now)
                P.burst[1] -= 1
                P.burst[0] = now + (0.1 if P.burst[1] > 0 else self.rng.uniform(1.2, 2.8))
            ch = self.changed(vals, "score" + suf)
            if ch and ch[1] > ch[0]:
                self.kill(side, ch[1] - ch[0], vals, now)
            ch = self.changed(vals, "grenades" + suf)
            lost = self.changed(vals, "lives" + suf)
            lost = bool(lost and lost[1] < lost[0])
            if ch and ch[1] < ch[0] and ch[0] - ch[1] <= 3:
                self.throw(side, now)
            if lost:                                                   # a life lost: the soldier is down
                P.down_t = P.hit_t = now
                x = self.x0(side) + S(PW) / 2
                fx.shake(10, 0.5)
                fx.flash((170, 0, 0), 0.25, 0.5)
                fx.explosion(x, S(240), 0.7, False)
                self.popup(tr("À TERRE !", "DOWN!"), x, S(250), RED, 50, life=1.5, key="stencil")
                continue                                               # what comes back with the next life is no pick-up
            ch = self.changed(vals, "energy" + suf)
            if ch and ch[1] < ch[0]:
                P.hit_t = now
                fx.shake(4 + min(10, (ch[0] - ch[1]) * 0.3), 0.3)
            ch = self.changed(vals, "weapon" + suf)
            if ch:
                P.weapon_t = now
                sx, sy = self.slot(side)
                if ch[1]:                                              # a weapon picked up / une arme ramassée
                    fx.glow(sx + S(95), sy + S(54), 30, 170, GOLD, 0.45, "front", 0.9, 0.0, hot=0.6)
                    fx.sparks(sx + S(95), sy + S(54), 30, GOLD, (200, 700), (0, 360), (0.3, 0.8), 400, "front", 3, 24)
                    self.popup(self.weapon(vals, side)[0] + " !", sx + S(95), S(14 + 300), GOLD, 30, 1.3, 50)
            ch = self.changed(vals, "power" + suf)
            if ch and ch[1] > ch[0]:
                self.power_up(side, ch[0], ch[1], now)
            elif ch and ch[1] < ch[0]:
                P.power_t = now
        self.machines(vals, now, anyone)

    def target(self, side):
        """Where a shot lands: on the machine whose bar is shown, else in the middle, on the player's side of the timer.
        / Où tombe un tir : sur l'engin dont la barre est montrée, sinon au milieu, du côté du joueur."""
        rng, S = self.rng, self.S
        if self.machine_on():
            cx, cy = self.machine_at()
            return cx + rng.uniform(-S(220), S(220)), cy + rng.uniform(-S(20), S(20))
        d0 = rng.uniform(130, 270) * self.s
        return (self.W / 2 - d0 if side == "p1" else self.W / 2 + d0), S(rng.uniform(260, 380))

    def shoot(self, side, vals, now):
        """The gun of the card fires, the way the soldier's does. / L'arme de la carte tire, à la façon du soldat."""
        fx, S = self.fx, self.S
        P = self.sides[side]
        name, kind, col = self.weapon(vals, side)
        x, y = self.tip(side, kind)
        tx, ty = P.aim = self.target(side)
        d = 1 if side == "p1" else -1
        P.recoil_t = now
        fx.muzzle(x, y, d, 0.8, col)
        if kind == "flame":
            for i in range(4):
                k = (i + 1) / 4
                fx.glow(x + (tx - x) * k * 0.5, y + (ty - y) * k * 0.5, 16, 40 + 30 * k, (255, 140 - 40 * k, 50), 0.3, "front", 0.9, 0.0,
                        delay=i * 0.03, hot=0.5)
        elif kind == "rocket":
            fx.tracer(x, y, tx, ty, 1600, col, 7, 70, impact=False)
            fx.later(abs(tx - x) / (1600 * self.s), fx.small_blast, tx, ty, 0.8, "back")
        elif name == "NORMAL" and SHOT.get(P.who) == "WIDE":           # three shots that open / trois tirs qui s'ouvrent
            for a in (-60, 0, 60):
                fx.tracer(x, y, tx, ty + S(a), 2800, col, 4, 120)
        elif name == "NORMAL" and SHOT.get(P.who) == "FRONT":          # two shots side by side / deux tirs côte à côte
            for a in (-9, 9):
                fx.tracer(x, y + S(a), tx, ty + S(a), 3000, col, 4, 140)
        else:
            fx.tracer(x, y, tx, ty, 3000, col, 5, 130)

    def kill(self, side, gain, vals, now):
        """Points scored: what was shot at blows up, as big as the points. / Des points : la cible explose."""
        fx, S = self.fx, self.S
        P = self.sides[side]
        P.score_t = now
        tx, ty = P.aim or self.target(side)
        if self.machine_on():                                          # the machine has its own end / l'engin a sa propre fin
            fx.small_blast(tx, ty, 1.2, "front")
        elif gain >= 300:
            fx.explosion(tx, ty, min(1.1, 0.55 + gain / 2500), True)
        else:
            fx.small_blast(tx, ty, 1.6, "front")
            fx.glow(tx, ty, 20, 120, (255, 200, 120), 0.3, "front", 0.9, 0.0)
            fx.shake(3, 0.15)
        if gain >= 100:
            fx.text(f"+{_fmt(gain)}", tx, ty - S(50), GOLD, 30 if gain < 1000 else 42, life=0.9, rise=70)

    def throw(self, side, now):
        """A grenade flies from the panel and blows up in the middle. / Une grenade part du panneau et explose au milieu."""
        fx, S = self.fx, self.S
        self.sides[side].grenade_t = now
        x = self.X(side, PW - 40)
        tx, ty = self.target(side)
        fx.projectile("grenade", x, S(14 + 370), tx, ty, 0.7, 170, self._grenade_boom)

    def _grenade_boom(self, x, y):
        self.fx.explosion(x, y, 1.0, True)
        self.fx.shake(9, 0.4)

    def power_up(self, side, old, new, now):
        """A P picked up: one more P lit; the third is the next level. / Un P ramassé : un P de plus ; le troisième est
        le niveau suivant."""
        fx, S = self.fx, self.S
        P = self.sides[side]
        P.power_t = now
        lv, lit = power_steps(new)
        sx, sy = self.slot(side)
        fx.glow(sx + S(95), sy + S(54), 30, 200, (255, 236, 160), 0.5, "front", 1.0, 0.0, hot=0.8)
        r = fx.add(Particle("ring", sx + S(95), sy + S(54), now, 0.5, "front"))
        r.r0, r.r1, r.col, r.a0, r.a1, r.data = 20 * self.s, 160 * self.s, GOLD, 0.9, 0.0, 6 * self.s
        if lv > power_steps(old)[0]:
            P.level_t = now
            fx.flash((255, 240, 200), 0.2, 0.3)
            fx.sparks(sx + S(95), sy + S(54), 40, (255, 230, 140), (300, 1000), (0, 360), (0.4, 0.9), 300, "front", 3, 26)
            self.slam(f"LEVEL {lv}", GOLD, now, 1.5, sub=tr("L'ARME MONTE D'UN NIVEAU", "THE WEAPON GOES UP A LEVEL"))
        else:
            self.popup("POWER UP", sx + S(95), S(14 + 300), (255, 110, 90), 32, 1.2, 50)
        self.hd.log(tr(f"{self.TITLE} : puissance {int(old)} -> {int(new)}, affichée LV {lv} et {lit} P",
                       f"{self.TITLE}: power {int(old)} -> {int(new)}, shown LV {lv} and {lit} P"))

    # ------------------------------------------------------------ the drawing / le dessin
    def draw_hud(self, screen, eng, vals, logo, now):
        self.draw_center(screen, vals, logo, now)
        for side in ("p1", "p2"):
            self.draw_panel(screen, side, vals, now)
        self.draw_machine(screen, now)

    def draw_center(self, screen, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        cx = W / 2
        hd.draw_logo(screen, logo, cx, S(8), S(560), S(124), now)
        tm = _n(vals.get("time"))
        if tm is not None:
            low = tm <= 10
            blink = low and int(now * 4) % 2 == 0
            bw, bh = S(170), S(84)
            y = S(152)
            self.box(screen, cx - bw / 2, y, bw, bh, (255, 120, 100) if blink else (255, 240, 220), fill=(8, 10, 22, 210), radius=14, width=3)
            hd.put(screen, hd.text(tr("TEMPS", "TIME"), "bold", S(18), CREAM, glow=0), cx, y + S(14), "center", "middle")
            hd.put_number(screen, str(int(tm)), "stencil", S(50), RED if low else GOLD, cx, y + S(52), "center", "middle")

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
        al = "left" if side == "p1" else "right"
        if not self.playing(vals, side):
            credits = _n(vals.get("credits"))
            word = tr("APPUIE SUR START", "PRESS START") if credits is None or credits > 0 else "INSERT COIN"
            col = acc if credits is None or credits > 0 else GOLD
            hd.put(screen, hd.text(word, "stencil", S(46), col, glow=0.5), x0 + S(PW) / 2, S(230), "center", "middle",
                   scale=1 + 0.04 * hd._pulse(now))
            if credits is None or credits > 0:
                hd.put(screen, hd.text(tr("POUR REJOINDRE LA PARTIE", "TO JOIN THE GAME"), "bold", S(22), GREY, glow=0), x0 + S(PW) / 2,
                       S(290), "center", "middle")
            return
        # the header: the soldier, the lives in reserve / l'en-tête : le soldat, les vies en réserve
        if P.who is not None:
            pop = max(0.0, 1 - (now - P.name_t) / 0.35)
            hd.put(screen, hd.text(SOLDIERS[P.who], "stencil", S(38), _mix(acc, WHITE, 0.15 + 0.85 * pop), glow=0.35), self.X(side, 120),
                   chip.centery, al, "middle", scale=1 + 0.15 * pop)
        lives = self.v(vals, side, "lives")
        if lives is not None:
            n = int(max(0, lives))
            for i in range(max(3, min(n, 5))):
                img = self.helmet if i < n else self.helmet_off
                screen.blit(img, (int(self.X(side, PW - 30 - (i + 1) * 46, 40)), int(y0 + S(14))))
            if n > 5:
                hd.put(screen, hd.text(f"×{n}", "xbold", S(28), CREAM, glow=0), self.X(side, PW - 30 - 5 * 46 - 12), chip.centery,
                       "right" if side == "p1" else "left", "middle")
        self.draw_energy(screen, side, vals, now, y0)
        # the score in the middle of its band, or the countdown of the game / le score, ou le décompte du jeu
        if vals.get(side + "_mode") == 2:
            k = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(now * 6))
            hd.put(screen, hd.text("CONTINUE ?", "stencil", S(62), GOLD, glow=0.5), x0 + S(PW) / 2, y0 + S(146), "center", "middle", alpha=k)
        else:
            score = self.v(vals, side, "score")
            if score is not None:
                if P.score_disp is None or score < P.score_disp:
                    P.score_disp = score
                else:
                    gap = score - P.score_disp
                    P.score_disp = min(score, P.score_disp + max(1, int(gap * 0.18) + 1)) if gap else score
                pop = max(0.0, 1 - (now - P.score_t) / 0.22)
                hd.put_number(screen, _fmt(P.score_disp), "stencil", S(70), GOLD, x0 + S(PW) / 2, y0 + S(146), "center", "middle",
                              scale=1 + 0.12 * pop)
        self.draw_weapon(screen, side, vals, now)
        self.draw_bottom(screen, side, vals, now)
        if hit:
            red = pg.Surface((S(PW), S(PH))).convert()
            red.fill((int(110 * hit), 0, 0))
            screen.blit(red, (x0, y0), special_flags=pg.BLEND_RGB_ADD)

    def draw_energy(self, screen, side, vals, now, y0):
        hd, S, pg = self.hd, self.S, self.pg
        P = self.sides[side]
        e = self.v(vals, side, "energy")
        if e is None:
            return
        f = 0.0 if e >= 128 else _clamp(e / float(self.tops.get("energy") or FULL))
        P.energy = f if P.energy is None else P.energy + (f - P.energy) * 0.2
        bw, bh = S(PW - 56), S(26)
        bx, by = self.X(side, 28, PW - 56), y0 + S(80)
        low = f < 0.25
        pg.draw.rect(screen, (40, 14, 18), (bx, by, bw, bh), border_radius=S(8))
        w = int((bw - S(6)) * P.energy)
        if w > 0:
            col = (255, 70, 50) if low and int(now * 5) % 2 == 0 else ((255, 190, 60) if f < 0.5 else GREEN)
            x = bx + S(3) if side == "p1" else bx + bw - S(3) - w
            pg.draw.rect(screen, col, (x, by + S(3), w, bh - S(6)), border_radius=S(6))
        pg.draw.rect(screen, (255, 255, 255), (bx, by, bw, bh), max(1, S(2)), border_radius=S(8))
        lab = hd.text(tr("ÉNERGIE", "ENERGY"), "xbold", S(15), (20, 20, 26) if w > S(120) else CREAM, glow=0)
        hd.put(screen, lab, bx + S(14) if side == "p1" else bx + bw - S(14), by + bh / 2, "left" if side == "p1" else "right", "middle")

    def draw_weapon(self, screen, side, vals, now):
        hd, S, pg = self.hd, self.S, self.pg
        P = self.sides[side]
        al = "left" if side == "p1" else "right"
        name, kind, _col = self.weapon(vals, side)
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
        shot = SHOT.get(P.who) if name == "NORMAL" else None           # NORMAL WIDE, NORMAL FRONT, as in the game's box
        ammo = self.v(vals, side, "ammo")
        if name != "NORMAL" and ammo is not None:                      # what is left of a weapon picked up, beside its name
            shot = f"× {int(ammo)}"
        t = hd.text(name, "stencil", S(40), (255, 226, 170), glow=0.35)
        if shot and side == "p2":                                      # read NORMAL WIDE on both sides / dans le même ordre
            sw = hd.put(screen, hd.text(shot, "xbold", S(26), CREAM, glow=0), nx, S(14 + 200), "right") + S(12)
            hd.put(screen, t, nx - sw, S(14 + 194), "right")
        else:
            nw = hd.put(screen, t, nx, S(14 + 194), al)
            if shot:
                hd.put(screen, hd.text(shot, "xbold", S(26), CREAM, glow=0), nx + nw + S(12), S(14 + 200), "left")
        # the power as on the game's screen: Lv and its three P / la puissance comme à l'écran du jeu : Lv et ses trois P
        p = self.v(vals, side, "power")
        if p is None:
            return
        lv, lit = power_steps(p)
        fresh = max(0.0, 1 - (now - P.power_t) / 0.6)
        up = max(0.0, 1 - (now - P.level_t) / 1.2)
        y = S(14 + 282)
        lw = hd.put(screen, hd.text(f"LV {lv}", "stencil", S(34), _mix((255, 214, 90), WHITE, up), glow=0.3 + 0.5 * up), self.X(side, 36), y,
                    al, "middle", scale=1 + 0.3 * up)
        cw, gap = S(56), S(8)
        for i in range(3):
            j = i if side == "p1" else -i - 1
            x = self.X(side, 36) + (lw + S(18) if side == "p1" else -lw - S(18)) + j * (cw + gap)
            r = pg.Rect(int(x), int(y - S(18)), cw, S(36))
            on = i < lit
            c = (226, 44, 40) if on else (40, 42, 56)
            if on and i == lit - 1 and fresh:
                c = _mix(c, (255, 255, 230), fresh)
            pg.draw.rect(screen, c, r, border_radius=S(8))
            pg.draw.rect(screen, (250, 244, 236) if on else (86, 88, 104), r, max(2, S(3)), border_radius=S(8))
            hd.put(screen, hd.text("P", "black", S(26), WHITE if on else (104, 106, 122), glow=0), r.centerx, r.centery, "center", "middle")
        if lv == 3 and lit == 3:
            x = self.X(side, 36) + (1 if side == "p1" else -1) * (lw + S(18) + 3 * (cw + gap) + S(4))
            hd.put(screen, hd.text("MAX", "black", S(22), _mix(GOLD, WHITE, 0.3 + 0.3 * math.sin(now * 8)), glow=0.3), x, y, al, "middle")

    def draw_bottom(self, screen, side, vals, now):
        """The grenades. / Les grenades."""
        hd, S = self.hd, self.S
        P = self.sides[side]
        al = "left" if side == "p1" else "right"
        g = self.v(vals, side, "grenades")
        if g is None:
            return
        y = S(14 + 370)
        hd.put(screen, hd.text("GRENADES", "bold", S(16), GREY, glow=0), self.X(side, 36), y - S(22), al, "middle")
        n = int(max(0, g))
        fresh = max(0.0, 1 - (now - P.grenade_t) / 0.4)
        step = S(30)
        for i in range(min(n, 12)):
            x = self.X(side, 36 + i * 30, 24)
            screen.blit(self.grenade, (int(x), int(y - S(4) - (S(6) * fresh if i == n - 1 else 0))))
        col = _mix(CREAM, WHITE, fresh) if n else RED
        hd.put(screen, hd.text(f"×{n}", "xbold", S(30), col, glow=0.2), self.X(side, 36) + (1 if side == "p1" else -1) * (min(n, 12) * step + S(10)),
               y + S(12), al, "middle")


SCENES = {"shocktr2": SecondSquadScene}
