"""Checks the moves recognised at the stick (dmd/hd_stick.py): motions read on a real match (a stick sampled every 10 to
80 ms, The King of Fighters '98) and the cases that must not be named. Run by the check of every pull request.

Vérifie les coups reconnus au stick : des gestes lus sur une vraie partie et les cas qui ne doivent pas être nommés.

usage: python tools/stick_check.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dmd.hd_stick import Stick, _assign, motion, progress  # noqa: E402

FAILS = []


def check(what, got, want):
    if got != want:
        FAILS.append(f"{what}: {got!r}, expected {want!r}")


def at(seq):
    """[(seconds before the button, direction)] -> the history the engine keeps. / L'historique du moteur."""
    return [(10.0 + t, d) for t, d in seq]


def did(steps, seq, charge=False, t=0.0):
    return motion(steps, at(seq), 10.0 + t, charge) is not None


# read on a real match / lus sur une vraie partie
HCB = [(-0.197, 6), (-0.113, 3), (-0.08, 2), (-0.047, 1), (-0.03, 4)]
HCF_REST = [(-0.357, 4), (-0.307, 1), (-0.257, 2), (-0.174, 3), (-0.14, 6), (-0.074, 5)]
QCF_HCB = [(-0.459, 2), (-0.326, 3), (-0.309, 6), (-0.192, 3), (-0.172, 2), (-0.092, 1), (-0.072, 4)]
QCF_UP = [(-0.883, 4), (-0.219, 1), (-0.186, 2), (-0.102, 3), (-0.053, 6), (-0.019, 9)]
check("half circle back", did([6, 3, 2, 1, 4], HCB), True)
check("half circle forward, the stick back at rest", did([4, 1, 2, 3, 6], HCF_REST), True)
check("quarter circle then half circle", did([2, 3, 6, 3, 2, 1, 4], QCF_HCB), True)
check("its last half circle alone", did([6, 3, 2, 1, 4], QCF_HCB), True)
check("quarter circle, the stick already going up", did([2, 3, 6], QCF_UP), True)
check("not the other way round", did([2, 1, 4], QCF_UP), False)
check("not a dragon punch", did([6, 2, 3], HCB), False)
# made up / inventés
check("a diagonal read too late", did([2, 3, 6], [(-0.10, 2), (-0.04, 6)]), True)
check("the button too late", did([2, 3, 6], [(-0.60, 2), (-0.55, 3), (-0.50, 6)]), False)
check("a pause inside the motion", did([2, 3, 6], [(-0.70, 2), (-0.65, 3), (-0.05, 6)]), False)
check("the first direction held, then the motion", did([2, 3, 6], [(-2.0, 2), (-0.10, 3), (-0.05, 6)]), True)
check("down twice", did([2, 2], [(-0.30, 2), (-0.20, 5), (-0.10, 2)]), True)
check("down once is not down twice", did([2, 2], [(-0.30, 5), (-0.10, 2)]), False)
check("charged back, forward", did([4, 6], [(-0.90, 4), (-0.05, 6)], charge=True), True)
check("charged down-back, forward", did([4, 6], [(-0.90, 1), (-0.30, 4), (-0.05, 6)], charge=True), True)
check("not charged long enough", did([4, 6], [(-0.35, 4), (-0.05, 6)], charge=True), False)
check("charged down, up-forward", did([2, 8], [(-0.80, 2), (-0.04, 9)], charge=True), True)
check("two buttons together", _assign([["B"], ["C"]], {"B", "C"}), {"B", "C"})
check("one of two is not both", _assign([["B"], ["C"]], {"B"}), None)
check("two kicks", _assign([["B", "D"], ["B", "D"]], {"B", "D"}), {"B", "D"})
check("one kick is not two", _assign([["B", "D"], ["B", "D"]], {"D"}), None)
check("steps lit as the stick goes", progress([2, 3, 6], at([(-0.10, 2), (-0.04, 3)]), 10.0), 2)
check("nothing lit at rest", progress([2, 3, 6], at([(-0.10, 2), (-0.04, 5)]), 10.0), 0)

