"""HD scenes of the Capcom CPS shoot'em ups (1.30), each drawn after screenshots of its game: 1941, 1944, 19XX, Varth,
U.N. Squadron, Carrier Air Wing, Forgotten Worlds, Giga Wing, Progear, Mars Matrix, Dimahoo and Eco Fighters (Mercs is shown
with player panels, hd_panels.py).
Each game has its own animated backdrop and reacts to the values read in its memory: the energy that drops is a hit
taken, a life lost blows up, a bomb spent sweeps the screen, the weapon read in the game is named. The planes, the
heroes, the enemies and the machines are creations of the program in the spirit of the games (the planes of the war
are generic types of the time), no picture comes from a game.

Scènes HD des shoot'em ups Capcom CPS (1.30), chacune dessinée d'après des captures de son jeu. Chaque jeu a son décor
animé et réagit aux valeurs lues dans sa mémoire : l'énergie qui baisse est un coup reçu, une vie perdue explose, une
bombe nettoie l'écran, l'arme lue dans le jeu est nommée. Les avions, les héros, les ennemis et les machines sont des
créations du programme dans l'esprit des jeux, aucune image ne vient d'un jeu.
"""

import math

from .hd_games import CREAM, GOLD, RED, WHITE, _clamp, _mix, _n
from .hd_games3 import DARK, AeroFightersScene, _poly, bomber_draw, jet_draw, prop_plane_draw
from .hd_games5 import SideShooterScene, side_heli_draw
from .hd_games6 import portrait_draw
from .hd_games10 import gunboat_draw
from .hd_themes13 import GW_LANES, MM_LANES, SEA41_LANES, SEA44_LANES, THEMES, VT_LANES
from .i18n import tr

LINE = DARK + (255,)


def _ow(W):
    return max(1, int(W * 0.014))


def _c(col, a=255):
    return tuple(col[:3]) + (a,)


# ============================================================================ the planes / les avions
def lightning_draw(body, accent):
    """A twin-boom fighter of the war seen from above, nose to the right: two engine booms with their propellers, the
    short pod of the pilot between them, the tail joining the booms. / Un chasseur bipoutre de la guerre vu du dessus."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh, acc = _c(body), _c(_mix(body, (0, 0, 0), 0.25)), _c(accent)
        _poly(d, [(0.62, 0.04), (0.66, 0.04), (0.6, 0.96), (0.56, 0.96)], W, H, sh, LINE, ow)            # the wing / l'aile
        _poly(d, [(0.66, 0.04), (0.6, 0.04), (0.5, 0.5), (0.6, 0.96), (0.66, 0.96), (0.58, 0.5)], W, H, b, LINE, ow)
        for y in (0.32, 0.68):                                                                         # the booms / les poutres
            _poly(d, [(0.82, y), (0.78, y - 0.06), (0.1, y - 0.035), (0.1, y + 0.035), (0.78, y + 0.06)], W, H, b, LINE, ow)
            d.ellipse([0.05 * W, (y - 0.09) * H, 0.13 * W, (y + 0.09) * H], fill=sh, outline=LINE, width=ow)     # the fins / dérives
            d.ellipse([0.8 * W, (y - 0.2) * H, 0.86 * W, (y + 0.2) * H], fill=(230, 230, 236, 70))             # propeller / hélice
            d.ellipse([0.8 * W, (y - 0.025) * H, 0.86 * W, (y + 0.025) * H], fill=acc)
        _poly(d, [(0.08, 0.3), (0.14, 0.3), (0.14, 0.7), (0.08, 0.7)], W, H, sh, LINE, ow)                 # the tail / l'empennage
        _poly(d, [(0.9, 0.5), (0.84, 0.44), (0.5, 0.45), (0.46, 0.5), (0.5, 0.55), (0.84, 0.56)], W, H, b, LINE, ow)   # the pod / la nacelle
        d.ellipse([0.64 * W, 0.465 * H, 0.78 * W, 0.535 * H], fill=(120, 200, 240, 255), outline=LINE, width=ow)
        for y in (0.08, 0.92):
            d.line([(0.59 * W, y * H), (0.63 * W, y * H)], fill=acc, width=max(2, int(H * 0.035)))
        d.ellipse([0.88 * W, 0.48 * H, 0.92 * W, 0.52 * H], fill=acc)
    return fn


def shinden_draw(body, accent):
    """A canard fighter of the war seen from above, nose to the right: the wing at the back, little wings at the nose,
    the propeller pushing at the tail. / Un chasseur canard vu du dessus : l'aile à l'arrière, l'hélice qui pousse."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh, acc = _c(body), _c(_mix(body, (0, 0, 0), 0.25)), _c(accent)
        for sgn in (1, -1):
            _poly(d, [(0.44, 0.5 + sgn * 0.05), (0.2, 0.5 + sgn * 0.44), (0.12, 0.5 + sgn * 0.44), (0.2, 0.5 + sgn * 0.05)], W, H, sh, LINE, ow)
            _poly(d, [(0.86, 0.5 + sgn * 0.03), (0.8, 0.5 + sgn * 0.17), (0.75, 0.5 + sgn * 0.17), (0.77, 0.5 + sgn * 0.03)], W, H, sh, LINE, ow)
            _poly(d, [(0.22, 0.5 + sgn * 0.3), (0.12, 0.5 + sgn * 0.3), (0.12, 0.5 + sgn * 0.27), (0.22, 0.5 + sgn * 0.27)], W, H, LINE)
            d.line([(0.16 * W, (0.5 + sgn * 0.4) * H), (0.22 * W, (0.5 + sgn * 0.4) * H)], fill=acc, width=max(2, int(H * 0.035)))
        _poly(d, [(0.94, 0.5), (0.86, 0.44), (0.12, 0.45), (0.08, 0.5), (0.12, 0.55), (0.86, 0.56)], W, H, b, LINE, ow)
        d.ellipse([0.52 * W, 0.465 * H, 0.64 * W, 0.535 * H], fill=(120, 200, 240, 255), outline=LINE, width=ow)
        d.ellipse([0.03 * W, 0.28 * H, 0.08 * W, 0.72 * H], fill=(230, 230, 236, 70))
        d.ellipse([0.03 * W, 0.47 * H, 0.08 * W, 0.53 * H], fill=acc)
    return fn


