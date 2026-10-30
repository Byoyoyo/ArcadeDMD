"""Builds the files of the Capcom CPS1, CPS2 and CPS3 games (games/<game>.json) from FinalBurn Neo.

From the list of FinalBurn Neo (src/burn/drv/capcom/d_cps1.cpp, d_cps2.cpp, d_cps2_custom.cpp, src/burn/drv/cps3/d_cps3.cpp)
each original game gets its file, with every version, bootleg and hack of it, for MAME as for RetroArch. From the cheat
database of FinalBurn Neo (FBNeo-cheats, cheats/<game>.ini) it takes what the cheats write: the health of each player
and its full value, the timer, the credits, the lives, the bombs, the super gauge, the characters and their names. The
genre of FinalBurn Neo picks the shared scene (games/cps_combat.json, cps_action.json, cps_shoot.json, cps_reflexion.json,
made here from the Neo Geo ones). A file that was changed by hand keeps its scene and what the tool does not make.

Construit les fichiers des jeux Capcom CPS1, CPS2 et CPS3 à partir de FinalBurn Neo : la liste des jeux avec leurs
versions, bootlegs et hacks, et ce qu'écrivent les codes de triche (vie, chrono, crédits, vies, bombes, jauge, persos).

usage: python tools/cps_games.py FBNEO_SOURCE_FOLDER FBNEO_CHEATS_FOLDER
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neogeo_sets import clean  # noqa: E402

TOOL = "tools/cps_games.py"
DRIVERS = ("src/burn/drv/capcom/d_cps1.cpp", "src/burn/drv/capcom/d_cps2.cpp", "src/burn/drv/capcom/d_cps2_custom.cpp",
           "src/burn/drv/cps3/d_cps3.cpp")
RA_CPS = {"ram_base": "0xFF0000", "ram_size": "0x10000", "swap16": True,
          "note": "FinalBurn Neo core: CPS work RAM from 0xFF0000 (64 KB), bytes swapped within 16-bit words"}
RA_CPS3 = {"ram_base": "0x2000000", "ram_size": "0x80000", "swap32": True,
           "note": "FinalBurn Neo core: CPS3 main RAM from 0x2000000 (512 KB), bytes reversed within 32-bit words"}
SCENES = [(("GBF_VSFIGHT",), "cps_combat"),
          (("GBF_VERSHOOT", "GBF_HORSHOOT"), "cps_shoot"),
          (("GBF_PUZZLE", "GBF_QUIZ", "GBF_MAHJONG", "GBF_MISC", "GBF_MINIGAMES"), "cps_reflexion")]
TEMPLATES = {"cps_combat": "neogeo_combat", "cps_action": "neogeo", "cps_shoot": "neogeo_shoot",
             "cps_reflexion": "neogeo_reflexion"}
PL = r"(?:pl|p|player ?)"
PATTERNS = {
    "time": r"^infinite time$",
    "credits": r"^infinite credits",
    "health": rf"^(?:select )?infinite (?:energy|health|vitality|life)(?: '?all'?| \((?:1st char(?:acter)?|active char)\))? {PL}1$",
    "health_p2": rf"^(?:select )?infinite (?:energy|health|vitality|life)(?: '?all'?| \((?:1st char(?:acter)?|active char)\))? {PL}2$",
    "_drain": rf"^(?:always have no energy|drain all energy now!?(?: \(active char\))?) {PL}1(?:/cpu)?$",
    "_drain_p2": rf"^(?:always have no energy|drain all energy now!?(?: \(active char\))?) {PL}2(?:/cpu)?$",
    # the counter itself, or the cheat that sets it to win the match with this round (Night Warriors)
    # le compteur lui-même, ou le code qui le règle pour gagner le match avec ce round
    "rounds": rf"^(?:rounds won always (?:set )?= 0|win this round to win match now!?) {PL}1$",
    "rounds_p2": rf"^(?:rounds won always (?:set )?= 0|win this round to win match now!?) {PL}2$",
    "lives": rf"^infinite lives {PL}1$",
    "lives_p2": rf"^infinite lives {PL}2$",
    "bombs": rf"^infinite (?:bombs|bomb stock|bomb) {PL}1$",
    "power": rf"^(?:infinite (?:power|super|super meter|super gauge)|always (?:have )?max(?:imum)? (?:power|super)(?: gauge)?) {PL}1$",
    "power_p2": rf"^(?:infinite (?:power|super|super meter|super gauge)|always (?:have )?max(?:imum)? (?:power|super)(?: gauge)?) {PL}2$",
    "_p1_chr": rf"^select (?:1st )?char(?:acter)?(?: \(active char\))?(?: now!)? {PL}1$",
    "_p2_chr": rf"^select (?:1st )?char(?:acter)?(?: \(active char\))?(?: now!)? {PL}2$",
}
PATTERNS = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}
BACKDROP = re.compile(r"^(?:select (?:permanent )?(?:background|backdrop)(?: now!?)?|background always =|select next stage now!?)$", re.I)


# ------------------------------------------------------------------ FinalBurn Neo list
def drivers(src):
    out = []
    for m in re.finditer(r"struct BurnDriver\w*\s+BurnDrv\w+\s*=\s*\{(.*?)\n\};", src, re.S):
        body = m.group(1)
        toks = re.findall(r'"((?:[^"\\]|\\.)*)"|\b(NULL)\b', body)
        vals = [a if a or not b else None for a, b in toks]
        flags = re.search(r"\b(BDF_[A-Z_]+(?:\s*\|\s*BDF_[A-Z_]+)*)", body)
        hw = re.search(r"\b(HARDWARE_[A-Z0-9_]+(?:\s*\|\s*HARDWARE_[A-Z0-9_]+)*)", body)
        genre = re.search(r"\b(GBF_[A-Z_]+(?:\s*\|\s*GBF_[A-Z_]+)*)", body)
        out.append({"name": vals[0], "parent": vals[1], "desc": (vals[5] or "").split("\\0")[0],
                    "flags": flags.group(1) if flags else "", "hw": hw.group(1) if hw else "",
                    "genre": genre.group(1) if genre else ""})
    return [d for d in out if "HARDWARE_CAPCOM_CPS" in d["hw"]]


def family(d):
    return "CPS3" if "CPS3" in d["hw"] else "CPS2" if "CPS2" in d["hw"] else "CPS1"


def scene_of(genre):
    for flags, scene in SCENES:
        if any(f in genre for f in flags):
            return scene
    return "cps_action"


# ------------------------------------------------------------------ cheat database
def cheats(path):
    """[{"name", "options": [{"n", "label", "triples": [(cpu, addr, value)...]}]}] of an FBNeo .ini."""
    try:
        with open(path, encoding="latin-1") as f:
            text = f.read()
    except OSError:
        return []
    out, cur = [], None
    for raw in text.splitlines():
        line = raw.strip()
        m = re.match(r'^cheat\s+"(.*)"', line)
        if m:
            cur = {"name": m.group(1).strip(), "options": []}
            out.append(cur)
            continue
        m = re.match(r'^(\d+)\s+"([^"]*)"\s*(,.*)?$', line) if cur is not None else None
        if m:
            vals = [int(x, 0) for x in re.findall(r"(0x[0-9A-Fa-f]+|\d+)", m.group(3) or "")]
            cur["options"].append({"n": int(m.group(1)), "label": m.group(2),
                                   "triples": [tuple(vals[i:i + 3]) for i in range(0, len(vals) - len(vals) % 3, 3)]})
    return out


def enabled(c):
    on = [o for o in c["options"] if o["n"] != 0 and o["triples"]]
    return on[0]["triples"] if on else []


def word(triples):
    """(address, bytes, full value) of what a cheat writes, two bytes when it writes two in a row."""
    if not triples:
        return None
    a0, v0 = triples[0][1], triples[0][2]
    if len(triples) > 1 and triples[1][1] == a0 + 1:
        return a0, 2, (v0 << 8) | triples[1][2]
    return a0, 1, v0


def bcd_like(v):
    return v not in (0x63, 0x3C, 0x5A, 0x64) and all(int(c, 16) <= 9 for c in f"{v:x}")


def visible(addr, fam):
    lo, size = (0x2000000, 0x80000) if fam == "CPS3" else (0xFF0000, 0x10000)
    return lo <= addr < lo + size


def value(addr, nbytes, fam, kind, note):
    v = {"addr": f"0x{addr:X}", "type": kind}
    if kind in ("bcd", "be") or nbytes > 1:
        v["bytes"] = nbytes
    v["note"] = note
    if not visible(addr, fam):
        v["mame_only"] = True                   # not in the RAM FinalBurn Neo gives RetroArch / hors de la RAM partagée
    return v


def short_name(label, most=11):
    """A character's name for the panel: no note in parentheses, at most 11 letters (CAPTAIN AMERICA -> C.AMERICA).
    / Le nom d'un personnage pour la dalle, 11 lettres au plus."""
    t = re.sub(r"\s*[\(\[].*?[\)\]]", "", label)
    t = re.sub(r"\s+", " ", t.replace("*", "")).strip(" -").upper()
    if len(t) > most and " " in t:
        words = t.split(" ")
        t = ".".join(w[0] for w in words[:-1]) + "." + words[-1]
    return t[:most] if len(t) > most else t


