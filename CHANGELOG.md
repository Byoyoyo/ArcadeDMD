# Changelog / Journal des versions

Newest version first. Each version is in English, then in French.
La version la plus récente en premier. Chaque version est en anglais, puis en français.

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