def heavy_bomber_draw(body):
    """A big bomber with four engines seen from above, nose to the left: a long wing, a round nose of glass, the tail.
    / Un gros bombardier à quatre moteurs vu du dessus, nez à gauche."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh = _c(body), _c(_mix(body, (0, 0, 0), 0.22))
        _poly(d, [(0.36, 0.02), (0.44, 0.02), (0.5, 0.5), (0.44, 0.98), (0.36, 0.98), (0.4, 0.5)], W, H, sh, LINE, ow)
        for y in (0.2, 0.36, 0.64, 0.8):
            _poly(d, [(0.22, y), (0.26, y - 0.04), (0.46, y - 0.035), (0.46, y + 0.035), (0.26, y + 0.04)], W, H, b, LINE, ow)
            d.ellipse([0.17 * W, (y - 0.09) * H, 0.21 * W, (y + 0.09) * H], fill=(230, 230, 236, 70))
        _poly(d, [(0.04, 0.5), (0.1, 0.44), (0.88, 0.46), (0.92, 0.5), (0.88, 0.54), (0.1, 0.56)], W, H, b, LINE, ow)
        _poly(d, [(0.8, 0.5), (0.9, 0.3), (0.96, 0.3), (0.94, 0.5), (0.96, 0.7), (0.9, 0.7)], W, H, sh, LINE, ow)
        d.ellipse([0.04 * W, 0.46 * H, 0.12 * W, 0.54 * H], fill=(150, 210, 240, 255), outline=LINE, width=ow)
        for x in (0.3, 0.6):
            d.ellipse([(x - 0.02) * W, 0.47 * H, (x + 0.02) * W, 0.53 * H], fill=(40, 40, 46, 255))
    return fn


def destroyer_draw(d, W, H):
    """A small grey warship seen from the sky, bow to the left, for the ground targets of the sea levels.
    / Un petit navire de guerre gris vu du ciel, proue à gauche."""
    ow = _ow(W)
    _poly(d, [(0.02, 0.5), (0.18, 0.12), (0.96, 0.16), (0.98, 0.5), (0.96, 0.84), (0.18, 0.88)], W, H, (110, 114, 122, 255), LINE, ow)
    _poly(d, [(0.4, 0.3), (0.66, 0.3), (0.66, 0.7), (0.4, 0.7)], W, H, (150, 154, 160, 255), LINE, ow)
    for x in (0.22, 0.82):
        d.ellipse([(x - 0.06) * W, 0.32 * H, (x + 0.06) * W, 0.68 * H], fill=(90, 94, 100, 255), outline=LINE, width=ow)
        d.line([(x * W, 0.5 * H), ((x - 0.14) * W, 0.5 * H)], fill=LINE, width=max(2, int(H * 0.06)))


def side_jet_draw(body, accent, canopy=(110, 200, 245), big=False):
    """A jet fighter of our own seen from the side, nose to the right: the long fuselage, the air intake, the swept
    wing, the fin, the bubble canopy, the exhaust. / Un chasseur à réaction à nous, de profil, nez à droite."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh, acc = _c(body), _c(_mix(body, (0, 0, 0), 0.3)), _c(accent)
        _poly(d, [(0.08, 0.5), (0.04, 0.12), (0.16, 0.12), (0.3, 0.46)], W, H, b, LINE, ow)                    # the fin / la dérive
        _poly(d, [(0.04, 0.62), (0.08, 0.44), (0.7, 0.4), (0.9, 0.48), (0.99, 0.56), (0.88, 0.62), (0.5, 0.7), (0.1, 0.72)],
              W, H, b, LINE, ow)
        _poly(d, [(0.3, 0.6), (0.62, 0.58), (0.4, 0.86), (0.28, 0.86)] if not big else [(0.24, 0.6), (0.62, 0.58), (0.36, 0.9), (0.2, 0.9)],
              W, H, sh, LINE, ow)                                                                            # the wing / l'aile
        _poly(d, [(0.52, 0.56), (0.62, 0.55), (0.6, 0.68), (0.5, 0.68)], W, H, sh, LINE, ow)                   # the intake / l'entrée d'air
        d.chord([0.62 * W, 0.28 * H, 0.84 * W, 0.62 * H], 180, 360, fill=_c(canopy), outline=LINE, width=ow)
        d.line([(0.12 * W, 0.56 * H), (0.82 * W, 0.53 * H)], fill=acc, width=max(2, int(H * 0.04)))
        _poly(d, [(0.04, 0.5), (0.04, 0.68), (0.0, 0.66), (0.0, 0.52)], W, H, (60, 60, 66, 255), LINE, ow)       # exhaust / tuyère
    return fn


def flyer_draw(frame):
    """Our flying soldier of our own: lying in the air, the legs behind, the jet pack, the big gun forward.
    / Notre soldat volant à nous : allongé dans les airs, le réacteur dorsal, le gros fusil devant."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.02))
        skin, suit, pack = (226, 176, 136, 255), (60, 90, 170, 255), (150, 150, 160, 255)
        kick = 0.04 if frame % 2 else -0.02
        _poly(d, [(0.06, 0.5 + kick), (0.12, 0.42 + kick), (0.42, 0.44), (0.42, 0.6), (0.12, 0.62 + kick)], W, H, (50, 60, 110, 255), LINE, ow)
        _poly(d, [(0.04, 0.62 + kick), (0.12, 0.6 + kick), (0.12, 0.72 + kick), (0.02, 0.72 + kick)], W, H, (60, 40, 30, 255), LINE, ow)
        d.rounded_rectangle([0.36 * W, 0.36 * H, 0.7 * W, 0.66 * H], radius=W * 0.06, fill=suit, outline=LINE, width=ow)
        d.rounded_rectangle([0.4 * W, 0.18 * H, 0.62 * W, 0.4 * H], radius=W * 0.04, fill=pack, outline=LINE, width=ow)      # the pack
        d.ellipse([0.68 * W, 0.26 * H, 0.84 * W, 0.56 * H], fill=skin, outline=LINE, width=ow)
        _poly(d, [(0.68, 0.32), (0.86, 0.26), (0.84, 0.36), (0.7, 0.4)], W, H, (230, 200, 60, 255), LINE, ow)             # headband
        _poly(d, [(0.6, 0.56), (0.98, 0.54), (0.98, 0.64), (0.6, 0.68)], W, H, (90, 92, 104, 255), LINE, ow)               # the gun
        d.ellipse([0.62 * W, 0.58 * H, 0.72 * W, 0.7 * H], fill=skin, outline=LINE, width=ow)
    return fn


def satellite_draw(d, W, H):
    """The little orbiting gun module of the flying soldier. / Le petit module de tir qui tourne autour du soldat."""
    ow = max(1, int(W * 0.05))
    d.ellipse([0.1 * W, 0.1 * H, 0.9 * W, 0.9 * H], fill=(200, 200, 214, 255), outline=LINE, width=ow)
    d.ellipse([0.3 * W, 0.3 * H, 0.7 * W, 0.7 * H], fill=(240, 90, 60, 255), outline=LINE, width=ow)
    d.line([(0.5 * W, 0.5 * H), (0.98 * W, 0.5 * H)], fill=LINE, width=max(2, int(H * 0.14)))


def lizard_draw(frame):
    """A golden winged lizard warrior of our own, flying, facing right. / Un guerrier lézard ailé doré à nous."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.02))
        gold, dark = (220, 170, 50, 255), (150, 100, 30, 255)
        up = frame % 2
        wing = [(0.4, 0.4), (0.2, 0.02 if up else 0.2), (0.56, 0.3)] if up else [(0.4, 0.44), (0.16, 0.7), (0.56, 0.5)]
        _poly(d, wing, W, H, (200, 120, 60, 220), LINE, ow)
        _poly(d, [(0.02, 0.72), (0.2, 0.56), (0.4, 0.5), (0.3, 0.66)], W, H, dark, LINE, ow)               # the tail / la queue
        d.ellipse([0.28 * W, 0.4 * H, 0.66 * W, 0.7 * H], fill=gold, outline=LINE, width=ow)
        d.ellipse([0.6 * W, 0.26 * H, 0.86 * W, 0.5 * H], fill=gold, outline=LINE, width=ow)
        _poly(d, [(0.82, 0.36), (0.98, 0.4), (0.84, 0.46)], W, H, gold, LINE, ow)
        d.ellipse([0.72 * W, 0.32 * H, 0.77 * W, 0.37 * H], fill=(200, 30, 30, 255))
        _poly(d, [(0.56, 0.6), (0.9, 0.62), (0.9, 0.68), (0.56, 0.68)], W, H, (120, 120, 130, 255), LINE, ow)   # a spear / une lance
    return fn


def pg_plane_draw(body, wing):
    """A steam age fighter of our own seen from the side, nose to the right: the big propeller, the brass engine and
    its chimney, the cloth wings, the pilot in the open seat. / Un chasseur de l'âge de la vapeur à nous, de profil."""
    def fn(d, W, H):
        ow = _ow(W)
        b, wg = _c(body), _c(wing)
        _poly(d, [(0.04, 0.42), (0.02, 0.16), (0.14, 0.16), (0.22, 0.44)], W, H, wg, LINE, ow)
        d.rounded_rectangle([0.06 * W, 0.4 * H, 0.84 * W, 0.68 * H], radius=H * 0.12, fill=b, outline=LINE, width=ow)
        _poly(d, [(0.3, 0.5), (0.66, 0.5), (0.56, 0.9), (0.36, 0.9)], W, H, wg, LINE, ow)
        d.rounded_rectangle([0.62 * W, 0.34 * H, 0.86 * W, 0.72 * H], radius=H * 0.06, fill=(200, 160, 70, 255), outline=LINE, width=ow)
        d.rectangle([0.66 * W, 0.12 * H, 0.72 * W, 0.36 * H], fill=(60, 56, 54, 255), outline=LINE, width=ow)      # chimney / cheminée
        d.ellipse([0.42 * W, 0.24 * H, 0.54 * W, 0.44 * H], fill=(226, 176, 136, 255), outline=LINE, width=ow)    # the pilot
        d.ellipse([0.42 * W, 0.22 * H, 0.54 * W, 0.32 * H], fill=(120, 70, 40, 255))
        d.ellipse([0.86 * W, 0.08 * H, 0.94 * W, 0.92 * H], fill=(230, 230, 236, 80))
        d.ellipse([0.86 * W, 0.46 * H, 0.94 * W, 0.58 * H], fill=(90, 70, 50, 255))
    return fn


