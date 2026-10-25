"""Décodage des valeurs RAM (score, vies...) à partir d'octets, comme le plugin MAME.

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


def decode(d, getb, big_endian=True):
    """Valeur décodée, getb(adresse) renvoyant un octet (ou None si illisible)."""
    addr = parse_addr(d.get("addr"))
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
