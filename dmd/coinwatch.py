"""test_coins.bat: what the Neo Geo BIOS does when a coin goes in, with RetroArch.

An MVS keeps its credits, and the coin slot each coin came through, in the backup RAM of the cabinet, which the
FinalBurn Neo core does not share. ArcadeDMD guesses the credits from the traces the BIOS leaves in the work RAM
(dmd/neocoins.py). This test watches that part of the memory while you put coins in on the left and on the right, and
writes each change down with its time, to find what tells the coins and their side apart. It changes nothing. The
result is shown and also written to runtime/test_coins.txt.

test_coins.bat : ce que fait le BIOS de la Neo Geo quand une pièce entre, avec RetroArch.

La MVS range ses crédits, et le monnayeur de chaque pièce, dans la mémoire de sauvegarde de la borne, que le cœur
FinalBurn Neo ne partage pas. Ce test surveille la mémoire du BIOS pendant que tu mets des pièces à gauche et à droite,
et note chaque changement avec son heure. Il ne modifie rien. Le résultat va aussi dans runtime/test_coins.txt.
"""

import os
import sys
import time

from .coinbuttons import CoinButtons, mvs_rates, side_word
from .i18n import tr
from .learn import load_games
from .neocoins import NeoCoins
from .retroarch import RetroArchClient, layout_for, match_game

WATCH = (0x10FC00, 0x10FFFF)              # the BIOS work RAM / la mémoire de travail du BIOS
NAMES = {0x10FD80: "BIOS_SYSTEM_MODE", 0x10FD81: "BIOS_SYSRET_STATUS", 0x10FD82: "BIOS_MVS_FLAG",
         0x10FDAC: "BIOS_STATCURNT", 0x10FDAD: "BIOS_STATCHANGE", 0x10FDAE: "BIOS_USER_REQUEST", 0x10FDAF: "BIOS_USER_MODE",
         0x10FDB0: "BIOS_CREDIT_DEC1", 0x10FDB1: "BIOS_CREDIT_DEC2", 0x10FDB2: "BIOS_CREDIT_DEC3", 0x10FDB3: "BIOS_CREDIT_DEC4",
         0x10FDB4: "BIOS_START_FLAG", 0x10FDB6: "BIOS_PLAYER_MOD1", 0x10FDB7: "BIOS_PLAYER_MOD2",
         0x10FDDA: "BIOS_COMPULSION_TIMER", 0x10FDDB: "BIOS_COMPULSION_FRAME_TIMER", 0x10FE00: "dev credits P1",
         0x10FE01: "dev credits P2", 0x10FEC5: "BIOS_TITLE_MODE", 0x10FEDC: "BIOS_STATCURNT_RAW",
         0x10FEDD: "BIOS_STATCHANGE_RAW", 0x10FEE1: "BIOS_FRAME_SKIP"}
# always moving: frame counters, joysticks, clock / bougent tout le temps : compteurs d'images, manettes, horloge
NOISY = set(range(0x10FE88, 0x10FE8C)) | {0x10FEE4, 0x10FDDB} | set(range(0x10FD94, 0x10FDAC)) | set(range(0x10FDD2, 0x10FDD9))
QUIET_LIMIT = 6                           # more changes than that in 3 seconds: a counter, left aside / un compteur


def playing(st):
    return bool(st) and st.get("state") in ("PLAYING", "PAUSED")


