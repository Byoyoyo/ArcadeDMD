"""Games running in RetroArch: reads the game memory through RetroArch's network commands.

Needs RetroArch 1.19 or newer with Network Commands enabled (UDP port 55355) and a core that shares
its memory (FinalBurn Neo, Genesis Plus GX). Addresses are mapped back to the CPU addresses.

Jeux lancés dans RetroArch : lecture de la mémoire par les commandes réseau.

RetroArch (1.19 ou plus récent) répond en UDP sur le port 55355 quand le réglage
« Commandes réseau » est activé :
  GET_STATUS             -> GET_STATUS PLAYING fb_alpha,mslug,crc32=1234abcd
  READ_CORE_RAM 377 2    -> READ_CORE_RAM 377 03 00   (ou « -1 » si illisible)

« -1 » veut dire que le cœur ne donne pas sa mémoire à RetroArch : FinalBurn Neo et
Genesis Plus GX la donnent, FB Alpha 2012 et les cœurs MAME jamais. GET_STATUS ne dit
pas quel cœur tourne (« fb_alpha » vaut pour FinalBurn Neo comme pour FB Alpha 2012),
wincore.py le retrouve d'après les DLL chargées par retroarch.exe.

Les adresses de READ_CORE_RAM sont celles de RetroAchievements : 0 = début de la RAM
du jeu exposée par le cœur. ArcadeDMD les ramène aux adresses du processeur, pour que
les fichiers games/*.json servent à la fois pour MAME et pour RetroArch :
  "retroarch": {"content": ["mslug"], "ram_base": "0x100000", "ram_size": "0x10000", "swap16": true}
swap16 : le cœur range la RAM du 68000 par mots de 16 bits inversés (FBNeo, Genesis Plus GX).
"""

import json
import os
import socket
import struct
import threading
import time
import zlib

from . import wincore
from .i18n import tr
from .memvalues import decode, game_values, parse_addr, target, value_size, value_span

DEFAULT_PORT = 55355
CHUNK = 512

# réglages par défaut selon l'identifiant de système donné par GET_STATUS
SYSTEM_DEFAULTS = (
    ("mega_drive", 0xFF0000, 0x10000, True),
    ("megadrive", 0xFF0000, 0x10000, True),
    ("genesis", 0xFF0000, 0x10000, True),
)


def version_tuple(text):
    out = []
    for part in (text or "").split(".")[:3]:
        digits = "".join(c for c in part if c.isdigit())
        out.append(int(digits) if digits else 0)
    return tuple(out)


def too_old(version):
    return bool(version) and version_tuple(version) < (1, 19)


def swap16(data):
    b = bytearray(data)
    b[0::2], b[1::2] = data[1::2], data[0::2]
    return bytes(b)


def swap32(data):
    """Bytes reversed in each 32-bit word: the SH-2 of the CPS3 in FinalBurn Neo (RamMain[addr ^ 3]).
    / Octets inversés dans chaque mot de 32 bits, le SH-2 du CPS3 dans FinalBurn Neo."""
    b = bytearray(data)
    b[0::4], b[1::4], b[2::4], b[3::4] = data[3::4], data[2::4], data[1::4], data[0::4]
    return bytes(b)


