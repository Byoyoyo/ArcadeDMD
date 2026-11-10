Everything ArcadeDMD does is written to `runtime\arcadedmd.log`. Look there first, it usually says what is wrong and what to do.

## Installation

- **"Python was not found".** The Microsoft Store `python` shortcut does not count, it launches nothing. Run `install.bat` again, it offers to install Python 3.13. The .bat files also find a Python that is installed but not in the PATH.
- **Windows asks for confirmation on every .bat file.** Right-click the zip before extracting it, Properties, tick "Unblock".
- **No virtual LED window.** pygame-ce must be installed (`py -m pip install pygame-ce`).

## MAME

- **ArcadeDMD does not appear in MAME's Tab menu.** MAME may be too old (0.227 or newer, `install.bat` shows the version). Otherwise the plugin is disabled, see [[MAME]].
- **Nothing shows during a game.** Check that `runtime\events.jsonl` grows during the game. If it does not, the `root` path in `MAME\plugins\arcadedmd\settings.json` does not point to the ArcadeDMD folder.

## RetroArch

- **Nothing changes with RetroArch.** Check that "Network Commands" is on in RetroArch and that the log says "RetroArch 1.19.x detected (network commands active)". The game must have its file in `games\`.
- **The scene shows but without values.** The core most likely does not share its memory (FB Alpha 2012, for example). Run `test_retroarch.bat` during the game, it says which core runs and which one to use. See [[RetroArch]].
- **"RetroArch refuses to read the game memory".** The same, it is the core. The log says which one is loaded.
- **A coin does not drop.** Run `coin_buttons.bat`. If it still does not, run `test_coins.bat` while you insert a coin and send its result.

## LCD marquee

- **The scene is on the wrong screen, or cut.** Run `screen_setup.bat` again, or set `x`, `y`, `width` and `height` in the `preview` section from Settings, Display. See [[HD Marquee]].
- **No logo.** Set the LaunchBox folder, `"launchbox": "E:\\LaunchBox"` in the `preview` section.

## Pixelcade

- **"Pixelcade: port not found".** Set the port in `config.json` (`ports.bat` finds it). ArcadeDMD does not probe the other COM ports, so as not to disturb light guns.
- **"pixelweb does not stop".** Close pixelweb by hand (its icon in the taskbar) and check `pixelweb_url` (default `http://127.0.0.1:8080`).
- **pixelweb does not come back after a game.** Its path is saved in `runtime\pixelweb_path.txt` the first time it is stopped. Otherwise fill in `pixelweb_exe`.
- **Black Pixelcade during a game.** If pixelweb was stopped but the board does not answer, unplug and replug the Pixelcade, then run `test_pixelcade.bat` again.
- **Green and blue swapped.** Run `test_pixelcade.bat` and answer n.

## ZeDMD

- **"ZeDMD: LED panel not found".** Check the cable (it must carry data), the native USB port of the ESP32-S3, and that no other software uses the panel (DOF2DMD, VPX, dmdext, or ArcadeDMD already running in the background). The search stops after three attempts. Once found, the panel's port is remembered.
- **Light guns or other serial devices.** Set the panel's port (`"device": "COM5"`) or exclude theirs (`"ignore_devices": ["COM3", "COM4"]`).
- **Black panel after sleep or after unplugging.** Restart ArcadeDMD, libzedmd does not reconnect on its own.
- **Swapped colours, ghost lines.** Set the RGB order and the "panel driver" in the ZeDMD menu (or with ZeDMD_Updater2).
- **Choppy animation.** Raise "USB packet size" and "min refresh" in the ZeDMD menu.
- **`test_panel.bat` says the engine is already running.** The automatic start holds the panel. End `pythonw.exe` in Task Manager, or test directly with a game.

## The engine

- **It stops on its own.** The error is written to `runtime\arcadedmd.log`.

## Asking for help

Open an [issue](https://github.com/Byoyoyo/ArcadeDMD/issues) with `runtime\arcadedmd.log`. For a game that misbehaves, add its recording (see [[Recording a Game]]).
