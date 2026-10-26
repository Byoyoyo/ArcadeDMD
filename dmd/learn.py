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


def rank(results, field, objects=None):
    """Trie les candidats : un score est en général large (3-4 octets), un compteur court.
    À codage égal : adresse fixe hors des combattants, puis l'objet du bon joueur, puis une adresse fixe
    tombée dans la mémoire d'un combattant (recyclée d'un round à l'autre)."""
    wide = any(k in field.lower() for k in WIDE_FIELDS)
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


def search(snaps_values, field="score", objects=None, big_endian=True):
    """snaps_values : liste de (Snapshot, valeur). Retourne (candidats triés, note)."""
    res = _search_all(snaps_values, objects, big_endian)
    if not res and len({v for _, v in snaps_values}) >= 2:
        res = _search_moving(snaps_values, big_endian, exclude=set(objects or ()))
        if res:
            return rank(res, field, objects), "(trouvé dans une zone qui change de place, suivie par son pointeur)"
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
    note = "(trouvé en ignorant une capture : refais une capture pour confirmer)" if found else ""
    return rank(found, field, objects), note


def describe(r):
    m = f" ×{r['mult']}" if r["mult"] != 1 else ""
    what = f"{LABELS.get(r['type'], r['type'])} {r['bytes']} octet(s){m}"
    if r.get("ptr") is not None:
        who = "zone qui change de place" if r.get("auto") else "objet du combattant"
        return f"0x{r['ptr']:06X} +0x{r['addr']:X}  {what}   ({who}, suivi par le pointeur 0x{r['ptr']:06X})"
    if r.get("in_obj"):
        return f"0x{r['addr']:06X}  {what}   (mémoire d'un combattant, recyclée d'un round à l'autre)"
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
    return d


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
}


def parse_values(line):
    out = {}
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


