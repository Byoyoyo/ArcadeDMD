# Changelog / Journal des versions

Newest version first. Each version is in English, then in French.
La version la plus récente en premier. Chaque version est en anglais, puis en français.

## 1.30.1

### English

**The START buttons**
- `coin_buttons.bat` now also asks for the START button of each player. In a game that does not give its credits (most Capcom games under RetroArch, Mercs, Final Fight, Street Fighter II', the Alpha series...), a player who presses START with a credit begins at once. The game shows from the select screen or the intro on, PRESS START no longer waits until the player has control. Player 2 who presses START takes his credit too, a challenger in a fighting game included. Nothing is counted for START pressed without a credit, during a game or in RetroArch's menu.

**Capcom games**
- Player 2 of the fighting games. PRESS START and CPU stayed on his side even when a second player came in. Street Fighter Alpha, Alpha 3, Marvel vs. Capcom, Vampire Hunter 2 and JoJo's Bizarre Adventure read who controls each fighter, a human or the computer (cheat database), and so do Marvel Super Heroes vs. Street Fighter and X-Men vs. Street Fighter (found in captures made on a cabinet). In the other fighting games, player 2 is seen as he comes in, his score going up once it is learned, his START with a credit, or a credit spent during a fight (a challenger). He leaves when nobody plays any more, or two minutes after his score stopped moving.
- Player 2 who plays alone against the computer. Player 1 shows as CPU, with PRESS START or INSERT COIN above him, and his score is no longer the computer's. The games above read it, the others see it from player 2's START followed by a credit the game spends. Player 1 who comes in afterwards plays again.
- In the Marvel games (X-Men: Children of the Atom, Marvel Super Heroes and the three "vs.") the computer scores too. A score going up no longer makes player 2 a human there.
- Hyper Street Fighter II, Marvel vs. Capcom, X-Men: Children of the Atom, Marvel Super Heroes vs. Street Fighter and X-Men vs. Street Fighter read the score of each player, learned on a cabinet.
- The super gauge of Marvel vs. Capcom, Marvel Super Heroes, X-Men vs. Street Fighter and X-Men: Children of the Atom works like the game's. The bar of the current level, with LEVEL 1, 2 or 3 beside it, and MAX at the top level (LEVEL MAX in X-Men: Children of the Atom, like the game). It showed the level as a third of the bar, X-Men's stayed empty at Level 1.
- Marvel vs. Capcom reads its credits, learned on a cabinet. Two coins for a credit is counted right.
- Marvel vs. Capcom, Marvel Super Heroes vs. Street Fighter and X-Men vs. Street Fighter give each player two fighters who take turns. The health and the name shown are those of the fighter on screen, and a partner who comes in is no longer a K.O. Two empty bars and a DOUBLE K.O. came in the middle of a fight.
- The empty part of the health bars on the HD screen is dark grey instead of dark red, in every fighting game. A nearly empty bar looked full and red on the cabinet (X-Men: Children of the Atom).
- Night Warriors reads the rounds won by each player (cheat database). Gold stars under the bars on the HD screen, gold squares next to the timer on the panel, and the winner of each round from them.
- The health of Magic Sword, Willow and Tenchi wo Kurau II reads empty when it goes below zero, like in the other Capcom games since 1.30.0.
- A version whose own cheats put its values elsewhere reads them there. The second revision of JoJo's Venture (all its values), Quiz & Dragons' Japanese resale (the lives) and the US Eco Fighters (the credits) read their parent's addresses until now.

**Neo Geo**
- The credits of a Neo Geo under RetroArch, guessed from its BIOS, start from those left the last time the game was quit. FinalBurn Neo keeps them in the game's backup memory and gives them back, ArcadeDMD guessed only one. Metal Slug showed one credit less than the game on a cabinet. The guess is no longer lost either when the game comes back after RetroArch's menu was open a while.

**Updating from 1.30.0**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept). Then run `coin_buttons.bat` once more and press the left coin button, the right one, then START for player 1 and START for player 2.

### Français

**Les boutons START**
- `coin_buttons.bat` demande maintenant aussi le bouton START de chaque joueur. Dans un jeu qui ne donne pas ses crédits (la plupart des jeux Capcom sous RetroArch, Mercs, Final Fight, Street Fighter II', les Alpha...), un joueur qui appuie sur START avec un crédit commence tout de suite. Le jeu s'affiche dès l'écran de sélection ou l'intro, PRESS START n'attend plus que le joueur ait le contrôle. Le joueur 2 qui appuie sur START prend aussi son crédit, un challenger dans un jeu de combat compris. Rien n'est compté pour un START appuyé sans crédit, en pleine partie ou dans le menu de RetroArch.

**Jeux Capcom**
- Le joueur 2 des jeux de combat. PRESS START et CPU restaient affichés de son côté même quand un deuxième joueur arrivait. Street Fighter Alpha, Alpha 3, Marvel vs. Capcom, Vampire Hunter 2 et JoJo's Bizarre Adventure lisent qui dirige chaque combattant, un humain ou l'ordinateur (base de triche), Marvel Super Heroes vs. Street Fighter et X-Men vs. Street Fighter aussi (trouvé dans des captures faites sur une borne). Dans les autres jeux de combat, le joueur 2 est vu quand il arrive, son score qui monte une fois appris, son START avec un crédit, ou un crédit dépensé en plein combat (un challenger). Il repart quand plus personne ne joue, ou deux minutes après que son score a cessé de bouger.
- Le joueur 2 qui joue seul contre l'ordinateur. Le joueur 1 s'affiche CPU, avec PRESS START ou INSERT COIN au-dessus, et son score n'est plus celui de l'ordinateur. Les jeux ci-dessus le lisent, les autres le voient au START du joueur 2 suivi d'un crédit que le jeu dépense. Le joueur 1 qui arrive ensuite rejoue.
- Dans les jeux Marvel (X-Men: Children of the Atom, Marvel Super Heroes et les trois « vs. ») l'ordinateur marque aussi des points. Un score qui monte ne fait plus du joueur 2 un humain dans ces jeux.
- Hyper Street Fighter II, Marvel vs. Capcom, X-Men: Children of the Atom, Marvel Super Heroes vs. Street Fighter et X-Men vs. Street Fighter lisent le score de chaque joueur, appris sur une borne.
- La jauge de super de Marvel vs. Capcom, Marvel Super Heroes, X-Men vs. Street Fighter et X-Men: Children of the Atom marche comme celle du jeu. La barre du niveau en cours, avec NIVEAU 1, 2 ou 3 à côté, et MAX au niveau le plus haut (NIVEAU MAX dans X-Men: Children of the Atom, comme le jeu). Elle montrait le niveau en tiers de barre, et celle de X-Men restait vide au Level 1.
- Marvel vs. Capcom lit ses crédits, appris sur une borne. Deux pièces pour un crédit sont bien comptées.
- Marvel vs. Capcom, Marvel Super Heroes vs. Street Fighter et X-Men vs. Street Fighter donnent à chaque joueur deux combattants qui se relaient. La vie et le nom affichés sont ceux du combattant à l'écran, et un partenaire qui prend la suite n'est plus un K.O. Deux barres vides et un DOUBLE K.O. arrivaient en plein combat.
- La partie vide des barres de vie sur l'écran HD est gris foncé au lieu de rouge foncé, dans tous les jeux de combat. Une barre presque vide paraissait pleine et rouge sur la borne (X-Men: Children of the Atom).
- Night Warriors lit les rounds gagnés par chaque joueur (base de triche). Des étoiles dorées sous les barres sur l'écran HD, des carrés dorés à côté du chrono sur la dalle, et le vainqueur de chaque round d'après eux.
- La vie de Magic Sword, Willow et Tenchi wo Kurau II se lit vide quand elle passe sous zéro, comme dans les autres jeux Capcom depuis la 1.30.0.
- Une version dont les propres codes de triche mettent ses valeurs ailleurs les lit là. La deuxième révision de JoJo's Venture (toutes ses valeurs), la réédition japonaise de Quiz & Dragons (les vies) et Eco Fighters américain (les crédits) lisaient jusqu'ici les adresses de leur jeu d'origine.

**Neo Geo**
- Les crédits d'une Neo Geo sous RetroArch, devinés d'après son BIOS, repartent de ceux qui restaient la dernière fois qu'on a quitté le jeu. FinalBurn Neo les garde dans la mémoire de sauvegarde du jeu et les rend, ArcadeDMD n'en devinait qu'un. Metal Slug affichait un crédit de moins que le jeu sur une borne. La devinette n'est plus perdue non plus quand le jeu revient après un moment dans le menu de RetroArch.

**Mettre à jour depuis la 1.30.0**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés). Relance ensuite une fois `coin_buttons.bat` et appuie sur le bouton des pièces de gauche, celui de droite, puis sur START du joueur 1 et START du joueur 2.

## 1.30.0

### English

**Every Capcom CPS1, CPS2 and CPS3 game**
- Every Capcom CPS1, CPS2 and CPS3 game of FinalBurn Neo is recognized, with MAME as with RetroArch. That makes 88 games and their 942 sets. A version, a bootleg or a hack takes the file of its original game, with its own name when it has one.
- The values of the cheat database of FinalBurn Neo are read, each player's health, the timer, the lives, the bombs, the super gauge, the characters and their names, the stage, and the credits when the game keeps them. The timer shows when the cheat gives all of it. In 23 games it only gives a part (one digit, the seconds of a clock, a counter that is not the timer seen in the game), ArcadeDMD then reads it only to see that the game runs. The RAM of the CPS3, whose bytes are reversed in 32-bit words, is put back in order.
- The Capcom games have no BIOS that tells who plays. ArcadeDMD watches the timer, the score once it is learned, and the health in the fighting games. As long as they move, player 1 plays, and after 10 seconds without any change the coin screen comes back. Without them, the game stays on its game scene. When the game's credits are read, a credit spent is a start, player 1 plays from the select screen on.
- `demo_capcom.bat` plays the demo of a Capcom game, most of them with the coin screen first.

