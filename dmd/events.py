"""The event bus: what the game does, said once, for every screen (docs/EVENT_BUS.md).

The scenes that follow a game decide when something happens (a grenade thrown, a life lost, a boss coming). Until now
each of them drew its own answer and nothing else could know. They now also say it here, with a stable name and plain
figures, and any renderer may listen: the HD marquee, the LED panel, the lights of the cabinet, a new graphical engine.
Nothing is decided in this module and no rule of detection lives in it.

Three kinds of message, all plain dicts (the same go to a journal, one JSON object per line):

    {"type": "hello", "protocol": 1, "arcadedmd": "1.40.0", "session": "9f2c41d07a3e", "t": 12.5, "wall": 1795300000.0,
     "game": {"key": "mslug2", "title": "Metal Slug 2", "system": "mslug2", "parent": "", "family": "mslug2",
              "detector": "MetalSlugScene"},
     "events": ["player.join", ...], "values": ["score", "lives", ...]}
    {"type": "state", "seq": 41, "t": 812.34, "state": {...}}
    {"type": "event", "seq": 42, "id": "9f2c41d07a3e:42", "t": 812.34, "at": 812.34, "name": "mslug.grenade.thrown",
     "side": "p1", "basis": "read", "data": {"count": 1, "bombs_before": 10, "bombs": 9, "synced": true}}
    {"type": "bye", "seq": 43, "t": 1420.0, "reason": "stop"}

"t" is when the thing was detected, in seconds on the engine's clock; "at" is when it is to be shown, the same unless
the engine itself schedules the announcement later. "seq" grows by one with each state, event and bye of a game, and
"id" (the session of the game, then seq) names one occurrence for good: the same id is the same event, never two.
"basis" says where the event comes from: "read" (a value of the game changed, and the event is that change), "deduced"
(a rule over several readings, or a threshold), "timed" (an instant set by ArcadeDMD's own clock, not by the game).

A pause of the emulator sends game.pause then game.resume; no reading comes in between, so nothing else is said, and
the instants already given are not moved. A game that stops, or another one that starts, sends a bye: everything a
listener still holds for that game is to be dropped. The next hello opens a new session, where seq starts again.

    bus = engine.events
    bus.subscribe(fn)                 # fn(message) for each message; a newcomer gets the hello and the last state
    bus.last_time("mslug.shot", "p1") # when it last happened, -99.0 if never
    bus.state                         # the last state published, or None

/ Le bus d'événements : ce que fait le jeu, dit une fois, pour tous les écrans. Les scènes décident, ce module transmet.
Aucune règle de détection ne vit ici.
"""

import importlib
import json
import os
import time
import uuid
from collections import deque

PROTOCOL = 1
NEVER = -99.0
BASES = ("read", "deduced", "timed")

DETECTORS = []         # (matches(key) -> family or "", name of the scene, names of its events)
LED_PAINTERS = []      # (matches(key) -> truthy, factory(engine) -> painter(canvas, engine, now) -> True when it drew)


def detector(matches, name, events):
    """A scene says which games it follows and what it may announce (called once, as its module is loaded).
    / Une scène dit quels jeux elle suit et ce qu'elle peut annoncer."""
    for d in DETECTORS:
        if d[1] == name:
            DETECTORS.remove(d)
            break
    DETECTORS.append((matches, name, tuple(events)))


def detector_for(key):
    """(family, scene name, event names) of the detector that follows this game, or ("", None, ()).
    / Le détecteur qui suit ce jeu."""
    for matches, name, events in DETECTORS:
        try:
            fam = matches(key)
        except Exception:
            fam = ""
        if fam:
            return (fam if isinstance(fam, str) else key), name, events
    return "", None, ()


def led_painter(matches, factory):
    """A renderer offers to draw the LED panel of some games, in place of the scene of their game file. matches(key)
    says which; factory(engine) is called when such a game starts and returns painter(canvas, engine, now), which
    draws on the 128x32 canvas and returns True, or returns False to leave that image to the usual scene.
    / Un moteur de rendu propose de dessiner la dalle LED de certains jeux."""
    LED_PAINTERS.append((matches, factory))


def pick_led_painter(engine, key, log=None):
    for matches, factory in LED_PAINTERS:
        try:
            if matches(key):
                return factory(engine)
        except Exception as e:                       # a renderer that fails never stops the engine / jamais bloquant
            if log:
                log(f"LED painter: {e}")
    return None


def load_modules(names, log=None):
    """The renderers named in config.json ("visual": {"modules": [...]}) are imported, which lets them register.
    / Les moteurs de rendu nommés dans config.json sont importés, ce qui leur permet de s'inscrire."""
    for name in names or []:
        try:
            importlib.import_module(str(name))
        except Exception as e:
            if log:
                log(f"visual module {name}: {e}")


