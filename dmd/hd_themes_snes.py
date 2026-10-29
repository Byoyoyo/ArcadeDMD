"""HD backdrops of the two Super Nintendo games (Super Mario World, A Link to the Past). They are not drawn after the
games: a bright platform world of our own (hills, sky, forest, cave, castle, haunted house, water, the map seen from
above) and a fantasy world of our own (fields, the dark land, dungeons, houses). Everything is drawn by the program,
no image comes from a game. The backdrops register in hd_bg.BUILDERS when this module is imported.

Décors HD des deux jeux Super Nintendo. Ils ne sont pas dessinés d'après les jeux : un monde de plateformes à nous
(collines, ciel, forêt, grotte, château, maison hantée, eau, la carte vue du ciel) et un monde de légende à nous
(prairies, la terre sombre, donjons, maisons). Tout est dessiné par le programme, aucune image tirée d'un jeu.
"""

import math
import random

from PIL import Image

from . import hd_bg
from .hd_bg import add_at, mix, radial, vgrad
from .hd_themes2 import _stars_sky, hook_embers
from .hd_themes3 import _Pic, _bushes, _canopy, _crowns, _cumulus, _fit, _rgba, _rock_isles, _trunks, _tufts

GROUND = 74            # top of the ground above the bottom of the screen (pixels at s = 1) / haut du sol


# ---------------------------------------------------------------------------- outils
def _hills(W, h, s, rng, tones, stripe, size=(220, 380), tall=(120, 210), n_stripes=5):
    """Big rounded hills with soft stripes, a darker rim. / Grosses collines rondes à rayures douces."""
    p = _Pic(W, h)
    x = rng.uniform(0, 100) * s
    while x < W:
        w, hh = rng.uniform(*size) * s / 2, rng.uniform(*tall) * s
        p.ellipse(x - w, h - hh, x + w, h + hh, _rgba(tones[0]), _rgba(tones[2]), 3 * s)
        p.ellipse(x - w * 0.82, h - hh * 0.94, x + w * 0.42, h + hh * 0.5, _rgba(tones[1]))
        for k in range(n_stripes):
            t = (k + 0.5) / n_stripes * 2 - 1
            sx = x + t * w * 0.72
            top = h - hh * math.sqrt(max(0.0, 1 - (t * 0.72) ** 2)) * 0.82
            p.ellipse(sx - 3.5 * s, top, sx + 3.5 * s, h, _rgba(stripe, 90))
        x += w * rng.uniform(1.25, 1.9)
    return p.done()


def _ground(W, s, rng, top, side, dark, dots, scallop=True, h=GROUND + 26):
    """The ground seen from the side: a band of grass with round edges, then the earth with pebbles.
    / Le sol de profil : une bande d'herbe aux bords ronds, puis la terre et ses cailloux."""
    hh = h * s
    gy = 26 * s
    p = _Pic(W, hh)
    p.poly([(0, gy), (W, gy), (W, hh), (0, hh)], _rgba(side))
    for _ in range(int(W / (16 * s))):
        x, y, r = rng.uniform(0, W), rng.uniform(gy + 24 * s, hh - 4 * s), rng.uniform(2.5, 5.5) * s
        p.ellipse(x - r * 1.4, y - r, x + r * 1.4, y + r, _rgba(rng.choice(dots)))
    p.poly([(0, gy - 3 * s), (W, gy - 3 * s), (W, gy + 12 * s), (0, gy + 12 * s)], _rgba(top[0]))
    if scallop:
        x = 0.0
        while x < W:
            r = 13 * s
            p.chord(x, gy + 12 * s - r, x + 2 * r, gy + 12 * s + r, 0, 180, _rgba(top[0]))
            x += 2 * r
    p.line([(0, gy - 2 * s), (W, gy - 2 * s)], _rgba(top[1]), 4 * s)
    p.line([(0, hh - 2 * s), (W, hh - 2 * s)], _rgba(dark), 4 * s)
    return p.done(), hh


