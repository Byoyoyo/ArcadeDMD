"""Special moves recognised at the stick, in the panel under a human player's name (1.39).

The stick and buttons of each player are read at every image ("_in_p1" and "_in_p2", the BIOS bytes of the Neo Geo,
"fast"). When a button ends the motion of one of the fighter's moves ("specials" in the game file), the panel shows that
move, its arrows lit, for a moment. The move shown in turn lights its arrows as the stick does them. What is recognised
is the motion: the game alone knows whether the move came out.

A motion reads the other way round when the fighter faces left. The side each fighter faces is a byte of the game
("_p1_dir" and "_p2_dir"); what it holds when a round starts is "player 1 faces right, player 2 faces left", learnt
there and never assumed. Without it, a motion that would be another move of the fighter the other way round is not named.

Les coups spéciaux reconnus au stick, dans le panneau sous le nom d'un joueur humain. Le stick et les boutons de chaque
joueur sont lus à chaque image. Quand un bouton finit le geste d'un des coups du combattant, le panneau montre ce coup,
ses flèches allumées, un instant. Le coup montré à son tour allume ses flèches à mesure que le stick les fait. Ce qui est
reconnu, c'est le geste : seul le jeu sait si le coup est sorti.

Un geste se lit à l'envers quand le combattant regarde à gauche. Le côté que regarde chaque combattant est un octet du
jeu ; ce qu'il contient au début d'un round, c'est « le joueur 1 regarde à droite, le joueur 2 à gauche », appris là et
jamais supposé. Sans lui, un geste qui serait un autre coup du combattant dans l'autre sens n'est pas nommé."""
from .hd_moves import MIRROR, VEC, pressed, stick
from .i18n import tr

LAST = 0.35       # the button at the latest that long after the last direction began / le bouton au plus tard après
STEP = 0.30       # a direction at the latest that long after the one before began / une direction après la précédente
REST = 0.20       # the stick elsewhere at the most that long after the first direction / ailleurs après la première
CHARGE = 0.60     # a direction held that long is charged / une direction tenue aussi longtemps est chargée
TOGETHER = 0.09   # buttons pressed that close are pressed together / des boutons appuyés aussi près le sont ensemble
JUMP = 0.80       # the stick up that long ago: the fighter is in the air / le stick en haut : le combattant est en l'air
SHOW = 1.8        # the move recognised stays that long / le coup reconnu reste affiché ce temps
CALIBRATE = 5.0   # the facing bytes learnt in the first seconds of a round / appris aux premières secondes d'un round
STABLE = 1.0      # once they have held that long: the game sets its fighters a moment after its bars / une fois stables
KEEP = 64         # directions kept / directions gardées


