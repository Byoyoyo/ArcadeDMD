# ArcadeDMD

Score, vies et crédits des jeux MAME en direct sur une dalle LED 128x32 posée sur la borne, avec une scène animée propre à chaque jeu. Même principe que les vidéos After Burner II et Sonic.

Comment ça marche, en une phrase. Un plugin MAME lit les valeurs dans la RAM du jeu, un petit programme Python dessine la scène et l'envoie à la dalle, une **Pixelcade LED** ou un **ZeDMD**, en USB. Le même programme peut aussi afficher la scène en « LED virtuelles » sur un écran LCD qui sert de DMD (section 3).

Tu as déjà une Pixelcade LED. Elle suffit, pas besoin d'acheter de dalle. Va directement aux sections 2 et 4. Pour les jeux lancés dans RetroArch (Metal Slug, Sonic...), lis aussi la section 7.

Contenu du dossier

| Fichier | Rôle |
|---|---|
| `installer.bat` | installe tout (Python requis, voir plus bas) |
| `demo_afterburner.bat`, `demo_sonic.bat` | montrent les scènes avec des valeurs simulées, sans MAME |
| `lancer.bat` | démarre le moteur avec la console visible |
| `apprendre.bat` | outil qui trouve une adresse RAM manquante (score, crédits...) |
| `test_pixelcade.bat` | mire de test sur la Pixelcade LED |
| `ecran_dmd.bat` | place la scène sur un écran LCD qui sert de DMD (section 3) |
| `test_retroarch.bat` | vérifie RetroArch, le cœur chargé et la lecture de la mémoire (section 7) |
| `ports.bat` | liste les ports COM, pour trouver celui de la Pixelcade |
| `test_dalle.bat` | mire de test sur une dalle ZeDMD |
| `config.json` | tes réglages (Pixelcade, RetroArch, fenêtre LED virtuelles...), créé par l'installeur à partir de `config.defaut.json`. Une nouvelle version d'ArcadeDMD ne l'écrase jamais |
| `games\*.json` | un fichier par jeu, avec les adresses RAM et la scène. Les fichiers `neogeo*.json` servent de scènes communes aux jeux Neo Geo, une par genre |
| `appris\` | copie des adresses trouvées par `apprendre.bat`. Remises en place toutes seules après une mise à jour |
| `mame-plugin\arcadedmd` | le plugin à copier dans `MAME\plugins` (l'installeur le fait) |
| `sprites\` | petits sprites (avion, anneau). Tu peux ajouter les tiens |

---

## 1. Le matériel (seulement si tu n'as pas de Pixelcade)

La dalle de la vidéo est un DMD RGB 128x32, c'est-à-dire deux modules LED HUB75 de 64x32 côte à côte. C'est exactement le format ZeDMD, le DMD libre bien connu du monde du flipper virtuel. On s'appuie dessus pour la partie dalle.

### Option A, le plus simple (pack prêt à brancher)

Des boutiques françaises vendent des ZeDMD montés ou des cartes prêtes à l'emploi.
- SmallCab, « Pack ZeDMD S3 – P2.5 » https://www.smallcab.net/pack-zedmd-p-3182.html
- Benfactory, « ZeDMD » https://benfactory.fr/produit/zedmd/

En P2.5 (2,5 mm entre deux LED) la dalle fait environ 32 × 8 cm. C'est la taille d'un DMD de flipper. Vérifie sur la page ce qui est inclus (alimentation, cadre).

### Option B, la même taille que dans la vidéo

La dalle des vidéos est plus grande, sans doute du P4 ou du P5. Mesure le dessus de ta borne et choisis.

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

---

## 2. Le logiciel

### Installation

1. Il faut Python 3.12 ou plus récent. S'il manque, `installer.bat` propose de l'installer (Python 3.13, depuis python.org). Sinon installe-le depuis https://www.python.org/downloads/ en cochant « Add python.exe to PATH ». Il faut aussi MAME 0.227 ou plus récent, l'installeur affiche ta version.
2. Avant d'extraire le zip, fais un clic droit dessus, Propriétés, coche « Débloquer » puis OK. Windows ne posera plus de question à chaque fichier .bat.
3. Extrais le dossier `ArcadeDMD` dans un chemin sans accent, idéalement `C:\ArcadeDMD`. MAME ne sait pas ouvrir les dossiers avec accents.
4. Lance `installer.bat`. Il installe Pillow, pyserial et pygame-ce, copie le plugin dans MAME, règle la Pixelcade et propose le lancement automatique au démarrage de Windows. Il ne télécharge libzedmd (le pilote des dalles ZeDMD) que si tu dis avoir une dalle ZeDMD. Si tu n'utilises que RetroArch, appuie sur Entrée à la question sur MAME.

### Ce que l'installation modifie

- Le dossier `C:\ArcadeDMD`. Les réglages, le journal et les captures restent dedans.
- Dans MAME, un nouveau dossier `plugins\arcadedmd` avec trois petits fichiers. Rien d'autre dans MAME. `mame.ini` et `plugin.ini` ne sont pas modifiés, MAME charge tout seul les plugins de son dossier `plugins`.
- Un fichier `ArcadeDMD.bat` dans le dossier Démarrage de Windows, seulement si tu acceptes le lancement automatique.
- Trois bibliothèques ajoutées à Python (Pillow, pyserial, pygame-ce).
- Pendant les jeux qui ont un fichier dans `games\` (After Burner II, Sonic 1 et 2), ArcadeDMD arrête pixelweb et le relance à la fin de la partie. Pour les autres jeux, rien ne change.

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

Lance `lancer.bat` (ou laisse le démarrage automatique faire), puis lance un jeu depuis ton frontend ou directement dans MAME. La Pixelcade passe à ArcadeDMD pendant les jeux qui ont leur fichier dans `games\` et reste à pixelweb le reste du temps. Une dalle ZeDMD, elle, affiche l'heure et « INSERT COIN » hors jeu, et le titre qui défile pour un jeu sans fichier dédié.

---

## 3. Écran LCD ou marquee en « LED virtuelles »

ArcadeDMD dessine la scène sur n'importe quel écran branché en plus, par exemple le LCD d'une borne qui sert de DMD, ou un marquee 1920×470. Ça marche avec RetroArch comme avec MAME.

Le plus simple, lance `ecran_dmd.bat` (l'installeur le propose aussi). Il liste les écrans, devine celui qui sert de DMD (le plus allongé) et règle tout dans `config.json`. Lance ensuite `lancer.bat` ou `demo_afterburner.bat` pour voir le résultat.

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
- `"mode": "games"` (réglage par défaut) fait comme avec la Pixelcade. Hors jeu, la fenêtre se cache et l'écran reste au frontal, par exemple aux clear logos et marquees de BigBox. Dès qu'un jeu connu démarre, ArcadeDMD passe au premier plan, au-dessus du marquee de BigBox ou d'HyperSpin, sans prendre le focus du jeu. Si le frontal repasse devant pendant la partie, ArcadeDMD revient devant dans la seconde. À la fin de la partie, l'écran est rendu au frontal deux secondes après. `"mode": "always"` garde la fenêtre affichée tout le temps, avec l'écran d'attente hors jeu.
- `"takeover": "known"` passe au premier plan seulement pour les jeux qui ont un fichier dans `games\` (Metal Slug, King of Fighters, tous les Neo Geo...). `"all"` le fait pour tous les jeux MAME, avec la scène générique.
- `"topmost": true` garde la fenêtre au-dessus des autres pendant qu'elle est affichée. Mets `"enabled": false` si tu ne veux que la vraie dalle.

---

## 4. Pixelcade LED

La Pixelcade LED est elle-même une dalle 128x32. ArcadeDMD la pilote directement par son port USB, avec le même protocole que Visual Pinball (dmdext, libdmdutil). Les cartes V1 et V2 sont reconnues toutes seules.

Le logiciel Pixelcade (pixelweb) ne peut pas partager la dalle. ArcadeDMD fait donc ce que Pixelcade recommande pour Visual Pinball. Au lancement d'un jeu qui a son fichier dans `games\`, il arrête pixelweb par son API (`/quit`) et prend la dalle. Quand tu quittes le jeu, il la rend et relance pixelweb. Pour tous les autres jeux, pixelweb continue d'afficher ses marquees comme avant.

### Réglage

`installer.bat` pose la question à l'étape 4 et règle le port tout seul. La sortie ZeDMD reste coupée si tu as répondu non à sa question, ArcadeDMD ne sonde alors aucun autre port série (pistolets par exemple). Pour le faire à la main :

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
| `"mode": "always"` | garde la dalle en permanence (si tu n'utilises plus pixelweb), avec l'écran d'attente hors jeu |
| `"pixelweb_exe"` | chemin de pixelweb.exe, trouvé tout seul d'habitude. S'il a besoin d'options, mets ici un .bat qui le lance avec |
| `"art_dir"` | dossier Pixelcade, pour reprendre ses marquees en fond de la scène générique (trouvé tout seul d'habitude) |

Les cartes V1 affichent 3 bits par couleur en mode direct, c'est une limite du matériel. Les cartes V2 affichent toutes les couleurs.

Pour un jeu avec fichier mais sans scène dédiée (un jeu appris avec `apprendre.bat` par exemple), la scène générique reprend le marquee Pixelcade du jeu en fond, atténué, avec le score et les crédits par-dessus.

---

## 5. After Burner II, trouver le score et les crédits

Le record est connu publiquement (table des records à `0xFF846E`, la même que `hiscore.dat`). L'adresse du score et celle des crédits ne sont documentées nulle part, d'où l'outil d'apprentissage. Compte cinq minutes.

1. Lance After Burner II.
2. Mets une pièce, attends un peu, mets-en une deuxième. Les crédits changent.
3. Joue. Quand le score est stable (pas pendant un décompte de bonus), appuie sur **Ctrl droit + D**. Un message « capture enregistrée » s'affiche. Tu peux aussi passer par Tab, Options des plugins, ArcadeDMD, « Capturer la RAM ».
4. Refais une capture à trois ou quatre moments avec des scores et des crédits différents.
5. Quitte MAME et lance `apprendre.bat`. Pour chaque capture, l'outil ouvre la photo d'écran et te demande les valeurs, par exemple `score=16060 credits=3`.
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

Rien d'autre à installer. Dès que le moteur tourne (`lancer.bat` ou le lancement automatique), il surveille RetroArch tout seul. Le journal indique « RetroArch détecté » quand les commandes réseau répondent, puis le cœur chargé à chaque jeu.

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
| Metal Slug (`mslug`) | FinalBurn Neo | score, vies, bombes, arme et munitions | rien |
| Metal Slug 2 (`mslug2`), Metal Slug X (`mslugx`) | FinalBurn Neo | vies, bombes, arme et munitions | score |
| Metal Slug 3 (`mslug3`) | FinalBurn Neo | score, vies, bombes, arme et munitions | score J2 |
| Metal Slug 4 (`mslug4`), Metal Slug 5 (`mslug5`) | FinalBurn Neo | vies, bombes, arme et munitions | score |
| Les 57 jeux de combat Neo Geo (King of Fighters, Samurai Shodown, Fatal Fury, Last Blade, World Heroes...) | FinalBurn Neo | voir le tableau Jeux de combat juste en dessous | le score, sauf KOF 96 à 2002 |
| Tous les autres jeux Neo Geo | FinalBurn Neo | scène selon le genre (crédits avec MAME) | score, crédits si le jeu en garde une copie |
| Sonic 1 et Sonic 2 | Genesis Plus GX | score, anneaux, vies | rien |

Les adresses des vies, bombes et munitions viennent de la base de codes de triche de MAME 2003-Plus. Celles de Sonic sont les mêmes que dans MAME. Les vies des Metal Slug suivent le « 1UP » de l'écran. Metal Slug 1 compte aussi la vie en cours, ArcadeDMD enlève donc 1 (vérifié). Metal Slug 3 ne la compte pas (vérifié). Pour 2 et X, ArcadeDMD fait comme pour le 1, et pour 4 et 5 comme pour le 3. Si un de ces jeux affiche une vie de moins que l'écran, enlève les lignes `"add"` et `"min"` de ses vies dans son fichier `games\mslugX.json`. S'il en affiche une de plus, ajoute `"add": -1, "min": 0`.

À deux joueurs, la scène change toute seule dès que le joueur 2 appuie sur Start. Le BIOS de la Neo Geo indique qui est en jeu. En haut, comme dans le jeu, « 1UP= » et les vies du joueur 1 à gauche, « 2UP= » et celles du joueur 2 à droite, avec le titre qui défile entre les deux. Dessous, chaque score sous son 1UP ou son 2UP. « SCORE ? » en gris veut dire que ce score n'est pas encore appris. En bas, les bombes puis l'arme de chaque joueur passent à tour de rôle, avec « P1 » en vert et « P2 » en jaune. Si seul le joueur 2 joue, la scène normale s'affiche avec ses valeurs à lui. Les crédits des Neo Geo ne se lisent qu'avec MAME (voir Tous les jeux Neo Geo).

Les scènes des Metal Slug s'inspirent de la vidéo de Vera, adaptées à une dalle 128x32 pour que rien ne passe sous le décor. En haut, « SNK » en bleu puis « - METAL SLUG » (avec le numéro du jeu) en blanc défilent lentement. Dessous, « P1 » en vert et le score en blanc à gauche, les vies à droite. La ligne suivante alterne les bombes, l'arme avec ses munitions (pistolet, mitraillette, fusil à pompe, lance-flammes, lance-roquettes, laser, tête chercheuse... un « + » indique la version améliorée) et les crédits avec MAME. Tout en bas, des petites collines et un petit char moins lumineux qui avance et tire quand le score monte.

Les scores de Metal Slug et de Metal Slug 3 sont déjà dans leurs fichiers, trouvés avec `apprendre.bat` sous RetroArch et FinalBurn Neo. Pour remplacer le char par ton propre dessin, dépose `mslug_tank.gif` (ou `mslug_tank.png` en bande de 3 images) dans `sprites\`. Il doit tenir sur 5 pixels de haut, canon vers la droite.

### Jeux de combat

Chaque jeu de combat Neo Geo a son propre fichier dans `games\`, versions officielles comprises (japonaise, coréenne, prototype). Les adresses viennent des codes de triche de FinalBurn Neo, des scripts d'entraînement FinalBurn Neo de peon2 et de la base de triche de MAME 2003-Plus. Le score n'est connu que pour les King of Fighters. Pour les autres, apprends-le avec `apprendre.bat` (`score=...` et `score2=...`).

Quand une barre de vie, un chrono ou un nom ne colle pas à l'écran, lance `test_retroarch.bat` pendant un combat et envoie le résultat.

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
| Samurai Shodown II | `samsho2.json` | oui | oui | oui (17) | à apprendre |
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

### Tous les jeux Neo Geo

Les jeux Neo Geo connus de MAME (clones compris) ont une scène commune selon leur genre, sans rien faire. En haut, « SNK - » puis le vrai titre du jeu défilent.

| Genre | Fichier | Ce qui s'affiche |
|---|---|---|
| Combat (King of Fighters, Samurai Shodown, Fatal Fury, Art of Fighting, World Heroes...) | `neogeo_combat.json` | façon Vera. En haut le score, ou le titre tant qu'il n'est pas appris, et INSERT COIN qui clignote du côté de l'ordinateur. Au milieu les barres de vie vertes et le chrono, « KO » à la fin du combat (52 jeux, voir le tableau Jeux de combat), sinon « VS ». En bas « P1 », et « CPU » ou « P2 » en face. Dans 34 jeux, le nom du personnage en train de se battre s'affiche à côté (« P1 RALF » et « LEONA CPU »). Les crédits sous le chrono quand ils sont connus. Un filet orange tout en bas |
| Shoot'em up (Blazing Star, Pulstar, Last Resort, Aero Fighters...) | `neogeo_shoot.json` | un petit vaisseau qui traverse un champ d'étoiles et tire quand le score monte |
| Sport et course (Super Sidekicks, Neo Turf Masters, Windjammers...) | `neogeo_sport.json` | un terrain avec un ballon qui rebondit |
| Réflexion, quiz, mahjong (Puzzle Bobble, Magical Drop...) | `neogeo_reflexion.json` | une rangée de blocs de couleur qui changent |
| Action, plates-formes, beat'em up et le reste (Sengoku, Shock Troopers...) | `neogeo.json` | des collines bleues, et les barres de vie des deux joueurs quand elles sont connues |

- Avec RetroArch, la scène affiche « NEO GEO » au milieu tant que rien n'est connu pour ce jeu. Avec MAME, les crédits s'affichent en plus.
- Les crédits d'une Neo Geo MVS sont rangés dans la mémoire de sauvegarde de la borne. MAME la lit. Le cœur FinalBurn Neo de RetroArch ne partage que la mémoire de travail du jeu, donc pas les crédits. Certains jeux en gardent une copie dans leur mémoire de travail. Pour le savoir, apprends-les avec `apprendre.bat` (même méthode que pour le score) en tapant `crédits=2`, puis remets une pièce et tape `crédits=3`, et encore une fois. Si l'outil trouve une adresse, les crédits s'affichent. S'il répond « Rien trouvé », ce jeu n'en garde pas de copie.
- Les barres de vie et le chrono viennent de la base de codes de triche de MAME 2003-Plus. Ils marchent avec RetroArch comme avec MAME.
- Apprends le score d'un jeu avec `apprendre.bat` (même méthode que juste en dessous). L'outil crée alors `games\<jeu>.json`, par exemple `games\kof98.json`. Il garde la scène du genre et ses barres de vie, et ajoute le score. Les fichiers communs ne sont jamais modifiés.
- Un jeu qui a son propre fichier (les Metal Slug par exemple) passe toujours avant la scène commune.
- Le score de KOF 98 a été trouvé avec `apprendre.bat`. Il est rangé dans la fiche de chaque joueur, et cette fiche est la même de KOF 96 à 2001 (barre de vie et jauge de puissance aux mêmes adresses). Le score de ces jeux est donc pris à la même place. Si la dalle n'affiche pas le même score que l'écran dans l'un d'eux, apprends-le avec `apprendre.bat`, l'adresse trouvée remplace la supposée.
- Dans King of Fighters '96 à 2000, chaque équipe est lue dans la mémoire du jeu (personnages choisis, ordre de passage, personnages déjà battus). Le nom change tout seul quand le personnage suivant entre. `test_retroarch.bat` affiche les deux personnages lus, pratique pour vérifier.
- Le BIOS de la Neo Geo dit qui joue. Contre l'ordinateur, « CPU » s'affiche en face et INSERT COIN clignote de son côté (PRESS START s'il reste des crédits). À deux, les deux scores sont en haut. Quand personne ne joue, le titre défile en haut et INSERT COIN clignote en bas.

### Apprendre le score

1. Lance le jeu dans RetroArch et commence une partie. Joue jusqu'à avoir quelques points.
2. Lance `apprendre.bat`. Il voit que RetroArch tourne et passe en mode direct.
3. Tape le score affiché à l'écran, par exemple `score=20600`, puis Entrée. Le jeu est en pause tant que tu es dans cette fenêtre.
4. Retourne dans le jeu (Alt+Tab), marque d'autres points, reviens dans la fenêtre d'`apprendre.bat` et tape le nouveau score.
5. Recommence trois ou quatre fois, avec un score différent à chaque fois. Entrée vide pour finir.
6. L'outil trouve l'adresse et l'écrit dans le fichier du jeu (`games\mslug3.json` par exemple, ou un nouveau fichier pour un jeu Neo Geo qui n'en a pas). Le score apparaît sur la dalle quelques secondes après, sans relancer le jeu.

Tape seulement les valeurs qui manquent. Les vies sont déjà connues, et les apprendre à partir du « 1UP » de l'écran donnerait une mauvaise adresse.

Pour le score du joueur 2, fais une partie à deux et tape les deux scores à chaque fois, par exemple `score=9400 score2=800`.

Noms reconnus `score`, `score2` (ou `score_p2`), `crédits` (ou `credits`), `vies`, `vies2`, `bombes`, `munitions`. Pour un autre jeu, l'outil crée un fichier dans `games\` avec la scène générique.

Ce que l'outil trouve est aussi copié dans `appris\`. Une nouvelle version d'ArcadeDMD remplace les fichiers de `games\`, mais le moteur remet tout seul les adresses apprises au démarrage. Pour oublier ce qui a été appris pour un jeu, supprime son fichier dans `appris\`.

### Bon à savoir

- Un jeu RetroArch sans fichier dans `games\` ne change rien sur la Pixelcade (sauf avec `"takeover": "all"`).
- Dans `config.json`, rubrique `retroarch`, `"enabled": false` coupe la surveillance.
- Si le journal dit « RetroArch refuse de lire la mémoire du jeu », c'est le cœur qui ne la donne pas. Le journal dit lequel est chargé et quoi faire.

---

## 8. Ajouter un jeu ou modifier une scène

1. Copie `games\aburner2.json` sous le nom court du jeu, par exemple `games\outrun.json`.
2. Change `"match"` (`"system": ["outrun"]`), le titre et les valeurs.
3. Trouve les adresses avec `apprendre.bat` (sans fichier dédié, l'outil crée le fichier pour toi).
4. Modifie la scène. Le moteur recharge les fichiers à chaud, pas besoin de relancer pendant que tu ajustes.

Formats de valeurs reconnus

| `type` | Signification |
|---|---|
| `u8` | un octet |
| `be` / `le` | binaire sur `bytes` octets, ordre normal ou inversé |
| `bcd` / `bcd_le` | BCD sur `bytes` octets (deux chiffres par octet) |
| `digits` | un chiffre par octet (`digit_offset` 0x30 pour de l'ASCII) |

Options communes, `mult` (score stocké divisé par 10, très fréquent), `add`, `min`, `max`, `mask`, `shift`. `learn_ranges` limite la zone capturée par l'outil d'apprentissage.

Pour une valeur rangée dans un objet qui change de place en mémoire (les combattants de Samurai Shodown à chaque round), `"ptr"` donne l'adresse où lire la position de l'objet (32 bits) et `"addr"` devient le décalage dans l'objet. `"ptr_range"` écarte un pointeur pas encore prêt.

`"derived"` calcule une valeur à partir d'autres, par exemple le nom du personnage. `"value"` reprend une valeur lue, `"pick"` choisit dans une liste selon `"at"`, `"names"` change un numéro en texte. Voir `games\samsho2.json` et `games\kof98.json`.

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
| `sprite` | sprite animé (PNG en bande ou GIF) | `image`, `frames`, `mode` (`pass`, `pingpong`, `fixed`), `dim` (luminosité), `alpha`, `shoot` (tire quand une valeur monte) |
| `gauge` | barre de vie | `var`, `max`, `x`, `y`, `w`, `h`, `anchor` (côté accroché), `color`, `low`, `back`, `border`, `bevel` (liseré clair en bas et à droite) |
| `clock` | horloge | `format`, `font` |
| `image`, `rect` | image fixe, rectangle | |

Polices disponibles `4x6`, `5x8`, `6x10`, `6x13`, `7x14`, `7x14B`, `8x13B`, `9x15B`. Le `y` d'un texte correspond au haut des majuscules. `when` affiche un élément sous condition, par exemple `{"has": "credits"}` ou `{"var": "mode", "eq": 12}`.

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
- **« Python est introuvable ».** Le raccourci `python` du Microsoft Store ne compte pas, il ne lance rien. Relance `installer.bat`, il propose d'installer Python 3.13. Les fichiers .bat trouvent aussi un Python installé sans être dans le PATH.
- **ArcadeDMD n'apparaît pas dans le menu Tab de MAME.** MAME est peut-être trop ancien (il faut 0.227 ou plus récent, `installer.bat` affiche la version). Sinon le plugin est désactivé, voir « Vérifier le plugin dans MAME ».
- **Rien ne s'affiche pendant un jeu.** Regarde `runtime\arcadedmd.log` et vérifie que `runtime\events.jsonl` grossit pendant la partie. Sinon, le chemin `root` du fichier `MAME\plugins\arcadedmd\settings.json` ne pointe pas vers le dossier ArcadeDMD.
- **« ZeDMD : dalle non trouvée ».** Vérifie le câble (data), le port USB natif de l'ESP32-S3, et qu'aucun autre logiciel n'utilise la dalle (DOF2DMD, VPX, dmdext, ou le moteur ArcadeDMD déjà lancé en arrière-plan). La recherche automatique s'arrête après trois essais. Une fois la dalle trouvée, son port est mémorisé et seul ce port est réessayé.
- **Pistolets RetroShooter ou autres appareils série.** La recherche d'une dalle ZeDMD interroge les ports COM (jamais celui de la Pixelcade, et pas du tout si la sortie ZeDMD est coupée). Pour ne jamais toucher aux pistolets, indique le port de la dalle dans `config.json` (`"device": "COM5"`) ou exclus ceux des pistolets (`"ignore_devices": ["COM3", "COM4"]`).
- **Dalle noire après une mise en veille ou un débranchement.** Relance ArcadeDMD, libzedmd ne se reconnecte pas toute seule.
- **Couleurs inversées, lignes fantômes.** Ordre RGB et « panel driver » dans le menu ZeDMD (ou avec ZeDMD_Updater2).
- **Animation saccadée sur la dalle.** Monte « USB packet size » et « min refresh » dans le menu ZeDMD.
- **Pas de fenêtre LED virtuelles.** pygame-ce doit être installé (`py -m pip install pygame-ce`).
- **`test_dalle.bat` dit que le moteur tourne déjà.** Le lancement automatique occupe la dalle. Ferme `pythonw.exe` dans le Gestionnaire des tâches, ou teste directement avec un jeu.
- **Le moteur s'arrête tout seul.** L'erreur est notée dans `runtime\arcadedmd.log`.
- **« Pixelcade : port introuvable ».** Indique le port dans `config.json` (`ports.bat` pour le trouver). ArcadeDMD ne sonde pas les autres ports COM, pour ne pas déranger les pistolets.
- **« pixelweb ne s'arrête pas ».** Ferme pixelweb à la main (icône dans la barre des tâches) et vérifie `pixelweb_url` (par défaut `http://127.0.0.1:8080`).
- **pixelweb ne revient pas après un jeu.** Le chemin est mémorisé dans `runtime\pixelweb_path.txt` au premier arrêt. Sinon, renseigne `pixelweb_exe` dans `config.json`.
- **Pixelcade noire pendant un jeu.** Regarde le journal. Si pixelweb a bien été arrêté mais que la carte ne répond pas, débranche et rebranche la Pixelcade, puis relance `test_pixelcade.bat`.

---

## Licences et crédits

Code ArcadeDMD sous licence MIT. Polices bitmap issues des polices X11 « misc-fixed » (domaine public). ZeDMD (firmware GPLv2) et libzedmd (GPLv3) sont téléchargés séparément depuis leurs dépôts officiels https://github.com/PPUC. Les noms de jeux servent uniquement à les identifier.