**The Capcom fighting games**
- 22 fighting games read their stage. The HD screen shows it, with the place under the stage banner (CHINA, INDIA, FEAST OF THE DAMNED...).
- Eight new fight stages drawn by the program. A castle roof in Japan at night, a Chinese street market, a steel factory, a gothic manor under the moon, an Indian palace at sunset, a golden temple on its river, a laboratory and an air base at dusk.
- The super gauges, on the bottom line of the panel and under the fighters on the HD screen. Blue as they fill up, gold with MAX when they are full.
- Street Fighter III: New Generation names its fighters.
- Street Fighter II, Champion Edition, Hyper Fighting, Super Street Fighter II and Street Fighter Alpha read the rounds won by each player. Gold stars under the bars on the HD screen, gold squares next to the timer on the panel, and the winner of each round from them. In Street Fighter II the health goes below zero at a K.O. and read full, the K.O. was missed and the WIN went to the wrong fighter. A bar below zero now reads empty, in every Capcom game. Street Fighter II also reads its credits and the score, learned on a cabinet. A credit spent switches to the game at the character select, PRESS START no longer stays on.

**The Capcom games done one by one**
- Fifty Capcom games get a panel scene and an animated HD scene of their own, drawn by the program.
- The 23 games with characters show like Metal Slug on the HD screen, with no character drawn by the program. The beat'em ups (Final Fight, Captain Commando, Cadillacs and Dinosaurs, The Punisher, The King of Dragons, Knights of the Round, Warriors of Fate, the two Dungeons & Dragons, Alien vs. Predator, Armored Warriors, Battle Circuit), the action games and platformers (Ghouls'n Ghosts, Strider, Mega Twins, Magic Sword, Willow, Nemo, Three Wonders, Dynasty Wars), the two Pang and Mercs. The place of the game stays behind, calm and darker, each player has a panel with what is read in the game (gauge, lives, score, bombs, weapon, level), and the middle shows the logo, the timer when it is read whole, and the credits. The game's events show between the panels. Points are a punch, a shot, a slash, a thrown weapon, a spell or a balloon that bursts, a bomb or a special leaves the panel and the middle blows up, a life lost turns the panel red. Player 2's panel lights up when his values move.
- The shoot'em ups (1944, 19XX, 1941, Varth, U.N. Squadron, Carrier Air Wing, Forgotten Worlds, Giga Wing, Progear, Mars Matrix, Dimahoo, Eco Fighters, Mercs). Once the score is learned, the enemies blow up when the game scores points, a bomb sweeps the screen, the weapon picked up and the plane chosen are named, and on the panel the plane of the game flies and fires.
- The puzzle games and quizzes (Super Puzzle Fighter II Turbo, Puzz Loop 2, Capcom Sports Club, Quiz & Dragons, Adventure Quiz Capcom World 2) play by themselves with our own gems, balls, questions and players.
- Quiz Tonosama no Yabou 2, Quiz Nanairo Dreams, Jyangokushi, Janpai Puzzle Choukou, Gulun.Pa!, Pnickies, Frog Feast, Pokonyan! Balloon, Magical Pumpkin and Ganbare! Marine Kun get theirs too.
- Final Fight Anniversary Edition, Final Fight EX and Tenchi wo Kurau II CPS Changer take the scene of their game.

**Credits and coins**
- Under RetroArch most Capcom games do not give their credits. With the coin buttons shown by `coin_buttons.bat`, ArcadeDMD counts them. A coin gives a credit and a player who begins takes one, at the start, at a continue (lives back from 0, or the energy in Mercs) and when player 2 joins in (his values start moving). For an exact count, `learn.bat` can find where the game keeps them.
- 1944 and Dimahoo keep all their values outside of the memory RetroArch shares. The log says so, launch them with MAME to see everything.
- Super Puzzle Fighter II Turbo no longer draws two little fighters, the counter gems fly across to the other well and the names read in the game show in the middle.
- 1944 on the HD screen takes the icons of the game. The bombs as B medals, the side fighters in stock in their frame with their number, the gold crystals picked up, POW in yellow. The side fighters fly at our plane's sides, a bomb is a salvo of missiles, and a big WARNING announces the boss once its address is found.
- The MAME plugin no longer opens an error window (CPU not found) when MAME starts on its own game list, and no longer sends a game start for it.

**HD screen**
- The animated backdrops are a little darker so that the information stands out (`"dim"` in the `preview` section, 30 percent by default, 0 to 80).
- The credits of the fighting games are bigger, on a dark pill.

**Also**
- Player 2 shows in the Capcom shoot'em ups when his values move, his score that goes up, a life or a bomb spent, a hit taken. He stayed on PRESS START, these games have no BIOS that tells who plays. Giga Wing also reads the bombs and the power of player 2, and its score and credits learned on a cabinet. The credits show under the logo during a game.
- Mercs reads its timer whole, three digits where only the last one was read (TIME 7), the score of both players learned on a cabinet, the mega crashes of player 2, which leave his panel too, and the weapon of each player, named next to his badge with its power-ups (assault rifle, flamethrower, shotgun, grenade launcher), and the mission, MISSION 1 COMPLETE! when the next one starts. FinalBurn Neo sets it for three players, the README tells how to set it for two (DIP switches).
- The HD screen gave the Metal Slug scene to Marvel Super Heroes and Magic Sword, their names start like Metal Slug's. Only the Metal Slug games get it now.

**Updating from 1.29.3**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept).

### Français

**Tous les jeux Capcom CPS1, CPS2 et CPS3**
- Chaque jeu Capcom CPS1, CPS2 et CPS3 de FinalBurn Neo est reconnu, avec MAME comme avec RetroArch. Ça fait 88 jeux et leurs 942 sets. Une version, un bootleg ou un hack prend le fichier de son jeu d'origine, avec son propre nom quand il en a un.
- Ce qu'écrit la base de codes de triche de FinalBurn Neo est lu. La vie de chaque joueur, le chrono, les vies, les bombes, la jauge de super, les personnages et leur nom, le décor, et les crédits quand le jeu les garde. Le chrono s'affiche quand la triche le donne en entier. Dans 23 jeux elle n'en donne qu'une partie (un chiffre, les secondes d'une horloge, un compteur qui n'est pas le chrono vu dans le jeu), ArcadeDMD ne le lit alors que pour voir que le jeu tourne. La RAM du CPS3, dont les octets sont inversés par mots de 32 bits, est remise dans l'ordre.
- Les jeux Capcom n'ont pas de BIOS qui dit qui joue. ArcadeDMD surveille le chrono, le score une fois appris, et la vie dans les jeux de combat. Tant qu'ils bougent, le joueur 1 joue, et au bout de 10 secondes sans le moindre changement l'écran des pièces revient. Sans eux, le jeu reste sur sa scène de jeu. Quand les crédits du jeu sont lus, un crédit dépensé est un départ, le joueur 1 joue dès l'écran de sélection.
- `demo_capcom.bat` lance la démo d'un jeu Capcom, la plupart avec l'écran des pièces d'abord.

**Les jeux de combat Capcom**
- 22 jeux de combat lisent leur décor. L'écran HD le montre, avec le lieu sous le bandeau du décor (CHINE, INDE, FEAST OF THE DAMNED...).
- Huit nouveaux décors de combat dessinés par le programme. Un toit de château au Japon la nuit, un marché chinois, une aciérie, un manoir gothique sous la lune, un palais indien au couchant, un temple d'or au bord de son fleuve, un laboratoire et une base aérienne au crépuscule.
- Les jauges de super, sur la ligne du bas de la dalle et sous les combattants sur l'écran HD. Bleues quand elles se remplissent, dorées avec MAX quand elles sont pleines.
- Street Fighter III: New Generation donne le nom de ses combattants.
- Street Fighter II, Champion Edition, Hyper Fighting, Super Street Fighter II et Street Fighter Alpha lisent les rounds gagnés par chaque joueur. Des étoiles dorées sous les barres sur l'écran HD, des carrés dorés à côté du chrono sur la dalle, et le vainqueur de chaque round d'après eux. Dans Street Fighter II la vie passe sous zéro au K.O. et se lisait pleine, le K.O. était raté et le WIN allait au mauvais combattant. Une barre sous zéro se lit maintenant vide, dans tous les jeux Capcom. Street Fighter II lit aussi ses crédits et le score, appris sur une borne. Un crédit dépensé passe au jeu dès la sélection des personnages, PRESS START ne reste plus affiché.

