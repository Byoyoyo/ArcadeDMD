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

## Tools for the curious

- `python tools\replay_capture.py runtime\captures\<file>` prints what the HD screen showed second by second, `--frames 30,47` draws it at those seconds.
- `python tools\ram_diff.py <file.ram> --down 120 160` lists the memory words that only go down between two moments (a life), `--watch 0x1012AA` follows one, `--diff 118 121` shows what changed.

The recordings already received are kept in `tests\captures` and replayed as tests.
