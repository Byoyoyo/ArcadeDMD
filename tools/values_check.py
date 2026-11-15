"""Checks each value of a game file against a game the robot recorded (1.39): runtime/robot/<game>.zip holds the whole
memory twice a second (.ram) and a screenshot every ten seconds. The values are read from the memory with the file as
it is now, the way the engine has them (read, then the file's "tag", then its "derived"), so a fix in the file shows
at once, without playing the game again.

    python tools/values_check.py runtime/robot/garou.zip
        one line per value: ok, BAD, flat (never moved), none (no address yet), with what it did
    python tools/values_check.py garou.zip --sheet garou.jpg
        six screenshots with, under each, what the file reads at that second: the check by eye (needs Pillow)
    python tools/values_check.py garou.zip --find
        looks in the whole memory for the timer and for the two life bars (needs numpy)
    python tools/values_check.py garou.zip --match 45:35 105:25~1 166:57
        the bytes that hold the numbers read on the screenshots: second of the game, value, tolerance; "bcd" first for
        a number kept in decimal digits (needs numpy)
    python tools/values_check.py garou.zip --round-bars 100
        round by round, the bytes that start at this full value and only go down: fighters whose place in memory
        changes from a round to the next (needs numpy)
    python tools/values_check.py garou.zip --relog garou.log
        writes the game again as a capture read with the file as it is now, for tools/replay_capture.py

What a verdict rests on. A timer counts down one by one and starts again from its top. A life bar goes down hit after
hit, comes back to full, and reads full when a round starts (the timer back at its top). A score only rises. The side a
fighter faces takes two values. A verdict "ok" says the value behaves as it should, not that its scale is right: the
sheet is there for that.

Vérifie chaque valeur d'un fichier de jeu contre une partie enregistrée par le robot. Les valeurs sont lues dans la
mémoire avec le fichier tel qu'il est maintenant, comme le moteur les voit : une correction se voit tout de suite, sans
rejouer. --sheet : six captures d'écran avec ce que lit le fichier à la même seconde, pour vérifier à l'œil. --find :
cherche le chrono et les deux barres de vie dans toute la mémoire. --match : les octets qui valent les nombres lus sur
les captures. --round-bars : round par round, les octets qui partent du plein et ne font que descendre. --relog : réécrit
la partie comme une capture lue avec le fichier actuel, pour tools/replay_capture.py.
"""
import argparse
import datetime
import io
import json
import os
import re
import struct
import sys
import zipfile
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dmd.memvalues import decode, derive, game_values, resolve_value  # noqa: E402

SHOW = ("time", "health", "health_p2", "p1_char", "p2_char", "round", "rounds", "rounds_p2", "backdrop", "score",
        "score_p2", "power", "power_p2")


# ---------------------------------------------------------------------- the recording
class Recording:
    """A game of the robot, from its zip or from the folder it was unpacked in. / Une partie du robot."""

    def __init__(self, path):
        self.path = path
        self.zip = zipfile.ZipFile(path) if os.path.isfile(path) else None
        names = self.zip.namelist() if self.zip else [
            os.path.relpath(os.path.join(d, f), path).replace(os.sep, "/") for d, _, fs in os.walk(path) for f in fs]
        ram = sorted(n for n in names if n.endswith(".ram"))
        if not ram:
            raise SystemExit(f"{path}: no .ram in it / pas de .ram")
        self.shots = sorted(n for n in names if n.lower().endswith((".png", ".jpg", ".bmp")))
        self.head, self.snaps = self._snaps(self.read(ram[0]))
        self.game = self.head.get("rom") or self.head.get("game") or os.path.basename(ram[0]).split("-")[0]
        self.base = self.head["base"]

    def read(self, name):
        if self.zip:
            return self.zip.read(name)
        with open(os.path.join(self.path, name), "rb") as f:
            return f.read()

    @staticmethod
    def _snaps(data):
        """The header and the snapshots (seconds, memory), as tools/ram_diff.py reads a file. / Les instantanés."""
        f = io.BytesIO(data)
        head = json.loads(f.readline().decode("utf-8"))
        snaps, prev = [], None
        while True:
            rec = f.read(12)
            if len(rec) < 12:
                break
            t, n = struct.unpack("<dI", rec)
            z = f.read(n)
            if len(z) < n:
                break
            mem = zlib.decompress(z)
            if head.get("delta") and prev is not None and len(prev) == len(mem):
                mem = (int.from_bytes(mem, "big") ^ int.from_bytes(prev, "big")).to_bytes(len(mem), "big")
            prev = mem
            snaps.append((t, mem))
        return head, snaps

    def shot_times(self):
        """[(second of the game, name)] from the time in each screenshot's name. / L'heure dans le nom de la capture."""
        start = datetime.datetime.strptime(self.head["date"], "%Y-%m-%d %H:%M:%S")
        out = []
        for n in self.shots:
            m = re.search(r"-(\d{6})-(\d{6})\.", os.path.basename(n))
            if m:
                when = datetime.datetime.strptime(m.group(1) + m.group(2), "%y%m%d%H%M%S")
                out.append(((when - start).total_seconds(), n))
        return out

    def matrix(self):
        """(seconds, memory as a table snapshot by byte), for the searches. / La mémoire en tableau, pour chercher."""
        import numpy as np
        t = np.array([s[0] for s in self.snaps])
        m = np.frombuffer(b"".join(s[1] for s in self.snaps), dtype=np.uint8).reshape(len(self.snaps), -1)
        return t, m


