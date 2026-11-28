Each of the 57 Neo Geo fighting games has its own file in `games\`, official variants included, and the 34 Capcom fighting games fight on their own stages. The King of Fighters '98 was tuned round after round on a real cabinet, from recorded games, and so were '97 and 2002 in 1.33.1.

![ROUND 1 and FIGHT ! in The King of Fighters '98](images/kof98_round_start.gif)

## What the HD screen shows

- At the top, each player's score, or CHALLENGER and BEAT BY in a VS match. In the middle, the health bars with a light trail for the hit just taken, and the timer or KO. At the bottom, P1, P2 or CPU with the current fighter, the full team in The King of Fighters '96 to 2000 (fighters already beaten struck out), and the credits.
- Sparks on every hit, the combo counter, FIRST ATTACK, a red heartbeat when the health is low. A big blow sends a shock wave from the bar, the damage shows on it, and a blow the game empties over several frames counts as one.
- The rounds won as gold stars under the health bars, read in the game or counted from the K.O. in every game of single fighters. A match won says how many rounds to how many.
- K.O. in big red letters on the loser's side and WIN in gold on the winner's, DOUBLE K.O., TIME UP, PERFECT, confetti for the winner.
- ROUND 2, ROUND 3... when the game starts the round, and FIGHT ! with the game's own FIGHT, GO or EN GARDE (as its timer starts in the games where that call is not read yet).
- The next King of Fighters fighter entering once the K.O. is over, and when a team loses its third fighter, P1 WINS and the team eliminated.
- Since 1.41 the fights are drawn on black. In The King of Fighters '97, '98 and 2002 the game's logo goes small in the top row and the panel under a player's name lists every move of his fighter (see the book of moves below).
- **Draw a stage behind the fights**, in the Screens tab of the window, brings back the stage that follows the game's own backdrop, in The King of Fighters '96 to 2000, Rage of the Dragons, Garou, Samurai Shodown II to IV, the Street Fighter games and more (see [[HD Marquee]] for the list of backdrops). The nine stages of The King of Fighters '98 are drawn after the game's places and change with the rounds as in the game.
- When nobody plays, the coin screen (see [[Usage]]).

![P1 WINS and the CPU team eliminated](images/kof98_team_eliminated.gif)

![On the author's cabinet, K.O., PERFECT and WINNER on the marquee and in the game](images/cabinet_kof98_perfect.gif)

## The desperation moves panel, The King of Fighters '98, '97 and 2002

Under the name of each human player, a panel.

- A badge says the stocks (1 STOCK, 2 STOCKS), EXTRA, MAX when every stock is lit as the game says it, or the MAX of Advanced while it runs, its timer read in the game.
- The power gauge is drawn as the game draws it, the bar and a square per stock.
- When the gauge allows a desperation move, the commands of the fighter's ones show under it, their arrows facing the other fighter. The arrows light up as the stick does them, read at every frame.
- When a button ends an attempt that missed a step, the steps missed are crossed in red with RATÉ, and DM ! or SDM ! shows once the game took its stock.
- Otherwise the panel shows the inputs pressed, as training mode does.
- '97 has its own commands, its gauge, its three stock squares and the game's own flag of a desperation move, and 2002 its own commands, MAX by B+C and its timer, a desperation move free in MAX and an SDM taking a stock, the fighting order of each team read.

### The book of moves, without the stage (1.41)

- The panel keeps the badge, the gauge and the inputs pressed on its top edge. Under them, every special move of the fighter is a card, its name over its arrows and its buttons. A card lights up arrow after arrow as the stick does the motion. The stick is what is read there, not whether the move came out.
- The desperation moves are beside the special moves, pale until one can come out. Then they light up in gold frames and get wider and bigger.
- A player alone has his desperation moves on the side nobody plays, bigger still once one can come out. The other team goes small beside its name and PRESS START small in the top row.
- With two players, the desperation moves widen as far as the special moves beside them keep arrows a player reads. A fighter with seven or eight special moves keeps them as they are, and his desperation moves widen less or only light up.
- The cards take one, two or three columns, whichever leaves the biggest arrows and letters. When the names are long, a card puts its name and its command on one line. A name is cut short only when keeping it whole would leave arrows too small.
- **List every move of the fighter under his name**, in the Screens tab of the window, turned off, gives the desperation moves alone back, bigger, with PRESS START big on the side nobody plays.

## The moves panel of the other fighting games

Under the name of each human player, a panel like the one of The King of Fighters '98 (1.38).

- The special moves of the fighter come one after another, their name, their arrows facing the other fighter and their buttons. A dot per move says which one shows. A charge is a blue arrow, a move done close or in the air says so.
- When the game's gauge is read and allows a super, the panel turns gold and shows only the supers. Samurai Shodown II shows its POW gauge, then POW MAX with its timer and the fighter's weapon-breaking technique. The Capcom games show their super gauge and its level.
- A game whose gauge is not read shows its supers in gold among the special moves.
- The special moves of the 79 fighting games come from the command list of MAME (`command.dat`, by Fabricio Coroquer and AntoPISA), written in the `specials` block of each game file by `tools/command_dat.py`.

## Moves recognised at the stick, Neo Geo

In 48 Neo Geo fighting games the stick and buttons of each player are read at every frame (1.39).

- When a button ends the motion of one of the fighter's moves, the panel shows that move for a moment, its arrows and its edge lit in green, and how many times it was done once it is more than one.
- The move shown in turn lights its arrows as the stick does them.
- The marquee reads which side each fighter faces. The arrows turn round when the fighters swap sides, and a quarter circle is named as the move it is that way round. Until that side is known, a motion that would be another move of the fighter the other way round is not named.
- A super is named when the game's gauge allows it. What is recognised is the motion, the game alone knows whether the move came out.
- The byte each game keeps for the side a fighter faces comes from the FBNeo training mode by peon2 and contributors. What it holds when a round starts is learnt there, and it is no longer used in a game where two rounds disagree.

## The desperation move show

When a human lands a desperation move, its name takes the whole marquee for a moment, then flies above his bar while the hits land, counting them. The bar of the one taking them jolts at each hit, the part just lost white then red, and at its edge the spark of each hit bursts with pieces of the bar flying off. Two at once, each name slams onto its side with DOUBLE DM ! between them.

![The second player's HOUOU KYAKU in The King of Fighters '97](images/kof97_player2_dm.gif)

## VS matches between two humans

In a two-player match, the King of Fighters games show CHALLENGER above the player who just joined and BEAT BY 02 above the one who beat 2 challengers in a row, once these counters were learned (see [[Learning Addresses]]). A WINS pill under the credits counts the matches each one won. Each win goes to `obs\vs_history.txt` and the best streak of each game is kept (see [[OBS and DOFLinx]]).

## What each game reads

Each Neo Geo fighting game has its own file in `games\`, official variants included (Japanese, Korean, prototype). The addresses come from the FinalBurn Neo cheats, peon2's FinalBurn Neo training scripts and the MAME 2003-Plus cheat database, checked against the cheat collection of MAME (mamecheat.co.uk). It gives the super gauge of Art of Fighting and Art of Fighting 2, Garou, The Last Blade 2 (with its rounds won and its stages, 1.38), Samurai Shodown II (its POW, 1.38), King of Fighters '96, Ninja Master's, the three Real Bout Fatal Fury, Rage of the Dragons, Samurai Shodown III, IV, V and V Special and World Heroes Perfect, shown under the fighters on the HD screen, the characters of Fatal Fury 2 and the timer of Karnov's Revenge. The score is known for the King of Fighters games ('99 and 2000 count battle points instead, nothing is shown) and for Samurai Shodown II. RetroAchievements gives it for Art of Fighting, Fatal Fury 1, 2, 3 and Special, Galaxy Fight, Garou, Karnov's Revenge, King of Fighters '94 and 2003, Rage of the Dragons, Real Bout Fatal Fury 1 and Special, Samurai Shodown, The Last Blade 1 and 2 and Waku Waku 7 (its public scripts on GitHub and the data `tools/ra_notes.py` downloads, to be checked in game), with the rounds won of Fatal Fury 3 and Karnov's Revenge, gold stars under the health bars on the HD screen. For the others, learn it with `learn.bat` (`score=...` and `score2=...`).

When a health bar, a timer or a name does not match the screen, run `test_retroarch.bat` during a fight and post the result in a GitHub issue.

| Game | File | Health bars | Timer | Character names | Moves | Stage | Score |
|---|---|---|---|---|---|---|---|
| 3 Count Bout | `3countb.json` | - | - | yes (8 of 10) | yes | - | to learn |
| Aggressors of Dark Kombat | `aodk.json` | yes | - | - | - | yes | to learn |
| Art of Fighting | `aof.json` | yes | yes | yes (10) | yes | yes | RetroAchievements, to be checked |
| Art of Fighting 2 | `aof2.json` | yes | yes | yes (13) | yes | yes | to learn |
| Art of Fighting 3 | `aof3.json` | yes | yes | yes (10) | yes | yes | to learn |
| Breakers | `breakers.json` | yes | yes | yes (9) | yes | yes | to learn |
| Breakers Revenge | `breakrev.json` | yes | yes | yes (10) | yes | yes | to learn |
| Double Dragon | `doubledr.json` | yes | yes | yes (14) | yes | yes | to learn |
| Dragon's Heaven | `dragonsh.json` | - | - | - | - | - | to learn |
| Fatal Fury | `fatfury1.json` | yes | yes | yes (14) | yes | - | RetroAchievements, to be checked |
| Fatal Fury 2 | `fatfury2.json` | yes | yes | yes (12) | yes | yes | RetroAchievements, checked on a recording |
| Fatal Fury 3 | `fatfury3.json` | yes | yes | yes (13) | yes | yes | RetroAchievements, to be checked |
| Fatal Fury Special | `fatfursp.json` | yes | yes | yes (12 of 16) | yes | yes | RetroAchievements, to be checked |
| Fight Fever | `fightfev.json` | yes | yes | yes (10) | yes | yes | to learn |
| Galaxy Fight | `galaxyfg.json` | yes | yes | yes (10) | yes | yes | RetroAchievements, checked on a recording |
| Garou | `garou.json` | yes | yes | yes (14) | yes | yes | RetroAchievements, to be checked |
| Kabuki Klash | `kabukikl.json` | yes | yes | yes (12) | yes | yes | to learn |
| Karnov's Revenge | `karnovr.json` | yes | yes | yes (14) | yes | - | RetroAchievements, checked on a recording |
| King of the Monsters | `kotm.json` | yes | - | - | - | - | to learn |
| King of the Monsters 2 | `kotm2.json` | yes | yes | yes (10) | - | - | to learn |
| Kizuna Encounter | `kizuna.json` | yes | yes | yes (13) | yes | yes | to learn |
| Legend of Success Joe | `legendos.json` | yes | - | - | - | - | to learn |
| Matrimelee | `matrim.json` | yes | yes | yes (16 of 20) | yes | yes | to learn |
| Ninja Master's | `ninjamas.json` | yes | yes | yes (12) | yes | yes | to learn |
| Rage of the Dragons | `rotd.json` | yes | yes | yes (16) | yes | yes | RetroAchievements, to be checked |
| Ragnagard | `ragnagrd.json` | yes | - | yes (12) | yes | yes | to learn |
| Real Bout Fatal Fury | `rbff1.json` | yes | yes | yes (16) | yes | yes | RetroAchievements, to be checked |
| Real Bout Fatal Fury 2 | `rbff2.json` | yes | yes | yes (23) | yes | yes | to learn |
| Real Bout Fatal Fury Special | `rbffspec.json` | yes | yes | yes (20) | yes | yes | RetroAchievements, to be checked |
| Samurai Shodown | `samsho.json` | yes | yes | yes (13) | yes | yes | RetroAchievements, to be checked |
| Samurai Shodown II | `samsho2.json` | yes | yes | yes (17) | yes | yes | yes |
| Samurai Shodown III | `samsho3.json` | yes | yes | yes (14) | yes | yes | to learn |
| Samurai Shodown IV | `samsho4.json` | yes | yes | yes (18) | yes | yes | to learn |
| Samurai Shodown V | `samsho5.json` | yes | yes | yes (28) | yes | yes | to learn |
| Samurai Shodown V Special | `samsh5sp.json` | yes | yes | yes (28) | yes | yes | to learn |
| Savage Reign | `savagere.json` | - | - | yes (12) | yes | yes | to learn |
| SNK vs. Capcom | `svc.json` | yes | yes | yes (36) | yes | yes | to learn |
| SNK vs. Capcom (JAMMA PCB) | `svcpcb.json` | yes | yes | yes (36) | yes | yes | to learn |
| The King of Fighters '94 | `kof94.json` | yes | yes | yes (26) | yes | yes | RetroAchievements, to be checked |
| The King of Fighters '95 | `kof95.json` | yes | yes | yes (26) | yes | yes | to learn |
| The King of Fighters '96 | `kof96.json` | yes | yes | yes (29) | yes | yes | assumed, to be checked |
| The King of Fighters '97 | `kof97.json` | yes | yes | yes (32) | yes | yes | found (1.33.1) |
| The King of Fighters '98 | `kof98.json` | yes | yes | yes (38) | yes | yes | found |
| The King of Fighters '99 | `kof99.json` | yes | yes | yes (34) | yes | yes | - (the game has no score) |
| The King of Fighters 2000 | `kof2000.json` | yes | yes | yes (36) | yes | yes | - (the game has no score) |
| The King of Fighters 2001 | `kof2001.json` | yes | yes | yes (42) | yes | yes | assumed, to be checked |
| The King of Fighters 2002 | `kof2002.json` | yes | yes | yes (41) | yes | yes | assumed, to be checked |
| The King of Fighters 2003 | `kof2003.json` | - | yes | yes (37) | yes | - | RetroAchievements, to be checked |
| The King of Fighters 2003 (Japan, JAMMA PCB) | `kf2k3pcb.json` | - | yes | - | - | - | to learn |
| The Last Blade | `lastblad.json` | yes | yes | yes (15) | yes | yes | RetroAchievements, to be checked |
| The Last Blade 2 | `lastbld2.json` | yes | yes | yes (20) | yes | yes | RetroAchievements, to be checked |
| Voltage Fighter Gowcaizer | `gowcaizr.json` | yes | yes | yes (12) | yes | yes | to learn |
| Waku Waku 7 | `wakuwak7.json` | yes | yes | yes (9) | yes | yes | RetroAchievements, checked on a recording |
| World Heroes | `wh1.json` | yes | yes | yes (9) | yes | yes | to learn |
| World Heroes 2 | `wh2.json` | yes | yes | yes (16) | yes | yes | to learn |
| World Heroes 2 Jet | `wh2j.json` | yes | yes | yes (17) | yes | yes | to learn |
| World Heroes Perfect | `whp.json` | yes | yes | yes (19) | yes | yes | to learn |

## Capcom fighting games

The 34 Capcom fighting games (Street Fighter II to III 3rd Strike, Alpha, Darkstalkers, Marvel vs. Capcom, X-Men...) fight on the stages of the game, with the super gauges under the fighters. See [[Capcom and Cave]].

## A fighting game that misbehaves

If ROUND, FIGHT !, K.O. or VS come at the wrong time, the capture of your game says why. See [[Recording a Game]].
