"""Replays the recorded games of tests/captures through the engine and its HD scene, with nothing on screen, listens to
the event bus (dmd/events.py) and compares what was said with what was said the day the references were written
(tests/events/<capture>.json: how many of each event, and a print of the whole stream). A rule of detection that moves
by a hair changes the stream, and the check says which game and which event.

It also checks what a renderer relies on: a hello first, numbers that follow one another, times that never go back, an
"at" never before its "t", only events the scene announced it may say.

    python tools/events_check.py                 the games whose scene speaks on the bus, against their references
    python tools/events_check.py --write         writes the references again (after a change that is meant)
    python tools/events_check.py --jsonl DIR     also writes each whole stream, one JSON object per line
    python tools/events_check.py FILE.log ...    only these captures

/ Rejoue les parties enregistrées de tests/captures dans le moteur et sa scène HD, sans rien afficher, écoute le bus
d'événements et compare ce qui a été dit avec les références. Une règle de détection qui bouge d'un cheveu change le
flux, et le contrôle dit dans quelle partie et pour quel événement.
"""

import collections
import glob
import hashlib
import importlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

STEP = 0.1                      # one image of the replay, in seconds; the references are written with this one
W, H = 480, 115
REFS = os.path.join(ROOT, "tests", "events")
ALWAYS = ("game.pause", "game.resume")


def replay(path, game):
    """Every message the bus sends while this capture is replayed. / Chaque message du bus pendant le rejeu."""
    from dmd import app
    from dmd.capture import read_capture
    from dmd.memvalues import derive, resolve_value
    from dmd.outputs import PreviewOutput
    log = app.Logger(None, echo=False)
    cfg = dict(app.load_config(ROOT, log), retroarch={"enabled": False}, textfiles={"enabled": False})
    cfg.pop("visual", None)
    cfg.pop("events", None)
    said = []
    out = PreviewOutput({"enabled": True, "x": 0, "y": 0, "width": W, "height": H, "mode": "always", "style": "hd",
                         "logos": False}, said.append)
    clock = [0.0]
    out.hd_view.clock = lambda: clock[0]
    msgs = []
    eng = app.Engine(ROOT, cfg, [out], log, demo_game=game)
    eng.sim = None
    eng.demo_until = None
    for d in (eng.state.values, eng.state.prev, eng.state.changed_at, eng.state.hist):
        d.clear()                                   # a real game starts with nothing read / rien de lu au départ
    eng.state.events.clear()
    eng.events.subscribe(msgs.append)               # the hello of the game comes first / le hello d'abord
    g = eng.library.get(game) or {}
    tag = g.get("tag") if isinstance(g.get("tag"), dict) else {}
    guess = None
    if "bios_request" in (g.get("memory") or {}).get("values", {}):
        from dmd.coinbuttons import mvs_rates
        from dmd.neocoins import NeoCoins
        guess = NeoCoins(mvs_rates(cfg))            # the credits, guessed as on a cabinet / les crédits devinés
    _, rows = read_capture(path)
    end = rows[-1][0] + 1.0 if rows else 0.0
    i, t = 0, 0.0
    while t < end:
        clock[0] = t
        while i < len(rows) and rows[i][0] <= t + 1e-9:
            _, name, value = rows[i]
            i += 1
            if name != "_end":
                eng.state.update(name, value, t)
        if guess is not None:
            c = guess.update(eng.state.values, t)
            guess.notes.clear()
            if c is not None and c != eng.state.values.get("credits"):
                eng.state.update("credits", c, t)
        for k, spec in tag.items():
            v = resolve_value(spec, eng.state.values)
            if v is not None and eng.state.values.get(k) != v:
                eng.state.update(k, v, t, quiet=True)
        if eng.derived:
            for k, v in derive(eng.derived, eng.state.values).items():
                if eng.state.values.get(k) != v:
                    eng.state.update(k, v, t, quiet=True)
        frame = eng.step(t)
        out.hd_next = 0.0
        out.send(frame)
        if out.hd_view is None:
            raise RuntimeError((said[-1] if said else "the HD screen stopped")[:300])
        t = round(t + STEP, 4)
    out.close()
    return msgs, end


