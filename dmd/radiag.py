"""test_retroarch.bat : RetroArch répond-il, quel cœur tourne, la mémoire du jeu se lit-elle ?

Ne modifie rien. Le résultat s'affiche et va aussi dans runtime/test_retroarch.txt.
"""

import os
import sys
import time

from . import wincore
from .learn import load_games
from .memvalues import derive, game_values, value_span
from .retroarch import (RetroArchClient, core_label, explain_failure, find_core, layout_for, match_game,
                        read_values, too_old)

LABELS = {"lives": "vies", "lives_p2": "vies J2", "bombs": "bombes", "bombs_p2": "bombes J2",
          "ammo": "munitions", "ammo_p2": "munitions J2", "weapon": "arme", "credits": "crédits",
          "time": "temps", "rings": "anneaux", "prisoners": "prisonniers", "score_p2": "score J2",
          "weapon_p2": "arme J2", "health": "vie J1 %", "health_p2": "vie J2 %",
          "p1_char": "perso J1", "p2_char": "perso J2", "beat": "BEAT BY J1", "beat_p2": "BEAT BY J2"}


HIDDEN = {"p1_mode", "p2_mode"}      # état des joueurs donné par le BIOS, utile à la scène seulement


def label(name):
    return LABELS.get(name, name)


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

    say("Test de RetroArch")
    say("")
    if not ra.get("enabled", True):
        say("Attention, la lecture de RetroArch est coupée dans config.json (retroarch, enabled).")
    st = client.status()
    if not playing(st) and wait > 0:
        say("Lance un jeu dans RetroArch, par exemple Metal Slug.")
        mins = max(1, round(wait / 60))
        say(f"Le test démarre tout seul dès que le jeu tourne (attente de {mins} minute{'s' if mins > 1 else ''} au plus).")
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
            f.write(time.strftime("%d/%m/%Y %H:%M") + "\n" + "\n".join(lines) + "\n")
        out("Ce résultat est aussi dans runtime\\test_retroarch.txt" if sys.platform == "win32"
            else "Ce résultat est aussi dans runtime/test_retroarch.txt")
    except OSError:
        pass
    return rc


def not_responding(port, say):
    say("RetroArch ne répond pas.")
    procs = wincore.find_retroarch()
    if not procs:
        say("RetroArch n'est pas lancé, ou ses commandes réseau sont coupées (voir LISEZMOI, section RetroArch).")
        return
    exe = procs[0]["exe"]
    say(f"Pourtant RetroArch tourne ({exe}).")
    radir = os.path.dirname(exe) if os.path.isabs(exe) else ""
    rcfg = wincore.read_cfg(os.path.join(radir, "retroarch.cfg")) if radir else {}
    if rcfg.get("network_cmd_enable") == "false":
        say("Le réglage Commandes réseau est désactivé dans RetroArch. Active-le (voir LISEZMOI, section RetroArch).")
    elif rcfg.get("network_cmd_port") and rcfg["network_cmd_port"] != str(port):
        say(f"RetroArch écoute sur le port {rcfg['network_cmd_port']} et ArcadeDMD sur le port {port}. "
            "Mets le même numéro des deux côtés.")
    else:
        say("Vérifie que le réglage Commandes réseau est activé (voir LISEZMOI, section RetroArch).")


def report(root, client, st, port, say):
    if st is None:
        not_responding(port, say)
        return 1
    if not playing(st):
        say("RetroArch répond, mais aucun jeu ne tourne. Lance un jeu puis relance ce test.")
        return 1
    version = client.version() or ""
    say(f"RetroArch {version} répond sur le port {port}.".replace("  ", " "))
    if too_old(version):
        say("Cette version est trop ancienne pour lire la mémoire des jeux. Il faut RetroArch 1.19 ou plus récent.")
    say(f"Jeu en cours {st['content']}, système {st['system']}.")
    core = find_core(st["content"])
    if core:
        say(f"Cœur chargé {core_label(core)}.")
    elif sys.platform == "win32":
        say("Je n'arrive pas à voir quel cœur est chargé.")
    games = load_games(root)
    key, game = match_game(games, st["content"], st["system"])
    template = bool(game and game.get("fallback"))
    if template:
        say(f"Pas de fichier propre à ce jeu, scène commune games/{key}.json.")
    else:
        say(f"Fichier ArcadeDMD games/{key}.json." if key else "Aucun fichier dans games pour ce jeu.")
    say("")
    data = client.read(0, 16)
    raw = client.last_reply
    say(f"Lecture de la mémoire (READ_CORE_RAM 0 16), réponse « {raw if raw is not None else 'aucune'} »")
    if data is None:
        say("")
        say("Résultat")
        for line in explain_failure(raw, version, core):
            say(line)
        return 1
    layout = layout_for(game, st["system"])
    say(f"La mémoire se lit ({layout.readable_size(client)} octets visibles).")
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
            say("Valeurs lues  " + ", ".join(f"{label(k)} {v}" for k, v in sorted(shown.items(), key=lambda kv: label(kv[0]))))
        if outside:
            say("Lisibles seulement avec MAME  " + ", ".join(sorted(label(k) for k in outside)))
        if todo:
            say("À apprendre avec apprendre.bat  " + ", ".join(sorted(label(k) for k in todo)))
    say("")
    say("Résultat")
    if template:
        say("La mémoire se lit. La scène commune s'affiche déjà. Apprends le score avec apprendre.bat pour l'ajouter.")
    elif game:
        say("Tout est bon. Les valeurs de ce jeu peuvent s'afficher sur la dalle.")
    else:
        say("La mémoire se lit. Pour ce jeu, il faut d'abord apprendre ses adresses avec apprendre.bat.")
    return 0
