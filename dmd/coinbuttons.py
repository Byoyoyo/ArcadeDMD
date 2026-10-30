"""The coin buttons of the cabinet, read straight from the controllers (coin_buttons.bat).

RetroArch does not tell when a coin goes in, nor through which slot. An MVS keeps that in the backup memory of the cabinet,
which the FinalBurn Neo core does not share, and its BIOS leaves no trace of a second coin put in during a game. So
ArcadeDMD reads the two coin buttons itself, on the controllers or on the keyboard, at the same time as RetroArch and
without taking them from it. coin_buttons.bat shows it once which buttons they are, and they go into config.json
("coin_buttons"). Each coin is then seen with its side, during a game too. The two START buttons can be shown too
("start1", "start2"): a game that does not give its credits then sees a player begin as soon as he presses START with a
credit, on the select screen. Windows only: the controllers are read through winmm and the keys through
GetAsyncKeyState, both work while another window has the focus.

Les boutons des pièces de la borne, lus directement sur les manettes (coin_buttons.bat).

RetroArch ne dit pas quand une pièce entre, ni par quel monnayeur. La MVS le garde dans la mémoire de sauvegarde de la
borne, que le cœur FinalBurn Neo ne partage pas, et son BIOS ne laisse aucune trace d'une deuxième pièce mise en pleine
partie. ArcadeDMD lit donc lui-même les deux boutons des pièces, sur les manettes ou le clavier, en même temps que
RetroArch et sans les lui prendre. coin_buttons.bat lui montre une fois quels boutons c'est, ils vont dans config.json.
Chaque pièce est alors vue avec son côté, en pleine partie aussi. Les deux boutons START aussi (« start1 », « start2 ») :
un jeu qui ne donne pas ses crédits voit alors un joueur commencer dès qu'il appuie sur START avec un crédit, sur l'écran
de sélection. Windows seulement.
"""

import collections
import sys
import threading
import time

from .i18n import tr

LEFT, RIGHT = 0, 1
SIDES = (("left", LEFT), ("right", RIGHT))
STARTS = (("start1", 0), ("start2", 1))   # START of player 1 and of player 2 / START du joueur 1 et du joueur 2
REFRACTORY = 0.15            # a button that bounces makes one coin / un bouton qui rebondit fait une seule pièce
AWAY = 3.0                   # a controller that is not there is tried again after that / manette absente
# keys looked at by coin_buttons.bat: not the mouse buttons, nor the Shift, Ctrl and Alt that also come as left or right
# touches regardées : ni les boutons de la souris, ni Maj, Ctrl et Alt qui arrivent aussi en version gauche ou droite
KEYS = [vk for vk in range(0x08, 0xFF) if vk not in (0x10, 0x11, 0x12, 0x5B, 0x5C, 0xFF)]
KEY_NAMES = {0x08: ("Retour arrière", "Backspace"), 0x09: ("Tab", "Tab"), 0x0D: ("Entrée", "Enter"),
             0x1B: ("Échap", "Esc"), 0x20: ("Espace", "Space"), 0x25: ("flèche gauche", "Left arrow"),
             0x26: ("flèche haut", "Up arrow"), 0x27: ("flèche droite", "Right arrow"), 0x28: ("flèche bas", "Down arrow"),
             0x2D: ("Inser", "Insert"), 0x2E: ("Suppr", "Delete"), 0x24: ("Début", "Home"), 0x23: ("Fin", "End"),
             0x21: ("Page haut", "Page up"), 0x22: ("Page bas", "Page down"), 0xA0: ("Maj gauche", "Left Shift"),
             0xA1: ("Maj droite", "Right Shift"), 0xA2: ("Ctrl gauche", "Left Ctrl"), 0xA3: ("Ctrl droite", "Right Ctrl"),
             0xA4: ("Alt gauche", "Left Alt"), 0xA5: ("Alt droite", "Right Alt")}


