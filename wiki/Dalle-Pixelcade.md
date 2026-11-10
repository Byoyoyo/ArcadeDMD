La Pixelcade LED est elle-même une dalle 128 x 32. ArcadeDMD la pilote directement par son port USB, avec le même protocole que Visual Pinball (dmdext, libdmdutil). Les cartes V1 et V2 sont reconnues toutes seules. Pas d'autre dalle à acheter.

![Les scènes sur une dalle LED 128 x 32](images/led_reel.gif)

## Comment elle partage la dalle avec pixelweb

pixelweb, le logiciel de la Pixelcade, ne sait pas partager la dalle. ArcadeDMD fait ce que Pixelcade conseille pour Visual Pinball.

1. Quand un jeu qui a son fichier dans `games\` démarre, ArcadeDMD arrête pixelweb par son API (`/quit`) et prend la dalle.
2. Quand tu quittes le jeu, il rend la dalle tout de suite et relance pixelweb. Le marquee du jeu reste affiché en attendant, puis ArcadeDMD demande à pixelweb de l'afficher, comme le ferait BigBox.
3. BigBox reprend la Pixelcade à chaque changement de jeu, comme avant.

Pour tous les autres jeux, pixelweb continue d'afficher ses marquees.

## Réglage

`install.bat` pose la question et règle le port tout seul. À la main.

1. Lance `ports.bat` et trouve le port de la Pixelcade (dans le doute, débranche-la et regarde quel port disparaît).
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

3. Lance `test_pixelcade.bat`. La mire affiche RED, GREEN et BLUE, puis le test demande si chaque mot est dans sa couleur. Si tu réponds n, il inverse le vert et le bleu dans `config.json`. Relance-le pour vérifier.
4. Lance `demo_fight.bat`. La scène passe sur la Pixelcade, puis pixelweb revient quand tu la fermes.

## Options

| Réglage | Effet |
|---|---|
| `"takeover": "known"` | prend la dalle seulement pour les jeux qui ont un fichier dans `games\` |
| `"takeover": "all"` | prend la dalle pour tous les jeux MAME, avec la scène générique |
| `"mode": "always"` | garde la dalle tout le temps (si tu n'utilises plus pixelweb), noire en dehors des jeux |
| `"pixelweb_exe"` | le chemin de pixelweb.exe, trouvé tout seul en général. S'il lui faut des options, mets ici un .bat qui le lance avec |
| `"art_dir"` | le dossier de la Pixelcade, pour reprendre ses marquees en fond de la scène générique |
| `"gamma": 2.2` | les LED s'allument en proportion de la valeur reçue, alors un gris foncé fait pour un écran brille sur la dalle. ArcadeDMD corrige les couleurs pour que la dalle ressemble au preview. `1.0` les envoie telles quelles |

Les cartes V1 affichent 3 bits par couleur en mode direct, c'est une limite du matériel. Les cartes V2 affichent toutes les couleurs.

Un jeu qui a un fichier mais pas de scène à lui (un jeu appris avec `learn.bat`, par exemple) a la scène générique, son marquee Pixelcade assombri derrière le score et les crédits.

## Ton propre INSERT COIN

Un GIF Pixelcade à toi, en 128 x 32, dans `sprites\insert_coin.gif` (ou `.png`) remplace l'écran des pièces tant qu'il n'y a pas de crédit. La pièce tombe quand même quand tu en mets une.

## Avec DOFLinx

ArcadeDMD ne touche pas aux fichiers de DOFLinx, ni au réglage `output` de `mame.ini` dont DOFLinx a besoin. Avec la Pixelcade et sans ZeDMD, ArcadeDMD n'ouvre aucun autre port COM, les appareils pilotés par DOFLinx ne sont donc pas dérangés. Voir [[OBS et DOFLinx]].

Si quelque chose ne va pas, voir [[Dépannage]].
