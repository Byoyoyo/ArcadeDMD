"""The window of ArcadeDMD (1.37): a page it serves itself on 127.0.0.1, opened as an app window (Microsoft Edge in app
mode, else the default browser), with the icon near the clock (dmd/tray.py) in place of the console.

The page reads /api/state, /api/log and the marquee and LED panel as they are now (/api/frame/hd.jpg, led.png, made by
the engine only while a page looks at them). What it changes goes through POST requests that carry the token written in
the page, so another site open in the browser cannot drive ArcadeDMD.

La fenêtre d'ArcadeDMD : une page qu'il sert lui-même sur 127.0.0.1, ouverte en fenêtre d'application (Edge en mode
application, sinon le navigateur), avec l'icône près de l'horloge à la place de la console. Ce qu'elle change passe par
des requêtes POST avec le jeton écrit dans la page, pour qu'un autre site ouvert dans le navigateur ne puisse pas
piloter ArcadeDMD.
"""

import io
import json
import os
import secrets
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .i18n import lang, tr

PORT = 47812
STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui")
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".ico": "image/x-icon", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2"}
FRAME_EVERY = 0.4                 # the marquee and the LED panel, while a page looks / tant qu'une page regarde


def port_file(root):
    return os.path.join(root, "runtime", "gui_port.txt")


def running_url(root):
    """The address of the window of an ArcadeDMD already running, or None. / L'adresse de celle qui tourne déjà."""
    try:
        with open(port_file(root), "r", encoding="utf-8") as f:
            port = int(f.read().strip())
    except (OSError, ValueError):
        return None
    return f"http://127.0.0.1:{port}/"


def _edge():
    """msedge.exe, or Chrome, for a window without the browser's bars. / Edge, ou Chrome, en fenêtre d'application."""
    if sys.platform != "win32":
        return None
    env = os.environ
    for base in (env.get("ProgramFiles(x86)"), env.get("ProgramFiles"), env.get("LOCALAPPDATA")):
        if not base:
            continue
        for rel in (r"Microsoft\Edge\Application\msedge.exe", r"Google\Chrome\Application\chrome.exe"):
            p = os.path.join(base, rel)
            if os.path.isfile(p):
                return p
    return None


def focus_window():
    """The window of ArcadeDMD already open (Edge or Chrome, titled ArcadeDMD) to the front. / Celle déjà ouverte
    passe devant."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        from ctypes import wintypes as w
        u = ctypes.WinDLL("user32")
        found = []
        PROC = ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)

        def each(hwnd, _):
            if not u.IsWindowVisible(hwnd):
                return True
            cls = ctypes.create_unicode_buffer(64)
            u.GetClassNameW(hwnd, cls, 64)
            if cls.value != "Chrome_WidgetWin_1":
                return True
            title = ctypes.create_unicode_buffer(256)
            u.GetWindowTextW(hwnd, title, 256)
            if title.value.startswith("ArcadeDMD"):
                found.append(hwnd)
                return False
            return True

        u.EnumWindows.argtypes = [PROC, w.LPARAM]
        u.IsWindowVisible.argtypes = [w.HWND]
        u.GetClassNameW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
        u.GetWindowTextW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
        u.IsIconic.argtypes = [w.HWND]
        u.ShowWindow.argtypes = [w.HWND, ctypes.c_int]
        u.SetForegroundWindow.argtypes = [w.HWND]
        u.EnumWindows(PROC(each), 0)
        if not found:
            return False
        if u.IsIconic(found[0]):
            u.ShowWindow(found[0], 9)                   # SW_RESTORE
        u.SetForegroundWindow(found[0])
        return True
    except Exception:
        return False


def open_window(url, log=None):
    """The page as an app window of its own. / La page en fenêtre à elle."""
    exe = _edge()
    if exe:
        try:
            flags = 0x00000008 | 0x00000200 if sys.platform == "win32" else 0     # DETACHED_PROCESS, NEW_PROCESS_GROUP
            subprocess.Popen([exe, f"--app={url}", "--window-size=1180,820"], creationflags=flags, close_fds=True)
            return True
        except OSError as e:
            if log:
                log(tr(f"fenêtre : Edge ne s'ouvre pas ({e}), le navigateur à la place",
                       f"window: Edge does not open ({e}), the browser instead"))
    try:
        return webbrowser.open(url)
    except Exception:
        return False


# ---------------------------------------------------------------- start with Windows / lancer avec Windows
def startup_file():
    base = os.environ.get("APPDATA")
    if not base:
        return None
    return os.path.join(base, "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "ArcadeDMD.bat")


def autostart_on():
    p = startup_file()
    return bool(p and os.path.isfile(p))


def set_autostart(root, on):
    """The same .bat as install.bat writes in the Startup folder. / Le même .bat qu'install.bat."""
    p = startup_file()
    if not p:
        return False
    if not on:
        try:
            os.remove(p)
        except OSError:
            pass
        return not os.path.exists(p)
    exe = sys.executable
    if exe.lower().endswith("python.exe"):
        w = exe[:-len("python.exe")] + "pythonw.exe"
        if os.path.isfile(w):
            exe = w
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="mbcs" if sys.platform == "win32" else "utf-8") as f:
            f.write("@echo off\r\n")
            f.write(f'cd /d "{root}"\r\n')
            f.write(f'start "" "{exe}" "{os.path.join(root, "arcadedmd.py")}"\r\n')
        return True
    except OSError:
        return False


