# Changelog / Journal des versions

Newest version first. Each version is in English, then in French.
La version la plus récente en premier. Chaque version est en anglais, puis en français.

To update, extract the new version over the old one. Your `config.json`, the addresses learned and your own pictures are kept.
Pour mettre à jour, extrais la nouvelle version par-dessus l'ancienne. Ton `config.json`, les adresses apprises et tes propres images sont gardés.

## 1.39.0

### English
- Neo Geo fighting games recognise the special moves done at the stick. When a button ends the motion of one of the fighter's moves, the panel under the name shows that move, lit, and how many times it was done. The move shown in turn lights its arrows as the stick does them. The marquee reads which side each fighter faces, so the arrows turn round when the fighters swap sides. 32 games, The King of Fighters '97, '98 and 2002 keeping their own panel.
- The robot. `robot_test.bat`, then `robot.bat`, let the games play by themselves through RetroArch, a few minutes each, so that ArcadeDMD records their memory with nobody at the cabinet. RetroArch's own settings are not changed.
- The cabinet's LEDs can follow the game through HyperHDR: a coin, a big blow, a K.O., a full gauge, a win, a boss warning. Off by default (`lights` in `config.json`). `test_lights.bat` plays every effect.

### Français
- Les jeux de combat Neo Geo reconnaissent les coups spéciaux faits au stick. Quand un bouton finit le geste d'un des coups du combattant, le panneau sous le nom montre ce coup, allumé, et le nombre de fois qu'il a été fait. Le coup montré à son tour allume ses flèches à mesure que le stick les fait. Le marquee lit de quel côté regarde chaque combattant, les flèches se retournent donc quand les combattants changent de côté. 32 jeux, The King of Fighters '97, '98 et 2002 gardant leur propre panneau.
- Le robot. `robot_test.bat`, puis `robot.bat`, font jouer les jeux tout seuls dans RetroArch, quelques minutes chacun, pour qu'ArcadeDMD enregistre leur mémoire sans personne devant la borne. Les réglages de RetroArch ne sont pas modifiés.
- Les LED de la borne peuvent suivre le jeu par HyperHDR : une pièce, un gros coup, un K.O., une jauge pleine, une victoire, l'alerte d'un boss. Coupé par défaut (`lights` dans `config.json`). `test_lights.bat` joue chaque effet.

## 1.38.0

### English
- Every fighting game shows its moves under a human player's name, as The King of Fighters '98 does. The special moves come one after another, their name, their arrows and their buttons, and the supers in gold when the game's gauge allows them. The moves of 70 games come from MAME's command list.
- The rounds won show as gold stars in every fighting game of single fighters, even when the game keeps no count of them. A match won says how many rounds to how many.
- Big blows hit harder on the marquee. The damage shows on the bar, and a blow the game empties over several frames counts as one, with its shock wave.
- Samurai Shodown II. The POW gauge under the fighter, POW MAX and its timer, and each fighter's weapon-breaking technique while it lasts. The winner's bar counted into the bonus no longer shows hits.
- Super Puzzle Fighter II Turbo. Player 2 stays a human, not CPU, when the loser of a VS game starts again.
- The marquee's window no longer closes on Esc or on a close sent by another program while ArcadeDMD's window and icon run. Any stop is written in the log, and the next start says when the run before ended without a word or crashed (runtime\crash.log).
- The Last Blade 2. The computer's fighter is named, the rounds won and the super gauge are read from the game, and the stage follows the game's.

