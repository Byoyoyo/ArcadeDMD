"""Builds the files of the Cave games (games/<game>.json) from FinalBurn Neo (1.31).

From the list of FinalBurn Neo, each original game gets its file with every version, bootleg and hack of it, for MAME as
for RetroArch:
  - the games of the Cave board with its 68000 (src/burn/drv/cave/d_*.cpp): DonPachi, DoDonPachi, ESP Ra.De., Dangun
    Feveron, Guwange, Uo Poko, and the games other companies made on that board (Power Instinct 2, Sailor Moon...),
  - the games Cave made for the IGS PGM (src/burn/drv/pgm/d_pgm.cpp): DoDonPachi Dai-Ou-Jou, Ketsui, Espgaluda, and
    DoDonPachi II that IGS made under Cave's licence,
  - the games of Cave's own CV1000 board with its SH-3 (src/burn/drv/cave/d_cv1k.cpp): Mushihime-sama, Espgaluda II,
    Ibara, Deathsmiles, DoDonPachi Dai-Fukkatsu, Akai Katana...
From the cheat database of FinalBurn Neo (FBNeo-cheats, cheats/<game>.ini), completed by MAME's (mamecheat.co.uk, the
XML files of its cheat.7z, read by tools/mame_cheats.py), it takes what the cheats write: the credits, the lives, the bombs
and their slots, the power of the shot, the combo gauge, the ship chosen, the stage. What a cheat does not give (the score,
the hit counter) is left to learn with learn.bat on the cabinet. A file that was changed by hand keeps its scene and what
the tool does not make, a value learned or set by hand wins over the cheats.

Construit les fichiers des jeux Cave à partir de FinalBurn Neo : la carte Cave à 68000, les jeux Cave du PGM d'IGS et la
carte CV1000 de Cave. Les codes de triche de FinalBurn Neo, complétés par ceux de MAME, donnent les crédits, les vies,
les bombes et leurs places, la puissance, la jauge de combo, le vaisseau choisi, le niveau. Le score et le compteur de
coups s'apprennent avec learn.bat.

usage: python tools/cave_games.py FBNEO_SOURCE_FOLDER FBNEO_CHEATS_FOLDER [MAME_CHEATS]
       MAME_CHEATS: the folder of the XML files of MAME's cheat.7z, or cheat.7z itself (pip install py7zr)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cps_games  # noqa: E402
from cps_games import cheats, dump, enabled, load, make_templates, value, values_from_cheats  # noqa: E402
from mame_cheats import MameCheats, merge as merge_cheats  # noqa: E402
from neogeo_sets import clean  # noqa: E402

TOOL = "tools/cave_games.py"
CAVE_DIR = "src/burn/drv/cave"
PGM_FILE = "src/burn/drv/pgm/d_pgm.cpp"
# the PGM games of Cave, DoDonPachi II made by IGS under Cave's licence / les jeux Cave du PGM
PGM_CAVE = ("ddp3", "ket", "espgal", "ddp2")
# medal games: Tobikose! Jumpman keeps its work RAM out of what FinalBurn Neo gives RetroArch, Moukari Bancho does not run
# des jeux à médailles : la RAM de Jumpman n'est pas partagée avec RetroArch, Moukari Bancho ne tourne pas
SKIP = {"tjumpman", "mmmbanc"}
# where the 68000 work RAM is (FinalBurn Neo SekMapMemory of Ram01, the start of the "RAM" it gives RetroArch)
# où est la RAM de travail du 68000 (le début de la RAM donnée à RetroArch)
BASES = {"d_guwange.cpp": 0x200000, "d_hotdogst.cpp": 0x300000, "d_korokoro.cpp": 0x300000, "d_pwrinst2.cpp": 0x400000,
         "d_metmqstr.cpp": 0x888000}
SET_BASES = {"crusherm": 0x340000}
SIZES = {"d_metmqstr.cpp": 0x8000}
TEMPLATES = {"cave_combat": "neogeo_combat", "cave_action": "neogeo", "cave_reflexion": "neogeo_reflexion"}
# the LED panel of the Cave shoot'em ups, in the spirit of DoDonPachi: pink and blue bullets drifting by, 1P and the score,
# the ships left, the hit counter in the middle (the ship chosen when there is no chain), the bombs and their empty slots,
# MAX when they are all full, the combo gauge that drains / la dalle des shoot'em ups Cave, dans l'esprit de DoDonPachi
SHIP = ["#.....", "###...", "######", "###...", "#....."]
BOMB = [".##.", "####", "####", "####", ".##."]
CAVE_SHOOT = [
    {"type": "particles", "rate": 9, "color": "#ff4aa8", "trail": 0, "speed": [18, 46], "y": [11, 24], "dir": "left"},
    {"type": "particles", "rate": 6, "color": "#4aa8ff", "trail": 0, "speed": [24, 60], "y": [11, 24], "dir": "left"},
    {"type": "marquee", "segments": [{"text": "{title}", "color": "#e6e6e6"}], "font": "6x10", "y": 0, "speed": 12, "gap": 40, "upper": True,
     "static_if_fits": True, "when": {"not": {"has": "score"}}},
    {"type": "text", "font": "6x10", "x": 1, "y": 0, "align": "left", "text": "1P", "color": "#ff5aa0", "when": {"has": "score"}},
    {"type": "text", "font": "6x10", "x": 15, "y": 0, "align": "left", "text": "{score}", "color": "#ffffff", "when": {"has": "score"},
     "flash": {"on": "score", "color": "#ffe08a", "ms": 120}},
    {"type": "icons", "var": "lives", "x": 127, "y": 2, "max": 5, "gap": 1, "align": "right", "pattern": SHIP, "colors": {"#": "#ff6a5a"},
     "when": {"all": [{"has": "score"}, {"has": "lives"}]}, "flash": {"on": "lives", "color": "#ffffff", "ms": 500}},
    {"type": "text", "font": "7x14", "x": 64, "y": 10, "align": "center", "segments": [{"text": "{hits}", "color": "#ffe05a"},
                                                                                      {"text": " HIT", "color": "#ff9a3c"}],
     "when": {"var": "hits", "gt": 0}, "flash": {"on": "hits", "color": "#ffffff", "ms": 90}},
    {"type": "text", "font": "6x10", "x": 64, "y": 13, "align": "center", "text": "{p1_ship}", "color": "#5ad8ff",
     "when": {"all": [{"has": "p1_ship"}, {"not": {"var": "hits", "gt": 0}}]}},
    {"type": "text", "font": "6x10", "x": 64, "y": 13, "align": "center", "text": "LIVES {lives}", "color": "#5ad8ff",
     "when": {"all": [{"has": "lives"}, {"not": {"has": "score"}}, {"not": {"has": "p1_ship"}}, {"not": {"var": "hits", "gt": 0}}]}},
    {"type": "icons", "var": "bombs", "slots": "bombs_max", "x": 1, "y": 26, "max": 8, "gap": 1, "pattern": BOMB, "colors": {"#": "#ffc83c"},
     "empty": "#3a2a10", "when": {"has": "bombs"}, "flash": {"on": "bombs", "color": "#ffffff", "ms": 300}},
    {"type": "text", "font": "4x6", "x": 50, "y": 26, "align": "left", "text": "MAX", "color": "#ffd040", "blink_period": 0.6,
     "when": {"all": [{"var": "bombs", "ge_var": "bombs_max"}, {"var": "bombs_max", "gt": 0}]}},
    {"type": "gauge", "var": "combo", "max": 100, "x": 66, "y": 28, "w": 61, "h": 3, "anchor": "left", "color": "#ff9a30", "low": "#ff9a30",
     "low_at": 0, "back": "#2a1c08", "shade": False, "when": {"has": "combo"}},
    # the boss's life read in the game (DoDonPachi, 1.31), a thin bar above the bombs, full at the highest life seen
    # la vie du boss lue dans le jeu, une barre fine au-dessus des bombes, pleine à la plus haute vie vue
    {"type": "gauge", "var": "boss_hp", "max": "peak", "x": 1, "y": 24, "w": 126, "h": 2, "anchor": "left", "color": "#ff5a2a",
     "low": "#ff2418", "low_at": 0.25, "back": "#2a0a06", "shade": False,
     "when": {"all": [{"var": "boss", "eq": 1}, {"var": "boss_hp", "gt": 0}]}},
    # the boss comes (a game that says it, DoDonPachi): WARNING! then its name / le boss arrive : WARNING! puis son nom
    {"type": "events", "events": [
        {"on": "boss", "change": "up", "to": [1], "text": "WARNING!", "color": "#ff3c30", "font": "9x15B", "ms": 1300, "priority": 6},
        {"on": "boss", "change": "up", "to": [1], "text": "{boss_name}", "color": "#ffd040", "font": "9x15B", "ms": 2200, "priority": 5.9,
         "when": {"has": "boss_name"}}]},
]


def make_shoot_template(games_dir):
    dump(os.path.join(games_dir, "cave_shoot.json"), {
        "note": f"Shared scene of the Cave shoot'em ups, in the spirit of DoDonPachi, made by {TOOL}. The games take it with scene_from.",
        "generated": TOOL, "scene": {"layers": CAVE_SHOOT}})
SCENES = [(("GBF_VSFIGHT",), "cave_combat"),
          (("GBF_VERSHOOT", "GBF_HORSHOOT"), "cave_shoot"),
          (("GBF_PUZZLE", "GBF_QUIZ", "GBF_MAHJONG", "GBF_MINIGAMES"), "cave_reflexion")]
# the HD scene of each game (dmd/hd_cave.py) / la scène HD de chaque jeu
HD = {"ddonpach": "ddonpach", "donpachi": "donpachi", "esprade": "esprade", "guwange": "guwange", "feversos": "feversos",
      "uopoko": "uopoko", "ddp3": "ddp3", "ket": "ket", "espgal": "espgal", "ddp2": "ddp2", "mushisam": "mushisam",
      "futari15": "futari15", "futaribl": "futaribl", "matsuri15": "matsuri15", "espgal2": "espgal2", "ibara": "ibara",
      "ibarablk": "ibarablk", "pinkswts": "pinkswts", "mmpork": "mmpork", "deathsml": "deathsml", "dsmbl": "dsmbl",
      "ddpdfk": "ddpdfk", "dfkbl": "dfkbl", "ddpsdoj": "ddpsdoj", "akatana": "akatana", "mushitam": "mushitam",
      "hotdogst": "hotdogst", "mazinger": "mazinger", "agallet": "agallet", "sailormn": "sailormn", "gaia": "gaia", "theroes": "theroes"}
# games made by Cave (the others only run on its board) / les jeux faits par Cave
BY_CAVE = {"donpachi", "ddonpach", "esprade", "feversos", "uopoko", "guwange", "ddp3", "ket", "espgal", "mushisam", "espgal2",
           "mushitam", "futari15", "futaribl", "matsuri15", "ibara", "ibarablk", "deathsml", "mmpork", "pinkswts", "ddpdfk", "dsmbl",
           "dfkbl", "ddpsdoj", "akatana"}
SRC = "FBNeo cheat database"
# the name the game is known by when FinalBurn Neo's parent is an export version / le nom sous lequel le jeu est connu
TITLES = {"ddp3": "DoDonPachi Dai-Ou-Jou"}
PL = r"(?:pl|p|player ?)"


def learn(key, kind="bcd", n=4, note=""):
    v = {"addr": "", "type": kind}
    if kind in ("bcd", "be") and n:
        v["bytes"] = n
    v["note"] = note
    return v


SCORES = {"score": learn("score", note="player 1 score, not in the cheat databases: learn it with learn.bat (score=...)"),
          "score_p2": learn("score_p2", note="player 2 score, learn it with learn.bat in a two-player game (score2=...)")}


def hand(fam):
    """What the cheats say once read by a person, game by game: the bombs and their slots, the power, the combo gauge,
    the ship. FinalBurn Neo cheat database, with MAME's notes (the first byte of the shot is a flag, the second its level).
    / Ce que disent les codes, lus par une personne, jeu par jeu."""
    def v(addr, note, kind="u8", n=1, **extra):
        out = value(addr, n, fam, kind, note)
        out.update(extra)
        return out
    return {
        "ddonpach": {
            # the game counts the ship in play too: the ships left, as the game shows them (2 at the start), are one less
            # le jeu compte aussi le vaisseau en jeu : ceux qui restent, comme le jeu les montre, sont un de moins
            "lives": v(0x101965, f"ships left of player 1 as the game shows them, 2 at the start: the game counts the ship in play "
                                 f"too, one less is read, -1 once the game is over ({SRC}, Infinite Lives PL1; RetroAchievements "
                                 "code notes, Lives - P1, 0 when the game is over), seen on the cabinet", add=-1),
            "lives_p2": v(0x101967, f"ships left of player 2, as player 1's ({SRC}, Infinite Lives PL2)", add=-1),
            "bombs": v(0x102CB0, f"bombs of player 1, 6 at most ({SRC}, Infinite Bombs PL1, the first byte)"),
            "bombs_max": v(0x102CB1, f"bomb slots of player 1: 3 at the start, one more for each ship lost, 6 at most ({SRC}, "
                                     "Infinite Bombs PL1, the second byte, capacity in MAME's notes)"),
            "bombs_p2": v(0x102CF0, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "bombs_max_p2": v(0x102CF1, f"bomb slots of player 2 ({SRC}, Infinite Bombs PL2, the second byte)"),
            "power": v(0x102CAD, f"shot level of player 1, 0 to 4 ({SRC}, Maximum Shot PL1, the first byte): it keeps the level "
                                 "while the ship blows up and comes back, the second byte drops to 0 meanwhile (captures from the "
                                 "cabinet)", max=4),
            "power_p2": v(0x102CED, f"shot level of player 2 ({SRC}, Maximum Shot PL2, the first byte)", max=4),
            "combo": v(0x1017D1, f"combo gauge of player 1, full = 0x37: it drains, each enemy destroyed fills it ({SRC}, "
                                 "Maximum Combo PL1)", mult=round(100 / 0x37, 6), round=1, min=0, max=100),
            "combo_p2": v(0x1017FB, f"combo gauge of player 2, full = 0x37 ({SRC}, Maximum Combo PL2)", mult=round(100 / 0x37, 6),
                          round=1, min=0, max=100),
            "ship": v(0x102D1D, f"ship of player 1: 0 type A (red fighter), 1 type B (helicopter), 2 type C (blue fighter) "
                                f"({SRC}, Select Option Type PL1)"),
            "ship_p2": v(0x102D5D, f"ship of player 2 ({SRC}, Select Option Type PL2)"),
            "credits": v(0x1013AB, f"credits, {LEARNED}: one less for each START and each continue. 0x100F83 matches the coins "
                                   "put in but never goes down, learn.bat sets it aside", not_learned=["0x100F83"]),
            "_score10": v(0x10161E, f"player 1 score without its last digit, {LEARNED}: the game shows the continues used as the last "
                                    "digit (tag score)", "bcd", 4, mult=10),
            "_cont": v(0x10174F, f"continues used by player 1, the last digit of the score as the game shows it, {LEARNED}"),
            "_score10_p2": v(0x101622, f"player 2 score without its last digit, {LEARNED} (tag score_p2)", "bcd", 4, mult=10),
            "_cont_p2": v(0x101753, f"continues used by player 2, {LEARNED}"),
            "hits": v(0x1017EC, f"hit counter of player 1 as the game shows it, it stays after a chain until the next one, {LEARNED}",
                      "bcd", 2),
            "hits_p2": v(0x101816, f"hit counter of player 2 as the game shows it, {LEARNED}", "bcd", 2),
            "stage": v(0x101979, "stage, the value read plus one (MAME cheat database: Select Level to follow Level 1 writes it, "
                                 "Kill Boss with 1 hit tests it), checked on the cabinet", add=1),
            "loop": v(0x10197A, "loop, 0 the first and 1 the second (MAME cheat database, Select Level to follow Level 1)", "u16", 2),
            # the boss of each stage comes where its stage stops scrolling (derived boss) / le boss arrive où le niveau s'arrête
            "distance": v(0x10198E, "how far the stage has scrolled, from 0 at its start: it stops where the boss comes, 0x200, 0x160, "
                                    "0x1B0, 0x200, 0x250 and 0x121 for stages 1 to 6 (RetroAchievements code notes, Distance into current "
                                    "stage, and its achievements for the bosses)", "be", 2),
            "phase": v(0x1017A4, "game state, 3 while the results of a stage show, 4 for the ending (RetroAchievements code notes, Game "
                                 "State)"),
            # who plays, said by the game itself (tags p1_mode and p2_mode) / qui joue, dit par le jeu lui-même
            "_state": v(0x1017A7, "game state: 0 both players, 7 player 1, 6 player 2 (playing, results, ending), 8 continue, 0x0B ship "
                                  "select, 5 demo, 1 and 4 the title before and after a coin, 2 the ranking, 0x0C and 0x0D the logos "
                                  "(RetroAchievements code notes, Game State, and its rich presence). Checked in captures taken on the "
                                  "cabinet: 7 with player 1 alone, 0 with both, 6 once player 1's game was over"),
            # who is out of the game, one bit each, also at the ship select where nobody has ships yet (tags p1_mode, p2_mode)
            # qui est hors du jeu, un bit chacun, aussi au choix du vaisseau où personne n'a encore de vaisseaux
            "_players": v(0x1017A9, "players' flags, 0x80 a game going on, 0x10 player 1 out of it, 0x20 player 2 out of it (27 captures "
                                    "taken on the cabinet: 0xE0 with player 1 alone, 0x80 with both, 0x90 with player 2 alone, 0 at the "
                                    "title)"),
            "_out_p1": v(0x1017A9, "player 1 out of the game, the bit 0x10 of the players' flags", mask=0x10, shift=4),
            "_out_p2": v(0x1017A9, "player 2 out of the game, the bit 0x20 of the players' flags", mask=0x20, shift=5),
            # the routine the stage runs, an address of the World program (derived warning) / la routine que suit le niveau
            "_stage_task": v(0x1013FC, "routine the stage runs, an address in the World program: 0x6DA98 while the WARNING of a boss "
                                       "shows, 0x6DB82 while the carrier drops the ship at the start of stage 1, others while the stage "
                                       "scrolls and during the boss fights (captures taken on the cabinet: the WARNING of the first three "
                                       "bosses, 0x6DA98 each time and never in the 23 other captures)", "be", 4),
            # the life of the boss on the screen, where the cheat that kills it in one hit writes (derived boss_hp)
            # la vie du boss à l'écran, là où écrit le code qui le tue d'un coup
            "_boss_hp": v(0x100198, "life of the boss of stages 1 to 5 and 7, a signed 32-bit number, learned on the cabinet with "
                                    "learn.bat (1.31: 12 captures of the fight against the boss of stage 1, 0 before it comes, 86016 "
                                    "once it is entirely on the screen, 81294, 50216, 42006, 33910, 23894, 12940, 8772, 850, 369 just "
                                    "before it blows up, -33 after). Where the cheat Kill Boss with 1 hit Now! writes (MAME 0 at the "
                                    "32-bit 0x100198, FinalBurn Neo 0 at 0x10019A); the word at 0x10019A alone jumped when the "
                                    "life went under 65536", "s32", 4),
            "_boss_hp_b": v(0x100158, "life of the boss of stage 6 and of the second boss of stage 7, a signed 32-bit number 0x40 "
                                      "before (MAME cheat database, Kill Boss with 1 hit Now!: 0 at the 32-bit 0x100158 from the "
                                      "stage read 5), to confirm in game", "s32", 4)},
        "donpachi": {
            "bombs": v(0x10217B, f"bombs of player 1 ({SRC}, Infinite Bombs PL1)"),
            "bombs_p2": v(0x1021BB, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "power": v(0x102179, f"shot level of player 1, 4 at most ({SRC}, Maximum Fire Power PL1)", max=4),
            "power_p2": v(0x1021B9, f"shot level of player 2 ({SRC}, Maximum Fire Power PL2)", max=4),
            "combo": v(0x101743, f"combo gauge of player 1, full = 0x1F ({SRC}, Always Combo gauge Max PL1)", mult=round(100 / 0x1F, 6),
                       round=1, min=0, max=100),
            "combo_p2": v(0x101761, f"combo gauge of player 2, full = 0x1F ({SRC}, Always Combo gauge Max PL2)",
                          mult=round(100 / 0x1F, 6), round=1, min=0, max=100),
            "hits": learn("hits", "u8", 1, "hit counter of player 1, learn it with learn.bat (hits=...)"),
            "stage": v(0x101A41, "area, the value read plus one (MAME cheat database: Select Area to follow Area 1 writes it)", add=1),
            "loop": v(0x101A42, "loop, 0 the first (MAME cheat database, Select Area to follow Area 1)", "u16", 2)},
        "esprade": {
            "bombs": v(0x102750, f"bombs of player 1 ({SRC}, Infinite Bombs PL1)"),
            "bombs_p2": v(0x1027A0, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "power": v(0x10272B, f"shot level of player 1, 4 at most ({SRC}, Maximum Power PL1)", max=4),
            "power_p2": v(0x10277B, f"shot level of player 2 ({SRC}, Maximum Power PL2)", max=4),
            "multiplier": v(0x1026FF, f"combo bonus multiplier, x16 at most: the value read plus one ({SRC}, Always Combo Bonus x16)",
                            add=1, max=16),
            "stage": learn("stage", "u8", 1, "stage, learn it with learn.bat (stage=...)")},
        "guwange": {
            "bombs": v(0x2028F9, f"bombs of player 1, 5 at most ({SRC}, Infinite Bombs PL1)"),
            "bombs_p2": v(0x202959, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "power": v(0x2028FB, f"shot power of player 1, 14 at most ({SRC}, Maximum Power PL1)", max=14),
            "power_p2": v(0x20295B, f"shot power of player 2 ({SRC}, Maximum Power PL2)", max=14),
            "combo": v(0x20289D, f"combo gauge of player 1, full = 10 ({SRC}, Infinite Combo Gauge PL1)", mult=10.0, round=1, min=0,
                       max=100),
            "combo_p2": v(0x20290D, f"combo gauge of player 2, full = 10 ({SRC}, Infinite Combo Gauge PL2)", mult=10.0, round=1, min=0,
                          max=100),
            "energy": v(0x2026DA, f"energy of player 1, full = 0x24 ({SRC}, Infinite Energy PL1)", mult=round(100 / 0x24, 6), round=1,
                        min=0, max=100),
            "energy_p2": v(0x2026E0, f"energy of player 2, full = 0x24 ({SRC}, Infinite Energy PL2)", mult=round(100 / 0x24, 6),
                           round=1, min=0, max=100),
            "char": v(0x2028E4, f"hero of player 1: 0 Sisin, 1 Kosame, 2 Gensuke ({SRC}, Select Color PL1)"),
            "char_p2": v(0x202944, f"hero of player 2 ({SRC}, Select Color PL2)"),
            "lives": learn("lives", "u8", 1, "lives of player 1, not in the cheat databases: learn it with learn.bat (lives=...)")},
        "feversos": {
            "bombs": v(0x105A3B, f"bombs of player 1, 3 at most ({SRC}, Infinite Bombs PL1)"),
            "bombs_p2": v(0x105A7B, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "power": v(0x105A35, f"shot level of player 1, 6 at most ({SRC}, Maximum Fire Power PL1, the first byte)", max=6),
            "power_p2": v(0x105A75, f"shot level of player 2 ({SRC}, Maximum Fire Power PL2)", max=6),
            "ship": v(0x105A36, f"fighter of player 1: 0 type A (concentrated shot), 8 type B (3-way), 16 type C (wide) "
                                f"({SRC}, Select Fighter Type PL1)"),
            "ship_p2": v(0x105A76, f"fighter of player 2 ({SRC}, Select Fighter Type PL2)"),
            "round": v(0x1052D9, f"round, the value read plus one ({SRC}, Select Starting Round)", add=1),
            "mode": v(0x105105, f"game mode: 0 normal, 1 time attack ({SRC}, Select Game Mode)")},
        "uopoko": {
            "stage": v(0x100203, f"stage, the value read plus one ({SRC}, Select Starting Stage)", add=1),
            "bubble": v(0x1022F1, f"bubble of player 1 ready to shoot: 0x80 magenta to 0x87 orange ({SRC}, Select Current Bubble PL1)"),
            "bubble_p2": v(0x1022F3, f"bubble of player 2 ({SRC}, Select Current Bubble PL2)")},
        "ddp3": {
            "lives": v(0x813022, f"lives of player 1 ({SRC}, Infinite Lives PL1)", "be", 2),
            "lives_p2": v(0x813024, f"lives of player 2 ({SRC}, Infinite Lives PL2)", "be", 2),
            "bombs": v(0x81037E, f"bombs of player 1 ({SRC}, Infinite Bombs PL1, the first byte)"),
            "bombs_max": v(0x81037F, f"bomb slots of player 1 ({SRC}, Infinite Bombs PL1, the second byte)"),
            "bombs_p2": v(0x8103E0, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "bombs_max_p2": v(0x8103E1, f"bomb slots of player 2 ({SRC}, Infinite Bombs PL2, the second byte)"),
            "power": v(0x81037A, f"shot level of player 1, 8 at most ({SRC}, Maximum Fire Power PL1, the first word)", "be", 2, max=8),
            "power_p2": v(0x8103DC, f"shot level of player 2 ({SRC}, Maximum Fire Power PL2)", "be", 2, max=8),
            "combo": v(0x81B365, f"combo gauge of player 1, full = 0x38 ({SRC}, Infinite Combo Gauge PL1)", mult=round(100 / 0x38, 6),
                       round=1, min=0, max=100),
            "combo_p2": v(0x81B38F, f"combo gauge of player 2, full = 0x38 ({SRC}, Infinite Combo Gauge PL2)",
                          mult=round(100 / 0x38, 6), round=1, min=0, max=100),
            "hits": learn("hits", "u8", 1, "hit counter of player 1, learn it with learn.bat (hits=...)"),
            "stage": learn("stage", "u8", 1, "stage, learn it with learn.bat (stage=...)")},
        "ket": {
            "lives": v(0x812472, f"lives of player 1 ({SRC}, Infinite Lives PL1)", "be", 2),
            "lives_p2": v(0x812474, f"lives of player 2 ({SRC}, Infinite Lives PL2)", "be", 2),
            "bombs": v(0x80FEC6, f"bombs of player 1 ({SRC}, Infinite Bombs PL1)", "be", 2),
            "bombs_p2": v(0x80FF36, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)", "be", 2),
            "power": v(0x80FEC2, f"shot level of player 1, 8 at most ({SRC}, Maximum Fire Power PL1)", "be", 2, max=8),
            "power_p2": v(0x80FF32, f"shot level of player 2 ({SRC}, Maximum Fire Power PL2)", "be", 2, max=8),
            "combo": v(0x81BB91, f"combo time of player 1, full = 0x38 ({SRC}, Infinite Combo Time PL1)", mult=round(100 / 0x38, 6),
                       round=1, min=0, max=100),
            "combo_p2": v(0x81BC01, f"combo time of player 2, full = 0x38 ({SRC}, Infinite Combo Time PL2)", mult=round(100 / 0x38, 6),
                          round=1, min=0, max=100)},
        "espgal": {
            "power": v(0x80EEB6, f"shot level of player 1, 8 at most ({SRC}, Maximum Fire Power PL1)", "be", 2, max=8),
            "power_p2": v(0x80EF56, f"shot level of player 2 ({SRC}, Maximum Fire Power PL2)", "be", 2, max=8),
            "stones": v(0x80EF04, f"spirit stones of player 1 for the awakening, 500 at most ({SRC}, Infinite Kakusei Counter PL1)",
                        "be", 2, max=500),
            "stones_p2": v(0x80EFA4, f"spirit stones of player 2 ({SRC}, Infinite Kakusei Counter PL2)", "be", 2, max=500)},
        "ddp2": {
            "bombs": v(0x8158A9, f"bombs of player 1, 5 at most ({SRC}, Infinite Bombs (Bomb) PL1)"),
            "bombs_p2": v(0x8158B0, f"bombs of player 2 ({SRC}, Infinite Bombs (Bomb) PL2)"),
            "power": v(0x81260B, f"shot level of player 1, 4 at most ({SRC}, Maximum Fire Power PL1)", max=4),
            "power_p2": v(0x81279D, f"shot level of player 2 ({SRC}, Maximum Fire Power PL2)", max=4),
            "combo": v(0x815A51, f"combo gauge of player 1, full = 0x40 ({SRC}, Infinite Combo Gauge PL1)", mult=round(100 / 0x40, 6),
                       round=1, min=0, max=100),
            "combo_p2": v(0x815A53, f"combo gauge of player 2, full = 0x40 ({SRC}, Infinite Combo Gauge PL2)",
                          mult=round(100 / 0x40, 6), round=1, min=0, max=100),
            "stage": v(0x815525, f"stage, the value read plus one ({SRC}, Select Current Stage)", add=1)},
        "hotdogst": {
            "bombs_p2": v(0x3010F3, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "power": v(0x3011ED, f"shot level of player 1, 3 at most ({SRC}, Always Max Power PL1)", max=3),
            "power_p2": v(0x3011EF, f"shot level of player 2 ({SRC}, Always Max Power PL2)", max=3)},
        "mazinger": {
            "bombs_p2": v(0x100AE6, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "power": v(0x100AB8, f"weapon level of player 1, 3 at most ({SRC}, Always have Full Power Weapon PL1)", max=3),
            "power_p2": v(0x100AE8, f"weapon level of player 2 ({SRC}, Always have Full Power Weapon PL2)", max=3)},
        "agallet": {
            "bombs_p2": v(0x100E33, f"bombs of player 2 ({SRC}, Infinite Bombs PL2)"),
            "power": v(0x100D7C, f"shot power of player 1, 0x1D at most ({SRC}, Maximum Fire Power PL1)", max=0x1D),
            "power_p2": v(0x100E3C, f"shot power of player 2 ({SRC}, Maximum Fire Power PL2)", max=0x1D)},
    }


# the clones whose own cheats put the values elsewhere (DoDonPachi Dai-Ou-Jou Black Label) / les versions qui les mettent ailleurs
def hand_clones(fam):
    def v(addr, note, kind="u8", n=1, **extra):
        out = value(addr, n, fam, kind, note)
        out.update(extra)
        return out
    blk = {"lives": v(0x8130BA, f"lives of player 1 ({SRC}, Black Label, Infinite Lives PL1)", "be", 2),
           "lives_p2": v(0x8130BC, f"lives of player 2 ({SRC}, Black Label)", "be", 2),
           "bombs": v(0x810406, f"bombs of player 1 ({SRC}, Black Label, Infinite Bombs PL1)"),
           "bombs_max": v(0x810407, f"bomb slots of player 1 ({SRC}, Black Label)"),
           "bombs_p2": v(0x810468, f"bombs of player 2 ({SRC}, Black Label)"),
           "bombs_max_p2": v(0x810469, f"bomb slots of player 2 ({SRC}, Black Label)"),
           "power": v(0x810402, f"shot level of player 1 ({SRC}, Black Label)", "be", 2, max=8),
           "power_p2": v(0x810464, f"shot level of player 2 ({SRC}, Black Label)", "be", 2, max=8),
           "combo": v(0x81B5B9, f"combo gauge of player 1, full = 0x38 ({SRC}, Black Label)", mult=round(100 / 0x38, 6), round=1, min=0,
                      max=100),
           "combo_p2": v(0x81B5E3, f"combo gauge of player 2 ({SRC}, Black Label)", mult=round(100 / 0x38, 6), round=1, min=0, max=100),
           "credits": v(0x80395A, f"credits ({SRC}, Black Label, Infinite Credits)")}
    return {"ddpdojblk": blk, "ddpdojblka": blk, "ddpdojblkb": blk, "ddpdojblkbl": blk}


# the version whose cheats the values of hand() were read from, when it is not the parent: the others, the parent too, get
# theirs where their own cheats write / la version dont les codes ont donné les valeurs de hand(), quand ce n'est pas le parent
REF = {"ddp3": "ddpdoj"}
# values a version does not have, its program being another one: the routine addresses read in DoDonPachi are those of the
# World program (ddonpach), the Japanese one and the Arrange version keep theirs elsewhere. Their boss comes where the stage
# stops scrolling. / valeurs qu'une version n'a pas, son programme étant un autre
OFF = {"ddonpach": {x: {"_stage_task": {"addr": "", "type": "be", "bytes": 4,
                                        "note": "the routines of this version's program are elsewhere, not read: the boss comes "
                                                "where its stage stops scrolling"}} for x in ("ddonpachj", "ddonpacha")}}


def ddp_mode(lives, score, alone, other_alone):
    """p1_mode or p2_mode of DoDonPachi, from its game state (_state) and the ships each player has, the ship in play counted
    (lives 0 and more): 0 both players, 7 player 1, 6 player 2, 8 continue for a player who has scored. At the ship select (0x0B)
    nobody has ships yet: the players' flags say who came in once the game has set them (0x80), else player 1. Nothing is
    guessed from what moves, as the RetroAchievements rich presence does it. / p1_mode ou p2_mode de DoDonPachi, d'après l'état
    du jeu et les vaisseaux de chaque joueur ; au choix du vaisseau, les drapeaux des joueurs disent qui est arrivé."""
    has = {"ge": [lives, 0]}
    out = "_out_p1" if lives == "lives" else "_out_p2"
    before = {"pick": [1, {"ge": ["lives", 0]}], "at": {"ge": ["lives_p2", 0]}} if lives == "lives" else has
    select = {"first": [{"pick": [before, {"pick": [1, 0], "at": out}], "at": {"ge": ["_players", 0x80]}}, before]}
    by_state = [has, 0, 0, 0, 0, 0, 0, 0, {"pick": [0, 2], "at": {"ge": [score, 1]}}, 0, 0, select, 0, 0]
    by_state[alone], by_state[other_alone] = 1, 0
    return {"pick": by_state, "at": "_state"}


# values made from others while the game runs ("tag" of the game file): DoDonPachi shows the continues used as the last
# digit of the score, the game keeps the tens apart, and says who plays / valeurs faites d'autres valeurs pendant le jeu
TAGS = {"ddonpach": {"score": {"sum": ["_score10", "_cont"]}, "score_p2": {"sum": ["_score10_p2", "_cont_p2"]},
                     "p1_mode": ddp_mode("lives", "_score10", 7, 6), "p2_mode": ddp_mode("lives_p2", "_score10_p2", 6, 7)},
        # the protection's ARM keeps Ketsui's score as a little-endian 32-bit number: two words for the 68000
        # l'ARM de la protection garde le score de Ketsui en 32 bits petit-boutiste : deux mots pour le 68000
        "ket": {"score": {"sum": ["_score_hi", "_score_lo"]}},
        # Dangun Feveron keeps a score per stage, the game's is their sum / un score par niveau, celui du jeu en est la somme
        "feversos": {"score": {"sum": [f"_score_s{i}" for i in range(1, 6)]}}}
LEARNED = "learned on the cabinet with learn.bat (1.31)"


# where each stage of DoDonPachi stops scrolling for its boss (RetroAchievements code notes and achievements), and how many
# steps before it the boss is announced: the game shows its WARNING a few seconds before (14 steps, about 3.7 s at a step of
# 16 pixels scrolled one pixel a frame) / où chaque niveau s'arrête pour son boss, et combien de pas avant il est annoncé
DDP_BOSS_AT = (0x200, 0x160, 0x1B0, 0x200, 0x250, 0x121)
DDP_BOSS_LEAD = 14


# the routine the World program runs while the WARNING of a boss shows (_stage_task) / la routine du WARNING
DDP_WARNING = 0x6DA98


def ddp_reset():
    """1 out of a game and while the results or the ending show. / 1 hors d'une partie et pendant les résultats ou la fin."""
    out_of_play = [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1]       # by _state: no game going on / pas de partie en cours
    results = [0, 0, 0, 1, 1]                                       # by phase: the results, the ending / les résultats, la fin
    return {"ge": [{"sum": [{"pick": out_of_play, "at": "_state"}, {"pick": results, "at": "phase"}]}, 1]}


