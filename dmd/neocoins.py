"""Credits of a Neo Geo MVS guessed from its BIOS, when they cannot be read.

An MVS keeps its credits in the backup RAM of the cabinet ($D00034). MAME reads it, but the FinalBurn Neo core of
RetroArch only shares the work RAM of the game. The BIOS leaves traces there. When a coin goes in while nobody plays, it
asks the game for its title screen (BIOS_USER_REQUEST at $10FDAE goes to 3), and the title screen counts down before the
game starts by itself (BIOS_COMPULSION_TIMER at $10FDDA), a countdown that starts again when another coin goes in. Each
player who starts takes a credit, and back to the demo (request 2) there is none left. That is enough for the coin to drop
on the panel and the HD screen, and for PRESS START. A coin put in during a game is not seen.

Crédits d'une Neo Geo MVS devinés d'après son BIOS, quand on ne peut pas les lire.

La MVS range ses crédits dans la mémoire de sauvegarde de la borne. MAME la lit, le cœur FinalBurn Neo de RetroArch ne
partage que la mémoire de travail du jeu. Le BIOS y laisse des traces. Quand une pièce entre alors que personne ne joue,
il demande au jeu son écran titre (la demande passe à 3), et cet écran compte à rebours avant de lancer la partie tout
seul, un compte qui repart quand une autre pièce entre. Chaque joueur qui commence prend un crédit, et de retour à la
démo (demande 2) il n'en reste plus. Une pièce mise en pleine partie ne se voit pas."""

DEMO, TITLE = 2, 3          # BIOS_USER_REQUEST
IN_GAME = 2                 # BIOS_USER_MODE


class NeoCoins:
    SETTLE = 1.5            # seconds of title screen before a countdown that starts again counts as a coin

    def __init__(self):
        self.notes = []                                  # (fr, en) for the log / pour le journal
        self.seen = None
        self.credits = None
        self.req = None
        self.timer = None
        self.top = None
        self.title_since = None
        self.modes = {}
        self.over_at = -99.0
        self.coins = 0                                   # coins seen (tests) / pièces vues (tests)

    def update(self, values, now):
        """The guessed credits, or None while the BIOS has said nothing. / Les crédits devinés, ou None."""
        req, mode, timer = values.get("bios_request"), values.get("bios_mode"), values.get("bios_timer")
        if not isinstance(req, int) or not isinstance(mode, int):
            return self.credits
        if self.credits is None:                         # first look / premier regard
            self.credits = 1 if (req == TITLE and mode != IN_GAME) else 0
            mvs = values.get("bios_mvs")
            if mvs == 0:
                self.notes.append(("BIOS Neo Geo en mode AES (console) : pas de pièces, le jeu démarre avec Start",
                                   "Neo Geo BIOS in AES mode (home console): no coins, the game starts with Start"))
            elif isinstance(mvs, int):
                self.notes.append(("BIOS Neo Geo en mode MVS (arcade) : crédits devinés d'après le BIOS",
                                   "Neo Geo BIOS in MVS mode (arcade): credits guessed from the BIOS"))
        if (req, mode) != self.seen:
            self.notes.append((f"BIOS Neo Geo : demande {req}, mode {mode}", f"Neo Geo BIOS: request {req}, mode {mode}"))
            self.seen = (req, mode)
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
        if coin:
            if now - self.over_at < 8.0 and self.credits > 0:
                pass                                     # the title again after a game over, credits left / le titre revient
            else:
                self.credits = min(99, self.credits + 1)
                self.coins += 1
                self.notes.append(("pièce vue par le BIOS", "coin seen by the BIOS"))
        if req == DEMO and mode != IN_GAME:
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
