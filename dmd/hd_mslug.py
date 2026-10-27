"""Metal Slug HD scene: two soldier panels, an animated backdrop and an effect for every game event.

Ammo going down fires shots in the style of the weapon, bombs are thrown and explode in the backdrop, a weapon
pickup drops a crate, a lost life drops the helmet, rescued prisoners, coins, score, timer, next mission (new
backdrop), player joining, CONTINUE and GAME OVER. Missing values are simply hidden. All drawings are made by
the program, no image comes from the games.

Scène HD des Metal Slug : deux panneaux de soldat, décor animé, et un effet pour chaque événement du jeu.

Ce que fait chaque valeur lue dans la mémoire du jeu
- munitions qui baissent : tirs (flamme à la bouche du canon, traçantes vers le décor, douilles éjectées) ;
  le style suit l'arme (mitraillette, fusil à pompe, lance-roquettes, lance-flammes, laser) ;
- bombes qui baissent : la grenade quitte sa rangée, part en cloche et explose dans le décor ;
- arme qui change : la carte de l'arme s'illumine, la jauge se remplit ;
- vie perdue : le casque tombe, le panneau rougit et tremble ; vie gagnée : « 1UP » ;
- prisonniers libérés, crédits, score qui défile, chrono qui passe au rouge, mission suivante (changement de décor),
  arrivée d'un joueur, CONTINUE et GAME OVER.
Les valeurs absentes (pas encore trouvées pour un jeu) sont simplement cachées.

Dessins (casques, grenades, armes, décors) faits par le programme, aucune image tirée des jeux.
"""

import math
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
         "gun": ("ARME SPÉCIALE", "SPECIAL WEAPON")}
MS1 = {0: "pistol", 1: "shotgun", 2: "flame", 3: "rocket", 4: "mg"}
MS2 = {255: "pistol", 0: "shotgun", 1: "rocket", 2: "flame", 3: "mg", 4: "laser"}
WEAPON_MAPS = {"mslug": MS1, "mslug2": MS2, "mslugx": MS2}

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
TIP = {"pistol": (0.89, 0.385), "shotgun": (0.985, 0.395), "flame": (0.975, 0.45), "rocket": (0.99, 0.41),
       "mg": (0.975, 0.41), "laser": (0.97, 0.44), "gun": (0.975, 0.41)}
PORT = {"pistol": (0.45, 0.30), "shotgun": (0.32, 0.36), "mg": (0.30, 0.33), "gun": (0.30, 0.33)}

PW, PH = 640, 418           # taille d'un panneau, écran de référence 1920 x 460
BTN_RIGHT, BTN_LEFT, BTN_A = 0x08, 0x04, 0x10      # octet des commandes du BIOS Neo Geo (P1CURRENT)


def family(key):
    k = (key or "").lower()
    for name in ("mslugx", "mslug2", "mslug3", "mslug4", "mslug5", "mslug"):
        if k.startswith(name):
            return name
    return "mslug" if k.startswith("ms") else ""


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
        d.rounded_rectangle([W * 0.31, H * 0.28, W * 0.69, H * 0.66], radius=W * 0.08, fill=c)
        d.line([W * 0.42, H * 0.62, W * 0.33, H * 0.99], fill=c, width=lw)
        d.line([W * 0.58, H * 0.62, W * 0.67, H * 0.99], fill=c, width=lw)
        d.rectangle([W * 0.31, H * 0.44, W * 0.69, H * 0.50], fill=(150, 120, 80))
    return _draw(w, h, fn)


def coin_img(size):
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=(176, 120, 24))
        d.ellipse([W * 0.08, H * 0.08, W * 0.92, H * 0.92], fill=(246, 194, 64))
        d.ellipse([W * 0.2, H * 0.2, W * 0.8, H * 0.8], outline=(200, 142, 34), width=max(2, int(W * 0.05)))
        d.arc([W * 0.12, H * 0.12, W * 0.88, H * 0.88], 200, 290, fill=(255, 240, 170), width=max(2, int(W * 0.06)))
        pts = []
        for i in range(10):
            r = W * (0.2 if i % 2 == 0 else 0.09)
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((W / 2 + r * math.cos(a), H / 2 + r * math.sin(a)))
        d.polygon(pts, fill=(214, 150, 38))
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
            P([(0.0, 0.36), (0.16, 0.36), (0.16, 0.53), (0.04, 0.57), (0.0, 0.55)], GUN_D)
            R(0.03, 0.41, 0.12, 0.48, (20, 22, 28))
            R(0.16, 0.31, 0.44, 0.54, GUN, 0.03)
            R(0.16, 0.31, 0.44, 0.34, GUN_L)
            R(0.44, 0.35, 0.88, 0.47, GUN)
            R(0.44, 0.35, 0.88, 0.37, GUN_L)
            if kind == "mg":
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


