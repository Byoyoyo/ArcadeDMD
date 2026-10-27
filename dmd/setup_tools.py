"""Helpers for install.bat and the setup commands: libzedmd check, MAME plugin installation,
Pixelcade and DMD screen settings written to config.json.

Aides pour install.bat : vérification de libzedmd et installation du plugin MAME."""

import ctypes
import json
import os
import re
import shutil
import subprocess
import sys

from .i18n import lang, tr


def short_path(path):
    """Chemin court 8.3 (ASCII) sous Windows, sinon le chemin tel quel."""
    if sys.platform != "win32":
        return path
    buf = ctypes.create_unicode_buffer(1024)
    n = ctypes.windll.kernel32.GetShortPathNameW(path, buf, 1024)
    return buf.value if 0 < n < 1024 else path


def check_zedmd(root, dll_rel="libzedmd/zedmd64.dll"):
    """Essaie de charger la DLL et ses dépendances. Retourne (ok, message)."""
    path = dll_rel if os.path.isabs(dll_rel) else os.path.join(root, dll_rel)
    if not os.path.exists(path):
        return False, tr(f"absente ({path})", f"missing ({path})")
    handle = None
    try:
        if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
            handle = os.add_dll_directory(os.path.dirname(os.path.abspath(path)))
        lib = ctypes.CDLL(path)
        for fn in ("ZeDMD_GetInstance", "ZeDMD_Open", "ZeDMD_SetFrameSize", "ZeDMD_RenderRgb888"):
            getattr(lib, fn)
    except (OSError, AttributeError) as e:
        return False, tr(f"chargement impossible : {e}", f"cannot be loaded: {e}")
    finally:
        if handle is not None:
            try:
                handle.close()
            except Exception:
                pass
    return True, "OK"


MIN_MAME = 227     # API Lua « manager.machine » ; avant 0.254 le plugin passe par emu.register_*


def mame_version(exe):
    """Numéro mineur de MAME (264 pour 0.264), ou None si inconnu."""
    try:
        kw = {}
        if sys.platform == "win32":
            kw["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        r = subprocess.run([exe, "-version"], capture_output=True, text=True, timeout=20,
                           cwd=os.path.dirname(exe) or None, **kw)
        m = re.search(r"\b0\.(\d{2,3})\b", (r.stdout or "") + " " + (r.stderr or ""))
        return int(m.group(1)) if m else None
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def find_mame_exe(mame_dir):
    """mame.exe, mame64.exe (versions modifiées pour DOFLinx par exemple), sinon un autre mame*.exe."""
    for n in ("mame.exe", "mame64.exe"):
        p = os.path.join(mame_dir, n)
        if os.path.isfile(p):
            return p
    try:
        names = sorted(os.listdir(mame_dir))
    except OSError:
        return ""
    for n in names:
        low = n.lower()
        if low.startswith("mame") and low.endswith(".exe") and "tool" not in low:
            return os.path.join(mame_dir, n)
    return ""


