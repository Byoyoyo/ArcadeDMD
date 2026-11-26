Since 1.33, ArcadeDMD records every game you play. One game, played normally, is enough to tune a game without the cabinet. Its file is fixed from the recording, the game is replayed in the HD scene to check every moment, and the recording is kept as a test so that nothing breaks later.

## What is recorded

1. **The values read**, with their time, to `runtime\captures\<game>-<date>.log`. A few hundred KB for a match, with MAME as with RetroArch. Every coin press is in it too.
2. **The whole memory of the game** (RetroArch), four times a second as compressed differences, to `runtime\captures\<game>-<date>.ram`. A few MB for ten minutes. It shows where the game keeps what is not read yet, the life of a boss, the kind of a vehicle.
3. **Screenshots** asked of RetroArch (its `SCREENSHOT` network command) at the first read, every two seconds while somebody plays, and at once when a life, a mission, a vehicle or one of the game's flags changes. They land in RetroArch's screenshot folder, the time in their name.
4. **The marker.** A coin button held a good second during the game writes `marker n` in the capture with its time, takes a screenshot and adds a line to the log. Use it to say "here" when something to look at happens.

## Settings

| Where | Setting |
|---|---|
| top of `config.json` | `"capture"`, `"all"` (every game, the default), `"fights"` (the fighting games only) or `"off"` |
| `retroarch` section | `"ram_dump": {"enabled": true, "every": 0.25}` |
| `retroarch` section | `"screenshots": {"enabled": true, "every": 2.0, "dir": ""}`. Set `"dir"` to RetroArch's screenshot folder (Settings, Directory, Screenshots) and the log says whether the first picture appeared |

In RetroArch, turn off the screenshot notification and flash (Settings, On-Screen Display, On-Screen Notifications). Also turn off "GPU Screenshot" (Settings, Video, Output, an advanced setting), otherwise the pictures come out with the CRT shader at full size, 3 MB each, instead of the game's own 304 x 224.

## Sending a game

For a game that is not tuned yet, or one that misbehaves, play a normal game of five to ten minutes. For a fighting game, a match is enough, two rounds won, one lost, a super move. For a Metal Slug, up to the first boss, with a few grenades, a life lost and a vehicle.

Then zip and attach to a GitHub [issue](https://github.com/Byoyoyo/ArcadeDMD/issues).

- the `.log` and the `.ram` of the game from `runtime\captures`
- the zip of the screenshots
- `runtime\arcadedmd.log`

## The robot

The games can play by themselves, so that their memory is recorded with nobody at the cabinet (1.39). RetroArch takes the buttons of a pad from the network, and the robot sends them: a coin, START, then the stick and the buttons at random, and a second player for the last part of each game.

1. Leave ArcadeDMD running. While the robot plays, it records the whole memory of each game whatever its settings, and leaves the screenshots to the robot. The robot waits for ArcadeDMD's word before it plays a game.
2. Run `robot_test.bat` with a Neo Geo game started from your frontend. It reads how RetroArch was started, closes the game, starts it again itself, checks that the game sees the stick it holds and plays for two minutes. Its result is in `runtime\robot_test.txt`.
3. Run `robot.bat`. It plays every game of ArcadeDMD whose ROM is in the same folder, six minutes each, the fighting games first. `robot.bat 10` plays ten minutes each, `robot.bat samsho2 garou` only those games. Ctrl+C stops it, and it goes on where it stopped when started again.

The robot asks RetroArch for a screenshot every ten seconds. When a game is closed, its recording and its screenshots go into one file, `runtime\robot\<game>.zip`.

While the robot plays, RetroArch runs in a window, without sound and without reading the computer's pads. The screen must stay on: RetroArch cannot open its window without it. Windows is kept awake. Only Ctrl+C stops the tour. A game that does not start, or that is cut before half, is tried once more at the end of the tour, then left aside and named at the end. Games left aside come last at the next run. When three games in a row fail, the robot starts a game it has already recorded. If that one runs, the three are at fault and the tour goes on. If it fails too, the screen is off, ArcadeDMD is closed or the ROMs are gone, and the robot waits, looks again every five minutes, and takes those games again by itself as soon as it works. A stick the game does not show, or a game that does not run at its own pace, is written on the game's line and never stops anything. An error nobody foresaw costs one game and is kept in `runtime\robot_crash.log`.

`robot_screen_off.bat` is the same tour for a screen that is off, at night for instance. RetroArch runs without any window and the memory is recorded, but without screenshots: RetroArch closes when asked for one without a video driver. The games played that way are played again, with their screenshots, by `robot.bat`.

`robot_win.bat` is a second tour, for the fighting games alone, ten minutes each (1.39). The robot of the first tour loses quickly and meets three to five fighters and two to four stages of a game. In this one it wins its fights, so that it crosses each game from its first opponent to its last. While a round is fought it writes three things in the game's memory, where the game's file reads them: player 1's life, put back to the highest it had in the round, the opponent's, kept at a tenth, and the timer, run out once it has counted three seconds. Nothing is written outside a round, and never in a game played by hand. A game whose life bars the file does not know is played as in the first tour, and when RetroArch does not take the writes the tour goes on with two robot players, who meet more fighters than one. Its files go to `runtime\robot\win`, its list of games done is its own, and it is stopped and started again like the first.

`robot_film.bat` is a third tour, for the fighting games again, three minutes each (1.39). It tells what a game shows at which instant when a round starts, so that the marquee's FIGHT ! can be set on the game's own. The robot wins as in the second tour, but leaves each round as the game plays it until its timer has counted two seconds, and asks for a screenshot every 1.2 seconds from the start of the round until then. RetroArch names a screenshot by its second, which is not enough. The robot writes down the instant it asked for each one in `shots.json`, kept in the game's file (`runtime\robot\film\<game>.zip`), and the recording's header holds the same clock's instant. A screenshot then falls among the snapshots of the memory to a tenth of a second. The first two tours keep that journal too. An ArcadeDMD started before this version was installed does not write that instant, the robot then closes it and starts the right one. Its list of games done is its own, and it is stopped and started again like the others.

RetroArch's own settings are not changed, and the games the robot plays stay out of its history. The robot's settings are in `runtime\robot.cfg`, given to RetroArch on its command line.

## Tools for the curious

- `python tools\replay_capture.py runtime\captures\<file>` prints what the HD screen showed second by second, `--frames 30,47` draws it at those seconds.
- `python tools\values_check.py runtime\robot\<game>.zip` checks each value of the game's file against a game the robot recorded (1.39): a timer counts down and starts again from its top, a life bar goes down hit after hit and reads full when a round starts, a score only rises. `--sheet out.jpg` puts six screenshots on one image with what the file reads at the same second, to check by eye. `--find` looks for the timer and the life bars in the whole memory, `--match 45:35 105:25` for the bytes that hold the numbers read on the screenshots.
- `python tools\ram_diff.py <file.ram> --down 120 160` lists the memory words that only go down between two moments (a life), `--watch 0x1012AA` follows one, `--diff 118 121` shows what changed.

The recordings already received are kept in `tests\captures`. The recorded fights are replayed as tests at every change: `python tools\captures_check.py` compares what the HD screen announces, second by second, with what is expected in `tests\expected`.
