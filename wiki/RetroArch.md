ArcadeDMD reads games launched in RetroArch with no plugin. RetroArch shares the game memory through its "network commands", which stay on the PC itself.

## One-time setup

1. RetroArch 1.19 or newer (Information, System Information shows the version).
2. Settings, Network, turn on "Network Commands". Leave the port at 55355.
3. Leave "Pause Content When Not Active" on (Settings, User Interface). It is the default, and `learn.bat` uses it.
4. Start the game with a core that shares its memory (just below).

Nothing else to install. As soon as ArcadeDMD runs, it watches RetroArch by itself. The log says "RetroArch 1.19.x detected (network commands active)", then the core loaded for each game.

## The right core

Not every core gives RetroArch access to the game memory. With the wrong core, the scene shows but without any values.

| System | Core that works | Cores that don't |
|---|---|---|
| Arcade, Neo Geo, Capcom CPS1 to CPS3, Cave | Arcade (FinalBurn Neo), up to date | FB Alpha 2012 in all its forms, MAME 2003, MAME 2003-Plus, MAME 2010, MAME |
| Mega Drive (Sonic) | Genesis Plus GX, or PicoDrive | |

Installing FinalBurn Neo.

1. Main Menu, Online Updater, Core Downloader, "Arcade (FinalBurn Neo)". If Online Updater is hidden, turn it on in Settings, User Interface, Menu Item Visibility, Main Menu.
2. To try it, Main Menu, Load Core, Arcade (FinalBurn Neo), then Load Content and pick the game (`mslug.zip`, for example).
3. If the game refuses to start, a BIOS is most likely missing. Put a recent `neogeo.zip` next to the game.
4. If you launch your games from HyperSpin, RocketLauncher or LaunchBox, change the core chosen for this system there too.

## Supported games

