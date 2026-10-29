"""HD scenes of the Capcom CPS beat'em ups (1.30), each drawn after screenshots of its game: Final Fight, Captain
Commando, Cadillacs and Dinosaurs, The Punisher, The King of Dragons, Knights of the Round, Warriors of Fate, the two
Dungeons & Dragons, Alien vs. Predator, Armored Warriors, Battle Circuit. Each game has its own animated backdrop and
reacts to the values read in its memory: a blow taken shakes the hero, a life lost knocks him down, a bomb or a special
attack sweeps the street, a level gained shines. The heroes, the enemies and the machines are creations of the program
in the spirit of the games, no picture comes from a game.

Scènes HD des beat'em ups Capcom CPS (1.30), chacune dessinée d'après des captures de son jeu. Chaque jeu a son décor
animé et réagit aux valeurs lues dans sa mémoire : un coup reçu secoue le héros, une vie perdue le met à terre, une
bombe ou une attaque spéciale balaie la rue, un niveau gagné brille. Les héros, les ennemis et les machines sont des
créations du programme dans l'esprit des jeux, aucune image ne vient d'un jeu.
"""

import math

from .hd_games import GOLD, WHITE, _n
from .hd_games3 import _capsule
from .hd_games5 import BrawlerScene, _mixc, fighter_draw
from .hd_themes12 import THEMES
from .i18n import tr

DARK = (22, 20, 30)
INK = (24, 20, 26, 255)
HANDS = {0: ((0.14, 0.34), (0.2, 0.3)), 1: ((0.12, 0.38), (0.06, 0.42)), 2: ((-0.04, 0.42), (0.14, 0.38)), 3: ((0.1, 0.36), (0.36, 0.26)),
         4: ((-0.12, 0.34), (0.08, 0.3)), 5: ((-0.14, 0.24), (-0.02, 0.2))}          # same hands as fighter_draw
LEAN = {3: 0.04, 4: -0.03, 5: -0.07}
WEAPON_ANGLE = {0: -62, 1: -32, 2: -40, 3: 4, 4: -128, 5: 64}
LONG = ("sword", "spear", "staff", "halberd")
BLADES = ("sword", "axe", "spear", "halberd", "knife", "claws")
BEASTS = ("raptor", "bug", "mech")


def _c(col, a=255):
    return tuple(col[:3]) + (a,)


# ============================================================================ our own heroes and foes
def hero_draw(look, frame):
    """A hero or a foe of our own, built on the street fighter of the Neo Geo brawlers (fighter_draw) with what each game
    needs: a helmet, a plume, a cape, a shield, a beard, a hat, long hair, pointed ears, tusks, a skull, a visor; and a
    weapon in the front hand: sword, axe, spear, halberd, mace, staff, club, knife, claws or gun.
    look = (style, top, pants, skin, hair, weapon, extras). / Un héros ou un ennemi à nous, avec casque, cape, bouclier,
    barbe, chapeau, cheveux longs, oreilles pointues, défenses, crâne, visière, et son arme."""
    style, top, pants, skin, hair = look[:5]
    weapon = look[5] if len(look) > 5 else None
    extras = dict(look[6]) if len(look) > 6 and look[6] else {}
    base = fighter_draw(style, top, pants, skin, hair, frame, "sword" if weapon == "sword" else None)

    def fn(d, W, H):
        u, cx = H, W * 0.5
        ow = max(1.0, H * 0.009)
        lean = LEAN.get(frame, 0.0)

        def P(x, y):
            return cx + (x + lean * (0.62 - y) / 0.62) * u, y * u
        down = frame == 6
        if "cape" in extras and not down:                                 # la cape, derrière le corps
            col = _c(extras["cape"])
            sw = 0.04 * math.sin(frame * 1.7)
            d.polygon([P(-0.08, 0.26), P(0.06, 0.26), P(-0.12 + sw, 0.74), P(-0.3 + sw, 0.7)], fill=col, outline=INK)
        if "longhair" in extras and not down:                             # les cheveux longs, derrière la tête
            hx, hy = P(0.02, 0.15)
            col = _c(extras["longhair"])
            d.polygon([(hx - 0.07 * u, hy - 0.05 * u), (hx + 0.02 * u, hy - 0.07 * u), (hx - 0.05 * u, hy + 0.2 * u), (hx - 0.14 * u, hy + 0.16 * u)],
                      fill=col, outline=INK)
        base(d, W, H)
        if down:
            hx, hy = W * 0.15, H * 0.88
            r = 0.075 * u
            if "helmet" in extras:
                d.chord([hx - r, hy - r, hx + r, hy + r], 90, 270, fill=_c(extras["helmet"]), outline=INK)
            return
        hx, hy = P(0.02, 0.15)
        r = 0.075 * u
        front = (cx + HANDS[frame][1][0] * u, HANDS[frame][1][1] * u)
        back = (cx + HANDS[frame][0][0] * u, HANDS[frame][0][1] * u)
        if "shield" in extras:                                            # le bouclier, sur le bras de derrière
            col = _c(extras["shield"])
            sr = 0.085 * u
            d.ellipse([back[0] - sr * 0.7, back[1] - sr, back[0] + sr * 0.7, back[1] + sr], fill=col, outline=INK, width=int(ow * 1.5))
            d.ellipse([back[0] - sr * 0.22, back[1] - sr * 0.3, back[0] + sr * 0.22, back[1] + sr * 0.3], fill=_mixc(extras["shield"], (255, 230, 150), 0.6))
        if "armor" in extras:                                             # les épaulières
            col = _c(extras["armor"])
            for sx in (-0.07, 0.07):
                p = P(sx, 0.29)
                d.ellipse([p[0] - 0.05 * u, p[1] - 0.035 * u, p[0] + 0.05 * u, p[1] + 0.04 * u], fill=col, outline=INK, width=int(ow))
        if "beard" in extras:
            col = _c(extras["beard"])
            d.chord([hx - r * 0.7, hy - r * 0.1, hx + r * 1.05, hy + r * 1.35], 0, 180, fill=col, outline=INK)
        if "tusks" in extras:                                             # les défenses d'un orque
            for k in (0.25, 0.65):
                d.polygon([(hx + r * k, hy + r * 0.55), (hx + r * (k + 0.16), hy + r * 0.55), (hx + r * (k + 0.06), hy + r * 0.1)], fill=(250, 245, 220, 255))
        if "ears" in extras:                                              # les oreilles pointues
            d.polygon([(hx - r * 0.3, hy - r * 0.1), (hx - r * 1.2, hy - r * 0.8), (hx - r * 0.5, hy + r * 0.25)], fill=_c(skin), outline=INK)
        if "skull" in extras:                                             # un crâne : orbites et dents
            d.ellipse([hx + r * 0.05, hy - r * 0.35, hx + r * 0.55, hy + r * 0.15], fill=(30, 24, 30, 255))
            d.rectangle([hx + r * 0.1, hy + r * 0.45, hx + r * 0.8, hy + r * 0.7], fill=(30, 24, 30, 255))
            for k in range(4):
                d.line([(hx + r * (0.15 + k * 0.17), hy + r * 0.45), (hx + r * (0.15 + k * 0.17), hy + r * 0.7)], fill=_c(skin), width=max(1, int(ow)))
        if "visor" in extras:                                             # une visière qui brille
            d.rectangle([hx - r * 0.1, hy - r * 0.35, hx + r * 1.02, hy + r * 0.05], fill=_c(extras["visor"]), outline=INK)
        if "helmet" in extras:                                            # le casque, son nasal
            col = _c(extras["helmet"])
            d.chord([hx - r * 1.1, hy - r * 1.2, hx + r * 1.05, hy + r * 0.55], 180, 360, fill=col, outline=INK)
            d.rectangle([hx + r * 0.42, hy - r * 0.4, hx + r * 0.62, hy + r * 0.45], fill=col, outline=INK)
            if "plume" in extras:
                pc = _c(extras["plume"])
                d.polygon([(hx - r * 0.2, hy - r * 1.05), (hx - r * 1.7, hy - r * 1.6), (hx - r * 1.4, hy - r * 0.6)], fill=pc, outline=INK)
        if "hat" in extras:                                               # chapeau à larges bords
            col = _c(extras["hat"])
            d.ellipse([hx - r * 1.6, hy - r * 0.75, hx + r * 1.7, hy - r * 0.35], fill=col, outline=INK)
            d.chord([hx - r * 0.9, hy - r * 1.55, hx + r * 0.95, hy - r * 0.2], 180, 360, fill=col, outline=INK)
        if "pointy" in extras:                                            # chapeau pointu de magicien
            col = _c(extras["pointy"])
            d.polygon([(hx - r * 1.2, hy - r * 0.5), (hx + r * 1.2, hy - r * 0.5), (hx - r * 0.6, hy - r * 2.6)], fill=col, outline=INK)
        if "band" in extras:                                              # bandeau
            col = _c(extras["band"])
            d.rectangle([hx - r * 1.0, hy - r * 0.62, hx + r * 0.95, hy - r * 0.38], fill=col)
            d.polygon([(hx - r * 0.9, hy - r * 0.55), (hx - r * 1.8, hy - r * 0.2), (hx - r * 1.6, hy + r * 0.1)], fill=col)
        if "wrap" in extras:                                              # bandelettes de momie
            col = _c(extras["wrap"])
            for k in range(6):
                y0 = 0.22 + k * 0.08
                d.line([P(-0.1, y0), P(0.1, y0 + 0.03)], fill=col, width=max(1, int(ow * 2.2)))
            d.line([(hx - r, hy - r * 0.2), (hx + r, hy + r * 0.1)], fill=col, width=max(1, int(ow * 2.5)))
        if weapon and weapon != "sword":
            _weapon(d, weapon, frame, front, u, ow, extras.get("metal", (220, 226, 236)))
    return fn


