Tout ce que fait ArcadeDMD est écrit dans `runtime\arcadedmd.log`, affiché en direct dans l'onglet Journal de sa fenêtre. Regarde là d'abord, il dit en général ce qui ne va pas et quoi faire.

## Installation

- **« Python est introuvable ».** Le raccourci `python` du Microsoft Store ne compte pas, il ne lance rien. Relance `install.bat`, il propose d'installer Python 3.13. Les fichiers .bat trouvent aussi un Python installé mais absent du PATH.
- **Windows demande une confirmation à chaque fichier .bat.** Fais un clic droit sur le zip avant de l'extraire, Propriétés, coche « Débloquer ».
- **Pas de fenêtre LED virtuelles.** pygame-ce doit être installé (`py -m pip install pygame-ce`).

## La fenêtre

- **Pas d'icône près de l'horloge.** Windows range les nouvelles icônes dans les icônes cachées, derrière la flèche ^. Glisse-la dans la barre des tâches. Si l'icône ne peut pas être ajoutée, ArcadeDMD ouvre sa fenêtre à la place.
- **La fenêtre ne s'ouvre pas.** Relance `run.bat`, il ouvre la fenêtre de l'ArcadeDMD qui tourne déjà. Sans Microsoft Edge, la fenêtre s'ouvre dans ton navigateur.
- **Pour voir la console comme avant.** Quitte ArcadeDMD depuis le menu de son icône, puis lance `run_console.bat`.

## MAME

- **ArcadeDMD n'apparaît pas dans le menu Tab de MAME.** MAME est peut-être trop ancien (0.227 ou plus récent, `install.bat` affiche la version). Sinon le plugin est désactivé, voir [[Avec MAME]].
- **Rien ne s'affiche pendant un jeu.** Vérifie que `runtime\events.jsonl` grossit pendant le jeu. Sinon, le chemin `root` de `MAME\plugins\arcadedmd\settings.json` ne pointe pas vers le dossier d'ArcadeDMD.

## RetroArch

- **Rien ne change avec RetroArch.** L'onglet Émulateurs de la fenêtre vérifie les réglages de RetroArch et les corrige d'un clic, RetroArch fermé. Sinon vérifie que « Commandes réseau » est activé dans RetroArch et que le journal dit « RetroArch 1.19.x détecté (commandes réseau actives) ». Le jeu doit avoir son fichier dans `games\`.
- **La scène s'affiche mais sans valeurs.** Le cœur ne partage sûrement pas sa mémoire (FB Alpha 2012, par exemple). Lance `test_retroarch.bat` pendant le jeu, il dit quel cœur tourne et lequel prendre. Voir [[Avec RetroArch]].
- **« RetroArch refuse de lire la mémoire du jeu ».** Pareil, c'est le cœur. Le journal dit lequel est chargé.
- **Une pièce ne tombe pas.** Lance `coin_buttons.bat`. Si elle ne tombe toujours pas, lance `test_coins.bat` pendant que tu mets une pièce et envoie son résultat.

## Marquee LCD

- **La scène est sur le mauvais écran, ou coupée.** Choisis l'écran du marquee dans l'onglet Écrans de la fenêtre, relance `screen_setup.bat`, ou règle `x`, `y`, `width` et `height` dans la section `preview` d'après Paramètres, Affichage. Voir [[Marquee HD]].
- **Pas de logo.** Donne le dossier de LaunchBox ou de RetroBat dans l'onglet Frontal de la fenêtre, ou `"launchbox": "E:\\LaunchBox"` dans la section `preview`.

## Pixelcade

- **« Pixelcade : port introuvable ».** Mets le port dans `config.json` (`ports.bat` le trouve). ArcadeDMD n'interroge pas les autres ports COM, pour ne pas déranger les pistolets.
- **« pixelweb ne s'arrête pas ».** Ferme pixelweb à la main (son icône dans la barre des tâches) et vérifie `pixelweb_url` (par défaut `http://127.0.0.1:8080`).
- **pixelweb ne revient pas après un jeu.** Son chemin est enregistré dans `runtime\pixelweb_path.txt` la première fois qu'il est arrêté. Sinon remplis `pixelweb_exe`.
- **Pixelcade noire pendant un jeu.** Si pixelweb a été arrêté mais que la carte ne répond pas, débranche et rebranche la Pixelcade, puis relance `test_pixelcade.bat`.
- **Le vert et le bleu inversés.** Lance `test_pixelcade.bat` et réponds n.

## ZeDMD

- **« ZeDMD : dalle LED introuvable ».** Vérifie le câble (il doit passer les données), le port USB natif de l'ESP32-S3, et qu'aucun autre logiciel n'utilise la dalle (DOF2DMD, VPX, dmdext, ou ArcadeDMD qui tourne déjà en arrière-plan). La recherche s'arrête après trois essais. Une fois trouvée, le port de la dalle est retenu.
- **Pistolets ou autres appareils série.** Donne le port de la dalle (`"device": "COM5"`) ou exclus les leurs (`"ignore_devices": ["COM3", "COM4"]`).
- **Dalle noire après une mise en veille ou un débranchement.** Relance ArcadeDMD, libzedmd ne se reconnecte pas tout seul.
- **Couleurs inversées, lignes fantômes.** Règle l'ordre RGB et le « panel driver » dans le menu de la ZeDMD (ou avec ZeDMD_Updater2).
- **Animation saccadée.** Monte « USB packet size » et « min refresh » dans le menu de la ZeDMD.
- **`test_panel.bat` dit que le moteur tourne déjà.** Le lancement automatique tient la dalle. Quitte ArcadeDMD depuis le menu de son icône, ou teste directement avec un jeu.

## Le moteur

- **Il s'arrête tout seul.** L'erreur est écrite dans `runtime\arcadedmd.log`.

## Demander de l'aide

Ouvre une [issue](https://github.com/Byoyoyo/ArcadeDMD/issues) avec `runtime\arcadedmd.log`. Pour un jeu qui se comporte mal, ajoute son enregistrement (voir [[Enregistrer une partie]]).
