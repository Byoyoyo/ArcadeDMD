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
    if any(k in r for k in ("ram_base", "ram_size", "swap16")):
        return Layout(parse_addr(r.get("ram_base")) or 0, parse_addr(r.get("ram_size")) or 0x10000,
                      bool(r.get("swap16")), r.get("big_endian"))
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


def read_values(client, layout, defs, clusters=None):
    """{nom: valeur} lues dans RetroArch, ou None si la lecture échoue."""
    bufs = []
    for start, end in (clusters if clusters is not None else make_clusters(defs) if defs else []):
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
            except Exception as e:          # le moteur doit continuer quoi qu'il arrive
                self.log(tr(f"RetroArch : erreur {e!r}", f"RetroArch: error {e!r}"))
                self.session = None
                self.stop_ev.wait(2.0)
            self.stop_ev.wait(self.poll)

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
        core = find_core(st["content"])
        self.session = {"ident": (st["system"], st["content"]), "key": key or "", "layout": layout,
                        "defs": defs, "clusters": make_clusters(defs) if defs else [], "last": {},
                        "last_hb": 0.0, "paused": False, "fails": 0, "warned": False, "retry_at": 0.0,
                        "core": core, "mt": getattr(self.library, "mtimes", {}).get(key) if key else None}
        title = own or game_title(game, parent or st["content"])
        ev = {"t": "start", "game": key or "", "system": st["content"], "description": title,
              "media": [], "values": sorted(defs), "source": "retroarch", "core": st["system"]}
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
            vals = read_values(self.client, s["layout"], s["defs"], s["clusters"])
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
                    self._emit({"t": "v", "v": changed})
        if now - s["last_hb"] >= 2.0:
            s["last_hb"] = now
            self._emit({"t": "hb", "v": dict(s["last"])})
