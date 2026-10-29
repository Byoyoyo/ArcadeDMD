"""Pixelcade LED: drives the panel directly through the serial port (IOIO protocol, as dmdext does).

The Pixelcade software (pixelweb.exe) must release the port: ArcadeDMD stops it through its API (/quit)
when a game starts, then restarts it when the game ends.

Pixelcade LED : pilotage direct de la dalle par le port série.

Le protocole (IOIO) est celui qu'utilisent dmdext et libdmdutil pour afficher le DMD de
Visual Pinball sur une Pixelcade. Comme pour Visual Pinball, le logiciel Pixelcade
(pixelweb.exe) doit lâcher le port pendant ce temps : ArcadeDMD l'arrête par son API
(/quit) au lancement d'un jeu, puis le relance quand le jeu se termine.
"""

import importlib.util
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

from .i18n import tr

WIDTH, HEIGHT = 128, 32
FRAME_BYTES = WIDTH * HEIGHT * 3

CMD_FRAME_V1 = 0x1F
CMD_ENABLE = 0x1E
CMD_ENABLE_V23 = 0x2E
CMD_INIT_V23 = 0xEF
CMD_RGB565 = 0x30
CMD_RGB888 = 0x40
FRAME_START = 0xFE
FRAME_END = 0xAA


# --------------------------------------------------------------------------
# conversion pour les cartes V1 : 3 plans de bits, deux lignes à la fois
# --------------------------------------------------------------------------

def _plane_tables():
    top, bot = [], []
    for k in range(3):
        t = bytearray(512)
        b = bytearray(512)
        for code in range(512):
            r, g, bl = (code >> 6) & 7, (code >> 3) & 7, code & 7
            t[code] = ((r >> k) & 1) << 5 | ((g >> k) & 1) << 4 | ((bl >> k) & 1) << 3
            b[code] = ((r >> k) & 1) << 2 | ((g >> k) & 1) << 1 | ((bl >> k) & 1)
        top.append(t)
        bot.append(b)
    return top, bot


_TOP, _BOT = _plane_tables()


