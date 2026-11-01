"""Reads the cheats of MAME (1.31) for the tools that build the game files.

The cheat collection of MAME (mamecheat.co.uk, its cheat.7z holds one XML file per game) is where the cheats of
FinalBurn Neo come from, and it often knows more: the credits of the CV1000 games, the lives and the bombs of games
FinalBurn Neo has no cheats for, the versions of a game that keep their values elsewhere. This module reads it in the
shape of the FinalBurn Neo cheats (cps_games.cheats): the name as FinalBurn Neo writes it ("Infinite Lives PL1" for
MAME's "P1 Infinite Lives"), each choice with what it writes in RAM, byte by byte, and "src" to say where it comes from.
Only plain writes in RAM are kept (maincpu.pb/pw/pd@address=value): a cheat that patches the program, waits for a
condition or copies a value is left out. The values of MAME's cheats are hexadecimal, as in its debugger.

Lit les codes de triche de MAME dans la forme de ceux de FinalBurn Neo : le nom comme FinalBurn Neo l'écrit, chaque
choix avec ce qu'il écrit en RAM, octet par octet. Seules les écritures simples en RAM sont gardées.

The source is a folder of the XML files (cheat.7z extracted with 7-Zip), or cheat.7z itself when py7zr is installed
(pip install py7zr). / La source : un dossier des fichiers XML, ou cheat.7z lui-même avec py7zr.
"""
import os
import re
import xml.etree.ElementTree as ET

SRC = "MAME cheat database"
WRITE = re.compile(r"^\s*(?::?maincpu)\.p([bwdq])@([0-9A-Fa-f]+)\s*=\s*(.+?)\s*$")
EXPR = re.compile(r"^\(?\s*(param|[0-9A-Fa-f]+)\s*(?:([+-])\s*([0-9A-Fa-f]+))?\s*\)?$", re.I)
SIZE = {"b": 1, "w": 2, "d": 4, "q": 8}


def fbneo_name(desc):
    """MAME's "P1 Infinite Lives" as FinalBurn Neo writes it, "Infinite Lives PL1". / Le nom à la façon de FinalBurn Neo."""
    desc = " ".join(desc.split())
    m = re.match(r"^P([12])\s+(.+)$", desc)
    return f"{m.group(2)} PL{m.group(1)}" if m else desc


def evaluate(expr, param=None):
    """A value of a cheat: a hexadecimal number, param, or param plus or minus a number. None for anything else (a value
    read elsewhere, a formula). / Une valeur : un nombre hexadécimal, param, ou param plus ou moins un nombre."""
    m = EXPR.match(expr.strip())
    if not m:
        return None
    if m.group(1).lower() == "param":
        if param is None:
            return None
        v = param
    else:
        v = int(m.group(1), 16)
    if m.group(2):
        k = int(m.group(3), 16)
        v = v + k if m.group(2) == "+" else v - k
    return v


def parse(text):
    """[{"name", "options": [{"n", "label", "triples": [(0, address, byte)...]}], "src"}] of one XML file of MAME."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []
    out = []
    for ch in root.iter("cheat"):
        desc = (ch.get("desc") or "").strip()
        if not desc:
            continue
        scripts = {s.get("state", "run"): s for s in ch.findall("script")}
        script = scripts.get("run") or scripts.get("on") or scripts.get("change")
        if script is None:
            continue
        writes = []
        for a in script.findall("action"):
            if a.get("condition") or not a.text:
                continue
            m = WRITE.match(a.text)
            if m:
                writes.append((SIZE[m.group(1).lower()], int(m.group(2), 16), m.group(3)))
        if not writes:
            continue
        par = ch.find("parameter")
        if par is None:
            choices = [(1, "Enabled", None)]
        else:
            items = par.findall("item")
            if items:
                choices = []
                for i, it in enumerate(items):
                    try:
                        choices.append((i + 1, (it.text or "").strip(), int(it.get("value", "0"), 0)))
                    except ValueError:
                        continue
            else:
                try:
                    lo, hi = int(par.get("min", "0"), 0), int(par.get("max", "0"), 0)
                    step = max(1, int(par.get("step", "1"), 0))
                except ValueError:
                    continue
                choices = [(i + 1, str(v), v) for i, v in enumerate(range(lo, hi + 1, step))][:256]
        options = []
        for n, label, param in choices:
            triples = []
            for size, addr, expr in writes:
                v = evaluate(expr, param)
                if v is None:
                    triples = []
                    break
                v &= (1 << (8 * size)) - 1
                triples += [(0, addr + i, (v >> (8 * (size - 1 - i))) & 0xFF) for i in range(size)]
            if triples:
                options.append({"n": n, "label": label, "triples": triples})
        if options:
            out.append({"name": fbneo_name(desc), "options": options, "src": SRC})
    return out


class MameCheats:
    """The cheats of MAME, game by game, from a folder of XML files or from cheat.7z. / Les codes de MAME, jeu par jeu."""

    def __init__(self, path):
        self.path = path or ""
        self.texts = {}
        self.cache = {}
        self.archive = bool(self.path) and os.path.isfile(self.path) and self.path.lower().endswith(".7z")

    def preload(self, names):
        """Reads the files of these games out of cheat.7z at once (one pass over the archive, it is solid).
        / Lit d'un coup les fichiers de ces jeux dans cheat.7z."""
        if not self.archive:
            return
        import py7zr
        want = {n + ".xml" for n in names if n + ".xml" not in self.texts}
        if not want:
            return
        with py7zr.SevenZipFile(self.path, "r") as z:
            have = want & set(z.getnames())
        if not have:
            return
        with py7zr.SevenZipFile(self.path, "r") as z:
            for name, bio in (z.read(targets=sorted(have)) or {}).items():
                self.texts[name] = bio.read().decode("utf-8", "replace")

    def get(self, name):
        if name in self.cache:
            return self.cache[name]
        text = None
        if self.archive:
            text = self.texts.get(name + ".xml")
        elif self.path:
            try:
                with open(os.path.join(self.path, name + ".xml"), encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                text = None
        cs = parse(text) if text else []
        self.cache[name] = cs
        return cs


def merge(fbneo, mame):
    """The cheats of FinalBurn Neo, then those of MAME that FinalBurn Neo does not have (same name).
    / Les codes de FinalBurn Neo, puis ceux de MAME qu'il n'a pas (même nom)."""
    have = {c["name"].lower() for c in fbneo}
    return list(fbneo) + [c for c in mame if c["name"].lower() not in have]
