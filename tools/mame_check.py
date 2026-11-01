"""Compares the game files made by hand (the Neo Geo games) with the cheats of MAME (1.31). Changes nothing.

For each game, the values the cheats of MAME give (read like the FinalBurn Neo ones, tools/mame_cheats.py) are put beside
those of its file. Same address, a different address, or a value MAME gives that the file does not have: a list to read
before adding anything by hand. A value learned on a cabinet is never to be replaced by a cheat.

Compare les fichiers de jeu faits à la main (les jeux Neo Geo) avec les codes de MAME, sans rien changer : même adresse,
adresse différente, ou valeur que MAME donne et que le fichier n'a pas. Une valeur apprise sur une borne ne se remplace pas.

usage: python tools/mame_check.py MAME_CHEATS [GAME ...]
       MAME_CHEATS: the folder of the XML files of MAME's cheat.7z, or cheat.7z itself (pip install py7zr)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cave_games  # noqa: E402
import cps_games  # noqa: E402
from mame_cheats import MameCheats  # noqa: E402

NEO = (0x100000, 0x10000)                  # the 68000 RAM FinalBurn Neo gives RetroArch / la RAM donnée à RetroArch
TEMPLATES = {"neogeo", "neogeo_combat", "neogeo_reflexion", "neogeo_shoot", "neogeo_sport"}


def hand_files(only=()):
    """(key, file) of the Neo Geo games made by hand. / Les jeux Neo Geo faits à la main."""
    out = []
    folder = os.path.join(ROOT, "games")
    for name in sorted(os.listdir(folder)):
        key = name[:-5]
        if not name.endswith(".json") or key in TEMPLATES or key.startswith("_") or (only and key not in only):
            continue
        d = cps_games.load(os.path.join(folder, name))
        if not isinstance(d, dict) or str(d.get("generated", "")).startswith("tools/") or \
                (d.get("retroarch") or {}).get("ram_base") != "0x100000":
            continue
        out.append((key, d))
    return out


def sets_of(d):
    out = []
    for m in d.get("match") or []:
        s = m.get("system") if isinstance(m, dict) else None
        out += s if isinstance(s, list) else [s]
    return [s for s in out if s]


def compare(d, mame):
    """(set read, same, differs, new) for one game file. / Pour un fichier de jeu."""
    sets = sets_of(d)
    cs, used = [], None
    for x in sets:
        cs = mame.get(x)
        if cs:
            used = x
            break
    if not cs:
        return None, [], [], []
    cps_games.WINDOWS["NEO"] = NEO
    vals, derived, _ = cps_games.values_from_cheats(cs, "NEO", sets[0])
    for k, v in cave_games.cave_values(cs, "NEO").items():
        vals.setdefault(k, v)
    have = (d.get("memory") or {}).get("values") or {}
    same, differs, new = [], [], []
    for k, v in vals.items():
        if k.startswith("_time"):                # a part of the timer only: the BIOS says who plays / le BIOS dit qui joue
            continue
        a, h = v.get("addr"), have.get(k)
        if isinstance(h, dict) and h.get("addr"):
            (same if int(h["addr"], 16) == int(a, 16) else differs).append((k, h["addr"], a, v.get("note", "")))
        else:
            new.append((k, None, a, v.get("note", "")))
    for k, spec in derived.items():
        if k not in (d.get("derived") or {}):
            new.append((k, None, f"{len(spec.get('names') or {})} names", ""))
    return used, same, differs, new


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    mame = MameCheats(argv[1])
    files = hand_files(set(argv[2:]))
    mame.preload([s for _, d in files for s in sets_of(d)])
    total = {"same": 0, "differs": 0, "new": 0}
    for key, d in files:
        used, same, differs, new = compare(d, mame)
        if used is None:
            print(f"{key}: no cheat in MAME")
            continue
        total["same"] += len(same)
        total["differs"] += len(differs)
        total["new"] += len(new)
        if not differs and not new:
            print(f"{key}: {len(same)} values, all the same as MAME")
            continue
        print(f"{key} ({used}): {len(same)} the same")
        for k, h, a, note in differs:
            print(f"   differs  {k}: file {h}, MAME {a}  ({note})")
        for k, h, a, note in new:
            print(f"   new      {k}: {a}  ({note})")
    print(f"{len(files)} games, {total['same']} the same, {total['differs']} different, {total['new']} that MAME adds")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
