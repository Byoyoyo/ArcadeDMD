"""Learning tool that finds the RAM address of a value shown on screen (score, credits...).
Capture the RAM several times during a game, then type the value seen on each capture. The tool
looks for the bytes holding exactly those values, in every common format.

Outil d'apprentissage : retrouve l'adresse RAM d'une valeur affichée (score, crédits...).

Principe : pendant une partie, on capture la RAM plusieurs fois (Ctrl droit + D, ou
Tab > Options des plugins > ArcadeDMD > Capturer). Ensuite on indique pour chaque capture
la valeur visible à l'écran. L'outil cherche les octets qui contiennent exactement ces
valeurs, dans tous les formats courants (binaire, BCD, un chiffre par octet...).
"""

import glob
import json
import os
import re
import sys

from .i18n import tr

# (type plugin, nombre d'octets, multiplicateurs testés)
ENCODINGS = [
    ("bcd", 4, (10, 1, 100)), ("bcd", 3, (10, 1, 100)), ("bcd", 2, (1, 10)), ("bcd", 1, (1,)),
    ("bcd_le", 4, (10, 1)), ("bcd_le", 3, (10, 1)), ("bcd_le", 2, (1,)),
    ("be", 4, (1, 10, 100)), ("le", 4, (1, 10, 100)),
    ("be", 2, (1, 10)), ("le", 2, (1, 10)),
    ("u8", 1, (1,)),
    ("digits", 8, (1, 10)), ("digits", 7, (1, 10)), ("digits", 6, (1, 10)),
    ("digits_ascii", 8, (1, 10)), ("digits_ascii", 7, (1, 10)), ("digits_ascii", 6, (1, 10)),
]

# (French, English) pairs, picked with tr() when displayed
LABELS = {
    "bcd": ("BCD", "BCD"), "bcd_le": ("BCD (ordre inversé)", "BCD (reversed byte order)"),
    "be": ("binaire", "binary"), "le": ("binaire (ordre inversé)", "binary (reversed byte order)"),
    "u8": ("octet", "byte"), "digits": ("1 chiffre par octet", "1 digit per byte"),
    "digits_ascii": ("chiffres ASCII", "ASCII digits"),
}


def encode(value, kind, nbytes, mult):
    """Octets attendus en mémoire pour `value`, ou None si impossible."""
    if value < 0 or value % mult:
        return None
    v = value // mult
    if kind in ("bcd", "bcd_le"):
        digits = str(v)
        if len(digits) > nbytes * 2:
            return None
        digits = digits.rjust(nbytes * 2, "0")
        out = bytes(int(digits[i]) * 16 + int(digits[i + 1]) for i in range(0, len(digits), 2))
        return out[::-1] if kind == "bcd_le" else out
    if kind in ("u8", "be"):
        if v >= 256 ** nbytes:
            return None
        return v.to_bytes(nbytes, "big")
    if kind == "le":
        if v >= 256 ** nbytes:
            return None
        return v.to_bytes(nbytes, "little")
    if kind in ("digits", "digits_ascii"):
        s = str(v)
        if len(s) > nbytes:
            return None
        s = s.rjust(nbytes, "0")
        off = 0x30 if kind == "digits_ascii" else 0
        return bytes(int(c) + off for c in s)
    return None


def find_all(data, pattern):
    out = []
    i = data.find(pattern)
    while i != -1:
        out.append(i)
        i = data.find(pattern, i + 1)
    return out


