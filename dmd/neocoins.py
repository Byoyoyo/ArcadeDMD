"""Credits of a Neo Geo MVS guessed from its BIOS, when they cannot be read.

An MVS keeps its credits in the backup RAM of the cabinet ($D00034). MAME reads it, but the FinalBurn Neo core of
RetroArch only shares the work RAM of the game. The BIOS leaves traces there. When a coin goes in while nobody plays, it
asks the game for its title screen (BIOS_USER_REQUEST at $10FDAE goes to 3), and the title screen counts down before the
game starts by itself (BIOS_COMPULSION_TIMER at $10FDDA), a countdown that starts again when another coin goes in. Its
seconds show a coin once a second at best; read with the frames of the current second ($10FDDB, "bios_frames", at every
image), each coin the BIOS takes shows as the frames jumping back up while the seconds stay (1.33 test 28). During a game
the BIOS sets that countdown again at each coin without running it, so only the first coin of a game shows. Each player
who starts takes a credit, and back to the demo (request 2) there is none left.

The coin buttons, when coin_buttons.bat has shown them (dmd/coinbuttons.py), tell each coin and its side. They come first.
A coin on the right then gives the credits of the second slot of the MVS (2 unless its settings were changed). What the
BIOS shows right after a press is that same coin. With the frames read, a press on the title screen must be shown by the
BIOS within two seconds or it is taken back: a button that bounces, or a hand quicker than the BIOS, made the HD screen
run ahead of the game (Seb's Windjammers, 10 presses, 7 credits in the game).

FinalBurn Neo saves the backup RAM of each game when it is quit (saves/fbneo/<game>.fs), credits included, and gives
them back the next time. The engine keeps the guessed credits of each game the same way (runtime/neo_credits.json), and
a game that starts on its title screen (credits left) starts from them ("kept").

Crédits d'une Neo Geo MVS devinés d'après son BIOS, quand on ne peut pas les lire.

La MVS range ses crédits dans la mémoire de sauvegarde de la borne. MAME la lit, le cœur FinalBurn Neo de RetroArch ne
partage que la mémoire de travail du jeu. Le BIOS y laisse des traces. Quand une pièce entre alors que personne ne joue,
il demande au jeu son écran titre (la demande passe à 3), et cet écran compte à rebours avant de lancer la partie tout
seul, un compte qui repart quand une autre pièce entre. Ses secondes montrent une pièce par seconde au mieux ; lu avec les
images de la seconde en cours ($10FDDB, « bios_frames », à chaque image), chaque pièce prise se voit, les images remontent
sans que les secondes bougent (1.33 test 28), et un appui sur l'écran titre que le BIOS ne montre pas dans les deux
secondes est repris. En pleine partie le BIOS remet ce compte à chaque pièce sans le faire tourner, seule la première
pièce de la partie se voit. Chaque joueur qui commence prend un crédit, et de retour à
la démo (demande 2) il n'en reste plus. Les boutons des pièces, quand coin_buttons.bat les a montrés, disent chaque
pièce et son côté. Ils passent avant. FinalBurn Neo sauve la mémoire de sauvegarde de chaque jeu quand on le quitte,
crédits compris, et la rend la fois suivante. Le moteur garde les crédits devinés de chaque jeu de la même façon, et un
jeu qui démarre sur son écran titre (des crédits restants) repart d'eux."""

DEMO, TITLE = 2, 3          # BIOS_USER_REQUEST
IN_GAME = 2                 # BIOS_USER_MODE