def names_of(c):
    """(address, {value: NAME}) of a Select Character cheat: the write whose value changes from one character to the next.
    / L'écriture dont la valeur change d'un personnage à l'autre."""
    opts = [o for o in c["options"] if o["n"] != 0 and o["triples"]]
    if len(opts) < 4:
        return None, None
    for i in range(min(len(o["triples"]) for o in opts)):
        addrs = [o["triples"][i][1] for o in opts]
        addr = max(set(addrs), key=addrs.count)
        same = [o for o in opts if o["triples"][i][1] == addr]
        if len(same) < len(opts) * 0.8 or len({o["triples"][i][2] for o in same}) < len(same) * 0.8:
            continue
        out = {}
        for o in same:
            label = short_name(o["label"])
            if label and str(o["triples"][i][2]) not in out:
                out[str(o["triples"][i][2])] = label
        return addr, out
    return None, None


def pair_names_of(c):
    """([address, address], {"a,b": NAME}) of a Select Character cheat that writes two bytes, the pair telling the character
    (a row and a column in Street Fighter III). / Deux octets dont la paire dit le personnage (ligne et colonne)."""
    opts = [o for o in c["options"] if o["n"] != 0 and len(o["triples"]) == 2]
    if len(opts) < 4 or len({tuple(t[1] for t in o["triples"]) for o in opts}) != 1:
        return None, None
    keys = [",".join(str(t[2]) for t in o["triples"]) for o in opts]
    if len(set(keys)) < len(keys) * 0.9:
        return None, None
    out = {}
    for o, k in zip(opts, keys):
        label = short_name(o["label"].strip("#"))
        if label and k not in out:
            out[k] = label
    return [t[1] for t in opts[0]["triples"]], out


