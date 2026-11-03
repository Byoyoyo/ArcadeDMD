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
RED_HEALTH = 25       # Extra: the desperation moves are free with the health this low / gratuits avec si peu de vie
FULL_POW = 0xA0       # the gauge full (MAX in Extra) / la jauge pleine


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
        self.abc_t = -99.0
        self.attempt = None          # (t, row, states, full, mirrored) a button after a motion, the game not heard yet
        self.result = None           # (t, row, text, colour, states, mirrored) RATÉ, DM !, SDM !
        self.live = None             # (row, states, mirrored) what the stick is doing now / ce que fait le stick


class Moves:
    """The panel of each player. update() at every image with the values and the input history of the engine.
    / Le panneau de chaque joueur."""

    def __init__(self, hd):
        self.hd = hd
        self.sides = {"p1": Side(), "p2": Side()}
        self.key = None
        self.icons = {}

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

    def update(self, vals, hist, now, key, game, humans):
        if key != self.key:
            self.key = key
            self.reset()
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
            self._gauge(side, sd, vals, suf, now)
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

    def _gauge(self, side, sd, vals, suf, now):
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
                self._spent(side, sd, now, vals)
        if maxv is not None and sd.maxv is not None and (maxv == 0) != (sd.maxv == 0):
            self.log(f"Combat, {tag} MAX ? _maxv 0x{int(sd.maxv):02X} -> 0x{int(maxv):02X}",
                     f"Fight, {tag} MAX? _maxv 0x{int(sd.maxv):02X} -> 0x{int(maxv):02X}")
        if mode == 1 and pow_ is not None and sd.pow is not None and sd.pow >= FULL_POW > pow_ + 0x40:
            self._spent(side, sd, now, vals)                      # Extra: the full gauge used / la jauge pleine utilisée
        if sd.max_on is not None:
            if maxv:
                sd.max_seen = True
            over = now - sd.max_on > MAX_LONG or (sd.max_seen and maxv == 0)
            if over:
                sd.max_on = None
                self.log(f"Combat, {tag} fin du MAX", f"Fight, {tag} MAX over")
        sd.stock, sd.pow, sd.mode, sd.maxv = (stock if stock is not None else sd.stock, pow_ if pow_ is not None else sd.pow,
                                              mode if mode is not None else sd.mode, maxv if maxv is not None else sd.maxv)

    def _input(self, side, sd, t, v, game, vals):
        if sd.first:
            sd.first = False
            self.log(f"Combat, {side.upper()} touches lues (0x{v:02X})", f"Fight, {side.upper()} inputs read (0x{v:02X})")
        if not sd.low and ((v & 3) == 3 or (v & 12) == 12):       # up and down at once: the byte is the other way round
            sd.low = True                                         # (0 when pressed) / haut et bas ensemble : à l'envers
            sd.dirs, sd.prev_btn = [], set()
            self.log(f"Combat, {side.upper()} touches à l'envers (0 = appuyé)", f"Fight, {side.upper()} inputs inverted (0 = pressed)")
        d = stick(v, sd.low)
        if not sd.dirs or sd.dirs[-1][1] != d:
            sd.dirs.append((t, d))
            if len(sd.dirs) > 48:
                del sd.dirs[:len(sd.dirs) - 48]
        btn = pressed(v, sd.low)
        new = btn - sd.prev_btn
        sd.prev_btn = btn
        if not new:
            return
        if {"A", "B", "C"} <= btn:
            sd.abc_t = t                                          # A+B+C: MAX asked / MAX demandé
            return
        att = self._best(side, sd, t, game, vals, final=True, buttons=new)
        if att is not None:
            sd.attempt = (t,) + att
            sd.result = None

    def _spent(self, side, sd, now, vals):
        """The game took a stock (or the full gauge in Extra): MAX after A+B+C, else the desperation move tried just
        before. A stock can also go to a guard cancel: nothing then. / Le jeu a pris un stock : le MAX après A+B+C,
        sinon le coup désespéré tenté juste avant ; un stock peut aussi partir dans une garde annulée."""
        tag = side.upper()
        att = sd.attempt
        if now - sd.abc_t < CONFIRM and (att is None or att[0] < sd.abc_t + 0.1):
            if _n(vals.get("_pmode" + ("" if side == "p1" else "_p2"))) != 1:
                sd.max_on, sd.max_seen = now, False               # A+B+C took a stock: MAX / le MAX
                self.log(f"Combat, {tag} lance le MAX", f"Fight, {tag} goes MAX")
            return
        if att is None or now - att[0] > CONFIRM + 0.6:
            return
        t, row, states, full, mir = att
        extra = _n(vals.get("_pmode" + ("" if side == "p1" else "_p2"))) == 1
        if extra:
            h = _n(vals.get("health" if side == "p1" else "health_p2"))
            sdm = h is not None and h <= RED_HEALTH               # Extra: MAX and the health in the red / MAX et vie rouge
        else:
            sdm = sd.max_on is not None
        word = "SDM !" if sdm else "DM !"
        sd.result = (now, row, word, GOLD if sdm else CREAM, ["ok"] * len(states), mir)
        sd.attempt = None
        if sdm:
            sd.max_on = None                                      # an SDM ends MAX / un SDM finit le MAX
        self._log_try(side, vals, None, row, states, word.rstrip(" !"))

    def _log_try(self, side, vals, game, row, states, word):
        missed = [i + 1 for i, s in enumerate(states) if s == "miss"]
        self.log(f"Combat, {side.upper()} {word}, ligne {row + 1}" + (f", étape(s) manquée(s) {missed}" if missed else ""),
                 f"Fight, {side.upper()} {word}, row {row + 1}" + (f", step(s) missed {missed}" if missed else ""))

    def _best(self, side, sd, now, game, vals, final, buttons=None):
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
            if score < NEAR:
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
        if _n(vals.get("_pmode" + suf)) == 1:                     # Extra
            pow_ = _n(vals.get("_pow" + suf))
            return (pow_ is not None and pow_ >= FULL_POW) or (health is not None and 0 < health <= RED_HEALTH)
        if sd.max_on is not None:
            return True
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
    return S(22) + n * (S(34) if n <= 2 else S(27)) if n else S(46)


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
    maxed = sd.max_on is not None or (extra and (pow_ or 0) >= FULL_POW)
    n = len(rows) if avail else 0
    gap = S(34) if n <= 2 else S(27)
    r = S(15) if n <= 2 else S(12)
    h = panel_height(hd, n)
    edge = GOLD if maxed else (120, 90, 40)
    screen.blit(_plate(moves, hd, int(x1 - x0), int(h), edge, S(18)), (int(x0), int(y0)))
    # the badge / la pastille
    if maxed:
        word = "MAX"
    elif extra:
        word = "EXTRA"
    elif stock is not None:
        word = f"{int(stock)} STOCK" + ("S" if stock > 1 else "")
    else:
        word = None
    if word:
        t = hd.text(word, "black", S(20), (40, 24, 0) if maxed else (10, 14, 28), glow=0)
        bw, bh = int(t["w"] + S(20)), S(26)
        b = _plate(moves, hd, bw, bh, GOLD if maxed else CREAM, bh // 2, fill=(*(GOLD if maxed else CREAM), 255))
        screen.blit(b, (int(x0 + S(14)), int(y0 - bh / 2)))
        hd.put(screen, t, x0 + S(14) + bw / 2, y0, "center", "middle")
    # the gauge as the game shows it: the bar, then a square per stock / la jauge comme dans le jeu
    gy = y0 + (S(38) if n else S(26))
    fill = max(0.0, min(1.0, (pow_ or 0) / FULL_POW))
    gbw, gbh = S(72), S(18)
    q = S(22)
    slots = 0
    if not extra and stock is not None:                           # 3 squares, one more for each teammate beaten
        slots = min(5, max(int(stock), 3 + int(lost or 0)))       # 3 carrés, un de plus par équipier battu
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
    if not n:
        return h
    names = (game or {}).get("buttons") if isinstance(game, dict) else None
    names = names if isinstance(names, dict) else {}
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

    def width(r):
        return max(len(st) * (2 * r + S(5)) + r * 1.6 + S(6) + len(bt) * (2 * r + S(5)) for _, st, _, _, _, bt in lines)
    while r > S(9) and cx0 + width(r) + tagw > x1 - S(12):
        r -= 1
    slot, plus = 2 * r + S(5), r * 1.6 + S(6)
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
