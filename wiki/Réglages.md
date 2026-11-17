Tous les réglages sont dans `config.json`, dans le dossier d'ArcadeDMD. L'installeur le crée à partir de `config.default.json`, et une nouvelle version ne l'écrase jamais. ArcadeDMD voit tout seul quand `config.json` change et prend les nouveaux réglages.

Modifie-le avec le Bloc-notes. Un chemin prend des doubles barres obliques inverses (`"E:\\LaunchBox"`).

## Au premier niveau

| Réglage | Par défaut | Effet |
|---|---|---|
| `language` | `"auto"` | `"auto"` suit la langue de Windows, `"en"` l'anglais, `"fr"` le français |
| `fps` | `50` | images par seconde du moteur |
| `coin_symbol` | `"€"` | le symbole frappé sur les pièces (`"$"`, `"£"`, `""` pour une pièce lisse) |
| `capture` | `"all"` | enregistre les valeurs lues pendant chaque partie (`"all"`, `"fights"`, `"off"`), voir [[Enregistrer une partie]] |
| `show_pause` | `true` | PAUSE clignote sur la dalle LED pendant que le jeu est en pause |
| `idle` | `{"show": false}` | `"show": true` remet l'ancien écran de veille (l'heure et `"text"`) sur une dalle ZeDMD en dehors des jeux |
| `intro` | voir plus bas | le logo du jeu quand un jeu démarre |
| `frontend` | `{"use": "auto", "retrobat": ""}` | d'où viennent les logos des jeux. `"auto"` prend LaunchBox, sinon RetroBat. `"launchbox"`, `"retrobat"` ou `"none"` en imposent un. `"retrobat"` est le dossier de RetroBat quand il n'est pas trouvé tout seul (onglet Frontal de la fenêtre) |
| `window` | `{"enabled": true}` | `false` coupe la fenêtre et l'icône près de l'horloge |

### `intro`

| Réglage | Par défaut | Effet |
|---|---|---|
| `logo` | `true` | `false` coupe le logo, sur la dalle et sur l'écran HD |
| `seconds` | `2.6` | sa durée, de 1 à 10 secondes |
| `launchbox` | `""` | le dossier de LaunchBox, quand il n'est pas trouvé tout seul |

## `outputs.preview`, le marquee LCD

| Réglage | Par défaut | Effet |
|---|---|---|
| `enabled` | `false` | dessine la scène sur un écran (`screen_setup.bat` le règle) |
| `x`, `y`, `width`, `height` | `0`, `1080`, `1920`, `470` | la place de l'écran sur le bureau de Windows et sa taille (Paramètres, Affichage) |
| `borderless`, `topmost` | `true` | une fenêtre sans bord, gardée au-dessus des autres quand elle est affichée |
| `mode` | `"games"` | `"games"` montre la fenêtre pendant les jeux connus seulement et laisse l'écran au frontend le reste du temps, `"always"` la garde, noire en dehors des jeux |
| `takeover` | `"known"` | `"known"` pour les jeux qui ont un fichier dans `games\`, `"all"` pour tous les jeux MAME avec la scène générique |
| `style` | `"led"` | `"led"` des LED rondes, `"pixel"` des pixels carrés, `"hd"` la HD lisse |
| `hd` | `"auto"` | la grille des LED virtuelles, `"auto"`, `1` (128 x 32), `2` ou `4` (plus fin) |
| `launchbox` | `""` | le dossier de LaunchBox pour les Clear Logos, quand il n'est pas trouvé tout seul |
| `coins` | `true` | `false` remet le simple INSERT COIN sur l'écran HD |
| `dim` | `30` | de combien les décors animés sont assombris, de 0 à 80 pour cent |
| `dim_fight` | `55` | la même chose pour les décors des jeux de combat |
| `stage_style` | `"cartoon"` | `"flat"` remet l'allure des décors de King of Fighters '98 de la 1.32 |

Voir [[Marquee HD]].

## `outputs.pixelcade`

| Réglage | Par défaut | Effet |
|---|---|---|
| `enabled` | `false` | pilote la Pixelcade LED |
| `device` | `""` | son port COM (`ports.bat` le trouve) |
| `color_order` | `"auto"` | réglé par `test_pixelcade.bat` quand le vert et le bleu sont inversés |
| `mode`, `takeover` | `"games"`, `"known"` | comme pour le preview |
| `max_fps` | `30` | images par seconde envoyées à la dalle |
| `gamma` | `2.2` | donne à la dalle l'allure du preview, `1.0` envoie les couleurs telles quelles |
| `pixelweb_url` | `"http://127.0.0.1:8080"` | l'adresse de pixelweb |
| `pixelweb_exe` | `""` | le chemin de pixelweb.exe, trouvé tout seul en général |
| `art_dir` | `""` | le dossier de la Pixelcade, pour reprendre ses marquees derrière la scène générique |

Voir [[Dalle Pixelcade]].

## `outputs.zedmd`

| Réglage | Par défaut | Effet |
|---|---|---|
| `enabled` | `false` | pilote une dalle ZeDMD |
| `dll` | `"libzedmd/zedmd64.dll"` | le pilote libzedmd |
| `device` | `""` | le port COM de la dalle, trouvé tout seul quand il est vide |
| `ignore_devices` | `[]` | les ports COM jamais interrogés (des pistolets, par exemple) |
| `wifi_ip` | `""` | l'adresse d'une ZeDMD jointe en Wi-Fi |
| `brightness` | `null` | de 0 à 15 règle la luminosité de la dalle, `null` garde celle de son menu |

Voir [[ZeDMD et matériel]].

## `retroarch`

| Réglage | Par défaut | Effet |
|---|---|---|
| `enabled` | `true` | surveille RetroArch |
| `host`, `port` | `"127.0.0.1"`, `55355` | les commandes réseau de RetroArch |
| `poll_ms` | `100` | tous les combien les valeurs sont lues |
| `ram_dump` | `{"enabled": true, "every": 0.25}` | enregistre toute la mémoire du jeu, voir [[Enregistrer une partie]] |
| `screenshots` | `{"enabled": true, "every": 2.0, "dir": ""}` | demande des captures d'écran à RetroArch pendant une partie, `dir` est le dossier des captures de RetroArch |

Voir [[Avec RetroArch]].

## `lights`

Les LED de la borne suivent le jeu par [HyperHDR](https://github.com/awawa-dev/HyperHDR) (1.39). ArcadeDMD envoie une courte suite de couleurs à un événement, puis rend le ruban à la capture de l'écran.

| Réglage | Par défaut | Effet |
|---|---|---|
| `enabled` | `false` | envoie les événements à HyperHDR |
| `host`, `port` | `"127.0.0.1"`, `8090` | le port web d'HyperHDR |
| `priority` | `50` | la priorité des couleurs d'ArcadeDMD, un nombre plus petit que celui de la capture de l'écran |
| `brightness` | `1.0` | de 0 à 1 |
| `events` | aucun | `{"blow": false}` coupe un événement, parmi `coin`, `blow`, `ko`, `super`, `win` et `boss` |

`test_lights.bat` demande à HyperHDR qui il est et joue chaque événement.

## `coin_buttons`

Écrit par `coin_buttons.bat`. `left`, `right`, `start1` et `start2` sont tes boutons de pièce et de START. `mvs_credits` est le nombre de crédits que donne chaque fente, `[1, 2]` comme une MVS par défaut.

## `textfiles` et `doflinx_bridge`

Voir [[OBS et DOFLinx]].
