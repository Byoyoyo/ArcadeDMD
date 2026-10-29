"""HD scenes of the third batch of Neo Geo games done one by one (1.19): Top Hunter, Baseball Stars 2, Last Resort,
Aero Fighters 2, Aero Fighters 3. Same idea as the first two batches: each game has its own animated backdrop and
reacts to the values read in its memory. Everything is drawn by the program, no image or character comes from a game.

Scènes HD du troisième lot de jeux Neo Geo faits un par un (1.19). Même principe que les deux premiers lots : chaque
jeu a son décor animé et réagit aux valeurs lues dans sa mémoire. Tout est dessiné par le programme, aucune image ni
aucun personnage tiré d'un jeu.
"""

import math

from .hd_fx import Particle
from .hd_games import BTN_A, BTN_B, CREAM, GOLD, GREY, P1C, P2C, RED, WHITE, BlazingStarScene, GameScene, _clamp, _mix, _n, draw_img
from .hd_themes3 import AF_AVENUES, TH_FEET, TH_WORLDS, bb_fence, bb_geom, bb_px, bb_xy     # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr

DARK = (22, 20, 30)


def _poly(d, pts, W, H, fill, outline=None, width=0):
    d.polygon([(x * W, y * H) for x, y in pts], fill=fill, outline=outline, width=width)


def _lerp(a, b, k):
    return a + (b - a) * k


# ============================================================================ Top Hunter
# The figures are drawn from a small skeleton: a pose gives the lean of the body and the angles of the limbs (0 = straight
# down, 90 = straight ahead, 180 = straight up), the joints follow, then the armour is drawn on the bones. Everything is
# drawn facing right; the robots are turned round when they are used. Sizes are in body units (about the height of the
# figure). / Les personnages sont dessinés sur un petit squelette ; tout est dessiné tourné vers la droite.
def _seg(p, a, ln):
    a = math.radians(a)
    return p[0] + math.sin(a) * ln, p[1] + math.cos(a) * ln


def _capsule(d, a, b, wa, wb, fill, out=None, ow=0):
    """A limb from a to b, wa wide at a and wb at b, rounded ends, with a dark outline. / Un membre arrondi au bout."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy) or 1e-6
    nx, ny = -dy / ln, dx / ln
    for col, extra in ((out, ow), (fill, 0)):
        if col is None:
            continue
        ra, rb = wa / 2 + extra, wb / 2 + extra
        d.polygon([(a[0] + nx * ra, a[1] + ny * ra), (b[0] + nx * rb, b[1] + ny * rb), (b[0] - nx * rb, b[1] - ny * rb),
                   (a[0] - nx * ra, a[1] - ny * ra)], fill=col)
        d.ellipse([a[0] - ra, a[1] - ra, a[0] + ra, a[1] + ra], fill=col)
        d.ellipse([b[0] - rb, b[1] - rb, b[0] + rb, b[1] + rb], fill=col)


def _shape(d, pts, fill, out, ow):
    d.polygon(pts, fill=fill)
    if out is not None and ow > 0:
        d.line(list(pts) + [pts[0], pts[1]], fill=out, width=int(ow), joint="curve")


def _disc(d, c, r, fill, out=None, ow=0):
    d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=fill, outline=out, width=int(ow) if out is not None else 0)


class _Frame:
    """Body frame of a figure: the pelvis, the lean, and the way from body units to pixels. / Repère du corps."""

    def __init__(self, ox, oy, unit, lean):
        a = math.radians(lean)
        self.ox, self.oy, self.u = ox, oy, unit
        self.up = (math.sin(a), -math.cos(a))
        self.fw = (math.cos(a), math.sin(a))

    def __call__(self, x, y):                       # x ahead, y up, from the pelvis
        u = self.u
        return (self.ox + (self.fw[0] * x + self.up[0] * y) * u, self.oy + (self.fw[1] * x + self.up[1] * y) * u)


def _cap(d, c, toward, r, fill, out=None, ow=0, light=None, band=None, flat=1.0):
    """Shoulder pad: a dome on c whose top points toward 'toward', r wide. / Épaulière : un dôme tourné vers 'toward'."""
    dx, dy = toward[0] - c[0], toward[1] - c[1]
    ln = math.hypot(dx, dy) or 1e-6
    ux, uy = dx / ln, dy / ln
    px, py = -uy, ux
    pts = []
    for i in range(13):
        a = -math.pi / 2 + math.pi * i / 12
        pts.append((c[0] + (ux * math.cos(a) * flat + px * math.sin(a)) * r, c[1] + (uy * math.cos(a) * flat + py * math.sin(a)) * r))
    pts.append((c[0] - ux * r * 0.28, c[1] - uy * r * 0.28))
    _shape(d, pts, fill, out, ow)
    if light is not None:
        q = [(c[0] + (ux * (0.25 + 0.6 * math.cos(a)) * flat + px * 0.62 * math.sin(a)) * r,
              c[1] + (uy * (0.25 + 0.6 * math.cos(a)) * flat + py * 0.62 * math.sin(a)) * r) for a in [(-1.1 + 1.7 * i / 8) for i in range(9)]]
        d.polygon(q, fill=light)
    if band is not None:
        d.line([(c[0] + px * r * 0.98 - ux * r * 0.02, c[1] + py * r * 0.98 - uy * r * 0.02), (c[0] - ux * r * 0.25, c[1] - uy * r * 0.25),
                (c[0] - px * r * 0.98 - ux * r * 0.02, c[1] - py * r * 0.98 - uy * r * 0.02)], fill=band, width=max(1, int(r * 0.2)), joint="curve")


def _boot(d, ankle, ang, u, fill, sole, out, ow, length=0.12):
    """Boot at the ankle, its toe turned by ang degrees (0 = flat, ahead). / Botte, la pointe tournée de ang degrés."""
    a = math.radians(ang)
    fx, fy = math.cos(a), math.sin(a)
    nx, ny = fy, -fx                                                       # vers le haut de la botte

    def P(f, n):
        return ankle[0] + (fx * f + nx * n) * u, ankle[1] + (fy * f + ny * n) * u
    pts = [P(-0.045, -0.03), P(length, -0.03), P(length + 0.008, -0.005), P(length - 0.03, 0.03), P(0.03, 0.05), P(-0.04, 0.065)]
    _shape(d, pts, fill, out, ow)
    d.polygon([P(-0.045, -0.03), P(length, -0.03), P(length - 0.004, -0.014), P(-0.045, -0.014)], fill=sole)


# poses of the hunter: lean of the body, tilt of the head, legs (far, near) as (thigh, shin, foot), arms (far, near) as
# (upper arm, forearm). / Poses du chasseur : inclinaison, tête, jambes (cuisse, tibia, pied), bras (bras, avant-bras).
TH_POSES = {
    0: (6, 0, ((-22, -8, 0), (30, -2, 0)), ((24, 122), (48, 128))),                 # garde
    1: (14, 4, ((-38, -72, 40), (44, 6, -10)), ((52, 132), (-38, 30))),             # course
    2: (14, 4, ((42, 2, -8), (-32, -76, 40)), ((-38, 30), (54, 132))),
    3: (16, 6, ((-34, -36, 0), (36, 4, 0)), ((24, 128), (90, 90))),                 # coup droit
    4: (8, -6, ((72, -24, 20), (98, 8, 10)), ((150, 176), (96, 128))),              # saut
    5: (-20, -18, ((-6, -2, 0), (34, 22, 0)), ((140, 168), (-58, -96))),            # touché
    6: (-12, -10, ((-26, -16, 0), (26, 14, 0)), ((150, 172), (136, 160))),          # soulève
    7: (10, -8, ((-32, -30, 0), (62, -14, 0)), ((28, 118), (122, 166))),            # uppercut
}
TH_BODY = {"thigh": 0.205, "shin": 0.205, "upper": 0.13, "fore": 0.13, "neck": 0.27}
TH_BOX = (0.92, 1.0)            # size of a hunter's picture (share of his height) / taille de l'image d'un chasseur
TH_ANCHOR = 0.5                 # his position in the picture / sa place dans l'image
TH_FILL = 0.92                  # height of the guard pose in the picture (room above for the other poses)


def _hunter_joints(frame):
    """Joints of the hunter in body units, pelvis at (0, 0), y down. / Articulations du chasseur."""
    lean, tilt, legs, arms = TH_POSES[frame]
    B = TH_BODY
    F = _Frame(0.0, 0.0, 1.0, lean)
    J = {"F": F, "lean": lean, "tilt": tilt}
    J["neck"] = F(0.005, B["neck"])
    J["sh"] = (F(-0.05, 0.225), F(0.035, 0.22))
    J["hip"] = (F(-0.035, 0.0), F(0.03, 0.0))
    J["legs"], J["arms"] = [], []
    for hip, (th, sh, ft) in zip(J["hip"], legs):
        knee = _seg(hip, th, B["thigh"])
        ankle = _seg(knee, sh, B["shin"])
        J["legs"].append((hip, knee, ankle, ft))
    for sh, (ua, fa) in zip(J["sh"], arms):
        el = _seg(sh, ua, B["upper"])
        J["arms"].append((sh, el, _seg(el, fa, B["fore"]), fa))
    h = math.radians(lean + tilt)
    J["head"] = (J["neck"][0] + math.sin(h) * 0.09 + math.cos(h) * 0.03, J["neck"][1] - math.cos(h) * 0.09 + math.sin(h) * 0.03)
    J["foot"] = max(a[1] + 0.03 for _, _, a, _ in J["legs"])                # bas des semelles
    return J


TH_HEIGHT = _hunter_joints(0)["foot"] - (_hunter_joints(0)["head"][1] - 0.14)      # guard pose, sole to crest


def th_hunter_point(frame, name):
    """Where a part of the hunter is in his picture (share of the width and the height): 'fist' of the near arm.
    / Où se trouve une partie du chasseur dans son image."""
    J = _hunter_joints(frame)
    u = TH_FILL / TH_HEIGHT
    p = J["arms"][1][2] if name == "fist" else J["head"]
    return TH_ANCHOR + p[0] * u / TH_BOX[0], 0.985 + (p[1] - J["foot"]) * u


def _hunter_head(d, hx, hy, r, rot, suit, trim, dark, ow, hurt=False):
    """Helmet with a visor over the eyes, the square jaw below, an ear piece, a crest. / Casque, visière, mâchoire, crête."""
    armor, armor_d, light = suit + (255,), _mix(suit, (0, 0, 0), 0.3) + (255,), _mix(suit, WHITE, 0.45) + (255,)
    tm, tm_l = trim + (255,), _mix(trim, WHITE, 0.55) + (255,)
    c, s_ = math.cos(rot), math.sin(rot)

    def H(x, y):
        return hx + (x * c - y * s_) * r, hy + (x * s_ + y * c) * r
    _shape(d, [H(0.1, -0.2), H(0.98, -0.18), H(1.1, 0.28), H(0.98, 0.42), H(0.92, 0.72), H(0.68, 1.02), H(0.2, 1.08), H(-0.15, 0.8)],
           (238, 190, 150, 255), dark, ow)                                                             # visage
    _shape(d, [H(0.62, 0.72), H(0.9, 0.68), H(0.86, 0.95), H(0.62, 1.0)], (214, 160, 124, 255), None, 0)   # ombre du menton
    if hurt:
        _shape(d, [H(0.55, 0.62), H(0.88, 0.58), H(0.84, 0.86), H(0.6, 0.86)], (110, 40, 40, 255), dark, ow * 0.7)
    else:
        d.line([H(0.56, 0.66), H(0.9, 0.6)], fill=(120, 60, 50, 255), width=max(1, int(ow * 0.9)))
    helmet = [H(1.02, -0.42), H(0.9, -0.78), H(0.5, -1.04), H(0.0, -1.1), H(-0.5, -0.98), H(-0.9, -0.64), H(-1.06, -0.12), H(-0.98, 0.38),
              H(-0.78, 0.74), H(-0.3, 0.76), H(-0.05, 0.42), H(0.1, -0.05), H(0.2, -0.42)]
    _shape(d, helmet, armor, dark, ow)
    d.polygon([H(0.82, -0.62), H(0.45, -0.92), H(0.0, -0.98), H(-0.45, -0.86), H(-0.7, -0.55), H(-0.3, -0.62), H(0.2, -0.58), H(0.6, -0.48)],
              fill=light)                                                                               # reflet
    d.polygon([H(-0.98, 0.3), H(-0.75, 0.66), H(-0.32, 0.68), H(-0.12, 0.38), H(-0.6, 0.42)], fill=armor_d)
    _shape(d, [H(-0.5, -0.98), H(0.12, -1.5), H(0.46, -1.38), H(0.3, -0.98)], tm, dark, ow)              # crête
    _shape(d, [H(0.12, -0.46), H(1.12, -0.44), H(1.16, 0.06), H(0.42, 0.14), H(0.08, -0.12)], (36, 196, 250, 255), dark, ow)   # visière
    d.polygon([H(0.55, -0.36), H(1.0, -0.35), H(0.98, -0.18), H(0.6, -0.15)], fill=(205, 250, 255, 255))
    d.polygon([H(0.3, -0.36), H(0.45, -0.36), H(0.5, -0.0), H(0.36, 0.02)], fill=(120, 230, 255, 255))
    _disc(d, H(-0.42, 0.12), 0.3 * r, tm, dark, ow)                                                       # écouteur
    _disc(d, H(-0.42, 0.12), 0.13 * r, _mix(trim, (0, 0, 0), 0.35) + (255,))
    _disc(d, H(-0.5, 0.03), 0.08 * r, tm_l)


def hunter_draw(suit, trim, frame):
    """Space hunter seen from the side, facing right: a helmet with a visor over a square jaw, armour plates on a dark
    suit, big power gloves, boots, a jet pack. Frames 0 guard, 1 and 2 run, 3 punch, 4 jump, 5 hurt, 6 lifting a robot,
    7 uppercut. / Chasseur de l'espace : casque à visière, armure, gros gants, bottes, réacteur dorsal."""
    def fn(d, W, H):
        J = _hunter_joints(frame)
        u = TH_FILL * H / TH_HEIGHT
        ox, oy = W * TH_ANCHOR, H * 0.985 - J["foot"] * u

        def P(p):
            return ox + p[0] * u, oy + p[1] * u
        dark = DARK + (255,)
        ow = max(1.0, 0.012 * u)
        armor = suit + (255,)
        armor_d = _mix(suit, (0, 0, 0), 0.3) + (255,)
        armor_dd = _mix(suit, (0, 0, 0), 0.5) + (255,)
        light = _mix(suit, WHITE, 0.42) + (255,)
        tm, tm_d = trim + (255,), _mix(trim, (0, 0, 0), 0.32) + (255,)
        tm_l = _mix(trim, WHITE, 0.55) + (255,)
        under, under_d = (60, 62, 80, 255), (38, 40, 54, 255)
        F = J["F"]

        def T(x, y):
            return P(F(x, y))

        def leg(i):
            hip, knee, ankle, ft = J["legs"][i]
            near = i == 1
            h, k, a = P(hip), P(knee), P(ankle)
            _capsule(d, h, k, 0.11 * u, 0.08 * u, under if near else under_d, dark, ow)            # cuisse
            dx, dy = k[0] - h[0], k[1] - h[1]
            ln = math.hypot(dx, dy) or 1
            nx, ny = dy / ln, -dx / ln                                                              # côté avant de la jambe
            if near:
                _capsule(d, (h[0] - nx * 0.02 * u + dx * 0.15, h[1] - ny * 0.02 * u + dy * 0.15), (k[0] - nx * 0.016 * u - dx * 0.2, k[1] - ny * 0.016 * u - dy * 0.2),
                         0.05 * u, 0.04 * u, armor_d, dark, ow * 0.8)                              # plaque de cuisse
                _capsule(d, (h[0] - nx * 0.03 * u + dx * 0.2, h[1] - ny * 0.03 * u + dy * 0.2), (k[0] - nx * 0.022 * u - dx * 0.28, k[1] - ny * 0.022 * u - dy * 0.28),
                         0.016 * u, 0.012 * u, armor)
            _capsule(d, k, a, 0.085 * u, 0.075 * u, armor if near else armor_d, dark, ow)          # jambière
            dx, dy = a[0] - k[0], a[1] - k[1]
            ln = math.hypot(dx, dy) or 1
            nx, ny = dy / ln, -dx / ln
            if near:
                _capsule(d, (k[0] - nx * 0.02 * u + dx * 0.18, k[1] - ny * 0.02 * u + dy * 0.18),
                         (a[0] - nx * 0.018 * u - dx * 0.3, a[1] - ny * 0.018 * u - dy * 0.3), 0.02 * u, 0.016 * u, light)
            _disc(d, k, 0.05 * u, tm if near else tm_d, dark, ow)                                  # genouillère
            if near:
                _disc(d, (k[0] - 0.014 * u, k[1] - 0.014 * u), 0.017 * u, tm_l)
            _boot(d, a, ft, u, armor_d if near else armor_dd, dark, dark, ow, length=0.135)
            d.line([P((ankle[0] - 0.035, ankle[1] - 0.045)), P((ankle[0] + 0.035, ankle[1] - 0.05))], fill=tm if near else tm_d,
                   width=int(0.02 * u))                                                              # bande de la botte

        def arm(i):
            sh, el, fist, fa = J["arms"][i]
            near = i == 1
            s, e, f = P(sh), P(el), P(fist)
            _capsule(d, s, e, 0.08 * u, 0.068 * u, under if near else under_d, dark, ow)          # bras
            _capsule(d, e, f, 0.092 * u, 0.104 * u, armor if near else armor_d, dark, ow)         # gantelet
            dx, dy = f[0] - e[0], f[1] - e[1]
            ln = math.hypot(dx, dy) or 1
            nx, ny = dy / ln, -dx / ln
            if ny > 0:
                nx, ny = -nx, -ny                                                                   # le reflet du côté du ciel
            d.line([(e[0] + dx * 0.55 + nx * 0.05 * u, e[1] + dy * 0.55 + ny * 0.05 * u), (e[0] + dx * 0.55 - nx * 0.05 * u, e[1] + dy * 0.55 - ny * 0.05 * u)],
                   fill=tm if near else tm_d, width=int(0.018 * u))                                  # bande du gantelet
            if near:
                _capsule(d, (e[0] + dx * 0.12 + nx * 0.026 * u, e[1] + dy * 0.12 + ny * 0.026 * u),
                         (e[0] + dx * 0.45 + nx * 0.03 * u, e[1] + dy * 0.45 + ny * 0.03 * u), 0.018 * u, 0.02 * u, light)
            r = 0.064 * u if near else 0.056 * u                                                    # gros poing
            _disc(d, f, r, tm if near else tm_d, dark, ow)
            a = math.radians(fa)
            kx, ky = f[0] + math.sin(a) * r * 0.42, f[1] + math.cos(a) * r * 0.42
            d.line([(kx - math.cos(a) * r * 0.62, ky + math.sin(a) * r * 0.62), (kx + math.cos(a) * r * 0.62, ky - math.sin(a) * r * 0.62)],
                   fill=dark, width=max(1, int(ow * 0.8)))                                          # jointures
            if near:
                _disc(d, (f[0] - r * 0.32, f[1] - r * 0.36), r * 0.3, tm_l)

        def pad(i):
            sh, el, _, _ = J["arms"][i]
            s, e = P(sh), P(el)
            near = i == 1
            c = (s[0] + (e[0] - s[0]) * 0.12, s[1] + (e[1] - s[1]) * 0.12 - 0.01 * u)
            _cap(d, c, (2 * c[0] - e[0], 2 * c[1] - e[1]), (0.075 if near else 0.066) * u, armor if near else armor_d, dark, ow,
                 light=light if near else None, band=tm if near else tm_d, flat=0.95)

        arm(0)
        pad(0)
        leg(0)
        _shape(d, [T(-0.16, 0.09), T(-0.075, 0.09), T(-0.065, 0.255), T(-0.14, 0.265)], (100, 106, 126, 255), dark, ow)   # réacteur
        d.polygon([T(-0.15, 0.2), T(-0.085, 0.2), T(-0.08, 0.25), T(-0.135, 0.255)], fill=(140, 148, 170, 255))
        _shape(d, [T(-0.155, 0.09), T(-0.085, 0.09), T(-0.09, 0.05), T(-0.15, 0.05)], (70, 72, 88, 255), dark, ow)
        _disc(d, T(-0.12, 0.04), 0.02 * u, (90, 226, 255, 255))
        neck = (J["neck"], J["head"])
        _capsule(d, P(neck[0]), P(((neck[0][0] + neck[1][0]) / 2, (neck[0][1] + neck[1][1]) / 2)), 0.07 * u, 0.065 * u, under_d, dark, ow)
        torso = [T(-0.08, -0.02), T(0.075, -0.02), T(0.07, 0.07), T(0.125, 0.165), T(0.1, 0.25), T(0.02, 0.272), T(-0.085, 0.265), T(-0.118, 0.17),
                 T(-0.085, 0.07)]
        _shape(d, torso, armor, dark, ow)
        d.polygon([T(-0.05, 0.13), T(0.105, 0.16), T(0.088, 0.238), T(0.02, 0.258), T(-0.06, 0.25)], fill=light)       # plastron
        d.polygon([T(-0.012, 0.15), T(0.06, 0.168), T(0.03, 0.2)], fill=tm)                                           # chevron
        for k in (0.04, 0.08):                                                                        # abdominaux
            d.line([T(-0.06, k), T(0.06, k + 0.006)], fill=armor_d, width=int(0.011 * u))
        d.line([T(0.0, 0.02), T(0.006, 0.12)], fill=armor_d, width=int(0.011 * u))
        _shape(d, [T(-0.085, -0.035), T(0.08, -0.035), T(0.08, 0.012), T(-0.085, 0.012)], dark, None, 0)              # ceinture
        _shape(d, [T(0.016, -0.03), T(0.066, -0.03), T(0.066, 0.008), T(0.016, 0.008)], tm, None, 0)
        leg(1)
        hx, hy = P(J["head"])
        _hunter_head(d, hx, hy, 0.105 * u, math.radians(J["lean"] + J["tilt"]), suit, trim, dark, ow, hurt=frame == 5)
        arm(1)
        pad(1)
    return fn


# ---------------------------------------------------------------------------- robots
BOT_POSES = {   # lean, legs (far, near) (thigh, shin, foot), far arm (upper, fore), near arm with the gun (upper, fore)
    0: (6, ((-24, -6, 0), (24, 2, 0)), ((-20, 40), (60, 88))),
    1: (6, ((10, -2, 0), (-8, -4, 0)), ((10, 60), (66, 90))),
    2: (-16, ((-10, -2, 0), (30, 18, 0)), ((120, 150), (150, 120))),
    3: (-4, ((-28, -10, 0), (26, 4, 0)), ((10, 70), (90, 90))),
}
BOT_BODY = {"thigh": 0.2, "shin": 0.2, "upper": 0.12, "fore": 0.15}
BOT_BOX = (0.95, 1.0)


