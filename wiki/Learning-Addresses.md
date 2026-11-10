Many games already know where their values live, from the cheat databases, RetroAchievements or a game recorded on a cabinet. When a value is missing (the score, very often), `learn.bat` finds it from a few readings of the game, with the values you see on screen.

## With RetroArch, live

1. Launch the game in RetroArch and play. Score a few points.
2. Run `learn.bat`. It sees that RetroArch is running and switches to live mode.
3. Type the score shown on screen, for example `score=20600`, then Enter. The game is paused while you are in this window.
4. Go back to the game (Alt+Tab), score more points, come back and type the new score.
5. Repeat three or four times, a different score each time. Enter on an empty line finishes.
6. The tool finds the address and writes it to the game file (`games\mslug3.json`, or a new file for a game that has none). The score shows on the marquee a few seconds later, without restarting the game.

Only type the missing values. A value already known learned again from what the screen shows could give a wrong address.

## With MAME, from captures

Press **Right Ctrl + D** at three or four moments during the game (or Tab, Plugin Options, ArcadeDMD, RAM capture), quit MAME, then run `learn.bat`. For each capture, it opens the screenshot and asks for the values. The example of After Burner II is in [[Other Games]].

When run while RetroArch is closed, `learn.bat` analyses the game's latest captures again with the values already typed.

## What to type

| Name | Value |
|---|---|
| `score`, `score2` (or `score_p2`) | each player's score. For player 2, play a two-player game and type both, `score=9400 score2=800` |
| `credits` | type it after a coin and once more after START (one credit less), so that the tool tells the credits from the coins put in |
| `lives`, `lives_p2`, `bombs`, `ammo` | lives, bombs, ammo |
| `wins`, `wins2` | the matches won in VS |
| `stage`, `mission`, `round` | type the number shown on screen, the tool finds it even when the game counts from 0 |
| `hits` | a chain (`hits=4` while the game shows 4 HIT) |
| `perfect` | something on or off, typed 1 or 0 |

The French names `crédits`, `vies`, `vies2`, `bombes`, `munitions`, `victoires`, `victoires2` work too. A name that neither the game file nor the scenes know is reported with the closest one ("scroe2 is not a value of this game, did you mean score2?").

## The VS counters of The King of Fighters (BEAT BY)

They are in no cheat database and are learned once per game.

1. Launch the game in RetroArch and play as player 1.
2. Bring player 2 in with a coin and START. You can hold both sticks yourself.
3. Run `learn.bat`.
4. After each match, when BEAT BY shows at the top of the game screen, type both counters, `beat=1 beat2=0`. Enter 0 for the side marked CHALLENGER.
5. Play five or six matches, one side winning then the other.
6. Enter on an empty line. The tool writes `beat` and `beat_p2` to the game file.

## Fighters that move around in memory

In Samurai Shodown and The Last Blade, the fighters move around in memory at every round. The tool follows the value inside the fighter. Take your captures over two different rounds or two different fights. It reminds you at the start.

## Where the learned addresses go

Whatever the tool finds is also copied to `learned\`. A new version of ArcadeDMD replaces the files of `games\`, and the engine puts the learned addresses back at startup. To forget what was learned for a game, delete its file in `learned\`.

If the tool finds nothing, zip the game's folder from `runtime\learn\` and attach it to a GitHub [issue](https://github.com/Byoyoyo/ArcadeDMD/issues).
