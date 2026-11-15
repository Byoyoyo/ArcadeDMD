Depuis la 1.33, ArcadeDMD enregistre chaque partie que tu joues. Une partie, jouée normalement, suffit pour régler un jeu sans la borne. Son fichier est corrigé d'après l'enregistrement, la partie est rejouée dans la scène HD pour vérifier chaque moment, et l'enregistrement est gardé comme test pour que rien ne casse plus tard.

## Ce qui est enregistré

1. **Les valeurs lues**, avec leur heure, dans `runtime\captures\<jeu>-<date>.log`. Quelques centaines de Ko pour un match, avec MAME comme avec RetroArch. Chaque appui sur un bouton de pièce y est aussi.
2. **Toute la mémoire du jeu** (RetroArch), quatre fois par seconde en différences compressées, dans `runtime\captures\<jeu>-<date>.ram`. Quelques Mo pour dix minutes. Elle montre où le jeu garde ce qui n'est pas encore lu, la vie d'un boss, le type d'un véhicule.
3. **Des captures d'écran** demandées à RetroArch (sa commande réseau `SCREENSHOT`) à la première lecture, toutes les deux secondes pendant qu'on joue, et tout de suite quand une vie, une mission, un véhicule ou un des drapeaux du jeu change. Elles arrivent dans le dossier des captures de RetroArch, l'heure dans leur nom.
4. **Le repère.** Un bouton de pièce tenu une bonne seconde pendant la partie écrit `marker n` dans l'enregistrement avec son heure, prend une capture d'écran et ajoute une ligne au journal. Sers-t'en pour dire « ici » quand il se passe quelque chose à regarder.

## Réglages

