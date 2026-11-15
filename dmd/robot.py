"""The robot: the games play by themselves so that their memory is recorded (1.39).

RetroArch takes the buttons of a pad from the network (its "Network RetroPad": one UDP port per player from 55400, the
settings network_remote_enable and network_remote_enable_user_p1, a message of 20 bytes per button). The robot starts
RetroArch with a game, puts a coin, presses START, plays at random for a few minutes, closes the game and goes on with
the next one. ArcadeDMD, running beside it, records each game as it does for a game played by hand (runtime/captures),
its whole memory included while the robot runs. The robot asks RetroArch for a screenshot every ten seconds, and puts
the recording and the screenshots of each game in one file, runtime/robot/<game>.zip. Nothing of RetroArch is changed:
its settings for the robot are in a file of ArcadeDMD (runtime/robot.cfg) given on its command line.

  python arcadedmd.py robot-test          one game, two minutes: does RetroArch take the buttons the robot sends?
  python arcadedmd.py robot [MINUTES]     every game whose ROM is in the folder, MINUTES each (6 by default)

Le robot : les jeux jouent tout seuls pour que leur mémoire soit enregistrée. RetroArch accepte les boutons d'une
manette par le réseau. Le robot lance RetroArch avec un jeu, met une pièce, appuie sur START, joue au hasard quelques
minutes, ferme le jeu et passe au suivant. ArcadeDMD, lancé à côté, enregistre chaque partie comme une partie jouée à
la main, toute sa mémoire comprise tant que le robot tourne. Le robot demande une capture d'écran à RetroArch toutes
les dix secondes, et range l'enregistrement et les captures de chaque jeu dans un seul fichier, runtime/robot/<jeu>.zip.
Rien n'est changé dans RetroArch : ses réglages pour le robot sont dans un fichier d'ArcadeDMD donné sur sa ligne de
commande."""
import collections
import json
import os
import random
import re
import socket
import struct
import subprocess
import threading
import time
import traceback
import zipfile

from .i18n import tr
from .memvalues import game_values, parse_addr
from .retroarch import RetroArchClient, layout_for

JOYPAD = 1                                    # RETRO_DEVICE_JOYPAD
B, Y, SELECT, START, UP, DOWN, LEFT, RIGHT, A, X, L, R = range(12)      # RETRO_DEVICE_ID_JOYPAD_*
ACTIONS = (B, A, Y, X, L, R)
BASE_PORT = 55400
SHOT_BIG = 400_000                            # a screenshot heavier than this is made smaller / une capture plus lourde est réduite
SHOT_WIDTH = 640
SHOT_EVERY = 10.0                             # a screenshot that often during a game / une capture d'écran aussi souvent
PACE = 0.018                                  # a little slower than the images / un peu moins vite que les images
CFG = """network_remote_enable = "true"
network_remote_enable_user_p1 = "true"
network_remote_enable_user_p2 = "true"
network_remote_base_port = "%d"
network_cmd_enable = "true"
pause_nonactive = "false"
quit_press_twice = "false"
screenshot_directory = "%s"
screenshots_in_content_dir = "false"
sort_screenshots_by_content_enable = "false"
auto_screenshot_filename = "true"
notification_show_screenshot = "false"
notification_show_screenshot_flash = "0"
history_list_enable = "false"
config_save_on_exit = "false"
video_gpu_screenshot = "false"
video_fullscreen = "false"
audio_mute_enable = "true"
input_joypad_driver = "null"
"""
# screen off ("robot --unseen"): no window and no sound device, nothing of the screen is needed. RetroArch then has
# neither the screen nor the sound to keep its pace, so its loop keeps the game's own frame rate (it runs flat out
# otherwise). No screenshot there: on Windows RetroArch closes when asked for one without a video driver (1.21.0)
# / écran éteint : ni fenêtre ni son, rien de l'écran n'est nécessaire. La boucle de RetroArch tient alors elle-même la
# cadence du jeu (il tourne à fond sinon). Pas de capture d'écran là : sous Windows RetroArch se ferme quand on lui en
# demande une sans pilote vidéo
CFG_UNSEEN = """video_driver = "null"
audio_driver = "null"
vrr_runloop_enable = "true"
fastforward_ratio = "1.000000"
"""


class RemotePad:
    """The pad of one player, sent to RetroArch. RetroArch reads one message per player and per image, and on some
    systems forgets every button at an image without a message: the buttons held are said again all the time, a little
    slower than the images so that nothing queues. / La manette d'un joueur, envoyée à RetroArch. RetroArch lit un
    message par joueur et par image, et oublie parfois tous les boutons à une image sans message : les boutons tenus
    sont redits sans arrêt, un peu moins vite que les images pour que rien ne s'accumule."""

    def __init__(self, player=1, host="127.0.0.1", base=BASE_PORT):
        self.player = player
        self.addr = (host, base + player - 1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.held = set()
        self.todo = collections.deque()
        self.lock = threading.Lock()
        self.turn = 0
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _send(self, button, down):
        """struct remote_message of RetroArch (input_driver.h): port, device, index, id as int, state as uint16, 20 bytes
        with its padding. / Le message de RetroArch, 20 octets."""
        try:
            self.sock.sendto(struct.pack("<iiiiH2x", self.player - 1, JOYPAD, 0, button, 1 if down else 0), self.addr)
        except OSError:
            pass

    def _run(self):
        while not self.stop.wait(PACE):
            with self.lock:
                if self.todo:
                    button, down = self.todo.popleft()
                elif self.held:
                    order = sorted(self.held)
                    self.turn = (self.turn + 1) % len(order)
                    button, down = order[self.turn], True
                else:
                    continue
            self._send(button, down)

    def set(self, button, down):
        """Presses or releases a button. / Appuie ou relâche un bouton."""
        with self.lock:
            if (button in self.held) == bool(down):
                return
            (self.held.add if down else self.held.discard)(button)
            self.todo.append((button, bool(down)))

    def tap(self, button, hold=0.12):
        self.set(button, True)
        time.sleep(hold)
        self.set(button, False)

    def release(self):
        for b in sorted(self.held):
            self.set(b, False)

    def close(self):
        self.release()
        end = time.monotonic() + 1.0
        while self.todo and time.monotonic() < end:
            time.sleep(PACE)
        self.stop.set()
        self.thread.join(1.0)
        try:
            self.sock.close()
        except OSError:
            pass


class Player:
    """A player who plays at random: a direction held a moment, buttons, START now and then to pass the screens.
    / Un joueur qui joue au hasard : une direction tenue un moment, des boutons, START de temps en temps."""

    def __init__(self, pad, rng):
        self.pad, self.rng = pad, rng
        self.move_t = self.hit_t = self.up_t = 0.0
        self.start_t = 0.0
        self.hit = None

    def step(self, now):
        rng, pad = self.rng, self.pad
        if now >= self.move_t:                                    # the stick / le stick
            self.move_t = now + rng.choice((0.08, 0.15, 0.3, 0.6, 1.0))
            x = rng.choice((LEFT, RIGHT, RIGHT, None))
            y = rng.choice((UP, DOWN, DOWN, None, None, None))
            for b in (LEFT, RIGHT, UP, DOWN):
                pad.set(b, b in (x, y))
        if self.hit is not None and now >= self.up_t:             # the button released / le bouton relâché
            pad.set(self.hit, False)
            self.hit = None
        if self.hit is None and now >= self.hit_t:
            self.hit = rng.choice(ACTIONS[:4] * 3 + ACTIONS[4:])
            pad.set(self.hit, True)
            self.up_t = now + rng.choice((0.05, 0.08, 0.15, 0.4))
            self.hit_t = self.up_t + rng.choice((0.03, 0.1, 0.25, 0.5))
        if now >= self.start_t:                                   # START: the select screens, CONTINUE / les écrans
            self.start_t = now + rng.uniform(4.0, 8.0)
            pad.tap(START)


def shots_dir(root):
    return os.path.join(os.path.abspath(root), "runtime", "robot_shots")


def write_cfg(root, base=BASE_PORT, unseen=False):
    """RetroArch's settings for the robot: the pad from the network, its screenshots in a folder of ArcadeDMD without
    their message on the screen, the games played left out of its history, and nothing saved to its own settings when
    it quits. It runs in a window, without sound and without reading the pads of the computer. unseen: without a window
    at all, for a screen that is off. / Les réglages de RetroArch pour le robot : la manette par le réseau, ses captures
    d'écran dans un dossier d'ArcadeDMD, les jeux joués hors de son historique, et rien d'écrit dans ses propres
    réglages quand il quitte. Il tourne en fenêtre, sans son et sans lire les manettes de l'ordinateur. unseen : sans
    fenêtre du tout, pour un écran éteint."""
    path = os.path.join(os.path.abspath(root), "runtime", "robot.cfg")
    os.makedirs(shots_dir(root), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(CFG % (base, shots_dir(root)) + (CFG_UNSEEN if unseen else ""))
    return path


_JOB = []


def tie(proc):
    """Windows: the RetroArch the robot started ends with the robot, however the robot ends (its window closed, the
    computer shut down). Without a window nobody would see it left behind. / Windows : le RetroArch lancé par le robot
    s'arrête avec le robot, quelle que soit la façon dont le robot s'arrête. Sans fenêtre, personne ne le verrait
    rester."""
    try:
        import ctypes
        from ctypes import wintypes
        k = ctypes.windll.kernel32

        class Basic(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                        ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD),
                        ("SchedulingClass", wintypes.DWORD)]

        class Extended(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", Basic), ("IoInfo", ctypes.c_uint64 * 6),
                        ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                        ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

        k.CreateJobObjectW.restype = wintypes.HANDLE
        k.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
        k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        if not _JOB:
            job = k.CreateJobObjectW(None, None)
            if not job:
                return False
            info = Extended()
            info.BasicLimitInformation.LimitFlags = 0x2000        # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            if not k.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info)):
                return False
            _JOB.append(job)                                      # kept open as long as the robot lives
        return bool(k.AssignProcessToJobObject(_JOB[0], int(proc._handle)))
    except Exception:                                             # not Windows, or refused: the game is simply not tied
        return False


def awake(on=True):
    """Keeps Windows from going to sleep while the robot plays: its buttons go to RetroArch by the network, Windows sees
    nobody at the keyboard. / Empêche Windows de se mettre en veille tant que le robot joue : ses touches passent par le
    réseau, Windows ne voit personne au clavier."""
    try:
        import ctypes
        ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if on else 0))
    except (AttributeError, OSError):
        pass                                                      # not Windows / pas Windows


