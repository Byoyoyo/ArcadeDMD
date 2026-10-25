"""Outil d'apprentissage : retrouve l'adresse RAM d'une valeur affichée (score, crédits...).

Principe : pendant une partie, on capture la RAM plusieurs fois (Ctrl droit + D, ou
Tab > Options des plugins > ArcadeDMD > Capturer). Ensuite on indique pour chaque capture
la valeur visible à l'écran. L'outil cherche les octets qui contiennent exactement ces
valeurs, dans tous les formats courants (binaire, BCD, un chiffre par octet...).
"""

import glob
import json
import os
import sys

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

LABELS = {
    "bcd": "BCD", "bcd_le": "BCD (ordre inversé)", "be": "binaire",
    "le": "binaire (ordre inversé)", "u8": "octet", "digits": "1 chiffre par octet",
    "digits_ascii": "chiffres ASCII",
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
    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            self.meta = json.load(f)
        self.json_path = json_path
        stem = json_path[:-5]
        self.bin_path = stem + ".bin"
        self.bmp_path = stem + ".bmp"
        with open(self.bin_path, "rb") as f:
            self.data = f.read()
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


def _search_all(snaps_values):
    results = []
    for kind, nbytes, mults in ENCODINGS:
        for mult in mults:
            common = None
            for snap, value in snaps_values:
                pat = encode(value, kind, nbytes, mult)
                if pat is None:
                    common = set()
                    break
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
                results.append({"addr": a, "type": kind, "bytes": nbytes, "mult": mult})
    return results


WIDE_FIELDS = ("score", "record", "hi", "point", "top", "best")


def rank(results, field):
    """Trie les candidats : un score est en général large (3-4 octets), un compteur court."""
    wide = any(k in field.lower() for k in WIDE_FIELDS)
    pref = {"bcd": 0, "be": 1, "u8": 1, "digits": 2, "digits_ascii": 3, "le": 4, "bcd_le": 5}

    def key(r):
        aligned = 0 if (r["bytes"] == 1 or r["addr"] % 2 == 0) else 1
        width = -r["bytes"] if wide else r["bytes"]
        return (pref.get(r["type"], 9), aligned, width, 0 if (r["mult"] == 10) == wide else 1, r["addr"])

    return sorted(results, key=key)


def search(snaps_values, field="score"):
    """snaps_values : liste de (Snapshot, valeur). Retourne (candidats triés, note)."""
    res = _search_all(snaps_values)
    if res or len(snaps_values) < 3:
        return rank(res, field), ""
    # une capture a peut-être été prise pendant un changement : on tolère un écart
    found = []
    for i in range(len(snaps_values)):
        sub = snaps_values[:i] + snaps_values[i + 1:]
        if len({v for _, v in sub}) < 2:
            continue
        for r in _search_all(sub):
            if r not in found:
                found.append(r)
    note = "(trouvé en ignorant une capture : refais une capture pour confirmer)" if found else ""
    return rank(found, field), note


def describe(r):
    m = f" ×{r['mult']}" if r["mult"] != 1 else ""
    return f"0x{r['addr']:06X}  {LABELS.get(r['type'], r['type'])} {r['bytes']} octet(s){m}"


def to_config(r):
    kind = r["type"]
    d = {"addr": f"0x{r['addr']:06X}"}
    if kind == "digits_ascii":
        d.update({"type": "digits", "bytes": r["bytes"], "digit_offset": "0x30"})
    elif kind in ("bcd", "bcd_le", "digits", "le", "be"):
        d.update({"type": kind, "bytes": r["bytes"]})
    else:
        d["type"] = kind
    if r["mult"] != 1:
        d["mult"] = r["mult"]
    return d


def ask(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ""


def parse_values(line):
    out = {}
    for part in line.replace(",", " ").split():
        if "=" in part:
            k, v = part.split("=", 1)
            v = v.replace(".", "").replace(" ", "")
            if v.isdigit():
                out[k.strip()] = int(v)
    return out


def open_image(path):
    if not os.path.exists(path):
        return
    try:
        if sys.platform == "win32":
            os.startfile(path)  # noqa: S606 (ouvre la visionneuse Windows)
    except OSError:
        pass


def run(root, game=None, answers=None, write=None, show=True):
    """answers : dict {numéro de capture: {champ: valeur}} pour l'usage non interactif."""
    base = os.path.join(root, "runtime", "learn")
    if not os.path.isdir(base):
        print("Aucune capture trouvée. Lance un jeu dans MAME et appuie sur Ctrl droit + D (voir le guide).")
        return 1
    games = sorted(d for d in os.listdir(base) if glob.glob(os.path.join(base, d, "snap_*.json")))
    if not games:
        print("Aucune capture trouvée.")
        return 1
    if game is None:
        if len(games) == 1:
            game = games[0]
        else:
            print("Jeux avec des captures :")
            for i, g in enumerate(games, 1):
                print(f"  {i}. {g}")
            c = ask("Numéro du jeu : ").strip()
            game = games[int(c) - 1] if c.isdigit() and 0 < int(c) <= len(games) else games[0]
    snaps = [Snapshot(p) for p in sorted(glob.glob(os.path.join(base, game, "snap_*.json")))]
    if not snaps:
        print(f"Pas de capture pour {game}.")
        return 1
    layouts = {s.layout() for s in snaps}
    if len(layouts) > 1:
        print("Attention : les captures n'ont pas toutes la même zone mémoire, seules les plus récentes sont gardées.")
        last = snaps[-1].layout()
        snaps = [s for s in snaps if s.layout() == last]

    cfg_path = os.path.join(root, "games", game + ".json")
    cfg = None
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

    print(f"\n{len(snaps)} capture(s) pour {game}.")
    print("Pour chaque capture, tape les valeurs lues sur l'image, par exemple :  score=16060 credits=3")
    print("(Entrée vide = capture ignorée)\n")
    observations = {}
    for s in snaps:
        n = s.meta.get("n")
        if answers is not None:
            vals = answers.get(n, {})
        else:
            if show:
                open_image(s.bmp_path)
            print(f"Capture {n} : {s.bmp_path if os.path.exists(s.bmp_path) else '(pas d image)'}")
            vals = parse_values(ask("  valeurs : "))
        for k, v in vals.items():
            observations.setdefault(k, []).append((s, v))

    if not observations:
        print("Aucune valeur saisie.")
        return 1

    chosen = {}
    for field, obs in observations.items():
        distinct = {v for _, v in obs}
        print(f"\n=== {field} ({len(obs)} capture(s), {len(distinct)} valeur(s) différente(s)) ===")
        if len(distinct) < 2:
            print("  Il faut au moins deux captures avec des valeurs différentes pour ce champ.")
            continue
        res, note = search(obs, field)
        if note:
            print("  " + note)
        if not res:
            print("  Rien trouvé. Vérifie les valeurs saisies, ou capture à des moments où la valeur a changé.")
            continue
        # regroupe les candidats qui désignent la même zone (ex. 1, 2 ou 4 octets au même endroit)
        clusters = []
        for r in res:
            for c in clusters:
                b = c[0]
                if r["addr"] < b["addr"] + 4 and b["addr"] < r["addr"] + r["bytes"] + 3:
                    c.append(r)
                    break
            else:
                clusters.append([r])
        res = [c[0] for c in clusters]
        for i, r in enumerate(res[:12], 1):
            alt = f"   (+{len(clusters[i - 1]) - 1} variante(s) au même endroit)" if len(clusters[i - 1]) > 1 else ""
            print(f"  {i}. {describe(r)}{alt}")
        if len(res) > 12:
            print(f"  ... {len(res) - 12} autre(s)")
        if len(res) == 1:
            print("  Une seule zone mémoire correspond : c'est quasi certainement la bonne.")
        elif len(res) <= 3:
            print("  Peu de candidats : le 1er est le plus probable. Une capture de plus permet de trancher.")
        else:
            print("  Trop de candidats : fais une ou deux captures de plus avec une valeur différente.")
        pick = res[0] if len(res) <= 3 else None
        if answers is None:
            c = ask(f"  Numéro à enregistrer pour « {field} » (Entrée = {'1' if pick else 'aucun'}) : ").strip()
            if c.isdigit() and 0 < int(c) <= len(res):
                pick = res[int(c) - 1]
            elif c:
                pick = None
        if pick:
            chosen[field] = to_config(pick)

    if not chosen:
        return 0
    print("\nÀ enregistrer :")
    for k, v in chosen.items():
        print(f"  {k}: {json.dumps(v)}")
    if cfg is None:
        cfg = {"title": snaps[-1].meta.get("description", game),
               "match": [{"system": [snaps[-1].meta.get("system", game)]}],
               "memory": {"cpu": snaps[-1].meta.get("cpu", ":maincpu"), "values": {}}}
        print(f"(nouveau fichier games/{game}.json, la scène générique sera utilisée)")
    do_write = write if write is not None else ask(f"Écrire dans games/{game}.json ? (O/n) ").strip().lower() in ("", "o", "oui", "y")
    if do_write:
        mem = cfg.setdefault("memory", {})
        vals = mem.setdefault("values", {})
        for k, v in chosen.items():
            old = vals.get(k, {})
            note = old.get("note") if isinstance(old, dict) else None
            vals[k] = v
            if note and "apprendre" not in note:
                vals[k]["note"] = note
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("Enregistré. Relance le jeu, les valeurs s'affichent aussi dans Tab > Options des plugins > ArcadeDMD.")
    return 0
