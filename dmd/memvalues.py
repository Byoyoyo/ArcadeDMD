"""Decodes RAM values (score, lives...) from raw bytes, the same way as the MAME plugin.
Definitions come from games/*.json, section memory.values; also computes "derived" values.

Décodage des valeurs RAM (score, vies...) à partir d'octets, comme le plugin MAME.

Les définitions sont celles de games/*.json, rubrique memory.values :
  {"addr": "0x100377", "type": "u8"}
  {"addr": "0xFFFE26", "type": "be", "bytes": 4, "mult": 10}
Types : u8, u16, u32, s8, s16, be, le, bcd, bcd_le, digits, digits_le.
"""


def parse_addr(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        s = v.strip()
        if s.startswith(("0x", "0X")):
            s = s[2:]
        elif s.startswith("$"):
            s = s[1:]
        if not s:
            return None
        try:
            return int(s, 16)
        except ValueError:
            return None
    return None


def value_size(d):
    t = (d.get("type") or "u8").lower()
    n = d.get("bytes")
    if isinstance(n, int) and n > 0:
        return n
    if "32" in t:
        return 4
    if "16" in t:
        return 2
    return 1


def value_span(d):
    """(premier, dernier) octet à lire d'office pour une valeur : son pointeur pour une valeur "ptr", sinon elle-même."""
    p = parse_addr(d.get("ptr"))
    if p is not None:
        return p, p + 3
    a = parse_addr(d.get("addr"))
    if a is None:
        return None
    return a, a + value_size(d) - 1


def target(d, getb, big_endian=True):
    """Adresse de la valeur. Avec "ptr", l'objet bouge en mémoire (Samurai Shodown...) : adresse lue à "ptr"
    (32 bits), plus "addr" qui est alors le décalage dans l'objet. "ptr_range" écarte un pointeur pas encore prêt."""
    off = parse_addr(d.get("addr"))
    if off is None:
        return None
    p = parse_addr(d.get("ptr"))
    if p is None:
        return off
    raw = [getb(p + i) for i in range(4)]
    if any(b is None for b in raw):
        return None
    base = int.from_bytes(bytes(raw), "big" if big_endian else "little") & 0xFFFFFF
    rng = d.get("ptr_range")
    if isinstance(rng, list) and len(rng) == 2:
        lo, hi = parse_addr(rng[0]), parse_addr(rng[1])
        if lo is not None and hi is not None and not lo <= base <= hi:
            return None
    return base + off


def decode(d, getb, big_endian=True):
    """Valeur décodée, getb(adresse) renvoyant un octet (ou None si illisible)."""
    addr = target(d, getb, big_endian)
    if addr is None:
        return None
    t = (d.get("type") or "u8").lower()
    n = value_size(d)
    raw = [getb(addr + i) for i in range(n)]
    if any(b is None for b in raw):
        return None
    if t in ("u16", "u32", "s16"):
        v = int.from_bytes(bytes(raw), "big" if big_endian else "little")
        if t == "s16" and v >= 0x8000:
            v -= 0x10000
    elif t == "u8":
        v = raw[0]
    elif t == "s8":
        v = raw[0] - 0x100 if raw[0] >= 0x80 else raw[0]
    elif t in ("be", "le"):
        v = int.from_bytes(bytes(raw), "big" if t == "be" else "little")
    elif t in ("bcd", "bcd_le"):
        seq = raw if t == "bcd" else raw[::-1]
        v = 0
        for b in seq:
            hi, lo = b >> 4, b & 15
            v = v * 100 + (hi if hi <= 9 else 0) * 10 + (lo if lo <= 9 else 0)
    elif t in ("digits", "digits_le"):
        off = parse_addr(d.get("digit_offset")) or 0
        seq = raw if t == "digits" else raw[::-1]
        v = 0
        for b in seq:
            dg = b - off
            v = v * 10 + (dg if 0 <= dg <= 9 else 0)
    else:
        return None
    mask = parse_addr(d.get("mask"))
    if mask is not None:
        v &= mask
    shift = d.get("shift")
    if isinstance(shift, int) and shift > 0:
        v >>= shift
    mult = d.get("mult", 1)
    add = d.get("add", 0)
    v = v * mult + add
    digits = d.get("round")
    if isinstance(digits, int) and not isinstance(digits, bool):
        v = round(v, digits)                    # a percentage of a full bar / un pourcentage de barre pleine
    lo, hi = d.get("min"), d.get("max")
    if isinstance(lo, (int, float)) and v < lo:
        v = lo
    if isinstance(hi, (int, float)) and v > hi:
        v = hi
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return v


def game_values(game, system="", parent=""):
    """Adresses d'un jeu : celles du fichier, plus celles propres au romset dans un modèle ("per_game")."""
    g = game or {}
    vals = dict(((g.get("memory") or {}).get("values")) or {})
    pg = g.get("per_game")
    if isinstance(pg, dict):
        co = g.get("clone_of") if isinstance(g.get("clone_of"), dict) else {}
        extra = pg.get(system or "") or pg.get(co.get(system or "", "")) or pg.get(parent or "")
        if isinstance(extra, dict):
            vals.update(extra)
    return vals


# --------------------------------------------------------------------------
# valeurs calculées à partir d'autres ("derived" dans games/*.json)
# --------------------------------------------------------------------------
# Exemple, le personnage en train de se battre dans King of Fighters '98 :
#   "p1_char": {"pick": ["_p1_ch0", "_p1_ch1", "_p1_ch2"],
#               "at": {"pick": ["_p1_ord0", "_p1_ord1", "_p1_ord2"], "at": "_p1_lost"},
#               "names": {"0": "KYO", "10": "RALF", ...}}
# pick : l'élément de la liste désigné par "at" (un nom de valeur, un nombre ou un autre calcul)
# find : la position dans la liste de la valeur égale à "eq"
# names : nombre lu -> texte affiché (sans correspondance, la valeur reste vide)
#         {"en": [...], "fr": [...]} : les noms dans chaque langue (club de golf, terrain, arme...)

def _resolve(expr, values, depth=0):
    if depth > 8:
        return None
    if isinstance(expr, bool):
        return None
    if isinstance(expr, (int, float)):
        return expr
    if isinstance(expr, str):
        return values.get(expr)
    if not isinstance(expr, dict):
        return None
    if "value" in expr:                       # une valeur lue telle quelle (le plus souvent avec "names")
        return _resolve(expr.get("value"), values, depth + 1)
    if "pick" in expr:
        lst = expr.get("pick")
        idx = _resolve(expr.get("at"), values, depth + 1)
        if not isinstance(lst, list) or isinstance(idx, bool) or not isinstance(idx, int) or not 0 <= idx < len(lst):
            return None
        return _resolve(lst[idx], values, depth + 1)
    if "join" in expr:                        # several values together, "a,b" (a character given by a row and a column)
        parts = [_resolve(x, values, depth + 1) for x in expr.get("join") or []]
        if not parts or any(p is None or isinstance(p, bool) for p in parts):
            return None
        return ",".join(str(int(p)) if isinstance(p, float) and p.is_integer() else str(p) for p in parts)
    if "find" in expr:
        lst = expr.get("find")
        target = _resolve(expr.get("eq"), values, depth + 1)
        if not isinstance(lst, list) or target is None:
            return None
        for i, name in enumerate(lst):
            if _resolve(name, values, depth + 1) == target:
                return i
        return None
    return None


def derive(specs, values):
    """{nom: valeur calculée ou None} pour les définitions "derived" d'un jeu."""
    out = {}
    if not isinstance(specs, dict):
        return out
    for name, spec in specs.items():
        if not isinstance(spec, dict):
            continue
        v = _resolve(spec, values)
        names = spec.get("names")
        if isinstance(names, dict) and names and set(names) <= {"en", "fr"}:   # names in both languages
            from .i18n import lang
            names = names.get(lang()) or names.get("en") or names.get("fr")
        if isinstance(names, dict) and v is not None:
            v = names.get(str(v))
        elif isinstance(names, list) and v is not None:
            v = names[v] if isinstance(v, int) and 0 <= v < len(names) else None
        out[name] = v
    return out
