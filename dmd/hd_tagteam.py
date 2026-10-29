"""Tag team fights on the HD screen (Marvel vs. Capcom 2): three characters per team, one on point.

Rests on the fighting scene of hd.py and its effects (hd_fight.py). The game file says in "hd": {"tag_team": {...}}
which values hold each character ([name, standing, on point], three per team), the hyper combo gauge of each team and
the value that tells a match is on:
  "tag_team": {"in_match": "in_match", "level": ["p1_level", "p2_level"], "level_max": 5,
               "p1": [["p1a_name", "p1a_up", "_p1a_on"], ...], "p2": [...]}
Under the names, the three characters of each team, the one on point lit, those KO struck out. Under the health bars,
the hyper combo gauge in pips. A gauge that goes down is a hyper combo, its banner slams in. A character KO is not the
end of the match: WIN and the confetti wait until the three characters of a team are down (none at the time out, TIME
OVER as the game says it). Out of a match, the logo.

Combats par équipes sur l'écran HD (Marvel vs. Capcom 2) : trois personnages par équipe, un seul au point. Sous les
noms, les trois personnages de chaque équipe, celui au point allumé, ceux mis KO barrés. Sous les barres de vie, la
jauge d'hyper combo en crans. Une jauge qui baisse est un hyper combo. Un personnage KO n'est pas la fin du match, WIN
et les confettis attendent que les trois personnages d'une équipe soient à terre (rien au temps écoulé, TIME OVER comme
le dit le jeu). Hors match, le logo."""

import math

HYPER = (64, 200, 255)
HYPER_DIM = (22, 48, 70)


def spec_of(game):
    hd = (game or {}).get("hd")
    s = hd.get("tag_team") if isinstance(hd, dict) else None
    return s if isinstance(s, dict) else None


def in_match(vals, spec):
    return vals.get(spec.get("in_match") or "in_match") == 1


def team(vals, spec, side):
    """[(name, state)] for a team, state "now" on point, "next" waiting, "done" KO, or None while not known."""
    rows = spec.get(side)
    if not isinstance(rows, list) or not rows:
        return None
    out = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 3:
            return None
        name, up, on = vals.get(row[0]), vals.get(row[1]), vals.get(row[2])
        if name is None or up is None:
            return None
        out.append((str(name), "done" if up == 0 else ("now" if on == 1 else "next")))
    return out


def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


class TagTeam:
    """Watches the values after FightFX.update: the hyper combos, and the win kept for the last character."""

    def __init__(self):
        self.prev = {}
        self.key = None

    def update(self, fight, vals, spec, now, key=None):
        if key != self.key:                              # another game: nothing kept / un autre jeu : on oublie tout
            self.key = key
            self.prev = {}
        if not in_match(vals, spec):
            self.prev = {}
            return
        from .hd_fight import GOLD
        levels = spec.get("level") if isinstance(spec.get("level"), list) else []
        for name in levels:
            v, old = _num(vals.get(name)), _num(self.prev.get(name))
            if v is not None and old is not None and v < old and fight is not None:
                fight.banner = ("HYPER COMBO", HYPER, now, 1.2)        # the gauge is spent / la jauge est dépensée
            self.prev[name] = v
        wiped = {}
        for side in ("p1", "p2"):
            rows = spec.get(side) if isinstance(spec.get(side), list) else []
            ups = [vals.get(r[1]) for r in rows if isinstance(r, list) and len(r) >= 3]
            wiped[side] = bool(ups) and all(u == 0 for u in ups)
        if fight is not None:
            if fight.banner is not None and fight.banner[0] == "TIME UP":
                fight.banner = ("TIME OVER",) + tuple(fight.banner[1:])  # the words of the game / les mots du jeu
            for side, other in (("p1", "p2"), ("p2", "p1")):
                w = fight.win
                if wiped[side] and not self.prev.get(side + "_wiped"):
                    if wiped[other]:                                     # both teams down: no winner / pas de vainqueur
                        fight.win = None
                    else:                                                # no PERFECT: it is about one character only
                        fight.win = [other, now + 0.8, False, False]
                        fight.banner = (("P1" if other == "p1" else "P2") + " WINS", GOLD, now + 0.9, 1.8)
                elif not wiped[side] and w is not None and w[0] == other and not w[3]:
                    fight.win = None                 # one character KO, or the time out / un seul KO, ou le temps écoulé
        for side in ("p1", "p2"):
            self.prev[side + "_wiped"] = wiped[side]


def draw_levels(hd, screen, vals, spec, now):
    """The hyper combo gauge of each team in pips, under its health bar."""
    S, W = hd.S, hd.W
    levels = spec.get("level") if isinstance(spec.get("level"), list) else []
    top = int(spec.get("level_max", 5) or 5)
    pw, ph, gap = S(46), S(14), S(10)
    for i, name in enumerate(levels[:2]):
        n = _num(vals.get(name))
        if n is None:
            continue
        n = max(0, min(top, int(n)))
        glow = 0.75 + 0.25 * math.sin(now * 5 + i)
        for k in range(top):
            x = S(40) + k * (pw + gap) if i == 0 else W - S(40) - pw - k * (pw + gap)
            lit = k < n
            col = tuple(int(c * glow) for c in HYPER) if lit else HYPER_DIM
            hd.pg.draw.rect(screen, col, (x, S(238), pw, ph), border_radius=max(1, S(5)))
            if lit:
                hd.pg.draw.rect(screen, (210, 245, 255), (x + S(4), S(240), pw - S(8), max(1, S(3))), border_radius=max(1, S(2)))


def draw_idle(hd, screen, logo, now):
    """Out of a match: the logo, and 3 VS 3. / Hors match : le logo, et 3 VS 3."""
    from .hd_fight import GOLD
    W, S = hd.W, hd.S
    hd.draw_logo(screen, logo, W / 2, S(190), S(1000), S(220), now, valign="middle")
    a = hd._pulse(now, 1.6)                              # 8 levels, the texts stay in the cache / textes gardés en cache
    hd.put(screen, hd.text("3 VS 3", "black", S(60), tuple(int(c * a) for c in GOLD)), W / 2, S(372), "center", "middle")
