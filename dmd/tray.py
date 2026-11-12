"""The icon of ArcadeDMD near the clock (1.37), in place of the console window: a click opens the window, a right click
the menu, and a balloon says when something goes wrong. Windows only, with nothing to install (ctypes).

L'icône d'ArcadeDMD près de l'horloge, à la place de la console : un clic ouvre la fenêtre, un clic droit le menu, et
une bulle prévient quand quelque chose ne va pas. Windows seulement, rien à installer (ctypes).
"""

import ctypes
import os
import queue
import sys
import threading
import time

WM_DESTROY = 0x0002
WM_CLOSE = 0x0010
WM_NULL = 0x0000
WM_COMMAND = 0x0111
WM_LBUTTONUP = 0x0202
WM_LBUTTONDBLCLK = 0x0203
WM_RBUTTONUP = 0x0205
WM_TIMER = 0x0113
WM_APP = 0x8000
WM_TRAY = WM_APP + 1               # the icon's mouse messages / les messages de la souris sur l'icône
WM_WAKE = WM_APP + 2               # a balloon or a tip to show / une bulle ou une info-bulle à montrer
NIN_BALLOONUSERCLICK = 0x0405
NIM_ADD, NIM_MODIFY, NIM_DELETE = 0, 1, 2
NIF_MESSAGE, NIF_ICON, NIF_TIP, NIF_INFO = 0x01, 0x02, 0x04, 0x10
NIIF_INFO, NIIF_WARNING = 0x01, 0x02
MF_STRING, MF_SEPARATOR, MF_CHECKED, MF_GRAYED = 0x0000, 0x0800, 0x0008, 0x0001
TPM_RIGHTBUTTON, TPM_RETURNCMD, TPM_NONOTIFY, TPM_BOTTOMALIGN = 0x0002, 0x0100, 0x0080, 0x0020
IMAGE_ICON, LR_LOADFROMFILE, LR_DEFAULTSIZE = 1, 0x0010, 0x0040
IDI_APPLICATION = 32512


def available():
    return sys.platform == "win32"


