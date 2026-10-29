"""The coin buttons of the cabinet, read straight from the controllers (coin_buttons.bat).

RetroArch does not tell when a coin goes in, nor through which slot. An MVS keeps that in the backup memory of the cabinet,
which the FinalBurn Neo core does not share, and its BIOS leaves no trace of a second coin put in during a game. So
ArcadeDMD reads the two coin buttons itself, on the controllers or on the keyboard, at the same time as RetroArch and
without taking them from it. coin_buttons.bat shows it once which buttons they are, and they go into config.json
("coin_buttons"). Each coin is then seen with its side, during a game too. Windows only: the controllers
are read through winmm and the keys through GetAsyncKeyState, both work while another window has the focus.

Les boutons des pièces de la borne, lus directement sur les manettes (coin_buttons.bat).

RetroArch ne dit pas quand une pièce entre, ni par quel monnayeur. La MVS le garde dans la mémoire de sauvegarde de la
borne, que le cœur FinalBurn Neo ne partage pas, et son BIOS ne laisse aucune trace d'une deuxième pièce mise en pleine
partie. ArcadeDMD lit donc lui-même les deux boutons des pièces, sur les manettes ou le clavier, en même temps que
RetroArch et sans les lui prendre. coin_buttons.bat lui montre une fois quels boutons c'est, ils vont dans config.json.
Chaque pièce est alors vue avec son côté, en pleine partie aussi. Windows seulement.
"""

import collections
import sys
import threading
import time

from .i18n import tr

LEFT, RIGHT = 0, 1
SIDES = (("left", LEFT), ("right", RIGHT))
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


def mvs_rates(cfg):
    """Credits given by a coin on a Neo Geo MVS, left slot then right slot. The MVS gives 2 for a coin in its second slot
    when nothing was changed in its settings ("mvs_credits" in coin_buttons). / Crédits par pièce d'une MVS."""
    cb = cfg.get("coin_buttons") if isinstance(cfg.get("coin_buttons"), dict) else {}
    r = cb.get("mvs_credits")
    if isinstance(r, list) and len(r) == 2 and all(isinstance(x, int) and 1 <= x <= 9 for x in r):
        return (r[0], r[1])
    return (1, 2)


class CoinButtons:
    """Watches the two coin buttons. poll() gives the side of each coin put in since the last call (0 left, 1 right)."""

    def __init__(self, cfg, log=None, source=None, thread=True):
        spec = cfg.get("coin_buttons") if isinstance(cfg.get("coin_buttons"), dict) else {}
        self.inputs = {}
        for name, side in SIDES:
            inp = parse(spec.get(name))
            if inp is not None:
                self.inputs[side] = inp
        self.source = source
        self.log = log
        self.q = collections.deque()
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
        if self.thread is None and self.source is not None and self.inputs:
            self.scan(time.monotonic() if now is None else now)
        out = []
        while self.q:
            out.append(self.q.popleft()[0])
        return out

    def close(self):
        self.stop_ev.set()


# ------------------------------------------------------------------ coin_buttons.bat
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
    """coin_buttons.bat: asks for the left coin button, then the right one, and writes them into config.json."""
    from .setup_tools import load_config_file, save_config_file
    out(tr("Boutons des pièces", "Coin buttons"))
    out("")
    src = source if source is not None else backend()
    if src is None:
        out(tr("Cette commande ne marche que sous Windows.", "This command only works on Windows."))
        return 1
    out(tr("ArcadeDMD va lire lui-même tes deux boutons de pièce. Il verra chaque pièce et son côté, même en pleine partie.",
           "ArcadeDMD is going to read your two coin buttons itself. It will see each coin and its side, during a game too."))
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
    cfg = load_config_file(root)
    cb = cfg.get("coin_buttons") if isinstance(cfg.get("coin_buttons"), dict) else {}
    cb["left"] = spec_of(left)
    cb["right"] = spec_of(right) if right is not None else None
    cfg["coin_buttons"] = cb
    save_config_file(root, cfg)
    out(tr("C'est enregistré dans config.json.", "Saved in config.json."))
    if check > 0:
        out("")
        out(tr(f"Pour vérifier, appuie encore sur l'un ou l'autre pendant {int(check)} secondes.",
               f"To check, press either of them again for {int(check)} seconds."))
        cbs = CoinButtons({"coin_buttons": cb}, None, src, thread=False)
        cbs.poll(clock())                                # the button just learned may still be held / encore appuyé
        end = clock() + check
        while clock() < end:
            for side in cbs.poll(clock()):
                out("   " + tr(f"pièce à {side_word(side)}", f"coin on the {side_word(side)}"))
            sleep(poll)
    out("")
    out(tr("Terminé. Si ArcadeDMD tourne, il reprend tout seul ce réglage.",
           "Done. If ArcadeDMD is running, it picks up this setting by itself."))
    return 0
