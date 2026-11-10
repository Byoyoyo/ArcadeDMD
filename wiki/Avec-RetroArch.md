ArcadeDMD lit les jeux lancés dans RetroArch sans aucun plugin. RetroArch partage la mémoire du jeu par ses « commandes réseau », qui restent sur le PC lui-même.

## Réglage, une seule fois

1. RetroArch 1.19 ou plus récent (Information, Informations système montre la version).
2. Réglages, Réseau, active « Commandes réseau ». Laisse le port à 55355.
3. Laisse « Mettre en pause quand inactif » activé (Réglages, Interface utilisateur). C'est le réglage par défaut, et `learn.bat` s'en sert.
4. Lance le jeu avec un cœur qui partage sa mémoire (juste en dessous).

Rien d'autre à installer. Dès qu'ArcadeDMD tourne, il surveille RetroArch tout seul. Le journal dit « RetroArch 1.19.x détecté (commandes réseau actives) », puis le cœur chargé pour chaque jeu.

## Le bon cœur

Tous les cœurs ne donnent pas à RetroArch l'accès à la mémoire du jeu. Avec le mauvais cœur, la scène s'affiche mais sans aucune valeur.

| Système | Cœur qui marche | Cœurs qui ne marchent pas |
|---|---|---|
| Arcade, Neo Geo, Capcom CPS1 à CPS3, Cave | Arcade (FinalBurn Neo), à jour | FB Alpha 2012 sous toutes ses formes, MAME 2003, MAME 2003-Plus, MAME 2010, MAME |
| Mega Drive (Sonic) | Genesis Plus GX, ou PicoDrive | |

Installer FinalBurn Neo.

1. Menu principal, Mise à jour en ligne, Téléchargement de cœurs, « Arcade (FinalBurn Neo) ». Si Mise à jour en ligne est cachée, active-la dans Réglages, Interface utilisateur, Visibilité des éléments de menu, Menu principal.
2. Pour l'essayer, Menu principal, Charger un cœur, Arcade (FinalBurn Neo), puis Charger du contenu et choisis le jeu (`mslug.zip`, par exemple).
3. Si le jeu refuse de démarrer, il manque sûrement un BIOS. Mets un `neogeo.zip` récent à côté du jeu.
4. Si tu lances tes jeux depuis HyperSpin, RocketLauncher ou LaunchBox, change aussi là-bas le cœur choisi pour ce système.

## Jeux prévus

