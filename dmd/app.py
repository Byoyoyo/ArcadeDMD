"""ArcadeDMD engine: reads the events of the MAME plugin (and of RetroArch and DOFLinx),
picks the scene and sends each frame to the outputs. Also loads config.json.

Moteur ArcadeDMD : lit les événements du plugin MAME, choisit la scène, envoie les images."""

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
from .scene import Scene, Ctx, GameState, LogoIntro
from .outputs import ZeDMDOutput, PreviewOutput, GifRecorder, NullOutput
from .pixelcade import PixelcadeOutput, guess_pixelcade_dir, list_ports
from .retroarch import RetroArchSource
from .memvalues import derive, game_values
from .coinbuttons import CoinButtons, mvs_rates, side_word
from .neocoins import NeoCoins
from .textfiles import TextFiles
from .i18n import tr

VERSION = "1.30.0"

DEFAULT_CONFIG = {
    "language": "auto",
    "fps": 50,
    "events_file": "runtime/events.jsonl",
    "heartbeat_timeout": 8,
    "show_pause": True,
    "idle": {"text": "INSERT COIN", "show": False},
    "outputs": {
        "zedmd": {"enabled": False, "dll": "", "device": "", "wifi_ip": "", "brightness": None,
                  "software_brightness": 1.0},
        "preview": {"enabled": True, "x": 100, "y": 100, "width": 1024, "height": 256,
                    "borderless": False, "topmost": False, "brightness": 1.0},
        "pixelcade": {"enabled": False, "device": "", "color_order": "auto", "mode": "games",
                      "takeover": "known", "max_fps": 30, "gamma": 2.2, "pixelweb_url": "http://127.0.0.1:8080",
                      "pixelweb_exe": "", "art_dir": ""},
    },
    "doflinx_bridge": {"enabled": False, "host": "127.0.0.1", "port": 8081},
    "textfiles": {"enabled": True, "folder": "obs", "history": True},
    "retroarch": {"enabled": True, "host": "127.0.0.1", "port": 55355, "poll_ms": 100},
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
                self.log(tr(f"games/{key}.json illisible : {e}", f"games/{key}.json unreadable: {e}"))
        changed = [k for k in mt if self.mtimes.get(k) != mt[k]]
        self.games = games
        self.mtimes = mt
        if not force:
            self.log(tr("configuration rechargée : ", "configuration reloaded: ") + ", ".join(changed))
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

        # d'abord les fichiers propres à un jeu, puis les modèles ("fallback", par exemple neogeo.json)
        for fallback in (False, True):
            for key, g in self.games.items():
                if key.startswith("_") or bool(g.get("fallback")) != fallback:
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
                self.log(tr("événement illisible ignoré", "unreadable event ignored"))
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
        log(tr(f"passerelle DOFLinx active sur http://{host}:{port}", f"DOFLinx bridge active on http://{host}:{port}"))

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
        if (game or {}).get("activity") and "p1_mode" not in self.names:   # who plays is guessed (Capcom): shown in the demo too
            self.names += ["p1_mode", "p2_mode"] + ([] if "credits" in self.names else ["credits"])
        demo = (game or {}).get("demo", {})
        self.values = {n: demo.get(n, self._initial(n)) for n in self.names}
        self.next = {}
        # jeux de combat : des coups au hasard, KO, puis nouveau round
        self.fighters = [n for n in ("health", "health_p2") if n in self.names]
        specs = ((game or {}).get("memory") or {}).get("values") or {}
        self.gauges = {n for n in ("power", "power_p2") if isinstance(specs.get(n), dict) and specs[n].get("max") == 100}
        self.fight_next = 1.0
        self.ko_until = None
        self.kos = 0
        # stage backdrops of the HD screen: a new stage every two K.O., like a new team in King of Fighters
        self.backdrops = len(((game or {}).get("hd") or {}).get("stages") or []) or 8
        if "mission" in self.names and not self.values.get("mission"):
            self.values["mission"] = 1
        # fighting games: first the attract screen (INSERT COIN, two coins, PRESS START), then the fight
        # jeux de combat : d'abord l'écran d'attente (deux pièces, PRESS START), puis le combat ("attract": false sans)
        self.t0 = None
        self.attract = None
        self.hidden = ()
        # values of a game of their own ("demo": {"sim": {...}}): they take turns, count or move at random
        # valeurs propres à un jeu : elles défilent, comptent ou bougent au hasard ("demo": {"sim": {...}})
        self.sim = {n: s for n, s in (demo.get("sim") or {}).items() if n in self.names and isinstance(s, dict)}
        self.sim_next = {n: float(s.get("start", 1.0)) for n, s in self.sim.items()}
        self.sim_index = {n: 0 for n in self.sim}
        fighting = len(self.fighters) == 2
        if demo.get("attract", fighting) and "p1_mode" in self.names:
            self.attract = [(4.0, {"credits": 1}), (6.0, {"credits": 2}), (11.0, {"p1_mode": 1, "credits": 1})]
            self.values["p1_mode"] = 0
            if "p2_mode" in self.values:
                self.values["p2_mode"] = 0
            if "credits" in self.values:
                self.values["credits"] = 0
            self.hidden = tuple(n for n in ("health", "health_p2", "time") if n in self.values)   # pas encore de combat
        for n in self.names:
            ln = n.lower()
            if n not in self.hidden:
                state.update(n, self.values[n], 0.0, quiet=True)
            if "score" in ln or "point" in ln or "ring" in ln or "anneau" in ln or "record" in ln:
                self.next[n] = 1.0
            elif "credit" in ln or "live" in ln or "vie" in ln:
                self.next[n] = 9.0
            elif "bomb" in ln:
                self.next[n] = 4.0
            elif "weapon" in ln or "arme" in ln:
                self.next[n] = 5.0
            elif "ammo" in ln or "munition" in ln:
                self.next[n] = 0.4
            elif "time" in ln or "chrono" in ln:
                self.next[n] = 1.0
            elif n == "mission":
                self.next[n] = 25.0
            elif n in self.gauges:
                self.next[n] = 1.5
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

    def _set(self, n, v, t):
        self.values[n] = v
        self.state.update(n, v, t)

    def _fight(self, t):
        if len(self.fighters) < 2 or t < self.fight_next:
            return
        if self.ko_until is not None:
            if t >= self.ko_until:                      # nouveau round
                self.kos += 1
                if self.kos % 2 == 0:                   # new stage: round number and backdrop change
                    if "stage" in self.values:
                        self._set("stage", (self.values["stage"] + 1) % 6, t)
                    if "backdrop" in self.values:
                        b = self.values["backdrop"]
                        self._set("backdrop", self.rng.choice([i for i in range(self.backdrops) if i != b] or [b]), t)
                for n in self.fighters:
                    self._set(n, 100, t)
                if "time" in self.values:
                    self._set("time", 60, t)
                self.ko_until = None
            self.fight_next = t + 0.5
            return
        n = self.rng.choice(self.fighters)
        v = max(0, self.values[n] - self.rng.choice([4, 6, 8, 12, 18]))
        self._set(n, v, t)
        if v <= 0:
            self.ko_until = t + 2.5
        self.fight_next = t + self.rng.uniform(0.6, 2.2)

    def _attract(self, t):
        """Écran d'attente du jeu de combat : True tant que la partie n'a pas commencé."""
        lt = t - self.t0
        while self.attract and lt >= self.attract[0][0]:
            for n, v in self.attract.pop(0)[1].items():
                if n in self.values:
                    self._set(n, v, t)
        if self.attract:
            return True
        self.attract = None
        for n in self.hidden:                      # la partie commence : barres pleines, chrono
            self._set(n, self.values[n], t)
        self.hidden = ()
        self.fight_next = t + 1.0
        for n in self.names:                       # les valeurs bougent à partir de maintenant
            self.next[n] = t + self.next[n]
        for n in self.sim:
            self.sim_next[n] = t + self.sim_next[n]
        return False

    def _sim_step(self, t):
        """Valeurs propres au jeu : "cycle" (une liste, à tour de rôle), "count" (min, max, pas), "random" (min, max).
        "every" : secondes entre deux changements (ou [min, max])."""
        for n, s in self.sim.items():
            if t < self.sim_next[n]:
                continue
            ev = s.get("every", 3.0)
            self.sim_next[n] = t + (self.rng.uniform(*ev) if isinstance(ev, list) and len(ev) == 2 else float(ev))
            v = self.values.get(n)
            if isinstance(s.get("cycle"), list) and s["cycle"]:
                i = self.sim_index[n] = (self.sim_index[n] + 1) % len(s["cycle"])
                v = s["cycle"][i]
            elif isinstance(s.get("count"), list) and len(s["count"]) >= 2:
                lo, hi = s["count"][0], s["count"][1]
                step = s["count"][2] if len(s["count"]) > 2 else 1
                v = (v if isinstance(v, (int, float)) else lo) + step
                if (step > 0 and v > hi) or (step < 0 and v < lo):
                    v = lo if step > 0 else hi
            elif isinstance(s.get("random"), list) and len(s["random"]) == 2:
                v = self.rng.randint(int(s["random"][0]), int(s["random"][1]))
            else:
                continue
            self._set(n, v, t)

    def step(self, t):
        if self.t0 is None:
            self.t0 = t
        if self.attract is not None and self._attract(t):
            return
        self._fight(t)
        if self.sim:
            self._sim_step(t)
        for n in self.names:
            if t < self.next[n] or n in self.sim:
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
            elif "bomb" in ln:
                v = 10 if v <= 0 else v - 1
                self.next[n] = t + self.rng.uniform(2.5, 6.0)
            elif "weapon" in ln or "arme" in ln:
                order = [4, 3, 2, 1, 0]
                v = order[(order.index(v) + 1) % len(order)] if v in order else 4
                for k in self.names:                    # the ammo of the same player, unless the game drives it itself
                    if ("ammo" in k.lower() or "munition" in k.lower()) and k not in self.sim and k.endswith("_p2") == n.endswith("_p2"):
                        self.values[k] = {4: 200, 3: 30, 2: 30, 1: 30}.get(v, 0)
                        self.state.update(k, self.values[k], t)
                self.next[n] = t + 7.0
            elif "ammo" in ln or "munition" in ln:
                self.next[n] = t + self.rng.uniform(0.15, 0.6)
                if v <= 0:
                    continue
                v = max(0, v - self.rng.choice([1, 1, 2, 3]))
            elif "time" in ln or "chrono" in ln:
                v = 60 if v <= 0 else v - 1
                self.next[n] = t + 1.0
            elif n in self.gauges:                     # super gauge in %: it fills up, then the super is used
                v = 0 if v >= 100 else min(100, v + self.rng.choice([8, 12, 16, 25]))
                self.next[n] = t + (2.5 if v >= 100 else self.rng.uniform(0.8, 2.0))
            elif n == "mission":                       # Metal Slug: next mission, then back to the first one
                v = v + 1 if v < 6 else 1
                self.next[n] = t + 25.0
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
        self.ctx.cfg = config
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
        tf = config.get("textfiles") or {}
        self.texts = TextFiles(tf, root, log) if tf.get("enabled") and not demo_game else None
        # config.json modifié (screen_setup.bat, réglage à la main) : le moteur redémarre avec les nouveaux réglages
        self.cfg_path = os.path.join(root, "config.json")
        self.cfg_mtime = _mtime(self.cfg_path)
        self.next_cfg_check = 0.0
        self.restart = False
        for out in outputs:            # l'affichage HD du LCD lit directement l'état du jeu
            attach = getattr(out, "attach", None)
            if attach is not None:
                attach(self)
        # game logo at the start of a game (LaunchBox Clear Logo), on the panel and on the HD screen
        # logo du jeu au lancement (Clear Logo de LaunchBox), sur la dalle et sur l'écran HD
        self.intro_cfg = config.get("intro") if isinstance(config.get("intro"), dict) else {}
        self.intro = None             # LogoIntro en cours sur la dalle
        self.intro_wait = None        # jeu lancé : on attend l'index LaunchBox et la dalle (Pixelcade qui se libère)
        self.intro_serial = 0         # +1 à chaque lancement : l'écran HD joue aussi son intro
        self.logos = None
        if self.intro_cfg.get("logo", True):
            for out in outputs:
                hv = getattr(out, "hd_view", None)
                if hv is not None and getattr(hv, "logos", None) is not None:
                    self.logos = hv.logos          # même index que l'écran HD
                    break
            if self.logos is None:
                from .launchbox import LogoFinder
                pv = (config.get("outputs") or {}).get("preview") or {}
                lb = self.intro_cfg.get("launchbox") or pv.get("launchbox") or ""
                self.logos = LogoFinder(root, {"launchbox": lb}, log, label=("logo au lancement", "logo at launch"))
        self.sim = None
        self.demo_until = None
        self.source = None
        self.last_start = None
        self.retroarch = None
        self.derived = None
        self.coin_guess = None        # crédits d'une Neo Geo devinés d'après le BIOS (RetroArch)
        self.activity = None          # who plays, guessed from the values that move (CPS) / qui joue, d'après ce qui bouge
        self.active_at = -1e9
        # the coin buttons read on the controllers (coin_buttons.bat) / les boutons des pièces lus sur les manettes
        self.coin_buttons = CoinButtons.from_config(config, log) if not demo_game else None
        self.hold_zero = {}           # score qui passe à 0 un instant (combattant recréé entre deux rounds)
        self.zero_since = {}
        self.demo_request = os.path.join(root, "runtime", "demo_request.json")
        self.next_request_check = 0.0
        self.pixelcade_dir = guess_pixelcade_dir(root, config.get("outputs", {}).get("pixelcade", {}))
        ev = os.path.join(root, config.get("events_file", "runtime/events.jsonl"))
        self.tail = EventTail(ev, log) if not demo_game else None
        br = config.get("doflinx_bridge", {})
        if br.get("enabled") and not demo_game:
            try:
                self.bridge = Dof2DmdBridge(br.get("host", "127.0.0.1"), int(br.get("port", 8080)), self.q, log)
            except OSError as e:
                log(tr(f"passerelle DOFLinx impossible sur le port {br.get('port')} : {e}",
                       f"DOFLinx bridge unavailable on port {br.get('port')}: {e}"))
        ra = config.get("retroarch", {})
        if ra.get("enabled", True) and not demo_game:
            try:
                self.retroarch = RetroArchSource(self.library, self.q, ra, log)
            except OSError as e:
                log(tr(f"RetroArch : surveillance impossible ({e})", f"RetroArch: cannot watch for games ({e})"))
        self.go_idle()
        if demo_game:
            self.start_demo(demo_game)

    # -- scènes
    def _scene_spec(self, key):
        if key == "_idle" and not (self.cfg.get("idle") or {}).get("show", False):
            return {"layers": []}      # hors jeu : dalle noire ("idle": {"show": true} remet l'heure et INSERT COIN)
        g = self.library.get(key) or {}
        if g.get("scene") is None and g.get("scene_from"):
            return (self.library.get(g["scene_from"]) or {}).get("scene")     # jeu appris : scène de son modèle
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
                    args = (self.mode if self.mode else "idle", self.state.meta.get("game") or "", self.scene_key)
                    try:     # romset et parent : la Pixelcade réaffiche le marquee du jeu après la partie
                        fn(*args, rom=self.state.meta.get("system") or "", parent=self.state.meta.get("parent") or "")
                    except TypeError:
                        fn(*args)
                except Exception as e:
                    self.log(tr(f"sortie {out.__class__.__name__} : {e}", f"output {out.__class__.__name__}: {e}"))

    def go_idle(self):
        self.mode = "idle"
        self.source = None
        self.sim = None
        self.demo_until = None
        self.intro = None
        self.intro_wait = None
        idle = self.cfg.get("idle", {})
        self.state.reset({"title": idle.get("text", "INSERT COIN"), "idle_text": idle.get("text", "INSERT COIN")})
        self.set_scene("_idle")

    def start_game(self, meta, source, intro=True):
        key = meta.get("game") or ""
        if not key or key not in self.library.games:
            key = self.library.match(meta) or ""
        g = self.library.get(key) or {}
        titles = g.get("titles") if isinstance(g.get("titles"), dict) else {}
        # own_title: the name of a version, a bootleg or a homebrew under RetroArch / le nom d'une version sous RetroArch
        title = (titles.get(meta.get("system") or "") or meta.get("own_title") or titles.get(meta.get("parent") or "")
                 or g.get("title") or clean_title(meta.get("description")) or meta.get("system", ""))
        meta = dict(meta)
        meta["title"] = title
        meta["game"] = key
        if not meta.get("parent") and not g.get("fallback"):       # RetroArch ne donne pas le parent d'un clone
            m = g.get("match")
            sets = m[0].get("system") if isinstance(m, list) and m and isinstance(m[0], dict) else None
            if isinstance(sets, list) and sets and meta.get("system") in sets[1:]:
                meta["parent"] = sets[0]
        if self.pixelcade_dir:
            meta["pixelcade"] = self.pixelcade_dir
        self.state.reset(meta)
        self.derived = g.get("derived") if isinstance(g.get("derived"), dict) else None
        names = meta.get("values") if isinstance(meta.get("values"), list) else []
        # credits of a Neo Geo that cannot be read (RetroArch): guessed from its BIOS / crédits devinés d'après le BIOS
        self.coin_guess = NeoCoins(mvs_rates(self.cfg)) if (source in ("plugin", "retroarch") and "credits" not in names
                                                            and "bios_request" in names) else None
        # a game without a BIOS that says who plays (CPS): player 1 plays while its values move (timer, health...)
        # un jeu sans BIOS qui dit qui joue (CPS) : le joueur 1 joue tant que ses valeurs bougent (chrono, vie...)
        act = g.get("activity") if isinstance(g.get("activity"), dict) else None
        self.activity = None
        if act and source in ("plugin", "retroarch") and "p1_mode" not in names:
            watch = [v for v in act.get("values", []) if isinstance(v, str) and v in names]     # nothing read: no guess
            # "moving": at least one of these must be read, values that move all through a game (the timer, the
            # score). Lives or bombs alone change too seldom: without them the game scene simply stays.
            # "moving" : au moins une de ces valeurs doit être lue, sinon la scène du jeu reste affichée.
            moving = act.get("moving")
            if watch and (not isinstance(moving, list) or any(v in watch for v in moving)):
                self.activity = {"values": set(watch), "seconds": float(act.get("seconds", 10))}
        self.active_at = -1e9
        vals = game_values(g, meta.get("system") or "", meta.get("parent") or "") if g else {}
        self.hold_zero = {k: float(d["hold_zero"]) for k, d in vals.items()
                          if isinstance(d, dict) and isinstance(d.get("hold_zero"), (int, float)) and d["hold_zero"] > 0}
        self.zero_since = {}
        self.mode = "game"
        self.source = source
        if source != "demo":
            self.sim = None
            self.demo_until = None
        self.set_scene(key if key else "_generic")
        self.intro = None
        self.intro_wait = None
        if intro and self.intro_cfg.get("logo", True):
            self.intro_serial += 1
            self.intro_wait = {"since": None, "roms": [meta.get("system") or "", meta.get("parent") or ""],
                               "title": title, "path": None}
        self.log(tr(f"jeu : {meta.get('system')} « {title} » -> scène {self.scene_key}",
                    f"game: {meta.get('system')} \"{title}\" -> scene {self.scene_key}"))

    def start_demo(self, key, seconds=None):
        g = self.library.get(key)
        if g is None and key not in ("_idle", "_generic"):
            files = ", ".join(sorted(self.library.games))
            self.log(tr(f"jeu inconnu : {key} (fichiers disponibles : {files})",
                        f"unknown game: {key} (available files: {files})"))
        if key == "_idle":
            return
        self.start_game({"game": key, "system": key, "description": (g or {}).get("title", key)}, "demo")
        self.sim = Simulator(key, g, self.state)
        self.demo_until = time.monotonic() + seconds if seconds else None

    def check_demo_request(self):
        """demo_sonic.bat lancé pendant que le moteur tourne : il dépose une demande ici."""
        now = time.monotonic()
        if now < self.next_request_check:
            return
        self.next_request_check = now + 0.5
        if not os.path.exists(self.demo_request):
            return
        try:
            with open(self.demo_request, "r", encoding="utf-8") as f:
                req = json.load(f)
        except (OSError, ValueError):
            req = {}
        try:
            os.remove(self.demo_request)
        except OSError:
            pass
        key = str(req.get("game") or "")
        if not key:
            return
        if self.mode == "game" and self.source in ("plugin", "retroarch"):
            self.log(tr(f"démo {key} ignorée : une partie est en cours", f"demo {key} ignored: a game is in progress"))
            return
        self.log(tr(f"démo demandée : {key}", f"demo requested: {key}"))
        self.start_demo(key, float(req.get("seconds", 20)))

    def message(self, text, seconds=2.0, color="#ffffff"):
        self.overlay = (text, time.monotonic() + seconds, parse_color(color))

    # -- événements
    def handle_event(self, ev, now, source="plugin"):
        t = ev.get("t")
        self.last_event = time.monotonic()
        if t == "start":
            self.last_start = dict(ev)
            self.start_game(ev, source)
        elif t in ("v", "hb"):
            if self.mode != "game" or self.source != source:
                # reprise après un silence (menu MAME ouvert longtemps, moteur relancé en cours de partie) : sans le logo
                self.start_game(self.last_start or {"system": "?", "description": ""}, source, intro=False)
            # état des joueurs d'abord : il dit si un score qui tombe à 0 est une vraie remise à zéro
            for k, v in sorted((ev.get("v") or {}).items(), key=lambda kv: not kv[0].endswith("_mode")):
                if k in self.hold_zero and self._hold_zero(k, v, now):
                    continue
                self.state.update(k, v, now, quiet=(t == "hb"))
            if self.derived:      # valeurs calculées (nom du personnage en train de se battre...)
                for k, v in derive(self.derived, self.state.values).items():
                    self.state.update(k, v, now, quiet=(t == "hb"))
            if self.coin_guess is not None:
                old = self.state.values.get("credits")
                c = self.coin_guess.update(self.state.values, now)
                for fr, en in self.coin_guess.notes:
                    self.log(tr(fr, en))
                self.coin_guess.notes.clear()
                if c is not None and c != old:
                    if isinstance(old, int) and c > old:
                        self.state.update("coin_side", None, now)      # seen by the BIOS only: side unknown / côté inconnu
                    self.state.update("credits", c, now)
                    self.log(tr(f"crédits devinés d'après le BIOS : {c}", f"credits guessed from the BIOS: {c}"))
        elif t == "stop":
            if self.source == source or self.mode != "game":
                self.go_idle()
        elif t == "pause":
            self.state.paused = True
        elif t == "resume":
            self.state.paused = False
        elif t == "capture":
            self.message(f"CAPTURE {ev.get('n', '')}", 1.5, "#ffdd33")

    def _activity(self, now):
        """p1_mode 1 while a watched value changes (not its first reading), 0 after "seconds" without a change: the coin
        screen when nobody plays, the game's layout during a game or its demo. / p1_mode d'après les valeurs qui bougent."""
        a = self.activity
        if any(e[0] in a["values"] for e in self.state.events):
            self.active_at = now
        self.state.update("p1_mode", 1 if now - self.active_at < a["seconds"] else 0, now)

    def coin_rates(self):
        """Credits a coin gives on the left and on the right, written on the coin doors of the HD screen. A Neo Geo in
        MVS mode gives 2 for a coin in its second slot unless its settings were changed ("mvs_credits").
        / Crédits d'une pièce à gauche et à droite, écrits sur les monnayeurs de l'écran HD."""
        return mvs_rates(self.cfg) if self.state.values.get("bios_mvs") == 0x80 else (1, 1)

    def coin_in(self, side, now):
        """A coin button pressed on the cabinet (0 left, 1 right): the side of the coin, and the credits of a Neo Geo
        under RetroArch. Nothing outside a game, nor while RetroArch shows its menu (the button moves in the menu).
        / Un bouton des pièces : le côté de la pièce, et les crédits d'une Neo Geo sous RetroArch."""
        if self.mode != "game" or self.source not in ("plugin", "retroarch") or self.state.paused:
            return
        self.state.update("coin_side", side, now)
        where = side_word(side)
        if self.coin_guess is None:
            self.log(tr(f"pièce à {where}", f"coin on the {where}"))
            return
        old = self.state.values.get("credits")
        c = self.coin_guess.add(side, now)
        if c is not None and c != old:
            self.state.update("credits", c, now)
        self.log(tr(f"pièce à {where}, crédits devinés {c}", f"coin on the {where}, credits guessed {c}"))

    def _hold_zero(self, k, v, now):
        """Score lu à 0 en pleine partie (l'objet du combattant n'est pas encore recréé entre deux rounds
        ou deux combats) : l'ancien score reste affiché, au plus "hold_zero" secondes."""
        old = self.state.values.get(k)
        mode = self.state.values.get("p2_mode" if "p2" in k else "p1_mode")
        if v == 0 and isinstance(old, (int, float)) and old > 0 and mode in (None, 1):
            first = self.zero_since.setdefault(k, now)
            return now - first < self.hold_zero[k]
        self.zero_since.pop(k, None)
        return False

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

    def _panels_ready(self):
        """Faux tant qu'une dalle n'est pas encore à nous (la Pixelcade attend que pixelweb la libère)."""
        for out in self.outputs:
            fn = getattr(out, "panel_ready", None)
            if fn is not None:
                try:
                    if not fn():
                        return False
                except Exception:
                    pass
        return True

    def _intro_start(self, now):
        """Jeu lancé : le logo arrive dès que LaunchBox l'a trouvé et que la dalle est prête.
        Renvoie True s'il faut garder la dalle noire en attendant (logo trouvé, dalle pas encore libre)."""
        w = self.intro_wait
        if w["since"] is None:
            w["since"] = now
        waited = now - w["since"]
        logos = self.logos
        if logos is None or waited > 10.0:
            self.intro_wait = None
            return False
        if w["path"] is None:
            if not logos.ready:                    # index LaunchBox pas encore prêt (ArcadeDMD tout juste lancé)
                if waited > 4.0:
                    self.intro_wait = None
                return False
            try:
                w["path"] = logos.find(w["roms"], w["title"]) or ""
            except Exception:
                w["path"] = ""
            if not w["path"]:
                self.intro_wait = None
                return False
        if not self._panels_ready() and waited < 8.0:
            return True
        try:
            self.intro = LogoIntro(w["path"], now, float(self.intro_cfg.get("seconds", 2.6)))
        except Exception as e:
            self.log(tr(f"logo au lancement illisible {w['path']} ({e})", f"unreadable launch logo {w['path']} ({e})"))
        self.intro_wait = None
        return False

    def render(self, now):
        self.ctx.t = now
        black = self._intro_start(now) if self.intro_wait is not None else False
        if self.intro is not None and not self.intro.draw(self.canvas, now):
            self.intro = None
        if black:
            self.canvas.clear((0, 0, 0))
        elif self.intro is None:
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
        if self.coin_buttons is not None:
            # before what the game shows of that same coin / avant ce que le jeu montre de cette même pièce
            for side in self.coin_buttons.poll(now):
                self.coin_in(side, now)
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
            elif item[0] == "ev":
                self.handle_event(item[1], now, "retroarch")
        if self.tail is not None:
            self.check_demo_request()
            if time.monotonic() >= self.next_cfg_check:
                self.next_cfg_check = time.monotonic() + 2.0
                m = _mtime(self.cfg_path)
                if m != self.cfg_mtime:
                    self.cfg_mtime = m
                    self.log(tr("config.json modifié : redémarrage avec les nouveaux réglages",
                                "config.json changed: restarting with the new settings"))
                    self.restart = True
        if self.sim:
            self.sim.step(now)
            if self.derived:
                for k, v in derive(self.derived, self.state.values).items():
                    self.state.update(k, v, now, quiet=True)
            if self.demo_until is not None and time.monotonic() > self.demo_until:
                self.log(tr("fin de la démo", "end of the demo"))
                self.go_idle()
        if (self.mode == "game" and self.source in ("plugin", "retroarch")
                and time.monotonic() - self.last_event > float(self.cfg.get("heartbeat_timeout", 8))):
            src = "MAME" if self.source == "plugin" else "RetroArch"
            self.log(tr(f"plus de nouvelles de {src} : retour à l'écran d'attente",
                        f"no news from {src}: back to the idle screen"))
            self.go_idle()
        if self.activity is not None:
            self._activity(now)
        if self.texts is not None:     # fichiers texte pour OBS, séries de victoires en match VS
            try:
                self.texts.update(self.state, self.mode == "game" and self.source != "demo",
                                  self.state.meta.get("game") or "")
            except Exception as e:
                self.log(tr(f"fichiers texte : {e}", f"text files: {e}"))
                self.texts = None
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
                if self.restart:
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
                    self.log(tr(f"fermeture sortie : {e}", f"closing output: {e}"))
            if self.bridge:
                self.bridge.close()
            if self.retroarch:
                self.retroarch.close()
            if self.coin_buttons:
                self.coin_buttons.close()
        return "restart" if self.restart else None


def _mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def scale(c, k):
    return (int(c[0] * k), int(c[1] * k), int(c[2] * k))


# --------------------------------------------------------------------------
# utilitaires de lancement
# --------------------------------------------------------------------------

def load_config(root, log):
    """Valeurs internes, puis config.default.json (livré), puis config.json (tes réglages, jamais écrasé)."""
    cfg = DEFAULT_CONFIG
    defaults = "config.default.json"
    if not os.path.exists(os.path.join(root, defaults)) and os.path.exists(os.path.join(root, "config.defaut.json")):
        defaults = "config.defaut.json"         # ancien nom, dossier pas encore mis à jour
    for name in (defaults, "config.json"):
        path = os.path.join(root, name)
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                cfg = deep_merge(cfg, json.load(f))
        except (OSError, ValueError) as e:
            log(tr(f"{name} illisible ({e}), fichier ignoré", f"{name} unreadable ({e}), file ignored"))
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
            log(tr(f"aperçu impossible : {e}", f"preview window unavailable: {e}"))
    if zedmd and o.get("pixelcade", {}).get("enabled"):
        outs.append(PixelcadeOutput(o["pixelcade"], root, log))
    if gif:
        outs.append(GifRecorder(gif, log=log))
    if not outs:
        outs.append(NullOutput())
    return outs
