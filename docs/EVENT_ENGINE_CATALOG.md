# Catalogue du moteur d'événements

Fichier produit par `python tools/event_catalog.py` à partir du code et des fichiers de jeu. Ne pas le modifier à la main. Il accompagne [EVENT_ENGINE_HANDOFF.md](EVENT_ENGINE_HANDOFF.md).

303 fichiers de jeu, 4108 valeurs lues, 79 classes qui annoncent, 215 annonces dans le code, 289 règles d'annonce de la dalle LED.

## 1. Les jeux

Pour chaque fichier de jeu, la partie de l'écran HD qui le suit, les valeurs lues (les noms qui commencent par `_` servent à la détection et ne sont pas affichés), les valeurs calculées, les options du bloc `hd`, les annonces de sa dalle LED et le nombre de parties réelles gardées dans `tests/captures`. Les adresses sont dans [EVENT_ENGINE_VALUES.md](EVENT_ENGINE_VALUES.md).

### FightFX (`dmd/hd_fight.py`)

**3countb** — 3 Count Bout — scène LED de `neogeo_combat`
- valeurs (9) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, score, score_p2
- internes (4) : _in_p1, _in_p2, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : specials (9 combattants)

**aodk** — Aggressors of Dark Kombat — scène LED de `neogeo_combat`
- valeurs (12) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, score, score_p2
- internes (2) : _time, _time_sub
- `hd` : 10 décors

**aof** — Art of Fighting — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, rounds, rounds_p2, time, score, score_p2, power, power_p2
- internes (5) : _in_p1, _in_p2, _time_sub, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 13 décors
- aussi : specials (12 combattants)

