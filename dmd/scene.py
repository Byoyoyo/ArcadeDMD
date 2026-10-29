"""Scenes: interprets the games/*.json files and draws each frame of the 128x32 panel.
The scene texts are written in English; in French their words are translated when drawn (PANEL_WORDS).

Scènes : interprète les fichiers games/*.json et dessine chaque image."""

import math
import os
import random
import re
import string
import time

from .canvas import Font, Sprite, parse_color, scale_color, load_sprite_frames
from .i18n import lang, tr


# --------------------------------------------------------------------------
# état du jeu
# --------------------------------------------------------------------------

class GameState:
    def __init__(self):
        self.values = {}
        self.prev = {}
        self.changed_at = {}
        self.meta = {}
        self.events = []          # (nom, ancienne valeur, nouvelle valeur, t) pour les effets
        self.paused = False

    def reset(self, meta=None):
        self.values.clear()
        self.prev.clear()
        self.changed_at.clear()
        self.events.clear()
        self.meta = dict(meta or {})
        self.paused = False

    def update(self, name, value, now, quiet=False):
        old = self.values.get(name)
        if old == value:
            return
        self.prev[name] = old
        self.values[name] = value
        if not quiet:
            self.changed_at[name] = now
            if old is not None:
                self.events.append((name, old, value, now))

    def mapping(self):
        m = {}
        for k, v in self.meta.items():
            if isinstance(v, (str, int, float)):
                m[k] = v
        m.update(self.values)
        return m


# --------------------------------------------------------------------------
# gabarits "{score}" et conditions "when"
# --------------------------------------------------------------------------

class _Missing:
    def __init__(self, text):
        self.text = text

    def __format__(self, spec):
        return self.text


class _Formatter(string.Formatter):
    def __init__(self, missing):
        super().__init__()
        self.missing = missing

    def get_value(self, key, args, kwargs):
        if isinstance(key, int):
            return _Missing(self.missing)
        v = kwargs.get(key)
        if v is None:
            return _Missing(self.missing)
        return v


def render_template(template, mapping, missing="-"):
    if "{" not in template:
        return template
    try:
        return _Formatter(missing).vformat(template, (), mapping)
    except (ValueError, KeyError, IndexError, TypeError):
        return template


# --------------------------------------------------------------------------
# panel words in English or French / mots de la dalle en anglais ou en français
# --------------------------------------------------------------------------

# The scene texts of games/*.json are written in English. In French, these whole words or phrases are replaced
# when drawn, never inside the {fields}. Texts written in French (older or personal files) are translated the
# other way for English. The panel is only 128 x 32: each French word is at most one letter longer or shorter.
# Les textes des scènes sont écrits en anglais ; en français, ces mots entiers sont remplacés au moment du dessin.
PANEL_WORDS = (                  # (French, English)
    ("ARME PISTOLET", "HANDGUN"),
    ("FUSIL À POMPE", "SHOTGUN"),
    ("LANCE-ROQUETTES", "ROCKET LAUNCHER"),
    ("LANCE-FLAMMES", "FLAMETHROWER"),
    ("MITRAILLETTE", "MACHINE GUN"),
    ("TÊTE CHERCHEUSE", "ENEMY CHASER"),
    ("NUAGE ORAGEUX", "THUNDER CLOUD"),
    ("MUNITIONS", "AMMO"),
    ("PRISONNIERS", "PRISONERS"),
    ("PISTOLET", "HANDGUN"),
    ("CRÉDITS", "CREDITS"),
    ("CRÉDIT", "CREDIT"),
    ("ANNEAUX", "RINGS"),
    ("BOMBES", "BOMBS"),
    ("BOMBE", "BOMB"),
    ("CANON", "CANNON"),
    ("TEMPS", "TIME"),
    ("VIES", "LIVES"),
    ("ARME", "ARMS"),
    ("SUIVANTE", "NEXT"),
    ("COUP", "STROKE"),
    ("VENT", "WIND"),
    ("BUT !", "GOAL!"),
    ("SCORE ?", "SCORE?"),
    ("J1", "P1"),
    ("J2", "P2"),
)
PANEL_EN = {fr: en for fr, en in PANEL_WORDS}
# English to French: HANDGUN stays "ARME PISTOLET", and P1/P2 stay P1/P2 (the French panel says P1 too)
PANEL_FR = {en: fr for fr, en in PANEL_WORDS if fr not in ("PISTOLET", "J1", "J2")}


def _words_re(table):
    return re.compile("(?<!\\w)(?:" + "|".join(re.escape(k) for k in sorted(table, key=len, reverse=True))
                      + ")(?!\\w)", re.IGNORECASE)        # longest phrases first


_PANEL_RE = {"en": (_words_re(PANEL_EN), PANEL_EN), "fr": (_words_re(PANEL_FR), PANEL_FR)}
_FIELD_RE = re.compile(r"(\{[^{}]*\})")
_panel_cache = {}


def _panel_word(table):
    def sub(m):
        src = m.group(0)
        dst = table.get(src.upper())
        if dst is None:
            return src
        if src.isupper():
            return dst
        return dst.lower() if src.islower() else dst.capitalize()
    return sub


def panel_text(text, language=None):
    """Text of a panel element in the chosen language: the words of PANEL_WORDS are replaced outside the
    {score}... fields. Cached for each text. / Texte d'un élément de la dalle dans la langue choisie."""
    if not text or not isinstance(text, str):
        return text
    language = language or lang()
    key = (language, text)
    out = _panel_cache.get(key)
    if out is None:
        rx, table = _PANEL_RE.get(language, _PANEL_RE["en"])
        parts = _FIELD_RE.split(text)
        parts[::2] = [rx.sub(_panel_word(table), p) for p in parts[::2]]
        out = _panel_cache[key] = "".join(parts)
    return out


def check_when(cond, state, now=None):
    if not cond:
        return True
    if isinstance(cond, list):
        return all(check_when(c, state, now) for c in cond)
    if "all" in cond:
        return all(check_when(c, state, now) for c in cond["all"])
    if "any" in cond:
        return any(check_when(c, state, now) for c in cond["any"])
    if "not" in cond:
        return not check_when(cond["not"], state, now)
    if "has" in cond:
        names = cond["has"] if isinstance(cond["has"], list) else [cond["has"]]
        # une valeur lue dans le jeu, ou une info du jeu non vide (titre, nom du joueur...)
        return all(state.values.get(n) is not None or bool(state.meta.get(n)) for n in names)
    if "changed_within" in cond:
        c = cond["changed_within"]
        t = state.changed_at.get(c.get("var"))
        return t is not None and now is not None and (now - t) * 1000.0 <= c.get("ms", 1000)
    if "var" in cond:
        v = state.values.get(cond["var"])
        if v is None:
            return False
        if "eq" in cond:
            return v == cond["eq"]
        if "ne" in cond:
            return v != cond["ne"]
        if "in" in cond:
            return v in cond["in"]
        if "gt" in cond:
            return v > cond["gt"]
        if "ge" in cond:
            return v >= cond["ge"]
        if "lt" in cond:
            return v < cond["lt"]
        if "le" in cond:
            return v <= cond["le"]
        return True
    return True


# --------------------------------------------------------------------------
# éléments
# --------------------------------------------------------------------------

class Ctx:
    def __init__(self, canvas, root, log=print):
        self.canvas = canvas
        self.root = root
        self.log = log
        self.t = 0.0
        self.dt = 0.0
        self.state = None
        self.cfg = {}                 # config.json (coin symbol of the attract screen...)