| Jeu | Cœur RetroArch | Affiché tout de suite | À apprendre |
|---|---|---|---|
| Metal Slug (`mslug`) | FinalBurn Neo | score de chaque joueur, vies, bombes, les grenades à l'écran, arme et munitions, les prisonniers libérés, la mission, le char (dedans ou pas, son énergie et ses obus) | rien |
| Metal Slug 2 (`mslug2`) | FinalBurn Neo | score de chaque joueur, vies, bombes, les grenades à l'écran, arme et munitions, le soldat choisi, les prisonniers de la mission, le véhicule de chaque joueur (l'adresse du véhicule tant qu'on est dessus, lequel, son énergie et ses obus), la mission (RetroAchievements et la base de triche, les nouvelles valeurs à vérifier) | rien |
| Metal Slug X (`mslugx`) | FinalBurn Neo | le score de chaque joueur, vies, bombes, les grenades à l'écran, arme et munitions, le soldat choisi, les prisonniers libérés, le véhicule de chaque joueur (sa propre adresse tant qu'il monte quelque chose, lequel, son énergie et ses obus), la mission, le chrono, la vie de tous les ennemis (l'Iron Nokana MKII et les gros ont leur barre), le drapeau de fin et le MISSION COMPLETE du jeu lui-même | les valeurs du joueur 2 et les boss des missions 2 à 6 par leur vie, à confirmer en jouant |
| Metal Slug 3 (`mslug3`) | FinalBurn Neo | le score de chaque joueur, vies, bombes, les grenades à l'écran, arme et munitions, le soldat choisi, les prisonniers libérés, le véhicule (lequel), la mission, les vies de tous les ennemis à l'écran (Huge Hermit, Sol Dae Rokker et les gros ennemis ont leur barre), le MISSION COMPLETE du jeu lui-même à chaque mission (son compteur de fin) | l'énergie et les missiles des véhicules, le Camel Slug de la mission 4, les boss des missions 2, 3 et 5 par leur vie |
| Metal Slug 6, le bootleg de Metal Slug 3 (`mslug3b6`) | FinalBurn Neo | tout ce que Metal Slug 3 lit, sous le nom Metal Slug 6, avec son propre compte des missions (il joue celles de Metal Slug 3 dans un autre ordre) et son code de pistolet | comme Metal Slug 3 |
| Metal Slug 4 (`mslug4`) | FinalBurn Neo | le score de chaque joueur, vies, bombes, les grenades à l'écran, arme et munitions, le soldat choisi, les prisonniers de la mission, dans un véhicule ou pas et son énergie, la mission, la vie de tous les ennemis (le boss parmi eux, par phases) et la fin de mission | quel véhicule |
| Metal Slug 5 (`mslug5`) | FinalBurn Neo | le score de chaque joueur, vies, bombes, les grenades à l'écran, arme et munitions, le soldat choisi, les prisonniers libérés, le véhicule (lequel) et son énergie, la mission, la vie de tous les ennemis (le Metal Rear et les gros ont leur barre), le drapeau de boss et le MISSION COMPLETE du jeu lui-même | les boss des missions 2 à 5 par leur vie |
| Twinkle Star Sprites (`twinspri`) | FinalBurn Neo | score, cœurs (avec les demis), bombes, jauge Pow, personnage, chaîne et PERFECT de chaque joueur, l'étape, la place de chaque joueur dans le jeu (sa sorcière sur l'écran HD la suit), les manches gagnées | rien |
| Les 57 jeux de combat Neo Geo (King of Fighters, Samurai Shodown, Fatal Fury, Last Blade, World Heroes...) | FinalBurn Neo | voir [[Jeux de combat]] | le score des jeux que le tableau ci-dessous marque à apprendre |
| Blazing Star (`blazstar`), Puzzle Bobble (`pbobblen`), Shock Troopers (`shocktro`), Pulstar (`pulstar`), Magical Drop III (`magdrop3`), Sengoku 3 (`sengoku3`), Top Hunter (`tophuntr`), Last Resort (`lresort`), Aero Fighters 2 (`sonicwi2`), Aero Fighters 3 (`sonicwi3`), Strikers 1945 Plus (`s1945p`), Super Dodge Ball (`sdodgeb`), Neo Bomberman (`neobombe`), League Bowling (`lbowling`), Magician Lord (`maglord`), NAM-1975 (`nam1975`), Cyber-Lip (`cyberlip`), Ghost Pilots (`gpilots`), Alpha Mission II (`alpham2`), Viewpoint (`viewpoin`), Zed Blade (`zedblade`), Prehistoric Isle 2 (`preisle2`), Shock Troopers 2nd Squad (`shocktr2`), Robo Army (`roboarmy`), Burning Fight (`burningf`), Mutation Nation (`mutnat`), Sengoku (`sengoku`), Sengoku 2 (`sengoku2`), Ninja Combat (`ncombat`), Ninja Commando (`ncommand`), Blue's Journey (`bjourney`), Puzzle Bobble 2 (`pbobbl2n`), Magical Drop II (`magdrop2`), Money Puzzle Exchanger (`miexchng`), Puzzle De Pon! (`puzzledp`), Puzzle De Pon! R! (`puzzldpr`), Panic Bomber (`panicbom`), Pop 'n Bounce (`popbounc`), Super Bubble Pop (`sbp`), Spin Master (`spinmast`), Ganryu (`ganryu`), Zupapa! (`zupapa`), Neo Mr. Do! (`neomrdo`), Bang Bead (`bangbead`), Battle Flip Shot (`flipshot`), Gururin (`gururin`), Ghostlop (`ghostlop`), Pochi and Nyaa (`pnyaa`), Puzzled (`joyjoy`), Zintrick (`zintrckb`), Digger Man (`diggerma`), Andro Dunos (`androdun`), Captain Tomaday (`ctomaday`), Choutetsu Brikin'ger (`ironclad`), Last Hope (`lasthope`), Bang Bang Busters (`b2b`), Crossed Swords (`crsword`), Eight Man (`eightman`), Nightmare in the Dark (`nitd`), The Super Spy (`superspy`), Quiz King of Fighters (`quizkof`), Quiz Daisousa Sen (`quizdais`), Quiz Meitantei Neo & Geo (`quizdai2`), Chibi Maruko-chan Deluxe Quiz (`marukodq`) | FinalBurn Neo | voir [[Jeux Neo Geo]] | score |
| Windjammers (`wjammers`), Neo Turf Masters (`turfmast`), Super Sidekicks 3 (`ssideki3`), The Ultimate 11 (`ssideki4`), Baseball Stars 2 (`bstars2`), Street Hoop (`strhoop`), Neo Drift Out (`neodrift`), Riding Hero (`ridhero`), Thrash Rally (`trally`), Super Sidekicks (`ssideki`), Super Sidekicks 2 (`ssideki2`), Tecmo World Soccer '96 (`twsoc96`), Goal! Goal! Goal! (`goalx3`), Neo-Geo Cup '98 (`neocup98`), Soccer Brawl (`socbrawl`), Football Frenzy (`fbfrenzy`), Pleasure Goal (`pgoal`), Baseball Stars Professional (`bstars`), 2020 Super Baseball (`2020bb`), Top Player's Golf (`tpgolf`), Power Spikes II (`pspikes2`), Over Top (`overtop`), Stakes Winner (`stakwin`), Stakes Winner 2 (`stakwin2`), Jockey Grand Prix (`jockeygp`), The Irritating Maze (`irrmaze`), Minasan no Okagesamadesu! (`minasan`), Mahjong Kyo Retsuden (`mahretsu`), Janshin Densetsu (`janshin`), Bakatonosama Mahjong Manyuuki (`bakatono`), Idol Mahjong Final Romance 2 (`froman2b`), Shougi no Tatsujin (`moshougi`) | FinalBurn Neo | voir [[Jeux Neo Geo]] | rien |
| Tous les autres jeux Neo Geo | FinalBurn Neo | scène selon le genre (crédits avec MAME) | score, crédits si le jeu en garde une copie |
| Tous les jeux Capcom CPS1, CPS2 et CPS3 | FinalBurn Neo | voir [[Capcom et Cave]] | score |
| Sonic 1 et Sonic 2 | Genesis Plus GX | score, anneaux, vies | rien |

