"""Your own pictures for the HD screen. The scene of a game can show the images you keep in artwork\\<game>\\hd\\
(a character, items, backdrops, a map). That folder is never published and an update never touches it. Without them,
the scene keeps its own drawings, or shows nothing where only the real picture makes sense.

Tes propres images pour l'écran HD. La scène d'un jeu peut montrer les images que tu gardes dans artwork\\<jeu>\\hd\\
(un personnage, des objets, des décors, une carte). Ce dossier n'est jamais publié et une mise à jour n'y touche pas.
Sans elles, la scène garde ses dessins, ou ne montre rien là où seule la vraie image a du sens.

A picture is found by its name without extension (.png, .gif, .webp or .jpg). An animated GIF or WebP plays with its own
timing. A PNG strip of N frames side by side is cut when the scene asks for N frames. Small pixel art (a sprite taken
from the game) is enlarged by a whole factor without smoothing, so it stays sharp.
/ Une image se trouve par son nom sans extension. Un GIF animé garde son rythme, une bande PNG se découpe, un petit
sprite est agrandi sans lissage pour rester net."""
import os

EXTS = (".png", ".gif", ".webp", ".jpg", ".jpeg")
MAX_FRAMES = 240


def folder(root, game):
    """artwork/<game>/hd: the HD pictures of a game. / Les images HD d'un jeu."""
    return os.path.join(root, "artwork", game, "hd")


def find(root, game, name):
    """The path of artwork/<game>/hd/<name>.<ext>, or None. / Le chemin de l'image, ou None."""
    if not game or not name:
        return None
    base = folder(root, game)
    for ext in EXTS:
        p = os.path.join(base, name + ext)
        if os.path.isfile(p):
            return p
    return None


def frames(path, strip=None):
    """[(PIL RGBA image, seconds)]: every frame of an animated picture, or the frames of a strip of `strip` images.
    / Toutes les images d'une animation, ou celles d'une bande."""
    from PIL import Image, ImageSequence
    img = Image.open(path)
    out = []
    if getattr(img, "is_animated", False):
        for fr in ImageSequence.Iterator(img):
            out.append((fr.convert("RGBA").copy(), max(0.02, float(fr.info.get("duration") or 100) / 1000.0)))
            if len(out) >= MAX_FRAMES:
                break
        return out
    img = img.convert("RGBA")
    w, h = img.size
    if strip and strip > 1 and w % strip == 0:
        fw = w // strip
        return [(img.crop((k * fw, 0, (k + 1) * fw, h)), 0.0) for k in range(strip)]
    return [(img, 0.0)]


class UserArt:
    """The HD pictures of one game as pygame surfaces, loaded once, scaled once to each size asked.
    / Les images HD d'un jeu, chargées une fois, mises à chaque taille demandée une fois."""

    def __init__(self, pg, root, game, log=None):
        self.pg, self.root, self.game, self.log = pg, root, game, log or (lambda m: None)
        self.paths = {}
        self.raw = {}
        self.cache = {}
        self.bad = set()

    def path(self, name):
        if name not in self.paths:
            self.paths[name] = find(self.root, self.game, name)
        return self.paths[name]

    def has(self, name):
        """True when the picture is in the folder. / Vrai quand l'image est dans le dossier."""
        return self.path(name) is not None and name not in self.bad

    def _raw(self, name, strip):
        key = (name, strip)
        if key not in self.raw:
            p = self.path(name)
            try:
                self.raw[key] = frames(p, strip) if p else []
            except Exception as e:  # noqa: BLE001 - a broken file is skipped / un fichier abîmé est ignoré
                self.log(f"artwork: {p}: {e}")
                self.bad.add(name)
                self.raw[key] = []
        return self.raw[key]

    def size(self, name, strip=None):
        """(width, height) of the picture (of one frame of a strip), or None. / La taille d'origine."""
        raw = self._raw(name, strip)
        return raw[0][0].size if raw else None

    def _scaled(self, im, w, h, flip):
        pg = self.pg
        sw, sh = im.size
        surf = pg.image.fromstring(im.tobytes(), (sw, sh), "RGBA").convert_alpha()
        k = min(w / sw, h / sh)
        if k >= 2.0 and sw <= 256 and sh <= 256:                 # a sprite of the game stays sharp / reste net
            n = int(k)
            surf = pg.transform.scale(surf, (sw * n, sh * n))
            if (sw * n, sh * n) != (w, h) and k - n > 0.05:
                surf = pg.transform.smoothscale(surf, (int(sw * k), int(sh * k)))
        elif (sw, sh) != (int(sw * k), int(sh * k)):
            surf = pg.transform.smoothscale(surf, (max(1, int(sw * k)), max(1, int(sh * k))))
        if flip:
            surf = pg.transform.flip(surf, True, False)
        return surf

    def get(self, name, w=None, h=None, now=0.0, strip=None, fps=8.0, flip=False, frame=None):
        """The picture fitted in w x h (ratio kept), the frame of the moment for an animation, or None.
        `frame` picks a frame of a strip. / L'image tenue dans w x h, l'image du moment pour une animation."""
        raw = self._raw(name, strip)
        if not raw:
            return None
        sw, sh = raw[0][0].size
        if w is None and h is None:
            w, h = sw, sh
        elif w is None:
            w = max(1, int(sw * h / sh))
        elif h is None:
            h = max(1, int(sh * w / sw))
        if frame is not None:
            i = int(frame) % len(raw)
        elif len(raw) == 1:
            i = 0
        else:
            durs = [d if d > 0 else 1.0 / max(1.0, fps) for _, d in raw]
            t = now % sum(durs)
            i = 0
            while i < len(durs) - 1 and t >= durs[i]:
                t -= durs[i]
                i += 1
        key = (name, strip, i, int(w), int(h), bool(flip))
        surf = self.cache.get(key)
        if surf is None:
            surf = self.cache[key] = self._scaled(raw[i][0], int(w), int(h), flip)
        return surf