def _icon_image(n):
    """The logo's ten dots on a dark tile, drawn for n x n pixels: crisp squares when small. / Les dix points du
    logo sur fond sombre, en carrés nets quand c'est petit."""
    from PIL import Image, ImageDraw
    dots = [(x, 0) for x in range(4)] + [(0, 1), (3, 1)] + [(x, 2) for x in range(4)]
    if n <= 24:
        img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, n - 1, n - 1), radius=max(2, n // 5), fill=(18, 20, 28, 255))
        size = 2 if n < 20 else 3
        step = size + 1
        ox = (n - (4 * step - 1)) // 2
        oy = (n - (3 * step - 1)) // 2
        for x, y in dots:
            d.rectangle((ox + x * step, oy + y * step, ox + x * step + size - 1, oy + y * step + size - 1),
                        fill=(255, 181, 71, 255))
        return img
    k = 8
    big = Image.new("RGBA", (n * k, n * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    m = n * k
    d.rounded_rectangle((0, 0, m - 1, m - 1), radius=int(m * 0.2), fill=(18, 20, 28, 255))
    step = m * 0.2
    r = step * 0.36
    ox = (m - 3 * step) / 2
    oy = (m - 2 * step) / 2
    for x, y in dots:
        cx, cy = ox + x * step, oy + y * step
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 181, 71, 255))
    return big.resize((n, n), Image.LANCZOS)


def make_icon(path):
    """The .ico of the icon near the clock, when it is missing. / Le .ico de l'icône, s'il manque."""
    sizes = [16, 20, 24, 32, 40, 48, 64, 256]
    imgs = [_icon_image(n) for n in sizes]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    imgs[-1].save(path, sizes=[(n, n) for n in sizes], append_images=imgs[:-1])
    return path


class TrayIcon:
    """The icon and its menu, in a thread of their own with a hidden window to get the clicks. menu() gives the items
    at each right click: [(label, callback, checked)] and None for a line. / L'icône et son menu, dans un fil à eux."""

    def __init__(self, tip, icon_path, on_open, menu, log=print):
        self.tip, self.icon_path, self.on_open, self.menu, self.log = tip, icon_path, on_open, menu, log
        self.hwnd = None
        self.ready = threading.Event()
        self.failed = None
        self.wake = queue.Queue()
        self.last_open = 0.0
        self.thread = threading.Thread(target=self._run, name="tray", daemon=True)
        self.thread.start()
        self.ready.wait(5.0)

    # ------------------------------------------------------------ from any thread / depuis n'importe quel fil
    def notify(self, title, text, level="info"):
        self.wake.put(("info", title, text, level))
        self._poke()

    def set_tip(self, tip):
        if tip != self.tip:
            self.tip = tip
            self.wake.put(("tip",))
            self._poke()

    def close(self):
        if self.hwnd:
            try:
                self.u32.PostMessageW(self.hwnd, WM_CLOSE, 0, 0)
            except Exception:
                pass
        self.thread.join(2.0)

    def _poke(self):
        if self.hwnd:
            try:
                self.u32.PostMessageW(self.hwnd, WM_WAKE, 0, 0)
            except Exception:
                pass

    # ------------------------------------------------------------ the icon's thread / le fil de l'icône
    def _api(self):
        from ctypes import wintypes as w
        LRESULT = ctypes.c_ssize_t
        self.WNDPROC = ctypes.WINFUNCTYPE(LRESULT, w.HWND, w.UINT, w.WPARAM, w.LPARAM)

        class WNDCLASSEXW(ctypes.Structure):
            _fields_ = [("cbSize", w.UINT), ("style", w.UINT), ("lpfnWndProc", self.WNDPROC), ("cbClsExtra", ctypes.c_int),
                        ("cbWndExtra", ctypes.c_int), ("hInstance", w.HINSTANCE), ("hIcon", w.HICON),
                        ("hCursor", w.HANDLE), ("hbrBackground", w.HBRUSH), ("lpszMenuName", w.LPCWSTR),
                        ("lpszClassName", w.LPCWSTR), ("hIconSm", w.HICON)]

        class GUID(ctypes.Structure):
            _fields_ = [("Data1", w.DWORD), ("Data2", w.WORD), ("Data3", w.WORD), ("Data4", ctypes.c_ubyte * 8)]

        class NOTIFYICONDATAW(ctypes.Structure):
            _fields_ = [("cbSize", w.DWORD), ("hWnd", w.HWND), ("uID", w.UINT), ("uFlags", w.UINT),
                        ("uCallbackMessage", w.UINT), ("hIcon", w.HICON), ("szTip", w.WCHAR * 128), ("dwState", w.DWORD),
                        ("dwStateMask", w.DWORD), ("szInfo", w.WCHAR * 256), ("uVersion", w.UINT),
                        ("szInfoTitle", w.WCHAR * 64), ("dwInfoFlags", w.DWORD), ("guidItem", GUID),
                        ("hBalloonIcon", w.HICON)]

        self.WNDCLASSEXW, self.NOTIFYICONDATAW = WNDCLASSEXW, NOTIFYICONDATAW
        u = self.u32 = ctypes.WinDLL("user32", use_last_error=True)      # own copies, own types / à part
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        s = self.shell = ctypes.WinDLL("shell32", use_last_error=True)
        k.GetModuleHandleW.argtypes = [w.LPCWSTR]
        k.GetModuleHandleW.restype = w.HMODULE
        u.RegisterClassExW.argtypes = [ctypes.POINTER(WNDCLASSEXW)]
        u.RegisterClassExW.restype = w.ATOM
        u.CreateWindowExW.argtypes = [w.DWORD, w.LPCWSTR, w.LPCWSTR, w.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                      ctypes.c_int, w.HWND, w.HMENU, w.HINSTANCE, w.LPVOID]
        u.CreateWindowExW.restype = w.HWND
        u.DefWindowProcW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM]
        u.DefWindowProcW.restype = LRESULT
        u.GetMessageW.argtypes = [ctypes.POINTER(w.MSG), w.HWND, w.UINT, w.UINT]
        u.GetMessageW.restype = w.BOOL
        u.TranslateMessage.argtypes = [ctypes.POINTER(w.MSG)]
        u.DispatchMessageW.argtypes = [ctypes.POINTER(w.MSG)]
        u.DispatchMessageW.restype = LRESULT
        u.PostMessageW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM]
        u.PostMessageW.restype = w.BOOL
        u.PostQuitMessage.argtypes = [ctypes.c_int]
        u.DestroyWindow.argtypes = [w.HWND]
        u.RegisterWindowMessageW.argtypes = [w.LPCWSTR]
        u.RegisterWindowMessageW.restype = w.UINT
        u.LoadImageW.argtypes = [w.HINSTANCE, w.LPCWSTR, w.UINT, ctypes.c_int, ctypes.c_int, w.UINT]
        u.LoadImageW.restype = w.HANDLE
        u.LoadIconW.argtypes = [w.HINSTANCE, w.LPVOID]
        u.LoadIconW.restype = w.HICON
        u.CreatePopupMenu.restype = w.HMENU
        u.AppendMenuW.argtypes = [w.HMENU, w.UINT, ctypes.c_size_t, w.LPCWSTR]
        u.AppendMenuW.restype = w.BOOL
        u.SetMenuDefaultItem.argtypes = [w.HMENU, w.UINT, w.UINT]
        u.TrackPopupMenu.argtypes = [w.HMENU, w.UINT, ctypes.c_int, ctypes.c_int, ctypes.c_int, w.HWND, w.LPVOID]
        u.TrackPopupMenu.restype = w.BOOL
        u.DestroyMenu.argtypes = [w.HMENU]
        u.SetForegroundWindow.argtypes = [w.HWND]
        u.GetCursorPos.argtypes = [ctypes.POINTER(w.POINT)]
        u.SetTimer.argtypes = [w.HWND, ctypes.c_size_t, w.UINT, w.LPVOID]
        u.SetTimer.restype = ctypes.c_size_t
        u.KillTimer.argtypes = [w.HWND, ctypes.c_size_t]
        s.Shell_NotifyIconW.argtypes = [w.DWORD, ctypes.POINTER(NOTIFYICONDATAW)]
        s.Shell_NotifyIconW.restype = w.BOOL
        return k.GetModuleHandleW(None)

    def _run(self):
        try:
            hinst = self._api()
            u = self.u32
            self.proc = self.WNDPROC(self._proc)                  # kept alive / gardé en vie
            wc = self.WNDCLASSEXW()
            wc.cbSize = ctypes.sizeof(self.WNDCLASSEXW)
            wc.lpfnWndProc = self.proc
            wc.hInstance = hinst
            wc.lpszClassName = "ArcadeDMDTray"
            if not u.RegisterClassExW(ctypes.byref(wc)) and ctypes.get_last_error() != 1410:   # already registered
                raise OSError(f"RegisterClassExW {ctypes.get_last_error()}")
            self.taskbar_created = u.RegisterWindowMessageW("TaskbarCreated")
            # a hidden top-level window (not message-only: it must hear TaskbarCreated) / une fenêtre cachée
            self.hwnd = u.CreateWindowExW(0, "ArcadeDMDTray", "ArcadeDMD tray", 0, 0, 0, 0, 0, None, None, hinst, None)
            if not self.hwnd:
                raise OSError(f"CreateWindowExW {ctypes.get_last_error()}")
            self.hicon = None
            if self.icon_path and os.path.isfile(self.icon_path):
                self.hicon = u.LoadImageW(None, self.icon_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE)
            if not self.hicon:
                self.hicon = u.LoadIconW(None, ctypes.c_void_p(IDI_APPLICATION))
            self.added = self._add()
            if not self.added:
                # started with Windows, the taskbar may not be there yet: tried again every 2 s, and when it comes
                # lancé avec Windows, la barre des tâches n'est peut-être pas encore là : réessayé toutes les 2 s
                self.tries = 0
                u.SetTimer(self.hwnd, 1, 2000, None)
        except Exception as e:
            self.failed = e
            self.hwnd = None
            self.ready.set()
            return
        self.ready.set()
        from ctypes import wintypes as w
        msg = w.MSG()
        while True:
            r = u.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if r == 0 or r == -1:
                break
            u.TranslateMessage(ctypes.byref(msg))
            u.DispatchMessageW(ctypes.byref(msg))
        self.hwnd = None

    def _nid(self, flags):
        n = self.NOTIFYICONDATAW()
        n.cbSize = ctypes.sizeof(self.NOTIFYICONDATAW)
        n.hWnd = self.hwnd
        n.uID = 1
        n.uFlags = flags
        n.uCallbackMessage = WM_TRAY
        n.hIcon = self.hicon
        n.szTip = (self.tip or "ArcadeDMD")[:127]
        return n

    def _add(self):
        n = self._nid(NIF_MESSAGE | NIF_ICON | NIF_TIP)
        return bool(self.shell.Shell_NotifyIconW(NIM_ADD, ctypes.byref(n)))

    def _proc(self, hwnd, msg, wp, lp):
        try:
            if msg == WM_TRAY:
                ev = lp & 0xFFFF
                if ev in (WM_LBUTTONUP, WM_LBUTTONDBLCLK, NIN_BALLOONUSERCLICK):
                    if time.monotonic() - self.last_open > 1.5:          # a double click opens one window / une seule
                        self.last_open = time.monotonic()
                        self._call(self.on_open)
                elif ev == WM_RBUTTONUP:
                    self._popup()
                return 0
            if msg == WM_WAKE:
                self._drain()
                return 0
            if msg == self.taskbar_created:                              # Explorer restarted / l'Explorateur relancé
                self.added = self._add()
                return 0
            if msg == WM_TIMER:
                self.tries += 1
                self.added = self.added or self._add()
                if self.added or self.tries >= 60:
                    self.u32.KillTimer(hwnd, 1)
                    if not self.added:
                        self.log("tray: Shell_NotifyIconW refused for 2 min")
                return 0
            if msg == WM_CLOSE:
                self.u32.DestroyWindow(hwnd)
                return 0
            if msg == WM_DESTROY:
                n = self._nid(0)
                self.shell.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(n))
                self.u32.PostQuitMessage(0)
                return 0
        except Exception as e:
            try:
                self.log(f"tray: {e!r}")
            except Exception:
                pass
        return self.u32.DefWindowProcW(hwnd, msg, wp, lp)

    def _drain(self):
        while True:
            try:
                item = self.wake.get_nowait()
            except queue.Empty:
                return
            if item[0] == "tip":
                n = self._nid(NIF_TIP)
            else:
                _, title, text, level = item
                n = self._nid(NIF_INFO)
                n.szInfo = str(text)[:255]
                n.szInfoTitle = str(title)[:63]
                n.dwInfoFlags = NIIF_WARNING if level == "warn" else NIIF_INFO
            self.shell.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(n))

    def _call(self, fn):
        """Away from the icon's thread: a slow action never freezes the menu. / Hors du fil de l'icône."""
        threading.Thread(target=fn, daemon=True).start()

    def _popup(self):
        from ctypes import wintypes as w
        u = self.u32
        try:
            items = self.menu() or []
        except Exception as e:
            self.log(f"tray menu: {e!r}")
            return
        h = u.CreatePopupMenu()
        calls = {}
        for i, item in enumerate(items, start=1):
            if item is None:
                u.AppendMenuW(h, MF_SEPARATOR, 0, None)
                continue
            label, fn, checked = (tuple(item) + (False,))[:3]
            flags = MF_STRING | (MF_CHECKED if checked else 0) | (MF_GRAYED if fn is None else 0)
            u.AppendMenuW(h, flags, i, label)
            calls[i] = fn
        first = next((i for i, fn in calls.items() if fn is not None), None)
        if first is not None:
            u.SetMenuDefaultItem(h, first, 0)                            # the first action in bold / en gras
        pt = w.POINT()
        u.GetCursorPos(ctypes.byref(pt))
        u.SetForegroundWindow(self.hwnd)                                 # else the menu stays open / sinon il reste
        cmd = u.TrackPopupMenu(h, TPM_RIGHTBUTTON | TPM_RETURNCMD | TPM_NONOTIFY | TPM_BOTTOMALIGN, pt.x, pt.y, 0,
                               self.hwnd, None)
        u.PostMessageW(self.hwnd, WM_NULL, 0, 0)
        u.DestroyMenu(h)
        fn = calls.get(int(cmd or 0))
        if fn is not None:
            self._call(fn)
