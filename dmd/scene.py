"""Scènes : interprète les fichiers games/*.json et dessine chaque image."""

import math
import os
import random
import string
import time

from .canvas import Font, parse_color, scale_color, load_sprite_frames


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
        return all(state.values.get(n) is not None for n in names)
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
        return check_when(self.when, ctx.state, ctx.t)

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
            s = render_template(tpl, mapping, self.missing)
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
        w = self.font.width(full, self.spacing)
        x = self.x
        if self.align == "center":
            x = self.x - w // 2
        elif self.align == "right":
            x = self.x - w + 1
        ctx.canvas.text(self.font, full, x, self.y, self.base, self.spacing, colors)


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
            parts = [(render_template(t, mapping, ""), c) for t, c in self.segments]
            s = "".join(p for p, _ in parts)
            seg_colors = [c for p, c in parts for _ in p]
        else:
            s = render_template(self.text, mapping, "")
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


class ParticlesEl(Element):
    """Missiles qui traversent + gerbes d'étincelles quand une valeur augmente."""

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
                    cx = self.rng.randint(20, cv.w - 20)
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
                    log(f"sprite illisible {path} : {e}")
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
                    log(f"image illisible {path} : {e}")
        self.alpha = float(spec.get("alpha", 1.0))
        self.fps = float(spec.get("fps", 10))

    def render(self, ctx):
        if self.frames:
            fr = self.frames[int(self.local_time(ctx) * self.fps) % len(self.frames)]
            ctx.canvas.sprite(fr, self.spec.get("x", 0), self.spec.get("y", 0), alpha=self.alpha)


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
            "text": TextEl, "marquee": MarqueeEl, "bars": BarsEl, "waves": WavesEl, "mountains": MountainsEl,
            "particles": ParticlesEl, "sprite": SpriteEl, "clock": ClockEl,
            "rect": RectEl, "image": ImageEl,
        }.get(kind)
        if kind == "cycle":
            return CycleEl(spec, self.root, self.log, self._make)
        if kind == "image":
            try:
                return ImageEl(spec, self.root, self.log, self.mapping)
            except Exception as e:
                self.log(f"élément image ignoré : {e}")
                return None
        if cls is None:
            self.log(f"type d'élément inconnu : {kind}")
            return None
        try:
            return cls(spec, self.root, self.log)
        except Exception as e:
            self.log(f"élément {kind} ignoré : {e}")
            return None

    def restart(self):
        for e in self.layers:
            e.restart()

    def render(self, ctx):
        ctx.canvas.clear(self.background)
        for e in self.layers:
            if e.visible(ctx):
                e.render(ctx)
