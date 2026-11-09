"""Desperation moves of a fighting game on the HD screen (The King of Fighters '98, 1.32, Seb).

Under the name of each human player, a panel: the power gauge as the game shows it (the bar, a green square per stock,
3 for the first fighter of a team, one more for each teammate beaten), and when the gauge allows one, the commands of
the fighter's desperation moves ("moves" in the game file). The arrows of a command light up as the stick does them,
read at every image (BIOS_P1CURRENT and BIOS_P2CURRENT of the Neo Geo, "_in_p1" and "_in_p2", "fast"). When a button
ends an attempt that missed a step, the steps missed are crossed in red with RATÉ, and DM ! or SDM ! comes once the game
took its stock (or its full gauge in Extra). Against a human, the matches each player won ("wins" of FightFX).

Les coups désespérés sur l'écran HD : sous le nom de chaque joueur humain, la jauge comme dans le jeu (la barre, un carré
vert par stock), et quand la jauge le permet, les commandes des coups désespérés du combattant. Les flèches s'allument
quand le stick les fait, lu à chaque image. Quand un bouton finit une tentative à qui il manque une étape, les étapes
manquées sont barrées en rouge avec RATÉ, et DM ! ou SDM ! vient quand le jeu a pris son stock. Contre un humain, les
matchs gagnés par chacun."""
import math

from .i18n import tr

GOLD = (255, 214, 120)
CREAM = (238, 228, 208)
WHITE = (255, 255, 255)
GREY = (120, 128, 150)
DIM = (70, 76, 96)
MISS = (255, 70, 50)
AMBER = (255, 176, 0)
BTN_COL = {"A": (232, 52, 44), "B": (250, 200, 30), "C": (40, 190, 80), "D": (40, 120, 235)}   # Neo Geo buttons
BTN_BIT = {"A": 0x10, "B": 0x20, "C": 0x40, "D": 0x80}
CLASS = {"P": "AC", "K": "BD"}                       # a punch is A or C, a kick B or D / un poing A ou C, un pied B ou D
NUM = {(-1, 1): 1, (0, 1): 2, (1, 1): 3, (-1, 0): 4, (0, 0): 5, (1, 0): 6, (-1, -1): 7, (0, -1): 8, (1, -1): 9}
VEC = {v: k for k, v in NUM.items()}
MIRROR = {1: 3, 3: 1, 4: 6, 6: 4, 7: 9, 9: 7, 2: 2, 5: 5, 8: 8}
ARROW = {1: "↙", 2: "↓", 3: "↘", 4: "←", 6: "→", 7: "↖", 8: "↑", 9: "↗"}
WINDOW = 1.6          # an attempt: the stick in the last 1.6 s / une tentative : le stick des 1,6 dernières secondes
PAUSE = 0.45          # the stick at rest that long ends a motion / le stick au repos aussi longtemps finit un geste
NEAR = 0.75           # RATÉ only for a near miss (a step or so), not for a special move / seulement pour un coup presque fait
CONFIRM = 0.8         # the game takes its stock that soon after the button / le jeu prend son stock aussi vite
SHOW = 1.6            # RATÉ, DM ! or SDM ! stays that long / reste affiché ce temps
MAX_LONG = 15.0       # MAX over at the latest / le MAX fini au plus tard
# the MAX timer of Advanced (0x1081EA, "_maxv"): the MAME cheat Infinite Power holds it at 0x40; in Seb's log the CPU's MAX
# set it to 0x3F and it counted down, a desperation move or a guard cancel only to 0x01 (1.32 test 8c). MAX while it is
# at 2 or more / le chrono du MAX d'Advanced : le code MAME Infinite Power le tient à 0x40 ; dans le log de Seb, le MAX de
# l'ordinateur l'a mis à 0x3F et il a décompté, un coup désespéré ou une garde annulée seulement à 0x01. MAX dès 2
MAXV_ON = 2
MAXV_FULL = 0x40
EXTRA_LONG = 30.0     # MAX of Extra over at the latest, else when its gauge is empty / le MAX d'Extra, au plus tard
INPUT_KEEP = 3.0      # the inputs shown that long after the last one, then they fade / les touches restent ce temps
RED_HEALTH = 25       # Extra: the desperation moves are free with the health this low / gratuits avec si peu de vie
FULL_POW = 0xA0       # the gauge full (MAX in Extra) / la jauge pleine
# The King of Fighters '97 fills its gauge to 0x80, not 0xA0: "pow_full" in the "hd" block of the game file (1.33 test 49)
# / '97 remplit sa jauge jusqu'à 0x80 : "pow_full" dans le bloc "hd" du fichier du jeu


def full_pow(game):
    """The gauge full for this game. / La jauge pleine pour ce jeu."""
    hd = (game or {}).get("hd") if isinstance(game, dict) else None
    v = hd.get("pow_full") if isinstance(hd, dict) else None
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else FULL_POW


def maxv_full(game):
    """The MAX timer when MAX starts: 0x40 in '98, 0x2F in 2002 ("maxv_full" in hd, 1.33 test 50). / Le chrono du MAX."""
    hd = (game or {}).get("hd") if isinstance(game, dict) else None
    v = hd.get("maxv_full") if isinstance(hd, dict) else None
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else MAXV_FULL


def max_buttons(game):
    """The buttons that start MAX: A+B+C in '98 and '97, B+C in 2002 ("max_buttons" in hd). / Les boutons du MAX."""
    hd = (game or {}).get("hd") if isinstance(game, dict) else None
    v = hd.get("max_buttons") if isinstance(hd, dict) else None
    if isinstance(v, str) and len(v) >= 2 and set(v) <= set("ABCD"):
        return set(v)
    return {"A", "B", "C"}


def max_dm_free(game):
    """True when a desperation move in MAX takes no stock, an SDM one (2002, "max_dm_free" in hd). / Un DM en MAX gratuit."""
    hd = (game or {}).get("hd") if isinstance(game, dict) else None
    return isinstance(hd, dict) and hd.get("max_dm_free") is True


def stick(byte, low=False):
    """The numpad direction (5 at rest) of a BIOS input byte: bit 0 up, 1 down, 2 left, 3 right. / La direction."""
    if low:
        byte ^= 0xFF
    x = (1 if byte & 8 else 0) - (1 if byte & 4 else 0)
    y = (1 if byte & 2 else 0) - (1 if byte & 1 else 0)
    return NUM[(x, y)]


def pressed(byte, low=False):
    """The buttons pressed in a BIOS input byte: bits 4 to 7, A B C D. / Les boutons appuyés."""
    if low:
        byte ^= 0xFF
    return {b for b, bit in BTN_BIT.items() if byte & bit}


