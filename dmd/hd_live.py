"""The lively side of the Metal Slug HD scene (1.40), for the games whose file asks for it ("hd": {"dynamic": true}).

The two soldier cards move with the game instead of standing still:
- the boss of the mission comes: the cards slide off the screen, WARNING takes the whole screen between two hazard
  bands, then the cards come back small at the bottom and the boss's life runs across the top; a pale part of the bar
  shows the hits just taken, and the bar bursts when the boss falls;
- a life lost knocks the soldier's card back, a vehicle blown up or a boss down blows both cards outwards;
- the weapon's picture flips when the weapon changes, the card's frame beats red on the last life;
- the mission ends (the game's own end-of-mission screens, the value "mission_ending"): a full-screen show of what was
  counted during the mission, player against player: the duel of the scores over the curve of the mission, one figure
  after the other, then each one's rank and medals.
Every figure is counted where the scene already reacts (a shot, a throw, a life lost, a weapon picked up): the program
reads values of the game, not its picture, so enemies shot down and accuracy are not counted and not shown.

Le côté vivant de la scène HD des Metal Slug, pour les jeux dont le fichier le demande ("hd": {"dynamic": true}).
Les deux cartes des soldats bougent avec le jeu : elles sortent pour le WARNING du boss et reviennent en petit en bas
pendant que sa vie prend le haut de l'écran, une vie perdue repousse la carte, l'arme se retourne quand elle change, le
cadre bat en rouge sur la dernière vie, et la fin de mission donne un spectacle plein écran de ce qui a été compté
pendant la mission, joueur contre joueur. Chaque chiffre est compté là où la scène réagit déjà ; le programme lit des
valeurs du jeu, pas son image.
"""

import math

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

from .hd_fx import FIRE_HOT, Particle
from .i18n import tr

SY, SH, SCUT = 286, 146, 16          # the small card: its top, its height, its cut corners (reference screen 1920 x 460)
SLOT = (526, 73, 95, 54)             # the weapon's picture in the small card: from its outer edge, from its top, size
INFO = 296                           # and its name, its gauge, from the outer edge / son nom, sa jauge
WARN_T = 2.4                         # WARNING holds the screen that long / le WARNING tient l'écran ce temps-là
DOWN_T = 2.6                         # BOSS DESTROYED stays that long / BOSS DÉTRUIT reste ce temps-là
STEP = 3.0                           # one point of the mission's curve every so many seconds / un point de la courbe
COUNTS = ("prisoners", "lives_lost", "continues", "shots", "grenades", "weapons")
VEIL = (8, 10, 22)                   # the dark veil of the show / le voile sombre du spectacle
HAZARD, HAZARD_DARK = (240, 182, 42), (22, 18, 10)
MEDALS = {"mvp": ("MVP", "MVP"), "saver": ("SAUVETEUR", "RESCUER"), "trigger": ("ROI DE LA GÂCHETTE", "TRIGGER HAPPY"),
          "gunner": ("ARTILLEUR", "GRENADIER"), "hothead": ("TÊTE BRÛLÉE", "DAREDEVIL"), "thrifty": ("ÉCONOME", "THRIFTY"),
          "clean": ("SANS UNE ÉGRATIGNURE", "NOT A SCRATCH"), "nocont": ("SANS CONTINUE", "NO CONTINUE")}


def clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else (hi if v > hi else v)


def ease_out(p):
    return 1 - (1 - p) ** 3


def ease_in(p):
    return p * p * p


def ease_io(p):
    return 4 * p * p * p if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def ease_back(p):
    """Past the end, then back to it. / Dépasse l'arrivée puis y revient."""
    c = 1.70158
    return 1 + (c + 1) * (p - 1) ** 3 + c * (p - 1) ** 2


def elastic(p):
    """0 to 1 like a spring let go. / De 0 à 1 comme un ressort lâché."""
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    return 2 ** (-9 * p) * math.sin((p * 10 - 0.75) * (2 * math.pi / 3)) + 1


def minutes(seconds):
    seconds = max(0, int(round(seconds)))
    return f"{seconds // 60}'{seconds % 60:02d}"


def put_num(hd, screen, text, key, size, color, x, y, align="left", glow=0.5, alpha=1.0):
    """A number laid digit by digit, its middle at y, see-through when alpha < 1 (hd.put_number has no alpha).
    / Un nombre posé chiffre par chiffre, son milieu en y, transparent si alpha < 1."""
    total = hd.text_width(text, key, size)
    x0 = x if align == "left" else (x - total / 2 if align == "center" else x - total)
    _, top, _, bottom, _ = hd._glyph(key, size, "0")
    y -= (bottom - top) / 2
    pen = 0.0
    for c in text:
        left, t, adv, _, _ = hd._glyph(key, size, c)
        if c.strip():
            hd.put(screen, hd.text(c, key, size, color, glow), x0 + pen + left, y + (t - top), alpha=alpha)
        pen += adv
    return total


class Tw:
    """A value on its way to another one, eased. / Une valeur en route vers une autre, en douceur."""
    __slots__ = ("a", "b", "t0", "dur", "ease")

    def __init__(self, v=0.0):
        self.a = self.b = v
        self.t0, self.dur, self.ease = 0.0, 0.0, ease_out

    def to(self, v, now, dur, ease=ease_out):
        if v == self.b:
            return
        self.a = self.at(now)
        self.b, self.t0, self.dur, self.ease = v, now, dur, ease

    def set(self, v):
        self.a = self.b = v
        self.dur = 0.0

    def at(self, now):
        if self.dur <= 0:
            return self.b
        p = (now - self.t0) / self.dur
        if p >= 1:
            return self.b
        if p <= 0:
            return self.a
        return self.a + (self.b - self.a) * self.ease(p)


class Tally:
    """What was counted during one mission, for each player: the figures, when each thing happened, and the score
    through time. / Ce qui a été compté pendant une mission, par joueur : les chiffres, le moment de chaque chose, et le
    score au fil du temps."""

    def __init__(self, now, mission):
        self.mission, self.t0 = mission, now
        self.n = {side: dict.fromkeys(COUNTS, 0) for side in ("p1", "p2")}
        self.score = {"p1": 0, "p2": 0}          # the points scored during the mission / les points de la mission
        self.sides = []                          # who played in it / qui y a joué
        self.events = []                         # (when, what, who) / (quand, quoi, qui)
        self.series = [(now, 0, 0)]
        self.next_s = now + STEP
        self.boss = [None, None]                 # when its boss came, when it fell / l'arrivée du boss, sa chute
        self.shown = False                       # its show was given / son spectacle a été donné

    def add(self, side, key, n, now, mark=False):
        if key == "score":
            if 0 < n < 10000000:                 # (a wild reading is no score / une lecture folle n'est pas un score)
                self.score[side] += n
            return
        self.n[side][key] += n
        if mark:
            self.events.append((now, key, side))

    def tick(self, now, sides):
        for side in sides:
            if side not in self.sides:
                self.sides.append(side)
        if now >= self.next_s:
            self.series.append((now, self.score["p1"], self.score["p2"]))
            self.next_s = now + STEP


def rank(n, score):
    """S, A, B, C or D for a mission: prisoners and score count for, lives lost and continues against.
    / S, A, B, C ou D pour une mission : les prisonniers et le score comptent pour, les vies perdues et les continues contre."""
    v = 2 * n["prisoners"] + score / 20000.0 - 2 * n["lives_lost"] - 4 * n["continues"]
    return "S" if v >= 20 else ("A" if v >= 10 else ("B" if v >= 0 else ("C" if v >= -6 else "D")))


def medals(tally, sides):
    """The medals of each player. Two players: the best of the two in each matter, nobody when they are level. One
    player: what he did without. / Les médailles de chacun. À deux : le meilleur des deux sur chaque point, personne à
    égalité. Seul : ce dont il s'est passé."""
    out = {side: [] for side in sides}
    if len(sides) == 1:
        n = tally.n[sides[0]]
        if n["lives_lost"] == 0:
            out[sides[0]].append("clean")
        if n["continues"] == 0:
            out[sides[0]].append("nocont")
        return out
    a, b = sides
    for name, key, way in (("mvp", "score", 1), ("saver", "prisoners", 1), ("trigger", "shots", 1), ("gunner", "grenades", 1),
                           ("hothead", "lives_lost", 1), ("thrifty", "shots", -1)):
        va = tally.score[a] if key == "score" else tally.n[a][key]
        vb = tally.score[b] if key == "score" else tally.n[b][key]
        if va == vb or (way > 0 and max(va, vb) <= 0):
            continue
        out[a if (va - vb) * way > 0 else b].append(name)
    for side in sides:
        del out[side][4:]                        # four lines at most / quatre lignes au plus
    return out