def _weapon(d, weapon, frame, hand, u, ow, metal):
    a = math.radians(WEAPON_ANGLE[frame])
    ca, sa = math.cos(a), math.sin(a)
    wood = (120, 80, 40, 255)
    mt = _c(metal)
    if weapon == "gun":                                                   # une arme à feu tenue à l'horizontale
        g = 0.0 if frame in (3, 0) else (-0.35 if frame == 4 else 0.25)
        ga, gs = math.cos(g), math.sin(g)
        tip = (hand[0] + ga * 0.2 * u, hand[1] + gs * 0.2 * u)
        bk = (hand[0] - ga * 0.08 * u, hand[1] - gs * 0.08 * u)
        d.line([bk, tip], fill=INK, width=max(3, int(0.05 * u)))
        d.line([bk, tip], fill=(70, 72, 80, 255), width=max(2, int(0.035 * u)))
        d.line([(hand[0], hand[1]), (hand[0] - 0.02 * u, hand[1] + 0.07 * u)], fill=(50, 50, 56, 255), width=max(2, int(0.03 * u)))
        return
    if weapon in ("spear", "halberd", "staff"):                           # une hampe longue tenue au milieu
        ln = 0.62 * u
        tip = (hand[0] + ca * ln * 0.62, hand[1] + sa * ln * 0.62)
        butt = (hand[0] - ca * ln * 0.38, hand[1] - sa * ln * 0.38)
        d.line([butt, tip], fill=INK, width=max(3, int(0.028 * u)))
        d.line([butt, tip], fill=wood, width=max(2, int(0.018 * u)))
        if weapon == "spear":
            d.polygon([(tip[0] + ca * 0.09 * u, tip[1] + sa * 0.09 * u), (tip[0] - sa * 0.025 * u, tip[1] + ca * 0.025 * u),
                       (tip[0] + sa * 0.025 * u, tip[1] - ca * 0.025 * u)], fill=mt, outline=INK)
        elif weapon == "halberd":
            d.polygon([(tip[0] + ca * 0.08 * u, tip[1] + sa * 0.08 * u), (tip[0] - sa * 0.09 * u + ca * 0.02 * u, tip[1] + ca * 0.09 * u + sa * 0.02 * u),
                       (tip[0] - sa * 0.07 * u - ca * 0.06 * u, tip[1] + ca * 0.07 * u - sa * 0.06 * u)], fill=mt, outline=INK)
        else:
            d.ellipse([tip[0] - 0.03 * u, tip[1] - 0.03 * u, tip[0] + 0.03 * u, tip[1] + 0.03 * u], fill=(120, 220, 255, 255), outline=INK)
        return
    ln = {"axe": 0.3, "mace": 0.3, "club": 0.32, "knife": 0.16, "claws": 0.12}[weapon] * u
    tip = (hand[0] + ca * ln, hand[1] + sa * ln)
    if weapon == "claws":
        for k in (-0.03, 0.0, 0.03):
            d.line([(hand[0], hand[1] + k * u), (tip[0], tip[1] + k * u)], fill=mt, width=max(1, int(0.012 * u)))
        return
    shaft = mt if weapon == "knife" else wood
    d.line([hand, tip], fill=INK, width=max(3, int(0.03 * u)))
    d.line([hand, tip], fill=shaft, width=max(2, int(0.02 * u)))
    if weapon == "axe":
        d.polygon([(tip[0] - ca * 0.06 * u, tip[1] - sa * 0.06 * u), (tip[0] - sa * 0.08 * u, tip[1] + ca * 0.08 * u),
                   (tip[0] - sa * 0.08 * u - ca * 0.1 * u, tip[1] + ca * 0.08 * u - sa * 0.1 * u)], fill=mt, outline=INK)
    elif weapon == "mace":
        d.ellipse([tip[0] - 0.045 * u, tip[1] - 0.045 * u, tip[0] + 0.045 * u, tip[1] + 0.045 * u], fill=mt, outline=INK)
        for k in range(6):
            aa = k * math.pi / 3
            d.line([tip, (tip[0] + math.cos(aa) * 0.065 * u, tip[1] + math.sin(aa) * 0.065 * u)], fill=INK, width=max(1, int(ow)))
    elif weapon == "club":
        d.ellipse([tip[0] - 0.035 * u, tip[1] - 0.035 * u, tip[0] + 0.035 * u, tip[1] + 0.035 * u], fill=wood, outline=INK)


