"""Sorties : dalle ZeDMD (libzedmd), fenêtre « LED virtuelles », enregistrement GIF."""

import ctypes
import os
import sys
import threading

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


class LedRenderer:
    """Rendu « dalle LED » : le masque de toute la dalle est calculé une seule fois."""

    def __init__(self, dot, unlit=(14, 14, 14), dot_y=None):
        from PIL import Image
        self.dx = dot
        self.dy = dot_y or dot
        mask = make_dot_mask(self.dx, self.dy)
        tile = Image.new("L", (WIDTH * self.dx, HEIGHT * self.dy))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                tile.paste(mask, (x * self.dx, y * self.dy))
        self.mask_rgb = Image.merge("RGB", (tile, tile, tile))
        self.unlit_img = Image.new("RGB", (WIDTH, HEIGHT), tuple(unlit)) if unlit else None

    def render(self, frame):
        from PIL import Image, ImageChops
        img = Image.frombytes("RGB", (WIDTH, HEIGHT), frame)
        if self.unlit_img is not None:
            img = ImageChops.lighter(img, self.unlit_img)
        big = img.resize((WIDTH * self.dx, HEIGHT * self.dy), Image.NEAREST)
        return ImageChops.multiply(big, self.mask_rgb)


# --------------------------------------------------------------------------
# fenêtre d'aperçu / « LED virtuelles » (pygame, sinon tkinter)
# --------------------------------------------------------------------------

class PreviewOutput:
    def __init__(self, cfg, log=print):
        self.cfg = cfg
        self.log = log
        self.backend = None
        self.closed = False
        self.width = int(cfg.get("width", 1024))
        self.height = int(cfg.get("height", 256))
        dx = max(2, self.width // WIDTH)
        dy = max(2, self.height // HEIGHT)
        if max(dx, dy) > 1.25 * min(dx, dy):     # garde des LED à peu près rondes
            dx = dy = min(dx, dy)
        self.renderer = LedRenderer(dx, tuple(cfg.get("unlit", [14, 14, 14])), dot_y=dy)
        self.brightness = float(cfg.get("brightness", 1.0))
        try:
            self._init_pygame()
        except Exception as e:
            self.log(f"aperçu pygame indisponible ({e}), essai tkinter")
            self._init_tk()

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

    def send(self, frame):
        if self.closed or self.backend is None:
            return
        frame = _apply_brightness(frame, self.brightness)
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
