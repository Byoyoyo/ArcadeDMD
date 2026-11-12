## What you need

- Windows.
- Python 3.12 or newer. If it is missing, `install.bat` offers to install Python 3.13 from python.org.
- For MAME games, MAME 0.227 or newer. The installer shows your version.
- For RetroArch games, RetroArch 1.19 or newer (see [[RetroArch]]).
- A display for the marquee. An LCD screen that Windows sees as a display (see [[HD Marquee]]), a [[Pixelcade LED]] or a ZeDMD panel (see [[ZeDMD and Hardware]]).

## Install

1. Download the zip of the latest version from the [Releases](https://github.com/Byoyoyo/ArcadeDMD/releases/latest) page.
2. Before extracting it, right-click the zip, choose Properties, tick "Unblock", then OK. Windows will then stop asking for confirmation on every .bat file.
3. Extract the `ArcadeDMD` folder to a path with no accented characters, ideally `C:\ArcadeDMD`. MAME cannot open folders with accented characters.
4. Run `install.bat`. It installs Pillow, pyserial and pygame-ce, copies the plugin into MAME, sets up the Pixelcade and offers to start ArcadeDMD automatically with Windows. It only downloads libzedmd (the ZeDMD driver) if you say you have a ZeDMD panel. If you only use RetroArch, press Enter at the MAME question.
5. With an LCD marquee, run `screen_setup.bat` (the installer offers it too). It finds the marquee screen and sets everything in `config.json`. Since 1.37, the Screens tab of ArcadeDMD's window does the same with the list of screens Windows sees (see [[Usage]]).

## What the installation changes

- The `C:\ArcadeDMD` folder. Settings, the log and the captures stay inside it.
- In MAME, a new `plugins\arcadedmd` folder with three small files. Nothing else in MAME. `mame.ini` and `plugin.ini` are not modified, since MAME loads the plugins of its `plugins` folder by itself.
- An `ArcadeDMD.bat` file in the Windows Startup folder, only if you accept the automatic start.
- Three libraries added to Python (Pillow, pyserial, pygame-ce).
- With a Pixelcade, during games that have a file in `games\`, ArcadeDMD stops pixelweb and restarts it when the game ends. For other games, nothing changes.

The plugin only reads the game memory. It changes neither the game, nor the controls, nor MAME's settings.

## First try without a game

The demos show the scenes with simulated values, on the marquee screen or the panel, without MAME or RetroArch.

| File | What it shows |
|---|---|
| `demo_fight.bat` | The King of Fighters '98, from the coin screen to the fight |
| `demo_neogeo.bat` | a Neo Geo game done one by one, to choose in a list |
| `demo_capcom.bat` | a Capcom CPS1, CPS2 or CPS3 game |
| `demo_cave.bat` | a Cave game (DoDonPachi, Ketsui, Espgaluda, Mushihime-sama, Deathsmiles...) |
| `demo_afterburner.bat`, `demo_sonic.bat` | After Burner II, Sonic |

## Updating

Extract the new version over the old one. `config.json` is never overwritten, it was created from `config.default.json` at the first install. The addresses found with `learn.bat` are kept in `learned\` and put back at startup. Your own pictures in `sprites\` stay.

## Uninstalling

Delete the `plugins\arcadedmd` folder from MAME, the `ArcadeDMD.bat` file from the Startup folder (type `shell:startup` in Win+R to open it), then the `C:\ArcadeDMD` folder. To only turn the plugin off, add the line `arcadedmd 0` to MAME's `plugin.ini`.

Next, [[Usage]].
