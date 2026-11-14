"""Special moves and supers of the fighting games, from the command list of MAME (command.dat, 1.38).

command.dat (Fabricio Coroquer, revised and distributed by AntoPISA with the MAME support files) gives, for each game,
the moves of each fighter: their names, their commands in MAME's own notation (_2_3_6_+_P), and what kind each one is
(_@ special moves, _* desperation moves...), as the game's "HOW TO PLAY" says. This tool reads it, finds each fighter of
the fighting games ArcadeDMD knows (the names of "p1_char" in their game files), and writes their moves in the game file
as "specials": the special moves, always possible, and the supers, possible when the game says (its gauge full...).
The HD screen shows them under the name of a human player, one after another.

Les coups spéciaux et les supers des jeux de combat, d'après la liste des commandes de MAME (command.dat). L'outil
retrouve chaque combattant des jeux de combat qu'ArcadeDMD connaît et écrit ses coups dans le fichier du jeu
("specials") : les coups spéciaux, toujours possibles, et les supers, possibles quand le jeu le dit. L'écran HD les
montre sous le nom d'un joueur humain, l'un après l'autre.

usage: python tools/command_dat.py COMMAND.DAT [GAMES_FOLDER] [--write] [--game NAME]
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

KEEP_SECTIONS = ("CONTROLS", "HOW TO PLAY", "COMMON COMMANDS", "COMBO INFO", "CHEATS", "NOTES", "SPECIAL THANKS", "TIPS",
                 "SECRETS", "HIDDEN", "BOSSES", "MISC", "UNLOCKABLES", "EXTRAS", "ENDINGS", "SYSTEM", "GAME MODES")
# the kinds of moves, from the words of the game's legend / le genre des coups, d'après la légende du jeu
SUPER_WORDS = ("SUPER", "DESPERATION", "HYPER", "WEAPON-BREAKING", "WEAPON BREAKING", "CRITICAL", "ULTIMATE", "LEVEL 3",
               "MAX", "SUPER ART", "FATAL", "LIBERATION", "EX ")
# MAME's glyphs (rendfont.cpp): "_" the default ones, "^" the expanded ones / les symboles de MAME
LABELS = {"_P": "P", "_K": "K", "^E": "LP", "^F": "MP", "^G": "HP", "^H": "LK", "^I": "MK", "^J": "HK", "^T": "KKK",
          "^U": "PPP", "^V": "KK", "^W": "PP", "_G": "G"}
NEOGEO = "ABCD"
MAX_ROWS = 8                              # moves kept per fighter / coups gardés par combattant
ALIASES = {
    # the game's name -> the fighter's header in command.dat, when the words differ too much / quand les mots diffèrent trop
    "S.SAMURAI": "SILVER SAMURAI",
    "WANG-FU": "WAN-FU",
    "V.V.GELDENH": "VICTOR VON GERDENHEIM",
    "B.B.HOOD": "BABY BONNIE HOOD",
    "#.B.HOOD": "BABY BONNIE HOOD",
    "A.DONOVAN": "DONOVAN BAINE",
    "D.BAINE": "DONOVAN BAINE",
    "A.PHOBOS": "HUITZIL",
    "GENJYURO": "GENJURO KIBAGAMI",
    "V.KEN": "VIOLENT KEN",
    "DOC DOOM": "DR. DOOM",
    "C.AMERICA": "CAPTAIN AMERICA",
    "S.GORATH": "SHUMA-GORATH",
    "HANZOU": "HANZO HATTORI",
    "J.CARN": "JENGHIS CARN",
    "J.MAX": "JOHNNY MAXIMUM",
    "GOKU": "SON GOKUU",
    "MATLOCK": "MATLOK JADE",
    "BULL": "OX",
    "STINGER": "HELLSTINGER",
    "BONNE": "BEHRN JENET",
    "TODO": "RYUHAKU TODOH",
    "MICKY": "MICKEY ROGERS",
    "KAZUMI": "KASUMI TODOH",
    "KUSARE-GEDOU": "YOUKAI KUSAREGEDO",
    "SANKURO": "SANKURO YOROZU",
    "S.BILLY": "BILLY LEE",
    "S.JIMMY": "JIMMY LEE",
    "R.M.NANAKAW": "RAINBOW MIKA NAKANAWA",
    "J.JOSTER": "JOSEPH JOESTAR",
    "H.K.JOSEPH": "JOSEPH JOESTAR",
    "JOUTARO": "JOTARO KUJO",
    "J.K.DIO": "DIO",
    "KAKYOUIN": "KAKYOIN NORIAKI",
    "K.W.N.KAKYO": "NEW KAKYOIN",
    "A.N.POLNARE": "BLACK POLNAREFF",
    "H.+.VOING": "HOL HORSE & VOING",
    "MAHRIAH": "MAHRAHIA",
    "KAHN": "KAN",
    "DEATH 13": "DEATH13",
    "VANILLA ICE": "VANILLA ICED",
    "#.N.H.N.M.R": "SHIN AKUMA",
    "OSHIMA": "GOKETSUJI OSIMA",
    "S.KURARA": "KURARA HANAKOUJI",
    "#AKUMA/GOUK": "AKUMA",
    "DIMITRI": "DEMITRI MAXIMOFF",
    "ZABELZAROCH": "LORD RAPTOR",
    "#.SPIDER-MA": "SPIDER-MAN",
    "ZANGEIF": "ZANGIEF",
    "ALT-HULK": "ORANGE HULK",
    "ALT-MORRIGA": "MORRIGAN LILITH STYLE",
    "ALT-VENOM": "RED VENOM",
    "ALT-WAR-MAC": "GOLDEN WAR MACHINE",
    "KUBIKIRI": "BASARA KUBIKIRI",
    "AMAKUSA": "SHIRO AMAKUSA TOKISADA",
}
# MAME's glyphs of whole motions (rendfont.cpp), for a fighter facing right / les gestes entiers, tourné vers la droite
MOTIONS = {"_k": "63214", "_l": "47896", "_m": "41236", "_n": "69874", "_o": "632", "_p": "214", "_q": "478", "_r": "896",
           "_s": "412", "_t": "236", "_u": "698", "_v": "874", "_w": "63214789", "_x": "41236987", "_y": "69874123",
           "_z": "47896321"}
CIRCLED = {"①": "SA1 ", "②": "SA2 ", "③": "SA3 ", "④": "4 ", "⑤": "5 "}
# conditions written before a command, kept as a word on the screen / les conditions écrites avant une commande
WHEN = {"close": "close", "near": "close", "far": "far", "running": "run", "while running": "run", "in the air": "air",
        "jumping": "air", "airborne": "air", "on air": "air", "crouching": "crouch"}


def entries(text):
    """{romset: text of its $cmd block} / le bloc de chaque jeu."""
    out = {}
    for m in re.finditer(r"^\$info=([^\n]*)\n(.*?)^\$end", text, re.M | re.S):
        block = m.group(2)
        k = block.find("$cmd")
        if k < 0:
            continue
        body = block[k + 4:]
        for s in m.group(1).split(","):
            s = s.strip()
            if s and s not in out:
                out[s] = body
    return out


def sections(body):
    """[(title, [lines])] of a game's block: "- NAME -" over a rule of ─. / Les sections du bloc d'un jeu."""
    lines = body.splitlines()
    out, cur = [], None
    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        m = re.match(r"^- (.+?) -(\s{2,}.*)?$", line.rstrip())
        if m and nxt.startswith("─"):
            cur = (m.group(1).strip(), [])
            out.append(cur)
        elif cur is not None and not line.startswith("─"):
            cur[1].append(line.rstrip())
    return out


def legend(secs):
    """{marker: label} from HOW TO PLAY, and {label: [notes]} (_` Desperation Moves / - Needs a FLASHING Life Bar).
    / La légende des marques et leurs notes."""
    marks, notes = {}, {}
    for title, lines in secs:
        if title != "HOW TO PLAY":
            continue
        cur = None
        for line in lines:
            m = re.match(r"^(_[()@*&#%$\]\[<>{}]) (.+)$", line)
            if m:
                marks[m.group(1)] = m.group(2).strip()
                continue
            m = re.match(r"^_` (.+)$", line)
            if m:
                cur = m.group(1).strip()
                notes.setdefault(cur, [])
                continue
            m = re.match(r"^\s+- (.+)$", line)
            if m and cur:
                notes[cur].append(m.group(1).strip())
    return marks, notes


def button_map(secs):
    """{"P": "AC", "K": "BD", "s": "AB"} for a game of lettered buttons (Neo Geo): the buttons each class is, from
    CONTROLS (_A : Weak Punch (_P)). / Les boutons de chaque classe, d'après CONTROLS."""
    out = {}
    for title, lines in secs:
        if title != "CONTROLS":
            continue
        if any(re.match(r"^\^[E-J] : ", line) for line in lines):
            return out                               # six buttons (Capcom): P and K as they are / six boutons
        for line in lines:
            if line.startswith("^s : "):
                out["s"] = "S"                       # a button of its own (JoJo's Stand) / un bouton à part
            m = re.match(r"^_([A-D]) : .*\((_P|_K|\^s)\)", line)
            if m and out.get("s") != "S":
                key = {"_P": "P", "_K": "K", "^s": "s"}[m.group(2)]
                out[key] = out.get(key, "") + m.group(1)
    return out


def kind_of(label):
    """'special', 'super' or None (a throw, a taunt, a hidden move...). / Le genre d'un coup."""
    u = (label or "").upper()
    if any(w in u for w in ("HIDDEN", "SECRET", "NUIGURUMI")):
        return None
    if "SPECIAL MOVE" in u or u in ("SPECIALS", "SPECIAL ATTACKS", "SPECIAL ATTACK"):
        return "special"
    if any(w in u for w in SUPER_WORDS):
        return "super"
    return None


def tokens(cmd):
    """(when, tokens) of a command: a condition the screen can say (close, far, in the air), None when it has other
    words (unarmed, jump against the wall...). / La condition et les jetons d'une commande, None avec d'autres mots."""
    s = re.sub(r"\((?:[^()]*)\)", " ", cmd).strip()  # (reflect projectile), (_^), (^*) / les parenthèses
    when = None
    for w in sorted(WHEN, key=len, reverse=True):
        if s.lower().startswith(w + " "):
            when, s = WHEN[w], s[len(w):].strip()
            break
    if s.startswith("_^"):                             # in the air only / en l'air seulement
        when, s = "air", s[2:].strip()
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in " \t":
            i += 1
            continue
        if c == "/":
            out.append("/")
            i += 1
            continue
        if c in "_^@" and i + 1 < len(s):
            out.append(s[i:i + 2])
            i += 2
            continue
        return None
    return when, out


def convert(cmd, bmap):
    """MAME's notation -> (directions, held steps, buttons, condition, rapid) or None. '_2_3_6_+_P' -> ('236', [], 'A/C',
    None, False). / La notation de MAME -> (directions, étapes tenues, boutons, condition, appui rapide) ou None."""
    got = tokens(cmd)
    if not got or not got[1]:
        return None
    when, toks = got
    alts, cur = [], []
    for t in toks:
        if t == "/":
            alts.append(cur)
            cur = []
        else:
            cur.append(t)
    alts.append(cur)
    first = alts[0]
    extra = []                                       # "/ _K": other buttons for the same motion / d'autres boutons
    for a in alts[1:]:
        if a and all(t not in ("_+",) and not re.match(r"[_^][1-9]$", t) for t in a):
            extra.append(a)
        else:
            break
    dirs, held, groups = "", [], []
    rapid = False
    for t in first:
        if t in MOTIONS:
            if groups:
                return None
            dirs += MOTIONS[t]
        elif re.match(r"_[1-9]$", t):
            if groups:
                return None                          # a direction after a button / une direction après un bouton
            dirs += t[1]
        elif re.match(r"\^[1-9]$", t):               # charge / chargé
            if groups:
                return None
            held.append(len(dirs))
            dirs += t[1]
        elif t == "^*":
            rapid = True
        elif t in ("_+", "_N", "_.", "_!", "^!"):
            continue
        else:
            b = button(t, bmap)
            if b is None:
                return None
            groups.append(b)
    if not groups:
        return None
    alt = [button(a[0], bmap) for a in extra if len(a) == 1]
    if len(groups) == 1:
        btn = "/".join([groups[0]] + [x for x in alt if x and x != groups[0]])
    else:
        btn = "+".join(groups)
    return dirs, held, btn, when, rapid


def button(t, bmap):
    """A button token -> its name on the screen: A, B... (Neo Geo) or P, K, LP, PPP (Capcom). / Le nom d'un bouton."""
    if re.match(r"_[A-D]$", t):
        return t[1]
    if t == "^s":
        return "/".join(bmap.get("s", "AB"))
    if re.match(r"_[a-j]$", t):                      # Capcom's numbered buttons (JoJo: light, medium, heavy) / numérotés
        return t[1].upper()
    if t in ("_P", "_K"):
        letters = bmap.get(t[1])
        if letters and all(x in NEOGEO for x in letters):
            return "/".join(letters)
        return LABELS[t]
    return LABELS.get(t)


def norm(name):
    return re.sub(r"[^A-Z0-9]+", " ", str(name).upper().replace("#", "").replace("'", "")).split()


def _word_ok(w, h):
    """A word of the game's name against a word of the header: the same, an initial (E. HONDA), the start of it (cut
    short in the game: NANAKAW), or nearly the same (MAXIMOV, MAXIMOFF). / Un mot du nom contre un mot de l'en-tête."""
    import difflib
    if w == h:
        return True
    if len(w) == 1:
        return h.startswith(w)
    if len(w) >= 4 and h.startswith(w):
        return True
    return len(w) >= 5 and difflib.SequenceMatcher(None, w, h[:len(w) + 1]).ratio() >= 0.8


def _names(head):
    """The names a header gives: its main name and the one in brackets (M. BISON (VEGA)). / Ses noms."""
    m = re.match(r"^(.*?)\s*\((.*)\)\s*$", head)
    return [m.group(1), m.group(2)] if m else [head]


def match_fighter(name, heads):
    """The header of command.dat for a fighter's name of the game, or None: the same words first, then the main names of
    the headers, then the names in brackets (Street Fighter's VEGA (BALROG) is the claw, BALROG (M. BISON) the boxer).
    / L'en-tête pour un nom du jeu : les mêmes mots d'abord, puis les noms principaux, puis ceux entre parenthèses."""
    want = norm(ALIASES.get(name, ALIASES.get(name.lstrip("#"), name)))
    if not want:
        return None
    joined = "".join(want)
    for rank in (0, 1):
        for h in heads:
            hn = _names(h)
            if rank >= len(hn):
                continue
            if "".join(norm(hn[rank])) == joined:
                return h
    for rank in (0, 1):
        for h in heads:
            hn = _names(h)
            if rank >= len(hn):
                continue
            hw = norm(hn[rank])
            i = 0
            for w in hw:                             # its words in order / ses mots dans l'ordre
                if i < len(want) and _word_ok(want[i], w):
                    i += 1
            if i == len(want) and (len(want) > 1 or want[0] == hw[0] or (len(want[0]) >= 4 and hw[0].startswith(want[0]))):
                return h
    if len(want) == 1 and len(want[0]) >= 4:      # one word, another of the header's (DAIMON -> GORO DAIMON), when only one
        found = sorted({h for h in heads if any(w == want[0] for n in _names(h) for w in norm(n))})   # one header / un seul
        if len(found) == 1:
            return found[0]
    return None


def fighter_moves(lines, marks, bmap):
    """[{name, cmd, btn, kind, hold?}] of a fighter's section. / Les coups d'une section de combattant."""
    out = []
    for line in lines:
        m = re.match(r"^(_[()@*&#%$\]\[<>{}]) (.*)$", line)
        if not m:
            continue
        kind = kind_of(marks.get(m.group(1), ""))
        if kind is None:
            continue
        rest = m.group(2)
        rest = re.sub(r"^\([─\-/A-Za-z*]{1,15}\)\s*", "", rest)      # (W) the weapon, (P) the plane... / les marques
        rest = re.sub(r"^\(\d+%\)\s*", "", rest)                       # (20%) its cost / son coût
        rest = re.sub(r"^\([^()]{1,12}\)\s+(?=\S)", "", rest)            # (!/EX), (I/O)... the game's marks / ses marques
        if rest.lstrip().startswith("^!"):
            continue                                                  # a follow-up / une suite
        parts = re.split(r"\s{2,}", rest.strip(), maxsplit=1)
        if len(parts) != 2:
            continue
        name, cmd = parts[0].strip(), parts[1].strip()
        if not name or name.startswith("^") or name.startswith("_") or len(re.findall(r"[A-Za-z]", name)) < 3:
            continue
        conv = convert(cmd, bmap)
        if conv is None:
            continue
        dirs, held, btn, when, rapid = conv
        for k, v in CIRCLED.items():                 # the Super Arts of Street Fighter III / les Super Arts
            name = name.replace(k, v)
        row = {"name": re.sub(r"\s+", " ", name.upper()).strip(), "cmd": dirs, "btn": btn, "kind": kind}
        if held:
            row["hold"] = held
        if when:
            row["when"] = when
        if rapid:
            row["rapid"] = True
        if any(r["name"] == row["name"] for r in out):
            continue
        out.append(row)
    specials = [r for r in out if r["kind"] == "special"][:MAX_ROWS]
    supers = [r for r in out if r["kind"] == "super"][:MAX_ROWS]
    return specials + supers


def game_sets(g):
    sets = []
    for mm in g.get("match") or []:
        s = mm.get("system")
        sets += s if isinstance(s, list) else [s]
    sets += (g.get("retroarch") or {}).get("content") or []
    return [s for s in sets if isinstance(s, str)]


def build(g, ents):
    """("specials" block, report) for a game file, or (None, why). / Le bloc "specials" d'un jeu."""
    d = (g.get("derived") or {}).get("p1_char")
    names = d.get("names") if isinstance(d, dict) else None
    if not isinstance(names, dict):
        return None, "no names"
    body = next((ents[s] for s in game_sets(g) if s in ents), None)
    if body is None:
        return None, "not in command.dat"
    secs = sections(body)
    marks, notes = legend(secs)
    bmap = button_map(secs)
    heads = [t for t, _ in secs if t not in KEEP_SECTIONS]
    block, found, missing = {}, [], []
    for name in sorted(set(v for v in names.values() if isinstance(v, str) and v)):
        h = match_fighter(name, heads)
        if h is None:
            missing.append(name)
            continue
        rows = fighter_moves(dict(secs)[h], marks, bmap)
        if rows:
            block[name.lstrip("#").upper()] = rows
            found.append(name)
        else:
            missing.append(name + " (0)")
    if not block:
        return None, f"nothing found (missing {missing})"
    kinds = sorted({marks[k] for k in marks if kind_of(marks[k])})
    cond = []
    for k in kinds:
        if kind_of(k) == "super":
            cond += notes.get(k, [])
    head = {"note": "special moves and supers of each fighter, shown under a human player's name (1.38): from the command "
                    "list of MAME (command.dat 0.273, Fabricio Coroquer and AntoPISA), made by tools/command_dat.py",
            "kinds": kinds}
    if cond:
        head["super_needs"] = cond
    head.update(block)
    return head, f"{len(found)} fighters, missing {missing}" if missing else f"{len(found)} fighters"


def block_text(block, ind):
    """The "specials" block, a move per line, in the file's own indent. / Le bloc, un coup par ligne."""
    pad = " " * ind
    lines = []
    keys = list(block)
    for i, k in enumerate(keys):
        v = block[k]
        end = "," if i < len(keys) - 1 else ""
        if isinstance(v, list) and v and isinstance(v[0], dict):
            rows = [pad * 3 + json.dumps(r, ensure_ascii=False) for r in v]
            lines.append(pad * 2 + json.dumps(k, ensure_ascii=False) + ": [\n" + ",\n".join(rows) + "\n" + pad * 2 + "]" + end)
        else:
            lines.append(pad * 2 + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) + end)
    return "{\n" + "\n".join(lines) + "\n" + pad + "}"


