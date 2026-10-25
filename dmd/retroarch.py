"""Jeux lancés dans RetroArch : lecture de la mémoire par les commandes réseau.

RetroArch (1.19 ou plus récent) répond en UDP sur le port 55355 quand le réglage
« Commandes réseau » est activé :
  GET_STATUS             -> GET_STATUS PLAYING fb_neo,mslug,crc32=1234abcd
  READ_CORE_RAM 377 2    -> READ_CORE_RAM 377 03 00   (ou « -1 » si illisible)

Les adresses de READ_CORE_RAM sont celles de RetroAchievements : 0 = début de la RAM
du jeu exposée par le cœur. ArcadeDMD les ramène aux adresses du processeur, pour que
les fichiers games/*.json servent à la fois pour MAME et pour RetroArch :
  "retroarch": {"content": ["mslug"], "ram_base": "0x100000", "ram_size": "0x10000", "swap16": true}
swap16 : le cœur range la RAM du 68000 par mots de 16 bits inversés (FBNeo, Genesis Plus GX).
"""

import socket
import threading
import time

from .memvalues import decode, parse_addr, value_size

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


class RetroArchClient:
    def __init__(self, host="127.0.0.1", port=DEFAULT_PORT, timeout=0.3):
        self.addr = (host, int(port))
        self.timeout = float(timeout)
        self.sock = None

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


class Layout:
    """Fenêtre de RAM vue par RetroArch, et sa correspondance avec les adresses du processeur."""

    def __init__(self, base=0, size=0x10000, swap=False, big_endian=None):
        self.base = int(base)
        self.size = int(size)
        self.swap = bool(swap)
        self.big_endian = self.swap if big_endian is None else bool(big_endian)

    def contains(self, start, end):
        return self.base <= start and end < self.base + self.size

    def read_cpu(self, client, start, end):
        """(adresse du 1er octet, octets) pour [start..end] en adresses processeur, ou None."""
        lo, hi = start - self.base, end - self.base
        if self.swap:
            lo &= ~1
            hi |= 1
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
        data = swap16(bytes(out)) if self.swap else bytes(out)
        return self.base + lo, data

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
        return (lo + 1) & ~1 if self.swap else lo + 1

    def capture(self, client):
        """Toute la RAM lisible, dans l'ordre du processeur, ou None."""
        size = self.readable_size(client)
        if size <= 0:
            return None
        out = bytearray()
        for off in range(0, size, CHUNK):
            data = client.read(off, min(CHUNK, size - off))
            if data is None:
                return None
            out += data
        return swap16(bytes(out)) if self.swap else bytes(out)


def ra_rules(game):
    r = (game or {}).get("retroarch")
    return r if isinstance(r, dict) else None


def match_game(games, content, system=""):
    """(clé, jeu) du fichier games/*.json qui correspond au contenu lancé dans RetroArch."""
    c = (content or "").lower()
    if not c:
        return None, None
    for key, g in games.items():
        if key.startswith("_"):
            continue
        r = ra_rules(g)
        if not r:
            continue
        if any(x.lower() in c for x in r.get("content_not", [])):
            continue
        systems = [x.lower() for x in r.get("systems", [])]
        if systems and not any(x in (system or "").lower() for x in systems):
            continue
        if c in [x.lower() for x in r.get("content", [])] or any(x.lower() in c for x in r.get("content_contains", [])):
            return key, g
    return None, None


def layout_for(game, system=""):
    r = ra_rules(game) or {}
    if any(k in r for k in ("ram_base", "ram_size", "swap16")):
        return Layout(parse_addr(r.get("ram_base")) or 0, parse_addr(r.get("ram_size")) or 0x10000,
                      bool(r.get("swap16")), r.get("big_endian"))
    s = (system or "").lower()
    for sub, base, size, sw in SYSTEM_DEFAULTS:
        if sub in s:
            return Layout(base, size, sw)
    return Layout(0, 0x10000, False)


def make_clusters(defs, gap=64, maxspan=512):
    spans = sorted((parse_addr(d["addr"]), parse_addr(d["addr"]) + value_size(d) - 1) for d in defs.values())
    out = []
    for s, e in spans:
        if out and s <= out[-1][1] + gap and max(e, out[-1][1]) - out[-1][0] < maxspan:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]