class RetroArchClient:
    def __init__(self, host="127.0.0.1", port=DEFAULT_PORT, timeout=0.3):
        self.addr = (host, int(port))
        self.timeout = float(timeout)
        self.sock = None
        self.last_reply = None      # réponse brute de la dernière lecture (pour expliquer un échec)

    def close(self):
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None

    def send(self, text):
        """A command without an answer (SCREENSHOT, 1.33 test 35). / Une commande sans réponse."""
        try:
            if self.sock is None:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.sendto((text + "\n").encode("ascii"), self.addr)
            return True
        except OSError:
            return False

    def cmd(self, text, expect=None):
        """Envoie une commande, renvoie la réponse (texte) ou None sans réponse."""
        try:
            if self.sock is None:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s = self.sock
            s.setblocking(False)               # vide les réponses en retard
            try:
                while True:
                    s.recv(65535)
            except OSError:
                pass
            s.settimeout(self.timeout)
            s.sendto((text + "\n").encode("ascii"), self.addr)
            end = time.monotonic() + self.timeout
            while True:
                reply = s.recv(65535).decode("utf-8", "replace").strip()
                if expect is None or reply.startswith(expect):
                    return reply
                if time.monotonic() > end:
                    return None
        except OSError:
            # délai dépassé, ou Windows qui signale qu'aucun programme n'écoute ce port
            self.close()
            return None

    def version(self):
        r = self.cmd("VERSION")
        return r if r and r[:1].isdigit() else None

    def config_param(self, name):
        """The value of one setting of RetroArch (GET_CONFIG_PARAM), or None. / La valeur d'un réglage, ou None."""
        r = self.cmd("GET_CONFIG_PARAM " + name, "GET_CONFIG_PARAM")
        if r is None:
            return None
        parts = r.split(" ", 2)
        if len(parts) < 3 or parts[1] != name:
            return None
        v = parts[2].strip()
        return None if v in ("", "unsupported", "null") else v

    def status(self):
        """None sans réponse, sinon {"state", "system", "content", "crc"}."""
        r = self.cmd("GET_STATUS", "GET_STATUS")
        if r is None:
            return None
        parts = r.split(" ", 2)
        state = parts[1].strip() if len(parts) > 1 else ""
        if state not in ("PLAYING", "PAUSED"):
            return {"state": state or "CONTENTLESS", "system": "", "content": "", "crc": ""}
        rest = parts[2] if len(parts) > 2 else ""
        crc = ""
        i = rest.rfind(",crc32=")
        if i >= 0:
            crc = rest[i + 7:].strip()
            rest = rest[:i]
        system, _, content = rest.partition(",")
        return {"state": state, "system": system.strip(), "content": content.strip(), "crc": crc}

    def read(self, addr, n):
        """n octets à l'adresse RetroAchievements addr, ou None."""
        prefix = "READ_CORE_RAM %x" % addr
        r = self.cmd("READ_CORE_RAM %x %d" % (addr, n), prefix)
        self.last_reply = r
        if r is None:
            return None
        rest = r[len(prefix):].split()
        if not rest or rest[0] == "-1":
            return None
        try:
            data = bytes(int(x, 16) for x in rest)
        except ValueError:
            return None
        return data if len(data) == n else None


    def read_batch(self, reqs):
        """{address: bytes or None} for a few [(address, n)...] sent together, RetroArch answering them at the same image
        (the values of a game read with its stick, 1.32). Unlike read_many, nothing is asked again one by one: a
        RetroArch that stopped answering is seen in its usual time. / Quelques demandes envoyées ensemble, servies à la
        même image ; rien n'est redemandé une par une, un RetroArch qui ne répond plus se voit dans le temps habituel."""
        out = {}
        try:
            if self.sock is None:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:                              # room for a whole batch of replies (Metal Slug 4's enemies, 25 of 1.6 KB)
                    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 262144)    # / la place pour toutes les réponses
                except OSError:
                    pass
            s = self.sock
            s.setblocking(False)
            try:
                while True:
                    s.recv(65535)                 # late replies / les réponses en retard
            except OSError:
                pass
            s.settimeout(self.timeout)
            want = {}
            for a, n in reqs:
                want["READ_CORE_RAM %x " % a] = (a, n)
                s.sendto(("READ_CORE_RAM %x %d\n" % (a, n)).encode("ascii"), self.addr)
            end = time.monotonic() + self.timeout
            while want and time.monotonic() < end:
                try:
                    reply = s.recv(65535).decode("utf-8", "replace").strip() + " "
                except socket.timeout:
                    break
                for prefix in want:
                    if reply.startswith(prefix):
                        a, n = want.pop(prefix)
                        rest = reply[len(prefix):].split()
                        self.last_reply = reply.strip()
                        try:
                            data = bytes(int(x, 16) for x in rest) if rest and rest[0] != "-1" else None
                        except ValueError:
                            data = None
                        out[a] = data if data is not None and len(data) == n else None
                        break
        except OSError:
            self.close()                          # Windows: nobody listens there any more / plus personne n'écoute
        if not out:
            self.last_reply = None
        return out

    def read_many(self, reqs, window=24):
        """{address: bytes or None} for [(address, n)...]. The requests go out a window at a time: RetroArch answers
        all those waiting at each image, where one at a time takes an image each (2 MB of a CV1000 took a minute). A
        reply is known by its address. What did not come back is asked again one by one.
        / Les demandes partent par fenêtres : RetroArch répond à toutes celles qui attendent à chaque image. Une réponse
        se reconnaît à son adresse, ce qui n'est pas revenu est redemandé une par une."""
        out = {}
        try:
            if self.sock is None:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s = self.sock
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1 << 20)   # room for the replies / place pour les réponses
            except OSError:
                pass
            s.setblocking(False)
            try:
                while True:
                    s.recv(65535)
            except OSError:
                pass
            s.settimeout(self.timeout)
            for i in range(0, len(reqs), window):
                want = {}
                for a, n in reqs[i:i + window]:
                    want["READ_CORE_RAM %x " % a] = (a, n)
                    s.sendto(("READ_CORE_RAM %x %d\n" % (a, n)).encode("ascii"), self.addr)
                end = time.monotonic() + max(self.timeout, 0.5)
                while want and time.monotonic() < end:
                    try:
                        reply = s.recv(65535).decode("utf-8", "replace").strip() + " "
                    except socket.timeout:
                        break
                    for prefix in want:
                        if reply.startswith(prefix):
                            a, n = want.pop(prefix)
                            rest = reply[len(prefix):].split()
                            try:
                                data = bytes(int(x, 16) for x in rest) if rest and rest[0] != "-1" else None
                            except ValueError:
                                data = None
                            out[a] = data if data is not None and len(data) == n else None
                            break
        except OSError:
            self.close()
        for a, n in reqs:
            if out.get(a) is None:
                out[a] = self.read(a, n)
        return out


def failure_kind(reply):
    """« muet » sans réponse, « refus » pour -1 (le cœur ne donne pas sa mémoire), « bizarre » sinon."""
    if reply is None:
        return "muet"
    return "refus" if reply.split()[-1:] == ["-1"] else "bizarre"


def core_label(core):
    if not core:
        return ""
    return f"{core['name']} ({core['file']}" + (f", {core['date']})" if core.get("date") else ")")


