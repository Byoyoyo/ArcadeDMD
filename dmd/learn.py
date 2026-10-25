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
    # un petit compteur (vies, bombes...) est plutôt un octet simple, les crédits souvent en BCD
    small = {"u8": 0, "bcd": 1} if "credit" not in field.lower() else {"bcd": 0, "u8": 1}

    def key(r):
        aligned = 0 if (r["bytes"] == 1 or r["addr"] % 2 == 0) else 1
        width = -r["bytes"] if wide else r["bytes"]
        p = small.get(r["type"], pref.get(r["type"], 9)) if (not wide and r["bytes"] == 1) else pref.get(r["type"], 9)
        return (p, aligned, width, 0 if (r["mult"] == 10) == wide else 1, r["addr"])

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


# noms français tapés par l'utilisateur -> noms utilisés dans games/*.json
ALIASES = {
    "vie": "lives", "vies": "lives", "bombe": "bombs", "bombes": "bombs", "grenades": "bombs",
    "munition": "ammo", "munitions": "ammo", "balles": "ammo", "arme": "weapon",
    "credit": "credits", "crédit": "credits", "crédits": "credits", "temps": "time", "chrono": "time",
    "anneau": "rings", "anneaux": "rings", "points": "score", "pts": "score",
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

    print(f"\n{len(snaps)} capture(s) pour {game}.")
    if answers is None:
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
            vals[k] = v
            if note and "apprendre" not in note:
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
    print("Entrée vide pour terminer.\n")
    answers = {}
    n = 0
    feed = iter(inputs) if inputs is not None else None
    while True:
        line = (next(feed, "") if feed is not None else ask("Valeurs à l'écran : ")).strip()
        if not line:
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
                "core": st["system"], "values": vals,
                "ranges": [{"start": layout.base, "end": layout.base + len(data) - 1, "offset": 0, "length": len(data)}]}
        with open(stem + ".json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=1, ensure_ascii=False)
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
