## After Burner II

L'emplacement du meilleur score est public (le tableau des meilleurs scores à `0xFF846E`, celui qu'utilise `hiscore.dat`). Le score et les crédits ne sont documentés nulle part, d'où l'outil d'apprentissage. Compte cinq minutes, avec MAME.

1. Lance After Burner II.
2. Mets une pièce, attends un peu, mets-en une deuxième. Les crédits changent.
3. Joue. Quand le score est stable (pas pendant un décompte de bonus), appuie sur **Ctrl droit + D**. Un message à l'écran confirme la capture. Tab, Plugin Options, ArcadeDMD, l'entrée de capture de la RAM fait la même chose.
4. Recommence la capture à trois ou quatre moments, avec des scores et des crédits différents, dont une juste après START (un crédit de moins).
5. Quitte MAME et lance `learn.bat`. Pour chaque capture, l'outil ouvre la capture d'écran et demande les valeurs, par exemple `score=16060 credits=3`.
6. Il trouve l'adresse dans tous les formats habituels et l'écrit dans `games\aburner2.json`.

Relance le jeu. Le score et les crédits s'affichent maintenant sur le marquee et dans le menu Tab du plugin.

Si plusieurs zones sont trouvées, une capture de plus tranche. Si rien n'est trouvé, supprime la ligne `learn_ranges` de `games\aburner2.json` et le dossier `runtime\learn\aburner2`, puis recommence les captures. L'outil cherche alors dans toute la RAM que voit le processeur principal.

DOFLinx peut aussi donner le score et les crédits d'After Burner II et de plus de 2 000 jeux (voir [[OBS et DOFLinx]]).

`demo_afterburner.bat` montre la scène avec des valeurs simulées.

## Sonic 1 et Sonic 2

Les adresses viennent des désassemblages de la communauté pour Sonic 1 et Sonic 2 (score, anneaux, vies, zone), les mêmes dans les deux jeux.

- Dans MAME, la Mega Drive / Genesis (pilotes `genesis` ou `megadriv`, la cartouche Sonic de la liste des logiciels ou un fichier ROM de ce nom), et les versions arcade Mega Play et Mega-Tech (`mp_sonic`, `mt_sonic`, `mp_soni2`, `mt_soni2`).
- Dans RetroArch, le cœur Genesis Plus GX, ou PicoDrive (voir [[Avec RetroArch]]).

`games\sonic.json` sert pour Sonic 1 et `games\sonic2.json` pour Sonic 2. Le petit personnage qui court sur l'herbe est un anneau générique. Ton propre sprite animé va dans `sprites\sonic.gif` (ou une bande `sonic.png` de 6 images), `sonic2.gif` pour Sonic 2. Règle `"y"` dans le fichier du jeu à sa hauteur.

`demo_sonic.bat` montre la scène avec des valeurs simulées.

## N'importe quel autre jeu

Un jeu MAME sans fichier a la scène générique avec `"takeover": "all"`. Pour lui donner la sienne, voir [[Fichiers des jeux]] et [[Apprendre les adresses]].