### Français
- Tous les jeux de combat montrent leurs coups sous le nom d'un joueur humain, comme The King of Fighters '98. Les coups spéciaux défilent l'un après l'autre, leur nom, leurs flèches et leurs boutons, et les supers en or quand la jauge du jeu les permet. Les coups de 70 jeux viennent de la liste des commandes de MAME.
- Les rounds gagnés s'affichent en étoiles dorées dans tous les jeux de combat à un combattant, même quand le jeu ne les compte pas. Un match gagné dit combien de rounds à combien.
- Les gros coups frappent plus fort sur le marquee. Les dégâts s'affichent sur la barre, et un coup que le jeu vide en plusieurs images compte pour un, avec son onde de choc.
- Samurai Shodown II. La jauge POW sous le combattant, POW MAX et son chrono, et la technique de bris d'arme de chaque combattant tant qu'il dure. La barre du vainqueur décomptée dans le bonus ne montre plus de coups.
- Super Puzzle Fighter II Turbo. Le joueur 2 reste un humain, et non CPU, quand le perdant d'une partie VS rejoue.
- La fenêtre du marquee ne se ferme plus sur Échap ni sur une fermeture envoyée par un autre programme tant que la fenêtre et l'icône d'ArcadeDMD tournent. Tout arrêt est écrit dans le journal, et le démarrage suivant dit quand la fois d'avant s'est terminée sans prévenir ou a planté (runtime\crash.log).
- The Last Blade 2. Le combattant de l'ordinateur a son nom, les rounds gagnés et la jauge de super sont lus dans le jeu, et le décor suit celui du jeu.

## 1.37.0

### English
- ArcadeDMD gets a window and an icon near the clock, in place of the console. Status shows the game running, with the marquee and the LED panel live. Screens picks the marquee screen and the LED panel. Emulators checks RetroArch and the MAME plugin and fixes them in one click. Frontend picks where the logos come from. Log follows the log live.
- The game logos can come from RetroBat, from what its scraper downloaded.
- `run.bat` starts ArcadeDMD without a console and opens its window. `run_console.bat` keeps the console.
- The folders of the Emulators and Frontend tabs can be picked in Windows' own folder window (Browse).
- Mercs. The boss bar follows the whole boss, part after part like the game's, a mega crash included. The boss of mission 3 is announced, its guns no longer. The energy bar is full at the player's top life, which grows in the game.

### Français
- ArcadeDMD a une fenêtre et une icône près de l'horloge, à la place de la console. État montre le jeu en cours, avec le marquee et la dalle LED en direct. Écrans choisit l'écran du marquee et la dalle LED. Émulateurs vérifie RetroArch et le plugin MAME et les corrige d'un clic. Frontal choisit d'où viennent les logos. Journal suit le journal en direct.
- Les logos des jeux peuvent venir de RetroBat, de ce que son scraper a téléchargé.
- `run.bat` lance ArcadeDMD sans console et ouvre sa fenêtre. `run_console.bat` garde la console.
- Les dossiers des onglets Émulateurs et Frontal se choisissent dans la fenêtre de dossiers de Windows (Parcourir).
- Mercs. La barre du boss suit tout le boss, partie après partie comme celle du jeu, méga crash compris. Le boss de la mission 3 est annoncé, ses canons non. La barre d'énergie est pleine au maximum du joueur, qui grandit dans le jeu.

## 1.36.2

### English
- The marquee could stay empty at the first game after a long wait, until ArcadeDMD was started again. Its link to RetroArch could take RetroArch's own port while RetroArch was closed. It now always takes another one.
- No more 1P and 2P START buttons on the attract screen. With credits, PRESS START shows in big and the coin doors stay. On the LED panel, the coin floats over its slot.

### Français
- Le marquee pouvait rester vide au premier jeu après une longue attente, jusqu'à ce qu'on relance ArcadeDMD. Son lien avec RetroArch pouvait prendre le port de RetroArch pendant que RetroArch était fermé. Il en prend maintenant toujours un autre.
- Plus de boutons START 1P et 2P sur l'écran d'attente. Avec des crédits, PRESS START s'affiche en grand et les monnayeurs restent. Sur la dalle LED, la pièce flotte au-dessus de sa fente.

## 1.36.1

### English
- Marvel vs. Capcom shows on the HD screen a stage closer to the game's for five of its stages. The street of Metro City shows a city, Kazakhstan a palace with domes, the mountains above the clouds a desert, the Japanese bathhouse a Japanese market, the ruined city at night ruins.

### Français
- Marvel vs. Capcom affiche sur l'écran HD un décor plus proche du jeu pour cinq de ses décors. La rue de Metro City affiche une ville, le Kazakhstan un palais à dômes, les montagnes au-dessus des nuages un désert, les bains japonais un marché japonais, la ville en ruines la nuit des ruines.

## 1.36.0

