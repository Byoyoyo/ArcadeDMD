"""Sorties : dalle ZeDMD (libzedmd), fenêtre « LED virtuelles », enregistrement GIF."""

import ctypes
import os
import sys
import threading
import time

from .canvas import WIDTH, HEIGHT

FRAME_BYTES = WIDTH * HEIGHT * 3
_BRIGHT_TABLES = {}


def _apply_brightness(frame, k):
    if k >= 0.999:
        return frame
    key = round(k, 3)
    table = _BRIGHT_TABLES.get(key)
    if table is None:
        table = _BRIGHT_TABLES[key] = bytes(min(255, int(i * key)) for i in range(256))
    return frame.translate(table)


# --------------------------------------------------------------------------
# ZeDMD via libzedmd (zedmd64.dll / libzedmd.so)
# --------------------------------------------------------------------------

class ZeDMDOutput:
    """Envoie les images à un ZeDMD (USB ou WiFi) avec l'API C de libzedmd.

    La recherche de la dalle (scan des ports série) peut prendre quelques secondes :
    elle se fait dans un fil séparé pour ne jamais bloquer l'animation.
    """

    def __init__(self, cfg, root, log=print):
        self.cfg = cfg
        self.root = root
        self.log = log
        self.lib = None
        self.handle = None
        self.ok = False
        self.last = None
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.brightness = float(cfg.get("software_brightness", 1.0))
        if self._load():
            self.thread = threading.Thread(target=self._connect_loop, daemon=True)
            self.thread.start()

    def _load(self):
        name = self.cfg.get("dll") or ("libzedmd/zedmd64.dll" if sys.platform == "win32" else "libzedmd/libzedmd.so")
        path = name if os.path.isabs(name) else os.path.join(self.root, name)
        if not os.path.exists(path):
            self.log(f"ZeDMD : bibliothèque introuvable ({path}). Voir le guide, étape « libzedmd ».")
            return False
        try:
            if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
                self._dll_dir = os.add_dll_directory(os.path.dirname(os.path.abspath(path)))
            lib = ctypes.CDLL(path)
        except OSError as e:
            self.log(f"ZeDMD : chargement impossible de {path} : {e}")
            return False
        vp = ctypes.c_void_p
        lib.ZeDMD_GetInstance.restype = vp
        lib.ZeDMD_GetInstance.argtypes = []
        for fn, args, res in (
            ("ZeDMD_Open", [vp], ctypes.c_bool),
            ("ZeDMD_OpenWiFi", [vp, ctypes.c_char_p], ctypes.c_bool),
            ("ZeDMD_Close", [vp], None),
            ("ZeDMD_SetDevice", [vp, ctypes.c_char_p], None),
            ("ZeDMD_SetFrameSize", [vp, ctypes.c_uint16, ctypes.c_uint16], None),
            ("ZeDMD_SetBrightness", [vp, ctypes.c_uint8], None),
            ("ZeDMD_ClearScreen", [vp], None),
            ("ZeDMD_RenderRgb888", [vp, ctypes.POINTER(ctypes.c_uint8)], None),
            ("ZeDMD_GetFirmwareVersion", [vp], ctypes.c_char_p),
            ("ZeDMD_GetDevice", [vp], ctypes.c_char_p),
            ("ZeDMD_IgnoreDevice", [vp, ctypes.c_char_p], None),
        ):
            f = getattr(lib, fn, None)
            if f is None:
                self.log(f"ZeDMD : fonction absente de la bibliothèque : {fn}")
                return False
            f.argtypes = args
            f.restype = res
        self.lib = lib
        self.handle = lib.ZeDMD_GetInstance()
        return bool(self.handle)

    def _saved_device_path(self):
        return os.path.join(self.root, "runtime", "zedmd_device.txt")

    def _connect_loop(self):
        """Port configuré ou mémorisé : on réessaie ce seul port toutes les 10 s.
        Sinon : recherche sur tous les ports, limitée à 3 essais (pour ne pas
        déranger les autres périphériques série de la borne, pistolets par exemple)."""
        dev = (self.cfg.get("device") or "").strip()
        ip = (self.cfg.get("wifi_ip") or "").strip()
        saved = ""
        if not dev and not ip:
            try:
                with open(self._saved_device_path(), "r", encoding="utf-8") as f:
                    saved = f.read().strip()
            except OSError:
                saved = ""
        scans = 0
        warned = False
        while not self.stop.is_set() and not self.ok:
            if ip or dev:
                if self._open(device=dev, ip=ip, quiet=warned):
                    return
            elif saved:
                if self._open(device=saved, quiet=True):
                    return
                if not warned:
                    self.log(f"ZeDMD : pas de réponse sur {saved}, recherche sur tous les ports")
                saved = ""
                continue
            else:
                scans += 1
                if self._open(quiet=warned):
                    return
                if scans >= 3:
                    self.log("ZeDMD : dalle introuvable, recherche arrêtée. Indique le port dans config.json (\"device\": \"COM5\") ou relance ArcadeDMD.")
                    return
            warned = True
            self.stop.wait(10 if (ip or dev) else 10 * scans)

    def _open(self, device="", ip="", quiet=False):
        lib, h = self.lib, self.handle
        try:
            with self.lock:
                if ip:
                    ok = bool(lib.ZeDMD_OpenWiFi(h, ip.encode()))
                else:
                    if device:
                        lib.ZeDMD_SetDevice(h, device.encode())
                    else:
                        for ign in self.cfg.get("ignore_devices", []) or []:
                            lib.ZeDMD_IgnoreDevice(h, str(ign).encode())
                    ok = bool(lib.ZeDMD_Open(h))
                if ok:
                    lib.ZeDMD_SetFrameSize(h, WIDTH, HEIGHT)
                    b = self.cfg.get("brightness")
                    if isinstance(b, int) and 0 <= b <= 15:
                        lib.ZeDMD_SetBrightness(h, b)
                    fw = lib.ZeDMD_GetFirmwareVersion(h)
                    found = lib.ZeDMD_GetDevice(h)
        except OSError as e:
            self.log(f"ZeDMD : erreur à l'ouverture : {e}")
            return False
        if not ok:
            if not quiet:
                self.log("ZeDMD : dalle non trouvée" + (f" sur {device or ip}" if (device or ip) else "") + ", nouvel essai dans 10 s")
            return False
        found = found.decode(errors="replace") if found else ""
        if found and not ip:
            try:
                os.makedirs(os.path.dirname(self._saved_device_path()), exist_ok=True)
                with open(self._saved_device_path(), "w", encoding="utf-8") as f:
                    f.write(found)
            except OSError:
                pass
        self.last = None
        self.ok = True
        self.log(f"ZeDMD connecté {found} (firmware {fw.decode(errors='replace') if fw else '?'})")
        return True

    def send(self, frame):
        if not self.ok or frame == self.last:
            return
        self.last = frame
        data = _apply_brightness(frame, self.brightness)
        buf = (ctypes.c_uint8 * FRAME_BYTES).from_buffer_copy(data)
        try:
            with self.lock:
                self.lib.ZeDMD_RenderRgb888(self.handle, buf)
        except OSError as e:
            self.log(f"ZeDMD : envoi interrompu : {e}")

    def close(self):
        self.stop.set()
        if self.ok and self.lib:
            try:
                with self.lock:
                    self.lib.ZeDMD_ClearScreen(self.handle)
                    self.lib.ZeDMD_Close(self.handle)
            except OSError:
                pass
        self.ok = False


