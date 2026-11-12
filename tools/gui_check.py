"""Checks that ArcadeDMD's window answers (used by the GitHub check, and by hand): the page, the state, the log, the
settings routes, and that a request without the page's token or from another host is refused.

Vérifie que la fenêtre d'ArcadeDMD répond : la page, l'état, le journal, les routes de réglage, et qu'une demande
sans le jeton de la page ou venue d'un autre hôte est refusée.

usage: python tools/gui_check.py
"""
import http.client
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dmd import app, gui, gui_setup  # noqa: E402


def ask(port, method, path, body=None, headers=None):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    c.request(method, path, body=json.dumps(body) if body is not None else None, headers=headers or {})
    r = c.getresponse()
    data = r.read()
    c.close()
    return r.status, data


def main():
    with tempfile.TemporaryDirectory() as tmp:
        log = app.Logger(None, echo=False)
        log("first line")
        panel = gui.ControlPanel(tmp, log, app.VERSION, port=47890)
        panel.extra.update(gui_setup.Setup(ROOT, log).routes())
        try:
            port = panel.port
            st, page = ask(port, "GET", "/")
            assert st == 200 and b"app.js" in page, "page"
            token = re.search(rb'TOKEN = "([0-9a-f]+)"', page).group(1).decode()
            for path in ("/app.js", "/setup.js", "/app.css", "/arcadedmd.ico"):
                assert ask(port, "GET", path)[0] == 200, path
            st, data = ask(port, "GET", "/api/state")
            assert st == 200 and json.loads(data)["version"] == app.VERSION, "state"
            st, data = ask(port, "GET", "/api/log?after=0")
            assert st == 200 and json.loads(data)["lines"][0]["text"].endswith("first line"), "log"
            for path in ("/api/screens", "/api/emulators", "/api/frontend"):
                st, data = ask(port, "GET", path)
                assert st == 200, path
                json.loads(data)
            assert ask(port, "POST", "/api/action", {"do": "quit"})[0] == 403, "no token"
            assert ask(port, "GET", "/api/state", headers={"Host": "example.com"})[0] == 403, "other host"
            st, data = ask(port, "POST", "/api/action", {"do": "nothing"}, {"X-ArcadeDMD-Token": token})
            assert st == 200 and json.loads(data)["ok"] is False, "unknown action"
        finally:
            panel.close()
    print("window ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
