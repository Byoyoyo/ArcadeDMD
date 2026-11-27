"""RetroAchievements (1.41): an achievement unlocked while a game is played is announced on the marquee.

The account is set in the Achievements tab of the window: the user name and the web API key of the site (its control
panel, section Keys), never the password. ArcadeDMD then asks the site, every EVERY seconds while a game is played,
for the achievements unlocked in the last minutes (API_GetUserRecentAchievements). What was unlocked before the game
was started is not news. For a new one it also asks how many of the game's achievements are now unlocked
(API_GetGameInfoAndUserProgress), and hands the engine one event:

  {"t": "achievement", "title", "description", "points", "game", "hardcore", "n", "of"}

The key is never written to the log, and a failure of the site stops nothing: it is said once and tried again later.

RetroAchievements (1.41) : un succès débloqué pendant une partie est annoncé sur le fronton. Le compte se règle dans
l'onglet Succès de la fenêtre, avec le nom d'utilisateur et la clé web API du site (son panneau de contrôle, section
Keys), jamais le mot de passe. ArcadeDMD demande ensuite au site, toutes les EVERY secondes pendant une partie, les
succès débloqués dans les dernières minutes. Ce qui était débloqué avant le lancement du jeu n'est pas une nouvelle.
La clé n'est jamais écrite dans le journal, et une panne du site n'arrête rien.
"""
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

from .i18n import tr

API = "https://retroachievements.org/API/"
EVERY = 15.0                  # seconds between two questions while a game is played / entre deux questions pendant une partie
LEAST = 10.0                  # never more often than this / jamais plus souvent
SOON = 5.0                    # a game that starts is asked about at once, unless the site was asked this recently / sauf si
LOOK_BACK = 10                # minutes of unlocks asked for each time / minutes de succès demandées à chaque fois
AFTER = 90.0                  # still asked this long after the game is closed / encore demandé après la fermeture du jeu
HOLD = 120.0                  # nothing asked this long when the site says too many requests / silence si le site le demande
TIMEOUT = 8.0


class Refused(ValueError):
    """The site answered, but not with what was asked: a name or a key it does not know.
    / Le site a répondu, mais pas ce qui était demandé : un nom ou une clé qu'il ne connaît pas."""