def steady_console():
    """Windows freezes a program whose console window is clicked (its "quick edit" selection) until a key is pressed:
    turned off for the robot's console, a tour would wait for hours. / Windows fige un programme dont on clique la
    fenêtre de console jusqu'à l'appui d'une touche : coupé pour la console du robot, un tour attendrait des heures."""
    try:
        import ctypes
        k = ctypes.windll.kernel32
        h = k.GetStdHandle(-10)                                   # STD_INPUT_HANDLE
        mode = ctypes.c_uint32()
        if k.GetConsoleMode(h, ctypes.byref(mode)):
            k.SetConsoleMode(h, (mode.value & ~0x0040) | 0x0080)  # without ENABLE_QUICK_EDIT_MODE, ENABLE_EXTENDED_FLAGS
    except (AttributeError, OSError):
        pass                                                      # not Windows / pas Windows


def clear_shots(root):
    """The screenshots of a game that was cut short are not the next game's. / Les captures d'un jeu coupé."""
    sdir = shots_dir(root)
    try:
        for n in os.listdir(sdir):
            if n.lower().endswith((".png", ".bmp", ".jpg")):
                os.remove(os.path.join(sdir, n))
    except OSError:
        pass


def flag(root, on=True):
    """Tells ArcadeDMD that the robot plays (runtime/robot.on, touched every few seconds): it records the whole memory
    and leaves the screenshots to the robot. / Dit à ArcadeDMD que le robot joue."""
    path = os.path.join(root, "runtime", "robot.on")
    try:
        if on:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S"))
        elif os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


def acked(root, rom, since, wait=10.0):
    """ArcadeDMD's word that it records this game (runtime/robot.ack, written when it sees the game start while the
    robot's flag is up): its dict, or None when it says nothing. / La parole d'ArcadeDMD qu'il enregistre ce jeu."""
    path = os.path.join(root, "runtime", "robot.ack")
    end = time.monotonic() + wait
    while True:
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, dict) and d.get("time", 0) >= since - 1.0 and str(d.get("content", "")).lower() == rom.lower():
                return d
        except (OSError, ValueError):
            pass
        if time.monotonic() >= end:
            return None
        time.sleep(0.5)


def _small(path):
    """A heavy screenshot (RetroArch kept its shader and its screen size) as a JPEG 640 wide, or None to keep the file
    as it is. / Une capture lourde en JPEG de 640 de large, ou None pour garder le fichier tel quel."""
    try:
        if os.path.getsize(path) <= SHOT_BIG:
            return None
        import io
        import pygame
        img = pygame.image.load(path)
        w, h = img.get_size()
        if w > SHOT_WIDTH:
            img = pygame.transform.smoothscale(img, (SHOT_WIDTH, max(1, round(h * SHOT_WIDTH / w))))
        buf = io.BytesIO()
        pygame.image.save(img, buf, "shot.jpg")
        return buf.getvalue()
    except Exception:                                             # no pygame, a file it cannot read: kept as it is
        return None


def bundle(root, rom, since, wait=8.0, sub=""):
    """One file per game: what ArcadeDMD recorded since the game started and the screenshots RetroArch took, in
    runtime/robot/<game>.zip. Returns (the path, recordings, screenshots, memory recorded). The screenshots are then
    removed from their folder, the recordings stay in runtime/captures. / Un fichier par jeu."""
    caps = os.path.join(root, "runtime", "captures")
    end = time.monotonic() + wait
    files = []
    while True:                                                   # ArcadeDMD closes its files a moment after the game
        files = [n for n in _recorded(root, since) if n.endswith((".log", ".ram"))]
        if any(n.endswith(".ram") for n in files) or time.monotonic() >= end:
            break
        time.sleep(1.0)
    time.sleep(1.0)
    sdir = shots_dir(root)
    try:
        shots = sorted(n for n in os.listdir(sdir) if n.lower().endswith((".png", ".bmp", ".jpg")))
    except OSError:
        shots = []
    out = os.path.join(root, "runtime", "robot", sub) if sub else os.path.join(root, "runtime", "robot")
    os.makedirs(out, exist_ok=True)                               # sub: the files of another tour, kept apart
    path = os.path.join(out, rom + ".zip")
    try:
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for n in files:
                z.write(os.path.join(caps, n), n)
            for n in shots:
                small = _small(os.path.join(sdir, n))
                if small is not None:
                    z.writestr(zipfile.ZipInfo("screenshots/" + os.path.splitext(n)[0] + ".jpg",
                                               time.localtime(os.path.getmtime(os.path.join(sdir, n)))[:6]), small)
                else:
                    z.write(os.path.join(sdir, n), "screenshots/" + n, zipfile.ZIP_STORED)
    except OSError:
        return path, 0, 0, False
    for n in shots:
        try:
            os.remove(os.path.join(sdir, n))
        except OSError:
            pass
    return path, len(files), len(shots), any(n.endswith(".ram") for n in files)


def _setup_path(root):
    return os.path.join(root, "runtime", "robot.json")


def load_setup(root):
    try:
        with open(_setup_path(root), encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) and d.get("exe") and d.get("core") and d.get("rom_dir") else None
    except (OSError, ValueError):
        return None