def install_plugin(root, mame_dir):
    """Copie le plugin dans MAME\\plugins\\arcadedmd et écrit settings.json.
    Ne touche à rien d'autre dans MAME (ni mame.ini, ni plugin.ini)."""
    mame_dir = mame_dir.strip().strip('"')
    if mame_dir.lower().endswith(".exe") and os.path.isfile(mame_dir):
        mame_dir = os.path.dirname(mame_dir)      # chemin de mame.exe tapé à la place du dossier
    exe = find_mame_exe(mame_dir)
    is_mame = bool(exe) or os.path.isfile(os.path.join(mame_dir, "plugins", "boot.lua"))
    if sys.platform == "win32" and not is_mame:
        print(tr(f"  MAME introuvable dans {mame_dir}", f"  MAME not found in {mame_dir}"))
        print(tr("  Il faut le dossier qui contient mame.exe et le sous-dossier plugins.",
                 "  Give the folder that contains mame.exe and the plugins subfolder."))
        return 1
    ver = mame_version(exe) if exe else None
    if ver is not None:
        print(f"  MAME 0.{ver}")
        if ver < MIN_MAME:
            print(tr(f"  Cette version de MAME est trop ancienne pour le plugin. Il faut MAME 0.{MIN_MAME} ou plus récent.",
                     f"  This MAME version is too old for the plugin. MAME 0.{MIN_MAME} or newer is required."))
            print(tr("  Le plugin est installé quand même, mais il ne lira rien tant que MAME n'est pas mis à jour.",
                     "  The plugin is installed anyway, but it will not read anything until MAME is updated."))
    # MAME passe le chemin tel quel à Lua : il doit être en ASCII
    safe_root = root if root.isascii() else short_path(root)
    if not safe_root.isascii():
        print(tr("  Le dossier ArcadeDMD contient des accents ou des caractères spéciaux :",
                 "  The path of the ArcadeDMD folder contains accents or special characters:"))
        print(f"  {root}")
        print(tr("  MAME ne saura pas l'ouvrir. Déplace ArcadeDMD dans un dossier simple, par exemple C:\\ArcadeDMD,",
                 "  MAME will not be able to open it. Move ArcadeDMD to a simple folder, for example C:\\ArcadeDMD,"))
        print(tr("  puis relance install.bat.", "  then run install.bat again."))
        return 2      # install.bat s'arrête au lieu de redemander le dossier de MAME
    src = os.path.join(root, "mame-plugin", "arcadedmd")
    dst = os.path.join(mame_dir, "plugins", "arcadedmd")
    old = {}
    old_settings = os.path.join(dst, "settings.json")
    if os.path.exists(old_settings):
        try:
            with open(old_settings, "r", encoding="utf-8") as f:
                old = json.load(f)
        except (OSError, ValueError):
            old = {}
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True)
    settings = {
        "root": safe_root.replace("\\", "/"),
        "capture_key": old.get("capture_key", "KEYCODE_RCONTROL KEYCODE_D"),
        "poll_frames": old.get("poll_frames", 2),
        "heartbeat_seconds": old.get("heartbeat_seconds", 2),
        "language": lang(),          # language of the plugin messages and menu (config.json "language" wins)
    }
    with open(os.path.join(dst, "settings.json"), "w", encoding="ascii") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")
    print(tr(f"  Plugin installé dans {dst}", f"  Plugin installed in {dst}"))
    if safe_root != root:
        print(tr(f"  (chemin court utilisé pour MAME : {safe_root})", f"  (short path used for MAME: {safe_root})"))
    return 0


def configure_pixelcade(root):
    """Active la sortie Pixelcade dans config.json après avoir choisi le port COM."""
    from .pixelcade import list_ports
    ports = list_ports()
    if not ports:
        print(tr("  Aucun port série visible (Pixelcade débranchée, ou pyserial absent).",
                 "  No serial port visible (Pixelcade unplugged, or pyserial missing)."))
        return 1
    print(tr("  Ports série :", "  Serial ports:"))
    for i, (dev, text, likely) in enumerate(ports, 1):
        mark = tr("   <- Pixelcade probable", "   <- probably the Pixelcade") if likely else ""
        print(f"   {i}. {dev:8} {text}{mark}")
    guess = next((d for d, _, likely in ports if likely), "")
    try:
        ans = input(tr(f"  Port de la Pixelcade (numéro ou nom{', Entrée = ' + guess if guess else ''}) : ",
                       f"  Pixelcade port (number or name{', Enter = ' + guess if guess else ''}): ")).strip()
    except EOFError:
        ans = ""
    if ans.isdigit() and 0 < int(ans) <= len(ports):
        dev = ports[int(ans) - 1][0]
    else:
        dev = ans or guess
    if not dev:
        print(tr("  Aucun port choisi, Pixelcade non activée.", "  No port chosen, Pixelcade not enabled."))
        return 1
    cfg = load_config_file(root)
    outs = cfg.setdefault("outputs", {})
    pc = outs.setdefault("pixelcade", {})
    pc.update({"enabled": True, "device": dev})
    for k, v in (("color_order", "auto"), ("mode", "games"), ("takeover", "known"), ("max_fps", 30),
                 ("pixelweb_url", "http://127.0.0.1:8080"), ("pixelweb_exe", ""), ("art_dir", "")):
        pc.setdefault(k, v)
    # la sortie ZeDMD reste comme l'a réglée l'étape 2 de l'installeur (désactivée par défaut)
    save_config_file(root, cfg)
    print(tr(f"  Pixelcade activée sur {dev}. Lance test_pixelcade.bat pour vérifier les couleurs.",
             f"  Pixelcade enabled on {dev}. Run test_pixelcade.bat to check the colors."))
    return 0


def set_output_enabled(root, name, flag):
    cfg = load_config_file(root)
    cfg.setdefault("outputs", {}).setdefault(name, {})["enabled"] = bool(flag)
    save_config_file(root, cfg)


def load_config_file(root):
    """config.json (tes réglages), sinon les valeurs de départ de config.default.json
    (ou de config.defaut.json, son ancien nom)."""
    for name in ("config.json", "config.default.json", "config.defaut.json"):
        path = os.path.join(root, name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}