def eco_ship_draw(d, W, H):
    """Our little ecological fighter of our own, seen from the side: a round white pod, a green band, the glass dome.
    / Notre petit vaisseau écologique à nous : une capsule ronde blanche, une bande verte, un dôme de verre."""
    ow = _ow(W)
    d.ellipse([0.1 * W, 0.24 * H, 0.86 * W, 0.84 * H], fill=(236, 240, 246, 255), outline=LINE, width=ow)
    d.chord([0.1 * W, 0.24 * H, 0.86 * W, 0.84 * H], 20, 160, fill=(80, 180, 90, 255), outline=LINE, width=ow)
    d.ellipse([0.4 * W, 0.12 * H, 0.66 * W, 0.44 * H], fill=(140, 220, 250, 255), outline=LINE, width=ow)
    _poly(d, [(0.1, 0.5), (0.0, 0.4), (0.0, 0.64)], W, H, (250, 170, 60, 255), LINE, ow)


def polluter_draw(frame):
    """A polluting robot of our own: a green shell with two big eyes and little legs that kick. / Un robot pollueur à
    nous : une carapace verte, deux gros yeux, des petites pattes."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.03))
        k = 0.05 if frame % 2 else 0.0
        for x in (0.3, 0.55):
            d.line([(x * W, 0.66 * H), ((x - 0.08) * W, (0.86 + k) * H)], fill=LINE, width=max(2, int(W * 0.04)))
        d.ellipse([0.06 * W, 0.2 * H, 0.94 * W, 0.78 * H], fill=(60, 160, 70, 255), outline=LINE, width=ow)
        for i in range(3):
            d.arc([(0.16 + i * 0.22) * W, 0.28 * H, (0.38 + i * 0.22) * W, 0.6 * H], 200, 340, fill=(30, 100, 40, 255), width=ow)
        for x in (0.62, 0.8):
            d.ellipse([(x - 0.08) * W, 0.3 * H, (x + 0.08) * W, 0.5 * H], fill=(255, 255, 255, 255), outline=LINE, width=ow)
            d.ellipse([(x - 0.08) * W, 0.36 * H, (x + 0.0) * W, 0.46 * H], fill=LINE)
        d.rectangle([0.4 * W, 0.04 * H, 0.48 * W, 0.24 * H], fill=(90, 80, 70, 255), outline=LINE, width=ow)      # smoke stack
    return fn


def mm_ship_draw(body, accent):
    """Our mech fighter of our own seen from above, nose to the right: a heavy armoured hull, two shoulder pods, the
    cockpit, the guns forward. / Notre chasseur mécanique à nous vu du dessus, nez à droite."""
    def fn(d, W, H):
        ow = _ow(W)
        b, sh, acc = _c(body), _c(_mix(body, (0, 0, 0), 0.3)), _c(accent)
        for sgn in (1, -1):
            _poly(d, [(0.7, 0.5 + sgn * 0.12), (0.62, 0.5 + sgn * 0.42), (0.3, 0.5 + sgn * 0.42), (0.2, 0.5 + sgn * 0.14)], W, H, sh, LINE, ow)
            d.rounded_rectangle([0.32 * W, (0.5 + sgn * 0.3 - 0.08) * H, 0.6 * W, (0.5 + sgn * 0.3 + 0.08) * H], radius=H * 0.04, fill=b,
                                outline=LINE, width=ow)
            d.line([(0.6 * W, (0.5 + sgn * 0.3) * H), (0.86 * W, (0.5 + sgn * 0.3) * H)], fill=LINE, width=max(2, int(H * 0.04)))
        _poly(d, [(0.96, 0.5), (0.8, 0.36), (0.1, 0.38), (0.04, 0.5), (0.1, 0.62), (0.8, 0.64)], W, H, b, LINE, ow)
        d.ellipse([0.56 * W, 0.42 * H, 0.76 * W, 0.58 * H], fill=(255, 200, 80, 255), outline=LINE, width=ow)
        d.line([(0.14 * W, 0.5 * H), (0.5 * W, 0.5 * H)], fill=acc, width=max(2, int(H * 0.05)))
    return fn


def drone_mm_draw(d, W, H):
    """An orange war drone of our own seen from above: a round core with a red eye and four arms. / Un drone de guerre
    orange à nous : un cœur rond à l'œil rouge et quatre bras."""
    ow = _ow(W)
    for a in range(4):
        ang = math.pi / 4 + a * math.pi / 2
        x, y = 0.5 + math.cos(ang) * 0.38, 0.5 + math.sin(ang) * 0.38
        d.line([(0.5 * W, 0.5 * H), (x * W, y * H)], fill=(90, 50, 30, 255), width=max(3, int(W * 0.1)))
        d.ellipse([(x - 0.1) * W, (y - 0.1) * H, (x + 0.1) * W, (y + 0.1) * H], fill=(200, 110, 50, 255), outline=LINE, width=ow)
    d.ellipse([0.24 * W, 0.24 * H, 0.76 * W, 0.76 * H], fill=(230, 140, 60, 255), outline=LINE, width=ow)
    d.ellipse([0.38 * W, 0.38 * H, 0.62 * W, 0.62 * H], fill=(230, 40, 40, 255), outline=LINE, width=ow)


def dragon_rider_draw(body, wing):
    """Our wizard of our own on his flying beast, seen from above, nose to the right: the long neck, the spread
    wings, the rider in his pointed hat. / Notre magicien à nous sur sa bête volante, vu du dessus."""
    def fn(d, W, H):
        ow = _ow(W)
        b, wg = _c(body), _c(wing)
        for sgn in (1, -1):
            _poly(d, [(0.56, 0.5 + sgn * 0.08), (0.44, 0.5 + sgn * 0.46), (0.36, 0.5 + sgn * 0.3), (0.26, 0.5 + sgn * 0.42),
                      (0.24, 0.5 + sgn * 0.08)], W, H, wg, LINE, ow)
        _poly(d, [(0.02, 0.5), (0.2, 0.44), (0.3, 0.5), (0.2, 0.56)], W, H, b, LINE, ow)                     # the tail / la queue
        d.ellipse([0.2 * W, 0.38 * H, 0.66 * W, 0.62 * H], fill=b, outline=LINE, width=ow)
        _poly(d, [(0.62, 0.46), (0.86, 0.44), (0.98, 0.5), (0.86, 0.56), (0.62, 0.54)], W, H, b, LINE, ow)    # neck and head
        d.ellipse([0.88 * W, 0.45 * H, 0.92 * W, 0.49 * H], fill=(255, 220, 60, 255))
        d.ellipse([0.36 * W, 0.4 * H, 0.52 * W, 0.6 * H], fill=(70, 50, 140, 255), outline=LINE, width=ow)     # the rider
        _poly(d, [(0.4, 0.44), (0.52, 0.5), (0.4, 0.56), (0.32, 0.5)], W, H, (230, 200, 60, 255), LINE, ow)
    return fn


def wyvern_draw(body):
    """A little dragon of our own seen from above, nose to the left. / Un petit dragon à nous vu du dessus."""
    def fn(d, W, H):
        ow = _ow(W)
        b, dk = _c(body), _c(_mix(body, (0, 0, 0), 0.35))
        for sgn in (1, -1):
            _poly(d, [(0.4, 0.5 + sgn * 0.06), (0.62, 0.5 + sgn * 0.46), (0.66, 0.5 + sgn * 0.2), (0.78, 0.5 + sgn * 0.3), (0.7, 0.5 + sgn * 0.04)],
                  W, H, dk, LINE, ow)
        _poly(d, [(0.98, 0.5), (0.74, 0.44), (0.7, 0.5), (0.74, 0.56)], W, H, b, LINE, ow)
        d.ellipse([0.3 * W, 0.38 * H, 0.76 * W, 0.62 * H], fill=b, outline=LINE, width=ow)
        _poly(d, [(0.02, 0.5), (0.16, 0.42), (0.34, 0.46), (0.34, 0.54), (0.16, 0.58)], W, H, b, LINE, ow)
        d.ellipse([0.1 * W, 0.44 * H, 0.15 * W, 0.49 * H], fill=(255, 230, 80, 255))
    return fn