class WinInput:
    """The controllers through winmm (16 of them, 32 buttons each) and the keys through GetAsyncKeyState.
    / Les manettes par winmm et les touches par GetAsyncKeyState, lues même quand une autre fenêtre a la main."""

    def __init__(self):
        import ctypes
        from ctypes import wintypes

        class JOYINFOEX(ctypes.Structure):
            _fields_ = [(n, wintypes.DWORD) for n in ("dwSize", "dwFlags", "dwXpos", "dwYpos", "dwZpos", "dwRpos",
                                                       "dwUpos", "dwVpos", "dwButtons", "dwButtonNumber", "dwPOV",
                                                       "dwReserved1", "dwReserved2")]
        self.ct = ctypes
        self.winmm = ctypes.WinDLL("winmm")
        self.winmm.joyGetPosEx.argtypes = [wintypes.UINT, ctypes.POINTER(JOYINFOEX)]
        self.winmm.joyGetPosEx.restype = wintypes.UINT
        self.user32 = ctypes.WinDLL("user32")
        self.user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
        self.user32.GetAsyncKeyState.restype = ctypes.c_short
        self.info = JOYINFOEX()
        self.info.dwSize = ctypes.sizeof(JOYINFOEX)

    def joystick(self, i):
        """The buttons held on controller i, one bit each, or None when it is not there."""
        self.info.dwFlags = 0x80                       # JOY_RETURNBUTTONS
        if self.winmm.joyGetPosEx(i, self.ct.byref(self.info)) != 0:
            return None
        return int(self.info.dwButtons)

    def key(self, vk):
        return bool(self.user32.GetAsyncKeyState(vk) & 0x8000)


def backend():
    """The way to read the controllers here, or None (Windows only). / None hors de Windows."""
    if sys.platform != "win32":
        return None
    try:
        return WinInput()
    except (OSError, AttributeError):
        return None


def parse(spec):
    """{"joystick": 0, "button": 8} or {"key": 53} from config.json, as ("joy", 0, 8) or ("key", 53). None otherwise."""
    if not isinstance(spec, dict):
        return None
    try:
        if "joystick" in spec and "button" in spec:
            j, b = int(spec["joystick"]), int(spec["button"])
            return ("joy", j, b) if 0 <= j < 16 and 0 <= b < 32 else None
        if "key" in spec:
            k = int(spec["key"])
            return ("key", k) if 0 < k < 256 else None
    except (TypeError, ValueError):
        pass
    return None


def spec_of(inp):
    return {"joystick": inp[1], "button": inp[2]} if inp[0] == "joy" else {"key": inp[1]}


def describe(inp):
    """controller 1, button 9 (counted from 1, like in the Windows game controllers panel) or key 5."""
    if inp is None:
        return tr("aucun", "none")
    if inp[0] == "joy":
        return tr(f"manette {inp[1] + 1}, bouton {inp[2] + 1}", f"controller {inp[1] + 1}, button {inp[2] + 1}")
    vk = inp[1]
    if 0x30 <= vk <= 0x39 or 0x41 <= vk <= 0x5A:
        name = chr(vk)
    elif 0x60 <= vk <= 0x69:
        name = tr(f"{vk - 0x60} du pavé numérique", f"keypad {vk - 0x60}")
    elif 0x70 <= vk <= 0x87:
        name = f"F{vk - 0x6F}"
    elif vk in KEY_NAMES:
        name = tr(*KEY_NAMES[vk])
    else:
        name = str(vk)
    return tr(f"touche {name}", f"key {name}")


def side_word(side):
    return tr("gauche", "left") if side == LEFT else tr("droite", "right")


def start_word(player):
    return tr(f"START du joueur {player + 1}", f"player {player + 1}'s START")


