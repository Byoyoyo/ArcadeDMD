Beaucoup de jeux savent déjà où sont leurs valeurs, grâce aux bases de codes de triche, à RetroAchievements ou à une partie enregistrée sur une borne. Quand une valeur manque (le score, très souvent), `learn.bat` la trouve à partir de quelques relevés du jeu, avec les valeurs que tu vois à l'écran.

## Avec RetroArch, en direct

1. Lance le jeu dans RetroArch et joue. Marque quelques points.
2. Lance `learn.bat`. Il voit que RetroArch tourne et passe en mode direct.
3. Tape le score affiché à l'écran, par exemple `score=20600`, puis Entrée. Le jeu est en pause pendant que tu es dans cette fenêtre.
4. Retourne dans le jeu (Alt+Tab), marque d'autres points, reviens et tape le nouveau score.
5. Recommence trois ou quatre fois, avec un score différent à chaque fois. Entrée sur une ligne vide termine.
6. L'outil trouve l'adresse et l'écrit dans le fichier du jeu (`games\mslug3.json`, ou un nouveau fichier pour un jeu qui n'en a pas). Le score s'affiche sur le marquee quelques secondes plus tard, sans relancer le jeu.

Ne tape que les valeurs qui manquent. Une valeur déjà connue, réapprise d'après ce que montre l'écran, pourrait donner une mauvaise adresse.

## Avec MAME, à partir de captures

Appuie sur **Ctrl droit + D** à trois ou quatre moments de la partie (ou Tab, Plugin Options, ArcadeDMD, capture de la RAM), quitte MAME, puis lance `learn.bat`. Pour chaque capture, il ouvre la capture d'écran et demande les valeurs. L'exemple d'After Burner II est dans [[Autres jeux]].

Lancé pendant que RetroArch est fermé, `learn.bat` réanalyse les dernières captures du jeu avec les valeurs déjà tapées.

## Ce qu'il faut taper

| Nom | Valeur |
|---|---|
| `score`, `score2` (ou `score_p2`) | le score de chaque joueur. Pour le joueur 2, joue une partie à deux et tape les deux, `score=9400 score2=800` |
| `credits` | tape-le après une pièce et encore une fois après START (un crédit de moins), pour que l'outil distingue les crédits des pièces mises |
| `lives`, `lives_p2`, `bombs`, `ammo` | les vies, les bombes, les munitions |
| `wins`, `wins2` | les matchs gagnés en VS |
| `stage`, `mission`, `round` | tape le numéro affiché à l'écran, l'outil le trouve même quand le jeu compte à partir de 0 |
| `hits` | une chaîne (`hits=4` pendant que le jeu affiche 4 HIT) |
| `perfect` | quelque chose d'allumé ou d'éteint, tapé 1 ou 0 |

Les noms français `crédits`, `vies`, `vies2`, `bombes`, `munitions`, `victoires`, `victoires2` marchent aussi. Un nom que ni le fichier du jeu ni les scènes ne connaissent est signalé avec le plus proche (« scroe2 n'est pas une valeur de ce jeu, tu voulais dire score2 ? »).

## Les compteurs VS de The King of Fighters (BEAT BY)

Ils ne sont dans aucune base de codes de triche et s'apprennent une fois par jeu.

1. Lance le jeu dans RetroArch et joue en joueur 1.
2. Fais entrer le joueur 2 avec une pièce et START. Tu peux tenir les deux sticks toi-même.
3. Lance `learn.bat`.
4. Après chaque match, quand BEAT BY s'affiche en haut de l'écran du jeu, tape les deux compteurs, `beat=1 beat2=0`. Mets 0 pour le côté marqué CHALLENGER.
5. Joue cinq ou six matchs, un côté qui gagne puis l'autre.
6. Entrée sur une ligne vide. L'outil écrit `beat` et `beat_p2` dans le fichier du jeu.

## Les combattants qui se déplacent en mémoire

Dans Samurai Shodown et The Last Blade, les combattants se déplacent en mémoire à chaque round. L'outil suit la valeur à l'intérieur du combattant. Prends tes captures sur deux rounds différents ou deux combats différents. Il te le rappelle au début.

## Où vont les adresses apprises

Tout ce que l'outil trouve est aussi copié dans `learned\`. Une nouvelle version d'ArcadeDMD remplace les fichiers de `games\`, et le moteur remet les adresses apprises au démarrage. Pour oublier ce qui a été appris pour un jeu, supprime son fichier dans `learned\`.

Si l'outil ne trouve rien, zippe le dossier du jeu dans `runtime\learn\` et joins-le à une [issue](https://github.com/Byoyoyo/ArcadeDMD/issues) GitHub.