def timer(t, fam, src):
    """("time", spec) when the Infinite Time cheat fills a whole two-digit timer, 99 in BCD or in binary. Otherwise it pins
    a part of it, one digit of a timer kept one digit per byte (Three Wonders, Cadillacs and Dinosaurs), the seconds of a
    clock (Ghouls'n Ghosts 1:35, Strider, Willow), the digits of a clock, a word, or a counter that is not the timer seen
    in the game (The Punisher shows TIME 23, its cheat writes 191). Then ("_time", spec), read only to see that the game
    runs, the panels do not show it.
    / Le chrono entier quand la triche le remplit (99). Sinon elle n'en fige qu'une partie (un chiffre, les secondes d'une
    horloge, un compteur qui n'est pas le chrono du jeu) : lu seulement pour voir que le jeu tourne, sans l'afficher."""
    addr, first = t[0][1], t[0][2]
    if first in (0x99, 0x63):
        kind = "bcd" if first == 0x99 else "u8"
        spec = value(addr, 1, fam, kind, f"timer ({src}, Infinite Time)")
        if kind == "u8":
            spec.pop("bytes", None)
        return "time", spec
    digits = 0
    for i, (_, a, x) in enumerate(t):            # digits written one per byte / des chiffres, un par octet
        if a != addr + i or x > 9:
            break
        digits += 1
    if digits >= 2:
        kind, n = "digits", digits
    elif len(t) == 2 and t[1][1] == addr + 1:    # a word, 999 in Janpai Puzzle Choukou / un mot de 16 bits
        kind, n = "be", 2
    else:
        kind, n = ("bcd" if bcd_like(first) else "u8"), 1
    writes = " ".join(f"{x:02X}" for _, _, x in t)
    spec = value(addr, n, fam, kind, f"part of the timer only ({src}, Infinite Time writes {writes}), read to see that "
                                     "the game runs, not shown")
    if kind == "u8":
        spec.pop("bytes", None)
    return "_time", spec


# full health of a game whose cheats only drain it, from a game of the same series / vie pleine d'un jeu de la même série
FULL = {"sf2": 0x90, "nwarr": 0x90}


def values_from_cheats(cs, fam, name=""):
    found = {}
    for c in cs:
        for key, pat in PATTERNS.items():
            if key not in found and pat.match(c["name"]):
                found[key] = c
    vals, derived, got = {}, {}, []
    src = "FBNeo cheat database"
    for key in ("health", "health_p2"):
        w = word(enabled(found[key])) if key in found else None
        drain = found.get("_drain" if key == "health" else "_drain_p2")
        if (not w or w[2] <= 0) and drain is not None and name in FULL and enabled(drain):
            w = (enabled(drain)[0][1], 1, FULL[name])
            found[key] = drain
        if w and w[2] > 0:
            addr, n, full = w
            v = value(addr, n, fam, "be" if n > 1 else "u8",
                      f"{'player 1' if key == 'health' else 'player 2'} health in %, full = 0x{full:X} ({src}, {found[key]['name']})")
            v.update({"mult": round(100.0 / full, 6), "round": 1, "min": 0, "max": 100})
            # gone below zero at a K.O. (Street Fighter II): 0xFF... reads an empty bar, not a full one
            # passée sous zéro au K.O. : 0xFF... se lit barre vide, pas pleine
            v["zero_from"] = f"0x{full + ((1 << (8 * n)) - full) // 2:X}"
            vals[key] = v
    for key in ("rounds", "rounds_p2"):              # rounds won, the markers under the bars / les rounds gagnés
        t = enabled(found[key]) if key in found else None
        if t:
            vals[key] = value(t[0][1], 1, fam, "u8", f"rounds won by {'player 1' if key == 'rounds' else 'player 2'} "
                                                     f"({src}, {found[key]['name']})")
    if "time" in found:
        t = enabled(found["time"])
        if t and t[0][2] > 0:
            key, spec = timer(t, fam, src)
            vals[key] = spec
    if "credits" in found:
        t = enabled(found["credits"])
        if t:
            kind = "bcd" if t[0][2] > 9 and bcd_like(t[0][2]) else "u8"
            vals["credits"] = value(t[0][1], 1, fam, kind, f"credits ({src}, {found['credits']['name']})")
    for key in ("lives", "lives_p2", "bombs"):
        if key in found:
            t = enabled(found[key])
            if t:
                vals[key] = value(t[0][1], 1, fam, "u8", f"{key.replace('_p2', ' of player 2')} ({src}, {found[key]['name']})")
    for key in ("power", "power_p2"):
        w = word(enabled(found[key])) if key in found else None
        if w and w[2] > 0:
            addr, n, full = w
            v = value(addr, n, fam, "be" if n > 1 else "u8",
                      f"super gauge of {'player 1' if key == 'power' else 'player 2'} in %, full = 0x{full:X} ({src})")
            v.update({"mult": round(100.0 / full, 6), "round": 1, "min": 0, "max": 100})
            vals[key] = v
    for key, out in (("_p1_chr", "p1_char"), ("_p2_chr", "p2_char")):
        if key in found:
            who = "player 1" if key == "_p1_chr" else "player 2 or computer"
            addr, names = names_of(found[key])
            if names:
                vals[key] = value(addr, 1, fam, "u8", f"{who} character ({src}, {found[key]['name']})")
                derived[out] = {"value": key, "names": names}
                continue
            addrs, names = pair_names_of(found[key])
            if names:                                # the character told by two bytes / le personnage dit par deux octets
                vals[key] = value(addrs[0], 1, fam, "u8", f"{who} character, first byte ({src}, {found[key]['name']})")
                vals[key + "2"] = value(addrs[1], 1, fam, "u8", f"{who} character, second byte ({src}, {found[key]['name']})")
                derived[out] = {"join": [key, key + "2"], "names": names}
    for k in vals:
        if not k.startswith("_"):
            got.append(k)
    if derived:
        got.append(f"{len(derived['p1_char']['names']) if 'p1_char' in derived else len(derived['p2_char']['names'])} characters")
    return vals, derived, got