def parse_cmd(text):
    """'236 214' -> [2, 3, 6, 2, 1, 4]: a motion after another, the shared direction kept once (qcb, hcf is 2141236).
    / Les gestes à la suite, la direction commune gardée une fois."""
    out = []
    for part in str(text).split():
        for ch in part:
            if not ch.isdigit() or ch in "05":
                continue
            d = int(ch)
            if not out or out[-1] != d:
                out.append(d)
    return out


def lcs(cmd, seq):
    """For each step of the command, True when it is in a longest common subsequence with what the stick did, in order.
    / Pour chaque étape de la commande, vrai si elle est faite, dans l'ordre."""
    n, m = len(cmd), len(seq)
    t = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            t[i][j] = t[i + 1][j + 1] + 1 if cmd[i] == seq[j] else max(t[i + 1][j], t[i][j + 1])
    hit = [False] * n
    i = j = 0
    while i < n and j < m:
        if cmd[i] == seq[j]:
            hit[i] = True
            i += 1
            j += 1
        elif t[i + 1][j] >= t[i][j + 1]:
            i += 1
        else:
            j += 1
    return hit


def _n(v):
    if isinstance(v, bool):
        return None
    return v if isinstance(v, (int, float)) else None


def _stock(vals, suf):
    """The stocks, 0 to 5, else None (not this address after all). / Les stocks, de 0 à 5, sinon None."""
    v = _n(vals.get("_stock" + suf))
    return v if v is not None and 0 <= v <= 5 else None


class Side:
    def __init__(self):
        self.low = False             # the BIOS byte read the other way round / l'octet lu à l'envers
        self.odd = 0                 # reads with up and down, or left and right, at once / lectures haut et bas ensemble
        self.pend = []               # (t, byte) read since the first of them / lus depuis la première
        self.dirs = []               # (t, numpad) each change of the stick / chaque changement du stick
        self.seen = 0                # number of the last input history entry read / numéro de la dernière entrée lue
        self.first = True            # nothing read yet (logged once) / rien lu encore (noté une fois)
        self.prev_btn = set()
        self.stock = None
        self.stock_raw = None
        self.pow = None
        self.mode = None
        self.maxv = None
        self.max_on = None           # since when MAX is on (A+B+C and a stock gone) / depuis quand le MAX est lancé
        self.max_seen = False        # its timer (the candidate "_maxv") seen running / son chrono vu tourner
        self.max_extra = False       # the MAX of Extra: the gauge full, over once it is empty / le MAX d'Extra
        self.max_low = None          # the gauge at its lowest during MAX (Advanced) / la jauge au plus bas pendant le MAX
        self.max_log = -99.0         # when MAX was last written in the log / quand le MAX a été noté
        self.groups = []             # (t, direction or None, [buttons]) the inputs as training mode shows them
        self.abc_t = -99.0
        self.press = None            # (t, buttons) the last button pressed / le dernier bouton appuyé
        self.attempt = None          # (t, row, states, full, mirrored) a button after a motion, the game not heard yet
        self.result = None           # (t, row, text, colour, states, mirrored) RATÉ, DM !, SDM !
        self.live = None             # (row, states, mirrored) what the stick is doing now / ce que fait le stick
        self.dm_bit = None           # the game's own desperation move flag ("_dm", bit 0), last read / le drapeau du jeu
        self.spent_t = -99.0         # when the game last took a stock or its gauge / quand le jeu a pris un stock
        self.res_max = False         # the last DM ! or SDM ! came in MAX / le dernier DM ! ou SDM ! est venu en MAX