### English
- Mercs gets an HD scene of its own, laid out like Metal Slug. The weapon held with its power level, the MEGA CRASH bombs, the energy, the time, bigger explosions, the boss announced with its life bar, and MISSION n.
- X-Men: Children of the Atom shows FIGHT! with the game's own. Under the full gauge, how to do each fighter's Hyper X, and its name in big when it goes off.
- Marvel vs. Capcom shows the Hyper Combos of the fighter on screen under the gauge, one after the other, and a big title each time a level is spent.
- Strikers 1945 Plus announces each mission and its boss, follows the boss's life and its shapes, then BOSS DESTROYED and MISSION COMPLETE. Its score is centred, and a plane taken from the reserve no longer shows -1 LIFE.
- The console window can no longer stop ArcadeDMD. A long stall is written in the log, with a file in `runtime` to find its cause.

### Français
- Mercs a sa propre scène HD, disposée comme Metal Slug. L'arme tenue et son niveau de puissance, les bombes MÉGA CRASH, l'énergie, le temps, des explosions plus fortes, le boss annoncé avec sa barre de vie, et MISSION n.
- X-Men: Children of the Atom affiche FIGHT ! en même temps que le jeu. Sous la jauge pleine, comment faire le Hyper X de chaque combattant, et son nom en grand quand il part.
- Marvel vs. Capcom affiche sous la jauge les Hyper Combos du combattant à l'écran, l'un après l'autre, et un grand titre à chaque niveau dépensé.
- Strikers 1945 Plus annonce chaque mission et son boss, suit la vie du boss et ses formes, puis BOSS DÉTRUIT et MISSION ACCOMPLIE. Son score est centré, et un avion sorti de la réserve n'affiche plus -1 VIE.
- La fenêtre de la console ne peut plus arrêter ArcadeDMD. Un long blocage est écrit dans le journal, avec un fichier dans `runtime` pour en trouver la cause.

## 1.35.0

### English
- Puzzle Bobble looks like the game: the blue machine around the boards, the purple checkered boards between their pillars.
- In VS, each player's wins are kept from one VS to the next, and the loser's bubbles turn black as in the game.
- Its score, round, bubble colours and player 2's arrow are confirmed.

### Français
- Puzzle Bobble ressemble au jeu, avec la machine bleue autour des plateaux et les plateaux à damier violet entre leurs piliers.
- En VS, les victoires de chaque joueur sont gardées d'un VS à l'autre, et les bulles du perdant noircissent comme dans le jeu.
- Son score, son round, la couleur des bulles et la flèche du joueur 2 sont confirmés.

## 1.34.0

### English
- Super Puzzle Fighter II Turbo gets a new HD scene built on the game's own wells, read gem by gem, face to face with VS, the next pairs and the rounds between them. Gems drop into place, bursts break into pieces and shake the screen, power gems shine as they form, counter gems fly to the other well and crash down there.
- The fuller a well, the faster its side of the marquee beats red, up to DANGER. The losing well collapses at the end of a round.
- Its score, who plays and the rounds are now read right, and two humans see the matches each one won.
- On the LED panel, both wells in small, their frames beating red as they fill.
- The MAME plugin reads lists of words too (the wells, the enemy tables of Metal Slug).
- Puzzle Bobble 2 keeps the VS wins of each player from match to match, with the trophies of the match under them.