| Game | RetroArch core | Shown right away | To learn |
|---|---|---|---|
| Metal Slug (`mslug`) | FinalBurn Neo | score of each player, lives, bombs, the grenades on screen, weapon and ammo, the rescued prisoners, the mission, the tank (in it or not, its energy and its shells) | nothing |
| Metal Slug 2 (`mslug2`) | FinalBurn Neo | score of each player, lives, bombs, the grenades on screen, weapon and ammo, the soldier chosen, the prisoners of the mission, the vehicle of each player (the vehicle's own address while riding anything, which one, its energy and its shells), the mission (RetroAchievements and the cheat database, the new values to be checked) | nothing |
| Metal Slug X (`mslugx`) | FinalBurn Neo | the score of each player, lives, bombs, the grenades on screen, weapon and ammo, the soldier chosen, the rescued prisoners, the vehicle of each player (its own address while riding anything, which one, its energy and its shells), the mission, the timer, the lives of all the enemies (the Iron Nokana MKII and the big ones get their bar), the game's own end flag and MISSION COMPLETE (test 44, from Seb's game) | player 2's values and the bosses of missions 2 to 6 by their lives, to confirm in play |
| Metal Slug 3 (`mslug3`) | FinalBurn Neo | the score of each player, lives, bombs, the grenades on screen, weapon and ammo, the soldier chosen, the rescued prisoners, the vehicle (which one), the mission, the lives of every enemy on screen (Huge Hermit, Sol Dae Rokker and the big enemies get their bar), the game's own MISSION COMPLETE in every mission (its end counter, test 46) | the vehicles' energy and missiles, the Camel Slug of mission 4, the bosses of missions 2, 3 and 5 by their lives |
| Metal Slug 6, the Metal Slug 3 bootleg (`mslug3b6`) | FinalBurn Neo | everything Metal Slug 3 reads, under the name Metal Slug 6, with its own mission count (it plays Metal Slug 3's missions in another order) and its handgun code (test 46, from Seb's two-player game) | the same as Metal Slug 3 |
| Metal Slug 4 (`mslug4`) | FinalBurn Neo | the score of each player, lives, bombs, the grenades on screen, weapon and ammo, the soldier chosen, the prisoners of the mission, in a vehicle or not and its energy, the mission, the lives of all the enemies (the boss among them, by phases) and the end of the mission (test 42, from Seb's two-player game) | which vehicle |
| Metal Slug 5 (`mslug5`) | FinalBurn Neo | the score of each player, lives, bombs, the grenades on screen, weapon and ammo, the soldier chosen, the rescued prisoners, the vehicle (which one) and its energy, the mission, the lives of all the enemies (the Metal Rear and the big ones get their bar), the game's own boss flag and MISSION COMPLETE (test 43, from Seb's two-player game) | the bosses of missions 2 to 5 by their lives |
| Twinkle Star Sprites (`twinspri`) | FinalBurn Neo | score, hearts (with the half ones), bombs, Pow gauge, character, chain and PERFECT of each player, the stage, where the game puts each player (his witch on the HD screen follows, test 47 from Seb's two-player game), the rounds won | nothing |
| The 57 Neo Geo fighting games (King of Fighters, Samurai Shodown, Fatal Fury, Last Blade, World Heroes...) | FinalBurn Neo | see [[Fighting Games]] | the score of the games the table below marks to learn |
| Blazing Star (`blazstar`), Puzzle Bobble (`pbobblen`), Shock Troopers (`shocktro`), Pulstar (`pulstar`), Magical Drop III (`magdrop3`), Sengoku 3 (`sengoku3`), Top Hunter (`tophuntr`), Last Resort (`lresort`), Aero Fighters 2 (`sonicwi2`), Aero Fighters 3 (`sonicwi3`), Strikers 1945 Plus (`s1945p`), Super Dodge Ball (`sdodgeb`), Neo Bomberman (`neobombe`), League Bowling (`lbowling`), Magician Lord (`maglord`), NAM-1975 (`nam1975`), Cyber-Lip (`cyberlip`), Ghost Pilots (`gpilots`), Alpha Mission II (`alpham2`), Viewpoint (`viewpoin`), Zed Blade (`zedblade`), Prehistoric Isle 2 (`preisle2`), Shock Troopers 2nd Squad (`shocktr2`), Robo Army (`roboarmy`), Burning Fight (`burningf`), Mutation Nation (`mutnat`), Sengoku (`sengoku`), Sengoku 2 (`sengoku2`), Ninja Combat (`ncombat`), Ninja Commando (`ncommand`), Blue's Journey (`bjourney`), Puzzle Bobble 2 (`pbobbl2n`), Magical Drop II (`magdrop2`), Money Puzzle Exchanger (`miexchng`), Puzzle De Pon! (`puzzledp`), Puzzle De Pon! R! (`puzzldpr`), Panic Bomber (`panicbom`), Pop 'n Bounce (`popbounc`), Super Bubble Pop (`sbp`), Spin Master (`spinmast`), Ganryu (`ganryu`), Zupapa! (`zupapa`), Neo Mr. Do! (`neomrdo`), Bang Bead (`bangbead`), Battle Flip Shot (`flipshot`), Gururin (`gururin`), Ghostlop (`ghostlop`), Pochi and Nyaa (`pnyaa`), Puzzled (`joyjoy`), Zintrick (`zintrckb`), Digger Man (`diggerma`), Andro Dunos (`androdun`), Captain Tomaday (`ctomaday`), Choutetsu Brikin'ger (`ironclad`), Last Hope (`lasthope`), Bang Bang Busters (`b2b`), Crossed Swords (`crsword`), Eight Man (`eightman`), Nightmare in the Dark (`nitd`), The Super Spy (`superspy`), Quiz King of Fighters (`quizkof`), Quiz Daisousa Sen (`quizdais`), Quiz Meitantei Neo & Geo (`quizdai2`), Chibi Maruko-chan Deluxe Quiz (`marukodq`) | FinalBurn Neo | see [[Neo Geo Games]] | score |
| Windjammers (`wjammers`), Neo Turf Masters (`turfmast`), Super Sidekicks 3 (`ssideki3`), The Ultimate 11 (`ssideki4`), Baseball Stars 2 (`bstars2`), Street Hoop (`strhoop`), Neo Drift Out (`neodrift`), Riding Hero (`ridhero`), Thrash Rally (`trally`), Super Sidekicks (`ssideki`), Super Sidekicks 2 (`ssideki2`), Tecmo World Soccer '96 (`twsoc96`), Goal! Goal! Goal! (`goalx3`), Neo-Geo Cup '98 (`neocup98`), Soccer Brawl (`socbrawl`), Football Frenzy (`fbfrenzy`), Pleasure Goal (`pgoal`), Baseball Stars Professional (`bstars`), 2020 Super Baseball (`2020bb`), Top Player's Golf (`tpgolf`), Power Spikes II (`pspikes2`), Over Top (`overtop`), Stakes Winner (`stakwin`), Stakes Winner 2 (`stakwin2`), Jockey Grand Prix (`jockeygp`), The Irritating Maze (`irrmaze`), Minasan no Okagesamadesu! (`minasan`), Mahjong Kyo Retsuden (`mahretsu`), Janshin Densetsu (`janshin`), Bakatonosama Mahjong Manyuuki (`bakatono`), Idol Mahjong Final Romance 2 (`froman2b`), Shougi no Tatsujin (`moshougi`) | FinalBurn Neo | see [[Neo Geo Games]] | nothing |
| All other Neo Geo games | FinalBurn Neo | scene by genre (credits with MAME) | score, and credits if the game keeps a copy of them |
| Every Capcom CPS1, CPS2 and CPS3 game | FinalBurn Neo | see [[Capcom and Cave]] | score |
| Sonic 1 and Sonic 2 | Genesis Plus GX | score, rings, lives | nothing |

The lives, bombs and ammo addresses come from the MAME 2003-Plus cheat database. Sonic's are the same as in MAME. Metal Slug lives follow the on-screen "1UP". Metal Slug 1 also counts the current life, so ArcadeDMD subtracts 1 (verified). Metal Slug 3 does not count it (verified). For 2 and X, ArcadeDMD does as for 1, and for 4 and 5 as for 3. If one of these games shows one life fewer than the screen, remove the `"add"` and `"min"` lines from its lives entry in its `games\mslugX.json` file. If it shows one more, add `"add": -1, "min": 0`.

With two players, the scene changes by itself as soon as player 2 presses Start. The Neo Geo BIOS tells who is in the game. At the top, as in the game, "1UP=" and player 1's lives on the left, "2UP=" and player 2's lives on the right, with the title scrolling between them. Below, each score sits under its 1UP or 2UP. A gray "SCORE ?" means that score has not been learned yet. At the bottom, each player's bombs and then weapon take turns, with "P1" in green and "P2" in yellow. If only player 2 is playing, the normal scene shows with player 2's values. Neo Geo credits can only be read with MAME (see [[Neo Geo Games]]).

The Metal Slug scenes are inspired by Vera's video, adapted to a 128x32 panel so that nothing ends up hidden behind the scenery. At the top, "SNK" in blue then "- METAL SLUG" (with the game number) in white scroll slowly. Below, "P1" in green and the score in white on the left, lives on the right. The next line alternates between the bombs, the weapon with its ammo (handgun, machine gun, shotgun, flamethrower, rocket launcher, laser, enemy chaser... a "+" marks the enhanced version) and, with MAME, the credits. At the very bottom, small hills and a small, dimmer tank that moves forward and fires when the score goes up.

The Metal Slug and Metal Slug 3 scores are already in their files, found with `learn.bat` under RetroArch and FinalBurn Neo. To replace the tank with your own drawing, drop `mslug_tank.gif` (or a `mslug_tank.png` strip of 3 frames) into `sprites\`. It must fit within 5 pixels in height, cannon facing right.

## Checking

Run `test_retroarch.bat` during a game. It shows the RetroArch version, the loaded core, the result of the memory read and the values read, and says what to do if something is wrong. The result is also saved to `runtime\test_retroarch.txt`. It also tells which game file a version, a bootleg or a hack takes.

## Credits and coins

RetroArch tells neither when a coin goes in nor through which slot, and FinalBurn Neo does not share the MVS backup memory where the Neo Geo keeps its credits. ArcadeDMD guesses them from the traces the Neo Geo BIOS leaves in the work RAM.

`coin_buttons.bat` makes it much better. Run it once, press the left coin button, the right one, player 1's START and player 2's START. ArcadeDMD then reads these buttons itself, on the controllers or the keyboard, at the same time as RetroArch and without taking them from it. It sees every coin and its side, during a game too, and every player who presses START.

- On the HD screen, the coin drops in the slot on the side where you put it.
- An MVS gives 2 credits for a coin in its second slot unless its settings were changed. ArcadeDMD counts the same, `"mvs_credits": [1, 2]` in the `coin_buttons` section. If you changed it in the MVS menu, put the same there, `[1, 1]` for example.
- While the RetroArch menu is open, the buttons move in the menu and ArcadeDMD counts no coin.
- If you plug your controllers into other USB ports, run `coin_buttons.bat` again, Windows may have changed their number.

## Recording

Under RetroArch, ArcadeDMD records each game (values, memory, screenshots) so that a game can be tuned without the cabinet. See [[Recording a Game]].

## Turning it off

`"enabled": false` in the `retroarch` section of `config.json`.

## Good to know

- A RetroArch game without a file in `games\` changes nothing on the Pixelcade (except with `"takeover": "all"`).
- In `config.json`, `retroarch` section, `"enabled": false` turns off the RetroArch monitoring.
- If the log says "RetroArch refuses to read the game memory", it is the core that does not expose it. The log says which core is loaded and what to do.
- **Captures of the fighting games** (since 1.33). During a game, every change of every value read is written with its time to `runtime\captures\<game>-<date>.log`, a few hundred KB for a match, with MAME as with RetroArch. One match per game (two rounds won, one lost, a super move) is enough to replay it in the fight engine without the game, tune the game's file (its select screens, the state of its fights, its round, its stocks) and keep the capture as a test. To report a fighting game whose ROUND, FIGHT !, K.O. or VS come at the wrong time, zip that folder and send it with a GitHub issue. `"capture"` in `config.json`: `"all"` (every game, the default), `"fights"` (the fighting games only) or `"off"`. `python tools\replay_capture.py runtime\captures\<file>` prints what the HD screen showed second by second, `--frames 30,47` draws it at those seconds. The captures already received are kept in `tests\captures` and replayed as tests: The King of Fighters '98 and '99, Fatal Fury, Windjammers, the Metal Slug games. To find where a game keeps what is not read yet (the life of a boss, the kind of a vehicle), the whole memory RetroArch shares is recorded for every game, four times a second as compressed differences, to `runtime\captures\<game>-<date>.ram` (`"ram_dump": {"enabled": true, "every": 0.25}` under `"retroarch"` in `config.json`, a few MB for ten minutes; `"ram_dump": true` in a game's file forces it for that game), and `python tools\ram_diff.py <file.ram> --down 120 160` lists the words that only go down between two moments (`--watch 0x1012AA` follows one, `--diff 118 121` shows what changed). To see what the screen showed when a byte moved, ArcadeDMD asks RetroArch for a screenshot (its `SCREENSHOT` command on the same port as the memory reads) at the first read, every two seconds while somebody plays and at once when a life, a mission, a vehicle or one of the game's flags changes (`"screenshots": {"enabled": true, "every": 2.0, "dir": ""}` under `"retroarch"`; set `"dir"` to RetroArch's `screenshot_directory` and the log says whether the first picture appeared). RetroArch's notification and flash for a screenshot are better off (Settings, On-Screen Display, On-Screen Notifications, Screenshot Notification and Screenshot Flash). A coin button held a good second sets a marker: `marker n` in the capture with its time, a screenshot, and a line in the log, to say "here" when something to look at happens (every coin press is in the capture too, `coin_press n`).