def ddp_boss():
    """DoDonPachi's boss, 1 from its WARNING until the results of the stage. In the World program, from the WARNING of the game
    itself, its routine read in _stage_task: the carrier that drops the ship at the start of stage 1 is no boss. In the other
    versions, whose routines are elsewhere, a little before the stage stops scrolling, once the stage was seen scrolling toward
    it in a game going on ("rise"), the true last boss of the second loop at once. / Le boss, de son WARNING aux résultats : le
    WARNING du jeu lui-même dans le programme mondial, ailleurs un peu avant l'arrêt du niveau."""
    warning = {"eq": ["_stage_task", DDP_WARNING]}
    by_warning = {"rise": {"ge": [warning, 0]}, "from": warning, "reset": ddp_reset()}
    warn = [None] + [a - DDP_BOSS_LEAD for a in DDP_BOSS_AT] + [{"pick": [100000, 0], "at": "loop"}]
    seen = [None] + [{"pick": [1, 0], "at": {"ge": ["distance", a - DDP_BOSS_LEAD]}} for a in DDP_BOSS_AT] + [1]
    by_scroll = {"rise": {"ge": ["distance", {"pick": warn, "at": "stage"}]}, "from": {"pick": seen, "at": "stage"},
                 "reset": ddp_reset()}
    return {"first": [by_warning, by_scroll]}


