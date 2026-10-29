"""HD scenes of the two Super Nintendo games under RetroArch (Super Mario World, A Link to the Past). The pictures are
our own: a little hero in a teal hood runs, jumps and grabs coins in a bright platform world, a young adventurer with
a red headband walks the fields and the dungeons of a fantasy world. Nothing is drawn after the games, no character,
no item and no logo of theirs. Both scenes follow the values read in the game's memory: the controller, the speed, the
jumps, the power, the coins, the hearts, the items used, the dungeons, and they show every event big, one at a time.

Scènes HD des deux jeux Super Nintendo sous RetroArch. Les images sont à nous : un petit héros à capuche turquoise
court, saute et attrape des pièces dans un monde de plateformes, un jeune aventurier au bandeau rouge parcourt les
prairies et les donjons d'un monde de légende. Rien n'est dessiné d'après les jeux. Les deux scènes suivent les valeurs
lues dans la mémoire du jeu (la manette, la vitesse, les sauts, les pièces, les cœurs, les objets, les donjons) et
montrent chaque événement en grand, un à la fois.
"""

import math

from .hd_fx import Particle
from .hd_games import AMBER, CREAM, GOLD, RED, WHITE, GameScene, _clamp, _mix, _n
from .hd_themes_snes import GROUND, MAP_LEVEL          # (and the backdrops into hd_bg.BUILDERS / et les décors)
from .i18n import tr

INK = (28, 24, 40)
GREEN = (80, 230, 110)
SKY = (110, 200, 255)
PINK = (255, 120, 170)
VIOLET = (190, 130, 255)
PAD_B, PAD_Y, PAD_SEL, PAD_START, PAD_UP, PAD_DOWN, PAD_LEFT, PAD_RIGHT = 0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01
PAD_A = 0x80


def _rgba(c, a=255):
    return tuple(int(v) for v in c[:3]) + (a,)


# ============================================================================ a puppet drawn with Pillow / une marionnette
def _capsule(d, p0, p1, w, fill, ol, olw):
    """A rounded limb from p0 to p1, with its outline. / Un membre arrondi, avec son contour."""
    for col, ww in ((ol, w + 2 * olw), (fill, w)):
        d.line([p0, p1], fill=col, width=max(1, int(ww)))
        r = ww / 2
        for (x, y) in (p0, p1):
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def puppet(d, W, H, st):
    """A little character seen from the side, facing right, feet at the bottom of the box: a big round head, a round
    body, short rounded limbs. st: the colors and the pose (angles of the limbs in degrees, 0 = straight down,
    90 = forward, 180 = straight up). / Un petit personnage de profil : grosse tête ronde, corps rond, membres courts."""
    k = H
    olw = max(1.0, k * 0.016)
    ol = _rgba(INK)
    lean = st.get("lean", 0.0)
    dy = st.get("crouch", 0.0) * k
    cx = W * 0.5
    hip_y, sh_y = k * 0.8 + dy, k * 0.61 + dy
    bx = cx + lean * k * 0.05
    hx, hy = cx + lean * k * 0.12, k * 0.31 + dy
    hr = k * 0.235
    arm, leg = k * 0.17, k * 0.165 - dy * 0.6
    aw, lw = k * 0.08, k * 0.095
    skin, tunic, boots = st["skin"], st["tunic"], st["boots"]
    dark = _mix(tunic, (0, 0, 0), 0.3)

    def end(base, ang, ln):
        a = math.radians(ang)
        return (base[0] + math.sin(a) * ln, base[1] + math.cos(a) * ln)

    def leg_(x, ang, col):
        hip = (x, hip_y)
        foot = end(hip, ang, leg)
        _capsule(d, hip, foot, lw, _rgba(col), ol, olw)
        d.ellipse([foot[0] - k * 0.05, foot[1] - k * 0.04, foot[0] + k * 0.085, foot[1] + k * 0.035], fill=_rgba(col), outline=ol,
                  width=max(1, int(olw)))

    def arm_(x, ang, col):
        sh = (x, sh_y)
        hand = end(sh, ang, arm)
        _capsule(d, sh, hand, aw, _rgba(col), ol, olw)
        r = k * 0.045
        d.ellipse([hand[0] - r, hand[1] - r, hand[0] + r, hand[1] + r], fill=_rgba(skin), outline=ol, width=max(1, int(olw)))
        return hand

    def sword_(hand):
        if not st.get("sword") or st.get("no_sword"):
            return
        a = math.radians(st.get("sword_ang", 40))
        blade = st["sword"][0]
        tip = end(hand, st.get("sword_ang", 40), k * 0.36)
        _capsule(d, hand, tip, k * 0.05, _rgba(blade), ol, olw)
        d.line([hand, end(hand, st.get("sword_ang", 40), k * 0.3)], fill=_rgba(_mix(blade, WHITE, 0.6)), width=max(1, int(k * 0.012)))
        gx, gy = math.cos(a) * k * 0.065, -math.sin(a) * k * 0.065
        _capsule(d, (hand[0] - gx, hand[1] - gy), (hand[0] + gx, hand[1] + gy), k * 0.035, (200, 150, 50, 255), ol, olw)

    if st.get("cape"):                                                   # the cape, behind / la cape, derrière
        cf = st.get("cape_fly", 0.0)
        top = (bx - k * 0.02, sh_y - k * 0.04)
        pts = [top, (bx - k * (0.24 + 0.3 * cf), sh_y + k * (0.26 - 0.2 * cf)), (bx - k * (0.12 + 0.26 * cf), sh_y + k * (0.34 - 0.12 * cf)),
               (bx + k * 0.06, sh_y + k * 0.12)]
        d.polygon(pts, fill=_rgba(st["cape"]), outline=ol)
    leg_(bx - k * 0.045, st.get("leg_b", -6), _mix(boots, (0, 0, 0), 0.25))
    arm_(bx - k * 0.05, st.get("arm_b", -10), _mix(tunic, (0, 0, 0), 0.25))
    # the body / le corps
    d.ellipse([bx - k * 0.15, sh_y - k * 0.07, bx + k * 0.15, hip_y + k * 0.06], fill=_rgba(tunic), outline=ol, width=max(1, int(olw)))
    d.chord([bx - k * 0.15, sh_y - k * 0.07, bx + k * 0.15, hip_y + k * 0.06], 20, 160, fill=_rgba(dark))
    d.line([(bx - k * 0.14, hip_y - k * 0.02), (bx + k * 0.14, hip_y - k * 0.02)], fill=_rgba(st.get("belt", dark)), width=max(2, int(k * 0.03)))
    if st.get("shield"):                                                 # a round shield on the back / un bouclier rond
        sc, rim = st["shield"]
        r = k * 0.13
        sx, sy = bx - k * 0.14, sh_y + k * 0.08
        d.ellipse([sx - r * 0.75, sy - r, sx + r * 0.75, sy + r], fill=_rgba(sc), outline=ol, width=max(1, int(olw)))
        d.ellipse([sx - r * 0.55, sy - r * 0.8, sx + r * 0.55, sy + r * 0.8], outline=_rgba(rim), width=max(1, int(k * 0.02)))
        star(d, sx, sy, r * 0.35, _rgba(rim))
    leg_(bx + k * 0.045, st.get("leg_f", 6), boots)
    raised = st.get("arm_f", 14) > 150
    if raised:                                                           # a raised arm goes behind the head / derrière la tête
        hand_f = arm_(bx + k * 0.06, st.get("arm_f", 14), tunic)
    # the head / la tête
    if st.get("hood"):
        hood = st["hood"]
        d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=_rgba(hood), outline=ol, width=max(1, int(olw)))
        for ex, ey in ((-0.55, -0.62), (0.15, -0.78)):                   # two little ears / deux petites oreilles
            x0, y0 = hx + ex * hr, hy + ey * hr
            d.polygon([(x0, y0 + hr * 0.1), (x0 + hr * 0.42, y0 - hr * 0.05), (x0 + hr * 0.12, y0 - hr * 0.62)], fill=_rgba(hood), outline=ol)
        d.ellipse([hx - hr * 0.35, hy - hr * 0.55, hx + hr * 0.92, hy + hr * 0.82], fill=_rgba(skin), outline=_rgba(_mix(hood, (0, 0, 0), 0.3)),
                  width=max(2, int(k * 0.02)))
    else:
        d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=_rgba(skin), outline=ol, width=max(1, int(olw)))
        hair = st["hair"]
        pts = [(hx + hr * 0.75, hy - hr * 0.55)]
        for j in range(6):                                               # spiky hair / des mèches en pointe
            a0 = math.radians(-60 - j * 32)
            a1 = math.radians(-60 - j * 32 - 16)
            pts.append((hx + math.cos(a1) * hr * 1.38, hy + math.sin(a1) * hr * 1.38))
            pts.append((hx + math.cos(a0 - math.radians(32)) * hr * 0.98, hy + math.sin(a0 - math.radians(32)) * hr * 0.98))
        pts += [(hx - hr * 0.6, hy + hr * 0.5), (hx - hr * 0.1, hy + hr * 0.05), (hx + hr * 0.3, hy - hr * 0.3)]
        d.polygon(pts, fill=_rgba(hair), outline=ol)
        d.polygon([(hx - hr * 0.98, hy - hr * 0.3), (hx + hr * 0.95, hy - hr * 0.42), (hx + hr * 0.97, hy - hr * 0.22), (hx - hr * 0.98, hy - hr * 0.08)],
                  fill=_rgba(st["band"]), outline=ol)
        tail = st.get("tail", 0.0)
        d.polygon([(hx - hr * 0.95, hy - hr * 0.25), (hx - hr * 1.65, hy - hr * (0.05 - tail)), (hx - hr * 1.55, hy + hr * (0.25 + tail)),
                   (hx - hr * 0.95, hy - hr * 0.05)], fill=_rgba(st["band"]), outline=ol)
        d.ellipse([hx - hr * 0.15, hy - hr * 0.05, hx + hr * 0.15, hy + hr * 0.3], fill=_rgba(_mix(skin, (0, 0, 0), 0.12)), outline=ol)
    if st.get("dead"):                                                   # eyes closed in an X / yeux en croix
        for ex in (0.3, 0.68):
            x0, y0 = hx + ex * hr, hy + hr * 0.05
            w0 = max(1, int(k * 0.018))
            d.line([(x0 - hr * 0.12, y0 - hr * 0.12), (x0 + hr * 0.12, y0 + hr * 0.12)], fill=ol, width=w0)
            d.line([(x0 - hr * 0.12, y0 + hr * 0.12), (x0 + hr * 0.12, y0 - hr * 0.12)], fill=ol, width=w0)
    else:
        for ex in (0.28, 0.66):
            d.ellipse([hx + (ex - 0.12) * hr, hy - hr * 0.22, hx + (ex + 0.12) * hr, hy + hr * 0.24], fill=(255, 255, 255, 255), outline=ol)
            d.ellipse([hx + (ex - 0.0) * hr, hy - hr * 0.08, hx + (ex + 0.1) * hr, hy + hr * 0.14], fill=ol)
        d.arc([hx + 0.3 * hr, hy + hr * 0.3, hx + 0.72 * hr, hy + hr * 0.58], 20, 160, fill=ol, width=max(1, int(k * 0.016)))
    if st.get("fire"):                                                   # embers on the fire outfit / braises
        for j in range(3):
            x0, y0 = hx - hr * (0.6 - j * 0.35), hy - hr * (1.25 + j * 0.12)
            d.ellipse([x0, y0, x0 + hr * 0.16, y0 + hr * 0.16], fill=(255, 190, 60, 255))
    if not raised:
        hand_f = arm_(bx + k * 0.06, st.get("arm_f", 14), tunic)
    sword_(hand_f)


