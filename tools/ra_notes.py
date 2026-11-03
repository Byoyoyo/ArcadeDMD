"""Downloads what RetroAchievements knows of the arcade games ArcadeDMD knows (1.31): the code notes, where each game
keeps its values, and with a RetroAchievements account the achievements, the leaderboards (the score often) and the rich
presence (the stage, the character...). Everything goes in ra_notes.json, to be read for the game files.

Run it from the ArcadeDMD folder (ra_notes.bat). The account is asked for once, its password only used to get the token
that RetroAchievements gives emulators, never kept. Without an account (just Enter) only the code notes come. One
request a second, as an emulator opening the games one after the other.

Télécharge ce que RetroAchievements sait des jeux d'arcade qu'ArcadeDMD connaît : les notes de code (où chaque jeu
garde ses valeurs) et, avec un compte, les succès, les classements (souvent le score) et la présence (le niveau, le
personnage...). Tout va dans ra_notes.json. Le mot de passe sert seulement à obtenir le jeton, il n'est pas gardé.

usage: python ra_notes.py [GAMES_FOLDER] [--no-account]
"""
import getpass
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

URL = "https://retroachievements.org/dorequest.php"
UA = "ArcadeDMD/1.31 (code notes for a personal arcade marquee; github.com/Byoyoyo/ArcadeDMD)"
ARCADE = 27                                    # RetroAchievements' arcade system / le système arcade
PAUSE = 1.0                                    # seconds between two requests / secondes entre deux demandes
FR = os.environ.get("L", "fr") != "en"
TEMPLATES = {"neogeo", "neogeo_combat", "neogeo_reflexion", "neogeo_shoot", "neogeo_sport", "cps_combat", "cps_action", "cps_shoot",
             "cps_reflexion", "cave_shoot", "cave_combat", "cave_action", "cave_reflexion"}


def say(fr, en):
    print(fr if FR else en, flush=True)


def post(params, tries=4):
    """The JSON answer of RetroAchievements to one request, tried again after a network trouble or a slow down.
    / La réponse JSON à une demande, redemandée après un souci réseau ou un ralentissement."""
    data = urllib.parse.urlencode(params).encode("ascii")
    last = "no answer"
    for k in range(tries):
        req = urllib.request.Request(URL, data=data, headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:                     # too fast or busy: wait / trop vite ou occupé
                time.sleep(20 * (k + 1))
                continue
            try:
                return json.loads(e.read().decode("utf-8", "replace"))
            except ValueError:
                return {"Success": False, "Error": f"HTTP {e.code}"}
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
            last = str(e)
            time.sleep(5 * (k + 1))
    return {"Success": False, "Error": last}


def known_sets(folder):
    """{set: (game file, title)} of every game file of ArcadeDMD. / Chaque set des fichiers de jeu."""
    out = {}
    for name in sorted(os.listdir(folder)):
        key = name[:-5]
        if not name.endswith(".json") or key in TEMPLATES or key.startswith("_"):
            continue
        try:
            with open(os.path.join(folder, name), encoding="utf-8") as f:
                d = json.load(f)
        except (OSError, ValueError):
            continue
        for m in d.get("match") or []:
            s = m.get("system") if isinstance(m, dict) else None
            for x in (s if isinstance(s, list) else [s]):
                if isinstance(x, str) and x:
                    out.setdefault(x, (key, d.get("title") or key))
    return out


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    args = [a for a in argv[1:] if not a.startswith("--")]
    folder = args[0] if args else os.path.join(here, "games")
    if not os.path.isdir(folder):
        folder = os.path.join(os.path.dirname(here), "games")          # run from tools/ / lancé depuis tools/
    if not os.path.isdir(folder):
        say("Dossier games introuvable, lance ce script depuis le dossier d'ArcadeDMD.",
            "games folder not found, run this script from the ArcadeDMD folder.")
        return 1
    sets = known_sets(folder)
    say(f"{len(sets)} sets d'arcade dans les fichiers de jeu.", f"{len(sets)} arcade sets in the game files.")

    user = token = ""
    if "--no-account" not in argv:
        user = input("Compte RetroAchievements (Entrée pour s'en passer) : " if FR else
                     "RetroAchievements account (Enter to go without): ").strip()
    if user:
        pw = getpass.getpass("Mot de passe (il ne s'affiche pas) : " if FR else "Password (not shown): ")
        r = post({"r": "login2", "u": user, "p": pw})
        pw = None
        token = r.get("Token") or ""
        if not r.get("Success") or not token:
            say(f"Connexion refusée ({r.get('Error') or 'sans raison'}), je continue avec les notes seules.",
                f"Login refused ({r.get('Error') or 'no reason'}), going on with the notes only.")
            user = token = ""
        else:
            user = r.get("User") or user
            say(f"Connecté en {user}.", f"Logged in as {user}.")

    lib = post({"r": "hashlibrary", "c": ARCADE})
    md5 = lib.get("MD5List") or {}
    if not md5:
        say(f"RetroAchievements ne donne pas sa liste des jeux d'arcade ({lib.get('Error')}).",
            f"RetroAchievements does not give its arcade game list ({lib.get('Error')}).")
        return 1
    games = {}
    for s, (key, title) in sets.items():
        gid = md5.get(hashlib.md5(s.encode("ascii", "ignore")).hexdigest())
        if gid:
            g = games.setdefault(int(gid), {"sets": [], "files": [], "titles": []})
            g["sets"].append(s)
            if key not in g["files"]:
                g["files"].append(key)
                g["titles"].append(title)
    say(f"{len(games)} de ces jeux sont sur RetroAchievements.", f"{len(games)} of these games are on RetroAchievements.")

    out_path = os.path.join(os.path.dirname(folder), "ra_notes.json")
    result = {"source": "retroachievements.org (dorequest.php: codenotes2" + (", patch" if token else "") + ")",
              "date": time.strftime("%Y-%m-%d %H:%M"), "account": bool(token), "games": {}}

    def save():
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)

    try:
        fetch(games, result, user, token, save)
    finally:
        save()                                                         # kept even if it stops / gardé même si ça s'arrête
    total = sum(len(e["notes"]) for e in result["games"].values())
    say(f"Fini, {total} notes pour {len(result['games'])} jeux dans {out_path}. Envoie-moi ce fichier.",
        f"Done, {total} notes for {len(result['games'])} games in {out_path}. Send this file.")
    return 0