# values made from others for the scenes ("derived"): DoDonPachi's boss (ddp_boss) and its name (DoDonPachi Database of
# BeeStorm, Japanese Wikipedia) / valeurs faites d'autres valeurs pour les scènes : le boss de DoDonPachi et son nom
DERIVED = {"ddonpach": {
    "warning": {"eq": ["_stage_task", DDP_WARNING]},
    "boss": ddp_boss(),
    # the boss's life: stage 6 keeps it 0x40 before the others (the stage read plus one picks it) / la vie du boss
    "boss_hp": {"pick": ["_boss_hp"] * 6 + ["_boss_hp_b", "_boss_hp"], "at": "stage"},
    "boss_name": {"value": "stage", "names": {"1": "SUZAKU", "2": "SENKOU", "3": "KAKOU", "4": "RAIKOU", "5": "RANKOU", "6": "RYUUKOU",
                                              "7": "HIBACHI"}}}}


# names of the values that tell a choice / noms des valeurs qui disent un choix
NAMES = {"ddonpach": {"p1_ship": ("ship", {"0": "TYPE-A", "1": "TYPE-B", "2": "TYPE-C"}),
                      "p2_ship": ("ship_p2", {"0": "TYPE-A", "1": "TYPE-B", "2": "TYPE-C"})},
         "feversos": {"p1_ship": ("ship", {"0": "TYPE-A", "8": "TYPE-B", "16": "TYPE-C"}),
                      "p2_ship": ("ship_p2", {"0": "TYPE-A", "8": "TYPE-B", "16": "TYPE-C"})},
         "guwange": {"p1_char": ("char", {"0": "SISIN", "1": "KOSAME", "2": "GENSUKE"}),
                     "p2_char": ("char_p2", {"0": "SISIN", "1": "KOSAME", "2": "GENSUKE"})}}


