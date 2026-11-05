"""Metal Slug HD scene: two soldier panels, an animated backdrop and an effect for every game event.

Ammo going down fires shots in the style of the weapon, bombs are thrown and explode in the backdrop, a weapon
pickup drops a crate, a lost life drops the helmet, rescued prisoners, coins, score, timer, next mission (new
backdrop), player joining, CONTINUE and GAME OVER. In a vehicle (the tank of the first Metal Slug), the tank
takes the place of the weapon, with its energy in hits and its cannon shells. Missing values are simply hidden. All
drawings are made by the program, no image comes from the games.

Scène HD des Metal Slug : deux panneaux de soldat, décor animé, et un effet pour chaque événement du jeu.

Ce que fait chaque valeur lue dans la mémoire du jeu
- munitions qui baissent : tirs (flamme à la bouche du canon, traçantes vers le décor, douilles éjectées) ;
  le style suit l'arme (mitraillette, fusil à pompe, lance-roquettes, lance-flammes, laser) ;
- bombes qui baissent : la grenade quitte sa rangée, part en cloche, rebondit une fois et explose au second
  rebond, comme dans le jeu ; quand le jeu dit ses grenades à l'écran (grenades_out, Metal Slug), elle explose au
  moment même où celle du jeu explose, sur un ennemi touché comme au sol ;
- arme qui change : la carte de l'arme s'illumine, la jauge se remplit ;
- vie perdue : le casque tombe, le panneau rougit et tremble ; vie gagnée : « 1UP » ;
- prisonniers libérés, crédits, score qui défile, chrono qui passe au rouge, mission suivante (changement de décor),
  arrivée d'un joueur, CONTINUE et GAME OVER ;
- dans un véhicule (le char du premier Metal Slug) : le char prend la place de l'arme, avec son énergie en coups
  et ses obus ; un coup reçu secoue la carte, un obus part vers le décor, le char détruit explose.
Les valeurs absentes (pas encore trouvées pour un jeu) sont simplement cachées.

Dessins (casques, grenades, armes, décors) faits par le programme, aucune image tirée des jeux.
"""

import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

from . import hd_stages
from .hd_bg import Backdrop
from .hd_fx import FIRE, FIRE_HOT, FX, SPARK
from .i18n import tr

ACCENT = {"p1": (255, 138, 44), "p2": (64, 200, 255)}
GOLD = (255, 214, 120)
CREAM = (238, 228, 208)
WHITE = (255, 255, 255)
RED = (255, 64, 44)
GREEN = (130, 255, 150)
GREY = (150, 156, 170)

# codes d'arme de chaque jeu -> (nom, dessin)
NAMES = {"pistol": ("PISTOLET", "HANDGUN"), "shotgun": ("FUSIL À POMPE", "SHOTGUN"), "flame": ("LANCE-FLAMMES", "FLAMETHROWER"),
         "rocket": ("LANCE-ROQUETTES", "ROCKET LAUNCHER"), "mg": ("MITRAILLETTE", "MACHINE GUN"), "laser": ("LASER", "LASER"),
         "gun": ("ARME SPÉCIALE", "SPECIAL WEAPON"), "chaser": ("ENEMY CHASER", "ENEMY CHASER"), "lizard": ("IRON LIZARD", "IRON LIZARD"),
         "drop": ("DROP SHOT", "DROP SHOT"), "sgrenade": ("SUPER GRENADE", "SUPER GRENADE"), "cannon": ("CANON", "CANNON"),
         "mg2": ("DOUBLE MITRAILLETTE", "TWO MACHINE GUNS")}
MS1 = {0: "pistol", 1: "shotgun", 2: "flame", 3: "rocket", 4: "mg"}
MS2 = {255: "pistol", 0: "shotgun", 1: "rocket", 2: "flame", 3: "mg", 4: "laser"}
# Metal Slug X, 3, 4 and 5 share their codes (cheat database, RetroAchievements code notes): 7 to 11 are the SUPER weapons
# / Metal Slug X, 3, 4 et 5 ont les mêmes codes : de 7 à 11 les armes SUPER
MS3 = {0: "pistol", 1: "cannon", 2: "shotgun", 3: "rocket", 4: "flame", 5: "mg", 6: "laser", 7: "shotgun", 8: "rocket", 9: "flame",
       10: "mg", 11: "laser", 12: "chaser", 13: "lizard", 14: "drop", 15: "sgrenade", 0x12: "mg2", 0x15: "chaser", 0x1D: "shotgun"}
WEAPON_MAPS = {"mslug": MS1, "mslug2": MS2, "mslugx": MS3, "mslug3": MS3, "mslug4": MS3, "mslug5": MS3}
SUPER_CODES = range(7, 12)
LOOK = {"chaser": "rocket", "lizard": "rocket", "drop": "rocket", "sgrenade": "rocket", "cannon": "gun"}   # drawn and fired like

# the vehicles of each game, by the code the game keeps (vehicle_kind), and their names; the owner's own pictures go in
# sprites/<game>/<name>.png (sprites/mslug2/camel.png), or sprites/mslug/<name>.png for all the Metal Slug games
# / les véhicules de chaque jeu, par le code que garde le jeu, et leurs noms ; ses propres images dans sprites/<jeu>/<nom>.png
VEHICLES = {"mslug": {1: "tank"},
            "mslug2": {1: "tank", 2: "camel", 3: "slugnoid", 4: "flyer"},
            "mslugx": {4: "tank", 6: "flyer", 2: "camel"},
            "mslug3": {4: "tank", 6: "flyer", 7: "copter", 8: "mariner", 9: "drill", 10: "slugnoid", 11: "astro"},
            "mslug4": {},
            "mslug5": {4: "tank", 6: "flyer", 14: "slugnoid"}}
VEHICLE_NAMES = {"tank": ("CHAR", "TANK"), "camel": ("CAMEL SLUG", "CAMEL SLUG"), "slugnoid": ("SLUGNOID", "SLUGNOID"),
                 "flyer": ("SLUG FLYER", "SLUG FLYER"), "copter": ("SLUG COPTER", "SLUG COPTER"), "mariner": ("SLUG MARINER", "SLUG MARINER"),
                 "drill": ("DRILL SLUG", "DRILL SLUG"), "astro": ("ASTRO SLUG", "ASTRO SLUG"), "vehicle": ("VÉHICULE", "VEHICLE")}
RIDE_IN = {"tank": ("EN CHAR !", "TANK!"), "camel": ("EN SELLE !", "SADDLE UP!")}
RIDE_IN_ANY = ("À BORD !", "ABOARD!")
RIDE_LOST = {"tank": ("CHAR DÉTRUIT", "TANK DESTROYED")}
RIDE_LOST_ANY = ("VÉHICULE DÉTRUIT", "VEHICLE DESTROYED")
SOLDIERS = {"mslug": ("MARCO", "TARMA")}          # the first game: no choice, Marco then Tarma / pas de choix
BOSS_MIN = 200                                   # a boss's life is at least that much (else another enemy) / au moins
BOSS_MAX = 9999                                  # and no more (else not a life) / et pas plus (sinon pas une vie)
MINOR_IDLE = 8.0                                 # a big enemy's quiet bar fades after this long without a hit / s'efface
SYNC_MIN, SYNC_MAX = 0.8, 10.0                   # quiet after a start: at least this long, until the mission timer runs, at most

# cadence (secondes entre deux tirs) et allure de chaque arme
STYLE = {
    "pistol": {"gap": 0.12, "muzzle": 0.6, "tracer": (SPARK, 3, 80), "casing": "case"},
    "mg": {"gap": 0.065, "muzzle": 1.0, "tracer": ((255, 220, 120), 4, 150), "casing": "case"},
    "shotgun": {"gap": 0.24, "muzzle": 1.8, "tracer": ((255, 206, 120), 4, 110), "casing": "shell", "pellets": 6},
    "rocket": {"gap": 0.3, "muzzle": 1.1, "rocket": True},
    "flame": {"gap": 0.06, "flame": True},
    "laser": {"gap": 0.08, "muzzle": 0.9, "tracer": ((120, 230, 255), 6, 260), "laser": True},
    "gun": {"gap": 0.08, "muzzle": 1.0, "tracer": ((255, 220, 120), 4, 140), "casing": "case"},
}
STYLE["mg2"] = dict(STYLE["mg"], gap=0.045)           # the two machine guns of Metal Slug 4 and 5: faster / plus rapide
TIP = {"pistol": (0.89, 0.385), "shotgun": (0.985, 0.395), "flame": (0.975, 0.45), "rocket": (0.99, 0.41),
       "mg": (0.975, 0.41), "mg2": (0.975, 0.36), "laser": (0.97, 0.44), "gun": (0.975, 0.41), "tank": (0.99, 0.36)}
TANK_HITS = 3               # coups qu'encaisse le char du premier Metal Slug (jauge pleine à 48, 16 par coup)
FRAME_DX, FRAME_DY = 2, 14  # middle of the card's frame from the middle of the picture slot (the frame is drawn in the
                            # panel, at PW-226..PW-24 x 192..306, and the panel 14 lower) / milieu du cadre de la carte
OWN_BOX = (184, 100)        # the owner's picture fits in it, in the middle of the frame / sa propre image y tient
PORT = {"pistol": (0.45, 0.30), "shotgun": (0.32, 0.36), "mg": (0.30, 0.33), "mg2": (0.30, 0.33), "gun": (0.30, 0.33)}

PW, PH = 640, 418           # taille d'un panneau, écran de référence 1920 x 460
BTN_RIGHT, BTN_LEFT, BTN_A = 0x08, 0x04, 0x10      # octet des commandes du BIOS Neo Geo (P1CURRENT)


FLAG_VEHICLE = {"mslug", "mslug2", "mslug4"}      # "vehicle" is a flag (bit 0), elsewhere a kind / un drapeau, sinon un genre


def family(key):
    k = (key or "").lower()
    for name in ("mslugx", "mslug2", "mslug3", "mslug4", "mslug5", "mslug"):
        if k.startswith(name):
            return name
    return "mslug" if k[:2] == "ms" and k[2:3].isdigit() else ""        # ms4plus, ms5plus... but not msword or msh (Capcom)


