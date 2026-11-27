"""Checks the RetroAchievements part (1.41) against a site played by this tool on this machine, never the real one:
what the watch announces and what it keeps quiet, what it says when the site refuses or is down, that the web API key
never reaches the log nor the page of the window, that the window keeps the key when its field is left empty, and that
the slab is drawn on the HD screen for six seconds and then gone.

Vérifie la partie RetroAchievements contre un site joué par cet outil sur cette machine, jamais le vrai : ce que la
veille annonce et ce qu'elle tait, ce qu'elle dit quand le site refuse ou tombe, que la clé web API n'arrive jamais
dans le journal ni dans la page de la fenêtre, que la fenêtre garde la clé quand son champ est laissé vide, et que le
cartouche est dessiné sur l'écran HD pendant six secondes puis disparaît.

usage: python tools/achievements_check.py
"""
import http.server
import json
import os
import queue
import sys
import tempfile
import threading
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ["NO_PROXY"] = os.environ["no_proxy"] = "127.0.0.1,localhost"

from dmd import app, gui_setup, racheevos  # noqa: E402

USER, KEY = "Joueur", "k3y-NEVER-in-the-log-0123456789"


class Site:
    """The pretend site: one account, its recent unlocks, its progress in each game. / Le faux site."""

    def __init__(self):
        self.recent = []
        self.progress = {}
        self.status = None                # answers this status to everything when set / répond ce statut à tout
        self.plain = False                # refuses with a 200 and a message, as some sites do / refuse en 200
        self.asked = []
        site = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                url = urllib.parse.urlparse(self.path)
                qs = {k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()}
                name = url.path.rsplit("/", 1)[-1]
                site.asked.append(name)
                code, body = site.answer(name, qs)
                raw = json.dumps(body).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}/API/"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def answer(self, name, qs):
        if self.status:
            return self.status, {"message": "no"}
        if qs.get("y") != KEY:
            return (200, {"message": "Unauthenticated."}) if self.plain else (401, {"message": "Unauthenticated."})
        if qs.get("u") != USER:
            return (200, []) if self.plain or name != "API_GetUserProfile.php" else (404, [])
        if name == "API_GetUserProfile.php":
            return 200, {"User": USER, "TotalPoints": 1200, "TotalSoftcorePoints": 340, "RichPresenceMsg": "Playing"}
        if name == "API_GetUserRecentAchievements.php":
            return 200, list(self.recent)
        if name == "API_GetGameInfoAndUserProgress.php":
            if qs.get("g") not in self.progress:
                return 500, {}
            n, of = self.progress[qs["g"]]
            return 200, {"NumAchievements": of, "NumAwardedToUser": n}
        return 404, {}

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def unlock(ident, date, title, points=5, game=10, hardcore=0):
    return {"Date": date, "HardcoreMode": hardcore, "AchievementID": ident, "Title": title, "Description": "...",
            "BadgeName": "1", "Points": points, "GameTitle": "A Game", "GameID": game}


def events(q):
    out = []
    while True:
        try:
            out.append(q.get_nowait()[1])
        except queue.Empty:
            return out


