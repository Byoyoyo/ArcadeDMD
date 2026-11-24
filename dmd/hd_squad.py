"""Shock Troopers 2nd Squad on the HD screen, laid out like Metal Slug and Mercs (1.39.2).

Each player's panel: the soldier chosen and the lives in reserve at the top, the energy under them, the score in the
middle of its band, the weapon held drawn on its card with its power as the game shows it (Lv and three P, one lit for
each P item picked up, a level for three of them), the grenades at the bottom. In the middle: the timer, and the life
bar of a big machine being shot at. The gun of the card fires when the player does, what he kills blows up in the
middle, a grenade flies from the panel.

The mission played is named beside the timer and announced as it starts, STAGE CLEAR when the game counts its bonuses.
The boss comes when the game says so: ALERT as on its screen, with the name of the mission's boss, then a box under the
timer where each part of the boss being shot at has its own bar, PHASE 2 when the next ones come, and BOSS DESTROYED at
the image the game stops its timer again. A player in a vehicle has it on his card, CHARGE as the game's box reads.

Shock Troopers 2nd Squad, disposé comme Metal Slug et Mercs. Dans le panneau de chaque joueur : le soldat choisi et les
vies en réserve en haut, l'énergie dessous, le score au milieu de sa bande, l'arme tenue dessinée sur sa carte avec sa
puissance comme le jeu la montre (Lv et trois P, un allumé par bonus P ramassé, un niveau tous les trois), les grenades
en bas. Au milieu, le chrono, et la barre de vie d'un gros engin sur lequel on tire. L'arme de la carte tire quand le
joueur tire, ce qu'il abat explose au milieu, une grenade part du panneau.

La mission jouée est nommée à côté du chrono et annoncée à son départ, STAGE CLEAR quand le jeu compte ses bonus. Le
boss arrive quand le jeu le dit : ALERT comme à son écran, avec le nom du boss de la mission, puis une boîte sous le
chrono où chaque pièce du boss sur laquelle on tire a sa barre, PHASE 2 quand les suivantes arrivent, et BOSS DÉTRUIT
à l'image où le jeu arrête de nouveau son chrono. Un joueur monté dans un véhicule l'a sur sa carte, CHARGE comme
l'écrit la boîte du jeu."""
import math

from .hd_fx import Particle
from .hd_games import BTN_A, WHITE, GameScene, Machines, _clamp, _mix, _n
from .hd_mslug import ACCENT, CREAM, GOLD, GREY, PH, PW, RED, TIP, chip_at, chip_img, grenade_img, helmet_img, panel_img, tank_img, weapon_img
from .i18n import tr

SOLDIERS = ("LEON", "ANGEL", "LULU", "TOY")     # in the order of the game's SOLDIER SELECT screen / dans l'ordre de l'écran
SHOT = {1: "FRONT", 2: "WIDE"}                  # the normal gun as the game names it, for the two soldiers seen with theirs
# the weapons of the game by its code: (name, the drawing of its card, the colour of its shots)
# les armes du jeu par leur code : le nom, le dessin de sa carte, la couleur de ses tirs
WEAPONS = {0: ("NORMAL", "mg", (255, 230, 150)), 4: ("FIRE", "flame", (255, 150, 60)), 8: ("ROUND", "shotgun", (120, 220, 255)),
           12: ("MISSILE", "rocket", (255, 190, 110)), 16: ("BOOMERANG", "laser", (170, 255, 140))}
BONUS_FOR = 2.6         # seconds the BONUS counter stays after its last point / secondes où le compteur BONUS reste
FULL = 64               # a soldier's full energy / l'énergie pleine d'un soldat
P_STEP = 4              # what one P item adds to the game's power / ce qu'un bonus P ajoute à la puissance du jeu
P_TOP = 36              # the top of the power: Lv3 and its three P / le maximum : Lv3 et ses trois P
GREEN = (90, 230, 110)
RIDE = ("CHARGE", "tank", (255, 214, 120))      # a player in a vehicle: what the game's box reads, the card, the shells
# The missions as the game's map names them, by (the mission counted from 1, the route taken after the first: "A" by
# Austin then Debon, "B" by Sommers then Brozna, None where both routes are the same one).
# Les missions comme la carte du jeu les nomme, par (la mission comptée à partir de 1, la route prise après la première :
# « A » par Austin puis Debon, « B » par Sommers puis Brozna, None quand les deux routes n'en font qu'une).
MISSIONS = {(1, None): "GOLDOMA CITY", (2, "A"): "AUSTIN AIR BASE", (2, "B"): "SOMMERS NAVAL BASE", (3, "A"): "DEBON RAIL LINES",
            (3, "B"): "BROZNA WARZONE", (4, None): "DIC BARRACKS", (5, None): "DIC HEADQUARTERS"}
