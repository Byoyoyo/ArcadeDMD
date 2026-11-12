"""The settings tabs of ArcadeDMD's window (1.37): the screens and the LED panel, the emulators (RetroArch, the MAME
plugin, the coin buttons, the recording of each game). What they change goes into config.json, and the engine starts
again with it by itself. Folders typed in the window only are kept in runtime/window.json.

Les onglets de réglage de la fenêtre : les écrans et la dalle, les émulateurs (RetroArch, le plugin MAME, les boutons
pièce, l'enregistrement des parties). Ce qu'ils changent va dans config.json, et le moteur repart tout seul avec.
"""

import contextlib
import io
import json
import os
import subprocess
import sys
import time
import zipfile

from . import setup_tools
from .i18n import tr

PORT_DEFAULT = 55355


def _home(*parts):
    return [os.path.join(os.environ.get(v, ""), *parts) for v in ("USERPROFILE",) if os.environ.get(v)]


RA_GUESSES = ([r"C:\RetroArch-Win64", r"C:\RetroArch", r"D:\RetroArch-Win64", r"D:\RetroArch", r"C:\RetroBat\emulators\retroarch",
               r"D:\RetroBat\emulators\retroarch", r"C:\LaunchBox\Emulators\RetroArch", r"D:\LaunchBox\Emulators\RetroArch"]
              + _home("LaunchBox", "Emulators", "RetroArch")
              + ([os.path.join(os.environ["APPDATA"], "RetroArch")] if os.environ.get("APPDATA") else []))
MAME_GUESSES = (_home("LaunchBox", "Emulators", "MAME")
                + [r"C:\LaunchBox\Emulators\MAME", r"D:\LaunchBox\Emulators\MAME", r"E:\LaunchBox\Emulators\MAME",
                   r"C:\HyperSpin\Emulators\MAME", r"D:\HyperSpin\Emulators\MAME", r"C:\RetroBat\emulators\mame",
                   r"D:\RetroBat\emulators\mame", r"C:\Emulateurs\MAME", r"D:\Emulateurs\MAME", r"C:\Emulators\MAME",
                   r"D:\Emulators\MAME", r"C:\MAME", r"D:\MAME", r"E:\MAME"])

IDENTIFY = r'''
import ctypes, json, sys, tkinter as tk
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass
screens = json.loads(sys.argv[1])
root = tk.Tk()
root.withdraw()
for i, s in enumerate(screens, 1):
    w = tk.Toplevel(root)
    w.overrideredirect(True)
    w.attributes("-topmost", True)
    hh = max(120, min(s["height"] * 2 // 3, 420))
    ww = max(200, min(s["width"] - 40, hh * 2))
    w.geometry("%dx%d+%d+%d" % (ww, hh, s["x"] + (s["width"] - ww) // 2, s["y"] + (s["height"] - hh) // 2))
    w.configure(bg="#FFB547")
    tk.Label(w, text=str(i), font=("Segoe UI", -int(hh * 0.75), "bold"), bg="#FFB547", fg="#1A1206").pack(expand=True, fill="both")
root.after(3500, root.destroy)
root.mainloop()
'''