def hook_bubbles(bd, screen, b, L, now, dt):
    """Bubbles rising in the water. / Des bulles qui montent dans l'eau."""
    st = bd.amb_state.setdefault("_bub", None)
    W, H, s = bd.W, bd.H, bd.s
    if st is None:
        st = bd.amb_state["_bub"] = [[bd.rng.uniform(0, W), bd.rng.uniform(0, H), bd.rng.uniform(0.3, 1.0), bd.rng.uniform(0, 6)]
                                     for _ in range(46)]
    pg = bd.pg
    for p in st:
        p[1] -= (30 + 70 * p[2]) * s * dt
        p[0] += math.sin(now * 2 + p[3]) * 14 * s * dt - bd.speed * 0.3 * p[2] * dt
        if p[1] < -12 or p[0] < -12:
            p[0], p[1] = bd.rng.uniform(0, W + 120 * s), H + 12
        r = max(2, int((3 + 6 * p[2]) * s))
        pg.draw.circle(screen, (170, 220, 255), (int(p[0]), int(p[1])), r, max(1, int(1.5 * s)))
        pg.draw.circle(screen, (235, 250, 255), (int(p[0] - r * 0.35), int(p[1] - r * 0.35)), max(1, r // 3))


def hook_rays(bd, screen, b, L, now, dt):
    """Light rays slowly swaying (water, forest). / Des rayons de lumière qui ondulent."""
    rays = b["amb"].get("rays")
    if not rays:
        return
    sp, add = bd.fx.sp, bd.pg.BLEND_RGB_ADD
    s = bd.s
    for i, (fx, col) in enumerate(rays):
        ang = 100 + 6 * math.sin(now * 0.4 + i * 1.7)
        ln = int(560 * s)
        g = sp.beam(ln, int(120 * s), col, ang, 3.5 + 1.5 * math.sin(now * 0.7 + i))
        cx = fx * bd.W + math.cos(math.radians(ang)) * ln / 2
        cy = -20 * s + math.sin(math.radians(ang)) * ln / 2
        screen.blit(g, (int(cx - g.get_width() / 2), int(cy - g.get_height() / 2)), special_flags=add)


# ---------------------------------------------------------------------------- the platform world / le monde des plateformes
LANDS = {
    #       sky stops, cloud tones, hills (tones, stripe), bushes, ground (top, side, dark, dots), extras
    "snes_hills": {"sky": [(0.0, (60, 140, 236)), (0.55, (120, 196, 250)), (1.0, (196, 236, 255))],
                   "clouds": ((255, 255, 255), (232, 242, 255), (184, 210, 240)),
                   "hills": (((96, 196, 92), (140, 224, 120), (40, 110, 52)), (220, 255, 200)),
                   "far": (((150, 210, 160), (176, 228, 180), (110, 170, 130)), (230, 255, 236)),
                   "bushes": ((30, 120, 48), (56, 168, 64), (130, 214, 96)),
                   "ground": (((90, 200, 70), (180, 250, 140)), (196, 128, 70), (120, 70, 34), [(176, 110, 60), (214, 150, 86)]),
                   "flowers": [(255, 110, 140), (255, 236, 96), (255, 255, 255)]},
    "snes_sky": {"sky": [(0.0, (70, 60, 170)), (0.45, (220, 120, 170)), (0.8, (255, 190, 140)), (1.0, (255, 226, 170))],
                 "clouds": ((255, 246, 240), (255, 214, 214), (210, 160, 190)),
                 "isles": True,
                 "ground": None},
    "snes_forest": {"sky": [(0.0, (16, 54, 46)), (0.5, (40, 96, 70)), (1.0, (90, 150, 96))],
                    "forest": True,
                    "bushes": ((16, 70, 34), (34, 110, 44), (86, 160, 70)),
                    "ground": (((60, 150, 56), (140, 210, 110)), (110, 76, 50), (60, 40, 26), [(90, 60, 40), (140, 100, 64)]),
                    "flowers": [(255, 190, 90), (210, 140, 255)]},
    # the fantasy world of the adventure game / le monde de légende du jeu d'aventure
    "z3_field": {"sky": [(0.0, (70, 150, 230)), (0.6, (150, 206, 245)), (1.0, (216, 240, 250))],
                 "clouds": ((255, 255, 255), (236, 244, 252), (196, 214, 236)),
                 "far": (((120, 170, 200), (150, 196, 220), (90, 130, 170)), (190, 220, 240)),
                 "castle": ((150, 170, 200), (110, 128, 160)),
                 "crowns": ((50, 130, 70), (76, 162, 84), (130, 204, 110)),
                 "bushes": ((40, 120, 52), (64, 160, 66), (140, 210, 100)),
                 "ground": (((100, 186, 70), (176, 236, 120)), (150, 120, 70), (90, 66, 40), [(130, 104, 60), (170, 140, 90)]),
                 "flowers": [(255, 120, 120), (255, 236, 120), (250, 250, 255)], "tall_grass": ((60, 150, 50), (150, 220, 90))},
    "z3_dark": {"sky": [(0.0, (40, 10, 40)), (0.5, (110, 36, 70)), (0.85, (190, 80, 70)), (1.0, (120, 50, 60))],
                "far": (((80, 40, 70), (100, 50, 84), (50, 24, 46)), (130, 70, 110)),
                "peak": True, "dead_trees": (40, 20, 34),
                "crowns": ((60, 40, 60), (80, 52, 76), (120, 80, 100)),
                "bushes": ((70, 50, 60), (96, 66, 76), (140, 96, 104)),
                "ground": (((110, 90, 70), (160, 130, 100)), (90, 60, 66), (50, 30, 40), [(110, 76, 80), (70, 46, 56)]),
                "flowers": None, "tall_grass": ((90, 70, 70), (150, 110, 100))},
}


def _castle_far(W, h, s, rng, tones):
    """A far castle on a hill, simple towers with pointed roofs (a castle of our own). / Un château au loin."""
    p = _Pic(W, h)
    for k in range(2):
        cx = W * (0.3 + 0.45 * k) + rng.uniform(-60, 60) * s
        base = h - rng.uniform(10, 30) * s
        p.chord(cx - 300 * s, base - 70 * s, cx + 300 * s, base + 70 * s, 180, 360, _rgba(tones[1]))
        body_w, body_h = rng.uniform(90, 130) * s, rng.uniform(60, 80) * s
        p.poly([(cx - body_w, base - 40 * s), (cx + body_w, base - 40 * s), (cx + body_w, base - 40 * s - body_h),
                (cx - body_w, base - 40 * s - body_h)], _rgba(tones[0]))
        for j in range(-2, 3):
            tx = cx + j * body_w * 0.48
            th = (90 if j == 0 else 60 + abs(j) * 6) * s
            tw = (16 if j == 0 else 12) * s
            top = base - 40 * s - body_h - th * 0.6
            p.poly([(tx - tw, base - 40 * s - body_h * 0.5), (tx + tw, base - 40 * s - body_h * 0.5), (tx + tw, top), (tx - tw, top)],
                   _rgba(tones[0]))
            p.poly([(tx - tw * 1.3, top), (tx + tw * 1.3, top), (tx, top - th * 0.55)], _rgba(tones[1]))
        for j in range(5):
            wx = cx - body_w * 0.7 + j * body_w * 0.35
            p.poly([(wx - 4 * s, base - 70 * s), (wx + 4 * s, base - 70 * s), (wx + 4 * s, base - 84 * s), (wx - 4 * s, base - 84 * s)],
                   _rgba(tones[1]))
    return p.done()


def _dead_trees(W, h, s, rng, col):
    """Bare twisted trees. / Arbres morts et tordus."""
    p = _Pic(W, h)
    x = rng.uniform(0, 120) * s
    while x < W:
        th = rng.uniform(150, 240) * s
        pts = [(x + math.sin(i * 0.9) * 8 * s, h - th * i / 6) for i in range(7)]
        p.line(pts, _rgba(col), 12 * s)
        for i in range(2, 7):
            bx, by = pts[i]
            d = rng.choice((-1, 1))
            ln = rng.uniform(30, 70) * s
            p.line([(bx, by), (bx + d * ln * 0.6, by - ln * 0.3), (bx + d * ln, by - ln * 0.7)], _rgba(col), 5 * s)
        x += rng.uniform(260, 420) * s
    return p.done()


def _peak(W, h, s, rng, col, glow):
    """A dark mountain far away, a glow at its top. / Une montagne sombre au loin, une lueur au sommet."""
    p = _Pic(W, h)
    for k in range(3):
        cx = W * (0.2 + 0.32 * k) + rng.uniform(-40, 40) * s
        hh = rng.uniform(180, 260) * s
        w = rng.uniform(220, 320) * s
        p.poly([(cx - w, h), (cx - w * 0.2, h - hh * 0.9), (cx, h - hh), (cx + w * 0.25, h - hh * 0.85), (cx + w, h)], _rgba(col))
        p.poly([(cx - w * 0.2, h - hh * 0.9), (cx, h - hh), (cx + w * 0.1, h - hh * 0.7), (cx - w * 0.3, h - hh * 0.6)],
               _rgba(mix(col, glow, 0.35)))
    return p.done()


def build_land(W, H, s, look, seed=0):
    """An outdoor world seen from the side: sky, clouds, far hills, trees, bushes, the ground. / Un monde de plein air."""
    pal = LANDS[look]
    rng = random.Random(seed or sum(map(ord, look)))
    sky = vgrad(W, H, pal["sky"])
    gtop = H - GROUND * s
    layers = []
    amb = {}
    if look == "z3_dark":
        tw = _stars_sky(sky, rng, 90, W, H, 0.45, 60, 140)
        amb["stars"] = [(x, y, sp_, ph) for x, y, sp_, ph in tw]
        add_at(sky, radial(int(520 * s), (120, 40, 60), 2.2), int(W * 0.7), int(H * 0.62))
        amb["fireflies"] = True
        amb["lightning"] = True
    else:
        add_at(sky, radial(int(480 * s), (90, 80, 40), 2.4), int(W * 0.78), int(70 * s))         # the sun's glow / la lueur du soleil
    if pal.get("clouds"):
        layers.append({"img": _cumulus(W, int(H * 0.62), s, rng, 7, pal["clouds"], 60 * s, 200 * s), "y": 0, "f": 0.03, "stage": "sky"})
    if pal.get("isles"):
        isles, iy = _rock_isles(W, s, rng, 170 * s, 3, (190, 140, 150), (140, 96, 120), (120, 190, 110), (180, 230, 150),
                                ((70, 140, 90), (100, 170, 110), (160, 210, 140)))
        layers.append({"img": isles, "y": iy, "f": 0.08, "stage": "sky"})
        layers.append({"img": _cumulus(W, int(H * 0.5), s, rng, 9, pal["clouds"], 120 * s, 210 * s, (90, 170)),
                       "y": int(H * 0.45), "f": 0.22, "stage": "mid"})
        floor = _cumulus(W, int(170 * s), s, rng, 16, ((255, 255, 255), (250, 230, 236), (220, 190, 210)), 60 * s, 110 * s, (60, 110))
        layers.append({"img": floor, "y": int(H - 150 * s), "f": 1.0, "stage": "near"})
        amb["dust"] = (255, 230, 200)
        _fit(layers)
        return {"sky": sky, "layers": layers, "tw": W, "amb": amb}
    if pal.get("peak"):
        layers.append({"img": _peak(W, int(H * 0.7), s, rng, (60, 26, 50), (255, 120, 90)), "y": int(H * 0.3) - int(40 * s), "f": 0.05,
                       "stage": "far", "lights": []})
    if pal.get("far"):
        tones, stripe = pal["far"]
        layers.append({"img": _hills(W, int(260 * s), s, rng, tones, stripe, (300, 520), (140, 230), 0), "y": int(gtop - 230 * s),
                       "f": 0.1, "stage": "far"})
    if pal.get("castle"):
        layers.append({"img": _castle_far(W, int(240 * s), s, rng, pal["castle"]), "y": int(gtop - 250 * s), "f": 0.14, "stage": "far"})
    if pal.get("hills"):
        tones, stripe = pal["hills"]
        layers.append({"img": _hills(W, int(250 * s), s, rng, tones, stripe), "y": int(gtop - 230 * s), "f": 0.3, "stage": "mid"})
    if pal.get("forest"):
        layers.append({"img": _crowns(W, int(H * 0.6), s, rng, 60 * s, ((24, 70, 50), (36, 96, 62), (70, 140, 90))), "y": int(H * 0.3),
                       "f": 0.12, "stage": "far"})
        layers.append({"img": _trunks(W, H, s, rng, int(gtop + 8 * s), ((150, 110, 76), (110, 78, 50), (64, 44, 30)),
                                      ((24, 80, 40), (44, 120, 50), (100, 170, 70)), ((36, 90, 40), (50, 130, 52), (100, 180, 76))),
                       "y": 0, "f": 0.45, "stage": "mid"})
        amb["fireflies"] = True
        amb["rays"] = [(0.2, (60, 90, 50)), (0.55, (70, 100, 60)), (0.85, (60, 90, 50))]
    if pal.get("crowns"):
        layers.append({"img": _crowns(W, int(200 * s), s, rng, 40 * s, pal["crowns"], (30, 60)), "y": int(gtop - 150 * s), "f": 0.25,
                       "stage": "mid"})
    if pal.get("dead_trees"):
        layers.append({"img": _dead_trees(W, int(260 * s), s, rng, pal["dead_trees"]), "y": int(gtop - 250 * s), "f": 0.4, "stage": "mid"})
    if pal.get("bushes"):
        layers.append({"img": _bushes(W, int(100 * s), s, rng, pal["bushes"], pal.get("flowers")), "y": int(gtop - 86 * s), "f": 0.6,
                       "stage": "mid"})
    top, side, dark, dots = pal["ground"]
    ground, gh = _ground(W, s, rng, top, side, dark, dots)
    if pal.get("tall_grass"):
        p = _Pic(W, gh)
        _tufts(p, W, 22 * s, s, rng, pal["tall_grass"], 1.6, gap=(30, 90))
        ground = Image.alpha_composite(ground, p.done())
    layers.append({"img": ground, "y": int(H - gh), "f": 1.0, "stage": "near"})
    if pal.get("forest"):
        layers.append({"img": _canopy(W, s, rng, ((14, 50, 26), (30, 90, 40), (70, 140, 60)), 200), "y": 0, "f": 1.1, "stage": "near"})
    hooks = {}
    if amb.get("rays"):
        hooks["sky"] = [hook_rays]
    if hooks:
        amb["hooks"] = hooks
    _fit(layers)
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


# ---------------------------------------------------------------------------- rooms: castle, ghost house, dungeon, house, cave
ROOMS = {
    "snes_castle": {"wall": ((70, 74, 96), (40, 42, 58)), "brick": (96, 100, 124), "mortar": (34, 34, 46), "bw": 64, "bh": 32,
                    "window": (255, 150, 60), "floor": ((110, 104, 120), (60, 56, 70)), "lava": True, "pillar": ((90, 92, 112), (52, 52, 66))},
    "snes_ghost": {"wall": ((44, 30, 66), (20, 14, 34)), "plank": (70, 50, 90), "mortar": (24, 16, 36), "bw": 46, "bh": 0,
                   "window": (180, 200, 255), "floor": ((90, 66, 60), (46, 32, 30)), "moon": True, "pillar": ((60, 44, 76), (30, 22, 40))},
    "snes_cave": {"wall": ((30, 40, 70), (12, 16, 30)), "rock": (52, 64, 100), "mortar": (16, 20, 36), "bw": 0, "bh": 0,
                  "window": (120, 220, 255), "floor": ((80, 88, 120), (36, 40, 60)), "stalactites": True, "crystals": True},
    "z3_dungeon": {"wall": ((50, 64, 80), (24, 30, 40)), "brick": (76, 92, 110), "mortar": (20, 26, 34), "bw": 96, "bh": 48,
                   "window": (255, 170, 70), "floor": ((92, 100, 110), (44, 48, 56)), "pillar": ((84, 98, 116), (44, 52, 64)), "torches": True},
    "z3_house": {"wall": ((120, 84, 56), (70, 46, 30)), "plank": (146, 104, 70), "mortar": (60, 38, 24), "bw": 54, "bh": 0,
                 "window": (255, 196, 110), "floor": ((150, 110, 70), (80, 56, 36)), "pillar": ((110, 74, 46), (64, 42, 26)), "lamps": True},
}


def build_room(W, H, s, look, seed=0):
    """An inside seen from the side: the far wall (bricks, planks or rock), windows or torches that flicker, pillars,
    the floor; lava for the castle, stalactites and crystals for the cave. / Un intérieur vu de profil."""
    pal = ROOMS[look]
    rng = random.Random(seed or sum(map(ord, look)))
    sky = vgrad(W, H, [(0.0, pal["wall"][0]), (1.0, pal["wall"][1])])
    gtop = H - GROUND * s
    layers, amb = [], {"window": pal["window"]}
    wall = _Pic(W, int(gtop + 4 * s))
    lights = []
    if pal.get("brick"):
        bw, bh = pal["bw"] * s, pal["bh"] * s
        y, row = 0.0, 0
        while y < gtop:
            x = -bw * 0.5 * (row % 2)
            while x < W:
                c = mix(pal["brick"], (0, 0, 0), rng.uniform(0.0, 0.25))
                wall.poly([(x + 2 * s, y + 2 * s), (x + bw - 2 * s, y + 2 * s), (x + bw - 2 * s, y + bh - 2 * s), (x + 2 * s, y + bh - 2 * s)],
                          _rgba(c, 120))
                x += bw
            y += bh
            row += 1
    if pal.get("plank"):
        x = 0.0
        while x < W:
            w = pal["bw"] * s * rng.uniform(0.8, 1.2)
            c = mix(pal["plank"], (0, 0, 0), rng.uniform(0.0, 0.3))
            wall.poly([(x, 0), (x + w - 3 * s, 0), (x + w - 3 * s, gtop), (x, gtop)], _rgba(c, 150))
            for k in range(rng.randint(1, 3)):
                ky = rng.uniform(0.1, 0.9) * gtop
                wall.ellipse(x + w * 0.3, ky, x + w * 0.5, ky + 10 * s, _rgba(mix(c, (0, 0, 0), 0.4), 160))
            x += w
    if pal.get("rock"):
        for _ in range(int(W / (40 * s))):
            x, y, r = rng.uniform(0, W), rng.uniform(0, gtop), rng.uniform(20, 60) * s
            wall.ellipse(x - r, y - r * 0.6, x + r, y + r * 0.6, _rgba(mix(pal["rock"], (0, 0, 0), rng.uniform(0, 0.4)), 110))
    # windows / fenêtres, torches
    n_win = 4
    for k in range(n_win):
        cx = (k + 0.5) * W / n_win + rng.uniform(-40, 40) * s
        if pal.get("brick") and not pal.get("torches"):
            top, bot, hw = 70 * s, 190 * s, 34 * s
            wall.poly([(cx - hw, bot), (cx + hw, bot), (cx + hw, top + hw), (cx - hw, top + hw)], (16, 12, 24, 255))
            wall.ellipse(cx - hw, top, cx + hw, top + 2 * hw, (16, 12, 24, 255))
            wall.line([(cx, top), (cx, bot)], _rgba(pal["mortar"]), 5 * s)
            wall.line([(cx - hw, top + 70 * s), (cx + hw, top + 70 * s)], _rgba(pal["mortar"]), 5 * s)
            lights.append((cx, bot + 30 * s))
        elif pal.get("moon"):
            top, bot, hw = 60 * s, 200 * s, 44 * s
            wall.poly([(cx - hw, top), (cx + hw, top), (cx + hw, bot), (cx - hw, bot)], (40, 50, 96, 255), (16, 10, 24, 255), 8 * s)
            wall.disc(cx + hw * 0.3, top + 40 * s, 20 * s, (236, 236, 210, 255))
            wall.line([(cx, top), (cx, bot)], (16, 10, 24, 255), 6 * s)
            wall.line([(cx - hw, (top + bot) / 2), (cx + hw, (top + bot) / 2)], (16, 10, 24, 255), 6 * s)
        elif pal.get("torches") or pal.get("lamps"):
            ty = 150 * s
            wall.poly([(cx - 8 * s, ty), (cx + 8 * s, ty), (cx + 5 * s, ty + 40 * s), (cx - 5 * s, ty + 40 * s)], (70, 50, 40, 255))
            wall.ellipse(cx - 14 * s, ty - 8 * s, cx + 14 * s, ty + 6 * s, (110, 80, 50, 255))
            wall.poly([(cx - 9 * s, ty - 4 * s), (cx + 9 * s, ty - 4 * s), (cx, ty - 34 * s)], (255, 190, 80, 255))
            wall.poly([(cx - 4 * s, ty - 4 * s), (cx + 4 * s, ty - 4 * s), (cx, ty - 20 * s)], (255, 246, 200, 255))
            lights.append((cx, ty - 16 * s))
    if pal.get("crystals"):
        for _ in range(9):
            cx, cy = rng.uniform(0, W), rng.uniform(gtop * 0.35, gtop - 10 * s)
            for j in range(3):
                a = math.radians(-90 + (j - 1) * 25)
                ln = rng.uniform(24, 46) * s
                tipx, tipy = cx + math.cos(a) * ln, cy + math.sin(a) * ln
                wall.poly([(cx - 6 * s, cy), (cx + 6 * s, cy), (tipx + 2 * s, tipy), (tipx - 2 * s, tipy)], (90, 200, 255, 230), (40, 90, 160, 255), 1.5 * s)
            lights.append((cx, cy - 20 * s))
    layers.append({"img": wall.done(), "y": 0, "f": 0.3, "stage": "far", "lights": lights})
    if pal.get("stalactites"):
        p = _Pic(W, int(150 * s))
        x = 0.0
        while x < W:
            w, hh = rng.uniform(20, 46) * s, rng.uniform(40, 140) * s
            p.poly([(x - w, 0), (x + w, 0), (x + w * 0.2, hh * 0.7), (x, hh), (x - w * 0.25, hh * 0.6)], _rgba(pal["rock"]), (14, 18, 34, 255), 2 * s)
            x += w * rng.uniform(1.4, 2.6)
        layers.append({"img": p.done(), "y": 0, "f": 0.6, "stage": "mid"})
        amb["dust"] = (150, 200, 255)
    if pal.get("pillar"):
        p = _Pic(W, int(gtop + 4 * s))
        light, dark = pal["pillar"]
        x = rng.uniform(100, 300) * s
        while x < W:
            w = 34 * s
            p.poly([(x - w, 0), (x + w, 0), (x + w, gtop), (x - w, gtop)], _rgba(light), (20, 20, 28, 255), 2 * s)
            p.poly([(x + w * 0.35, 0), (x + w, 0), (x + w, gtop), (x + w * 0.35, gtop)], _rgba(dark))
            p.poly([(x - w * 1.3, gtop - 26 * s), (x + w * 1.3, gtop - 26 * s), (x + w * 1.3, gtop), (x - w * 1.3, gtop)], _rgba(dark), (20, 20, 28, 255), 2 * s)
            p.poly([(x - w * 1.3, 0), (x + w * 1.3, 0), (x + w * 1.3, 26 * s), (x - w * 1.3, 26 * s)], _rgba(dark), (20, 20, 28, 255), 2 * s)
            x += rng.uniform(560, 760) * s
        layers.append({"img": p.done(), "y": 0, "f": 0.62, "stage": "mid"})
    # floor / le sol
    fh = int((GROUND + 26) * s)
    p = _Pic(W, fh)
    c0, c1 = pal["floor"]
    p.poly([(0, 26 * s), (W, 26 * s), (W, fh), (0, fh)], _rgba(c1))
    tile = 80 * s
    x = 0.0
    while x < W:
        p.poly([(x + 2 * s, 26 * s), (x + tile - 2 * s, 26 * s), (x + tile - 2 * s, 46 * s), (x + 2 * s, 46 * s)], _rgba(c0))
        x += tile
    p.line([(0, 27 * s), (W, 27 * s)], _rgba(mix(c0, (255, 255, 255), 0.3)), 3 * s)
    floor = p.done()
    if pal.get("lava"):
        lava = vgrad(W, int(44 * s), [(0, (255, 210, 90)), (0.3, (255, 120, 30)), (1.0, (140, 30, 10))], noise=4).convert("RGBA")
        floor.paste(lava, (0, fh - int(44 * s)))
        amb["hooks"] = {"front": [hook_embers]}
    layers.append({"img": floor, "y": int(H - fh), "f": 1.0, "stage": "near", "lights": []})
    _fit(layers)
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


# ---------------------------------------------------------------------------- under the water / sous l'eau
def build_water(W, H, s, seed=901):
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (40, 150, 220)), (0.5, (20, 90, 170)), (1.0, (10, 40, 90))])
    layers = []
    far = _Pic(W, int(H * 0.6))
    for _ in range(14):
        x, w, h = rng.uniform(0, W), rng.uniform(60, 160) * s, rng.uniform(80, 220) * s
        far.poly([(x - w, H * 0.6), (x - w * 0.3, H * 0.6 - h), (x + w * 0.4, H * 0.6 - h * 0.8), (x + w, H * 0.6)], (24, 70, 120, 255))
    layers.append({"img": far.done(), "y": int(H * 0.4), "f": 0.1, "stage": "far"})
    weeds = _Pic(W, int(260 * s))
    x = 0.0
    while x < W:
        h = rng.uniform(120, 250) * s
        col = rng.choice(((40, 160, 90), (60, 190, 110), (30, 130, 80)))
        pts = [(x + math.sin(i * 0.8 + x) * 12 * s, 260 * s - h * i / 10) for i in range(11)]
        weeds.line(pts, _rgba(col), 10 * s)
        x += rng.uniform(50, 130) * s
    layers.append({"img": weeds.done(), "y": int(H - 280 * s), "f": 0.5, "stage": "mid"})
    sand, gh = _ground(W, s, rng, ((236, 214, 150), (255, 240, 190)), (210, 180, 120), (150, 120, 80),
                       [(190, 160, 100), (230, 200, 140), (255, 160, 140)], scallop=False)
    layers.append({"img": sand, "y": int(H - gh), "f": 1.0, "stage": "near"})
    _fit(layers)
    amb = {"rays": [(0.15, (60, 120, 160)), (0.45, (70, 140, 170)), (0.75, (60, 120, 160))],
           "hooks": {"sky": [hook_rays], "front": [hook_bubbles]}}
    return {"sky": sky, "layers": layers, "tw": W, "amb": amb}