def mvs_rates(cfg):
    """Credits given by a coin on a Neo Geo MVS, left slot then right slot. The MVS gives 2 for a coin in its second slot
    when nothing was changed in its settings ("mvs_credits" in coin_buttons). / Crédits par pièce d'une MVS."""
    cb = cfg.get("coin_buttons") if isinstance(cfg.get("coin_buttons"), dict) else {}
    r = cb.get("mvs_credits")
    if isinstance(r, list) and len(r) == 2 and all(isinstance(x, int) and 1 <= x <= 9 for x in r):
        return (r[0], r[1])
    return (1, 2)


class CoinButtons:
    """Watches the two coin buttons, and the two START buttons when they are known. poll() gives the side of each coin put
    in since the last call (0 left, 1 right), poll_starts() the player of each START pressed (0 player 1, 1 player 2).
    / Surveille les boutons des pièces, et les deux START quand ils sont connus."""

    def __init__(self, cfg, log=None, source=None, thread=True):
        spec = cfg.get("coin_buttons") if isinstance(cfg.get("coin_buttons"), dict) else {}
        self.inputs = {}
        for name, side in SIDES:
            inp = parse(spec.get(name))
            if inp is not None:
                self.inputs[side] = inp
        # START buttons, kept apart from the coins (keys "s0", "s1" in held and last) / les START, à part des pièces
        self.starts = {}
        for name, player in STARTS:
            inp = parse(spec.get(name))
            if inp is not None and inp not in self.inputs.values():
                self.starts[player] = inp
        self.source = source
        self.log = log
        self.q = collections.deque()
        self.sq = collections.deque()
        self.held = {}
        self.last = {}
        self.away = {}                    # controller not there: when to try again / manette absente : quand réessayer
        self.failed = False
        self.stop_ev = threading.Event()
        self.thread = None
        if thread and self.inputs and source is not None:
            self.thread = threading.Thread(target=self._run, name="coin-buttons", daemon=True)
            self.thread.start()

    @classmethod
    def from_config(cls, cfg, log, source=None):
        """None when no button is set (coin_buttons.bat) or when the controllers cannot be read here."""
        spec = cfg.get("coin_buttons") if isinstance(cfg.get("coin_buttons"), dict) else {}
        found = {side: parse(spec.get(name)) for name, side in SIDES}
        if not any(found.values()):
            return None
        src = source or backend()
        if src is None:
            log(tr("boutons des pièces : les manettes ne se lisent que sous Windows, réglage ignoré",
                   "coin buttons: the controllers can only be read on Windows, setting ignored"))
            return None
        log(tr(f"boutons des pièces : à gauche ({describe(found[LEFT])}), à droite ({describe(found[RIGHT])})",
               f"coin buttons: on the left ({describe(found[LEFT])}), on the right ({describe(found[RIGHT])})"))
        starts = [parse(spec.get(name)) for name, _ in STARTS]
        if any(starts):
            log(tr(f"boutons START : joueur 1 ({describe(starts[0])}), joueur 2 ({describe(starts[1])})",
                   f"START buttons: player 1 ({describe(starts[0])}), player 2 ({describe(starts[1])})"))
        return cls(cfg, log, src)

    def down(self, inp, now, cache):
        if inp[0] == "key":
            return self.source.key(inp[1])
        j = inp[1]
        if j not in cache:
            if now < self.away.get(j, 0.0):
                cache[j] = None
            else:
                cache[j] = self.source.joystick(j)
                if cache[j] is None:
                    self.away[j] = now + AWAY            # unplugged, or not this number / débranchée
        b = cache[j]
        return b is not None and bool(b >> inp[2] & 1)

    def scan(self, now):
        cache = {}                                       # each controller read once / chaque manette lue une fois
        for side, inp in self.inputs.items():
            d = self.down(inp, now, cache)
            if d and not self.held.get(side) and now - self.last.get(side, -9.0) >= REFRACTORY:
                self.q.append((side, now))
                self.last[side] = now
            self.held[side] = d
        for player, inp in self.starts.items():
            k = f"s{player}"
            d = self.down(inp, now, cache)
            if d and not self.held.get(k) and now - self.last.get(k, -9.0) >= REFRACTORY:
                self.sq.append((player, now))
                self.last[k] = now
            self.held[k] = d

    def _run(self):
        while not self.stop_ev.is_set():
            try:
                self.scan(time.monotonic())
            except Exception as e:                       # the engine goes on / le moteur continue
                if not self.failed and self.log is not None:
                    self.failed = True
                    self.log(tr(f"boutons des pièces : erreur {e!r}", f"coin buttons: error {e!r}"))
                self.stop_ev.wait(1.0)
            self.stop_ev.wait(0.01)

    def poll(self, now=None):
        """The sides of the coins put in since the last call. Without a thread, the buttons are read here."""
        if self.thread is None and self.source is not None and (self.inputs or self.starts):
            self.scan(time.monotonic() if now is None else now)
        out = []
        while self.q:
            out.append(self.q.popleft()[0])
        return out

    def poll_starts(self):
        """The players who pressed START since the last call (read by poll()). / Les joueurs qui ont appuyé sur START."""
        out = []
        while self.sq:
            out.append(self.sq.popleft()[0])
        return out

    def close(self):
        self.stop_ev.set()


