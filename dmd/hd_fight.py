"""Fighting game effects on the HD screen.

Stage backdrop (city at night, temple, harbor, ruins, arena, desert, snow, jungle...) that follows the game's
stage when its address is known ("backdrop" picks the theme, "stage" numbers it), with a wipe and the place name.
Sparks and shards on every hit, combo counter, first attack, super move (the screen darkens, light rays),
danger when health is low (red heartbeat), exploding K.O., DOUBLE K.O., TIME UP, PERFECT, confetti for the
winner, next King of Fighters fighter, "FIGHT !". Everything comes from the health bars, the timer, the
fighters' names and the stage values.

Effets des jeux de combat sur l'écran HD.

Décor du stage (ville la nuit, temple, port, ruines, arène, désert, neige, jungle), qui change avec le stage
du jeu quand son adresse est connue (valeur « stage »), avec un volet et le nom du stage.
Étincelles et éclats à chaque coup, compteur de combo, premier coup du round, super coup (l'écran s'assombrit,
rayons de lumière), danger quand il reste peu de vie (battement de cœur rouge), K.O. qui explose, DOUBLE K.O.,
TIME UP, PERFECT, confettis pour le vainqueur, combattant suivant des King of Fighters, « FIGHT ! ».

Tout se déduit des barres de vie (health, health_p2), du chrono, du nom des combattants et du stage.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFilter

from . import hd_stages
from .hd_bg import Backdrop
from .hd_fx import FX, Particle
from .hd_dm import DMShow
from .hd_moves import Moves
from .hd_themes15 import CPS_STAGES
from . import hd_themes18
from .i18n import tr

STAGE_STYLE = hd_themes18.STYLE     # the stages of The King of Fighters '98 register in hd_bg.BUILDERS as their module is
                                    # imported; their style is read here (the CI's pyflakes took the bare import for an unused
                                    # one) / les décors de KOF '98 s'enregistrent à l'import ; leur style se lit ici

GOLD = (255, 214, 120)
WHITE = (255, 255, 255)
RED = (255, 64, 44)
CREAM = (238, 228, 208)
# FIGHT ! waits for the round's timer to start counting down (the game's own FIGHT or GO), this long at most after the
# bars filled (a timer set to infinite). The King of Fighters '98 says GO 6.5 s after ROUND, and its first round has the
# entrances of the fighters before / FIGHT ! attend que le chrono du round décompte (le FIGHT ou le GO du jeu), au plus ce
# temps après que les barres se sont remplies ; GO 6,5 s après ROUND, et les entrées des combattants avant au premier round
FIGHT_WAIT = 12.0         # its first second counted down tells it / sa première seconde décomptée le dit
FIGHT_WAIT_SUB = 20.0     # its fraction of a second moving tells it at once / sa fraction de seconde le dit tout de suite
# The King of Fighters '97 and '98 keep the state of the fight ("_fight_state"): 0x18 when READY comes, the fight (bit 1,
# 0x1A) when GO is over and the timer runs. GO comes 1.15 s after READY, 0.65 s before the timer (the video, 1.31.1)
# l'état du combat : 0x18 quand READY arrive, le combat (bit 1) quand GO est fini et que le chrono tourne ; GO vient
# 1,15 s après READY, 0,65 s avant le chrono (la vidéo)
READY_STATE = 0x18
# the log of The King of Fighters '98 (1.32 test 8b): after a K.O. the state goes 0x19 and 0x01 by turns, then stays at
# 0x01, and the next round's intro starts at 0 (ROUND n at once on the game's screen, its next fighter 1.5 s after), READY
# (0x18) 4 to 5 s later, the fight 0x1A. Between the select screens and a first round it stays at 0, READY says it.
# Le log : après un K.O. l'état passe par 0x19 et 0x01 tour à tour, puis reste à 0x01, et l'intro du round suivant
# commence à 0 (ROUND n tout de suite à l'écran du jeu, le combattant suivant 1,5 s après), READY 4 à 5 s plus tard, le
# combat 0x1A. Entre les écrans de sélection et un premier round il reste à 0, READY le dit.
INTRO_STATE = 0x00
ROUND_OVER = (0x01, 0x19)
READY_GO = 1.15
READY_MIN = 2.5           # READY never comes sooner after the bars filled / READY ne vient jamais plus tôt
MATCH_END = 5.5           # the winner of a match in big letters, this long (1.31.1) / le vainqueur du match, ce temps
VS_FORGET = 20.0          # the wins of two humans forgotten when one of them left that long ago (1.32) / victoires oubliées
# a select screen, or the fight's, once it has lasted that long: a screen of a moment does not start or end a fight (1.32)
# un écran de sélection, ou celui du combat, une fois qu'il a duré ce temps : un écran d'un instant ne lance ni ne finit rien
SELECT_HOLD = 0.4
TIMEUP_HOLD = 4.0         # no select screen this long after TIME UP: KOF 2002 keeps no fight (0) for 3 s there (1.33 test 50)
JUDGE_WAIT = 0.9          # the winner on time judged this long after TIME UP, the last blow landed (1.33) / jugé après
ROUNDS_TO_WIN = 2         # rounds won that end a match, in a game that counts no round of its own (1.33) / rounds gagnés
CONFETTI = ((255, 80, 80), (255, 210, 60), (80, 220, 255), (120, 255, 140), (255, 120, 220), (255, 255, 255))

# place shown under STAGE n, for each theme ("fight_city" uses "city") / nom du lieu sous STAGE n
STAGE_NAMES = {"arena": ("ARÈNE", "ARENA"), "city": ("VILLE", "CITY"), "temple": ("TEMPLE", "TEMPLE"),
               "harbor": ("PORT", "HARBOR"), "ruins": ("RUINES", "RUINS"), "desert": ("DÉSERT", "DESERT"),
               "snow": ("MONTAGNE", "MOUNTAIN"), "jungle": ("JUNGLE", "JUNGLE"), "base": ("BASE", "BASE"),
               "city_war": ("CHAMP DE BATAILLE", "BATTLEFIELD"), "castle": ("CHÂTEAU", "CASTLE"), "market": ("MARCHÉ", "MARKET"),
               "factory": ("ACIÉRIE", "STEEL MILL"), "gothic": ("MANOIR", "MANOR"), "palace": ("PALAIS", "PALACE"),
               "thai": ("TEMPLE D'OR", "GOLDEN TEMPLE"), "lab": ("LABORATOIRE", "LABORATORY"),
               "kof_osaka": ("OSAKA", "OSAKA"), "kof_china": ("CHINE", "CHINA"), "kof_korea": ("CORÉE", "KOREA"),
               "kof_mideast": ("MOYEN-ORIENT", "MIDDLE EAST"), "kof_spain": ("ESPAGNE", "SPAIN"), "kof_yard": ("DÉPÔT", "TRAIN YARD"),
               "kof_dojo": ("DOJO", "DOJO"), "kof_wharf": ("QUAI", "WHARF"), "kof_noah": ("BLACK NOAH", "BLACK NOAH")}


def stage_name(theme):
    fr, en = STAGE_NAMES.get(theme) or STAGE_NAMES.get(theme.replace("fight_", ""), ("", ""))
    return tr(fr, en)


def _n(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def shard_img(color, s):
    w, h = max(6, int(16 * s)), max(4, int(9 * s))
    k = 4
    img = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(w * k * 0.2, 0), (w * k, 0), (w * k * 0.8, h * k), (0, h * k)], fill=color + (255,))
    d.line([(w * k * 0.22, 2 * k), (w * k * 0.95, 2 * k)], fill=(255, 255, 255, 200), width=k)
    return img.resize((w, h), Image.LANCZOS)


def confetti_img(color, s):
    w, h = max(4, int(12 * s)), max(3, int(7 * s))
    img = Image.new("RGBA", (w, h), color + (255,))
    ImageDraw.Draw(img).line([(0, 0), (w, 0)], fill=(255, 255, 255, 160), width=1)
    return img


def stable_index(text, n):
    return sum(ord(c) * (i + 1) for i, c in enumerate(text or "")) % max(1, n)


class FightFX:
    def __init__(self, hd, rng=None):
        self.hd, self.pg, self.s = hd, hd.pg, hd.s
        self.W, self.H = hd.W, hd.H
        self.rng = rng or random.Random()
        self.fx = FX(hd, random.Random(self.rng.random()))
        self.bd = Backdrop(hd, "arena", random.Random(self.rng.random()), threaded=False)
        self.bd.static = True
        self.bd.dim = getattr(hd, "dim_fight", None)                   # darker under the fight (1.32) / plus sombre
        self.bd.no_neons = True                                       # no shop signs at the level of the names (1.32)
        self.buf = None
        self.dark = None
        self.key = None
        self._reset(-99.0)
        for name, col in (("shard_g", (48, 240, 160)), ("shard_y", (255, 214, 60)), ("shard_r", (255, 70, 50))):
            self.fx.sp.register(name, shard_img(col, self.s))
        for i, col in enumerate(CONFETTI):
            self.fx.sp.register(f"conf{i}", confetti_img(col, self.s))
        self.danger_imgs = {}
        self.bands = {}
        self.idle = False
        self.select = False                                           # a select screen the game says / écran de sélection
        self.idle_attract = False                                     # nobody plays (the attract screen) / personne ne joue
        self.rays = None
        self._rays()                                                  # préparés d'avance : pas d'à-coup au premier super
        self.moves = Moves(hd)                                        # the desperation moves (1.32) / les coups désespérés
        self.dm = DMShow(self)                                        # their show (1.33 test 51) / leur spectacle
        self.hyper_lv = {}                                            # the gauge level seen, for the supers (1.36)
        self.warm = self._warm_list()

    def _warm_list(self):
        """Textes et halos préparés petit à petit pendant les moments calmes (pas d'à-coup au premier coup)."""
        hd, S, sp, s = self.hd, self.hd.S, self.fx.sp, self.s
        out = []
        for text, size in (("FIGHT !", 112), ("PERFECT !", 112), ("TIME UP", 112), ("DOUBLE K.O.", 112), ("WIN !", 72),
                           (tr("MATCH NUL", "DRAW GAME"), 112)):
            out.append((hd.text, (text, "stencil", S(size), GOLD if "K.O." not in text else RED, 0.8 if size > 100 else 0.6)))
        for n in range(2, 13):
            out.append((hd.text, (f"{n} HITS", "stencil", S(58 + min(20, n * 3)), GOLD, 0.6)))
        out.append((hd.text, (tr("PREMIER COUP", "FIRST ATTACK"), "stencil", S(44), (255, 240, 200), 0.6)))
        out.append((hd.text, (tr("ENTRE EN SCÈNE", "NEXT FIGHTER"), "bold", S(26), GOLD, 0)))
        for side in ("p1", "p2"):
            for lv in range(1, 7):
                out.append((self._danger_img, (side, lv)))
        for color, rmax in (((255, 245, 220), 200), ((255, 130, 50), 320), ((255, 236, 190), 128), ((255, 150, 50), 160),
                            ((255, 210, 120), 160), ((255, 110, 40), 160)):
            for r in (16, 20, 25, 32, 40, 50, 64, 80, 100, 128, 160, 200, 256, 320):
                if r > rmax:
                    break
                for lv in range(12, 0, -1):
                    out.append((sp.glow, (r * s, color, lv, 0.8 if color == (255, 245, 220) else 0.35)))
        return out

    def _warm_step(self, budget):
        import time as _t
        end = _t.perf_counter() + budget
        while self.warm and _t.perf_counter() < end:
            fn, args = self.warm.pop(0)
            try:
                fn(*args)
            except Exception:
                self.warm = []

    def _reset(self, now):
        self.prev = {}
        self.combo = {"p1": [0, -99.0], "p2": [0, -99.0]}
        self.combo_txt = {"p1": None, "p2": None}
        self.ko_t = -99.0
        self.fight_t = -99.0
        self.first = False
        self.stage_v = None
        self.stage_t = -99.0
        self.stage_changed = set()
        self.stage_label = None
        self.chars = {"p1": None, "p2": None}
        self.next_t = {"p1": -99.0, "p2": -99.0}
        self.next_name = {"p1": "", "p2": ""}
        self.win = None              # [côté, moment, PERFECT ?, déjà fêté ?]
        self.banner = None           # (texte, couleur, début, durée)
        self.judge = None            # when the winner on time is judged (TIME UP) / quand le vainqueur au temps est jugé
        self.timeup_t = -99.0        # when TIME UP last showed / quand TIME UP s'est affiché
        self.dm_seen = {}            # side -> (time, word) of the last DM ! or SDM ! shown / le dernier montré
        if getattr(self, "dm", None) is not None:
            self.dm.reset()
        self.super_t = -99.0
        self.super_xy = (0, 0)
        self.health = {"p1": None, "p2": None}
        self.prev_time = None
        self.rounds = {"p1": None, "p2": None}     # rounds won read in the game / rounds gagnés lus dans le jeu
        self.round_t = {"p1": -99.0, "p2": -99.0}
        self.live_t = -99.0                        # when somebody began to play / quand quelqu'un s'est mis à jouer
        self.zero_t = {}                           # when each bar fell to 0 / quand chaque barre est tombée à 0
        # 1.31, the rounds of a King of Fighters match / les rounds d'un match de King of Fighters
        self.round_v = None                        # the round of the match read in the game, from 0 / le round du match
        self.round_show = -99.0                     # when ROUND n shows, before FIGHT ! / quand ROUND n s'affiche
        self.round_sub = ""                        # the place of a new match under its first round / le lieu sous ROUND 1
        self.place_next = ""                       # the place of the match to come / le lieu du match qui vient
        self.ko_side = None                        # (loser, t): K.O. in red on its half / K.O. en rouge de son côté
        self.win_side = None                       # (winner, t): WIN in gold on its half / WIN doré de son côté
        self.ko_until = -99.0                      # until the K.O. and the WIN are over / jusqu'à la fin du K.O. et du WIN
        self.out = None                            # (winner, loser, t): a team eliminated, the match won / une équipe éliminée
        # fighters of each team beaten when the fight began (GO): the game counts a K.O. a moment before its bar is read
        # empty, so the count read while the bar is up already had it (1.31.1, a team out after its second fighter)
        # combattants battus de chaque équipe au début du combat (GO) : le jeu compte un K.O. juste avant que sa barre se
        # lise vide, le compte lu barre levée l'avait déjà (une équipe éliminée après son deuxième combattant)
        self.lost_go = {"p1": None, "p2": None}
        self.lost_raw = {"p1": None, "p2": None}   # as last read / tel que lu la dernière fois
        self.next_wait = {"p1": None, "p2": None}  # the next fighter counted before the K.O.: its band waits / le suivant attend
        self.hold = {"p1": None, "p2": None}       # (name, beaten) shown until the band of the next one / montrés jusque-là
        self.humans = {"p1": True, "p2": False}    # who plays, the other side is the computer / qui joue
        self.time_seen = -99.0                     # when the timer last moved / quand le chrono a bougé
        self.time_tick = -99.0                     # when it last counted a second down / quand il a décompté une seconde
        self.time_reset = False                    # put back to 0 at a round's start, not shown / remis à 0, pas affiché
        # 1.31.1, FIGHT ! with the game's GO / FIGHT ! avec le GO du jeu
        self.fight_wait = None                     # (earliest, since): FIGHT ! waits for the timer / attend le chrono
        self.timer_read = False                    # the game reads its timer / le jeu lit son chrono
        self.sub_read = False                      # and its fraction of a second / et sa fraction de seconde
        self.run_t = -99.0                         # when the timer was last seen counting down / quand il a décompté
        self.sub_prev = None                       # the timer's fraction of a second ("_time_sub") / sa fraction de seconde
        self.sub_moves = []                        # when it changed lately / quand elle a changé dernièrement
        self.sub_start = None                      # the value it holds until FIGHT, if the game says it / sa valeur d'attente
        self.fs_prev = None                        # the fight's state last read ("_fight_state") / l'état du combat
        self.round_t0 = None                       # when the bars of this round filled / quand les barres se sont remplies
        self.fight_why = ""                        # what gave FIGHT ! (log) / ce qui a donné FIGHT !
        self.run_logged = True                     # the timer's start of this round logged / le départ du chrono noté
        # 1.32, the matches won by each of two humans (as in Puzzle Bobble) / les matchs gagnés par chacun de deux humains
        self.wins = {"p1": 0, "p2": 0}
        self.win_pop = {"p1": None, "p2": None}    # when one more came, its number pops / quand il en vient un, il grossit
        # 1.33 test 6 (the capture of Fatal Fury): a game that counts no round gets its rounds counted here, from the
        # K.O. and TIME UP, ROUND n and VICTOIRE after two rounds won; a game that keeps its rounds won ("rounds") gives
        # them / un jeu qui ne compte pas ses rounds les voit comptés ici, d'après les K.O. et TIME UP
        self.rounds_won = {"p1": 0, "p2": 0}
        self.round_draws = 0
        self.won_here = {"p1": 0, "p2": 0}         # rounds won as seen here (K.O., TIME UP), whatever the game reads
        self.lost_named = {}                       # "_lost" as the name of each side was last set / quand le nom a changé
        self.rounds_game = False                   # "rounds" read in the game / « rounds » lu dans le jeu
        self.hd_round_value = None                 # "round" read in the game / « round » lu dans le jeu
        self.win_add = None                        # (winner, t): counted when VICTOIRE shows / compté quand VICTOIRE s'affiche
        self.vs_t = -99.0                          # when both players were last human / quand les deux étaient humains
        # 1.32 test 6, the video: the screens between the select screens and the fight / les écrans entre la sélection et
        self.sel_raw = None                        # the select screen as last read / l'écran de sélection tel que lu
        self.sel_t = -99.0                         # since when / depuis quand
        self.sel_on = False                        # as it counts, once it lasted SELECT_HOLD / tel qu'il compte
        self.sel_phase = {}                        # per side, where the select screens stand: "chars" (the slots fill
        # pick by pick), "picked" (the three in), "order" (the orders come one by one), "done" / où en est la sélection
        self.sel_lost = {}                         # "_lost" as last read there / « _lost » tel que lu
        self.time_stale = None                     # the last match's timer, not shown in the new one / le chrono d'avant
        self.fs_known = False                      # the game keeps the state of the fight / le jeu garde l'état du combat
        self.in_round = False                      # a match going, from its first round (state of the fight) / un match
        self.match_done = False                    # its last K.O. seen, until the next one / son dernier K.O. vu
        self.scr_prev = None                       # en cours ; the screen, the timer and the state last logged / notés
        self.tv_prev = None
        self.fs_log = None
        self.next_round = {"p1": False, "p2": False}   # its next fighter shown when the round starts / au début du round

    def round_glow(self, side, now):
        """1 when the side just won a round, down to 0 in 1.5 s (its last star glows). / L'étoile du round gagné brille."""
        k = (now - self.round_t.get(side, -99.0)) / 1.5
        return 0.0 if k >= 1 or k < 0 else 1.0 - k

    def _rounds(self, vals, now, play=True):
        """The rounds won read in the game (Street Fighter II, Alpha): one more is the winner of the round, whatever the
        health bars said. / Un round gagné de plus désigne le vainqueur, quoi qu'aient dit les barres de vie."""
        for side, key in (("p1", "rounds"), ("p2", "rounds_p2")):
            r = _n(vals.get(key))
            old = self.rounds.get(side)
            if play and r is not None and old is not None and r == old + 1:
                self.round_t[side] = now
                if self.win is None or self.win[0] != side:
                    self.win = [side, now + 0.2, (self.health.get(side) or 0) >= 99, False]
            self.rounds[side] = r

    def stages(self, game):
        """Themes of the game's stages, indexed by the "backdrop" value; an unknown theme becomes the arena, so that the
        places keep their index. / Thèmes des décors du jeu ; un thème inconnu devient l'arène."""
        lst = ((game or {}).get("hd") or {}).get("stages")
        if lst:
            return [s if s in hd_stages.hd_bg.BUILDERS else "arena" for s in lst]
        return list(hd_stages.FIGHT_STAGES) + (list(CPS_STAGES) if (game or {}).get("cps") else [])   # Capcom: their stages too

    @staticmethod
    def place(game, pick, theme):
        """Place shown under STAGE n: the game's own ("hd" "places", [french, english] by backdrop value, the countries of
        Street Fighter II for example), else the theme's. / Le lieu du jeu (pays de Street Fighter II...), sinon celui du thème."""
        places = ((game or {}).get("hd") or {}).get("places")
        if isinstance(places, list) and places:
            p = places[int(pick) % len(places)]
            if isinstance(p, list) and len(p) == 2 and all(isinstance(x, str) for x in p):
                return tr(p[0], p[1])
            if isinstance(p, str):
                return p
        return stage_name(theme)

    def geom(self):
        """Place des barres de vie, comme dans HDRenderer.draw_fight."""
        S, W = self.hd.S, self.W
        cx = W / 2
        bw = int(cx - S(160) - S(40))
        return {"p1": (S(40), S(176), bw, S(50)), "p2": (int(cx + S(160)), S(176), bw, S(50)), "cx": cx}

    # ------------------------------------------------------------ ce qui a changé
    def update(self, vals, now, key, game=None, idle=False, hist=None):
        """idle: nobody plays, the game's own demo runs behind the attract screen. Its fights change the health
        bars, but no spark, banner or K.O. is shown for them. hist: the stick and buttons read ("_in_p1", "_in_p2"),
        for the desperation moves (1.32). / Personne ne joue : pas d'effet pour la démo du jeu. hist : le stick et les
        boutons lus, pour les coups désespérés."""
        stages = self.stages(game)
        if key != self.key:
            self.key = key
            self._reset(now)
            self.bd.set_theme(stages[stable_index(key, len(stages))], now, wipe=0)
            self.bd.prebuild(stages)                                  # les autres stages se préparent en arrière-plan
        self.fx.update(now)
        self._vs(vals, now)
        # a select screen the game says (King of Fighters, Real Bout Special: "select", 1.31.1): no fight there, its values
        # are only followed as on the attract screen / un écran de sélection que dit le jeu : pas de combat, valeurs suivies
        jsel = _n(vals.get("select")) == 1
        if jsel or idle:
            self.in_round = self.match_done = False                   # no match going / pas de match en cours
            self.rounds_won, self.round_draws = {"p1": 0, "p2": 0}, 0
            self.won_here = {"p1": 0, "p2": 0}
            self.judge = None
        raw = jsel
        fs_now = _n(vals.get("_fight_state"))
        self.fs_known = fs_now is not None
        # the game keeping the state of the fight (King of Fighters '97 and '98): no fight (0) while no match is going,
        # the screens between the select and the first round, or after a match, are select screens too (1.32 test 8b,
        # the log) / sans combat (0) tant qu'aucun match n'est en cours : les écrans entre la sélection et le premier
        # round, ou après un match, sont aussi des écrans de sélection
        r1 = False
        tv_was = self.tv_prev                                         # the timer as last read / le chrono d'avant
        if self.fs_known and int(fs_now) == 0 and not self.in_round and now - self.timeup_t < TIMEUP_HOLD and not jsel:
            pass                                                      # the TIME UP of KOF 2002: 3 s with no fight (0),
            # its winner still on screen, not a select screen (a game of 9 November, 1.33 test 50) / le TIME UP de
            # KOF 2002 : 3 s sans combat, son vainqueur encore à l'écran, pas un écran de sélection
        elif self.fs_known and int(fs_now) == 0 and not self.in_round:
            # a first round's intro: the game sets its timer (0 -> 60) when the stage appears, ROUND 1 just after on its
            # screen, READY 6 s later (the log, 1.32 test 8d) / l'intro d'un premier round : le jeu met son chrono quand
            # le décor apparaît, ROUND 1 juste après à son écran, READY 6 s plus tard
            tv, tv0 = _n(vals.get("time")), self.tv_prev
            if not jsel and not idle and tv is not None and tv0 is not None and tv > tv0 and tv >= 30:
                self.in_round, self.match_done, r1 = True, False, True
            else:
                raw = True
        if not idle:
            self._log_screens(vals, fs_now, raw)
        if raw != self.sel_raw:
            self.sel_raw, self.sel_t = raw, now
        # the intro or READY of a first round ends those screens at once: ROUND 1 then / l'intro ou READY d'un premier
        # round finit ces écrans tout de suite : ROUND 1 alors
        if now - self.sel_t >= SELECT_HOLD or self.sel_raw is None or (not raw and (fs_now == READY_STATE or r1)):
            self.sel_on = raw
        select = self.sel_on
        if self.idle and not (idle or select) and self.fs_known:
            self.fs_prev = 0                                          # out of a select screen: no fight before it, its
            # READY is seen even if it came with the screen / pas de combat avant : son READY est vu
        self.sub_read = _n(vals.get("_time_sub")) is not None
        sdef = (((game or {}).get("memory") or {}).get("values") or {}).get("_time_sub")
        self.sub_start = _n(sdef.get("start")) if isinstance(sdef, dict) else None
        self.timer_read = self.sub_read or _n(vals.get("time")) is not None
        if self.idle and not idle:
            self.live_t = now                                         # START pressed: the game clears its fighters
            if self.select and not select and not self.idle_attract and not self.fs_known:   # out of the select screen:
                h1, h2 = _n(vals.get("health")), _n(vals.get("health_p2"))                   # the fight begins, bars
                if (h1 or 0) >= 50 and (h2 or 0) >= 50:               # full (KOF '99 keeps 1 % between its screens, the
                    # says it in the games that keep it) / la fin de la sélection, le combat commence (l'état le dit)
                    self.round_v = _n(vals.get("round"))
                    self.time_stale = _n(vals.get("time"))           # the last match's, until the game sets its own
                    self._fight(now)                                  # celui du match d'avant, jusqu'au nouveau
        self._select_phase(vals, game, select)
        self.idle, self.select, self.idle_attract = idle or select, select, idle   # the picks since then show (1.33)
        if idle or select:
            self._idle(vals, stages, game)
            self.moves.skip(hist)                                     # no fight: the inputs only followed / suivies
            return
        if r1:                                                        # the first round's intro: ROUND 1 / l'intro : ROUND 1
            self.round_v = _n(vals.get("round"))
            self._fight(now)
        p1m, p2m = vals.get("p1_mode"), vals.get("p2_mode")
        self.humans = {"p1": p1m in (1, 2) or p1m is None, "p2": p2m in (1, 2)}
        if isinstance((game or {}).get("moves"), dict):
            self.moves.update(vals, hist, now, key, game, self.humans)
            self._dm_watch(vals, game, now)
        if isinstance((game or {}).get("hyper"), dict):
            self._hyper_watch(vals, game["hyper"], now)
        # "round": the round of a King of Fighters match, from 0, one more at each K.O. (cheat "Select Current Round"),
        # shown as ROUND n when the next fight begins (1.31) / le round du match, ROUND n quand le combat suivant commence
        self.round_v = _n(vals.get("round"))
        self.hd_round_value = self.round_v
        rw1, rw2 = _n(vals.get("rounds")), _n(vals.get("rounds_p2"))
        self.rounds_game = rw1 is not None and rw2 is not None
        if self.rounds_game:                                          # the game's own count / le compte du jeu
            self.rounds_won = {"p1": int(rw1), "p2": int(rw2)}
        if self.round_v is None:                                      # counted here (1.33) / compté ici
            self.round_v = self.rounds_won["p1"] + self.rounds_won["p2"] + self.round_draws
        # a game without the state of its fights sets its timer as a round begins (0 -> 60, 90): ROUND n then, unless one
        # just showed (1.33, the captures of KOF '99 and Fatal Fury) / un jeu sans l'état de ses combats remet son
        # chrono quand un round commence : ROUND n alors, sauf s'il vient de s'afficher
        if not self.fs_known:
            tv, tv0 = _n(vals.get("time")), tv_was
            if tv is not None and tv0 is not None and tv > tv0 and tv >= 30 and tv0 < tv - 5 and now - self.round_show > 3.0 \
                    and now - self.fight_t > 3.0:
                self._fight(now)
        # "stage": match number in the run, from 0 (Rage of the Dragons, cheat "Select Stage"), shown as STAGE n.
        # "backdrop": backdrop of the fight (cheat "Select Backdrop"), picks the theme in the game's "hd" list.
        stage = _n(vals.get("stage"))
        back = _n(vals.get("backdrop"))
        pick = back if back is not None else stage
        sig = (stage, back)
        if pick is not None and sig != self.stage_v and self.round_v is not None and stage is None:
            # a game that counts its rounds: the new backdrop at once, its place under the ROUND 1 of the match
            # un jeu qui compte ses rounds : le nouveau décor tout de suite, son lieu sous le ROUND 1 du match
            theme = stages[int(pick) % len(stages)]
            if self.stage_v is None:
                self.bd.set_theme(theme, now, wipe=0)
            elif theme != self.bd.theme:
                self.bd.set_theme(theme, now)
            self.bd.set_round(0, now, fade=0)                         # a new match: its first round's look / 1er round
            self.place_next = self.place(game, pick, theme)
            self.stage_v = sig
        elif pick is not None and sig != self.stage_v:
            theme = stages[int(pick) % len(stages)]
            place = self.place(game, pick, theme)
            label = (f"STAGE {int(stage) + 1}", place) if stage is not None else (place, "")
            changed = {i for i in (0, 1) if self.stage_v is None or sig[i] != self.stage_v[i]}
            if self.stage_v is None:
                self.bd.set_theme(theme, now, wipe=0)
            elif now - self.stage_t < 1.5 and not (changed & self.stage_changed):
                if theme != self.bd.theme:               # the other value of the same change (round, then backdrop)
                    self.bd.set_theme(theme, now)
                self.stage_label = label
                self.stage_changed |= changed
            else:
                self.bd.set_theme(theme, now)
                self.stage_t = now
                self.stage_label = label
                self.stage_changed = changed
            self.stage_v = sig
        team = any(_n(vals.get(k)) is not None for k in ("_p1_lost", "_p2_lost"))
        for side in ("p1", "p2"):                                     # combattant suivant (équipes des KOF)
            name = vals.get(side + "_char")
            lr = _n(vals.get("_p1_lost" if side == "p1" else "_p2_lost"))
            if isinstance(name, str) and name:
                old = self.chars.get(side)
                if team:
                    # one more fighter of its team beaten: the next one comes, once the K.O. and the WIN are over (1.31).
                    # The game counts it a moment before the bar of the beaten one reads empty: its band and its name wait
                    # for that K.O. (3 s at most, a TIME UP lost) / un combattant de plus battu : le suivant entre, une fois
                    # le K.O. et le WIN finis. Le jeu le compte juste avant que la barre du battu se lise vide : son bandeau
                    # et son nom attendent ce K.O. (3 s au plus, un TIME UP perdu)
                    prev = self.lost_raw.get(side)
                    named = self.lost_named.get(side)
                    # the name read from the fighter on screen changes only as the next round begins, seconds after the
                    # count (KOF 2002, the capture, 1.33 test 10): a count gone up since the name was last set counts
                    # too / le nom lu sur le combattant à l'écran ne change qu'au round suivant : un compte monté depuis
                    if old and name != old and lr is not None and ((prev is not None and lr == prev + 1)
                                                                   or (named is not None and lr > named)):
                        self.next_name[side] = name
                        late = not (prev is not None and lr == prev + 1)      # the name came late, with the round
                        if self.hold[side] is None and not late:
                            self.hold[side] = (old, prev)
                        if self.fs_known and late and now - self.round_show < 3.0 and self.round_show > self.ko_t:
                            self.next_t[side] = max(now, self.round_show + 1.4)   # its ROUND n already showed / déjà montré
                            self.next_wait[side] = None
                            self.next_round[side] = False
                        elif self.fs_known:                                   # the next round says when it comes
                            self.next_wait[side] = now + 60.0                 # (1.32 test 8, not at the K.O.)
                            self.next_round[side] = True                      # le round suivant dit quand il entre
                        elif self.ko_side is not None and self.ko_side[0] == side and 0 <= now - self.ko_side[1] < 3.0:
                            self.next_t[side] = max(now, self.ko_until)       # its K.O. already seen / déjà vu
                        else:
                            self.next_wait[side] = now + 3.0
                            self.next_t[side] = max(now + 3.0, self.ko_until)
                    elif (old and name != old and lr is not None and lr == self.lost_named.get(side) and self.next_name[side]
                          and (self.next_wait[side] is not None or now <= self.next_t[side] + 1.7)):
                        # the name read again before its fighter enters: a read in between had another one (KYO for
                        # half a second before K', the KOF 2002 of 9 November, 1.33 test 50) / le nom lu à nouveau
                        # avant que son combattant entre : une lecture entre les deux en avait un autre
                        self.next_name[side] = name
                elif old and name != old and now - self.stage_t > 2.5:   # pas au changement de stage (nouvelle équipe)
                    self.next_t[side] = now
                    self.next_name[side] = name
                if name != old:
                    self.lost_named[side] = lr
                self.chars[side] = name
            self.lost_raw[side] = lr
        h1, h2 = _n(vals.get("health")), _n(vals.get("health_p2"))
        self.health = {"p1": h1, "p2": h2}
        t = _n(vals.get("time"))
        o1, o2 = self.prev.get("p1"), self.prev.get("p2")
        # both bars emptied at once while neither was low: the game clears its fighters (select screen after START, end
        # of a game), not a DOUBLE K.O. / les deux barres vidées d'un coup sans être basses : le jeu vide ses combattants
        cleared = (None not in (h1, h2, o1, o2) and h1 <= 0 and h2 <= 0 and o1 > 0 and o2 > 0 and max(o1, o2) > 50)
        if cleared:
            self.won_here = {"p1": 0, "p2": 0}                        # a new match / un nouveau match
            if not self.rounds_game:
                self.rounds_won, self.round_draws = {"p1": 0, "p2": 0}, 0
        for side, h in (("p1", h1), ("p2", h2)):
            old = self.prev.get(side)
            if h is not None and old is not None:
                if h < old:
                    if h <= 0 and (cleared or old >= 90 or now - self.live_t < 2.5):
                        continue                                      # a bar emptied, no blow did it / sans coup
                    other = self.zero_t.get("p2" if side == "p1" else "p1")
                    if h <= 0 and other is not None and now - other > 1.0:
                        continue                                      # the round was over: the winner's bar cleared
                    self._hit(side, old, h, now)
                elif old <= 0 < h and now - self.fight_t > 2.0 and not self.fs_known:   # combattant suivant ou nouveau
                    self._fight(now)                                                      # round (sans l'état du combat)
        if (h1 is not None and h2 is not None and self.prev.get("p1") is None and h1 >= 100 and h2 >= 100 and (t is None or t >= 50)
                and not self.fs_known):
            self._fight(now)                                          # début de round vu en arrivant (ou barres qui apparaissent)
        # TIME UP only when the timer counted down to 0, a second after another: at the start of a round King of Fighters
        # puts it back to 0 before its 60 or 90 seconds (1.31) / seulement quand le chrono a décompté jusqu'à 0 ;
        # au début d'un round, King of Fighters le remet à 0 avant ses 60 ou 90 secondes
        counting = now - self.time_tick < 2.5
        if t is not None and t != self.prev_time:
            if self.time_stale is not None and t != self.time_stale:
                self.time_stale = None                                # the game set the new one / le jeu a mis le nouveau
            step = self.prev_time is not None and t == self.prev_time - 1
            if step:
                self.time_tick = now
                self.run_t = now
            self.time_seen = now
            self.time_reset = t <= 0 and not step                     # put back to 0, not counted down / remis à 0
        # its fraction of a second ("_time_sub", The King of Fighters '98) moves at every frame while it runs, three moves
        # in 0.6 s tell it at once, a value put back at a round's start moves once / sa fraction de seconde bouge à chaque
        # image quand il tourne, trois changements en 0,6 s le disent tout de suite ; remise en place, elle ne bouge qu'une fois
        # a game that holds it at one value until its FIGHT ("start", X-Men: Children of the Atom 40): its first move away
        # from it tells it (1.36) / un jeu qui la tient à une valeur jusqu'à son FIGHT : la quitter le dit
        sub = _n(vals.get("_time_sub"))
        if sub is not None and self.sub_prev is not None and sub != self.sub_prev:
            self.sub_moves = [x for x in self.sub_moves if now - x < 0.6] + [now]
            if len(self.sub_moves) >= 3 or (self.sub_start is not None and self.sub_prev == self.sub_start):
                self.run_t = now
        self.sub_prev = sub
        fs = _n(vals.get("_fight_state"))
        if fs is not None and fs != self.fs_prev:
            fs = int(fs)
            if self.fs_prev is not None and self.round_t0 is not None:
                dt = now - self.round_t0
                self.hd.log(tr(f"Combat, état 0x{fs:02X} à {dt:.2f} s du début du round",
                               f"Fight, state 0x{fs:02X} at {dt:.2f} s from the round's start"))
            if fs == INTRO_STATE and self.fs_prev in ROUND_OVER and self.in_round:
                # the next round's intro after a K.O.: ROUND n at once, as the game shows it, its next fighter after it
                # (the log and video, 1.32 test 8b) / l'intro du round suivant : ROUND n tout de suite, comme le jeu
                self.round_v = _n(vals.get("round"))
                self._fight(now)
                for side in ("p1", "p2"):                               # its next fighter, after ROUND n / son suivant
                    if self.next_round[side]:
                        self.next_round[side] = False
                        self.next_wait[side] = None
                        self.next_t[side] = self.round_show + 1.4
            elif fs == READY_STATE and (not self.in_round or (self.fight_wait is None and self.round_show < self.ko_t)):
                # the first round of a match: nothing tells its intro, ROUND 1 at READY, FIGHT ! after it with GO (and a
                # next round whose intro was not seen) / le premier round d'un match : rien ne dit son intro, ROUND 1 à
                # READY, FIGHT ! ensuite avec GO (et un round suivant dont l'intro n'a pas été vue)
                self.round_v = _n(vals.get("round"))
                self.in_round, self.match_done = True, False
                self._fight(now)
                self.fight_t = self.round_show + 1.35
                self.fight_why = "READY"
            if (fs & 0x02 or fs in ROUND_OVER) and not self.match_done:
                self.in_round = True                                  # a match going: a fight or a K.O. / un match en cours
            if fs & 0x02:                                             # the fight runs / le combat a commencé
                self.run_t = now
            elif fs == READY_STATE and self.fight_wait is not None and now - self.fight_wait[1] >= READY_MIN:
                self.fight_t = min(self.fight_t, max(self.fight_wait[0], now + READY_GO))   # GO after READY
                self.fight_why = "READY"
            self.fs_prev = fs
        if self.fight_wait is not None:
            earliest, since = self.fight_wait
            if self.run_t > since:                                    # GO: the timer runs / le chrono tourne
                self.fight_t = min(self.fight_t, max(now, earliest))
                self.fight_wait = None
                self._go(self.fight_t, now, tr("chrono lancé", "timer running"))
            elif now >= self.fight_t:                                 # READY, or never ran (infinite time) / jamais lancé
                self.fight_wait = None
                self._go(self.fight_t, now, "READY + 1,15 s" if self.fight_why == "READY" else tr("délai maximum", "longest wait"))
        if not self.run_logged and self.run_t > (self.round_t0 or 0) and self.fs_prev is not None:
            self.run_logged = True                                    # its start, to set READY_GO / son départ
            self.hd.log(tr(f"Combat, le chrono démarre à {self.run_t - self.round_t0:.2f} s du début du round",
                           f"Fight, the timer starts at {self.run_t - self.round_t0:.2f} s from the round's start"))
        if (t is not None and self.prev_time is not None and t <= 0 < self.prev_time <= 2 and counting and now - self.ko_t > 2.0
                and (h1 or 0) > 0 and (h2 or 0) > 0):
            self.banner = ("TIME UP", GOLD, now, 1.6)                 # chrono à zéro sans K.O.
            self.timeup_t = now
            self.ko_until = now + 1.7
            self.judge = now + JUDGE_WAIT                             # the winner judged a moment later / jugé après
        if self.judge is not None and now >= self.judge and h1 is not None and h2 is not None:
            # the winner on time, judged once the last blow landed: a hit in flight at TIME UP still counts, and equal
            # bars are a draw, both fighters out (the capture, 1.33 test 7) / le vainqueur au temps, jugé une fois le
            # dernier coup arrivé : un coup en l'air à TIME UP compte encore, et des barres égales font match nul
            self.judge = None
            if h1 != h2:                                              # WIN once TIME UP is over / WIN après TIME UP
                self.win = ["p1" if h1 > h2 else "p2", max(now, self.ko_until), False, False]
                # the last fighter of a team lost on time: the team is out too (1.31.1) / perdu au temps, éliminée aussi
                loser = "p2" if h1 > h2 else "p1"
                idx = self.lost_go.get(loser)
                if idx is not None and idx >= 2 and (self.round_v is None or self.round_v >= 2):
                    self._match_won(self.win[0], loser, now, 3.8)
                self._round_over(self.win[0], now, 3.8)
            else:
                self.banner = (tr("MATCH NUL", "DRAW GAME"), GOLD, max(now, self.ko_until), 1.6)
                self.ko_until = max(now, self.ko_until) + 1.7
                self._round_over(None, now, 1.7)
        self.prev_time = t
        for side, h in (("p1", h1), ("p2", h2)):
            if h is not None and h <= 0:
                self.zero_t.setdefault(side, now)
            else:
                self.zero_t.pop(side, None)
        self._rounds(vals, now)
        for side in ("p1", "p2"):
            w = self.next_wait[side]
            if w is not None:                                         # waits for its K.O. and the WIN / attend son K.O.
                self.next_t[side] = max(w, self.ko_until)
                if now >= self.next_t[side]:
                    self.next_wait[side] = None
            if self.hold[side] is not None and self.next_wait[side] is None and now >= self.next_t[side]:
                self.hold[side] = None                                # its band came: the new name / son bandeau est venu
        if self.fight_wait is not None or now < self.fight_t:         # until GO, the count of the fighters beaten
            self.lost_go = dict(self.lost_raw)                        # jusqu'au GO, le compte des combattants battus
        if self.win is not None and not self.win[3] and now >= self.win[1]:
            self._celebrate(*self.win[:3])
            self.win[3] = True
        self.prev["p1"], self.prev["p2"] = h1, h2

    def _select_phase(self, vals, game, select):
        """Where the select screens stand, per side, as the game writes them (the captures of KOF '98 and '99, 1.33
        test 6): the character select empties the slots (0xFF) and fills them pick by pick ("chars"), then the three
        are in ("picked"); the order select counts the orders in "_lost", from 0 again ("order"). / Où en est la
        sélection : les cases vidées puis remplies ("chars"), les trois dedans ("picked"), puis les ordres un à un,
        « _lost » revenu à 0 et les comptant ("order")."""
        if not select:
            self.sel_phase = {}
            self.sel_lost = {}
            return
        derived = game.get("derived") if isinstance(game, dict) else None
        for side in ("p1", "p2"):
            names = ((derived or {}).get(side + "_char") or {}).get("names") or {}
            chars = [vals.get(f"_{side}_ch{i}") for i in range(3)]
            full = all(c is not None and str(c) in names for c in chars)
            lost = _n(vals.get(f"_{side}_lost"))
            ph = self.sel_phase.get(side)
            if not full:
                ph = "chars"
            elif ph in (None, "chars"):
                ph = "picked"
            if ph == "picked" and lost is not None and lost <= 0:
                ph = "order"
            elif ph == "order" and lost is not None and lost <= 0 and (self.sel_lost.get(side) or 0) > 0:
                ph = "done"                                           # the order set, "_lost" back to 0 / l'ordre mis
            self.sel_phase[side] = ph
            self.sel_lost[side] = lost

    def _idle(self, vals, stages, game=None):
        """Attract screen: the values are only followed (backdrop of the demo's stage, last health, names),
        so that nothing goes off when the game starts."""
        stage, back = _n(vals.get("stage")), _n(vals.get("backdrop"))
        pick = back if back is not None else stage
        if pick is not None and (stage, back) != self.stage_v:
            theme = stages[int(pick) % len(stages)]
            if self.stage_v is None:
                self.bd.set_theme(theme, self.fx.now, wipe=0)
            else:
                self.bd.set_theme(theme, self.fx.now)                   # the demo changes stage: wipe, no banner
            self.bd.set_round(0, self.fx.now, fade=0)                   # its first round's look / le look du 1er round
            self.stage_v = (stage, back)
            if _n(vals.get("round")) is not None and stage is None:   # the next match chosen on the select screen: its place
                self.place_next = self.place(game, pick, theme)
        self.stage_label = None
        # the winner of a match stays its time over the screen of the game after it (its quotes, 1.32 test 6)
        # le vainqueur d'un match reste son temps par-dessus l'écran qui suit (ses répliques)
        keep = self.out is not None and self.fx.now < self.out[2] + MATCH_END and not self.idle_attract
        if not keep:
            self.banner = None
            self.win = None
            self.ko_side = self.win_side = self.out = None
        self.round_show = -99.0
        if self.fight_wait is not None or self.fight_t > self.fx.now:
            self.fight_wait = None
            self.fight_t = -99.0
        for side in ("p1", "p2"):
            name = vals.get(side + "_char")
            if isinstance(name, str) and name:
                self.chars[side] = name
            self.lost_raw[side] = _n(vals.get("_p1_lost" if side == "p1" else "_p2_lost"))
            self.lost_go[side] = None
            self.next_wait[side] = self.hold[side] = None
            self.next_round[side] = False
        h1, h2 = _n(vals.get("health")), _n(vals.get("health_p2"))
        self.health = {"p1": h1, "p2": h2}
        self.prev["p1"], self.prev["p2"] = h1, h2
        self.prev_time = _n(vals.get("time"))
        self._rounds(vals, self.fx.now, play=False)

    def _hyper_watch(self, vals, hyper, now):
        """The supers of a game whose gauge has levels ("hyper" in the game file, 1.36), shown like a desperation move,
        its name over the marquee then on its side, the hits counted. X-Men ("spend": "top"): the gauge going from its top
        level back to the first one. Marvel vs. Capcom ("spend": "level"): any level spent, the super named when only one
        of the fighter's costs that many levels ("lv"), two levels at once without one being the team super ("team").
        / Les supers d'un jeu à niveaux, montrés comme un coup désespéré : la jauge qui retombe du plus haut niveau au
        premier (X-Men), ou chaque niveau dépensé (Marvel vs. Capcom)."""
        top = hyper.get("top", 3)
        by_level = hyper.get("spend") == "level"
        h1, h2 = _n(vals.get("health")), _n(vals.get("health_p2"))
        fresh = h1 is not None and h2 is not None and h1 >= 99.5 and h2 >= 99.5    # a new round, the gauges set again
        kind = tr(*hyper.get("label", ("HYPER X", "HYPER X")))
        for side in ("p1", "p2"):
            lv = _n(vals.get("power_level" if side == "p1" else "power_level_p2"))
            old = self.hyper_lv.get(side)
            self.hyper_lv[side] = lv
            if lv is None or old is None or fresh:
                continue
            spent = (old - lv) if by_level else (top if old >= top and lv <= 1 else 0)
            if spent <= 0:
                continue
            name = vals.get(side + "_char")
            moves = (hyper.get("moves") or {}).get(name.upper() if isinstance(name, str) else "") or []
            names = [str(m.get("name")) for m in moves if isinstance(m, dict) and m.get("name")
                     and (not by_level or (_n(m.get("lv")) or 1) == spent)]
            fighter = name if isinstance(name, str) else ""
            if len(names) == 1:                                       # the only one it can be / le seul possible
                self.dm.start(side, names[0], fighter, False, now, kind=kind)
            elif by_level and spent >= 2 and hyper.get("team"):       # both fighters at once / les deux à la fois
                self.dm.start(side, tr(*hyper["team"]), fighter, False, now, kind="")
            else:                                                     # which one is not known / lequel, on ne sait pas
                self.dm.start(side, kind, fighter, False, now, kind="")

    def _dm_watch(self, vals, game, now):
        """A DM ! or SDM ! the panel just told for a human: its show starts (the choice of 9 November, 1.33 test 51).
        / Un DM ! ou SDM ! que le panneau vient de dire pour un humain : son spectacle commence."""
        for side in ("p1", "p2"):
            if not self.humans.get(side):
                continue
            self.dm.prepare([row[0] for row in self.moves.rows(game, vals.get(side + "_char"))])
            r = self.moves.sides[side].result
            if r is None or r[2] not in ("DM !", "SDM !"):
                continue
            seen = self.dm_seen.get(side)
            if seen is not None and seen[0] == r[0]:
                if r[2] == "SDM !" and seen[1] != "SDM !":            # found an SDM a moment later (2002) / un SDM finalement
                    self.dm.upgrade(side, now)
                    self.dm_seen[side] = (r[0], r[2])
                continue
            self.dm_seen[side] = (r[0], r[2])
            if now - r[0] > 0.5:
                continue
            name = vals.get(side + "_char")
            rows = self.moves.rows(game, name)
            move = rows[r[1]][0] if 0 <= r[1] < len(rows) else ""
            self.dm.start(side, move, name if isinstance(name, str) else "", r[2] == "SDM !", now)

    def _hit(self, victim, old, new, now):
        fx, rng, S = self.fx, self.rng, self.hd.S
        in_dm = self.dm.hit(victim, old, new, now)                  # a hit of a desperation move: its name counts the hits
        g = self.geom()
        x, y, w, h = g[victim]
        d = old - new
        f = max(0.0, new / 100.0)
        ex = x + w * (1 - f) if victim == "p1" else x + w * f      # bord de la vie qui vient de partir
        ey = y + h / 2
        fx.glow(ex, ey, 16, 50 + d * 3, (255, 245, 220), 0.22, "front", 1.0, 0.0, hot=0.8)
        fx.sparks(ex, ey, int(8 + d * 1.4), (255, 230, 150), (250, 900), (190, 350), (0.25, 0.6), 1100, "front", 3, 34)
        col = "shard_g" if f > 0.5 else ("shard_y" if f > 0.25 else "shard_r")
        for _ in range(int(2 + d / 4)):                             # éclats de la barre qui tombent
            fx.obj(col, ex + rng.uniform(-10, 10) * self.s, ey, rng.uniform(-260, 260), -rng.uniform(250, 520), gravity=1600,
                   vrot=rng.uniform(-700, 700), life=0.9, rot=rng.uniform(0, 360))
        fx.shake(min(9.0, 1.5 + d * 0.35), 0.25)
        self.bd.excite(0.05 + d * 0.025)
        attacker = "p2" if victim == "p1" else "p1"
        ax, ay, aw, _ = g[attacker]
        if not self.first and now - self.fight_t < 60 and not in_dm:  # premier coup du round
            self.first = True
            old_t = self.combo_txt.get(attacker)
            if old_t is not None:
                old_t.dead = True
            self.combo_txt[attacker] = fx.text(tr("PREMIER COUP", "FIRST ATTACK"), ax + aw * 0.5, S(132), (255, 240, 200), 44,
                                               life=1.2, rise=10)
        if d >= 25:                                                 # super coup : l'écran s'assombrit, rayons de lumière
            self.super_t = now
            self.super_xy = (ex, ey)
            fx.shake(12, 0.5)
            fx.flash((255, 255, 255), 0.25, 0.15)
            self.bd.excite(1.2)
        if d >= 15:                                                 # gros coup : onde de choc
            r = fx.add(Particle("ring", ex, ey, now, 0.4, "front"))
            r.r0, r.r1, r.col, r.a0, r.a1, r.data = 10 * self.s, 170 * self.s, (255, 235, 200), 0.9, 0.0, 6 * self.s
            fx.flash((255, 240, 220), 0.1, 0.12)
            self.bd.excite(0.5)
        c = self.combo[attacker]
        c[0] = c[0] + 1 if now - c[1] < 0.7 else 1
        c[1] = now
        if in_dm:                                                   # the name of the move says the hits / le nom les dit
            old_t = self.combo_txt.get(attacker)
            if old_t is not None:
                old_t.dead = True
            self.combo_txt[attacker] = None
        elif c[0] >= 2:
            old_t = self.combo_txt.get(attacker)
            if old_t is not None:
                old_t.dead = True
            self.combo_txt[attacker] = fx.text(f"{c[0]} HITS", ax + aw * 0.5, S(132), GOLD, 58 + min(20, c[0] * 3), life=1.1, rise=15)
        if new <= 0:
            self.ko_t = now
            self.dm.ko(now)
            fx.explosion(x + w / 2, ey, 1.25, layer_back=False)
            fx.flash((255, 220, 200), 0.25, 0.25)
            fx.shake(14, 0.6)
            self.bd.excite(2.5)
            other = self.health.get(attacker)
            if other is not None and other <= 0:
                self.banner = ("DOUBLE K.O.", RED, now + 0.5, 1.6)
                self.ko_until = now + 2.2
                self._round_over(None, now, 2.2)
            else:
                perfect = other is not None and other >= 99
                # K.O. in big red letters on the loser's side, then WIN on the winner's (1.31), PERFECT after them;
                # the next fighter waits until they are over / K.O. en grosses lettres rouges du côté du perdant, puis WIN
                # du côté du gagnant, PERFECT après ; le combattant suivant attend qu'ils soient finis
                self.ko_side = (victim, now)
                self.ko_until = now + (4.4 if perfect else 2.7)
                self.win = [attacker, now + 0.6, perfect, False]
                if self.next_wait.get(victim) is not None and not self.next_round.get(victim):   # its next fighter counted
                    self.next_wait[victim] = now                         # just before / son suivant, compté juste avant
                idx = self.lost_go.get(victim)
                raw = self.lost_raw.get(victim)                          # counted just before: its third / son troisième
                if ((idx is not None and idx >= 2) or (raw is not None and raw >= 3)) and (self.round_v is None or self.round_v >= 2):
                    self._match_won(attacker, victim, now, 4.4 if perfect else 2.7)   # its third fighter: the team is
                    # out, after the WIN and the PERFECT / son troisième combattant : l'équipe est éliminée, après le WIN
                self._round_over(attacker, now, 4.4 if perfect else 2.7)

    def _log_screens(self, vals, fs, sel):
        """The screen of the game, its timer set again and the state of the fight outside the fights, in the log: to find
        on a cabinet what tells the intro of a first round (1.32 test 8b). / L'écran du jeu, son chrono remis et l'état du
        combat hors des combats, dans le journal : pour trouver sur une borne ce qui dit l'intro d'un premier round."""
        scr, tv = _n(vals.get("_screen")), _n(vals.get("time"))
        fsx = f"0x{int(fs):02X}" if fs is not None else "?"
        if scr is not None and scr != self.scr_prev:
            if self.scr_prev is not None:
                self.hd.log(tr(f"Combat, écran 0x{int(scr):04X} (état {fsx}, chrono {tv})",
                               f"Fight, screen 0x{int(scr):04X} (state {fsx}, timer {tv})"))
            self.scr_prev = scr
        if tv is not None and self.tv_prev is not None and tv != self.tv_prev and tv != self.tv_prev - 1:
            self.hd.log(tr(f"Combat, chrono {self.tv_prev} -> {tv} (état {fsx})", f"Fight, timer {self.tv_prev} -> {tv} (state {fsx})"))
        self.tv_prev = tv
        if fs is not None and sel and fs != self.fs_log:
            self.hd.log(tr(f"Combat, état {fsx} hors combat", f"Fight, state {fsx} outside a fight"))
        self.fs_log = fs if sel else None

    def _round_over(self, winner, now, later):
        """A round over, for a game that counts no round of its own (1.33): one more won, ROUND n follows; two won, the
        match is over, VICTOIRE. / Un round fini, pour un jeu qui ne compte pas ses rounds : un de plus gagné, ROUND n
        suit ; deux gagnés, le match est fini, VICTOIRE."""
        team = any(_n(v) is not None for v in (self.lost_raw.get("p1"), self.lost_raw.get("p2")))
        if winner is None:
            self.round_draws += 1
            return
        self.won_here[winner] += 1                                    # counted here, the game's own may come later
        if not self.rounds_game:
            self.rounds_won[winner] += 1
        if self.won_here[winner] >= ROUNDS_TO_WIN and not team:        # two rounds won in a game of single fighters:
            self._match_won(winner, "p2" if winner == "p1" else "p1", now, later)   # the match is over (Fatal Fury)
            self.rounds_won, self.round_draws = {"p1": 0, "p2": 0}, 0
            self.won_here = {"p1": 0, "p2": 0}

    def _match_won(self, winner, loser, now, later):
        """A team eliminated: VICTOIRE and the confetti once the WIN is over, one more match won for a human against a
        human (1.32). / Une équipe éliminée : VICTOIRE et les confettis après le WIN, un match gagné de plus entre humains."""
        if self.out is not None and -1.0 < now + later - self.out[2] < MATCH_END:
            return                                                    # the same match / le même match
        self.in_round, self.match_done = False, True                  # the match is over / le match est fini
        self.out = (winner, loser, now + later)
        self.ko_until = now + later + MATCH_END
        self.fx.later(later, self._confetti, 0, self.W, 150)
        if self.humans.get("p1") and self.humans.get("p2"):
            self.win_add = (winner, now + later)

    def _vs(self, vals, now):
        """The matches won by each of two humans: one more when VICTOIRE shows, all forgotten once one of them left
        VS_FORGET ago. / Les matchs gagnés par chacun : un de plus quand VICTOIRE s'affiche, oubliés quand l'un est parti."""
        if self.win_add is not None and now >= self.win_add[1]:
            side = self.win_add[0]
            self.wins[side] += 1
            self.win_pop[side] = now
            self.win_add = None
            self.hd.log(tr(f"Combat, victoires P1 {self.wins['p1']} P2 {self.wins['p2']}",
                           f"Fight, wins P1 {self.wins['p1']} P2 {self.wins['p2']}"))
        p1m, p2m = vals.get("p1_mode"), vals.get("p2_mode")
        if p1m in (1, 2) and p2m in (1, 2):
            self.vs_t = now
        elif now - self.vs_t > VS_FORGET and (self.wins["p1"] or self.wins["p2"]):
            self.wins = {"p1": 0, "p2": 0}
            self.hd.log(tr("Combat, victoires remises à zéro (un joueur est parti)", "Fight, wins back to 0 (a player left)"))

    def vs_on(self):
        """Two humans play: their wins under the credits. / Deux humains jouent : leurs victoires sous les crédits."""
        return bool(self.humans.get("p1") and self.humans.get("p2")) and not self.idle_attract

    def panel_on(self, side):
        """The panel of the desperation moves under a human's name, during a fight. / Le panneau, pendant un combat."""
        return bool(self.humans.get(side)) and not self.idle

    def _confetti(self, x0, x1, n):
        fx, rng = self.fx, self.rng
        for i in range(n):
            p = fx.obj(f"conf{rng.randint(0, len(CONFETTI) - 1)}", rng.uniform(x0, x1), -rng.uniform(10, 120) * self.s,
                       rng.uniform(-60, 60), rng.uniform(80, 200), gravity=60, vrot=rng.uniform(-500, 500), life=rng.uniform(2.6, 3.6),
                       rot=rng.uniform(0, 360))
            p.wob = rng.uniform(40, 90) * self.s
            p.drag = 0.4

    def _celebrate(self, side, t, perfect):
        """Le vainqueur : confettis au-dessus de son côté, WIN en grand de son côté, PERFECT si aucun coup reçu."""
        x, y, w, h = self.geom()[side]
        self._confetti(x, x + w, 70)
        old_t = self.combo_txt.get(side)
        if old_t is not None:
            old_t.dead = True
        now = self.fx.now
        self.win_side = (side, now)
        self.ko_until = max(self.ko_until, now + 2.1)
        self.bd.excite(1.5)
        if perfect:
            self.banner = ("PERFECT !", GOLD, now + 2.1, 1.6)         # once the WIN is over / une fois le WIN fini

    def _fight(self, now):
        # pas en même temps que le bandeau du stage, le K.O. et le WIN, ou le nom du combattant suivant
        busy = max([self.stage_t + 1.95 if now - self.stage_t < 2.0 else -99.0, self.ko_until if now < self.ko_until else -99.0] +
                   [t + 1.75 for t in self.next_t.values() if -0.1 <= now - t < 1.75 or 0 < t - now < 2.5])
        start = max(now, busy)
        if self.round_v is not None:                                  # ROUND n, then FIGHT ! / ROUND n, puis FIGHT !
            self.round_show = start
            self.round_sub, self.place_next = self.place_next, ""     # a new match: its place / un nouveau match : son lieu
            start += 1.35
        # the stage takes the look of this round (the time of day...), as the game between its rounds (1.32 test 9)
        # le décor prend le look de ce round (l'heure du jour...), comme le jeu entre ses rounds
        self.bd.set_round(self.round_v, now)
        # FIGHT ! with the game's own FIGHT or GO, when the round's timer starts counting down after ROUND n, FIGHT_WAIT
        # after the bars filled at the latest; a game that reads no timer shows it at once (1.31.1, in The King of
        # Fighters '98 it came with the names of the fighters, 5 s before READY and GO) / FIGHT ! avec le FIGHT ou le GO du
        # jeu, quand le chrono du round se met à décompter après ROUND n ; sans chrono lu, tout de suite (il venait avec
        # les noms des combattants, 5 s avant READY et GO)
        self.round_t0 = now
        self.fight_why = ""
        self.run_logged = False
        if self.timer_read:
            self.fight_wait = (start, now)
            self.fight_t = max(start + 1.0, now + (FIGHT_WAIT_SUB if self.sub_read else FIGHT_WAIT))
            self.sub_moves = []
            self.lost_go = dict(self.lost_raw)
        else:
            self.fight_wait = None
            self.fight_t = start
            self.lost_go = dict(self.lost_raw)
            self._go(start, now)
        self.first = False
        self.win = None

    def _go(self, t, now, why=""):
        """The shock wave of FIGHT ! when it comes. / L'onde de choc de FIGHT ! quand il arrive."""
        self.time_stale = None                                        # the fight runs: its timer / le combat : son chrono
        if why and self.fs_prev is not None and self.round_t0 is not None:      # the games that keep their state (log)
            self.hd.log(tr(f"Combat, FIGHT ! à {t - self.round_t0:.2f} s du début du round ({why})",
                           f"Fight, FIGHT ! at {t - self.round_t0:.2f} s from the round's start ({why})"))
        self.fx.later(max(0.0, t - now), self.bd.excite, 0.8)
        cx, cy = self.W / 2, self.hd.S(240)
        r = self.fx.add(Particle("ring", cx, cy, t + 0.12, 0.5, "front"))
        r.r0, r.r1, r.col, r.a0, r.a1, r.data = 30 * self.s, 520 * self.s, (255, 220, 150), 0.8, 0.0, 8 * self.s

    def ko_scale(self, now):
        k = (now - self.ko_t) / 0.22
        if k >= 1 or k < 0:
            return 1.0
        return 2.6 - 1.6 * (1 - (1 - k) ** 3)

    # ------------------------------------------------------------ dessin
    def begin(self, screen, now):
        ox, oy = self.fx.offset()
        target = screen
        if ox or oy:
            if self.buf is None or self.buf.get_size() != screen.get_size():
                self.buf = self.pg.Surface(screen.get_size()).convert()
            target = self.buf
        self.bd.draw(target, now, 0.0)
        k = (now - self.super_t) / 0.5
        if 0 <= k < 1:                                               # super coup : décor assombri, rayons
            if self.dark is None:
                self.dark = self.pg.Surface(screen.get_size()).convert()
                self.dark.fill((0, 0, 0))
            self.dark.set_alpha(int(170 * (1 - k)))
            target.blit(self.dark, (0, 0))
            rays = self._rays()
            lv = 1 - k
            r2 = rays.copy()
            r2.fill((int(255 * lv),) * 3, special_flags=self.pg.BLEND_RGB_MULT)
            x, y = self.super_xy
            target.blit(r2, (int(x - r2.get_width() / 2), int(y - r2.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
        self.fx.draw(target, "back")
        return target

    def _rays(self):
        if self.rays is None:
            size = int(900 * self.s)
            m = Image.new("L", (size, size), 0)
            d = ImageDraw.Draw(m)
            rng = random.Random(9)
            c = size / 2
            for i in range(44):
                a = i * math.tau / 44 + rng.uniform(-0.03, 0.03)
                w = rng.uniform(0.008, 0.02)
                d.polygon([(c, c), (c + math.cos(a - w) * c, c + math.sin(a - w) * c), (c + math.cos(a + w) * c, c + math.sin(a + w) * c)],
                          fill=rng.randint(90, 200))
            fade = Image.radial_gradient("L").resize((size, size)).point(lambda v: max(0, 255 - v * 255 // 181))
            from PIL import ImageChops
            m = ImageChops.multiply(m, fade).filter(ImageFilter.GaussianBlur(2 * self.s))
            self.rays = self.hd._surf(Image.merge("RGB", (m, m.point(lambda v: v * 9 // 10), m.point(lambda v: v * 7 // 10))))
        return self.rays

    def end(self, screen, target, now):
        if not getattr(self, "idle", False):                         # no health bar on the attract screen
            self._danger(target, now)
        self.fx.draw(target, "front")
        self.dm.draw(target, now)
        self._next_fighter(target, now)
        self._banners(target, now)
        self.fx.draw_flash(target)
        if target is not screen:
            ox, oy = self.fx.offset()
            screen.fill((0, 0, 0))
            screen.blit(target, (ox, oy))
        if self.warm and len(self.fx.parts) < 60:
            self._warm_step(0.004)

    def _danger_img(self, side, level):
        key = (side, level)
        s = self.danger_imgs.get(key)
        if s is None:
            x, y, w, h = self.geom()[side]
            pad = int(40 * self.s)
            m = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
            ImageDraw.Draw(m).rounded_rectangle([pad - 6, pad - 6, pad + w + 6, pad + h + 6], radius=int(12 * self.s), outline=255,
                                                width=max(3, int(8 * self.s)))
            m = m.filter(ImageFilter.GaussianBlur(10 * self.s))
            k = level / 6
            s = self.danger_imgs[key] = self.hd._surf(Image.merge("RGB", (m.point(lambda v: int(v * k)), m.point(lambda v: int(v * 0.12 * k)),
                                                                          m.point(lambda v: int(v * 0.08 * k)))))
        return s

    def _danger(self, screen, now):
        """Moins de 20 % de vie : la barre bat en rouge comme un cœur."""
        p = (now % 0.9) / 0.9
        env = math.exp(-((p - 0.05) / 0.06) ** 2) + 0.7 * math.exp(-((p - 0.25) / 0.06) ** 2)
        lvl = int(round(min(1.0, env) * 6))
        if lvl <= 0:
            return
        for side, h in self.health.items():
            if h is None or not (0 < h <= 20):
                continue
            x, y, w, hh = self.geom()[side]
            img = self._danger_img(side, lvl)
            pad = int(40 * self.s)
            screen.blit(img, (x - pad, y - pad), special_flags=self.pg.BLEND_RGB_ADD)

    def _slam(self, screen, text, color, t0, dur, now, size=112, y=240):
        k = now - t0
        if k < 0 or k > dur:
            return
        hd, S, W = self.hd, self.hd.S, self.W
        start = max(1.2, min(2.4, W * 0.96 / max(1, hd.text_width(text, "stencil", S(size)))))
        scale = start - (start - 1.0) * min(1.0, k / 0.16)
        alpha = 1.0 if k < dur - 0.25 else max(0.0, (dur - k) / 0.25)
        bar = self.pg.Surface((W, S(130))).convert()
        bar.fill((0, 0, 0))
        bar.set_alpha(int(215 * alpha))
        screen.blit(bar, (0, S(y - 65)))
        hd.put(screen, hd.text(text, "stencil", S(size), color, glow=0.8), W / 2, S(y), "center", "middle", scale=scale, alpha=alpha)

    def _slam_sub(self, screen, title, sub, color, t0, dur, now, alone=(96, 228)):
        """A banner with a line under it (STAGE 2 and its place, ROUND 1 and the place of the match). alone: size and
        height of the title without a line. / Un bandeau avec une ligne dessous."""
        k = now - t0
        if k < 0 or k > dur:
            return
        size, y = (96, 228) if sub else alone
        self._slam(screen, title, color, t0, dur, now, size=size, y=y)
        a = 1.0 if k < dur - 0.25 else max(0.0, (dur - k) / 0.25)
        if sub and k > 0.12:
            self.hd.put(screen, self.hd.text(sub, "stencil", self.hd.S(36), GOLD, glow=0.5), self.W / 2, self.hd.S(282),
                        "center", "middle", alpha=a)

    def _band(self, w, h):
        key = (w, h)
        band = self.bands.get(key)
        if band is None:
            band = self.bands[key] = self.pg.Surface((w, h)).convert()
            band.fill((6, 4, 10))
        return band

    def _side_slam(self, screen, text, color, side, t0, dur, now, size=124):
        """A word slammed onto one side of the screen, over its health bar: K.O. on the loser's, WIN on the winner's.
        / Un mot plaqué d'un côté de l'écran, sur sa barre de vie : K.O. chez le perdant, WIN chez le gagnant."""
        k = now - t0
        if k < 0 or k > dur:
            return
        hd, S = self.hd, self.hd.S
        x, y, w, h = self.geom()[side]
        cx, cy = x + w / 2, S(200)                                      # over the bar, above the name / au-dessus du nom
        scale = 2.2 - 1.2 * (1 - (1 - min(1.0, k / 0.18)) ** 3)
        alpha = 1.0 if k < dur - 0.3 else max(0.0, (dur - k) / 0.3)
        band = self._band(w + S(40), S(132))
        band.set_alpha(int(205 * alpha))
        screen.blit(band, (int(x - S(20)), int(cy - S(66))))
        hd.put(screen, hd.text(text, "stencil", S(size), color, glow=0.8), cx, cy, "center", "middle", scale=scale, alpha=alpha)

    def side_ko(self, now):
        """True while K.O. shows on the loser's side (the middle shows the stopped timer, not a second K.O.).
        / Vrai tant que K.O. s'affiche du côté du perdant."""
        return self.ko_side is not None and 0 <= now - self.ko_side[1] < 2.4

    def time_live(self, now):
        """The timer moved a moment ago. Frozen for 6 s, it is the last fight's (the select screen), and put back to 0 at the
        start of a round it was not counted down: not shown (1.31). Waiting for GO it is the new round's, shown even
        after 6 s (1.31.1) / Le chrono a bougé il y a peu ; figé 6 s, c'est celui du combat d'avant (écran de sélection), et
        remis à 0 au début d'un round il n'a pas été décompté : pas affiché. En attendant le GO, c'est celui du nouveau round."""
        if self.time_stale is not None:
            return False                  # the last match's, the game has not set the new one yet (1.32) / celui d'avant
        return (now - max(self.time_seen, self.fight_t) < 6.0 or self.fight_wait is not None) and not self.time_reset

    def held(self, side):
        """(name, fighters beaten) to show for a side while its next fighter waits for the K.O. of the one before, else
        None (1.31.1). / (nom, battus) à montrer tant que le suivant attend le K.O. de celui d'avant, sinon None."""
        return self.hold.get(side)

    def tag(self, side):
        return ("P1" if side == "p1" else "P2") if self.humans.get(side) else "CPU"

    def _match_end(self, screen, now):
        """A team eliminated: the winner in big letters, the loser's team out under it (1.31).
        / Une équipe éliminée : le vainqueur en grand, l'équipe du perdant éliminée dessous."""
        if self.out is None:
            return
        win, lose, t0 = self.out
        k, dur = now - t0, MATCH_END
        if k < 0 or k > dur:
            return
        hd, S, W = self.hd, self.hd.S, self.W
        alpha = 1.0 if k < dur - 0.3 else max(0.0, (dur - k) / 0.3)
        band = self._band(W, S(190))
        band.set_alpha(int(220 * alpha))
        screen.blit(band, (0, S(140)))
        title = tr(f"VICTOIRE {self.tag(win)}", f"{self.tag(win)} WINS")
        start = max(1.2, min(2.0, W * 0.9 / max(1, hd.text_width(title, "stencil", S(110)))))
        scale = start - (start - 1.0) * min(1.0, k / 0.18)
        hd.put(screen, hd.text(title, "stencil", S(110), GOLD, glow=0.9), W / 2, S(212), "center", "middle", scale=scale, alpha=alpha)
        if k > 0.35:
            sub = tr(f"ÉQUIPE {self.tag(lose)} ÉLIMINÉE", f"{self.tag(lose)} TEAM ELIMINATED")
            hd.put(screen, hd.text(sub, "stencil", S(54), RED, glow=0.6), W / 2, S(292), "center", "middle",
                   alpha=alpha * min(1.0, (k - 0.35) / 0.2))

    def _banners(self, screen, now):
        if self.stage_label is not None:
            title, place = self.stage_label
            self._slam_sub(screen, title, place, CREAM, self.stage_t + 0.3, 1.6, now)
        if self.round_v is not None:                                  # ROUND n, its round read in the game (1.31)
            self._slam_sub(screen, f"ROUND {int(self.round_v) + 1}", self.round_sub, GOLD, self.round_show + 0.1, 1.25, now,
                           alone=(112, 240))
        self._slam(screen, "FIGHT !", GOLD, self.fight_t + 0.1, 1.15, now)
        if self.ko_side is not None:
            self._side_slam(screen, "K.O.", RED, self.ko_side[0], self.ko_side[1], 2.4, now)
        if self.win_side is not None:
            self._side_slam(screen, "WIN", GOLD, self.win_side[0], self.win_side[1], 2.0, now)
        self._match_end(screen, now)
        if self.banner is not None:
            text, col, t0, dur = self.banner
            self._slam(screen, text, col, t0, dur, now)

    def _next_fighter(self, screen, now):
        """Combattant suivant : son nom arrive de son côté de l'écran."""
        hd, S, W = self.hd, self.hd.S, self.W
        for side in ("p1", "p2"):
            k = now - self.next_t[side]
            if k < 0 or k > 1.7:
                continue
            slide = min(1.0, k / 0.25) if k < 1.45 else max(0.0, (1.7 - k) / 0.25)
            e = 1 - (1 - slide) ** 3
            bw = int(W * 0.46)
            x = -bw + bw * e if side == "p1" else W - bw * e
            band = self.pg.Surface((bw, S(120))).convert()
            band.fill((8, 6, 14))
            band.set_alpha(225)
            screen.blit(band, (int(x), S(236)))
            self.pg.draw.rect(screen, GOLD, (int(x), S(236), bw, max(2, S(3))))
            self.pg.draw.rect(screen, GOLD, (int(x), S(353), bw, max(2, S(3))))
            name = self.next_name[side]
            size = hd.fit_size(name, "stencil", S(84), bw - S(80), S(30))
            cx = x + bw / 2
            hd.put(screen, hd.text(tr("ENTRE EN SCÈNE", "NEXT FIGHTER"), "bold", S(26), GOLD, glow=0), cx, S(258), "center", "middle")
            hd.put(screen, hd.text(name, "stencil", size, RED, glow=0.6), cx, S(306), "center", "middle")