def eye_beast_draw(d, W, H):
    """A big floating eye beast of our own seen from above, with its tentacles. / Une grosse bête-œil volante à nous."""
    ow = _ow(W)
    for a in range(7):
        ang = math.pi * 0.4 + a * math.pi * 1.2 / 6
        d.line([(0.5 * W, 0.5 * H), ((0.5 + math.cos(ang) * 0.48) * W, (0.5 + math.sin(ang) * 0.46) * H)], fill=(120, 60, 130, 255),
               width=max(3, int(W * 0.05)))
    d.ellipse([0.14 * W, 0.14 * H, 0.86 * W, 0.86 * H], fill=(170, 90, 170, 255), outline=LINE, width=ow)
    d.ellipse([0.22 * W, 0.28 * H, 0.62 * W, 0.72 * H], fill=(250, 250, 240, 255), outline=LINE, width=ow)
    d.ellipse([0.24 * W, 0.4 * H, 0.42 * W, 0.6 * H], fill=(200, 30, 40, 255))


# ============================================================================ shared behaviour / comportement commun
class _CpsShooter:
    """What the CPS shoot'em ups share: the energy that drops is a hit taken, the weapon read in the game is named, the
    bomb sweeps the screen, the HUD helpers. / Ce que partagent les shoot'em ups CPS."""
    WEAPONS = {}                                       # value -> name of the weapon read in the game / nom de l'arme
    WEAPON = "weapon"
    hits = 0                                           # (tests)
    named = 0
    swept = 0

    def energy_hits(self, vals, now):
        for side, suf in (("p1", ""), ("p2", "_p2")):
            ch = self.changed(vals, "health" + suf)
            P = self.ships[side]
            if not (ch and ch[1] < ch[0] and P["in"]):
                continue
            self.hits += 1
            x, y = self.pos(side, now)
            fx, S = self.fx, self.S
            fx.sparks(x, y, 16, (255, 220, 140), (200, 600), (0, 360), (0.2, 0.5), 0, "front", 3, 22)
            fx.glow(x, y, 30, 140, (255, 120, 60), 0.3, "front", 0.9, 0.0)
            fx.shake(5, 0.25)
            if ch[1] <= 25 < ch[0]:
                self.popup(tr("DANGER !", "DANGER!"), x, max(S(176), y - S(80)), RED, 40)

    def weapon_name(self, vals, suf=""):
        w = _n(vals.get(self.WEAPON + suf))
        return None if w is None else self.WEAPONS.get(int(w))

    def weapon_popups(self, vals, now):
        for side, suf in (("p1", ""), ("p2", "_p2")):
            ch = self.changed(vals, self.WEAPON + suf)
            name = self.weapon_name(vals, suf)
            if ch and name and self.ships[side]["in"]:
                self.named += 1
                x, y = self.pos(side, now)
                self.popup(name, x, max(self.S(176), y - self.S(80)), GOLD, 38, key="stencil")

    def sweep(self, side, now, color=(255, 210, 140)):
        """A bomb of a side-view game: blasts along the way, every enemy blows up. / Une bombe : des explosions."""
        S, fx = self.S, self.fx
        self.swept += 1
        self.weapon_window(now)
        x, y = self.pos(side, now)
        fx.flash(color, 0.35, 0.4)
        fx.shake(8, 0.4)
        for i in range(7):
            fx.later(i * 0.07, fx.explosion, x + S(180) + i * S(220), y + self.rng.uniform(-S(90), S(90)), 0.7, False)
        for e in self.enemies:
            if not e.get("dead"):
                fx.later(0.35 + self.rng.uniform(0, 0.3), self._boom, e)
        self.popup(tr("BOMBE !", "BOMB!"), x, max(S(176), y - S(80)), (255, 170, 80), 40)

    def bombs_swept(self, vals, now):
        for side, suf in (("p1", ""), ("p2", "_p2")):
            ch = self.changed(vals, "bombs" + suf)
            if ch and ch[1] < ch[0] and self.ships[side]["in"]:
                self.sweep(side, now)

    # -- HUD helpers / outils du HUD
    def score_box(self, screen, eng, vals, side, tag, color, w=420, y=8):
        """The tag of the player as in the game and the score. / L'étiquette du joueur et le score."""
        S, W, hd = self.S, self.W, self.hd
        right = side == "p2"
        x = W - S(16) - S(w) if right else S(16)
        self.pill(screen, x, S(y), S(w), S(60), 150)
        self.text(screen, tag, x + S(18), S(y + 30), 28, color, key="black", valign="middle")
        name = "score_p2" if right else "score"
        if _n(vals.get(name)) is not None:
            hd._score(screen, eng, name, x + S(w) - S(14), S(y + 6), "right", S(44))

    def p2_corner(self, screen, eng, vals, now, tag="2P", color=(255, 120, 200), w=420):
        if self.p2_in(vals):
            self.score_box(screen, eng, vals, "p2", tag, color, w)
        else:
            word, col = self.invite(vals, now)
            self.label(screen, word, self.W - self.S(24), self.S(44), 32, col, align="right")

    def gauge(self, screen, tag, frac, x, y, w, color, tag_color=CREAM, segments=0):
        """A gauge with its name as in the game, in segments or whole. / Une jauge et son nom, en segments ou pleine."""
        S, pg = self.S, self.pg
        tw_ = self.hd.text(tag, "black", S(26), tag_color)["w"]
        self.pill(screen, x - S(12), y - S(24), tw_ + S(w) + S(44), S(48), 160, radius=12)
        self.text(screen, tag, x, y, 26, tag_color, key="black", valign="middle")
        gx = x + tw_ + S(14)
        if not segments:
            self.bar(screen, gx, y - S(11), S(w), S(22), frac, color)
            return
        n = int(math.ceil(_clamp(frac) * segments - 1e-6))
        sw = S(w) / segments
        for i in range(segments):
            pg.draw.rect(screen, color if i < n else (50, 36, 30), (int(gx + i * sw), y - S(11), max(2, int(sw - S(4))), S(22)),
                         border_radius=S(4))

    def icons_row(self, screen, img, n, x, y, step, most=8, right=False, label=None):
        if n is None:
            return
        n = int(n)
        k = min(most, max(0, n))
        w = max(1, k) * step + (self.hd.text(label, "black", self.S(26), WHITE)["w"] + self.S(12) if label else 0)
        bx = x - w if right else x
        self.pill(screen, bx - self.S(10), y - self.S(26), w + self.S(20), self.S(52), 150, radius=12)
        for i in range(k):
            screen.blit(img, (int(bx + i * step), int(y - img.get_height() / 2)))
        if label:
            self.text(screen, label, bx + k * step + self.S(6), y, 26, WHITE, key="black", valign="middle")


# ============================================================================ vertical shooters / verticaux
class WarPlanesScene(_CpsShooter, AeroFightersScene):
    """The CPS war games seen from the sky: our twin-boom fighter, the enemy fighters of the time and their bombers.
    / Les jeux de guerre CPS vus du ciel : notre chasseur bipoutre, les chasseurs ennemis et leurs bombardiers."""
    PROP = True
    ODD = "bomber"
    SHIPS = False                                      # warships for the targets on the sea / navires sur la mer
    LANES = None
    FOE_KIND = 2
    FOE_ACC = (230, 40, 40)
    BOMBER = None                                      # draw function of the big bomber / le gros bombardier

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        if self.SHIPS:                                 # the ground targets are warships / les cibles au sol sont des navires
            self.imgs[("ground", "tank")] = self.img("destroyer", S(130), S(44), destroyer_draw)
            self.imgs["wreck"] = self.img("oil", S(60), S(30), lambda d, W, H: d.ellipse([0, 0, W, H], fill=(20, 24, 40, 120)))

    def plane_fn(self, side, kind):
        return lightning_draw((176, 184, 196) if side == "p1" else (196, 186, 150), self.ACC[side])

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            if kind == "bomber":
                s = self.img(("enemyimg", "bomber"), S(170), S(190), self.BOMBER or bomber_draw)
            else:
                s = self.img(("enemyimg", "warprop"), S(96), S(90), prop_plane_draw(self.FOE_KIND, self.FOE_ACC), flip=True)
            if shadow:
                s = self.shadow_of(self.pg, s, 70)
            self.imgs[key] = s
        return s

    def lane_y(self):
        if self.LANES:
            return self.S(self.rng.choice(self.LANES) + self.rng.uniform(-14, 14))
        return super().lane_y()

    def update(self, vals, now):
        super().update(vals, now)
        if self.LANES is None and not self.SHIPS:
            self.ground = []                           # high in the sky: nothing on the ground / rien au sol
        self.energy_hits(vals, now)
        self.weapon_popups(vals, now)

    def bomb(self, side, now):
        """The special attack of the war games: lightning strikes all over the sky. / L'attaque spéciale : des éclairs."""
        fx, S, rng = self.fx, self.S, self.rng
        x, y = self.pos(side, now)
        self.bombs += 1
        self.bpop[side] = now
        self.weapon_window(now)
        self.popup(tr("ÉCLAIR !", "LIGHTNING!"), x, max(S(176), y - S(80)), (160, 220, 255), 40)
        fx.flash((200, 230, 255), 0.5, 0.5)
        fx.shake(10, 0.5)
        for i in range(7):
            tx = x + S(200) + i * S(230)
            fx.later(i * 0.06, fx.tracer, tx, -S(20), tx + rng.uniform(-60, 60) * self.s, S(400), 5000, (200, 230, 255), 10, 400, "front", False)
            fx.later(0.1 + i * 0.06, fx.explosion, tx, rng.uniform(S(170), S(320)), 0.6, False)
        for e in self.enemies:
            if not e.get("dead"):
                fx.later(0.4 + rng.uniform(0, 0.4), self._boom, e)
        for g in self.ground:
            if not g.get("dead"):
                fx.later(0.5 + rng.uniform(0, 0.3), self._ground_boom, g)

    def bolt_icon(self):
        S = self.S
        return self.img("bolt", S(30), S(40), lambda d, W, H: _poly(d, [(0.62, 0.0), (0.18, 0.56), (0.48, 0.56), (0.34, 1.0), (0.84, 0.38),
                                                                        (0.52, 0.38), (0.7, 0.0)], W, H, (255, 170, 40, 255), LINE, 2))