**aof2** — Art of Fighting 2 (2 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, rounds, rounds_p2, time, score, score_p2, power, power_p2
- internes (7) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 16 décors
- aussi : specials (15 combattants)

**aof3** — Art of Fighting 3 (2 romsets) — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 18 décors
- aussi : specials (12 combattants)

**breakers** — Breakers — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2
- internes (8) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _time_sub, _fight_cue
- `derived` : p1_char, p2_char
- `hd` : 9 décors
- aussi : specials (11 combattants)

**breakrev** — Breakers Revenge — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2
- internes (8) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _time_sub, _fight_cue
- `derived` : p1_char, p2_char
- `hd` : 10 décors
- aussi : specials (12 combattants)

**cave_combat** — modèle, pas un jeu

**cps_combat** — modèle, pas un jeu

**cybots** — Cyberbots: Fullmetal Madness (6 romsets) — scène LED de `cps_combat`
- valeurs (7) : health, health_p2, time, credits, power, power_p2, backdrop
- internes (1) : _p1_chr
- `derived` : p1_char
- `hd` : 16 décors
- aussi : activity

**doubledr** — Double Dragon — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop
- internes (8) : _in_p1, _in_p2, _time_sub, _fight_cue, _p1_chr, _p2_chr, _p1_dir, _p2_dir
- `derived` : p1_char, p2_char
- `hd` : 14 décors
- aussi : specials (15 combattants)

**dragonsh** — Dragon's Heaven — scène LED de `neogeo_combat`
- valeurs (9) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, score, score_p2

**dstlk** — Darkstalkers: The Night Warriors (12 romsets) — scène LED de `cps_combat`
- valeurs (4) : health, health_p2, time, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (14 combattants), activity

**fatfursp** — Fatal Fury Special (2 romsets) — scène LED de `neogeo_combat`
- valeurs (14) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop, round
- internes (8) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _time_sub, _fight_cue
- `derived` : p1_char, p2_char
- `hd` : 17 décors
- aussi : specials (14 combattants)

**fatfury1** — Fatal Fury — scène LED de `neogeo_combat`
- valeurs (14) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, time, score, score_p2, rounds, rounds_p2, round
- internes (15) : _in_p1, _in_p2, _p1_dir, _p2_dir, _p2_hp, _cpu_hp, _time_sub, _fight_cue, _p1_chr, _p2_chr, _cpu_chr, _round_result, _sc2_a, _sc2_b, _sc2_c
- `derived` : p1_char, p2_char
- `tag` : p2_mode, health_p2
- `hd` : health_drain=0.3
- aussi : specials (4 combattants)
- parties réelles dans `tests/captures` : 2

**fatfury2** — Fatal Fury 2 — scène LED de `neogeo_combat`
- valeurs (14) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop, round
- internes (7) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 15 décors
- aussi : specials (14 combattants)

**fatfury3** — Fatal Fury 3 — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, time, score, score_p2, backdrop, rounds, rounds_p2
- internes (11) : _in_p1, _in_p2, _p1_dir, _p2_dir, _hp, _hp_vs, _hp_p2, _hp_p2_vs, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `tag` : health, health_p2
- `hd` : 16 décors
- aussi : specials (15 combattants)

**fightfev** — Fight Fever (2 romsets) — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2
- internes (6) : _in_p1, _in_p2, _p1_dir, _p2_dir, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 11 décors
- aussi : specials (12 combattants)

**galaxyfg** — Galaxy Fight — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2
- internes (6) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (10 combattants)

**garou** — Garou (4 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, rounds, rounds_p2, time, score, score_p2, backdrop, power, power_p2
- internes (7) : _in_p1, _in_p2, _p1_dir, _p2_dir, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 14 décors
- aussi : specials (15 combattants)

**gowcaizr** — Voltage Fighter Gowcaizer — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 13 décors
- aussi : specials (14 combattants)

**hsf2** — Hyper Street Fighter II: The Anniversary Edition (14 romsets) — scène LED de `cps_combat`
- valeurs (8) : health, health_p2, time, credits, power, power_p2, score, score_p2
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 10 décors
- aussi : specials (19 combattants), activity

**jojo** — JoJo's Venture (15 romsets) — scène LED de `cps_combat`
- valeurs (6) : health, health_p2, time, credits, power, power_p2
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 5 décors
- aussi : specials (15 combattants), activity, per_game

**jojoba** — JoJo's Bizarre Adventure (11 romsets) — scène LED de `cps_combat`
- valeurs (7) : health, health_p2, time, credits, power, power_p2, score
- internes (4) : _p1_ctl, _p2_ctl, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 5 décors
- aussi : specials (24 combattants), activity

**kabukikl** — Kabuki Klash — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, backdrop, power, power_p2, health, health_p2, rounds, rounds_p2, time, score, score_p2
- internes (4) : _in_p1, _in_p2, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (14 combattants)

**karnovr** — Karnov's Revenge — scène LED de `neogeo_combat`
- valeurs (14) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, score, score_p2, time, rounds, rounds_p2
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _p1_chr, _p2_chr, _time_sub, _fight_cue
- `derived` : p1_char, p2_char
- aussi : specials (15 combattants)

**kf2k3pcb** — The King of Fighters 2003 (Japan, JAMMA PCB) — scène LED de `neogeo_combat`
- valeurs (12) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, time, score, score_p2, beat, beat_p2
- internes (2) : _in_p1, _in_p2

**kizuna** — Kizuna Encounter (2 romsets) — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2
- internes (7) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _time_sub
- `derived` : p1_char, p2_char
- `hd` : 19 décors
- aussi : specials (13 combattants)

**kof2000** — The King of Fighters 2000 (2 romsets) — scène LED de `neogeo_combat`
- valeurs (16) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, round, backdrop
- internes (22) : _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_lost, _p1_ch0, _p1_ch1, _p1_ch2, _p1_ch3, _p1_ord0, _p1_ord1, _p1_ord2, _p2_lost, _p2_ch0, _p2_ch1, _p2_ch2, _p2_ch3, _p2_ord0, _p2_ord1, _p2_ord2, _in_p1, _in_p2
- `derived` : p1_char, p2_char
- `hd` : 9 décors
- aussi : specials (38 combattants)

**kof2001** — The King of Fighters 2001 (2 romsets) — scène LED de `neogeo_combat`
- valeurs (15) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, backdrop
- internes (16) : _time_sub, _fight_cue, _p1_lost, _p1_cur, _p1_seq0, _p1_seq1, _p1_seq2, _p2_lost, _p2_cur, _p2_seq0, _p2_seq1, _p2_seq2, _p1_dir, _p2_dir, _in_p1, _in_p2
- `derived` : p1_char, p2_char, round
- `hd` : 9 décors
- aussi : specials (44 combattants)

**kof2002** — The King of Fighters 2002 — scène LED de `neogeo_combat`
- valeurs (19) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, backdrop, power, power_p2, power_level, power_level_p2
- internes (29) : _fight_cue, _screen, _p1_lost, _p1_ch0, _p1_ch1, _p1_ch2, _p1_cur, _p2_lost, _p2_ch0, _p2_ch1, _p2_ch2, _p2_cur, _p1_seq0, _p1_seq1, _p1_seq2, _p2_seq0, _p2_seq1, _p2_seq2, _in_p1, _in_p2, _fight_state, _pow, _pow_p2, _stock, _stock_p2, _maxv, _maxv_p2, _dm, _dm_p2
- `derived` : select, p1_char, p2_char, round
- `hd` : pow_full=64, maxv_full=47, max_buttons="BC", max_dm_free=true, 9 décors
- aussi : moves (41 combattants)
- parties réelles dans `tests/captures` : 3

**kof2003** — The King of Fighters 2003 (2 romsets) — scène LED de `neogeo_combat`
- valeurs (12) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, time, score, score_p2, beat, beat_p2
- internes (11) : _time_sub, _p1_ch0, _p1_ch1, _p1_ch2, _p1_act, _p2_ch0, _p2_ch1, _p2_ch2, _p2_act, _in_p1, _in_p2
- `derived` : p1_char, p2_char
- aussi : specials (39 combattants)

**kof94** — The King of Fighters '94 — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, backdrop, power, power_p2
- internes (8) : _time_sub, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _screen, _in_p1, _in_p2
- `derived` : select, p1_char, p2_char
- `hd` : 9 décors
- aussi : specials (26 combattants)

**kof95** — The King of Fighters '95 (3 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, backdrop, power, power_p2
- internes (20) : _time_sub, _fight_cue, _p1_lost, _p1_ch0, _p1_ch1, _p1_ch2, _p1_ord0, _p1_ord1, _p1_ord2, _p2_lost, _p2_ch0, _p2_ch1, _p2_ch2, _p2_ord0, _p2_ord1, _p2_ord2, _p1_dir, _p2_dir, _in_p1, _in_p2
- `derived` : p1_char, p2_char
- `hd` : 9 décors
- aussi : specials (28 combattants)

**kof96** — The King of Fighters '96 (2 romsets) — scène LED de `neogeo_combat`
- valeurs (18) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, round, backdrop, power, power_p2
- internes (20) : _p1_dir, _p2_dir, _time_sub, _p1_lost, _p1_ch0, _p1_ch1, _p1_ch2, _p1_ord0, _p1_ord1, _p1_ord2, _p2_lost, _p2_ch0, _p2_ch1, _p2_ch2, _p2_ord0, _p2_ord1, _p2_ord2, _screen, _in_p1, _in_p2
- `derived` : p1_char, p2_char, select
- `hd` : 11 décors
- aussi : specials (31 combattants)

**kof97** — The King of Fighters '97 (3 romsets) — scène LED de `neogeo_combat`
- valeurs (16) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, round, backdrop
- internes (28) : _time_sub, _fight_state, _p1_lost, _p1_ch0, _p1_ch1, _p1_ch2, _p1_ord0, _p1_ord1, _p1_ord2, _p2_lost, _p2_ch0, _p2_ch1, _p2_ch2, _p2_ord0, _p2_ord1, _p2_ord2, _pow, _pow_p2, _stock, _stock_p2, _maxv, _maxv_p2, _pmode, _pmode_p2, _dm, _dm_p2, _in_p1, _in_p2
- `derived` : p1_char, p2_char
- `hd` : ready_go=0.85, pow_full=128, stock_max=3, 8 décors
- aussi : moves (29 combattants)
- parties réelles dans `tests/captures` : 1

**kof98** — The King of Fighters '98 (5 romsets) — scène LED de `neogeo_combat`
- valeurs (16) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, round, backdrop
- internes (27) : _time_sub, _fight_state, _p1_lost, _p1_ch0, _p1_ch1, _p1_ch2, _p1_ord0, _p1_ord1, _p1_ord2, _p2_lost, _p2_ch0, _p2_ch1, _p2_ch2, _p2_ord0, _p2_ord1, _p2_ord2, _screen, _in_p1, _in_p2, _pow, _pow_p2, _stock, _stock_p2, _pmode, _pmode_p2, _maxv, _maxv_p2
- `derived` : select, p1_char, p2_char
- `hd` : 9 décors
- aussi : moves (38 combattants)
- parties réelles dans `tests/captures` : 5

**kof99** — The King of Fighters '99 (6 romsets) — scène LED de `neogeo_combat`
- valeurs (16) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, beat, beat_p2, round, backdrop
- internes (23) : _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_lost, _p1_ch0, _p1_ch1, _p1_ch2, _p1_ch3, _p1_ord0, _p1_ord1, _p1_ord2, _p2_lost, _p2_ch0, _p2_ch1, _p2_ch2, _p2_ch3, _p2_ord0, _p2_ord1, _p2_ord2, _screen, _in_p1, _in_p2
- `derived` : p1_char, p2_char, select
- `hd` : 7 décors
- aussi : specials (35 combattants)
- parties réelles dans `tests/captures` : 1

**kotm** — King of the Monsters (2 romsets) — scène LED de `neogeo_combat`
- valeurs (10) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, score, score_p2
- internes (2) : _p2_hp, _cpu_hp
- `tag` : health_p2

**kotm2** — King of the Monsters 2 (3 romsets) — scène LED de `neogeo_combat`
- valeurs (12) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char

**lastblad** — The Last Blade (3 romsets) — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop
- internes (9) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr, _cpu_chr
- `derived` : p1_char, p2_char
- `hd` : 15 décors
- aussi : specials (15 combattants)

**lastbld2** — The Last Blade 2 — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, rounds, power, rounds_p2, power_p2, time, score, score_p2, backdrop
- internes (7) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 16 décors
- aussi : specials (19 combattants)

**legendos** — Legend of Success Joe — scène LED de `neogeo_combat`
- valeurs (10) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, score, score_p2
- internes (2) : _p2_hp, _cpu_hp
- `tag` : health_p2

**matrim** — Matrimelee — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2
- internes (7) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _time_sub
- `derived` : p1_char, p2_char
- `hd` : 14 décors
- aussi : specials (17 combattants)

**mbombrd** — Muscle Bomber Duo: Ultimate Team Battle (6 romsets) — scène LED de `cps_combat`
- valeurs (2) : health, health_p2
- internes (1) : _time
- `hd` : 1 décors
- aussi : activity

**megaman** — Mega Man: The Power Battle (7 romsets) — scène LED de `cps_combat`
- valeurs (4) : health, health_p2, score, score_p2
- internes (1) : _time
- `hd` : 4 décors
- aussi : activity

**megaman2** — Mega Man 2: The Power Fighters (6 romsets) — scène LED de `cps_combat`
- valeurs (3) : health, health_p2, score
- internes (1) : _time
- `hd` : 4 décors
- aussi : activity

**metmqstr** — Metamoqester (2 romsets) — scène LED de `cave_combat`
- valeurs (7) : health, health_p2, time, credits, lives, lives_p2, stage
- aussi : activity

**msh** — Marvel Super Heroes (11 romsets) — scène LED de `cps_combat`
- valeurs (9) : health, health_p2, time, power, power_level, power_p2, power_level_p2, rounds, rounds_p2
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 8 décors
- aussi : specials (14 combattants), activity

**mshvsf** — Marvel Super Heroes Vs. Street Fighter (19 romsets) — scène LED de `cps_combat`
- valeurs (5) : time, power, power_p2, score, score_p2
- internes (14) : _p1_chr, _p2_chr, _p1_ctl, _p2_ctl, _p1_hp1, _p1_hp2, _p1_on1, _p1_on2, _p1_chr2, _p2_hp1, _p2_hp2, _p2_on1, _p2_on2, _p2_chr2
- `derived` : p1_char, p2_char
- `tag` : health, health_p2
- `hd` : 8 décors
- aussi : specials (26 combattants), activity

**mvsc** — Marvel Vs. Capcom: Clash of Super Heroes (15 romsets) — scène LED de `cps_combat`
- valeurs (9) : time, power, power_p2, score, score_p2, credits, power_level, power_level_p2, backdrop
- internes (14) : _p1_ctl, _p2_ctl, _p1_chr, _p2_chr, _p1_hp1, _p1_hp2, _p1_on1, _p1_on2, _p1_chr2, _p2_hp1, _p2_hp2, _p2_on1, _p2_on2, _p2_chr2
- `derived` : p1_char, p2_char
- `tag` : health, health_p2
- `hd` : hand=true, 10 décors
- aussi : specials (24 combattants), activity, hyper

**neogeo_combat** (134 romsets)
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- aussi : per_game

**ninjamas** — Ninja Master's — scène LED de `neogeo_combat`
- valeurs (15) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, time, score, score_p2, power, power_p2
- internes (7) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _time_sub
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (14 combattants)

**nwarr** — Night Warriors: Darkstalkers' Revenge (11 romsets) — scène LED de `cps_combat`
- valeurs (8) : health, health_p2, rounds, rounds_p2, time, credits, score, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 14 décors
- aussi : specials (16 combattants), activity

**plegends** — Gogetsuji Legends (3 romsets) — scène LED de `cave_combat`
- valeurs (7) : health, health_p2, time, credits, power, power_p2, score
- aussi : activity

**pwrinst2** — Power Instinct 2 (5 romsets) — scène LED de `cave_combat`
- valeurs (5) : health, health_p2, time, credits, score
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : specials (16 combattants), activity

**ragnagrd** — Ragnagard — scène LED de `neogeo_combat`
- valeurs (12) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, score, score_p2
- internes (7) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _time
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (13 combattants)

**rbff1** — Real Bout Fatal Fury (4 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, rounds, rounds_p2, time, score, score_p2, power, power_p2
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 14 décors
- aussi : specials (18 combattants)

**rbff2** — Real Bout Fatal Fury 2 (3 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, rounds, rounds_p2, time, score, score_p2, backdrop, power, power_p2
- internes (6) : _in_p1, _in_p2, _p1_dir, _p2_dir, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 11 décors
- aussi : specials (25 combattants)

**rbffspec** — Real Bout Fatal Fury Special (2 romsets) — scène LED de `neogeo_combat`
- valeurs (18) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, rounds, rounds_p2, time, score, score_p2, backdrop, power, power_p2, round
- internes (9) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr, _screen
- `derived` : p1_char, p2_char, select
- `hd` : 11 décors
- aussi : specials (21 combattants)

**redearth** — Red Earth (6 romsets) — scène LED de `cps_combat`
- valeurs (4) : health, health_p2, credits, backdrop
- `hd` : 10 décors
- aussi : activity

**ringdest** — Ring of Destruction: Slammasters II (7 romsets) — scène LED de `cps_combat`
- valeurs (4) : health, health_p2, time, credits
- `hd` : 1 décors
- aussi : activity

**rotd** — Rage of the Dragons (2 romsets) — scène LED de `neogeo_combat`
- valeurs (16) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, stage, backdrop, power, power_p2
- internes (8) : _in_p1, _in_p2, _p1_chr, _p2_chr, _p1_dir, _p2_dir, _time_sub, _fight_cue
- `derived` : p1_char, p2_char
- `hd` : 9 décors
- aussi : specials (18 combattants)

**samsh5sp** — Samurai Shodown V Special (3 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, rounds, rounds_p2, time, score, score_p2, power, power_p2
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 20 décors
- aussi : specials (29 combattants)

**samsho** — Samurai Shodown (2 romsets) — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop
- internes (7) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : fight_after=0.8, 13 décors
- aussi : specials (14 combattants)

**samsho2** — Samurai Shodown II (3 romsets) — scène LED de `neogeo_combat`
- valeurs (15) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, power, power_p2, time, score, score_p2, backdrop
- internes (9) : _in_p1, _in_p2, _p1_dir, _p2_dir, _powmax, _powmax_p2, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : power_label="POW", power_timer="_powmax", health_drain=0.8, 18 décors
- aussi : specials (19 combattants)

**samsho3** — Samurai Shodown III (3 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, rounds, rounds_p2, time, score, score_p2, backdrop, power, power_p2
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 18 décors
- aussi : specials (15 combattants)

**samsho4** — Samurai Shodown IV (2 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, rounds, rounds_p2, time, score, score_p2, backdrop, power, power_p2
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (20 combattants)

**samsho5** — Samurai Shodown V (3 romsets) — scène LED de `neogeo_combat`
- valeurs (17) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, backdrop, rounds, rounds_p2, time, score, score_p2, power, power_p2
- internes (7) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 26 décors
- aussi : specials (30 combattants)

**savagere** — Savage Reign — scène LED de `neogeo_combat`
- valeurs (10) : credits, p1_mode, p2_mode, backdrop, bios_request, bios_mode, bios_timer, bios_mvs, score, score_p2
- internes (5) : _in_p1, _in_p2, _p1_chr, _p2_chr, _time
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (13 combattants)

**sf2** — Street Fighter II: The World Warrior (46 romsets) — scène LED de `cps_combat`
- valeurs (9) : health, health_p2, rounds, rounds_p2, time, credits, score, score_p2, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (9 combattants), activity

**sf2ce** — Street Fighter II': Champion Edition (98 romsets) — scène LED de `cps_combat`
- valeurs (6) : health, health_p2, rounds, rounds_p2, time, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (13 combattants), activity

**sf2hf** — Street Fighter II': Hyper Fighting (7 romsets) — scène LED de `cps_combat`
- valeurs (7) : health, health_p2, rounds, rounds_p2, time, score, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (13 combattants), activity

**sfa** — Street Fighter Alpha: Warriors' Dreams (22 romsets) — scène LED de `cps_combat`
- valeurs (10) : health, health_p2, rounds, rounds_p2, time, power, power_p2, score, score_p2, backdrop
- internes (4) : _p1_ctl, _p2_ctl, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 25 décors
- aussi : specials (15 combattants), activity

**sfa2** — Street Fighter Alpha 2 (17 romsets) — scène LED de `cps_combat`
- valeurs (6) : health, health_p2, time, power, power_p2, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 39 décors
- aussi : specials (24 combattants), activity

**sfa3** — Street Fighter Alpha 3 (23 romsets) — scène LED de `cps_combat`
- valeurs (9) : health, health_p2, time, power, power_p2, score, rounds, rounds_p2, backdrop
- internes (4) : _p1_ctl, _p2_ctl, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 59 décors
- aussi : specials (29 combattants), activity

**sfiii** — Street Fighter III: New Generation (8 romsets) — scène LED de `cps_combat`
- valeurs (7) : health, health_p2, time, credits, power, power_p2, backdrop
- internes (4) : _p1_chr, _p1_chr2, _p2_chr, _p2_chr2
- `derived` : p1_char, p2_char
- `hd` : 13 décors
- aussi : specials (13 combattants), activity

**sfiii2** — Street Fighter III 2nd Impact: Giant Attack (6 romsets) — scène LED de `cps_combat`
- valeurs (7) : health, health_p2, time, credits, power, power_p2, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 16 décors
- aussi : specials (17 combattants), activity

**sfiii3** — Street Fighter III 3rd Strike: Fight for the Future (17 romsets) — scène LED de `cps_combat`
- valeurs (8) : health, health_p2, time, credits, power, power_p2, score, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 21 décors
- aussi : specials (21 combattants), activity

**sfz2al** — Street Fighter Zero 2 Alpha (15 romsets) — scène LED de `cps_combat`
- valeurs (4) : health, health_p2, time, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 39 décors
- aussi : specials (21 combattants), activity

**sfzch** — Street Fighter Zero (7 romsets) — scène LED de `cps_combat`
- valeurs (8) : health, health_p2, rounds, rounds_p2, time, power, power_p2, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 25 décors
- aussi : specials (15 combattants), activity

**sgemf** — Super Gem Fighter: Mini Mix (6 romsets) — scène LED de `cps_combat`
- valeurs (7) : health, health_p2, time, power, power_p2, score, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 15 décors
- aussi : specials (13 combattants), activity

**slammast** — Saturday Night Slam Masters (7 romsets) — scène LED de `cps_combat`
- valeurs (2) : health, health_p2
- internes (1) : _time
- `hd` : 1 décors
- aussi : activity

**ssf2** — Super Street Fighter II: The New Challengers (20 romsets) — scène LED de `cps_combat`
- valeurs (6) : health, health_p2, rounds, rounds_p2, time, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 16 décors
- aussi : specials (17 combattants), activity

**ssf2t** — Super Street Fighter II Turbo (22 romsets) — scène LED de `cps_combat`
- valeurs (6) : health, health_p2, time, power, power_p2, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 16 décors
- aussi : specials (18 combattants), activity

**svc** — SNK vs. Capcom — scène LED de `neogeo_combat`
- valeurs (15) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, rounds, rounds_p2, time, score, score_p2, backdrop
- internes (7) : _in_p1, _in_p2, _p1_dir, _p2_dir, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 10 décors
- aussi : specials (36 combattants)

**svcpcb** — SNK vs. Capcom (JAMMA PCB) (2 romsets) — scène LED de `neogeo_combat`
- valeurs (15) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, rounds, rounds_p2, time, score, score_p2, backdrop
- internes (6) : _in_p1, _in_p2, _p1_dir, _p2_dir, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 10 décors
- aussi : specials (36 combattants)

**vhunt2** — Vampire Hunter 2: Darkstalkers Revenge (6 romsets) — scène LED de `cps_combat`
- valeurs (6) : health, health_p2, time, power, power_p2, backdrop
- internes (4) : _p1_ctl, _p2_ctl, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 25 décors
- aussi : specials (20 combattants), activity

**vsav** — Vampire Savior: The Lord of Vampire (10 romsets) — scène LED de `cps_combat`
- valeurs (4) : health, health_p2, time, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 23 décors
- aussi : specials (20 combattants), activity

**vsav2** — Vampire Savior 2: The Lord of Vampire (5 romsets) — scène LED de `cps_combat`
- valeurs (4) : health, health_p2, time, backdrop
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 25 décors
- aussi : specials (18 combattants), activity

**wakuwak7** — Waku Waku 7 — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop
- internes (6) : _in_p1, _in_p2, _p1_dir, _p2_dir, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 16 décors
- aussi : specials (10 combattants)

**wh1** — World Heroes (3 romsets) — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 32 décors
- aussi : specials (9 combattants)

**wh2** — World Heroes 2 (2 romsets) — scène LED de `neogeo_combat`
- valeurs (13) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 64 décors
- aussi : specials (16 combattants)

**wh2j** — World Heroes 2 Jet — scène LED de `neogeo_combat`
- valeurs (14) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop, round
- internes (8) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _fight_cue, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 64 décors
- aussi : specials (18 combattants)

**whp** — World Heroes Perfect — scène LED de `neogeo_combat`
- valeurs (16) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, health, health_p2, time, score, score_p2, backdrop, power, power_p2, round
- internes (7) : _in_p1, _in_p2, _p1_dir, _p2_dir, _time_sub, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- `hd` : 32 décors
- aussi : specials (21 combattants)

**xmcota** — X-Men: Children of the Atom (17 romsets) — scène LED de `cps_combat`
- valeurs (12) : health, health_p2, time, power, power_level, power_p2, power_level_p2, score, score_p2, rounds, rounds_p2, backdrop
- internes (5) : _p1_chr, _p2_chr, _p1_ctl, _p2_ctl, _time_sub
- `derived` : p1_char, p2_char
- `hd` : 12 décors
- aussi : specials (15 combattants), activity, hyper

**xmvsf** — X-Men Vs. Street Fighter (23 romsets) — scène LED de `cps_combat`
- valeurs (9) : time, power, power_level, power_p2, power_level_p2, score, score_p2, rounds, rounds_p2
- internes (10) : _p1_chr, _p2_chr, _p1_ctl, _p2_ctl, _p1_hp1, _p1_hp2, _p1_chr2, _p2_hp1, _p2_hp2, _p2_chr2
- `derived` : p1_char, p2_char
- `tag` : health, health_p2
- `hd` : 8 décors
- aussi : specials (21 combattants), activity

### MetalSlugScene (`dmd/hd_mslug.py`)

**mslug** — Metal Slug
- valeurs (33) : score, score_p2, lives, lives_p2, bombs, bombs_p2, grenades_out, grenades_out_p2, ammo, ammo_p2, weapon, weapon_p2, vehicle, vehicle_hp, vehicle_ammo, vehicle_p2, vehicle_hp_p2, vehicle_ammo_p2, prisoners, prisoners_p2, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, mission, p1_input, p2_input, end_state, boss_alive
- internes (1) : _hps
- `derived` : boss_name, boss_dead, mission_done
- `hd` : boss_slots=["_hps"], boss_life={"1": 2200, "2": 3900, "3": 2000, "4": 1200}, boss_min=2000
- parties réelles dans `tests/captures` : 5

**mslug2** — Metal Slug 2 (2 romsets)
- valeurs (38) : score, score_p2, lives, lives_p2, bombs, bombs_p2, grenades_out, grenades_out_p2, ammo, ammo_p2, weapon, weapon_p2, p1_chr, p2_chr, form, form_p2, prisoners, prisoners_p2, vehicle, vehicle_kind, vehicle_hp, vehicle_ammo, vehicle_p2, vehicle_kind_p2, vehicle_hp_p2, vehicle_ammo_p2, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, mission, p1_input, p2_input, end_ptr
- internes (3) : _veh1, _veh2, _hps
- `derived` : p1_name, p2_name, boss_name, mission_done
- `hd` : boss_slots=["_hps"], boss_life={"1": 3000}, boss_min=2000
- parties réelles dans `tests/captures` : 4

**mslug3** — Metal Slug 3 (5 romsets)
- valeurs (35) : score, score_p2, lives, lives_p2, bombs, bombs_p2, ammo, ammo_p2, weapon, weapon_p2, prisoners, prisoners_p2, p1_chr, p2_chr, form, form_p2, vehicle_kind, vehicle, vehicle_kind_p2, vehicle_p2, time, mission, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, p1_input, p2_input, grenades_out, grenades_out_p2, end_text, end_count
- internes (7) : _p1b, _eq1, _eq2, _eq3, _st1, _vf1, _hps
- `derived` : p1_name, p2_name, boss_name, mission_done
- `hd` : boss_slots=["_hps"], boss_life={"1": 5000, "4": 4000}, boss_min=2000, per_game={"mslug3b6": {"mission_count": true, "weapon_codes": {"17":…
- parties réelles dans `tests/captures` : 2

**mslug4** — Metal Slug 4 (3 romsets)
- valeurs (32) : score, score_p2, lives, lives_p2, bombs, bombs_p2, grenades_out, grenades_out_p2, ammo, ammo_p2, weapon, weapon_p2, p1_chr, p2_chr, prisoners, prisoners_p2, vehicle, vehicle_hp, vehicle_hp_p2, stage_state, boss_flag, time, mission, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, p1_input, p2_input
- internes (16) : _hps, _ew0, _ew1, _ew2, _ew3, _ew4, _ew5, _ew6, _ew7, _ex0, _ex1, _ex2, _ex3, _p1b, _p1k, _veh
- `derived` : p1_name, p2_name, boss_name, mission_done
- `hd` : boss_slots=["_hps", "_boss1", "_boss2", "_boss3", "_boss4", "_boss5", …, boss_life={"1": 850}, boss_min=600, minor_idle=20, boss_flag="boss_flag"
- parties réelles dans `tests/captures` : 7

**mslug5** — Metal Slug 5 (5 romsets)
- valeurs (36) : score, score_p2, lives, lives_p2, bombs, bombs_p2, grenades_out, grenades_out_p2, ammo, ammo_p2, weapon, weapon_p2, prisoners, p1_chr, p2_chr, prisoners_p2, vehicle_kind, vehicle, vehicle_kind_p2, vehicle_p2, vehicle_hp, vehicle_hp_p2, boss_down, fade, section, time, mission, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, p1_input, p2_input
- internes (2) : _hps, _p1b
- `derived` : p1_name, p2_name, boss_name, boss_dead, mission_done
- `hd` : boss_slots=["_hps"], boss_min=2000, minor_min=256
- parties réelles dans `tests/captures` : 1

**mslugx** — Metal Slug X
- valeurs (39) : score, score_p2, lives, lives_p2, bombs, bombs_p2, grenades_out, grenades_out_p2, ammo, ammo_p2, weapon, weapon_p2, prisoners, prisoners_p2, p1_chr, p2_chr, form, form_p2, vehicle_kind, vehicle, vehicle_hp, vehicle_ammo, vehicle_kind_p2, vehicle_p2, vehicle_hp_p2, vehicle_ammo_p2, time, mission, boss_down, end_ptr, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, p1_input, p2_input
- internes (3) : _veh1, _veh2, _hps
- `derived` : p1_name, p2_name, boss_name, boss_dead, mission_done
- `hd` : boss_slots=["_hps"], boss_life={"1": 5000}, boss_min=2000
- parties réelles dans `tests/captures` : 1

### AeroFighters2Scene (`dmd/hd_games3.py`)

**sonicwi2** — Aero Fighters 2
- valeurs (17) : score, score_p2, p1_input, p2_input, lives, lives_p2, bombs, bombs_p2, power, power_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (17) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[1, 2, 3]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[3]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `bombs_p2 down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[1, 2, 3]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[3]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### AeroFighters3Scene (`dmd/hd_games3.py`)

**sonicwi3** — Aero Fighters 3
- valeurs (18) : score, score_p2, p1_input, p2_input, lives, lives_p2, bombs, bombs_p2, power, power_p2, plane, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : pilot_name, plane_name
- annonces de la dalle LED (17) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[1, 2, 3, 4]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[4]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `bombs_p2 down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[1, 2, 3, 4]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[4]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### AirGalletScene (`dmd/hd_cave.py`)

**agallet** — Air Gallet (12 romsets) — scène LED de `cave_shoot`
- valeurs (9) : credits, lives, lives_p2, bombs, bombs_p2, power, power_p2, score, score_p2
- aussi : activity

### AkaiKatanaScene (`dmd/hd_cave.py`)

**akatana** — Akai Katana — scène LED de `cave_shoot`
- valeurs (2) : score, score_p2
- aussi : activity

### AlphaMission2Scene (`dmd/hd_games5.py`)

**alpham2** — Alpha Mission II (2 romsets)
- valeurs (17) : score, score_p2, p1_input, p2_input, lives, lives_p2, power, power_p2, gold, gold_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (12) :
  - `power up` → **ARMOR** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### AndroDunosScene (`dmd/hd_games10.py`)

**androdun** — Andro Dunos
- valeurs (21) : score, score_p2, p1_input, p2_input, lives, shot, bomb_pw, missile, unit, lives_p2, shot_p2, bomb_pw_p2, missile_p2, unit_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (15) :
  - `shot up to=[1, 2, 3, 4, 5, 6, 7]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `shot up to=[7]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `shot_p2 up to=[1, 2, 3, 4, 5, 6, 7]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `shot_p2 up to=[7]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### BakatonoScene (`dmd/hd_games11.py`)

**bakatono** — Bakatonosama Mahjong Manyuuki
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (1) : _move_time

### BangBangBustersScene (`dmd/hd_games10.py`)

**b2b** — Bang Bang Busters
- valeurs (14) : score, score_p2, p1_input, p2_input, lives, lives_p2, boss, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### BangBeadScene (`dmd/hd_games9.py`)

**bangbead** — Bang Bead
- valeurs (17) : score, score_p2, p1_input, p2_input, time_tens, time_units, power, stock, power_p2, stock_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### Baseball2020Scene (`dmd/hd_games8.py`)

**2020bb** — 2020 Super Baseball (3 romsets)
- valeurs (10) : time, time_min, outs_total, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### BaseballScene (`dmd/hd_games3.py`)

**bstars2** — Baseball Stars 2
- valeurs (14) : runs, runs_p2, balls, strikes, outs, pow, pow_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### BaseballStarsProScene (`dmd/hd_games8.py`)

**bstars** — Baseball Stars Professional (2 romsets)
- valeurs (13) : balls, strikes, outs, inning, time, time_min, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### BlazingStarScene (`dmd/hd_games.py`)

**blazstar** — Blazing Star
- valeurs (16) : score, score_p2, p1_input, p2_input, lives, lives_p2, power, power_p2, round, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (16) :
  - `power up to=[1, 2, 3]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[3]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `power_p2 up to=[1, 2, 3]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[3]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `round up step=1` → **ROUND {round}** (priorité 4, 1600 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### BluesJourneyScene (`dmd/hd_games6.py`)

**bjourney** — Blue's Journey (2 romsets)
- valeurs (16) : score, score_p2, time, lives, lives_p2, energy, energy_p2, money, money_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### BurningFightScene (`dmd/hd_games5.py`)

**burningf** — Burning Fight (5 romsets)
- valeurs (14) : score, score_p2, time, lives, lives_p2, energy, energy_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### CapcomWorldScene (`dmd/hd_games14.py`)

**cworld2j** — Adventure Quiz Capcom World 2 (3 romsets)
- valeurs (5) : credits, lives, lives_p2, score, score_p2
- aussi : activity

### CaptainTomadayScene (`dmd/hd_games10.py`)

**ctomaday** — Captain Tomaday
- valeurs (19) : score, score_p2, score_units, score_units_p2, p1_input, p2_input, lives, power, power_l, lives_p2, power_p2, power_l_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (15) :
  - `power up to=[1, 2, 3, 4, 5]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[5]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `power_p2 up to=[1, 2, 3, 4, 5]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[5]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### CarrierAirWingScene (`dmd/hd_games13.py`)

**cawing** — Carrier Air Wing (8 romsets)
- valeurs (10) : health, health_p2, time, credits, ammo, money, weapon, power, score, score_p2
- `derived` : weapon_name
- aussi : activity
- annonces de la dalle LED (4) :
  - `power up to=[1, 2, 3, 4, 5]` → **POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[5]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `weapon any` → **{weapon_name}** (priorité 2, 1200 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"weapon_name"}]}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### ChoukouScene (`dmd/hd_games16.py`)

**choko** — Janpai Puzzle Choukou (2 romsets)
- valeurs (1) : credits
- internes (1) : _time
- aussi : activity

### Counter1941Scene (`dmd/hd_games13.py`)

**1941** — 1941: Counter Attack (4 romsets)
- valeurs (7) : health, health_p2, credits, weapon, weapon_time, score, score_p2
- `derived` : weapon_name
- aussi : activity
- annonces de la dalle LED (2) :
  - `weapon any` → **{weapon_name}** (priorité 2, 1200 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"weapon_name"}]}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### CrossedSwordsScene (`dmd/hd_games10.py`)

**crsword** — Crossed Swords
- valeurs (17) : score, score_p2, p1_input, p2_input, energy, magic, gold, energy_p2, magic_p2, gold_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### CyberLipScene (`dmd/hd_games5.py`)

**cyberlip** — Cyber-Lip
- valeurs (23) : score, score_p2, time, time_min, lives, lives_p2, ammo_auto, ammo_fire, ammo_wide, ammo_bazooka, ammo_grenade, ammo_auto_p2, ammo_fire_p2, ammo_wide_p2, ammo_bazooka_p2, ammo_grenade_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### DaiFukkatsuScene (`dmd/hd_cave.py`)

**ddpdfk** — DoDonPachi Dai-Fukkatsu Ver 1.5 (2 romsets) — scène LED de `cave_shoot`
- valeurs (7) : credits, lives, lives_p2, bombs, bombs_p2, score, score_p2
- aussi : activity, per_game

**ddpsdoj** — DoDonPachi SaiDaiOuJou (2 romsets) — scène LED de `cave_shoot`
- valeurs (2) : score, score_p2
- aussi : activity

**dfkbl** — DoDonPachi Dai-Fukkatsu Black Label — scène LED de `cave_shoot`
- valeurs (7) : credits, lives, lives_p2, bombs, bombs_p2, score, score_p2
- aussi : activity

### DaiOuJouScene (`dmd/hd_cave.py`)

**ddp3** — DoDonPachi Dai-Ou-Jou (9 romsets) — scène LED de `cave_shoot`
- valeurs (15) : credits, lives, lives_p2, bombs, bombs_p2, bombs_max, bombs_max_p2, power, power_p2, combo, combo_p2, hits, stage, score, score_p2
- aussi : activity, per_game

### DeathsmilesScene (`dmd/hd_cave.py`)

**deathsml** — Deathsmiles — scène LED de `cave_shoot`
- valeurs (5) : credits, energy, energy_p2, score, score_p2
- aussi : activity

**dsmbl** — Deathsmiles MegaBlack Label — scène LED de `cave_shoot`
- valeurs (5) : credits, energy, energy_p2, score, score_p2
- aussi : activity

### DeluxeQuizScene (`dmd/hd_games11.py`)

**marukodq** — Chibi Maruko-chan Deluxe Quiz
- valeurs (14) : score, score_p2, p1_input, p2_input, lives, lives_p2, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### DiggerManScene (`dmd/hd_games10.py`)

**diggerma** — Digger Man
- valeurs (17) : score, score_p2, p1_input, p2_input, lives, energy, bombs, lives_p2, energy_p2, bombs_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### DimahooScene (`dmd/hd_games13.py`)

**dimahoo** — Dimahoo (4 romsets)
- valeurs (5) : lives, lives_p2, bombs, score, score_p2
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : activity, coins
- annonces de la dalle LED (5) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### DoDonPachi2Scene (`dmd/hd_cave.py`)

**ddp2** — DoDonPachi II - Bee Storm (18 romsets) — scène LED de `cave_shoot`
- valeurs (12) : credits, lives, lives_p2, stage, bombs_p2, bombs, power, power_p2, combo, combo_p2, score, score_p2
- aussi : activity, per_game

### DoDonPachiScene (`dmd/hd_cave.py`)

**ddonpach** — DoDonPachi (3 romsets) — scène LED de `cave_shoot`
- valeurs (19) : lives, lives_p2, bombs, bombs_p2, bombs_max, bombs_max_p2, power, power_p2, combo, combo_p2, ship, ship_p2, credits, hits, hits_p2, stage, loop, distance, phase
- internes (11) : _score10, _cont, _score10_p2, _cont_p2, _state, _players, _out_p1, _out_p2, _stage_task, _boss_hp, _boss_hp_b
- `derived` : p1_ship, p2_ship, boss, boss_name, warning, boss_hp
- `tag` : score, score_p2, p1_mode, p2_mode
- aussi : per_game

### DodgeBallScene (`dmd/hd_games4.py`)

**sdodgeb** — Super Dodge Ball (2 romsets)
- valeurs (24) : score, score_p2, time, hp1, hp2, hp3, hp1_p2, hp2_p2, hp3_p2, power, power_p2, char1, char2, char3, char1_p2, char2_p2, char3_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : name1, name1_p2, name2, name2_p2, name3, name3_p2

### DonPachiScene (`dmd/hd_cave.py`)

**donpachi** — DonPachi (5 romsets) — scène LED de `cave_shoot`
- valeurs (14) : credits, lives, lives_p2, bombs, bombs_p2, power, power_p2, combo, combo_p2, hits, stage, loop, score, score_p2
- aussi : activity

### EcoFightersScene (`dmd/hd_games13.py`)

**ecofghtr** — Eco Fighters (7 romsets)
- valeurs (7) : credits, lives, lives_p2, power, weapon, score, score_p2
- `derived` : weapon_name
- aussi : activity, per_game
- annonces de la dalle LED (7) :
  - `power up to=[1, 2, 3, 4, 5]` → **POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[5]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `weapon any` → **{weapon_name}** (priorité 2, 1200 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"weapon_name"}]}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### EightManScene (`dmd/hd_games10.py`)

**eightman** — Eight Man
- valeurs (19) : score, score_p2, p1_input, p2_input, time, lives, energy, bombs, power8, lives_p2, energy_p2, bombs_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### EspRadeScene (`dmd/hd_cave.py`)

**esprade** — ESP Ra.De. - A.D.2018 Tokyo (3 romsets) — scène LED de `cave_shoot`
- valeurs (11) : credits, lives, lives_p2, bombs, bombs_p2, power, power_p2, multiplier, stage, score, score_p2
- aussi : activity

### EspgaludaScene (`dmd/hd_cave.py`)

**espgal** — Espgaluda (2 romsets) — scène LED de `cave_shoot`
- valeurs (10) : credits, lives, lives_p2, bombs_p2, power, power_p2, stones, stones_p2, score, score_p2
- aussi : activity

**espgal2** — Espgaluda II (3 romsets) — scène LED de `cave_shoot`
- valeurs (7) : credits, lives, lives_p2, bombs, bombs_p2, score, score_p2
- aussi : activity, per_game

### FeveronScene (`dmd/hd_cave.py`)

**feversos** — Fever SOS (2 romsets) — scène LED de `cave_shoot`
- valeurs (12) : credits, lives, lives_p2, bombs, round, bombs_p2, power, power_p2, ship, ship_p2, mode, score_p2
- internes (5) : _score_s1, _score_s2, _score_s3, _score_s4, _score_s5
- `derived` : p1_ship, p2_ship
- `tag` : score
- aussi : activity

### FinalRomanceScene (`dmd/hd_games11.py`)

**froman2b** — Idol Mahjong Final Romance 2
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### FlipShotScene (`dmd/hd_games9.py`)

**flipshot** — Battle Flip Shot
- valeurs (24) : score, score_p2, p1_input, p2_input, time, target1, target1_p2, target2, target2_p2, target3, target3_p2, target4, target4_p2, target5, target5_p2, target6, target6_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### FootballFrenzyScene (`dmd/hd_games8.py`)

**fbfrenzy** — Football Frenzy
- valeurs (12) : score, score_p2, time_min, time_sec, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, time

### ForgottenWorldsScene (`dmd/hd_games13.py`)

**forgottn** — Forgotten Worlds (10 romsets)
- valeurs (6) : health, health_p2, zenny, weapon, score, score_p2
- `derived` : weapon_name
- aussi : activity
- annonces de la dalle LED (2) :
  - `weapon any` → **{weapon_name}** (priorité 2, 1200 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"weapon_name"}]}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### FrogFeastScene (`dmd/hd_games16.py`)

**cps1frog** — Frog Feast

### GanryuScene (`dmd/hd_games7.py`)

**ganryu** — Ganryu
- valeurs (18) : score, score_p2, time, lives, lives_p2, energy, energy_p2, ammo, ammo_p2, weapon, weapon_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (1) : _turn

### GhostPilotsScene (`dmd/hd_games5.py`)

**gpilots** — Ghost Pilots (3 romsets)
- valeurs (18) : score, score_p2, p1_input, p2_input, lives, lives_p2, bombs, bombs_p2, stars, stars_p2, power, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (15) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 2…` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[28]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `bombs_p2 down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### GhostlopScene (`dmd/hd_games9.py`)

**ghostlop** — Ghostlop
- valeurs (12) : score, score_p2, p1_input, p2_input, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### GigaWingScene (`dmd/hd_games13.py`)

**gigawing** — Giga Wing (7 romsets)
- valeurs (9) : lives, lives_p2, bombs, credits, power, score, score_p2, bombs_p2, power_p2
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : activity
- annonces de la dalle LED (7) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[1, 2, 3]` → **POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[3]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### Goal3Scene (`dmd/hd_games8.py`)

**goalx3** — Goal! Goal! Goal!
- valeurs (9) : goals, goals_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (2) : _time_min, _time_sec
- `derived` : time

### GulunpaScene (`dmd/hd_games16.py`)

**gulunpa** — Gulun.Pa!
- valeurs (2) : score, score_p2
- aussi : activity

### GururinScene (`dmd/hd_games9.py`)

**gururin** — Gururin
- valeurs (24) : score, score_p2, p1_input, p2_input, level, cur_l, cur_l_p2, cur_c, cur_c_p2, cur_r, cur_r_p2, next_l, next_l_p2, next_c, next_c_p2, next_r, next_r_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### GuwangeScene (`dmd/hd_cave.py`)

**guwange** — Guwange (2 romsets) — scène LED de `cave_shoot`
- valeurs (14) : credits, bombs, bombs_p2, power, power_p2, combo, combo_p2, energy, energy_p2, char, char_p2, lives, score, score_p2
- `derived` : p1_char, p2_char
- aussi : activity, per_game

### HotdogStormScene (`dmd/hd_cave.py`)

**hotdogst** — Hotdog Storm - The First Supersonics — scène LED de `cave_shoot`
- valeurs (9) : credits, lives, lives_p2, bombs, bombs_p2, power, power_p2, score, score_p2
- aussi : activity

### IbaraScene (`dmd/hd_cave.py`)

**ibara** — Ibara (2 romsets) — scène LED de `cave_shoot`
- valeurs (7) : credits, lives, lives_p2, bombs, bombs_p2, score, score_p2
- aussi : activity, per_game

**ibarablk** — Ibara Kuro Black Label (2 romsets) — scène LED de `cave_shoot`
- valeurs (6) : credits, lives, lives_p2, bombs_p2, score, score_p2
- aussi : activity, per_game

### IroncladScene (`dmd/hd_games10.py`)

**ironclad** — Choutetsu Brikin'ger (2 romsets)
- valeurs (19) : score, score_p2, p1_input, p2_input, energy, power, level, l_arm, r_arm, energy_p2, power_p2, level_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (10) :
  - `power up to=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[12]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `power_p2 up to=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[12]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `level up step=1` → **LEVEL {level}** (priorité 4, 1600 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### IrritatingMazeScene (`dmd/hd_games10.py`)

**irrmaze** — The Irritating Maze
- valeurs (11) : time_sec, time_tenths, lives, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, time

### JanshinScene (`dmd/hd_games11.py`)

**janshin** — Janshin Densetsu
- valeurs (12) : time, hp, mp, weapon, shield, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### JockeyGPScene (`dmd/hd_games9.py`)

**jockeygp** — Jockey Grand Prix (2 romsets)
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### JyangokushiScene (`dmd/hd_games16.py`)

**jyangoku** — Jyangokushi: Haoh no Saihai

### KetsuiScene (`dmd/hd_cave.py`)

**ket** — Ketsui: Kizuna Jigoku Tachi (16 romsets) — scène LED de `cave_shoot`
- valeurs (10) : credits, lives, lives_p2, bombs, bombs_p2, power, power_p2, combo, combo_p2, score_p2
- internes (2) : _score_hi, _score_lo
- `tag` : score
- aussi : activity

### LastHopeScene (`dmd/hd_games10.py`)

**lasthope** — Last Hope
- valeurs (11) : score, score_p2, p1_input, p2_input, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (5) :
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### LastResortScene (`dmd/hd_games3.py`)

**lresort** — Last Resort
- valeurs (17) : score, score_p2, p1_input, p2_input, lives, lives_p2, power, power_p2, speed, speed_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (17) :
  - `power up to=[1, 2, 3, 4]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[4]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `speed up step=1 to=[1, 2, 3, 4, 5]` → **SPEED UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `power_p2 up to=[1, 2, 3, 4]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[4]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `speed_p2 up step=1 to=[1, 2, 3, 4, 5]` → **SPEED UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### LeagueBowlingScene (`dmd/hd_games4.py`)

**lbowling** — League Bowling
- valeurs (11) : score, score_p2, time, time_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### Loop1944Scene (`dmd/hd_games13.py`)

**1944** — 1944: The Loop Master (5 romsets)
- valeurs (12) : health, health_p2, credits, bombs, power, score, score_p2, fighters, gold, fighters_p2, gold_p2, warning
- aussi : activity
- annonces de la dalle LED (4) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[1, 2, 3]` → **POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[3]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### MagicalDrop2Scene (`dmd/hd_games6.py`)

**magdrop2** — Magical Drop II
- valeurs (14) : score, score_p2, p1_input, p2_input, level, quota, quota_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### MagicalDropScene (`dmd/hd_games2.py`)

**magdrop3** — Magical Drop III
- valeurs (17) : score, score_p2, p1_input, p2_input, card, card_p2, cpu_p2, quota, quota_p2, level, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : card_name, card_name_p2

### MagicalPumpkinScene (`dmd/hd_games16.py`)

**mpumpkin** — Magical Pumpkin: Puroland de Daibouken

### MagicianLordScene (`dmd/hd_games4.py`)

**maglord** — Magician Lord (2 romsets)
- valeurs (16) : score, score_p2, lives, lives_p2, energy, energy_p2, power, power_p2, form, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (1) : _turn
- `derived` : form_name

### MahjongKyoScene (`dmd/hd_games11.py`)

**mahretsu** — Mahjong Kyo Retsuden
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (1) : _move_time

### MarineKunScene (`dmd/hd_games16.py`)

**ganbare** — Ganbare! Marine Kun

### MarsMatrixScene (`dmd/hd_games13.py`)

**mmatrix** — Mars Matrix: Hyper Solid Shooting (5 romsets)
- valeurs (6) : credits, lives, lives_p2, power, score, score_p2
- aussi : activity
- annonces de la dalle LED (6) :
  - `power up to=[1, 2, 3, 4, 5, 6, 7]` → **POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[7]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### MazingerScene (`dmd/hd_cave.py`)

**mazinger** — Mazinger Z (2 romsets) — scène LED de `cave_shoot`
- valeurs (9) : credits, bombs, bombs_p2, energy, energy_p2, power, power_p2, score, score_p2
- aussi : activity

### MercsScene (`dmd/hd_mercs.py`)

**mercs** — Mercs (5 romsets)
- valeurs (14) : health, health_p2, health_top, health_top_p2, time, mission, bombs, bombs_p2, weapon, weapon_p2, weapon_level, weapon_level_p2, score, score_p2
- internes (1) : _hps
- `derived` : p1_weapon, p2_weapon
- `hd` : boss_parts={"1": 1, "2": 3, "3": 3}
- aussi : activity, coins
- annonces de la dalle LED (9) :
  - `mission up step=1` → **MISSION COMPLETE** (priorité 6, 1400 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `mission up step=1` → **MISSION {mission}** (priorité 5.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `bombs down step=1` → **MEGA CRASH** (priorité 3, 1400 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `bombs_p2 down step=1` → **2P MEGA CRASH** (priorité 3, 1400 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `weapon any` → **{p1_weapon}** (priorité 2, 1300 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"p1_weapon"}]}`
  - `weapon_p2 any` → **2P {p2_weapon}** (priorité 2, 1300 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"p2_weapon"}]}`
  - `weapon_level up step=1` → **POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `weapon_level_p2 up step=1` → **2P POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
- parties réelles dans `tests/captures` : 1

### MinasanScene (`dmd/hd_games11.py`)

**minasan** — Minasan no Okagesamadesu!
- valeurs (8) : steps, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (1) : _move_time

### MoneyPuzzleScene (`dmd/hd_games6.py`)

**miexchng** — Money Puzzle Exchanger
- valeurs (14) : score, score_p2, p1_input, p2_input, level, max_chain, chain, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### MuchiPorkScene (`dmd/hd_cave.py`)

**mmpork** — Muchi Muchi Pork! — scène LED de `cave_shoot`
- valeurs (7) : credits, lives, lives_p2, bombs, bombs_p2, score, score_p2
- aussi : activity

### MushiTamaScene (`dmd/hd_cave.py`)

**mushitam** — Puzzle! Mushihime-Tama (2 romsets) — scène LED de `cave_reflexion`
- valeurs (5) : credits, lives, lives_p2, score, score_p2
- aussi : activity

### MushihimeScene (`dmd/hd_cave.py`)

**futari15** — Mushihime-Sama Futari Ver 1.5 (3 romsets) — scène LED de `cave_shoot`
- valeurs (7) : credits, lives, lives_p2, bombs, bombs_p2, score, score_p2
- aussi : activity, per_game

**futaribl** — Mushihime-Sama Futari Black Label - Another Ver (2 romsets) — scène LED de `cave_shoot`
- valeurs (7) : credits, lives, lives_p2, bombs, bombs_p2, score, score_p2
- aussi : activity, per_game

**matsuri15** — Mushihime-Sama Matsuri Ver 1.5 — scène LED de `cave_shoot`
- valeurs (2) : score, score_p2
- aussi : activity

**mushisam** — Mushihime-Sama (3 romsets) — scène LED de `cave_shoot`
- valeurs (7) : credits, lives, lives_p2, bombs, bombs_p2, score, score_p2
- aussi : activity, per_game

### MutationNationScene (`dmd/hd_games6.py`)

**mutnat** — Mutation Nation
- valeurs (15) : score, score_p2, time, energy, energy_p2, bombs, bombs_p2, special, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### NamScene (`dmd/hd_games5.py`)

**nam1975** — NAM-1975
- valeurs (17) : score, score_p2, lives, lives_p2, ammo, ammo_p2, grenades, grenades_p2, weapon, weapon_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### NanairoScene (`dmd/hd_games16.py`)

**qndream** — Quiz Nanairo Dreams: Nijiirochou no Kiseki
- valeurs (3) : credits, score, score_p2
- aussi : activity

### NeoBombermanScene (`dmd/hd_games4.py`)

**neobombe** — Neo Bomberman
- valeurs (19) : score, score_p2, lives, lives_p2, fire, fire_p2, speed, speed_p2, bombs, bombs_p2, world, stage, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### NeoCup98Scene (`dmd/hd_games8.py`)

**neocup98** — Neo-Geo Cup '98
- valeurs (9) : goals, goals_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### NeoDriftScene (`dmd/hd_games4.py`)

**neodrift** — Neo Drift Out - New Technology
- valeurs (8) : time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### NeoMrDoScene (`dmd/hd_games7.py`)

**neomrdo** — Neo Mr. Do!
- valeurs (12) : score, score_p2, lives, lives_p2, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### NightmareScene (`dmd/hd_games11.py`)

**nitd** — Nightmare in the Dark (2 romsets)
- valeurs (17) : score, score_p2, p1_input, p2_input, time, lives, fire, speed, lives_p2, boss, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### NinjaCombatScene (`dmd/hd_games6.py`)

**ncombat** — Ninja Combat (2 romsets)
- valeurs (18) : score, score_p2, time, time_p2, lives, lives_p2, energy, energy_p2, power, power_p2, char, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### NinjaCommandoScene (`dmd/hd_games6.py`)

**ncommand** — Ninja Commando
- valeurs (17) : score, score_p2, ninja, ninja_p2, p1_input, p2_input, time, time_p2, energy, energy_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : char_name, char_name_p2

### OverTopScene (`dmd/hd_games9.py`)

**overtop** — Over Top
- valeurs (13) : time, rank, speed, lap_min, lap_sec, lap_cs, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### PanelScene_3wonders

**3wonders** — Three Wonders (7 romsets)
- valeurs (6) : credits, lives, lives_p2, score, score_p2, weapon
- internes (1) : _time
- aussi : activity

### PanelScene_armwar

**armwar** — Armored Warriors (10 romsets)
- valeurs (6) : health, health_p2, lives, lives_p2, score, score_p2
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : activity, coins

### PanelScene_avsp

**avsp** — Alien vs. Predator (6 romsets)
- valeurs (8) : health, health_p2, lives, lives_p2, power, power_p2, score, score_p2
- internes (3) : _time, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : activity, coins

### PanelScene_batcir

**batcir** — Battle Circuit (4 romsets)
- valeurs (8) : health, health_p2, credits, lives, lives_p2, score, score_p2, money
- internes (1) : _time
- aussi : activity

### PanelScene_captcomm

**captcomm** — Captain Commando (22 romsets)
- valeurs (7) : health, health_p2, credits, lives, lives_p2, score, score_p2
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : activity

### PanelScene_ddsom

**ddsom** — Dungeons & Dragons: Shadow over Mystara (18 romsets)
- valeurs (4) : health, health_p2, score, score_p2
- internes (1) : _time
- aussi : activity

### PanelScene_ddtod

**ddtod** — Dungeons & Dragons: Tower of Doom (14 romsets)
- valeurs (5) : health, health_p2, score, score_p2, daggers
- internes (1) : _time
- aussi : activity, per_game

### PanelScene_dino

**dino** — Cadillacs and Dinosaurs (36 romsets)
- valeurs (6) : health, health_p2, lives, lives_p2, score, score_p2
- internes (3) : _time, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : activity, coins

### PanelScene_dynwar

**dynwar** — Dynasty Wars (4 romsets)
- valeurs (5) : health, health_p2, score, score_p2, level
- aussi : activity

### PanelScene_ffight

**ffex2u** — Final Fight EX (3 romsets)
- valeurs (2) : score, score_p2
- aussi : activity

**ffight** — Final Fight (24 romsets)
- valeurs (8) : health, health_p2, time, credits, lives, lives_p2, score, score_p2
- aussi : activity

**ffightaec2** — Final Fight: Anniversary Edition (2 romsets)
- valeurs (2) : score, score_p2
- aussi : activity

### PanelScene_gaia

**gaia** — Gaia Crusaders — scène LED de `cave_action`
- valeurs (8) : health, health_p2, time, credits, lives, lives_p2, stage, score
- aussi : activity

### PanelScene_ghouls

**ghouls** — Ghouls'n Ghosts (11 romsets)
- valeurs (7) : lives, lives_p2, score, score_p2, armor, armor_kind, weapon
- internes (1) : _time
- `derived` : _one
- aussi : activity, coins

### PanelScene_knights

**knights** — Knights of the Round (14 romsets)
- valeurs (7) : health, health_p2, lives, lives_p2, score, score_p2, level
- internes (1) : _time
- aussi : activity, coins

### PanelScene_kod

**kod** — The King of Dragons (16 romsets)
- valeurs (9) : health, health_p2, lives, lives_p2, score, score_p2, level, weapon, shield
- internes (1) : _time
- aussi : activity, coins

### PanelScene_mpang

**mpang** — Mighty! Pang (6 romsets)
- valeurs (5) : time, lives, lives_p2, score, score_p2
- aussi : activity, coins

### PanelScene_msword

**msword** — Magic Sword: Heroic Fantasy (4 romsets)
- valeurs (9) : time, power, power_p2, score, score_p2, health, keys, floor, partner
- `derived` : _one
- aussi : activity

### PanelScene_mtwins

**mtwins** — Mega Twins (3 romsets)
- valeurs (7) : health, health_p2, credits, lives, lives_p2, score, score_p2
- internes (1) : _time
- `derived` : _one
- aussi : activity

### PanelScene_nemo

**nemo** — Nemo (4 romsets)
- valeurs (5) : lives, lives_p2, score, score_p2, bombs
- internes (1) : _time
- aussi : activity, coins

### PanelScene_pang3

**pang3** — Pang! 3 (11 romsets)
- valeurs (4) : lives, lives_p2, score, score_p2
- internes (1) : _time
- aussi : activity, coins

### PanelScene_punisher

**punisher** — The Punisher (15 romsets)
- valeurs (7) : health, health_p2, lives, lives_p2, bombs, score, score_p2
- internes (1) : _time
- aussi : activity, coins

### PanelScene_sailormn

**sailormn** — Bishoujo Senshi Sailor Moon (34 romsets) — scène LED de `cave_action`
- valeurs (7) : health, health_p2, time, credits, lives, lives_p2, score
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : activity

### PanelScene_strider

**strider** — Strider (8 romsets)
- valeurs (4) : score, score_p2, lives, pods
- internes (1) : _time
- `derived` : _one
- aussi : activity, coins

### PanelScene_theroes

**theroes** — Thunder Heroes (2 romsets) — scène LED de `cave_action`
- valeurs (7) : health, health_p2, time, credits, lives, lives_p2, stage
- internes (2) : _p1_chr, _p2_chr
- `derived` : p1_char, p2_char
- aussi : activity

### PanelScene_willow

**willow** — Willow (5 romsets)
- valeurs (6) : credits, score, score_p2, lives, health, hero
- internes (1) : _time
- `derived` : _one
- aussi : activity

### PanelScene_wof

**wof** — Warriors of Fate (40 romsets)
- valeurs (7) : health, health_p2, credits, lives, lives_p2, score, score_p2
- internes (1) : _time
- aussi : activity

**wofch** — Tenchi wo Kurau II: Sekiheki no Tatakai (3 romsets)
- valeurs (5) : score, score_p2, health, credits, lives
- internes (1) : _time
- aussi : activity

### PanicBomberScene (`dmd/hd_games7.py`)

**panicbom** — Panic Bomber
- valeurs (15) : score, score_p2, p1_input, p2_input, power, power_p2, level, level_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### PinkSweetsScene (`dmd/hd_cave.py`)

**pinkswts** — Pink Sweets: Ibara Sorekara (5 romsets) — scène LED de `cave_shoot`
- valeurs (5) : credits, lives, lives_p2, score, score_p2
- aussi : activity, per_game

### PleasureGoalScene (`dmd/hd_games8.py`)

**pgoal** — Pleasure Goal
- valeurs (9) : goals, goals_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (2) : _clock, _clock_vs
- `tag` : clock

### PnickiesScene (`dmd/hd_games16.py`)

**pnickj** — Pnickies (2 romsets)
- valeurs (2) : score, score_p2
- aussi : activity

### PochiNyaaScene (`dmd/hd_games9.py`)

**pnyaa** — Pochi and Nyaa (2 romsets)
- valeurs (11) : score, score_p2, p1_input, p2_input, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### PokonyanScene (`dmd/hd_games16.py`)

**pokonyan** — Pokonyan! Balloon

### PopBounceScene (`dmd/hd_games7.py`)

**popbounc** — Pop 'n Bounce
- valeurs (13) : score, score_p2, p1_input, p2_input, lives, lives_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### PowerSpikes2Scene (`dmd/hd_games8.py`)

**pspikes2** — Power Spikes II
- valeurs (15) : p1_input, p2_input, time_min, time_sec, power, power_p2, energy, energy_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### PrehistoricIsle2Scene (`dmd/hd_games5.py`)

**preisle2** — Prehistoric Isle 2
- valeurs (19) : score, score_p2, p1_input, p2_input, lives, lives_p2, bombs, bombs_p2, power, power_p2, stars, stars_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (14) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `power up` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `bombs_p2 down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### ProgearScene (`dmd/hd_games13.py`)

**progear** — Progear (8 romsets)
- valeurs (8) : credits, lives, lives_p2, bombs, power, fighter, score, score_p2
- aussi : activity
- annonces de la dalle LED (7) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[1, 2, 3, 4, 5, 6, 7, 8]` → **POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[8]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### PulstarScene (`dmd/hd_games2.py`)

**pulstar** — Pulstar
- valeurs (17) : score, score_p2, p1_input, p2_input, lives, lives_p2, stage, charge, speed, pods, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : stage_name
- annonces de la dalle LED (13) :
  - `speed up step=1 to=[1, 2, 3, 4, 5, 6, 7]` → **SPEED UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `stage up step=1` → **STAGE {stage}** (priorité 4, 1600 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### PuzzLoopScene (`dmd/hd_games14.py`)

**pzloop2** — Puzz Loop 2 (5 romsets)
- valeurs (3) : credits, score, score_p2
- `derived` : _one
- aussi : activity

### PuzzleBobble1Scene (`dmd/hd_games6.py`)

**pbobblen** — Puzzle Bobble (2 romsets)
- valeurs (21) : score, score_p2, p1_input, p2_input, round, vs_mode, wins, wins_p2, bubble, bubble_next, bubble_p2, bubble_next_p2, angle, angle_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### PuzzleBobble2Scene (`dmd/hd_games6.py`)

**pbobbl2n** — Puzzle Bobble 2
- valeurs (25) : score, score_p2, p1_input, p2_input, time, time_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, round, path, mode, wins, wins_p2, rounds_done, bubble, bubble_next, bubble_p2, bubble_next_p2, angle, angle_p2
- `derived` : vs_mode
- parties réelles dans `tests/captures` : 1

### PuzzleDePonRScene (`dmd/hd_games7.py`)

**puzzldpr** — Puzzle De Pon! R!
- valeurs (17) : score, score_p2, p1_input, p2_input, time, level, bubble, bubble_next, bubble_p2, bubble_next_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### PuzzleDePonScene (`dmd/hd_games6.py`)

**puzzledp** — Puzzle De Pon!
- valeurs (17) : score, score_p2, p1_input, p2_input, time, level, bubble, bubble_next, bubble_p2, bubble_next_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### PuzzledScene (`dmd/hd_games9.py`)

**joyjoy** — Puzzled
- valeurs (15) : score, score_p2, p1_input, p2_input, balloons, balloons_p2, next, next_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### QuizDaisousaScene (`dmd/hd_games11.py`)

**quizdais** — Quiz Daisousa Sen (2 romsets)
- valeurs (13) : score, score_p2, p1_input, p2_input, lives, lives_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### QuizDragonsScene (`dmd/hd_games14.py`)

**qad** — Quiz & Dragons: Capcom Quiz Game (2 romsets)
- valeurs (4) : lives, lives_p2, score, score_p2
- aussi : activity, coins, per_game

### QuizKOFScene (`dmd/hd_games11.py`)

**quizkof** — Quiz King of Fighters (2 romsets)
- valeurs (13) : score, score_p2, p1_input, p2_input, lives, lives_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### QuizMeitanteiScene (`dmd/hd_games11.py`)

**quizdai2** — Quiz Meitantei Neo & Geo
- valeurs (14) : score, score_p2, p1_input, p2_input, lives, lives_p2, gold, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### RidingHeroScene (`dmd/hd_games4.py`)

**ridhero** — Riding Hero (2 romsets)
- valeurs (11) : time, turbo, rank, speed, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : rank_name

### RoboArmyScene (`dmd/hd_games5.py`)

**roboarmy** — Robo Army (2 romsets)
- valeurs (15) : score, score_p2, lives, lives_p2, energy, energy_p2, bombs, bombs_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SecondSquadScene (`dmd/hd_squad.py`)

**shocktr2** — Shock Troopers 2nd Squad (2 romsets)
- valeurs (26) : score, score_p2, p1_input, p2_input, energy, energy_p2, soldier, soldier_p2, time, lives, lives_p2, grenades, grenades_p2, power, power_p2, ammo, ammo_p2, weapon, weapon_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (9) : _hps, _boss, _wait, _clear, _stage, _mission, _area, _ride, _ride_p2
- `derived` : char_name, char_name_p2, power_lv, power_lv_p2
- annonces de la dalle LED (5) :
  - `power up to=[12]` → **LEVEL 2** (priorité 3, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[24]` → **LEVEL 3** (priorité 3, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[4, 8, 16, 20, 28, 32, 36]` → **POWER UP** (priorité 2, 1000 ms) si `{"var":"p1_mode","eq":1}`
  - `_boss up` → **ALERT** (priorité 5, 2400 ms) si `{"any":[{"var":"p1_mode","eq":1},{"var":"p2_mode","eq":1}]}`
  - `_clear up` → **STAGE CLEAR** (priorité 4, 2000 ms) si `{"any":[{"var":"p1_mode","eq":1},{"var":"p2_mode","eq":1}]}`

### Sengoku2Scene (`dmd/hd_games6.py`)

**sengoku2** — Sengoku 2
- valeurs (15) : score, score_p2, lives, lives_p2, energy, energy_p2, weapon, weapon_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SengokuScene (`dmd/hd_games6.py`)

**sengoku** — Sengoku (2 romsets)
- valeurs (15) : score, score_p2, lives, lives_p2, energy, energy_p2, weapon, weapon_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

**sengoku3** — Sengoku 3 (2 romsets)
- valeurs (22) : score, score_p2, p1_input, p2_input, health, health_p2, magic, magic_p2, stars, stars_p2, weapon, weapon_p2, fighter, fighter_p2, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : fighter_name, fighter_name_p2, weapon_name

### ShockTroopersScene (`dmd/hd_games.py`)

**shocktro** — Shock Troopers (2 romsets)
- valeurs (22) : score, score_p2, p1_input, p2_input, energy, energy_p2, weapon, ammo, member, weapon_p2, ammo_p2, member_p2, time, stage_id, area, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (14) : _tm1, _tm2, _tm3, _bombs1, _bombs2, _bombs3, _tm1_p2, _tm2_p2, _tm3_p2, _bombs1_p2, _bombs2_p2, _bombs3_p2, _route_screen, _hps
- `derived` : weapon_name, special, special_name, char_name, bombs, special_p2, special_name_p2, char_name_p2, bombs_p2, weapon_name_p2

### ShogiScene (`dmd/hd_games11.py`)

**moshougi** — Shougi no Tatsujin
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SoccerBrawlScene (`dmd/hd_games8.py`)

**socbrawl** — Soccer Brawl (2 romsets)
- valeurs (13) : goals, goals_p2, energy, energy_p2, time_min, time_sec, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SpfScene (`dmd/hd_spf.py`)

**spf2t** — Super Puzzle Fighter II Turbo (10 romsets)
- valeurs (21) : credits, score, score_p2, well1, well2, pair1, pair2, x1, y1, rot1, x2, y2, rot2, wins1, wins2, chain1, chain2, atk1, atk2, pcs1, pcs2
- internes (8) : _major, _minor, _sub, _vs, _p2_in, _rounds_vs, _p1_chr, _p2_chr
- `derived` : p1_char, p2_char, p1_mode, p2_mode, _one
- annonces de la dalle LED (4) :
  - `chain1 up` → **{chain1} CHAIN!** (priorité 1, 1300 ms) si `{"var":"chain1","gt":1}`
  - `chain2 up` → **{chain2} CHAIN!** (priorité 1, 1300 ms) si `{"var":"chain2","gt":1}`
  - `wins1 up` → **{p1_char} WINS** (priorité 2, 1800 ms)
  - `wins2 up` → **{p2_char} WINS** (priorité 2, 1800 ms)

### SpinMasterScene (`dmd/hd_games7.py`)

**spinmast** — Spin Master
- valeurs (16) : score, score_p2, lives, lives_p2, energy, energy_p2, bombs, bombs_p2, weapon, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SportsClubScene (`dmd/hd_games14.py`)

**csclub** — Capcom Sports Club (7 romsets)
- valeurs (3) : credits, score, score_p2
- internes (1) : _time
- aussi : activity

### StakesWinner2Scene (`dmd/hd_games9.py`)

**stakwin2** — Stakes Winner 2
- valeurs (12) : power, power_p2, speed, stamina, burst, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### StakesWinnerScene (`dmd/hd_games9.py`)

**stakwin** — Stakes Winner
- valeurs (10) : speed, stamina, strength, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### StreetHoopScene (`dmd/hd_games4.py`)

**strhoop** — Street Hoop
- valeurs (14) : points, points_p2, time_min, time_sec, half, super, super_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### StrikersScene (`dmd/hd_games4.py`)

**s1945p** — Strikers 1945 Plus
- valeurs (23) : score, score_p2, p1_input, p2_input, lives, lives_p2, bombs, bombs_p2, power, power_p2, super, super_p2, charge, charge_p2, plane, plane_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- internes (4) : _mission, _title, _bhp, _bmark
- `derived` : plane_name
- annonces de la dalle LED (19) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[1, 2, 3, 4]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `power up to=[4]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `super down step=1` → **SUPER SHOT** (priorité 3, 1400 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `bombs_p2 down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[1, 2, 3, 4]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p2_mode","eq":1}`
  - `power_p2 up to=[4]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `super_p2 down step=1` → **SUPER SHOT** (priorité 3, 1400 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### SuperBubblePopScene (`dmd/hd_games7.py`)

**sbp** — Super Bubble Pop
- valeurs (11) : score, score_p2, p1_input, p2_input, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SuperSidekicks2Scene (`dmd/hd_games7.py`)

**ssideki2** — Super Sidekicks 2
- valeurs (9) : goals, goals_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SuperSidekicks3Scene (`dmd/hd_games2.py`)

**ssideki3** — Super Sidekicks 3 - The Next Glory
- valeurs (9) : goals, goals_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SuperSidekicksScene (`dmd/hd_games7.py`)

**ssideki** — Super Sidekicks
- valeurs (11) : goals, goals_p2, time_min, time_sec, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### SuperSpyScene (`dmd/hd_games11.py`)

**superspy** — The Super Spy
- valeurs (17) : score, score_p2, p1_input, p2_input, energy, exp, weapon, ammo, ammo_mg, knife, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### TecmoSoccerScene (`dmd/hd_games8.py`)

**twsoc96** — Tecmo World Soccer '96
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### ThrashRallyScene (`dmd/hd_games4.py`)

**trally** — Thrash Rally
- valeurs (9) : time, speed, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### TonosamaScene (`dmd/hd_games16.py`)

**qtono2j** — Quiz Tonosama no Yabou 2: Zenkoku-ban
- valeurs (4) : lives, lives_p2, score, score_p2
- aussi : activity, coins

### TopHunterScene (`dmd/hd_games3.py`)

**tophuntr** — Top Hunter - Roddy & Cathy (2 romsets)
- valeurs (18) : score, score_p2, p1_input, p2_input, lives, lives_p2, health, health_p2, power, power_p2, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### TopPlayersGolfScene (`dmd/hd_games8.py`)

**tpgolf** — Top Player's Golf
- valeurs (10) : strokes, holes, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### TurfMastersScene (`dmd/hd_games.py`)

**turfmast** — Neo Turf Masters
- valeurs (14) : club, power, wind, wind_dir, strokes, strokes_p2, golfer, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : club_name, club_yards, golfer_name

### TwinkleScene (`dmd/hd_twinkle.py`)

**twinspri** — Twinkle Star Sprites
- valeurs (32) : score, score_p2, p1_input, p2_input, pos_x, pos_y, pos_x_p2, pos_y_p2, lives, lives_p2, bombs, bombs_p2, power, power_p2, attack, attack_p2, char, char_p2, hits, hits_p2, wins, wins_p2, stage, perfect, perfect_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- `derived` : name, name_p2
- `hd` : fields=[[8, 144], [160, 296]], field_y=[16, 224]
- parties réelles dans `tests/captures` : 1

### UNSquadronScene (`dmd/hd_games13.py`)

**unsquad** — U.N. Squadron (3 romsets)
- valeurs (6) : credits, bombs, weapon, power, score, score_p2
- `derived` : weapon_name
- aussi : activity
- annonces de la dalle LED (2) :
  - `weapon any` → **{weapon_name}** (priorité 2, 1200 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"weapon_name"}]}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### Ultimate11Scene (`dmd/hd_games2.py`)

**ssideki4** — The Ultimate 11 - The SNK Football Championship
- valeurs (11) : goals, goals_p2, power, power_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### UoPokoScene (`dmd/hd_cave.py`)

**uopoko** — Puzzle Uo Poko (2 romsets) — scène LED de `cave_reflexion`
- valeurs (6) : credits, stage, bubble, bubble_p2, score, score_p2
- aussi : activity

### VarthScene (`dmd/hd_games13.py`)

**varth** — Varth: Operation Thunderstorm (8 romsets)
- valeurs (9) : credits, lives, lives_p2, bombs, power, weapon, pods, score, score_p2
- `derived` : weapon_name
- aussi : activity
- annonces de la dalle LED (8) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[1, 2, 3, 4, 5, 6, 7]` → **POWER UP** (priorité 2, 1100 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `power up to=[7]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `weapon any` → **{weapon_name}** (priorité 2, 1200 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"weapon_name"}]}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### ViewpointScene (`dmd/hd_games5.py`)

**viewpoin** — Viewpoint
- valeurs (15) : score, score_p2, p1_input, p2_input, lives, lives_p2, bomb_type, bomb_type_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- annonces de la dalle LED (13) :
  - `bomb_type down` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `bomb_type_p2 down` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1` → **x{lives_p2}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p2_mode","eq":1}`
  - `lives_p2 up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p2_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### War19XXScene (`dmd/hd_games13.py`)

**19xx** — 19XX: The War Against Destiny (10 romsets)
- valeurs (9) : credits, lives, lives_p2, bombs, weapon, plane, plane_p2, score, score_p2
- `derived` : weapon_name
- aussi : activity
- annonces de la dalle LED (6) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `weapon any` → **{weapon_name}** (priorité 2, 1200 ms) si `{"all":[{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}},{"has":"weapon_name"}]}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### WindjammersScene (`dmd/hd_games.py`)

**wjammers** — Windjammers
- valeurs (30) : set_points, set_points_p2, time, court, to_win, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, p1_x, p1_y, p2_x, p2_y, sets, sets_p2, score, score_p2, disc_x, disc_y, disc_h, disc_state, disc_last, p1_state, p2_state, p1_chr, p2_chr, bios_country
- `derived` : court_name, p1_name, p2_name, p1_nation, p2_nation
- parties réelles dans `tests/captures` : 5

### ZedBladeScene (`dmd/hd_games5.py`)

**zedblade** — Zed Blade
- valeurs (17) : score, score_p2, p1_input, p2_input, lives, bombs, shot_level, shot_type, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs, lives_p2, bombs_p2
- annonces de la dalle LED (11) :
  - `bombs down step=1` → **BOMB!** (priorité 3, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `shot_level up to=[1, 2, 3]` → **POWER UP** (priorité 2, 1100 ms) si `{"var":"p1_mode","eq":1}`
  - `shot_level up to=[3]` → **MAX POWER** (priorité 2.5, 1300 ms) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1` → **x{lives}** (priorité 5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives down step=1 to=[0]` → **LAST LIFE** (priorité 5.5, 2000 ms, délai du texte 0.45 s) si `{"var":"p1_mode","eq":1}`
  - `lives up step=1` → **1UP** (priorité 4, 1500 ms) si `{"var":"p1_mode","eq":1}`
  - `p1_mode any from=[0, 3] to=[1]` → **PLAYER 1** (priorité 1, 1200 ms)
  - `p2_mode any from=[0, 3] to=[1]` → **PLAYER 2** (priorité 1, 1200 ms)
  - `p1_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p2_mode","in":[1,2]}}`
  - `p2_mode any from=[1, 2] to=[0, 3]` → **GAME OVER** (priorité 9, 2600 ms) si `{"not":{"var":"p1_mode","in":[1,2]}}`
  - `credits up` → **CREDIT {credits}** (priorité 1.5, 1500 ms) si `{"not":{"all":[{"has":"p1_mode"},{"not":{"var":"p1_mode","in":[1,2]}},{"not":{"var":"p2_mode","in":[1,2]}}]}}`

### ZintrickScene (`dmd/hd_games10.py`)

**zintrckb** — Zintrick
- valeurs (18) : score, score_p2, p1_input, p2_input, time, energy, item, level, energy_p2, item_p2, level_p2, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### ZupapaScene (`dmd/hd_games7.py`)

**zupapa** — Zupapa!
- valeurs (12) : score, score_p2, lives, lives_p2, time, credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

### (générique)

**_generic** — Generic scene (all games without a dedicated file) — modèle, pas un jeu

**_idle** — Idle screen (no game running) — modèle, pas un jeu

**aburner2** — After Burner II (2 romsets)
- valeurs (3) : record, score, credits

**cave_action** — modèle, pas un jeu

**cave_reflexion** — modèle, pas un jeu

**cave_shoot** — modèle, pas un jeu
- annonces de la dalle LED (2) :
  - `boss up to=[1]` → **WARNING!** (priorité 6, 1300 ms)
  - `boss up to=[1]` → **{boss_name}** (priorité 5.9, 2200 ms) si `{"has":"boss_name"}`

**cps1demo** — Chaos Demo — scène LED de `cps_reflexion`

**cps_action** — modèle, pas un jeu

**cps_reflexion** — modèle, pas un jeu

**cps_shoot** — modèle, pas un jeu

**crusherm** — Crusher Makochan — scène LED de `cave_reflexion`
- valeurs (2) : score, score_p2
- aussi : activity

**korokoro** — Koro Koro Quest — scène LED de `cave_action`
- valeurs (2) : credits, round

**neogeo** (58 romsets)
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs
- aussi : per_game

**neogeo_reflexion** (36 romsets)
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

**neogeo_shoot** (22 romsets)
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

**neogeo_sport** (36 romsets)
- valeurs (7) : credits, p1_mode, p2_mode, bios_request, bios_mode, bios_timer, bios_mvs

**sonic** — Sonic The Hedgehog (2 romsets)
- valeurs (6) : score, rings, lives, zone, act, mode

**sonic2** — Sonic The Hedgehog 2 (2 romsets)
- valeurs (6) : score, rings, lives, zone, act, mode

## 2. Les scènes de l'écran HD

Pour chaque classe, les valeurs qu'elle lit par leur nom, celles dont elle guette le changement (`changed`), et chaque endroit où elle annonce quelque chose, avec les conditions qui l'entourent telles que le code les écrit. Une classe hérite des annonces de ses classes de base. Les réactions sans texte (explosions, secousses, mouvements du héros) ne sont pas listées ici, elles suivent les mêmes changements de valeurs.

### HDRenderer — `dmd/hd.py` lignes 100 à 1180

- valeurs lues : `_p1_lost`, `_p2_lost`, `beat`, `beat_p2`, `credits`, `health`, `health_p2`, `p1_mode`, `p2_mode`, `score`, `score_p2`, `select`, `time`

### CaveShooterScene — `dmd/hd_cave.py` lignes 432 à 1764

- hérite de : _CpsShooter, AeroFightersScene
- valeurs lues : `boss`, `boss_hp`, `boss_name`, `distance`, `loop`, `phase`, `ship`, `stage`
- changements guettés : `'bombs_max' + suf`, `'combo' + suf`, `'hits' + suf`, `'lives' + suf`, `'ship' + suf`, `boss`, `hname`, `loop`, `name`, `self.STAGE_KEY`
- annonces :
  - ligne 613, `update`, slam **f'{self.STAGE_WORD} {int(ch[1])}'** — si `ch and ch[1] > 0` ET `self.STAGE_KEY != 'round'`
  - ligne 661, `update`, slam **2ND LOOP** — si `ch and ch[1] > ch[0]`
  - ligne 686, `update`, popup **name** — si `ch and P['in'] and name`
  - ligne 952, `boss_arrives`, slam **WARNING** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 961, `_boss_banner`, slam **name** — si `self.boss is not None and self.boss['down'] is None`
  - ligne 1073, `score_events`, popup **f'+{int(gain)}'** — si `now - self.last_points > 0.35`
  - ligne 1095, `chain_kill`, popup **f'{h // 50 * 50} HIT !'** — si `h // 50 > (h - n) // 50 and h >= 50`
  - ligne 1150, `bomb`, popup **BOMB!** — sans condition dans cette fonction, voir qui l'appelle

### DoDonPachiScene — `dmd/hd_cave.py` lignes 1768 à 1782

- hérite de : CaveShooterScene
- jeux (1) : ddonpach

### DonPachiScene — `dmd/hd_cave.py` lignes 1785 à 1792

- hérite de : CaveShooterScene
- jeux (1) : donpachi

### DaiOuJouScene — `dmd/hd_cave.py` lignes 1795 à 1805

- hérite de : CaveShooterScene
- jeux (1) : ddp3

### DaiFukkatsuScene — `dmd/hd_cave.py` lignes 1808 à 1814

- hérite de : DaiOuJouScene
- jeux (3) : ddpdfk, ddpsdoj, dfkbl

### DoDonPachi2Scene — `dmd/hd_cave.py` lignes 1817 à 1825

- hérite de : DoDonPachiScene
- jeux (1) : ddp2

### EspRadeScene — `dmd/hd_cave.py` lignes 1850 à 1873

- hérite de : CaveShooterScene
- jeux (1) : esprade
- valeurs lues : `multiplier`

### GuwangeScene — `dmd/hd_cave.py` lignes 1907 à 1945

- hérite de : CaveShooterScene
- jeux (1) : guwange
- valeurs lues : `energy`, `p1_char`

### FeveronScene — `dmd/hd_cave.py` lignes 1949 à 1962

- hérite de : CaveShooterScene
- jeux (1) : feversos

### KetsuiScene — `dmd/hd_cave.py` lignes 1966 à 1999

- hérite de : CaveShooterScene
- jeux (1) : ket

### EspgaludaScene — `dmd/hd_cave.py` lignes 2019 à 2079

- hérite de : CaveShooterScene
- jeux (2) : espgal, espgal2
- valeurs lues : `stones`
- changements guettés : `'stones' + suf`

### MushihimeScene — `dmd/hd_cave.py` lignes 2114 à 2151

- hérite de : CaveShooterScene
- jeux (4) : futari15, futaribl, matsuri15, mushisam

### IbaraScene — `dmd/hd_cave.py` lignes 2155 à 2166

- hérite de : CaveShooterScene
- jeux (2) : ibara, ibarablk

### PinkSweetsScene — `dmd/hd_cave.py` lignes 2169 à 2174

- hérite de : IbaraScene
- jeux (1) : pinkswts

### MuchiPorkScene — `dmd/hd_cave.py` lignes 2196 à 2209

- hérite de : CaveShooterScene
- jeux (1) : mmpork

### DeathsmilesScene — `dmd/hd_cave.py` lignes 2250 à 2297

- hérite de : CaveShooterScene
- jeux (2) : deathsml, dsmbl
- changements guettés : `'energy' + suf`

### AkaiKatanaScene — `dmd/hd_cave.py` lignes 2300 à 2334

- hérite de : CaveShooterScene
- jeux (1) : akatana

### HotdogStormScene — `dmd/hd_cave.py` lignes 2338 à 2348

- hérite de : CaveShooterScene
- jeux (1) : hotdogst

### MazingerScene — `dmd/hd_cave.py` lignes 2351 à 2371

- hérite de : HotdogStormScene
- jeux (1) : mazinger
- valeurs lues : `energy`
- changements guettés : `'energy' + suf`

### AirGalletScene — `dmd/hd_cave.py` lignes 2374 à 2380

- hérite de : HotdogStormScene
- jeux (1) : agallet

### UoPokoScene — `dmd/hd_cave.py` lignes 2384 à 2395

- hérite de : PuzzleBobble2Scene
- jeux (1) : uopoko
- changements guettés : `stage`
- annonces :
  - ligne 2393, `update`, slam **f'STAGE {int(ch[1])}'** — si `ch and ch[1] > 0`

### MushiTamaScene — `dmd/hd_cave.py` lignes 2398 à 2400

- hérite de : UoPokoScene
- jeux (1) : mushitam

### CoinDoors — `dmd/hd_coin.py` lignes 58 à 442

- valeurs lues : `coin_side`, `credits`, `p1_mode`, `p2_mode`

### CreditsBar — `dmd/hd_credits.py` lignes 23 à 132

- annonces :
  - ligne 83, `_ding`, fx.text **credits_word(n)** — si `n and (not quiet) and (self.box is not None)`

### FightFX — `dmd/hd_fight.py` lignes 127 à 1361

- jeux (97) : 3countb, aodk, aof, aof2, aof3, breakers, breakrev, cave_combat, cps_combat, cybots, doubledr, dragonsh, dstlk, fatfursp, fatfury1, fatfury2, fatfury3, fightfev, galaxyfg, garou, gowcaizr, hsf2, jojo, jojoba, kabukikl, karnovr, kf2k3pcb, kizuna, kof2000, kof2001, kof2002, kof2003, kof94, kof95, kof96, kof97, kof98, kof99, kotm, kotm2, lastblad, lastbld2, legendos, matrim, mbombrd, megaman, megaman2, metmqstr, msh, mshvsf, mvsc, neogeo_combat, ninjamas, nwarr, plegends, pwrinst2, ragnagrd, rbff1, rbff2, rbffspec, redearth, ringdest, rotd, samsh5sp, samsho, samsho2, samsho3, samsho4, samsho5, savagere, sf2, sf2ce, sf2hf, sfa, sfa2, sfa3, sfiii, sfiii2, sfiii3, sfz2al, sfzch, sgemf, slammast, ssf2, ssf2t, svc, svcpcb, vhunt2, vsav, vsav2, wakuwak7, wh1, wh2, wh2j, whp, xmcota, xmvsf
- valeurs lues : `_fight_cue`, `_fight_state`, `_p1_lost`, `_p2_lost`, `_screen`, `_time`, `_time_sub`, `backdrop`, `health`, `health_p2`, `p1_mode`, `p2_mode`, `round`, `rounds`, `rounds_p2`, `select`, `stage`, `time`
- annonces :
  - ligne 692, `update`, banner **TIME UP** — si `t is not None and self.prev_time is not None and (t <= 0 < self.prev_time <= 2) and counting and (now - self.ko_t > 2.0) and ((h1 or 0) > 0) and ((h2…`
  - ligne 712, `update`, banner **DRAW GAME** — si `self.judge is not None and now >= self.judge and (h1 is not None) and (h2 is not None)` ET `not (h1 != h2)`
  - ligne 893, `_hit`, fx.text **FIRST ATTACK** — si `not self.first and now - self.fight_t < 60 and (not in_dm)`
  - ligne 897, `_hit`, light **blow** — si `total >= BLOW_SUPER and b[3] < 2`
  - ligne 923, `_hit`, fx.text **f'-{pct}%'** — si `total >= BLOW_SHOW and new > 0`
  - ligne 937, `_hit`, fx.text **f'{c[0]} HITS'** — si `not (in_dm)` ET `c[0] >= 2`
  - ligne 943, `_hit`, light **ko** — si `new <= 0`
  - ligne 951, `_hit`, banner **DOUBLE K.O.** — si `new <= 0` ET `other is not None and other <= 0`
  - ligne 1014, `_match_won`, light **win** — si `self.humans.get(winner)`
  - ligne 1068, `_celebrate`, banner **PERFECT !** — si `perfect`
  - ligne 1074, `_light`, lights **name** — si `lights is not None and (not self.idle)`
  - ligne 1243, `_slam_sub`, slam **screen** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1330, `_banners`, slam **screen** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1332, `_banners`, side_slam **screen** — si `self.ko_side is not None`
  - ligne 1334, `_banners`, side_slam **screen** — si `self.win_side is not None`
  - ligne 1338, `_banners`, slam **screen** — si `self.banner is not None`

### GameScene — `dmd/hd_games.py` lignes 70 à 590

- valeurs lues : `credits`, `max`, `p1_mode`, `p2_mode`
- changements guettés : `'lives' if side == 'p1' else 'lives_p2'`
- annonces :
  - ligne 336, `power_pop`, popup **'POWER MAX' if top else 'POWER UP'** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 340, `power_pop`, popup **f'LV {lit}/{total}'** — si `not (total is not None and 0 < total <= 12)` ET `total is not None and (not top)`
  - ligne 342, `power_pop`, popup **f'LV {lit}'** — si `not (total is not None and 0 < total <= 12)` ET `not (total is not None and (not top))` ET `lit > 0`
  - ligne 420, `slam`, banner **text** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 544, `render`, slam **GAME OVER** — si `m == 3 and self.modes.get(side) in (1, 2)`

### BlazingStarScene — `dmd/hd_games.py` lignes 628 à 974

- hérite de : GameScene
- jeux (1) : blazstar
- valeurs lues : `round`, `score`, `score_p2`
- changements guettés : `'lives' + suf`, `'power' + suf`, `name`, `round`
- annonces :
  - ligne 750, `update`, popup **-1 LIFE** — si `(last or (ch and ch[1] < ch[0])) and alive` ET `not last`
  - ligne 755, `update`, popup **1UP !** — si `not ((last or (ch and ch[1] < ch[0])) and alive)` ET `self.one_up(vals, side)`
  - ligne 760, `update`, power_pop **x** — si `ch and ch[1] > ch[0] and alive`
  - ligne 773, `update`, slam **f'ROUND {int(ch[1])}'** — si `ch`
  - ligne 882, `score_kill`, popup **f'+{int(gain)}'** — si `big or now - self.last_points > 0.25`

### PuzzleBobbleScene — `dmd/hd_games.py` lignes 1137 à 1351

- hérite de : GameScene
- valeurs lues : `p1_mode`, `p2_mode`, `round`, `total_wins`, `total_wins_p2`, `vs_mode`, `wins`, `wins_p2`
- changements guettés : `'bubble' + suf`, `name`, `round`
- annonces :
  - ligne 1211, `update`, slam **f'ROUND {int(ch[1])}'** — si `ch and (not vs)`
  - ligne 1224, `won`, slam **tr('J1 GAGNE !', 'P1 WINS!') if side == 'p1' else tr('J2 GAGNE !', 'P…** — sans condition dans cette fonction, voir qui l'appelle

### WindjammersScene — `dmd/hd_games.py` lignes 1449 à 2098

- hérite de : GameScene
- jeux (1) : wjammers
- valeurs lues : `bios_country`, `court`, `disc_h`, `disc_last`, `disc_state`, `disc_x`, `disc_y`, `p1_chr`, `p2_chr`, `sets`, `sets_p2`, `time`, `to_win`
- changements guettés : `name`
- annonces :
  - ligne 1752, `set_won`, slam **text** — si `sets >= 2`
  - ligne 1975, `draw_hud`, popup **f"+{f['pts']}"** — si `k >= 1.0 and f['zone'] is None`
  - ligne 1987, `draw_hud`, popup **f"+{f['pts']}"** — si `k >= 1.0`

### Machines — `dmd/hd_games.py` lignes 2197 à 2309

- valeurs lues : `_hps`
- annonces :
  - ligne 2263, `machines`, slam **BOSS DESTROYED** — si `not (gone)` ET `v <= 0` ET `B['shown']` ET `B['boss']` (et 2 autres conditions au-dessus)
  - ligne 2265, `machines`, popup **DESTROYED!** — si `not (gone)` ET `v <= 0` ET `B['shown']` ET `not (B['boss'])` (et 2 autres conditions au-dessus)
  - ligne 2280, `machines`, slam **WARNING** — si `is_boss`

### ShockTroopersScene — `dmd/hd_games.py` lignes 2312 à 2712

- hérite de : Machines, GameScene
- jeux (1) : shocktro
- valeurs lues : `_route_screen`, `area`, `stage_id`, `time`
- changements guettés : `'ammo' + suf`, `'bombs' + suf`, `'energy' + suf`, `'weapon' + suf`
- annonces :
  - ligne 2557, `update`, popup **DOWN!** — si `ch and ch[1] != ch[0]` ET `ch[1] >= 128 > ch[0]`
  - ligne 2571, `update`, slam **f'STAGE {st[0]}'** — si `anyone and runs and (st is not None) and (not self.in_stage or st != self.staged) and (vals.get('_route_screen') is not None)`

### TurfMastersScene — `dmd/hd_games.py` lignes 2727 à 2858

- hérite de : GameScene
- jeux (1) : turfmast
- valeurs lues : `club`, `golfer`, `power`, `strokes`, `wind`, `wind_dir`
- changements guettés : `club`, `strokes`, `strokes_p2`

### ZintrickScene — `dmd/hd_games10.py` lignes 155 à 237

- hérite de : GameScene
- jeux (1) : zintrckb
- valeurs lues : `time`
- changements guettés : `'item' + suf`, `'level' + suf`
- annonces :
  - ligne 193, `update`, popup **ITEM!** — si `ch and ch[1] < ch[0]`
  - ligne 197, `update`, popup **f'LEVEL {int(ch[1])}'** — si `ch and ch[1] > ch[0]`

### DiggerManScene — `dmd/hd_games10.py` lignes 264 à 459

- hérite de : GameScene
- jeux (1) : diggerma
- changements guettés : `bombs`, `energy`, `score`
- annonces :
  - ligne 365, `update`, popup **f'+{int(ch[1] - ch[0])}'** — si `ch and 0 < ch[1] - ch[0] <= 5000`
  - ligne 388, `update`, popup **OUCH!** — si `ch and ch[1] < ch[0] - 20`

### IrritatingMazeScene — `dmd/hd_games10.py` lignes 463 à 557

- hérite de : GameScene
- jeux (1) : irrmaze
- valeurs lues : `lives`, `time_sec`, `time_tenths`
- changements guettés : `lives`
- annonces :
  - ligne 504, `update`, slam **GOAL!** — si `self.u >= self.total`
  - ligne 518, `update`, popup **BZZT!** — si `ch and ch[1] < ch[0]`

### AndroDunosScene — `dmd/hd_games10.py` lignes 630 à 695

- hérite de : SideShooterScene
- jeux (1) : androdun
- changements guettés : `name`
- annonces :
  - ligne 662, `update`, popup **f'{lab} MAX' if v >= mx else f'{lab} UP'** — si `len(ups) == 1 and self.ships['p1']['in'] and (not self.starting('p1'))`
  - ligne 664, `update`, popup **f'LV {int(v)}/{mx}'** — si `len(ups) == 1 and self.ships['p1']['in'] and (not self.starting('p1'))` ET `v < mx`

### IroncladScene — `dmd/hd_games10.py` lignes 698 à 763

- hérite de : SideShooterScene
- jeux (1) : ironclad
- changements guettés : `energy`, `level`
- annonces :
  - ligne 727, `update`, popup **LEVEL UP** — si `ch and ch[1] > ch[0] and self.ships['p1']['in']`

### LastHopeScene — `dmd/hd_games10.py` lignes 766 à 804

- hérite de : SideShooterScene
- jeux (1) : lasthope
- valeurs lues : `score`

### CaptainTomadayScene — `dmd/hd_games10.py` lignes 837 à 901

- hérite de : AeroFightersScene
- jeux (1) : ctomaday

### BangBangBustersScene — `dmd/hd_games10.py` lignes 955 à 1134

- hérite de : GameScene
- jeux (1) : b2b
- valeurs lues : `boss`
- changements guettés : `boss`, `lives`, `score`
- annonces :
  - ligne 1039, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`

### CrossedSwordsScene — `dmd/hd_games10.py` lignes 1183 à 1287

- hérite de : GameScene
- jeux (1) : crsword
- changements guettés : `energy`, `gold`, `magic`
- annonces :
  - ligne 1235, `values`, popup **HIT!** — si `ch and ch[1] < ch[0]`
  - ligne 1248, `values`, popup **f'+{int(ch[1] - ch[0])} GOLD'** — si `ch and ch[1] > ch[0] and (not self.starting('p1'))`

### EightManScene — `dmd/hd_games10.py` lignes 1291 à 1350

- hérite de : BrawlerScene
- jeux (1) : eightman
- valeurs lues : `power8`, `time`

### NightmareScene — `dmd/hd_games11.py` lignes 75 à 123

- hérite de : BangBangBustersScene
- jeux (1) : nitd
- valeurs lues : `time`

### SuperSpyScene — `dmd/hd_games11.py` lignes 162 à 262

- hérite de : GameScene
- jeux (1) : superspy
- valeurs lues : `energy`, `exp`, `score`, `weapon`
- changements guettés : `ammo`, `ammo_mg`, `energy`

### QuizScene — `dmd/hd_games11.py` lignes 285 à 401

- hérite de : GameScene
- valeurs lues : `lives`, `score`
- changements guettés : `lives`, `score`

### QuizKOFScene — `dmd/hd_games11.py` lignes 404 à 408

- hérite de : QuizScene
- jeux (1) : quizkof

### QuizDaisousaScene — `dmd/hd_games11.py` lignes 411 à 415

- hérite de : QuizScene
- jeux (1) : quizdais

### QuizMeitanteiScene — `dmd/hd_games11.py` lignes 418 à 422

- hérite de : QuizScene
- jeux (1) : quizdai2

### DeluxeQuizScene — `dmd/hd_games11.py` lignes 425 à 430

- hérite de : QuizScene
- jeux (1) : marukodq

### MahjongScene — `dmd/hd_games11.py` lignes 470 à 599

- hérite de : GameScene
- valeurs lues : `time`
- annonces :
  - ligne 558, `win`, slam **self.rng.choice(('RON!', 'TSUMO!'))** — sans condition dans cette fonction, voir qui l'appelle

### MahjongKyoScene — `dmd/hd_games11.py` lignes 602 à 606

- hérite de : MahjongScene
- jeux (1) : mahretsu

### JanshinScene — `dmd/hd_games11.py` lignes 609 à 637

- hérite de : MahjongScene
- jeux (1) : janshin
- changements guettés : `hp`
- annonces :
  - ligne 623, `update`, popup **f'HP -{int(ch[0] - ch[1])}'** — si `ch and ch[1] < ch[0]`

### BakatonoScene — `dmd/hd_games11.py` lignes 640 à 644

- hérite de : MahjongScene
- jeux (1) : bakatono

### FinalRomanceScene — `dmd/hd_games11.py` lignes 647 à 651

- hérite de : MahjongScene
- jeux (1) : froman2b

### MinasanScene — `dmd/hd_games11.py` lignes 654 à 693

- hérite de : MahjongScene
- jeux (1) : minasan
- changements guettés : `steps`
- annonces :
  - ligne 672, `update`, popup **f'{int(ch[1])} STEPS'** — si `ch and ch[1] > 0`

### ShogiScene — `dmd/hd_games11.py` lignes 711 à 828

- hérite de : GameScene
- jeux (1) : moshougi
- annonces :
  - ligne 780, `update`, slam **CHECKMATE** — si `tgt is not None and tgt[0] == 'K'`

### _CpsShooter — `dmd/hd_games13.py` lignes 289 à 426

- valeurs lues : `_state`, `p2_mode`
- changements guettés : `'bombs' + suf`, `'health' + suf`, `bombs_p2`, `health_p2`, `lives_p2`, `score_p2`, `self.WEAPON + suf`
- annonces :
  - ligne 344, `energy_hits`, popup **DANGER!** — si `ch[1] <= 25 < ch[0]`
  - ligne 357, `weapon_popups`, popup **name** — si `ch and name and self.ships[side]['in']`
  - ligne 372, `sweep`, popup **BOMB!** — sans condition dans cette fonction, voir qui l'appelle

### WarPlanesScene — `dmd/hd_games13.py` lignes 430 à 501

- hérite de : _CpsShooter, AeroFightersScene
- annonces :
  - ligne 484, `bomb`, popup **LIGHTNING!** — sans condition dans cette fonction, voir qui l'appelle

### Loop1944Scene — `dmd/hd_games13.py` lignes 520 à 712

- hérite de : WarPlanesScene
- jeux (1) : 1944
- valeurs lues : `health`
- changements guettés : `'bombs' + suf`, `'fighters' + suf`, `'gold' + suf`, `warning`
- annonces :
  - ligne 555, `update`, popup **WINGMEN!** — si `ch` ET `ch[1] > ch[0] and P['in']`
  - ligne 576, `bomb`, popup **MISSILES!** — sans condition dans cette fonction, voir qui l'appelle

### War19XXScene — `dmd/hd_games13.py` lignes 715 à 765

- hérite de : WarPlanesScene
- jeux (1) : 19xx
- valeurs lues : `bombs`, `lives`, `plane`
- changements guettés : `plane`
- annonces :
  - ligne 745, `update`, popup **self.PLANES.get(int(ch[1]), '')** — si `ch and self.ships['p1']['in']`

### Counter1941Scene — `dmd/hd_games13.py` lignes 768 à 796

- hérite de : WarPlanesScene
- jeux (1) : 1941
- valeurs lues : `health`, `weapon_time`

### VarthScene — `dmd/hd_games13.py` lignes 799 à 857

- hérite de : _CpsShooter, AeroFightersScene
- jeux (1) : varth
- valeurs lues : `bombs`, `lives`, `pods`

### GigaWingScene — `dmd/hd_games13.py` lignes 860 à 908

- hérite de : _CpsShooter, AeroFightersScene
- jeux (1) : gigawing
- valeurs lues : `bombs`, `bombs_p2`, `lives`, `lives_p2`, `p1_char`
- changements guettés : `bombs`

### MarsMatrixScene — `dmd/hd_games13.py` lignes 911 à 954

- hérite de : _CpsShooter, AeroFightersScene
- jeux (1) : mmatrix
- valeurs lues : `lives`, `power`

### DimahooScene — `dmd/hd_games13.py` lignes 958 à 1026

- hérite de : _CpsShooter, AeroFightersScene
- jeux (1) : dimahoo
- valeurs lues : `bombs`, `lives`, `p1_char`
- annonces :
  - ligne 998, `bomb`, popup **MAGIC!** — sans condition dans cette fonction, voir qui l'appelle

### UNSquadronScene — `dmd/hd_games13.py` lignes 1038 à 1090

- hérite de : _SideCps
- jeux (1) : unsquad
- valeurs lues : `bombs`
- changements guettés : `bombs`

### CarrierAirWingScene — `dmd/hd_games13.py` lignes 1093 à 1130

- hérite de : _SideCps
- jeux (1) : cawing
- valeurs lues : `ammo`, `health`, `money`, `power`

### ForgottenWorldsScene — `dmd/hd_games13.py` lignes 1133 à 1197

- hérite de : _SideCps
- jeux (1) : forgottn
- valeurs lues : `health`, `zenny`
- changements guettés : `zenny`
- annonces :
  - ligne 1164, `update`, popup **f'+{int(ch[1] - ch[0])} ZENNY'** — si `ch and ch[1] > ch[0] and self.ships['p1']['in']`
  - ligne 1167, `update`, popup **tr('BOUTIQUE', 'SHOP') + f' -{int(ch[0] - ch[1])} ZENNY'** — si `not (ch and ch[1] > ch[0] and self.ships['p1']['in'])` ET `ch and ch[1] < ch[0]`

### ProgearScene — `dmd/hd_games13.py` lignes 1200 à 1237

- hérite de : _SideCps
- jeux (1) : progear
- valeurs lues : `bombs`, `fighter`, `lives`, `power`

### EcoFightersScene — `dmd/hd_games13.py` lignes 1240 à 1287

- hérite de : _SideCps
- jeux (1) : ecofghtr
- valeurs lues : `lives`, `power`

### PuzzleFighterScene — `dmd/hd_games14.py` lignes 168 à 303

- hérite de : GameScene
- valeurs lues : `score`, `score_p2`
- changements guettés : `score`

### PuzzLoopScene — `dmd/hd_games14.py` lignes 310 à 464

- hérite de : GameScene
- jeux (1) : pzloop2
- valeurs lues : `score`
- changements guettés : `score`
- annonces :
  - ligne 396, `update`, popup **str(int(ch[1] - ch[0])) if ch[1] - ch[0] < 100000 else 'BURST'** — si `ch and ch[1] > ch[0] and self.chain`

### SportsClubScene — `dmd/hd_games14.py` lignes 468 à 484

- hérite de : SoccerScene
- jeux (1) : csclub
- valeurs lues : `time`

### QuizDragonsScene — `dmd/hd_games14.py` lignes 488 à 496

- hérite de : QuizScene
- jeux (1) : qad

### CapcomWorldScene — `dmd/hd_games14.py` lignes 499 à 505

- hérite de : QuizScene
- jeux (1) : cworld2j

### TonosamaScene — `dmd/hd_games16.py` lignes 25 à 32

- hérite de : QuizScene
- jeux (1) : qtono2j

### NanairoScene — `dmd/hd_games16.py` lignes 35 à 41

- hérite de : QuizScene
- jeux (1) : qndream

### JyangokushiScene — `dmd/hd_games16.py` lignes 45 à 49

- hérite de : MahjongScene
- jeux (1) : jyangoku

### ChoukouScene — `dmd/hd_games16.py` lignes 52 à 187

- hérite de : MahjongScene
- jeux (1) : choko
- valeurs lues : `time`
- annonces :
  - ligne 131, `update`, popup **+100** — si `self.link is not None`
  - ligne 135, `update`, slam **CLEAR!** — si `self.link is not None` ET `all((t is None for row in self.board for t in row))`
  - ligne 149, `update`, popup **SHUFFLE** — si `got is None`

### BlobWell — `dmd/hd_games16.py` lignes 206 à 362

- annonces :
  - ligne 307, `step`, popup **FULL!** — si `self.pair is None` ET `self.height(c) < 2 or self.height(c + 1) < 2`
  - ligne 337, `burst`, popup **f'{self.chain} CHAIN!'** — si `self.chain >= 2`
  - ligne 339, `burst`, popup **f'+{len(cells) * 10}'** — si `not (self.chain >= 2)`

### GulunpaScene — `dmd/hd_games16.py` lignes 390 à 411

- hérite de : BlobScene
- jeux (1) : gulunpa

### PnickiesScene — `dmd/hd_games16.py` lignes 414 à 432

- hérite de : BlobScene
- jeux (1) : pnickj

### FrogFeastScene — `dmd/hd_games16.py` lignes 457 à 555

- hérite de : GameScene
- jeux (1) : cps1frog
- annonces :
  - ligne 500, `update`, slam **TIME UP** — si `now - self.t0 > self.ROUND`
  - ligne 525, `update`, popup **+1** — si `(near[0] - f['x']) ** 2 + (near[1] - f['y']) ** 2 < self.S(260) ** 2 and self.rng.random() < 0.75`

### PokonyanScene — `dmd/hd_games16.py` lignes 611 à 674

- hérite de : GameScene
- jeux (1) : pokonyan
- annonces :
  - ligne 652, `update`, popup **+10** — si `(b[0] - bx) ** 2 + (b[1] - (by + S(70))) ** 2 < S(90) ** 2`

### MagicalPumpkinScene — `dmd/hd_games16.py` lignes 709 à 759

- hérite de : GameScene
- jeux (1) : mpumpkin
- annonces :
  - ligne 742, `update`, popup **+50** — si `(st[0] - cx) ** 2 + (st[1] - cy) ** 2 < S(90) ** 2`

### MarineKunScene — `dmd/hd_games16.py` lignes 772 à 837

- hérite de : GameScene
- jeux (1) : ganbare
- annonces :
  - ligne 813, `update`, popup **f'+{win}'** — si `self.target is not None` ET `(tx - self.aim[0]) ** 2 + (ty - self.aim[1]) ** 2 < S(18) ** 2 and now - self.target['t0'] > self.target['dur'] * 0.35`

### PulstarScene — `dmd/hd_games2.py` lignes 87 à 318

- hérite de : BlazingStarScene
- jeux (1) : pulstar
- valeurs lues : `charge`, `pods`, `speed`, `stage`, `stage_name`
- changements guettés : `charge`, `pods`, `stage`
- annonces :
  - ligne 160, `update`, popup **tr('BOUCLIER', 'SHIELD') if gained == 1 else 'POD +'** — si `ch and alive` ET `gained`
  - ligne 166, `update`, slam **FINAL STAGE** — si `ch and ch[1] >= 1` ET `n >= 8`
  - ligne 168, `update`, slam **f'STAGE {n}'** — si `ch and ch[1] >= 1` ET `not (n >= 8)`
  - ligne 199, `_release`, popup **CHARGED SHOT** — si `level > 0.8`

### MagicalDropScene — `dmd/hd_games2.py` lignes 550 à 794

- hérite de : GameScene
- jeux (1) : magdrop3
- valeurs lues : `cpu_p2`, `level`
- changements guettés : `'card' + suf`, `'quota' + suf`, `level`
- annonces :
  - ligne 632, `_pop`, popup **f'CHAIN ×{n // 3}'** — si `n >= 6`
  - ligne 668, `update`, popup **CLEAR!** — si `ch` ET `new < old` ET `new <= 0`
  - ligne 707, `update`, popup **f'LV {int(ch[1])}'** — si `ch and ch[1] > ch[0]`

### SoccerScene — `dmd/hd_games2.py` lignes 884 à 1349

- hérite de : GameScene
- changements guettés : `name`
- annonces :
  - ligne 1059, `scored`, slam **GOAL!** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1078, `saved`, popup **SAVE!** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1095, `super_shot`, popup **SUPER SHOT!** — sans condition dans cette fonction, voir qui l'appelle

### SuperSidekicks3Scene — `dmd/hd_games2.py` lignes 1352 à 1353

- hérite de : SoccerScene
- jeux (1) : ssideki3

### Ultimate11Scene — `dmd/hd_games2.py` lignes 1356 à 1358

- hérite de : SoccerScene
- jeux (1) : ssideki4

### TopHunterScene — `dmd/hd_games3.py` lignes 549 à 1111

- hérite de : GameScene
- jeux (1) : tophuntr
- valeurs lues : `time`
- changements guettés : `'lives' + suf`, `'power' + suf`, `'score' + suf`, `time`
- annonces :
  - ligne 852, `special`, slam **SPECIAL MOVE!** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 867, `hurt`, popup **-1 LIFE** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 888, `update`, popup **1UP !** — si `not (ch and ch[1] < ch[0])` ET `self.one_up(vals, side)`

### BaseballScene — `dmd/hd_games3.py` lignes 1299 à 1905

- hérite de : GameScene
- jeux (1) : bstars2
- changements guettés : `n`, `name`
- annonces :
  - ligne 1436, `update`, popup **POW !** — si `ch and ch[1] <= ch[0] - 12`
  - ligne 1596, `scored`, slam **GRAND SLAM!** — si `r['last']` ET `n >= 4`
  - ligne 1605, `fireworks`, slam **HOME RUN!** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1620, `switch`, popup **3 OUTS** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1843, `call`, popup **text** — sans condition dans cette fonction, voir qui l'appelle

### LastResortScene — `dmd/hd_games3.py` lignes 1981 à 2192

- hérite de : BlazingStarScene
- jeux (1) : lresort
- valeurs lues : `speed`
- changements guettés : `'speed' + suf`
- annonces :
  - ligne 2069, `update`, popup **SPEED UP** — si `ch and ch[1] > ch[0] and (side == 'p1')`

### AeroFightersScene — `dmd/hd_games3.py` lignes 2474 à 2835

- hérite de : BlazingStarScene
- changements guettés : `'bombs' + suf`
- annonces :
  - ligne 2574, `update`, popup **BOMB UP** — si `not (ch and ch[1] < ch[0] and (now - P['t_dead'] > 1.2))` ET `ch and ch[1] == ch[0] + 1 and (now - P['t_dead'] > 1.2) and (vals.get(side + '_mode') in (1, None))`
  - ligne 2654, `bomb`, popup **BOMB!** — sans condition dans cette fonction, voir qui l'appelle

### AeroFighters2Scene — `dmd/hd_games3.py` lignes 2838 à 2839

- hérite de : AeroFightersScene
- jeux (1) : sonicwi2

### AeroFighters3Scene — `dmd/hd_games3.py` lignes 2842 à 2880

- hérite de : AeroFightersScene
- jeux (1) : sonicwi3
- valeurs lues : `pilot_name`, `plane`, `plane_name`
- changements guettés : `plane`

### StrikersScene — `dmd/hd_games4.py` lignes 203 à 591

- hérite de : BossAlert, AeroFightersScene
- jeux (1) : s1945p
- valeurs lues : `_bhp`, `_bmark`, `_mission`, `_title`, `plane_name`
- changements guettés : `'lives' + suf`, `'super' + suf`
- annonces :
  - ligne 261, `missions`, slam **f'MISSION {m}'** — si `t == 0 and self.title_prev == 1 and (m is not None)`
  - ligne 287, `track_boss`, announce **now** — si `B is None` ET `parts and (not self.nobody(vals))` ET `self.boss_seen != self.mission`
  - ligne 296, `track_boss`, slam **IT TRANSFORMS!** — si `B['gone'] is not None` ET `parts`
  - ligne 300, `track_boss`, slam **BOSS DESTROYED!** — si `B['gone'] is not None` ET `not (parts)` ET `now - B['gone'] >= self.BOSS_WAIT`
  - ligne 440, `super_shot`, popup **SUPER SHOT !** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 453, `bomb`, popup **BOMB!** — sans condition dans cette fonction, voir qui l'appelle

### StreetHoopScene — `dmd/hd_games4.py` lignes 696 à 999

- hérite de : GameScene
- jeux (1) : strhoop
- valeurs lues : `points`, `points_p2`, `time_min`, `time_sec`
- changements guettés : `half`, `name`
- annonces :
  - ligne 778, `update`, slam **2ND HALF** — si `ch and ch[1] > ch[0]`
  - ligne 819, `scored`, popup **MISSED** — si `b['kind'] == 'miss'`
  - ligne 829, `scored`, popup **SUPER SHOT !** — si `st is not None and now - st[0] < 5.0 and (st[1] == b['team'])`
  - ligne 835, `scored`, popup **DUNK !** — si `not (st is not None and now - st[0] < 5.0 and (st[1] == b['team']))` ET `b['kind'] == 'dunk'`
  - ligne 838, `scored`, popup **f"{b['pts']} POINTS" if b['pts'] > 1 else '1 POINT'** — si `not (st is not None and now - st[0] < 5.0 and (st[1] == b['team']))` ET `not (b['kind'] == 'dunk')`

### DodgeBallScene — `dmd/hd_games4.py` lignes 1123 à 1395

- hérite de : GameScene
- jeux (1) : sdodgeb
- valeurs lues : `time`
- changements guettés : `'power' + suf`, `f'hp{k + 1}{suf}'`
- annonces :
  - ligne 1229, `throw`, slam **POWER SHOT !** — si `power`
  - ligne 1249, `landed`, popup **OUT !** — si `b['hit']` ET `b['out']`

### NeoBombermanScene — `dmd/hd_games4.py` lignes 1469 à 1821

- hérite de : GameScene
- jeux (1) : neobombe
- valeurs lues : `stage`, `world`
- changements guettés : `'bombs' + suf`, `'lives' + suf`, `name + suf`, `stage`
- annonces :
  - ligne 1558, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0] and alive`
  - ligne 1563, `update`, popup **1UP !** — si `not (ch and ch[1] < ch[0] and alive)` ET `self.one_up(vals, side)`
  - ligne 1568, `update`, popup **label** — si `ch and ch[1] > ch[0] and alive`
  - ligne 1585, `update`, slam **f'STAGE {w}-{int(ch[1])}'** — si `ch`

### RallyScene — `dmd/hd_games4.py` lignes 1853 à 1991

- hérite de : GameScene
- valeurs lues : `time`
- annonces :
  - ligne 1944, `update`, popup **EXTENDED TIME** — si `sec is not None and old is not None and (old > 0) and (sec > old + 1.5)`

### NeoDriftScene — `dmd/hd_games4.py` lignes 1994 à 2019

- hérite de : RallyScene
- jeux (1) : neodrift
- valeurs lues : `time_cs`, `time_s`

### ThrashRallyScene — `dmd/hd_games4.py` lignes 2022 à 2053

- hérite de : RallyScene
- jeux (1) : trally
- valeurs lues : `speed`, `time`

### RidingHeroScene — `dmd/hd_games4.py` lignes 2087 à 2264

- hérite de : GameScene
- jeux (1) : ridhero
- valeurs lues : `rank`, `speed`, `time`, `turbo`
- changements guettés : `rank`, `time`, `turbo`
- annonces :
  - ligne 2149, `update`, popup **TURBO !** — si `ch and ch[1] == ch[0] - 1`
  - ligne 2159, `update`, popup **f"{int(ch[1])}{self.ORD.get(int(ch[1]), 'TH')}"** — si `ch and 0 < ch[1] < ch[0]`
  - ligne 2164, `update`, popup **EXTENDED TIME** — si `ch and ch[0] > 0 and (ch[1] > ch[0] + 5)`

### LeagueBowlingScene — `dmd/hd_games4.py` lignes 2319 à 2472

- hérite de : GameScene
- jeux (1) : lbowling
- valeurs lues : `score`, `time`
- changements guettés : `time`
- annonces :
  - ligne 2409, `hit`, slam **STRIKE !** — si `all((not p['up'] for p in self.pins))` ET `not self.second`
  - ligne 2411, `hit`, slam **SPARE !** — si `all((not p['up'] for p in self.pins))` ET `not (not self.second)`
  - ligne 2413, `hit`, popup **str(n)** — si `not (all((not p['up'] for p in self.pins)))` ET `n`

### MagicianLordScene — `dmd/hd_games4.py` lignes 2589 à 2741

- hérite de : GameScene
- jeux (1) : maglord
- valeurs lues : `_turn`, `form`, `power`
- changements guettés : `energy`, `lives`, `power`, `score`
- annonces :
  - ligne 2636, `always`, slam **TRANSFORMATION !** — si `form != self.form`
  - ligne 2646, `update`, popup **-1** — si `ch and ch[1] < ch[0]`
  - ligne 2650, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`
  - ligne 2654, `update`, popup **POW UP** — si `ch and ch[1] > ch[0]`

### NamScene — `dmd/hd_games5.py` lignes 90 à 316

- hérite de : GameScene
- jeux (1) : nam1975
- valeurs lues : `weapon_p2`
- changements guettés : `'lives' + suf2`, `ammo`, `ammo_p2`, `grenades`, `grenades_p2`, `score`, `weapon`, `weapon_p2`
- annonces :
  - ligne 180, `update`, popup **tr(*NAM_WEAPONS.get(int(ch[1]), NAM_WEAPONS[0])) + ' !'** — si `ch`
  - ligne 197, `update`, popup **tr(*NAM_WEAPONS.get(int(ch[1]), NAM_WEAPONS[0])) + ' !'** — si `self.p2_in(vals)` ET `ch`
  - ligne 203, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0] and (self.p1_in(vals) if side == 'p1' else self.p2_in(vals))`

### CyberLipScene — `dmd/hd_games5.py` lignes 383 à 585

- hérite de : GameScene
- jeux (1) : cyberlip
- valeurs lues : `score`, `score_p2`, `time`, `time_min`
- changements guettés : `key`, `key + '_p2'`, `lives`, `lives_p2`, `score`
- annonces :
  - ligne 444, `update`, popup **name + ' !'** — si `ch and ch[1] < ch[0]` ET `self.weapon is None or self.weapon[0] != name`
  - ligne 452, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`
  - ligne 458, `update`, popup **name + ' !'** — si `self.p2_in(vals)` ET `ch and ch[1] < ch[0]` ET `self.weapon2 is None or self.weapon2[0] != name`
  - ligne 465, `update`, popup **-1 LIFE** — si `self.p2_in(vals)` ET `ch and ch[1] < ch[0]`

### GhostPilotsScene — `dmd/hd_games5.py` lignes 647 à 727

- hérite de : AeroFightersScene
- jeux (1) : gpilots

### AlphaMission2Scene — `dmd/hd_games5.py` lignes 730 à 802

- hérite de : AeroFightersScene
- jeux (1) : alpham2
- annonces :
  - ligne 763, `power_pop`, popup **ARMOR!** — sans condition dans cette fonction, voir qui l'appelle

### ViewpointScene — `dmd/hd_games5.py` lignes 845 à 960

- hérite de : BlazingStarScene
- jeux (1) : viewpoin
- changements guettés : `bomb_type`
- annonces :
  - ligne 876, `update`, popup **name** — si `not (ch and ch[0] and (not ch[1]) and self.ships['p1']['in'])` ET `ch and ch[1]`

### ZedBladeScene — `dmd/hd_games5.py` lignes 1056 à 1132

- hérite de : SideShooterScene
- jeux (1) : zedblade
- valeurs lues : `score`, `score_p2`, `shot_level`
- changements guettés : `bombs`, `shot_level`
- annonces :
  - ligne 1093, `update`, power_pop **x** — si `ch and ch[1] > ch[0] and self.ships['p1']['in']`

### PrehistoricIsle2Scene — `dmd/hd_games5.py` lignes 1135 à 1203

- hérite de : SideShooterScene
- jeux (1) : preisle2
- changements guettés : `bombs`

### ShockTroopers2Scene — `dmd/hd_games5.py` lignes 1318 à 1689

- hérite de : Machines, GameScene
- valeurs lues : `power`, `power_p2`, `time`
- changements guettés : `'energy' + suf`, `ammo`, `ammo_p2`, `grenades`, `grenades_p2`, `lives`, `lives_p2`, `score`, `weapon`, `weapon_p2`
- annonces :
  - ligne 1421, `second`, popup **name + ' !'** — si `ch`
  - ligne 1444, `second`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`
  - ligne 1449, `second`, popup **LV UP !** — si `p is not None` ET `self.lv2 is not None and lv > self.lv2`
  - ligne 1486, `update`, popup **name + ' !'** — si `ch`
  - ligne 1516, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`
  - ligne 1521, `update`, popup **LV UP !** — si `p is not None` ET `self.lv is not None and lv > self.lv`

### BrawlerScene — `dmd/hd_games5.py` lignes 1829 à 2020

- hérite de : GameScene
- changements guettés : `'lives' + suf`, `'score' + suf`, `self.ENERGY + suf`
- annonces :
  - ligne 1953, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`

### RoboArmyScene — `dmd/hd_games5.py` lignes 2023 à 2055

- hérite de : BrawlerScene
- jeux (1) : roboarmy

### BurningFightScene — `dmd/hd_games5.py` lignes 2058 à 2088

- hérite de : BrawlerScene
- jeux (1) : burningf
- valeurs lues : `time`

### MutationNationScene — `dmd/hd_games6.py` lignes 42 à 96

- hérite de : BrawlerScene
- jeux (1) : mutnat
- changements guettés : `'bombs' + suf`
- annonces :
  - ligne 70, `update`, popup **ATTACK!** — sans condition dans cette fonction, voir qui l'appelle

### SengokuScene — `dmd/hd_games6.py` lignes 104 à 158

- hérite de : BrawlerScene
- jeux (2) : sengoku, sengoku3
- changements guettés : `'weapon' + suf`
- annonces :
  - ligne 123, `update`, popup **name + ' !'** — si `ch and ch[1]`

### Sengoku2Scene — `dmd/hd_games6.py` lignes 161 à 172

- hérite de : SengokuScene
- jeux (1) : sengoku2

### NinjaCombatScene — `dmd/hd_games6.py` lignes 179 à 230

- hérite de : BrawlerScene
- jeux (1) : ncombat

### NinjaCommandoScene — `dmd/hd_games6.py` lignes 241 à 350

- hérite de : ShockTroopers2Scene
- jeux (1) : ncommand
- changements guettés : `energy`, `energy_p2`

### BluesJourneyScene — `dmd/hd_games6.py` lignes 436 à 553

- hérite de : CyberLipScene
- jeux (1) : bjourney
- valeurs lues : `time`
- changements guettés : `energy`, `lives`, `money`, `score`
- annonces :
  - ligne 480, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`
  - ligne 487, `update`, popup **f'+{int(ch[1] - ch[0])}'** — si `ch and ch[1] > ch[0]`

### PuzzleBobble2Scene — `dmd/hd_games6.py` lignes 606 à 674

- hérite de : PuzzleBobbleScene
- jeux (1) : pbobbl2n
- valeurs lues : `wins`, `wins_p2`
- changements guettés : `'time' + suf`, `name`

### PuzzleBobble1Scene — `dmd/hd_games6.py` lignes 677 à 752

- hérite de : PuzzleBobbleScene
- jeux (1) : pbobblen
- changements guettés : `name`
- annonces :
  - ligne 706, `won`, slam **tr('J1 GAGNE !', 'P1 WINS!') if side == 'p1' else tr('J2 GAGNE !', 'P…** — sans condition dans cette fonction, voir qui l'appelle

### PuzzleDePonScene — `dmd/hd_games6.py` lignes 772 à 793

- hérite de : PuzzleBobble2Scene
- jeux (1) : puzzledp
- valeurs lues : `level`, `time`

### MagicalDrop2Scene — `dmd/hd_games6.py` lignes 797 à 808

- hérite de : MagicalDropScene
- jeux (1) : magdrop2
- valeurs lues : `level`

### MoneyPuzzleScene — `dmd/hd_games6.py` lignes 843 à 882

- hérite de : MagicalDropScene
- jeux (1) : miexchng
- valeurs lues : `level`, `max_chain`
- changements guettés : `chain`, `score`
- annonces :
  - ligne 869, `update`, popup **f'{int(ch[1])} CHAIN'** — si `ch and ch[1] > ch[0]`

### PuzzleDePonRScene — `dmd/hd_games7.py` lignes 23 à 26

- hérite de : PuzzleDePonScene
- jeux (1) : puzzldpr

### SpinMasterScene — `dmd/hd_games7.py` lignes 87 à 189

- hérite de : CyberLipScene
- jeux (1) : spinmast
- changements guettés : `bombs`, `energy`, `lives`, `score`
- annonces :
  - ligne 129, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`

### GanryuScene — `dmd/hd_games7.py` lignes 204 à 278

- hérite de : SengokuScene
- jeux (1) : ganryu
- valeurs lues : `_turn`, `energy`, `time`
- changements guettés : `ammo`

### SuperSidekicksScene — `dmd/hd_games7.py` lignes 291 à 312

- hérite de : SoccerScene
- jeux (1) : ssideki
- valeurs lues : `time_min`, `time_sec`

### SuperSidekicks2Scene — `dmd/hd_games7.py` lignes 315 à 334

- hérite de : SoccerScene
- jeux (1) : ssideki2

### PanicBomberScene — `dmd/hd_games7.py` lignes 475 à 558

- hérite de : GameScene
- jeux (1) : panicbom
- changements guettés : `'power' + suf`, `score`
- annonces :
  - ligne 511, `update`, popup **POWER UP !** — si `ch and ch[1] > ch[0]`
  - ligne 516, `update`, popup **f'{int(ch[1] - ch[0])} Pts.'** — si `ch and ch[1] > ch[0]`

### PopBounceScene — `dmd/hd_games7.py` lignes 577 à 691

- hérite de : GameScene
- jeux (1) : popbounc
- valeurs lues : `lives`, `score`
- changements guettés : `score`

### SuperBubblePopScene — `dmd/hd_games7.py` lignes 695 à 811

- hérite de : GameScene
- jeux (1) : sbp
- valeurs lues : `score`
- changements guettés : `score`

### ZupapaScene — `dmd/hd_games7.py` lignes 867 à 1002

- hérite de : GameScene
- jeux (1) : zupapa
- changements guettés : `lives`, `score`
- annonces :
  - ligne 947, `update`, popup **-1 LIFE** — si `ch and ch[1] < ch[0]`

### NeoMrDoScene — `dmd/hd_games7.py` lignes 1040 à 1151

- hérite de : GameScene
- jeux (1) : neomrdo
- changements guettés : `score`

### TecmoSoccerScene — `dmd/hd_games8.py` lignes 31 à 49

- hérite de : SoccerScene
- jeux (1) : twsoc96

### Goal3Scene — `dmd/hd_games8.py` lignes 52 à 73

- hérite de : SoccerScene
- jeux (1) : goalx3
- valeurs lues : `time`

### NeoCup98Scene — `dmd/hd_games8.py` lignes 76 à 96

- hérite de : SoccerScene
- jeux (1) : neocup98

### SoccerBrawlScene — `dmd/hd_games8.py` lignes 99 à 120

- hérite de : SoccerScene
- jeux (1) : socbrawl
- valeurs lues : `time_min`, `time_sec`

### PleasureGoalScene — `dmd/hd_games8.py` lignes 123 à 142

- hérite de : SoccerScene
- jeux (1) : pgoal
- valeurs lues : `clock`

### FootballFrenzyScene — `dmd/hd_games8.py` lignes 167 à 298

- hérite de : GameScene
- jeux (1) : fbfrenzy
- valeurs lues : `time_min`, `time_sec`
- changements guettés : `name`
- annonces :
  - ligne 250, `update`, slam **TOUCHDOWN!** — si `not (ph[0] == 'set' and now - ph[1] > 1.6)` ET `ph[0] == 'run'` ET `done or now - ph[1] > 6` ET `ph[2] or not 0 <= c['yd'] <= 100`

### BaseballStarsProScene — `dmd/hd_games8.py` lignes 302 à 329

- hérite de : BaseballScene
- jeux (1) : bstars
- valeurs lues : `inning`, `time`, `time_min`

### Baseball2020Scene — `dmd/hd_games8.py` lignes 332 à 359

- hérite de : BaseballScene
- jeux (1) : 2020bb
- valeurs lues : `time`, `time_min`
- changements guettés : `outs_total`

### TopPlayersGolfScene — `dmd/hd_games8.py` lignes 363 à 377

- hérite de : TurfMastersScene
- jeux (1) : tpgolf
- valeurs lues : `holes`, `time`

### PowerSpikes2Scene — `dmd/hd_games8.py` lignes 407 à 493

- hérite de : GameScene
- jeux (1) : pspikes2
- valeurs lues : `time_min`, `time_sec`
- changements guettés : `'power' + suf`
- annonces :
  - ligne 452, `update`, popup **POWER SPIKE!** — si `ch and ch[1] < ch[0] - 8`

### BangBeadScene — `dmd/hd_games9.py` lignes 254 à 314

- hérite de : CourtDuelScene
- jeux (1) : bangbead
- changements guettés : `'score' + suf`, `'stock' + suf`
- annonces :
  - ligne 274, `update`, popup **MIRACLE SHOT!** — si `ch and ch[1] < ch[0]`
  - ligne 285, `scored`, popup **GOAL!** — sans condition dans cette fonction, voir qui l'appelle

### FlipShotScene — `dmd/hd_games9.py` lignes 317 à 400

- hérite de : CourtDuelScene
- jeux (1) : flipshot
- valeurs lues : `time`
- changements guettés : `f'target{k + 1}{suf}'`
- annonces :
  - ligne 366, `scored`, popup **TARGET!** — si `cr[k] >= 3`
  - ligne 368, `scored`, slam **ROUND CLEAR** — si `cr[k] >= 3` ET `all((c >= 3 for c in cr))`

### OverTopScene — `dmd/hd_games9.py` lignes 407 à 482

- hérite de : RallyScene
- jeux (1) : overtop
- valeurs lues : `lap_cs`, `lap_min`, `lap_sec`, `rank`, `speed`
- changements guettés : `rank`
- annonces :
  - ligne 434, `update`, popup **OVERTAKE!** — si `ch and ch[1] < ch[0]`

### HorseRaceScene — `dmd/hd_games9.py` lignes 550 à 676

- hérite de : GameScene
- annonces :
  - ligne 596, `surge`, popup **text** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 614, `update`, slam **GOAL!** — si `self.phase == 'finish'` ET `self.winner is None and self.post < self.hx(lead) + self.S(90)`

### StakesWinnerScene — `dmd/hd_games9.py` lignes 687 à 735

- hérite de : HorseRaceScene
- jeux (1) : stakwin
- changements guettés : `name`

### StakesWinner2Scene — `dmd/hd_games9.py` lignes 738 à 753

- hérite de : StakesWinnerScene
- jeux (1) : stakwin2
- valeurs lues : `power`
- changements guettés : `power`

### JockeyGPScene — `dmd/hd_games9.py` lignes 756 à 791

- hérite de : HorseRaceScene
- jeux (1) : jockeygp

### GururinScene — `dmd/hd_games9.py` lignes 935 à 1042

- hérite de : GameScene
- jeux (1) : gururin
- valeurs lues : `level`
- changements guettés : `f'cur_{p}{suf}'`, `level`
- annonces :
  - ligne 984, `update`, slam **f'LEVEL {int(ch[1])}'** — si `ch and ch[1] > ch[0]`

### GhostlopScene — `dmd/hd_games9.py` lignes 1091 à 1183

- hérite de : PuzzleBobble2Scene
- jeux (1) : ghostlop
- valeurs lues : `time`

### PetField — `dmd/hd_games9.py` lignes 1213 à 1300

- annonces :
  - ligne 1288, `resolve`, popup **f'{self.chain} CHAIN!'** — si `self.chain >= 2`

### PochiNyaaScene — `dmd/hd_games9.py` lignes 1303 à 1373

- hérite de : GameScene
- jeux (1) : pnyaa

### PuzzleWell — `dmd/hd_games9.py` lignes 1405 à 1505

- annonces :
  - ligne 1485, `step`, popup **STAGE CLEAR!** — si `self.flash is not None` ET `now - t0 > 0.3` ET `not any((v == 7 for row in self.grid for v in row))`

### PuzzledScene — `dmd/hd_games9.py` lignes 1508 à 1596

- hérite de : GameScene
- jeux (1) : joyjoy
- valeurs lues : `balloons`, `score`

### BossAlert — `dmd/hd_mercs.py` lignes 59 à 97

- annonces :
  - ligne 67, `announce`, slam **WARNING!** — sans condition dans cette fonction, voir qui l'appelle

### MercsScene — `dmd/hd_mercs.py` lignes 101 à 570

- hérite de : BossAlert, GameScene
- jeux (1) : mercs
- valeurs lues : `_hps`, `credits`, `mission`, `p1_mode`, `time`
- changements guettés : `'bombs' + suf`, `'health' + suf`, `'score' + suf`, `'weapon' + suf`, `'weapon_level' + suf`
- annonces :
  - ligne 165, `always`, slam **f'MISSION {int(m)}'** — si `m is not None and m != self.mission` ET `self.mission is not None and m > self.mission`
  - ligne 191, `update`, popup **+ ENERGY** — si `not (ch and ch[1] < ch[0] and (ch[1] > 0))` ET `ch and ch[1] > ch[0] and (ch[0] > 0)`
  - ligne 199, `update`, popup **tr(name[0], name[1]) + ' !'** — si `ch`
  - ligne 215, `kill`, fx.text **f'+{_fmt(gain)}'** — si `self.boss and self.boss.get('down') is not None`
  - ligne 248, `kill`, fx.text **f'+{_fmt(gain)}'** — si `gain >= 100`
  - ligne 258, `power_up`, popup **POWER UP!** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 263, `mega_crash`, slam **MEGA CRASH!** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 313, `track_boss`, announce **now** — si `B is None or (not B['armoured'] and B['down'] is None)` ET `found is not None and (B is None or (found[2] and (not B['armoured'])))` ET `self.boss_seen != self.mission or (armour and B is not None)`

### MetalSlugScene — `dmd/hd_mslug.py` lignes 635 à 2492

- jeux (6) : mslug, mslug2, mslug3, mslug4, mslug5, mslugx
- valeurs lues : `ammo`, `bombs`, `boss_dead`, `boss_name`, `credits`, `grenades_out`, `lives`, `mission`, `mission_done`, `p1_mode`, `p2_mode`, `prisoners`, `score`, `time`, `vehicle`, `vehicle_ammo`, `vehicle_hp`, `vehicle_kind`, `weapon`
- annonces :
  - ligne 1186, `_boss.alert`, lights **boss** — si `lights is not None`
  - ligne 1431, `_player`, fx.text **P2 JOINS IN!** — si `mode != P.mode` ET `mode == 1 and P.mode not in (1, 2)` ET `P.mode is not None and side == 'p2' and self.playing(self.players['p1'])`
  - ligne 1515, `_diff`, fx.text **f'+{d}'** — si `cur['ammo'] is not None and old.get('ammo') is not None and (w == wo)` ET `not (d < 0 and (not P.tank))` ET `d > 0` ET `cur['ammo'] < 60000` (et 1 autre condition au-dessus)
  - ligne 1571, `_diff`, fx.text **tr('+1 PRISONNIER', '+1 PRISONER') if pr - po == 1 else tr(f'+{pr - p…** — si `pr is not None and po is not None and (pr > po)`
  - ligne 1634, `_tank_in`, fx.text **tr(*RIDE_IN.get(P.ride or 'tank', RIDE_IN_ANY))** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1646, `_tank_out`, fx.text **tr(*RIDE_LOST.get(P.ride or 'tank', RIDE_LOST_ANY))** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1692, `_score_float`, fx.text **txt** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1702, `_life_lost`, fx.text **-1 LIFE** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1706, `_bombs_found`, fx.text **f'+{n} BOMBS'** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1714, `_life_up`, fx.text **1UP !** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 1724, `_weapon_change`, fx.text **OUT OF AMMO** — si `kind == 'pistol'`
  - ligne 1932, `_coin_ding`, fx.text **word** — si `n and (not self.in_attract) and (self.coin_box is not None)`

### PanelScene — `dmd/hd_panels.py` lignes 142 à 763

- hérite de : GameScene
- valeurs lues : `armor`, `armor_kind`, `p2_mode`, `time`, `weapon`
- changements guettés : `'bombs' + sfx`, `'lives' + sfx`, `'score' + sfx`, `_p2_chr`, `fl.get('value', 'floor')`, `g2['value'] + sfx`, `gauge['value'] + sfx`, `health_p2`, `item['value']`, `item['value'] + (sfx if both else '')`, `lives_p2`, `lv[0] + sfx`, `name`, `power_p2`, `score_p2`, `watch[0] if side == 'p1' else watch[1]`, `weapon`
- annonces :
  - ligne 241, `update`, popup **PLAYER 2!** — si `any(moved2) and spec.get('two', True)` ET `not self.p2_in(vals)`
  - ligne 261, `update`, popup **+ LIFE** — si `gauge` ET `ch` ET `not (ch[1] < ch[0])` ET `ch[1] > ch[0] + 5`
  - ligne 268, `update`, popup **1UP** — si `ch` ET `not (ch[1] < ch[0])`
  - ligne 307, `update`, popup **ARMOUR LOST!** — si `spec.get('armor') and side == 'p1'` ET `self._armor is not None and state != self._armor` ET `state == 'none'`
  - ligne 316, `update`, popup **tr(*item['up'])** — si `ch and ch[1] > ch[0]`
  - ligne 332, `update`, popup **f'{n}!'** — si `spec.get('names')` ET `ch` ET `n`
  - ligne 340, `update`, popup **tr(*lv[1])** — si `spec.get('names')` ET `ch` ET `ch[1] > ch[0]`
  - ligne 353, `update`, popup **tr(*fl['done']).format(n=int(ch[0]))** — si `spec.get('floor')` ET `ch` ET `fl.get('done') and ch[1] == ch[0] + 1`
  - ligne 389, `_hit`, popup **f'+{int(gain)}'** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 427, `_down`, popup **-1 LIFE** — sans condition dans cette fonction, voir qui l'appelle

### SpfScene — `dmd/hd_spf.py` lignes 251 à 952

- hérite de : GameScene
- jeux (1) : spf2t
- valeurs lues : `_rounds_vs`, `atk1`, `atk2`, `credits`, `p1_mode`, `p2_mode`, `wins1`, `wins2`
- changements guettés : `name`
- annonces :
  - ligne 530, `burst`, fx.text **f'{n}'** — si `n >= 4`

### SecondSquadScene — `dmd/hd_squad.py` lignes 106 à 868

- hérite de : Machines, GameScene
- jeux (1) : shocktr2
- valeurs lues : `_area`, `_boss`, `_clear`, `_hps`, `_mission`, `_stage`, `_wait`, `credits`, `p1_mode`, `time`
- changements guettés : `'energy' + suf`, `'grenades' + suf`, `'lives' + suf`, `'power' + suf`, `'score' + suf`, `'weapon' + suf`, `_boss`, `_clear`, `_stage`, `_wait`
- annonces :
  - ligne 223, `missions`, slam **STAGE CLEAR** — si `cl and cl[1] and (not cl[0])`
  - ligne 230, `missions`, slam **f'MISSION {m[0]}'** — si `self.pending and m and (m[1] or now >= self.pending[1])` ET `m[0] == self.pending[0]`
  - ligne 271, `update`, popup **'ROLLING IN!' if ride else 'ROLLING OUT'** — si `ride != P.ride`
  - ligne 308, `update`, popup **DOWN!** — si `lost`
  - ligne 321, `update`, popup **self.weapon(vals, side)[0] + ' !'** — si `ch` ET `ch[1]`
  - ligne 386, `boss_watch`, slam **ALERT** — si `F is None` ET `heard`
  - ligne 459, `_part_shown`, popup **f"PHASE {F['wave']}"** — si `not row or (all((q['dead'] is not None for q in row)) and p['batch'] > max((q['batch'] for q in row)))` ET `F['wave'] > 1`
  - ligne 478, `_boss_down`, slam **BOSS DESTROYED** — sans condition dans cette fonction, voir qui l'appelle
  - ligne 627, `kill`, fx.text **f'+{_fmt(gain)}'** — si `gain >= 100`
  - ligne 656, `power_up`, slam **f'LEVEL {lv}'** — si `lv > power_steps(old)[0]`
  - ligne 658, `power_up`, popup **POWER UP** — si `not (lv > power_steps(old)[0])`

### Stick — `dmd/hd_stick.py` lignes 157 à 402

- valeurs lues : `_p1_dir`, `_p2_dir`

### TwinkleScene — `dmd/hd_twinkle.py` lignes 231 à 1129

- hérite de : GameScene
- jeux (1) : twinspri
- valeurs lues : `stage`, `wins`, `wins_p2`
- changements guettés : `'attack' + suf`, `'bombs' + suf`, `'hits' + suf`, `'lives' + suf`, `'perfect' + suf`, `'power' + suf`