def _bot_joints(frame):
    lean, legs, arms = BOT_POSES[frame]
    F = _Frame(0.0, 0.0, 1.0, lean)
    J = {"F": F, "lean": lean, "legs": [], "arms": []}
    J["sh"] = (F(-0.07, 0.25), F(0.04, 0.245))
    for hip, (th, sh, ft) in zip((F(-0.05, 0.0), F(0.04, 0.0)), legs):
        knee = _seg(hip, th, BOT_BODY["thigh"])
        J["legs"].append((hip, knee, _seg(knee, sh, BOT_BODY["shin"]), ft))
    for s, (ua, fa) in zip(J["sh"], arms):
        el = _seg(s, ua, BOT_BODY["upper"])
        J["arms"].append((s, el, _seg(el, fa, BOT_BODY["fore"]), fa))
    J["head"] = F(0.035, 0.37)
    J["foot"] = max(a[1] + 0.035 for _, _, a, _ in J["legs"])
    return J


BOT_HEIGHT = _bot_joints(0)["foot"] - (_bot_joints(0)["head"][1] - 0.125)


def bot_muzzle(frame):
    """End of the robot's gun in its picture (share of the width and the height, facing right)."""
    J = _bot_joints(frame)
    u = 0.95 / BOT_HEIGHT
    s, e, f, fa = J["arms"][1]
    a = math.radians(fa)
    tip = (f[0] + math.sin(a) * 0.075, f[1] + math.cos(a) * 0.075)
    return 0.42 + tip[0] * u / BOT_BOX[0], 0.985 + (tip[1] - J["foot"]) * u


def bot_draw(tint, frame):
    """Robot trooper, drawn facing right: a heavy helmet with a red visor and a grille, a barrel chest with a light in it,
    big shoulder pads, a gun for a forearm. Frames 0 and 1 walk, 2 hit, 3 fire.
    / Robot soldat : casque lourd à visière rouge, torse en tonneau, grosses épaulières, bras canon."""
    def fn(d, W, H):
        J = _bot_joints(frame)
        u = 0.95 * H / BOT_HEIGHT
        ox, oy = W * 0.42, H * 0.985 - J["foot"] * u

        def P(p):
            return ox + p[0] * u, oy + p[1] * u
        F = J["F"]

        def T(x, y):
            return P(F(x, y))
        dark = DARK + (255,)
        ow = max(1.0, 0.014 * u)
        body, light = tint + (255,), _mix(tint, WHITE, 0.42) + (255,)
        shade, shade2 = _mix(tint, (0, 0, 0), 0.3) + (255,), _mix(tint, (0, 0, 0), 0.5) + (255,)
        joint, metal = (60, 62, 76, 255), (96, 100, 116, 255)

        def leg(i):
            hip, knee, ankle, ft = J["legs"][i]
            near = i == 1
            h, k, a = P(hip), P(knee), P(ankle)
            _capsule(d, h, k, 0.075 * u, 0.065 * u, joint, dark, ow)
            _capsule(d, k, a, 0.11 * u, 0.095 * u, body if near else shade, dark, ow)
            if near:
                _capsule(d, (k[0] - 0.024 * u, k[1] + 0.03 * u), (a[0] - 0.022 * u, a[1] - 0.035 * u), 0.022 * u, 0.018 * u, light)
            _disc(d, k, 0.05 * u, shade if near else shade2, dark, ow)
            _boot(d, a, ft, u, shade if near else shade2, dark, dark, ow, length=0.14)

        def arm(i):
            s, e, f, fa = J["arms"][i]
            near = i == 1
            S_, E, Fp = P(s), P(e), P(f)
            _capsule(d, S_, E, 0.065 * u, 0.06 * u, joint, dark, ow)
            if near:                                                                      # le bras canon
                a = math.radians(fa)
                tip = P((f[0] + math.sin(a) * 0.075, f[1] + math.cos(a) * 0.075))
                _capsule(d, E, tip, 0.075 * u, 0.065 * u, metal, dark, ow)
                _capsule(d, E, Fp, 0.115 * u, 0.105 * u, body, dark, ow)
                for k in (0.35, 0.7):
                    q = (E[0] + (Fp[0] - E[0]) * k, E[1] + (Fp[1] - E[1]) * k)
                    nx, ny = -math.cos(a), math.sin(a)
                    d.line([(q[0] + nx * 0.05 * u, q[1] + ny * 0.05 * u), (q[0] - nx * 0.05 * u, q[1] - ny * 0.05 * u)], fill=shade,
                           width=int(0.014 * u))
                _capsule(d, (E[0] + 0.01 * u, E[1] - 0.026 * u), (Fp[0] - 0.01 * u, Fp[1] - 0.026 * u), 0.02 * u, 0.02 * u, light)
                _disc(d, tip, 0.03 * u, (255, 150, 70, 255) if frame == 3 else dark)
            else:
                _capsule(d, E, Fp, 0.08 * u, 0.075 * u, shade, dark, ow)
                _disc(d, Fp, 0.05 * u, shade2, dark, ow)

        def pad(i):
            s, e, _, _ = J["arms"][i]
            S_, E = P(s), P(e)
            near = i == 1
            c = (S_[0] + (E[0] - S_[0]) * 0.1, S_[1] + (E[1] - S_[1]) * 0.1 - 0.01 * u)
            _cap(d, c, (2 * c[0] - E[0], 2 * c[1] - E[1]), (0.09 if near else 0.08) * u, shade if near else shade2, dark, ow,
                 light=body if near else None, band=dark, flat=0.8)

        arm(0)
        pad(0)
        leg(0)
        _shape(d, [T(-0.11, -0.03), T(0.09, -0.03), T(0.13, 0.12), T(0.11, 0.28), T(-0.12, 0.29), T(-0.16, 0.13)], body, dark, ow)   # torse
        d.polygon([T(-0.09, 0.16), T(0.11, 0.15), T(0.095, 0.26), T(-0.1, 0.27)], fill=light)
        d.polygon([T(-0.11, -0.03), T(0.09, -0.03), T(0.105, 0.05), T(-0.13, 0.05)], fill=shade)
        d.line([T(-0.13, 0.12), T(0.12, 0.12)], fill=shade, width=int(0.012 * u))
        _disc(d, T(0.045, 0.13), 0.042 * u, (255, 190, 60, 255), dark, ow)                            # voyant
        _disc(d, T(0.036, 0.142), 0.016 * u, (255, 250, 210, 255))
        leg(1)
        hx, hy = P(J["head"])
        r = 0.12 * u
        rot = math.radians(J["lean"])
        c_, s_ = math.cos(rot), math.sin(rot)

        def Hh(x, y):
            return hx + (x * c_ - y * s_) * r, hy + (x * s_ + y * c_) * r
        d.line([Hh(-0.45, -0.8), Hh(-0.8, -1.45)], fill=dark, width=int(0.018 * u))                 # antenne
        _disc(d, Hh(-0.8, -1.45), 0.02 * u, (255, 70, 50, 255))
        helm = [Hh(-0.95, 0.75), Hh(-1.0, -0.2), Hh(-0.75, -0.8), Hh(-0.2, -1.02), Hh(0.45, -0.95), Hh(0.92, -0.55), Hh(1.05, 0.0), Hh(1.0, 0.72)]
        _shape(d, helm, body, dark, ow)
        d.polygon([Hh(-0.8, -0.2), Hh(-0.62, -0.68), Hh(-0.15, -0.88), Hh(0.42, -0.82), Hh(0.7, -0.55), Hh(0.1, -0.5), Hh(-0.45, -0.3)], fill=light)
        _shape(d, [Hh(-0.1, -0.38), Hh(1.12, -0.36), Hh(1.14, 0.12), Hh(-0.05, 0.14)], dark, None, 0)       # visière
        d.polygon([Hh(0.1, -0.24), Hh(1.02, -0.22), Hh(1.02, 0.0), Hh(0.12, 0.02)], fill=(255, 50, 40, 255))
        d.polygon([Hh(0.3, -0.2), Hh(0.7, -0.19), Hh(0.7, -0.12), Hh(0.3, -0.13)], fill=(255, 200, 180, 255))
        _shape(d, [Hh(0.2, 0.2), Hh(1.02, 0.2), Hh(0.98, 0.72), Hh(0.25, 0.75)], shade, dark, ow)          # grille
        for k in range(4):
            x = 0.38 + k * 0.17
            d.line([Hh(x, 0.3), Hh(x, 0.64)], fill=dark, width=max(1, int(0.01 * u)))
        _disc(d, Hh(-0.45, 0.25), 0.3 * r, shade, dark, ow)
        arm(1)
        pad(1)
    return fn


# the walking machine: a fat body on two long legs, a glass cockpit with its robot pilot, two fans, a cannon
MECH_FANS = ((0.3, 0.27, 0.15), (0.33, 0.5, 0.165))     # far fan, near fan: centre x, y, radius (share of the width, facing right)
MECH_MUZZLE = (0.985, 0.585)


def mech_draw(tint, frame):
    """Big walking machine drawn facing right: a round armoured body with hazard stripes, a glass cockpit with its robot
    pilot, the housings of two fans (their blades are drawn apart and turn), long bird legs, a cannon under the nose.
    Frames 0 and 1 walk, 2 hit, 3 fire. / Grosse machine qui marche : cockpit vitré, deux turbines, pattes d'oiseau."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1.0, 0.009 * W)
        body, light = tint + (255,), _mix(tint, WHITE, 0.45) + (255,)
        shade, shade2 = _mix(tint, (0, 0, 0), 0.3) + (255,), _mix(tint, (0, 0, 0), 0.5) + (255,)
        metal, metal_d = (110, 114, 130, 255), (70, 72, 86, 255)
        lean = {2: -0.02, 3: -0.012}.get(frame, 0.0) * W
        bob = {0: 0.0, 1: 0.012, 2: 0.0, 3: 0.0}[frame] * H
        fx, fy, fr = MECH_FANS[0]                                                        # turbine du fond (ses pales tournent dessous)
        c = (fx * W + lean, fy * H + bob)
        d.ellipse([c[0] - fr * W * 1.12, c[1] - fr * W * 1.12, c[0] + fr * W * 1.12, c[1] + fr * W * 1.12], outline=dark, width=int(fr * W * 0.3))
        d.ellipse([c[0] - fr * W * 1.06, c[1] - fr * W * 1.06, c[0] + fr * W * 1.06, c[1] + fr * W * 1.06], outline=shade2,
                  width=int(fr * W * 0.14))
        hip = (W * 0.52 + lean, H * 0.62 + bob)
        legs = {0: ((0.66, 0.74, 0.5), (0.4, 0.78, 0.66)), 1: ((0.58, 0.76, 0.6), (0.5, 0.76, 0.56)),
                2: ((0.64, 0.75, 0.5), (0.42, 0.78, 0.64)), 3: ((0.7, 0.74, 0.48), (0.4, 0.78, 0.66))}[frame]
        for i, (kx, ky, ax) in enumerate(legs):                                          # pattes d'oiseau
            near = i == 1
            knee = (W * kx + lean * 0.5, H * ky + bob * 0.5)
            ankle = (W * ax, H * 0.9)
            _capsule(d, hip, knee, 0.075 * W, 0.055 * W, shade if not near else body, dark, ow)
            _capsule(d, knee, ankle, 0.045 * W, 0.04 * W, metal_d if not near else metal, dark, ow)
            _disc(d, knee, 0.04 * W, metal_d, dark, ow)
            for t in (-0.07, 0.0, 0.08):                                                 # trois doigts
                _capsule(d, ankle, (ankle[0] + t * W, H * 0.975), 0.025 * W, 0.02 * W, dark)
            _disc(d, ankle, 0.028 * W, metal_d if not near else metal, dark, ow)
        cx, cy = W * 0.52 + lean, H * 0.42 + bob                                         # corps
        rx, ry = W * 0.32, H * 0.2
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=body, outline=dark, width=int(ow * 1.5))
        d.chord([cx - rx * 0.92, cy - ry * 0.9, cx + rx * 0.9, cy + ry * 0.35], 180, 360, fill=light)
        d.chord([cx - rx, cy - ry * 0.2, cx + rx, cy + ry], 20, 160, fill=shade)
        sx0, sy0, sx1, sy1 = cx - rx * 0.05, cy - ry * 0.18, cx + rx * 0.55, cy + ry * 0.08          # plaque à bandes
        d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=ry * 0.08, fill=dark)
        k = 0
        while sx0 + k * rx * 0.13 < sx1:
            x0 = sx0 + k * rx * 0.13
            d.polygon([(max(sx0, x0), sy0 + ry * 0.04), (min(sx1, x0 + rx * 0.065), sy0 + ry * 0.04), (min(sx1, x0 + rx * 0.065 - rx * 0.08), sy1 - ry * 0.04),
                       (max(sx0, x0 - rx * 0.08), sy1 - ry * 0.04)], fill=(255, 210, 60, 255))
            k += 1
        for k in (-0.35, 0.15, 0.65):                                                    # rivets
            _disc(d, (cx + rx * k, cy - ry * 0.55), 0.008 * W, shade2)
        gy = MECH_MUZZLE[1] * H + bob                                                    # canon sous le nez
        _capsule(d, (cx + rx * 0.4, gy), (MECH_MUZZLE[0] * W - 0.03 * W + lean, gy), 0.05 * H, 0.045 * H, metal, dark, ow)
        d.rectangle([MECH_MUZZLE[0] * W - 0.06 * W + lean, gy - 0.035 * H, MECH_MUZZLE[0] * W - 0.035 * W + lean, gy + 0.035 * H], fill=dark)
        _disc(d, (MECH_MUZZLE[0] * W - 0.02 * W + lean, gy), 0.022 * H, (255, 140, 60, 255) if frame == 3 else dark)
        _shape(d, [(cx + rx * 0.2, cy + ry * 0.55), (cx + rx * 0.62, cy + ry * 0.3), (cx + rx * 0.66, gy - cy + cy - 0.01 * H),
                   (cx + rx * 0.3, gy + 0.02 * H)], metal_d, dark, ow)                   # support du canon
        kx, ky, kr = cx + rx * 0.42, cy - ry * 0.62, W * 0.12                           # cockpit
        d.chord([kx - kr, ky - kr, kx + kr, ky + kr], 180, 360, fill=(120, 200, 240, 255), outline=dark, width=int(ow * 1.4))
        px, py = kx - kr * 0.05, ky - kr * 0.35                                          # le pilote robot
        _disc(d, (px, py), kr * 0.38, (96, 100, 118, 255), dark, ow)
        d.rounded_rectangle([px + kr * 0.02, py - kr * 0.12, px + kr * 0.36, py + kr * 0.06], radius=kr * 0.06, fill=(255, 52, 40, 255))
        d.chord([kx - kr * 0.92, ky - kr * 0.92, kx + kr * 0.92, ky + kr * 0.92], 200, 250, fill=(220, 245, 255, 200))
        d.rectangle([kx - kr * 1.05, ky - 0.012 * H, kx + kr * 1.05, ky + 0.01 * H], fill=shade2)
        fx, fy, fr = MECH_FANS[1]                                                        # turbine de devant, sur un bras
        c = (fx * W + lean, fy * H + bob)
        _capsule(d, (cx - rx * 0.3, cy + ry * 0.1), c, 0.06 * W, 0.05 * W, metal_d, dark, ow)
        _disc(d, c, fr * W * 1.14, light, dark, ow * 1.5)
        _disc(d, c, fr * W * 0.98, (26, 26, 36, 255), shade2, ow)
        for a in range(0, 360, 30):                                                      # grille de la turbine
            t = math.radians(a)
            d.line([(c[0] + math.cos(t) * fr * W * 0.98, c[1] + math.sin(t) * fr * W * 0.98),
                    (c[0] + math.cos(t) * fr * W * 1.1, c[1] + math.sin(t) * fr * W * 1.1)], fill=shade, width=max(1, int(ow)))
    return fn


def fan_draw(d, W, H):
    """Blades of a fan in its dark housing, turned by the scene. / Pales d'une turbine, que la scène fait tourner."""
    cx, cy, r = W / 2, H / 2, W / 2
    _disc(d, (cx, cy), r, (24, 24, 34, 255))
    for i in range(5):
        a = i * math.tau / 5
        pts = []
        for k in range(7):
            t = k / 6
            rr = r * (0.2 + 0.78 * t)
            aa = a + 0.55 * t - 0.25 + 0.25 * math.sin(t * math.pi)
            pts.append((cx + math.cos(aa) * rr, cy + math.sin(aa) * rr))
        for k in range(6, -1, -1):
            t = k / 6
            rr = r * (0.2 + 0.78 * t)
            aa = a + 0.55 * t + 0.12
            pts.append((cx + math.cos(aa) * rr, cy + math.sin(aa) * rr))
        d.polygon(pts, fill=(196, 202, 216, 240), outline=(60, 62, 76, 255))
    _disc(d, (cx, cy), r * 0.24, (232, 184, 64, 255), (60, 50, 30, 255), max(1, W * 0.02))
    _disc(d, (cx - r * 0.06, cy - r * 0.06), r * 0.08, (255, 236, 170, 255))


def badge_draw(suit, trim):
    """The hunter's head in a frame, for the panels at the top. / La tête du chasseur dans un cadre."""
    def fn(d, W, H):
        d.rounded_rectangle([0, 0, W - 1, H - 1], radius=W * 0.18, fill=(18, 20, 34, 240), outline=_mix(trim, WHITE, 0.25) + (255,),
                            width=max(2, int(W * 0.05)))
        d.rounded_rectangle([W * 0.2, H * 0.8, W * 0.8, H - W * 0.05], radius=W * 0.06, fill=_mix(suit, (0, 0, 0), 0.3) + (255,))
        _hunter_head(d, W * 0.43, H * 0.5, W * 0.25, 0.0, suit, trim, DARK + (255,), max(1.0, W * 0.025))
    return fn


