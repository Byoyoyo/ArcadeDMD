"""Game logos taken from the RetroBat media (1.37), for cabinets without LaunchBox.

RetroBat's scraper puts the logo of each game next to its roms, named after the rom:
  <RetroBat>\\roms\\<system>\\images\\<rom>-marquee.png        (or -wheel.png)
and writes it in <RetroBat>\\roms\\<system>\\gamelist.xml (<marquee>, <wheel>). Both are read, gamelist.xml first.
The arcade systems are looked at first when a rom is in several.

Logos des jeux pris dans les médias de RetroBat, pour les bornes sans LaunchBox. Le scraper range le logo de chaque
jeu à côté de ses roms, au nom de la rom, et l'écrit dans gamelist.xml. Les deux sont lus, gamelist.xml d'abord.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

from .i18n import tr

ARCADE = ("mame", "fbneo", "neogeo", "cps1", "cps2", "cps3", "naomi", "naomi2", "atomiswave", "model2", "model3",
          "hikaru", "triforce", "daphne", "arcade")
TAGS = ("marquee", "wheel")
_IMG = (".png", ".jpg", ".jpeg", ".webp")
_SUFFIX = re.compile(r"^(.*)-(marquee|wheel)$", re.I)


def norm(title):
    t = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", title or "")
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def is_retrobat(d):
    return bool(d) and os.path.isdir(os.path.join(d, "roms")) and (
        os.path.isdir(os.path.join(d, "emulationstation")) or os.path.isfile(os.path.join(d, "retrobat.exe")))


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def find_retrobat(root, folder=""):
    """RetroBat's folder: the setting, the last one found, RetroBat or its EmulationStation running, then the usual
    places. / Le dossier de RetroBat : le réglage, le dernier trouvé, RetroBat lancé, puis les endroits habituels."""
    cands = [folder or "", _read(os.path.join(root, "runtime", "retrobat_path.txt"))]
    try:
        from .pixelcade import find_process
        for name in ("retrobat.exe", "emulationstation.exe"):
            for _, p in find_process(name):
                if p:
                    d = os.path.dirname(p)
                    cands += [d, os.path.dirname(d)]           # emulationstation\emulationstation.exe
    except Exception:
        pass
    if sys.platform == "win32":
        for drive in "CDEFGHIJ":
            for sub in ("RetroBat", "Games\\RetroBat", "Jeux\\RetroBat", "Emulation\\RetroBat", "Arcade\\RetroBat"):
                cands.append(f"{drive}:\\{sub}")
    cands.append(os.path.join(os.path.expanduser("~"), "RetroBat"))
    for c in cands:
        c = (c or "").strip().strip('"')
        if is_retrobat(c):
            return os.path.normpath(c)
    return ""


class RetroBatLogos:
    """romset -> logo image, built once. find() has the same use as LaunchBox's LogoFinder.find().
    romset -> image du logo, construit une fois."""

    def __init__(self, folder, log=print):
        self.dir = folder
        self.log = log
        self.roms = {}            # rom -> [(rank, path)]
        self.titles = {}          # normalised title / titre normalisé -> [(rank, path)]
        self.games = 0
        self._build()

    @staticmethod
    def _rank(system):
        s = system.lower()
        return ARCADE.index(s) if s in ARCADE else len(ARCADE)

    def _add(self, rom, title, rank, path):
        if rom:
            self.roms.setdefault(rom.lower(), []).append((rank, path))
        if title:
            self.titles.setdefault(norm(title), []).append((rank, path))

    def _build(self):
        base = os.path.join(self.dir, "roms")
        try:
            systems = sorted(n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n)))
        except OSError:
            return
        for system in systems:
            sdir = os.path.join(base, system)
            rank = self._rank(system)
            seen = set()
            gl = os.path.join(sdir, "gamelist.xml")
            if os.path.isfile(gl):
                try:
                    for _, el in ET.iterparse(gl, events=("end",)):
                        if el.tag != "game":
                            continue
                        path = (el.findtext("path") or "").strip()
                        rom = os.path.splitext(os.path.basename(path.replace("\\", "/")))[0]
                        name = (el.findtext("name") or "").strip()
                        for i, tag in enumerate(TAGS):
                            img = (el.findtext(tag) or "").strip()
                            if img:
                                full = os.path.normpath(os.path.join(sdir, img.replace("/", os.sep)))
                                self._add(rom, name, rank * 10 + i, full)
                                seen.add(rom.lower())
                        if rom:
                            self.games += 1
                        el.clear()
                except (ET.ParseError, OSError) as e:
                    self.log(tr(f"RetroBat : {system}\\gamelist.xml illisible ({e})",
                                f"RetroBat: cannot read {system}\\gamelist.xml ({e})"))
            idir = os.path.join(sdir, "images")
            try:
                names = os.listdir(idir)
            except OSError:
                continue
            for n in names:                    # scraped images that gamelist.xml does not name / non nommées
                stem, ext = os.path.splitext(n)
                m = _SUFFIX.match(stem)
                if not m or ext.lower() not in _IMG or m.group(1).lower() in seen:
                    continue
                i = TAGS.index(m.group(2).lower())
                self._add(m.group(1), "", rank * 10 + 5 + i, os.path.join(idir, n))

    def find(self, roms, title=""):
        """The logo for these romsets (the game, then its parent), else by its title. None when nothing.
        Le logo pour ces romsets (le jeu, puis son parent), sinon d'après son titre."""
        for rom in [r for r in roms if r]:
            for _, p in sorted(self.roms.get(rom.lower(), [])):
                if os.path.isfile(p):
                    return p
        if title:
            for _, p in sorted(self.titles.get(norm(title), [])):
                if os.path.isfile(p):
                    return p
        return None
