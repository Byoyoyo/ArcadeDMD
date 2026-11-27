ArcadeDMD annonce sur le fronton les succès que tu débloques sur [RetroAchievements](https://retroachievements.org) pendant que tu joues. Nouveau en 1.41.

## Ce qui s'affiche

Quand un succès est débloqué, un bandeau s'ouvre sur toute la largeur du marquee HD pendant six secondes, quelle que soit la scène. Il donne le nom du succès, ses points et le nombre de succès du jeu que tu as maintenant, et ce compteur gagne un cran. Pendant un combat le bandeau vient en haut, pour que les barres de vie restent en vue. Ailleurs il prend le milieu. La dalle LED affiche le nom sur une ligne.

## Régler le compte

1. Dans l'émulateur, connecte-toi à ton compte RetroAchievements. Dans RetroArch c'est dans Réglages, Succès. C'est l'émulateur qui débloque les succès, ArcadeDMD ne fait que les annoncer.
2. Sur retroachievements.org, ouvre les réglages de ton compte et copie la **clé web API** de la section Keys.
3. Dans la fenêtre d'ArcadeDMD, ouvre l'onglet **Succès**. Tape ton nom d'utilisateur, colle la clé, coche la case et clique sur **Essayer le compte**. Le site répond avec ton nom et tes points.
4. Enregistre. ArcadeDMD repart avec le compte.

ArcadeDMD ne demande jamais ton mot de passe. La clé reste dans `config.json` sur ton PC. Elle n'est écrite ni dans le journal ni dans les enregistrements, et la fenêtre ne la renvoie jamais dans sa page. **Oublier la clé** la retire.

## Bon à savoir

- ArcadeDMD interroge le site toutes les 15 secondes pendant une partie, et encore une minute et demie après la fermeture du jeu. Le bandeau arrive dans ces 15 secondes, le temps que l'émulateur prévienne le site et qu'ArcadeDMD demande.
- Rien n'est demandé tant qu'aucun jeu ne tourne.
- Ce que tu avais débloqué avant de lancer le jeu n'est pas annoncé.
- Sans Internet, ou quand le site ne répond pas, le jeu et le marquee continuent. Le journal le dit une fois et ArcadeDMD réessaie.
- Quand ArcadeDMD démarre avec le compte réglé, le journal dit `RetroAchievements : le site répond pour` et ton nom.

## À la main

L'onglet écrit cette partie de `config.json`.

```json
"retroachievements": {"enabled": true, "user": "TonNom", "key": "ta clé web API", "every": 15}
```

`every` est le nombre de secondes entre deux questions au site, jamais moins de 10.
