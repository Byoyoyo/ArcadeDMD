# Le bus d'événements d'ArcadeDMD

Ce que le jeu fait, dit une fois, pour tous les écrans. Les scènes qui suivent un jeu décident toujours seules quand quelque chose se passe. Elles le disent maintenant aussi sur un bus, avec un nom stable et des chiffres, et n'importe quel moteur de rendu peut écouter.

Protocole 1. Branché pour la famille Metal Slug (`mslug`, `mslug2`, `mslugx`, `mslug3`, `mslug4`, `mslug5` et leurs versions). Les autres jeux envoient un `hello` sans détecteur et aucun événement.

Rien n'est décidé dans le bus. Aucune adresse, aucune temporisation et aucune règle de détection n'a changé. Chaque événement est une ligne ajoutée à côté de l'effet que la scène dessinait déjà. Le code d'origine de la scène Metal Slug n'a reçu que des ajouts, aucune ligne retirée ni modifiée.

## 1. Ce qu'il faut savoir d'abord

- **Les valeurs viennent de la mémoire du jeu.** Un événement est la comparaison de deux lectures. Le stock de bombes baisse et le jeu compte une grenade en l'air, c'est un lancer. Le jeu ne la compte plus, elle a explosé.
- **L'interface ne dépend ni de pygame ni des scènes.** Un moteur de rendu reçoit des dictionnaires. Il ne lit aucun champ interne d'une scène et n'écrit rien dedans.
- **La détection tourne encore dans la scène de l'écran HD.** Il faut que l'écran HD soit actif (`preview` en style `hd`) pour que le bus parle. Sortir ce code de la scène est l'étape suivante (chapitre 11).
- **Les noms calculés se lisent, ils ne se recodent pas.** Le soldat choisi est dans `players.<côté>.character`. L'ordre des soldats change d'un Metal Slug à l'autre.

## 2. Écouter

```python
def on_message(msg):
    if msg["type"] == "event" and msg["name"] == "mslug.grenade.burst":
        ...

bus = engine.events                  # dmd/events.py, classe EventBus
bus.subscribe(on_message)            # le hello du jeu en cours et son dernier état arrivent d'abord
bus.last_time("mslug.shot", "p1")    # instant du dernier, -99.0 si jamais
bus.state                            # dernier état publié, ou None
```

Depuis l'écran HD, `HDRenderer.render(screen, eng)` reçoit le moteur, le bus est `eng.events`. Un abonné qui lève une exception est retiré, le moteur continue.

`tools/events_example.py` est un moteur de rendu complet en une classe, qui écrit en mots ce qu'il dessinerait. `python tools/events_example.py` le fait tourner sur une partie réelle.

## 3. Messages

Des dictionnaires simples. Les mêmes s'écrivent dans un journal, un objet JSON par ligne.

```json
{"type": "hello", "protocol": 1, "arcadedmd": "1.39.2", "session": "cc6a760cfb87", "t": 0.0, "wall": 1795364344.475,
 "game": {"key": "mslug2", "title": "Metal Slug 2", "system": "mslug2", "parent": "",
          "family": "mslug2", "detector": "MetalSlugScene"},
 "events": ["player.join", "life.lost", "mslug.grenade.thrown"],
 "values": ["ammo", "bombs", "grenades_out", "lives", "score"]}
{"type": "state", "seq": 82, "t": 34.8, "state": {}}
{"type": "event", "seq": 83, "id": "cc6a760cfb87:83", "t": 34.8, "at": 34.8, "name": "mslug.grenade.thrown",
 "side": "p1", "basis": "read",
 "data": {"count": 1, "bombs_before": 9, "bombs": 8, "synced": true, "early": 0, "ids": ["p1-2"]}}
{"type": "bye", "seq": 4712, "t": 1049.0, "reason": "stop"}
```

