"""test_retroarch.bat: does RetroArch respond, which core is running, can the game memory be read?

Changes nothing. The result is shown and also written to runtime/test_retroarch.txt.

test_retroarch.bat : RetroArch répond-il, quel cœur tourne, la mémoire du jeu se lit-elle ?

Ne modifie rien. Le résultat s'affiche et va aussi dans runtime/test_retroarch.txt.
"""

import os
import sys
import time

from . import wincore
from .i18n import tr
from .learn import load_games
from .memvalues import derive, game_values, value_span
from .retroarch import (RetroArchClient, core_label, explain_failure, find_core, layout_for, match_game,
                        read_values, too_old)

# (français, anglais) : traduit à l'affichage par label()
LABELS = {"lives": ("vies", "lives"), "lives_p2": ("vies J2", "P2 lives"), "bombs": ("bombes", "bombs"),
          "bombs_p2": ("bombes J2", "P2 bombs"), "ammo": ("munitions", "ammo"), "ammo_p2": ("munitions J2", "P2 ammo"),
          "weapon": ("arme", "weapon"), "credits": ("crédits", "credits"), "time": ("temps", "time"),
          "rings": ("anneaux", "rings"), "prisoners": ("prisonniers", "prisoners"), "score_p2": ("score J2", "P2 score"),
          "weapon_p2": ("arme J2", "P2 weapon"), "health": ("vie J1 %", "P1 health %"), "health_p2": ("vie J2 %", "P2 health %"),
          "p1_char": ("perso J1", "P1 character"), "p2_char": ("perso J2", "P2 character"),
          "beat": ("BEAT BY J1", "BEAT BY P1"), "beat_p2": ("BEAT BY J2", "BEAT BY P2"),
          "mission": ("mission", "mission"), "stage": ("stage", "stage"), "backdrop": ("décor", "backdrop")}


HIDDEN = {"p1_mode", "p2_mode", "p1_input", "p2_input"}      # BIOS : état des joueurs et commandes, utiles à la scène seulement


def label(name):
    pair = LABELS.get(name)
    return tr(*pair) if pair else name


def playing(st):
    return bool(st) and st.get("state") in ("PLAYING", "PAUSED")


def run(root, cfg, wait=180, out=print):
    ra = cfg.get("retroarch", {}) or {}
    port = int(ra.get("port", 55355))
    client = RetroArchClient(ra.get("host", "127.0.0.1"), port, timeout=0.5)
    lines = []

    def say(text=""):
        out(text)
        lines.append(text)

    say(tr("Test de RetroArch", "RetroArch test"))
    say("")
    if not ra.get("enabled", True):
        say(tr("Attention, la lecture de RetroArch est coupée dans config.json (retroarch, enabled).",
               "Warning, reading from RetroArch is turned off in config.json (retroarch, enabled)."))
    st = client.status()
    if not playing(st) and wait > 0:
        say(tr("Lance un jeu dans RetroArch, par exemple Metal Slug.", "Start a game in RetroArch, for example Metal Slug."))
        mins = max(1, round(wait / 60))
        say(tr(f"Le test démarre tout seul dès que le jeu tourne (attente de {mins} minute{'s' if mins > 1 else ''} au plus).",
               f"The test starts by itself as soon as the game is running (waiting {mins} minute{'s' if mins > 1 else ''} at most)."))
        end = time.monotonic() + wait
        while time.monotonic() < end:
            time.sleep(1.0)
            st = client.status()
            if playing(st):
                time.sleep(3.0)              # le temps que le jeu démarre vraiment
                st = client.status() or st
                break
        say("")
    try:
        rc = report(root, client, st, port, say)
    finally:
        client.close()
    say("")
    path = os.path.join(root, "runtime", "test_retroarch.txt")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(time.strftime(tr("%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M")) + "\n" + "\n".join(lines) + "\n")
        out(tr("Ce résultat est aussi dans runtime\\test_retroarch.txt", "This result is also in runtime\\test_retroarch.txt")
            if sys.platform == "win32"
            else tr("Ce résultat est aussi dans runtime/test_retroarch.txt", "This result is also in runtime/test_retroarch.txt"))
    except OSError:
        pass
    return rc


def not_responding(port, say):
    say(tr("RetroArch ne répond pas.", "RetroArch is not responding."))
    procs = wincore.find_retroarch()
    if not procs:
        say(tr("RetroArch n'est pas lancé, ou ses commandes réseau sont coupées (voir README.fr.md, section RetroArch).",
               "RetroArch is not running, or its network commands are turned off (see README.md, RetroArch section)."))
        return
    exe = procs[0]["exe"]
    say(tr(f"Pourtant RetroArch tourne ({exe}).", f"Yet RetroArch is running ({exe})."))
    radir = os.path.dirname(exe) if os.path.isabs(exe) else ""
    rcfg = wincore.read_cfg(os.path.join(radir, "retroarch.cfg")) if radir else {}
    if rcfg.get("network_cmd_enable") == "false":
        say(tr("Le réglage Commandes réseau est désactivé dans RetroArch. Active-le (voir README.fr.md, section RetroArch).",
               "The Network Commands setting is turned off in RetroArch. Turn it on (see README.md, RetroArch section)."))
    elif rcfg.get("network_cmd_port") and rcfg["network_cmd_port"] != str(port):
        say(tr(f"RetroArch écoute sur le port {rcfg['network_cmd_port']} et ArcadeDMD sur le port {port}. "
               "Mets le même numéro des deux côtés.",
               f"RetroArch listens on port {rcfg['network_cmd_port']} and ArcadeDMD on port {port}. "
               "Use the same number on both sides."))
    else:
        say(tr("Vérifie que le réglage Commandes réseau est activé (voir README.fr.md, section RetroArch).",
               "Check that the Network Commands setting is turned on (see README.md, RetroArch section)."))