class Moves:
    """The panel of each player. update() at every image with the values and the input history of the engine.
    / Le panneau de chaque joueur."""

    def __init__(self, hd):
        self.hd = hd
        self.sides = {"p1": Side(), "p2": Side()}
        self.key = None
        self.icons = {}
        self.pow_full = FULL_POW

    def reset(self):
        self.sides = {"p1": Side(), "p2": Side()}

    def log(self, fr, en):
        log = getattr(self.hd, "log", None)
        if callable(log):
            log(tr(fr, en))

    # ------------------------------------------------------------------ reading
    def rows(self, game, name):
        """[(name, steps, button class)] of the fighter's desperation moves, from "moves" in the game file.
        / Les coups désespérés du combattant."""
        moves = (game or {}).get("moves") if isinstance(game, dict) else None
        if not isinstance(moves, dict) or not isinstance(name, str):
            return []
        out = []
        for m in moves.get(name.upper()) or moves.get(name) or []:
            if isinstance(m, dict) and m.get("cmd"):
                steps = parse_cmd(m["cmd"])
                if len(steps) >= 2:
                    out.append((str(m.get("name", "")), steps, str(m.get("btn", "P"))))
        return out[:3]

    def skip(self, hist):
        """No fight (select screen, demo): the inputs read are left behind, the gauge forgotten. / Pas de combat : les
        touches lues sont laissées de côté."""
        for side, sd in self.sides.items():
            entries = (hist or {}).get("_in_" + side) or []
            if entries:
                sd.seen = entries[-1][0]
            sd.attempt = sd.result = sd.live = None
            sd.max_on = None
            sd.groups = []
            sd.low, sd.odd, sd.pend, sd.dirs, sd.prev_btn = False, 0, [], [], set()   # the byte's way round decided again: the
            # memory RetroArch gives while the game loads (0xFD) once made every input of a game read backwards
            # (Seb's KOF '97, 1.33 test 49) / le sens de l'octet décidé à nouveau au combat suivant : la mémoire que
            # RetroArch donne pendant le chargement du jeu (0xFD) avait fait lire toutes les touches d'une partie à l'envers
            sd.dm_bit = None

    def update(self, vals, hist, now, key, game, humans):
        if key != self.key:
            self.key = key
            self.reset()
            for side, sd in self.sides.items():                   # the inputs read before this game's first fight are
                entries = (hist or {}).get("_in_" + side) or []   # left behind: the memory RetroArch gives while the
                if entries:                                       # game loads (0xFD) made every input of Seb's KOF '98
                    sd.seen = entries[-1][0]                      # read backwards, no DM ! nor show (9 November, 1.33
                    # test 52) / les touches lues avant le premier combat du jeu sont laissées : la mémoire donnée
                    # pendant le chargement (0xFD) faisait lire toutes les touches de son KOF '98 à l'envers
        self.pow_full = full_pow(game)
        for side in ("p1", "p2"):
            sd = self.sides[side]
            suf = "" if side == "p1" else "_p2"
            # the stick and buttons first, each at the time it was read / le stick et les boutons d'abord
            entries = (hist or {}).get("_in_" + side) or []
            if entries and entries[-1][0] < sd.seen:
                sd.seen = 0                                       # the history started again / l'historique repart
            for n, t, v in entries:
                if n > sd.seen and isinstance(v, (int, float)):
                    self._input(side, sd, t, int(v), game, vals)
            if entries:
                sd.seen = max(sd.seen, entries[-1][0])
            self._gauge(side, sd, vals, suf, now, game)
            # the motion going on, lit as it goes / le geste en cours, allumé au fur et à mesure
            sd.live = self._best(side, sd, now, game, vals, final=False) if humans.get(side) else None
            if sd.attempt is not None and now - sd.attempt[0] > CONFIRM:
                t, row, states, full, mir = sd.attempt
                sd.attempt = None
                health = _n(vals.get("health" if side == "p1" else "health_p2"))
                if not self.available(side, vals, health):
                    pass                                          # nothing could come out / rien ne pouvait sortir
                elif not full:                                    # a step or so missed: RATÉ / une étape manquée
                    sd.result = (t, row, "RATÉ", MISS, states, mir)
                    self._log_try(side, vals, game, row, states, "RATÉ")
                else:                                             # all done, the game took nothing: lit a moment, no
                    sd.result = (t, row, None, None, states, mir)  # word (too slow, or the stock read elsewhere)
                    self._log_try(side, vals, game, row, states, tr("complet, rien de pris", "complete, nothing taken"))

    def _gauge(self, side, sd, vals, suf, now, game=None):
        """The stock, the gauge, the mode and the candidate MAX timer: what the game took. / Ce que le jeu a pris."""
        pow_, mode, maxv, raw = (_n(vals.get(k + suf)) for k in ("_pow", "_pmode", "_maxv", "_stock"))
        stock = _stock(vals, suf)
        tag = side.upper()
        if raw is not None and raw != sd.stock_raw and (stock is None or sd.stock_raw is None or not 0 <= sd.stock_raw <= 5):
            self.log(f"Combat, {tag} stock lu 0x{int(raw):02X}" + ("" if stock is not None else ", hors de 0 à 5"),
                     f"Fight, {tag} stock read 0x{int(raw):02X}" + ("" if stock is not None else ", outside 0 to 5"))
        sd.stock_raw = raw if raw is not None else sd.stock_raw
        if mode is not None and mode != sd.mode:
            self.log(f"Combat, {tag} mode {int(mode)} ({'Extra' if mode == 1 else 'Advanced' if mode == 0 else '?'})",
                     f"Fight, {tag} mode {int(mode)} ({'Extra' if mode == 1 else 'Advanced' if mode == 0 else '?'})")
        if stock is not None and stock != sd.stock and sd.stock is not None:
            self.log(f"Combat, {tag} stock {int(sd.stock)} -> {int(stock)} (jauge 0x{int(pow_ or 0):02X})",
                     f"Fight, {tag} stock {int(sd.stock)} -> {int(stock)} (gauge 0x{int(pow_ or 0):02X})")
            if stock < sd.stock:
                self._spent(side, sd, now, vals, game, took=True)
        dm = _n(vals.get("_dm" + suf))
        if dm is not None:
            # the game's own flag of a desperation move ("_dm", bit 0 while one runs; The King of Fighters '97, 1.33 test
            # 49): the move came out, even when the gauge of Extra empties over a second rather than at once / le drapeau
            # du jeu : le coup est sorti, même quand la jauge d'Extra se vide en une seconde plutôt que d'un coup
            bit = int(dm) & 1
            if bit and sd.dm_bit == 0 and now - sd.spent_t > 1.0:
                self.log(f"Combat, {tag} coup désespéré (drapeau du jeu 0x{int(dm):02X})",
                         f"Fight, {tag} desperation move (game flag 0x{int(dm):02X})")
                self._spent(side, sd, now, vals, game)
            sd.dm_bit = bit
        if maxv is not None and sd.maxv is not None and (maxv == 0) != (sd.maxv == 0):
            self.log(f"Combat, {tag} MAX ? _maxv 0x{int(sd.maxv):02X} -> 0x{int(maxv):02X}",
                     f"Fight, {tag} MAX? _maxv 0x{int(sd.maxv):02X} -> 0x{int(maxv):02X}")
        if mode == 1 and pow_ is not None:
            # Extra: the gauge full is MAX, until it is empty or a desperation move uses it all at once (1.32 test 3)
            # Extra : la jauge pleine, c'est le MAX, jusqu'à ce qu'elle soit vide ou qu'un coup désespéré la prenne d'un coup
            if pow_ >= self.pow_full and (sd.pow is None or sd.pow < self.pow_full) and sd.max_on is None:
                sd.max_on, sd.max_seen, sd.max_extra = now, False, True
                self.log(f"Combat, {tag} jauge pleine, MAX (0x{int(pow_):02X})", f"Fight, {tag} gauge full, MAX (0x{int(pow_):02X})")
            elif sd.max_on is not None and sd.max_extra and sd.pow is not None and sd.pow - pow_ >= 0x20:
                self.log(f"Combat, {tag} jauge 0x{int(sd.pow):02X} -> 0x{int(pow_):02X} d'un coup",
                         f"Fight, {tag} gauge 0x{int(sd.pow):02X} -> 0x{int(pow_):02X} at once")
                self._spent(side, sd, now, vals, game)            # used by a desperation move / prise par un coup
                sd.max_on = None
            elif sd.max_on is not None and sd.max_extra and pow_ <= 0x04:
                sd.max_on = None
                self.log(f"Combat, {tag} fin du MAX (jauge vide)", f"Fight, {tag} MAX over (gauge empty)")
        if mode != 1 and maxv is not None:
            # Advanced: MAX while its timer runs, whatever the buttons (1.32 test 8c) / MAX tant que son chrono tourne
            on = maxv >= MAXV_ON
            if on and (sd.max_on is None or sd.max_extra) and (sd.maxv is None or maxv > sd.maxv):   # set again (not the
                # end of the one an SDM just used) / remis (pas la fin de celui qu'un SDM vient de prendre)
                sd.max_on, sd.max_seen, sd.max_extra = now, True, False
                sd.max_low, sd.max_log = None, now
                self.log(f"Combat, {tag} MAX (_maxv 0x{int(maxv):02X}, jauge 0x{int(pow_ or 0):02X})",
                         f"Fight, {tag} MAX (_maxv 0x{int(maxv):02X}, gauge 0x{int(pow_ or 0):02X})")
            elif not on and sd.max_on is not None and not sd.max_extra:
                att = sd.attempt
                if att is not None and now - att[0] < CONFIRM + 0.3:  # a desperation move in MAX: SDM !, MAX over
                    self._spent(side, sd, now, vals, game)            # un coup désespéré en MAX : SDM !, fin du MAX
                sd.max_on = None
                self.log(f"Combat, {tag} fin du MAX (_maxv 0x{int(maxv):02X})", f"Fight, {tag} MAX over (_maxv 0x{int(maxv):02X})")
        if sd.max_on is not None and (maxv is None or sd.max_extra):
            if maxv:
                sd.max_seen = True
            why = None
            if sd.max_extra:
                if now - sd.max_on > EXTRA_LONG:
                    why = tr("au plus tard", "at the latest")
            else:
                # Advanced: the game does not fill its gauge nor give a stock during MAX. A stock gained, or the gauge
                # filling again, is MAX over (Seb, 1.32 test 7, MAX stayed lit after the game's)
                # Advanced : le jeu ne remplit pas sa jauge et ne donne pas de stock pendant le MAX. Un stock gagné, ou la
                # jauge qui se remplit à nouveau, c'est la fin du MAX (le MAX restait allumé après celui du jeu)
                if pow_ is not None and now - sd.max_on > 0.5:
                    sd.max_low = pow_ if sd.max_low is None else min(sd.max_low, pow_)
                if now - sd.max_on > MAX_LONG:
                    why = tr("au plus tard", "at the latest")
                elif sd.max_seen and maxv == 0:
                    why = "_maxv 0"
                elif stock is not None and sd.stock is not None and stock > sd.stock:
                    why = tr("un stock gagné", "a stock gained")
                elif pow_ is not None and sd.max_low is not None and pow_ >= sd.max_low + 0x10:
                    why = tr(f"la jauge se remplit (0x{int(sd.max_low):02X} -> 0x{int(pow_):02X})",
                             f"the gauge fills (0x{int(sd.max_low):02X} -> 0x{int(pow_):02X})")
            if why is None and now - sd.max_log >= 1.0:               # MAX in the log once a second, to set its end
                sd.max_log = now                                      # le MAX noté une fois par seconde, pour régler sa fin
                self.log(f"Combat, {tag} MAX depuis {now - sd.max_on:.1f} s (jauge 0x{int(pow_ or 0):02X}, _maxv 0x{int(maxv or 0):02X})",
                         f"Fight, {tag} MAX for {now - sd.max_on:.1f} s (gauge 0x{int(pow_ or 0):02X}, _maxv 0x{int(maxv or 0):02X})")
            if why is not None:
                sd.max_on, sd.max_low = None, None
                self.log(f"Combat, {tag} fin du MAX ({why})", f"Fight, {tag} MAX over ({why})")
        sd.stock, sd.pow, sd.mode, sd.maxv = (stock if stock is not None else sd.stock, pow_ if pow_ is not None else sd.pow,
                                              mode if mode is not None else sd.mode, maxv if maxv is not None else sd.maxv)

    def _input(self, side, sd, t, v, game, vals):
        if sd.first:
            sd.first = False
            self.log(f"Combat, {side.upper()} touches lues (0x{v:02X})", f"Fight, {side.upper()} inputs read (0x{v:02X})")
        if not sd.low and ((v & 3) == 3 or (v & 12) == 12):       # up and down at once: impossible the right way round,
            sd.odd += 1                                           # left aside; read three times, the byte is the other
            sd.pend.append((t, v))                                # way round (0 when pressed) and what was read since
            if sd.odd < 3:                                        # the first is read again so: one stray byte no longer
                return                                            # turns a whole game round (1.33 test 52) / impossible
            sd.low = True                                         # à l'endroit, laissé ; lu trois fois, l'octet est à
            sd.dirs, sd.prev_btn, sd.groups = [], set(), []       # l'envers et ce qui a été lu depuis le premier est relu
            sd.attempt, sd.abc_t = None, -99.0
            self.log(f"Combat, {side.upper()} touches à l'envers (0 = appuyé)", f"Fight, {side.upper()} inputs inverted (0 = pressed)")
            pend, sd.pend = sd.pend, []
            for pt, pv in pend:
                self._input(side, sd, pt, pv, game, vals)
            return
        if not sd.low and sd.pend:
            sd.pend.append((t, v))
            del sd.pend[:-48]
        d = stick(v, sd.low)
        moved = not sd.dirs or sd.dirs[-1][1] != d
        if moved:
            sd.dirs.append((t, d))
            if len(sd.dirs) > 48:
                del sd.dirs[:len(sd.dirs) - 48]
        btn = pressed(v, sd.low)
        new = btn - sd.prev_btn
        sd.prev_btn = btn
        self._group(sd, t, d, new, moved)
        if not new:
            return
        mb = max_buttons(game)
        if mb <= btn:
            if t - sd.abc_t > 2.0:
                self.log(f"Combat, {side.upper()} {'+'.join(sorted(mb))}", f"Fight, {side.upper()} {'+'.join(sorted(mb))}")
            sd.abc_t = t                                          # A+B+C: MAX asked / MAX demandé
            return
        sd.press = (t, new)
        att = self._best(side, sd, t, game, vals, final=True, buttons=new)
        if att is not None:
            sd.attempt = (t,) + att
            sd.result = None

    @staticmethod
    def _group(sd, t, d, new, moved):
        """The inputs as training mode shows them: each direction the stick takes, the buttons pressed with it.
        / Les touches comme le mode entraînement : chaque direction du stick, les boutons appuyés avec."""
        g = sd.groups
        if moved and d != 5:
            g.append((t, d, []))
        if new:
            b = sorted(new)
            if g and t - g[-1][0] <= 0.12 and (not g[-1][2] or t - g[-1][0] <= 0.05):
                g[-1] = (g[-1][0], g[-1][1], sorted(set(g[-1][2]) | set(b)))   # pressed with it / appuyés avec
            else:
                g.append((t, d if d != 5 else None, b))
        if len(g) > 24:
            del g[:len(g) - 24]

    def _spent(self, side, sd, now, vals, game=None, took=False):
        """The game took a stock (or the full gauge in Extra): MAX after A+B+C, else the desperation move tried just
        before. A stock can also go to a guard cancel: nothing then. / Le jeu a pris un stock : le MAX après A+B+C,
        sinon le coup désespéré tenté juste avant ; un stock peut aussi partir dans une garde annulée."""
        tag = side.upper()
        att = sd.attempt
        twice = ("_dm" + ("" if side == "p1" else "_p2")) in vals and now - sd.spent_t <= 1.0
        free = max_dm_free(game)
        if twice and sd.result is not None and sd.result[2] in ("DM !", "SDM !") and now - sd.result[0] <= 1.0:
            if free and took and sd.result[2] == "DM !" and sd.res_max:
                # 2002: the flag first, then a stock in MAX, it was an SDM / le drapeau d'abord, puis un stock en MAX : un SDM
                r = sd.result
                sd.result = (r[0], r[1], "SDM !", GOLD, r[4], r[5])
                sd.max_on = None
                self._log_try(side, vals, None, r[1], r[4], "SDM")
            return                                                # the same move heard twice, its flag and its stock
                                                                  # le même coup entendu deux fois, drapeau et stock
        if now - sd.abc_t < CONFIRM and (att is None or att[0] < sd.abc_t + 0.1):
            if _n(vals.get("_pmode" + ("" if side == "p1" else "_p2"))) == 1:
                return                                            # Extra: A+B+C charges the gauge / charge la jauge
            mv = _n(vals.get("_maxv" + ("" if side == "p1" else "_p2")))
            if mv is None:
                self._max_on(side, sd, now, vals)                 # no MAX timer read: A+B+C and a stock, MAX
                return
            if mv >= MAXV_ON:
                return                                            # its timer says MAX / son chrono dit le MAX
            # A+B+C, a stock taken, and no MAX: a guard cancel or a desperation move (Seb, 1.32 test 8b, MAX lit at
            # the life in the red) / pas de MAX : une garde annulée ou un coup désespéré (MAX allumé dans le rouge)
            self.log(f"Combat, {tag} A+B+C et un stock pris sans MAX (_maxv 0x{int(mv):02X})",
                     f"Fight, {tag} A+B+C and a stock taken, no MAX (_maxv 0x{int(mv):02X})")
            if att is None or now - att[0] > CONFIRM + 0.6:
                return                                            # no desperation move tried: a guard cancel / garde annulée
        if att is None or now - att[0] > CONFIRM + 0.6:
            # no attempt seen: a shorter form of the command the game takes too, or a step not read. The last button
            # pressed, looked at more leniently / pas de tentative vue : une forme plus courte que le jeu prend aussi,
            # ou une étape pas lue ; le dernier bouton appuyé, regardé avec plus d'indulgence
            p = sd.press
            if p is None or now - p[0] > CONFIRM + 0.6:
                return
            found = self._best(side, sd, p[0], game, vals, final=True, buttons=p[1], need=0.4)
            if found is None:
                return
            att = (p[0],) + found
        t, row, states, full, mir = att
        extra = _n(vals.get("_pmode" + ("" if side == "p1" else "_p2"))) == 1
        if extra:
            h = _n(vals.get("health" if side == "p1" else "health_p2"))
            sdm = h is not None and h <= RED_HEALTH               # Extra: MAX and the health in the red / MAX et vie rouge
        else:
            # in MAX: an SDM; in 2002 only when it took a stock, a desperation move in MAX being free there (1.33 test 50)
            # en MAX : un SDM ; dans 2002 seulement s'il a pris un stock, un coup désespéré en MAX y étant gratuit
            sdm = sd.max_on is not None and (took or not free)
        word = "SDM !" if sdm else "DM !"
        sd.result = (now, row, word, GOLD if sdm else CREAM, ["ok"] * len(states), mir)
        sd.res_max = sd.max_on is not None
        sd.spent_t = now                                          # only a move told: the stock of MAX is not one (2002, its
        # flag a moment after B+C, 1.33 test 50) / seulement un coup dit : le stock du MAX n'en est pas un
        sd.attempt = None
        if sdm or extra or (free and sd.max_on is not None):
            sd.max_on = None                                      # an SDM ends MAX, Extra's is used, and in 2002 a desperation
                                                                  # move too / le MAX fini, et dans 2002 par un coup aussi
        self._log_try(side, vals, None, row, states, word.rstrip(" !"))

    def _max_on(self, side, sd, now, vals):
        """MAX in Advanced. / Le MAX en Advanced."""
        tag, suf = side.upper(), "" if side == "p1" else "_p2"
        sd.max_on, sd.max_seen, sd.max_extra = now, False, False
        sd.max_low, sd.max_log = None, now
        pv, mv = int(_n(vals.get("_pow" + suf)) or 0), int(_n(vals.get("_maxv" + suf)) or 0)
        self.log(f"Combat, {tag} lance le MAX (jauge 0x{pv:02X}, _maxv 0x{mv:02X})",
                 f"Fight, {tag} goes MAX (gauge 0x{pv:02X}, _maxv 0x{mv:02X})")

    def _log_try(self, side, vals, game, row, states, word):
        missed = [i + 1 for i, s in enumerate(states) if s == "miss"]
        self.log(f"Combat, {side.upper()} {word}, ligne {row + 1}" + (f", étape(s) manquée(s) {missed}" if missed else ""),
                 f"Fight, {side.upper()} {word}, row {row + 1}" + (f", step(s) missed {missed}" if missed else ""))

    def _best(self, side, sd, now, game, vals, final, buttons=None, need=NEAR):
        """The desperation move the stick is doing: the most steps done, in order, either way round (the fighter can
        face both ways). / Le coup que fait le stick : le plus d'étapes faites, dans l'ordre, dans un sens ou l'autre."""
        rows = self.rows(game, vals.get(side + "_char"))
        if not rows:
            return None
        start = now - WINDOW
        seq = []
        last_t = None
        for t, d in sd.dirs:
            if t < start or t > now + 1e-6:
                continue
            if last_t is not None and seq and seq[-1] == 5 and t - last_t > PAUSE:
                seq = []                                          # a long rest: a new motion / un long repos
            seq.append(d)
            last_t = t
        if not final and sd.dirs and sd.dirs[-1][1] == 5 and now - sd.dirs[-1][0] > PAUSE:
            return None                                           # at rest for a while / au repos depuis un moment
        seq = [d for d in seq if d != 5]
        if len(seq) < 2:
            return None
        best = None
        for k, (nm, cmd, btn) in enumerate(rows):
            if final and not (buttons & set(CLASS.get(btn, btn))):
                continue
            for mir in (False, True):
                c = [MIRROR[x] for x in cmd] if mir else cmd
                hit = lcs(c, seq)
                score = sum(hit) / len(c)
                pref = (score, mir == (side == "p2"))             # facing the other one first / tourné vers l'autre d'abord
                if best is None or pref > best[0]:
                    best = (pref, k, hit, mir)
        if best is None:
            return None
        (score, _), k, hit, mir = best
        if final:
            # a command of four steps or fewer (Joe's 2369 in 2002): RATÉ would come with every special move of three
            # steps (his Slash Kick 41236, Seb's game, 1.33 test 50), so it needs all its steps / une commande de quatre
            # étapes ou moins : RATÉ viendrait avec chaque coup spécial de trois étapes, il lui faut toutes ses étapes
            if score < (need if need < NEAR or len(rows[k][1]) > 4 else 1.0):
                return None
            return k, ["ok" if h else "miss" for h in hit], all(hit), mir
        if score < 0.34:                                          # live: the steps done so far, nothing crossed
            return None                                           # en direct : les étapes faites, rien de barré
        return k, ["ok" if h else "dim" for h in hit], mir

    # ------------------------------------------------------------------ state for the drawing
    def available(self, side, vals, health):
        """A desperation move can come out: a stock or MAX (Advanced), the gauge full or the health in the red (Extra).
        / Un coup désespéré peut sortir."""
        sd = self.sides[side]
        suf = "" if side == "p1" else "_p2"
        if sd.max_on is not None:
            return True
        if _n(vals.get("_pmode" + suf)) == 1:                     # Extra
            pow_ = _n(vals.get("_pow" + suf))
            return (pow_ is not None and pow_ >= self.pow_full) or (health is not None and 0 < health <= RED_HEALTH)
        stock = _stock(vals, suf)
        return stock is not None and stock >= 1

    def showing(self, side, now):
        """RATÉ, DM ! or SDM ! still shown: its row stays, the stock gone or not. / Le mot est encore affiché."""
        r = self.sides[side].result
        return r is not None and now - r[0] < SHOW

    def row_states(self, side, k, n, now):
        """The look of a row: ('ok'/'miss'/'dim' per step, tag, tag colour, mirrored). / L'aspect d'une ligne."""
        sd = self.sides[side]
        r = sd.result
        if r is not None and now - r[0] < SHOW and r[1] == k:
            return r[4], r[2], r[3], r[5]
        a = sd.attempt
        if a is not None and a[1] == k:
            return [s if s == "ok" else "dim" for s in a[2]], None, None, a[4]
        if sd.live is not None and sd.live[0] == k:
            return sd.live[1], None, None, sd.live[2]
        return ["dim"] * n, None, None, side == "p2"