# poses: angles of the limbs (0 down, 90 forward, 180 up) / angles des membres (0 en bas, 90 devant, 180 en haut)
RUN = ({"leg_b": -40, "leg_f": 45, "arm_b": 40, "arm_f": -35, "lean": 0.35}, {"leg_b": -12, "leg_f": 14, "arm_b": 12, "arm_f": -10, "lean": 0.3},
       {"leg_b": 45, "leg_f": -40, "arm_b": -35, "arm_f": 40, "lean": 0.35}, {"leg_b": 14, "leg_f": -12, "arm_b": -10, "arm_f": 12, "lean": 0.3})
POSES = {"stand": {"leg_b": -5, "leg_f": 6, "arm_b": -10, "arm_f": 14},
         "jump": {"leg_b": -35, "leg_f": 55, "arm_b": -140, "arm_f": 145, "lean": 0.15},
         "fall": {"leg_b": -18, "leg_f": 28, "arm_b": -110, "arm_f": 115, "lean": 0.05},
         "duck": {"leg_b": -75, "leg_f": 80, "arm_b": 30, "arm_f": 45, "crouch": 0.13, "lean": 0.2},
         "fly": {"leg_b": -40, "leg_f": -20, "arm_b": 160, "arm_f": 170, "lean": 0.2, "cape_fly": 1.0},
         "swim": {"leg_b": -45, "leg_f": -15, "arm_b": 120, "arm_f": 70, "lean": 0.3, "cape_fly": 0.6},
         "win": {"leg_b": -12, "leg_f": 12, "arm_b": -128, "arm_f": 128},
         "dead": {"leg_b": -18, "leg_f": 18, "arm_b": -125, "arm_f": 125, "dead": True, "no_sword": True},
         "swing0": {"leg_b": -20, "leg_f": 25, "arm_b": -20, "arm_f": 155, "sword_ang": 200, "lean": 0.0},
         "swing1": {"leg_b": -28, "leg_f": 35, "arm_b": -30, "arm_f": 95, "sword_ang": 95, "lean": 0.35},
         "hold": {"leg_b": -8, "leg_f": 8, "arm_b": -135, "arm_f": 135, "no_sword": True},
         "hurt": {"leg_b": -30, "leg_f": 22, "arm_b": -60, "arm_f": -45, "lean": -0.45},
         "dash": {"leg_b": -55, "leg_f": 50, "arm_b": 50, "arm_f": 75, "lean": 0.75, "sword_ang": 100}}

PIP_LOOK = {0: ((32, 196, 196), (255, 140, 40)), 1: ((32, 196, 196), (255, 140, 40)), 2: ((32, 196, 196), (255, 140, 40)),
            3: ((246, 246, 250), (230, 64, 44))}


def pip_draw(pose, power, frame=0, star=False):
    """The little hero of the platform world: a teal hood with two small ears, an orange tunic; a purple cape with the
    cape, white and red with the fire. / Le petit héros : capuche turquoise, tunique orange ; cape violette, ou blanc et rouge."""
    hood, tunic = PIP_LOOK.get(power, PIP_LOOK[1])
    st = {"skin": (255, 206, 160), "hood": hood, "tunic": tunic, "boots": (120, 72, 40), "belt": (90, 50, 30)}
    if star:
        st.update(hood=(255, 236, 90), tunic=(255, 250, 220))
    if power == 2:
        st["cape"] = (150, 70, 210)
    if power == 3:
        st["fire"] = True
    st.update(RUN[frame % 4] if pose == "run" else POSES.get(pose, POSES["stand"]))

    def fn(d, W, H):
        puppet(d, W, H, st)
    return fn


REN_TUNIC = {0: (60, 110, 220), 1: (150, 80, 210), 2: (200, 50, 60)}
REN_BLADE = {0: None, 1: ((210, 220, 235), None), 2: ((170, 220, 255), None), 3: ((255, 170, 90), None), 4: ((255, 220, 90), None)}
REN_SHIELD = {0: None, 1: ((150, 100, 60), (230, 200, 120)), 2: ((200, 70, 50), (255, 210, 120)), 3: ((190, 210, 230), (255, 255, 255))}


def ren_draw(pose, armor, sword, shield, frame=0):
    """The young adventurer of the fantasy world: dark hair, a red headband, a tunic blue, purple or crimson with the
    mail, a round shield, a sword whose blade shines more with each new one. / Le jeune aventurier du monde de légende."""
    st = {"skin": (255, 206, 160), "hood": None, "hair": (70, 44, 30), "band": (220, 40, 40), "tunic": REN_TUNIC.get(armor, REN_TUNIC[0]),
          "boots": (110, 70, 40), "belt": (120, 80, 40), "tail": math.sin(frame * 1.6) * 0.3}
    if REN_BLADE.get(sword):
        st["sword"] = REN_BLADE[sword]
    if REN_SHIELD.get(shield):
        st["shield"] = REN_SHIELD[shield]
    st.update(RUN[frame % 4] if pose == "run" else POSES.get(pose, POSES["stand"]))
    if pose in ("run", "stand", "hurt"):
        st.setdefault("sword_ang", 45)

    def fn(d, W, H):
        puppet(d, W, H, st)
    return fn


def bunny_draw(d, W, H):
    """A pink rabbit, the hero changed by the dark land. / Un lapin rose."""
    ol = _rgba(INK)
    k = H
    body = (255, 170, 200)
    d.ellipse([W * 0.25, k * 0.45, W * 0.8, k * 0.98], fill=_rgba(body), outline=ol, width=max(1, int(k * 0.03)))
    d.ellipse([W * 0.45, k * 0.22, W * 0.88, k * 0.58], fill=_rgba(body), outline=ol, width=max(1, int(k * 0.03)))
    for ex in (0.52, 0.68):
        d.ellipse([W * ex, k * 0.0, W * (ex + 0.12), k * 0.32], fill=_rgba(body), outline=ol, width=max(1, int(k * 0.025)))
    d.ellipse([W * 0.7, k * 0.33, W * 0.76, k * 0.4], fill=ol)
    d.ellipse([W * 0.18, k * 0.62, W * 0.32, k * 0.76], fill=(255, 255, 255, 255), outline=ol)


