"""HD scenes of the Capcom CPS shoot'em ups (1.30), each drawn after screenshots of its game: 1941, 1944, 19XX, Varth,
Carrier Air Wing, U.N. Squadron, Forgotten Worlds, Giga Wing, Mars Matrix, Progear, Dimahoo, Eco Fighters. Each game
has its own animated backdrop and reacts to the values read in its memory. The heroes, the enemies and the machines
are creations of the program in the spirit of the games, no picture comes from a game.

Scènes HD des shoot'em ups Capcom CPS (1.30), chacune dessinée d'après des captures de son jeu. Les héros, les ennemis
et les machines sont des créations du programme dans l'esprit des jeux, aucune image ne vient d'un jeu.
"""

from .hd_themes13 import THEMES          # the backdrops of this batch (into hd_bg.BUILDERS when imported)

SCENES = {}
__all__ = ["SCENES", "THEMES"]
