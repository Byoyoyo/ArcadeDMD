## After Burner II

The high score location is public (the high score table at `0xFF846E`, the one `hiscore.dat` uses). The score and credits are documented nowhere, hence the learning tool. Allow five minutes, with MAME.

1. Start After Burner II.
2. Insert a coin, wait a little, insert a second one. The credits change.
3. Play. When the score is stable (not during a bonus count), press **Right Ctrl + D**. A message on screen confirms the capture. Tab, Plugin Options, ArcadeDMD, the RAM capture entry does the same.
4. Capture again at three or four moments, with different scores and credits, one of them just after START (one credit less).
5. Quit MAME and run `learn.bat`. For each capture, the tool opens the screenshot and asks for the values, for example `score=16060 credits=3`.
6. It finds the address in all the usual formats and writes it to `games\aburner2.json`.

Start the game again. The score and credits now show on the marquee and in the plugin's Tab menu.

If several areas are found, one more capture decides. If nothing is found, delete the `learn_ranges` line in `games\aburner2.json` and the `runtime\learn\aburner2` folder, then capture again. The tool then searches all the RAM the main CPU sees.

DOFLinx can also give the score and credits of After Burner II and of more than 2,000 games (see [[OBS and DOFLinx]]).

`demo_afterburner.bat` shows the scene with simulated values.

## Sonic 1 and Sonic 2

The addresses come from the community disassemblies of Sonic 1 and Sonic 2 (score, rings, lives, zone), the same in both games.

- In MAME, the Mega Drive / Genesis (`genesis` or `megadriv` drivers, the Sonic cartridge from the software list or a ROM file of that name), and the Mega Play and Mega-Tech arcade versions (`mp_sonic`, `mt_sonic`, `mp_soni2`, `mt_soni2`).
- In RetroArch, the Genesis Plus GX core, or PicoDrive (see [[RetroArch]]).

`games\sonic.json` is used for Sonic 1 and `games\sonic2.json` for Sonic 2. The little character running on the grass is a generic ring. Your own animated sprite goes in `sprites\sonic.gif` (or a `sonic.png` strip of 6 frames), `sonic2.gif` for Sonic 2. Adjust `"y"` in the game file to its height.

`demo_sonic.bat` shows the scene with simulated values.

## Any other game

A MAME game without a file gets the generic scene with `"takeover": "all"`. To give it its own, see [[Game Files]] and [[Learning Addresses]].