# ------------------------------------------------------------------ stages of the fighting games / décors des jeux de combat
COUNTRIES = {"japan": ("JAPON", "JAPAN"), "usa": ("ÉTATS-UNIS", "USA"), "china": ("CHINE", "CHINA"), "hong kong": ("HONG KONG", "HONG KONG"),
             "thailand": ("THAÏLANDE", "THAILAND"), "india": ("INDE", "INDIA"), "ussr": ("URSS", "USSR"), "russia": ("RUSSIE", "RUSSIA"),
             "brazil": ("BRÉSIL", "BRAZIL"), "england": ("ANGLETERRE", "ENGLAND"), "italy": ("ITALIE", "ITALY"), "spain": ("ESPAGNE", "SPAIN"),
             "mexico": ("MEXIQUE", "MEXICO"), "jamaica": ("JAMAÏQUE", "JAMAICA"), "greece": ("GRÈCE", "GREECE"),
             "australia": ("AUSTRALIE", "AUSTRALIA"), "venezuela": ("VENEZUELA", "VENEZUELA"), "kenya": ("KENYA", "KENYA"),
             "france": ("FRANCE", "FRANCE"), "egypt": ("ÉGYPTE", "EGYPT"), "canada": ("CANADA", "CANADA"), "scotland": ("ÉCOSSE", "SCOTLAND"),
             "germany": ("ALLEMAGNE", "GERMANY"), "romania": ("ROUMANIE", "ROMANIA")}
# (country, words of the detail, HD theme): the first that fits / le premier qui convient
PLACE_THEMES = [("japan", r"winter|snow", "fight_snow"), ("japan", r"cave|gokuentou|akuma", "fight_ruins"), ("japan", r"market", "fight_market"),
                ("japan", r"seaside", "fight_harbor"), ("japan", r"bath|sumo|house|swings", "fight_temple"), ("japan", "", "fight_castle"),
                ("usa", r"air ?base|plane|hangar|military|prison", "fight_base"), ("usa", r"truck", "fight_desert"),
                ("usa", r"pier|boat|party|yard", "fight_harbor"), ("usa", "", "fight_city"), ("china", "", "fight_market"),
                ("hong kong", "", "fight_market"), ("thailand", "", "fight_thai"), ("india", "", "fight_palace"), ("ussr", "", "fight_factory"),
                ("russia", "", "fight_factory"), ("brazil", "", "fight_jungle"), ("venezuela", "", "fight_jungle"), ("jamaica", "", "fight_harbor"),
                ("england", "", "fight_gothic"), ("scotland", "", "fight_gothic"), ("romania", "", "fight_gothic"), ("italy", "", "fight_harbor"),
                ("spain", "", "fight_city"), ("mexico", "", "fight_desert"), ("greece", "", "fight_ruins"), ("australia", "", "fight_desert"),
                ("kenya", "", "fight_desert"), ("egypt", "", "fight_desert"), ("canada", "", "fight_snow"), ("germany", "", "fight_lab"),
                ("france", "", "fight_city")]