def save(path, block):
    """The block put at the end of the game file, or in place of the one there, the rest of the file as it was.
    / Le bloc mis à la fin du fichier du jeu, ou à la place de celui qui y est, le reste du fichier tel quel."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    g = json.loads(text)
    second = text.split("\n")[1] if "\n" in text else " "
    ind = max(1, len(second) - len(second.lstrip(" ")))
    body = block_text(block, ind)
    if "specials" in g:
        m = re.search(r'\n' + " " * ind + r'"specials": \{.*?\n' + " " * ind + r'\}(?=,?\n)', text, re.S)
        if m is None:
            print(f"  {os.path.basename(path)}: its \"specials\" block not found as written here, left as it is")
            return False
        new = text[:m.start()] + "\n" + " " * ind + '"specials": ' + body + text[m.end():]
    else:
        new = text.rstrip()
        if not new.endswith("}"):
            return False
        new = new[:-1].rstrip() + ",\n" + " " * ind + '"specials": ' + body + "\n}\n"
    g2 = json.loads(new)                             # still valid, the block as made / toujours valide
    if g2.get("specials") != json.loads(json.dumps(block)):
        raise ValueError(path)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    return True


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    dat = argv[1]
    folder = argv[2] if len(argv) > 2 and not argv[2].startswith("--") else os.path.join(ROOT, "games")
    write = "--write" in argv
    only = argv[argv.index("--game") + 1] if "--game" in argv else None
    with open(dat, encoding="utf-8-sig") as f:
        ents = entries(f.read())
    for path in sorted(glob.glob(os.path.join(folder, "*.json"))):
        key = os.path.basename(path)[:-5]
        if only and key != only:
            continue
        with open(path, encoding="utf-8") as f:
            g = json.load(f)
        if not str(g.get("scene_from") or "").endswith("_combat") or not (g.get("derived") or {}).get("p1_char"):
            continue
        if isinstance(g.get("moves"), dict):
            continue                                 # its own panel (The King of Fighters '97, '98, 2002) / son panneau
        block, why = build(g, ents)
        print(f"{key:12} {why}")
        if block is None or not write:
            continue
        save(path, block)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