# ------------------------------------------------------------------ FinalBurn Neo list
def drivers(src, fname):
    out = []
    for m in re.finditer(r"struct BurnDriver\w*\s+BurnDrv\w+\s*=\s*\{(.*?)\n\};", src, re.S):
        body = m.group(1)
        toks = re.findall(r'"((?:[^"\\]|\\.)*)"|\b(NULL)\b', body)
        vals = [a if a or not b else None for a, b in toks]
        hw = re.search(r"\b(HARDWARE_[A-Z0-9_]+(?:\s*\|\s*HARDWARE_[A-Z0-9_]+)*)", body)
        genre = re.search(r"\b(GBF_[A-Z_]+(?:\s*\|\s*GBF_[A-Z_]+)*)", body)
        flags = re.search(r"\b(BDF_[A-Z_]+(?:\s*\|\s*BDF_[A-Z_]+)*)", body)
        out.append({"name": vals[0], "parent": vals[1], "desc": (vals[5] or "").split("\\0")[0], "file": fname,
                    "hw": hw.group(1) if hw else "", "genre": genre.group(1) if genre else "", "flags": flags.group(1) if flags else ""})
    return out


def board(d):
    return "CV1000" if "CV1000" in d["hw"] else "PGM" if "PGM" in d["hw"] else "CAVE"


