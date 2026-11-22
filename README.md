# ArcadeDMD

En français, [README.fr.md](README.fr.md).

Live score, lives, credits and game events from MAME and RetroArch games, shown on the marquee of an arcade cabinet, with an animated scene for each game. On a 128x32 LED panel (**Pixelcade LED**, **ZeDMD**), or in smooth HD on an LCD marquee screen (a 1920 x 460 Vewlix marquee, for example).

**ArcadeDMD is in BETA.** How to install it, set it up and use it is in the **[wiki](https://github.com/Byoyoyo/ArcadeDMD/wiki)**, in English and in French.

[What it does](#what-it-does) · [The games in pictures](#the-games-in-pictures) · [Quick start](#quick-start) · [The wiki](#the-wiki)

![The King of Fighters '98 on an HD marquee, King's ILLUSION DANCE](wiki/images/kof98_desperation_move.gif)
![Metal Slug 3 on an HD marquee, BOSS DESTROYED and MISSION COMPLETE](wiki/images/metal_slug_3_mission_complete.gif)
![On the author's cabinet, K.O., PERFECT and WINNER on the marquee and in the game](wiki/images/cabinet_kof98_perfect.gif)
![The coin screen of the fighting games on an HD marquee](wiki/images/coin_screen_hd.gif)
![The same games on a 128 x 32 LED panel](wiki/images/led_reel.gif)

## What it does

- Reads the game memory live, with a MAME plugin or through RetroArch's network commands (FinalBurn Neo, Genesis Plus GX). Nothing in the game or the emulator is modified.
- Ready-made scenes for Metal Slug 1 to 5 and X, the 57 Neo Geo fighting games, ninety-seven Neo Geo games done one by one and every other Neo Geo game by genre, every Capcom CPS1, CPS2 and CPS3 game (34 fighting games on their own stages and fifty games done one by one, from Final Fight to 1944), every Cave game (37 games, DoDonPachi, Dai-Ou-Jou, Ketsui, Espgaluda, Mushihime-sama, Deathsmiles, Akai Katana...), After Burner II, Sonic 1 and 2.
- HD scenes with animated backgrounds that follow the game's stage or mission, and an effect for every event (hits, combos, K.O., weapons, bombs, coins...).
- The game's logo when it starts (your LaunchBox Clear Logo, or the logo RetroBat's scraper downloaded). With nobody playing, the fighting games wait for a coin. Insert one and it drops into the slot, the credits roll, then PRESS START.
- In the Neo Geo fighting games, each fighter's special moves show under the name and light up when done at the stick, and FIGHT ! comes with the game's own call.
- A robot lets the Neo Geo games play by themselves in RetroArch and records them, so that every game file is checked against a real game (`robot.bat`). The cabinet's LEDs can follow the game through HyperHDR.
- Everything is drawn by the program. Your own pictures can replace some drawings ([Your Own Pictures](https://github.com/Byoyoyo/ArcadeDMD/wiki/Your-Own-Pictures)).
- A learning tool finds the missing addresses (score, credits...) from a few captures.
- A window and an icon near the clock, in place of a console. The game running with the marquee and the LED panel live, the marquee screen picked among those Windows sees, RetroArch and the MAME plugin checked and fixed in one click, the frontend, the log.
- Works next to LaunchBox and BigBox, RetroBat, HyperSpin or any other frontend. English and French. Windows, Python 3.12 or newer.

## The window

ArcadeDMD runs near the clock. A click on its icon opens its window, with five tabs, Status, Screens, Emulators, Frontend and Log. See [Usage](https://github.com/Byoyoyo/ArcadeDMD/wiki/Usage).

![ArcadeDMD's window, The King of Fighters '98 running, the marquee and the LED panel live](docs/images/window_status_en.jpg)

## The games done with the most care

Every game has a scene, but these were tuned on a real cabinet, round after round, with videos, photos, logs of the games and, since 1.33, one game recorded whole (the values read, the game's memory, its screenshots, see [Recording a Game](https://github.com/Byoyoyo/ArcadeDMD/wiki/Recording-a-Game)), until the marquee follows the game to the moment. The games finished in 1.33, checked frame by frame against a recorded game, are The King of Fighters '98, the six Neo Geo Metal Slug games, Windjammers and Puzzle Bobble 2.

- **The King of Fighters '98.** Its nine stages drawn after the game's places, in a cartoon style, changing with the rounds as the game does, the select screen showing the picks. Under each player, his desperation moves with their commands, the arrows lighting up as the stick does them, RATÉ, DM ! and SDM !, the power gauge, the stocks and MAX as the game shows them. ROUND, FIGHT !, K.O., WIN, PERFECT, the next fighter entering, the team eliminated, and the matches won between two humans. See [Fighting Games](https://github.com/Byoyoyo/ArcadeDMD/wiki/Fighting-Games).
- **Metal Slug 1 to 5 and X.** All six, each tuned on one game recorded whole (1.33). The soldier chosen (Marco, Tarma, Eri, Fio...) beside J1 / J2, his weapon and ammo, the laser as a held beam, the bombs and the grenade that blows up when the game's does, the vehicles of each player (the tank, the camel, the Slugnoid, the Slug Flyer, the Slug Mariner, the Slug Gunner...) with their energy and shells, the lives as the game writes them, the prisoners freed, the lives of every enemy on screen, the boss of mission 1 of each game with WARNING, its name and its life bar (Tetsuyuki, The Keesi II, Iron Nokana MKII, Huge Hermit, Brave Guerrier, Metal Rear), BOSS DESTROYED and MISSION COMPLETE at the game's moment, the backdrops of each mission, the credits with the coin dropping in. The bosses of the later missions are recognised by their life and named after the game's list, to confirm in play.
- **Windjammers.** The game's court as a live map, the disc and the two players where the game puts them, read at every frame, the lobs, a super charging in a ring of flames then SUPER ! with the shot's name, the goals pushing the whole image into the wall, the sets and the match, the players named as in the game, the coins counted even when pressed very fast.
- **Puzzle Bobble and Puzzle Bobble 2.** Both scores, the bubble in the launcher and the next one in their colours, the arrow turning as the game's, each bubble shot leaving in its direction, the round, the VS matches and the rounds won.
- **DoDonPachi.** The score with the continues, the hit counter, the ship and its type, six stages drawn after the maps of the game, and the boss of each stage with its life read in the game, falling when it runs out.
- **Learned on a cabinet too.** Twinkle Star Sprites (its own scene, the hearts and chains), The King of Fighters 2002 and Fatal Fury (their select screens, rounds and teams read from recorded games), Marvel vs. Capcom, X-Men vs. Street Fighter, Marvel Super Heroes vs. Street Fighter, X-Men: Children of the Atom and Hyper Street Fighter II (scores, credits, the POWER gauge, the partners), Strikers 1945 Plus, Giga Wing and Mercs (scores, timer, SUPER SHOT).

The other games read the addresses of the cheat databases and of RetroAchievements, which still have to be confirmed in game. [PROGRESS.md](PROGRESS.md) says where each one stands.

## The games in pictures

The 155 Neo Geo games below, each on the HD marquee and, under it, on the 128 x 32 LED panel. Both are drawn by ArcadeDMD itself from a recorded game, with the game files of this version. Each family can be folded.

<details open>
<summary><b>Neo Geo fighting games</b> (54)</summary>

**3 Count Bout** (`3countb`). 8 fighters named, their moves under the name, moves recognised at the stick.

![3 Count Bout, the HD marquee and the LED panel](wiki/images/games/3countb.jpg)

**Aggressors of Dark Kombat** (`aodk`). Life bars, 7 stages.

![Aggressors of Dark Kombat, the HD marquee and the LED panel](wiki/images/games/aodk.jpg)

**Art of Fighting** (`aof`). Life bars, timer, 10 fighters named, their moves under the name, moves recognised at the stick, 10 stages, gauge.

![Art of Fighting, the HD marquee and the LED panel](wiki/images/games/aof.jpg)

**Art of Fighting 2** (`aof2`). Life bars, timer, 13 fighters named, their moves under the name, moves recognised at the stick, 12 stages, gauge.

![Art of Fighting 2, the HD marquee and the LED panel](wiki/images/games/aof2.jpg)

**Art of Fighting 3** (`aof3`). Life bars, timer, 10 fighters named, their moves under the name, moves recognised at the stick, 10 stages.

![Art of Fighting 3, the HD marquee and the LED panel](wiki/images/games/aof3.jpg)

**Breakers** (`breakers`). Life bars, timer, 9 fighters named, their moves under the name, moves recognised at the stick, 9 stages.

![Breakers, the HD marquee and the LED panel](wiki/images/games/breakers.jpg)

**Breakers Revenge** (`breakrev`). Life bars, timer, 10 fighters named, their moves under the name, moves recognised at the stick, 10 stages.

![Breakers Revenge, the HD marquee and the LED panel](wiki/images/games/breakrev.jpg)

**Double Dragon** (`doubledr`). Life bars, timer, 14 fighters named, their moves under the name, moves recognised at the stick, 6 stages.

![Double Dragon, the HD marquee and the LED panel](wiki/images/games/doubledr.jpg)

**Fatal Fury** (`fatfury1`). Life bars, timer, 14 fighters named, their moves under the name, moves recognised at the stick.

![Fatal Fury, the HD marquee and the LED panel](wiki/images/games/fatfury1.jpg)

**Fatal Fury 2** (`fatfury2`). Life bars, timer, 12 fighters named, their moves under the name, moves recognised at the stick, 12 stages.

![Fatal Fury 2, the HD marquee and the LED panel](wiki/images/games/fatfury2.jpg)

**Fatal Fury 3** (`fatfury3`). Life bars, timer, 13 fighters named, their moves under the name, moves recognised at the stick, 15 stages.

![Fatal Fury 3, the HD marquee and the LED panel](wiki/images/games/fatfury3.jpg)

**Fatal Fury Special** (`fatfursp`). Life bars, timer, 12 fighters named, their moves under the name, moves recognised at the stick, the game's stages.

![Fatal Fury Special, the HD marquee and the LED panel](wiki/images/games/fatfursp.jpg)

**Fight Fever** (`fightfev`). Life bars, timer, 10 fighters named, their moves under the name, moves recognised at the stick, 10 stages.

![Fight Fever, the HD marquee and the LED panel](wiki/images/games/fightfev.jpg)

**Galaxy Fight** (`galaxyfg`). Life bars, timer, 10 fighters named, their moves under the name, moves recognised at the stick, 9 stages.

![Galaxy Fight, the HD marquee and the LED panel](wiki/images/games/galaxyfg.jpg)

**Garou** (`garou`). Life bars, timer, 14 fighters named, their moves under the name, moves recognised at the stick, 14 stages, gauge.

![Garou, the HD marquee and the LED panel](wiki/images/games/garou.jpg)

**Kabuki Klash** (`kabukikl`). Life bars, timer, 12 fighters named, their moves under the name, moves recognised at the stick, 10 stages, gauge.

![Kabuki Klash, the HD marquee and the LED panel](wiki/images/games/kabukikl.jpg)

**Karnov's Revenge** (`karnovr`). Life bars, timer, 14 fighters named, their moves under the name, moves recognised at the stick.

![Karnov's Revenge, the HD marquee and the LED panel](wiki/images/games/karnovr.jpg)

**King of the Monsters** (`kotm`). Life bars.

![King of the Monsters, the HD marquee and the LED panel](wiki/images/games/kotm.jpg)

**King of the Monsters 2** (`kotm2`). Life bars, timer, 10 fighters named.

![King of the Monsters 2, the HD marquee and the LED panel](wiki/images/games/kotm2.jpg)

**Kizuna Encounter** (`kizuna`). Life bars, timer, 13 fighters named, their moves under the name, moves recognised at the stick, 10 stages.

![Kizuna Encounter, the HD marquee and the LED panel](wiki/images/games/kizuna.jpg)

**Legend of Success Joe** (`legendos`). Life bars.

![Legend of Success Joe, the HD marquee and the LED panel](wiki/images/games/legendos.jpg)

**Matrimelee** (`matrim`). Life bars, timer, 16 fighters named, their moves under the name, moves recognised at the stick, 9 stages.

![Matrimelee, the HD marquee and the LED panel](wiki/images/games/matrim.jpg)

**Ninja Master's** (`ninjamas`). Life bars, timer, 12 fighters named, their moves under the name, moves recognised at the stick, 12 stages, gauge.

![Ninja Master's, the HD marquee and the LED panel](wiki/images/games/ninjamas.jpg)

**Rage of the Dragons** (`rotd`). Life bars, timer, 16 fighters named, their moves under the name, moves recognised at the stick, 8 stages, gauge.

![Rage of the Dragons, the HD marquee and the LED panel](wiki/images/games/rotd.jpg)

**Ragnagard** (`ragnagrd`). Life bars, 12 fighters named, their moves under the name, moves recognised at the stick, 4 stages.

![Ragnagard, the HD marquee and the LED panel](wiki/images/games/ragnagrd.jpg)

**Real Bout Fatal Fury** (`rbff1`). Life bars, timer, 16 fighters named, their moves under the name, moves recognised at the stick, 13 stages, gauge.

![Real Bout Fatal Fury, the HD marquee and the LED panel](wiki/images/games/rbff1.jpg)

**Real Bout Fatal Fury 2** (`rbff2`). Life bars, timer, 23 fighters named, their moves under the name, moves recognised at the stick, 10 stages, gauge.

![Real Bout Fatal Fury 2, the HD marquee and the LED panel](wiki/images/games/rbff2.jpg)

**Real Bout Fatal Fury Special** (`rbffspec`). Life bars, timer, 20 fighters named, their moves under the name, moves recognised at the stick, 10 stages, gauge.

![Real Bout Fatal Fury Special, the HD marquee and the LED panel](wiki/images/games/rbffspec.jpg)

**Samurai Shodown** (`samsho`). Life bars, timer, 13 fighters named, their moves under the name, moves recognised at the stick, 12 stages.

![Samurai Shodown, the HD marquee and the LED panel](wiki/images/games/samsho.jpg)

**Samurai Shodown II** (`samsho2`). Life bars, timer, 17 fighters named, their moves under the name, moves recognised at the stick, 12 stages, gauge.

![Samurai Shodown II, the HD marquee and the LED panel](wiki/images/games/samsho2.jpg)

**Samurai Shodown III** (`samsho3`). Life bars, timer, 14 fighters named, their moves under the name, moves recognised at the stick, 3 stages, gauge.

![Samurai Shodown III, the HD marquee and the LED panel](wiki/images/games/samsho3.jpg)

**Samurai Shodown IV** (`samsho4`). Life bars, timer, 18 fighters named, their moves under the name, moves recognised at the stick, 12 stages, gauge.

![Samurai Shodown IV, the HD marquee and the LED panel](wiki/images/games/samsho4.jpg)

**Samurai Shodown V** (`samsho5`). Life bars, timer, 28 fighters named, their moves under the name, moves recognised at the stick, 15 stages, gauge.

![Samurai Shodown V, the HD marquee and the LED panel](wiki/images/games/samsho5.jpg)

**Samurai Shodown V Special** (`samsh5sp`). Life bars, timer, 28 fighters named, their moves under the name, moves recognised at the stick, 15 stages, gauge.

![Samurai Shodown V Special, the HD marquee and the LED panel](wiki/images/games/samsh5sp.jpg)

**Savage Reign** (`savagere`). 12 fighters named, their moves under the name, moves recognised at the stick, 5 stages.

![Savage Reign, the HD marquee and the LED panel](wiki/images/games/savagere.jpg)

**SNK vs. Capcom** (`svc`). Life bars, timer, 36 fighters named, their moves under the name, moves recognised at the stick, 8 stages.

![SNK vs. Capcom, the HD marquee and the LED panel](wiki/images/games/svc.jpg)

**The King of Fighters '94** (`kof94`). Life bars, timer, 26 fighters named, their moves under the name, moves recognised at the stick, 9 stages, gauge.

![The King of Fighters '94, the HD marquee and the LED panel](wiki/images/games/kof94.jpg)

**The King of Fighters '95** (`kof95`). Life bars, timer, 26 fighters named, their moves under the name, moves recognised at the stick, 9 stages, gauge.

![The King of Fighters '95, the HD marquee and the LED panel](wiki/images/games/kof95.jpg)

**The King of Fighters '96** (`kof96`). Life bars, timer, 29 fighters named, their moves under the name, moves recognised at the stick, 9 stages, gauge.

![The King of Fighters '96, the HD marquee and the LED panel](wiki/images/games/kof96.jpg)

**The King of Fighters '97** (`kof97`). Life bars, timer, 32 fighters named, desperation moves under the gauge, moves recognised at the stick, 6 stages.

![The King of Fighters '97, the HD marquee and the LED panel](wiki/images/games/kof97.jpg)

**The King of Fighters '98** (`kof98`). Life bars, timer, 38 fighters named, desperation moves under the gauge, moves recognised at the stick, 9 stages.

![The King of Fighters '98, the HD marquee and the LED panel](wiki/images/games/kof98.jpg)

**The King of Fighters '99** (`kof99`). Life bars, timer, 34 fighters named, their moves under the name, moves recognised at the stick, 6 stages.

![The King of Fighters '99, the HD marquee and the LED panel](wiki/images/games/kof99.jpg)

**The King of Fighters 2000** (`kof2000`). Life bars, timer, 36 fighters named, their moves under the name, moves recognised at the stick, 9 stages.

![The King of Fighters 2000, the HD marquee and the LED panel](wiki/images/games/kof2000.jpg)

**The King of Fighters 2001** (`kof2001`). Life bars, timer, 42 fighters named, their moves under the name, moves recognised at the stick, 6 stages.

![The King of Fighters 2001, the HD marquee and the LED panel](wiki/images/games/kof2001.jpg)

**The King of Fighters 2002** (`kof2002`). Life bars, timer, 41 fighters named, desperation moves under the gauge, moves recognised at the stick, 7 stages, gauge.

![The King of Fighters 2002, the HD marquee and the LED panel](wiki/images/games/kof2002.jpg)

**The King of Fighters 2003** (`kof2003`). Timer, 37 fighters named, their moves under the name, moves recognised at the stick.

![The King of Fighters 2003, the HD marquee and the LED panel](wiki/images/games/kof2003.jpg)

**The Last Blade** (`lastblad`). Life bars, timer, 15 fighters named, their moves under the name, moves recognised at the stick, 9 stages.

![The Last Blade, the HD marquee and the LED panel](wiki/images/games/lastblad.jpg)

**The Last Blade 2** (`lastbld2`). Life bars, timer, 20 fighters named, their moves under the name, moves recognised at the stick, 10 stages, gauge.

![The Last Blade 2, the HD marquee and the LED panel](wiki/images/games/lastbld2.jpg)

**Voltage Fighter Gowcaizer** (`gowcaizr`). Life bars, timer, 12 fighters named, their moves under the name, moves recognised at the stick, 12 stages.

![Voltage Fighter Gowcaizer, the HD marquee and the LED panel](wiki/images/games/gowcaizr.jpg)

**Waku Waku 7** (`wakuwak7`). Life bars, timer, 9 fighters named, their moves under the name, moves recognised at the stick, 6 stages.

![Waku Waku 7, the HD marquee and the LED panel](wiki/images/games/wakuwak7.jpg)

**World Heroes** (`wh1`). Life bars, timer, 9 fighters named, their moves under the name, moves recognised at the stick, 15 stages.

![World Heroes, the HD marquee and the LED panel](wiki/images/games/wh1.jpg)

**World Heroes 2** (`wh2`). Life bars, timer, 16 fighters named, their moves under the name, moves recognised at the stick, 15 stages.

![World Heroes 2, the HD marquee and the LED panel](wiki/images/games/wh2.jpg)

**World Heroes 2 Jet** (`wh2j`). Life bars, timer, 17 fighters named, their moves under the name, moves recognised at the stick, 21 stages.

![World Heroes 2 Jet, the HD marquee and the LED panel](wiki/images/games/wh2j.jpg)

**World Heroes Perfect** (`whp`). Life bars, timer, 19 fighters named, their moves under the name, moves recognised at the stick, 12 stages, gauge.

![World Heroes Perfect, the HD marquee and the LED panel](wiki/images/games/whp.jpg)

</details>

<details open>
<summary><b>Shoot'em ups</b> (15)</summary>

**Aero Fighters 2** (`sonicwi2`). Score, lives, bombs, power.

![Aero Fighters 2, the HD marquee and the LED panel](wiki/images/games/sonicwi2.jpg)

**Aero Fighters 3** (`sonicwi3`). Score, lives, bombs, power.

![Aero Fighters 3, the HD marquee and the LED panel](wiki/images/games/sonicwi3.jpg)

**Alpha Mission II** (`alpham2`). Score, lives, power.

![Alpha Mission II, the HD marquee and the LED panel](wiki/images/games/alpham2.jpg)

**Andro Dunos** (`androdun`). Score, lives.

![Andro Dunos, the HD marquee and the LED panel](wiki/images/games/androdun.jpg)

**Blazing Star** (`blazstar`). Score, lives, power.

![Blazing Star, the HD marquee and the LED panel](wiki/images/games/blazstar.jpg)

**Captain Tomaday** (`ctomaday`). Lives, power.

![Captain Tomaday, the HD marquee and the LED panel](wiki/images/games/ctomaday.jpg)

**Choutetsu Brikin'ger** (`ironclad`). Score, power.

![Choutetsu Brikin'ger, the HD marquee and the LED panel](wiki/images/games/ironclad.jpg)

**Ghost Pilots** (`gpilots`). Score, lives, bombs, power.

![Ghost Pilots, the HD marquee and the LED panel](wiki/images/games/gpilots.jpg)

**Last Resort** (`lresort`). Score, lives, power.

![Last Resort, the HD marquee and the LED panel](wiki/images/games/lresort.jpg)

**Prehistoric Isle 2** (`preisle2`). Score, lives, bombs, power.

![Prehistoric Isle 2, the HD marquee and the LED panel](wiki/images/games/preisle2.jpg)

**Pulstar** (`pulstar`). Score, lives, stage.

![Pulstar, the HD marquee and the LED panel](wiki/images/games/pulstar.jpg)

**Strikers 1945 Plus** (`s1945p`). Score, lives, bombs, power.

![Strikers 1945 Plus, the HD marquee and the LED panel](wiki/images/games/s1945p.jpg)

**Twinkle Star Sprites** (`twinspri`). Score, lives, bombs, power, stage.

![Twinkle Star Sprites, the HD marquee and the LED panel](wiki/images/games/twinspri.jpg)

**Viewpoint** (`viewpoin`). Score, lives.

![Viewpoint, the HD marquee and the LED panel](wiki/images/games/viewpoin.jpg)

**Zed Blade** (`zedblade`). Score, lives, bombs.

![Zed Blade, the HD marquee and the LED panel](wiki/images/games/zedblade.jpg)

</details>

<details open>
<summary><b>Run and gun</b> (11)</summary>

**Cyber-Lip** (`cyberlip`). Score, timer, lives.

![Cyber-Lip, the HD marquee and the LED panel](wiki/images/games/cyberlip.jpg)

**Metal Slug** (`mslug`). Score, timer, lives, bombs, mission.

![Metal Slug, the HD marquee and the LED panel](wiki/images/games/mslug.jpg)

**Metal Slug 2** (`mslug2`). Score, timer, lives, bombs, mission.

![Metal Slug 2, the HD marquee and the LED panel](wiki/images/games/mslug2.jpg)

**Metal Slug 3** (`mslug3`). Score, timer, lives, bombs, mission.

![Metal Slug 3, the HD marquee and the LED panel](wiki/images/games/mslug3.jpg)

**Metal Slug 4** (`mslug4`). Score, timer, lives, bombs, mission.

![Metal Slug 4, the HD marquee and the LED panel](wiki/images/games/mslug4.jpg)

**Metal Slug 5** (`mslug5`). Score, timer, lives, bombs, mission.

![Metal Slug 5, the HD marquee and the LED panel](wiki/images/games/mslug5.jpg)

**Metal Slug X** (`mslugx`). Score, timer, lives, bombs, mission.

![Metal Slug X, the HD marquee and the LED panel](wiki/images/games/mslugx.jpg)

**NAM-1975** (`nam1975`). Score.

![NAM-1975, the HD marquee and the LED panel](wiki/images/games/nam1975.jpg)

**Ninja Commando** (`ncommand`). Score, timer.

![Ninja Commando, the HD marquee and the LED panel](wiki/images/games/ncommand.jpg)

**Shock Troopers** (`shocktro`). Score, timer, energy, the soldier's name and his team, special weapon, stage and route, boss life bar.

![Shock Troopers, the HD marquee and the LED panel](wiki/images/games/shocktro.jpg)

**Shock Troopers 2nd Squad** (`shocktr2`). Score, timer, lives, energy, the soldier's name, the weapon and its power level, grenades, the second player, the mission and its name, the boss (ALERT, a bar for each part being shot at, BOSS DESTROYED), the vehicle.

![Shock Troopers 2nd Squad, the HD marquee and the LED panel](wiki/images/games/shocktr2.jpg)

</details>

<details open>
<summary><b>Action and platform games</b> (21)</summary>

**Bang Bang Busters** (`b2b`). Lives.

![Bang Bang Busters, the HD marquee and the LED panel](wiki/images/games/b2b.jpg)

**Blue's Journey** (`bjourney`). Score, timer, lives.

![Blue's Journey, the HD marquee and the LED panel](wiki/images/games/bjourney.jpg)

**Burning Fight** (`burningf`). Score, timer, lives.

![Burning Fight, the HD marquee and the LED panel](wiki/images/games/burningf.jpg)

**Crossed Swords** (`crsword`). Scene of its genre.

![Crossed Swords, the HD marquee and the LED panel](wiki/images/games/crsword.jpg)

**Digger Man** (`diggerma`). Lives, bombs.

![Digger Man, the HD marquee and the LED panel](wiki/images/games/diggerma.jpg)

**Eight Man** (`eightman`). Score, timer, lives, bombs.

![Eight Man, the HD marquee and the LED panel](wiki/images/games/eightman.jpg)

**Ganryu** (`ganryu`). Score, timer, lives.

![Ganryu, the HD marquee and the LED panel](wiki/images/games/ganryu.jpg)

**Magician Lord** (`maglord`). Lives, power.

![Magician Lord, the HD marquee and the LED panel](wiki/images/games/maglord.jpg)

**Mutation Nation** (`mutnat`). Score, bombs.

![Mutation Nation, the HD marquee and the LED panel](wiki/images/games/mutnat.jpg)

**Neo Bomberman** (`neobombe`). Lives, bombs, stage.

![Neo Bomberman, the HD marquee and the LED panel](wiki/images/games/neobombe.jpg)

**Neo Mr. Do!** (`neomrdo`). Score, lives.

![Neo Mr. Do!, the HD marquee and the LED panel](wiki/images/games/neomrdo.jpg)

**Nightmare in the Dark** (`nitd`). Score, timer, lives.

![Nightmare in the Dark, the HD marquee and the LED panel](wiki/images/games/nitd.jpg)

**Ninja Combat** (`ncombat`). Score, timer, lives, power.

![Ninja Combat, the HD marquee and the LED panel](wiki/images/games/ncombat.jpg)

**Robo Army** (`roboarmy`). Lives, bombs.

![Robo Army, the HD marquee and the LED panel](wiki/images/games/roboarmy.jpg)

**Sengoku** (`sengoku`). Score, lives.

![Sengoku, the HD marquee and the LED panel](wiki/images/games/sengoku.jpg)

**Sengoku 2** (`sengoku2`). Score, lives.

![Sengoku 2, the HD marquee and the LED panel](wiki/images/games/sengoku2.jpg)

**Sengoku 3** (`sengoku3`). Score, timer.

![Sengoku 3, the HD marquee and the LED panel](wiki/images/games/sengoku3.jpg)

**Spin Master** (`spinmast`). Score, lives, bombs.

![Spin Master, the HD marquee and the LED panel](wiki/images/games/spinmast.jpg)

**The Super Spy** (`superspy`). Score.

![The Super Spy, the HD marquee and the LED panel](wiki/images/games/superspy.jpg)

**Top Hunter - Roddy & Cathy** (`tophuntr`). Timer, lives, power.

![Top Hunter - Roddy & Cathy, the HD marquee and the LED panel](wiki/images/games/tophuntr.jpg)

**Zupapa!** (`zupapa`). Score, lives.

![Zupapa!, the HD marquee and the LED panel](wiki/images/games/zupapa.jpg)

</details>

<details open>
<summary><b>Sports games</b> (22)</summary>

**2020 Super Baseball** (`2020bb`). Timer.

![2020 Super Baseball, the HD marquee and the LED panel](wiki/images/games/2020bb.jpg)

**Bang Bead** (`bangbead`). Score, power.

![Bang Bead, the HD marquee and the LED panel](wiki/images/games/bangbead.jpg)

**Baseball Stars 2** (`bstars2`). Scene of its genre.

![Baseball Stars 2, the HD marquee and the LED panel](wiki/images/games/bstars2.jpg)

**Baseball Stars Professional** (`bstars`). Timer.

![Baseball Stars Professional, the HD marquee and the LED panel](wiki/images/games/bstars.jpg)

**Battle Flip Shot** (`flipshot`). Score, timer.

![Battle Flip Shot, the HD marquee and the LED panel](wiki/images/games/flipshot.jpg)

**Football Frenzy** (`fbfrenzy`). Scene of its genre.

![Football Frenzy, the HD marquee and the LED panel](wiki/images/games/fbfrenzy.jpg)

**Goal! Goal! Goal!** (`goalx3`). Timer.

![Goal! Goal! Goal!, the HD marquee and the LED panel](wiki/images/games/goalx3.jpg)

**League Bowling** (`lbowling`). Timer.

![League Bowling, the HD marquee and the LED panel](wiki/images/games/lbowling.jpg)

**Neo Turf Masters** (`turfmast`). Power.

![Neo Turf Masters, the HD marquee and the LED panel](wiki/images/games/turfmast.jpg)

**Neo-Geo Cup '98** (`neocup98`). Scene of its genre.

![Neo-Geo Cup '98, the HD marquee and the LED panel](wiki/images/games/neocup98.jpg)

**Pleasure Goal** (`pgoal`). Scene of its genre.

![Pleasure Goal, the HD marquee and the LED panel](wiki/images/games/pgoal.jpg)

**Power Spikes II** (`pspikes2`). Power.

![Power Spikes II, the HD marquee and the LED panel](wiki/images/games/pspikes2.jpg)

**Soccer Brawl** (`socbrawl`). Scene of its genre.

![Soccer Brawl, the HD marquee and the LED panel](wiki/images/games/socbrawl.jpg)

**Street Hoop** (`strhoop`). Scene of its genre.

![Street Hoop, the HD marquee and the LED panel](wiki/images/games/strhoop.jpg)

**Super Dodge Ball** (`sdodgeb`). Score, timer, power.

![Super Dodge Ball, the HD marquee and the LED panel](wiki/images/games/sdodgeb.jpg)

**Super Sidekicks** (`ssideki`). Scene of its genre.

![Super Sidekicks, the HD marquee and the LED panel](wiki/images/games/ssideki.jpg)

**Super Sidekicks 2** (`ssideki2`). Scene of its genre.

![Super Sidekicks 2, the HD marquee and the LED panel](wiki/images/games/ssideki2.jpg)

**Super Sidekicks 3 - The Next Glory** (`ssideki3`). Scene of its genre.

![Super Sidekicks 3 - The Next Glory, the HD marquee and the LED panel](wiki/images/games/ssideki3.jpg)

**Tecmo World Soccer '96** (`twsoc96`). Scene of its genre.

![Tecmo World Soccer '96, the HD marquee and the LED panel](wiki/images/games/twsoc96.jpg)

**The Ultimate 11 - The SNK Football Championship** (`ssideki4`). Power.

![The Ultimate 11 - The SNK Football Championship, the HD marquee and the LED panel](wiki/images/games/ssideki4.jpg)

**Top Player's Golf** (`tpgolf`). Timer.

![Top Player's Golf, the HD marquee and the LED panel](wiki/images/games/tpgolf.jpg)

**Windjammers** (`wjammers`). Score, timer.

![Windjammers, the HD marquee and the LED panel](wiki/images/games/wjammers.jpg)

</details>

<details open>
<summary><b>Racing games</b> (6)</summary>

**Neo Drift Out - New Technology** (`neodrift`). Timer.

![Neo Drift Out - New Technology, the HD marquee and the LED panel](wiki/images/games/neodrift.jpg)

**Over Top** (`overtop`). Timer.

![Over Top, the HD marquee and the LED panel](wiki/images/games/overtop.jpg)

**Riding Hero** (`ridhero`). Timer.

![Riding Hero, the HD marquee and the LED panel](wiki/images/games/ridhero.jpg)

**Stakes Winner** (`stakwin`). Scene of its genre.

![Stakes Winner, the HD marquee and the LED panel](wiki/images/games/stakwin.jpg)

**Stakes Winner 2** (`stakwin2`). Power.

![Stakes Winner 2, the HD marquee and the LED panel](wiki/images/games/stakwin2.jpg)

**Thrash Rally** (`trally`). Timer.

![Thrash Rally, the HD marquee and the LED panel](wiki/images/games/trally.jpg)

</details>

<details open>
<summary><b>Puzzle games</b> (16)</summary>

**Ghostlop** (`ghostlop`). Timer.

![Ghostlop, the HD marquee and the LED panel](wiki/images/games/ghostlop.jpg)

**Gururin** (`gururin`). Scene of its genre.

![Gururin, the HD marquee and the LED panel](wiki/images/games/gururin.jpg)

**Magical Drop II** (`magdrop2`). Scene of its genre.

![Magical Drop II, the HD marquee and the LED panel](wiki/images/games/magdrop2.jpg)

**Magical Drop III** (`magdrop3`). Scene of its genre.

![Magical Drop III, the HD marquee and the LED panel](wiki/images/games/magdrop3.jpg)

**Money Puzzle Exchanger** (`miexchng`). Scene of its genre.

![Money Puzzle Exchanger, the HD marquee and the LED panel](wiki/images/games/miexchng.jpg)

**Panic Bomber** (`panicbom`). Score, power.

![Panic Bomber, the HD marquee and the LED panel](wiki/images/games/panicbom.jpg)

**Pochi and Nyaa** (`pnyaa`). Score.

![Pochi and Nyaa, the HD marquee and the LED panel](wiki/images/games/pnyaa.jpg)

**Pop 'n Bounce** (`popbounc`). Lives.

![Pop 'n Bounce, the HD marquee and the LED panel](wiki/images/games/popbounc.jpg)

**Puzzle Bobble** (`pbobblen`). Score.

![Puzzle Bobble, the HD marquee and the LED panel](wiki/images/games/pbobblen.jpg)

**Puzzle Bobble 2** (`pbobbl2n`). Score.

![Puzzle Bobble 2, the HD marquee and the LED panel](wiki/images/games/pbobbl2n.jpg)

**Puzzle De Pon!** (`puzzledp`). Score, timer.

![Puzzle De Pon!, the HD marquee and the LED panel](wiki/images/games/puzzledp.jpg)

**Puzzle De Pon! R!** (`puzzldpr`). Score, timer.

![Puzzle De Pon! R!, the HD marquee and the LED panel](wiki/images/games/puzzldpr.jpg)

**Puzzled** (`joyjoy`). Scene of its genre.

![Puzzled, the HD marquee and the LED panel](wiki/images/games/joyjoy.jpg)

**Super Bubble Pop** (`sbp`). Score.

![Super Bubble Pop, the HD marquee and the LED panel](wiki/images/games/sbp.jpg)

**The Irritating Maze** (`irrmaze`). Timer, lives.

![The Irritating Maze, the HD marquee and the LED panel](wiki/images/games/irrmaze.jpg)

**Zintrick** (`zintrckb`). Timer.

![Zintrick, the HD marquee and the LED panel](wiki/images/games/zintrckb.jpg)

</details>

<details open>
<summary><b>Quiz, mahjong and shogi</b> (10)</summary>

**Bakatonosama Mahjong Manyuuki** (`bakatono`). Scene of its genre.

![Bakatonosama Mahjong Manyuuki, the HD marquee and the LED panel](wiki/images/games/bakatono.jpg)

**Chibi Maruko-chan Deluxe Quiz** (`marukodq`). Lives.

![Chibi Maruko-chan Deluxe Quiz, the HD marquee and the LED panel](wiki/images/games/marukodq.jpg)

**Idol Mahjong Final Romance 2** (`froman2b`). Scene of its genre.

![Idol Mahjong Final Romance 2, the HD marquee and the LED panel](wiki/images/games/froman2b.jpg)

**Janshin Densetsu** (`janshin`). Timer.

![Janshin Densetsu, the HD marquee and the LED panel](wiki/images/games/janshin.jpg)

**Mahjong Kyo Retsuden** (`mahretsu`). Scene of its genre.

![Mahjong Kyo Retsuden, the HD marquee and the LED panel](wiki/images/games/mahretsu.jpg)

**Minasan no Okagesamadesu!** (`minasan`). Scene of its genre.

![Minasan no Okagesamadesu!, the HD marquee and the LED panel](wiki/images/games/minasan.jpg)

**Quiz Daisousa Sen** (`quizdais`). Lives.

![Quiz Daisousa Sen, the HD marquee and the LED panel](wiki/images/games/quizdais.jpg)

**Quiz King of Fighters** (`quizkof`). Lives.

![Quiz King of Fighters, the HD marquee and the LED panel](wiki/images/games/quizkof.jpg)

**Quiz Meitantei Neo & Geo** (`quizdai2`). Lives.

![Quiz Meitantei Neo & Geo, the HD marquee and the LED panel](wiki/images/games/quizdai2.jpg)

**Shougi no Tatsujin** (`moshougi`). Scene of its genre.

![Shougi no Tatsujin, the HD marquee and the LED panel](wiki/images/games/moshougi.jpg)

</details>

<details open>
<summary><b>Capcom CPS1, CPS2 and CPS3, Cave</b></summary>

These scenes are drawn with simulated values, their games have not been recorded yet.

![Four Capcom fighting games on their stages](docs/images/hd_capcom_stages.jpg)

![Capcom beat'em ups](docs/images/hd_cps_beat_1.jpg)

![Capcom beat'em ups](docs/images/hd_cps_beat_2.jpg)

![Capcom beat'em ups](docs/images/hd_cps_beat_3.jpg)

![Capcom action games](docs/images/hd_cps_action_1.jpg)

![Capcom action games](docs/images/hd_cps_action_2.jpg)

![Capcom action games](docs/images/hd_cps_action_3.jpg)

![Capcom shooters](docs/images/hd_cps_shooters_1.jpg)

![Capcom shooters](docs/images/hd_cps_shooters_2.jpg)

![Capcom shooters](docs/images/hd_cps_shooters_3.jpg)

![Capcom puzzle, quiz and sports games](docs/images/hd_cps_small_1.jpg)

![Capcom puzzle, quiz and sports games](docs/images/hd_cps_small_2.jpg)

![DoDonPachi](docs/images/hd_dodonpachi.jpg)

![Twinkle Star Sprites](docs/images/hd_twinkle_star_sprites.jpg)

</details>
## Quick start

1. Download the zip of the latest version from the [Releases](../../releases/latest) page. Before extracting it, right-click it, choose Properties and tick "Unblock".
2. Extract the `ArcadeDMD` folder to a path with no accented characters, ideally `C:\ArcadeDMD`.
3. Run `install.bat`. It installs what is needed (Python 3.13 too if it is missing), copies the plugin into MAME and sets up the Pixelcade.
4. With an LCD marquee, run `screen_setup.bat`, or pick the screen later in the Screens tab of the window. With RetroArch, turn on "Network Commands" (Settings, Network) and play with the Arcade (FinalBurn Neo) core.
5. Run `demo_fight.bat` to see a scene without a game, then `run.bat`. Its icon sits near the clock and its window opens. Play from your frontend.

Every step in detail is in [Installation](https://github.com/Byoyoyo/ArcadeDMD/wiki/Installation), and what to do when something goes wrong in [Troubleshooting](https://github.com/Byoyoyo/ArcadeDMD/wiki/Troubleshooting).

## The wiki

| English | Français |
|---|---|
| [Home](https://github.com/Byoyoyo/ArcadeDMD/wiki/Home) | [Accueil](https://github.com/Byoyoyo/ArcadeDMD/wiki/Accueil) |
| [Installation](https://github.com/Byoyoyo/ArcadeDMD/wiki/Installation) | [Installer ArcadeDMD](https://github.com/Byoyoyo/ArcadeDMD/wiki/Installer-ArcadeDMD) |
| [Usage](https://github.com/Byoyoyo/ArcadeDMD/wiki/Usage) | [Utilisation](https://github.com/Byoyoyo/ArcadeDMD/wiki/Utilisation) |
| [Configuration](https://github.com/Byoyoyo/ArcadeDMD/wiki/Configuration) | [Réglages](https://github.com/Byoyoyo/ArcadeDMD/wiki/R%C3%A9glages) |
| [HD Marquee](https://github.com/Byoyoyo/ArcadeDMD/wiki/HD-Marquee) | [Marquee HD](https://github.com/Byoyoyo/ArcadeDMD/wiki/Marquee-HD) |
| [Pixelcade LED](https://github.com/Byoyoyo/ArcadeDMD/wiki/Pixelcade-LED) | [Dalle Pixelcade](https://github.com/Byoyoyo/ArcadeDMD/wiki/Dalle-Pixelcade) |
| [ZeDMD and Hardware](https://github.com/Byoyoyo/ArcadeDMD/wiki/ZeDMD-and-Hardware) | [ZeDMD et matériel](https://github.com/Byoyoyo/ArcadeDMD/wiki/ZeDMD-et-mat%C3%A9riel) |
| [OBS and DOFLinx](https://github.com/Byoyoyo/ArcadeDMD/wiki/OBS-and-DOFLinx) | [OBS et DOFLinx](https://github.com/Byoyoyo/ArcadeDMD/wiki/OBS-et-DOFLinx) |
| [MAME](https://github.com/Byoyoyo/ArcadeDMD/wiki/MAME) | [Avec MAME](https://github.com/Byoyoyo/ArcadeDMD/wiki/Avec-MAME) |
| [RetroArch](https://github.com/Byoyoyo/ArcadeDMD/wiki/RetroArch) | [Avec RetroArch](https://github.com/Byoyoyo/ArcadeDMD/wiki/Avec-RetroArch) |
| [Fighting Games](https://github.com/Byoyoyo/ArcadeDMD/wiki/Fighting-Games) | [Jeux de combat](https://github.com/Byoyoyo/ArcadeDMD/wiki/Jeux-de-combat) |
| [Metal Slug](https://github.com/Byoyoyo/ArcadeDMD/wiki/Metal-Slug) | [Les Metal Slug](https://github.com/Byoyoyo/ArcadeDMD/wiki/Les-Metal-Slug) |
| [Neo Geo Games](https://github.com/Byoyoyo/ArcadeDMD/wiki/Neo-Geo-Games) | [Jeux Neo Geo](https://github.com/Byoyoyo/ArcadeDMD/wiki/Jeux-Neo-Geo) |
| [Capcom and Cave](https://github.com/Byoyoyo/ArcadeDMD/wiki/Capcom-and-Cave) | [Capcom et Cave](https://github.com/Byoyoyo/ArcadeDMD/wiki/Capcom-et-Cave) |
| [Other Games](https://github.com/Byoyoyo/ArcadeDMD/wiki/Other-Games) | [Autres jeux](https://github.com/Byoyoyo/ArcadeDMD/wiki/Autres-jeux) |
| [Games in Pictures](https://github.com/Byoyoyo/ArcadeDMD/wiki/Games-in-Pictures) | [Les jeux en images](https://github.com/Byoyoyo/ArcadeDMD/wiki/Les-jeux-en-images) |
| [Learning Addresses](https://github.com/Byoyoyo/ArcadeDMD/wiki/Learning-Addresses) | [Apprendre les adresses](https://github.com/Byoyoyo/ArcadeDMD/wiki/Apprendre-les-adresses) |
| [Recording a Game](https://github.com/Byoyoyo/ArcadeDMD/wiki/Recording-a-Game) | [Enregistrer une partie](https://github.com/Byoyoyo/ArcadeDMD/wiki/Enregistrer-une-partie) |
| [Game Files](https://github.com/Byoyoyo/ArcadeDMD/wiki/Game-Files) | [Fichiers des jeux](https://github.com/Byoyoyo/ArcadeDMD/wiki/Fichiers-des-jeux) |
| [Your Own Pictures](https://github.com/Byoyoyo/ArcadeDMD/wiki/Your-Own-Pictures) | [Tes propres images](https://github.com/Byoyoyo/ArcadeDMD/wiki/Tes-propres-images) |
| [Troubleshooting](https://github.com/Byoyoyo/ArcadeDMD/wiki/Troubleshooting) | [Dépannage](https://github.com/Byoyoyo/ArcadeDMD/wiki/D%C3%A9pannage) |

## Following the project

What changed in each version is in [CHANGELOG.md](CHANGELOG.md), where each game stands and what comes next in [PROGRESS.md](PROGRESS.md). To report a problem or ask for a new game, see [CONTRIBUTING.md](CONTRIBUTING.md). A game recorded on your cabinet helps the most ([Recording a Game](https://github.com/Byoyoyo/ArcadeDMD/wiki/Recording-a-Game)).

## Licenses and credits

ArcadeDMD is © 2026 Byoyoyo. From version 1.39.1 it is free for personal, non-commercial use: you may install it on your own cabinets and modify it for yourself. Selling it, any commercial use and redistributing it need the author's agreement (`LICENSE` file). The versions up to 1.39.0 stay under the MIT license. The bitmap fonts come from the X11 "misc-fixed" fonts (public domain). The HD fonts are Inter (The Inter Project Authors) and Black Ops One (The Black-Ops Project Authors), both under the SIL Open Font License, see the `fonts` folder. The sprites, the HD backgrounds and the effects are drawn by the program or for it, no image comes from a game. ZeDMD (GPLv2 firmware) and libzedmd (GPLv3) are downloaded separately from their official repositories https://github.com/PPUC. Game names are used only to identify the games. The addresses come from the community cheat databases (FinalBurn Neo, MAME 2003-Plus), peon2's training scripts and the Sonic disassemblies, with thanks to their authors.

Byoyoyo had wanted to build ArcadeDMD for a long time, and started it after his exchanges with Vera AI. Thanks to Vera AI for those exchanges.