# ---------------------------------------------------------------------- drawing
def _icon(moves, key, make):
    s = moves.icons.get(key)
    if s is None:
        if len(moves.icons) > 400:
            moves.icons.clear()
        s = moves.icons[key] = make()
    return s


def arrow(hd, surf, cx, cy, r, d, col, alpha=255, moves=None):
    """A direction of the stick: a white arrow in a dark disc, its ring coloured. / Une flèche dans un disque sombre."""
    pg = hd.pg
    c = r + 2

    def make():
        dx, dy = VEC[d]
        a = math.atan2(dy, dx)
        tmp = pg.Surface((2 * r + 4, 2 * r + 4), pg.SRCALPHA)
        pg.draw.circle(tmp, (16, 20, 34, 235), (c, c), r)
        pg.draw.circle(tmp, (*col, 255), (c, c), r, max(2, hd.S(2)))
        L, w, hw, hl = r * 0.62, r * 0.20, r * 0.42, r * 0.48
        ca, sa = math.cos(a), math.sin(a)

        def P(u, v):
            return (c + u * ca - v * sa, c + u * sa + v * ca)
        pg.draw.polygon(tmp, (*WHITE, 255), [P(-L, -w), P(L - hl, -w), P(L - hl, -hw), P(L, 0), P(L - hl, hw), P(L - hl, w),
                                             P(-L, w)])
        return tmp
    tmp = _icon(moves, ("a", d, col, r), make) if moves is not None else make()
    tmp.set_alpha(alpha)
    surf.blit(tmp, (int(cx - c), int(cy - c)))


