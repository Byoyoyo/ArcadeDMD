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


def install_plugin(root, mame_dir):
    """Copie le plugin dans MAME\\plugins\\arcadedmd et écrit settings.json."""
    mame_dir = mame_dir.strip().strip('"')
    if mame_dir.lower().endswith(".exe") and os.path.isfile(mame_dir):
        mame_dir = os.path.dirname(mame_dir)      # chemin de mame.exe tapé à la place du dossier
    exe = next((os.path.join(mame_dir, n) for n in ("mame.exe", "mame64.exe")
                if os.path.exists(os.path.join(mame_dir, n))), "")
    if sys.platform == "win32" and not exe:
        print(f"  mame.exe introuvable dans {mame_dir}")
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
    # Avec une Pixelcade, la recherche d'un ZeDMD sur les ports série ne sert à rien
    # et pourrait déranger la Pixelcade ou les pistolets de la borne.
    z = outs.setdefault("zedmd", {})
    zedmd_was_on = bool(z.get("enabled"))
    z["enabled"] = False
    save_config_file(root, cfg)
    print(f"  Pixelcade activée sur {dev}. Lance test_pixelcade.bat pour vérifier les couleurs.")
    if zedmd_was_on:
        print("  Sortie ZeDMD désactivée, inutile avec la Pixelcade.")
        print("  Si tu as aussi un ZeDMD, remets \"enabled\": true dans la rubrique zedmd de config.json.")
    return 0


def load_config_file(root):
    path = os.path.join(root, "config.json")
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