def save_setup(root, setup):
    os.makedirs(os.path.join(root, "runtime"), exist_ok=True)
    with open(_setup_path(root), "w", encoding="utf-8") as f:
        json.dump(setup, f, indent=1, ensure_ascii=False)


def _command_line():
    """The command line of the RetroArch that runs (Windows), as a list, or []. / La ligne de commande de RetroArch."""
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command",
                              "(Get-CimInstance Win32_Process -Filter \"name='retroarch.exe'\").CommandLine"],
                             capture_output=True, text=True, timeout=15).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [a or b for a, b in re.findall(r'"([^"]*)"|(\S+)', out.strip().splitlines()[0])] if out.strip() else []


def learn_setup(content):
    """How RetroArch was started for the game that runs: its program, its core and the folder of its ROMs, read from its
    process and its history. None when it cannot be told. / Comment RetroArch a été lancé pour le jeu en cours."""
    from . import wincore
    for p in wincore.find_retroarch():
        exe = p.get("exe") or ""
        if not os.path.isabs(exe):
            continue
        radir = os.path.dirname(exe)
        core = p["cores"][-1] if p.get("cores") else wincore.core_from_history(radir, content)
        rom = ""
        for h in wincore.history_files(radir):
            try:
                with open(h, encoding="utf-8", errors="replace") as f:
                    items = json.load(f).get("items") or []
            except (OSError, ValueError, AttributeError):
                continue
            for it in items:
                path = (it.get("path") or "") if isinstance(it, dict) else ""
                path = path.split("#")[0]                             # a file inside an archive / un fichier dans une archive
                if os.path.splitext(os.path.basename(path.replace("\\", "/")))[0].lower() == (content or "").lower():
                    rom = path
                    break
            if rom:
                break
        args = _command_line()
        config = ""
        for i, a in enumerate(args):
            stem = os.path.splitext(os.path.basename(a.replace("\\", "/")))[0].lower()
            if not rom and stem == (content or "").lower() and os.path.isabs(a):
                rom = a                                               # not in the history: on the command line
            if a in ("-c", "--config") and i + 1 < len(args):
                config = args[i + 1]                                  # a settings file of its own / son fichier de réglages
            elif a.startswith("--config="):
                config = a.split("=", 1)[1]
            if not core and a in ("-L", "--libretro") and i + 1 < len(args):
                core = args[i + 1]
        if core and rom:
            return {"exe": exe, "core": core, "rom_dir": os.path.dirname(rom), "ext": os.path.splitext(rom)[1] or ".zip",
                    "last": content, "config": config}
    return None