def run(root, cfg, seconds=150, out=print, poll=0.05, client=None, buttons=None):
    ra = cfg.get("retroarch", {}) or {}
    client = client or RetroArchClient(ra.get("host", "127.0.0.1"), int(ra.get("port", 55355)), timeout=0.5)
    lines = []

    def say(text=""):
        out(text)
        lines.append(text)

    say(tr("Test des pièces (Neo Geo sous RetroArch)", "Coin test (Neo Geo with RetroArch)"))
    say("")
    st = client.status()
    if not playing(st):
        say(tr("Lance un jeu Neo Geo dans RetroArch, par exemple Aero Fighters 2 ou King of Fighters '98.",
               "Start a Neo Geo game in RetroArch, for example Aero Fighters 2 or King of Fighters '98."))
        end = time.monotonic() + 180
        while time.monotonic() < end and not playing(st):
            time.sleep(1.0)
            st = client.status()
        if not playing(st):
            say(tr("Aucun jeu ne tourne dans RetroArch, test arrêté.", "No game is running in RetroArch, test stopped."))
            return _save(root, lines, out, 1)
    key, game = match_game(load_games(root), st["content"], st["system"])
    layout = layout_for(game, st["system"])
    if not layout.contains(*WATCH):
        say(tr(f"{st['content']} n'est pas un jeu Neo Geo pour ArcadeDMD, test arrêté.",
               f"{st['content']} is not a Neo Geo game for ArcadeDMD, test stopped."))
        return _save(root, lines, out, 1)
    say(tr(f"Jeu {st['content']}. Je note pendant {seconds} secondes ce qui change dans la mémoire du BIOS.",
           f"Game {st['content']}. For {seconds} seconds I write down what changes in the memory of the BIOS."))
    say(tr("Retourne dans le jeu, puis, en attendant 5 secondes entre chaque geste",
           "Go back to the game, then, waiting 5 seconds between each step"))
    for step in (tr("1. une pièce avec le monnayeur de gauche", "1. a coin through the left slot"),
                 tr("2. une pièce avec le monnayeur de droite", "2. a coin through the right slot"),
                 tr("3. encore une à gauche", "3. one more on the left"),
                 tr("4. encore une à droite", "4. one more on the right"),
                 tr("5. Start à gauche, et une fois la partie commencée, une pièce à droite",
                    "5. Start on the left, and once the game has started, a coin on the right"),
                 tr("6. une pièce à gauche pendant la partie", "6. a coin on the left during the game")):
        say("   " + step)
    say(tr("Le test s'arrête tout seul. Envoie ensuite runtime\\test_coins.txt.",
           "The test stops by itself. Then send runtime\\test_coins.txt."))
    say("")
    guess = NeoCoins(mvs_rates(cfg))
    if buttons is None:                                  # coin_buttons.bat done: each press is written down too
        buttons = CoinButtons.from_config(cfg, say)
    prev = None
    changes = {}                                       # address: recent times / adresse : moments récents
    loud = set()
    t0 = time.monotonic()
    fails = 0
    while time.monotonic() - t0 < seconds:
        got = layout.read_cpu(client, WATCH[0], WATCH[1])
        now = time.monotonic() - t0
        if got is None:
            fails += 1
            if fails > 40:
                say(tr("RetroArch ne répond plus, test arrêté.", "RetroArch no longer answers, test stopped."))
                break
            time.sleep(0.2)
            continue
        fails = 0
        base, data = got
        if prev is not None:
            for i, (a, b) in enumerate(zip(prev, data)):
                if a == b:
                    continue
                addr = base + i
                if addr in NOISY or addr in loud:
                    continue
                seen = [x for x in changes.get(addr, []) if now - x < 3.0] + [now]
                changes[addr] = seen
                if len(seen) > QUIET_LIMIT:
                    loud.add(addr)
                    say(tr(f"{now:7.2f} s  ${addr:06X}  bouge tout le temps, je ne le note plus",
                           f"{now:7.2f} s  ${addr:06X}  keeps moving, no longer written down"))
                    continue
                name = NAMES.get(addr, "")
                say(f"{now:7.2f} s  ${addr:06X}  {a:3d} -> {b:3d}  ({a:02X} -> {b:02X})  {name}".rstrip())
        vals = {"bios_request": data[0x10FDAE - base], "bios_mode": data[0x10FDAF - base],
                "bios_timer": _bcd(data[0x10FDDA - base]), "bios_mvs": data[0x10FD82 - base],
                "p1_mode": data[0x10FDB6 - base], "p2_mode": data[0x10FDB7 - base]}
        before = guess.coins
        for side in (buttons.poll() if buttons is not None else []):
            say(tr(f"{now:7.2f} s  bouton des pièces à {side_word(side)}", f"{now:7.2f} s  coin button on the {side_word(side)}"))
            guess.add(side, now)
        c = guess.update(vals, now)
        for fr, en in guess.notes:
            say(f"{now:7.2f} s  " + tr(fr, en))
        guess.notes.clear()
        if guess.coins > before:
            say(tr(f"{now:7.2f} s  ArcadeDMD voit une pièce, crédits devinés {c}",
                   f"{now:7.2f} s  ArcadeDMD sees a coin, credits guessed {c}"))
        prev = data
        time.sleep(poll)
    if buttons is not None:
        buttons.close()
    say("")
    say(tr("Fin du test.", "End of the test."))
    return _save(root, lines, out, 0)


def _bcd(b):
    hi, lo = b >> 4, b & 15
    return (hi if hi < 10 else 0) * 10 + (lo if lo < 10 else 0)


def _save(root, lines, out, rc):
    path = os.path.join(root, "runtime", "test_coins.txt")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(time.strftime(tr("%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M")) + "\n" + "\n".join(lines) + "\n")
        out(tr("Ce résultat est aussi dans runtime\\test_coins.txt", "This result is also in runtime\\test_coins.txt")
            if sys.platform == "win32"
            else tr("Ce résultat est aussi dans runtime/test_coins.txt", "This result is also in runtime/test_coins.txt"))
    except OSError:
        pass
    return rc
