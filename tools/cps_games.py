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
    "lives": rf"^infinite lives {PL}1$",
    "lives_p2": rf"^infinite lives {PL}2$",
    "bombs": rf"^infinite (?:bombs|bomb stock|bomb) {PL}1$",
    "power": rf"^(?:infinite (?:power|super|super meter|super gauge)|always have max (?:power|super)) {PL}1$",
    "power_p2": rf"^(?:infinite (?:power|super|super meter|super gauge)|always have max (?:power|super)) {PL}2$",
    "_p1_chr": rf"^select (?:1st )?char(?:acter)?(?: \(active char\))?(?: now!)? {PL}1$",
    "_p2_chr": rf"^select (?:1st )?char(?:acter)?(?: \(active char\))?(?: now!)? {PL}2$",
}
PATTERNS = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}


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
            vals[key] = v
    if "time" in found:
        t = enabled(found["time"])
        if t and t[0][2] > 0:
            kind = "bcd" if bcd_like(t[0][2]) else "u8"
            vals["time"] = value(t[0][1], 1, fam, kind, f"timer ({src}, Infinite Time)")
            if kind == "u8":
                vals["time"].pop("bytes", None)
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
            addr, names = names_of(found[key])
            if names:
                vals[key] = value(addr, 1, fam, "u8", f"{'player 1' if key == '_p1_chr' else 'player 2 or computer'} character "
                                                     f"({src}, {found[key]['name']})")
                derived[out] = {"value": key, "names": names}
    for k in vals:
        if not k.startswith("_"):
            got.append(k)
    if derived:
        got.append(f"{len(derived['p1_char']['names']) if 'p1_char' in derived else len(derived['p2_char']['names'])} characters")
    return vals, derived, got


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
        d["memory"] = {"cpu": ":maincpu", "values": merged}
        if derived:
            dv = d.get("derived") if isinstance(d.get("derived"), dict) else {}
            dv.update(derived)
            d["derived"] = dv
        watch = [k for k in ("time", "health", "health_p2", "lives", "lives_p2", "bombs") if k in merged]
        if watch:
            d["activity"] = {"values": watch, "seconds": 10,
                             "note": "no BIOS says who plays: player 1 plays while these values move"}
        else:
            d.pop("activity", None)
        demo = {"credits": 2, "p1_mode": 1, "p2_mode": 0}
        if scene == "cps_combat":
            demo.update({"health": 100, "health_p2": 100, "time": 99})
        for k in ("lives", "bombs"):
            if k in merged:
                demo[k] = 3
        if "_p1_chr" in merged and "p1_char" in derived:
            demo["_p1_chr"] = int(sorted(derived["p1_char"]["names"], key=int)[0])
        if "_p2_chr" in merged and "p2_char" in derived:
            keys = sorted(derived["p2_char"]["names"], key=int)
            demo["_p2_chr"] = int(keys[1] if len(keys) > 1 else keys[0])
        if not d.get("demo_hand"):
            d["demo"] = demo
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
