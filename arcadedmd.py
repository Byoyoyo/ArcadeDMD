"""ArcadeDMD: shows the score, lives and credits of MAME and RetroArch games on a 128x32 LED panel.
Entry point of every tool. The command list (help text) is in USAGE_EN and USAGE_FR below.

ArcadeDMD : affiche score, vies et crédits des jeux MAME sur une dalle LED 128x32.
Point d'entrée de tous les outils. La liste des commandes (aide) est dans USAGE_FR et USAGE_EN plus bas.
"""

import json
import os
import sys
import time
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from dmd import app, learn, setup_tools  # noqa: E402
from dmd.canvas import Canvas, Font  # noqa: E402
from dmd.i18n import tr, set_language  # noqa: E402

USAGE_FR = """ArcadeDMD : affiche score, vies et crédits des jeux MAME sur une dalle LED 128x32.

Usage :
  python arcadedmd.py                  moteur normal (attend les jeux lancés dans MAME)
  python arcadedmd.py demo [jeu]       démo avec valeurs simulées (ex. demo aburner2)
  python arcadedmd.py gif jeu fichier.gif [secondes]   enregistre une démo en GIF
  python arcadedmd.py learn [jeu]      outil d'apprentissage des adresses RAM
  python arcadedmd.py test             mire de test sur la dalle
  python arcadedmd.py check-zedmd      vérifie que libzedmd se charge
  python arcadedmd.py install-plugin DOSSIER_MAME   installe le plugin MAME
  python arcadedmd.py ports            liste les ports série (pour trouver la Pixelcade)
  python arcadedmd.py test-pixelcade   mire de test sur la Pixelcade LED
  python arcadedmd.py setup-pixelcade  choisit le port de la Pixelcade et l'active
  python arcadedmd.py enable-zedmd     active la sortie ZeDMD (désactivée par défaut)
  python arcadedmd.py test-retroarch   vérifie RetroArch, le cœur chargé et la lecture de la mémoire
  python arcadedmd.py test-coins       note ce que fait le BIOS Neo Geo quand une pièce entre (RetroArch)
  python arcadedmd.py setup-screen     place la fenêtre LED virtuelles sur un écran LCD qui sert de DMD
"""

USAGE_EN = """ArcadeDMD: shows the score, lives and credits of MAME games on a 128x32 LED panel.

Usage:
  python arcadedmd.py                  normal engine (waits for games started in MAME)
  python arcadedmd.py demo [game]      demo with simulated values (e.g. demo aburner2)
  python arcadedmd.py gif game file.gif [seconds]   records a demo as a GIF
  python arcadedmd.py learn [game]     RAM address learning tool
  python arcadedmd.py test             test pattern on the LED panel
  python arcadedmd.py check-zedmd      checks that libzedmd loads
  python arcadedmd.py install-plugin MAME_FOLDER   installs the MAME plugin
  python arcadedmd.py ports            lists the serial ports (to find the Pixelcade)
  python arcadedmd.py test-pixelcade   test pattern on the Pixelcade LED
  python arcadedmd.py setup-pixelcade  chooses the Pixelcade port and enables it
  python arcadedmd.py enable-zedmd     enables the ZeDMD output (disabled by default)
  python arcadedmd.py test-retroarch   checks RetroArch, the loaded core and memory reading
  python arcadedmd.py test-coins       writes down what the Neo Geo BIOS does when a coin goes in (RetroArch)
  python arcadedmd.py setup-screen     puts the virtual LED window on an LCD screen used as a DMD
"""


def usage():
    return tr(USAGE_FR, USAGE_EN)


def busy():
    return tr("Le moteur ArcadeDMD tourne déjà en arrière-plan et occupe la dalle. "
              "Ferme-le (Gestionnaire des tâches, pythonw.exe) pour utiliser la dalle ici.",
              "The ArcadeDMD engine is already running in the background and is using the LED panel. "
              "Close it (Task Manager, pythonw.exe) to use the panel here.")


def test_pattern(cfg, log):
    if app.engine_running():
        log(busy())
        return 1
    cfg = dict(cfg)
    cfg["outputs"] = dict(cfg.get("outputs", {}))
    cfg["outputs"]["pixelcade"] = {"enabled": False}
    cfg["outputs"]["zedmd"] = dict(cfg["outputs"].get("zedmd", {}), enabled=True)   # test de la dalle ZeDMD
    outs = app.build_outputs(ROOT, cfg, log, preview=False)
    zed = [o for o in outs if o.__class__.__name__ == "ZeDMDOutput" and o.lib is not None]
    if not zed:
        log(tr("libzedmd n'est pas chargée, voir README.fr.md (étape libzedmd).",
               "libzedmd is not loaded, see README.md (libzedmd step)."))
        return 1
    log(tr("Recherche de la dalle...", "Looking for the LED panel..."))
    t_end = time.time() + 15
    while time.time() < t_end and not zed[0].ok:
        time.sleep(0.2)
    if not zed[0].ok:
        log(tr("Dalle non trouvée (voir README.fr.md, section Dépannage)",
               "LED panel not found (see README.md, Troubleshooting section)"))
        for o in outs:
            o.close()
        return 1
    log(tr("Dalle connectée, mire pendant 6 secondes", "LED panel connected, test pattern for 6 seconds"))
    cv = Canvas()
    f = Font.get("6x10")
    for k in range(6 * 25):
        draw_pattern(cv, f, k)
        for o in outs:
            o.send(cv.to_bytes())
        time.sleep(0.04)
    for o in outs:
        o.close()
    return 0


