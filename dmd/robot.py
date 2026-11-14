"""The robot: the games play by themselves so that their memory is recorded (1.39).

RetroArch takes the buttons of a pad from the network (its "Network RetroPad": one UDP port per player from 55400, the
settings network_remote_enable and network_remote_enable_user_p1, a message of 20 bytes per button). The robot starts
RetroArch with a game, puts a coin, presses START, plays at random for a few minutes, closes the game and goes on with
the next one. ArcadeDMD, running beside it with its full recording on, records each game as it does for a game played
by hand (runtime/captures). Nothing of RetroArch is changed: its settings for the robot are in a file of ArcadeDMD
(runtime/robot.cfg) given on its command line.

  python arcadedmd.py robot-test          one game, two minutes: does RetroArch take the buttons the robot sends?
  python arcadedmd.py robot [MINUTES]     every game whose ROM is in the folder, MINUTES each (6 by default)

Le robot : les jeux jouent tout seuls pour que leur mémoire soit enregistrée. RetroArch accepte les boutons d'une
manette par le réseau. Le robot lance RetroArch avec un jeu, met une pièce, appuie sur START, joue au hasard quelques
minutes, ferme le jeu et passe au suivant. ArcadeDMD, lancé à côté avec son enregistrement complet, enregistre chaque
partie comme une partie jouée à la main. Rien n'est changé dans RetroArch : ses réglages pour le robot sont dans un
fichier d'ArcadeDMD donné sur sa ligne de commande."""
import collections
import json
import os
import random
import socket
import struct
import subprocess
import threading
import time

from .i18n import tr
from .retroarch import RetroArchClient, layout_for