# The bosses. The game itself only writes ALERT: these names are the ones of a reference page (Arcade Quartermaster,
# "Shock Troopers 2nd Squad, stages & bosses"), which gives none for the last two missions. The truck of mission 1 is
# the only one seen in a recorded game.
# Les boss. Le jeu n'écrit que ALERT : ces noms sont ceux d'une page de référence, qui n'en donne pas pour les deux
# dernières missions. Le camion de la mission 1 est le seul vu dans une partie enregistrée.
BOSSES = {(1, None): "ARMORED BATTLE TRUCK", (2, "A"): "STEALTH BOMBER", (2, "B"): "WATERCRAFT WAR MACHINE",
          (3, "A"): "3-SECTION WEAPONS LOCOMOTIVE", (3, "B"): "QUADRA-BATTLE TECH"}
AUSTIN = 4              # "_mission" on the route of Austin Air Base / « _mission » sur la route d'Austin Air Base
AUSTIN_AREAS = (7, 8)   # and the first parts of that mission ("_area") / et les premières zones de cette mission
PART_MIN = 100          # the least energy a part of a boss comes with / la plus petite énergie d'une pièce de boss
PART_SHOWN = 0.08       # a part gets its bar once it has lost that share of it / sa barre vient quand elle en a perdu ça
ALERT_FOR = 2.6         # how long ALERT stays across the screen / le temps qu'ALERT reste en travers de l'écran
BOSS_BOX = (588, 122, 244)                      # width, height, top of the boss's box / la boîte du boss


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
        self.ride = False           # in a vehicle / dans un véhicule
        self.zero_t = -99.0         # when his energy was last at zero / la dernière fois que son énergie était à zéro
        self.bonus = 0              # the points the game counts at STAGE CLEAR / les points comptés à STAGE CLEAR
        self.bonus_t = -99.0
        self.bonus_shown = (0, -99.0)


