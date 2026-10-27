"""128x32 RGB framebuffer, bitmap fonts and drawing primitives (text, sprites, blending).

Framebuffer 128x32 RGB, fonts bitmap et primitives de dessin."""

from .fonts_data import FONTS

WIDTH = 128
HEIGHT = 32


def parse_color(value, default=(255, 255, 255)):
    """Accepte [r, g, b], (r, g, b) ou '#rrggbb'."""
    if value is None:
        return default
    if isinstance(value, str):
        s = value.strip().lstrip("#")
        if len(s) == 3:
            s = "".join(c * 2 for c in s)
        try:
            return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
        except ValueError:
            return default
    if isinstance(value, (list, tuple)) and len(value) >= 3:
        return (int(value[0]) & 255, int(value[1]) & 255, int(value[2]) & 255)
    return default


def scale_color(c, k):
    return (min(255, int(c[0] * k)), min(255, int(c[1] * k)), min(255, int(c[2] * k)))


def mix(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t), int(a[2] + (b[2] - a[2]) * t))


class Font:
    _cache = {}

    def __init__(self, name):
        data = FONTS[name]
        self.name = name
        self.w = data["w"]
        self.h = data["h"]
        self.cap_top = data["cap_top"]
        self.cap_h = data["cap_h"]
        hexw = data["hexw"]
        self.glyphs = {}
        for code, s in data["glyphs"].items():
            self.glyphs[int(code)] = [int(s[i:i + hexw], 16) for i in range(0, len(s), hexw)]
        # precompute pixel offsets for speed
        self.pixels = {}
        for code, rows in self.glyphs.items():
            pts = []
            for y, bits in enumerate(rows):
                for x in range(self.w):
                    if bits & (1 << (self.w - 1 - x)):
                        pts.append((x, y))
            self.pixels[code] = pts

    @classmethod
    def get(cls, name):
        if name not in FONTS:
            name = "6x10"
        f = cls._cache.get(name)
        if f is None:
            f = cls._cache[name] = Font(name)
        return f

    def glyph_points(self, ch):
        pts = self.pixels.get(ord(ch))
        if pts is None:
            pts = self.pixels.get(ord(_fold_char(ch)), self.pixels.get(ord("?"), []))
        return pts

    def width(self, text, spacing=0):
        if not text:
            return 0
        return len(text) * (self.w + spacing) - spacing


_FOLD = str.maketrans(
    "ŒœŠšŽžŸ‘’“”–—…",
    "OoSsZzY''\"\"--.",
)


def _fold_char(ch):
    return ch.translate(_FOLD) if len(ch) == 1 else "?"