| Champ | Sens |
| --- | --- |
| `session` | Un nom pour cette partie du jeu, différent à chaque `hello` |
| `seq` | Augmente de 1 à chaque état, événement et `bye`. Repart de 1 à chaque `hello` |
| `id` | La session puis `seq`. Nomme une occurrence une fois pour toutes. Le même `id`, c'est le même événement, à ne dessiner qu'une fois |
| `t` | Instant de la détection, en secondes sur l'horloge du moteur |
| `at` | Instant prévu pour le montrer. Égal à `t`, sauf quand le moteur programme l'annonce plus tard. Le rendu ne recalcule aucun délai |
| `side` | `p1` ou `p2`. Absent pour un événement du jeu |
| `basis` | D'où vient l'événement, voir le tableau suivant |
| `data` | Nombres, booléens et codes. Jamais de texte traduit |
| `hello.events` | Tout ce que la scène de ce jeu peut dire. Liste vide, la scène ne parle pas encore sur le bus |
| `hello.values` | Les valeurs que le jeu lit. Une valeur absente de cette liste ne sera jamais dans l'état |
| `hello.wall` | L'heure réelle au temps `t` |

| `basis` | Sens |
| --- | --- |
| `read` | Une valeur du jeu a changé, et l'événement est ce changement. Confirmé par la mémoire |
| `deduced` | Une règle sur plusieurs lectures, ou un seuil. Juste dans les parties enregistrées, mais c'est une déduction |
| `timed` | Un instant fixé par l'horloge d'ArcadeDMD, pas par le jeu. Une estimation |

## 4. Pause, changement de jeu, redémarrage

| Cas | Ce que le bus envoie | Ce que le rendu fait |
| --- | --- | --- |
| Pause de l'émulateur | `game.pause`, puis `game.resume` à la reprise. Entre les deux aucune lecture n'arrive, donc rien d'autre | Il fige ses animations. Les instants déjà annoncés ne sont pas décalés par le bus, le rendu les décale de la durée de la pause s'il veut les rejouer |
| Le jeu s'arrête | `bye` avec `reason` `stop` | Il lâche tout ce qu'il tenait pour ce jeu, grenades en vol comprises |
| Un autre jeu commence, ou le même est relancé | `bye` avec `reason` `next`, puis un nouveau `hello` | Idem. Nouvelle `session`, `seq` repart de 1, les numéros de grenades repartent de 1 |
| ArcadeDMD redémarre | Rien pour l'ancien programme. Un `hello` au jeu suivant | Un `hello` vaut toujours remise à zéro |
| Un abonné arrive en cours de partie | Le `hello` de la partie puis son dernier état | Il n'a pas les événements passés. `bus.recent` garde les 512 derniers |
| Plus de nouvelles de l'émulateur pendant 8 s | `bye` | Idem |

Pendant la démonstration du jeu, seuls `attract.*` et `coin.in` sont envoyés. À l'arrivée d'un joueur, son `player.join` part tout de suite, puis aucune valeur n'est comparée pendant sa mise en place (entre 0,8 et 10 s, jusqu'à ce que le chrono de la mission tourne).

## 5. État de Metal Slug

Publié après chaque image où il a changé.

```json
{"mode": "game", "attract": false, "credits": 0, "time": 57,
 "stage": {"kind": "mission", "n": 1, "code": 1},
 "players": {
   "p1": {"mode": "playing", "since": 10.2, "character": "MARCO", "score": 25420, "lives": 1,
          "bombs": 15, "grenades_out": 1, "weapon": {"code": 255, "kind": "pistol"}, "ammo": 65535,
          "prisoners": 2, "moving": 1.0, "vehicle": null,
          "grenades": {"waiting": [], "flying": ["p1-12"]},
          "last": {"shot": 163.1, "grenade": 150.6, "hit": -99.0}},
   "p2": {"mode": "out"}},
 "boss": null}
```