def _n(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def steps_of(row):
    """The directions of a move, as written ('22' stays two taps). / Les directions du coup, telles qu'écrites."""
    return [int(c) for c in str(row.get("cmd", "")) if c.isdigit() and c not in "05"]


def _holds(d, want):
    """True when the stick at d holds the direction wanted: down-back charges back, and down. / d tient la direction."""
    (dx, dy), (wx, wy) = VEC[d], VEC[want]
    return (wx == 0 or dx == wx) and (wy == 0 or dy == wy) and (wx, wy) != (0, 0)


def groups_of(row):
    """'A/B' -> [['A', 'B']], 'B+C' -> [['B'], ['C']]. / Les groupes appuyés ensemble, chacun ses possibilités."""
    return [[x for x in g.split("/") if x] for g in str(row.get("btn", "")).split("+") if g]


def _assign(groups, have):
    """A different button of `have` for each group, or None. / Un bouton différent pour chaque groupe, sinon None."""
    if not groups:
        return set()
    for b in groups[0]:
        if b in have:
            rest = _assign(groups[1:], have - {b})
            if rest is not None:
                return rest | {b}
    return None


def motion(steps, dirs, t, charge=False):
    """When the motion began if the stick did these steps, the last one just before t, else None. dirs: [(t, numpad)],
    each change of the stick. One direction elsewhere is allowed between two steps, and a diagonal inside the motion may
    be missing when its two neighbours follow each other (read too late). charge: the first step held a while.
    / Le début du geste si le stick a fait ces étapes, la dernière juste avant t, sinon None."""
    ents = [e for e in dirs if e[0] <= t + 1e-6]
    n, m = len(ents), len(steps)
    if not n or not m:
        return None

    def end(i):
        return ents[i + 1][0] if i + 1 < n else t
    j, k = n - 1, m - 1
    nxt = None                                                    # where the step after this one began / l'étape d'après
    skipped = 0
    while k >= 0:
        want, found = steps[k], None
        first = k == 0
        for back in (0, 1):
            i = j - back
            if i < 0:
                break
            d = ents[i][1]
            if d == want or (charge and first and _holds(d, want)) or (charge and k == 1 and VEC[want][0] == 0 and _holds(d, want)):
                found = i
                break
        if found is None:
            if 0 < k < m - 1 and want in (1, 3, 7, 9) and skipped < max(1, m // 4) and j >= 0 and ents[j][1] == steps[k - 1]:
                skipped += 1                                      # a diagonal read too late / une diagonale lue trop tard
                k -= 1
                continue
            return None
        s = ents[found][0]
        if nxt is None:
            if t - s > LAST and not (charge and m == 1):
                return None                                       # the button too late / le bouton trop tard
        elif first:
            last = found
            if charge:                                            # held through its neighbours / tenue par ses voisines
                while last + 1 < n and _holds(ents[last + 1][1], want) and ents[last + 1][0] < nxt:
                    last += 1
            if nxt - end(last) > REST:
                return None
        elif nxt - s > STEP:
            return None
        if first and charge:
            a = found
            while a > 0 and _holds(ents[a - 1][1], want):
                a -= 1
            b = found
            while b + 1 < n and _holds(ents[b + 1][1], want) and (nxt is None or ents[b + 1][0] < nxt):
                b += 1
            if end(b) - ents[a][0] < CHARGE:
                return None                                       # not charged / pas chargée
            s = ents[a][0]
        nxt = s
        j = found - 1
        k -= 1
    return nxt


def progress(steps, dirs, now):
    """How many first steps of the motion the stick has just done, the last of them where it is now. / Le nombre de
    premières étapes du geste que le stick vient de faire, la dernière là où il est."""
    if not dirs or dirs[-1][1] == 5 or now - dirs[-1][0] > STEP + LAST:
        return 0
    for k in range(len(steps), 1, -1):
        if steps[k - 1] == dirs[-1][1] and motion(steps[:k], dirs, dirs[-1][0] + 1e-4) is not None:
            return k
    return 0


class Pad:
    """The stick and buttons of one player. / Le stick et les boutons d'un joueur."""

    def __init__(self):
        self.low = False             # the byte read the other way round (0 = pressed) / l'octet lu à l'envers
        self.odd = 0
        self.pend = []
        self.dirs = []               # (t, numpad) each change of the stick / chaque changement du stick
        self.btn = set()
        self.down = {}               # button -> when it was pressed / quand il a été appuyé
        self.seen = 0
        self.first = True
        self.hit = None              # (t, row, mirrored, groups, n) the move just recognised / le coup reconnu
        self.count = {}              # (fighter, move) -> times done / le nombre de fois
        self.base = None             # the facing byte when a round started / l'octet d'orientation au début d'un round
        self.vals = set()            # its values seen / ses valeurs vues


class Stick:
    """The moves recognised of each player. update() at every image, with the values and the input history.
    / Les coups reconnus de chaque joueur."""

    def __init__(self, hd=None):
        self.hd = hd
        self.pads = {"p1": Pad(), "p2": Pad()}
        self.key = None
        self.arm = None              # a round started then: the facing bytes are learnt / un round a commencé
        self.cal = None              # (since when, the two bytes) while they hold / depuis quand ils tiennent
        self.votes = {}              # what they held at each round's start / ce qu'ils tenaient à chaque début de round
        self.face_ok = None          # None not learnt yet, False not to be trusted / pas encore appris, False pas fiable
        self.many = False            # a facing byte with more than two values / un octet à plus de deux valeurs
        self.ready = {"p1": None, "p2": None}

    def log(self, fr, en):
        log = getattr(self.hd, "log", None)
        if callable(log):
            log(tr(fr, en))

    @staticmethod
    def wanted(game):
        """True for a game with moves to recognise and its stick read. / Un jeu aux coups connus dont le stick est lu."""
        if not isinstance(game, dict) or not isinstance(game.get("specials"), dict) or isinstance(game.get("moves"), dict):
            return False
        vals = (game.get("memory") or {}).get("values") or {}
        return "_in_p1" in vals

    def reset(self):
        self.pads = {"p1": Pad(), "p2": Pad()}
        self.arm, self.cal, self.votes, self.face_ok, self.many = None, None, {}, None, False

    def skip(self, hist):
        """No fight: the inputs read are left behind, the byte's way round decided again. / Pas de combat."""
        for side, pad in self.pads.items():
            entries = (hist or {}).get("_in_" + side) or []
            if entries:
                pad.seen = entries[-1][0]
            pad.low, pad.odd, pad.pend, pad.dirs, pad.btn, pad.down, pad.hit = False, 0, [], [], set(), {}, None

    def round_start(self, now):
        self.arm = now

    # ------------------------------------------------------------------ facing
    def _calibrate(self, vals, now, game):
        """A round started: what the two bytes hold, once they have held a second, is "player 1 faces right, player 2
        left". Each round votes, the most seen wins, and nothing is trusted while two readings disagree.
        / Un round a commencé : ce que tiennent les deux octets, stables une seconde, c'est « J1 à droite, J2 à gauche ».
        Chaque round vote, le plus vu l'emporte, et rien n'est cru tant que deux lectures se contredisent."""
        if self.arm is None:
            return
        if now - self.arm > CALIBRATE:
            self.arm = self.cal = None
            return
        d1, d2 = _n(vals.get("_p1_dir")), _n(vals.get("_p2_dir"))
        defs = ((game or {}).get("memory") or {}).get("values") or {}
        a, b = defs.get("_p1_dir") or {}, defs.get("_p2_dir") or {}
        shared = (a.get("addr"), a.get("ptr")) == (b.get("addr"), b.get("ptr"))
        if d1 is None or d2 is None or (not shared and d1 == d2):
            self.cal = None                                       # not yet face to face / pas encore face à face
            return
        if self.cal is None or self.cal[1] != (d1, d2):
            self.cal = (now, (d1, d2))
            return
        if now - self.cal[0] < STABLE:
            return
        self.arm = self.cal = None
        self.votes[(d1, d2)] = self.votes.get((d1, d2), 0) + 1
        ranked = sorted(self.votes.items(), key=lambda kv: -kv[1])
        base, ok = ranked[0][0], ranked[0][1] > 2 * (ranked[1][1] if len(ranked) > 1 else 0)
        p1, p2 = self.pads["p1"], self.pads["p2"]
        if (base, ok) != ((p1.base, p2.base), self.face_ok):
            if ok:
                self.log(f"Combat, orientation lue (J1 à droite 0x{int(base[0]):02X}, J2 à gauche 0x{int(base[1]):02X})",
                         f"Fight, facing read (P1 right 0x{int(base[0]):02X}, P2 left 0x{int(base[1]):02X})")
            else:
                self.log(f"Combat, orientation au début du round 0x{int(d1):02X} et 0x{int(d2):02X}, pas comme avant : "
                         "les gestes à double sens ne sont pas nommés",
                         f"Fight, facing at the round's start 0x{int(d1):02X} and 0x{int(d2):02X}, not as before: "
                         "the motions that read both ways are not named")
        p1.base, p2.base = base
        self.face_ok = ok

    def facing(self, side, vals):
        """1 when the fighter faces right, -1 left, None when it is not known. / 1 à droite, -1 à gauche, None inconnu."""
        pad = self.pads[side]
        cur = _n(vals.get(f"_{side}_dir"))
        if not self.face_ok or self.many or pad.base is None or cur is None:
            return None
        pad.vals.add(cur)
        if len(pad.vals) > 2:                                     # more than its two sides: not a facing byte after all
            if not self.many:
                self.many = True
                self.log(f"Combat, orientation de {side.upper()} à plus de deux valeurs, plus utilisée",
                         f"Fight, facing of {side.upper()} has more than two values, no longer used")
            return None
        start = 1 if side == "p1" else -1
        return start if cur == pad.base else -start

    # ------------------------------------------------------------------ reading
    def update(self, vals, hist, now, key, game, humans, ready=None):
        if key != self.key:
            self.key = key
            arm = self.arm                                        # the round that just started stays / le round reste
            self.reset()
            self.arm = arm
            self.skip(hist)                                       # the inputs read while the game loads are left behind
        self.ready = dict(ready or {})
        self._calibrate(vals, now, game)
        for side in ("p1", "p2"):
            pad = self.pads[side]
            entries = (hist or {}).get("_in_" + side) or []
            if entries and entries[-1][0] < pad.seen:
                pad.seen = 0
            for n, t, v in entries:
                if n > pad.seen and isinstance(v, (int, float)):
                    self._input(side, pad, t, int(v), game, vals, bool(humans.get(side)))
            if entries:
                pad.seen = max(pad.seen, entries[-1][0])
            if pad.hit is not None and now - pad.hit[0] > SHOW:
                pad.hit = None

    def _input(self, side, pad, t, v, game, vals, human):
        if pad.first:
            pad.first = False
            self.log(f"Combat, {side.upper()} touches lues (0x{v:02X})", f"Fight, {side.upper()} inputs read (0x{v:02X})")
        if not pad.low and ((v & 3) == 3 or (v & 12) == 12):       # up and down at once: the byte is the other way
            pad.odd += 1                                          # round once read three times (as the panel of The
            pad.pend.append((t, v))                               # King of Fighters) / haut et bas ensemble : l'octet
            if pad.odd < 3:                                       # est à l'envers une fois lu trois fois
                return
            pad.low = True
            pad.dirs, pad.btn, pad.down = [], set(), {}
            self.log(f"Combat, {side.upper()} touches à l'envers (0 = appuyé)", f"Fight, {side.upper()} inputs inverted (0 = pressed)")
            pend, pad.pend = pad.pend, []
            for pt, pv in pend:
                self._input(side, pad, pt, pv, game, vals, human)
            return
        if not pad.low and pad.pend:
            pad.pend.append((t, v))
            del pad.pend[:-48]
        d = stick(v, pad.low)
        if not pad.dirs or pad.dirs[-1][1] != d:
            pad.dirs.append((t, d))
            del pad.dirs[:-KEEP]
        btn = pressed(v, pad.low)
        new = btn - pad.btn
        pad.btn = btn
        for b in new:
            pad.down[b] = t
        if new and human:
            self._press(side, pad, t, new, game, vals)

    def rows(self, game, name, side):
        """(the moves that can come out now, the supers that cannot). / Les coups possibles, les supers qui ne le sont pas."""
        from .hd_specials import fighter_rows
        specials, supers = fighter_rows(game, name)
        if self.ready.get(side):
            return specials + supers, []
        return specials, supers

    def _best(self, rows, pad, t, new, orient):
        """The move these buttons end, facing that way: the longest motion, then the most buttons. / Le coup que finissent
        ces boutons dans ce sens : le geste le plus long, puis le plus de boutons."""
        together = {b for b in pad.btn if t - pad.down.get(b, -99.0) <= TOGETHER}
        best = None
        for row in rows:
            groups = groups_of(row)
            used = _assign(groups, together)
            if not used or not (used & new):
                continue
            steps = steps_of(row)
            hold = row.get("hold") or []
            charge = hold == [0]
            if hold and not charge:
                continue
            if len(steps) < 2 or row.get("when") in ("run", "crouch"):
                continue                                          # a button alone, or one direction: not a motion
            if orient < 0:
                steps = [MIRROR[c] for c in steps]
            began = motion(steps, pad.dirs, t, charge)
            if began is None:
                continue
            ends = [e[0] for e in pad.dirs[1:]] + [t]              # the stick up shortly before the motion: in the air
            up = any(d in (7, 8, 9) and dt < began and de > t - JUMP for (dt, d), de in zip(pad.dirs, ends))
            if (row.get("when") == "air") != up:
                continue                                          # a move of the air on the ground, or the reverse
            score = (len(steps), len(groups))
            if best is None or score > best[0]:
                best = (score, row, groups)
        return best

    def _press(self, side, pad, t, new, game, vals):
        name = vals.get(side + "_char")
        rows, later = self.rows(game, name, side)
        if not rows and not later:
            return
        face = self.facing(side, vals)
        found = {o: self._best(rows, pad, t, new, o) for o in ((face,) if face else (1, -1))}
        found = {o: b for o, b in found.items() if b is not None}
        tag = side.upper()
        if not found:
            return
        if len(found) == 2 and found[1][1] is not found[-1][1]:
            self.log(f"Combat, {tag} geste à double sens ({found[1][1].get('name')} ou {found[-1][1].get('name')}), pas nommé",
                     f"Fight, {tag} motion reads both ways ({found[1][1].get('name')} or {found[-1][1].get('name')}), not named")
            return
        orient = face or (1 if 1 in found else -1)
        score, row, groups = found[orient]
        if later:                                                 # a super the gauge does not allow, its motion done
            sup = self._best(later, pad, t, new, orient)
            if sup is not None and sup[0] >= score and self.ready.get(side) is None:
                self.log(f"Combat, {tag} geste de {sup[1].get('name')} ou de {row.get('name')}, jauge pas lue, pas nommé",
                         f"Fight, {tag} motion of {sup[1].get('name')} or {row.get('name')}, gauge not read, not named")
                return
        old = pad.hit
        if old is not None and t - old[0] <= TOGETHER and len(groups) <= len(old[3]):
            return                                                # the same press, read in two times / le même appui
        key = (str(name), str(row.get("name")))
        if old is not None and t - old[0] <= TOGETHER:
            okey = (str(name), str(old[1].get("name")))
            pad.count[okey] = max(0, pad.count.get(okey, 1) - 1)
        pad.count[key] = pad.count.get(key, 0) + 1
        pad.hit = (t, row, orient < 0, groups, pad.count[key])
        way = "" if face else tr(", orientation déduite", ", facing guessed")
        self.log(f"Combat, {tag} geste reconnu {row.get('name')} ({row.get('cmd')} + {row.get('btn')}), "
                 f"{'vers la gauche' if orient < 0 else 'vers la droite'}{way}",
                 f"Fight, {tag} motion recognised {row.get('name')} ({row.get('cmd')} + {row.get('btn')}), "
                 f"{'facing left' if orient < 0 else 'facing right'}{way}")

    # ------------------------------------------------------------------ for the panel
    def shown(self, side, now):
        """(row, mirrored, age, times done) of the move just recognised, or None. / Le coup qui vient d'être reconnu."""
        h = self.pads[side].hit
        if h is None or not 0 <= now - h[0] <= SHOW:
            return None
        return h[1], h[2], now - h[0], h[4]

    def done(self, side, row, mirrored, now):
        """How many first steps of this move the stick has just done. / Les premières étapes que le stick vient de faire."""
        steps = steps_of(row)
        if len(steps) < 2 or row.get("hold"):
            return 0
        if mirrored:
            steps = [MIRROR[c] for c in steps]
        return progress(steps, self.pads[side].dirs, now)