CV1000_RAM = (0xC000000, 0x800000)            # the 8 MB of the CV1000's RAM / les 8 Mo de RAM du CV1000


def window(d, cv_size=0x200000):
    """(RAM base, size, layout for RetroArch) of a set. The CV1000 gives RetroArch its 8 MB, read as far as the values of
    the game go (cv_size): 2 MB for most, more for those that keep them further (Ibara, Pink Sweets, Muchi Muchi Pork).
    / La RAM partagée avec RetroArch. Le CV1000 se lit aussi loin que vont les valeurs du jeu."""
    b = board(d)
    if b == "PGM":
        return 0x800000, 0x20000, {"ram_base": "0x800000", "ram_size": "0x20000", "swap16": True,
                                   "note": "FinalBurn Neo core: PGM 68000 RAM from 0x800000 (128 KB), bytes swapped within 16-bit words"}
    if b == "CV1000":
        mb = cv_size // 0x100000
        return 0xC000000, cv_size, {"ram_base": "0xC000000", "ram_size": f"0x{cv_size:X}", "swap16": True,
                                    "note": f"FinalBurn Neo core: CV1000 SH-3 RAM from 0xC000000, the first {mb} MB of its 8, as far as "
                                            "the values of the game go, bytes swapped within 16-bit words"}
    base = SET_BASES.get(d["name"], BASES.get(d["file"], 0x100000))
    size = SIZES.get(d["file"], 0x10000)
    return base, size, {"ram_base": f"0x{base:X}", "ram_size": f"0x{size:X}", "swap16": True,
                        "note": f"FinalBurn Neo core: Cave 68000 work RAM from 0x{base:X} ({size // 1024} KB), bytes swapped "
                                "within 16-bit words"}


