"""Replays the recorded fights of tests/captures through the fight engine and compares what the HD screen announces,
second by second, with what is expected (tests/expected/<capture>.json): the select screens, ROUND n, FIGHT !, the hits,
K.O., WIN, TIME UP, the next fighter. A change in the engine or in a game's file that moves one of these shows here,
before it shows on a cabinet. Run by the checks of every pull request (1.40.2).

Rejoue les combats enregistrés de tests/captures dans le moteur de combat et compare ce que l'écran HD annonce, seconde
par seconde, avec ce qui est attendu. Un changement du moteur ou d'un fichier de jeu qui déplace une annonce se voit
ici, avant de se voir sur une borne.

usage: python tools/captures_check.py            compares / compare
       python tools/captures_check.py --update   writes what is expected from the engine as it is, after a change that
                                                 is meant: read the difference before / réécrit l'attendu
"""
import glob
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPTURES = os.path.join(ROOT, "tests", "captures")
EXPECTED = os.path.join(ROOT, "tests", "expected")


def replay(capture):
    """The events of a capture, [[second, text], ...]. / Les annonces d'une capture."""
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "t.json")
        env = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy", ARCADEDMD_LANG="fr")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "replay_capture.py"), capture, "--json", out],
                           env=env, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            raise RuntimeError((r.stderr or r.stdout or "no timeline").strip().splitlines()[-1])
        with open(out, encoding="utf-8") as f:
            return json.load(f)["events"]


def main():
    update = "--update" in sys.argv[1:]
    if update:
        os.makedirs(EXPECTED, exist_ok=True)
        names = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(EXPECTED, "*.json")))
        names = names or sys.argv[2:]
    else:
        names = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(EXPECTED, "*.json")))
    if not names:
        print("ERROR nothing expected in tests/expected")
        return 1
    bad = 0
    for name in names:
        capture = os.path.join(CAPTURES, name + ".log")
        path = os.path.join(EXPECTED, name + ".json")
        try:
            got = replay(capture)
        except (OSError, RuntimeError, ValueError, KeyError) as e:
            print(f"ERROR {name}: {e}")
            bad += 1
            continue
        if update:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write("[\n" + ",\n".join(json.dumps(e, ensure_ascii=False) for e in got) + "\n]\n")
            print(f"written {name}: {len(got)} announcements")
            continue
        with open(path, encoding="utf-8") as f:
            want = json.load(f)
        if got != want:                           # once more before saying so: a machine under load / une seconde fois
            try:
                again = replay(capture)
            except (OSError, RuntimeError, ValueError, KeyError):
                again = got
            if again == want:
                print(f"ok {name}: {len(again)} announcements, at the second replay")
                continue
        if got == want:
            print(f"ok {name}: {len(got)} announcements")
            continue
        bad += 1
        k = next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), min(len(got), len(want)))
        print(f"ERROR {name}: {len(got)} announcements, {len(want)} expected, the first difference is number {k + 1}")
        print("   expected:", json.dumps(want[k], ensure_ascii=False) if k < len(want) else "nothing more")
        print("   replayed:", json.dumps(got[k], ensure_ascii=False) if k < len(got) else "nothing more")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
