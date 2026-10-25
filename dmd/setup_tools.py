"""Aides pour installer.bat : vérification de libzedmd et installation du plugin MAME."""

import ctypes
import json
import os
import re
import shutil
import subprocess
import sys


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
        return False, f"absente ({path})"
    handle = None
    try:
        if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
            handle = os.add_dll_directory(os.path.dirname(os.path.abspath(path)))
        lib = ctypes.CDLL(path)
        for fn in ("ZeDMD_GetInstance", "ZeDMD_Open", "ZeDMD_SetFrameSize", "ZeDMD_RenderRgb888"):
            getattr(lib, fn)
    except (OSError, AttributeError) as e:
        return False, f"chargement impossible : {e}"
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
        print(f"  MAME introuvable dans {mame_dir}")
        print("  Il faut le dossier qui contient mame.exe et le sous-dossier plugins.")
        return 1
    ver = mame_version(exe) if exe else None
    if ver is not None:
        print(f"  MAME 0.{ver}")
        if ver < MIN_MAME:
            print(f"  Cette version de MAME est trop ancienne pour le plugin. Il faut MAME 0.{MIN_MAME} ou plus récent.")
            print("  Le plugin est installé quand même, mais il ne lira rien tant que MAME n'est pas mis à jour.")
    # MAME passe le chemin tel quel à Lua : il doit être en ASCII
    safe_root = root if root.isascii() else short_path(root)
    if not safe_root.isascii():
        print("  Le dossier ArcadeDMD contient des accents ou des caractères spéciaux :")
        print(f"  {root}")
        print("  MAME ne saura pas l'ouvrir. Déplace ArcadeDMD dans un dossier simple, par exemple C:\\ArcadeDMD,")
        print("  puis relance installer.bat.")
        return 2      # installer.bat s'arrête au lieu de redemander le dossier de MAME
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
    }
    with open(os.path.join(dst, "settings.json"), "w", encoding="ascii") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")
    print(f"  Plugin installé dans {dst}")
    if safe_root != root:
        print(f"  (chemin court utilisé pour MAME : {safe_root})")
    return 0


def configure_pixelcade(root):
    """Active la sortie Pixelcade dans config.json après avoir choisi le port COM."""
    from .pixelcade import list_ports
    ports = list_ports()
    if not ports:
        print("  Aucun port série visible (Pixelcade débranchée, ou pyserial absent).")
        return 1
    print("  Ports série :")
    for i, (dev, text, likely) in enumerate(ports, 1):
        print(f"   {i}. {dev:8} {text}{'   <- Pixelcade probable' if likely else ''}")
    guess = next((d for d, _, likely in ports if likely), "")
    try:
        ans = input(f"  Port de la Pixelcade (numéro ou nom{', Entrée = ' + guess if guess else ''}) : ").strip()
    except EOFError:
        ans = ""
    if ans.isdigit() and 0 < int(ans) <= len(ports):
        dev = ports[int(ans) - 1][0]
    else:
        dev = ans or guess
    if not dev:
        print("  Aucun port choisi, Pixelcade non activée.")
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
    print(f"  Pixelcade activée sur {dev}. Lance test_pixelcade.bat pour vérifier les couleurs.")
    return 0


def set_output_enabled(root, name, flag):
    cfg = load_config_file(root)
    cfg.setdefault("outputs", {}).setdefault(name, {})["enabled"] = bool(flag)
    save_config_file(root, cfg)


def load_config_file(root):
    """config.json (tes réglages), sinon les valeurs de départ de config.defaut.json."""
    for name in ("config.json", "config.defaut.json"):
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


def configure_screen(root, answer=None):
    """Place la fenêtre « LED virtuelles » sur l'écran choisi (LCD qui sert de DMD) dans config.json."""
    from .screens import guess_dmd, list_screens
    screens = list_screens()
    if not screens:
        print("  Aucun écran trouvé (cette commande ne marche que sous Windows).")
        return 1
    print("  Écrans branchés :")
    for i, sc in enumerate(screens, 1):
        tag = "   écran principal" if sc["primary"] else ""
        print(f"   {i}. {sc['width']} x {sc['height']}, position {sc['x']}, {sc['y']}{tag}")
    g = guess_dmd(screens)
    hint = f", Entrée = {g + 1}" if g is not None else ""
    if answer is None:
        try:
            answer = input(f"  Numéro de l'écran qui sert de DMD (0 pour n'en mettre aucun{hint}) : ").strip()
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
        print("  Pas d'écran DMD, fenêtre LED virtuelles coupée.")
        return 0
    sc = screens[idx]
    cfg = load_config_file(root)
    pv = cfg.setdefault("outputs", {}).setdefault("preview", {})
    pv.update({"enabled": True, "x": sc["x"], "y": sc["y"], "width": sc["width"], "height": sc["height"],
               "borderless": True, "topmost": True})
    pv.setdefault("hd", "auto")
    pv.setdefault("style", "led")
    save_config_file(root, cfg)
    from .outputs import hd_factor
    f = hd_factor(pv, sc["width"], sc["height"])
    finesse = f"{128 * f} x {32 * f} LED" + (", deux fois plus fin qu'une vraie dalle" if f == 2 else "")
    print(f"  Fenêtre LED virtuelles sur l'écran {idx + 1} ({sc['width']} x {sc['height']}), {finesse}.")
    print("  Lance lancer.bat ou demo_afterburner.bat pour voir le résultat.")
    return 0