| Où | Réglage |
|---|---|
| en haut de `config.json` | `"capture"`, `"all"` (toutes les parties, par défaut), `"fights"` (les jeux de combat seulement) ou `"off"` |
| section `retroarch` | `"ram_dump": {"enabled": true, "every": 0.25}` |
| section `retroarch` | `"screenshots": {"enabled": true, "every": 2.0, "dir": ""}`. Mets dans `"dir"` le dossier des captures de RetroArch (Réglages, Dossiers, Captures d'écran) et le journal dit si la première image est apparue |

Dans RetroArch, coupe la notification et le flash des captures d'écran (Réglages, Affichage à l'écran, Notifications à l'écran). Coupe aussi « Capture d'écran GPU » (Réglages, Vidéo, Sortie, un réglage avancé), sinon les images sortent avec le shader CRT en pleine taille, 3 Mo chacune, au lieu du 304 x 224 du jeu.

## Envoyer une partie

Pour un jeu qui n'est pas encore réglé, ou un jeu qui se comporte mal, joue une partie normale de cinq à dix minutes. Pour un jeu de combat, un match suffit, deux rounds gagnés, un perdu, un super coup. Pour un Metal Slug, jusqu'au premier boss, avec quelques grenades, une vie perdue et un véhicule.

Ensuite zippe et joins à une [issue](https://github.com/Byoyoyo/ArcadeDMD/issues) GitHub.

- le `.log` et le `.ram` de la partie, dans `runtime\captures`
- le zip des captures d'écran
- `runtime\arcadedmd.log`

## Le robot

Les jeux peuvent jouer tout seuls, pour que leur mémoire soit enregistrée sans personne devant la borne (1.39). RetroArch accepte les boutons d'une manette par le réseau, et le robot les envoie : une pièce, START, puis le stick et les boutons au hasard, et un deuxième joueur pour la fin de chaque partie.

1. Laisse ArcadeDMD tourner. Tant que le robot joue, il enregistre toute la mémoire de chaque jeu quels que soient ses réglages, et laisse les captures d'écran au robot. Le robot attend la parole d'ArcadeDMD avant de jouer un jeu.
2. Lance `robot_test.bat` avec un jeu Neo Geo démarré depuis ton frontend. Il lit comment RetroArch a été lancé, ferme le jeu, le relance lui-même, vérifie que le jeu voit le stick qu'il tient et joue deux minutes. Son résultat est dans `runtime\robot_test.txt`.
3. Lance `robot.bat`. Il joue tous les jeux d'ArcadeDMD dont la ROM est dans le même dossier, six minutes chacun, les jeux de combat d'abord. `robot.bat 10` joue dix minutes chacun, `robot.bat samsho2 garou` seulement ces jeux. Ctrl+C l'arrête, et il reprend où il en était quand il est relancé.

Le robot demande une capture d'écran à RetroArch toutes les dix secondes. Quand un jeu est fermé, son enregistrement et ses captures vont dans un seul fichier, `runtime\robot\<jeu>.zip`.

Tant que le robot joue, RetroArch tourne en fenêtre, sans son et sans lire les manettes de l'ordinateur. L'écran doit rester allumé : RetroArch ne peut pas ouvrir sa fenêtre sans lui. Windows est empêché de se mettre en veille. Seul Ctrl+C arrête le tour. Un jeu qui ne démarre pas, ou qui est coupé avant la moitié, est réessayé une fois à la fin du tour, puis laissé de côté et nommé à la fin. Les jeux laissés de côté passent en dernier au lancement suivant. Quand trois jeux de suite échouent, le robot lance un jeu qu'il a déjà enregistré. S'il tourne, ce sont ces trois jeux qui sont en cause et le tour continue. S'il échoue aussi, l'écran est éteint, ArcadeDMD est fermé ou les ROM ne sont plus là, et le robot attend, regarde à nouveau toutes les cinq minutes, puis reprend ces jeux tout seul dès que ça remarche. Un stick que le jeu ne montre pas, ou un jeu qui ne tourne pas à sa vitesse, est écrit sur la ligne du jeu et n'arrête jamais rien. Une erreur imprévue coûte un jeu et reste dans `runtime\robot_crash.log`.

`robot_screen_off.bat` est le même tour pour un écran éteint, la nuit par exemple. RetroArch tourne sans aucune fenêtre et la mémoire est enregistrée, mais sans captures d'écran : RetroArch se ferme quand on lui en demande une sans pilote vidéo. Les jeux joués ainsi sont rejoués, avec leurs captures, par `robot.bat`.

`robot_win.bat` est un deuxième tour, pour les seuls jeux de combat, dix minutes chacun (1.39). Le robot du premier tour perd vite et ne rencontre que trois à cinq combattants et deux à quatre stages d'un jeu. Dans celui-ci il gagne ses combats, pour traverser chaque jeu de son premier adversaire au dernier. Pendant un round il écrit trois choses dans la mémoire du jeu, là où le fichier du jeu les lit. La vie du joueur 1 est remise au plus haut qu'elle a eu dans le round, celle de l'adversaire est gardée à un dixième, et le chrono est mis à sa fin dès qu'il a compté trois secondes. Rien n'est écrit hors d'un round, et jamais dans une partie jouée à la main. Un jeu dont le fichier ne connaît pas les barres de vie est joué comme au premier tour, et si RetroArch ne prend pas les écritures le tour continue avec deux joueurs robots, qui rencontrent plus de combattants qu'un seul. Ses fichiers vont dans `runtime\robot\win`, sa liste de jeux faits est la sienne, et il s'arrête et reprend comme le premier.

Les réglages de RetroArch ne sont pas modifiés, et les jeux joués par le robot restent hors de son historique. Les réglages du robot sont dans `runtime\robot.cfg`, donné à RetroArch sur sa ligne de commande.

## Des outils pour les curieux

- `python tools\replay_capture.py runtime\captures\<fichier>` écrit ce que montrait l'écran HD seconde par seconde, `--frames 30,47` le dessine à ces secondes.
- `python tools\values_check.py runtime\robot\<jeu>.zip` vérifie chaque valeur du fichier du jeu contre une partie enregistrée par le robot (1.39). Un chrono descend et repart de son plus haut, une barre de vie descend coup après coup et se lit pleine au début d'un round, un score ne fait que monter. `--sheet out.jpg` met six captures d'écran sur une image avec ce que lit le fichier à la même seconde, pour vérifier à l'œil. `--find` cherche le chrono et les barres de vie dans toute la mémoire, `--match 45:35 105:25` les octets qui valent les nombres lus sur les captures.
- `python tools\ram_diff.py <fichier.ram> --down 120 160` liste les mots de mémoire qui ne font que baisser entre deux moments (une vie), `--watch 0x1012AA` en suit un, `--diff 118 121` montre ce qui a changé.

Les enregistrements déjà reçus sont gardés dans `tests\captures` et rejoués comme tests.
