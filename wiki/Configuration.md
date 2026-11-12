All the settings are in `config.json`, in the ArcadeDMD folder. The installer creates it from `config.default.json`, and a new version never overwrites it. ArcadeDMD notices by itself when `config.json` changes and picks up the new settings.

Edit it with Notepad. A path takes double backslashes (`"E:\\LaunchBox"`).

## Top level

| Setting | Default | Effect |
|---|---|---|
| `language` | `"auto"` | `"auto"` follows the Windows language, `"en"` English, `"fr"` French |
| `fps` | `50` | frames per second of the engine |
| `coin_symbol` | `"€"` | the symbol struck on the coins (`"$"`, `"£"`, `""` for a plain coin) |
| `capture` | `"all"` | records the values read during each game (`"all"`, `"fights"`, `"off"`), see [[Recording a Game]] |
| `show_pause` | `true` | PAUSE blinks on the LED panel while the game is paused |
| `idle` | `{"show": false}` | `"show": true` brings back the old idle screen (the time and `"text"`) on a ZeDMD panel outside games |
| `intro` | see below | the game's logo when a game starts |
| `frontend` | `{"use": "auto", "retrobat": ""}` | where the game logos come from. `"auto"` takes LaunchBox, else RetroBat. `"launchbox"`, `"retrobat"` or `"none"` force one. `"retrobat"` is RetroBat's folder when it is not found on its own (Frontend tab of the window) |
| `window` | `{"enabled": true}` | `false` turns off the window and the icon near the clock |

### `intro`

| Setting | Default | Effect |
|---|---|---|
| `logo` | `true` | `false` turns the logo off, on the panel and on the HD screen |
| `seconds` | `2.6` | how long it lasts, 1 to 10 seconds |
| `launchbox` | `""` | the LaunchBox folder, when it is not found by itself |

## `outputs.preview`, the LCD marquee

| Setting | Default | Effect |
|---|---|---|
| `enabled` | `false` | draws the scene on a screen (`screen_setup.bat` sets it) |
| `x`, `y`, `width`, `height` | `0`, `1080`, `1920`, `470` | where the screen sits on the Windows desktop and its size (Settings, Display) |
| `borderless`, `topmost` | `true` | a window with no border, kept above the others while shown |
| `mode` | `"games"` | `"games"` shows the window during known games only and leaves the screen to the frontend the rest of the time, `"always"` keeps it, black outside games |
| `takeover` | `"known"` | `"known"` for games that have a file in `games\`, `"all"` for every MAME game with the generic scene |
| `style` | `"led"` | `"led"` round LEDs, `"pixel"` square pixels, `"hd"` smooth HD |
| `hd` | `"auto"` | LED grid of the virtual LEDs, `"auto"`, `1` (128 x 32), `2` or `4` (finer) |
| `launchbox` | `""` | the LaunchBox folder for the Clear Logos, when it is not found by itself |
| `coins` | `true` | `false` brings back the plain INSERT COIN on the HD screen |
| `dim` | `30` | how much the animated backdrops are darkened, 0 to 80 percent |
| `dim_fight` | `55` | the same for the fighting games' stages |
| `stage_style` | `"cartoon"` | `"flat"` gives back the look of the King of Fighters '98 stages of 1.32 |

See [[HD Marquee]].

## `outputs.pixelcade`

| Setting | Default | Effect |
|---|---|---|
| `enabled` | `false` | drives the Pixelcade LED |
| `device` | `""` | its COM port (`ports.bat` finds it) |
| `color_order` | `"auto"` | set by `test_pixelcade.bat` when green and blue are swapped |
| `mode`, `takeover` | `"games"`, `"known"` | as for the preview |
| `max_fps` | `30` | frames per second sent to the panel |
| `gamma` | `2.2` | makes the panel look like the preview, `1.0` sends the colours as they are |
| `pixelweb_url` | `"http://127.0.0.1:8080"` | pixelweb's address |
| `pixelweb_exe` | `""` | path to pixelweb.exe, usually found by itself |
| `art_dir` | `""` | the Pixelcade folder, to reuse its marquees behind the generic scene |

See [[Pixelcade LED]].

## `outputs.zedmd`

| Setting | Default | Effect |
|---|---|---|
| `enabled` | `false` | drives a ZeDMD panel |
| `dll` | `"libzedmd/zedmd64.dll"` | the libzedmd driver |
| `device` | `""` | the panel's COM port, found by itself when empty |
| `ignore_devices` | `[]` | COM ports never probed (light guns, for example) |
| `wifi_ip` | `""` | the address of a ZeDMD reached over Wi-Fi |
| `brightness` | `null` | 0 to 15 sets the panel's brightness, `null` keeps the one of its menu |

See [[ZeDMD and Hardware]].

## `retroarch`

| Setting | Default | Effect |
|---|---|---|
| `enabled` | `true` | watches RetroArch |
| `host`, `port` | `"127.0.0.1"`, `55355` | RetroArch's network commands |
| `poll_ms` | `100` | how often the values are read |
| `ram_dump` | `{"enabled": true, "every": 0.25}` | records the game's whole memory, see [[Recording a Game]] |
| `screenshots` | `{"enabled": true, "every": 2.0, "dir": ""}` | asks RetroArch for screenshots during a game, `dir` is RetroArch's screenshot folder |

See [[RetroArch]].

## `coin_buttons`

Written by `coin_buttons.bat`. `left`, `right`, `start1` and `start2` are your coin and START buttons. `mvs_credits` is the credits each coin slot gives, `[1, 2]` as an MVS does by default.

## `textfiles` and `doflinx_bridge`

See [[OBS and DOFLinx]].