def scene_of(genre):
    for flags, scene in SCENES:
        if any(f in genre for f in flags):
            return scene
    return "cave_action"


# ------------------------------------------------------------------ what the cheats give / ce que donnent les codes
PATTERNS = {"bombs_p2": re.compile(rf"^infinite bombs(?: \(bomb\))? {PL}2$", re.I),
            "stage": re.compile(r"^select (?:starting|current) (?:stage|level)$", re.I),
            "round": re.compile(r"^select starting round$", re.I)}


def cave_values(cs, fam):
    """The values the CPS rules do not see: player 2's bombs, the stage. / Ce que les règles CPS ne voient pas."""
    out = {}
    for c in cs:
        for key, pat in PATTERNS.items():
            if key in out or not pat.match(c["name"]):
                continue
            t = enabled(c)
            if not t:
                continue
            if key == "bombs_p2":
                out[key] = value(t[0][1], 1, fam, "u8", f"bombs of player 2 ({c.get('src') or SRC}, {c['name']})")
            else:
                spec = value(t[0][1], 1, fam, "u8", f"{key}, the value read plus one ({c.get('src') or SRC}, {c['name']})")
                spec["add"] = 1
                out[key] = spec
    return out


def locate(cs, addr):
    """(cheat, option, write) of the first write of a cheat at this address. / Le code et l'écriture à cette adresse."""
    for c in cs:
        for o in c["options"]:
            for i, t in enumerate(o["triples"]):
                if t[1] == addr:
                    return c["name"], o["n"], i
    return None


def address_of(cs, where):
    name, n, i = where
    for c in cs:
        if c["name"] == name:
            for o in c["options"]:
                if o["n"] == n and len(o["triples"]) > i:
                    return o["triples"][i][1]
    return None