class Element:
    def __init__(self, spec, root, log):
        self.spec = spec
        self.when = spec.get("when")
        self.t0 = None
        self.root = root
        self.log = log

    def local_time(self, ctx):
        if self.t0 is None:
            self.t0 = ctx.t
        return ctx.t - self.t0

    def visible(self, ctx):
        if not check_when(self.when, ctx.state, ctx.t):
            return False
        period = self.spec.get("blink_period")         # clignote : allumé blink_on (part de la période)
        if period:
            try:
                period = float(period)
                on = float(self.spec.get("blink_on", 0.5))
            except (TypeError, ValueError):
                return True
            if period > 0:
                return (ctx.t % period) < period * on
        return True

    def restart(self):
        self.t0 = None

    def render(self, ctx):
        raise NotImplementedError


def _accent_colors(text, accents, base):
    """Couleurs par caractère : initiales des mots colorées dans l'ordre."""
    if not accents:
        return None
    cols = [None] * len(text)
    word = 0
    prev_space = True
    for i, ch in enumerate(text):
        if ch != " " and prev_space:
            if word < len(accents):
                cols[i] = accents[word]
            word += 1
        prev_space = ch == " "
    return cols


def _flash_color(spec, ctx, base):
    fl = spec.get("flash")
    if not fl:
        return base
    names = fl.get("on")
    names = names if isinstance(names, list) else [names]
    ms = fl.get("ms", 150)
    for n in names:
        t = ctx.state.changed_at.get(n)
        if t is not None and (ctx.t - t) * 1000.0 <= ms:
            return parse_color(fl.get("color"), (255, 255, 255))
    return base


class TextEl(Element):
    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.font = Font.get(spec.get("font", "6x10"))
        self.x = spec.get("x", 0)
        self.y = spec.get("y", 0)
        self.align = spec.get("align", "left")
        self.spacing = spec.get("spacing", 0)
        self.upper = spec.get("upper", False)
        self.missing = spec.get("missing", "-")
        self.fit = bool(spec.get("fit", False))          # texte trop long : police plus étroite
        self.max_w = int(spec.get("max_w", 128))
        base = parse_color(spec.get("color"), (255, 255, 255))
        if "segments" in spec:
            self.segments = [(s.get("text", ""), parse_color(s.get("color"), base)) for s in spec["segments"]]
        else:
            self.segments = [(spec.get("text", ""), base)]
        self.base = base

    def render(self, ctx):
        mapping = ctx.state.mapping()
        parts = []
        for tpl, col in self.segments:
            s = render_template(panel_text(tpl), mapping, self.missing)
            if self.upper:
                s = s.upper()
            parts.append((s, col))
        full = "".join(p for p, _ in parts)
        if not full:
            return
        colors = []
        for s, col in parts:
            colors.extend([col] * len(s))
        flash = _flash_color(self.spec, ctx, None)
        if flash is not None:
            colors = [flash] * len(full)
        font = self.font
        w = font.width(full, self.spacing)
        if self.fit and w > self.max_w:
            for name in ("5x8", "4x6"):
                font = Font.get(name)
                w = font.width(full, self.spacing)
                if w <= self.max_w:
                    break
        x = self.x
        if self.align == "center":
            x = self.x - w // 2
        elif self.align == "right":
            x = self.x - w + 1
        ctx.canvas.text(font, full, x, self.y, self.base, self.spacing, colors)


