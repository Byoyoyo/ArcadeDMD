"""What a game file must look like, checked when it is loaded (1.40.2). A file is written by hand or by a tool, and one
field of the wrong kind (a text where a table is expected) used to stop every game from being recognised, or to turn
the HD screen off until the next start. The part that is wrong is now left out, with a line in the log, and the rest of
the file is kept.

Ce qu'un fichier de jeu doit être, vérifié à son chargement. Un champ du mauvais genre (un texte là où une table est
attendue) pouvait empêcher tous les jeux d'être reconnus, ou éteindre l'écran HD jusqu'au redémarrage. La partie fausse
est maintenant écartée, avec une ligne dans le journal, et le reste du fichier est gardé."""

from .i18n import tr

NUM = (int, float)
TOP = {"match": list, "memory": dict, "hd": dict, "derived": dict, "demo": dict, "moves": dict, "titles": dict,
       "per_game": dict, "retroarch": dict, "scene": dict, "tag": dict, "specials": dict, "hyper": dict, "buttons": dict,
       "coins": dict, "activity": dict, "clone_of": dict, "capture_renames": dict, "title": str, "scene_from": str,
       "fallback": bool, "demo_hand": bool}
MEMORY = {"values": dict, "cpu": str, "learn_ranges": list}
VALUE = {"type": str, "addr": str, "ptr": str, "bytes": int, "count": int, "stride": int, "shift": int, "round": int,
         "min": int, "max": int, "start": int, "hold_zero": int, "human": int, "mult": NUM, "add": NUM, "delay": NUM,
         "mask": (int, str), "zero_from": (int, str), "fast": bool, "mame_only": bool, "ptr_range": list, "valid": list}
HD = {"scene": str, "stages": list, "places": list, "fields": list, "field_y": list, "boss_slots": list, "per_game": dict,
      "boss_life": dict, "boss_parts": dict, "boss_stages": dict, "boss_flag": str, "power_label": str, "power_timer": str,
      "max_buttons": str, "dynamic": bool, "hand": bool, "max_dm_free": bool, "fight_after": NUM, "ready_go": NUM,
      "health_drain": NUM, "boss_min": int, "maxv_full": int, "minor_idle": int, "minor_min": int, "pow_full": int,
      "show_time": int, "stock_max": int}
DERIVED = {"names": (dict, list), "pick": list, "distinct": list, "all": list, "between": list, "eq": list, "first": list,
           "join": list, "sum": list, "team": list, "at": (dict, str), "value": (int, str)}
WORDS = {dict: ("une table {...}", "a table {...}"), list: ("une liste [...]", "a list [...]"), str: ("un texte", "a text"),
         bool: ("true ou false", "true or false"), int: ("un nombre entier", "a whole number"), float: ("un nombre", "a number")}


def _is(v, kind):
    kinds = kind if isinstance(kind, tuple) else (kind,)
    if isinstance(v, bool):                       # true is not a number here / true n'est pas un nombre ici
        return bool in kinds
    return isinstance(v, kinds)


def _want(kind):
    kinds = kind if isinstance(kind, tuple) else (kind,)
    return tr(" ou ", " or ").join(dict.fromkeys(tr(*WORDS[k]) for k in kinds))


def _fields(obj, table, where, out):
    """The fields of obj that are of the wrong kind, taken out. / Les champs du mauvais genre, retirés."""
    bad = [k for k, kind in table.items() if k in obj and obj[k] is not None and not _is(obj[k], kind)]
    for k in bad:
        out.append(tr(f"{where}{k} doit être {_want(table[k])}", f"{where}{k} must be {_want(table[k])}"))
        del obj[k]
    return bad


def clean_game(game):
    """(the game file with its wrong parts left out, or None when nothing of it can be kept ; what was wrong).
    / (le fichier de jeu sans ses parties fausses, ou None s'il n'y a rien à en garder ; ce qui était faux)."""
    out = []
    if not isinstance(game, dict):
        return None, [tr("le fichier doit contenir une table {...}", "the file must hold one table {...}")]
    _fields(game, TOP, "", out)
    match = game.get("match")
    if isinstance(match, list) and any(not isinstance(r, dict) for r in match):
        out.append(tr("match doit lister des tables {...}", "match must list tables {...}"))
        game["match"] = [r for r in match if isinstance(r, dict)]
    memory = game.get("memory")
    if isinstance(memory, dict):
        _fields(memory, MEMORY, "memory.", out)
        values = memory.get("values")
        if isinstance(values, dict):
            for name in list(values):
                spec = values[name]
                if not isinstance(spec, dict):
                    out.append(tr(f"memory.values.{name} doit être une table {{...}}", f"memory.values.{name} must be a table {{...}}"))
                    del values[name]
                elif _fields(spec, VALUE, f"memory.values.{name}.", out):
                    del values[name]              # a value with a wrong field is not read at all / pas lue du tout
    hd = game.get("hd")
    if isinstance(hd, dict):
        _fields(hd, HD, "hd.", out)
    derived = game.get("derived")
    if isinstance(derived, dict):
        for name in list(derived):
            spec = derived[name]
            if not isinstance(spec, dict):
                out.append(tr(f"derived.{name} doit être une table {{...}}", f"derived.{name} must be a table {{...}}"))
                del derived[name]
            elif _fields(spec, DERIVED, f"derived.{name}.", out):
                del derived[name]
    return game, out
