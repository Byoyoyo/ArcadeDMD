"""The LEDs of the cabinet follow the game, through HyperHDR (1.39). Off until "lights" is enabled in config.json.

HyperHDR drives the LED strip and usually shows the colours of the screen. It also takes orders in JSON on its web port
(http://host:8090/json-rpc, the same orders as Hyperion: "color" with a duration and a priority, "clear"). At an event
of the game ArcadeDMD sends a short run of colours with a priority that wins over the screen capture, then clears its
priority and HyperHDR goes back to the screen. Each colour is sent with a duration of its own, so the strip never stays
on a colour if ArcadeDMD stops in the middle.

  "lights": {"enabled": true, "host": "127.0.0.1", "port": 8090, "priority": 50, "brightness": 1.0,
             "events": {"blow": false}}          an event set to false is not shown
  python arcadedmd.py test-lights                asks HyperHDR who it is, then plays every event

Les LED de la borne suivent le jeu, par HyperHDR. Coupé tant que « lights » n'est pas activé dans config.json. HyperHDR
pilote le ruban et montre d'habitude les couleurs de l'écran. Il prend aussi des ordres en JSON sur son port web. À un
événement du jeu, ArcadeDMD envoie une courte suite de couleurs avec une priorité qui passe devant la capture de
l'écran, puis libère sa priorité et HyperHDR revient à l'écran. Chaque couleur est envoyée avec sa durée, le ruban ne
reste donc jamais sur une couleur si ArcadeDMD s'arrête au milieu."""
import json
import queue
import threading
import time
import urllib.request

from .i18n import tr

# event -> [(red, green, blue), milliseconds] one after the other / l'une après l'autre
RECIPES = {
    "coin": [((255, 190, 40), 140), ((60, 40, 0), 80), ((255, 190, 40), 180)],
    "blow": [((255, 255, 255), 90), ((255, 90, 30), 160)],
    "ko": [((255, 255, 255), 130), ((255, 30, 20), 250), ((120, 0, 0), 350), ((255, 30, 20), 250)],
    "super": [((255, 200, 60), 160), ((90, 60, 0), 90), ((255, 200, 60), 160), ((90, 60, 0), 90), ((255, 220, 120), 420)],
    "win": [((255, 200, 60), 200), ((255, 255, 255), 120), ((255, 200, 60), 200), ((255, 255, 255), 120),
            ((255, 200, 60), 200), ((255, 255, 255), 120), ((255, 180, 40), 700)],
    "boss": [((255, 0, 0), 300), ((70, 0, 0), 300), ((255, 0, 0), 300), ((70, 0, 0), 300), ((255, 0, 0), 300),
             ((70, 0, 0), 300)],
}
LABELS = {"coin": ("une pièce", "a coin"), "blow": ("un gros coup", "a big blow"), "ko": ("un K.O.", "a K.O."),
          "super": ("la jauge pleine", "the gauge full"), "win": ("une victoire", "a win"),
          "boss": ("l'alerte d'un boss", "a boss warning")}
RANK = {"blow": 1, "coin": 2, "super": 3, "boss": 4, "ko": 5, "win": 6}     # a K.O. is not cut by a blow / pas coupé
MARGIN = 400              # each colour lasts that much longer than its step, in ms / chaque couleur dure un peu plus


class Lights:
    def __init__(self, cfg, log=None):
        cfg = cfg if isinstance(cfg, dict) else {}
        self.enabled = bool(cfg.get("enabled", False))
        self.url = f"http://{cfg.get('host', '127.0.0.1')}:{int(cfg.get('port', 8090))}/json-rpc"
        self.priority = int(cfg.get("priority", 50))
        self.gain = max(0.0, min(1.0, float(cfg.get("brightness", 1.0))))
        ev = cfg.get("events") if isinstance(cfg.get("events"), dict) else {}
        self.off = {k for k, v in ev.items() if v is False}
        self.log = log or (lambda m: None)
        self.q = queue.Queue()
        self.busy = None          # (event, until) the run of colours being played / la suite en cours
        self.failed = 0
        self.thread = None
        if self.enabled:
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    # ------------------------------------------------------------------ HyperHDR
    def call(self, order, timeout=0.6):
        """Sends an order, returns HyperHDR's answer (a dict) or None. / Envoie un ordre, renvoie la réponse ou None."""
        try:
            req = urllib.request.Request(self.url, data=json.dumps(order).encode("utf-8"),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace") or "{}")
        except (OSError, ValueError):
            return None

    def color(self, rgb, ms):
        rgb = [max(0, min(255, int(c * self.gain))) for c in rgb]
        return self.call({"command": "color", "color": rgb, "duration": int(ms), "priority": self.priority,
                          "origin": "ArcadeDMD"})

    def clear(self):
        return self.call({"command": "clear", "priority": self.priority})

    # ------------------------------------------------------------------ events
    def event(self, name, now=None):
        """An event of the game: its colours, unless a stronger one is being played. / Un événement du jeu."""
        if not self.enabled or name in self.off or name not in RECIPES:
            return False
        now = time.monotonic() if now is None else now
        if self.busy is not None and now < self.busy[1] and RANK.get(name, 0) < RANK.get(self.busy[0], 0):
            return False
        self.busy = (name, now + sum(ms for _, ms in RECIPES[name]) / 1000.0)
        self.q.put(name)
        return True

    def _run(self):
        while True:
            name = self.q.get()
            if name is None:
                return
            self._play(name)

    def _play(self, name, wait=None):
        ok = True
        for rgb, ms in RECIPES[name]:
            if not self.q.empty():                                # a newer event takes over / un événement plus récent
                return
            if self.color(rgb, ms + MARGIN) is None:
                ok = False
                break
            (wait or time.sleep)(ms / 1000.0)
        if ok:
            if self.q.empty():
                self.clear()                                      # back to the screen capture / retour à l'écran
            self.failed = 0
        else:
            self.failed += 1
            if self.failed in (1, 20):                            # said once, and once more / dit une fois, puis une
                self.log(tr(f"lumières : HyperHDR ne répond pas à {self.url}", f"lights: HyperHDR does not answer at {self.url}"))

    def close(self):
        if self.thread is not None:
            self.q.put(None)
            self.thread.join(1.5)
            self.thread = None
            self.clear()


def test(cfg, out=print):
    """python arcadedmd.py test-lights: who answers, then every event. / Qui répond, puis chaque événement."""
    cfg = dict(cfg if isinstance(cfg, dict) else {}, enabled=False)
    li = Lights(cfg)
    out(tr(f"Test des lumières, HyperHDR à {li.url}", f"Lights test, HyperHDR at {li.url}"))
    info = li.call({"command": "serverinfo"}, timeout=2.0)
    if info is None:
        out(tr("HyperHDR ne répond pas. Est-il lancé, et son adresse est-elle la bonne dans config.json (lights, host et port) ?",
               "HyperHDR does not answer. Is it running, and is its address right in config.json (lights, host and port)?"))
        return 1
    data = info.get("info") if isinstance(info.get("info"), dict) else {}
    out(tr(f"HyperHDR répond (version {data.get('version') or data.get('hyperhdr', {}).get('version') or '?'}).",
           f"HyperHDR answers (version {data.get('version') or data.get('hyperhdr', {}).get('version') or '?'})."))
    for name in ("coin", "blow", "super", "ko", "win", "boss"):
        out("  " + tr(*LABELS[name]))
        li._play(name)
        time.sleep(0.6)
    li.clear()
    out(tr("Fini. Le ruban doit être revenu aux couleurs de l'écran.", "Done. The strip should be back to the screen's colours."))
    return 0