def beast_draw(look, frame):
    """A creature of our own, facing right: "raptor" (a small dinosaur on two legs), "bug" (a six-legged crawler with
    mandibles and glowing eyes), "mech" (a walking war machine with a gun arm). Same frames as the fighters.
    / Une créature à nous : petit dinosaure, insecte à six pattes, machine de guerre qui marche."""
    kind, body, accent = look[0], look[1], look[2]

    def fn(d, W, H):
        u = H
        ow = max(1.0, H * 0.01)
        b, bd = _c(body), _mixc(body, (0, 0, 0), 0.3)
        ac = _c(accent)
        if kind == "raptor":
            if frame == 6:
                y = H * 0.9
                _capsule(d, (W * 0.2, y - 0.06 * u), (W * 0.62, y - 0.05 * u), 0.08 * u, 0.06 * u, b, INK, ow)
                d.line([(W * 0.62, y - 0.05 * u), (W * 0.95, y - 0.02 * u)], fill=b, width=max(2, int(0.05 * u)))
                d.ellipse([W * 0.06, y - 0.14 * u, W * 0.24, y - 0.02 * u], fill=b, outline=INK)
                return
            bob = 0.02 * (frame in (1, 2))
            lean = {3: 0.06, 5: -0.08}.get(frame, 0.0)
            hip = (W * 0.42, H * (0.5 + bob))
            for i, (kx, fx) in enumerate(((-0.02, -0.08), (0.04, 0.1)) if frame != 2 else ((0.04, 0.12), (-0.04, -0.1))):
                knee = (hip[0] + kx * u, H * 0.72)
                foot = (hip[0] + fx * u, H * 0.95)
                _capsule(d, hip, knee, 0.085 * u, 0.055 * u, bd if i == 0 else b, INK, ow)
                _capsule(d, knee, foot, 0.045 * u, 0.032 * u, bd if i == 0 else b, INK, ow)
                d.polygon([(foot[0] - 0.02 * u, foot[1]), (foot[0] + 0.08 * u, foot[1]), (foot[0] + 0.02 * u, foot[1] - 0.04 * u)], fill=INK)
            d.polygon([hip, (W * 0.02, H * (0.36 + bob)), (W * 0.05, H * (0.42 + bob)), (hip[0], hip[1] + 0.08 * u)], fill=b, outline=INK)   # la queue
            neck = (W * (0.62 + lean), H * (0.3 + bob))
            _capsule(d, hip, neck, 0.14 * u, 0.075 * u, b, INK, ow)
            for k in range(4):                                            # les rayures
                p0 = (hip[0] + (neck[0] - hip[0]) * (0.2 + k * 0.2), hip[1] + (neck[1] - hip[1]) * (0.2 + k * 0.2))
                d.line([(p0[0], p0[1] - 0.07 * u), (p0[0] - 0.03 * u, p0[1] + 0.02 * u)], fill=ac, width=max(1, int(0.02 * u)))
            jaw = 0.07 if frame == 3 else 0.02
            hx, hy = neck
            d.polygon([(hx - 0.05 * u, hy - 0.08 * u), (hx + 0.25 * u, hy - 0.05 * u), (hx + 0.25 * u, hy + 0.01 * u), (hx, hy + 0.04 * u)], fill=b,
                      outline=INK)
            d.polygon([(hx, hy + 0.03 * u), (hx + 0.22 * u, hy + (jaw + 0.01) * u), (hx + 0.02 * u, hy + 0.09 * u)], fill=bd, outline=INK)
            for k in range(4):                                            # les dents
                tx = hx + (0.06 + k * 0.045) * u
                d.polygon([(tx, hy + 0.01 * u), (tx + 0.02 * u, hy + 0.01 * u), (tx + 0.01 * u, hy + 0.035 * u)], fill=(250, 245, 230, 255))
            d.ellipse([hx + 0.04 * u, hy - 0.045 * u, hx + 0.075 * u, hy - 0.015 * u], fill=(255, 220, 60, 255))
            arm = (hx - 0.02 * u, hy + 0.12 * u)
            d.line([arm, (arm[0] + 0.08 * u, arm[1] + 0.06 * u)], fill=bd, width=max(2, int(0.025 * u)))
            return
        if kind == "bug":
            if frame == 6:
                y = H * 0.9
                d.ellipse([W * 0.15, y - 0.14 * u, W * 0.8, y], fill=b, outline=INK, width=int(ow))
                for k in range(6):
                    x = W * (0.25 + k * 0.09)
                    d.line([(x, y - 0.1 * u), (x + 0.03 * u, y - 0.26 * u)], fill=bd, width=max(2, int(0.02 * u)))
                return
            rise = {3: -0.06, 5: 0.04}.get(frame, 0.0)
            cy = H * (0.66 + rise * 0.3)
            step = 0.03 if frame in (1, 2) else 0.0
            for k in range(3):                                            # les six pattes
                x = W * (0.32 + k * 0.17)
                sgn = 1 if (k + frame) % 2 else -1
                for side, col in ((-1, bd), (1, b)):
                    knee = (x + side * 0.05 * u + sgn * step * u, cy - 0.1 * u)
                    foot = (x + side * 0.1 * u + sgn * step * u, H * 0.96)
                    d.line([(x, cy), knee, foot], fill=INK, width=max(3, int(0.028 * u)), joint="curve")
                    d.line([(x, cy), knee, foot], fill=col, width=max(2, int(0.018 * u)), joint="curve")
            d.ellipse([W * 0.12, cy - 0.16 * u, W * 0.62, cy + 0.08 * u], fill=b, outline=INK, width=int(ow))          # l'abdomen
            for k in range(3):
                x = W * (0.2 + k * 0.12)
                d.arc([x, cy - 0.15 * u, x + 0.16 * u, cy + 0.06 * u], 300, 60, fill=ac, width=max(1, int(0.015 * u)))
            d.polygon([(W * 0.12, cy - 0.04 * u), (W * 0.0, cy - 0.22 * u), (W * 0.05, cy - 0.02 * u)], fill=bd, outline=INK)  # le dard
            hx = W * (0.68 + (0.06 if frame == 3 else 0.0))
            hy = cy - (0.12 + (0.06 if frame == 3 else 0.0)) * u
            d.ellipse([hx - 0.1 * u, hy - 0.08 * u, hx + 0.1 * u, hy + 0.08 * u], fill=bd, outline=INK, width=int(ow))
            gap = 0.05 if frame == 3 else 0.02
            for sg in (-1, 1):                                            # les mandibules
                d.polygon([(hx + 0.07 * u, hy + sg * 0.02 * u), (hx + 0.18 * u, hy + sg * gap * u), (hx + 0.08 * u, hy + sg * 0.06 * u)], fill=ac, outline=INK)
            for ex in (0.0, 0.045):
                d.ellipse([hx + ex * u, hy - 0.05 * u, hx + (ex + 0.035) * u, hy - 0.015 * u], fill=(255, 80, 60, 255))
            return
        # mech: a war machine on two legs / une machine de guerre sur deux jambes
        if frame == 6:
            y = H * 0.92
            d.rounded_rectangle([W * 0.15, y - 0.2 * u, W * 0.7, y], radius=0.03 * u, fill=b, outline=INK, width=int(ow))
            d.ellipse([W * 0.62, y - 0.16 * u, W * 0.86, y], fill=bd, outline=INK, width=int(ow))
            d.line([(W * 0.3, y - 0.24 * u), (W * 0.42, y - 0.36 * u)], fill=(120, 120, 130, 255), width=max(2, int(0.02 * u)))
            return
        lean = {3: 0.05, 5: -0.06}.get(frame, 0.0) * u
        cx = W * 0.5 + lean
        hipy = H * 0.56
        legs = {1: (-0.08, 0.1), 2: (0.08, -0.06)}.get(frame, (-0.07, 0.07))
        for i, lx in enumerate(legs):
            knee = (W * 0.5 + lx * u * 0.6, H * 0.74)
            foot = (W * 0.5 + lx * u, H * 0.95)
            _capsule(d, (cx, hipy), knee, 0.06 * u, 0.055 * u, bd if i == 0 else b, INK, ow)
            _capsule(d, knee, foot, 0.055 * u, 0.05 * u, bd if i == 0 else b, INK, ow)
            d.rounded_rectangle([foot[0] - 0.07 * u, foot[1] - 0.04 * u, foot[0] + 0.09 * u, foot[1] + 0.01 * u], radius=0.01 * u, fill=bd, outline=INK)
        d.rounded_rectangle([cx - 0.16 * u, H * 0.24, cx + 0.14 * u, H * 0.58], radius=0.05 * u, fill=b, outline=INK, width=int(ow * 1.5))
        d.rounded_rectangle([cx - 0.02 * u, H * 0.3, cx + 0.12 * u, H * 0.4], radius=0.02 * u, fill=(40, 60, 80, 255), outline=INK)   # le cockpit
        d.rectangle([cx + 0.0 * u, H * 0.32, cx + 0.1 * u, H * 0.345], fill=_mixc(accent, (255, 255, 255), 0.4))
        d.rectangle([cx - 0.16 * u, H * 0.44, cx + 0.14 * u, H * 0.47], fill=ac)
        reach = 0.22 if frame == 3 else (0.12 if frame == 4 else 0.08)
        sh = (cx + 0.06 * u, H * 0.33)
        hand = (sh[0] + reach * u, H * (0.38 if frame != 5 else 0.3))
        _capsule(d, (cx - 0.12 * u, H * 0.33), (cx - 0.14 * u, H * 0.5), 0.05 * u, 0.045 * u, bd, INK, ow)
        _capsule(d, sh, hand, 0.05 * u, 0.045 * u, b, INK, ow)
        d.rectangle([hand[0], hand[1] - 0.025 * u, hand[0] + 0.14 * u, hand[1] + 0.02 * u], fill=(70, 72, 80, 255), outline=INK)    # le canon
        d.ellipse([cx - 0.15 * u, H * 0.18, cx - 0.03 * u, H * 0.27], fill=ac, outline=INK)      # le radar
    return fn