# ------------------------------------------------------------------ coin_buttons.bat
def learn_starts(coins, out, src, wait, clock, sleep, poll):
    """The START of player 1, then of player 2, not a coin button. [] when none is pressed within wait seconds.
    / Le START du joueur 1, puis celui du joueur 2, pas un bouton des pièces."""
    starts = []
    for player in (0, 1):
        out(tr(f"Appuie maintenant sur le bouton START du joueur {player + 1}.",
               f"Now press player {player + 1}'s START button."))
        got = None
        end = clock() + wait
        while clock() < end:
            b = wait_press(src, max(0.0, end - clock()), clock, sleep, poll)
            if b is None:
                break
            if b in coins:
                out("   " + tr("C'est un bouton des pièces. Appuie sur START.", "That is a coin button. Press START."))
                continue
            if b in starts:
                out("   " + tr("C'est le START du joueur 1. Appuie sur celui du joueur 2.",
                               "That is player 1's START. Press player 2's."))
                continue
            got = b
            break
        if got is None:
            if not starts:
                out("   " + tr("Aucun bouton START vu. ArcadeDMD devinera le départ d'après ce qui bouge dans le jeu.",
                               "No START button seen. ArcadeDMD will guess the start from what moves in the game."))
            else:
                out("   " + tr("Aucun START vu pour le joueur 2. Seul celui du joueur 1 est enregistré.",
                               "No START seen for player 2. Only player 1's is saved."))
            break
        out("   " + tr(f"C'est la {describe(got)}.", f"That is {describe(got)}."))
        starts.append(got)
    return starts


def held_now(src, ids):
    """Everything held right now, on the controllers ids and the keyboard."""
    held = set()
    for j in ids:
        b = src.joystick(j)
        if b:
            held.update(("joy", j, k) for k in range(32) if b >> k & 1)
    held.update(("key", vk) for vk in KEYS if src.key(vk))
    return held


def controllers(src):
    return [j for j in range(16) if src.joystick(j) is not None]


def wait_press(src, seconds, clock, sleep, poll):
    """The first button pressed within seconds, or None. Those already held count once they are let go."""
    end = clock() + seconds
    ids = controllers(src)
    scan_at = clock() + 5.0
    base = held_now(src, ids)
    while clock() < end:
        if clock() >= scan_at:                           # a controller plugged in meanwhile / branchée entre-temps
            ids, scan_at = controllers(src), clock() + 5.0
        now = held_now(src, ids)
        base &= now
        new = sorted(now - base)
        if new:
            return new[0]
        sleep(poll)
    return None