def clone_values(x, vals, kept, cs, load_cs, fam, name):
    """A version whose own cheats put values elsewhere (DoDonPachi Dai-Ou-Jou V100, Guwange Special...): each value read
    where the same cheat of that version writes, in the same shape as the parent's (a word stays a word). The values its
    cheats do not give, in a part of the RAM where the others moved, are left to learn rather than read at a wrong place.
    / Une version dont les codes mettent des valeurs ailleurs : chaque valeur lue là où écrit le même code de cette
    version, de la même forme. Celles que ses codes ne donnent pas, dans une partie de la RAM où les autres ont bougé,
    sont à apprendre plutôt que lues au mauvais endroit."""
    xc = load_cs(x)
    if not xc:
        return {}
    moved, found = {}, set()
    for k, v in vals.items():
        if k in kept or k.startswith("_") or not v.get("addr"):
            continue
        where = locate(cs, int(v["addr"], 16))
        a2 = address_of(xc, where) if where else None
        if a2 is None:
            continue
        found.add(k)
        if a2 != int(v["addr"], 16):
            moved[k] = dict(v, addr=f"0x{a2:X}", note=f"{v.get('note', '')} ({x}: its own cheats)")
    if moved:
        regions = {int(v["addr"], 16) >> 16 for v in moved.values()}
        for k, v in vals.items():
            if k in moved or k in found or k in kept or k.startswith("_") or not v.get("addr"):
                continue
            if int(v["addr"], 16) >> 16 in regions:
                moved[k] = {"addr": "", "type": v.get("type", "u8"),
                            "note": f"not known for {x}: its cheats put the other values elsewhere, learn it with learn.bat"}
    return moved


def shooter_demo(merged, derived):
    """The demo of a Cave shoot'em up (demo.bat): the coin screen, then a game where the gauge drains and fills, the hit
    counter climbs, the bombs go and come back with their slots, the shot grows, the ship and the stage change.
    / La démo : l'écran des pièces, puis une partie où la jauge se vide et se remplit, le compteur de coups monte, les
    bombes partent et reviennent, le tir grandit, le vaisseau et le niveau changent."""
    demo = {"attract": True, "credits": 0, "p1_mode": 1, "p2_mode": 0, "score": 0}
    sim = {}
    if "lives" in merged:
        demo["lives"] = 3
    if "bombs" in merged:
        demo["bombs"] = 3
        sim["bombs"] = {"cycle": [3, 3, 2, 2, 1, 2, 3, 3], "every": 6.0, "start": 9.0}
    if "bombs_max" in merged:
        demo["bombs_max"] = 3
        sim["bombs_max"] = {"cycle": [3, 4, 4, 5, 6, 6, 3], "every": 14.0, "start": 22.0}
    if "power" in merged:
        top = int(merged["power"].get("max", 4))
        demo["power"] = 1
        sim["power"] = {"cycle": list(range(1, top + 1)) + [top, top, 1], "every": 7.0, "start": 6.0}
    if "combo" in merged:
        demo["combo"] = 0
        sim["combo"] = {"cycle": [100, 92, 84, 100, 94, 86, 78, 100, 96, 88, 80, 72, 100, 90, 80, 70, 58, 46, 34, 22, 10, 0, 0, 0],
                        "every": 0.25, "start": 4.0}
    if "hits" in merged:
        demo["hits"] = 0
        sim["hits"] = {"count": [0, 180, 3], "every": 0.3, "start": 4.0}
    for key, out in (("ship", "p1_ship"), ("char", "p1_char")):
        if key in merged and out in derived:
            keys = sorted((int(k) for k in derived[out]["names"]))
            demo[key] = keys[0]
            sim[key] = {"cycle": keys, "every": 40.0, "start": 40.0}
    for key in ("stage", "round"):
        if key in merged:
            demo[key] = 1
            sim[key] = {"cycle": list(range(1, 8)), "every": 30.0, "start": 30.0}
    if "multiplier" in merged:
        demo["multiplier"] = 1
        sim["multiplier"] = {"cycle": [1, 2, 3, 4, 6, 8, 12, 16, 16, 1], "every": 2.5, "start": 6.0}
    if "stones" in merged:
        demo["stones"] = 120
        sim["stones"] = {"cycle": [120, 160, 200, 260, 320, 380, 300, 220, 140, 60, 0, 40, 80], "every": 1.2, "start": 6.0}
    if "energy" in merged:
        demo["energy"] = 100
        sim["energy"] = {"cycle": [100, 100, 80, 60, 40, 20, 100], "every": 3.0, "start": 6.0}
    for k in ("score_p2", "lives_p2", "bombs_p2", "bombs_max_p2", "power_p2", "combo_p2", "hits_p2", "ship_p2", "char_p2", "stones_p2",
              "energy_p2"):
        if k in merged:                          # player 1 alone: player 2's values stay still / le joueur 1 seul
            v = {"lives_p2": 0, "bombs_p2": 0, "bombs_max_p2": 0}.get(k, 0)
            demo[k] = v
            sim[k] = {"cycle": [v], "every": 3600.0, "start": 3600.0}
    if sim:
        demo["sim"] = sim
    return demo


