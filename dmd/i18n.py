"""Language of messages and on-screen texts.

English by default, French automatically when Windows (or the system locale) is in French.
Force it with "language": "en" or "fr" in config.json, or with the ARCADEDMD_LANG environment variable.

Langue des messages : anglais par défaut, français automatiquement si Windows est en français.
Réglage "language" dans config.json ("auto", "en" ou "fr"), ou variable d'environnement ARCADEDMD_LANG.
"""

import locale
import os
import sys

_lang = None


def detect():
    env = (os.environ.get("ARCADEDMD_LANG") or "").strip().lower()
    if env[:2] in ("en", "fr"):
        return env[:2]
    if sys.platform == "win32":
        try:
            import ctypes
            lid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return "fr" if (lid & 0x3FF) == 0x0C else "en"
        except Exception:
            pass
    try:
        loc = locale.getlocale()[0] or ""
    except ValueError:
        loc = ""
    loc = loc or os.environ.get("LC_ALL") or os.environ.get("LC_MESSAGES") or os.environ.get("LANG") or ""
    return "fr" if loc.lower().startswith("fr") else "en"


def set_language(value=None):
    """value : "auto", "en" or "fr" (config.json). Returns the language in use."""
    global _lang
    v = (value or "auto").strip().lower()
    _lang = v[:2] if v[:2] in ("en", "fr") else detect()
    return _lang


def lang():
    global _lang
    if _lang is None:
        _lang = detect()
    return _lang


def tr(fr, en):
    """The French or English text, depending on the language in use."""
    return fr if lang() == "fr" else en
