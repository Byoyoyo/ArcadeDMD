## Running ArcadeDMD

Launch `run.bat`, or let the automatic start do it when Windows starts. Then start your games as usual, from LaunchBox, BigBox, HyperSpin or directly in MAME or RetroArch. The frontend needs no setting.

`run.bat` shows the console. The automatic start runs the same engine without a window. Everything it does is written to `runtime\arcadedmd.log`.

## What happens during a game

1. The game starts. ArcadeDMD recognises it (its MAME name, or the content RetroArch loaded) and takes the marquee if the game has a file in `games\`. On an LCD marquee, its window comes in front of the BigBox marquee without taking the focus from the game.
2. The game's logo comes first, your LaunchBox Clear Logo, big then gliding to its place. A game without a Clear Logo gets its title in metallic lettering on the HD screen.
3. The scene of the game follows the game live. The values read in the game's memory drive it.
4. You quit the game. The marquee goes back to the frontend at once (the Pixelcade goes back to pixelweb).

With `"mode": "always"` (see [[Configuration]]) the marquee stays with ArcadeDMD all the time, black outside games.

## When nobody plays

The fighting games wait for a coin. The game's logo sits between two coin doors, a coin spinning above each one. Insert a coin and it drops into its slot with +1 and the credits rolling, then PRESS START shows in big while the doors and their coins stay. The game's own demo, behind, sets off nothing.

![The coin screen on the HD marquee](images/coin_screen_hd.gif)

![The coin screen on the LED panel](images/coin_screen_led.gif)

With RetroArch, run `coin_buttons.bat` once so that ArcadeDMD sees every coin and every START (see [[RetroArch]]). With MAME, the credits are read in the game.

## Tools in the folder

| File | Purpose |
|---|---|
| `install.bat` | installs everything |
| `run.bat` | starts the engine with the console visible |
| `screen_setup.bat` | puts the scene on an LCD marquee, as virtual LEDs or in smooth HD |
| `demo_fight.bat`, `demo_neogeo.bat`, `demo_capcom.bat`, `demo_cave.bat`, `demo_afterburner.bat`, `demo_sonic.bat` | the scenes with simulated values |
| `learn.bat` | finds a missing address (score, credits...), see [[Learning Addresses]] |
| `coin_buttons.bat` | shows ArcadeDMD your coin and START buttons (RetroArch) |
| `test_retroarch.bat` | checks RetroArch, the loaded core and the memory reading |
| `test_coins.bat` | writes down what the Neo Geo BIOS does when a coin goes in, to send if a coin does not drop |
| `test_pixelcade.bat` | test pattern on the Pixelcade |
| `test_panel.bat` | test pattern on a ZeDMD panel |
| `ports.bat` | lists the COM ports, to find the Pixelcade's |

## Language

Texts are in English, or in French when Windows is in French. `"language"` at the top of `config.json` chooses (`"auto"`, `"en"`, `"fr"`).

## Pause

When the game is paused, PAUSE blinks on the LED panel (`"show_pause": false` turns it off).