def explain_failure(reply, version="", core=None):
    """Phrases (journal, apprentissage, test_retroarch) qui disent pourquoi la mémoire ne se lit pas."""
    kind = failure_kind(reply)
    if kind == "muet":
        lines = [tr("RetroArch ne répond pas aux lectures de la mémoire (commande READ_CORE_RAM).",
                    "RetroArch does not answer memory reads (READ_CORE_RAM command).")]
        if too_old(version):
            lines.append(tr(f"RetroArch {version} est trop ancien. Il faut la version 1.19 ou plus récente.",
                            f"RetroArch {version} is too old. Version 1.19 or newer is required."))
        else:
            lines.append(tr("Il faut la version officielle de RetroArch, 1.19 ou plus récente (voir le wiki, page Avec RetroArch).",
                            "You need the official RetroArch release, 1.19 or newer (see the wiki, RetroArch page)."))
        return lines
    if kind == "bizarre":
        return [tr(f"RetroArch donne une réponse inattendue à la lecture de la mémoire « {reply[:80]} ».",
                   f"RetroArch gives an unexpected reply to the memory read \"{reply[:80]}\".")]
    lines = [tr(f"RetroArch refuse de lire la mémoire du jeu (réponse « {reply[:60]} »).",
                f"RetroArch refuses to read the game memory (reply \"{reply[:60]}\").")]
    if too_old(version):
        lines.append(tr(f"RetroArch {version} est trop ancien. Il faut la version 1.19 ou plus récente.",
                        f"RetroArch {version} is too old. Version 1.19 or newer is required."))
        return lines
    if not core:
        lines.append(tr("Le cœur chargé ne donne pas sa mémoire à RetroArch. Pour voir lequel c'est, "
                        "appuie sur F1 puis Informations, Informations sur le cœur.",
                        "The loaded core does not share its memory with RetroArch. To see which one it is, "
                        "press F1, then Information, Core Information."))
        lines.append(tr("Pour l'arcade il faut FinalBurn Neo. FB Alpha 2012 et les cœurs MAME ne donnent pas "
                        "leur mémoire (voir le wiki, page Avec RetroArch).",
                        "For arcade games you need FinalBurn Neo. FB Alpha 2012 and the MAME cores do not share "
                        "their memory (see the wiki, RetroArch page)."))
        return lines
    lines.append(tr(f"Le cœur chargé est {core_label(core)}.", f"The loaded core is {core_label(core)}."))
    if core.get("memory") is False:
        lines.append(tr("Ce cœur ne donne jamais sa mémoire à RetroArch. ArcadeDMD ne peut rien lire avec lui.",
                        "This core never shares its memory with RetroArch. ArcadeDMD cannot read anything with it."))
        lines.append(tr("Lance ce jeu avec le cœur FinalBurn Neo (voir le wiki, page Avec RetroArch).",
                        "Run this game with the FinalBurn Neo core (see the wiki, RetroArch page)."))
    elif core.get("memory") is True:
        lines.append(tr("Ce cœur est sûrement trop ancien pour donner sa mémoire. "
                        "Mets-le à jour (voir le wiki, page Avec RetroArch).",
                        "This core is probably too old to share its memory. "
                        "Update it (see the wiki, RetroArch page)."))
    else:
        lines.append(tr("Ce cœur ne donne pas sa mémoire à RetroArch. Il faut un cœur compatible avec les succès "
                        "RetroAchievements, par exemple FinalBurn Neo pour l'arcade (voir le wiki, page Avec RetroArch).",
                        "This core does not share its memory with RetroArch. You need a core that supports "
                        "RetroAchievements, for example FinalBurn Neo for arcade games (see the wiki, RetroArch page)."))
    return lines


def find_core(content=""):
    """Cœur chargé par RetroArch (Windows), ou None. Ne lève jamais d'exception."""
    try:
        return wincore.find_core(content)
    except Exception:
        return None


class Layout:
    """Fenêtre de RAM vue par RetroArch, et sa correspondance avec les adresses du processeur."""

    def __init__(self, base=0, size=0x10000, swap=False, big_endian=None, swap32=False):
        self.base = int(base)
        self.size = int(size)
        self.swap32 = bool(swap32)
        self.swap = bool(swap) and not self.swap32
        self.align = 4 if self.swap32 else 2 if self.swap else 1
        self.big_endian = (self.swap or self.swap32) if big_endian is None else bool(big_endian)

    def _unswap(self, data):
        return swap32(data) if self.swap32 else swap16(data) if self.swap else data

    def contains(self, start, end):
        return self.base <= start and end < self.base + self.size

    def read_cpu(self, client, start, end):
        """(adresse du 1er octet, octets) pour [start..end] en adresses processeur, ou None."""
        lo, hi = start - self.base, end - self.base
        if self.align > 1:
            lo &= ~(self.align - 1)
            hi |= self.align - 1
        if lo < 0 or hi >= self.size:
            return None
        out = bytearray()
        pos = lo
        while pos <= hi:
            n = min(CHUNK - (pos % CHUNK), hi - pos + 1)     # jamais à cheval sur deux blocs
            data = client.read(pos, n)
            if data is None:
                return None
            out += data
            pos += n
        return self.base + lo, self._unswap(bytes(out))

    def read_cpu_many(self, client, spans):
        """read_cpu for several spans, the requests sent together: RetroArch answers them all at its next image, where
        one at a time takes an image each (1.32, the stick read between). [(address, bytes)] or None.
        / read_cpu pour plusieurs plages, les demandes envoyées ensemble : RetroArch y répond à la même image."""
        plan, reqs = [], []
        for start, end in spans:
            lo, hi = start - self.base, end - self.base
            if self.align > 1:
                lo &= ~(self.align - 1)
                hi |= self.align - 1
            if lo < 0 or hi >= self.size:
                return None
            parts, pos = [], lo
            while pos <= hi:
                n = min(CHUNK - (pos % CHUNK), hi - pos + 1)
                parts.append((pos, n))
                pos += n
            plan.append((lo, parts))
            reqs += parts
        got = client.read_batch(reqs) if hasattr(client, "read_batch") else client.read_many(reqs)
        out = []
        for lo, parts in plan:
            data = bytearray()
            for pos, n in parts:
                d = got.get(pos)
                if d is None:
                    return None
                data += d
            out.append((self.base + lo, self._unswap(bytes(data))))
        return out

    def readable_size(self, client):
        """Taille réellement lisible (sondage octet par octet, sans jamais lire hors de la RAM)."""
        if client.read(self.size - 1, 1) is not None:
            return self.size
        if client.read(0, 1) is None:
            return 0
        lo, hi = 0, self.size - 1          # lo lisible, hi illisible
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if client.read(mid, 1) is not None:
                lo = mid
            else:
                hi = mid
        return (lo + 1) & ~(self.align - 1)

    def capture(self, client):
        """Toute la RAM lisible, dans l'ordre du processeur, ou None. Une grande RAM (le CV1000 de Cave) se lit par
        fenêtres de demandes (read_many), une petite une demande à la fois, comme toujours."""
        size = self.readable_size(client)
        if size <= 0:
            return None
        out = bytearray()
        if size > 0x20000 and hasattr(client, "read_many"):
            reqs = [(off, min(CHUNK, size - off)) for off in range(0, size, CHUNK)]
            got = client.read_many(reqs)
            for off, n in reqs:
                if got.get(off) is None:
                    return None
                out += got[off]
            return self._unswap(bytes(out))
        for off in range(0, size, CHUNK):
            data = client.read(off, min(CHUNK, size - off))
            if data is None:
                return None
            out += data
        return self._unswap(bytes(out))