def _plain(v):
    """A value a journal can hold: numbers, strings, booleans, lists and dicts of them. / Une valeur écrivable."""
    if isinstance(v, bool) or v is None or isinstance(v, (int, str)):
        return v
    if isinstance(v, float):
        return round(v, 3)
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _plain(x) for k, x in v.items()}
    return str(v)


class EventBus:
    def __init__(self, log=None, keep=512):
        self.log = log
        self.subs = []
        self.seq = 0
        self.recent = deque(maxlen=keep)       # the last events, for a listener that comes late / les derniers
        self.last = {}                         # (name, side or "") -> t of the latest / l'instant du dernier
        self.hello_msg = None
        self.state = None
        self.state_msg = None
        self.journal = None
        self.game = ""
        self.session = ""

    # -- listeners / les abonnés
    def subscribe(self, fn, replay=True):
        """fn(message) for every message from now on. With replay, the game in progress is told first: its hello and
        its last state. / fn(message) pour chaque message ; avec replay, le jeu en cours est d'abord annoncé."""
        if fn not in self.subs:
            self.subs.append(fn)
        if replay:
            for msg in (self.hello_msg, self.state_msg):
                if msg is not None:
                    self._call(fn, msg)
        return fn

    def unsubscribe(self, fn):
        if fn in self.subs:
            self.subs.remove(fn)

    def _call(self, fn, msg):
        try:
            fn(msg)
        except Exception as e:                 # a listener that fails is dropped, the engine goes on / on continue
            self.unsubscribe(fn)
            if self.log:
                self.log(f"event listener dropped: {e}")

    def _send(self, msg):
        if self.journal is not None:
            try:
                self.journal.write(json.dumps(msg, ensure_ascii=False, separators=(",", ":")) + "\n")
            except (OSError, ValueError):
                self.close_journal()
        for fn in list(self.subs):
            self._call(fn, msg)

    # -- a game / un jeu
    def hello(self, t, game, values=(), version=""):
        """A game starts. Everything of the game before is forgotten. / Un jeu commence."""
        key = game.get("key") or ""
        fam, name, events = detector_for(key)
        self.seq = 0
        self.recent.clear()
        self.last = {}
        self.state = self.state_msg = None
        self.game = key
        self.session = uuid.uuid4().hex[:12]
        self.hello_msg = {"type": "hello", "protocol": PROTOCOL, "arcadedmd": version, "session": self.session,
                          "t": round(t, 3),
                          "wall": round(time.time(), 3),
                          "game": dict(_plain(game), family=fam, detector=name),
                          "events": list(events), "values": sorted(str(v) for v in values if not str(v).startswith("_"))}
        self._send(self.hello_msg)
        return self.hello_msg

    def bye(self, t, reason="stop"):
        if self.hello_msg is None:
            return None
        self.seq += 1
        msg = {"type": "bye", "seq": self.seq, "t": round(t, 3), "reason": reason}
        self._send(msg)
        self.hello_msg = self.state_msg = self.state = None
        self.game = ""
        self.close_journal()
        return msg

    # -- what happens / ce qui se passe
    def emit(self, name, t, side=None, at=None, read_at=None, data=None, basis=None):
        """An event: its name, when it was detected, whose it is, when to show it, its figures (a dict), and where it
        comes from ("read" unless told "deduced" or "timed").
        Nothing is said while no game runs. / Un événement... Rien n'est dit hors d'un jeu."""
        if self.hello_msg is None:
            return None
        self.seq += 1
        msg = {"type": "event", "seq": self.seq, "id": f"{self.session}:{self.seq}", "t": round(t, 3),
               "at": round(t if at is None else at, 3), "name": name}
        if side:
            msg["side"] = side
        if read_at is not None:
            msg["read_at"] = round(read_at, 3)
        msg["basis"] = basis if basis in BASES else "read"
        msg["data"] = _plain(data or {})
        self.last[(name, side or "")] = t
        self.recent.append(msg)
        self._send(msg)
        return msg

    def last_time(self, name, side=None):
        """When that event last happened in this game, NEVER (-99.0) if it has not. / Son dernier instant."""
        return self.last.get((name, side or ""), NEVER)

    def publish(self, state, t):
        """The state after a reading. Sent only when it differs from the last one. / L'état après une lecture."""
        state = _plain(state)
        if state == self.state:
            return None
        self.state = state
        self.seq += 1
        self.state_msg = {"type": "state", "seq": self.seq, "t": round(t, 3), "state": state}
        self._send(self.state_msg)
        return self.state_msg

    # -- the journal / le journal
    def open_journal(self, path):
        self.close_journal()
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.journal = open(path, "w", encoding="utf-8", newline="\n")
        except OSError as e:
            self.journal = None
            if self.log:
                self.log(f"event journal: {e}")

    def close_journal(self):
        if self.journal is not None:
            try:
                self.journal.close()
            except OSError:
                pass
            self.journal = None