### Français
- Super Puzzle Fighter II Turbo a une nouvelle scène HD construite sur les puits du jeu, lus gemme par gemme, face à face avec le VS, les paires suivantes et les manches entre eux. Les gemmes tombent à leur place, les explosions partent en morceaux et font trembler l'écran, les gemmes de puissance brillent en se formant, les gemmes à compteur volent vers l'autre puits et s'y écrasent.
- Plus un puits se remplit, plus son côté du marquee bat vite en rouge, jusqu'à DANGER. Le puits perdant s'effondre en fin de manche.
- Le score, qui joue et les manches sont maintenant bien lus, et deux humains voient les matchs gagnés par chacun.
- Sur la dalle LED, les deux puits en petit, leur cadre qui bat en rouge quand ils se remplissent.
- Le plugin MAME lit aussi les listes de mots (les puits, les tables d'ennemis de Metal Slug).
- Puzzle Bobble 2 garde les victoires VS de chaque joueur d'un match à l'autre, avec les trophées du match en dessous.

## 1.33.1

### English
- The King of Fighters '97 and 2002 get the desperation moves panel of '98, with their own commands, gauge and stocks. 2002 also reads MAX, its timer and the fighting order of each team.
- A desperation move gets its show on the HD screen. Its name fills the marquee, then flies above the bar while the hits are counted. The bar that takes them jolts, with a spark and pieces flying off.
- Metal Slug 6 (the Metal Slug 3 bootleg) is recognized, and Metal Slug 3 follows its mission 4.
- Twinkle Star Sprites places each witch where the game puts her and counts the rounds won.
- The documentation moves to the [wiki](https://github.com/Byoyoyo/ArcadeDMD/wiki), in English and in French. The README is now a short presentation.

### Français
- The King of Fighters '97 et 2002 ont le panneau des coups désespérés de '98, avec leurs propres commandes, leur jauge et leurs stocks. 2002 lit aussi le MAX, son chrono et l'ordre de combat de chaque équipe.
- Un coup désespéré a son spectacle sur l'écran HD. Son nom remplit le marquee, puis vole au-dessus de la barre pendant que les coups sont comptés. La barre touchée sursaute, avec une étincelle et des morceaux qui volent.
- Metal Slug 6 (le bootleg de Metal Slug 3) est reconnu, et Metal Slug 3 suit sa mission 4.
- Twinkle Star Sprites place chaque sorcière là où le jeu la met et compte les manches gagnées.
- La documentation passe dans le [wiki](https://github.com/Byoyoyo/ArcadeDMD/wiki/Accueil), en anglais et en français. Le README devient une courte présentation.

## 1.33.0

### English
- Each game played can be recorded, the values read and, with RetroArch, the game's memory and screenshots. One recorded game is enough to tune a game. See Recording a Game in the wiki.
- Metal Slug 1 to 5 and X are each tuned on a full game. The lives as the game counts them, the boss of mission 1 with its life bar, MISSION COMPLETE at the right moment, the vehicles of each player, the grenades, the laser as a beam.
- Your own pictures of the Metal Slug vehicles and soldiers can replace the drawings.
- The stages of The King of Fighters '98 in a cartoon style, and the fighters' names in cream with a black outline.
- The character select shows the fighters picked. Fixes for the select screens and the time over, and for KOF '99, KOF 2002 and Fatal Fury.
- Windjammers on the HD screen, with the disc and the players where the game puts them, the super shot, the sets, the match and a scoreboard with the flags.
- Puzzle Bobble 2 at the level of Puzzle Bobble.
- The Neo Geo credits under RetroArch follow the game better, coins inserted early or very fast included.

### Français
- Chaque partie jouée peut être enregistrée, les valeurs lues et, avec RetroArch, la mémoire du jeu et des captures d'écran. Une partie enregistrée suffit pour régler un jeu. Voir Enregistrer une partie dans le wiki.
- Metal Slug 1 à 5 et X sont chacun réglés sur une partie complète. Les vies comme le jeu les compte, le boss de la mission 1 avec sa barre de vie, MISSION COMPLETE au bon moment, les véhicules de chaque joueur, les grenades, le laser en rayon.
- Tes propres images des véhicules et des soldats de Metal Slug peuvent remplacer les dessins.
- Les décors de The King of Fighters '98 en style cartoon, et les noms des combattants en crème avec un contour noir.
- La sélection des personnages montre les combattants choisis. Corrections des écrans de sélection et du temps écoulé, et de KOF '99, KOF 2002 et Fatal Fury.
- Windjammers sur l'écran HD, avec le disque et les joueurs là où le jeu les met, le super tir, les sets, le match et un tableau des scores avec les drapeaux.
- Puzzle Bobble 2 au niveau de Puzzle Bobble.
- Les crédits Neo Geo sous RetroArch suivent mieux le jeu, y compris les pièces mises trop tôt ou très vite.

## 1.32.0

### English
- The King of Fighters '98 shows a desperation moves panel under each human player, with the commands, the gauge, the stocks and the inputs pressed. MAX as the game says it, in Advanced and in Extra.
- Two human players see the matches won by each one.
- ROUND and FIGHT ! come when the game shows them.
- The nine stages of The King of Fighters '98, drawn after the game's places, and darker under the fights.
- The stick and the buttons are read at every frame.

### Français
- The King of Fighters '98 montre un panneau des coups désespérés sous chaque joueur humain, avec les commandes, la jauge, les stocks et les touches appuyées. Le MAX comme le jeu le dit, en Advanced et en Extra.
- Deux joueurs humains voient les matchs gagnés par chacun.
- ROUND et FIGHT ! arrivent quand le jeu les montre.
- Les neuf décors de The King of Fighters '98, dessinés d'après les lieux du jeu, et plus sombres sous les combats.
- Le stick et les boutons sont lus à chaque image.

## 1.31.1

### English
- The K.O. of the fighting games. A health bar below zero reads empty, and the computer's health is read in more games.
- The rounds won are read in 13 more games, and the round number in more games.
- In The King of Fighters, FIGHT ! comes with the game's GO, and the end of a match and the fighters a team has lost are shown right.

### Français
- Le K.O. des jeux de combat. Une barre de vie sous zéro est vide, et la vie de l'ordinateur est lue dans plus de jeux.
- Les manches gagnées sont lues dans 13 jeux de plus, et le numéro du round dans plus de jeux.
- Dans The King of Fighters, FIGHT ! arrive avec le GO du jeu, et la fin d'un match et les combattants perdus par une équipe s'affichent juste.

## 1.31.0

### English
- Every Cave game is recognized, 37 games, with MAME and with RetroArch. `demo_cave.bat` shows them.
- DoDonPachi has a full HD scene, with the ship, the bombs, the stages and the boss of each stage with its life. The other Cave games get their own scene built on it.
- More values for the Neo Geo and Capcom games, from the MAME cheats and from RetroAchievements. 15 more games read their score.
- Puzzle Bobble shows both scores, the VS matches, the arrow and each bubble shot. Strikers 1945 Plus reads both scores and its super shot.
- The credits look the same in every HD scene. The Metal Slug grenade bounces and shakes the screen.
- `learn.bat` is faster on big memories and suggests the closest name when one is mistyped.

### Français
- Tous les jeux Cave sont reconnus, 37 jeux, avec MAME et avec RetroArch. `demo_cave.bat` les montre.
- DoDonPachi a une scène HD complète, avec le vaisseau, les bombes, les niveaux et le boss de chaque niveau avec sa vie. Les autres jeux Cave ont leur propre scène construite sur celle-ci.
- Plus de valeurs pour les jeux Neo Geo et Capcom, grâce aux codes de triche de MAME et à RetroAchievements. 15 jeux de plus lisent leur score.
- Puzzle Bobble montre les deux scores, les matchs VS, la flèche et chaque bulle tirée. Strikers 1945 Plus lit les deux scores et son super tir.
- Les crédits ont la même allure dans toutes les scènes HD. La grenade de Metal Slug rebondit et secoue l'écran.
- `learn.bat` est plus rapide sur les grosses mémoires et propose le nom le plus proche en cas de faute de frappe.

## 1.30.1

### English
- `coin_buttons.bat` also asks for the START buttons.
- The Capcom fighting games show player 2 and the computer on the right side, with super gauges and rounds won in more games.
- Metal Slug shows its tank, the prisoners freed, the mission and the timer. The credits are bigger.
- Twinkle Star Sprites has a new HD scene and the right hearts.
- `learn.bat` finds a stage, a mission or a round that the game counts from 0.

### Français
- `coin_buttons.bat` demande aussi les boutons START.
- Les jeux de combat Capcom montrent le joueur 2 et l'ordinateur du bon côté, avec les jauges de super et les manches gagnées dans plus de jeux.
- Metal Slug montre son tank, les prisonniers libérés, la mission et le chrono. Les crédits sont plus gros.
- Twinkle Star Sprites a une nouvelle scène HD et les bons cœurs.
- `learn.bat` trouve un stage, une mission ou un round que le jeu compte à partir de 0.

## 1.30.0

### English
- Every Capcom CPS1, CPS2 and CPS3 game is recognized, with MAME and with RetroArch. `demo_capcom.bat` shows them.
- The Capcom fighting games show their stage, with eight new stages drawn by the program, and the super gauges.
- Fifty Capcom games get a scene of their own, action games, shoot'em ups, puzzle games and quizzes.
- Under RetroArch, the coin buttons give the credits of the Capcom games.

### Français
- Tous les jeux Capcom CPS1, CPS2 et CPS3 sont reconnus, avec MAME et avec RetroArch. `demo_capcom.bat` les montre.
- Les jeux de combat Capcom montrent leur décor, avec huit nouveaux décors dessinés par le programme, et les jauges de super.
- Cinquante jeux Capcom ont leur propre scène, jeux d'action, shoot'em up, jeux de réflexion et quiz.
- Sous RetroArch, les boutons de pièce donnent les crédits des jeux Capcom.

## 1.29.3

### English
- Every Neo Geo set of FinalBurn Neo is recognized (693). A version, a bootleg or a hack takes the file of its original game.
- On the HD screen, each coin door says what a coin gives.

### Français
- Tous les jeux Neo Geo de FinalBurn Neo sont reconnus (693). Une version, un bootleg ou un hack prend le fichier de son jeu d'origine.
- Sur l'écran HD, chaque monnayeur dit ce que donne une pièce.

## 1.29.2

### English
- With RetroArch, `coin_buttons.bat` lets ArcadeDMD see every coin and its side. An MVS gives 2 credits for its second slot.
- `test_coins.bat` writes down each press of the coin buttons.

### Français
- Avec RetroArch, `coin_buttons.bat` fait voir à ArcadeDMD chaque pièce et son côté. Une MVS donne 2 crédits pour sa deuxième fente.
- `test_coins.bat` note chaque appui sur les boutons de pièce.

## 1.29.1

### English
- Fixes for the timer of the fighting games, the game title on the panel and the side of the coins with RetroArch.
- `test_coins.bat` writes down what the Neo Geo BIOS does when a coin goes in.

### Français
- Corrections du chrono des jeux de combat, du titre du jeu sur la dalle et du côté des pièces avec RetroArch.
- `test_coins.bat` note ce que fait le BIOS Neo Geo quand une pièce entre.

## 1.29.0

### English
- A simpler panel for the Neo Geo shoot'em ups. The score in big digits, your ship following your stick, and the events one at a time as on a pinball.
- The LED panel looks like the preview.
- The coin drops with RetroArch too.

### Français
- Une dalle plus simple pour les shoot'em up Neo Geo. Le score en gros chiffres, ton vaisseau qui suit le stick, et les événements un par un comme sur un flipper.
- La dalle LED ressemble au preview.
- La pièce tombe aussi avec RetroArch.

## 1.28.0

### English
- The Neo Geo shoot'em ups follow the game more closely. The enemies blow up when the game counts them, with the bombs and the bonus.
- Explosions drawn pixel by pixel on the panel. Your own animations (DOFLinx or Pixelcade GIFs) can replace ours.

### Français
- Les shoot'em up Neo Geo suivent le jeu de plus près. Les ennemis explosent quand le jeu les compte, avec les bombes et le bonus.
- Des explosions dessinées pixel par pixel sur la dalle. Tes propres animations (GIF de DOFLinx ou de la Pixelcade) peuvent remplacer les nôtres.

## 1.27.0

### English
- Twelve more Neo Geo games done one by one, Nightmare in the Dark, The Super Spy, four quizzes, five mahjong games and Shougi no Tatsujin. Ninety-seven games in all.

### Français
- Douze jeux Neo Geo de plus faits un par un, Nightmare in the Dark, The Super Spy, quatre quiz, cinq jeux de mahjong et Shougi no Tatsujin. Quatre-vingt-dix-sept jeux en tout.

## 1.26.0

### English
- Ten more Neo Geo games done one by one, Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords and Eight Man.

### Français
- Dix jeux Neo Geo de plus faits un par un, Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords et Eight Man.

## 1.25.0

### English
- Ten more Neo Geo games done one by one, Bang Bead, Battle Flip Shot, Over Top, Stakes Winner 1 and 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa and Puzzled.

### Français
- Dix jeux Neo Geo de plus faits un par un, Bang Bead, Battle Flip Shot, Over Top, Stakes Winner 1 et 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa et Puzzled.

## 1.24.0

### English
- Ten more Neo Geo games done one by one, the football, baseball, golf and volleyball games. Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf and Power Spikes II.

### Français
- Dix jeux Neo Geo de plus faits un par un, les jeux de foot, de baseball, de golf et de volley. Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf et Power Spikes II.

## 1.23.0

### English
- Ten more Neo Geo games done one by one, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks 1 and 2.

### Français
- Dix jeux Neo Geo de plus faits un par un, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks 1 et 2.

## 1.22.0

### English
- Ten more Neo Geo games done one by one, Mutation Nation, Sengoku 1 and 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger and Puzzle De Pon!.

### Français
- Dix jeux Neo Geo de plus faits un par un, Mutation Nation, Sengoku 1 et 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger et Puzzle De Pon!.

## 1.21.0

### English
- Ten more Neo Geo games done one by one, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army and Burning Fight.

### Français
- Dix jeux Neo Geo de plus faits un par un, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army et Burning Fight.

## 1.20.0

### English
- Ten more Neo Geo games done one by one, Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally and Magician Lord.

### Français
- Dix jeux Neo Geo de plus faits un par un, Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally et Magician Lord.

## 1.19.0

### English
- Five more Neo Geo games done one by one, Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2 and 3.
- On the HD screen, a new background appears without a jolt.

### Français
- Cinq jeux Neo Geo de plus faits un par un, Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2 et 3.
- Sur l'écran HD, un nouveau décor apparaît sans à-coup.

## 1.18.0

### English
- Five more Neo Geo games done one by one, Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11 and Sengoku 3.
- On the HD screen, the name of the stage under its banner, and no more freeze while a background is prepared.

### Français
- Cinq jeux Neo Geo de plus faits un par un, Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11 et Sengoku 3.
- Sur l'écran HD, le nom du stage sous sa bannière, et plus de blocage pendant la préparation d'un décor.

## 1.17.0

### English
- The first Neo Geo games done one by one, Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers and Neo Turf Masters, each with a panel scene and an animated HD scene. `demo_neogeo.bat` shows them.
- With nobody playing, these games also wait for a coin.
- The animated backgrounds are 2 to 8 times faster to draw.

### Français
- Les premiers jeux Neo Geo faits un par un, Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers et Neo Turf Masters, chacun avec une scène pour la dalle et une scène HD animée. `demo_neogeo.bat` les montre.
- Quand personne ne joue, ces jeux attendent aussi une pièce.
- Les décors animés se dessinent 2 à 8 fois plus vite.

## 1.16.0

### English
- The game's LaunchBox Clear Logo when a game starts.
- The coin screen of the Neo Geo fighting games, on the panel and on the HD screen. A coin inserted drops into its slot.
- The fight scene on the panel is easier to read.

### Français
- Le Clear Logo LaunchBox du jeu quand un jeu démarre.
- L'écran des pièces des jeux de combat Neo Geo, sur la dalle et sur l'écran HD. Une pièce mise tombe dans sa fente.
- La scène de combat de la dalle se lit plus facilement.

## 1.15.0

### English
- English and French. ArcadeDMD follows the language of Windows, or `"language"` in `config.json`.
- The files have English names (`run.bat`, `learn.bat`, `install.bat`...). Your `config.json` is kept and `learned\` is moved by itself.
- A new Metal Slug scene on the HD screen, with a backdrop for each mission.
- New fighting game effects and eight animated fighting backgrounds that follow the game's stage.

### Français
- Anglais et français. ArcadeDMD suit la langue de Windows, ou `"language"` dans `config.json`.
- Les fichiers ont des noms en anglais (`run.bat`, `learn.bat`, `install.bat`...). Ton `config.json` est gardé et `learned\` est déplacé tout seul.
- Une nouvelle scène Metal Slug sur l'écran HD, avec un décor pour chaque mission.
- De nouveaux effets pour les jeux de combat et huit décors de combat animés qui suivent le stage du jeu.

## 1.14.0 and earlier / et avant

Versions released before the project moved to GitHub. Each one is a commit named after its version (ArcadeDMD 1.2 to ArcadeDMD 1.14.0) in the history of the main branch.

Versions publiées avant l'arrivée du projet sur GitHub. Chacune est un commit qui porte son numéro (ArcadeDMD 1.2 à ArcadeDMD 1.14.0) dans l'historique de la branche main.