def strip_img(M, side, s, accent):
    """The small card (dark glass, edge, hazard bands, the window behind the weapon), drawn for player 1 then mirrored.
    / La petite carte, dessinée pour J1 puis retournée pour J2."""
    ss = 2
    W, H = int(M.PW * s), int(SH * s)
    w, h = W * ss, H * ss
    k = s * ss
    cut = SCUT * k
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shape = [(cut, 0), (w - 1, 0), (w - 1, h - 1 - cut), (w - 1 - cut, h - 1), (0, h - 1), (0, cut)]
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(shape, fill=255)
    grad = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(grad)
    for y in range(h):
        t = y / max(1, h - 1)
        gd.line([0, y, w, y], fill=(int(14 - 6 * t), int(18 - 8 * t), int(38 - 18 * t), int(228 + 14 * t)))
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)
    stripes = Image.new("L", (w, h), 0)
    sd = ImageDraw.Draw(stripes)
    for x in range(int(110 * k), int(330 * k), int(28 * k)):
        sd.polygon([(x, 6 * k), (x + 12 * k, 6 * k), (x - 34 * k, 66 * k), (x - 46 * k, 66 * k)], fill=34)
    img.paste(accent + (255,), (0, 0), ImageChops.multiply(stripes, mask))
    d.line([(16 * k, 72 * k), (w - 16 * k, 72 * k)], fill=accent + (110,), width=max(1, int(2 * k)))
    lx, ly, sw, sh = SLOT
    d.rounded_rectangle([(lx - 6) * k, (ly + 5) * k, (lx + sw + 6) * k, (ly + sh + 8) * k], radius=8 * k, fill=M.CARD_WINDOW)
    d.line(shape + [shape[0]], fill=accent + (190,), width=max(2, int(3 * k)))
    img = img.resize((W, H), Image.LANCZOS)
    return img if side == "p1" else ImageOps.mirror(img)


