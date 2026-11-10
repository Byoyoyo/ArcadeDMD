## Text files for OBS

ArcadeDMD writes the values of the current game to the `obs\` folder, one file per value. Each file is updated as soon as the value changes, and is emptied outside games. It works with MAME, Arcade64 and RetroArch.

| File | Content |
|---|---|
| `game.txt` | game title |
| `score_p1.txt`, `score_p2.txt` | each player's score |
| `credits.txt` | credits (MAME and Arcade64) |
| `fighter_p1.txt`, `fighter_p2.txt` | character currently fighting, when known |
| `streak_p1.txt`, `streak_p2.txt` | wins in a row in VS matches (King of Fighters, once learned) |
| `vs_p1.txt`, `vs_p2.txt` | "BEAT BY 02" or "CHALLENGER", as at the top of the game screen |
| `best_streak.txt` | best streak of the current game, for example "BEAT BY 05 \| P2 RUGAL \| 26/10/2026" |
| `vs_history.txt` | one line per VS match won, with the date, the game, the winner and their streak |
| `records.json` | the best streak of each game, kept from one session to the next |

In OBS, add a Text (GDI+) source, tick "Read from file" and choose the file. The texts are the same in every language. "P2 RUGAL > P1 KIM" means that P2 beat P1.

To turn this off, set `"enabled": false` in the `textfiles` section of `config.json`. `"folder"` picks another folder, and `"history": false` turns off the history.

## DOFLinx bridge (optional)

ArcadeDMD can pose as DOF2DMD. DOFLinx then sends it the score and credits of every game it knows, with no address to look for.

1. In `config.json`, set `"enabled": true` in the `doflinx_bridge` section. It listens on port 8081, leaving 8080 to pixelweb.
2. DOFLinx reads the address from DOF2DMD's `settings.ini` (`url_prefix`). Set it to `http://127.0.0.1:8081`.
3. Do not run DOF2DMD at the same time, since the two cannot listen on the same port. When ArcadeDMD answers, DOFLinx no longer tries to start DOF2DMD.

The two sources complement each other. For After Burner II, the high score comes from the plugin and the score from DOFLinx.