def ra_rules(game):
    r = (game or {}).get("retroarch")
    return r if isinstance(r, dict) else None


_SETS = None


def neogeo_sets():
    """Every Neo Geo set of FinalBurn Neo with its parent (a version, a bootleg, a hack), or the scene of its genre for a
    game without a parent ("@neogeo_shoot"), and its title when it differs from the parent's. dmd/neogeo_sets.json,
    made by tools/neogeo_sets.py. / Chaque set Neo Geo de FinalBurn Neo, son parent ou la scène de son genre."""
    global _SETS
    if _SETS is None:
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "neogeo_sets.json"), encoding="utf-8") as f:
                sets = json.load(f).get("sets")
            _SETS = sets if isinstance(sets, dict) else {}
        except (OSError, ValueError):
            _SETS = {}
    return _SETS


def _system_ok(game, system):
    systems = [x.lower() for x in (ra_rules(game) or {}).get("systems", [])]
    return not systems or any(x in (system or "").lower() for x in systems)


def _direct(games, c, system):
    for fallback in (False, True):          # les modèles (neogeo.json) passent après les fichiers propres à un jeu
        for key, g in games.items():
            if key.startswith("_") or bool(g.get("fallback")) != fallback:
                continue
            r = ra_rules(g)
            if not r:
                continue
            if any(x.lower() in c for x in r.get("content_not", [])):
                continue
            if not _system_ok(g, system):
                continue
            if c in [x.lower() for x in r.get("content", [])] or any(x.lower() in c for x in r.get("content_contains", [])):
                return key, g
    return None, None


def resolve(games, content, system=""):
    """(key, game, parent, title) of the content started in RetroArch. RetroArch does not give the parent of a set, so a
    version, a bootleg or a hack of a Neo Geo game that is not listed takes the file of its original game (parent), as
    with MAME, and a Neo Geo game without a parent nor a file of its own (a homebrew) the scene of its genre. title is
    the name of that set when it differs from its parent's, otherwise "".
    / Le fichier du contenu lancé. Une version, un bootleg ou un hack d'un jeu Neo Geo prend le fichier du jeu d'origine,
    comme avec MAME, et un jeu Neo Geo sans parent ni fichier à lui la scène de son genre."""
    c = (content or "").lower()
    if not c:
        return None, None, "", ""
    key, g = _direct(games, c, system)
    if key is not None:
        return key, g, "", ""
    sets = neogeo_sets()
    name, title, seen = c, "", set()
    while name in sets and name not in seen:
        seen.add(name)
        entry = sets[name]
        if not isinstance(entry, list) or not entry or not isinstance(entry[0], str):
            break
        title = title or (entry[1] if len(entry) > 1 and isinstance(entry[1], str) else "")
        to = entry[0].lower()
        if to.startswith("@"):                  # a game of its own: the scene of its genre / la scène de son genre
            g = games.get(to[1:])
            if g is not None and _system_ok(g, system):
                return to[1:], g, "", title
            break
        key, g = _direct(games, to, system)
        if key is not None:
            return key, g, to, title
        name = to
    return None, None, "", ""


def match_game(games, content, system=""):
    """(clé, jeu) du fichier games/*.json qui correspond au contenu lancé dans RetroArch."""
    key, game, _, _ = resolve(games, content, system)
    return key, game


def game_title(game, content):
    g = game or {}
    titles = g.get("titles") if isinstance(g.get("titles"), dict) else {}
    return titles.get(content) or g.get("title") or content