def outline(M, side, s, height, cut, pad):
    """The red frame of the last life: a thick line right on the card's own outline, cut corners included, with its glow
    and a light thread in the middle. / Le cadre rouge de la dernière vie : un trait épais posé sur le contour même de la
    carte, coins coupés compris, avec sa lueur et un filet clair."""
    ss = 2
    k = s * ss
    w, h = int(M.PW * s) * ss, int(height * s) * ss
    p = int(pad * k)
    c = cut * k
    pts = [(c, 0), (w - 1, 0), (w - 1, h - 1 - c), (w - 1 - c, h - 1), (0, h - 1), (0, c)]
    pts = [(x + p, y + p) for x, y in pts]
    size = ((w + 2 * p) // ss, (h + 2 * p) // ss)
    line = Image.new("L", (w + 2 * p, h + 2 * p), 0)
    ImageDraw.Draw(line).line(pts + [pts[0], pts[1]], fill=255, width=max(2, int(7 * k)), joint="curve")
    line = line.resize(size, Image.LANCZOS)                    # (the glow is made at the screen's size: much quicker)
    glow = line.filter(ImageFilter.GaussianBlur(11 * s)).point(lambda v: min(255, int(v * 2.2)))
    img = Image.new("RGBA", size, (255, 46, 30, 0))
    img.putalpha(glow)
    body = Image.new("RGBA", size, (255, 70, 50, 0))
    body.putalpha(line)
    img.alpha_composite(body)
    thread = Image.new("L", (w + 2 * p, h + 2 * p), 0)
    ImageDraw.Draw(thread).line(pts + [pts[0], pts[1]], fill=235, width=max(1, int(2 * k)), joint="curve")
    light = Image.new("RGBA", size, (255, 214, 190, 0))
    light.putalpha(thread.resize(size, Image.LANCZOS))
    img.alpha_composite(light)
    return img if side == "p1" else ImageOps.mirror(img)


def solid(M, side, s, height, cut):
    """The card's own shape, white on black, to light it up in red. / La forme de la carte, pour la rougir."""
    w, h = int(M.PW * s), int(height * s)
    c = cut * s
    img = Image.new("RGB", (w, h), (0, 0, 0))
    ImageDraw.Draw(img).polygon([(c, 0), (w - 1, 0), (w - 1, h - 1 - c), (w - 1 - c, h - 1), (0, h - 1), (0, c)], fill=(255, 255, 255))
    return img if side == "p1" else ImageOps.mirror(img)


def crown_img(size):
    ss = 4
    w, h = int(size * 1.7) * ss, size * ss
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(0.08, 0.92), (0.0, 0.2), (0.27, 0.56), (0.5, 0.04), (0.73, 0.56), (1.0, 0.2), (0.92, 0.92)]
    d.polygon([(x * (w - 1), y * (h - 1)) for x, y in pts], fill=(255, 214, 120, 255))
    d.rectangle([0.08 * w, 0.78 * h, 0.92 * w, 0.92 * h], fill=(214, 160, 60, 255))
    for x in (0.0, 0.5, 1.0):
        r = 0.07 * h
        cx, cy = x * (w - 1) * 0.94 + 0.03 * w, (0.2 if x != 0.5 else 0.06) * h + r
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 244, 200, 255))
    return img.resize((w // ss, h // ss), Image.LANCZOS)


def medal_img(size):
    ss = 4
    w, h = size * ss, int(size * 1.45) * ss
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(0.22 * w, 0), (0.78 * w, 0), (0.66 * w, 0.42 * h), (0.34 * w, 0.42 * h)], fill=(190, 62, 50, 255))
    d.polygon([(0.42 * w, 0), (0.58 * w, 0), (0.55 * w, 0.42 * h), (0.45 * w, 0.42 * h)], fill=(236, 226, 200, 255))
    r = 0.46 * w
    cx, cy = w / 2, h - r - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(184, 132, 44, 255))
    d.ellipse([cx - r * 0.84, cy - r * 0.84, cx + r * 0.84, cy + r * 0.84], fill=(255, 214, 120, 255))
    d.ellipse([cx - r * 0.5, cy - r * 0.62, cx + r * 0.1, cy - r * 0.1], fill=(255, 243, 196, 255))
    pts = []
    for i in range(10):
        rr = r * (0.52 if i % 2 == 0 else 0.22)
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=(184, 132, 44, 255))
    return img.resize((w // ss, h // ss), Image.LANCZOS)


class Live:
    """The stage direction of one game: where the cards are, what form they have, the boss's bar, the counts of the
    mission and its show. / La mise en scène d'une partie : où sont les cartes, leur forme, la barre du boss, les comptes
    de la mission et son spectacle."""

    def __init__(self, sc):
        from . import hd_mslug as M
        self.M, self.sc = M, sc
        self.now = 0.0
        self.small = False                       # the cards have their small form / les cartes sont en petit
        self.out = Tw(0.0)                       # 0 at home, 1 off the screen / 0 à leur place, 1 hors de l'écran
        self.top = Tw(0.0)                       # the logo and the timer put away at the top / rangés en haut
        self.bot = Tw(0.0)                       # the credits put away at the bottom / rangés en bas
        self.low = False                         # the timer and the credits small at the bottom (a boss) / en petit, en bas
        self.knocks = {"p1": (0.0, -99.0, 1.0), "p2": (0.0, -99.0, 1.0)}
        self.tally = None
        self.show = None
        self.end_prev = None
        self.bar = None                          # the boss's bar on the screen / la barre du boss à l'écran
        self.bar_a = Tw(0.0)
        self.boss_ref = None
        self.ghost, self.ghost_to, self.ghost_t = 1.0, 1.0, -99.0
        self.down_t = -99.0
        self.spark_t = -99.0
        self.img = {}
        self.buf = None
        self.real = False                        # the boss of the mission is on the screen / le boss de la mission est là
        self.vals = {}

    # ------------------------------------------------------------ what the scene tells / ce que dit la scène
    def count(self, side, key, n=1, mark=False):
        if self.tally is not None and n > 0:
            self.tally.add(side, key, n, self.sc.fx.now, mark)

    def knock(self, side, amp, dur=0.9):
        """The card pushed outwards, back like a spring. / La carte repoussée vers le bord, qui revient en ressort."""
        now = self.sc.fx.now
        if abs(self._knock(side, now)) <= amp * self.sc.s:
            self.knocks[side] = (amp, now, dur)

    def _knock(self, side, now):
        amp, t0, dur = self.knocks[side]
        p = (now - t0) / dur
        return amp * self.sc.s * (1 - elastic(p)) if 0 <= p < 1 else 0.0

    def blast(self, amp=120):
        """A big blast: a wave from the middle of the screen, both cards blown outwards. / Une grosse explosion : une
        onde part du milieu de l'écran, les deux cartes sont soufflées vers les bords."""
        sc = self.sc
        fx, s = sc.fx, sc.s
        for side in ("p1", "p2"):
            self.knock(side, amp, 1.0)
        for delay, r1, width, col, a0 in ((0.0, 520, 20, (255, 170, 80), 0.8), (0.08, 340, 10, (255, 236, 190), 0.6)):
            r = fx.add(Particle("ring", sc.W / 2, sc.H * 0.54, fx.now + delay, 0.7, "front"))
            r.r0, r.r1, r.col, r.a0, r.a1, r.data = 30 * s, r1 * s, col, a0, 0.0, width * s

    def card_dx(self, side):
        d = -1 if side == "p1" else 1
        return int(round(d * (self.out.at(self.now) * self.sc.S(self.M.PW + 60) + self._knock(side, self.now))))

    def gone(self):
        """The cards are off the screen: nothing fires from them. / Les cartes sont hors de l'écran."""
        return self.out.at(self.now) >= 0.9

    def busy(self, now):
        """The show or BOSS DESTROYED has the screen: no other banner over it. / Le spectacle ou BOSS DÉTRUIT tient l'écran."""
        return self.show is not None or now - self.down_t < DOWN_T

    def reset(self):
        self.tally = self.show = self.bar = self.boss_ref = None
        self.small = self.low = self.real = False
        for tw in (self.out, self.top, self.bot, self.bar_a):
            tw.set(0.0)
        self.down_t = -99.0

    # ------------------------------------------------------------ each image / à chaque image
    def update(self, vals, now, anyone, attract):
        sc, M = self.sc, self.M
        self.now, self.vals = now, vals
        if attract:
            self.reset()
            self.end_prev = M._n(vals.get("mission_ending"))
            return
        playing = anyone
        m = sc.mission
        if playing and m is not None:
            if self.tally is None or self.tally.mission != m:
                self.tally = Tally(now, m)
            self.tally.tick(now, [side for side, P in sc.players.items() if sc.playing(P)])
        B = sc.boss
        real = self.real = bool(playing and B is not None and not B.get("minor") and B.get("slot") is not None
                                and B.get("mission") == m)
        if real and self.tally is not None:
            if self.tally.boss[0] is None:
                self.tally.boss[0] = B["t0"]
            if B["down"] is not None and self.tally.boss[1] is None:
                self.tally.boss[1] = B["down"]
        # the mission ends on the game's screen: its show / la mission se termine à l'écran du jeu : son spectacle
        end = M._n(vals.get("mission_ending"))
        if (end == 1 and self.end_prev == 0 and playing and self.show is None and self.tally is not None
                and not self.tally.shown and self.tally.sides):
            self.tally.shown = True
            self.show = Show(self, self.tally, now)
        self.end_prev = end
        if self.show is not None:
            if self.show.cut_t is None and (self.show.tally.mission != m or not playing):
                self.show.cut_t = now                              # the next mission begins: the show gives way
            if self.show.over(now):
                self.show = None
        self._boss(B if real else None, now)
        warn = real and B["down"] is None and now - B["t0"] < WARN_T
        hide = warn or self.show is not None
        if hide or real != self.small:
            self.out.to(1.0, now, 0.38, ease_in)
            if self.out.at(now) >= 0.999:
                self.small = real                                  # the form changes off the screen / la forme change dehors
        else:
            self.out.to(0.0, now, 0.55, ease_back if self.small else ease_out)
        away = warn or real or self.show is not None
        self.top.to(1.0 if away else 0.0, now, 0.3 if away else 0.5, ease_in if away else ease_out)
        if hide or real != self.low:
            self.bot.to(1.0, now, 0.3, ease_in)
            if self.bot.at(now) >= 0.999:
                self.low = real
        else:
            self.bot.to(0.0, now, 0.45, ease_out)

    def _boss(self, B, now):
        """The boss's wide bar: it comes after the WARNING, follows the hits, bursts when the boss falls.
        / La grande barre du boss : elle arrive après le WARNING, suit les coups, éclate à la chute."""
        sc = self.sc
        fx = sc.fx
        if B is None:
            self.boss_ref = None
            self.bar_a.to(0.0, now, 0.3)
            return
        frac = clamp(B["hp"] / max(1, B["top"]))
        if B is not self.boss_ref:                                  # another boss, or its bar back / un autre boss
            self.boss_ref = B
            self.ghost = self.ghost_to = frac
            self.bar = {"t0": None}
        bar = self.bar
        bar.update(name=B["name"] or "BOSS", phase=B.get("phase", 1), hit_t=B["hit_t"])
        if B["down"] is not None:
            if bar.get("down") is None:                             # it falls: the bar bursts / il tombe : la barre éclate
                bar["down"] = now
                self.down_t = now
                self.bar_a.to(0.0, now, 0.4)
                x0, y, w, h = self.bar_box()
                for i in range(10):
                    fx.sparks(x0 + w * (i + 0.5) / 10, y + h / 2, 8, FIRE_HOT, (300, 900), (0, 360), (0.4, 1.1), 1100,
                              "front", 3, 46)
                self.blast()
            bar["frac"] = 0.0
            return
        if now - B["t0"] >= WARN_T - 0.3:
            if bar["t0"] is None:
                bar["t0"] = now
            self.bar_a.to(1.0, now, 0.45, ease_back)
        else:
            self.bar_a.to(0.0, now, 0.2)
        old = bar.get("frac", frac)
        bar["frac"] = frac
        if frac > old:                                              # its next phase: full again / sa phase suivante
            self.ghost = self.ghost_to = frac
        elif frac < old:
            self.ghost_to, self.ghost_t = frac, now + 0.35         # the pale part waits, then follows / attend, puis suit
            if bar["t0"] is not None and now - self.spark_t > 0.07:
                self.spark_t = now
                x0, y, w, h = self.bar_box()
                big = old - frac >= 0.04                            # a grenade, a shell / une grenade, un obus
                fx.sparks(x0 + w * frac, y + h / 2, 14 if big else 5, FIRE_HOT, (300, 700), (0, 360), (0.25, 0.6), 1100,
                          "front", 3, 46)
                if big:
                    fx.shake(4, 0.2)
        if now >= self.ghost_t and self.ghost > self.ghost_to:
            self.ghost = max(self.ghost_to, self.ghost - max(0.004, (self.ghost - self.ghost_to) * min(1.0, sc.fx_dt / 0.16)))

    def bar_box(self):
        S = self.sc.S
        return S(260), S(80), S(1400), S(34)

    # ------------------------------------------------------------ pictures made once / images faites une fois
    def art(self, key, make):
        s = self.img.get(key)
        if s is None:
            s = self.img[key] = self.sc.hd._surf(make())
        return s

    def plate(self, side):
        return self.art(("plate", side), lambda: strip_img(self.M, side, self.sc.s, self.M.ACCENT[side]))

    def frame(self, side, small=None):
        small = self.small if small is None else small
        return self.art(("frame", side, small), lambda: outline(self.M, side, self.sc.s, SH if small else self.M.PH,
                                                                 SCUT if small else 28, 36))

    def icon(self, name, h):
        """One of the program's small drawings, h high (reference screen). / Un petit dessin du programme, haut de h."""
        def make():
            M, sc = self.M, self.sc
            hh = max(4, sc.S(h))
            if name == "helmet":
                return M.helmet_img(hh)
            if name == "grenade":
                return M.grenade_img(max(3, int(hh * 30 / 38)), hh)
            if name == "prisoner":
                return M.prisoner_img(max(3, int(hh * 34 / 40)), hh)
            if name == "coin":
                return M.coin_img(hh, sc.coin_symbol or "", sc.hd.font)
            if name == "crown":
                return crown_img(hh)
            if name == "medal":
                return medal_img(max(4, int(hh / 1.45)))
            return M.small_imgs(hh / (6.0 if name == "case" else 52.0))[name]
        return self.art(("icon", name, h), make)

    def warm(self):
        """What to prepare in the calm images of a game, so that nothing stutters when it is needed.
        / Ce qu'il faut préparer pendant les images calmes, pour que rien n'accroche au moment voulu."""
        out = [(self.plate, (side,)) for side in ("p1", "p2")]
        out += [(self.frame, (side, small)) for side in ("p1", "p2") for small in (False, True)]
        out += [(self.hazard, ()), (self.veil, ()), (self.bar_fill, ())]
        out += [(self.icon, (n, h)) for n, h in (("crown", 44), ("medal", 62), ("helmet", 84), ("helmet", 40), ("helmet", 30),
                                                  ("prisoner", 84), ("prisoner", 40), ("prisoner", 30), ("coin", 84), ("coin", 30),
                                                  ("grenade", 84), ("grenade", 40), ("crate", 84), ("crate", 40), ("crate", 30),
                                                  ("case", 16))]
        hd, S = self.sc.hd, self.sc.S
        for text, size, col, glow in (("WARNING", 124, self.M.RED, 0.8), (tr("BOSS DÉTRUIT", "BOSS DESTROYED"), 96, self.M.GOLD, 0.7),
                                      (tr("BOSS DÉTRUIT", "BOSS DESTROYED"), 96, self.M.GOLD, 0)):
            out.append((hd.text, (text, "stencil", S(size), col, glow)))
        for c in "0123456789":
            out.append((hd.text, (c, "stencil", S(110), self.M.GOLD, 0.6)))
        return out

    def hazard(self):
        def make():
            S = self.sc.S
            h, step = S(58), max(8, S(80))
            w = self.sc.W + 3 * step
            img = Image.new("RGB", (w * 2, h * 2), HAZARD_DARK)
            d = ImageDraw.Draw(img)
            for x in range(-2 * step * 2, w * 2 + step * 2, step * 2):
                d.polygon([(x, h * 2), (x + step, h * 2), (x + step + h * 2, 0), (x + h * 2, 0)], fill=HAZARD)
            d.line([(0, 1), (w * 2, 1)], fill=(60, 46, 12), width=3)
            d.line([(0, h * 2 - 2), (w * 2, h * 2 - 2)], fill=(60, 46, 12), width=3)
            return img.resize((w, h), Image.LANCZOS)
        return self.art("hazard", make)

    def veil(self):
        """The show's backdrop: a dark veil over the scenery, warm on player 1's side, cold on player 2's.
        / Le fond du spectacle : un voile sombre sur le décor, chaud du côté du J1, froid du côté du J2."""
        def make():
            W, H = self.sc.W, self.sc.H
            a1, a2 = self.M.ACCENT["p1"], self.M.ACCENT["p2"]
            row = Image.new("RGBA", (W, 1))
            px = row.load()
            for x in range(W):
                u = x / max(1, W - 1)
                tint, k = (a1, 0.3 * (1 - u * 2) ** 1.4) if u < 0.5 else (a2, 0.3 * (u * 2 - 1) ** 1.4)
                alpha = 1 - (1 - 0.74) * (1 - k)
                px[x, 0] = tuple(int((VEIL[i] * 0.74 * (1 - k) + tint[i] * 0.5 * k) / alpha) for i in range(3)) + (int(255 * alpha),)
            return row.resize((W, H), Image.NEAREST)
        return self.art("veil", make)

    def bar_fill(self):
        def make():
            _, _, w, h = self.bar_box()
            S = self.sc.S
            w, h = max(1, w - S(6)), max(1, h - S(6))
            img = Image.new("RGB", (w, 2 * h))
            for row, right in ((0, (255, 122, 48)), (1, (255, 176, 48))):          # healthy, then nearly down / puis presque à terre
                line = Image.new("RGB", (w, 1))
                px = line.load()
                for x in range(w):
                    u = x / max(1, w - 1)
                    px[x, 0] = tuple(int((255, 58, 42)[i] * (1 - u) + right[i] * u) for i in range(3))
                img.paste(line.resize((w, h), Image.NEAREST), (0, row * h))
                lit = line.point(lambda v: min(255, v + 46)).resize((w, max(1, h // 5)), Image.NEAREST)
                img.paste(lit, (0, row * h))
            return img
        return self.art("bar_fill", make)

    def tmp(self, screen):
        if self.buf is None or self.buf.get_size() != screen.get_size():
            self.buf = self.sc.pg.Surface(screen.get_size()).convert()
        return self.buf

    # ------------------------------------------------------------ the small card / la petite carte
    def anchor(self, side, name, i=0):
        """Where the effects of an event go while the cards are small. / Où vont les effets pendant que les cartes sont
        en petit."""
        sc = self.sc
        S, X = sc.S, sc.X
        x0 = sc.x0(side, sc.players[side])
        if name == "slot":
            return X(side, x0, SLOT[0], SLOT[2]), S(SY + SLOT[1])
        if name == "ammo":
            return X(side, x0, INFO + 214), S(SY + 92)
        if name == "text":
            return X(side, x0, INFO), S(SY + 62)
        if name == "helmet":
            return None, S(SY + 28)
        if name == "gauge":
            return X(side, x0, INFO, 150) + S(75), S(SY + 92)
        if name == "prisoner":
            return X(side, x0, 150), S(SY + 104)
        return X(side, x0, SLOT[0], SLOT[2]) + S(SLOT[2] / 2), S(SY + SLOT[1] + SLOT[3] / 2)     # "bomb": from the picture

    def draw_strip(self, screen, side, vals, now):
        sc, M = self.sc, self.M
        P = sc.players[side]
        hd, S, pg, X = sc.hd, sc.S, sc.pg, sc.X
        x0 = sc.x0(side, P)
        hit = max(0.0, 1 - (now - P.hit_t) / 0.45)
        if hit:
            x0 += int(math.sin(now * 90) * S(7) * hit)
        y0 = S(SY)
        screen.blit(self.plate(side), (x0, y0))
        acc = M.ACCENT[side]
        playing = sc.playing(P)
        at, chip = M.chip_at(pg, sc.chips[side], side, x0, y0, S)
        screen.blit(sc.chips[side], at)
        hd.put(screen, hd.text(tr("J1", "P1") if side == "p1" else tr("J2", "P2"), "stencil", S(36), (24, 14, 8), glow=0),
               chip.centerx, chip.centery, "center", "middle")
        mid = x0 + S(M.PW) / 2
        if not playing and (P.over_t is None or now - P.over_t > 5.0):
            credits = M._n(vals.get("credits"))
            word = tr("APPUIE SUR START", "PRESS START") if credits is None or credits > 0 else "INSERT COIN"
            k = hd._pulse(now)
            hd.put(screen, hd.text(word, "stencil", S(38), tuple(int(c * k) for c in acc)), mid, y0 + S(108), "center", "middle")
            return
        name = sc.soldier(side, vals)
        if name:
            lx = 114
            pic = sc.portrait(name)
            if pic is not None:
                screen.blit(pic, (X(side, x0, lx, 48), chip.centery - pic.get_height() // 2))
                lx += 58
            hd.put(screen, hd.text(name, "stencil", hd.fit_size(name, "stencil", S(34), S(230), S(18)), acc, glow=0.3),
                   X(side, x0, lx), chip.centery, "left" if side == "p1" else "right", "middle")
        lives = sc.lives_shown(side, P, vals, now)
        if lives is not None:
            sc._draw_lives(screen, side, P, x0, int(lives), now)
        score = M._n(sc.get(vals, side, "score"))
        if score is not None:
            if P.score_disp is None or score < P.score_disp:
                P.score_disp = score
            else:
                gap = score - P.score_disp
                P.score_disp = min(score, P.score_disp + max(1, int(gap * 0.18) + 1)) if gap else score
            pop = max(0.0, 1 - (now - P.score_t) / 0.22)
            text = sc._fmt(P.score_disp)
            size = S(57)
            fit = min(1.0, S(250) / max(1, hd.text_width(text, "stencil", size)))
            hd.put_number(screen, text, "stencil", size, M.GOLD, X(side, x0, 25), y0 + S(107), "left" if side == "p1" else "right",
                          "middle", scale=round(fit * 50) / 50.0 * (1 + 0.1 * pop))
        self._strip_weapon(screen, side, P, x0, y0, vals, now)
        if P.mode == 2:
            self._stamp(screen, x0, y0, "CONTINUE ?", M.GOLD, now, P.join_t, pulse=True)
        elif P.over_t is not None and not playing:
            self._stamp(screen, x0, y0, "GAME OVER", M.RED, now, P.over_t)
        self.red(screen, side, x0, y0, hit)
        if sc.last_life(P, lives, now):
            self.beat(screen, side, x0, y0, now)

    def _strip_weapon(self, screen, side, P, x0, y0, vals, now):
        sc, M = self.sc, self.M
        hd, S, pg, X = sc.hd, sc.S, sc.pg, sc.X
        left = "left" if side == "p1" else "right"
        cx = X(side, x0, SLOT[0], SLOT[2]) + S(SLOT[2] / 2)
        cy = y0 + S(SLOT[1] + SLOT[3] / 2)
        gx, gw, gh, gy = X(side, x0, INFO, 150), S(150), S(17), y0 + S(84)
        ax, ay = X(side, x0, INFO + 214), y0 + S(92)
        if P.tank:
            mount = P.ride in M.MOUNTS
            hp = None if mount else M._n(sc.get(vals, side, "vehicle_hp"))
            shells = None if mount else M._n(sc.get(vals, side, "vehicle_ammo"))
            kind = P.ride or "tank"
            img = self.small_pic(("ride", kind, side), lambda: sc.ride_surf(kind, side))
            tt = now - P.tank_t
            jx = math.sin(now * 80) * S(3) * max(0.0, 1 - (now - P.tank_hit_t) / 0.4)
            self._flip(screen, img, cx + jx, cy, tt)
            name = tr(*M.VEHICLE_NAMES.get(kind, M.VEHICLE_NAMES["vehicle"]))
            hd.put(screen, hd.text(name, "stencil", hd.fit_size(name, "stencil", S(20), S(214), S(12)), (176, 232, 140), glow=0.3),
                   X(side, x0, INFO), y0 + S(112), left)
            hits = None if hp is None else max(0, min(M.TANK_HITS, math.ceil(hp * M.TANK_HITS / 100.0 - 0.05)))
            if hits is not None:
                sw = gw / M.TANK_HITS
                blink = int(now * 6) % 2 == 0
                col = {3: (110, 220, 90), 2: (240, 210, 70), 1: (255, 80, 50)}.get(hits, (255, 80, 50))
                for i in range(M.TANK_HITS):
                    j = i if side == "p1" else M.TANK_HITS - 1 - i
                    c = col if i < hits else (40, 42, 56)
                    if i < hits and hits == 1 and blink:
                        c = (150, 40, 30)
                    pg.draw.rect(screen, c, pg.Rect(int(gx + j * sw + 2), gy, int(sw - 4), gh), border_radius=S(3))
            if shells is not None and shells <= 99:
                hd.put_number(screen, str(int(shells)), "stencil", S(30), M.WHITE if shells > 0 else M.RED, ax, ay,
                              "right" if side == "p1" else "left", "middle")
            return
        code = M._n(sc.get(vals, side, "weapon"))
        if code is None:
            return
        name, kind = sc.weapon(side, code)
        kind = kind or "gun"
        ammo = M._n(sc.get(vals, side, "ammo"))
        wt = now - P.weapon_t
        if wt < 0:                                                 # the crate is on its way / la caisse arrive
            return
        img = self.small_pic(("weapon", kind, side), lambda: sc.weapon_surf(kind, side))
        kick = max(0.0, 1 - (now - P.recoil_t) / 0.08) * S(3) * (-1 if side == "p1" else 1)
        self._flip(screen, img, cx + kick, cy, wt)
        col = (255, 226, 170) if kind != "pistol" else M.CREAM
        hd.put(screen, hd.text(name, "stencil", hd.fit_size(name, "stencil", S(20), S(214), S(12)), col, glow=0.3),
               X(side, x0, INFO), y0 + S(112), left)
        if kind == "pistol" or ammo is None:
            hd.put(screen, hd.text("∞", "black", S(34), M.GREY, glow=0), X(side, x0, INFO), ay, left, "middle")
            return
        frac = max(0.0, min(1.0, ammo / max(1, P.ammo_max)))
        P.gauge += (frac - P.gauge) * (0.25 if wt < 0.5 else 0.5)
        if wt < 0.45:
            P.gauge = min(frac, (wt / 0.45) * frac)
        segs = 16
        sw = gw / segs
        lit = P.gauge * segs
        low = frac < 0.25
        flash = max(0.0, 1 - (now - P.recoil_t) / 0.1)
        for i in range(segs):
            j = i if side == "p1" else segs - 1 - i
            r = pg.Rect(int(gx + j * sw + 1), gy, max(1, int(sw - 2)), gh)
            if i < int(lit):
                c = (255, 80, 50) if low and int(now * 6) % 2 == 0 else (255, int(200 - 90 * i / segs), 70)
                if i == int(lit) - 1 and flash:
                    c = (255, 255, 230)
            elif i < lit:
                c = (150, 110, 50)
            else:
                c = (40, 42, 56)
            pg.draw.rect(screen, c, r, border_radius=S(2))
        hd.put_number(screen, str(int(ammo)), "stencil", S(30), M.WHITE if not low else M.RED, ax, ay,
                      "right" if side == "p1" else "left", "middle", scale=1 + 0.1 * flash)

    def small_pic(self, key, get):
        """A picture of the big card, half its size. / Une image de la grande carte, deux fois plus petite."""
        key = ("half",) + key
        s = self.img.get(key)
        if s is None:
            big = get()
            s = self.img[key] = self.sc.pg.transform.smoothscale(big, (max(1, big.get_width() // 2), max(1, big.get_height() // 2)))
        return s

    def _flip(self, screen, img, cx, cy, age):
        """A picture that has just changed turns over into place. / Une image qui vient de changer se retourne."""
        k = self.flip(age)
        if k < 1.0:
            img = self.sc.pg.transform.smoothscale(img, (img.get_width(), max(1, int(img.get_height() * k))))
        screen.blit(img, (int(cx - img.get_width() / 2), int(cy - img.get_height() / 2)))

    @staticmethod
    def flip(age):
        """How tall the picture is, 0.32 s after it changed: flat, past its size, then its size.
        / La hauteur de l'image dans les 0,32 s après son changement : à plat, plus grande, puis sa taille."""
        return 1.0 if age >= 0.32 else max(0.04, ease_back(clamp(age / 0.32)))

    def _stamp(self, screen, x0, y0, text, color, now, t0, pulse=False):
        sc = self.sc
        hd, S, pg = sc.hd, sc.S, sc.pg
        k = min(1.0, (now - t0) / 0.18)
        shade = pg.Surface((S(self.M.PW - 16), S(66)), pg.SRCALPHA)
        shade.fill((0, 0, 0, 170))
        screen.blit(shade, (x0 + S(8), y0 + S(74)))
        a = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(now * 6)) if pulse else 1.0
        t = hd.text(text, "stencil", hd.fit_size(text, "stencil", S(54), S(self.M.PW - 120), S(24)), color, glow=0.6)
        hd.put(screen, t, x0 + S(self.M.PW) / 2, y0 + S(107), "center", "middle", scale=2.0 - 1.0 * k, alpha=a)

    # ------------------------------------------------------------ the card takes a hit, the last life / coup reçu, dernière vie
    def red(self, screen, side, x0, y0, hit):
        """The card lights up red in its own shape (not the whole rectangle: its corners are cut).
        / La carte rougit dans sa forme (pas tout le rectangle : ses coins sont coupés)."""
        if hit <= 0:
            return
        small = self.small
        pg = self.sc.pg
        shape = self.art(("solid", side, small), lambda: solid(self.M, side, self.sc.s, SH if small else self.M.PH,
                                                              SCUT if small else 28))
        work = self.img.get(("work", small))
        if work is None:
            work = self.img[("work", small)] = shape.copy()
        work.blit(shape, (0, 0))
        work.fill((int(100 * hit), 0, 0), special_flags=pg.BLEND_RGB_MULT)
        screen.blit(work, (x0, y0), special_flags=pg.BLEND_RGB_ADD)

    def beat(self, screen, side, x0, y0, now):
        """The last life: the card's frame beats red. / La dernière vie : le cadre de la carte bat en rouge."""
        f = self.frame(side)
        k = 0.5 + 0.5 * math.sin(now * 6.5)
        pad = (f.get_width() - self.sc.S(self.M.PW)) // 2
        f.set_alpha(int(255 * (0.35 + 0.65 * k)))
        screen.blit(f, (x0 - pad, y0 - pad))
        f.set_alpha(255)

    # ------------------------------------------------------------ the middle of the screen / le milieu de l'écran
    def draw_center(self, screen, vals, logo, now):
        """The logo, MISSION n, the timer and the credits, as the scene draws them, but put away when a boss or the
        show takes the screen; with a boss, the timer and the credits come back small between the two small cards.
        / Le logo, MISSION n, le chrono et les crédits, rangés quand un boss ou le spectacle prend l'écran ; avec un
        boss, le chrono et les crédits reviennent en petit entre les deux petites cartes."""
        sc, M = self.sc, self.M
        hd, S, W, pg = sc.hd, sc.S, sc.W, sc.pg
        cx = W / 2
        up = self.top.at(now)
        dy = -int(up * S(330))
        credits = M._n(vals.get("credits"))
        if up < 0.995:
            h = hd.draw_logo(screen, logo, cx, S(14) + dy, S(540), S(116), now)
            y = S(14) + max(h, S(60)) + S(16)
            B = sc.boss
            if B is not None and not self.real and (B.get("minor") or B["down"] is not None or now - B["t0"] >= 2.4):
                sc._draw_boss(screen, B, cx, y + dy, now)
                y += S(70)
            elif B is not None:
                y += S(52)
            elif sc.mission_shown is not None:
                t = hd.text(f"MISSION {int(sc.mission_shown)}", "stencil", S(34), M.CREAM, glow=0.4)
                hd.put(screen, t, cx, y + dy, "center")
                for d in (-1, 1):
                    x = cx + d * (t["w"] / 2 + S(24))
                    for j in range(3):
                        xx = x + d * j * S(12)
                        pg.draw.lines(screen, M.ACCENT["p1" if d < 0 else "p2"], False,
                                      [(xx - d * S(6), y + dy + S(4)), (xx + d * S(2), y + dy + S(17)), (xx - d * S(6), y + dy + S(30))],
                                      max(2, S(4)))
                y += S(52)
            if sc.time_v is not None and not self.real:
                self._time(screen, cx, y + dy, 1.0, now)
        down = int(self.bot.at(now) * S(150))
        if self.bot.at(now) >= 0.995:
            return
        if self.low:                                               # a boss: small, side by side / un boss : en petit
            if sc.time_v is not None:
                self._time(screen, cx - S(133 if credits is not None else 0), S(358) + down, 0.74, now)
            if credits is not None:
                sc._draw_credits(screen, credits, cx + S(75 if sc.time_v is not None else 0), S(392) + down, now, 0.74)
        elif credits is not None:
            sc._draw_credits(screen, credits, cx, S(14 + 418 - 34) + down, now)

    def _time(self, screen, cx, y, k, now):
        sc, M = self.sc, self.M
        hd, S, pg = sc.hd, sc.S, sc.pg
        bw, bh = S(170 * k), S(92 * k)
        low = sc.time_v <= 10
        pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
        if low:
            cx += math.sin(now * 47) * S(3)                        # the last seconds: it shakes / les dernières secondes
        r = pg.Rect(int(cx - bw / 2), int(y), bw, bh)
        pg.draw.rect(screen, (10, 12, 26), r, border_radius=S(16 * k))
        edge = tuple(int(M.CREAM[i] * (1 - pulse) + M.RED[i] * pulse) for i in range(3)) if low else M.CREAM
        pg.draw.rect(screen, edge, r, max(2, S(3 * k)), border_radius=S(16 * k))
        hd.put(screen, hd.text(tr("TEMPS", "TIME"), "bold", S(17 * k), M.GREY, glow=0), cx, y + S(10 * k), "center")
        hd.put_number(screen, str(int(sc.time_v)), "stencil", S(56 * k), M.RED if low else M.GOLD, cx, y + S(56 * k), "center",
                      "middle", scale=1.0 + 0.12 * pulse)

    def draw_bar(self, screen, now):
        """The boss's life across the top of the screen. / La vie du boss sur toute la largeur, en haut."""
        a = self.bar_a.at(now)
        bar = self.bar
        if bar is None or a <= 0.01:
            return
        sc, M = self.sc, self.M
        hd, S, pg = sc.hd, sc.S, sc.pg
        x0, y, w, h = self.bar_box()
        off = -int((1 - min(1.0, a)) * S(130))
        y += off
        al = clamp(a)
        name = bar["name"]
        if bar["phase"] > 1:
            name = f"{name}  ·  PHASE {bar['phase']}"
        hd.put(screen, hd.text(name, "stencil", hd.fit_size(name, "stencil", S(40), S(1100), S(20)), (255, 170, 150), glow=0.5),
               sc.W / 2, y - S(40), "center", "middle", alpha=al)
        hd.put(screen, hd.text("BOSS", "stencil", S(30), M.RED, glow=0.5), x0 - S(22), y + h / 2, "right", "middle", alpha=al)
        pg.draw.rect(screen, (10, 6, 10), pg.Rect(x0 - S(6), y - S(6), w + S(12), h + S(12)), border_radius=S(12))
        pg.draw.rect(screen, (30, 10, 14), pg.Rect(x0, y, w, h), border_radius=S(8))
        frac = bar.get("frac", 1.0)
        grow = ease_out(clamp((now - bar["t0"]) / 0.9)) if bar.get("t0") is not None else 0.0
        full = w - S(6)
        low = frac < 0.3
        pulse = 0.5 + 0.5 * math.sin(now * 10) if low else 0.0
        if self.ghost > frac:
            pg.draw.rect(screen, (255, 236, 170), pg.Rect(x0 + S(3), y + S(3), int(full * self.ghost * grow), h - S(6)),
                         border_radius=S(5))
        fw = int(full * frac * grow)
        if fw > 0:
            fill = self.bar_fill()
            fh = fill.get_height() // 2
            screen.blit(fill, (x0 + S(3), y + S(3)), area=pg.Rect(0, fh if low else 0, fw, fh))
            if now - bar["hit_t"] < 0.11:                              # a hit: its end flashes / un coup : le bout s'éclaire
                cap = min(fw, S(22))
                pg.draw.rect(screen, (255, 251, 230), pg.Rect(x0 + S(3) + fw - cap, y + S(3), cap, h - S(6)), border_radius=S(4))
        for i in range(1, 10):
            pg.draw.rect(screen, (20, 6, 8), pg.Rect(int(x0 + w * i / 10) - 1, y + S(3), max(2, S(2)), h - S(6)))
        pg.draw.rect(screen, (255, int(90 + 80 * pulse), int(80 + 60 * pulse)), pg.Rect(x0, y, w, h), max(2, S(3)), border_radius=S(8))

    def draw_warning(self, screen, B, now):
        """WARNING on the whole screen: a red veil that beats, two hazard bands that run, the boss's name.
        / WARNING sur tout l'écran : un voile rouge qui bat, deux bandes de danger qui défilent, le nom du boss."""
        sc, M = self.sc, self.M
        hd, S, W, H = sc.hd, sc.S, sc.W, sc.H
        k = now - B["t0"]
        a = clamp(k / 0.2) * (1.0 if k < WARN_T - 0.4 else max(0.0, (WARN_T - k) / 0.4))
        beat = 0.5 + 0.5 * math.sin(k * 12)
        red = self.tmp(screen)
        red.fill((255, 20, 10))
        red.set_alpha(int(255 * (0.10 + 0.12 * beat) * a))
        screen.blit(red, (0, 0))
        red.set_alpha(255)
        band = self.hazard()
        bh, step = band.get_height(), max(8, S(80))
        for top, way in ((True, 1), (False, -1)):
            x = -2 * step + int((k * S(260) * way) % step)
            y = -int(bh * (1 - a)) if top else H - bh + int(bh * (1 - a))
            screen.blit(band, (x, y))
        red.fill((30, 0, 0))
        red.set_alpha(int(150 * a))
        screen.blit(red, (0, S(140)), area=sc.pg.Rect(0, 0, W, S(214)))
        red.set_alpha(255)
        grow = 2.0 - 1.0 * min(1.0, k / 0.18)
        hd.put(screen, hd.text("WARNING", "stencil", S(124), M.RED, glow=0.8), W / 2, S(214), "center", "middle",
               scale=grow * (1 + 0.05 * beat), alpha=a * (0.6 + 0.4 * beat))
        if B["name"]:
            hd.put(screen, hd.text(B["name"], "stencil", hd.fit_size(B["name"], "stencil", S(44), S(1200), S(22)), M.CREAM, glow=0.4),
                   W / 2, S(318), "center", "middle", alpha=a)

    def draw_over(self, screen, now):
        """BOSS DESTROYED, big, in the middle. / BOSS DÉTRUIT, en grand, au milieu."""
        k = now - self.down_t
        if not 0 <= k < DOWN_T:
            return
        sc, M = self.sc, self.M
        hd, S = sc.hd, sc.S
        a = 1.0 if k < DOWN_T - 0.4 else max(0.0, (DOWN_T - k) / 0.4)
        p = clamp(k / 0.45)
        bar = self.tmp(screen)
        bar.fill((0, 0, 0))
        bar.set_alpha(int(150 * a * clamp(k / 0.15)))
        screen.blit(bar, (0, S(170)), area=sc.pg.Rect(0, 0, sc.W, S(130)))
        bar.set_alpha(255)
        word = tr("BOSS DÉTRUIT", "BOSS DESTROYED")
        if p < 1:                                                      # it lands without its glow: one picture to stretch
            hd.put(screen, hd.text(word, "stencil", S(96), M.GOLD, glow=0), sc.W / 2, S(234), "center", "middle",
                   scale=1 + 1.0 * (1 - ease_back(p)), alpha=a)
        else:
            hd.put(screen, hd.text(word, "stencil", S(96), M.GOLD, glow=0.7), sc.W / 2, S(234), "center", "middle", alpha=a)


class Show:
    """The end of a mission on the whole screen, in three parts: one figure after the other, the duel of the scores over
    the curve of the mission, then each one's rank and medals. With one player, the same parts for him alone. The
    scores come second: the game adds its end-of-mission bonus a few seconds after its own tally begins, and the duel
    is then played with it.
    / La fin d'une mission sur tout l'écran, en trois temps : chaque chiffre à son tour, le duel des scores sur la
    courbe de la mission, puis le rang et les médailles de chacun. À un joueur, les mêmes temps pour lui seul. Les
    scores passent en second : le jeu ajoute son bonus de fin de mission quelques secondes après le début de son propre
    décompte, et le duel se joue alors avec lui."""

    T_SCORE, T_CARD, T_RANK, FADE = 3.9, 0.8, 3.7, 0.3
    CARDS = (("prisoners", "prisoner", 1, ("PRISONNIERS SAUVÉS", "PRISONERS RESCUED")),
             ("lives_lost", "helmet", -1, ("VIES PERDUES", "LIVES LOST")),
             ("continues", "coin", -1, ("CONTINUES", "CONTINUES")),
             ("shots", "case", 0, ("BALLES TIRÉES", "SHOTS FIRED")),
             ("grenades", "grenade", 0, ("GRENADES LANCÉES", "GRENADES THROWN")),
             ("weapons", "crate", 0, ("ARMES RAMASSÉES", "WEAPONS PICKED UP")))
    EVENT_ICON = {"lives_lost": "helmet", "prisoners": "prisoner", "continues": "coin", "weapons": "crate"}
    RANK_COLOR = {"S": (255, 214, 120), "A": (255, 214, 120), "B": (238, 228, 208), "C": (255, 64, 44), "D": (255, 64, 44)}

    def __init__(self, live, tally, now):
        self.live, self.tally, self.t0 = live, tally, now
        self.sides = [side for side in ("p1", "p2") if side in tally.sides]
        self.cut_t = None
        self.once = set()
        self.t_duel = len(self.CARDS) * self.T_CARD
        self.t_rank = self.t_duel + self.T_SCORE
        self.t_end = self.t_rank + self.T_RANK
        self.start = dict(tally.score)                 # the scores as the game's tally begins / les scores à ce moment
        self.disp = {"p1": 0.0, "p2": 0.0}
        self.series = list(tally.series) + [(now, tally.score["p1"], tally.score["p2"])]
        self.events = [e for e in tally.events if e[1] in self.EVENT_ICON]
        self.span = (tally.t0, max(now, tally.t0 + 1.0))
        self.boss = tuple(tally.boss)
        self.label = live.sc.mission_shown             # the mission's number as the screen says it / son numéro à l'écran
        self.verdict = None

    def over(self, now):
        return now - self.t0 > self.t_end + self.FADE or (self.cut_t is not None and now - self.cut_t > 0.25)

    def first(self, key):
        if key in self.once:
            return False
        self.once.add(key)
        return True

    # ------------------------------------------------------------ drawing / dessin
    def draw(self, screen, now):
        live = self.live
        t = now - self.t0
        A = clamp(t / self.FADE) * (1 - clamp((t - self.t_end) / self.FADE))
        if self.cut_t is not None:
            A *= 1 - clamp((now - self.cut_t) / 0.25)
        if A <= 0.004:
            return
        target = screen
        if A < 0.996:                                              # coming or going: the whole show see-through
            target = live.tmp(screen)                              # / il arrive ou il part : tout le spectacle en transparence
            target.blit(screen, (0, 0))
        target.blit(live.veil(), (0, 0))
        self._heads(target)
        if t < self.t_duel:
            i = min(len(self.CARDS) - 1, int(t / self.T_CARD))
            self._card(target, i, t - i * self.T_CARD)
        elif t < self.t_rank:
            u = t - self.t_duel
            self._duel(target, u, clamp(u / 0.2) * (1 - clamp((u - (self.T_SCORE - 0.2)) / 0.2)))
        else:
            self._ranks(target, t - self.t_rank)
        if target is not screen:
            target.set_alpha(int(255 * A))
            screen.blit(target, (0, 0))
            target.set_alpha(255)

    def dim(self, col, a):
        """A colour sinking into the veil. / Une couleur qui s'enfonce dans le voile."""
        return tuple(int(VEIL[i] + (col[i] - VEIL[i]) * clamp(a)) for i in range(3))

    def _heads(self, d):
        """Who is who, in the top corners. / Qui est qui, dans les coins du haut."""
        sc, M = self.live.sc, self.live.M
        hd, S, W, pg = sc.hd, sc.S, sc.W, sc.pg
        live_vals = self.live.vals
        for side in self.sides:
            x0 = S(18) if side == "p1" else W - S(18 + M.PW)
            at, chip = M.chip_at(pg, sc.chips[side], side, x0, S(6), S)
            d.blit(sc.chips[side], at)
            hd.put(d, hd.text(tr("J1", "P1") if side == "p1" else tr("J2", "P2"), "stencil", S(36), (24, 14, 8), glow=0),
                   chip.centerx, chip.centery, "center", "middle")
            name = sc.soldier(side, live_vals)
            if name:
                hd.put(d, hd.text(name, "stencil", hd.fit_size(name, "stencil", S(34), S(230), S(18)), M.ACCENT[side], glow=0.3),
                       sc.X(side, x0, 114), chip.centery, "left" if side == "p1" else "right", "middle")

    def _title(self, d, text, x, a, size=58):
        sc, M = self.live.sc, self.live.M
        hd, S = sc.hd, sc.S
        hd.put(d, hd.text(text, "stencil", hd.fit_size(text, "stencil", S(size), S(900), S(30)), M.CREAM, glow=0.4), x, S(52), "center",
               "middle", alpha=clamp(a))

    def _num(self, d, text, x, y, align, a, size=110):
        sc, M = self.live.sc, self.live.M
        return put_num(sc.hd, d, text, "stencil", sc.S(size), M.GOLD, x, y, align, 0.6, clamp(a))

    def _pop(self, d, name, h, x, y, p):
        """One of the small drawings, its middle at (x, y), p of its size. / Un petit dessin, son milieu en (x, y)."""
        if p <= 0.02:
            return
        img = self.live.icon(name, h)
        if abs(p - 1.0) > 0.02:
            pg = self.live.sc.pg
            img = pg.transform.smoothscale(img, (max(1, int(img.get_width() * p)), max(1, int(img.get_height() * p))))
        d.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))

    def _duel(self, d, t, a):
        """The scores face to face, pulling on a rope, over the mission drawn as a curve with what happened on it.
        / Les scores face à face, qui tirent sur une corde, au-dessus de la mission en courbe avec ce qui s'y est passé."""
        live = self.live
        sc, M = live.sc, live.M
        hd, S, W, pg, fx = sc.hd, sc.S, sc.W, sc.pg, sc.fx
        cx = W / 2
        k = ease_out(clamp(t / 1.5))
        score = self.tally.score
        for side in self.sides:                                        # the numbers run up, and again when the game's
            goal = score[side] * k                                     # bonus comes / les chiffres montent, et encore
            gap = goal - self.disp[side]                               # quand le bonus du jeu arrive
            self.disp[side] = goal if gap <= 0 else self.disp[side] + max(1.0, gap * min(1.0, sc.fx_dt / 0.1))
            self.disp[side] = min(self.disp[side], score[side])
        col = {side: M.ACCENT[side] for side in ("p1", "p2")}
        self._title(d, tr("SCORE DE LA MISSION", "MISSION SCORE"), cx, a)
        two = len(self.sides) == 2
        if two:
            s1, s2 = self.disp["p1"], self.disp["p2"]
            w1 = self._num(d, sc._fmt(int(s1)), S(56), S(148), "left", a)
            w2 = self._num(d, sc._fmt(int(s2)), W - S(56), S(148), "right", a)
            jx = int(W * (0.5 + ((s1 / (s1 + s2) if s1 + s2 else 0.5) - 0.5)))
            pg.draw.rect(d, self.dim(col["p1"], a), pg.Rect(0, S(212), jx, S(14)))
            pg.draw.rect(d, self.dim(col["p2"], a), pg.Rect(jx, S(212), W - jx, S(14)))
            pg.draw.rect(d, self.dim((255, 222, 190), a * 0.6), pg.Rect(0, S(212), jx, max(1, S(3))))
            pg.draw.rect(d, self.dim((200, 236, 255), a * 0.6), pg.Rect(jx, S(212), W - jx, max(1, S(3))))
            if a > 0.5:
                g = fx.sp.glow(S(46), (255, 255, 255), 9, hot=0.6)             # (made once, kept) / (faite une fois)
                d.blit(g, (jx - g.get_width() // 2, S(219) - g.get_height() // 2), special_flags=pg.BLEND_RGB_ADD)
            if t > 1.6 and score["p1"] != score["p2"]:
                first = score["p1"] > score["p2"]
                x = S(56) + w1 + S(64) if first else W - S(56) - w2 - S(64)
                self._pop(d, "crown", 44, x, S(142), ease_back(clamp((t - 1.6) / 0.25)) * (1 if a > 0.5 else 0))
                if self.first("duel"):
                    fx.shake(8, 0.3)
                    fx.sparks(S(300) if first else W - S(300), S(150), 40, M.GOLD, (200, 600), (0, 360), (0.5, 1.2), 500, "front", 3, 26)
        else:
            side = self.sides[0]
            self._num(d, sc._fmt(int(self.disp[side])), cx, S(148), "center", a)
            pg.draw.rect(d, self.dim(col[side], a), pg.Rect(0, S(212), W, S(14)))
            pg.draw.rect(d, self.dim((255, 240, 220), a * 0.5), pg.Rect(0, S(212), W, max(1, S(3))))
        # the mission as a curve / la mission en courbe
        x0, x1, y0, y1 = S(90), W - S(90), S(250), S(422)
        ta, tb = self.span
        top = max(max(p[1], p[2]) for p in self.series) or 1

        def px(tm):
            return x0 + (x1 - x0) * (tm - ta) / (tb - ta)

        def py(v):
            return y1 - (y1 - y0 - S(34)) * (max(0, v) / top) ** 0.6       # softened: the early small scores show / adoucie

        def at(tm, j):
            pts = self.series
            for i in range(1, len(pts)):
                if pts[i][0] >= tm:
                    p, q = pts[i - 1], pts[i]
                    return p[j] + (q[j] - p[j]) * (tm - p[0]) / max(0.001, q[0] - p[0])
            return pts[-1][j]

        ca = a * clamp((t - 0.3) / 0.3)
        pen = ta + (tb - ta) * clamp((t - 0.5) / 2.4)
        pg.draw.rect(d, self.dim((70, 74, 92), ca), pg.Rect(x0, y1, x1 - x0, max(1, S(2))))
        hd.put(d, hd.text(tr("LA MISSION, MINUTE PAR MINUTE", "THE MISSION, MINUTE BY MINUTE"), "bold", S(20), M.CREAM, glow=0), x0, y0 - S(6),
               alpha=ca)
        for mn in range(1, 60):
            x = px(ta + mn * 60)
            if x >= x1 - S(30):
                break
            pg.draw.rect(d, self.dim((52, 56, 72), ca), pg.Rect(int(x), y0 + S(22), max(1, S(2)), y1 - y0 - S(22)))
            if (tb - ta) / 60 <= 12 or mn % 5 == 0:
                hd.put(d, hd.text(f"{mn} min", "bold", S(16), M.GREY, glow=0), x, y1 + S(8), "center", alpha=ca)
        came, fell = self.boss
        if came is not None and pen > came and ca > 0.5:                 # the time of the boss / le temps du boss
            bx0, bx1 = int(px(came)), int(px(min(pen, fell if fell is not None else tb)))
            if bx1 > bx0:
                zone = pg.Surface((bx1 - bx0, y1 - y0 - S(22))).convert()
                zone.fill((255, 60, 40))
                zone.set_alpha(48)
                d.blit(zone, (bx0, y0 + S(22)))
            pg.draw.rect(d, (255, 90, 70), pg.Rect(bx0, y0 + S(22), max(2, S(2)), y1 - y0 - S(22)))
            hd.put(d, hd.text("BOSS", "bold", S(18), (255, 150, 130), glow=0), bx0 + S(8), y0 + S(26), alpha=ca)
        for j, side in ((1, "p1"), (2, "p2")):
            if side not in self.sides or ca <= 0.02:
                continue
            pts = [(px(p[0]), py(p[j])) for p in self.series if p[0] <= pen]
            head = (px(pen), py(at(pen, j)))
            pts.append(head)
            if len(pts) >= 2:
                pg.draw.lines(d, self.dim(tuple(v // 3 for v in col[side]), ca), False, pts, max(3, S(9)))
                pg.draw.lines(d, self.dim(col[side], ca), False, pts, max(2, S(4)))
            pg.draw.circle(d, self.dim((255, 255, 255), ca), (int(head[0]), int(head[1])), max(3, S(6)))
            bonus = score[side] - self.start[side]                     # scored since the game's tally began: its bonus
            if bonus > 0 and pen >= tb and ca > 0.5:                   # / marqué depuis le début du décompte : son bonus
                text = tr(f"BONUS DE FIN +{sc._fmt(bonus)}", f"END BONUS +{sc._fmt(bonus)}")
                hd.put(d, hd.text(text, "bold", S(20), col[side], glow=0), x1, head[1] - S(16 if j == 1 else -16), "right", "middle")
        if ca > 0.5:
            for tm, what, side in self.events:                         # what happened, on the curve of the one it
                if tm > pen or side not in self.sides:                 # happened to / ce qui s'est passé, sur sa courbe
                    continue
                p = ease_back(clamp((pen - tm) / max(1.0, (tb - ta) * 0.03)))
                self._pop(d, self.EVENT_ICON[what], 30, px(tm), py(at(tm, 1 if side == "p1" else 2)) - S(24), p)

    def _card(self, d, i, u):
        """One figure at a time, as big as the screen allows, with one small drawing for each unit while they are few.
        / Un chiffre à la fois, aussi grand que l'écran le permet, avec un petit dessin par unité tant qu'ils sont peu."""
        live = self.live
        sc, M = live.sc, live.M
        hd, S, W, pg, fx = sc.hd, sc.S, sc.W, sc.pg, sc.fx
        key, icon, better, names = self.CARDS[i]
        cx = W / 2
        p = ease_out(clamp(u / 0.16))
        q = clamp((u - (self.T_CARD - 0.1)) / 0.1)
        off = int(((1 - p) * 340 - q * 340) * sc.s)
        al = p * (1 - q)
        if al <= 0.01:
            return
        k = ease_out(clamp(u / 0.38))
        n = self.tally.n
        vals = [n[side][key] for side in self.sides]
        mx = max(vals + [1])
        self._title(d, tr(*names), cx + off, al)
        few = mx <= 10
        per = 1.0 if mx <= 46 else mx / 46.0
        hgt = 84 if few else (16 if icon == "case" else 40)
        img = live.icon(icon, hgt)
        step = img.get_width() + S(14 if few else 6)
        row_n = max(1, int(S(780) / step))
        if len(self.sides) == 2:
            hd.put(d, hd.text("VS", "stencil", S(48), M.GREY, glow=0.2), cx + off, S(164), "center", "middle", alpha=al * 0.7)
            widths = (self._num(d, sc._fmt(int(round(vals[0] * k))), cx - S(150) + off, S(164), "right", al),
                      self._num(d, sc._fmt(int(round(vals[1] * k))), cx + S(150) + off, S(164), "left", al))
            bl = S(700)
            for v, way, side in ((vals[0], -1, "p1"), (vals[1], 1, "p2")):
                edge = cx + way * S(150) + off
                b = int(bl * v / mx * k)
                track = pg.Rect(edge - bl if way < 0 else edge, S(238), bl, S(18))
                pg.draw.rect(d, self.dim((34, 38, 54), al), track)
                if b > 0:
                    r = pg.Rect(edge - b if way < 0 else edge, S(238), b, S(18))
                    pg.draw.rect(d, self.dim(M.ACCENT[side], al), r)
                    pg.draw.rect(d, self.dim(tuple(min(255, c + 70) for c in M.ACCENT[side]), al), pg.Rect(r.x, r.y, r.w, max(1, S(5))))
                count = int(round(v / per))
                for j in range(count):
                    pj = ease_back(clamp((u - 0.08 - j * (0.36 / max(count, 1))) / 0.14))
                    x = edge + way * (step / 2 + (j % row_n) * step)
                    y = S(326 if few else 292) + (j // row_n) * (img.get_height() + S(8)) + img.get_height() / 2
                    self._pop(d, icon, hgt, x, y, pj)
            if better and vals[0] != vals[1] and u > 0.42:
                first = (vals[0] - vals[1]) * better > 0
                x = cx - S(150) + off - widths[0] - S(60) if first else cx + S(150) + off + widths[1] + S(60)
                self._pop(d, "crown", 44, x, S(158), ease_back(clamp((u - 0.42) / 0.2)))
        else:
            v = vals[0]
            self._num(d, sc._fmt(int(round(v * k))), cx + off, S(164), "center", al)
            count = int(round(v / per))
            per_row = min(row_n * 2, max(1, count))
            for j in range(count):
                pj = ease_back(clamp((u - 0.08 - j * (0.36 / max(count, 1))) / 0.14))
                in_row = min(per_row, count - (j // per_row) * per_row)
                x = cx + off + ((j % per_row) - (in_row - 1) / 2) * step
                y = S(300 if few else 270) + (j // per_row) * (img.get_height() + S(8)) + img.get_height() / 2
                self._pop(d, icon, hgt, x, y, pj)
        if u > 0.38 and self.first(("card", i)):
            fx.shake(4, 0.18)

    def _ranks(self, d, u):
        """Each one's rank, falling in after the letters have run, then the medals one by one, and the times.
        / Le rang de chacun, qui tombe après le défilement des lettres, puis les médailles une à une, et les temps."""
        live = self.live
        sc, M = live.sc, live.M
        hd, S, W, fx = sc.hd, sc.S, sc.W, sc.fx
        cx = W / 2
        tally = self.tally
        if self.verdict is None:
            self.verdict = ({side: rank(tally.n[side], tally.score[side]) for side in self.sides}, medals(tally, self.sides))
        ranks, meds = self.verdict
        two = len(self.sides) == 2
        self._title(d, f"MISSION {int(self.label)}" if self.label is not None else "MISSION", cx, u / 0.25, 64)
        for n, side in enumerate(self.sides):
            way = (-1 if side == "p1" else 1) if two else -1
            t0 = 0.1 + 0.3 * n
            lx = (S(250) if way < 0 else W - S(250)) if two else (cx - S(330) if meds[side] else cx)
            if u < t0:
                continue
            hd.put(d, hd.text(tr("RANG", "RANK"), "stencil", S(36), M.CREAM, glow=0.3), lx, S(112), "center", "middle",
                   alpha=clamp((u - t0) / 0.2))
            roll = u - t0
            if roll < 0.45:                                            # the letters run / les lettres défilent
                letter = "SABCD"[int(roll / 0.06) % 5]
                hd.put(d, hd.text(letter, "stencil", S(190), M.GREY, glow=0), lx, S(262), "center", "middle", scale=0.6, alpha=0.5)
            else:
                p = clamp((roll - 0.45) / 0.32)
                letter = ranks[side]
                hd.put(d, hd.text(letter, "stencil", S(190), self.RANK_COLOR[letter], glow=0.7), lx, S(262), "center", "middle",
                       scale=1 + 2.0 * (1 - ease_out(p)), alpha=min(1.0, p * 2.5))
                if p >= 1 and self.first(("rank", side)):
                    fx.shake(12, 0.4)
                    fx.flash(M.ACCENT[side], 0.22, 0.3)
                    fx.sparks(lx, S(262), 40, M.GOLD, (200, 600), (0, 360), (0.5, 1.1), 500, "front", 3, 26)
            for j, name in enumerate(meds[side]):
                pm = ease_back(clamp((u - 1.15 - j * 0.3 - 0.15 * n) / 0.24))
                if pm <= 0.02:
                    continue
                y = S(140 + j * 62)
                mx = lx - way * S(210)
                self._pop(d, "medal", 62, mx, y, pm)
                text = tr(*MEDALS[name])
                hd.put(d, hd.text(text, "stencil", hd.fit_size(text, "stencil", S(40), S(430), S(22)), M.GOLD, glow=0.4),
                       mx - way * S(38), y + S(4), "left" if way < 0 else "right", "middle", alpha=clamp(pm))
        a = clamp((u - 1.8) / 0.4)
        if a > 0:
            came, fell = self.boss
            parts = [(tr("TEMPS DE LA MISSION", "MISSION TIME"), minutes(self.span[1] - self.span[0]))]
            if came is not None and fell is not None and fell > came:
                parts.append((tr("BOSS ABATTU EN", "BOSS DOWN IN"), minutes(fell - came)))
            for n, (label, value) in enumerate(parts):
                x = cx + (S(250) * (2 * n - 1) if len(parts) == 2 else 0)
                lt = hd.text(label, "bold", S(22), M.CREAM, glow=0)
                vt = hd.text(value, "stencil", S(44), M.GOLD, glow=0.5)
                total = lt["w"] + S(16) + vt["w"]
                hd.put(d, lt, x - total / 2, S(418), "left", "middle", alpha=a)
                hd.put(d, vt, x - total / 2 + lt["w"] + S(16), S(418), "left", "middle", alpha=a)
        for at in (1.3, 1.7, 2.1, 2.5):                                # the scene's own fireworks / ses feux d'artifice
            if u > at and self.first(("fw", at)):
                sc._firework()