def coin_draw(d, W, H):
    d.ellipse([0, 0, W - 1, H - 1], fill=(255, 196, 40, 255), outline=(150, 90, 10, 255), width=max(1, W // 10))
    d.ellipse([W * 0.22, H * 0.18, W * 0.78, H * 0.82], outline=(255, 240, 150, 255), width=max(1, W // 14))
    d.rectangle([W * 0.44, H * 0.3, W * 0.56, H * 0.7], fill=(200, 130, 20, 255))
    d.ellipse([W * 0.2, H * 0.14, W * 0.42, H * 0.3], fill=(255, 255, 230, 255))


def medal_draw(d, W, H):
    """A big gold medal with a star (the big coins of a level). / Une grosse médaille d'or avec une étoile."""
    d.ellipse([0, 0, W - 1, H - 1], fill=(255, 190, 40, 255), outline=(150, 80, 10, 255), width=max(1, W // 12))
    star(d, W / 2, H / 2, W * 0.32, (255, 250, 210, 255))


def star(d, cx, cy, r, fill, outline=None):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=fill, outline=outline)


def star_draw(d, W, H):
    star(d, W / 2, H / 2 + H * 0.04, W * 0.48, (255, 230, 70, 255), (170, 110, 10, 255))


def item_draw(kind):
    """Our own pictures for the reserve item: a growth gem, a flame orb, a star, a feather. / Nos images pour l'objet en réserve."""
    def fn(d, W, H):
        if kind == 1:
            d.polygon([(W * 0.5, H * 0.05), (W * 0.92, H * 0.4), (W * 0.5, H * 0.95), (W * 0.08, H * 0.4)], fill=(255, 140, 40, 255),
                      outline=(130, 50, 10, 255))
            d.rectangle([W * 0.44, H * 0.28, W * 0.56, H * 0.66], fill=(255, 255, 255, 255))
            d.rectangle([W * 0.3, H * 0.42, W * 0.7, H * 0.52], fill=(255, 255, 255, 255))
        elif kind == 2:
            d.ellipse([W * 0.15, H * 0.3, W * 0.85, H * 0.95], fill=(255, 90, 30, 255), outline=(140, 30, 10, 255))
            d.polygon([(W * 0.2, H * 0.55), (W * 0.35, H * 0.05), (W * 0.5, H * 0.35), (W * 0.65, H * 0.0), (W * 0.8, H * 0.55)],
                      fill=(255, 200, 60, 255))
            d.ellipse([W * 0.35, H * 0.5, W * 0.65, H * 0.8], fill=(255, 245, 200, 255))
        elif kind == 3:
            star_draw(d, W, H)
        elif kind == 4:
            d.polygon([(W * 0.15, H * 0.95), (W * 0.35, H * 0.4), (W * 0.8, H * 0.05), (W * 0.65, H * 0.55)], fill=(210, 236, 255, 255),
                      outline=(70, 110, 170, 255))
            d.line([(W * 0.15, H * 0.95), (W * 0.75, H * 0.12)], fill=(70, 110, 170, 255), width=max(1, W // 16))
    return fn


def board_draw(d, W, H):
    """A hover board with a small jet (the mount of the hero). / Une planche volante à réacteur."""
    d.rounded_rectangle([0, H * 0.3, W - 1, H * 0.75], radius=int(H * 0.22), fill=(60, 200, 160, 255), outline=_rgba(INK), width=max(1, H // 8))
    d.rectangle([W * 0.1, H * 0.42, W * 0.9, H * 0.5], fill=(255, 255, 255, 255))
    d.rectangle([W * 0.0, H * 0.55, W * 0.14, H * 0.95], fill=(90, 90, 110, 255))


def heart_draw(fill, rim, half=False):
    def fn(d, W, H):
        pts = []
        for i in range(48):
            t = math.tau * i / 48
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((W / 2 + x / 34 * W, H * 0.45 + y / 34 * H))
        d.polygon(pts, fill=_rgba(rim))
        inner = [(W / 2 + (x - W / 2) * 0.8, H * 0.47 + (y - H * 0.45) * 0.8) for x, y in pts]
        if half:
            d.polygon(inner, fill=(40, 10, 16, 255))
            d.polygon([p for p in inner if p[0] <= W / 2 + 0.5] or inner, fill=_rgba(fill))
        else:
            d.polygon(inner, fill=_rgba(fill))
        if fill[0] > 120:
            d.ellipse([W * 0.25, H * 0.2, W * 0.4, H * 0.35], fill=(255, 230, 230, 255))
    return fn


def gem_draw(col):
    """A cut jewel: a flat top, its facets, a point at the bottom. / Un joyau taillé : le dessus plat, les facettes, une pointe."""
    def fn(d, W, H):
        d.polygon([(W * 0.22, H * 0.08), (W * 0.78, H * 0.08), (W, H * 0.36), (W * 0.5, H - 1), (0, H * 0.36)], fill=_rgba(col),
                  outline=_rgba(_mix(col, (0, 0, 0), 0.5)))
        d.polygon([(W * 0.22, H * 0.08), (W * 0.78, H * 0.08), (W * 0.66, H * 0.36), (W * 0.34, H * 0.36)], fill=_rgba(_mix(col, WHITE, 0.5)))
        d.line([(0, H * 0.36), (W, H * 0.36)], fill=_rgba(_mix(col, (0, 0, 0), 0.35)), width=max(1, W // 12))
        d.line([(W * 0.34, H * 0.36), (W * 0.5, H - 2)], fill=_rgba(_mix(col, WHITE, 0.25)), width=max(1, W // 14))
    return fn


def bomb_draw(d, W, H):
    d.ellipse([W * 0.08, H * 0.25, W * 0.92, H * 0.98], fill=(50, 70, 140, 255), outline=_rgba(INK), width=max(1, W // 12))
    d.ellipse([W * 0.25, H * 0.38, W * 0.42, H * 0.52], fill=(170, 190, 255, 255))
    d.line([(W * 0.55, H * 0.28), (W * 0.7, H * 0.08)], fill=(200, 170, 120, 255), width=max(2, W // 10))
    d.ellipse([W * 0.62, 0, W * 0.86, H * 0.2], fill=(255, 200, 60, 255))


def arrow_draw(d, W, H):
    d.line([(0, H * 0.5), (W * 0.85, H * 0.5)], fill=(200, 160, 100, 255), width=max(2, H // 5))
    d.polygon([(W, H * 0.5), (W * 0.72, H * 0.1), (W * 0.72, H * 0.9)], fill=(220, 230, 240, 255))
    d.polygon([(0, H * 0.5), (W * 0.15, H * 0.1), (W * 0.22, H * 0.5), (W * 0.15, H * 0.9)], fill=(240, 80, 70, 255))


def key_draw(d, W, H):
    d.ellipse([W * 0.15, 0, W * 0.85, H * 0.4], outline=(255, 210, 70, 255), width=max(2, W // 6))
    d.rectangle([W * 0.42, H * 0.36, W * 0.58, H], fill=(255, 210, 70, 255))
    d.rectangle([W * 0.58, H * 0.7, W * 0.85, H * 0.8], fill=(255, 210, 70, 255))


def boomerang_draw(d, W, H):
    d.polygon([(W * 0.1, H * 0.9), (W * 0.5, H * 0.1), (W * 0.9, H * 0.9), (W * 0.5, H * 0.45)], fill=(90, 150, 230, 255), outline=_rgba(INK))


def orb_draw(col):
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=_rgba(col), outline=_rgba(_mix(col, WHITE, 0.6)), width=max(1, W // 10))
        d.ellipse([W * 0.25, H * 0.2, W * 0.45, H * 0.4], fill=(255, 255, 255, 230))
    return fn


# ============================================================================ the platform game / le jeu de plateformes
TILESETS = {0: "snes_hills", 7: "snes_hills", 1: "snes_castle", 11: "snes_castle", 4: "snes_castle", 10: "snes_castle", 2: "snes_sky",
            6: "snes_sky", 8: "snes_sky", 3: "snes_cave", 9: "snes_cave", 14: "snes_cave", 5: "snes_ghost", 13: "snes_ghost",
            12: "snes_forest"}
POWER_WORDS = {0: ("PETIT", "SMALL"), 1: ("SUPER !", "SUPER!"), 2: ("CAPE !", "CAPE!"), 3: ("FEU !", "FIRE!")}
ITEM_WORDS = {1: ("CHAMPIGNON", "MUSHROOM"), 2: ("FLEUR DE FEU", "FIRE FLOWER"), 3: ("ÉTOILE", "STAR"), 4: ("PLUME", "FEATHER")}
SWITCHES = (("sw_green", (60, 220, 80), ("BLOCS VERTS !", "GREEN BLOCKS!")), ("sw_yellow", (255, 220, 40), ("BLOCS JAUNES !", "YELLOW BLOCKS!")),
            ("sw_blue", (60, 120, 255), ("BLOCS BLEUS !", "BLUE BLOCKS!")), ("sw_red", (255, 60, 50), ("BLOCS ROUGES !", "RED BLOCKS!")))


class PlatformScene(GameScene):
    """Super Mario World on the HD screen, drawn our own way: our little hero runs, jumps, spins, flies with his cape and
    rides a hover board, following the speed, the jumps and the controller read in the game. The coins fly to the
    counter, the big coins fill their five slots, the points pop up. The level's look (hills, cave, castle, ghost house,
    forest, sky, water) follows the game, the map is seen from above. Every event is a big banner: power up, star,
    midway gate, P-switch, hurry up, course clear, secret exit, a life lost, GAME OVER, TIME UP.
    / Super Mario World sur l'écran HD, à notre façon : notre petit héros suit la vitesse, les sauts et la manette du
    jeu. Le décor suit le niveau, la carte est vue du ciel. Chaque événement est un grand bandeau."""
    THEME = "snes_hills"
    FPS = 50
    SHADE = (90, 40)
    EXPLOSIONS = True
    PILLS = True
    BANNERS = GameScene.BANNERS + (("COURSE CLEAR!", GOLD), ("NIVEAU RÉUSSI !", GOLD))
    HERO = 150                                   # height of the big hero (pixels at s = 1) / hauteur du héros

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.bd.prebuild(["snes_map"])                    # the map comes right after the title / la carte vient juste après le titre
        self.world = self.THEME
        self.hx = self.W * 0.32                  # where the hero is on the screen / où est le héros
        self.hy = 0.0                            # height of his jump / hauteur du saut
        self.vy = 0.0
        self.base_y = None
        self.face = 1
        self.run_ph = 0.0
        self.cam = None
        self.scroll = 0.0
        self.auto_next = 0.0
        self.seen_move = -99.0
        self.dead_t = None
        self.pops_count = 0                      # (tests)
        self.coins_flown = 0                     # (tests)
        self.banners = []                        # banners shown, for the tests / bandeaux montrés (tests)
        self.water_t = None
        self.water_ready = False
        for name, fn, w, h in (("coin", coin_draw, 34, 40), ("medal", medal_draw, 46, 52), ("star", star_draw, 40, 40)):
            self.fx.sp.register("snes_" + name, self._pil(w, h, fn))

    def _pil(self, w, h, fn):
        from .hd_games import draw_img
        return draw_img(self.S(w), self.S(h), fn)

    # ------------------------------------------------------------ helpers
    def ground_y(self):
        return self.H - self.S(GROUND) + self.S(8)

    def part(self, vals):
        return _n(vals.get("part")) or 0

    def hero_img(self, pose, power, frame, star=False, flip=False):
        h = self.HERO * (0.72 if power == 0 else 1.0)
        return self.img(("pip", pose, power, frame % 4, star, flip), self.S(h * 0.82), self.S(h), pip_draw(pose, power, frame, star), ss=2,
                        flip=flip)

    def say(self, fr, en, color, now, dur=1.6, sub=None):
        text = tr(fr, en)
        self.banners = (self.banners + [text])[-30:]
        self.slam(text, color, now, dur, sub)

    def nobody(self, vals):
        return vals.get("p1_mode") is not None and vals.get("p1_mode") != 1

    # ------------------------------------------------------------ the backdrop of the level / le décor du niveau
    def always(self, vals, now):
        p = self.part(vals)
        want = self.world
        if p in (1, 2):
            want = "snes_map"
        elif p == 3:
            want = TILESETS.get(_n(vals.get("tileset")), "snes_hills")
            if not self.water_ready:                                     # ready before the first swim / prêt avant d'y plonger
                self.water_ready = True
                self.bd.prebuild(["snes_water"])
            swim = _n(vals.get("swimming")) or 0
            if swim:                                                     # under the water for a while / sous l'eau
                if self.water_t is None:
                    self.water_t = now
                if now - self.water_t > 1.0:
                    want = "snes_water"
            else:
                self.water_t = None
        elif self.nobody(vals):
            want = "snes_hills"
        if want != self.world:
            self.world = want
            self.bd.prebuild([want])
        if self.world != self.bd.theme and self.bd.warm(self.world):
            self.bd.set_theme(self.world, now, wipe=0 if self.bd.last is None else 1.0)

    def move(self, vals, now, idle):
        return 0.0

    # ------------------------------------------------------------ events / les événements
    def restart(self, vals, now):
        self.dead_t = None
        self.base_y = None

    def update(self, vals, now):
        ch = self.changed
        gy = self.ground_y()
        hero_top = gy - self.hy - self.S(self.HERO)
        c = ch(vals, "coins")
        if c and (c[1] > c[0] or c[1] == 0):
            for i in range(max(1, min(5, (c[1] - c[0]) if c[1] > c[0] else 1))):
                self.fx.later(i * 0.08, self._coin_fly, self.hx, hero_top)
        sc = ch(vals, "cur_score") or ch(vals, "score")
        if sc and sc[1] > sc[0]:
            gain = sc[1] - sc[0]
            self.pops_count += 1
            self.popup(f"+{gain}", self.hx + self.S(90), hero_top - self.S(10), GOLD if gain < 1000 else (255, 120, 60),
                       size=34 if gain < 1000 else 48, life=1.0)
            if gain >= 1000:
                self.fx.small_blast(self.hx + self.S(140), gy - self.S(80), 1.0, "front")
        lv = ch(vals, "lives")
        if lv and lv[1] == lv[0] + 1:
            self.popup(tr("1UP !", "1UP!"), self.hx, hero_top - self.S(30), GREEN, size=58, life=1.4)
            self.fx.sparks(self.hx, hero_top, 26, (120, 255, 140), (200, 700), (180, 360), (0.3, 0.8), 500)
        elif lv and lv[1] == 0 and lv[0] > 0:
            self.say("GAME OVER", "GAME OVER", RED, now, 3.0)
        pw = ch(vals, "power")
        if pw and _n(vals.get("dead")) != 1:
            if pw[1] > 0:
                fr, en = POWER_WORDS.get(pw[1], POWER_WORDS[1])
                self.say(fr, en, (255, 160, 50), now, 1.4)
                self.fx.glow(self.hx, gy - self.hy - self.S(70), 30, 180, (255, 220, 120), 0.6, "front")
                for k in range(12):
                    a = k * math.tau / 12
                    self.fx.sparks(self.hx + math.cos(a) * self.S(70), gy - self.hy - self.S(70) + math.sin(a) * self.S(70), 1,
                                   (255, 230, 120), (100, 300), (0, 360), (0.3, 0.6), 0)
            else:
                self.say("AÏE !", "OUCH!", (255, 90, 70), now, 1.0)
                self.fx.flash((255, 60, 40), 0.25, 0.25)
        st = ch(vals, "star")
        if st and st[0] == 0 and st[1] > 0:
            self.say("INVINCIBLE !", "STAR POWER!", (255, 230, 60), now, 1.5)
        yo = ch(vals, "yoshi")
        if yo and yo[1] and not yo[0]:
            self.say("YOSHI !", "YOSHI!", (90, 230, 110), now, 1.3)
            self.fx.smoke(self.hx, gy, 8, (14, 24), 2.2, (0.4, 0.8), (20, 60), 40, (220, 230, 240), 150, "front")
        dc = ch(vals, "dragon_coins")
        if dc and dc[1] == dc[0] + 1:
            self.say(f"PIÈCE DRAGON {dc[1]}/5", f"DRAGON COIN {dc[1]}/5", (255, 200, 40), now, 1.5)
            self._medal_fly(dc[1], now)
        for name, fr, en, col in (("midway", "MI-PARCOURS !", "MIDWAY!", PINK), ("p_switch", "BOUTON P !", "P-SWITCH!", (90, 140, 255)),
                                  ("p_silver", "BOUTON P !", "P-SWITCH!", (220, 226, 236)), ("bonus_game", "JEU BONUS !", "BONUS GAME!", GOLD)):
            v = ch(vals, name)
            if v and v[0] == 0 and v[1] > 0:
                self.say(fr, en, col, now, 1.5)
        tm = ch(vals, "time")
        if tm and tm[1] == 99 and tm[0] > 99 and self.part(vals) == 3:
            self.say("VITE !", "HURRY UP!", RED, now, 1.8)
        gl = ch(vals, "goal")
        if gl and gl[0] == 0 and gl[1] > 0:
            self.say("NIVEAU RÉUSSI !", "COURSE CLEAR!", GOLD, now, 2.6)
            for i in range(10):
                self.fx.later(0.15 + i * 0.22, self._firework)
        kh = ch(vals, "keyhole")
        if kh and kh[0] == 0 and kh[1] > 0:
            self.say("SORTIE SECRÈTE !", "SECRET EXIT!", (80, 220, 255), now, 2.6)
            self.fx.glow(self.W / 2, self.H / 2, 60, 520, (60, 160, 255), 1.4, "front", 0.9, 0.0)
        dd = ch(vals, "dead")
        if dd and dd[1] == 1:
            self.dead_t = now
            self.say("PERDU !", "TOO BAD!", RED, now, 2.0)
        elif dd and dd[1] == 0:
            self.dead_t = None
        for name, col, (fr, en) in SWITCHES:
            v = ch(vals, name)
            if v and v[0] == 0 and v[1] > 0:
                self.say(fr, en, col, now, 1.8)
                self.fx.flash(col, 0.3, 0.3)
        pt = ch(vals, "part")
        if pt and pt[1] == 4:
            if (_n(vals.get("lives")) or 0) > 0:
                self.say("TEMPS ÉCOULÉ", "TIME UP!", GOLD, now, 2.4)
        if pt and pt[1] == 2 and vals.get("world_name"):
            self.say(str(vals["world_name"]), str(vals["world_name"]), CREAM, now, 1.6)

    def _coin_fly(self, x, y):
        self.coins_flown += 1
        tx, ty = self.S(250), self.S(42)
        self.fx.projectile("snes_coin", x, y, tx, ty, 0.55, 90, self._coin_land, spin=0, trail=0)

    def _coin_land(self, x, y):
        self.fx.glow(x, y, 6, 40, (255, 230, 120), 0.25, "front")
        self.fx.sparks(x, y, 6, (255, 230, 120), (100, 300), (0, 360), (0.15, 0.35), 0)

    def _medal_fly(self, n, now):
        x0, y0 = self.hx, self.ground_y() - self.hy - self.S(self.HERO)
        tx, ty = self.S(60 + (n - 1) * 46), self.S(98)
        self.fx.projectile("snes_medal", x0, y0, tx, ty, 0.8, 140, self._coin_land, spin=0, trail=0)

    def _firework(self):
        rng = self.rng
        x, y = rng.uniform(0.15, 0.85) * self.W, rng.uniform(0.25, 0.55) * self.H
        col = rng.choice(((255, 90, 90), (90, 220, 255), (255, 230, 90), (140, 255, 140), (220, 120, 255)))
        self.fx.glow(x, y, 10, 90, col, 0.5, "front")
        self.fx.sparks(x, y, 30, col, (250, 700), (0, 360), (0.5, 1.0), 300)

    # ------------------------------------------------------------ the hero / le héros
    def _hero_state(self, vals, now):
        """Moves the hero from the values of the game, or by himself when they do not move (demo).
        / Le héros suit les valeurs du jeu, ou se débrouille seul quand elles ne bougent pas."""
        dt = self.dt
        W, S = self.W, self.S
        pos_x, cam_x = _n(vals.get("pos_x")), _n(vals.get("cam_x"))
        pos_y, in_air = _n(vals.get("pos_y")), _n(vals.get("in_air"))
        speed = _n(vals.get("speed_x")) or 0
        pos = (pos_x, cam_x, pos_y)
        if pos_x is not None and cam_x is not None and pos != getattr(self, "last_pos", None):
            if getattr(self, "last_pos", None) is not None:
                self.seen_move = now
            self.last_pos = pos
        real = now - self.seen_move < 3.0
        if real:
            sx = _clamp((pos_x - cam_x) / 256.0, 0.0, 1.0)
            target = W * 0.14 + sx * W * 0.72
            self.hx += (target - self.hx) * min(1.0, dt * 10)
            if self.cam is None:
                self.cam = float(cam_x)
            self.cam += (cam_x - self.cam) * min(1.0, dt * 10)
            self.bd.scroll = self.cam * W * 0.72 / 256.0
            if in_air == 0 or pos_y is None:
                self.base_y = pos_y
                self.hy += (0 - self.hy) * min(1.0, dt * 14)
            elif self.base_y is not None:
                self.hy += (_clamp((self.base_y - pos_y) * S(1.6), 0, S(260)) - self.hy) * min(1.0, dt * 12)
            facing = _n(vals.get("facing"))
            if facing is not None:
                self.face = 1 if facing else -1
            moving = abs(speed) > 2
            self.run_ph += dt * (4 + abs(speed) * 0.25) if moving else 0
            return moving, in_air not in (None, 0)
        # by himself: runs right, jumps now and then / tout seul : court, saute de temps en temps
        self.bd.scroll += S(260) * dt
        self.run_ph += dt * 9
        if now >= self.auto_next and self.hy <= 0:
            self.vy = S(900)
            self.auto_next = now + self.rng.uniform(1.2, 2.8)
        self.hy += self.vy * dt
        self.vy -= S(2600) * dt
        if self.hy <= 0:
            self.hy, self.vy = 0.0, 0.0
        self.hx += (W * 0.32 - self.hx) * min(1.0, dt * 2)
        self.face = 1
        return True, self.hy > 0

    def draw_hero(self, screen, vals, now):
        moving, air = self._hero_state(vals, now)
        power = int(_n(vals.get("power")) or 0)
        star = (_n(vals.get("star")) or 0) > 0
        gy = self.ground_y()
        pose, frame = "stand", 0
        if self.dead_t is not None:
            pose = "dead"
            k = now - self.dead_t
            self.hy = max(-self.S(300), self.S(420) * k - self.S(900) * k * k)
        elif _n(vals.get("flight")):
            pose = "fly"
        elif _n(vals.get("swimming")):
            pose = "swim"
        elif _n(vals.get("ducking")):
            pose = "duck"
        elif air:
            pose = "jump" if (_n(vals.get("speed_y")) or 0) < 0 or self.vy > 0 else "fall"
        elif moving:
            pose, frame = "run", int(self.run_ph) % 4
        if (_n(vals.get("goal")) or 0) > 0:
            pose = "win"
        img = self.hero_img(pose, power, frame, star and int(now * 12) % 2 == 0, flip=self.face < 0)
        spin = _n(vals.get("spin"))
        if spin and air:
            img = self.rotated(("pip_spin", pose, power), img, (now * 900) % 360, 15)
        elif pose in ("fly", "swim"):                                    # lying forward / allongé vers l'avant
            img = self.rotated(("pip_tilt", pose, power, self.face), img, (-55 if pose == "fly" else -35) * self.face, 5)
        x = self.hx - img.get_width() / 2
        y = gy - self.hy - img.get_height()
        riding = _n(vals.get("yoshi"))
        if riding:                                                       # on the hover board / sur la planche volante
            board = self.img(("board",), self.S(150), self.S(40), board_draw, flip=self.face < 0)
            by = gy - self.hy - self.S(34) + math.sin(now * 5) * self.S(4)
            g = self.fx.sp.glow(self.S(26), (120, 220, 255), 8)
            screen.blit(g, (int(self.hx - self.face * self.S(70) - g.get_width() / 2), int(by + self.S(20) - g.get_height() / 2)),
                        special_flags=self.pg.BLEND_RGB_ADD)
            screen.blit(board, (int(self.hx - board.get_width() / 2), int(by)))
            y = by - img.get_height() + self.S(10)
        hurt = (_n(vals.get("hurt")) or 0) > 0 and int(now * 16) % 2 == 0
        if not hurt:
            screen.blit(img, (int(x), int(y)))
        if star and int(now * 30) % 3 == 0:
            self.fx.sparks(self.hx, y + img.get_height() * 0.5, 2, (255, 240, 120), (60, 200), (0, 360), (0.2, 0.5), 0)
        if pose == "run" and self.rng.random() < 0.15:
            self.fx.smoke(self.hx - self.face * self.S(30), gy - self.S(4), 1, (6, 10), 2.0, (0.3, 0.5), (10, 30), 6, (240, 230, 210), 110,
                          "front")

    # ------------------------------------------------------------ the HUD / les informations
    def draw_hud(self, screen, eng, vals, logo, now):
        hd, S, W, H = self.hd, self.S, self.W, self.H
        p = self.part(vals)
        if p in (1, 2):
            self.draw_map(screen, vals, now)
        elif p != 4 or self.dead_t is not None:
            self.draw_hero(screen, vals, now)
        hd.draw_logo(screen, logo, W / 2, S(8), S(520), S(92), now)
        # lives and coins / vies et pièces
        head = self.img(("pip_head",), S(58), S(58), lambda d, w, h: pip_draw("stand", 1)(d, w * 1.0, h * 1.9), ss=2)
        self.pill(screen, S(14), S(6), S(330), S(64), 140)
        screen.blit(head, (S(28), S(12)))
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.text(screen, f"× {int(lives)}", S(92), S(18), 40, WHITE)
        coin = self.img(("coin_icon",), S(30), S(36), coin_draw)
        screen.blit(coin, (S(196), S(20)))
        coins = _n(vals.get("coins"))
        if coins is not None:
            self.text(screen, f"× {int(coins)}", S(234), S(18), 40, (255, 220, 90))
        if p == 3 or p == 0:
            n = int(_n(vals.get("dragon_coins")) or 0)
            for i in range(5):
                x, y = S(60 + i * 46), S(98)
                if i < n:
                    m = self.img(("medal_icon",), S(36), S(40), medal_draw)
                    screen.blit(m, (x - m.get_width() // 2, y - m.get_height() // 2))
                else:
                    self.pg.draw.circle(screen, (60, 50, 30), (int(x), int(y)), S(15), max(2, S(3)))
        # score and time / score et temps
        sc = _n(vals.get("cur_score"))
        if sc is None:
            sc = _n(vals.get("score"))
        if sc is not None:
            w = hd.text(str(int(sc)), "black", S(62), AMBER)["w"]
            self.pill(screen, W - S(40) - w - S(30), S(6), w + S(60), S(70), 140)
            hd.put_number(screen, str(int(sc)), "black", S(62), AMBER, W - S(40), S(14), "right")
        tm = _n(vals.get("time"))
        if tm is not None and p == 3:
            low = tm <= 99
            col = RED if low and int(now * 3) % 2 == 0 else (WHITE if not low else (255, 160, 140))
            self.label(screen, f"{tr('TEMPS', 'TIME')} {int(tm)}", W - S(40), S(108), 34, col, align="right")
        # the reserve item / l'objet en réserve
        it = int(_n(vals.get("item_box")) or 0)
        bx, by, bs = W / 2 + S(330), S(14), S(76)
        if p == 3:
            self.box(screen, bx, by, bs, bs, (255, 255, 255), fill=(10, 14, 30, 190), radius=14, width=4)
            if it in (1, 2, 3, 4):
                ic = self.img(("item", it), S(52), S(52), item_draw(it))
                screen.blit(ic, (int(bx + bs / 2 - ic.get_width() / 2), int(by + bs / 2 - ic.get_height() / 2)))
                fr, en = ITEM_WORDS[it]
                self.text(screen, tr(fr, en), bx + bs + S(14), by + S(26), 24, CREAM, key="xbold")
        # the power and the bonus stars / la puissance et les étoiles bonus
        if p == 3:
            pw = int(_n(vals.get("power")) or 0)
            if pw:
                fr, en = POWER_WORDS[pw]
                self.label(screen, tr(fr, en).rstrip(" !"), S(30), H - S(40), 30, (255, 170, 70))
            stars = _n(vals.get("cur_stars"))
            if stars:
                st_img = self.img(("star_icon",), S(34), S(34), star_draw)
                w = self.label(screen, f"{int(stars)}", W - S(30), H - S(40), 30, (255, 230, 90), align="right")
                screen.blit(st_img, (int(W - S(30) - w - S(42)), int(H - S(40) - st_img.get_height() / 2)))
            for name, col, fr in (("p_switch", (80, 130, 255), 176), ("star", (255, 230, 80), 255)):
                v = _n(vals.get(name)) or 0
                if v > 0:
                    self.bar(screen, W * 0.3, H - S(22), W * 0.4, S(12), v / fr, col)
                    break
        if (_n(vals.get("pause")) or 0) and p == 3:
            self.label(screen, "PAUSE", W / 2, H / 2, 70, GOLD, key="stencil", align="center", alpha=200)
        if p == 4 and (_n(vals.get("lives")) or 0) == 0 and self.banner is None:
            self.label(screen, "GAME OVER", W / 2, S(250), 80, RED, key="stencil", align="center", alpha=200)

    def draw_map(self, screen, vals, now):
        """The map seen from above: the hero walks along the path, the name of the world, the exits found, the switch
        palaces pressed. / La carte vue du ciel : le héros marche sur le chemin, le nom du monde, les sorties."""
        S, W, H = self.S, self.W, self.H
        self.bd.scroll += S(40) * self.dt
        x = W * 0.42
        y = H * MAP_LEVEL + math.sin((self.bd.scroll * 0.5 + x) / (W * 2) * math.tau * 3) * S(60)
        img = self.img(("pip_map", int(now * 6) % 4), S(70), S(86), pip_draw("run", 1, int(now * 6) % 4), ss=2)
        screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() + S(10))))
        name = vals.get("world_name")
        if name:
            self.label(screen, str(name), W / 2, H - S(46), 44, GOLD, key="black", align="center", alpha=170)
        ex = _n(vals.get("exits"))
        if ex is not None:
            self.label(screen, f"{tr('SORTIES', 'EXITS')} {int(ex)}", S(30), H - S(40), 30, CREAM)
        for i, (name, col, _) in enumerate(SWITCHES):
            on = (_n(vals.get(name)) or 0) > 0
            bx, by = W - S(60) - (3 - i) * S(56), H - S(64)
            self.pg.draw.rect(screen, col if on else _mix(col, (0, 0, 0), 0.7), (int(bx), int(by), S(44), S(44)), border_radius=S(8))
            self.pg.draw.rect(screen, WHITE if on else (60, 60, 70), (int(bx), int(by), S(44), S(44)), max(2, S(3)), border_radius=S(8))

    def draw_attract(self, screen, eng, vals, logo, now):
        """Nobody plays (title, file select): the logo, PRESS START, the hero on the hills. / Personne ne joue."""
        hd, S, W = self.hd, self.S, self.W
        self.bd.scroll += S(70) * self.dt
        hd.draw_logo(screen, logo, W / 2, S(170), S(1000), S(220), now, valign="middle")
        k = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(now * 5))
        self.label(screen, tr("APPUIE SUR START", "PRESS START"), W / 2, S(372), 48, tuple(int(c * k) for c in AMBER), align="center")
        img = self.hero_img("run", 1, int(now * 8) % 4)
        screen.blit(img, (int(W * 0.12), int(self.ground_y() - img.get_height())))


# ============================================================================ the adventure game / le jeu d'aventure
DUNGEON_THEME = "z3_dungeon"
ITEM_FX = {1: "bow", 2: "boomerang", 3: "hookshot", 4: "bomb", 5: "powder", 6: "fire", 7: "ice", 11: "lamp", 12: "hammer", 13: "flute",
           14: "net", 15: "book", 17: "somaria", 18: "byrna", 19: "cape", 20: "mirror"}


class AdventureScene(GameScene):
    """A Link to the Past on the HD screen, drawn our own way: our young adventurer walks where the hero of the game
    walks, swings his sword, spins, dashes, swims, holds up what he finds; the bombs blow up, the arrows fly, the rods
    shoot fire or ice, the medallions shake the whole screen. The hearts, the magic, the rupees and the progress of the
    quest are at the top; the backdrop follows the world (light, dark), the dungeons and the houses.
    / A Link to the Past sur l'écran HD, à notre façon : notre jeune aventurier marche, frappe, tourbillonne, court,
    nage, brandit ce qu'il trouve ; les bombes explosent, les flèches volent, les médaillons secouent tout l'écran."""
    THEME = "z3_field"
    FPS = 50
    SHADE = (90, 40)
    EXPLOSIONS = True
    PILLS = True
    BANNERS = GameScene.BANNERS + (("VICTOIRE !", GOLD), ("VICTORY!", GOLD))
    HERO = 170

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.world = self.THEME
        self.hx = self.W * 0.4
        self.face = 1
        self.walk_ph = 0.0
        self.last_move = -99.0
        self.swing_t = -99.0
        self.hurt_t = -99.0
        self.hold_t = None
        self.dead_t = None
        self.bombs_out = 0                        # (tests)
        self.arrows_out = 0                       # (tests)
        self.banners = []
        for name, fn, w, h in (("bomb", bomb_draw, 44, 48), ("arrow", arrow_draw, 70, 16), ("rupee_g", gem_draw((60, 220, 90)), 22, 34),
                               ("rupee_b", gem_draw((70, 130, 255)), 22, 34), ("rupee_r", gem_draw((255, 70, 70)), 22, 34),
                               ("boomerang", boomerang_draw, 40, 40), ("fireball", orb_draw((255, 120, 40)), 40, 40),
                               ("iceball", orb_draw((150, 220, 255)), 40, 40), ("heart", heart_draw((240, 40, 50), (120, 10, 20)), 50, 46)):
            self.fx.sp.register("z3_" + name, self._pil(w, h, fn))

    def _pil(self, w, h, fn):
        from .hd_games import draw_img
        return draw_img(self.S(w), self.S(h), fn)

    def ground_y(self):
        return self.H - self.S(GROUND) + self.S(8)

    def nobody(self, vals):
        return vals.get("p1_mode") is not None and vals.get("p1_mode") != 1

    def say(self, fr, en, color, now, dur=1.8, sub=None):
        text = tr(fr, en)
        self.banners = (self.banners + [text])[-30:]
        self.slam(text, color, now, dur, sub)

    def hero_img(self, pose, vals, frame=0, flip=False):
        armor, sword, shield = (int(_n(vals.get(k)) or 0) for k in ("armor", "sword", "shield"))
        return self.img(("ren", pose, armor, sword, shield, frame % 4, flip), self.S(self.HERO * 0.9), self.S(self.HERO),
                        ren_draw(pose, armor, sword, shield, frame), ss=2, flip=flip)

    def always(self, vals, now):
        palace = _n(vals.get("palace"))
        if self.nobody(vals):
            want = "z3_field"
        elif palace is not None and palace != 255:
            want = DUNGEON_THEME
        elif _n(vals.get("indoors")):
            want = "z3_house"
        elif _n(vals.get("dark")):
            want = "z3_dark"
        else:
            want = "z3_field"
        if want != self.world:
            self.world = want
            self.bd.prebuild([want])
        if self.world != self.bd.theme and self.bd.warm(self.world):
            self.bd.set_theme(self.world, now, wipe=0 if self.bd.last is None else 1.0)

    def move(self, vals, now, idle):
        return 0.0

    def restart(self, vals, now):
        self.dead_t = None
        self.hold_t = None

    # ------------------------------------------------------------ events / les événements
    def update(self, vals, now):
        ch = self.changed
        S, W = self.S, self.W
        gy = self.ground_y()
        hand = (self.hx + self.face * S(50), gy - S(95))
        px = ch(vals, "pos_x")
        if px:
            dx = max(-40, min(40, px[1] - px[0]))
            self.hx = _clamp(self.hx + dx * S(3), W * 0.18, W * 0.82)
            self.bd.scroll += dx * S(6)
            self.last_move = now
            if dx:
                self.face = 1 if dx > 0 else -1
        py = ch(vals, "pos_y")
        if py:
            self.last_move = now
        fc = _n(vals.get("facing"))
        if fc in (4, 6):
            self.face = -1 if fc == 4 else 1
        pad = ch(vals, "pad")
        if pad and (pad[1] & PAD_B) and not (pad[0] & PAD_B):           # the sword / l'épée
            self.swing_t = now
            self.fx.later(0.08, self._slash)
        if pad and (pad[1] & PAD_Y) and not (pad[0] & PAD_Y):           # the item on Y / l'objet sur Y
            self._use_item(int(_n(vals.get("item")) or 0), vals, now)
        bm = ch(vals, "bombs")
        if bm and bm[1] == bm[0] - 1:
            self._bomb(now)
        ar = ch(vals, "arrows")
        if ar and ar[1] == ar[0] - 1:
            self.arrows_out += 1
            self.fx.projectile("z3_arrow", hand[0], hand[1], hand[0] + self.face * W * 0.7, hand[1] - S(10), 0.5, 4, self._hit, spin=0, trail=0)
        rg = ch(vals, "rupee_goal")
        if rg and rg[1] > rg[0]:
            gain = rg[1] - rg[0]
            kind = "rupee_r" if gain >= 20 else ("rupee_b" if gain >= 5 else "rupee_g")
            for i in range(min(6, 1 + gain // 20)):
                self.fx.later(i * 0.07, self._rupee_fly, kind)
            if gain >= 50:
                self.say(f"+{gain} RUBIS", f"+{gain} RUPEES", GREEN, now, 1.4)
            else:
                self.popup(f"+{gain}", self.hx, gy - S(200), GREEN, size=36, life=0.9)
        hp = ch(vals, "health")
        if hp and hp[1] < hp[0] and hp[1] > 0:
            self.hurt_t = now
            self.fx.flash((255, 40, 40), 0.18, 0.2)
            self.fx.shake(6, 0.25)
        elif hp and hp[1] > hp[0]:
            self.fx.sparks(self.hx, gy - S(100), 10, (255, 140, 170), (80, 260), (180, 360), (0.3, 0.7), 100)
        hm = ch(vals, "health_max")
        if hm and hm[1] > hm[0]:
            self.say("+1 COEUR !", "+1 HEART!", (255, 80, 100), now, 1.8)
            self.fx.projectile("z3_heart", self.hx, gy - S(220), S(200), S(40), 0.9, 120, self._hit_soft, spin=0, trail=0)
        hpc = ch(vals, "heart_pieces")
        if hpc and hpc[1] > hpc[0]:
            self.say(f"QUART DE COEUR {hpc[1]}/4", f"HEART PIECE {hpc[1]}/4", PINK, now, 1.6)
        pose = ch(vals, "item_pose")
        if pose and pose[1] and not pose[0]:
            self.hold_t = now
            name = vals.get("got_name") or tr("OBJET", "ITEM")
            self.say(str(name), str(name), GOLD, now, 2.2)
            self.fx.glow(self.hx, gy - S(230), 20, 160, (255, 240, 160), 1.6, "front", 0.9, 0.0)
        elif pose and not pose[1]:
            self.hold_t = None
        for name, fr, en, col, total in (("pendant_count", "PENDENTIF", "PENDANT", (120, 255, 140), 3),
                                         ("crystal_count", "CRISTAL", "CRYSTAL", (230, 240, 255), 7)):
            v = ch(vals, name)
            if v and v[1] > v[0]:
                self.say(f"{fr} {v[1]}/{total}", f"{en} {v[1]}/{total}", col, now, 2.2)
                for i in range(8):
                    self.fx.later(0.1 + i * 0.2, self._firework)
        vi = ch(vals, "victory")
        if vi and vi[1] == 1:
            self.say("VICTOIRE !", "VICTORY!", GOLD, now, 2.6)
            for i in range(10):
                self.fx.later(0.2 + i * 0.25, self._firework)
        dk = ch(vals, "dark")
        if dk:
            self.say("MONDE DES TÉNÈBRES" if dk[1] else "MONDE DE LA LUMIÈRE", "DARK WORLD" if dk[1] else "LIGHT WORLD",
                        VIOLET if dk[1] else GREEN, now, 2.0)
            self.fx.flash((200, 160, 255), 0.4, 0.5)
        pl = ch(vals, "palace")
        if pl and pl[1] != 255 and vals.get("place"):
            self.say(str(vals["place"]), str(vals["place"]), (210, 170, 255), now, 2.0)
        md = ch(vals, "medallion")
        if md and md[1]:
            self._medallion(md[1], now)
        sp = ch(vals, "spin")
        if sp and sp[1]:
            self.fx.glow(self.hx, gy - S(90), 30, 200, (200, 230, 255), 0.5, "front", 0.8, 0.0)
            r = self.fx.add(Particle("ring", self.hx, gy - S(90), now, 0.45, "front"))
            r.r0, r.r1, r.col, r.a0, r.a1, r.data = S(30), S(220), (220, 240, 255), 0.9, 0.0, S(12)
        bn = ch(vals, "bunny")
        if bn and bn[1] and not bn[0]:
            self.say("LAPIN !", "BUNNY!", PINK, now, 1.4)
        fl = ch(vals, "fallen")
        if fl and fl[1] == 1:
            self.dead_t = now
            self.say("VAINCU !", "DEFEATED!", RED, now, 2.0)
        elif fl and fl[1] == 0:
            self.dead_t = None
        go = ch(vals, "game_over")
        if go and go[1] == 1:
            self.say("GAME OVER", "GAME OVER", RED, now, 3.0)
        fy = ch(vals, "fairy")
        if fy and fy[1] == 1:
            self.say("FÉE !", "FAIRY!", PINK, now, 2.0)
            for i in range(20):
                a = i * math.tau / 20
                self.fx.glow(self.hx + math.cos(a) * S(120), gy - S(100) + math.sin(a) * S(60), 6, 30, (255, 170, 230), 0.8, "front",
                             1.0, 0.0, delay=i * 0.04)
        te = ch(vals, "the_end")
        if te and te[1] == 1:
            self.say("FIN", "THE END", GOLD, now, 4.0)

    def _hit(self, x, y):
        self.fx.glow(x, y, 8, 50, (255, 220, 160), 0.2, "front")
        self.fx.sparks(x, y, 6, (255, 230, 170), (100, 300), (120, 240), (0.15, 0.35), 300)

    def _hit_soft(self, x, y):
        self.fx.glow(x, y, 8, 60, (255, 120, 140), 0.4, "front")

    def _rupee_fly(self, kind):
        S = self.S
        self.fx.projectile("z3_" + kind, self.hx, self.ground_y() - S(120), self.W - S(560), S(40), 0.6, 120, self._hit_soft, spin=0, trail=0)

    def _slash(self):
        S = self.S
        x, y = self.hx + self.face * S(80), self.ground_y() - S(100)
        self.fx.glow(x, y, 20, 110, (220, 236, 255), 0.22, "front", 0.9, 0.0)
        self.fx.sparks(x, y, 10, (230, 240, 255), (300, 800), (-60, 60) if self.face > 0 else (120, 240), (0.12, 0.25), 0)

    def _bomb(self, now):
        S = self.S
        self.bombs_out += 1
        x, y = self.hx + self.face * S(110), self.ground_y() - S(26)
        p = self.fx.obj("z3_bomb", x, y, 0, 0, gravity=0, life=1.5)
        p.on_end = (self._boom, (x, y - S(10)))

    def _boom(self, x, y):
        self.fx.explosion(x, y, 1.0)

    def _firework(self):
        rng = self.rng
        x, y = rng.uniform(0.15, 0.85) * self.W, rng.uniform(0.25, 0.55) * self.H
        col = rng.choice(((255, 90, 90), (90, 220, 255), (255, 230, 90), (140, 255, 140), (220, 120, 255)))
        self.fx.glow(x, y, 10, 90, col, 0.5, "front")
        self.fx.sparks(x, y, 30, col, (250, 700), (0, 360), (0.5, 1.0), 300)

    def _use_item(self, item, vals, now):
        """What the item on Y does on the screen. / Ce que fait l'objet sur Y à l'écran."""
        S, W = self.S, self.W
        gy = self.ground_y()
        hand = (self.hx + self.face * S(50), gy - S(95))
        far = (hand[0] + self.face * W * 0.45, hand[1])
        kind = ITEM_FX.get(item)
        if kind == "boomerang":
            self.fx.projectile("z3_boomerang", hand[0], hand[1], far[0], far[1] - S(20), 0.45, 30,
                               lambda x, y: self.fx.projectile("z3_boomerang", x, y, self.hx, hand[1], 0.45, -30, self._hit_soft, spin=900,
                                                               trail=0), spin=900, trail=0)
        elif kind == "fire":
            self.fx.projectile("z3_fireball", hand[0], hand[1], far[0], far[1], 0.45, 0, lambda x, y: self.fx.small_blast(x, y, 1.4, "front"),
                               spin=0, trail=0.03)
        elif kind == "ice":
            self.fx.projectile("z3_iceball", hand[0], hand[1], far[0], far[1], 0.45, 0,
                               lambda x, y: self.fx.sparks(x, y, 24, (190, 240, 255), (200, 600), (0, 360), (0.3, 0.7), 300), spin=0, trail=0)
        elif kind == "hookshot":
            self.fx.tracer(hand[0], hand[1], far[0], far[1], 2200, (220, 220, 230), 5, 160)
        elif kind == "hammer":
            self.fx.shake(14, 0.35)
            self.fx.smoke(hand[0] + self.face * S(40), gy, 6, (14, 26), 2.4, (0.5, 0.9), (20, 60), 40, (200, 190, 170), 160, "front")
        elif kind == "lamp":
            self.fx.glow(hand[0] + self.face * S(40), hand[1], 20, 120, (255, 170, 60), 0.6, "front")
        elif kind == "powder":
            self.fx.sparks(hand[0] + self.face * S(40), hand[1], 26, (255, 200, 255), (60, 260), (0, 360), (0.4, 0.9), -100)
        elif kind == "flute":
            for i in range(5):
                self.fx.glow(self.hx + S(30) * i * self.face, gy - S(180) - S(30) * i, 6, 34, (200, 240, 255), 0.9, "front", 1.0, 0.0,
                             delay=i * 0.15)
        elif kind in ("net", "book", "somaria", "byrna", "mirror", "cape"):
            self.fx.glow(self.hx, gy - S(100), 20, 150, (200, 200, 255), 0.5, "front", 0.8, 0.0)

    def _medallion(self, which, now):
        S, W, H = self.S, self.W, self.H
        if which == 2:                                                   # Bombos: fire all over / du feu partout
            self.say("BOMBOS !", "BOMBOS!", (255, 140, 60), now, 2.2)
            for i in range(9):
                self.fx.later(0.2 + i * 0.16, self.fx.explosion, (i + 0.5) * W / 9, H - S(150), 0.9)
        elif which == 1:                                                 # Ether: lightning / des éclairs
            self.say("ETHER !", "ETHER!", SKY, now, 2.2)
            for i in range(6):
                x = self.rng.uniform(0.1, 0.9) * W
                self.fx.later(0.15 + i * 0.2, self.fx.tracer, x, -S(20), x + self.rng.uniform(-80, 80) * self.s, H - S(80), 9000, (190, 220, 255),
                              10, 500)
                self.fx.later(0.15 + i * 0.2, self.fx.flash, (160, 200, 255), 0.5, 0.15)
        else:                                                            # Quake: the ground shakes / la terre tremble
            self.say("SÉISME !", "QUAKE!", (220, 180, 110), now, 2.2)
            self.fx.shake(30, 1.8)
            for i in range(14):
                self.fx.later(i * 0.1, self.fx.smoke, self.rng.uniform(0, W), self.ground_y(), 2, (20, 40), 2.6, (0.8, 1.4), (30, 90), 30,
                              (170, 150, 120), 170, "front")

    # ------------------------------------------------------------ drawing / le dessin
    def draw_hero(self, screen, vals, now):
        S = self.S
        gy = self.ground_y()
        action = int(_n(vals.get("action")) or 0)
        walking = now - self.last_move < 0.35
        if walking:
            self.walk_ph += self.dt * 9
        pose, frame = ("run", int(self.walk_ph) % 4) if walking else ("stand", 0)
        if now - self.swing_t < 0.3:
            pose = "swing0" if now - self.swing_t < 0.12 else "swing1"
        if action == 17:
            pose = "dash"
            if self.rng.random() < 0.4:
                self.fx.smoke(self.hx - self.face * S(40), gy - S(6), 1, (8, 14), 2.0, (0.3, 0.6), (10, 30), 8, (230, 220, 200), 120, "front")
        if now - self.hurt_t < 0.4:
            pose = "hurt"
        if self.hold_t is not None or action == 21:
            pose = "hold"
        dead = self.dead_t is not None
        if _n(vals.get("bunny")):
            img = self.img(("bunny", self.face < 0), S(120), S(130), bunny_draw, ss=2, flip=self.face < 0)
        else:
            img = self.hero_img("dead" if dead else pose, vals, frame, flip=self.face < 0)
        if action in (3, 30):                                            # spin attack / attaque tourbillon
            img = self.rotated(("ren_spin",) + tuple(int(_n(vals.get(k)) or 0) for k in ("armor", "sword", "shield")), img, (now * 1100) % 360, 15)
        if dead:
            img = self.rotated(("ren_dead", self.face) + tuple(int(_n(vals.get(k)) or 0) for k in ("armor", "sword", "shield")), img,
                               90 * self.face, 90)
        y = gy - img.get_height()
        swim = action == 4
        if swim:
            y += img.get_height() * 0.45
        if (_n(vals.get("cape_on")) or 0) and int(now * 10) % 2:
            return
        screen.blit(img, (int(self.hx - img.get_width() / 2), int(y)))
        if swim:
            self.pg.draw.rect(screen, (60, 140, 220), (0, int(gy - S(40)), self.W, S(60)))
        if pose == "hold" and vals.get("got_name"):
            self.fx.glow(self.hx, gy - S(205), 4, 40, (255, 240, 180), 0.08, "front")
        charge = _n(vals.get("sword_charge")) or 0
        if charge > 30 and int(now * 12) % 2 == 0:
            tip = (self.hx + self.face * S(110), gy - S(110))
            self.fx.glow(tip[0], tip[1], 6, 40, (200, 230, 255), 0.08, "front")
        if (_n(vals.get("module")) == 14 and _n(vals.get("submodule")) == 2):     # a text box / une boîte de texte
            self.label(screen, "...", self.hx, gy - S(200), 40, WHITE, align="center")

    def draw_hud(self, screen, eng, vals, logo, now):
        hd, S, W, H = self.hd, self.S, self.W, self.H
        self.draw_hero(screen, vals, now)
        hd.draw_logo(screen, logo, W / 2, S(8), S(520), S(92), now)
        # hearts / les cœurs
        cap = int(_n(vals.get("health_max")) or 0) // 8
        hp = int(_n(vals.get("health")) or 0)
        full, half = (((hp + 3) & ~3) // 8, (((hp + 3) & ~3) % 8) // 4)
        low = hp <= 8 and int(now * 4) % 2 == 0
        shake = S(4) * math.sin(now * 60) if now - self.hurt_t < 0.3 else 0
        if cap:
            self.pill(screen, S(14), S(6), S(26) + min(cap, 10) * S(34), S(30) + (S(34) if cap > 10 else 0) + S(32), 140, radius=16)
        for i in range(cap):
            x, y = S(30) + (i % 10) * S(34) + shake, S(14) + (i // 10) * S(34)
            if i < full:
                key, fn = ("h_full", low), heart_draw((255, 255, 255) if low else (240, 40, 50), (120, 10, 20))
            elif i == full and half:
                key, fn = ("h_half",), heart_draw((240, 40, 50), (120, 10, 20), half=True)
            else:
                key, fn = ("h_empty",), heart_draw((40, 10, 16), (110, 30, 40))
            screen.blit(self.img(key, S(30), S(28), fn), (int(x), int(y)))
        mg = _n(vals.get("magic"))
        if mg is not None:
            yb = S(20) + (S(34) if cap > 10 else 0) + S(32)
            self.bar(screen, S(30), yb, S(240), S(14), mg / 128.0, (60, 220, 90), back=(20, 40, 24))
        # rupees, bombs, arrows, keys / rubis, bombes, flèches, clés
        x = W - S(30)
        items = [("keys", key_draw, (24, 34), (255, 220, 90)), ("arrows", arrow_draw, (52, 14), CREAM), ("bombs", bomb_draw, (34, 36), (170, 190, 255)),
                 ("rupees", gem_draw((60, 220, 90)), (22, 34), (120, 255, 140))]
        self.pill(screen, W - S(560), S(6), S(546), S(70), 140)
        for name, fn, (iw, ih), col in items:
            v = _n(vals.get(name))
            if v is None or (name == "keys" and (v == 255 or v > 99)):
                continue
            t = f"{int(v):03d}" if name == "rupees" else str(int(v))
            w = hd.text(t, "black", S(44), col)["w"]
            hd.put_number(screen, t, "black", S(44), col, x, S(22), "right")
            ic = self.img(("hud", name), S(iw), S(ih), fn)
            x -= w + S(10) + ic.get_width()
            screen.blit(ic, (int(x), int(S(40) - ic.get_height() / 2)))
            x -= S(28)
        # the item on Y / l'objet sur Y
        nm = vals.get("item_name")
        if nm:
            self.label(screen, f"Y  {nm}", S(30), H - S(40), 30, CREAM)
        # the quest: pendants and crystals / la quête : pendentifs et cristaux
        gems = [((60, 220, 90), _n(vals.get("pend_courage"))), ((70, 130, 255), _n(vals.get("pend_power"))),
                ((255, 80, 80), _n(vals.get("pend_wisdom")))] + [((235, 240, 255), _n(vals.get(f"crystal{i + 1}"))) for i in range(7)]
        if any(v is not None for _, v in gems):
            self.pill(screen, W - S(30) - S(10 * 34 + 30), H - S(70), S(10 * 34 + 30), S(56), 140)
            for i, (col, v) in enumerate(gems):
                gx = W - S(30) - S(10 * 34) + i * S(34) + (S(10) if i >= 3 else 0)
                ic = self.img(("gem", col, bool(v)), S(20), S(30), gem_draw(col if v else _mix(col, (0, 0, 0), 0.75)))
                screen.blit(ic, (int(gx), int(H - S(57))))
        place = vals.get("place") if _n(vals.get("palace")) not in (None, 255) else vals.get("world_name")
        if place:
            self.label(screen, str(place), W / 2, H - S(40), 28, (210, 190, 255) if _n(vals.get("palace")) not in (None, 255) else CREAM,
                       align="center", alpha=120)

    def draw_attract(self, screen, eng, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        self.bd.scroll += S(50) * self.dt
        hd.draw_logo(screen, logo, W / 2, S(170), S(1000), S(220), now, valign="middle")
        k = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(now * 5))
        self.label(screen, tr("APPUIE SUR START", "PRESS START"), W / 2, S(372), 48, tuple(int(c * k) for c in AMBER), align="center")
        img = self.hero_img("run", {"sword": 1, "shield": 1}, int(now * 8) % 4)
        screen.blit(img, (int(W * 0.12), int(self.ground_y() - img.get_height())))


SCENES = {"smw": PlatformScene, "zelda3": AdventureScene}