def button(hd, surf, cx, cy, r, letter, names, alpha=255, moves=None):
    """A button, its Neo Geo colour, and its name in the game (LP, LK, HP, HK). / Un bouton, sa couleur, son nom."""
    pg = hd.pg
    c = r + 2
    label = str(names.get(letter, letter))

    def make():
        col = BTN_COL[letter]
        tmp = pg.Surface((2 * r + 4, 2 * r + 4), pg.SRCALPHA)
        pg.draw.circle(tmp, (*col, 255), (c, c), r)
        pg.draw.circle(tmp, (255, 255, 255, 200), (c, c), r, max(2, hd.S(2)))
        shine = tuple(int(x + (255 - x) * 0.35) for x in col)          # drawn opaque: pygame does not blend here
        pg.draw.circle(tmp, (*shine, 255), (c - r * 0.3, c - r * 0.38), r * 0.28)
        ink = (40, 30, 0) if letter == "B" else WHITE
        t = hd.text(label, "black", int(r * (1.25 if len(label) == 1 else 0.92)), ink, glow=0)
        hd.put(tmp, t, c, c + 1, "center", "middle")
        return tmp
    tmp = _icon(moves, ("b", letter, label, r), make) if moves is not None else make()
    tmp.set_alpha(alpha)
    surf.blit(tmp, (int(cx - c), int(cy - c)))