# --------------------------------------------------------------------------
# rendu « LED » (points ronds) commun à l'aperçu et au GIF
# --------------------------------------------------------------------------

def make_dot_mask(dx, dy=None, gap_ratio=0.18):
    """Masque L (niveaux de gris) d'une LED ronde dans une cellule de dx x dy pixels."""
    from PIL import Image, ImageDraw
    dy = dy or dx
    k = 8
    w, h = dx * k, dy * k
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    r = min(w, h) * (1 - gap_ratio) / 2
    cx, cy = w / 2, h / 2
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    return m.resize((dx, dy), Image.LANCZOS)


def make_square_mask(dx, dy=None):
    """Masque d'un pixel carré avec un fin espace autour (style « pixel » pour écran LCD)."""
    from PIL import Image, ImageDraw
    dy = dy or dx
    m = Image.new("L", (dx, dy), 0)
    gap = 1 if min(dx, dy) >= 4 else 0
    ImageDraw.Draw(m).rectangle((0, 0, dx - 1 - gap, dy - 1 - gap), fill=255)
    return m


def scale2x(frame, w, h):
    """Agrandit une image RGB par 2 en lissant les diagonales (algorithme Scale2x / EPX).
    Les lettres et les pentes gardent leur forme mais deviennent plus fines et plus rondes."""
    px = [frame[i:i + 3] for i in range(0, w * h * 3, 3)]
    out = bytearray(w * h * 12)
    w2 = w * 6
    for y in range(h):
        row = y * w
        up = row - w if y > 0 else row
        down = row + w if y < h - 1 else row
        for x in range(w):
            p = px[row + x]
            a = px[up + x]
            d = px[down + x]
            c = px[row + x - 1] if x > 0 else p
            b = px[row + x + 1] if x < w - 1 else p
            o = y * 2 * w2 + x * 6
            if c != b and a != d:
                out[o:o + 3] = a if c == a else p
                out[o + 3:o + 6] = b if a == b else p
                out[o + w2:o + w2 + 3] = c if d == c else p
                out[o + w2 + 3:o + w2 + 6] = d if b == d else p
            else:
                out[o:o + 6] = p + p
                out[o + w2:o + w2 + 6] = p + p
    return bytes(out)