# ============================================================================ shared scene of the CPS brawlers
class CapcomBrawler(BrawlerScene):
    """The beat'em ups of Capcom: the hero (the one chosen when the game says it), the foes of the game with their
    name and their gauge when a blow lands, a bomb or a special that sweeps the street, the level that goes up, and the
    top bar of each game. / Les beat'em ups de Capcom : le héros choisi, les ennemis avec leur nom et leur jauge quand un
    coup porte, la bombe ou le coup spécial qui balaie la rue, le niveau qui monte, la barre du haut de chaque jeu."""
    ENERGY = "health"
    ENERGY_MAX = 100
    HEROES = {}                    # value of _p1_chr -> look / valeur de _p1_chr -> apparence
    FOE_NAMES = ("THUG",)
    SPECIAL = None                 # value whose fall is a bomb or a special attack / valeur dont la baisse est une bombe
    SPECIAL_WORD = ("SPÉCIAL !", "SPECIAL!")
    TAG = (255, 230, 120)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.hero0 = self.HERO
        self.tag = None
        self.specials = 0                                                 # (tests)
        for look in self.HEROES.values():
            if look != self.HERO:
                self.warm += [(self.fig, (look, f, False)) for f in (0, 3, 5)]

    SIZES = {}                     # style -> size factor (big war machines) / style -> facteur de taille

    def fig(self, look, frame, left):
        S = self.S
        k = self.SIZES.get(look[0], 1.0)
        if look[0] in BEASTS:
            w = {"raptor": 300, "bug": 270, "mech": 250}[look[0]]
            return self.img(("cbeast", look, frame, left), S(w * k), S(250 * k), beast_draw(look, frame), ss=2, flip=left)
        weapon = look[5] if len(look) > 5 else None
        w = 420 if weapon in LONG else (280 if weapon else 190)
        return self.img(("chero", look, frame, left), S(w * k), S(250 * k), hero_draw(look, frame), ss=2, flip=left)

    def face(self, look, size):
        """The hero's head cut out of his figure, for the portrait. / La tête du héros, découpée dans sa figure."""
        key = ("cface", look, size)
        surf = self.imgs.get(key)
        if surf is None:
            fig = self.fig(look, 0, False)
            w, h = fig.get_size()
            if look[0] in BEASTS:
                x0, y0, side = w * 0.48, h * 0.12, h * 0.42
            else:
                side = 0.26 * h
                x0, y0 = w * 0.5 + 0.02 * h - side / 2, 0.15 * h - side * 0.55
            x0, y0 = max(0, int(x0)), max(0, int(y0))
            side = int(min(side, w - x0, h - y0))
            surf = self.imgs[key] = self.pg.transform.smoothscale(fig.subsurface((x0, y0, side, side)), (size, size))
        return surf

    def always(self, vals, now):
        ch = _n(vals.get("_p1_chr"))
        self.HERO = self.HEROES.get(int(ch), self.hero0) if ch is not None and self.HEROES else self.hero0

    def strike(self, now, dmg=1):
        """The hero hits the nearest foe: a blade leaves its trail, a gun fires, the foe's name and gauge show.
        / Le héros frappe : une lame laisse sa traînée, une arme à feu tire, le nom et la jauge de l'ennemi s'affichent."""
        f = self.nearest()
        if f is None:
            return
        S, fx = self.S, self.fx
        h = self.hero
        weapon = "gun" if self.HERO[0] == "mech" else (self.HERO[5] if len(self.HERO) > 5 else None)
        if weapon == "gun":
            h["face"] = 1 if f["x"] > h["x"] else -1
            h["act"] = (now, 3)
            self.blows += 1
            y = self.ground(h["z"]) - S(160)
            mx = h["x"] + h["face"] * S(75)
            fx.muzzle(mx, y, 0 if h["face"] > 0 else 180, 0.7)
            fx.tracer(mx, y, f["x"], self.ground(f["z"]) - S(150), color=(255, 240, 180), width=3, length=90)
            f["hp"] -= dmg
            f["hurt"] = now
            if f["hp"] <= 0:
                self.knocked += 1
                f["down"] = now
                f["vx"] = h["face"] * S(420)
                fx.shake(4, 0.2)
        else:
            super().strike(now, dmg)                                      # the sword: frame 3 and its trail (BrawlerScene)
            if weapon and weapon != "sword":
                h["act"] = (now, 3)
                if weapon in BLADES:
                    self.slashes.append((h["x"] + h["face"] * S(60), self.ground(h["z"]) - S(150), now, h["face"]))
        self.tag = (f, now)

    def update(self, vals, now):
        for f in self.foes:
            if "name" not in f:
                f["name"] = self.rng.choice(self.FOE_NAMES)
                f["hp0"] = f["hp"]
        super().update(vals, now)
        for f in self.foes:
            if "name" not in f:
                f["name"] = self.rng.choice(self.FOE_NAMES)
                f["hp0"] = max(1, f["hp"])
        if self.SPECIAL:
            ch = self.changed(vals, self.SPECIAL)
            if ch and ch[1] < ch[0]:
                self.special(now)
        ch = self.changed(vals, "level")
        if ch and ch[1] > ch[0]:
            h = self.hero
            self.fx.glow(h["x"], self.ground(h["z"]) - self.S(130), 30, 200, (255, 230, 140), 0.6, "front", 0.9, 0.0)
            self.popup(tr("NIVEAU SUPÉRIEUR !", "LEVEL UP!"), h["x"], self.ground(h["z"]) - self.S(300), GOLD, 42)

    def special(self, now):
        """A bomb or a special attack: the foes near the hero fly away. / Une bombe ou un coup spécial balaie la rue."""
        S, fx = self.S, self.fx
        h = self.hero
        self.specials += 1
        fx.flash((255, 230, 160), 0.25, 0.3)
        for i in range(8):
            fx.later(i * 0.04, fx.glow, h["x"] + math.cos(i * 0.8) * S(220), self.ground(h["z"]) - S(140) + math.sin(i * 0.8) * S(70), 30, 150,
                     (255, 210, 120), 0.4, "front", 1.0, 0.0)
        for f in self.foes:
            if f["hp"] > 0 and abs(f["x"] - h["x"]) < self.W * 0.45:
                f["hp"] = 0
                f["down"] = now
                f["vx"] = (1 if f["x"] > h["x"] else -1) * S(520)
                self.knocked += 1
        fx.shake(7, 0.3)
        self.popup(tr(*self.SPECIAL_WORD), h["x"], self.ground(h["z"]) - S(300), GOLD, 42)

    # ------------------------------------------------------------ the top bar, as in each game
    def foe_tag(self, screen, x, y, now, color=(255, 70, 60), w=None):
        """The name and the gauge of the foe just hit, under the hero's, as in the Capcom brawlers.
        / Le nom et la jauge de l'ennemi qu'on vient de frapper, sous ceux du héros."""
        if self.tag is None or now - self.tag[1] > 2.5:
            return
        S = self.S
        f = self.tag[0]
        w = w or S(300)
        self.text(screen, f["name"], x, y, 24, WHITE, key="black", valign="middle")
        self.bar(screen, x, y + S(16), w, S(14), max(0, f["hp"]) / float(max(1, f.get("hp0", 3))), color, back=(50, 20, 20))

    def portrait(self, screen, x, y, size, border=(255, 230, 120)):
        S, pg = self.S, self.pg
        pg.draw.rect(screen, (10, 12, 24), (int(x), int(y), int(size), int(size)))
        screen.blit(self.face(self.HERO, int(size) - S(6)), (int(x) + S(3), int(y) + S(3)))
        pg.draw.rect(screen, border, (int(x), int(y), int(size), int(size)), max(1, S(3)))

    @staticmethod
    def name(vals, default="1P"):
        """The name of the character chosen, read in the game, else 1P. / Le nom du personnage choisi, sinon 1P."""
        v = vals.get("p1_char")
        return v if isinstance(v, str) and v else default

    NAME_COL = WHITE
    BAR = ((255, 220, 40), (170, 30, 30))      # gauge colour and the colour under it / couleur de la jauge et du fond
    LIVES = " ={}"                              # how the lives follow the name / comment les vies suivent le nom
    PILL_W = 560

    def hud(self, screen, eng, vals, logo, now, name=None, foe_col=None):
        """The top left box of the Capcom brawlers: the portrait, the name and the lives, the score, the gauge, the foe
        just hit. Returns the right edge of the box. / L'encadré du haut à gauche : portrait, nom et vies, score, jauge,
        l'ennemi qu'on vient de frapper."""
        S, W, hd = self.S, self.W, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        w = S(self.PILL_W)
        self.pill(screen, S(12), S(6), w, S(150), 160, radius=14)
        self.portrait(screen, S(24), S(18), S(64))
        lives = _n(vals.get("lives"))
        txt = (name or self.name(vals)) + (self.LIVES.format(int(lives)) if lives is not None else "")
        self.text(screen, txt, S(102), S(32), 30, self.NAME_COL, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(12) + w - S(16), S(12), "right", S(40))
        e = _n(vals.get("health"))
        if e is not None:
            self.bar(screen, S(102), S(60), w - S(110), S(22), e / 100.0, self.BAR[0], back=self.BAR[1])
        self.foe_tag(screen, S(102), S(108), now, foe_col or self.BAR[0], S(300))
        return S(12) + w

    def invite_right(self, screen, vals, now):
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, self.W - self.S(24), self.S(40), 30, col, align="right")

    def time_box(self, screen, vals, x, y, label_col, num_col, key="stencil", size=64, label="TIME"):
        t = _n(vals.get("time"))
        if t is None:
            return
        S, hd = self.S, self.hd
        self.pill(screen, x - S(80), y, S(160), S(108), 170, radius=14)
        self.text(screen, label, x, y + S(18), 28, label_col, key=key, align="center", valign="middle")
        hd.put_number(screen, f"{int(t):02d}", key, S(size), num_col, x, y + S(66), "center", "middle")


