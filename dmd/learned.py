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