def game_file(game):
    with open(os.path.join(ROOT, "games", game + ".json"), encoding="utf-8") as f:
        return json.load(f)


def read_at(j, game, rec, k, extra=None):
    """Every value at snapshot k, as the engine has it. / Toutes les valeurs à l'instantané k, comme le moteur."""
    mem = rec.snaps[k][1]
    base = rec.base

    def getb(a):
        return mem[a - base] if 0 <= a - base < len(mem) else None
    defs = {n: d for n, d in game_values(j, game).items() if not d.get("mame_only") and d.get("addr")}
    defs.update(extra or {})
    vals = {n: decode(d, getb, True) for n, d in defs.items()}
    raw = dict(vals)
    for n, spec in (j.get("tag") or {}).items():
        if isinstance(spec, dict):
            v = resolve_value(spec, vals)
            if v is not None:
                vals[n] = v
    try:
        vals.update(derive(j.get("derived") or {}, vals))
    except Exception:                                             # a file being written / un fichier en cours d'écriture
        pass
    return raw, vals


def series(j, game, rec):
    names, cols = [], {}
    for k in range(len(rec.snaps)):
        _, vals = read_at(j, game, rec, k)
        for n, v in vals.items():
            if n not in cols:
                names.append(n)
                cols[n] = [None] * k
            cols[n].append(v)
        for n in names:
            if len(cols[n]) <= k:
                cols[n].append(None)
    return cols


def runs(seq):
    out = []
    for i, v in enumerate(seq):
        if out and out[-1][0] == v:
            out[-1][2] += 1
        else:
            out.append([v, i, 1])
    return out


# ---------------------------------------------------------------------- the verdicts
def playing(ser):
    """The snapshots where the BIOS says player 1 plays a game. / Les instantanés où le joueur 1 joue."""
    pm, bm = ser.get("p1_mode"), ser.get("bios_mode")
    if not pm:
        return list(range(len(next(iter(ser.values()), []))))
    return [i for i, v in enumerate(pm) if v == 1 and (not bm or bm[i] == 2)]


def round_starts(ser, idx):
    """The snapshots where the timer comes back to its top. / Les instantanés où le chrono revient à son plus haut."""
    tm = ser.get("time")
    if not tm:
        return []
    on = set(idx)
    vals = [v for i, v in enumerate(tm) if i in on and isinstance(v, (int, float))]
    if not vals:
        return []
    top = max(vals)
    return [i for i in range(1, len(tm)) if i in on and tm[i] == top and tm[i - 1] != top]