class SecondSquadScene(Machines, GameScene):
    THEME = "desert"
    SHADE = (60, 90)
    EXPLOSIONS = True
    TITLE = "Shock Troopers 2nd Squad"
    BANNERS = GameScene.BANNERS + (("LEVEL 2", GOLD), ("LEVEL 3", GOLD), ("ALERT", RED), ("STAGE CLEAR", GOLD), ("MISSION 1", GOLD))
    BOSS_MIN = None                                            # the boss is not an object with a big life here: the game says
    BIG_MIN = 150                                              # an object that comes with that much life is a big machine
    MACHINE_HITS = 3                                           # its bar comes once it has been hit that many times
    MACHINE_BOX = (560, 64, 252)                               # width, height, top of the bar's box, between the panels

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        s, S = hd.s, self.S
        self.panels = {side: hd._surf(panel_img(side, s, ACCENT[side])) for side in ("p1", "p2")}
        self.chips = {side: hd._surf(chip_img(side, s, ACCENT[side])) for side in ("p1", "p2")}
        self.sides = {"p1": Side(), "p2": Side()}
        self.guns = {}
        self.helmet = hd._surf(helmet_img(S(40)))
        self.helmet_off = self.helmet.copy()
        self.helmet_off.fill((70, 70, 90, 130), special_flags=self.pg.BLEND_RGBA_MULT)
        self.grenade = hd._surf(grenade_img(S(24), S(30)))
        self.fx.sp.register("grenade", grenade_img(S(34), S(42)))
        self.machines_reset()
        self.squad_reset()

    def squad_reset(self):
        self.fight = None           # the boss being fought / le boss qu'on combat
        self.boss_over = False      # the boss of this alarm is done with / le boss de cette alerte est réglé
        self.alerts = {}            # the alarms heard in each mission / les alertes entendues dans chaque mission
        self.route = None           # "A" or "B" once the second mission tells / la route, une fois la deuxième mission lue
        self.pending = None         # (mission, until) to announce once its name is known / à annoncer quand son nom est su
        self.lost_t = -99.0         # when a life was last lost / la dernière vie perdue
        self.after = None           # the objects' energies once the boss is down / les énergies une fois le boss tombé

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
            img = tank_img(self.S(w), self.S(h)) if kind == "tank" else weapon_img(kind, self.S(w), self.S(h))
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
        if self.v(vals, side, "_ride"):                        # in a vehicle: its gun, CHARGE in the game's box
            return RIDE
        code = self.v(vals, side, "weapon")
        return WEAPONS.get(int(code) if code is not None else 0, WEAPONS[0])

    # ------------------------------------------------------------ the mission / la mission
    def mission(self, vals):
        """(the mission from 1, its name or None, the name of its boss or None). The route is read at the second
        mission: Sommers when the game's number is not Austin's, Austin when it is and the mission starts by Austin's
        own parts; a third mission is named by the route kept from the second. Nothing is named without that.
        / (la mission à partir de 1, son nom ou None, le nom de son boss ou None). La route se lit à la deuxième mission :
        Sommers quand le numéro du jeu n'est pas celui d'Austin, Austin quand il l'est et que la mission commence par
        les zones d'Austin ; la troisième est nommée par la route gardée de la deuxième. Sans ça, rien n'est nommé."""
        st = _n(vals.get("_stage"))
        if st is None or not 1 <= st <= 9:
            return None
        st = int(st)
        if st == 1:                                                    # a game starts again by the first mission
            self.route = None
        if st == 2 and self.route is None:
            m = _n(vals.get("_mission"))
            if m is not None and m < 128:
                if m != AUSTIN:
                    self.route = "B"
                elif _n(vals.get("_area")) in AUSTIN_AREAS:
                    self.route = "A"
        key = (st, self.route if st in (2, 3) else None)
        return st, MISSIONS.get(key), BOSSES.get(key)

    def missions(self, vals, now):
        """MISSION n and its name as it starts, STAGE CLEAR when the game counts its bonuses. / MISSION n et son nom à
        son départ, STAGE CLEAR quand le jeu compte ses bonus."""
        m = self.mission(vals)
        st = self.changed(vals, "_stage")
        cl = self.changed(vals, "_clear")
        if st and m:                                                   # another mission: its alarms are still to come
            self.alerts.pop(m[0], None)
        if cl and cl[1] and not cl[0]:                                 # the bonuses of the mission just won
            self.slam("STAGE CLEAR", GOLD, now, 2.0, sub=m[1] if m else None)
            self.fx.flash((255, 240, 200), 0.2, 0.4)
            self.pending = None
        elif m and ((st and st[1] > st[0] and not vals.get("_clear")) or (cl and cl[0] and not cl[1])):
            self.pending = (m[0], now + 0.8)                           # the first mission starts, or the map is left
        if self.pending and m and (m[1] or now >= self.pending[1]):    # its name may come an image or two later
            if m[0] == self.pending[0]:
                self.slam(f"MISSION {m[0]}", GOLD, now, 2.0, sub=m[1])
                self.hd.log(tr(f"{self.TITLE} : mission {m[0]}" + (f", {m[1]}" if m[1] else ", pas encore nommée"),
                               f"{self.TITLE}: mission {m[0]}" + (f", {m[1]}" if m[1] else ", not named yet")))
            self.pending = None

    # ------------------------------------------------------------ what happens / ce qui se passe
    def restart(self, vals, now):
        for side, P in self.sides.items():
            P.score_disp = None
            P.burst = [now + 1.0, 0]
            P.ride = bool(self.v(vals, side, "_ride"))
        self.machines_reset()
        self.squad_reset()
        self.boss_over = bool(vals.get("_boss")) and bool(vals.get("_clear"))   # started on the bonuses of a boss already down

    def update(self, vals, now):
        fx, S = self.fx, self.S
        anyone = False
        counting = bool(_n(vals.get("_clear")))                         # STAGE CLEAR and the map: the game counts its bonuses
        ch = self.changed(vals, "_clear")
        if ch and ch[1] and not ch[0]:                                  # a count starts / un décompte commence
            for P in self.sides.values():
                P.bonus = 0
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
            ride = bool(self.v(vals, side, "_ride"))                    # into a vehicle or out of it, as the game writes it
            if ride != P.ride:
                P.ride = ride
                P.weapon_t = now
                sx, sy = self.slot(side)
                if ride:
                    fx.glow(sx + S(95), sy + S(54), 30, 190, GREEN, 0.5, "front", 0.9, 0.0, hot=0.6)
                self.popup("ROLLING IN!" if ride else "ROLLING OUT", sx + S(95), S(14 + 300), GREEN if ride else (255, 110, 90), 32, 1.4,
                           50)
            e = self.v(vals, side, "energy")
            if e is not None and e <= 0:
                P.zero_t = now
            if counting:                                               # points counted, not scored: one BONUS counter,
                ch = self.changed(vals, "score" + suf)                 # nothing is shot at and nothing blows up
                if ch and ch[1] > ch[0]:
                    P.score_t = P.bonus_t = now
                    P.bonus += ch[1] - ch[0]
                continue
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
                P.down_t = P.hit_t = self.lost_t = now
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
            elif ch and ch[1] < ch[0]:                                 # a hit puts one P out / un coup reçu éteint un P
                P.power_t = now
        if anyone:
            self.missions(vals, now)
        self.boss_watch(vals, now, anyone)
        if self.fight is None:
            self.machines(vals, now, anyone)
        else:                                                          # the boss has the box / le boss a la boîte
            self.hps, self.boss = None, None

    # ------------------------------------------------------------ the boss / le boss
    def boss_watch(self, vals, now, playing):
        """The boss of the mission, from the game's own alarm ("_boss", ALERT on its screen) to the image it stops its
        timer again with no life lost ("_wait"). Its parts are the objects that come with PART_MIN of energy or more
        while the alarm is on: each gets a bar once it has lost PART_SHOWN of its energy, so that a part nobody can hurt
        never gets one, and the bars start again when new parts come after the ones shown are all down (the next phase).
        / Le boss de la mission, de l'alerte du jeu (« _boss », ALERT à son écran) à l'image où il arrête de nouveau son
        chrono sans vie perdue (« _wait »). Ses pièces sont les objets qui arrivent avec PART_MIN d'énergie ou plus
        pendant l'alerte : chacune a sa barre quand elle a perdu PART_SHOWN de son énergie, une pièce intouchable n'en a
        donc jamais, et les barres repartent quand de nouvelles pièces arrivent après la chute de toutes celles montrées."""
        fx = self.fx
        hps = vals.get("_hps")
        flag = bool(_n(vals.get("_boss")))
        F = self.fight
        if not playing or not flag or not isinstance(hps, (list, tuple)):
            if not flag:
                self.boss_over = False
            if F is not None and (not playing or F["down"] is None or now - F["down"] > 2.6):
                self.fight = None
            return
        wait = bool(_n(vals.get("_wait")))
        cur = [v if isinstance(v, int) and 0 < v < 0x8000 else 0 for v in hps]
        part_min = _n(self.hd_opts.get("part_min")) or PART_MIN
        before = None
        if F is not None and F["down"] is not None and now - F["down"] > 2.6:
            F = self.fight = None                                      # BOSS DESTROYED has been said
        if self.boss_over:
            # down, as far as the timer told. If parts come again under the same alarm, it was only a pause of the game:
            # the fight goes on / tombé, d'après le chrono. Si des pièces reviennent sous la même alerte, ce n'était
            # qu'une pause du jeu : le combat reprend
            before, self.after = self.after, cur
            if (before is None or len(before) != len(cur) or vals.get("_clear")
                    or not any(part_min <= v <= 5000 and v > before[i] + 4 for i, v in enumerate(cur))):
                return
            self.boss_over = False
            F = self.fight = None
            self.hd.log(tr(f"{self.TITLE} : boss, des pièces reviennent, le combat reprend",
                           f"{self.TITLE}: boss, parts come again, the fight goes on"))
        if F is None:
            heard = self.changed(vals, "_boss")
            heard = bool(heard and heard[1] and not heard[0])           # the alarm starts now: ALERT is on the game's screen
            m = self.mission(vals)
            n = m[0] if m else None
            first = heard and not self.alerts.get(n)
            self.alerts[n] = self.alerts.get(n, 0) + 1
            F = self.fight = {"t0": now, "name": m[2] if m and (first or not heard) else None, "mission": n, "heard": heard,
                              "engaged": None if wait and heard else now, "parts": {}, "row": [], "wave": 0, "down": None,
                              "hit": -99.0, "maybe": None, "batch": 0, "batch_t": -99.0,
                              "prev": cur if heard else (before or [0] * len(cur))}   # what was there before the alarm is no part
            self.hps, self.boss = None, None
            if heard:
                self.slam("ALERT", RED, now, ALERT_FOR, sub=F["name"] or tr("LE BOSS DE LA MISSION ARRIVE", "THE MISSION'S BOSS IS COMING"))
                fx.flash((170, 0, 0), 0.22, 0.6)
                fx.shake(8, 0.5)
            self.hd.log(tr(f"{self.TITLE} : ALERT, boss de la mission {n or '?'}" + (f", {F['name']}" if F["name"] else ""),
                           f"{self.TITLE}: ALERT, boss of mission {n or '?'}" + (f", {F['name']}" if F["name"] else "")))
        if F["engaged"] is None and not wait:
            F["engaged"] = now                                         # PLEASE WAIT is gone: the fight is on
        prev, F["prev"] = F["prev"], cur
        parts = F["parts"]
        if len(prev) == len(cur):
            for i, v in enumerate(cur):
                p = parts.get(i)
                if p is not None and p["dead"] is None:
                    if v >= part_min and v > p["hp"] + 4:              # filled again: the same object, its next phase
                        if p["shown"]:                                 # the bar it had is done with / sa barre a fini
                            p["dead"], p["hp"] = now, 0
                        p = None
                    elif v > p["hp"] + 4:                              # a small object took its place: it was down or left
                        if p["shown"] and p["hp"] <= 0.25 * p["max"]:
                            p["dead"], p["hp"] = now, 0
                        else:
                            del parts[i]
                            if p in F["row"]:
                                F["row"].remove(p)
                        continue
                    elif v < p["hp"]:
                        gone = v <= 0 and p["hp"] - v > 0.5 * p["max"]   # it left, nobody destroyed it
                        if gone and not p["shown"]:
                            del parts[i]
                            continue
                        p["hp"], p["hit"] = v, now
                        F["hit"] = now
                        if not p["shown"] and (v <= 0 or p["max"] - v >= PART_SHOWN * p["max"]):
                            self._part_shown(F, p, now)
                        if v <= 0:
                            p["dead"] = now
                            bx, by = self._part_at(F, p)
                            fx.explosion(bx, by, 0.7, False)
                            fx.shake(6, 0.3)
                            self.hd.log(tr(f"{self.TITLE} : boss, pièce détruite (vie de départ {p['max']})",
                                           f"{self.TITLE}: boss, part destroyed (life at first {p['max']})"))
                        continue
                    else:
                        continue
                if part_min <= v <= 5000 and v > prev[i] + 4:           # a part comes / une pièce arrive
                    if now - F["batch_t"] > 1.0:                       # the ones that come together are one phase
                        F["batch"], F["batch_t"] = F["batch"] + 1, now
                    parts[i] = {"slot": i, "max": v, "hp": v, "shown": False, "dead": None, "hit": -99.0, "t0": now, "batch": F["batch"]}
                    self.hd.log(tr(f"{self.TITLE} : boss, pièce de vie {v}", f"{self.TITLE}: boss, part of life {v}"))
        # destroyed: the game stops its timer again, and no soldier is coming back from a life lost
        if F["engaged"] is not None:
            ch = self.changed(vals, "_wait")
            if ch and ch[1] and not ch[0] and now - F["engaged"] > 1.0:
                F["maybe"] = now
            if F["maybe"] is not None:
                back = now - self.lost_t < 2.5 or any(now - P.zero_t < 2.5 for P in self.sides.values())
                alive = any(q["dead"] is None for q in F["row"])
                if back or not wait:
                    F["maybe"] = None                                  # a soldier back in the game, or a pause that ended
                elif now - F["maybe"] >= (1.6 if alive else 0.4):
                    self._boss_down(F, now)
            if F["down"] is None and vals.get("_clear"):               # the bonuses are counted: it is down for sure
                self._boss_down(F, now)

    def _part_shown(self, F, p, now):
        row = F["row"]
        # the bars start again with the next phase: the parts shown are all down and this one came after them
        # les barres repartent à la phase suivante : les pièces montrées sont toutes tombées et celle-ci est arrivée après
        if not row or (all(q["dead"] is not None for q in row) and p["batch"] > max(q["batch"] for q in row)):
            F["row"] = row = []
            F["wave"] += 1
            if F["wave"] > 1:
                cx, cy = self.machine_at()
                self.popup(f"PHASE {F['wave']}", cx, cy + self.S(96), GOLD, 40, life=1.5, key="stencil")
        p["shown"], p["t0"] = True, now
        row.append(p)
        if len(row) > 6:                                               # six bars at most: the oldest one down leaves
            down = [q for q in row if q["dead"] is not None]
            row.remove(down[0] if down else row[0])

    def _boss_down(self, F, now):
        fx, S = self.fx, self.S
        F["down"] = now
        self.boss_over, self.after = True, None
        for q in F["row"]:
            if q["dead"] is None:
                q["dead"], q["hp"] = now, 0
        cx, cy = self.machine_at()
        for i in range(6):
            fx.later(i * 0.16, fx.explosion, cx + self.rng.uniform(-S(260), S(260)), cy + self.rng.uniform(-S(40), S(40)), 1.1, False)
        fx.shake(12, 0.7)
        fx.flash((255, 240, 200), 0.25, 0.5)
        self.slam(tr("BOSS DÉTRUIT", "BOSS DESTROYED"), GOLD, now, 2.0, sub=F["name"])
        took = now - (F["engaged"] or F["t0"])
        self.hd.log(tr(f"{self.TITLE} : boss détruit en {took:.0f} s, {F['wave']} phase(s)",
                       f"{self.TITLE}: boss destroyed in {took:.0f} s, {F['wave']} phase(s)"))

    def machine_on(self):
        F = self.fight
        if F is not None:
            return F["down"] is None and any(q["dead"] is None for q in F["row"])
        return super().machine_on()

    def machine_at(self):
        if self.fight is not None:
            return self.W / 2, self.S(BOSS_BOX[2] + 67)
        return super().machine_at()

    def _row_boxes(self, F):
        """[(part, x, width)] of the bars, each as wide as its life is big. / Les barres, larges comme leur vie."""
        S = self.S
        row = F["row"]
        w = S(BOSS_BOX[0])
        x, room = self.W / 2 - w / 2 + S(18), w - S(36)
        gap = S(8)
        room -= gap * (len(row) - 1)
        least = min(S(56), room / max(1, len(row)))
        total = float(sum(q["max"] for q in row)) or 1.0
        widths = [max(least, room * q["max"] / total) for q in row]
        k = room / sum(widths) if widths else 1.0
        out = []
        for q, bw in zip(row, widths):
            out.append((q, x, bw * k))
            x += bw * k + gap
        return out

    def _part_at(self, F, p):
        for q, x, bw in self._row_boxes(F):
            if q is p:
                return x + bw / 2, self.S(BOSS_BOX[2] + 67)
        return self.machine_at()

    def draw_machine(self, screen, now):
        F = self.fight
        if F is None:
            return super().draw_machine(screen, now)
        hd, S, W, pg = self.hd, self.S, self.W, self.pg
        k = now - F["t0"]
        if F["heard"] and F["down"] is None and k < ALERT_FOR:           # ALERT is across the screen
            return
        w, h, y0 = (S(v) for v in BOSS_BOX)
        down = F["down"] is not None
        hit = _clamp(1 - (now - F["hit"]) / 0.25)
        x0 = W / 2 - w / 2 + (int(math.sin(now * 90) * S(5) * hit) if hit and not down else 0)
        self.box(screen, x0, y0, w, h, GOLD if down else _mix(RED, WHITE, hit * 0.7))
        # the first line: BOSS and its name / la première ligne : BOSS et son nom
        tag = pg.Rect(int(x0 + S(18)), int(y0 + S(12)), S(96), S(36))
        pg.draw.rect(screen, GOLD if down else RED, tag, border_radius=S(8))
        hd.put(screen, hd.text("BOSS", "stencil", S(27), (24, 10, 8), glow=0), tag.centerx, tag.centery, "center", "middle")
        name = F["name"] or (f"MISSION {F['mission']}" if F["mission"] else "")
        if name:
            t = hd.text(name, "stencil", S(30), (255, 226, 170), glow=0.35)
            room = w - S(18 + 96 + 16 + 18)
            hd.put(screen, t, tag.right + S(16), tag.centery, "left", "middle", scale=min(1.0, room / max(1.0, t["w"])))
        # the second line: a bar for each part being shot at / la deuxième ligne : une barre par pièce sur laquelle on tire
        by, bh = y0 + S(54), S(26)
        row = F["row"]
        if not row:
            if F["engaged"] is None and int(now * 3) % 2 == 0:           # the boss is coming in / le boss arrive
                hd.put(screen, hd.text("ALERT", "stencil", S(30), RED, glow=0.5), W / 2, by + bh / 2, "center", "middle")
            elif F["engaged"] is not None:                             # the fight is on, nothing hurt yet: a full bar, dim
                self.bar(screen, x0 + S(18), by, w - S(36), bh, 1.0, _mix(RED, (40, 14, 14), 0.45), back=(40, 14, 14))
        for q, bx, bw in self._row_boxes(F):
            bx += x0 - (W / 2 - w / 2)
            gone = q["dead"] is not None
            frac = 0.0 if gone else q["hp"] / float(q["max"])
            fresh = _clamp(1 - (now - q["hit"]) / 0.25)
            low = not gone and frac < 0.25 and int(now * 6) % 2 == 0
            self.bar(screen, bx, by, bw, bh, frac, _mix(WHITE if low else RED, WHITE, fresh * 0.8), back=(40, 14, 14))
            if gone:                                                   # down: struck out / détruite : barrée
                c = (150, 84, 84)
                pg.draw.line(screen, c, (int(bx + bw / 2 - S(9)), int(by + S(5))), (int(bx + bw / 2 + S(9)), int(by + bh - S(5))), max(2, S(3)))
                pg.draw.line(screen, c, (int(bx + bw / 2 + S(9)), int(by + S(5))), (int(bx + bw / 2 - S(9)), int(by + bh - S(5))), max(2, S(3)))
        # the third line: the phase, the parts down / la troisième ligne : la phase, les pièces détruites
        ly = y0 + S(100)
        if down:
            hd.put(screen, hd.text(tr("DÉTRUIT", "DESTROYED"), "xbold", S(20), GOLD, glow=0.3), W / 2, ly, "center", "middle")
        elif row:
            hd.put(screen, hd.text(f"PHASE {F['wave']}", "xbold", S(20), CREAM, glow=0), x0 + S(20), ly, "left", "middle")
            if len(row) > 1:
                n = sum(1 for q in row if q["dead"] is not None)
                hd.put(screen, hd.text(tr(f"CIBLES DÉTRUITES {n} / {len(row)}", f"TARGETS DOWN {n} / {len(row)}"), "xbold", S(20), CREAM,
                                       glow=0), x0 + w - S(20), ly, "right", "middle")

    def target(self, side):
        """Where a shot lands: on the machine whose bar is shown, else in the middle, on the player's side of the timer.
        / Où tombe un tir : sur l'engin dont la barre est montrée, sinon au milieu, du côté du joueur."""
        rng, S = self.rng, self.S
        F = self.fight
        if F is not None and self.machine_on():                        # on one of the boss's parts still up
            up = [(x, bw) for q, x, bw in self._row_boxes(F) if q["dead"] is None]
            x, bw = up[rng.randrange(len(up))]
            return x + rng.uniform(0.15, 0.85) * bw, self.machine_at()[1] + rng.uniform(-S(10), S(10))
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
        elif kind in ("rocket", "tank"):                               # a rocket, or the shell of the vehicle's gun
            fx.tracer(x, y, tx, ty, 1600, col, 7, 70, impact=False)
            fx.later(abs(tx - x) / (1600 * self.s), fx.small_blast, tx, ty, 0.8 if kind == "rocket" else 1.2, "back")
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
        self.draw_bonus(screen, now)

    def draw_bonus(self, screen, now):
        """The points the game counts at STAGE CLEAR, in one counter per player between the panels, in his colour when
        both play. / Les points que le jeu compte à STAGE CLEAR, un compteur par joueur entre les panneaux."""
        S = self.S
        on = [(side, P) for side, P in self.sides.items() if P.bonus > 0 and now - P.bonus_t <= BONUS_FOR]
        for i, (side, P) in enumerate(on):
            k = now - P.bonus_t
            if now - P.bonus_shown[1] > 0.2 or k > 0.3:                # the counter moves five times a second
                P.bonus_shown = (P.bonus, now)
            fade = 1.0 if k < BONUS_FOR - 0.4 else max(0.0, (BONUS_FOR - k) / 0.4)
            two = len(on) > 1
            txt = f"BONUS +{_fmt(P.bonus_shown[0])}"
            y = S(336) if not two else S(284 + 58 * i)
            self.label(screen, txt, self.W / 2, y, 40 if two else 50, ACCENT[side] if two else GOLD, key="stencil", align="center",
                       glow=0.6, alpha=190, fade=fade)

    def draw_center(self, screen, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        cx = W / 2
        hd.draw_logo(screen, logo, cx, S(8), S(560), S(124), now)
        tm = _n(vals.get("time"))
        on_map = bool(vals.get("_clear")) and not vals.get("_boss")     # the map between two missions has no timer
        if tm is not None and not on_map:
            low = tm <= 10
            blink = low and int(now * 4) % 2 == 0
            bw, bh = S(170), S(84)
            y = S(152)
            self.box(screen, cx - bw / 2, y, bw, bh, (255, 120, 100) if blink else (255, 240, 220), fill=(8, 10, 22, 210), radius=14, width=3)
            hd.put(screen, hd.text(tr("TEMPS", "TIME"), "bold", S(18), CREAM, glow=0), cx, y + S(14), "center", "middle")
            hd.put_number(screen, str(int(tm)), "stencil", S(50), RED if low else GOLD, cx, y + S(52), "center", "middle")
        m = self.mission(vals)
        if m and not vals.get("_clear"):                               # the mission on the left of the timer, its name on the right
            hd.put(screen, hd.text("MISSION", "bold", S(18), CREAM, glow=0), cx - S(104), S(176), "right", "middle")
            hd.put(screen, hd.text(str(m[0]), "stencil", S(44), GOLD, glow=0.35), cx - S(104), S(210), "right", "middle")
            if m[1]:
                first, _, rest = m[1].partition(" ")
                hd.put(screen, hd.text(first, "stencil", S(28), (255, 226, 170), glow=0.3), cx + S(104), S(180), "left", "middle")
                hd.put(screen, hd.text(rest, "xbold", S(19), CREAM, glow=0), cx + S(104), S(212), "left", "middle")
        elif m and on_map and self.banner is None:                     # the map: the next mission is chosen
            k = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(now * 6))
            self.label(screen, tr("CHOIX DE LA MISSION", "MISSION SELECT"), cx, S(214), 44, GOLD, key="stencil", align="center", alpha=170,
                       fade=k)

    def draw_panel(self, screen, side, vals, now):
        hd, S, pg = self.hd, self.S, self.pg
        P = self.sides[side]
        acc = ACCENT[side]
        hit = max(0.0, 1 - (now - P.hit_t) / 0.4)
        x0 = self.x0(side) + (int(math.sin(now * 90) * S(6) * hit) if hit else 0)
        y0 = S(14)
        screen.blit(self.panels[side], (x0, y0))
        at, chip = chip_at(pg, self.chips[side], side, x0, y0, S)
        screen.blit(self.chips[side], at)
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
        if kind == "tank":                                             # in a vehicle: CHARGE, as the game's box reads
            shot = tr("VÉHICULE", "VEHICLE")
        elif name != "NORMAL" and ammo is not None:                    # what is left of a weapon picked up, beside its name
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
