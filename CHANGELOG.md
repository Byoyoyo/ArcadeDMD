# Changelog / Journal des versions

Newest version first. Each version is in English, then in French.
La version la plus récente en premier. Chaque version est en anglais, puis en français.

## 1.17.0

### English

**Neo Geo games done one by one**
- Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers and Neo Turf Masters now have a file of their own, with a panel scene and an animated HD scene made for each game. They are the first five, the best-known first. `PROGRESS.md` shows what comes next.
- Blazing Star. On the panel, the lives as small ships, ROUND and the shot power. On the HD screen, the ship flies above a big planet and fires, an enemy blows up when the score goes up, POWER UP, and ROUND with a burst of speed.
- Puzzle Bobble. On the panel, the bubble in the launcher and the next one, in their colors. On the HD screen, each bubble shot in the game leaves the launcher and sticks to a little board, and three of a color pop.
- Windjammers. On the panel, the points of the set with the timer in between, the court and the opponent's country. On the HD screen, the court of the game and the scoreboard. The disc flies into the goal with +3 or +5, or drops on the other side with +2.
- Shock Troopers. Energy, gun and ammo, special weapon. On the HD screen, a jungle at war with the shots and the grenades blowing up.
- Neo Turf Masters. Club and distance, stroke, power and wind. On the HD screen, a golf course where the wind pushes the clouds and the flag, and the ball flies to the green at each stroke.
- The score of Blazing Star, Puzzle Bobble and Shock Troopers is in no database. Learn it with `learn.bat`.
- When the stick and the buttons can be read (Neo Geo BIOS), the ship and the launcher follow them. Until the player touches them, the scene plays by itself.
- With nobody playing, the coin screen, as for the fighting games. GAME OVER when the game ends, CONTINUE ? during the countdown.
- `demo_neogeo.bat` shows these games with simulated values.

**HD screen**
- The animated backgrounds are 2 to 8 times faster to draw, for Metal Slug and the fighting games too.

**Game files**
- New panel elements, `icons` (a small drawing repeated for a value, such as lives), `dot` (a disk colored by a value, such as a bubble) and `arrow` (an arrow that turns with a value, such as the wind). See README section 8.
- `"names"` in `"derived"` can hold one list per language.
- The `"demo"` section can move the game's own values (`"sim"`), and `"attract": true` starts any game on the coin screen.

**Updating from 1.16**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un**
- Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers et Neo Turf Masters ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu. Ce sont les cinq premiers, les plus connus d'abord. `PROGRESS.md` montre ce qui vient ensuite.
- Blazing Star. Sur la dalle, les vies en petits vaisseaux, ROUND et la puissance du tir. Sur l'écran HD, le vaisseau vole au-dessus d'une grosse planète et tire, un ennemi explose quand le score monte, POWER UP, et ROUND avec une pointe de vitesse.
- Puzzle Bobble. Sur la dalle, la bulle dans le lanceur et la suivante, à leurs couleurs. Sur l'écran HD, chaque bulle tirée dans le jeu part du lanceur et colle à un petit plateau, et trois de la même couleur éclatent.
- Windjammers. Sur la dalle, les points du set avec le chrono entre les deux, le terrain et le pays de l'adversaire. Sur l'écran HD, le terrain du jeu et le tableau des scores. Le palet file dans le but avec +3 ou +5, ou tombe de l'autre côté avec +2.
- Shock Troopers. L'énergie, l'arme et ses munitions, l'arme spéciale. Sur l'écran HD, une jungle en guerre avec les tirs et les grenades qui explosent.
- Neo Turf Masters. Le club et sa distance, le coup, la puissance et le vent. Sur l'écran HD, un parcours de golf où le vent pousse les nuages et le drapeau, et la balle part vers le green à chaque coup.
- Le score de Blazing Star, Puzzle Bobble et Shock Troopers n'est dans aucune base. Apprends-le avec `learn.bat`.
- Quand le stick et les boutons se lisent (BIOS Neo Geo), le vaisseau et le lanceur les suivent. Tant que le joueur n'y touche pas, la scène joue toute seule.
- Quand personne ne joue, l'écran des pièces, comme pour les jeux de combat. GAME OVER quand la partie finit, CONTINUE ? pendant le compte à rebours.
- `demo_neogeo.bat` montre ces jeux avec des valeurs simulées.

