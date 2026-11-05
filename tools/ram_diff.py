"""Reads the memory snapshots ArcadeDMD writes for a game with "ram_dump": true (runtime/captures/<game>-<date>.ram,
the whole memory RetroArch shares once a second) and looks for what a value does over time: the life of a boss goes
down, hit after hit, and ends at 0 when it falls.

    python tools/ram_diff.py runtime/captures/mslug-20261105-200000.ram --list
    python tools/ram_diff.py <file.ram> --down 120 160          # the words that only go down between 120 s and 160 s
    python tools/ram_diff.py <file.ram> --down 120 160 --bytes  # the same with single bytes
    python tools/ram_diff.py <file.ram> --watch 0x1012AA         # one word, snapshot by snapshot
    python tools/ram_diff.py <file.ram> --diff 118 121           # every byte that differs between two snapshots

Lit les instantanés de mémoire qu'ArcadeDMD écrit pour un jeu avec "ram_dump": true, et cherche ce qu'une valeur fait
dans le temps : la vie d'un boss descend coup après coup et finit à 0 quand il tombe."""
import json
import struct
import sys
import zlib


def load(path):
    with open(path, "rb") as f:
        head = json.loads(f.readline().decode("utf-8"))
        snaps = []
        while True:
            rec = f.read(12)
            if len(rec) < 12:
                break
            t, n = struct.unpack("<dI", rec)
            z = f.read(n)
            if len(z) < n:
                break
            snaps.append((t, zlib.decompress(z)))
    return head, snaps


def word(data, off):
    return (data[off] << 8) | data[off + 1]


def down(head, snaps, t0, t1, as_bytes=False, min_steps=3, top=40):
    """The places whose value never goes up between t0 and t1, changes at least min_steps times and ends at 0 or lower
    than it began: a life bar. / Les places qui ne font que descendre et finissent plus bas."""
    base = head["base"]
    sel = [(t, d) for t, d in snaps if t0 <= t <= t1]
    if len(sel) < 2:
        print("pas assez d'instantanés dans cette fenêtre / not enough snapshots in that window")
        return
    size = len(sel[0][1])
    step = 1 if as_bytes else 2
    found = []
    for off in range(0, size - (0 if as_bytes else 1), step):
        seq = [d[off] if as_bytes else word(d, off) for t, d in sel]
        first, last = seq[0], seq[-1]
        if first == 0 or last >= first:
            continue
        ok, changes = True, 0
        for a, b in zip(seq, seq[1:]):
            if b > a:
                ok = False
                break
            if b < a:
                changes += 1
        if ok and changes >= min_steps:
            found.append((changes, off, seq))
    found.sort(key=lambda x: (-x[0], x[1]))
    for changes, off, seq in found[:top]:
        shown = [str(seq[0])] + [str(v) for i, v in enumerate(seq[1:], 1) if v != seq[i - 1]]
        print(f"0x{base + off:06X}  {changes:3d} baisses / drops  {' > '.join(shown[:14])}{' ...' if len(shown) > 14 else ''}")
    if not found:
        print("rien ne fait que descendre ici / nothing only goes down here")


def watch(head, snaps, addr, as_bytes=False):
    off = addr - head["base"]
    for t, d in snaps:
        if 0 <= off < len(d) - 1:
            print(f"{t:8.1f}  {d[off] if as_bytes else word(d, off)}")


def diff(head, snaps, t0, t1):
    a = min(snaps, key=lambda s: abs(s[0] - t0))
    b = min(snaps, key=lambda s: abs(s[0] - t1))
    base = head["base"]
    n = 0
    for off in range(len(a[1])):
        if a[1][off] != b[1][off]:
            n += 1
            if n <= 400:
                print(f"0x{base + off:06X}  {a[1][off]:3d} -> {b[1][off]:3d}")
    print(f"{n} octet(s) différent(s) entre {a[0]:.1f} s et {b[0]:.1f} s / byte(s) differ")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    head, snaps = load(argv[1])
    args = argv[2:]
    as_bytes = "--bytes" in args
    args = [a for a in args if a != "--bytes"]
    if not args or args[0] == "--list":
        print(f"{head.get('rom')} ({head.get('game')}), {head.get('date')}, {len(snaps)} instantané(s) / snapshot(s), "
              f"{snaps[-1][0]:.0f} s, mémoire 0x{head['base']:06X} + 0x{head['size']:X}" if snaps else "vide / empty")
        return 0
    if args[0] == "--down" and len(args) >= 3:
        down(head, snaps, float(args[1]), float(args[2]), as_bytes)
    elif args[0] == "--watch" and len(args) >= 2:
        watch(head, snaps, int(args[1], 16) if args[1].lower().startswith("0x") else int(args[1]), as_bytes)
    elif args[0] == "--diff" and len(args) >= 3:
        diff(head, snaps, float(args[1]), float(args[2]))
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
