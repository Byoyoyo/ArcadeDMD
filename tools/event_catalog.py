"""Writes the catalogue of what ArcadeDMD reads and announces, game by game, from the code and the game files as they
are: docs/EVENT_ENGINE_CATALOG.md (each game, the scene that follows it, the values it reads, the announcements of its
LED panel; then each scene, the values it reads and every place it announces something, with the conditions around it)
and docs/EVENT_ENGINE_VALUES.md (every address of every game file). Reads only, changes nothing in the engine. To be run
again after a change, so that docs/EVENT_ENGINE_HANDOFF.md keeps pointing at the truth.

Écrit le catalogue de ce qu'ArcadeDMD lit et annonce, jeu par jeu, à partir du code et des fichiers de jeu tels qu'ils
sont. Lecture seule, rien n'est changé dans le moteur.

usage: python tools/event_catalog.py [--check]
"""

import ast
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

FIGHT_SCENES = ("neogeo_combat", "cps_combat", "cave_combat")
ANNOUNCE = ("popup", "slam", "power_pop", "announce", "_light", "_slam", "_side_slam")
VALUE_OPTS = ("bytes", "mult", "add", "min", "max", "zero_from", "round", "mask", "shift", "valid", "ptr", "ptr_range",
              "count", "stride", "start", "delay", "fast", "mame_only", "hold_zero", "human")
HD_SKIP = ("note", "scene", "stages", "places")


def short(s, n):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n - 1] + "…"


def code(s, n=160):
    return "`" + short(s, n).replace("`", "'").replace("|", "¦") + "`"


def text_of(node):
    """The text an announcement shows, in English when the code gives both languages. / Le texte annoncé."""
    if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "tr" and len(node.args) == 2:
        node = node.args[1]
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return ast.unparse(node)


