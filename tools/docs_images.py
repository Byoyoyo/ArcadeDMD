"""Pictures of the README (docs/images), made with the real code of ArcadeDMD and simulated values.

Writes led_fight.gif (King of Fighters '98, from the game logo to the fight), led_metal_slug.gif, led_shooter.gif
(Aero Fighters 2, the simple panel of the shoot'em ups and its plane), hd_coin_screen.jpg (the coin screen of an
MVS, 1 credit on the left and 2 on the right) and hd_capcom_stages.jpg (four Capcom fighting games on their stages). In English, like the other pictures. The game logo is the
"GAME LOGO / Clear Logo from LaunchBox" badge, kept in a fake LaunchBox folder, never a real logo.

Images du README faites avec le vrai code d'ArcadeDMD et des valeurs simulées.

usage: python tools/docs_images.py [out_folder [picture ...]]      (docs/images and every picture by default,
       needs pygame and Pillow)
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["ARCADEDMD_LANG"] = "en"
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
TMP = tempfile.mkdtemp(prefix="arcadedmd_docs_")
KIT = os.path.join(TMP, "kit")
shutil.copytree(ROOT, KIT, ignore=shutil.ignore_patterns(".git", "runtime", "__pycache__", "learned", "obs", "dist", "artwork",
                                                         "appris"))
sys.path.insert(0, KIT)
import pygame  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from dmd import app  # noqa: E402
from dmd.i18n import set_language  # noqa: E402
from dmd.memvalues import derive  # noqa: E402
from dmd.outputs import LedRenderer, PreviewOutput  # noqa: E402

set_language("en")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "images")
W, H = 1920, 460
FPS = 25
LOG = app.Logger(None, echo=False)
CFG = app.load_config(KIT, LOG)
CFG = dict(CFG, retroarch={"enabled": False}, textfiles={"enabled": False})


def placeholder_logo():
    img = Image.new("RGBA", (1000, 250), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([8, 8, 992, 242], radius=40, fill=(30, 34, 52, 200), outline=(230, 230, 240, 255), width=8)
    f = ImageFont.truetype(os.path.join(KIT, "fonts", "InterDisplay-BlackItalic.otf"), 118)
    d.text((500, 112), "GAME LOGO", font=f, fill=(245, 245, 250, 255), anchor="mm")
    f2 = ImageFont.truetype(os.path.join(KIT, "fonts", "Inter-Bold.otf"), 40)
    d.text((500, 200), "Clear Logo from LaunchBox", font=f2, fill=(170, 176, 196, 255), anchor="mm")
    return img


LB = os.path.join(TMP, "launchbox")
os.makedirs(os.path.join(LB, "Data", "Platforms"))
os.makedirs(os.path.join(LB, "Images", "Arcade", "Clear Logo"))
with open(os.path.join(LB, "Data", "Platforms", "Arcade.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" standalone="yes"?>\n<LaunchBox>\n  <Game><Title>The King of Fighters \'98: The Slugfest</Title>'
            '<ApplicationPath>..\\Roms\\FBNeo\\kof98.zip</ApplicationPath><Platform>Arcade</Platform></Game>\n</LaunchBox>')
placeholder_logo().save(os.path.join(LB, "Images", "Arcade", "Clear Logo", "The King of Fighters _98_ The Slugfest-01.png"))


def hd_output():
    out = PreviewOutput({"enabled": True, "x": 0, "y": 0, "width": W, "height": H, "mode": "always", "style": "hd",
                         "launchbox": LB}, lambda m: None)
    t0 = time.time()
    while not out.hd_view.logos.ready and time.time() - t0 < 10:
        time.sleep(0.05)
    clock = [0.0]
    out.hd_view.clock = lambda: clock[0]
    return out, clock


def save_gif(frames, path):
    while len(frames) > 1 and frames[0].getextrema()[0][1] < 40 and frames[0].convert("L").getextrema()[1] < 40:
        frames = frames[1:]                               # no black frames at the start / pas d'images noires au début
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)
    if shutil.which("gifsicle"):
        subprocess.run(["gifsicle", "-O3", "--colors", "256", "--batch", path], check=False)
    print(path, len(frames), "frames", os.path.getsize(path) // 1024, "KB")


def led_fight():
    """King of Fighters '98: the logo, the coin screen, two coins, PRESS START, then the fight."""
    out, clock = hd_output()
    eng = app.Engine(KIT, CFG, [out], LOG, demo_game="kof98")
    eng.sim = None                                    # values driven here / valeurs pilotées ici
    eng.demo_until = None
    for k in ("health", "health_p2", "time"):
        eng.state.values.pop(k, None)
    v = {"p1_mode": 0, "p2_mode": 0, "credits": 0, "score": 0, "backdrop": 5, "stage": 0,
         "_p1_lost": 0, "_p1_ch0": 0, "_p1_ch1": 1, "_p1_ch2": 2, "_p1_ord0": 0, "_p1_ord1": 1, "_p1_ord2": 2,
         "_p2_lost": 0, "_p2_ch0": 21, "_p2_ch1": 22, "_p2_ch2": 23, "_p2_ord0": 0, "_p2_ord1": 1, "_p2_ord2": 2}
    events = [(3.4, {"credits": 1}), (4.9, {"credits": 2}),
              (9.4, {"p1_mode": 1, "credits": 1, "health": 100, "health_p2": 100, "time": 60}),
              (10.6, {"health_p2": 88, "score": 600}), (11.1, {"health_p2": 80, "score": 1000}), (11.5, {"health": 92}),
              (12.2, {"health_p2": 62, "score": 2800})]
    led = LedRenderer(6)
    frames, tick = [], 10.4
    for i in range(int(13.0 * FPS)):
        t = i / FPS
        clock[0] = t
        while events and events[0][0] <= t:
            v.update(events.pop(0)[1])
        if v.get("time") and t >= tick:
            v["time"] -= 1
            tick += 1.0
        for k, val in v.items():
            eng.state.update(k, val, t)
        if eng.derived:
            for k, val in derive(eng.derived, eng.state.values).items():
                eng.state.update(k, val, t, quiet=True)
        frame = eng.step(t)
        out.hd_next = 0.0
        out.send(frame)
        if i % 2 == 0:
            frames.append(led.render(frame).convert("RGB"))
    out.close()
    save_gif(frames, os.path.join(OUT, "led_fight.gif"))