def rules(msgs):
    """What a renderer relies on. Returns the faults found. / Ce sur quoi un moteur de rendu compte."""
    bad = []
    if not msgs or msgs[0].get("type") != "hello":
        return ["no hello first"]
    hello = msgs[0]
    if hello.get("protocol") != 1 or not hello["game"].get("detector"):
        bad.append(f"hello: protocol {hello.get('protocol')}, detector {hello['game'].get('detector')}")
    known = set(hello.get("events") or ()) | set(ALWAYS)
    seq, last_t = 0, -1.0
    for m in msgs[1:]:
        if m["type"] == "hello":
            bad.append("a second hello")
            continue
        if m["seq"] != seq + 1:
            bad.append(f"seq {m['seq']} after {seq}")
        seq = m["seq"]
        if m["t"] < last_t - 1e-6:
            bad.append(f"time goes back at seq {seq}: {m['t']} after {last_t}")
        last_t = m["t"]
        if m["type"] == "event":
            if m["name"] not in known:
                bad.append(f"event not announced in the hello: {m['name']}")
            if m["at"] < m["t"] - 1e-6:
                bad.append(f"{m['name']} to be shown before it was detected (seq {seq})")
    return bad[:12]


def summary(path, game, msgs, end):
    ev = [m for m in msgs if m["type"] == "event"]
    lines = [json.dumps([m["seq"], m["t"], m["at"], m["name"], m.get("side"), m["data"]], sort_keys=True,
                        ensure_ascii=False, separators=(",", ":")) for m in ev]
    st = [json.dumps([m["seq"], m["t"], m["state"]], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
          for m in msgs if m["type"] == "state"]
    return {"capture": os.path.basename(path), "game": game, "step": STEP, "seconds": round(end),
            "events": len(ev), "states": len(st),
            "counts": dict(sorted(collections.Counter(m["name"] for m in ev).items())),
            "stream": hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:20],
            "state_stream": hashlib.sha256("\n".join(st).encode("utf-8")).hexdigest()[:20]}