# stages named after a fighter: the country of the stage (and its detail) / décors au nom d'un combattant : leur pays
CHAR_PLACES = {"ryu": "japan (castle)", "e.honda": "japan (bath house)", "blanka": "brazil", "guile": "usa (air base)", "ken": "usa (pier)",
               "chun li": "china", "chun-li": "china", "zangief": "ussr", "dhalsim": "india", "dictator": "thailand (temple)",
               "m.bison": "thailand (temple)", "sagat": "thailand (statue)", "boxer": "usa (las vegas)", "claw": "spain", "cammy": "england",
               "t.hawk": "mexico", "fei long": "hong kong", "dee jay": "jamaica", "charlie": "usa (air base)", "adon": "thailand",
               "sodom": "usa (japanese)", "guy": "usa (metro city)", "birdie": "england", "rose": "italy", "dan": "hong kong",
               "akuma": "japan (cave)", "shin akuma": "japan (cave)", "gouki": "japan (cave)", "alex": "usa (city)", "yun": "hong kong",
               "yang": "hong kong", "dudley": "england", "q": "england", "necro": "russia", "ibuki": "japan (house)", "elena": "kenya",
               "oro": "brazil", "sean": "brazil", "makoto": "japan (house)", "remy": "france", "demitri": "romania", "jon talbain": "england",
               "victor": "germany", "morrigan": "scotland", "anakaris": "egypt", "felicia": "usa (city)", "bishamon": "japan (house)",
               "rikuo": "brazil", "sasquatch": "canada", "hsien-ko": "china"}
# stages with no country, by name / décors sans pays, par leur nom : (thème, nom français, nom anglais)
NAMED = {"city": ("fight_city", "VILLE", "CITY"), "arena": ("arena", "ARÈNE", "ARENA"),
         "orbital station": ("pul_station", "STATION ORBITALE", "ORBITAL STATION"), "town-3": ("mn_city", "TOWN-3", "TOWN-3"),
         "forest": ("cs_forest", "FORÊT", "FOREST"), "warship": ("ic_sea", "CUIRASSÉ", "WARSHIP"), "seafloor": ("pul_water", "FOND MARIN", "SEAFLOOR"),
         "airfield": ("fight_base", "AÉRODROME", "AIRFIELD"), "volcano": ("th_fire", "VOLCAN", "VOLCANO"), "brain": ("pul_nebula", "CERVEAU", "BRAIN"),
         "capcom cafe": ("fight_city", "CAPCOM CAFÉ", "CAPCOM CAFE"), "shopping center": ("lr_city", "CENTRE COMMERCIAL", "SHOPPING CENTER"),
         "slopes": ("fight_snow", "PISTES DE SKI", "SKI SLOPES"), "dock": ("fight_harbor", "DOCKS", "DOCK"),
         "chinatown": ("fight_market", "CHINATOWN", "CHINATOWN"), "fireplace": ("fight_temple", "AU COIN DU FEU", "FIREPLACE"),
         "morrigan's castle": ("fight_gothic", "CHÂTEAU DE MORRIGAN", "MORRIGAN'S CASTLE"),
         "demitri's castle": ("fight_gothic", "CHÂTEAU DE DEMITRI", "DEMITRI'S CASTLE"), "bonus stage": ("arena", "BONUS", "BONUS"),
         "point 48106": ("fight_base", "POINT 48106", "POINT 48106")}
# stages named after a fighter or a boss with no place to show: the theme only / le thème seul
THEME_ONLY = {"urien": "fight_lab", "gill": "pul_nebula", "twelve": "fight_lab", "hugo": "fight_harbor", "pyron": "space", "donovan": "nd_grave",
              "lord raptor": "arena", "huitzil": "fight_ruins", "wolverine": "cs_forest", "psylocke": "fight_temple", "colossus": "fight_snow",
              "cyclops/gouki": "fight_city", "storm": "fight_desert", "iceman": "fight_snow", "spiral": "fight_lab",
              "silver samurai": "fight_castle", "omega red": "fight_factory", "sentinel": "fight_lab", "juggernaut": "fight_ruins",
              "magneto": "space", "hauzer": "fight_desert", "tanuma": "fight_temple", "hydron": "pul_water", "lavia": "th_wind",
              "ravange": "nd_grave", "gi gi": "ml_temple", "blade": "fight_castle", "scion": "pul_nebula"}
# the numbered stages of Vampire Savior and Vampire Hunter 2 / les décors numérotés
NUMBERED = ["fight_gothic", "fight_ruins", "fight_gothic", "nd_grave", "fight_gothic", "fight_temple", "fight_city", "fight_ruins", "th_fire",
            "fight_jungle", "fight_factory", "pul_nebula", "fight_snow"]
# a game whose stages have no name (Marvel vs. Capcom) and the games with no stage value: their themes / leurs thèmes
CYCLE = ["fight_city", "fight_lab", "fight_harbor", "fight_market", "fight_jungle", "fight_desert", "fight_snow", "space", "fight_castle",
         "fight_ruins"]
SF2_LOOK = ["fight_castle", "fight_temple", "fight_jungle", "fight_base", "fight_harbor", "fight_market", "fight_factory", "fight_palace",
            "fight_city", "fight_thai"]
MARVEL_LOOK = ["fight_lab", "fight_city", "space", "fight_ruins", "fight_snow", "fight_factory", "fight_harbor", "fight_desert"]
STAGE_LISTS = {"hsf2": SF2_LOOK, "sfzch": SF2_LOOK, "msh": MARVEL_LOOK, "xmvsf": MARVEL_LOOK, "mshvsf": MARVEL_LOOK,
               "megaman": ["fight_lab", "fight_city", "fight_factory", "space"], "megaman2": ["fight_lab", "fight_city", "fight_factory", "space"],
               "slammast": ["arena"], "mbombrd": ["arena"], "ringdest": ["arena"],
               "jojo": ["fight_city", "fight_desert", "fight_harbor", "fight_gothic", "fight_ruins"],
               "jojoba": ["fight_city", "fight_desert", "fight_harbor", "fight_gothic", "fight_ruins"]}