class Setup:
    """The routes of the Screens and Emulators tabs, given to the window's server. / Les routes des onglets."""

    def __init__(self, root, log):
        self.root, self.log = root, log
        self.mame_cache = {}

    def routes(self):
        return {("GET", "/api/screens"): self.screens, ("POST", "/api/screens"): self.save_screens,
                ("POST", "/api/screens/identify"): self.identify, ("POST", "/api/test"): self.test,
                ("GET", "/api/emulators"): self.emulators, ("POST", "/api/emulators/folder"): self.set_folder,
                ("POST", "/api/emulators/retroarch/fix"): self.fix_retroarch,
                ("POST", "/api/emulators/mame/install"): self.install_plugin,
                ("POST", "/api/emulators/open"): self.open_thing, ("POST", "/api/emulators/record"): self.save_record,
                ("POST", "/api/coins/learn"): self.learn_coins, ("POST", "/api/captures/pack"): self.pack_last,
                ("GET", "/api/frontend"): self.frontend, ("POST", "/api/frontend"): self.save_frontend}

    # ------------------------------------------------------------ remembered folders / dossiers retenus
    def _window_file(self):
        return os.path.join(self.root, "runtime", "window.json")

    def remembered(self):
        try:
            with open(self._window_file(), "r", encoding="utf-8") as f:
                d = json.load(f)
            return d if isinstance(d, dict) else {}
        except (OSError, ValueError):
            return {}

    def remember(self, **kw):
        d = self.remembered()
        d.update(kw)
        os.makedirs(os.path.dirname(self._window_file()), exist_ok=True)
        with open(self._window_file(), "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)

    def config(self):
        try:
            cfg = setup_tools.load_config_file(self.root)
        except (OSError, ValueError):
            cfg = {}
        return cfg if isinstance(cfg, dict) else {}

    # ------------------------------------------------------------ screens / écrans
    def screens(self, _qs):
        from .screens import guess_dmd, list_screens
        from .app import load_config
        scr = list_screens()
        guess = guess_dmd(scr) if scr else None
        cfg = load_config(self.root, lambda *_: None)          # with the defaults / avec les valeurs de départ
        outs = cfg.get("outputs", {})
        pv = dict(outs.get("preview", {}))
        pc = dict(outs.get("pixelcade", {}))
        zd = dict(outs.get("zedmd", {}))
        for s in scr:
            s["chosen"] = bool(pv.get("enabled")) and s["x"] <= int(pv.get("x", -99999)) < s["x"] + s["width"] \
                and s["y"] <= int(pv.get("y", -99999)) < s["y"] + s["height"]
        for i, s in enumerate(scr):
            s["guess"] = i == guess
        try:
            from .pixelcade import list_ports
            ports = [{"device": d, "text": t, "likely": bool(lk)} for d, t, lk in list_ports()]
        except Exception:
            ports = []
        led = "pixelcade" if pc.get("enabled") else "zedmd" if zd.get("enabled") else "none"
        return {"screens": scr, "windows": sys.platform == "win32", "ports": ports,
                "preview": {k: pv.get(k) for k in ("enabled", "x", "y", "width", "height", "style", "topmost", "mode")},
                "led": {"kind": led, "device": pc.get("device") or "", "color_order": pc.get("color_order") or "auto",
                        "brightness": zd.get("brightness")}}

    def save_screens(self, data):
        cfg = self.config()
        outs = cfg.setdefault("outputs", {})
        pv_in = data.get("preview") if isinstance(data.get("preview"), dict) else {}
        pv = outs.setdefault("preview", {})
        if "enabled" in pv_in:
            pv["enabled"] = bool(pv_in["enabled"])
        for k in ("x", "y", "width", "height"):
            if k in pv_in:
                try:
                    pv[k] = int(pv_in[k])
                except (TypeError, ValueError):
                    name = {"x": tr("Position x", "Position x"), "y": tr("Position y", "Position y"),
                            "width": tr("Largeur", "Width"), "height": tr("Hauteur", "Height")}[k]
                    return {"ok": False, "error": tr(f"{name} doit être un nombre entier", f"{name} must be a whole number")}
        if pv.get("enabled") and (int(pv.get("width", 0)) < 64 or int(pv.get("height", 0)) < 16):
            return {"ok": False, "error": tr("La taille du marquee est trop petite", "The marquee size is too small")}
        if pv_in.get("style") in ("hd", "led"):
            pv["style"] = pv_in["style"]
        if "topmost" in pv_in:
            pv["topmost"] = bool(pv_in["topmost"])
        if pv.get("enabled"):
            pv.setdefault("borderless", True)
        led = data.get("led") if isinstance(data.get("led"), dict) else {}
        kind = led.get("kind")
        if kind in ("pixelcade", "zedmd", "none"):
            outs.setdefault("pixelcade", {})["enabled"] = kind == "pixelcade"
            outs.setdefault("zedmd", {})["enabled"] = kind == "zedmd"
        if kind == "pixelcade":
            pc = outs["pixelcade"]
            pc["device"] = str(led.get("device") or "")
            if led.get("color_order") in ("auto", "rgb", "rbg"):
                pc["color_order"] = led["color_order"]
        if kind == "zedmd" and "brightness" in led:
            b = led.get("brightness")
            outs["zedmd"]["brightness"] = int(b) if isinstance(b, (int, float)) and not isinstance(b, bool) else None
        setup_tools.save_config_file(self.root, cfg)
        self.log(tr("fenêtre : réglages des écrans enregistrés dans config.json", "window: screen settings saved in config.json"))
        return {"ok": True}

    def identify(self, _data):
        from .screens import list_screens
        scr = list_screens()
        if not scr:
            return {"ok": False, "error": tr("Windows seulement", "Windows only")}
        try:
            subprocess.Popen([sys.executable, "-c", IDENTIFY, json.dumps(scr)], close_fds=True,
                             creationflags=0x08000000 if sys.platform == "win32" else 0)
            return {"ok": True}
        except OSError as e:
            return {"ok": False, "error": str(e)}

    def test(self, data):
        """A demo of a few seconds on the marquee and the LED panel, like demo_fight.bat with ArcadeDMD running.
        Une démo de quelques secondes sur le marquee et la dalle."""
        game = str(data.get("game") or "kof98")
        if not os.path.isfile(os.path.join(self.root, "games", game + ".json")):
            return {"ok": False, "error": "game"}
        req = os.path.join(self.root, "runtime", "demo_request.json")
        os.makedirs(os.path.dirname(req), exist_ok=True)
        with open(req, "w", encoding="utf-8") as f:
            json.dump({"game": game, "seconds": int(data.get("seconds") or 12)}, f)
        return {"ok": True}

    # ------------------------------------------------------------ emulators / émulateurs
    def _ra_dir(self, cfg):
        rem = self.remembered().get("retroarch_dir")
        if rem and os.path.isfile(os.path.join(rem, "retroarch.cfg")):
            return rem, "remembered"
        try:
            from . import wincore
            for p in wincore.find_retroarch():
                d = os.path.dirname(p["exe"]) if os.path.isabs(p["exe"]) else ""
                if d and os.path.isfile(os.path.join(d, "retroarch.cfg")):
                    return d, "running"
        except Exception:
            pass
        for d in RA_GUESSES:
            if d and os.path.isfile(os.path.join(d, "retroarch.cfg")):
                return d, "found"
        return rem or "", ""

    def _mame_dir(self):
        rem = self.remembered().get("mame_dir")
        if rem and (setup_tools.find_mame_exe(rem) or os.path.isdir(os.path.join(rem, "plugins"))):
            return rem, "remembered"
        lb = (self.config().get("intro") or {}).get("launchbox") or ""
        for d in ([os.path.join(lb, "Emulators", "MAME")] if lb else []) + MAME_GUESSES:
            if d and (setup_tools.find_mame_exe(d) or os.path.isfile(os.path.join(d, "plugins", "boot.lua"))):
                return d, "found"
        return rem or "", ""

    def _mame_version(self, exe):
        try:
            key = (exe, os.path.getmtime(exe))
        except OSError:
            return None
        if key not in self.mame_cache:
            self.mame_cache[key] = setup_tools.mame_version(exe)
        return self.mame_cache[key]

    def emulators(self, _qs):
        from . import wincore
        from .app import load_config
        cfg = load_config(self.root, lambda *_: None)
        ra_cfg = cfg.get("retroarch") if isinstance(cfg.get("retroarch"), dict) else {}
        port = int(ra_cfg.get("port") or PORT_DEFAULT)
        radir, how = self._ra_dir(cfg)
        rcfg = wincore.read_cfg(os.path.join(radir, "retroarch.cfg")) if radir else {}
        running = False
        try:
            running = bool(wincore.find_retroarch())
        except Exception:
            pass
        ra = {"enabled": bool(ra_cfg.get("enabled", True)), "port": port, "dir": radir, "how": how,
              "cfg": bool(rcfg), "running": running,
              "net": rcfg.get("network_cmd_enable"), "net_port": rcfg.get("network_cmd_port") or str(PORT_DEFAULT),
              "save_on_exit": rcfg.get("config_save_on_exit", "true"),
              "shot_dir": wincore._resolve(radir, rcfg.get("screenshot_directory", "")) if radir else ""}
        mdir, mhow = self._mame_dir()
        exe = setup_tools.find_mame_exe(mdir) if mdir else ""
        mine = self._plugin_version(os.path.join(self.root, "mame-plugin", "arcadedmd"))
        theirs = self._plugin_version(os.path.join(mdir, "plugins", "arcadedmd")) if mdir else None
        mame = {"dir": mdir, "how": mhow, "exe": os.path.basename(exe) if exe else "",
                "version": self._mame_version(exe) if exe else None, "min": setup_tools.MIN_MAME,
                "plugin": theirs, "current": mine, "off": self._plugin_off(mdir) if mdir else False,
                "root_ok": self._plugin_root_ok(mdir) if mdir and theirs else None}
        cb = cfg.get("coin_buttons") if isinstance(cfg.get("coin_buttons"), dict) else {}
        coins = {}
        try:
            from .coinbuttons import describe, parse
            for k in ("left", "right", "start1", "start2"):
                coins[k] = describe(parse(cb.get(k))) if cb.get(k) else None
        except Exception:
            coins = {k: None for k in ("left", "right", "start1", "start2")}
        shots = ra_cfg.get("screenshots") if isinstance(ra_cfg.get("screenshots"), dict) else {}
        dump = ra_cfg.get("ram_dump") if isinstance(ra_cfg.get("ram_dump"), dict) else {}
        cap_dir = os.path.join(self.root, "runtime", "captures")
        last = self._last_capture()
        record = {"capture": cfg.get("capture", "all"), "ram": bool(dump.get("enabled", False)),
                  "shots": bool(shots.get("enabled", False)), "shots_dir": shots.get("dir") or "",
                  "last": os.path.basename(last) if last else "", "folder": cap_dir}
        return {"retroarch": ra, "mame": mame, "coins": coins, "record": record, "windows": sys.platform == "win32"}

    @staticmethod
    def _plugin_version(folder):
        try:
            with open(os.path.join(folder, "plugin.json"), "r", encoding="utf-8") as f:
                return json.load(f)["plugin"]["version"]
        except (OSError, ValueError, KeyError, TypeError):
            return None

    @staticmethod
    def _plugin_off(mdir):
        """"arcadedmd 0" in MAME's plugin.ini (its folder or ini). / Le plugin coupé dans plugin.ini."""
        for p in (os.path.join(mdir, "plugin.ini"), os.path.join(mdir, "ini", "plugin.ini")):
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        bits = line.split()
                        if len(bits) >= 2 and bits[0] == "arcadedmd":
                            return bits[1] == "0"
            except OSError:
                continue
        return False

    def _plugin_root_ok(self, mdir):
        try:
            with open(os.path.join(mdir, "plugins", "arcadedmd", "settings.json"), "r", encoding="utf-8") as f:
                root = json.load(f).get("root") or ""
        except (OSError, ValueError, AttributeError):
            return False
        norm = lambda p: os.path.normcase(os.path.normpath(p.replace("/", os.sep)))      # noqa: E731
        mine = {norm(self.root)}
        try:
            mine.add(norm(setup_tools.short_path(self.root)))
        except Exception:
            pass
        return norm(root) in mine

    def set_folder(self, data):
        what, folder = data.get("what"), str(data.get("dir") or "").strip().strip('"')
        if what == "retroarch":
            if folder.lower().endswith(".exe") or folder.lower().endswith(".cfg"):
                folder = os.path.dirname(folder)
            if not os.path.isfile(os.path.join(folder, "retroarch.cfg")):
                return {"ok": False, "error": tr("Pas de retroarch.cfg dans ce dossier", "No retroarch.cfg in this folder")}
            self.remember(retroarch_dir=folder)
            return {"ok": True}
        if what == "mame":
            if folder.lower().endswith(".exe"):
                folder = os.path.dirname(folder)
            if not (setup_tools.find_mame_exe(folder) or os.path.isdir(os.path.join(folder, "plugins"))):
                return {"ok": False, "error": tr("MAME introuvable dans ce dossier", "MAME not found in this folder")}
            self.remember(mame_dir=folder)
            return {"ok": True}
        return {"ok": False}

    def fix_retroarch(self, _data):
        """network_cmd_enable and network_cmd_port in retroarch.cfg, a copy kept first. RetroArch closed only: it
        writes its file again when it quits. / Les commandes réseau dans retroarch.cfg, avec une copie, RetroArch
        fermé seulement : il réécrit son fichier en quittant."""
        from . import wincore
        from .app import load_config
        if wincore.find_retroarch():
            return {"ok": False, "error": tr("Ferme RetroArch d'abord, il réécrit son réglage en quittant.",
                                             "Close RetroArch first, it writes its settings again when it quits.")}
        cfg = load_config(self.root, lambda *_: None)
        port = int((cfg.get("retroarch") or {}).get("port") or PORT_DEFAULT)
        radir, _ = self._ra_dir(cfg)
        path = os.path.join(radir, "retroarch.cfg") if radir else ""
        if not path or not os.path.isfile(path):
            return {"ok": False, "error": tr("retroarch.cfg introuvable", "retroarch.cfg not found")}
        with open(path, "rb") as f:
            raw = f.read()
        nl = b"\r\n" if b"\r\n" in raw else b"\n"
        lines = raw.split(nl)
        want = {b"network_cmd_enable": b'"true"', b"network_cmd_port": str(port).encode()}
        want[b"network_cmd_port"] = b'"' + want[b"network_cmd_port"] + b'"'
        done = set()
        for i, line in enumerate(lines):
            key = line.split(b"=", 1)[0].strip()
            if key in want:
                lines[i] = key + b" = " + want[key]
                done.add(key)
        if lines and lines[-1] == b"":
            lines.pop()
        for key, v in want.items():
            if key not in done:
                lines.append(key + b" = " + v)
        backup = path + ".arcadedmd-" + time.strftime("%Y%m%d-%H%M%S") + ".bak"
        with open(backup, "wb") as f:
            f.write(raw)
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(nl.join(lines) + nl)
        os.replace(tmp, path)
        self.log(tr(f"fenêtre : commandes réseau activées dans {path} (copie {os.path.basename(backup)})",
                    f"window: network commands turned on in {path} (copy {os.path.basename(backup)})"))
        return {"ok": True}

    def install_plugin(self, data):
        mdir = str(data.get("dir") or "").strip().strip('"') or self._mame_dir()[0]
        if not mdir:
            return {"ok": False, "error": tr("Dossier de MAME inconnu", "MAME folder unknown")}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                rc = setup_tools.install_plugin(self.root, mdir)
            except Exception as e:
                print(repr(e))
                rc = 9
        text = "\n".join(line.strip() for line in out.getvalue().splitlines() if line.strip())
        if rc == 0:
            self.remember(mame_dir=mdir)
        self.log(tr(f"fenêtre : plugin MAME, {text}", f"window: MAME plugin, {text}").replace("\n", " · "))
        return {"ok": rc == 0, "text": text}

    def open_thing(self, data):
        from .gui import open_path
        what = data.get("what")
        if what == "retroarch_cfg":
            radir, _ = self._ra_dir({})
            p = os.path.join(radir, "retroarch.cfg") if radir else ""
        elif what == "mame":
            p = self._mame_dir()[0]
        elif what == "captures":
            p = os.path.join(self.root, "runtime", "captures")
            os.makedirs(p, exist_ok=True)
        else:
            p = ""
        if not p or not os.path.exists(p):
            return {"ok": False}
        if what == "retroarch_cfg" and sys.platform == "win32":
            try:
                subprocess.Popen(["notepad.exe", p], close_fds=True)
                return {"ok": True}
            except OSError:
                pass
        return {"ok": open_path(p)}

    def save_record(self, data):
        cfg = self.config()
        if data.get("capture") in ("all", "fights", "off"):
            cfg["capture"] = data["capture"]
        ra = cfg.setdefault("retroarch", {})
        if "ram" in data:
            d = ra.get("ram_dump") if isinstance(ra.get("ram_dump"), dict) else {}
            d["enabled"] = bool(data["ram"])
            ra["ram_dump"] = d
        if "shots" in data or "shots_dir" in data:
            s = ra.get("screenshots") if isinstance(ra.get("screenshots"), dict) else {}
            if "shots" in data:
                s["enabled"] = bool(data["shots"])
            if "shots_dir" in data:
                s["dir"] = str(data["shots_dir"] or "")
            ra["screenshots"] = s
        setup_tools.save_config_file(self.root, cfg)
        self.log(tr("fenêtre : enregistrement des parties réglé dans config.json",
                    "window: game recording set in config.json"))
        return {"ok": True}

    def learn_coins(self, _data):
        bat = os.path.join(self.root, "coin_buttons.bat")
        if sys.platform != "win32" or not os.path.isfile(bat):
            return {"ok": False}
        try:
            subprocess.Popen(["cmd.exe", "/c", "start", "", bat], cwd=self.root, close_fds=True,
                             creationflags=0x08000000)
            return {"ok": True}
        except OSError as e:
            return {"ok": False, "error": str(e)}

    # ------------------------------------------------------------ the last game, ready to send / prête à envoyer
    def _last_capture(self):
        d = os.path.join(self.root, "runtime", "captures")
        try:
            logs = [os.path.join(d, n) for n in os.listdir(d) if n.endswith(".log")]
        except OSError:
            return None
        return max(logs, key=os.path.getmtime) if logs else None

    def pack_last(self, _data):
        """The capture of the last game (.log and .ram) and the log, in one zip next to them. / La capture de la
        dernière partie et le journal, dans un zip."""
        last = self._last_capture()
        if not last:
            return {"ok": False, "error": tr("Aucune partie enregistrée", "No game recorded")}
        stem = os.path.splitext(last)[0]
        out = os.path.join(self.root, "runtime", "envoi-" + os.path.basename(stem) + ".zip")
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for ext in (".log", ".ram"):
                if os.path.isfile(stem + ext):
                    z.write(stem + ext, "captures/" + os.path.basename(stem + ext))
            journal = os.path.join(self.root, "runtime", "arcadedmd.log")
            if os.path.isfile(journal):
                z.write(journal, "arcadedmd.log")
        size = os.path.getsize(out)
        if sys.platform == "win32":
            try:
                subprocess.Popen(["explorer.exe", "/select,", out], close_fds=True)
            except OSError:
                pass
        self.log(tr(f"fenêtre : {os.path.basename(out)} prêt à envoyer", f"window: {os.path.basename(out)} ready to send"))
        return {"ok": True, "file": os.path.basename(out), "size": size}

    # ------------------------------------------------------------ the frontend / le frontal
    def frontend(self, _qs):
        from .app import load_config
        from .launchbox import find_launchbox
        from .retrobat import find_retrobat
        cfg = load_config(self.root, lambda *_: None)
        fe = cfg.get("frontend") if isinstance(cfg.get("frontend"), dict) else {}
        pv = (cfg.get("outputs") or {}).get("preview") or {}
        lb_set = (cfg.get("intro") or {}).get("launchbox") or pv.get("launchbox") or ""
        lb = find_launchbox(self.root, {"launchbox": lb_set})
        rb = find_retrobat(self.root, str(fe.get("retrobat") or ""))
        platforms = 0
        if lb:
            try:
                platforms = len([n for n in os.listdir(os.path.join(lb, "Data", "Platforms")) if n.lower().endswith(".xml")])
            except OSError:
                pass
        logos, systems = 0, 0
        if rb:
            base = os.path.join(rb, "roms")
            try:
                for sysname in os.listdir(base):
                    try:
                        n = len([f for f in os.listdir(os.path.join(base, sysname, "images"))
                                 if f.lower().rsplit(".", 1)[0].endswith(("-marquee", "-wheel"))])
                    except OSError:
                        continue
                    if n:
                        logos += n
                        systems += 1
            except OSError:
                pass
        use = str(fe.get("use") or "auto").lower()
        return {"use": use if use in ("auto", "launchbox", "retrobat", "none") else "auto",
                "launchbox": {"dir": lb or lb_set, "found": bool(lb), "platforms": platforms},
                "retrobat": {"dir": rb or str(fe.get("retrobat") or ""), "found": bool(rb), "logos": logos, "systems": systems},
                "between": "games" if str(pv.get("mode") or "always").lower() == "games" else "always",
                "preview": bool(pv.get("enabled")), "logo_intro": bool((cfg.get("intro") or {}).get("logo", True))}

    def save_frontend(self, data):
        cfg = self.config()
        fe = cfg.get("frontend") if isinstance(cfg.get("frontend"), dict) else {}
        use = data.get("use")
        if use in ("auto", "launchbox", "retrobat", "none"):
            fe["use"] = use
        if use == "launchbox" and data.get("launchbox") is not None:
            d = str(data["launchbox"]).strip().strip('"')
            if d:
                from .launchbox import is_launchbox
                if os.path.basename(d.rstrip("\\/")).lower() == "core":
                    d = os.path.dirname(d.rstrip("\\/"))
                if not is_launchbox(d):
                    return {"ok": False, "error": tr("LaunchBox introuvable dans ce dossier, il faut celui qui contient Data et Images",
                                                     "LaunchBox not found in this folder, it must hold Data and Images")}
            cfg.setdefault("intro", {})["launchbox"] = d
            cfg.setdefault("outputs", {}).setdefault("preview", {})["launchbox"] = d
        if use == "retrobat" and data.get("retrobat") is not None:
            d = str(data["retrobat"]).strip().strip('"')
            if d:
                from .retrobat import is_retrobat
                if not is_retrobat(d):
                    return {"ok": False, "error": tr("RetroBat introuvable dans ce dossier, il faut celui qui contient roms et emulationstation",
                                                     "RetroBat not found in this folder, it must hold roms and emulationstation")}
            fe["retrobat"] = d
        cfg["frontend"] = fe
        if data.get("between") in ("games", "always"):
            cfg.setdefault("outputs", {}).setdefault("preview", {})["mode"] = data["between"]
        setup_tools.save_config_file(self.root, cfg)
        self.log(tr("fenêtre : frontal enregistré dans config.json", "window: frontend saved in config.json"))
        return {"ok": True}