def bus_rules():
    """The bus itself, without a game: what a listener may count on. Returns the faults found.
    / Le bus lui-même, sans jeu : ce sur quoi un abonné peut compter."""
    from dmd import app, events
    bad, got = [], []
    bus = events.EventBus()
    if bus.emit("too.early", 1.0) is not None:
        bad.append("an event was sent while no game runs")
    bus.hello(0.0, {"key": "nogame", "title": "No game"}, ["score", "_hidden"], "0")
    bus.subscribe(got.append)
    if not got or got[0].get("type") != "hello" or got[0].get("values") != ["score"]:
        bad.append("a newcomer does not get the hello, or the hidden values are in it")
    bus.emit("a.b", 1.0, "p1", 2.5, None, {"name": "n", "side": "s", "at": 9})
    e = got[-1]
    if (e.get("name"), e.get("side"), e.get("t"), e.get("at"), e.get("data")) != ("a.b", "p1", 1.0, 2.5, {"name": "n", "side": "s", "at": 9}):
        bad.append(f"an event does not come out as it went in: {e}")
    if bus.last_time("a.b", "p1") != 1.0 or bus.last_time("a.b", "p2") != events.NEVER:
        bad.append("last_time is wrong")

    def broken(msg):
        raise ValueError("listener")
    bus.subscribe(broken, replay=False)
    bus.emit("a.c", 2.0)
    if broken in bus.subs or got[-1].get("name") != "a.c":
        bad.append("a listener that fails is kept, or stops the others")
    if bus.publish({"a": 1}, 2.0) is None or bus.publish({"a": 1}, 2.1) is not None or bus.publish({"a": 2}, 2.2) is None:
        bad.append("the state is not sent exactly when it changes")
    late = []
    bus.subscribe(late.append)
    if [m.get("type") for m in late] != ["hello", "state"]:
        bad.append("a late listener does not get the hello and the last state")
    seqs = [m["seq"] for m in got if "seq" in m]
    if seqs != list(range(1, len(seqs) + 1)):
        bad.append(f"the numbers do not follow one another: {seqs}")
    bus.bye(3.0)
    if got[-1].get("type") != "bye" or bus.emit("too.late", 4.0) is not None:
        bad.append("no bye, or an event after it")
    # the LED panel: a renderer draws in place of the scene, and a renderer that fails gives the panel back
    log = app.Logger(None, echo=False)
    cfg = dict(app.load_config(ROOT, log), retroarch={"enabled": False}, textfiles={"enabled": False},
               visual={"enabled": True, "led": True})
    calls = []

    def factory(engine):
        def paint(canvas, eng, now):
            calls.append(now)
            if len(calls) > 2:
                raise RuntimeError("painter")
            canvas.clear((1, 2, 3))
            return True
        return paint
    saved = list(events.LED_PAINTERS)
    events.led_painter(lambda key: key == "mslug2", factory)
    try:
        eng = app.Engine(ROOT, cfg, [], log, demo_game="mslug2")
        first = eng.step(0.02)
        eng.step(0.04)
        if eng.led_painter is None or bytes(first[:3]) != bytes((1, 2, 3)):
            bad.append("the renderer plugged on the LED panel did not draw it")
        after = eng.step(0.06)
        if eng.led_painter is not None or bytes(after[:3]) == bytes((1, 2, 3)):
            bad.append("a renderer that fails keeps the LED panel")
        plain = app.Engine(ROOT, dict(cfg, visual={"enabled": False}), [], log, demo_game="mslug2")
        if plain.led_painter is not None:
            bad.append("a renderer draws the LED panel while \"visual\" is off")
    finally:
        events.LED_PAINTERS[:] = saved
    return bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    out_dir = None
    if "--jsonl" in sys.argv:
        out_dir = args.pop(0) if args else None
        if not out_dir:
            print(__doc__)
            return 2
        os.makedirs(out_dir, exist_ok=True)
    importlib.import_module("dmd.hd")              # the scenes say on loading which games they follow / leurs jeux
    from dmd.events import detector_for
    files = args or sorted(glob.glob(os.path.join(ROOT, "tests", "captures", "*.log")))
    failed = done = 0
    if not args:
        bad = bus_rules()
        print(f"{'FAIL' if bad else 'ok  '} the bus and the LED panel's renderer / le bus et le moteur de la dalle")
        for b in bad:
            print("     " + b)
        failed += bool(bad)
    for path in files:
        base = os.path.basename(path)
        game = base.split("-20")[0]
        if not detector_for(game)[1]:
            continue                                # its scene does not speak on the bus yet / pas encore sur le bus
        msgs, end = replay(path, game)
        done += 1
        s = summary(path, game, msgs, end)
        bad = rules(msgs)
        ref_path = os.path.join(REFS, base[:-4] + ".json")
        if out_dir:
            with open(os.path.join(out_dir, base[:-4] + ".jsonl"), "w", encoding="utf-8", newline="\n") as f:
                for m in msgs:
                    f.write(json.dumps(m, ensure_ascii=False, separators=(",", ":")) + "\n")
        if write:
            os.makedirs(REFS, exist_ok=True)
            with open(ref_path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(s, f, ensure_ascii=False, indent=1, sort_keys=True)
                f.write("\n")
        elif not os.path.exists(ref_path):
            bad.append("no reference (python tools/events_check.py --write)")
        else:
            with open(ref_path, "r", encoding="utf-8") as f:
                ref = json.load(f)
            if ref != s:
                names = sorted(set(ref.get("counts", {})) | set(s["counts"]))
                moved = [f"{n} {ref.get('counts', {}).get(n, 0)} -> {s['counts'].get(n, 0)}" for n in names
                         if ref.get("counts", {}).get(n, 0) != s["counts"].get(n, 0)]
                bad.append("differs from its reference: " + (", ".join(moved) or "same counts, other figures or times"))
        print(f"{'FAIL' if bad else 'ok  '} {base}: {s['events']} events, {s['states']} states, {s['seconds']} s")
        for b in bad:
            print("     " + b)
        failed += bool(bad)
    print(f"{done} games replayed, {failed} failed / {done} parties rejouées, {failed} en échec")
    return 1 if failed or not done else 0


if __name__ == "__main__":
    sys.exit(main())
