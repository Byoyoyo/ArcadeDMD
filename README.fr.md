# ArcadeDMD

English version: [README.md](README.md)

Score, vies, crédits et événements des jeux MAME et RetroArch en direct sur le marquee d'une borne d'arcade, avec une scène animée propre à chaque jeu. Sur une dalle LED 128x32 (**Pixelcade LED**, **ZeDMD**), ou en HD lisse sur un écran LCD de marquee (le marquee 1920 x 460 d'une Vewlix par exemple).

![Jeu de combat sur un marquee LCD, affichage HD](docs/images/hd_fight.jpg)
![Écran des pièces d'un jeu de combat sur un marquee LCD, affichage HD](docs/images/hd_coin_screen.jpg)
![Metal Slug sur un marquee LCD, affichage HD](docs/images/hd_metal_slug.jpg)
![Logo du jeu, écran des pièces et combat sur une dalle LED 128x32](docs/images/led_fight.gif)
![Metal Slug sur une dalle LED 128x32](docs/images/led_metal_slug.gif)

- Lit la mémoire du jeu en direct, avec un plugin MAME ou par les commandes réseau de RetroArch (FinalBurn Neo, Genesis Plus GX). Rien n'est modifié dans le jeu ni dans l'émulateur.
- Scènes prêtes pour Metal Slug 1 à 5 et X, les 57 jeux de combat Neo Geo, quatre-vingt-dix-sept jeux Neo Geo faits un par un (Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers, Neo Turf Masters, Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11, Sengoku 3, Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2, Aero Fighters 3, Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally, Magician Lord, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army, Burning Fight, Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger, Puzzle De Pon!, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks, Super Sidekicks 2, Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf, Power Spikes II, Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa, Puzzled, Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords, Eight Man, Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2, Shougi no Tatsujin), tous les autres jeux Neo Geo selon leur genre, tous les jeux Capcom CPS1, CPS2 et CPS3 (34 jeux de combat dans leurs décors et cinquante jeux faits un par un, de Final Fight à 1944), After Burner II, Sonic 1 et 2.
- Scènes HD avec des décors animés qui suivent le stage ou la mission du jeu, et un effet pour chaque événement (coups, combos, K.O., armes, bombes, pièces...).
- Le logo du jeu au lancement (ton Clear Logo LaunchBox). Quand personne ne joue, les jeux de combat attendent une pièce. Mets-en une, elle tombe dans la fente, les crédits roulent, puis PRESS START.
- Un outil d'apprentissage trouve les adresses manquantes (score, crédits...) à partir de quelques captures.
- En anglais et en français. Windows, Python 3.12 ou plus récent.

Comment ça marche, en une phrase. Un plugin MAME lit les valeurs dans la RAM du jeu, un petit programme Python dessine la scène et l'envoie à la dalle en USB, ou l'affiche sur un écran LCD qui sert de DMD (section 3).

Télécharge la dernière version sur la page [Releases](../../releases), puis suis la section 2. Les changements de chaque version sont dans [CHANGELOG.md](CHANGELOG.md), et l'avancement jeu par jeu, avec la suite, dans [PROGRESS.md](PROGRESS.md). Pour signaler un problème ou demander un nouveau jeu, vois [CONTRIBUTING.md](CONTRIBUTING.md).

Tu as déjà une Pixelcade LED ? Elle suffit, pas besoin d'acheter de dalle. Va directement aux sections 2 et 4. Pour les jeux lancés dans RetroArch (Metal Slug, Sonic...), lis aussi la section 7.

Contenu du dossier

| Fichier | Rôle |
|---|---|
| `install.bat` | installe tout (Python requis, voir plus bas) |
| `demo_afterburner.bat`, `demo_sonic.bat` | montrent les scènes avec des valeurs simulées, sans MAME |
| `run.bat` | démarre le moteur avec la console visible |
| `learn.bat` | outil qui trouve une adresse RAM manquante (score, crédits...) |
| `test_pixelcade.bat` | mire de test sur la Pixelcade LED |
| `screen_setup.bat` | place la scène sur un écran LCD qui sert de DMD, en LED virtuelles ou en HD lisse avec le logo du jeu (section 3) |
| `demo_fight.bat` | démo d'un jeu de combat (King of Fighters '98) avec des valeurs simulées |
| `demo_neogeo.bat` | démo d'un jeu Neo Geo fait un par un (Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers, Neo Turf Masters, Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11, Sengoku 3, Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2, Aero Fighters 3, Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally, Magician Lord, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army, Burning Fight, Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger, Puzzle De Pon!, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks, Super Sidekicks 2, Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf, Power Spikes II, Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa, Puzzled, Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords, Eight Man, Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2, Shougi no Tatsujin) avec des valeurs simulées |
| `demo_capcom.bat` | démo d'un jeu Capcom CPS1, CPS2 ou CPS3 avec des valeurs simulées |
| `test_retroarch.bat` | vérifie RetroArch, le cœur chargé et la lecture de la mémoire (section 7) |
| `test_coins.bat` | note ce que fait le BIOS de la Neo Geo quand une pièce entre avec RetroArch, à envoyer si une pièce ne tombe pas (section 7) |
| `coin_buttons.bat` | montre à ArcadeDMD tes deux boutons de pièce et tes deux boutons START, pour qu'il voie chaque pièce et son côté, et chaque joueur qui commence, avec RetroArch (section 7) |
| `ports.bat` | liste les ports COM, pour trouver celui de la Pixelcade |
| `test_panel.bat` | mire de test sur une dalle ZeDMD |
| `config.json` | tes réglages (Pixelcade, RetroArch, fenêtre LED virtuelles...), créé par l'installeur à partir de `config.default.json`. Une nouvelle version d'ArcadeDMD ne l'écrase jamais |
| `games\*.json` | un fichier par jeu, avec les adresses RAM et la scène. Les fichiers `neogeo*.json` servent de scènes communes aux jeux Neo Geo, une par genre, et les fichiers `cps_*.json` aux jeux Capcom |
| `learned\` | copie des adresses trouvées par `learn.bat`. Remises en place toutes seules après une mise à jour |
| `mame-plugin\arcadedmd` | le plugin à copier dans `MAME\plugins` (l'installeur le fait) |
| `sprites\` | petits sprites (avion, anneau). Tu peux ajouter les tiens |
| `obs\` | fichiers texte mis à jour en direct pour OBS, historique des matchs VS et records de séries (section 11) |
| `fonts\` | polices Inter et Black Ops One de l'affichage HD (licence libre OFL, dans `fonts\OFL.txt` et `fonts\OFL-BlackOpsOne.txt`) |

---

## 1. Le matériel (seulement si tu n'as pas de Pixelcade)

Un DMD RGB 128x32, ce sont deux modules LED HUB75 de 64x32 côte à côte. C'est exactement le format ZeDMD, le DMD libre bien connu du monde du flipper virtuel. On s'appuie dessus pour la partie dalle.

### Option A, le plus simple (pack prêt à brancher)

Des boutiques vendent des ZeDMD montés ou des cartes prêtes à l'emploi, par exemple en France.
- SmallCab, « Pack ZeDMD S3 – P2.5 » https://www.smallcab.net/pack-zedmd-p-3182.html
- Benfactory, « ZeDMD » https://benfactory.fr/produit/zedmd/

En P2.5 (2,5 mm entre deux LED) la dalle fait environ 32 × 8 cm. C'est la taille d'un DMD de flipper. Vérifie sur la page ce qui est inclus (alimentation, cadre).

### Option B, une dalle plus grande

Avec des LED plus grosses (P4 ou P5), la dalle occupe tout le dessus de la borne. Mesure le dessus de ta borne et choisis.

| Pas | Taille d'un module 64x32 | Dalle 128x32 complète |
|---|---|---|
| P3 | 19,2 × 9,6 cm | 38 × 10 cm |
| P4 | 25,6 × 12,8 cm | 51 × 13 cm |
| P5 | 32 × 16 cm | 64 × 16 cm |

Liste d'achats pour l'option B (ordres de grandeur de prix)

| Quantité | Article | Remarque |
|---|---|---|
| 2 | Module LED RGB HUB75 64x32, intérieur, scan 1/16 | Waveshare P4 vers 18 $ pièce, moins cher sur AliExpress |
| 1 | ESP32-S3-DevKitC-1 **N16R8** | vers 10 à 15 €, c'est la carte recommandée par ZeDMD |
| 1 | Shield ZeDMD pour ESP32-S3 (SmallCab, Benfactory, Arnoz) | évite de câbler 14 fils à la main, et ajoute les boutons du menu |
| 1 | Alimentation 5 V 10 A (type Mean Well LRS-50-5) | un module peut tirer 4 A en plein blanc, un DMD reste loin de ça |
| 1 | Câble USB-C **data** | vers le PC de la borne |

Évite les modules « outdoor » ou en scan 1/8. Les modules avec puces FM6126A ou ICN2038S marchent aussi, il suffit de régler le « panel driver » avec ZeDMD_Updater2.

### Montage

1. Branche le shield sur l'entrée HUB75 du premier module (la flèche imprimée au dos indique le sens des données).
2. Relie la sortie du module 1 à l'entrée du module 2 avec la nappe fournie.
3. Alimente les deux modules en 5 V depuis l'alimentation.
4. Relie l'ESP32-S3 au PC par son port USB **natif** (celui marqué USB, à gauche sur la DevKitC-1).

Sans shield, le câblage fil à fil est donné dans le README de ZeDMD (tableau « ZeDMD pinout diagram ») https://github.com/PPUC/ZeDMD

### Firmware de la dalle

1. Télécharge ZeDMD_Updater2 (Windows) https://github.com/zesinger/ZeDMD_Updater2 et flashe la variante **ZeDMD S3 128x32**. Autre possibilité, le fichier `.bin` des releases ZeDMD avec esptool.
2. Au premier démarrage la dalle affiche un menu. Règle l'ordre des couleurs (le rouge doit être rouge), la luminosité, « USB packet size » à 1024 et « min refresh » vers 90 Hz, puis va sur **Exit**.
3. Si la dalle vient d'un pack déjà flashé, mets quand même le firmware à jour. La bibliothèque libzedmd récente attend un firmware récent.

### Option C, un écran LCD à la place des LED

Un écran LCD affiche les scènes en HD lisse, avec les décors animés (section 3). N'importe quel écran que Windows voit comme un écran en plus convient, branché au PC en HDMI, DisplayPort ou USB-C. Pour un marquee, cherche un « stretched bar LCD », un écran très long et très fin. Les mêmes écrans sont vendus pour l'affichage en rayon des magasins et pour les panneaux de capteurs des PC.

Mesure d'abord la fenêtre du marquee de ta borne, puis prends la plus grande surface visible qui rentre.

| Taille | Résolution | Surface visible, environ | Remarque |
|---|---|---|---|
| 12,3" | 1920 × 720 | 29 × 11 cm | proche de la taille d'un DMD de flipper |
| 14,9" | 1280 × 390 | 36 × 11 cm | vendu en kit marquee pour les bornes de type Vewlix |
| 19" | 1920 × 360 | 48 × 9 cm | |
| 24" | 1920 × 360 | 58 × 11 cm | le format des marquees LCD faits pour l'AtGames Legends Ultimate |

Les scènes HD s'adaptent à l'écran. Elles ont été vérifiées en 1920 × 360, 1280 × 390, 1920 × 480 et 1920 × 720.

Où acheter (prix relevés en octobre 2026)
- AliExpress, Amazon ou eBay. Cherche « stretched bar LCD HDMI » suivi de la résolution. Prends une version vendue avec sa carte contrôleur HDMI et son alimentation. Une dalle nue (connecteur LVDS ou eDP) demande une carte contrôleur à part. Un 19" 1920 × 360 vendu avec sa carte était annoncé vers 260 $ plus le port sur eBay, envoyé de Chine, et un 24" vers 250 £ plus le port. Le module 24" nu mesure 61,3 × 13,2 cm pour 1 cm d'épaisseur, prévois un cadre pour le tenir dans le marquee.
- Waveshare 12.3inch 1920x720 LCD, en HDMI ou USB-C, vers 110 $, vu par Windows comme un écran normal https://www.waveshare.com/product/displays/12.3inch-1920x720-lcd.htm
- Arcade Game Sales, marquee LCD 14,9" 1280 × 390 avec cadre métal, pour bornes Vewlix, Chewlix et Game Wizard Xtreme, vers 225 $, en VGA et HDMI https://arcade-game-sales.com/products/lcd-arcade-marquee-for-arcade-cabinets/19366-2.html
- Un écran de PC classique marche aussi, si le haut de la borne est assez profond et assez haut pour le loger. Cache ce qui dépasse de la fenêtre du marquee, et règle la fenêtre d'ArcadeDMD sur la bande visible avec `x`, `y`, `width` et `height` (section 3).

ArcadeDMD dessine seulement sur un écran que Windows voit comme un écran. Vérifie-le avant d'acheter un marquee livré avec son propre logiciel, comme le Pixelcade LCD (il a son propre petit ordinateur et se pilote par le réseau) ou l'AtGames Legends BitLCD HD (il se branche en USB et se pilote avec sa propre application).

---

## 2. Le logiciel

### Installation

1. Il faut Python 3.12 ou plus récent. S'il manque, `install.bat` propose de l'installer (Python 3.13, depuis python.org). Sinon installe-le depuis https://www.python.org/downloads/ en cochant « Add python.exe to PATH ». Il faut aussi MAME 0.227 ou plus récent, l'installeur affiche ta version.
2. Avant d'extraire le zip, fais un clic droit dessus, Propriétés, coche « Débloquer » puis OK. Windows ne posera plus de question à chaque fichier .bat.
3. Extrais le dossier `ArcadeDMD` dans un chemin sans accent, idéalement `C:\ArcadeDMD`. MAME ne sait pas ouvrir les dossiers avec accents.
4. Lance `install.bat`. Il installe Pillow, pyserial et pygame-ce, copie le plugin dans MAME, règle la Pixelcade et propose le lancement automatique au démarrage de Windows. Il ne télécharge libzedmd (le pilote des dalles ZeDMD) que si tu dis avoir une dalle ZeDMD. Si tu n'utilises que RetroArch, appuie sur Entrée à la question sur MAME.

### Ce que l'installation modifie

- Le dossier `C:\ArcadeDMD`. Les réglages, le journal et les captures restent dedans.
- Dans MAME, un nouveau dossier `plugins\arcadedmd` avec trois petits fichiers. Rien d'autre dans MAME. `mame.ini` et `plugin.ini` ne sont pas modifiés, MAME charge tout seul les plugins de son dossier `plugins`.
- Un fichier `ArcadeDMD.bat` dans le dossier Démarrage de Windows, seulement si tu acceptes le lancement automatique.
- Trois bibliothèques ajoutées à Python (Pillow, pyserial, pygame-ce).
- Pendant les jeux qui ont un fichier dans `games\` (Metal Slug, jeux Neo Geo, After Burner II, Sonic...), ArcadeDMD arrête pixelweb et le relance à la fin de la partie. Pour les autres jeux, rien ne change.

Le plugin ne fait que lire la mémoire du jeu. Il ne change ni le jeu, ni les touches, ni les réglages de MAME.

### Et DOFLinx

ArcadeDMD ne touche pas aux fichiers de DOFLinx, ni au réglage `output` de `mame.ini` dont DOFLinx a besoin. MAME fait tourner plusieurs plugins en même temps, celui de DOFLinx et celui d'ArcadeDMD ne se gênent pas. Avec la Pixelcade et sans ZeDMD, ArcadeDMD n'ouvre aucun autre port COM, les appareils pilotés par DOFLinx ne sont donc pas dérangés. Le seul point commun est la Pixelcade elle-même. Pendant After Burner II et Sonic, c'est la scène d'ArcadeDMD qui s'y affiche.

### Tout enlever

Supprime le dossier `plugins\arcadedmd` de MAME, le fichier `ArcadeDMD.bat` du dossier Démarrage (tape `shell:startup` dans Win+R pour l'ouvrir), puis le dossier `C:\ArcadeDMD`. Pour seulement couper le plugin sans rien supprimer, ajoute la ligne `arcadedmd 0` dans le fichier `plugin.ini` de MAME.

### libzedmd (dalle ZeDMD seulement)

Si le téléchargement de libzedmd échoue, prends l'archive `win-mingw-x64-Release` sur https://github.com/PPUC/libzedmd/releases et copie toutes ses DLL dans `ArcadeDMD\libzedmd\`. Prends bien la version mingw, l'autre archive n'embarque pas les DLL dont zedmd64.dll a besoin.

### Vérifier le plugin dans MAME

Lance un jeu, appuie sur Tab, puis « Options des plugins » (Plugin Options). Tu dois voir **ArcadeDMD** avec le jeu détecté et les valeurs lues en direct. S'il n'apparaît pas, vérifie dans le menu Plugins de MAME qu'il est bien activé, ou ajoute la ligne `arcadedmd 1` dans `plugin.ini` (dossier de MAME ou `ini\`).

Le plugin n'a besoin d'aucun réglage dans ton frontend (HyperSpin, LaunchBox...), il est chargé par MAME à chaque lancement.

### Premier essai sans MAME

`demo_afterburner.bat` et `demo_sonic.bat` ouvrent une fenêtre « LED virtuelles » avec des valeurs simulées. Si la dalle est branchée, elle affiche la même chose.

### En vrai

Lance `run.bat` (ou laisse le démarrage automatique faire), puis lance un jeu depuis ton frontend ou directement dans MAME. La Pixelcade passe à ArcadeDMD pendant les jeux qui ont leur fichier dans `games\` et reste à pixelweb le reste du temps. Une dalle ZeDMD, elle, reste noire hors jeu, et affiche le titre qui défile pour un jeu sans fichier dédié. L'ancien écran d'attente (l'heure et « INSERT COIN ») revient avec `"idle": {"show": true}` dans `config.json`.

### Langue

Les messages et les textes affichés à l'écran sont en anglais par défaut. Ils passent tout seuls en français quand Windows est en français. Pour choisir la langue, mets `"language"` dans `config.json`, au premier niveau (pas dans une section). `"auto"` suit la langue de Windows (réglage par défaut), `"en"` force l'anglais et `"fr"` force le français.

```json
"language": "fr"
```

---

## 3. Écran LCD ou marquee en « LED virtuelles »

ArcadeDMD dessine la scène sur n'importe quel écran branché en plus, par exemple le LCD d'une borne qui sert de DMD, ou un marquee 1920×470. Ça marche avec RetroArch comme avec MAME.

Le plus simple, lance `screen_setup.bat` (l'installeur le propose aussi). Il liste les écrans, devine celui qui sert de DMD (le plus allongé) et règle tout dans `config.json`. Lance ensuite `run.bat` ou `demo_afterburner.bat` pour voir le résultat.

Sur un grand écran, la scène s'affiche deux fois plus fine qu'une vraie dalle. 256 × 64 LED au lieu de 128 × 32, avec les lettres et les pentes lissées. Sur un LCD de 1920 × 460, chaque LED fait 7 pixels.

Le réglage à la main, dans `config.json`, section `preview`

```json
"preview": {
  "enabled": true,
  "x": 1920, "y": 0,
  "width": 1920, "height": 460,
  "borderless": true,
  "topmost": true,
  "mode": "games",
  "takeover": "known",
  "hd": "auto",
  "style": "led"
}
```

- `x` et `y` sont la position du coin haut gauche de l'écran dans le bureau Windows (Paramètres, Affichage). Ici un LCD placé à droite d'un écran 1080p. S'il est placé dessous, ce sera `"x": 0, "y": 1080`.
- `"hd"` vaut `"auto"` (plus fin dès que l'écran est assez grand), `1` (LED de la taille d'une vraie dalle 128 × 32), `2` ou `4` (encore plus fin, pour un très grand écran).
- `"style"` vaut `"led"` (LED rondes, comme une vraie dalle) ou `"pixel"` (pixels carrés, plus net sur un LCD).
- `"mode": "games"` (réglage par défaut) fait comme avec la Pixelcade. Hors jeu, la fenêtre se cache et l'écran reste au frontal, par exemple aux clear logos et marquees de BigBox. Dès qu'un jeu connu démarre, ArcadeDMD passe au premier plan, au-dessus du marquee de BigBox ou d'HyperSpin, sans prendre le focus du jeu. Si le frontal repasse devant pendant la partie, ArcadeDMD revient devant dans la seconde. À la fin de la partie, l'écran est rendu au frontal tout de suite. `"mode": "always"` garde la fenêtre affichée tout le temps, noire hors jeu.
- `"takeover": "known"` passe au premier plan seulement pour les jeux qui ont un fichier dans `games\` (Metal Slug, King of Fighters, tous les Neo Geo...). `"all"` le fait pour tous les jeux MAME, avec la scène générique.
- `"topmost": true` garde la fenêtre au-dessus des autres pendant qu'elle est affichée. Mets `"enabled": false` si tu ne veux que la vraie dalle.

---

### Affichage HD lisse, avec le logo du jeu

Sur un écran LCD, ArcadeDMD peut aussi dessiner la scène directement à la taille de l'écran, sans effet LED. Les textes sont lisses, les barres de vie ont des dégradés, et le logo du jeu est en haut au centre.

Pour l'activer, relance `screen_setup.bat` et choisis 2 à la question sur l'affichage. Ou mets `"style": "hd"` dans la section `preview` de `config.json`. ArcadeDMD voit tout seul que `config.json` a changé et redémarre avec le nouveau réglage. Lance ensuite `demo_fight.bat`, ou un jeu depuis BigBox.

Le logo vient de tes images Clear Logo de LaunchBox. ArcadeDMD trouve le dossier LaunchBox tout seul quand BigBox tourne, ou dans les emplacements habituels (`C:\LaunchBox`, `E:\LaunchBox`...). Sinon, indique-le dans la section `preview`, par exemple `"launchbox": "E:\\LaunchBox"`. Le lien entre le jeu lancé et son logo passe par le chemin de la rom dans LaunchBox, et pour un clone par le jeu parent. Quand un jeu n'a pas de logo, son titre s'affiche à la place en lettres métal.

- Jeux de combat. En haut le score de chaque joueur, ou CHALLENGER et BEAT BY en match VS. Au milieu les barres de vie, avec une traînée claire qui montre le coup qu'on vient de prendre, et le chrono ou KO. En bas P1, P2 ou CPU avec le combattant en cours, l'équipe complète dans les King of Fighters '96 à 2000 (ceux déjà battus sont barrés), et les crédits, en gros, sur une pastille sombre.
- Les autres jeux. Le logo, le score de chaque joueur, puis en bas l'arme, les vies, les bombes, le temps et les crédits quand ils sont connus.
- Personne ne joue. Le logo en grand, et INSERT COIN ou les crédits. Dans les jeux de combat, le logo est entre deux monnayeurs (Écran des pièces, section 7).
- Les décors animés sont un peu assombris, pour que les infos ressortent. `"dim": 30` dans la section `preview` le règle, de 0 (tel que dessiné) à 80 %.

La Pixelcade et les dalles ZeDMD gardent la scène en 128 x 32, c'est la taille de leurs LED.

### Logo du jeu au lancement

Quand un jeu démarre, son logo arrive d'abord. Sur l'écran HD, il entre en grand sur un écran sombre, avec un éclair et un reflet, puis glisse à sa place dans la scène. Sur la Pixelcade et les dalles ZeDMD, il grandit sur les LED 128 x 32, puis la scène arrive. La Pixelcade l'affiche dès que pixelweb lui a laissé la dalle.

![Logo du jeu au lancement, affichage HD](docs/images/hd_logo_intro.jpg)

C'est le Clear Logo LaunchBox du jeu, trouvé comme expliqué juste au-dessus. Sur une dalle, un jeu sans Clear Logo passe directement à sa scène. Sur l'écran HD, son titre en lettres métal le remplace.

```json
"intro": {
  "logo": true,
  "seconds": 2.6,
  "launchbox": ""
}
```

- `"logo": false` le coupe, sur la dalle et sur l'écran HD.
- `"seconds"` est sa durée, de 1 à 10 secondes.
- `"launchbox"` est le dossier LaunchBox, s'il n'est pas trouvé tout seul. Avec une dalle et sans écran HD, c'est ici qu'il faut l'indiquer. Celui de la section `preview` marche aussi.

### Scènes HD animées, Metal Slug et jeux de combat

Avec l'affichage HD lisse, les Metal Slug et les jeux de combat ont une scène complète à eux. Tout est dessiné par le programme, aucune image ne vient des jeux.

![Changement de stage dans un jeu de combat](docs/images/hd_fight_stage.jpg)

- **Metal Slug.** Un panneau de soldat par joueur, avec le score, l'arme et sa jauge de munitions, les bombes, les vies et les prisonniers libérés (premier Metal Slug, X, 3 et 5). Les tirs suivent l'arme (traçantes et douilles, décharges du fusil à pompe, roquettes, lance-flammes), les bombes volent et explosent dans le décor, une caisse tombe quand on ramasse une arme, le casque tombe quand on perd une vie et DERNIÈRE VIE clignote sur la dernière. Dans le char du premier Metal Slug, le char prend la place de l'arme, avec son énergie en coups (trois, comme dans le jeu) et ses obus. Un coup reçu fait clignoter la case perdue, un obus part vers le décor, ÉJECTE-TOI ! clignote quand il n'a plus d'énergie et le char détruit explose. Pour afficher ton propre dessin du char à la place de celui d'ArcadeDMD, dépose-le dans `sprites\mslug_tank_hd.png` (vu de profil, canon vers la droite). Un fond uni autour du dessin devient transparent, les marges vides sont coupées et il se place au milieu de la carte. Le joueur 2 peut arriver à tout moment. Chaque mission a son décor (jungle, désert, montagne enneigée, ville en guerre, port, base ennemie), avec MISSION COMPLETE et un feu d'artifice entre les deux. Quand personne ne joue, les décors passent à tour de rôle.
- **Jeux de combat.** Étincelles à chaque coup, compteur de combo, PREMIER COUP, super coups (l'écran s'assombrit), battement de cœur rouge quand la vie est basse, K.O. qui explose, DOUBLE K.O., TIME UP, PERFECT, confettis pour le vainqueur, combattant suivant des King of Fighters, et FIGHT ! au début de chaque round. Le public en bas réagit à l'action.
- **Jeux Neo Geo faits un par un.** Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers, Neo Turf Masters, Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11, Sengoku 3, Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2, Aero Fighters 3, Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally, Magician Lord, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army, Burning Fight, Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger, Puzzle De Pon!, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks, Super Sidekicks 2, Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf, Power Spikes II, Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa, Puzzled, Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords, Eight Man, Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2 et Shougi no Tatsujin ont chacun une scène à eux, voir la section 7 (Jeux Neo Geo faits un par un).
- **Jeux Capcom.** Les 34 jeux de combat se battent dans les décors du jeu, avec les jauges de super sous les combattants. Cinquante autres jeux Capcom, de Final Fight à 1944, Strider et Ghouls'n Ghosts, ont chacun une scène à eux, voir la section 7 (Les jeux Capcom faits un par un).

#### Des décors qui suivent le stage

Le décor change avec le stage du jeu quand le fichier du jeu sait où le lire.
- `backdrop` est le décor du combat en cours, tiré des bases de triche (« Select Backdrop »). Il choisit le décor HD dans la liste `"hd"` du fichier du jeu.
- `stage` est le numéro du match dans la partie (« Select Current Round »). Il s'affiche en STAGE 2, STAGE 3... avec le nom du lieu.
- Pour les Metal Slug, `mission` choisit le décor de chaque mission.

| Jeux | Valeurs |
|---|---|
| The King of Fighters '96, '97, '98, '99 et 2000, Rage of the Dragons | `stage` et `backdrop` |
| The King of Fighters 2002, Garou, Fatal Fury 2, Fatal Fury Special, Real Bout Fatal Fury 2, Real Bout Fatal Fury Special, Samurai Shodown II, III et IV, World Heroes, World Heroes Perfect, SNK vs. Capcom (JAMMA PCB) | `backdrop` |
| Metal Slug, Metal Slug 2 | `mission` |
| Street Fighter II, II' Champion Edition, II' Hyper Fighting, Super Street Fighter II et Turbo, Street Fighter Alpha, Alpha 2, Alpha 3, Zero 2 Alpha, Street Fighter III et ses 2nd Impact et 3rd Strike, Darkstalkers, Night Warriors, Vampire Savior, Vampire Hunter 2, Vampire Savior 2, X-Men: Children of the Atom, Marvel vs. Capcom, Cyberbots, Super Gem Fighter, Red Earth | `backdrop`, avec le lieu de chaque décor (`"places"`) |

Ces adresses viennent des bases de triche et restent à confirmer en jeu (`test_retroarch.bat` les affiche). Les autres jeux gardent toujours le même décor. `demo_fight.bat` change de stage tous les deux K.O., pour le voir sans jouer.

Chaque fichier de jeu dit quel décor HD va avec chaque décor du jeu, dans l'ordre de leurs numéros. Par exemple, dans `games\kof98.json`

```json
"hd": {"stages": ["fight_city", "fight_jungle", "fight_snow", "fight_desert", "fight_ruins", "arena", "fight_temple", "fight_harbor", "base"]}
```

Le décor 0 (Japon, rue) donne la ville la nuit, le 3 (Moyen-Orient) le désert, le 7 (USA, quai) le port, et ainsi de suite. La note de la valeur `backdrop` liste les décors du jeu. Change la liste à ton goût, le moteur recharge le fichier tout seul.

| Décor | Ce qu'il montre |
|---|---|
| `fight_city` | ville la nuit, néons, métro aérien, vapeur |
| `fight_temple` | temple au crépuscule, lanternes qui se balancent, pétales qui tombent |
| `fight_harbor` | port au soleil couchant, reflets sur l'eau, phare, mouettes |
| `fight_ruins` | ruines la nuit, torches, braises, lucioles |
| `fight_desert`, `fight_jungle`, `fight_snow` | désert au crépuscule, jungle de nuit, montagne enneigée |
| `arena` | arène avec projecteurs |
| `base`, `city_war` | base ennemie (gyrophares, projecteurs), ville en guerre (incendies, explosions) |
| `fight_castle` | toit de château au Japon la nuit, pleine lune, pétales de cerisier |
| `fight_market` | marché chinois, lanternes suspendues, vapeur des étals |
| `fight_factory` | aciérie, hauts fourneaux, coulée de métal et étincelles |
| `fight_gothic` | manoir gothique sous la lune, chauves-souris, éclairs |
| `fight_palace` | palais indien au couchant, éléphants, torches |
| `fight_thai` | temple d'or au bord du fleuve, lanternes qui s'envolent, reflets sur l'eau |
| `fight_lab` | laboratoire, cuves lumineuses, écrans |
| `fight_airbase` (ou `fight_base`) | base aérienne au crépuscule, hangars, avions, balises de piste |

Un fichier de jeu Capcom peut aussi donner le lieu affiché sous le bandeau du décor, en français et en anglais, un par valeur de `backdrop` (`"places": [["CHINE", "CHINA"], ...]`). Sans lui, c'est le lieu du décor HD qui s'affiche.

Les décors `fight_` et `arena` ont du public devant. Sans le préfixe `fight_` (`city`, `temple`, `harbor`, `ruins`, `desert`, `jungle`, `snow`), les mêmes lieux n'ont pas de public, comme dans les missions des Metal Slug. Un fichier Metal Slug peut aussi avoir sa propre liste `"hd": {"stages": [...]}`, un décor par mission.

## 4. Pixelcade LED

La Pixelcade LED est elle-même une dalle 128x32. ArcadeDMD la pilote directement par son port USB, avec le même protocole que Visual Pinball (dmdext, libdmdutil). Les cartes V1 et V2 sont reconnues toutes seules.

Le logiciel Pixelcade (pixelweb) ne peut pas partager la dalle. ArcadeDMD fait donc ce que Pixelcade recommande pour Visual Pinball. Au lancement d'un jeu qui a son fichier dans `games\`, il arrête pixelweb par son API (`/quit`) et prend la dalle. Quand tu quittes le jeu, il la rend tout de suite et relance pixelweb. Le marquee du jeu reste affiché pendant ce temps, puis ArcadeDMD demande à pixelweb de l'afficher, comme le ferait BigBox (le jeu que tu viens de quitter est celui sélectionné dans BigBox). Ensuite BigBox reprend la main sur la Pixelcade à chaque changement de jeu, comme sur un écran LCD de marquee. Pour tous les autres jeux, pixelweb continue d'afficher ses marquees comme avant.

### Réglage

`install.bat` pose la question à l'étape 4 et règle le port tout seul. La sortie ZeDMD reste coupée si tu as répondu non à sa question, ArcadeDMD ne sonde alors aucun autre port série (pistolets par exemple). Pour le faire à la main :

1. Lance `ports.bat` et repère le port de la Pixelcade (dans le doute, débranche-la et regarde quel port disparaît).
2. Dans `config.json`, section `pixelcade`, mets `"enabled": true` et ce port.

```json
"pixelcade": {
  "enabled": true,
  "device": "COM4",
  "color_order": "auto",
  "mode": "games",
  "takeover": "known",
  "max_fps": 30
}
```

3. Lance `test_pixelcade.bat`. La mire affiche ROUGE, VERT et BLEU. À la fin elle reste affichée et le test te demande si chaque mot est de sa couleur. Si tu réponds n, il inverse le vert et le bleu dans `config.json` (`"color_order"`). Relance le test pour vérifier.
4. Lance `demo_afterburner.bat`, la scène passe sur la Pixelcade, puis pixelweb revient à la fermeture.

### Options

| Réglage | Effet |
|---|---|
| `"takeover": "known"` | prend la dalle seulement pour les jeux qui ont un fichier dans `games\` (After Burner II, Sonic 1 et 2, et ceux que tu ajoutes) |
| `"takeover": "all"` | prend la dalle pour tous les jeux MAME, avec la scène générique |
| `"mode": "always"` | garde la dalle en permanence (si tu n'utilises plus pixelweb), noire hors jeu |
| `"pixelweb_exe"` | chemin de pixelweb.exe, trouvé tout seul d'habitude. S'il a besoin d'options, mets ici un .bat qui le lance avec |
| `"art_dir"` | dossier Pixelcade, pour reprendre ses marquees en fond de la scène générique (trouvé tout seul d'habitude) |
| `"gamma": 2.2` | les LED éclairent en proportion de la valeur reçue, donc un gris sombre prévu pour un écran brille sur la dalle et les scènes paraissent plus chargées que dans l'aperçu. ArcadeDMD corrige les couleurs pour que la dalle ressemble à l'aperçu. `1.0` les envoie telles quelles |

Les cartes V1 affichent 3 bits par couleur en mode direct, c'est une limite du matériel. Les cartes V2 affichent toutes les couleurs.

Pour un jeu avec fichier mais sans scène dédiée (un jeu appris avec `learn.bat` par exemple), la scène générique reprend le marquee Pixelcade du jeu en fond, atténué, avec le score et les crédits par-dessus.

---

## 5. After Burner II, trouver le score et les crédits

Le record est connu publiquement (table des records à `0xFF846E`, la même que `hiscore.dat`). L'adresse du score et celle des crédits ne sont documentées nulle part, d'où l'outil d'apprentissage. Compte cinq minutes.

1. Lance After Burner II.
2. Mets une pièce, attends un peu, mets-en une deuxième. Les crédits changent.
3. Joue. Quand le score est stable (pas pendant un décompte de bonus), appuie sur **Ctrl droit + D**. Un message « capture enregistrée » s'affiche. Tu peux aussi passer par Tab, Options des plugins, ArcadeDMD, « Capturer la RAM ».
4. Refais une capture à trois ou quatre moments avec des scores et des crédits différents.
5. Quitte MAME et lance `learn.bat`. Pour chaque capture, l'outil ouvre la photo d'écran et te demande les valeurs, par exemple `score=16060 credits=3`.
6. Il cherche ces valeurs dans tous les formats courants, propose l'adresse et l'écrit dans `games\aburner2.json`.

Relance le jeu, le score et les crédits s'affichent sur la dalle et dans le menu Tab du plugin.

Avec une seule zone trouvée, c'est la bonne. Avec plusieurs, une capture de plus suffit à trancher. Si rien n'est trouvé, supprime la ligne `learn_ranges` dans `games\aburner2.json`, efface le dossier `runtime\learn\aburner2` et refais les captures. L'outil fouille alors toute la RAM visible du processeur principal.

Autre voie si tu utilises déjà DOFLinx avec DOF2DMD (voir la section 9). DOFLinx sait déjà lire le score et les crédits d'After Burner II et de plus de 2 000 jeux.

---

## 6. Sonic 1 et Sonic 2

Les adresses viennent des désassemblages communautaires de Sonic 1 et de Sonic 2 (score, anneaux, vies, zone). Elles sont les mêmes dans les deux jeux. La scène se déclenche dans MAME avec la Mega Drive (pilotes `genesis` ou `megadriv`, cartouche « Sonic The Hedgehog » ou « Sonic The Hedgehog 2 » par la liste logicielle ou un fichier ROM portant ce nom) et normalement avec les versions arcade Mega Play et Mega-Tech (`mp_sonic`, `mt_sonic`, `mp_soni2`, `mt_soni2`). Avec RetroArch et le cœur Genesis Plus GX, elle marche aussi (voir la section 7).

Le fichier `games\sonic.json` sert pour Sonic 1 et `games\sonic2.json` pour Sonic 2. Les deux scènes sont pareilles, seul le titre change.

Le petit personnage qui court sur l'herbe est un anneau générique. Pour mettre ton propre sprite animé, dépose `sonic.gif` (ou un `sonic.png` en bande horizontale de 6 images) dans `sprites\`. Pour Sonic 2, un `sonic2.gif` passe en priorité s'il existe. Ajuste `"y"` dans le fichier du jeu selon sa hauteur.

---

## 7. RetroArch (Metal Slug, Sonic...)

ArcadeDMD lit aussi les jeux lancés dans RetroArch, sans plugin. RetroArch donne la mémoire du jeu par ses « commandes réseau », qui restent sur le PC lui-même. C'est la méthode du zip de Vera.

### À régler une fois dans RetroArch

1. Il faut RetroArch 1.19 ou plus récent. La version s'affiche dans Informations, puis Informations système.
2. Dans Réglages, puis Réseau, active « Commandes réseau ». Laisse le port 55355.
3. Laisse activé « Mettre en pause quand la fenêtre n'est plus active » (Réglages, Interface utilisateur). C'est le réglage par défaut, il sert pour l'apprentissage.
4. Lance le jeu avec un cœur qui donne sa mémoire (voir juste en dessous).

Rien d'autre à installer. Dès que le moteur tourne (`run.bat` ou le lancement automatique), il surveille RetroArch tout seul. Le journal indique « RetroArch détecté » quand les commandes réseau répondent, puis le cœur chargé à chaque jeu.

### Le bon cœur

Tous les cœurs ne donnent pas la mémoire du jeu à RetroArch. Avec un mauvais cœur, la scène s'affiche mais sans aucune valeur.

| Système | Cœur qui marche | Cœurs qui ne marchent pas |
|---|---|---|
| Arcade, Neo Geo (Metal Slug...) | Arcade (FinalBurn Neo), à jour | FB Alpha 2012 sous toutes ses formes (Neo Geo, CPS-1...), MAME 2003, MAME 2003-Plus, MAME 2010, MAME |
| Mega Drive (Sonic) | Genesis Plus GX, ou PicoDrive | |

Installer FinalBurn Neo
1. Dans RetroArch, va dans Menu principal, Mise à jour en ligne, Télécharger un cœur, puis choisis « Arcade (FinalBurn Neo) ». Si Mise à jour en ligne n'apparaît pas, active-la dans Réglages, Interface utilisateur, Visibilité des éléments du menu, Menu principal.
2. Pour essayer, va dans Menu principal, Charger un cœur, Arcade (FinalBurn Neo), puis Charger un contenu et choisis le jeu (par exemple `mslug.zip`).
3. Si le jeu refuse de démarrer, il manque sûrement un fichier du BIOS. Mets un `neogeo.zip` récent à côté du jeu.
4. Si tu lances tes jeux depuis HyperSpin ou RocketLauncher, change aussi le cœur choisi pour ce système dans ton lanceur.

Pour savoir quel cœur tourne, appuie sur F1 pendant le jeu, puis Informations, Informations sur le cœur. Ou lance `test_retroarch.bat` pendant une partie. Il affiche la version de RetroArch, le cœur chargé, ce que donne la lecture de la mémoire et les valeurs lues, puis dit quoi faire si quelque chose cloche. Le résultat va aussi dans `runtime\test_retroarch.txt`.

### Jeux prévus

| Jeu | Cœur RetroArch | Affiché tout de suite | À apprendre |
|---|---|---|---|
| Metal Slug (`mslug`) | FinalBurn Neo | score, vies, bombes, arme et munitions, le char (dedans ou pas, son énergie et ses obus) | rien |
| Metal Slug 2 (`mslug2`), Metal Slug X (`mslugx`) | FinalBurn Neo | vies, bombes, arme et munitions | score |
| Metal Slug 3 (`mslug3`) | FinalBurn Neo | score, vies, bombes, arme et munitions | score J2 |
| Metal Slug 4 (`mslug4`), Metal Slug 5 (`mslug5`) | FinalBurn Neo | vies, bombes, arme et munitions | score |
| Les 57 jeux de combat Neo Geo (King of Fighters, Samurai Shodown, Fatal Fury, Last Blade, World Heroes...) | FinalBurn Neo | voir le tableau Jeux de combat juste en dessous | le score, sauf KOF 96 à 2002 et Samurai Shodown II |
| Blazing Star (`blazstar`), Puzzle Bobble (`pbobblen`), Shock Troopers (`shocktro`), Pulstar (`pulstar`), Magical Drop III (`magdrop3`), Sengoku 3 (`sengoku3`), Top Hunter (`tophuntr`), Last Resort (`lresort`), Aero Fighters 2 (`sonicwi2`), Aero Fighters 3 (`sonicwi3`), Strikers 1945 Plus (`s1945p`), Super Dodge Ball (`sdodgeb`), Neo Bomberman (`neobombe`), Twinkle Star Sprites (`twinspri`), League Bowling (`lbowling`), Magician Lord (`maglord`), NAM-1975 (`nam1975`), Cyber-Lip (`cyberlip`), Ghost Pilots (`gpilots`), Alpha Mission II (`alpham2`), Viewpoint (`viewpoin`), Zed Blade (`zedblade`), Prehistoric Isle 2 (`preisle2`), Shock Troopers 2nd Squad (`shocktr2`), Robo Army (`roboarmy`), Burning Fight (`burningf`), Mutation Nation (`mutnat`), Sengoku (`sengoku`), Sengoku 2 (`sengoku2`), Ninja Combat (`ncombat`), Ninja Commando (`ncommand`), Blue's Journey (`bjourney`), Puzzle Bobble 2 (`pbobbl2n`), Magical Drop II (`magdrop2`), Money Puzzle Exchanger (`miexchng`), Puzzle De Pon! (`puzzledp`), Puzzle De Pon! R! (`puzzldpr`), Panic Bomber (`panicbom`), Pop 'n Bounce (`popbounc`), Super Bubble Pop (`sbp`), Spin Master (`spinmast`), Ganryu (`ganryu`), Zupapa! (`zupapa`), Neo Mr. Do! (`neomrdo`), Bang Bead (`bangbead`), Battle Flip Shot (`flipshot`), Gururin (`gururin`), Ghostlop (`ghostlop`), Pochi and Nyaa (`pnyaa`), Puzzled (`joyjoy`), Zintrick (`zintrckb`), Digger Man (`diggerma`), Andro Dunos (`androdun`), Captain Tomaday (`ctomaday`), Choutetsu Brikin'ger (`ironclad`), Last Hope (`lasthope`), Bang Bang Busters (`b2b`), Crossed Swords (`crsword`), Eight Man (`eightman`), Nightmare in the Dark (`nitd`), The Super Spy (`superspy`), Quiz King of Fighters (`quizkof`), Quiz Daisousa Sen (`quizdais`), Quiz Meitantei Neo & Geo (`quizdai2`), Chibi Maruko-chan Deluxe Quiz (`marukodq`) | FinalBurn Neo | voir Jeux Neo Geo faits un par un | score |
| Windjammers (`wjammers`), Neo Turf Masters (`turfmast`), Super Sidekicks 3 (`ssideki3`), The Ultimate 11 (`ssideki4`), Baseball Stars 2 (`bstars2`), Street Hoop (`strhoop`), Neo Drift Out (`neodrift`), Riding Hero (`ridhero`), Thrash Rally (`trally`), Super Sidekicks (`ssideki`), Super Sidekicks 2 (`ssideki2`), Tecmo World Soccer '96 (`twsoc96`), Goal! Goal! Goal! (`goalx3`), Neo-Geo Cup '98 (`neocup98`), Soccer Brawl (`socbrawl`), Football Frenzy (`fbfrenzy`), Pleasure Goal (`pgoal`), Baseball Stars Professional (`bstars`), 2020 Super Baseball (`2020bb`), Top Player's Golf (`tpgolf`), Power Spikes II (`pspikes2`), Over Top (`overtop`), Stakes Winner (`stakwin`), Stakes Winner 2 (`stakwin2`), Jockey Grand Prix (`jockeygp`), The Irritating Maze (`irrmaze`), Minasan no Okagesamadesu! (`minasan`), Mahjong Kyo Retsuden (`mahretsu`), Janshin Densetsu (`janshin`), Bakatonosama Mahjong Manyuuki (`bakatono`), Idol Mahjong Final Romance 2 (`froman2b`), Shougi no Tatsujin (`moshougi`) | FinalBurn Neo | voir Jeux Neo Geo faits un par un | rien |
| Tous les autres jeux Neo Geo | FinalBurn Neo | scène selon le genre (crédits avec MAME) | score, crédits si le jeu en garde une copie |
| Tous les jeux Capcom CPS1, CPS2 et CPS3 | FinalBurn Neo | voir Les jeux Capcom CPS1, CPS2 et CPS3 | score |
| Sonic 1 et Sonic 2 | Genesis Plus GX | score, anneaux, vies | rien |

Les adresses des vies, bombes et munitions viennent de la base de codes de triche de MAME 2003-Plus. Celles de Sonic sont les mêmes que dans MAME. Les vies des Metal Slug suivent le « 1UP » de l'écran. Metal Slug 1 compte aussi la vie en cours, ArcadeDMD enlève donc 1 (vérifié). Metal Slug 3 ne la compte pas (vérifié). Pour 2 et X, ArcadeDMD fait comme pour le 1, et pour 4 et 5 comme pour le 3. Si un de ces jeux affiche une vie de moins que l'écran, enlève les lignes `"add"` et `"min"` de ses vies dans son fichier `games\mslugX.json`. S'il en affiche une de plus, ajoute `"add": -1, "min": 0`.

À deux joueurs, la scène change toute seule dès que le joueur 2 appuie sur Start. Le BIOS de la Neo Geo indique qui est en jeu. En haut, comme dans le jeu, « 1UP= » et les vies du joueur 1 à gauche, « 2UP= » et celles du joueur 2 à droite, avec le titre qui défile entre les deux. Dessous, chaque score sous son 1UP ou son 2UP. « SCORE ? » en gris veut dire que ce score n'est pas encore appris. En bas, les bombes puis l'arme de chaque joueur passent à tour de rôle, avec « P1 » en vert et « P2 » en jaune. Si seul le joueur 2 joue, la scène normale s'affiche avec ses valeurs à lui. Les crédits des Neo Geo ne se lisent qu'avec MAME (voir Tous les jeux Neo Geo).

Les scènes des Metal Slug s'inspirent de la vidéo de Vera, adaptées à une dalle 128x32 pour que rien ne passe sous le décor. En haut, « SNK » en bleu puis « - METAL SLUG » (avec le numéro du jeu) en blanc défilent lentement. Dessous, « P1 » en vert et le score en blanc à gauche, les vies à droite. La ligne suivante alterne les bombes, l'arme avec ses munitions (pistolet, mitraillette, fusil à pompe, lance-flammes, lance-roquettes, laser, tête chercheuse... un « + » indique la version améliorée) et les crédits avec MAME. Tout en bas, des petites collines et un petit char moins lumineux qui avance et tire quand le score monte.

Les scores de Metal Slug et de Metal Slug 3 sont déjà dans leurs fichiers, trouvés avec `learn.bat` sous RetroArch et FinalBurn Neo. Pour remplacer le char par ton propre dessin, dépose `mslug_tank.gif` (ou `mslug_tank.png` en bande de 3 images) dans `sprites\`. Il doit tenir sur 5 pixels de haut, canon vers la droite.

### Jeux de combat

Chaque jeu de combat Neo Geo a son propre fichier dans `games\`, versions officielles comprises (japonaise, coréenne, prototype). Les adresses viennent des codes de triche de FinalBurn Neo, des scripts d'entraînement FinalBurn Neo de peon2 et de la base de triche de MAME 2003-Plus. Le score est connu pour les King of Fighters et pour Samurai Shodown II. Pour les autres, apprends-le avec `learn.bat` (`score=...` et `score2=...`).

Quand une barre de vie, un chrono ou un nom ne colle pas à l'écran, lance `test_retroarch.bat` pendant un combat et poste le résultat dans une issue GitHub.

| Jeu | Fichier | Barres de vie | Chrono | Nom des personnages | Score |
|---|---|---|---|---|---|
| 3 Count Bout | `3countb.json` | - | - | - | à apprendre |
| Aggressors of Dark Kombat | `aodk.json` | oui | - | - | à apprendre |
| Art of Fighting | `aof.json` | oui | oui | oui (10) | à apprendre |
| Art of Fighting 2 | `aof2.json` | oui | oui | oui (13) | à apprendre |
| Art of Fighting 3 | `aof3.json` | oui | oui | oui (10) | à apprendre |
| Breakers | `breakers.json` | oui | oui | - | à apprendre |
| Breakers Revenge | `breakrev.json` | oui | oui | - | à apprendre |
| Double Dragon | `doubledr.json` | oui | oui | oui (14) | à apprendre |
| Dragon's Heaven | `dragonsh.json` | - | - | - | à apprendre |
| Fatal Fury | `fatfury1.json` | oui | oui | oui (14) | à apprendre |
| Fatal Fury 2 | `fatfury2.json` | oui | oui | - | à apprendre |
| Fatal Fury 3 | `fatfury3.json` | oui | oui | oui (13) | à apprendre |
| Fatal Fury Special | `fatfursp.json` | oui | oui | - | à apprendre |
| Fight Fever | `fightfev.json` | oui | oui | oui (10) | à apprendre |
| Galaxy Fight | `galaxyfg.json` | oui | - | - | à apprendre |
| Garou | `garou.json` | oui | oui | oui (14) | à apprendre |
| Kabuki Klash | `kabukikl.json` | oui | oui | - | à apprendre |
| Karnov's Revenge | `karnovr.json` | oui | - | oui (14) | à apprendre |
| King of the Monsters | `kotm.json` | oui | - | - | à apprendre |
| King of the Monsters 2 | `kotm2.json` | oui | oui | oui (10) | à apprendre |
| Kizuna Encounter | `kizuna.json` | oui | oui | - | à apprendre |
| Legend of Success Joe | `legendos.json` | oui | - | - | à apprendre |
| Matrimelee | `matrim.json` | oui | oui | - | à apprendre |
| Ninja Master's | `ninjamas.json` | oui | oui | - | à apprendre |
| Rage of the Dragons | `rotd.json` | oui | oui | - | à apprendre |
| Ragnagard | `ragnagrd.json` | oui | - | - | à apprendre |
| Real Bout Fatal Fury | `rbff1.json` | oui | oui | oui (16) | à apprendre |
| Real Bout Fatal Fury 2 | `rbff2.json` | oui | oui | oui (23) | à apprendre |
| Real Bout Fatal Fury Special | `rbffspec.json` | oui | oui | oui (20) | à apprendre |
| Samurai Shodown | `samsho.json` | oui | oui | oui (13) | à apprendre |
| Samurai Shodown II | `samsho2.json` | oui | oui | oui (17) | oui |
| Samurai Shodown III | `samsho3.json` | oui | oui | oui (14) | à apprendre |
| Samurai Shodown IV | `samsho4.json` | oui | oui | oui (18) | à apprendre |
| Samurai Shodown V | `samsho5.json` | oui | oui | oui (28) | à apprendre |
| Samurai Shodown V Special | `samsh5sp.json` | oui | oui | oui (28) | à apprendre |
| Savage Reign | `savagere.json` | - | - | - | à apprendre |
| SNK vs. Capcom | `svc.json` | oui | oui | oui (36) | à apprendre |
| SNK vs. Capcom (JAMMA PCB) | `svcpcb.json` | oui | oui | oui (36) | à apprendre |
| The King of Fighters '94 | `kof94.json` | oui | oui | - | à apprendre |
| The King of Fighters '95 | `kof95.json` | oui | oui | - | à apprendre |
| The King of Fighters '96 | `kof96.json` | oui | oui | oui (29) | supposé, à vérifier |
| The King of Fighters '97 | `kof97.json` | oui | oui | oui (32) | supposé, à vérifier |
| The King of Fighters '98 | `kof98.json` | oui | oui | oui (38) | trouvé |
| The King of Fighters '99 | `kof99.json` | oui | oui | oui (34) | supposé, à vérifier |
| The King of Fighters 2000 | `kof2000.json` | oui | oui | oui (36) | supposé, à vérifier |
| The King of Fighters 2001 | `kof2001.json` | oui | oui | - | supposé, à vérifier |
| The King of Fighters 2002 | `kof2002.json` | oui | oui | - | supposé, à vérifier |
| The King of Fighters 2003 | `kof2003.json` | - | oui | - | à apprendre |
| The King of Fighters 2003 (Japan, JAMMA PCB) | `kf2k3pcb.json` | - | oui | - | à apprendre |
| The Last Blade | `lastblad.json` | oui | oui | oui (15) | à apprendre |
| The Last Blade 2 | `lastbld2.json` | oui | oui | oui (20) | à apprendre |
| Voltage Fighter Gowcaizer | `gowcaizr.json` | oui | oui | oui (12) | à apprendre |
| Waku Waku 7 | `wakuwak7.json` | oui | oui | oui (9) | à apprendre |
| World Heroes | `wh1.json` | oui | oui | oui (9) | à apprendre |
| World Heroes 2 | `wh2.json` | oui | oui | oui (16) | à apprendre |
| World Heroes 2 Jet | `wh2j.json` | oui | oui | oui (17) | à apprendre |
| World Heroes Perfect | `whp.json` | oui | oui | oui (19) | à apprendre |

### Match VS des King of Fighters (BEAT BY)

En match à deux, les King of Fighters affichent « CHALLENGER » au-dessus du joueur qui vient d'arriver, et « BEAT BY 02 » au-dessus de celui qui a déjà battu 2 challengers d'affilée. La dalle affiche la même chose à la place des scores, dès que ces compteurs sont appris. Chaque victoire est aussi notée dans `obs\vs_history.txt`, et la meilleure série de chaque jeu est gardée (section 11).

Ces compteurs ne sont dans aucune base de codes de triche. Il faut les apprendre une fois par jeu, par exemple KOF 2002 puis KOF 98.
1. Lance le jeu dans RetroArch et commence une partie avec le joueur 1.
2. Fais entrer le joueur 2 avec une pièce et Start. Le match VS commence. Tu peux tenir les deux sticks toi-même.
3. Lance `learn.bat`.
4. Après chaque match, quand « BEAT BY » s'affiche en haut de l'écran, tape les deux compteurs, par exemple `beat=1 beat2=0`. Mets 0 du côté marqué CHALLENGER.
5. Fais au moins cinq ou six matchs. Fais gagner tantôt un côté, tantôt l'autre, pour que les compteurs changent.
6. Entrée vide pour finir. L'outil écrit `beat` et `beat_p2` dans le fichier du jeu.

Si l'outil ne trouve rien, zippe le dossier `runtime\learn\` du jeu (`kof2002` par exemple) et joins-le à une issue GitHub, comme pour Samurai Shodown II.

### Jeux Neo Geo faits un par un

Jeu après jeu, les jeux Neo Geo ont reçu une scène de dalle et une scène HD animée à leur image, les plus connus d'abord, et maintenant ils en ont tous une. [PROGRESS.md](PROGRESS.md) montre où on en est et ce qui vient ensuite. Tout est dessiné par le programme, aucune image ne vient des jeux.

Dans les shoot'em up (Blazing Star, Pulstar, Last Resort, Aero Fighters 2 et 3, Strikers 1945 Plus, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope), dès que le score est lu, les ennemis de l'écran HD n'explosent que quand le jeu marque des points. L'ennemi que nos tirs touchent part d'abord, ses points s'affichent au-dessus, et plus le gain est gros plus l'explosion est forte. Une bombe ou une arme spéciale du jeu détruit ce qu'elle touche, et un bonus compté par le jeu en fin de niveau s'affiche en un seul compteur. Tant que le score d'un jeu n'a pas été appris avec `learn.bat`, sa scène HD joue toute seule.

La dalle de ces jeux reste simple pendant la partie. Le score en gros au milieu, ou le titre du jeu tant que le score n'est pas appris. Tes vies en bas à gauche (un avion et x2), tes bombes en bas à droite. Ni crédits ni INSERT COIN pendant la partie. Entre les deux vole ton vaisseau. Il suit ton stick et tire tant que tu tiens le bouton de tir (le BIOS de la Neo Geo les garde, avec MAME comme avec RetroArch), et vole tout seul tant que tu n'y as pas touché. À deux, les deux scores en haut, les vies et les bombes de chaque joueur en dessous, et les deux vaisseaux face à face. Tout le reste prend la dalle un instant, une chose à la fois, comme sur un flipper. BOMBE! et ses explosions, POWER UP puis MAX POWER, l'avion qui explose avec les vies qui restent, LAST LIFE, 1UP, ROUND 2 ou STAGE 2, SPEED UP, le SUPER SHOT de Strikers 1945 Plus, CONTINUE?, GAME OVER, PLAYER 1 et PLAYER 2 quand quelqu'un commence, et CRÉDIT 1 quand une pièce entre en pleine partie. Chaque ennemi détruit dans le jeu explose devant ton vaisseau, de la taille et au rythme des explosions de DOFLinx, une grosse pour un gros ennemi, et rien n'explose pendant un décompte de bonus. Tant que le score n'est pas appris, un ennemi explose devant lui de temps en temps pendant qu'il tire, comme sur l'écran HD. L'écran des pièces, quand personne ne joue, ne change pas.

![Aero Fighters 2 sur une dalle LED 128x32, l'avion qui vole et tire, POWER UP, une pièce en pleine partie et BOMBE!](docs/images/led_shooter.gif)

Tes propres animations (les GIF de DOFLinx ou de la Pixelcade par exemple) peuvent remplacer les nôtres sur la dalle. Mets-les dans un dossier `artwork` à côté d'`arcadedmd.py`, il n'est jamais publié et une mise à jour n'y touche pas. `artwork\boom.gif` est l'explosion d'un ennemi, `boom_big.gif` la grosse, `bomb.gif` et `shock.gif` la bombe, `super.gif` le super tir de Strikers 1945 Plus, `charge.gif` le tir chargé de Pulstar et `ship.gif` ton vaisseau (tourné vers la droite, environ 14 x 5). Pour un seul jeu, mets-les dans `artwork\<jeu>\` (`artwork\s1945p\boom.gif` par exemple). Un GIF de 128 x 32 se joue sur toute la dalle et son noir laisse voir la scène, mais quand son dessin tient au milieu (les explosions de DOFLinx), il est recadré et part à l'endroit de l'action.

![Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers et Neo Turf Masters sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games.jpg)

![Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11 et Sengoku 3 sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_2.jpg)

![Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2 et Aero Fighters 3 sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_3.jpg)

![Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman et Twinkle Star Sprites sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_4.jpg)

![League Bowling, Neo Drift Out, Riding Hero, Thrash Rally et Magician Lord sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_5.jpg)

![NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II et Viewpoint sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_6.jpg)

![Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army et Burning Fight sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_7.jpg)

![Mutation Nation, Sengoku, Sengoku 2, Ninja Combat et Ninja Commando sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_8.jpg)

![Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger et Puzzle De Pon! sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_9.jpg)

![Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop et Spin Master sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_10.jpg)

![Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks et Super Sidekicks 2 sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_11.jpg)

![Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl et Football Frenzy sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_12.jpg)

![Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf et Power Spikes II sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_13.jpg)

![Bang Bead, Battle Flip Shot, Over Top, Stakes Winner et Stakes Winner 2 sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_14.jpg)

![Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa et Puzzled sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_15.jpg)

![Zintrick, Digger Man, The Irritating Maze, Andro Dunos et Captain Tomaday sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_16.jpg)

![Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords et Eight Man sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_17.jpg)

![Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo et Chibi Maruko-chan Deluxe Quiz sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_18.jpg)

![Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2 et Shougi no Tatsujin sur un marquee LCD, affichage HD](docs/images/hd_neogeo_games_19.jpg)

| Jeu | Fichier | Dalle | Écran HD |
|---|---|---|---|
| Blazing Star | `blazstar.json` | le score ou le titre, les vies, le vaisseau qui suit le stick et tire, POWER UP, ROUND 2, une vie perdue | l'espace et une grosse planète. Le vaisseau tire, un ennemi explose quand le score monte, POWER UP, ROUND avec une pointe de vitesse, le vaisseau explose quand une vie est perdue |
| Puzzle Bobble | `pbobblen.json` | la bulle dans le lanceur et la suivante, à leurs couleurs, ROUND | le lanceur avec sa flèche et son engrenage. Chaque bulle tirée dans le jeu part du lanceur et colle à un petit plateau, trois de la même couleur éclatent et celles qui ne tiennent plus tombent |
| Windjammers | `wjammers.json` | les points du set avec le chrono entre les deux, le terrain, le pays de l'adversaire, un palet qui fait des allers-retours | le terrain du jeu (plage, gazon, carrelage, béton, terre battue, stade) et le tableau des scores. Le palet file dans la zone de but avec +3 ou +5, ou tombe de l'autre côté avec +2 |
| Shock Troopers | `shocktro.json` | l'énergie, l'arme et ses munitions, l'arme spéciale et ce qu'il en reste, le chrono | une jungle en guerre, un panneau par joueur avec l'énergie, l'arme, les munitions et les grenades. Les tirs, les grenades qui explosent dans la jungle, le panneau qui tremble quand on est touché |
| Neo Turf Masters | `turfmast.json` | le club et sa distance, le coup, la jauge de puissance, le golfeur, le vent avec une flèche | un parcours de golf, le club, la jauge de puissance et la boussole du vent. Le vent pousse les nuages et le drapeau, et la balle part vers le green à chaque coup |
| Pulstar | `pulstar.json` | le score ou le titre, les vies, le vaisseau qui suit le stick et tire, le tir chargé, SPEED UP, STAGE 2 | un monde par stage (la Terre, la veine d'eau, le feu, la station spatiale, la forêt, la nébuleuse). La charge brille au nez du vaisseau et part en rayon, les modules et le bouclier avant suivent le vaisseau, un ennemi explose quand le score monte, STAGE avec son nom |
| Magical Drop III | `magdrop3.json` | les cartes de tarot des deux joueurs, le quota, le niveau | deux champs de gouttes sous un ciel de tarot, les deux cartes au milieu. Quand le quota baisse, le fou lance une goutte et autant de gouttes éclatent, un gros groupe fait une chaîne, le niveau fait descendre une rangée, la carte se retourne quand le personnage change |
| Super Sidekicks 3 | `ssideki3.json` | les buts des deux équipes, BUT ! quand il y en a un, un ballon qui fait des allers-retours | un stade de jour, le match vu par la caméra de télé. Quand les buts montent, le ballon finit au fond du filet, BUT !, confettis, le public saute |
| The Ultimate 11 | `ssideki4.json` | les buts et les jauges de puissance des deux joueurs | le même match de nuit sous les projecteurs, avec la jauge de puissance. Quand la jauge pleine se vide, le super tir part en feu |
| Sengoku 3 | `sengoku3.json` | la vie et la magie des deux joueurs, le chrono, le combattant, l'arme de jet et ce qu'il en reste | un temple sous la lune et des guerriers de l'ombre, un panneau par combattant. Les armes de jet partent (shuriken, kunai, bombe, disque), un guerrier tombe sous le sabre quand le score monte, la magie balaie l'écran, le panneau tremble quand on est touché |
| Top Hunter | `tophuntr.json` | les vies en petits chasseurs, le chrono, la jauge de puissance en cinq segments, des collines | des chasseurs aussi grands que dans le jeu sur quatre planètes (forêt, glace, vent, feu) avec leurs deux voies, du feuillage, de la glace ou de la roche en haut de l'écran comme dans le jeu. Des robots et des machines à turbines arrivent sur les deux voies, le chasseur saute d'une voie à l'autre et les frappe, les jette ou leur tire dessus quand le score monte, la jauge de puissance pleine qui se vide donne un coup spécial, les chasseurs passent à la planète suivante quand le chrono repart pour un nouveau stage. En haut, la tête du chasseur avec 1UP= et les vies, le score, la puissance, TIME |
| Baseball Stars 2 | `bstars2.json` | les points des deux équipes, RUN! quand il y en a un, les lampes des balles, des prises et des retraits, les deux jauges POW | le terrain comme dans la vue de frappe du jeu, une herbe vert vif vue de derrière le marbre, le frappeur en grand devant, le lanceur sur le monticule. Chaque balle, prise et retrait lu dans le jeu est un lancer, annoncé en grosses lettres arc-en-ciel, le frappeur frappe et un joueur attrape la balle, les points envoient la balle loin et les coureurs au marbre (feu d'artifice quand elle passe le mur), l'autre équipe passe à la batte après le troisième retrait. Le compte en pastilles de couleur |
| Last Resort | `lresort.json` | le score ou le titre, les vies, le vaisseau qui suit le stick et tire, POWER UP, SPEED UP | la ville la nuit du premier stage du jeu, des tours géantes aux fenêtres orange, des immeubles violets, l'autoroute avec ses réverbères et ses voitures. L'unité tourne autour du vaisseau, du côté opposé à sa route, et tire avec lui, de temps en temps elle part droit devant puis revient, un ennemi explose quand le score monte. 1P= et les vies en haut, POW en bas |
| Aero Fighters 2 | `sonicwi2.json` | le score ou le titre, les vies et les bombes, l'avion qui suit le stick et tire, BOMBE!, POWER UP, MAX POWER | une ville vue du ciel en plein jour, ses avenues et leurs voitures, des parkings et des parcs. Des avions de chasse dessinés d'après de vrais avions volent avec leur ombre dessous, les avions ennemis, les hélicoptères et les chars explosent quand le score monte, une bombe envoie une salve de missiles qui nettoie l'écran. Les bombes dans leur cadre comme dans le jeu |
| Aero Fighters 3 | `sonicwi3.json` | la même chose, avec le nom du pilote du joueur 1 | une ville au bord d'un fleuve à la tombée de la nuit vue du ciel, avec l'avion du pilote choisi par le joueur 1 (douze avions, le biplan Swordfish, le Seiran et ses flotteurs...), de gros bombardiers et des chars sur les avenues. La grosse bombe tombe et tout saute |
| Strikers 1945 Plus | `s1945p.json` | le score ou le titre, les vies et les bombes, l'avion qui suit le stick et tire, BOMBE!, SUPER SHOT, POWER UP | les deux panneaux de côté du jeu (SCORE, les avions qui restent, BOMB, la jauge SUPER SHOT) autour d'un sol ravagé vu du ciel, des villages aux toits de tuiles crevés par les bombes, une voie ferrée et son train, une rivière et ses ponts. L'avion choisi par le joueur, dessiné d'après le vrai (P-38 Lightning, F5U, Spitfire, Ta 152, Zero, Fiat G.56, XP-55 Ascender). La jauge pleine qui se vide est le super tir, une bombe amène une formation de bombardiers dont le tapis de bombes nettoie l'écran |
| Street Hoop | `strhoop.json` | les points des deux équipes, l'horloge, les deux jauges SUPER SHOT, le terrain et son panier | un demi-terrain dans un parc comme dans le jeu, des arbres, une barrière de bois, du monde sur les bancs, un vélo dans l'herbe, l'asphalte peint et le panier à droite. Trois contre trois, la balle passe de main en main, les points lus dans le jeu sont des tirs de loin, des tirs en suspension ou des smashs, un tir rate de temps en temps. La jauge pleine qui se vide est un super tir enflammé. Les points en grosses lettres en haut, rouge et bleu, l'horloge dans son cadre orange entre les deux jauges SUPER SHOT, 1P au-dessus du joueur |
| Super Dodge Ball | `sdodgeb.json` | la vie des trois joueurs de chaque équipe en trois couleurs, TIME, les deux jauges POW | un terrain vague pavé en fin d'après-midi, des gens qui regardent par-dessus la palissade, des boîtes et des bouteilles qui traînent. Deux équipes de trois joueurs à nous, grosses têtes sur petits corps. La balle traverse et se fait attraper, un joueur dont la vie baisse la prend en pleine figure, à zéro il est éliminé, la jauge POW pleine qui se vide donne un tir enflammé. Les barres de vie des deux équipes en haut avec les noms, TIME au milieu |
| Neo Bomberman | `neobombe.json` | les vies en petites têtes, le feu, le stage, un labyrinthe et ses blocs | le labyrinthe vu de haut comme dans le jeu, un style par monde (ruines, eau, usine, château), des piliers de pierre une case sur deux, des blocs qui cassent et reviennent. De petits robots mineurs à nous parcourent les couloirs, les bombes posées dans le jeu sont posées ici et sautent, les flammes partent en croix, des boules errent. Une bande de couleur en haut avec les vies, le feu et le stage |
| Twinkle Star Sprites | `twinspri.json` | les cœurs, les bombes, la jauge Pow et le nom du personnage, une colonne entre deux terrains | deux terrains côte à côte comme dans le jeu, une forêt vue de haut qui défile vers le bas, la colonne ornée entre les deux. Dans chaque terrain une petite sorcière à nous tire sur les boules qui descendent, les chaînes envoient des boules de feu de l'autre côté, les attaques lues dans le jeu (niveau 1, 2, boss) passent de l'autre côté, un cœur perdu la fait tourner, une bombe nettoie son terrain. Le nom et les cœurs en haut, Pow 1 2 Max et les bombes en bas |
| League Bowling | `lbowling.json` | le chrono du lancer, une piste et ses quilles | la salle vue de derrière le joueur comme dans le jeu, les pistes cirées qui filent vers leurs quilles, les pistes voisines, les panneaux éclairés du mur du fond. Chaque fois que le chrono du jeu repart, un joueur à nous lance, la boule file en courbe et les quilles volent, STRIKE ! ou SPARE ! de temps en temps. TIME dans son cadre en haut |
| Neo Drift Out | `neodrift.json` | le temps avec ses centièmes, une route et une voiture de rallye | les spéciales vues du ciel, une piste de terre dans les bois, puis une route goudronnée dans la campagne. La voiture de rallye blanche dérape dans les virages et soulève la poussière, une arche de contrôle passe quand du temps s'ajoute. TIME en gros chiffres bleus avec les centièmes, comme dans le jeu |
| Riding Hero | `ridhero.json` | le temps, les turbos, le classement, une route et ses vibreurs | la route vue de derrière la moto file vers l'horizon comme dans le jeu, ses vibreurs rouges et blancs, les virages qui la balancent, un volcan enneigé, des montagnes, la grande tribune et un dirigeable. Le pilote se penche dans les virages, les autres sont dépassés ou reviennent, un turbo dépensé donne un coup d'accélérateur. SPEED, TIME, TURBO et RANK là où le jeu les met |
| Thrash Rally | `trally.json` | le temps et la vitesse, une route et une voiture de rallye | une piste de terre entre des barrières jaunes et noires, puis une route enneigée avec vibreurs rouges et blancs et bonshommes de neige, vues du ciel. La voiture rouge dérape au milieu de ses rivales, une arche de contrôle passe quand du temps s'ajoute, la vitesse lue dans le jeu règle l'allure. TIME en jaune, SPEED en rouge |
| Magician Lord | `maglord.json` | les HP, les vies, le nom de la forme prise, un chemin de planches et les arbres | les villages de huttes dans les arbres géants comme dans le jeu, puis un temple au visage de pierre géant. Un héros à nous parcourt les chemins et lance sa magie sur les morts-vivants, et prend la forme lue dans le jeu (ninja, homme-poisson, samouraï, guerrier dragon, guerrier des mers, dieu du tonnerre). 1UP et les vies en haut, HP et POW dans leurs jauges en bas |
| NAM-1975 | `nam1975.json` | les grenades, les balles de l'arme spéciale, une ville en feu et sa route | notre soldat vu de dos en bas de l'écran tire dans la ville en feu, puis la jungle et sa rivière, comme dans le jeu. Les ennemis courent sur la route, des chars et des hélicoptères passent, le viseur suit sa cible. Les balles, les grenades et l'arme lues dans le jeu s'affichent (fusil, mitrailleuse, lance-flammes, bazooka), une grenade saute là où est le viseur |
| Cyber-Lip | `cyberlip.json` | P= et les vies, le chrono, la ville la nuit, notre héros qui tire | notre héros parcourt la ville la nuit, devant le théâtre et les boutiques, et tire sur les robots marcheurs et les drones. L'arme dont les munitions baissent dans le jeu est celle qu'il tire (auto, wide, fire, bazooka, grenade). 1P et TIME en bleu en haut, l'arme et ses munitions dans la barre bleue en bas, P= et les vies, comme dans le jeu |
| Ghost Pilots | `gpilots.json` | le score ou le titre, les avions qui restent et les bombes, l'avion qui suit le stick et tire, BOMBE!, POWER UP | vu du ciel comme dans le jeu, la terre brune et sa jungle, puis la mer d'un bleu profond. Notre chasseur à gros moteur en étoile, des chasseurs ennemis rouges et des bombardiers, des chars au sol. Une bombe dépensée tombe et nettoie l'écran. 1-PLAYER et le score en haut, les avions qui restent, B= et les étoiles en bas à gauche |
| Alpha Mission II | `alpham2.json` | le score ou le titre, les vaisseaux qui restent, le vaisseau qui suit le stick et tire, POWER UP | notre chasseur survole une immense forteresse dans l'espace comme dans le jeu, des soucoupes arrivent, les tourelles de la forteresse sautent. Les vaisseaux qui restent =02 et le score en haut, G= l'or et la puissance de l'arme en bas |
| Viewpoint | `viewpoin.json` | le score ou le titre, les vaisseaux qui restent, le vaisseau qui suit le stick et tire, BOMBE! quand la bombe portée part | le sol de dalles d'ardoise vu de biais défile comme dans le jeu, notre vaisseau le survole avec son ombre, des rampants et des mines en anneau arrivent. La bombe portée dans le jeu (plasma, feu, chercheuse) s'affiche, quand elle part elle balaie l'écran dans sa couleur. 1UP, le score et les trois voyants de bombe en bas |
| Zed Blade | `zedblade.json` | le score ou le titre, les vaisseaux qui restent et les bombes, le vaisseau qui suit le stick et tire, BOMBE!, POWER UP | notre chasseur survole une vallée à l'aube comme dans le jeu, montagnes, forêt, piliers de pierre, les hélicoptères ennemis arrivent par groupes, une bombe dépensée les fait tous sauter. 1P- en rouge et 2P- en bleu en haut, les bombes en capsules bleues en bas à gauche, LEVEL et le niveau du tir |
| Prehistoric Isle 2 | `preisle2.json` | le score ou le titre, les hélicoptères qui restent et les bombes, le vaisseau qui suit le stick et tire, BOMBE!, POWER UP | notre hélicoptère survole la mer au bord de l'île comme dans le jeu, des piliers de pierre sortent des vagues, les reptiles volants arrivent, une bombe dépensée fait sauter l'écran. PLAYER 1 et le score en haut, les hélicoptères qui restent, Lv le niveau de l'arme et les bombes en bas à gauche |
| Shock Troopers 2nd Squad | `shocktr2.json` | les grenades, le chrono, la jauge de puissance, une route, un commando et un char | la rue de la ville vue du dessus comme dans le jeu, le jardin et le mur fissuré, le trottoir blanc carrelé et ses lampadaires, la route grise et sa ligne jaune, des voitures brûlées. Notre commando remonte la route et tire sur les soldats, les jeeps et les chars qui arrivent. L'arme lue dans le jeu est celle qu'il tire (normal, fire, round, missile, boomerang), une grenade dépensée est lancée, une vie perdue explose à côté de lui. En haut un visage à nous, 1P- et le score, TIME en gros chiffres jaunes, en bas les grenades, le cadre de l'arme et LV |
| Robo Army | `roboarmy.json` | la jauge LIFE, x et les vies, les orbes POW, la ville au soir | le bord de la ville au soir comme dans le jeu, un ciel violet, des palissades de bois, une maison de béton fissurée, des arbres et de l'herbe sèche. Un cyborg à nous combat les robots qui arrivent des deux côtés. Les points lus dans le jeu sont des coups portés, la LIFE qui baisse un coup reçu, une vie perdue une chute. LIFE en bleu, 1P- et le score, x et les vies, les orbes POW en haut |
| Burning Fight | `burningf.json` | la jauge de vie, le chrono, P= et les vies, des boutiques et leurs lanternes | une rue de petites boutiques la nuit comme dans le jeu, des enseignes carrées, des lanternes de papier rouges, des vitrines éclairées, des distributeurs et des pavés. Notre combattant affronte les voyous qui arrivent des deux côtés. Les points sont des coups portés, la vie qui baisse un coup reçu. 1UP et le score avec la jauge jaune, TIME en gros chiffres jaunes au milieu, P= et les vies en bas à gauche |
| Mutation Nation | `mutnat.json` | la jauge LIFE, B et les objets d'attaque, une ville en ruine | la ville en ruine comme dans le jeu, des tours bleues sous un ciel violet, de vieux immeubles de pierre aux vitres cassées, des gravats, une épave et la route fissurée. Notre combattant affronte les mutants qui arrivent des deux côtés, les points sont des coups portés, la LIFE qui baisse un coup reçu, un objet d'attaque dépensé balaie l'écran. 1P et le score, LIFE en segments arc-en-ciel, B et les objets en haut |
| Sengoku | `sengoku.json` | les vies, les six cases de LIFE, la couleur de la sphère, un coucher de soleil rouge | la fin du monde au coucher du soleil comme dans le jeu, un ciel rouge sang et orange, un château flottant sur son île, les ruines violettes et les bannières d'un village, le champ doré et la brume grise. Notre sabreur à nous combat les guerriers fantômes en armure et les ninjas, chaque coup laisse une traînée de lumière, la sphère prise dans le jeu fait briller la lame de sa couleur. SCORE-, un visage à nous, les vies et les six cases de LIFE |
| Sengoku 2 | `sengoku2.json` | les vies, les six cases de LIFE, la couleur de la sphère, un ciel de crépuscule et le sable | sous le grand pont de bois au crépuscule comme dans le jeu, un ciel violet et orange, des montagnes sombres, les toits d'un village dans la brume, l'arche du pont sur sa pile de pierre, le sable et ses pierres. Notre sabreur combat les guerriers en armure sombre, la sphère lue dans le jeu (bleue, rose, jaune) s'affiche. 1P-, un visage à nous, les vies et les cases de LIFE |
| Ninja Combat | `ncombat.json` | LIFE et POW, les vies, un parc la nuit et ses lampadaires | un parc la nuit comme dans le jeu, des arbres sombres, des lampadaires aux globes blancs, un portique aux piliers or et bleu sous son toit, la grille et les pavés gris. Notre ninja rouge affronte les ninjas noirs, gris et violets. En bas comme dans le jeu un visage à nous, POW et LIFE, TIME en minutes et secondes, les vies et le nom du personnage |
| Ninja Commando | `ncommand.json` | la jauge LIFE, le chrono, un chemin dans la jungle | la jungle vue du dessus comme dans le jeu, un chemin de terre qui serpente entre les buissons, des rochers violets, une rivière et son pont de bois. Notre ninja bleu remonte le chemin et lance des dragons de feu sur les ninjas ennemis. En bas comme dans le jeu un visage à nous, LIFE en jaune, TIME en minutes et secondes |
| Blue's Journey | `bjourney.json` | les cœurs, les vies, les fleurs, l'herbe et la terre | le pays des plantes géantes comme dans le jeu, de longues feuilles rayées de jaune qui pendent du haut, un arbre bleu, des feuilles rouges, un énorme pot de terre, des boutons roses, l'herbe sur la terre dorée. Notre petit héros à nous lance des feuilles aux escargots et aux abeilles. 1P=, les vies, TIME=, LIFE et ses cœurs en haut, les fleurs en bas à gauche |
| Puzzle Bobble 2 | `pbobbl2n.json` | le chrono du tir, les blocs de couleur | la plage des premiers rounds comme dans le jeu, un ciel bleu profond et ses gros nuages, des palmiers, la mer et un voilier. Les plateaux dans leurs cadres de métal, le lanceur et sa flèche, les bulles partent quand le chrono du tir du jeu repart |
| Magical Drop II | `magdrop2.json` | LEVEL, les quotas des deux joueurs | le mur de briques orange et ses colonnes de marbre pâle autour des deux champs bleu-vert, comme dans le jeu. Le fou lance les gouttes, le quota qui baisse les fait éclater, le niveau qui monte pousse une rangée. LEVEL en haut, les quotas en bas |
| Money Puzzle Exchanger | `miexchng.json` | la chaîne, MAX CHAIN, le niveau | les losanges pastel bleus, blancs et lilas comme dans le jeu, les deux champs encadrés de rose pleins de pièces de 10, 50, 100 et 500, une petite tirelire à nous sous chaque champ. Une chaîne lue dans le jeu fait éclater des pièces. STAGE et MAX CHAIN entre les champs |
| Puzzle De Pon! | `puzzledp.json` | la bulle du lanceur et la suivante, LEVEL | le ciel bleu pâle plein de grandes étoiles douces comme dans le jeu, les plateaux entre leurs piliers de briques autour d'une nuit étoilée, le cadran étoilé dont l'aiguille tourne avec le temps qui reste. La bulle tirée et la suivante viennent du jeu. LEVEL en bas |
| Puzzle De Pon! R! | `puzzldpr.json` | la bulle du lanceur et la suivante, LEVEL | les mêmes plateaux entre leurs piliers de briques et le même cadran étoilé que Puzzle De Pon!, sous un ciel rose étoilé, comme dans le jeu |
| Panic Bomber | `panicbom.json` | les jauges de puissance des deux joueurs, le niveau | deux champs sur le damier vert comme dans le jeu, les pièces de trois petites têtes rondes à nous tombent et s'empilent, trois de la même couleur éclatent, les bombes sautent en croix de flammes. Les points lus dans le jeu font sauter les bombes, la puissance qui monte fait une grosse explosion. SCORE et NEXT au-dessus de chaque champ |
| Pop 'n Bounce | `popbounc.json` | les vies, une balle qui rebondit | la jungle au crépuscule comme dans le jeu, des créatures rondes et molles à nous entassées en haut du champ, la barre du bas renvoie la balle, une créature touchée éclate avec celles de sa couleur qui la touchent. ATTACK en haut, 1P, les vies et BALL au milieu |
| Super Bubble Pop | `sbp.json` | les blocs de couleur | le tourbillon magenta et ses bulles lilas comme dans le jeu, le plateau blanc vu de biais où tombent les bulles, notre petit robot à nous tire sa bulle dans une colonne, trois de la même couleur éclatent. Le score dans sa capsule en haut |
| Spin Master | `spinmast.json` | les segments de vie, B et les bombes, les vies, le désert | le désert des pyramides comme dans le jeu, un ciel bleu profond, de grandes pyramides, un sphinx, des dunes et un mur de blocs de pierre. Notre héros à nous lance son yo-yo sur les soldats et les oiseaux, une bombe dépensée fait sauter l'écran. 1P, la vie en segments orange et les bombes B en haut, les vies en bas |
| Ganryu | `ganryu.json` | le chrono, les vies, les armes qui restent, une rue la nuit | une rue du vieux Japon la nuit comme dans le jeu, des maisons de bois sous leurs toits de tuiles sombres, des rideaux au blason rond, des lanternes. Notre sabreur à nous combat les ninjas de la nuit, sa lame laisse une traînée de lumière, une arme dépensée dans le jeu est lancée. PLAYER_1 et le score, la jauge jaune, un visage par vie, TIME en gros chiffres, l'arme et son nombre |
| Zupapa! | `zupapa.json` | les vies, les plateformes | la grotte bleue et ses vieilles statues de pierre comme dans le jeu, les plateformes rayées orange et bleu. Notre petit héros rond à nous parcourt les plateformes, saute de l'une à l'autre et chasse les monstres, qui s'envolent dans une pluie d'étoiles. P1, le score et les vies |
| Neo Mr. Do! | `neomrdo.json` | les vies en cerises, le champ de cases | le champ de cases colorées et leurs jouets et outils dans un cadre d'étoiles, comme dans le jeu. Notre petit mineur à nous creuse ses tunnels, ramasse les cerises, les monstres bleus le suivent dans les tunnels et tombent sous sa boule. 1P-, les vies et EXTRA qui s'allume lettre par lettre |
| Super Sidekicks | `ssideki.json` | les buts des deux équipes en gros, le temps | le match dans le stade, les deux drapeaux avec les buts dans leurs cadres orange et TIME sur son panneau, comme dans le jeu. Un but lu dans le jeu envoie le ballon au fond des filets |
| Super Sidekicks 2 | `ssideki2.json` | les buts des deux équipes en gros | le match dans le stade, le bandeau bleu en haut avec les deux drapeaux et les buts en gros chiffres blancs, comme dans le jeu. Un but lu dans le jeu envoie le ballon au fond des filets |
| Tecmo World Soccer '96 | `twsoc96.json` | le terrain et un ballon qui le traverse | le match dans le stade, les deux drapeaux en haut et l'horloge ronde entre eux, comme dans le jeu. Aucune valeur du jeu n'est encore connue, alors le match se joue tout seul |
| Goal! Goal! Goal! | `goalx3.json` | les buts des deux équipes en gros, le temps | le match dans le stade, les drapeaux et les buts en gros chiffres jaunes en haut, le temps avec sa petite lune, comme dans le jeu. Un but lu dans le jeu envoie le ballon au fond des filets |
| Neo-Geo Cup '98 | `neocup98.json` | les buts des deux équipes en gros | le match dans le stade, le bandeau bleu en haut avec les deux drapeaux et les buts, comme dans le jeu. Un but lu dans le jeu envoie le ballon au fond des filets |
| Soccer Brawl | `socbrawl.json` | les buts des deux équipes en gros, le POWER METER de chaque équipe, le temps | le football du futur sur un terrain de nuit, nos joueurs à nous dans leur armure, le POWER METER de chaque équipe en haut et TIME dessous, comme dans le jeu. Les buts et la puissance lus dans le jeu |
| Football Frenzy | `fbfrenzy.json` | les points des deux équipes en gros, le chrono du quart-temps, les lignes du terrain | le terrain vu de haut avec ses lignes et ses zones d'en-but rouge et bleue, comme dans le jeu. Deux équipes à nous s'alignent, la balle est mise en jeu, le porteur file jusqu'au plaquage. Les points lus dans le jeu sont des touchdowns. Les points des deux équipes en gros chiffres jaunes et le chrono du quart-temps en haut |
| Pleasure Goal | `pgoal.json` | les buts des deux équipes en gros, le temps | le futsal, cinq contre cinq dans le stade, un visage à nous pour chaque équipe à côté de ses buts et le temps au milieu, comme dans le jeu. Un but lu dans le jeu envoie le ballon au fond des filets |
| Baseball Stars Professional | `bstars.json` | la manche, le compte B S O en voyants | le terrain vu de derrière le marbre, notre batteur à nous, le compte B S O en voyants avec l'horloge et la boîte de la manche, comme dans le jeu. Les balles, prises et retraits lus dans le jeu font les lancers |
| 2020 Super Baseball | `2020bb.json` | le terrain et le temps | le baseball du futur sur son terrain clair, la boîte bleue avec la manche et le temps, comme dans le jeu. Les retraits comptés dans le jeu font les actions, entre deux le jeu se joue tout seul |
| Top Player's Golf | `tpgolf.json` | STROKE et les coups, le temps qui reste pour le coup | le parcours et son drapeau, les cadres bleus avec HOLE et PAR, STROKE et le temps, comme dans le jeu. La balle vole vers le drapeau à chaque coup lu dans le jeu |
| Power Spikes II | `pspikes2.json` | les jauges de puissance des deux joueurs, le temps | la salle avec ses projecteurs et ses tribunes pleines, trois joueurs à nous de chaque côté du filet, comme dans le jeu. Le ballon passe d'un côté à l'autre, les joueurs sautent et smashent. Un super coup dépensé dans le jeu est un smash en feu. Le temps sur son panneau et les jauges POWER |
| Bang Bead | `bangbead.json` | le terrain dans la rue et la balle, TIME, les jauges du pouvoir 'Miracle' et leurs étoiles | le terrain dans la rue vu du dessus comme dans le jeu, les voitures garées le long du trottoir, la plaque d'égout et les marques orange. Deux joueurs à nous se renvoient la balle d'un bout à l'autre, les lignes de but et leurs étoiles jaunes s'allument à chaque but, un pouvoir 'Miracle' dépensé dans le jeu est un tir en feu. PLAYER et le score, TIME au milieu, les jauges de pouvoir en bas |
| Battle Flip Shot | `flipshot.json` | l'arène et sa cible, la balle, TIME | l'arène de métal bleu-vert vue du dessus comme dans le jeu, ses circuits, la grande cible orange au milieu. Deux joueurs à nous derrière leurs boucliers renvoient la balle lumineuse, les six cibles de chaque joueur le long de son mur se fissurent et cassent, une cible touchée dans le jeu est un tir sur elle. SCORE et TIME en haut |
| Over Top | `overtop.json` | le temps, RANK, la vitesse, le temps du tour | les étapes vues du ciel comme dans le jeu, une piste de terre dans la forêt de pins, puis une route grise entre les champs, la voiture rouge parmi ses rivales. La carte dans sa petite télévision en haut à gauche, le temps en gros chiffres jaunes, RANK, le compteur et le temps du tour. Une place gagnée dans le jeu est une rivale dépassée |
| Stakes Winner | `stakwin.json` | un cheval au galop, la vitesse, l'endurance et la force du cheval | un hippodrome japonais comme dans le jeu, le gazon vert et ses lisses blanches, la tribune et son public. Huit chevaux et jockeys à nous galopent, le cheval du joueur porte son 1P, le poteau d'arrivée vient et le vainqueur s'affiche. Le chrono de la course en haut à gauche, la jauge du cheval en bas, sa vitesse, son endurance et sa force lues dans le jeu |
| Stakes Winner 2 | `stakwin2.json` | un cheval au galop, POWER, la vitesse, l'endurance et l'accélération du cheval | Longchamp comme dans le jeu, sa tribune et son moulin, le gazon vert. Les chevaux à nous galopent, POWER en bas lu dans le jeu, la puissance dépensée fait foncer le cheval du joueur, sa vitesse, son endurance et son accélération |
| Jockey Grand Prix | `jockeygp.json` | un cheval au galop sur la terre, CREDIT | la piste en terre et sa lisse verte comme dans le jeu, huit chevaux numérotés à nous, le tableau des cotes en haut avec les numéros, WAGER et CREDIT. Le numéro du vainqueur s'allume sur le tableau. Aucune valeur du jeu n'est encore connue, alors les courses vont toutes seules |
| Gururin | `gururin.json` | la pièce suivante dans ses couleurs, le niveau | le damier bleu et violet comme dans le jeu, les piliers dorés et leurs médaillons, les plateaux dans leurs cadres dorés. Les petits bonshommes ronds à nous tombent par trois, quatre de la même couleur qui se touchent s'en vont, et le plateau tourne d'un quart de temps en temps, tout retombe de l'autre côté. La pièce et la suivante dans leurs couleurs lues dans le jeu, LEVEL |
| Ghostlop | `ghostlop.json` | TIME | une rue de la ville la nuit comme dans le jeu, les deux champs pleins de petits fantômes à nous de toutes les couleurs, un petit chasseur sous chaque champ tire les fantômes vers le haut, trois de la même couleur qui se touchent disparaissent. Au milieu, PLAYER 1 et son score, TIME en gros chiffres, PLAYER 2 ou COMPUTER |
| Pochi and Nyaa | `pnyaa.json` | les blocs | la forêt verte et ses lumières douces comme dans le jeu, les champs de blocs tout doux aux petites têtes de chats et de chiens à nous, les paires tombent, quatre de la même couleur qui se touchent partent et les chaînes comptent. NEXT à côté du champ, le score en haut, et de gros ours en peluche à nous assis dans la forêt |
| Puzzled | `joyjoy.json` | la pièce suivante dans sa couleur, les ballons qui restent | les collines vertes et les nuages blancs comme sur le titre du jeu, les tours de briques et leurs puits. Les pièces tombent et remplissent les lignes, les lignes pleines partent, et quand les briques de l'étape sont parties le ballon de l'enfant s'envole. NEXT dans sa couleur lue dans le jeu, le score, STAGE et les ballons qui restent au milieu |
| Zintrick | `zintrckb.json` | le temps, les jauges ENERGY | les montagnes vertes sous un ciel pâle comme dans le jeu, les deux champs dans leurs cadres violets, les joyaux en forme de gouttes suspendus en haut. Un petit lanceur à nous sous chaque champ lance un joyau dans une colonne, trois de la même couleur alignés partent, un objet utilisé dans le jeu vide une rangée. Le temps en gros entre les champs, ENERGY, ITEM et LEVEL de chaque joueur |
| Digger Man | `diggerma.json` | les vies, les bombes, ENERGY, un petit mineur | la mine dans son cadre de briques grises comme dans le jeu, la terre orange, les murs de pierre grise, les rochers qui tombent dans les tunnels, les joyaux de couleur. Notre petit mineur à nous creuse jusqu'à chaque joyau, une bombe dépensée dans le jeu fait sauter les pierres autour de lui. Le score, les joyaux qui restent en gros chiffres bleus, ENERGY, les vies et les bombes |
| The Irritating Maze | `irrmaze.json` | TIME et ses dixièmes, les vies | le sol en damier rouge comme dans le jeu, le couloir du labyrinthe entre ses rails bleus, la grande flèche, le butoir et la caisse. Notre pointeur suit le couloir sans toucher les rails, une vie perdue dans le jeu est une décharge électrique. TIME en chiffres rouges lumineux avec ses dixièmes, la carte du labyrinthe et le pointeur |
| Andro Dunos | `androdun.json` | le score ou le titre, les vaisseaux qui restent, le vaisseau qui suit le stick et tire, POWER UP | l'espace au-dessus d'une planète comme dans le jeu, la lueur bleue de l'horizon et le sol rocheux, notre petit chasseur à nous contre des capsules ennemies rondes. 1P et le score, les quatre armes et leurs niveaux lus dans le jeu dans leurs couleurs, les vaisseaux qui restent |
| Captain Tomaday | `ctomaday.json` | le score ou le titre, les vies, le vaisseau qui suit le stick et tire, POWER UP | la forêt vue du ciel comme dans le jeu, ses petites maisons aux toits rouges, la voie ferrée et son train à vapeur, une rivière. Notre petit engin rouge à nous et sa crête de feuilles vertes contre des robots volants en fer-blanc. PLAYER 1 et le score, les vies et la puissance des deux bras lues dans le jeu |
| Choutetsu Brikin'ger | `ironclad.json` | le score ou le titre, la jauge de vie, le vaisseau qui suit le stick et tire, POWER UP, LEVEL 2 | la mer au crépuscule, les cuirassés de fer à l'horizon, notre chasseur à vapeur à nous et son poing de robot contre des canonnières volantes. La jauge de vie, POWER et LEVEL lus dans le jeu, les armes des bras |
| Last Hope | `lasthope.json` | le score ou le titre, le vaisseau qui suit le stick et tire | l'espace profond comme dans le jeu, plein d'étoiles bleues et blanches, les nébuleuses et une grosse planète bleue, notre petit chasseur à nous et son module bleu contre des drones en tonneau rouges. Le score en haut |
| Bang Bang Busters | `b2b.json` | les cœurs, la jauge du boss | le monde de glace comme dans le jeu, le ciel bleu et son aurore, les plateformes de blocs de glace. Notre petit chasseur à nous enferme les pingouins et les phoques à nous dans ses bulles et les chasse. Le score et les cœurs en haut, l'étape, la jauge du boss lue dans le jeu |
| Crossed Swords | `crsword.json` | l'énergie, GOLD, la magie | la forêt la nuit comme dans le jeu, un chevalier en armure à nous face à nous avec son bouclier et son épée, notre chevalier vu de dos en contour de lumière. Les épées se croisent, ENEMY et sa jauge en haut. L'énergie, l'or et la magie lus dans le jeu, un coup reçu, l'or qui monte, un sort d'éclairs |
| Eight Man | `eightman.json` | LIFE, BOMB, le temps | la ville en ruine au coucher du soleil comme dans le jeu, des tours dorées et un pont effondré. Un cyborg rapide à nous, bleu et argent, combat des mutants violets et des cyborgs armés, et laisse une traînée de copies derrière lui quand le jeu allume son 8 Power. 1P et le score, LIFE, BOMB et le temps dans sa case rouge |
| Nightmare in the Dark | `nitd.json` | les vies, le temps, la pleine lune, un petit gardien | le cimetière la nuit sous une énorme pleine lune comme dans le jeu, les plateformes de pierres moussues, les arbres nus et les tombes. Notre petit gardien à nous enflamme les zombies et les fantômes à nous avec sa lanterne et chasse les boules de feu. 1UP et le score, les vies et TIME en jaune lus dans le jeu |
| The Super Spy | `superspy.json` | l'énergie, les balles, le couloir | le couloir de l'immeuble comme dans le jeu, ses portes et leurs signaux rouges, un combattant masqué à nous face à nous avec ses couteaux, nos poings frappent d'en bas. L'énergie lue dans le jeu baisse quand il nous touche, une balle dépensée est un tir, il tombe et on monte d'un étage. 1P et le score, EX, l'arme et ses balles, l'étage |
| Quiz King of Fighters | `quizkof.json` | les vies en cœurs, Q et les quatre réponses | une scène dans la ville la nuit comme dans le jeu, deux combattants à nous face à face. Le panneau de la question et ses quatre réponses A B C D, le temps qui passe. Les questions sont à nous, le score qui monte est une bonne réponse et un grand rond, une vie perdue est une mauvaise réponse et une grande croix. P1, le score et LIFE |
| Quiz Daisousa Sen | `quizdais.json` | les vies en cœurs, Q et les quatre réponses | le grillage devant la ville au crépuscule comme dans le jeu, un détective encapuchonné à nous et son équipier. Le panneau de la question et ses quatre réponses A B C D, le temps qui passe. Les questions sont à nous, le score qui monte est une bonne réponse et un grand rond, une vie perdue est une mauvaise réponse et une grande croix. P1, le score et LIFE |
| Quiz Meitantei Neo & Geo | `quizdai2.json` | les vies en cœurs, Q et les quatre réponses | le bureau d'un détective comme dans le jeu, ses étagères de livres et sa fenêtre, un vieux détective à nous et son jeune assistant. Le panneau de la question et ses quatre réponses A B C D, le temps qui passe. Les questions sont à nous, le score qui monte est une bonne réponse et un grand rond, une vie perdue est une mauvaise réponse et une grande croix. P1, le score et LIFE |
| Chibi Maruko-chan Deluxe Quiz | `marukodq.json` | les vies en cœurs, Q et les quatre réponses | un studio de télévision comme dans le jeu, ses projecteurs et son arc-en-ciel, deux enfants à nous sur le plateau. Le panneau de la question et ses quatre réponses A B C D, le temps qui passe. Les questions sont à nous, le score qui monte est une bonne réponse et un grand rond, une vie perdue est une mauvaise réponse et une grande croix. P1, le score et LIFE |
| Minasan no Okagesamadesu! | `minasan.json` | les tuiles, les pas du dé | la table bleue et sa partie de mahjong comme dans le jeu. La main cachée de l'adversaire en haut, les tuiles jetées au milieu, notre main de treize tuiles en bas. Une tuile est piochée, une tuile est jetée, de temps en temps une main gagne par RON ou TSUMO, et les cases des points à droite suivent notre partie. Les pas du jeu de plateau lus dans le jeu lancent un dé, le temps pour jouer |
| Mahjong Kyo Retsuden | `mahretsu.json` | les tuiles, le temps | le tapis vert et les dos de tuiles jaunes comme dans le jeu. La main cachée de l'adversaire en haut, les tuiles jetées au milieu, notre main de treize tuiles en bas. Une tuile est piochée, une tuile est jetée, de temps en temps une main gagne par RON ou TSUMO, et les cases des points à droite suivent notre partie. Le temps pour jouer lu dans le jeu |
| Janshin Densetsu | `janshin.json` | les tuiles, HP | le tapis violet et les dos de tuiles verts comme dans le jeu. La main cachée de l'adversaire en haut, les tuiles jetées au milieu, notre main de treize tuiles en bas. Une tuile est piochée, une tuile est jetée, de temps en temps une main gagne par RON ou TSUMO, et les cases des points à droite suivent notre partie. Le panneau du héros avec HP, MP, WEAPON et SHIELD lus dans le jeu, les HP qui baissent, le temps pour jouer |
| Bakatonosama Mahjong Manyuuki | `bakatono.json` | les tuiles, le temps | le tapis olive et les dos de tuiles orange comme dans le jeu. La main cachée de l'adversaire en haut, les tuiles jetées au milieu, notre main de treize tuiles en bas. Une tuile est piochée, une tuile est jetée, de temps en temps une main gagne par RON ou TSUMO, et les cases des points à droite suivent notre partie. Le temps pour jouer lu dans le jeu |
| Idol Mahjong Final Romance 2 | `froman2b.json` | les tuiles | le tapis vert dans son cadre de bois et les dos de tuiles orange comme dans le jeu. La main cachée de l'adversaire en haut, les tuiles jetées au milieu, notre main de treize tuiles en bas. Une tuile est piochée, une tuile est jetée, de temps en temps une main gagne par RON ou TSUMO, et les cases des points à droite suivent notre partie |
| Shougi no Tatsujin | `moshougi.json` | le plateau de bois | la côte rocheuse au bord de la mer comme dans le jeu, le plateau de bois et ses deux supports, celui de l'adversaire en haut à gauche et le nôtre en bas à droite. Nos pièces avancent une à une, une pièce prise va sur le support de celui qui l'a prise, la pendule de chacun tourne |

- Les valeurs viennent des codes de triche de FinalBurn Neo et de MAME 2003-Plus et doivent encore être confirmées en jeu (`test_retroarch.bat` les affiche). Le score de Blazing Star, Puzzle Bobble, Shock Troopers, Pulstar, Magical Drop III, Sengoku 3, Top Hunter, Last Resort, des deux Aero Fighters, de Strikers 1945 Plus, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Magician Lord, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army, Burning Fight, Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger, Puzzle De Pon!, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Bang Bead, Battle Flip Shot, Gururin, Ghostlop, Pochi and Nyaa, Puzzled, Zintrick, Digger Man, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords, Eight Man, Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo et Chibi Maruko-chan Deluxe Quiz n'est dans aucune base, apprends-le avec `learn.bat` (voir Apprendre le score). En attendant, le titre défile à sa place sur la dalle.
- Quand le stick et les boutons se lisent (le BIOS de la Neo Geo les garde, avec MAME comme avec RetroArch), les vaisseaux de Blazing Star, de Pulstar, de Last Resort, de Viewpoint, de Zed Blade et de Prehistoric Isle 2, les avions des Aero Fighters, de Strikers 1945 Plus, de Ghost Pilots et d'Alpha Mission II, le commando de Shock Troopers 2nd Squad et le ninja de Ninja Commando (haut et bas), les chasseurs de Top Hunter, les sorcières de Twinkle Star Sprites, les flèches de Puzzle Bobble, de Puzzle Bobble 2 et des deux Puzzle De Pon!, les fous de Magical Drop II et III et les tirelires de Money Puzzle Exchanger les suivent. Le bouton A tire dans Blazing Star, Pulstar, Last Resort, les Aero Fighters, les deux Shock Troopers et Ninja Commando, et frappe dans Sengoku 3 et Top Hunter. Dans Top Hunter, haut et bas font sauter d'une voie à l'autre et B fait sauter. Dans Last Resort, le bouton B lance l'unité. Dans Magical Drop II et III et Money Puzzle Exchanger, le bouton A prend les gouttes ou les pièces et B les relance. Tant que le joueur n'y a pas touché, la scène joue toute seule. Sur la dalle des quinze shoot'em up aussi, le vaisseau suit le stick et tire avec le bouton A.
- Quand personne ne joue, l'écran des pièces, comme pour les jeux de combat (voir Écran des pièces).
- `demo_neogeo.bat` les montre sans jouer. Choisis le jeu dans la liste, ou donne-le directement, `demo_neogeo.bat wjammers` par exemple.

### Tous les jeux Neo Geo

Les jeux Neo Geo connus de MAME (clones compris) ont une scène commune selon leur genre, sans rien faire. En haut, le titre du jeu, fixe quand il tient, qui défile sinon.

| Genre | Fichier | Ce qui s'affiche |
|---|---|---|
| Combat (King of Fighters, Samurai Shodown, Fatal Fury, Art of Fighting, World Heroes...) | `neogeo_combat.json` | façon Vera. En haut le score, ou le titre tant qu'il n'est pas appris, et du côté de l'ordinateur INSERT COIN qui clignote, ou les crédits et PRESS START tour à tour. Au milieu les barres de vie vertes et le chrono dans un cadre, « KO » à la fin du combat (52 jeux, voir le tableau Jeux de combat), sinon « VS ». En bas « P1 », et « CPU » ou « P2 » en face. Dans 34 jeux, le nom du personnage en train de se battre s'affiche à côté, en blanc (« P1 RALF » et « LEONA CPU »). Un filet orange tout en bas. Quand personne ne joue, l'écran des pièces (plus bas) |
| Shoot'em up (Zed Blade, Viewpoint, Ghost Pilots...) | `neogeo_shoot.json` | un petit vaisseau qui traverse un champ d'étoiles et tire quand le score monte |
| Sport et course (Neo Drift Out, Riding Hero, Super Sidekicks 2...) | `neogeo_sport.json` | un terrain avec un ballon qui rebondit |
| Réflexion, quiz, mahjong (Puzzle De Pon, Pop 'n Bounce, Magical Drop II...) | `neogeo_reflexion.json` | une rangée de blocs de couleur qui changent |
| Action, plates-formes, beat'em up et le reste (Ninja Combat, Sengoku 2, Cyber-Lip...) | `neogeo.json` | des collines bleues, et les barres de vie des deux joueurs quand elles sont connues |

- Avec RetroArch, la scène affiche « NEO GEO » au milieu tant que rien n'est connu pour ce jeu. Avec MAME, les crédits s'affichent en plus.
- Avec RetroArch, chaque set Neo Geo de FinalBurn Neo est reconnu. Une version, un bootleg ou un hack prend le fichier de son jeu d'origine, comme avec MAME. Metal Slug 3 Fully Decrypted prend celui de Metal Slug 3, et KOF 2002 Magic Plus celui de KOF 2002 avec son propre nom. Un jeu amateur (homebrew) a la scène de son genre. Seuls le BIOS et les programmes de test ne sont pas reconnus. La liste est dans `dmd\neogeo_sets.json`, et `test_retroarch.bat` dit de quel jeu une version prend le fichier.
- Les crédits d'une Neo Geo MVS sont rangés dans la mémoire de sauvegarde de la borne. MAME la lit. Le cœur FinalBurn Neo de RetroArch ne partage que la mémoire de travail du jeu, donc pas les crédits. ArcadeDMD les devine alors d'après le BIOS de la Neo Geo, qui laisse des traces dans la mémoire de travail. Une pièce mise quand personne ne joue tombe sur la dalle et sur l'écran HD, PRESS START suit, et chaque joueur qui commence prend un crédit. En pleine partie, le BIOS ne montre que la première pièce. Pour que chaque pièce soit vue avec son côté, lance une fois `coin_buttons.bat` (Boutons des pièces, plus bas). FinalBurn Neo garde les crédits de chaque jeu quand on le quitte et les rend la fois suivante. ArcadeDMD garde de même ses crédits devinés (`runtime\neo_credits.json`) et repart d'eux quand le jeu démarre sur son écran titre. FinalBurn Neo doit être en mode MVS (option du cœur Neo-Geo mode), le mode AES de la console ne prend pas de pièces. `runtime\arcadedmd.log` dit ce que le BIOS a fait, et `test_coins.bat` note en détail ce qui change dans sa mémoire pendant que tu mets des pièces à gauche et à droite. Certains jeux gardent une copie des crédits dans leur mémoire de travail. Pour le savoir, apprends-les avec `learn.bat` (même méthode que pour le score) en tapant `crédits=2`, puis remets une pièce et tape `crédits=3`, et encore une fois. Si l'outil trouve une adresse, les crédits s'affichent. S'il répond « Rien trouvé », ce jeu n'en garde pas de copie.
- Les barres de vie et le chrono viennent de la base de codes de triche de MAME 2003-Plus. Ils marchent avec RetroArch comme avec MAME.
- Apprends le score d'un jeu avec `learn.bat` (même méthode que juste en dessous). L'outil crée alors `games\<jeu>.json`, par exemple `games\kof98.json`. Il garde la scène du genre et ses barres de vie, et ajoute le score. Les fichiers communs ne sont jamais modifiés.
- Un jeu qui a son propre fichier (les Metal Slug, ou les jeux faits un par un juste au-dessus) passe toujours avant la scène commune.
- Le score de KOF 98 a été trouvé avec `learn.bat`. Il est rangé dans la fiche de chaque joueur, et cette fiche est la même de KOF 96 à 2001 (barre de vie et jauge de puissance aux mêmes adresses). Le score de ces jeux est donc pris à la même place. Si la dalle n'affiche pas le même score que l'écran dans l'un d'eux, apprends-le avec `learn.bat`, l'adresse trouvée remplace la supposée.
- Dans King of Fighters '96 à 2000, chaque équipe est lue dans la mémoire du jeu (personnages choisis, ordre de passage, personnages déjà battus). Le nom change tout seul quand le personnage suivant entre. `test_retroarch.bat` affiche les deux personnages lus, pratique pour vérifier.
- Le BIOS de la Neo Geo dit qui joue. Contre l'ordinateur, « CPU » s'affiche en face, avec INSERT COIN qui clignote de son côté, ou les crédits et PRESS START tour à tour s'il reste des crédits. À deux, les deux scores sont en haut. Quand personne ne joue, l'écran des pièces juste en dessous.

### Les jeux Capcom CPS1, CPS2 et CPS3

Chaque jeu Capcom CPS1, CPS2 et CPS3 de FinalBurn Neo est reconnu, avec MAME comme avec RetroArch. Ça fait 88 jeux et leurs 942 sets. Une version, un bootleg ou un hack prend le fichier de son jeu d'origine, avec son propre nom quand il en a un (Street Fighter II' Magic Delta Turbo par exemple). Une version dont les propres codes de triche mettent une valeur ailleurs la lit là, dans la rubrique `"per_game"` du fichier (la deuxième révision de JoJo's Venture, la réédition japonaise de Quiz & Dragons, Eco Fighters américain). Les fichiers sont faits par `tools/cps_games.py` à partir de la liste et de la base de codes de triche de FinalBurn Neo.

![Quatre jeux de combat Capcom dans leurs décors, affichage HD](docs/images/hd_capcom_stages.jpg)

- **Ce qui est lu.** La vie de chaque joueur, le chrono, les vies, les bombes, la jauge de super, les personnages et leur nom, le décor, et les crédits quand le jeu les garde. Le chrono s'affiche quand la triche le donne en entier. Dans 23 jeux elle n'en donne qu'une partie, un chiffre, les secondes d'une horloge ou un compteur qui n'est pas le chrono vu dans le jeu. ArcadeDMD ne le lit alors que pour voir que le jeu tourne, sans l'afficher. Le score n'est pas dans les bases de codes de triche, apprends-le avec `learn.bat` (Apprendre le score, plus bas).
- **Qui joue.** Les jeux Capcom n'ont pas de BIOS qui le dit. ArcadeDMD surveille le chrono, le score une fois appris, la vie, les vies et les bombes. Tant qu'ils bougent, le joueur 1 joue. Au bout de 10 secondes sans le moindre changement, l'écran des pièces revient. Il faut pour ça le chrono ou le score (ou la vie dans un jeu de combat), parce que les vies et les bombes seules bougent trop rarement. Sans eux, le jeu reste sur sa scène de jeu. Quand les crédits du jeu sont lus (appris avec `learn.bat` au besoin), un ou deux crédits dépensés sont un départ, et le joueur 1 joue dès l'écran de sélection, pendant 45 secondes, le temps que le combat bouge.
- **RetroArch.** Cœur FinalBurn Neo. Le CPS1 et le CPS2 partagent 64 Ko de RAM à partir de 0xFF0000, le CPS3 ses 512 Ko à partir de 0x2000000, avec ses octets inversés par mots de 32 bits qu'ArcadeDMD remet dans l'ordre. Une valeur hors de cette RAM (les crédits de certains jeux CPS2) n'est lue qu'avec MAME. 1944 et Dimahoo gardent toutes leurs valeurs en dehors, RetroArch n'en montre donc rien et le journal le dit. Lance ces deux jeux avec MAME pour tout voir (dans LaunchBox, Modifier, puis l'onglet Émulation). Mercs est réglé pour trois joueurs dans FinalBurn Neo, et avec deux manettes l'une d'elles dirige deux joueurs. Règle ses DIP switches sur Play Mode 2 Player et Coin Slots 1 (Menu rapide, Options du cœur, DIP Switches), puis relance le jeu.
- **Crédits.** Sous RetroArch la plupart des jeux Capcom ne donnent pas leurs crédits. Une fois que `coin_buttons.bat` a montré tes boutons des pièces à ArcadeDMD, il les compte. Une pièce donne un crédit, et un joueur qui commence en prend un. Une fois les boutons START montrés aussi, un joueur qui appuie sur START avec un crédit commence tout de suite. Sinon le départ se voit quand le jeu se met à bouger, un continue et l'arrivée du joueur 2 quand les vies reviennent de 0 d'au moins 2 (une vie en plus ne fait que 1), et dans Mercs, qui n'a pas de vies, quand l'énergie revient de 0. Le joueur 2 en prend un aussi quand ses valeurs se mettent à bouger après 45 secondes sans (son score monte, une vie ou une bombe en moins, un coup reçu), sauf dans les jeux de combat où sa vie est celle de l'ordinateur. Les fichiers de jeu le disent dans leur rubrique `"coins"`. Ça reste une estimation. Pour un compte exact, apprends où le jeu garde ses crédits avec `learn.bat` (`credits=0`, `credits=1`, `credits=2`...), c'est alors le jeu lui-même qui les donne, continues compris.
- **Jeux de combat.** Sur la dalle, les barres de vie, le chrono, les noms, et sur la ligne du bas la jauge de super de chaque joueur, bleue quand elle se remplit, dorée et clignotante quand elle est pleine. Sur l'écran HD, la scène de combat dans le décor du jeu, avec le lieu sous le bandeau du décor (CHINE, INDE, FEAST OF THE DAMNED...), et les jauges de super sous les combattants. Street Fighter II, sa Champion Edition et Hyper Fighting, Super Street Fighter II, Street Fighter Alpha et Night Warriors lisent les rounds gagnés par chaque joueur (base de triche), X-Men: Children of the Atom aussi (trouvé dans des captures faites sur une borne). Ce sont des étoiles dorées sous les barres sur l'écran HD et des carrés dorés à côté du chrono sur la dalle, et le vainqueur d'un round est celui dont le compte monte. Une barre de vie qui passe sous zéro au K.O. (0xFF dans son octet, Street Fighter II) se lit vide, elle se lisait pleine et le K.O. était raté. Les deux barres vidées d'un coup (l'écran de sélection après START, la fin d'une partie) ne sont pas un K.O. La jauge de super de Marvel vs. Capcom, Marvel Super Heroes, X-Men vs. Street Fighter et X-Men: Children of the Atom a des niveaux, comme dans le jeu. La barre est celle du niveau en cours (`power`), avec POWER et le niveau à côté (`power_level`, `"max"` pour le niveau le plus haut, où la barre s'affiche pleine avec POWER MAX). Dans Marvel vs. Capcom, Marvel Super Heroes vs. Street Fighter et X-Men vs. Street Fighter, chaque joueur a deux combattants qui se relaient. La vie et le nom affichés sont ceux du combattant à l'écran, faits par le moteur à partir des valeurs des deux (`"tag"` dans le fichier du jeu, une expression `"team"`), et l'équipe n'est K.O. que quand les deux sont à terre. Le joueur 2 est un humain ou l'ordinateur. Street Fighter Alpha, Alpha 3, Marvel vs. Capcom, Vampire Hunter 2 et JoJo's Bizarre Adventure le lisent dans le jeu (base de triche, `"human"` dans la rubrique `activity`), Marvel Super Heroes vs. Street Fighter, X-Men vs. Street Fighter et X-Men: Children of the Atom aussi (trouvé dans des captures faites sur une borne). Le joueur 1 est l'ordinateur quand le joueur 2 joue seul, lu dans ces jeux, vu dans les autres au START du joueur 2 suivi d'un crédit que le jeu dépense. Dans les autres jeux de combat, le joueur 2 est un humain dès que son score monte (une fois appris, mais pas dans les jeux Marvel où l'ordinateur marque aussi, `"cpu_scores"` dans la rubrique `activity`), qu'il appuie sur START avec un crédit, ou qu'un crédit est dépensé en plein combat (un challenger), jusqu'à ce que plus personne ne joue ou que son score n'ait pas bougé depuis deux minutes. Street Fighter II lit ses crédits et le score du joueur 1, appris avec `learn.bat` sur une borne sous RetroArch. Le score du joueur 2 est pris au même endroit dans son propre bloc et reste à confirmer. Un crédit dépensé est alors un départ, vu dès la sélection des personnages. Le combattant de Street Fighter III: New Generation est donné par deux octets, une ligne et une colonne de l'écran de sélection, et le fichier du jeu les réunit (`"join"`).
- **Les autres jeux.** Chacun a sa scène de dalle et sa scène HD à lui, voir Les jeux Capcom faits un par un juste en dessous.
- `demo_capcom.bat` lance la démo d'un jeu Capcom, la plupart avec l'écran des pièces d'abord.

| Jeu | Système | Fichier | Barres de vie | Chrono | Noms des persos | Jauge de super | Décors (HD) |
|---|---|---|---|---|---|---|---|
| Cyberbots: Fullmetal Madness | CPS2 | `cybots.json` | oui | oui | oui (10) | oui | oui |
| Darkstalkers: The Night Warriors | CPS2 | `dstlk.json` | oui | oui | oui (12) | - | oui |
| Hyper Street Fighter II: The Anniversary Edition | CPS2 | `hsf2.json` | oui | oui | oui (17) | oui | fixe |
| JoJo's Bizarre Adventure | CPS3 | `jojoba.json` | oui | oui | oui (25) | oui | fixe |
| JoJo's Venture | CPS3 | `jojo.json` | oui | oui | - | oui | fixe |
| Marvel Super Heroes | CPS2 | `msh.json` | oui | oui | oui (13) | oui | fixe |
| Marvel Super Heroes Vs. Street Fighter | CPS2 | `mshvsf.json` | oui | oui | oui (25) | oui | fixe |
| Marvel Vs. Capcom: Clash of Super Heroes | CPS2 | `mvsc.json` | oui | oui | oui (22) | oui | oui |
| Mega Man 2: The Power Fighters | CPS2 | `megaman2.json` | oui | - | - | - | fixe |
| Mega Man: The Power Battle | CPS1 | `megaman.json` | oui | - | - | - | fixe |
| Muscle Bomber Duo: Ultimate Team Battle | CPS1 | `mbombrd.json` | oui | - | - | - | fixe |
| Night Warriors: Darkstalkers' Revenge | CPS2 | `nwarr.json` | oui | oui | oui (14) | - | oui |
| Red Earth | CPS3 | `redearth.json` | oui | - | - | - | oui |
| Ring of Destruction: Slammasters II | CPS2 | `ringdest.json` | oui | oui | - | - | fixe |
| Saturday Night Slam Masters | CPS1 | `slammast.json` | oui | - | - | - | fixe |
| Street Fighter Alpha 2 | CPS2 | `sfa2.json` | oui | oui | oui (24) | oui | oui |
| Street Fighter Alpha 3 | CPS2 | `sfa3.json` | oui | oui | oui (29) | oui | oui |
| Street Fighter Alpha: Warriors' Dreams | CPS2 | `sfa.json` | oui | oui | oui (13) | oui | oui |
| Street Fighter II': Champion Edition | CPS1 | `sf2ce.json` | oui | oui | oui (12) | - | oui |
| Street Fighter II': Hyper Fighting | CPS1 | `sf2hf.json` | oui | oui | oui (12) | - | oui |
| Street Fighter II: The World Warrior | CPS1 | `sf2.json` | oui | oui | oui (12) | - | oui |
| Street Fighter III 2nd Impact: Giant Attack | CPS3 | `sfiii2.json` | oui | oui | oui (15) | oui | oui |
| Street Fighter III 3rd Strike: Fight for the Future | CPS3 | `sfiii3.json` | oui | oui | oui (19) | oui | oui |
| Street Fighter III: New Generation | CPS3 | `sfiii.json` | oui | oui | oui (11) | oui | oui |
| Street Fighter Zero | CPS1 | `sfzch.json` | - | - | - | - | fixe |
| Street Fighter Zero 2 Alpha | CPS2 | `sfz2al.json` | oui | oui | oui (21) | - | oui |
| Super Gem Fighter: Mini Mix | CPS2 | `sgemf.json` | oui | oui | oui (12) | oui | oui |
| Super Street Fighter II Turbo | CPS2 | `ssf2t.json` | oui | oui | oui (16) | oui | oui |
| Super Street Fighter II: The New Challengers | CPS2 | `ssf2.json` | oui | oui | oui (16) | - | oui |
| Vampire Hunter 2: Darkstalkers Revenge | CPS2 | `vhunt2.json` | oui | oui | oui (21) | oui | oui |
| Vampire Savior 2: The Lord of Vampire | CPS2 | `vsav2.json` | oui | oui | oui (19) | - | oui |
| Vampire Savior: The Lord of Vampire | CPS2 | `vsav.json` | oui | oui | oui (18) | - | oui |
| X-Men Vs. Street Fighter | CPS2 | `xmvsf.json` | oui | oui | oui (19) | oui | fixe |
| X-Men: Children of the Atom | CPS2 | `xmcota.json` | oui | oui | oui (13) | oui | oui |

Les adresses viennent de la base de codes de triche de FinalBurn Neo et doivent encore être confirmées en jeu (`test_retroarch.bat` les affiche). « fixe » veut dire que le jeu a toujours les mêmes décors, pris dans une liste qui lui va (le ring des Slam Masters, le laboratoire de Mega Man).

### Les jeux Capcom faits un par un

Comme les jeux Neo Geo, les autres jeux Capcom ont reçu une scène de dalle et une scène HD animée à leur image, cinquante en tout. Tout est dessiné par le programme, aucune image, aucun personnage ni aucun logo ne vient des jeux.

- **Les jeux à personnages, façon Metal Slug (1.30).** Les beat'em up, les jeux d'action et de plateformes, les deux Pang et Mercs ne montrent plus de personnages dessinés par le programme. Le décor du jeu reste derrière, calme et plus sombre. Chaque joueur a un panneau avec ce qui est lu dans le jeu (jauge, vies, score, bombes, arme, niveau), et le milieu montre le logo, TIME quand le chrono est lu en entier (en rouge quand il reste peu de temps) et les crédits. Les événements du jeu se voient entre les panneaux. Des points font un coup au milieu, un coup de poing, un tir, une entaille, une arme lancée, un sort ou un ballon qui éclate. Une bombe ou un coup spécial part du panneau et le milieu explose. Une vie perdue fait rougir le panneau et trembler l'écran, la vie qui remonte affiche + VIE, et un niveau gagné NIVEAU SUPÉRIEUR ! Le panneau du joueur 2 s'allume quand sa vie, ses vies ou son score bougent, et s'éteint 45 secondes après qu'ils ont cessé de bouger.
- **Shoot'em up.** Dès que le score est appris, un ennemi n'explose que quand le jeu marque des points, comme pour la Neo Geo. Une bombe dépensée balaie l'écran, l'arme ramassée et l'avion choisi sont nommés. Sur la dalle, l'avion, le vaisseau ou le soldat du jeu vole et tire. Le joueur 2 arrive quand son score monte, ou quand il perd une vie, lance une bombe ou prend un coup, et repart 45 secondes après qu'ils ont cessé de bouger. Les crédits s'affichent sous le logo. Mercs s'affiche en panneaux, comme les beat'em up.
- **Jeux d'action et de plateformes.** Dans leurs panneaux, l'arme tenue est lue dans Ghouls'n Ghosts et Three Wonders, l'armure dans Ghouls'n Ghosts, le compagnon et l'étage dans Magic Sword, le héros dans Willow, et les points de Pang! 3 et Mighty! Pang font éclater un ballon. Strider et Willow gardent un seul panneau, on y joue chacun son tour.
- **Jeux de réflexion, quiz et mahjong.** Ils jouent tout seuls, avec nos propres questions, tuiles, gemmes et bulles, et suivent ce qui est lu dans le jeu. Une vie perdue dans un quiz est une mauvaise réponse.
- **Les petits jeux** (Frog Feast, Pokonyan! Balloon, Magical Pumpkin, Ganbare! Marine Kun) jouent tout seuls aussi. Les grenouilles sautent, la montgolfière survole la savane, le carrosse citrouille traverse la ville, le viseur suit les poissons.
- Final Fight Anniversary Edition et Final Fight EX (hacks CPS2) prennent la scène de Final Fight, Tenchi wo Kurau II CPS Changer celle de Warriors of Fate.
- Les valeurs viennent des codes de triche de FinalBurn Neo et de MAME 2003-Plus et doivent encore être confirmées en jeu (`test_retroarch.bat` les affiche). Le score n'y est pas, apprends-le avec `learn.bat`, le titre du jeu prend sa place sur la dalle d'ici là. The King of Dragons compte son expérience, qui est lue.
- Quand personne ne joue, l'écran des pièces (voir Qui joue, juste au-dessus).
- `demo_capcom.bat` les montre sans jouer. Choisis le jeu dans la liste, ou donne-le directement, `demo_capcom.bat ffight` par exemple.

![Final Fight, Captain Commando, Cadillacs and Dinosaurs et The Punisher sur un marquee LCD, affichage HD](docs/images/hd_cps_beat_1.jpg)

![The King of Dragons, Knights of the Round, Warriors of Fate et Dungeons & Dragons: Shadow over Mystara sur un marquee LCD, affichage HD](docs/images/hd_cps_beat_2.jpg)

![Dungeons & Dragons: Tower of Doom, Alien vs. Predator, Armored Warriors et Battle Circuit sur un marquee LCD, affichage HD](docs/images/hd_cps_beat_3.jpg)

![1944, 19XX, 1941, Varth et U.N. Squadron sur un marquee LCD, affichage HD](docs/images/hd_cps_shooters_1.jpg)

![Carrier Air Wing, Forgotten Worlds, Giga Wing et Progear sur un marquee LCD, affichage HD](docs/images/hd_cps_shooters_2.jpg)

![Mars Matrix, Dimahoo, Eco Fighters et Mercs sur un marquee LCD, affichage HD](docs/images/hd_cps_shooters_3.jpg)

![Ghouls'n Ghosts, Strider, Pang! 3, Mighty! Pang et Super Puzzle Fighter II Turbo sur un marquee LCD, affichage HD](docs/images/hd_cps_action_1.jpg)

![Mega Twins, Magic Sword, Willow, Nemo et Three Wonders sur un marquee LCD, affichage HD](docs/images/hd_cps_action_2.jpg)

![Dynasty Wars, Puzz Loop 2, Capcom Sports Club, Quiz & Dragons et Adventure Quiz Capcom World 2 sur un marquee LCD, affichage HD](docs/images/hd_cps_action_3.jpg)

![Quiz Tonosama no Yabou 2, Quiz Nanairo Dreams, Jyangokushi, Janpai Puzzle Choukou et Gulun.Pa! sur un marquee LCD, affichage HD](docs/images/hd_cps_small_1.jpg)

![Pnickies, Frog Feast, Pokonyan! Balloon, Magical Pumpkin et Ganbare! Marine Kun sur un marquee LCD, affichage HD](docs/images/hd_cps_small_2.jpg)

| Jeu | Fichier | Dalle | Écran HD |
|---|---|---|---|
| Final Fight | `ffight.json` | la jauge jaune sur le rouge, TIME en violet, =vies, les immeubles de briques | panneaux sur le quartier de briques d'une grande ville américaine de jour. VIE jaune sur le rouge, les vies, le score, des coups de poing au milieu |
| Captain Commando | `captcomm.json` | la jauge verte, xvies, les façades de verre et leurs néons | panneaux sur une ville du futur de jour, ses façades de verre et leurs néons. Le nom du héros choisi dans le jeu, VIE en vert, les vies, le score, des coups de poing |
| Cadillacs and Dinosaurs | `dino.json` | la jauge jaune, =vies, les colonnes brisées et la vieille voiture | panneaux sur une ville avalée par la jungle, des volcans qui fument au loin. Le nom du héros choisi dans le jeu, VIE jaune sur le rouge, les vies, le score, des coups de poing |
| The Punisher | `punisher.json` | la jauge cyan, xvies, les grenades | panneaux sur le hall de la villa d'un mafieux la nuit. VIE en cyan, les vies, le score, les GRENADES, des tirs au milieu. Une grenade lancée (lue dans le jeu) part du panneau et le milieu explose |
| The King of Dragons | `kod.json` | la jauge verte, le niveau L, xvies, l'expérience EP comme score | panneaux sur une forêt de grands arbres au soleil. VIE en vert, les vies, l'expérience en score, NIVEAU, ÉPÉE et BOUCLIER qui montent (NIVEAU SUPÉRIEUR !, ÉPÉE +1 !), des entailles de lame au milieu |
| Knights of the Round | `knights.json` | la jauge rouge, le niveau L, xvies, les maisons à colombages | panneaux sur un village de maisons à colombages, le château au loin. VIE en rouge, les vies, le score, NIVEAU qui monte, des entailles de lame |
| Warriors of Fate | `wof.json` | la jauge jaune-vert, xvies, la palissade et ses bannières | panneaux sur une forêt de la Chine ancienne et la palissade d'un camp. VIE jaune-vert, les vies, le score, des entailles de lame |
| Dungeons & Dragons: Shadow over Mystara | `ddsom.json` | la jauge verte, les falaises de grès | panneaux sur un canyon de grès chaud, un château sombre au loin. VIE en vert, le score, des entailles de lame |
| Dungeons & Dragons: Tower of Doom | `ddtod.json` | la jauge verte, les collines dorées | panneaux sur des collines vertes dans la lumière dorée. VIE en vert, le score, les DAGUES du joueur 1, des entailles de lame. Une dague lancée (lue dans le jeu) part vers le milieu |
| Alien vs. Predator | `avsp.json` | la jauge jaune, la jauge du coup spécial, xvies | panneaux sur une ville industrielle en ruine au crépuscule dans une brume verte. Le nom du héros choisi dans le jeu, VIE en jaune, la jauge SPÉCIAL, les vies, le score, des tirs. Quand la jauge spéciale se vide (lu dans le jeu) le milieu explose |
| Armored Warriors | `armwar.json` | la jauge bleue, xvies, le hangar d'acier et ses bandes de danger | panneaux sur le hangar d'acier des machines de guerre. Le nom de la machine choisie dans le jeu, VIE en bleu, les vies, le score, des tirs |
| Battle Circuit | `batcir.json` | la jauge jaune, xvies, les gradins de l'arène | panneaux sur une arène du futur la nuit. VIE en jaune, les vies, le score, COIN et l'argent lu dans le jeu, des coups de poing |
| Final Fight Anniversary Edition, Final Fight EX (hacks CPS2) | `ffightaec2.json`, `ffex2u.json` | la dalle de Final Fight | la scène de Final Fight (rien de connu dans leur mémoire pour l'instant) |
| Tenchi wo Kurau II, CPS Changer | `wofch.json` | la dalle de Warriors of Fate | la scène de Warriors of Fate, avec ses valeurs (cheat.dat de MAME, mêmes adresses que Warriors of Fate) |
| 1944: The Loop Master | `1944.json` | le score ou le titre, la jauge d'énergie et les bombes, l'avion qui vole et tire, BOMBE!, POWER UP | le Pacifique bleu profond vu du ciel comme dans le jeu, d'énormes cuirassés au pont de bois et leur sillage, un atoll de temps en temps. Notre chasseur bipoutre argenté contre des chasseurs verts et des bombardiers, des navires en bas, ses chasseurs d'escorte à ses côtés. Une bombe dépensée est une salve de missiles qui nettoie le ciel, un grand WARNING annonce le boss. Le HUD dans l'esprit du jeu, 1P en rouge et le score, POW (l'énergie) en jaune, et en bas à gauche les bombes en médailles B, l'escorte en réserve dans son cadre avec son nombre, les cristaux d'or ramassés, 2P en rose. Lu avec MAME seulement, l'escorte et les cristaux restent à confirmer en jeu, le WARNING et le score à trouver avec des captures de la mémoire |
| 19XX: The War Against Destiny | `19xx.json` | le score ou le titre, les avions qui restent et les bombes, l'avion qui vole et tire, l'arme ramassée | haut dans le ciel au-dessus de la mer et de ses îles comme dans le jeu, des nuages blancs qui passent plus vite. L'avion choisi dans le jeu (le bipoutre, le canard ou le bimoteur), de gros bombardiers quadrimoteurs. 1P et le score, les avions qui restent, les bombes rondes en bas à gauche et le nom de l'avion |
| 1941: Counter Attack | `1941.json` | le score ou le titre, la jauge VITAL, l'avion qui vole et tire, l'arme ramassée | une mer bleu sombre entre deux côtes rocheuses enneigées comme dans le jeu. Notre chasseur bipoutre contre les chasseurs au nez rouge et les bombardiers, des navires en bas. 1PLAYER et le score, la jauge VITAL en sept segments, l'arme ramassée et son temps |
| Varth: Operation Thunderstorm | `varth.json` | le score ou le titre, les avions qui restent et les bombes, l'avion qui vole et tire, POWER UP, l'arme | une base militaire de plaques bleu-vert vue du ciel comme dans le jeu, des hangars et des aires rondes. Notre chasseur et ses deux modules de garde qui tournent autour, des chars sur les voies. SCORE et le score, les avions qui restent, les bombes, l'arme et les missiles des modules |
| U.N. Squadron | `unsquad.json` | le score ou le titre, le stock de l'arme spéciale, l'avion qui vole et tire, BOMBE! | notre chasseur au-dessus d'un canyon du désert comme dans le jeu, des mesas mauves, les tours d'une raffinerie, des chars sur le béton, les hélicoptères ennemis. Une arme spéciale tirée fait exploser l'écran. 1 PLAYER et le score, l'arme spéciale lue dans le jeu et son stock en bas |
| Carrier Air Wing | `cawing.json` | le score ou le titre, la jauge FUEL, l'avion qui vole et tire, POWER UP, l'arme | notre gros chasseur de l'aéronavale haut au-dessus d'une ville entière vue de biais comme dans le jeu, des nuages blancs qui passent, des chasseurs ennemis. 1PLAYER et le score, LEVEL et l'argent, WEAPON, ses munitions et la jauge FUEL en bas |
| Forgotten Worlds | `forgottn.json` | le score ou le titre, la jauge VITAL, le soldat qui vole et tire, l'arme | notre soldat volant et son module de tir qui tourne autour de lui au-dessus d'une ville morte comme dans le jeu, une énorme planète verte dans le ciel noir, des guerriers lézards dorés. Les zenny ramassés s'affichent, l'arme achetée à la boutique est nommée. 1P et le score, ZENNY, la jauge VITAL |
| Giga Wing | `gigawing.json` | le score ou le titre, les avions qui restent et les bombes, l'avion qui vole et tire, POWER UP | une vieille forteresse d'acier coupée de rivières de lave brûlante, vue du ciel comme dans le jeu, des chars sur les rails. Notre chasseur contre les canonnières, une bombe dépensée allume la barrière dorée et nettoie l'écran. 1P et le score, les avions et les bombes, le pilote choisi, REFLECT OK. Le score du joueur 1 et les crédits sont connus (appris sur une borne), les avions et les bombes du joueur 2 s'affichent quand il joue |
| Progear | `progear.json` | le score ou le titre, les avions qui restent et les bombes, l'avion qui vole et tire, POWER UP | notre chasseur de l'âge de la vapeur au-dessus d'une vieille ville européenne comme dans le jeu, des toits rouges et un grand aqueduc de pierre, les canonnières volantes à vapeur. P.1 et le score, les avions et les bombes, la jauge POWER en huit crans, l'avion choisi (Gambler ou Militant) |
| Mars Matrix | `mmatrix.json` | le score ou le titre, les vaisseaux qui restent, le vaisseau qui vole et tire, POWER UP | une base mécanique couleur rouille vue du ciel comme dans le jeu, des aires rondes, des tuyaux et des bandes jaunes et noires. Notre chasseur mécanique contre les drones de guerre orange. 1P et le score, les vaisseaux qui restent, LEVEL à droite |
| Dimahoo | `dimahoo.json` | le score ou le titre, les vies et les bombes magiques, la bête qui vole et tire | un ciel magique de nuages violets vu d'en haut comme dans le jeu, des rochers flottants. Notre magicien sur sa bête volante contre des petits dragons et de grosses bêtes-yeux, une bombe magique lance des anneaux de lumière. PLAYER 1 et le score, les vies, les bombes en étoiles, le héros choisi |
| Eco Fighters | `ecofghtr.json` | le score ou le titre, les vaisseaux qui restent, la capsule qui vole et tire, POWER UP, l'arme | notre petite capsule écologique et son bras-canon qui tourne au-dessus d'une mer bleu vif comme dans le jeu, des falaises ocre et leur cascade, des robots pollueurs dans leurs carapaces vertes. 1P-SCORE et le score, ARM-LV et les vaisseaux qui restent, l'arme du bras |
| Mercs | `mercs.json` | le score ou le titre, l'énergie, le temps, les méga attaques, le nom de l'arme ramassée, MISSION COMPLETE puis la mission suivante, notre mercenaire qui court et tire | panneaux sur une piste de sable à travers le désert. ÉNERGIE en vert, le score, les MÉGA ATTAQUE, TIME, des tirs. Une méga attaque de l'un ou l'autre joueur (lue dans le jeu) part de son panneau et le milieu explose. L'arme de chaque joueur est nommée à côté de son badge avec ses POW (FUSIL D'ASSAUT +2, LANCE-FLAMMES, FUSIL À POMPE, LANCE-GRENADES, les armes du bezel du jeu), son nom surgit quand il la ramasse et PUISSANCE +1 ! quand un POW la renforce. MISSION et son numéro sous le logo, MISSION 1 ACCOMPLIE ! au milieu quand la suivante commence |
| Ghouls'n Ghosts | `ghouls.json` | le score ou le titre, les vies | panneaux sur le lieu des exécutions sous l'orage. L'arme que le jeu dit que le chevalier tient (lance, dague, torche, épée, hache) et son armure (argent, or, ARMURE PERDUE !), les vies, le score. Chaque point lance l'arme vers le milieu |
| Strider | `strider.json` | le score ou le titre, les vies | un seul panneau sur la ville du premier niveau la nuit et ses dômes dorés (on joue chacun son tour). Les vies, le score, les ROBOTS D'APPUI, des entailles de lumière |
| Pang! 3 | `pang3.json` | le score ou le titre, les vies | panneaux sur le mur peint d'un temple en Égypte. Les vies, le score. De gros ballons rebondissent au milieu, les points lus dans le jeu en font éclater un qui se coupe en deux |
| Mighty! Pang | `mpang.json` | le score ou le titre, les vies, le temps | panneaux sur la plus haute montagne du monde sous la neige qui tombe. Les vies, le score, TIME, les ballons de Pang! 3 |
| Super Puzzle Fighter II Turbo | `spf2t.json` | le score ou le titre, les deux puits | la salle des combats, ses portes de papier éclairées et ses lanternes rouges, les deux puits de gemmes dans leurs cadres dorés. Des paires de gemmes à nous tombent, une gemme ronde fait éclater sa couleur et les gemmes à compteur volent vers l'autre puits. Aucun personnage n'est dessiné, les noms des personnages lus dans le jeu s'affichent au milieu. NEXT et SCORE |
| Mega Twins | `mtwins.json` | le score ou le titre, la jauge de vie, les vies | panneaux sur la forêt lumineuse du premier niveau. VITAL en bleu, les vies, le score, des entailles de lame |
| Magic Sword: Heroic Fantasy | `msword.json` | le score ou le titre, la jauge de vie, le temps | panneaux sur un étage de la tour, ses pierres grises et ses torches. VITAL, PUISSANCE qui brille quand elle est pleine, les CLÉS, le compagnon lu dans le jeu, ÉTAGE et son numéro, des entailles de lame |
| Willow | `willow.json` | le score ou le titre, la jauge de vie | un seul panneau sur le village du premier niveau, ses maisons à colombages et ses toits rouges (on joue chacun son tour). Le héros lu dans le jeu, VITAL, les vies, le score, des boules de magie |
| Nemo | `nemo.json` | le score ou le titre, les vies | panneaux sur le palais du pays des rêves, ses arches bleu pâle et sa lune. Les vies, le score, les ATTAQUES SPÉCIALES en grand, les étoiles de la baguette. Une attaque spéciale (lue dans le jeu) part du panneau et illumine le milieu |
| Three Wonders | `3wonders.json` | le score ou le titre, les vies | panneaux sur la forêt de Midnight Wanderers, ses falaises orange et ses champignons. Le tir que le jeu dit que l'elfe tient, les vies, le score. Chaque point le lance vers le milieu |
| Dynasty Wars | `dynwar.json` | le score ou le titre, la jauge de vie | panneaux sur le champ de bataille, ses falaises et ses pins. VIT, le score, NIVEAU qui monte, des coups de hallebarde |
| Puzz Loop 2 | `pzloop2.json` | le score ou le titre, les boules | le ciel de nuages violets et le chemin sculpté du jeu. Une chaîne de boules de couleur roule vers le trou, le lanceur au milieu y tire une boule, trois de la même couleur éclatent et la chaîne se resserre. BALLS et SCORE |
| Capcom Sports Club | `csclub.json` | le score ou le titre | le match de football du jeu dans un stade en fin d'après-midi, les tribunes pleines et les drapeaux sur le toit. Nos deux équipes se passent le ballon, tirent, le gardien plonge. Les drapeaux des deux équipes en haut, comme dans le jeu |
| Quiz & Dragons: Capcom Quiz Game | `qad.json` | le score ou le titre, les vies, la question et ses réponses | la salle du donjon et un dragon rouge à nous peint au mur, un chevalier et un magicien à nous, le panneau vert et ses quatre réponses. Le score qui monte donne un grand rond, une vie perdue une grande croix. Les questions sont à nous |
| Adventure Quiz Capcom World 2 | `cworld2j.json` | le score ou le titre, les vies, la question et ses réponses | le plateau de l'aventure, ses terres vertes, sa mer bleue et son chemin de cases, deux petits aventuriers à nous, le panneau bleu et ses quatre réponses. Les questions sont à nous |
| Quiz Tonosama no Yabou 2: Zenkoku-ban | `qtono2j.json` | le score ou le titre, les vies, la question et ses réponses | le château d'un seigneur de guerre sur un ciel rouge, ses flammes et ses bannières, un seigneur et un ninja à nous, le panneau des questions et ses quatre réponses. Les vies lues dans le jeu disent juste ou faux. Les questions sont à nous |
| Quiz Nanairo Dreams: Nijiirochou no Kiseki | `qndream.json` | le score ou le titre, les vies, la question et ses réponses | un parc de la ville au crépuscule, ses arbres, ses réverbères, sa fontaine et un arc-en-ciel pâle, une fille et un garçon à nous, le panneau des questions. Les questions sont à nous |
| Jyangokushi: Haoh no Saihai | `jyangoku.json` | le titre, les tuiles | le tapis vert dans son cadre laqué rouge, les tuiles aux dos bleus, une tuile piochée, une tuile jetée, et de temps en temps une main gagne avec RON ou TSUMO. Les points à droite |
| Janpai Puzzle Choukou | `choko.json` | le titre, les tuiles et la ligne dorée | les tuiles posées sur la soie rouge dans son cadre doré. Deux tuiles pareilles s'en vont quand une ligne d'au plus deux coudes les relie, la ligne dorée montre le chemin, les tuiles sont mélangées quand plus aucune paire ne va. PAIRES |
| Gulun.Pa! | `gulunpa.json` | le score ou le titre, deux puits de bulles | le ciel violet étoilé et ses planètes, deux puits entre des colonnes dorées. Des paires de petites bêtes rondes à nous tombent et éclatent quatre par quatre, les enchaînements brillent. NEXT à côté de chaque puits, 1P et 2P au milieu |
| Pnickies | `pnickj.json` | le score ou le titre, le puits, l'ange et le diablotin | le ciel pastel entre le paradis et le monde d'en bas, un ange à nous à gauche et un petit diablotin à droite, le puits dans son cadre rose. Les paires tombent et éclatent quatre par quatre. NEXT et le score à côté du puits |
| Frog Feast | `cps1frog.json` | le titre, la mare, les grenouilles et les mouches | la mare bleue entre deux grands sapins et ses deux nénuphars. Deux grenouilles à nous sautent de leur rive à leur nénuphar et attrapent les mouches avec leur langue. Le score de chacune sur son poteau de bois, TIME au milieu, TIME UP à la fin |
| Pokonyan! Balloon | `pokonyan.json` | le titre, la montgolfière et les ballons qui montent | la savane vue du ciel défile en dessous, zèbres et girafes marchent, notre montgolfière et son petit explorateur passent au-dessus. Les ballons de toutes les couleurs montent et éclatent quand la nacelle les touche |
| Magical Pumpkin: Puroland de Daibouken | `mpumpkin.json` | le titre, la ville et le carrosse citrouille | une ville de conte de fées aux maisons rondes pastel et son château rose défilent, notre carrosse citrouille roule sur la route en bonbon au bord de la rivière et ramasse les étoiles qui flottent devant lui |
| Ganbare! Marine Kun | `ganbare.json` | le titre, la mer, les poissons et le viseur | la pleine mer entre ses pitons rocheux, les poissons qui sautent hors de l'eau. Le viseur rouge les suit, se verrouille et touche, les médailles s'ajoutent en bas |

### Écran des pièces (jeux de combat)

Quand personne ne joue, les jeux de combat Neo Geo attendent une pièce, sur la dalle et sur l'écran HD. La pièce ne tombe que quand les crédits montent vraiment, il faut donc que les crédits soient connus. MAME les lit pour tous les jeux Neo Geo. Avec RetroArch, ArcadeDMD les devine d'après le BIOS (voir plus haut), et `coin_buttons.bat` lui fait voir chaque pièce (juste en dessous).

![Boutons START une fois les pièces mises, affichage HD](docs/images/hd_start_buttons.jpg)

- Sur la dalle, une pièce € flotte au-dessus d'une fente, à côté de INSERT COIN. Mets une pièce, elle tombe dans la fente, +1 monte et le compteur de crédits roule. Un instant après, PRESS START s'affiche avec un bouton rouge et les crédits en dessous. Le titre défile toujours en haut.
- Sur l'écran HD, le logo du jeu est entre deux monnayeurs, avec une pièce qui tourne au-dessus de chacun. Mets une pièce, l'une d'elles se met sur la tranche et tombe dans sa fente, avec des étincelles, +1 et le compteur qui roule. Puis les monnayeurs laissent la place aux boutons START 1P et 2P et à PRESS START.
- Tant qu'aucune pièce n'entre, rien ne tombe. Les combats de démonstration du jeu, derrière, ne déclenchent aucun effet sur l'écran HD.
- En haut de `config.json`, `"coin_symbol": "€"` est le symbole des pièces. `"$"` et `"£"` marchent aussi, et `""` donne une pièce sans symbole.
- Ta propre animation INSERT COIN pour la dalle (un GIF de la Pixelcade, par exemple) va dans `sprites\insert_coin.gif` (ou `.png`), en 128 x 32. Elle remplace l'écran des pièces tant qu'il n'y a pas de crédit, et la pièce tombe toujours quand tu en mets une.
- Dans la section `preview`, `"coins": false` remet le simple INSERT COIN sur l'écran HD.
- `demo_fight.bat` commence maintenant sur cet écran. Deux pièces entrent, START est appuyé, puis le combat commence. Dans un fichier de jeu, `"demo": {"attract": false}` passe directement au combat.

### Boutons des pièces (`coin_buttons.bat`)

RetroArch ne dit ni quand une pièce entre, ni par quel monnayeur. ArcadeDMD peut lire lui-même tes deux boutons de pièce et tes deux boutons START, sur les manettes ou le clavier, en même temps que RetroArch et sans les lui prendre. Il voit alors chaque pièce et son côté, même en pleine partie, et chaque joueur qui appuie sur START.

- Lance `coin_buttons.bat`. Appuie sur le bouton des pièces de gauche, puis sur celui de droite, puis sur START du joueur 1 et START du joueur 2. L'outil dit ce qu'il a vu (« manette 1, bouton 9 ») et l'écrit dans `config.json`, rubrique `coin_buttons` (`left`, `right`, `start1`, `start2`). Appuie encore sur ces boutons pour vérifier, il dit lequel c'est. Si ArcadeDMD tourne, il reprend ce réglage tout seul. Sans START appuyé, les boutons START déjà enregistrés restent.
- Sur l'écran HD, la pièce tombe dans le monnayeur du côté où tu l'as mise. Sans ce réglage, elle tombe dans celui du joueur 1 quand personne ne joue, dans celui de l'autre joueur pendant une partie (celui qui arrive), et dans celui du joueur au CONTINUE.
- Une MVS donne 2 crédits pour une pièce dans son deuxième monnayeur, tant que ses réglages n'ont pas été changés. ArcadeDMD compte pareil, 1 crédit à gauche et 2 à droite, et sur l'écran HD le monnayeur de droite affiche 2 CRÉDITS. Si tu changes ce réglage dans le menu de la MVS, mets la même chose dans la rubrique `coin_buttons` de `config.json`, par exemple `"mvs_credits": [1, 1]`.
- Quand le menu de RetroArch est ouvert, le bouton sert à s'y déplacer, et ArcadeDMD ne compte pas de pièce.
- Si tu branches tes manettes sur d'autres ports USB, relance `coin_buttons.bat`. Windows a pu changer leur numéro.
- Avec MAME, les crédits sont déjà lus dans le jeu. Le bouton donne alors seulement le côté de la pièce sur l'écran HD.
- Avec RetroArch, un jeu Capcom qui ne donne pas ses crédits les compte d'après ces boutons (Les jeux Capcom CPS1, CPS2 et CPS3, Crédits). Un joueur qui appuie sur START avec un crédit commence alors tout de suite, le jeu s'affiche dès l'écran de sélection ou l'intro au lieu de PRESS START. Le START du joueur 2 prend aussi son crédit, un challenger dans un jeu de combat compris. Un START appuyé sans crédit, en pleine partie ou dans le menu de RetroArch ne compte rien.
- Seulement sous Windows.

### Apprendre le score

1. Lance le jeu dans RetroArch et commence une partie. Joue jusqu'à avoir quelques points.
2. Lance `learn.bat`. Il voit que RetroArch tourne et passe en mode direct.
3. Tape le score affiché à l'écran, par exemple `score=20600`, puis Entrée. Le jeu est en pause tant que tu es dans cette fenêtre.
4. Retourne dans le jeu (Alt+Tab), marque d'autres points, reviens dans la fenêtre de `learn.bat` et tape le nouveau score.
5. Recommence trois ou quatre fois, avec un score différent à chaque fois. Entrée vide pour finir.
6. L'outil trouve l'adresse et l'écrit dans le fichier du jeu (`games\mslug3.json` par exemple, ou un nouveau fichier pour un jeu Neo Geo qui n'en a pas). Le score apparaît sur la dalle quelques secondes après, sans relancer le jeu.

Tape seulement les valeurs qui manquent. Les vies sont déjà connues, et les apprendre à partir du « 1UP » de l'écran donnerait une mauvaise adresse.

Pour le score du joueur 2, fais une partie à deux et tape les deux scores à chaque fois, par exemple `score=9400 score2=800`.

Dans Samurai Shodown et The Last Blade, les combattants changent de place dans la mémoire. Samurai Shodown II recrée chaque combattant ailleurs à chaque round. Il range le score dans le combattant et le recopie dans le nouveau. L'ancien garde un moment la dernière valeur, puis passe à 0. C'est ce qui trompait l'outil. Il préfère maintenant le score « dans le combattant » à une adresse fixe tombée dans la mémoire des combattants, et la dalle le suit de round en round. Fais tes captures sur deux rounds ou deux combats différents. L'outil le rappelle au début, et prévient si toutes les captures viennent du même round. Si une ancienne adresse ne marche plus, refais simplement l'apprentissage. La nouvelle remplace l'ancienne dans `games\` et dans `learned\`.

Lancé quand RetroArch est fermé, `learn.bat` réanalyse les dernières captures du jeu avec les valeurs déjà tapées, sans rien redemander.

Noms reconnus `score`, `score2` (ou `score_p2`), `crédits` (ou `credits`), `vies`, `vies2`, `bombes`, `munitions`. Pour un autre jeu, l'outil crée un fichier dans `games\` avec la scène générique.

Ce que l'outil trouve est aussi copié dans `learned\`. Une nouvelle version d'ArcadeDMD remplace les fichiers de `games\`, mais le moteur remet tout seul les adresses apprises au démarrage. Pour oublier ce qui a été appris pour un jeu, supprime son fichier dans `learned\`. Une adresse que le fichier du jeu écarte (`not_learned`, là où le jeu garde autre chose que l'outil prend pour la valeur) est retirée toute seule de `learned\`, et l'outil la laisse de côté. Dans Metal Slug, la place que l'outil trouvait garde le score du dernier joueur qui a marqué.

### Bon à savoir

- Un jeu RetroArch sans fichier dans `games\` ne change rien sur la Pixelcade (sauf avec `"takeover": "all"`).
- Dans `config.json`, rubrique `retroarch`, `"enabled": false` coupe la surveillance.
- Si le journal dit « RetroArch refuse de lire la mémoire du jeu », c'est le cœur qui ne la donne pas. Le journal dit lequel est chargé et quoi faire.

---

## 8. Ajouter un jeu ou modifier une scène

1. Copie `games\aburner2.json` sous le nom court du jeu, par exemple `games\outrun.json`.
2. Change `"match"` (`"system": ["outrun"]`), le titre et les valeurs.
3. Trouve les adresses avec `learn.bat` (sans fichier dédié, l'outil crée le fichier pour toi).
4. Modifie la scène. Le moteur recharge les fichiers à chaud, pas besoin de relancer pendant que tu ajustes.

Formats de valeurs reconnus

| `type` | Signification |
|---|---|
| `u8` | un octet |
| `be` / `le` | binaire sur `bytes` octets, ordre normal ou inversé |
| `bcd` / `bcd_le` | BCD sur `bytes` octets (deux chiffres par octet) |
| `digits` | un chiffre par octet (`digit_offset` 0x30 pour de l'ASCII) |

Options communes, `mult` (score stocké divisé par 10, très fréquent), `add`, `min`, `max`, `mask`, `shift`. `learn_ranges` limite la zone capturée par l'outil d'apprentissage. `hold_zero` (en secondes) garde le dernier score affiché quand la valeur lue tombe à 0 un instant en pleine partie, le temps que le jeu recrée le combattant entre deux rounds.

Pour une valeur rangée dans un objet qui change de place en mémoire (les combattants de Samurai Shodown à chaque round), `"ptr"` donne l'adresse où lire la position de l'objet (32 bits) et `"addr"` devient le décalage dans l'objet. `"ptr_range"` écarte un pointeur pas encore prêt. `learn.bat` écrit ce genre de valeur tout seul quand les captures montrent que la valeur suit l'objet.

Certains noms de valeurs ont un rôle particulier dans les scènes HD. `stage`, `backdrop` et `mission` changent le décor (section 3), `p1_input` et `p2_input` sont le stick et les boutons lus par le BIOS Neo Geo (tirs au pistolet des Metal Slug, vaisseaux de Blazing Star, de Pulstar et de Last Resort, avions des Aero Fighters, chasseurs de Top Hunter, flèche de Puzzle Bobble, fou de Magical Drop III).

`"derived"` calcule une valeur à partir d'autres, par exemple le nom du personnage. `"value"` reprend une valeur lue, `"pick"` choisit dans une liste selon `"at"`, `"names"` change un numéro en texte. `"names"` peut aussi avoir une liste par langue, `{"en": [...], "fr": [...]}`, comme dans `games\wjammers.json`. Voir `games\samsho2.json` et `games\kof98.json`.

Éléments de scène

| `type` | Rôle | Réglages principaux |
|---|---|---|
| `marquee` | texte qui défile | `text` ou `segments` (morceaux de couleurs différentes), `font`, `y`, `speed`, `gap`, `color`, `accent_initials` |
| `text` | texte fixe ou valeur | `text` avec `{score}`, `x`, `y`, `align`, `segments`, `flash` |
| `cycle` | alterne plusieurs pages | `period`, `pages` |
| `bars` | herbe ou égaliseur | `x`, `w`, `min`, `max`, `color`, `tip`, `flowers` |
| `waves` | collines qui défilent en fond | `layers` (`y`, `amp`, `speed`, `color`, `edge`) |
| `mountains` | montagnes pleines et ligne de sol (style Vera) | `peaks` (`[x, hauteur]`), `floor`, `color`, `ground`, `speed` |
| `particles` | missiles et gerbes quand une valeur monte | `rate`, `color`, `y`, `burst` |
| `anim` | une animation jouée une fois quand une valeur change (une explosion quand le score monte) | `image` (liste, le premier fichier trouvé, `{game}` pour le jeu), `on`, `change` (`up`, `down`, `any`), `ratio` (petit ou gros gain), `x` et `y` (un nombre, `[début, fin]`, ou plusieurs `[début, fin]` au choix), `near` et `ahead` (devant un `ship`), `count`, `spread`, `delay`, `ms`, `black` |
| `events` | des événements courts qui prennent la dalle un instant, un à la fois, comme sur un flipper (BOMBE!, POWER UP, une vie perdue, GAME OVER) | `events`, une liste. Chacun a `on`, `change`, `step` (la taille du changement), `from` et `to` (les valeurs avant et après), `when`, `text` (avec `{lives}`...), `color`, `font` (sa plus grande taille, il grandit jusqu'à elle), `y`, `icon` et `colors` (un petit dessin à gauche du texte), `icon_scale`, `anim` (des animations jouées au départ, mêmes clés que `anim`), `text_delay`, `ms`, `clear` (`false` garde la scène derrière), `priority` (un événement plus important remplace celui en cours, un moins important attend) |
| `sprite` | sprite animé (PNG en bande ou GIF) | `image`, `frames`, `mode` (`pass`, `pingpong`, `fixed`), `dim` (luminosité), `alpha`, `shoot` (tire quand une valeur monte) |
| `gauge` | barre de vie | `var`, `max`, `x`, `y`, `w`, `h`, `anchor` (côté accroché), `color`, `low`, `back`, `border`, `bevel` (liseré clair en bas et à droite) |
| `clock` | horloge | `format`, `font` |
| `icons` | un petit dessin répété selon une valeur (vies en vaisseaux, niveaux de puissance) | `var`, `pattern` (lignes de caractères, `.` pour le vide), `colors`, `max`, `gap`, `empty` (couleur des cases restantes), `align`, `flash` |
| `counter` | un petit dessin suivi d'un nombre (un avion et x3 pour les vies) | `var`, `pattern`, `colors`, `font`, `color` (du nombre), `prefix` (`x`), `align` (`left` à partir de `x`, `right` jusqu'à `x`), `max` (au-dessus rien ne s'affiche, une valeur que le jeu n'a pas encore posée), `flash` |
| `ship` | le vaisseau du joueur, qui suit le stick et tire tant que le bouton A est tenu (`p1_input`), ou vole tout seul | `image` (liste, `{game}` pour le jeu), `frames`, `fps`, `face` (`right`, ou `left` pour le joueur 2 face au joueur 1), `area` (`[x0, y0, x1, y1]`), `input`, `speed`, `fire` (`color`, `speed`, `rate`, `len`), `shoot_on` (tire quand le score monte), `anchor` (pour qu'une couche `anim` avec `near` parte devant lui), `hit` et `unless` (un ennemi explose de temps en temps tant que le score n'est pas connu) |
| `dot` | un disque dont la couleur vient d'une valeur (bulles de Puzzle Bobble), ou toujours la première couleur sans `var` (une lune) | `var`, `colors` (une couleur par valeur), `x`, `y`, `r`, `rim`, `shine` |
| `arrow` | une flèche qui tourne selon une valeur (vent de Neo Turf Masters) | `var`, `steps` (16, 0 vers le haut puis dans le sens des aiguilles d'une montre), `x`, `y`, `len`, `color`, `ring`, `flash` |
| `image`, `rect` | image fixe, rectangle | |

Polices disponibles `4x6`, `5x8`, `6x10`, `6x13`, `7x14`, `7x14B`, `8x13B`, `9x15B`. Le `y` d'un texte correspond au haut des majuscules. `when` affiche un élément sous condition, par exemple `{"has": "credits"}` ou `{"var": "mode", "eq": 12}`.

La section `"demo"` donne les valeurs de départ des démos (`demo_neogeo.bat`, `python arcadedmd.py demo <jeu>`). `"attract": true` commence sur l'écran des pièces, puis deux pièces et START. `"sim"` fait bouger les valeurs propres au jeu, une entrée par valeur, avec `"cycle"` (une liste prise à tour de rôle), `"count"` (`[min, max, pas]`, retour au début à la fin) ou `"random"` (`[min, max]`), `"every"` (secondes, ou `[min, max]`) et `"start"` (premier changement). Voir `games\wjammers.json`.

---

## 9. Passerelle DOFLinx (facultatif)

ArcadeDMD sait se faire passer pour DOF2DMD. DOFLinx lui envoie alors le score et les crédits de tous les jeux qu'il connaît, sans aucune adresse à chercher.

1. Dans `config.json`, mets `"enabled": true` dans la section `doflinx_bridge`. Elle écoute sur le port 8081, pour laisser le 8080 à pixelweb.
2. DOFLinx lit l'adresse dans le `settings.ini` de DOF2DMD (`url_prefix`). Mets `http://127.0.0.1:8081`.
3. Ne lance plus DOF2DMD en même temps, les deux ne peuvent pas écouter le même port. Quand ArcadeDMD répond, DOFLinx ne cherche plus à démarrer DOF2DMD.

Les deux sources se complètent. Pour After Burner II, le record vient du plugin et le score de DOFLinx.


---

## 10. Dépannage

- **RetroArch, rien ne change sur la Pixelcade.** Vérifie que les « Commandes réseau » sont actives dans RetroArch et que le journal dit « RetroArch détecté ». Le jeu doit avoir son fichier dans `games\`.
- **RetroArch, la scène s'affiche mais sans valeurs.** Le cœur ne donne sûrement pas sa mémoire (FB Alpha 2012 par exemple). Lance `test_retroarch.bat` pendant la partie, il dit quel cœur tourne et lequel prendre (voir « Le bon cœur », section 7).
- **« Python est introuvable ».** Le raccourci `python` du Microsoft Store ne compte pas, il ne lance rien. Relance `install.bat`, il propose d'installer Python 3.13. Les fichiers .bat trouvent aussi un Python installé sans être dans le PATH.
- **ArcadeDMD n'apparaît pas dans le menu Tab de MAME.** MAME est peut-être trop ancien (il faut 0.227 ou plus récent, `install.bat` affiche la version). Sinon le plugin est désactivé, voir « Vérifier le plugin dans MAME ».
- **Rien ne s'affiche pendant un jeu.** Regarde `runtime\arcadedmd.log` et vérifie que `runtime\events.jsonl` grossit pendant la partie. Sinon, le chemin `root` du fichier `MAME\plugins\arcadedmd\settings.json` ne pointe pas vers le dossier ArcadeDMD.
- **« ZeDMD : dalle non trouvée ».** Vérifie le câble (data), le port USB natif de l'ESP32-S3, et qu'aucun autre logiciel n'utilise la dalle (DOF2DMD, VPX, dmdext, ou le moteur ArcadeDMD déjà lancé en arrière-plan). La recherche automatique s'arrête après trois essais. Une fois la dalle trouvée, son port est mémorisé et seul ce port est réessayé.
- **Pistolets RetroShooter ou autres appareils série.** La recherche d'une dalle ZeDMD interroge les ports COM (jamais celui de la Pixelcade, et pas du tout si la sortie ZeDMD est coupée). Pour ne jamais toucher aux pistolets, indique le port de la dalle dans `config.json` (`"device": "COM5"`) ou exclus ceux des pistolets (`"ignore_devices": ["COM3", "COM4"]`).
- **Dalle noire après une mise en veille ou un débranchement.** Relance ArcadeDMD, libzedmd ne se reconnecte pas toute seule.
- **Couleurs inversées, lignes fantômes.** Ordre RGB et « panel driver » dans le menu ZeDMD (ou avec ZeDMD_Updater2).
- **Animation saccadée sur la dalle.** Monte « USB packet size » et « min refresh » dans le menu ZeDMD.
- **Pas de fenêtre LED virtuelles.** pygame-ce doit être installé (`py -m pip install pygame-ce`).
- **`test_panel.bat` dit que le moteur tourne déjà.** Le lancement automatique occupe la dalle. Ferme `pythonw.exe` dans le Gestionnaire des tâches, ou teste directement avec un jeu.
- **Le moteur s'arrête tout seul.** L'erreur est notée dans `runtime\arcadedmd.log`.
- **« Pixelcade : port introuvable ».** Indique le port dans `config.json` (`ports.bat` pour le trouver). ArcadeDMD ne sonde pas les autres ports COM, pour ne pas déranger les pistolets.
- **« pixelweb ne s'arrête pas ».** Ferme pixelweb à la main (icône dans la barre des tâches) et vérifie `pixelweb_url` (par défaut `http://127.0.0.1:8080`).
- **pixelweb ne revient pas après un jeu.** Le chemin est mémorisé dans `runtime\pixelweb_path.txt` au premier arrêt. Sinon, renseigne `pixelweb_exe` dans `config.json`.
- **Pixelcade noire pendant un jeu.** Regarde le journal. Si pixelweb a bien été arrêté mais que la carte ne répond pas, débranche et rebranche la Pixelcade, puis relance `test_pixelcade.bat`.

---

## 11. Fichiers texte pour OBS

ArcadeDMD écrit les valeurs du jeu en cours dans le dossier `obs\`, un fichier par valeur. Chaque fichier change dès que la valeur change, et se vide hors jeu. Ça marche avec MAME, Arcade64 et RetroArch.

| Fichier | Contenu |
|---|---|
| `game.txt` | titre du jeu |
| `score_p1.txt`, `score_p2.txt` | score de chaque joueur |
| `credits.txt` | crédits (MAME et Arcade64) |
| `fighter_p1.txt`, `fighter_p2.txt` | personnage en train de se battre, quand il est connu |
| `streak_p1.txt`, `streak_p2.txt` | victoires d'affilée en match VS (King of Fighters, une fois appris) |
| `vs_p1.txt`, `vs_p2.txt` | « BEAT BY 02 » ou « CHALLENGER », comme en haut de l'écran du jeu |
| `best_streak.txt` | meilleure série du jeu en cours, par exemple « BEAT BY 05 \| P2 RUGAL \| 26/10/2026 » |
| `vs_history.txt` | une ligne par match VS gagné, avec la date, le jeu, le gagnant et sa série |
| `records.json` | la meilleure série de chaque jeu, gardée d'une partie à l'autre |

Dans OBS, ajoute une source Texte (GDI+), coche « Read from file » (lire depuis un fichier) et choisis le fichier. Les textes sont les mêmes dans toutes les langues. « P2 RUGAL > P1 KIM » veut dire que P2 a battu P1.

Pour couper, mets `"enabled": false` dans la section `textfiles` de `config.json`. `"folder"` choisit un autre dossier, `"history": false` coupe l'historique.

## Licences et crédits

ArcadeDMD © 2026 Byoyoyo, sous licence MIT (fichier `LICENSE`). Tu peux l'utiliser, le modifier et le partager, à condition de garder la mention de copyright et la licence avec. Polices bitmap issues des polices X11 « misc-fixed » (domaine public). Les polices HD sont Inter (The Inter Project Authors) et Black Ops One (The Black-Ops Project Authors), toutes deux sous licence SIL Open Font License, voir le dossier `fonts`. Les sprites, les décors HD et les effets sont dessinés par le programme ou pour lui, aucune image ne vient d'un jeu. ZeDMD (firmware GPLv2) et libzedmd (GPLv3) sont téléchargés séparément depuis leurs dépôts officiels https://github.com/PPUC. Les noms de jeux servent uniquement à les identifier. Les adresses viennent des bases de triche de la communauté (FinalBurn Neo, MAME 2003-Plus), des scripts d'entraînement de peon2 et des désassemblages de Sonic, merci à leurs auteurs.

Byoyoyo voulait créer ArcadeDMD depuis longtemps, et l'a lancé après ses échanges avec Vera AI. Merci à Vera AI pour ces échanges.
