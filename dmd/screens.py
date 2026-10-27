"""Screens connected to the PC (Windows only), used to place the "virtual LED" window on an LCD screen used as a DMD.

Écrans branchés sur le PC (Windows), pour placer la fenêtre « LED virtuelles » sur un LCD qui sert de DMD."""

import ctypes
import sys


def list_screens():
    """[{"x", "y", "width", "height", "primary"}] en vrais pixels, vide hors Windows."""
    if sys.platform != "win32":
        return []
    from ctypes import wintypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)     # coordonnées réelles même avec un zoom Windows
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass

    class MONITORINFO(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT), ("rcWork", wintypes.RECT),
                    ("dwFlags", wintypes.DWORD)]

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC, ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)
    user32.EnumDisplayMonitors.argtypes = (wintypes.HDC, ctypes.POINTER(wintypes.RECT), proc, wintypes.LPARAM)
    user32.EnumDisplayMonitors.restype = wintypes.BOOL
    user32.GetMonitorInfoW.argtypes = (wintypes.HMONITOR, ctypes.POINTER(MONITORINFO))
    user32.GetMonitorInfoW.restype = wintypes.BOOL
    out = []

    def cb(hmon, hdc, rect, data):
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(mi)
        if user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
            r = mi.rcMonitor
            out.append({"x": r.left, "y": r.top, "width": r.right - r.left, "height": r.bottom - r.top,
                        "primary": bool(mi.dwFlags & 1)})
        return True

    try:
        user32.EnumDisplayMonitors(None, None, proc(cb), 0)
    except OSError:
        return []
    return out


def guess_dmd(screens):
    """Index de l'écran le plus probable pour le DMD : le plus allongé qui n'est pas l'écran principal."""
    best, ratio = None, 0.0
    for i, s in enumerate(screens):
        if s["primary"] or s["height"] <= 0:
            continue
        r = s["width"] / s["height"]
        if r > ratio:
            best, ratio = i, r
    return best if ratio >= 2.5 else None