class Snapshot:
    def __init__(self, json_path=None, meta=None, data=None):
        if json_path:
            with open(json_path, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
            stem = json_path[:-5]
            self.bin_path = stem + ".bin"
            self.bmp_path = stem + ".bmp"
            with open(self.bin_path, "rb") as f:
                self.data = f.read()
        else:                                   # capture encore en mémoire (apprentissage RetroArch)
            self.meta, self.data = meta or {}, data or b""
            self.bin_path = self.bmp_path = ""
        self.json_path = json_path
        self.ranges = self.meta.get("ranges", [])
        if isinstance(self.ranges, dict):   # liste vide encodée en {}
            self.ranges = []

    def layout(self):
        return tuple((r["start"], r["end"]) for r in self.ranges)

    def addr_of(self, offset):
        for r in self.ranges:
            if r["offset"] <= offset < r["offset"] + r["length"]:
                return r["start"] + (offset - r["offset"])
        return None

    def same_range(self, offset, n):
        for r in self.ranges:
            if r["offset"] <= offset and offset + n <= r["offset"] + r["length"]:
                return True
        return False

    def window(self, addr, size):
        """Position (début, fin) dans data des octets [addr, addr + size), coupée à la fin de leur zone mémoire."""
        for r in self.ranges:
            if r["start"] <= addr < r["start"] + r["length"]:
                lo = r["offset"] + addr - r["start"]
                return lo, min(lo + size, r["offset"] + r["length"])
        return None

    def zone(self, addr):
        """(premier, dernier) octet de la zone mémoire qui contient addr."""
        for r in self.ranges:
            if r["start"] <= addr < r["start"] + r["length"]:
                return r["start"], r["start"] + r["length"] - 1
        return None

    def dword(self, addr, big_endian=True):
        w = self.window(addr, 4)
        if w is None or w[1] - w[0] < 4:
            return None
        return int.from_bytes(self.data[w[0]:w[1]], "big" if big_endian else "little")

    def pointer(self, p, rng=None, big_endian=True):
        """Adresse rangée en p (pointeur 32 bits), si elle tombe dans la mémoire capturée."""
        v = self.dword(p, big_endian)
        if v is None:
            return None
        base = v & 0xFFFFFF
        if rng and not rng[0] <= base <= rng[1]:
            return None
        return base if self.window(base, 1) else None


# Objets qui changent de place en mémoire (combattants de Samurai Shodown, The Last Blade...) :
# le jeu garde leur adresse dans un pointeur. Une valeur rangée dans un tel objet n'a pas d'adresse
# fixe, on la cherche alors à un décalage constant depuis l'adresse lue au pointeur.
OBJ_WINDOW = 0x400


def is_p2(name):
    n = (name or "").lower()
    return "p2" in n or n.endswith("2")


def object_pointers(values):
    """Pointeurs d'objets déclarés dans le fichier du jeu (valeurs "ptr") : {adresse: {"range", "player"}}."""
    from .memvalues import parse_addr
    out = {}
    for name, d in (values or {}).items():
        if not isinstance(d, dict):
            continue
        p = parse_addr(d.get("ptr"))
        if p is None or p in out:
            continue
        rng = d.get("ptr_range")
        rng = (parse_addr(rng[0]), parse_addr(rng[1])) if isinstance(rng, list) and len(rng) == 2 else None
        out[p] = {"range": rng if rng and None not in rng else None, "player": "p2" if is_p2(name) else "p1"}
    return out


def object_bases(snaps, objects, big_endian=True):
    """{pointeur: [adresse de l'objet dans chaque capture]} pour les pointeurs valables dans toutes les captures."""
    out = {}
    for p, o in (objects or {}).items():
        bases = [s.pointer(p, o.get("range"), big_endian) for s in snaps]
        if bases and all(b is not None for b in bases):
            out[p] = bases
    return out


def objects_moved(snaps, objects, big_endian=True):
    """Un des objets a-t-il changé de place entre les captures (pointeurs pas prêts ignorés) ?"""
    for p, o in (objects or {}).items():
        if len({s.pointer(p, o.get("range"), big_endian) for s in snaps} - {None}) > 1:
            return True
    return False


def _in_window(snaps_values, pats, bases, nbytes):
    """Décalages où chaque capture contient sa valeur, comptés depuis l'adresse de l'objet dans cette capture."""
    offs = None
    for (snap, _), pat, b in zip(snaps_values, pats, bases):
        w = snap.window(b, OBJ_WINDOW + nbytes - 1)
        found = set()
        if w:
            i = snap.data.find(pat, w[0], w[1])
            while i != -1:
                found.add(i - w[0])
                i = snap.data.find(pat, i + 1, w[1])
        offs = found if offs is None else offs & found
        if not offs:
            return set()
    return offs or set()


def _search_all(snaps_values, objects=None, big_endian=True):
    results = []
    snaps = [s for s, _ in snaps_values]
    bases = object_bases(snaps, objects, big_endian)
    seen = {s.pointer(p, o.get("range"), big_endian) for s in snaps for p, o in (objects or {}).items()} - {None}
    for kind, nbytes, mults in ENCODINGS:
        for mult in mults:
            pats = [encode(v, kind, nbytes, mult) for _, v in snaps_values]
            if any(p is None for p in pats):
                continue
            common = None
            for snap, pat in zip(snaps, pats):
                addrs = set()
                for off in find_all(snap.data, pat):
                    if snap.same_range(off, nbytes):
                        a = snap.addr_of(off)
                        if a is not None:
                            addrs.add(a)
                common = addrs if common is None else (common & addrs)
                if not common:
                    break
            for a in sorted(common or []):
                r = {"addr": a, "type": kind, "bytes": nbytes, "mult": mult}
                # adresse fixe tombée dans un combattant pendant une capture : le jeu recycle cette mémoire,
                # la valeur peut y rester un moment après le round (Samurai Shodown II), puis repasser à 0
                if any(b <= a < b + OBJ_WINDOW for b in seen):
                    r["in_obj"] = True
                results.append(r)
            for p, bl in bases.items():
                for o in sorted(_in_window(snaps_values, pats, bl, nbytes)):
                    results.append({"ptr": p, "addr": o, "type": kind, "bytes": nbytes, "mult": mult,
                                    "ptr_range": objects[p].get("range")})
    return results


def moving_pointers(snaps, big_endian=True, exclude=(), limit=3000):
    """Pointeurs inconnus dont la valeur change d'une capture à l'autre (objets qui bougent) : {adresse: [bases]}."""
    out = {}
    first = snaps[0]
    for r in first.ranges:
        start, end = r["start"], r["start"] + r["length"] - 4
        for a in range(start + (start & 1), end + 1, 2):
            if a in exclude:
                continue
            bases = []
            for s in snaps:
                v = s.dword(a, big_endian)
                if v is None or v >> 24 or not s.window(v, 1):
                    break
                bases.append(v)
            else:
                if len(set(bases)) > 1:
                    out[a] = bases
                    if len(out) > limit:
                        return {}
    return out


def _search_moving(snaps_values, big_endian=True, exclude=(), most=6):
    """Dernier recours : valeur rangée dans un objet qui bouge, suivi par un pointeur inconnu du fichier du jeu.
    Seulement pour des valeurs assez grandes (score...) : un petit nombre se retrouve partout par hasard."""
    if max(v for _, v in snaps_values) < 100:
        return []
    snaps = [s for s, _ in snaps_values]
    ptrs = moving_pointers(snaps, big_endian, exclude)
    results, seen = [], set()
    for kind, nbytes, mults in ENCODINGS:
        if nbytes < 2:
            continue
        for mult in mults:
            pats = [encode(v, kind, nbytes, mult) for _, v in snaps_values]
            if any(p is None for p in pats):
                continue
            for p, bl in sorted(ptrs.items()):
                for o in sorted(_in_window(snaps_values, pats, bl, nbytes)):
                    spot = (kind, nbytes, mult, tuple(b + o for b in bl))     # même octets vus par un autre pointeur
                    if spot in seen:
                        continue
                    seen.add(spot)
                    results.append({"ptr": p, "addr": o, "type": kind, "bytes": nbytes, "mult": mult,
                                    "ptr_range": snaps[0].zone(bl[0]), "auto": True})
    places = {(r["ptr"], r["addr"] // 8) for r in results}
    return results if len(places) <= most else []          # trop de réponses : du hasard, pas un vrai score


WIDE_FIELDS = ("score", "record", "hi", "point", "top", "best")
# counted from 1 on the screen, often from 0 in memory (stage 1 kept as 0) / comptés à partir de 1 à l'écran, de 0 en mémoire
FROM_ONE = ("stage", "mission", "round", "level", "area", "loop")


def is_wide(field):
    """A score is wide (3-4 bytes), a counter short. "hi" stands for hiscore, not for hits (a chain is a short counter).
    / Un score est large, un compteur court ; « hi » veut dire hiscore, pas hits."""
    f = field.lower()
    return not f.startswith("hit") and any(k in f for k in WIDE_FIELDS)


def counts_from_one(field):
    f = field.lower()
    return any(f == k or f.startswith(k + "_") or f.startswith(k + "2") for k in FROM_ONE)


def rank(results, field, objects=None):
    """Trie les candidats : un score est en général large (3-4 octets), un compteur court.
    À codage égal : adresse fixe hors des combattants, puis l'objet du bon joueur, puis une adresse fixe
    tombée dans la mémoire d'un combattant (recyclée d'un round à l'autre)."""
    wide = is_wide(field)
    pref = {"bcd": 0, "be": 1, "u8": 1, "digits": 2, "digits_ascii": 3, "le": 4, "bcd_le": 5}
    # un petit compteur (vies, bombes...) est plutôt un octet simple, les crédits souvent en BCD
    small = {"u8": 0, "bcd": 1} if "credit" not in field.lower() else {"bcd": 0, "u8": 1}
    side = "p2" if is_p2(field) else "p1"

    def key(r):
        aligned = 0 if (r["bytes"] == 1 or r["addr"] % 2 == 0) else 1
        width = -r["bytes"] if wide else r["bytes"]
        p = small.get(r["type"], pref.get(r["type"], 9)) if (not wide and r["bytes"] == 1) else pref.get(r["type"], 9)
        if r.get("ptr") is None:
            where = 2 if r.get("in_obj") else 0
        else:
            where = 1 if ((objects or {}).get(r["ptr"]) or {}).get("player", side) == side else 3
        return (p, aligned, width, 0 if (r["mult"] == 10) == wide else 1, where, r.get("ptr") or 0, r["addr"])

    return sorted(results, key=key)


def _search_flag(snaps_values):
    """Something that is on or off (typed 1 or 0): a byte that is not 0 in every capture typed 1 and 0 in every capture
    typed 0, a timer or a counter as well as a true flag. Read 0 or 1 ("max": 1).
    / Un interrupteur tapé 1 ou 0 : un octet non nul dans les captures à 1, nul dans celles à 0, lu 0 ou 1."""
    first = snaps_values[0][0]
    if any(s.layout() != first.layout() for s, _ in snaps_values):
        return []
    on = [s.data for s, v in snaps_values if v]
    off = [s.data for s, v in snaps_values if not v]
    out = []
    for off_i in range(len(first.data)):
        if all(d[off_i] for d in on) and not any(d[off_i] for d in off):
            a = first.addr_of(off_i)
            if a is not None:
                out.append({"addr": a, "type": "u8", "bytes": 1, "mult": 1, "max": 1})
    return out if len(out) <= 400 else []


def search(snaps_values, field="score", objects=None, big_endian=True):
    """snaps_values : liste de (Snapshot, valeur). Retourne (candidats triés, note)."""
    res = _search_all(snaps_values, objects, big_endian)
    if {v for _, v in snaps_values} == {0, 1}:
        # on or off: the exact 1 and 0 first, then what is merely not 0 / allumé ou éteint : 1 et 0 exacts, puis non nul
        seen = {r["addr"] for r in res if r.get("ptr") is None}
        flags = [r for r in _search_flag(snaps_values) if r["addr"] not in seen]
        if flags:
            return rank(res, field, objects) + rank(flags, field, objects), tr(
                "(allumé ou éteint : ArcadeDMD lit 1 quand l'octet n'est pas à 0)", "(on or off: ArcadeDMD reads 1 when the byte is not 0)")
    if not res and counts_from_one(field) and all(v >= 1 for _, v in snaps_values):
        # stage 1 kept as 0: the game file adds 1 / stage 1 gardé à 0 : le fichier du jeu ajoute 1
        res = _search_all([(s, v - 1) for s, v in snaps_values], objects, big_endian)
        if res:
            for r in res:
                r["add"] = 1
            return rank(res, field, objects), tr(f"(le jeu compte à partir de 0 : 0 pour {field} 1, ArcadeDMD ajoute 1)",
                                                 f"(the game counts from 0: 0 for {field} 1, ArcadeDMD adds 1)")
    if not res and len({v for _, v in snaps_values}) >= 2:
        res = _search_moving(snaps_values, big_endian, exclude=set(objects or ()))
        if res:
            return rank(res, field, objects), tr("(trouvé dans une zone qui change de place, suivie par son pointeur)",
                                                 "(found in a moving area, tracked by its pointer)")
    if res or len(snaps_values) < 3:
        return rank(res, field, objects), ""
    # une capture a peut-être été prise pendant un changement : on tolère un écart
    found = []
    for i in range(len(snaps_values)):
        sub = snaps_values[:i] + snaps_values[i + 1:]
        if len({v for _, v in sub}) < 2:
            continue
        for r in _search_all(sub, objects, big_endian):
            if r not in found:
                found.append(r)
    note = tr("(trouvé en ignorant une capture : refais une capture pour confirmer)",
              "(found by ignoring one capture: take another capture to confirm)") if found else ""
    return rank(found, field, objects), note


def describe(r):
    m = (f" ×{r['mult']}" if r["mult"] != 1 else "") + (f" +{r['add']}" if r.get("add") else "") + (
        tr(" (lu 0 ou 1)", " (read 0 or 1)") if r.get("max") == 1 else "")
    label = tr(*LABELS[r["type"]]) if r["type"] in LABELS else r["type"]
    what = tr(f"{label} {r['bytes']} octet(s){m}", f"{label} {r['bytes']} byte(s){m}")
    if r.get("ptr") is not None:
        who = tr("zone qui change de place", "moving area") if r.get("auto") else tr("objet du combattant", "fighter's object")
        return tr(f"0x{r['ptr']:06X} +0x{r['addr']:X}  {what}   ({who}, suivi par le pointeur 0x{r['ptr']:06X})",
                  f"0x{r['ptr']:06X} +0x{r['addr']:X}  {what}   ({who}, tracked by pointer 0x{r['ptr']:06X})")
    if r.get("in_obj"):
        return tr(f"0x{r['addr']:06X}  {what}   (mémoire d'un combattant, recyclée d'un round à l'autre)",
                  f"0x{r['addr']:06X}  {what}   (a fighter's memory, reused from one round to the next)")
    return f"0x{r['addr']:06X}  {what}"


def to_config(r):
    kind = r["type"]
    if r.get("ptr") is not None:
        d = {"ptr": f"0x{r['ptr']:06X}", "addr": f"0x{r['addr']:X}"}
        rng = r.get("ptr_range")
        if rng:
            d["ptr_range"] = [f"0x{rng[0]:06X}", f"0x{rng[1]:06X}"]
    else:
        d = {"addr": f"0x{r['addr']:06X}"}
    if kind == "digits_ascii":
        d.update({"type": "digits", "bytes": r["bytes"], "digit_offset": "0x30"})
    elif kind in ("bcd", "bcd_le", "digits", "le", "be"):
        d.update({"type": kind, "bytes": r["bytes"]})
    else:
        d["type"] = kind
    if r["mult"] != 1:
        d["mult"] = r["mult"]
    if r.get("add"):
        d["add"] = r["add"]
    if r.get("max") is not None:
        d["max"] = r["max"]
    return d


# placeholder notes of games/*.json, in French or English ("à trouver avec learn.bat", "to find with learn.bat"...)
TO_FIND = ("à trouver", "to find", "to be found", "to learn")


def still_to_find(d):
    """Definition of games/*.json that is only a reminder: no address yet, or a note saying it is still to be found."""
    note = str(d.get("note") or "").lower()
    return not d.get("addr") or any(m in note for m in TO_FIND)


def ask(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ""


# noms français tapés par l'utilisateur -> noms utilisés dans games/*.json
ALIASES = {
    "vie": "lives", "vies": "lives", "bombe": "bombs", "bombes": "bombs", "grenades": "bombs",
    "munition": "ammo", "munitions": "ammo", "balles": "ammo", "arme": "weapon",
    "credit": "credits", "crédit": "credits", "crédits": "credits", "temps": "time", "chrono": "time",
    "anneau": "rings", "anneaux": "rings", "points": "score", "pts": "score",
    # joueur 2 : score2=800 ou scorej2=800, vies2=2...
    "score2": "score_p2", "scorej2": "score_p2", "score_j2": "score_p2", "j2": "score_p2", "p2": "score_p2",
    "vies2": "lives_p2", "viesj2": "lives_p2", "bombes2": "bombs_p2", "bombesj2": "bombs_p2",
    "score1": "score", "scorej1": "score", "j1": "score", "p1": "score",
    # match VS des King of Fighters : BEAT BY (victoires d'affilée) de chaque côté, 0 pour le CHALLENGER
    "beat1": "beat", "beatj1": "beat", "beatp1": "beat", "beatby": "beat",
    "beat2": "beat_p2", "beatj2": "beat_p2", "beatp2": "beat_p2", "beatby2": "beat_p2",
    # English names. score, lives, bombs, ammo, credits, time, weapon, prisoners, health, beat, rings, record
    # and their *_p2 forms are already the names used in games/*.json and need no alias.
    "score_p1": "score", "scorep1": "score", "scorep2": "score_p2",
    "life": "lives", "lives1": "lives", "livesp1": "lives", "lives_p1": "lives",
    "lives2": "lives_p2", "livesp2": "lives_p2", "life2": "lives_p2",
    "bomb": "bombs", "grenade": "bombs", "bombs1": "bombs", "bombsp1": "bombs", "bombs_p1": "bombs",
    "bombs2": "bombs_p2", "bombsp2": "bombs_p2", "bomb2": "bombs_p2",
    "bullets": "ammo", "ammo1": "ammo", "ammop1": "ammo", "ammo_p1": "ammo", "ammo2": "ammo_p2", "ammop2": "ammo_p2",
    "weapon1": "weapon", "weapon_p1": "weapon", "weapon2": "weapon_p2", "weaponp2": "weapon_p2",
    "timer": "time", "ring": "rings",
    "prisoner": "prisoners", "pow": "prisoners", "pows": "prisoners", "prisonnier": "prisoners", "prisonniers": "prisoners",
    "hp": "health", "health1": "health", "healthp1": "health", "health_p1": "health",
    "health2": "health_p2", "healthp2": "health_p2", "hp2": "health_p2",
    "beat_p1": "beat", "beatby1": "beat",
    "hit": "hits", "chain": "hits", "chaine": "hits", "combo": "hits", "hit2": "hits_p2", "hits2": "hits_p2", "chain2": "hits_p2",
    "chaine2": "hits_p2", "combo2": "hits_p2",
    # Twinkle Star Sprites' PERFECT, 1 while the game shows it, 0 otherwise / 1 pendant que le jeu l'affiche, 0 sinon
    "parfait": "perfect", "perfect1": "perfect", "perfect2": "perfect_p2", "parfait2": "perfect_p2", "perfectj2": "perfect_p2",
    "hiscore": "record", "highscore": "record", "hi_score": "record", "high_score": "record", "hi": "record",
    "top": "record", "best": "record",
}


def parse_values(line):
    out = {}
    line = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", line)        # 16,060: English thousands separator
    for part in line.replace(",", " ").split():
        if "=" in part:
            k, v = part.split("=", 1)
            v = v.replace(".", "").replace(" ", "")
            if v.isdigit():
                k = k.strip().lower()
                out[ALIASES.get(k, k)] = int(v)
    return out


def open_image(path):
    if not os.path.exists(path):
        return
    try:
        if sys.platform == "win32":
            os.startfile(path)  # noqa: S606 (ouvre la visionneuse Windows)
    except OSError:
        pass


def _migrate_learned(root):
    """Old appris/ folder moved to learned/ once, before the learning tool uses it."""
    from . import learned
    learned.migrate(root)


def run(root, game=None, answers=None, write=None, show=True, pick_interactive=False, new_cfg=None):
    """answers : dict {numéro de capture: {champ: valeur}} (valeurs déjà connues).
    pick_interactive : demander quand même le choix des candidats (mode RetroArch)."""
    _migrate_learned(root)
    base = os.path.join(root, "runtime", "learn")
    if not os.path.isdir(base):
        print(tr("Aucune capture trouvée. Lance un jeu dans MAME et appuie sur Ctrl droit + D, "
                 "ou lance d'abord le jeu dans RetroArch (voir README.fr.md, sections 5 et 7).",
                 "No capture found. Start a game in MAME and press Right Ctrl + D, "
                 "or start the game in RetroArch first (see README.md, sections 5 and 7)."))
        return 1
    games = sorted(d for d in os.listdir(base) if glob.glob(os.path.join(base, d, "snap_*.json")))
    if not games:
        print(tr("Aucune capture trouvée.", "No capture found."))
        return 1
    if game is None:
        if len(games) == 1:
            game = games[0]
        else:
            print(tr("Jeux avec des captures :", "Games with captures:"))
            for i, g in enumerate(games, 1):
                print(f"  {i}. {g}")
            c = ask(tr("Numéro du jeu : ", "Game number: ")).strip()
            game = games[int(c) - 1] if c.isdigit() and 0 < int(c) <= len(games) else games[0]
    snaps = [Snapshot(p) for p in sorted(glob.glob(os.path.join(base, game, "snap_*.json")))]
    if not snaps:
        print(tr(f"Pas de capture pour {game}.", f"No capture for {game}."))
        return 1
    layouts = {s.layout() for s in snaps}
    if len(layouts) > 1:
        print(tr("Attention : les captures n'ont pas toutes la même zone mémoire, seules les plus récentes sont gardées.",
                 "Warning: the captures do not all cover the same memory area, only the most recent ones are kept."))
        last = snaps[-1].layout()
        snaps = [s for s in snaps if s.layout() == last]

    cfg_path = os.path.join(root, "games", game + ".json")
    cfg = None
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    objects, big_endian = learn_context(root, cfg or new_cfg, snaps[-1].meta)

    print(tr(f"\n{len(snaps)} capture(s) pour {game}.", f"\n{len(snaps)} capture(s) for {game}."))
    stored = all(s.meta.get("source") == "retroarch" and s.meta.get("values") for s in snaps)
    if answers is None and stored:
        print(tr("Valeurs tapées pendant la partie, analysées de nouveau :", "Values typed during the game, analyzed again:"))
    elif answers is None:
        print(tr("Pour chaque capture, tape les valeurs lues sur l'image, par exemple :  score=16060 credits=3",
                 "For each capture, type the values shown in the picture, for example:  score=16060 credits=3"))
        print(tr("(Entrée vide = capture ignorée)\n", "(Enter alone = capture skipped)\n"))
    observations = {}
    for s in snaps:
        n = s.meta.get("n")
        if answers is not None:
            vals = answers.get(n, {})
        elif s.meta.get("source") == "retroarch" and isinstance(s.meta.get("values"), dict) and s.meta["values"]:
            vals = {k: v for k, v in s.meta["values"].items() if isinstance(v, int)}     # tapées pendant la partie
            print(tr(f"Capture {n} : ", f"Capture {n}: ") + ", ".join(f"{k}={v}" for k, v in vals.items()))
        else:
            if show:
                open_image(s.bmp_path)
            img = s.bmp_path if os.path.exists(s.bmp_path) else tr("(pas d image)", "(no image)")
            print(tr(f"Capture {n} : {img}", f"Capture {n}: {img}"))
            vals = parse_values(ask(tr("  valeurs : ", "  values: ")))
        for k, v in vals.items():
            observations.setdefault(k, []).append((s, v))

    if not observations:
        print(tr("Aucune valeur saisie.", "No value entered."))
        return 1

    chosen = {}
    for field, obs in observations.items():
        distinct = {v for _, v in obs}
        print(tr(f"\n=== {field} ({len(obs)} capture(s), {len(distinct)} valeur(s) différente(s)) ===",
                 f"\n=== {field} ({len(obs)} capture(s), {len(distinct)} different value(s)) ==="))
        if len(distinct) < 2:
            print(tr("  Il faut au moins deux captures avec des valeurs différentes pour ce champ.",
                     "  This field needs at least two captures with different values."))
            continue
        res, note = search(obs, field, objects, big_endian)
        if note:
            print("  " + note)
        spec = (((cfg or new_cfg or {}).get("memory") or {}).get("values") or {}).get(field)
        bad = [a for a in (spec.get("not_learned") or [])] if isinstance(spec, dict) else []
        if bad and res:
            from .learned import _addr
            right = _addr(spec.get("addr")) if spec.get("addr") else None        # the game file's own: kept / gardée
            far = [r for r in res if r.get("ptr") is not None or r["addr"] == right
                   or all(abs(r["addr"] - (_addr(a) or -99)) >= 4 for a in bad)]
            if len(far) < len(res):
                print(tr(f"  {', '.join(bad)} laissé de côté : le jeu n'y garde pas « {field} » (voir games/{game}.json).",
                         f"  {', '.join(bad)} left aside: the game does not keep \"{field}\" there (see games/{game}.json)."))
            res = far
        if not res:
            print(tr("  Rien trouvé. Vérifie les valeurs saisies, ou capture à des moments où la valeur a changé.",
                     "  Nothing found. Check the values you typed, or capture at moments when the value has changed."))
            continue
        if objects and any(r.get("ptr") in objects for r in res[:3]) and not objects_moved([s for s, _ in obs], objects, big_endian):
            print(tr("  Les combattants sont restés à la même place pendant ces captures. Elles viennent sans doute",
                     "  The fighters stayed in the same place during these captures. They probably come"))
            print(tr("  du même combat. Pour être sûr, refais l'apprentissage avec une capture dans le combat suivant.",
                     "  from the same fight. To be sure, learn again with a capture in the next fight."))
        # regroupe les candidats qui désignent la même zone (ex. 1, 2 ou 4 octets au même endroit)
        clusters = []
        for r in res:
            for c in clusters:
                b = c[0]
                if r.get("ptr") == b.get("ptr") and r["addr"] < b["addr"] + 4 and b["addr"] < r["addr"] + r["bytes"] + 3:
                    c.append(r)
                    break
            else:
                clusters.append([r])
        res = [c[0] for c in clusters]
        for i, r in enumerate(res[:12], 1):
            more = len(clusters[i - 1]) - 1
            alt = tr(f"   (+{more} variante(s) au même endroit)", f"   (+{more} variant(s) at the same place)") if more else ""
            print(f"  {i}. {describe(r)}{alt}")
        if len(res) > 12:
            print(tr(f"  ... {len(res) - 12} autre(s)", f"  ... {len(res) - 12} more"))
        if len(res) == 1:
            print(tr("  Une seule zone mémoire correspond : c'est quasi certainement la bonne.",
                     "  Only one memory area matches: it is almost certainly the right one."))
        elif len(res) <= 3:
            print(tr("  Peu de candidats : le 1er est le plus probable. Une capture de plus permet de trancher.",
                     "  Few candidates: the 1st is the most likely. One more capture will settle it."))
        else:
            print(tr("  Trop de candidats : fais une ou deux captures de plus avec une valeur différente.",
                     "  Too many candidates: take one or two more captures with a different value."))
        pick = res[0] if len(res) <= 3 else None
        if answers is None or pick_interactive:
            default = "1" if pick else tr("aucun", "none")
            c = ask(tr(f"  Numéro à enregistrer pour « {field} » (Entrée = {default}) : ",
                       f'  Number to save for "{field}" (Enter = {default}): ')).strip()
            if c.isdigit() and 0 < int(c) <= len(res):
                pick = res[int(c) - 1]
            elif c:
                pick = None
        if pick:
            chosen[field] = to_config(pick)

    if not chosen:
        return 0
    print(tr("\nÀ enregistrer :", "\nTo save:"))
    for k, v in chosen.items():
        print(f"  {k}: {json.dumps(v)}")
    created = False
    if cfg is None and new_cfg is not None:
        cfg = new_cfg
        created = True
        if cfg.get("scene_from"):
            print(tr(f"(nouveau fichier games/{game}.json, avec la scène de {cfg['scene_from']}.json)",
                     f"(new file games/{game}.json, with the scene from {cfg['scene_from']}.json)"))
        else:
            print(tr(f"(nouveau fichier games/{game}.json, la scène générique sera utilisée)",
                     f"(new file games/{game}.json, the generic scene will be used)"))
    if cfg is None:
        meta = snaps[-1].meta
        cfg = {"title": meta.get("description", game),
               "match": [{"system": [meta.get("system", game)]}],
               "memory": {"cpu": meta.get("cpu", ":maincpu"), "values": {}}}
        tkey = meta.get("template")
        if tkey and tkey in (all_games := load_games(root)):
            apply_template(cfg, all_games, tkey, meta.get("system", game))
            print(tr(f"(nouveau fichier games/{game}.json, avec la scène de {tkey}.json)",
                     f"(new file games/{game}.json, with the scene from {tkey}.json)"))
        else:
            print(tr(f"(nouveau fichier games/{game}.json, la scène générique sera utilisée)",
                     f"(new file games/{game}.json, the generic scene will be used)"))
    prompt = tr(f"Écrire dans games/{game}.json ? (O/n) ", f"Write to games/{game}.json? (Y/n) ")
    do_write = write if write is not None else ask(prompt).strip().lower() in ("", "o", "oui", "y", "yes")
    if do_write:
        mem = cfg.setdefault("memory", {})
        vals = mem.setdefault("values", {})
        for k, v in chosen.items():
            old = vals.get(k, {})
            note = old.get("note") if isinstance(old, dict) and not still_to_find(old) else None
            if isinstance(old, dict) and old.get("mame_only"):
                note = "copy kept by the game, found with learn.bat"     # lisible aussi avec RetroArch
            if v.get("ptr") and not (isinstance(old, dict) and old.get("ptr") == v["ptr"]):
                note = f"in a moving area, address read at {v['ptr']}, found with learn.bat"
            if v.get("ptr") and k.startswith("score"):
                # entre deux rounds l'objet est recréé : un 0 passager ne doit pas effacer le score
                v["hold_zero"] = old.get("hold_zero", 20) if isinstance(old, dict) else 20
            if isinstance(old, dict) and old.get("not_learned"):
                v["not_learned"] = old["not_learned"]                # still ruled out next time / toujours écartée
            vals[k] = v
            if note:
                vals[k]["note"] = note
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
            f.write("\n")
        try:          # copie de secours, remise en place après une mise à jour d'ArcadeDMD
            from . import learned
            learned.save(root, game, chosen, cfg.get("retroarch") if created else None)
        except OSError:
            pass
        if snaps[-1].meta.get("source") == "retroarch":
            print(tr("Enregistré. ArcadeDMD prend les nouvelles adresses tout seul, la dalle les affiche dans quelques secondes.",
                     "Saved. ArcadeDMD picks up the new addresses by itself, the panel shows them within a few seconds."))
        else:
            print(tr("Enregistré. Relance le jeu, les valeurs s'affichent aussi dans Tab > Options des plugins > ArcadeDMD.",
                     "Saved. Restart the game, the values also show in Tab > Plugin Options > ArcadeDMD."))
    return 0


# --------------------------------------------------------------------------
# apprentissage en direct pendant une partie RetroArch
# --------------------------------------------------------------------------

def learn_context(root, cfg, meta):
    """Pointeurs d'objets connus pour ce jeu (fichier du jeu et sa scène commune), et ordre des octets."""
    vals = dict(((cfg or {}).get("memory") or {}).get("values") or {})
    tkey = (cfg or {}).get("scene_from") or meta.get("template")
    if isinstance(tkey, str) and tkey:
        tmpl = load_games(root).get(tkey)
        if tmpl:
            from .memvalues import game_values
            merged = game_values(tmpl, meta.get("system", ""))
            merged.update(vals)
            vals = merged
    return object_pointers(vals), bool(meta.get("big_endian", True))


def load_games(root):
    games = {}
    for p in glob.glob(os.path.join(root, "games", "*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                games[os.path.basename(p)[:-5]] = json.load(f)
        except (OSError, ValueError):
            pass
    return games


def apply_template(cfg, games, tkey, system):
    """Nouveau fichier d'un jeu couvert par un modèle (neogeo.json) : titre, scène, adresses communes."""
    tmpl = games.get(tkey) or {}
    titles = tmpl.get("titles") if isinstance(tmpl.get("titles"), dict) else {}
    cfg["title"] = titles.get(system) or cfg.get("title") or system
    cfg["match"] = [{"system": [system]}]
    cfg["scene_from"] = tkey
    ra = tmpl.get("retroarch") if isinstance(tmpl.get("retroarch"), dict) else {}
    cfg["retroarch"] = dict({k: v for k, v in ra.items() if k in ("ram_base", "ram_size", "swap16", "big_endian")},
                            content=[system])
    mem = cfg.setdefault("memory", {})
    from .memvalues import game_values
    vals = game_values(tmpl, system)          # adresses communes + barres de vie connues pour ce jeu
    vals.update(mem.get("values") or {})
    mem["values"] = vals
    mem.setdefault("cpu", (tmpl.get("memory") or {}).get("cpu", ":maincpu"))
    return cfg


def safe_key(text):
    out = "".join(c if c.isalnum() else "_" for c in (text or "").lower()).strip("_")
    return out[:40] or "jeu"


def run_live_retroarch(root, client, st, game=None, inputs=None):
    """Captures prises au moment où l'on tape les valeurs vues à l'écran."""
    _migrate_learned(root)
    from .retroarch import game_title, layout_for, resolve
    games = load_games(root)
    key, spec, parent, own = resolve(games, st["content"], st["system"])
    if game and game in games:
        key, spec, parent, own = game, games[game], "", ""
    tkey = None
    if spec is not None and spec.get("fallback"):      # jeu couvert par neogeo.json : fichier à lui
        tkey, key, spec = key, None, None
    if not key:
        key = safe_key(st["content"])
    layout = layout_for(spec or games.get(tkey), st["system"])
    base = os.path.join(root, "runtime", "learn", key)
    os.makedirs(base, exist_ok=True)
    old = sorted(glob.glob(os.path.join(base, "snap_*")))
    if old:
        arch = os.path.join(base, "anciennes")
        os.makedirs(arch, exist_ok=True)
        for p in old:
            try:
                os.replace(p, os.path.join(arch, os.path.basename(p)))
            except OSError:
                pass
    title = own or game_title(spec or games.get(tkey), parent or st["content"])
    from .retroarch import explain_failure, find_core, too_old
    version = client.version()
    if too_old(version):
        print(tr(f"RetroArch {version} est trop ancien pour lire la mémoire des jeux. Il faut la version 1.19 ou plus récente.",
                 f"RetroArch {version} is too old to read game memory. Version 1.19 or later is needed."))
        return 1
    core = find_core(st["content"])
    if client.read(0, 1) is None:          # inutile de jouer si la mémoire ne se lit pas
        for line in explain_failure(client.last_reply, version, core):
            print(line)
        return 1
    what = tr(f"cœur {core['name']}", f"core {core['name']}") if core else tr(f"système {st['system']}", f"system {st['system']}")
    print(tr(f"Jeu RetroArch : {st['content']} ({what}), fichier games/{key}.json",
             f"RetroArch game: {st['content']} ({what}), file games/{key}.json"))
    print(tr("Joue, puis reviens dans cette fenêtre (Alt+Tab) quand une valeur est bien visible.",
             "Play, then come back to this window (Alt+Tab) when a value is clearly visible."))
    print(tr("RetroArch se met en pause tout seul quand sa fenêtre n'est plus active.",
             "RetroArch pauses by itself when its window is no longer active."))
    print(tr("Tape alors ce que tu vois, par exemple   score=1200 vies=2",
             "Then type what you see, for example   score=1200 lives=2"))
    print(tr("Retourne jouer, et recommence trois ou quatre fois avec des valeurs différentes.",
             "Go back to the game, and repeat three or four times with different values."))
    known = dict(((spec or {}).get("memory") or {}).get("values") or {})
    if not spec and tkey:
        from .memvalues import game_values
        known = game_values(games.get(tkey) or {}, st["content"], parent)
    objects = object_pointers(known)
    if objects:
        print(tr("Dans ce jeu, les combattants changent de place en mémoire à chaque combat.",
                 "In this game, the fighters move to a new place in memory at every fight."))
        print(tr("Fais des captures dans deux combats différents, par exemple deux dans le premier et deux dans le suivant.",
                 "Take captures in two different fights, for example two in the first one and two in the next."))
    print(tr("Entrée vide pour terminer.\n", "Press Enter alone to finish.\n"))
    answers = {}
    shots = []
    warned = False
    n = 0
    feed = iter(inputs) if inputs is not None else None
    while True:
        line = (next(feed, "") if feed is not None else ask(tr("Valeurs à l'écran : ", "Values on screen: "))).strip()
        if not line:
            if objects and len(shots) >= 2 and not warned and not objects_moved(shots, objects, layout.big_endian):
                warned = True
                print(tr("  Les combattants sont restés à la même place depuis la première capture.",
                         "  The fighters have stayed in the same place since the first capture."))
                print(tr("  Tes captures viennent sans doute toutes du même combat.",
                         "  Your captures probably all come from the same fight."))
                print(tr("  Fais encore une capture dans le combat suivant. Ou Entrée vide pour terminer quand même.",
                         "  Take one more capture in the next fight. Or press Enter alone to finish anyway."))
                continue
            break
        vals = parse_values(line)
        if not vals:
            print(tr("  Exemple de saisie :  score=1200 vies=2", "  Example:  score=1200 lives=2"))
            continue
        now = client.status()
        if not now or now.get("content") != st["content"]:
            print(tr("  RetroArch ne répond plus, ou le jeu a changé. Arrêt des captures.",
                     "  RetroArch no longer responds, or the game has changed. Stopping captures."))
            break
        if now.get("state") != "PAUSED":
            print(tr("  (le jeu n'était pas en pause, la capture peut être un peu décalée)",
                     "  (the game was not paused, the capture may be slightly off)"))
        data = layout.capture(client)
        if not data:
            for line in explain_failure(client.last_reply, version, core):
                print("  " + line)
            break
        n += 1
        stem = os.path.join(base, f"snap_{n:03d}")
        with open(stem + ".bin", "wb") as f:
            f.write(data)
        meta = {"n": n, "system": st["content"], "description": title, "source": "retroarch",
                "core": st["system"], "values": vals, "big_endian": layout.big_endian,
                "ranges": [{"start": layout.base, "end": layout.base + len(data) - 1, "offset": 0, "length": len(data)}]}
        with open(stem + ".json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=1, ensure_ascii=False)
        shots.append(Snapshot(meta=meta, data=data))
        answers[n] = vals
        typed = ", ".join(f"{k}={v}" for k, v in vals.items())
        print(tr(f"  Capture {n} enregistrée ({typed}).", f"  Capture {n} saved ({typed})."))
    if not answers:
        print(tr("Aucune capture.", "No captures."))
        return 1
    new_cfg = {"title": title, "match": [],
               "retroarch": {"content": [st["content"]], "ram_base": f"0x{layout.base:06X}",
                             "ram_size": f"0x{layout.size:X}", "swap16": layout.swap},
               "memory": {"values": {}}}
    if tkey:
        apply_template(new_cfg, games, tkey, st["content"])
    return run(root, key, answers=answers, show=False, pick_interactive=inputs is None, new_cfg=new_cfg,
               write=None if inputs is None else True)