def check_watch(site):
    lines, q = [], queue.Queue()
    cfg = {"retroachievements": {"enabled": True, "user": USER, "key": KEY, "every": 1}}
    assert racheevos.settings(cfg) == (True, USER, KEY, racheevos.LEAST), "never more often than LEAST"
    assert racheevos.settings({"retroachievements": {"enabled": True, "user": USER, "key": ""}})[0] is False, "no key, off"
    assert racheevos.settings({"retroachievements": "x"})[0] is False and racheevos.settings(None)[0] is False, "odd settings"
    w = racheevos.Watch(cfg, q, lines.append, base=site.base, start=False)
    site.recent = [unlock(1, "2026-11-27 20:00:00", "Old One")]
    site.progress = {"10": (3, 40)}
    assert w.look() == 0 and not events(q), "what was unlocked before is not news"
    assert sum("Joueur" in ln for ln in lines) == 1, "says once who the account is"
    assert w.look() == 0 and not events(q), "nothing new, nothing said"
    site.recent.insert(0, unlock(2, "2026-11-27 20:05:00", "First Blood", points=10, hardcore=1))
    assert w.look() == 1, "one new"
    ev = events(q)
    assert ev == [{"t": "achievement", "title": "First Blood", "description": "...", "points": 10, "game": "A Game",
                   "hardcore": True, "n": 3, "of": 40}], ev
    assert w.look() == 0 and not events(q), "announced once"
    site.recent.insert(0, unlock(3, "2026-11-27 20:06:10", "Second", game=99))        # a game whose progress fails
    site.recent.insert(0, unlock(4, "2026-11-27 20:06:05", "Earlier"))
    site.recent.insert(0, "not an unlock")
    assert w.look() == 2, "two new, the odd line left out"
    ev = events(q)
    assert [e["title"] for e in ev] == ["Earlier", "Second"], "in the order they were unlocked"
    assert ev[1]["n"] is None and ev[1]["of"] is None, "the news goes without the count"
    # a game closed for long, then another started: what was unlocked meanwhile elsewhere is not news
    w.game(True)
    w.game(False)
    w.until = 0.0
    site.recent.insert(0, unlock(5, "2026-11-27 21:00:00", "Elsewhere"))
    w.game(True)
    assert w.fresh and w.look() == 0 and not events(q), "a game that starts takes stock first"
    site.recent.insert(0, unlock(6, "2026-11-27 21:01:00", "In This Game"))
    assert w.look() == 1 and [e["title"] for e in events(q)] == ["In This Game"], "then announces"
    # the site refuses, is down, comes back
    before = len(lines)
    site.status = 500
    assert w.look() == 0 and w.look() == 0 and len(lines) == before + 1, "a failure is said once"
    site.status = 429
    assert w.look() == 0 and w.hold > time.monotonic() + racheevos.HOLD - 5, "too many requests: nothing asked for a while"
    site.status = None
    site.recent.insert(0, unlock(7, "2026-11-27 21:02:00", "After The Outage"))
    assert w.look() == 1 and events(q)[0]["title"] == "After The Outage", "what was unlocked during the outage is announced"
    assert any("de nouveau" in ln or "again" in ln for ln in lines[before:]), "says the site answers again"
    # a wrong key, a wrong name, with a status or with a plain message
    for plain in (False, True):
        site.plain = plain
        for user, key in ((USER, "wrong"), ("Nobody", KEY)):
            said = []
            bad = racheevos.Watch({"retroachievements": {"enabled": True, "user": user, "key": key}}, q, said.append,
                                  base=site.base, start=False)
            assert bad.look() == 0 and len(said) == 1 and not bad.known, (plain, user, said)
            assert "wrong" not in said[0] and KEY not in said[0], "the key is not in the reason"
    site.plain = False
    site.close()
    down = racheevos.Watch(cfg, q, lines.append, base=site.base, start=False)
    assert down.look() == 0, "a site that is not there stops nothing"
    assert not events(q)
    assert not any(KEY in ln for ln in lines), "the key never reaches the log"
    return len(lines)


def check_thread(site):
    """The watch as it runs: asks at the start, then only while a game is played. / La veille telle qu'elle tourne."""
    q, lines = queue.Queue(), []
    old = racheevos.LEAST, racheevos.SOON
    racheevos.LEAST, racheevos.SOON = 0.2, 0.0
    try:
        w = racheevos.Watch({"retroachievements": {"enabled": True, "user": USER, "key": KEY, "every": 0.2}}, q,
                            lines.append, base=site.base)
        time.sleep(0.8)
        idle = site.asked.count("API_GetUserRecentAchievements.php")
        assert idle == 1, f"no game, the site is asked once at the start, not {idle} times"
        w.game(True)
        time.sleep(0.5)
        site.recent.insert(0, unlock(20, "2026-11-27 22:00:00", "Live"))
        deadline = time.monotonic() + 5
        got = []
        while not got and time.monotonic() < deadline:
            time.sleep(0.1)
            got = events(q)
        assert [e["title"] for e in got] == ["Live"], got
        w.close()
        time.sleep(0.5)
        n = len(site.asked)
        time.sleep(0.6)
        assert len(site.asked) == n, "closed, nothing more is asked"
    finally:
        racheevos.LEAST, racheevos.SOON = old


