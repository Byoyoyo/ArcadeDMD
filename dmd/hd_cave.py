"""HD scenes of the Cave shoot'em ups (1.31), DoDonPachi first.

Seen from the sky like the other vertical shoot'em ups of the marquee, the ship flies to the right over a backdrop of
the stage, and the enemies answer the way Cave's games do: rings and spirals of pink and blue bullets, fans of needles,
big slow orbs. The values read in the game drive everything: the points scored blow up an enemy, a big gain (a boss, a
big machine) turns all its bullets into gold stars that fly to the ship, a bomb spent burns the screen and wipes the
bullets, a life lost blows up the ship and gives a new bomb slot, the shot level, the bombs and their slots, the combo
gauge that drains, the hit counter once learned, the ship chosen and the stage.
The ships, the enemies and the backdrops are creations of the program in the spirit of the games, no picture comes from
a game (no ship, character or emblem of Cave's games is drawn).

Scènes HD des shoot'em ups Cave (1.31), DoDonPachi d'abord. Vu du ciel, le vaisseau vole vers la droite au-dessus du
décor du niveau, les ennemis répondent comme dans les jeux Cave : anneaux et spirales de boulettes roses et bleues,
éventails d'aiguilles, grosses sphères lentes. Les valeurs lues dans le jeu pilotent tout : les points marqués font
exploser un ennemi, un gros gain (un boss) change toutes ses boulettes en étoiles d'or qui filent vers le vaisseau,
une bombe embrase l'écran et efface les boulettes, une vie perdue fait exploser le vaisseau et donne une place de
bombe de plus, le niveau de tir, les bombes et leurs places, la jauge de combo qui se vide, le compteur de coups une
fois appris, le vaisseau choisi et le niveau. Vaisseaux, ennemis et décors sont des créations du programme.
"""

import math

from PIL import Image

from .hd_credits import CreditsBar
from .hd_games import CREAM, GOLD, RED, WHITE, _clamp, _mix, _n
from .hd_games3 import DARK, AeroFightersScene, _poly, heli_draw, rotor_draw, tank_draw
from .hd_games6 import PuzzleBobble2Scene
from .hd_games13 import _CpsShooter, pg_plane_draw
from .hd_panels import VIE, PanelScene, _g
from .hd_themes17 import DDP_ROAD, DOCK_ROAD, HIVE_LANES, NEON_LANES, VILLAGE_PATHS
from .i18n import tr

LINE = DARK + (255,)
PINK, BLUE, ORANGE, VIOLET = (255, 70, 170), (70, 170, 255), (255, 150, 40), (190, 90, 255)
MAX_BULLETS = 300
# the roads of the backdrops where the tanks drive / les routes des décors où roulent les chars
LANES = {"ddp_country": DDP_ROAD, "ddp_dock": DOCK_ROAD, "ddp_hive": HIVE_LANES, "fv_neon": NEON_LANES, "gu_village": VILLAGE_PATHS}


def _c(col, a=255):
    return tuple(col[:3]) + (a,)


def _ow(W):
    return max(1, int(W * 0.014))


# ============================================================================ our ships / nos vaisseaux
def fighter_draw(style, body, accent):
    """A fighter of the future seen from above, nose to the right, of our own. 'narrow': a long thin hull, wings swept
    far back, two fins (the type of the focused shot). 'wide': a broad wing swept forward, three guns at the front (the
    type of the spread shot). / Un chasseur du futur vu du dessus, à nous : coque fine et ailes très en flèche, ou aile
    large en flèche inversée et trois canons."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh, lt, acc = _c(body), _c(_mix(body, (0, 0, 0), 0.3)), _c(_mix(body, WHITE, 0.35)), _c(accent)
        if style == "wide":
            for sgn in (1, -1):
                _poly(d, [(0.62, 0.5 + sgn * 0.08), (0.74, 0.5 + sgn * 0.46), (0.6, 0.5 + sgn * 0.46), (0.3, 0.5 + sgn * 0.12)], W, H, sh, LINE, ow)
                _poly(d, [(0.7, 0.5 + sgn * 0.4), (0.92, 0.5 + sgn * 0.4), (0.92, 0.5 + sgn * 0.33), (0.7, 0.5 + sgn * 0.33)], W, H, b, LINE, ow)
                _poly(d, [(0.16, 0.5 + sgn * 0.06), (0.06, 0.5 + sgn * 0.24), (0.14, 0.5 + sgn * 0.24), (0.26, 0.5 + sgn * 0.08)], W, H, sh, LINE, ow)
            _poly(d, [(0.98, 0.5), (0.86, 0.43), (0.12, 0.42), (0.04, 0.46), (0.04, 0.54), (0.12, 0.58), (0.86, 0.57)], W, H, b, LINE, ow)
            _poly(d, [(0.86, 0.47), (0.2, 0.46), (0.2, 0.5), (0.86, 0.5)], W, H, lt)
        else:
            for sgn in (1, -1):
                _poly(d, [(0.56, 0.5 + sgn * 0.06), (0.18, 0.5 + sgn * 0.44), (0.1, 0.5 + sgn * 0.44), (0.2, 0.5 + sgn * 0.06)], W, H, sh, LINE, ow)
                _poly(d, [(0.2, 0.5 + sgn * 0.05), (0.02, 0.5 + sgn * 0.2), (0.08, 0.5 + sgn * 0.2), (0.28, 0.5 + sgn * 0.06)], W, H, b, LINE, ow)
                d.line([(0.22 * W, (0.5 + sgn * 0.34) * H), (0.36 * W, (0.5 + sgn * 0.2) * H)], fill=acc, width=max(2, int(H * 0.04)))
            _poly(d, [(1.0, 0.5), (0.84, 0.44), (0.1, 0.43), (0.03, 0.47), (0.03, 0.53), (0.1, 0.57), (0.84, 0.56)], W, H, b, LINE, ow)
            _poly(d, [(0.84, 0.47), (0.16, 0.465), (0.16, 0.5), (0.84, 0.5)], W, H, lt)
        d.ellipse([0.56 * W, 0.455 * H, 0.78 * W, 0.545 * H], fill=(120, 220, 255, 255), outline=LINE, width=ow)
        d.ellipse([0.62 * W, 0.47 * H, 0.7 * W, 0.49 * H], fill=(230, 250, 255, 255))
        d.line([(0.14 * W, 0.5 * H), (0.5 * W, 0.5 * H)], fill=acc, width=max(2, int(H * 0.035)))
        d.rectangle([0.0, 0.46 * H, 0.04 * W, 0.54 * H], fill=(60, 60, 70, 255), outline=LINE, width=ow)
    return fn


def heli_top_draw(body, accent):
    """Our attack helicopter of our own seen from above, nose to the right (the rotor is drawn apart): the slim cockpit
    with its two seats, the stub wings and their gun pods, the tail boom and its rotor. / Notre hélicoptère d'attaque
    à nous vu du dessus : cockpit fin, petites ailes et leurs nacelles, poutre de queue."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh, acc = _c(body), _c(_mix(body, (0, 0, 0), 0.3)), _c(accent)
        _poly(d, [(0.46, 0.46), (0.02, 0.475), (0.02, 0.525), (0.46, 0.54)], W, H, sh, LINE, ow)            # tail boom / poutre
        _poly(d, [(0.08, 0.36), (0.02, 0.36), (0.02, 0.64), (0.08, 0.64)], W, H, sh, LINE, ow)
        d.ellipse([0.0, 0.26 * H, 0.06 * W, 0.4 * H], fill=(220, 230, 220, 90))
        for sgn in (1, -1):                                                                                 # stub wings / ailettes
            _poly(d, [(0.62, 0.5 + sgn * 0.06), (0.56, 0.5 + sgn * 0.34), (0.44, 0.5 + sgn * 0.34), (0.42, 0.5 + sgn * 0.06)], W, H, sh, LINE, ow)
            d.rounded_rectangle([0.46 * W, (0.5 + sgn * 0.3 - 0.06) * H, 0.72 * W, (0.5 + sgn * 0.3 + 0.06) * H], radius=H * 0.04, fill=acc,
                                outline=LINE, width=ow)
        d.ellipse([0.36 * W, 0.37 * H, 0.98 * W, 0.63 * H], fill=b, outline=LINE, width=ow)
        d.ellipse([0.7 * W, 0.42 * H, 0.94 * W, 0.58 * H], fill=(120, 220, 255, 255), outline=LINE, width=ow)
        d.ellipse([0.54 * W, 0.42 * H, 0.72 * W, 0.58 * H], fill=(90, 190, 240, 255), outline=LINE, width=ow)
        d.line([(0.4 * W, 0.5 * H), (0.56 * W, 0.5 * H)], fill=_c(_mix(body, WHITE, 0.4)), width=max(2, int(H * 0.04)))
    return fn


def option_draw(color):
    """A little floating gun pod, beside our ship. / Une petite nacelle de tir flottante."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.06))
        d.ellipse([0.08 * W, 0.08 * H, 0.92 * W, 0.92 * H], fill=(210, 214, 226, 255), outline=LINE, width=ow)
        d.ellipse([0.28 * W, 0.28 * H, 0.72 * W, 0.72 * H], fill=_c(color), outline=LINE, width=max(1, ow // 2))
        d.ellipse([0.36 * W, 0.32 * H, 0.5 * W, 0.46 * H], fill=(255, 255, 255, 220))
    return fn


# ============================================================================ the enemies / les ennemis
def zako_draw(body, light):
    """A small enemy fighter of our own seen from above, nose to the left: an arrow of dark metal, its engine glowing at
    the back. / Un petit chasseur ennemi à nous, nez à gauche : une flèche de métal sombre, le réacteur qui luit."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh = _c(body), _c(_mix(body, (0, 0, 0), 0.35))
        for sgn in (1, -1):
            _poly(d, [(0.3, 0.5 + sgn * 0.08), (0.82, 0.5 + sgn * 0.46), (0.92, 0.5 + sgn * 0.42), (0.7, 0.5 + sgn * 0.08)], W, H, sh, LINE, ow)
        _poly(d, [(0.0, 0.5), (0.2, 0.4), (0.92, 0.38), (0.98, 0.5), (0.92, 0.62), (0.2, 0.6)], W, H, b, LINE, ow)
        d.ellipse([0.16 * W, 0.44 * H, 0.38 * W, 0.56 * H], fill=_c(light), outline=LINE, width=ow)
        d.ellipse([0.86 * W, 0.42 * H, 1.0 * W, 0.58 * H], fill=(255, 170, 70, 255))
    return fn


def gunship_draw(body, accent):
    """A big armoured gunship of our own seen from above, nose to the left: a thick hull of plates, two engine pods,
    turrets on its back that fire the bullets. / Une grosse canonnière blindée à nous, nez à gauche, tourelles sur le dos."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh, lt, acc = _c(body), _c(_mix(body, (0, 0, 0), 0.32)), _c(_mix(body, WHITE, 0.25)), _c(accent)
        for sgn in (1, -1):
            _poly(d, [(0.34, 0.5 + sgn * 0.12), (0.5, 0.5 + sgn * 0.48), (0.86, 0.5 + sgn * 0.48), (0.9, 0.5 + sgn * 0.14)], W, H, sh, LINE, ow)
            d.rounded_rectangle([0.62 * W, (0.5 + sgn * 0.33 - 0.09) * H, 1.0 * W, (0.5 + sgn * 0.33 + 0.09) * H], radius=H * 0.05, fill=b,
                                outline=LINE, width=ow)
            d.ellipse([0.94 * W, (0.5 + sgn * 0.33 - 0.07) * H, 1.0 * W, (0.5 + sgn * 0.33 + 0.07) * H], fill=(255, 160, 60, 255))
        _poly(d, [(0.02, 0.5), (0.14, 0.34), (0.84, 0.3), (0.96, 0.5), (0.84, 0.7), (0.14, 0.66)], W, H, b, LINE, ow)
        for x in (0.3, 0.5, 0.7):
            d.line([(x * W, 0.33 * H), (x * W, 0.67 * H)], fill=sh, width=max(1, ow))
        _poly(d, [(0.14, 0.42), (0.84, 0.4), (0.84, 0.46), (0.14, 0.47)], W, H, lt)
        for x, r in ((0.32, 0.09), (0.62, 0.11)):                                                         # turrets / tourelles
            d.ellipse([(x - r) * W, 0.5 * H - r * W, (x + r) * W, 0.5 * H + r * W], fill=sh, outline=LINE, width=ow)
            d.ellipse([(x - r * 0.5) * W, 0.5 * H - r * 0.5 * W, (x + r * 0.5) * W, 0.5 * H + r * 0.5 * W], fill=acc)
        d.ellipse([0.04 * W, 0.46 * H, 0.14 * W, 0.54 * H], fill=(255, 90, 60, 255), outline=LINE, width=ow)
    return fn


def turret_draw(d, W, H):
    """A gun turret on the ground of our own seen from above, its barrel to the left. / Une tourelle au sol à nous."""
    ow = _ow(W)
    d.ellipse([0.1 * W, 0.1 * H, 0.9 * W, 0.9 * H], fill=(84, 88, 96, 255), outline=LINE, width=ow)
    d.ellipse([0.26 * W, 0.26 * H, 0.74 * W, 0.74 * H], fill=(120, 124, 132, 255), outline=LINE, width=ow)
    d.line([(0.5 * W, 0.5 * H), (0.0, 0.5 * H)], fill=LINE, width=max(3, int(H * 0.14)))
    d.line([(0.5 * W, 0.5 * H), (0.04 * W, 0.5 * H)], fill=(150, 154, 160, 255), width=max(2, int(H * 0.07)))
    d.ellipse([0.42 * W, 0.42 * H, 0.58 * W, 0.58 * H], fill=(255, 120, 60, 255))


# ============================================================================ bullets and HUD pieces / boulettes et HUD
def bullet_draw(core, rim):
    """A round bullet of the danmaku: a white heart, a ring of colour, a soft halo. / Une boulette : cœur blanc, anneau
    de couleur, halo doux."""
    def fn(d, W, H):
        for k in range(8):                                               # the halo / le halo
            r = 0.5 - k * 0.025
            d.ellipse([(0.5 - r) * W, (0.5 - r) * H, (0.5 + r) * W, (0.5 + r) * H], fill=_c(rim, 18 + k * 6))
        d.ellipse([0.2 * W, 0.2 * H, 0.8 * W, 0.8 * H], fill=_c(rim), outline=_c(_mix(rim, (0, 0, 0), 0.3)), width=max(1, int(W * 0.04)))
        d.ellipse([0.32 * W, 0.32 * H, 0.68 * W, 0.68 * H], fill=_c(core))
    return fn


def needle_draw(color):
    """A needle shot, long and thin, pointing to the right (turned by the scene). / Une aiguille, longue et fine."""
    def fn(d, W, H):
        d.ellipse([0.0, 0.1 * H, W, 0.9 * H], fill=_c(color, 90))
        d.ellipse([0.06 * W, 0.24 * H, 0.94 * W, 0.76 * H], fill=_c(color))
        d.ellipse([0.2 * W, 0.38 * H, 0.86 * W, 0.62 * H], fill=(255, 255, 255, 255))
    return fn


def capsule_draw(color, full=True):
    """A bomb of the HUD: a rounded capsule, or the empty slot of a bomb still to come. / Une bombe du HUD : une capsule,
    ou la place vide d'une bombe à venir."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.08))
        if not full:
            d.rounded_rectangle([0.06 * W, 0.06 * H, 0.94 * W, 0.94 * H], radius=W * 0.4, fill=(20, 22, 34, 150), outline=(130, 120, 100, 200),
                                width=ow)
            return
        d.rounded_rectangle([0.06 * W, 0.06 * H, 0.94 * W, 0.94 * H], radius=W * 0.4, fill=_c(color), outline=LINE, width=ow)
        d.rounded_rectangle([0.2 * W, 0.12 * H, 0.42 * W, 0.6 * H], radius=W * 0.12, fill=(255, 255, 255, 120))
    return fn


