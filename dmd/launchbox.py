"""Logos des jeux pris dans les médias de LaunchBox et BigBox (images « Clear Logo »).

LaunchBox range ses images par plateforme et par titre de jeu
  <LaunchBox>\\Images\\<plateforme>\\Clear Logo\\<titre>-01.png      (parfois dans un sous-dossier de région)
Le lien entre le romset (kof98) et le titre (The King of Fighters '98) vient de
  <LaunchBox>\\Data\\Platforms\\<plateforme>.xml                     (ApplicationPath de chaque jeu)
L'index est construit une seule fois, en arrière-plan.
"""

import glob
import os
import re
import sys
import threading
import xml.etree.ElementTree as ET

IMAGE_TYPES = ("Clear Logo",)
_BAD = re.compile(r"[\\/:*?\"<>|']")        # caractères que LaunchBox remplace par _ dans les noms d'images
_IMG = (".png", ".jpg", ".jpeg", ".gif")


def norm(title):
    t = _BAD.sub("_", title or "")
    return re.sub(r"\s+", " ", t).strip().lower()


def stem_key(filename):
    """« The King of Fighters _98-01.png » -> « the king of fighters _98 »."""
    stem = os.path.splitext(filename)[0]
    m = re.match(r"^(.*)-\d{2}$", stem)
    return norm(m.group(1) if m else stem)


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def is_launchbox(d):
    return bool(d) and os.path.isdir(os.path.join(d, "Data", "Platforms")) and os.path.isdir(os.path.join(d, "Images"))


def find_launchbox(root, cfg):
    """Dossier LaunchBox : réglage, dernier trouvé, BigBox ou LaunchBox en cours, puis les endroits habituels."""
    cands = [(cfg or {}).get("launchbox") or "", _read(os.path.join(root, "runtime", "launchbox_path.txt"))]
    try:
        from .pixelcade import find_process
        for name in ("BigBox.exe", "LaunchBox.exe"):
            cands += [os.path.dirname(p) for _, p in find_process(name) if p]
    except Exception:
        pass
    if sys.platform == "win32":
        for drive in "CDEFGHIJ":
            for sub in ("LaunchBox", "Games\\LaunchBox", "Jeux\\LaunchBox", "Emulation\\LaunchBox", "Arcade\\LaunchBox",
                        "Emulateurs\\LaunchBox", "Frontend\\LaunchBox"):
                cands.append(f"{drive}:\\{sub}")
    cands.append(os.path.join(os.path.expanduser("~"), "LaunchBox"))
    for c in cands:
        c = (c or "").strip().strip('"')
        if c and os.path.basename(c.rstrip("\\/")).lower() == "core":   # LaunchBox 13+ : exe dans Core
            c = os.path.dirname(c.rstrip("\\/"))
        if is_launchbox(c):
            return os.path.normpath(c)
    return ""


class LogoFinder:
    def __init__(self, root, cfg, log=print, background=True):
        self.root, self.cfg, self.log = root, cfg or {}, log
        self.dir = ""
        self.games = {}          # romset -> [(plateforme, titre)]
        self.files = {}          # plateforme -> {titre normalisé: chemin de l'image}
        self.ready = False
        if background:
            threading.Thread(target=self._build, daemon=True).start()
        else:
            self._build()

    def _build(self):
        try:
            d = find_launchbox(self.root, self.cfg)
            if not d:
                self.log("écran HD : dossier LaunchBox introuvable, le titre du jeu remplace son logo "
                         "(réglage \"launchbox\" de la section preview dans config.json)")
                return
            games = {}
            for xml in sorted(glob.glob(os.path.join(d, "Data", "Platforms", "*.xml"))):
                plat_file = os.path.splitext(os.path.basename(xml))[0]
                try:
                    for _, el in ET.iterparse(xml, events=("end",)):
                        if el.tag != "Game":
                            continue
                        title = (el.findtext("Title") or "").strip()
                        app = (el.findtext("ApplicationPath") or "").strip()
                        plat = (el.findtext("Platform") or plat_file).strip()
                        if title and app:
                            rom = os.path.splitext(os.path.basename(app.replace("\\", "/")))[0].lower()
                            games.setdefault(rom, []).append((plat, title))
                        el.clear()
                except (ET.ParseError, OSError) as e:
                    self.log(f"écran HD : {os.path.basename(xml)} illisible ({e})")
            self.games = games
            self.dir = d
            try:
                os.makedirs(os.path.join(self.root, "runtime"), exist_ok=True)
                with open(os.path.join(self.root, "runtime", "launchbox_path.txt"), "w", encoding="utf-8") as f:
                    f.write(d)
            except OSError:
                pass
            self.log(f"écran HD : logos des jeux pris dans {d} ({len(games)} jeux dans LaunchBox)")
        except Exception as e:                   # l'affichage continue sans logo
            self.log(f"écran HD : index LaunchBox impossible ({e})")
        finally:
            self.ready = True

    def _platform_files(self, plat):
        if plat in self.files:
            return self.files[plat]
        out, rank = {}, {}
        for typ in IMAGE_TYPES:
            base = os.path.join(self.dir, "Images", plat, typ)
            for dirpath, _, names in os.walk(base):
                for n in names:
                    if not n.lower().endswith(_IMG):
                        continue
                    k = stem_key(n)
                    r = (0 if dirpath == base else 1, 0 if re.search(r"-01\.\w+$", n) else 1, n)
                    if k not in rank or r < rank[k]:      # dossier principal et image -01 d'abord
                        rank[k] = r
                        out[k] = os.path.join(dirpath, n)
        self.files[plat] = out
        return out

    def platforms(self):
        try:
            return sorted(os.listdir(os.path.join(self.dir, "Images")))
        except OSError:
            return []

    def find(self, roms, title=""):
        """Image du logo pour ces romsets (le jeu, puis son parent), sinon d'après le titre. None si rien."""
        if not self.ready or not self.dir:
            return None
        for rom in [r for r in roms if r]:
            for plat, t in self.games.get(rom.lower(), []):
                p = self._platform_files(plat).get(norm(t))
                if p:
                    return p
        if title:
            k = norm(title)
            for plat in self.platforms():
                p = self._platform_files(plat).get(k)
                if p:
                    return p
        return None