def save_config_file(root, cfg):
    path = os.path.join(root, "config.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def set_pixelcade_option(root, key, value):
    cfg = load_config_file(root)
    cfg.setdefault("outputs", {}).setdefault("pixelcade", {})[key] = value
    save_config_file(root, cfg)


def configure_screen(root, answer=None, style_answer=None):
    """Place la fenêtre « LED virtuelles » sur l'écran choisi (LCD qui sert de DMD) dans config.json."""
    from .screens import guess_dmd, list_screens
    screens = list_screens()
    if not screens:
        print(tr("  Aucun écran trouvé (cette commande ne marche que sous Windows).",
                 "  No screen found (this command only works on Windows)."))
        return 1
    print(tr("  Écrans branchés :", "  Connected screens:"))
    for i, sc in enumerate(screens, 1):
        tag = tr("   écran principal", "   main screen") if sc["primary"] else ""
        print(f"   {i}. {sc['width']} x {sc['height']}, position {sc['x']}, {sc['y']}{tag}")
    g = guess_dmd(screens)
    hint = tr(f", Entrée = {g + 1}", f", Enter = {g + 1}") if g is not None else ""
    if answer is None:
        try:
            answer = input(tr(f"  Numéro de l'écran qui sert de DMD (0 pour n'en mettre aucun{hint}) : ",
                              f"  Number of the screen used as DMD (0 for none{hint}): ")).strip()
        except EOFError:
            answer = ""
    if answer == "" and g is not None:
        idx = g
    elif answer.isdigit() and 0 < int(answer) <= len(screens):
        idx = int(answer) - 1
    else:
        cfg = load_config_file(root)
        cfg.setdefault("outputs", {}).setdefault("preview", {})["enabled"] = False
        save_config_file(root, cfg)
        print(tr("  Pas d'écran DMD, fenêtre LED virtuelles coupée.", "  No DMD screen, virtual LED window turned off."))
        return 0
    sc = screens[idx]
    size = f"{sc['width']} x {sc['height']}"
    cfg = load_config_file(root)
    pv = cfg.setdefault("outputs", {}).setdefault("preview", {})
    pv.update({"enabled": True, "x": sc["x"], "y": sc["y"], "width": sc["width"], "height": sc["height"],
               "borderless": True, "topmost": True, "mode": "games"})
    pv.setdefault("hd", "auto")
    pv.setdefault("style", "led")
    cur = "HD" if str(pv.get("style")).lower() == "hd" else "LED"
    if style_answer is None:
        try:
            style_answer = input(tr(f"  Affichage. 1 = LED virtuelles, comme une vraie dalle. 2 = HD lisse, avec le logo du jeu "
                                    f"(Entrée = garder {cur}) : ",
                                    f"  Display. 1 = virtual LEDs, like a real LED panel. 2 = smooth HD, with the game logo "
                                    f"(Enter = keep {cur}): ")).strip()
        except EOFError:
            style_answer = ""
    if style_answer == "2":
        pv["style"] = "hd"
    elif style_answer == "1":
        pv["style"] = "led"
    save_config_file(root, cfg)
    if str(pv.get("style")).lower() == "hd":
        print(tr(f"  Affichage HD lisse sur l'écran {idx + 1} ({size}). Le logo de chaque jeu vient de "
                 "tes images Clear Logo de LaunchBox.",
                 f"  Smooth HD display on screen {idx + 1} ({size}). Each game's logo comes from "
                 "your LaunchBox Clear Logo images."))
        print(tr("  Lance demo_fight.bat pour voir le résultat, ou un jeu depuis BigBox.",
                 "  Run demo_fight.bat to see the result, or start a game from BigBox."))
        return 0
    from .outputs import hd_factor
    f = hd_factor(pv, sc["width"], sc["height"])
    finesse = (tr(f"{128 * f} x {32 * f} LED", f"{128 * f} x {32 * f} LEDs")
               + (tr(", deux fois plus fin qu'une vraie dalle", ", twice as fine as a real LED panel") if f == 2 else ""))
    print(tr(f"  Fenêtre LED virtuelles sur l'écran {idx + 1} ({size}), {finesse}.",
             f"  Virtual LED window on screen {idx + 1} ({size}), {finesse}."))
    print(tr("  Lance run.bat ou demo_afterburner.bat pour voir le résultat.",
             "  Launch run.bat or demo_afterburner.bat to see the result."))
    return 0
