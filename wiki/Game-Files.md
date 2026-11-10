## Adding a game or editing a scene

1. Copy `games\aburner2.json` under the game's short name, for example `games\outrun.json`.
2. Change `"match"` (`"system": ["outrun"]`), the title and the values.
3. Find the addresses with `learn.bat` (if there is no dedicated file, the tool creates it for you).
4. Edit the scene. The engine reloads the files on the fly, so there is no need to restart while you fine-tune.

Supported value formats

| `type` | Meaning |
|---|---|
| `u8` | one byte |
| `u16` / `u32` / `s8` / `s16` / `s32` | one byte (`s8`), two or four bytes in the order of the processor, `s` for a signed number (a boss's life going below zero) |
| `be` / `le` | binary over `bytes` bytes, big-endian or little-endian |
| `bcd` / `bcd_le` | BCD over `bytes` bytes (two digits per byte) |
| `digits` | one digit per byte (`digit_offset` 0x30 for ASCII) |

The common options are `mult` (for a score stored divided by 10, which is very common), `add`, `min`, `max`, `mask` and `shift`. `valid` gives the values the game can really have, `[1, 6]` for the six missions of Metal Slug. Another value read is set aside and the last good one stays, so the RAM of a game that boots shows nothing wrong. `learn_ranges` limits the area captured for the learning tool. `hold_zero` (in seconds) keeps the last score on display when the value read briefly drops to 0 in the middle of a game, while the game recreates the fighter between two rounds.

For a value stored in an object that moves around in memory (the Samurai Shodown fighters at every round), `"ptr"` gives the address where the object's location is read (32 bits) and `"addr"` becomes the offset inside the object. `"ptr_range"` rules out a pointer that is not ready yet. `learn.bat` writes this kind of value by itself when the captures show that the value follows the object.

Some value names have a special role in the HD scenes. `stage`, `backdrop` and `mission` change the background ([[HD Marquee]]), `p1_input` and `p2_input` are the Neo Geo BIOS stick and buttons (Metal Slug handgun shots, the ships of Blazing Star, Pulstar and Last Resort, the planes of the Aero Fighters, the hunters of Top Hunter, the arrow of Puzzle Bobble, the jester of Magical Drop III).

`"derived"` computes a value from other values, for example the character name. `"value"` takes a value that was read, `"pick"` chooses from a list according to `"at"`, and `"names"` turns a number into text. `"sum"` adds values, `"ge"` gives 1 when the first value reaches the second and 0 otherwise. `"eq"` gives 1 when both are equal and 0 otherwise, `"first"` the first of its values that is known. `"rise"` gives 1 while its value is 1, once `"from"` has been 1 since the last `"reset"`, the only one that remembers from one reading to the next (the boss of DoDonPachi, once its stage was seen scrolling toward it in a game going on, in `games\ddonpach.json`). `"names"` can also hold one list per language, `{"en": [...], "fr": [...]}`, as in `games\wjammers.json`. See `games\samsho2.json` and `games\kof98.json`.

Scene elements

| `type` | Role | Main settings |
|---|---|---|
| `marquee` | scrolling text | `text` or `segments` (pieces in different colors), `font`, `y`, `speed`, `gap`, `color`, `accent_initials` |
| `text` | fixed text or value | `text` with `{score}`, `x`, `y`, `align`, `segments`, `flash` |
| `cycle` | alternates between several pages | `period`, `pages` |
| `bars` | grass or equalizer | `x`, `w`, `min`, `max`, `color`, `tip`, `flowers` |
| `waves` | hills scrolling in the background | `layers` (`y`, `amp`, `speed`, `color`, `edge`) |
| `mountains` | solid mountains and ground line (Vera style) | `peaks` (`[x, height]`), `floor`, `color`, `ground`, `speed` |
| `particles` | missiles and bursts when a value goes up | `rate`, `color`, `y`, `burst` |
| `anim` | an animation played once when a value changes (an explosion when the score goes up) | `image` (list, the first file found, `{game}` for the game), `on`, `change` (`up`, `down`, `any`), `ratio` (small or big gain), `x` and `y` (a number, `[start, end]`, or several `[start, end]` to pick from), `near` and `ahead` (ahead of a `ship`), `count`, `spread`, `delay`, `ms`, `black` |
| `events` | short events that take the panel for a moment, one at a time, as on a pinball (BOMB!, POWER UP, a life lost, GAME OVER) | `events`, a list. Each one has `on`, `change`, `step` (the size of the change), `from` and `to` (the values before and after), `when`, `text` (with `{lives}`...), `color`, `font` (its biggest size, it grows up to it), `y`, `icon` and `colors` (a small drawing at the left of the text), `icon_scale`, `anim` (animations played at the start, same keys as `anim`), `text_delay`, `ms`, `clear` (`false` keeps the scene behind), `priority` (a more important event replaces the one playing, a less important one waits) |
| `sprite` | animated sprite (PNG strip or GIF) | `image`, `frames`, `mode` (`pass`, `pingpong`, `fixed`), `dim` (brightness), `alpha`, `shoot` (fires when a value goes up) |
| `gauge` | health bar | `var`, `max` (a number, or `"peak"` for the highest value seen while it shows, a boss's life, kept `peak_hold` seconds while hidden), `x`, `y`, `w`, `h`, `anchor` (anchored side), `color`, `low`, `back`, `border`, `bevel` (light edge at the bottom and on the right) |
| `clock` | clock | `format`, `font` |
| `icons` | a small drawing repeated for a value (lives as ships, power pips) | `var`, `pattern` (rows of characters, `.` for empty), `colors`, `max`, `gap`, `empty` (color of the slots left), `align`, `flash` |
| `counter` | a small drawing followed by a number (a plane and x3 for the lives) | `var`, `pattern`, `colors`, `font`, `color` (of the number), `prefix` (`x`), `align` (`left` from `x`, `right` up to `x`), `max` (above it nothing shows, a value the game has not set yet), `flash` |
| `ship` | the player's ship, which follows the stick and fires while button A is held (`p1_input`), or flies by itself | `image` (list, `{game}` for the game), `frames`, `fps`, `face` (`right`, or `left` for player 2 facing player 1), `area` (`[x0, y0, x1, y1]`), `input`, `speed`, `fire` (`color`, `speed`, `rate`, `len`), `shoot_on` (fires when the score goes up), `anchor` (so that an `anim` layer with `near` goes off ahead of it), `hit` and `unless` (an enemy blows up now and then as long as the score is not known) |
| `dot` | a disk whose color comes from a value (Puzzle Bobble bubbles), or always the first color without `var` (a moon) | `var`, `colors` (one color per value), `x`, `y`, `r`, `rim`, `shine` |
| `arrow` | an arrow that turns with a value (Neo Turf Masters wind) | `var`, `steps` (16, 0 points up then clockwise), `x`, `y`, `len`, `color`, `ring`, `flash` |
| `image`, `rect` | fixed image, rectangle | |

The available fonts are `4x6`, `5x8`, `6x10`, `6x13`, `7x14`, `7x14B`, `8x13B` and `9x15B`. The `y` of a text is the top of the capital letters. `when` shows an element only under a condition, for example `{"has": "credits"}` or `{"var": "mode", "eq": 12}`.

The `"demo"` section gives the starting values for the demos (`demo_neogeo.bat`, `python arcadedmd.py demo <game>`). `"attract": true` starts on the coin screen, then two coins and START. `"sim"` moves the game's own values, one entry per value, with `"cycle"` (a list taken in turn), `"count"` (`[min, max, step]`, back to the start at the end) or `"random"` (`[min, max]`), `"every"` (seconds, or `[min, max]`) and `"start"` (first change). See `games\wjammers.json`.
