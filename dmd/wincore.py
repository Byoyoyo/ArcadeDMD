"""Which RetroArch core is loaded? (Windows)

Reads the list of DLLs loaded by retroarch.exe, or else RetroArch's content history. Changes nothing.

Quel cœur RetroArch est chargé ? (Windows)

GET_STATUS ne donne qu'un identifiant de système. « fb_alpha » vaut aussi bien pour
FinalBurn Neo que pour les cœurs FB Alpha 2012, qui ne donnent pas leur mémoire.
On lit donc la liste des DLL chargées par retroarch.exe (comme le Gestionnaire des tâches),
et à défaut l'historique de RetroArch (playlists/builtin/content_history.lpl).
Rien n'est modifié, ni dans RetroArch ni ailleurs.
"""

import ctypes
import json
import os
import re
import sys
import time

from .i18n import tr

# nom du fichier sans extension -> (nom lisible, donne sa mémoire à RetroArch)
CORES = {
    "fbneo_libretro": ("FinalBurn Neo", True),
    "fbalpha2012_libretro": ("FB Alpha 2012", False),
    "fbalpha2012_neogeo_libretro": ("FB Alpha 2012 Neo Geo", False),
    "fbalpha2012_cps1_libretro": ("FB Alpha 2012 CPS-1", False),
    "fbalpha2012_cps2_libretro": ("FB Alpha 2012 CPS-2", False),
    "fbalpha2012_cps3_libretro": ("FB Alpha 2012 CPS-3", False),
    "fbalpha_libretro": ("FB Alpha", None),
    "mame2000_libretro": ("MAME 2000", False),
    "mame2003_libretro": ("MAME 2003", False),
    "mame2003_plus_libretro": ("MAME 2003-Plus", False),
    "mame2003_midway_libretro": ("MAME 2003 Midway", False),
    "mame2010_libretro": ("MAME 2010", False),
    "mame2015_libretro": ("MAME 2015", False),
    "mame2016_libretro": ("MAME 2016", False),
    "mame_libretro": ("MAME", False),
    "genesis_plus_gx_libretro": ("Genesis Plus GX", True),
    "genesis_plus_gx_wide_libretro": ("Genesis Plus GX Wide", True),
    "picodrive_libretro": ("PicoDrive", True),
    "flycast_libretro": ("Flycast", True),
    "flycast_gles2_libretro": ("Flycast GLES2", True),
}


def _day(ts):
    return time.strftime(tr("%d/%m/%Y", "%Y-%m-%d"), time.localtime(ts))


def pe_build_time(path):
    """Date de compilation inscrite dans l'en-tête de la DLL, ou None si absente ou invraisemblable."""
    try:
        with open(path, "rb") as f:
            head = f.read(0x40)
            if len(head) < 0x40 or head[:2] != b"MZ":
                return None
            f.seek(int.from_bytes(head[0x3C:0x40], "little"))
            pe = f.read(12)
    except (OSError, ValueError):
        return None
    if len(pe) < 12 or pe[:4] != b"PE\0\0":
        return None
    ts = int.from_bytes(pe[8:12], "little")
    if not 1262304000 <= ts <= time.time() + 86400:     # entre 2010 et demain
        return None
    return ts


def describe(path):
    """{"path", "file", "name", "memory", "date"} pour le fichier d'un cœur."""
    file = os.path.basename(path.replace("\\", "/"))
    stem = file.lower()
    for ext in (".dll", ".so", ".dylib"):
        if stem.endswith(ext):
            stem = stem[:-len(ext)]
            break
    name, mem = CORES.get(stem, (None, None))
    if name is None:
        if stem.startswith("fbalpha2012"):
            name, mem = "FB Alpha 2012", False
        elif stem.startswith("fbneo"):
            name, mem = "FinalBurn Neo", True
        elif stem.startswith("mame"):
            name, mem = "MAME", False
        else:
            name = file
    date = ""
    ts = pe_build_time(path)
    if ts:
        date = tr("compilé le ", "built on ") + _day(ts)
    else:
        try:
            date = tr("fichier du ", "file dated ") + _day(os.path.getmtime(path))
        except OSError:
            pass
    return {"path": path, "file": file, "name": name, "memory": mem, "date": date}


def read_cfg(path):
    """Réglages « clé = "valeur" » d'un retroarch.cfg (dictionnaire vide si illisible)."""
    out = {}
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r'\s*([A-Za-z0-9_]+)\s*=\s*"(.*)"\s*$', line)
                if m:
                    out[m.group(1)] = m.group(2)
    except OSError:
        pass
    return out


def _resolve(radir, p):
    p = (p or "").strip()
    if p[:2] in (":\\", ":/"):
        p = os.path.join(radir, p[2:])
    return p


def history_files(radir):
    cfg = read_cfg(os.path.join(radir, "retroarch.cfg"))
    paths = []
    hdir = cfg.get("content_history_directory", "")
    if hdir and hdir != "default":
        paths.append(os.path.join(_resolve(radir, hdir), "content_history.lpl"))
    pdir = cfg.get("playlist_directory", "")
    if pdir and pdir != "default":
        paths.append(os.path.join(_resolve(radir, pdir), "builtin", "content_history.lpl"))
    paths.append(os.path.join(radir, "playlists", "builtin", "content_history.lpl"))
    paths.append(os.path.join(radir, "content_history.lpl"))
    return paths