def fetch(games, result, user, token, save):
    """The notes of each game, and with an account its achievements, leaderboards and rich presence.
    / Les notes de chaque jeu, et avec un compte ses succès, classements et présence."""
    for n, (gid, g) in enumerate(sorted(games.items(), key=lambda kv: kv[1]["titles"][0].lower()), 1):
        entry = dict(g)
        time.sleep(PAUSE)
        r = post({"r": "codenotes2", "g": gid})
        notes = [{"address": c.get("Address"), "note": c.get("Note"), "user": c.get("User")}
                 for c in (r.get("CodeNotes") or []) if c.get("Note") not in (None, "", "''")]
        entry["notes"] = notes
        if not r.get("Success"):
            entry["error"] = r.get("Error")
        if token:
            time.sleep(PAUSE)
            p = post({"r": "patch", "u": user, "t": token, "g": gid})
            pd = p.get("PatchData") or {}
            entry["ra_title"] = pd.get("Title")
            entry["rich_presence"] = pd.get("RichPresencePatch")
            entry["achievements"] = [{"title": a.get("Title"), "description": a.get("Description"), "mem": a.get("MemAddr")}
                                     for a in pd.get("Achievements") or []]
            entry["leaderboards"] = [{"title": b.get("Title"), "description": b.get("Description"), "mem": b.get("Mem"),
                                      "format": b.get("Format")} for b in pd.get("Leaderboards") or []]
        result["games"][str(gid)] = entry
        extra = f", {len(entry.get('achievements') or [])} succès, {len(entry.get('leaderboards') or [])} classements" if token else ""
        extra_en = f", {len(entry.get('achievements') or [])} achievements, {len(entry.get('leaderboards') or [])} leaderboards" \
            if token else ""
        say(f"{n}/{len(games)}  {g['titles'][0]}  {len(notes)} notes{extra}", f"{n}/{len(games)}  {g['titles'][0]}  {len(notes)} notes{extra_en}")
        if n % 20 == 0:
            save()


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        say("Arrêté. Ce qui a été lu est dans ra_notes.json.", "Stopped. What was read is in ra_notes.json.")
        sys.exit(1)
