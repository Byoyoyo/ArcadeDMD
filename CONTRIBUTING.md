# Contributing / Contribuer

English first, then French. / L'anglais d'abord, puis le français.

## English

Thanks for your interest in ArcadeDMD.

- **A game shows wrong values, or a display misbehaves.** Open an issue with the "Problem with a game or a display" template. Attach `runtime\arcadedmd.log`, and the output of `test_retroarch.bat` for a RetroArch game.
- **You would like a new game.** Open an issue with the "New game" template. Say which emulator and core you use. If `learn.bat` already found some addresses, attach the files of the `learned` folder.
- **You want to change the code or a game file.** Open a pull request with one subject per pull request. Write every message in English and in French (`tr("français", "English")` in Python, the same in the MAME plugin), and run `python tools/package.py --check` before sending it. The maintainer reviews every pull request and decides what is merged.

Game names are used only to identify the games. Do not add images, logos or sounds taken from a game. Everything on screen is drawn by the program.

## Français

Merci de ton intérêt pour ArcadeDMD.

- **Un jeu affiche de mauvaises valeurs, ou un affichage se comporte mal.** Ouvre une issue avec le modèle « Problème avec un jeu ou un affichage ». Joins `runtime\arcadedmd.log`, et le résultat de `test_retroarch.bat` pour un jeu RetroArch.
- **Tu aimerais un nouveau jeu.** Ouvre une issue avec le modèle « Nouveau jeu ». Indique l'émulateur et le core utilisés. Si `learn.bat` a déjà trouvé des adresses, joins les fichiers du dossier `learned`.
- **Tu veux modifier le code ou un fichier de jeu.** Ouvre une pull request, avec un seul sujet par pull request. Écris chaque message en anglais et en français (`tr("français", "English")` en Python, pareil dans le plugin MAME), et lance `python tools/package.py --check` avant de l'envoyer. Le mainteneur relit chaque pull request et décide de ce qui est fusionné.

Les noms de jeux servent uniquement à les identifier. N'ajoute pas d'images, de logos ou de sons pris dans un jeu. Tout ce qui s'affiche est dessiné par le programme.
