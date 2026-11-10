With MAME, a small Lua plugin reads the values from the game's RAM and hands them to ArcadeDMD. It only reads. It changes neither the game, nor the controls, nor MAME's settings.

## Installing the plugin

`install.bat` copies the plugin into MAME's `plugins\arcadedmd` folder. MAME 0.227 or newer is needed, the installer shows your version. MAME loads the plugins of its `plugins` folder by itself, `mame.ini` and `plugin.ini` are not touched.

The frontend (LaunchBox, BigBox, HyperSpin...) needs no setting. MAME loads the plugin every time it starts.

## Checking the plugin

Start a game, press Tab, then go to "Plugin Options". You should see **ArcadeDMD** with the detected game and the values read live.

If it does not appear, check in MAME's Plugins menu that it is enabled, or add the line `arcadedmd 1` to `plugin.ini` (in the MAME folder or in `ini\`). If it appears but nothing shows on the marquee, the `root` path in `MAME\plugins\arcadedmd\settings.json` must point to the ArcadeDMD folder (see [[Troubleshooting]]).

## What MAME gives that RetroArch does not

- The credits of every Neo Geo game. They live in the MVS backup memory, which MAME reads and RetroArch's FinalBurn Neo core does not share.
- Any MAME game. With `"takeover": "all"`, a game without a file of its own gets the generic scene (its title, and its Pixelcade marquee behind on a Pixelcade).

## Learning a game under MAME

For a game whose score or credits nobody documented, the plugin takes RAM captures. Press **Right Ctrl + D** when the score is stable (or Tab, Plugin Options, ArcadeDMD, the RAM capture entry), at three or four moments, then quit MAME and run `learn.bat`. See [[Learning Addresses]] and the example of After Burner II in [[Other Games]].

## With DOFLinx

MAME runs several plugins at once. The DOFLinx and ArcadeDMD plugins do not get in each other's way, and ArcadeDMD does not touch the `output` setting of `mame.ini` that DOFLinx needs. See [[OBS and DOFLinx]].

## Turning it off

Add the line `arcadedmd 0` to MAME's `plugin.ini`, or delete the `plugins\arcadedmd` folder.