class TopHunterScene(GameScene):
    """Two space hunters fight robots and walking machines on the two lanes of a planet, as big as in the game: they
    punch, jump from one lane to the other, throw their enemies, shoot when they are far, and the full power gauge that
    empties is a special move. When the timer starts again for a new stage, the planet changes. At the top, as in the
    game: the hunter's head, 1UP= and the lives, the score and the power on each side, TIME next to the logo.
    / Deux chasseurs se battent contre des robots et des machines sur les deux voies d'une planète, aussi grands que
    dans le jeu. En haut comme dans le jeu : la tête du chasseur, 1UP=, le score et la puissance, TIME."""
    THEME = TH_WORLDS[0]
    WORLDS = TH_WORLDS
    SHADE = (40, 30)
    EXPLOSIONS = True
    PILLS = True
    BANNERS = GameScene.BANNERS + (("COUP SPÉCIAL !", GOLD), ("SPECIAL MOVE!", GOLD))
    SUIT = {"p1": ((222, 82, 50), (255, 206, 72)), "p2": ((48, 128, 222), (126, 238, 206))}
    HOME = {"p1": 0.25, "p2": 0.34}
    BOT = {"th_forest": (176, 184, 198), "th_ice": (110, 122, 156), "th_wind": (176, 150, 118), "th_fire": (150, 160, 178)}
    MECH = {"th_forest": (230, 116, 60), "th_ice": (90, 160, 220), "th_wind": (210, 80, 84), "th_fire": (120, 186, 110)}
    HERO_H, BOT_H, MECH_H = 262, 200, 300          # heights of the pictures on the front lane / hauteurs des images devant
    REACH = {"bot": 150, "mech": 205}              # distance of a robot in front of the hunter who hits it
    HALF = {"bot": 70, "mech": 130}                # half width of a robot when they queue up / demi-largeur dans la file

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        W = self.W
        self.world = self.THEME
        self.heroes = {side: {"x": W * self.HOME[side], "lane": 1 if side == "p1" else 0, "in": False, "jump": None, "punch": -99.0,
                              "throw": -99.0, "hurt": -99.0, "super": -99.0, "upper": -99.0, "combo": 0, "btn": 0, "next": 0.0, "run": 0.0}
                       for side in ("p1", "p2")}
        self.enemies = []
        self.next_enemy = 0.0
        self.lost = -99.0
        self.started = -99.0
        self.kills = 0                                         # enemies defeated (tests)
        self.supers = 0                                        # special moves (tests)
        self.planets = 0                                       # planet changes (tests)
        first = [(self.hero_img, (side, f, lane)) for side in ("p1", "p2") for f in range(8) for lane in (0, 1)]
        self.warm = first + self.robots_warm(self.THEME) + self.warm         # the figures first, then the explosions

    def robots_warm(self, world):
        """The pictures of a planet's robots, to prepare before they come. / Les images des robots d'une planète."""
        return [(self.enemy_img, (kind, f, lane, tint)) for kind, tint in (("bot", self.BOT[world]), ("mech", self.MECH[world]))
                for f in range(4) for lane in (0, 1)]

    # ------------------------------------------------------------ outils
    def feet(self, lane):
        return self.H - self.S(TH_FEET[0] if lane == 0 else TH_FEET[1])

    @staticmethod
    def scale(lane):
        return 0.78 if lane == 0 else 1.0

    def hero_img(self, side, frame, lane):
        S, k = self.S, self.scale(lane)
        suit, trim = self.SUIT[side]
        return self.img(("hunter", side, frame, lane), S(TH_BOX[0] * self.HERO_H * k), S(self.HERO_H * k), hunter_draw(suit, trim, frame), ss=2)

    def enemy_img(self, kind, frame, lane, tint):
        """Robots are drawn facing right and turned round: they come from the right. / Les robots regardent vers la gauche."""
        S, k = self.S, self.scale(lane)
        if kind == "mech":
            return self.img(("mech", frame, lane, tint), S(self.MECH_H * k), S(self.MECH_H * k), mech_draw(tint, frame), ss=2, flip=True)
        return self.img(("bot", frame, lane, tint), S(BOT_BOX[0] * self.BOT_H * k), S(self.BOT_H * k), bot_draw(tint, frame), ss=2, flip=True)

    def fan_img(self, r, angle):
        size = max(8, int(2 * r) // 4 * 4)
        base = self.img(("fan", size), size, size, fan_draw)
        return self.rotated(("fan", size), base, angle, 15)

    def hero_pos(self, side, now):
        """(x, feet y, scale) of a hunter, during a jump from one lane to the other too."""
        P = self.heroes[side]
        dash = P.get("dash")
        if dash is not None:                                           # quick dash towards a robot
            q = (now - dash[0]) / dash[3]
            if q >= 1.0:
                P["x"], P["dash"] = dash[2], None
            else:
                P["x"] = _lerp(dash[1], dash[2], q)
        j = P["jump"]
        if j is None:
            return P["x"], self.feet(P["lane"]), self.scale(P["lane"])
        t0, a, b, dur = j
        k = _clamp((now - t0) / dur)
        y = _lerp(self.feet(a), self.feet(b), k) - math.sin(k * math.pi) * self.S(120)
        return P["x"], y, _lerp(self.scale(a), self.scale(b), k)

    def fist(self, side, frame, now):
        """Where the fist of the hunter is on the screen in this frame. / Où est le poing du chasseur à l'écran."""
        x, y, k = self.hero_pos(side, now)
        fx, fy = th_hunter_point(frame, "fist")
        w, h = self.S(TH_BOX[0] * self.HERO_H * k), self.S(self.HERO_H * k)
        return x + (fx - TH_ANCHOR) * w, y - h + fy * h

    def ex(self, e):
        return e["wx"] - self.bd.scroll

    def alive(self):
        return [e for e in self.enemies if e["dead"] is None and e["thrown"] is None and not e.get("grabbed")]

    def fighting(self):
        return any(self.ex(e) < self.W * 0.62 for e in self.alive())

    def move(self, vals, now, idle):
        if idle:
            return 0.1
        return -0.72 if self.fighting() else 0.75

    # ------------------------------------------------------------ monde
    def always(self, vals, now):
        name = self.world
        if name == self.bd.theme:
            return
        if self.bd.warm(name):                                         # built in the background, converted bit by bit
            old = self.bd.theme
            self.bd.set_theme(name, now, wipe=0 if self.bd.last is None else 1.2)
            with self.bd.lock:                                         # only one planet kept in memory
                self.bd.raw.pop(old, None)
            self.bd.built.pop(old, None)

    def next_planet(self, now):
        """A new stage: the hunters run on to the next planet. / Un nouveau stage : la planète suivante."""
        i = self.WORLDS.index(self.world) if self.world in self.WORLDS else 0
        self.world = self.WORLDS[(i + 1) % len(self.WORLDS)]
        self.bd.prebuild([self.world])                                 # one thread, the display goes on meanwhile
        self.warm = self.robots_warm(self.world) + self.warm           # its robots are drawn before they come
        self.planets += 1
        for e in self.alive():                                         # the robots left behind vanish
            e["gone"] = True
            self.fx.smoke(self.ex(e), self.feet(e["lane"]) - self.S(80), 5, (16, 30), 2.2, (0.5, 0.9), (20, 50), 30, (150, 150, 160), 150,
                          "front")
        self.boost = (2.6, now + 2.2)
        self.next_enemy = now + 2.5

    def restart(self, vals, now):
        self.enemies = []
        self.next_enemy = now + 0.8
        self.started = now
        for P in self.heroes.values():
            P["in"] = False
            P["jump"] = None

    # ------------------------------------------------------------ combat
    def spawn(self, now):
        lane = self.rng.choice((0, 1))
        mech = not any(e["kind"] == "mech" for e in self.alive()) and self.rng.random() < 0.3
        e = {"kind": "mech" if mech else "bot", "lane": lane, "wx": self.bd.scroll + self.W + self.S(150), "hp": 6 if mech else 2,
             "hit": -99.0, "dead": None, "thrown": None, "strike": -99.0, "ph": self.rng.uniform(0, 6),
             "v": self.rng.uniform(300, 360) * self.s if mech else self.rng.uniform(560, 680) * self.s,
             "tint": (self.MECH if mech else self.BOT).get(self.world, (160, 170, 186))}
        self.enemies.append(e)

    def stops(self):
        """Where each robot stops: in front of the hunters, one behind the other on its lane. / Où chaque robot s'arrête."""
        front = max((P["x"] for P in self.heroes.values() if P["in"]), default=self.W * 0.25)
        out = {}
        S = self.S
        for lane in (0, 1):
            k = self.scale(lane)
            x, prev = front, None
            for e in sorted((e for e in self.alive() if e["lane"] == lane), key=lambda e: e["wx"]):
                x += S(self.REACH[e["kind"]] if prev is None else self.HALF[prev["kind"]] + self.HALF[e["kind"]]) * k
                out[id(e)] = x
                prev = e
        return out

    def target(self, side):
        P = self.heroes[side]
        near = [e for e in self.alive() if self.ex(e) < self.W - self.S(60)]
        if not near:
            return None
        same = [e for e in near if e["lane"] == P["lane"]]
        return min(same or near, key=lambda e: self.ex(e))

    def jump(self, side, lane, now):
        P = self.heroes[side]
        if P["jump"] is not None:
            return
        P["jump"] = (now, P["lane"], lane, 0.42)
        self.fx.later(0.42, self.land, side)

    def land(self, side):
        P = self.heroes[side]
        if P["jump"] is not None:
            P["lane"] = P["jump"][2]
            P["jump"] = None
            x, y, k = self.hero_pos(side, self.fx.now)
            self.fx.smoke(x, y, 4, (10, 18), 2.0, (0.3, 0.6), (10, 30), 30, (150, 140, 130), 120, "back")

    def attack(self, side, now=None, dmg=1, tries=0):
        """A blow at the nearest robot; the hunter jumps to the other lane first if the robot is there, rushes at it when
        it is a little far, walks to meet it when it is still coming, shoots when it stays far.
        / Un coup au robot le plus proche ; saute, fonce, va à sa rencontre, ou tire s'il reste loin."""
        now = self.fx.now if now is None else now
        P = self.heroes[side]
        e = self.target(side)
        if e is None or P["jump"] is not None:
            return False
        if e["lane"] != P["lane"]:
            self.jump(side, e["lane"], now)
            self.fx.later(0.46, self.attack, side, None, dmg, tries)
            return True
        S, fx = self.S, self.fx
        k = self.scale(e["lane"])
        reach = S(self.REACH[e["kind"]]) * k
        gap = self.ex(e) - P["x"]
        if gap > reach + S(10):
            if P["x"] + gap - reach <= self.W * 0.6:                   # a quick rush forward first
                if P.get("dash") is None:
                    dur = min(0.24, 0.1 + (gap - reach) / (4000 * self.s))
                    P["dash"] = (now, P["x"], P["x"] + gap - reach, dur)
                    fx.later(dur + 0.01, self.attack, side, None, dmg, tries)
                return True
            if tries < 3:                                              # still coming: walk to meet it
                P["dash"] = (now, P["x"], min(self.W * 0.5, P["x"] + S(90)), 0.25)
                fx.later(0.26, self.attack, side, None, dmg, tries + 1)
                return True
            P["punch"] = now                                           # it stays far: a blaster shot
            mx, my = self.fist(side, 3, now)
            ty = self.feet(e["lane"]) - S(110 if e["kind"] == "bot" else 170) * k
            fx.muzzle(mx, my, 1, 0.9 * k, (140, 230, 255))
            fx.tracer(mx, my, self.ex(e), ty, 4200, (150, 230, 255), 8, 200, "front", True)
            fx.later(gap / (4200 * self.s), self.shot_hit, e, dmg)
            return True
        P["combo"] += 1
        if P["combo"] % 4 == 0 and e["kind"] == "bot":                 # grab and throw
            P["throw"] = now
            e["hp"], e["grabbed"] = 0, True                            # nobody else aims at it while it is lifted
            fx.later(0.12, self.throw_enemy, e, side)
            return True
        upper = P["combo"] % 4 == 2
        if upper:
            P["upper"] = now
        else:
            P["punch"] = now
        hx, hy = self.fist(side, 7 if upper else 3, now)
        hx += S(30) * k
        fx.glow(hx, hy, 16, 130 * k, (255, 236, 180), 0.2, "front", 1.0, 0.0, hot=0.8)
        fx.sparks(hx, hy, 16, (255, 220, 140), (300, 1000), (-80, -10) if upper else (-40, 40), (0.15, 0.35), 500, "front", 4, 40)
        star = fx.add(Particle("star", hx, hy, now, 0.14, "front"))
        star.r0, star.r1, star.col, star.a0, star.a1, star.data = S(54) * k, S(84) * k, (255, 240, 200), 1.0, 0.2, self.rng.randint(0, 3)
        fx.shake(4.0 if not upper else 5.5, 0.14)
        e["hp"] -= dmg
        e["hit"] = now
        if e["hp"] <= 0:
            self.knock(e, now, upper)
        return True

    def shot_hit(self, e, dmg):
        if e["dead"] is not None or e["thrown"] is not None:
            return
        now = self.fx.now
        e["hp"] -= dmg
        e["hit"] = now
        if e["hp"] <= 0:
            self.knock(e, now)

    def knock(self, e, now, upper=False):
        """The robot flies back (or up after an uppercut) and blows up. / Le robot vole en arrière (ou en l'air) et explose."""
        e["dead"] = now
        e["fly"] = (self.ex(e), self.feet(e["lane"]), 1.0 if upper else 0.0)
        self.kills += 1
        k = self.scale(e["lane"])
        self.fx.later(0.5, self._boom, e, 1.05 * k if e["kind"] == "mech" else 0.6 * k)

    def throw_enemy(self, e, side=None):
        """The hunter lifts the robot over his head and throws it far ahead. / Le chasseur soulève le robot et le jette au loin."""
        now = self.fx.now
        x0, k = self.ex(e), self.scale(e["lane"])
        hx = self.hero_pos(side, now)[0] if side in self.heroes else x0 - self.S(150) * k
        e["thrown"] = (now, x0, self.feet(e["lane"]), hx + self.S(10) * k, self.feet(e["lane"]) - self.S(205) * k, x0 + self.S(480) * k,
                       self.feet(e["lane"]))
        self.kills += 1
        self.fx.later(0.75, self._boom, e, 0.7 * k)

    def _boom(self, e, size):
        if e.get("gone"):
            return
        e["gone"] = True
        x, y = e.get("bx", self.ex(e)), e.get("by", self.feet(e["lane"]) - self.S(90))
        self.fx.explosion(x, y, size, layer_back=False)
        self.bd.excite(0.3)

    def special(self, side, now, level):
        """Special move: the hunter shines, a wave of fire runs along the two lanes, every robot blows up.
        / Coup spécial : une vague de feu sur les deux voies, tous les robots explosent."""
        P = self.heroes[side]
        P["super"] = now
        S, fx = self.S, self.fx
        x, y, k = self.hero_pos(side, now)
        fx.glow(x, y - S(130) * k, 60, 340 * level, (255, 200, 90), 0.6, "front", 1.0, 0.0, hot=0.6)
        for lane in (0, 1):
            ly = self.feet(lane) - S(90) * self.scale(lane)
            for i in range(3):
                fx.later(i * 0.06, fx.tracer, x + S(80), ly + (i - 1) * S(26), self.W + S(300), ly + (i - 1) * S(26), 2600, (255, 160, 60), 26,
                         560, "front", False)
        fx.flash((255, 180, 90), 0.3 * level, 0.35)
        fx.shake(8, 0.45)
        for e in self.alive():
            e["hp"] = 0
            e["dead"] = now + max(0.0, self.ex(e) - x) / (2600 * self.s)
            e["fly"] = (self.ex(e), self.feet(e["lane"]), 0.5)
            self.kills += 1
            fx.later(max(0.0, e["dead"] - now) + 0.1, self._boom, e, 0.85 * self.scale(e["lane"]))
        self.slam(tr("COUP SPÉCIAL !", "SPECIAL MOVE!"), GOLD, now, 1.3)
        self.supers += 1

    def hurt(self, side, now):
        P = self.heroes[side]
        P["hurt"] = now
        self.lost = now
        x, y, k = self.hero_pos(side, now)
        fx = self.fx
        fx.flash((150, 0, 0), 0.14, 0.25)
        fx.shake(6, 0.3)
        fx.sparks(x, y - self.S(150) * k, 18, (255, 120, 90), (200, 700), (180, 360), (0.2, 0.5), 600, "front", 4, 28)
        e = self.target(side)
        if e is not None:
            e["strike"] = now
        self.popup(tr("-1 VIE", "-1 LIFE"), x, y - self.S(290) * k, RED, 40)

    # ------------------------------------------------------------ chaque image
    def update(self, vals, now):
        S, dt = self.S, self.dt
        ch = self.changed(vals, "time")
        if ch and ch[1] > ch[0] + 4 and now - self.lost > 4.0 and now - self.started > 5.0:     # the timer starts again
            self.next_planet(now)
        for side, suf in (("p1", ""), ("p2", "_p2")):
            P = self.heroes[side]
            playing = self.p1_in(vals) if side == "p1" else self.p2_in(vals)
            if not playing:
                P["in"] = False
                continue
            if not P["in"]:
                P["in"], P["x"] = True, self.W * self.HOME[side]
            ch = self.changed(vals, "lives" + suf)
            if ch and ch[1] < ch[0]:
                self.hurt(side, now)
            elif ch and ch[1] > ch[0]:
                x, y, k = self.hero_pos(side, now)
                self.popup("1UP !", x, y - S(290) * k, (140, 255, 150), 44)
            ch = self.changed(vals, "power" + suf)
            if ch and ch[0] >= 4 and ch[1] <= ch[0] - 2:
                self.special(side, now, _clamp(ch[0] / 5.0, 0.5, 1.0))
            ch = self.changed(vals, "score" + suf)
            if ch and ch[1] > ch[0]:
                self.attack(side, now, 2)
            st = self.stick(vals, side)
            if st is not None:                                         # the player's stick and buttons
                dx, dy, btn = st
                if P["jump"] is None:
                    P["x"] = _clamp(P["x"] + dx * dt * S(440), S(130), self.W * 0.62)
                    want = 0 if dy < 0 else (1 if dy > 0 else P["lane"])
                    if want != P["lane"]:
                        self.jump(side, want, now)
                press = btn & ~P["btn"]
                P["btn"] = btn
                if press & BTN_A:
                    self.attack(side, now)
                if press & BTN_B:
                    self.jump(side, P["lane"], now)
            elif P.get("dash") is None and now - P["punch"] > 0.5 and now - P["throw"] > 0.6:
                P["x"] += (self.W * self.HOME[side] - P["x"]) * min(1.0, dt * 1.5)
            if st is None and _n(vals.get("score" + suf)) is None and now >= P["next"]:      # score not learned: blows now and then
                P["next"] = now + self.rng.uniform(0.8, 1.8)
                self.attack(side, now)
        if now >= self.next_enemy:
            self.next_enemy = now + self.rng.uniform(0.9, 1.8)
            if len(self.alive()) < 4:
                self.spawn(now)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, dt = self.S, self.dt
        stops = self.stops()
        items = []
        self.enemies = [e for e in self.enemies if not e.get("gone") and self.ex(e) > -S(400)]
        for e in self.enemies:
            if e["dead"] is None and e["thrown"] is None:
                stop = stops.get(id(e), self.W)
                walking = self.ex(e) > stop + 1
                if walking:
                    e["wx"] -= min(e["v"] * dt, self.ex(e) - stop)
                if now - e["strike"] > 2.5 and not walking and self.rng.random() < dt * 0.4:
                    e["strike"] = now
                e["walk"] = walking
            items.append((e["lane"], 0, -self.ex(e), e))
        for side in ("p1", "p2"):
            if self.heroes[side]["in"]:
                P = self.heroes[side]
                lane = P["lane"] if P["jump"] is None else P["jump"][2]
                items.append((lane, 1, 0, side))
        for lane, kind, _, it in sorted(items, key=lambda t: (t[0], t[1], t[2])):
            if kind == 0:
                self.draw_enemy(screen, it, now)
            else:
                self.draw_hero(screen, it, now)
        self.draw_status(screen, eng, vals, logo, now)

    def draw_enemy(self, screen, e, now):
        S, pg = self.S, self.pg
        k = self.scale(e["lane"])
        mech = e["kind"] == "mech"
        if e["thrown"] is not None:                                    # lifted over the hunter's head, then thrown, spinning
            t0, xs, ys, xh, yh, x1, y1 = e["thrown"]
            img = self.enemy_img(e["kind"], 2, e["lane"], e["tint"])
            q = (now - t0) / 0.75
            if q < 0.2:                                                # soulevé
                a = q / 0.2
                x, y = _lerp(xs, xh, a), _lerp(ys - img.get_height() / 2, yh, a)
                ang = -20 * a
            else:
                a = _clamp((q - 0.2) / 0.8)
                x = _lerp(xh, x1, a)
                y = _lerp(yh, y1 - S(60) * k, a) - math.sin(a * math.pi) * S(150) * k
                ang = -20 - a * 520
            e["bx"], e["by"] = x, y
            img = self.rotated(("thr", e["kind"], e["lane"], e["tint"]), img, ang, 15)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
            return
        if e["dead"] is not None:                                      # knocked back, or up after an uppercut
            q = (now - e["dead"]) / 0.5
            img = self.enemy_img(e["kind"], 2, e["lane"], e["tint"])
            if q < 0:
                x, y = self.ex(e), self.feet(e["lane"])
                screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height())))
                return
            x0, y0, up = e.get("fly", (self.ex(e), self.feet(e["lane"]), 0.0))
            q = min(1.0, q)
            x = x0 + S(320 - 200 * up) * q * k
            y = y0 - math.sin(q * math.pi * 0.9) * S(150 + 260 * up) * k
            e["bx"], e["by"] = x, y - img.get_height() * 0.45
            img = self.rotated(("ko", e["kind"], e["lane"], e["tint"]), img, -q * (200 + 300 * up), 10)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height())))
            return
        x, y = self.ex(e), self.feet(e["lane"])
        if now - e["strike"] < 0.3:
            frame = 3
        elif now - e["hit"] < 0.18:
            frame = 2
        elif e.get("walk"):
            frame = int(now * (5 if mech else 6) + e["ph"]) % 2
        else:
            frame = int(now * 1.6 + e["ph"]) % 2
        img = self.enemy_img(e["kind"], frame, e["lane"], e["tint"])
        w, h = img.get_width(), img.get_height()
        x0 = x - w * (0.5 if mech else 0.58)                           # turned round: the robot's anchor moves
        y0 = y - h
        if frame == 3:                                                 # fires its gun
            mx, my = MECH_MUZZLE if mech else bot_muzzle(3)
            self.fx.muzzle(x0 + (1 - mx) * w, y0 + my * h, -1, (1.0 if mech else 0.7) * k, (255, 170, 90))
        sh = self.imgs.get(("esh", e["kind"], e["lane"]))
        if sh is None:
            sh = self.imgs[("esh", e["kind"], e["lane"])] = pg.Surface((int(w * (0.62 if mech else 0.66)), S(20 * k)), pg.SRCALPHA)
            pg.draw.ellipse(sh, (0, 0, 0, 90), sh.get_rect())
        screen.blit(sh, (int(x - sh.get_width() / 2), int(y - sh.get_height() / 2)))
        if mech:                                                       # the far fan turns behind the body
            fx_, fy_, fr = MECH_FANS[0]
            fan = self.fan_img(fr * w * 1.04, (now * 900 + e["ph"] * 50) % 360)
            screen.blit(fan, (int(x0 + (1 - fx_) * w - fan.get_width() / 2), int(y0 + fy_ * h - fan.get_height() / 2)))
        screen.blit(img, (int(x0), int(y0)))
        if mech:                                                       # and the near one in front
            fx_, fy_, fr = MECH_FANS[1]
            fan = self.fan_img(fr * w, (-now * 1100 + e["ph"] * 40) % 360)
            screen.blit(fan, (int(x0 + (1 - fx_) * w - fan.get_width() / 2), int(y0 + fy_ * h - fan.get_height() / 2)))
        if now - e["hit"] < 0.08:
            g = self.fx.sp.glow(S(80 * k), (255, 255, 255), 7, hot=0.6)
            screen.blit(g, (int(x - g.get_width() / 2), int(y - h * 0.5 - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)

    def draw_hero(self, screen, side, now):
        S, P = self.S, self.heroes[side]
        x, y, k = self.hero_pos(side, now)
        hurt = now - P["hurt"]
        if hurt < 1.4 and int(now * 14) % 2 == 0 and hurt > 0.3:      # blinking after a hit
            return
        if P["jump"] is not None:
            frame = 4
        elif hurt < 0.3:
            frame = 5
            x -= S(40) * (1 - hurt / 0.3)
        elif now - P["throw"] < 0.45:
            frame = 6
        elif now - P["upper"] < 0.2:
            frame = 7
        elif now - P["punch"] < 0.16:
            frame = 3
        elif self.bd.speed > 12 * self.s or now - P["super"] < 0.6 or P.get("dash") is not None:
            P["run"] += self.dt * 9
            frame = 1 + int(P["run"]) % 2
        else:
            frame = 0
        lane = 0 if k < 0.89 else 1
        img = self.hero_img(side, frame, lane)
        if abs(k - self.scale(lane)) > 0.01:
            img = self.pg.transform.smoothscale(img, (int(img.get_width() * k / self.scale(lane)), int(img.get_height() * k / self.scale(lane))))
        sh = self.imgs.get(("hsh", lane))
        if sh is None:
            kk = self.scale(lane)
            sh = self.imgs[("hsh", lane)] = self.pg.Surface((S(130 * kk), S(22 * kk)), self.pg.SRCALPHA)
            self.pg.draw.ellipse(sh, (0, 0, 0, 100), sh.get_rect())
        fy = self.feet(P["lane"] if P["jump"] is None else P["jump"][2])
        screen.blit(sh, (int(x - sh.get_width() / 2), int(fy - sh.get_height() / 2)))
        if now - P["super"] < 0.8:                                     # special move: the hunter shines
            g = self.fx.sp.glow(S(160 * k), (255, 190, 80), 9 * (1 - (now - P["super"]) / 0.8), hot=0.4)
            screen.blit(g, (int(x - g.get_width() / 2), int(y - S(130) * k - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
        screen.blit(img, (int(x - img.get_width() * TH_ANCHOR), int(y - img.get_height())))

    def draw_status(self, screen, eng, vals, logo, now):
        """As in the game: on each side the hunter's head, 1UP= and the lives, the score, the power; TIME next to the logo.
        / Comme dans le jeu : la tête du chasseur, 1UP= et les vies, le score, la puissance ; TIME à côté du logo."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(520), S(104), now)
        t = _n(vals.get("time"))
        if t is not None:
            low = t <= 10
            pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
            tx = W / 2 + S(380)
            self.pill(screen, tx - S(72), S(10), S(144), S(100), 160, radius=18)
            self.text(screen, "TIME", tx, S(32), 24, CREAM, key="black", align="center", valign="middle", glow=0.3)
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(52), RED if low else GOLD, tx, S(76), "center", "middle", scale=1 + 0.1 * pulse)
        for side in ("p1", "p2"):
            right = side == "p2"
            if right and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, W - S(24), S(56), 34, col, align="right")
                continue
            suf = "_p2" if right else ""
            lives, pw, sc = _n(vals.get("lives" + suf)), _n(vals.get("power" + suf)), _n(vals.get("score" + suf))
            if lives is None and pw is None and sc is None:
                continue
            suit, trim = self.SUIT[side]
            w = S(424)
            x = W - S(16) - w if right else S(16)
            self.pill(screen, x, S(8), w, S(140), 160, radius=18)
            bw = S(88)
            bx = x + w - S(10) - bw if right else x + S(10)
            badge = self.img(("badge", side), bw, bw, badge_draw(suit, trim))
            screen.blit(badge, (int(bx), S(16)))
            tx = bx - S(16) if right else bx + bw + S(16)
            al = "right" if right else "left"
            if lives is not None:                                      # 1UP=3 as in the game
                tag = ("2UP=" if right else "1UP=")
                if right:
                    nw = self.text(screen, str(int(lives)), tx, S(36), 32, WHITE, key="black", align="right", valign="middle")
                    self.text(screen, tag, tx - nw, S(36), 32, P2C, key="black", align="right", valign="middle")
                else:
                    tw_ = self.text(screen, tag, tx, S(36), 32, P1C, key="black", align="left", valign="middle")
                    self.text(screen, str(int(lives)), tx + tw_, S(36), 32, WHITE, key="black", align="left", valign="middle")
            if sc is not None:
                hd._score(screen, eng, "score" + suf, tx, S(54), al, S(52))
            if pw is not None:                                         # power: five segments under the head
                full = pw >= 5
                py = S(114)
                lab = self.text(screen, "POWER", (x + w - S(14)) if right else x + S(14), py + S(12), 20, CREAM, key="bold", align=al,
                                valign="middle", glow=0)
                for i in range(5):
                    on = i < int(pw)
                    col = _mix(GOLD, WHITE, 0.5 + 0.5 * math.sin(now * 10)) if full else ((255, 170, 60) if on else (60, 44, 24))
                    sx = (x + w - S(14) - lab - S(12) - (i + 1) * S(50) + S(6)) if right else (x + S(14) + lab + S(12) + i * S(50))
                    pg.draw.rect(screen, col, (int(sx), py, S(44), S(24)), border_radius=S(5))
                    if on:
                        pg.draw.rect(screen, (255, 240, 200), (int(sx) + S(6), py + S(4), S(32), S(6)), border_radius=S(2))


# ============================================================================ Baseball Stars 2
KITS = ({"jersey": (246, 244, 238), "trim": (220, 60, 46), "pants": (236, 234, 228), "cap": (200, 44, 36)},
        {"jersey": (150, 156, 170), "trim": (40, 90, 200), "pants": (170, 174, 186), "cap": (30, 60, 150)})
SKINS = ((236, 196, 160), (214, 160, 120), (170, 116, 80), (120, 80, 56))


def _ik(s, t, l1, l2, bend=1.0):
    """Elbow (or knee) of a limb from s to the target t, bones l1 and l2 long, bent on the side 'bend'.
    / Le coude d'un membre qui va de s vers t."""
    dx, dy = t[0] - s[0], t[1] - s[1]
    dist = math.hypot(dx, dy) or 1e-6
    d = min(dist, (l1 + l2) * 0.999)
    a = math.atan2(dy, dx)
    b = math.acos(_clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1.0, 1.0))
    e = (s[0] + math.cos(a + bend * b) * l1, s[1] + math.sin(a + bend * b) * l1)
    return e, (s[0] + dx * d / dist, s[1] + dy * d / dist)


# poses of the batter seen from the side, facing the plate (to the right): lean, legs (far, near) as (thigh, shin), the
# hands on the handle, the direction of the bat, the bat in front of the body or not.
# / Poses du frappeur de profil : inclinaison, jambes, les mains sur le manche, la direction de la batte.
BAT_POSES = {
    0: (8, ((-22, -6), (26, 4)), (-0.07, -0.35), (-0.58, -0.81), False),        # prêt, la batte levée derrière la tête
    1: (6, ((-34, -24), (14, 2)), (0.2, -0.17), (1.0, -0.06), True),            # la frappe
    2: (-2, ((-24, -46), (10, 2)), (0.06, -0.36), (-0.92, -0.38), False),       # fin du geste, la batte enroulée
    3: (16, ((-38, -72), (44, 6)), None, None, False),                          # course vers la première base
}


def batter_draw(kit, skin, frame):
    """Batter seen from the side, facing the plate (to the right), as tall as in the game's batting view: a helmet with
    its ear flap, the jersey and its number, white trousers, socks and cleats, the bat. Frames 0 ready, 1 swing,
    2 follow-through, 3 run. / Frappeur de profil, grand comme dans la vue de frappe du jeu : casque, maillot, batte."""
    def fn(d, W, H):
        lean, legs, hands, bat, bat_front = BAT_POSES[frame]
        u = H * 0.86 / 0.98                                                    # room above the head for the bat
        ox, oy = W * 0.5, H * 0.985 - 0.49 * u                                 # le bassin

        def P(p):
            return ox + p[0] * u, oy + p[1] * u
        dark = DARK + (255,)
        ow = max(1.0, 0.012 * u)
        jer, jer_d = kit["jersey"] + (255,), _mix(kit["jersey"], (0, 0, 0), 0.28) + (255,)
        jer_l = _mix(kit["jersey"], WHITE, 0.5) + (255,)
        pants, pants_d = kit["pants"] + (255,), _mix(kit["pants"], (0, 0, 0), 0.22) + (255,)
        trim, cap, cap_l = kit["trim"] + (255,), kit["cap"] + (255,), _mix(kit["cap"], WHITE, 0.4) + (255,)
        sk, sk_d = skin + (255,), _mix(skin, (0, 0, 0), 0.25) + (255,)
        wood, wood_l = (196, 146, 86, 255), (230, 190, 130, 255)
        F = _Frame(0.0, 0.0, 1.0, lean)

        def T(x, y):
            return P(F(x, y))
        hips = (F(-0.03, 0.0), F(0.03, 0.0))
        sh = (F(-0.035, 0.23), F(0.035, 0.225))
        head = F(0.03, 0.345)

        def leg(i):
            th, shin = legs[i]
            hip = hips[i]
            knee = _seg(hip, th, 0.23)
            ankle = _seg(knee, shin, 0.22)
            near = i == 1
            h, k, a = P(hip), P(knee), P(ankle)
            _capsule(d, h, k, 0.11 * u, 0.085 * u, pants if near else pants_d, dark, ow)
            _capsule(d, k, a, 0.075 * u, 0.06 * u, trim if near else _mix(kit["trim"], (0, 0, 0), 0.3) + (255,), dark, ow)    # chaussettes
            _capsule(d, k, (k[0] + (a[0] - k[0]) * 0.25, k[1] + (a[1] - k[1]) * 0.25), 0.082 * u, 0.074 * u, pants if near else pants_d)
            _boot(d, a, 0 if ankle[1] > -0.05 else -30, u * 0.9, (30, 30, 36, 255), (240, 240, 240, 255), dark, ow, length=0.13)

        def arm(i, hand):
            near = i == 1
            s = sh[i]
            el, hd = _ik(s, hand, 0.12, 0.12, -1.0 if bat is not None and bat[1] < 0 else 1.0)
            S_, E, Hh = P(s), P(el), P(hd)
            _capsule(d, S_, E, 0.07 * u, 0.06 * u, jer if near else jer_d, dark, ow)
            _capsule(d, E, Hh, 0.055 * u, 0.05 * u, sk if near else sk_d, dark, ow)
            _disc(d, Hh, 0.036 * u, (240, 240, 240, 255) if near else (200, 200, 206, 255), dark, ow)      # gant de frappe

        def draw_bat():
            hx, hy = hands
            bx, by = bat
            a, b = P((hx - bx * 0.04, hy - by * 0.04)), P((hx + bx * 0.42, hy + by * 0.42))
            _capsule(d, a, P((hx + bx * 0.22, hy + by * 0.22)), 0.022 * u, 0.03 * u, wood, dark, ow)
            _capsule(d, P((hx + bx * 0.2, hy + by * 0.2)), b, 0.03 * u, 0.05 * u, wood, dark, ow)
            _capsule(d, P((hx + bx * 0.25, hy + by * 0.25)), P((hx + bx * 0.39, hy + by * 0.39)), 0.01 * u, 0.016 * u, wood_l)

        if frame == 3:                                                           # course : les bras balancent
            far_hand, near_hand = _seg(_seg(sh[0], 50, 0.12), 130, 0.12), _seg(_seg(sh[1], -40, 0.12), 40, 0.12)
        else:
            far_hand = (hands[0] - bat[0] * 0.04, hands[1] - bat[1] * 0.04)
            near_hand = (hands[0] + bat[0] * 0.03, hands[1] + bat[1] * 0.03)
        arm(0, far_hand)
        leg(0)
        if bat is not None and not bat_front:
            draw_bat()
        torso = [T(-0.08, -0.02), T(0.075, -0.02), T(0.075, 0.08), T(0.105, 0.17), T(0.085, 0.245), T(-0.075, 0.25), T(-0.1, 0.16), T(-0.08, 0.06)]
        _shape(d, torso, jer, dark, ow)
        d.polygon([T(-0.06, 0.16), T(0.09, 0.17), T(0.075, 0.235), T(-0.06, 0.24)], fill=jer_l)
        d.line([T(0.07, 0.24), T(0.085, 0.02)], fill=trim, width=int(0.012 * u))                    # boutonnière
        _shape(d, [T(-0.085, -0.03), T(0.08, -0.03), T(0.08, 0.01), T(-0.085, 0.01)], (36, 36, 44, 255), None, 0)      # ceinture
        leg(1)
        hx, hy = P(head)                                                         # la tête et le casque
        r = 0.085 * u
        d.ellipse([hx - r * 0.7, hy - r * 0.4, hx + r * 1.0, hy + r * 1.05], fill=sk, outline=dark, width=int(ow))
        d.polygon([(hx + r * 0.9, hy + r * 0.1), (hx + r * 1.15, hy + r * 0.35), (hx + r * 0.9, hy + r * 0.45)], fill=sk)     # le nez
        d.ellipse([hx - r, hy - r, hx + r, hy + r * 0.55], fill=cap, outline=dark, width=int(ow))
        d.chord([hx - r * 0.85, hy - r * 0.9, hx + r * 0.7, hy + r * 0.2], 190, 320, fill=cap_l)
        d.rectangle([hx + r * 0.4, hy + r * 0.05, hx + r * 1.25, hy + r * 0.22], fill=cap)              # visière
        _disc(d, (hx - r * 0.2, hy + r * 0.32), r * 0.42, cap, dark, ow)                                # oreillette
        _disc(d, (hx - r * 0.2, hy + r * 0.32), r * 0.14, _mix(kit["cap"], (0, 0, 0), 0.4) + (255,))
        if bat is not None and bat_front:
            draw_bat()
        arm(1, near_hand)
    return fn


def pitcher_draw(kit, skin, frame):
    """Pitcher seen from the front on the mound. Frames 0 set, 1 leg up, 2 arm back, 3 release.
    / Lanceur vu de face : 0 prêt, 1 jambe levée, 2 bras armé, 3 lancer."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1, int(W * 0.035))
        jer, pants, cap, trim, sk = kit["jersey"] + (255,), kit["pants"] + (255,), kit["cap"] + (255,), kit["trim"] + (255,), skin + (255,)
        cx = W * 0.5
        hip = (cx, H * 0.58)
        legs = {0: ((-0.12, 0.98), (0.12, 0.98)), 1: ((-0.08, 0.98), (0.18, 0.62)), 2: ((-0.14, 0.98), (0.3, 0.96)),
                3: ((-0.28, 0.94), (0.16, 0.98))}[frame]
        for fx_, fy in legs:
            foot = (cx + fx_ * W, fy * H)
            knee = ((hip[0] + foot[0]) / 2 + (W * 0.12 if fy < 0.8 else 0), (hip[1] + foot[1]) / 2 - (H * 0.08 if fy < 0.8 else 0))
            d.line([hip, knee, foot], fill=pants, width=max(2, int(W * 0.17)), joint="curve")
            d.ellipse([foot[0] - W * 0.09, foot[1] - H * 0.03, foot[0] + W * 0.09, foot[1] + H * 0.015], fill=dark)
        d.rounded_rectangle([cx - W * 0.22, H * 0.27, cx + W * 0.22, H * 0.6], radius=W * 0.08, fill=jer, outline=dark, width=ow)
        d.line([(cx, H * 0.3), (cx, H * 0.58)], fill=trim, width=max(1, int(W * 0.04)))
        d.ellipse([cx - W * 0.14, H * 0.06, cx + W * 0.14, H * 0.26], fill=sk, outline=dark, width=ow)
        d.chord([cx - W * 0.16, H * 0.04, cx + W * 0.16, H * 0.2], 180, 360, fill=cap)
        d.rectangle([cx - W * 0.17, H * 0.12, cx + W * 0.17, H * 0.14], fill=cap)
        glove = {0: (0.0, 0.4), 1: (0.02, 0.36), 2: (0.34, 0.4), 3: (0.24, 0.5)}[frame]
        ball = {0: (0.06, 0.4), 1: (-0.02, 0.36), 2: (-0.42, 0.14), 3: (0.08, 0.32)}[frame]
        for (bx, by), col in ((glove, (150, 90, 40, 255)), (ball, sk)):
            p = (cx + bx * W, by * H)
            sh_ = (cx + (W * 0.2 if bx > 0 else -W * 0.2), H * 0.32)
            d.line([sh_, p], fill=jer, width=max(2, int(W * 0.11)))
            r = W * (0.1 if col != sk else 0.07)
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col, outline=dark, width=ow)
    return fn


def fielder_draw(kit, skin, frame):
    """Fielder seen from the front, ready (0), running (1) or catching high (2). / Joueur de champ vu de face."""
    def fn(d, W, H):
        dark = DARK + (255,)
        ow = max(1, int(W * 0.04))
        jer, pants, cap, sk = kit["jersey"] + (255,), kit["pants"] + (255,), kit["cap"] + (255,), skin + (255,)
        cx = W * 0.5
        hip = (cx, H * 0.58)
        for side in (-1, 1):
            fx_ = side * (0.2 if frame != 1 else (0.28 if side > 0 else 0.04))
            foot = (cx + fx_ * W, H * 0.98 - (H * 0.08 if frame == 1 and side < 0 else 0))
            knee = ((hip[0] + foot[0]) / 2 + side * W * 0.08, (hip[1] + foot[1]) / 2)
            d.line([hip, knee, foot], fill=pants, width=max(2, int(W * 0.18)), joint="curve")
        d.rounded_rectangle([cx - W * 0.24, H * 0.28, cx + W * 0.24, H * 0.6], radius=W * 0.1, fill=jer, outline=dark, width=ow)
        d.ellipse([cx - W * 0.15, H * 0.06, cx + W * 0.15, H * 0.27], fill=sk, outline=dark, width=ow)
        d.chord([cx - W * 0.17, H * 0.04, cx + W * 0.17, H * 0.2], 180, 360, fill=cap)
        hands = {0: ((-0.24, 0.62), (0.24, 0.62)), 1: ((-0.3, 0.42), (0.3, 0.5)), 2: ((-0.2, 0.36), (0.22, 0.0))}[frame]
        for i, (hx, hy) in enumerate(hands):
            sh_ = (cx + (W * 0.22 if hx > 0 else -W * 0.22), H * 0.33)
            p = (cx + hx * W, hy * H)
            d.line([sh_, p], fill=jer, width=max(2, int(W * 0.12)))
            if i == 1:
                d.ellipse([p[0] - W * 0.13, p[1] - W * 0.13, p[0] + W * 0.13, p[1] + W * 0.13], fill=(150, 90, 40, 255), outline=dark, width=ow)
    return fn


def baseball_draw(d, W, H):
    d.ellipse([0, 0, W - 1, H - 1], fill=(252, 250, 244, 255), outline=(120, 110, 100, 255), width=max(1, int(W * 0.06)))
    d.arc([-W * 0.3, H * 0.1, W * 0.45, H * 0.9], -60, 60, fill=(220, 40, 40, 255), width=max(1, int(W * 0.08)))
    d.arc([W * 0.55, H * 0.1, W * 1.3, H * 0.9], 120, 240, fill=(220, 40, 40, 255), width=max(1, int(W * 0.08)))


POSITIONS = {"1B": (52.0, 78.0), "2B": (30.0, 138.0), "SS": (-30.0, 138.0), "3B": (-52.0, 78.0), "LF": (-150.0, 262.0),
             "CF": (0.0, 318.0), "RF": (150.0, 262.0)}
MOUND, PLATE, BATTER = (0.0, 60.5), (0.0, 0.0), (-2.7, 0.2)
BASES = {1: (63.6, 63.6), 2: (0.0, 127.3), 3: (-63.6, 63.6), 0: (0.0, 0.0)}


class BaseballScene(GameScene):
    """Baseball seen from behind home plate. The balls, strikes and outs read in memory make the pitches: the ball
    goes into the mitt, the umpire calls the strike, the batter hits, a fielder catches. The runs read in memory send
    the ball far and the runners home. / Le baseball vu de derrière le marbre."""
    THEME = "ballpark"
    STATIC = True
    SHADE = (90, 0)
    PILLS = True
    BANNERS = GameScene.BANNERS + (("GRAND CHELEM !", GOLD), ("GRAND SLAM!", GOLD), ("HOME RUN !", GOLD), ("HOME RUN!", GOLD))
    WATCH = ("balls", "strikes", "outs", "runs", "runs_p2")

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.g = bb_geom(self.W, self.H, self.s)
        self.bat = 0                                           # team at bat: 0 player 1, 1 player 2 or computer
        self.pitches = 0                                       # balls and strikes seen since the last at-bat ended
        self.queue = []
        self.pend = None
        self.play = None
        self.play_end = 0.0
        self.ball = None
        self.pitch_t = -99.0
        self.swing_t = -99.0
        self.call_t = -99.0
        self.catch_t = -99.0
        self.batter_t = -99.0                                  # the new batter arrives
        self.batter_out = None                                 # (t0, kind) the batter leaves: runs to first or walks away
        self.runners = []
        self.fielders = {k: {"pos": list(v), "to": list(v), "speed": 0.0, "catch": -99.0} for k, v in POSITIONS.items()}
        self.power = [-99.0, -99.0]                            # POW spent by a team: its next ball burns
        self.rpop = [-99.0, -99.0]
        self.plays = 0                                         # plays shown (tests)
        self.swaps = 0                                         # changes of the team at bat (tests)
        self.skins = [self.rng.choice(SKINS) for _ in range(12)]
        self.fx.sp.register("bball", draw_img(self.S(12), self.S(12), baseball_draw))
        for team in (0, 1):
            self.warm += [(self.fig, ("bat", team, f, bb_px(self.g, 0.0) * 6.1, False)) for f in range(4)]
            self.warm += [(self.fig, ("pit", team, f, self.size_at(MOUND[1]), False)) for f in range(4)]
            for name, (x, z) in POSITIONS.items():
                self.warm += [(self.fig, ("fld", team, f, self.size_at(z), False)) for f in range(3)]

    # ------------------------------------------------------------ outils
    def P(self, x, z, h=0.0):
        return bb_xy(self.g, x, z, h)

    def size_at(self, z):
        """Height in pixels of a 6-foot player at the depth z. / Taille en pixels d'un joueur à la profondeur z."""
        return bb_px(self.g, z) * 6.0

    def fig(self, kind, team, frame, height, flip):
        """A player's picture at a given height (kept by steps of 4 pixels). / Image d'un joueur à une hauteur donnée."""
        h = max(8, int(round(height / 4.0)) * 4)
        key = ("fig", kind, team, frame, h, flip)
        s = self.imgs.get(key)
        if s is not None:
            return s
        kit = KITS[team]
        skin = self.skins[(team * 5 + frame) % len(self.skins)]
        if kind == "bat":                                              # a taller picture: room for the bat above the head
            return self.img(key, h * 0.95, h / 0.86, batter_draw(kit, self.skins[team], frame), ss=2, flip=flip)
        elif kind == "pit":
            fn, w = pitcher_draw(kit, self.skins[team + 2], frame), h * 0.62
        elif kind == "run":
            fn, w = batter_draw(kit, skin, 3), h * 0.62
        else:
            fn, w = fielder_draw(kit, skin, frame), h * 0.62
        return self.img(key, w, h, fn, flip=flip)

    def kits(self):
        return self.bat, 1 - self.bat                                  # (batting, fielding)

    # ------------------------------------------------------------ ce qui arrive dans le jeu
    def restart(self, vals, now):
        self.queue, self.pend, self.play, self.ball, self.runners = [], None, None, None, []
        self.bat = 0
        self.pitches = 0
        self.batter_t = now
        self.batter_out = None

    def classify(self, o, n):
        """Turns the counts before and after into what happened. / Ce qui s'est passé, d'après les compteurs."""
        def g(dct, k):
            v = dct.get(k)
            return int(v) if isinstance(v, (int, float)) else None
        r1 = (g(n, "runs") or 0) - (g(o, "runs") or 0)
        r2 = (g(n, "runs_p2") or 0) - (g(o, "runs_p2") or 0)
        if r1 < 0 or r2 < 0:                                           # a new game / une nouvelle partie
            self.bat = 0
            self.pitches = 0
            return []
        bo, bn, so, sn, oo, on = g(o, "balls"), g(n, "balls"), g(o, "strikes"), g(n, "strikes"), g(o, "outs"), g(n, "outs")
        third = oo is not None and on is not None and on < oo
        out_up = (oo is not None and on is not None and on > oo) or (third and oo == 2)
        plays = []
        if r1 > 0 or r2 > 0:
            team = 0 if r1 > 0 else 1
            plays.append(("run", {"team": team, "n": r1 if r1 > 0 else r2}))
        elif out_up:
            plays.append(("strikeout" if so == 2 else "out", {}))
        elif so is not None and sn is not None and sn > so:
            plays.append(("strike", {}))
        elif bo is not None and bn is not None and bn > bo:
            plays.append(("ball", {}))
        elif (bo is not None and bn is not None and bn < bo) or (so is not None and sn is not None and sn < so):
            if self.pitches > 0:                                       # the counts of this batter go back to zero: on base
                plays.append(("walk" if bo == 3 else "hit", {}))
            # otherwise the counts of the batter who is already out are cleared for the next one: nothing to show
        if third:
            plays.append(("switch", {}))
        if any(k in ("strike", "ball") for k, _ in plays):
            self.pitches += 1
        elif plays:
            self.pitches = 0
        return plays

    def update(self, vals, now):
        moved = [n for n in self.WATCH if self.changed(vals, n)]
        if moved:                                                      # a few frames together: one play
            if self.pend is None:
                self.pend = {"old": {n: self.prev.get(n) for n in self.WATCH}}
            self.pend["new"] = {n: vals.get(n) for n in self.WATCH}
            self.pend["t"] = now
            for n, team in (("runs", 0), ("runs_p2", 1)):
                ch = self.changed(vals, n)
                if ch and ch[1] > ch[0]:
                    self.rpop[team] = now
        if self.pend is not None and now - self.pend["t"] > 0.3:
            for kind, info in self.classify(self.pend["old"], self.pend["new"]):
                self.queue.append((kind, info))
            self.pend = None
            del self.queue[:-3]
        for team, name in ((0, "pow"), (1, "pow_p2")):
            ch = self.changed(vals, name)
            if ch and ch[1] <= ch[0] - 12:                             # POW spent: the next ball of this team burns
                self.power[team] = now
                x, y = (self.P(*BATTER) if team == self.bat else self.P(*MOUND))
                self.popup("POW !", x, y - self.S(120), (255, 170, 80), 40)
        if self.play is not None and now >= self.play_end:
            self.play = None
        if self.play is None and self.queue:
            self.start(self.queue.pop(0), now)
        self.move_players(now)

    def start(self, play, now):
        kind, info = play
        self.play = kind
        self.plays += 1
        L = self.fx.later
        if kind == "switch":
            self.switch(now)
            self.play_end = now + 1.2
            return
        rng = self.rng
        if kind == "run" and info.get("team", self.bat) != self.bat:    # the runs tell which team is at bat
            self.bat = info["team"]
            self.batter_t = now
        wind = 0.3 if self.queue else 0.55
        self.pitch_t = now
        fire_pitch = now - self.power[1 - self.bat] < 6.0
        if fire_pitch:
            self.power[1 - self.bat] = -99.0
        if kind in ("ball", "walk"):
            end = (rng.choice((-1, 1)) * rng.uniform(1.6, 2.3), -0.4, rng.uniform(1.4, 3.6))
        else:
            end = (rng.uniform(-0.5, 0.6), -0.4, rng.uniform(2.0, 3.0))
        self.ball = {"kind": "pitch", "t0": now + wind, "dur": 0.42, "p0": (-1.5, 55.5, 5.9), "p1": end, "apex": 0.4, "fire": fire_pitch}
        contact = kind in ("out", "hit", "run")
        swing = contact or (kind in ("strike", "strikeout") and rng.random() < 0.65)
        if swing:
            L(wind + 0.34, self.swing)
        if contact:
            L(wind + 0.42, self.contact, kind, info)
            self.play_end = now + wind + 0.42 + {"out": 2.0, "hit": 2.0, "run": 1.8 + 0.4 * info.get("n", 1)}[kind]
        else:
            L(wind + 0.42, self.caught, kind)
            self.play_end = now + wind + 0.42 + (1.3 if kind in ("strikeout", "walk") else 0.95)

    def swing(self):
        self.swing_t = self.fx.now

    def caught(self, kind):
        """The ball ends in the mitt: strike, ball, strike out, walk. / La balle finit dans le gant."""
        now = self.fx.now
        self.catch_t = now
        b = self.ball
        if b is not None:
            b["end"] = now
        if kind in ("strike", "strikeout"):
            self.call_t = now
            self.call("STRIKE !" if kind == "strike" else "STRIKE OUT !", 96 if kind == "strike" else 104)
            if kind == "strikeout":
                self.batter_out = (now + 0.4, "away")
        else:
            self.call(tr("BALLE", "BALL") if kind == "ball" else tr("BUT SUR BALLES", "WALK"), 90)
            if kind == "walk":
                self.batter_out = (now + 0.3, "first")

    def contact(self, kind, info):
        """The bat meets the ball: where it goes depends on what happened in the game. / La batte touche la balle."""
        now, rng, fx = self.fx.now, self.rng, self.fx
        bx, by = self.P(0.4, 0.8, 2.8)
        fx.glow(bx, by, 10, 80, (255, 250, 220), 0.18, "front", 1.0, 0.0, hot=0.8)
        fx.sparks(bx, by, 10, (255, 240, 200), (200, 600), (180, 360), (0.15, 0.3), 300, "front", 2, 18)
        fire = now - self.power[self.bat] < 6.0
        if fire:
            self.power[self.bat] = -99.0
        p0 = (0.4, 0.8, 2.8)
        if kind == "out":
            if rng.random() < 0.6:                                     # a fly ball caught in the outfield
                who = rng.choice(("LF", "CF", "RF"))
                hx, hz = POSITIONS[who]
                land = (hx + rng.uniform(-30, 30), hz + rng.uniform(-30, 20), 5.0)
                self.ball = {"kind": "fly", "t0": now, "dur": 1.5, "p0": p0, "p1": land, "apex": self.apex(p0, land, rng.uniform(50, 70)),
                             "fire": fire}
                self.send(who, land, 1.4)
                fx.later(1.5, self.catch_out, who)
            else:                                                      # a ground ball, fielded and thrown to first
                who = rng.choice(("3B", "SS", "2B"))
                hx, hz = POSITIONS[who]
                land = (hx + rng.uniform(-8, 8), hz - rng.uniform(4, 14), 1.0)
                self.ball = {"kind": "ground", "t0": now, "dur": 0.75, "p0": p0, "p1": land, "apex": 0.0, "fire": fire}
                self.send(who, land, 0.6)
                fx.later(0.75, self.throw_first, who, land)
            self.batter_out = (now + 0.15, "first")
        elif kind == "hit":                                            # a hit into a gap
            a = rng.choice((-0.55, -0.3, 0.3, 0.55)) + rng.uniform(-0.08, 0.08)
            r = rng.uniform(200, 250)
            land = (math.sin(a) * r, math.cos(a) * r, 0.0)
            self.ball = {"kind": "line", "t0": now, "dur": 1.0, "p0": p0, "p1": land, "apex": 22.0, "fire": fire, "roll": 0.7}
            who = min(("LF", "CF", "RF"), key=lambda k: math.hypot(POSITIONS[k][0] - land[0], POSITIONS[k][1] - land[1]))
            self.send(who, (land[0] * 1.1, land[1] * 1.1), 1.6)
            self.batter_out = (now + 0.15, "first")
            fx.later(0.5, self.call, tr("COUP SÛR !", "HIT!"), 96)
        else:                                                          # runs: a drive to the wall or over it, runners home
            n = int(info.get("n", 1))
            team = info.get("team", self.bat)
            if team != self.bat:
                self.bat = team
            a = rng.uniform(-0.62, 0.62)
            over = n >= 4 or rng.random() < 0.5
            r = bb_fence(a) + (rng.uniform(25, 45) if over else -rng.uniform(8, 20))
            land = (math.sin(a) * r, math.cos(a) * r, 26.0 if over else 6.0)
            self.ball = {"kind": "deep", "t0": now, "dur": 1.6 if over else 1.35, "p0": p0, "p1": land,
                         "apex": self.apex(p0, land, 85.0 if over else 55.0), "fire": fire, "over": over}
            if not over:
                who = min(("LF", "CF", "RF"), key=lambda k: math.hypot(POSITIONS[k][0] - land[0], POSITIONS[k][1] - land[1]))
                self.send(who, (land[0] * 0.92, land[1] * 0.92), 1.3)
            else:
                fx.later(1.6, self.fireworks, land)
            for i in range(n):                                         # the runners come home one after the other
                start = 3 if i < 3 else 0
                fx.later(0.2 + i * 0.42, self.run_home, team, start, i == n - 1, n)
            if n < 4:
                self.batter_out = (now + 0.15, "first")

    def send(self, who, to, dur):
        f = self.fielders[who]
        f["to"] = [to[0], to[1]]
        f["speed"] = math.hypot(to[0] - f["pos"][0], to[1] - f["pos"][1]) / max(0.3, dur)

    def catch_out(self, who):
        now = self.fx.now
        f = self.fielders[who]
        f["catch"] = now
        if self.ball is not None:
            self.ball["end"] = now
        self.call("OUT !", 100)
        self.fx.later(0.6, self.home_fielders)

    def throw_first(self, who, frm):
        f = self.fielders[who]
        f["catch"] = self.fx.now
        to = self.fielders["1B"]["pos"]
        self.ball = {"kind": "throw", "t0": self.fx.now + 0.15, "dur": 0.42, "p0": (frm[0], frm[1], 4.0), "p1": (to[0] - 2, to[1] - 2, 5.0),
                     "apex": 6.0, "fire": False}
        self.fx.later(0.6, self.catch_out, "1B")

    def home_fielders(self):
        for k, f in self.fielders.items():
            self.send(k, POSITIONS[k], 1.4)

    def run_home(self, team, start, last, n):
        """A runner from third (or the batter) runs to the plate; one run more on the board. / Un coureur rentre au marbre."""
        now = self.fx.now
        path = [BASES[3], BASES[0]] if start == 3 else [BASES[0], BASES[1], BASES[2], BASES[3], BASES[0]]
        dur = 1.0 if start == 3 else 3.2
        self.runners.append({"team": team, "path": path, "t0": now, "dur": dur, "done": False, "last": last, "n": n})

    def scored(self, r):
        now, S = self.fx.now, self.S
        x, y = self.P(*PLATE)
        self.fx.sparks(x, y - S(20), 16, (255, 240, 180), (200, 700), (190, 350), (0.3, 0.6), 600, "front", 3, 22)
        self.bd.excite(1.2)
        if r["last"]:
            n = r["n"]
            if n >= 4:
                self.slam(tr("GRAND CHELEM !", "GRAND SLAM!"), GOLD, now, 2.0)
            else:
                self.call(tr("POINT !", "RUN!") if n == 1 else tr(f"{n} POINTS !", f"{n} RUNS!"), 96)

    def fireworks(self, land):
        """The ball lands in the stands: fireworks above them. / La balle tombe dans les tribunes : un feu d'artifice."""
        now, S, fx, rng = self.fx.now, self.S, self.fx, self.rng
        x, y = self.P(land[0], land[1], land[2])
        fx.sparks(x, y, 20, (255, 255, 255), (150, 500), (180, 360), (0.3, 0.6), 500, "front", 3, 20)
        self.slam(tr("HOME RUN !", "HOME RUN!"), GOLD, now, 1.8)
        self.bd.excite(2.2)
        for i in range(7):
            fxx, fy = self.W * rng.uniform(0.08, 0.92), S(rng.uniform(40, 150))
            col = rng.choice(((255, 90, 70), (255, 220, 90), (120, 200, 255), (160, 255, 140), (255, 140, 240)))
            fx.later(i * 0.22, fx.glow, fxx, fy, 10, 90, col, 0.5, "back", 1.0, 0.0, 0.0, 0.5)
            fx.later(i * 0.22, fx.sparks, fxx, fy, 26, col, (150, 420), (0, 360), (0.5, 1.0), 160, "back", 2, 16)

    def switch(self, now):
        """Three outs: the other team comes to bat. / Trois retraits : l'autre équipe passe à la batte."""
        self.bat = 1 - self.bat
        self.swaps += 1
        self.batter_t = now + 0.4
        self.batter_out = None
        x, y = self.P(*MOUND)
        self.popup(tr("3 RETRAITS", "3 OUTS"), x, y - self.S(80), (255, 200, 120), 40, 1.3, 40, "stencil")
        self.home_fielders()

    # ------------------------------------------------------------ mouvement
    def move_players(self, now):
        dt = self.dt
        for f in self.fielders.values():
            dx, dz = f["to"][0] - f["pos"][0], f["to"][1] - f["pos"][1]
            dist = math.hypot(dx, dz)
            step = max(f["speed"], 20.0) * dt
            if dist <= step:
                f["pos"] = [f["to"][0], f["to"][1]]
                f["moving"] = False
            else:
                f["pos"][0] += dx / dist * step
                f["pos"][1] += dz / dist * step
                f["moving"] = True
        if self.batter_out is not None and now - self.batter_out[0] > 1.6:     # the next batter steps in
            self.batter_out = None
            self.batter_t = now
        for r in self.runners:
            if not r["done"] and now - r["t0"] >= r["dur"]:
                r["done"] = True
                self.scored(r)
        self.runners = [r for r in self.runners if now - r["t0"] < r["dur"] + 0.5]

    def ball_xyz(self, b, now):
        k = (now - b["t0"]) / b["dur"]
        if k < 0:
            return None
        x0, z0, h0 = b["p0"]
        x1, z1, h1 = b["p1"]
        if k >= 1.0:
            if b.get("roll") and k < 1.0 + b["roll"] / b["dur"]:       # the ball rolls on after landing
                q = (k - 1.0) * b["dur"] / b["roll"]
                return x1 + (x1 - x0) * 0.25 * q * (2 - q), z1 + (z1 - z0) * 0.25 * q * (2 - q), 0.0
            return x1, z1, h1
        x, z = _lerp(x0, x1, k), _lerp(z0, z1, k)
        if b["kind"] == "ground":
            h = _lerp(h0, h1, k) + abs(math.sin(k * math.pi * 3)) * 3.0 * (1 - k)
        else:
            h = _lerp(h0, h1, k) + b["apex"] * 4 * k * (1 - k)
        return x, z, h

    # ------------------------------------------------------------ dessin
    def blit_fig(self, screen, surf, x, y, alpha=1.0):
        if alpha < 0.99:
            surf.set_alpha(int(255 * _clamp(alpha)))
        screen.blit(surf, (int(x - surf.get_width() / 2), int(y - surf.get_height())))
        if alpha < 0.99:
            surf.set_alpha(255)

    def draw_field(self, screen, now):
        S, pg = self.S, self.pg
        batting, fielding = self.kits()
        sh = self.imgs.get("sh")
        if sh is None:
            sh = self.imgs["sh"] = pg.Surface((S(40), S(12)), pg.SRCALPHA)
            pg.draw.ellipse(sh, (0, 0, 0, 80), sh.get_rect())
        b = self.ball
        if b is not None:                                              # the shadow of the ball on the grass
            p = self.ball_xyz(b, now)
            if p is not None and b["kind"] != "pitch":
                x, y = self.P(p[0], p[1], 0.0)
                w = max(4, int(bb_px(self.g, p[1]) * 2.0 + S(4)))
                screen.blit(pg.transform.smoothscale(sh, (w, max(2, w // 3))), (int(x - w / 2), int(y - w / 6)))
        items = []
        for name, f in self.fielders.items():
            items.append((f["pos"][1], "fld", name))
        items.append((MOUND[1], "pit", None))
        for r in self.runners:
            items.append((self.runner_xz(r, now)[1], "run", r))
        items.sort(key=lambda t: -t[0])
        for z, kind, it in items:
            if kind == "fld":
                f = self.fielders[it]
                x, y = self.P(f["pos"][0], f["pos"][1])
                frame = 2 if now - f["catch"] < 0.8 else (1 if f.get("moving") else 0)
                hh = self.size_at(f["pos"][1])
                img = self.fig("fld", fielding, frame, hh, False)
                ssh = self.shadow(int(hh * 0.5))
                screen.blit(ssh, (int(x - ssh.get_width() / 2), int(y - ssh.get_height() / 2)))
                self.blit_fig(screen, img, x, y)
            elif kind == "pit":
                t = now - self.pitch_t
                wind = 0.3 if self.queue else 0.55
                frame = 1 if t < wind * 0.5 else (2 if t < wind else (3 if t < wind + 0.3 else 0))
                x, y = self.P(*MOUND)
                self.blit_fig(screen, self.fig("pit", fielding, frame, self.size_at(MOUND[1]), False), x, y - S(3))
            else:
                rx, rz = self.runner_xz(it, now)
                x, y = self.P(rx, rz)
                ahead = self.P(*self.runner_xz(it, now + 0.05))[0]        # facing where he runs
                img = self.fig("run", it["team"], int(now * 9) % 2, self.size_at(rz), ahead < x)
                self.blit_fig(screen, img, x, y)
        bx, by = self.P(*BATTER)                                       # the batter, then the catcher and the umpire
        alpha, ox, frame = 1.0, 0.0, 0
        if self.batter_out is not None:
            t0, how = self.batter_out
            k = _clamp((now - t0) / 1.4)
            if how == "first":                                         # runs to first base
                p = (_lerp(BATTER[0], 40.0, k), _lerp(BATTER[1], 40.0, k))
                bx, by = self.P(*p)
                frame = 3
                alpha = 1.0 - _clamp((k - 0.6) / 0.4)
                img = self.fig("bat", batting, 3, self.size_at(p[1]), False)
            else:
                alpha = 1.0 - k
                ox = -S(60) * k
                img = self.fig("bat", batting, 0, bb_px(self.g, 0.0) * 6.1, False)
        else:
            t = now - self.swing_t
            frame = 1 if t < 0.1 else (2 if t < 0.7 else 0)
            alpha = _clamp((now - self.batter_t) / 0.4)
            img = self.fig("bat", batting, frame, bb_px(self.g, 0.0) * 6.1, False)
        if alpha > 0.02:
            ssh = self.shadow(int(img.get_width() * 0.6))
            screen.blit(ssh, (int(bx + ox - ssh.get_width() / 2), int(by - ssh.get_height() / 2)))
            self.blit_fig(screen, img, bx + ox, by, alpha)
        if b is not None:                                              # the ball, on top of everything
            p = self.ball_xyz(b, now)
            if p is not None and not (b.get("end") is not None and now - b["end"] > 0.15):
                x, y = self.P(*p)
                r = max(S(5), bb_px(self.g, p[1]) * 0.24 * 1.4)
                if b.get("fire"):                                      # POW: the ball burns
                    g = self.fx.sp.glow(r * 3.2, (255, 140, 50), 10, hot=0.6)
                    screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
                img = self.fx.sp.obj("bball", (now * 900) % 360)
                if img is not None:
                    sc = 2 * r / img.get_width()
                    img = pg.transform.smoothscale(img, (max(3, int(img.get_width() * sc)), max(3, int(img.get_height() * sc))))
                    screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
                if b["kind"] != "pitch" or (now - b["t0"]) / b["dur"] > 0.5:
                    g = self.fx.sp.glow(r * 1.6, (255, 250, 230), 5, hot=0.3)
                    screen.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            elif p is not None and b.get("end") is not None and now - b["end"] > 0.15:
                self.ball = None

    def shadow(self, w):
        w = max(4, w // 2 * 2)
        sh = self.imgs.get(("bsh", w))
        if sh is None:
            sh = self.imgs[("bsh", w)] = self.pg.Surface((w, max(2, w // 3)), self.pg.SRCALPHA)
            self.pg.draw.ellipse(sh, (0, 0, 0, 80), sh.get_rect())
        return sh

    def apex(self, p0, p1, want):
        """Highest arc that keeps the ball on the screen at the middle of its flight. / Arc qui reste dans l'écran."""
        x, z, h0 = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2
        lo, hi = 0.0, 200.0
        for _ in range(24):                                            # the highest point still below the top of the screen
            mid = (lo + hi) / 2
            if bb_xy(self.g, x, z, h0 + mid)[1] > self.S(40):
                lo = mid
            else:
                hi = mid
        return max(4.0, min(want, lo))

    def runner_xz(self, r, now):
        k = _clamp((now - r["t0"]) / r["dur"])
        path = r["path"]
        seg = min(len(path) - 2, int(k * (len(path) - 1)))
        q = k * (len(path) - 1) - seg
        (x0, z0), (x1, z1) = path[seg], path[seg + 1]
        return _lerp(x0, x1, q), _lerp(z0, z1, q)

    def rainbow(self, text, size):
        """A call in big letters in the colours of the rainbow, outlined, as in the game. / Une annonce en grosses lettres
        aux couleurs de l'arc-en-ciel, comme dans le jeu."""
        key = ("rainbow", text, size)
        s = self.imgs.get(key)
        if s is None:
            pg, S = self.pg, self.S
            t = self.hd.text(text, "stencil", S(size), WHITE, 0.0)
            src_ = t["surf"]
            w, h = src_.get_size()
            grad = pg.Surface((w, h)).convert()
            cols = ((255, 70, 60), (255, 170, 40), (255, 240, 70), (90, 230, 90), (70, 200, 255), (170, 110, 255))
            for y in range(h):
                k = y / max(1, h - 1) * (len(cols) - 1)
                i = min(len(cols) - 2, int(k))
                pg.draw.line(grad, _mix(cols[i], cols[i + 1], k - i), (0, y), (w, y))
            face = src_.copy()
            face.blit(grad, (0, 0), special_flags=pg.BLEND_RGB_MULT)
            edge = src_.copy()
            edge.fill((20, 16, 40, 255), special_flags=pg.BLEND_RGBA_MIN)
            o = max(2, S(4))
            s = pg.Surface((w + 2 * o, h + 2 * o), pg.SRCALPHA)
            for dx, dy in ((-o, 0), (o, 0), (0, -o), (0, o), (-o, -o), (o, o), (-o, o), (o, -o)):
                s.blit(edge, (o + dx, o + dy))
            s.blit(face, (o, o))
            self.imgs[key] = s
        return s

    def draw_pops(self, screen, now):
        """The calls of the umpire in rainbow letters, the rest as everywhere. / Les annonces en lettres arc-en-ciel."""
        keep = []
        for p in self.pops:
            text, x, y, color, size, t0, life, rise, key = p
            if key != "rainbow":
                keep.append(p)
                continue
            k = (now - t0) / life
            if k >= 1.0 or k < 0:
                if k < 0:
                    keep.append(p)
                continue
            img = self.rainbow(text, size)
            pop = 1.0 + 0.6 * max(0.0, 1 - k / 0.12)
            if pop != 1.0:
                img = self.pg.transform.smoothscale(img, (int(img.get_width() * pop), int(img.get_height() * pop)))
            fade = 1.0 if k < 0.75 else max(0.0, (1 - k) / 0.25)
            if fade < 1.0:
                img = img.copy()
                img.set_alpha(int(255 * fade))
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        rest = self.pops
        self.pops = keep
        GameScene.draw_pops(self, screen, now)
        self.pops = self.pops + [p for p in rest if p[8] == "rainbow" and 0 <= (now - p[5]) / p[6] < 1.0]

    def call(self, text, size=90):
        """A call of the umpire in the middle of the screen. / Une annonce au milieu de l'écran."""
        self.popup(text, self.W / 2, self.S(300), WHITE, size, 1.3, 0, "rainbow")

    def scoreboard(self, screen, vals, now):
        """As in the game: the score of the two teams in a framed box, the count B S O in coloured dots beside it.
        / Comme dans le jeu : le score dans un cadre, le compte B S O en pastilles de couleur à côté."""
        hd, S, pg = self.hd, self.S, self.pg
        x, y, bw, bh = S(20), S(12), S(300), S(122)
        self.box(screen, x, y, bw, bh, (255, 150, 60), fill=(12, 18, 70, 226), radius=12, width=4)
        right = "P2" if self.p2_in(vals) else "CPU"
        cy = y + S(32)
        self.text(screen, "P1", x + S(34), cy, 32, P1C, valign="middle")
        self.text(screen, right, x + bw - S(34), cy, 32, P2C, align="right", valign="middle")
        ax = x + S(14) if self.bat == 0 else x + bw - S(14)                  # who is at bat: a small ball beside the team
        pg.draw.circle(screen, (250, 250, 244), (int(ax), int(cy)), S(8))
        pg.draw.circle(screen, (220, 40, 40), (int(ax), int(cy)), S(8), max(1, S(2)))
        self.text(screen, "-", x + bw / 2, cy, 32, GREY, align="center", valign="middle", glow=0)
        for name, team, xx in (("runs", 0, x + bw * 0.27), ("runs_p2", 1, x + bw * 0.73)):
            v = _n(vals.get(name))
            if v is None:
                continue
            k = now - self.rpop[team]
            col = (P1C if team == 0 else P2C) if not (k < 1.0 and int(k * 8) % 2 == 0) else WHITE
            hd.put_number(screen, f"{int(v)}", "black", S(58), col, xx, y + S(86), "center", "middle", scale=1.0 + 0.35 * max(0.0, 1 - k / 0.4))
        bx, bw2 = x + bw + S(12), S(214)                               # B S O, as in the game
        self.box(screen, bx, y, bw2, bh, (255, 150, 60), fill=(12, 18, 70, 226), radius=12, width=4)
        for row, (lab, name, n, col, off) in enumerate((("B", "balls", 3, (70, 230, 90), (24, 50, 30)),
                                                        ("S", "strikes", 2, (255, 210, 60), (60, 50, 20)),
                                                        ("O", "outs", 2, (255, 80, 60), (60, 26, 22)))):
            v = _n(vals.get(name))
            ry = y + S(26) + row * S(35)
            self.text(screen, lab, bx + S(20), ry, 28, CREAM, key="black", valign="middle", glow=0)
            for i in range(n):
                on = v is not None and i < int(v)
                cxx = int(bx + S(70) + i * S(42))
                pg.draw.circle(screen, col if on else off, (cxx, int(ry)), S(13))
                if on:
                    pg.draw.circle(screen, _mix(col, WHITE, 0.6), (cxx - S(4), int(ry) - S(4)), S(5))

    def pow_bars(self, screen, vals, now):
        S, W = self.S, self.W
        for side, name, x0, d, acc in (("p1", "pow", S(30), 1, P1C), ("p2", "pow_p2", W - S(30), -1, P2C)):
            if side == "p2" and not self.p2_in(vals):
                continue
            p = _n(vals.get(name))
            if p is None:
                continue
            full = p >= 99
            bw = S(300)
            x = x0 if d > 0 else x0 - bw
            self.pill(screen, x - S(14), S(374), bw + S(28), S(78), 150, radius=14)
            k = 0.5 + 0.5 * math.sin(now * 10)
            self.text(screen, "POW", x, S(382), 24, _mix(GOLD, WHITE, k) if full else CREAM, key="black" if full else "bold", glow=0.5 if full else 0)
            self.bar(screen, x, S(414), bw, S(26), p / 99.0, (255, 220, 120) if full else (255, 170, 60), back=(46, 32, 10))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        self.draw_field(screen, now)
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(560), S(104), now)
        self.scoreboard(screen, vals, now)
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(54), 34, col, align="right")
        self.pow_bars(screen, vals, now)


# ============================================================================ Last Resort
def lr_ship_draw(accent, body=(222, 226, 236), dark=(26, 24, 40)):
    """A long slim fighter seen from the side, nose to the right: a round hull, a pointed nose, a glass canopy, a swept
    wing below, a fin above, the engine at the back. / Un long chasseur fin de profil : nez pointu, verrière, aile en flèche."""
    def fn(d, W, H):
        ow = max(1.0, H * 0.035)
        line = dark + (255,)
        shade, light = _mix(body, (40, 44, 80), 0.42) + (255,), _mix(body, WHITE, 0.6) + (255,)
        acc, acc_d = accent + (255,), _mix(accent, (0, 0, 0), 0.35) + (255,)

        def P(pts):
            return [(x * W, y * H) for x, y in pts]
        _shape(d, P([(0.26, 0.44), (0.36, 0.44), (0.24, 0.06), (0.14, 0.06)]), acc_d, line, ow)       # dérive
        _shape(d, P([(0.3, 0.54), (0.56, 0.56), (0.3, 0.98), (0.16, 0.98)]), shade, line, ow)          # aile en flèche
        d.polygon(P([(0.32, 0.6), (0.48, 0.6), (0.3, 0.9), (0.22, 0.9)]), fill=body + (255,))
        d.line(P([(0.3, 0.58), (0.2, 0.94)]), fill=acc, width=int(H * 0.05))
        _shape(d, P([(0.0, 0.3), (0.13, 0.26), (0.13, 0.74), (0.0, 0.7)]), (80, 84, 104, 255), line, ow)    # réacteur
        d.ellipse(P([(0.0, 0.34), (0.05, 0.66)])[0] + P([(0.0, 0.34), (0.05, 0.66)])[1], fill=(40, 40, 56, 255))
        hull = P([(0.1, 0.32), (0.7, 0.3), (0.86, 0.36), (1.0, 0.5), (0.86, 0.64), (0.7, 0.7), (0.1, 0.68)])
        _shape(d, hull, body + (255,), line, ow)
        d.polygon(P([(0.11, 0.52), (0.98, 0.52), (0.86, 0.63), (0.7, 0.69), (0.11, 0.67)]), fill=shade)   # ventre dans l'ombre
        d.polygon(P([(0.12, 0.35), (0.7, 0.33), (0.82, 0.38), (0.7, 0.41), (0.12, 0.42)]), fill=light)    # reflet
        for x in (0.24, 0.4, 0.56):                                                                      # anneaux
            d.line(P([(x, 0.32), (x, 0.68)]), fill=_mix(body, (40, 44, 80), 0.6) + (255,), width=max(1, int(ow * 0.7)))
        d.line(P([(0.14, 0.5), (0.86, 0.5)]), fill=acc, width=int(H * 0.06))
        _shape(d, P([(0.6, 0.33), (0.66, 0.2), (0.78, 0.2), (0.86, 0.34)]), (40, 70, 150, 255), line, ow)       # verrière
        d.polygon(P([(0.66, 0.31), (0.69, 0.23), (0.75, 0.23), (0.7, 0.31)]), fill=(170, 220, 255, 255))
    return fn


def unit_draw(core):
    """The unit: a metal ball with a glowing core in the colour of the shots and a ring. / L'unité : une boule de métal au
    cœur lumineux de la couleur des tirs."""
    def fn(d, W, H):
        d.ellipse([0, 0, W - 1, H - 1], fill=(60, 62, 80, 255))
        for i in range(8):
            k = i / 8
            r = (W / 2) * (0.94 - k * 0.5)
            cx, cy = W / 2 - W * 0.1 * k, H / 2 - H * 0.1 * k
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_mix((70, 74, 96), (190, 196, 220), k) + (255,))
        d.ellipse([W * 0.3, H * 0.3, W * 0.7, H * 0.7], fill=core + (255,))
        d.ellipse([W * 0.4, H * 0.38, W * 0.54, H * 0.5], fill=(255, 255, 255, 230))
        d.ellipse([0, 0, W - 1, H - 1], outline=(24, 24, 36, 255), width=max(1, int(W * 0.06)))
        for a in range(0, 360, 60):
            r0, r1 = W * 0.36, W * 0.48
            t = math.radians(a)
            d.line([(W / 2 + math.cos(t) * r0, H / 2 + math.sin(t) * r0), (W / 2 + math.cos(t) * r1, H / 2 + math.sin(t) * r1)],
                   fill=(30, 30, 44, 255), width=max(1, int(W * 0.05)))
    return fn


def lr_enemy_draw(d, W, H):
    """Enemy craft of Last Resort coming from the right, like an armoured insect: a body in bronze plates, a head with a
    red eye in front, claws below, two blades at the back. / Engin ennemi en forme d'insecte blindé, plaques de bronze."""
    dark = (30, 22, 16, 255)
    ow = max(1.0, H * 0.04)
    body, light, shade = (170, 146, 96, 255), (222, 202, 150, 255), (110, 90, 56, 255)
    _shape(d, [(0.62 * W, 0.42 * H), (0.98 * W, 0.04 * H), (0.86 * W, 0.44 * H)], (130, 110, 72, 255), dark, ow)     # lames
    _shape(d, [(0.62 * W, 0.58 * H), (0.98 * W, 0.96 * H), (0.86 * W, 0.56 * H)], shade, dark, ow)
    for k in range(3):                                                                              # pattes
        x = (0.3 + 0.16 * k) * W
        d.line([(x, 0.62 * H), (x - 0.06 * W, 0.86 * H), (x - 0.12 * W, 0.84 * H)], fill=dark, width=max(1, int(H * 0.06)), joint="curve")
    d.ellipse([0.14 * W, 0.24 * H, 0.9 * W, 0.76 * H], fill=body, outline=dark, width=int(ow))         # corps
    d.chord([0.18 * W, 0.27 * H, 0.86 * W, 0.6 * H], 180, 360, fill=light)
    for x in (0.38, 0.54, 0.7):                                                                     # plaques
        d.arc([x * W - 0.1 * W, 0.24 * H, x * W + 0.1 * W, 0.76 * H], 250, 110, fill=dark, width=max(1, int(ow * 0.8)))
    d.ellipse([0.02 * W, 0.3 * H, 0.32 * W, 0.7 * H], fill=(120, 100, 64, 255), outline=dark, width=int(ow))       # tête
    d.ellipse([0.06 * W, 0.4 * H, 0.18 * W, 0.58 * H], fill=(255, 50, 40, 255), outline=dark, width=max(1, int(ow * 0.8)))
    d.ellipse([0.09 * W, 0.43 * H, 0.13 * W, 0.49 * H], fill=(255, 220, 200, 255))
    d.line([(0.06 * W, 0.34 * H), (0.0, 0.2 * H)], fill=dark, width=max(1, int(H * 0.05)))              # mandibules
    d.line([(0.06 * W, 0.66 * H), (0.0, 0.8 * H)], fill=dark, width=max(1, int(H * 0.05)))


class LastResortScene(BlazingStarScene):
    """The ship and its unit over the city at night of the game: giant towers lit orange, purple buildings, the highway
    and its cars. The unit turns around the ship on the side away from where it goes, fires with it, and is launched
    straight ahead from time to time (button B). At the top 1P= and the score, the ship and the lives, POW at the bottom.
    / Le vaisseau et son unité au-dessus de la ville de nuit du jeu. En haut 1P= et le score, les vies, POW en bas."""
    THEME = "lr_city"
    SHADE = (100, 120)
    BANNERS = GameScene.BANNERS
    ACC = {"p1": (255, 110, 70), "p2": (80, 190, 255)}
    ZONE = (150, 285)                                  # the unit below the ship stays above the panels
    CORE = ((150, 200, 255), (110, 230, 255), (120, 255, 200), (255, 220, 120), (255, 150, 90))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.units = {side: {"a": math.pi, "launch": None, "last": None, "btn": 0, "next": 0.0} for side in ("p1", "p2")}
        self.launches = 0                                      # unit launches (tests)

    def ship_surf(self, side):
        return self.img("lrship_" + side, self.S(190), self.S(64), lr_ship_draw(self.ACC[side]))

    def move(self, vals, now, idle):
        sp = _n(vals.get("speed"))
        return 0.15 if idle else 0.55 + 0.1 * (2 if sp is None else _clamp(sp, 0, 5))

    def unit_xy(self, side, x, y, now):
        U, S = self.units[side], self.S
        ox, oy = x + math.cos(U["a"]) * S(92), y + math.sin(U["a"]) * S(66)
        L = U["launch"]
        if L is None:
            return ox, oy
        k = now - L[0]
        if k < 0.45:                                                   # flies straight ahead
            q = k / 0.45
            return _lerp(L[1], self.W + S(80), q * q * (3 - 2 * q)), _lerp(L[2], L[2], q)
        q = _clamp((k - 0.45) / 0.55)                                   # comes back
        return _lerp(self.W + S(80), ox, q * q * (3 - 2 * q)), _lerp(L[2], oy, q)

    def launch(self, side, now):
        U = self.units[side]
        if U["launch"] is not None:
            return
        x, y = self.pos(side, now)
        ux, uy = self.unit_xy(side, x, y, now)
        U["launch"] = (now, ux, uy)
        self.launches += 1
        self.fx.glow(ux, uy, 20, 120, (255, 220, 160), 0.3, "front", 1.0, 0.0, hot=0.6)

    def restart(self, vals, now):
        super().restart(vals, now)
        for U in self.units.values():
            U["launch"], U["last"] = None, None

    def update(self, vals, now):
        super().update(vals, now)
        dt, S = self.dt, self.S
        for side, suf in (("p1", ""), ("p2", "_p2")):
            P, U = self.ships[side], self.units[side]
            if not P["in"]:
                continue
            x, y = self.pos(side, now)
            if U["last"] is not None and dt > 0:                       # the unit swings to the side away from where the ship goes
                vx, vy = (x - U["last"][0]) / dt, (y - U["last"][1]) / dt
                if math.hypot(vx, vy) > S(40):
                    want = math.atan2(-vy, -vx)
                    diff = (want - U["a"] + math.pi) % math.tau - math.pi
                    U["a"] = (U["a"] + _clamp(diff, -4.0 * dt, 4.0 * dt) + math.pi) % math.tau - math.pi
            U["last"] = (x, y)
            if U["launch"] is not None:
                k = now - U["launch"][0]
                if k < 0.45:
                    ux, uy = self.unit_xy(side, x, y, now)
                    for e in self.enemies:
                        if not e.get("dead") and abs(e["x"] - ux) < S(60) and abs(e.get("yy", e["y"]) - uy) < S(60):
                            self._boom(e)
                elif k > 1.0:
                    U["launch"] = None
            st = self.stick(vals, side)
            if st is not None:
                press = st[2] & ~U["btn"]
                U["btn"] = st[2]
                if press & BTN_B:
                    self.launch(side, now)
            elif now >= U["next"] and any(not e.get("dead") and e["x"] > x for e in self.enemies):
                U["next"] = now + self.rng.uniform(7.0, 12.0)
                if now - P["t_spawn"] > 2.0:
                    self.launch(side, now)
            ch = self.changed(vals, "speed" + suf)
            if ch and ch[1] > ch[0] and side == "p1":
                self.popup(tr("VITESSE +", "SPEED UP"), x, max(S(176), y - S(74)), (130, 210, 255), 34)

    def _fire(self, side, pw, now):
        super()._fire(side, min(3, pw), now)
        U = self.units[side]
        if U["launch"] is not None:
            return
        x, y = self.pos(side, now)
        ux, uy = self.unit_xy(side, x, y, now)
        col = self.CORE[int(_clamp(pw, 0, 4))]
        a = U["a"] if math.cos(U["a"]) > -0.2 else 0.0                  # behind the ship, the unit fires ahead too
        tx, ty = ux + math.cos(a) * self.W, uy + math.sin(a) * self.W
        self.fx.tracer(ux, uy, tx, ty, speed=3000, color=col, width=4 if pw < 3 else 6, length=90, impact=False)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg, dt, sp = self.S, self.pg, self.dt, self.fx.sp
        add = pg.BLEND_RGB_ADD
        enemy = self.img("lr_enemy", S(96), S(58), lr_enemy_draw)
        keep = []
        for e in self.enemies:                                         # enemies coming from the right
            if e.get("dead"):
                continue
            e["x"] -= e["v"] * dt
            if e["x"] < -S(100):
                continue
            e["yy"] = e["y"] + math.sin(now * 2.4 + e["ph"]) * S(16)
            keep.append(e)
            screen.blit(enemy, (int(e["x"] - enemy.get_width() / 2), int(e["yy"] - enemy.get_height() / 2)))
            g = sp.glow(S(16), (255, 60, 40), 5 + 3 * math.sin(now * 8 + e["ph"]), hot=0.5)
            screen.blit(g, (int(e["x"] - S(37) - g.get_width() / 2), int(e["yy"] - S(1) - g.get_height() / 2)), special_flags=add)
            if now - e["hit"] < 0.06:
                h = sp.glow(S(40), (255, 255, 255), 8, hot=0.6)
                screen.blit(h, (int(e["x"] - h.get_width() / 2), int(e["yy"] - h.get_height() / 2)), special_flags=add)
        self.enemies = keep
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"] or now - P["t_dead"] < 1.2 or now < P["t_spawn"]:
                continue
            if now - P["t_spawn"] < 1.6 and int(now * 14) % 2 == 0:
                continue
            x, y = self.pos(side, now)
            suf = "" if side == "p1" else "_p2"
            spd = _n(vals.get("speed" + suf))
            spd = 2 if spd is None else _clamp(spd, 0, 5)
            fl = sp.streak(S(30 + 14 * spd) + S(6) * math.sin(now * 40), S(12), (255, 150, 90), 0, 10)    # the engine, longer when fast
            screen.blit(fl, (int(x - S(93) - fl.get_width()), int(y - fl.get_height() / 2)), special_flags=add)
            g = sp.glow(S(16) + S(3) * math.sin(now * 37), (255, 200, 150), 9, hot=0.8)
            screen.blit(g, (int(x - S(93) - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=add)
            ship = self.rotated("lrship_" + side, self.ship_surf(side), _clamp(-P["vy"] * 6, -10, 10))
            screen.blit(ship, (int(x - ship.get_width() / 2), int(y - ship.get_height() / 2)))
            pw = int(_clamp(_n(vals.get("power" + suf)) or 0, 0, 4))
            ux, uy = self.unit_xy(side, x, y, now)
            core = self.CORE[pw]
            g = sp.glow(S(36 + 7 * pw) + S(3) * math.sin(now * 12), core, 5 + pw, hot=0.4)
            screen.blit(g, (int(ux - g.get_width() / 2), int(uy - g.get_height() / 2)), special_flags=add)
            unit = self.rotated(("unit", pw), self.img(("unit", pw), S(66), S(66), unit_draw(core)), (now * 120) % 360, 10)
            screen.blit(unit, (int(ux - unit.get_width() / 2), int(uy - unit.get_height() / 2)))
            if self.units[side]["launch"] is not None and now - self.units[side]["launch"][0] < 0.45:
                tr_ = sp.streak(S(160), S(14), core, 180, 9)
                screen.blit(tr_, (int(ux - tr_.get_width()), int(uy - tr_.get_height() / 2)), special_flags=add)
        self.status(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        """As in the game: 1P= and the score at the top, the ship and the lives below, POW at the bottom; the logo in the
        middle. / Comme dans le jeu : 1P= et le score en haut, le vaisseau et les vies dessous, POW en bas."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(560), S(112), now)
        for side in ("p1", "p2"):
            right = side == "p2"
            if right and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, W - S(24), S(44), 36, col, align="right")
                continue
            suf = "_p2" if right else ""
            x0 = W - S(30) if right else S(30)
            sc = _n(vals.get("score" + suf))
            tag = "2P=" if right else "1P="
            tw_ = hd.text(tag, "black", S(40), WHITE)["w"]
            sw = hd.text(str(sc), "black", S(56), GOLD)["w"] if sc is not None else 0
            self.pill(screen, (x0 - tw_ - sw - S(34)) if right else x0 - S(16), S(8), tw_ + sw + S(48), S(70), 150)
            if right:
                if sc is not None:
                    hd._score(screen, eng, "score" + suf, x0, S(14), "right", S(56))
                self.text(screen, tag, x0 - sw - S(16), S(22), 40, WHITE, align="right")
            else:
                self.text(screen, tag, x0, S(22), 40, WHITE)
                if sc is not None:
                    hd._score(screen, eng, "score" + suf, x0 + tw_ + S(16), S(14), "left", S(56))
            lives = _n(vals.get("lives" + suf))
            if lives is not None:                                      # the ship and x03, as in the game
                icon = self.img("lrlife_" + side, S(78), S(26), lr_ship_draw(self.ACC[side]))
                txt = f"x{int(lives):02d}"
                lw = hd.text(txt, "black", S(34), CREAM)["w"]
                bx = x0 - icon.get_width() - lw - S(14) if right else x0
                self.pill(screen, bx - S(12), S(84), icon.get_width() + lw + S(38), S(44), 140)
                screen.blit(icon, (int(bx), S(93)))
                self.text(screen, txt, bx + icon.get_width() + S(12), S(106), 34, CREAM, valign="middle")
            pw, spd = _n(vals.get("power" + suf)), _n(vals.get("speed" + suf))
            y = S(408)
            if pw is not None:                                         # POW: a long gauge in a metal frame
                gw = S(300)
                lab = hd.text("POW", "black", S(30), CREAM)["w"]
                lx = x0 - gw - lab - S(14) if right else x0
                self.pill(screen, lx - S(14), y - S(26), lab + gw + S(42), S(52), 150)
                self.text(screen, "POW", lx, y, 30, CREAM, valign="middle")
                gx = lx + lab + S(14)
                pg.draw.rect(screen, (150, 156, 176), (int(gx), y - S(12), gw, S(24)), border_radius=S(12))
                pg.draw.rect(screen, (24, 20, 34), (int(gx) + S(3), y - S(9), gw - S(6), S(18)), border_radius=S(9))
                frac = _clamp(pw / 4.0)
                if frac > 0:
                    full = frac >= 1.0
                    col = _mix(GOLD, WHITE, 0.5 + 0.5 * math.sin(now * 10)) if full else (255, 150, 60)
                    pg.draw.rect(screen, col, (int(gx) + S(3), y - S(9), int((gw - S(6)) * frac), S(18)), border_radius=S(9))
                    pg.draw.rect(screen, (255, 230, 180), (int(gx) + S(8), y - S(6), max(1, int((gw - S(16)) * frac)), S(4)),
                                 border_radius=S(2))
            if spd is not None:                                        # speed: five pips next to it
                lab = hd.text(tr("VITESSE", "SPEED"), "bold", S(24), CREAM)["w"]
                sx = x0 - S(300) - S(110) - lab - 5 * S(24) - S(30) if right else x0 + S(300) + S(110)
                self.pill(screen, sx - S(14), y - S(22), lab + 5 * S(24) + S(40), S(44), 150)
                self.text(screen, tr("VITESSE", "SPEED"), sx, y, 24, CREAM, key="bold", valign="middle", glow=0)
                for i in range(5):
                    on = i < int(spd)
                    pg.draw.rect(screen, (110, 200, 255) if on else (30, 44, 60), (int(sx + lab + S(14) + i * S(24)), y - S(13), S(18), S(26)),
                                 border_radius=S(4))


# ============================================================================ Aero Fighters 2 et 3 (vu du ciel)
def _sym(pts):
    """A shape of the upper half of a plane (y < 0.5) and its mirror. / Une moitié d'avion et son reflet."""
    return [pts, [(x, 1 - y) for x, y in pts]]


def jet_draw(style, body, accent, dark=(30, 34, 46)):
    """Jet fighters of Aero Fighters 2 seen from above, nose to the right: 'tomcat' with swing wings swept back, two
    engines apart and two fins, 'hornet' with straight wings, strakes along the nose and two fins leaning out.
    / Les chasseurs d'Aero Fighters 2 vus du dessus : ailes en flèche et deux réacteurs, ou ailes droites et virures."""
    def fn(d, W, H):
        line = dark + (255,)
        ow = max(1.0, W * 0.012)
        b = body + (255,)
        lt, sh, sh2 = _mix(body, WHITE, 0.35) + (255,), _mix(body, (0, 0, 0), 0.22) + (255,), _mix(body, (0, 0, 0), 0.4) + (255,)
        acc = accent + (255,)

        def P(pts):
            return [(x * W, y * H) for x, y in pts]
        if style == "tomcat":
            for half in _sym([(0.17, 0.42), (0.02, 0.16), (0.08, 0.15), (0.24, 0.42)]):                       # empennage
                _shape(d, P(half), sh, line, ow)
            for half in _sym([(0.5, 0.38), (0.3, 0.02), (0.22, 0.03), (0.3, 0.38)]):                          # ailes en flèche
                _shape(d, P(half), sh, line, ow)
            for half in _sym([(0.47, 0.37), (0.3, 0.05), (0.27, 0.06), (0.36, 0.37)]):
                d.polygon(P(half), fill=b)
            for half in _sym([(0.28, 0.07), (0.25, 0.04), (0.23, 0.05)]):
                d.polygon(P(half), fill=acc)
            for half in _sym([(0.64, 0.42), (0.46, 0.27), (0.38, 0.27), (0.4, 0.42)]):                        # gants d'aile
                _shape(d, P(half), b, line, ow)
            for y in (0.36, 0.64):                                                                          # réacteurs écartés
                _shape(d, P([(0.56, y - 0.07), (0.06, y - 0.07), (0.03, y - 0.05), (0.03, y + 0.05), (0.06, y + 0.07), (0.56, y + 0.07)]), sh, line, ow)
                d.rectangle(P([(0.01, y - 0.045), (0.05, y + 0.045)])[0] + P([(0.01, y - 0.045), (0.05, y + 0.045)])[1], fill=(60, 60, 70, 255))
                _shape(d, P([(0.58, y - 0.07), (0.5, y - 0.07), (0.5, y + 0.07), (0.58, y + 0.07)]), sh2, line, ow)        # entrées d'air
            _shape(d, P([(0.62, 0.38), (0.12, 0.4), (0.12, 0.6), (0.62, 0.62)]), b, line, ow)                 # corps plat
            for y in (0.4, 0.6):                                                                            # dérives
                d.line(P([(0.08, y), (0.3, y)]), fill=line, width=int(H * 0.035))
                d.line(P([(0.09, y), (0.28, y)]), fill=lt, width=max(1, int(H * 0.012)))
            nose = [(1.0, 0.5), (0.92, 0.46), (0.62, 0.43), (0.62, 0.57), (0.92, 0.54)]
        else:
            for half in _sym([(0.2, 0.44), (0.04, 0.24), (0.1, 0.23), (0.27, 0.44)]):                         # empennage
                _shape(d, P(half), sh, line, ow)
            for half in _sym([(0.56, 0.42), (0.42, 0.06), (0.33, 0.06), (0.32, 0.42)]):                      # ailes droites
                _shape(d, P(half), sh, line, ow)
            for half in _sym([(0.53, 0.41), (0.42, 0.1), (0.36, 0.1), (0.36, 0.41)]):
                d.polygon(P(half), fill=b)
            for half in _sym([(0.44, 0.04), (0.31, 0.04), (0.31, 0.065), (0.44, 0.065)]):                    # missiles en bout d'aile
                _shape(d, P(half), (236, 236, 240, 255), line, ow * 0.7)
            for half in _sym([(0.86, 0.47), (0.56, 0.37), (0.5, 0.4)]):                                      # virures
                _shape(d, P(half), b, line, ow)
            for half in _sym([(0.32, 0.44), (0.14, 0.36), (0.1, 0.38), (0.24, 0.45)]):                       # dérives inclinées
                _shape(d, P(half), sh2, line, ow)
            _shape(d, P([(0.62, 0.42), (0.08, 0.43), (0.05, 0.46), (0.05, 0.54), (0.08, 0.57), (0.62, 0.58)]), b, line, ow)
            for y in (0.46, 0.54):
                d.rectangle(P([(0.03, y - 0.025), (0.06, y + 0.025)])[0] + P([(0.03, y - 0.025), (0.06, y + 0.025)])[1], fill=(60, 60, 70, 255))
            nose = [(1.0, 0.5), (0.9, 0.465), (0.62, 0.43), (0.62, 0.57), (0.9, 0.535)]
        _shape(d, P(nose), b, line, ow)
        d.polygon(P([(0.98, 0.5), (0.92, 0.475), (0.86, 0.475), (0.86, 0.5)]), fill=lt)                       # radôme éclairé
        d.polygon(P([(0.6, 0.47), (0.15, 0.47), (0.15, 0.49), (0.6, 0.49)]), fill=lt)                          # reflet du dos
        d.line(P([(0.16, 0.5), (0.62, 0.5)]), fill=acc, width=max(1, int(H * 0.02)))
        _shape(d, P([(0.86, 0.5), (0.8, 0.465), (0.7, 0.465), (0.68, 0.5), (0.7, 0.535), (0.8, 0.535)]), (40, 80, 140, 255), line, ow)     # verrière
        d.polygon(P([(0.82, 0.49), (0.79, 0.475), (0.73, 0.475), (0.73, 0.49)]), fill=(170, 220, 255, 255))
    return fn


def heli_draw(d, W, H):
    """Enemy helicopter seen from above, nose to the left (its rotor is drawn apart). / Hélicoptère ennemi vu du dessus."""
    line = (24, 30, 22, 255)
    ow = max(1.0, W * 0.02)
    body, lt, sh = (80, 120, 64, 255), (130, 170, 100, 255), (56, 84, 44, 255)
    _shape(d, [(0.5 * W, 0.46 * H), (0.98 * W, 0.47 * H), (0.98 * W, 0.53 * H), (0.5 * W, 0.54 * H)], sh, line, ow)       # poutre de queue
    _shape(d, [(0.92 * W, 0.36 * H), (0.98 * W, 0.36 * H), (0.98 * W, 0.64 * H), (0.92 * W, 0.64 * H)], sh, line, ow)     # dérive
    for y in (0.3, 0.7):                                                                             # ailerons et roquettes
        _shape(d, [(0.36 * W, 0.5 * H), (0.42 * W, y * H), (0.5 * W, y * H), (0.5 * W, 0.5 * H)], sh, line, ow)
        d.rounded_rectangle([0.32 * W, (y - 0.04) * H, 0.48 * W, (y + 0.04) * H], radius=H * 0.03, fill=(150, 150, 140, 255), outline=line)
    d.ellipse([0.08 * W, 0.34 * H, 0.62 * W, 0.66 * H], fill=body, outline=line, width=int(ow))
    d.chord([0.12 * W, 0.37 * H, 0.58 * W, 0.6 * H], 180, 360, fill=lt)
    d.ellipse([0.08 * W, 0.4 * H, 0.26 * W, 0.6 * H], fill=(60, 110, 150, 255), outline=line, width=int(ow))         # verrière
    d.ellipse([0.11 * W, 0.43 * H, 0.17 * W, 0.49 * H], fill=(190, 230, 255, 255))


def rotor_draw(d, W, H):
    """Blades of a rotor, turned by the scene. / Pales d'un rotor, que la scène fait tourner."""
    cx, cy, r = W / 2, H / 2, W / 2
    d.ellipse([0, 0, W - 1, H - 1], fill=(200, 210, 200, 40))
    for a in (0, 90):
        t = math.radians(a)
        dx, dy = math.cos(t) * r, math.sin(t) * r
        nx, ny = -math.sin(t) * r * 0.05, math.cos(t) * r * 0.05
        d.polygon([(cx - dx + nx, cy - dy + ny), (cx + dx + nx, cy + dy + ny), (cx + dx - nx, cy + dy - ny), (cx - dx - nx, cy - dy - ny)],
                  fill=(40, 44, 40, 230))
    d.ellipse([cx - r * 0.1, cy - r * 0.1, cx + r * 0.1, cy + r * 0.1], fill=(60, 60, 60, 255))


def enemy_jet_draw(d, W, H):
    """Enemy jet seen from above, nose to the left: delta wings, dark green and sand camouflage, red nose.
    / Chasseur ennemi vu du dessus, nez à gauche : aile delta, camouflage vert sombre et sable."""
    line = (24, 22, 26, 255)
    ow = max(1.0, W * 0.016)
    body, wing, camo = (110, 116, 90, 255), (86, 96, 70, 255), (150, 140, 100, 255)
    for half in ([(0.34, 0.44), (0.78, 0.04), (0.9, 0.06), (0.86, 0.44)], [(0.34, 0.56), (0.78, 0.96), (0.9, 0.94), (0.86, 0.56)]):
        _shape(d, [(x * W, y * H) for x, y in half], wing, line, ow)
    d.polygon([(0.6 * W, 0.3 * H), (0.76 * W, 0.12 * H), (0.82 * W, 0.2 * H), (0.7 * W, 0.34 * H)], fill=camo)
    d.polygon([(0.6 * W, 0.7 * H), (0.76 * W, 0.88 * H), (0.82 * W, 0.8 * H), (0.7 * W, 0.66 * H)], fill=camo)
    _shape(d, [(0.0, 0.5 * H), (0.16 * W, 0.44 * H), (0.98 * W, 0.45 * H), (0.98 * W, 0.55 * H), (0.16 * W, 0.56 * H)], body, line, ow)
    d.line([(0.84 * W, 0.5 * H), (1.0 * W, 0.5 * H)], fill=line, width=max(1, int(H * 0.06)))
    d.polygon([(0.0, 0.5 * H), (0.1 * W, 0.465 * H), (0.1 * W, 0.535 * H)], fill=(190, 60, 46, 255))
    d.ellipse([0.16 * W, 0.46 * H, 0.32 * W, 0.54 * H], fill=(60, 100, 140, 255), outline=line)


def prop_enemy_draw(d, W, H):
    """Enemy propeller fighter seen from above, nose to the left, olive with a yellow nose. / Chasseur ennemi à hélice."""
    line = (24, 20, 30, 255)
    ow = max(1.0, W * 0.018)
    body, wing, lt = (96, 104, 76, 255), (84, 92, 66, 255), (130, 140, 104, 255)
    _shape(d, [(0.34 * W, 0.47 * H), (0.38 * W, 0.04 * H), (0.5 * W, 0.04 * H), (0.52 * W, 0.47 * H)], wing, line, ow)
    _shape(d, [(0.34 * W, 0.53 * H), (0.38 * W, 0.96 * H), (0.5 * W, 0.96 * H), (0.52 * W, 0.53 * H)], wing, line, ow)
    d.line([(0.37 * W, 0.08 * H), (0.37 * W, 0.92 * H)], fill=lt, width=max(1, int(W * 0.02)))
    _shape(d, [(0.82 * W, 0.3 * H), (0.92 * W, 0.3 * H), (0.92 * W, 0.7 * H), (0.82 * W, 0.7 * H)], wing, line, ow)
    _shape(d, [(0.06 * W, 0.5 * H), (0.14 * W, 0.42 * H), (0.96 * W, 0.46 * H), (0.96 * W, 0.54 * H), (0.14 * W, 0.58 * H)], body, line, ow)
    d.ellipse([0.3 * W, 0.45 * H, 0.44 * W, 0.55 * H], fill=(170, 200, 210, 255), outline=line)
    d.ellipse([0.0, 0.1 * H, 0.08 * W, 0.9 * H], fill=(220, 220, 220, 90))
    d.ellipse([0.04 * W, 0.44 * H, 0.13 * W, 0.56 * H], fill=(230, 196, 60, 255), outline=line)


def bomber_draw(d, W, H):
    """Big enemy bomber seen from above, nose to the left: long straight wings with two engines, a glass nose, twin
    tails. / Gros bombardier ennemi vu du dessus : longues ailes, deux moteurs, nez vitré."""
    line = (22, 26, 20, 255)
    ow = max(1.0, W * 0.012)
    body, wing, lt = (92, 120, 80, 255), (78, 104, 68, 255), (130, 160, 110, 255)
    _shape(d, [(0.36 * W, 0.47 * H), (0.42 * W, 0.02 * H), (0.56 * W, 0.02 * H), (0.6 * W, 0.47 * H)], wing, line, ow)
    _shape(d, [(0.36 * W, 0.53 * H), (0.42 * W, 0.98 * H), (0.56 * W, 0.98 * H), (0.6 * W, 0.53 * H)], wing, line, ow)
    d.line([(0.4 * W, 0.06 * H), (0.4 * W, 0.94 * H)], fill=lt, width=max(1, int(W * 0.012)))
    for y in (0.24, 0.76):                                                                           # moteurs
        _shape(d, [(0.22 * W, y * H - 0.05 * H), (0.62 * W, y * H - 0.05 * H), (0.62 * W, y * H + 0.05 * H), (0.22 * W, y * H + 0.05 * H)],
               (70, 90, 62, 255), line, ow)
        d.ellipse([0.19 * W, y * H - 0.12 * H, 0.23 * W, y * H + 0.12 * H], fill=(220, 220, 220, 90))
    _shape(d, [(0.84 * W, 0.24 * H), (0.94 * W, 0.24 * H), (0.94 * W, 0.76 * H), (0.84 * W, 0.76 * H)], wing, line, ow)
    for y in (0.26, 0.74):
        d.line([(0.86 * W, y * H), (0.97 * W, y * H)], fill=line, width=max(1, int(H * 0.04)))
    _shape(d, [(0.02 * W, 0.5 * H), (0.1 * W, 0.42 * H), (0.98 * W, 0.45 * H), (0.98 * W, 0.55 * H), (0.1 * W, 0.58 * H)], body, line, ow)
    d.polygon([(0.12 * W, 0.46 * H), (0.9 * W, 0.47 * H), (0.9 * W, 0.49 * H), (0.12 * W, 0.48 * H)], fill=lt)
    d.ellipse([0.02 * W, 0.44 * H, 0.14 * W, 0.56 * H], fill=(150, 200, 230, 220), outline=line)
    d.ellipse([0.24 * W, 0.46 * H, 0.34 * W, 0.54 * H], fill=(60, 100, 130, 255), outline=line)


PLANE_BODY = ((46, 70, 120), (40, 40, 48), (196, 196, 176), (90, 110, 86), (88, 108, 70), (96, 128, 72), (120, 128, 128), (110, 120, 86),
              (136, 120, 86), (176, 176, 166), (220, 54, 50), (84, 52, 116))


def prop_plane_draw(kind, accent):
    """The planes of Aero Fighters 3 seen from above, nose to the right: kind 0 Corsair (bent wings), 1 Black Widow
    (twin booms), 2 Zero, 3 Seiran (floats), 4 Sturmovik, 5 I-16 (short and round), 6 Pfeil (a propeller at each end),
    7 Stuka (bent wings, wheel spats), 8 Whirlwind (two engines), 9 Swordfish (biplane), 10 a red racer, 11 a dark plane.
    / Les avions d'Aero Fighters 3 vus du dessus, nez à droite."""
    def fn(d, W, H):
        line = DARK + (255,)
        ow = max(1, int(W * 0.014))
        col = PLANE_BODY[kind % len(PLANE_BODY)]
        b, sh = col + (255,), _mix(col, (0, 0, 0), 0.22) + (255,)
        acc = accent + (255,)
        prop = (230, 230, 236, 80)

        def wings(front, back, span, tip, bent=False, y0=0.0):
            for s_ in (1, -1):
                def m(y):
                    return 0.5 + s_ * (y - 0.5)
                if bent:
                    pts = [(front, m(0.46)), (front - 0.03, m(0.3)), (front - 0.01, m(0.5 - span)), (front - tip, m(0.5 - span)),
                           (back - 0.03, m(0.3)), (back, m(0.46))]
                else:
                    pts = [(front, m(0.46)), (front - 0.05, m(0.5 - span)), (front - tip, m(0.5 - span)), (back, m(0.46))]
                _poly(d, pts, W, H, sh, line, ow)
                d.line([((front - tip * 0.5) * W, m(0.5 - span + 0.03) * H), ((front - tip * 0.3) * W, m(0.5 - span + 0.03) * H)], fill=acc,
                       width=max(2, int(H * 0.03)))

        def tail(x, span):
            for s_ in (1, -1):
                _poly(d, [(x + 0.08, 0.5 + s_ * 0.03), (x + 0.04, 0.5 + s_ * span), (x - 0.02, 0.5 + s_ * span), (x, 0.5 + s_ * 0.03)], W, H, sh,
                      line, ow)

        def fuselage(x0, x1, w):
            _poly(d, [(x1, 0.5), (x1 - 0.06, 0.5 - w), (x0 + 0.04, 0.5 - w * 0.55), (x0, 0.5), (x0 + 0.04, 0.5 + w * 0.55), (x1 - 0.06, 0.5 + w)],
                  W, H, b, line, ow)

        def canopy(x, w=0.08):
            d.ellipse([x * W, (0.5 - 0.035) * H, (x + w) * W, (0.5 + 0.035) * H], fill=(120, 200, 240, 255), outline=line, width=ow)

        def disc(x, y=0.5, r=0.2):
            d.ellipse([(x - 0.025) * W, (y - r) * H, (x + 0.025) * W, (y + r) * H], fill=prop)
            d.ellipse([(x - 0.012) * W, (y - 0.03) * H, (x + 0.02) * W, (y + 0.03) * H], fill=(200, 190, 120, 255))
        if kind == 1:                                                  # P-61 : deux poutres
            wings(0.62, 0.42, 0.47, 0.12)
            for y in (0.33, 0.67):
                _poly(d, [(0.74, y), (0.7, y - 0.05), (0.06, y - 0.03), (0.06, y + 0.03), (0.7, y + 0.05)], W, H, b, line, ow)
                disc(0.76, y, 0.15)
            _poly(d, [(0.1, 0.3), (0.16, 0.3), (0.16, 0.7), (0.1, 0.7)], W, H, sh, line, ow)
            fuselage(0.4, 0.86, 0.06)
            canopy(0.66)
        elif kind == 8:                                                # Whirlwind : deux moteurs
            wings(0.62, 0.44, 0.44, 0.12)
            for y in (0.3, 0.7):
                _poly(d, [(0.76, y), (0.72, y - 0.05), (0.46, y - 0.04), (0.46, y + 0.04), (0.72, y + 0.05)], W, H, b, line, ow)
                disc(0.78, y, 0.14)
            fuselage(0.06, 0.82, 0.06)
            tail(0.06, 0.18)
            canopy(0.6)
        elif kind == 9:                                                # Swordfish : biplan
            wings(0.64, 0.5, 0.47, 0.1)
            wings(0.7, 0.58, 0.45, 0.08)
            for y in (0.2, 0.8):
                d.line([(0.6 * W, y * H), (0.66 * W, y * H)], fill=line, width=max(1, int(W * 0.01)))
            fuselage(0.04, 0.84, 0.06)
            tail(0.04, 0.2)
            disc(0.86)
            canopy(0.5, 0.12)
        else:
            stubby = kind == 5
            fuselage(0.08 if not stubby else 0.24, 0.9 if not stubby else 0.84, 0.065 if not stubby else 0.09)
            span = {5: 0.38, 10: 0.36, 11: 0.4}.get(kind, 0.46)
            wings(0.64 if not stubby else 0.66, 0.46 if not stubby else 0.5, span, 0.12 if kind != 11 else 0.2, bent=kind in (0, 7))
            if kind == 11:
                for s_ in (1, -1):
                    _poly(d, [(0.4, 0.5 + s_ * 0.05), (0.2, 0.5 + s_ * 0.4), (0.14, 0.5 + s_ * 0.4), (0.24, 0.5 + s_ * 0.05)], W, H, sh, line, ow)
            tail(0.08 if not stubby else 0.24, 0.2 if not stubby else 0.17)
            if kind == 3:                                              # Seiran : flotteurs
                for y in (0.34, 0.66):
                    d.rounded_rectangle([0.42 * W, (y - 0.035) * H, 0.88 * W, (y + 0.035) * H], radius=H * 0.03, fill=(220, 220, 210, 255),
                                        outline=line, width=ow)
            if kind == 7:                                              # Stuka : carénages de roues
                for y in (0.36, 0.64):
                    d.ellipse([0.62 * W, (y - 0.03) * H, 0.74 * W, (y + 0.03) * H], fill=sh, outline=line, width=ow)
            if kind == 6:                                              # Pfeil : une hélice à chaque bout
                disc(0.07, 0.5, 0.14)
            canopy(0.58 if kind != 4 else 0.52, 0.08 if kind != 4 else 0.14)
            disc(0.92 if not stubby else 0.86, 0.5, 0.2)
            if kind in (5, 10):
                d.ellipse([0.8 * W, 0.44 * H, 0.9 * W, 0.56 * H], fill=acc)
    return fn


def bomb_draw(d, W, H):
    d.ellipse([0.1 * W, 0.2 * H, 0.86 * W, 0.8 * H], fill=(60, 62, 70, 255), outline=(20, 20, 26, 255), width=max(1, int(H * 0.06)))
    d.polygon([(0.1 * W, 0.5 * H), (0.0, 0.1 * H), (0.0, 0.9 * H)], fill=(80, 82, 90, 255))
    d.ellipse([0.5 * W, 0.3 * H, 0.7 * W, 0.45 * H], fill=(150, 150, 160, 255))


def bomb_icon_draw(color, frame, full=True):
    """Bomb of the panel as in the games: a bomb standing in a rounded frame. / Bombe du panneau, dans un cadre arrondi."""
    def fn(d, W, H):
        d.rounded_rectangle([0, 0, W - 1, H - 1], radius=W * 0.45, fill=(10, 14, 30, 220) if full else (10, 14, 30, 120),
                            outline=frame + (255,), width=max(1, int(W * 0.1)))
        if not full:
            return
        cx = W / 2
        d.polygon([(cx - W * 0.2, H * 0.78), (cx - W * 0.28, H * 0.9), (cx + W * 0.28, H * 0.9), (cx + W * 0.2, H * 0.78)], fill=_mix(color, (0, 0, 0), 0.3) + (255,))
        d.ellipse([cx - W * 0.26, H * 0.16, cx + W * 0.26, H * 0.82], fill=color + (255,), outline=(30, 20, 20, 255), width=max(1, int(W * 0.05)))
        d.ellipse([cx - W * 0.14, H * 0.24, cx - W * 0.02, H * 0.44], fill=(255, 255, 255, 200))
    return fn


def missile_draw(d, W, H):
    d.rounded_rectangle([0.1 * W, 0.3 * H, 0.95 * W, 0.7 * H], radius=H * 0.2, fill=(230, 230, 236, 255), outline=(40, 40, 50, 255),
                        width=max(1, int(H * 0.08)))
    d.polygon([(0.1 * W, 0.3 * H), (0.0, 0.0), (0.24 * W, 0.3 * H)], fill=(200, 60, 50, 255))
    d.polygon([(0.1 * W, 0.7 * H), (0.0, H), (0.24 * W, 0.7 * H)], fill=(200, 60, 50, 255))


def tank_draw(d, W, H):
    """Tank seen from above, gun to the left. / Char vu du dessus, canon à gauche."""
    line = (24, 26, 20, 255)
    d.rounded_rectangle([0.1 * W, 0.0, W, 0.24 * H], radius=H * 0.06, fill=(50, 50, 40, 255))
    d.rounded_rectangle([0.1 * W, 0.76 * H, W, H], radius=H * 0.06, fill=(50, 50, 40, 255))
    d.rounded_rectangle([0.14 * W, 0.16 * H, 0.96 * W, 0.84 * H], radius=H * 0.1, fill=(96, 100, 64, 255), outline=line)
    d.ellipse([0.36 * W, 0.26 * H, 0.76 * W, 0.74 * H], fill=(110, 116, 74, 255), outline=line)
    d.line([(0.4 * W, 0.5 * H), (0.0, 0.5 * H)], fill=line, width=max(2, int(H * 0.1)))


class AeroFightersScene(BlazingStarScene):
    """Seen from high above, as in the games: the planes fly over a city that scrolls by, their shadows below them,
    enemy planes and helicopters (or bombers) come from the right, tanks drive on the avenues. A bomb spent clears the
    screen. At the top 1P: and the score with the lives below, the bombs at the bottom in their frames.
    / Vu du ciel comme dans les jeux : la ville défile sous les avions et leurs ombres, des tanks sur les avenues."""
    THEME = "af_city"
    SHADE = (90, 90)
    PILLS = True
    EXPLOSIONS = True
    BANNERS = GameScene.BANNERS
    ACC = {"p1": (230, 70, 50), "p2": (255, 170, 60)}
    ZONE = (160, 320)                                  # above the panels at the bottom / au-dessus des panneaux du bas
    PROP = False
    SHOT = {"p1": (140, 200, 255), "p2": (255, 210, 130)}
    SHOT_SIZE = ((7, 70), (10, 96))                    # shots: (width, length), weak then strong / tirs : faibles, puis forts
    BOMB = ((230, 50, 40), (70, 120, 255))             # bomb and frame of the panel / bombe et cadre du panneau
    ODD = "heli"                                       # the other enemy, now and then / l'autre ennemi, de temps en temps
    SIZES = {"jet": (96, 90), "prop": (96, 90), "heli": (112, 72), "bomber": (150, 176)}

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.fx.sp.register("af_bomb", draw_img(S(44), S(22), bomb_draw))
        self.fx.sp.register("missile", draw_img(S(40), S(12), missile_draw))
        self.ground = []
        self.wrecks = []
        self.next_ground = 0.0
        self.bombs = 0                                         # bombs shown (tests)
        self.bpop = {"p1": -99.0, "p2": -99.0}
        self.warm = [(self.enemy_surf, (k, sh)) for k in ("prop" if self.PROP else "jet", self.ODD) for sh in (False, True)] + self.warm

    def kind(self, vals, side):
        return None

    def plane_fn(self, side, kind):
        return jet_draw("tomcat" if side == "p1" else "hornet", (150, 158, 170) if side == "p1" else (120, 150, 196), self.ACC[side])

    @staticmethod
    def shadow_of(pg, s, alpha):
        sh = pg.transform.smoothscale(s, (int(s.get_width() * 0.78), int(s.get_height() * 0.78))).copy()
        sh.fill((0, 0, 0, 255), special_flags=pg.BLEND_RGBA_MIN)
        sh.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MIN)
        return sh

    def plane_surf(self, side, kind, shadow=False):
        S = self.S
        key = ("plane", side, kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            s = self.img(("planeimg", side, kind), S(150), S(136), self.plane_fn(side, kind))
            if shadow:
                s = self.shadow_of(self.pg, s, 80)
            self.imgs[key] = s
        return s

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            w, h = self.SIZES.get(kind, (96, 90))
            fn = {"jet": enemy_jet_draw, "prop": prop_enemy_draw, "heli": heli_draw, "bomber": bomber_draw}.get(kind, enemy_jet_draw)
            s = self.img(("enemyimg", kind), S(w), S(h), fn)
            if shadow:
                s = self.shadow_of(self.pg, s, 70)
            self.imgs[key] = s
        return s

    def move(self, vals, now, idle):
        return 0.4 if idle else 1.3

    def restart(self, vals, now):
        super().restart(vals, now)
        self.ground, self.wrecks = [], []
        self.next_ground = now + 1.5

    def gx(self, g):
        return g["wx"] - self.bd.scroll

    def update(self, vals, now):
        super().update(vals, now)
        S = self.S
        for e in self.enemies:                                         # what each new enemy is
            if "type" not in e:
                odd = self.rng.random() < (0.3 if self.ODD == "heli" else 0.14)
                if odd and self.ODD == "bomber" and any(f.get("type") == "bomber" and not f.get("dead") for f in self.enemies):
                    odd = False
                e["type"] = self.ODD if odd else ("prop" if self.PROP else "jet")
                if odd:
                    e["v"] *= 0.6
                    e["hp"] = 8 if self.ODD == "bomber" else 4
        for side, suf in (("p1", ""), ("p2", "_p2")):
            P = self.ships[side]
            if not P["in"]:
                continue
            ch = self.changed(vals, "bombs" + suf)
            if ch and ch[1] < ch[0] and now - P["t_dead"] > 1.2:
                self.bomb(side, now)
            elif ch and ch[1] > ch[0]:
                x, y = self.pos(side, now)
                self.popup(tr("BOMBE +", "BOMB UP"), x, max(S(176), y - S(80)), (255, 190, 90), 36)
                self.bpop[side] = now
        for name in ("score", "score_p2"):                             # points with no plane ahead: a target on the ground
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0]:
                ahead = [e for e in self.enemies if S(420) < e["x"] < self.W * 0.78 and not e.get("dead")]
                if not ahead:
                    side = "p1" if name == "score" else "p2"
                    tgt = [g for g in self.ground if not g.get("dead") and S(300) < self.gx(g) < self.W * 0.9]
                    if tgt and self.ships[side]["in"]:
                        self.strafe(side, min(tgt, key=self.gx), now)
        if now >= self.next_ground:                                    # tanks driving on the avenues
            self.next_ground = now + self.rng.uniform(2.5, 5.0)
            if len([g for g in self.ground if not g.get("dead")]) < 3:
                lane = self.rng.choice([(a + k * 11.5) for a in AF_AVENUES for k in (-1, 1)])
                self.ground.append({"wx": self.bd.scroll + self.W + S(120), "y": S(lane), "v": self.rng.uniform(10, 40) * self.s,
                                    "ph": self.rng.uniform(0, 6)})

    def _fire(self, side, pw, now):
        """Shots like in the games: thick bright bolts, more of them with the power. / Des tirs épais et lumineux."""
        x, y = self.pos(side, now)
        fx, S = self.fx, self.S
        col = self.SHOT[side]
        mx = x + S(80)
        end = self.W + S(60)
        fx.muzzle(mx, y, 1, 0.6, col)
        lanes = (0,) if pw <= 0 else ((-1, 1) if pw == 1 else (-1, 0, 1))
        width, length = self.SHOT_SIZE[1 if pw >= 3 else 0]
        for k in lanes:
            sy = y + k * S(14)
            ty = sy + (k * S(70) if pw >= 2 else 0)
            target = None
            for e in self.enemies:                                    # an enemy in the line of fire is hit
                if e.get("dead") or e["x"] <= mx:
                    continue
                ly = sy + (ty - sy) * (e["x"] - mx) / max(1, end - mx)
                reach = S(60 if e.get("type") == "bomber" else 26)
                if abs(e.get("yy", e["y"]) - ly) < reach and (target is None or e["x"] < target["x"]):
                    target = e
            if target is not None:
                fx.tracer(mx, sy, target["x"], target.get("yy", target["y"]), speed=3000, color=col, width=width, length=length)
                target["hp"] -= 1
                target["hit"] = now
                if target["hp"] <= 0:
                    fx.later(0.12, self._boom, target)
            else:
                fx.tracer(mx, sy, end, ty, speed=3000, color=col, width=width, length=length, impact=False)

    def _boom(self, e):
        if e.get("dead"):
            return
        e["dead"] = True
        self.fx.explosion(e["x"], e.get("yy", e["y"]), 1.0 if e.get("type") == "bomber" else 0.55, layer_back=False)

    def strafe(self, side, g, now):
        x, y = self.pos(side, now)
        gx = self.gx(g)
        for i in range(3):
            self.fx.later(i * 0.05, self.fx.tracer, x + self.S(60), y + (i - 1) * self.S(8), gx, g["y"], 3000, (255, 230, 140), 3, 80, "front",
                          True)
        self.fx.later(0.2, self._ground_boom, g)

    def _ground_boom(self, g):
        if g.get("dead"):
            return
        g["dead"] = True
        x = self.gx(g)
        self.fx.small_blast(x, g["y"], 1.2, "back")
        self.fx.smoke(x, g["y"], 5, (10, 20), 2.4, (1.0, 1.8), (10, 30), 20, (60, 56, 60), 160, "back")
        self.wrecks.append({"wx": g["wx"], "y": g["y"], "t": self.fx.now})

    def bomb(self, side, now):
        """A bomb: the screen is cleared. / Une bombe : l'écran est nettoyé."""
        fx, S, rng = self.fx, self.S, self.rng
        x, y = self.pos(side, now)
        self.bombs += 1
        self.bpop[side] = now
        self.popup(tr("BOMBE !", "BOMB!"), x, max(S(176), y - S(80)), (255, 170, 80), 40)
        if self.PROP:                                                  # a big bomb falls, then one huge blast
            tx = min(self.W * 0.75, x + S(420))
            fx.projectile("af_bomb", x + S(20), y, tx, y + S(10), 0.7, 0, lambda a, b: self._carpet(a, b, 1.6), spin=0.0, trail=0)
        else:                                                          # a salvo of missiles, then the blasts
            for i in range(10):
                ty = S(self.ZONE[0]) + (S(self.ZONE[1]) - S(self.ZONE[0])) * (i + 0.5) / 10
                tx = x + S(500) + rng.uniform(0, S(700))
                p = fx.projectile("missile", x + S(40), y, tx, ty, 0.5 + 0.04 * i, rng.uniform(-30, 30), lambda a, b: fx.explosion(a, b, 0.6,
                                                                                                                                   False),
                                  spin=0.0, kind="rocket", trail=0.02)
                p.rot = -math.degrees(math.atan2(ty - y, tx - x))
            fx.later(0.55, self._carpet, x + S(600), y, 0.0)
        for e in self.enemies:
            if not e.get("dead"):
                fx.later(0.5 + rng.uniform(0, 0.4), self._boom, e)
        for g in self.ground:
            if not g.get("dead") and self.gx(g) > x:
                fx.later(0.6 + rng.uniform(0, 0.3), self._ground_boom, g)

    def _carpet(self, x, y, size):
        fx = self.fx
        if size > 0:
            fx.explosion(x, y, size, layer_back=False)
        fx.flash((255, 220, 160), 0.45, 0.4)
        fx.shake(10, 0.5)
        self.bd.excite(1.0)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, pg, dt, sp = self.S, self.pg, self.dt, self.fx.sp
        add = pg.BLEND_RGB_ADD
        wreck = self.imgs.get("wreck")
        if wreck is None:
            wreck = self.imgs["wreck"] = pg.Surface((S(46), S(30)), pg.SRCALPHA)
            pg.draw.ellipse(wreck, (20, 18, 16, 150), wreck.get_rect())
        self.wrecks = [w for w in self.wrecks if self.gx(w) > -S(60) and now - w["t"] < 20]
        for w in self.wrecks:                                          # scorch marks left on the ground
            screen.blit(wreck, (int(self.gx(w) - S(23)), int(w["y"] - S(15))))
        gimg = self.img(("ground", "tank"), S(64), S(30), tank_draw)
        keep = []
        for g in self.ground:                                          # tanks driving slowly on the avenues
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
        for e in self.enemies:                                         # enemy planes and their shadows
            if e.get("dead"):
                continue
            e["x"] -= e["v"] * dt
            if e["x"] < -S(140):
                continue
            e["yy"] = e["y"] + math.sin(now * 1.6 + e["ph"]) * S(20 if e.get("type") != "bomber" else 8)
            keep.append(e)
            sh = self.enemy_surf(e.get("type", "jet"), True)
            screen.blit(sh, (int(e["x"] + S(50) - sh.get_width() / 2), int(e["yy"] + S(36) - sh.get_height() / 2)))
        for e in keep:
            kind = e.get("type", "jet")
            tilt = 0 if kind == "heli" else (5 if kind == "bomber" else 14)
            img = self.rotated(("enemy_r", kind), self.enemy_surf(kind), _clamp(math.cos(now * 1.6 + e["ph"]) * tilt, -tilt, tilt), 4)
            screen.blit(img, (int(e["x"] - img.get_width() / 2), int(e["yy"] - img.get_height() / 2)))
            if kind == "heli":                                         # the rotor turns
                base = self.img("rotor", S(124), S(124), rotor_draw)
                rot = self.rotated("rotor", base, (now * 1400 + e["ph"] * 40) % 90, 15)
                screen.blit(rot, (int(e["x"] - S(17) - rot.get_width() / 2), int(e["yy"] - rot.get_height() / 2)))
            if now - e["hit"] < 0.06:
                h = sp.glow(S(44 if kind != "bomber" else 80), (255, 255, 255), 8, hot=0.6)
                screen.blit(h, (int(e["x"] - h.get_width() / 2), int(e["yy"] - h.get_height() / 2)), special_flags=add)
        self.enemies = keep
        planes = []
        for side in ("p1", "p2"):
            P = self.ships[side]
            if not P["in"] or now - P["t_dead"] < 1.2 or now < P["t_spawn"]:
                continue
            if now - P["t_spawn"] < 1.6 and int(now * 14) % 2 == 0:
                continue
            kind = self.kind(vals, side)
            x, y = self.pos(side, now)
            planes.append((side, kind, x, y))
            sh = self.plane_surf(side, kind, True)
            screen.blit(sh, (int(x + S(64) - sh.get_width() / 2), int(y + S(44) - sh.get_height() / 2)))
        for side, kind, x, y in planes:
            P = self.ships[side]
            if not self.PROP:                                          # jet engines
                for dy in ((-S(9), S(9)) if side == "p1" else (-S(4), S(4))):
                    fl = sp.streak(S(40) + S(6) * math.sin(now * 40 + dy), S(9), (255, 170, 90), 0, 10)
                    screen.blit(fl, (int(x - S(74) - fl.get_width()), int(y + dy - fl.get_height() / 2)), special_flags=add)
            img = self.rotated(("planer", side, kind), self.plane_surf(side, kind), _clamp(-P["vy"] * 8, -14, 14), 2)
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        self.status(screen, eng, vals, logo, now)

    def life_icon(self, side, vals):
        key = ("aflife", side, self.kind(vals, side))
        icon = self.imgs.get(key)
        if icon is None:                                               # light on the dark pill
            icon = self.hd._surf(draw_img(self.S(40), self.S(36), self.plane_fn(side, self.kind(vals, side))))
            icon.fill((214, 222, 236, 0), special_flags=self.pg.BLEND_RGBA_MAX)
            self.imgs[key] = icon
        return icon

    def status(self, screen, eng, vals, logo, now):
        """As in the games: 1P: and the score at the top with small planes for the lives, the bombs at the bottom in
        their frames, the power next to them. / Comme dans les jeux : 1P: et le score, les vies, les bombes en bas."""
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(560), S(112), now)
        for side in ("p1", "p2"):
            right = side == "p2"
            if right and not self.p2_in(vals):
                word, col = self.invite(vals, now)
                self.label(screen, word, W - S(24), S(44), 36, col, align="right")
                continue
            suf = "_p2" if right else ""
            x0 = W - S(30) if right else S(30)
            sc = _n(vals.get("score" + suf))
            tag = "2P:" if right else "1P:"
            tw_ = hd.text(tag, "black", S(40), CREAM)["w"]
            sw = hd.text(str(sc), "black", S(56), WHITE)["w"] if sc is not None else 0
            self.pill(screen, (x0 - tw_ - sw - S(34)) if right else x0 - S(16), S(8), tw_ + sw + S(48), S(70), 150)
            if right:
                if sc is not None:
                    hd._score(screen, eng, "score" + suf, x0, S(14), "right", S(56))
                self.text(screen, tag, x0 - sw - S(16), S(22), 40, CREAM, align="right")
            else:
                self.text(screen, tag, x0, S(22), 40, CREAM)
                if sc is not None:
                    hd._score(screen, eng, "score" + suf, x0 + tw_ + S(16), S(14), "left", S(56))
            lives = _n(vals.get("lives" + suf))
            if lives is not None and lives > 0:                        # lives: small planes under the score
                icon = self.life_icon(side, vals)
                n = min(6, int(lives))
                lw = n * S(44)
                bx = x0 - lw if right else x0
                self.pill(screen, bx - S(10), S(82), lw + S(20), S(44), 140)
                for i in range(n):
                    screen.blit(icon, (int(bx + i * S(44)), S(86)))
            bombs, pw = _n(vals.get("bombs" + suf)), _n(vals.get("power" + suf))
            y = S(392)
            if bombs is not None:                                      # bombs in their frames, as in the games
                k = max(0.0, 1 - (now - self.bpop[side]) / 0.5)
                n = min(7, int(bombs))
                bimg = self.img(("bombicon", self.BOMB), S(30), S(46), bomb_icon_draw(*self.BOMB))
                bw = max(1, n) * S(36)
                bx = x0 - bw if right else x0
                self.pill(screen, bx - S(10), y - S(32), bw + S(20), S(64), 150)
                for i in range(n):
                    screen.blit(bimg, (int(bx + i * S(36)), y - S(23) - int(S(6) * k)))
                px = bx - S(30) if right else bx + bw + S(30)
            else:
                px = x0
            if pw is not None:                                         # power
                mx = self.power_max(vals, side)
                lab = hd.text("POWER", "bold", S(22), CREAM)["w"]
                gw = lab + S(14) + mx * S(40) + S(64)
                lx = px - gw if right else px
                self.pill(screen, lx - S(12), y - S(22), gw + S(24), S(44), 150)
                self.text(screen, "POWER", lx, y, 22, CREAM, key="bold", valign="middle", glow=0)
                for i in range(mx):
                    on = i < int(pw)
                    pg.draw.rect(screen, (255, 210, 70) if on else (58, 46, 26), (int(lx + lab + S(14) + i * S(40)), y - S(12), S(34), S(24)),
                                 border_radius=S(5))
                if pw >= mx:
                    self.text(screen, "MAX", lx + lab + S(14) + mx * S(40) + S(8), y, 22, GOLD, key="black", valign="middle",
                              scale=1 + 0.08 * math.sin(now * 10))

    def power_max(self, vals, side):
        return 3


class AeroFighters2Scene(AeroFightersScene):
    THEME = "af_city"


class AeroFighters3Scene(AeroFightersScene):
    """Aero Fighters 3: propeller planes over a city by a river at nightfall, the plane of the pilot chosen by player 1,
    big bombers now and then. / Des avions à hélice au-dessus d'une ville au bord d'un fleuve, à la tombée de la nuit."""
    THEME = "af_night"
    PROP = True
    PMAX = {3: 2, 4: 2, 5: 4, 7: 4, 9: 1}
    SHOT = {"p1": (255, 240, 170), "p2": (170, 230, 255)}
    SHOT_SIZE = ((6, 60), (9, 84))
    BOMB = ((70, 190, 80), (200, 204, 214))
    ODD = "bomber"

    def kind(self, vals, side):
        if side != "p1":
            return -1
        v = _n(vals.get("plane"))
        return int(v) if v is not None and 0 <= v < 12 else -1

    def plane_fn(self, side, kind):
        if kind is None or kind < 0:
            return prop_plane_draw(2, self.ACC[side])
        return prop_plane_draw(kind, self.ACC[side])

    def power_max(self, vals, side):
        k = self.kind(vals, side)
        return self.PMAX.get(k, 3) if k is not None and k >= 0 else 3

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "plane")
        if ch and self.ships["p1"]["in"]:
            x, y = self.pos("p1", now)
            self.fx.glow(x, y, 30, 160, (255, 230, 160), 0.4, "front", 0.9, 0.0)

    def status(self, screen, eng, vals, logo, now):
        super().status(screen, eng, vals, logo, now)
        pilot, plane = vals.get("pilot_name"), vals.get("plane_name")
        if isinstance(pilot, str) and pilot and self.p1_in(vals):
            txt = pilot + (f"  ·  {plane}" if isinstance(plane, str) and plane else "")
            self.label(screen, txt, self.W / 2, self.S(412), 28, GOLD, key="xbold", align="center", alpha=130)


SCENES = {"tophuntr": TopHunterScene, "bstars2": BaseballScene, "lresort": LastResortScene, "sonicwi2": AeroFighters2Scene,
          "sonicwi3": AeroFighters3Scene}