def draw_pattern(cv, f, k):
    cv.clear((0, 0, 0))
    for x in range(128):
        cv.set(x, 0, (255, 0, 0))
        cv.set(x, 31, (0, 0, 255))
    for y in range(32):
        cv.set(0, y, (0, 255, 0))
        cv.set(127, y, (255, 255, 255))
    cv.text(f, tr("ROUGE", "RED"), 4, 4, (255, 0, 0))
    cv.text(f, tr("VERT", "GREEN"), 46, 4, (0, 255, 0))
    cv.text(f, tr("BLEU", "BLUE"), 82, 4, (0, 0, 255))
    cv.text(f, "ARCADEDMD %3d" % (k // 25), 22, 18, (255, 255, 255))


def list_serial_ports():
    from dmd.pixelcade import list_ports
    ports = list_ports()
    if not ports:
        print(tr("Aucun port série trouvé (ou module pyserial absent : py -m pip install pyserial).",
                 "No serial port found (or the pyserial module is missing: py -m pip install pyserial)."))
        return 1
    print(tr("Ports série :", "Serial ports:"))
    for dev, text, likely in ports:
        mark = tr("   <- Pixelcade probable", "   <- probably the Pixelcade") if likely else ""
        print(f"  {dev:8} {text}{mark}")
    print(tr("\nLa Pixelcade apparaît souvent comme « Périphérique série USB ». En cas de doute, débranche-la,",
             "\nThe Pixelcade often shows up as \"USB Serial Device\". If in doubt, unplug it,"))
    print(tr("relance ports.bat et regarde quel port a disparu.",
             "run ports.bat again and see which port has disappeared."))
    return 0


def test_pixelcade(cfg, log):
    if app.engine_running():
        log(busy())
        return 1
    from dmd.pixelcade import PixelcadeOutput
    pc_cfg = dict(cfg.get("outputs", {}).get("pixelcade", {}))
    pc_cfg["mode"] = "always"
    out = PixelcadeOutput(pc_cfg, ROOT, log)
    t_end = time.time() + 20
    while time.time() < t_end and out.dev is None and out.mode != "off" and not out.failed:
        time.sleep(0.2)
    if out.dev is None:
        log(tr("Pixelcade non trouvée (voir README.fr.md, section Pixelcade)",
               "Pixelcade not found (see README.md, Pixelcade section)"))
        out.close()
        return 1
    log(tr("Pixelcade connectée, mire pendant 6 secondes", "Pixelcade connected, test pattern for 6 seconds"))
    cv = Canvas()
    f = Font.get("6x10")
    for k in range(6 * 25):
        draw_pattern(cv, f, k)
        out.send(cv.to_bytes())
        time.sleep(0.04)
    rbg = bool(getattr(out.dev, "rbg", False))
    ok = ask_colors_ok()          # la dernière image reste affichée pendant la question
    out.close()
    if ok is False:
        order = "rgb" if rbg else "rbg"
        setup_tools.set_pixelcade_option(ROOT, "color_order", order)
        log(tr(f"Vert et bleu inversés dans config.json (couleurs {order.upper()}). Relance test_pixelcade.bat pour vérifier.",
               f"Green and blue swapped in config.json (colors {order.upper()}). Run test_pixelcade.bat again to check."))
    elif ok:
        log(tr("Couleurs OK.", "Colors OK."))
    return 0


def ask_colors_ok():
    """True ou False selon la réponse, None sans console (lancement automatique)."""
    if not (sys.stdin and sys.stdin.isatty()):
        return None
    try:
        ans = input(tr("ROUGE, VERT et BLEU sont-ils chacun de leur couleur sur la Pixelcade ? (O/n) : ",
                       "Are RED, GREEN and BLUE each shown in their own color on the Pixelcade? (Y/n): "))
    except EOFError:
        return None
    return not ans.strip().lower().startswith("n")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "run"
    os.makedirs(os.path.join(ROOT, "runtime"), exist_ok=True)
    log = app.Logger(os.path.join(ROOT, "runtime", "arcadedmd.log"))
    cfg = app.load_config(ROOT, log)
    set_language(cfg.get("language"))

    if cmd == "learn":
        hint = argv[2] if len(argv) > 2 else None
        ra = cfg.get("retroarch", {})
        if ra.get("enabled", True):
            from dmd.retroarch import RetroArchClient
            client = RetroArchClient(ra.get("host", "127.0.0.1"), ra.get("port", 55355))
            st = client.status()
            if st and st.get("state") in ("PLAYING", "PAUSED"):
                return learn.run_live_retroarch(ROOT, client, st, hint)
        return learn.run(ROOT, hint)

    if cmd == "check-zedmd":
        dll = cfg.get("outputs", {}).get("zedmd", {}).get("dll") or "libzedmd/zedmd64.dll"
        ok, msg = setup_tools.check_zedmd(ROOT, dll)
        print(tr("  libzedmd : ", "  libzedmd: ") + msg)
        return 0 if ok else 1

    if cmd == "install-plugin":
        if len(argv) < 3:
            print(usage())
            return 2
        return setup_tools.install_plugin(ROOT, argv[2])

    if cmd == "gif":
        if len(argv) < 4:
            print(usage())
            return 2
        seconds = float(argv[4]) if len(argv) > 4 else 12.0
        outs = app.build_outputs(ROOT, cfg, log, preview=False, zedmd=False, gif=argv[3])
        eng = app.Engine(ROOT, cfg, outs, log, demo_game=argv[2])
        eng.run(seconds=seconds)
        return 0

    if cmd == "test":
        return test_pattern(cfg, log)

    if cmd == "ports":
        return list_serial_ports()

    if cmd == "setup-pixelcade":
        return setup_tools.configure_pixelcade(ROOT)

    if cmd == "enable-zedmd":
        setup_tools.set_output_enabled(ROOT, "zedmd", True)
        print(tr("  Sortie ZeDMD activée dans config.json.", "  ZeDMD output enabled in config.json."))
        return 0

    if cmd == "test-pixelcade":
        return test_pixelcade(cfg, log)

    if cmd in ("setup-screen", "setup-ecran"):      # setup-ecran : ancien nom, gardé pour les anciens .bat
        return setup_tools.configure_screen(ROOT, argv[2] if len(argv) > 2 else None)

    if cmd == "test-retroarch":
        from dmd import radiag
        wait = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 180
        return radiag.run(ROOT, cfg, wait=wait)

    if cmd == "test-coins":
        from dmd import coinwatch
        seconds = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 150
        return coinwatch.run(ROOT, cfg, seconds=seconds)

    demo = None
    use_zedmd = True
    if cmd == "demo":
        demo = argv[2] if len(argv) > 2 else "aburner2"
        if app.engine_running():
            # le moteur tourne déjà et tient la dalle : on lui demande de jouer la démo
            req = os.path.join(ROOT, "runtime", "demo_request.json")
            with open(req, "w", encoding="utf-8") as f:
                json.dump({"game": demo, "seconds": 20}, f)
            print(tr("ArcadeDMD tourne déjà. La démo passe sur la Pixelcade pendant 20 secondes.",
                     "ArcadeDMD is already running. The demo plays on the Pixelcade for 20 seconds."))
            time.sleep(5)
            return 0
    elif cmd != "run":
        print(usage())
        return 2
    else:
        lock = app.single_instance()
        if lock is None:
            log(tr("ArcadeDMD tourne déjà.", "ArcadeDMD is already running."))
            return 0
    log(tr(f"ArcadeDMD {app.VERSION} - dossier {ROOT}", f"ArcadeDMD {app.VERSION} - folder {ROOT}"))
    if not demo:
        from dmd import learned
        learned.restore(ROOT, log)
        learned.complete(ROOT, log)
    if demo:
        pv = dict(cfg["outputs"].get("preview", {}))
        pv.update({"enabled": True, "x": 80, "y": 80, "width": 1024, "height": 256, "borderless": False, "topmost": False,
                   "mode": "always"})
        cfg["outputs"]["preview"] = pv
    while True:
        outs = app.build_outputs(ROOT, cfg, log, zedmd=use_zedmd)
        if not demo and not any(o.__class__.__name__ in ("ZeDMDOutput", "PreviewOutput", "PixelcadeOutput") for o in outs):
            log(tr("Aucune sortie active. Active la Pixelcade, la dalle ZeDMD ou la fenêtre LED virtuelles dans config.json",
                   "No active output. Enable the Pixelcade, the ZeDMD panel or the virtual LED window in config.json"))
        eng = app.Engine(ROOT, cfg, outs, log, demo_game=demo)
        if eng.run() != "restart":
            return 0
        cfg = app.load_config(ROOT, log)      # réglages modifiés pendant que le moteur tournait
        set_language(cfg.get("language"))


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except SystemExit:
        raise
    except Exception:
        # sous pythonw il n'y a pas de console : on garde une trace dans le journal
        msg = traceback.format_exc()
        try:
            with open(os.path.join(ROOT, "runtime", "arcadedmd.log"), "a", encoding="utf-8") as f:
                f.write(time.strftime("%H:%M:%S ") + tr("ERREUR", "ERROR") + "\n" + msg + "\n")
        except OSError:
            pass
        print(msg, file=sys.stderr)
        sys.exit(1)