def ask(endpoint, user, key, base=API, timeout=TIMEOUT, **params):
    """One question to the site, its answer read as JSON. / Une question au site, sa réponse lue en JSON."""
    query = dict(params, y=key, u=user)
    req = urllib.request.Request(base + endpoint + "?" + urllib.parse.urlencode(query), headers={"User-Agent": "ArcadeDMD"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def why(e):
    """Why the site did not answer, in a few words and without the address asked, which holds the key.
    / Pourquoi le site n'a pas répondu, en quelques mots et sans l'adresse demandée, qui contient la clé."""
    if isinstance(e, urllib.error.HTTPError):
        if e.code in (401, 403):
            return tr("le site refuse cette clé", "the site refuses this key")
        if e.code == 404:
            return tr("le site ne connaît pas cet utilisateur", "the site does not know this user")
        if e.code == 429:
            return tr("trop de demandes, le site demande d'attendre", "too many requests, the site asks to wait")
        return tr(f"le site répond {e.code}", f"the site answers {e.code}")
    if isinstance(e, Refused):
        return tr("le site ne reconnaît pas ce nom ou cette clé", "the site does not recognise this name or this key")
    if isinstance(e, (urllib.error.URLError, OSError)):
        return tr("le site ne répond pas", "the site does not answer")
    return tr("réponse du site illisible", "answer of the site unreadable")


def profile(user, key, base=API):
    """Who the account is, to try it from the window: {"user", "points", "softcore", "last"}. Raises when the site
    refuses or knows nobody by that name. / Qui est ce compte, pour l'essayer depuis la fenêtre."""
    d = ask("API_GetUserProfile.php", user, key, base)
    if not isinstance(d, dict) or not d.get("User"):
        raise Refused("no such user")
    return {"user": str(d["User"]), "points": _int(d.get("TotalPoints")), "softcore": _int(d.get("TotalSoftcorePoints")),
            "last": str(d.get("RichPresenceMsg") or "")}


def _int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def settings(cfg):
    """(on, user, key, every) from the "retroachievements" part of the settings. / Depuis les réglages."""
    ra = cfg.get("retroachievements") if isinstance(cfg, dict) and isinstance(cfg.get("retroachievements"), dict) else {}
    user, key = str(ra.get("user") or "").strip(), str(ra.get("key") or "").strip()
    try:
        every = max(LEAST, float(ra.get("every", EVERY)))
    except (TypeError, ValueError):
        every = EVERY
    return bool(ra.get("enabled")) and bool(user) and bool(key), user, key, every


class Watch:
    """Asks the site while a game is played and hands the new achievements to the engine's queue.
    / Interroge le site pendant une partie et donne les nouveaux succès à la file du moteur."""

    def __init__(self, cfg, q, log, base=API, start=True):
        self.on, self.user, self.key, self.every = settings(cfg)
        self.q, self.log, self.base = q, log, base
        self.known = False                # the site has said who this account is / le site a dit qui est ce compte
        self.seen = set()                 # (achievement, date) already known / déjà connus
        self.fresh = True                 # the next answer is where things stand, not news / un état des lieux, pas une nouvelle
        self.playing = False
        self.until = 0.0                  # asked until then once the game is closed / demandé jusque-là, jeu fermé
        self.hold = 0.0                   # nothing asked before / rien demandé avant
        self.last = -99.0                 # the last question / la dernière question
        self.said = None                  # the last failure said, not to repeat it every time / la dernière panne dite
        self.stop_ev = threading.Event()
        self.wake = threading.Event()
        self.thread = None
        if self.on and start:
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def game(self, on):
        """A game starts or is closed. What was unlocked before a game starts is not news: the site is asked at once
        where things stand. / Un jeu démarre ou se ferme. Ce qui était débloqué avant n'est pas une nouvelle."""
        now = time.monotonic()
        if on and not self.playing and now >= self.until:
            self.fresh = True
            self.wake.set()
        if self.playing and not on:
            self.until = now + AFTER
        self.playing = bool(on)

    def close(self):
        self.stop_ev.set()
        self.wake.set()

    def _run(self):
        self.look()                                               # who the account is, said in the log at the start / au départ
        while not self.stop_ev.is_set():
            woken = self.wake.wait(self.every)
            self.wake.clear()
            now = time.monotonic()
            if self.stop_ev.is_set() or now < self.hold or (woken and now - self.last < SOON):
                continue
            if self.playing or now < self.until:
                self.look()

    def _failed(self, e):
        if isinstance(e, urllib.error.HTTPError) and e.code == 429:
            self.hold = time.monotonic() + HOLD
        reason = why(e)
        if reason != self.said:
            self.said = reason
            self.log(tr(f"RetroAchievements : {reason}, nouvel essai plus tard", f"RetroAchievements: {reason}, tried again later"))
        return 0

    def look(self):
        """One question, the new achievements handed over. Returns how many. / Une question, les nouveaux succès donnés."""
        self.last = time.monotonic()
        try:
            if not self.known:                                    # a name the site does not know would never say so otherwise
                who = profile(self.user, self.key, self.base)
                self.known = True
                self.log(tr(f"RetroAchievements : le site répond pour {who['user']}", f"RetroAchievements: the site answers for {who['user']}"))
            items = ask("API_GetUserRecentAchievements.php", self.user, self.key, self.base, m=LOOK_BACK)
            if not isinstance(items, list):
                raise Refused("not a list")
        except Exception as e:
            return self._failed(e)
        if self.said is not None:
            self.said = None
            self.log(tr("RetroAchievements : le site répond de nouveau", "RetroAchievements: the site answers again"))
        items = [it for it in items if isinstance(it, dict)]
        if self.fresh:
            self.fresh = False
            self.seen = {(it.get("AchievementID"), it.get("Date")) for it in items}
            return 0
        new = [it for it in items if (it.get("AchievementID"), it.get("Date")) not in self.seen]
        for it in sorted(new, key=lambda it: str(it.get("Date") or "")):
            self.seen.add((it.get("AchievementID"), it.get("Date")))
            n = of = None
            try:
                g = ask("API_GetGameInfoAndUserProgress.php", self.user, self.key, self.base, g=it.get("GameID"))
                of = _int(g.get("NumAchievements"), None)
                n = _int(g.get("NumAwardedToUser"), None)
            except Exception:
                pass                                              # the count is a plus, the news goes without it / un plus
            self.q.put(("ev", {"t": "achievement", "title": str(it.get("Title") or ""), "description": str(it.get("Description") or ""),
                               "points": _int(it.get("Points")), "game": str(it.get("GameTitle") or ""),
                               "hardcore": bool(_int(it.get("HardcoreMode"))), "n": n, "of": of}))
        return len(new)