class MarqueeEl(Element):
    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.font = Font.get(spec.get("font", "6x10"))
        self.text = spec.get("text", "")
        self.y = spec.get("y", 0)
        self.x = spec.get("x", 0)
        self.w = spec.get("w", 128)
        self.speed = float(spec.get("speed", 25))
        self.gap = int(spec.get("gap", 32))
        self.spacing = spec.get("spacing", 0)
        self.color = parse_color(spec.get("color"), (230, 230, 230))
        self.accents = [parse_color(c) for c in spec.get("accent_initials", [])]
        self.upper = spec.get("upper", False)
        self.static_if_fits = spec.get("static_if_fits", False)
        # "segments" : morceaux de couleurs différentes, par exemple SNK en bleu puis le titre en blanc
        self.segments = [(g.get("text", ""), parse_color(g.get("color"), self.color))
                         for g in spec.get("segments", []) if isinstance(g, dict)]

    def render(self, ctx):
        mapping = ctx.state.mapping()
        seg_colors = None
        if self.segments:
            parts = [(render_template(panel_text(t), mapping, ""), c) for t, c in self.segments]
            s = "".join(p for p, _ in parts)
            seg_colors = [c for p, c in parts for _ in p]
        else:
            s = render_template(panel_text(self.text), mapping, "")
        if self.upper:
            s = s.upper()
        if not s:
            return
        cv = ctx.canvas
        fl = _flash_color(self.spec, ctx, None)
        colors = [fl] * len(s) if fl else (seg_colors or _accent_colors(s, self.accents, self.color))
        tw = self.font.width(s, self.spacing)
        cv.set_clip(self.x, 0, self.x + self.w, cv.h)
        try:
            if self.static_if_fits and tw <= self.w:
                cv.text(self.font, s, self.x + (self.w - tw) // 2, self.y, self.color, self.spacing, colors)
                return
            period = tw + self.gap
            offset = self.local_time(ctx) * self.speed
            if offset < self.w:
                first = self.x + self.w - offset
            else:
                first = self.x - ((offset - self.w) % period)
            xx = first
            while xx < self.x + self.w:
                cv.text(self.font, s, int(round(xx)), self.y, self.color, self.spacing, colors)
                xx += period
        finally:
            cv.reset_clip()


class CycleEl(Element):
    def __init__(self, spec, root, log, factory):
        super().__init__(spec, root, log)
        self.period = float(spec.get("period", 4.0))
        self.pages = []
        for page in spec.get("pages", []):
            if isinstance(page, dict):
                cond = page.get("when")
                layers = page.get("layers", [])
            else:
                cond, layers = None, page
            self.pages.append((cond, [factory(e) for e in layers]))

    def restart(self):
        super().restart()
        for _, els in self.pages:
            for e in els:
                e.restart()

    def render(self, ctx):
        avail = [els for cond, els in self.pages if check_when(cond, ctx.state, ctx.t)]
        if not avail:
            return
        lt = self.local_time(ctx)
        els = avail[int(lt / self.period) % len(avail)]
        for e in els:
            if e.visible(ctx):
                e.render(ctx)


class BarsEl(Element):
    """Bande d'herbe / égaliseur animé en bas de l'écran."""

    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.x = spec.get("x", 0)
        self.w = spec.get("w", 40)
        self.bottom = spec.get("bottom", 31)
        self.min = spec.get("min", 1)
        self.max = spec.get("max", 5)
        self.color = parse_color(spec.get("color"), (24, 160, 56))
        self.tip = parse_color(spec.get("tip"), (120, 255, 120))
        self.speed = float(spec.get("speed", 1.0))
        rnd = random.Random(spec.get("seed", 1))
        self.base = [rnd.random() for _ in range(self.w)]
        self.phase = [rnd.random() * 6.283 for _ in range(self.w)]
        # lissage du profil
        sm = []
        for i in range(self.w):
            a = self.base[max(0, i - 1)]
            b = self.base[i]
            c = self.base[min(self.w - 1, i + 1)]
            sm.append((a + 2 * b + c) / 4.0)
        self.base = sm
        self.flowers = []
        for c in spec.get("flowers", []):
            self.flowers.append((rnd.randrange(self.w), parse_color(c)))

    def render(self, ctx):
        cv = ctx.canvas
        t = self.local_time(ctx) * self.speed
        span = self.max - self.min
        for i in range(self.w):
            wig = 0.25 * math.sin(t * 2.0 + self.phase[i])
            h = int(round(self.min + span * max(0.0, min(1.0, self.base[i] + wig * 0.4))))
            x = self.x + i
            for k in range(h):
                y = self.bottom - k
                cv.set(x, y, self.tip if k == h - 1 else scale_color(self.color, 0.55 + 0.45 * (k / max(1, h))))
        for (i, col) in self.flowers:
            h = int(round(self.min + span * self.base[i]))
            cv.set(self.x + i, self.bottom - h, col)


class WavesEl(Element):
    """Collines sombres qui défilent en fond."""

    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.layers = []
        for i, lay in enumerate(spec.get("layers", [spec])):
            self.layers.append({
                "y": lay.get("y", 20),
                "amp": lay.get("amp", 3.0),
                "freq": lay.get("freq", 0.09),
                "speed": lay.get("speed", 0.6),
                "color": parse_color(lay.get("color"), (0, 24, 48)),
                "edge": parse_color(lay.get("edge"), None) if lay.get("edge") else None,
                "phase": i * 1.7,
            })

    def render(self, ctx):
        cv = ctx.canvas
        t = self.local_time(ctx)
        for L in self.layers:
            for x in range(cv.w):
                xx = x * L["freq"] + t * L["speed"] + L["phase"]
                top = int(round(L["y"] - L["amp"] * (0.6 * math.sin(xx) + 0.4 * math.sin(xx * 2.3 + 1.1))))
                for y in range(max(0, top), cv.h):
                    cv.set(x, y, L["color"])
                if L["edge"] is not None and 0 <= top < cv.h:
                    cv.set(x, top, L["edge"])


class MountainsEl(Element):
    """Montagnes pleines avec une ligne de sol, comme dans la vidéo Metal Slug 3 de Vera AI.

    peaks : [[x, hauteur], ...] (pentes à 45°), floor : hauteur minimale de la bande,
    bottom : rangée du sol, color : remplissage, edge : crête (facultatif), ground : sol,
    speed : défilement en pixels par seconde (0 = fixe), period : largeur du motif."""

    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.bottom = int(spec.get("bottom", 31))
        self.floor = int(spec.get("floor", 4))
        self.period = max(1, int(spec.get("period", 128)))
        self.speed = float(spec.get("speed", 0))
        self.color = parse_color(spec.get("color"), (14, 122, 54))
        self.edge = parse_color(spec.get("edge"), None) if spec.get("edge") else None
        self.ground = parse_color(spec.get("ground"), None) if spec.get("ground") else None
        peaks = spec.get("peaks") or [[12, 7], [38, 5], [62, 11], [90, 6], [114, 9]]
        self.heights = []
        for x in range(self.period):
            h = self.floor
            for px, ph in peaks:
                d = abs(x - px) % self.period
                d = min(d, self.period - d)
                h = max(h, int(ph) - d)
            self.heights.append(h)

    def render(self, ctx):
        cv = ctx.canvas
        off = int(self.local_time(ctx) * self.speed) if self.speed else 0
        for x in range(cv.w):
            h = self.heights[(x + off) % self.period]
            top = self.bottom - h
            for y in range(max(0, top), self.bottom):
                cv.set(x, y, self.edge if (self.edge is not None and y == top) else self.color)
            cv.set(x, self.bottom, self.ground if self.ground is not None else self.color)


class GaugeEl(Element):
    """Barre de vie (jeux de combat) : var / max, accrochée d'un côté comme dans le jeu.

    anchor "right" : la barre reste collée à droite et se vide par la gauche (joueur 1),
    anchor "left" : l'inverse (joueur 2). low_at : sous ce rapport, couleur low."""

    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.var = spec.get("var", "health")
        self.max = float(spec.get("max", 100))
        self.x, self.y = int(spec.get("x", 0)), int(spec.get("y", 0))
        self.w, self.h = max(1, int(spec.get("w", 50))), max(1, int(spec.get("h", 5)))
        self.anchor = spec.get("anchor", "left")
        self.color = parse_color(spec.get("color"), (255, 208, 48))
        self.low = parse_color(spec.get("low"), (255, 64, 32))
        self.low_at = float(spec.get("low_at", 0.3))
        self.back = parse_color(spec.get("back"), (64, 8, 8))
        self.border = parse_color(spec.get("border"), None) if spec.get("border") else None
        # bevel : liseré clair en bas et à droite de la barre (style de Vera)
        self.bevel = parse_color(spec.get("bevel"), None) if spec.get("bevel") else None
        self.shade = spec.get("shade", True)              # première ligne un peu plus claire

    def render(self, ctx):
        v = ctx.state.values.get(self.var)
        if not isinstance(v, (int, float)):
            return
        r = max(0.0, min(1.0, v / self.max)) if self.max > 0 else 0.0
        n = int(round(r * self.w))
        col = self.low if r <= self.low_at else self.color
        fl = _flash_color(self.spec, ctx, None)
        if fl is not None:
            col = fl
        top = scale_color(col, 1.25) if self.shade else col
        cv = ctx.canvas
        x0, y0 = self.x, self.y
        w = self.w
        if self.bevel is not None:
            w = max(1, self.w - 1)                    # dernière colonne et ligne du dessous : le liseré
            n = int(round(r * w))
            for xx in range(x0, x0 + self.w):
                cv.set(xx, y0 + self.h, self.bevel)
            for yy in range(y0, y0 + self.h):
                cv.set(x0 + self.w - 1, yy, self.bevel)
        if self.border is not None:
            for xx in range(x0 - 1, x0 + self.w + 1):
                cv.set(xx, y0 - 1, self.border)
                cv.set(xx, y0 + self.h, self.border)
            for yy in range(y0, y0 + self.h):
                cv.set(x0 - 1, yy, self.border)
                cv.set(x0 + self.w, yy, self.border)
        for i in range(w):
            filled = (i >= w - n) if self.anchor == "right" else (i < n)
            for k, yy in enumerate(range(y0, y0 + self.h)):
                cv.set(x0 + i, yy, (top if k == 0 else col) if filled else self.back)


class ParticlesEl(Element):
    """Missiles qui traversent + gerbes d'étincelles quand une valeur augmente.
    "burst": {"on": valeurs, "color", "count", "x": [x0, x1]} : une gerbe à un endroit pris entre x0 et x1 (et dans "y")
    chaque fois qu'une des valeurs monte, par exemple un ennemi qui explose quand le score monte."""

    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.rate = float(spec.get("rate", 1.0))
        self.color = parse_color(spec.get("color"), (255, 120, 0))
        self.trail = int(spec.get("trail", 3))
        sp = spec.get("speed", [50, 90])
        self.vmin, self.vmax = float(sp[0]), float(sp[1])
        yr = spec.get("y", [10, 20])
        self.ymin, self.ymax = int(yr[0]), int(yr[1])
        self.dir = spec.get("dir", "right")
        self.burst = spec.get("burst")
        self.items = []
        self.sparks = []
        self.rng = random.Random(7)
        self.last_t = None
        self.burst_times = []

    def _burst_ok(self, t):
        """Not too many bursts: at most one every "gap" seconds, none while the value climbs very fast (a bonus that the
        game counts). / Pas trop de gerbes : rien pendant un décompte rapide de points (un bonus compté par le jeu)."""
        self.burst_times = [x for x in self.burst_times if t - x < 0.8] + [t]
        if len(self.burst_times) > 6:
            return False
        return len(self.burst_times) < 2 or t - self.burst_times[-2] >= float(self.burst.get("gap", 0.0))

    def render(self, ctx):
        cv = ctx.canvas
        t = ctx.t
        dt = 0.0 if self.last_t is None else max(0.0, min(0.1, t - self.last_t))
        self.last_t = t
        # apparition (processus de Poisson)
        if self.rate > 0 and self.rng.random() < self.rate * dt:
            d = self.dir
            if d == "both":
                d = self.rng.choice(["left", "right"])
            v = self.rng.uniform(self.vmin, self.vmax)
            x = -2.0 if d == "right" else cv.w + 1.0
            self.items.append([x, self.rng.randint(self.ymin, self.ymax), v if d == "right" else -v])
        # gerbes sur événement
        if self.burst:
            names = self.burst.get("on")
            names = names if isinstance(names, list) else [names]
            for (name, old, new, et) in ctx.state.events:
                if name in names and isinstance(old, (int, float)) and isinstance(new, (int, float)) and new > old:
                    if not self._burst_ok(t):
                        continue
                    xr = self.burst.get("x") or [20, cv.w - 20]
                    cx = self.rng.randint(int(xr[0]), max(int(xr[0]), int(xr[1])))
                    cy = self.rng.randint(self.ymin, self.ymax)
                    col = parse_color(self.burst.get("color"), (255, 200, 60))
                    for _ in range(int(self.burst.get("count", 8))):
                        a = self.rng.uniform(0, 6.283)
                        s = self.rng.uniform(15, 45)
                        self.sparks.append([cx, cy, math.cos(a) * s, math.sin(a) * s * 0.6, 0.0, col])
        # missiles
        alive = []
        for it in self.items:
            it[0] += it[2] * dt
            x, y, v = it
            if -self.trail - 2 <= x <= cv.w + self.trail + 2:
                alive.append(it)
                cv.add(int(x), y, self.color)
                step = -1 if v > 0 else 1
                for k in range(1, self.trail + 1):
                    cv.add(int(x) + step * k, y, self.color, 0.5 / k)
        self.items = alive
        # étincelles
        sparks = []
        for s in self.sparks:
            s[4] += dt
            if s[4] < 0.6:
                s[0] += s[2] * dt
                s[1] += s[3] * dt
                k = 1.0 - s[4] / 0.6
                cv.add(int(s[0]), int(s[1]), s[5], k)
                sparks.append(s)
        self.sparks = sparks


class AnimEl(Element):
    """Une animation jouée une fois quand une valeur du jeu change : une explosion quand le score monte, une onde de choc
    quand une bombe part. / An animation played once when a value of the game changes.

    "image" : un fichier ou une liste (le premier qui existe est pris, "{game}" devient le nom du jeu). Un GIF animé garde
      ses propres durées, une bande PNG se découpe en "frames" images de "ms" millisecondes (une image de 128 x 32 ou un GIF
      fixe reste une seule image, sur toute la dalle si elle en a la taille). Une image de toute la dalle dont le dessin
      tient au milieu (une explosion de DOFLinx) est recadrée et se joue à l'endroit de l'action, sauf "trim": false.
      Les fichiers du dossier perso
      passent avant les nôtres, par exemple ["perso/{game}/boom.gif", "perso/boom.gif", "sprites/fx_pop.png"].
    "on" : valeur(s) surveillée(s), "change" : "up" (défaut), "down" ou "any".
    "ratio" : [min, max], seulement si le gain est entre min et max fois le gain habituel (petit ennemi, gros ennemi).
    "x", "y" : le centre, un nombre ou [début, fin] (au hasard dedans). Une image de toute la dalle (128 x 32) se joue
      toujours sur toute la dalle.
    "count", "spread", "delay" : plusieurs animations réparties sur [début, fin] de "spread", l'une après l'autre.
    "black" : "clear" (défaut, le noir de l'image laisse voir la scène) ou "keep" (l'image recouvre tout, comme DOFLinx).
    "max" : animations en même temps au plus, "gap" : secondes entre deux départs. Rien pendant un décompte rapide de
      points (un bonus compté par le jeu)."""

    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.frames = None
        self.durs = []
        self.full = False
        self.game = None
        self.plays = []
        self.times = []
        self.gains = []
        self.last = -9.0
        self.rng = random.Random(11)
        self.count = 0                                   # (tests)

    def _load(self, game):
        from PIL import Image, ImageSequence
        self.game, self.frames, self.durs = game, [], []
        images = self.spec.get("image")
        images = images if isinstance(images, list) else [images]
        keep_black = self.spec.get("black") == "keep"
        ms = self.spec.get("ms")
        for name in images:
            if not name:
                continue
            name = str(name).replace("{game}", game or "_")
            path = name if os.path.isabs(name) else os.path.join(self.root, name)
            if not os.path.exists(path):
                continue
            try:
                img = Image.open(path)
                raw = []
                if getattr(img, "is_animated", False):                   # a GIF keeps its own timing / un GIF garde son rythme
                    for fr in ImageSequence.Iterator(img):
                        raw.append((fr.convert("RGBA").copy(), float(fr.info.get("duration") or ms or 80)))
                else:
                    gif = img.format == "GIF"
                    img = img.convert("RGBA")
                    w, h = img.size
                    strip = not gif and h and w % h == 0 and w > h and (w, h) != (128, 32)
                    n = max(1, int(self.spec.get("frames", 0) or (w // h if strip else 1)))
                    fw = w // n
                    d = float((img.info.get("duration") if gif else 0) or ms or 70)
                    if n == 1:                                         # a still image stays a moment / une image fixe reste un moment
                        d = float((img.info.get("duration") if gif else 0) or 0) or max(d, 500.0)
                    raw = [(img.crop((k * fw, 0, (k + 1) * fw, h)), d) for k in range(n)]
            except Exception as e:  # image illisible
                self.log(tr(f"animation illisible {path} : {e}", f"unreadable animation {path}: {e}"))
                continue
            for im, d in raw:
                if not keep_black:                           # le noir laisse voir la scène / black shows the scene
                    px = im.load()
                    for y in range(im.size[1]):
                        for x in range(im.size[0]):
                            r, g, b, a = px[x, y]
                            if r + g + b < 36:
                                px[x, y] = (0, 0, 0, 0)
            box = None
            if not keep_black and raw and raw[0][0].size == (128, 32) and self.spec.get("trim", True):
                for im, _ in raw:                            # une explosion au milieu d'une image de toute la dalle
                    b = im.getbbox()
                    if b:
                        box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
                if box and box[2] - box[0] > 48:
                    box = None                               # elle occupe la dalle : elle reste entière / it fills the panel
            for im, d in raw:
                self.frames.append(Sprite(im.crop(box) if box else im))
                self.durs.append(max(10.0, d) / 1000.0)
            self.full = bool(self.frames) and self.frames[0].w >= 128 and self.frames[0].h >= 32
            return

    def _ratio_ok(self, gain):
        rr = self.spec.get("ratio")
        past = sorted(self.gains)
        self.gains = (self.gains + [gain])[-24:]
        if not rr:
            return True
        ratio = 1.0 if len(past) < 3 else gain / max(1e-6, past[len(past) // 2])
        return float(rr[0]) <= ratio < float(rr[1])

    def _pick(self, v, cv_size):
        if isinstance(v, (list, tuple)) and len(v) == 2:
            return self.rng.uniform(float(v[0]), float(v[1]))
        return float(v if v is not None else cv_size / 2)

    def render(self, ctx):
        cv, t = ctx.canvas, ctx.t
        game = (ctx.state.meta or {}).get("game")
        if self.frames is None or game != self.game:
            self._load(game)
        names = self.spec.get("on") or ["score"]
        names = names if isinstance(names, list) else [names]
        change = self.spec.get("change", "up")
        for (name, old, new, et) in ctx.state.events:
            if name not in names or not isinstance(old, (int, float)) or not isinstance(new, (int, float)) or new == old:
                continue
            if (change == "up" and new < old) or (change == "down" and new > old):
                continue
            self.times = [x for x in self.times if t - x < 0.8] + [t]
            if len(self.times) > 6:                            # un bonus compté par le jeu / a bonus being counted
                continue
            if change == "up" and not self._ratio_ok(new - old):
                continue
            if not self.frames or t - self.last < float(self.spec.get("gap", 0.08)):
                continue
            self.last = t
            self.count += 1
            n = 1 if self.full else max(1, int(self.spec.get("count", 1)))
            spread = self.spec.get("spread")
            for k in range(n):
                if self.full:
                    x, y = cv.w / 2, cv.h / 2
                elif n > 1 and spread:
                    x = float(spread[0]) + (float(spread[1]) - float(spread[0])) * (k + 0.5) / n
                    y = self._pick(self.spec.get("y"), cv.h)
                else:
                    x, y = self._pick(self.spec.get("x"), cv.w), self._pick(self.spec.get("y"), cv.h)
                self.plays.append([t + k * float(self.spec.get("delay", 0.1)), x, y])
            self.plays = self.plays[-int(self.spec.get("max", 4)) - n:]
        if not self.frames:
            return
        total = sum(self.durs)
        alive = []
        for p in self.plays:
            el = t - p[0]
            if el < 0:
                alive.append(p)
                continue
            if el >= total:
                continue
            alive.append(p)
            k, acc = 0, 0.0
            while k < len(self.durs) - 1 and acc + self.durs[k] <= el:
                acc += self.durs[k]
                k += 1
            fr = self.frames[k]
            if self.full:
                cv.sprite(fr, 0, 0)
            else:                                            # inside the panel / dans la dalle
                x = min(max(p[1], fr.w / 2), cv.w - fr.w / 2)
                y = min(max(p[2], fr.h / 2), cv.h - fr.h / 2)
                cv.sprite(fr, int(round(x - fr.w / 2)), int(round(y - fr.h / 2)))
        self.plays = alive


class SpriteEl(Element):
    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.frames = []
        images = spec.get("image")
        images = images if isinstance(images, list) else [images]
        for img in images:
            if not img:
                continue
            path = img if os.path.isabs(img) else os.path.join(root, img)
            if os.path.exists(path):
                try:
                    self.frames = load_sprite_frames(path, spec.get("frame_w", 0), spec.get("frames", 0))
                    break
                except Exception as e:  # image illisible
                    log(tr(f"sprite illisible {path} : {e}", f"unreadable sprite {path}: {e}"))
        self.fps = float(spec.get("fps", 8))
        self.mode = spec.get("mode", "pass")
        self.y = spec.get("y", 10)
        self.speed = float(spec.get("speed", 40))
        self.every = float(spec.get("every", 6.0))
        self.x0 = spec.get("x0", 0)
        self.x1 = spec.get("x1", 128)
        self.face = spec.get("face", "right")
        self.bob = float(spec.get("bob", 0))
        self.x = spec.get("x", 0)
        self.alpha = float(spec.get("alpha", 1.0))
        dim = float(spec.get("dim", 1.0))
        if dim < 0.999 and self.frames:
            for fr in self.frames:          # moins lumineux, mais toujours opaque
                fr.points = [(x, y, scale_color(c, dim), a) for (x, y, c, a) in fr.points]
        self.shoot = spec.get("shoot")
        self.shells = []
        self.muzzle_until = 0.0
        self.last_shot = -9.0
        self.last_t = None

    def _shots(self, ctx, x, y, fr, moving_right):
        """Obus tirés quand une valeur surveillée augmente (par exemple le score)."""
        sh = self.shoot
        t = ctx.t
        dt = 0.0 if self.last_t is None else max(0.0, min(0.1, t - self.last_t))
        self.last_t = t
        cv = ctx.canvas
        names = sh.get("on", ["score"])
        names = names if isinstance(names, list) else [names]
        dx = int(sh.get("dx", fr.w))
        dy = int(sh.get("dy", 1))
        if x is not None:
            for (name, old, new, et) in ctx.state.events:
                if (name in names and isinstance(old, (int, float)) and isinstance(new, (int, float))
                        and new > old and t - self.last_shot >= float(sh.get("gap", 0.3))):
                    self.last_shot = t
                    sx = x + dx if moving_right else x + fr.w - 1 - dx
                    v = float(sh.get("speed", 80))
                    self.shells.append([float(sx), y + dy, v if moving_right else -v])
                    self.muzzle_until = t + 0.08
            if t < self.muzzle_until:
                mx = x + dx if moving_right else x + fr.w - 1 - dx
                cv.set(mx, y + dy, parse_color(sh.get("flash"), (255, 230, 120)))
        col = parse_color(sh.get("color"), (255, 80, 40))
        n = int(sh.get("len", 2))
        alive = []
        for s in self.shells:
            s[0] += s[2] * dt
            if -n <= s[0] <= cv.w + n:
                alive.append(s)
                step = -1 if s[2] > 0 else 1
                for k in range(n):
                    cv.set(int(s[0]) + step * k, s[1], col if k == 0 else scale_color(col, 0.5))
        self.shells = alive

    def render(self, ctx):
        if not self.frames:
            return
        lt = self.local_time(ctx)
        fr = self.frames[int(lt * self.fps) % len(self.frames)]
        cv = ctx.canvas
        moving_right = True
        if self.mode == "fixed":
            x = self.x
        elif self.mode == "pingpong":
            span = max(1, self.x1 - self.x0 - fr.w)
            p = (lt * self.speed) % (2 * span)
            moving_right = p < span
            x = self.x0 + (p if moving_right else 2 * span - p)
        else:  # "pass" : traverse l'écran puis attend
            travel = (cv.w + fr.w) / max(1.0, self.speed)
            cycle = travel + self.every
            p = lt % cycle
            right = self.spec.get("dir", "left") == "right"
            moving_right = right
            if p > travel:
                if self.shoot:
                    self._shots(ctx, None, self.y, fr, moving_right)
                return
            x = -fr.w + p * self.speed if right else cv.w - p * self.speed
        flip = (self.face == "right") != moving_right
        y = self.y + (int(round(math.sin(lt * 6.0) * self.bob)) if self.bob else 0)
        cv.sprite(fr, int(round(x)), y, flip=flip, alpha=self.alpha)
        if self.shoot:
            self._shots(ctx, int(round(x)), y, fr, moving_right)


class ClockEl(Element):
    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        self.font = Font.get(spec.get("font", "7x14"))
        self.fmt = spec.get("format", "%H:%M")
        self.x = spec.get("x", 64)
        self.y = spec.get("y", 9)
        self.align = spec.get("align", "center")
        self.color = parse_color(spec.get("color"), (255, 180, 40))
        self.blink = spec.get("blink", True)

    def render(self, ctx):
        s = time.strftime(self.fmt)
        if self.blink and int(time.time() * 2) % 2:
            s = s.replace(":", " ")
        w = self.font.width(s)
        x = self.x - w // 2 if self.align == "center" else (self.x - w + 1 if self.align == "right" else self.x)
        ctx.canvas.text(self.font, s, x, self.y, self.color)


class RectEl(Element):
    def render(self, ctx):
        s = self.spec
        ctx.canvas.fill_rect(s.get("x", 0), s.get("y", 0), s.get("w", 1), s.get("h", 1), parse_color(s.get("color"), (40, 40, 40)))


class ImageEl(Element):
    """Image fixe ou GIF animé. "image" peut être une liste de chemins candidats avec des
    gabarits, par exemple "{pixelcade}/mame/{system}.gif" : le premier qui existe est pris."""

    def __init__(self, spec, root, log, mapping=None):
        super().__init__(spec, root, log)
        self.frames = []
        images = spec.get("image", "")
        images = images if isinstance(images, list) else [images]
        for tpl in images:
            if not tpl:
                continue
            path = render_template(tpl, mapping or {}, "\0")
            if "\0" in path:
                continue
            path = path if os.path.isabs(path) else os.path.join(root, path)
            if os.path.exists(path):
                try:
                    fit = (128, 32) if spec.get("fit") else None
                    self.frames = load_sprite_frames(path, fit=fit)
                    break
                except Exception as e:
                    log(tr(f"image illisible {path} : {e}", f"unreadable image {path}: {e}"))
        self.alpha = float(spec.get("alpha", 1.0))
        self.fps = float(spec.get("fps", 10))

    def render(self, ctx):
        if self.frames:
            fr = self.frames[int(self.local_time(ctx) * self.fps) % len(self.frames)]
            ctx.canvas.sprite(fr, self.spec.get("x", 0), self.spec.get("y", 0), alpha=self.alpha)


def _int_value(ctx, name):
    v = ctx.state.values.get(name)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return int(v)


class IconsEl(Element):
    """A small drawing repeated for a value: lives as ships, bombs, power pips.
    "pattern": rows of characters, "." empty, other characters colored by "colors" (or "color").
    "max": at most this many, "empty": color of the slots left (up to max), "align": "left" or "right".

    Un petit dessin répété autant de fois que la valeur : vies en vaisseaux, bombes, niveaux de puissance."""

    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        rows = spec.get("pattern") or ["#"]
        base = parse_color(spec.get("color"), (255, 255, 255))
        cmap = {k: parse_color(v, base) for k, v in (spec.get("colors") or {}).items()}
        self.points = [(x, y, cmap.get(ch, base)) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch not in ". "]
        self.w = max((len(r) for r in rows), default=1)
        self.empty = parse_color(spec.get("empty"), None) if spec.get("empty") else None

    def render(self, ctx):
        s = self.spec
        n = _int_value(ctx, s.get("var", "lives"))
        if n is None:
            return
        mx = int(s.get("max", 8))
        n = max(0, min(n, mx))
        slots = mx if self.empty is not None else n
        gap = int(s.get("gap", 1))
        x0, y0 = int(s.get("x", 0)), int(s.get("y", 0))
        right = s.get("align") == "right"
        flash = _flash_color(s, ctx, None)
        cv = ctx.canvas
        for i in range(slots):
            ox = x0 - (i + 1) * self.w - i * gap + 1 if right else x0 + i * (self.w + gap)
            for (px, py, c) in self.points:
                col = c if i < n else self.empty
                if i < n and flash is not None:
                    col = flash
                cv.set(ox + px, y0 + py, col)


class DotEl(Element):
    """A round dot whose color comes from a value: the bubbles of Puzzle Bobble.
    "colors": color of each value (0, 1, 2...), "r": radius, "shine": a light pixel at the top left.
    Without "var" the dot is always drawn in the first color (a moon, a ball).

    Un disque dont la couleur vient d'une valeur : les bulles de Puzzle Bobble."""

    def render(self, ctx):
        s = self.spec
        v = _int_value(ctx, s["var"]) if s.get("var") else 0
        cols = s.get("colors") or []
        if v is None or not 0 <= v < len(cols) or not cols[v]:
            return
        col = parse_color(cols[v], (255, 255, 255))
        rim = parse_color(s.get("rim"), None) if s.get("rim") else None
        cx, cy, r = float(s.get("x", 0)), float(s.get("y", 0)), float(s.get("r", 3))
        cv = ctx.canvas
        for y in range(int(math.floor(cy - r)), int(math.ceil(cy + r)) + 1):
            for x in range(int(math.floor(cx - r)), int(math.ceil(cx + r)) + 1):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                if d > r:
                    continue
                c = col
                if rim is not None and d > r - 1.0:
                    c = rim
                elif d > r * 0.7:
                    c = scale_color(col, 0.7)
                cv.set(x, y, c)
        if s.get("shine", True) and r >= 2.5:
            cv.add(int(cx - r * 0.45), int(cy - r * 0.45), (255, 255, 255), 0.85)


class ArrowEl(Element):
    """An arrow pointing in the direction of a value: the wind of Neo Turf Masters.
    "steps": number of directions (16), 0 points up, then clockwise. "ring": circle color around it.

    Une flèche orientée selon une valeur : le vent de Neo Turf Masters."""

    def render(self, ctx):
        s = self.spec
        v = _int_value(ctx, s.get("var", ""))
        if v is None:
            return
        steps = max(1, int(s.get("steps", 16)))
        a = math.radians(360.0 * (v % steps) / steps + float(s.get("offset", 0)))
        cx, cy, ln = float(s.get("x", 0)), float(s.get("y", 0)), float(s.get("len", 6))
        col = _flash_color(s, ctx, parse_color(s.get("color"), (255, 255, 255)))
        cv = ctx.canvas
        if s.get("ring"):
            ring = parse_color(s.get("ring"), (60, 60, 80))
            for k in range(48):
                t = k * math.tau / 48
                cv.set(int(round(cx + math.cos(t) * (ln + 1.5))), int(round(cy + math.sin(t) * (ln + 1.5))), ring)
        dx, dy = math.sin(a), -math.cos(a)

        def line(x0, y0, x1, y1, c):
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
            for i in range(n + 1):
                k = i / n
                cv.set(int(round(x0 + (x1 - x0) * k)), int(round(y0 + (y1 - y0) * k)), c)

        tip = (cx + dx * ln, cy + dy * ln)
        line(cx - dx * ln * 0.8, cy - dy * ln * 0.8, tip[0], tip[1], col)
        for side in (-1, 1):                                      # pointe de la flèche
            b = a + math.pi + side * 0.55
            line(tip[0], tip[1], tip[0] + math.sin(b) * ln * 0.55, tip[1] - math.cos(b) * ln * 0.55, col)


# --------------------------------------------------------------------------
# attract screen of a game with credits / écran d'attente d'un jeu à crédits
# --------------------------------------------------------------------------

GOLD_TOP, GOLD_BOTTOM, WHITE = (255, 246, 160), (255, 130, 15), (255, 255, 255)
COIN_FACE, COIN_LIGHT, COIN_RIM, COIN_EDGE, COIN_SIGN = (255, 200, 40), (255, 246, 170), (205, 125, 15), (150, 92, 8), (115, 60, 0)
EURO = ("..###", ".#...", "####.", ".#...", "####.", ".#...", "..###")
# coin symbol ("coin_symbol" in config.json): €, $, £ or "" for a plain coin / symbole de la pièce
COIN_SYMBOLS = {"€": EURO,
                "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
                "£": ("..##.", ".#..#", ".#...", "###..", ".#...", ".#...", "#####")}


def _mix(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t), int(a[2] + (b[2] - a[2]) * t))


class CoinOpEl(Element):
    """Attract screen of a game with credits, drawn over the whole panel.

    With no credit, a € coin floats above a coin slot, next to INSERT COIN. When the credits go up, the coin
    drops into the slot, +1 rises and the credit counter rolls. A moment later, PRESS START with a button.
    "title": segments of the title that scrolls at the top. "idle_image": your own GIF (or PNG) shown
    instead of the INSERT COIN screen, for example sprites/insert_coin.gif.

    Écran d'attente d'un jeu à crédits, sur toute la dalle. Sans crédit, une pièce € flotte au-dessus d'une
    fente, à côté de INSERT COIN. Quand les crédits montent, la pièce tombe dans la fente, +1 monte et le
    compteur de crédits roule. Puis PRESS START avec un bouton. "idle_image" : ton propre GIF à la place."""

    HOLD = 2.6                       # seconds of CREDITS n after a coin, then PRESS START
    FALL, INSERT, GLOW = 0.35, 0.40, 0.30
    SLOT_X, SLOT_W, SLOT_Y = 3, 19, 25
    R = 6.5
    HOVER = 9.5
    ZONE_X, ZONE_W = 26, 102         # right part of the panel: title and big texts

    def __init__(self, spec, root, log):
        super().__init__(spec, root, log)
        base = parse_color(spec.get("color"), (255, 168, 48))
        title = [g for g in spec.get("title", []) if isinstance(g, dict)] or [{"text": "{title}", "color": "#ffa830"}]
        self.marquee = MarqueeEl({"segments": title, "font": "6x10", "x": self.ZONE_X, "y": 1, "w": self.ZONE_W,
                                  "speed": 12, "gap": 40, "upper": True, "color": base}, root, log)
        self.big = Font.get(spec.get("font", "8x13B"))
        self.small = Font.get("4x6")
        self.plus = Font.get("6x10")
        self.line = parse_color(spec.get("line"), (168, 112, 30)) if spec.get("line", True) else None
        self.frames = []
        images = spec.get("idle_image") or []
        for img in images if isinstance(images, list) else [images]:
            path = img if os.path.isabs(img) else os.path.join(root, img)
            if img and os.path.exists(path):
                try:
                    self.frames = load_sprite_frames(path, fit=(128, 32))
                    break
                except Exception as e:  # image illisible
                    log(tr(f"image d'attente illisible {path} : {e}", f"unreadable attract image {path}: {e}"))
        self.fps = float(spec.get("fps", 12))
        self.symbol = EURO
        self.restart()

    def restart(self):
        super().restart()
        self.marquee.restart()
        self.credits = None
        self.seen = None
        self.inserted = None
        self.roll_from = 0

    # -- drawing helpers
    def _coin(self, cv, cx, cy, f, clip_bottom=None):
        """€ coin seen from the front (f = 1) or more and more from the side (f towards 0), cut below clip_bottom."""
        r = self.R
        rx = max(0.6, r * f)
        for y in range(int(math.floor(cy - r)), int(math.ceil(cy + r)) + 1):
            if clip_bottom is not None and y >= clip_bottom:
                continue
            for x in range(int(math.floor(cx - rx)) - 1, int(math.ceil(cx + rx)) + 2):
                dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / r
                d = dx * dx + dy * dy
                if d > 1.0:
                    continue
                if f < 0.3:
                    col = COIN_EDGE if abs(x + 0.5 - cx) < 0.7 else COIN_RIM
                elif d > 0.55:
                    col = COIN_RIM
                else:
                    col = COIN_LIGHT if (dx < -0.05 and dy < -0.05 and d < 0.3) else COIN_FACE
                cv.set(x, y, col)
        if f > 0.8 and self.symbol:
            for j, row in enumerate(self.symbol):
                yy = int(round(cy)) - 3 + j
                if clip_bottom is not None and yy >= clip_bottom:
                    continue
                for i, ch in enumerate(row):
                    if ch == "#":
                        cv.set(int(round(cx)) - 2 + i, yy, COIN_SIGN)

    def _slot(self, cv, glow):
        lip = _mix((205, 205, 215), (255, 225, 130), glow)
        x0, y0, w = self.SLOT_X, self.SLOT_Y, self.SLOT_W
        for x in range(x0, x0 + w):
            end = x in (x0, x0 + w - 1)
            cv.set(x, y0, scale_color(lip, 0.65 if end else 1.0))
            cv.set(x, y0 + 1, scale_color(lip, 0.45))
        if glow > 0:
            for x in range(x0 + 1, x0 + w - 1):
                cv.add(x, y0 - 1, (255, 215, 110), 0.7 * glow)
                cv.add(x, y0 - 2, (255, 215, 110), 0.3 * glow)

    def _idle_coin(self, cv, t, appear=1.0):
        cx = self.SLOT_X + self.SLOT_W / 2
        f = max(0.3, abs(math.cos(2 * math.pi * t / 2.4)))
        cy = self.HOVER + 0.8 * math.sin(t * 3)
        if appear < 1.0:                                  # the next coin comes down from the top
            e = 1 - (1 - appear) ** 2
            cy = -self.R - 1 + (cy + self.R + 1) * e
        self._coin(cv, cx, cy, f)

    def _drop(self, cv, lt):
        """Coin put in: falls into the slot and goes in on its edge, the slot lights up, a new coin arrives."""
        cx = self.SLOT_X + self.SLOT_W / 2
        rest = self.SLOT_Y - self.R
        if lt < self.FALL:
            k = lt / self.FALL
            self._coin(cv, cx, self.HOVER + (rest - self.HOVER) * k * k, 1.0)
            return 0.0
        if lt < self.FALL + self.INSERT:
            k = (lt - self.FALL) / self.INSERT
            self._coin(cv, cx, rest + (2 * self.R + 1) * k, 1.0 - 0.75 * k, clip_bottom=self.SLOT_Y)
            return 0.25 * k
        done = lt - self.FALL - self.INSERT
        if done >= self.GLOW * 0.5:
            self._idle_coin(cv, lt, appear=min(1.0, (done - self.GLOW * 0.5) / 0.45))
        return max(0.0, 1.0 - done / self.GLOW)

    def _button(self, cv, cx, cy, r, press, glow):
        for y in range(int(cy - r - 3), int(cy + r + 4)):
            for x in range(int(cx - r - 3), int(cx + r + 4)):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                if r + 1.2 < d <= r + 2.8:
                    cv.add(x, y, (255, 70, 30), 0.4 * glow)
                elif r < d <= r + 1.2:
                    cv.set(x, y, (70, 70, 80))
        oy = 1 if press else 0
        for y in range(int(cy - r), int(cy + r + 1)):
            for x in range(int(cx - r), int(cx + r + 1)):
                dx, dy = x + 0.5 - cx, y + 0.5 - (cy + oy * 0.6)
                d = math.hypot(dx, dy)
                if d > r - (0.6 if press else 0):
                    continue
                col = (150, 15, 8) if press else (215, 25, 15)
                if dx < -1 and dy < -1 and d < r * 0.55 and not press:
                    col = (255, 175, 160)
                elif dx + dy > r * 0.6:
                    col = scale_color(col, 0.7)
                cv.set(x, y, col)

    def _gold(self, cv, text, x, y, t, k=1.0, flash=0.0):
        """Big gold text, lighter at the top, with a light sweep."""
        font = self.big
        sx = 20 + ((t % 2.2) / 2.2) * 130
        oy = y - font.cap_top
        cx = x
        for ch in text:
            for (px, py) in font.glyph_points(ch):
                r = py - font.cap_top
                col = scale_color(_mix(GOLD_TOP, GOLD_BOTTOM, max(0.0, min(1.0, r / 9.0))), k)
                dd = abs((cx + px - sx) - r * 0.5)
                if dd < 4.0:
                    col = _mix(col, WHITE, (1 - dd / 4.0) * 0.85)
                if flash:
                    col = _mix(col, WHITE, flash)
                cv.set(cx + px, oy + py, col)
            cx += font.w
        return cx - x

    def _centered_x(self, text):
        return self.ZONE_X + (self.ZONE_W - self.big.width(text)) // 2

    # -- frame
    def render(self, ctx):
        cv, t = ctx.canvas, ctx.t
        cv.clear((0, 0, 0))
        sym = self.spec.get("symbol", (getattr(ctx, "cfg", None) or {}).get("coin_symbol", "€"))
        self.symbol = COIN_SYMBOLS.get(str(sym or "").strip())
        c = ctx.state.values.get("credits")
        c = c if isinstance(c, (int, float)) and not isinstance(c, bool) else None
        if self.seen is None or t - self.seen > 0.5:          # shown again: no coin for credits added meanwhile
            self.credits = c
        elif c is not None and self.credits is not None and c > self.credits:
            self.roll_from = int(self.credits)
            self.inserted = t
            self.credits = c
        else:
            self.credits = c
        self.seen = t
        recent = self.inserted is not None and 0 <= t - self.inserted < self.HOLD
        if not recent and not c and self.frames:               # your own INSERT COIN animation
            fr = self.frames[int(self.local_time(ctx) * self.fps) % len(self.frames)]
            cv.sprite(fr, 0, 0)
            return
        self.marquee.render(ctx)
        if recent:
            lt = t - self.inserted
            self._slot(cv, self._drop(cv, lt))
            shown = self.FALL + self.INSERT                   # the counter changes when the coin is in
            n = int(c) if lt >= shown else self.roll_from
            if shown <= lt < shown + 0.8:                     # +1 rising from the slot
                k = (lt - shown) / 0.8
                cv.text(self.plus, "+1", int(self.SLOT_X + self.SLOT_W / 2 - 6), int(self.SLOT_Y - 9 - 10 * k),
                        _mix(WHITE, (255, 168, 48), k), alpha=1 - k * 0.8)
            if n <= 0:
                self._gold(cv, "INSERT COIN", self._centered_x("INSERT COIN"), 14, t)
            else:
                word = panel_text(f"CREDIT {n}" if n == 1 else f"CREDITS {n}")
                num = str(n)
                label = word[:-len(num)]
                x = self._centered_x(word)
                roll = min(1.0, max(0.0, (lt - shown) / 0.25))
                flash = max(0.0, 1 - (lt - shown) / 0.4) if lt >= shown else 0.0
                self._gold(cv, label, x, 14, t, flash=flash)
                nx = x + self.big.width(label)
                cv.set_clip(nx, 12, nx + self.big.w * max(len(num), len(str(self.roll_from))) + 1, 26)
                if lt >= shown and roll < 1.0:
                    cv.text(self.big, str(self.roll_from), nx, int(14 - 13 * roll), (255, 168, 48))
                    cv.text(self.big, num, nx, int(14 + 13 * (1 - roll)), _mix((255, 168, 48), WHITE, flash))
                else:
                    self._gold(cv, num, nx, 14, t, flash=flash)
                cv.reset_clip()
        elif c:                                               # credits: PRESS START with a button
            lt = t % 1.2
            self._button(cv, self.SLOT_X + self.SLOT_W / 2, 20.5, 6.0, 0.15 < lt < 0.4, 0.5 + 0.5 * math.sin(t * 6))
            cv.text(self.small, "1P", int(self.SLOT_X + self.SLOT_W / 2) - 3, 9, (255, 168, 48))
            k = 0.75 + 0.25 * math.sin(t * 6)
            self._gold(cv, "PRESS START", self._centered_x("PRESS START"), 13, t, k=k)
            n = int(c)
            s = panel_text(f"CREDIT {n}" if n == 1 else f"CREDITS {n}")
            cv.text(self.small, s, self.ZONE_X + (self.ZONE_W - self.small.width(s)) // 2, 25, scale_color((255, 168, 48), 0.8))
        else:                                                 # no credit: the coin floats above the slot
            self._idle_coin(cv, t)
            self._slot(cv, 0.0)
            k = 0.8 + 0.2 * math.sin(t * 5)
            self._gold(cv, "INSERT COIN", self._centered_x("INSERT COIN"), 14, t, k=k)
        if self.line is not None:
            cv.fill_rect(0, 30, 128, 2, self.line)


class LogoIntro:
    """The game's logo (LaunchBox Clear Logo) at the start of a game, on the 128 x 32 panel: it zooms in,
    a light sweeps across it, then the scene comes. / Le logo du jeu au lancement, sur la dalle 128 x 32."""

    def __init__(self, path, t0, seconds=2.6):
        from PIL import Image
        img = Image.open(path)
        img.load()
        img = img.convert("RGBA")
        box = img.getchannel("A").getbbox()
        if box:
            img = img.crop(box)
        k = min(126 / img.width, 30 / img.height)
        self.base = img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.LANCZOS)
        k4 = min(1.0, 4 * k)                       # big logo brought down to 4 x the panel: quick zoom frames
        self.big = img.resize((max(1, int(img.width * k4)), max(1, int(img.height * k4))), Image.LANCZOS) if k4 < 1 else img
        self.t0 = t0
        self.seconds = max(1.0, min(10.0, float(seconds)))
        self.cache = {}

    def _frame(self, sc):
        from PIL import Image
        key = round(sc, 2)
        hit = self.cache.get(key)
        if hit is None:
            w, h = max(1, int(self.base.width * key)), max(1, int(self.base.height * key))
            small = self.big.resize((w, h), Image.LANCZOS)
            tile = Image.new("RGBA", (128, 32), (0, 0, 0, 0))
            tile.paste(small, ((128 - w) // 2, (32 - h) // 2), small)
            px = tile.load()
            hit = [(x, y, px[x, y][:3], px[x, y][3] / 255.0) for y in range(32) for x in range(128) if px[x, y][3] > 30]
            self.cache[key] = hit
        return hit

    def draw(self, cv, now):
        """Draws the intro over the whole panel. False when it is over."""
        lt = now - self.t0
        if lt < 0 or lt >= self.seconds:
            return False
        sc = 0.45 + 0.55 * min(1.0, lt / 0.45) ** 0.6
        k = min(1.0, lt / 0.3, max(0.0, (self.seconds - lt) / 0.3))
        sx = -20 + (lt - 0.6) / 0.7 * 170 if 0.6 <= lt < 1.3 else -99
        cv.clear((0, 0, 0))
        pts = self._frame(sc)
        for x, y, col, a in pts:
            c = scale_color(col, a * k)
            dd = abs((x - sx) - (y - 16) * 0.6)
            if dd < 5:
                c = _mix(c, WHITE, (1 - dd / 5) * 0.8 * k)
            cv.set(x, y, c)
        if lt > 1.3 and pts:
            rng = random.Random(int(lt * 10))
            for _ in range(3):
                x, y, _, a = pts[rng.randrange(len(pts))]
                if a > 0.5:
                    cv.add(x, y, WHITE, 0.8 * k)
        return True


class Scene:
    def __init__(self, spec, root, log=print, mapping=None):
        self.spec = spec or {}
        self.root = root
        self.log = log
        self.mapping = mapping or {}
        self.background = parse_color(self.spec.get("background"), (0, 0, 0))
        self.layers = [self._make(e) for e in self.spec.get("layers", [])]
        self.layers = [e for e in self.layers if e is not None]

    def _make(self, spec):
        kind = spec.get("type", "text")
        cls = {
            "text": TextEl, "marquee": MarqueeEl, "bars": BarsEl, "waves": WavesEl, "mountains": MountainsEl, "gauge": GaugeEl,
            "particles": ParticlesEl, "sprite": SpriteEl, "clock": ClockEl, "anim": AnimEl,
            "rect": RectEl, "image": ImageEl, "coinop": CoinOpEl, "icons": IconsEl, "dot": DotEl, "arrow": ArrowEl,
        }.get(kind)
        if kind == "cycle":
            return CycleEl(spec, self.root, self.log, self._make)
        if kind == "image":
            try:
                return ImageEl(spec, self.root, self.log, self.mapping)
            except Exception as e:
                self.log(tr(f"élément image ignoré : {e}", f"image element ignored: {e}"))
                return None
        if cls is None:
            self.log(tr(f"type d'élément inconnu : {kind}", f"unknown element type: {kind}"))
            return None
        try:
            return cls(spec, self.root, self.log)
        except Exception as e:
            self.log(tr(f"élément {kind} ignoré : {e}", f"{kind} element ignored: {e}"))
            return None

    def restart(self):
        for e in self.layers:
            e.restart()

    def render(self, ctx):
        ctx.canvas.clear(self.background)
        for e in self.layers:
            if e.visible(ctx):
                e.render(ctx)