def judge(name, d, seq, idx, starts, ser):
    vals = [seq[i] for i in idx if isinstance(seq[i], (int, float)) and not isinstance(seq[i], bool)]
    if not vals:
        return "?", "never read"
    r = runs(vals)
    dist = set(vals)
    steps = [b[0] - a[0] for a, b in zip(r, r[1:])]
    ups, downs = sum(1 for s in steps if s > 0), sum(1 for s in steps if s < 0)
    flat = len(dist) == 1
    base = name[:-3] if name.endswith("_p2") else name
    hi = d.get("max")
    if base == "time":
        top = max(vals)
        ones = sum(1 for s in steps if s == -1)
        refill = sum(1 for a, b in zip(r, r[1:]) if b[0] > a[0] and b[0] >= max(30, top - 1))
        other = len(steps) - ones - refill - sum(1 for a, b in zip(r, r[1:]) if b[0] == 0)
        if flat:
            return "BAD", f"always {vals[0]}"
        if top > 999 and downs >= 20 and ups <= 0.2 * downs:          # not seconds: the scene turns it into the game's number
            return "", f"a counter that runs down from {top}, not seconds: to check on the sheet with the scene's own rule"
        if ones >= 20 and other <= 0.25 * ones and top <= 999:
            return "ok", f"{ones} seconds counted down, {refill} starts from {top}"
        return "BAD", f"{ones} steps of one second, {other} other changes, top {top}"
    if base == "health":
        full = hi if isinstance(hi, (int, float)) else max(vals)
        refill = sum(1 for a, b in zip(r, r[1:]) if b[0] > a[0] and b[0] >= 0.95 * full)
        if flat:
            return "BAD", f"always {vals[0]}"
        if len(dist) < 4:
            return "BAD", f"only {sorted(dist)}"
        if not (downs >= 4 and refill >= 1 and ups - refill <= max(2, 0.5 * downs)):
            return "BAD", f"{downs} downs, {refill} refills, {ups - refill} other ups, {len(dist)} levels"
        other = ser.get("health" if name.endswith("_p2") else "health_p2")
        if starts:                                                # full when a round starts, this bar or the other
            def top_of(col, i):
                got = [col[k] for k in range(i, min(i + 5, len(col))) if isinstance(col[k], (int, float))]
                return max(got) if got else None
            here = [top_of(seq, i) for i in starts]
            there = [top_of(other, i) for i in starts] if other else [None] * len(starts)
            one = sum(1 for a, b in zip(here, there) if (a is not None and a >= 0.98 * full) or (b is not None and b >= 0.98 * full))
            mine = sum(1 for a in here if a is not None and a >= 0.98 * full)
            if one < 0.75 * len(starts) or mine == 0:
                seen = sorted({round(a) for a in here if a is not None})
                return "BAD", f"reads {seen} when a round starts, not {full:g}: its full value is not the right one"
            return "ok", f"{downs} hits taken, full at {mine} of {len(starts)} round starts"
        return "ok", f"{downs} hits taken, {refill} refills"
    if base in ("round", "rounds"):
        if flat:
            return "flat", f"always {vals[0]}"
        if max(vals) > 9 or min(vals) < 0 or len(r) > 60:
            return "BAD", f"{min(vals)}..{max(vals)}, {len(r) - 1} changes"
        return "ok", f"{min(vals)}..{max(vals)}, {len(r) - 1} changes"
    if base == "score":
        if flat:
            return "flat", f"always {vals[0]}"
        if ups >= 3 and downs <= max(3, 0.2 * ups):
            small = max(vals) < 100
            return ("ok", f"{ups} rises, up to {max(vals)}") if not small else \
                ("BAD", f"never above {max(vals)}: not a score")
        return "BAD", f"{ups} ups, {downs} downs"
    if base in ("power", "_pow", "_stock", "_maxv", "power_level", "_dm"):
        if flat:
            return "flat", f"always {vals[0]}"
        if isinstance(hi, (int, float)) and max(vals) > hi:
            return "BAD", f"up to {max(vals)} over {hi}"
        return "ok", f"{min(vals)}..{max(vals)}, {len(r) - 1} changes"
    if base == "backdrop":
        if len(r) > 40:
            return "BAD", f"{len(r)} changes"
        return ("flat" if flat else "ok"), f"values {sorted(dist)}"
    if base in ("_p1_dir", "_p2_dir"):
        top = sorted(((vals.count(v), v) for v in dist), reverse=True)
        if flat:
            return "flat", f"always {vals[0]}"
        cover = sum(c for c, _ in top[:2]) / len(vals)
        if cover >= 0.9:
            return "ok", f"{top[0][1]} and {top[1][1]}, {len(r) - 1} turns"
        return "BAD", f"{len(dist)} values, two of them {cover:.0%} of the time"
    return "", f"always {vals[0]}" if flat else f"{len(dist)} values {min(vals)}..{max(vals)}, {len(r) - 1} changes"