def open_path(path):
    """A folder or a file in Windows' own program. / Un dossier ou un fichier dans le programme de Windows."""
    try:
        if sys.platform == "win32":
            os.startfile(path)                          # noqa: S606 (the user's own folder)
        else:
            subprocess.Popen(["xdg-open", path])
        return True
    except Exception:
        return False


def _retroarch_running():
    """Is retroarch.exe running (Windows, from the list of processes, nothing started)? None when it cannot be told.
    RetroArch tourne-t-il (liste des processus, rien n'est lancé) ? None si on ne peut pas savoir."""
    if sys.platform != "win32":
        return None
    try:
        import ctypes
        from ctypes import wintypes as w

        class ENTRY(ctypes.Structure):
            _fields_ = [("dwSize", w.DWORD), ("cntUsage", w.DWORD), ("th32ProcessID", w.DWORD),
                        ("th32DefaultHeapID", ctypes.c_size_t), ("th32ModuleID", w.DWORD), ("cntThreads", w.DWORD),
                        ("th32ParentProcessID", w.DWORD), ("pcPriClassBase", w.LONG), ("dwFlags", w.DWORD),
                        ("szExeFile", w.WCHAR * 260)]

        k = ctypes.WinDLL("kernel32", use_last_error=True)
        k.CreateToolhelp32Snapshot.argtypes = [w.DWORD, w.DWORD]
        k.CreateToolhelp32Snapshot.restype = w.HANDLE
        k.Process32FirstW.argtypes = [w.HANDLE, ctypes.POINTER(ENTRY)]
        k.Process32NextW.argtypes = [w.HANDLE, ctypes.POINTER(ENTRY)]
        k.CloseHandle.argtypes = [w.HANDLE]
        snap = k.CreateToolhelp32Snapshot(0x2, 0)                 # TH32CS_SNAPPROCESS
        if not snap or snap == w.HANDLE(-1).value:
            return None
        try:
            e = ENTRY()
            e.dwSize = ctypes.sizeof(ENTRY)
            ok = k.Process32FirstW(snap, ctypes.byref(e))
            while ok:
                if e.szExeFile.lower() == "retroarch.exe":
                    return True
                ok = k.Process32NextW(snap, ctypes.byref(e))
            return False
        finally:
            k.CloseHandle(snap)
    except Exception:
        return None