def core_from_history(radir, content=""):
    """Chemin du cœur utilisé pour content d'après l'historique de RetroArch, ou ""."""
    want = (content or "").lower()
    for p in history_files(radir):
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                items = json.load(f).get("items") or []
        except (OSError, ValueError, AttributeError):
            continue
        for it in items:
            if not isinstance(it, dict):
                continue
            core = it.get("core_path") or ""
            if not core or core in ("DETECT", "builtin"):
                continue
            stem = os.path.splitext(os.path.basename((it.get("path") or "").replace("\\", "/")))[0].lower()
            if not want or stem == want:
                return core
    return ""


# --------------------------------------------------------------------------
# liste des processus et des DLL (API Toolhelp32 de Windows)
# --------------------------------------------------------------------------

if sys.platform == "win32":
    from ctypes import wintypes

    TH32CS_SNAPPROCESS = 0x2
    TH32CS_SNAPMODULE = 0x8
    TH32CS_SNAPMODULE32 = 0x10
    ERROR_BAD_LENGTH = 24
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    INVALID_HANDLE = ctypes.c_void_p(-1).value

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_size_t),
                    ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD), ("szExeFile", wintypes.WCHAR * 260)]

    class MODULEENTRY32W(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("th32ModuleID", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD), ("GlblcntUsage", wintypes.DWORD),
                    ("ProccntUsage", wintypes.DWORD), ("modBaseAddr", ctypes.c_void_p),
                    ("modBaseSize", wintypes.DWORD), ("hModule", wintypes.HMODULE),
                    ("szModule", wintypes.WCHAR * 256), ("szExePath", wintypes.WCHAR * 260)]

    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _snapshot = _k32.CreateToolhelp32Snapshot
    _snapshot.argtypes = (wintypes.DWORD, wintypes.DWORD)
    _snapshot.restype = wintypes.HANDLE
    _p_first, _p_next = _k32.Process32FirstW, _k32.Process32NextW
    for _fn in (_p_first, _p_next):
        _fn.argtypes = (wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W))
        _fn.restype = wintypes.BOOL
    _m_first, _m_next = _k32.Module32FirstW, _k32.Module32NextW
    for _fn in (_m_first, _m_next):
        _fn.argtypes = (wintypes.HANDLE, ctypes.POINTER(MODULEENTRY32W))
        _fn.restype = wintypes.BOOL
    _close = _k32.CloseHandle
    _close.argtypes = (wintypes.HANDLE,)
    _close.restype = wintypes.BOOL
    _open = _k32.OpenProcess
    _open.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    _open.restype = wintypes.HANDLE
    _image_name = _k32.QueryFullProcessImageNameW
    _image_name.argtypes = (wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD))
    _image_name.restype = wintypes.BOOL

    def _valid(h):
        return bool(h) and h != INVALID_HANDLE

    def retroarch_processes():
        """[(pid, nom)] des processus retroarch*.exe."""
        h = _snapshot(TH32CS_SNAPPROCESS, 0)
        if not _valid(h):
            return []
        out = []
        try:
            e = PROCESSENTRY32W()
            e.dwSize = ctypes.sizeof(e)
            ok = _p_first(h, ctypes.byref(e))
            while ok:
                low = e.szExeFile.lower()
                if low.startswith("retroarch") and low.endswith(".exe"):
                    out.append((int(e.th32ProcessID), e.szExeFile))
                ok = _p_next(h, ctypes.byref(e))
        finally:
            _close(h)
        return out

    def process_modules(pid):
        """(chemin de l'exe, [DLL *_libretro.dll]) ou None si Windows refuse (RetroArch lancé en administrateur...)."""
        h = None
        for _ in range(5):
            h = _snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
            if _valid(h):
                break
            if ctypes.get_last_error() != ERROR_BAD_LENGTH:     # liste en cours de changement : on réessaie
                return None
            time.sleep(0.05)
        if not _valid(h):
            return None
        exe, cores = "", []
        try:
            m = MODULEENTRY32W()
            m.dwSize = ctypes.sizeof(m)
            ok = _m_first(h, ctypes.byref(m))
            while ok:
                path = m.szExePath
                if not exe and path.lower().endswith(".exe"):
                    exe = path
                if m.szModule.lower().endswith("_libretro.dll"):
                    cores.append(path)
                ok = _m_next(h, ctypes.byref(m))
        finally:
            _close(h)
        return exe, cores

    def image_path(pid):
        h = _open(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not _valid(h):
            return ""
        try:
            buf = ctypes.create_unicode_buffer(32768)
            n = wintypes.DWORD(len(buf))
            if _image_name(h, 0, buf, ctypes.byref(n)):
                return buf.value
        finally:
            _close(h)
        return ""
else:
    def retroarch_processes():
        return []

    def process_modules(pid):
        return None

    def image_path(pid):
        return ""


def find_retroarch():
    """[{"pid", "exe", "cores"}] pour chaque RetroArch lancé ("cores" vaut None si la liste des DLL est refusée)."""
    out = []
    try:
        procs = retroarch_processes()
    except Exception:
        return out
    for pid, name in procs:
        try:
            mods = process_modules(pid)
        except Exception:
            mods = None
        exe = mods[0] if mods else ""
        if not exe:
            try:
                exe = image_path(pid)
            except Exception:
                exe = ""
        out.append({"pid": pid, "exe": exe or name, "cores": mods[1] if mods else None})
    return out


def find_core(content=""):
    """Cœur chargé par RetroArch, décrit par describe() avec "how" et "retroarch", ou None."""
    for p in find_retroarch():
        if p["cores"]:
            info = describe(p["cores"][-1])
            info.update(how="processus", retroarch=p["exe"])
            return info
        radir = os.path.dirname(p["exe"]) if os.path.isabs(p["exe"]) else ""
        core = core_from_history(radir, content) if radir else ""
        if core:
            info = describe(core)
            info.update(how="historique", retroarch=p["exe"])
            return info
    return None
