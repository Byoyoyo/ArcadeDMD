"""Moteur ArcadeDMD : lit les événements du plugin MAME, choisit la scène, envoie les images."""

import errno
import json
import os
import queue
import random
import re
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from .canvas import Canvas, Font, parse_color
from .scene import Scene, Ctx, GameState
from .outputs import ZeDMDOutput, PreviewOutput, GifRecorder, NullOutput
from .pixelcade import PixelcadeOutput, guess_pixelcade_dir, list_ports

VERSION = "1.2.2"

DEFAULT_CONFIG = {
    "fps": 50,
    "events_file": "runtime/events.jsonl",
    "heartbeat_timeout": 8,
    "show_pause": True,
    "idle": {"text": "INSERT COIN"},
    "outputs": {
        "zedmd": {"enabled": False, "dll": "", "device": "", "wifi_ip": "", "brightness": None,
                  "software_brightness": 1.0},
        "preview": {"enabled": True, "x": 100, "y": 100, "width": 1024, "height": 256,
                    "borderless": False, "topmost": False, "brightness": 1.0},
        "pixelcade": {"enabled": False, "device": "", "color_order": "auto", "mode": "games",
                      "takeover": "known", "max_fps": 30, "pixelweb_url": "http://127.0.0.1:8080",
                      "pixelweb_exe": "", "art_dir": ""},
    },
    "doflinx_bridge": {"enabled": False, "host": "127.0.0.1", "port": 8081},
}


def deep_merge(base, extra):
    out = dict(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


class Logger:
    def __init__(self, path=None, echo=True):
        self.path = path
        self.echo = echo

    def __call__(self, msg):
        line = time.strftime("%H:%M:%S ") + str(msg)
        if self.echo:
            try:
                print(line, flush=True)
            except Exception:
                pass
        if self.path:
            try:
                with open(self.path, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            except OSError:
                pass


def clean_title(desc):
    if not desc:
        return ""
    s = re.sub(r"\s*[\(\[].*?[\)\]]", "", desc)
    s = s.replace(" / ", " - ")
    return s.strip()


# --------------------------------------------------------------------------
# bibliothèque des jeux (games/*.json), rechargée à chaud
# --------------------------------------------------------------------------

class GameLibrary:
    def __init__(self, root, log):
        self.root = root
        self.dir = os.path.join(root, "games")
        self.log = log
        self.games = {}
        self.mtimes = {}
        self.next_check = 0.0
        self.reload(force=True)

    def _scan(self):
        out = {}
        if os.path.isdir(self.dir):
            for name in os.listdir(self.dir):
                if name.lower().endswith(".json"):
                    p = os.path.join(self.dir, name)
                    try:
                        out[name[:-5]] = os.path.getmtime(p)
                    except OSError:
                        pass
        return out

    def reload(self, force=False):
        now = time.time()
        if not force and now < self.next_check:
            return False
        self.next_check = now + 2.0
        mt = self._scan()
        if not force and mt == self.mtimes:
            return False
        games = {}
        for key in mt:
            p = os.path.join(self.dir, key + ".json")
            try:
                with open(p, "r", encoding="utf-8") as f:
                    games[key] = json.load(f)
            except (OSError, ValueError) as e:
                self.log(f"games/{key}.json illisible : {e}")
        changed = [k for k in mt if self.mtimes.get(k) != mt[k]]
        self.games = games
        self.mtimes = mt
        if not force:
            self.log("configuration rechargée : " + ", ".join(changed))
        return True

    def get(self, key):
        return self.games.get(key)

    def match(self, meta):
        system = meta.get("system")
        parent = meta.get("parent")
        hay = "||".join(
            "|".join(str(m.get(k) or "").lower() for k in ("file", "longname", "parent"))
            for m in meta.get("media") or [])

        def rule_ok(r):
            if not isinstance(r, dict):
                return False
            if "system" in r and system not in r["system"] and parent not in r["system"]:
                return False
            if "software" in r and not any(p.lower() in hay for p in r["software"]):
                return False
            if any(p.lower() in hay for p in r.get("software_not", [])):
                return False
            return "system" in r or "software" in r

        for key, g in self.games.items():
            if key.startswith("_"):
                continue
            m = g.get("match")
            rules = m if isinstance(m, list) else [m]
            if any(rule_ok(r) for r in rules):
                return key
        return None


# --------------------------------------------------------------------------
# lecture des événements écrits par le plugin MAME
# --------------------------------------------------------------------------

class EventTail:
    def __init__(self, path, log, skip_stale=10.0):
        self.path = path
        self.log = log
        self.pos = 0
        self.buf = b""
        try:
            st = os.stat(path)
            if time.time() - st.st_mtime > skip_stale:
                self.pos = st.st_size   # ancienne session : on l'ignore
        except OSError:
            pass

    def poll(self):
        try:
            size = os.path.getsize(self.path)
        except OSError:
            return []
        if size < self.pos:
            self.pos = 0
            self.buf = b""
        if size == self.pos:
            return []
        try:
            with open(self.path, "rb") as f:
                f.seek(self.pos)
                data = f.read()
                self.pos = f.tell()
        except OSError:
            return []
        self.buf += data
        lines = self.buf.split(b"\n")
        self.buf = lines.pop()
        out = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line.decode("utf-8", errors="replace")))
            except ValueError:
                self.log("événement illisible ignoré")
        return out