def _n(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


# ---------------------------------------------------------------------------- dessins (Pillow)
def _draw(w, h, fn, ss=4, outline=True):
    big = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    fn(ImageDraw.Draw(big), w * ss, h * ss)
    if outline:                                               # contour sombre : lisible sur le verre du panneau
        a = big.getchannel("A").filter(ImageFilter.MaxFilter(ss * 2 + 1))
        back = Image.new("RGBA", big.size, (6, 8, 14, 0))
        back.putalpha(a.point(lambda v: v * 200 // 255))
        back.alpha_composite(big)
        big = back
    return big.resize((w, h), Image.LANCZOS)


def helmet_img(size):
    def fn(d, W, H):
        d.chord([W * 0.08, H * 0.10, W * 0.92, H * 1.06], 180, 360, fill=(84, 98, 58))
        d.chord([W * 0.18, H * 0.18, W * 0.60, H * 0.74], 200, 290, fill=(128, 144, 88))
        d.rounded_rectangle([W * 0.0, H * 0.54, W * 1.0, H * 0.68], radius=H * 0.06, fill=(62, 72, 42))
        d.arc([W * 0.26, H * 0.50, W * 0.74, H * 0.98], 25, 155, fill=(44, 50, 30), width=max(2, int(W * 0.05)))
        for i in range(5):
            x = W * (0.25 + i * 0.12)
            d.ellipse([x - W * 0.018, H * 0.40, x + W * 0.018, H * 0.44], fill=(60, 70, 40))
    return _draw(size, size, fn)


def grenade_img(w, h):
    def fn(d, W, H):
        d.ellipse([W * 0.10, H * 0.28, W * 0.90, H * 0.99], fill=(64, 90, 50))
        for k in (0.45, 0.62, 0.79):
            d.line([W * 0.14, H * k, W * 0.86, H * k], fill=(38, 56, 30), width=max(2, int(W * 0.05)))
        d.line([W * 0.5, H * 0.30, W * 0.5, H * 0.97], fill=(38, 56, 30), width=max(2, int(W * 0.05)))
        d.ellipse([W * 0.22, H * 0.36, W * 0.44, H * 0.56], fill=(118, 150, 92))
        d.rectangle([W * 0.36, H * 0.14, W * 0.64, H * 0.32], fill=(140, 140, 128))
        d.polygon([(W * 0.60, H * 0.14), (W * 0.82, H * 0.16), (W * 0.90, H * 0.56), (W * 0.80, H * 0.56), (W * 0.74, H * 0.24)],
                  fill=(112, 112, 100))
        d.ellipse([W * 0.06, H * 0.0, W * 0.40, H * 0.26], outline=(196, 196, 186), width=max(2, int(W * 0.06)))
    return _draw(w, h, fn)


def prisoner_img(w, h):
    def fn(d, W, H):
        c = (236, 222, 194)
        lw = max(3, int(W * 0.12))
        d.line([W * 0.37, H * 0.36, W * 0.12, H * 0.04], fill=c, width=lw)
        d.line([W * 0.63, H * 0.36, W * 0.88, H * 0.04], fill=c, width=lw)
        d.ellipse([W * 0.35, H * 0.02, W * 0.65, H * 0.29], fill=c)
        hair = (252, 204, 48)                                         # yellow hair, easier to read / plus parlant
        d.chord([W * 0.31, H * -0.01, W * 0.69, H * 0.25], 180, 360, fill=hair)
        d.ellipse([W * 0.31, H * 0.08, W * 0.40, H * 0.20], fill=hair)
        d.ellipse([W * 0.60, H * 0.08, W * 0.69, H * 0.20], fill=hair)
        d.rounded_rectangle([W * 0.31, H * 0.28, W * 0.69, H * 0.66], radius=W * 0.08, fill=c)
        d.line([W * 0.42, H * 0.62, W * 0.33, H * 0.99], fill=c, width=lw)
        d.line([W * 0.58, H * 0.62, W * 0.67, H * 0.99], fill=c, width=lw)
        d.rectangle([W * 0.31, H * 0.44, W * 0.69, H * 0.50], fill=(150, 120, 80))
    return _draw(w, h, fn)


def coin_img(size, symbol="", font=None):
    """Gold coin with the currency symbol (€, $, £) struck in relief, as on the coin doors; a plain coin without one.
    font(key, size) gives the font (hd.font). / Pièce d'or frappée du symbole de la monnaie, en relief ; unie sans symbole."""
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=(176, 116, 20))
        d.ellipse([W * 0.07, H * 0.07, W * 0.93, H * 0.93], fill=(250, 198, 66))
        d.arc([W * 0.12, H * 0.12, W * 0.88, H * 0.88], 200, 290, fill=(255, 242, 178), width=max(2, int(W * 0.06)))
        if symbol and font is not None:
            fe = font("black", max(8, int(W * 0.64 / max(1.0, 0.75 * len(symbol)))))
            l, t, r, b = fe.getbbox(symbol)
            x, y = W / 2 - (l + r) / 2, H / 2 - (t + b) / 2
            o = max(1, W // 36)
            d.text((x - o, y - o), symbol, font=fe, fill=(255, 248, 200))     # light edge, top left / arête claire
            d.text((x + o, y + o), symbol, font=fe, fill=(150, 90, 6))        # shadow, bottom right / ombre
            d.text((x, y), symbol, font=fe, fill=(206, 136, 20))
        else:
            d.ellipse([W * 0.2, H * 0.2, W * 0.8, H * 0.8], outline=(206, 146, 34), width=max(2, int(W * 0.05)))
    return _draw(size, size, fn, outline=False)


GUN, GUN_D, GUN_L = (78, 86, 100), (36, 40, 50), (160, 170, 186)
WOOD, OLIVE, RUST = (128, 78, 42), (84, 100, 62), (156, 46, 32)


def weapon_img(kind, w, h):
    def fn(d, W, H):
        def R(x0, y0, x1, y1, fill, r=0):
            if r:
                d.rounded_rectangle([x0 * W, y0 * H, x1 * W, y1 * H], radius=r * H, fill=fill)
            else:
                d.rectangle([x0 * W, y0 * H, x1 * W, y1 * H], fill=fill)

        def P(pts, fill):
            d.polygon([(x * W, y * H) for x, y in pts], fill=fill)

        def L(x0, y0, x1, y1, fill, wd):
            d.line([x0 * W, y0 * H, x1 * W, y1 * H], fill=fill, width=max(2, int(wd * H)))

        if kind == "pistol":
            R(0.20, 0.28, 0.24, 0.36, GUN_D)
            R(0.22, 0.30, 0.84, 0.47, GUN, 0.03)
            R(0.22, 0.30, 0.84, 0.33, GUN_L)
            for i in range(4):
                L(0.27 + i * 0.03, 0.34, 0.27 + i * 0.03, 0.45, GUN_D, 0.015)
            R(0.84, 0.34, 0.89, 0.43, GUN_D)
            R(0.79, 0.25, 0.82, 0.30, GUN_D)
            R(0.30, 0.47, 0.70, 0.55, GUN_D)
            P([(0.30, 0.53), (0.48, 0.53), (0.43, 0.93), (0.21, 0.93)], (54, 50, 52))
            for i in range(4):
                L(0.27 + i * 0.03, 0.62, 0.25 + i * 0.03, 0.88, (34, 32, 36), 0.012)
            d.arc([0.45 * W, 0.46 * H, 0.64 * W, 0.74 * H], 0, 180, fill=GUN_D, width=max(2, int(0.04 * H)))
            L(0.53, 0.54, 0.51, 0.64, GUN_D, 0.03)
        elif kind == "shotgun":
            P([(0.0, 0.40), (0.22, 0.36), (0.24, 0.53), (0.08, 0.67), (0.0, 0.65)], WOOD)
            L(0.02, 0.44, 0.20, 0.40, (160, 104, 60), 0.02)
            R(0.22, 0.33, 0.42, 0.54, GUN, 0.03)
            R(0.40, 0.36, 0.985, 0.43, GUN_D)
            R(0.40, 0.36, 0.985, 0.38, GUN_L)
            R(0.40, 0.45, 0.86, 0.50, GUN)
            R(0.56, 0.42, 0.76, 0.56, WOOD, 0.04)
            for i in range(5):
                L(0.58 + i * 0.035, 0.44, 0.58 + i * 0.035, 0.54, (90, 52, 26), 0.015)
            P([(0.24, 0.52), (0.34, 0.52), (0.30, 0.68), (0.21, 0.68)], (60, 44, 34))
            d.arc([0.33 * W, 0.48 * H, 0.45 * W, 0.68 * H], 0, 180, fill=GUN_D, width=max(2, int(0.035 * H)))
            R(0.95, 0.31, 0.97, 0.36, GUN_L)
        elif kind == "flame":
            R(0.02, 0.14, 0.18, 0.88, RUST, 0.06)
            R(0.04, 0.18, 0.07, 0.84, (200, 90, 70), 0.02)
            d.ellipse([0.08 * W, 0.20 * H, 0.15 * W, 0.32 * H], fill=(220, 220, 200))
            d.line([0.12 * W, 0.86 * H, 0.22 * W, 0.98 * H, 0.32 * W, 0.80 * H, 0.38 * W, 0.56 * H], fill=(40, 40, 44),
                   width=max(3, int(0.06 * H)), joint="curve")
            R(0.30, 0.38, 0.84, 0.51, GUN, 0.03)
            R(0.30, 0.38, 0.84, 0.41, GUN_L)
            R(0.52, 0.51, 0.58, 0.70, GUN_D, 0.02)
            P([(0.34, 0.50), (0.42, 0.50), (0.38, 0.72), (0.30, 0.72)], GUN_D)
            P([(0.84, 0.37), (0.975, 0.35), (0.975, 0.55), (0.84, 0.53)], GUN_D)
            for i in range(3):
                L(0.87 + i * 0.03, 0.37, 0.87 + i * 0.03, 0.53, (70, 74, 84), 0.015)
            d.ellipse([0.95 * W, 0.40 * H, 1.0 * W - 1, 0.50 * H], fill=(255, 150, 60))
        elif kind == "rocket":
            P([(0.04, 0.31), (0.0, 0.26), (0.0, 0.57), (0.04, 0.52)], (60, 72, 46))
            R(0.04, 0.30, 0.90, 0.52, OLIVE, 0.04)
            R(0.04, 0.30, 0.90, 0.335, (130, 150, 100))
            for x in (0.20, 0.72):
                R(x, 0.29, x + 0.04, 0.53, (58, 70, 44))
            P([(0.88, 0.28), (0.95, 0.26), (0.95, 0.56), (0.88, 0.54)], (60, 72, 46))
            P([(0.93, 0.33), (1.0, 0.41), (0.93, 0.49)], (196, 54, 40))
            R(0.40, 0.52, 0.46, 0.76, GUN_D, 0.02)
            R(0.56, 0.52, 0.61, 0.69, GUN_D, 0.02)
            R(0.50, 0.19, 0.63, 0.30, GUN_D, 0.02)
            d.ellipse([0.60 * W, 0.20 * H, 0.64 * W, 0.28 * H], fill=(110, 200, 255))
        elif kind == "laser":
            R(0.08, 0.32, 0.80, 0.56, (120, 130, 150), 0.06)
            R(0.08, 0.32, 0.80, 0.36, (200, 210, 226))
            for i in range(5):
                R(0.18 + i * 0.11, 0.42, 0.24 + i * 0.11, 0.46, (90, 230, 255))
            R(0.80, 0.36, 0.86, 0.52, GUN_D)
            for i in range(3):
                R(0.86 + i * 0.035, 0.38 - i * 0.02, 0.88 + i * 0.035, 0.50 + i * 0.02, (90, 100, 118))
            d.ellipse([0.92 * W, 0.40 * H, 0.99 * W, 0.48 * H], fill=(160, 240, 255))
            P([(0.26, 0.55), (0.36, 0.55), (0.32, 0.78), (0.24, 0.78)], GUN_D)
        else:                                                     # mitraillette, et toute arme inconnue
            if kind == "mg2":                                     # the second gun, strapped on top / la seconde, dessus
                R(0.18, 0.14, 0.44, 0.30, GUN, 0.03)
                R(0.18, 0.14, 0.44, 0.17, GUN_L)
                R(0.44, 0.17, 0.88, 0.29, GUN)
                R(0.44, 0.17, 0.88, 0.19, GUN_L)
                for i in range(7):
                    x = 0.48 + i * 0.055
                    d.ellipse([x * W, 0.21 * H, (x + 0.03) * W, 0.26 * H], fill=GUN_D)
                R(0.88, 0.15, 0.975, 0.31, GUN_D)
                R(0.30, 0.28, 0.36, 0.36, (40, 42, 50))             # the strap between the two / la sangle
                R(0.70, 0.28, 0.76, 0.36, (40, 42, 50))
            P([(0.0, 0.36), (0.16, 0.36), (0.16, 0.53), (0.04, 0.57), (0.0, 0.55)], GUN_D)
            R(0.03, 0.41, 0.12, 0.48, (20, 22, 28))
            R(0.16, 0.31, 0.44, 0.54, GUN, 0.03)
            R(0.16, 0.31, 0.44, 0.34, GUN_L)
            R(0.44, 0.35, 0.88, 0.47, GUN)
            R(0.44, 0.35, 0.88, 0.37, GUN_L)
            if kind in ("mg", "mg2"):
                for i in range(7):
                    x = 0.48 + i * 0.055
                    d.ellipse([x * W, 0.39 * H, (x + 0.03) * W, 0.44 * H], fill=GUN_D)
            R(0.88, 0.33, 0.975, 0.49, GUN_D)
            d.arc([0.24 * W, 0.14 * H, 0.40 * W, 0.40 * H], 180, 360, fill=GUN_D, width=max(2, int(0.05 * H)))
            R(0.26, 0.54, 0.38, 0.84, OLIVE, 0.02)
            R(0.26, 0.54, 0.38, 0.58, (120, 140, 92))
            P([(0.18, 0.52), (0.26, 0.52), (0.22, 0.75), (0.14, 0.75)], GUN_D)
            L(0.80, 0.47, 0.74, 0.82, GUN_D, 0.03)
            L(0.82, 0.47, 0.88, 0.82, GUN_D, 0.03)
    return _draw(w, h, fn)


def tank_img(w, h):
    """Un petit char vu de profil, canon vers la droite (dessin du programme, pas celui du jeu).
    / A small tank seen from the side, gun to the right (the program's own drawing, not the game's)."""
    def fn(d, W, H):
        def R(x0, y0, x1, y1, fill, r=0):
            if r:
                d.rounded_rectangle([x0 * W, y0 * H, x1 * W, y1 * H], radius=r * H, fill=fill)
            else:
                d.rectangle([x0 * W, y0 * H, x1 * W, y1 * H], fill=fill)

        def P(pts, fill):
            d.polygon([(x * W, y * H) for x, y in pts], fill=fill)

        dark, mid, light = (58, 70, 44), OLIVE, (132, 152, 98)
        R(0.08, 0.66, 0.80, 0.94, GUN_D, 0.14)                         # chenille
        for i in range(6):
            x = 0.15 + i * 0.115
            d.ellipse([(x - 0.045) * W, 0.70 * H, (x + 0.045) * W, 0.90 * H], fill=GUN)
            d.ellipse([(x - 0.018) * W, 0.76 * H, (x + 0.018) * W, 0.84 * H], fill=GUN_L)
        P([(0.04, 0.68), (0.12, 0.46), (0.76, 0.46), (0.86, 0.62), (0.84, 0.70), (0.06, 0.72)], mid)   # caisse
        R(0.12, 0.46, 0.76, 0.51, light)
        R(0.06, 0.64, 0.84, 0.70, dark)
        R(0.24, 0.26, 0.62, 0.48, mid, 0.08)                            # tourelle
        R(0.26, 0.26, 0.60, 0.31, light, 0.04)
        R(0.34, 0.18, 0.46, 0.27, dark, 0.03)                           # trappe
        R(0.60, 0.32, 0.99, 0.40, GUN, 0.02)                            # canon
        R(0.60, 0.32, 0.99, 0.34, GUN_L)
        R(0.93, 0.30, 0.99, 0.42, GUN_D, 0.02)
        pts = []
        for i in range(10):                                             # étoile au pochoir
            r = H * (0.075 if i % 2 == 0 else 0.03)
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((W * 0.43 + r * math.cos(a), H * 0.585 + r * math.sin(a)))
        d.polygon(pts, fill=(236, 226, 200))
    return _draw(w, h, fn)


def vehicle_img(kind, w, h):
    """The vehicles of the later games, seen from the side and facing right, the program's own drawings: the camel and its
    gun, the Slugnoid mech, the Slug Flyer, the Slug Copter, the Slug Mariner submarine, the Drill Slug, the Astro Slug.
    / Les véhicules des Metal Slug suivants, de profil, vers la droite, dessins du programme : chameau, mécha, avion,
    hélicoptère, sous-marin, foreuse, navette."""
    if kind in ("tank", "vehicle") or kind not in VEHICLE_NAMES:
        return tank_img(w, h)

    def fn(d, W, H):
        def R(x0, y0, x1, y1, fill, r=0):
            if r:
                d.rounded_rectangle([x0 * W, y0 * H, x1 * W, y1 * H], radius=r * H, fill=fill)
            else:
                d.rectangle([x0 * W, y0 * H, x1 * W, y1 * H], fill=fill)

        def P(pts, fill):
            d.polygon([(x * W, y * H) for x, y in pts], fill=fill)

        def E(x0, y0, x1, y1, fill):
            d.ellipse([x0 * W, y0 * H, x1 * W, y1 * H], fill=fill)

        def L(x0, y0, x1, y1, fill, wd):
            d.line([x0 * W, y0 * H, x1 * W, y1 * H], fill=fill, width=max(2, int(wd * H)))

        dark, mid, light = (58, 70, 44), OLIVE, (132, 152, 98)
        if kind == "camel":                                              # the camel, the gun on its hump / le chameau
            tan, tan_d = (206, 164, 96), (150, 112, 60)
            for x in (0.22, 0.32, 0.56, 0.66):                           # legs / pattes
                L(x, 0.62, x - 0.02, 0.96, tan_d, 0.06)
            E(0.14, 0.40, 0.74, 0.74, tan)                               # body / corps
            E(0.30, 0.26, 0.58, 0.50, tan)                               # hump / bosse
            P([(0.66, 0.46), (0.78, 0.22), (0.86, 0.24), (0.76, 0.50)], tan)      # neck / cou
            E(0.78, 0.14, 0.96, 0.30, tan)                               # head / tête
            E(0.92, 0.20, 0.98, 0.27, (40, 30, 20))
            L(0.12, 0.52, 0.04, 0.70, tan_d, 0.03)                       # tail / queue
            R(0.34, 0.20, 0.54, 0.30, GUN_D, 0.03)                       # the gun mount / l'affût
            R(0.44, 0.10, 0.90, 0.18, GUN, 0.02)                         # the machine gun / la mitrailleuse
            R(0.44, 0.10, 0.90, 0.12, GUN_L)
            R(0.86, 0.08, 0.92, 0.20, GUN_D, 0.02)
        elif kind == "slugnoid":                                         # the mech: body on two legs / le mécha
            for x0 in (0.26, 0.52):                                      # legs / jambes
                P([(x0, 0.60), (x0 + 0.12, 0.60), (x0 + 0.16, 0.80), (x0 + 0.06, 0.80)], dark)
                R(x0 + 0.02, 0.78, x0 + 0.22, 0.90, GUN_D, 0.04)
            R(0.18, 0.22, 0.74, 0.62, mid, 0.08)                         # body / corps
            R(0.20, 0.22, 0.72, 0.28, light, 0.04)
            R(0.40, 0.08, 0.62, 0.26, dark, 0.05)                        # cockpit
            E(0.46, 0.11, 0.60, 0.23, (110, 200, 255))
            for y0 in (0.30, 0.44):                                      # the two vulcans / les deux canons
                R(0.70, y0, 0.98, y0 + 0.08, GUN, 0.02)
                R(0.70, y0, 0.98, y0 + 0.02, GUN_L)
            R(0.08, 0.34, 0.20, 0.52, dark, 0.03)                        # the pack behind / le réservoir
        elif kind == "flyer":                                            # the jet, nose to the right / l'avion
            grey, grey_d, grey_l = (150, 160, 176), (90, 98, 112), (210, 216, 228)
            P([(0.02, 0.30), (0.22, 0.14), (0.30, 0.44), (0.12, 0.52)], grey_d)         # tail fin / dérive
            P([(0.04, 0.44), (0.98, 0.50), (0.90, 0.62), (0.10, 0.64)], grey)           # fuselage
            P([(0.06, 0.46), (0.92, 0.52), (0.90, 0.55), (0.08, 0.50)], grey_l)
            E(0.56, 0.36, 0.80, 0.52, (120, 210, 255))                   # canopy / verrière
            P([(0.26, 0.56), (0.70, 0.58), (0.60, 0.74), (0.34, 0.74)], grey_d)         # wing / aile
            R(0.38, 0.72, 0.62, 0.80, (196, 54, 40), 0.03)               # missile under the wing / missile
            P([(0.62, 0.72), (0.70, 0.76), (0.62, 0.80)], (240, 200, 60))
            E(0.00, 0.50, 0.10, 0.60, (255, 150, 60))                    # the jet flame / la flamme
        elif kind == "copter":                                           # the helicopter / l'hélicoptère
            grey, grey_d = (150, 160, 176), (90, 98, 112)
            L(0.10, 0.12, 0.90, 0.12, GUN_D, 0.03)                       # rotor
            R(0.48, 0.10, 0.54, 0.26, GUN_D)
            P([(0.06, 0.40), (0.40, 0.34), (0.42, 0.46), (0.10, 0.48)], grey_d)         # tail boom / poutre
            L(0.08, 0.26, 0.08, 0.54, GUN_D, 0.025)                      # tail rotor / rotor de queue
            E(0.36, 0.24, 0.92, 0.66, grey)                              # cabin / cabine
            E(0.60, 0.30, 0.90, 0.52, (120, 210, 255))                   # glass / vitre
            R(0.40, 0.56, 0.86, 0.62, GUN, 0.02)                         # the gun / le canon
            L(0.40, 0.76, 0.84, 0.76, GUN_D, 0.03)                       # skids / patins
            L(0.50, 0.64, 0.50, 0.76, GUN_D, 0.02)
            L(0.76, 0.64, 0.76, 0.76, GUN_D, 0.02)
        elif kind == "mariner":                                          # the submarine / le sous-marin
            blue, blue_d, blue_l = (96, 128, 170), (54, 76, 110), (160, 190, 226)
            E(0.04, 0.38, 0.96, 0.78, blue)                              # hull / coque
            E(0.08, 0.42, 0.90, 0.56, blue_l)
            R(0.38, 0.20, 0.60, 0.42, blue_d, 0.05)                      # tower / kiosque
            R(0.46, 0.08, 0.50, 0.22, GUN_D)                             # periscope / périscope
            R(0.46, 0.08, 0.56, 0.11, GUN_D)
            for x in (0.22, 0.34, 0.66, 0.78):                           # portholes / hublots
                E(x, 0.52, x + 0.08, 0.66, (140, 230, 255))
            P([(0.00, 0.44), (0.06, 0.52), (0.06, 0.66), (0.00, 0.74)], blue_d)          # rudder / gouvernail
            L(0.02, 0.58, 0.06, 0.58, GUN_D, 0.03)
            R(0.90, 0.54, 1.00, 0.62, GUN_D, 0.02)                       # torpedo tube / tube lance-torpilles
        elif kind == "drill":                                            # the drill on treads / la foreuse
            R(0.06, 0.66, 0.66, 0.94, GUN_D, 0.14)                       # treads / chenilles
            for i in range(5):
                x = 0.12 + i * 0.11
                E(x - 0.04, 0.70, x + 0.04, 0.90, GUN)
            P([(0.04, 0.68), (0.10, 0.40), (0.62, 0.40), (0.70, 0.56), (0.68, 0.70), (0.06, 0.72)], mid)   # body / caisse
            R(0.10, 0.40, 0.62, 0.45, light)
            R(0.20, 0.22, 0.46, 0.42, dark, 0.06)                        # cab / cabine
            E(0.28, 0.26, 0.42, 0.38, (110, 200, 255))
            P([(0.64, 0.36), (0.99, 0.56), (0.64, 0.76)], (176, 180, 192))     # the drill cone / le cône
            for i in range(3):                                           # its spiral / sa spirale
                x0 = 0.68 + i * 0.09
                L(x0, 0.40 + i * 0.04, x0 + 0.06, 0.70 - i * 0.04, (110, 114, 126), 0.025)
        elif kind == "astro":                                            # the shuttle, nose to the right / la navette
            white, grey_d = (226, 228, 236), (120, 126, 140)
            P([(0.00, 0.38), (0.16, 0.20), (0.26, 0.42), (0.10, 0.50)], grey_d)         # fin / dérive
            P([(0.08, 0.44), (0.80, 0.42), (0.98, 0.56), (0.80, 0.70), (0.08, 0.68)], white)   # fuselage
            P([(0.10, 0.46), (0.80, 0.44), (0.94, 0.56), (0.10, 0.52)], (246, 248, 252))
            P([(0.20, 0.60), (0.70, 0.60), (0.60, 0.82), (0.26, 0.82)], grey_d)          # wing / aile
            E(0.60, 0.44, 0.78, 0.56, (120, 210, 255))                   # window / hublot
            R(0.02, 0.48, 0.10, 0.66, (196, 54, 40), 0.03)               # engine / moteur
            E(-0.06, 0.50, 0.06, 0.64, (255, 150, 60))                   # its flame / sa flamme
    return _draw(w, h, fn)


def clear_background(img, tol=48):
    """An opaque picture's plain background made transparent. The four corners give its colour (when they differ it is
    not a plain background, a photo say, and the picture stays as it is); it goes from the corners inwards, as far as it
    stays close to that colour (each channel within tol), so a light colour inside the drawing's outline stays.
    / Le fond uni d'une image opaque rendu transparent : la couleur de ses quatre coins, depuis les coins et tant qu'on
    reste proche d'elle. Le clair à l'intérieur du contour du dessin reste, une photo aussi."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    r, g, b = ImageChops.difference(rgb, Image.new("RGB", rgb.size, rgb.getpixel((0, 0)))).split()
    dist = ImageChops.lighter(ImageChops.lighter(r, g), b).point(lambda v: min(v, 254))     # 255 = background found
    corners = ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))
    if any(dist.getpixel(xy) > tol for xy in corners):
        return img
    for xy in corners:
        if dist.getpixel(xy) != 255:
            ImageDraw.floodfill(dist, xy, 255, thresh=tol)
    out = img.copy()
    out.putalpha(ImageChops.multiply(img.getchannel("A"), dist.point(lambda v: 0 if v == 255 else 255)))
    return out


def small_imgs(s):
    """Objets qui volent : douille, cartouche, éclats, roquette (Pillow RGBA)."""
    out = {}

    def case(d, W, H):
        d.rounded_rectangle([0, H * 0.15, W * 0.78, H * 0.85], radius=H * 0.2, fill=(214, 168, 70))
        d.rectangle([W * 0.70, H * 0.05, W * 0.84, H * 0.95], fill=(170, 128, 50))
        d.line([W * 0.05, H * 0.3, W * 0.7, H * 0.3], fill=(255, 226, 150), width=max(1, int(H * 0.15)))
    out["case"] = _draw(max(6, int(14 * s)), max(3, int(6 * s)), case, outline=False)

    def shell(d, W, H):
        d.rounded_rectangle([0, H * 0.1, W * 0.74, H * 0.9], radius=H * 0.2, fill=(190, 40, 36))
        d.rectangle([W * 0.70, H * 0.0, W * 1.0, H * 1.0], fill=(214, 168, 70))
        d.line([W * 0.05, H * 0.3, W * 0.66, H * 0.3], fill=(240, 110, 100), width=max(1, int(H * 0.15)))
    out["shell"] = _draw(max(8, int(18 * s)), max(4, int(8 * s)), shell, outline=False)
    rng = random.Random(4)
    for i in range(3):
        def chunk(d, W, H, i=i):
            pts = [(W / 2 + math.cos(a) * W * rng.uniform(0.25, 0.5), H / 2 + math.sin(a) * H * rng.uniform(0.25, 0.5))
                   for a in [k * math.tau / 7 for k in range(7)]]
            d.polygon(pts, fill=((70, 58, 52), (52, 46, 44), (96, 70, 50))[i])
        out["chunk%d" % i] = _draw(max(6, int((12 + i * 4) * s)), max(6, int((10 + i * 3) * s)), chunk, outline=False)

    def rocket(d, W, H):
        d.polygon([(0, H * 0.1), (W * 0.18, H * 0.3), (W * 0.18, H * 0.7), (0, H * 0.9)], fill=(70, 80, 60))
        d.rounded_rectangle([W * 0.12, H * 0.28, W * 0.82, H * 0.72], radius=H * 0.2, fill=(150, 156, 140))
        d.polygon([(W * 0.8, H * 0.28), (W, H * 0.5), (W * 0.8, H * 0.72)], fill=(200, 56, 40))
        d.line([W * 0.14, H * 0.36, W * 0.78, H * 0.36], fill=(210, 214, 200), width=max(1, int(H * 0.1)))
    out["rocket"] = _draw(max(16, int(48 * s)), max(6, int(14 * s)), rocket)

    def crate(d, W, H):
        d.rectangle([0, 0, W - 1, H - 1], fill=(150, 98, 52))
        for k in (0.33, 0.66):
            d.line([0, H * k, W, H * k], fill=(104, 64, 30), width=max(2, int(H * 0.04)))
        d.line([0, 0, W, H], fill=(120, 76, 38), width=max(3, int(W * 0.06)))
        for (x0, y0) in ((0, 0), (W * 0.82, 0), (0, H * 0.8), (W * 0.82, H * 0.8)):
            d.rectangle([x0, y0, x0 + W * 0.18, y0 + H * 0.2], fill=(90, 96, 104))
        pts = []
        for i in range(10):                                             # étoile au pochoir
            r = H * (0.26 if i % 2 == 0 else 0.11)
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((W / 2 + r * math.cos(a), H / 2 + r * math.sin(a)))
        d.polygon(pts, fill=(236, 226, 200))
        d.rectangle([0, 0, W - 1, H - 1], outline=(70, 42, 20), width=max(2, int(W * 0.03)))
    out["crate"] = _draw(max(20, int(64 * s)), max(16, int(52 * s)), crate)

    def plank(d, W, H):
        d.rectangle([0, 0, W - 1, H - 1], fill=(150, 98, 52))
        d.line([0, H * 0.5, W, H * 0.5], fill=(110, 70, 34), width=1)
    out["plank"] = _draw(max(10, int(30 * s)), max(4, int(9 * s)), plank, outline=False)
    return out


def panel_img(side, s, accent):
    """Fond d'un panneau (verre sombre, liserés, bandes de danger), dessiné pour J1 puis retourné pour J2."""
    ss = 2
    W, H = int(PW * s), int(PH * s)
    w, h = W * ss, H * ss
    k = s * ss
    cut = 28 * k
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shape = [(cut, 0), (w - 1, 0), (w - 1, h - 1 - cut), (w - 1 - cut, h - 1), (0, h - 1), (0, cut)]
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(shape, fill=255)
    grad = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(grad)
    for y in range(h):
        t = y / max(1, h - 1)
        gd.line([0, y, w, y], fill=(int(14 - 6 * t), int(18 - 8 * t), int(38 - 18 * t), int(222 + 18 * t)))
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)
    stripes = Image.new("L", (w, h), 0)                              # bandes de danger dans l'en-tête
    sd = ImageDraw.Draw(stripes)
    for x in range(int(110 * k), int(330 * k), int(28 * k)):
        sd.polygon([(x, 6 * k), (x + 12 * k, 6 * k), (x - 34 * k, 66 * k), (x - 46 * k, 66 * k)], fill=34)
    img.paste(accent + (255,), (0, 0), ImageChops.multiply(stripes, mask))
    d.line([(16 * k, 72 * k), (w - 16 * k, 72 * k)], fill=accent + (110,), width=max(1, int(2 * k)))
    d.rounded_rectangle([16 * k, 184 * k, (PW - 16) * k, 314 * k], radius=12 * k, fill=(0, 0, 0, 96), outline=accent + (80,),
                        width=max(1, int(2 * k)))
    d.rounded_rectangle([(PW - 226) * k, 192 * k, (PW - 24) * k, 306 * k], radius=10 * k, fill=(255, 255, 255, 12))
    d.line([(16 * k, 324 * k), (w - 16 * k, 324 * k)], fill=(255, 255, 255, 34), width=max(1, int(k)))
    d.line(shape + [shape[0]], fill=accent + (170,), width=max(2, int(3 * k)))
    inner = [(cut + 8 * k, 7 * k), (w - 8 * k, 7 * k), (w - 8 * k, h - 9 * k - cut), (w - 9 * k - cut, h - 8 * k),
             (8 * k, h - 8 * k), (8 * k, cut + 8 * k)]
    d.line(inner + [inner[0]], fill=(255, 255, 255, 22), width=max(1, int(k)))
    for (x, y) in ((22 * k, h - 22 * k), (w - 22 * k, 22 * k), (w - 60 * k, h - 22 * k)):
        r = 4 * k
        d.ellipse([x - r, y - r, x + r, y + r], fill=(180, 186, 200, 90))
    img = img.resize((W, H), Image.LANCZOS)
    return img if side == "p1" else ImageOps.mirror(img)


# ---------------------------------------------------------------------------- un joueur
class Player:
    def __init__(self, side):
        self.side = side
        self.mode = None
        self.shown = 0.0
        self.join_t = -99.0
        self.sync_until = -99.0
        self.seen = {}
        self.score_disp = None
        self.score_t = -99.0
        self.float_acc, self.float_t = 0, -99.0
        self.ammo_max = 0
        self.gauge = 0.0
        self.weapon_t = -99.0
        self.weapon_kind = "pistol"
        self.empty_t = -99.0
        self.hit_t = -99.0
        self.up_t = -99.0
        self.prison_t = -99.0
        self.bomb_t = -99.0
        self.bomb_add = (-99.0, 0)
        self.shots = []
        self.flame_until = -99.0
        self.recoil_t = -99.0
        self.over_t = None
        self.move = 0.0
        self.flying = 0                 # grenades en vol (icônes déjà parties)
        self.live = []                  # grenades of the HD screen waiting for the game's own to blow up / en attente
        self.out_ok = False             # the game's grenades on screen are read and follow the throws / suivies
        self.early = 0                  # the game's grenade blew up before ours left the hand / partie trop tôt
        self.tank = False               # dans un véhicule / in a vehicle
        self.ride = None                # which one: tank, camel, flyer... (VEHICLES) / lequel
        self.tank_t = -99.0             # monté dans le char / got in
        self.tank_hit_t = -99.0         # coup reçu par le char / hit taken by the tank


# ---------------------------------------------------------------------------- la scène
class MetalSlugScene:
    FPS = 50
    SLIDE_EVERY = 9.0                   # écran d'attente : un décor toutes les 9 secondes
    GRENADE_FLIGHT = 0.62               # seconds of the grenade's arc before it touches the ground / avant le sol
    GRENADE_BOUNCE = 0.55               # its bounce: it lands again about a second after the throw / second rebond vers 1 s
    GRENADE_WAIT = 2.0                  # waiting for the game's own explosion, at most / attente de l'explosion du jeu

    def __init__(self, hd, rng=None, threaded=True):
        self.hd, self.pg, self.s = hd, hd.pg, hd.s
        self.W, self.H = hd.W, hd.H
        self.rng = rng or random.Random()
        self.fx = FX(hd, random.Random(self.rng.random()))
        self.bd = Backdrop(hd, hd_stages.MISSION_STAGES[0], random.Random(self.rng.random()), threaded=False)
        self.players = {"p1": Player("p1"), "p2": Player("p2")}
        self.last = None
        self.key = None
        self.mission = None
        self.mission_shown = None
        self.mission_t = -99.0
        self.complete_t = -99.0
        self.slide_t = 0.0
        self.slide_i = 0
        self.was_attract = False
        self._stages_key = object()
        self._stages = list(hd_stages.MISSION_STAGES)
        self.credits = None
        self.coin_t = -99.0
        self.time_v = None
        self.buf = None
        self.fx_dt = 0.0
        s = self.s
        self.icons = {"helmet": hd._surf(helmet_img(int(46 * s))), "grenade": hd._surf(grenade_img(int(30 * s), int(38 * s))),
                      "prisoner": hd._surf(prisoner_img(int(34 * s), int(40 * s)))}
        self.coin_symbol = None                  # the coins' symbol, from coin_symbol in config.json / symbole des pièces
        self.coin_sprite = "coin"
        self.coin_xy = None                      # the credits' coin on screen, where inserted coins land / où tombent les pièces
        self.boom_t = -99.0                      # when the last grenade blew up / quand la dernière grenade a explosé
        self.booms = 0                           # (tests)
        self.coin_box = None
        self.in_attract = False
        self.pills = {}
        self.panels = {side: hd._surf(panel_img(side, s, ACCENT[side])) for side in ("p1", "p2")}
        self.weapons = {}
        self.rides = {}                          # the vehicles' pictures, (kind, side) / les dessins des véhicules
        self.ride_own = {}                       # kind -> the owner's own picture / sa propre image
        self.ride_tip = {}                       # kind -> its gun's end in the slot / le bout de son canon
        self.own = {}                            # the owner's pictures found or not, by name / ses images, par nom
        self.boss = None                         # the boss of the mission on the screen (a game that gives its life)
        self.boss_prev = {}                      # / le boss de la mission, pour un jeu qui donne sa vie
        self._slots_key = object()
        self._slots = []
        self._boss_flag = None                   # the value that says the boss is fought, when the game has one / le drapeau
        self._boss_big = None                    # or the life a boss has at least, when the game has no flag / ou sa vie
        self._boss_life = {}                     # or the life each mission's boss starts with / ou la vie de chaque boss
        self.meta_ref = None                     # the game session the players belong to / la partie des joueurs
        self.boss_hit = {}                       # when each big life was last hit / quand chaque grosse vie a été touchée
        self.boss_top = {}                       # the most each one had / le plus qu'elle a eu
        self.boss_rise = {}                      # entry -> when a boss's life last filled it / quand une vie l'a remplie
        self.boss_ref = None                     # the entry the boss of the mission was found in / la case du boss
        self.boss_parts = set()                  # entries filled with the boss's own life: its parts / ses morceaux
        self.boss_dead_prev = None               # the game's "boss dead" flag at the previous image / le drapeau d'avant
        self.done_prev = None                    # and its "mission done" flag / et son drapeau de fin de mission
        self.complete_m = None                   # the mission the game said was complete / la mission dite finie
        self.boss_alerts = 0                     # (tests)
        self.boss_downs = 0
        self.ride_surf("tank", "p1")             # ready before the first tank (the owner's picture takes a moment)
        sp = self.fx.sp
        for name, img in small_imgs(s).items():
            sp.register(name, img)
        sp.register("helmet", helmet_img(int(46 * s)))
        sp.register("grenade", grenade_img(int(24 * s), int(30 * s)))
        self.set_coin_symbol("€")
        self.warm = self._warm_list()

    def set_coin_symbol(self, symbol):
        """The coin beside the credits and the falling coins carry the symbol of config.json (€, $, £, "" plain).
        / La pièce des crédits et celles qui tombent portent le symbole de config.json."""
        symbol = str(symbol or "").strip()[:2]
        if symbol == self.coin_symbol:
            return
        self.coin_symbol = symbol
        self.icons["coin"] = self.hd._surf(coin_img(self.S(54), symbol, self.hd.font))
        self.coin_sprite = "coin" + symbol                    # one name per symbol: turned copies stay right / une par symbole
        self.fx.sp.register(self.coin_sprite, coin_img(self.S(54), symbol, self.hd.font))

    def _warm_list(self):
        """Images des grosses explosions, préparées petit à petit pendant les images calmes (pas d'à-coup)."""
        sp, s, out = self.fx.sp, self.s, []
        for color, rmax in (((255, 130, 50), 256), (FIRE, 128), (FIRE_HOT, 128), ((255, 110, 40), 128), ((255, 236, 190), 100)):
            for r in (40, 50, 64, 80, 100, 128, 160, 200, 256):
                if r > rmax:
                    break
                for lv in range(12, 0, -1):
                    out.append((sp.glow, (r * s, color, lv, 0.35)))
        for color in ((58, 52, 62), (120, 70, 40), (150, 140, 140)):
            for r in (13, 16, 20, 25, 32, 40, 50, 64, 80, 100):
                for v in range(3):
                    out.append((sp.puff, (r * s, color, v)))
        hd, S = self.hd, self.S                                        # textes des annonces, avec leur lueur
        texts = [("MISSION COMPLETE !", 88, GOLD, 0.8), (tr("J2 ARRIVE !", "P2 JOINS IN!"), 56, ACCENT["p2"], 0.6),
                 (tr("-1 VIE", "-1 LIFE"), 40, RED, 0.6), ("1UP !", 46, GREEN, 0.6), (tr("+1 CRÉDIT", "+1 CREDIT"), 34, GOLD, 0.6),
                 (tr("+1 PRISONNIER", "+1 PRISONER"), 34, CREAM, 0.6), (tr("PLUS DE MUNITIONS", "OUT OF AMMO"), 30, (255, 120, 90), 0.6),
                 (tr("DERNIÈRE VIE", "LAST LIFE"), 34, RED, 0.7), ("CONTINUE ?", 80, GOLD, 0.6), ("GAME OVER", 80, RED, 0.6),
                 (tr("EN CHAR !", "TANK!"), 40, GREEN, 0.6), (tr("CHAR DÉTRUIT", "TANK DESTROYED"), 40, RED, 0.6),
                 (tr(*RIDE_IN["camel"]), 40, GREEN, 0.6), (tr(*RIDE_IN_ANY), 40, GREEN, 0.6), (tr(*RIDE_LOST_ANY), 40, RED, 0.6),
                 (tr("ÉJECTE-TOI !", "BAIL OUT!"), 30, RED, 0.7), ("WARNING", 92, RED, 0.8), (tr("BOSS DÉTRUIT", "BOSS DESTROYED"), 60, GOLD, 0.7),
                 (tr("ENNEMI", "ENEMY"), 22, (200, 196, 180), 0.2), (tr("DÉTRUIT", "DESTROYED"), 30, (255, 200, 150), 0.5)]
        texts += [(f"MISSION {n}", 92, GOLD, 0.7) for n in range(1, 7)]
        for text, size, col, glow in texts:
            out.insert(0, (hd.text, (text, "stencil", S(size), col, glow)))
        return out

    def _warm_step(self, budget):
        import time as _t
        end = _t.perf_counter() + budget
        while self.warm and _t.perf_counter() < end:
            fn, args = self.warm.pop(0)
            try:
                fn(*args)
            except Exception:
                self.warm = []

    # ------------------------------------------------------------ outils
    def S(self, v):
        return int(round(v * self.s))

    def x0(self, side, P):
        """Bord gauche du panneau, en tenant compte de son arrivée en glissant."""
        k = P.shown
        e = 1 - (1 - k) ** 3 if k < 1 else 1.0
        hidden = -self.S(PW + 40) if side == "p1" else self.W + self.S(40)
        home = self.S(18) if side == "p1" else self.W - self.S(18 + PW)
        return int(hidden + (home - hidden) * e)

    def X(self, side, x0, lx, w=0):
        """Abscisse d'un élément placé à lx du bord extérieur (gauche pour J1, droit pour J2)."""
        return x0 + self.S(lx) if side == "p1" else x0 + self.S(PW) - self.S(lx) - self.S(w)

    def aboard(self, v):
        """Whether a "vehicle" value means the soldier is in a vehicle: a flag byte (bit 0) in the first Metal Slug, 2 and
        4, its other bits the soldier's state on foot (1.33 test 29, Seb's capture of 17:58: 2, 4, 6, 16, 22 while he moves
        and shoots, read as the tank since test 21); a kind in the others; 255 is his block wiped between two lives.
        / Un octet de bits dans le premier Metal Slug, le 2 et le 4, un genre dans les autres ; 255, son bloc effacé."""
        if v is None or v == 255:
            return False
        return bool(int(v) & 1) if family(self.key) in FLAG_VEHICLE else v > 0

    def weapon(self, side, code):
        """(name, kind) of a weapon code: the name shown, the kind it is drawn and fired as. / (nom, genre) d'un code."""
        m = WEAPON_MAPS.get(family(self.key), MS1)
        if code is None:
            return None, None
        kind = m.get(int(code))
        if kind is None:
            # 255: the soldier's block wiped (dead, between two lives), the handgun as in 1.31 (test 29, Seb's capture of
            # the first Metal Slug: ARME SPÉCIALE flashed at each death) / 255 : le bloc du soldat effacé, le pistolet
            kind = "pistol" if int(code) in (0, 255) else "gun"
        name = tr(*NAMES[kind])
        if m is MS3 and int(code) in SUPER_CODES:
            name = "SUPER " + name
        return name, LOOK.get(kind, kind)

    def soldier(self, side, vals):
        """The soldier's name beside J1 / J2: the one the game says (p1_name, from the soldier chosen), or the first
        game's, where player 1 is always Marco and player 2 Tarma. / Le nom du soldat : celui que dit le jeu, ou ceux du
        premier Metal Slug."""
        name = vals.get("p1_name" if side == "p1" else "p2_name")
        if isinstance(name, str) and name:
            return name
        fixed = SOLDIERS.get(family(self.key))
        return fixed[0 if side == "p1" else 1] if fixed else None

    def ride_kind(self, code):
        """Which vehicle a code of the game is (vehicle_kind), for this game. / Quel véhicule est ce code, pour ce jeu."""
        table = VEHICLES.get(family(self.key)) or VEHICLES["mslug"]
        if code is None:
            return "tank" if list(table.values()) == ["tank"] else "vehicle"
        return table.get(int(code), "vehicle")

    def weapon_surf(self, kind, side):
        key = (kind, side)
        s = self.weapons.get(key)
        if s is None:
            img = weapon_img(kind, self.S(190), self.S(108))
            if side == "p2":
                img = ImageOps.mirror(img)
            s = self.weapons[key] = self.hd._surf(img)
        return s

    def tank_surf(self, side):
        return self.ride_surf("tank", side)

    @property
    def tank_own(self):
        return bool(self.ride_own.get("tank"))

    @property
    def tank_tip(self):
        return self.ride_tip.get("tank")

    def ride_surf(self, kind, side):
        """A vehicle's picture, the program's drawing or the owner's own (sprites/<game>/<kind>.png, side view, gun to the
        right, fitted in the card). / Le dessin d'un véhicule, celui du programme ou le sien (sprites/<jeu>/<genre>.png)."""
        s = self.rides.get((kind, side))
        if s is None:
            img = self.rides.get(("img", kind))
            if img is None:
                own = self._own_picture(kind, self.S(190), self.S(108), OWN_BOX)
                self.ride_own[kind] = own is not None
                self.ride_tip[kind] = self._cannon_tip(own) if own is not None else None
                img = self.rides[("img", kind)] = own or vehicle_img(kind, self.S(190), self.S(108))
            if side == "p2":
                img = ImageOps.mirror(img)
            s = self.rides[(kind, side)] = self.hd._surf(img)
        return s

    def own_path(self, name):
        """The owner's own picture of a vehicle or a soldier: sprites/<romset>/<name>.png, then sprites/<family>/<name>.png
        (sprites/mslug2/camel.png), then sprites/mslug/<name>.png for all the Metal Slug games, and the tank's older
        sprites/mslug_tank_hd.png. None without one. / Sa propre image : sprites/<romset>/, sprites/<famille>/, sprites/mslug/."""
        root = getattr(self.hd, "root", "") or ""
        seen = []
        for d in ((self.key or "").lower(), family(self.key), "mslug"):
            if d and d not in seen:
                seen.append(d)
                p = os.path.join(root, "sprites", d, name + ".png")
                if os.path.isfile(p):
                    return p
        if name == "tank":
            p = os.path.join(root, "sprites", "mslug_tank_hd.png")
            if os.path.isfile(p):
                return p
        return None

    def _own_picture(self, name, w, h, box):
        """The owner's picture fitted in a card of w x h, in the middle of a box (drawn in the middle of the card's frame).
        A plain background (a picture without transparency) is made transparent, empty margins are cut. None without one.
        / Son image dans une carte, au milieu : un fond uni devient transparent, les marges vides partent."""
        key = (name, w, h)
        if key in self.own:
            return self.own[key]
        path = self.own_path(name)
        out = None
        if path is not None:
            try:
                img = Image.open(path).convert("RGBA")
                img.thumbnail((w * 3, h * 3), Image.LANCZOS)            # a big picture made small first / réduite d'abord
                if img.getchannel("A").getextrema()[0] == 255:
                    clear = clear_background(img)                     # no transparency: its plain background goes
                    img = clear if clear.getchannel("A").getbbox() else img    # (a picture of one colour stays whole)
                bb = img.getchannel("A").point(lambda v: 255 if v > 16 else 0).getbbox()
                if bb is not None:
                    img = img.crop(bb)                                # the drawing only / le dessin seul
                    k = min(self.S(box[0]) / img.width, self.S(box[1]) / img.height)
                    img = img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.LANCZOS)
                    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                    out.alpha_composite(img, ((w - img.width) // 2, (h - img.height) // 2))
            except Exception as e:                                    # a picture it cannot read: the program's drawing
                log = getattr(self.hd, "log", None)
                if callable(log):
                    log(f"{os.path.relpath(path, getattr(self.hd, 'root', '') or '.')}: {e}")
                out = None
        self.own[key] = out
        return out

    def portrait(self, name):
        """The owner's picture of a soldier beside J1 / J2 (sprites/mslug/marco.png...), a pygame surface or None.
        / Sa propre image d'un soldat à côté de J1 / J2."""
        key = ("portrait", name)
        s = self.rides.get(key)
        if s is None:
            img = self._own_picture(name.lower(), self.S(48), self.S(48), (48, 48))
            s = self.rides[key] = self.hd._surf(img) if img is not None else False
        return s or None

    def _cannon_tip(self, img):
        """Where the shells of the owner's tank start, as a part of the slot: the right end of the drawing in its upper
        part (the treads may go further at the bottom). / Le bout du canon de son char : le bout droit du haut du dessin."""
        alpha = img.getchannel("A").point(lambda v: 255 if v > 128 else 0)
        full = alpha.getbbox()
        if full is None:
            return None
        top = alpha.crop((0, full[1], img.width, full[1] + max(1, int((full[3] - full[1]) * 0.6))))
        box = top.getbbox() or (full[0], 0, full[2], 1)
        cb = top.crop((box[2] - 1, 0, box[2], top.height)).getbbox() or box    # its last column / sa dernière colonne
        x, y = box[2], full[1] + (cb[1] + cb[3]) / 2
        return (self.S(FRAME_DX) + x) / self.S(190), (self.S(FRAME_DY) + y) / self.S(108)

    def get(self, vals, side, base):
        return vals.get(base if side == "p1" else base + "_p2")

    # ------------------------------------------------------------ ce qui a changé depuis l'image précédente
    def update(self, eng, now):
        vals = eng.state.values
        key = (eng.state.meta.get("game") or "")
        if key != self.key or eng.state.meta is not self.meta_ref:    # another game, or the same one started again
            self.key, self.meta_ref = key, eng.state.meta             # / un autre jeu, ou le même relancé
            self.players = {"p1": Player("p1"), "p2": Player("p2")}
            self.mission = self.mission_shown = None
            self.rides, self.ride_own, self.ride_tip, self.own = {}, {}, {}, {}     # the pictures of this game / ses images
            self.boss, self.boss_prev, self.boss_rise = None, {}, {}     # (the rises keep their mission under "mission")
            self.boss_hit, self.boss_top = {}, {}
            self.boss_ref, self.boss_parts = None, set()
            self.boss_dead_prev = self.done_prev = self.complete_m = None
        dt = 0.0 if self.last is None else max(0.0, min(0.1, now - self.last))
        self.last = now
        self.fx_dt = dt
        for side in ("p1", "p2"):
            self._player(side, vals, now, dt)
        attract = self._attract(vals)
        anyone = any(self.playing(P) for P in self.players.values())
        for P in self.players.values():                         # panneaux qui arrivent ou repartent en glissant
            over = P.over_t is not None and now - P.over_t < 5.0
            target = 0.0 if attract else (1.0 if (self.playing(P) or over or anyone) else 0.0)
            P.shown += (1 if target > P.shown else -1) * min(abs(target - P.shown), dt / 0.45)
        c = _n(vals.get("credits"))
        if c is not None and self.credits is not None and c > self.credits:
            self._coin(now, c - self.credits)
        self.credits = c
        stages = self.stages(eng)
        m = _n(vals.get("mission"))
        # the game that says when its mission is complete (the first Metal Slug: its end-of-mission word once the boss is
        # down, Seb's memory snapshots of 19:15, 1.33 test 33; Metal Slug 4: its stage state): MISSION COMPLETE at that
        # moment, as on its screen, not when the next mission begins / le jeu qui dit quand sa mission est finie : le
        # bandeau à ce moment-là, comme sur son écran, pas au début de la mission suivante
        done = _n(vals.get("mission_done"))
        if (done == 1 and self.done_prev == 0 and anyone and not attract and self.mission is not None
                and self.complete_m != self.mission):
            self.complete_m = self.mission
            self.complete_t = now                                      # mission accomplie : bandeau, feu d'artifice
            for i in range(6):
                self.fx.later(0.15 + i * 0.25, self._firework)
        self.done_prev = done
        if m is not None and m != self.mission:
            theme = stages[(max(1, int(m)) - 1) % len(stages)]
            if self.mission is not None and m == self.mission + 1 and anyone and self.complete_m == self.mission:
                self._show_mission(theme, m)                           # the game said it already: the next one at once
            elif self.mission is not None and m == self.mission + 1 and anyone:
                self.complete_t = now                                  # mission accomplie : bandeau, feu d'artifice
                self.mission_t = now + 1.9
                self.fx.later(1.9, self._show_mission, theme, m)
                for i in range(6):
                    self.fx.later(0.15 + i * 0.25, self._firework)
            elif self.mission is not None:
                self._show_mission(theme, m)
            else:
                self.bd.set_theme(theme, now, wipe=0)
                self.mission_shown = m
            self.mission = m
        if attract and now - self.slide_t > self.SLIDE_EVERY:          # écran d'attente : diaporama des décors
            self.slide_t = now
            self.slide_i = (self.slide_i + 1) % len(stages)
            self.bd.set_theme(stages[self.slide_i], now)
        if self.was_attract and not attract and self.mission is None:  # la partie commence, sans numéro de mission connu
            self.bd.set_theme(stages[0], now)
        self.was_attract = attract
        self.time_v = _n(vals.get("time"))
        self._boss(vals, now, anyone and not attract, self.boss_slots(eng))
        self.fx.update(now)

    # ------------------------------------------------------------ the boss of the mission / le boss de la mission
    def boss_slots(self, eng):
        """The values that hold the bosses' lives: the game's "hd": {"boss_slots": [...]} (Metal Slug 4, the six enemy slots
        of the RetroAchievements notes), else boss_hp alone when the game has it. / Les valeurs qui portent la vie des boss."""
        key = self.key
        if self._slots_key != key:
            g = eng.library.get(key) or {}
            hd = g.get("hd") if isinstance(g.get("hd"), dict) else {}
            lst = hd.get("boss_slots")
            self._slots = [x for x in lst if isinstance(x, str)] if isinstance(lst, list) else ["boss_hp"]
            flag = hd.get("boss_flag")
            self._boss_flag = flag if isinstance(flag, str) and flag else None
            # a game without a flag: a life of at least "boss_min" is its boss, below it a big enemy (the first Metal
            # Slug, Seb's memory snapshots of 19:15: 400 for a helicopter, 2200 for the boss of mission 1, 1.33 test 31)
            # / sans drapeau : une vie d'au moins boss_min est le boss, en dessous un gros ennemi
            big = hd.get("boss_min")
            self._boss_big = int(big) if isinstance(big, (int, float)) and big > 0 else None
            # the life each mission's boss starts with, when known ("boss_life": {"1": 2200, "2": 3900}, the first Metal
            # Slug from Seb's captures): an entry filled with less is a big enemy, whatever its size (the mission 2
            # machine of 1200 before Hairbuster Riberts, test 33) / la vie de départ du boss de chaque mission
            life = hd.get("boss_life") if isinstance(hd.get("boss_life"), dict) else {}
            self._boss_life = {}
            for k, v in life.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 and str(k).isdigit():
                    self._boss_life[int(k)] = int(v)
            self._slots_key = key
        return self._slots

    def _boss(self, vals, now, playing, slots):
        """A game that gives its boss's life (Metal Slug 4 from the RetroAchievements notes): WARNING and its name when it
        comes, its life bar in the middle, BOSS DESTROYED when it runs out. The lives sit in slots of the game's enemies
        (each one holds any enemy in turn: Seb's capture of 23:58 showed mission 1's boss in the second slot, 250 of life,
        and an enemy of 100 in the fifth), so the boss is the slot a big life fills while the mission is played, named
        after the mission, and that slot alone is followed until it runs out.
        / Un jeu qui donne la vie de son boss : WARNING et son nom quand il arrive, sa barre de vie au milieu, BOSS DÉTRUIT.
        Les vies sont dans des cases d'ennemis : le boss est la case qu'une grosse vie remplit pendant la mission."""
        B = self.boss
        if B is not None and (not playing or self.mission != B["mission"]):
            self.boss = B = None                                       # the mission over, or everybody gone / mission finie
        cur = {}
        for slot in slots:                                             # a slot may be a whole list of lives / une liste
            v = vals.get(slot)
            if isinstance(v, list):
                for i, hp in enumerate(v):
                    cur[(slot, i)] = _n(hp)
            else:
                cur[slot] = _n(v)

        if not playing or self.mission != self.boss_rise.get("mission"):   # another mission: its own lives / une autre mission
            self.boss_rise = {"mission": self.mission}
            self.boss_hit, self.boss_top = {}, {}
            self.boss_ref, self.boss_parts = None, set()
        ref = self.boss_ref                                            # the boss's own entry this mission / sa case
        ref_hp = cur.get(ref) if ref is not None else None
        for slot, hp in cur.items():                                   # the entries a big life has just filled, while
            prev = self.boss_prev.get(slot)                            # somebody plays / les cases qu'une grosse vie remplit
            # the boss's parts (the first Metal Slug, Hairbuster Riberts in Seb's capture of 21:33: an entry filled with
            # the boss's life as it stood, 2420 then 1337, gone a few seconds later): not a boss, not a big enemy
            # / les morceaux du boss, remplis avec sa vie du moment : ni un boss ni un gros ennemi
            if slot in self.boss_parts:
                if hp is None or hp < BOSS_MIN or hp > BOSS_MAX:
                    self.boss_parts.discard(slot)                      # emptied: the entry is free again / libre
                continue
            # an empty entry holds 0 (Metal Slug 4) or 0xFFFF (the first Metal Slug) / une case vide : 0 ou 0xFFFF
            if (playing and hp is not None and BOSS_MIN <= hp <= BOSS_MAX and prev is not None
                    and (prev < BOSS_MIN or prev > BOSS_MAX)):
                if ref is not None and slot != ref and ref_hp is not None and hp == ref_hp:
                    self.boss_parts.add(slot)
                    continue
                self.boss_rise[slot] = now
                self.boss_top[slot] = hp
            # a big life hit (Seb's capture of 20:31: four small tanks of 210 to 300 at once, the bar on the first one filled
            # while he shot the others) / une grosse vie touchée : la barre suit l'ennemi qu'on frappe
            if (playing and hp is not None and prev is not None and hp < prev and BOSS_MIN <= prev <= BOSS_MAX):
                self.boss_hit[slot] = now
                self.boss_top[slot] = max(self.boss_top.get(slot, 0), prev)
        # the game that says when its boss is fought (Metal Slug 4, boss_flag): the big enemies of a mission have as much
        # life as the boss, so only a life filled while the flag is up, or up to 6 s before it, is the boss
        # / le jeu qui dit quand son boss se bat : seules les vies remplies pendant le drapeau, ou 6 s avant, sont le boss
        gate = _n(vals.get(self._boss_flag)) == 1 if self._boss_flag else True
        want = self._boss_life.get(int(self.mission)) if isinstance(self.mission, (int, float)) else None

        def rising(window=0.0):
            """The entry a boss's life filled in the last window seconds, the latest, or None. / La case remplie."""
            best = None
            for slot, t in self.boss_rise.items():
                if slot == "mission":
                    continue
                if (now - t <= window and cur.get(slot) is not None and BOSS_MIN <= cur[slot] <= BOSS_MAX
                        and (best is None or t > best[1])):
                    best = (slot, t)
            return best[0] if best else None

        def alert():
            """WARNING: the boss of the mission comes. / Le boss de la mission arrive."""
            self.boss_alerts += 1
            self.fx.flash(RED, 0.25, 0.5)
            self.fx.shake(8, 0.6)
            for i in range(3):
                self.fx.later(0.5 + i * 0.5, self.fx.shake, 3, 0.2)

        def is_boss(slot):
            """Whether the life in that entry is the boss of the mission: the game's flag up, or a life at least as big as
            the mission's boss ("boss_life", test 33) or as "boss_min" when it has no flag (the first Metal Slug, test 31),
            else a big enemy with a quiet bar (test 25). / Le boss de la mission : le drapeau du jeu levé, ou une vie
            d'au moins celle du boss de la mission, ou d'au moins boss_min ; sinon un gros ennemi."""
            if not gate:
                return False
            # Metal Slug 4's flag is up for every locked screen, a wave of helicopters as well as the boss (Seb's capture
            # of 22:39, mission 2: TOSCHKA DALANUE on a tank of 400, then on helicopters of 490), so the flag alone is a
            # gate and the life decides when the game gives one / le drapeau est une porte, la vie décide
            if want is not None:
                return max(self.boss_top.get(slot, 0), cur.get(slot) or 0) >= want
            if self._boss_big is not None:
                return (cur.get(slot) or 0) >= self._boss_big
            return True

        def hit(window):
            """The big life hit in the last window seconds, the latest, or None. / La grosse vie touchée en dernier."""
            best = None
            for slot, t in self.boss_hit.items():
                if now - t <= window and cur.get(slot) is not None and 0 < cur[slot] <= BOSS_MAX and (best is None or t > best[1]):
                    best = (slot, t)
            return best[0] if best else None

        def show(slot, it):
            name = vals.get("boss_name")
            top = max(self.boss_top.get(slot, 0), cur[slot])
            self.boss = {"name": name if isinstance(name, str) and it else tr("ENNEMI", "ENEMY"),
                         "top": top, "hp": cur[slot], "t0": now, "down": None, "mission": self.mission, "hit_t": -99.0,
                         "slot": slot, "moved": now, "minor": not it}
            if it:
                self.boss_ref = slot
                alert()

        def twin(B):
            """The entry the boss's life went on in when its own emptied: filled with the same life at the same time
            (Hairbuster Riberts came in two entries of 3900 at once, one gone two seconds later, Seb's capture of 21:33)
            / la case jumelle du boss, remplie en même temps avec la même vie, quand la sienne se vide"""
            for slot, top in self.boss_top.items():
                if (slot != B["slot"] and top == B["top"] and cur.get(slot) is not None and 0 < cur[slot] <= top
                        and abs(self.boss_rise.get(slot, -99.0) - self.boss_rise.get(B["slot"], -99.0)) <= 0.5):
                    return slot
            return None

        def fall(B):
            """It fell: BOSS DESTROYED, a flash for a big enemy. / Il tombe."""
            B["hp"], B["down"] = 0, now
            if B.get("minor"):                                         # a machine down: a flash, no fireworks / un engin
                self.fx.flash((255, 220, 160), 0.15, 0.3)
                self.fx.shake(5, 0.3)
            else:
                self.boss_downs += 1
                self.fx.flash((255, 220, 160), 0.3, 0.5)
                self.fx.shake(10, 0.7)
                for i in range(8):
                    self.fx.later(0.1 + i * 0.22, self._firework)

        # the game that says when its boss is dead (the first Metal Slug, its flag from the RetroAchievements notes, 1 to 0
        # as Tetsuyuki fell in Seb's snapshots of 19:15): BOSS DESTROYED at that moment, bar or no bar
        # / le jeu qui dit quand son boss est mort : BOSS DÉTRUIT à ce moment-là, barre ou pas
        dead = _n(vals.get("boss_dead"))
        died = dead == 1 and self.boss_dead_prev == 0 and playing and self.mission is not None
        self.boss_dead_prev = dead
        if died and (B is None or B.get("minor")):                     # (a boss already down: said once)
            name = vals.get("boss_name")
            self.boss = B = {"name": name if isinstance(name, str) else "", "top": 1, "hp": 1, "t0": now, "down": None,
                             "mission": self.mission, "hit_t": -99.0, "slot": None, "moved": now, "minor": False}
            fall(B)

        if B is None:
            if playing:
                slot = rising(6.0 if self._boss_flag else 0.0) if gate else rising(0.0)
                if slot is not None:
                    # a big life without the game's flag: a tank, a helicopter, a sergeant on foot (Seb, test 25: its bar is
                    # worth showing, but it is not the boss and the game gives no name); with "boss_min" instead of a flag,
                    # a life that big is the boss (test 31) / une grosse vie sans le drapeau ; avec boss_min, le boss
                    show(slot, is_boss(slot))
                else:
                    slot = hit(0.5)                                    # a big enemy hit while no bar shows: its bar, quiet
                    if slot is not None and not is_boss(slot):         # / un gros ennemi touché sans barre : la sienne
                        show(slot, False)
        else:
            if B.get("minor") and gate and self._boss_flag and B["down"] is None and is_boss(B["slot"]):
                name = vals.get("boss_name")                           # the game's flag goes up: that machine was the
                                                                       # boss / le drapeau se lève
                B.update(minor=False, name=name if isinstance(name, str) else "", t0=now)
                self.boss_ref = B["slot"]
                alert()
            if B.get("minor") and B["down"] is None:
                # the boss of the mission comes while a big enemy has the bar: the boss takes it (Seb's capture of 20:31:
                # Tetsuyuki came while a small tank kept the bar, no WARNING at all) / le boss arrive : il prend la barre
                big = rising(0.0)
                if big is not None and big != B["slot"] and is_boss(big):
                    show(big, True)
                    B = self.boss
                elif now - B["moved"] > 2.0:
                    # the enemy that has the bar is left alone: the bar goes to the one being hit, or fades after a while
                    # (a tank passed by, a cannon out of reach) / l'ennemi laissé tranquille : la barre va à celui qu'on
                    # frappe, ou s'efface au bout d'un moment
                    other = hit(0.5)
                    if other is not None and other != B["slot"] and not is_boss(other):
                        show(other, False)
                        B = self.boss
                    elif now - B["moved"] > MINOR_IDLE:
                        self.boss = B = None
            if B is None:
                self.boss_prev = cur
                return
            if B["slot"] is None:                                      # BOSS DESTROYED on the game's word alone / sur
                if now - B["down"] > 3.0:                              # le seul mot du jeu
                    self.boss = None
                self.boss_prev = cur
                return
            hp = cur.get(B["slot"])
            if B["down"] is None:
                done = _n(vals.get("mission_done")) == 1 or died        # the mission complete, or the game's flag: it fell
                # its life goes on in another entry (a new phase, Seb's capture of 00:22, Metal Slug 4 and its flag): only
                # an entry a boss-sized life filled, not a soldier of 250 passing by (both Metal Slugs, test 33)
                # / sa vie continue ailleurs : seulement une case remplie d'une vie de boss
                other = rising(0.5) if hp is not None and now - B["moved"] > 2.0 and not B.get("minor") else None
                if other is not None and other != B["slot"] and is_boss(other):
                    B["slot"], B["moved"] = other, now
                    self.boss_ref = other
                    hp = B["hp"] = cur[other]
                    B["top"] = max(B["top"], hp)
                if hp is None or hp > B["top"] * 1.5:                  # not a life any more: the entry is empty, or holds
                    other = twin(B) if not B.get("minor") else None    # another thing / plus une vie : la case s'est vidée
                    if other is not None:                              # (its twin goes on) / (sa jumelle continue)
                        B["slot"], B["moved"] = other, now
                        self.boss_ref = other
                        B["hp"] = cur[other]
                    elif died or (now - B["moved"] <= 1.0 and B["hit_t"] > -1):   # emptied right after a hit, or the
                        fall(B)                                        # game says it fell (Hairbuster Riberts, 155 then
                                                                       # gone) / vidée sur un coup, ou le jeu le dit
                    else:
                        self.boss = None
                elif hp > B["top"]:
                    B["top"] = hp
                elif hp < B["hp"] or done:
                    if hp < B["hp"]:
                        B["hit_t"] = now
                        B["moved"] = now
                    B["hp"] = 0 if done else hp
                    if hp <= 0 or done:
                        fall(B)
            elif now - B["down"] > (0.8 if B.get("minor") else 3.0):
                self.boss = None
        self.boss_prev = cur

    def stages(self, eng):
        key = self.key
        if self._stages_key != key:
            g = eng.library.get(key) or {}
            lst = (g.get("hd") or {}).get("stages")
            self._stages = [s for s in lst if s in hd_stages.hd_bg.BUILDERS] if lst else list(hd_stages.MISSION_STAGES)
            self._stages_key = key
            self.bd.prebuild(self._stages)
        return self._stages

    def _show_mission(self, theme, m):
        self.bd.set_theme(theme, self.fx.now)
        self.mission_t = self.fx.now
        self.mission_shown = m
        self.fx.flash((255, 220, 160), 0.2, 0.3)

    def _firework(self):
        rng = self.rng
        x = self.W / 2 + rng.uniform(-520, 520) * self.s
        y = rng.uniform(50, 170) * self.s
        col = rng.choice(((255, 90, 90), (255, 220, 80), (90, 220, 255), (140, 255, 150), (255, 130, 230)))
        self.fx.glow(x, y, 10, 90, col, 0.35)
        self.fx.sparks(x, y, 36, col, (150, 520), (0, 360), (0.7, 1.3), 260, "front", 3, 20)

    def playing(self, P):
        return P.mode in (1, 2)

    def _player(self, side, vals, now, dt):
        P = self.players[side]
        mode = _n(vals.get("p1_mode" if side == "p1" else "p2_mode"))
        if mode is None:                                            # pas de BIOS : J1 joue, J2 s'il a un score
            mode = 1 if side == "p1" or (_n(self.get(vals, side, "score")) or 0) > 0 else 0
        if mode != P.mode:
            if mode == 1 and P.mode not in (1, 2):
                P.join_t = now
                # quiet until the game has set its soldier up: the first Metal Slug sets his lives 0, 1, 0, 2, 0 over its
                # HOW TO PLAY screen with its timer at 1, then wipes his block and starts the mission with the timer at 60
                # (Seb's capture of 20:31: 7 s, 1UP ! and LAST LIFE on the HD screen meanwhile) / au calme jusqu'à ce que
                # le jeu ait mis son soldat en place, le chrono de la mission parti
                P.sync_until = now + SYNC_MAX
                P.over_t = None
                P.seen = {}
                P.score_disp = None
                if P.mode is not None and side == "p2" and self.playing(self.players["p1"]):
                    self.fx.text(tr("J2 ARRIVE !", "P2 JOINS IN!"), self.W / 2, self.S(330), ACCENT["p2"], 56, life=1.6, rise=40)
            elif mode == 3 and P.mode in (1, 2):
                P.over_t = now
                self.fx.shake(7, 0.35)
            P.mode = mode
        if not self.playing(P):
            P.shots = []
            return
        cur = {b: _n(self.get(vals, side, b)) for b in ("score", "lives", "bombs", "ammo", "weapon", "prisoners", "vehicle",
                                                          "vehicle_kind", "vehicle_hp", "vehicle_ammo", "grenades_out")}
        inp = _n(vals.get("p1_input" if side == "p1" else "p2_input"))
        # the block wiped: 0xFF everywhere at once, the bombs with the ammo or the weapon, or the lives (Metal Slug 4 gives
        # its handgun 65535 of ammo, unlimited, and that alone is no wipe: Seb's video of 22:39, test 33, no grenade thrown
        # on the HD screen while he held the handgun) / le bloc effacé : 0xFF partout, pas la seule munition illimitée
        wiped = ((cur["bombs"] == 255 and (cur["ammo"] == 65535 or cur["weapon"] == 255))
                 or (cur["lives"] is not None and cur["lives"] >= 250))
        quiet = now < P.sync_until
        if quiet and not wiped:
            tm = _n(vals.get("time"))
            if now - P.join_t >= SYNC_MIN and (tm is None or tm >= 2 or now - P.join_t >= SYNC_MAX):
                P.sync_until = now                                     # the mission runs: these values are the start,
                                                                       # the next ones are compared to them / le départ
        # the soldier's block wiped (0xFF everywhere) for a few images as a game begins and between two lives (Seb's
        # video of 19:20, the first Metal Slug: +245 BOMBES and four grenades blowing up at the start, 1.33 test 31): not
        # values, nothing to compare / le bloc du soldat effacé quelques images : pas des valeurs, rien à comparer
        if wiped:
            return
        old = P.seen
        P.seen = dict(cur, input=inp)
        if inp is not None:
            P.move = 1.0 if inp & BTN_RIGHT else (-1.0 if inp & BTN_LEFT else 0.0)
        if quiet or not old:
            P.tank = self.aboard(cur["vehicle"])                       # déjà à bord : sans fanfare / already aboard
            P.ride = self.ride_kind(cur["vehicle_kind"]) if P.tank else None
            if cur["weapon"] is not None:
                P.weapon_kind = self.weapon(side, cur["weapon"])[1] or "pistol"
                P.ammo_max = max(1, cur["ammo"] or 0)
                P.gauge = 1.0 if (cur["ammo"] or 0) > 0 else 0.0
            return
        self._diff(side, P, old, cur, inp, now)

    def _diff(self, side, P, old, cur, inp, now):
        sc, so = cur["score"], old.get("score")
        if sc is not None and so is not None and sc > so:
            P.score_t = now
            if now - P.float_t < 0.3:
                P.float_acc += sc - so
            else:
                P.float_acc = sc - so
            P.float_t = now
            self._score_float(side, P, now, sc)
        lv, lo = cur["lives"], old.get("lives")
        if lv is not None and lo is not None:
            if lv < lo:
                self._life_lost(side, P, now, lo)
            elif lv > lo:
                self._life_up(side, P, now)
        w, wo = cur["weapon"], old.get("weapon")
        if w is not None and wo is not None and w != wo:
            self._weapon_change(side, P, now, w, cur["ammo"])
        elif cur["ammo"] is not None and old.get("ammo") is not None and w == wo:
            d = cur["ammo"] - old["ammo"]
            if d < 0 and not P.tank:
                self._queue_shots(P, now, -d)
            elif d > 0:
                P.ammo_max = max(P.ammo_max, cur["ammo"])
                P.weapon_t = now
                self.fx.text(f"+{d}", self._ammo_xy(side)[0], self.S(250), GREEN, 40, life=1.0)
        b, bo = cur["bombs"], old.get("bombs")
        if b is not None and bo is not None:
            if b < bo:
                for i in range(min(4, bo - b)):
                    P.flying += 1
                    self.fx.later(i * 0.16, self._throw, side, P, bo - i - 1)
            elif b > bo:
                P.bomb_add = (now, b - bo)
                self.fx.text(tr(f"+{b - bo} BOMBES", f"+{b - bo} BOMBS"), self._bomb_xy(side, 0)[0] + (self.S(120) if side == "p1" else -self.S(120)),
                             self.S(340), GOLD, 36, life=1.2)
        go, goo = cur["grenades_out"], old.get("grenades_out")
        if go is not None and goo is not None:
            if go > goo:                                   # the game's grenade left the hand: wait for its explosion
                P.out_ok = True                            # la grenade du jeu est partie : on attend son explosion
                for g in P.live:
                    g.life = max(g.life, self.fx.now - g.t0 + self.GRENADE_WAIT)
            elif go < goo and P.out_ok:                    # it blew up, on an enemy or at its second bounce / elle explose
                self._explode_live(P, goo - go)
        pr, po = cur["prisoners"], old.get("prisoners")
        if pr is not None and po is not None and pr > po:
            P.prison_t = now
            x, y = self._prisoner_xy(side)
            self.fx.sparks(x, y, 18, GOLD, (200, 600), (200, 340), (0.3, 0.7), 500, "front", 3, 26)
            self.fx.glow(x, y, 10, 70, GOLD, 0.4)
            self.fx.text(tr("+1 PRISONNIER", "+1 PRISONER") if pr - po == 1 else tr(f"+{pr - po} PRISONNIERS", f"+{pr - po} PRISONERS"), x, y - self.S(40), CREAM, 34, life=1.3)
        if inp is not None and (P.weapon_kind == "pistol" or P.tank):
            prev = old.get("input")
            if prev is not None and (inp & BTN_A) and not (prev & BTN_A):
                if P.tank:
                    self._tank_vulcan(side, P)                         # la mitrailleuse du char / the tank's machine gun
                else:
                    self._queue_shots(P, now, 1)
        self._vehicle(side, P, old, cur, now)

    # ------------------------------------------------------------ le char / the tank
    def _vehicle(self, side, P, old, cur, now):
        """In and out of a vehicle (the tank, the camel, the submarine...), the hits it takes, its shells.
        / Le véhicule (char, chameau, sous-marin...) : dedans, dehors, coups, obus."""
        v, vo = cur["vehicle"], old.get("vehicle")
        if v is None:
            P.tank, P.ride = False, None
            return
        # a flag byte (bit 0) in the first Metal Slug, 2 and 4: its other bits are the soldier's state on foot (1.33 test
        # 29, Seb's capture of 17:58: 2, 4, 6, 16, 22 while he moves and shoots, read as the tank since test 21); a kind in
        # the others / un octet de bits dans le premier Metal Slug, le 2 et le 4, un genre dans les autres
        aboard = self.aboard
        riding = aboard(v)
        if vo is not None and riding != aboard(vo):
            if riding:
                P.ride = self.ride_kind(cur["vehicle_kind"])
                self._tank_in(side, P, now)
            else:
                self._tank_out(side, P, now, old.get("vehicle_hp"))
        P.tank = riding
        P.ride = self.ride_kind(cur["vehicle_kind"]) if riding else None
        if not riding or vo is None or not aboard(vo):
            return
        hp, ho = cur["vehicle_hp"], old.get("vehicle_hp")
        if hp is not None and ho is not None and hp < ho:
            self._tank_hit(side, P, now, hp)
        sh, so = cur["vehicle_ammo"], old.get("vehicle_ammo")
        if sh is not None and so is not None and sh < so <= 99:
            for i in range(min(3, int(so - sh))):
                self.fx.later(i * 0.25, self._tank_fire, side, P)

    def _tank_in(self, side, P, now):
        P.tank_t = now
        P.shots = []
        sx, sy = self._slot_xy(side)
        cx, cy = sx + self.S(95), sy + self.S(54)
        self.fx.glow(cx, cy, 30, 240, GREEN, 0.45)
        self.fx.smoke(cx, sy + self.S(100), 4, (10, 18), 2.6, (0.5, 0.9), (20, 60), 20, (170, 150, 120), 120, "front")
        self.fx.text(tr(*RIDE_IN.get(P.ride or "tank", RIDE_IN_ANY)), cx, sy + self.S(96), GREEN, 40, life=1.3, rise=40)
        self.fx.shake(4, 0.25)                                         # over the picture, not the name / sur l'image

    def _tank_out(self, side, P, now, hp):
        P.weapon_t = now                                              # l'arme revient dans la carte / the weapon comes back
        if hp is not None and hp > 0:
            return
        sx, sy = self._slot_xy(side)                                   # détruit : il explose / destroyed: it blows up
        cx, cy = sx + self.S(95), sy + self.S(54)
        self.fx.explosion(cx, cy, 1.4)
        for i in range(3):
            self.fx.later(0.12 + i * 0.14, self._boom, cx + self.rng.uniform(-60, 60) * self.s, cy + self.rng.uniform(-20, 30) * self.s)
        self.fx.text(tr(*RIDE_LOST.get(P.ride or "tank", RIDE_LOST_ANY)), cx, sy + self.S(96), RED, 40, life=1.6, rise=40)
        self.fx.shake(9, 0.5)

    def _tank_hit(self, side, P, now, hp):
        P.tank_hit_t = now
        gx, gy = self._tank_gauge_xy(side)
        self.fx.sparks(gx, gy, 18, (255, 120, 70), (200, 600), (0, 360), (0.25, 0.6), 600, "front", 3, 24)
        self.fx.glow(gx, gy, 10, 80, RED, 0.35)
        self.fx.shake(5 if hp > 0 else 8, 0.3)

    def _tank_fire(self, side, P):
        """A cannon shell, from the tank to the backdrop. / Un obus du char vers le décor."""
        if not P.tank:
            return
        fx, rng = self.fx, self.rng
        x, y = self._tip_xy(side, "tank")
        d = 1 if side == "p1" else -1
        P.recoil_t = fx.now
        fx.muzzle(x, y, d, 1.8, FIRE_HOT)
        tx = self.W / 2 + d * rng.uniform(-40, 260) * self.s
        ty = self.H * 0.725 + rng.uniform(-20, 30) * self.s
        p = fx.projectile("rocket", x + d * self.S(10), y, tx, ty, 0.36, 4, self._shell_hit, spin=0.0, kind="rocket", trail=0.02)
        p.rot = -math.degrees(math.atan2(ty - y, tx - x))
        fx.smoke(x - d * self.S(60), y, 4, (10, 18), 2.6, (0.4, 0.8), (10, 40), 20, (170, 160, 150), 140, "front")
        fx.shake(4, 0.18)

    def _tank_vulcan(self, side, P):
        fx, rng = self.fx, self.rng
        x, y = self._tip_xy(side, "tank")
        d = 1 if side == "p1" else -1
        fx.muzzle(x, y - self.S(6), d, 0.9, FIRE_HOT)
        for i in range(2):
            tx = self.W / 2 + d * rng.uniform(-60, 300) * self.s
            ty = self.H * 0.725 + rng.uniform(-30, 40) * self.s
            fx.tracer(x + d * self.S(18), y - self.S(6), tx, ty, 2400, (255, 220, 120), 4, 150, "front")

    def _shell_hit(self, x, y):
        self.fx.explosion(x, y, 0.9)

    # ------------------------------------------------------------ effets des événements
    def _score_float(self, side, P, now, score):
        x = self._score_end_x(side, score)
        txt = f"+{P.float_acc}"
        for p in list(self.fx.parts):                            # un seul « +N » à la fois par joueur
            if p.kind == "text" and p.name == side + "score":
                p.dead = True
        t = self.fx.text(txt, x, self.S(160), (255, 238, 150), 34, key="stencil", life=0.9, rise=70,
                         align="left" if side == "p1" else "right")
        t.name = side + "score"

    def _life_lost(self, side, P, now, before):
        P.hit_t = now
        x, y = self._helmet_xy(side, max(0, int(before) - 1), int(before))
        self.fx.obj("helmet", x, y, (-1 if side == "p1" else 1) * self.rng.uniform(80, 200), -self.rng.uniform(420, 560),
                    gravity=1500, vrot=self.rng.uniform(-500, 500), life=1.3)
        self.fx.sparks(x, y, 14, (255, 90, 60), (200, 600), (0, 360), (0.25, 0.6), 600, "front", 3, 24)
        self.fx.text(tr("-1 VIE", "-1 LIFE"), x, y + self.S(36), RED, 40, life=1.2, rise=50)
        self.fx.shake(6, 0.35)

    def _life_up(self, side, P, now):
        P.up_t = now
        x, y = self._helmet_xy(side, 0, 1)
        self.fx.glow(x, y, 10, 90, GREEN, 0.5)
        self.fx.sparks(x, y, 16, GREEN, (150, 500), (0, 360), (0.3, 0.7), 200, "front", 3, 22)
        self.fx.text("1UP !", x, y + self.S(40), GREEN, 46, life=1.4, rise=40)

    def _weapon_change(self, side, P, now, code, ammo):
        name, kind = self.weapon(side, code)
        P.weapon_t = now
        P.weapon_kind = kind or "gun"
        P.shots = []
        if kind == "pistol":
            P.empty_t = now
            P.ammo_max = 1
            self.fx.text(tr("PLUS DE MUNITIONS", "OUT OF AMMO"), self._card_text_x(side), self.S(232), (255, 120, 90), 30, life=1.2, rise=30,
                         align="left" if side == "p1" else "right")
            return
        P.ammo_max = max(1, ammo or 1)
        P.gauge = 0.0
        drop = 0.42                                                    # la caisse tombe dans la carte de l'arme
        P.weapon_t = now + drop
        sx, sy = self._slot_xy(side)
        cx = sx + self.S(95)
        p = self.fx.obj("crate", cx, -self.S(60), self.rng.uniform(-30, 30), 300, gravity=2090, vrot=self.rng.uniform(-90, 90),
                        life=drop, rot=self.rng.uniform(-10, 10))
        p.on_end = (self._crate_open, (side, name, cx, self.S(250)))

    def _crate_open(self, side, name, cx, cy):
        fx, rng = self.fx, self.rng
        for _ in range(7):                                             # planches qui volent
            fx.obj("plank", cx + rng.uniform(-20, 20) * self.s, cy, rng.uniform(-420, 420), -rng.uniform(300, 650), gravity=1700,
                   vrot=rng.uniform(-800, 800), life=1.0, rot=rng.uniform(0, 360))
        fx.glow(cx, cy, 30, 260, ACCENT[side], 0.45)
        fx.sparks(cx, cy, 26, (255, 230, 160), (300, 900), (0, 360), (0.3, 0.7), 300, "front", 3, 30)
        fx.smoke(cx, cy, 3, (10, 18), 2.6, (0.5, 0.9), (20, 60), 20, (170, 150, 120), 120, "front")
        fx.shake(4, 0.2)

    def _queue_shots(self, P, now, n):
        st = STYLE.get(P.weapon_kind, STYLE["gun"])
        gap = st["gap"]
        if len(P.shots) > 14:
            return
        n = min(n, 12)
        start = max(now, P.shots[-1] + gap if P.shots else now)
        span = 0.12 if n > 1 else 0.0                              # étalés jusqu'à la lecture suivante
        gap = max(0.03, min(gap, span / n if span else gap))
        for i in range(n):
            P.shots.append(start + i * gap)

    def _fire(self, side, P, now):
        kind = P.weapon_kind
        st = STYLE.get(kind, STYLE["gun"])
        rng, fx = self.rng, self.fx
        x, y = self._tip_xy(side, kind)
        d = 1 if side == "p1" else -1
        P.recoil_t = now
        if st.get("flame"):                                       # jet continu tant que la réserve baisse
            P.flame_until = max(P.flame_until, now + 0.2)
            return
        fx.muzzle(x, y, d, st.get("muzzle", 1.0), (160, 240, 255) if st.get("laser") else FIRE_HOT)
        tx = self.W / 2 + d * rng.uniform(-60, 300) * self.s
        ty = self.H * 0.725 + rng.uniform(-30, 40) * self.s
        if st.get("rocket"):
            ang = math.degrees(math.atan2(ty - y, tx - x))
            p = fx.projectile("rocket", x + d * self.S(10), y, tx, ty, 0.42, 6, self._rocket_hit, spin=0.0, kind="rocket", trail=0.026)
            p.rot = -ang
            fx.smoke(x - d * self.S(200), y, 4, (10, 18), 2.6, (0.4, 0.8), (10, 40), 20, (170, 160, 150), 140, "front")
            fx.shake(3, 0.15)
            return
        col, wd, ln = st["tracer"]
        for i in range(st.get("pellets", 1)):
            spread = (i - (st.get("pellets", 1) - 1) / 2) * 0.1 if st.get("pellets") else 0
            tyy = ty + spread * 600 * self.s + rng.uniform(-10, 10) * self.s
            fx.tracer(x + d * self.S(18), y, tx + rng.uniform(-30, 30) * self.s, tyy, 2400 if not st.get("laser") else 4200,
                      col, wd, ln, "front")
        if st.get("pellets"):
            fx.smoke(x + d * self.S(30), y, 3, (8, 14), 2.4, (0.4, 0.7), (20, 50), 10, (150, 146, 140), 130, "front")
            fx.shake(2.5, 0.12)
        cas = st.get("casing")
        if cas:
            px, py = PORT.get(kind, PORT["gun"])
            sx, sy = self._slot_xy(side)
            ex = sx + (px if side == "p1" else 1 - px) * self.S(190)
            ey = sy + py * self.S(108)
            fx.obj(cas, ex, ey, -d * rng.uniform(40, 170), -rng.uniform(240, 380), gravity=1700,
                   vrot=rng.uniform(-900, 900), life=1.0, floor=self.S(316), bounce=0.35, rot=rng.uniform(0, 360))

    def _flame(self, side, P, now, dt):
        """Jet du lance-flammes : des boules de feu qui partent vite, gonflent, montent et s'éteignent."""
        rng, fx = self.rng, self.fx
        x, y = self._tip_xy(side, "flame")
        d = 1 if side == "p1" else -1
        n = max(2, int(dt * 260))
        for i in range(n):
            col = rng.choice((FIRE_HOT, FIRE, FIRE, (255, 110, 40)))
            p = fx.glow(x + d * self.S(4), y + rng.uniform(-5, 5) * self.s, rng.uniform(6, 10), rng.uniform(46, 84), col,
                        rng.uniform(0.32, 0.55), "front", 0.95, 0.0, hot=0.3)
            p.vx = d * rng.uniform(1100, 1500) * self.s
            p.vy = rng.uniform(-90, 50) * self.s
            p.ay = -300 * self.s
            p.drag = 3.4
        g = fx.glow(x + d * self.S(10), y, 12, 30, (255, 236, 180), 0.05, "front", 1.0, 0.2, hot=0.8)
        g.vx = 0
        if rng.random() < dt * 6:
            fx.smoke(x + d * self.S(rng.uniform(260, 380)), y - self.S(30), 1, (14, 22), 2.8, (0.9, 1.5), (30, 70), 30,
                     (52, 42, 46), 120, "back")

    def _rocket_hit(self, x, y):
        self.fx.small_blast(x, y, 1.4, "back")
        self.fx.shake(4, 0.2)

    def _throw(self, side, P, index):
        """The grenade leaves its row in an arc, bounces once and blows up as it lands again, as in the game (about a second
        after the throw). When the game's grenades on screen are read, it waits for the game's own to blow up instead,
        on an enemy hit on the way as on the ground, two seconds at most. / La grenade part en cloche, rebondit une fois et
        explose en retombant, comme dans le jeu ; quand on lit les grenades du jeu, elle attend que celle du jeu explose."""
        x, y = self._bomb_xy(side, index)
        d = 1 if side == "p1" else -1
        tx = self.W / 2 + d * self.rng.uniform(-80, 220) * self.s
        ty = self.H * 0.74 + self.rng.uniform(-8, 26) * self.s
        P.bomb_t = self.fx.now
        self.fx.glow(x, y, 6, 40, GOLD, 0.25)
        P.flying = max(0, P.flying - 1)
        if P.early > 0:                                    # the game's one already blew up / celle du jeu a déjà explosé
            P.early -= 1
            self._boom(x + (tx - x) * 0.3, y - self.S(60))
            return
        g = self.fx.projectile("grenade", x, y, tx, ty, self.GRENADE_FLIGHT, 170, None, spin=d * 620, kind="proj", trail=0.03)
        g.floor, g.bounce = ty, self.GRENADE_BOUNCE
        land = g.vy + g.ay * self.GRENADE_FLIGHT           # its speed as it lands the first time / en touchant le sol
        g.life = self.GRENADE_FLIGHT + 2 * land * self.GRENADE_BOUNCE / g.ay     # the second landing / le second rebond
        if P.out_ok:
            g.life = self.GRENADE_WAIT                     # the game tells when it blows up / le jeu dit quand
        g.on_end = (self._boom_live, (P, g))
        P.live.append(g)

    def _boom_live(self, P, g):
        """A grenade of the HD screen blows up where it is. / Une grenade explose là où elle est."""
        if g in P.live:
            P.live.remove(g)
        g.on_end = None
        g.dead = True
        self._boom(g.x, g.y)

    def _explode_live(self, P, n):
        """The game's grenades blew up: as many of ours, the oldest first, where they are. One that has not left the hand
        yet blows up as soon as it does. / Les grenades du jeu ont explosé : autant des nôtres, les plus anciennes d'abord."""
        for _ in range(int(n)):
            live = [g for g in P.live if not g.dead]
            if live:
                self._boom_live(P, live[0])
            elif P.flying > 0:
                P.early += 1

    def _boom(self, x, y):
        """A grenade blows up, player 1's or player 2's: the explosion, the whole screen shakes hard and lights up orange; a
        grenade right after another one shakes less (no endless quake). / Une grenade explose : tout l'écran tremble fort et
        s'éclaire ; celle qui suit de près une autre tremble moins."""
        first = self.fx.now - self.boom_t > 0.35
        self.boom_t = self.fx.now
        self.booms += 1
        self.fx.explosion(x, y, 1.15)
        self.fx.shake(15 if first else 6, 0.6)
        self.fx.flash((255, 200, 130), 0.24 if first else 0.1, 0.24)

    def _coin(self, now, n):
        """Coins inserted: each one falls onto the credits' coin; one +n CRÉDITS for them all.
        / Pièces mises : chacune tombe sur la pièce des crédits ; un seul +n CRÉDITS pour toutes."""
        k = min(3, n)
        for i in range(k):
            self.fx.later(i * 0.22, self._drop_coin, n if i == k - 1 else 0)

    def _drop_coin(self, n):
        x, y = self.coin_xy or (self.W / 2, self.S(398))
        p = self.fx.projectile(self.coin_sprite, x, self.S(-40), x, y, 0.55, 90, self._coin_ding, spin=0, trail=0)
        p.on_end = (self._coin_ding, (x, y, n))
        p.floor, p.bounce = y, 0.0                                # stops right on the coin / s'arrête pile dessus

    def _coin_ding(self, x, y, n=0):
        self.coin_t = self.fx.now
        self.fx.glow(x, y, 12, 96, GOLD, 0.35)
        self.fx.sparks(x, y, 16, GOLD, (180, 520), (200, 340), (0.3, 0.6), 500, "front", 2, 18)
        if n and not self.in_attract and self.coin_box is not None:     # waiting screen: PRESS START says it / l'attente le dit
            bx, by = self.coin_box
            word = tr(f"+{n} CRÉDIT" + ("S" if n > 1 else ""), f"+{n} CREDIT" + ("S" if n > 1 else ""))
            self.fx.text(word, bx, by - self.S(30), GOLD, 36, life=1.2, rise=40)

    # ------------------------------------------------------------ positions (pour les effets)
    def _slot_xy(self, side):
        x0 = self.x0(side, self.players[side])
        return self.X(side, x0, PW - 222, 190), self.S(195)

    def _tip_xy(self, side, kind):
        sx, sy = self._slot_xy(side)
        P = self.players[side]
        own = self.ride_tip.get(P.ride or "tank") if kind == "tank" else None
        tx, ty = own or TIP.get(kind or "gun", TIP["gun"])
        if side == "p2":
            tx = 1 - tx
        kick = max(0.0, 1 - (self.fx.now - P.recoil_t) / 0.08) * self.S(6)
        return sx + tx * self.S(190) - (kick if side == "p1" else -kick), sy + ty * self.S(108)

    def _card_text_x(self, side):
        x0 = self.x0(side, self.players[side])
        return self.X(side, x0, 36)

    def _ammo_xy(self, side):
        x0 = self.x0(side, self.players[side])
        return self.X(side, x0, PW - 246), self.S(282)

    def _score_end_x(self, side, score):
        x0 = self.x0(side, self.players[side])
        w = self.hd.text_width(self._fmt(score or 0), "stencil", self.S(92))
        return self.X(side, x0, 28) + (w + self.S(18) if side == "p1" else -w - self.S(18))

    def _helmet_xy(self, side, i, n):
        x0 = self.x0(side, self.players[side])
        lx = PW - 24 - 46 - (min(n, 5) - 1 - i) * 52 if n <= 5 else PW - 24 - 46
        return self.X(side, x0, lx, 46) + self.S(23), self.S(42)

    def _bomb_xy(self, side, i):
        x0 = self.x0(side, self.players[side])
        return self.X(side, x0, 28 + min(i, 9) * 31, 30) + self.S(15), self.S(370)

    def _prisoner_xy(self, side):
        x0 = self.x0(side, self.players[side])
        return self.X(side, x0, PW - 150, 34) + self.S(17), self.S(370)

    @staticmethod
    def _fmt(n):
        return f"{int(n):,}".replace(",", " ")

    def _attract(self, vals):
        m1, m2 = _n(vals.get("p1_mode")), _n(vals.get("p2_mode"))
        return m1 is not None and m1 not in (1, 2) and (m2 is None or m2 not in (1, 2)) and \
            all(self.players[s].over_t is None or self.fx.now - self.players[s].over_t > 5.0 for s in ("p1", "p2"))

    # ------------------------------------------------------------ dessin
    def render(self, screen, eng, now, logo):
        self.set_coin_symbol((getattr(eng, "cfg", None) or {}).get("coin_symbol", "€"))
        self.update(eng, now)
        vals = eng.state.values
        self.in_attract = self._attract(vals)
        for side in ("p1", "p2"):                                   # tirs en attente
            P = self.players[side]
            while P.shots and P.shots[0] <= now:
                P.shots.pop(0)
                if self.playing(P):
                    self._fire(side, P, now)
            if now < P.flame_until and self.playing(P) and P.weapon_kind == "flame":
                self._flame(side, P, now, self.fx_dt)
        ox, oy = self.fx.offset()
        target = screen
        if ox or oy:
            if self.buf is None or self.buf.get_size() != screen.get_size():
                self.buf = self.pg.Surface(screen.get_size()).convert()
            target = self.buf
        move = max([P.move for P in self.players.values() if self.playing(P)] or [0.0])
        if self._attract(vals):
            move = -0.15
        self.bd.draw(target, now, move)
        self.fx.draw(target, "back")
        if self._attract(vals):
            self._draw_attract(target, vals, logo, now)
        else:
            for side in ("p1", "p2"):
                self._draw_panel(target, side, vals, now)
            self._draw_center(target, vals, logo, now)
        self.fx.draw(target, "front")
        self._draw_banner(target, now)
        self.fx.draw_flash(target)
        if target is not screen:
            screen.fill((0, 0, 0))
            screen.blit(target, (ox, oy))
        if self.warm and len(self.fx.parts) < 120:
            self._warm_step(0.004)

    def _draw_attract(self, screen, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        credits = _n(vals.get("credits"))
        if credits is None:
            ly, lh, y, ph = S(200), S(230), S(372), S(92)
        else:                                                     # a little higher: the credits below / crédits dessous
            ly, lh, y, ph = S(186), S(200), S(339), S(84)
        hd.draw_logo(screen, logo, W / 2, ly, S(1000), lh, now, valign="middle")
        word = "PRESS START" if credits else "INSERT COIN"
        k = hd._pulse(now)
        t = hd.text(word, "stencil", S(62), tuple(int(c * k) for c in GOLD), glow=0.7)
        pill = self.pg.Surface((int(t["w"] + S(90)), ph), self.pg.SRCALPHA)
        self.pg.draw.rect(pill, (6, 6, 14, 170), pill.get_rect(), border_radius=ph // 2)
        screen.blit(pill, (int(W / 2 - pill.get_width() / 2), y - pill.get_height() // 2))
        hd.put(screen, t, W / 2, y, "center", "middle")
        if credits is not None:
            self._draw_credits(screen, credits, W / 2, S(421), now, 0.9)

    def _draw_credits(self, screen, credits, cx, cy, now, k=1.0):
        """The coin (€) and CRÉDITS 07, big and bright in a dark pill that stands out from the scenery; the coin and the
        number jump when a coin lands. / La pièce (€) et CRÉDITS 07, gros et clairs dans une pastille sombre ; ils sautent
        quand une pièce tombe dessus."""
        hd, S = self.hd, self.S
        bump = max(0.0, 1 - (now - self.coin_t) / 0.35)
        num = f"{int(credits):02d}"
        lsize, nsize = S(32 * k), S(48 * k)
        lab = hd.text(tr("CRÉDITS", "CREDITS"), "stencil", lsize, CREAM, glow=0)
        nw = hd.text_width(num, "stencil", nsize)
        ic = self.icons["coin"]
        if k != 1.0:
            key = ("coin", self.coin_symbol, k)
            if key not in self.pills:
                self.pills[key] = self.pg.transform.smoothscale(ic, (int(ic.get_width() * k), int(ic.get_height() * k)))
            ic = self.pills[key]
        cw = ic.get_width()
        ph = S(68 * k)
        pw = int(ph / 2 + cw / 2 + S(14 * k) + lab["w"] + S(16 * k) + nw + S(30 * k))
        x0, y0 = int(cx - pw / 2), int(cy - ph / 2)
        screen.blit(self._pill(pw, ph, int(round(bump * 6))), (x0, y0))
        icx = x0 + ph / 2
        self.coin_xy, self.coin_box = (icx, cy), (cx, y0)
        screen.blit(ic, (int(icx - ic.get_width() / 2), int(cy - ic.get_height() / 2 - bump * S(9 * k))))
        _, top, _, bottom, _ = hd._glyph("stencil", nsize, "0")
        base = cy + (bottom - top) / 2                            # label and number on one baseline / même ligne de pied
        x = icx + cw / 2 + S(14 * k)
        hd.put(screen, lab, x, base, "left", "bottom")
        x += lab["w"] + S(16 * k)
        hd.put_number(screen, num, "stencil", nsize, GOLD, x + nw / 2, cy, "center", "middle", scale=1 + 0.3 * bump, glow=0.45)

    def _pill(self, w, h, lv):
        """Dark pill with a gold edge, drawn smooth once per size; lv 0-6 lights the edge up.
        / Pastille sombre au bord doré, lisse, dessinée une fois par taille ; lv allume le bord."""
        key = (w, h, lv)
        p = self.pills.get(key)
        if p is None:
            if len(self.pills) > 40:
                self.pills.clear()
            ss = 3
            img = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            e = max(2, self.S(3)) * ss
            f = 0.6 + 0.4 * lv / 6
            d.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=h * ss // 2, fill=tuple(int(c * f) for c in GOLD) + (255,))
            d.rounded_rectangle([e, e, w * ss - 1 - e, h * ss - 1 - e], radius=h * ss // 2 - e, fill=(10, 12, 26, 226))
            p = self.pills[key] = self.hd._surf(img.resize((w, h), Image.LANCZOS))
        return p

    def _draw_center(self, screen, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        cx = W / 2
        h = hd.draw_logo(screen, logo, cx, S(14), S(540), S(116), now)
        y = S(14) + max(h, S(60)) + S(16)
        B = self.boss
        if B is not None and (B.get("minor") or B["down"] is not None or now - B["t0"] >= 2.4):   # the boss after its
            self._draw_boss(screen, B, cx, y, now)                    # WARNING, a machine at once / le boss, un engin
            y += S(70)
        elif B is not None:
            y += S(52)
        elif self.mission_shown is not None:
            t = hd.text(f"MISSION {int(self.mission_shown)}", "stencil", S(34), CREAM, glow=0.4)
            hd.put(screen, t, cx, y, "center")
            for d in (-1, 1):
                x = cx + d * (t["w"] / 2 + S(24))
                for j in range(3):
                    xx = x + d * j * S(12)
                    self.pg.draw.lines(screen, ACCENT["p1" if d < 0 else "p2"], False,
                                       [(xx - d * S(6), y + S(4)), (xx + d * S(2), y + S(17)), (xx - d * S(6), y + S(30))], max(2, S(4)))
            y += S(52)
        if self.time_v is not None:
            bw, bh = S(170), S(92)
            r = self.pg.Rect(int(cx - bw / 2), int(y), bw, bh)
            low = self.time_v <= 10
            pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
            self.pg.draw.rect(screen, (10, 12, 26), r, border_radius=S(16))
            edge = tuple(int(CREAM[i] * (1 - pulse) + RED[i] * pulse) for i in range(3)) if low else CREAM
            self.pg.draw.rect(screen, edge, r, max(2, S(3)), border_radius=S(16))
            hd.put(screen, hd.text(tr("TEMPS", "TIME"), "bold", S(17), GREY, glow=0), cx, y + S(10), "center")
            col = RED if low else GOLD
            hd.put_number(screen, str(int(self.time_v)), "stencil", S(56), col, cx, y + S(56), "center", "middle",
                          scale=1.0 + 0.12 * pulse)
        credits = _n(vals.get("credits"))
        if credits is not None:                                   # bottom edge with the panels' / en bas, comme les panneaux
            self._draw_credits(screen, credits, cx, S(14 + 418 - 34), now)

    def _draw_boss(self, screen, B, cx, y, now):
        """The boss's name and its life bar in the middle, under the logo: red, it empties as the boss takes hits, flashes
        white on a hit, and BOSS DESTROYED takes its place when it runs out. / Le nom du boss et sa barre de vie."""
        hd, S, pg = self.hd, self.S, self.pg
        k = now - B["t0"]
        minor = bool(B.get("minor"))
        if B["down"] is not None:
            if minor:                                                  # a machine down: its bar fades / sa barre s'efface
                a = max(0.0, 1 - (now - B["down"]) / 0.8)
                hd.put(screen, hd.text(tr("DÉTRUIT", "DESTROYED"), "stencil", S(30), (255, 200, 150), glow=0.5), cx, y + S(30), "center",
                       "middle", alpha=a)
                return
            a = max(0.0, 1 - (now - B["down"] - 1.5) / 1.5)
            hd.put(screen, hd.text(tr("BOSS DÉTRUIT", "BOSS DESTROYED"), "stencil", S(44), GOLD, glow=0.7), cx, y + S(30), "center", "middle",
                   scale=1 + 0.3 * max(0.0, 1 - (now - B["down"]) / 0.3), alpha=a)
            return
        name = B["name"] or "BOSS"
        blink = not minor and k < 2.4 and int(k * 6) % 2 == 0
        col = (200, 196, 180) if minor else (RED if blink else (255, 150, 130))
        hd.put(screen, hd.text(name, "stencil", hd.fit_size(name, "stencil", S(22 if minor else 30), S(560), S(16)), col, glow=0.2 if minor else 0.5),
               cx, y + S(8 if minor else 2), "center")
        bw, bh = (S(380), S(12)) if minor else (S(540), S(18))
        r = pg.Rect(int(cx - bw / 2), int(y + S(42)), bw, bh)
        pg.draw.rect(screen, (30, 10, 14), r, border_radius=S(6))
        frac = max(0.0, min(1.0, B["hp"] / max(1, B["top"])))
        hit = max(0.0, 1 - (now - B["hit_t"]) / 0.25)
        fill = pg.Rect(r.x + S(3), r.y + S(3), max(0, int((bw - S(6)) * frac)), bh - S(6))
        if fill.width:
            c = (255, 255, 230) if hit > 0.5 else ((255, 70, 50) if frac > 0.3 else (255, 150, 40))
            if minor:
                c = (255, 255, 230) if hit > 0.5 else (220, 170, 70)   # amber: not the boss / ambre : pas le boss
            pg.draw.rect(screen, c, fill, border_radius=S(4))
        pg.draw.rect(screen, (120, 110, 90) if minor else ((255, 120, 110) if blink else (150, 60, 60)), r, max(1, S(2)), border_radius=S(6))

    def _draw_panel(self, screen, side, vals, now):
        P = self.players[side]
        if P.shown <= 0.001:
            return
        hd, S, pg = self.hd, self.S, self.pg
        x0 = self.x0(side, P)
        hit = max(0.0, 1 - (now - P.hit_t) / 0.45)
        jx = int(math.sin(now * 90) * S(7) * hit) if hit else 0
        x0 += jx
        y0 = S(14)
        screen.blit(self.panels[side], (x0, y0))
        acc = ACCENT[side]
        playing = self.playing(P)
        # en-tête : J1 / J2, état, casques
        chip = pg.Rect(self.X(side, x0, 18, 84), y0 + S(10), S(84), S(48))
        pg.draw.rect(screen, acc, chip, border_radius=S(8))
        hd.put(screen, hd.text(tr("J1", "P1") if side == "p1" else tr("J2", "P2"), "stencil", S(36), (24, 14, 8), glow=0), chip.centerx, chip.centery,
               "center", "middle")
        if not playing and (P.over_t is None or now - P.over_t > 5.0):
            self._invite(screen, side, x0, vals, now)
            return
        name = self.soldier(side, vals)                                 # the soldier beside J1 / J2 (1.33, Seb)
        if name:
            lx = 114
            pic = self.portrait(name)
            if pic is not None:                                        # the owner's own picture of him / sa propre image
                screen.blit(pic, (self.X(side, x0, lx, 48), chip.centery - pic.get_height() // 2))
                lx += 58
            hd.put(screen, hd.text(name, "stencil", hd.fit_size(name, "stencil", S(34), S(230), S(18)), acc, glow=0.3),
                   self.X(side, x0, lx), chip.centery, "left" if side == "p1" else "right", "middle")
        lives = _n(self.get(vals, side, "lives"))
        if lives is not None:
            self._draw_lives(screen, side, P, x0, int(lives), now)
        # score qui défile
        score = _n(self.get(vals, side, "score"))
        if score is not None:
            if P.score_disp is None or score < P.score_disp:
                P.score_disp = score
            else:
                gap = score - P.score_disp
                P.score_disp = min(score, P.score_disp + max(1, int(gap * 0.18) + 1)) if gap else score
            pop = max(0.0, 1 - (now - P.score_t) / 0.22)
            # in the middle of the band between the line under J1 / J2 (panel y 72) and the card (184), Seb found it on the line
            # au milieu de la bande entre le trait sous J1 / J2 et la carte : il était collé au trait
            hd.put_number(screen, self._fmt(P.score_disp), "stencil", S(92), GOLD, self.X(side, x0, 28), y0 + S(128),
                          "left" if side == "p1" else "right", "middle", scale=1 + 0.12 * pop)
        elif side == "p2":
            hd.put(screen, hd.text(tr("SCORE À APPRENDRE", "SCORE NOT LEARNED YET"), "bold", S(24), GREY, glow=0), self.X(side, x0, 28), S(120), "right")
        self._draw_weapon(screen, side, P, x0, vals, now)
        self._draw_items(screen, side, P, x0, vals, now)
        if P.mode == 2:
            self._stamp(screen, x0, "CONTINUE ?", GOLD, now, P.join_t, pulse=True)
        elif P.over_t is not None and not playing:
            self._stamp(screen, x0, "GAME OVER", RED, now, P.over_t)
        if hit:
            red = pg.Surface((S(PW), S(PH))).convert()
            red.fill((int(100 * hit), 0, 0))
            screen.blit(red, (x0, y0), special_flags=pg.BLEND_RGB_ADD)
        join = max(0.0, 1 - (now - P.join_t) / 0.6)
        if join and P.shown >= 1.0:
            g = self.fx.sp.glow(S(300), acc, 10 * join, hot=0.2)
            screen.blit(g, (int(x0 + S(PW) / 2 - g.get_width() / 2), int(y0 + S(PH) / 2 - g.get_height() / 2)),
                        special_flags=pg.BLEND_RGB_ADD)

    def _invite(self, screen, side, x0, vals, now):
        hd, S = self.hd, self.S
        credits = _n(vals.get("credits"))
        word = tr("APPUIE SUR START", "PRESS START") if credits is None or credits > 0 else "INSERT COIN"
        k = hd._pulse(now)
        cx = x0 + S(PW) / 2
        hd.put(screen, hd.text(word, "stencil", S(46), tuple(int(c * k) for c in ACCENT[side])), cx, S(230), "center", "middle")
        hd.put(screen, hd.text(tr("POUR REJOINDRE LA PARTIE", "TO JOIN THE GAME"), "bold", S(22), GREY, glow=0), cx, S(290), "center", "middle")

    def _draw_lives(self, screen, side, P, x0, n, now):
        ic = self.icons["helmet"]
        S = self.S
        if n <= 0 and P.mode == 1 and now >= P.sync_until:             # plus de vie de réserve (pas pendant la mise en place)
            x, y = self._helmet_xy(side, 0, 1)
            k = 0.5 + 0.5 * math.sin(now * 8)
            self.hd.put(screen, self.hd.text(tr("DERNIÈRE VIE", "LAST LIFE"), "stencil", S(34), RED, glow=0.7),
                        x + (S(23) if side == "p1" else -S(23)), y, "right" if side == "p1" else "left", "middle", alpha=0.45 + 0.55 * k)
            return
        up = max(0.0, 1 - (now - P.up_t) / 0.4)
        if n > 5:
            x, y = self._helmet_xy(side, 0, n)
            screen.blit(ic, (int(x - ic.get_width() / 2), int(y - ic.get_height() / 2)))
            t = self.hd.text(f"×{n}", "stencil", S(40), CREAM)
            self.hd.put(screen, t, x + (-S(34) if side == "p1" else S(34)), y, "right" if side == "p1" else "left", "middle")
            return
        for i in range(n):
            x, y = self._helmet_xy(side, i, n)
            img = ic
            if up and i == (n - 1 if side == "p1" else 0):
                sz = int(ic.get_width() * (1 + 0.8 * up))
                img = self.pg.transform.smoothscale(ic, (sz, sz))
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))

    def _draw_weapon(self, screen, side, P, x0, vals, now):
        hd, S, pg = self.hd, self.S, self.pg
        if P.tank and (_n(self.get(vals, side, "vehicle")) or 0) > 0:
            self._draw_tank(screen, side, P, x0, vals, now)
            return
        code = _n(self.get(vals, side, "weapon"))
        if code is None:
            return
        name, kind = self.weapon(side, code)
        kind = kind or "gun"
        ammo = _n(self.get(vals, side, "ammo"))
        wt = now - P.weapon_t
        if wt < 0:                                                     # la caisse n'est pas encore arrivée
            return
        # icône de l'arme, côté intérieur, tournée vers le centre
        sx, sy = self._slot_xy(side)
        sx += x0 - self.x0(side, P)
        img = self.weapon_surf(kind, side)
        kick = max(0.0, 1 - (now - P.recoil_t) / 0.08) * S(6) * (-1 if side == "p1" else 1)
        pop = max(0.0, 1 - wt / 0.35)
        if pop:
            k = 1 + 0.35 * pop
            img = pg.transform.smoothscale(img, (int(img.get_width() * k), int(img.get_height() * k)))
        screen.blit(img, (int(sx + S(95) - img.get_width() / 2 + kick), int(sy + S(54) - img.get_height() / 2)))
        # nom de l'arme
        slide = max(0.0, 1 - wt / 0.3)
        nx = self.X(side, x0, 36) + (-1 if side == "p1" else 1) * S(60) * slide
        col = (255, 226, 170) if kind != "pistol" else CREAM
        size = hd.fit_size(name, "stencil", S(40), S(360), S(20))
        hd.put(screen, hd.text(name, "stencil", size, col, glow=0.35), nx, S(208), "left" if side == "p1" else "right")
        # munitions et jauge
        if kind == "pistol" or ammo is None:
            hd.put(screen, hd.text("∞", "black", S(52), GREY, glow=0), self.X(side, x0, 36), S(282),
                   "left" if side == "p1" else "right", "middle")
            hd.put(screen, hd.text(tr("MUNITIONS ILLIMITÉES", "UNLIMITED AMMO"), "bold", S(20), GREY, glow=0), self.X(side, x0, 100), S(282),
                   "left" if side == "p1" else "right", "middle")
            return
        frac = max(0.0, min(1.0, ammo / max(1, P.ammo_max)))
        P.gauge += (frac - P.gauge) * (0.25 if wt < 0.5 else 0.5)
        if wt < 0.45:
            P.gauge = min(frac, (wt / 0.45) * frac)
        segs, gw, gh = 16, S(250), S(28)
        gx = self.X(side, x0, 36, 250)
        gy = S(268)
        sw = gw / segs
        lit = P.gauge * segs
        low = frac < 0.25
        flash = max(0.0, 1 - (now - P.recoil_t) / 0.1)
        for i in range(segs):
            j = i if side == "p1" else segs - 1 - i
            r = pg.Rect(int(gx + j * sw + 2), gy, int(sw - 4), gh)
            if i < int(lit):
                c = (255, 80, 50) if low and int(now * 6) % 2 == 0 else (255, int(200 - 90 * i / segs), 70)
                if i == int(lit) - 1 and flash:
                    c = (255, 255, 230)
            elif i < lit:
                c = (150, 110, 50)
            else:
                c = (40, 42, 56)
            pg.draw.rect(screen, c, r, border_radius=S(3))
        ax, ay = self._ammo_xy(side)
        ax += x0 - self.x0(side, P)
        hd.put_number(screen, str(int(ammo)), "stencil", S(50), WHITE if not low else RED, ax, ay,
                      "right" if side == "p1" else "left", "middle", scale=1 + 0.1 * flash)

    def _draw_tank(self, screen, side, P, x0, vals, now):
        """The tank in the weapon card: its drawing, its energy in hits, its cannon shells. When it has no energy left it
        is about to blow up. / Le char dans la carte de l'arme : son dessin, son énergie en coups, ses obus."""
        hd, S, pg = self.hd, self.S, self.pg
        hp = _n(self.get(vals, side, "vehicle_hp"))
        shells = _n(self.get(vals, side, "vehicle_ammo"))
        tt = now - P.tank_t
        hit = max(0.0, 1 - (now - P.tank_hit_t) / 0.4)
        sx, sy = self._slot_xy(side)
        sx += x0 - self.x0(side, P)
        kind = P.ride or "tank"
        img = self.ride_surf(kind, side)
        pop = max(0.0, 1 - tt / 0.35)
        if pop:
            k = 1 + 0.35 * pop
            img = pg.transform.smoothscale(img, (int(img.get_width() * k), int(img.get_height() * k)))
        kick = max(0.0, 1 - (now - P.recoil_t) / 0.1) * S(8) * (-1 if side == "p1" else 1)
        jx = math.sin(now * 80) * S(5) * hit
        cx, cy = sx + S(95), sy + S(54)
        if self.ride_own.get(kind):                                    # the owner's picture: the middle of the frame
            cx, cy = cx + (S(FRAME_DX) if side == "p1" else -S(FRAME_DX)), cy + S(FRAME_DY)
        screen.blit(img, (int(cx - img.get_width() / 2 + kick + jx), int(cy - img.get_height() / 2)))
        slide = max(0.0, 1 - tt / 0.3)
        nx = self.X(side, x0, 36) + (-1 if side == "p1" else 1) * S(60) * slide
        name = tr(*VEHICLE_NAMES.get(kind, VEHICLE_NAMES["vehicle"]))
        hd.put(screen, hd.text(name, "stencil", hd.fit_size(name, "stencil", S(40), S(360), S(20)), (176, 232, 140), glow=0.35),
               nx, S(208), "left" if side == "p1" else "right")
        hits = None if hp is None else max(0, min(TANK_HITS, math.ceil(hp * TANK_HITS / 100.0 - 0.05)))
        gx, gw, gh, gy = self.X(side, x0, 36, 250), S(250), S(28), S(268)
        if hits is not None:
            sw = gw / TANK_HITS
            blink = int(now * 6) % 2 == 0
            col = {3: (110, 220, 90), 2: (240, 210, 70), 1: (255, 80, 50)}.get(hits, (255, 80, 50))
            for i in range(TANK_HITS):
                j = i if side == "p1" else TANK_HITS - 1 - i
                r = pg.Rect(int(gx + j * sw + 3), gy, int(sw - 6), gh)
                lit = i < hits
                c = col if lit else (40, 42, 56)
                if lit and hits == 1 and blink:
                    c = (150, 40, 30)
                if hit and i == hits:                                  # la case qui vient de partir / the one just lost
                    c = (255, 240, 220) if blink else (255, 90, 60)
                pg.draw.rect(screen, c, r, border_radius=S(4))
            if hits == 0:
                k = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(now * 10))
                hd.put(screen, hd.text(tr("ÉJECTE-TOI !", "BAIL OUT!"), "stencil", S(30), RED, glow=0.7), gx + gw / 2, gy + gh / 2,
                       "center", "middle", alpha=k)
        if shells is not None and shells <= 99:
            ax, ay = self._ammo_xy(side)
            ax += x0 - self.x0(side, P)
            flash = max(0.0, 1 - (now - P.recoil_t) / 0.1)
            hd.put_number(screen, str(int(shells)), "stencil", S(50), WHITE if shells > 0 else RED, ax, ay - S(6),
                          "right" if side == "p1" else "left", "middle", scale=1 + 0.12 * flash)
            hd.put(screen, hd.text(tr("OBUS", "SHELLS") if kind == "tank" else "MISSILES", "bold", S(16), GREY, glow=0), ax, ay + S(24),
                   "right" if side == "p1" else "left", "middle")

    def _tank_gauge_xy(self, side):
        x0 = self.x0(side, self.players[side])
        return self.X(side, x0, 36, 250) + self.S(125), self.S(282)

    def _draw_items(self, screen, side, P, x0, vals, now):
        hd, S, pg = self.hd, self.S, self.pg
        dx = x0 - self.x0(side, P)
        bombs = _n(self.get(vals, side, "bombs"))
        if bombs is not None:
            ic = self.icons["grenade"]
            shown = int(bombs) + P.flying
            n = min(shown, 10)
            add_t, add_n = P.bomb_add
            fall = max(0.0, 1 - (now - add_t) / 0.45)
            for i in range(n):
                x, y = self._bomb_xy(side, i)
                lift = 0
                if fall and i >= n - min(add_n, n):
                    lift = -fall * fall * S(80)
                screen.blit(ic, (int(x + dx - ic.get_width() / 2), int(y - ic.get_height() / 2 + lift)))
            if shown > 10:
                x, y = self._bomb_xy(side, 9)
                hd.put(screen, hd.text(f"+{shown - 10}", "stencil", S(30), CREAM), x + dx + (S(26) if side == "p1" else -S(26)), y,
                       "left" if side == "p1" else "right", "middle")
            if shown == 0:
                x, y = self._bomb_xy(side, 0)
                hd.put(screen, hd.text(tr("PLUS DE BOMBES", "NO BOMBS LEFT"), "bold", S(20), GREY, glow=0), x + dx, y,
                       "left" if side == "p1" else "right", "middle")
        pr = _n(self.get(vals, side, "prisoners"))
        if pr is not None:
            ic = self.icons["prisoner"]
            x, y = self._prisoner_xy(side)
            bump = max(0.0, 1 - (now - P.prison_t) / 0.4)
            img = ic if not bump else pg.transform.smoothscale(ic, (int(ic.get_width() * (1 + 0.5 * bump)),
                                                                    int(ic.get_height() * (1 + 0.5 * bump))))
            screen.blit(img, (int(x + dx - img.get_width() / 2), int(y - img.get_height() / 2 - bump * S(10))))
            hd.put_number(screen, f"×{int(pr)}", "stencil", S(40), CREAM, x + dx + (S(28) if side == "p1" else -S(28)), y,
                          "left" if side == "p1" else "right", "middle")

    def _stamp(self, screen, x0, text, color, now, t0, pulse=False):
        hd, S, pg = self.hd, self.S, self.pg
        k = min(1.0, (now - t0) / 0.18)
        scale = 2.2 - 1.2 * k
        t = hd.text(text, "stencil", hd.fit_size(text, "stencil", S(80), S(PW - 120), S(30)), color, glow=0.6)
        surf = pg.Surface((t["surf"].get_width() + S(40), t["surf"].get_height() + S(30)), pg.SRCALPHA)
        hd.put(surf, t, surf.get_width() / 2, surf.get_height() / 2, "center", "middle")
        shade = pg.Surface((S(PW) - S(40), S(170)), pg.SRCALPHA)
        shade.fill((0, 0, 0, 150))
        screen.blit(shade, (x0 + S(20), S(160)))
        if pulse:
            a = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(now * 6))
            surf.set_alpha(int(255 * a))
        rot = pg.transform.rotozoom(surf, 6, scale)
        screen.blit(rot, (int(x0 + S(PW) / 2 - rot.get_width() / 2), int(S(244) - rot.get_height() / 2)))

    def _draw_banner(self, screen, now):
        B = self.boss
        if B is not None and not B.get("minor") and B["down"] is None and now - B["t0"] < 2.4:   # WARNING: the boss comes
            hd, S, W = self.hd, self.S, self.W
            k = now - B["t0"]
            a = 1.0 if k < 2.0 else max(0.0, (2.4 - k) / 0.4)
            bar = self.pg.Surface((W, S(120))).convert()
            bar.fill((40, 0, 0))
            bar.set_alpha(int(170 * a))
            screen.blit(bar, (0, S(180)))
            on = int(k * 5) % 2 == 0
            self.pg.draw.line(screen, RED if on else (120, 30, 30), (0, S(180)), (W, S(180)), max(2, S(4)))
            self.pg.draw.line(screen, RED if on else (120, 30, 30), (0, S(299)), (W, S(299)), max(2, S(4)))
            scale = 2.0 - 1.0 * min(1.0, k / 0.18)
            hd.put(screen, hd.text("WARNING", "stencil", S(92), RED if on else (255, 120, 100), glow=0.8), W / 2, S(232), "center",
                   "middle", scale=scale, alpha=a)
            if B["name"]:
                hd.put(screen, hd.text(B["name"], "stencil", S(30), CREAM, glow=0.4), W / 2, S(284), "center", "middle", alpha=a)
            return
        k = now - self.complete_t
        if 0 <= k <= 1.9:                                              # MISSION COMPLETE
            hd, S, W = self.hd, self.S, self.W
            scale = 2.0 - 1.0 * min(1.0, k / 0.18)
            a = 1.0 if k < 1.6 else max(0.0, (1.9 - k) / 0.3)
            bar = self.pg.Surface((W, S(120))).convert()
            bar.fill((0, 0, 0))
            bar.set_alpha(int(170 * a))
            screen.blit(bar, (0, S(180)))
            hd.put(screen, hd.text("MISSION COMPLETE !", "stencil", S(88), GOLD, glow=0.8), W / 2, S(240), "center", "middle",
                   scale=scale, alpha=a)
            return
        if self.mission_shown is None:
            return
        k = now - self.mission_t
        if k > 2.4 or k < 0:
            return
        hd, S, W = self.hd, self.S, self.W
        if k < 0.35:
            x = W / 2 + (1 - k / 0.35) ** 2 * W * 0.6
        elif k < 2.0:
            x = W / 2
        else:
            x = W / 2 - ((k - 2.0) / 0.4) ** 2 * W * 0.6
        bar = self.pg.Surface((W, S(120))).convert()
        bar.fill((0, 0, 0))
        bar.set_alpha(150)
        screen.blit(bar, (0, S(180)))
        self.pg.draw.line(screen, GOLD, (0, S(180)), (W, S(180)), max(2, S(3)))
        self.pg.draw.line(screen, GOLD, (0, S(299)), (W, S(299)), max(2, S(3)))
        hd.put(screen, hd.text(f"MISSION {int(self.mission_shown)}", "stencil", S(92), GOLD, glow=0.7), x, S(240), "center", "middle")