| Champ | Sens |
| --- | --- |
| `attract` | La démonstration du jeu tourne, personne ne joue |
| `players.<côté>.mode` | `out`, `playing`, `continue` (décompte), `over` |
| `since` | Début de sa partie ou de son dernier crédit |
| `character` | Le soldat choisi, tel que le jeu le dit. `null` si le jeu ne le donne pas |
| `weapon.kind` | `pistol`, `shotgun`, `flame`, `rocket`, `mg`, `laser`, `gun`, `mg2` |
| `ammo` | 65535 pour le pistolet, munitions sans fin |
| `moving` | 1.0 vers la droite, -1.0 vers la gauche, 0.0 à l'arrêt, d'après le manche |
| `vehicle` | `null` à pied, sinon `kind` (`tank`, `camel`, `slugnoid`, `flyer`, `copter`, `mariner`, `drill`, `astro`, `gunner`, ou `vehicle` quand le genre n'est pas connu), `hp`, `ammo` |
| `grenades` | `waiting`, lancées et pas encore parties. `flying`, en vol, la plus ancienne d'abord |
| `last` | Instants des derniers `mslug.shot`, `mslug.grenade.thrown` et `life.lost` de ce joueur, -99.0 si jamais |
| `stage.n` | Le numéro affiché. `code` est la valeur lue |
| `boss` | `null`, ou `name`, `hp`, `top`, `phase`, `minor` (gros ennemi sans alerte), `down`, `since` |

Une valeur que le jeu ne donne pas vaut `null`. Un rendu n'affiche jamais un zéro à sa place.

## 6. Événements de Metal Slug

| Nom | Côté | Données | Quand | `basis` |
| --- | --- | --- | --- | --- |
| `attract.begin`, `attract.end` | | | La démonstration du jeu commence ou s'arrête | `read` |
| `player.join` | oui | `kind` `start`, `join` ou `continue` | Un joueur commence, rejoint l'autre, ou revient d'un continue | `read` |
| `player.continue` | oui | | Le décompte du continue commence | `read` |
| `player.over` | oui | | Game over | `read` |
| `coin.in` | | `count`, `credits` | Les crédits montent | `read` |
| `score.gain` | oui | `gain`, `score` | Le score monte | `read` |
| `life.lost` | oui | `lives`, `before` | Une vie perdue | `read` |
| `life.gained` | oui | `lives` | Une vie gagnée en jeu. Jamais les vies d'un départ ou d'un continue | `read` |
| `stage.clear` | | `kind`, `n`, `code`, `source` | Mission accomplie. `source` `game`, le jeu le dit. `source` `next`, déduit du passage à la suivante | `read` ou `deduced` |
| `stage.begin` | | `kind`, `n`, `code` | Mission suivante. `at` vaut `t` + 1,9 s quand la fin vient d'être déduite | `read` |
| `weapon.change` | oui | `code`, `kind`, `ammo` | L'arme change. `kind` `pistol` au retour au pistolet | `read` |
| `ammo.gain` | oui | `gain`, `ammo` | Munitions ramassées | `read` |
| `mslug.shot` | oui | `count`, `weapon`, `source` | Tirs. `source` `ammo`, les munitions baissent. `source` `button`, le bouton de tir au pistolet | `read` ou `deduced` |
| `mslug.grenade.thrown` | oui | `count` (4 au plus), `bombs_before`, `bombs`, `synced`, `early`, `ids` | Des grenades sont lancées | `read` si le jeu a compté chacune en l'air, sinon `deduced` |
| `mslug.grenade.launch` | oui | `id` | Une grenade quitte la rangée | `timed` |
| `mslug.grenade.exploded` | oui | `count`, `ids` | Le jeu dit que des grenades ont explosé | `read` |
| `mslug.grenade.burst` | oui | `id`, `cause` | Une grenade explose à l'écran | selon `cause` |
| `mslug.bombs.found` | oui | `gain`, `bombs` | Dix bombes trouvées dans une caisse. Jamais celles d'une nouvelle vie | `deduced` |
| `mslug.prisoner` | oui | `count`, `prisoners` | Prisonniers libérés | `read` |
| `mslug.vehicle.in` | oui | `kind` | Le soldat monte dans un véhicule | `read` |
| `mslug.vehicle.out` | oui | `kind`, `hp`, `destroyed` | Il en sort, ou le véhicule est détruit | `read` |
| `mslug.vehicle.hit` | oui | `hp` | Le véhicule est touché | `read` |
| `mslug.vehicle.shell` | oui | `count` (3 au plus), `ammo` | Obus tirés | `read` |
| `mslug.vehicle.vulcan` | oui | | La mitrailleuse du véhicule, au bouton de tir | `deduced` |
| `boss.warning` | | `name`, `hp`, `top`, `phase`, `mission` | Le boss de la mission arrive | `deduced` |
| `boss.bar` | | idem | La barre du boss revient sans nouvelle alerte | `deduced` |
| `boss.hit` | | idem | Sa vie baisse | `deduced` |
| `boss.phase` | | idem | Sa vie remonte, phase suivante | `deduced` |
| `boss.destroyed` | | idem | Il tombe | `deduced` |
| `enemy.big` | | idem, `name` vide | Un gros ennemi reçoit une barre discrète | `deduced` |
| `enemy.big.hit`, `enemy.big.destroyed` | | idem | Il est touché, il tombe | `deduced` |
| `enemy.big.gone` | | | Sa barre s'efface sans qu'il soit tombé | `deduced` |
| `game.pause`, `game.resume` | | | L'émulateur est mis en pause, puis repris | `read` |

Les boss sont `deduced` parce que le jeu ne dit pas « voici le boss ». Leur vie est lue dans la mémoire, et c'est une règle (une grosse vie qui remplit une case pendant la mission, comparée à la vie connue du boss) qui dit que c'est lui.

## 7. Les grenades

Chaque grenade porte un numéro, `p1-12` pour la douzième du joueur 1. Sa vie tient en trois événements.

| Étape | Événement | Instant |
| --- | --- | --- |
| Lancée | `mslug.grenade.thrown`, avec les numéros du lancer dans `ids` | La lecture où le stock de bombes baisse |
| Elle part | `mslug.grenade.launch`, une par grenade | Les grenades d'un lancer partent toutes les 0,16 s |
| Elle explose | `mslug.grenade.burst`, une par grenade, avec sa `cause` | L'image même où le marquee actuel la fait exploser |

Un moteur de rendu qui fait partir sa grenade à `launch` et la fait exploser à `burst` explose au même instant que le marquee actuel. Ces deux événements sortent des fonctions qui font partir et exploser la grenade de l'écran HD.

| `cause` | Ce qui s'est passé | `basis` |
| --- | --- | --- |
| `game` | Le jeu a retiré une grenade de son compte. Sur un ennemi tout de suite, ou au deuxième rebond, c'est le jeu qui décide | `read` |
| `early` | La grenade du jeu avait déjà explosé quand le lancer a été vu. Elle explose à la main, dès son départ | `deduced` |
| `landed` | Le jeu ne comptait pas ses grenades à ce moment. Elle vole 0,62 s, rebondit et explose en retombant, environ une seconde après son départ | `timed` |
| `timeout` | Le jeu compte ses grenades mais n'a rien dit. Elle explose seule au bout de 2 s. Chaque nouveau lancer repousse cette attente pour les grenades en vol | `timed` |

`mslug.grenade.exploded` est ce que le jeu dit, un nombre. `ids` nomme les grenades en vol à qui l'explosion est attribuée, les plus anciennes d'abord. Si `count` dépasse la longueur de `ids`, le reste vaut pour des grenades pas encore parties, qui exploseront `early` à leur départ. Chaque grenade nommée a son `burst` dans la même image.

Limites de précision, à ne pas présenter comme des certitudes.

- Le jeu donne un nombre de grenades en l'air, pas laquelle a explosé. Avec plusieurs grenades en vol, « la plus ancienne d'abord » est une règle. Le nombre d'explosions et leurs instants sont justes, l'attribution à une grenade précise est une convention.
- Le bus sait quand une grenade explose, pas où. Il ne distingue pas le sol d'un ennemi. Une explosion rapide après le départ est sur un ennemi, une explosion vers une seconde est le deuxième rebond.
- Les rebonds ne sont pas lus. Le rebond du marquee actuel est une mise en scène calée sur la durée du jeu.
- `t` est l'instant où le moteur a vu la lecture. Le retard sur le jeu est celui de la lecture, 0,1 à 0,2 s sur une borne.
- Deux lancers qui se chevauchent prennent leurs numéros dans l'ordre des départs. `launch` donne l'instant exact de chaque grenade.

Mesuré sur les 21 parties réelles. 947 grenades, dont 365 explosées sur l'ordre du jeu, 337 au deuxième rebond, 66 après l'attente et 179 à la main. Entre le départ et l'explosion dite par le jeu, de 0,1 à 3,4 s, la moitié sous 0,6 s.

## 8. Dalle LED

Un moteur de rendu peut dessiner la dalle de certains jeux à la place de la scène du fichier de jeu.

```python
from dmd import events
from dmd.hd_mslug import family

def factory(engine):
    def paint(canvas, engine, now):          # canvas : dmd/canvas.py, 128 x 32
        state = engine.events.state
        if state is None:
            return False                     # cette image reste à la scène habituelle
        canvas.clear((0, 0, 0))
        ...
        return True
    return paint

events.led_painter(family, factory)          # family(key) dit si le jeu est un Metal Slug
```

Dans `config.json`.

```json
"visual": {"enabled": true, "led": true, "modules": ["dmd.mon_moteur_led"]}
```

| Règle | Détail |
| --- | --- |
| Par défaut | `visual` absent ou `enabled` faux, rien ne change |
| Repli | Si `paint` rend faux ou lève une exception, la scène du fichier de jeu dessine. Après une exception le moteur de rendu est retiré jusqu'au jeu suivant |
| Taille | 128 x 32 points. Des dessins faits à cette taille, pas des images HD réduites |
| Cadence | 30 images par seconde au plus vers la dalle |
| Canevas | `clear`, `set`, `add`, `blend`, `fill_rect`, `hline`, `vline`, `text`, `sprite`, `dim` |

## 9. Journal et travail sans borne

```json
"events": {"journal": true}
```

Chaque partie écrit alors `runtime/events/<jeu>-<date>.jsonl`, un message par ligne. Éteint par défaut.

`tests/captures` contient 21 parties réelles de Metal Slug. Elles se rejouent sans émulateur et sans écran.

```bash
python tools/events_check.py --jsonl out      # le flux complet de chaque partie, dans out/
python tools/events_example.py                # l'exemple de moteur de rendu sur une partie
```

## 10. Tests de non-régression

`python tools/events_check.py` tourne dans le contrôle de chaque demande de fusion. Il rejoue les 21 parties réelles et compare le flux d'événements à ses références (`tests/events`). Il échoue si un seul événement change de nom, de chiffres ou d'instant. Après un changement voulu, `--write` réécrit les références.

| Contrôle | Résultat |
| --- | --- |
| Annonces, explosions et bandeaux du marquee actuel, avant et après l'ajout du bus, sur 27 parties (21 réelles, 6 du robot) | Identiques, image pour image. 2549 explosions aux mêmes instants |
| Le même flux d'un passage à l'autre | Identique sur les 21 parties |
| Ordre des messages | Un `hello` en premier, des `seq` qui se suivent, des temps qui ne reculent pas, un `at` jamais avant son `t`, aucun nom hors de `hello.events`, un `id` par événement |
| Cycle de vie des grenades | 947 grenades. Chacune lancée, partie et explosée une fois, dans cet ordre |
| Correction de la 1.39.2, les vies | 42 départs, 4 arrivées d'un second joueur, 70 continues. Aucune vie annoncée |
| Correction de la 1.39.2, les bombes | 45 caisses annoncées. Aucune annonce de dix bombes avec une nouvelle vie ou une nouvelle mission |
| Le bus sans jeu | Rien hors d'une partie, un abonné en panne est retiré sans gêner les autres, l'état n'est envoyé que s'il change |
| La dalle LED | Un moteur de rendu branché la dessine. S'il échoue, la scène du fichier de jeu reprend |
| Toutes les scènes HD | Les 301 jeux jouent leur partie inventée, un joueur puis deux |

Total des 21 parties. 2 h 27 de jeu, 28 439 événements, 18 alertes de boss, 17 boss détruits, 6 changements de phase, 171 vies perdues.

## 11. Ce qui reste à faire

| Sujet | État |
| --- | --- |
| Sortir la détection de la scène HD | Pas fait. Le code de détection est à sa place d'origine, intact. Le déplacer dans un détecteur sans pygame permettra au bus de parler sans écran HD. Les références de `tests/events` sont le filet de cette étape, le flux doit rester le même |
| Les autres familles | Pas sur le bus. Combat, boss des autres jeux, shoot'em up, puis le reste |
| `coin.in` | Vient des crédits lus. Une pièce vue seulement aux boutons de la borne n'y est pas |
| Première mission d'une partie | Pas de `stage.begin`. Elle est dans l'état |
| Ce que la mémoire lue ne donne pas | Où une grenade explose, les rebonds, les ennemis tués un par un (seul le score monte), le saut et l'accroupi du soldat |
| Très anciennes captures | Sans `grenades_out`, tous les lancers ont `synced` faux et explosent `landed` |
