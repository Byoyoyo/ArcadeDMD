"""Checks the orders sent to HyperHDR (dmd/lights.py) against a server of its own that plays HyperHDR's part: the colours
of each event with their duration and priority, the priority cleared at the end, a strong event not cut by a weak one,
and nothing sent while "lights" is off. Run by the check of every pull request.

Vérifie les ordres envoyés à HyperHDR avec un serveur à lui qui joue le rôle d'HyperHDR.

usage: python tools/lights_check.py
"""
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dmd import lights  # noqa: E402

GOT = []
FAILS = []


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        GOT.append((self.path, json.loads(body)))
        out = json.dumps({"success": True, "info": {"version": "test"}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


def check(what, ok):
    if not ok:
        FAILS.append(what)


srv = HTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

off = lights.Lights({"enabled": False, "port": port})
check("nothing sent while off", off.event("ko") is False and not GOT)

li = lights.Lights({"enabled": True, "port": port, "priority": 42, "brightness": 0.5})
check("a K.O. is taken", li.event("ko") is True)
check("a blow does not cut a K.O.", li.event("blow") is False)
time.sleep(sum(ms for _, ms in lights.RECIPES["ko"]) / 1000.0 + 0.6)
orders = [o for _, o in GOT]
colors = [o for o in orders if o.get("command") == "color"]
check("every order goes to /json-rpc", all(p == "/json-rpc" for p, _ in GOT))
check("the colours of a K.O., one after the other", len(colors) == len(lights.RECIPES["ko"]))
check("its priority", all(o.get("priority") == 42 for o in orders))
check("each colour ends by itself", all(o.get("duration", 0) > 0 for o in colors))
check("the brightness asked", colors and colors[0]["color"] == [127, 127, 127])
check("the priority cleared at the end", orders and orders[-1] == {"command": "clear", "priority": 42})
del GOT[:]
check("an event turned off", lights.Lights({"enabled": True, "port": port, "events": {"coin": False}}).event("coin") is False)
li.close()
dead = lights.Lights({"enabled": True, "port": 1})                  # nobody there: no error, nothing blocks
t0 = time.monotonic()
dead.event("coin")
time.sleep(0.3)
check("no HyperHDR: the game goes on", time.monotonic() - t0 < 1.5)
srv.shutdown()
if FAILS:
    print("\n".join("FAILED " + f for f in FAILS))
    sys.exit(1)
print("lights: ok")