def launch(setup, rom, cfg_path):
    """Starts RetroArch with this game and the robot's settings on top of its own. / Lance RetroArch avec ce jeu."""
    path = os.path.join(setup["rom_dir"], rom + setup.get("ext", ".zip"))
    args = [setup["exe"], "-L", setup["core"], "--appendconfig", cfg_path]
    if setup.get("config"):
        args += ["-c", setup["config"]]
    if setup.get("fullscreen", False):
        args.append("-f")
    args.append(path)
    proc = subprocess.Popen(args, cwd=os.path.dirname(setup["exe"]) or None,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tie(proc)
    return proc


def wait_playing(client, timeout, proc=None):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        st = client.status()
        if st and st.get("state") in ("PLAYING", "PAUSED"):
            return st
        if proc is not None and proc.poll() is not None:
            return None
        time.sleep(0.5)
    return None


def close_game(client, proc=None, wait=12.0):
    """Asks RetroArch to quit, and ends it when it does not. / Demande à RetroArch de quitter, sinon l'arrête."""
    client.send("QUIT")
    end = time.monotonic() + wait
    while time.monotonic() < end:
        time.sleep(0.5)
        if proc is not None:
            if proc.poll() is not None:
                return True
        elif client.status() is None:
            return True
        if end - time.monotonic() < wait / 2:
            client.send("QUIT")                                   # asked twice by some settings / demandé deux fois
    if proc is not None:
        try:
            proc.terminate()
            proc.wait(5)
        except (OSError, subprocess.TimeoutExpired):
            pass
    return False


WIN_TICK = 0.3            # seconds between two looks at the fight / entre deux regards au combat
WIN_COUNT = 3             # seconds a round is let run before its clock is run out / secondes de round avant la fin du chrono
WIN_LOW = 10              # the opponent's life is kept at one part in so many / la vie adverse gardée à un dixième
WIN_DEAF = 10             # looks where a write did not hold before giving up / écritures sans effet avant d'abandonner


def _tag_names(spec, out):
    """Every name a tag reads. / Tous les noms lus par un tag."""
    if isinstance(spec, str):
        out.add(spec)
    elif isinstance(spec, list):
        for x in spec:
            _tag_names(x, out)
    elif isinstance(spec, dict):
        for k, x in spec.items():
            if k not in ("note", "names"):
                _tag_names(x, out)
    return out


class Winner:
    """Makes player 1 win its fights, so that the robot crosses a game from its first opponent to its last and meets
    every fighter and every stage (the second tour, 1.39). While a round is fought, player 1's life is put back to
    the highest it was in the round, the opponent's is kept at a tenth, and the clock is run out once it has counted
    three seconds: the fighter with more life wins. Only what the game's file reads is written (the two life bars and
    the timer), at the place it is read, and only while both fighters stand and the BIOS says player 1 plays. Where
    the file works a life out from several (the computer's or player 2's), the one it picks at that moment is the one
    written. A game whose life bars the file does not know, or where a write does not hold, is played as in the first
    tour.

    Fait gagner ses combats au joueur 1, pour que le robot traverse un jeu de son premier adversaire au dernier et
    rencontre chaque combattant et chaque stage. Pendant un round, la vie du joueur 1 est remise au plus haut qu'elle
    a eu dans le round, celle de l'adversaire est gardée à un dixième, et le chrono est mis à sa fin dès qu'il a
    compté trois secondes : celui qui a le plus de vie gagne. Seul ce que le fichier du jeu lit est écrit (les deux
    barres de vie et le chrono), là où c'est lu, et seulement tant que les deux combattants sont debout et que le
    BIOS dit que le joueur 1 joue. Quand le fichier calcule une vie à partir de plusieurs (celle de l'ordinateur ou
    du joueur 2), celle qu'il choisit à cet instant est celle qui est écrite. Un jeu dont le fichier ne connaît pas
    les barres, ou qui ne garde pas une écriture, est joué comme au premier tour."""

    SIDES = ("health", "health_p2")
    ALONE = {"p1_mode": 1, "p2_mode": 0}                          # player 1 against the computer / contre l'ordinateur

    def __init__(self, client, layout, game, system=""):
        self.client, self.lay = client, layout
        g = game if isinstance(game, dict) else {}
        vals = game_values(g, system)
        self.tag = {k: v for k, v in (g.get("tag") or {}).items() if isinstance(v, dict)} if isinstance(g.get("tag"), dict) else {}
        read = set(self.SIDES)
        for side in self.SIDES:
            _tag_names(self.tag.get(side), read)
        self.cands = {}                                           # name -> where and how a life is read
        for name in sorted(read):
            bar = self._bar(vals.get(name))
            if bar is not None:
                self.cands[name] = bar
        t = vals.get("time")
        ok = isinstance(t, dict) and parse_addr(t.get("addr")) is not None and t.get("ptr") is None
        self.clock = t if ok and (t.get("type") or "u8").lower() in ("u8", "bcd") and (t.get("bytes") or 1) == 1 else None
        self.bios = layout.contains(0x10FDAE, 0x10FDB7)            # a Neo Geo: its BIOS says who plays / qui joue
        self.cur = self._pick(self.ALONE)
        self.ready = all(b is not None for b in self.cur)
        self.rounds = self.wins = self.written = 0
        self.off = None               # why nothing is written any more / pourquoi plus rien n'est écrit
        self.on = False               # a round is being fought / un round est en cours
        self.top = [0, 0]             # the highest life read in this round / la plus haute vie lue dans ce round
        self.last = None
        self.t_top = self.t_prev = None
        self.deaf = 0
        self.asked = False

    @staticmethod
    def _bar(d):
        if not isinstance(d, dict) or not d.get("addr") or d.get("mame_only") or d.get("mask") is not None or d.get("shift"):
            return None
        kind = (d.get("type") or "u8").lower()
        size = 2 if kind in ("u16", "s16") or (kind == "be" and d.get("bytes") == 2) else 1 if kind == "u8" else 0
        mult = d.get("mult")
        if not size or isinstance(mult, bool) or not isinstance(mult, (int, float)) or mult <= 0 or parse_addr(d.get("addr")) is None:
            return None
        full = round((100 - (d.get("add") or 0)) / mult)
        if full < 8:
            return None
        rng = d.get("ptr_range") if isinstance(d.get("ptr_range"), list) and len(d.get("ptr_range")) == 2 else None
        return {"addr": parse_addr(d.get("addr")), "ptr": parse_addr(d.get("ptr")), "size": size, "signed": kind == "s16",
                "range": (parse_addr(rng[0]), parse_addr(rng[1])) if rng else None,
                "cap": int(full * 1.3) + 1, "zero": parse_addr(d.get("zero_from"))}

    def _pick(self, modes):
        """The life the file reads for each side right now: its tags are worked out with each life's own name in the
        place of its value, as the engine works them out. / La vie que le fichier lit pour chaque côté à cet instant."""
        from .memvalues import resolve_value
        values = {name: name for name in self.cands}
        values.update(modes)
        for k, spec in self.tag.items():
            try:
                v = resolve_value(spec, values)
            except Exception:
                v = None
            if v is not None:
                values[k] = v
        return [self.cands.get(values.get(side)) if isinstance(values.get(side), str) else None for side in self.SIDES]

    def _look(self):
        """(where and what each life is, the clock, does player 1 play), or None when RetroArch does not answer.
        / (où et combien vaut chaque vie, le chrono, le joueur 1 joue-t-il), ou None."""
        spans = [(0x10FDAE, 0x10FDB7)] if self.bios else []
        if self.clock:
            a = parse_addr(self.clock["addr"])
            spans.append((a, a))
        for b in self.cands.values():
            spans.append((b["ptr"], b["ptr"] + 3) if b["ptr"] is not None else (b["addr"], b["addr"] + b["size"] - 1))
        got = self.lay.read_cpu_many(self.client, spans, True)
        if got is None:
            return None

        def cell(a, n):
            for base, data in got:
                if base <= a and a + n <= base + len(data):
                    return int.from_bytes(data[a - base:a - base + n], "big")
            return None
        modes, plays = self.ALONE, True
        if self.bios:
            modes = {"p1_mode": cell(0x10FDB6, 1), "p2_mode": cell(0x10FDB7, 1)}
            plays = modes["p1_mode"] == 1 and cell(0x10FDAF, 1) == 2
        clock = None
        if self.clock:
            raw = cell(parse_addr(self.clock["addr"]), 1)
            if (self.clock.get("type") or "u8").lower() == "bcd":
                clock = (raw >> 4) * 10 + (raw & 15) if (raw >> 4) <= 9 and (raw & 15) <= 9 else None
            else:
                clock = raw
        self.cur = self._pick(modes)
        out = []
        for b in self.cur:
            if b is None:
                out.append((None, None))
                continue
            if b["ptr"] is not None:                              # an object that moves: read where it points
                where = cell(b["ptr"], 4) & 0xFFFFFF
                if b["range"] and not b["range"][0] <= where <= b["range"][1]:
                    out.append((None, None))
                    continue
                addr = where + b["addr"]
                r = self.lay.read_cpu(self.client, addr, addr + b["size"] - 1)
                v = int.from_bytes(r[1][addr - r[0]:addr - r[0] + b["size"]], "big") if r is not None else None
            else:
                addr, v = b["addr"], cell(b["addr"], b["size"])
            if v is not None and b["signed"] and v >= 0x8000:
                v -= 0x10000
            out.append((addr, v))
        return out, clock, plays

    def _stands(self, k, v):
        b = self.cur[k]
        return b is not None and v is not None and 0 < v <= b["cap"] and (b["zero"] is None or v < b["zero"])

    def _set(self, k, addr, v):
        self.written += 1
        b = self.cur[k]
        return self.lay.write_cpu(self.client, addr, int(v).to_bytes(b["size"], "big", signed=b["signed"]))

    def _end(self):
        if self.on:
            self.on = False
            if self.last is not None and self.last[0] > self.last[1]:
                self.wins += 1
        self.asked = False

    def tick(self, now):
        """One look at the fight, and what it takes to keep player 1 ahead. / Un regard au combat."""
        if self.off or not self.ready:
            return
        try:
            self._tick()
        except Exception as e:                                    # a game that does not fit: played as it is
            self.off = tr(f"erreur {type(e).__name__}", f"error {type(e).__name__}")

    def _tick(self):
        look = self._look()
        if look is None:
            return self._end()
        ((a1, h1), (a2, h2)), clock, plays = look
        fought = plays and self._stands(0, h1) and self._stands(1, h2) \
            and (self.clock is None or (clock is not None and 1 <= clock <= 999))
        if not fought:
            return self._end()
        if self.on and clock is not None and self.t_prev is not None and clock > self.t_prev + 1:
            self._end()                                           # the clock set again: another round / un autre round
        if not self.on:
            self.on = True
            self.rounds += 1
            self.top = [h1, h2]
            self.t_top = clock
            self.deaf = 0
        self.t_prev = clock
        self.top = [max(self.top[0], h1), max(self.top[1], h2)]
        self.last = (h1, h2)
        if h1 < self.top[0]:
            self._set(0, a1, self.top[0])
        low = max(1, self.top[1] // WIN_LOW)
        if h2 > low:
            if self.asked:                                        # asked at the last look, and still above
                self.deaf += 1
                if self.deaf >= WIN_DEAF:
                    self.off = tr("le jeu ne garde pas ce que j'écris", "the game does not keep what is written")
                    return
            self._set(1, a2, low)
            self.asked = True
        else:
            self.asked = False
            self.deaf = 0
        if self.clock and clock > 1 and self.t_top is not None and self.t_top - clock >= WIN_COUNT:
            self.written += 1
            self.lay.write_cpu(self.client, parse_addr(self.clock["addr"]), [1])


def play(client, seconds, rng, base=BASE_PORT, two_from=0.7, alive=None, tick=None, shots=True, probe=None,
         trace=None, winner=None):
    """Plays the game that runs: a coin, START, then at random; a second player joins for the last part; a screenshot
    asked of RetroArch every ten seconds. Returns False when RetroArch stopped answering.
    / Joue le jeu en cours : une pièce, START, puis au hasard, une capture d'écran toutes les dix secondes."""
    p1, p2 = RemotePad(1, base=base), RemotePad(2, base=base)
    one, two = Player(p1, rng), Player(p2, rng)
    t0 = time.monotonic()
    coin_t = seen_t = win_t = t0
    shot_t = t0 + 8.0
    ok = True
    try:
        time.sleep(2.0)
        for _ in range(2):
            p1.tap(SELECT, 0.15)                                  # the coin of FinalBurn Neo is SELECT / la pièce
            time.sleep(0.6)
        p1.tap(START, 0.15)
        one.start_t = time.monotonic() + 3.0
        joined = False
        while True:
            now = time.monotonic()
            if now - t0 >= seconds:
                break
            if now >= coin_t + 20.0:                              # a coin now and then: CONTINUE / une pièce : CONTINUE
                coin_t = now
                p1.tap(SELECT, 0.15)
                if joined and two_from <= 0:                      # two players from the start: the second stays too
                    p2.tap(SELECT, 0.15)
            one.step(now)
            if now - t0 >= seconds * two_from:                    # the second player joins / le deuxième joueur arrive
                if not joined:
                    joined = True
                    p2.tap(SELECT, 0.15)
                    time.sleep(0.5)
                    p2.tap(START, 0.15)
                two.step(now)
            if winner is not None and now >= win_t:               # player 1 kept ahead / le joueur 1 gardé devant
                win_t = now + WIN_TICK
                winner.tick(now)
            if shots and now >= shot_t:
                shot_t = now + SHOT_EVERY
                client.send("SCREENSHOT")
            if now - seen_t >= 5.0:
                seen_t = now
                st = client.status()
                if not st or st.get("state") not in ("PLAYING", "PAUSED") or (alive is not None and not alive()):
                    ok = False
                    break
                if tick is not None:
                    tick(now - t0)
                if probe is not None and trace is not None:       # the stick the game sees, its frame count
                    got = probe()
                    if got is not None:
                        trace.append(got)
            time.sleep(0.015)
    finally:
        p1.close()
        p2.close()
    return ok


_LIBRARY = {}


def _game(st, root):
    """The game that runs, as ArcadeDMD knows it: its file, or None. / Le jeu en cours, tel qu'ArcadeDMD le connaît."""
    from .app import GameLibrary
    from .retroarch import resolve
    try:
        if root not in _LIBRARY:
            _LIBRARY[root] = GameLibrary(root, lambda m: None).games
        return resolve(_LIBRARY[root], st.get("content") or "", st.get("system") or "")[1]
    except Exception:
        return None


def _layout(st, root):
    """Where the game's memory is, as ArcadeDMD knows the game. / Où est la mémoire du jeu."""
    return layout_for(_game(st, root), st.get("system") or "")


def game_speed(client, st, root, wait=1.0, tries=4):
    """Neo Geo: the frames the game runs in a second, counted by its BIOS (the bytes at 0x10FE88, one more at each
    frame), or None when it cannot be told. 59 is right; hundreds mean RetroArch runs flat out. The BIOS sets its
    counter again while a game starts (Fatal Fury 2, ten seconds in), so only its low 16 bits are compared, a measure
    out of range is taken again, and the middle one of those taken is kept.
    / Neo Geo : les images que le jeu fait en une seconde, comptées par son BIOS, ou None. Le BIOS remet son compteur
    pendant le démarrage d'un jeu, donc seuls ses 16 bits bas sont comparés, une mesure hors norme est refaite, et
    celle du milieu est gardée."""
    lay = _layout(st, root)
    if not lay.contains(0x10FE88, 0x10FE8B):
        return None

    def read():
        got = lay.read_cpu(client, 0x10FE88, 0x10FE8B)
        return (int.from_bytes(got[1][0x10FE8A - got[0]:0x10FE8C - got[0]], "big"), time.monotonic()) if got else None
    seen = []
    for _ in range(tries):
        a = read()
        time.sleep(wait)
        b = read()
        if a is None or b is None or b[1] <= a[1]:
            continue
        fps = ((b[0] - a[0]) % 65536) / (b[1] - a[1])
        seen.append(fps)
        if 50 <= fps <= 70:
            return fps                                            # as it should: no need to measure again
    return sorted(seen)[len(seen) // 2] if seen else None


def prober(client, st, root):
    """Neo Geo: a function that reads what the game sees of player 1's stick and the frames it has run (the low 16
    bits of the BIOS counter), with the time; None for another system. Read every few seconds while the robot plays:
    a game does not read its stick during its start, which one reading there would take for a robot it does not see.
    / Neo Geo : une fonction qui lit ce que le jeu voit du stick du joueur 1 et les images qu'il a faites, avec
    l'heure ; None pour un autre système. Lu toutes les quelques secondes pendant que le robot joue : un jeu ne lit
    pas son stick pendant son démarrage."""
    lay = _layout(st, root)
    if not (lay.contains(0x10FD96, 0x10FD96) and lay.contains(0x10FE88, 0x10FE8B)):
        return None

    def probe():
        a = lay.read_cpu(client, 0x10FD96, 0x10FD96)
        b = lay.read_cpu(client, 0x10FE88, 0x10FE8B)
        if not a or not b:
            return None
        return (a[1][0x10FD96 - a[0]], int.from_bytes(b[1][0x10FE8A - b[0]:0x10FE8C - b[0]], "big"), time.monotonic())
    return probe


def judged(trace):
    """(the game saw the robot's stick, its frames a second) from the readings of a whole game; None for what cannot
    be told. The stick is seen when the byte took several values; the speed is the middle one of all the intervals.
    / (le jeu a vu le stick du robot, ses images par seconde) d'après les lectures de toute une partie."""
    if not trace or len(trace) < 6:
        return None, None
    stick = len({t[0] for t in trace}) >= 3
    rates = sorted(((b[1] - a[1]) % 65536) / (b[2] - a[2]) for a, b in zip(trace, trace[1:]) if b[2] > a[2])
    return stick, rates[len(rates) // 2] if rates else None


def inputs_seen(client, st, root):
    """Neo Geo: does the BIOS see the stick the robot holds? True, False, or None when it cannot be told (another
    system). / Le BIOS voit-il le stick que tient le robot ?"""
    lay = _layout(st, root)
    if not lay.contains(0x10FD96, 0x10FD96):
        return None
    pad = RemotePad(1)
    try:
        def read():
            got = lay.read_cpu(client, 0x10FD96, 0x10FD96)
            return got[1][0x10FD96 - got[0]] if got else None
        time.sleep(0.3)
        rest = read()
        pad.set(RIGHT, True)
        held = []
        for _ in range(8):                                        # read several times: an image may have forgotten it
            time.sleep(0.1)
            held.append(read())
        pad.set(RIGHT, False)
        held = [v for v in held if v is not None]
        if rest is None or not held:
            return None
        return any((rest ^ v) & 0x08 for v in held)
    finally:
        pad.close()


def roms(root, setup, fights=False):
    """The games of ArcadeDMD whose ROM is in the folder, the fighting games first; fights: those alone.
    / Les jeux dont la ROM est là, les jeux de combat d'abord ; fights : eux seuls."""
    out = []
    ext = setup.get("ext", ".zip")
    for name in sorted(os.listdir(os.path.join(root, "games"))):
        key = name[:-5]
        if not name.endswith(".json") or key.startswith("_") or not os.path.isfile(os.path.join(setup["rom_dir"], key + ext)):
            continue
        try:
            with open(os.path.join(root, "games", name), encoding="utf-8") as f:
                g = json.load(f)
        except (OSError, ValueError):
            continue
        if isinstance(g, dict) and isinstance(g.get("memory"), dict):
            fight = isinstance(g.get("scene_from"), str) and "combat" in g["scene_from"]
            out.append((0 if fight else 1, key))
    return [k for kind, k in sorted(out) if kind == 0 or not fights]


class Report:
    def __init__(self, root, name, out=print):
        self.path = os.path.join(root, "runtime", name)
        self.out = out
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write("\n" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

    def __call__(self, text=""):
        self.out(text)
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(time.strftime("%H:%M:%S ") + text + "\n")
        except OSError:
            pass


def _recorded(root, since):
    """The recordings ArcadeDMD wrote since then. / Les enregistrements écrits par ArcadeDMD depuis."""
    folder = os.path.join(root, "runtime", "captures")
    try:
        return sorted(n for n in os.listdir(folder) if os.path.getmtime(os.path.join(folder, n)) >= since)
    except OSError:
        return []


def _client(cfg):
    ra = cfg.get("retroarch", {}) or {}
    return RetroArchClient(ra.get("host", "127.0.0.1"), int(ra.get("port", 55355)), timeout=0.5)


def snapshots(path):
    """How many snapshots of the memory a .ram file or a game's zip holds. / Le nombre d'instantanés de la mémoire."""
    try:
        if path.endswith(".zip"):
            with zipfile.ZipFile(path) as z:
                data = b"".join(z.read(n) for n in z.namelist() if n.endswith(".ram"))
        else:
            with open(path, "rb") as f:
                data = f.read()
    except (OSError, zipfile.BadZipFile):
        return 0
    n, pos = 0, data.find(b"\n") + 1
    while 0 < pos <= len(data) - 12:
        size = struct.unpack_from("<dI", data, pos)[1]
        pos += 12 + size
        n += 1
    return n


def _result(root, rom, since, say, head="", sub=""):
    """Puts the game's recording in its file and says what it holds. / Range l'enregistrement du jeu et dit ce qu'il a."""
    path, files, shots, ram = bundle(root, rom, since, sub=sub)
    name = os.path.join("runtime", "robot", sub, os.path.basename(path)) if sub else os.path.join("runtime", "robot", os.path.basename(path))
    count = snapshots(path) if ram else 0
    if not files:
        say(tr(f"{head}ArcadeDMD n'a rien enregistré. Est-il lancé ? ({shots} captures d'écran dans {name})",
               f"{head}ArcadeDMD recorded nothing. Is it running? ({shots} screenshots in {name})"))
    else:
        say(tr(f"{head}{name} : {f'mémoire enregistrée ({count} instantanés)' if ram else 'SANS la mémoire'}, {shots} captures d'écran",
               f"{head}{name}: {f'memory recorded ({count} snapshots)' if ram else 'WITHOUT the memory'}, {shots} screenshots"))
    return files, shots, ram, count


def test(root, cfg, wait=300, seconds=120, out=print):
    """One game, two minutes: RetroArch started by the robot, the buttons it sends seen by the game, the recording
    written by ArcadeDMD. / Un jeu, deux minutes : la chaîne complète vérifiée."""
    say = Report(root, "robot_test.txt", out)
    say(tr("Essai du robot", "Robot test"))
    client = _client(cfg)
    awake()
    steady_console()
    try:
        st = client.status()
        running = bool(st) and st.get("state") in ("PLAYING", "PAUSED")
        setup = load_setup(root)
        if not running and setup is None:
            say(tr("Lance un jeu Neo Geo depuis LaunchBox comme d'habitude, par exemple Samurai Shodown II. "
                   "L'essai continue tout seul dès que le jeu tourne.",
                   "Start a Neo Geo game from LaunchBox as usual, for example Samurai Shodown II. The test goes on "
                   "by itself as soon as the game runs."))
            st = wait_playing(client, wait)
            running = st is not None
            if not running:
                say(tr("Aucun jeu vu dans RetroArch. Essai arrêté.", "No game seen in RetroArch. Test stopped."))
                return 1
            time.sleep(3.0)
        if running:
            found = learn_setup(st.get("content") or "")
            if found is None and setup is None:
                say(tr("Je ne trouve pas comment RetroArch a été lancé (son programme, son cœur, le dossier des ROM). "
                       "Essai arrêté.",
                       "Cannot tell how RetroArch was started (its program, its core, the ROM folder). Test stopped."))
                return 1
            if found is not None:
                for k in ("done", "unseen", "aside", "won", "aside_won"):   # what the tours know stays known
                    if setup is not None and setup.get(k):
                        found[k] = setup[k]
                setup = found
                save_setup(root, setup)
            say(tr(f"RetroArch : {setup['exe']}", f"RetroArch: {setup['exe']}"))
            say(tr(f"Cœur : {setup['core']}", f"Core: {setup['core']}"))
            say(tr(f"Dossier des ROM : {setup['rom_dir']}", f"ROM folder: {setup['rom_dir']}"))
            say(tr("Je ferme le jeu pour le relancer moi-même.", "Closing the game to start it again myself."))
            close_game(client)
            time.sleep(3.0)
        rom = setup.get("last") or ""
        say(tr(f"Lancement de {rom}", f"Starting {rom}"))
        since = time.time()
        flag(root)
        clear_shots(root)
        proc = launch(setup, rom, write_cfg(root))
        st = wait_playing(client, 60, proc)
        if st is None:
            say(tr("RetroArch n'a pas démarré le jeu en une minute. Essai arrêté.",
                   "RetroArch did not start the game within a minute. Test stopped."))
            close_game(client, proc)
            return 1
        say(tr(f"Le jeu tourne ({st.get('content')}).", f"The game runs ({st.get('content')})."))
        time.sleep(6.0)
        ack = acked(root, rom, since)
        if ack is None:
            say(tr("ÉCHEC, ArcadeDMD ne dit pas qu'il enregistre ce jeu. Il doit tourner pendant l'essai, depuis ce "
                   "dossier et dans cette version. Lance ArcadeDMD, puis relance robot_test.bat.",
                   "FAILED, ArcadeDMD does not say it records this game. It must run during the test, from this folder "
                   "and in this version. Start ArcadeDMD, then run robot_test.bat again."))
            close_game(client, proc)
            return 1
        say(tr("OK, ArcadeDMD enregistre ce jeu avec toute sa mémoire." if ack.get("memory")
               else "ArcadeDMD voit ce jeu mais n'enregistre pas sa mémoire.",
               "OK, ArcadeDMD records this game with its whole memory." if ack.get("memory")
               else "ArcadeDMD sees this game but does not record its memory."))
        seen = inputs_seen(client, st, root)
        for _ in range(9):                                        # a game reads its stick once it has started
            if seen is not False:
                break
            time.sleep(1.5)
            seen = inputs_seen(client, st, root)
        if seen is True:
            say(tr("OK, le jeu voit le stick que j'envoie.", "OK, the game sees the stick I send."))
        elif seen is False:
            say(tr("ÉCHEC, le jeu ne voit pas le stick que j'envoie. RetroArch n'a pas pris mes réglages "
                   "(network_remote_enable).",
                   "FAILED, the game does not see the stick I send. RetroArch did not take my settings "
                   "(network_remote_enable)."))
        else:
            say(tr("Pas un jeu Neo Geo, je ne peux pas vérifier le stick dans sa mémoire. Je joue quand même.",
                   "Not a Neo Geo game, the stick cannot be checked in its memory. Playing anyway."))
        fps = game_speed(client, st, root)
        if fps is not None:
            say(tr(f"{'OK' if 50 <= fps <= 70 else 'ANORMAL'}, le jeu tourne à {fps:.0f} images par seconde (59 attendues).",
                   f"{'OK' if 50 <= fps <= 70 else 'ABNORMAL'}, the game runs at {fps:.0f} frames a second (59 expected)."))
        say(tr(f"Je joue {seconds // 60} minutes, dans une fenêtre et sans son : une pièce, START, puis le personnage "
               "bouge tout seul.",
               f"Playing for {seconds // 60} minutes, in a window and without sound: a coin, START, then the character "
               "moves alone."))
        ok = play(client, seconds, random.Random(), alive=lambda: proc.poll() is None, tick=lambda t: flag(root))
        say(tr("Partie finie, je ferme le jeu.", "Game over, closing it.") if ok
            else tr("RetroArch s'est arrêté pendant la partie.", "RetroArch stopped during the game."))
        close_game(client, proc)
        files, shots, ram, _count = _result(root, rom, since, say)
        say(tr(f"Envoie-moi runtime\\robot_test.txt et runtime\\robot\\{rom}.zip.",
               f"Send me runtime\\robot_test.txt and runtime\\robot\\{rom}.zip."))
        return 0 if seen is not False and ok and ram and shots and (fps is None or 50 <= fps <= 70) else 1
    finally:
        flag(root, False)
        awake(False)
        client.close()


WAIT = 300.0              # between two looks at a screen that is off / entre deux regards à un écran éteint


def _pause(seconds):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        time.sleep(5.0)


def _trouble(root):
    """An error nobody foresaw, kept in runtime/robot_crash.log. / Une erreur imprévue, gardée dans ce fichier."""
    try:
        with open(os.path.join(root, "runtime", "robot_crash.log"), "a", encoding="utf-8") as f:
            f.write("\n" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n" + traceback.format_exc())
    except OSError:
        pass


def works(client, root, setup, rom, cfg_path, seconds=15.0):
    """A game that was recorded before, started for a quarter of a minute: True when RetroArch runs it, ArcadeDMD says
    it records it and its memory can be read. It tells games that cannot be played from a screen that is off, an
    ArcadeDMD that is closed or ROMs that are gone, which fail the same way.
    / Un jeu déjà enregistré, lancé un quart de minute : True quand RetroArch le fait tourner, qu'ArcadeDMD dit
    l'enregistrer et que sa mémoire se lit. Distingue des jeux injouables d'un écran éteint, d'un ArcadeDMD fermé ou
    de ROM disparues, qui échouent de la même façon."""
    proc = None
    try:
        since = time.time()
        flag(root)
        proc = launch(setup, rom, cfg_path)
        st = wait_playing(client, 45, proc)
        if st is None or acked(root, rom, since, 20.0) is None:
            return False
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            time.sleep(1.0)
            flag(root)
            now = client.status()
            if not now or now.get("state") not in ("PLAYING", "PAUSED") or proc.poll() is not None:
                return False
        probe = prober(client, st, root)
        return probe is None or probe() is not None
    except Exception:
        _trouble(root)
        return False
    finally:
        if proc is not None:
            close_game(client, proc, 6.0)
        clear_shots(root)


def _attempt(client, root, setup, rom, cfg_path, minutes, rng, unseen, say, head, win=False, state=None):
    """One game played and put in its file: None when it is recorded, else why it is not. win: player 1 is made to
    win its fights and no second player comes in. state: what the second tour remembers from a game to the next;
    "versus" in it: nothing is written, two players play from the start instead.
    / Un jeu joué et rangé. win : le joueur 1 gagne ses combats et le deuxième joueur ne vient pas. state : ce que le
    deuxième tour retient d'un jeu à l'autre ; avec "versus", rien n'est écrit, deux joueurs jouent dès le début."""
    state = state if isinstance(state, dict) else {}
    versus = win and bool(state.get("versus"))
    since = time.time()
    flag(root)
    clear_shots(root)
    proc = launch(setup, rom, cfg_path)
    trace = []
    try:
        st = wait_playing(client, 45, proc)
        if st is None:
            return tr("ne démarre pas", "does not start")
        if acked(root, rom, since, 20.0) is None:                 # nobody records / personne n'enregistre
            return tr("ArcadeDMD ne dit pas qu'il l'enregistre", "ArcadeDMD does not say it records it")
        say(tr(f"{head} : en cours, {minutes} minute{'s' if minutes > 1 else ''}",
               f"{head}: playing, {minutes} minute{'s' if minutes > 1 else ''}"))
        champ = Winner(client, _layout(st, root), _game(st, root), st.get("system") or "") if win and not versus else None
        ok = play(client, minutes * 60, rng, alive=lambda: proc.poll() is None, tick=lambda t: flag(root),
                  shots=not unseen, probe=prober(client, st, root), trace=trace, winner=champ,
                  two_from=0.0 if versus else 2.0 if win else 0.7)
    finally:
        close_game(client, proc)
    stick, fps = judged(trace)
    notes = "" if ok else tr("arrêté avant la fin, ", "stopped early, ")
    if versus:
        notes += tr("à deux joueurs, ", "two players, ")
    if champ is not None:
        if not champ.ready:
            notes += tr("barres de vie inconnues, joué sans gagner, ", "life bars not known, played without winning, ")
        elif champ.off:
            notes += tr(f"{champ.wins} rounds gagnés puis {champ.off}, ", f"{champ.wins} rounds won, then {champ.off}, ")
        else:
            notes += tr(f"{champ.wins} rounds gagnés, ", f"{champ.wins} rounds won, ")
        if champ.ready:                                           # three games in a row that keep no write: not them
            state["deaf"] = state.get("deaf", 0) + 1 if champ.off and champ.wins == 0 else 0
            if state["deaf"] >= 3:
                state["versus"] = True
                say(tr("Trois jeux de suite n'ont rien gardé de ce que j'écris : RetroArch ne prend pas mes écritures. "
                       "Je continue le tour à deux joueurs, sans rien écrire, pour rencontrer plus de combattants.",
                       "Three games in a row kept nothing of what is written: RetroArch does not take the writes. The "
                       "tour goes on with two players, writing nothing, to meet more fighters."))
    if stick is False:                                            # said, never a reason to stop / dit, jamais un arrêt
        notes += tr("stick du robot pas vu par le jeu, ", "the robot's stick not seen by the game, ")
    if fps is not None and not 50 <= fps <= 70:
        notes += tr(f"{fps:.0f} images par seconde au lieu de 59, ", f"{fps:.0f} frames a second instead of 59, ")
    count = _result(root, rom, since, say, f"{head} : {notes}", "win" if win else "")[3]
    if count < minutes * 60:                                      # less than half its memory / moins de la moitié
        return tr("pas assez de mémoire enregistrée", "not enough memory recorded")
    return None


def tour(root, cfg, minutes=6, only=None, out=print, unseen=False, win=False):
    """Every game whose ROM is in the folder, a few minutes each. Only Ctrl+C stops it; started again, it goes on where
    it stopped. A game that cannot be played is tried once more at the end of the tour, then left aside. Three games
    failing in a row are not taken for their own fault: a game recorded before is started, and when it fails too (the
    screen is off, ArcadeDMD is closed) the tour waits and looks again every five minutes, then takes those games
    again. unseen: for a screen that is off, RetroArch without a window and no screenshot (it closes when asked for
    one without a video driver); these games keep their place in the tour with the screen on, which plays them again
    with their screenshots. win: the second tour, the fighting games alone, player 1 made to win so that each game
    is crossed to its end (Winner); its files go to runtime/robot/win and its list is its own.
    / Tous les jeux dont la ROM est là, quelques minutes chacun. Seul Ctrl+C l'arrête ; relancé, il reprend où il
    s'est arrêté. Un jeu injouable est réessayé une fois à la fin du tour, puis laissé de côté. Trois jeux qui
    échouent de suite ne sont pas tenus pour fautifs : un jeu déjà enregistré est lancé, et s'il échoue aussi (écran
    éteint, ArcadeDMD fermé) le tour attend et regarde à nouveau toutes les cinq minutes, puis reprend ces jeux.
    unseen : pour un écran éteint, RetroArch sans fenêtre et sans capture d'écran ; ces jeux gardent leur place dans
    le tour écran allumé, qui les rejoue avec leurs captures. win : le deuxième tour, les jeux de combat seuls, le
    joueur 1 gagne pour que chaque jeu soit traversé jusqu'au bout ; ses fichiers vont dans runtime/robot/win et sa
    liste est la sienne."""
    say = Report(root, "robot.txt", out)
    setup = load_setup(root)
    if setup is None:
        say(tr("Lance d'abord robot_test.bat, il apprend où sont RetroArch et les ROM.",
               "Run robot_test.bat first, it learns where RetroArch and the ROMs are."))
        return 1
    have = roms(root, setup)
    games = [g for g in (roms(root, setup, True) if win else have) if not only or g in only]
    key = "won" if win else "unseen" if unseen else "done"
    side = "aside_won" if win else "aside"
    known = [g for g in have if g in set(setup.get("done") or []) | set(setup.get("unseen") or []) | set(setup.get("won") or [])]
    done = set(setup.get(key if win else "done") or []) if not only else set()
    if unseen and not only:
        done |= set(setup.get("unseen") or [])                    # with or without its screenshots / avec ou sans
    todo = [g for g in games if g not in done]
    if not todo and games:
        if unseen:
            say(tr("Tous les jeux sont déjà enregistrés. Rien à faire écran éteint.",
                   "Every game is already recorded. Nothing to do with the screen off."))
            return 0
        done, todo = set(), games                                 # all done: a new tour / tout est fait : un nouveau tour
    aside = set(setup.get(side) or []) if not only else set()
    todo = [g for g in todo if g not in aside] + [g for g in todo if g in aside]   # those left aside before come last
    total = len(todo) * (minutes + 0.7)
    long_fr = f"{total / 60:.1f} heures" if total >= 90 else f"{total:.0f} minutes"
    long_en = f"{total / 60:.1f} hours" if total >= 90 else f"{total:.0f} minutes"
    if win:
        say(tr(f"Deuxième tour, le robot gagne ses combats : {len(todo)} jeu(x) de combat, {minutes} minute(s) chacun, "
               f"environ {long_fr}. L'écran doit rester allumé. Ctrl+C pour arrêter.",
               f"Second tour, the robot wins its fights: {len(todo)} fighting game(s), {minutes} minute(s) each, about "
               f"{long_en}. The screen must stay on. Ctrl+C to stop."))
    elif unseen:
        say(tr(f"Tour du robot écran éteint : {len(todo)} jeu(x), {minutes} minute(s) chacun, environ {long_fr}. "
               "RetroArch tourne sans fenêtre, la mémoire est enregistrée, sans captures d'écran. Ctrl+C pour arrêter.",
               f"Robot tour, screen off: {len(todo)} game(s), {minutes} minute(s) each, about {long_en}. RetroArch "
               "runs without a window, the memory is recorded, without screenshots. Ctrl+C to stop."))
    else:
        say(tr(f"Tour du robot : {len(todo)} jeu(x), {minutes} minute(s) chacun, environ {long_fr}. L'écran doit "
               "rester allumé. Ctrl+C pour arrêter.",
               f"Robot tour: {len(todo)} game(s), {minutes} minute(s) each, about {long_en}. The screen must stay "
               "on. Ctrl+C to stop."))
    client = _client(cfg)
    cfg_path = write_cfg(root, unseen=unseen)
    rng = random.Random()
    place = {g: i + 1 for i, g in enumerate(todo)}
    queue = collections.deque(todo)
    tries = collections.Counter({g: 1 for g in todo if g in aside})   # left aside before: one try / un seul essai
    streak = []                                                   # the games that failed in a row / échecs de suite
    left, fresh, waits = [], [], 0                                # fresh: recorded by this tour / enregistrés ici
    memo = {}                                                     # what the second tour remembers between games
    if setup.get("last") in have:
        known.insert(0, setup["last"])

    def keep():
        if only:
            return
        setup[key] = sorted(set(setup.get(key) or []) | set(fresh)) if unseen else sorted(done)
        setup[side] = sorted(aside)
        try:
            save_setup(root, setup)
        except OSError:
            pass

    awake()
    steady_console()
    try:
        if client.status() is not None:
            say(tr("RetroArch tourne déjà, je le ferme.", "RetroArch is already running, closing it."))
            close_game(client)
            time.sleep(3.0)
        while queue:
            rom = queue.popleft()
            head = f"{place[rom]}/{len(todo)} {rom}"
            try:
                why = _attempt(client, root, setup, rom, cfg_path, minutes, rng, unseen, say, head, win, memo)
            except Exception as e:                                # one game lost, not the tour / un jeu, pas le tour
                _trouble(root)
                why = tr(f"erreur imprévue ({type(e).__name__}), notée dans runtime\\robot_crash.log",
                         f"unforeseen error ({type(e).__name__}), written in runtime\\robot_crash.log")
            if why is None:
                streak, waits = [], 0
                fresh.append(rom)
                done.add(rom)
                aside.discard(rom)
                keep()
                time.sleep(3.0)
                continue
            tries[rom] += 1
            streak.append(rom)
            if tries[rom] < 2:
                say(tr(f"{head} : {why}, il sera réessayé à la fin du tour", f"{head}: {why}, tried again at the end of the tour"))
                queue.append(rom)
            else:
                say(tr(f"{head} : {why}, je le laisse de côté", f"{head}: {why}, left aside"))
                left.append(rom)
                aside.add(rom)
                keep()
            time.sleep(3.0)
            if len(streak) < 3:
                continue
            # three in a row: these games, or the screen that went off, ArcadeDMD that was closed?
            # trois de suite : ces jeux, ou l'écran qui s'est éteint, ArcadeDMD qui a été fermé ?
            good = [g for g in fresh[::-1] + known[::-1] if g not in streak]
            good = list(dict.fromkeys(good))[:2]                  # two games that were recorded / deux jeux enregistrés
            if good:
                if any(works(client, root, setup, g, cfg_path) for g in good):
                    streak = []                                   # these games: each keeps what was said of it
                    continue
                say(tr(f"{time.strftime('%H:%M')}, trois jeux de suite n'ont pas marché, et {' et '.join(good)}, "
                       f"{'déjà enregistrés, ne marchent' if len(good) > 1 else 'déjà enregistré, ne marche'} plus non "
                       "plus. L'écran est éteint, ArcadeDMD est fermé ou les ROM ne sont plus là. J'attends et je "
                       "regarde toutes les cinq minutes. Je reprends tout seul dès que ça remarche.",
                       f"{time.strftime('%H:%M')}, three games in a row did not work, and {' and '.join(good)}, "
                       f"recorded before, {'do' if len(good) > 1 else 'does'} not work any more either. The screen is "
                       "off, ArcadeDMD is closed or the ROMs are gone. Waiting, and looking every five minutes. The "
                       "tour goes on by itself as soon as it works again."))
                while True:
                    _pause(WAIT)
                    if any(works(client, root, setup, g, cfg_path) for g in good):
                        break
                say(tr(f"{time.strftime('%H:%M')}, ça remarche. Je reprends à {streak[0]}.",
                       f"{time.strftime('%H:%M')}, it works again. Going on from {streak[0]}."))
            elif waits < 2:                                       # no game known to work: waits twice, no more
                waits += 1
                say(tr("Trois jeux de suite n'ont pas marché. L'écran est-il allumé, ArcadeDMD ouvert ? J'attends "
                       "cinq minutes et je les reprends.",
                       "Three games in a row did not work. Is the screen on, ArcadeDMD open? Waiting five minutes, "
                       "then taking them again."))
                _pause(WAIT)
            else:
                streak = []
                continue
            again = list(dict.fromkeys(streak))                   # a game may have failed twice in these three
            for g in again:                                       # not their fault: as if they had not been tried
                tries[g] -= streak.count(g)
                while g in queue:
                    queue.remove(g)
                if g in left:
                    left.remove(g)
                    if tries[g] < 1:
                        aside.discard(g)
            queue.extendleft(reversed(again))
            streak = []
            keep()
        where = "runtime\\robot\\win" if win else "runtime\\robot"
        say(tr(f"Tour fini, {len(fresh)} jeu(x) enregistré(s). Un fichier par jeu dans {where}.",
               f"Tour over, {len(fresh)} game(s) recorded. One file per game in {where}."))
        if left:
            say(tr(f"Laissés de côté, à vérifier (ROM que FinalBurn Neo n'accepte pas ?) : {', '.join(left)}",
                   f"Left aside, to check (a ROM FinalBurn Neo does not take?): {', '.join(left)}"))
        return 0
    except KeyboardInterrupt:
        bat = "robot_win.bat" if win else "robot.bat"
        say(tr(f"Arrêté. Relance {bat} pour reprendre où il en était.", f"Stopped. Run {bat} again to go on where it was."))
        return 0
    finally:
        flag(root, False)
        awake(False)
        client.close()