def report(root, client, st, port, say):
    if st is None:
        not_responding(port, say)
        return 1
    if not playing(st):
        say(tr("RetroArch répond, mais aucun jeu ne tourne. Lance un jeu puis relance ce test.",
               "RetroArch responds, but no game is running. Start a game, then run this test again."))
        return 1
    version = client.version() or ""
    say(tr(f"RetroArch {version} répond sur le port {port}.", f"RetroArch {version} responds on port {port}.").replace("  ", " "))
    if too_old(version):
        say(tr("Cette version est trop ancienne pour lire la mémoire des jeux. Il faut RetroArch 1.19 ou plus récent.",
               "This version is too old to read game memory. RetroArch 1.19 or newer is required."))
    say(tr(f"Jeu en cours {st['content']}, système {st['system']}.", f"Current game {st['content']}, system {st['system']}."))
    core = find_core(st["content"])
    if core:
        say(tr(f"Cœur chargé {core_label(core)}.", f"Loaded core {core_label(core)}."))
    elif sys.platform == "win32":
        say(tr("Je n'arrive pas à voir quel cœur est chargé.", "I can't tell which core is loaded."))
    games = load_games(root)
    key, game = match_game(games, st["content"], st["system"])
    template = bool(game and game.get("fallback"))
    if template:
        say(tr(f"Pas de fichier propre à ce jeu, scène commune games/{key}.json.",
               f"No file of its own for this game, shared scene games/{key}.json."))
    else:
        say(tr(f"Fichier ArcadeDMD games/{key}.json.", f"ArcadeDMD file games/{key}.json.") if key
            else tr("Aucun fichier dans games pour ce jeu.", "No file in games for this game."))
    say("")
    data = client.read(0, 16)
    raw = client.last_reply
    say(tr(f"Lecture de la mémoire (READ_CORE_RAM 0 16), réponse « {raw if raw is not None else 'aucune'} »",
           f"Memory read (READ_CORE_RAM 0 16), reply \"{raw if raw is not None else 'none'}\""))
    if data is None:
        say("")
        say(tr("Résultat", "Result"))
        for line in explain_failure(raw, version, core):
            say(line)
        return 1
    layout = layout_for(game, st["system"])
    size = layout.readable_size(client)          # lit la mémoire : une seule fois, hors de tr()
    say(tr(f"La mémoire se lit ({size} octets visibles).", f"Memory is readable ({size} bytes visible)."))
    if game:
        values = game_values(game, st["content"])
        defs, outside, todo = {}, [], []
        for name, d in values.items():
            if not isinstance(d, dict):
                continue
            span = value_span(d)
            if span is None:
                todo.append(name)
            elif layout.contains(*span):
                defs[name] = d
            else:
                outside.append(name)
        vals = read_values(client, layout, defs) if defs else {}
        for k, v in derive(game.get("derived"), vals).items():     # personnage en train de se battre...
            if v is not None:
                vals[k] = v
        if vals:
            shown = {k: v for k, v in vals.items() if k not in HIDDEN and not k.startswith("_")}
            say(tr("Valeurs lues  ", "Values read  ")
                + ", ".join(f"{label(k)} {v}" for k, v in sorted(shown.items(), key=lambda kv: label(kv[0]))))
        if outside:
            say(tr("Lisibles seulement avec MAME  ", "Readable only with MAME  ") + ", ".join(sorted(label(k) for k in outside)))
        if todo:
            say(tr("À apprendre avec learn.bat  ", "To learn with learn.bat  ") + ", ".join(sorted(label(k) for k in todo)))
    say("")
    say(tr("Résultat", "Result"))
    if template:
        say(tr("La mémoire se lit. La scène commune s'affiche déjà. Apprends le score avec learn.bat pour l'ajouter.",
               "Memory is readable. The shared scene is already displayed. Learn the score with learn.bat to add it."))
    elif game:
        say(tr("Tout est bon. Les valeurs de ce jeu peuvent s'afficher sur la dalle.",
               "All good. This game's values can be shown on the panel."))
    else:
        say(tr("La mémoire se lit. Pour ce jeu, il faut d'abord apprendre ses adresses avec learn.bat.",
               "Memory is readable. For this game, first learn its addresses with learn.bat."))
    return 0