def check(rec, j):
    game = rec.game
    ser = series(j, game, rec)
    idx = playing(ser)
    if len(idx) < 60:
        return ser, idx, [("", "BAD", "the BIOS never says player 1 plays: no game was played")]
    starts = round_starts(ser, idx)
    defs = game_values(j, game)
    out = []
    for name, seq in ser.items():
        if name.startswith(("bios_", "_in_")) or name in ("p1_mode", "p2_mode"):
            continue
        if name in ("p1_char", "p2_char"):
            got = [seq[i] for i in idx if seq[i]]
            cover = len(got) / len(idx)
            who = sorted(set(got))
            out.append((name, "ok" if cover >= 0.5 else "BAD", f"named {cover:.0%} of the time: {', '.join(who[:10])}"))
            continue
        d = defs.get(name) or ({"max": 100} if name.startswith("health") else {})
        out.append((name,) + judge(name, d, seq, idx, starts, ser))
    for name, d in defs.items():
        if not d.get("mame_only") and not d.get("addr"):
            out.append((name, "none", "no address yet"))
    stages = (j.get("hd") or {}).get("stages") if isinstance(j.get("hd"), dict) else None
    if stages and "backdrop" in ser:
        seen = sorted({ser["backdrop"][i] for i in idx if isinstance(ser["backdrop"][i], int)})
        out.append(("stages", "", "met: " + ", ".join(f"{v} {stages[v] if 0 <= v < len(stages) else '(no theme)'}" for v in seen)))
    return ser, idx, out


