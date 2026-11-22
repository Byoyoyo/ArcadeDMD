# Le bus d'événements d'ArcadeDMD

Ce que le jeu fait, dit une fois, pour tous les écrans. Les scènes qui suivent un jeu décident toujours seules quand quelque chose se passe. Elles le disent maintenant aussi sur un bus, avec un nom stable et des chiffres, et n'importe quel moteur de rendu peut écouter.

Protocole 1. Branché pour la famille Metal Slug (`mslug`, `mslug2`, `mslugx`, `mslug3`, `mslug4`, `mslug5` et leurs versions). Les autres jeux envoient un `hello` sans détecteur et aucun événement.

Rien n'est décidé dans le bus. Aucune adresse, aucune temporisation et aucune règle de détection n'a changé. Chaque événement est une ligne ajoutée à côté de l'effet que la scène dessinait déjà.

## 1. Ce qu'il faut savoir d'abord

- **Les valeurs viennent de la mémoire du jeu.** Un événement est la comparaison de deux lectures. Le stock de bombes baisse et le jeu compte une grenade en l'air, c'est un lancer. Le jeu ne la compte plus, elle a explosé.
- **La détection tourne encore dans la scène de l'écran HD.** Il faut que l'écran HD soit actif (`preview` en style `hd`) pour que le bus parle. La dalle LED seule ne reçoit rien pour l'instant.
- **Un moteur de rendu ne lit que le bus et les valeurs nommées.** Il ne lit aucun champ interne des scènes et n'écrit rien dedans.
- **Les noms calculés se lisent, ils ne se recodent pas.** Le soldat choisi est dans `players.<côté>.character`. L'ordre des soldats change d'un Metal Slug à l'autre.

## 2. Écouter

```python
def on_message(msg):
    if msg["type"] == "event" and msg["name"] == "mslug.grenade.thrown":
        ...

bus = engine.events                  # dmd/events.py, classe EventBus
bus.subscribe(on_message)            # le hello du jeu en cours et son dernier état arrivent d'abord
bus.last_time("mslug.shot", "p1")    # instant du dernier, -99.0 si jamais
bus.state                            # dernier état publié, ou None
```

Depuis l'écran HD, `HDRenderer.render(screen, eng)` reçoit le moteur, le bus est `eng.events`. Un abonné qui lève une exception est retiré, le moteur continue.

## 3. Messages

Des dictionnaires simples. Les mêmes s'écrivent dans un journal, un objet JSON par ligne.

```json
{"type": "hello", "protocol": 1, "arcadedmd": "1.39.2", "t": 0.0, "wall": 1795363234.773,
 "game": {"key": "mslug2", "title": "Metal Slug 2", "system": "mslug2", "parent": "",
          "family": "mslug2", "detector": "MetalSlugScene"},
 "events": ["player.join", "life.lost", "mslug.grenade.thrown"],
 "values": ["ammo", "bombs", "grenades_out", "lives", "score"]}
{"type": "state", "seq": 41, "t": 163.3, "state": {}}
{"type": "event", "seq": 42, "t": 34.8, "at": 34.8, "name": "mslug.grenade.thrown", "side": "p1",
 "data": {"count": 1, "bombs_before": 9, "bombs": 8, "synced": true, "early": 0}}
{"type": "bye", "seq": 43, "t": 1420.0, "reason": "stop"}
```

| Champ | Sens |
| --- | --- |
| `seq` | Augmente de 1 à chaque état, événement et `bye` d'un jeu. Repart de 1 à chaque `hello` |
| `t` | Instant de la détection, en secondes sur l'horloge du moteur |
| `at` | Instant où montrer l'annonce. Égal à `t`, sauf quand le moteur la programme plus tard |
| `side` | `p1` ou `p2`. Absent pour un événement du jeu |
| `data` | Nombres, booléens et codes. Jamais de texte traduit |
| `hello.events` | Tout ce que la scène de ce jeu peut dire. Liste vide, la scène ne parle pas encore sur le bus |
| `hello.values` | Les valeurs que le jeu lit. Une valeur absente de cette liste ne sera jamais dans l'état |
| `hello.wall` | L'heure réelle au temps `t` |

## 4. État de Metal Slug

Publié après chaque image où il a changé.