def rgb888_to_v1_planes(frame, rbg=False):
    """RGB888 128x32 -> 3 x 2048 octets (format des cartes Pixelcade V1, 3 bits par couleur).

    Chaque octet regroupe un pixel de la moitié haute (ligne y) et celui de la moitié
    basse (ligne y + 16) ; le plan k contient le bit k des 3 bits de poids fort.
    """
    codes = [0] * (WIDTH * HEIGHT)        # codes 9 bits (r, g, b sur 3 bits)
    for i in range(WIDTH * HEIGHT):
        r = frame[3 * i] >> 5
        g = frame[3 * i + 1] >> 5
        b = frame[3 * i + 2] >> 5
        if rbg:
            g, b = b, g
        codes[i] = (r << 6) | (g << 3) | b
    half = WIDTH * (HEIGHT // 2)
    out = bytearray(3 * half)
    for k in range(3):
        t, bt = _TOP[k], _BOT[k]
        base = k * half
        for i in range(half):
            out[base + i] = t[codes[i]] | bt[codes[i + half]]
    return out


def gamma_table(gamma):
    """256 bytes for bytes.translate: the colors drawn for a screen made right for the LEDs, which light in proportion to
    the value (a dark gray would glow). None for 1.0. / Les couleurs pensées pour un écran remises à l'échelle des LED,
    qui éclairent en proportion de la valeur (un gris sombre brillerait)."""
    try:
        g = float(gamma)
    except (TypeError, ValueError):
        g = 2.2
    if g <= 0 or abs(g - 1.0) < 1e-3:
        return None
    return bytes(int(round(255 * (v / 255.0) ** g)) for v in range(256))


def swap_green_blue(frame):
    out = bytearray(frame)
    out[1::3] = frame[2::3]
    out[2::3] = frame[1::3]
    return bytes(out)


def framed(command, data):
    n = 1 + len(data)
    return bytes((FRAME_START, FRAME_START, n & 0xFF, (n >> 8) & 0xFF, command)) + bytes(data) + bytes((FRAME_END,))


# --------------------------------------------------------------------------
# la carte
# --------------------------------------------------------------------------

class PixelcadeDevice:
    def __init__(self, port, color_order="auto", log=print):
        self.port = port
        self.color_order = (color_order or "auto").lower()
        self.log = log
        self.ser = None
        self.v2 = False
        self.framing = False
        self.rbg = False
        self.firmware = ""
        self.size = (128, 32)
        self.last = None

    def open(self):
        import serial
        try:
            s = serial.Serial()
            s.port = self.port
            s.baudrate = 115200
            s.timeout = 0.6
            s.write_timeout = 2.0
            s.dtr = False
            s.rts = True
            s.open()
            time.sleep(0.1)
            s.dtr = True
            time.sleep(0.1)
            resp = s.read(29)
        except (serial.SerialException, OSError, ValueError) as e:
            self.log(tr(f"Pixelcade : ouverture de {self.port} impossible ({e})",
                        f"Pixelcade: cannot open {self.port} ({e})"))
            return False
        if len(resp) < 29 or resp[0] != 0 or resp[1:5] != b"IOIO":
            s.close()
            return False
        fw = resp[21:29]
        self.firmware = fw.decode("ascii", errors="replace").strip("\x00 ")
        version = 0
        if fw[0:1] == b"P" and fw[1] and fw[2] and fw[3]:
            if fw[2:3] == b"M":
                self.size = (64, 32)
            self.v2 = fw[3:4] == b"R"
            if fw[6] and fw[7] and chr(fw[6]).isdigit() and chr(fw[7]).isdigit():
                version = (fw[6] - 48) * 10 + (fw[7] - 48)
        self.framing = self.v2 and version >= 23
        if self.color_order == "rbg":
            self.rbg = True
        elif self.color_order == "rgb":
            self.rbg = False
        else:
            self.rbg = (not self.v2) and fw[4:5] == b"C"
        if self.size != (128, 32):
            self.log(tr(f"Pixelcade {self.size[0]}x{self.size[1]} non gérée (firmware {self.firmware})",
                        f"Pixelcade {self.size[0]}x{self.size[1]} not supported (firmware {self.firmware})"))
            s.close()
            return False
        self.ser = s
        cfg = (WIDTH // 32) & 0x0F | (1 << 4)
        if self.framing:
            self._write(bytes((CMD_INIT_V23,)))
            self._write(framed(CMD_ENABLE_V23, bytes((cfg,))))
        else:
            self._write(bytes((CMD_ENABLE, cfg)))
        self.log(tr(f"Pixelcade connectée sur {self.port} (firmware {self.firmware}, "
                    f"{'V2' if self.v2 else 'V1'}{', protocole encadré' if self.framing else ''}, "
                    f"couleurs {'RBG' if self.rbg else 'RGB'})",
                    f"Pixelcade connected on {self.port} (firmware {self.firmware}, "
                    f"{'V2' if self.v2 else 'V1'}{', framed protocol' if self.framing else ''}, "
                    f"colors {'RBG' if self.rbg else 'RGB'})"))
        return True

    def _write(self, data):
        self.ser.write(data)

    def send(self, frame):
        if self.ser is None or frame == self.last:
            return
        self.last = frame
        if self.v2:
            data = swap_green_blue(frame) if self.rbg else frame
            self._write(framed(CMD_RGB888, data) if self.framing else bytes((CMD_RGB888,)) + data)
        else:
            self._write(bytes((CMD_FRAME_V1,)) + rgb888_to_v1_planes(frame, self.rbg))

    def clear(self):
        if self.ser is None:
            return
        self.last = None
        try:
            self.send(bytes(FRAME_BYTES))
        except Exception:
            pass

    def close(self, frame=None):
        """frame : image laissée sur la dalle (le marquee du jeu en attendant pixelweb), sinon noir."""
        if self.ser is None:
            return
        try:
            if frame is not None and len(frame) == FRAME_BYTES:
                self.last = None
                self.send(frame)
            else:
                self.clear()
            try:
                self.ser.flush()
            except Exception:
                pass
            time.sleep(0.05)
            self.ser.reset_output_buffer()
            self.ser.dtr = False
            self.ser.rts = False
            time.sleep(0.1)
            self.ser.close()
        except Exception:
            pass
        self.ser = None


def list_ports():
    try:
        from serial.tools import list_ports as lp
    except ImportError:
        return []
    out = []
    for p in lp.comports():
        text = " ".join(str(x or "") for x in (p.description, p.manufacturer, p.product, p.hwid))
        likely = ("IOIO" in text.upper()) or ("PIXELCADE" in text.upper()) or (p.vid == 0x1B4F)
        out.append((p.device, text.strip(), likely))
    return out


# --------------------------------------------------------------------------
# pixelweb (logiciel Pixelcade) : trouver, arrêter, relancer
# --------------------------------------------------------------------------

def find_process(name):
    """[(pid, chemin_exe)] des processus Windows portant ce nom."""
    if sys.platform != "win32":
        return []
    import ctypes
    from ctypes import wintypes
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_void_p),
                    ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", ctypes.c_long),
                    ("dwFlags", wintypes.DWORD), ("szExeFile", ctypes.c_wchar * 260)]

    k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    k32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    k32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    k32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    k32.OpenProcess.restype = wintypes.HANDLE
    k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k32.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR,
                                               ctypes.POINTER(wintypes.DWORD)]
    k32.CloseHandle.argtypes = [wintypes.HANDLE]

    snap = k32.CreateToolhelp32Snapshot(0x2, 0)
    if not snap or snap == wintypes.HANDLE(-1).value:
        return []
    found = []
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        ok = k32.Process32FirstW(snap, ctypes.byref(entry))
        while ok:
            if entry.szExeFile.lower() == name.lower():
                pid = entry.th32ProcessID
                path = ""
                h = k32.OpenProcess(0x1000, False, pid)     # PROCESS_QUERY_LIMITED_INFORMATION
                if h:
                    buf = ctypes.create_unicode_buffer(1024)
                    size = wintypes.DWORD(1024)
                    if k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
                        path = buf.value
                    k32.CloseHandle(h)
                found.append((pid, path))
            ok = k32.Process32NextW(snap, ctypes.byref(entry))
    finally:
        k32.CloseHandle(snap)
    return found