Les adresses des vies, bombes et munitions viennent de la base de codes de triche de MAME 2003-Plus. Celles de Sonic sont les mêmes que dans MAME. Les vies des Metal Slug suivent le « 1UP » de l'écran. Metal Slug 1 compte aussi la vie en cours, ArcadeDMD enlève donc 1 (vérifié). Metal Slug 3 ne la compte pas (vérifié). Pour 2 et X, ArcadeDMD fait comme pour le 1, et pour 4 et 5 comme pour le 3. Si un de ces jeux affiche une vie de moins que l'écran, enlève les lignes `"add"` et `"min"` de ses vies dans son fichier `games\mslugX.json`. S'il en affiche une de plus, ajoute `"add": -1, "min": 0`.

À deux joueurs, la scène change toute seule dès que le joueur 2 appuie sur Start. Le BIOS de la Neo Geo indique qui est en jeu. En haut, comme dans le jeu, « 1UP= » et les vies du joueur 1 à gauche, « 2UP= » et celles du joueur 2 à droite, avec le titre qui défile entre les deux. Dessous, chaque score sous son 1UP ou son 2UP. « SCORE ? » en gris veut dire que ce score n'est pas encore appris. En bas, les bombes puis l'arme de chaque joueur passent à tour de rôle, avec « P1 » en vert et « P2 » en jaune. Si seul le joueur 2 joue, la scène normale s'affiche avec ses valeurs à lui. Les crédits des Neo Geo ne se lisent qu'avec MAME (voir [[Jeux Neo Geo]]).

Les scènes des Metal Slug s'inspirent de la vidéo de Vera, adaptées à une dalle 128x32 pour que rien ne passe sous le décor. En haut, « SNK » en bleu puis « - METAL SLUG » (avec le numéro du jeu) en blanc défilent lentement. Dessous, « P1 » en vert et le score en blanc à gauche, les vies à droite. La ligne suivante alterne les bombes, l'arme avec ses munitions (pistolet, mitraillette, fusil à pompe, lance-flammes, lance-roquettes, laser, tête chercheuse... un « + » indique la version améliorée) et les crédits avec MAME. Tout en bas, des petites collines et un petit char moins lumineux qui avance et tire quand le score monte.

