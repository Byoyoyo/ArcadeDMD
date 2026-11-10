Tout ce qu'affiche ArcadeDMD est dessiné par le programme. Aucune image ne vient des jeux, à part ton Clear Logo LaunchBox quand un jeu démarre. Tu peux remplacer certains dessins par tes propres images, en les déposant dans le dossier `sprites\` d'ArcadeDMD.

Tes images restent à toi. Elles ne sont jamais dans le zip d'une nouvelle version, ni dans le dépôt, et une mise à jour les laisse en place.

## Comment une image est utilisée

- Le PNG marche partout. `.gif`, `.jpg` et `.webp` marchent aussi pour les images des Metal Slug.
- Un fond uni autour du dessin est rendu transparent et les marges vides sont coupées, une image détourée grossièrement convient donc.
- `runtime\arcadedmd.log` dit quelle image est utilisée, ou où une image serait lue.

## Sur l'écran HD

| Jeu | Où | Noms |
|---|---|---|
| Metal Slug, les six jeux | `sprites\mslug\<nom>.png` | les véhicules `tank`, `camel`, `slugnoid`, `flyer`, `copter`, `mariner`, `drill`, `astro`, et `elephant`, `ostrich`, `bradley`, `mobile`, `gunner`, `claw`, `walker`, `armor`, vus de côté, canon à droite |
| Metal Slug, les six jeux | `sprites\mslug\<nom>.png` | les soldats `marco`, `tarma`, `eri`, `fio`, `trevor`, `nadia`, un petit portrait à côté du nom du soldat |
| Un seul Metal Slug | `sprites\mslug2\<nom>.png`, `sprites\mslug3\<nom>.png`... | les mêmes noms, pour ce jeu seulement |
| Windjammers | `sprites\wjammers\<nom>.png` | les six joueurs `scott`, `costa`, `wessel`, `yoo`, `biaggi`, `mita`, sur le terrain là où le jeu les met |

Les noms français (`char.png`, `chameau.png`) et l'ancien `sprites\mslug_tank_hd.png` pour le tank marchent encore. Voir [[Les Metal Slug]].

## Sur la dalle LED

| Quoi | Fichier |
|---|---|
| L'écran INSERT COIN | `sprites\insert_coin.gif` (ou `.png`), 128 x 32. Un GIF Pixelcade, par exemple. Il remplace l'écran des pièces tant qu'il n'y a pas de crédit, et la pièce tombe quand même quand tu en mets une |
| Le petit tank de Metal Slug | `sprites\mslug_tank.gif`, ou une bande `mslug_tank.png` de 3 images, 5 pixels de haut au plus, canon à droite |
| Le coureur de Sonic | `sprites\sonic.gif`, ou une bande `sonic.png` de 6 images, `sonic2.gif` pour Sonic 2. Règle `"y"` dans le fichier du jeu à sa hauteur |

## Le logo du jeu

Le logo affiché quand un jeu démarre est ton Clear Logo LaunchBox, trouvé tout seul (voir [[Marquee HD]]). Un jeu qui n'en a pas a son titre en lettres métalliques sur l'écran HD.
