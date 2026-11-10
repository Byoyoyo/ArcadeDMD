Everything ArcadeDMD shows is drawn by the program. No image comes from the games, apart from your LaunchBox Clear Logo when a game starts. You can swap some drawings for pictures of your own, by dropping them in the `sprites\` folder of ArcadeDMD.

Your pictures stay yours. They are never in the zip of a new version, nor in the repository, and an update leaves them in place.

## How a picture is used

- PNG works everywhere. `.gif`, `.jpg` and `.webp` work too for the Metal Slug pictures.
- A plain background around the drawing is made transparent and the empty margins are cut, so a picture cut out roughly is fine.
- `runtime\arcadedmd.log` says which picture is used, or where one would be read from.

## On the HD screen

| Game | Where | Names |
|---|---|---|
| Metal Slug, all six games | `sprites\mslug\<name>.png` | vehicles `tank`, `camel`, `slugnoid`, `flyer`, `copter`, `mariner`, `drill`, `astro`, and `elephant`, `ostrich`, `bradley`, `mobile`, `gunner`, `claw`, `walker`, `armor`, seen from the side, gun to the right |
| Metal Slug, all six games | `sprites\mslug\<name>.png` | soldiers `marco`, `tarma`, `eri`, `fio`, `trevor`, `nadia`, a small portrait beside the soldier's name |
| One Metal Slug game only | `sprites\mslug2\<name>.png`, `sprites\mslug3\<name>.png`... | the same names, for that game alone |
| Windjammers | `sprites\wjammers\<name>.png` | the six players `scott`, `costa`, `wessel`, `yoo`, `biaggi`, `mita`, on the court where the game puts them |

The French names (`char.png`, `chameau.png`) and the older `sprites\mslug_tank_hd.png` for the tank still work. See [[Metal Slug]].

## On the LED panel

| What | File |
|---|---|
| The INSERT COIN screen | `sprites\insert_coin.gif` (or `.png`), 128 x 32. A Pixelcade GIF, for example. It replaces the coin screen as long as there is no credit, and the coin still drops when you insert one |
| The little Metal Slug tank | `sprites\mslug_tank.gif`, or a `mslug_tank.png` strip of 3 frames, 5 pixels high at most, cannon to the right |
| The runner of Sonic | `sprites\sonic.gif`, or a `sonic.png` strip of 6 frames, `sonic2.gif` for Sonic 2. Adjust `"y"` in the game file to its height |

## The game's logo

The logo shown when a game starts is your LaunchBox Clear Logo, found by itself (see [[HD Marquee]]). A game without one gets its title in metallic lettering on the HD screen.