class Sites(ast.NodeVisitor):
    """Every announcement of a class with the conditions around it, and the values the class reads by name.
    / Chaque annonce d'une classe avec les conditions qui l'entourent, et les valeurs qu'elle lit par leur nom."""

    def __init__(self):
        self.conds, self.func, self.sites, self.reads, self.watched = [], [], [], set(), set()
        self.names = {}                          # a loop's variable and the names it takes / la variable d'une boucle

    @staticmethod
    def consts(node):
        """The names a loop goes through, when they are written there. / Les noms que parcourt une boucle."""
        if isinstance(node, (ast.Tuple, ast.List)) and node.elts and all(
                isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
            return [e.value for e in node.elts]
        return None

    def loop(self, target, it, body):
        names = self.consts(it)
        key = target.id if isinstance(target, ast.Name) else None
        if key and names:
            self.names[key] = names
        for n in body:
            self.visit(n)
        if key and names:
            self.names.pop(key, None)

    def visit_For(self, node):
        self.visit(node.iter)
        self.loop(node.target, node.iter, node.body + node.orelse)

    def comp(self, node):
        gens = node.generators
        body = [node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]
        if len(gens) == 1:
            self.loop(gens[0].target, gens[0].iter, body + gens[0].ifs)
        else:
            self.generic_visit(node)

    visit_DictComp = visit_ListComp = visit_SetComp = visit_GeneratorExp = comp

    def named(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return [node.value]
        if isinstance(node, ast.Name) and node.id in self.names:
            return self.names[node.id]
        return [ast.unparse(node)]

    def visit_FunctionDef(self, node):
        self.func.append(node.name)
        saved, self.conds = self.conds, [] if len(self.func) == 1 else list(self.conds)
        self.generic_visit(node)
        self.conds = saved
        self.func.pop()

    def visit_ClassDef(self, node):
        return                                   # a class inside a class is read on its own / lue à part

    def visit_If(self, node):
        test = ast.unparse(node.test)
        self.visit(node.test)
        self.conds.append(test)
        for n in node.body:
            self.visit(n)
        self.conds[-1] = "not (" + test + ")"
        for n in node.orelse:
            self.visit(n)
        self.conds.pop()

    def visit_Assign(self, node):
        if (isinstance(node.value, ast.Tuple) and node.value.elts
                and any(isinstance(t, ast.Attribute) and t.attr == "banner" for t in node.targets)):
            self.site(node, "banner", node.value.elts[0])
        self.generic_visit(node)

    def site(self, node, kind, arg):
        self.sites.append({"line": node.lineno, "kind": kind, "func": ".".join(self.func) or "?",
                           "text": text_of(arg) if arg is not None else "", "when": list(self.conds)})

    def visit_Call(self, node):
        f = node.func
        if isinstance(f, ast.Attribute):
            recv = ast.unparse(f.value)
            arg = node.args[0] if node.args else None
            if f.attr in ANNOUNCE:
                self.site(node, f.attr.lstrip("_"), arg)
            elif f.attr == "text" and recv.endswith("fx"):
                self.site(node, "fx.text", arg)
            elif f.attr == "event" and "lights" in recv:
                self.site(node, "lights", arg)
            elif f.attr == "get" and recv in ("vals", "self.vals", "v", "values", "eng.state.values", "st.values"):
                if arg is not None and (isinstance(arg, ast.Constant) or (isinstance(arg, ast.Name) and arg.id in self.names)):
                    self.reads.update(n for n in self.named(arg) if isinstance(n, str))
            elif f.attr in ("changed", "get") and len(node.args) >= 2 and recv == "self":
                last = node.args[-1] if f.attr == "get" else node.args[1]
                (self.watched if f.attr == "changed" else self.reads).update(self.named(last))
        self.generic_visit(node)


def classes():
    """{class name: its module, lines, bases, announcements and values read}, for the modules of the HD screen.
    / Chaque classe des modules de l'écran HD."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "dmd", "hd*.py"))):
        tree = ast.parse(open(path, encoding="utf-8").read())
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            s = Sites()
            for n in node.body:
                s.visit(n)
            doc = ast.get_docstring(node) or ""
            out[node.name] = {"module": "dmd/" + os.path.basename(path), "line": node.lineno, "end": node.end_lineno,
                              "bases": [ast.unparse(b) for b in node.bases], "sites": s.sites,
                              "reads": sorted(s.reads), "watched": sorted(s.watched),
                              "doc": doc.split("\n\n")[0].split(" / ")[0]}
    return out


def detector(key, g, scenes, family):
    """The part of the HD screen that follows a game, as dmd/hd.py picks it. / Ce qui suit un jeu sur l'écran HD."""
    if family(key):
        return "MetalSlugScene"
    hd = g.get("hd") if isinstance(g.get("hd"), dict) else {}
    if hd.get("scene") in scenes:
        return scenes[hd["scene"]].__name__
    names = ((g.get("memory") or {}).get("values") or {})
    if (g.get("scene_from") or key) in FIGHT_SCENES or ("health" in names and "health_p2" in names):
        return "FightFX"
    return "(générique)"


def bare(obj):
    """An expression of a game file without its notes. / Une expression d'un fichier de jeu sans ses notes."""
    if isinstance(obj, dict):
        return {k: bare(v) for k, v in obj.items() if k != "note" and not k.endswith("_note")}
    if isinstance(obj, list):
        return [bare(v) for v in obj]
    return obj


def when_text(c):
    return short(json.dumps(c, ensure_ascii=False, separators=(",", ":")), 150) if c else ""


def led_rules(g):
    """The announcements of the LED panel a game file declares ("events" layers). / Les annonces de la dalle LED."""
    rules = []

    def walk(layers):
        for layer in layers or []:
            if not isinstance(layer, dict):
                continue
            if layer.get("type") == "events":
                for e in layer.get("events") or []:
                    if isinstance(e, dict):
                        rules.append(e)
            for page in layer.get("pages") or []:
                walk(page.get("layers") if isinstance(page, dict) else [])
            walk(layer.get("layers"))
    sc = g.get("scene")
    walk(sc.get("layers") if isinstance(sc, dict) else [])
    return rules


def rule_line(e):
    on = e.get("on")
    bits = [",".join(on) if isinstance(on, list) else str(on), e.get("change", "any")]
    for k in ("step", "from", "to"):
        if k in e:
            bits.append(f"{k}={json.dumps(e[k])}")
    w = when_text(e.get("when"))
    return (f"  - {code(' '.join(bits), 90)} → **{short(e.get('text', ''), 40)}**"
            f" (priorité {e.get('priority', 1)}, {e.get('ms', 1400)} ms" + (f", délai du texte {e['text_delay']} s" if e.get("text_delay") else "")
            + ")" + (f" si {code(w, 150)}" if w else ""))


def value_line(name, d):
    opts = []
    for k in VALUE_OPTS:
        if k in d and not (k == "bytes" and d.get("type") in ("u8", None)):
            opts.append(f"{k}={json.dumps(d[k], separators=(',', ':'))}")
    return f"{name:<22} {str(d.get('addr') or '-'):<10} {str(d.get('type', 'u8')):<9} {' '.join(opts)}".rstrip()


def build():
    import dmd.hd as hd
    from dmd.hd_mslug import family
    scenes = hd.GAME_SCENES
    cls = classes()
    caps = {}
    for p in glob.glob(os.path.join(ROOT, "tests", "captures", "*.log")):
        k = os.path.basename(p).split("-20")[0]
        caps[k] = caps.get(k, 0) + 1
    games = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "games", "*.json"))):
        games[os.path.basename(p)[:-5]] = json.load(open(p, encoding="utf-8"))
    by_det = {}
    for key, g in games.items():
        by_det.setdefault(detector(key, g, scenes, family), []).append(key)

    cat = ["# Catalogue du moteur d'événements", "",
           "Fichier produit par `python tools/event_catalog.py` à partir du code et des fichiers de jeu. Ne pas le modifier à la"
           " main. Il accompagne [EVENT_ENGINE_HANDOFF.md](EVENT_ENGINE_HANDOFF.md).", "",
           f"{len(games)} fichiers de jeu, {sum(len((g.get('memory') or {}).get('values') or {}) for g in games.values())} valeurs lues,"
           f" {len([c for c in cls.values() if c['sites']])} classes qui annoncent, {sum(len(c['sites']) for c in cls.values())} annonces dans le code,"
           f" {sum(len(led_rules(g)) for g in games.values())} règles d'annonce de la dalle LED.", "",
           "## 1. Les jeux", "",
           "Pour chaque fichier de jeu, la partie de l'écran HD qui le suit, les valeurs lues (les noms qui commencent par `_`"
           " servent à la détection et ne sont pas affichés), les valeurs calculées, les options du bloc `hd`, les annonces"
           " de sa dalle LED et le nombre de parties réelles gardées dans `tests/captures`. Les adresses sont dans"
           " [EVENT_ENGINE_VALUES.md](EVENT_ENGINE_VALUES.md).", ""]
    order = sorted(by_det, key=lambda d: (d == "(générique)", d not in ("MetalSlugScene", "FightFX"), d))
    for det in order:
        c = cls.get(det)
        where = f" (`{c['module']}`)" if c else ""
        cat += [f"### {det}{where}", ""]
        for key in sorted(by_det[det]):
            g = games[key]
            vals = (g.get("memory") or {}).get("values") or {}
            pub = [n for n in vals if not n.startswith("_")]
            prv = [n for n in vals if n.startswith("_")]
            m = g.get("match")
            sets = m[0].get("system") if isinstance(m, list) and m and isinstance(m[0], dict) else None
            nsets = len(sets) if isinstance(sets, list) else (1 if sets else 0)
            title = g.get("title") or ""
            cat.append(f"**{key}**" + (f" — {title}" if title else "") + (f" ({nsets} romsets)" if nsets > 1 else "")
                       + ("" if m else " — modèle, pas un jeu") + (f" — scène LED de `{g['scene_from']}`" if g.get("scene_from") else ""))
            if pub:
                cat.append(f"- valeurs ({len(pub)}) : " + ", ".join(pub))
            if prv:
                cat.append(f"- internes ({len(prv)}) : " + ", ".join(prv))
            for blk in ("derived", "tag"):
                if isinstance(g.get(blk), dict) and g[blk]:
                    cat.append(f"- `{blk}` : " + ", ".join(k for k in g[blk] if k != "note"))
            hdb = g.get("hd") if isinstance(g.get("hd"), dict) else {}
            opts = [f"{k}={short(json.dumps(bare(v), ensure_ascii=False), 60)}" for k, v in hdb.items()
                    if k not in HD_SKIP and not k.endswith("note") and not k.startswith("note")]
            if hdb.get("stages"):
                opts.append(f"{len(hdb['stages'])} décors")
            if opts:
                cat.append("- `hd` : " + ", ".join(opts))
            extra = [f"{k} ({len([x for x in g[k] if x != 'note'])} combattants)" for k in ("specials", "moves") if isinstance(g.get(k), dict)]
            extra += [k for k in ("activity", "coins", "hyper", "per_game") if g.get(k)]
            if extra:
                cat.append("- aussi : " + ", ".join(extra))
            rules = led_rules(g)
            if rules:
                cat.append(f"- annonces de la dalle LED ({len(rules)}) :")
                cat += [rule_line(e) for e in rules]
            if caps.get(key):
                cat.append(f"- parties réelles dans `tests/captures` : {caps[key]}")
            cat.append("")

    cat += ["## 2. Les scènes de l'écran HD", "",
            "Pour chaque classe, les valeurs qu'elle lit par leur nom, celles dont elle guette le changement (`changed`), et"
            " chaque endroit où elle annonce quelque chose, avec les conditions qui l'entourent telles que le code les écrit."
            " Une classe hérite des annonces de ses classes de base. Les réactions sans texte (explosions, secousses,"
            " mouvements du héros) ne sont pas listées ici, elles suivent les mêmes changements de valeurs.", ""]
    used = {}
    for det, keys in by_det.items():
        used[det] = keys
    for name in sorted(cls, key=lambda n: (cls[n]["module"], cls[n]["line"])):
        c = cls[name]
        if not (c["sites"] or c["reads"] or c["watched"] or name in used):
            continue
        cat.append(f"### {name} — `{c['module']}` lignes {c['line']} à {c['end']}")
        cat.append("")
        if c["bases"]:
            cat.append("- hérite de : " + ", ".join(c["bases"]))
        if name in used:
            cat.append(f"- jeux ({len(used[name])}) : " + ", ".join(sorted(used[name])))
        if c["reads"]:
            cat.append("- valeurs lues : " + ", ".join(code(r, 40) for r in c["reads"]))
        if c["watched"]:
            cat.append("- changements guettés : " + ", ".join(code(r, 50) for r in c["watched"]))
        if c["sites"]:
            cat.append("- annonces :")
            for s in c["sites"]:
                when = " ET ".join(code(w, 150) for w in s["when"][-4:])
                when = "si " + when if when else "sans condition dans cette fonction, voir qui l'appelle"
                over = len(s["when"]) - 4
                more = f" (et {over} autre{'s' if over > 1 else ''} condition{'s' if over > 1 else ''} au-dessus)" if over > 0 else ""
                cat.append(f"  - ligne {s['line']}, `{s['func']}`, {s['kind']} **{short(s['text'], 70)}** — {when}{more}")
        cat.append("")

    val = ["# Adresses lues, jeu par jeu", "",
           "Fichier produit par `python tools/event_catalog.py` à partir de `games/*.json`, qui restent la référence. Chaque ligne"
           " donne le nom de la valeur, son adresse, son type et ses options. Le sens de chaque valeur est dans le champ `note`"
           " du fichier de jeu. Le décodage est décrit dans `dmd/memvalues.py` et résumé dans"
           " [EVENT_ENGINE_HANDOFF.md](EVENT_ENGINE_HANDOFF.md).", ""]
    for key in sorted(games):
        g = games[key]
        mem = g.get("memory") or {}
        vals = mem.get("values") or {}
        if not vals and not g.get("per_game"):
            continue
        ra = g.get("retroarch") if isinstance(g.get("retroarch"), dict) else {}
        head = [f"cpu {mem.get('cpu')}"] if mem.get("cpu") else []
        head += [f"{k} {ra[k]}" for k in ("ram_base", "ram_size", "swap16", "swap32") if k in ra]
        val += [f"## {key}" + (f" — {g['title']}" if g.get("title") else ""), ""]
        if head:
            val += [", ".join(head), ""]
        val.append("```")
        val += [value_line(n, d) for n, d in vals.items() if isinstance(d, dict)]
        val.append("```")
        pg = g.get("per_game") if isinstance(g.get("per_game"), dict) else {}
        for rom, over in pg.items():
            if isinstance(over, dict) and over:
                val += ["", f"Propre au romset `{rom}` :", "", "```"]
                val += [value_line(n, d) for n, d in over.items() if isinstance(d, dict)]
                val.append("```")
        for blk in ("tag", "derived"):
            if isinstance(g.get(blk), dict) and g[blk]:
                val += ["", f"`{blk}` :", ""]
                val += [f"- `{k}` = {code(json.dumps(bare(v), ensure_ascii=False, separators=(',', ':')), 230)}" for k, v in g[blk].items() if k != "note"]
        val.append("")
    return "\n".join(cat) + "\n", "\n".join(val) + "\n"


def main():
    cat, val = build()
    targets = ((os.path.join(ROOT, "docs", "EVENT_ENGINE_CATALOG.md"), cat), (os.path.join(ROOT, "docs", "EVENT_ENGINE_VALUES.md"), val))
    if "--check" in sys.argv:
        stale = [os.path.basename(p) for p, s in targets if not os.path.exists(p) or open(p, encoding="utf-8").read() != s]
        if stale:
            print("not up to date / pas à jour : " + ", ".join(stale) + " (python tools/event_catalog.py)")
            return 1
        print("ok")
        return 0
    for p, s in targets:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(s)
        print(os.path.relpath(p, ROOT), len(s) // 1024, "KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