def check_window(site):
    with tempfile.TemporaryDirectory() as tmp:
        lines = []
        setup = gui_setup.Setup(tmp, lines.append)
        setup.ra_base = site.base
        routes = setup.routes()
        get, save, test = routes[("GET", "/api/achievements")], routes[("POST", "/api/achievements")], routes[("POST", "/api/achievements/test")]
        assert get({}) == {"enabled": False, "user": "", "key_set": False}, "nothing set at first"
        assert test({"user": USER, "key": ""})["ok"] is False, "no key, nothing asked"
        r = test({"user": USER, "key": KEY})
        assert r == {"ok": True, "user": USER, "points": 1200, "softcore": 340, "last": "Playing"}, r
        for user, key in ((USER, "wrong-key-xyz"), ("Nobody", KEY)):
            r = test({"user": user, "key": key})
            assert r["ok"] is False and r["error"] and "wrong-key-xyz" not in r["error"] and KEY not in r["error"], r
        assert save({"enabled": True, "user": " " + USER + " ", "key": KEY}) == {"ok": True}
        with open(os.path.join(tmp, "config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        assert cfg["retroachievements"] == {"enabled": True, "user": USER, "key": KEY}, "saved in config.json"
        page = get({})
        assert page == {"enabled": True, "user": USER, "key_set": True} and KEY not in json.dumps(page), "the key never goes back to the page"
        assert test({})["ok"] is True, "tried with the key that is kept"
        save({"enabled": False, "user": USER, "key": ""})
        with open(os.path.join(tmp, "config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        assert cfg["retroachievements"]["key"] == KEY and cfg["retroachievements"]["enabled"] is False, "an empty field keeps the key"
        save({"enabled": False, "user": USER, "key": "", "forget": True})
        assert get({})["key_set"] is False, "forgotten when asked"
        assert not any(KEY in ln for ln in lines), "the key never reaches the log"


def check_engine_and_screen():
    import pygame
    from dmd.hd import HDRenderer
    pygame.init()
    pygame.display.set_mode((1, 1))
    log = app.Logger(None, echo=False)
    cfg = dict(app.load_config(ROOT, log), retroarch={"enabled": False}, textfiles={"enabled": False})
    eng = app.Engine(ROOT, cfg, [], log, demo_game="kof98")
    assert eng.ra_watch is None and eng.achievement is None, "off until an account is set"
    eng.handle_event({"t": "achievement", "title": "First Blood", "points": 10, "game": "A Game", "n": 3, "of": 40}, 0.0, "site")
    assert eng.achievement["serial"] == 1 and eng.achievement["title"] == "First Blood" and eng.overlay, "the engine keeps the news"
    hd = HDRenderer(pygame, (1920, 470), ROOT, {"logos": False}, lambda *a: None, logos=None)
    long_one = dict(eng.achievement, serial=2, title="An Achievement With A Name Far Longer Than Any Slab Could Ever Hold In Big Letters", n=None)

    def drawn(ev, now):
        s = pygame.Surface((1920, 470), pygame.SRCALPHA)           # see-through, to find what was drawn / pour voir ce qui est dessiné

        class E:
            achievement = ev
        hd._draw_achievement(s, E, now)
        return s.get_bounding_rect()

    assert drawn(None, 0.0).w == 0, "no news, nothing drawn"
    box = drawn(eng.achievement, 10.0)
    assert box.w == 0, "the first picture of a slab starts from nothing"
    box = drawn(eng.achievement, 12.0)
    assert 850 <= box.w <= 910 and 150 <= box.h <= 170 and abs(box.centerx - 960) <= 2, f"a slab in the middle, {box}"
    assert drawn(eng.achievement, 10.0 + hd.ACH_SECONDS + 0.1).w == 0, "gone after six seconds"
    box = drawn(long_one, 30.0)
    box = drawn(long_one, 32.0)
    assert 850 <= box.w <= 910, f"a long name stays inside the slab, {box}"
    pygame.quit()


def main():
    site = Site()
    n = check_watch(site)
    print(f"ok watch: {n} lines in the log, the key in none")
    site = Site()
    try:
        check_thread(site)
        print("ok thread: asks once at the start, then while a game is played")
        check_window(site)
        print("ok window: the key is kept, never sent back")
    finally:
        site.close()
    check_engine_and_screen()
    print("ok screen: a slab in the middle for six seconds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