```json
{"mode": "game", "attract": false, "credits": 0, "time": 57,
 "stage": {"kind": "mission", "n": 1, "code": 1},
 "players": {
   "p1": {"mode": "playing", "since": 10.2, "character": "MARCO", "score": 25420, "lives": 1,
          "bombs": 15, "grenades_out": 0, "weapon": {"code": 255, "kind": "pistol"}, "ammo": 65535,
          "prisoners": 2, "moving": 1.0, "vehicle": null,
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
| `last` | Instants des derniers `mslug.shot`, `mslug.grenade.thrown` et `life.lost` de ce joueur, -99.0 si jamais |
| `stage.n` | Le numéro affiché. `code` est la valeur lue |
| `boss` | `null`, ou `name`, `hp`, `top`, `phase`, `minor` (gros ennemi sans alerte), `down`, `since` |

Une valeur que le jeu ne donne pas vaut `null`. Un rendu n'affiche jamais un zéro à sa place.

## 5. Événements de Metal Slug

| Nom | Côté | Données | Quand |
| --- | --- | --- | --- |
| `attract.begin`, `attract.end` | | | La démonstration du jeu commence ou s'arrête |
| `player.join` | oui | `kind` `start`, `join` ou `continue` | Un joueur commence, rejoint l'autre, ou revient d'un continue |
| `player.continue` | oui | | Le décompte du continue commence |
| `player.over` | oui | | Game over |
| `coin.in` | | `count`, `credits` | Les crédits montent |
| `score.gain` | oui | `gain`, `score` | Le score monte |
| `life.lost` | oui | `lives`, `before` | Une vie perdue |
| `life.gained` | oui | `lives` | Une vie gagnée en jeu. Jamais les vies d'un départ ou d'un continue |
| `stage.clear` | | `kind`, `n`, `code`, `source` `game` ou `next` | Mission accomplie, dite par le jeu ou déduite du passage à la suivante |
| `stage.begin` | | `kind`, `n`, `code` | Mission suivante. `at` vaut `t` + 1,9 s quand la fin vient d'être déduite |
| `weapon.change` | oui | `code`, `kind`, `ammo` | L'arme change. `kind` `pistol` au retour au pistolet |
| `ammo.gain` | oui | `gain`, `ammo` | Munitions ramassées |
| `mslug.shot` | oui | `count`, `weapon`, `source` `ammo` ou `button` | Tirs. Les munitions baissent, ou le bouton de tir au pistolet |
| `mslug.grenade.thrown` | oui | `count` (4 au plus), `bombs_before`, `bombs`, `synced`, `early` | Des grenades sont lancées |
| `mslug.grenade.exploded` | oui | `count` | Le jeu dit que des grenades ont explosé |
| `mslug.bombs.found` | oui | `gain`, `bombs` | Dix bombes trouvées dans une caisse. Jamais celles d'une nouvelle vie |
| `mslug.prisoner` | oui | `count`, `prisoners` | Prisonniers libérés |
| `mslug.vehicle.in` | oui | `kind` | Le soldat monte dans un véhicule |
| `mslug.vehicle.out` | oui | `kind`, `hp`, `destroyed` | Il en sort, ou le véhicule est détruit |
| `mslug.vehicle.hit` | oui | `hp` | Le véhicule est touché |
| `mslug.vehicle.shell` | oui | `count` (3 au plus), `ammo` | Obus tirés |
| `mslug.vehicle.vulcan` | oui | | La mitrailleuse du véhicule, au bouton de tir |
| `boss.warning` | | `name`, `hp`, `top`, `phase`, `mission` | Le boss de la mission arrive |
| `boss.bar` | | idem | La barre du boss revient sans nouvelle alerte |
| `boss.hit` | | idem | Sa vie baisse |
| `boss.phase` | | idem | Sa vie remonte, phase suivante |
| `boss.destroyed` | | idem | Il tombe |
| `enemy.big` | | idem, `name` vide | Un gros ennemi reçoit une barre discrète |
| `enemy.big.hit`, `enemy.big.destroyed` | | idem | Il est touché, il tombe |
| `enemy.big.gone` | | | Sa barre s'efface sans qu'il soit tombé |
| `game.pause`, `game.resume` | | | L'émulateur est mis en pause, puis repris |

### Dessiner une grenade

- `synced` vrai. Le jeu compte ses grenades. Chaque grenade vole et attend `mslug.grenade.exploded`. Sans nouvelle au bout de 2 s, elle explose seule.
- `synced` faux. Le jeu ne les compte pas à ce moment. Elle vole 0,62 s, rebondit et explose en retombant, environ une seconde après le lancer.
- `early` grenades du lancer ont déjà explosé dans le jeu. Elles explosent à la main, sans vol.
- Les grenades d'un même lancer partent l'une après l'autre, toutes les 0,16 s.
- Un `mslug.grenade.exploded` vaut pour les grenades les plus anciennes encore en vol. Reçu pour une grenade pas encore partie, il la fait exploser dès son départ.
- Le jeu retire sa grenade du compte quand elle explose, sur un ennemi tout de suite ou au deuxième rebond. Le bus sait quand elle explose, pas où.

Sur une partie réelle à deux joueurs, le lancer et l'explosion sont séparés de 0,4 s quand la grenade touche un ennemi, de 0,9 s quand elle va au bout de ses rebonds.

## 6. Dalle LED

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

## 7. Journal

```json
"events": {"journal": true}
```

Chaque partie écrit alors `runtime/events/<jeu>-<date>.jsonl`, un message par ligne. Éteint par défaut.

## 8. Travailler sans borne

`tests/captures` contient 21 parties réelles de Metal Slug. Elles se rejouent sans émulateur et sans écran.

```bash
python tools/events_check.py --jsonl out      # le flux complet de chaque partie, dans out/
python tools/events_check.py                  # contrôle contre les références de tests/events
```

Le contrôle échoue si un seul événement change de nom, de chiffres ou d'instant. Il vérifie aussi ce sur quoi un rendu compte, un `hello` en premier, des `seq` qui se suivent, des temps qui ne reculent pas, un `at` jamais avant son `t`, aucun nom hors de `hello.events`. Après un changement voulu, `python tools/events_check.py --write` réécrit les références.

## 9. Limites connues

- La détection dépend encore de l'écran HD (point 1).
- `coin.in` vient des crédits lus. Une pièce vue seulement aux boutons de la borne n'y est pas.
- La première mission d'une partie n'a pas de `stage.begin`. Elle est dans l'état.
- `t` est l'instant où le moteur a vu la lecture, pas celui de l'image du jeu. Le retard est celui de la lecture, 0,1 à 0,2 s sur une borne.
- Sans `grenades_out` (très anciennes captures), tous les lancers ont `synced` faux.