Les scores de Metal Slug et de Metal Slug 3 sont déjà dans leurs fichiers, trouvés avec `learn.bat` sous RetroArch et FinalBurn Neo. Pour remplacer le char par ton propre dessin, dépose `mslug_tank.gif` (ou `mslug_tank.png` en bande de 3 images) dans `sprites\`. Il doit tenir sur 5 pixels de haut, canon vers la droite.

## Vérifier

Lance `test_retroarch.bat` pendant un jeu. Il montre la version de RetroArch, le cœur chargé, le résultat de la lecture de la mémoire et les valeurs lues, et dit quoi faire si quelque chose ne va pas. Le résultat est aussi enregistré dans `runtime\test_retroarch.txt`. Il dit aussi quel fichier de jeu prend une version, un bootleg ou un hack.

## Crédits et pièces

RetroArch ne dit ni quand une pièce entre ni par quelle fente, et FinalBurn Neo ne partage pas la mémoire de sauvegarde de la MVS où la Neo Geo garde ses crédits. ArcadeDMD les devine d'après les traces que le BIOS Neo Geo laisse dans la RAM de travail.

`coin_buttons.bat` fait beaucoup mieux. Lance-le une fois, appuie sur le bouton de pièce de gauche, celui de droite, le START du joueur 1 et le START du joueur 2. ArcadeDMD lit alors ces boutons lui-même, sur les manettes ou le clavier, en même temps que RetroArch et sans les lui prendre. Il voit chaque pièce et son côté, pendant une partie aussi, et chaque joueur qui appuie sur START.

- Sur l'écran HD, la pièce tombe dans la fente du côté où tu l'as mise.
- Une MVS donne 2 crédits pour une pièce dans sa deuxième fente, sauf si ses réglages ont été changés. ArcadeDMD compte pareil, `"mvs_credits": [1, 2]` dans la section `coin_buttons`. Si tu l'as changé dans le menu de la MVS, mets la même chose ici, `[1, 1]` par exemple.
- Tant que le menu de RetroArch est ouvert, les boutons bougent dans le menu et ArcadeDMD ne compte aucune pièce.
- Si tu branches tes manettes sur d'autres ports USB, relance `coin_buttons.bat`, Windows a pu changer leur numéro.

## Enregistrement

Sous RetroArch, ArcadeDMD enregistre chaque partie (les valeurs, la mémoire, des captures d'écran) pour qu'un jeu puisse être réglé sans la borne. Voir [[Enregistrer une partie]].

## Le couper

`"enabled": false` dans la section `retroarch` de `config.json`.

## Bon à savoir

- Un jeu RetroArch sans fichier dans `games\` ne change rien sur la Pixelcade (sauf avec `"takeover": "all"`).
- Dans `config.json`, rubrique `retroarch`, `"enabled": false` coupe la surveillance.
- Si le journal dit « RetroArch refuse de lire la mémoire du jeu », c'est le cœur qui ne la donne pas. Le journal dit lequel est chargé et quoi faire.
- **Captures des jeux de combat** (depuis la 1.33). Pendant une partie, chaque changement de chaque valeur lue est écrit avec son heure dans `runtime\captures\<jeu>-<date>.log`, quelques centaines de Ko par match, avec MAME comme avec RetroArch. Un match par jeu (deux rounds gagnés, un perdu, un super coup) suffit pour le rejouer dans le moteur de combat sans le jeu, régler le fichier du jeu (ses écrans de sélection, l'état de ses combats, son round, ses stocks) et garder la capture comme test. Pour signaler un jeu de combat dont ROUND, FIGHT !, K.O. ou VS viennent au mauvais moment, zippe ce dossier et envoie-le avec une issue GitHub. `"capture"` dans `config.json` : `"all"` (tous les jeux, par défaut), `"fights"` (les jeux de combat seuls) ou `"off"`. `python tools\replay_capture.py runtime\captures\<fichier>` écrit ce que l'écran HD a montré seconde par seconde, `--frames 30,47` le dessine à ces secondes. Les captures déjà reçues sont gardées dans `tests\captures` et rejouées comme tests : The King of Fighters '98 et '99, Fatal Fury, Windjammers, les Metal Slug. Pour trouver où un jeu range ce qui n'est pas encore lu (la vie d'un boss, le type d'un véhicule), toute la mémoire que RetroArch partage est enregistrée pour tous les jeux, quatre fois par seconde en différences compressées, dans `runtime\captures\<jeu>-<date>.ram` (`"ram_dump": {"enabled": true, "every": 0.25}` sous `"retroarch"` dans `config.json`, quelques Mo pour dix minutes ; `"ram_dump": true` dans le fichier d'un jeu le force pour ce jeu), et `python tools\ram_diff.py <fichier.ram> --down 120 160` liste les mots qui ne font que descendre entre deux moments (`--watch 0x1012AA` en suit un, `--diff 118 121` montre ce qui a changé). Pour voir ce que l'écran montrait quand un octet a bougé, ArcadeDMD demande une capture d'écran à RetroArch (sa commande `SCREENSHOT` sur le même port que les lectures mémoire) à la première lecture, toutes les deux secondes pendant qu'on joue et tout de suite quand une vie, une mission, un véhicule ou un drapeau du jeu change (`"screenshots": {"enabled": true, "every": 2.0, "dir": ""}` sous `"retroarch"` ; mets dans `"dir"` le `screenshot_directory` de RetroArch et le journal dit si la première image est bien apparue). Mieux vaut couper la notification et le flash de RetroArch à chaque capture (Réglages, Affichage à l'écran, Notifications, Notification de capture d'écran et Flash de capture d'écran). Un bouton pièce tenu une bonne seconde pose un repère : `marker n` dans la capture avec son heure, une capture d'écran et une ligne dans le journal, pour dire « ici » quand quelque chose à regarder se produit (chaque appui pièce est aussi dans la capture, `coin_press n`).