class _Server(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass                                            # a page closed in the middle of an answer / page fermée


class ControlPanel:
    """The page's server, alive across the engine's restarts. main() gives it each new engine. / Le serveur de la
    page, vivant d'un redémarrage du moteur à l'autre."""

    def __init__(self, root, log, version, port=PORT):
        self.root, self.log, self.version = root, log, version
        self.engine = None
        self.token = secrets.token_hex(16)
        self.started = time.time()
        self.frames = {}
        self.want_until = 0.0
        self.next_frame = 0.0
        self.alerts = []                                # [(time, level, text)]
        self.notify = None                              # the icon's balloon, set by main / la bulle de l'icône
        self.actions = {}                               # "quit", "restart" -> callables set by main
        self.extra = {}                                 # GET/POST routes of the other tabs / des autres onglets
        self.silent_since = None
        self.silent_told = False
        self.last_seen = -1e9                           # when a page last asked for the state / la dernière page
        self.goto = [0, ""]                             # a tab the page should show / un onglet à montrer
        self.on_tip = None                              # the icon's tooltip / l'info-bulle de l'icône
        self.server = None
        for p in range(port, port + 10):
            try:
                self.server = _Server(("127.0.0.1", p), self._handler())
                self.port = p
                break
            except OSError:
                continue
        if self.server is None:
            raise OSError("no free port for the window")
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, name="window", daemon=True).start()
        threading.Thread(target=self._watch, name="window-watch", daemon=True).start()
        try:
            os.makedirs(os.path.join(root, "runtime"), exist_ok=True)
            with open(port_file(root), "w", encoding="utf-8") as f:
                f.write(str(self.port))
        except OSError:
            pass
        self.url = f"http://127.0.0.1:{self.port}/"
        log(tr(f"fenêtre d'ArcadeDMD sur {self.url}", f"ArcadeDMD's window on {self.url}"))

    def close(self):
        try:
            self.server.shutdown()
        except Exception:
            pass
        try:
            os.remove(port_file(self.root))
        except OSError:
            pass

    def open(self, tab=""):
        """The window already open comes to the front (on the tab asked), else a new one. / La fenêtre déjà ouverte
        passe devant (sur l'onglet demandé), sinon une nouvelle."""
        if tab:
            self.goto = [self.goto[0] + 1, tab]
        if time.monotonic() - self.last_seen < 3.0 and focus_window():
            return True
        return open_window(self.url + (f"#{tab}" if tab else ""), self.log)

    def alert(self, level, text):
        """Shown on the page, and in a balloon by the icon. / Montrée sur la page et dans une bulle de l'icône."""
        self.alerts = (self.alerts + [(time.time(), level, text)])[-20:]
        if self.notify is not None:
            try:
                self.notify("ArcadeDMD", text, level)
            except Exception:
                pass

    def on_stall(self, name, stuck):
        if stuck:
            self.alert("warn", tr(f"{name} s'est arrêté. Le détail est dans le journal.",
                                  f"{name} stopped. The details are in the log."))

    # ------------------------------------------------------------ what the engine gives / ce que donne le moteur
    def tick(self, eng, frame):
        """Each image of the engine: the marquee and the LED panel as images, while a page looks at them. / À chaque
        image du moteur : le marquee et la dalle en images, tant qu'une page les regarde."""
        now = time.monotonic()
        if now > self.want_until or now < self.next_frame:
            return
        self.next_frame = now + FRAME_EVERY
        from PIL import Image
        for o in eng.outputs:
            if o.__class__.__name__ == "PreviewOutput" and getattr(o, "backend", None) == "pygame":
                pg = o.pg
                w, h = o.screen.get_size()
                small = pg.transform.smoothscale(o.screen, (960, max(1, int(960 * h / max(1, w)))))
                raw = (getattr(pg.image, "tobytes", None) or pg.image.tostring)(small, "RGB")
                img = Image.frombytes("RGB", small.get_size(), raw)
                buf = io.BytesIO()
                img.save(buf, "JPEG", quality=82)
                self.frames["hd.jpg"] = buf.getvalue()
                break
        if frame is not None:
            if not hasattr(self, "_led"):
                from .outputs import LedRenderer
                self._led = LedRenderer(4)
            img = self._led.render(frame)
            buf = io.BytesIO()
            img.save(buf, "PNG", optimize=False)
            self.frames["led.png"] = buf.getvalue()

    def tip(self):
        eng = self.engine
        if eng is not None and eng.mode == "game" and getattr(eng, "game_title", ""):
            return f"ArcadeDMD {self.version}\n" + tr(f"{eng.game_title} en cours", f"{eng.game_title} running")
        return f"ArcadeDMD {self.version}"

    def _watch(self):
        """The icon's tooltip, and RetroArch running without answering its network commands, told once (1.37).
        L'info-bulle de l'icône, et RetroArch qui tourne sans répondre, dit une fois."""
        turn = 0
        while True:
            time.sleep(2.0)
            turn += 1
            if self.on_tip is not None:
                try:
                    self.on_tip(self.tip())
                except Exception:
                    pass
            if turn % 5:
                continue
            try:
                eng = self.engine
                ra = getattr(eng, "retroarch", None) if eng is not None else None
                if ra is None:
                    continue
                last = getattr(ra, "last_answer", None)
                if last is not None and time.time() - last < 15:
                    self.silent_since, self.silent_told = None, False
                    continue
                if not _retroarch_running():
                    self.silent_since, self.silent_told = None, False
                    continue
                if self.silent_since is None:
                    self.silent_since = time.time()
                elif time.time() - self.silent_since > 30 and not self.silent_told:
                    self.silent_told = True
                    self.log(tr("RetroArch tourne mais ne répond pas à ses commandes réseau (port 55355)",
                                "RetroArch runs but does not answer its network commands (port 55355)"))
                    self.alert("warn", tr("RetroArch tourne mais ne répond pas. Le marquee ne peut pas suivre le jeu.",
                                          "RetroArch runs but does not answer. The marquee cannot follow the game."))
            except Exception:
                pass

    # ------------------------------------------------------------ the state / l'état
    def state(self):
        eng = self.engine
        now = time.time()
        out = {"version": self.version, "lang": lang(), "up": now - self.started, "mode": "starting", "game": None,
               "credits": None, "retroarch": None, "outputs": [], "alerts": [], "stall": [], "silent": False,
               "autostart": autostart_on(), "windows": sys.platform == "win32"}
        out["alerts"] = [{"t": t, "level": lv, "text": tx} for t, lv, tx in self.alerts if now - t < 600][-5:]
        dog = getattr(self, "watchdog", None)
        if dog is not None:
            out["stall"] = sorted(dog.stuck)
        out["silent"] = bool(self.silent_told)
        out["goto"] = self.goto
        if eng is None:
            return out
        out["mode"] = eng.mode
        out["since"] = now - getattr(eng, "started_at", now)
        ls = eng.last_start or {}
        if eng.mode == "game":
            src = eng.source or ""
            demo = src == "demo"
            out["game"] = {"title": getattr(eng, "game_title", "") or ls.get("description") or ls.get("system") or "",
                           "key": getattr(eng, "game_key", ""), "rom": "" if demo else (ls.get("system") or ""),
                           "source": src, "core": "" if demo else (ls.get("core") or ""),
                           "values": 0 if demo else len(ls.get("values") or [])}
        vals = getattr(eng.state, "values", {}) or {}
        c = vals.get("credits")
        out["credits"] = c if isinstance(c, (int, float)) and not isinstance(c, bool) else None
        ra = eng.retroarch
        if ra is not None:
            last = getattr(ra, "last_answer", None)
            out["retroarch"] = {"seen": bool(getattr(ra, "seen", False)), "version": getattr(ra, "version", "") or "",
                                "age": (now - last) if last else None, "playing": bool(getattr(ra, "session", None)),
                                "port": getattr(getattr(ra, "client", None), "addr", ("", 55355))[1]}
        out["mame"] = {"playing": eng.mode == "game" and eng.source == "plugin"}
        for o in eng.outputs:
            name = o.__class__.__name__
            if name == "PreviewOutput":
                hd = getattr(o, "hd_view", None) is not None
                out["outputs"].append({"kind": "marquee" if hd else "window", "x": o.pos[0], "y": o.pos[1],
                                       "w": o.width, "h": o.height, "shown": bool(getattr(o, "shown", True))})
            elif name == "PixelcadeOutput":
                dev = getattr(o, "dev", None)
                out["outputs"].append({"kind": "pixelcade", "ok": dev is not None, "port": getattr(dev, "port", "") or ""})
            elif name == "ZeDMDOutput":
                out["outputs"].append({"kind": "zedmd", "ok": bool(getattr(o, "ok", False))})
        return out

    def log_lines(self, after):
        lines = list(getattr(self.log, "recent", []))
        return {"lines": [{"n": n, "text": t} for n, t in lines if n > after][-800:],
                "file": os.path.join(self.root, "runtime", "arcadedmd.log")}

    # ------------------------------------------------------------ the server / le serveur
    def _handler(self):
        panel = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *a):
                pass

            def _send(self, code, body, ctype="application/json; charset=utf-8", cache=False):
                if isinstance(body, (dict, list)):
                    body = json.dumps(body, ensure_ascii=False).encode("utf-8")
                elif isinstance(body, str):
                    body = body.encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "max-age=60" if cache else "no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                self.wfile.write(body)

            def _local(self):
                host = (self.headers.get("Host") or "").split(":")[0]
                return host in ("127.0.0.1", "localhost")

            def do_GET(self):
                if not self._local():
                    return self._send(403, {"error": "host"})
                u = urlparse(self.path)
                path = u.path
                qs = {k: v[-1] for k, v in parse_qs(u.query).items()}
                try:
                    if path in ("/", "/index.html"):
                        with open(os.path.join(STATIC, "index.html"), "r", encoding="utf-8") as f:
                            page = f.read().replace("__TOKEN__", panel.token).replace("__VERSION__", panel.version)
                        return self._send(200, page, TYPES[".html"])
                    if path == "/api/state":
                        panel.last_seen = time.monotonic()
                        return self._send(200, panel.state())
                    if path == "/api/log":
                        return self._send(200, panel.log_lines(int(qs.get("after", "0") or 0)))
                    if path.startswith("/api/frame/"):
                        panel.want_until = time.monotonic() + 3.0
                        name = path.rsplit("/", 1)[-1]
                        data = panel.frames.get(name)
                        if data is None:                    # not drawn yet / pas encore dessinée
                            return self._send(204, b"", "text/plain")
                        return self._send(200, data, "image/jpeg" if name.endswith(".jpg") else "image/png")
                    route = panel.extra.get(("GET", path))
                    if route is not None:
                        return self._send(200, route(qs))
                    name = os.path.basename(path)
                    full = os.path.join(STATIC, name)
                    ext = os.path.splitext(name)[1].lower()
                    if name and ext in TYPES and os.path.isfile(full):
                        with open(full, "rb") as f:
                            return self._send(200, f.read(), TYPES[ext], cache=True)
                    return self._send(404, {"error": "not found"})
                except Exception as e:                              # the page never takes the engine down
                    return self._send(500, {"error": repr(e)})

            def do_POST(self):
                try:                                    # the body read first, the connection stays clean / lu d'abord
                    n = int(self.headers.get("Content-Length") or 0)
                    raw = self.rfile.read(n) if 0 < n <= 1 << 20 else b""
                except (ValueError, OSError):
                    self.close_connection = True
                    return self._send(400, {"error": "length"})
                if n > 1 << 20:
                    self.close_connection = True
                    return self._send(413, {"error": "size"})
                if not self._local() or self.headers.get("X-ArcadeDMD-Token") != panel.token:
                    return self._send(403, {"error": "token"})
                try:
                    data = json.loads(raw or b"{}")
                except ValueError:
                    return self._send(400, {"error": "json"})
                if not isinstance(data, dict):
                    return self._send(400, {"error": "json"})
                path = urlparse(self.path).path
                try:
                    if path == "/api/action":
                        return self._send(200, panel.action(data))
                    route = panel.extra.get(("POST", path))
                    if route is not None:
                        return self._send(200, route(data))
                    return self._send(404, {"error": "not found"})
                except Exception as e:
                    return self._send(500, {"error": repr(e)})

        return Handler

    def action(self, data):
        what = str(data.get("do") or "")
        if what in ("quit", "restart"):
            fn = self.actions.get(what)
            if fn is not None:
                threading.Timer(0.3, fn).start()                    # the answer leaves first / la réponse part avant
                return {"ok": True}
            return {"ok": False}
        if what == "autostart":
            ok = set_autostart(self.root, bool(data.get("on")))
            return {"ok": ok, "on": autostart_on()}
        if what == "open_log":
            return {"ok": open_path(os.path.join(self.root, "runtime", "arcadedmd.log"))}
        if what == "open_folder":
            sub = str(data.get("folder") or "")
            target = os.path.join(self.root, "runtime", "captures") if sub == "captures" else self.root
            os.makedirs(target, exist_ok=True)
            return {"ok": open_path(target)}
        return {"ok": False, "error": "unknown"}