def learn(root, out=print, source=None, wait=60.0, check=10.0, poll=0.01, clock=time.monotonic, sleep=time.sleep):
    """coin_buttons.bat: asks for the left coin button, then the right one, then the START of each player, and writes
    them into config.json. / Demande les boutons des pièces, puis les START, et les écrit dans config.json."""
    from .setup_tools import load_config_file, save_config_file
    out(tr("Boutons des pièces", "Coin buttons"))
    out("")
    src = source if source is not None else backend()
    if src is None:
        out(tr("Cette commande ne marche que sous Windows.", "This command only works on Windows."))
        return 1
    out(tr("ArcadeDMD va lire lui-même tes deux boutons de pièce et tes deux boutons START. Il verra chaque pièce et son "
           "côté, même en pleine partie, et chaque joueur qui commence.",
           "ArcadeDMD is going to read your two coin buttons and your two START buttons itself. It will see each coin "
           "and its side, during a game too, and each player who begins."))
    out(tr("RetroArch peut rester ouvert.", "RetroArch can stay open."))
    out("")
    out(tr("Appuie sur le bouton des pièces de gauche, celui du joueur 1.",
           "Press the coin button on the left, player 1's."))
    left = wait_press(src, wait, clock, sleep, poll)
    if left is None:
        out(tr(f"Aucun bouton vu en {int(wait)} secondes, rien n'a changé.",
               f"No button seen in {int(wait)} seconds, nothing changed."))
        return 1
    out("   " + tr(f"C'est la {describe(left)}.", f"That is {describe(left)}."))
    out(tr("Appuie maintenant sur le bouton des pièces de droite, celui du joueur 2.",
           "Now press the coin button on the right, player 2's."))
    right = None
    end = clock() + wait
    while clock() < end:
        got = wait_press(src, max(0.0, end - clock()), clock, sleep, poll)
        if got is None:
            break
        if got == left:
            out("   " + tr("C'est le même bouton qu'à gauche. Appuie sur celui de droite.",
                           "That is the same button as on the left. Press the one on the right."))
            continue
        right = got
        break
    if right is None:
        out("   " + tr("Aucun bouton vu à droite. Seul celui de gauche est enregistré.",
                       "No button seen on the right. Only the left one is saved."))
    else:
        out("   " + tr(f"C'est la {describe(right)}.", f"That is {describe(right)}."))
    starts = learn_starts([b for b in (left, right) if b is not None], out, src, wait, clock, sleep, poll)
    cfg = load_config_file(root)
    cb = cfg.get("coin_buttons") if isinstance(cfg.get("coin_buttons"), dict) else {}
    cb["left"] = spec_of(left)
    cb["right"] = spec_of(right) if right is not None else None
    if starts:                                           # none seen: the old ones stay / aucun vu : les anciens restent
        cb["start1"] = spec_of(starts[0])
        cb["start2"] = spec_of(starts[1]) if len(starts) > 1 else None
    cfg["coin_buttons"] = cb
    save_config_file(root, cfg)
    out(tr("C'est enregistré dans config.json.", "Saved in config.json."))
    if check > 0:
        out("")
        out(tr(f"Pour vérifier, appuie encore sur ces boutons pendant {int(check)} secondes.",
               f"To check, press these buttons again for {int(check)} seconds."))
        cbs = CoinButtons({"coin_buttons": cb}, None, src, thread=False)
        cbs.poll(clock())                                # the button just learned may still be held / encore appuyé
        cbs.poll_starts()
        end = clock() + check
        while clock() < end:
            for side in cbs.poll(clock()):
                out("   " + tr(f"pièce à {side_word(side)}", f"coin on the {side_word(side)}"))
            for player in cbs.poll_starts():
                out("   " + start_word(player))
            sleep(poll)
    out("")
    out(tr("Terminé. Si ArcadeDMD tourne, il reprend tout seul ce réglage.",
           "Done. If ArcadeDMD is running, it picks up this setting by itself."))
    return 0
