"""Addresses found by learn.bat, also kept in learned/ so they survive updates.
At startup the engine puts them back into games/<game>.json when an update replaced them.
Delete learned/<game>.json to forget what was learned for a game.

Adresses trouvées par learn.bat, gardées aussi dans learned/ pour survivre aux mises à jour.

Une mise à jour d'ArcadeDMD remplace les fichiers games/*.json. Au démarrage, le moteur remet
les adresses apprises dans games/<jeu>.json si elles n'y sont plus. Pour oublier ce qui a été
appris pour un jeu, il suffit de supprimer learned/<jeu>.json.
"""

import glob
import json
import os
import shutil
import time

from .i18n import tr

DIR = "learned"
OLD_DIR = "appris"          # folder name used by older versions, moved to learned/ by migrate()


def migrate(root, log=print):
    """One-time move of the old appris/ folder: renamed to learned/ when learned/ does not exist yet,
    otherwise its files missing from learned/ are copied there (learned/ wins). Returns True if anything moved."""
    old = os.path.join(root, OLD_DIR)
    new = os.path.join(root, DIR)
    if not os.path.isdir(old):
        return False
    if not os.path.exists(new):
        try:
            os.rename(old, new)
            log(tr("Dossier appris/ renommé en learned/ (adresses apprises)",
                   "Folder appris/ renamed to learned/ (learned addresses)"))
            return True
        except OSError as e:
            log(tr(f"appris/ ne peut pas être renommé en learned/ ({e}), copie des fichiers à la place",
                   f"appris/ cannot be renamed to learned/ ({e}), copying its files instead"))
    try:
        entries = sorted(os.listdir(old))
    except OSError:
        return False
    copied = []
    failed = False
    for name in entries:
        src, dst = os.path.join(old, name), os.path.join(new, name)
        if not os.path.isfile(src) or os.path.exists(dst):
            continue
        try:
            os.makedirs(new, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(name)
        except OSError as e:
            failed = True
            log(tr(f"{name} non copié depuis appris/ ({e})", f"{name} not copied from appris/ ({e})"))
    if copied:
        names = ", ".join(copied)
        log(tr(f"Adresses apprises copiées depuis appris/ vers learned/ ({names})",
               f"Learned addresses copied from appris/ to learned/ ({names})"))
    if not failed and not os.path.exists(old + ".old"):
        try:                       # done once: a file deleted from learned/ must not come back from appris/
            os.rename(old, old + ".old")
        except OSError:
            pass
    return bool(copied)


def _load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def _core(d):
    return {k: v for k, v in d.items() if k != "note"} if isinstance(d, dict) else {}


def _addr(a):
    try:
        s = str(a).strip().lower()
        return int(s, 16) if s.startswith("0x") else int(s)
    except ValueError:
        return None


def not_learned(spec, d):
    """True when the game file says this learned address is not the right one ("not_learned": addresses learn.bat
    finds, where the game keeps something else, such as the score of the last player who scored).
    / L'adresse apprise est une de celles que le fichier du jeu écarte."""
    if not isinstance(spec, dict) or not isinstance(d, dict) or d.get("ptr"):
        return False
    bad = {_addr(a) for a in (spec.get("not_learned") or [])}
    return bool(bad) and _addr(d.get("addr")) in bad


def _about_learning(note):
    """Note that mentions the learning tool, in French or English ("à trouver avec apprendre.bat",
    "to find with learn.bat", "found with learn.bat"...)."""
    low = str(note).lower()
    return "apprendre" in low or "learn" in low


def save(root, key, values, retroarch=None):
    """Ajoute les valeurs apprises (dict nom -> définition) à learned/<key>.json."""
    migrate(root)
    path = os.path.join(root, DIR, key + ".json")
    data = _load(path) or {}
    vals = data.setdefault("values", {})
    for name, d in values.items():
        vals[name] = _core(d)
    if retroarch:
        data["retroarch"] = retroarch
    data["date"] = time.strftime("%d/%m/%Y %H:%M")
    _write(path, data)
    return path


def restore(root, log=print):
    """Remet dans games/*.json les adresses apprises qu'une mise à jour a remplacées. Renvoie les jeux modifiés."""
    migrate(root, log)
    done = []
    for path in sorted(glob.glob(os.path.join(root, DIR, "*.json"))):
        key = os.path.basename(path)[:-5]
        data = _load(path)
        gpath = os.path.join(root, "games", key + ".json")
        if not data or not os.path.exists(gpath):
            continue
        cfg = _load(gpath)
        if cfg is None:
            continue
        vals = cfg.setdefault("memory", {}).setdefault("values", {})
        changed = []
        obsolete = []
        wrong = []
        for name, d in (data.get("values") or {}).items():
            if not isinstance(d, dict) or not d.get("addr"):
                continue
            cur = vals.get(name)
            if not_learned(cur, d):
                wrong.append(name)                # the game file has the right one / le fichier du jeu a la bonne
                continue
            if _core(cur) == _core(d):
                continue
            if isinstance(cur, dict) and cur.get("ptr") and cur.get("addr") and not d.get("ptr"):
                # le fichier du jeu suit maintenant l'objet qui bouge : l'adresse fixe apprise avant ne tient pas
                obsolete.append(name)
                continue
            new = _core(d)
            note = cur.get("note") if isinstance(cur, dict) else None
            if note and not _about_learning(note):
                new["note"] = note
            vals[name] = new
            changed.append(name)
        if wrong:
            for name in wrong:
                data["values"].pop(name, None)
            try:
                _write(path, data)
                names = ", ".join(wrong)
                log(tr(f"learned/{key}.json : {names} retiré, l'adresse apprise n'était pas la bonne "
                       "(le fichier du jeu a la bonne)",
                       f"learned/{key}.json: {names} removed, the learned address was not the right one "
                       "(the game file has it)"))
            except OSError:
                pass
        if obsolete:
            for name in obsolete:
                data["values"].pop(name, None)
            try:
                _write(path, data)
                names = ", ".join(obsolete)
                log(tr(f"learned/{key}.json : {names} retiré, le fichier du jeu le lit maintenant "
                       "dans l'objet du combattant",
                       f"learned/{key}.json: {names} removed, the game file now reads it "
                       "from the fighter's object"))
            except OSError:
                pass
        if data.get("retroarch") and not cfg.get("retroarch"):
            cfg["retroarch"] = data["retroarch"]
            changed.append("retroarch")
        if changed:
            try:
                _write(gpath, cfg)
            except OSError as e:
                log(tr(f"games/{key}.json non modifiable : {e}", f"games/{key}.json cannot be modified: {e}"))
                continue
            names = ", ".join(changed)
            log(tr(f"Adresses apprises remises dans games/{key}.json ({names})",
                   f"Learned addresses put back into games/{key}.json ({names})"))
            done.append(key)
    return done


def complete(root, log=print):
    """Fichiers créés par learn.bat pour un jeu couvert par une scène commune ("scene_from") :
    ajoute les adresses que la scène commune a gagnées depuis (état des joueurs donné par le BIOS
    par exemple). Ce qui est déjà dans le fichier du jeu ne bouge pas. Renvoie les jeux complétés."""
    from .memvalues import game_values
    games_dir = os.path.join(root, "games")
    templates = {}
    done = []
    for path in sorted(glob.glob(os.path.join(games_dir, "*.json"))):
        cfg = _load(path)
        tkey = cfg.get("scene_from") if cfg else None
        if not isinstance(tkey, str) or not tkey:
            continue
        if tkey not in templates:
            templates[tkey] = _load(os.path.join(games_dir, tkey + ".json"))
        tmpl = templates[tkey]
        if not tmpl:
            continue
        system = ""
        for m in cfg.get("match") or []:
            names = m.get("system") if isinstance(m, dict) else None
            if isinstance(names, list) and names:
                system = names[0]
                break
            if isinstance(names, str) and names:
                system = names
                break
        vals = cfg.setdefault("memory", {}).setdefault("values", {})
        if not isinstance(vals, dict):
            continue
        added = [k for k in game_values(tmpl, system) if k not in vals]
        if not added:
            continue
        tvals = game_values(tmpl, system)
        for k in added:
            vals[k] = tvals[k]
        key = os.path.basename(path)[:-5]
        try:
            _write(path, cfg)
        except OSError as e:
            log(tr(f"games/{key}.json non modifiable : {e}", f"games/{key}.json cannot be modified: {e}"))
            continue
        added_names = ", ".join(added)
        log(tr(f"games/{key}.json complété avec la scène commune {tkey} ({added_names})",
               f"games/{key}.json completed from the shared scene {tkey} ({added_names})"))
        done.append(key)
    return done