def layout_for(game, system=""):
    r = ra_rules(game) or {}
    if any(k in r for k in ("ram_base", "ram_size", "swap16", "swap32")):
        return Layout(parse_addr(r.get("ram_base")) or 0, parse_addr(r.get("ram_size")) or 0x10000,
                      bool(r.get("swap16")), r.get("big_endian"), bool(r.get("swap32")))
    s = (system or "").lower()
    for sub, base, size, sw in SYSTEM_DEFAULTS:
        if sub in s:
            return Layout(base, size, sw)
    return Layout(0, 0x10000, False)


def make_clusters(defs, gap=64, maxspan=512):
    spans = sorted(sp for sp in (value_span(d) for d in defs.values()) if sp is not None)
    out = []
    for s, e in spans:
        # close to the previous span and not too long together, or overlapping it (the lists of a whole table, read once
        # whatever their offsets, 1.33) / proche de la précédente et pas trop long, ou la chevauchant
        if out and s <= out[-1][1] + gap and (s <= out[-1][1] or max(e, out[-1][1]) - out[-1][0] < maxspan):
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]


def read_values(client, layout, defs, clusters=None, batch=False):
    """{nom: valeur} lues dans RetroArch, ou None si la lecture échoue. batch: the requests sent together, answered at
    the same image (1.32) / les demandes envoyées ensemble, servies à la même image."""
    spans = clusters if clusters is not None else make_clusters(defs) if defs else []
    if batch and len(spans) > 1 and (hasattr(client, "read_batch") or hasattr(client, "read_many")):
        bufs = layout.read_cpu_many(client, spans)
        if bufs is None:
            return None
    else:
        bufs = []
        for start, end in spans:
            r = layout.read_cpu(client, start, end)
            if r is None:
                return None
            bufs.append(r)

    def getb(a):
        for base, data in bufs:
            if base <= a < base + len(data):
                return data[a - base]
        return None

    vals = {}
    for name, d in defs.items():
        if d.get("ptr") is not None:          # objet qui bouge : on lit là où pointe le pointeur
            a = target(d, getb, layout.big_endian)
            n = value_size(d)
            if a is None:
                continue
            if any(getb(a + i) is None for i in range(n)):
                if not layout.contains(a, a + n - 1):
                    continue
                r = layout.read_cpu(client, a, a + n - 1)
                if r is None:
                    continue
                bufs.append(r)
        v = decode(d, getb, layout.big_endian)
        if v is not None:
            vals[name] = v
    return vals


# between two reads of the stick: RetroArch answers at its next image, the read itself keeps the pace of the game
# entre deux lectures du stick : RetroArch répond à l'image suivante, la lecture suit d'elle-même le rythme du jeu
FAST_POLL = 0.001
DUMP_EVERY = 0.25             # seconds between two snapshots of the whole memory ("ram_dump") / entre deux instantanés
SHOT_EVERY = 2.0              # seconds between two screenshots asked of RetroArch while a game is played / entre deux
SHOT_ON = ("lives", "lives_p2", "mission", "vehicle", "boss_flag", "stage_state")   # and when one of these changes
SHOT_GAP = 0.5                # not two screenshots closer than this / pas deux captures plus proches


def _secs(v, default, least):
    """A duration setting, or its default. / Une durée du réglage, ou sa valeur par défaut."""
    if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
        return max(least, float(v))
    return default