def backdrop_of(c):
    """(address, [(value, label)...]) of a Select Background cheat: the write that changes from one stage to the next.
    / L'écriture dont la valeur change d'un décor à l'autre."""
    opts = [o for o in c["options"] if o["n"] != 0 and o["triples"]]
    if len(opts) < 2:
        return None, None
    for i in range(min(len(o["triples"]) for o in opts)):
        addrs = [o["triples"][i][1] for o in opts]
        addr = max(set(addrs), key=addrs.count)
        same = [o for o in opts if o["triples"][i][1] == addr]
        vals = [o["triples"][i][2] for o in same]
        if len(same) < len(opts) * 0.8 or len(set(vals)) < len(same) * 0.8:
            continue
        return addr, [(o["triples"][i][2], o["label"]) for o in same]
    return None, None


def stage_look(label):
    """(HD theme, [french, english] place or "") of a stage of the cheat database. / Thème HD et lieu d'un décor."""
    t = label.strip().lstrip("#").strip()
    m = re.match(r"^(\d+)\s*-\s*(.+)$", t)
    if m:                                                    # 01 - FEAST OF THE DAMNED
        name = m.group(2).strip().upper()
        return NUMBERED[(int(m.group(1)) - 1) % len(NUMBERED)], [name, name]
    low = re.sub(r"\s+ii$", "", t.lower())
    if re.match(r"^\d+$", low):                             # stages with no name / décors sans nom
        return CYCLE[(int(low) - 1) % len(CYCLE)], ""
    low = re.sub(r"\s*\(=.*\)$", "", low)
    if low in THEME_ONLY:
        return THEME_ONLY[low], ""
    for key, (theme, fr, en) in NAMED.items():
        if low == key or low.startswith(key + " "):
            return theme, [fr, en]
    low = CHAR_PLACES.get(low, low)
    m = re.match(r"^([a-z .'-]+?)\s*(?:\((.*)\))?$", low)
    country, detail = (m.group(1).strip(), m.group(2) or "") if m else (low, "")
    if country in COUNTRIES:
        for c, words, theme in PLACE_THEMES:
            if c == country and (not words or re.search(words, detail)):
                return theme, list(COUNTRIES[country])
    return "", ""


def stages_from_cheats(cs, fam):
    """The "backdrop" value and the "hd" stages of a fighting game. / La valeur "backdrop" et les décors HD."""
    for c in cs:
        if BACKDROP.match(c["name"]):
            addr, opts = backdrop_of(c)
            if addr is None:
                continue
            looks = {}
            for v, label in opts:
                theme, place = stage_look(label)
                if theme and v not in looks:
                    looks[v] = (theme, place)
            if len(looks) < 2:
                continue
            stages, places = [], []
            for v in range(max(looks) + 1):               # indexed by the value read / rangés par valeur lue
                theme, place = looks.get(v) or ((stages[-1], places[-1]) if stages else looks[min(looks)])
                stages.append(theme)
                places.append(place)
            val = value(addr, 1, fam, "u8", f"stage backdrop, picks the HD theme in hd.stages (FBNeo cheat database, {c['name']})")
            hd = {"stages": stages, "places": places,
                  "note": f"HD theme and place shown for each backdrop value (index = value), made by {TOOL} from the stages of the "
                          "cheat database, see README, HD themes"}
            return val, hd
    return None, None


