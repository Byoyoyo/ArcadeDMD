# ArcadeDMD

Version française : [README.fr.md](README.fr.md)

Live score, lives, credits and game events from MAME and RetroArch games, shown on the marquee of an arcade cabinet, with an animated scene for each game. On a 128x32 LED panel (**Pixelcade LED**, **ZeDMD**), or in smooth HD on an LCD marquee screen (a 1920 x 460 Vewlix marquee, for example).

![Fighting game on an LCD marquee, HD display](docs/images/hd_fight.jpg)
![Coin screen of a fighting game on an LCD marquee, HD display](docs/images/hd_coin_screen.jpg)
![Metal Slug on an LCD marquee, HD display](docs/images/hd_metal_slug.jpg)
![Game logo, coin screen and fight on a 128x32 LED panel](docs/images/led_fight.gif)
![Metal Slug on a 128x32 LED panel](docs/images/led_metal_slug.gif)

- Reads the game memory live, with a MAME plugin or through RetroArch's network commands (FinalBurn Neo, Genesis Plus GX). Nothing in the game or the emulator is modified.
- Ready-made scenes for Metal Slug 1 to 5 and X, the 57 Neo Geo fighting games, ninety-seven Neo Geo games done one by one (Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers, Neo Turf Masters, Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11, Sengoku 3, Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2, Aero Fighters 3, Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally, Magician Lord, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army, Burning Fight, Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger, Puzzle De Pon!, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks, Super Sidekicks 2, Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf, Power Spikes II, Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa, Puzzled, Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords, Eight Man, Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2, Shougi no Tatsujin), every other Neo Geo game by genre, every Capcom CPS1, CPS2 and CPS3 game (34 fighting games on their own stages and fifty games done one by one, from Final Fight to 1944), After Burner II, Sonic 1 and 2.
- HD scenes with animated backgrounds that follow the game's stage or mission, and an effect for every event (hits, combos, K.O., weapons, bombs, coins...).
- The game's logo when it starts (your LaunchBox Clear Logo). With nobody playing, the fighting games wait for a coin. Insert one and it drops into the slot, the credits roll, then PRESS START.
- A learning tool finds the missing addresses (score, credits...) from a few captures.
- English and French. Windows, Python 3.12 or newer.

How it works, in one sentence. A MAME plugin reads the values from the game's RAM, and a small Python program draws the scene and sends it over USB to the panel, or shows it on an LCD screen used as a DMD (section 3).

Download the latest version from the [Releases](../../releases) page, then follow section 2. The changes of each version are in [CHANGELOG.md](CHANGELOG.md), and the progress game by game, with what comes next, in [PROGRESS.md](PROGRESS.md). To report a problem or ask for a new game, see [CONTRIBUTING.md](CONTRIBUTING.md).

Already have a Pixelcade LED? It does the job on its own, no need to buy a panel. Go straight to sections 2 and 4. For games launched in RetroArch (Metal Slug, Sonic...), also read section 7.

What's in the folder

