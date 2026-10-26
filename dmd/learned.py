"""Adresses trouvées par apprendre.bat, gardées aussi dans appris/ pour survivre aux mises à jour.

Une mise à jour d'ArcadeDMD remplace les fichiers games/*.json. Au démarrage, le moteur remet
les adresses apprises dans games/<jeu>.json si elles n'y sont plus. Pour oublier ce qui a été
appris pour un jeu, il suffit de supprimer appris/<jeu>.json.
"""

import glob
import json
import os
import time

DIR = "appris"


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


def save(root, key, values, retroarch=None):
    """Ajoute les valeurs apprises (dict nom -> définition) à appris/<key>.json."""
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
        for name, d in (data.get("values") or {}).items():
            if not isinstance(d, dict) or not d.get("addr"):
                continue
            cur = vals.get(name)
            if _core(cur) == _core(d):
                continue
            new = _core(d)
            note = cur.get("note") if isinstance(cur, dict) else None
            if note and "apprendre" not in note:
                new["note"] = note
            vals[name] = new
            changed.append(name)
        if data.get("retroarch") and not cfg.get("retroarch"):
            cfg["retroarch"] = data["retroarch"]
            changed.append("retroarch")
        if changed:
            try:
                _write(gpath, cfg)
            except OSError as e:
                log(f"games/{key}.json non modifiable : {e}")
                continue
            log(f"Adresses apprises remises dans games/{key}.json ({', '.join(changed)})")
            done.append(key)
    return done


def complete(root, log=print):
    """Fichiers créés par apprendre.bat pour un jeu couvert par une scène commune ("scene_from") :
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
            log(f"games/{key}.json non modifiable : {e}")
            continue
        log(f"games/{key}.json complété avec la scène commune {tkey} ({', '.join(added)})")
        done.append(key)
    return done