class NeoCoins:
    SETTLE = 1.5            # seconds of title screen before a countdown that starts again counts as a coin
    FINE_SETTLE = 0.2       # the same, image by image: its frames back up are a coin after this (test 28)
    PRESSED = 2.0           # what the BIOS shows this long after a button is that coin / la même pièce
    # 1.33 test 19 (Seb's capture of 21:25): after a game over the BIOS passes by the demo for a few images before asking
    # the title screen again when credits are left; the demo must last this long before it means no credit is left, and
    # that title screen, up to this long after the game over, is not a coin / après un game over le BIOS passe par la
    # démo quelques images avant de redemander l'écran titre s'il reste des crédits
    DEMO_SETTLE = 1.0
    OVER_TITLE = 20.0

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
        self.demo_since = None                           # when the demo began / depuis quand la démo
        self.coins = 0                                   # coins seen (tests) / pièces vues (tests)
        # 1.33 test 8 (Seb: a coin pressed too early put ArcadeDMD one credit ahead of the game). A coin before the BIOS
        # is ready is not counted, the BIOS ignores it. A coin during the demo is counted at once but must be seen by the
        # BIOS (its title screen asked) within PRESSED seconds, or it is taken back. / Une pièce avant que le BIOS soit
        # prêt n'est pas comptée, il l'ignore. Une pièce pendant la démo est comptée tout de suite mais doit être vue
        # par le BIOS (son écran titre demandé) dans les PRESSED secondes, sinon elle est reprise.
        self.unconfirmed = []                            # [(when, credits)] coins of the demo not seen yet / pas encore vues
        # 1.33 test 22 (Seb's Windjammers captures: the coin pressed as the game boots, and the title at once): a coin before
        # the BIOS is ready is kept aside; if the BIOS then comes up on its title screen, it took that coin, which counts on
        # top of the credits left from last time (the title alone was read as those credits, and ArcadeDMD ran ahead of the
        # game by that much); if it comes up on the demo, it ignored it (test 8). / Une pièce avant que le BIOS soit prêt
        # est mise de côté : s'il arrive sur son écran titre, il l'a prise, en plus des crédits restants ; sur la démo, non.
        self.early = []                                  # [(when, credits)] coins pressed during the boot / pendant le démarrage
        self.EARLY = 8.0                                 # seconds such a coin stays worth something / combien de temps elle vaut
        # 1.33 test 28 (Seb's Windjammers: the button counted 10 coins, the game 7). With the countdown read image by image
        # ("bios_frames", $10FDDB, the frames of its current second), each coin the BIOS takes on the title screen shows:
        # the frames jump back up while the seconds do not go down. A press on the title screen is then counted at once
        # but must be seen that way within PRESSED seconds, or it is taken back (a button that bounces, a press the BIOS
        # did not take). / Avec le compte à rebours lu image par image, chaque pièce prise par le BIOS sur l'écran titre
        # se voit : un appui sur l'écran titre est compté tout de suite mais doit être vu ainsi, sinon il est repris.
        self.fine = False                                # bios_frames read: coins seen one by one / pièces vues une à une
        self.frames = None
        self.pending = []                                # [(when, credits)] presses on the title not seen yet / pas encore vues
        self.bios_coins = 0                              # coins the BIOS showed / pièces que le BIOS a montrées

    def add(self, side, now):
        """A coin seen on the coin buttons, with its side (0 left, 1 right). The guessed credits, None on an AES or
        before the BIOS is ready (that coin counts only if the BIOS comes up on its title screen, 1.33 tests 8 and 22)."""
        if self.aes:
            return None
        n = self.rates[side] if side in (0, 1) else 1
        if not self.looked or self.credits is None:
            self.early.append((now, n))
            self.notes.append(("pièce avant que le BIOS soit prêt : comptée s'il arrive sur son écran titre",
                               "coin before the BIOS is ready: counted if it comes up on its title screen"))
            return None
        if self.req == DEMO:
            self.unconfirmed.append((now, n))            # to be seen by the BIOS / à voir par le BIOS
        elif self.fine and self.req == TITLE and self.seen and self.seen[1] != IN_GAME:
            self.pending.append((now, n))                # to be seen on the countdown / à voir sur le compte à rebours
        self.credits = min(99, (self.credits or 0) + n)
        self.coins += 1
        self.pressed_at = now
        return self.credits

    def update(self, values, now):
        """The guessed credits, or None while the BIOS has said nothing. / Les crédits devinés, ou None."""
        req, mode, timer = values.get("bios_request"), values.get("bios_mode"), values.get("bios_timer")
        frames = values.get("bios_frames")
        if isinstance(frames, int):
            self.fine = True
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
                early = sum(n for t, n in self.early if now - t < self.EARLY)
                self.early = []
                if req == TITLE and mode != IN_GAME:
                    if early:
                        # a coin pressed as the game booted and the title at once: the BIOS took it, on top of the credits
                        # left from last time (test 22) / une pièce pendant le démarrage et l'écran titre : prise par le
                        # BIOS, en plus des crédits restants
                        self.credits = min(99, self.kept + early)
                        self.coins += 1
                        self.pressed_at = now
                        self.notes.append((f"pièce prise par le BIOS au démarrage : {early}, en plus des {self.kept} restants",
                                           f"coin taken by the BIOS at the boot: {early}, on top of the {self.kept} left"))
                    else:
                        # the title at once: credits are left, those of last time if there were more than one
                        # l'écran titre tout de suite : il reste des crédits, ceux de la dernière fois s'il y en avait plus
                        self.credits = max(1, self.kept)
                elif mode == IN_GAME:
                    self.credits = self.kept             # a game going on: the best guess / une partie en cours
                else:
                    self.credits = 0
                    if early:
                        self.notes.append(("pièce pendant le démarrage ignorée par le BIOS (la démo) : pas comptée",
                                           "coin during the boot ignored by the BIOS (the demo): not counted"))
                if self.credits == self.kept > 0:
                    self.notes.append((f"crédits restants de la dernière fois : {self.kept}",
                                       f"credits left from last time: {self.kept}"))
        if (req, mode) != self.seen:
            self.notes.append((f"BIOS Neo Geo : demande {req}, mode {mode}", f"Neo Geo BIOS: request {req}, mode {mode}"))
            self.seen = (req, mode)
        pressed = now - self.pressed_at < self.PRESSED
        if self.unconfirmed:
            if req == TITLE:
                self.unconfirmed = []                    # the BIOS saw them: the title / le BIOS les a vues
            else:
                late = [c for c in self.unconfirmed if now - c[0] >= self.PRESSED]
                if late:                                 # the BIOS stayed on the demo: those coins went nowhere
                    self.credits = max(0, self.credits - sum(n for _, n in late))
                    self.coins -= len(late)
                    self.unconfirmed = [c for c in self.unconfirmed if now - c[0] < self.PRESSED]
                    self.notes.append(("pièce non vue par le BIOS (toujours la démo) : reprise",
                                       "coin not seen by the BIOS (still the demo): taken back"))
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
                elif (isinstance(frames, int) and isinstance(self.frames, int) and frames > self.frames
                      and isinstance(self.timer, int) and timer >= self.timer and self.title_since is not None
                      and now - self.title_since >= self.FINE_SETTLE):
                    coin = True                          # its frames back up, not a new second: set again (test 28)
                self.top = timer if self.top is None else max(self.top, timer)
        else:
            self.title_since = None
            self.top = None
            if self.pending:                             # the title left: the presses stay counted / restent comptées
                self.pending = []
            if mode == IN_GAME and isinstance(timer, int) and isinstance(self.timer, int) and timer > self.timer:
                coin = True                              # set again during a game / remis en pleine partie
        if coin:
            self.bios_coins += 1
            if self.pending:                             # the press just counted, seen by the BIOS / l'appui, vu
                self.pending.pop(0)
                self.notes.append(("pièce vue par le BIOS (celle du bouton)", "coin seen by the BIOS (the button's)"))
            elif now - self.over_at < self.OVER_TITLE and self.credits > 0:
                pass                                     # the title again after a game over, credits left / le titre revient
            elif pressed:
                pass                                     # the coin of the button just pressed / celle du bouton
            else:
                self.credits = min(99, self.credits + 1)
                self.coins += 1
                self.notes.append(("pièce vue par le BIOS", "coin seen by the BIOS"))
        late = [c for c in self.pending if now - c[0] >= self.PRESSED]
        if late:                                         # the BIOS did not take them / le BIOS ne les a pas prises
            self.credits = max(0, self.credits - sum(n for _, n in late))
            self.coins -= len(late)
            self.pending = [c for c in self.pending if now - c[0] < self.PRESSED]
            self.notes.append(("pièce non vue par le BIOS (compte à rebours pas relancé) : reprise",
                               "coin not seen by the BIOS (countdown not set again): taken back"))
        if req == DEMO and mode != IN_GAME:
            if self.demo_since is None:
                self.demo_since = now
            if now - self.demo_since >= self.DEMO_SETTLE and not pressed and self.credits:
                self.credits = 0                         # the demo for good: no credit left / la démo pour de bon
                self.notes.append(("la démo reste : plus de crédit", "the demo stays: no credit left"))
        else:
            self.demo_since = None
        for p in ("p1_mode", "p2_mode"):
            v, old = values.get(p), self.modes.get(p)
            if v == 1 and old in (0, 2, 3) and self.credits > 0:
                self.credits -= 1                        # a player starts / un joueur commence
            if v == 3 and old in (1, 2):
                self.over_at = now
            self.modes[p] = v
        self.req, self.timer = req, timer
        if isinstance(frames, int):
            self.frames = frames
        return self.credits