# ============================================================================ Final Fight
class FinalFightScene(CapcomBrawler):
    """Final Fight as in the game: the slum of a big American city by day, its pinkish brick tenements, the iron fire
    escapes and the grey sidewalk; our street fighter of our own in a red tank top faces the gang that comes from both
    sides. The portrait, the name and =lives, the score, the yellow gauge over red, TIME in big purple numbers, the name
    and the gauge of the thug just hit under it. / Le quartier pauvre d'une grande ville de jour ; notre combattant à
    nous affronte le gang qui arrive des deux côtés. Portrait, =vies, score, jauge jaune sur rouge, TIME en violet."""
    THEME = "ff_slum"
    HERO = ("brawler", (220, 70, 56), (44, 46, 58), (226, 176, 136), (60, 40, 30))
    FOES = (("thug", (70, 110, 200), (60, 60, 70), (214, 160, 120), (30, 30, 34)),
            ("jacket", (200, 60, 50), (50, 50, 60), (200, 150, 110), (40, 30, 26)),
            ("brawler", (240, 200, 60), (90, 70, 50), (190, 140, 100), (200, 60, 40), None, (("band", (240, 70, 60)),)),
            ("thug", (120, 60, 140), (40, 40, 50), (226, 176, 136), (240, 240, 240), "knife"))
    FOE_NAMES = ("SLIM", "BRUNO", "RUSTY", "VINNIE", "TEX", "ROCCO", "DUKE", "MOE")

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the portrait, the name and =lives, the score, the yellow gauge over red, TIME in purple, the
        gauge of the foe just hit. / Comme dans le jeu : portrait, nom et =vies, score, jauge jaune sur rouge, TIME."""
        right = self.hud(screen, eng, vals, logo, now)
        self.time_box(screen, vals, right + self.S(96), self.S(8), (170, 120, 255), (190, 150, 255))
        self.invite_right(screen, vals, now)


# ============================================================================ Captain Commando
class CaptainCommandoScene(CapcomBrawler):
    """Captain Commando as in the game: a city of the future by day, the glass fronts and their neon strips, the light
    marble floor; the hero chosen in the game (a hero of our own for each: the wrapped knife fighter, the captain with
    his visor, the ninja, the little pilot in his walking machine) against the punks and the cyborgs. 1P and the score,
    the name in blue, the green gauge. / Une ville du futur de jour ; le héros choisi dans le jeu (un héros à nous pour
    chacun) contre les voyous et les cyborgs. 1P et le score, le nom en bleu, la jauge verte."""
    THEME = "cc_future"
    HERO = ("jacket", (232, 232, 242), (56, 60, 84), (226, 176, 136), (60, 40, 30), None, (("helmet", (196, 202, 220)), ("visor", (255, 200, 60))))
    HEROES = {0: ("brawler", (222, 208, 172), (204, 190, 156), (214, 200, 166), (204, 190, 156), "knife", (("wrap", (244, 236, 210)),)),
              1: HERO,
              2: ("ninja", (60, 62, 84), (50, 52, 70), (226, 176, 136), (0, 0, 0), "sword"),
              3: ("mech", (80, 120, 200), (255, 200, 60))}
    FOES = (("thug", (240, 120, 40), (60, 60, 80), (214, 160, 120), (40, 40, 50)),
            ("cyborg", (140, 160, 180), (80, 90, 110), (226, 176, 136), (255, 60, 60)),
            ("mutant", (120, 90, 160), (70, 60, 90), (190, 150, 210), (90, 40, 110)),
            ("jacket", (60, 200, 200), (40, 40, 50), (200, 150, 110), (240, 60, 160), "knife"))
    FOE_NAMES = ("SKIP", "BLADE", "ZOOK", "MAXX", "KRAG", "RONIN", "VOLT")
    NAME_COL = (120, 200, 255)
    BAR = ((170, 230, 60), (40, 60, 30))
    LIVES = "  x{}"

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and the score, the name of the hero in blue, the green gauge. / 1P, le score, le nom en bleu."""
        self.hud(screen, eng, vals, logo, now, name=self.name(vals, "1P"))
        self.invite_right(screen, vals, now)