# ---------------------------------------------------------------------------- the map seen from above / la carte vue du ciel
MAP_LEVEL = 0.56       # height of the path of the map (part of the screen) / hauteur du chemin de la carte


def build_map(W, H, s, seed=911):
    """Islands seen from above on a blue sea, a dotted path from level to level. / Des îles vues du ciel."""
    rng = random.Random(seed)
    tw = W * 2
    sky = vgrad(W, H, [(0.0, (40, 110, 200)), (1.0, (30, 80, 170))])
    p = _Pic(tw, H, 2, tw)
    for _ in range(140):                                                 # the waves / les vagues
        x, y = rng.uniform(0, tw), rng.uniform(0, H)
        p.chord(x - 14 * s, y - 6 * s, x + 14 * s, y + 6 * s, 200, 340, (110, 170, 240, 200))
    y0 = H * MAP_LEVEL
    path = [(x, y0 + math.sin(x / tw * math.tau * 3) * 60 * s) for x in range(0, int(tw) + 40, 40)]
    for k in range(6):                                                   # islands along the path / des îles
        cx = (k + 0.5) * tw / 6
        cy = y0 + math.sin(cx / tw * math.tau * 3) * 60 * s
        rx, ry = rng.uniform(220, 300) * s, rng.uniform(150, 190) * s
        p.ellipse(cx - rx - 14 * s, cy - ry - 10 * s, cx + rx + 14 * s, cy + ry + 10 * s, (236, 214, 150, 255))
        col = rng.choice(((90, 190, 80), (120, 200, 90), (170, 190, 80), (200, 160, 90)))
        p.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, _rgba(col))
        for _ in range(9):                                               # small hills and trees / petites collines, arbres
            hx, hy = cx + rng.uniform(-rx * 0.8, rx * 0.8), cy + rng.uniform(-ry * 0.8, ry * 0.8)
            if abs(hy - cy) < 30 * s:
                continue
            if rng.random() < 0.5:
                p.chord(hx - 26 * s, hy - 22 * s, hx + 26 * s, hy + 22 * s, 180, 360, _rgba(mix(col, (40, 80, 30), 0.4)))
            else:
                p.poly([(hx - 3 * s, hy), (hx + 3 * s, hy), (hx + 3 * s, hy - 10 * s), (hx - 3 * s, hy - 10 * s)], (110, 70, 40, 255))
                p.disc(hx, hy - 18 * s, 13 * s, _rgba(mix(col, (20, 90, 30), 0.5)))
    for i in range(len(path) - 1):                                       # the dotted path / le chemin en pointillés
        if i % 2 == 0:
            p.line([path[i], path[i + 1]], (250, 236, 190, 255), 8 * s)
    for k in range(12):                                                  # the levels / les niveaux
        x = (k + 0.25) * tw / 12
        y = y0 + math.sin(x / tw * math.tau * 3) * 60 * s
        col = (255, 220, 60, 255) if k % 3 else (255, 80, 60, 255)
        p.disc(x, y, 17 * s, (60, 40, 30, 255))
        p.disc(x, y - 2 * s, 13 * s, col)
    layers = [{"img": p.done(), "y": 0, "f": 0.5, "stage": "near"}]
    clouds = _cumulus(W, int(H * 0.5), s, random.Random(seed + 1), 4, ((255, 255, 255), (236, 244, 255), (200, 220, 240)), 30 * s, 120 * s,
                      (50, 90))
    layers.append({"img": clouds, "y": 0, "f": 1.2, "stage": "near"})
    _fit(layers)
    return {"sky": sky, "layers": layers, "tw": tw, "amb": {}}


LAND_LOOKS = tuple(LANDS)
ROOM_LOOKS = tuple(ROOMS)
hd_bg.BUILDERS.update({name: (lambda W, H, s, n=name: build_land(W, H, s, n)) for name in LAND_LOOKS})
hd_bg.BUILDERS.update({name: (lambda W, H, s, n=name: build_room(W, H, s, n)) for name in ROOM_LOOKS})
hd_bg.BUILDERS.update({"snes_water": build_water, "snes_map": build_map})
SNES_THEMES = LAND_LOOKS + ROOM_LOOKS + ("snes_water", "snes_map")
