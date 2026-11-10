## Ce qu'il te faut

- Windows.
- Python 3.12 ou plus récent. S'il manque, `install.bat` propose d'installer Python 3.13 depuis python.org.
- Pour les jeux MAME, MAME 0.227 ou plus récent. L'installeur affiche ta version.
- Pour les jeux RetroArch, RetroArch 1.19 ou plus récent (voir [[Avec RetroArch]]).
- Un affichage pour le marquee. Un écran LCD que Windows voit comme un écran (voir [[Marquee HD]]), une [[Dalle Pixelcade]] ou une dalle ZeDMD (voir [[ZeDMD et matériel]]).

## Installer

1. Télécharge le zip de la dernière version sur la page [Releases](https://github.com/Byoyoyo/ArcadeDMD/releases/latest).
2. Avant de l'extraire, fais un clic droit sur le zip, Propriétés, coche « Débloquer », puis OK. Windows ne demandera plus de confirmation à chaque fichier .bat.
3. Extrais le dossier `ArcadeDMD` dans un chemin sans accents, idéalement `C:\ArcadeDMD`. MAME ne sait pas ouvrir les dossiers avec des accents.
4. Lance `install.bat`. Il installe Pillow, pyserial et pygame-ce, copie le plugin dans MAME, règle la Pixelcade et propose de lancer ArcadeDMD automatiquement avec Windows. Il ne télécharge libzedmd (le pilote ZeDMD) que si tu dis avoir une dalle ZeDMD. Si tu n'utilises que RetroArch, appuie sur Entrée à la question MAME.
5. Avec un marquee LCD, lance `screen_setup.bat` (l'installeur le propose aussi). Il trouve l'écran du marquee et règle tout dans `config.json`.

## Ce que l'installation change

- Le dossier `C:\ArcadeDMD`. Les réglages, le journal et les enregistrements restent dedans.
- Dans MAME, un nouveau dossier `plugins\arcadedmd` avec trois petits fichiers. Rien d'autre dans MAME. `mame.ini` et `plugin.ini` ne sont pas modifiés, MAME charge tout seul les plugins de son dossier `plugins`.
- Un fichier `ArcadeDMD.bat` dans le dossier Démarrage de Windows, seulement si tu acceptes le lancement automatique.
- Trois bibliothèques ajoutées à Python (Pillow, pyserial, pygame-ce).
- Avec une Pixelcade, pendant les jeux qui ont un fichier dans `games\`, ArcadeDMD arrête pixelweb et le relance à la fin du jeu. Pour les autres jeux, rien ne change.

Le plugin ne fait que lire la mémoire du jeu. Il ne change ni le jeu, ni les commandes, ni les réglages de MAME.

## Premier essai sans jeu

Les démos montrent les scènes avec des valeurs simulées, sur l'écran du marquee ou sur la dalle, sans MAME ni RetroArch.

| Fichier | Ce qu'il montre |
|---|---|
| `demo_fight.bat` | The King of Fighters '98, de l'écran des pièces au combat |
| `demo_neogeo.bat` | un jeu Neo Geo fait un par un, à choisir dans une liste |
| `demo_capcom.bat` | un jeu Capcom CPS1, CPS2 ou CPS3 |
| `demo_cave.bat` | un jeu Cave (DoDonPachi, Ketsui, Espgaluda, Mushihime-sama, Deathsmiles...) |
| `demo_afterburner.bat`, `demo_sonic.bat` | After Burner II, Sonic |

## Mettre à jour

Extrais la nouvelle version par-dessus l'ancienne. `config.json` n'est jamais écrasé, il a été créé à partir de `config.default.json` à la première installation. Les adresses trouvées avec `learn.bat` sont gardées dans `learned\` et remises au démarrage. Tes propres images dans `sprites\` restent.

## Désinstaller

Supprime le dossier `plugins\arcadedmd` de MAME, le fichier `ArcadeDMD.bat` du dossier Démarrage (tape `shell:startup` dans Win+R pour l'ouvrir), puis le dossier `C:\ArcadeDMD`. Pour seulement couper le plugin, ajoute la ligne `arcadedmd 0` au `plugin.ini` de MAME.

Ensuite, [[Utilisation]].