# ---------------------------------------------------------------------------- la scène
class MetalSlugScene:
    FPS = 50
    SLIDE_EVERY = 9.0                   # écran d'attente : un décor toutes les 9 secondes

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
                      "prisoner": hd._surf(prisoner_img(int(34 * s), int(40 * s))), "coin": hd._surf(coin_img(int(34 * s)))}
        self.panels = {side: hd._surf(panel_img(side, s, ACCENT[side])) for side in ("p1", "p2")}
        self.weapons = {}
        sp = self.fx.sp
        for name, img in small_imgs(s).items():
            sp.register(name, img)
        sp.register("helmet", helmet_img(int(46 * s)))
        sp.register("grenade", grenade_img(int(24 * s), int(30 * s)))
        sp.register("coin", coin_img(int(40 * s)))
        self.warm = self._warm_list()

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
                 (tr("DERNIÈRE VIE", "LAST LIFE"), 34, RED, 0.7), ("CONTINUE ?", 80, GOLD, 0.6), ("GAME OVER", 80, RED, 0.6)]
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

    def weapon(self, side, code):
        m = WEAPON_MAPS.get(family(self.key), MS1)
        if code is None:
            return None, None
        kind = m.get(int(code))
        if kind is None:
            kind = "pistol" if int(code) in (0, 255) and family(self.key) not in WEAPON_MAPS else "gun"
        return tr(*NAMES[kind]), kind

    def weapon_surf(self, kind, side):
        key = (kind, side)
        s = self.weapons.get(key)
        if s is None:
            img = weapon_img(kind, self.S(190), self.S(108))
            if side == "p2":
                img = ImageOps.mirror(img)
            s = self.weapons[key] = self.hd._surf(img)
        return s

    def get(self, vals, side, base):
        return vals.get(base if side == "p1" else base + "_p2")

    # ------------------------------------------------------------ ce qui a changé depuis l'image précédente
    def update(self, eng, now):
        vals = eng.state.values
        key = (eng.state.meta.get("game") or "")
        if key != self.key:
            self.key = key
            self.players = {"p1": Player("p1"), "p2": Player("p2")}
            self.mission = self.mission_shown = None
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
        if m is not None and m != self.mission:
            theme = stages[(max(1, int(m)) - 1) % len(stages)]
            if self.mission is not None and m == self.mission + 1 and anyone:
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
        self.fx.update(now)

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
                P.sync_until = now + 0.8
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
        quiet = now < P.sync_until
        cur = {b: _n(self.get(vals, side, b)) for b in ("score", "lives", "bombs", "ammo", "weapon", "prisoners")}
        inp = _n(vals.get("p1_input" if side == "p1" else "p2_input"))
        old = P.seen
        P.seen = dict(cur, input=inp)
        if inp is not None:
            P.move = 1.0 if inp & BTN_RIGHT else (-1.0 if inp & BTN_LEFT else 0.0)
        if quiet or not old:
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
            if d < 0:
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
        pr, po = cur["prisoners"], old.get("prisoners")
        if pr is not None and po is not None and pr > po:
            P.prison_t = now
            x, y = self._prisoner_xy(side)
            self.fx.sparks(x, y, 18, GOLD, (200, 600), (200, 340), (0.3, 0.7), 500, "front", 3, 26)
            self.fx.glow(x, y, 10, 70, GOLD, 0.4)
            self.fx.text(tr("+1 PRISONNIER", "+1 PRISONER") if pr - po == 1 else tr(f"+{pr - po} PRISONNIERS", f"+{pr - po} PRISONERS"), x, y - self.S(40), CREAM, 34, life=1.3)
        if inp is not None and P.weapon_kind == "pistol":
            prev = old.get("input")
            if prev is not None and (inp & BTN_A) and not (prev & BTN_A):
                self._queue_shots(P, now, 1)

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
        x, y = self._bomb_xy(side, index)
        d = 1 if side == "p1" else -1
        tx = self.W / 2 + d * self.rng.uniform(-80, 220) * self.s
        ty = self.H * 0.74 + self.rng.uniform(-8, 26) * self.s
        P.bomb_t = self.fx.now
        self.fx.glow(x, y, 6, 40, GOLD, 0.25)
        self.fx.projectile("grenade", x, y, tx, ty, 0.62, 170, self._boom, spin=d * 620, kind="proj", trail=0.03)
        P.flying = max(0, P.flying - 1)

    def _boom(self, x, y):
        self.fx.explosion(x, y, 1.0)

    def _coin(self, now, n):
        self.coin_t = now
        cx, cy = self.W / 2, self.S(412)
        for i in range(min(3, n)):
            self.fx.later(i * 0.2, self._drop_coin, cx + (i - (min(3, n) - 1) / 2) * self.S(40), cy)

    def _drop_coin(self, x, y):
        p = self.fx.obj("coin", x, self.S(-30), 0, 200, gravity=1800, vrot=0, life=0.9, floor=y - self.S(30), bounce=0.3)
        p.on_end = (self._coin_ding, (x, y - self.S(30)))

    def _coin_ding(self, x, y):
        self.fx.glow(x, y, 10, 80, GOLD, 0.35)
        self.fx.sparks(x, y, 12, GOLD, (150, 450), (200, 340), (0.3, 0.6), 500, "front", 2, 18)
        self.fx.text(tr("+1 CRÉDIT", "+1 CREDIT"), x, y - self.S(40), GOLD, 34, life=1.1, rise=60)

    # ------------------------------------------------------------ positions (pour les effets)
    def _slot_xy(self, side):
        x0 = self.x0(side, self.players[side])
        return self.X(side, x0, PW - 222, 190), self.S(195)

    def _tip_xy(self, side, kind):
        sx, sy = self._slot_xy(side)
        tx, ty = TIP.get(kind or "gun", TIP["gun"])
        if side == "p2":
            tx = 1 - tx
        P = self.players[side]
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
        self.update(eng, now)
        vals = eng.state.values
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
        hd.draw_logo(screen, logo, W / 2, S(200), S(1000), S(230), now, valign="middle")
        credits = _n(vals.get("credits"))
        word = "PRESS START" if credits else "INSERT COIN"
        k = hd._pulse(now)
        t = hd.text(word, "stencil", S(62), tuple(int(c * k) for c in GOLD), glow=0.7)
        pill = self.pg.Surface((int(t["w"] + S(90)), S(92)), self.pg.SRCALPHA)
        self.pg.draw.rect(pill, (6, 6, 14, 170), pill.get_rect(), border_radius=S(46))
        screen.blit(pill, (int(W / 2 - pill.get_width() / 2), S(372) - pill.get_height() // 2))
        hd.put(screen, t, W / 2, S(372), "center", "middle")
        if credits is not None:
            hd.put(screen, hd.text(tr(f"CRÉDITS {int(credits):02d}", f"CREDITS {int(credits):02d}"), "bold", S(26), (214, 184, 132), glow=0),
                   W / 2, S(436), "center", "middle")

    def _draw_center(self, screen, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        cx = W / 2
        h = hd.draw_logo(screen, logo, cx, S(14), S(540), S(116), now)
        y = S(14) + max(h, S(60)) + S(16)
        if self.mission_shown is not None:
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
        if credits is not None:
            t = hd.text(tr(f"CRÉDITS {int(credits):02d}", f"CREDITS {int(credits):02d}"), "bold", S(26), (214, 184, 132), glow=0)
            ic = self.icons["coin"]
            total = ic.get_width() + S(10) + t["w"]
            x = cx - total / 2
            bump = max(0.0, 1 - (now - self.coin_t) / 0.3)
            screen.blit(ic, (int(x), int(S(424) - ic.get_height() / 2 - bump * S(8))))
            hd.put(screen, t, x + ic.get_width() + S(10), S(424), valign="middle", scale=1 + 0.25 * bump)

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
            hd.put_number(screen, self._fmt(P.score_disp), "stencil", S(92), GOLD, self.X(side, x0, 28), S(84),
                          "left" if side == "p1" else "right", scale=1 + 0.12 * pop)
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
        if n <= 0 and P.mode == 1:                                     # plus de vie de réserve
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