class RetroArchSource:
    """Surveille RetroArch et envoie au moteur les mêmes événements que le plugin MAME."""

    def __init__(self, library, q, cfg, log):
        self.library = library
        self.q = q
        self.log = log
        self.client = RetroArchClient(cfg.get("host", "127.0.0.1"), cfg.get("port", DEFAULT_PORT))
        self.poll = max(0.05, float(cfg.get("poll_ms", 100)) / 1000.0)
        self.stop_ev = threading.Event()
        self.session = None
        self.seen = False
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
        misses = 0
        while not self.stop_ev.is_set():
            try:
                now = time.monotonic()
                if now >= next_status:
                    next_status = now + 1.0
                    st = self.client.status()
                    if st is None:
                        misses += 1
                        if self.session and misses >= 2:
                            self._end("RetroArch ne répond plus")
                        if not self.session:
                            self.stop_ev.wait(2.0)
                            continue
                    else:
                        misses = 0
                        if not self.seen:
                            self.seen = True
                            v = self.client.version()
                            self.log(f"RetroArch {v or ''} détecté (commandes réseau actives)".replace("  ", " "))
                            if too_old(v):
                                self.log("RetroArch est trop ancien pour lire la mémoire des jeux, il faut la version 1.19 ou plus récente.")
                        if st["state"] not in ("PLAYING", "PAUSED"):
                            if self.session:
                                self._end("jeu fermé")
                            self.stop_ev.wait(1.0)
                            continue
                        ident = (st["system"], st["content"])
                        if self.session is None or self.session["ident"] != ident:
                            if self.session:
                                self._end("changement de jeu")
                            self._begin(st)
                        paused = st["state"] == "PAUSED"
                        if paused != self.session["paused"]:
                            self.session["paused"] = paused
                            self._emit({"t": "pause" if paused else "resume"})
                if self.session:
                    self._poll_values()
            except Exception as e:          # le moteur doit continuer quoi qu'il arrive
                self.log(f"RetroArch : erreur {e!r}")
                self.session = None
                self.stop_ev.wait(2.0)
            self.stop_ev.wait(self.poll)

    def _begin(self, st):
        key, game = match_game(self.library.games, st["content"], st["system"])
        layout = layout_for(game, st["system"])
        values = ((game or {}).get("memory") or {}).get("values") or {}
        defs = {}
        for name, d in values.items():
            if not isinstance(d, dict):
                continue
            a = parse_addr(d.get("addr"))
            if a is None:
                continue
            if layout.contains(a, a + value_size(d) - 1):
                defs[name] = d
            else:
                self.log(f"RetroArch : {name} ({d.get('addr')}) hors de la mémoire visible par RetroArch, ignoré")
        self.session = {"ident": (st["system"], st["content"]), "key": key or "", "layout": layout,
                        "defs": defs, "clusters": make_clusters(defs) if defs else [], "last": {},
                        "last_hb": 0.0, "paused": False, "fails": 0, "warned": False}
        title = (game or {}).get("title") or st["content"]
        self._emit({"t": "start", "game": key or "", "system": st["content"], "description": title,
                    "media": [], "values": sorted(defs), "source": "retroarch", "core": st["system"]})
        self.log(f"RetroArch : {st['content']} ({st['system']}) -> "
                 + (f"games/{key}.json, {len(defs)} valeur(s)" if key else "pas de fichier dans games"))

    def _end(self, why):
        self.session = None
        self._emit({"t": "stop"})
        self.log(f"RetroArch : fin de partie ({why})")

    def _poll_values(self):
        s = self.session
        bufs = []
        for start, end in s["clusters"]:
            r = s["layout"].read_cpu(self.client, start, end)
            if r is None:
                s["fails"] += 1
                if s["fails"] == 10 and not s["warned"]:
                    s["warned"] = True
                    self.log("RetroArch : lecture de la mémoire refusée. Il faut RetroArch 1.19 ou plus récent "
                             "(voir LISEZMOI, section RetroArch).")
                bufs = None
                break
            bufs.append(r)
        if bufs is not None:
            s["fails"] = 0

            def getb(a):
                for base, data in bufs:
                    if base <= a < base + len(data):
                        return data[a - base]
                return None

            vals = {}
            for name, d in s["defs"].items():
                v = decode(d, getb, s["layout"].big_endian)
                if v is not None:
                    vals[name] = v
            changed = {k: v for k, v in vals.items() if s["last"].get(k) != v}
            if changed:
                s["last"].update(changed)
                self._emit({"t": "v", "v": changed})
        now = time.monotonic()
        if now - s["last_hb"] >= 2.0:
            s["last_hb"] = now
            self._emit({"t": "hb", "v": dict(s["last"])})