# ------------------------------------------------------------------ build / construction
def build(fbneo, cheats_dir, games_dir, mame_path=""):
    ds = []
    folder = os.path.join(fbneo, CAVE_DIR)
    for fname in sorted(os.listdir(folder)):
        if fname.startswith("d_") and fname.endswith(".cpp"):
            with open(os.path.join(folder, fname), encoding="latin-1") as f:
                ds += drivers(f.read(), fname)
    with open(os.path.join(fbneo, PGM_FILE), encoding="latin-1") as f:
        pgm = drivers(f.read(), "d_pgm.cpp")
    by_pgm = {d["name"]: d for d in pgm}

    def pgm_root(d):
        seen = set()
        while d["parent"] and d["parent"] in by_pgm and d["name"] not in seen:
            seen.add(d["name"])
            d = by_pgm[d["parent"]]
        return d["name"]
    ds += [d for d in pgm if pgm_root(d) in PGM_CAVE]
    ds = [d for d in ds if d["name"] and d["name"] not in SKIP]
    by = {d["name"]: d for d in ds}

    def root(d):
        seen = set()
        while d["parent"] and d["parent"] in by and d["name"] not in seen:
            seen.add(d["name"])
            d = by[d["parent"]]
        return d
    groups = {}
    for d in ds:
        groups.setdefault(root(d)["name"], []).append(d)
    mame = MameCheats(mame_path)
    mame.preload([d["name"] for d in ds])
    loaded = {}

    def load_cs(x):
        """The cheats of a version: FinalBurn Neo's, then MAME's it does not have. / Les codes d'une version."""
        if x not in loaded:
            loaded[x] = merge_cheats(cheats(os.path.join(cheats_dir, x + ".ini")), mame.get(x))
        return loaded[x]
    make_templates(games_dir, TEMPLATES, "Cave", TOOL)
    make_shoot_template(games_dir)
    report = []
    for name in sorted(groups):
        p = by[name]
        sets = [name] + sorted(x["name"] for x in groups[name] if x["name"] != name)
        base, size, ra = window(p, CV1000_RAM[1])  # the CV1000 cut down below, once its values are known / coupé plus bas
        fam = f"{board(p)}@{base:X}"
        cps_games.WINDOWS[fam] = (base, size)
        ref = None                                   # the version whose cheats give the values / celle dont les codes servent
        for x in [REF.get(name), name] + sets[1:]:
            if x and load_cs(x):
                ref = x
                break
        cs = load_cs(ref) if ref else []
        vals, derived, got = values_from_cheats(cs, fam, name)
        for k, v in cave_values(cs, fam).items():
            vals.setdefault(k, v)
        extra = hand(fam).get(name, {})
        scene = scene_of(p["genre"])
        tags = TAGS.get(name, {})
        if scene == "cave_shoot":                    # the energy of a shoot'em up, not the health of a fight / l'énergie d'un shoot
            for a, b in (("health", "energy"), ("health_p2", "energy_p2")):
                if a in vals and b not in vals and b not in extra:
                    vals[b] = vals.pop(a)
                    vals[b]["note"] = vals[b]["note"].replace("health in %", "energy in %")
                vals.pop(a, None)
        if scene in ("cave_shoot", "cave_reflexion"):
            for k, v in SCORES.items():
                if k not in tags:
                    extra.setdefault(k, v)
        vals.update(extra)
        title = clean(p["desc"])
        titles = {}
        for x in groups[name]:
            t = clean(x["desc"])
            if x["name"] != name and t and t != title:
                titles[x["name"]] = t
        path = os.path.join(games_dir, name + ".json")
        old = load(path)
        if old is not None and old.get("generated") != TOOL:
            report.append(f"{name}: games/{name}.json is not one of ours, left as it is")
            continue
        d = old if old is not None else {}
        d["title"] = d.get("title_hand") or TITLES.get(name) or title
        if name in TITLES and title != d["title"]:
            titles[name] = title
        kind = {"cave_combat": "fighting game", "cave_shoot": "shoot'em up", "cave_reflexion": "puzzle game",
                "cave_action": "action game"}[scene]
        maker = "by Cave" if name in BY_CAVE else ("by IGS under Cave's licence" if name == "ddp2" else "on the Cave board")
        known = [k for k in vals if not k.startswith("_") and vals[k].get("addr")] + list(tags)
        dbs = " and ".join(db for db, word in (("FinalBurn Neo", "FBNeo cheat database"), ("MAME", "MAME cheat database"))
                           if any(word in str(v.get("note", "")) for v in vals.values()))
        d["note"] = (f"{kind[0].upper() + kind[1:]} {maker} ({board(p)}): " + (", ".join(known) if known else "no value known yet")
                     + (f" ({dbs} cheat database{'s' if ' and ' in dbs else ''})" if dbs else "") + f". Made by {TOOL}.")
        d["generated"] = TOOL
        d["cave"] = board(p)
        d["match"] = [{"system": sets}]
        d["retroarch"] = dict(ra, content=sets)
        if titles:
            d["titles"] = titles
        else:
            d.pop("titles", None)
        if "scene" not in d:
            d["scene_from"] = scene
        mem = d.get("memory") if isinstance(d.get("memory"), dict) else {}
        kept = {k: v for k, v in (mem.get("values") or {}).items()
                if isinstance(v, dict) and v.get("addr") and "cheat database" not in str(v.get("note", ""))}
        merged = dict(vals)
        merged.update(kept)                          # learned or set by hand wins / ce qui est appris passe avant
        for k in tags:                               # made while the game runs, not read / fait pendant le jeu, pas lu
            merged.pop(k, None)
        if tags:
            d["tag"] = tags
        else:
            d.pop("tag", None)
        per = {}
        clones = hand_clones(fam)
        for x in sets:
            if x == ref or (x == name and ref is None):
                continue
            diff = {k: v for k, v in clones.get(x, {}).items() if k not in kept}
            if not diff:
                diff = clone_values(x, vals, kept, cs, load_cs, fam, name)
            off = OFF.get(name, {}).get(x)
            if off:                                  # another program: not read there / un autre programme : pas lu là
                diff = dict(diff or {}, **off)
            if diff:
                per[x] = diff
        if per:
            d["per_game"] = per
        else:
            d.pop("per_game", None)
        if board(p) == "CV1000":                     # read as far as its values go / lu aussi loin que vont ses valeurs
            lo, most = CV1000_RAM
            far = [int(v["addr"], 16) for vs in [merged] + list(per.values()) for v in vs.values()
                   if isinstance(v, dict) and v.get("addr") and lo <= int(v["addr"], 16) < lo + most]
            cv_size = max(0x200000, (max(far) - lo) // 0x100000 * 0x100000 + 0x100000) if far else 0x200000
            ra = window(p, cv_size)[2]
            d["retroarch"] = dict(ra, content=sets)
        d["memory"] = {"cpu": ":maincpu", "values": merged}
        dv = d.get("derived") if isinstance(d.get("derived"), dict) else {}
        dv.update(derived)
        for out, (src, names) in NAMES.get(name, {}).items():
            dv[out] = {"value": src, "names": names}
        for out, spec in DERIVED.get(name, {}).items():
            dv[out] = spec
        for k in list(dv):                           # names of a value no longer read / noms d'une valeur plus lue
            spec = dv[k] if isinstance(dv[k], dict) else {}
            used = [spec["value"]] if isinstance(spec.get("value"), str) else [x for x in spec.get("join") or [] if isinstance(x, str)]
            if used and any(u not in merged for u in used):
                del dv[k]
        if dv:
            d["derived"] = dv
        else:
            d.pop("derived", None)
        if name in HD:
            hd_old = d.get("hd") if isinstance(d.get("hd"), dict) else {}
            hd_old["scene"] = HD[name]
            d["hd"] = hd_old
        watch = [k for k in ("time", "_time", "health", "health_p2", "lives", "lives_p2", "bombs", "bombs_p2", "score", "score_p2")
                 if k in merged or k in tags]
        moving = [k for k in ("time", "_time", "score", "score_p2") + (("health", "health_p2") if scene == "cave_combat" else ())
                  if k in merged or k in tags]
        if moving and "p1_mode" not in tags:         # the game says who plays: nothing to guess / le jeu dit qui joue
            d["activity"] = {"values": watch, "moving": moving, "seconds": 10,
                             "note": "no BIOS says who plays: player 1 plays while these values move, as long as one of "
                                     "the moving ones is read (lives or bombs alone change too seldom)"}
        else:
            d.pop("activity", None)
        coins = d.get("coins") if isinstance(d.get("coins"), dict) else {}
        if not coins.get("hand"):
            begin = {k: pl for k, pl in (("lives", "p1"), ("lives_p2", "p2")) if k in merged and merged[k].get("addr")}
            if not (merged.get("credits") or {}).get("addr") and scene != "cave_combat" and begin:
                d["coins"] = {"begin": begin, "rise": 2,
                              "note": "credits not read: counted from the coin buttons (coin_buttons.bat). A player begins "
                                      "(start, continue, joining in) and uses one when his lives come back from 0 by 2 or "
                                      "more (an extra life is 1)"}
            else:
                d.pop("coins", None)
        if not d.get("demo_hand") and scene == "cave_shoot":
            d["demo"] = shooter_demo(merged, dv)
        elif not d.get("demo_hand"):
            demo = {"credits": 2, "p1_mode": 1, "p2_mode": 0}
            if scene == "cave_combat":
                demo.update({"health": 100, "health_p2": 100})
                if "time" in merged:
                    demo["time"] = 99
            for k in ("lives", "bombs"):
                if k in merged:
                    demo[k] = 3
            if "bombs_max" in merged:
                demo["bombs_max"] = 3
            d["demo"] = demo
        dump(path, d)
        report.append(f"{board(p):6s} {name:10s} {scene:14s} {len(sets):3d} sets  " + (", ".join(known) or "-"))
    return report


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    report = build(argv[1], argv[2], os.path.join(ROOT, "games"), argv[3] if len(argv) > 3 else "")
    print("\n".join(report))
    print(len(report), "games")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