**Les jeux Capcom faits un par un**
- Cinquante jeux Capcom ont une scène de dalle et une scène HD animée à leur image, dessinées par le programme.
- Les 23 jeux à personnages s'affichent façon Metal Slug sur l'écran HD, sans personnage dessiné par le programme. Les beat'em up (Final Fight, Captain Commando, Cadillacs and Dinosaurs, The Punisher, The King of Dragons, Knights of the Round, Warriors of Fate, les deux Dungeons & Dragons, Alien vs. Predator, Armored Warriors, Battle Circuit), les jeux d'action et de plateformes (Ghouls'n Ghosts, Strider, Mega Twins, Magic Sword, Willow, Nemo, Three Wonders, Dynasty Wars), les deux Pang et Mercs. Le décor du jeu reste derrière, calme et plus sombre, chaque joueur a un panneau avec ce qui est lu dans le jeu (jauge, vies, score, bombes, arme, niveau), et le milieu montre le logo, le chrono quand il est lu en entier, et les crédits. Les événements du jeu se voient entre les panneaux. Des points font un coup de poing, un tir, une entaille, une arme lancée, un sort ou un ballon qui éclate, une bombe ou un coup spécial part du panneau et le milieu explose, une vie perdue fait rougir le panneau. Le panneau du joueur 2 s'allume quand ses valeurs bougent.
- Les shoot'em up (1944, 19XX, 1941, Varth, U.N. Squadron, Carrier Air Wing, Forgotten Worlds, Giga Wing, Progear, Mars Matrix, Dimahoo, Eco Fighters, Mercs). Une fois le score appris, les ennemis explosent quand le jeu marque des points, une bombe balaie l'écran, l'arme ramassée et l'avion choisi sont nommés, et sur la dalle l'avion du jeu vole et tire.
- Les jeux de réflexion et les quiz (Super Puzzle Fighter II Turbo, Puzz Loop 2, Capcom Sports Club, Quiz & Dragons, Adventure Quiz Capcom World 2) jouent tout seuls avec nos propres gemmes, billes, questions et joueurs.
- Quiz Tonosama no Yabou 2, Quiz Nanairo Dreams, Jyangokushi, Janpai Puzzle Choukou, Gulun.Pa!, Pnickies, Frog Feast, Pokonyan! Balloon, Magical Pumpkin et Ganbare! Marine Kun ont aussi les leurs.
- Final Fight Anniversary Edition, Final Fight EX et Tenchi wo Kurau II CPS Changer prennent la scène de leur jeu.

**Crédits et pièces**
- Sous RetroArch la plupart des jeux Capcom ne donnent pas leurs crédits. Avec les boutons des pièces montrés par `coin_buttons.bat`, ArcadeDMD les compte. Une pièce donne un crédit et un joueur qui commence en prend un, au départ, à un continue (les vies qui reviennent de 0, ou l'énergie dans Mercs) et quand le joueur 2 arrive (ses valeurs se mettent à bouger). Pour un compte exact, `learn.bat` peut trouver où le jeu les garde.
- 1944 et Dimahoo gardent toutes leurs valeurs hors de la mémoire que RetroArch partage. Le journal le dit, lance-les avec MAME pour tout voir.
- Super Puzzle Fighter II Turbo ne dessine plus deux petits combattants, les gemmes à compteur volent vers l'autre puits et les noms lus dans le jeu s'affichent au milieu.
- 1944 prend les icônes du jeu sur l'écran HD. Les bombes en médailles B, l'escorte en réserve dans son cadre avec son nombre, les cristaux d'or ramassés, POW en jaune. Les chasseurs d'escorte volent à côté de notre avion, une bombe est une salve de missiles, et un grand WARNING annonce le boss une fois son adresse trouvée.
- Le plugin MAME n'ouvre plus de fenêtre d'erreur (CPU introuvable) quand MAME démarre sur sa liste de jeux, et n'envoie plus de départ de partie pour elle.

**Écran HD**
- Les décors animés sont un peu assombris pour que les infos ressortent (`"dim"` dans la section `preview`, 30 % par défaut, de 0 à 80).
- Les crédits des jeux de combat sont plus gros, sur une pastille sombre.

**Aussi**
- Le joueur 2 apparaît dans les shoot'em up Capcom quand ses valeurs bougent, son score qui monte, une vie ou une bombe en moins, un coup reçu. Il restait sur PRESS START, ces jeux n'ont pas de BIOS qui dit qui joue. Giga Wing lit aussi les bombes et la puissance du joueur 2, et son score et ses crédits appris sur une borne. Les crédits s'affichent sous le logo pendant la partie.
- Mercs lit son chrono en entier, trois chiffres dont seul le dernier était lu (TIME 7), le score des deux joueurs appris sur une borne, les méga attaques du joueur 2, qui partent aussi de son panneau, et l'arme de chaque joueur, nommée à côté de son badge avec ses POW (fusil d'assaut, lance-flammes, fusil à pompe, lance-grenades), et la mission, MISSION 1 ACCOMPLIE ! quand la suivante commence. FinalBurn Neo le règle pour trois joueurs, le README dit comment le régler pour deux (DIP switches).
- L'écran HD donnait la scène de Metal Slug à Marvel Super Heroes et à Magic Sword, leur nom commence comme celui de Metal Slug. Seuls les Metal Slug l'ont maintenant.

**Mettre à jour depuis la 1.29.3**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés).

## 1.29.3

### English

**Every Neo Geo game with RetroArch**
- Every Neo Geo set of FinalBurn Neo is recognized (693 of them). A version, a bootleg or a hack takes the file of its original game, as with MAME. Metal Slug 3 Fully Decrypted plays like Metal Slug 3, and KOF 2002 Magic Plus like KOF 2002 with its own name at the top. A homebrew game gets the scene of its genre, and so does Treasure of the Caribbean, the last official game that was missing. Only the BIOS and the test programs are left out.
- `test_retroarch.bat` tells which game a version takes the file of.
- On the HD screen, each coin door says what a coin gives. On a Neo Geo MVS, the right one says 2 CREDITS, like the machine.

**Updating from 1.29.2**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept).

### Français

**Tous les jeux Neo Geo avec RetroArch**
- Chaque set Neo Geo de FinalBurn Neo est reconnu (693 en tout). Une version, un bootleg ou un hack prend le fichier de son jeu d'origine, comme avec MAME. Metal Slug 3 Fully Decrypted se joue comme Metal Slug 3, et KOF 2002 Magic Plus comme KOF 2002 avec son propre nom en haut. Un jeu amateur (homebrew) a la scène de son genre, tout comme Treasure of the Caribbean, le dernier jeu officiel qui manquait. Seuls le BIOS et les programmes de test sont laissés de côté.
- `test_retroarch.bat` dit de quel jeu une version prend le fichier.
- Sur l'écran HD, chaque monnayeur dit ce que donne une pièce. Sur une Neo Geo MVS, celui de droite affiche 2 CRÉDITS, comme la machine.

**Mettre à jour depuis la 1.29.2**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés).

## 1.29.2

### English

**Every coin and its side, with RetroArch**
- `coin_buttons.bat` shows ArcadeDMD your two coin buttons, on the controllers or the keyboard. ArcadeDMD then reads them itself, at the same time as RetroArch and without taking them from it. Every coin is seen with its side, during a game too, and on the HD screen the coin drops in the slot on the side where you put it. Windows only.
- An MVS gives 2 credits for a coin in its second slot when its settings were not changed. ArcadeDMD counts the same way (`"mvs_credits": [1, 2]` in the `coin_buttons` section of `config.json`).
- Without the buttons, the BIOS now also shows the first coin put in during a game.
- `test_coins.bat` also writes down each press on the coin buttons.

**Updating from 1.29.1**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept). Then run `coin_buttons.bat` once.

### Français

**Chaque pièce et son côté, avec RetroArch**
- `coin_buttons.bat` montre à ArcadeDMD tes deux boutons de pièce, sur les manettes ou le clavier. ArcadeDMD les lit alors lui-même, en même temps que RetroArch et sans les lui prendre. Chaque pièce est vue avec son côté, même en pleine partie, et sur l'écran HD la pièce tombe dans le monnayeur du côté où tu l'as mise. Seulement sous Windows.
- Une MVS donne 2 crédits pour une pièce dans son deuxième monnayeur quand ses réglages n'ont pas été changés. ArcadeDMD compte pareil (`"mvs_credits": [1, 2]` dans la rubrique `coin_buttons` de `config.json`).
- Sans les boutons, le BIOS montre maintenant aussi la première pièce mise en pleine partie.
- `test_coins.bat` note aussi chaque appui sur les boutons des pièces.

**Mettre à jour depuis la 1.29.1**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés). Lance ensuite une fois `coin_buttons.bat`.

## 1.29.1

### English

**Fixes from the cabinet**
- Fighting games. The timer sits right between its two lines, with the same gap on each side. The line on the left touched the digits.
- Only the name of the game on the panel, without the maker (SNK, VIDEO SYSTEM...), on the coin screen and at the top during a game. A title that fits stays still instead of scrolling.
- With RetroArch, the HD screen no longer drops the coins once on the right, once on the left. RetroArch does not tell which coin slot a coin came through, so the coin drops in player 1's slot when nobody plays, in the slot of the player who comes in during a game, and in the slot of the player at the CONTINUE.
- `test_coins.bat` writes down what the Neo Geo BIOS does when a coin goes in with RetroArch, to find out on a real cabinet how to see every coin and its side. The result goes to `runtime\test_coins.txt`.

**Updating from 1.29**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept).

### Français

**Corrections vues sur la borne**
- Jeux de combat. Le chrono est pile entre ses deux traits, avec le même espace de chaque côté. Le trait de gauche touchait les chiffres.
- Seulement le nom du jeu sur la dalle, sans le fabricant (SNK, VIDEO SYSTEM...), sur l'écran des pièces et en haut pendant la partie. Un titre qui tient reste fixe au lieu de défiler.
- Avec RetroArch, l'écran HD ne fait plus tomber les pièces une fois à droite, une fois à gauche. RetroArch ne dit pas par quel monnayeur une pièce est passée, alors la pièce tombe dans le monnayeur du joueur 1 quand personne ne joue, dans celui du joueur qui arrive pendant une partie, et dans celui du joueur au CONTINUE.
- `test_coins.bat` note ce que fait le BIOS de la Neo Geo quand une pièce entre avec RetroArch, pour trouver sur une vraie borne comment voir chaque pièce et son côté. Le résultat va dans `runtime\test_coins.txt`.