| File | Purpose |
|---|---|
| `install.bat` | installs everything (Python required, see below) |
| `demo_afterburner.bat`, `demo_sonic.bat` | show the scenes with simulated values, without MAME |
| `run.bat` | starts the engine with the console visible |
| `learn.bat` | tool that finds a missing RAM address (score, credits...) |
| `test_pixelcade.bat` | test pattern on the Pixelcade LED |
| `screen_setup.bat` | puts the scene on an LCD screen used as a DMD, as virtual LEDs or in smooth HD with the game logo (section 3) |
| `demo_fight.bat` | fighting game demo (King of Fighters '98) with simulated values |
| `demo_neogeo.bat` | demo of a Neo Geo game done one by one (Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers, Neo Turf Masters, Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11, Sengoku 3, Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2, Aero Fighters 3, Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally, Magician Lord, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army, Burning Fight, Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger, Puzzle De Pon!, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks, Super Sidekicks 2, Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf, Power Spikes II, Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa, Puzzled, Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords, Eight Man, Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2, Shougi no Tatsujin) with simulated values |
| `demo_capcom.bat` | demo of a Capcom CPS1, CPS2 or CPS3 game with simulated values |
| `test_retroarch.bat` | checks RetroArch, the loaded core and memory reading (section 7) |
| `test_coins.bat` | writes down what the Neo Geo BIOS does when a coin goes in with RetroArch, to send if a coin does not drop (section 7) |
| `coin_buttons.bat` | shows ArcadeDMD your two coin buttons and your two START buttons, so that it sees every coin and its side, and every player who begins, with RetroArch (section 7) |
| `ports.bat` | lists the COM ports, to find the Pixelcade's port |
| `test_panel.bat` | test pattern on a ZeDMD panel |
| `config.json` | your settings (Pixelcade, RetroArch, virtual LED window...), created by the installer from `config.default.json`. A new version of ArcadeDMD never overwrites it |
| `games\*.json` | one file per game, with the RAM addresses and the scene. The `neogeo*.json` files are shared scenes for Neo Geo games, one per genre, and the `cps_*.json` files the shared scenes of the Capcom games |
| `learned\` | copy of the addresses found by `learn.bat`. Restored automatically after an update |
| `mame-plugin\arcadedmd` | the plugin to copy into `MAME\plugins` (the installer does it) |
| `sprites\` | small sprites (plane, ring). You can add your own |
| `obs\` | text files updated live for OBS, VS match history and streak records (section 11) |
| `fonts\` | Inter and Black Ops One fonts for the HD display (free OFL license, in `fonts\OFL.txt` and `fonts\OFL-BlackOpsOne.txt`) |

---

## 1. Hardware (only if you don't have a Pixelcade)

A 128x32 RGB DMD is two 64x32 HUB75 LED modules side by side. This is exactly the ZeDMD format, the well-known open-source DMD from the virtual pinball world. ArcadeDMD relies on it for the panel side.

### Option A, the easiest (plug-and-play kit)

Some shops sell assembled ZeDMDs or ready-to-use boards, for example in France.
- SmallCab, "Pack ZeDMD S3 – P2.5" https://www.smallcab.net/pack-zedmd-p-3182.html
- Benfactory, "ZeDMD" https://benfactory.fr/produit/zedmd/

At P2.5 (2.5 mm between two LEDs) the panel is about 32 × 8 cm. That is the size of a pinball DMD. Check on the product page what is included (power supply, frame).

### Option B, a bigger panel

With bigger LEDs (P4 or P5), the panel fills the top of a cabinet. Measure the top of your cabinet and choose.

| Pitch | Size of one 64x32 module | Full 128x32 panel |
|---|---|---|
| P3 | 19.2 × 9.6 cm | 38 × 10 cm |
| P4 | 25.6 × 12.8 cm | 51 × 13 cm |
| P5 | 32 × 16 cm | 64 × 16 cm |

Shopping list for option B (approximate prices)

| Qty | Item | Note |
|---|---|---|
| 2 | RGB HUB75 LED module 64x32, indoor, 1/16 scan | Waveshare P4 around $18 each, cheaper on AliExpress |
| 1 | ESP32-S3-DevKitC-1 **N16R8** | around €10 to €15, the board recommended by ZeDMD |
| 1 | ZeDMD shield for ESP32-S3 (SmallCab, Benfactory, Arnoz) | saves you from wiring 14 wires by hand, and adds the menu buttons |
| 1 | 5 V 10 A power supply (Mean Well LRS-50-5 type) | a module can draw 4 A at full white, but a DMD stays far below that |
| 1 | USB-C **data** cable | to the cabinet PC |

Avoid "outdoor" modules and 1/8 scan modules. Modules with FM6126A or ICN2038S chips work too, as long as you set the "panel driver" with ZeDMD_Updater2.

### Assembly

1. Plug the shield into the HUB75 input of the first module (the arrow printed on the back shows the data direction).
2. Connect the output of module 1 to the input of module 2 with the supplied ribbon cable.
3. Power both modules with 5 V from the power supply.
4. Connect the ESP32-S3 to the PC through its **native** USB port (the one marked USB, on the left on the DevKitC-1).

Without a shield, the wire-by-wire connections are given in the ZeDMD README ("ZeDMD pinout diagram" table) https://github.com/PPUC/ZeDMD

### Panel firmware

1. Download ZeDMD_Updater2 (Windows) https://github.com/zesinger/ZeDMD_Updater2 and flash the **ZeDMD S3 128x32** variant. Alternatively, flash the `.bin` file from the ZeDMD releases with esptool.
2. On first boot the panel shows a menu. Set the color order (red must be red), the brightness, "USB packet size" to 1024 and "min refresh" to around 90 Hz, then go to **Exit**.
3. If the panel comes from a pre-flashed kit, update the firmware anyway. Recent versions of the libzedmd library expect a recent firmware.

### Option C, an LCD screen instead of LEDs

An LCD screen shows the scenes in smooth HD, with the animated backgrounds (section 3). Any screen that Windows sees as an extra display works, plugged into the PC by HDMI, DisplayPort or USB-C. For a marquee, look for a "stretched bar LCD", a very long and thin screen. The same screens are sold for shelf-edge advertising and PC sensor panels.

Measure the marquee window of your cabinet first, then choose the biggest visible area that fits.

| Size | Resolution | Visible area, about | Note |
|---|---|---|---|
| 12.3" | 1920 × 720 | 29 × 11 cm | close to the size of a pinball DMD |
| 14.9" | 1280 × 390 | 36 × 11 cm | sold as a marquee kit for Vewlix-type cabinets |
| 19" | 1920 × 360 | 48 × 9 cm | |
| 24" | 1920 × 360 | 58 × 11 cm | the format of the LCD marquees made for the AtGames Legends Ultimate |

The HD scenes adapt to the screen. They were checked at 1920 × 360, 1280 × 390, 1920 × 480 and 1920 × 720.

Where to buy (prices seen in October 2026)
- AliExpress, Amazon or eBay. Search for "stretched bar LCD HDMI" followed by the resolution. Take a version sold with its HDMI controller board and its power supply. A bare panel (LVDS or eDP connector) needs a separate controller board. A 19" 1920 × 360 sold with its board was listed around $260 plus shipping on eBay, shipped from China, and a 24" around £250 plus shipping. The bare 24" module measures 61.3 × 13.2 cm and 1 cm thick, plan a frame to hold it in the marquee.
- Waveshare 12.3inch 1920x720 LCD, HDMI or USB-C, around $110, seen by Windows as a normal display https://www.waveshare.com/product/displays/12.3inch-1920x720-lcd.htm
- Arcade Game Sales, 14.9" 1280 × 390 LCD marquee with a metal frame, for Vewlix, Chewlix and Game Wizard Xtreme cabinets, around $225, VGA and HDMI https://arcade-game-sales.com/products/lcd-arcade-marquee-for-arcade-cabinets/19366-2.html
- A standard PC monitor also works, if the top of the cabinet is deep and tall enough to hold it. Hide what is outside the marquee window, and set the ArcadeDMD window to the visible band with `x`, `y`, `width` and `height` (section 3).

ArcadeDMD only draws on screens that Windows sees as displays. Check this before buying a marquee that comes with its own software, such as the Pixelcade LCD (it has its own small computer and is reached over the network) or the AtGames Legends BitLCD HD (it connects by USB and is driven by its own app).

---

## 2. Software

### Installation

1. You need Python 3.12 or newer. If it is missing, `install.bat` offers to install it (Python 3.13, from python.org). Otherwise install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH". You also need MAME 0.227 or newer. The installer shows your version.
2. Before extracting the zip, right-click it, choose Properties, tick "Unblock", then OK. Windows will then stop asking for confirmation on every .bat file.
3. Extract the `ArcadeDMD` folder to a path with no accented characters, ideally `C:\ArcadeDMD`. MAME cannot open folders with accented characters.
4. Run `install.bat`. It installs Pillow, pyserial and pygame-ce, copies the plugin into MAME, sets up the Pixelcade and offers to start ArcadeDMD automatically with Windows. It only downloads libzedmd (the ZeDMD panel driver) if you say you have a ZeDMD panel. If you only use RetroArch, press Enter at the MAME question.

### What the installation changes

- The `C:\ArcadeDMD` folder. Settings, the log and the captures stay inside it.
- In MAME, a new `plugins\arcadedmd` folder with three small files. Nothing else in MAME. `mame.ini` and `plugin.ini` are not modified, since MAME loads the plugins in its `plugins` folder by itself.
- An `ArcadeDMD.bat` file in the Windows Startup folder, only if you accept the automatic start.
- Three libraries added to Python (Pillow, pyserial, pygame-ce).
- During games that have a file in `games\` (Metal Slug, Neo Geo games, After Burner II, Sonic...), ArcadeDMD stops pixelweb and restarts it when the game ends. For other games, nothing changes.

The plugin only reads the game memory. It changes neither the game, nor the controls, nor MAME's settings.

### What about DOFLinx?

ArcadeDMD does not touch DOFLinx's files, nor the `output` setting in `mame.ini` that DOFLinx needs. MAME runs several plugins at once, and the DOFLinx and ArcadeDMD plugins do not get in each other's way. With the Pixelcade and without ZeDMD, ArcadeDMD opens no other COM port, so the devices driven by DOFLinx are not disturbed. The only thing they share is the Pixelcade itself. During After Burner II and Sonic, the Pixelcade shows ArcadeDMD's scene.

### Uninstalling

Delete the `plugins\arcadedmd` folder from MAME, the `ArcadeDMD.bat` file from the Startup folder (type `shell:startup` in Win+R to open it), then the `C:\ArcadeDMD` folder. To just turn the plugin off without deleting anything, add the line `arcadedmd 0` to MAME's `plugin.ini` file.

### libzedmd (ZeDMD panel only)

If the libzedmd download fails, get the `win-mingw-x64-Release` archive from https://github.com/PPUC/libzedmd/releases and copy all its DLLs into `ArcadeDMD\libzedmd\`. Make sure you take the mingw version, because the other archive does not include the DLLs that zedmd64.dll needs.

### Checking the plugin in MAME

Start a game, press Tab, then go to "Plugin Options". You should see **ArcadeDMD** with the detected game and the values read live. If it does not appear, check in MAME's Plugins menu that it is enabled, or add the line `arcadedmd 1` to `plugin.ini` (in the MAME folder or in `ini\`).

The plugin needs no setting in your frontend (HyperSpin, LaunchBox...). MAME loads it every time it starts.

### First try without MAME

`demo_afterburner.bat` and `demo_sonic.bat` open a "virtual LED" window with simulated values. If the panel is connected, it shows the same thing.

### Running it for real

Launch `run.bat` (or let the automatic start do it), then start a game from your frontend or directly in MAME. The Pixelcade switches to ArcadeDMD during games that have their file in `games\` and stays with pixelweb the rest of the time. A ZeDMD panel, on the other hand, stays black outside games, and shows the scrolling title for a game with no dedicated file. The old idle screen (the time and "INSERT COIN") comes back with `"idle": {"show": true}` in `config.json`.

### Language

Messages and on-screen texts are in English by default. They switch to French automatically when Windows is in French. To choose the language, set `"language"` in `config.json`, at the top level (not inside a section). `"auto"` follows the Windows language (default), `"en"` forces English and `"fr"` forces French.

```json
"language": "en"
```

---

## 3. LCD screen or marquee as "virtual LEDs"

ArcadeDMD can draw the scene on any additional screen, for example a cabinet LCD used as a DMD, or a 1920×470 marquee. It works with RetroArch as well as with MAME.

The easiest way is to run `screen_setup.bat` (the installer offers it too). It lists the screens, guesses which one is the DMD (the most elongated one) and sets everything in `config.json`. Then launch `run.bat` or `demo_afterburner.bat` to see the result.

On a large screen, the scene is drawn twice as fine as on a real panel, 256 × 64 LEDs instead of 128 × 32, with smoothed letters and slopes. On a 1920 × 460 LCD, each LED is 7 pixels wide.

Manual setup, in the `preview` section of `config.json`

```json
"preview": {
  "enabled": true,
  "x": 1920, "y": 0,
  "width": 1920, "height": 460,
  "borderless": true,
  "topmost": true,
  "mode": "games",
  "takeover": "known",
  "hd": "auto",
  "style": "led"
}
```

- `x` and `y` are the position of the screen's top-left corner on the Windows desktop (Settings > Display). Here, an LCD placed to the right of a 1080p screen. If it is placed below it, use `"x": 0, "y": 1080`.
- `"hd"` is `"auto"` (finer as soon as the screen is large enough), `1` (same LED grid as a real 128 × 32 panel), `2` or `4` (finer still, for a very large screen).
- `"style"` is `"led"` (round LEDs, like a real panel) or `"pixel"` (square pixels, sharper on an LCD).
- `"mode": "games"` (the default) behaves as with the Pixelcade. Outside games, the window hides and the screen is left to the frontend, for example to BigBox clear logos and marquees. As soon as a known game starts, ArcadeDMD comes to the foreground, above the BigBox or HyperSpin marquee, without taking focus away from the game. If the frontend comes back in front during the game, ArcadeDMD returns to the front within a second. When the game ends, the screen goes back to the frontend immediately. `"mode": "always"` keeps the window shown all the time, black outside games.
- `"takeover": "known"` brings the window to the foreground only for games that have a file in `games\` (Metal Slug, King of Fighters, all Neo Geo games...). `"all"` does it for every MAME game, with the generic scene.
- `"topmost": true` keeps the window above the others while it is shown. Set `"enabled": false` if you only want the real panel.

---

### Smooth HD display, with the game logo

On an LCD screen, ArcadeDMD can also draw the scene directly at the screen's resolution, without the LED effect. Texts are smooth, health bars have gradients, and the game logo sits at the top center.

To turn it on, run `screen_setup.bat` again and choose 2 at the display question. Or set `"style": "hd"` in the `preview` section of `config.json`. ArcadeDMD notices by itself that `config.json` has changed and restarts with the new setting. Then run `demo_fight.bat`, or a game from BigBox.

The logo comes from your LaunchBox Clear Logo images. ArcadeDMD finds the LaunchBox folder by itself when BigBox is running, or in the usual locations (`C:\LaunchBox`, `E:\LaunchBox`...). Otherwise, set it in the `preview` section, for example `"launchbox": "E:\\LaunchBox"`. The running game is matched to its logo through the ROM path in LaunchBox, and through the parent game for a clone. When a game has no logo, its title is shown instead in metallic lettering.

- Fighting games. At the top, each player's score, or CHALLENGER and BEAT BY in a VS match. In the middle, the health bars, with a light trail showing the hit just taken, and the timer or KO. At the bottom, P1, P2 or CPU with the current fighter, the full team in King of Fighters '96 to 2000 (fighters already beaten are crossed out), and the credits, big, on a dark pill.
- Other games. The logo, each player's score, then at the bottom the weapon, lives, bombs, time and credits when they are known.
- Nobody playing. A large logo, and INSERT COIN or the credits. In the fighting games, the logo sits between two coin doors (Coin screen, section 7).
- The animated backdrops are a little darker, so that the information stands out. `"dim": 30` in the `preview` section sets it, from 0 (as drawn) to 80 percent.

The Pixelcade and ZeDMD panels keep the scene at 128 x 32, which is their LED resolution.

### Game logo when a game starts

When a game starts, its logo comes first. On the HD screen it arrives big on a dark screen, with a flash and a light sweep, then glides to its place in the scene. On the Pixelcade and ZeDMD panels it zooms in on the 128 x 32 LEDs, then the scene comes. The Pixelcade shows it as soon as pixelweb has handed the panel over.

![Game logo when a game starts, HD display](docs/images/hd_logo_intro.jpg)

It is the game's LaunchBox Clear Logo, found as described just above. On a panel, a game without a Clear Logo goes straight to its scene. On the HD screen, its title in metallic lettering is used instead.

```json
"intro": {
  "logo": true,
  "seconds": 2.6,
  "launchbox": ""
}
```

- `"logo": false` turns it off, on the panel and on the HD screen.
- `"seconds"` is how long it lasts, from 1 to 10 seconds.
- `"launchbox"` is the LaunchBox folder, when it is not found by itself. With a panel and no HD screen, set it here. The one in the `preview` section works too.

### Animated HD scenes, Metal Slug and fighting games

With the smooth HD display, the Metal Slug games and the fighting games get a full scene of their own. Everything is drawn by the program, no image comes from the games.

![Stage change in a fighting game](docs/images/hd_fight_stage.jpg)

- **Metal Slug.** One soldier panel per player, with the score, the weapon and its ammo gauge, the bombs, the lives and the rescued prisoners (first Metal Slug, X, 3 and 5). Shots follow the weapon (tracers and shell casings, shotgun blasts, rockets, flamethrower), bombs fly and explode in the backdrop, a crate drops when a weapon is picked up, the helmet falls when a life is lost and LAST LIFE blinks on the last one. In the tank of the first Metal Slug, the tank takes the place of the weapon, with its energy in hits (three, like in the game) and its cannon shells. A hit makes the lost case blink, a shell flies to the backdrop, BAIL OUT! blinks when it has no energy left and a destroyed tank blows up. To show your own drawing of the tank instead of ArcadeDMD's, put it in `sprites\mslug_tank_hd.png` (seen from the side, gun to the right). A plain background around the drawing is made transparent, empty margins are cut and it sits in the middle of the card. Player 2 can join at any time. Each mission has its own backdrop (jungle, desert, snowy mountain, city at war, harbor, enemy base), with MISSION COMPLETE and fireworks in between. With nobody playing, the backdrops take turns.
- **Fighting games.** Sparks on every hit, combo counter, FIRST ATTACK, super moves (the screen darkens), a red heartbeat when health is low, exploding K.O., DOUBLE K.O., TIME UP, PERFECT, confetti for the winner, the next King of Fighters fighter, and FIGHT ! at the start of each round. The crowd at the bottom reacts to the action.
- **Neo Geo games done one by one.** Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers, Neo Turf Masters, Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11, Sengoku 3, Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2, Aero Fighters 3, Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman, Twinkle Star Sprites, League Bowling, Neo Drift Out, Riding Hero, Thrash Rally, Magician Lord, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army, Burning Fight, Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger, Puzzle De Pon!, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks, Super Sidekicks 2, Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl, Football Frenzy, Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf, Power Spikes II, Bang Bead, Battle Flip Shot, Over Top, Stakes Winner, Stakes Winner 2, Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa, Puzzled, Zintrick, Digger Man, The Irritating Maze, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords, Eight Man, Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo, Chibi Maruko-chan Deluxe Quiz, Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2 and Shougi no Tatsujin each have a scene of their own, see section 7 (Neo Geo games done one by one).
- **Capcom games.** The 34 fighting games fight on the stages of the game, with the super gauges under the fighters. Fifty other Capcom games, from Final Fight to 1944, Strider and Ghouls'n Ghosts, each have a scene of their own, see section 7 (Capcom games done one by one).

#### Backgrounds that follow the stage

The background changes with the game's stage when the game file knows where to read it.
- `backdrop` is the backdrop of the current fight, from the cheat databases ("Select Backdrop"). It picks the HD background in the `"hd"` list of the game file.
- `stage` is the match number in the run ("Select Current Round"). It is shown as STAGE 2, STAGE 3... with the name of the place.
- For Metal Slug, `mission` picks the backdrop of each mission.

| Games | Values |
|---|---|
| The King of Fighters '96, '97, '98, '99 and 2000, Rage of the Dragons | `stage` and `backdrop` |
| The King of Fighters 2002, Garou, Fatal Fury 2, Fatal Fury Special, Real Bout Fatal Fury 2, Real Bout Fatal Fury Special, Samurai Shodown II, III and IV, World Heroes, World Heroes Perfect, SNK vs. Capcom (JAMMA PCB) | `backdrop` |
| Metal Slug, Metal Slug 2 | `mission` |
| Street Fighter II, II' Champion Edition, II' Hyper Fighting, Super Street Fighter II and Turbo, Street Fighter Alpha, Alpha 2, Alpha 3, Zero 2 Alpha, Street Fighter III and its 2nd Impact and 3rd Strike, Darkstalkers, Night Warriors, Vampire Savior, Vampire Hunter 2, Vampire Savior 2, X-Men: Children of the Atom, Marvel vs. Capcom, Cyberbots, Super Gem Fighter, Red Earth | `backdrop`, with the place of each stage (`"places"`) |

These addresses come from the cheat databases and still have to be confirmed in game (`test_retroarch.bat` shows them). The other games always get the same background. `demo_fight.bat` changes the stage every two K.O., so you can see it without playing.

Each game file says which background goes with each backdrop, in the order of the backdrop numbers. For example, in `games\kof98.json`

```json
"hd": {"stages": ["fight_city", "fight_jungle", "fight_snow", "fight_desert", "fight_ruins", "arena", "fight_temple", "fight_harbor", "base"]}
```

Backdrop 0 (Japan, street) gets the city at night, 3 (Mid-East) the desert, 7 (USA, wharf) the harbor, and so on. The note of the `backdrop` value lists the game's backdrops. Change the list to your taste, the engine reloads the file by itself.

| Background | What it shows |
|---|---|
| `fight_city` | city at night, neon signs, elevated train, steam |
| `fight_temple` | temple at dusk, swinging lanterns, falling petals |
| `fight_harbor` | harbor at sunset, reflections on the water, lighthouse, gulls |
| `fight_ruins` | ruins at night, torches, embers, fireflies |
| `fight_desert`, `fight_jungle`, `fight_snow` | desert at dusk, jungle at night, snowy mountain |
| `arena` | arena with spotlights |
| `base`, `city_war` | enemy base (beacons, searchlights), city at war (fires, explosions) |
| `fight_castle` | castle roof in Japan at night, full moon, cherry petals |
| `fight_market` | Chinese street market, hanging lanterns, steam from the stalls |
| `fight_factory` | steel factory, furnaces, molten metal and sparks |
| `fight_gothic` | gothic manor under the moon, bats, lightning |
| `fight_palace` | Indian palace at sunset, elephants, torches |
| `fight_thai` | golden temple on its river, sky lanterns, glints on the water |
| `fight_lab` | laboratory, glowing tanks, screens |
| `fight_airbase` (or `fight_base`) | air base at dusk, hangars, jets, runway lights |

A Capcom game file can also give the place shown under the stage banner, in French and English, one per backdrop value (`"places": [["CHINE", "CHINA"], ...]`). Without it, the place of the background is shown.

The `fight_` backgrounds and `arena` have a crowd in front. Without the `fight_` prefix (`city`, `temple`, `harbor`, `ruins`, `desert`, `jungle`, `snow`), the same places have no crowd, as in the Metal Slug missions. A Metal Slug file can also have its own `"hd": {"stages": [...]}` list, one background per mission.

## 4. Pixelcade LED

The Pixelcade LED is itself a 128x32 panel. ArcadeDMD drives it directly through its USB port, with the same protocol as Visual Pinball (dmdext, libdmdutil). V1 and V2 boards are detected automatically.

The Pixelcade software (pixelweb) cannot share the panel, so ArcadeDMD does what Pixelcade recommends for Visual Pinball. When a game that has its file in `games\` starts, it stops pixelweb through its API (`/quit`) and takes over the panel. When you quit the game, it releases the panel immediately and restarts pixelweb. The game's marquee stays displayed in the meantime, then ArcadeDMD asks pixelweb to display it, as BigBox would (the game you just quit is the one selected in BigBox). After that, BigBox takes the Pixelcade back at every game change, as on an LCD marquee screen. For all other games, pixelweb keeps showing its marquees as before.

### Setup

`install.bat` asks about it at step 4 and sets the port by itself. The ZeDMD output stays off if you answered no to the ZeDMD question, and ArcadeDMD then probes no other serial port (light guns, for example). To do it by hand, follow these steps.

1. Run `ports.bat` and find the Pixelcade's port (if in doubt, unplug it and see which port disappears).
2. In `config.json`, `pixelcade` section, set `"enabled": true` and that port.

```json
"pixelcade": {
  "enabled": true,
  "device": "COM4",
  "color_order": "auto",
  "mode": "games",
  "takeover": "known",
  "max_fps": 30
}
```

3. Run `test_pixelcade.bat`. The test pattern shows RED, GREEN and BLUE. At the end the pattern stays on the panel and the test asks you whether each word is shown in its own color. If you answer n, it swaps green and blue in `config.json` (`"color_order"`). Run the test again to check.
4. Run `demo_afterburner.bat`. The scene moves to the Pixelcade, then pixelweb comes back when you close it.

### Options

| Setting | Effect |
|---|---|
| `"takeover": "known"` | takes over the panel only for games that have a file in `games\` (After Burner II, Sonic 1 and 2, and the ones you add) |
| `"takeover": "all"` | takes over the panel for every MAME game, with the generic scene |
| `"mode": "always"` | keeps the panel all the time (if you no longer use pixelweb), black outside games |
| `"pixelweb_exe"` | path to pixelweb.exe, usually found automatically. If it needs options, put here a .bat that launches it with them |
| `"art_dir"` | Pixelcade folder, to reuse its marquees as the background of the generic scene (usually found automatically) |
| `"gamma": 2.2` | LEDs light up in proportion to the value they get, so a dark gray made for a screen glows on the panel and the scenes look busier than in the preview. ArcadeDMD corrects the colors so that the panel looks like the preview. `1.0` sends them as they are |

V1 boards show 3 bits per color in direct mode, which is a hardware limit. V2 boards show all colors.

For a game that has a file but no dedicated scene (a game learned with `learn.bat`, for example), the generic scene uses the game's Pixelcade marquee as a dimmed background, with the score and credits on top.

---

## 5. After Burner II, finding the score and credits

The high score location is public (high score table at `0xFF846E`, the same one `hiscore.dat` uses). The score and credits addresses are not documented anywhere, hence the learning tool. Allow five minutes.

1. Start After Burner II.
2. Insert a coin, wait a little, insert a second one. The credits change.
3. Play. When the score is stable (not during a bonus count), press **Right Ctrl + D**. A message on screen confirms the capture. You can also go through Tab > Plugin Options > ArcadeDMD and select the RAM capture entry.
4. Repeat the capture at three or four moments, with different scores and credits.
5. Quit MAME and run `learn.bat`. For each capture, the tool opens the screenshot and asks you for the values, for example `score=16060 credits=3`.
6. It searches for these values in all common formats, suggests the address and writes it to `games\aburner2.json`.

Start the game again. The score and credits now show on the panel and in the plugin's Tab menu.

If only one area is found, it is the right one. If several are found, one more capture is enough to decide. If nothing is found, delete the `learn_ranges` line in `games\aburner2.json`, delete the `runtime\learn\aburner2` folder and take the captures again. The tool then searches all the RAM visible to the main CPU.

There is another way if you already use DOFLinx with DOF2DMD (see section 9). DOFLinx can already read the score and credits of After Burner II and of more than 2,000 games.

---

## 6. Sonic 1 and Sonic 2

The addresses come from the community disassemblies of Sonic 1 and Sonic 2 (score, rings, lives, zone). They are the same in both games. In MAME, the scene triggers with the Mega Drive/Genesis (`genesis` or `megadriv` drivers, "Sonic The Hedgehog" or "Sonic The Hedgehog 2" cartridge from the software list or a ROM file with that name), and normally with the Mega Play and Mega-Tech arcade versions (`mp_sonic`, `mt_sonic`, `mp_soni2`, `mt_soni2`). It also works with RetroArch and the Genesis Plus GX core (see section 7).

`games\sonic.json` is used for Sonic 1 and `games\sonic2.json` for Sonic 2. Both scenes are identical, only the title changes.

The little character running on the grass is a generic ring. To use your own animated sprite, drop `sonic.gif` (or a `sonic.png` horizontal strip of 6 frames) into `sprites\`. For Sonic 2, a `sonic2.gif` takes priority if it exists. Adjust `"y"` in the game file to match its height.

---

## 7. RetroArch (Metal Slug, Sonic...)

ArcadeDMD also reads games launched in RetroArch, with no plugin. RetroArch exposes the game memory through its "network commands", which stay on the PC itself. This is the method used in Vera's zip.

### One-time setup in RetroArch

1. You need RetroArch 1.19 or newer. The version is shown in Information > System Information.
2. In Settings > Network, turn on "Network Commands". Leave the port at 55355.
3. Leave "Pause Content When Not Active" turned on (Settings > User Interface). It is the default setting, and it is used for learning.
4. Start the game with a core that exposes its memory (see just below).

Nothing else to install. As soon as the engine is running (`run.bat` or the automatic start), it watches RetroArch by itself. The log shows "RetroArch 1.19.x detected (network commands active)" when the network commands respond, then the loaded core for each game.

### The right core

Not every core gives RetroArch access to the game memory. With the wrong core, the scene shows but without any values.

| System | Core that works | Cores that don't work |
|---|---|---|
| Arcade, Neo Geo (Metal Slug...) | Arcade (FinalBurn Neo), up to date | FB Alpha 2012 in all its forms (Neo Geo, CPS-1...), MAME 2003, MAME 2003-Plus, MAME 2010, MAME |
| Mega Drive (Sonic) | Genesis Plus GX, or PicoDrive | |

Installing FinalBurn Neo
1. In RetroArch, go to Main Menu > Online Updater > Core Downloader, then choose "Arcade (FinalBurn Neo)". If Online Updater does not appear, turn it on in Settings > User Interface > Menu Item Visibility > Main Menu.
2. To try it, go to Main Menu > Load Core > Arcade (FinalBurn Neo), then Load Content and pick the game (for example `mslug.zip`).
3. If the game refuses to start, a BIOS file is most likely missing. Put a recent `neogeo.zip` next to the game.
4. If you launch your games from HyperSpin or RocketLauncher, also change the core selected for this system in your launcher.

To see which core is running, press F1 during the game, then go to Information > Core Information. Or run `test_retroarch.bat` during a game. It shows the RetroArch version, the loaded core, the result of the memory read and the values read, then tells you what to do if something is wrong. The result is also saved to `runtime\test_retroarch.txt`.

### Supported games

| Game | RetroArch core | Shown right away | To learn |
|---|---|---|---|
| Metal Slug (`mslug`) | FinalBurn Neo | score, lives, bombs, weapon and ammo, the tank (in it or not, its energy and its shells) | nothing |
| Metal Slug 2 (`mslug2`), Metal Slug X (`mslugx`) | FinalBurn Neo | lives, bombs, weapon and ammo | score |
| Metal Slug 3 (`mslug3`) | FinalBurn Neo | score, lives, bombs, weapon and ammo | P2 score |
| Metal Slug 4 (`mslug4`), Metal Slug 5 (`mslug5`) | FinalBurn Neo | lives, bombs, weapon and ammo | score |
| The 57 Neo Geo fighting games (King of Fighters, Samurai Shodown, Fatal Fury, Last Blade, World Heroes...) | FinalBurn Neo | see the Fighting games table just below | the score, except KOF 96 to 2002 and Samurai Shodown II |
| Blazing Star (`blazstar`), Puzzle Bobble (`pbobblen`), Shock Troopers (`shocktro`), Pulstar (`pulstar`), Magical Drop III (`magdrop3`), Sengoku 3 (`sengoku3`), Top Hunter (`tophuntr`), Last Resort (`lresort`), Aero Fighters 2 (`sonicwi2`), Aero Fighters 3 (`sonicwi3`), Strikers 1945 Plus (`s1945p`), Super Dodge Ball (`sdodgeb`), Neo Bomberman (`neobombe`), Twinkle Star Sprites (`twinspri`), League Bowling (`lbowling`), Magician Lord (`maglord`), NAM-1975 (`nam1975`), Cyber-Lip (`cyberlip`), Ghost Pilots (`gpilots`), Alpha Mission II (`alpham2`), Viewpoint (`viewpoin`), Zed Blade (`zedblade`), Prehistoric Isle 2 (`preisle2`), Shock Troopers 2nd Squad (`shocktr2`), Robo Army (`roboarmy`), Burning Fight (`burningf`), Mutation Nation (`mutnat`), Sengoku (`sengoku`), Sengoku 2 (`sengoku2`), Ninja Combat (`ncombat`), Ninja Commando (`ncommand`), Blue's Journey (`bjourney`), Puzzle Bobble 2 (`pbobbl2n`), Magical Drop II (`magdrop2`), Money Puzzle Exchanger (`miexchng`), Puzzle De Pon! (`puzzledp`), Puzzle De Pon! R! (`puzzldpr`), Panic Bomber (`panicbom`), Pop 'n Bounce (`popbounc`), Super Bubble Pop (`sbp`), Spin Master (`spinmast`), Ganryu (`ganryu`), Zupapa! (`zupapa`), Neo Mr. Do! (`neomrdo`), Bang Bead (`bangbead`), Battle Flip Shot (`flipshot`), Gururin (`gururin`), Ghostlop (`ghostlop`), Pochi and Nyaa (`pnyaa`), Puzzled (`joyjoy`), Zintrick (`zintrckb`), Digger Man (`diggerma`), Andro Dunos (`androdun`), Captain Tomaday (`ctomaday`), Choutetsu Brikin'ger (`ironclad`), Last Hope (`lasthope`), Bang Bang Busters (`b2b`), Crossed Swords (`crsword`), Eight Man (`eightman`), Nightmare in the Dark (`nitd`), The Super Spy (`superspy`), Quiz King of Fighters (`quizkof`), Quiz Daisousa Sen (`quizdais`), Quiz Meitantei Neo & Geo (`quizdai2`), Chibi Maruko-chan Deluxe Quiz (`marukodq`) | FinalBurn Neo | see Neo Geo games done one by one | score |
| Windjammers (`wjammers`), Neo Turf Masters (`turfmast`), Super Sidekicks 3 (`ssideki3`), The Ultimate 11 (`ssideki4`), Baseball Stars 2 (`bstars2`), Street Hoop (`strhoop`), Neo Drift Out (`neodrift`), Riding Hero (`ridhero`), Thrash Rally (`trally`), Super Sidekicks (`ssideki`), Super Sidekicks 2 (`ssideki2`), Tecmo World Soccer '96 (`twsoc96`), Goal! Goal! Goal! (`goalx3`), Neo-Geo Cup '98 (`neocup98`), Soccer Brawl (`socbrawl`), Football Frenzy (`fbfrenzy`), Pleasure Goal (`pgoal`), Baseball Stars Professional (`bstars`), 2020 Super Baseball (`2020bb`), Top Player's Golf (`tpgolf`), Power Spikes II (`pspikes2`), Over Top (`overtop`), Stakes Winner (`stakwin`), Stakes Winner 2 (`stakwin2`), Jockey Grand Prix (`jockeygp`), The Irritating Maze (`irrmaze`), Minasan no Okagesamadesu! (`minasan`), Mahjong Kyo Retsuden (`mahretsu`), Janshin Densetsu (`janshin`), Bakatonosama Mahjong Manyuuki (`bakatono`), Idol Mahjong Final Romance 2 (`froman2b`), Shougi no Tatsujin (`moshougi`) | FinalBurn Neo | see Neo Geo games done one by one | nothing |
| All other Neo Geo games | FinalBurn Neo | scene by genre (credits with MAME) | score, and credits if the game keeps a copy of them |
| Every Capcom CPS1, CPS2 and CPS3 game | FinalBurn Neo | see Capcom CPS1, CPS2 and CPS3 games | score |
| Sonic 1 and Sonic 2 | Genesis Plus GX | score, rings, lives | nothing |

The lives, bombs and ammo addresses come from the MAME 2003-Plus cheat database. Sonic's are the same as in MAME. Metal Slug lives follow the on-screen "1UP". Metal Slug 1 also counts the current life, so ArcadeDMD subtracts 1 (verified). Metal Slug 3 does not count it (verified). For 2 and X, ArcadeDMD does as for 1, and for 4 and 5 as for 3. If one of these games shows one life fewer than the screen, remove the `"add"` and `"min"` lines from its lives entry in its `games\mslugX.json` file. If it shows one more, add `"add": -1, "min": 0`.

With two players, the scene changes by itself as soon as player 2 presses Start. The Neo Geo BIOS tells who is in the game. At the top, as in the game, "1UP=" and player 1's lives on the left, "2UP=" and player 2's lives on the right, with the title scrolling between them. Below, each score sits under its 1UP or 2UP. A gray "SCORE ?" means that score has not been learned yet. At the bottom, each player's bombs and then weapon take turns, with "P1" in green and "P2" in yellow. If only player 2 is playing, the normal scene shows with player 2's values. Neo Geo credits can only be read with MAME (see All Neo Geo games).

The Metal Slug scenes are inspired by Vera's video, adapted to a 128x32 panel so that nothing ends up hidden behind the scenery. At the top, "SNK" in blue then "- METAL SLUG" (with the game number) in white scroll slowly. Below, "P1" in green and the score in white on the left, lives on the right. The next line alternates between the bombs, the weapon with its ammo (handgun, machine gun, shotgun, flamethrower, rocket launcher, laser, enemy chaser... a "+" marks the enhanced version) and, with MAME, the credits. At the very bottom, small hills and a small, dimmer tank that moves forward and fires when the score goes up.

The Metal Slug and Metal Slug 3 scores are already in their files, found with `learn.bat` under RetroArch and FinalBurn Neo. To replace the tank with your own drawing, drop `mslug_tank.gif` (or a `mslug_tank.png` strip of 3 frames) into `sprites\`. It must fit within 5 pixels in height, cannon facing right.

### Fighting games

Each Neo Geo fighting game has its own file in `games\`, official variants included (Japanese, Korean, prototype). The addresses come from the FinalBurn Neo cheats, peon2's FinalBurn Neo training scripts and the MAME 2003-Plus cheat database. The score is known for the King of Fighters games and for Samurai Shodown II. For the others, learn it with `learn.bat` (`score=...` and `score2=...`).

When a health bar, a timer or a name does not match the screen, run `test_retroarch.bat` during a fight and post the result in a GitHub issue.

| Game | File | Health bars | Timer | Character names | Score |
|---|---|---|---|---|---|
| 3 Count Bout | `3countb.json` | - | - | - | to learn |
| Aggressors of Dark Kombat | `aodk.json` | yes | - | - | to learn |
| Art of Fighting | `aof.json` | yes | yes | yes (10) | to learn |
| Art of Fighting 2 | `aof2.json` | yes | yes | yes (13) | to learn |
| Art of Fighting 3 | `aof3.json` | yes | yes | yes (10) | to learn |
| Breakers | `breakers.json` | yes | yes | - | to learn |
| Breakers Revenge | `breakrev.json` | yes | yes | - | to learn |
| Double Dragon | `doubledr.json` | yes | yes | yes (14) | to learn |
| Dragon's Heaven | `dragonsh.json` | - | - | - | to learn |
| Fatal Fury | `fatfury1.json` | yes | yes | yes (14) | to learn |
| Fatal Fury 2 | `fatfury2.json` | yes | yes | - | to learn |
| Fatal Fury 3 | `fatfury3.json` | yes | yes | yes (13) | to learn |
| Fatal Fury Special | `fatfursp.json` | yes | yes | - | to learn |
| Fight Fever | `fightfev.json` | yes | yes | yes (10) | to learn |
| Galaxy Fight | `galaxyfg.json` | yes | - | - | to learn |
| Garou | `garou.json` | yes | yes | yes (14) | to learn |
| Kabuki Klash | `kabukikl.json` | yes | yes | - | to learn |
| Karnov's Revenge | `karnovr.json` | yes | - | yes (14) | to learn |
| King of the Monsters | `kotm.json` | yes | - | - | to learn |
| King of the Monsters 2 | `kotm2.json` | yes | yes | yes (10) | to learn |
| Kizuna Encounter | `kizuna.json` | yes | yes | - | to learn |
| Legend of Success Joe | `legendos.json` | yes | - | - | to learn |
| Matrimelee | `matrim.json` | yes | yes | - | to learn |
| Ninja Master's | `ninjamas.json` | yes | yes | - | to learn |
| Rage of the Dragons | `rotd.json` | yes | yes | - | to learn |
| Ragnagard | `ragnagrd.json` | yes | - | - | to learn |
| Real Bout Fatal Fury | `rbff1.json` | yes | yes | yes (16) | to learn |
| Real Bout Fatal Fury 2 | `rbff2.json` | yes | yes | yes (23) | to learn |
| Real Bout Fatal Fury Special | `rbffspec.json` | yes | yes | yes (20) | to learn |
| Samurai Shodown | `samsho.json` | yes | yes | yes (13) | to learn |
| Samurai Shodown II | `samsho2.json` | yes | yes | yes (17) | yes |
| Samurai Shodown III | `samsho3.json` | yes | yes | yes (14) | to learn |
| Samurai Shodown IV | `samsho4.json` | yes | yes | yes (18) | to learn |
| Samurai Shodown V | `samsho5.json` | yes | yes | yes (28) | to learn |
| Samurai Shodown V Special | `samsh5sp.json` | yes | yes | yes (28) | to learn |
| Savage Reign | `savagere.json` | - | - | - | to learn |
| SNK vs. Capcom | `svc.json` | yes | yes | yes (36) | to learn |
| SNK vs. Capcom (JAMMA PCB) | `svcpcb.json` | yes | yes | yes (36) | to learn |
| The King of Fighters '94 | `kof94.json` | yes | yes | - | to learn |
| The King of Fighters '95 | `kof95.json` | yes | yes | - | to learn |
| The King of Fighters '96 | `kof96.json` | yes | yes | yes (29) | assumed, to be checked |
| The King of Fighters '97 | `kof97.json` | yes | yes | yes (32) | assumed, to be checked |
| The King of Fighters '98 | `kof98.json` | yes | yes | yes (38) | found |
| The King of Fighters '99 | `kof99.json` | yes | yes | yes (34) | assumed, to be checked |
| The King of Fighters 2000 | `kof2000.json` | yes | yes | yes (36) | assumed, to be checked |
| The King of Fighters 2001 | `kof2001.json` | yes | yes | - | assumed, to be checked |
| The King of Fighters 2002 | `kof2002.json` | yes | yes | - | assumed, to be checked |
| The King of Fighters 2003 | `kof2003.json` | - | yes | - | to learn |
| The King of Fighters 2003 (Japan, JAMMA PCB) | `kf2k3pcb.json` | - | yes | - | to learn |
| The Last Blade | `lastblad.json` | yes | yes | yes (15) | to learn |
| The Last Blade 2 | `lastbld2.json` | yes | yes | yes (20) | to learn |
| Voltage Fighter Gowcaizer | `gowcaizr.json` | yes | yes | yes (12) | to learn |
| Waku Waku 7 | `wakuwak7.json` | yes | yes | yes (9) | to learn |
| World Heroes | `wh1.json` | yes | yes | yes (9) | to learn |
| World Heroes 2 | `wh2.json` | yes | yes | yes (16) | to learn |
| World Heroes 2 Jet | `wh2j.json` | yes | yes | yes (17) | to learn |
| World Heroes Perfect | `whp.json` | yes | yes | yes (19) | to learn |

### King of Fighters VS matches (BEAT BY)

In a two-player match, the King of Fighters games show "CHALLENGER" above the player who just joined, and "BEAT BY 02" above the one who has already beaten 2 challengers in a row. The panel shows the same thing in place of the scores, as soon as these counters have been learned. Each win is also logged in `obs\vs_history.txt`, and the best streak for each game is kept (section 11).

These counters are not in any cheat database. They have to be learned once per game, for example KOF 2002, then KOF 98.
1. Launch the game in RetroArch and start playing as player 1.
2. Bring player 2 in with a coin and Start. The VS match begins. You can hold both sticks yourself.
3. Run `learn.bat`.
4. After each match, when "BEAT BY" shows at the top of the screen, type both counters, for example `beat=1 beat2=0`. Enter 0 for the side marked CHALLENGER.
5. Play at least five or six matches. Let one side win, then the other, so that the counters change.
6. Press Enter on an empty line to finish. The tool writes `beat` and `beat_p2` to the game file.

If the tool finds nothing, zip the game's folder from `runtime\learn\` (`kof2002`, for example) and attach it to a GitHub issue, as was done for Samurai Shodown II.

### Neo Geo games done one by one

Game after game, the Neo Geo games got a panel scene and an animated HD scene of their own, the best-known first, and now they all have one. [PROGRESS.md](PROGRESS.md) shows where things stand and what comes next. Everything is drawn by the program, no image comes from the games.

In the shoot'em ups (Blazing Star, Pulstar, Last Resort, Aero Fighters 2 and 3, Strikers 1945 Plus, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope), once the score is read, the enemies of the HD screen only blow up when the game scores points. The enemy our shots are hitting goes first, its points show above it, and the bigger the gain the bigger the blast. A bomb or a special weapon of the game destroys what it hits, and a bonus that the game counts at the end of a stage shows as one counter. As long as the score of a game has not been learned with `learn.bat`, its HD scene plays by itself.

The panel of these games keeps it simple during a game. The score in big digits in the middle, or the title of the game as long as the score has not been learned. Your lives at the bottom left (a plane and x2), your bombs at the bottom right. No credits and no INSERT COIN during a game. Between them flies your ship. It follows your stick and fires while you hold the fire button (the Neo Geo BIOS keeps them, with MAME as with RetroArch), and flies by itself until you touch them. With two players, both scores at the top, the lives and bombs of each player below, and both ships face to face. Everything else takes the panel for a moment, one thing at a time, as on a pinball. BOMB! and its explosions, POWER UP then MAX POWER, the plane that blows up with the lives left, LAST LIFE, 1UP, ROUND 2 or STAGE 2, SPEED UP, the SUPER SHOT of Strikers 1945 Plus, CONTINUE?, GAME OVER, PLAYER 1 and PLAYER 2 when someone starts, and CREDIT 1 when a coin goes in during a game. Each enemy destroyed in the game blows up ahead of your ship, the size and pace of the DOFLinx explosions, a big one for a big enemy, and nothing blows up during a bonus count. As long as the score has not been learned, an enemy blows up ahead of it now and then while it fires, as on the HD screen. The coin screen, when nobody plays, does not change.

![Aero Fighters 2 on a 128x32 LED panel, the plane that flies and fires, POWER UP, a coin during a game and BOMB!](docs/images/led_shooter.gif)

Your own animations (the GIFs of DOFLinx or of the Pixelcade, for example) can replace ours on the panel. Put them in an `artwork` folder next to `arcadedmd.py`, it is never published and an update never touches it. `artwork\boom.gif` is the explosion of an enemy, `boom_big.gif` the big one, `bomb.gif` and `shock.gif` the bomb, `super.gif` the super shot of Strikers 1945 Plus, `charge.gif` the charged shot of Pulstar and `ship.gif` your ship (facing right, about 14 x 5). For one game only, put them in `artwork\<game>\` (`artwork\s1945p\boom.gif`, for example). A 128 x 32 GIF plays over the whole panel and its black lets the scene show through, but when its drawing fits in the middle (the explosions of DOFLinx) it is cropped and plays at the place of the action.

![Blazing Star, Puzzle Bobble, Windjammers, Shock Troopers and Neo Turf Masters on an LCD marquee, HD display](docs/images/hd_neogeo_games.jpg)

![Pulstar, Magical Drop III, Super Sidekicks 3, The Ultimate 11 and Sengoku 3 on an LCD marquee, HD display](docs/images/hd_neogeo_games_2.jpg)

![Top Hunter, Baseball Stars 2, Last Resort, Aero Fighters 2 and Aero Fighters 3 on an LCD marquee, HD display](docs/images/hd_neogeo_games_3.jpg)

![Strikers 1945 Plus, Street Hoop, Super Dodge Ball, Neo Bomberman and Twinkle Star Sprites on an LCD marquee, HD display](docs/images/hd_neogeo_games_4.jpg)

![League Bowling, Neo Drift Out, Riding Hero, Thrash Rally and Magician Lord on an LCD marquee, HD display](docs/images/hd_neogeo_games_5.jpg)

![NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II and Viewpoint on an LCD marquee, HD display](docs/images/hd_neogeo_games_6.jpg)

![Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army and Burning Fight on an LCD marquee, HD display](docs/images/hd_neogeo_games_7.jpg)

![Mutation Nation, Sengoku, Sengoku 2, Ninja Combat and Ninja Commando on an LCD marquee, HD display](docs/images/hd_neogeo_games_8.jpg)

![Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger and Puzzle De Pon! on an LCD marquee, HD display](docs/images/hd_neogeo_games_9.jpg)

![Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop and Spin Master on an LCD marquee, HD display](docs/images/hd_neogeo_games_10.jpg)

![Ganryu, Zupapa!, Neo Mr. Do!, Super Sidekicks and Super Sidekicks 2 on an LCD marquee, HD display](docs/images/hd_neogeo_games_11.jpg)

![Tecmo World Soccer '96, Goal! Goal! Goal!, Neo-Geo Cup '98, Soccer Brawl and Football Frenzy on an LCD marquee, HD display](docs/images/hd_neogeo_games_12.jpg)

![Pleasure Goal, Baseball Stars Professional, 2020 Super Baseball, Top Player's Golf and Power Spikes II on an LCD marquee, HD display](docs/images/hd_neogeo_games_13.jpg)

![Bang Bead, Battle Flip Shot, Over Top, Stakes Winner and Stakes Winner 2 on an LCD marquee, HD display](docs/images/hd_neogeo_games_14.jpg)

![Jockey Grand Prix, Gururin, Ghostlop, Pochi and Nyaa and Puzzled on an LCD marquee, HD display](docs/images/hd_neogeo_games_15.jpg)

![Zintrick, Digger Man, The Irritating Maze, Andro Dunos and Captain Tomaday on an LCD marquee, HD display](docs/images/hd_neogeo_games_16.jpg)

![Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords and Eight Man on an LCD marquee, HD display](docs/images/hd_neogeo_games_17.jpg)

![Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo and Chibi Maruko-chan Deluxe Quiz on an LCD marquee, HD display](docs/images/hd_neogeo_games_18.jpg)

![Minasan no Okagesamadesu!, Mahjong Kyo Retsuden, Janshin Densetsu, Bakatonosama Mahjong Manyuuki, Idol Mahjong Final Romance 2 and Shougi no Tatsujin on an LCD marquee, HD display](docs/images/hd_neogeo_games_19.jpg)

| Game | File | Panel | HD screen |
|---|---|---|---|
| Blazing Star | `blazstar.json` | the score or the title, the lives, the ship that follows the stick and fires, POWER UP, ROUND 2, a life lost | space and a big planet. The ship fires, an enemy blows up when the score goes up, POWER UP, ROUND with a burst of speed, the ship explodes when a life is lost |
| Puzzle Bobble | `pbobblen.json` | the bubble in the launcher and the next one, in their colors, ROUND | the launcher with its arrow and its gear. Each bubble shot in the game leaves the launcher and sticks to a little board, three of a color pop and the ones left hanging fall |
| Windjammers | `wjammers.json` | points of the set with the timer in between, the court, the opponent's country, a disc going back and forth | the court of the game (beach, lawn, tiles, concrete, clay, stadium) and the scoreboard. The disc flies into the goal zone with +3 or +5, or drops on the other side with +2 |
| Shock Troopers | `shocktro.json` | energy, gun and ammo, special weapon and what is left, timer | jungle at war, one panel per player with energy, gun, ammo and grenades. Shots, grenades blowing up in the jungle, the panel shakes when hit |
| Neo Turf Masters | `turfmast.json` | club and distance, stroke, power gauge, golfer, wind with an arrow | golf course, club, power gauge and wind compass. The wind pushes the clouds and the flag, and the ball flies to the green at each stroke |
| Pulstar | `pulstar.json` | the score or the title, the lives, the ship that follows the stick and fires, the charged shot, SPEED UP, STAGE 2 | one world per stage (Earth, water vein, fire, space station, forest, nebula). The charge glows on the nose and leaves as a beam, the pods and the front shield follow the ship, an enemy blows up when the score goes up, STAGE with its name |
| Magical Drop III | `magdrop3.json` | both players' tarot cards, quota, level | two fields of drops under a tarot sky, both cards in the middle. When the quota goes down, the jester throws a drop and as many pop, a big group makes a chain, the level pushes a row down, the card flips when the character changes |
| Super Sidekicks 3 | `ssideki3.json` | both teams' goals, GOAL! when one goes in, a ball going back and forth | a stadium by day, the match seen by the TV camera. When the goals go up, the ball ends in the net, GOAL!, confetti, the crowd jumps |
| The Ultimate 11 | `ssideki4.json` | goals and both players' power gauges | the same match at night under the floodlights, with the power gauge. When the full gauge empties, the super shot flies on fire |
| Sengoku 3 | `sengoku3.json` | health and magic of both players, timer, fighter, throwing weapon and how many are left | a temple under the moon and shadow warriors, one panel per fighter. The throwing weapons fly (shuriken, kunai, bomb, saucer), a warrior falls under the sword when the score goes up, the magic sweeps the screen, the panel shakes when hit |
| Top Hunter | `tophuntr.json` | lives as small hunters, timer, power gauge in five segments, hills | hunters as big as in the game on four planets (forest, ice, wind, fire) with their two lanes, leaves, ice or rock across the top of the screen as in the game. Robots and walking machines with turbines come on both lanes, the hunter jumps from one lane to the other and punches, throws or shoots them when the score goes up, the full power gauge that empties is a special move, the hunters move on to the next planet when the timer starts again for a new stage. At the top, the hunter's head with 1UP= and the lives, the score, the power, TIME |
| Baseball Stars 2 | `bstars2.json` | both teams' runs, RUN! when one comes in, balls, strikes and outs lights, both POW gauges | the field as in the game's batting view, bright green grass seen from behind home plate, the batter big in front, the pitcher on the mound. Each ball, strike and out read in the game is a pitch, called in big rainbow letters, the batter hits and a fielder catches, the runs send the ball far and the runners home (fireworks when it goes over the wall), the other team comes to bat after the third out. The count in coloured dots |
| Last Resort | `lresort.json` | the score or the title, the lives, the ship that follows the stick and fires, POWER UP, SPEED UP | the city at night of the game's first stage, giant towers lit with orange windows, purple buildings, the highway with its lamps and its cars. The unit turns around the ship on the side away from where it goes and fires with it, now and then it flies straight ahead and comes back, an enemy blows up when the score goes up. 1P= and the lives at the top, POW at the bottom |
| Aero Fighters 2 | `sonicwi2.json` | the score or the title, the lives and the bombs, the jet that follows the stick and fires, BOMB!, POWER UP, MAX POWER | a city seen from the sky in daylight, its avenues and their cars, car parks and parks. Jets drawn after real fighters fly with their shadows below, enemy jets, helicopters and tanks blow up when the score goes up, a bomb sends a salvo of missiles that clears the screen. The bombs in their frames as in the game |
| Aero Fighters 3 | `sonicwi3.json` | the same, with the name of player 1's pilot | a city by a river at nightfall seen from the sky, with the plane of the pilot chosen by player 1 (twelve planes, the Swordfish biplane, the Seiran and its floats...), big bombers and tanks on the avenues. The big bomb falls and everything blows up |
| Strikers 1945 Plus | `s1945p.json` | the score or the title, the lives and the bombs, the plane that follows the stick and fires, BOMB!, SUPER SHOT, POWER UP | the game's two side panels (SCORE, the planes left, BOMB, the SUPER SHOT gauge) around war-torn ground seen from the sky, villages of tiled roofs broken by the bombs, a railway and its train, a river and its bridges. The plane chosen by the player, drawn after the real one (P-38 Lightning, F5U, Spitfire, Ta 152, Zero, Fiat G.56, XP-55 Ascender). The full gauge that empties is the super shot, a bomb brings a formation of bombers whose carpet of bombs clears the screen |
| Street Hoop | `strhoop.json` | both teams' points, the clock, both SUPER SHOT gauges, the court and its hoop | a half court in a park as in the game, trees, a wooden fence, people on the benches, a bike in the grass, the painted asphalt and the hoop on the right. Three against three, the ball goes from hand to hand, the points read in the game are shots from far, jump shots or dunks, a shot misses now and then. The full gauge that empties is a super shot on fire. The points in big letters at the top, red and blue, the clock in its orange box between the two SUPER SHOT gauges, 1P above the player's man |
| Super Dodge Ball | `sdodgeb.json` | the health of the three players of each team in three colours, TIME, both POW gauges | a cobbled lot at the end of the afternoon, people watching over the fence, cans and bottles lying about. Two teams of three players of our own, big heads on short bodies. The ball crosses and is caught, a player whose health goes down takes it full in the face, at zero he is out, the full POW gauge that empties is a power shot on fire. The health bars of both teams at the top with the names, TIME in the middle |
| Neo Bomberman | `neobombe.json` | lives as small heads, fire, the stage, a maze with its blocks | the maze seen from above as in the game, one look per world (ruins, water, factory, castle), stone pillars on every other cell, blocks that break and come back. Little miner robots of our own walk the corridors, the bombs dropped in the game are dropped here and blow up, the flames run in a cross, blobs wander. A coloured band at the top with the lives, the fire and the stage |
| Twinkle Star Sprites | `twinspri.json` | hearts, bombs, the Pow gauge and the character's name, a column between two fields | two fields side by side as in the game, a forest seen from above that scrolls down, the ornate column between them. A little witch of our own in each field shoots the puffballs that come down. At the top the character's name in big letters on a plate in its colours, the score, five big hearts with the half ones (the game's energy). At the bottom POW 1 2 MAX in three blocks and the bombs. In the column, VERSUS and VS between two players, STAGE and its number against the computer, whose side shows its character with PRESS START in place of its score. The big moments come from the game. The chain the game counts (4 HIT, 7 HIT..., for each player, learned on a cabinet like the stage), the fireballs of an attack cross the column and land with LV1 or LV2 ATTACK, a charged shot leaves as a beam of light with LV 1, LV 2 or MAX !, a bomb rumbles the whole screen three times, flashes it white then gold, giant rays of light turn over it, three shockwaves cross both fields and a shower of stars falls on them, with BOMB ! bouncing in and a rainbow shield, a boss attack darkens the other field under BOSS ATTACK !, a heart lost breaks and one given back fills up, and the last heart lost gives K.O. on one side and WIN ! with fireworks on the other, PERFECT ! in big letters above it when the winner lost no heart in the round |
| League Bowling | `lbowling.json` | the shot clock, a lane and its pins | the alley seen from behind the bowler as in the game, the polished lanes running to their pins, the lanes next door, the lit panels of the back wall. Each time the game's shot clock starts again, a bowler of our own throws, the ball hooks down the lane and the pins fly, STRIKE! or SPARE! now and then. TIME in its box at the top |
| Neo Drift Out | `neodrift.json` | the time with its hundredths, a road and a rally car | the rally stages seen from the sky, a dirt road through the woods, then a tarmac road in the countryside. The white rally car drifts in the bends and throws dust, a checkpoint arch goes by when time is added. TIME in big blue numbers with the hundredths, as in the game |
| Riding Hero | `ridhero.json` | time, turbos, rank, a road and its kerbs | the road seen from behind the bike rushes to the horizon as in the game, its red and white kerbs, the bends that sweep it, a snowy volcano, mountains, the long grandstand and a blimp. The rider leans into the bends, the others are passed or come back, a turbo spent is a burst of speed. SPEED, TIME, TURBO and RANK where the game puts them |
| Thrash Rally | `trally.json` | the time and the speed, a road and a rally car | a dirt track between yellow and black barriers, then a snowy road with red and white kerbs and snowmen, seen from the sky. The red car drifts among its rivals, a checkpoint arch goes by when time is added, the speed read in the game sets the pace. TIME in yellow, SPEED in red |
| Magician Lord | `maglord.json` | HP, lives, the name of the shape taken, a walkway and the trees | the villages of huts in the giant trees as in the game, then a temple with a huge stone face. A hero of our own walks the walkways and throws his magic at the undead, and takes the shape read in the game (ninja, merman, samurai, dragon warrior, sea warrior, thunder god). 1UP and the lives at the top, HP and POW in their gauges at the bottom |
| NAM-1975 | `nam1975.json` | grenades, the bullets of the special weapon, a burning city and its road | our soldier seen from behind at the bottom of the screen shoots into the burning city, then the jungle and its river, as in the game. Enemies run along the road, tanks and helicopters cross, the crosshair follows its target. The bullets, the grenades and the weapon read in the game are shown (rifle, machine gun, flamethrower, bazooka), a grenade blows up where the crosshair is |
| Cyber-Lip | `cyberlip.json` | P= and the lives, the timer, the city at night, our hero firing | our hero runs down the city at night, past the theater and the shops, and shoots the walking robots and the drones. The weapon whose ammo goes down in the game is the one he fires (auto, wide, fire, bazooka, grenade). 1P and TIME in blue at the top, the weapon and its ammo in the blue bar at the bottom, P= and the lives, as in the game |
| Ghost Pilots | `gpilots.json` | the score or the title, the planes left and the bombs, the plane that follows the stick and fires, BOMB!, POWER UP | seen from the sky as in the game, the brown earth and its jungle, then the deep blue sea. Our fighter with its big radial engine, red enemy fighters and bombers, tanks on the ground. A bomb spent falls and clears the screen. 1-PLAYER and the score at the top, the planes left, B= and the stars at the bottom left |
| Alpha Mission II | `alpham2.json` | the score or the title, the ships left, the ship that follows the stick and fires, POWER UP | our fighter flies over a huge fortress in deep space as in the game, saucers come, the turrets of the fortress blow up. The ships left =02 and the score at the top, G= the gold and the power of the weapon at the bottom |
| Viewpoint | `viewpoin.json` | the score or the title, the ships left, the ship that follows the stick and fires, BOMB! when the bomb carried goes | the floor of slate tiles seen at an angle slides by as in the game, our hover-ship flies over it with its shadow, crawlers and ring mines come. The bomb carried in the game (plasma, fire, homing) is shown, when it is spent it sweeps the screen in its colour. 1UP, the score and the three bomb lights at the bottom |
| Zed Blade | `zedblade.json` | the score or the title, the ships left and the bombs, the ship that follows the stick and fires, BOMB!, POWER UP | our fighter flies over a valley at dawn as in the game, mountains, forest, stone pillars, the enemy helicopters come in packs, a bomb spent blows them all up. 1P- in red and 2P- in blue at the top, the bombs as blue capsules at the bottom left, LEVEL and the shot level |
| Prehistoric Isle 2 | `preisle2.json` | the score or the title, the helicopters left and the bombs, the ship that follows the stick and fires, BOMB!, POWER UP | our helicopter flies over the sea by the island as in the game, stone pillars rise from the waves, the flying reptiles come, a bomb spent blows up the screen. PLAYER 1 and the score at the top, the helicopters left, Lv the weapon level and the bombs at the bottom left |
| Shock Troopers 2nd Squad | `shocktr2.json` | grenades, the timer, the power gauge, a road, a commando and a tank | the city street seen from above as in the game, the garden and the cracked wall, the white tiled pavement and its lamp posts, the grey road with its yellow line and its burnt cars. Our commando goes up the road and shoots the soldiers, the jeeps and the tanks that come. The weapon read in the game is the one he fires (normal, fire, round, missile, boomerang), a grenade spent is thrown, a life lost blows up next to him. At the top a face of our own, 1P- and the score, TIME in big yellow numbers, at the bottom the grenades, the weapon box and LV |
| Robo Army | `roboarmy.json` | the LIFE gauge, x and the lives, the POW orbs, the town at dusk | the edge of the town at dusk as in the game, a purple sky, wooden fences, a cracked concrete house, trees and dry grass. A cyborg of our own fights the robots that come from both sides. The points read in the game are blows that land, the LIFE that goes down is a blow taken, a life lost a fall. LIFE in blue, 1P- and the score, x and the lives, the POW orbs at the top |
| Burning Fight | `burningf.json` | the health gauge, the timer, P= and the lives, shops with lanterns | a street of small shops at night as in the game, square signs, red paper lanterns, lit windows, vending machines and cobbles. Our street fighter faces the thugs that come from both sides. The points are blows that land, the health that goes down a blow taken. 1UP and the score with the yellow gauge, TIME in big yellow numbers in the middle, P= and the lives at the bottom left |
| Mutation Nation | `mutnat.json` | the LIFE gauge, B and the attack items, a ruined city | the ruined city as in the game, blue towers under a violet sky, old stone buildings with broken windows, rubble, a wrecked car and the cracked road. Our street fighter faces the mutants that come from both sides, the points are blows that land, the LIFE that goes down a blow taken, an attack item spent sweeps the screen. 1P and the score, LIFE in rainbow segments, B and the items at the top |
| Sengoku | `sengoku.json` | the lives, the six LIFE boxes, the colour of the sphere, a red sunset | the end of the world at sunset as in the game, a blood-red and orange sky, a castle floating on its island, the violet ruins and banners of a village, the golden field and the grey mist. Our swordsman of our own fights the armoured ghost warriors and the ninjas, each blow leaves a trail of light, the sphere taken in the game makes the blade glow in its colour. SCORE-, a face of our own, the lives and the six LIFE boxes |
| Sengoku 2 | `sengoku2.json` | the lives, the six LIFE boxes, the colour of the sphere, a dusk sky and the sand | under the great wooden bridge at dusk as in the game, a violet and orange sky, dark mountains, the roofs of a village in the mist, the arch of the bridge on its stone pier, the sand and its stones. Our swordsman fights the dark armoured warriors, the sphere read in the game (blue, pink, yellow) is shown. 1P-, a face of our own, the lives and the LIFE boxes |
| Ninja Combat | `ncombat.json` | LIFE and POW, the lives, a park at night with its lamp posts | a park at night as in the game, dark trees, lamp posts with white globes, a gate of gold and blue pillars under its roof, the fence and the grey paving stones. Our red ninja faces the black, grey and purple ninjas. At the bottom as in the game a face of our own, POW and LIFE, TIME in minutes and seconds, the lives and the name of the character |
| Ninja Commando | `ncommand.json` | the LIFE gauge, the timer, a jungle path | the jungle seen from above as in the game, a winding dirt path between thick bushes, purple boulders, a river and its wooden bridge. Our blue ninja runs up the path and throws fire dragons at the enemy ninjas. At the bottom as in the game a face of our own, LIFE in yellow, TIME in minutes and seconds |
| Blue's Journey | `bjourney.json` | the hearts, the lives, the flowers, the grass and the soil | the land of giant plants as in the game, long leaves striped with yellow hanging from the top, a blue tree, red leaves, a huge clay pot, pink buds, the grass over the golden soil. Our little hero of our own throws leaves at the snails and the bees. 1P=, the lives, TIME=, LIFE and its hearts at the top, the flowers at the bottom left |
| Puzzle Bobble 2 | `pbobbl2n.json` | the shot timer, the coloured blocks | the beach of the first rounds as in the game, a deep blue sky and its big clouds, palm trees, the sea and a sailing boat. The boards in their metal frames, the launcher and its arrow, the bubbles leave when the game's shot timer starts again |
| Magical Drop II | `magdrop2.json` | LEVEL, the quotas of both players | the orange brick wall and its pale marble columns around the two fields of deep teal, as in the game. The jester throws the drops, the quota going down pops them, the level rising pushes a row. LEVEL at the top, the quotas at the bottom |
| Money Puzzle Exchanger | `miexchng.json` | the chain, MAX CHAIN, the level | the pastel diamonds of blue, white and lilac as in the game, the two fields framed in pink full of coins of 10, 50, 100 and 500, a little piggy bank of our own under each field. A chain read in the game pops coins. STAGE and MAX CHAIN between the fields |
| Puzzle De Pon! | `puzzledp.json` | the bubble in the launcher and the next one, LEVEL | the pale blue sky full of big soft stars as in the game, the boards between brick pillars around a starry night, the star dial whose hand turns with the time left. The bubble shot and the next one come from the game. LEVEL at the bottom |
| Puzzle De Pon! R! | `puzzldpr.json` | the bubble in the launcher and the next one, LEVEL | the same boards between their brick pillars and the star dial as Puzzle De Pon!, under a pink sky full of stars, as in the game |
| Panic Bomber | `panicbom.json` | the power gauges of both players, the level | two fields on the green checkerboard as in the game, the pieces of three little round heads of our own fall and stack, three of a colour burst, the bombs blow up in a cross of flames. The points read in the game set the bombs off, the power going up is a big blast. SCORE and NEXT above each field |
| Pop 'n Bounce | `popbounc.json` | the lives, a bouncing ball | the jungle at dusk as in the game, soft round creatures of our own piled up at the top of the field, the bar at the bottom sends the ball back, a creature hit bursts with the ones of its colour that touch it. ATTACK at the top, 1P, the lives and BALL in the middle |
| Super Bubble Pop | `sbp.json` | the coloured blocks | the magenta swirl and its lilac bubbles as in the game, the white board seen at an angle where the bubbles fall, our little robot of our own shoots its bubble up a column, three of a colour burst. The score in its capsule at the top |
| Spin Master | `spinmast.json` | the health segments, B and the bombs, the lives, the desert | the desert of the pyramids as in the game, a deep blue sky, great pyramids, a sphinx, dunes and a wall of stone blocks. Our hero of our own throws his yo-yo at the soldiers and the birds, a bomb spent blows up the screen. 1P, the health in orange segments and the bombs B at the top, the lives at the bottom |
| Ganryu | `ganryu.json` | the timer, the lives, the weapons left, a street at night | a street of old Japan at night as in the game, wooden houses under their dark tiled roofs, curtains with a round crest, lanterns. Our swordsman of our own fights the ninjas of the night, his blade leaves a trail of light, a weapon spent in the game is thrown. PLAYER_1 and the score, the yellow gauge, a face for each life, TIME in big numbers, the weapon and its count |
| Zupapa! | `zupapa.json` | the lives, the platforms | the blue cave and its old stone statues as in the game, the platforms striped orange and blue. Our little round hero of our own walks the platforms, jumps from one to the other and boots the monsters, who fly off in a shower of stars. P1, the score and the lives |
| Neo Mr. Do! | `neomrdo.json` | the lives as cherries, the field of tiles | the field of coloured tiles and their toys and tools inside a frame of stars, as in the game. Our little digger of our own digs his tunnels, picks the cherries, the blue monsters follow him in the tunnels and fall to his power ball. 1P-, the lives and EXTRA lit letter by letter |
| Super Sidekicks | `ssideki.json` | the goals of both teams in big numbers, the time | the match in the stadium, the two flags with the goals in their orange boxes and TIME on its panel, as in the game. A goal read in the game sends the ball into the net |
| Super Sidekicks 2 | `ssideki2.json` | the goals of both teams in big numbers | the match in the stadium, the blue band at the top with the two flags and the goals in big white numbers, as in the game. A goal read in the game sends the ball into the net |
| Tecmo World Soccer '96 | `twsoc96.json` | the pitch and a ball crossing it | the match in the stadium, the two flags at the top and the round clock between them, as in the game. No value of the game is known yet, so the match plays by itself |
| Goal! Goal! Goal! | `goalx3.json` | the goals of both teams in big numbers, the time | the match in the stadium, the flags and the goals in big yellow numbers at the top, the time with its little moon, as in the game. A goal read in the game sends the ball into the net |
| Neo-Geo Cup '98 | `neocup98.json` | the goals of both teams in big numbers | the match in the stadium, the blue band at the top with the two flags and the goals, as in the game. A goal read in the game sends the ball into the net |
| Soccer Brawl | `socbrawl.json` | the goals of both teams in big numbers, the POWER METER of each team, the time | football of the future on a pitch at night, the players of our own in their armour, the POWER METER of each team at the top and TIME below, as in the game. The goals and the power read in the game |
| Football Frenzy | `fbfrenzy.json` | the points of both teams in big numbers, the clock of the quarter, the yard lines | the field seen from above with its yard lines and its red and blue end zones, as in the game. Two teams of our own line up, the ball is snapped, the runner breaks through until he is tackled. The points read in the game are touchdowns. The points of both teams in big yellow numbers and the clock of the quarter at the top |
| Pleasure Goal | `pgoal.json` | the goals of both teams in big numbers, the time | futsal, five against five in the stadium, a face of our own for each team beside its goals and the time in the middle, as in the game. A goal read in the game sends the ball into the net |
| Baseball Stars Professional | `bstars.json` | the inning, the count B S O in lights | the field seen from behind home plate, the batter of our own, the count B S O in lights with the clock and the box with the inning, as in the game. The balls, strikes and outs read in the game make the pitches |
| 2020 Super Baseball | `2020bb.json` | the field and the time | baseball of the future on its bright field, the blue box with the inning and the time, as in the game. The outs counted in the game make the plays, between them the game plays by itself |
| Top Player's Golf | `tpgolf.json` | STROKE and the strokes, the time left for the stroke | the course and its flag, the blue boxes with HOLE and PAR, STROKE and the time, as in the game. The ball flies to the flag at each stroke read in the game |
| Power Spikes II | `pspikes2.json` | the power gauges of both players, the time | the indoor arena with its lamps and its stands full of people, three players of our own on each side of the net, as in the game. The ball flies from one side to the other, the players jump and spike. A super shot spent in the game is a spike on fire. The time on its board and the POWER gauges |
| Bang Bead | `bangbead.json` | the street court and the ball, TIME, the 'Miracle' power gauges and their stars | the street court seen from above as in the game, the cars parked along the pavement, the manhole and the orange lane marks. Two players of our own hit the ball from one end to the other, the goal lines and their yellow stars light up at each goal, a 'Miracle' power spent in the game is a shot on fire. PLAYER and the score, TIME in the middle, the power gauges at the bottom |
| Battle Flip Shot | `flipshot.json` | the arena and its target, the ball, TIME | the arena of teal metal seen from above as in the game, its circuits, the big orange target in the middle. Two players of our own behind their shields send the glowing ball back, the six targets of each player along his wall crack and break, a target hit in the game is a shot on it. SCORE and TIME at the top |
| Over Top | `overtop.json` | the time, RANK, the speed, the lap time | the stages seen from the sky as in the game, a dirt track through the pine forest, then a grey road between the fields, the red car among its rivals. The map in its little television at the top left, the time in big yellow numbers, RANK, the speedometer and the lap time. A place won in the game is a rival overtaken |
| Stakes Winner | `stakwin.json` | a galloping horse, the speed, stamina and strength of the horse | a Japanese racecourse as in the game, the green turf and its white rails, the grandstand and its crowd. Eight horses and jockeys of our own gallop, the player's horse wears its 1P, the finish post comes and the winner is shown. The race clock at the top left, the horse's gauge at the bottom, its speed, stamina and strength read in the game |
| Stakes Winner 2 | `stakwin2.json` | a galloping horse, POWER, the speed, stamina and burst of the horse | Longchamp as in the game, its grandstand and its windmill, the green turf. The horses of our own gallop, POWER at the bottom read in the game, power spent is a dash of the player's horse, its speed, stamina and burst |
| Jockey Grand Prix | `jockeygp.json` | a galloping horse on the dirt, CREDIT | the dirt track and its green rail as in the game, eight numbered horses of our own, the odds board at the top with the race numbers, WAGER and CREDIT. The winner's number lights up on the board. No value of the game is known yet, so the races run by themselves |
| Gururin | `gururin.json` | the next piece in its colours, the level | the blue and purple checkerboard as in the game, the golden pillars and their medallions, the boards in their golden frames. The little round fellows of our own fall three by three, four of a colour that touch leave, and the board turns a quarter now and then, everything falling the other way. The piece and the next one in their colours read in the game, LEVEL |
| Ghostlop | `ghostlop.json` | TIME | a city street at night as in the game, the two fields full of little ghosts of our own in their colours, a little ghost hunter below each field shoots the ghosts up, three of a colour that touch vanish. In the middle, PLAYER 1 and its score, TIME in big numbers, PLAYER 2 or COMPUTER |
| Pochi and Nyaa | `pnyaa.json` | the blocks | the green forest and its soft lights as in the game, the fields of soft blocks with the little faces of cats and dogs of our own, the pairs fall, four of a colour that touch leave and the chains count. NEXT beside the field, the score at the top, and big plush bears of our own sitting in the forest |
| Puzzled | `joyjoy.json` | the next piece in its colour, the balloons left | the green hills and the white clouds as on the title of the game, the brick towers and their wells. The pieces fall and fill the lines, the full lines leave, and when the bricks of the stage are gone the kid's balloon floats away. NEXT in its colour read in the game, the score, STAGE and the balloons left in the middle |
| Zintrick | `zintrckb.json` | the time, the ENERGY gauges | green mountains under a pale sky as in the game, the two fields in their purple frames, the jewels shaped like drops hang from the top. A little thrower of our own below each field throws a jewel up a column, three of a colour in a line leave, an item used in the game clears a row. The time in big numbers between the fields, ENERGY, ITEM and LEVEL of each player |
| Digger Man | `diggerma.json` | the lives, the bombs, ENERGY, a little digger | the mine in its grey brick frame as in the game, the orange earth, the grey stone walls, the rocks that fall into the tunnels, the coloured jewels. Our little digger of our own digs his way to each jewel, a bomb spent in the game blows up the stones around him. The score, the jewels left in big blue numbers, ENERGY, the lives and the bombs |
| The Irritating Maze | `irrmaze.json` | TIME and its tenths, the lives | the red checkered floor as in the game, the corridor of the maze between its blue rails, the big arrow, the bumper and the crate. Our pointer goes along the corridor without touching the rails, a life lost in the game is an electric shock. TIME in red LED numbers with its tenths, the map of the maze with the pointer |
| Andro Dunos | `androdun.json` | the score or the title, the ships left, the ship that follows the stick and fires, POWER UP | space over a planet as in the game, the blue glow of the horizon and the rocky ground, our small fighter of our own against round enemy pods. 1P and the score, the four weapons and their levels read in the game in their colours, the ships left |
| Captain Tomaday | `ctomaday.json` | the score or the title, the lives, the ship that follows the stick and fires, POWER UP | the forest seen from the sky as in the game, its little red-roofed houses, the railway and its steam train, a river. Our little red craft of our own with its green leafy crest against flying tin robots. PLAYER 1 and the score, the lives and the power of both arms read in the game |
| Choutetsu Brikin'ger | `ironclad.json` | the score or the title, the life meter, the ship that follows the stick and fires, POWER UP, LEVEL 2 | the sea at dusk, the iron warships on the horizon, our steam fighter of our own and its robot fist against flying gunboats. The life meter, POWER and LEVEL read in the game, the arm weapons |
| Last Hope | `lasthope.json` | the score or the title, the ship that follows the stick and fires | deep space as in the game, full of blue and white stars, the nebulas and a big blue planet, our small fighter of our own and its blue pod against red barrel drones. The score at the top |
| Bang Bang Busters | `b2b.json` | the hearts, the boss gauge | the ice world as in the game, the blue sky and its aurora, the platforms of ice blocks. Our little buster of our own traps the penguins and the seals of our own in his bubbles and kicks them away. The score and the hearts at the top, the stage, the boss gauge read in the game |
| Crossed Swords | `crsword.json` | the energy, GOLD, the magic | the forest at night as in the game, an armoured knight of our own faces us with his shield and his sword, our own knight is seen from behind as an outline of light. They cross swords, ENEMY and its gauge at the top. The energy, the gold and the magic read in the game, a blow taken, the gold that rises, a spell of lightning |
| Eight Man | `eightman.json` | LIFE, BOMB, the time | the ruined city at sunset as in the game, golden towers and a fallen bridge. A fast cyborg of our own, blue and silver, fights purple mutants and armed cyborgs, and leaves a trail of copies behind him when the game turns its 8 Power on. 1P and the score, LIFE, BOMB and the time in its red box |
| Nightmare in the Dark | `nitd.json` | the lives, the time, the full moon, a little gravekeeper | the graveyard at night under a huge full moon as in the game, the platforms of mossy stones, the bare trees and the graves. Our little gravekeeper of our own sets the zombies and the ghosts of our own on fire with his lantern and kicks the balls of fire away. 1UP and the score, the lives and TIME in yellow read in the game |
| The Super Spy | `superspy.json` | the energy, the bullets, the corridor | the corridor of the building as in the game, its doors and their red signs, a masked fighter of our own faces us with his knives, our fists strike from below. The energy read in the game drops when he hits us, a bullet spent is a shot, he falls and we go up a floor. 1P and the score, EX, the weapon and its bullets, the floor |
| Quiz King of Fighters | `quizkof.json` | the lives as hearts, Q and the four answers | a stage in the city at night as in the game, two fighters of our own face to face. The question panel and its four answers A B C D, the time that runs. The questions are our own, the score that rises is a right answer and a big circle, a life lost is a wrong answer and a big cross. P1, the score and LIFE |
| Quiz Daisousa Sen | `quizdais.json` | the lives as hearts, Q and the four answers | the wire fence in front of the city at dusk as in the game, a hooded detective of our own and his partner. The question panel and its four answers A B C D, the time that runs. The questions are our own, the score that rises is a right answer and a big circle, a life lost is a wrong answer and a big cross. P1, the score and LIFE |
| Quiz Meitantei Neo & Geo | `quizdai2.json` | the lives as hearts, Q and the four answers | a detective's office as in the game, its shelves of books and its window, an old detective of our own and his young assistant. The question panel and its four answers A B C D, the time that runs. The questions are our own, the score that rises is a right answer and a big circle, a life lost is a wrong answer and a big cross. P1, the score and LIFE |
| Chibi Maruko-chan Deluxe Quiz | `marukodq.json` | the lives as hearts, Q and the four answers | a television studio as in the game, its lights and its rainbow, two children of our own on the set. The question panel and its four answers A B C D, the time that runs. The questions are our own, the score that rises is a right answer and a big circle, a life lost is a wrong answer and a big cross. P1, the score and LIFE |
| Minasan no Okagesamadesu! | `minasan.json` | the tiles, the steps of the die | the blue table and its mahjong game as in the game. The hidden hand of the opponent at the top, the tiles thrown in the middle, our hand of thirteen tiles at the bottom. A tile is drawn, a tile is thrown, now and then a hand wins with RON or TSUMO, and the boxes of points on the right follow our own game. The steps of the board game read in the game roll a die, the time to play |
| Mahjong Kyo Retsuden | `mahretsu.json` | the tiles, the time | the green felt and the yellow tile backs as in the game. The hidden hand of the opponent at the top, the tiles thrown in the middle, our hand of thirteen tiles at the bottom. A tile is drawn, a tile is thrown, now and then a hand wins with RON or TSUMO, and the boxes of points on the right follow our own game. The time to play read in the game |
| Janshin Densetsu | `janshin.json` | the tiles, HP | the purple felt and the green tile backs as in the game. The hidden hand of the opponent at the top, the tiles thrown in the middle, our hand of thirteen tiles at the bottom. A tile is drawn, a tile is thrown, now and then a hand wins with RON or TSUMO, and the boxes of points on the right follow our own game. The panel of the hero with HP, MP, WEAPON and SHIELD read in the game, the HP that drop, the time to play |
| Bakatonosama Mahjong Manyuuki | `bakatono.json` | the tiles, the time | the olive felt and the orange tile backs as in the game. The hidden hand of the opponent at the top, the tiles thrown in the middle, our hand of thirteen tiles at the bottom. A tile is drawn, a tile is thrown, now and then a hand wins with RON or TSUMO, and the boxes of points on the right follow our own game. The time to play read in the game |
| Idol Mahjong Final Romance 2 | `froman2b.json` | the tiles | the green felt in its wooden frame and the orange tile backs as in the game. The hidden hand of the opponent at the top, the tiles thrown in the middle, our hand of thirteen tiles at the bottom. A tile is drawn, a tile is thrown, now and then a hand wins with RON or TSUMO, and the boxes of points on the right follow our own game |
| Shougi no Tatsujin | `moshougi.json` | the wooden board | the rocky coast by the sea as in the game, the wooden board and its two stands, the opponent's at the top left and ours at the bottom right. Our own pieces move one by one, a piece taken goes onto the stand of the one who took it, each player's clock runs |

- The values come from the FinalBurn Neo and MAME 2003-Plus cheats and still have to be confirmed in game (`test_retroarch.bat` shows them). The score of Blazing Star, Puzzle Bobble, Shock Troopers, Pulstar, Magical Drop III, Sengoku 3, Top Hunter, Last Resort, the two Aero Fighters, Strikers 1945 Plus, Super Dodge Ball, Neo Bomberman, League Bowling, Magician Lord, NAM-1975, Cyber-Lip, Ghost Pilots, Alpha Mission II, Viewpoint, Zed Blade, Prehistoric Isle 2, Shock Troopers 2nd Squad, Robo Army, Burning Fight, Mutation Nation, Sengoku, Sengoku 2, Ninja Combat, Ninja Commando, Blue's Journey, Puzzle Bobble 2, Magical Drop II, Money Puzzle Exchanger, Puzzle De Pon!, Puzzle De Pon! R!, Panic Bomber, Pop 'n Bounce, Super Bubble Pop, Spin Master, Ganryu, Zupapa!, Neo Mr. Do!, Bang Bead, Battle Flip Shot, Gururin, Ghostlop, Pochi and Nyaa, Puzzled, Zintrick, Digger Man, Andro Dunos, Captain Tomaday, Choutetsu Brikin'ger, Last Hope, Bang Bang Busters, Crossed Swords, Eight Man, Nightmare in the Dark, The Super Spy, Quiz King of Fighters, Quiz Daisousa Sen, Quiz Meitantei Neo & Geo and Chibi Maruko-chan Deluxe Quiz is in no database, learn it with `learn.bat` (see Learning the score). Until then, the title scrolls in its place on the panel.
- When the stick and the buttons can be read (the Neo Geo BIOS keeps them, with MAME as with RetroArch), the ships of Blazing Star, Pulstar, Last Resort, Viewpoint, Zed Blade and Prehistoric Isle 2, the planes of the Aero Fighters, Strikers 1945 Plus, Ghost Pilots and Alpha Mission II, the commando of Shock Troopers 2nd Squad and the ninja of Ninja Commando (up and down), the hunters of Top Hunter, the witches of Twinkle Star Sprites, the arrows of Puzzle Bobble, Puzzle Bobble 2 and the two Puzzle De Pon!, the jesters of Magical Drop II and III and the piggy banks of Money Puzzle Exchanger follow them. Button A fires in Blazing Star, Pulstar, Last Resort, the Aero Fighters, the two Shock Troopers and Ninja Commando, and strikes in Sengoku 3 and Top Hunter. In Top Hunter, up and down jump from one lane to the other and B jumps. In Last Resort, button B launches the unit. In Magical Drop II and III and Money Puzzle Exchanger, button A grabs the drops or the coins and B throws them back. As long as the player has not touched them, the scene plays by itself. On the panel of the fifteen shoot'em ups, the ship follows the stick and fires with button A too.
- With nobody playing, the coin screen, as for the fighting games (see Coin screen).
- `demo_neogeo.bat` shows them without playing. Pick the game in the list, or give it directly, `demo_neogeo.bat wjammers` for example.

### All Neo Geo games

Neo Geo games known to MAME (clones included) get a shared scene based on their genre, with nothing to set up. At the top, the game's title, still when it fits, scrolling otherwise.

| Genre | File | What is shown |
|---|---|---|
| Fighting (King of Fighters, Samurai Shodown, Fatal Fury, Art of Fighting, World Heroes...) | `neogeo_combat.json` | Vera style. At the top the score, or the title as long as the score has not been learned, and on the computer's side INSERT COIN blinking, or the credits and PRESS START in turn. In the middle the green health bars and the timer in a frame, "KO" at the end of the fight (52 games, see the Fighting games table), otherwise "VS". At the bottom "P1", and "CPU" or "P2" opposite. In 34 games, the name of the character currently fighting shows next to it, in white ("P1 RALF" and "LEONA CPU"). A thin orange line at the very bottom. When nobody is playing, the coin screen (below) |
| Shoot'em up (Zed Blade, Viewpoint, Ghost Pilots...) | `neogeo_shoot.json` | a small ship flying through a star field, firing when the score goes up |
| Sports and racing (Neo Drift Out, Riding Hero, Super Sidekicks 2...) | `neogeo_sport.json` | a field with a bouncing ball |
| Puzzle, quiz, mahjong (Puzzle De Pon, Pop 'n Bounce, Magical Drop II...) | `neogeo_reflexion.json` | a row of colored blocks that keep changing |
| Action, platformers, beat'em ups and everything else (Ninja Combat, Sengoku 2, Cyber-Lip...) | `neogeo.json` | blue hills, and both players' health bars when they are known |

- With RetroArch, the scene shows "NEO GEO" in the middle as long as nothing is known for that game. With MAME, the credits are shown as well.
- With RetroArch, every Neo Geo set of FinalBurn Neo is recognized. A version, a bootleg or a hack takes the file of its original game, as with MAME. Metal Slug 3 Fully Decrypted takes the one of Metal Slug 3, and KOF 2002 Magic Plus the one of KOF 2002 with its own name. A homebrew game gets the scene of its genre. Only the BIOS and the test programs are not recognized. The list is in `dmd\neogeo_sets.json`, and `test_retroarch.bat` tells which game a version takes the file of.
- The credits of a Neo Geo MVS are stored in the cabinet's backup memory. MAME reads it. RetroArch's FinalBurn Neo core only shares the game's work RAM, so not the credits. ArcadeDMD then guesses them from the Neo Geo BIOS, which leaves traces in the work RAM. A coin put in while nobody plays drops on the panel and the HD screen, PRESS START follows, and each player who starts takes a credit. During a game, the BIOS only shows the first coin. For every coin to be seen with its side, run `coin_buttons.bat` once (Coin buttons, below). FinalBurn Neo keeps the credits of each game when it is quit and gives them back the next time. ArcadeDMD keeps its guessed credits the same way (`runtime\neo_credits.json`) and starts from them when the game starts on its title screen. FinalBurn Neo must be in MVS mode (core option Neo-Geo mode), the AES mode of the home console takes no coins. `runtime\arcadedmd.log` tells what the BIOS did, and `test_coins.bat` writes down in detail what changes in its memory while you put coins in on the left and on the right. Some games keep a copy of the credits in their work RAM. To find out, learn them with `learn.bat` (same method as for the score) by typing `credits=2`, then insert another coin and type `credits=3`, and once more. If the tool finds an address, the credits are shown. If it answers "Nothing found", that game does not keep a copy.
- The health bars and the timer come from the MAME 2003-Plus cheat database. They work with RetroArch as well as with MAME.
- Learn a game's score with `learn.bat` (same method as just below). The tool then creates `games\<game>.json`, for example `games\kof98.json`. It keeps the genre scene and its health bars, and adds the score. The shared files are never modified.
- A game that has its own file (the Metal Slug games, or the games done one by one just above) always takes priority over the shared scene.
- The KOF 98 score was found with `learn.bat`. It is stored in each player's data block, and that block is the same from KOF 96 to 2001 (health bar and power gauge at the same addresses). So the score of these games is read from the same place. If the panel does not show the same score as the screen in one of them, learn it with `learn.bat`, and the address found replaces the assumed one.
- In King of Fighters '96 to 2000, each team is read from the game memory (chosen characters, fighting order, characters already beaten). The name changes by itself when the next character steps in. `test_retroarch.bat` shows both characters read, which is handy for checking.
- The Neo Geo BIOS tells who is playing. Against the computer, "CPU" shows opposite, with INSERT COIN blinking on its side, or the credits and PRESS START in turn when there are credits left. With two players, both scores are at the top. When nobody is playing, the coin screen just below.

### Capcom CPS1, CPS2 and CPS3 games

Every Capcom CPS1, CPS2 and CPS3 game of FinalBurn Neo is recognized, with MAME as with RetroArch. That makes 88 games and their 942 sets. A version, a bootleg or a hack takes the file of its original game, with its own name when it has one (Street Fighter II' Magic Delta Turbo, for example). A version whose own cheats put a value elsewhere reads it there, in the `"per_game"` section of the file (the second revision of JoJo's Venture, Quiz & Dragons' Japanese resale, the US Eco Fighters). The files are made by `tools/cps_games.py` from the list and the cheat database of FinalBurn Neo.

![Four Capcom fighting games on their stages, HD display](docs/images/hd_capcom_stages.jpg)

- **What is read.** Each player's health, the timer, the lives, the bombs, the super gauge, the characters and their names, the stage, and the credits when the game keeps them. The timer shows when the cheat gives all of it. In 23 games it only gives a part, one digit, the seconds of a clock or a counter that is not the timer seen in the game. ArcadeDMD then reads it only to see that the game runs, without showing it. The score is not in the cheat databases, learn it with `learn.bat` (Learning the score, below).
- **Who plays.** The Capcom games have no BIOS that tells it. ArcadeDMD watches the timer, the score once it is learned, the health, the lives and the bombs. As long as they move, player 1 plays. After 10 seconds without any change, the coin screen comes back. This needs the timer or the score (or the health in a fighting game), because the lives and the bombs alone change too seldom. Without them, the game stays on its game scene. When the game's credits are read (learned with `learn.bat` if needed), one or two credits spent are a start, and player 1 plays from the select screen on, for 45 seconds until the fight moves.
- **RetroArch.** FinalBurn Neo core. CPS1 and CPS2 share 64 KB of RAM from 0xFF0000, CPS3 its 512 KB from 0x2000000, with its bytes reversed in 32-bit words that ArcadeDMD puts back in order. A value outside of this RAM (the credits of some CPS2 games) is read with MAME only. 1944 and Dimahoo keep all their values outside of it, so RetroArch shows nothing of them and the log says so. Launch these two games with MAME to see everything (in LaunchBox, Edit, then the Emulation tab). Mercs is set for three players in FinalBurn Neo, and with two controllers one of them drives two players. Set its DIP switches to Play Mode 2 Player and Coin Slots 1 (Quick Menu, Core Options, DIP Switches), then restart the game.
- **Credits.** Under RetroArch most Capcom games do not give their credits. Once `coin_buttons.bat` has shown ArcadeDMD your coin buttons, it counts them. A coin gives a credit, and a player who begins takes one. Once the START buttons are shown too, a player who presses START with a credit begins at once. Otherwise the start is seen when the game starts moving, a continue and player 2 joining in when the lives come back from 0 by 2 or more (an extra life is only 1), and in Mercs, which has no lives, when the energy comes back from 0. Player 2 also takes one when his values start moving after 45 seconds without (his score goes up, a life or a bomb spent, a hit taken), out of the fighting games where his health is the computer's. Game files say it in their `"coins"` section. It stays a guess. For an exact count, learn where the game keeps its credits with `learn.bat` (`credits=0`, `credits=1`, `credits=2`...), the game itself then gives them, continues included.
- **Fighting games.** On the panel, the health bars, the timer, the names, and on the bottom line the super gauge of each player, blue as it fills up, gold and blinking when it is full. On the HD screen, the fight scene on the game's own stage, with the place under the stage banner (CHINA, INDIA, FEAST OF THE DAMNED...), and the super gauges under the fighters. Street Fighter II, its Champion Edition and Hyper Fighting, Super Street Fighter II, Street Fighter Alpha and Night Warriors read the rounds won by each player (cheat database), X-Men: Children of the Atom too (found in captures made on a cabinet). They are gold stars under the bars on the HD screen and gold squares next to the timer on the panel, and the winner of a round is the one whose count goes up. A health bar that goes below zero at a K.O. (0xFF in its byte, Street Fighter II) reads empty, it read full and the K.O. was missed. Both bars emptied at once (the select screen after START, the end of a game) are not a K.O. The super gauge of Marvel vs. Capcom, Marvel Super Heroes, X-Men vs. Street Fighter and X-Men: Children of the Atom has levels, like the game. The bar is the one of the current level (`power`), with POWER and the level beside it (`power_level`, `"max"` for the top level, where the bar shows full with POWER MAX). In Marvel vs. Capcom, Marvel Super Heroes vs. Street Fighter and X-Men vs. Street Fighter each player has two fighters who take turns. The health and the name shown are those of the fighter on screen, made by the engine from the values of both (`"tag"` in the game file, a `"team"` expression), and the team is K.O. only when both are down. Player 2 is a human or the computer. Street Fighter Alpha, Alpha 3, Marvel vs. Capcom, Vampire Hunter 2 and JoJo's Bizarre Adventure read it in the game (cheat database, `"human"` in the `activity` section), and so do Marvel Super Heroes vs. Street Fighter, X-Men vs. Street Fighter and X-Men: Children of the Atom (found in captures made on a cabinet). Player 1 is the computer when player 2 plays alone, read in these games, seen in the others from player 2's START followed by a credit the game spends. In the other fighting games, player 2 is a human from the moment his score goes up (once it is learned, but not in the Marvel games where the computer scores too, `"cpu_scores"` in the `activity` section), he presses START with a credit, or a credit is spent during a fight (a challenger), until nobody plays any more or his score has not moved for two minutes. Street Fighter II reads its credits and the score of player 1, learned with `learn.bat` on a cabinet under RetroArch. Player 2's score is taken at the same place in his own block and is still to be confirmed. A credit spent is then a start, seen at the character select. The fighter of Street Fighter III: New Generation is told by two bytes, a row and a column of the select screen, and the game file joins them (`"join"`).
- **The other games.** Each one has its own panel scene and HD scene, see Capcom games done one by one just below.
- `demo_capcom.bat` plays the demo of a Capcom game, most of them with the coin screen first.

| Game | System | File | Health bars | Timer | Character names | Super gauge | Stages (HD) |
|---|---|---|---|---|---|---|---|
| Cyberbots: Fullmetal Madness | CPS2 | `cybots.json` | yes | yes | yes (10) | yes | yes |
| Darkstalkers: The Night Warriors | CPS2 | `dstlk.json` | yes | yes | yes (12) | - | yes |
| Hyper Street Fighter II: The Anniversary Edition | CPS2 | `hsf2.json` | yes | yes | yes (17) | yes | fixed |
| JoJo's Bizarre Adventure | CPS3 | `jojoba.json` | yes | yes | yes (25) | yes | fixed |
| JoJo's Venture | CPS3 | `jojo.json` | yes | yes | - | yes | fixed |
| Marvel Super Heroes | CPS2 | `msh.json` | yes | yes | yes (13) | yes | fixed |
| Marvel Super Heroes Vs. Street Fighter | CPS2 | `mshvsf.json` | yes | yes | yes (25) | yes | fixed |
| Marvel Vs. Capcom: Clash of Super Heroes | CPS2 | `mvsc.json` | yes | yes | yes (22) | yes | yes |
| Mega Man 2: The Power Fighters | CPS2 | `megaman2.json` | yes | - | - | - | fixed |
| Mega Man: The Power Battle | CPS1 | `megaman.json` | yes | - | - | - | fixed |
| Muscle Bomber Duo: Ultimate Team Battle | CPS1 | `mbombrd.json` | yes | - | - | - | fixed |
| Night Warriors: Darkstalkers' Revenge | CPS2 | `nwarr.json` | yes | yes | yes (14) | - | yes |
| Red Earth | CPS3 | `redearth.json` | yes | - | - | - | yes |
| Ring of Destruction: Slammasters II | CPS2 | `ringdest.json` | yes | yes | - | - | fixed |
| Saturday Night Slam Masters | CPS1 | `slammast.json` | yes | - | - | - | fixed |
| Street Fighter Alpha 2 | CPS2 | `sfa2.json` | yes | yes | yes (24) | yes | yes |
| Street Fighter Alpha 3 | CPS2 | `sfa3.json` | yes | yes | yes (29) | yes | yes |
| Street Fighter Alpha: Warriors' Dreams | CPS2 | `sfa.json` | yes | yes | yes (13) | yes | yes |
| Street Fighter II': Champion Edition | CPS1 | `sf2ce.json` | yes | yes | yes (12) | - | yes |
| Street Fighter II': Hyper Fighting | CPS1 | `sf2hf.json` | yes | yes | yes (12) | - | yes |
| Street Fighter II: The World Warrior | CPS1 | `sf2.json` | yes | yes | yes (12) | - | yes |
| Street Fighter III 2nd Impact: Giant Attack | CPS3 | `sfiii2.json` | yes | yes | yes (15) | yes | yes |
| Street Fighter III 3rd Strike: Fight for the Future | CPS3 | `sfiii3.json` | yes | yes | yes (19) | yes | yes |
| Street Fighter III: New Generation | CPS3 | `sfiii.json` | yes | yes | yes (11) | yes | yes |
| Street Fighter Zero | CPS1 | `sfzch.json` | - | - | - | - | fixed |
| Street Fighter Zero 2 Alpha | CPS2 | `sfz2al.json` | yes | yes | yes (21) | - | yes |
| Super Gem Fighter: Mini Mix | CPS2 | `sgemf.json` | yes | yes | yes (12) | yes | yes |
| Super Street Fighter II Turbo | CPS2 | `ssf2t.json` | yes | yes | yes (16) | yes | yes |
| Super Street Fighter II: The New Challengers | CPS2 | `ssf2.json` | yes | yes | yes (16) | - | yes |
| Vampire Hunter 2: Darkstalkers Revenge | CPS2 | `vhunt2.json` | yes | yes | yes (21) | yes | yes |
| Vampire Savior 2: The Lord of Vampire | CPS2 | `vsav2.json` | yes | yes | yes (19) | - | yes |
| Vampire Savior: The Lord of Vampire | CPS2 | `vsav.json` | yes | yes | yes (18) | - | yes |
| X-Men Vs. Street Fighter | CPS2 | `xmvsf.json` | yes | yes | yes (19) | yes | fixed |
| X-Men: Children of the Atom | CPS2 | `xmcota.json` | yes | yes | yes (13) | yes | yes |

The addresses come from the cheat database of FinalBurn Neo and still have to be confirmed in game (`test_retroarch.bat` shows them). "fixed" means the game always gets the same backgrounds, taken from a list that fits it (the ring of the Slam Masters, the laboratory of Mega Man).

### Capcom games done one by one

Like the Neo Geo games, the other Capcom games got a panel scene and an animated HD scene of their own, fifty of them. Everything is drawn by the program, no image, character or logo comes from the games.

- **The games with characters, like Metal Slug (1.30).** The beat'em ups, the action games and platformers, the two Pang and Mercs show no character drawn by the program any more. The place of the game stays behind, calm and darker. Each player has a panel with what is read in the game (gauge, lives, score, bombs, weapon, level), and the middle shows the logo, TIME when the timer is read whole (red when little time is left) and the credits. The game's events show between the panels. Points are a blow in the middle, a punch, a shot, a slash, a thrown weapon, a spell or a balloon that bursts. A bomb or a special leaves the panel and the middle blows up. A life lost turns the panel red and shakes the screen, health that comes back says + LIFE, and a level gained says LEVEL UP! Player 2's panel lights up when his health, his lives or his score move, and goes dark 45 seconds after they stop.
- **Shoot'em ups.** Once the score is learned, an enemy only blows up when the game scores points, as with the Neo Geo. A bomb spent sweeps the screen, the weapon picked up and the plane chosen are named. On the panel, the plane, the ship or the soldier of the game flies and fires. Player 2 comes in when his score goes up, or when he loses a life, spends a bomb or takes a hit, and leaves 45 seconds after they stop. The credits show under the logo. Mercs shows in panels, like the beat'em ups.
- **Action games and platformers.** In their panels, the weapon held is read in Ghouls'n Ghosts and Three Wonders, the armour in Ghouls'n Ghosts, the partner and the floor in Magic Sword, the hero in Willow, and the points of Pang! 3 and Mighty! Pang burst a balloon. Strider and Willow keep one panel, the players take turns.
- **Puzzle games, quizzes and mahjong.** They play by themselves, with our own questions, tiles, gems and bubbles, and follow what is read in the game. A life lost in a quiz is a wrong answer.
- **The small games** (Frog Feast, Pokonyan! Balloon, Magical Pumpkin, Ganbare! Marine Kun) play by themselves too. The frogs leap, the balloon flies over the savanna, the pumpkin carriage rolls through the town, the sight follows the fish.
- Final Fight Anniversary Edition and Final Fight EX (CPS2 hacks) take the scene of Final Fight, Tenchi wo Kurau II CPS Changer the one of Warriors of Fate.
- The values come from the cheat databases of FinalBurn Neo and MAME 2003-Plus and still have to be confirmed in game (`test_retroarch.bat` shows them). The score is in neither of them, learn it with `learn.bat`, the title of the game takes its place on the panel until then. The King of Dragons counts its experience, which is read.
- With nobody playing, the coin screen (see Who plays, just above).
- `demo_capcom.bat` shows them without playing. Pick the game in the list, or give it directly, `demo_capcom.bat ffight` for example.

![Final Fight, Captain Commando, Cadillacs and Dinosaurs and The Punisher on an LCD marquee, HD display](docs/images/hd_cps_beat_1.jpg)

![The King of Dragons, Knights of the Round, Warriors of Fate and Dungeons & Dragons: Shadow over Mystara on an LCD marquee, HD display](docs/images/hd_cps_beat_2.jpg)

![Dungeons & Dragons: Tower of Doom, Alien vs. Predator, Armored Warriors and Battle Circuit on an LCD marquee, HD display](docs/images/hd_cps_beat_3.jpg)

![1944, 19XX, 1941, Varth and U.N. Squadron on an LCD marquee, HD display](docs/images/hd_cps_shooters_1.jpg)

![Carrier Air Wing, Forgotten Worlds, Giga Wing and Progear on an LCD marquee, HD display](docs/images/hd_cps_shooters_2.jpg)

![Mars Matrix, Dimahoo, Eco Fighters and Mercs on an LCD marquee, HD display](docs/images/hd_cps_shooters_3.jpg)

![Ghouls'n Ghosts, Strider, Pang! 3, Mighty! Pang and Super Puzzle Fighter II Turbo on an LCD marquee, HD display](docs/images/hd_cps_action_1.jpg)

![Mega Twins, Magic Sword, Willow, Nemo and Three Wonders on an LCD marquee, HD display](docs/images/hd_cps_action_2.jpg)

![Dynasty Wars, Puzz Loop 2, Capcom Sports Club, Quiz & Dragons and Adventure Quiz Capcom World 2 on an LCD marquee, HD display](docs/images/hd_cps_action_3.jpg)

![Quiz Tonosama no Yabou 2, Quiz Nanairo Dreams, Jyangokushi, Janpai Puzzle Choukou and Gulun.Pa! on an LCD marquee, HD display](docs/images/hd_cps_small_1.jpg)

![Pnickies, Frog Feast, Pokonyan! Balloon, Magical Pumpkin and Ganbare! Marine Kun on an LCD marquee, HD display](docs/images/hd_cps_small_2.jpg)

| Game | File | Panel | HD screen |
|---|---|---|---|
| Final Fight | `ffight.json` | the yellow gauge over red, TIME in purple, =lives, the brick tenements | panels on the brick slum of a big American city by day. LIFE yellow over red, the lives, the score, punches in the middle |
| Captain Commando | `captcomm.json` | the green gauge, xlives, the glass fronts and their neon | panels on a city of the future by day, its glass fronts and their neon. The name of the hero chosen in the game, LIFE in green, the lives, the score, punches |
| Cadillacs and Dinosaurs | `dino.json` | the yellow gauge, =lives, the broken columns and the old car | panels on a town swallowed by the jungle, smoking volcanoes far off. The name of the hero chosen in the game, LIFE yellow over red, the lives, the score, punches |
| The Punisher | `punisher.json` | the cyan gauge, xlives, the grenades | panels on the hall of a mobster's mansion at night. LIFE in cyan, the lives, the score, the GRENADES, shots in the middle. A grenade thrown (read in the game) flies from the panel and the middle blows up |
| The King of Dragons | `kod.json` | the green gauge, the level L, xlives, the experience EP as score | panels on a forest of huge old trees in the sun. LIFE in green, the lives, the experience as score, LEVEL, SWORD and SHIELD that go up (LEVEL UP!, SWORD UP!), slashes in the middle |
| Knights of the Round | `knights.json` | the red gauge, the level L, xlives, the half-timbered houses | panels on a village of half-timbered houses, the castle far off. LIFE in red, the lives, the score, LEVEL that goes up, slashes |
| Warriors of Fate | `wof.json` | the yellow-green gauge, xlives, the palisade and its banners | panels on a forest of ancient China and the palisade of a camp. LIFE yellow-green, the lives, the score, slashes |
| Dungeons & Dragons: Shadow over Mystara | `ddsom.json` | the green gauge, the sandstone cliffs | panels on a canyon of warm sandstone, a dark castle far off. LIFE in green, the score, slashes |
| Dungeons & Dragons: Tower of Doom | `ddtod.json` | the green gauge, the golden hills | panels on green hills in the golden light. LIFE in green, the score, the DAGGERS of player 1, slashes. A dagger thrown (read in the game) flies to the middle |
| Alien vs. Predator | `avsp.json` | the yellow gauge, the special gauge, xlives | panels on a ruined industrial city at dusk in a green haze. The name of the hero chosen in the game, LIFE in yellow, the SPECIAL gauge, the lives, the score, shots. When the special gauge empties (read in the game) the middle blows up |
| Armored Warriors | `armwar.json` | the blue gauge, xlives, the steel hangar and its hazard stripes | panels on the steel hangar of the war machines. The name of the machine chosen in the game, LIFE in blue, the lives, the score, shots |
| Battle Circuit | `batcir.json` | the yellow gauge, xlives, the stands of the arena | panels on an arena of the future at night. LIFE in yellow, the lives, the score, COIN and the money read in the game, punches |
| Final Fight Anniversary Edition, Final Fight EX (CPS2 hacks) | `ffightaec2.json`, `ffex2u.json` | the panel of Final Fight | the scene of Final Fight (nothing is known in their memory yet) |
| Tenchi wo Kurau II, CPS Changer | `wofch.json` | the panel of Warriors of Fate | the scene of Warriors of Fate, with its values (MAME cheat.dat, same addresses as Warriors of Fate) |
| 1944: The Loop Master | `1944.json` | the score or the title, the energy gauge and the bombs, the plane that flies and fires, BOMB!, POWER UP | the deep blue Pacific seen from the sky as in the game, huge battleships with their wooden decks and their wakes, an atoll now and then. Our silver twin-boom fighter against green fighters and bombers, warships below, its side fighters at its sides. A bomb spent is a salvo of missiles that clears the sky, a big WARNING announces the boss. The HUD in the spirit of the game, 1P in red and the score, POW (the energy) in yellow, and at the bottom left the bombs as B medals, the side fighters in stock in their frame with their number, the gold crystals picked up, 2P in pink. Read with MAME only, the side fighters and the crystals still to confirm in game, the WARNING and the score to find with RAM captures |
| 19XX: The War Against Destiny | `19xx.json` | the score or the title, the planes left and the bombs, the plane that flies and fires, the weapon picked up | high in the sky over the sea and its islands as in the game, white clouds flying by faster. The plane chosen in the game (the twin-boom fighter, the canard fighter or the twin-engine one), big four-engine bombers. 1P and the score, the planes left, the round bombs at the bottom left and the name of the plane |
| 1941: Counter Attack | `1941.json` | the score or the title, the VITAL gauge, the plane that flies and fires, the weapon picked up | a dark blue sea between two snowy rocky coasts as in the game. Our twin-boom fighter against the red-nosed fighters and the bombers, warships below. 1PLAYER and the score, the VITAL gauge in seven segments, the weapon picked up and its time |
| Varth: Operation Thunderstorm | `varth.json` | the score or the title, the planes left and the bombs, the plane that flies and fires, POWER UP, the weapon | a military base of teal plates seen from the sky as in the game, hangars and round pads. Our jet and its two guard pods turning around it, tanks on the taxiways. SCORE and the score, the planes left, the bombs, the weapon and the missiles of the pods |
| U.N. Squadron | `unsquad.json` | the score or the title, the stock of the special weapon, the plane that flies and fires, BOMB! | our jet over a desert canyon as in the game, mauve mesas, the towers of a refinery, tanks on the concrete, enemy helicopters. A special weapon fired blows up the screen. 1 PLAYER and the score, the special weapon read in the game and its stock at the bottom |
| Carrier Air Wing | `cawing.json` | the score or the title, the FUEL gauge, the plane that flies and fires, POWER UP, the weapon | our big navy jet high above a whole city seen at an angle as in the game, white clouds flying by, enemy jets. 1PLAYER and the score, LEVEL and the money, WEAPON, its ammo and the FUEL gauge at the bottom |
| Forgotten Worlds | `forgottn.json` | the score or the title, the VITAL gauge, the soldier who flies and fires, the weapon | our flying soldier and his gun module turning around him over a dead city as in the game, a huge green planet in the black sky, golden lizard warriors. The zenny picked up show, the weapon bought at the shop is named. 1P and the score, ZENNY, the VITAL gauge |
| Giga Wing | `gigawing.json` | the score or the title, the planes left and the bombs, the plane that flies and fires, POWER UP | an old steel fortress cut by rivers of glowing lava, seen from the sky as in the game, tanks on the rails. Our jet against the gunships, a bomb spent lights the golden barrier and clears the screen. 1P and the score, the planes and the bombs, the pilot chosen, REFLECT OK. The score of player 1 and the credits are known (learned on a cabinet), player 2's planes and bombs show when he plays |
| Progear | `progear.json` | the score or the title, the planes left and the bombs, the plane that flies and fires, POWER UP | our steam age fighter over an old European town as in the game, red roofs and a great stone aqueduct, the flying steam gunboats. P.1 and the score, the planes left and the bombs, the POWER gauge in eight steps, the plane chosen (Gambler or Militant) |
| Mars Matrix | `mmatrix.json` | the score or the title, the ships left, the ship that flies and fires, POWER UP | a rust-red mechanical base seen from the sky as in the game, round pads, pipes and warning stripes. Our mech fighter against orange war drones. 1P and the score, the ships left, LEVEL at the right |
| Dimahoo | `dimahoo.json` | the score or the title, the lives and the magic bombs, the beast that flies and fires | a magic sky of violet clouds seen from above as in the game, floating rocks. Our wizard on his flying beast against little dragons and big eye beasts, a magic bomb sends rings of light. PLAYER 1 and the score, the lives, the bombs as stars, the hero chosen |
| Eco Fighters | `ecofghtr.json` | the score or the title, the ships left, the pod that flies and fires, POWER UP, the weapon | our little ecological pod and its turning gun arm over a bright sea as in the game, ochre cliffs and their waterfall, polluting robots in green shells. 1P-SCORE and the score, ARM-LV and the ships left, the weapon of the arm |
| Mercs | `mercs.json` | the score or the title, the energy, the time, the mega crashes, the name of the weapon picked up, MISSION COMPLETE then the next mission, our mercenary who runs and fires | panels on a sandy track across the desert. ENERGY in green, the score, the MEGA CRASH, TIME, shots. A mega crash of either player (read in the game) flies from his panel and the middle blows up. The weapon each player holds is named next to his badge with its power-ups (ASSAULT RIFLE +2, FLAMETHROWER, SHOTGUN, GRENADE LAUNCHER, the names of the game's bezel), its name pops up when he picks it up and POWER UP! when a POW raises it. MISSION and its number under the logo, MISSION 1 COMPLETE! in the middle when the next one starts |
| Ghouls'n Ghosts | `ghouls.json` | the score or the title, the lives | panels on the place of the executions under the storm. The weapon the game says the knight holds (lance, dagger, torch, sword, axe) and his armour (silver, gold, ARMOUR LOST!), the lives, the score. Each point throws the weapon to the middle |
| Strider | `strider.json` | the score or the title, the lives | one panel on the city of the first stage at night and its golden domes (the players take turns). The lives, the score, the OPTION ROBOTS, slashes of light |
| Pang! 3 | `pang3.json` | the score or the title, the lives | panels on the painted wall of a temple in Egypt. The lives, the score. Big balloons bounce in the middle, the points read in the game burst one and it splits in two |
| Mighty! Pang | `mpang.json` | the score or the title, the lives, the time | panels on the highest mountain of the world under the falling snow. The lives, the score, TIME, the balloons of Pang! 3 |
| Super Puzzle Fighter II Turbo | `spf2t.json` | the score or the title, the two wells | the hall of the fights, its lit paper doors and its red lanterns, the two wells of gems in their golden frames. Pairs of gems of our own fall, a round gem bursts its colour and the counter gems fly across to the other well. No character is drawn, the names of the characters read in the game show in the middle. NEXT and SCORE |
| Mega Twins | `mtwins.json` | the score or the title, the health gauge, the lives | panels on the bright forest of the first stage. VITAL in blue, the lives, the score, slashes |
| Magic Sword: Heroic Fantasy | `msword.json` | the score or the title, the health gauge, the time | panels on a floor of the tower, its grey stones and its torches. VITAL, POWER that glows when full, the KEYS, the partner read in the game, FLOOR and its number, slashes |
| Willow | `willow.json` | the score or the title, the health gauge | one panel on the village of the first stage, its timber houses and red roofs (the players take turns). The hero read in the game, VITAL, the lives, the score, balls of magic |
| Nemo | `nemo.json` | the score or the title, the lives | panels on the palace of the land of dreams, its pale blue arches and its moon. The lives, the score, the SPECIAL ATTACKS in big, the stars of the wand. A special attack (read in the game) flies from the panel and lights up the middle |
| Three Wonders | `3wonders.json` | the score or the title, the lives | panels on the forest of Midnight Wanderers, its orange cliffs and its mushrooms. The shot the game says the elf holds, the lives, the score. Each point throws it to the middle |
| Dynasty Wars | `dynwar.json` | the score or the title, the health gauge | panels on the field of battle, its cliffs and its pines. VIT, the score, LEVEL that goes up, slashes of the halberd |
| Puzz Loop 2 | `pzloop2.json` | the score or the title, the balls | the sky of purple clouds and the carved track of the game. A chain of coloured balls rolls toward the hole, the launcher in the middle fires a ball into it, three of a colour burst and the chain closes up. BALLS and SCORE |
| Capcom Sports Club | `csclub.json` | the score or the title | the football match of the game in a stadium in the late afternoon, the full stands and the flags on the roof. Our own two teams pass the ball, shoot, the keeper dives. The flags of both teams at the top, as in the game |
| Quiz & Dragons: Capcom Quiz Game | `qad.json` | the score or the title, the lives, the question and its answers | the hall of the dungeon and a red dragon of our own painted on the wall, a knight and a wizard of our own, the green panel and its four answers. The score going up gives a big circle, a life lost a big cross. The questions are our own |
| Adventure Quiz Capcom World 2 | `cworld2j.json` | the score or the title, the lives, the question and its answers | the board of the adventure, its green lands, its blue sea and its path of squares, two little adventurers of our own, the blue panel and its four answers. The questions are our own |
| Quiz Tonosama no Yabou 2: Zenkoku-ban | `qtono2j.json` | the score or the title, the lives, the question and its answers | the castle of a warring lord against a red sky, its flames and its war banners, a lord and a ninja of our own, the question panel and its four answers. The lives read in the game decide right or wrong. The questions are our own |
| Quiz Nanairo Dreams: Nijiirochou no Kiseki | `qndream.json` | the score or the title, the lives, the question and its answers | a town park at dusk, its trees, its street lamps, its fountain and a pale rainbow, a girl and a boy of our own, the question panel. The questions are our own |
| Jyangokushi: Haoh no Saihai | `jyangoku.json` | the title, the tiles | the green felt in its red lacquer frame, the tiles with blue backs, a tile drawn, a tile thrown, and now and then a hand wins with RON or TSUMO. The points on the right |
| Janpai Puzzle Choukou | `choko.json` | the title, the tiles and the golden line | the tiles laid on the red silk in its golden frame. Two equal tiles leave when a line with two turns at most joins them, the golden line shows the way, the tiles are shuffled when no pair is left. PAIRS |
| Gulun.Pa! | `gulunpa.json` | the score or the title, two wells of blobs | the starry purple sky and its planets, two wells between golden pillars. Pairs of round little creatures of our own fall and pop four by four, the chains shine. NEXT beside each well, 1P and 2P in the middle |
| Pnickies | `pnickj.json` | the score or the title, the well, the angel and the imp | the pastel sky between heaven and the underworld, an angel of our own on the left and a little imp on the right, the well in its pink frame. The pairs fall and pop four by four. NEXT and the score beside the well |
| Frog Feast | `cps1frog.json` | the title, the pond, the frogs and the flies | the blue pond between two tall pines and its two lily pads. Two frogs of our own leap from their bank to their pad and catch the flies with their tongue. Each one's score on its wooden post, TIME in the middle, TIME UP at the end |
| Pokonyan! Balloon | `pokonyan.json` | the title, the balloon and the rising balloons | the savanna seen from the sky scrolls below, zebras and giraffes walk, our hot-air balloon and its little explorer drift above. The balloons of all colours rise and pop when the basket touches them |
| Magical Pumpkin: Puroland de Daibouken | `mpumpkin.json` | the title, the town and the pumpkin carriage | a fairy-tale town of round pastel houses and its pink castle scroll by, our pumpkin carriage rolls on the candy road by the river and picks up the stars that float ahead |
| Ganbare! Marine Kun | `ganbare.json` | the title, the sea, the fish and the sight | the open sea between its rocky stacks, the fish that leap out of the water. The red sight follows them, locks on and hits, the medals add up at the bottom |

### Coin screen (fighting games)

When nobody is playing, the Neo Geo fighting games wait for a coin, on the panel and on the HD screen. The coin drops only when the credits really go up, so the credits have to be known. MAME reads them for every Neo Geo game. With RetroArch, ArcadeDMD guesses them from the BIOS (see above), and `coin_buttons.bat` makes it see every coin (just below).

![START buttons once the coins are in, HD display](docs/images/hd_start_buttons.jpg)

- On the panel, a € coin floats above a coin slot, next to INSERT COIN. Insert a coin and it drops into the slot, +1 rises and the credit counter rolls. A moment later, PRESS START shows with a red button and the credits underneath. The title keeps scrolling at the top.
- On the HD screen, the game's logo sits between two coin doors, with a coin spinning above each one. Insert a coin and one of them turns on its edge and drops into its slot, with sparks, +1 and the counter rolling. Then the doors make way for the 1P and 2P START buttons and PRESS START.
- As long as no coin goes in, nothing drops. The game's own demo fights, behind, set off no effect on the HD screen.
- At the top of `config.json`, `"coin_symbol": "€"` is the symbol on the coins, those of Metal Slug's credits included. `"$"` and `"£"` work too, and `""` gives a plain coin.
- Your own INSERT COIN animation for the panel (a Pixelcade GIF, for example) goes in `sprites\insert_coin.gif` (or `.png`), 128 x 32. It replaces the coin screen as long as there is no credit, and the coin still drops when you insert one.
- In the `preview` section, `"coins": false` brings back the plain INSERT COIN on the HD screen.
- `demo_fight.bat` now starts on this screen. Two coins go in, START is pressed, then the fight begins. In a game file, `"demo": {"attract": false}` goes straight to the fight.

### Coin buttons (`coin_buttons.bat`)

RetroArch tells neither when a coin goes in nor through which coin slot. ArcadeDMD can read your two coin buttons and your two START buttons itself, on the controllers or the keyboard, at the same time as RetroArch and without taking them from it. It then sees every coin and its side, during a game too, and every player who presses START.

- Run `coin_buttons.bat`. Press the coin button on the left, then the one on the right, then player 1's START and player 2's START. The tool tells what it saw ("controller 1, button 9") and writes it into `config.json`, section `coin_buttons` (`left`, `right`, `start1`, `start2`). Press these buttons again to check, it tells which one. If ArcadeDMD is running, it picks up this setting by itself. Without START pressed, the START buttons already saved stay.
- On the HD screen, the coin drops in the slot on the side where you put it. Without this setting, it drops in player 1's slot when nobody plays, in the other player's slot during a game (the one who comes in), and in the slot of the player at the CONTINUE.
- An MVS gives 2 credits for a coin in its second slot, as long as its settings were not changed. ArcadeDMD counts the same way, 1 credit on the left and 2 on the right, and on the HD screen the right coin door says 2 CREDITS. If you change that setting in the MVS menu, put the same in the `coin_buttons` section of `config.json`, for example `"mvs_credits": [1, 1]`.
- While the RetroArch menu is open, the button moves in the menu, and ArcadeDMD counts no coin.
- If you plug your controllers into other USB ports, run `coin_buttons.bat` again. Windows may have changed their number.
- With MAME, the credits are already read in the game. The button then only gives the side of the coin on the HD screen.
- With RetroArch, a Capcom game that does not give its credits counts them from these buttons (Capcom CPS1, CPS2 and CPS3 games, Credits). A player who presses START with a credit then begins at once, the game shows from the select screen or the intro on instead of PRESS START. Player 2's START takes his credit too, a challenger in a fighting game included. START pressed without a credit, during a game or in RetroArch's menu counts nothing.
- Windows only.

### Learning the score

1. Launch the game in RetroArch and start playing. Score a few points.
2. Run `learn.bat`. It sees that RetroArch is running and switches to live mode.
3. Type the score shown on screen, for example `score=20600`, then press Enter. The game is paused while you are in this window.
4. Go back to the game (Alt+Tab), score more points, come back to the `learn.bat` window and type the new score.
5. Repeat three or four times, with a different score each time. Press Enter on an empty line to finish.
6. The tool finds the address and writes it to the game file (`games\mslug3.json` for example, or a new file for a Neo Geo game that has none). The score appears on the panel a few seconds later, without restarting the game.

Only type the missing values. Lives are already known, and learning them from the on-screen "1UP" would give a wrong address.

For player 2's score, play a two-player game and type both scores each time, for example `score=9400 score2=800`.

In Samurai Shodown and The Last Blade, the fighters move around in memory. Samurai Shodown II recreates each fighter somewhere else every round. It stores the score in the fighter and copies it into the new one. The old one keeps the last value for a while, then drops to 0. That is what used to fool the tool. It now prefers the score "inside the fighter" over a fixed address that happens to fall in the fighters' memory, and the panel follows it from round to round. Take your captures over two different rounds or two different fights. The tool reminds you at the start, and warns you if all the captures come from the same round. If an old address stops working, simply redo the learning. The new address replaces the old one in `games\` and in `learned\`.

When run while RetroArch is closed, `learn.bat` re-analyzes the game's latest captures with the values already typed, without asking for anything again.

The recognized names are `score`, `score2` (or `score_p2`), `credits`, `lives`, `lives_p2`, `bombs` and `ammo`. The French names `crédits`, `vies`, `vies2`, `bombes` and `munitions` work too. For a game that has no file yet, the tool creates one in `games\` with the generic scene.

A stage, a mission or a round (`stage=2`, `mission=3`, `round=2`) is often kept from 0 by the game, 0 for stage 1. Type the number shown on screen, the tool finds it anyway and saves it with `"add": 1`. A chain (`hits=4` while the game shows 4 HIT) is looked for as a short counter.

Whatever the tool finds is also copied to `learned\`. A new version of ArcadeDMD replaces the files in `games\`, but the engine automatically puts the learned addresses back at startup. To forget what was learned for a game, delete its file in `learned\`. An address that the game's file rules out (`not_learned`, where the game keeps something else that the tool mistakes for the value) is removed from `learned\` by itself, and the tool leaves it aside. In Metal Slug, the place the tool found holds the score of the last player who scored.

### Good to know

- A RetroArch game without a file in `games\` changes nothing on the Pixelcade (except with `"takeover": "all"`).
- In `config.json`, `retroarch` section, `"enabled": false` turns off the RetroArch monitoring.
- If the log says "RetroArch refuses to read the game memory", it is the core that does not expose it. The log says which core is loaded and what to do.

---

## 8. Adding a game or editing a scene

1. Copy `games\aburner2.json` under the game's short name, for example `games\outrun.json`.
2. Change `"match"` (`"system": ["outrun"]`), the title and the values.
3. Find the addresses with `learn.bat` (if there is no dedicated file, the tool creates it for you).
4. Edit the scene. The engine reloads the files on the fly, so there is no need to restart while you fine-tune.

Supported value formats

| `type` | Meaning |
|---|---|
| `u8` | one byte |
| `be` / `le` | binary over `bytes` bytes, big-endian or little-endian |
| `bcd` / `bcd_le` | BCD over `bytes` bytes (two digits per byte) |
| `digits` | one digit per byte (`digit_offset` 0x30 for ASCII) |

The common options are `mult` (for a score stored divided by 10, which is very common), `add`, `min`, `max`, `mask` and `shift`. `learn_ranges` limits the area captured for the learning tool. `hold_zero` (in seconds) keeps the last score on display when the value read briefly drops to 0 in the middle of a game, while the game recreates the fighter between two rounds.

For a value stored in an object that moves around in memory (the Samurai Shodown fighters at every round), `"ptr"` gives the address where the object's location is read (32 bits) and `"addr"` becomes the offset inside the object. `"ptr_range"` rules out a pointer that is not ready yet. `learn.bat` writes this kind of value by itself when the captures show that the value follows the object.

Some value names have a special role in the HD scenes. `stage`, `backdrop` and `mission` change the background (section 3), `p1_input` and `p2_input` are the Neo Geo BIOS stick and buttons (Metal Slug handgun shots, the ships of Blazing Star, Pulstar and Last Resort, the planes of the Aero Fighters, the hunters of Top Hunter, the arrow of Puzzle Bobble, the jester of Magical Drop III).

`"derived"` computes a value from other values, for example the character name. `"value"` takes a value that was read, `"pick"` chooses from a list according to `"at"`, and `"names"` turns a number into text. `"names"` can also hold one list per language, `{"en": [...], "fr": [...]}`, as in `games\wjammers.json`. See `games\samsho2.json` and `games\kof98.json`.

Scene elements

| `type` | Role | Main settings |
|---|---|---|
| `marquee` | scrolling text | `text` or `segments` (pieces in different colors), `font`, `y`, `speed`, `gap`, `color`, `accent_initials` |
| `text` | fixed text or value | `text` with `{score}`, `x`, `y`, `align`, `segments`, `flash` |
| `cycle` | alternates between several pages | `period`, `pages` |
| `bars` | grass or equalizer | `x`, `w`, `min`, `max`, `color`, `tip`, `flowers` |
| `waves` | hills scrolling in the background | `layers` (`y`, `amp`, `speed`, `color`, `edge`) |
| `mountains` | solid mountains and ground line (Vera style) | `peaks` (`[x, height]`), `floor`, `color`, `ground`, `speed` |
| `particles` | missiles and bursts when a value goes up | `rate`, `color`, `y`, `burst` |
| `anim` | an animation played once when a value changes (an explosion when the score goes up) | `image` (list, the first file found, `{game}` for the game), `on`, `change` (`up`, `down`, `any`), `ratio` (small or big gain), `x` and `y` (a number, `[start, end]`, or several `[start, end]` to pick from), `near` and `ahead` (ahead of a `ship`), `count`, `spread`, `delay`, `ms`, `black` |
| `events` | short events that take the panel for a moment, one at a time, as on a pinball (BOMB!, POWER UP, a life lost, GAME OVER) | `events`, a list. Each one has `on`, `change`, `step` (the size of the change), `from` and `to` (the values before and after), `when`, `text` (with `{lives}`...), `color`, `font` (its biggest size, it grows up to it), `y`, `icon` and `colors` (a small drawing at the left of the text), `icon_scale`, `anim` (animations played at the start, same keys as `anim`), `text_delay`, `ms`, `clear` (`false` keeps the scene behind), `priority` (a more important event replaces the one playing, a less important one waits) |
| `sprite` | animated sprite (PNG strip or GIF) | `image`, `frames`, `mode` (`pass`, `pingpong`, `fixed`), `dim` (brightness), `alpha`, `shoot` (fires when a value goes up) |
| `gauge` | health bar | `var`, `max`, `x`, `y`, `w`, `h`, `anchor` (anchored side), `color`, `low`, `back`, `border`, `bevel` (light edge at the bottom and on the right) |
| `clock` | clock | `format`, `font` |
| `icons` | a small drawing repeated for a value (lives as ships, power pips) | `var`, `pattern` (rows of characters, `.` for empty), `colors`, `max`, `gap`, `empty` (color of the slots left), `align`, `flash` |
| `counter` | a small drawing followed by a number (a plane and x3 for the lives) | `var`, `pattern`, `colors`, `font`, `color` (of the number), `prefix` (`x`), `align` (`left` from `x`, `right` up to `x`), `max` (above it nothing shows, a value the game has not set yet), `flash` |
| `ship` | the player's ship, which follows the stick and fires while button A is held (`p1_input`), or flies by itself | `image` (list, `{game}` for the game), `frames`, `fps`, `face` (`right`, or `left` for player 2 facing player 1), `area` (`[x0, y0, x1, y1]`), `input`, `speed`, `fire` (`color`, `speed`, `rate`, `len`), `shoot_on` (fires when the score goes up), `anchor` (so that an `anim` layer with `near` goes off ahead of it), `hit` and `unless` (an enemy blows up now and then as long as the score is not known) |
| `dot` | a disk whose color comes from a value (Puzzle Bobble bubbles), or always the first color without `var` (a moon) | `var`, `colors` (one color per value), `x`, `y`, `r`, `rim`, `shine` |
| `arrow` | an arrow that turns with a value (Neo Turf Masters wind) | `var`, `steps` (16, 0 points up then clockwise), `x`, `y`, `len`, `color`, `ring`, `flash` |
| `image`, `rect` | fixed image, rectangle | |

The available fonts are `4x6`, `5x8`, `6x10`, `6x13`, `7x14`, `7x14B`, `8x13B` and `9x15B`. The `y` of a text is the top of the capital letters. `when` shows an element only under a condition, for example `{"has": "credits"}` or `{"var": "mode", "eq": 12}`.

The `"demo"` section gives the starting values for the demos (`demo_neogeo.bat`, `python arcadedmd.py demo <game>`). `"attract": true` starts on the coin screen, then two coins and START. `"sim"` moves the game's own values, one entry per value, with `"cycle"` (a list taken in turn), `"count"` (`[min, max, step]`, back to the start at the end) or `"random"` (`[min, max]`), `"every"` (seconds, or `[min, max]`) and `"start"` (first change). See `games\wjammers.json`.

---

## 9. DOFLinx bridge (optional)

ArcadeDMD can pose as DOF2DMD. DOFLinx then sends it the score and credits of every game it knows, with no address to look for.

1. In `config.json`, set `"enabled": true` in the `doflinx_bridge` section. It listens on port 8081, leaving 8080 to pixelweb.
2. DOFLinx reads the address from DOF2DMD's `settings.ini` (`url_prefix`). Set it to `http://127.0.0.1:8081`.
3. Do not run DOF2DMD at the same time, since the two cannot listen on the same port. When ArcadeDMD answers, DOFLinx no longer tries to start DOF2DMD.

The two sources complement each other. For After Burner II, the high score comes from the plugin and the score from DOFLinx.


---

## 10. Troubleshooting

- **Nothing changes on the Pixelcade with RetroArch.** Check that "Network Commands" is turned on in RetroArch and that the log says "RetroArch 1.19.x detected (network commands active)". The game must have its file in `games\`.
- **With RetroArch, the scene shows but without values.** The core most likely does not expose its memory (FB Alpha 2012, for example). Run `test_retroarch.bat` during the game. It tells you which core is running and which one to use (see "The right core", section 7).
- **"Python was not found".** The Microsoft Store `python` shortcut does not count, because it does not launch anything. Run `install.bat` again and it offers to install Python 3.13. The .bat files also find a Python that is installed but not in the PATH.
- **ArcadeDMD does not appear in MAME's Tab menu.** MAME may be too old (0.227 or newer is required, and `install.bat` shows the version). Otherwise the plugin is disabled (see "Checking the plugin in MAME").
- **Nothing shows during a game.** Look at `runtime\arcadedmd.log` and check that `runtime\events.jsonl` grows during the game. If it does not, the `root` path in `MAME\plugins\arcadedmd\settings.json` does not point to the ArcadeDMD folder.
- **"ZeDMD: LED panel not found".** Check the cable (it must carry data), the native USB port of the ESP32-S3, and that no other software is using the panel (DOF2DMD, VPX, dmdext, or the ArcadeDMD engine already running in the background). The automatic search stops after three attempts. Once the panel has been found, its port is remembered and only that port is retried.
- **RetroShooter light guns or other serial devices.** The search for a ZeDMD panel queries the COM ports (never the Pixelcade's, and none at all if the ZeDMD output is off). To never touch the guns, set the panel's port in `config.json` (`"device": "COM5"`) or exclude the guns' ports (`"ignore_devices": ["COM3", "COM4"]`).
- **Black panel after sleep mode or after unplugging.** Restart ArcadeDMD, because libzedmd does not reconnect on its own.
- **Swapped colors, ghost lines.** Set the RGB order and the "panel driver" in the ZeDMD menu (or with ZeDMD_Updater2).
- **Choppy animation on the panel.** Raise "USB packet size" and "min refresh" in the ZeDMD menu.
- **No virtual LED window.** pygame-ce must be installed (`py -m pip install pygame-ce`).
- **`test_panel.bat` says the engine is already running.** The automatic start is holding the panel. End `pythonw.exe` in Task Manager, or test directly with a game.
- **The engine stops on its own.** The error is written to `runtime\arcadedmd.log`.
- **"Pixelcade: port not found".** Set the port in `config.json` (`ports.bat` helps you find it). ArcadeDMD does not probe the other COM ports, so as not to disturb light guns.
- **"pixelweb does not stop".** Close pixelweb by hand (its icon in the taskbar) and check `pixelweb_url` (default `http://127.0.0.1:8080`).
- **pixelweb does not come back after a game.** Its path is saved in `runtime\pixelweb_path.txt` the first time it is stopped. Otherwise, fill in `pixelweb_exe` in `config.json`.
- **Black Pixelcade during a game.** Look at the log. If pixelweb was stopped but the board does not respond, unplug and replug the Pixelcade, then run `test_pixelcade.bat` again.

---

## 11. Text files for OBS

ArcadeDMD writes the values of the current game to the `obs\` folder, one file per value. Each file is updated as soon as the value changes, and is emptied outside games. It works with MAME, Arcade64 and RetroArch.

| File | Content |
|---|---|
| `game.txt` | game title |
| `score_p1.txt`, `score_p2.txt` | each player's score |
| `credits.txt` | credits (MAME and Arcade64) |
| `fighter_p1.txt`, `fighter_p2.txt` | character currently fighting, when known |
| `streak_p1.txt`, `streak_p2.txt` | wins in a row in VS matches (King of Fighters, once learned) |
| `vs_p1.txt`, `vs_p2.txt` | "BEAT BY 02" or "CHALLENGER", as at the top of the game screen |
| `best_streak.txt` | best streak of the current game, for example "BEAT BY 05 \| P2 RUGAL \| 26/10/2026" |
| `vs_history.txt` | one line per VS match won, with the date, the game, the winner and their streak |
| `records.json` | the best streak of each game, kept from one session to the next |

In OBS, add a Text (GDI+) source, tick "Read from file" and choose the file. The texts are the same in every language. "P2 RUGAL > P1 KIM" means that P2 beat P1.

To turn this off, set `"enabled": false` in the `textfiles` section of `config.json`. `"folder"` picks another folder, and `"history": false` turns off the history.

## Licenses and credits

ArcadeDMD is © 2026 Byoyoyo, released under the MIT license (`LICENSE` file). You may use, modify and share it, as long as the copyright notice and the license stay with it. The bitmap fonts come from the X11 "misc-fixed" fonts (public domain). The HD fonts are Inter (The Inter Project Authors) and Black Ops One (The Black-Ops Project Authors), both under the SIL Open Font License, see the `fonts` folder. The sprites, the HD backgrounds and the effects are drawn by the program or for it, no image comes from a game. ZeDMD (GPLv2 firmware) and libzedmd (GPLv3) are downloaded separately from their official repositories https://github.com/PPUC. Game names are used only to identify the games. The addresses come from the community cheat databases (FinalBurn Neo, MAME 2003-Plus), peon2's training scripts and the Sonic disassemblies, with thanks to their authors.

Byoyoyo had wanted to build ArcadeDMD for a long time, and started it after his exchanges with Vera AI. Thanks to Vera AI for those exchanges.