class Loop1944Scene(WarPlanesScene):
    """1944: The Loop Master as in the game: the deep blue Pacific seen from the sky, huge battleships and their wakes,
    our silver twin-boom fighter against the green fighters and the bombers. 1P in red and the score, the red energy
    gauge under it, the lightning bombs at the bottom left, 2P in pink. / Le Pacifique bleu profond, d'énormes
    cuirassés, notre chasseur bipoutre argenté contre les chasseurs verts, comme dans le jeu."""
    THEME = "c44_sea"
    SHADE = (70, 60)
    SHIPS = True
    LANES = SEA44_LANES
    ACC = {"p1": (220, 40, 40), "p2": (250, 120, 190)}
    SHOT = {"p1": (255, 220, 120), "p2": (255, 170, 220)}
    FOE_KIND = 4
    FOE_ACC = (230, 230, 230)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P in red and the score, the red energy gauge, 2P in pink, the lightning bombs at the bottom
        left. / Comme dans le jeu : 1P en rouge et le score, la jauge d'énergie rouge, 2P en rose, les éclairs en bas."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1P", (255, 70, 60))
        e = _n(vals.get("health"))
        if e is not None:
            self.gauge(screen, "POW", e / 100.0, S(30), S(98), 300, (240, 50, 40))
        self.p2_corner(screen, eng, vals, now, "2P", (255, 120, 200))
        b = _n(vals.get("bombs"))
        if b is not None:
            self.icons_row(screen, self.bolt_icon(), b, S(30), H - S(40), S(34))


class War19XXScene(WarPlanesScene):
    """19XX: The War Against Destiny as in the game: high in the sky over the sea and its islands, white clouds
    flying by, the plane chosen read in the game (the twin-boom fighter, the canard fighter or the twin-engine
    fighter-bomber), the big four-engine bombers. 1P and the score, the planes left and the bombs at the bottom.
    / Haut dans le ciel au-dessus de la mer, l'avion choisi lu dans le jeu, les gros bombardiers, comme dans le jeu."""
    THEME = "c19_sky"
    SHADE = (60, 60)
    ACC = {"p1": (230, 60, 50), "p2": (80, 160, 250)}
    SHOT = {"p1": (255, 230, 130), "p2": (160, 220, 255)}
    BOMBER = staticmethod(heavy_bomber_draw((196, 202, 210)))
    PLANES = {0: "LIGHTNING", 1: "SHINDEN", 2: "MOSQUITO"}
    WEAPONS = {4: "SHOT", 8: "3-WAY", 12: "SHELL"}

    def kind(self, vals, side):
        k = _n(vals.get("plane" if side == "p1" else "plane_p2"))
        return int(k) if k is not None and int(k) in self.PLANES else 0

    def plane_fn(self, side, kind):
        body = (176, 184, 196) if side == "p1" else (196, 186, 150)
        if kind == 1:
            return shinden_draw((150, 160, 120), self.ACC[side])
        if kind == 2:
            return prop_plane_draw(8, self.ACC[side])
        return lightning_draw(body, self.ACC[side])

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "plane")
        if ch and self.ships["p1"]["in"]:
            x, y = self.pos("p1", now)
            self.popup(self.PLANES.get(int(ch[1]), ""), x, max(self.S(176), y - self.S(80)), GOLD, 38, key="stencil")

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score, the planes left, the round bombs at the bottom left, the plane's name.
        / Comme dans le jeu : 1P et le score, les avions restants, les bombes rondes en bas à gauche, le nom de l'avion."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1P", (255, 90, 80))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.icons_row(screen, self.life_icon("p1", vals), lives, S(30), S(102), S(44), 6)
        self.p2_corner(screen, eng, vals, now, "2P", (110, 180, 255))
        b = _n(vals.get("bombs"))
        if b is not None:
            ball = self.img("19bomb", S(30), S(30), lambda d, W_, H_: (d.ellipse([0, 0, W_ - 1, H_ - 1], fill=(250, 200, 60, 255), outline=LINE,
                                                                                  width=2),
                                                                        d.ellipse([W_ * 0.3, H_ * 0.3, W_ * 0.7, H_ * 0.7], fill=(220, 60, 40, 255))))
            self.icons_row(screen, ball, b, S(30), H - S(40), S(36))
        name = self.PLANES.get(self.kind(vals, "p1"))
        if name and _n(vals.get("plane")) is not None:
            self.label(screen, name, W / 2, H - S(30), 28, GOLD, key="black", align="center")


class Counter1941Scene(WarPlanesScene):
    """1941: Counter Attack as in the game: a dark blue sea between two snowy rocky coasts, our twin-boom fighter
    against the red-nosed fighters and the bombers, the warships below. 1PLAYER and the score, at the bottom the
    VITAL gauge in segments and the weapon picked up with its time. / Une mer bleu sombre entre deux côtes enneigées,
    notre chasseur bipoutre, la jauge VITAL en segments et l'arme ramassée, comme dans le jeu."""
    THEME = "c41_coast"
    SHADE = (70, 70)
    SHIPS = True
    LANES = SEA41_LANES
    ACC = {"p1": (60, 110, 230), "p2": (230, 80, 60)}
    SHOT = {"p1": (255, 230, 130), "p2": (255, 180, 140)}
    FOE_KIND = 2
    FOE_ACC = (230, 40, 40)
    WEAPONS = {0: "NORMAL", 1: "M. GUN", 2: "S. SHELL", 3: "MISSILE"}

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1PLAYER and the score, the VITAL gauge in seven segments, the weapon and its time.
        / Comme dans le jeu : 1PLAYER et le score, la jauge VITAL en sept segments, l'arme et son temps."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1PLAYER", (255, 210, 80), 460)
        self.p2_corner(screen, eng, vals, now, "2PLAYER", (120, 200, 255), 460)
        e = _n(vals.get("health"))
        if e is not None:
            self.gauge(screen, "VITAL", e / 100.0, S(30), H - S(40), 280, (80, 200, 255), segments=7)
        name = self.weapon_name(vals)
        if name:
            t = _n(vals.get("weapon_time"))
            self.label(screen, name + (f"  {int(t)}" if t is not None and name != "NORMAL" else ""), S(560), H - S(40), 28, GOLD, key="black")


