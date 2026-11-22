"""A renderer in a few lines, to show how one listens to the event bus (docs/EVENT_BUS.md). It knows nothing of
ArcadeDMD but the messages: no pygame, no scene, no memory address. It says in words what it would draw.

In ArcadeDMD itself a renderer subscribes once and is called for every message:

    renderer = TextRenderer()
    engine.events.subscribe(renderer)        # the hello of the game in progress and its last state come first

Here it is fed a recorded game, replayed without a screen:

    python tools/events_example.py                       the shortest Metal Slug 2 game of tests/captures
    python tools/events_example.py CAPTURE.log [LINES]   another one, and how many lines to print (60)

/ Un moteur de rendu en quelques lignes, pour montrer comment on écoute le bus d'événements. Il ne connaît d'ArcadeDMD
que les messages : ni pygame, ni scène, ni adresse mémoire. Il dit en mots ce qu'il dessinerait.
"""

import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TextRenderer:
    """Everything a renderer has to do with the bus: one method that takes a message.
    / Tout ce qu'un moteur de rendu a à faire avec le bus : une méthode qui reçoit un message."""

    def __init__(self, say=print):
        self.say = say
        self.state = None
        self.flying = {}                 # grenade id -> when it left / l'instant de son départ
        self.seen = set()                # ids of the events already drawn / événements déjà dessinés

    def __call__(self, msg):
        kind = msg["type"]
        if kind == "hello":              # a game starts: nothing of the game before is kept / on repart de zéro
            self.state, self.flying, self.seen = None, {}, set()
            game = msg["game"]
            self.say(f"--- {game['title']} ({game['key']}), {len(msg['events'])} kinds of events")
        elif kind == "bye":              # the game is over: drop whatever was still to be drawn / on lâche tout
            self.flying = {}
            self.say(f"--- end ({msg['reason']})")
        elif kind == "state":            # where the game stands, after a reading / où en est le jeu
            self.state = msg["state"]
        elif kind == "event" and msg["id"] not in self.seen:     # an id is one event, never drawn twice
            self.seen.add(msg["id"])
            handler = getattr(self, "on_" + msg["name"].replace(".", "_"), None)
            if handler:                  # a name this renderer does not know is simply left / un nom inconnu est ignoré
                handler(msg, msg["data"], msg.get("side", ""))

    def line(self, msg, text):
        later = f" (to show at {msg['at']:.2f})" if msg["at"] > msg["t"] else ""
        self.say(f"{msg['t']:8.2f} {msg.get('side', '  '):2s} {text}{later}   [{msg['basis']}]")

    # -- one method per event the renderer answers / une méthode par événement
    def on_player_join(self, m, d, side):
        self.line(m, f"the soldier comes in ({d['kind']})")

    def on_life_lost(self, m, d, side):
        self.line(m, f"hit: {d['lives']} lives left")

    def on_weapon_change(self, m, d, side):
        self.line(m, f"new weapon: {d['kind']}")

    def on_mslug_grenade_thrown(self, m, d, side):
        how = "the game counts them" if d["synced"] else "the game does not count them"
        self.line(m, f"throws {d['count']} grenade(s) {d['ids']}, {how}")

    def on_mslug_grenade_launch(self, m, d, side):
        self.flying[d["id"]] = m["t"]
        self.line(m, f"grenade {d['id']} leaves")

    def on_mslug_grenade_burst(self, m, d, side):
        t0 = self.flying.pop(d["id"], None)
        after = f" {m['t'] - t0:.2f} s after it left" if t0 is not None else ""
        self.line(m, f"grenade {d['id']} blows up{after} ({d['cause']})")

    def on_mslug_vehicle_in(self, m, d, side):
        self.line(m, f"gets into the {d['kind']}")

    def on_mslug_vehicle_out(self, m, d, side):
        self.line(m, f"the {d['kind']} is {'destroyed' if d['destroyed'] else 'left'}")

    def on_stage_clear(self, m, d, side):
        self.line(m, f"{d['kind']} {d['n']} complete")

    def on_stage_begin(self, m, d, side):
        self.line(m, f"{d['kind']} {d['n']} begins")

    def on_boss_warning(self, m, d, side):
        self.line(m, f"WARNING: {d['name'] or 'the boss'} comes, {d['hp']} of life")

    def on_boss_phase(self, m, d, side):
        self.line(m, f"the boss comes back, phase {d['phase']}")

    def on_boss_destroyed(self, m, d, side):
        self.line(m, "boss destroyed")


def main():
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import events_check                                     # only for its replay of a recorded game / pour le rejeu
    args = sys.argv[1:]
    path = args[0] if args else min(glob.glob(os.path.join(ROOT, "tests", "captures", "mslug2-*.log")), key=os.path.getsize)
    lines = int(args[1]) if len(args) > 1 else 60
    msgs, _ = events_check.replay(path, os.path.basename(path).split("-20")[0])
    shown = []
    renderer = TextRenderer(shown.append)
    for msg in msgs:                                        # what bus.subscribe(renderer) does, message by message
        renderer(msg)
    for text in shown[:lines]:
        print(text)
    if len(shown) > lines:
        print(f"... {len(shown) - lines} more lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