JOYPAD = 1                                    # RETRO_DEVICE_JOYPAD
B, Y, SELECT, START, UP, DOWN, LEFT, RIGHT, A, X, L, R = range(12)      # RETRO_DEVICE_ID_JOYPAD_*
ACTIONS = (B, A, Y, X, L, R)
BASE_PORT = 55400
PACE = 0.018                                  # a little slower than the images / un peu moins vite que les images
CFG = """network_remote_enable = "true"
network_remote_enable_user_p1 = "true"
network_remote_enable_user_p2 = "true"
network_remote_base_port = "%d"
network_cmd_enable = "true"
pause_nonactive = "false"
quit_press_twice = "false"
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


def write_cfg(root, base=BASE_PORT):
    path = os.path.join(root, "runtime", "robot.cfg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(CFG % base)
    return path


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
        if core and rom:
            return {"exe": exe, "core": core, "rom_dir": os.path.dirname(rom), "ext": os.path.splitext(rom)[1] or ".zip",
                    "last": content}
    return None


def launch(setup, rom, cfg_path):
    """Starts RetroArch with this game and the robot's settings on top of its own. / Lance RetroArch avec ce jeu."""
    path = os.path.join(setup["rom_dir"], rom + setup.get("ext", ".zip"))
    args = [setup["exe"], "-L", setup["core"], "--appendconfig", cfg_path]
    if setup.get("fullscreen", True):
        args.append("-f")
    args.append(path)
    return subprocess.Popen(args, cwd=os.path.dirname(setup["exe"]) or None,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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


def play(client, seconds, rng, base=BASE_PORT, two_from=0.7, alive=None, tick=None):
    """Plays the game that runs: a coin, START, then at random; a second player joins for the last part. Returns False
    when RetroArch stopped answering. / Joue le jeu en cours : une pièce, START, puis au hasard."""
    p1, p2 = RemotePad(1, base=base), RemotePad(2, base=base)
    one, two = Player(p1, rng), Player(p2, rng)
    t0 = time.monotonic()
    coin_t = seen_t = t0
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
            one.step(now)
            if now - t0 >= seconds * two_from:                    # the second player joins / le deuxième joueur arrive
                if not joined:
                    joined = True
                    p2.tap(SELECT, 0.15)
                    time.sleep(0.5)
                    p2.tap(START, 0.15)
                two.step(now)
            if now - seen_t >= 5.0:
                seen_t = now
                st = client.status()
                if not st or st.get("state") not in ("PLAYING", "PAUSED") or (alive is not None and not alive()):
                    ok = False
                    break
                if tick is not None:
                    tick(now - t0)
            time.sleep(0.015)
    finally:
        p1.close()
        p2.close()
    return ok


def inputs_seen(client, st):
    """Neo Geo: does the BIOS see the stick the robot holds? True, False, or None when it cannot be told (another
    system). / Le BIOS voit-il le stick que tient le robot ?"""
    lay = layout_for(None, st.get("system") or "")
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


def roms(root, setup):
    """The games of ArcadeDMD whose ROM is in the folder, the fighting games first. / Les jeux dont la ROM est là."""
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
    return [k for _, k in sorted(out)]


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


def _recording_note(cfg, say):
    ra = cfg.get("retroarch", {}) or {}
    dump = ra.get("ram_dump") if isinstance(ra.get("ram_dump"), dict) else {}
    if not dump.get("enabled"):
        say(tr("Attention, l'enregistrement de la mémoire est coupé dans ArcadeDMD. Coche « Toute la mémoire de "
               "RetroArch » dans sa fenêtre (Enregistrer les parties) avant le grand tour.",
               "Warning, the memory recording is off in ArcadeDMD. Tick \"The whole RetroArch memory\" in its window "
               "(Record the games) before the full tour."))


def test(root, cfg, wait=300, seconds=120, out=print):
    """One game, two minutes: RetroArch started by the robot, the buttons it sends seen by the game, the recording
    written by ArcadeDMD. / Un jeu, deux minutes : la chaîne complète vérifiée."""
    say = Report(root, "robot_test.txt", out)
    say(tr("Essai du robot", "Robot test"))
    client = _client(cfg)
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
        proc = launch(setup, rom, write_cfg(root))
        st = wait_playing(client, 60, proc)
        if st is None:
            say(tr("RetroArch n'a pas démarré le jeu en une minute. Essai arrêté.",
                   "RetroArch did not start the game within a minute. Test stopped."))
            close_game(client, proc)
            return 1
        say(tr(f"Le jeu tourne ({st.get('content')}).", f"The game runs ({st.get('content')})."))
        time.sleep(6.0)
        seen = inputs_seen(client, st)
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
        say(tr(f"Je joue {seconds // 60} minutes. Regarde l'écran : une pièce, START, puis le personnage bouge tout seul.",
               f"Playing for {seconds // 60} minutes. Watch the screen: a coin, START, then the character moves alone."))
        ok = play(client, seconds, random.Random(), alive=lambda: proc.poll() is None)
        say(tr("Partie finie, je ferme le jeu.", "Game over, closing it.") if ok
            else tr("RetroArch s'est arrêté pendant la partie.", "RetroArch stopped during the game."))
        close_game(client, proc)
        time.sleep(2.0)
        files = _recorded(root, since)
        if files:
            say(tr(f"Enregistré par ArcadeDMD : {', '.join(files)}", f"Recorded by ArcadeDMD: {', '.join(files)}"))
        else:
            say(tr("ArcadeDMD n'a rien enregistré pendant l'essai. Est-il lancé ?",
                   "ArcadeDMD recorded nothing during the test. Is it running?"))
        _recording_note(cfg, say)
        say(tr("Envoie-moi runtime\\robot_test.txt.", "Send me runtime\\robot_test.txt."))
        return 0 if seen is not False and ok else 1
    finally:
        client.close()


def tour(root, cfg, minutes=6, only=None, out=print):
    """Every game whose ROM is in the folder, a few minutes each. Ctrl+C stops it; started again, it goes on where it
    stopped. / Tous les jeux dont la ROM est là, quelques minutes chacun. Relancé, il reprend où il s'est arrêté."""
    say = Report(root, "robot.txt", out)
    setup = load_setup(root)
    if setup is None:
        say(tr("Lance d'abord robot_test.bat, il apprend où sont RetroArch et les ROM.",
               "Run robot_test.bat first, it learns where RetroArch and the ROMs are."))
        return 1
    games = [g for g in roms(root, setup) if not only or g in only]
    done = set(setup.get("done") or []) if not only else set()
    todo = [g for g in games if g not in done]
    if not todo and games:
        done, todo = set(), games                                 # all done: a new tour / tout est fait : un nouveau tour
    total = len(todo) * (minutes + 0.7)
    long_fr = f"{total / 60:.1f} heures" if total >= 90 else f"{total:.0f} minutes"
    long_en = f"{total / 60:.1f} hours" if total >= 90 else f"{total:.0f} minutes"
    say(tr(f"Tour du robot : {len(todo)} jeu(x), {minutes} minute(s) chacun, environ {long_fr}. Ctrl+C pour arrêter.",
           f"Robot tour: {len(todo)} game(s), {minutes} minute(s) each, about {long_en}. Ctrl+C to stop."))
    _recording_note(cfg, say)
    client = _client(cfg)
    cfg_path = write_cfg(root)
    rng = random.Random()
    proc = None
    try:
        if client.status() is not None:
            say(tr("RetroArch tourne déjà, je le ferme.", "RetroArch is already running, closing it."))
            close_game(client)
            time.sleep(3.0)
        for i, rom in enumerate(todo, 1):
            since = time.time()
            proc = launch(setup, rom, cfg_path)
            st = wait_playing(client, 45, proc)
            if st is None:
                say(tr(f"{i}/{len(todo)} {rom} : ne démarre pas, je passe au suivant",
                       f"{i}/{len(todo)} {rom}: does not start, going on with the next"))
                close_game(client, proc, 6.0)
            else:
                ok = play(client, minutes * 60, rng, alive=lambda: proc.poll() is None)
                close_game(client, proc)
                files = _recorded(root, since)
                say(tr(f"{i}/{len(todo)} {rom} : {'joué' if ok else 'arrêté avant la fin'}, {len(files)} fichier(s) enregistré(s)",
                       f"{i}/{len(todo)} {rom}: {'played' if ok else 'stopped early'}, {len(files)} file(s) recorded"))
            proc = None
            done.add(rom)
            if not only:
                setup["done"] = sorted(done)
                save_setup(root, setup)
            time.sleep(3.0)
        say(tr("Tour fini. Les enregistrements sont dans runtime\\captures.",
               "Tour over. The recordings are in runtime\\captures."))
        return 0
    except KeyboardInterrupt:
        say(tr("Arrêté. Relance robot.bat pour reprendre où il en était.",
               "Stopped. Run robot.bat again to go on where it was."))
        if proc is not None:
            close_game(client, proc, 6.0)
        return 0
    finally:
        client.close()