**Écran HD**
- Les décors animés se dessinent 2 à 8 fois plus vite, pour les Metal Slug et les jeux de combat aussi.

**Fichiers de jeu**
- Nouveaux éléments de dalle, `icons` (un petit dessin répété selon une valeur, comme les vies), `dot` (un disque coloré selon une valeur, comme une bulle) et `arrow` (une flèche qui tourne selon une valeur, comme le vent). Voir la section 8 du README.
- `"names"` dans `"derived"` peut avoir une liste par langue.
- La section `"demo"` peut faire bouger les valeurs propres au jeu (`"sim"`), et `"attract": true` fait commencer n'importe quel jeu sur l'écran des pièces.

**Mettre à jour depuis la 1.16**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.16.0

### English

**Game logo when a game starts**
- When a game starts, its LaunchBox Clear Logo comes first. On the HD screen it arrives big with a flash and a light sweep, then glides to its place in the scene. On the Pixelcade and ZeDMD panels it zooms in on the LEDs. The Pixelcade shows it as soon as pixelweb has handed the panel over.
- New `"intro"` section in `config.json` (`"logo"`, `"seconds"`, `"launchbox"`), see README section 3.

**Coin screen for the fighting games**
- With nobody playing, the Neo Geo fighting games wait for a coin. On the panel, a € coin floats above a slot and drops into it when a coin is inserted, with +1 and the credit counter rolling, then PRESS START with a button.
- On the HD screen, two coin doors with a coin spinning above each one. An inserted coin drops into its slot with sparks, +1 and the counter rolling, then come the 1P and 2P START buttons.
- A coin only drops when the credits really go up. The game's own demo fights no longer set off sparks or K.O. on the HD screen.
- `"coin_symbol"` sets the symbol on the coins (€, $, £ or none). `sprites\insert_coin.gif` replaces the panel's coin screen with your own animation. `"coins": false` in the `preview` section brings back the plain INSERT COIN on the HD screen. See README section 7.

**Fighting scene on the panel**
- The top row is one pixel lower, so the accents stay visible.
- On the computer's side, the credits and PRESS START take turns.
- The timer sits in a frame, and the fighters' names are white.

**Other changes**
- `demo_fight.bat` starts on the coin screen. Two coins go in, then the fight begins (`"demo": {"attract": false}` in a game file skips it).
- HD screen, the arena backdrop no longer has bright dots on its spotlights.

**Updating from 1.15**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Logo du jeu au lancement**
- Quand un jeu démarre, son Clear Logo LaunchBox arrive d'abord. Sur l'écran HD, il entre en grand avec un éclair et un reflet, puis glisse à sa place dans la scène. Sur la Pixelcade et les dalles ZeDMD, il grandit sur les LED. La Pixelcade l'affiche dès que pixelweb lui a laissé la dalle.
- Nouvelle section `"intro"` dans `config.json` (`"logo"`, `"seconds"`, `"launchbox"`), voir la section 3 du README.

**Écran des pièces des jeux de combat**
- Quand personne ne joue, les jeux de combat Neo Geo attendent une pièce. Sur la dalle, une pièce € flotte au-dessus d'une fente et tombe dedans quand une pièce est mise, avec +1 et le compteur de crédits qui roule, puis PRESS START avec un bouton.
- Sur l'écran HD, deux monnayeurs avec une pièce qui tourne au-dessus de chacun. Une pièce mise tombe dans sa fente avec des étincelles, +1 et le compteur qui roule, puis arrivent les boutons START 1P et 2P.
- Une pièce ne tombe que quand les crédits montent vraiment. Les combats de démonstration du jeu ne déclenchent plus d'étincelles ni de K.O. sur l'écran HD.
- `"coin_symbol"` règle le symbole des pièces (€, $, £ ou aucun). `sprites\insert_coin.gif` remplace l'écran des pièces de la dalle par ta propre animation. `"coins": false` dans la section `preview` remet le simple INSERT COIN sur l'écran HD. Voir la section 7 du README.