def _plate(moves, hd, w, h, edge, radius, fill=(6, 8, 18, 215)):
    def make():
        pg = hd.pg
        p = pg.Surface((w, h), pg.SRCALPHA)
        pg.draw.rect(p, fill, p.get_rect(), border_radius=radius)
        pg.draw.rect(p, (*edge, 210), p.get_rect(), max(1, hd.S(2)), border_radius=radius)
        return p
    return _icon(moves, ("p", w, h, edge, radius, fill), make)


def panel_height(hd, n):
    S = hd.S
    return S(22) + n * (S(34) if n <= 2 else S(27)) if n else S(58)


def stock_slots(stock, lost, extra, fixed=None):
    """The squares of the stocks in Advanced: 3, one more for each teammate beaten ('98); always the same number when the
    game file says so ("stock_max" in hd: 3 in '97, its screenshots, 1.33 test 49). / 3 carrés, un de plus par équipier
    battu ; toujours le même nombre quand le fichier du jeu le dit (3 dans '97)."""
    if extra or stock is None:
        return 0
    if isinstance(fixed, int) and not isinstance(fixed, bool) and fixed > 0:
        return min(5, max(int(stock), fixed))
    return min(5, max(int(stock), 3 + int(lost or 0)))


def stock_max(game):
    """The fixed number of stock squares of this game, else None. / Le nombre fixe de carrés de ce jeu, sinon None."""
    hd = (game or {}).get("hd") if isinstance(game, dict) else None
    v = hd.get("stock_max") if isinstance(hd, dict) else None
    return v if isinstance(v, int) and not isinstance(v, bool) and v > 0 else None