# the whole way: the bytes of the BIOS, the fighter's moves, the side he faces / du BIOS au coup nommé
GAME = {"memory": {"values": {"_in_p1": {}, "_in_p2": {}, "_p1_dir": {"addr": "0x1"}, "_p2_dir": {"addr": "0x2"}}},
        "specials": {"TEST": [{"name": "FORWARD", "cmd": "236", "btn": "A/B", "kind": "special"},
                              {"name": "BACK", "cmd": "214", "btn": "A/B", "kind": "special"},
                              {"name": "RISING", "cmd": "623", "btn": "A", "kind": "special"},
                              {"name": "SUPER", "cmd": "236236", "btn": "A", "kind": "super"}]}}
BIT = {5: 0, 8: 1, 2: 2, 4: 4, 6: 8, 1: 6, 3: 10, 7: 5, 9: 9}
LOGS = []


class Hd:
    @staticmethod
    def log(msg):
        LOGS.append(msg)


def run(presses, dirs=None, ready=None, calibrate=True):
    """presses: [(t, [directions], button bit)] played 50 ms a step; dirs: [(t, p1 byte, p2 byte)]. Returns the names."""
    st = Stick(Hd())
    hist = {"_in_p1": []}
    events = [(0.0, 0)]
    for t, seq, btn in presses:
        for i, d in enumerate(seq):
            events.append((t + i * 0.05, BIT[d]))
        tb = t + (len(seq) - 1) * 0.05 + 0.03
        events += [(tb, BIT[seq[-1]] | btn), (tb + 0.1, 0)]
    vals = {"p1_char": "TEST"}
    names, now, k = [], 0.0, 0
    faces = list(dirs or [(0.0, 1, 0)])
    st.update(vals, hist, 0.0, "test", GAME, {"p1": True}, ready)
    if calibrate:
        st.round_start(0.0)
    while now < events[-1][0] + 0.5:
        while faces and faces[0][0] <= now:
            _, vals["_p1_dir"], vals["_p2_dir"] = faces.pop(0)
        while k < len(events) and events[k][0] <= now:
            hist["_in_p1"].append((k + 1, events[k][0], events[k][1]))
            k += 1
        st.update(vals, hist, now, "test", GAME, {"p1": True}, ready)
        h = st.shown("p1", now)
        if h is not None and (not names or names[-1] != h[0]["name"]):
            names.append(h[0]["name"])
        now += 1 / 60
    return names


A = 0x10
check("facing right", run([(3.0, [2, 3, 6], A)]), ["FORWARD"])
check("facing left, the same stick is the other move", run([(3.0, [2, 3, 6], A)], [(0.0, 1, 0), (2.0, 0, 1)]), ["BACK"])
check("side not known: a motion that reads both ways is not named", run([(3.0, [2, 3, 6], A)], calibrate=False), [])
check("side not known: a motion that reads one way is", run([(3.0, [6, 2, 3], A)], calibrate=False), ["RISING"])
check("the super when the gauge allows it", run([(3.0, [2, 3, 6, 5, 2, 3, 6], A)], ready={"p1": True}), ["SUPER"])
check("its last motion when the gauge is empty", run([(3.0, [2, 3, 6, 5, 2, 3, 6], A)], ready={"p1": False}), ["FORWARD"])
check("nothing when the gauge is not read", run([(3.0, [2, 3, 6, 5, 2, 3, 6], A)]), [])
st = Stick(Hd())
for start, d1, d2 in ((0.0, 1, 0), (10.0, 0, 1)):                    # two rounds that say the opposite / deux rounds opposés
    st.round_start(start)
    for i in range(80):
        st.update({"_p1_dir": d1, "_p2_dir": d2}, {}, start + i / 60, "test", GAME, {"p1": True})
    check(f"side trusted after the round at {start:.0f} s", st.facing("p1", {"_p1_dir": d1}), 1 if start == 0 else None)

if FAILS:
    print("\n".join(FAILS))
    sys.exit(1)
print("stick: ok")
