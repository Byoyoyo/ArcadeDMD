"""Captures of the games (1.33): during a fighting game, every change of every value read is written with its time to
runtime/captures/<game>-<date>.log, a few hundred KB for a match. One match per game is enough to replay it offline
in the fight engine, tune the game's file (its select screens, the state of its fights, its round) and keep the
capture as a test. "capture" in config.json: "all" (every game, the default since test 7, Seb played Windjammers
and nothing was captured), "fights" (the fighting games only) or "off".

Captures des parties : pendant un jeu de combat, chaque changement de chaque valeur lue est écrit avec son heure dans
runtime/captures/<jeu>-<date>.log. Un match par jeu suffit pour le rejouer dans le moteur de combat, régler le
fichier du jeu et garder la capture comme test. "capture" dans config.json : "all" (tous les jeux, par défaut), "fights" ou "off".

Format, one line each / une ligne chacun :
  # {"version": "1.33.0", "game": "samsho2", "system": "samsho2", "title": "...", "date": "...", "values": [...]}
  0.000 health 100
  12.345 _in_p1 253
The time is in seconds from the start of the capture, the stick and buttons at the time they were read.
"""
import json
import os
import time

from .i18n import tr

FIGHT_SCENES = ("neogeo_combat", "cps_combat", "cave_combat")
MAX_LINES = 400000          # a capture stops there (a game left running) / une capture s'arrête là
FLUSH_EVERY = 2.0


class Capture:
    def __init__(self, root, log, mode="all"):
        self.root, self.log = root, log
        self.mode = str(mode or "all").lower()
        self.f = None
        self.path = None
        self.t0 = 0.0
        self.last = {}
        self.seen = {}              # "_in_" history numbers already written / numéros déjà écrits
        self.lines = 0
        self.flushed = 0.0

    @property
    def on(self):
        return self.f is not None

    @staticmethod
    def is_fight(game, key):
        if not isinstance(game, dict):
            return False
        if (game.get("scene_from") or key) in FIGHT_SCENES:
            return True
        vals = (game.get("memory") or {}).get("values") or {}
        return "health" in vals and "health_p2" in vals

    def start(self, meta, game, key, version, now):
        """A game starts: its capture, if its kind asks for one. / Un jeu commence : sa capture, si son genre le demande."""
        self.stop(now)
        if self.mode == "off" or (self.mode != "all" and not self.is_fight(game, key)):
            return
        folder = os.path.join(self.root, "runtime", "captures")
        try:
            os.makedirs(folder, exist_ok=True)
            stamp = time.strftime("%Y%m%d-%H%M%S")
            self.path = os.path.join(folder, f"{key or 'game'}-{stamp}.log")
            self.f = open(self.path, "w", encoding="utf-8")
        except OSError as e:
            self.f = None
            self.log(tr(f"capture : impossible d'écrire dans {folder} ({e})", f"capture: cannot write in {folder} ({e})"))
            return
        self.t0 = now
        self.last = {}
        self.seen = {}
        self.lines = 0
        self.flushed = now
        vals = (game.get("memory") or {}).get("values") or {} if isinstance(game, dict) else {}
        head = {"version": version, "game": key, "system": meta.get("system"), "parent": meta.get("parent"),
                "title": meta.get("title"), "date": time.strftime("%Y-%m-%d %H:%M:%S"), "values": sorted(vals)}
        self.f.write("# " + json.dumps(head, ensure_ascii=False) + "\n")
        self.log(tr(f"capture de la partie dans {os.path.relpath(self.path, self.root)}",
                    f"capture of the game in {os.path.relpath(self.path, self.root)}"))

    def poll(self, state, now):
        """Writes what changed since the last call. / Écrit ce qui a changé depuis le dernier appel."""
        if self.f is None:
            return
        try:
            t = now - self.t0
            for name, value in state.values.items():
                if name.startswith("_in_"):
                    continue                                          # from its history, at the time read / de l'historique
                if self.last.get(name, _MISSING) != value:
                    self.last[name] = value
                    self._line(t, name, value)
            for name, hist in (getattr(state, "hist", None) or {}).items():
                done = self.seen.get(name, 0)
                for n, at, v in hist:
                    if n > done:
                        self._line(max(0.0, at - self.t0), name, v)
                        done = n
                self.seen[name] = done
            if now - self.flushed >= FLUSH_EVERY:
                self.f.flush()
                self.flushed = now
            if self.lines >= MAX_LINES:
                self.log(tr("capture arrêtée (trop longue)", "capture stopped (too long)"))
                self.stop(now)
        except OSError as e:
            self.log(tr(f"capture : {e}", f"capture: {e}"))
            self.f = None

    def _line(self, t, name, value):
        if isinstance(value, float):
            value = round(value, 3)
        self.f.write(f"{t:.3f} {name} {json.dumps(value, ensure_ascii=False)}\n")
        self.lines += 1

    def stop(self, now):
        if self.f is None:
            return
        try:
            self.f.write(f"{now - self.t0:.3f} _end 1\n")
            self.f.close()
        except OSError:
            pass
        self.f = None
        self.log(tr(f"capture écrite, {self.lines} changements : {os.path.relpath(self.path, self.root)}",
                    f"capture written, {self.lines} changes: {os.path.relpath(self.path, self.root)}"))


_MISSING = object()


def read_capture(path):
    """A capture read back: (header, [(t, name, value)]). / Une capture relue."""
    head, rows = {}, []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("#"):
                try:
                    head = json.loads(line[1:].strip())
                except ValueError:
                    pass
                continue
            t, name, value = line.split(" ", 2)
            rows.append((float(t), name, json.loads(value)))
    return head, rows