class Canvas:
    """Framebuffer RGB888 en bytearray (rapide en Python pur)."""

    def __init__(self, width=WIDTH, height=HEIGHT):
        self.w = width
        self.h = height
        self.buf = bytearray(width * height * 3)
        self.clip = (0, 0, width, height)

    def clear(self, color=(0, 0, 0)):
        r, g, b = color
        if r == g == b:
            self.buf[:] = bytes([r]) * len(self.buf)
        else:
            self.buf[:] = bytes((r, g, b)) * (self.w * self.h)

    def set_clip(self, x0=0, y0=0, x1=None, y1=None):
        self.clip = (max(0, x0), max(0, y0), min(self.w, self.w if x1 is None else x1),
                     min(self.h, self.h if y1 is None else y1))

    def reset_clip(self):
        self.clip = (0, 0, self.w, self.h)

    def set(self, x, y, c):
        cx0, cy0, cx1, cy1 = self.clip
        if cx0 <= x < cx1 and cy0 <= y < cy1:
            i = (y * self.w + x) * 3
            self.buf[i] = c[0]
            self.buf[i + 1] = c[1]
            self.buf[i + 2] = c[2]

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            return (self.buf[i], self.buf[i + 1], self.buf[i + 2])
        return (0, 0, 0)

    def add(self, x, y, c, k=1.0):
        """Mélange additif (lueurs, particules)."""
        cx0, cy0, cx1, cy1 = self.clip
        if cx0 <= x < cx1 and cy0 <= y < cy1:
            i = (y * self.w + x) * 3
            b = self.buf
            b[i] = min(255, b[i] + int(c[0] * k))
            b[i + 1] = min(255, b[i + 1] + int(c[1] * k))
            b[i + 2] = min(255, b[i + 2] + int(c[2] * k))

    def blend(self, x, y, c, a):
        cx0, cy0, cx1, cy1 = self.clip
        if cx0 <= x < cx1 and cy0 <= y < cy1:
            i = (y * self.w + x) * 3
            b = self.buf
            b[i] = int(b[i] + (c[0] - b[i]) * a)
            b[i + 1] = int(b[i + 1] + (c[1] - b[i + 1]) * a)
            b[i + 2] = int(b[i + 2] + (c[2] - b[i + 2]) * a)

    def fill_rect(self, x, y, w, h, c):
        for yy in range(max(0, y), min(self.h, y + h)):
            for xx in range(max(0, x), min(self.w, x + w)):
                self.set(xx, yy, c)

    def hline(self, x0, x1, y, c):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            self.set(x, y, c)

    def vline(self, x, y0, y1, c):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            self.set(x, y, c)

    def text(self, font, text, x, y, color, spacing=0, colors=None, alpha=None):
        """Dessine `text` avec le haut des majuscules en `y`.

        colors : liste optionnelle de couleurs par caractère (None = color).
        Retourne la largeur dessinée.
        """
        oy = y - font.cap_top
        cx = x
        cx0, cy0, cx1, cy1 = self.clip
        adv = font.w + spacing
        for idx, ch in enumerate(text):
            if cx + font.w > cx0 and cx < cx1:
                col = color
                if colors is not None and idx < len(colors) and colors[idx] is not None:
                    col = colors[idx]
                for (px, py) in font.glyph_points(ch):
                    if alpha is None:
                        self.set(cx + px, oy + py, col)
                    else:
                        self.blend(cx + px, oy + py, col, alpha)
            cx += adv
        return cx - x - (spacing if text else 0)

    def sprite(self, img, x, y, flip=False, alpha=1.0):
        """img : objet Sprite (liste de pixels RGBA)."""
        w = img.w
        for (px, py, c, a) in img.points:
            if flip:
                px = w - 1 - px
            k = a * alpha
            if k >= 0.99:
                self.set(x + px, y + py, c)
            elif k > 0.02:
                self.blend(x + px, y + py, c, k)

    def dim(self, k):
        b = self.buf
        for i in range(len(b)):
            b[i] = int(b[i] * k)

    def to_bytes(self):
        return bytes(self.buf)


class Sprite:
    """Image RGBA chargée via Pillow et réduite à une liste de pixels visibles."""

    def __init__(self, image):
        image = image.convert("RGBA")
        self.w, self.h = image.size
        self.points = []
        px = image.load()
        for y in range(self.h):
            for x in range(self.w):
                r, g, b, a = px[x, y]
                if a > 8:
                    self.points.append((x, y, (r, g, b), a / 255.0))


def load_sprite_frames(path, frame_w=0, frames=0, fit=None):
    """Charge un PNG (bande horizontale de frames) ou un GIF animé.

    fit=(w, h) : réduit chaque image pour tenir dans w x h (centrée), utile pour les
    marquees d'autres tailles."""
    from PIL import Image, ImageSequence

    def fitted(im):
        im = im.convert("RGBA")
        if fit and im.size != tuple(fit):
            im.thumbnail(fit, Image.LANCZOS)
            canvas = Image.new("RGBA", fit, (0, 0, 0, 0))
            canvas.paste(im, ((fit[0] - im.size[0]) // 2, (fit[1] - im.size[1]) // 2))
            im = canvas
        return im

    img = Image.open(path)
    out = []
    if getattr(img, "is_animated", False):
        for fr in ImageSequence.Iterator(img):
            out.append(Sprite(fitted(fr.copy())))
        return out
    img = img.convert("RGBA")
    w, h = img.size
    if frames and frames > 1 and not frame_w:
        frame_w = w // frames
    if frame_w and frame_w < w:
        for x in range(0, w - frame_w + 1, frame_w):
            out.append(Sprite(fitted(img.crop((x, 0, x + frame_w, h))) if fit else img.crop((x, 0, x + frame_w, h))))
    else:
        out.append(Sprite(fitted(img) if fit else img))
    return out
