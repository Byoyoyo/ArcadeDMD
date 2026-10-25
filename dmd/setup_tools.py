"""Aides pour installer.bat : vérification de libzedmd et installation du plugin MAME."""

import ctypes
import json
import os
import shutil
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


def install_plugin(root, mame_dir):
    """Copie le plugin dans MAME\\plugins\\arcadedmd et écrit settings.json."""
    mame_dir = mame_dir.strip().strip('"')
    exe = os.path.join(mame_dir, "mame.exe")
    if sys.platform == "win32" and not os.path.exists(exe):
        print(f"  mame.exe introuvable dans {mame_dir}")
        return 1
    # MAME passe le chemin tel quel à Lua : il doit être en ASCII
    safe_root = root if root.isascii() else short_path(root)
    if not safe_root.isascii():
        print("  Le dossier ArcadeDMD contient des accents ou des caractères spéciaux :")
        print(f"  {root}")
        print("  MAME ne saura pas l'ouvrir. Déplace ArcadeDMD dans un dossier simple, par exemple C:\\ArcadeDMD,")
        print("  puis relance installer.bat.")
        return 1
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
    path = os.path.join(root, "config.json")
    cfg = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    outs = cfg.setdefault("outputs", {})
    pc = outs.setdefault("pixelcade", {})
    pc.update({"enabled": True, "device": dev})
    for k, v in (("color_order", "auto"), ("mode", "games"), ("takeover", "known"), ("max_fps", 30),
                 ("pixelweb_url", "http://127.0.0.1:8080"), ("pixelweb_exe", ""), ("art_dir", "")):
        pc.setdefault(k, v)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Pixelcade activée sur {dev}. Lance test_pixelcade.bat pour vérifier les couleurs.")
    return 0