# ============================================================================ the shared scene / la scène commune
class CaveShooterScene(_CpsShooter, AeroFightersScene):
    """What the Cave shoot'em ups share: the bullets of the danmaku, the shot and the laser, the gold stars when a boss
    falls, the bomb that burns the screen, the HUD with the hit counter, the combo gauge, the bombs and their slots.
    / Ce que partagent les shoot'em ups Cave : les boulettes, le tir et le laser, les étoiles d'or quand un boss tombe,
    la bombe qui embrase l'écran, le HUD avec le compteur de coups, la jauge de combo, les bombes et leurs places."""
    THEME = "ddp_country"
    STAGES = ("ddp_country",)                          # the backdrop of each stage (stage 1 first) / le décor de chaque niveau
    SHADE = (80, 70)
    ZONE = (150, 330)
    LANES = DDP_ROAD
    ACC = {"p1": (255, 220, 120), "p2": (255, 160, 220)}
    SHOT = {"p1": (255, 236, 150), "p2": (255, 190, 230)}
    LASER = ((80, 150, 255), (170, 225, 255))          # glow and heart of the laser / halo et cœur du laser
    SHIPS = {0: ("narrow", (214, 52, 46)), 1: ("heli", (96, 178, 82)), 2: ("wide", (60, 110, 220))}
    SHIPS_P2 = {0: ("narrow", (230, 120, 50)), 1: ("heli", (170, 170, 60)), 2: ("wide", (150, 80, 210))}
    SHIP_NAMES = {0: "TYPE-A", 1: "TYPE-B", 2: "TYPE-C"}
    SHIP_DEFAULT = {"p1": 0, "p2": 2}
    FOES = (((88, 92, 104), (255, 120, 70)), ((120, 70, 70), (255, 200, 80)))
    GUNSHIP = ((96, 104, 120), (255, 80, 60))
    BULLETS = (PINK, BLUE)                             # the two colours of the bullets / les deux couleurs des boulettes
    TAGS = ("1P", "2P")
    BOMB_COLOR = (255, 196, 60)
    STAGE_WORD = "STAGE"
    DENSITY = 1.0                                      # how thick the bullets are / la densité des boulettes
    MAX_FOES = 9
    SIDE = False                                       # seen from the side (Deathsmiles, Akai Katana) / vu de profil
    STAGE_KEY = "stage"                                # the value of the stage ("round" in Dangun Feveron) / la valeur du niveau
    SIZES = {"jet": (84, 70), "prop": (84, 70), "heli": (112, 72), "bomber": (190, 150)}
    ROTOR = True                                       # the enemy helicopters turn their rotor / rotor des hélicoptères
    LASER_TYPES = (0, 1, 2)                            # ships that use the laser when the fire is held / ceux qui ont un laser

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.bullets = []                              # [x, y, vx, vy, kind]
        self.stars = []                                # [x, y, vx, vy, t0, side]
        self.spirals = []                              # [x, y, angle, turn, arms, until, next, speed, kind, enemy]
        self.maxhit = {"p1": 0, "p2": 0}
        self.hitpop = {"p1": -99.0, "p2": -99.0}
        self.slot_t = {"p1": -99.0, "p2": -99.0}
        self.bomb_t = -99.0
        self.calm_t = -99.0                            # a ship lost: the enemies hold their fire until then / répit
        self.waves = []                                # the rings of the bomb: [t0, x, y, r1, color, life, width]
        self.wave_buf = None
        self.cancels = 0                               # (tests)
        self.lasers = 0
        self.patterns = 0
        self.stage_banners = 0
        self.boss_stars = 0
        self.slow = 1.0                                # the bullets slowed down (Espgaluda's awakening) / ralenties
        self.cbar = CreditsBar(hd, self.fx)            # the credits as in Metal Slug / les crédits comme dans Metal Slug
        self.kill_t = {"p1": -99.0, "p2": -99.0}
        self.kill_xy = {"p1": None, "p2": None}
        self.chain_kills = 0                           # (tests)
        self.chain_sparks = 0
        self.loops = 0
        for P in self.ships.values():
            P.update({"mode": "shot", "mode_t": 0.0, "laser_t": -99.0, "tgt": None, "opt": 0.0})
        self.bd.prebuild([t for t in self.STAGES if t != self.THEME])
        self.warm = [(self.bullet_img, (k,)) for k in range(5)] + self.warm

    # -- pictures / images
    def ship_kind(self, vals, side):
        k = _n(vals.get("ship" if side == "p1" else "ship_p2"))
        table = self.SHIPS if side == "p1" else self.SHIPS_P2
        if k is not None and int(k) in table:
            return int(k)
        if k is not None:                                # a value with other codes (8, 16) / d'autres codes
            keys = sorted(table)
            return keys[min(len(keys) - 1, int(k) // 8)] if int(k) % 8 == 0 else self.SHIP_DEFAULT[side]
        return self.SHIP_DEFAULT[side]

    def kind(self, vals, side):
        return self.ship_kind(vals, side)

    def plane_fn(self, side, kind):
        table = self.SHIPS if side == "p1" else self.SHIPS_P2
        style, body = table.get(kind, table[min(table)])
        if style == "heli":
            return heli_top_draw(body, _mix(body, WHITE, 0.5))
        return fighter_draw(style, body, (255, 255, 255) if side == "p1" else (255, 230, 120))

    def enemy_fn(self, kind):
        """The drawing of an enemy: the little fighters, the helicopter, the big gunship. / Le dessin d'un ennemi."""
        if kind == "bomber":
            return gunship_draw(*self.GUNSHIP)
        if kind == "heli":
            return heli_draw
        body, light = self.FOES[0 if kind == "jet" else 1]
        return zako_draw(body, light)

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            w, h = self.SIZES.get(kind, (84, 70))
            s = self.img(("enemyimg", kind), S(w), S(h), self.enemy_fn(kind))
            if shadow:
                s = self.shadow_of(self.pg, s, 70)
            self.imgs[key] = s
        return s

    def bullet_img(self, kind):
        S = self.S
        key = ("bullet", kind)
        s = self.imgs.get(key)
        if s is None:
            a, b = self.BULLETS
            if kind == 0:
                s = self.img(key, S(32), S(32), bullet_draw((255, 255, 255), a))
            elif kind == 1:
                s = self.img(key, S(32), S(32), bullet_draw((255, 255, 255), b))
            elif kind == 2:
                s = self.img(key, S(44), S(15), needle_draw(b))
            elif kind == 3:
                s = self.img(key, S(50), S(50), bullet_draw((255, 250, 220), ORANGE))
            else:
                s = self.img(key, S(24), S(24), bullet_draw((255, 255, 255), a))
        return s

    def lane_y(self):
        """Where a tank drives: a road of the backdrop of the stage. / Où roule un char : une route du décor du niveau."""
        lanes = LANES.get(self.bd.theme, self.LANES)
        return self.S(self.rng.choice(lanes) + self.rng.uniform(-8, 8))

    def always(self, vals, now):
        """The credits on every image: a coin falls onto the pill when they go up during a game (on the attract screen the
        coin doors show it). / Les crédits à chaque image : une pièce tombe sur la pastille pendant une partie."""
        super().always(vals, now)
        self.cbar.watch(_n(vals.get("credits")), now, drop=not self.nobody(vals))

    # -- a game starts / une partie commence
    def restart(self, vals, now):
        super().restart(vals, now)
        self.bullets, self.stars, self.spirals = [], [], []
        self.maxhit = {"p1": 0, "p2": 0}
        st = _n(vals.get(self.STAGE_KEY))
        if st is not None:
            self.bd.set_theme(self.stage_theme(st), now, 0.0)

    def stage_theme(self, stage):
        return self.STAGES[(max(1, int(stage)) - 1) % len(self.STAGES)]

    # -- the values read / les valeurs lues
    def update(self, vals, now):
        super().update(vals, now)
        S, rng = self.S, self.rng
        if self.next_enemy - now > 1.3:                                 # enemies come thicker / plus d'ennemis
            self.next_enemy = now + rng.uniform(0.5, 1.3)
        for e in self.enemies:                                         # what each new enemy is / ce qu'est chaque ennemi
            if e.get("cave"):
                continue
            e["cave"] = True
            k = rng.random()
            big = any(f.get("type") == "bomber" and not f.get("dead") for f in self.enemies)
            if k < 0.13 and not big:
                e.update({"type": "bomber", "hp": 10, "v": e["v"] * 0.55})
            elif k < 0.38:
                e.update({"type": "heli", "hp": 4, "v": e["v"] * 0.7})
            else:
                e.update({"type": "jet" if rng.random() < 0.6 else "prop", "hp": 3})
        if self.SIDE:
            self.ground = []                                           # nothing on the ground seen from the side / rien au sol
        loop = _n(vals.get("loop"))
        ch = self.changed(vals, self.STAGE_KEY)
        if ch and ch[1] > 0:                                           # a new stage / un nouveau niveau
            self.stage_banners += 1
            self.bd.set_theme(self.stage_theme(ch[1]), now, 1.4)
            if self.STAGE_KEY != "round":                              # ROUND n is already slammed / déjà annoncé
                sub = tr("2E BOUCLE", "2ND LOOP") if loop is not None and loop >= 1 else None
                self.slam(f"{self.STAGE_WORD} {int(ch[1])}", GOLD, now, 2.0, sub=sub)
            self.boost = (3.0, now + 2.0)
            self.bullets, self.spirals = [], []
        ch = self.changed(vals, "loop")
        if ch and ch[1] > ch[0]:                                       # the second loop begins / la 2e boucle commence
            self.loops += 1
            self.slam(tr("2E BOUCLE", "2ND LOOP"), (255, 120, 90), now, 2.6, sub=tr("PLUS DE BOULETTES", "MORE BULLETS"))
            self.fx.flash((255, 200, 160), 0.3, 0.5)
            self.fx.shake(10, 0.6)
        for side, suf in (("p1", ""), ("p2", "_p2")):
            P = self.ships[side]
            ch = self.changed(vals, "hits" + suf)
            if ch:
                old, h = int(ch[0]), int(ch[1])
                n = h - old if h > old else (h if 0 < h < old else 0)   # a new chain starts again from 1 / repart de 1
                if n > 0:
                    self.hitpop[side] = now
                    self.maxhit[side] = max(self.maxhit[side], h)
                    if P["in"]:
                        self.chain_kill(side, n, h, now)
            ch = self.changed(vals, "bombs_max" + suf)
            if ch and ch[1] > ch[0]:
                self.slot_t[side] = now
            ch = self.changed(vals, "lives" + suf)
            if ch and ch[1] < ch[0] and P["in"]:                       # the ship blows up: the bullets vanish / plus de boulettes
                self.clear_bullets(sparkle=True)
                self.calm_t = now + 1.0                                # a moment of respite / un moment de répit
            ch = self.changed(vals, "ship" + suf)
            name = self.SHIP_NAMES.get(self.ship_kind(vals, side), "")
            if ch and P["in"] and name:
                x, y = self.pos(side, now)
                self.popup(name, x, max(S(176), y - S(80)), GOLD, 36, key="stencil")
            ch = self.changed(vals, "combo" + suf)
            if ch and ch[1] > ch[0] + 20 and P["in"]:                    # an enemy destroyed fills the gauge / la jauge se remplit
                self.hitpop[side] = max(self.hitpop[side], now - 0.12)
        self.enemy_fire(now)

    def _steer(self, side, vals, now, dt):
        firing = super()._steer(side, vals, now, dt)
        P = self.ships[side]
        if not firing:
            P["mode"] = "shot"
            return False
        if now >= P["mode_t"]:                                          # the fire held: the laser / tir maintenu : le laser
            laser = P["mode"] == "shot" and self.ship_kind(vals, side) in self.LASER_TYPES
            P["mode"] = "laser" if laser else "shot"
            P["mode_t"] = now + (self.rng.uniform(0.8, 1.6) if laser else self.rng.uniform(1.6, 3.2))
        return True

    # -- our fire / notre tir
    def _fire(self, side, pw, now):
        P = self.ships[side]
        if P["mode"] == "laser":
            self.laser_hit(side, now)
            return
        x, y = self.pos(side, now)
        fx, S = self.fx, self.S
        col = self.SHOT[side]
        kind = self.ship_kind(self.prev, side)
        style = (self.SHIPS if side == "p1" else self.SHIPS_P2).get(kind, ("narrow", None))[0]
        mx = x + S(78)
        fx.muzzle(mx, y, 1, 0.5, col)
        n = 2 + min(3, max(0, int(pw)))
        if style == "wide":                                             # the spread / l'éventail
            lanes = [(0, a) for a in ((-14, 0, 14) if n <= 3 else (-22, -10, 0, 10, 22))]
        elif style == "heli":                                           # the guns follow the turn / les canons suivent
            tilt = _clamp(P["vy"] * 30, -16, 16)
            lanes = [(k * 10, tilt * k * 0.6) for k in (-1, 0, 1)] + ([(k * 26, tilt + k * 6) for k in (-1, 1)] if n > 3 else [])
        else:                                                           # the focused stream / le flot serré
            lanes = [(k * 8, 0) for k in range(-(n // 2), n // 2 + 1)][:n]
        end = self.W + S(60)
        for off, ang in lanes:
            sy = y + S(off)
            ty = sy + math.tan(math.radians(ang)) * (end - mx)
            target = self.in_line(mx, sy, end, ty, S(30))
            if target is not None:
                fx.tracer(mx, sy, target["x"], target.get("yy", target["y"]), speed=3200, color=col, width=6, length=84)
                target["hp"] -= 1
                target["hit"] = now
                if target["hp"] <= 0:
                    fx.later(0.1, self._boom, target)
            else:
                fx.tracer(mx, sy, end, ty, speed=3200, color=col, width=6, length=84, impact=False)

    def in_line(self, x0, y0, x1, y1, reach):
        target = None
        for e in self.enemies:
            if e.get("dead") or e["x"] <= x0:
                continue
            ly = y0 + (y1 - y0) * (e["x"] - x0) / max(1, x1 - x0)
            r = reach * (2.2 if e.get("type") == "bomber" else 1.0)
            if abs(e.get("yy", e["y"]) - ly) < r and (target is None or e["x"] < target["x"]):
                target = e
        return target

    def laser_hit(self, side, now):
        """The laser: a thick beam to the first enemy in front, which flashes, the sparks where it bites.
        / Le laser : un rayon épais jusqu'au premier ennemi devant, qui clignote, des étincelles où il mord."""
        P = self.ships[side]
        x, y = self.pos(side, now)
        S = self.S
        P["laser_t"] = now
        self.lasers += 1
        target = self.in_line(x + S(60), y, self.W + S(60), y, S(36))
        P["tgt"] = target
        if target is not None:
            target["hp"] -= 0.5
            target["hit"] = now
            tx, ty = target["x"], target.get("yy", target["y"])
            self.fx.sparks(tx - S(20), ty, 3, self.LASER[0], (200, 600), (120, 240), (0.12, 0.3), 0, "front", 3, 20)
            if target["hp"] <= 0:
                self.fx.later(0.05, self._boom, target)

    # -- their fire / leur tir
    def aim(self, x, y):
        """Toward the nearest of our ships. / Vers le plus proche de nos vaisseaux."""
        best = None
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"]:
                continue
            sx, sy = self.pos(side, self.fx.now)
            dd = (sx - x) ** 2 + (sy - y) ** 2
            if best is None or dd < best[0]:
                best = (dd, sx, sy)
        if best is None:
            return math.pi
        return math.atan2(best[2] - y, best[1] - x)

    def shoot(self, x, y, ang, speed, kind):
        now = self.fx.now
        if now < self.calm_t or now - self.bomb_t < 1.2:                # a fan already on its way waits too / attend aussi
            return
        if len(self.bullets) < MAX_BULLETS:
            v = speed * self.s
            self.bullets.append([x, y, math.cos(ang) * v, math.sin(ang) * v, kind])

    def ring(self, x, y, n, speed, kind, phase=0.0):
        self.patterns += 1
        for i in range(n):
            self.shoot(x, y, phase + i * math.tau / n, speed, kind)

    def fan(self, x, y, n, spread, speed, kind):
        self.patterns += 1
        base = self.aim(x, y)
        for i in range(n):
            k = (i - (n - 1) / 2) / max(1, (n - 1) / 2)
            self.shoot(x, y, base + math.radians(spread) * k / 2, speed, kind)

    def enemy_fire(self, now):
        """The enemies on the screen fire their patterns: the little ones aimed bullets, the helicopters fans of needles,
        the gunships rings and spirals. / Les ennemis tirent leurs motifs : balles visées, éventails d'aiguilles, anneaux
        et spirales."""
        if self.fx.now - self.bomb_t < 1.2 or self.fx.now < self.calm_t:  # the bomb burns everything, a ship lost / répit
            return
        S, W, rng = self.S, self.W, self.rng
        d = self.DENSITY
        for e in self.enemies:
            if e.get("dead") or not (W * 0.4 < e["x"] < W - S(30)):
                continue
            if "gun" not in e:
                e["gun"] = now + rng.uniform(0.2, 0.8)
                continue
            if now < e["gun"]:
                continue
            x, y = e["x"] - S(20), e.get("yy", e["y"])
            t = e.get("type", "jet")
            if t == "bomber":                                           # rings, flowers, spirals / anneaux, fleurs, spirales
                k = rng.random()
                if k < 0.4:
                    ph = rng.uniform(0, math.tau)
                    self.ring(x, y, int(24 * d), 190, 0, ph)
                    self.ring(x, y, int(24 * d), 130, 1, ph + math.pi / 24)
                elif k < 0.7:
                    self.spirals.append([x, y, rng.uniform(0, math.tau), rng.choice((-1, 1)) * 0.3, 4 if d >= 1 else 2, now + 1.8, now,
                                         200, rng.choice((0, 1)), e])
                else:
                    for j in range(3):                                  # a fan that opens three times / un éventail triple
                        self.fx.later(j * 0.16, self.fan, x, y, int(9 * d) | 1, 70, 260 + j * 40, 4)
                e["gun"] = now + rng.uniform(1.4, 2.2) / d
            elif t == "heli":                                           # fans of needles / éventails d'aiguilles
                self.fan(x, y, int(7 * d) | 1, 46, 380, 2)
                if rng.random() < 0.4:
                    self.fx.later(0.18, self.fan, x, y, int(6 * d) | 1, 40, 330, 2)
                e["gun"] = now + rng.uniform(1.0, 1.8) / d
            else:                                                       # aimed bullets / balles visées
                k = rng.random()
                if k < 0.55:
                    self.fan(x, y, 3, 24, 270, 4)
                elif k < 0.8:
                    self.shoot(x, y, self.aim(x, y), 300, 0)
                else:
                    self.fan(x, y, int(5 * d) | 1, 50, 240, 1)
                e["gun"] = now + rng.uniform(0.7, 1.4) / d
        for g in self.ground:                                          # the tanks lob slow orbs / les chars : sphères lentes
            if g.get("dead"):
                continue
            gx = self.gx(g)
            if W * 0.45 < gx < W - S(40):
                if "gun" not in g:
                    g["gun"] = now + rng.uniform(0.5, 2.0)
                elif now >= g["gun"]:
                    self.shoot(gx - S(26), g["y"], self.aim(gx, g["y"]), 170, 3)
                    g["gun"] = now + rng.uniform(2.4, 4.0) / d
        keep = []
        for sp in self.spirals:                                        # the spirals turn / les spirales tournent
            x, y, ang, turn, arms, until, nxt, speed, kind, e = sp
            if now > until or (e is not None and e.get("dead")):
                continue
            if e is not None:
                sp[0], sp[1] = x, y = e["x"] - S(20), e.get("yy", e["y"])
            while sp[6] <= now:
                for a in range(arms):
                    self.shoot(x, y, sp[2] + a * math.tau / arms, speed, kind)
                sp[2] += turn
                sp[6] += 0.07
            keep.append(sp)
        self.spirals = keep

    # -- the big moments / les grands moments
    def clear_bullets(self, sparkle=False):
        if sparkle:
            for b in self.bullets[::3]:
                self.fx.glow(b[0], b[1], 4, 22, (255, 230, 200), 0.25, "front", 0.9, 0.0)
        self.bullets, self.spirals = [], []

    def cancel(self, side, now):
        """A boss or a big machine falls: all the bullets turn into gold stars that fly to the ship.
        / Un boss ou une grosse machine tombe : toutes les boulettes deviennent des étoiles d'or qui filent au vaisseau."""
        if not self.bullets:
            return
        self.cancels += 1
        self.calm_t = max(self.calm_t, now + 0.8)                       # a breather / un moment de répit
        self.boss_stars += len(self.bullets)
        for b in self.bullets:
            self.stars.append([b[0], b[1], b[2] * 0.15, b[3] * 0.15, now, side])
        self.bullets, self.spirals = [], []

    def score_kill(self, side, gain, ratio, now):
        super().score_kill(side, gain, ratio, now)
        if ratio >= 6 and self.bullets:                                 # a boss: the gold stars / un boss : les étoiles d'or
            self.cancel(side, now)
            self.fx.flash((255, 240, 200), 0.15, 0.35)

    def score_events(self, vals, now):
        """Points scored. With the hit counter read, the enemies destroyed come from it (chain_kill) and their points only
        show as +n; the points that come without a hit (a medal, a boss, the bonus of the stage) go as before: a big blast
        or the bonus counted. / Des points marqués. Avec le compteur de coups lu, les ennemis détruits viennent de lui et
        leurs points s'affichent en +n ; les autres points (médaille, boss, bonus du niveau) comme avant."""
        chained = {}
        for name, side, hname in (("score", "p1", "hits"), ("score_p2", "p2", "hits_p2")):
            ch, hc = self.changed(vals, name), self.changed(vals, hname)
            if ch and ch[1] > ch[0] and hc and (hc[1] > hc[0] or 0 < hc[1] < hc[0]):
                chained[side] = ch[1] - ch[0]
        if not chained:
            super().score_events(vals, now)
            return
        keep = {}
        for side, gain in chained.items():                              # their points: +n where the last one blew up
            name = "score" if side == "p1" else "score_p2"
            keep[name] = self.prev.get(name)
            self.prev[name] = vals.get(name)                            # not counted again below / pas recompté
            if now - self.last_points > 0.35:
                self.last_points = now
                x, y = self.kill_xy[side] or self.pos(side, now)
                self.popup(f"+{int(gain)}", x, y - self.S(50), CREAM, 24)
        super().score_events(vals, now)
        for name, v in keep.items():
            if v is not None:
                self.prev[name] = v

    def chain_kill(self, side, n, h, now):
        """Enemies destroyed in the game, told by the hit counter that climbs: one blows up on the screen for each, three at
        most at once; a burst of hits (the laser on a big one) makes it spark and shake; every 50 hits the chain glows.
        / Des ennemis détruits, dits par le compteur qui monte : un explose pour chacun, trois au plus d'un coup ; une
        rafale de coups (le laser sur un gros) le fait étinceler ; tous les 50 coups la chaîne brille."""
        self.chain_kills += 1
        if now - self.kill_t[side] < 0.08:
            self.spark_target(side, now)
        else:
            self.kill_t[side] = now
            for i in range(min(3, n)):
                self.fx.later(i * 0.05, self.kill_one, side)
        if len([e for e in self.enemies if not e.get("dead")]) < 4:     # more enemies to destroy / d'autres arrivent
            self.next_enemy = min(self.next_enemy, now + 0.15)
        if h // 50 > (h - n) // 50 and h >= 50:                         # every 50 hits / tous les 50 coups
            x, y = self.pos(side, now)
            self.popup(f"{h // 50 * 50} HIT !", x + self.S(120), max(self.S(176), y - self.S(90)), (255, 220, 90), 44, key="stencil")
            self.fx.glow(x, y, 30, 260, (255, 200, 80), 0.5, "front", 0.7, 0.0)

    def kill_one(self, side):
        """One enemy blown up for the chain: the one hit, else the nearest ahead; a big one only takes a hit until its last.
        / Un ennemi détruit pour la chaîne : celui touché, sinon le plus proche devant ; un gros encaisse jusqu'au bout."""
        fx, S, now = self.fx, self.S, self.fx.now
        e = self.kill_target(side, now)
        if e is None:
            spot = self.no_target_kill(side, now)
            if spot is not None:
                self.kill_xy[side] = spot
            return
        x, y = e["x"], e.get("yy", e["y"])
        self.kill_xy[side] = (x, y)
        if e.get("type") == "bomber" and e.get("hp", 0) > 2:
            e["hp"] -= 2
            e["hit"] = now
            fx.sparks(x - S(30), y, 10, (255, 230, 160), (200, 700), (120, 240), (0.15, 0.4), 0, "front", 3, 24)
            fx.small_blast(x + S(self.rng.uniform(-40, 40)), y + S(self.rng.uniform(-30, 30)), 0.8, "front")
            return
        e["doomed"] = True
        self._boom(e)
        fx.sparks(x, y, 14, (255, 236, 170), (300, 900), (0, 360), (0.2, 0.5), 400, "front", 3, 26)
        fx.glow(x, y, 20, 150, (255, 255, 230), 0.18, "front", 0.9, 0.0, hot=0.7)

    def spark_target(self, side, now):
        """A burst of hits on the target of the shot: sparks and a white glint. / Une rafale de coups : étincelles."""
        self.chain_sparks += 1
        e = self.kill_target(side, now)
        if e is None:
            return
        x, y = e["x"], e.get("yy", e["y"])
        e["hit"] = now
        self.fx.sparks(x - self.S(24), y, 6, (255, 240, 200), (200, 600), (120, 240), (0.1, 0.3), 0, "front", 2, 18)

    def bomb(self, side, now):
        """The bomb: the screen burns from the ship forward, waves of blasts, every bullet wiped away, every enemy blown up.
        / La bombe : l'écran s'embrase du vaisseau vers l'avant, vagues d'explosions, plus une boulette, plus un ennemi."""
        fx, S, rng = self.fx, self.S, self.rng
        x, y = self.pos(side, now)
        self.bombs += 1
        self.bpop[side] = now
        self.bomb_t = now
        self.weapon_window(now, 2.2)
        self.popup(tr("BOMBE !", "BOMB!"), x, max(S(176), y - S(80)), (255, 190, 90), 62)
        fx.flash((255, 250, 235), 0.85, 0.6)                             # the screen goes white / l'écran blanchit
        fx.shake(30, 1.6)                                                # the whole screen quakes / tout l'écran tremble
        fx.later(0.35, fx.shake, 22, 1.1)
        fx.later(0.8, fx.shake, 14, 0.9)
        fx.glow(x, y, 60, 1150, (255, 150, 60), 1.0, "front", 0.6, 0.0)
        fx.glow(x, y, 30, 620, (255, 250, 220), 0.5, "front", 0.9, 0.0)
        for i, (col, r1, life, wd) in enumerate((((255, 250, 230), 2300, 0.9, 26), ((255, 190, 90), 1900, 1.1, 18),
                                                 ((255, 120, 60), 1500, 1.3, 12))):
            self.waves.append([now + i * 0.12, x, y, S(r1), col, life, S(wd)])  # rings that sweep the screen / des anneaux
        for b in self.bullets:                                           # the bullets burn away / les boulettes brûlent
            fx.glow(b[0], b[1], 6, 26, (255, 210, 150), 0.3, "front", 0.9, 0.0, delay=rng.uniform(0, 0.25))
        self.bullets, self.spirals = [], []
        for wave in range(5):                                            # waves of blasts / vagues d'explosions
            for i in range(6):
                bx = x + S(140) + wave * S(290) + rng.uniform(-S(90), S(90))
                by = S(self.ZONE[0] - 40) + (S(self.ZONE[1] + 60) - S(self.ZONE[0] - 40)) * (i + rng.uniform(0.1, 0.9)) / 6
                fx.later(0.06 + wave * 0.14 + i * 0.025, fx.explosion, bx, by, rng.uniform(0.8, 1.25), False)
        fx.later(0.45, fx.flash, (255, 170, 90), 0.5, 0.6)
        fx.later(1.0, fx.flash, (255, 120, 60), 0.25, 0.5)
        for e in self.enemies:
            if not e.get("dead"):
                fx.later(0.3 + rng.uniform(0, 0.5), self._boom, e)
        for g in self.ground:
            if not g.get("dead") and self.gx(g) > x:
                fx.later(0.4 + rng.uniform(0, 0.4), self._ground_boom, g)
        self.bd.excite(1.0)

    def draw_waves(self, screen, now):
        """The rings of the bomb, growing from the ship across the whole screen, added to the picture: drawn here and not
        as particles, the blasts that follow would push them out. / Les anneaux de la bombe, qui grandissent du vaisseau
        à tout l'écran, ajoutés à l'image : dessinés ici, les explosions qui suivent les chasseraient des particules."""
        if not self.waves:
            return
        pg = self.pg
        if self.wave_buf is None or self.wave_buf.get_size() != screen.get_size():
            self.wave_buf = pg.Surface(screen.get_size()).convert()
        buf = self.wave_buf
        buf.fill((0, 0, 0))
        keep, drawn = [], False
        for w in self.waves:
            t0, x, y, r1, col, life, wd = w
            k = (now - t0) / life
            if k >= 1:
                continue
            keep.append(w)
            if k < 0:
                continue
            r = self.S(30) + (r1 - self.S(30)) * (1 - (1 - k) ** 2)
            a = 1 - k
            for rr, ww, f in ((r + wd, wd * 2 + 1, 0.3), (r + wd // 2, wd + 1, 0.6), (r, max(2, wd // 3), 1.0)):
                if rr > ww:
                    pg.draw.circle(buf, tuple(min(255, int(v * a * f)) for v in col), (int(x), int(y)), int(rr), int(ww))
                    drawn = True
        self.waves = keep
        if drawn:
            screen.blit(buf, (0, 0), special_flags=pg.BLEND_RGB_ADD)

    # -- what is drawn / ce qui est dessiné
    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg, dt, sp = self.S, self.pg, self.dt, self.fx.sp
        add = pg.BLEND_RGB_ADD
        wreck = self.imgs.get("wreck")
        if wreck is None:
            wreck = self.imgs["wreck"] = pg.Surface((S(46), S(30)), pg.SRCALPHA)
            pg.draw.ellipse(wreck, (20, 18, 16, 150), wreck.get_rect())
        self.wrecks = [w for w in self.wrecks if self.gx(w) > -S(60) and now - w["t"] < 20]
        for w in self.wrecks:
            screen.blit(wreck, (int(self.gx(w) - S(23)), int(w["y"] - S(15))))
        gimg = self.img(("ground", "tank"), S(64), S(30), tank_draw)
        keep = []
        for g in self.ground:                                           # tanks on the roads / chars sur les routes
            if g.get("dead"):
                continue
            g["wx"] -= g["v"] * dt
            x = self.gx(g)
            if x < -S(100):
                continue
            keep.append(g)
            screen.blit(gimg, (int(x - gimg.get_width() / 2), int(g["y"] - gimg.get_height() / 2)))
        self.ground = keep
        keep = []
        for e in self.enemies:                                          # their shadows first / leurs ombres d'abord
            if e.get("dead"):
                continue
            e["x"] -= e["v"] * dt
            if e["x"] < -S(160):
                continue
            big = e.get("type") == "bomber"
            if big and e["x"] < self.W * 0.72:                           # a gunship slows down to fire / ralentit pour tirer
                e.setdefault("slow_t", now)
                if now - e["slow_t"] < 9.0:
                    e["v"] = max(40 * self.s, e["v"] * (1 - dt * 0.8))
                else:                                                    # then it goes away / puis il s'en va
                    e["v"] = min(260 * self.s, e["v"] + 120 * self.s * dt)
            e["yy"] = e["y"] + math.sin(now * 1.6 + e["ph"]) * S(8 if big else 20)
            keep.append(e)
            if not self.SIDE:
                sh = self.enemy_surf(e.get("type", "jet"), True)
                screen.blit(sh, (int(e["x"] + S(50) - sh.get_width() / 2), int(e["yy"] + S(36) - sh.get_height() / 2)))
        for e in keep:
            kind = e.get("type", "jet")
            tilt = 0 if kind == "heli" else (4 if kind == "bomber" else 14)
            img = self.rotated(("enemy_r", kind), self.enemy_surf(kind), _clamp(math.cos(now * 1.6 + e["ph"]) * tilt, -tilt, tilt), 4)
            screen.blit(img, (int(e["x"] - img.get_width() / 2), int(e["yy"] - img.get_height() / 2)))
            if kind == "heli" and not self.SIDE and self.ROTOR:
                base = self.img("rotor", S(124), S(124), rotor_draw)
                rot = self.rotated("rotor", base, (now * 1400 + e["ph"] * 40) % 90, 15)
                screen.blit(rot, (int(e["x"] - S(17) - rot.get_width() / 2), int(e["yy"] - rot.get_height() / 2)))
            if now - e["hit"] < 0.06:
                h = sp.glow(S(44 if kind != "bomber" else 90), (255, 255, 255), 8, hot=0.6)
                screen.blit(h, (int(e["x"] - h.get_width() / 2), int(e["yy"] - h.get_height() / 2)), special_flags=add)
        self.enemies = keep
        self.draw_ships(screen, vals, now)
        self.draw_bullets(screen, now)
        self.draw_stars(screen, now)
        self.draw_waves(screen, now)
        self.draw_over(screen, vals, now)
        self.status(screen, eng, vals, logo, now)
        self.extra_hud(screen, vals, now)

    def draw_over(self, screen, vals, now):
        """Over the bullets (the lock-on of Ketsui, the awakening of Espgaluda). / Par-dessus les boulettes."""

    def extra_hud(self, screen, vals, now):
        """What a game adds to the HUD (a multiplier, an energy gauge, the hero's name). / Ce qu'un jeu ajoute au HUD."""

    def draw_ships(self, screen, vals, now):
        S, sp, pg = self.S, self.fx.sp, self.pg
        add = pg.BLEND_RGB_ADD
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"] or now - P["t_dead"] < 1.2 or now < P["t_spawn"]:
                continue
            kind = self.ship_kind(vals, side)
            x, y = self.pos(side, now)
            if not self.SIDE:
                sh = self.plane_surf(side, kind, True)
                screen.blit(sh, (int(x + S(64) - sh.get_width() / 2), int(y + S(44) - sh.get_height() / 2)))
            laser = now - P["laser_t"] < 0.12
            if laser:
                self.draw_laser(screen, side, x, y, now)
            blink = now - P["t_spawn"] < 1.6 and int(now * 14) % 2 == 0
            if not blink:
                halo = sp.glow(S(70), (255, 255, 255), 2, hot=0.2)          # a soft light under it / une lueur douce
                screen.blit(halo, (int(x - halo.get_width() / 2), int(y - halo.get_height() / 2)), special_flags=add)
                style = (self.SHIPS if side == "p1" else self.SHIPS_P2).get(kind, ("narrow", None))[0]
                if style in ("narrow", "wide"):
                    for dy in (-S(5), S(5)):                             # the engines / les réacteurs
                        fl = sp.streak(S(38) + S(6) * math.sin(now * 40 + dy), S(9), (255, 170, 90), 0, 10)
                        screen.blit(fl, (int(x - S(72) - fl.get_width()), int(y + dy - fl.get_height() / 2)), special_flags=add)
                img = self.rotated(("planer", side, kind), self.plane_surf(side, kind), _clamp(-P["vy"] * 8, -14, 14), 2)
                screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
                if style == "heli":                                      # its rotor turns / son rotor tourne
                    base = self.img("protor", S(150), S(150), rotor_draw)
                    rot = self.rotated("protor", base, (now * 1300) % 90, 15)
                    screen.blit(rot, (int(x + S(10) - rot.get_width() / 2), int(y - rot.get_height() / 2)))
            self.draw_options(screen, side, kind, x, y, laser, now)

    def draw_options(self, screen, side, kind, x, y, laser, now):
        """The little gun pods: close behind the focused ship, turning around the helicopter, wide apart for the spread,
        gathered in front for the laser. / Les nacelles : serrées, qui tournent, écartées, réunies devant pour le laser."""
        S = self.S
        P = self.ships[side]
        style = (self.SHIPS if side == "p1" else self.SHIPS_P2).get(kind, ("narrow", None))[0]
        img = self.img(("option", side), S(26), S(26), option_draw(self.SHOT[side]))
        if laser:
            spots = [(S(70), -S(16)), (S(70), S(16))]
        elif style == "heli":
            P["opt"] += P["vy"] * self.dt * 2.0 + self.dt * 0.6
            spots = [(math.cos(P["opt"] + k * math.pi) * S(56), math.sin(P["opt"] + k * math.pi) * S(56)) for k in (0, 1)]
        elif style == "wide":
            spots = [(S(10), -S(74)), (S(10), S(74))]
        else:
            spots = [(-S(40), -S(40)), (-S(40), S(40))]
        for dx, dy in spots:
            ox, oy = x + dx, y + dy + math.sin(now * 5 + dx) * S(3)
            screen.blit(img, (int(ox - img.get_width() / 2), int(oy - img.get_height() / 2)))

    def laser_img(self, k):
        """The laser beam, long enough for the whole screen, cut to its length when drawn: a wide glow, a white heart,
        three widths that take turns so it quivers. / Le rayon laser, coupé à sa longueur : halo large, cœur blanc,
        trois largeurs qui alternent pour qu'il vibre."""
        key = ("laser", k, self.LASER)
        s = self.imgs.get(key)
        if s is None:
            S = self.S
            glow, heart = self.LASER
            w, h = self.W + S(80), S(72)
            half = h / 2
            core = S(5) + k * S(1.2)
            outer = S(20) + k * S(3)
            col = Image.new("RGB", (1, h))
            for yy in range(h):
                dd = abs(yy + 0.5 - half)
                g = math.exp(-(dd / outer) ** 2) * 0.8 + math.exp(-(dd / (outer * 2.2)) ** 2) * 0.25
                c = math.exp(-(dd / core) ** 2) * 0.8
                col.putpixel((0, yy), tuple(min(255, int(gc * g + hc * c)) for gc, hc in zip(glow, heart)))
            s = self.imgs[key] = self.hd._surf(col.resize((w, h)))
        return s

    def draw_laser(self, screen, side, x, y, now):
        """The laser beam: a wide glow and a white heart, an aura around the ship, a blaze where it bites.
        / Le rayon laser : un halo large et un cœur blanc, une aura autour du vaisseau, un brasier où il mord."""
        S, sp, pg = self.S, self.fx.sp, self.pg
        add = pg.BLEND_RGB_ADD
        P = self.ships[side]
        x0 = x + S(66)
        tgt = P.get("tgt")
        x1 = tgt["x"] - S(24) if tgt is not None and not tgt.get("dead") else self.W + S(40)
        length = max(S(40), int(x1 - x0))
        img = self.laser_img(int(now * 30) % 3)
        screen.blit(img, (int(x0), int(y - img.get_height() / 2)), area=pg.Rect(0, 0, length, img.get_height()), special_flags=add)
        glow = self.LASER[0]
        lv = 7 + int(round(math.sin(now * 50) * 2))
        aura = sp.glow(S(64), glow, lv, hot=0.5)
        screen.blit(aura, (int(x - aura.get_width() / 2 + S(30)), int(y - aura.get_height() / 2)), special_flags=add)
        if tgt is not None and not tgt.get("dead"):
            bite = sp.glow(S(50), (255, 240, 200), lv + 2, hot=0.7)
            screen.blit(bite, (int(x1 - bite.get_width() / 2), int(y - bite.get_height() / 2)), special_flags=add)

    def draw_bullets(self, screen, now):
        dt, W, H, S = self.dt, self.W, self.H, self.S
        imgs = [self.bullet_img(k) for k in range(5)]
        keep = []
        blit = screen.blit
        k = dt * self.slow
        for b in self.bullets:
            b[0] += b[2] * k
            b[1] += b[3] * k
            x, y, kind = b[0], b[1], b[4]
            if x < -S(40) or x > W + S(40) or y < -S(40) or y > H + S(40):
                continue
            keep.append(b)
            if kind == 2:                                                # the needles point their way / les aiguilles
                img = self.rotated(("needle", self.BULLETS), imgs[2], -math.degrees(math.atan2(b[3], b[2])), 15)
            else:
                img = imgs[kind]
            blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        self.bullets = keep

    def draw_stars(self, screen, now):
        """The gold stars of the bullets cancelled: they hang a moment, then fly to the ship. / Les étoiles d'or."""
        if not self.stars:
            return
        S, dt, sp, pg = self.S, self.dt, self.fx.sp, self.pg
        keep = []
        for st in self.stars:
            x, y, vx, vy, t0, side = st
            k = now - t0
            if k > 2.4:
                continue
            if k > 0.45:                                                  # they fly to the ship / ils filent au vaisseau
                tx, ty = self.pos(side, now) if self.ships[side]["in"] else (S(200), self.H / 2)
                dx, dy = tx - x, ty - y
                dist = math.hypot(dx, dy)
                if dist < S(30):
                    if self.rng.random() < 0.15:
                        self.fx.glow(tx, ty, 6, 30, (255, 220, 120), 0.2, "front", 0.8, 0.0)
                    continue
                v = (600 + 900 * min(1.0, (k - 0.45) * 1.5)) * self.s
                st[2], st[3] = dx / dist * v, dy / dist * v
            st[0] += st[2] * dt
            st[1] += st[3] * dt
            keep.append(st)
            img = sp.star(S(13), (255, 214, 60), int(t0 * 10 + x) % 4)
            screen.blit(img, (int(st[0] - img.get_width() / 2), int(st[1] - img.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        self.stars = keep

    # -- the HUD / le HUD
    def ship_icon(self, side, vals):
        key = ("cavelife", side, self.ship_kind(vals, side))
        icon = self.imgs.get(key)
        if icon is None:
            icon = self.img(("cavelifeimg", side, self.ship_kind(vals, side)), self.S(44), self.S(38), self.plane_fn(side, self.ship_kind(vals, side)))
            self.imgs[key] = icon
        return icon

    def score_tag(self, screen, eng, vals, side, now):
        """1P and the score, the ships left under it. / 1P et le score, les vaisseaux restants dessous."""
        S, W, hd = self.S, self.W, self.hd
        right = side == "p2"
        suf = "_p2" if right else ""
        tag = self.TAGS[1 if right else 0]
        col = (255, 120, 200) if right else (255, 210, 70)
        sc = _n(vals.get("score" + suf))
        tw_ = hd.text(tag, "black", S(40), col)["w"]
        sw = hd.text(str(int(sc)), "black", S(56), WHITE)["w"] if sc is not None else 0
        w = tw_ + sw + S(48)
        x0 = W - S(16) - w if right else S(16)
        self.pill(screen, x0, S(8), w, S(70), 150)
        if right:
            self.text(screen, tag, W - S(16) - S(18), S(22), 40, col, align="right")
            if sc is not None:
                hd._score(screen, eng, "score" + suf, W - S(16) - S(30) - tw_, S(14), "right", S(56))
        else:
            self.text(screen, tag, x0 + S(18), S(22), 40, col)
            if sc is not None:
                hd._score(screen, eng, "score" + suf, x0 + S(30) + tw_, S(14), "left", S(56))
        lives = _n(vals.get("lives" + suf))
        if lives is not None and lives > 0:
            icon = self.ship_icon(side, vals)
            n = min(6, int(lives))
            lw = n * S(46)
            bx = W - S(26) - lw if right else S(26)
            self.pill(screen, bx - S(10), S(82), lw + S(20), S(46), 140)
            for i in range(n):
                screen.blit(icon, (int(bx + i * S(46)), S(86)))
        self.power_gauge(screen, vals, side, now)

    def power_gauge(self, screen, vals, side, now):
        """The level of the shot beside the ships left: POWER and a case per level, lit up to the level read in the game,
        the newest one flashing when it grows, MAX at the top. Many levels (Guwange, Air Gallet): a bar and 12/14.
        / Le niveau du tir à côté des vaisseaux : POWER et une case par niveau, allumées jusqu'au niveau lu, MAX en haut."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        right = side == "p2"
        v = _n(vals.get("power" + ("_p2" if right else "")))
        if v is None:
            return
        lit, total = self.power_cases(vals, side, v)
        total = max(1, total or 1)
        lit = min(lit, total)
        top = lit >= total
        y = S(105)
        lab = hd.text("POWER", "bold", S(22), CREAM)["w"]
        cases = total <= 10
        cw, gap = (S(30 if total <= 6 else 24), S(7)) if cases else (0, 0)
        body = total * cw + (total - 1) * gap if cases else S(200)
        tail = S(64) if top else (0 if cases else S(70))
        w = lab + S(14) + body + tail
        x0 = W - S(330) - w if right else S(330)
        self.pill(screen, x0 - S(12), y - S(23), w + S(24), S(46), 150)
        self.text(screen, "POWER", x0, y, 22, CREAM, key="bold", valign="middle", glow=0)
        bx = x0 + lab + S(14)
        k = max(0.0, 1 - (now - self.powered.get(side, -99.0)) / 0.6)      # the level just grew / le niveau vient de grandir
        if cases:
            for i in range(total):
                on = i < lit
                if top:
                    col = _mix(GOLD, WHITE, 0.5 + 0.5 * math.sin(now * 10))
                elif on and i == lit - 1 and k > 0 and int(now * 16) % 2 == 0:
                    col = WHITE
                else:
                    col = (255, 210, 70) if on else (58, 46, 26)
                cx = int(bx + i * (cw + gap))
                pg.draw.rect(screen, col, (cx, y - S(11), cw, S(22)), border_radius=S(5))
                if on:
                    pg.draw.rect(screen, _mix(col, WHITE, 0.6), (cx + S(5), y - S(8), cw - S(10), S(5)), border_radius=S(2))
        else:
            self.bar(screen, bx, y - S(9), body, S(18), lit / float(total), (255, 200, 60) if not top else GOLD, back=(40, 30, 16))
            if not top:
                self.text(screen, f"{int(lit)}/{int(total)}", bx + body + S(10), y, 20, CREAM, key="bold", valign="middle", glow=0)
        if top:
            self.text(screen, "MAX", bx + body + S(10), y, 24, GOLD, key="black", valign="middle", glow=0.4,
                      scale=1 + 0.08 * math.sin(now * 10))

    def hit_counter(self, screen, vals, side, now):
        """The hit counter as in the game: the number and HIT, the gauge that drains under it, the best chain.
        / Le compteur de coups : le nombre et HIT, la jauge qui se vide dessous, la meilleure chaîne."""
        S, W, pg = self.S, self.W, self.pg
        right = side == "p2"
        suf = "_p2" if right else ""
        hits, gauge = _n(vals.get("hits" + suf)), _n(vals.get("combo" + suf))
        if hits is None and gauge is None:
            return
        x = W - S(28) if right else S(28)
        y = S(162)
        gw = S(220)
        if hits is not None and hits > 0:
            k = max(0.0, 1 - (now - self.hitpop[side]) / 0.25)
            num = self.hd.text(str(int(hits)), "stencil", S(58), (255, 230, 90), 0.7)
            word = self.hd.text("HIT", "stencil", S(30), (255, 150, 60), 0.5)
            w = num["w"] + S(8) + word["w"]
            x0 = x - w if right else x
            self.pill(screen, x0 - S(12), y - S(30), max(w, gw) + S(24), S(98 if gauge is not None else 62), 130, radius=14)
            self.hd.put(screen, num, x0, y, "left", "middle", scale=1 + 0.25 * k)
            self.hd.put(screen, word, x0 + num["w"] + S(8), y + S(9), "left", "middle")
            y += S(40)
        elif gauge is not None and gauge > 0:
            self.pill(screen, (x - gw if right else x) - S(12), y - S(14), gw + S(24), S(28), 120, radius=10)
        if gauge is not None:
            gx = x - gw if right else x
            frac = _clamp(gauge / 100.0)
            pg.draw.rect(screen, (30, 20, 16), (int(gx), int(y - S(6)), gw, S(12)), border_radius=S(6))
            if frac > 0:
                col = (255, int(120 + 110 * frac), 40)
                fw = max(S(12), int(gw * frac))
                pg.draw.rect(screen, col, (int(gx if not right else gx + gw - fw), int(y - S(6)), fw, S(12)), border_radius=S(6))
            pg.draw.rect(screen, (150, 110, 60), (int(gx), int(y - S(6)), gw, S(12)), max(1, S(2)), border_radius=S(6))
        if self.maxhit[side] > 0 and hits is not None:
            self.text(screen, f"MAX HIT {self.maxhit[side]}", x if not right else x, y + S(20), 22, CREAM, key="black",
                      align="right" if right else "left", valign="middle", glow=0.2)

    def bombs_row(self, screen, vals, side, now):
        """The bombs at the bottom as in the game, the empty slots of the bombs still to come, MAX when they are all full.
        / Les bombes en bas, les places vides des bombes à venir, MAX quand tout est plein."""
        S, W, H = self.S, self.W, self.H
        right = side == "p2"
        suf = "_p2" if right else ""
        n, slots = _n(vals.get("bombs" + suf)), _n(vals.get("bombs_max" + suf))
        if n is None:
            return None
        n = max(0, int(n))
        total = max(n, int(slots)) if slots is not None else n
        total = min(8, total)
        full = self.img(("capsule", True), S(30), S(44), capsule_draw(self.BOMB_COLOR, True))
        empty = self.img(("capsule", False), S(30), S(44), capsule_draw(self.BOMB_COLOR, False))
        step = S(36)
        bw = max(1, total) * step
        y = H - S(40)
        x0 = W - S(30) - bw if right else S(30)
        self.pill(screen, x0 - S(12), y - S(30), bw + S(24), S(60), 150, radius=14)
        pop = max(0.0, 1 - (now - self.bpop[side]) / 0.5)
        for i in range(total):
            img = full if i < n else empty
            screen.blit(img, (int(x0 + i * step), int(y - img.get_height() / 2 - (S(6) * pop if i < n else 0))))
            if i < n:
                self.text(screen, "B", x0 + i * step + img.get_width() / 2, y + S(2), 22, (90, 40, 10), key="black", align="center",
                          valign="middle", glow=0)
        if now - self.slot_t[side] < 1.0 and total:                       # a new slot glints / une place neuve brille
            g = self.fx.sp.glow(S(60), (255, 230, 150), 9, hot=0.6)
            gx = x0 + (total - 1) * step + S(15)
            screen.blit(g, (int(gx - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
        if slots is not None and n >= int(slots) > 0:
            k = 0.75 + 0.25 * math.sin(now * 6)
            self.label(screen, "MAX", (x0 - S(20)) if right else (x0 + bw + S(20)), y, 30, GOLD, key="black", align="right" if right else "left",
                       fade=k)
            return bw + S(110)
        return bw + S(30)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score at the top left with the ships left, the hit counter and its gauge, the bombs
        and their slots at the bottom, the ship chosen, 2P on the right, the credits in the middle.
        / Comme dans le jeu : 1P et le score avec les vaisseaux, le compteur de coups et sa jauge, les bombes et leurs
        places en bas, le vaisseau choisi, 2P à droite, les crédits au milieu."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(96), now)
        self.score_tag(screen, eng, vals, "p1", now)
        self.hit_counter(screen, vals, "p1", now)
        two = self.p2_in(vals)
        if two:
            self.score_tag(screen, eng, vals, "p2", now)
            self.hit_counter(screen, vals, "p2", now)
        else:
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(44), 34, col, align="right")
        w1 = self.bombs_row(screen, vals, "p1", now)
        name = self.SHIP_NAMES.get(self.ship_kind(vals, "p1")) if vals.get("ship") is not None else None
        if name:
            self.label(screen, name, S(30) + (w1 or 0) + S(10), H - S(40), 26, CREAM, key="black", alpha=140)
        if two:
            self.bombs_row(screen, vals, "p2", now)
        c = _n(vals.get("credits"))
        if c is not None:                                                # as in Metal Slug / comme dans Metal Slug
            self.cbar.set_symbol((getattr(eng, "cfg", None) or {}).get("coin_symbol", "€"))
            self.cbar.draw(screen, c, W / 2, H - S(44), now, 0.85)


# ============================================================================ DoDonPachi
class DoDonPachiScene(CaveShooterScene):
    """DoDonPachi (1997), as in the game: the three ships read in the game, the red fighter of the focused shot, the
    helicopter whose guns follow its turns, the blue fighter of the spread, each with its laser when the fire is held;
    the stages in the spirit of the game (the countryside and its highway, the city, the harbour and its docks, the
    ruins, the fortress, the honeycomb hive, the last fortress in space); the hit counter and its gauge that drains,
    the bombs and their slots, MAX when they are full, the gold stars when a boss falls. / DoDonPachi comme dans le
    jeu : les trois vaisseaux lus dans le jeu avec leur laser, les niveaux dans l'esprit du jeu, le compteur de coups et
    sa jauge, les bombes et leurs places, MAX quand tout est plein, les étoiles d'or quand un boss tombe."""
    THEME = "ddp_country"
    STAGES = ("ddp_country", "af_city", "ddp_dock", "s45_ground", "ddp_fortress", "ddp_hive", "am_fortress")
    BULLETS = (PINK, BLUE)


class DonPachiScene(CaveShooterScene):
    """DonPachi (1995), the first of the series, as in the game: the three ships (the red fighter, the helicopter, the
    blue fighter), the stages in the spirit of the game, the combo gauge, thinner bullets than in its sequel.
    / DonPachi, le premier de la série : les trois vaisseaux, les niveaux, la jauge de combo, moins de boulettes."""
    THEME = "s45_ground"
    STAGES = ("s45_ground", "ddp_dock", "af_city", "ddp_fortress", "am_fortress")
    BULLETS = ((255, 120, 60), (90, 200, 255))
    DENSITY = 0.6


class DaiOuJouScene(CaveShooterScene):
    """DoDonPachi Dai-Ou-Jou (2002) and its Black Label: the red fighter and the helicopter-like gunship of our own, the
    thickest rain of bullets of the series, the hit counter, the bombs and their slots, the gold stars.
    / DoDonPachi Dai-Ou-Jou : la pluie de boulettes la plus épaisse de la série, le compteur, les bombes et leurs places."""
    THEME = "ddp_fortress"
    STAGES = ("ddp_fortress", "af_city", "ddp_dock", "ddp_hive", "am_fortress", "lh_space")
    SHIPS = {0: ("narrow", (214, 52, 46)), 1: ("wide", (60, 110, 220))}
    SHIPS_P2 = {0: ("narrow", (230, 120, 50)), 1: ("wide", (150, 80, 210))}
    SHIP_DEFAULT = {"p1": 0, "p2": 1}
    BULLETS = ((255, 80, 150), (110, 150, 255))
    DENSITY = 1.3


class DaiFukkatsuScene(DaiOuJouScene):
    """DoDonPachi Dai-Fukkatsu, its Black Label and SaiDaiOuJou (CV1000): the later games of the series, the same rain
    of bullets in brighter colours. / Les derniers jeux de la série, la même pluie de boulettes en plus vif."""
    THEME = "af_city"
    STAGES = ("af_city", "ddp_fortress", "ddp_dock", "ddp_hive", "lh_space", "am_fortress")
    BULLETS = ((255, 90, 200), (90, 210, 255))
    LASER = ((120, 255, 200), (220, 255, 240))


class DoDonPachi2Scene(DoDonPachiScene):
    """DoDonPachi II: Bee Storm, made by IGS under Cave's licence: the three ships, the stages, the combo gauge.
    / DoDonPachi II, fait par IGS sous licence Cave : les trois vaisseaux, les niveaux, la jauge de combo."""
    THEME = "c44_sea"
    STAGES = ("c44_sea", "ddp_country", "af_city", "ddp_fortress", "ddp_hive", "am_fortress")
    BULLETS = ((255, 110, 60), (80, 190, 255))
    DENSITY = 0.9


# ============================================================================ ESP Ra.De.
def psychic_draw(suit, hair, glow):
    """A young psychic of our own flying head first, seen from above, head to the right: the arms stretched forward,
    the legs behind, the coat that floats. / Un jeune médium à nous qui vole tête la première, vu du dessus."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.02))
        sk = (236, 196, 160, 255)
        _poly(d, [(0.46, 0.38), (0.02, 0.2), (0.06, 0.5), (0.02, 0.8), (0.46, 0.62)], W, H, _c(_mix(suit, (0, 0, 0), 0.3), 230), LINE, ow)
        for sgn in (1, -1):                                              # the legs / les jambes
            d.line([(0.42 * W, (0.5 + sgn * 0.06) * H), (0.12 * W, (0.5 + sgn * 0.12) * H)], fill=LINE, width=max(3, int(H * 0.12)))
            d.line([(0.42 * W, (0.5 + sgn * 0.06) * H), (0.13 * W, (0.5 + sgn * 0.12) * H)], fill=_c(_mix(suit, (0, 0, 0), 0.45)),
                   width=max(2, int(H * 0.08)))
            d.line([(0.62 * W, (0.5 + sgn * 0.1) * H), (0.9 * W, (0.5 + sgn * 0.08) * H)], fill=LINE, width=max(3, int(H * 0.1)))   # arms
            d.line([(0.62 * W, (0.5 + sgn * 0.1) * H), (0.89 * W, (0.5 + sgn * 0.08) * H)], fill=_c(suit), width=max(2, int(H * 0.07)))
            d.ellipse([0.88 * W, (0.5 + sgn * 0.08 - 0.05) * H, 0.96 * W, (0.5 + sgn * 0.08 + 0.05) * H], fill=sk, outline=LINE, width=ow)
        d.rounded_rectangle([0.38 * W, 0.36 * H, 0.7 * W, 0.64 * H], radius=H * 0.1, fill=_c(suit), outline=LINE, width=ow)
        d.ellipse([0.66 * W, 0.38 * H, 0.86 * W, 0.62 * H], fill=_c(hair), outline=LINE, width=ow)
        d.ellipse([0.8 * W, 0.44 * H, 0.88 * W, 0.56 * H], fill=sk)
        d.ellipse([0.48 * W, 0.44 * H, 0.6 * W, 0.56 * H], fill=_c(glow))
    return fn


class EspRadeScene(CaveShooterScene):
    """ESP Ra.De. (1998), as in the game: young psychics of our own who fly over the Tokyo of the future, by night, the
    combo multiplier read in the game (up to x16), the bombs of the guard barrier, the psychic beam when the fire is held.
    / ESP Ra.De. : de jeunes médiums à nous au-dessus du Tokyo du futur, la nuit, le multiplicateur lu dans le jeu (x16),
    les bombes de la barrière, le rayon psychique quand le tir est maintenu."""
    THEME = "af_night"
    STAGES = ("af_night", "af_city", "ddp_dock", "ddp_fortress", "am_fortress")
    SHIPS = {0: ("psy", (60, 90, 200))}
    SHIPS_P2 = {0: ("psy", (200, 60, 90))}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    LASER = ((200, 120, 255), (240, 220, 255))
    BULLETS = ((255, 70, 110), (150, 110, 255))
    DENSITY = 1.1

    def plane_fn(self, side, kind):
        if side == "p1":
            return psychic_draw((60, 90, 200), (40, 30, 30), (120, 220, 255))
        return psychic_draw((200, 60, 90), (230, 200, 120), (255, 160, 220))

    def extra_hud(self, screen, vals, now):
        m = _n(vals.get("multiplier"))
        if m is not None and m > 1:                                      # the multiplier / le multiplicateur
            k = 0.8 + 0.2 * math.sin(now * 8)
            self.label(screen, f"x{int(m)}", self.S(300), self.S(162), 44, GOLD, key="stencil", align="left", fade=k)


# ============================================================================ Guwange
def wanderer_draw(robe, hat):
    """A wanderer of old Japan of our own seen from above, walking to the right: the wide straw hat, the shoulders of
    his robe, the sleeves. / Un voyageur du Japon d'autrefois à nous, vu du dessus : le grand chapeau de paille, la robe."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.02))
        r, rd = _c(robe), _c(_mix(robe, (0, 0, 0), 0.35))
        d.ellipse([0.18 * W, 0.22 * H, 0.66 * W, 0.78 * H], fill=rd, outline=LINE, width=ow)           # the robe / la robe
        for sgn in (1, -1):                                               # sleeves / manches
            d.ellipse([0.36 * W, (0.5 + sgn * 0.28 - 0.12) * H, 0.66 * W, (0.5 + sgn * 0.28 + 0.12) * H], fill=r, outline=LINE, width=ow)
        d.ellipse([0.3 * W, 0.18 * H, 0.86 * W, 0.82 * H], fill=_c(hat), outline=LINE, width=ow)        # the hat / le chapeau
        for k in range(1, 4):
            rr = 0.28 * k / 4
            d.ellipse([(0.58 - rr) * W, (0.5 - rr * 1.15) * H, (0.58 + rr) * W, (0.5 + rr * 1.15) * H], outline=_c(_mix(hat, (0, 0, 0), 0.3)),
                      width=max(1, ow // 2))
        d.ellipse([0.54 * W, 0.46 * H, 0.62 * W, 0.54 * H], fill=_c(_mix(hat, (0, 0, 0), 0.4)))
    return fn


def spirit_draw(color):
    """A guardian spirit of our own: a floating flame with two eyes, its tail of light. / Un esprit gardien à nous."""
    def fn(d, W, H):
        for k in range(6):
            r = 0.46 - k * 0.05
            d.ellipse([(0.5 - r) * W, (0.5 - r) * H, (0.5 + r) * W, (0.5 + r) * H], fill=_c(color, 40 + k * 30))
        d.polygon([(0.5 * W, 0.08 * H), (0.78 * W, 0.5 * H), (0.5 * W, 0.86 * H), (0.22 * W, 0.5 * H)], fill=(255, 250, 230, 230))
        for x in (0.42, 0.58):
            d.ellipse([(x - 0.05) * W, 0.42 * H, (x + 0.05) * W, 0.54 * H], fill=(40, 30, 60, 255))
    return fn


class GuwangeScene(CaveShooterScene):
    """Guwange (1999), as in the game: our wanderer of old Japan walks the village at dusk while his guardian spirit
    flies around him and fires, the hero read in the game (Sisin, Kosame, Gensuke), his energy, the combo gauge, the
    bombs. / Guwange : notre voyageur du Japon d'autrefois marche dans le village au crépuscule, son esprit gardien vole
    autour de lui et tire, le héros lu dans le jeu, son énergie, la jauge de combo, les bombes."""
    THEME = "gu_village"
    STAGES = ("gu_village", "ct_forest", "ncm_jungle", "gw_lava")
    LANES = VILLAGE_PATHS
    SHIPS = {0: ("walk", (90, 60, 120)), 1: ("walk", (150, 60, 60)), 2: ("walk", (60, 100, 90))}
    SHIPS_P2 = SHIPS
    SHIP_NAMES = {0: "SISIN", 1: "KOSAME", 2: "GENSUKE"}
    FOES = (((96, 70, 50), (255, 200, 90)), ((70, 60, 80), (255, 120, 160)))
    GUNSHIP = ((110, 80, 56), (255, 140, 60))
    BULLETS = ((255, 90, 120), (120, 150, 255))
    LASER = ((255, 200, 120), (255, 250, 220))

    def ship_kind(self, vals, side):
        k = _n(vals.get("char" if side == "p1" else "char_p2"))
        return int(k) if k is not None and int(k) in self.SHIPS else 0

    def plane_fn(self, side, kind):
        robe = self.SHIPS.get(kind, self.SHIPS[0])[1]
        return wanderer_draw(robe, (196, 170, 110) if side == "p1" else (150, 130, 90))

    def draw_options(self, screen, side, kind, x, y, laser, now):
        """The spirit flies around the wanderer, in front when he fires. / L'esprit vole autour du voyageur."""
        S = self.S
        img = self.img(("spirit", side), S(48), S(48), spirit_draw((150, 220, 255) if side == "p1" else (255, 170, 220)))
        a = now * 2.2 + (0 if side == "p1" else math.pi)
        ox, oy = (x + S(70), y) if laser else (x + math.cos(a) * S(64), y + math.sin(a) * S(46))
        screen.blit(img, (int(ox - img.get_width() / 2), int(oy - img.get_height() / 2)))

    def extra_hud(self, screen, vals, now):
        e = _n(vals.get("energy"))
        if e is not None:
            self.gauge(screen, tr("ÉNERGIE", "ENERGY"), e / 100.0, self.S(30), self.S(216), 200, (120, 220, 140) if e > 25 else RED)
        name = vals.get("p1_char")
        if isinstance(name, str) and name:
            self.label(screen, name, self.W / 2, self.H - self.S(76), 28, WHITE, key="black", align="center", alpha=130)


# ============================================================================ Dangun Feveron
class FeveronScene(CaveShooterScene):
    """Dangun Feveron (Fever SOS, 1998), as in the game: a night of fever on a floor of neon, the three fighters read in
    the game (the focused shot, the three ways, the wide area), the round read in the game, the bombs. / Dangun
    Feveron : une nuit de fièvre sur une piste au néon, les trois chasseurs lus dans le jeu, le round, les bombes."""
    THEME = "fv_neon"
    STAGES = ("fv_neon", "af_night", "lh_space", "fv_neon", "am_fortress")
    LANES = NEON_LANES
    STAGE_KEY = "round"
    STAGE_WORD = "ROUND"
    SHIPS = {0: ("narrow", (240, 60, 160)), 1: ("wide", (60, 200, 240)), 2: ("wide", (250, 210, 60))}
    SHIPS_P2 = {0: ("narrow", (160, 80, 240)), 1: ("wide", (80, 240, 140)), 2: ("wide", (250, 140, 60))}
    BULLETS = ((255, 60, 200), (60, 230, 255))
    LASER_TYPES = ()
    DENSITY = 1.1


# ============================================================================ Ketsui
class KetsuiScene(CaveShooterScene):
    """Ketsui (2003), as in the game: two attack helicopters of our own over the city, the docks and the fortress, the
    lock-on that marks the nearest enemy, the combo time that drains, the bombs. / Ketsui : deux hélicoptères d'attaque à
    nous au-dessus de la ville, le verrouillage qui marque l'ennemi le plus proche, le temps de combo, les bombes."""
    THEME = "af_city"
    STAGES = ("af_city", "c44_sea", "s45_ground", "ddp_dock", "ddp_fortress", "am_fortress")
    SHIPS = {0: ("heli", (70, 90, 120)), 1: ("heli", (150, 70, 60))}
    SHIPS_P2 = {0: ("heli", (150, 70, 60)), 1: ("heli", (70, 90, 120))}
    SHIP_NAMES = {}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    BULLETS = ((255, 120, 60), (120, 160, 255))
    LASER_TYPES = ()
    DENSITY = 1.2

    def draw_over(self, screen, vals, now):
        """The lock-on: square marks on the nearest enemy of each ship. / Le verrouillage sur l'ennemi le plus proche."""
        S, pg = self.S, self.pg
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"]:
                continue
            x, y = self.pos(side, now)
            near = [e for e in self.enemies if not e.get("dead") and e["x"] > x]
            if not near:
                continue
            e = min(near, key=lambda f: (f["x"] - x) ** 2 + (f.get("yy", f["y"]) - y) ** 2)
            ex, ey = e["x"], e.get("yy", e["y"])
            r = S(40) + S(6) * math.sin(now * 12)
            col = (255, 80, 80) if side == "p1" else (255, 200, 80)
            w = max(2, S(3))
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                cx, cy = ex + sx * r, ey + sy * r
                pg.draw.line(screen, col, (cx, cy), (cx - sx * S(14), cy), w)
                pg.draw.line(screen, col, (cx, cy), (cx, cy - sy * S(14)), w)


# ============================================================================ Espgaluda
def winged_draw(body, wing):
    """A winged hero of our own seen from above, head to the right: the great wings of light spread, the cloak, the
    head. / Un héros ailé à nous vu du dessus : les grandes ailes de lumière, la cape, la tête."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.018))
        for sgn in (1, -1):
            for k, a in ((0, 230), (1, 150)):
                _poly(d, [(0.56, 0.5 + sgn * 0.06), (0.36 - k * 0.1, 0.5 + sgn * (0.48 - k * 0.08)), (0.2 - k * 0.08, 0.5 + sgn * (0.4 - k * 0.1)),
                          (0.4, 0.5 + sgn * 0.08)], W, H, _c(wing, a), LINE if k == 0 else None, ow)
        _poly(d, [(0.62, 0.42), (0.1, 0.4), (0.04, 0.5), (0.1, 0.6), (0.62, 0.58)], W, H, _c(_mix(body, (0, 0, 0), 0.3)), LINE, ow)
        d.rounded_rectangle([0.44 * W, 0.4 * H, 0.74 * W, 0.6 * H], radius=H * 0.08, fill=_c(body), outline=LINE, width=ow)
        d.ellipse([0.7 * W, 0.42 * H, 0.86 * W, 0.58 * H], fill=(236, 196, 160, 255), outline=LINE, width=ow)
        d.chord([0.7 * W, 0.42 * H, 0.86 * W, 0.58 * H], 90, 270, fill=(220, 200, 120, 255))
    return fn


class EspgaludaScene(CaveShooterScene):
    """Espgaluda (2003) and Espgaluda II (CV1000), as in the games: winged heroes of our own, the spirit stones read in
    the game, and when they drain the awakening: the bullets slow down and turn gold, the screen goes violet.
    / Espgaluda : des héros ailés à nous, les pierres d'esprit lues dans le jeu, et quand elles se vident l'éveil : les
    boulettes ralentissent et deviennent dorées, l'écran vire au violet."""
    THEME = "ddp_fortress"
    STAGES = ("ddp_fortress", "mm_base", "gw_lava", "dh_clouds", "am_fortress")
    SHIPS = {0: ("winged", (90, 80, 160))}
    SHIPS_P2 = {0: ("winged", (170, 70, 90))}
    SHIP_NAMES = {}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    BULLETS = ((255, 80, 140), (100, 160, 255))
    LASER = ((150, 255, 200), (230, 255, 240))
    DENSITY = 1.2

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.awake_t = -99.0
        self.awakenings = 0                                       # (tests)

    def plane_fn(self, side, kind):
        return winged_draw((90, 80, 160) if side == "p1" else (170, 70, 90), (140, 230, 255) if side == "p1" else (255, 170, 220))

    def update(self, vals, now):
        super().update(vals, now)
        for suf in ("", "_p2"):
            ch = self.changed(vals, "stones" + suf)
            if ch and ch[1] < ch[0]:                                  # the stones drain: awake / les pierres fondent
                if now - self.awake_t > 1.0:
                    self.awakenings += 1
                    self.fx.flash((200, 120, 255), 0.25, 0.4)
                self.awake_t = now
        awake = now - self.awake_t < 0.8
        self.slow += ((0.35 if awake else 1.0) - self.slow) * min(1.0, self.dt * 4)

    def bullet_img(self, kind):
        if self.slow < 0.7 and kind != 3:                             # gold while awake / dorées pendant l'éveil
            key = ("goldbullet", kind)
            s = self.imgs.get(key)
            if s is None:
                S = self.S
                size = (S(44), S(15)) if kind == 2 else (S(32), S(32)) if kind in (0, 1) else (S(24), S(24))
                s = self.img(key, size[0], size[1], needle_draw((255, 200, 60)) if kind == 2 else bullet_draw((255, 255, 230), (255, 190, 50)))
            return s
        return super().bullet_img(kind)

    def draw_over(self, screen, vals, now):
        if self.slow < 0.95:                                          # the violet of the awakening / le violet de l'éveil
            veil = self.imgs.get("awake")
            if veil is None:
                veil = self.imgs["awake"] = self.pg.Surface((self.W, self.H)).convert()
                veil.fill((120, 40, 170))
            veil.set_alpha(int(70 * (1 - self.slow) / 0.65))
            screen.blit(veil, (0, 0))

    def extra_hud(self, screen, vals, now):
        st = _n(vals.get("stones"))
        if st is not None:
            awake = self.slow < 0.7
            self.label(screen, (tr("ÉVEIL ", "AWAKENING ") if awake else "") + f"◆ {int(st)}", self.S(30), self.S(216), 30,
                       (220, 150, 255) if awake else (150, 220, 255), key="black")


# ============================================================================ Mushihime-sama
def beetle_draw(shell, horn):
    """A great horned beetle of our own seen from above, head to the right: the shell split in two, the long horn, the
    legs. / Un grand scarabée à corne à nous vu du dessus : la carapace fendue, la longue corne, les pattes."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.02))
        for sgn in (1, -1):                                               # legs / pattes
            for x in (0.36, 0.5, 0.64):
                d.line([(x * W, (0.5 + sgn * 0.2) * H), ((x - 0.06) * W, (0.5 + sgn * 0.44) * H)], fill=LINE, width=max(2, int(H * 0.04)))
        d.ellipse([0.14 * W, 0.22 * H, 0.7 * W, 0.78 * H], fill=_c(shell), outline=LINE, width=ow)
        d.line([(0.14 * W, 0.5 * H), (0.7 * W, 0.5 * H)], fill=LINE, width=ow)
        d.ellipse([0.24 * W, 0.3 * H, 0.42 * W, 0.42 * H], fill=(255, 255, 255, 110))
        d.ellipse([0.62 * W, 0.34 * H, 0.82 * W, 0.66 * H], fill=_c(_mix(shell, (0, 0, 0), 0.35)), outline=LINE, width=ow)
        _poly(d, [(0.78, 0.46), (0.99, 0.4), (0.96, 0.5), (0.99, 0.6), (0.78, 0.54)], W, H, _c(horn), LINE, ow)
    return fn


def bug_draw(body, light):
    """A small enemy bug of our own seen from above, head to the left: round shell, wings, glowing eyes. / Un petit
    insecte ennemi à nous, tête à gauche."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.03))
        for sgn in (1, -1):
            d.ellipse([0.3 * W, (0.5 + sgn * 0.22 - 0.2) * H, 0.92 * W, (0.5 + sgn * 0.22 + 0.2) * H], fill=(220, 230, 240, 110), outline=LINE,
                      width=max(1, ow // 2))
        d.ellipse([0.2 * W, 0.28 * H, 0.8 * W, 0.72 * H], fill=_c(body), outline=LINE, width=ow)
        d.ellipse([0.06 * W, 0.36 * H, 0.32 * W, 0.64 * H], fill=_c(_mix(body, (0, 0, 0), 0.4)), outline=LINE, width=ow)
        for y in (0.42, 0.58):
            d.ellipse([0.08 * W, (y - 0.05) * H, 0.16 * W, (y + 0.05) * H], fill=_c(light))
    return fn


class MushihimeScene(CaveShooterScene):
    """Mushihime-sama (2004) and its Futari, Black Label and Matsuri (CV1000): a great horned beetle of our own flies over
    the forest of the insects, the enemy bugs and their rain of pink and blue bullets. / Mushihime-sama : un grand
    scarabée à nous survole la forêt des insectes, les insectes ennemis et leur pluie de boulettes."""
    THEME = "ct_forest"
    STAGES = ("ct_forest", "ncm_jungle", "pk_savanna", "gw_lava", "dh_clouds")
    SHIPS = {0: ("beetle", (200, 150, 40))}
    SHIPS_P2 = {0: ("beetle", (60, 140, 200))}
    SHIP_NAMES = {}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    BULLETS = ((255, 90, 170), (110, 170, 255))
    LASER = ((255, 210, 90), (255, 250, 220))
    DENSITY = 1.3
    ROTOR = False

    def plane_fn(self, side, kind):
        return beetle_draw((200, 150, 40) if side == "p1" else (60, 140, 200), (120, 70, 20) if side == "p1" else (30, 70, 120))

    def enemy_fn(self, kind):
        if kind == "bomber":
            return beetle_draw((110, 60, 120), (60, 30, 70))
        if kind == "heli":
            return bug_draw((70, 120, 70), (255, 220, 60))
        return bug_draw((120, 80, 60) if kind == "jet" else (90, 60, 110), (255, 90, 60))

    def enemy_surf(self, kind="jet", shadow=False):
        """The big beetle faces left like the other enemies. / Le gros scarabée regarde à gauche comme les autres."""
        if kind != "bomber":
            return super().enemy_surf(kind, shadow)
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            s = self.img(("enemyimg", kind), S(170), S(150), self.enemy_fn(kind), flip=True)
            if shadow:
                s = self.shadow_of(self.pg, s, 70)
            self.imgs[key] = s
        return s


# ============================================================================ Ibara, Pink Sweets
class IbaraScene(CaveShooterScene):
    """Ibara (2005), Ibara Kuro Black Label and Pink Sweets (CV1000): fighters of our own high in the sky, over the clouds
    and the fortresses, the rain of bullets in rose and blue. / Ibara et Pink Sweets : des chasseurs à nous haut dans le
    ciel, au-dessus des nuages et des forteresses."""
    THEME = "c19_sky"
    STAGES = ("c19_sky", "ddp_fortress", "dh_clouds", "ddp_dock", "am_fortress")
    SHIPS = {0: ("narrow", (200, 60, 90))}
    SHIPS_P2 = {0: ("narrow", (70, 90, 200))}
    SHIP_NAMES = {}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    BULLETS = ((255, 100, 170), (120, 180, 255))
    DENSITY = 1.2


class PinkSweetsScene(IbaraScene):
    THEME = "dh_clouds"
    STAGES = ("dh_clouds", "c19_sky", "fv_neon", "ddp_fortress")
    SHIPS = {0: ("wide", (240, 110, 180))}
    SHIPS_P2 = {0: ("wide", (120, 200, 240))}
    BULLETS = ((255, 120, 200), (255, 220, 90))


# ============================================================================ Muchi Muchi Pork!
def pig_draw(body):
    """A flying pig of our own seen from above, snout to the right, little wings. / Un cochon volant à nous, groin à droite."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.02))
        b, dk = _c(body), _c(_mix(body, (0, 0, 0), 0.25))
        for sgn in (1, -1):                                               # the little wings / les petites ailes
            d.ellipse([0.3 * W, (0.5 + sgn * 0.3 - 0.16) * H, 0.6 * W, (0.5 + sgn * 0.3 + 0.16) * H], fill=(250, 250, 255, 230), outline=LINE,
                      width=ow)
        d.ellipse([0.1 * W, 0.24 * H, 0.86 * W, 0.76 * H], fill=b, outline=LINE, width=ow)
        d.ellipse([0.8 * W, 0.4 * H, 0.98 * W, 0.6 * H], fill=dk, outline=LINE, width=ow)          # the snout / le groin
        for y in (0.46, 0.54):
            d.ellipse([0.88 * W, (y - 0.025) * H, 0.92 * W, (y + 0.025) * H], fill=LINE)
        for y in (0.34, 0.66):
            d.ellipse([0.62 * W, (y - 0.06) * H, 0.72 * W, (y + 0.06) * H], fill=dk, outline=LINE, width=ow)   # ears / oreilles
        d.line([(0.1 * W, 0.5 * H), (0.02 * W, 0.44 * H)], fill=LINE, width=max(2, int(H * 0.04)))
    return fn


class MuchiPorkScene(CaveShooterScene):
    """Muchi Muchi Pork! (2007, CV1000): flying pigs of our own over the countryside and the savanna, a rain of bullets in
    candy colours. / Muchi Muchi Pork! : des cochons volants à nous au-dessus de la campagne, des boulettes acidulées."""
    THEME = "ddp_country"
    STAGES = ("ddp_country", "pk_savanna", "dh_clouds", "fv_neon")
    SHIPS = {0: ("pig", (250, 170, 190))}
    SHIPS_P2 = {0: ("pig", (250, 210, 150))}
    SHIP_NAMES = {}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    BULLETS = ((255, 120, 200), (120, 220, 255))
    LASER_TYPES = ()

    def plane_fn(self, side, kind):
        return pig_draw((250, 170, 190) if side == "p1" else (250, 210, 150))


# ============================================================================ seen from the side / vus de profil
def caped_flyer_draw(dress, wing):
    """A gothic flyer of our own seen from the side, facing right: the dark dress that floats, the bat wings, the pale
    face. / Une silhouette gothique à nous, de profil : la robe sombre, les ailes de chauve-souris, le visage pâle."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.02))
        _poly(d, [(0.5, 0.4), (0.18, 0.04), (0.28, 0.26), (0.1, 0.2), (0.24, 0.42), (0.46, 0.48)], W, H, _c(wing), LINE, ow)
        _poly(d, [(0.62, 0.38), (0.66, 0.78), (0.2, 0.92), (0.34, 0.62), (0.5, 0.4)], W, H, _c(dress), LINE, ow)
        d.ellipse([0.58 * W, 0.12 * H, 0.84 * W, 0.42 * H], fill=(240, 222, 210, 255), outline=LINE, width=ow)
        _poly(d, [(0.56, 0.16), (0.86, 0.1), (0.8, 0.24), (0.62, 0.3), (0.5, 0.4)], W, H, _c(_mix(dress, (0, 0, 0), 0.3)), LINE, ow)
        d.line([(0.62 * W, 0.5 * H), (0.96 * W, 0.46 * H)], fill=(200, 180, 120, 255), width=max(2, int(H * 0.05)))   # a wand
        d.ellipse([0.92 * W, 0.4 * H, 1.0 * W, 0.52 * H], fill=(255, 220, 120, 255))
    return fn


def bat_draw(body):
    """A big bat of our own seen from the side, facing left. / Une grosse chauve-souris à nous, de profil."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.025))
        for up in (1, -1):
            _poly(d, [(0.5, 0.5), (0.9, 0.5 - up * 0.42), (0.78, 0.5 - up * 0.2), (0.96, 0.5 - up * 0.16), (0.6, 0.5)], W, H, _c(body), LINE, ow)
        d.ellipse([0.2 * W, 0.34 * H, 0.62 * W, 0.66 * H], fill=_c(_mix(body, WHITE, 0.15)), outline=LINE, width=ow)
        d.ellipse([0.08 * W, 0.36 * H, 0.32 * W, 0.6 * H], fill=_c(_mix(body, WHITE, 0.15)), outline=LINE, width=ow)
        d.ellipse([0.12 * W, 0.42 * H, 0.17 * W, 0.48 * H], fill=(255, 60, 60, 255))
    return fn


def ghost_draw(d, W, H):
    """A ghost of our own, a white sheet with a wavy tail, facing left. / Un fantôme à nous, un drap blanc."""
    ow = max(1, int(W * 0.02))
    pts = [(0.1 * W, 0.5 * H), (0.3 * W, 0.12 * H), (0.6 * W, 0.16 * H), (0.98 * W, 0.4 * H), (0.84 * W, 0.56 * H), (0.98 * W, 0.7 * H),
           (0.78 * W, 0.76 * H), (0.84 * W, 0.92 * H), (0.4 * W, 0.86 * H)]
    d.polygon(pts, fill=(236, 236, 250, 230), outline=LINE)
    d.line(pts + [pts[0]], fill=LINE, width=ow)
    for x in (0.26, 0.4):
        d.ellipse([(x - 0.04) * W, 0.36 * H, (x + 0.04) * W, 0.5 * H], fill=(30, 20, 50, 255))


class DeathsmilesScene(CaveShooterScene):
    """Deathsmiles (2007) and its MegaBlack Label (CV1000), seen from the side as in the games: a gothic flyer of our own
    over the graveyards, the dark forests and the burning lands, the bats and the ghosts. / Deathsmiles, de profil comme
    dans les jeux : une silhouette gothique à nous au-dessus des cimetières, des forêts sombres, des terres en feu."""
    SIDE = True
    THEME = "nd_grave"
    STAGES = ("nd_grave", "cs_forest", "em_city", "th_fire", "gg_grave")
    SHIPS = {0: ("flyer", (60, 40, 80))}
    SHIPS_P2 = {0: ("flyer", (110, 30, 50))}
    SHIP_NAMES = {}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    BULLETS = ((255, 110, 60), (170, 120, 255))
    LASER = ((255, 170, 120), (255, 240, 220))
    SIZES = {"jet": (90, 70), "prop": (80, 80), "heli": (100, 80), "bomber": (180, 150)}

    def plane_fn(self, side, kind):
        return caped_flyer_draw((60, 40, 80) if side == "p1" else (110, 30, 50), (40, 30, 50) if side == "p1" else (70, 20, 30))

    def plane_surf(self, side, kind, shadow=False):
        S = self.S
        key = ("plane", side, kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            s = self.imgs[key] = self.img(("planeimg", side, kind), S(130), S(120), self.plane_fn(side, kind))
        return s

    def enemy_fn(self, kind):
        if kind == "bomber":
            return bat_draw((60, 50, 70))
        if kind == "prop":
            return ghost_draw
        return bat_draw((80, 50, 60) if kind == "jet" else (50, 50, 80))

    def update(self, vals, now):
        super().update(vals, now)
        for side, suf in (("p1", ""), ("p2", "_p2")):                    # the energy that drops: a hit / un coup reçu
            ch = self.changed(vals, "energy" + suf)
            if ch and ch[1] < ch[0] and self.ships[side]["in"]:
                x, y = self.pos(side, now)
                self.fx.sparks(x, y, 16, (220, 180, 255), (200, 600), (0, 360), (0.2, 0.5), 0, "front", 3, 22)
                self.fx.shake(5, 0.25)

    def extra_hud(self, screen, vals, now):
        """The energy read in the game (MAME cheat database, 1.31). / L'énergie lue dans le jeu."""
        for side, suf, x in (("p1", "", self.S(30)), ("p2", "_p2", self.W - self.S(250))):
            e = _n(vals.get("energy" + suf))
            if e is not None and (side == "p1" or self.p2_in(vals)):
                self.gauge(screen, tr("ÉNERGIE", "ENERGY"), e / 100.0, x, self.S(160), 220, (190, 140, 255) if e > 25 else RED)


class AkaiKatanaScene(CaveShooterScene):
    """Akai Katana (2010, CV1000), seen from the side as in the game: fighters of the age of steam of our own over the
    old towns, the coasts and the canyons, the enemy planes and their bullets. / Akai Katana, de profil comme dans le jeu :
    des chasseurs de l'âge de la vapeur à nous au-dessus des vieilles villes, des côtes et des canyons."""
    SIDE = True
    THEME = "pg_village"
    STAGES = ("pg_village", "ef_coast", "un_canyon", "ca_city")
    SHIPS = {0: ("steam", (180, 50, 40))}
    SHIPS_P2 = {0: ("steam", (60, 90, 160))}
    SHIP_NAMES = {}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    BULLETS = ((255, 90, 70), (110, 170, 255))
    LASER = ((255, 120, 90), (255, 230, 210))
    SIZES = {"jet": (110, 64), "prop": (110, 64), "heli": (110, 64), "bomber": (200, 120)}

    def plane_fn(self, side, kind):
        return pg_plane_draw((180, 50, 40) if side == "p1" else (60, 90, 160), (230, 210, 170))

    def plane_surf(self, side, kind, shadow=False):
        S = self.S
        key = ("plane", side, kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            s = self.imgs[key] = self.img(("planeimg", side, kind), S(160), S(90), self.plane_fn(side, kind))
        return s

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            w, h = self.SIZES.get(kind, (110, 64))
            body = {"bomber": (70, 70, 64), "heli": (90, 70, 50)}.get(kind, (60, 64, 70))
            s = self.imgs[key] = self.img(("enemyimg", kind), S(w), S(h), pg_plane_draw(body, (120, 110, 100)), flip=True)
        return s


# ============================================================================ the shoot'em ups of other companies on the Cave board
class HotdogStormScene(CaveShooterScene):
    """Hotdog Storm (Marble, 1996, on the Cave board): our jet fighters over the sea and the clouds. / Nos chasseurs
    au-dessus de la mer et des nuages."""
    THEME = "c44_sea"
    STAGES = ("c44_sea", "c19_sky", "ddp_country", "ddp_fortress")
    SHIPS = {0: ("narrow", (60, 120, 220))}
    SHIPS_P2 = {0: ("narrow", (220, 80, 60))}
    SHIP_NAMES = {}
    SHIP_DEFAULT = {"p1": 0, "p2": 0}
    LASER_TYPES = ()
    DENSITY = 0.6


class MazingerScene(HotdogStormScene):
    """Mazinger Z (Banpresto, 1994, on the Cave board): a jet fighter of our own over the city, the energy read in the
    game. / Un chasseur à nous au-dessus de la ville, l'énergie lue dans le jeu."""
    THEME = "af_city"
    STAGES = ("af_city", "ddp_fortress", "s45_ground")
    SHIPS = {0: ("wide", (200, 50, 50))}
    SHIPS_P2 = {0: ("wide", (60, 90, 200))}

    def update(self, vals, now):
        super().update(vals, now)
        for side, suf in (("p1", ""), ("p2", "_p2")):                    # the energy that drops: a hit / un coup reçu
            ch = self.changed(vals, "energy" + suf)
            if ch and ch[1] < ch[0] and self.ships[side]["in"]:
                x, y = self.pos(side, now)
                self.fx.sparks(x, y, 16, (255, 220, 140), (200, 600), (0, 360), (0.2, 0.5), 0, "front", 3, 22)
                self.fx.shake(5, 0.25)

    def extra_hud(self, screen, vals, now):
        e = _n(vals.get("energy"))
        if e is not None:
            self.gauge(screen, tr("ÉNERGIE", "ENERGY"), e / 100.0, self.S(30), self.S(160), 220, (120, 220, 255) if e > 25 else RED)


class AirGalletScene(HotdogStormScene):
    """Air Gallet (Gazelle, 1996, on the Cave board): our jet fighters over the countryside and the coasts. / Nos
    chasseurs au-dessus de la campagne et des côtes."""
    THEME = "ddp_country"
    STAGES = ("ddp_country", "c41_coast", "ddp_dock", "ddp_fortress")
    SHIPS = {0: ("wide", (90, 140, 90))}
    SHIPS_P2 = {0: ("wide", (170, 120, 70))}


# ============================================================================ puzzles
class UoPokoScene(PuzzleBobble2Scene):
    """Puzzle Uo Poko (1998): the bubbles shot from the launcher at the bottom of the sea, the bubble ready read in the
    game, the stage. / Les bulles tirées au fond de la mer, la bulle prête lue dans le jeu, le niveau."""
    THEME = "pul_water"

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "stage")
        if ch and ch[1] > 0:                                              # a new stage: new boards / nouveaux plateaux
            self.slam(f"STAGE {int(ch[1])}", GOLD, now, 1.6)
            for b in self.boards.values():
                self._clear(b, now, 3 + min(3, int(ch[1]) // 8))


class MushiTamaScene(UoPokoScene):
    """Puzzle! Mushihime-Tama (2005, CV1000): the bubbles shot over the forest. / Les bulles tirées au-dessus de la forêt."""
    THEME = "ct_forest"


# ============================================================================ the beat'em ups on the Cave board / les beat'em up
# shown like the Capcom ones, two player panels on a backdrop of the game's kind / comme ceux de Capcom, deux panneaux de joueur
PANEL_SPECS = {"sailormn": dict(theme="bf_street", hit="fist", names=True, gauge=_g(VIE, (255, 120, 200), (60, 30, 50))),
               "gaia": dict(theme="mn_city", hit="slash", gauge=_g(VIE, (255, 220, 40), (170, 30, 30))),
               "theroes": dict(theme="ff_slum", hit="fist", gauge=_g(VIE, (90, 220, 255), (30, 40, 60)))}
PANELS = {key: type(f"PanelScene_{key}", (PanelScene,), {"THEME": spec["theme"], "SPEC": spec}) for key, spec in PANEL_SPECS.items()}

SCENES = {"ddonpach": DoDonPachiScene, "donpachi": DonPachiScene, "ddp3": DaiOuJouScene, "ddp2": DoDonPachi2Scene,
          "ddpdfk": DaiFukkatsuScene, "dfkbl": DaiFukkatsuScene, "ddpsdoj": DaiFukkatsuScene, "esprade": EspRadeScene,
          "guwange": GuwangeScene, "feversos": FeveronScene, "ket": KetsuiScene, "espgal": EspgaludaScene, "espgal2": EspgaludaScene,
          "mushisam": MushihimeScene, "futari15": MushihimeScene, "futaribl": MushihimeScene, "matsuri15": MushihimeScene,
          "ibara": IbaraScene, "ibarablk": IbaraScene, "pinkswts": PinkSweetsScene, "mmpork": MuchiPorkScene, "deathsml": DeathsmilesScene,
          "dsmbl": DeathsmilesScene, "akatana": AkaiKatanaScene, "hotdogst": HotdogStormScene, "mazinger": MazingerScene,
          "agallet": AirGalletScene, "uopoko": UoPokoScene, "mushitam": MushiTamaScene}
SCENES.update(PANELS)