class LedRenderer:
    """Rendu « dalle LED » : le masque de toute la dalle est calculé une seule fois."""

    def __init__(self, dot, unlit=(14, 14, 14), dot_y=None, w=WIDTH, h=HEIGHT, style="led"):
        from PIL import Image
        self.dx = dot
        self.dy = dot_y or dot
        self.w, self.h = w, h
        mask = make_square_mask(self.dx, self.dy) if style == "pixel" else make_dot_mask(self.dx, self.dy)
        tile = Image.new("L", (w * self.dx, h * self.dy))
        for y in range(h):
            for x in range(w):
                tile.paste(mask, (x * self.dx, y * self.dy))
        self.mask_rgb = Image.merge("RGB", (tile, tile, tile))
        self.unlit_img = Image.new("RGB", (w, h), tuple(unlit)) if unlit else None

    def render(self, frame):
        from PIL import Image, ImageChops
        img = Image.frombytes("RGB", (self.w, self.h), frame)
        if self.unlit_img is not None:
            img = ImageChops.lighter(img, self.unlit_img)
        big = img.resize((self.w * self.dx, self.h * self.dy), Image.NEAREST)
        return ImageChops.multiply(big, self.mask_rgb)


def hd_factor(cfg, width, height):
    """1, 2 ou 4 : finesse de l'affichage sur un écran (« hd » dans config.json, "auto" par défaut).
    En auto, on double tant que chaque LED garde au moins 6 pixels."""
    v = cfg.get("hd", "auto")
    if isinstance(v, (int, float)) and int(v) in (1, 2, 4):
        return int(v)
    for f in (4, 2):
        if min(width // (WIDTH * f), height // (HEIGHT * f)) >= 6:
            return f
    return 1


# --------------------------------------------------------------------------
# fenêtre d'aperçu / « LED virtuelles » (pygame, sinon tkinter)
# --------------------------------------------------------------------------

class PreviewOutput:
    """"mode": "always", la fenêtre reste affichée. "mode": "games", elle n'apparaît que pendant un jeu, au premier
    plan, et se cache ensuite : le frontal (marquee ou clear logos de BigBox...) garde l'écran le reste du temps.
    "takeover": "known" (jeux qui ont un fichier dans games) ou "all" (tous les jeux), comme pour la Pixelcade."""

    RELEASE_DELAY = 2.0     # fin de partie : se cache après ce délai (enchaîner deux jeux ne fait pas clignoter)
    CHECK_EVERY = 1.0       # pendant un jeu : vérifie chaque seconde que rien n'est passé devant

    def __init__(self, cfg, log=print):
        self.cfg = cfg
        self.log = log
        self.backend = None
        self.closed = False
        self.mode = str(cfg.get("mode") or "always").lower()
        self.takeover = str(cfg.get("takeover") or "known").lower()
        self.shown = True
        self.release_at = None
        self.next_check = 0.0
        self.hwnd = None
        self.pos = (int(cfg.get("x", 100)), int(cfg.get("y", 100)))
        self.watch = sys.platform == "win32" and (self.mode == "games" or bool(cfg.get("topmost", False)))
        self.width = int(cfg.get("width", 1024))
        self.height = int(cfg.get("height", 256))
        self.hd = hd_factor(cfg, self.width, self.height)      # écran assez grand : image deux fois plus fine
        gw, gh = WIDTH * self.hd, HEIGHT * self.hd
        dx = max(2, self.width // gw)
        dy = max(2, self.height // gh)
        if max(dx, dy) > 1.25 * min(dx, dy):     # garde des LED à peu près rondes
            dx = dy = min(dx, dy)
        style = "pixel" if str(cfg.get("style", "led")).lower() in ("pixel", "pixels", "lcd") else "led"
        self.renderer = LedRenderer(dx, tuple(cfg.get("unlit", [14, 14, 14])), dot_y=dy, w=gw, h=gh, style=style)
        self.brightness = float(cfg.get("brightness", 1.0))
        self._last_in = None
        self._last_out = None
        try:
            self._init_pygame()
        except Exception as e:
            self.log(f"aperçu pygame indisponible ({e}), essai tkinter")
            self._init_tk()
        if self.mode == "games":
            self._show(False, quiet=True)  # attend le premier jeu

    # -- pygame
    def _init_pygame(self):
        x, y = int(self.cfg.get("x", 100)), int(self.cfg.get("y", 100))
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"
        if self.cfg.get("borderless", False):
            os.environ["SDL_WINDOW_NO_ACTIVATION_WHEN_SHOWN"] = "1"
        # coordonnées en vrais pixels même si Windows applique une mise à l'échelle (125 %, 150 %...)
        os.environ.setdefault("SDL_WINDOWS_DPI_AWARENESS", "permonitorv2")
        import pygame
        pygame.display.init()
        flags = pygame.NOFRAME if self.cfg.get("borderless", False) else 0
        self.pg = pygame
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption("ArcadeDMD")
        self.screen.fill((0, 0, 0))
        self.backend = "pygame"
        if sys.platform == "win32":
            try:
                self.hwnd = pygame.display.get_wm_info()["window"]
            except Exception:
                self.hwnd = None
        if sys.platform == "win32" and (self.cfg.get("topmost", False) or self.cfg.get("borderless", False)):
            try:
                hwnd = pygame.display.get_wm_info()["window"]
                user32 = ctypes.windll.user32
                if self.cfg.get("borderless", False):
                    # WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW : ne prend pas le focus, pas de bouton dans la barre des tâches
                    ex = user32.GetWindowLongW(hwnd, -20)
                    user32.SetWindowLongW(hwnd, -20, ex | 0x08000000 | 0x00000080)
                after = -1 if self.cfg.get("topmost", False) else 0
                user32.SetWindowPos(hwnd, after, x, y, 0, 0, 0x0001 | 0x0010)
            except Exception:
                pass

    def _init_tk(self):
        import tkinter as tk
        self.tk = tk.Tk()
        self.tk.title("ArcadeDMD")
        x, y = int(self.cfg.get("x", 100)), int(self.cfg.get("y", 100))
        self.tk.geometry(f"{self.width}x{self.height}+{x}+{y}")
        if self.cfg.get("borderless", False):
            self.tk.overrideredirect(True)
        if self.cfg.get("topmost", False):
            self.tk.attributes("-topmost", True)
        self.tk.configure(bg="black")
        self.label = tk.Label(self.tk, bg="black", bd=0)
        self.label.pack(expand=True)
        self.tk.protocol("WM_DELETE_WINDOW", self._on_close)
        self.backend = "tk"

    def _on_close(self):
        self.closed = True

    # -- premier plan pendant les jeux
    def on_mode(self, mode, game_key, scene_key):
        """Appelé par le moteur à chaque changement d'écran (jeu lancé, retour à l'attente)."""
        if self.mode != "games" or self.closed or self.backend is None:
            return
        if mode == "game" and (self.takeover == "all" or bool(game_key)):
            self.release_at = None
            if not self.shown:
                self._show(True)
                self.log("écran LCD : ArcadeDMD passe au premier plan")
            else:
                self._raise()
        elif self.shown and self.release_at is None:
            self.release_at = time.monotonic() + self.RELEASE_DELAY

    def _user32(self):
        u = getattr(self, "_u32", None)
        if u is None:
            from ctypes import wintypes
            u = self._u32 = ctypes.WinDLL("user32")          # fonctions à part, types précis
            u.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
            u.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                       ctypes.c_int, ctypes.c_uint]
            u.WindowFromPoint.argtypes = [wintypes.POINT]
            u.WindowFromPoint.restype = wintypes.HWND
            u.GetAncestor.argtypes = [wintypes.HWND, ctypes.c_uint]
            u.GetAncestor.restype = wintypes.HWND
            u.IsWindowVisible.argtypes = [wintypes.HWND]
        return u

    def _show(self, on, quiet=False):
        self.shown = on
        if self.backend == "pygame" and self.hwnd and sys.platform == "win32":
            try:
                u = self._user32()
                if on:
                    u.ShowWindow(self.hwnd, 4)           # SW_SHOWNOACTIVATE : le jeu garde le clavier et les manettes
                    self._raise()
                else:
                    u.ShowWindow(self.hwnd, 0)           # SW_HIDE
                    if not quiet:
                        self.log("écran LCD : rendu au frontal")
            except Exception as e:
                self.log(f"écran LCD : {e}")
        elif self.backend == "tk":
            try:
                if on:
                    self.tk.deiconify()
                    self.tk.attributes("-topmost", True)
                    self.tk.lift()
                else:
                    self.tk.withdraw()
            except Exception:
                pass

    def _raise(self):
        """Au-dessus de toutes les fenêtres, même celles « toujours devant », sans prendre le focus."""
        if self.backend == "pygame" and self.hwnd and sys.platform == "win32":
            try:
                # HWND_TOPMOST, SWP_NOSIZE | SWP_NOMOVE | SWP_NOACTIVATE | SWP_SHOWWINDOW
                self._user32().SetWindowPos(self.hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0040)
            except Exception:
                pass
        elif self.backend == "tk":
            try:
                self.tk.attributes("-topmost", True)
                self.tk.lift()
            except Exception:
                pass

    def _covered(self):
        """Une autre fenêtre (marquee du frontal...) est-elle passée devant ? Vérifié à trois endroits."""
        if not (self.backend == "pygame" and self.hwnd and sys.platform == "win32"):
            return False
        try:
            from ctypes import wintypes
            u = self._user32()
            x, y = self.pos
            for fx in (0.25, 0.5, 0.75):
                h = u.WindowFromPoint(wintypes.POINT(int(x + self.width * fx), int(y + self.height // 2)))
                if not h:
                    continue
                root = u.GetAncestor(h, 2) or h          # GA_ROOT
                if int(root) != int(self.hwnd):
                    return True
        except Exception:
            return False
        return False

    def send(self, frame):
        if self.closed or self.backend is None:
            return
        now = time.monotonic()
        if self.release_at is not None and now >= self.release_at:
            self.release_at = None
            self._show(False)
        if not self.shown:                          # cachée : on garde juste la fenêtre en vie
            if self.backend == "pygame":
                for ev in self.pg.event.get():
                    if ev.type == self.pg.QUIT:
                        self.closed = True
            return
        if self.watch and now >= self.next_check:
            self.next_check = now + self.CHECK_EVERY
            if self._covered():
                self._raise()
        frame = _apply_brightness(frame, self.brightness)
        if self.hd > 1:
            if frame == self._last_in:
                frame = self._last_out           # image inchangée : pas de nouveau calcul
            else:
                self._last_in = frame
                big = scale2x(frame, WIDTH, HEIGHT)
                if self.hd == 4:
                    big = scale2x(big, WIDTH * 2, HEIGHT * 2)
                self._last_out = frame = big
        img = self.renderer.render(frame)
        if self.backend == "pygame":
            pg = self.pg
            for ev in pg.event.get():
                if ev.type == pg.QUIT or (ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE):
                    self.closed = True
            surf = pg.image.frombuffer(img.tobytes(), img.size, "RGB")
            ox = (self.width - img.size[0]) // 2
            oy = (self.height - img.size[1]) // 2
            self.screen.blit(surf, (ox, oy))
            pg.display.flip()
        else:
            from PIL import ImageTk
            self._photo = ImageTk.PhotoImage(img)
            self.label.configure(image=self._photo)
            self.tk.update_idletasks()
            self.tk.update()

    def close(self):
        try:
            if self.backend == "pygame":
                self.pg.display.quit()
            elif self.backend == "tk":
                self.tk.destroy()
        except Exception:
            pass
        self.backend = None


# --------------------------------------------------------------------------
# enregistrement GIF (pour tester ou partager une scène)
# --------------------------------------------------------------------------

class GifRecorder:
    def __init__(self, path, fps=25, dot=6, log=print):
        self.path = path
        self.fps = fps
        self.renderer = LedRenderer(dot)
        self.frames = []
        self.log = log
        self.interval = 1.0 / fps
        self.next_t = 0.0

    def send(self, frame, t=None):
        if t is not None:
            if t + 1e-6 < self.next_t:
                return
            self.next_t += self.interval
            if self.next_t < t:
                self.next_t = t + self.interval
        self.frames.append(self.renderer.render(frame))

    def close(self):
        if not self.frames:
            return
        from PIL import Image
        pal = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in self.frames]
        pal[0].save(self.path, save_all=True, append_images=pal[1:], duration=int(1000 / self.fps), loop=0, optimize=False)
        self.log(f"GIF écrit : {self.path} ({len(self.frames)} images)")


class NullOutput:
    def send(self, frame):
        pass

    def close(self):
        pass
