## Ajouter un jeu ou modifier une scène

1. Copie `games\aburner2.json` sous le nom court du jeu, par exemple `games\outrun.json`.
2. Change `"match"` (`"system": ["outrun"]`), le titre et les valeurs.
3. Trouve les adresses avec `learn.bat` (sans fichier dédié, l'outil crée le fichier pour toi).
4. Modifie la scène. Le moteur recharge les fichiers à chaud, pas besoin de relancer pendant que tu ajustes.

Formats de valeurs reconnus

| `type` | Signification |
|---|---|
| `u8` | un octet |
| `u16` / `u32` / `s8` / `s16` / `s32` | un octet (`s8`), deux ou quatre octets dans l'ordre du processeur, `s` pour un nombre signé (la vie d'un boss qui passe sous zéro) |
| `be` / `le` | binaire sur `bytes` octets, ordre normal ou inversé |
| `bcd` / `bcd_le` | BCD sur `bytes` octets (deux chiffres par octet) |
| `digits` | un chiffre par octet (`digit_offset` 0x30 pour de l'ASCII) |

Options communes, `mult` (score stocké divisé par 10, très fréquent), `add`, `min`, `max`, `mask`, `shift`. `valid` donne les valeurs que le jeu peut vraiment avoir, `[1, 6]` pour les six missions de Metal Slug. Une autre valeur lue est écartée et la dernière bonne reste, la RAM d'un jeu qui démarre n'affiche rien de faux. `learn_ranges` limite la zone capturée par l'outil d'apprentissage. `hold_zero` (en secondes) garde le dernier score affiché quand la valeur lue tombe à 0 un instant en pleine partie, le temps que le jeu recrée le combattant entre deux rounds.

Pour une valeur rangée dans un objet qui change de place en mémoire (les combattants de Samurai Shodown à chaque round), `"ptr"` donne l'adresse où lire la position de l'objet (32 bits) et `"addr"` devient le décalage dans l'objet. `"ptr_range"` écarte un pointeur pas encore prêt. `learn.bat` écrit ce genre de valeur tout seul quand les captures montrent que la valeur suit l'objet.

Certains noms de valeurs ont un rôle particulier dans les scènes HD. `stage`, `backdrop` et `mission` changent le décor ([[Marquee HD]]), `p1_input` et `p2_input` sont le stick et les boutons lus par le BIOS Neo Geo (tirs au pistolet des Metal Slug, vaisseaux de Blazing Star, de Pulstar et de Last Resort, avions des Aero Fighters, chasseurs de Top Hunter, flèche de Puzzle Bobble, fou de Magical Drop III).

`"derived"` calcule une valeur à partir d'autres, par exemple le nom du personnage. `"value"` reprend une valeur lue, `"pick"` choisit dans une liste selon `"at"`, `"names"` change un numéro en texte. `"sum"` additionne des valeurs, `"ge"` donne 1 quand la première atteint la seconde et 0 sinon. `"eq"` donne 1 quand les deux sont égales et 0 sinon, `"first"` la première de ses valeurs qui est connue. `"rise"` donne 1 tant que sa valeur vaut 1, une fois que `"from"` a valu 1 depuis le dernier `"reset"`, la seule qui se souvienne d'une lecture à l'autre (le boss de DoDonPachi, une fois son niveau vu défiler vers lui en pleine partie, dans `games\ddonpach.json`). `"names"` peut aussi avoir une liste par langue, `{"en": [...], "fr": [...]}`, comme dans `games\wjammers.json`. Voir `games\samsho2.json` et `games\kof98.json`.

Éléments de scène

| `type` | Rôle | Réglages principaux |
|---|---|---|
| `marquee` | texte qui défile | `text` ou `segments` (morceaux de couleurs différentes), `font`, `y`, `speed`, `gap`, `color`, `accent_initials` |
| `text` | texte fixe ou valeur | `text` avec `{score}`, `x`, `y`, `align`, `segments`, `flash` |
| `cycle` | alterne plusieurs pages | `period`, `pages` |
| `bars` | herbe ou égaliseur | `x`, `w`, `min`, `max`, `color`, `tip`, `flowers` |
| `waves` | collines qui défilent en fond | `layers` (`y`, `amp`, `speed`, `color`, `edge`) |
| `mountains` | montagnes pleines et ligne de sol (style Vera) | `peaks` (`[x, hauteur]`), `floor`, `color`, `ground`, `speed` |
| `particles` | missiles et gerbes quand une valeur monte | `rate`, `color`, `y`, `burst` |
| `anim` | une animation jouée une fois quand une valeur change (une explosion quand le score monte) | `image` (liste, le premier fichier trouvé, `{game}` pour le jeu), `on`, `change` (`up`, `down`, `any`), `ratio` (petit ou gros gain), `x` et `y` (un nombre, `[début, fin]`, ou plusieurs `[début, fin]` au choix), `near` et `ahead` (devant un `ship`), `count`, `spread`, `delay`, `ms`, `black` |
| `events` | des événements courts qui prennent la dalle un instant, un à la fois, comme sur un flipper (BOMBE!, POWER UP, une vie perdue, GAME OVER) | `events`, une liste. Chacun a `on`, `change`, `step` (la taille du changement), `from` et `to` (les valeurs avant et après), `when`, `text` (avec `{lives}`...), `color`, `font` (sa plus grande taille, il grandit jusqu'à elle), `y`, `icon` et `colors` (un petit dessin à gauche du texte), `icon_scale`, `anim` (des animations jouées au départ, mêmes clés que `anim`), `text_delay`, `ms`, `clear` (`false` garde la scène derrière), `priority` (un événement plus important remplace celui en cours, un moins important attend) |
| `sprite` | sprite animé (PNG en bande ou GIF) | `image`, `frames`, `mode` (`pass`, `pingpong`, `fixed`), `dim` (luminosité), `alpha`, `shoot` (tire quand une valeur monte) |
| `gauge` | barre de vie | `var`, `max` (un nombre, ou `"peak"` pour la plus haute valeur vue pendant qu'elle s'affiche, la vie d'un boss, gardée `peak_hold` secondes quand elle est cachée), `x`, `y`, `w`, `h`, `anchor` (côté accroché), `color`, `low`, `back`, `border`, `bevel` (liseré clair en bas et à droite) |
| `clock` | horloge | `format`, `font` |
| `icons` | un petit dessin répété selon une valeur (vies en vaisseaux, niveaux de puissance) | `var`, `pattern` (lignes de caractères, `.` pour le vide), `colors`, `max`, `gap`, `empty` (couleur des cases restantes), `align`, `flash` |
| `counter` | un petit dessin suivi d'un nombre (un avion et x3 pour les vies) | `var`, `pattern`, `colors`, `font`, `color` (du nombre), `prefix` (`x`), `align` (`left` à partir de `x`, `right` jusqu'à `x`), `max` (au-dessus rien ne s'affiche, une valeur que le jeu n'a pas encore posée), `flash` |
| `ship` | le vaisseau du joueur, qui suit le stick et tire tant que le bouton A est tenu (`p1_input`), ou vole tout seul | `image` (liste, `{game}` pour le jeu), `frames`, `fps`, `face` (`right`, ou `left` pour le joueur 2 face au joueur 1), `area` (`[x0, y0, x1, y1]`), `input`, `speed`, `fire` (`color`, `speed`, `rate`, `len`), `shoot_on` (tire quand le score monte), `anchor` (pour qu'une couche `anim` avec `near` parte devant lui), `hit` et `unless` (un ennemi explose de temps en temps tant que le score n'est pas connu) |
| `dot` | un disque dont la couleur vient d'une valeur (bulles de Puzzle Bobble), ou toujours la première couleur sans `var` (une lune) | `var`, `colors` (une couleur par valeur), `x`, `y`, `r`, `rim`, `shine` |
| `arrow` | une flèche qui tourne selon une valeur (vent de Neo Turf Masters) | `var`, `steps` (16, 0 vers le haut puis dans le sens des aiguilles d'une montre), `x`, `y`, `len`, `color`, `ring`, `flash` |
| `image`, `rect` | image fixe, rectangle | |

Polices disponibles `4x6`, `5x8`, `6x10`, `6x13`, `7x14`, `7x14B`, `8x13B`, `9x15B`. Le `y` d'un texte correspond au haut des majuscules. `when` affiche un élément sous condition, par exemple `{"has": "credits"}` ou `{"var": "mode", "eq": 12}`.

La section `"demo"` donne les valeurs de départ des démos (`demo_neogeo.bat`, `python arcadedmd.py demo <jeu>`). `"attract": true` commence sur l'écran des pièces, puis deux pièces et START. `"sim"` fait bouger les valeurs propres au jeu, une entrée par valeur, avec `"cycle"` (une liste prise à tour de rôle), `"count"` (`[min, max, pas]`, retour au début à la fin) ou `"random"` (`[min, max]`), `"every"` (secondes, ou `[min, max]`) et `"start"` (premier changement). Voir `games\wjammers.json`.