**Scène de combat sur la dalle**
- La ligne du haut est un pixel plus bas, les accents restent visibles.
- Du côté de l'ordinateur, les crédits et PRESS START s'affichent tour à tour.
- Le chrono est dans un cadre, et les noms des combattants sont en blanc.

**Autres changements**
- `demo_fight.bat` commence sur l'écran des pièces. Deux pièces entrent, puis le combat commence (`"demo": {"attract": false}` dans un fichier de jeu le saute).
- Écran HD, le décor de l'arène n'a plus de points lumineux sur ses projecteurs.

**Mettre à jour depuis la 1.15**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.15.0

### English

**English and French**
- Everything is now in English, and switches to French by itself when Windows is in French. This covers the messages, `install.bat`, the learning tool, the test tools, the MAME plugin (messages and Tab menu), the words on the LED panel and the HD screen.
- To force a language, add `"language": "en"` or `"fr"` at the top of `config.json`. `"auto"` (the default) follows Windows.
- The texts of the scenes in `games\*.json` are now written in English and translated to French when drawn. Files written in French still work in both languages.

**New file names**
- `run.bat` (was `lancer.bat`), `learn.bat` (`apprendre.bat`), `install.bat` (`installer.bat`), `screen_setup.bat` (`ecran_dmd.bat`), `test_panel.bat` (`test_dalle.bat`), `demo_fight.bat` (`demo_combat.bat`).
- `config.default.json` (was `config.defaut.json`). Your `config.json` is kept.
- `learned\` (was `appris\`). The folder is moved by itself the first time ArcadeDMD starts.
- `README.md` in English and `README.fr.md` in French (was `LISEZMOI.md`).
- `install.bat` removes the old French-named files.

**HD screen (LCD marquee)**
- New Metal Slug scene. One soldier panel per player, shots in the style of each weapon, bombs that explode in the backdrop, a crate when a weapon is picked up, the helmet falling when a life is lost, LAST LIFE, rescued prisoners, coins, player 2 joining, CONTINUE and GAME OVER.
- Each Metal Slug mission has its own animated backdrop (jungle, desert, snowy mountain, city at war, harbor, enemy base), with MISSION COMPLETE and fireworks in between, and a slideshow of the backdrops when nobody plays.
- New fighting game effects. Sparks, combo counter, FIRST ATTACK, super moves, red heartbeat when health is low, exploding K.O., DOUBLE K.O., TIME UP, PERFECT, confetti for the winner, next King of Fighters fighter, FIGHT !
- Eight animated fighting backgrounds with a crowd (city at night, temple, harbor, ruins, arena, desert, snowy mountain, jungle).
- The background follows the game's stage. Addresses from the cheat databases for The King of Fighters '96 to 2000 and 2002, Garou, Fatal Fury 2 and Special, Real Bout Fatal Fury 2 and Special, Samurai Shodown II to IV, World Heroes and World Heroes Perfect, Rage of the Dragons, SNK vs. Capcom (JAMMA PCB), and the mission number of Metal Slug 1 and 2. They still have to be confirmed in game.
- Each game file chooses the background of each of its stages (`"hd": {"stages": [...]}`), see README section 3.
- Metal Slug games read the Neo Geo BIOS stick and buttons, so handgun shots and the backdrop scrolling follow the player. To be confirmed in game.

**Other changes**
- `demo_fight.bat` changes the stage every two K.O. The Metal Slug demo moves to the next mission every 25 seconds.
- `test_retroarch.bat` shows the stage, backdrop and mission values.
- The project is on GitHub. Each version comes with its zip on the Releases page.

**Updating from 1.14**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once. It updates the MAME plugin and removes the old files.

### Français

**Anglais et français**
- Tout est maintenant en anglais, et passe tout seul en français quand Windows est en français. C'est le cas des messages, de `install.bat`, de l'outil d'apprentissage, des outils de test, du plugin MAME (messages et menu Tab), des mots de la dalle LED et de l'écran HD.
- Pour forcer une langue, ajoute `"language": "en"` ou `"fr"` en haut de `config.json`. `"auto"` (par défaut) suit Windows.
- Les textes des scènes dans `games\*.json` sont maintenant écrits en anglais et traduits en français à l'affichage. Les fichiers écrits en français marchent toujours dans les deux langues.

**Nouveaux noms de fichiers**
- `run.bat` (ex `lancer.bat`), `learn.bat` (`apprendre.bat`), `install.bat` (`installer.bat`), `screen_setup.bat` (`ecran_dmd.bat`), `test_panel.bat` (`test_dalle.bat`), `demo_fight.bat` (`demo_combat.bat`).
- `config.default.json` (ex `config.defaut.json`). Ton `config.json` est gardé.
- `learned\` (ex `appris\`). Le dossier est déplacé tout seul au premier démarrage d'ArcadeDMD.
- `README.md` en anglais et `README.fr.md` en français (ex `LISEZMOI.md`).
- `install.bat` supprime les anciens fichiers aux noms français.

**Écran HD (marquee LCD)**
- Nouvelle scène Metal Slug. Un panneau de soldat par joueur, des tirs dans le style de chaque arme, des bombes qui explosent dans le décor, une caisse quand on ramasse une arme, le casque qui tombe quand on perd une vie, DERNIÈRE VIE, prisonniers libérés, pièces, arrivée du joueur 2, CONTINUE et GAME OVER.
- Chaque mission des Metal Slug a son décor animé (jungle, désert, montagne enneigée, ville en guerre, port, base ennemie), avec MISSION COMPLETE et un feu d'artifice entre les deux, et un diaporama des décors quand personne ne joue.
- Nouveaux effets des jeux de combat. Étincelles, compteur de combo, PREMIER COUP, super coups, battement de cœur rouge quand la vie est basse, K.O. qui explose, DOUBLE K.O., TIME UP, PERFECT, confettis pour le vainqueur, combattant suivant des King of Fighters, FIGHT !
- Huit décors de combat animés avec du public (ville la nuit, temple, port, ruines, arène, désert, montagne enneigée, jungle).
- Le décor suit le stage du jeu. Adresses tirées des bases de triche pour The King of Fighters '96 à 2000 et 2002, Garou, Fatal Fury 2 et Special, Real Bout Fatal Fury 2 et Special, Samurai Shodown II à IV, World Heroes et World Heroes Perfect, Rage of the Dragons, SNK vs. Capcom (JAMMA PCB), et le numéro de mission de Metal Slug 1 et 2. Elles restent à confirmer en jeu.
- Chaque fichier de jeu choisit le décor de chacun de ses stages (`"hd": {"stages": [...]}`), voir la section 3 du README.
- Les Metal Slug lisent le stick et les boutons par le BIOS Neo Geo, les tirs au pistolet et le défilement du décor suivent donc le joueur. À confirmer en jeu.

**Autres changements**
- `demo_fight.bat` change de stage tous les deux K.O. La démo Metal Slug passe à la mission suivante toutes les 25 secondes.
- `test_retroarch.bat` affiche les valeurs du stage, du décor et de la mission.
- Le projet est sur GitHub. Chaque version a son zip sur la page Releases.

**Mise à jour depuis la 1.14**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois. Il met à jour le plugin MAME et supprime les anciens fichiers.

## 1.14.0 and earlier / et avant

Versions released before the project moved to GitHub. Each one is a commit named after its version (ArcadeDMD 1.2 to ArcadeDMD 1.14.0) in the history of the main branch.

Versions publiées avant l'arrivée du projet sur GitHub. Chacune est un commit qui porte son numéro (ArcadeDMD 1.2 à ArcadeDMD 1.14.0) dans l'historique de la branche main.
