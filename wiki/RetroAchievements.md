ArcadeDMD announces on the marquee the achievements you unlock on [RetroAchievements](https://retroachievements.org) while you play. New in 1.41.

## What it shows

When an achievement is unlocked, a slab comes over the middle of the HD marquee for six seconds, whatever the scene. It gives the name of the achievement, its points and how many of the game's achievements you now have. The LED panel shows the name on one line.

## Setting the account

1. In the emulator, sign in to your RetroAchievements account. In RetroArch it is in Settings, Achievements. The emulator is what unlocks the achievements, ArcadeDMD only announces them.
2. On retroachievements.org, open the settings of your account and copy the **web API key** from the Keys section.
3. In the ArcadeDMD window, open the **Achievements** tab. Type your user name, paste the key, tick the box and press **Try the account**. The site answers with your name and your points.
4. Save. ArcadeDMD starts again with the account.

ArcadeDMD never asks for your password. The key stays in `config.json` on your PC. It is written neither in the log nor in the recordings, and the window never sends it back to its page. **Forget the key** removes it.

## Good to know

- ArcadeDMD asks the site every 15 seconds while a game is played, and for a minute and a half after it is closed. The slab comes within those 15 seconds, the time for the emulator to tell the site and for ArcadeDMD to ask.
- Nothing is asked while no game is played.
- What you unlocked before the game was started is not announced.
- Without Internet, or when the site does not answer, the game and the marquee carry on. The log says it once and ArcadeDMD tries again.
- When ArcadeDMD starts with the account set, the log says `RetroAchievements: the site answers for` and your name.

## By hand

The tab writes this part of `config.json`.

```json
"retroachievements": {"enabled": true, "user": "YourName", "key": "your web API key", "every": 15}
```

`every` is the number of seconds between two questions to the site, never under 10.
