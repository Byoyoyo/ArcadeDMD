"""ArcadeDMD : affiche score, vies et crédits des jeux MAME sur une dalle LED 128x32.

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
  python arcadedmd.py setup-ecran      place la fenêtre LED virtuelles sur un écran LCD qui sert de DMD
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

BUSY = ("Le moteur ArcadeDMD tourne déjà en arrière-plan et occupe la dalle. "
        "Ferme-le (Gestionnaire des tâches, pythonw.exe) pour utiliser la dalle ici.")


def test_pattern(cfg, log):
    if app.engine_running():
        log(BUSY)
        return 1
    cfg = dict(cfg)
    cfg["outputs"] = dict(cfg.get("outputs", {}))
    cfg["outputs"]["pixelcade"] = {"enabled": False}
    cfg["outputs"]["zedmd"] = dict(cfg["outputs"].get("zedmd", {}), enabled=True)   # test de la dalle ZeDMD
    outs = app.build_outputs(ROOT, cfg, log, preview=False)
    zed = [o for o in outs if o.__class__.__name__ == "ZeDMDOutput" and o.lib is not None]
    if not zed:
        log("libzedmd n'est pas chargée, voir LISEZMOI (étape libzedmd).")
        return 1
    log("Recherche de la dalle...")
    t_end = time.time() + 15
    while time.time() < t_end and not zed[0].ok:
        time.sleep(0.2)
    if not zed[0].ok:
        log("Dalle non trouvée (voir LISEZMOI, section Dépannage)")
        for o in outs:
            o.close()
        return 1
    log("Dalle connectée, mire pendant 6 secondes")
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
    cv.text(f, "ROUGE", 4, 4, (255, 0, 0))
    cv.text(f, "VERT", 46, 4, (0, 255, 0))
    cv.text(f, "BLEU", 82, 4, (0, 0, 255))
    cv.text(f, "ARCADEDMD %3d" % (k // 25), 22, 18, (255, 255, 255))


def list_serial_ports():
    from dmd.pixelcade import list_ports
    ports = list_ports()
    if not ports:
        print("Aucun port série trouvé (ou module pyserial absent : py -m pip install pyserial).")
        return 1
    print("Ports série :")
    for dev, text, likely in ports:
        print(f"  {dev:8} {text}{'   <- Pixelcade probable' if likely else ''}")
    print("\nLa Pixelcade apparaît souvent comme « Périphérique série USB ». En cas de doute, débranche-la,")
    print("relance ports.bat et regarde quel port a disparu.")
    return 0


def test_pixelcade(cfg, log):
    if app.engine_running():
        log(BUSY)
        return 1
    from dmd.pixelcade import PixelcadeOutput
    pc_cfg = dict(cfg.get("outputs", {}).get("pixelcade", {}))
    pc_cfg["mode"] = "always"
    out = PixelcadeOutput(pc_cfg, ROOT, log)
    t_end = time.time() + 20
    while time.time() < t_end and out.dev is None and out.mode != "off" and not out.failed:
        time.sleep(0.2)
    if out.dev is None:
        log("Pixelcade non trouvée (voir LISEZMOI, section Pixelcade)")
        out.close()
        return 1
    log("Pixelcade connectée, mire pendant 6 secondes")
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
        log(f"Vert et bleu inversés dans config.json (couleurs {order.upper()}). Relance test_pixelcade.bat pour vérifier.")
    elif ok:
        log("Couleurs OK.")
    return 0


def ask_colors_ok():
    """True ou False selon la réponse, None sans console (lancement automatique)."""
    if not (sys.stdin and sys.stdin.isatty()):
        return None
    try:
        ans = input("ROUGE, VERT et BLEU sont-ils chacun de leur couleur sur la Pixelcade ? (O/n) : ")
    except EOFError:
        return None
    return not ans.strip().lower().startswith("n")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "run"
    os.makedirs(os.path.join(ROOT, "runtime"), exist_ok=True)
    log = app.Logger(os.path.join(ROOT, "runtime", "arcadedmd.log"))
    cfg = app.load_config(ROOT, log)

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
        print(("  libzedmd : " + msg))
        return 0 if ok else 1

    if cmd == "install-plugin":
        if len(argv) < 3:
            print(__doc__)
            return 2
        return setup_tools.install_plugin(ROOT, argv[2])

    if cmd == "gif":
        if len(argv) < 4:
            print(__doc__)
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
        print("  Sortie ZeDMD activée dans config.json.")
        return 0

    if cmd == "test-pixelcade":
        return test_pixelcade(cfg, log)

    if cmd == "setup-ecran":
        return setup_tools.configure_screen(ROOT, argv[2] if len(argv) > 2 else None)

    if cmd == "test-retroarch":
        from dmd import radiag
        wait = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 180
        return radiag.run(ROOT, cfg, wait=wait)

    demo = None
    use_zedmd = True
    if cmd == "demo":
        demo = argv[2] if len(argv) > 2 else "aburner2"
        if app.engine_running():
            # le moteur tourne déjà et tient la dalle : on lui demande de jouer la démo
            req = os.path.join(ROOT, "runtime", "demo_request.json")
            with open(req, "w", encoding="utf-8") as f:
                json.dump({"game": demo, "seconds": 20}, f)
            print("ArcadeDMD tourne déjà. La démo passe sur la Pixelcade pendant 20 secondes.")
            time.sleep(5)
            return 0
    elif cmd != "run":
        print(__doc__)
        return 2
    else:
        lock = app.single_instance()
        if lock is None:
            log("ArcadeDMD tourne déjà.")
            return 0
    log(f"ArcadeDMD {app.VERSION} - dossier {ROOT}")
    if not demo:
        from dmd import learned
        learned.restore(ROOT, log)
        learned.complete(ROOT, log)
    if demo:
        pv = dict(cfg["outputs"].get("preview", {}))
        pv.update({"enabled": True, "x": 80, "y": 80, "width": 1024, "height": 256, "borderless": False, "topmost": False})
        cfg["outputs"]["preview"] = pv
    outs = app.build_outputs(ROOT, cfg, log, zedmd=use_zedmd)
    if not demo and not any(o.__class__.__name__ in ("ZeDMDOutput", "PreviewOutput", "PixelcadeOutput") for o in outs):
        log("Aucune sortie active. Active la Pixelcade, la dalle ZeDMD ou la fenêtre LED virtuelles dans config.json")
    eng = app.Engine(ROOT, cfg, outs, log, demo_game=demo)
    eng.run()
    return 0


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
                f.write(time.strftime("%H:%M:%S ") + "ERREUR\n" + msg + "\n")
        except OSError:
            pass
        print(msg, file=sys.stderr)
        sys.exit(1)
