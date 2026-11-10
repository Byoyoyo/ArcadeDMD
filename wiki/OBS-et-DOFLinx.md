## Fichiers texte pour OBS

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

## Passerelle DOFLinx (facultatif)

ArcadeDMD sait se faire passer pour DOF2DMD. DOFLinx lui envoie alors le score et les crédits de tous les jeux qu'il connaît, sans aucune adresse à chercher.

1. Dans `config.json`, mets `"enabled": true` dans la section `doflinx_bridge`. Elle écoute sur le port 8081, pour laisser le 8080 à pixelweb.
2. DOFLinx lit l'adresse dans le `settings.ini` de DOF2DMD (`url_prefix`). Mets `http://127.0.0.1:8081`.
3. Ne lance plus DOF2DMD en même temps, les deux ne peuvent pas écouter le même port. Quand ArcadeDMD répond, DOFLinx ne cherche plus à démarrer DOF2DMD.

Les deux sources se complètent. Pour After Burner II, le record vient du plugin et le score de DOFLinx.