def badge(stock, slots, extra, maxed, red):
    """The badge says why a desperation move can come out (1.32 test 4): MAX when every stock is lit, as the game says it,
    MAX ACTIVÉ for the MAX of A+B+C (Seb, test 8). / La pastille dit pourquoi un coup peut sortir : MAX quand tous les
    stocks sont allumés, comme le dit le jeu, MAX ACTIVÉ pour le MAX de A+B+C. Returns (word, colour, ink)."""
    if maxed and red:
        return "MAX + VIE ROUGE", GOLD, (40, 24, 0)
    if maxed and not extra:
        return tr("MAX ACTIVÉ", "MAX ON"), GOLD, (40, 24, 0)
    if maxed or (slots and stock >= slots):
        return "MAX", GOLD, (40, 24, 0)
    if red:
        return "VIE ROUGE", (230, 50, 40), WHITE
    if extra:
        return "EXTRA", CREAM, (10, 14, 28)
    if stock is not None:
        return f"{int(stock)} STOCK" + ("S" if stock > 1 else ""), CREAM, (10, 14, 28)
    return None, None, None


def draw_panel(hd, screen, moves, side, vals, game, name, x0, x1, y0, now, lost, health):
    """The panel of a player under his name, as in the mockup Seb chose (B): the badge (STOCK, EXTRA, MAX), the gauge
    as the game shows it, and the desperation moves when one can come out, their arrows facing the other fighter.
    / Le panneau d'un joueur sous son nom, comme la maquette B : la pastille, la jauge comme dans le jeu, et les coups
    désespérés quand l'un d'eux peut sortir, leurs flèches tournées vers l'autre combattant."""
    pg, S = hd.pg, hd.S
    sd = moves.sides[side]
    suf = "" if side == "p1" else "_p2"
    rows = moves.rows(game, name)
    extra = _n(vals.get("_pmode" + suf)) == 1
    pow_ = _n(vals.get("_pow" + suf))
    stock = _stock(vals, suf)
    avail = bool(rows) and (moves.available(side, vals, health) or moves.showing(side, now))
    pfull = full_pow(game)
    maxed = sd.max_on is not None or (extra and (pow_ or 0) >= pfull)
    n = len(rows) if avail else 0
    gap = S(34) if n <= 2 else S(27)
    r = S(15) if n <= 2 else S(12)
    h = panel_height(hd, n)
    red = extra and health is not None and 0 < health <= RED_HEALTH  # Extra: the life flashing red / la vie en rouge
    edge = GOLD if maxed else (230, 60, 40) if red else (120, 90, 40)
    screen.blit(_plate(moves, hd, int(x1 - x0), int(h), edge, S(18)), (int(x0), int(y0)))
    fixed = stock_max(game)
    slots = stock_slots(stock, lost, extra, fixed)
    word, bcol, ink = badge(stock, None if fixed else slots, extra, maxed, red)   # '97 says no MAX at three stocks
    if word:
        t = hd.text(word, "black", S(20), ink, glow=0)
        bw, bh = int(t["w"] + S(20)), S(26)
        b = _plate(moves, hd, bw, bh, bcol, bh // 2, fill=(*bcol, 255))
        screen.blit(b, (int(x0 + S(14)), int(y0 - bh / 2)))
        hd.put(screen, t, x0 + S(14) + bw / 2, y0, "center", "middle")
    # the gauge as the game shows it: the bar, then a square per stock / la jauge comme dans le jeu
    gy = y0 + S(38) if n else y0 + S(33)
    fill = max(0.0, min(1.0, (pow_ or 0) / pfull))
    mv = _n(vals.get("_maxv" + suf))
    if maxed and not extra and mv is not None:                    # MAX: its timer in the bar, as the game shows it
        fill = max(0.0, min(1.0, mv / maxv_full(game)))           # le MAX : son chrono dans la barre, comme le jeu
    gbw, gbh = (S(150) if extra and not n else S(72)), S(18)    # Extra has no squares: a longer bar / une barre plus longue
    q = S(22)
    gx = x0 + S(18)
    pg.draw.rect(screen, (24, 26, 40), (gx, gy - gbh / 2, gbw, gbh), border_radius=S(3))
    fw = int(gbw * fill)
    if fw > 0:
        col = GOLD if maxed else (255, 110, 30)
        pg.draw.rect(screen, col, (gx, gy - gbh / 2, fw, gbh), border_radius=S(3))
        for k in range(1, 6):                                     # the game's segments / les segments du jeu
            sx = gx + k * gbw / 6
            if sx < gx + fw:
                pg.draw.line(screen, (150, 110, 40) if maxed else (120, 40, 10), (sx, gy - gbh / 2 + 2), (sx, gy + gbh / 2 - 2), 1)
    pg.draw.rect(screen, (150, 170, 210), (gx, gy - gbh / 2, gbw, gbh), max(1, S(2)), border_radius=S(3))
    x = gx + gbw + S(6)
    for k in range(slots):
        rc = pg.Rect(int(x), int(gy - q / 2), q, q)
        if k < stock:
            pg.draw.rect(screen, (60, 220, 70), rc, border_radius=S(2))
            pg.draw.rect(screen, (200, 255, 190), (rc.x + S(4), rc.y + S(4), S(7), S(5)))
        else:
            pg.draw.rect(screen, (14, 16, 26), rc, border_radius=S(2))
        pg.draw.rect(screen, (150, 170, 210), rc, max(1, S(2)), border_radius=S(2))
        x += q + S(5)
    gauge_end = x
    names = (game or {}).get("buttons") if isinstance(game, dict) else None
    names = names if isinstance(names, dict) else {}
    if not n:                                                     # no desperation move now: the inputs pressed, as
        if extra and pow_ is not None and not maxed:              # training mode shows them. Extra: how full, and the
            pct = min(100, int(round(100 * fill)))               # rule (Seb, test 4) / Extra : le remplissage, la règle
            x = gauge_end + S(4)
            x += hd.put(screen, hd.text(f"{pct} %", "xbold", S(19), CREAM, glow=0), x, gy, "left", "middle") + S(16)
            x += hd.put(screen, hd.text(tr("SUPER À 100 %", "SUPER AT 100 %"), "xbold", S(15), GREY, glow=0), x, gy, "left",
                        "middle")
            gauge_end = x
        draw_inputs(hd, screen, moves, sd, names, gauge_end + S(26), x1 - S(16), gy, now)
        return h
    lines = []
    for k, (nm, cmd, btn) in enumerate(rows):
        states, tag, tcol, mir = moves.row_states(side, k, len(cmd), now)
        steps = [MIRROR[c] for c in cmd] if mir else list(cmd)    # P2 on the right faces left / P2 regarde à gauche
        btns = [b for b in CLASS.get(btn, btn) if b in BTN_COL]
        lines.append((nm, steps, states, tag, tcol, btns))
    # the commands from where the mockup has them, the arrows smaller when a long one would leave no room for its word
    # les commandes là où la maquette les met, les flèches plus petites quand une longue ne laisserait pas de place
    tagw = max(hd.text_width(w, "black", S(21)) for w in ("RATÉ", "DM !", "SDM !")) + S(8)
    cx0 = x0 + S(352)

    def width(r, sp):
        return max(len(st) * (2 * r + sp) + r * 1.6 + S(6) + len(bt) * (2 * r + sp) for _, st, _, _, _, bt in lines)
    sp = S(5)                                                     # the room between two arrows / l'écart entre deux flèches
    while r > S(11) and cx0 + width(r, sp) + tagw > x1 - S(12):
        r -= 1
    if cx0 + width(r, sp) + tagw > x1 - S(12):                    # two motions in a row (hcb hcb): closer together
        sp = max(1, S(2))                                         # deux gestes à la suite : plus serrées
        while r > S(8) and cx0 + width(r, sp) + tagw > x1 - S(12):
            r -= 1
    slot, plus = 2 * r + sp, r * 1.6 + S(6)
    # the names in one size, between the gauge and the commands / les noms d'une même taille, entre la jauge et les commandes
    room = cx0 - S(12) - (gauge_end + S(10))
    nsize = min([hd.fit_size(nm, "xbold", S(17), room, S(11)) for nm, *_ in lines if nm] or [S(17)])
    for k, (nm, steps, states, tag, tcol, btns) in enumerate(lines):
        y = y0 + S(28) + k * gap
        lit = tag is not None or any(st == "ok" for st in states)
        ncol = (GOLD if maxed else CREAM) if lit else GREY
        if nm:
            hd.put(screen, hd.text(nm, "xbold", nsize, ncol, glow=0), cx0 - S(12), y, "right", "middle")
        x = cx0
        for d, st in zip(steps, list(states) + ["dim"] * (len(steps) - len(states))):
            cx = x + r
            col = {"ok": GOLD, "miss": MISS}.get(st, (200, 205, 225) if maxed else (170, 176, 196))
            arrow(hd, screen, cx, y, r, d, col, alpha=255 if st in ("ok", "miss") else 140, moves=moves)
            if st == "miss":                                      # the step not done: a red cross / une croix rouge
                dd = r * 0.75
                pg.draw.line(screen, MISS, (cx - dd, y - dd), (cx + dd, y + dd), max(2, S(4)))
                pg.draw.line(screen, MISS, (cx - dd, y + dd), (cx + dd, y - dd), max(2, S(4)))
            x += slot
        hd.put(screen, hd.text("+", "black", max(S(12), int(r * 1.45)), CREAM if lit else GREY, glow=0), x + r * 0.6, y,
               "center", "middle")
        x += plus
        for b in btns:
            button(hd, screen, x + r, y, r, b, names, alpha=255 if lit else 130, moves=moves)
            x += slot
        if tag:
            hd.put(screen, hd.text(tag, "black", S(21), tcol, glow=0.4), x + S(6), y, "left", "middle")
    return h


def draw_inputs(hd, screen, moves, sd, names, xa, xb, y, now):
    """The inputs of a player as training mode shows them (Seb, 1.32 test 3): each direction of the stick and the buttons
    pressed with it, the newest on the right and lit, the older ones fading, all gone a moment after the last one.
    / Les touches d'un joueur comme le mode entraînement : chaque direction et les boutons appuyés avec, la plus récente à
    droite et éclairée, les plus anciennes plus pâles, le tout parti un moment après la dernière."""
    S = hd.S
    groups = sd.groups
    if not groups:
        return
    idle = now - groups[-1][0]
    fade = 1.0 if idle < INPUT_KEEP else max(0.0, 1.0 - (idle - INPUT_KEEP) / 0.6)
    if fade <= 0:
        return
    r, sp, gg = S(14), S(4), S(12)
    slot = 2 * r + sp
    chosen, room = [], xb - xa
    for g in reversed(groups):                                    # the newest that fit / les plus récentes qui tiennent
        w = ((1 if g[1] else 0) + len(g[2])) * slot - sp
        if w <= 0:
            continue
        need = w + (gg if chosen else 0)
        if need > room:
            break
        chosen.append((g, w))
        room -= need
    chosen.reverse()
    x = xb - sum(w for _, w in chosen) - gg * max(0, len(chosen) - 1)
    for i, ((t, d, btns), w) in enumerate(chosen):
        age = len(chosen) - 1 - i
        alpha = int((255 if age == 0 else max(110, 230 - 16 * age)) * fade)
        if age == 0 and now - t < 0.5:                            # the last one lit a moment / la dernière éclairée
            glow = _plate(moves, hd, int(w + S(14)), int(2 * r + S(12)), GOLD, r + S(6), fill=(255, 214, 120, 60))
            glow.set_alpha(int(255 * (1 - (now - t) / 0.5)))
            screen.blit(glow, (int(x - S(7)), int(y - r - S(6))))
        cx = x + r
        if d:
            arrow(hd, screen, cx, y, r, d, GOLD if age == 0 else (150, 160, 190), alpha=alpha, moves=moves)
            cx += slot
        for b in btns:
            if b in BTN_COL:
                button(hd, screen, cx, y, r, b, names, alpha=alpha, moves=moves)
                cx += slot
        x += w + gg


def draw_wins(hd, screen, moves, w1, w2, cx, cy, now, pops=None):
    """Against a human, the matches each one won, P1 on the left and P2 on the right, under the credits (Seb, as in
    Puzzle Bobble). / Contre un humain, les matchs gagnés par chacun, sous les crédits."""
    S = hd.S
    w, h = S(330), S(84)
    screen.blit(_plate(moves, hd, w, h, GOLD, S(20), fill=(6, 8, 18, 230)), (int(cx - w / 2), int(cy - h / 2)))
    hd.put(screen, hd.text(tr("VICTOIRES", "WINS"), "xbold", S(22), CREAM, glow=0), cx, cy - S(18), "center", "middle")
    hd.put(screen, hd.text("P1", "black", S(26), AMBER, glow=0), cx - S(54), cy + S(16), "center", "middle")
    hd.put(screen, hd.text("P2", "black", S(26), AMBER, glow=0), cx + S(54), cy + S(16), "center", "middle")
    for side, v, x in (("p1", w1, cx - S(122)), ("p2", w2, cx + S(122))):
        k = 0.0
        if pops and pops.get(side) is not None:
            dt = now - pops[side]
            if 0 <= dt < 0.6:
                k = 1 - dt / 0.6
        hd.put_number(screen, str(int(v)), "black", S(64), GOLD, x, cy + S(2), "center", "middle", scale=1 + 0.35 * k,
                      glow=0.6 + 0.4 * k)
    hd.pg.draw.line(screen, (120, 90, 40), (cx, cy + S(4)), (cx, cy + S(28)), max(1, S(2)))