# ============================================================================ Cadillacs and Dinosaurs
class CadillacsScene(CapcomBrawler):
    """Cadillacs and Dinosaurs as in the game: a town swallowed by the jungle under a hot sky, volcanoes far off, broken
    columns taken by the vines, a big old car on the dusty road; the hero chosen in the game (a hero of our own for
    each: the hunter with his rifle, the mechanic with his wrench, the explorer, the bruiser) against the poachers and
    the little dinosaurs. =lives and the name, the score, the yellow gauge, the time. / Une ville avalée par la jungle ;
    le héros choisi (un héros à nous pour chacun) contre les braconniers et les petits dinosaures."""
    THEME = "cd_ruins"
    HERO = ("jacket", (214, 184, 124), (60, 80, 124), (226, 176, 136), (110, 70, 40), "gun", (("hat", (124, 84, 44)),))
    HEROES = {0: HERO,
              1: ("jacket", (240, 170, 50), (90, 70, 50), (190, 140, 100), (30, 26, 24), "club", (("band", (40, 120, 200)),)),
              2: ("jacket", (60, 150, 90), (70, 60, 50), (236, 190, 150), (200, 100, 40), "knife", (("longhair", (200, 100, 40)),)),
              3: ("brawler", (200, 50, 40), (60, 60, 70), (210, 160, 120), (50, 40, 30), None, (("band", (236, 236, 236)),))}
    FOES = (("thug", (110, 120, 70), (70, 60, 50), (214, 160, 120), (60, 50, 40), "gun"),
            ("brawler", (130, 100, 70), (60, 60, 60), (200, 150, 110), (30, 30, 30), "knife"),
            ("raptor", (110, 150, 70), (60, 90, 40)), ("raptor", (170, 120, 60), (110, 70, 40)))
    FOE_NAMES = ("POACHER", "BUTCH", "HOGG", "SLICK", "RAPTOR", "VICE")

    def hud_name(self, vals):
        lives = _n(vals.get("lives"))
        return (f"={int(lives)} " if lives is not None else "") + self.name(vals, "1P")

    def status(self, screen, eng, vals, logo, now):
        """As in the game: =lives then the name, the score, the yellow gauge, the time. / =vies puis le nom, le score."""
        right = self.hud(screen, eng, dict(vals, lives=None), logo, now, name=self.hud_name(vals))
        self.time_box(screen, vals, right + self.S(96), self.S(8), (255, 220, 120), (255, 240, 200))
        self.invite_right(screen, vals, now)