# --------------------------------------------------------------------------
# passerelle DOFLinx : imite l'API HTTP de DOF2DMD
# --------------------------------------------------------------------------

class Dof2DmdBridge:
    def __init__(self, host, port, q, log):
        self.q = q
        self.log = log
        bridge = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                u = urlparse(self.path)
                qs = {k: v[-1] for k, v in parse_qs(u.query).items()}
                path = u.path.rstrip("/").lower()
                body = "OK"
                if path.endswith("/v1/version"):
                    body = "ArcadeDMD " + VERSION
                else:
                    bridge.q.put(("http", path, qs))
                data = body.encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self.server = ThreadingHTTPServer((host, port), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        log(f"passerelle DOFLinx active sur http://{host}:{port}")

    def close(self):
        try:
            self.server.shutdown()
        except Exception:
            pass


# --------------------------------------------------------------------------
# simulation (mode démo, sans MAME)
# --------------------------------------------------------------------------

class Simulator:
    def __init__(self, game_key, game, state, rng=None):
        self.rng = rng or random.Random(3)
        self.state = state
        self.names = list(((game or {}).get("memory") or {}).get("values", {}).keys()) or ["score", "credits"]
        demo = (game or {}).get("demo", {})
        self.values = {n: demo.get(n, self._initial(n)) for n in self.names}
        self.next = {}
        for n in self.names:
            ln = n.lower()
            if any(k in ln for k in ("score", "point", "ring", "anneau", "credit", "live", "vie", "record", "hi")):
                state.update(n, self.values[n], 0.0, quiet=True)
                self.next[n] = 1.0 if ("score" in ln or "ring" in ln or "anneau" in ln) else 9.0
            else:
                self.next[n] = float("inf")

    def _initial(self, n):
        n = n.lower()
        if "record" in n or "hi" in n:
            return 7000000
        if "credit" in n:
            return 2
        if "live" in n or "vie" in n:
            return 3
        if "score" in n or "point" in n:
            return 0
        if "ring" in n or "anneau" in n:
            return 0
        return 0

    def step(self, t):
        for n in self.names:
            if t < self.next[n]:
                continue
            ln = n.lower()
            v = self.values[n]
            if "score" in ln or "point" in ln:
                v += self.rng.choice([10, 30, 30, 50, 100, 200, 300, 1000])
                self.next[n] = t + self.rng.uniform(0.25, 1.4)
            elif "ring" in ln or "anneau" in ln:
                v = 0 if self.rng.random() < 0.06 else v + self.rng.choice([1, 1, 1, 2, 10])
                self.next[n] = t + self.rng.uniform(0.3, 1.2)
            elif "credit" in ln:
                v = v + 1 if v < 9 else 1
                self.next[n] = t + 9.0
            elif "live" in ln or "vie" in ln:
                v = 3 if v <= 1 else v - 1
                self.next[n] = t + 11.0
            elif "record" in ln or "hi" in ln:
                score = max([self.values[k] for k in self.names if "score" in k.lower()] or [0])
                v = max(v, score)
                self.next[n] = t + 1.0
            else:
                self.next[n] = t + 5.0
                continue
            self.values[n] = v
            self.state.update(n, v, t)


# --------------------------------------------------------------------------
# moteur
# --------------------------------------------------------------------------

class Engine:
    def __init__(self, root, config, outputs, log, demo_game=None):
        self.root = root
        self.cfg = config
        self.outputs = outputs
        self.log = log
        self.canvas = Canvas()
        self.ctx = Ctx(self.canvas, root, log)
        self.state = GameState()
        self.ctx.state = self.state
        self.library = GameLibrary(root, log)
        self.scene = None
        self.scene_key = None
        self.mode = "idle"
        self.last_event = 0.0
        self.overlay = None           # (texte, fin, couleur)
        self.q = queue.Queue()
        self.bridge = None
        self.sim = None
        self.source = None
        self.last_start = None
        self.pixelcade_dir = guess_pixelcade_dir(root, config.get("outputs", {}).get("pixelcade", {}))
        ev = os.path.join(root, config.get("events_file", "runtime/events.jsonl"))
        self.tail = EventTail(ev, log) if not demo_game else None
        br = config.get("doflinx_bridge", {})
        if br.get("enabled") and not demo_game:
            try:
                self.bridge = Dof2DmdBridge(br.get("host", "127.0.0.1"), int(br.get("port", 8080)), self.q, log)
            except OSError as e:
                log(f"passerelle DOFLinx impossible sur le port {br.get('port')} : {e}")
        self.go_idle()
        if demo_game:
            self.start_demo(demo_game)

    # -- scènes
    def _scene_spec(self, key):
        g = self.library.get(key) or {}
        return g.get("scene")

    def set_scene(self, key):
        spec = self._scene_spec(key)
        if spec is None:
            key = "_generic"
            spec = self._scene_spec(key) or {"layers": [{"type": "marquee", "text": "{title}", "font": "7x14", "y": 11, "upper": True}]}
        self.scene = Scene(spec, self.root, self.log, mapping=self.state.mapping())
        self.scene_key = key
        self._notify_outputs()

    def _notify_outputs(self):
        for out in self.outputs:
            fn = getattr(out, "on_mode", None)
            if fn is not None:
                try:
                    fn(self.mode if self.mode else "idle", self.state.meta.get("game") or "", self.scene_key)
                except Exception as e:
                    self.log(f"sortie {out.__class__.__name__} : {e}")

    def go_idle(self):
        self.mode = "idle"
        self.source = None
        idle = self.cfg.get("idle", {})
        self.state.reset({"title": idle.get("text", "INSERT COIN"), "idle_text": idle.get("text", "INSERT COIN")})
        self.set_scene("_idle")

    def start_game(self, meta, source):
        key = meta.get("game") or ""
        if not key or key not in self.library.games:
            key = self.library.match(meta) or ""
        g = self.library.get(key) or {}
        title = g.get("title") or clean_title(meta.get("description")) or meta.get("system", "")
        meta = dict(meta)
        meta["title"] = title
        meta["game"] = key
        if self.pixelcade_dir:
            meta["pixelcade"] = self.pixelcade_dir
        self.state.reset(meta)
        self.mode = "game"
        self.source = source
        self.set_scene(key if key else "_generic")
        self.log(f"jeu : {meta.get('system')} « {title} » -> scène {self.scene_key}")

    def start_demo(self, key):
        g = self.library.get(key)
        if g is None and key not in ("_idle", "_generic"):
            self.log(f"jeu inconnu : {key} (fichiers disponibles : {', '.join(sorted(self.library.games))})")
        if key == "_idle":
            return
        self.start_game({"game": key, "system": key, "description": (g or {}).get("title", key)}, "demo")
        self.sim = Simulator(key, g, self.state)

    def message(self, text, seconds=2.0, color="#ffffff"):
        self.overlay = (text, time.monotonic() + seconds, parse_color(color))

    # -- événements
    def handle_event(self, ev, now):
        t = ev.get("t")
        self.last_event = time.monotonic()
        if t == "start":
            self.last_start = dict(ev)
            self.start_game(ev, "plugin")
        elif t in ("v", "hb"):
            if self.mode != "game":
                # reprise après un silence (menu MAME ouvert longtemps, moteur relancé en cours de partie)
                self.start_game(self.last_start or {"system": "?", "description": ""}, "plugin")
            for k, v in (ev.get("v") or {}).items():
                self.state.update(k, v, now, quiet=(t == "hb"))
        elif t == "stop":
            self.go_idle()
        elif t == "pause":
            self.state.paused = True
        elif t == "resume":
            self.state.paused = False
        elif t == "capture":
            self.message(f"CAPTURE {ev.get('n', '')}", 1.5, "#ffdd33")

    def handle_http(self, path, qs, now):
        def num(name):
            try:
                return int(float(qs.get(name, "")))
            except ValueError:
                return None
        if path.endswith("/display/score") or path.endswith("/display/scorev2"):
            if self.mode != "game":
                self.start_game({"system": "doflinx", "description": ""}, "doflinx")
            player = num("player") or num("activeplayer") or 1
            score = num("score")
            if score is not None:
                self.state.update("score", score, now)
                self.state.update(f"score_p{player}", score, now)
            for name in ("players", "credits"):
                v = num(name)
                if v is not None:
                    self.state.update(name, v, now)
            self.state.update("player", player, now)
        elif path.endswith("/display/picture"):
            p = qs.get("path", "")
            m = re.match(r"mame/([^/&?]+)$", p)
            if m and m.group(1).lower() != "doflinx" and self.source != "plugin":
                self.start_game({"system": m.group(1), "description": m.group(1).upper()}, "doflinx")
        elif path.endswith("/display/text") or path.endswith("/display/advanced"):
            text = qs.get("text", "").replace("|", " ")
            if text:
                try:
                    dur = float(qs.get("duration", "2"))
                except ValueError:
                    dur = 2.0
                self.message(text.upper(), max(1.0, min(dur if dur > 0 else 2.0, 6.0)), "#" + qs.get("color", "ffffff")[:6])
        elif path.endswith("/blank") or path.endswith("/exit"):
            if self.source == "doflinx":
                self.go_idle()

    # -- dessin
    def draw_overlay(self):
        if not self.overlay:
            return
        text, end, color = self.overlay
        if time.monotonic() > end:
            self.overlay = None
            return
        cv = self.canvas
        font = Font.get("6x10")
        w = font.width(text)
        if w > cv.w - 4:
            font = Font.get("5x8")
            w = font.width(text)
        x = max(1, (cv.w - w) // 2)
        cv.fill_rect(x - 2, 9, min(cv.w, w + 4), 13, (0, 0, 0))
        cv.hline(x - 2, x + w + 1, 9, scale(color, 0.5))
        cv.hline(x - 2, x + w + 1, 21, scale(color, 0.5))
        cv.text(font, text, x, 12, color)

    def render(self, now):
        self.ctx.t = now
        self.scene.render(self.ctx)
        if self.state.paused and self.cfg.get("show_pause", True) and int(now * 2) % 2 == 0:
            cv = self.canvas
            f = Font.get("5x8")
            cv.fill_rect(cv.w - 27, 0, 27, 8, (0, 0, 0))
            cv.text(f, "PAUSE", cv.w - 26, 1, (255, 255, 255))
        self.draw_overlay()
        self.state.events.clear()
        return self.canvas.to_bytes()

    # -- boucle principale
    def step(self, now):
        if self.library.reload():
            if self.scene_key:
                self.set_scene(self.scene_key)
        if self.tail:
            for ev in self.tail.poll():
                self.handle_event(ev, now)
        while True:
            try:
                item = self.q.get_nowait()
            except queue.Empty:
                break
            if item[0] == "http":
                self.handle_http(item[1], item[2], now)
        if self.sim:
            self.sim.step(now)
        if (self.mode == "game" and self.source == "plugin"
                and time.monotonic() - self.last_event > float(self.cfg.get("heartbeat_timeout", 8))):
            self.log("plus de nouvelles de MAME : retour à l'écran d'attente")
            self.go_idle()
        return self.render(now)

    def run(self, seconds=None):
        fps = float(self.cfg.get("fps", 50))
        period = 1.0 / fps
        t0 = time.monotonic()
        nxt = t0
        try:
            while True:
                now = time.monotonic() - t0
                frame = self.step(now)
                for out in self.outputs:
                    if isinstance(out, GifRecorder):
                        out.send(frame, now)
                    else:
                        out.send(frame)
                if any(getattr(o, "closed", False) for o in self.outputs):
                    break
                if seconds is not None and now >= seconds:
                    break
                nxt += period
                delay = nxt - time.monotonic()
                if delay > 0:
                    time.sleep(delay)
                else:
                    nxt = time.monotonic()
        except KeyboardInterrupt:
            pass
        finally:
            for out in self.outputs:
                try:
                    out.close()
                except Exception as e:
                    self.log(f"fermeture sortie : {e}")
            if self.bridge:
                self.bridge.close()


def scale(c, k):
    return (int(c[0] * k), int(c[1] * k), int(c[2] * k))


# --------------------------------------------------------------------------
# utilitaires de lancement
# --------------------------------------------------------------------------

def load_config(root, log):
    path = os.path.join(root, "config.json")
    cfg = DEFAULT_CONFIG
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                cfg = deep_merge(DEFAULT_CONFIG, json.load(f))
        except (OSError, ValueError) as e:
            log(f"config.json illisible ({e}), valeurs par défaut utilisées")
    return cfg


def single_instance(port=47811):
    """Verrou « une seule instance ». Retourne un objet à garder, None si déjà lancé.

    Windows : mutex nommé (aucun port réseau, insensible aux plages réservées par Hyper-V).
    Ailleurs : port local ; seule l'erreur « adresse déjà utilisée » signifie « déjà lancé ».
    """
    if sys.platform == "win32":
        import ctypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateMutexW.restype = ctypes.c_void_p
        k32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
        h = k32.CreateMutexW(None, False, "Local\\ArcadeDMD_engine")
        if h and ctypes.get_last_error() == 183:   # ERROR_ALREADY_EXISTS
            k32.CloseHandle(ctypes.c_void_p(h))
            return None
        return h or True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
        s.listen(1)
        return s
    except OSError as e:
        if e.errno in (errno.EADDRINUSE, 10048):
            return None
        return True


def engine_running():
    """Vrai si le moteur tourne déjà (lancement automatique par exemple)."""
    if sys.platform == "win32":
        import ctypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.OpenMutexW.restype = ctypes.c_void_p
        k32.OpenMutexW.argtypes = [ctypes.c_uint32, ctypes.c_bool, ctypes.c_wchar_p]
        h = k32.OpenMutexW(0x00100000, False, "Local\\ArcadeDMD_engine")   # SYNCHRONIZE
        if h:
            k32.CloseHandle(ctypes.c_void_p(h))
            return True
        return False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", 47811))
        return False
    except OSError as e:
        return e.errno in (errno.EADDRINUSE, 10048)
    finally:
        s.close()


def pixelcade_ports(pc_cfg):
    """Port(s) de la Pixelcade : celui de config.json, sinon ceux qui y ressemblent."""
    dev = (pc_cfg.get("device") or "").strip()
    if dev:
        return [dev]
    return [p for p, _, likely in list_ports() if likely]


def build_outputs(root, cfg, log, preview=True, zedmd=True, gif=None, gif_seconds=None):
    outs = []
    o = cfg.get("outputs", {})
    if zedmd and o.get("zedmd", {}).get("enabled"):
        zcfg = dict(o["zedmd"])
        pc_cfg = o.get("pixelcade", {})
        if pc_cfg.get("enabled") and not (zcfg.get("device") or zcfg.get("wifi_ip")):
            # la recherche du ZeDMD ne doit jamais toucher au port de la Pixelcade
            ignore = list(zcfg.get("ignore_devices") or [])
            for p in pixelcade_ports(pc_cfg):
                if p not in ignore:
                    ignore.append(p)
            zcfg["ignore_devices"] = ignore
        outs.append(ZeDMDOutput(zcfg, root, log))
    if preview and o.get("preview", {}).get("enabled"):
        try:
            outs.append(PreviewOutput(o["preview"], log))
        except Exception as e:
            log(f"aperçu impossible : {e}")
    if zedmd and o.get("pixelcade", {}).get("enabled"):
        outs.append(PixelcadeOutput(o["pixelcade"], root, log))
    if gif:
        outs.append(GifRecorder(gif, log=log))
    if not outs:
        outs.append(NullOutput())
    return outs