**Mettre à jour depuis la 1.29**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés).

## 1.29.0

### English

**A simpler panel for the shoot'em ups**
- During a game, the panel of the fifteen Neo Geo shoot'em ups only shows the score in big digits in the middle (or the title of the game as long as the score has not been learned), your lives at the bottom left (a plane and x2) and your bombs at the bottom right. The title no longer scrolls during a game, the credits and INSERT COIN are gone, as are the power gauge and the scenery.
- Between them flies your ship. It follows your stick and fires while you hold the fire button, read in the Neo Geo BIOS with MAME as with RetroArch, and flies by itself until you touch them. With two players, both ships face to face.
- Everything else takes the panel for a moment, one thing at a time, as on a pinball. BOMB! and its explosions, POWER UP then MAX POWER, the plane that blows up and the lives left, LAST LIFE, 1UP, ROUND 2 or STAGE 2, SPEED UP, the SUPER SHOT of Strikers 1945 Plus, CONTINUE?, GAME OVER, PLAYER 1 and PLAYER 2, and CREDIT 1 when a coin goes in during a game. A more important event replaces the one playing (GAME OVER over a life lost), a less important one waits its turn.
- Each enemy destroyed in the game blows up ahead of your ship, a big one for a big enemy. As long as the score has not been learned, an enemy blows up ahead of it now and then while it fires, as on the HD screen. Your own animations in the `artwork` folder still come first, and `artwork\ship.gif` (or `artwork\<game>\ship.gif`) replaces the ship.
- A value that the game has not set yet (the lives during the choice of the plane) is not shown.
- Three new panel layers, `events` (short events, one at a time), `counter` (a small drawing followed by a number) and `ship` (the ship that follows the stick).

**The panel looks like the preview**
- LEDs light up in proportion to the value they get, so the dark grays of the scenes glowed on the Pixelcade and made them look busy. ArcadeDMD now corrects the colors it sends to the Pixelcade (`"gamma": 2.2` in the `pixelcade` section, `1.0` sends them as they are).

**The coin drops with RetroArch too**
- The FinalBurn Neo core of RetroArch does not share the memory where an MVS keeps its credits, so the coin never dropped. ArcadeDMD now guesses the credits from the Neo Geo BIOS. A coin put in while nobody plays drops on the panel and the HD screen, PRESS START follows, and each player who starts takes a credit. A coin put in during a game is not seen. FinalBurn Neo must be in MVS mode, and `runtime\arcadedmd.log` tells what the BIOS did. With MAME, the real credits are still read.

**Fixes**
- In the Neo Geo games whose score has not been learned, the title that scrolls at the top no longer runs into INSERT COIN.