# ------------------------------------------------------------------ files
def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def dump(path, d):
    """JSON with the lists of names on one line (the sets of a game) / les listes de noms sur une ligne."""
    text = json.dumps(d, ensure_ascii=False, indent=2)
    text = re.sub(r'\[\s*\n\s*("[^"\n]*"(?:,\s*\n\s*"[^"\n]*")*)\s*\n\s*\]',
                  lambda m: "[" + re.sub(r",\s*\n\s*", ", ", m.group(1)) + "]", text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


# the super gauges on the bottom line of the panel, blue, gold and blinking when full / les jauges de super en bas de la dalle
SUPER_LAYERS = [
    {"type": "gauge", "var": "power", "max": 100, "x": 0, "y": 30, "w": 63, "h": 2, "anchor": "left", "color": "#3c96ff", "low": "#3c96ff",
     "low_at": 0, "back": "#2a1c08", "shade": False, "when": {"has": "power"}},
    {"type": "rect", "x": 0, "y": 30, "w": 63, "h": 2, "color": "#ffd040", "blink_period": 0.5, "when": {"var": "power", "gt": 99.5}},
    {"type": "gauge", "var": "power_p2", "max": 100, "x": 65, "y": 30, "w": 63, "h": 2, "anchor": "right", "color": "#3c96ff",
     "low": "#3c96ff", "low_at": 0, "back": "#2a1c08", "shade": False, "when": {"has": "power_p2"}},
    {"type": "rect", "x": 65, "y": 30, "w": 63, "h": 2, "color": "#ffd040", "blink_period": 0.5, "when": {"var": "power_p2", "gt": 99.5}}]


# the rounds won, small gold squares above the bars, on each side of the timer (Street Fighter II and others)
# les rounds gagnés, petits carrés dorés au-dessus des barres, de chaque côté du chrono
ROUND_LAYERS = [
    {"type": "icons", "var": "rounds", "x": 54, "y": 11, "max": 2, "gap": 1, "align": "right", "pattern": ["##", "##"],
     "colors": {"#": "#ffd040"}, "empty": "#3a2a10", "when": {"all": [{"has": "rounds"}, {"has": ["health", "health_p2"]}]}},
    {"type": "icons", "var": "rounds_p2", "x": 73, "y": 11, "max": 2, "gap": 1, "pattern": ["##", "##"],
     "colors": {"#": "#ffd040"}, "empty": "#3a2a10", "when": {"all": [{"has": "rounds_p2"}, {"has": ["health", "health_p2"]}]}}]


def make_templates(games_dir):
    """games/cps_*.json: the shared scenes, the Neo Geo ones with the title where they said NEO GEO."""
    for key, src in TEMPLATES.items():
        d = load(os.path.join(games_dir, src + ".json")) or {}
        layers = json.loads(json.dumps((d.get("scene") or {}).get("layers") or []))
        out = []
        for ly in layers:
            segs = ly.get("segments")
            text = "".join(s.get("text", "") for s in segs) if isinstance(segs, list) else ly.get("text")
            if isinstance(text, str) and text.replace(" ", "") == "NEOGEO":
                ly = {"type": "marquee", "segments": [{"text": "{title}", "color": "#ececec"}], "font": ly.get("font", "7x14"),
                      "y": ly.get("y", 11), "x": 0, "w": 128, "speed": 14, "gap": 40, "upper": True, "static_if_fits": True,
                      "when": ly.get("when")}
                if ly["when"] is None:
                    ly.pop("when")
            out.append(ly)
        if key == "cps_combat":
            out[1:1] = SUPER_LAYERS
            bars = [i for i, ly in enumerate(out) if ly.get("type") == "gauge" and ly.get("var") == "health_p2"]
            if bars:
                out[bars[0] + 1:bars[0] + 1] = ROUND_LAYERS
        dump(os.path.join(games_dir, key + ".json"), {
            "note": f"Shared scene of the Capcom CPS games ({key.split('_')[-1] if '_' in key else 'action'}), made by {TOOL} "
                    f"from games/{src}.json. The games take it with scene_from.",
            "generated": TOOL, "scene": {"layers": out}})


def build(fbneo, cheats_dir, games_dir):
    ds = []
    for rel in DRIVERS:
        path = os.path.join(fbneo, rel)
        with open(path, encoding="latin-1") as f:
            ds += drivers(f.read())
    by = {d["name"]: d for d in ds}

    def root(d):
        seen = set()
        while d["parent"] and d["parent"] in by and d["name"] not in seen:
            seen.add(d["name"])
            d = by[d["parent"]]
        return d
    groups = {}
    for d in ds:
        groups.setdefault(root(d)["name"], []).append(d)
    make_templates(games_dir)
    report = []
    for name in sorted(groups):
        p = by[name]
        fam = family(p)
        sets = [name] + sorted(x["name"] for x in groups[name] if x["name"] != name)
        cs = cheats(os.path.join(cheats_dir, name + ".ini"))
        if not cs:                                   # a version that has cheats / une version qui en a
            for x in sets[1:]:
                cs = cheats(os.path.join(cheats_dir, x + ".ini"))
                if cs:
                    break
        vals, derived, got = values_from_cheats(cs, fam, name)
        scene = scene_of(p["genre"])
        title = clean(p["desc"])
        titles = {}
        for x in groups[name]:
            t = clean(x["desc"])
            if x["name"] != name and t and t != title:
                titles[x["name"]] = t
        path = os.path.join(games_dir, name + ".json")
        old = load(path)
        if old is not None and old.get("generated") != TOOL and not old.get("cps"):
            report.append(f"{name}: games/{name}.json is not one of ours, left as it is")
            continue
        d = old if old is not None else {}
        d["title"] = d.get("title_hand") or title
        kind = {"cps_combat": "fighting game", "cps_shoot": "shoot'em up", "cps_reflexion": "puzzle, quiz or other game",
                "cps_action": "action game"}[scene]
        d["note"] = (f"Capcom {fam} {kind}: " + (", ".join(got) if got else "no value known yet")
                     + f" (FinalBurn Neo cheat database). Made by {TOOL}.")
        d["generated"] = TOOL
        d["cps"] = fam
        d["match"] = [{"system": sets}]
        d["retroarch"] = dict(RA_CPS3 if fam == "CPS3" else RA_CPS, content=sets)
        if titles:
            d["titles"] = titles
        else:
            d.pop("titles", None)
        if "scene" not in d:
            d["scene_from"] = scene
        mem = d.get("memory") if isinstance(d.get("memory"), dict) else {}
        hand = {k: v for k, v in (mem.get("values") or {}).items()
                if not (isinstance(v, dict) and "FBNeo cheat database" in str(v.get("note", "")))}
        merged = dict(vals)
        merged.update(hand)                          # learned or set by hand wins / ce qui est appris passe avant
        # versions whose own cheats put a value elsewhere (JoJo's Venture's second revision, Quiz & Dragons in Japan...):
        # read there for that version, MAME and RetroArch both take "per_game" over the file's values
        # les versions dont les propres codes de triche mettent une valeur ailleurs : lue là pour cette version
        per = {}
        for x in sets[1:]:
            xc = cheats(os.path.join(cheats_dir, x + ".ini"))
            if xc:
                xv = values_from_cheats(xc, fam, name)[0]
                diff = {k: v for k, v in xv.items() if k in vals and k not in hand and v.get("addr") != vals[k].get("addr")}
                if diff:
                    per[x] = diff
        if per:
            d["per_game"] = per
        else:
            d.pop("per_game", None)
        if "time" in hand:                           # the whole timer found by hand (Mercs) / le chrono entier trouvé à la main
            merged.pop("_time", None)
        d["memory"] = {"cpu": ":maincpu", "values": merged}
        dv = d.get("derived") if isinstance(d.get("derived"), dict) else {}
        dv.update(derived)
        for k in list(dv):                           # names of a value no longer read / noms d'une valeur qui n'est plus lue
            spec = dv[k] if isinstance(dv[k], dict) else {}
            used = [spec["value"]] if isinstance(spec.get("value"), str) else [x for x in spec.get("join") or [] if isinstance(x, str)]
            if used and any(u not in merged for u in used):
                del dv[k]
        if dv:
            d["derived"] = dv
        else:
            d.pop("derived", None)
        if scene == "cps_combat":
            hd_old = d.get("hd") if isinstance(d.get("hd"), dict) else {}
            if not hd_old.get("scene") and not hd_old.get("hand"):
                bval, hd = stages_from_cheats(cs, fam)
                if bval is not None:
                    merged.setdefault("backdrop", bval)
                    got.append("stages")
                elif name in STAGE_LISTS:
                    hd = {"stages": STAGE_LISTS[name], "note": f"HD themes of the fights (one per game, no stage value known), made by {TOOL}"}
                if hd:
                    d["hd"] = hd
        watch = [k for k in ("time", "_time", "health", "health_p2", "lives", "lives_p2", "bombs", "score", "score_p2") if k in merged]
        moving = [k for k in ("time", "_time", "score", "score_p2") + (("health", "health_p2") if scene == "cps_combat" else ())
                  if k in merged]
        if moving:                                   # the timer, the score once learned, the health of a fight
            d["activity"] = {"values": watch, "moving": moving, "seconds": 10,
                             "note": "no BIOS says who plays: player 1 plays while these values move, as long as one of "
                                     "the moving ones is read (lives or bombs alone change too seldom)"}
        else:
            d.pop("activity", None)
        # credits not read: counted from the coin buttons. A player begins (start, continue, joining in) when his lives
        # come back from 0 by 2 or more, an extra life is 1. Kept when set by hand (Mercs: its energy, it has no lives).
        # crédits comptés d'après les boutons : un joueur commence quand ses vies reviennent de 0 (2 ou plus)
        coins = d.get("coins") if isinstance(d.get("coins"), dict) else {}
        if not coins.get("hand"):
            begin = {k: p for k, p in (("lives", "p1"), ("lives_p2", "p2")) if k in merged}
            if "credits" not in merged and scene != "cps_combat" and begin:
                d["coins"] = {"begin": begin, "rise": 2,
                              "note": "credits not read: counted from the coin buttons (coin_buttons.bat). A player begins "
                                      "(start, continue, joining in) and uses one when his lives come back from 0 by 2 or "
                                      "more (an extra life is 1)"}
            else:
                d.pop("coins", None)
        demo = {"credits": 2, "p1_mode": 1, "p2_mode": 0}
        if scene == "cps_combat":
            demo.update({"health": 100, "health_p2": 100})
            if "time" in merged:
                demo["time"] = 99
        for k in ("lives", "bombs"):
            if k in merged:
                demo[k] = 3
        for side, key, pick in (("p1_char", "_p1_chr", 0), ("p2_char", "_p2_chr", 1)):
            if key in merged and side in derived:
                keys = sorted(derived[side]["names"], key=lambda k: [int(x) for x in k.split(",")])
                parts = [int(x) for x in keys[min(pick, len(keys) - 1)].split(",")]
                demo[key] = parts[0]
                if len(parts) > 1:                   # the second byte of the pair / le second octet de la paire
                    demo[key + "2"] = parts[1]
        if not d.get("demo_hand"):
            d["demo"] = demo
        dd = d.get("demo") if isinstance(d.get("demo"), dict) else {}
        if "time" not in merged:                     # a timer not shown, not in the demo either / pas de chrono dans la démo
            dd.pop("time", None)
            if isinstance(dd.get("sim"), dict) and "time" in dd["sim"]:
                dd["sim"].pop("time")
                if not dd["sim"]:                    # it only moved the timer / elle ne faisait bouger que le chrono
                    dd.pop("sim")
        dump(path, d)
        report.append(f"{fam} {name:10s} {scene:14s} {len(sets):3d} sets  " + (", ".join(got) or "-"))
    return report


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    report = build(argv[1], argv[2], os.path.join(ROOT, "games"))
    print("\n".join(report))
    print(len(report), "games")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