# ---------------------------------------------------------------------- the sheet
def sheet(rec, j, out, count=6, extra=None):
    from PIL import Image, ImageDraw, ImageFont
    game = rec.game
    shots = rec.shot_times()
    if not shots:
        raise SystemExit("no screenshot in this recording / pas de capture d'écran")
    times = [s[0] for s in rec.snaps]

    def near(t):
        return min(range(len(times)), key=lambda i: abs(times[i] - t))
    pool = []
    for n, (t, name) in enumerate(shots):
        _, v = read_at(j, game, rec, near(t))
        tm = v.get("time")
        if v.get("p1_mode") in (1, None) and (not isinstance(tm, (int, float)) or tm >= 1):
            pool.append(n)
    pool = pool or list(range(len(shots)))
    step = len(pool) / count
    pick = sorted({pool[min(len(pool) - 1, int(k * step + step / 2))] for k in range(count)})
    font = ImageFont.load_default(size=17)
    w, h, cap, cols = 640, 448, 74, 3
    rows = (len(pick) + cols - 1) // cols
    im = Image.new("RGB", (w * cols, (h + cap) * rows), (20, 20, 24))
    dr = ImageDraw.Draw(im)
    for n, k in enumerate(pick):
        t, name = shots[k]
        x, y = (n % cols) * w, (n // cols) * (h + cap)
        try:
            im.paste(Image.open(io.BytesIO(rec.read(name))).convert("RGB").resize((w, h), Image.NEAREST), (x, y))
        except Exception as e:
            dr.text((x + 8, y + 8), f"unreadable: {e}", fill=(255, 80, 80), font=font)
        _, v = read_at(j, game, rec, near(t), extra)
        keys = [n2 for n2 in SHOW if v.get(n2) is not None] + list(extra or {})
        words = [f"{n2}={round(v[n2], 1) if isinstance(v[n2], float) else v[n2]}" for n2 in keys]
        lines = [f"t={t:.0f}s"]
        for word in words:
            if dr.textlength(lines[-1] + "  " + word, font=font) > w - 12:
                lines.append(word)
            else:
                lines[-1] += "  " + word
        for i, line in enumerate(lines[:3]):
            dr.text((x + 6, y + h + 4 + i * 22), line, fill=(255, 220, 90) if i == 0 else (235, 235, 235), font=font)
    im.save(out, quality=84)
    return len(pick)


# ---------------------------------------------------------------------- the searches (numpy)
def _bcd(m):
    import numpy as np
    hi, lo = m >> 4, m & 15
    return np.where((hi <= 9) & (lo <= 9), hi.astype(np.int16) * 10 + lo, -1)


def _play_mask(rec, m):
    b = rec.base
    if not (0 <= 0x10FDB6 - b < m.shape[1]):
        import numpy as np
        return np.ones(m.shape[0], bool)
    return (m[:, 0x10FDB6 - b] == 1) & (m[:, 0x10FDAF - b] == 2)


def find_timers(rec, top=4):
    """Bytes that count the seconds down, in decimal digits or as a number. / Les octets qui comptent les secondes."""
    import numpy as np
    t, m = rec.matrix()
    play = _play_mask(rec, m)
    out = []
    for kind, v in (("bcd", _bcd(m)), ("u8", m.astype(np.int16))):
        a, b = v[:-1], v[1:]
        ch = (a != b) & (play[:-1] & play[1:])[:, None] & (a >= 0) & (b >= 0)
        ones = (ch & (b - a == -1)).sum(0)
        highest = np.where(play[:, None], v, -1).max(0)
        refill = (ch & (b > a) & (b >= np.maximum(30, highest - 1)[None, :])).sum(0)
        other = ch.sum(0) - ones - refill - (ch & (b == 0)).sum(0)
        score = ones - 4 * other
        for i in np.argsort(-score)[:top]:
            if ones[i] >= 20 and refill[i] >= 1:
                out.append((int(score[i]), kind, rec.base + int(i), int(ones[i]), int(refill[i]), int(highest[i])))
    return sorted(out, reverse=True)[:top]


def find_bars(rec, rounds=None):
    """Bytes and words that behave as a life bar, and the pairs of them a round distance apart with the same full
    value: player 1 and player 2. Read signed (a bar below zero at a K.O. reads 0xFF) and unsigned.
    / Les octets et mots qui se comportent comme une barre de vie, et leurs paires."""
    import numpy as np
    t, m = rec.matrix()
    play = _play_mask(rec, m)
    w = (m[:, :-1].astype(np.int32) << 8) | m[:, 1:]
    found = []
    for kind, v in (("s8", m.astype(np.int8).astype(np.int32)), ("u8", m.astype(np.int32)),
                    ("s16", w.astype(np.int16).astype(np.int32)), ("u16", w)):
        vp = v[play]
        big = 128 if kind == "u8" else 32768
        if kind in ("u8", "u16") and not (vp >= big).any():
            continue
        a, b = vp[:-1], vp[1:]
        d = b - a
        full = vp.max(0)
        isref = (d > 0) & (b == full[None, :])
        refill = isref.sum(0)
        down = (d < 0).sum(0)
        lost = np.where((d < 0) & (a >= 0), -d, 0).sum(0)
        back = np.where((d > 0) & ~isref, d, 0).sum(0)
        atfull = (vp == full[None, :]).mean(0)
        most = 40 if rounds is None else rounds + 3
        ok = (down >= 4) & (refill >= 2) & (refill <= most) & (back <= 0.3 * lost) & (atfull >= 0.03) \
            & (atfull <= 0.8) & (full >= 8) & ((d == -1).sum(0) <= 0.6 * down)
        for i in np.nonzero(ok)[0]:
            if (kind in ("s16", "u16") and i % 2) or (kind in ("u8", "u16") and vp[:, i].max() < big):
                continue
            if len(np.unique(vp[:, i])) < 5:
                continue
            found.append({"kind": kind, "addr": rec.base + int(i), "down": int(down[i]), "refill": int(refill[i]),
                          "back": int(back[i]), "lost": int(lost[i]), "full": int(full[i]), "low": int(vp[:, i].min())})
    pairs = []
    for i, a in enumerate(found):
        for b in found[i + 1:]:
            gap = abs(b["addr"] - a["addr"])
            if a["kind"] == b["kind"] and a["full"] == b["full"] and 0x20 <= gap <= 0x2000:
                lo, hi = (a, b) if a["addr"] < b["addr"] else (b, a)
                nice = 3 if gap % 0x100 == 0 else 2 if gap % 0x10 == 0 else 1 if gap % 2 == 0 else 0
                pairs.append((nice, min(a["down"], b["down"]), lo, hi, gap))
    return sorted(pairs, key=lambda p: (p[0], p[1]), reverse=True)


def match(rec, wants, as_bcd=False):
    """The bytes whose value, around each given second, is the number read on a screenshot. / Les octets qui valent."""
    import numpy as np
    t, m = rec.matrix()
    v = _bcd(m) if as_bcd else m.astype(int)
    ok = np.ones(m.shape[1], bool)
    for when, val, tol in wants:
        seg = v[np.nonzero(np.abs(t - when) <= 1.2)[0]]           # a screenshot's second is known to a second or so
        ok &= (np.abs(seg - val) <= tol).any(0)
    return [rec.base + int(i) for i in np.nonzero(ok)[0]]


def round_bars(rec, j, full):
    """Round by round, the bytes that start at `full` and only go down. / Round par round."""
    import numpy as np
    t, m = rec.matrix()
    ser = series(j, rec.game, rec)
    starts = round_starts(ser, playing(ser))
    out = []
    for a, b in zip(starts, starts[1:] + [len(t)]):
        seg = m[a:min(b, a + 400)].astype(int)
        if len(seg) < 12:
            continue
        d = np.diff(seg, axis=0)
        ok = (seg[:6].max(0) == full) & (seg.max(0) == full) & ((d > 0).sum(0) <= 1) & ((d < 0).sum(0) >= 2)
        out.append((float(t[a]), [(rec.base + int(i), int(seg[-1][i])) for i in np.nonzero(ok)[0][:24]]))
    return out


# ---------------------------------------------------------------------- the game written again as a capture
def relog(rec, j, out):
    """The raw values of every snapshot, each change on a line, as dmd/capture.py writes a game: the engine applies the
    file's "tag" and "derived" itself when it replays. The stick is read twice a second only, too coarse for the moves
    recognised at the stick. / Les valeurs brutes de chaque instantané, comme une capture : le moteur applique lui-même
    "tag" et "derived" en rejouant."""
    game = rec.game
    head = {"version": rec.head.get("version"), "game": game, "system": game, "parent": None, "title": j.get("title"),
            "date": rec.head.get("date"), "values": sorted(game_values(j, game)), "from": "values_check --relog"}
    last, lines = {}, 0
    with open(out, "w", encoding="utf-8") as f:
        f.write("# " + json.dumps(head, ensure_ascii=False) + "\n")
        for k, (t, _) in enumerate(rec.snaps):
            raw, _ = read_at(j, game, rec, k)
            for name, v in raw.items():
                if v is None or isinstance(v, (list, str)) or last.get(name) == v:
                    continue
                last[name] = v
                f.write(f"{t:.3f} {name} {v}\n")
                lines += 1
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("recording", help="runtime/robot/<game>.zip, or the folder it was unpacked in")
    ap.add_argument("--game", help="the game file to read it with (default: the recording's own)")
    ap.add_argument("--sheet", metavar="OUT.jpg")
    ap.add_argument("--find", action="store_true")
    ap.add_argument("--match", nargs="+", metavar="T:VALUE[~TOL]")
    ap.add_argument("--round-bars", type=lambda s: int(s, 0), metavar="FULL")
    ap.add_argument("--relog", metavar="OUT.log")
    a = ap.parse_args()
    rec = Recording(a.recording)
    if a.game:
        rec.game = a.game
    j = game_file(rec.game)
    if a.match:
        words = list(a.match)
        as_bcd = words[0] == "bcd"
        wants = []
        for word in words[1:] if as_bcd else words:
            when, _, rest = word.partition(":")
            val, _, tol = rest.partition("~")
            wants.append((float(when), int(val, 0), int(tol or 0)))
        got = match(rec, wants, as_bcd)
        print(f"{len(got)} place(s): " + " ".join(f"{x:#x}" for x in got[:60]))
        return 0
    if a.round_bars is not None:
        for t, cells in round_bars(rec, j, a.round_bars):
            print(f"round at {t:.0f} s: " + " ".join(f"{x:#x}(→{v})" for x, v in cells))
        return 0
    if a.relog:
        print(f"{relog(rec, j, a.relog)} lines in {a.relog}")
        return 0
    if a.sheet:
        print(f"{sheet(rec, j, a.sheet)} screenshots on {a.sheet}")
        return 0
    ser, idx, out = check(rec, j)
    print(f"{rec.game} ({j.get('title')}): {len(rec.snaps)} snapshots, player 1 plays in {len(idx)}, "
          f"{len(rec.shots)} screenshots")
    for name, verdict, why in out:
        print(f"  {verdict:4s} {name:14s} {why}")
    if a.find:
        timers = find_timers(rec)
        print("timers found (address, seconds counted down, starts, top):")
        for _, kind, addr, ones, refill, top in timers:
            print(f"  {kind:3s} {addr:#x}  {ones} s, {refill} starts from {top}")
        print("pairs of life bars found (player 1 / player 2, full value, lowest, hits, refills):")
        for _, _, lo, hi, gap in find_bars(rec, timers[0][4] if timers else None)[:8]:
            print(f"  {lo['kind']:3s} {lo['addr']:#x} / {hi['addr']:#x} (+{gap:#x})  full {lo['full']}, lowest "
                  f"{lo['low']}/{hi['low']}, hits {lo['down']}/{hi['down']}, refills {lo['refill']}/{hi['refill']}")
    return 1 if any(v == "BAD" for _, v, _ in out) else 0


if __name__ == "__main__":
    sys.exit(main())