**Updating from 1.28**
Extract the new zip over the old folder (`config.json`, your learned addresses and your `artwork` folder are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Une dalle plus simple pour les shoot'em up**
- Pendant la partie, la dalle des quinze shoot'em up Neo Geo ne montre plus que le score en gros au milieu (ou le titre du jeu tant que le score n'est pas appris), tes vies en bas à gauche (un avion et x2) et tes bombes en bas à droite. Le titre ne défile plus pendant la partie, les crédits et INSERT COIN disparaissent, comme la jauge de puissance et le décor.
- Entre les deux vole ton vaisseau. Il suit ton stick et tire tant que tu tiens le bouton de tir, lus dans le BIOS de la Neo Geo avec MAME comme avec RetroArch, et vole tout seul tant que tu n'y as pas touché. À deux, les deux vaisseaux face à face.
- Tout le reste prend la dalle un instant, une chose à la fois, comme sur un flipper. BOMBE! et ses explosions, POWER UP puis MAX POWER, l'avion qui explose et les vies qui restent, LAST LIFE, 1UP, ROUND 2 ou STAGE 2, SPEED UP, le SUPER SHOT de Strikers 1945 Plus, CONTINUE?, GAME OVER, PLAYER 1 et PLAYER 2, et CRÉDIT 1 quand une pièce entre en pleine partie. Un événement plus important remplace celui en cours (GAME OVER par-dessus une vie perdue), un moins important attend son tour.
- Chaque ennemi détruit dans le jeu explose devant ton vaisseau, une grosse explosion pour un gros ennemi. Tant que le score n'est pas appris, un ennemi explose devant lui de temps en temps pendant qu'il tire, comme sur l'écran HD. Tes propres animations du dossier `artwork` passent toujours en premier, et `artwork\ship.gif` (ou `artwork\<jeu>\ship.gif`) remplace le vaisseau.
- Une valeur que le jeu n'a pas encore posée (les vies pendant le choix de l'avion) ne s'affiche pas.
- Trois nouvelles couches de dalle, `events` (des événements courts, un à la fois), `counter` (un petit dessin suivi d'un nombre) et `ship` (le vaisseau qui suit le stick).

**La dalle ressemble à l'aperçu**
- Les LED éclairent en proportion de la valeur reçue, donc les gris sombres des scènes brillaient sur la Pixelcade et les rendaient chargées. ArcadeDMD corrige maintenant les couleurs qu'il envoie à la Pixelcade (`"gamma": 2.2` dans la section `pixelcade`, `1.0` les envoie telles quelles).

**La pièce tombe aussi avec RetroArch**
- Le cœur FinalBurn Neo de RetroArch ne partage pas la mémoire où la MVS range ses crédits, donc la pièce ne tombait jamais. ArcadeDMD devine maintenant les crédits d'après le BIOS de la Neo Geo. Une pièce mise quand personne ne joue tombe sur la dalle et sur l'écran HD, PRESS START suit, et chaque joueur qui commence prend un crédit. Une pièce mise en pleine partie ne se voit pas. FinalBurn Neo doit être en mode MVS, et `runtime\arcadedmd.log` dit ce que le BIOS a fait. Avec MAME, les vrais crédits sont toujours lus.

**Corrections**
- Dans les jeux Neo Geo dont le score n'est pas appris, le titre qui défile en haut ne chevauche plus INSERT COIN.

**Mettre à jour depuis la 1.28**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json`, tes adresses apprises et ton dossier `artwork` sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.28.0

### English

**The shoot'em ups follow the game more closely**
- In the fifteen Neo Geo shoot'em ups done one by one, once the score is read, the enemies of the HD screen only blow up when the game scores points. The enemy our shots are hitting goes first and its points show above it. The bigger the gain next to the usual ones, the bigger the blast, and the screen shakes for a big enemy. Our shots still hit the enemies, they flash.
- The bombs, the super shot of Strikers 1945 Plus and the charged shot of Pulstar stay weapons of the game, they destroy what they hit. The unit of Last Resort hits the enemies too, and the points decide which one blows up.
- A bonus that the game counts at the end of a stage shows as one BONUS counter instead of blowing up dozens of enemies.
- On the panel, real explosions drawn pixel by pixel. One goes off ahead of the ship at each point scored, the size and pace of the DOFLinx ones, a big fireball (or a blue plasma blast in space) for a big gain, and a row of explosions with a shock wave when a bomb goes off. The super shot of Strikers 1945 Plus and the charged shot of Pulstar have theirs too. The ship fires at each point, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger and Last Hope included.
- Your own animations (the GIFs of DOFLinx or of the Pixelcade, for example) can replace ours. They go in an `artwork` folder next to `arcadedmd.py`, which is never published and which an update never touches (`artwork\boom.gif`, `boom_big.gif`, `bomb.gif`, `shock.gif`, `super.gif`, `charge.gif`, or `artwork\<game>\` for one game). A 128 x 32 GIF plays over the whole panel, or at the place of the action when its drawing fits in the middle, like the explosions of DOFLinx.
- A new panel layer, `anim`, plays an animation once when a value of the game changes.
- The score of these games is in no database. Until it is learned with `learn.bat`, the scenes play by themselves as before.

**Updating from 1.27**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Les shoot'em up suivent mieux le jeu**
- Dans les quinze shoot'em up Neo Geo faits un par un, dès que le score est lu, les ennemis de l'écran HD n'explosent que quand le jeu marque des points. L'ennemi que nos tirs touchent part d'abord et ses points s'affichent au-dessus. Plus le gain est gros à côté des gains habituels, plus l'explosion est forte, et l'écran tremble pour un gros ennemi. Nos tirs touchent toujours les ennemis, ils clignotent.
- Les bombes, le super tir de Strikers 1945 Plus et le tir chargé de Pulstar restent des armes du jeu, ils détruisent ce qu'ils touchent. L'unité de Last Resort touche aussi les ennemis, et les points décident lequel explose.
- Un bonus compté par le jeu en fin de niveau s'affiche en un seul compteur BONUS au lieu de faire exploser des dizaines d'ennemis.
- Sur la dalle, de vraies explosions dessinées pixel par pixel. Une part devant le vaisseau à chaque point marqué, de la taille et au rythme de celles de DOFLinx, une grosse boule de feu (ou une explosion de plasma bleu dans l'espace) pour un gros gain, et une rangée d'explosions avec une onde de choc quand une bombe part. Le super tir de Strikers 1945 Plus et le tir chargé de Pulstar ont aussi la leur. Le vaisseau tire à chaque point, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger et Last Hope compris.
- Tes propres animations (les GIF de DOFLinx ou de la Pixelcade par exemple) peuvent remplacer les nôtres. Elles vont dans un dossier `artwork` à côté d'`arcadedmd.py`, jamais publié et jamais touché par une mise à jour (`artwork\boom.gif`, `boom_big.gif`, `bomb.gif`, `shock.gif`, `super.gif`, `charge.gif`, ou `artwork\<jeu>\` pour un seul jeu). Un GIF de 128 x 32 se joue sur toute la dalle, ou à l'endroit de l'action quand son dessin tient au milieu, comme les explosions de DOFLinx.
- Une nouvelle couche de dalle, `anim`, joue une animation une fois quand une valeur du jeu change.
- Le score de ces jeux n'est dans aucune base. Tant qu'il n'est pas appris avec `learn.bat`, les scènes jouent toutes seules comme avant.

**Mettre à jour depuis la 1.27**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.27.0

### English

**Neo Geo games done one by one, eleventh and last batch**
- Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2 and Shougi no Tatsujin now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes ninety-seven games done one by one, every game of `PROGRESS.md`.
- Nightmare in the Dark and The Super Spy. The graveyard under a huge full moon where the monsters burn, the corridor of the building where a masked fighter faces our fists.
- The four quizzes. Their sets as in the games, the question panel and its four answers, a big circle for a right answer and a big cross for a wrong one, read from the score and the lives. The questions are our own.
- The five mahjong games and Shougi no Tatsujin. Each felt and its tile backs, our hand of thirteen tiles, RON and TSUMO, the HP of Janshin Densetsu, the die of Minasan no Okagesamadesu!, then the wooden board by the sea where each piece taken goes onto a stand.
- Fixed. A round dot of a panel scene that follows no value is now drawn (the full moon of Nightmare in the Dark, the centre circle of Battle Flip Shot around the time).
- The score of Nightmare in the Dark, The Super Spy and the four quizzes is in no database. Learn it with `learn.bat`.
- `demo_neogeo.bat` now offers the ninety-seven games.

**Updating from 1.26**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, onzième et dernier lot**
- Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2 et Shougi no Tatsujin ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait quatre-vingt-dix-sept jeux faits un par un, tous les jeux de `PROGRESS.md`.
- Nightmare in the Dark et The Super Spy. Le cimetière sous une énorme pleine lune où les monstres brûlent, le couloir de l'immeuble où un combattant masqué fait face à nos poings.
- Les quatre quiz. Leurs décors comme dans les jeux, le panneau de la question et ses quatre réponses, un grand rond pour une bonne réponse et une grande croix pour une mauvaise, lus dans le score et les vies. Les questions sont à nous.
- Les cinq jeux de mahjong et Shougi no Tatsujin. Chaque tapis et ses dos de tuiles, notre main de treize tuiles, RON et TSUMO, les HP de Janshin Densetsu, le dé de Minasan no Okagesamadesu!, puis le plateau de bois au bord de la mer où chaque pièce prise va sur un support.
- Corrigé. Un disque d'une scène de dalle qui ne suit aucune valeur est maintenant dessiné (la pleine lune de Nightmare in the Dark, le cercle central de Battle Flip Shot autour du temps).
- Le score de Nightmare in the Dark, The Super Spy et des quatre quiz n'est dans aucune base. Apprends-le avec `learn.bat`.
- `demo_neogeo.bat` propose maintenant les quatre-vingt-dix-sept jeux.

**Mettre à jour depuis la 1.26**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.26.0

### English

**Neo Geo games done one by one, tenth batch**
- Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords and Eight Man now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes eighty-five games done one by one. `PROGRESS.md` shows what comes next.
- Zintrick, Digger Man and The Irritating Maze. Jewels shaped like drops thrown up their columns, a mine where our little digger digs to each jewel while the rocks fall, a corridor of the maze where a life lost in the game is an electric shock.
- Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger and Last Hope. Space over a planet with the four weapons in their colours, the forest and its steam train seen from the sky, the sea at dusk and its iron warships, deep space and its nebulas.
- Bang Bang Busters, Crossed Swords and Eight Man. The ice world where the enemies are trapped in bubbles, a duel of knights in the forest at night with the gold and the magic read in the game, the ruined city at sunset where our fast cyborg leaves a trail of copies.
- The score of these games except The Irritating Maze is in no database. Learn it with `learn.bat`.
- `demo_neogeo.bat` now offers the eighty-five games.

**Updating from 1.25**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, dixième lot**
- Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords et Eight Man ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait quatre-vingt-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Zintrick, Digger Man et The Irritating Maze. Des joyaux en gouttes lancés dans leurs colonnes, une mine où notre petit mineur creuse jusqu'à chaque joyau pendant que les rochers tombent, un couloir du labyrinthe où une vie perdue dans le jeu est une décharge électrique.
- Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger et Last Hope. L'espace au-dessus d'une planète avec les quatre armes dans leurs couleurs, la forêt et son train à vapeur vus du ciel, la mer au crépuscule et ses cuirassés, l'espace profond et ses nébuleuses.
- Bang Bang Busters, Crossed Swords et Eight Man. Le monde de glace où les ennemis sont pris dans des bulles, un duel de chevaliers dans la forêt la nuit avec l'or et la magie lus dans le jeu, la ville en ruine au coucher du soleil où notre cyborg rapide laisse une traînée de copies.
- Le score de ces jeux, sauf The Irritating Maze, n'est dans aucune base. Apprends-le avec `learn.bat`.
- `demo_neogeo.bat` propose maintenant les quatre-vingt-cinq jeux.

**Mettre à jour depuis la 1.25**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.25.0

### English

**Neo Geo games done one by one, ninth batch**
- Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa and Puzzled now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes seventy-five games done one by one. `PROGRESS.md` shows what comes next.
- Bang Bead and Battle Flip Shot. Two players face to face on a court seen from above, the street with its parked cars, the arena of teal metal and its targets. A 'Miracle' power spent is a shot on fire, a target hit in the game cracks.
- Over Top. The stages seen from the sky, the pine forest and the grey road, the map in its little television, the time, RANK, the speedometer and the lap time.
- Stakes Winner, Stakes Winner 2 and Jockey Grand Prix. Horse races seen from the side, a Japanese racecourse, Longchamp and its windmill, a dirt track with its odds board. The horse's qualities and POWER read in the game.
- Gururin, Ghostlop, Pochi and Nyaa and Puzzled. A board that turns a quarter, little ghosts shot up in a street at night, soft blocks with faces of cats and dogs, brick towers whose full lines leave until the balloon floats away. The next pieces read in the game where they are known.
- The score of Bang Bead, Battle Flip Shot, Gururin, Ghostlop, Pochi and Nyaa and Puzzled is in no database. Learn it with `learn.bat`. No value of Jockey Grand Prix is known yet, its races run by themselves.
- A new panel sprite, a galloping horse and its jockey.
- `demo_neogeo.bat` now offers the seventy-five games.

**Updating from 1.24**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, neuvième lot**
- Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa et Puzzled ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait soixante-quinze jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Bang Bead et Battle Flip Shot. Deux joueurs face à face sur un terrain vu du dessus, la rue et ses voitures garées, l'arène de métal bleu-vert et ses cibles. Un pouvoir 'Miracle' dépensé est un tir en feu, une cible touchée dans le jeu se fissure.
- Over Top. Les étapes vues du ciel, la forêt de pins et la route grise, la carte dans sa petite télévision, le temps, RANK, le compteur et le temps du tour.
- Stakes Winner, Stakes Winner 2 et Jockey Grand Prix. Des courses de chevaux vues de côté, un hippodrome japonais, Longchamp et son moulin, une piste en terre et son tableau des cotes. Les qualités du cheval et POWER lus dans le jeu.
- Gururin, Ghostlop, Pochi and Nyaa et Puzzled. Un plateau qui tourne d'un quart, de petits fantômes tirés dans une rue la nuit, des blocs tout doux aux têtes de chats et de chiens, des tours de briques dont les lignes pleines partent jusqu'à ce que le ballon s'envole. Les pièces suivantes lues dans le jeu quand elles sont connues.
- Le score de Bang Bead, Battle Flip Shot, Gururin, Ghostlop, Pochi and Nyaa et Puzzled n'est dans aucune base. Apprends-le avec `learn.bat`. Aucune valeur de Jockey Grand Prix n'est encore connue, ses courses vont toutes seules.
- Un nouveau sprite pour la dalle, un cheval au galop et son jockey.
- `demo_neogeo.bat` propose maintenant les soixante-quinze jeux.

**Mettre à jour depuis la 1.24**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.24.0

### English

**Neo Geo games done one by one, eighth batch**
- Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf and Power Spikes II now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes sixty-five games done one by one. `PROGRESS.md` shows what comes next.
- Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98 and Pleasure Goal. The match in the stadium with the scoreboard of each game, the round clock, the yellow numbers and the moon, the blue band, the faces of futsal. The goals and the time read in the game.
- Soccer Brawl. Football of the future at night, the players in armour, the POWER METER of each team.
- Football Frenzy. The field seen from above, two teams line up, the runner breaks through until he is tackled, the points read in the game are touchdowns.
- Baseball Stars Professional and 2020 Super Baseball. The field seen from behind home plate, the count B S O in lights, the box of the inning, the outs counted in the game.
- Top Player's Golf and Power Spikes II. The course where the ball flies to the flag at each stroke, the indoor arena where three players on each side jump and spike, a super shot is a spike on fire.
- Nothing to learn in these ten games. No value of Tecmo World Soccer '96 is known yet, its match plays by itself.
- `demo_neogeo.bat` now offers the sixty-five games.

**Updating from 1.23**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, huitième lot**
- Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf et Power Spikes II ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait soixante-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98 et Pleasure Goal. Le match dans le stade avec le tableau de score de chaque jeu, l'horloge ronde, les chiffres jaunes et la lune, le bandeau bleu, les visages du futsal. Les buts et le temps lus dans le jeu.
- Soccer Brawl. Le football du futur la nuit, les joueurs en armure, le POWER METER de chaque équipe.
- Football Frenzy. Le terrain vu de haut, deux équipes s'alignent, le porteur file jusqu'au plaquage, les points lus dans le jeu sont des touchdowns.
- Baseball Stars Professional et 2020 Super Baseball. Le terrain vu de derrière le marbre, le compte B S O en voyants, la boîte de la manche, les retraits comptés dans le jeu.
- Top Player's Golf et Power Spikes II. Le parcours où la balle vole vers le drapeau à chaque coup, la salle où trois joueurs de chaque côté sautent et smashent, un super coup est un smash en feu.
- Rien à apprendre dans ces dix jeux. Aucune valeur de Tecmo World Soccer '96 n'est encore connue, son match se joue tout seul.
- `demo_neogeo.bat` propose maintenant les soixante-cinq jeux.

**Mettre à jour depuis la 1.23**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.23.0

### English

**Neo Geo games done one by one, seventh batch**
- Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks and Super Sidekicks 2 now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes fifty-five games done one by one. `PROGRESS.md` shows what comes next.
- Puzzle De Pon! R!. The boards and the star dial of Puzzle De Pon!, under a pink sky.
- Panic Bomber, Pop 'n Bounce and Super Bubble Pop. Fields of their own, little heads that fall and stack with bombs that blow up in a cross, soft creatures that a bouncing ball bursts, a white board seen at an angle where a little robot shoots its bubbles. The points and the power read in the game set things off.
- Spin Master and Ganryu. The desert of the pyramids where our hero throws his yo-yo, a street of old Japan at night where our swordsman fights the ninjas. The counters where each game puts them.
- Zupapa! and Neo Mr. Do!. The blue cave and its striped platforms where our little round hero boots the monsters, the field of coloured tiles where our little digger digs his tunnels and picks the cherries, EXTRA lit letter by letter.
- Super Sidekicks and Super Sidekicks 2. The match with the scoreboard of each game, the goals and the time read in the game.
- The score of Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa! and Neo Mr. Do! is in no database. Learn it with `learn.bat`.
- `demo_neogeo.bat` now offers the fifty-five games.

**Updating from 1.22**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, septième lot**
- Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks et Super Sidekicks 2 ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait cinquante-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Puzzle De Pon! R!. Les plateaux et le cadran étoilé de Puzzle De Pon!, sous un ciel rose.
- Panic Bomber, Pop 'n Bounce et Super Bubble Pop. Des champs à eux, de petites têtes qui tombent et s'empilent avec des bombes qui sautent en croix, des créatures molles qu'une balle qui rebondit fait éclater, un plateau blanc vu de biais où un petit robot tire ses bulles. Les points et la puissance lus dans le jeu déclenchent tout ça.
- Spin Master et Ganryu. Le désert des pyramides où notre héros lance son yo-yo, une rue du vieux Japon la nuit où notre sabreur combat les ninjas. Les compteurs là où chaque jeu les met.
- Zupapa! et Neo Mr. Do!. La grotte bleue et ses plateformes rayées où notre petit héros rond chasse les monstres, le champ de cases colorées où notre petit mineur creuse ses tunnels et ramasse les cerises, EXTRA qui s'allume lettre par lettre.
- Super Sidekicks et Super Sidekicks 2. Le match avec le tableau de score de chaque jeu, les buts et le temps lus dans le jeu.
- Le score de Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa! et Neo Mr. Do! n'est dans aucune base. Apprends-le avec `learn.bat`.
- `demo_neogeo.bat` propose maintenant les cinquante-cinq jeux.

**Mettre à jour depuis la 1.22**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.22.0

### English

**Neo Geo games done one by one, sixth batch**
- Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger and Puzzle De Pon! now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes forty-five games done one by one. `PROGRESS.md` shows what comes next.
- Mutation Nation, Sengoku, Sengoku 2 and Ninja Combat. Beat'em ups seen from the side, a ruined city, a red sunset with a castle floating in the sky, a great wooden bridge at dusk, a park at night. Fighters of our own, a swordsman whose blade leaves a trail of light, mutants, armoured ghost warriors and ninjas. The points are blows that land, the health that goes down a blow taken, the sphere or the attack item read in the game is shown. The counters where each game puts them.
- Ninja Commando. The jungle seen from above, our blue ninja runs up the path and throws fire dragons at the enemy ninjas. LIFE and TIME at the bottom as in the game.
- Blue's Journey. The land of giant plants, our little hero of our own throws leaves at the snails and the bees. 1P=, TIME=, the hearts and the flowers as in the game.
- Puzzle Bobble 2 and Puzzle De Pon!. The beach, then a sky full of stars, the boards in their frames of metal or bricks, the star dial of Puzzle De Pon! whose hand turns with the time left. The bubbles of Puzzle De Pon! come from the game.
- Magical Drop II and Money Puzzle Exchanger. The orange brick wall and its marble columns, the pastel diamonds and the coins of 10 to 500 with a little piggy bank of our own. The quota, the level and the chains read in the game pop the drops and the coins.
- The score of these ten games is in no database. Learn it with `learn.bat`.
- `demo_neogeo.bat` now offers the forty-five games.

**Updating from 1.21**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, sixième lot**
- Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger et Puzzle De Pon! ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait quarante-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Mutation Nation, Sengoku, Sengoku 2 et Ninja Combat. Des beat'em up de profil, une ville en ruine, un coucher de soleil rouge et un château flottant, un grand pont de bois au crépuscule, un parc la nuit. Des combattants à nous, un sabreur dont la lame laisse une traînée de lumière, des mutants, des guerriers fantômes en armure et des ninjas. Les points sont des coups portés, la vie qui baisse un coup reçu, la sphère ou l'objet d'attaque lu dans le jeu s'affiche. Les compteurs là où chaque jeu les met.
- Ninja Commando. La jungle vue du dessus, notre ninja bleu remonte le chemin et lance des dragons de feu sur les ninjas ennemis. LIFE et TIME en bas comme dans le jeu.
- Blue's Journey. Le pays des plantes géantes, notre petit héros à nous lance des feuilles aux escargots et aux abeilles. 1P=, TIME=, les cœurs et les fleurs comme dans le jeu.
- Puzzle Bobble 2 et Puzzle De Pon!. La plage, puis un ciel plein d'étoiles, les plateaux dans leurs cadres de métal ou de briques, le cadran étoilé de Puzzle De Pon! dont l'aiguille tourne avec le temps qui reste. Les bulles de Puzzle De Pon! viennent du jeu.
- Magical Drop II et Money Puzzle Exchanger. Le mur de briques orange et ses colonnes de marbre, les losanges pastel et les pièces de 10 à 500 avec une petite tirelire à nous. Le quota, le niveau et les chaînes lus dans le jeu font éclater les gouttes et les pièces.
- Le score de ces dix jeux n'est dans aucune base. Apprends-le avec `learn.bat`.
- `demo_neogeo.bat` propose maintenant les quarante-cinq jeux.

**Mettre à jour depuis la 1.21**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.21.0

### English

**Neo Geo games done one by one, fifth batch**
- NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army and Burning Fight now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes thirty-five games done one by one. `PROGRESS.md` shows what comes next.
- NAM-1975. Our soldier seen from behind shoots into the burning city, then the jungle. The bullets, the grenades and the weapon read in the game are shown, a grenade blows up where the crosshair is.
- Cyber-Lip. Our hero runs down the city at night and shoots the walking robots and the drones. The weapon whose ammo goes down in the game is the one he fires. TIME in blue, the weapon in the blue bar at the bottom.
- Ghost Pilots and Alpha Mission II. Seen from the sky, the earth and the sea, then a fortress in space. A fighter with a big radial engine, a space fighter, enemy planes, bombers and saucers. The planes left, the bombs, the stars, the gold and the power where each game puts them.
- Viewpoint. The floor of tiles seen at an angle, our hover-ship and its shadow. The bomb carried in the game sweeps the screen in its colour when it is spent.
- Zed Blade and Prehistoric Isle 2. Seen from the side, a valley at dawn with its helicopters, the sea by the island with its flying reptiles. A bomb spent blows up the screen.
- Shock Troopers 2nd Squad. The city street seen from above, our commando goes up the road and shoots the soldiers, the jeeps and the tanks. The weapon read in the game is the one he fires, a grenade spent is thrown. TIME in big yellow numbers, the weapon box and LV as in the game.
- Robo Army and Burning Fight. Beat'em ups seen from the side, the edge of a town at dusk, a street of small shops at night. A cyborg and a street fighter of our own face the robots and the thugs that come from both sides. The points are blows that land, the health that goes down a blow taken.
- The score of these ten games is in no database. Learn it with `learn.bat`.
- New panel sprite `sprites/runner.png`, a small running fighter.
- `demo_neogeo.bat` now lists the thirty-five games.
- Demo mode. A game that drives the ammo of its weapon itself keeps it when the weapon changes.

**Updating from 1.20**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, cinquième lot**
- NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army et Burning Fight ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait trente-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- NAM-1975. Notre soldat vu de dos tire dans la ville en feu, puis la jungle. Les balles, les grenades et l'arme lues dans le jeu s'affichent, une grenade saute là où est le viseur.
- Cyber-Lip. Notre héros parcourt la ville la nuit et tire sur les robots marcheurs et les drones. L'arme dont les munitions baissent dans le jeu est celle qu'il tire. TIME en bleu, l'arme dans la barre bleue en bas.
- Ghost Pilots et Alpha Mission II. Vus du ciel, la terre et la mer, puis une forteresse dans l'espace. Un chasseur à gros moteur en étoile, un chasseur spatial, des avions ennemis, des bombardiers et des soucoupes. Les avions qui restent, les bombes, les étoiles, l'or et la puissance là où chaque jeu les met.
- Viewpoint. Le sol de dalles vu de biais, notre vaisseau et son ombre. La bombe portée dans le jeu balaie l'écran dans sa couleur quand elle part.
- Zed Blade et Prehistoric Isle 2. De profil, une vallée à l'aube et ses hélicoptères, la mer au bord de l'île et ses reptiles volants. Une bombe dépensée fait sauter l'écran.
- Shock Troopers 2nd Squad. La rue de la ville vue du dessus, notre commando remonte la route et tire sur les soldats, les jeeps et les chars. L'arme lue dans le jeu est celle qu'il tire, une grenade dépensée est lancée. TIME en gros chiffres jaunes, le cadre de l'arme et LV comme dans le jeu.
- Robo Army et Burning Fight. Des beat'em up de profil, le bord d'une ville au soir, une rue de petites boutiques la nuit. Un cyborg et un combattant à nous affrontent les robots et les voyous qui arrivent des deux côtés. Les points sont des coups portés, la vie qui baisse un coup reçu.
- Le score de ces dix jeux n'est dans aucune base. Apprends-le avec `learn.bat`.
- Nouveau sprite de dalle `sprites/runner.png`, un petit combattant qui court.
- `demo_neogeo.bat` propose maintenant les trente-cinq jeux.
- Mode démo. Un jeu qui gère lui-même les munitions de son arme les garde quand l'arme change.

**Mettre à jour depuis la 1.20**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.20.0

### English

**Neo Geo games done one by one, fourth batch**
- Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally and Magician Lord now have a file of their own, with a panel scene and an animated HD scene made for each game after screenshots of the game. That makes twenty-five games done one by one. `PROGRESS.md` shows what comes next.
- Strikers 1945 Plus. On the HD screen, the game's two side panels (SCORE, the planes left, BOMB, the SUPER SHOT gauge) around war-torn ground seen from the sky, villages with broken tiled roofs, a railway and its train, a river and its bridges. The plane chosen by the player, drawn after the real one (P-38, F5U, Spitfire, Ta 152, Zero, Fiat G.56, XP-55). The full gauge that empties is the super shot, a bomb brings a formation of bombers.
- Street Hoop. A half court in a park, three against three. The points read in the game are shots from far, jump shots or dunks, the full SUPER SHOT gauge that empties is a shot on fire. The points in big red and blue letters at the top, the clock in its orange box at the bottom.
- Super Dodge Ball. A cobbled lot, two teams of three players of our own. A player whose health goes down takes the ball full in the face, at zero he is out, the full POW gauge that empties is a power shot on fire. The health bars of both teams with the names, TIME in the middle.
- Neo Bomberman. The maze seen from above, one look per world, little miner robots of our own. The bombs dropped in the game are dropped here and blow up in a cross, blocks break and come back.
- Twinkle Star Sprites. Two fields side by side and the ornate column between them, a forest that scrolls down, little witches of our own. The attacks read in the game cross over to the other field, a heart lost makes the witch spin, a bomb clears her field. Pow 1 2 Max and the bombs at the bottom.
- League Bowling. The alley seen from behind the bowler. Each time the game's shot clock starts again, the bowler throws, the ball hooks down the lane and the pins fly, STRIKE! or SPARE! now and then.
- Neo Drift Out and Thrash Rally. The rally stages seen from the sky, dirt, tarmac or snow, the car drifts in the bends, a checkpoint arch goes by when time is added. TIME as in each game, and the speed in Thrash Rally.
- Riding Hero. The road seen from behind the bike rushes to the horizon, the rider leans into the bends, the others are passed or come back, a turbo spent is a burst of speed. SPEED, TIME, TURBO and RANK where the game puts them.
- Magician Lord. The villages in the giant trees, then a temple. A hero of our own throws his magic at the undead and takes the shape read in the game. HP and POW at the bottom.
- The score of Strikers 1945 Plus, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling and Magician Lord is in no database. Learn it with `learn.bat`.
- When the stick and the buttons can be read (Neo Geo BIOS), the planes of Strikers 1945 Plus and the witches of Twinkle Star Sprites follow them.
- New panel sprite `sprites/car.png`, a rally car seen from above.
- `demo_neogeo.bat` now lists the twenty-five games.

**Updating from 1.19**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, quatrième lot**
- Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally et Magician Lord ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu d'après des captures du jeu. Ça fait vingt-cinq jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Strikers 1945 Plus. Sur l'écran HD, les deux panneaux de côté du jeu (SCORE, les avions qui restent, BOMB, la jauge SUPER SHOT) autour d'un sol ravagé vu du ciel, des villages aux toits de tuiles crevés, une voie ferrée et son train, une rivière et ses ponts. L'avion choisi par le joueur, dessiné d'après le vrai (P-38, F5U, Spitfire, Ta 152, Zero, Fiat G.56, XP-55). La jauge pleine qui se vide est le super tir, une bombe amène une formation de bombardiers.
- Street Hoop. Un demi-terrain dans un parc, trois contre trois. Les points lus dans le jeu sont des tirs de loin, des tirs en suspension ou des smashs, la jauge SUPER SHOT pleine qui se vide donne un tir enflammé. Les points en grosses lettres rouges et bleues en haut, l'horloge dans son cadre orange en bas.
- Super Dodge Ball. Un terrain vague pavé, deux équipes de trois joueurs à nous. Un joueur dont la vie baisse prend la balle en pleine figure, à zéro il est éliminé, la jauge POW pleine qui se vide donne un tir enflammé. Les barres de vie des deux équipes avec les noms, TIME au milieu.
- Neo Bomberman. Le labyrinthe vu de haut, un style par monde, de petits robots mineurs à nous. Les bombes posées dans le jeu sont posées ici et sautent en croix, les blocs cassent et reviennent.
- Twinkle Star Sprites. Deux terrains côte à côte et la colonne ornée entre les deux, une forêt qui défile vers le bas, de petites sorcières à nous. Les attaques lues dans le jeu passent de l'autre côté, un cœur perdu fait tourner la sorcière, une bombe nettoie son terrain. Pow 1 2 Max et les bombes en bas.
- League Bowling. La salle vue de derrière le joueur. Chaque fois que le chrono du jeu repart, le joueur lance, la boule file en courbe et les quilles volent, STRIKE ! ou SPARE ! de temps en temps.
- Neo Drift Out et Thrash Rally. Les spéciales vues du ciel, terre, goudron ou neige, la voiture dérape dans les virages, une arche de contrôle passe quand du temps s'ajoute. TIME comme dans chaque jeu, et la vitesse dans Thrash Rally.
- Riding Hero. La route vue de derrière la moto file vers l'horizon, le pilote se penche dans les virages, les autres sont dépassés ou reviennent, un turbo dépensé donne un coup d'accélérateur. SPEED, TIME, TURBO et RANK là où le jeu les met.
- Magician Lord. Les villages dans les arbres géants, puis un temple. Un héros à nous lance sa magie sur les morts-vivants et prend la forme lue dans le jeu. HP et POW en bas.
- Le score de Strikers 1945 Plus, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling et Magician Lord n'est dans aucune base. Apprends-le avec `learn.bat`.
- Quand le stick et les boutons se lisent (BIOS Neo Geo), les avions de Strikers 1945 Plus et les sorcières de Twinkle Star Sprites les suivent.
- Nouveau sprite de dalle `sprites/car.png`, une voiture de rallye vue du dessus.
- `demo_neogeo.bat` propose maintenant les vingt-cinq jeux.

**Mettre à jour depuis la 1.19**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.19.0

### English

**Neo Geo games done one by one, third batch**
- Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2 and Aero Fighters 3 now have a file of their own, with a panel scene and an animated HD scene made for each game. That makes fifteen games done one by one. `PROGRESS.md` shows what comes next.
- Top Hunter. On the panel, the lives as small hunters, the timer and the power gauge. On the HD screen, hunters as big as in the game on four planets (forest, ice, wind, fire) with their two lanes, and as in the game leaves, ice or rock across the top of the screen. Robots and walking machines with turbines come on both lanes, the hunter jumps from one lane to the other and punches, throws or shoots them when the score goes up, and the full power gauge that empties is a special move. When the timer starts again for a new stage, the hunters move on to the next planet. At the top, as in the game, the hunter's head with 1UP= and the lives, the score and the power, and TIME next to the logo.
- Baseball Stars 2. On the panel, the runs of both teams with RUN! when one comes in, the balls, strikes and outs lights, and the POW gauges. On the HD screen, the field as in the game's batting view, bright green grass seen from behind home plate, the batter big in front and the pitcher on the mound. Each ball, strike and out read in the game becomes a pitch, called in big rainbow letters as in the game. The batter hits and a fielder catches the ball, and the runs send the ball far and the runners home, with fireworks when it goes over the wall. After the third out, the other team comes to bat. The count is shown in coloured dots, as in the game.
- Last Resort. On the panel, the lives, the power and the speed over a city at night. On the HD screen, the city at night of the game's first stage, giant towers lit with orange windows, purple buildings, the highway with its street lamps and its cars. The unit turns around the ship on the side away from where it goes and fires with it, and now and then it flies straight ahead and comes back. At the top 1P= and the score with the lives, POW at the bottom, as in the game.
- Aero Fighters 2 and 3. On the panel, the lives, the bombs and the power, with the pilot's name in Aero Fighters 3. On the HD screen, seen from the sky as in the games, a city in daylight with its avenues, car parks and parks in Aero Fighters 2, a city by a river at nightfall in Aero Fighters 3. Jets drawn after real fighters, helicopters and tanks in Aero Fighters 2, propeller planes and big bombers in Aero Fighters 3. The planes fly with their shadows below, the enemies blow up when the score goes up, and a bomb clears the screen. The bombs are shown in their frames, as in the games. In Aero Fighters 3, the plane is the one of the pilot chosen by player 1, among twelve.
- The score of Top Hunter, Last Resort and the two Aero Fighters is in no database. Learn it with `learn.bat`.
- When the stick and the buttons can be read (Neo Geo BIOS), the hunters of Top Hunter (up and down change lanes), the ships of Last Resort (button B launches the unit) and the planes of the Aero Fighters follow them.
- `demo_neogeo.bat` now lists the fifteen games.

**HD screen**
- A background prepared while a game runs now appears without a jolt, its layers are made ready a little at each image.

**Updating from 1.18**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, troisième lot**
- Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2 et Aero Fighters 3 ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu. Ça fait quinze jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Top Hunter. Sur la dalle, les vies en petits chasseurs, le chrono et la jauge de puissance. Sur l'écran HD, des chasseurs aussi grands que dans le jeu sur quatre planètes (forêt, glace, vent, feu) avec leurs deux voies, et comme dans le jeu du feuillage, de la glace ou de la roche en haut de l'écran. Des robots et des machines à turbines arrivent sur les deux voies, le chasseur saute d'une voie à l'autre et les frappe, les jette ou leur tire dessus quand le score monte, et la jauge de puissance pleine qui se vide donne un coup spécial. Quand le chrono repart pour un nouveau stage, les chasseurs passent à la planète suivante. En haut, comme dans le jeu, la tête du chasseur avec 1UP= et les vies, le score et la puissance, et TIME à côté du logo.
- Baseball Stars 2. Sur la dalle, les points des deux équipes avec RUN! quand il y en a un, les lampes des balles, des prises et des retraits, et les jauges POW. Sur l'écran HD, le terrain comme dans la vue de frappe du jeu, une herbe vert vif vue de derrière le marbre, le frappeur en grand devant et le lanceur sur le monticule. Chaque balle, prise et retrait lu dans le jeu devient un lancer, annoncé en grosses lettres arc-en-ciel comme dans le jeu. Le frappeur frappe et un joueur attrape la balle, et les points envoient la balle loin et les coureurs au marbre, avec un feu d'artifice quand elle passe le mur. Après le troisième retrait, l'autre équipe passe à la batte. Le compte s'affiche en pastilles de couleur, comme dans le jeu.
- Last Resort. Sur la dalle, les vies, la puissance et la vitesse au-dessus d'une ville la nuit. Sur l'écran HD, la ville la nuit du premier stage du jeu, des tours géantes aux fenêtres orange, des immeubles violets, l'autoroute avec ses réverbères et ses voitures. L'unité tourne autour du vaisseau, du côté opposé à sa route, et tire avec lui, et de temps en temps elle part droit devant puis revient. En haut 1P= et le score avec les vies, POW en bas, comme dans le jeu.
- Aero Fighters 2 et 3. Sur la dalle, les vies, les bombes et la puissance, avec le nom du pilote dans Aero Fighters 3. Sur l'écran HD, vues du ciel comme dans les jeux, une ville en plein jour avec ses avenues, ses parkings et ses parcs dans Aero Fighters 2, une ville au bord d'un fleuve à la tombée de la nuit dans Aero Fighters 3. Des avions de chasse dessinés d'après de vrais avions, des hélicoptères et des chars dans Aero Fighters 2, des avions à hélice et de gros bombardiers dans Aero Fighters 3. Les avions volent avec leur ombre dessous, les ennemis explosent quand le score monte, et une bombe nettoie l'écran. Les bombes s'affichent dans leur cadre, comme dans les jeux. Dans Aero Fighters 3, l'avion est celui du pilote choisi par le joueur 1, parmi douze.
- Le score de Top Hunter, Last Resort et des deux Aero Fighters n'est dans aucune base. Apprends-le avec `learn.bat`.
- Quand le stick et les boutons se lisent (BIOS Neo Geo), les chasseurs de Top Hunter (haut et bas changent de voie), les vaisseaux de Last Resort (le bouton B lance l'unité) et les avions des Aero Fighters les suivent.
- `demo_neogeo.bat` propose maintenant les quinze jeux.

**Écran HD**
- Un décor préparé pendant qu'un jeu tourne s'affiche maintenant sans à-coup, ses couches sont prêtes un peu à chaque image.

**Mettre à jour depuis la 1.18**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

## 1.18.0

### English

**Neo Geo games done one by one, second batch**
- Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11 and Sengoku 3 now have a file of their own, with a panel scene and an animated HD scene made for each game. That makes ten games done one by one. `PROGRESS.md` shows what comes next.
- Pulstar. On the panel, the lives as small ships, the stage and the charge gauge. On the HD screen, one world per stage (Earth, water vein, fire, space station, forest, nebula). The charge glows on the nose of the ship and leaves as a big beam, the pods and the front shield follow the ship, and STAGE comes with the name of the stage.
- Magical Drop III. On the panel, both players' tarot cards, the quota and the level. On the HD screen, two fields of drops under a tarot sky. When the quota goes down, the jester throws a drop and as many pop, a big group makes a chain, the level pushes a row down, and the card flips when the character changes.
- Super Sidekicks 3 and The Ultimate 11. On the panel, the goals of both teams and GOAL! when one goes in, with the power gauges in The Ultimate 11. On the HD screen, the match seen by the TV camera, by day, or at night under the floodlights. When the goals go up, the ball ends in the net, GOAL!, confetti, and the crowd jumps. In The Ultimate 11, a full power gauge that empties fires a super shot on fire.
- Sengoku 3. On the panel, the health and the magic of both players, the timer, the fighter, the throwing weapon and how many are left. On the HD screen, a temple under the moon and shadow warriors. The throwing weapons fly when their count goes down, a warrior falls under the sword when the score goes up, the magic sweeps the screen, and the panel shakes when hit.
- The score of Pulstar, Magical Drop III and Sengoku 3 is in no database. Learn it with `learn.bat`.
- When the stick and the buttons can be read (Neo Geo BIOS), the ship of Pulstar and the jester of Magical Drop III follow them, and button A strikes in Sengoku 3.
- `demo_neogeo.bat` now lists the ten games.

**HD screen**
- A banner can have a line under it, such as the name of the stage in Pulstar.
- Preparing a background while a game runs no longer freezes the display for a moment.

**Updating from 1.17**
Extract the new zip over the old folder (`config.json` and your learned addresses are kept), then run `install.bat` once to update the MAME plugin.

### Français

**Jeux Neo Geo faits un par un, deuxième lot**
- Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11 et Sengoku 3 ont maintenant un fichier à eux, avec une scène de dalle et une scène HD animée faites pour chaque jeu. Ça fait dix jeux faits un par un. `PROGRESS.md` montre ce qui vient ensuite.
- Pulstar. Sur la dalle, les vies en petits vaisseaux, le stage et la jauge de charge. Sur l'écran HD, un monde par stage (la Terre, la veine d'eau, le feu, la station spatiale, la forêt, la nébuleuse). La charge brille au nez du vaisseau et part en gros rayon, les modules et le bouclier avant suivent le vaisseau, et STAGE arrive avec le nom du stage.
- Magical Drop III. Sur la dalle, les cartes de tarot des deux joueurs, le quota et le niveau. Sur l'écran HD, deux champs de gouttes sous un ciel de tarot. Quand le quota baisse, le fou lance une goutte et autant de gouttes éclatent, un gros groupe fait une chaîne, le niveau fait descendre une rangée, et la carte se retourne quand le personnage change.
- Super Sidekicks 3 et The Ultimate 11. Sur la dalle, les buts des deux équipes et BUT ! quand il y en a un, avec les jauges de puissance dans The Ultimate 11. Sur l'écran HD, le match vu par la caméra de télé, de jour, ou de nuit sous les projecteurs. Quand les buts montent, le ballon finit au fond du filet, BUT !, des confettis, et le public saute. Dans The Ultimate 11, une jauge de puissance pleine qui se vide lance un super tir en feu.
- Sengoku 3. Sur la dalle, la vie et la magie des deux joueurs, le chrono, le combattant, l'arme de jet et ce qu'il en reste. Sur l'écran HD, un temple sous la lune et des guerriers de l'ombre. Les armes de jet partent quand leur nombre baisse, un guerrier tombe sous le sabre quand le score monte, la magie balaie l'écran, et le panneau tremble quand on est touché.
- Le score de Pulstar, Magical Drop III et Sengoku 3 n'est dans aucune base. Apprends-le avec `learn.bat`.
- Quand le stick et les boutons se lisent (BIOS Neo Geo), le vaisseau de Pulstar et le fou de Magical Drop III les suivent, et le bouton A frappe dans Sengoku 3.
- `demo_neogeo.bat` propose maintenant les dix jeux.

**Écran HD**
- Un bandeau peut avoir une ligne dessous, comme le nom du stage dans Pulstar.
- Préparer un décor pendant qu'un jeu tourne ne fige plus l'affichage un instant.

**Mettre à jour depuis la 1.17**
Décompresse le nouveau zip par-dessus l'ancien dossier (`config.json` et tes adresses apprises sont gardés), puis lance `install.bat` une fois pour mettre à jour le plugin MAME.

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
