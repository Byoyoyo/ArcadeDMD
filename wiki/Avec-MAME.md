Avec MAME, un petit plugin Lua lit les valeurs dans la RAM du jeu et les passe à ArcadeDMD. Il ne fait que lire. Il ne change ni le jeu, ni les commandes, ni les réglages de MAME.

## Installer le plugin

`install.bat` copie le plugin dans le dossier `plugins\arcadedmd` de MAME. Il faut MAME 0.227 ou plus récent, l'installeur affiche ta version. MAME charge tout seul les plugins de son dossier `plugins`, `mame.ini` et `plugin.ini` ne sont pas touchés.

Le frontend (LaunchBox, BigBox, HyperSpin...) n'a besoin d'aucun réglage. MAME charge le plugin à chaque démarrage.

## Vérifier le plugin

Lance un jeu, appuie sur Tab, puis va dans « Plugin Options ». Tu dois voir **ArcadeDMD** avec le jeu détecté et les valeurs lues en direct.

S'il n'apparaît pas, vérifie dans le menu Plugins de MAME qu'il est activé, ou ajoute la ligne `arcadedmd 1` à `plugin.ini` (dans le dossier de MAME ou dans `ini\`). S'il apparaît mais que rien ne s'affiche sur le marquee, le chemin `root` de `MAME\plugins\arcadedmd\settings.json` doit pointer vers le dossier d'ArcadeDMD (voir [[Dépannage]]).

## Ce que MAME donne et pas RetroArch

- Les crédits de tous les jeux Neo Geo. Ils sont dans la mémoire de sauvegarde de la MVS, que MAME lit et que le cœur FinalBurn Neo de RetroArch ne partage pas.
- N'importe quel jeu MAME. Avec `"takeover": "all"`, un jeu sans fichier à lui a la scène générique (son titre, et son marquee Pixelcade derrière sur une Pixelcade).

## Apprendre un jeu sous MAME

Pour un jeu dont personne n'a documenté le score ou les crédits, le plugin prend des captures de la RAM. Appuie sur **Ctrl droit + D** quand le score est stable (ou Tab, Plugin Options, ArcadeDMD, l'entrée de capture de la RAM), à trois ou quatre moments, puis quitte MAME et lance `learn.bat`. Voir [[Apprendre les adresses]] et l'exemple d'After Burner II dans [[Autres jeux]].

## Avec DOFLinx

MAME fait tourner plusieurs plugins à la fois. Les plugins de DOFLinx et d'ArcadeDMD ne se gênent pas, et ArcadeDMD ne touche pas au réglage `output` de `mame.ini` dont DOFLinx a besoin. Voir [[OBS et DOFLinx]].

## Le couper

Ajoute la ligne `arcadedmd 0` au `plugin.ini` de MAME, ou supprime le dossier `plugins\arcadedmd`.