def http_alive(url, timeout=0.5):
    """pixelweb répond-il (n'importe quelle réponse HTTP) ?"""
    try:
        with urllib.request.urlopen(url, timeout=timeout):
            return True
    except urllib.error.HTTPError:
        return True
    except Exception:
        return False


def marquee_path(art_dir, roms):
    """Marquee Pixelcade d'un jeu (dossier mame, romset puis parent), ou ""."""
    if not art_dir:
        return ""
    for rom in roms:
        for ext in (".gif", ".png", ".jpg"):
            p = os.path.join(art_dir, "mame", rom + ext)
            if os.path.exists(p):
                return p
    return ""


def marquee_frame(art_dir, roms, size=(128, 32)):
    """Image RGB 128 x 32 du marquee Pixelcade d'un jeu (première image d'un GIF), ou None."""
    path = marquee_path(art_dir, roms)
    if not path:
        return None
    try:
        from PIL import Image
        with Image.open(path) as im:
            im.seek(0)
            rgb = im.convert("RGB")
            if rgb.size != size:
                rgb = rgb.resize(size, Image.LANCZOS)
            return rgb.tobytes()
    except Exception:
        return None


def http_get(url, timeout=2.0):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read(2000)
    except Exception:
        return None, b""


def start_detached(exe):
    folder = os.path.dirname(exe) or None
    if sys.platform == "win32":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 7                       # SW_SHOWMINNOACTIVE : réduit, sans voler le focus
        flags = subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP
        subprocess.Popen([exe], cwd=folder, startupinfo=si, creationflags=flags, close_fds=True)
    else:
        subprocess.Popen([exe], cwd=folder, start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def guess_pixelcade_dir(root, cfg):
    """Dossier Pixelcade (artwork) : réglage, emplacement de pixelweb mémorisé, ou chemins courants."""
    d = (cfg.get("art_dir") or "").strip()
    if d and os.path.isdir(d):
        return d
    for p in (cfg.get("pixelweb_exe") or "", _read(os.path.join(root, "runtime", "pixelweb_path.txt"))):
        if p and os.path.isdir(os.path.dirname(p)):
            return os.path.dirname(p)
    for d in (r"C:\Pixelcade", r"D:\Pixelcade", r"C:\arcade\pixelcade", r"D:\arcade\pixelcade"):
        if os.path.isdir(os.path.join(d, "mame")):
            return d
    return ""


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


# --------------------------------------------------------------------------
# sortie ArcadeDMD : prend la main pendant les jeux, rend la main à pixelweb ensuite
# --------------------------------------------------------------------------

class PixelcadeOutput:
    RELEASE_DELAY = 0.0      # fin de partie : la dalle revient tout de suite à pixelweb et au frontal

    def __init__(self, cfg, root, log=print):
        self.cfg = cfg
        self.root = root
        self.log = log
        self.mode = (cfg.get("mode") or "games").lower()          # "games" ou "always"
        self.takeover = (cfg.get("takeover") or "known").lower()  # "known" ou "all"
        self.url = (cfg.get("pixelweb_url") or "http://127.0.0.1:8080").rstrip("/")
        self.dev = None
        self.lock = threading.Lock()
        self.want = self.mode == "always"
        self.release_at = None
        self.blocked_until = 0.0
        self.stopped_exe = None
        self.closing = False
        self.last_sent = 0.0
        self.failed = False
        self.min_interval = 1.0 / max(5.0, float(cfg.get("max_fps", 30)))
        self.gamma = gamma_table(cfg.get("gamma", 2.2))
        self.last_game = []          # jeu en cours (romset, parent) : son marquee revient après la partie
        self.art_dir = guess_pixelcade_dir(root, cfg)
        if importlib.util.find_spec("serial") is None:
            self.log(tr("Pixelcade : le module pyserial manque (py -m pip install pyserial)",
                        "Pixelcade: the pyserial module is missing (py -m pip install pyserial)"))
            self.want = False
            self.mode = "off"
            return
        self.wake = threading.Event()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    # appelé par le moteur à chaque changement d'écran
    def on_mode(self, mode, game_key, scene_key, rom="", parent=""):
        if self.mode == "off":
            return
        active = self.mode == "always" or (mode == "game" and (self.takeover == "all" or bool(game_key)))
        if active and mode == "game" and (rom or parent):
            self.last_game = list(dict.fromkeys(n for n in (rom, parent) if n))
        if active:
            self.release_at = None
            if not self.want:
                self.want = True
                self.wake.set()
        elif self.want and self.release_at is None:
            # petit délai : enchaîner deux jeux ne relance pas pixelweb pour rien
            self.release_at = time.time() + self.RELEASE_DELAY

    def panel_ready(self):
        """False while the panel is being taken over (pixelweb stopping, serial port opening): the game's logo
        waits for it. / Faux pendant la prise de la dalle : le logo du jeu attend qu'elle soit à nous."""
        if self.mode == "off" or not self.want:
            return True
        return self.dev is not None or self.failed or time.time() < self.blocked_until

    def send(self, frame):
        now = time.time()
        if self.release_at is not None and now >= self.release_at:
            self.release_at = None
            self.want = False
            self.wake.set()
        if self.dev is None or now - self.last_sent < self.min_interval:
            return
        with self.lock:
            dev = self.dev
            if dev is None:
                return
            try:
                dev.send(frame.translate(self.gamma) if self.gamma else frame)
                self.last_sent = now
            except Exception as e:
                self.log(tr(f"Pixelcade : envoi interrompu ({e})", f"Pixelcade: sending interrupted ({e})"))
                dev.close()
                self.dev = None
                self.blocked_until = now + 10

    def close(self):
        self.closing = True
        if self.mode == "off":
            return
        self.want = False
        self._release()

    # -- fil de travail : arrêter/relancer pixelweb et ouvrir/fermer le port sans bloquer l'animation
    def _worker(self):
        while not self.closing:
            self.wake.wait(0.5)
            self.wake.clear()
            if self.closing:
                return
            if self.want and self.dev is None and time.time() >= self.blocked_until:
                if self._acquire():
                    self.failed = False
                else:
                    self.failed = True
                    self.blocked_until = time.time() + 30
            elif not self.want and self.dev is not None:
                self._release()

    def _saved_exe_path(self):
        return os.path.join(self.root, "runtime", "pixelweb_path.txt")

    def _stop_pixelweb(self):
        procs = find_process("pixelweb.exe")
        status, _ = (None, b"") if procs else http_get(self.url + "/info", 1.0)
        if not procs and status is None:
            return True                      # pixelweb ne tourne pas
        exe = next((p for _, p in procs if p), "") or self.cfg.get("pixelweb_exe") or _read(self._saved_exe_path())
        if exe:
            try:
                os.makedirs(os.path.dirname(self._saved_exe_path()), exist_ok=True)
                with open(self._saved_exe_path(), "w", encoding="utf-8") as f:
                    f.write(exe)
            except OSError:
                pass
        self.log(tr("Pixelcade : arrêt de pixelweb le temps du jeu", "Pixelcade: stopping pixelweb while the game runs"))
        http_get(self.url + "/quit", 3.0)
        t_end = time.time() + 8
        while time.time() < t_end:
            if not find_process("pixelweb.exe") and http_get(self.url + "/info", 0.5)[0] is None:
                self.stopped_exe = exe or None
                time.sleep(0.5)
                return True
            time.sleep(0.3)
        self.log(tr("Pixelcade : pixelweb ne s'arrête pas, la dalle reste à pixelweb",
                    "Pixelcade: pixelweb does not stop, the panel stays with pixelweb"))
        return False

    def _ports(self):
        dev = (self.cfg.get("device") or "").strip()
        if dev:
            return [dev]
        return [p for p, _, likely in list_ports() if likely]

    def _acquire(self):
        if not self._stop_pixelweb():
            return False
        ports = self._ports()
        if not ports:
            self.log(tr("Pixelcade : port introuvable. Indique-le dans config.json (\"device\": \"COM4\"), "
                        "la liste s'obtient avec ports.bat",
                        "Pixelcade: port not found. Set it in config.json (\"device\": \"COM4\"), "
                        "ports.bat lists the ports"))
            self._restart_pixelweb()
            return False
        t_end = time.time() + 6
        while time.time() < t_end and self.want and not self.closing:
            for port in ports:
                d = PixelcadeDevice(port, self.cfg.get("color_order", "auto"), self.log)
                if d.open():
                    with self.lock:
                        self.dev = d
                    return True
            time.sleep(0.5)
        self.log(tr("Pixelcade : pas de réponse de la carte", "Pixelcade: no response from the board"))
        self._restart_pixelweb()
        return False

    def _release(self):
        if not self.art_dir:                  # chemin de pixelweb mémorisé au premier arrêt
            self.art_dir = guess_pixelcade_dir(self.root, self.cfg)
        with self.lock:
            d, self.dev = self.dev, None
            if d is not None:
                # le marquee du jeu qu'on quitte reste affiché le temps que pixelweb revienne
                d.close(marquee_frame(self.art_dir, self.last_game) if self.mode != "always" else None)
        if self._restart_pixelweb() and self.last_game and not self.closing:
            self._marquee_back()

    def _marquee_back(self):
        """pixelweb vient d'être relancé. Le frontal ne lui a rien envoyé pendant la partie, on lui
        demande le marquee du jeu qu'on vient de quitter (celui qui est sélectionné dans BigBox)."""
        t_end = time.time() + 15
        while not http_alive(self.url + "/info"):
            if self.want or self.closing or time.time() > t_end:
                return
            time.sleep(0.25)
        time.sleep(0.4)                       # pixelweb finit de démarrer
        if self.want or self.closing:
            return
        path = marquee_path(self.art_dir, self.last_game)
        # sans dossier d'images connu : le parent, qui a plus souvent son marquee qu'un clone
        rom = os.path.splitext(os.path.basename(path))[0] if path else self.last_game[-1]
        status, _ = http_get(f"{self.url}/arcade/stream/mame/{urllib.parse.quote(rom)}", 3.0)
        if status is not None:
            self.log(tr(f"Pixelcade : pixelweb réaffiche le marquee de {rom}",
                        f"Pixelcade: pixelweb shows the marquee of {rom} again"))

    def _restart_pixelweb(self):
        exe, self.stopped_exe = self.stopped_exe, None
        if not exe:
            return False
        if not os.path.exists(exe):
            self.log(tr(f"Pixelcade : impossible de relancer pixelweb ({exe} introuvable)",
                        f"Pixelcade: cannot restart pixelweb ({exe} not found)"))
            return False
        try:
            start_detached(exe)
            self.log(tr("Pixelcade : pixelweb relancé", "Pixelcade: pixelweb restarted"))
            return True
        except OSError as e:
            self.log(tr(f"Pixelcade : relance de pixelweb impossible ({e})", f"Pixelcade: cannot restart pixelweb ({e})"))
            return False