def run(root, game=None, answers=None, write=None, show=True, pick_interactive=False, new_cfg=None):
    """answers : dict {numéro de capture: {champ: valeur}} (valeurs déjà connues).
    pick_interactive : demander quand même le choix des candidats (mode RetroArch)."""
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
    objects, big_endian = learn_context(root, cfg or new_cfg, snaps[-1].meta)

    print(f"\n{len(snaps)} capture(s) pour {game}.")
    stored = all(s.meta.get("source") == "retroarch" and s.meta.get("values") for s in snaps)
    if answers is None and stored:
        print("Valeurs tapées pendant la partie, analysées de nouveau :")
    elif answers is None:
        print("Pour chaque capture, tape les valeurs lues sur l'image, par exemple :  score=16060 credits=3")
        print("(Entrée vide = capture ignorée)\n")
    observations = {}
    for s in snaps:
        n = s.meta.get("n")
        if answers is not None:
            vals = answers.get(n, {})
        elif s.meta.get("source") == "retroarch" and isinstance(s.meta.get("values"), dict) and s.meta["values"]:
            vals = {k: v for k, v in s.meta["values"].items() if isinstance(v, int)}     # tapées pendant la partie
            print(f"Capture {n} : " + ", ".join(f"{k}={v}" for k, v in vals.items()))
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
        res, note = search(obs, field, objects, big_endian)
        if note:
            print("  " + note)
        if not res:
            print("  Rien trouvé. Vérifie les valeurs saisies, ou capture à des moments où la valeur a changé.")
            continue
        if objects and any(r.get("ptr") in objects for r in res[:3]) and not objects_moved([s for s, _ in obs], objects, big_endian):
            print("  Les combattants sont restés à la même place pendant ces captures. Elles viennent sans doute")
            print("  du même combat. Pour être sûr, refais l'apprentissage avec une capture dans le combat suivant.")
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
        if answers is None or pick_interactive:
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
    created = False
    if cfg is None and new_cfg is not None:
        cfg = new_cfg
        created = True
        if cfg.get("scene_from"):
            print(f"(nouveau fichier games/{game}.json, avec la scène de {cfg['scene_from']}.json)")
        else:
            print(f"(nouveau fichier games/{game}.json, la scène générique sera utilisée)")
    if cfg is None:
        meta = snaps[-1].meta
        cfg = {"title": meta.get("description", game),
               "match": [{"system": [meta.get("system", game)]}],
               "memory": {"cpu": meta.get("cpu", ":maincpu"), "values": {}}}
        tkey = meta.get("template")
        if tkey and tkey in (all_games := load_games(root)):
            apply_template(cfg, all_games, tkey, meta.get("system", game))
            print(f"(nouveau fichier games/{game}.json, avec la scène de {tkey}.json)")
        else:
            print(f"(nouveau fichier games/{game}.json, la scène générique sera utilisée)")
    do_write = write if write is not None else ask(f"Écrire dans games/{game}.json ? (O/n) ").strip().lower() in ("", "o", "oui", "y")
    if do_write:
        mem = cfg.setdefault("memory", {})
        vals = mem.setdefault("values", {})
        for k, v in chosen.items():
            old = vals.get(k, {})
            note = old.get("note") if isinstance(old, dict) else None
            if isinstance(old, dict) and old.get("mame_only"):
                note = "copie gardée par le jeu, trouvée avec apprendre.bat"     # lisible aussi avec RetroArch
            if v.get("ptr") and not (isinstance(old, dict) and old.get("ptr") == v["ptr"]):
                note = f"dans une zone qui change de place, adresse lue en {v['ptr']}, trouvé avec apprendre.bat"
            if v.get("ptr") and k.startswith("score"):
                # entre deux rounds l'objet est recréé : un 0 passager ne doit pas effacer le score
                v["hold_zero"] = old.get("hold_zero", 20) if isinstance(old, dict) else 20
            vals[k] = v
            if note and "à trouver" not in note:
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
            print("Enregistré. ArcadeDMD prend les nouvelles adresses tout seul, la dalle les affiche dans quelques secondes.")
        else:
            print("Enregistré. Relance le jeu, les valeurs s'affichent aussi dans Tab > Options des plugins > ArcadeDMD.")
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
    from .retroarch import game_title, layout_for, match_game
    games = load_games(root)
    key, spec = match_game(games, st["content"], st["system"])
    if game and game in games:
        key, spec = game, games[game]
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
    title = game_title(spec or games.get(tkey), st["content"])
    from .retroarch import explain_failure, find_core, too_old
    version = client.version()
    if too_old(version):
        print(f"RetroArch {version} est trop ancien pour lire la mémoire des jeux. Il faut la version 1.19 ou plus récente.")
        return 1
    core = find_core(st["content"])
    if client.read(0, 1) is None:          # inutile de jouer si la mémoire ne se lit pas
        for line in explain_failure(client.last_reply, version, core):
            print(line)
        return 1
    what = f"cœur {core['name']}" if core else f"système {st['system']}"
    print(f"Jeu RetroArch : {st['content']} ({what}), fichier games/{key}.json")
    print("Joue, puis reviens dans cette fenêtre (Alt+Tab) quand une valeur est bien visible.")
    print("RetroArch se met en pause tout seul quand sa fenêtre n'est plus active.")
    print("Tape alors ce que tu vois, par exemple   score=1200 vies=2")
    print("Retourne jouer, et recommence trois ou quatre fois avec des valeurs différentes.")
    known = dict(((spec or {}).get("memory") or {}).get("values") or {})
    if not spec and tkey:
        from .memvalues import game_values
        known = game_values(games.get(tkey) or {}, st["content"])
    objects = object_pointers(known)
    if objects:
        print("Dans ce jeu, les combattants changent de place en mémoire à chaque combat.")
        print("Fais des captures dans deux combats différents, par exemple deux dans le premier et deux dans le suivant.")
    print("Entrée vide pour terminer.\n")
    answers = {}
    shots = []
    warned = False
    n = 0
    feed = iter(inputs) if inputs is not None else None
    while True:
        line = (next(feed, "") if feed is not None else ask("Valeurs à l'écran : ")).strip()
        if not line:
            if objects and len(shots) >= 2 and not warned and not objects_moved(shots, objects, layout.big_endian):
                warned = True
                print("  Les combattants sont restés à la même place depuis la première capture.")
                print("  Tes captures viennent sans doute toutes du même combat.")
                print("  Fais encore une capture dans le combat suivant. Ou Entrée vide pour terminer quand même.")
                continue
            break
        vals = parse_values(line)
        if not vals:
            print("  Exemple de saisie :  score=1200 vies=2")
            continue
        now = client.status()
        if not now or now.get("content") != st["content"]:
            print("  RetroArch ne répond plus, ou le jeu a changé. Arrêt des captures.")
            break
        if now.get("state") != "PAUSED":
            print("  (le jeu n'était pas en pause, la capture peut être un peu décalée)")
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
        print(f"  Capture {n} enregistrée ({', '.join(f'{k}={v}' for k, v in vals.items())}).")
    if not answers:
        print("Aucune capture.")
        return 1
    new_cfg = {"title": title, "match": [],
               "retroarch": {"content": [st["content"]], "ram_base": f"0x{layout.base:06X}",
                             "ram_size": f"0x{layout.size:X}", "swap16": layout.swap},
               "memory": {"values": {}}}
    if tkey:
        apply_template(new_cfg, games, tkey, st["content"])
    return run(root, key, answers=answers, show=False, pick_interactive=inputs is None, new_cfg=new_cfg,
               write=None if inputs is None else True)
