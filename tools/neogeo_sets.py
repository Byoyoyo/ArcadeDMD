"""Builds dmd/neogeo_sets.json from the list of FinalBurn Neo (src/burn/drv/neogeo/d_neogeo.cpp of libretro/FBNeo).

Under RetroArch, ArcadeDMD only gets the name of the set that runs, not its parent. MAME gives the parent, so with MAME a
version of a game takes the file of the original game. This table does the same for RetroArch. Each Neo Geo set gets
its parent (a version, a bootleg, a hack, a prototype), or, for a game of its own that has no parent (a homebrew for
example), the scene of its genre ("@neogeo_shoot"), and its title when it differs from the one of its parent. The BIOS,
the systems and the test programs are left out.

Construit dmd/neogeo_sets.json à partir de la liste de FinalBurn Neo. Sous RetroArch, ArcadeDMD ne reçoit que le nom du
set lancé, pas son parent. Cette table donne à chaque set Neo Geo son parent, ou la scène de son genre pour un jeu à
part, et son titre quand il diffère de celui de son parent.

usage: python tools/neogeo_sets.py path/to/d_neogeo.cpp [dmd/neogeo_sets.json]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEMS = {"neogeo", "ng_mv1", "ng_mv2f", "ng_mv4f", "neocdz"}
# FinalBurn Neo genre -> shared scene / genre -> scène commune
GENRES = [(("GBF_VSFIGHT",), "neogeo_combat"),
          (("GBF_VERSHOOT", "GBF_HORSHOOT"), "neogeo_shoot"),
          (("GBF_SPORTSMISC", "GBF_SPORTSFOOTBALL", "GBF_RACING", "GBF_BALLPADDLE", "GBF_BREAKOUT", "GBF_MINIGAMES"),
           "neogeo_sport"),
          (("GBF_PUZZLE", "GBF_QUIZ", "GBF_MAHJONG", "GBF_CASINO", "GBF_CARD"), "neogeo_reflexion")]


def drivers(src):
    out = []
    for m in re.finditer(r"struct BurnDriver\w*\s+BurnDrv\w+\s*=\s*\{(.*?)\n\};", src, re.S):
        body = m.group(1)
        toks = re.findall(r'"((?:[^"\\]|\\.)*)"|\b(NULL)\b', body)
        vals = [a if a or not b else None for a, b in toks]
        flags = re.search(r"\b(BDF_[A-Z_]+(?:\s*\|\s*BDF_[A-Z_]+)*)", body)
        hw = re.search(r"\b(HARDWARE_[A-Z_]+(?:\s*\|\s*HARDWARE_[A-Z_]+)*)", body)
        genre = re.search(r"\b(GBF_[A-Z_]+(?:\s*\|\s*GBF_[A-Z_]+)*)", body)
        out.append({"name": vals[0], "parent": vals[1], "desc": (vals[5] or "").split("\\0")[0],
                    "flags": flags.group(1) if flags else "", "hw": hw.group(1) if hw else "",
                    "genre": genre.group(1) if genre else ""})
    return [d for d in out if "SNK_NEOGEO" in d["hw"]]


def clean(desc):
    """The name of the game alone: no alternate title after " / ", nothing in parentheses, no "Neo Geo Conversion"."""
    t = desc.split(" / ")[0]
    t = re.sub(r"\s*\([^)]*\)", "", t)
    t = re.sub(r"\s*-?\s*Neo ?Geo(?: Conversion)?\s*$", "", t, flags=re.I)
    return re.sub(r"\s+", " ", t).strip(" -")


def scene_of(genre):
    for flags, scene in GENRES:
        if any(f in genre for f in flags):
            return scene
    return "neogeo"


def tool(d):
    return "BDF_BOARDROM" in d["flags"] or d["name"] in SYSTEMS or d["name"].startswith(("ng_mv", "neocd")) or (
        "GBF_MISC" in d["genre"] and re.search(r"\b(test|check)\b", d["desc"], re.I) is not None)


def build(src):
    ds = [d for d in drivers(src) if not tool(d)]
    by = {d["name"]: d for d in ds}
    sets = {}
    for d in ds:
        title = clean(d["desc"])
        p = by.get(d["parent"]) if d["parent"] else None
        if p is not None:
            sets[d["name"]] = [p["name"], "" if title == clean(p["desc"]) else title]
        else:
            sets[d["name"]] = ["@" + scene_of(d["genre"]), title]
    return sets


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    with open(argv[1], encoding="latin-1") as f:
        sets = build(f.read())
    out = argv[2] if len(argv) > 2 else os.path.join(ROOT, "dmd", "neogeo_sets.json")
    lines = ['{', '  "note": "Neo Geo sets of FinalBurn Neo (src/burn/drv/neogeo/d_neogeo.cpp): parent, or @scene of the genre, '
             'and title when it differs from the parent. Made by tools/neogeo_sets.py.",', '  "sets": {']
    items = sorted(sets.items())
    for i, (k, v) in enumerate(items):
        lines.append(f"    {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" + ("," if i < len(items) - 1 else ""))
    lines += ["  }", "}"]
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    roots = sum(1 for v in sets.values() if v[0].startswith("@"))
    print(f"{out}: {len(sets)} sets, {roots} without a parent")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
