"""Credits of a Neo Geo MVS guessed from its BIOS, when they cannot be read.

An MVS keeps its credits in the backup RAM of the cabinet ($D00034). MAME reads it, but the FinalBurn Neo core of
RetroArch only shares the work RAM of the game. The BIOS leaves traces there. When a coin goes in while nobody plays, it
asks the game for its title screen (BIOS_USER_REQUEST at $10FDAE goes to 3), and the title screen counts down before the
game starts by itself (BIOS_COMPULSION_TIMER at $10FDDA), a countdown that starts again when another coin goes in. During
a game the BIOS sets that countdown again at each coin without running it, so only the first coin of a game shows. Each
player who starts takes a credit, and back to the demo (request 2) there is none left.

The coin buttons, when coin_buttons.bat has shown them (dmd/coinbuttons.py), tell each coin and its side. They come first.
A coin on the right then gives the credits of the second slot of the MVS (2 unless its settings were changed). What the
BIOS shows right after a press is that same coin.

FinalBurn Neo saves the backup RAM of each game when it is quit (saves/fbneo/<game>.fs), credits included, and gives
them back the next time. The engine keeps the guessed credits of each game the same way (runtime/neo_credits.json), and
a game that starts on its title screen (credits left) starts from them ("kept").

Crédits d'une Neo Geo MVS devinés d'après son BIOS, quand on ne peut pas les lire.

La MVS range ses crédits dans la mémoire de sauvegarde de la borne. MAME la lit, le cœur FinalBurn Neo de RetroArch ne
partage que la mémoire de travail du jeu. Le BIOS y laisse des traces. Quand une pièce entre alors que personne ne joue,
il demande au jeu son écran titre (la demande passe à 3), et cet écran compte à rebours avant de lancer la partie tout
seul, un compte qui repart quand une autre pièce entre. En pleine partie le BIOS remet ce compte à chaque pièce sans le
faire tourner, seule la première pièce de la partie se voit. Chaque joueur qui commence prend un crédit, et de retour à
la démo (demande 2) il n'en reste plus. Les boutons des pièces, quand coin_buttons.bat les a montrés, disent chaque
pièce et son côté. Ils passent avant. FinalBurn Neo sauve la mémoire de sauvegarde de chaque jeu quand on le quitte,
crédits compris, et la rend la fois suivante. Le moteur garde les crédits devinés de chaque jeu de la même façon, et un
jeu qui démarre sur son écran titre (des crédits restants) repart d'eux."""

DEMO, TITLE = 2, 3          # BIOS_USER_REQUEST
IN_GAME = 2                 # BIOS_USER_MODE


class NeoCoins:
    SETTLE = 1.5            # seconds of title screen before a countdown that starts again counts as a coin
    PRESSED = 2.0           # what the BIOS shows this long after a button is that coin / la même pièce

    def __init__(self, rates=(1, 2), kept=0):
        self.notes = []                                  # (fr, en) for the log / pour le journal
        self.rates = rates                               # credits of a coin, left then right / crédits d'une pièce
        # credits left when this game was last quit, given back by FinalBurn Neo / crédits restants la dernière fois
        self.kept = kept if isinstance(kept, int) and 0 < kept <= 99 else 0
        self.seen = None
        self.looked = False
        self.aes = False
        self.credits = None
        self.req = None
        self.timer = None
        self.top = None
        self.title_since = None
        self.modes = {}
        self.over_at = -99.0
        self.pressed_at = -99.0
        self.coins = 0                                   # coins seen (tests) / pièces vues (tests)

    def add(self, side, now):
        """A coin seen on the coin buttons, with its side (0 left, 1 right). The guessed credits, None on an AES."""
        if self.aes:
            return None
        n = self.rates[side] if side in (0, 1) else 1
        self.credits = min(99, (self.credits or 0) + n)
        self.coins += 1
        self.pressed_at = now
        return self.credits

    def update(self, values, now):
        """The guessed credits, or None while the BIOS has said nothing. / Les crédits devinés, ou None."""
        req, mode, timer = values.get("bios_request"), values.get("bios_mode"), values.get("bios_timer")
        if not isinstance(req, int) or not isinstance(mode, int) or req not in (DEMO, TITLE):
            return self.credits                          # the BIOS is not running the game yet / pas encore prêt
        mvs = values.get("bios_mvs")
        if mvs == 0:                                     # a home console takes no coins / une console AES
            if not self.aes:
                self.aes = True
                self.notes.append(("BIOS Neo Geo en mode AES (console) : pas de pièces, le jeu démarre avec Start",
                                   "Neo Geo BIOS in AES mode (home console): no coins, the game starts with Start"))
            return None
        if not self.looked:                              # first look / premier regard
            self.looked = True
            self.notes.append(("BIOS Neo Geo en mode MVS (arcade) : crédits devinés d'après le BIOS",
                               "Neo Geo BIOS in MVS mode (arcade): credits guessed from the BIOS"))
            if self.credits is None:
                if req == TITLE and mode != IN_GAME:
                    # the title at once: credits are left, those of last time if there were more than one
                    # l'écran titre tout de suite : il reste des crédits, ceux de la dernière fois s'il y en avait plus
                    self.credits = max(1, self.kept)
                elif mode == IN_GAME:
                    self.credits = self.kept             # a game going on: the best guess / une partie en cours
                else:
                    self.credits = 0
                if self.credits == self.kept > 0:
                    self.notes.append((f"crédits restants de la dernière fois : {self.kept}",
                                       f"credits left from last time: {self.kept}"))
        if (req, mode) != self.seen:
            self.notes.append((f"BIOS Neo Geo : demande {req}, mode {mode}", f"Neo Geo BIOS: request {req}, mode {mode}"))
            self.seen = (req, mode)
        pressed = now - self.pressed_at < self.PRESSED
        coin = False
        if req == TITLE and mode != IN_GAME:
            if self.req is not None and self.req != TITLE:
                coin = True                              # a coin while nobody plays / une pièce, personne ne joue
                self.title_since = now
                self.top = None
            elif self.title_since is None:
                self.title_since = now
            if isinstance(timer, int):
                if (self.top is not None and isinstance(self.timer, int) and 0 < self.timer < timer == self.top
                        and now - self.title_since >= self.SETTLE):
                    coin = True                          # the countdown starts again / le compte à rebours repart
                self.top = timer if self.top is None else max(self.top, timer)
        else:
            self.title_since = None
            self.top = None
            if mode == IN_GAME and isinstance(timer, int) and isinstance(self.timer, int) and timer > self.timer:
                coin = True                              # set again during a game / remis en pleine partie
        if coin:
            if now - self.over_at < 8.0 and self.credits > 0:
                pass                                     # the title again after a game over, credits left / le titre revient
            elif pressed:
                pass                                     # the coin of the button just pressed / celle du bouton
            else:
                self.credits = min(99, self.credits + 1)
                self.coins += 1
                self.notes.append(("pièce vue par le BIOS", "coin seen by the BIOS"))
        if req == DEMO and mode != IN_GAME and not pressed:
            self.credits = 0                             # back to the demo, no credit left / retour à la démo
        for p in ("p1_mode", "p2_mode"):
            v, old = values.get(p), self.modes.get(p)
            if v == 1 and old in (0, 2, 3) and self.credits > 0:
                self.credits -= 1                        # a player starts / un joueur commence
            if v == 3 and old in (1, 2):
                self.over_at = now
            self.modes[p] = v
        self.req, self.timer = req, timer
        return self.credits
