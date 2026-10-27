"""Live game values written to small text files for OBS (score, credits, fighters, VS win streaks),
plus the King of Fighters VS history (vs_history.txt) and best streaks (records.json).
The file contents use no French words, only the log messages are translated.

Valeurs du jeu écrites dans de petits fichiers texte, mis à jour en direct.

OBS (source « Texte », case « Lire à partir d'un fichier ») les affiche pendant un direct.
Dans les King of Fighters en match VS, chaque victoire d'affilée (BEAT BY en haut de l'écran du jeu)
est aussi notée dans vs_history.txt, et la meilleure série de chaque jeu est gardée dans records.json.

Textes sans mots français, lisibles par tout le monde : « P2 RUGAL > P1 KIM » veut dire que P2 a gagné.
"""

import json
import os
import time

from .i18n import tr

LIVE = (
    ("game.txt", "title"),
    ("score_p1.txt", "score"),
    ("score_p2.txt", "score_p2"),
    ("credits.txt", "credits"),
    ("fighter_p1.txt", "p1_char"),
    ("fighter_p2.txt", "p2_char"),
    ("streak_p1.txt", "beat"),
    ("streak_p2.txt", "beat_p2"),
)


def _int(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return None


class TextFiles:
    def __init__(self, cfg, root, log=print):
        folder = (cfg or {}).get("folder") or "obs"
        self.dir = folder if os.path.isabs(folder) else os.path.join(root, folder)
        self.log = log
        self.history = bool((cfg or {}).get("history", True))
        self.written = {}
        self.prev = {}
        self.game = None
        self.warned = False
        self.records_path = os.path.join(self.dir, "records.json")
        self.records = {}
        try:
            with open(self.records_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                self.records = data
        except (OSError, ValueError):
            pass

    # -- écriture
    def _write(self, name, text):
        path = os.path.join(self.dir, name)
        try:
            os.makedirs(self.dir, exist_ok=True)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)
            try:
                os.replace(tmp, path)
            except PermissionError:          # OBS lisait le fichier à cet instant : écriture directe
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                os.remove(tmp)
            self.written[name] = text
            return True
        except OSError as e:
            if not self.warned:
                self.warned = True
                self.log(tr(f"fichiers texte : écriture impossible dans {self.dir} ({e})",
                            f"text files: cannot write to {self.dir} ({e})"))
            return False

    def _append(self, name, line):
        try:
            os.makedirs(self.dir, exist_ok=True)
            with open(os.path.join(self.dir, name), "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except OSError as e:
            self.log(tr(f"fichiers texte : {name} non modifiable ({e})", f"text files: cannot update {name} ({e})"))

    # -- séries de victoires en match VS
    def _won(self, state, game, side, streak):
        vals = state.values
        me, other = ("p1", "p2") if side == "P1" else ("p2", "p1")
        who = " ".join(x for x in (side, vals.get(me + "_char")) if x)
        them = " ".join(x for x in (other.upper(), vals.get(other + "_char")) if x)
        when = time.strftime("%d/%m/%Y %H:%M")
        title = state.meta.get("title") or game
        if self.history:
            self._append("vs_history.txt", f"{when} | {title} | {who} > {them} | BEAT BY {streak:02d}")
        best = self.records.get(game) or {}
        if streak > (_int(best.get("best")) or 0):
            self.records[game] = {"best": streak, "side": side, "fighter": vals.get(me + "_char") or "", "date": when,
                                  "title": title}
            try:
                os.makedirs(self.dir, exist_ok=True)
                with open(self.records_path, "w", encoding="utf-8") as f:
                    json.dump(self.records, f, indent=1, ensure_ascii=False)
                    f.write("\n")
            except OSError as e:
                self.log(tr(f"fichiers texte : records.json non modifiable ({e})", f"text files: cannot update records.json ({e})"))
            self.log(tr(f"nouveau record de série pour {title} : BEAT BY {streak:02d} ({who})",
                        f"new win streak record for {title}: BEAT BY {streak:02d} ({who})"))

    def best_text(self, game):
        r = self.records.get(game) if game else None
        if not isinstance(r, dict) or not _int(r.get("best")):
            return ""
        who = " ".join(x for x in (r.get("side"), r.get("fighter")) if x)
        return f"BEAT BY {_int(r['best']):02d} | {who} | {str(r.get('date', ''))[:10]}"

    # -- appelé par le moteur à chaque image
    def update(self, state, playing, game):
        vals = state.values
        out = {}
        for name, key in LIVE:
            v = state.meta.get(key) if key == "title" else vals.get(key)
            out[name] = "" if (not playing or v is None or v == "") else str(v)
        b1, b2 = _int(vals.get("beat")), _int(vals.get("beat_p2"))
        vs = (playing and vals.get("p1_mode") == 1 and vals.get("p2_mode") == 1 and b1 is not None and b2 is not None
              and (b1 > 0 or b2 > 0))
        out["vs_p1.txt"] = (f"BEAT BY {b1:02d}" if b1 else "CHALLENGER") if vs else ""
        out["vs_p2.txt"] = (f"BEAT BY {b2:02d}" if b2 else "CHALLENGER") if vs else ""
        if playing and game:
            if game != self.game:
                self.prev = {}
                self.game = game
            for side, key in (("P1", "beat"), ("P2", "beat_p2")):
                v, p = _int(vals.get(key)), self.prev.get(key)
                if v is not None and p is not None and v == p + 1:
                    self._won(state, game, side, v)          # une victoire de plus en match VS
                if v is not None:
                    self.prev[key] = v
        else:
            self.prev = {}
            self.game = None
        out["best_streak.txt"] = self.best_text(game) if playing else ""
        for name, text in out.items():
            if self.written.get(name) != text:
                self._write(name, text)