class RetroArchSource:
    """Surveille RetroArch et envoie au moteur les mêmes événements que le plugin MAME."""

    def __init__(self, library, q, cfg, log):
        self.library = library
        self.q = q
        self.log = log
        self.cfg = cfg
        self.client = RetroArchClient(cfg.get("host", "127.0.0.1"), cfg.get("port", DEFAULT_PORT))
        self.poll = max(0.05, float(cfg.get("poll_ms", 100)) / 1000.0)
        # the whole memory recorded for every game, and screenshots asked of RetroArch (1.33 test 35, one game
        # should be enough to find every address of a game) / toute la mémoire et des captures d'écran pour tous les jeux
        dump = cfg.get("ram_dump") if isinstance(cfg.get("ram_dump"), dict) else {}
        self.dump_all = bool(dump.get("enabled", False))
        self.dump_every = _secs(dump.get("every"), DUMP_EVERY, 0.05)
        shots = cfg.get("screenshots") if isinstance(cfg.get("screenshots"), dict) else {}
        self.shots_on = bool(shots.get("enabled", False))
        self.shot_every = _secs(shots.get("every"), SHOT_EVERY, 0.5)
        self.shot_values = tuple(shots.get("on")) if isinstance(shots.get("on"), list) else SHOT_ON
        self.shot_dir = str(shots.get("dir") or "")
        self.stop_ev = threading.Event()
        self.session = None
        self.seen = False
        self.version = ""
        self.check_now = False        # lecture ratée : RetroArch vient peut-être de se fermer
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def close(self):
        self.stop_ev.set()
        self.thread.join(1.5)
        self._dump_close()
        self.client.close()

    def _emit(self, ev):
        self.q.put(("ev", ev))

    def _run(self):
        next_status = 0.0
        last_status = 0.0
        misses = 0
        while not self.stop_ev.is_set():
            try:
                now = time.monotonic()
                if now >= next_status or (self.check_now and now - last_status >= 0.2):
                    self.check_now = False
                    last_status = now
                    next_status = now + 1.0
                    st = self.client.status()
                    if st is None:
                        misses += 1
                        if self.session and misses >= 2:
                            self._end(tr("RetroArch ne répond plus", "RetroArch stopped responding"))
                        elif self.session:
                            next_status = now + 0.2      # sans doute fermé : confirmation tout de suite
                        if not self.session:
                            self.stop_ev.wait(2.0)
                            continue
                    else:
                        misses = 0
                        if not self.seen:
                            self.seen = True
                            v = self.client.version()
                            self.version = v or ""
                            self.log(tr(f"RetroArch {v or ''} détecté (commandes réseau actives)",
                                        f"RetroArch {v or ''} detected (network commands active)").replace("  ", " "))
                            if too_old(v):
                                self.log(tr("RetroArch est trop ancien pour lire la mémoire des jeux, "
                                            "il faut la version 1.19 ou plus récente.",
                                            "RetroArch is too old to read game memory, version 1.19 or newer is required."))
                        if st["state"] not in ("PLAYING", "PAUSED"):
                            if self.session:
                                self._end(tr("jeu fermé", "game closed"))
                            self.stop_ev.wait(1.0)
                            continue
                        ident = (st["system"], st["content"])
                        if self.session is None or self.session["ident"] != ident:
                            if self.session:
                                self._end(tr("changement de jeu", "game changed"))
                            self._begin(st)
                        elif self._game_file_changed():
                            self._begin(st)              # adresses apprises : on les lit tout de suite
                        paused = st["state"] == "PAUSED"
                        if paused != self.session["paused"]:
                            self.session["paused"] = paused
                            self._emit({"t": "pause" if paused else "resume"})
                if self.session:
                    self._poll_values()
                    s = self.session
                    if s and s.get("fast") and not s.get("paused") and not s.get("fails"):
                        if self._poll_fast(time.monotonic() + self.poll):
                            continue                      # the stick read until now / le stick lu jusqu'ici
            except Exception as e:          # le moteur doit continuer quoi qu'il arrive
                self.log(tr(f"RetroArch : erreur {e!r}", f"RetroArch: error {e!r}"))
                self.session = None
                self.stop_ev.wait(2.0)
            self.stop_ev.wait(self.poll)

    def _poll_fast(self, until):
        """The stick and buttons until the next read of everything, once an image (RetroArch answers once an image),
        each change sent with the time it was read. / Le stick et les boutons jusqu'à la prochaine lecture de tout,
        une fois par image, chaque changement envoyé avec le moment de sa lecture."""
        s = self.session
        done = False
        while not self.stop_ev.is_set() and time.monotonic() < until:
            # all the fast places at the same image (1.33 test 30: Windjammers read its players, its disc and the BIOS
            # countdown one image each, the countdown sampled every 4 images and two quick coins could show as one)
            # / toutes les places rapides à la même image
            vals = read_values(self.client, s["layout"], s["fast"], s["fast_clusters"], batch=True)
            if vals is None:
                self.check_now = True             # RetroArch closed, maybe / RetroArch fermé, peut-être
                break
            done = True
            changed = {k: v for k, v in vals.items() if s["last"].get(k) != v}
            if changed:
                s["last"].update(changed)
                self._emit({"t": "v", "v": changed, "at": time.monotonic()})
            self.stop_ev.wait(FAST_POLL)
        return done

    def _begin(self, st):
        key, game, parent, own = resolve(self.library.games, st["content"], st["system"])
        layout = layout_for(game, st["system"])
        values = game_values(game, st["content"], parent)
        defs = {}
        for name, d in values.items():
            if not isinstance(d, dict):
                continue
            span = value_span(d)
            if span is None:
                continue
            if layout.contains(*span):
                defs[name] = d
            elif not d.get("mame_only"):
                self.log(tr(f"RetroArch : {name} ({d.get('addr')}) hors de la mémoire visible par RetroArch, ignoré",
                            f"RetroArch: {name} ({d.get('addr')}) is outside the memory visible to RetroArch, ignored"))
        mame = [n for n, d in values.items() if isinstance(d, dict) and d.get("mame_only") and value_span(d) is not None]
        if mame and not defs:
            # 1944, Dimahoo: everything outside the 64 KB that FinalBurn Neo shares / tout hors des 64 Ko partagés
            self.log(tr(f"RetroArch : {key or st['content']} garde ses valeurs hors de la mémoire que RetroArch partage "
                        f"({', '.join(sorted(mame))}), rien n'est lu. Lance ce jeu avec MAME pour tout voir.",
                        f"RetroArch: {key or st['content']} keeps its values outside the memory RetroArch shares "
                        f"({', '.join(sorted(mame))}), nothing is read. Launch this game with MAME to see everything."))
        core = find_core(st["content"])
        # the stick and buttons ("fast"): read at every image between the other reads, a quarter circle lasts a few
        # images only (1.32) / le stick et les boutons, lus à chaque image entre les autres lectures
        fast = {n: d for n, d in defs.items() if d.get("fast")}
        self.session = {"ident": (st["system"], st["content"]), "key": key or "", "layout": layout,
                        "defs": defs, "clusters": make_clusters(defs) if defs else [], "last": {},
                        "fast": fast, "fast_clusters": make_clusters(fast) if fast else [],
                        "last_hb": 0.0, "paused": False, "fails": 0, "warned": False, "retry_at": 0.0,
                        "core": core, "mt": getattr(self.library, "mtimes", {}).get(key) if key else None,
                        "dump": None, "dump_at": 0.0, "dump_prev": None,
                        "shot_at": -9.0, "shots": 0, "shot_seen": None, "shot_check": 0.0}
        if self.dump_all or (isinstance(game, dict) and game.get("ram_dump")):
            self._dump_open(st["content"], key, layout)
        title = own or game_title(game, parent or st["content"])
        ev = {"t": "start", "game": key or "", "system": st["content"], "description": title,
              "media": [], "values": sorted(defs), "source": "retroarch", "core": st["system"]}
        if "bios_request" in defs and "credits" not in defs:          # an MVS: its credits guessed from its BIOS
            # the compulsion countdown of the BIOS, image by image: each coin the BIOS takes on the title screen starts it
            # again (1.33 test 28) / le compte à rebours du BIOS image par image, chaque pièce prise le relance
            if "bios_timer" in defs and "bios_frames" not in defs and layout.contains(0x10FDDB, 0x10FDDB):
                # both at the same image, or a second that ends looks like a coin / les deux à la même image
                defs["bios_timer"] = dict(defs["bios_timer"], fast=True)
                defs["bios_frames"] = {"addr": "0x10FDDB", "type": "u8", "fast": True}
                self.session["defs"] = defs
                self.session["clusters"] = make_clusters(defs)
                fast = {n: d for n, d in defs.items() if d.get("fast")}
                self.session["fast"] = fast
                self.session["fast_clusters"] = make_clusters(fast)
                ev["values"] = sorted(defs)
        if parent:
            ev["parent"] = parent
        if own:
            ev["own_title"] = own
        self._emit(ev)
        where = st["system"] + (tr(f", cœur {core['file']}", f", core {core['file']}") if core else "")
        how = (tr(f" (version de {parent})", f" (version of {parent})") if parent
               else tr(" (scène de son genre)", " (scene of its genre)") if own else "")
        self.log(tr(f"RetroArch : {st['content']} ({where}) -> ", f"RetroArch: {st['content']} ({where}) -> ")
                 + (tr(f"games/{key}.json{how}, {len(defs)} valeur(s)", f"games/{key}.json{how}, {len(defs)} value(s)") if key
                    else tr("pas de fichier dans games", "no file in games")))

    def _game_file_changed(self):
        """Fichier du jeu modifié, ou nouveau fichier propre au jeu (appris pendant la partie)."""
        s = self.session
        key, _ = match_game(self.library.games, s["ident"][1], s["ident"][0])
        if (key or "") != s["key"]:
            return True
        return bool(key) and getattr(self.library, "mtimes", {}).get(key) != s["mt"]

    def _end(self, why):
        self._dump_close()
        s = self.session
        if s and s.get("shots"):
            self.log(tr(f"capture d'écran : {s['shots']} demandée(s) à RetroArch pendant la partie",
                        f"screenshot: {s['shots']} asked of RetroArch during the game"))
        self.session = None
        self._emit({"t": "stop"})
        self.log(tr(f"RetroArch : fin de partie ({why})", f"RetroArch: game ended ({why})"))

    # ------------------------------------------------------------------ the whole memory, once a second / toute la mémoire
    def _dump_open(self, rom, key, layout):
        """"ram_dump": true in a game file: the whole memory RetroArch shares, written once a second to
        runtime/captures/<rom>-<date>.ram, to find where the game keeps what is not read yet (the bosses of the Metal Slug
        games, 1.33 test 30). Each record: the seconds since the start (8 bytes, little endian double), the size of the
        zlib block (4 bytes) and the block, the memory in the order of the processor. tools/ram_diff.py reads it.
        / Toute la mémoire une fois par seconde, pour trouver ce que le jeu range où (les boss des Metal Slug)."""
        folder = os.path.join(getattr(self.library, "root", "."), "runtime", "captures")
        try:
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, f"{key or rom}-{time.strftime('%Y%m%d-%H%M%S')}.ram")
            f = open(path, "wb")
        except OSError as e:
            self.log(tr(f"mémoire : impossible d'écrire dans {folder} ({e})", f"memory: cannot write in {folder} ({e})"))
            return
        # each record holds the bytes that differ from the record before (XOR), zlib'd: a few KB four times a second
        # instead of 64 KB once ("delta" in the header, 1.33 test 35) / chaque enregistrement, la différence avec le
        # précédent, compressée
        head = {"version": "1.33.0", "game": key, "rom": rom, "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "base": layout.base, "size": layout.size, "every": self.dump_every, "delta": True}
        f.write((json.dumps(head) + "\n").encode("utf-8"))
        self.session["dump"] = {"f": f, "path": path, "t0": time.monotonic(), "n": 0}
        self.session["dump_prev"] = None
        self.log(tr(f"mémoire : toute la mémoire de {rom} enregistrée {self.dump_every:g} s par {self.dump_every:g} s dans {path} "
                    f"(pour retrouver ce que le jeu range où)",
                    f"memory: the whole memory of {rom} written every {self.dump_every:g} s to {path} (to find where the game keeps what)"))

    def _dump_tick(self, s, now):
        d = s.get("dump")
        if not d or now - s["dump_at"] < self.dump_every:
            return
        s["dump_at"] = now
        lay = s["layout"]
        half = lay.size // 2
        raw = bytearray()
        for start, end in ((lay.base, lay.base + half - 1), (lay.base + half, lay.base + lay.size - 1)):
            got = lay.read_cpu_many(self.client, [(start, end)])     # 64 requests of 512 bytes, one image / une image
            if not got:
                return
            raw += got[0][1]
        raw = bytes(raw)
        prev = s.get("dump_prev")
        if prev is None or len(prev) != len(raw):
            diff = raw
        else:                                                          # XOR of the two, in one go / en une fois
            diff = (int.from_bytes(raw, "big") ^ int.from_bytes(prev, "big")).to_bytes(len(raw), "big")
        s["dump_prev"] = raw
        try:
            z = zlib.compress(diff, 6)
            d["f"].write(struct.pack("<dI", now - d["t0"], len(z)) + z)
            d["n"] += 1
            if d["n"] % 10 == 0:
                d["f"].flush()
        except OSError:
            self._dump_close()

    # ------------------------------------------------------------------ screenshots asked of RetroArch / les captures d'écran
    def shot(self, why, now=None):
        """Asks RetroArch for a screenshot (its SCREENSHOT command on the same port as the memory reads): the picture lands
        in its screenshots folder with the date and time in its name, to see what happened on the screen when a byte
        moved (1.33 test 35). / Demande une capture d'écran à RetroArch : l'image tombe dans son dossier avec l'heure."""
        s = self.session
        if not s or not self.shots_on:
            return False
        now = time.monotonic() if now is None else now
        if now - s["shot_at"] < SHOT_GAP:
            return False
        s["shot_at"] = now
        if not self.client.send("SCREENSHOT"):
            return False
        s["shots"] += 1
        if s["shots"] == 1:
            self.log(tr(f"capture d'écran : première demandée à RetroArch ({why})", f"screenshot: the first asked of RetroArch ({why})"))
            if self.shot_dir:
                s["shot_seen"] = self._shot_files()
                s["shot_check"] = now + 3.0
        return True

    def _shot_files(self):
        try:
            return {n for n in os.listdir(self.shot_dir) if n.lower().endswith(".png")}
        except OSError:
            return None

    def _shot_tick(self, s, vals, changed, now):
        """A screenshot every shot_every seconds while somebody plays, and at once when one of the values that mark a
        moment changes (a life lost, a mission, a vehicle, the game's flags). / Une toutes les shot_every secondes
        pendant qu'on joue, et à chaque changement d'une des valeurs qui marquent un moment."""
        if not self.shots_on:
            return
        if s["shot_check"] and now >= s["shot_check"]:                # the first one: did a file appear? / un fichier ?
            s["shot_check"] = 0.0
            seen = s.get("shot_seen")
            files = self._shot_files()
            if files is None:
                self.log(tr(f"capture d'écran : le dossier {self.shot_dir} ne se lit pas", f"screenshot: the folder {self.shot_dir} cannot be read"))
            elif seen is not None and files - seen:
                self.log(tr(f"capture d'écran : vue dans {self.shot_dir} ({sorted(files - seen)[0]})",
                            f"screenshot: seen in {self.shot_dir} ({sorted(files - seen)[0]})"))
            else:
                self.log(tr(f"capture d'écran : aucun fichier nouveau dans {self.shot_dir} 3 s après la demande "
                            "(le réglage screenshot_directory de RetroArch, ou ses commandes réseau)",
                            f"screenshot: no new file in {self.shot_dir} 3 s after the request (RetroArch's screenshot_directory, or its network commands)"))
        playing = True
        modes = [vals.get(k) for k in ("p1_mode", "p2_mode") if k in vals]
        if modes:
            playing = any(m in (1, 2) for m in modes)                  # a Neo Geo: somebody plays / quelqu'un joue
        if any(k in changed for k in self.shot_values):
            self.shot(", ".join(k for k in self.shot_values if k in changed), now)
        elif playing and now - s["shot_at"] >= self.shot_every:
            self.shot("période", now)

    def _dump_close(self):
        d = (self.session or {}).get("dump") if self.session else None
        if not d:
            return
        self.session["dump"] = None
        try:
            d["f"].close()
        except OSError:
            pass
        self.log(tr(f"mémoire : {d['n']} instantané(s) écrit(s) dans {d['path']}", f"memory: {d['n']} snapshot(s) written to {d['path']}"))

    def _poll_values(self):
        s = self.session
        now = time.monotonic()
        if s["clusters"] and now >= s["retry_at"]:
            # with the stick to read (1.32), everything at the same image, then the stick at every image until the next
            # read / avec le stick à lire, tout à la même image, puis le stick à chaque image jusqu'à la lecture suivante
            # everything at the same image (1.33 test 25: Metal Slug 4 read 13 places one image each, 0.32 s a round; the
            # fighting games have read this way since 1.32) / tout à la même image
            vals = read_values(self.client, s["layout"], s["defs"], s["clusters"], batch=True)
            if vals is None:
                s["fails"] += 1
                self.check_now = True
                if s["warned"]:
                    s["retry_at"] = now + 3.0        # déjà expliqué : on réessaie sans insister
                elif s["fails"] >= 10:
                    s["warned"] = True
                    s["retry_at"] = now + 3.0
                    reply = self.client.last_reply
                    core = s["core"] or find_core(s["ident"][1])
                    for line in explain_failure(reply, self.version, core):
                        self.log(line)
            else:
                if s["warned"]:
                    self.log(tr("RetroArch : la lecture de la mémoire marche à nouveau.",
                                "RetroArch: memory reads work again."))
                s["fails"] = 0
                s["warned"] = False
                s["retry_at"] = 0.0
                changed = {k: v for k, v in vals.items() if s["last"].get(k) != v}
                if changed:
                    s["last"].update(changed)
                    self._emit({"t": "v", "v": changed, "at": time.monotonic()})
                self._dump_tick(s, now)
                self._shot_tick(s, vals, changed, now)
        if now - s["last_hb"] >= 2.0:
            s["last_hb"] = now
            self._emit({"t": "hb", "v": dict(s["last"])})
