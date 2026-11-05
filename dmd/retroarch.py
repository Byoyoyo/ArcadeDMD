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

import glob
import json
import os
import socket
import subprocess
import threading
import time

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
            lines.append(tr("Il faut la version officielle de RetroArch, 1.19 ou plus récente (voir README.fr.md, section RetroArch).",
                            "You need the official RetroArch release, 1.19 or newer (see README.md, RetroArch section)."))
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
                        "leur mémoire (voir README.fr.md, section RetroArch).",
                        "For arcade games you need FinalBurn Neo. FB Alpha 2012 and the MAME cores do not share "
                        "their memory (see README.md, RetroArch section)."))
        return lines
    lines.append(tr(f"Le cœur chargé est {core_label(core)}.", f"The loaded core is {core_label(core)}."))
    if core.get("memory") is False:
        lines.append(tr("Ce cœur ne donne jamais sa mémoire à RetroArch. ArcadeDMD ne peut rien lire avec lui.",
                        "This core never shares its memory with RetroArch. ArcadeDMD cannot read anything with it."))
        lines.append(tr("Lance ce jeu avec le cœur FinalBurn Neo (voir README.fr.md, section RetroArch).",
                        "Run this game with the FinalBurn Neo core (see README.md, RetroArch section)."))
    elif core.get("memory") is True:
        lines.append(tr("Ce cœur est sûrement trop ancien pour donner sa mémoire. "
                        "Mets-le à jour (voir README.fr.md, section RetroArch).",
                        "This core is probably too old to share its memory. "
                        "Update it (see README.md, RetroArch section)."))
    else:
        lines.append(tr("Ce cœur ne donne pas sa mémoire à RetroArch. Il faut un cœur compatible avec les succès "
                        "RetroAchievements, par exemple FinalBurn Neo pour l'arcade (voir README.fr.md, section RetroArch).",
                        "This core does not share its memory with RetroArch. You need a core that supports "
                        "RetroAchievements, for example FinalBurn Neo for arcade games (see README.md, RetroArch section)."))
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
        if out and s <= out[-1][1] + gap and max(e, out[-1][1]) - out[-1][0] < maxspan:
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


def retroarch_exe_dir():
    """The folder of the RetroArch program running on this machine (Windows), or None. / Le dossier de RetroArch."""
    if os.name != "nt":
        return None
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command",
                              "(Get-Process retroarch -ErrorAction SilentlyContinue | Select-Object -First 1).Path"],
                             capture_output=True, text=True, timeout=8, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        path = (out.stdout or "").strip().splitlines()
        path = path[-1].strip() if path else ""
        return os.path.dirname(path) if path and os.path.isfile(path) else None
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def fbneo_nvram_credits(client, rom, cfg_saves=None, log=None):
    """The credits an MVS game had when FinalBurn Neo last quit it, read in the backup RAM it saved
    (<saves>/fbneo/<rom>.fs, the 64 KB of $D00000 with the bytes of each word swapped: $D00034, the credits in BCD, at
    0x35). The saves folder comes from config.json ("retroarch": {"saves": ...}) or from RetroArch itself
    (GET_CONFIG_PARAM savefile_directory, a relative one resolved against the running program). None without the file.
    (1.33, Seb: the guessed credits drifted from the game's, the guess started from ArcadeDMD's own memory of them.)
    / Les crédits qu'un jeu MVS avait quand FinalBurn Neo l'a quitté, lus dans la mémoire de sauvegarde qu'il écrit."""
    if not rom:
        return None
    dirs = []
    if cfg_saves and isinstance(cfg_saves, str):
        dirs.append(cfg_saves)
    raw = client.config_param("savefile_directory") if client is not None else None
    exe = None
    if raw:
        raw = raw.strip('"')
        if raw.startswith(":"):                          # ":\saves": next to the program / à côté du programme
            exe = retroarch_exe_dir()
            if exe:
                dirs.append(os.path.join(exe, raw[1:].lstrip("\\/")))
        elif raw.lower() != "default":
            dirs.append(raw)
    if not dirs or not raw or raw.startswith(":"):
        exe = exe or retroarch_exe_dir()
        if exe:
            dirs.append(os.path.join(exe, "saves"))
    # RetroArch may sort the saves into a folder named after the core ("FinalBurn Neo") and another after the content's
    # folder: the file is looked for one and two folders down too, the newest one wins (1.33 test 22, Seb's log: never
    # found) / RetroArch peut ranger les sauvegardes dans un dossier au nom du cœur et un autre au nom du dossier du jeu
    found = []
    for d in dirs:
        d = os.path.expandvars(d)
        for pat in (("fbneo", rom + ".fs"), ("*", "fbneo", rom + ".fs"), ("*", "*", "fbneo", rom + ".fs")):
            for path in glob.glob(os.path.join(d, *pat)):
                if os.path.isfile(path):
                    try:
                        found.append((os.path.getmtime(path), path))
                    except OSError:
                        pass
    for _, path in sorted(found, reverse=True):
        try:
            with open(path, "rb") as f:
                data = f.read(0x40)
        except OSError:
            continue
        if len(data) < 0x36:
            continue
        b = data[0x35]
        hi, lo = b >> 4, b & 15
        if hi > 9 or lo > 9:
            if callable(log):
                log(f"{path}: crédits illisibles ({b:#x})")
            continue
        return {"credits": hi * 10 + lo, "path": path}
    if callable(log):
        where = ", ".join(os.path.expandvars(d) for d in dirs) or "aucun dossier"
        log(tr(f"FinalBurn Neo : pas de sauvegarde {rom}.fs trouvée (savefile_directory {raw!r}, programme {exe!r}, cherché dans {where})",
               f"FinalBurn Neo: no {rom}.fs save found (savefile_directory {raw!r}, program {exe!r}, looked in {where})"))
    return None


class RetroArchSource:
    """Surveille RetroArch et envoie au moteur les mêmes événements que le plugin MAME."""

    def __init__(self, library, q, cfg, log):
        self.library = library
        self.q = q
        self.log = log
        self.cfg = cfg
        self.client = RetroArchClient(cfg.get("host", "127.0.0.1"), cfg.get("port", DEFAULT_PORT))
        self.poll = max(0.05, float(cfg.get("poll_ms", 100)) / 1000.0)
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
            vals = read_values(self.client, s["layout"], s["fast"], s["fast_clusters"])
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
                        "core": core, "mt": getattr(self.library, "mtimes", {}).get(key) if key else None}
        title = own or game_title(game, parent or st["content"])
        ev = {"t": "start", "game": key or "", "system": st["content"], "description": title,
              "media": [], "values": sorted(defs), "source": "retroarch", "core": st["system"]}
        if "bios_request" in defs and "credits" not in defs:          # an MVS: its credits left last time, if saved
            nv = fbneo_nvram_credits(self.client, st["content"], self.cfg.get("saves"), self.log)
            if nv is not None:
                ev["nvram_credits"] = nv["credits"]
                self.log(tr(f"FinalBurn Neo : {nv['credits']} crédit(s) restant(s) la dernière fois, lus dans {nv['path']}",
                            f"FinalBurn Neo: {nv['credits']} credit(s) left last time, read in {nv['path']}"))
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
        self.session = None
        self._emit({"t": "stop"})
        self.log(tr(f"RetroArch : fin de partie ({why})", f"RetroArch: game ended ({why})"))

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
        if now - s["last_hb"] >= 2.0:
            s["last_hb"] = now
            self._emit({"t": "hb", "v": dict(s["last"])})