def led_demo(game, name, t_from, t_to):
    """The demo of a game, as demo_neogeo.bat plays it. / La démo d'un jeu."""
    eng = app.Engine(KIT, CFG, [], LOG, demo_game=game)
    led = LedRenderer(6)
    frames = []
    for i in range(int(t_to * FPS)):
        t = i / FPS
        frame = eng.step(t)
        if t >= t_from and i % 2 == 0:
            frames.append(led.render(frame).convert("RGB"))
    save_gif(frames, os.path.join(OUT, name))


def hd_capcom_stages():
    """Four Capcom fighting games on their own stages (the backdrop value read in the game), the place under the stage."""
    out, clock = hd_output()
    shots = []
    t = 0.0
    for game, back, p1, p2, power in (("sf2ce", 0, 0, 3, None), ("sfa3", 0x22, 1, 9, (60, 100)), ("vsav", 0, None, None, None),
                                      ("xmcota", 9, 0, 4, (35, 80))):
        eng = app.Engine(KIT, CFG, [out], LOG, demo_game=game)
        eng.sim = None
        eng.demo_until = None
        v = {"p1_mode": 1, "p2_mode": 0, "credits": 1, "health": 100, "health_p2": 100, "time": 99, "backdrop": back}
        if p1 is not None:
            v.update({"_p1_chr": p1, "_p2_chr": p2})
        if power:
            v.update({"power": power[0], "power_p2": power[1]})
        for k in range(int(3.0 * FPS)):
            t += 1 / FPS
            clock[0] = t
            if k == int(1.2 * FPS):
                v.update({"health_p2": 72, "time": 97})
            for key, val in v.items():
                eng.state.update(key, val, t)
            if eng.derived:
                for key, val in derive(eng.derived, eng.state.values).items():
                    eng.state.update(key, val, t, quiet=True)
            frame = eng.step(t)
            out.hd_next = 0.0
            out.send(frame)
        shots.append(Image.frombytes("RGB", (W, H), pygame.image.tostring(out.screen, "RGB")))
    out.close()
    sheet = Image.new("RGB", (W, H * len(shots)))
    for i, im in enumerate(shots):
        sheet.paste(im, (0, i * H))
    path = os.path.join(OUT, "hd_capcom_stages.jpg")
    sheet.save(path, quality=84)
    print(path, os.path.getsize(path) // 1024, "KB")


def hd_coin_screen():
    """The coin screen of an MVS under RetroArch: two coins on the left, the right door gives 2 credits."""
    out, clock = hd_output()
    eng = app.Engine(KIT, CFG, [out], LOG)
    names = ["bios_request", "bios_mode", "bios_timer", "bios_mvs", "p1_mode", "p2_mode", "health", "health_p2", "time"]
    eng.handle_event({"t": "start", "game": "kof98", "system": "kof98", "description": "The King of Fighters '98",
                      "values": names}, 0.0, "retroarch")
    bios = {"bios_request": 2, "bios_mode": 1, "bios_timer": 0, "bios_mvs": 0x80, "p1_mode": 0, "p2_mode": 0}
    coins = [3.4, 4.9]
    best = None
    for i in range(int(6.2 * FPS)):
        t = i / FPS
        clock[0] = t
        if coins and t >= coins[0]:
            coins.pop(0)
            eng.coin_in(0, t)
            bios = dict(bios, bios_request=3, bios_timer=30)
        eng.handle_event({"t": "v", "v": bios}, t, "retroarch")
        frame = eng.step(t)
        out.hd_next = 0.0
        out.send(frame)
        cd = out.hd_view.coins
        if cd is not None and cd.last_land is not None and 0.34 <= t - cd.last_land <= 0.42 and cd.shown == 2:
            best = Image.frombytes("RGB", (W, H), pygame.image.tostring(out.screen, "RGB"))
    out.close()
    path = os.path.join(OUT, "hd_coin_screen.jpg")
    best.save(path, quality=88)
    print(path, os.path.getsize(path) // 1024, "KB")


ALL = {"led_fight": led_fight, "led_metal_slug": lambda: led_demo("mslug", "led_metal_slug.gif", 0.0, 12.0),
       "led_shooter": lambda: led_demo("sonicwi2", "led_shooter.gif", 11.0, 25.0), "hd_coin_screen": hd_coin_screen,
       "hd_capcom_stages": hd_capcom_stages}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pygame.init()
    for name in sys.argv[2:] or ALL:                  # only some pictures: docs_images.py docs/images hd_capcom_stages
        ALL[name]()
    shutil.rmtree(TMP, ignore_errors=True)