# ============================================================================ The Punisher
class PunisherScene(CapcomBrawler):
    """The Punisher as in the game: the hall of a mobster's mansion at night, purple walls and gold trims, chandeliers
    and the red carpet; our vigilante of our own in his dark suit, his gun in hand, against the mobsters. The portrait,
    1P and xlives, the score, the cyan gauge, TIME in yellow, the grenades at the bottom left: a grenade thrown sweeps the
    hall. / Le hall d'une villa de gangster la nuit ; notre justicier à nous, en costume sombre, arme au poing, contre
    les mafieux. Jauge cyan, TIME en jaune, les grenades en bas à gauche : une grenade lancée balaie le hall."""
    THEME = "pn_mansion"
    HERO = ("jacket", (44, 48, 60), (36, 38, 48), (226, 176, 136), (40, 30, 26), "gun")
    FOES = (("jacket", (60, 60, 70), (50, 50, 60), (214, 160, 120), (30, 30, 34)),
            ("thug", (150, 40, 40), (40, 40, 50), (226, 176, 136), (20, 20, 24), "knife"),
            ("brawler", (230, 230, 230), (80, 60, 50), (200, 150, 110), (240, 200, 60), "club"),
            ("jacket", (110, 70, 140), (40, 40, 50), (190, 140, 100), (50, 40, 30), "gun"))
    FOE_NAMES = ("PAULIE", "FRANKIE", "BIG TONY", "NICKY", "SAL", "LOUIE")
    SPECIAL = "bombs"
    SPECIAL_WORD = ("GRENADE !", "GRENADE!")
    BAR = ((60, 220, 240), (30, 40, 60))
    LIVES = " x{}"

    def special(self, now):
        h = self.hero
        self.fx.explosion(h["x"] + h["face"] * self.S(320), self.ground(h["z"]) - self.S(100), 1.2)
        super().special(now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and xlives, the score, the cyan gauge, TIME in yellow, the grenades at the bottom left.
        / Comme dans le jeu : 1P et xvies, le score, la jauge cyan, TIME en jaune, les grenades en bas à gauche."""
        S, H = self.S, self.H
        right = self.hud(screen, eng, vals, logo, now)
        self.time_box(screen, vals, right + S(96), S(8), (255, 220, 60), (255, 230, 60))
        b = _n(vals.get("bombs"))
        if b is not None:
            pg = self.pg
            self.pill(screen, S(12), H - S(70), S(170), S(60), 160, radius=14)
            pg.draw.circle(screen, (70, 100, 60), (S(50), H - S(40)), S(17))
            pg.draw.rect(screen, (60, 60, 60), (S(44), H - S(64), S(12), S(9)))
            pg.draw.circle(screen, (20, 30, 20), (S(50), H - S(40)), S(17), max(1, S(2)))
            self.text(screen, f"x{int(b)}", S(80), H - S(40), 32, WHITE, key="black", valign="middle")
        self.invite_right(screen, vals, now)


# ============================================================================ The King of Dragons
class KingOfDragonsScene(CapcomBrawler):
    """The King of Dragons as in the game: a forest of huge old trees in the sun, blue mountains far off, the meadow;
    our knight of our own with his helmet, his plume, his sword and his shield against the orcs, the dog-men, the
    skeletons and the lizard-men. EP and the experience read in the game, the class and the level that goes up, the
    gauge. / Une forêt d'arbres immenses ; notre chevalier à nous contre les orques, les hommes-chiens, les squelettes.
    EP et l'expérience lue dans le jeu, la classe et le niveau qui monte, la jauge."""
    THEME = "kd_forest"
    HERO = ("jacket", (170, 170, 186), (90, 90, 104), (226, 176, 136), (220, 190, 90), "sword",
            (("helmet", (200, 205, 216)), ("plume", (230, 40, 40)), ("shield", (40, 80, 170))))
    FOES = (("mutant", (110, 80, 50), (80, 60, 40), (110, 160, 80), (60, 50, 30), "axe", (("tusks", None),)),
            ("mutant", (150, 110, 60), (90, 70, 40), (170, 130, 80), (110, 80, 40), "spear", (("ears", None),)),
            ("brawler", (232, 226, 212), (222, 216, 202), (236, 232, 216), (236, 232, 216), "sword", (("skull", None),)),
            ("mutant", (60, 120, 90), (60, 90, 60), (90, 170, 110), (40, 100, 60), "mace"))
    FOE_NAMES = ("ORC", "GNOLL", "SKELETON", "LIZARDMAN", "HOBGOBLIN", "BUGBEAR")
    BAR = ((80, 220, 90), (40, 40, 60))
    LIVES = "  x{}"

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the class and its level L, the gauge, EP and the experience. / La classe et son niveau L, EP."""
        S = self.S
        lv = _n(vals.get("level"))
        name = tr("CHEVALIER", "FIGHTER") + (f"  L {int(lv)}" if lv is not None else "")
        self.hud(screen, eng, dict(vals, score=None), logo, now, name=name)
        if _n(vals.get("score")) is not None:                             # EP and the experience, right of the logo
            x = self.W / 2 + S(220)
            self.pill(screen, x, S(6), S(330), S(64), 160, radius=14)
            self.text(screen, "EP", x + S(18), S(38), 28, (120, 200, 255), key="black", valign="middle")
            self.hd._score(screen, eng, "score", x + S(314), S(14), "right", S(40))
        self.invite_right(screen, vals, now)


# ============================================================================ Knights of the Round
class KnightsScene(CapcomBrawler):
    """Knights of the Round as in the game: a village of half-timbered houses with the castle on the hill; our knight
    of our own in his blue tabard and red cape against the soldiers, the barbarians and the dark knights. The portrait,
    1P and the score, xlives, the level L-, the red gauge. / Un village de maisons à colombages ; notre chevalier à nous
    contre les soldats, les barbares et les chevaliers noirs. Score, xvies, le niveau L-, la jauge rouge."""
    THEME = "kn_village"
    HERO = ("jacket", (40, 70, 160), (90, 90, 100), (226, 176, 136), (200, 160, 60), "sword", (("armor", (190, 195, 210)), ("cape", (160, 30, 40))))
    FOES = (("jacket", (120, 110, 90), (80, 70, 60), (214, 160, 120), (60, 50, 40), "spear", (("helmet", (150, 150, 160)),)),
            ("brawler", (150, 100, 60), (90, 60, 40), (200, 150, 110), (180, 80, 30), "axe", (("beard", (180, 80, 30)),)),
            ("jacket", (60, 60, 70), (60, 60, 70), (214, 160, 120), (30, 30, 34), "sword", (("helmet", (90, 90, 100)), ("shield", (120, 30, 30)))))
    FOE_NAMES = ("SOLDIER", "BARBARIAN", "AXEMAN", "DARK KNIGHT", "GUARD")
    BAR = ((240, 60, 50), (50, 30, 30))
    LIVES = "  x{:02d}"

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P, xlives, the score, the red gauge, the level L- under it. / 1P, xvies, le score, la jauge, L-."""
        S = self.S
        right = self.hud(screen, eng, vals, logo, now)
        lv = _n(vals.get("level"))
        if lv is not None:
            self.label(screen, f"L-{int(lv)}", right + S(70), S(40), 30, (255, 220, 120), align="center")
        self.invite_right(screen, vals, now)


# ============================================================================ Warriors of Fate
class WarriorsOfFateScene(CapcomBrawler):
    """Warriors of Fate as in the game: a forest of ancient China, sharp peaks in the mist, the wooden palisade of a camp
    with its banners and its barrels; our general of our own in red armour with his halberd against the soldiers and
    the bandits. The portrait, 1P and xlives, the score, the yellow-green gauge, the time. / Une forêt de la Chine
    ancienne ; notre général à nous, armure rouge et hallebarde, contre les soldats et les bandits."""
    THEME = "wf_forest"
    HERO = ("samurai", (200, 40, 40), (90, 60, 40), (226, 176, 136), (230, 190, 60), "halberd")
    FOES = (("jacket", (60, 90, 160), (60, 60, 70), (214, 160, 120), (40, 40, 40), "spear", (("hat", (180, 150, 90)),)),
            ("brawler", (140, 100, 70), (70, 60, 50), (200, 150, 110), (30, 30, 30), "sword", (("band", (200, 40, 40)),)),
            ("jacket", (90, 120, 80), (60, 60, 50), (214, 160, 120), (40, 40, 40), "spear", (("helmet", (110, 100, 80)),)))
    FOE_NAMES = ("SOLDIER", "BANDIT", "SPEARMAN", "ARCHER", "CAPTAIN")
    BAR = ((200, 230, 40), (60, 40, 20))
    LIVES = " x{}"

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P and xlives, the score, the yellow-green gauge, the time. / 1P et xvies, le score, la jauge."""
        right = self.hud(screen, eng, vals, logo, now)
        self.time_box(screen, vals, right + self.S(96), self.S(8), (255, 220, 120), (255, 240, 200))
        self.invite_right(screen, vals, now)


# ============================================================================ Dungeons & Dragons: Shadow over Mystara
class MystaraScene(CapcomBrawler):
    """Dungeons & Dragons: Shadow over Mystara as in the game: a canyon of warm sandstone, a dark castle on a far peak;
    our hero of our own with his helmet, his mace and his shield against the goblins, the dog-men, the trolls and the
    skeletons. The portrait, 1P, the score, the green gauge. / Un canyon de grès ; notre héros à nous, casque, masse et
    bouclier, contre les gobelins, les hommes-chiens, les trolls et les squelettes."""
    THEME = "ds_canyon"
    HERO = ("jacket", (60, 90, 170), (120, 100, 70), (226, 176, 136), (110, 70, 40), "mace",
            (("helmet", (190, 190, 200)), ("shield", (170, 140, 60)), ("cape", (40, 50, 120))))
    FOES = (("mutant", (120, 90, 50), (90, 70, 40), (120, 170, 80), (60, 50, 30), "club", (("ears", None),)),
            ("mutant", (150, 110, 60), (90, 70, 40), (170, 130, 80), (110, 80, 40), "spear", (("ears", None),)),
            ("mutant", (80, 110, 70), (70, 80, 60), (100, 150, 90), (50, 80, 40), None, (("tusks", None),)),
            ("brawler", (232, 226, 212), (222, 216, 202), (236, 232, 216), (236, 232, 216), "sword", (("skull", None),)))
    FOE_NAMES = ("GOBLIN", "GNOLL", "TROLL", "SKELETON", "KOBOLD")
    BAR = ((80, 220, 90), (40, 40, 60))

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the portrait, 1P, the score, the green gauge. / Le portrait, 1P, le score, la jauge verte."""
        self.hud(screen, eng, vals, logo, now)
        self.invite_right(screen, vals, now)


# ============================================================================ Dungeons & Dragons: Tower of Doom
class TowerOfDoomScene(CapcomBrawler):
    """Dungeons & Dragons: Tower of Doom as in the game: green hills in the golden light, a walled town far off, a
    signpost and a treasure chest; our elf of our own with her cloak and her sword against the kobolds, the orcs and the
    skeletons. The four places of the players at the bottom, as in the game: ours with its gauge, JOIN IN! in the others.
    / Des collines vertes dans la lumière dorée ; notre elfe à nous contre les kobolds, les orques et les squelettes.
    Les quatre places des joueurs en bas : la nôtre et sa jauge, JOIN IN! dans les autres."""
    THEME = "dt_hills"
    SHADE = (90, 110)
    HERO = ("jacket", (60, 130, 70), (110, 90, 60), (236, 196, 156), (230, 210, 120), "sword",
            (("ears", None), ("cape", (40, 90, 50)), ("longhair", (230, 210, 120))))
    FOES = (("mutant", (150, 70, 50), (100, 70, 40), (170, 110, 70), (120, 70, 40), "spear", (("ears", None),)),
            ("mutant", (110, 80, 50), (80, 60, 40), (110, 160, 80), (60, 50, 30), "axe", (("tusks", None),)),
            ("brawler", (232, 226, 212), (222, 216, 202), (236, 232, 216), (236, 232, 216), "sword", (("skull", None),)))
    FOE_NAMES = ("KOBOLD", "ORC", "GNOLL", "HOBGOBLIN", "SKELETON")

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the foe's name at the top, the four places of the players at the bottom. / Le nom de l'ennemi
        en haut, les quatre places des joueurs en bas."""
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        if self.tag is not None and now - self.tag[1] < 2.5:
            self.label(screen, self.tag[0]["name"], W / 2, S(110), 30, (255, 230, 120), key="black", align="center")
        bw = (W - S(40)) / 4
        for k in range(4):
            x = S(12) + k * (bw + S(5))
            self.box(screen, x, H - S(78), bw, S(70), (200, 170, 90), fill=(14, 12, 30, 200), radius=10)
            if k == 0:
                self.portrait(screen, x + S(10), H - S(70), S(54))
                self.text(screen, "1P", x + S(76), H - S(56), 26, WHITE, key="black", valign="middle")
                if _n(vals.get("score")) is not None:
                    hd._score(screen, eng, "score", x + bw - S(14), H - S(76), "right", S(34))
                e = _n(vals.get("health"))
                if e is not None:
                    self.bar(screen, x + S(76), H - S(34), bw - S(92), S(18), e / 100.0, (80, 220, 90), back=(40, 40, 60))
            elif k == 1 and self.p2_in(vals):
                self.text(screen, "2P", x + bw / 2, H - S(43), 30, WHITE, key="black", align="center", valign="middle")
            else:
                word, col = ("JOIN IN!", (255, 230, 120)) if _n(vals.get("credits")) else self.invite(vals, now)
                self.text(screen, "JOIN IN!" if k else word, x + bw / 2, H - S(43), 30, col, key="black", align="center", valign="middle")


# ============================================================================ Alien vs. Predator
class AlienVsPredatorScene(CapcomBrawler):
    """Alien vs. Predator as in the game: a ruined industrial city at dusk in a green haze, big pipes and the wreck of a
    hover tank; the hero chosen in the game (a hero of our own for each: two masked hunters of the stars with their
    claws or their spear, the soldier with his gun, the cyborg with her sword) against the crawling creatures of our own.
    The name and xlives, the score, the yellow gauge, the gauge of the special that fills: when it empties, the special
    sweeps the street. / Une ville industrielle en ruine ; le héros choisi (un héros à nous pour chacun) contre nos
    créatures rampantes. Quand la jauge du coup spécial se vide, le coup balaie la rue."""
    THEME = "av_ruins"
    HERO = ("cyborg", (120, 110, 90), (90, 80, 60), (226, 176, 136), (255, 60, 40), "claws", (("armor", (150, 140, 110)),))
    HEROES = {0: HERO,
              1: ("jacket", (110, 120, 80), (70, 80, 60), (226, 176, 136), (90, 60, 30), "gun", (("band", (70, 80, 50)),)),
              2: ("cyborg", (90, 100, 110), (70, 70, 80), (226, 176, 136), (60, 220, 255), "spear", (("armor", (120, 130, 140)),)),
              3: ("cyborg", (220, 220, 230), (60, 70, 120), (236, 196, 156), (255, 90, 160), "sword", (("longhair", (40, 40, 60)),))}
    FOES = (("bug", (50, 70, 70), (120, 200, 160)), ("bug", (90, 60, 50), (200, 120, 60)), ("bug", (60, 60, 80), (170, 120, 220)))
    FOE_NAMES = ("CRAWLER", "STALKER", "SPITTER", "BRUTE", "DRONE")
    SPECIAL = "power"
    BAR = ((255, 220, 40), (60, 30, 30))
    LIVES = " x{}"

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the name and xlives, the score, the yellow gauge, the special gauge. / Le nom, la jauge spéciale."""
        S = self.S
        self.hud(screen, eng, vals, logo, now, name=self.name(vals, "1P"))
        pw = _n(vals.get("power"))
        if pw is not None:                                                # the special gauge, right of the logo
            x = self.W / 2 + S(220)
            self.pill(screen, x, S(6), S(260), S(64), 160, radius=14)
            self.text(screen, "SP", x + S(18), S(38), 26, (120, 230, 255), key="black", valign="middle")
            self.bar(screen, x + S(70), S(28), S(170), S(20), pw / 100.0, (90, 210, 255), back=(20, 30, 50))
        self.invite_right(screen, vals, now)


# ============================================================================ Armored Warriors
class ArmoredWarriorsScene(CapcomBrawler):
    """Armored Warriors as in the game: the hangar of the war machines, teal steel, shutters and hazard stripes; the
    machine chosen in the game (one of our own for each, in its colours) fires on the enemy machines. 1P- and the score,
    the name and xlives, the gauge. / Le hangar des machines de guerre ; la machine choisie (une à nous pour chacune)
    tire sur les machines ennemies. 1P- et le score, le nom et xvies, la jauge."""
    THEME = "aw_hangar"
    HERO = ("mech", (200, 60, 50), (255, 220, 80))
    HEROES = {0: HERO, 1: ("mech", (70, 150, 90), (250, 240, 120)), 2: ("mech", (200, 170, 60), (120, 200, 255)),
              3: ("mech", (70, 110, 190), (255, 160, 60))}
    FOES = (("mech", (120, 120, 110), (255, 70, 60)), ("mech", (90, 100, 80), (255, 200, 60)),
            ("robot", (150, 160, 190), (90, 96, 120), (0, 0, 0), (0, 0, 0)))
    FOE_NAMES = ("GRUNT", "RAIDER", "TITAN", "HORNET", "BRUISER")
    SIZES = {"mech": 1.4, "robot": 1.2}
    BAR = ((90, 220, 255), (30, 40, 60))
    LIVES = " x{}"

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P- and the score, the name of the machine and xlives, the gauge. / 1P-, le nom, xvies."""
        self.hud(screen, eng, vals, logo, now, name=self.name(vals, "1P-"))
        self.invite_right(screen, vals, now)


# ============================================================================ Battle Circuit
class BattleCircuitScene(CapcomBrawler):
    """Battle Circuit as in the game: an arena of the future at night, its neon beams and its stands of strange fans,
    the blue tiles; our masked hero of our own in yellow with his cape against the robots, the mutants and the punks.
    The name and xlives, the score, COIN and the money read in the game, the gauge. / Une arène du futur la nuit ; notre
    héros masqué à nous, en jaune et cape, contre les robots et les mutants. COIN et l'argent lu dans le jeu."""
    THEME = "bc_arena"
    HERO = ("jacket", (250, 210, 40), (40, 40, 50), (226, 176, 136), (40, 40, 50), None, (("visor", (60, 220, 255)), ("cape", (60, 60, 200))))
    FOES = (("robot", (180, 180, 200), (110, 110, 130), (0, 0, 0), (0, 0, 0)),
            ("mutant", (200, 80, 160), (90, 60, 120), (200, 160, 220), (120, 40, 140)),
            ("thug", (60, 200, 120), (40, 40, 60), (214, 160, 120), (240, 240, 240), "club"))
    FOE_NAMES = ("BOT", "PUNK", "MUTANT", "GOON", "DROID")
    BAR = ((255, 220, 40), (60, 30, 50))
    LIVES = " x{}"

    def status(self, screen, eng, vals, logo, now):
        """As in the game: the name and xlives, the score, COIN and the money, the gauge. / Le nom, le score, COIN."""
        S = self.S
        self.hud(screen, eng, vals, logo, now)
        m = _n(vals.get("money"))
        if m is not None:                                                 # COIN and the money, right of the logo
            self.label(screen, f"COIN {int(m)}", self.W / 2 + S(220), S(40), 30, (255, 220, 120))
        self.invite_right(screen, vals, now)


SCENES = {"ffight": FinalFightScene, "captcomm": CaptainCommandoScene, "dino": CadillacsScene, "punisher": PunisherScene,
          "kod": KingOfDragonsScene, "knights": KnightsScene, "wof": WarriorsOfFateScene, "ddsom": MystaraScene, "ddtod": TowerOfDoomScene,
          "avsp": AlienVsPredatorScene, "armwar": ArmoredWarriorsScene, "batcir": BattleCircuitScene}
__all__ = ["SCENES", "THEMES"]