class VarthScene(_CpsShooter, AeroFightersScene):
    """Varth: Operation Thunderstorm as in the game: a military base of teal plates seen from the sky, hangars and
    round pads, our jet with its two guard pods turning around it, tanks on the taxiways. SCORE and the score, the
    planes left, the bombs, the weapon and the missiles read in the game. / Une base militaire de plaques bleu-vert,
    notre chasseur et ses deux modules de garde qui tournent autour, comme dans le jeu."""
    THEME = "vt_base"
    SHADE = (70, 70)
    ACC = {"p1": (60, 140, 240), "p2": (240, 120, 60)}
    SHOT = {"p1": (160, 230, 255), "p2": (255, 210, 140)}
    ODD = "heli"
    WEAPONS = {0: "NORMAL", 2: "3-WAY", 4: "LASER"}
    PODS = {0: "H", 1: "M", 2: "N"}

    def plane_fn(self, side, kind):
        return jet_draw("hornet", (200, 206, 216) if side == "p1" else (216, 200, 180), self.ACC[side])

    def lane_y(self):
        return self.S(self.rng.choice(VT_LANES) + self.rng.uniform(-10, 10))

    def power_max(self, vals, side):
        return 7

    def update(self, vals, now):
        super().update(vals, now)
        self.weapon_popups(vals, now)

    def draw_hud(self, screen, eng, vals, logo, now):
        super().draw_hud(screen, eng, vals, logo, now)
        S, sp = self.S, self.fx.sp
        P = self.ships["p1"]
        if P["in"] and now - P["t_dead"] > 1.2 and now >= P["t_spawn"]:     # the two guard pods / les deux modules
            x, y = self.pos("p1", now)
            for k in (0, 1):
                a = now * 3.0 + k * math.pi
                px, py = x + math.cos(a) * S(70), y + math.sin(a) * S(56)
                g = sp.glow(S(26), (120, 220, 255), 8, hot=0.7)
                screen.blit(g, (int(px - g.get_width() / 2), int(py - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
                self.pg.draw.circle(screen, (230, 240, 255), (int(px), int(py)), S(9))

    def status(self, screen, eng, vals, logo, now):
        """As in the game: SCORE and the score, the planes left, the bombs, the weapon and the missiles of the pods.
        / Comme dans le jeu : SCORE et le score, les avions, les bombes, l'arme et les missiles des modules."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "SCORE", (120, 230, 255))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.icons_row(screen, self.life_icon("p1", vals), lives, S(30), S(102), S(44), 6)
        self.p2_corner(screen, eng, vals, now, "SCORE", (255, 170, 110))
        b = _n(vals.get("bombs"))
        if b is not None:
            bimg = self.img("vtb", S(30), S(30), lambda d, W_, H_: (d.rectangle([0, 0, W_ - 1, H_ - 1], fill=(230, 60, 50, 255), outline=LINE, width=2),
                                                                    d.ellipse([W_ * 0.25, H_ * 0.25, W_ * 0.75, H_ * 0.75], fill=(255, 255, 255, 255))))
            self.icons_row(screen, bimg, b, S(30), H - S(40), S(36))
        name = self.weapon_name(vals)
        pod = _n(vals.get("pods"))
        bits = [n for n in (name, (tr("MISSILES ", "MISSILES ") + self.PODS[int(pod)]) if pod is not None and int(pod) in self.PODS else None) if n]
        if bits:
            self.label(screen, "   ".join(bits), W / 2, H - S(30), 28, GOLD, key="black", align="center")


class GigaWingScene(_CpsShooter, AeroFightersScene):
    """Giga Wing as in the game: an old steel fortress seen from the sky, cut by rivers of glowing lava, tanks on
    the rails, our jet against the gunships. 1P and the score, the planes and the bombs read in the game, the pilot
    chosen, REFLECT ready at the bottom. / Une vieille forteresse d'acier coupée de rivières de lave, notre chasseur
    contre les canonnières, comme dans le jeu."""
    THEME = "gw_lava"
    SHADE = (70, 70)
    ACC = {"p1": (230, 60, 60), "p2": (60, 140, 240)}
    SHOT = {"p1": (255, 220, 120), "p2": (150, 220, 255)}
    ODD = "heli"

    def plane_fn(self, side, kind):
        return jet_draw("tomcat", (214, 218, 226) if side == "p1" else (190, 200, 220), self.ACC[side])

    def lane_y(self):
        return self.S(self.rng.choice(GW_LANES) + self.rng.choice((-40, 40)))

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "bombs")
        if ch and ch[1] < ch[0]:                                         # the barrier flashes gold / la barrière dorée
            x, y = self.pos("p1", now)
            self.fx.glow(x, y, 60, 520, (255, 210, 90), 0.6, "front", 0.9, 0.0)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score, the planes and the bombs, the pilot, REFLECT ready.
        / Comme dans le jeu : 1P et le score, les avions et les bombes, le pilote, REFLECT prêt."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1P", (255, 200, 80))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.icons_row(screen, self.life_icon("p1", vals), lives, S(30), S(102), S(44), 6)
        self.p2_corner(screen, eng, vals, now, "2P", (120, 190, 255))
        b = _n(vals.get("bombs"))
        if b is not None:
            bimg = self.img("gwb", S(30), S(30), lambda d, W_, H_: d.ellipse([0, 0, W_ - 1, H_ - 1], fill=(250, 210, 60, 255), outline=LINE, width=2))
            self.icons_row(screen, bimg, b, S(30), H - S(40), S(36), label="B")
        pilot = vals.get("p1_char")
        if isinstance(pilot, str) and pilot:
            self.label(screen, pilot, W / 2, H - S(30), 28, WHITE, key="black", align="center")
        k = 0.7 + 0.3 * math.sin(now * 4)
        self.label(screen, "REFLECT OK", W - S(30), H - S(36), 28, GOLD, key="black", align="right", fade=k)


class MarsMatrixScene(_CpsShooter, AeroFightersScene):
    """Mars Matrix as in the game: a rust-red mechanical base seen from the sky, round pads, pipes and warning
    stripes, our mech fighter against the orange war drones. 1P and the score, the ships left, LEVEL and the power
    of the shot at the right. / Une base mécanique rouille, notre chasseur mécanique contre les drones orange."""
    THEME = "mm_base"
    SHADE = (70, 70)
    ACC = {"p1": (60, 200, 120), "p2": (240, 160, 40)}
    SHOT = {"p1": (120, 200, 255), "p2": (255, 210, 140)}
    ODD = "bomber"

    def plane_fn(self, side, kind):
        return mm_ship_draw((120, 170, 140) if side == "p1" else (190, 170, 120), self.ACC[side])

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            big = kind == "bomber"
            s = self.img(("enemyimg", "mmdrone", big), S(150 if big else 80), S(150 if big else 80), drone_mm_draw)
            if shadow:
                s = self.shadow_of(self.pg, s, 70)
            self.imgs[key] = s
        return s

    def lane_y(self):
        return self.S(self.rng.choice(MM_LANES) + self.rng.uniform(-12, 12))

    def power_max(self, vals, side):
        return 7

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score, the ships left, LEVEL and the power at the right.
        / Comme dans le jeu : 1P et le score, les vaisseaux, LEVEL et la puissance à droite."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1P", (120, 255, 160))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.icons_row(screen, self.life_icon("p1", vals), lives, S(30), S(102), S(44), 6)
        self.p2_corner(screen, eng, vals, now, "2P", (255, 190, 90))
        pw = _n(vals.get("power"))
        if pw is not None:
            self.label(screen, f"LEVEL {int(pw) + 1}", W - S(30), H - S(36), 32, GOLD, key="black", align="right")



class DimahooScene(_CpsShooter, AeroFightersScene):
    """Dimahoo as in the game: a magic sky of violet clouds seen from above, floating rocks, our wizard of our own
    on his flying beast against little dragons and big eye beasts. PLAYER 1 and the score, the lives, the magic
    bombs, the hero chosen. / Un ciel magique de nuages violets, notre magicien sur sa bête volante contre des petits
    dragons, comme dans le jeu."""
    THEME = "dh_clouds"
    SHADE = (60, 60)
    PROP = True
    ACC = {"p1": (240, 200, 60), "p2": (240, 110, 170)}
    SHOT = {"p1": (255, 160, 240), "p2": (160, 240, 255)}
    ODD = "bomber"

    def plane_fn(self, side, kind):
        return dragon_rider_draw((90, 170, 120) if side == "p1" else (170, 110, 90), (200, 220, 160) if side == "p1" else (230, 180, 140))

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            if kind == "bomber":
                s = self.img(("enemyimg", "eyebeast"), S(150), S(150), eye_beast_draw)
            else:
                s = self.img(("enemyimg", "wyvern"), S(110), S(96), wyvern_draw((170, 60, 60)))
            if shadow:
                s = self.shadow_of(self.pg, s, 60)
            self.imgs[key] = s
        return s

    def update(self, vals, now):
        super().update(vals, now)
        self.ground = []                                                 # nothing on the ground / rien au sol

    def bomb(self, side, now):
        """A magic bomb: rings of light. / Une bombe magique : des anneaux de lumière."""
        fx, S = self.fx, self.S
        x, y = self.pos(side, now)
        self.bombs += 1
        self.bpop[side] = now
        self.weapon_window(now)
        self.popup(tr("MAGIE !", "MAGIC!"), x, max(S(176), y - S(80)), (255, 160, 240), 40)
        fx.flash((240, 200, 255), 0.4, 0.5)
        for i in range(5):
            fx.later(i * 0.1, fx.glow, x + S(300) * (i + 1) / 2, y, 40, 300, (220, 140, 255), 0.6, "front", 0.9, 0.0)
        for e in self.enemies:
            if not e.get("dead"):
                fx.later(0.4 + self.rng.uniform(0, 0.4), self._boom, e)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: PLAYER 1 and the score, the lives, the magic bombs, the hero chosen.
        / Comme dans le jeu : PLAYER 1 et le score, les vies, les bombes magiques, le héros choisi."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "PLAYER 1", (255, 220, 90), 460)
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.icons_row(screen, self.life_icon("p1", vals), lives, S(30), S(102), S(44), 6)
        self.p2_corner(screen, eng, vals, now, "PLAYER 2", (255, 140, 200), 460)
        b = _n(vals.get("bombs"))
        if b is not None:
            star = self.img("dhb", S(32), S(32), lambda d, W_, H_: _poly(d, [(0.5 + 0.48 * math.cos(-math.pi / 2 + i * math.pi / 5) *
                                                                              (1 if i % 2 == 0 else 0.45),
                                                                              0.5 + 0.48 * math.sin(-math.pi / 2 + i * math.pi / 5) *
                                                                              (1 if i % 2 == 0 else 0.45)) for i in range(10)],
                                                                         W_, H_, (250, 150, 240, 255), LINE, 2))
            self.icons_row(screen, star, b, S(30), H - S(40), S(36))
        hero = vals.get("p1_char")
        if isinstance(hero, str) and hero:
            self.label(screen, hero, W / 2, H - S(30), 28, WHITE, key="black", align="center")


# ============================================================================ side-view shooters / de profil
class _SideCps(_CpsShooter, SideShooterScene):
    def update(self, vals, now):
        super().update(vals, now)
        self.energy_hits(vals, now)
        self.weapon_popups(vals, now)
        self.bombs_swept(vals, now)


class UNSquadronScene(_SideCps):
    """U.N. Squadron as in the game: our jet of our own over a desert canyon, mauve mesas, the towers of a refinery,
    tanks on the concrete, the enemy helicopters. 1 PLAYER and the score at the top, at the bottom the special
    weapon read in the game and its stock, as in the game. / Notre chasseur au-dessus d'un canyon du désert, les
    tours d'une raffinerie, les hélicoptères ennemis, l'arme spéciale et son stock, comme dans le jeu."""
    THEME = "un_canyon"
    ACC = {"p1": (230, 60, 50), "p2": (60, 130, 230)}
    SHIP = (210, 90)
    FOE = (170, 92)
    FLIP_FOE = True
    WEAPONS = {0: "PHOENIX", 4: "FALCON", 8: "BOMB", 12: "BOMB II", 16: "NAPALM", 20: "NAPALM II", 28: "BULLPUP", 32: "BULLPUP II",
               52: "SUPER SHELL", 56: "SUPER SHELL II"}

    def ship_fn(self, side):
        return side_jet_draw((150, 160, 176) if side == "p1" else (170, 160, 140), self.ACC[side])

    def foe_fn(self, frame):
        return side_heli_draw((70, 90, 60), (210, 200, 70))

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.1

    def bombs_swept(self, vals, now):
        """Each shot of the special weapon spends one of its stock: a missile goes to the nearest enemy ahead.
        / Chaque tir de l'arme spéciale en dépense une : un missile part vers l'ennemi le plus proche devant."""
        ch = self.changed(vals, "bombs")
        if not (ch and ch[1] < ch[0] and self.ships["p1"]["in"]):
            return
        S, fx = self.S, self.fx
        self.swept += 1
        x, y = self.pos("p1", now)
        live = [e for e in self.enemies if not e.get("dead") and e["x"] > x]
        tgt = min(live, key=lambda e: e["x"]) if live else None
        tx, ty = (tgt["x"], tgt.get("yy", tgt["y"])) if tgt else (self.W + S(40), y + S(20))
        fx.tracer(x + S(60), y + S(14), tx, ty, 1600, (255, 200, 120), 8, 90, "front", False)
        fx.glow(x + S(60), y + S(14), 16, 60, (255, 200, 120), 0.2, "front", 0.9, 0.0)
        if tgt is not None:
            self.weapon_window(now, 0.9)
            fx.later(min(0.8, abs(tx - x) / (1600 * self.s)), self._boom, tgt)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1 PLAYER and the score, the face of our pilot next to it, 2 PLAYER at the right, the special
        weapon and its stock at the bottom. / Comme dans le jeu : 1 PLAYER et le score, le visage de notre pilote,
        l'arme spéciale et son stock en bas."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1 PLAYER", (255, 230, 120), 460)
        screen.blit(self.img("unface", S(60), S(60), portrait_draw((226, 176, 136), (170, 70, 40), bg=(70, 100, 170)), ss=2), (S(490), S(8)))
        self.p2_corner(screen, eng, vals, now, "2 PLAYER", (120, 190, 255), 460)
        name, n = self.weapon_name(vals), _n(vals.get("bombs"))
        if name or n is not None:
            txt = (name or tr("ARME", "WEAPON")) + (f"  {int(n)}" if n is not None else "")
            self.label(screen, txt, S(30), H - S(36), 30, (255, 200, 90), key="black")


class CarrierAirWingScene(_SideCps):
    """Carrier Air Wing as in the game: our big navy jet of our own high above a whole city seen at an angle, white
    clouds flying by, enemy jets coming. LEVEL, 1PLAYER and the score, the money at the top, WEAPON and the FUEL
    gauge at the bottom, read in the game. / Notre gros chasseur de l'aéronavale au-dessus d'une ville vue de biais,
    la jauge FUEL et l'arme en bas, comme dans le jeu."""
    THEME = "ca_city"
    ACC = {"p1": (60, 110, 220), "p2": (230, 80, 60)}
    SHIP = (240, 104)
    FOE = (170, 76)
    FLIP_FOE = True
    WEAPONS = {0: "SPREAD", 1: "MISSILE", 2: "GUNS"}

    def ship_fn(self, side):
        return side_jet_draw((170, 178, 190) if side == "p1" else (186, 176, 160), self.ACC[side], big=True)

    def foe_fn(self, frame):
        return side_jet_draw((90, 100, 80), (230, 200, 60))

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.2

    def status(self, screen, eng, vals, logo, now):
        """As in the game: LEVEL, 1PLAYER and the score, the money, WEAPON and the FUEL gauge.
        / Comme dans le jeu : LEVEL, 1PLAYER et le score, l'argent, WEAPON et la jauge FUEL."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1PLAYER", (255, 220, 90), 460)
        lv, money = _n(vals.get("power")), _n(vals.get("money"))
        bits = ([f"LEVEL {int(lv) + 1}"] if lv is not None else []) + ([f"$ {int(money)}"] if money is not None else [])
        if bits:
            self.label(screen, "   ".join(bits), S(30), S(100), 26, WHITE, key="black")
        self.p2_corner(screen, eng, vals, now, "2PLAYER", (120, 190, 255), 460)
        e = _n(vals.get("health"))
        if e is not None:
            self.gauge(screen, "FUEL", e / 100.0, W - S(420), H - S(40), 300, (250, 90, 70))
        name, ammo = self.weapon_name(vals), _n(vals.get("ammo"))
        if name or ammo is not None:
            self.label(screen, "WEAPON " + (name or "") + (f"  {int(ammo)}" if ammo is not None else ""), S(30), H - S(36), 28, GOLD, key="black")


class ForgottenWorldsScene(_SideCps):
    """Forgotten Worlds as in the game: our flying soldier of our own and his orbiting gun module over a dead city,
    a huge green planet in the black sky, the golden lizard warriors. 1P and the score, ZENNY, the VITAL gauge and the
    weapon bought at the shop, read in the game. / Notre soldat volant et son module qui tourne autour de lui au-dessus
    d'une ville morte, une énorme planète verte, les guerriers lézards dorés, comme dans le jeu."""
    THEME = "fw_ruins"
    SHADE = (60, 60)
    ACC = {"p1": (60, 110, 220), "p2": (220, 70, 60)}
    SHIP = (240, 160)
    FOE = (160, 140)
    WEAPONS = {0: "LASER", 2: "BEAM", 4: "MISSILE", 6: "BALCAN", 8: "NAPALM", 10: "V-CANNON", 12: "BURNER", 14: "MULTI-WAY"}

    sat_t = 0.0
    shopped = 0                                        # (tests)

    def ship_fn(self, side):
        return flyer_draw(0)

    def foe_fn(self, frame):
        return lizard_draw(frame)

    FLIP_FOE = True

    def move(self, vals, now, idle):
        return 0.25 if idle else 0.9

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "zenny")
        if ch and ch[1] > ch[0] and self.ships["p1"]["in"]:
            x, y = self.pos("p1", now)
            self.popup(f"+{int(ch[1] - ch[0])} ZENNY", x, max(self.S(176), y - self.S(80)), GOLD, 34)
        elif ch and ch[1] < ch[0]:                                       # zenny spent at the shop / dépensés à la boutique
            self.shopped += 1
            self.popup(tr("BOUTIQUE", "SHOP") + f"  -{int(ch[0] - ch[1])} ZENNY", self.W / 2, self.S(230), (255, 220, 120), 40, life=2.0)

    def draw_hud(self, screen, eng, vals, logo, now):
        P = self.ships["p1"]
        S = self.S
        if P["in"] and now - P["t_dead"] > 1.2 and now >= P["t_spawn"]:     # the gun module turns around him
            x, y = self.pos("p1", now)
            a = now * 2.4
            mx, my = x + math.cos(a) * S(110), y + math.sin(a) * S(80)
            sat = self.img("fwsat", S(40), S(40), satellite_draw)
            screen.blit(sat, (int(mx - S(20)), int(my - S(20))))
            if now >= self.sat_t:
                self.sat_t = now + 0.45
                self.fx.tracer(mx + S(20), my, self.W + S(40), my, 3200, (255, 150, 90), 5, 60, "front", False)
        super().draw_hud(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score, ZENNY, the VITAL gauge and the weapon. / 1P et le score, ZENNY, VITAL."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1P", (120, 200, 255))
        z = _n(vals.get("zenny"))
        if z is not None:
            self.label(screen, f"ZENNY {int(z)}", S(30), S(100), 26, GOLD, key="black")
        self.p2_corner(screen, eng, vals, now, "2P", (255, 140, 120))
        e = _n(vals.get("health"))
        if e is not None:
            self.gauge(screen, "VITAL", e / 100.0, S(30), H - S(40), 300, (90, 220, 120))
        name = self.weapon_name(vals)
        if name:
            self.label(screen, name, W - S(30), H - S(36), 28, GOLD, key="black", align="right")


class ProgearScene(_SideCps):
    """Progear as in the game: our steam age fighter of our own over an old European town, red roofs and a great
    stone aqueduct, the flying steam gunboats of the enemy. P.1 and the score, the planes left, the bombs, the power
    of the shot and the type of plane read in the game. / Notre chasseur de l'âge de la vapeur au-dessus d'une
    vieille ville européenne, un grand aqueduc, les canonnières volantes, comme dans le jeu."""
    THEME = "pg_village"
    ACC = {"p1": (200, 60, 50), "p2": (60, 120, 200)}
    SHIP = (200, 110)
    FOE = (170, 100)
    FLIP_FOE = True
    FIGHTERS = {0: "GAMBLER", 1: "MILITANT"}

    def ship_fn(self, side):
        return pg_plane_draw((150, 70, 50) if side == "p1" else (60, 90, 140), (220, 210, 180))

    def foe_fn(self, frame):
        return gunboat_draw

    def move(self, vals, now, idle):
        return 0.25 if idle else 0.9

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "power")
        if ch and ch[1] > ch[0] and self.ships["p1"]["in"]:
            x, y = self.pos("p1", now)
            self.popup("POWER UP", x, max(self.S(176), y - self.S(80)), GOLD, 36)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: P.1 and the score, the planes left, the bombs, the power and the plane.
        / Comme dans le jeu : P.1 et le score, les avions, les bombes, la puissance et l'avion."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "P.1", (255, 200, 120))
        lives, b = _n(vals.get("lives")), _n(vals.get("bombs"))
        bits = ([f"x{int(lives)}"] if lives is not None else []) + ([f"B {int(b)}"] if b is not None else [])
        if bits:
            self.label(screen, "   ".join(bits), S(30), S(100), 28, WHITE, key="black")
        self.p2_corner(screen, eng, vals, now, "P.2", (140, 190, 255))
        pw = _n(vals.get("power"))
        if pw is not None:
            self.gauge(screen, "POWER", (int(pw) + 1) / 9.0, S(30), H - S(40), 240, (255, 190, 60), segments=8)
        f = _n(vals.get("fighter"))
        if f is not None and int(f) in self.FIGHTERS:
            self.label(screen, self.FIGHTERS[int(f)], W - S(30), H - S(36), 28, GOLD, key="black", align="right")


class EcoFightersScene(_SideCps):
    """Eco Fighters as in the game: our little ecological pod of our own and its turning gun arm over a bright sea,
    ochre cliffs and their waterfall, the polluting robots in green shells. 1P-SCORE and the score, ARM-LV and the
    ships left read in the game. / Notre petite capsule écologique et son bras-canon qui tourne au-dessus d'une mer
    bleu vif, les robots pollueurs dans leurs carapaces vertes, comme dans le jeu."""
    THEME = "ef_coast"
    ACC = {"p1": (80, 180, 90), "p2": (240, 140, 60)}
    SHIP = (150, 110)
    FOE = (130, 110)
    FLIP_FOE = True
    WEAPONS = {3: "ENERGY BALL", 4: "HAMMER", 7: "WHEEL", 9: "LASER SWORD"}

    def ship_fn(self, side):
        return eco_ship_draw

    def foe_fn(self, frame):
        return polluter_draw(frame)

    def move(self, vals, now, idle):
        return 0.25 if idle else 0.8

    def draw_hud(self, screen, eng, vals, logo, now):
        super().draw_hud(screen, eng, vals, logo, now)
        P = self.ships["p1"]
        S, pg = self.S, self.pg
        if P["in"] and now - P["t_dead"] > 1.2 and now >= P["t_spawn"]:     # the gun arm turns / le bras-canon tourne
            x, y = self.pos("p1", now)
            a = math.sin(now * 1.7) * 1.2
            ex, ey = x + math.cos(a) * S(110), y + math.sin(a) * S(110)
            pg.draw.line(screen, (60, 60, 70), (int(x), int(y)), (int(ex), int(ey)), S(12))
            pg.draw.line(screen, (200, 210, 220), (int(x), int(y)), (int(ex), int(ey)), S(6))
            pg.draw.circle(screen, (250, 180, 60), (int(ex), int(ey)), S(14))
            pg.draw.circle(screen, (60, 60, 70), (int(ex), int(ey)), S(14), max(1, S(3)))

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P-SCORE and the score, ARM-LV, the ships left, the weapon.
        / Comme dans le jeu : 1P-SCORE et le score, ARM-LV, les vaisseaux, l'arme."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.score_box(screen, eng, vals, "p1", "1P-SCORE", (255, 230, 90), 460)
        self.p2_corner(screen, eng, vals, now, "2P-SCORE", (120, 200, 255), 460)
        pw, lives = _n(vals.get("power")), _n(vals.get("lives"))
        bits = ([f"ARM-LV {int(pw) + 1}"] if pw is not None else []) + ([f"x{int(lives)}"] if lives is not None else [])
        if bits:
            self.label(screen, "   ".join(bits), S(30), H - S(36), 30, (255, 230, 90), key="black")
        name = self.weapon_name(vals)
        if name:
            self.label(screen, name, W - S(30), H - S(36), 28, GOLD, key="black", align="right")


SCENES = {"1944": Loop1944Scene, "19xx": War19XXScene, "1941": Counter1941Scene, "varth": VarthScene, "gigawing": GigaWingScene,
          "mmatrix": MarsMatrixScene, "dimahoo": DimahooScene, "unsquad": UNSquadronScene, "cawing": CarrierAirWingScene,
          "forgottn": ForgottenWorldsScene, "progear": ProgearScene, "ecofghtr": EcoFightersScene}
__all__ = ["SCENES", "THEMES"]
