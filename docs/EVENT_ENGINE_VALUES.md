# Adresses lues, jeu par jeu

Fichier produit par `python tools/event_catalog.py` à partir de `games/*.json`, qui restent la référence. Chaque ligne donne le nom de la valeur, son adresse, son type et ses options. Le sens de chaque valeur est dans le champ `note` du fichier de jeu. Le décodage est décrit dans `dmd/memvalues.py` et résumé dans [EVENT_ENGINE_HANDOFF.md](EVENT_ENGINE_HANDOFF.md).

## 1941 — 1941: Counter Attack

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF0DA5   u8        mult=14.285714 min=0 max=100 zero_from="0x83" round=1
health_p2              0xFF0DA7   u8        mult=14.285714 min=0 max=100 zero_from="0x83" round=1
credits                0xFF0D59   u8
weapon                 0xFF0DC8   u8
weapon_time            0xFF0DE7   bcd       bytes=1
score                  0xFF0DB6   bcd       bytes=4
score_p2               0xFF0DBA   bcd       bytes=4
```

`derived` :

- `weapon_name` = `{"value":"weapon","names":{"0":"NORMAL","1":"M. GUN","2":"S. SHELL","3":"MISSILE"}}`

## 1944 — 1944: The Loop Master

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0x9226A5   u8        mult=1.333333 min=0 max=100 zero_from="0xA5" round=1 mame_only=true
health_p2              0x9227A5   u8        mult=1.333333 min=0 max=100 zero_from="0xA5" round=1 mame_only=true
credits                0x921D51   u8        mame_only=true
bombs                  0x922405   u8        mame_only=true
power                  0x922429   u8        max=3 mame_only=true
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
fighters               0x9223FB   u8        mame_only=true
gold                   0x9223FD   u8        mame_only=true
fighters_p2            0x9224FB   u8        mame_only=true
gold_p2                0x9224FD   u8        mame_only=true
warning                -          u8        mame_only=true
```

## 19xx — 19XX: The War Against Destiny

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF4D15   u8
lives                  0xFF82EC   u8
lives_p2               0xFF83EC   u8
bombs                  0xFF8305   u8
weapon                 0xFF82F1   u8
plane                  0xFF8247   u8
plane_p2               0xFF8347   u8
score                  0xFF8306   bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `weapon_name` = `{"value":"weapon","names":{"4":"SHOT","8":"3-WAY","12":"SHELL"}}`

## 2020bb — 2020 Super Baseball

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
time                   0x104290   bcd       bytes=1
time_min               0x10428F   u8        valid=[0,9]
outs_total             0x1000C0   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## 3countb — 3 Count Bout

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_chr                0x1082E9   u8
_p2_chr                0x1082ED   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"T.ROGERS","1":"R.WILSON","6":"GANDHARA","7":"L.BRADLAY","9":"G.BIGBOMB","10":"BRAB.MAN","11":"B.HABLAM","12":"M.BARNES"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"T.ROGERS","1":"R.WILSON","6":"GANDHARA","7":"L.BRADLAY","9":"G.BIGBOMB","10":"BRAB.MAN","11":"B.HABLAM","12":"M.BARNES"}}`

## 3wonders — Three Wonders

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_time                  0xFF1011   bcd       bytes=1
credits                0xFF0D59   u8
lives                  0xFF0DE7   u8
lives_p2               0xFF0DE8   u8
score                  0xFF0DD2   bcd       bytes=4
score_p2               -          bcd       bytes=4
weapon                 0xFF0E14   u8
```

## aburner2 — After Burner II

cpu :mainpcb:maincpu

```
record                 0xFF846E   bcd       bytes=4 mult=10
score                  -          bcd       bytes=4 mult=10
credits                -          u8
```

## agallet — Air Gallet

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0x1001CD   u8
lives                  0x1002ED   u8
lives_p2               0x1002EF   u8
bombs                  0x100D73   u8
bombs_p2               0x100E33   u8
power                  0x100D7C   u8        max=29
power_p2               0x100E3C   u8        max=29
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## akatana — Akai Katana

cpu :maincpu, ram_base 0xC000000, ram_size 0x800000, swap16 True

```
score                  0xC7E86AC  digits_le bytes=10
score_p2               0xC7E89FC  digits_le bytes=10
```

## alpham2 — Alpha Mission II

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1010A8   bcd       bytes=4
score_p2               0x1011A8   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x1010F2   u8        zero_from=240
lives_p2               0x1011F2   u8        zero_from=240
power                  0x1010DD   u8        max=24 zero_from=240
power_p2               0x1011DD   u8        max=24 zero_from=240
gold                   0x1010B0   bcd       bytes=2
gold_p2                0x1011B0   bcd       bytes=2
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## androdun — Andro Dunos

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x100184   be        bytes=4 mult=10
score_p2               0x100188   be        bytes=4 mult=10
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x100343   u8        add=-1 min=0
shot                   0x100350   u8        max=7
bomb_pw                0x100351   u8        max=5
missile                0x100352   u8        max=8
unit                   0x100353   u8        max=8
lives_p2               0x100383   u8        add=-1 min=0
shot_p2                0x100390   u8        max=7
bomb_pw_p2             0x100391   u8        max=5
missile_p2             0x100392   u8        max=8
unit_p2                0x100393   u8        max=8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## aodk — Aggressors of Dark Kombat

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x100066   be        bytes=2 mult=0.032563 min=0 max=100 zero_from="0x85FF"
health_p2              0x100166   be        bytes=2 mult=0.032563 min=0 max=100 zero_from="0x85FF"
backdrop               0x10C008   u8
_time                  0x10B649   u8
_time_sub              0x10B64B   u8        start=0
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## aof — Art of Fighting

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x1092CD   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x1093CD   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
backdrop               0x108401   u8
rounds                 0x1090E7   u8
rounds_p2              0x1091E7   u8
time                   0x108406   bcd       bytes=1
_time_sub              0x108407   u8        start=60
score                  0x1094A8   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x1092C3   u8
_p2_chr                0x1093C3   u8
power                  0x1094A4   u8        mult=0.78125 min=0 max=100 round=1
power_p2               0x1095A4   u8        mult=0.78125 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYO","1":"ROBERT","2":"TODO","3":"JACK","4":"LEE","5":"KING","6":"MICKY","7":"JOHN","8":"MR.BIG","9":"MR.KARATE"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYO","1":"ROBERT","2":"TODO","3":"JACK","4":"LEE","5":"KING","6":"MICKY","7":"JOHN","8":"MR.BIG","9":"MR.KARATE"}}`

## aof2 — Art of Fighting 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x1080BD   u8
_p2_dir                0x10847D   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x1092ED   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x1093ED   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
backdrop               0x108401   u8
rounds                 0x1090F1   u8
rounds_p2              0x1091F1   u8
time                   0x108406   bcd       bytes=1
_time_sub              0x108407   u8        start=60
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x1092E3   u8
_p2_chr                0x1093E3   u8
power                  0x1094A4   u8        mult=0.78125 min=0 max=100 round=1
power_p2               0x1095A4   u8        mult=0.78125 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"RYO","2":"ROBERT","3":"EIJI","4":"JACK","5":"LEE","6":"KING","7":"MICKEY","8":"JOHN","9":"MR.BIG","10":"TAKUMA","11":"YURI","12":"TEMJIN","13":"GEESE"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"RYO","2":"ROBERT","3":"EIJI","4":"JACK","5":"LEE","6":"KING","7":"MICKEY","8":"JOHN","9":"MR.BIG","10":"TAKUMA","11":"YURI","12":"TEMJIN","13":"GEESE"}}`

## aof3 — Art of Fighting 3

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x10048C   u8
_p2_dir                0x10058C   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x100468   be        bytes=2 mult=0.024414 min=0 max=100 zero_from="0x8800"
health_p2              0x100568   be        bytes=2 mult=0.024414 min=0 max=100 zero_from="0x8800"
backdrop               0x104BE7   u8
time                   0x10DF0F   u8        max=99
_time_sub              0x10DF11   u8        start=60
_fight_cue             0x10E338   u8        start=0
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x104C0D   u8
_p2_chr                0x104C0F   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"ROBERT","1":"RYO","2":"KARMAN","3":"KAZUMI","4":"RODY","5":"LENNY","6":"WANG","7":"JIN","8":"SINCLAIR","9":"WYLER"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"ROBERT","1":"RYO","2":"KARMAN","3":"KAZUMI","4":"RODY","5":"LENNY","6":"WANG","7":"JIN","8":"SINCLAIR","9":"WYLER"}}`

## armwar — Armored Warriors

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF95DD   u8        mult=1.25 min=0 max=100 zero_from="0xA8" round=1
health_p2              0xFF979D   u8        mult=1.25 min=0 max=100 zero_from="0xA8" round=1
lives                  0xFF96E3   u8
lives_p2               0xFF98A3   u8
_p1_chr                0xFF95DA   u8
_p2_chr                0xFF979A   u8
score                  0xFF971A   bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"BLOODIA","1":"REPTOS","2":"GULDIN","3":"FORDY"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"BLOODIA","1":"REPTOS","2":"GULDIN","3":"FORDY"}}`

## avsp — Alien vs. Predator

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF83C1   u8        mult=0.990099 min=0 max=100 zero_from="0xB2" round=1
health_p2              0xFF84C1   u8        mult=0.990099 min=0 max=100 zero_from="0xB2" round=1
_time                  0xFF8225   bcd       bytes=1
lives                  0xFF8471   u8
lives_p2               0xFF8571   u8
power                  0xFF842F   u8        mult=0.438596 min=0 max=100 round=1
power_p2               0xFF852F   u8        mult=0.438596 min=0 max=100 round=1
_p1_chr                0xFF8452   u8
_p2_chr                0xFF8552   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"P.WARRIOR","1":"SCHAEFER","2":"P.HUNTER","3":"LINN"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"P.WARRIOR","1":"SCHAEFER","2":"P.HUNTER","3":"LINN"}}`

## b2b — Bang Bang Busters

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x105D24   bcd       bytes=4
score_p2               0x105D28   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x106907   u8
lives_p2               0x106967   u8
boss                   0x107247   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## bakatono — Bakatonosama Mahjong Manyuuki

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_move_time             0x1000FD   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## bangbead — Bang Bead

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10048A   be        bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time_tens              0x1044C9   u8
time_units             0x1044CB   u8
power                  0x10444C   u8        max=128
stock                  0x104461   u8        max=3
power_p2               0x104476   u8        max=128
stock_p2               0x10448B   u8        max=3
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## batcir — Battle Circuit

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF82B7   u8        mult=0.78125 min=0 max=100 zero_from="0xC0" round=1
health_p2              0xFF83F7   u8        mult=0.78125 min=0 max=100 zero_from="0xC0" round=1
_time                  0xFF5D57   u8
credits                0xFF5863   u8
lives                  0xFF830A   u8
lives_p2               0xFF844A   u8
score                  0xFF832A   bcd       bytes=4
score_p2               0xFF846A   bcd       bytes=4
money                  0xFF8328   be        bytes=2
```

## bjourney — Blue's Journey

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1030A0   bcd       bytes=4
score_p2               -          bcd       bytes=4
time                   0x106906   u16
lives                  0x107000   u8
lives_p2               0x107400   u8
energy                 0x107011   u8        max=5
energy_p2              0x107411   u8        max=5
money                  0x107010   u8
money_p2               0x107410   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## blazstar — Blazing Star

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x101BA4   bcd       bytes=4
score_p2               0x101BA8   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x101BA1   u8
lives_p2               0x101BA3   u8
power                  0x101B79   u8        max=3
power_p2               0x101B7B   u8        max=3
round                  0x101C87   u8        add=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## breakers — Breakers

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x107332   u8        mult=3.333333 min=0 max=100 zero_from="0x8F"
health_p2              0x107892   u8        mult=3.333333 min=0 max=100 zero_from="0x8F"
_p1_chr                0x107155   u8
_p2_chr                0x1076B5   u8
_p1_dir                0x107348   u8
_p2_dir                0x1078A8   u8
backdrop               0x1076B5   u8
time                   0x107C0B   u8        max=99
_time_sub              0x107C0D   u8        start=32
_fight_cue             0x107C1F   u8        start=96
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"SHO","1":"DAO-LONG","2":"CONDOR","3":"TIA","4":"RILA","5":"ALSION III","6":"PIELLE","7":"MAHERL","8":"BAI-HU"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"SHO","1":"DAO-LONG","2":"CONDOR","3":"TIA","4":"RILA","5":"ALSION III","6":"PIELLE","7":"MAHERL","8":"BAI-HU"}}`

## breakrev — Breakers Revenge

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10734E   be        bytes=2 mult=0.013021 min=0 max=100 zero_from="0x8F00"
health_p2              0x1078AE   be        bytes=2 mult=0.013021 min=0 max=100 zero_from="0x8F00"
_p1_chr                0x107171   u8
_p2_chr                0x1076D1   u8
_p1_dir                0x107364   u8
_p2_dir                0x1078C4   u8
backdrop               0x1076D1   u8
time                   0x107C27   u8        max=99
_time_sub              0x107C29   u8        start=32
_fight_cue             0x107C3B   u8        start=96
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"SHO","1":"DAO-LONG","2":"CONDOR","3":"TIA","4":"RILA","5":"ALSION III","6":"PIELLE","7":"MAHERL","8":"BAI-HU","9":"SAIZO"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"SHO","1":"DAO-LONG","2":"CONDOR","3":"TIA","4":"RILA","5":"ALSION III","6":"PIELLE","7":"MAHERL","8":"BAI-HU","9":"SAIZO"}}`

## bstars — Baseball Stars Professional

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
balls                  0x10107D   u8
strikes                0x10107E   u8
outs                   0x10107C   u8
inning                 0x101083   u8
time                   0x10004A   bcd       bytes=1
time_min               0x100049   u8        valid=[0,9]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## bstars2 — Baseball Stars 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
runs                   0x1043F2   bcd       bytes=1
runs_p2                0x1043F3   bcd       bytes=1
balls                  0x10442D   u8        max=3
strikes                0x10442C   u8        max=2
outs                   0x10442B   u8        max=3
pow                    0x104422   u8        max=99
pow_p2                 0x104423   u8        max=99
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## burningf — Burning Fight

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10C004   bcd       bytes=4 mult=0.1 round=0
score_p2               0x10C00C   bcd       bytes=3 mult=10
time                   0x10D002   bcd       bytes=1
lives                  0x100230   u8
lives_p2               0x1002B0   u8
energy                 0x100221   u8        max=255
energy_p2              0x1002A1   u8        max=255
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## captcomm — Captain Commando

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFFA9D1   u8        mult=1.388889 min=0 max=100 zero_from="0xA4" round=1
health_p2              0xFFAAD1   u8        mult=1.388889 min=0 max=100 zero_from="0xA4" round=1
credits                0xFFA850   u8
lives                  0xFFAA7C   u8
lives_p2               0xFFAB7C   u8
_p1_chr                0xFFAA34   u8
_p2_chr                0xFFAB34   u8
score                  0xFFAA75   bcd       bytes=3
score_p2               0xFFAB75   bcd       bytes=3
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"M.COMMANDO","1":"C.COMMANDO","2":"N.COMMANDO","3":"B.COMMANDO"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"M.COMMANDO","1":"C.COMMANDO","2":"N.COMMANDO","3":"B.COMMANDO"}}`

## cawing — Carrier Air Wing

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF838C   be        bytes=2 mult=1.041667 min=0 max=100 zero_from="0x8030" round=1
health_p2              0xFF848C   be        bytes=2 mult=1.041667 min=0 max=100 zero_from="0x8030" round=1
time                   0xFF800B   bcd       bytes=1
credits                0xFF82AB   u8
ammo                   0xFF83BB   bcd       bytes=1
money                  0xFF83B3   bcd       bytes=2
weapon                 0xFF83C8   u8
power                  0xFF83B0   u8        max=5
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `weapon_name` = `{"value":"weapon","names":{"0":"SPREAD","1":"MISSILE","2":"GUNS"}}`

## choko — Janpai Puzzle Choukou

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_time                  0xFF63E8   be        bytes=2
credits                0xFF809E   u8
```

## crsword — Crossed Swords

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
energy                 0x10405B   u8        max=50
magic                  0x10405C   u8        max=99
gold                   0x104066   u16
energy_p2              0x1040DB   u8        max=50
magic_p2               0x1040DC   u8        max=99
gold_p2                0x1040E6   u16
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## crusherm — Crusher Makochan

cpu :maincpu, ram_base 0x340000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## csclub — Capcom Sports Club

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_time                  0xFF8C92   digits    bytes=3
credits                0xFF8AE9   u8
score                  0xFF8B80   be        bytes=4
score_p2               -          bcd       bytes=4
```

## ctomaday — Captain Tomaday

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x101382   be        bytes=4
score_p2               0x10139E   be        bytes=4
score_units            0x101382   be        bytes=4 mult=0.01 round=2
score_units_p2         0x10139E   be        bytes=4 mult=0.01 round=2
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x10137D   u8        zero_from=240
power                  0x104201   u8        max=5
power_l                0x1041AB   u8        max=5
lives_p2               0x101399   u8        zero_from=240
power_p2               0x1043F1   u8        max=5
power_l_p2             0x10439B   u8        max=5
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## cworld2j — Adventure Quiz Capcom World 2

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF0EE3   u8
lives                  0xFF11DB   u8
lives_p2               0xFF14AB   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## cyberlip — Cyber-Lip

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x102080   bcd       bytes=4
score_p2               0x102180   bcd       bytes=4
time                   0x107E25   bcd       bytes=1
time_min               0x107E26   u8        valid=[0,9]
lives                  0x10209D   bcd       bytes=1 zero_from=90
lives_p2               0x10219D   bcd       bytes=1 zero_from=90
ammo_auto              0x1020EC   bcd       bytes=2
ammo_fire              0x1020EE   bcd       bytes=2
ammo_wide              0x1020F0   bcd       bytes=2
ammo_bazooka           0x1020F2   bcd       bytes=2
ammo_grenade           0x1020F4   bcd       bytes=2
ammo_auto_p2           0x1021EC   bcd       bytes=2
ammo_fire_p2           0x1021EE   bcd       bytes=2
ammo_wide_p2           0x1021F0   bcd       bytes=2
ammo_bazooka_p2        0x1021F2   bcd       bytes=2
ammo_grenade_p2        0x1021F4   bcd       bytes=2
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## cybots — Cyberbots: Fullmetal Madness

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF81E5   u8        mult=0.657895 min=0 max=100 zero_from="0xCC" round=1
health_p2              0xFF85E5   u8        mult=0.657895 min=0 max=100 zero_from="0xCC" round=1
time                   0xFFEBA0   bcd       bytes=1
credits                0xFF80B6   u8
power                  0xFF8534   u8        mult=1.587302 min=0 max=100 round=1
power_p2               0xFF8934   u8        mult=1.587302 min=0 max=100 round=1
_p1_chr                0xFF8510   u8
backdrop               0xFFEA2D   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"JIN","1":"SANTANA","2":"MARY","3":"ARIETA","4":"GAWAINE","5":"BAO + MAO","6":"DEVILOTTE","7":"C.+.TESSAN","8":"SHADE","9":"G. O. D."}}`

## ddonpach — DoDonPachi

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
lives                  0x101965   u8        add=-1
lives_p2               0x101967   u8        add=-1
bombs                  0x102CB0   u8
bombs_p2               0x102CF0   u8
bombs_max              0x102CB1   u8
bombs_max_p2           0x102CF1   u8
power                  0x102CAD   u8        max=4
power_p2               0x102CED   u8        max=4
combo                  0x1017D1   u8        mult=1.818182 min=0 max=100 round=1
combo_p2               0x1017FB   u8        mult=1.818182 min=0 max=100 round=1
ship                   0x102D1D   u8
ship_p2                0x102D5D   u8
credits                0x1013AB   u8
_score10               0x10161E   bcd       bytes=4 mult=10
_cont                  0x10174F   u8
_score10_p2            0x101622   bcd       bytes=4 mult=10
_cont_p2               0x101753   u8
hits                   0x1017EC   bcd       bytes=2
hits_p2                0x101816   bcd       bytes=2
stage                  0x101979   u8        add=1
loop                   0x10197A   u16       bytes=2
distance               0x10198E   be        bytes=2
phase                  0x1017A4   u8
_state                 0x1017A7   u8
_players               0x1017A9   u8
_out_p1                0x1017A9   u8        mask=16 shift=4
_out_p2                0x1017A9   u8        mask=32 shift=5
_stage_task            0x1013FC   be        bytes=4
_boss_hp               0x100198   s32       bytes=4
_boss_hp_b             0x100158   s32       bytes=4
```

Propre au romset `ddonpacha` :

```
_stage_task            -          be        bytes=4
```

Propre au romset `ddonpachj` :

```
_stage_task            -          be        bytes=4
```

`tag` :

- `score` = `{"sum":["_score10","_cont"]}`
- `score_p2` = `{"sum":["_score10_p2","_cont_p2"]}`
- `p1_mode` = `{"pick":[{"ge":["lives",0]},0,0,0,0,0,0,1,{"pick":[0,2],"at":{"ge":["_score10",1]}},0,0,{"first":[{"pick":[{"pick":[1,{"ge":["lives",0]}],"at":{"ge":["lives_p2",0]}},{"pick":[1,0],"at":"_out_p1"}],"at":{"ge":["_players",128]}},{"…`
- `p2_mode` = `{"pick":[{"ge":["lives_p2",0]},0,0,0,0,0,1,0,{"pick":[0,2],"at":{"ge":["_score10_p2",1]}},0,0,{"first":[{"pick":[{"ge":["lives_p2",0]},{"pick":[1,0],"at":"_out_p2"}],"at":{"ge":["_players",128]}},{"ge":["lives_p2",0]}]},0,0],"at"…`

`derived` :

- `p1_ship` = `{"value":"ship","names":{"0":"TYPE-A","1":"TYPE-B","2":"TYPE-C"}}`
- `p2_ship` = `{"value":"ship_p2","names":{"0":"TYPE-A","1":"TYPE-B","2":"TYPE-C"}}`
- `boss` = `{"first":[{"rise":{"ge":[{"eq":["_stage_task",449176]},0]},"from":{"eq":["_stage_task",449176]},"reset":{"ge":[{"sum":[{"pick":[0,1,1,1,1,1,0,0,0,1,1,1,1,1],"at":"_state"},{"pick":[0,0,0,1,1],"at":"phase"}]},1]}},{"rise":{"ge":["…`
- `boss_name` = `{"value":"stage","names":{"1":"SUZAKU","2":"SENKOU","3":"KAKOU","4":"RAIKOU","5":"RANKOU","6":"RYUUKOU","7":"HIBACHI"}}`
- `warning` = `{"eq":["_stage_task",449176]}`
- `boss_hp` = `{"pick":["_boss_hp","_boss_hp","_boss_hp","_boss_hp","_boss_hp","_boss_hp","_boss_hp_b","_boss_hp"],"at":"stage"}`

## ddp2 — DoDonPachi II - Bee Storm

cpu :maincpu, ram_base 0x800000, ram_size 0x20000, swap16 True

```
credits                0x80EED6   u8
lives                  0x815976   u8
lives_p2               0x81598A   u8
stage                  0x815525   u8        add=1
bombs_p2               0x8158B0   u8
bombs                  0x8158A9   u8
power                  0x81260B   u8        max=4
power_p2               0x81279D   u8        max=4
combo                  0x815A51   u8        mult=1.5625 min=0 max=100 round=1
combo_p2               0x815A53   u8        mult=1.5625 min=0 max=100 round=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `ddp2100` :

```
credits                0x80EED4   u8
power                  0x812609   u8        max=4
power_p2               0x81271D   u8        max=4
combo                  0x815953   u8        mult=1.5625 min=0 max=100 round=1
combo_p2               0x815955   u8        mult=1.5625 min=0 max=100 round=1
```

Propre au romset `ddp2100c` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2100hk` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2100j` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2100k` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2100t` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2101` :

```
credits                0x80EED4   u8
power                  0x812609   u8        max=4
power_p2               0x81271D   u8        max=4
combo                  0x815953   u8        mult=1.5625 min=0 max=100 round=1
combo_p2               0x815955   u8        mult=1.5625 min=0 max=100 round=1
```

Propre au romset `ddp2101c` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2101hk` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2101j` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2101k` :

```
credits                0x80EED4   u8
```

Propre au romset `ddp2101t` :

```
credits                0x80EED4   u8
```

## ddp3 — DoDonPachi Dai-Ou-Jou

cpu :maincpu, ram_base 0x800000, ram_size 0x20000, swap16 True

```
credits                0x80394A   u8
lives                  0x813022   be        bytes=2
lives_p2               0x813024   be        bytes=2
bombs                  0x81037E   u8
bombs_p2               0x8103E0   u8
bombs_max              0x81037F   u8
bombs_max_p2           0x8103E1   u8
power                  0x81037A   be        bytes=2 max=8
power_p2               0x8103DC   be        bytes=2 max=8
combo                  0x81B365   u8        mult=1.785714 min=0 max=100 round=1
combo_p2               0x81B38F   u8        mult=1.785714 min=0 max=100 round=1
hits                   -          u8
stage                  -          u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `ddp3` :

```
credits                0x80394C   u8
lives                  0x813271   be        bytes=2
lives_p2               0x813273   be        bytes=2
bombs                  0x8105C8   u8
bombs_p2               0x81062A   u8
bombs_max              0x8105C9   u8
bombs_max_p2           0x81062B   u8
power                  -          be
power_p2               -          be
combo                  -          u8
combo_p2               -          u8
```

Propre au romset `ddpdoja` :

```
lives                  0x813012   be        bytes=2
lives_p2               0x813014   be        bytes=2
bombs                  0x81036E   u8
bombs_p2               0x8103D0   u8
bombs_max              0x81036F   u8
bombs_max_p2           0x8103D1   u8
power                  0x81036A   be        bytes=2 max=8
power_p2               0x8103CC   be        bytes=2 max=8
combo                  0x81B355   u8        mult=1.785714 min=0 max=100 round=1
combo_p2               0x81B37F   u8        mult=1.785714 min=0 max=100 round=1
```

Propre au romset `ddpdojb` :

```
lives                  0x813012   be        bytes=2
lives_p2               0x813014   be        bytes=2
bombs                  0x81036E   u8
bombs_p2               0x8103D0   u8
bombs_max              0x81036F   u8
bombs_max_p2           0x8103D1   u8
power                  0x81036A   be        bytes=2 max=8
power_p2               0x8103CC   be        bytes=2 max=8
combo                  0x81B355   u8        mult=1.785714 min=0 max=100 round=1
combo_p2               0x81B37F   u8        mult=1.785714 min=0 max=100 round=1
```

Propre au romset `ddpdojblk` :

```
lives                  0x8130BA   be        bytes=2
lives_p2               0x8130BC   be        bytes=2
bombs                  0x810406   u8
bombs_max              0x810407   u8
bombs_p2               0x810468   u8
bombs_max_p2           0x810469   u8
power                  0x810402   be        bytes=2 max=8
power_p2               0x810464   be        bytes=2 max=8
combo                  0x81B5B9   u8        mult=1.785714 min=0 max=100 round=1
combo_p2               0x81B5E3   u8        mult=1.785714 min=0 max=100 round=1
credits                0x80395A   u8
```

Propre au romset `ddpdojblka` :

```
lives                  0x8130BA   be        bytes=2
lives_p2               0x8130BC   be        bytes=2
bombs                  0x810406   u8
bombs_max              0x810407   u8
bombs_p2               0x810468   u8
bombs_max_p2           0x810469   u8
power                  0x810402   be        bytes=2 max=8
power_p2               0x810464   be        bytes=2 max=8
combo                  0x81B5B9   u8        mult=1.785714 min=0 max=100 round=1
combo_p2               0x81B5E3   u8        mult=1.785714 min=0 max=100 round=1
credits                0x80395A   u8
```

Propre au romset `ddpdojblkb` :

```
lives                  0x8130BA   be        bytes=2
lives_p2               0x8130BC   be        bytes=2
bombs                  0x810406   u8
bombs_max              0x810407   u8
bombs_p2               0x810468   u8
bombs_max_p2           0x810469   u8
power                  0x810402   be        bytes=2 max=8
power_p2               0x810464   be        bytes=2 max=8
combo                  0x81B5B9   u8        mult=1.785714 min=0 max=100 round=1
combo_p2               0x81B5E3   u8        mult=1.785714 min=0 max=100 round=1
credits                0x80395A   u8
```

Propre au romset `ddpdojblkbl` :

```
lives                  0x8130BA   be        bytes=2
lives_p2               0x8130BC   be        bytes=2
bombs                  0x810406   u8
bombs_max              0x810407   u8
bombs_p2               0x810468   u8
bombs_max_p2           0x810469   u8
power                  0x810402   be        bytes=2 max=8
power_p2               0x810464   be        bytes=2 max=8
combo                  0x81B5B9   u8        mult=1.785714 min=0 max=100 round=1
combo_p2               0x81B5E3   u8        mult=1.785714 min=0 max=100 round=1
credits                0x80395A   u8
```

Propre au romset `ddpdojp` :

```
lives                  0x813012   be        bytes=2
lives_p2               0x813014   be        bytes=2
bombs                  0x81036E   u8
bombs_p2               0x8103D0   u8
bombs_max              0x81036F   u8
bombs_max_p2           0x8103D1   u8
power                  -          be
power_p2               -          be
combo                  -          u8
combo_p2               -          u8
```

## ddpdfk — DoDonPachi Dai-Fukkatsu Ver 1.5

cpu :maincpu, ram_base 0xC000000, ram_size 0x600000, swap16 True

```
credits                0xC1E0D7F  u8
lives                  0xC5C3703  u8
lives_p2               0xC5C3A0F  u8
bombs                  0xC5C3706  u8
bombs_p2               0xC5C3A12  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `ddpdfk10` :

```
lives                  0xC5C23C3  u8
lives_p2               0xC5C26B7  u8
bombs                  0xC5C23C6  u8
bombs_p2               0xC5C26BA  u8
```

## ddpsdoj — DoDonPachi SaiDaiOuJou

cpu :maincpu, ram_base 0xC000000, ram_size 0x200000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## ddsom — Dungeons & Dragons: Shadow over Mystara

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8641   u8        mult=0.649351 min=0 max=100 zero_from="0xCD" round=1
health_p2              0xFF8841   u8        mult=0.649351 min=0 max=100 zero_from="0xCD" round=1
_time                  0xFFCAB2   bcd       bytes=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## ddtod — Dungeons & Dragons: Tower of Doom

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8719   u8        mult=0.625 min=0 max=100 zero_from="0xD0" round=1
health_p2              0xFF8819   u8        mult=0.625 min=0 max=100 zero_from="0xD0" round=1
_time                  0xFF8069   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
daggers                0xFF84A8   u8
```

Propre au romset `ddtodar1` :

```
_time                  0xFF8068   be        bytes=2
```

## deathsml — Deathsmiles

cpu :maincpu, ram_base 0xC000000, ram_size 0x400000, swap16 True

```
credits                0xC060B23  u8
energy                 0xC388F3A  be        bytes=2 mult=0.110988 min=0 max=100 zero_from="0x81C2" round=1
energy_p2              0xC38906A  be        bytes=2 mult=0.110988 min=0 max=100 zero_from="0x81C2" round=1
score                  0xC388F60  be        bytes=4
score_p2               0xC389090  be        bytes=4
```

## dfkbl — DoDonPachi Dai-Fukkatsu Black Label

cpu :maincpu, ram_base 0xC000000, ram_size 0x800000, swap16 True

```
credits                0xC1E0D7F  u8
lives                  0xC71742B  u8
lives_p2               0xC71774B  u8
bombs                  0xC71742E  u8
bombs_p2               0xC71774E  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## diggerma — Digger Man

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x102027   bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x102093   u8
energy                 0x102091   u8        max=160
bombs                  0x10219F   u8
lives_p2               0x1020AF   u8
energy_p2              0x1020AD   u8        max=160
bombs_p2               0x1021A1   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## dimahoo — Dimahoo

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
lives                  0x92804E   u8        mame_only=true
lives_p2               0x92814E   u8        mame_only=true
bombs                  0x92804F   u8        mame_only=true
_p1_chr                0x928055   u8        mame_only=true
_p2_chr                0x928155   u8        mame_only=true
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"SOLO-BANG","1":"KARTE","2":"MIYAMOTO","3":"GRIMLEN","4":"GAIN","5":"CHITTA","6":"BIRTHDAY","7":"GOLDEN"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"SOLO-BANG","1":"KARTE","2":"MIYAMOTO","3":"GRIMLEN","4":"GAIN","5":"CHITTA","6":"BIRTHDAY","7":"GOLDEN"}}`

## dino — Cadillacs and Dinosaurs

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFFB2E1   u8        mult=1.0 min=0 max=100 zero_from="0xB2" round=1
health_p2              0xFFB461   u8        mult=1.0 min=0 max=100 zero_from="0xB2" round=1
_time                  0xFF84E9   bcd       bytes=1
lives                  0xFFB317   u8
lives_p2               0xFFB497   u8
_p1_chr                0xFFB277   u8
_p2_chr                0xFFB3F7   u8
score                  0xFFB374   bcd       bytes=3 mult=100
score_p2               0xFFB4F4   bcd       bytes=3 mult=100
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"JACK.T","2":"HANNAH.D","1":"MUSTAPHA.C","3":"MESS.O"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"JACK.T","2":"HANNAH.D","1":"MUSTAPHA.C","3":"MESS.O"}}`

## donpachi — DonPachi

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0x10139B   u8
lives                  0x101A2F   u8
lives_p2               0x101A31   u8
bombs                  0x10217B   u8
bombs_p2               0x1021BB   u8
power                  0x102179   u8        max=4
power_p2               0x1021B9   u8        max=4
combo                  0x101743   u8        mult=3.225806 min=0 max=100 round=1
combo_p2               0x101761   u8        mult=3.225806 min=0 max=100 round=1
hits                   -          u8
stage                  0x101A41   u8        add=1
loop                   0x101A42   u16       bytes=2
score                  0x10177A   bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## doubledr — Double Dragon

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x100450   be        bytes=2 mult=-0.003756 add=100 min=0 max=100
health_p2              0x100550   be        bytes=2 mult=-0.003756 add=100 min=0 max=100
time                   0x102242   bcd       bytes=1
_time_sub              0x102243   u8        start=36
_fight_cue             0x101A0A   u8        start=0
score                  0x100452   bcd       bytes=4
score_p2               0x100552   bcd       bytes=4
_p1_chr                0x100445   u8
_p2_chr                0x100545   u8
_p1_dir                0x10042B   u8        mask=32
_p2_dir                0x10052B   u8        mask=32
backdrop               0x100545   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"BILLY","1":"S.BILLY","2":"JIMMY","3":"S.JIMMY","4":"MARIAN","5":"ABOBO","6":"AMON","7":"EDDIE","8":"REBECCA","9":"DULTON","10":"CHENG-FU","11":"BURNOV","12":"DUKE","13":"SHUKO"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"BILLY","1":"S.BILLY","2":"JIMMY","3":"S.JIMMY","4":"MARIAN","5":"ABOBO","6":"AMON","7":"EDDIE","8":"REBECCA","9":"DULTON","10":"CHENG-FU","11":"BURNOV","12":"DUKE","13":"SHUKO"}}`

## dragonsh — Dragon's Heaven

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## dsmbl — Deathsmiles MegaBlack Label

cpu :maincpu, ram_base 0xC000000, ram_size 0x700000, swap16 True

```
credits                0xC1E109F  u8
energy                 0xC66145E  be        bytes=2 mult=0.110988 min=0 max=100 zero_from="0x81C2" round=1
energy_p2              0xC6615BE  be        bytes=2 mult=0.110988 min=0 max=100 zero_from="0x81C2" round=1
score                  0xC661490  digits_le bytes=12
score_p2               0xC6615F0  digits_le bytes=12
```

## dstlk — Darkstalkers: The Night Warriors

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF83CB   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF87CB   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0xFF9409   bcd       bytes=1
_p1_chr                0xFF8729   u8
_p2_chr                0xFF8B29   u8
backdrop               0xFF9389   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"DIMITRI","2":"GALLON","3":"VICTOR","4":"ZABELZAROCH","5":"MORRIGAN","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"AULBATH","10":"SASQUATCH","11":"PHOBOS","12":"PYRON"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"DIMITRI","2":"GALLON","3":"VICTOR","4":"ZABELZAROCH","5":"MORRIGAN","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"AULBATH","10":"SASQUATCH","11":"PHOBOS","12":"PYRON"}}`

## dynwar — Dynasty Wars

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8288   be        bytes=2 mult=0.0407 min=0 max=100 zero_from="0x84CC" round=1
health_p2              0xFF8328   be        bytes=2 mult=0.0407 min=0 max=100 zero_from="0x84CC" round=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
level                  0xFF82EE   u8
```

## ecofghtr — Eco Fighters

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF02E8   u8
lives                  0xFFF5F2   u8
lives_p2               0xFFF5F3   u8
power                  0xFF8952   u8        max=5
weapon                 0xFF8904   u8
score                  0xFF88EA   bcd       bytes=4
score_p2               0xFF8EBA   bcd       bytes=4
```

Propre au romset `ecofghtru` :

```
credits                0xFF02EA   u8
```

`derived` :

- `weapon_name` = `{"value":"weapon","names":{"3":"ENERGY BALL","4":"HAMMER","7":"WHEEL","9":"LASER SWORD"}}`

## eightman — Eight Man

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x100CF0   bcd       bytes=4
score_p2               0x1011F0   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x100482   bcd       bytes=1
lives                  0x100CF7   u8        add=-1 min=0
energy                 0x100CF6   u8        max=6
bombs                  0x100CF5   u8
power8                 0x100CC2   u8
lives_p2               0x1011F7   u8        add=-1 min=0
energy_p2              0x1011F6   u8        max=6
bombs_p2               0x1011F5   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## espgal — Espgaluda

cpu :maincpu, ram_base 0x800000, ram_size 0x20000, swap16 True

```
credits                0x8011E8   u8
lives                  0x8139D7   u8
lives_p2               0x8139D9   u8
bombs_p2               0x80EF5A   u8
power                  0x80EEB6   be        bytes=2 max=8
power_p2               0x80EF56   be        bytes=2 max=8
stones                 0x80EF04   be        bytes=2 max=500
stones_p2              0x80EFA4   be        bytes=2 max=500
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## espgal2 — Espgaluda II

cpu :maincpu, ram_base 0xC000000, ram_size 0x400000, swap16 True

```
credits                0xC05EB57  u8
lives                  0xC37D6FF  u8
lives_p2               0xC37D7CF  u8
bombs                  0xC37D78A  u8
bombs_p2               0xC37D85A  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `espgal2a` :

```
credits                0xC05EB4B  u8
lives                  0xC37D6EF  u8
lives_p2               0xC37D7BF  u8
bombs                  0xC37D77A  u8
bombs_p2               0xC37D84A  u8
```

Propre au romset `espgal2b` :

```
credits                0xC05EB4B  u8
lives                  0xC37D6EF  u8
lives_p2               0xC37D7BF  u8
bombs                  0xC37D77A  u8
bombs_p2               0xC37D84A  u8
```

## esprade — ESP Ra.De. - A.D.2018 Tokyo

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0x101227   u8
lives                  0x10254F   u8
lives_p2               0x102551   u8
bombs                  0x102750   u8
bombs_p2               0x1027A0   u8
power                  0x10272B   u8        max=4
power_p2               0x10277B   u8        max=4
multiplier             0x1026FF   u8        add=1 max=16
stage                  0x1025A7   u8        add=1 max=5 mask=15
score                  0x1022E4   bcd       bytes=4 mult=10
score_p2               -          bcd       bytes=4
```

## fatfursp — Fatal Fury Special

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10049A   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
health_p2              0x10059A   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
_p1_chr                0x10045D   u8
_p2_chr                0x10055D   u8
_p1_dir                0x100469   u8
_p2_dir                0x100569   u8
time                   0x10092A   bcd       bytes=1
_time_sub              0x10092B   u8        start=60
_fight_cue             0x10F2D0   u8        start=66
score                  0x10E00C   bcd       bytes=4
score_p2               0x10E010   bcd       bytes=4
backdrop               0x10B2ED   u8
round                  0x10B2F1   u8        add=-1 min=0
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"BIG BEAR","5":"JUBEI","6":"CHENG","7":"KIM","8":"MAI","9":"DUCK KING","10":"TUNG","11":"BILLY","12":"AXEL"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"BIG BEAR","5":"JUBEI","6":"CHENG","7":"KIM","8":"MAI","9":"DUCK KING","10":"TUNG","11":"BILLY","12":"AXEL"}}`

## fatfury1 — Fatal Fury

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100445   u8
_p2_dir                0x100345   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x1003B8   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
_p2_hp                 0x1004B8   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
_cpu_hp                0x1005B8   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
time                   0x1042F3   bcd       bytes=1
_time_sub              0x1042F4   u8        start=30
_fight_cue             0x10767E   u8        start=0
score                  0x104308   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x100331   u8
_p2_chr                0x100431   u8
_cpu_chr               0x100531   u8
rounds                 0x1042E6   u8
rounds_p2              0x1042E7   u8
round                  0x100025   u8
_round_result          0x1042E3   u8
_sc2_a                 0x104408   bcd       bytes=4
_sc2_b                 0x10430C   bcd       bytes=4
_sc2_c                 0x104310   bcd       bytes=4
```

`tag` :

- `p2_mode` = `{"eq":["p2_mode",1]}`
- `health_p2` = `{"first":[{"pick":["_cpu_hp","_p2_hp"],"at":{"eq":["p2_mode",1]}},"_cpu_hp"]}`

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"DUCK KING","5":"RICHARD","6":"MICHAEL","7":"TUNG","8":"HWA","9":"RAIDEN","10":"BILLY","11":"GEESE","12":"MYER","13":"TUNG","14":"HWA"}}`
- `p2_char` = `{"pick":["_cpu_chr","_p2_chr"],"at":"p2_mode","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"DUCK KING","5":"RICHARD","6":"MICHAEL","7":"TUNG","8":"HWA","9":"RAIDEN","10":"BILLY","11":"GEESE","12":"MYER","13":"TUNG","14":"HWA"}}`

## fatfury2 — Fatal Fury 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100367   u8
_p2_dir                0x100467   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x1003CB   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
health_p2              0x1004CB   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
time                   0x10092A   bcd       bytes=1
_time_sub              0x10092B   u8        start=40
score                  0x10E00C   bcd       bytes=4
score_p2               0x10E010   bcd       bytes=4
backdrop               0x10AAD5   u8
_p1_chr                0x10419B   u8
_p2_chr                0x10419D   u8
round                  0x10AAD9   u8        add=-1 min=0
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"BIG BEAR","5":"JUBEI","6":"CHENG","7":"KIM","8":"MAI","9":"BILLY","10":"AXEL","11":"LAURENCE","12":"KRAUSER"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"BIG BEAR","5":"JUBEI","6":"CHENG","7":"KIM","8":"MAI","9":"BILLY","10":"AXEL","11":"LAURENCE","12":"KRAUSER"}}`

## fatfury3 — Fatal Fury 3

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100471   u8
_p2_dir                0x100571   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
_hp                    0x100489   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
_hp_vs                 0x100489   u8        mult=0.833333 add=0.4 min=0 max=100 zero_from="0xBC"
_hp_p2                 0x100589   u8        mult=1.041667 add=0.4 min=0 max=100 zero_from="0xB0"
_hp_p2_vs              0x100589   u8        mult=0.833333 add=0.4 min=0 max=100 zero_from="0xBC"
time                   0x105680   bcd       bytes=1
_fight_cue             0x105789   u8        start=96
score                  0x10E008   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10561D   u8
_p2_chr                0x10561F   u8
backdrop               0x105627   u8
rounds                 0x105666   u8
rounds_p2              0x105667   u8
```

`tag` :

- `health` = `{"pick":["_hp","_hp_vs"],"at":{"all":[{"eq":["p1_mode",1]},{"eq":["p2_mode",1]}]}}`
- `health_p2` = `{"pick":["_hp_p2","_hp_p2_vs"],"at":{"all":[{"eq":["p1_mode",1]},{"eq":["p2_mode",1]}]}}`

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"MAI","5":"GEESE","6":"SOKAKU","7":"BOB","8":"HON FU","9":"MARY","10":"FRANCO","11":"YAMAZAKI","12":"CHONREI","13":"CHONSHU"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"MAI","5":"GEESE","6":"SOKAKU","7":"BOB","8":"HON FU","9":"MARY","10":"FRANCO","11":"YAMAZAKI","12":"CHONREI","13":"CHONSHU"}}`

## fbfrenzy — Football Frenzy

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x104368   bcd       bytes=1
score_p2               0x104468   bcd       bytes=1
time_min               0x100AD8   bcd       bytes=1
time_sec               0x100AD9   bcd       bytes=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
time                   0x100AD8   bcd       bytes=1
```

## feversos — Fever SOS

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0x101731   u8
lives                  0x1052C5   u8
lives_p2               0x1052C7   u8
bombs                  0x105A3B   u8
round                  0x1052D9   u8        add=1
bombs_p2               0x105A7B   u8
power                  0x105A35   u8        max=6
power_p2               0x105A75   u8        max=6
ship                   0x105A36   u8
ship_p2                0x105A76   u8
mode                   0x105105   u8
score_p2               -          bcd       bytes=4
_score_s1              0x103FAE   bcd       bytes=4
_score_s2              0x103FB2   bcd       bytes=4
_score_s3              0x103FB6   bcd       bytes=4
_score_s4              0x103FBA   bcd       bytes=4
_score_s5              0x103FBE   bcd       bytes=4
```

`tag` :

- `score` = `{"sum":["_score_s1","_score_s2","_score_s3","_score_s4","_score_s5"]}`

`derived` :

- `p1_ship` = `{"value":"ship","names":{"0":"TYPE-A","8":"TYPE-B","16":"TYPE-C"}}`
- `p2_ship` = `{"value":"ship_p2","names":{"0":"TYPE-A","8":"TYPE-B","16":"TYPE-C"}}`

## ffex2u — Final Fight EX

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## ffight — Final Fight

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8581   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF8641   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0xFF80AF   bcd       bytes=1
credits                0xFF804D   u8
lives                  0xFF85E8   u8
lives_p2               0xFF86A8   u8
score                  0xFF85EC   bcd       bytes=4
score_p2               0xFF86AC   bcd       bytes=4
```

## ffightaec2 — Final Fight: Anniversary Edition

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## fightfev — Fight Fever

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x10C649   u8
_p2_dir                0x10C749   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10C602   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
health_p2              0x10C702   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
backdrop               0x108501   u8
time                   0x108110   bcd       bytes=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10C6B0   u8
_p2_chr                0x10C7B0   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAN","1":"MIYUKI","2":"ROPHEN","3":"GOLRIO","4":"NICK","5":"CHINTAO","6":"KIM","7":"MASTER","8":"MAGIC","9":"KARATE"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAN","1":"MIYUKI","2":"ROPHEN","3":"GOLRIO","4":"NICK","5":"CHINTAO","6":"KIM","7":"MASTER","8":"MAGIC","9":"KARATE"}}`

## flipshot — Battle Flip Shot

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x103787   bcd       bytes=3
score_p2               0x103793   bcd       bytes=3
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x1037AE   bcd       bytes=1
target1                0x1034B7   u8
target1_p2             0x103547   u8
target2                0x1034CF   u8
target2_p2             0x10355F   u8
target3                0x1034E7   u8
target3_p2             0x103577   u8
target4                0x1034FF   u8
target4_p2             0x10358F   u8
target5                0x103517   u8
target5_p2             0x1035A7   u8
target6                0x10352F   u8
target6_p2             0x1035BF   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## forgottn — Forgotten Worlds

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF9035   u8        mult=1.785714 min=0 max=100 zero_from="0x9C" round=1
health_p2              0xFF9055   u8        mult=1.785714 min=0 max=100 zero_from="0x9C" round=1
zenny                  0xFFE192   bcd       bytes=3
weapon                 0xFFCF18   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `weapon_name` = `{"value":"weapon","names":{"0":"LASER","2":"BEAM","4":"MISSILE","6":"BALCAN","8":"NAPALM","10":"V-CANNON","12":"BURNER","14":"MULTI-WAY"}}`

## froman2b — Idol Mahjong Final Romance 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## futari15 — Mushihime-Sama Futari Ver 1.5

cpu :maincpu, ram_base 0xC000000, ram_size 0x400000, swap16 True

```
credits                0xC0601E7  u8
lives                  0xC38AABF  u8
lives_p2               0xC38AB77  u8
bombs                  0xC38AAC2  u8
bombs_p2               0xC38AB7A  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `futari10` :

```
lives                  0xC3883DF  u8
lives_p2               0xC388497  u8
bombs                  0xC3883E2  u8
bombs_p2               0xC38849A  u8
```

Propre au romset `futari15a` :

```
lives                  0xC38AAAF  u8
lives_p2               0xC38AB67  u8
bombs                  0xC38AAB2  u8
bombs_p2               0xC38AB6A  u8
```

## futaribl — Mushihime-Sama Futari Black Label - Another Ver

cpu :maincpu, ram_base 0xC000000, ram_size 0x400000, swap16 True

```
credits                0xC0601E7  u8
lives                  0xC383E4F  u8
lives_p2               0xC383F1B  u8
bombs                  0xC383E52  u8
bombs_p2               0xC383F1E  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `futariblj` :

```
lives                  0xC383A1F  u8
lives_p2               0xC383AEB  u8
bombs                  0xC383A22  u8
bombs_p2               0xC383AEE  u8
```

## gaia — Gaia Crusaders

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
health                 0x1058C9   u8        mult=1.041667 min=0 max=100 zero_from="0xB0" round=1
health_p2              0x1059C9   u8        mult=1.041667 min=0 max=100 zero_from="0xB0" round=1
time                   0x105809   u8
credits                0x10257D   u8
lives                  0x1058C7   u8
lives_p2               0x1059C7   u8
stage                  0x105803   u8        add=1
score                  0x1058C2   be        bytes=4
```

## galaxyfg — Galaxy Fight

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10103C   u8        mult=0.392157 min=0 max=100
health_p2              0x101152   u8        mult=0.392157 min=0 max=100
_p1_chr                0x101001   u8
_p2_chr                0x101117   u8
_p1_dir                0x10100D   u8
_p2_dir                0x101123   u8
backdrop               0x101117   u8
time                   0x1051B1   u8        max=99
score                  0x101048   u32       mult=10
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"KAZUMA","1":"ROLF","2":"JURI","3":"ROOMI","4":"GUNTER","5":"ALVAN","6":"G. DONE","7":"MUSAFAR","8":"FELDEN","9":"YACOPU"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"KAZUMA","1":"ROLF","2":"JURI","3":"ROOMI","4":"GUNTER","5":"ALVAN","6":"G. DONE","7":"MUSAFAR","8":"FELDEN","9":"YACOPU"}}`

## ganryu — Ganryu

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1004A2   be        bytes=2
score_p2               0x1004C2   be        bytes=2
time                   0x100453   u8
lives                  0x1004A1   u8        add=-1 min=0
lives_p2               0x1004C1   u8        add=-1 min=0
energy                 0x100481   u8        max=10
energy_p2              0x100481   u8        max=10
_turn                  0x1004E7   u8
ammo                   0x100497   u8
ammo_p2                0x1004B7   u8
weapon                 0x100499   u8
weapon_p2              0x1004B9   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## garou — Garou

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100458   u8
_p2_dir                0x100558   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10048E   u8        mult=0.833333 add=0.4 min=0 max=100 zero_from="0xBC"
health_p2              0x10058E   u8        mult=0.833333 add=0.4 min=0 max=100 zero_from="0xBC"
rounds                 0x107477   u8
rounds_p2              0x107476   u8
time                   0x107490   bcd       bytes=1
_fight_cue             0x10748A   u8        start=54
score                  0x10E00C   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10742B   u8
_p2_chr                0x10742D   u8
backdrop               0x107435   u8
power                  0x1004BE   u8        mult=0.78125 min=0 max=100 round=1
power_p2               0x1005BE   u8        mult=0.78125 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"TERRY","1":"ROCK","2":"DONG HWAN","3":"JAE HOON","4":"HOTARU","5":"GATO","6":"BONNE","7":"BUTT","8":"HOKUTOMARU","9":"FREEMAN","10":"TIZOC","11":"KEVIN","12":"GRANT","13":"KAIN"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"TERRY","1":"ROCK","2":"DONG HWAN","3":"JAE HOON","4":"HOTARU","5":"GATO","6":"BONNE","7":"BUTT","8":"HOKUTOMARU","9":"FREEMAN","10":"TIZOC","11":"KEVIN","12":"GRANT","13":"KAIN"}}`

## ghostlop — Ghostlop

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x10C846   digits    bytes=2
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ghouls — Ghouls'n Ghosts

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_time                  0xFF06D3   bcd       bytes=1
lives                  0xFF07AD   u8
lives_p2               0xFF080D   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
armor                  0xFF07AA   u8
armor_kind             0xFF07AC   u8
weapon                 0xFF07C6   u8
```

`derived` :

- `_one` = `{"value":1}`

## gigawing — Giga Wing

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
lives                  0xFF72DD   u8
lives_p2               0xFF72DF   u8
bombs                  0xFF72E1   u8
_p1_chr                0xFF7309   u8
_p2_chr                0xFF7311   u8
credits                0xFF2095   bcd       bytes=1
power                  0xFF730D   u8        max=3
score                  0xFF70D0   bcd       bytes=4
score_p2               -          bcd       bytes=4
bombs_p2               0xFF72E3   u8
power_p2               0xFF7315   u8        max=3
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"SINNOSUKE","1":"RUBY","2":"ISHA","3":"STUCK","4":"STRANGER"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"SINNOSUKE","1":"RUBY","2":"ISHA","3":"STUCK","4":"STRANGER"}}`

## goalx3 — Goal! Goal! Goal!

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
goals                  0x1004F1   u8
goals_p2               0x1004F3   u8
_time_min              0x1004E2   u8        mult=60
_time_sec              0x1004E3   digits    bytes=2
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `time` = `{"sum":["_time_min","_time_sec"]}`

## gowcaizr — Voltage Fighter Gowcaizer

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100186   u8        mask="0x80"
_p2_dir                0x100187   u8        mask="0x80"
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x102D09   u8        mult=1.0 add=0.4 min=0 max=100 zero_from="0xB2"
health_p2              0x1035BF   u8        mult=1.0 add=0.4 min=0 max=100 zero_from="0xB2"
backdrop               0x1044D2   u8
time                   0x1062E1   u8        max=99
_time_sub              0x1062E5   u8        start=60
_fight_cue             0x1007B4   u8        start=0
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10464D   u8
_p2_chr                0x10467D   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"GOWCAIZER","1":"CAPTAIN","2":"KARIN","3":"FUDOMARU","4":"MARION","5":"SHAIA","6":"SHENLONG","7":"KYOSUKE","8":"STINGER","9":"BRIDER","10":"PLATONIC","11":"OHGA"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"GOWCAIZER","1":"CAPTAIN","2":"KARIN","3":"FUDOMARU","4":"MARION","5":"SHAIA","6":"SHENLONG","7":"KYOSUKE","8":"STINGER","9":"BRIDER","10":"PLATONIC","11":"OHGA"}}`

## gpilots — Ghost Pilots

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x103F31   bcd       bytes=3 mult=100
score_p2               0x103FB1   bcd       bytes=3 mult=100
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x103F37   u8        add=-1 min=0
lives_p2               0x103FB7   u8        add=-1 min=0
bombs                  0x103F40   u8
bombs_p2               0x103FC0   u8
stars                  0x103F44   bcd       bytes=1
stars_p2               0x103FC4   bcd       bytes=1
power                  0x103F3D   u8        max=28
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## gulunpa — Gulun.Pa!

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## gururin — Gururin

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
level                  0x101C5D   u8
cur_l                  0x101D03   u8
cur_l_p2               0x101F03   u8
cur_c                  0x101D23   u8
cur_c_p2               0x101F23   u8
cur_r                  0x101D43   u8
cur_r_p2               0x101F43   u8
next_l                 0x101D63   u8
next_l_p2              0x101F63   u8
next_c                 0x101D83   u8
next_c_p2              0x101F83   u8
next_r                 0x101DA3   u8
next_r_p2              0x101FA3   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## guwange — Guwange

cpu :maincpu, ram_base 0x200000, ram_size 0x10000, swap16 True

```
credits                0x201011   u8
bombs                  0x2028F9   u8
bombs_p2               0x202959   u8
power                  0x2028FB   u8        max=14
power_p2               0x20295B   u8        max=14
combo                  0x20289D   u8        mult=10.0 min=0 max=100 round=1
combo_p2               0x20290D   u8        mult=10.0 min=0 max=100 round=1
energy                 0x2026DA   u8        mult=2.777778 min=0 max=100 round=1
energy_p2              0x2026E0   u8        mult=2.777778 min=0 max=100 round=1
char                   0x2028E4   u8
char_p2                0x202944   u8
lives                  -          u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `guwanges` :

```
credits                0x20101B   u8
bombs                  0x202905   u8
bombs_p2               0x202965   u8
power                  0x202907   u8        max=14
power_p2               0x202967   u8        max=14
combo                  0x2028A9   u8        mult=10.0 min=0 max=100 round=1
combo_p2               0x202909   u8        mult=10.0 min=0 max=100 round=1
energy                 0x2026E6   u8        mult=2.777778 min=0 max=100 round=1
energy_p2              0x2026EC   u8        mult=2.777778 min=0 max=100 round=1
char                   0x2028F0   u8
char_p2                0x202950   u8
```

`derived` :

- `p1_char` = `{"value":"char","names":{"0":"SISIN","1":"KOSAME","2":"GENSUKE"}}`
- `p2_char` = `{"value":"char_p2","names":{"0":"SISIN","1":"KOSAME","2":"GENSUKE"}}`

## hotdogst — Hotdog Storm - The First Supersonics

cpu :maincpu, ram_base 0x300000, ram_size 0x10000, swap16 True

```
credits                0x3010A9   u8
lives                  0x3010ED   u8
lives_p2               0x3010EF   u8
bombs                  0x3010F1   u8
bombs_p2               0x3010F3   u8
power                  0x3011ED   u8        max=3
power_p2               0x3011EF   u8        max=3
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## hsf2 — Hyper Street Fighter II: The Anniversary Edition

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8367   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF8767   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0xFF8BFC   bcd       bytes=1
credits                0xFF830A   u8
power                  0xFF85F0   u8        mult=2.083333 min=0 max=100 round=1
power_p2               0xFF89F0   u8        mult=2.083333 min=0 max=100 round=1
_p1_chr                0xFF8667   u8
_p2_chr                0xFF8A67   u8
score                  0xFF8658   bcd       bytes=4
score_p2               0xFF8A58   bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN-LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA","12":"CAMMY","13":"T. HAWK","14":"FEI LONG","1…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN-LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA","12":"CAMMY","13":"T. HAWK","14":"FEI LONG","1…`

## ibara — Ibara

cpu :maincpu, ram_base 0xC000000, ram_size 0x300000, swap16 True

```
credits                0xC26C878  u8
lives                  0xC2839E7  u8
lives_p2               0xC283C67  u8
bombs                  0xC2839EA  u8
bombs_p2               0xC283C6A  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `ibarao` :

```
credits                0xC26C8A8  u8
lives                  0xC283A17  u8
lives_p2               0xC283C97  u8
bombs                  0xC283A1A  u8
bombs_p2               0xC283C9A  u8
```

## ibarablk — Ibara Kuro Black Label

cpu :maincpu, ram_base 0xC000000, ram_size 0x300000, swap16 True

```
credits                0xC2860B0  u8
lives                  0xC29D432  u8
lives_p2               0xC29D6D2  u8
bombs_p2               0xC29D6D5  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `ibarablka` :

```
credits                0xC2860C0  u8
lives                  0xC29D442  u8
lives_p2               0xC29D6E2  u8
bombs_p2               0xC29D6E5  u8
```

## ironclad — Choutetsu Brikin'ger

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x108A2A   bcd       bytes=4
score_p2               0x108C2A   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
energy                 0x10027D   u8        max=3
power                  0x108A15   u8        max=12
level                  0x108A17   u8        add=1 max=32
l_arm                  0x108A55   u8
r_arm                  0x108A71   u8
energy_p2              0x101F7D   u8        max=3
power_p2               0x108C15   u8        max=12
level_p2               0x108C17   u8        add=1 max=32
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## irrmaze — The Irritating Maze

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
time_sec               0x10A857   u8
time_tenths            0x10A859   u8
lives                  0x10808F   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
time                   0x10A857   u8
```

## janshin — Janshin Densetsu

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
time                   0x108418   u8
hp                     0x104C68   bcd       bytes=2
mp                     0x104C6A   bcd       bytes=2
weapon                 0x104C76   u8
shield                 0x104C78   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## jockeygp — Jockey Grand Prix

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## jojo — JoJo's Venture

cpu :maincpu, ram_base 0x2000000, ram_size 0x80000, swap32 True

```
health                 0x20305AD  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0x20309B5  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0x202D0B0  u8
credits                0x206B850  u8
power                  0x2030443  u8        mult=10.0 min=0 max=100 round=1
power_p2               0x2030467  u8        mult=10.0 min=0 max=100 round=1
_p1_chr                0x203047F  u8
_p2_chr                0x2030887  u8
```

Propre au romset `jojojr2` :

```
health                 0x2030589  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0x2030991  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0x202D098  u8
credits                0x2068CAC  u8
power                  0x203041F  u8        mult=10.0 min=0 max=100 round=1
power_p2               0x2030443  u8        mult=10.0 min=0 max=100 round=1
```

Propre au romset `jojonr2` :

```
health                 0x2030589  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0x2030991  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0x202D098  u8
credits                0x2068CAC  u8
power                  0x203041F  u8        mult=10.0 min=0 max=100 round=1
power_p2               0x2030443  u8        mult=10.0 min=0 max=100 round=1
```

Propre au romset `jojor2` :

```
health                 0x2030589  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0x2030991  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0x202D098  u8
credits                0x2068CAC  u8
power                  0x203041F  u8        mult=10.0 min=0 max=100 round=1
power_p2               0x2030443  u8        mult=10.0 min=0 max=100 round=1
```

Propre au romset `jojour2` :

```
health                 0x2030589  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0x2030991  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
credits                0x2068CAC  u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"JOUTARO","1":"KAKYOUIN","2":"AVDOL","3":"POLNAREFF","4":"J.JOSTER","5":"IGGI","6":"ALESSY","7":"CHACA","8":"D'BO","9":"N'DOUL","10":"MIDLER","11":"DIO","12":"VANILLA ICE","13":"DEATH 13","14":"J.K…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"JOUTARO","1":"KAKYOUIN","2":"AVDOL","3":"POLNAREFF","4":"J.JOSTER","5":"IGGI","6":"ALESSY","7":"CHACA","8":"D'BO","9":"N'DOUL","10":"MIDLER","11":"DIO","12":"VANILLA ICE","13":"DEATH 13","14":"J.K…`

## jojoba — JoJo's Bizarre Adventure

cpu :maincpu, ram_base 0x2000000, ram_size 0x80000, swap32 True

```
health                 0x20349CD  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0x2034DED  u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p1_ctl                0x2034A18  u8        human=0
_p2_ctl                0x2034E38  u8        human=0
time                   0x20314B4  u8
credits                0x20713A8  u8
power                  0x2034862  be        bytes=2 mult=0.003755 min=0 max=100 round=1
power_p2               0x2034886  be        bytes=2 mult=0.003755 min=0 max=100 round=1
_p1_chr                0x203489F  u8
_p2_chr                0x2034CBF  u8
score                  0x20349EC  bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"JOUTARO","1":"KAKYOUIN","2":"AVDOL","3":"POLNAREFF","4":"J.JOSTER","5":"IGGI","6":"ALESSY","7":"CHACA","8":"D'BO","9":"N'DOUL","10":"MIDLER","11":"DIO","12":"VANILLA ICE","13":"DEATH 13","14":"J.K…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"JOUTARO","1":"KAKYOUIN","2":"AVDOL","3":"POLNAREFF","4":"J.JOSTER","5":"IGGI","6":"ALESSY","7":"CHACA","8":"D'BO","9":"N'DOUL","10":"MIDLER","11":"DIO","12":"VANILLA ICE","13":"DEATH 13","14":"J.K…`

## joyjoy — Puzzled

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
balloons               0x100904   u8
balloons_p2            0x100C14   u8
next                   0x100673   u8
next_p2                0x100983   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## kabukikl — Kabuki Klash

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_chr                0x1050B8   u8
_p2_chr                0x1050B9   u8
backdrop               0x1050B9   u8
power                  0x6E       u8        mult=1.666667 min=0 max=100 round=1 ptr="0x105094" ptr_range=["0x100000","0x10FFFF"]
power_p2               0x6E       u8        mult=1.666667 min=0 max=100 round=1 ptr="0x105098" ptr_range=["0x100000","0x10FFFF"]
health                 0x56       u8        mult=1.0 min=0 max=100 zero_from="0xB2" ptr="0x105094" ptr_range=["0x100000","0x10FFFF"]
health_p2              0x56       u8        mult=1.0 min=0 max=100 zero_from="0xB2" ptr="0x105098" ptr_range=["0x100000","0x10FFFF"]
rounds                 0x1050E8   u8
rounds_p2              0x1050E9   u8
time                   0x1060DA   bcd       bytes=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"MANJIMARU","1":"GOKURAKU","2":"TSUNADE","3":"OROCHIMARU","4":"YAGUMO","5":"ZIRIA","6":"KABUKI","7":"KINU","8":"MANTO","9":"KARAKURI","10":"JYASHINSAI","11":"LUCIFELLER"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"MANJIMARU","1":"GOKURAKU","2":"TSUNADE","3":"OROCHIMARU","4":"YAGUMO","5":"ZIRIA","6":"KABUKI","7":"KINU","8":"MANTO","9":"KARAKURI","10":"JYASHINSAI","11":"LUCIFELLER"}}`

## karnovr — Karnov's Revenge

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x103691   u8        mask="0xBF"
_p2_dir                0x103891   u8        mask="0xBF"
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x1037B3   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
health_p2              0x1039B3   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
score                  0x10367C   u32
score_p2               -          bcd       bytes=4
_p1_chr                0x103671   u8
_p2_chr                0x103871   u8
time                   0x103A70   u8
_time_sub              0x103A71   u8        start=32
_fight_cue             0x103A72   u8        start=2
rounds                 0x103677   u8
rounds_p2              0x103877   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RAY","1":"FEILIN","2":"RYOKO","3":"MATLOCK","4":"SAMCHAY","5":"LEE","6":"MIZOGUCHI","7":"JEAN","8":"MARSTORIUS","9":"YUNGMIE","10":"ZAZIE","11":"CLOWN","12":"KARNOV","13":"BULL"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RAY","1":"FEILIN","2":"RYOKO","3":"MATLOCK","4":"SAMCHAY","5":"LEE","6":"MIZOGUCHI","7":"JEAN","8":"MARSTORIUS","9":"YUNGMIE","10":"ZAZIE","11":"CLOWN","12":"KARNOV","13":"BULL"}}`

## ket — Ketsui: Kizuna Jigoku Tachi

cpu :maincpu, ram_base 0x800000, ram_size 0x20000, swap16 True

```
credits                0x801160   u8
lives                  0x812472   be        bytes=2
lives_p2               0x812474   be        bytes=2
bombs                  0x80FEC6   be        bytes=2
bombs_p2               0x80FF36   be        bytes=2
power                  0x80FEC2   be        bytes=2 max=8
power_p2               0x80FF32   be        bytes=2 max=8
combo                  0x81BB91   u8        mult=1.785714 min=0 max=100 round=1
combo_p2               0x81BC01   u8        mult=1.785714 min=0 max=100 round=1
score_p2               -          bcd       bytes=4
_score_hi              0x81A642   be        bytes=2 mult=65536
_score_lo              0x81A640   be        bytes=2
```

`tag` :

- `score` = `{"sum":["_score_hi","_score_lo"]}`

## kf2k3pcb — The King of Fighters 2003 (Japan, JAMMA PCB)

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
time                   0x107D62   bcd       bytes=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

## kizuna — Kizuna Encounter

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108313   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
health_p2              0x108513   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
_p1_chr                0x10821F   u8        mask=127
_p2_chr                0x10841F   u8        mask=127
_p1_dir                0x10820F   u8
_p2_dir                0x10840F   u8
backdrop               0x109659   u8
time                   0x10892A   bcd       bytes=1
_time_sub              0x10892D   u8        start=120
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAYATE","1":"EAGLE","2":"GOZU","3":"MEZU","4":"ROSA","5":"KIM","6":"JOKER","7":"CHUNG","8":"GORDON","9":"KING LION","10":"SHIN KING LION","11":"CHUNG","12":"JYAZU"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAYATE","1":"EAGLE","2":"GOZU","3":"MEZU","4":"ROSA","5":"KIM","6":"JOKER","7":"CHUNG","8":"GORDON","9":"KING LION","10":"SHIN KING LION","11":"CHUNG","12":"JYAZU"}}`

## knights — Knights of the Round

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFFABA5   u8        mult=1.25 min=0 max=100 zero_from="0xA8" round=1
health_p2              0xFFACC5   u8        mult=1.25 min=0 max=100 zero_from="0xA8" round=1
_time                  0xFFE7DA   bcd       bytes=1
lives                  0xFFAC76   u8
lives_p2               0xFFAD96   u8
score                  0xFFAC8C   bcd       bytes=4
score_p2               -          bcd       bytes=4
level                  0xFFAC4E   u8        add=1
```

## kod — The King of Dragons

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF129B   u8        mult=1.010101 min=0 max=100 zero_from="0xB1" round=1
health_p2              0xFF139B   u8        mult=1.010101 min=0 max=100 zero_from="0xB1" round=1
_time                  0xFFE084   u8
lives                  0xFF125D   u8
lives_p2               0xFF135D   u8
score                  0xFF12C2   bcd       bytes=4
score_p2               0xFF13C2   bcd       bytes=4
level                  0xFF12A2   u8        add=1
weapon                 0xFF12A3   u8
shield                 0xFF12A4   u8
```

## kof2000 — The King of Fighters 2000

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_p1_dir                0x108131   u8
_p2_dir                0x108331   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108239   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A7E6   bcd       bytes=1
_time_sub              0x10A7E7   u8        start=50
_fight_cue             0x10E4B2   u8        start=115
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_lost               0x10A7F9   u8
_p1_ch0                0x10A7FA   u8
_p1_ch1                0x10A7FB   u8
_p1_ch2                0x10A7FC   u8
_p1_ch3                0x10A7FD   u8
_p1_ord0               0x10A802   u8
_p1_ord1               0x10A803   u8
_p1_ord2               0x10A804   u8
_p2_lost               0x10A80E   u8
_p2_ch0                0x10A80F   u8
_p2_ch1                0x10A810   u8
_p2_ch2                0x10A811   u8
_p2_ch3                0x10A812   u8
_p2_ord0               0x10A817   u8
_p2_ord1               0x10A818   u8
_p2_ord2               0x10A819   u8
round                  0x10A7B6   u8
backdrop               0x10A7AE   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

`derived` :

- `p1_char` = `{"pick":["_p1_ch0","_p1_ch1","_p1_ch2","_p1_ch3"],"at":{"pick":["_p1_ord0","_p1_ord1","_p1_ord2"],"at":"_p1_lost"},"names":{"0":"K'","1":"MAXIMA","2":"BENIMARU","3":"SHINGO","4":"TERRY","5":"ANDY","6":"JOE","7":"MAI","8":"RYO","9…`
- `p2_char` = `{"pick":["_p2_ch0","_p2_ch1","_p2_ch2","_p2_ch3"],"at":{"pick":["_p2_ord0","_p2_ord1","_p2_ord2"],"at":"_p2_lost"},"names":{"0":"K'","1":"MAXIMA","2":"BENIMARU","3":"SHINGO","4":"TERRY","5":"ANDY","6":"JOE","7":"MAI","8":"RYO","9…`

## kof2001 — The King of Fighters 2001

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108239   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A7D2   bcd       bytes=1
_time_sub              0x10A7D3   u8        start=50
_fight_cue             0x10A781   u8        start=96
score                  0x1081FC   bcd       bytes=4
score_p2               0x1083FC   bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_lost               0x10A7E5   u8
_p1_cur                0x108171   u8
_p1_seq0               0x10A7EE   u8
_p1_seq1               0x10A7EF   u8
_p1_seq2               0x10A7F0   u8
_p2_lost               0x10A80B   u8
_p2_cur                0x108371   u8
_p2_seq0               0x10A814   u8
_p2_seq1               0x10A815   u8
_p2_seq2               0x10A816   u8
backdrop               0x10A79A   u8
_p1_dir                0x108131   u8
_p2_dir                0x108331   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

`derived` :

- `p1_char` = `{"value":"_p1_cur","names":{"0":"K'","1":"MAXIMA","2":"WHIP","3":"LIN","4":"KYO","5":"BENIMARU","6":"DAIMON","7":"SHINGO","8":"IORI","9":"VANESSA","10":"SETH","11":"RAMON","12":"LEONA","13":"RALF","14":"CLARK","15":"HEIDERN","16"…`
- `p2_char` = `{"value":"_p2_cur","names":{"0":"K'","1":"MAXIMA","2":"WHIP","3":"LIN","4":"KYO","5":"BENIMARU","6":"DAIMON","7":"SHINGO","8":"IORI","9":"VANESSA","10":"SETH","11":"RAMON","12":"LEONA","13":"RALF","14":"CLARK","15":"HEIDERN","16"…`
- `round` = `{"sum":["_p1_lost","_p2_lost"]}`

## kof2002 — The King of Fighters 2002

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108239   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A7D2   bcd       bytes=1
_fight_cue             0x10E22E   u8        start=0
score                  0x1081FC   bcd       bytes=4
score_p2               0x1083FC   bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
backdrop               0x10A79A   u8
_screen                0x10858A   u8
_p1_lost               0x10A7E5   u8
_p1_ch0                0x10A7E6   u8
_p1_ch1                0x10A7E7   u8
_p1_ch2                0x10A7E8   u8
_p1_cur                0x108171   u8
_p2_lost               0x10A80B   u8
_p2_ch0                0x10A80C   u8
_p2_ch1                0x10A80D   u8
_p2_ch2                0x10A80E   u8
_p2_cur                0x108371   u8
_p1_seq0               0x10A7EE   u8
_p1_seq1               0x10A7EF   u8
_p1_seq2               0x10A7F0   u8
_p2_seq0               0x10A814   u8
_p2_seq1               0x10A815   u8
_p2_seq2               0x10A816   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_fight_state           0x10A786   u8
power                  0x1081E8   u8        mult=1.5625 min=0 max=100
power_p2               0x1083E8   u8        mult=1.5625 min=0 max=100
power_level            0x1082E3   u8        max=3
power_level_p2         0x1084E3   u8        max=3
_pow                   0x1081E8   u8
_pow_p2                0x1083E8   u8
_stock                 0x1082E3   u8
_stock_p2              0x1084E3   u8
_maxv                  0x1081EA   u8
_maxv_p2               0x1083EA   u8
_dm                    0x1081E2   u8
_dm_p2                 0x1083E2   u8
```

`derived` :

- `select` = `{"sum":[{"eq":["_screen",35]},{"eq":["_screen",47]}]}`
- `p1_char` = `{"value":"_p1_cur","names":{"0":"KYO","1":"BENIMARU","2":"DAIMON","3":"TERRY","4":"ANDY","5":"JOE","6":"KIM","7":"CHANG","8":"CHOI","9":"ATHENA","10":"KENSOU","11":"CHIN","12":"LEONA","13":"RALF","14":"CLARK","15":"RYO","16":"ROB…`
- `p2_char` = `{"value":"_p2_cur","names":{"0":"KYO","1":"BENIMARU","2":"DAIMON","3":"TERRY","4":"ANDY","5":"JOE","6":"KIM","7":"CHANG","8":"CHOI","9":"ATHENA","10":"KENSOU","11":"CHIN","12":"LEONA","13":"RALF","14":"CLARK","15":"RYO","16":"ROB…`
- `round` = `{"sum":["_p1_lost","_p2_lost"]}`

## kof2003 — The King of Fighters 2003

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
time                   0x107D62   bcd       bytes=1
_time_sub              0x107D63   u8
score                  0x107808   bcd       bytes=4
score_p2               -          bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_ch0                0x107D12   u8        mask=63
_p1_ch1                0x107D13   u8        mask=63
_p1_ch2                0x107D14   u8        mask=63
_p1_act                0x107D1A   u8
_p2_ch0                0x107D15   u8        mask=63
_p2_ch1                0x107D16   u8        mask=63
_p2_ch2                0x107D17   u8        mask=63
_p2_act                0x107D1B   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

`derived` :

- `p1_char` = `{"pick":["_p1_ch0","_p1_ch1","_p1_ch2"],"at":"_p1_act","names":{"0":"ASH","1":"DUOLON","2":"SHEN","3":"TERRY","4":"JOE","5":"TIZOC","6":"RYO","7":"ROBERT","8":"YURI","9":"KIM","10":"CHANG","11":"JHUN","12":"LEONA","13":"RALF","14…`
- `p2_char` = `{"pick":["_p2_ch0","_p2_ch1","_p2_ch2"],"at":"_p2_act","names":{"0":"ASH","1":"DUOLON","2":"SHEN","3":"TERRY","4":"JOE","5":"TIZOC","6":"RYO","7":"ROBERT","8":"YURI","9":"KIM","10":"CHANG","11":"JHUN","12":"LEONA","13":"RALF","14…`

## kof94 — The King of Fighters '94

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108221   u8        mult=0.483092 min=0 max=100 zero_from="0xE7"
health_p2              0x108421   u8        mult=0.483092 min=0 max=100 zero_from="0xE7"
time                   0x10882E   bcd       bytes=1
_time_sub              0x10882F   u8        start=50
score                  0x10C6EC   bcd       bytes=4
score_p2               -          bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_chr                0x108171   u8
_p2_chr                0x108371   u8
backdrop               0x1087E0   u8
power                  0x108219   u8        mult=0.7874 min=0 max=100 round=1
power_p2               0x108419   u8        mult=0.7874 min=0 max=100 round=1
_p1_dir                0x108131   u8
_p2_dir                0x108331   u8
_screen                0x108586   u16
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

`derived` :

- `select` = `{"eq":["_screen",28742]}`
- `p1_char` = `{"value":"_p1_chr","names":{"0":"HEIDERN","1":"RALF","2":"CLARK","3":"ATHENA","4":"KENSOU","5":"CHIN","6":"KYO","7":"BENIMARU","8":"DAIMON","9":"HEAVY D!","10":"LUCKY","11":"BRIAN","12":"KIM","13":"CHANG","14":"CHOI","15":"TERRY"…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HEIDERN","1":"RALF","2":"CLARK","3":"ATHENA","4":"KENSOU","5":"CHIN","6":"KYO","7":"BENIMARU","8":"DAIMON","9":"HEAVY D!","10":"LUCKY","11":"BRIAN","12":"KIM","13":"CHANG","14":"CHOI","15":"TERRY"…`

## kof95 — The King of Fighters '95

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108221   u8        mult=0.483092 min=0 max=100 zero_from="0xE7"
health_p2              0x108421   u8        mult=0.483092 min=0 max=100 zero_from="0xE7"
time                   0x10A836   bcd       bytes=1
_time_sub              0x10A837   u8        start=50
_fight_cue             0x10DE19   u8        start=32
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_lost               0x10A842   u8
_p1_ch0                0x10A843   u8
_p1_ch1                0x10A844   u8
_p1_ch2                0x10A845   u8
_p1_ord0               0x10A849   u8
_p1_ord1               0x10A84A   u8
_p1_ord2               0x10A84B   u8
_p2_lost               0x10A852   u8
_p2_ch0                0x10A853   u8
_p2_ch1                0x10A854   u8
_p2_ch2                0x10A855   u8
_p2_ord0               0x10A859   u8
_p2_ord1               0x10A85A   u8
_p2_ord2               0x10A85B   u8
backdrop               0x10A7E8   u8
power                  0x108219   u8        mult=0.7874 min=0 max=100 round=1
power_p2               0x108419   u8        mult=0.7874 min=0 max=100 round=1
_p1_dir                0x108131   u8
_p2_dir                0x108331   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

`derived` :

- `p1_char` = `{"pick":["_p1_ch0","_p1_ch1","_p1_ch2"],"at":{"pick":["_p1_ord0","_p1_ord1","_p1_ord2"],"at":"_p1_lost"},"names":{"0":"HEIDERN","1":"RALF","2":"CLARK","3":"ATHENA","4":"KENSOU","5":"CHIN","6":"KYO","7":"BENIMARU","8":"DAIMON","9"…`
- `p2_char` = `{"pick":["_p2_ch0","_p2_ch1","_p2_ch2"],"at":{"pick":["_p2_ord0","_p2_ord1","_p2_ord2"],"at":"_p2_lost"},"names":{"0":"HEIDERN","1":"RALF","2":"CLARK","3":"ATHENA","4":"KENSOU","5":"CHIN","6":"KYO","7":"BENIMARU","8":"DAIMON","9"…`

## kof96 — The King of Fighters '96

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_p1_dir                0x108131   u8
_p2_dir                0x108331   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108239   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A836   bcd       bytes=1
_time_sub              0x10A837   u8        start=50
score                  0x1081FC   bcd       bytes=4
score_p2               0x1083FC   bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_lost               0x10A845   u8
_p1_ch0                0x10A846   u8
_p1_ch1                0x10A847   u8
_p1_ch2                0x10A848   u8
_p1_ord0               0x10A84C   u8
_p1_ord1               0x10A84D   u8
_p1_ord2               0x10A84E   u8
_p2_lost               0x10A856   u8
_p2_ch0                0x10A857   u8
_p2_ch1                0x10A858   u8
_p2_ch2                0x10A859   u8
_p2_ord0               0x10A85D   u8
_p2_ord1               0x10A85E   u8
_p2_ord2               0x10A85F   u8
round                  0x10A7ED   u8
backdrop               0x10A7E8   u8
power                  0x1081E8   u8        mult=0.78125 min=0 max=100 round=1
power_p2               0x1083E8   u8        mult=0.78125 min=0 max=100 round=1
_screen                0x108502   u16
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

`derived` :

- `p1_char` = `{"pick":["_p1_ch0","_p1_ch1","_p1_ch2"],"at":{"pick":["_p1_ord0","_p1_ord1","_p1_ord2"],"at":"_p1_lost"},"names":{"0":"KYO","1":"BENIMARU","2":"DAIMON","3":"TERRY","4":"ANDY","5":"JOE","6":"RYO","7":"ROBERT","8":"YURI","9":"LEONA…`
- `p2_char` = `{"pick":["_p2_ch0","_p2_ch1","_p2_ch2"],"at":{"pick":["_p2_ord0","_p2_ord1","_p2_ord2"],"at":"_p2_lost"},"names":{"0":"KYO","1":"BENIMARU","2":"DAIMON","3":"TERRY","4":"ANDY","5":"JOE","6":"RYO","7":"ROBERT","8":"YURI","9":"LEONA…`
- `select` = `{"eq":["_screen",47998]}`

## kof97 — The King of Fighters '97

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108239   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A83A   bcd       bytes=1
_time_sub              0x10A83B   u8
_fight_state           0x10A786   u8
score                  0x1081FC   bcd       bytes=4
score_p2               0x1083FC   bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_lost               0x10A84A   u8
_p1_ch0                0x10A84B   u8
_p1_ch1                0x10A84C   u8
_p1_ch2                0x10A84D   u8
_p1_ord0               0x10A851   u8
_p1_ord1               0x10A852   u8
_p1_ord2               0x10A853   u8
_p2_lost               0x10A85B   u8
_p2_ch0                0x10A85C   u8
_p2_ch1                0x10A85D   u8
_p2_ch2                0x10A85E   u8
_p2_ord0               0x10A862   u8
_p2_ord1               0x10A863   u8
_p2_ord2               0x10A864   u8
round                  0x10A7F1   u8
backdrop               0x10A7EA   u8
_pow                   0x1081E8   u8
_pow_p2                0x1083E8   u8
_stock                 0x1082E3   u8
_stock_p2              0x1084E3   u8
_maxv                  0x1081EA   u8
_maxv_p2               0x1083EA   u8
_pmode                 0x10A849   u8
_pmode_p2              0x10A85A   u8
_dm                    0x1081E2   u8
_dm_p2                 0x1083E2   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

`derived` :

- `p1_char` = `{"pick":["_p1_ch0","_p1_ch1","_p1_ch2"],"at":{"pick":["_p1_ord0","_p1_ord1","_p1_ord2"],"at":"_p1_lost"},"names":{"0":"KYO","1":"BENIMARU","2":"DAIMON","3":"TERRY","4":"ANDY","5":"JOE","6":"RYO","7":"ROBERT","8":"YURI","9":"LEONA…`
- `p2_char` = `{"pick":["_p2_ch0","_p2_ch1","_p2_ch2"],"at":{"pick":["_p2_ord0","_p2_ord1","_p2_ord2"],"at":"_p2_lost"},"names":{"0":"KYO","1":"BENIMARU","2":"DAIMON","3":"TERRY","4":"ANDY","5":"JOE","6":"RYO","7":"ROBERT","8":"YURI","9":"LEONA…`

## kof98 — The King of Fighters '98

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108239   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A83A   bcd       bytes=1
_time_sub              0x10A83B   u8
_fight_state           0x10A786   u8
score                  0x1081FC   bcd       bytes=4
score_p2               0x1083FC   bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_lost               0x10A84D   u8
_p1_ch0                0x10A84E   u8
_p1_ch1                0x10A84F   u8
_p1_ch2                0x10A850   u8
_p1_ord0               0x10A854   u8
_p1_ord1               0x10A855   u8
_p1_ord2               0x10A856   u8
_p2_lost               0x10A85E   u8
_p2_ch0                0x10A85F   u8
_p2_ch1                0x10A860   u8
_p2_ch2                0x10A861   u8
_p2_ord0               0x10A865   u8
_p2_ord1               0x10A866   u8
_p2_ord2               0x10A867   u8
round                  0x10A7F1   u8
backdrop               0x10A7EA   u8
_screen                0x108502   u16
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_pow                   0x1081E8   u8
_pow_p2                0x1083E8   u8
_stock                 0x1082E3   u8
_stock_p2              0x1084E3   u8
_pmode                 0x10A84C   u8
_pmode_p2              0x10A85D   u8
_maxv                  0x1081EA   u8
_maxv_p2               0x1083EA   u8
```

`derived` :

- `select` = `{"sum":[{"eq":["_screen",30642]},{"eq":["_screen",45984]}],"names":{"0":0,"1":1,"2":1}}`
- `p1_char` = `{"pick":["_p1_ch0","_p1_ch1","_p1_ch2"],"at":{"pick":["_p1_ord0","_p1_ord1","_p1_ord2"],"at":"_p1_lost"},"names":{"0":"KYO","1":"BENIMARU","2":"DAIMON","3":"TERRY","4":"ANDY","5":"JOE","6":"RYO","7":"ROBERT","8":"YURI","9":"LEONA…`
- `p2_char` = `{"pick":["_p2_ch0","_p2_ch1","_p2_ch2"],"at":{"pick":["_p2_ord0","_p2_ord1","_p2_ord2"],"at":"_p2_lost"},"names":{"0":"KYO","1":"BENIMARU","2":"DAIMON","3":"TERRY","4":"ANDY","5":"JOE","6":"RYO","7":"ROBERT","8":"YURI","9":"LEONA…`

## kof99 — The King of Fighters '99

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_p1_dir                0x108131   u8
_p2_dir                0x108331   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108239   u8        mult=0.990099 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.990099 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A7E6   bcd       bytes=1
_time_sub              0x10A7E7   u8        start=50
_fight_cue             0x10A786   u8        start=0
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
beat                   -          u8
beat_p2                -          u8
_p1_lost               0x10A7F9   u8
_p1_ch0                0x10A7FA   u8
_p1_ch1                0x10A7FB   u8
_p1_ch2                0x10A7FC   u8
_p1_ch3                0x10A7FD   u8
_p1_ord0               0x10A802   u8
_p1_ord1               0x10A803   u8
_p1_ord2               0x10A804   u8
_p2_lost               0x10A80E   u8
_p2_ch0                0x10A80F   u8
_p2_ch1                0x10A810   u8
_p2_ch2                0x10A811   u8
_p2_ch3                0x10A812   u8
_p2_ord0               0x10A817   u8
_p2_ord1               0x10A818   u8
_p2_ord2               0x10A819   u8
round                  0x10A7B6   u8
backdrop               0x10A7AE   u8
_screen                0x108502   u16
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
```

`derived` :

- `p1_char` = `{"pick":["_p1_ch0","_p1_ch1","_p1_ch2","_p1_ch3"],"at":{"pick":["_p1_ord0","_p1_ord1","_p1_ord2"],"at":"_p1_lost"},"names":{"0":"K'","1":"MAXIMA","2":"BENIMARU","3":"SHINGO","4":"TERRY","5":"ANDY","6":"JOE","7":"MAI","8":"RYO","9…`
- `p2_char` = `{"pick":["_p2_ch0","_p2_ch1","_p2_ch2","_p2_ch3"],"at":{"pick":["_p2_ord0","_p2_ord1","_p2_ord2"],"at":"_p2_lost"},"names":{"0":"K'","1":"MAXIMA","2":"BENIMARU","3":"SHINGO","4":"TERRY","5":"ANDY","6":"JOE","7":"MAI","8":"RYO","9…`
- `select` = `{"sum":[{"eq":["_screen",11504]},{"eq":["_screen",26074]},{"eq":["_screen",11498]},{"eq":["_screen",26062]}]}`

## korokoro — Koro Koro Quest

cpu :maincpu, ram_base 0x300000, ram_size 0x10000, swap16 True

```
credits                0x30029D   u8
round                  0x30029B   u8        add=1
```

## kotm — King of the Monsters

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10206B   u8        mult=1.666667 min=0 max=100 zero_from="0x9E"
_p2_hp                 0x10216B   u8        mult=1.666667 min=0 max=100 zero_from="0x9E"
_cpu_hp                0x10226B   u8        mult=1.666667 min=0 max=100 zero_from="0x9E"
score                  0x101FF4   bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`tag` :

- `health_p2` = `{"first":[{"pick":["_cpu_hp","_p2_hp","_p2_hp","_cpu_hp"],"at":"p2_mode"},"_cpu_hp"]}`

## kotm2 — King of the Monsters 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x101417   u8        mult=1.5625 min=0 max=100 zero_from="0xA0"
health_p2              0x101517   u8        mult=1.5625 min=0 max=100 zero_from="0xA0"
time                   0x1013D2   bcd       bytes=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x1013DC   u8
_p2_chr                0x1014DC   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"GEON","1":"ATOMIC","2":"WOO","4":"HUGE KEAL","6":"HORN","3":"YAM","7":"KILI-KILI","5":"SACK","8":"EAT","9":"KING"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"GEON","1":"ATOMIC","2":"WOO","4":"HUGE KEAL","6":"HORN","3":"YAM","7":"KILI-KILI","5":"SACK","8":"EAT","9":"KING"}}`

## lastblad — The Last Blade

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0xE3       u8        ptr="0x10AC98" ptr_range=["0x100000","0x10FFFF"]
_p2_dir                0xE3       u8        ptr="0x10AC9C" ptr_range=["0x100000","0x10FFFF"]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x180      be        bytes=2 mult=0.390625 min=0 max=100 zero_from="0x8080" ptr="0x10AC98" ptr_range=["0x100000","0x10FFFF"]
health_p2              0x180      be        bytes=2 mult=0.390625 min=0 max=100 zero_from="0x8080" ptr="0x10AC9C" ptr_range=["0x100000","0x10FFFF"]
time                   0x10E32B   bcd       bytes=1
_time_sub              0x100719   u8        start=70
_fight_cue             0x10CEDE   u8        start=0
score                  0x10E2CE   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10EAAD   u8
_p2_chr                0x10EAAF   u8
_cpu_chr               0x10EC39   u8
backdrop               0x10EC39   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"KAEDE","1":"MORIYA","2":"YUKI","3":"OKINA","4":"AKARI","5":"JUZOH","6":"WASHIZUKA","7":"SHIKYOH","8":"AMANO","9":"LEE","10":"ZANTETSU","11":"SHIGEN","12":"MUSASHI","13":"KAGAMI","14":"KAEDE"}}`
- `p2_char` = `{"pick":["_cpu_chr","_p2_chr"],"at":{"eq":["p2_mode",1]},"names":{"0":"KAEDE","1":"MORIYA","2":"YUKI","3":"OKINA","4":"AKARI","5":"JUZOH","6":"WASHIZUKA","7":"SHIKYOH","8":"AMANO","9":"LEE","10":"ZANTETSU","11":"SHIGEN","12":"MUS…`

## lastbld2 — The Last Blade 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x41       u8        ptr="0x10E344" ptr_range=["0x100000","0x10FFFF"]
_p2_dir                0x41       u8        ptr="0x10E348" ptr_range=["0x100000","0x10FFFF"]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x17E      be        bytes=2 mult=0.390625 min=0 max=100 zero_from="0x8080" ptr="0x10E344" ptr_range=["0x100000","0x10FFFF"]
health_p2              0x17E      be        bytes=2 mult=0.390625 min=0 max=100 zero_from="0x8080" ptr="0x10E348" ptr_range=["0x100000","0x10FFFF"]
rounds                 0x1AD      u8        ptr="0x10E344" ptr_range=["0x100000","0x10FFFF"]
power                  0x17D      u8        mult=1.5625 min=0 max=100 ptr="0x10E344" ptr_range=["0x100000","0x10FFFF"]
rounds_p2              0x1AD      u8        ptr="0x10E348" ptr_range=["0x100000","0x10FFFF"]
power_p2               0x17D      u8        mult=1.5625 min=0 max=100 ptr="0x10E348" ptr_range=["0x100000","0x10FFFF"]
time                   0x10E595   bcd       bytes=1
_time_sub              0x100709   u8        start=70
score                  0x10E4CE   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10BD59   u8
_p2_chr                0x10E357   u8
backdrop               0x10E57D   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"KAEDE","1":"MORIYA","2":"YUKI","3":"OKINA","4":"AKARI","5":"JUZOH","6":"WASHIZUKA","7":"MUKURO","8":"AMANO","9":"LEE","10":"ZANTETSU","11":"SHIGEN","12":"KAGAMI","13":"KOJIROH","14":"HIBIKI","15":…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"KAEDE","1":"MORIYA","2":"YUKI","3":"OKINA","4":"AKARI","5":"JUZOH","6":"WASHIZUKA","7":"MUKURO","8":"AMANO","9":"LEE","10":"ZANTETSU","11":"SHIGEN","12":"KAGAMI","13":"KOJIROH","14":"HIBIKI","15":…`

## lasthope — Last Hope

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## lbowling — League Bowling

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
time                   0x1010A5   bcd       bytes=1
time_p2                0x1011A5   bcd       bytes=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## legendos — Legend of Success Joe

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x100363   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
_p2_hp                 0x100763   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
_cpu_hp                0x100463   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
score                  0x100384   be        bytes=2 mult=100
score_p2               -          bcd       bytes=4
```

`tag` :

- `health_p2` = `{"first":[{"pick":["_cpu_hp","_p2_hp","_p2_hp","_cpu_hp"],"at":"p2_mode"},"_cpu_hp"]}`

## lresort — Last Resort

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x108018   bcd       bytes=4
score_p2               0x10801C   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x108030   u8        zero_from=240
lives_p2               0x108031   u8        zero_from=240
power                  0x104265   u8        max=4
power_p2               0x1042E5   u8        max=4
speed                  0x104267   u8        max=5
speed_p2               0x1042E7   u8        max=5
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## magdrop2 — Magical Drop II

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10007A   bcd       bytes=4
score_p2               0x10007E   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
level                  0x100A5F   u8
quota                  0x100A4B   u8
quota_p2               0x100A6B   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## magdrop3 — Magical Drop III

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10007C   bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
card                   0x1000FA   u8        mask=127
card_p2                0x1000FB   u8        mask=127
cpu_p2                 0x1000FB   u8        mask=128 shift=7
quota                  0x100611   u8
quota_p2               0x100651   u8
level                  0x100626   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `card_name` = `{"value":"card","names":{"en":["FOOL","MAGICIAN","HIGH PRIESTESS","EMPRESS","EMPEROR","HIEROPHANT","LOVERS","CHARIOT","STRENGTH","HERMIT","FORTUNE","JUSTICE","HANGED MAN","DEATH","TEMPERANCE","DEVIL","TOWER","STAR","MOON","SUN","…`
- `card_name_p2` = `{"value":"card_p2","names":{"en":["FOOL","MAGICIAN","HIGH PRIESTESS","EMPRESS","EMPEROR","HIEROPHANT","LOVERS","CHARIOT","STRENGTH","HERMIT","FORTUNE","JUSTICE","HANGED MAN","DEATH","TEMPERANCE","DEVIL","TOWER","STAR","MOON","SUN…`

## maglord — Magician Lord

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x100CA1   bcd       bytes=3 mult=10
score_p2               0x100CA5   bcd       bytes=3 mult=10
lives                  0x103B00   u8
lives_p2               0x103C00   u8
energy                 0x103B07   u8        max=5
energy_p2              0x103C07   u8        max=5
power                  0x103B04   u8        max=2
power_p2               0x103C04   u8        max=2
_turn                  0x10383E   u8
form                   0x103B05   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `form_name` = `{"value":"form","names":{"1":"MAGICIAN LORD","13":"SHINOBI","9":"WATERMAN","14":"SAMURAI","5":"DRAGON WARRIOR","10":"POSEIDON","15":"RAIJIN"}}`

## mahretsu — Mahjong Kyo Retsuden

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_move_time             0x100227   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## marukodq — Chibi Maruko-chan Deluxe Quiz

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x101303   u8
lives_p2               0x101403   u8
time                   0x100429   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## matrim — Matrimelee

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10306B   u8        mult=0.671141 min=0 max=100 zero_from="0xCA"
health_p2              0x102E9F   u8        mult=0.671141 min=0 max=100 zero_from="0xCA"
_p1_chr                0x10B81F   u8
_p2_chr                0x10B84F   u8
_p1_dir                0x103041   u8
_p2_dir                0x102E75   u8
backdrop               0x10B135   u8
time                   0x10B90B   u8        max=99
_time_sub              0x10B90C   u8        start=255
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"KEITH","3":"SAIZO","4":"WHITE","5":"ANNY","6":"CLARA","7":"KANJI","10":"UME","11":"OLOF","12":"BUNTARO","13":"SHINTARO","14":"HIKARU","15":"SISSY","16":"MR. JONES","17":"LYNN","18":"ELIAS","19":"J…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"KEITH","3":"SAIZO","4":"WHITE","5":"ANNY","6":"CLARA","7":"KANJI","10":"UME","11":"OLOF","12":"BUNTARO","13":"SHINTARO","14":"HIKARU","15":"SISSY","16":"MR. JONES","17":"LYNN","18":"ELIAS","19":"J…`

## matsuri15 — Mushihime-Sama Matsuri Ver 1.5

cpu :maincpu, ram_base 0xC000000, ram_size 0x200000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## mazinger — Mazinger Z

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0x1000A0   u8
bombs                  0x100AB6   u8
bombs_p2               0x100AE6   u8
energy                 0x100ABB   u8        mult=0.735294 min=0 max=100 zero_from="0xC4" round=1
energy_p2              0x100AEB   u8        mult=0.735294 min=0 max=100 zero_from="0xC4" round=1
power                  0x100AB8   u8        max=3
power_p2               0x100AE8   u8        max=3
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## mbombrd — Muscle Bomber Duo: Ultimate Team Battle

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF907B   u8        mult=0.392157 min=0 max=100 round=1
health_p2              0xFF927B   u8        mult=0.392157 min=0 max=100 round=1
_time                  0xFFA00C   digits    bytes=2
```

## megaman — Mega Man: The Power Battle

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8351   u8        mult=6.25 min=0 max=100 zero_from="0x88" round=1
health_p2              0xFF8751   u8        mult=6.25 min=0 max=100 zero_from="0x88" round=1
_time                  0xFF8119   bcd       bytes=1
score                  0xFF8390   bcd       bytes=4
score_p2               0xFF8790   bcd       bytes=4
```

## megaman2 — Mega Man 2: The Power Fighters

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8351   u8        mult=3.125 min=0 max=100 zero_from="0x90" round=1
health_p2              0xFF8751   u8        mult=3.125 min=0 max=100 zero_from="0x90" round=1
_time                  0xFF8119   bcd       bytes=1
score                  0xFF8390   bcd       bytes=4
```

## mercs — Mercs

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF1175   u8        mult=2.083333 min=0 max=100 zero_from="0x98" round=1
health_p2              0xFF1225   u8        mult=2.083333 min=0 max=100 zero_from="0x98" round=1
health_top             0xFF1181   u8        mult=2.083333 min=0 max=200 round=1
health_top_p2          0xFF1231   u8        mult=2.083333 min=0 max=200 round=1
time                   0xFF0ECB   digits    bytes=3
mission                0xFF0E8B   u8        add=1
bombs                  0xFF117C   bcd       bytes=1
bombs_p2               0xFF122C   bcd       bytes=1
weapon                 0xFF1185   u8
weapon_p2              0xFF1235   u8
weapon_level           0xFF1188   u8
weapon_level_p2        0xFF1238   u8
score                  0xFF0F78   digits    bytes=8
score_p2               0xFF0F80   digits    bytes=8
_hps                   0xFF2354   u16s      count=35 stride=128
```

`derived` :

- `p1_weapon` = `{"value":"weapon","names":{"fr":{"0":"FUSIL D'ASSAUT","1":"LANCE-FLAMMES","2":"FUSIL À POMPE","3":"LANCE-GRENADES"},"en":{"0":"ASSAULT RIFLE","1":"FLAMETHROWER","2":"SHOTGUN","3":"GRENADE LAUNCHER"}}}`
- `p2_weapon` = `{"value":"weapon_p2","names":{"fr":{"0":"FUSIL D'ASSAUT","1":"LANCE-FLAMMES","2":"FUSIL À POMPE","3":"LANCE-GRENADES"},"en":{"0":"ASSAULT RIFLE","1":"FLAMETHROWER","2":"SHOTGUN","3":"GRENADE LAUNCHER"}}}`

## metmqstr — Metamoqester

cpu :maincpu, ram_base 0x888000, ram_size 0x8000, swap16 True

```
health                 0xF0907C   u8        mult=0.787402 min=0 max=100 zero_from="0xBF" round=1 mame_only=true
health_p2              0xF0917C   u8        mult=0.787402 min=0 max=100 zero_from="0xBF" round=1 mame_only=true
time                   0xF0834D   u8        mame_only=true
credits                0xF08080   u8        mame_only=true
lives                  0xF0801C   u8        mame_only=true
lives_p2               0xF0801D   u8        mame_only=true
stage                  0xF08013   u8        add=1 mame_only=true
```

## miexchng — Money Puzzle Exchanger

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x102E38   bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
level                  0x107546   u8
max_chain              0x1030FB   u8
chain                  0x1030FD   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## minasan — Minasan no Okagesamadesu!

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_move_time             0x1000CD   u8
steps                  0x10131C   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## mmatrix — Mars Matrix: Hyper Solid Shooting

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF49A3   u8
lives                  0xFF49A9   u8
lives_p2               0xFF49CF   u8
power                  0xFF49B5   u8        max=7
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## mmpork — Muchi Muchi Pork!

cpu :maincpu, ram_base 0xC000000, ram_size 0x600000, swap16 True

```
credits                0xC4B75A7  u8
lives                  0xC510D2B  u8
lives_p2               0xC510F77  u8
bombs                  0xC510D3C  u8
bombs_p2               0xC510F88  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## moshougi — Shougi no Tatsujin

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## mpang — Mighty! Pang

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
time                   0xFF8108   u8
lives                  0xFF8126   u8
lives_p2               0xFF8127   u8
score                  0xFF80D4   bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## msh — Marvel Super Heroes

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF4191   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF4591   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0xFF4808   bcd       bytes=1
power                  0xFF4195   u8        mult=0.694444 min=0 max=100 round=1
power_level            0xFF4198   u8        max=3
power_p2               0xFF4595   u8        mult=0.694444 min=0 max=100 round=1
power_level_p2         0xFF4598   u8        max=3
_p1_chr                0xFF4051   u8
_p2_chr                0xFF4451   u8
rounds                 0xFF4802   u8
rounds_p2              0xFF4803   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"SPIDERMAN","2":"C.AMERICA","4":"HULK","6":"IRON MAN","8":"WOLVERINE","10":"PSYLOCKE","12":"BLACKHEART","14":"S.GORATH","16":"JUGGERNAUT","18":"MAGNETO","20":"DOC DOOM","22":"THANOS","24":"ANITA"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"SPIDERMAN","2":"C.AMERICA","4":"HULK","6":"IRON MAN","8":"WOLVERINE","10":"PSYLOCKE","12":"BLACKHEART","14":"S.GORATH","16":"JUGGERNAUT","18":"MAGNETO","20":"DOC DOOM","22":"THANOS","24":"ANITA"}}`

## mshvsf — Marvel Super Heroes Vs. Street Fighter

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
time                   0xFF4808   bcd       bytes=1
power                  0xFF3A54   u8        mult=33.333333 min=0 max=100 round=1
power_p2               0xFF3E54   u8        mult=33.333333 min=0 max=100 round=1
_p1_chr                0xFF3853   u8
_p2_chr                0xFF3C53   u8
score                  0xFF3A94   bcd       bytes=4
score_p2               0xFF3E94   bcd       bytes=4
_p1_ctl                0xFF3803   u8        human=1
_p2_ctl                0xFF3C03   u8        human=1
_p1_hp1                0xFF3A51   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p1_hp2                0xFF4251   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p1_on1                0xFF3800   u8
_p1_on2                0xFF4000   u8
_p1_chr2               0xFF4053   u8
_p2_hp1                0xFF3E51   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p2_hp2                0xFF4651   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p2_on1                0xFF3C00   u8
_p2_on2                0xFF4400   u8
_p2_chr2               0xFF4453   u8
```

`tag` :

- `health` = `{"team":[["_p1_on1","_p1_hp1","_p1_hp1"],["_p1_on2","_p1_hp2","_p1_hp2"]]}`
- `health_p2` = `{"team":[["_p2_on1","_p2_hp1","_p2_hp1"],["_p2_on2","_p2_hp2","_p2_hp2"]]}`

`derived` :

- `p1_char` = `{"team":[["_p1_on1","_p1_hp1","_p1_chr"],["_p1_on2","_p1_hp2","_p1_chr2"]],"names":{"2":"CYCLOPS","4":"C.AMERICA","6":"HULK","8":"WOLVERINE","10":"S.GORATH","12":"OMEGA RED","14":"SPIDER-MAN","16":"BLACKHEART","18":"RYU","20":"KE…`
- `p2_char` = `{"team":[["_p2_on1","_p2_hp1","_p2_chr"],["_p2_on2","_p2_hp2","_p2_chr2"]],"names":{"2":"CYCLOPS","4":"C.AMERICA","6":"HULK","8":"WOLVERINE","10":"S.GORATH","12":"OMEGA RED","14":"SPIDER-MAN","16":"BLACKHEART","18":"RYU","20":"KE…`

## mslug — Metal Slug

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x106E94   digits    bytes=8
score_p2               0x106E9C   digits    bytes=8
lives                  0x100377   u8        add=-1 min=0
lives_p2               0x100417   u8        add=-1 min=0
bombs                  0x1004C0   u8
bombs_p2               0x100560   u8
grenades_out           0x1004C1   u8
grenades_out_p2        0x100561   u8
ammo                   0x1004C2   be        bytes=2
ammo_p2                0x100562   be        bytes=2
weapon                 0x1004B1   u8
weapon_p2              0x100551   u8
vehicle                0x1004CC   u8        mask="0x01"
vehicle_hp             0x1005E7   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
vehicle_ammo           0x100610   u8        zero_from="0x80"
vehicle_p2             0x10056C   u8        mask="0x01"
vehicle_hp_p2          0x1005E7   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
vehicle_ammo_p2        0x100610   u8        zero_from="0x80"
prisoners              0x100376   u8        zero_from="0x80"
prisoners_p2           0x100416   u8        zero_from="0x80"
time                   0x106E93   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
mission                0x10E3B7   u8        add=1 valid=[1,6]
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
_hps                   0x100A46   u16s      count=104 stride=160
end_state              0x100204   be        bytes=2
boss_alive             0x106ED3   u8
```

`derived` :

- `boss_name` = `{"value":"mission","names":{"1":"TETSUYUKI","2":"HAIRBUSTER RIBERTS","3":"TANI OH","4":"SHOE & KARN","5":"IRON NOKANA","6":"HI-DO"}}`
- `boss_dead` = `{"eq":["boss_alive",0]}`
- `mission_done` = `{"all":[{"eq":["end_state",514]},{"eq":["boss_alive",0]}]}`

## mslug2 — Metal Slug 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10E86E   bcd       bytes=4
score_p2               0x10E878   bcd       bytes=4
lives                  0x101276   u8        zero_from="0x80"
lives_p2               0x10131E   u8        zero_from="0x80"
bombs                  0x10C348   u8
bombs_p2               0x10C349   u8
grenades_out           0x10C340   u8
grenades_out_p2        0x10C341   u8
ammo                   0x10C34C   be        bytes=2
ammo_p2                0x10C34E   be        bytes=2
weapon                 0x10C346   u8
weapon_p2              0x10C347   u8
p1_chr                 0x101274   u8        valid=[0,3]
p2_chr                 0x10131C   u8        valid=[0,3]
form                   0x101525   u8        valid=[0,3]
form_p2                0x1015CD   u8        valid=[0,3]
prisoners              0x105BDB   u8        zero_from="0x80"
prisoners_p2           0x105BDF   u8        zero_from="0x80"
vehicle                0x10E882   be        bytes=2
vehicle_kind           0x10E8A3   u8        valid=[0,8]
vehicle_hp             0x10E89B   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
vehicle_ammo           0x10E8A1   u8        zero_from="0x80"
vehicle_p2             0x10E8A6   be        bytes=2
vehicle_kind_p2        0x10E8C7   u8        valid=[0,8]
vehicle_hp_p2          0x10E8BF   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
vehicle_ammo_p2        0x10E8C5   u8        zero_from="0x80"
_veh1                  0x10E880   hex       bytes=36
_veh2                  0x10E8A4   hex       bytes=36
time                   0x1013B4   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
mission                0x10C31F   u8        add=1 valid=[1,6]
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
_hps                   0x101782   u16s      count=64 stride=168
end_ptr                0x101346   be        bytes=2
```

`derived` :

- `p1_name` = `{"value":"p1_chr","names":["MARCO","TARMA","ERI","FIO"]}`
- `p2_name` = `{"value":"p2_chr","names":["MARCO","TARMA","ERI","FIO"]}`
- `boss_name` = `{"value":"mission","names":{"1":"THE KEESI II","2":"AESHI NERO","3":"DRAGON NOSUKE","4":"BIG SHIEE","5":"HOZMI","6":"RUGNAME"}}`
- `mission_done` = `{"eq":["end_ptr",62764]}`

## mslug3 — Metal Slug 3

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10ED18   bcd       bytes=4
score_p2               0x10ED20   bcd       bytes=4
lives                  0x1002BB   u8
lives_p2               0x10036B   u8
bombs                  0x10EAF5   u8
bombs_p2               0x10EB03   u8
ammo                   0x10EAFA   be        bytes=2
ammo_p2                0x10EB08   be        bytes=2
weapon                 0x10EAF3   u8
weapon_p2              0x10EB01   u8
prisoners              0x10ED05   u8
prisoners_p2           0x10ED0D   u8
p1_chr                 0x100567   u8        valid=[0,3]
p2_chr                 0x100617   u8        valid=[0,3]
form                   0x10058F   u8        valid=[0,15]
form_p2                0x10063F   u8        valid=[0,15]
vehicle_kind           0x1002C1   u8        valid=[0,15]
vehicle                0x1002C1   u8        add=-1 min=0 valid=[-1,15]
vehicle_kind_p2        0x100371   u8        valid=[0,15]
vehicle_p2             0x100371   u8        add=-1 min=0 valid=[-1,15]
_p1b                   0x1002B0   hex       bytes=24
_eq1                   0x10EB0C   hex       bytes=16
_eq2                   0x10EB1C   hex       bytes=16
_eq3                   0x10EB2C   hex       bytes=16
_st1                   0x10ED00   hex       bytes=24
_vf1                   0x10A090   hex       bytes=16
time                   0x10ED78   bcd       bytes=1
mission                0x10ED7A   u8        add=1 valid=[1,5]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
grenades_out           0x10EAF0   u8
grenades_out_p2        0x10EAFE   u8
_hps                   0x10075A   u16s      count=81 stride=176
end_text               0x102A90   be        bytes=2
end_count              0x10040A   be        bytes=2
```

`derived` :

- `p1_name` = `{"value":"p1_chr","names":["MARCO","TARMA","ERI","FIO"]}`
- `p2_name` = `{"value":"p2_chr","names":["MARCO","TARMA","ERI","FIO"]}`
- `boss_name` = `{"value":"mission","names":{"1":"HUGE HERMIT","2":"MONOEYE UFO","3":"JUPITER KING","4":"SOL DAE ROKKER","5":"ROOTMARS"}}`
- `mission_done` = `{"between":["end_count",100,200]}`

## mslug4 — Metal Slug 4

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1066D6   bcd       bytes=4
score_p2               0x1066DE   bcd       bytes=4
lives                  0x100A89   u8        zero_from="0x80"
lives_p2               0x100B39   u8        zero_from="0x80"
bombs                  0x10EDED   u8
bombs_p2               0x10EDFD   u8
grenades_out           0x10EDE7   u8
grenades_out_p2        0x10EDF7   u8
ammo                   0x10EDF2   be        bytes=2
ammo_p2                0x10EE02   be        bytes=2
weapon                 0x10EDEA   u8
weapon_p2              0x10EDFA   u8
p1_chr                 0x100A88   u8        valid=[0,3]
p2_chr                 0x100B38   u8        valid=[0,3]
prisoners              0x100A90   u8        zero_from="0x80"
prisoners_p2           0x100B40   u8        zero_from="0x80"
vehicle                0x10670F   u8        valid=[0,1]
vehicle_hp             0x100A7A   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
vehicle_hp_p2          0x100B2A   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
_hps                   0x10112A   u16s      count=73 stride=176
_ew0                   0x101080   u16s      count=73 stride=176
_ew1                   0x101082   u16s      count=73 stride=176
_ew2                   0x101084   u16s      count=73 stride=176
_ew3                   0x101086   u16s      count=73 stride=176
_ew4                   0x101088   u16s      count=73 stride=176
_ew5                   0x10108A   u16s      count=73 stride=176
_ew6                   0x10108C   u16s      count=73 stride=176
_ew7                   0x10108E   u16s      count=73 stride=176
_ex0                   0x1010DC   u16s      count=73 stride=176
_ex1                   0x1010DE   u16s      count=73 stride=176
_ex2                   0x1010E0   u16s      count=73 stride=176
_ex3                   0x1010E2   u16s      count=73 stride=176
stage_state            0x100B5E   be        bytes=2
boss_flag              0x106700   u8        valid=[0,1]
_p1b                   0x100A78   hex       bytes=24
_p1k                   0x100A8F   u8
_veh                   0x106700   hex       bytes=16
time                   0x10ED5C   bcd       bytes=1
mission                0x10ED5E   u8        add=1 valid=[1,6]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
```

`derived` :

- `p1_name` = `{"value":"p1_chr","names":["MARCO","TREVOR","NADIA","FIO"]}`
- `p2_name` = `{"value":"p2_chr","names":["MARCO","TREVOR","NADIA","FIO"]}`
- `boss_name` = `{"value":"mission","names":{"1":"BRAVE GUERRIER","2":"TOSCHKA DALANUE","3":"THE IRON","4":"BIG JOHN","5":"SEA SATAN","6":"AMADEUS MOTHER COMPUTER"}}`
- `mission_done` = `{"eq":["stage_state",40916]}`

## mslug5 — Metal Slug 5

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10DE14   bcd       bytes=4
score_p2               0x10DE1C   bcd       bytes=4
lives                  0x100A41   u8        zero_from="0x80"
lives_p2               0x100B05   u8        zero_from="0x80"
bombs                  0x10D457   u8
bombs_p2               0x10D467   u8
grenades_out           0x10D451   u8
grenades_out_p2        0x10D461   u8
ammo                   0x10D45C   be        bytes=2
ammo_p2                0x10D46C   be        bytes=2
weapon                 0x10D454   u8
weapon_p2              0x10D464   u8
prisoners              0x10DDDD   u8        zero_from="0x80"
p1_chr                 0x100A40   u8        valid=[0,3]
p2_chr                 0x100B04   u8        valid=[0,3]
prisoners_p2           0x100B0C   u8        zero_from="0x80"
vehicle_kind           0x100A47   u8        valid=[0,15]
vehicle                0x100A47   u8        add=-1 min=0 valid=[-1,15]
vehicle_kind_p2        0x100B0B   u8        valid=[0,15]
vehicle_p2             0x100B0B   u8        add=-1 min=0 valid=[-1,15]
vehicle_hp             0x100A30   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
vehicle_hp_p2          0x100AF4   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
_hps                   0x100E28   u16s      count=60 stride=196
boss_down              0x10D682   u8
fade                   0x100BAB   u8
section                0x100BAD   u8
_p1b                   0x100A30   hex       bytes=32
time                   0x10D67E   bcd       bytes=1
mission                0x10D680   u8        add=1 valid=[1,5]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
```

`derived` :

- `p1_name` = `{"value":"p1_chr","names":["MARCO","TARMA","ERI","FIO"]}`
- `p2_name` = `{"value":"p2_chr","names":["MARCO","TARMA","ERI","FIO"]}`
- `boss_name` = `{"value":"mission","names":{"1":"METAL REAR","2":"SHOOTING RAY","3":"WALL CRAWLER","4":"SANDMARINE","5":"AVATAR OF EVIL"}}`
- `boss_dead` = `{"eq":["boss_down",1]}`
- `mission_done` = `{"all":[{"eq":["boss_down",1]},{"between":["fade",100,200]}]}`

## mslugx — Metal Slug X

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10C46A   bcd       bytes=4
score_p2               0x10C472   bcd       bytes=4
lives                  0x101288   u8        zero_from="0x80"
lives_p2               0x101338   u8        zero_from="0x80"
bombs                  0x10C720   u8
bombs_p2               0x10C721   u8
grenades_out           0x10C718   u8
grenades_out_p2        0x10C719   u8
ammo                   0x10C724   be        bytes=2
ammo_p2                0x10C726   be        bytes=2
weapon                 0x10C71E   u8
weapon_p2              0x10C71F   u8
prisoners              0x10C5FD   u8        zero_from="0x80"
prisoners_p2           0x10C601   u8        zero_from="0x80"
p1_chr                 0x101287   u8        valid=[0,3]
p2_chr                 0x101337   u8        valid=[0,3]
form                   0x101557   u8        valid=[0,3]
form_p2                0x101607   u8        valid=[0,3]
vehicle_kind           0x10C629   u8        valid=[0,8]
vehicle                0x10C608   be        bytes=2
vehicle_hp             0x10C621   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
vehicle_ammo           0x10C627   u8        zero_from="0x80"
vehicle_kind_p2        0x10C64D   u8        valid=[0,8]
vehicle_p2             0x10C62C   be        bytes=2
vehicle_hp_p2          0x10C645   u8        mult=2.083333 min=0 max=100 zero_from="0x80" round=1
vehicle_ammo_p2        0x10C64B   u8        zero_from="0x80"
_veh1                  0x10C606   hex       bytes=36
_veh2                  0x10C62A   hex       bytes=36
time                   0x1013DE   u8
mission                0x10C2F5   u8        add=1 valid=[1,6]
boss_down              0x10C304   u8
_hps                   0x101722   u16s      count=72 stride=176
end_ptr                0x101366   be        bytes=2
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
```

`derived` :

- `p1_name` = `{"value":"p1_chr","names":["MARCO","ERI","TARMA","FIO"]}`
- `p2_name` = `{"value":"p2_chr","names":["MARCO","ERI","TARMA","FIO"]}`
- `boss_name` = `{"value":"mission","names":{"1":"IRON NOKANA MKII","2":"AESHI NERO","3":"DRAGON NOSUKE","4":"BIG SHIEE","5":"HOZMI","6":"RUGNAME"}}`
- `boss_dead` = `{"eq":["boss_down",4]}`
- `mission_done` = `{"eq":["end_ptr",35060]}`

## msword — Magic Sword: Heroic Fantasy

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
time                   0xFFFF4B   bcd       bytes=1
power                  0xFFA9CA   be        bytes=2 mult=0.004053 min=0 max=100 round=1
power_p2               0xFFAA8A   be        bytes=2 mult=0.004053 min=0 max=100 round=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
health                 0xFFA98C   be        bytes=2 mult=0.0125 min=0 max=100 zero_from="0x8FA0" round=1
keys                   0xFFA9E9   u8
floor                  0xFFA8A6   u8
partner                0xFFB7A1   u8
```

`derived` :

- `_one` = `{"value":1}`

## mtwins — Mega Twins

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF14AB   u8        mult=1.5625 min=0 max=100 zero_from="0xA0" round=1
health_p2              0xFF156B   u8        mult=1.5625 min=0 max=100 zero_from="0xA0" round=1
_time                  0xFF0F69   bcd       bytes=1
credits                0xFF0F3E   u8
lives                  0xFF147B   u8
lives_p2               0xFF153B   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `_one` = `{"value":1}`

## mushisam — Mushihime-Sama

cpu :maincpu, ram_base 0xC000000, ram_size 0x200000, swap16 True

```
credits                0xC056BE7  u8
lives                  0xC1ED35B  u8
lives_p2               0xC1ED41B  u8
bombs                  0xC1ED35F  u8
bombs_p2               0xC1ED41F  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `mushisama` :

```
credits                0xC056B73  u8
lives                  0xC1ED2EB  u8
lives_p2               0xC1ED3AB  u8
bombs                  0xC1ED2EF  u8
bombs_p2               0xC1ED3AF  u8
```

Propre au romset `mushisamb` :

```
lives                  0xC1ED3BB  u8
lives_p2               0xC1ED47B  u8
bombs                  0xC1ED3BF  u8
bombs_p2               0xC1ED47F  u8
```

## mushitam — Puzzle! Mushihime-Tama

cpu :maincpu, ram_base 0xC000000, ram_size 0x200000, swap16 True

```
credits                0xC0564F7  u8
lives                  0xC175CF3  u8
lives_p2               0xC175CF7  u8
score                  0xC139188  u32
score_p2               -          bcd       bytes=4
```

## mutnat — Mutation Nation

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1000C2   bcd       bytes=4
score_p2               0x1000CC   bcd       bytes=4
time                   0x101562   u8
energy                 0x102019   u8        max=64
energy_p2              0x102119   u8        max=64
bombs                  0x10153F   u8
bombs_p2               0x101541   u8
special                0x10153E   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## mvsc — Marvel Vs. Capcom: Clash of Super Heroes

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_p1_ctl                0xFF3003   u8        human=1
_p2_ctl                0xFF3403   u8        human=1
time                   0xFF4008   bcd       bytes=1
power                  0xFF3273   u8        mult=0.694444 min=0 max=100 round=1
power_p2               0xFF3673   u8        mult=0.694444 min=0 max=100 round=1
_p1_chr                0xFF3053   u8
_p2_chr                0xFF3453   u8
score                  0xFF32B4   bcd       bytes=4
score_p2               0xFF36B4   bcd       bytes=4
credits                0xFF4499   bcd       bytes=1
power_level            0xFF3274   u8        max=3
power_level_p2         0xFF3674   u8        max=3
backdrop               0xFF4113   u8
_p1_hp1                0xFF3271   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p1_hp2                0xFF3A71   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p1_on1                0xFF3000   u8
_p1_on2                0xFF3800   u8
_p1_chr2               0xFF3853   u8
_p2_hp1                0xFF3671   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p2_hp2                0xFF3E71   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p2_on1                0xFF3400   u8
_p2_on2                0xFF3C00   u8
_p2_chr2               0xFF3C53   u8
```

`tag` :

- `health` = `{"team":[["_p1_on1","_p1_hp1","_p1_hp1"],["_p1_on2","_p1_hp2","_p1_hp2"]]}`
- `health_p2` = `{"team":[["_p2_on1","_p2_hp1","_p2_hp1"],["_p2_on2","_p2_hp2","_p2_hp2"]]}`

`derived` :

- `p1_char` = `{"team":[["_p1_on1","_p1_hp1","_p1_chr"],["_p1_on2","_p1_hp2","_p1_chr2"]],"names":{"2":"WAR MACHINE","4":"C.AMERICA","6":"HULK","8":"WOLVERINE","10":"GAMBIT","12":"VENOM","14":"SPIDER-MAN","16":"ROLL","18":"RYU","20":"C.COMMANDO…`
- `p2_char` = `{"team":[["_p2_on1","_p2_hp1","_p2_chr"],["_p2_on2","_p2_hp2","_p2_chr2"]],"names":{"2":"WAR MACHINE","4":"C.AMERICA","6":"HULK","8":"WOLVERINE","10":"GAMBIT","12":"VENOM","14":"SPIDER-MAN","16":"ROLL","18":"RYU","20":"C.COMMANDO…`

## nam1975 — NAM-1975

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x101008   bcd       bytes=4
score_p2               0x10100C   bcd       bytes=4
lives                  0x10109E   u8        mask="0x0F"
lives_p2               0x10119E   u8        mask="0x0F"
ammo                   0x1010E7   bcd       bytes=1
ammo_p2                0x1011E7   bcd       bytes=1
grenades               0x1010ED   bcd       bytes=1
grenades_p2            0x1011ED   bcd       bytes=1
weapon                 0x1010E6   u8
weapon_p2              0x1011E6   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ncombat — Ninja Combat

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x101814   bcd       bytes=2
score_p2               0x101824   bcd       bytes=2
time                   0x101818   u16
time_p2                0x101828   u16
lives                  0x102402   u8        add=-1 min=0
lives_p2               0x102403   u8        add=-1 min=0
energy                 0x100632   u8        max=20
energy_p2              0x100682   u8        max=20
power                  0x10063B   u8        max=2
power_p2               0x10068B   u8        max=2
char                   0x10262E   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ncommand — Ninja Commando

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x106006   bcd       bytes=4
score_p2               0x106106   bcd       bytes=4
ninja                  0x10600C   u8
ninja_p2               0x10610C   u8
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x106029   u8
time_p2                0x106129   u8
energy                 0x106030   u8        max=2
energy_p2              0x106130   u8        max=2
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `char_name` = `{"value":"ninja","names":[null,"JOE TIGER","RAYAR DRAGON","RYU EAGLE"]}`
- `char_name_p2` = `{"value":"ninja_p2","names":[null,"JOE TIGER","RAYAR DRAGON","RYU EAGLE"]}`

## nemo — Nemo

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_time                  0xFF8525   bcd       bytes=1
lives                  0xFF8398   u8
lives_p2               0xFF8498   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
bombs                  0xFF838D   u8
```

## neobombe — Neo Bomberman

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
lives                  0x101658   u8        zero_from=240
lives_p2               0x1016D8   u8        zero_from=240
fire                   0x101671   u8        max=6
fire_p2                0x1016F1   u8        max=6
speed                  0x101656   u8
speed_p2               0x1016D6   u8
bombs                  0x101672   u8
bombs_p2               0x1016F2   u8
world                  0x1000E0   u8        add=1
stage                  0x1000E1   u8        add=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## neocup98 — Neo-Geo Cup '98

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
goals                  0x1051EA   u8
goals_p2               0x1051EE   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## neodrift — Neo Drift Out - New Technology

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
time                   0x103334   u16       mult=0.016667 round=2
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## neogeo

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

Propre au romset `burningf` :

```
health                 0x100221   u8        mult=0.392157 min=0 max=100
health_p2              0x1002A1   u8        mult=0.392157 min=0 max=100
time                   0x10D002   bcd       bytes=1
```

Propre au romset `crsword` :

```
health                 0x10405B   u8        mult=2.0 min=0 max=100
health_p2              0x1040DB   u8        mult=2.0 min=0 max=100
```

Propre au romset `eightman` :

```
health                 0x100CF6   u8        mult=16.666667 min=0 max=100
health_p2              0x1011F6   u8        mult=16.666667 min=0 max=100
time                   0x100482   bcd       bytes=1
```

Propre au romset `maglord` :

```
health                 0x103B07   u8        mult=20.0 min=0 max=100
health_p2              0x103C07   u8        mult=20.0 min=0 max=100
```

Propre au romset `mutnat` :

```
health                 0x102019   u8        mult=1.5625 min=0 max=100
health_p2              0x102119   u8        mult=1.5625 min=0 max=100
```

Propre au romset `ncombat` :

```
health                 0x100632   u8        mult=3.125 min=0 max=100
health_p2              0x100682   u8        mult=3.125 min=0 max=100
```

Propre au romset `ncommand` :

```
health                 0x106030   u8        mult=50.0 min=0 max=100
health_p2              0x106130   u8        mult=50.0 min=0 max=100
```

Propre au romset `roboarmy` :

```
health                 0x1000D3   u8        mult=10.0 min=0 max=100
health_p2              0x1001D3   u8        mult=10.0 min=0 max=100
```

Propre au romset `sengoku` :

```
health                 0x100305   u8        mult=16.666667 min=0 max=100
health_p2              0x100405   u8        mult=16.666667 min=0 max=100
```

Propre au romset `sengoku2` :

```
health                 0x102CF3   u8        mult=16.666667 min=0 max=100
health_p2              0x102DF3   u8        mult=16.666667 min=0 max=100
```

Propre au romset `sengoku3` :

```
health                 0x102C19   u8        mult=1.041667 min=0 max=100
health_p2              0x102D13   u8        mult=1.041667 min=0 max=100
```

Propre au romset `shocktro` :

```
health                 0x1001B5   u8        mult=0.78125 min=0 max=100
health_p2              0x1021B5   u8        mult=0.78125 min=0 max=100
time                   0x108D01   bcd       bytes=1
```

Propre au romset `spinmast` :

```
health                 0x105F62   u8        mult=33.333333 min=0 max=100
health_p2              0x106022   u8        mult=33.333333 min=0 max=100
```

## neogeo_combat

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

Propre au romset `aodk` :

```
health                 0x100066   be        bytes=2 mult=0.032563 min=0 max=100 zero_from="0x85FF"
health_p2              0x100166   be        bytes=2 mult=0.032563 min=0 max=100 zero_from="0x85FF"
```

Propre au romset `aof` :

```
health                 0x1092CD   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x1093CD   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
```

Propre au romset `aof2` :

```
health                 0x1092ED   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x1093ED   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
```

Propre au romset `aof3` :

```
health                 0x100468   be        bytes=2 mult=0.024414 min=0 max=100 zero_from="0x8800"
health_p2              0x100568   be        bytes=2 mult=0.024414 min=0 max=100 zero_from="0x8800"
```

Propre au romset `breakers` :

```
health                 0x107332   u8        mult=3.333333 min=0 max=100 zero_from="0x8F"
health_p2              0x107892   u8        mult=3.333333 min=0 max=100 zero_from="0x8F"
```

Propre au romset `breakrev` :

```
health                 0x10734E   u8        mult=3.333333 min=0 max=100 zero_from="0x8F"
health_p2              0x1078AE   u8        mult=3.333333 min=0 max=100 zero_from="0x8F"
```

Propre au romset `fatfursp` :

```
health                 0x10049A   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x10059A   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
time                   0x10092A   bcd       bytes=1
```

Propre au romset `fatfury1` :

```
health                 0x1003B8   be        bytes=2 mult=0.004053 min=0 max=100 zero_from="0xB030"
health_p2              0x1004B8   be        bytes=2 mult=0.004053 min=0 max=100 zero_from="0xB030"
time                   0x1042F3   bcd       bytes=1
```

Propre au romset `fatfury2` :

```
health                 0x1003CB   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x1004CB   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
time                   0x10092A   bcd       bytes=1
```

Propre au romset `fatfury3` :

```
health                 0x100489   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
health_p2              0x100589   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
```

Propre au romset `fightfev` :

```
health                 0x10C602   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
health_p2              0x10C702   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
time                   0x108110   bcd       bytes=1
```

Propre au romset `galaxyfg` :

```
health                 0x10103C   u8        mult=0.392157 min=0 max=100
health_p2              0x101152   u8        mult=0.392157 min=0 max=100
```

Propre au romset `garou` :

```
health                 0x10048E   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
health_p2              0x10058E   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
time                   0x107490   bcd       bytes=1
```

Propre au romset `gowcaizr` :

```
health                 0x102D09   u8        mult=1.0 min=0 max=100 zero_from="0xB2"
health_p2              0x1035BF   u8        mult=1.0 min=0 max=100 zero_from="0xB2"
```

Propre au romset `kizuna` :

```
health                 0x108313   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
health_p2              0x108513   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
time                   0x10892A   bcd       bytes=1
```

Propre au romset `kof2000` :

```
health                 0x108239   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A7E6   bcd       bytes=1
```

Propre au romset `kof2001` :

```
health                 0x108239   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.980392 add=1 min=0 max=100 zero_from="0x80"
score                  0x1081FC   bcd       bytes=4
score_p2               0x1083FC   bcd       bytes=4
```

Propre au romset `kof94` :

```
health                 0x108221   u8        mult=0.483092 min=0 max=100 zero_from="0xE7"
health_p2              0x108421   u8        mult=0.483092 min=0 max=100 zero_from="0xE7"
time                   0x10882E   bcd       bytes=1
```

Propre au romset `kof95` :

```
health                 0x108221   u8        mult=0.483092 min=0 max=100 zero_from="0xE7"
health_p2              0x108421   u8        mult=0.483092 min=0 max=100 zero_from="0xE7"
time                   0x10A836   bcd       bytes=1
```

Propre au romset `kof96` :

```
health                 0x108239   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A836   bcd       bytes=1
```

Propre au romset `kof97` :

```
health                 0x108239   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A83A   bcd       bytes=1
```

Propre au romset `kof98` :

```
health                 0x108239   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.970874 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A83A   bcd       bytes=1
```

Propre au romset `kof99` :

```
health                 0x108239   u8        mult=0.990099 add=1 min=0 max=100 zero_from="0x80"
health_p2              0x108439   u8        mult=0.990099 add=1 min=0 max=100 zero_from="0x80"
time                   0x10A7E6   bcd       bytes=1
```

Propre au romset `kotm` :

```
health                 0x10206B   u8        mult=1.666667 min=0 max=100 zero_from="0x9E"
health_p2              0x10216B   u8        mult=1.666667 min=0 max=100 zero_from="0x9E"
```

Propre au romset `kotm2` :

```
health                 0x101417   u8        mult=1.5625 min=0 max=100 zero_from="0xA0"
health_p2              0x101517   u8        mult=1.5625 min=0 max=100 zero_from="0xA0"
time                   0x1013D2   bcd       bytes=1
```

Propre au romset `legendos` :

```
health                 0x100363   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
health_p2              0x100763   u8        mult=0.833333 min=0 max=100 zero_from="0xBC"
```

Propre au romset `ninjamas` :

```
health                 0x100050   u8        mult=0.480769 min=0 max=100 zero_from="0xE8"
health_p2              0x101050   u8        mult=0.480769 min=0 max=100 zero_from="0xE8"
```

Propre au romset `rbff1` :

```
health                 0x100489   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
health_p2              0x100589   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
```

Propre au romset `rbff2` :

```
health                 0x10048B   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
health_p2              0x10058B   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
time                   0x107C28   bcd       bytes=1
```

Propre au romset `rbffspec` :

```
health                 0x10048B   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
health_p2              0x10058B   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
time                   0x106AB4   bcd       bytes=1
```

Propre au romset `samsho3` :

```
health                 0x108573   u8        mult=0.78125 min=0 max=100 zero_from="0xC0"
health_p2              0x108673   u8        mult=0.78125 min=0 max=100 zero_from="0xC0"
time                   0x10849E   bcd       bytes=1
```

Propre au romset `samsho4` :

```
health                 0x108443   u8        mult=0.396825 min=0 max=100 zero_from="0xFE"
health_p2              0x108643   u8        mult=0.396825 min=0 max=100 zero_from="0xFE"
```

Propre au romset `samsho5` :

```
health                 0x108445   u8        mult=0.8 min=0 max=100 zero_from="0xBE"
health_p2              0x108655   u8        mult=0.8 min=0 max=100 zero_from="0xBE"
```

Propre au romset `wh2` :

```
health                 0x10600C   u8        mult=0.787402 min=0 max=100 zero_from="0xBF"
health_p2              0x10610C   u8        mult=0.787402 min=0 max=100 zero_from="0xBF"
```

Propre au romset `wh2j` :

```
health                 0x10600C   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x10610C   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
```

Propre au romset `whp` :

```
health                 0x10600C   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
health_p2              0x10610C   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
```

## neogeo_reflexion

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## neogeo_shoot

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## neogeo_sport

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## neomrdo — Neo Mr. Do!

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x104652   be        bytes=4
score_p2               0x104656   be        bytes=4
lives                  0x10465B   u8
lives_p2               0x10465D   u8
time                   0x104257   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ninjamas — Ninja Master's

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x100050   u8        mult=0.480769 min=0 max=100 zero_from="0xE8"
health_p2              0x101050   u8        mult=0.480769 min=0 max=100 zero_from="0xE8"
_p1_chr                0x10C044   u8
_p2_chr                0x10C084   u8
_p1_dir                0x100D21   u8
_p2_dir                0x101D21   u8
backdrop               0x10C008   u8
time                   0x10C021   bcd       bytes=1
_time_sub              0x10C023   u8        start=255
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
power                  0x1000AE   u8        mult=1.041667 min=0 max=100 round=1
power_p2               0x1010AE   u8        mult=1.041667 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"SASUKE","1":"KAMUI","2":"RAIGA","3":"TENHO","4":"KARASU","5":"HOUOH","6":"NATSUME","7":"GOEMON","8":"UNZEN","9":"KASUMI","10":"RANMARU","11":"NOBUNAGA"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"SASUKE","1":"KAMUI","2":"RAIGA","3":"TENHO","4":"KARASU","5":"HOUOH","6":"NATSUME","7":"GOEMON","8":"UNZEN","9":"KASUMI","10":"RANMARU","11":"NOBUNAGA"}}`

## nitd — Nightmare in the Dark

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10005E   bcd       bytes=4
score_p2               0x100294   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x100002   u8
lives                  0x100055   u8
fire                   0x100052   u8
speed                  0x100051   u8
lives_p2               0x10028B   u8
boss                   0x1029B7   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## nwarr — Night Warriors: Darkstalkers' Revenge

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF83CB   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF88CB   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
rounds                 0xFF8830   u8
rounds_p2              0xFF8D30   u8
time                   0xFF8E09   bcd       bytes=1
credits                0xFF81B2   u8
_p1_chr                0xFF8829   u8
_p2_chr                0xFF8D29   u8
score                  0xFF881A   bcd       bytes=4
backdrop               0xFF8D89   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"DEMITRI","2":"JON TALBAIN","3":"VICTOR","4":"LORD RAPTOR","5":"MORRIGAN","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"RIKUO","10":"SASQUATCH","11":"HUITZIL","12":"PYRON","13":"HSIEN-KO","14":"…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"DEMITRI","2":"JON TALBAIN","3":"VICTOR","4":"LORD RAPTOR","5":"MORRIGAN","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"RIKUO","10":"SASQUATCH","11":"HUITZIL","12":"PYRON","13":"HSIEN-KO","14":"…`

## overtop — Over Top

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
time                   0x10B004   bcd       bytes=1
rank                   0x10E0FD   u8        add=1
speed                  0x104851   u8        max=255
lap_min                0x10E098   bcd       bytes=1
lap_sec                0x10E099   bcd       bytes=1
lap_cs                 0x10E09A   bcd       bytes=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## pang3 — Pang! 3

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_time                  0xFF8BAE   u8
lives                  0xFF8BB4   u8
lives_p2               0xFF8BB5   u8
score                  0xFF8BBA   bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## panicbom — Panic Bomber

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1038BC   be        bytes=4
score_p2               0x103B5E   be        bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
power                  0x1038CD   u8        max=8
power_p2               0x103B6F   u8        max=8
level                  0x103941   u8
level_p2               0x103BE3   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## pbobbl2n — Puzzle Bobble 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1057DC   be        bytes=4
score_p2               0x1057E0   be        bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x10D617   u8
time_p2                0x10D6AD   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
round                  0x105831   u8        add=1
path                   0x10E701   u8
mode                   0x1057CD   u8
wins                   0x1057F5   u8
wins_p2                0x1057F7   u8
rounds_done            0x1057D3   u8
bubble                 -0x11      u8        valid=[0,7] ptr="0x10D620" ptr_range=["0x109000","0x10C000"]
bubble_next            -0x11      u8        valid=[0,7] ptr="0x10D62E" ptr_range=["0x109000","0x10C000"]
bubble_p2              -0x11      u8        valid=[0,7] ptr="0x10D6B6" ptr_range=["0x109000","0x10C000"]
bubble_next_p2         -0x11      u8        valid=[0,7] ptr="0x10D6C4" ptr_range=["0x109000","0x10C000"]
angle                  0x10D5DA   s16
angle_p2               0x10D670   s16
```

`derived` :

- `vs_mode` = `{"eq":["mode",2]}`

## pbobblen — Puzzle Bobble

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10820A   be        bytes=4
score_p2               0x1082A6   be        bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
round                  0x102271   u8        add=1
vs_mode                0x101079   u8
wins                   0x102275   u8
wins_p2                0x102277   u8
bubble                 0x10821F   u8
bubble_next            0x10823D   u8
bubble_p2              0x1082BB   u8
bubble_next_p2         0x1082D9   u8
angle                  0x108262   s16
angle_p2               0x1082FE   s16
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## pgoal — Pleasure Goal

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
goals                  0x1069C9   u8
goals_p2               0x1069CB   u8
_clock                 0x104C28   u16       mult=0.125 round=0
_clock_vs              0x104C28   u16       mult=0.090909 round=0
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`tag` :

- `clock` = `{"pick":["_clock","_clock_vs"],"at":{"all":[{"eq":["p1_mode",1]},{"eq":["p2_mode",1]}]}}`

## pinkswts — Pink Sweets: Ibara Sorekara

cpu :maincpu, ram_base 0xC000000, ram_size 0x500000, swap16 True

```
credits                0xC4164B0  u8
lives                  0xC49C857  u8
lives_p2               0xC49CB0F  u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

Propre au romset `pinkswtsa` :

```
credits                0xC416500  u8
lives                  0xC49C8A7  u8
lives_p2               0xC49CB5F  u8
```

Propre au romset `pinkswtsb` :

```
credits                0xC4164EC  u8
lives                  0xC49C893  u8
lives_p2               0xC49CB4B  u8
```

Propre au romset `pinkswtsx` :

```
lives                  0xC495A9B  u8
lives_p2               0xC495D53  u8
```

## plegends — Gogetsuji Legends

cpu :maincpu, ram_base 0x400000, ram_size 0x10000, swap16 True

```
health                 0x4007A1   u8        mult=0.446429 min=0 max=100 zero_from="0xF0" round=1
health_p2              0x400BA1   u8        mult=0.446429 min=0 max=100 zero_from="0xF0" round=1
time                   0x40034C   bcd       bytes=1
credits                0x40FE48   bcd       bytes=1
power                  0x4007A7   u8        mult=1.5625 min=0 max=100 round=1
power_p2               0x400BA7   u8        mult=1.5625 min=0 max=100 round=1
score                  0x400354   bcd       bytes=4
```

## pnickj — Pnickies

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## pnyaa — Pochi and Nyaa

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x101F9A   be        bytes=4
score_p2               0x102C0C   be        bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## popbounc — Pop 'n Bounce

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x10823D   u8
lives_p2               0x10824B   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## preisle2 — Prehistoric Isle 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10C1A4   bcd       bytes=4 mult=100
score_p2               0x10C1A8   bcd       bytes=4 mult=100
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x105055   u8        add=-1 min=0
lives_p2               0x1062D5   u8        add=-1 min=0
bombs                  0x105071   u8
bombs_p2               0x1062F1   u8
power                  0x105076   u8        mult=0.25 add=1 max=5
power_p2               0x1062F6   u8        mult=0.25 add=1 max=5
stars                  0x10506A   be        bytes=2
stars_p2               0x1062EA   be        bytes=2
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## progear — Progear

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF2389   u8
lives                  0xFF3F73   u8
lives_p2               0xFF3F75   u8
bombs                  0xFF4305   u8
power                  0xFF4303   u8        max=8
fighter                0xFF39E5   u8
score                  0xFF3DC6   bcd       bytes=4 mult=10
score_p2               -          bcd       bytes=4
```

## pspikes2 — Power Spikes II

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time_min               0x102B4B   u8
time_sec               0x102B4D   u8
power                  0x102CD9   u8        max=48
power_p2               0x102CDB   u8        max=48
energy                 0x1018F9   u8        max=96
energy_p2              0x1018FB   u8        max=96
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## pulstar — Pulstar

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x101322   bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x10132A   u8
lives_p2               0x10132B   u8
stage                  0x101ADD   u8
charge                 0x101696   u8
speed                  0x1017DE   u8        max=7
pods                   0x1017E1   u8        mask=7
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `stage_name` = `{"value":"stage","names":{"en":[null,"FRONT LINE","WATER VEIN","FIRE PROMINENCE","SPACE STATION","DANGEROUS FOREST","TERMINATORS","DARK NEBULA","LIFE OR DEATH","FINAL BOSS"],"fr":[null,"LIGNE DE FRONT","VEINE D'EAU","MER DE FEU",…`

## punisher — The Punisher

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8E9F   u8        mult=0.735294 min=0 max=100 zero_from="0xC4" round=1
health_p2              0xFF8F9F   u8        mult=0.735294 min=0 max=100 zero_from="0xC4" round=1
_time                  0xFF18AB   u8
lives                  0xFF5BA4   u8
lives_p2               0xFF5BA5   u8
bombs                  0xFF5BCA   u8
score                  0xFF5BAA   bcd       bytes=3 mult=100
score_p2               -          bcd       bytes=4
```

## puzzldpr — Puzzle De Pon! R!

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x100030   be        bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x107D23   u8
level                  0x1001E5   u8
bubble                 0x1023B5   u8
bubble_next            0x10212B   u8
bubble_p2              0x104B9D   u8
bubble_next_p2         0x104913   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## puzzledp — Puzzle De Pon!

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x100030   be        bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x107D23   u8
level                  0x1001E5   u8
bubble                 0x1023B5   u8
bubble_next            0x10212B   u8
bubble_p2              0x104B9D   u8
bubble_next_p2         0x104913   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## pwrinst2 — Power Instinct 2

cpu :maincpu, ram_base 0x400000, ram_size 0x10000, swap16 True

```
health                 0x40079D   u8        mult=0.446429 min=0 max=100 zero_from="0xF0" round=1
health_p2              0x400B9D   u8        mult=0.446429 min=0 max=100 zero_from="0xF0" round=1
time                   0x400344   bcd       bytes=1
credits                0x40FE48   bcd       bytes=1
_p1_chr                0x400327   u8
_p2_chr                0x40032B   u8
score                  0x40034C   bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"2":"ANNIE","1":"OUME","3":"OUME","4":"THIN NEN","5":"KEITH","6":"ANGELA","7":"WHITE","8":"SAIZO","9":"REIJI","10":"SAHAD","11":"OSHIMA","12":"KANJI","13":"KANJI","14":"KINTARO","15":"POCHI","16":"KURA…`
- `p2_char` = `{"value":"_p2_chr","names":{"2":"ANNIE","1":"OUME","3":"OUME","4":"THIN NEN","5":"KEITH","6":"ANGELA","7":"WHITE","8":"SAIZO","9":"REIJI","10":"SAHAD","11":"OSHIMA","12":"KANJI","13":"KANJI","14":"KINTARO","15":"POCHI","16":"KURA…`

## pzloop2 — Puzz Loop 2

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF80B0   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `_one` = `{"value":1}`

## qad — Quiz & Dragons: Capcom Quiz Game

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
lives                  0xFFE477   u8
lives_p2               0xFFE479   u8
score                  0xFFE466   u32
score_p2               0xFFE46A   u32
```

Propre au romset `qadjr` :

```
lives                  0xFF81A7   u8
lives_p2               0xFF82A7   u8
```

## qndream — Quiz Nanairo Dreams: Nijiirochou no Kiseki

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF8D67   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## qtono2j — Quiz Tonosama no Yabou 2: Zenkoku-ban

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
lives                  0xFF81A5   u8
lives_p2               0xFF82A5   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

## quizdai2 — Quiz Meitantei Neo & Geo

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x101AC4   u8
lives_p2               0x101FC4   u8
gold                   0x100956   u16
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## quizdais — Quiz Daisousa Sen

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x1022B3   u8
lives_p2               0x1023B3   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## quizkof — Quiz King of Fighters

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x10150A   u8
lives_p2               0x10158A   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ragnagrd — Ragnagard

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x109088   s16       mult=0.392157 min=0 max=100
health_p2              0x109360   s16       mult=0.392157 min=0 max=100
_p1_chr                0x109025   u8
_p2_chr                0x1092FD   u8
_p1_dir                0x10915E   u8
_p2_dir                0x109436   u8
backdrop               0x1092FD   u8
_time                  0x1099F4   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"SUSANO","1":"BENTEN","2":"CHICHI-NENE","3":"GOKUU","4":"BINTEN","5":"SYUTEN-DOZI","6":"SEENA","7":"IGRET","8":"BEHEMOTH","9":"EELIS","10":"LUCIFER","11":"GILFER"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"SUSANO","1":"BENTEN","2":"CHICHI-NENE","3":"GOKUU","4":"BINTEN","5":"SYUTEN-DOZI","6":"SEENA","7":"IGRET","8":"BEHEMOTH","9":"EELIS","10":"LUCIFER","11":"GILFER"}}`

## rbff1 — Real Bout Fatal Fury

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100471   u8
_p2_dir                0x100571   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x100489   u8        mult=0.520833 add=0.4 min=0 max=100 zero_from="0xE0"
health_p2              0x100589   u8        mult=0.520833 add=0.4 min=0 max=100 zero_from="0xE0"
backdrop               0x106A33   u8
rounds                 0x106A76   u8
rounds_p2              0x106A77   u8
time                   0x106AA8   bcd       bytes=1
_time_sub              0x106AA9   u8
_fight_cue             0x106AA2   u8        start=51 delay=0.45
score                  0x10E00A   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x106A25   u8
_p2_chr                0x106A27   u8
power                  0x1004BA   u8        mult=1.666667 min=0 max=100 round=1
power_p2               0x1005BA   u8        mult=1.666667 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"MAI","5":"GEESE","6":"SOKAKU","7":"BOB","8":"HON-FU","9":"MARY","10":"FRANCO","11":"YAMAZAKI","12":"CHONSHU","13":"CHONREI","14":"DUCK KING","15":"KIM","16":"BILLY…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"MAI","5":"GEESE","6":"SOKAKU","7":"BOB","8":"HON-FU","9":"MARY","10":"FRANCO","11":"YAMAZAKI","12":"CHONSHU","13":"CHONREI","14":"DUCK KING","15":"KIM","16":"BILLY…`

## rbff2 — Real Bout Fatal Fury 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100471   u8
_p2_dir                0x100571   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10048B   u8        mult=0.520833 add=0.4 min=0 max=100 zero_from="0xE0"
health_p2              0x10058B   u8        mult=0.520833 add=0.4 min=0 max=100 zero_from="0xE0"
rounds                 0x107C0C   u8
rounds_p2              0x107C0D   u8
time                   0x107C28   bcd       bytes=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x107BA5   u8
_p2_chr                0x107BA7   u8
backdrop               0x107BB1   u8
power                  0x1004BC   u8        mult=1.666667 min=0 max=100 round=1
power_p2               0x1005BC   u8        mult=1.666667 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"MAI","5":"GEESE","6":"SOKAKU","7":"BOB","8":"HON-FU","9":"MARY","10":"FRANCO","11":"YAMAZAKI","12":"CHONSHU","13":"CHONREI","14":"DUCK KING","15":"KIM","16":"BILLY…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"MAI","5":"GEESE","6":"SOKAKU","7":"BOB","8":"HON-FU","9":"MARY","10":"FRANCO","11":"YAMAZAKI","12":"CHONSHU","13":"CHONREI","14":"DUCK KING","15":"KIM","16":"BILLY…`

## rbffspec — Real Bout Fatal Fury Special

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100471   u8
_p2_dir                0x100571   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10048B   u8        mult=0.520833 add=0.4 min=0 max=100 zero_from="0xE0"
health_p2              0x10058B   u8        mult=0.520833 add=0.4 min=0 max=100 zero_from="0xE0"
rounds                 0x106A83   u8
rounds_p2              0x106A82   u8
time                   0x106AB4   bcd       bytes=1
_time_sub              0x106AB5   u8
_fight_cue             0x106AAE   u8        start=51
score                  0x10E00A   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x106A25   u8
_p2_chr                0x100511   u8
backdrop               0x106A31   u8
power                  0x1004BC   u8        mult=1.666667 min=0 max=100 round=1
power_p2               0x1005BC   u8        mult=1.666667 min=0 max=100 round=1
_screen                0x1041D1   u8
round                  0x106A37   u8        add=-1 min=0
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"MAI","5":"GEESE","6":"SOKAKU","7":"BOB","8":"HON FU","9":"MARY","10":"FRANCO","11":"YAMAZAKI","12":"CHONSHU","13":"CHONREI","14":"DUCK KING","15":"KIM","16":"BILLY…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"TERRY","2":"ANDY","3":"JOE","4":"MAI","5":"GEESE","6":"SOKAKU","7":"BOB","8":"HON FU","9":"MARY","10":"FRANCO","11":"YAMAZAKI","12":"CHONSHU","13":"CHONREI","14":"DUCK KING","15":"KIM","16":"BILLY…`
- `select` = `{"sum":[{"eq":["_screen",7]},{"eq":["_screen",8]}]}`

## redearth — Red Earth

cpu :maincpu, ram_base 0x2000000, ram_size 0x80000, swap32 True

```
health                 0x206A840  be        bytes=2 mult=0.337838 min=0 max=100 zero_from="0x8094" round=1
health_p2              0x206AAC0  be        bytes=2 mult=0.337838 min=0 max=100 zero_from="0x8094" round=1
credits                0x2000A10  u8
backdrop               0x20606E7  u8
```

## ridhero — Riding Hero

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
time                   0x1000F8   bcd       bytes=1
turbo                  0x100F79   u8        max=4
rank                   0x100F89   u8
speed                  0x100F52   bcd       bytes=2 max=199
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `rank_name` = `{"value":"rank","names":{"1":"1ST","2":"2ND","3":"3RD","4":"4TH","5":"5TH","6":"6TH","7":"7TH","8":"8TH"}}`

## ringdest — Ring of Destruction: Slammasters II

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF802C   be        bytes=2 mult=0.359712 min=0 max=100 zero_from="0x808B" round=1
health_p2              0xFF842C   be        bytes=2 mult=0.359712 min=0 max=100 zero_from="0x808B" round=1
time                   0xFF72CA   bcd       bytes=1
credits                0xFF726E   u8
```

## roboarmy — Robo Army

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x100037   bcd       bytes=4 mult=10
score_p2               0x100137   bcd       bytes=4 mult=10
lives                  0x1000D2   u8
lives_p2               0x1001D2   u8
energy                 0x1000D3   u8        max=10
energy_p2              0x1001D3   u8        max=10
bombs                  0x1000D4   u8        max=6
bombs_p2               0x1001D4   u8        max=6
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## rotd — Rage of the Dragons

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x1024CE   s16       mult=0.555556 min=0 max=100
health_p2              0x102356   s16       mult=0.555556 min=0 max=100
_p1_chr                0x102473   u8
_p2_chr                0x1022FB   u8
_p1_dir                0x102427   u8        mask=1
_p2_dir                0x1022AF   u8        mask=1
time                   0x106B11   u8        max=99
_time_sub              0x106B1F   u8
_fight_cue             0x100FE8   u8        start=8
score                  0x106B36   bcd       bytes=4
score_p2               -          bcd       bytes=4
stage                  0x106909   u8
backdrop               0x106B97   u8
power                  0x1024E3   u8        mult=0.462963 min=0 max=100 round=1
power_p2               0x10236B   u8        mult=0.462963 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"BILLY","1":"LYNN","2":"RADEL","3":"ANNIE","4":"CASSANDRA","5":"ONI","6":"PEPE","7":"PUPA","8":"ALICE","9":"ELIAS","10":"JONES","11":"KANG","12":"SONIA","13":"JIMMY","14":"ABUBO","15":"JOHANN"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"BILLY","1":"LYNN","2":"RADEL","3":"ANNIE","4":"CASSANDRA","5":"ONI","6":"PEPE","7":"PUPA","8":"ALICE","9":"ELIAS","10":"JONES","11":"KANG","12":"SONIA","13":"JIMMY","14":"ABUBO","15":"JOHANN"}}`

## s1945p — Strikers 1945 Plus

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1000E0   be        bytes=4
score_p2               0x10013C   be        bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x1000E9   u8
lives_p2               0x100145   u8
bombs                  0x1000EB   u8
bombs_p2               0x100147   u8
power                  0x1000ED   u8        max=4
power_p2               0x100149   u8        max=4
super                  0x1000F5   u8        max=8
super_p2               0x100151   u8        max=8
charge                 0x1000F6   be        bytes=2
charge_p2              0x100152   be        bytes=2
plane                  0x1000E7   u8
plane_p2               0x100143   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
_mission               0x1000D9   u8
_title                 0x100128   u8
_bhp                   0x101EE6   u16s      count=40 stride=328
_bmark                 0x101EF8   u16s      count=40 stride=328
```

`derived` :

- `plane_name` = `{"value":"plane","names":["","P-38 LIGHTNING","F5U FLYING PANCAKE","SPITFIRE MK.VI","TA-152","ZERO TYPE 52","FIAT G.56","XP-55 ASCENDER"]}`

## sailormn — Bishoujo Senshi Sailor Moon

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
health                 0x102033   u8        mult=1.470588 min=0 max=100 zero_from="0xA2" round=1
health_p2              0x102133   u8        mult=1.470588 min=0 max=100 zero_from="0xA2" round=1
time                   0x10A416   bcd       bytes=1
credits                0x10835F   u8
lives                  0x1020F4   u8
lives_p2               0x1021F4   u8
_p1_chr                0x102001   u8
_p2_chr                0x102101   u8
score                  0x1094C0   bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"SAILOR MOON","2":"S.MERCURY","3":"SAILOR MARS","4":"S.JUPITER","5":"S.VENUS"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"SAILOR MOON","2":"S.MERCURY","3":"SAILOR MARS","4":"S.JUPITER","5":"S.VENUS"}}`

## samsh5sp — Samurai Shodown V Special

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x0F       u8        ptr="0x108332" ptr_range=["0x100000","0x10FFFF"]
_p2_dir                0x0F       u8        ptr="0x108336" ptr_range=["0x100000","0x10FFFF"]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108445   u8        mult=0.8 min=0 max=100 zero_from="0xBE"
health_p2              0x108655   u8        mult=0.8 min=0 max=100 zero_from="0xBE"
backdrop               0x108B4F   u8
rounds                 0x108464   u8
rounds_p2              0x108674   u8
time                   0x10836A   bcd       bytes=1
_time_sub              0x10836B   u8        start=60
_fight_cue             0x108B38   u8        start=16
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x108322   u8
_p2_chr                0x108323   u8
power                  0x10844E   u8        mult=1.5625 min=0 max=100 round=1
power_p2               0x10865E   u8        mult=1.5625 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"RIMURURU","3":"HANZO","4":"GALFORD","5":"KYOSHIRO","6":"UKYO","7":"GENJURO","8":"BASARA","9":"SHIZUMARU","10":"GAIRA","11":"AMAKUSA","12":"JUBEI","13":"SANKURO","14":…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"RIMURURU","3":"HANZO","4":"GALFORD","5":"KYOSHIRO","6":"UKYO","7":"GENJURO","8":"BASARA","9":"SHIZUMARU","10":"GAIRA","11":"AMAKUSA","12":"JUBEI","13":"SANKURO","14":…`

## samsho — Samurai Shodown

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x4E       u8        ptr="0x100A0A" ptr_range=["0x100000","0x10FFFF"]
_p2_dir                0x4E       u8        ptr="0x100A0E" ptr_range=["0x100000","0x10FFFF"]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0xA5       u8        mult=0.78125 min=0 max=100 zero_from="0xC0" ptr="0x100A0A" ptr_range=["0x100000","0x10FFFF"]
health_p2              0xA5       u8        mult=0.78125 min=0 max=100 zero_from="0xC0" ptr="0x100A0E" ptr_range=["0x100000","0x10FFFF"]
time                   0x100A08   bcd       bytes=1
_time_sub              0x100A09   u8        start=16
score                  0x101000   bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10100B   u8
_p2_chr                0x10102B   u8
backdrop               0x10102B   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"HANZO","3":"GALFORD","4":"WANG-FU","5":"UKYO","6":"KYOSHIRO","7":"GEN-AN","8":"EARTHQUAKE","9":"JUBEI","10":"TAMTAM","11":"CHARLOTTE","12":"AMAKUSA"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"HANZO","3":"GALFORD","4":"WANG-FU","5":"UKYO","6":"KYOSHIRO","7":"GEN-AN","8":"EARTHQUAKE","9":"JUBEI","10":"TAMTAM","11":"CHARLOTTE","12":"AMAKUSA"}}`

## samsho2 — Samurai Shodown II

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x7F       u8        ptr="0x100A46" ptr_range=["0x100000","0x10FFFF"]
_p2_dir                0x7F       u8        ptr="0x100A4A" ptr_range=["0x100000","0x10FFFF"]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0xBB       u8        mult=0.78125 min=0 max=100 zero_from="0xC0" ptr="0x100A46" ptr_range=["0x100000","0x10FFFF"]
health_p2              0xBB       u8        mult=0.78125 min=0 max=100 zero_from="0xC0" ptr="0x100A4A" ptr_range=["0x100000","0x10FFFF"]
power                  0xF0       u8        mult=3.125 min=0 max=100 ptr="0x100A46" ptr_range=["0x100000","0x10FFFF"]
power_p2               0xF0       u8        mult=3.125 min=0 max=100 ptr="0x100A4A" ptr_range=["0x100000","0x10FFFF"]
_powmax                0xB8       u16       ptr="0x100A46" ptr_range=["0x100000","0x10FFFF"]
_powmax_p2             0xB8       u16       ptr="0x100A4A" ptr_range=["0x100000","0x10FFFF"]
time                   0x100AC6   bcd       bytes=1
_fight_cue             0x100AD3   u8        start=254
score                  0x90       bcd       bytes=4 ptr="0x100A46" ptr_range=["0x100000","0x10FFFF"] hold_zero=20
score_p2               0x90       bcd       bytes=4 ptr="0x100A4A" ptr_range=["0x100000","0x10FFFF"] hold_zero=20
_p1_chr                0x100D0B   u8
_p2_chr                0x100D1B   u8
backdrop               0x100AD9   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"HANZO","3":"GALFORD","4":"WAN-FU","5":"UKYO","6":"KYOSHIRO","7":"GEN-AN","8":"EARTHQUAKE","9":"JUBEI","11":"CHARLOTTE","12":"GENJURO","13":"CHAM CHAM","14":"SIEGER","…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"HANZO","3":"GALFORD","4":"WAN-FU","5":"UKYO","6":"KYOSHIRO","7":"GEN-AN","8":"EARTHQUAKE","9":"JUBEI","11":"CHARLOTTE","12":"GENJURO","13":"CHAM CHAM","14":"SIEGER","…`

## samsho3 — Samurai Shodown III

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x1085DB   u8
_p2_dir                0x1085DB   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108573   u8        mult=0.78125 min=0 max=100 zero_from="0xC0"
health_p2              0x108673   u8        mult=0.78125 min=0 max=100 zero_from="0xC0"
rounds                 0x108592   u8
rounds_p2              0x108692   u8
time                   0x10849E   bcd       bytes=1
_time_sub              0x10849F   u8        start=30
_fight_cue             0x109062   u8        start=41
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x108470   u8        mask="0x0F"
_p2_chr                0x108471   u8        mask="0x0F"
backdrop               0x109069   u8
power                  0x10857C   u8        mult=1.5625 min=0 max=100 round=1
power_p2               0x10867C   u8        mult=1.5625 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"RIMURURU","3":"HANZO","4":"GALFORD","5":"KYOSHIRO","6":"UKYO","7":"GENJURO","8":"KUBIKIRI","9":"SHIZUMARU","10":"GAIRA","11":"AMAKUSA","12":"KUROKO","13":"ZANKURO"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"RIMURURU","3":"HANZO","4":"GALFORD","5":"KYOSHIRO","6":"UKYO","7":"GENJURO","8":"KUBIKIRI","9":"SHIZUMARU","10":"GAIRA","11":"AMAKUSA","12":"KUROKO","13":"ZANKURO"}}`

## samsho4 — Samurai Shodown IV

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x0F       u8        ptr="0x108330" ptr_range=["0x100000","0x10FFFF"]
_p2_dir                0x0F       u8        ptr="0x108334" ptr_range=["0x100000","0x10FFFF"]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108443   u8        mult=0.396825 min=0 max=100 zero_from="0xFE"
health_p2              0x108643   u8        mult=0.396825 min=0 max=100 zero_from="0xFE"
rounds                 0x108462   u8
rounds_p2              0x108662   u8
time                   0x108368   bcd       bytes=1
_time_sub              0x108369   u8        start=60
_fight_cue             0x108B16   u8        start=12
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x108322   u8
_p2_chr                0x108323   u8
backdrop               0x108B2B   u8
power                  0x10844C   u8        mult=1.5625 min=0 max=100 round=1
power_p2               0x10864C   u8        mult=1.5625 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"RIMURURU","3":"HANZO","4":"GALFORD","5":"KYOSHIRO","6":"UKYO","7":"GENJURO","8":"KUBIKIRI","9":"SHIZUMARU","10":"GAIRA","11":"AMAKUSA","12":"JUBEI","13":"ZANKURO","14…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"RIMURURU","3":"HANZO","4":"GALFORD","5":"KYOSHIRO","6":"UKYO","7":"GENJURO","8":"KUBIKIRI","9":"SHIZUMARU","10":"GAIRA","11":"AMAKUSA","12":"JUBEI","13":"ZANKURO","14…`

## samsho5 — Samurai Shodown V

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x0F       u8        ptr="0x108332" ptr_range=["0x100000","0x10FFFF"]
_p2_dir                0x0F       u8        ptr="0x108336" ptr_range=["0x100000","0x10FFFF"]
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x108445   u8        mult=0.8 min=0 max=100 zero_from="0xBE"
health_p2              0x108655   u8        mult=0.8 min=0 max=100 zero_from="0xBE"
backdrop               0x108B4F   u8
rounds                 0x108464   u8
rounds_p2              0x108674   u8
time                   0x10836A   bcd       bytes=1
_time_sub              0x10836B   u8        start=60
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x108322   u8
_p2_chr                0x108323   u8
power                  0x10844E   u8        mult=1.5625 min=0 max=100 round=1
power_p2               0x10865E   u8        mult=1.5625 min=0 max=100 round=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"RIMURURU","3":"HANZO","4":"GALFORD","5":"KYOSHIRO","6":"UKYO","7":"GENJURO","8":"BASARA","9":"SHIZUMARU","10":"GAIRA","11":"YUMEJI","12":"JUBEI","13":"SANKURO","14":"…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAOHMARU","1":"NAKORURU","2":"RIMURURU","3":"HANZO","4":"GALFORD","5":"KYOSHIRO","6":"UKYO","7":"GENJURO","8":"BASARA","9":"SHIZUMARU","10":"GAIRA","11":"YUMEJI","12":"JUBEI","13":"SANKURO","14":"…`

## savagere — Savage Reign

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_chr                0x108468   u8        mask=127
_p2_chr                0x108469   u8        mask=127
backdrop               0x108469   u8        mask=127
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
_time                  0x1084A8   bcd       bytes=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"HAYATE","1":"EAGLE","2":"GOZU","3":"MEZU","4":"CAROL","5":"NICOLA","6":"JOKER","7":"CHUNG","8":"GORDON","9":"KING LION","10":"KING LEO","11":"CHUNG"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"HAYATE","1":"EAGLE","2":"GOZU","3":"MEZU","4":"CAROL","5":"NICOLA","6":"JOKER","7":"CHUNG","8":"GORDON","9":"KING LION","10":"KING LEO","11":"CHUNG"}}`

## sbp — Super Bubble Pop

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1074A4   be        bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## sdodgeb — Super Dodge Ball

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x101133   bcd       bytes=3
score_p2               -          bcd       bytes=4
time                   0x1065AB   bcd       bytes=1
hp1                    0x105CBD   u8        max=255
hp2                    0x105CBF   u8        max=255
hp3                    0x105CC1   u8        max=255
hp1_p2                 0x105CC5   u8        max=255
hp2_p2                 0x105CC7   u8        max=255
hp3_p2                 0x105CC9   u8        max=255
power                  0x105FD2   u16       max=36863
power_p2               0x105FDA   u16       max=36863
char1                  0x103E5B   u8
char2                  0x103E5D   u8
char3                  0x103E5F   u8
char1_p2               0x103E63   u8
char2_p2               0x103E65   u8
char3_p2               0x103E67   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `name1` = `{"value":"char1","names":{"0":"KUNIO","1":"RIKI","2":"SHINJI","3":"MISUZU","4":"KENJI","5":"MIYUKI","6":"SABU","7":"D.B.MAOU","10":"KAMEKICHI","11":"KIYOSHI","12":"MUSASHI","13":"JYOJI","14":"KEIKO","15":"KAEDE","16":"KOZUE","17"…`
- `name1_p2` = `{"value":"char1_p2","names":{"0":"KUNIO","1":"RIKI","2":"SHINJI","3":"MISUZU","4":"KENJI","5":"MIYUKI","6":"SABU","7":"D.B.MAOU","10":"KAMEKICHI","11":"KIYOSHI","12":"MUSASHI","13":"JYOJI","14":"KEIKO","15":"KAEDE","16":"KOZUE","…`
- `name2` = `{"value":"char2","names":{"0":"KUNIO","1":"RIKI","2":"SHINJI","3":"MISUZU","4":"KENJI","5":"MIYUKI","6":"SABU","7":"D.B.MAOU","10":"KAMEKICHI","11":"KIYOSHI","12":"MUSASHI","13":"JYOJI","14":"KEIKO","15":"KAEDE","16":"KOZUE","17"…`
- `name2_p2` = `{"value":"char2_p2","names":{"0":"KUNIO","1":"RIKI","2":"SHINJI","3":"MISUZU","4":"KENJI","5":"MIYUKI","6":"SABU","7":"D.B.MAOU","10":"KAMEKICHI","11":"KIYOSHI","12":"MUSASHI","13":"JYOJI","14":"KEIKO","15":"KAEDE","16":"KOZUE","…`
- `name3` = `{"value":"char3","names":{"0":"KUNIO","1":"RIKI","2":"SHINJI","3":"MISUZU","4":"KENJI","5":"MIYUKI","6":"SABU","7":"D.B.MAOU","10":"KAMEKICHI","11":"KIYOSHI","12":"MUSASHI","13":"JYOJI","14":"KEIKO","15":"KAEDE","16":"KOZUE","17"…`
- `name3_p2` = `{"value":"char3_p2","names":{"0":"KUNIO","1":"RIKI","2":"SHINJI","3":"MISUZU","4":"KENJI","5":"MIYUKI","6":"SABU","7":"D.B.MAOU","10":"KAMEKICHI","11":"KIYOSHI","12":"MUSASHI","13":"JYOJI","14":"KEIKO","15":"KAEDE","16":"KOZUE","…`

## sengoku — Sengoku

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1000B6   bcd       bytes=4
score_p2               0x1000BA   bcd       bytes=4
lives                  0x1000B3   u8
lives_p2               0x1000B5   u8
energy                 0x100305   u8        max=6
energy_p2              0x100405   u8        max=6
weapon                 0x1002F9   u8
weapon_p2              0x1003F9   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## sengoku2 — Sengoku 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1001B2   bcd       bytes=4
score_p2               0x1001B6   bcd       bytes=4
lives                  0x1001AF   u8        add=-1 min=0
lives_p2               0x1001B1   u8        add=-1 min=0
energy                 0x102CF3   u8        max=6
energy_p2              0x102DF3   u8        max=6
weapon                 0x102D29   u8
weapon_p2              0x102E29   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## sengoku3 — Sengoku 3

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x1083E6   bcd       bytes=4
score_p2               0x108404   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
health                 0x102C19   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x102D13   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
magic                  0x1083E3   u8        max=56
magic_p2               0x108401   u8        max=56
stars                  0x1083EB   u8
stars_p2               0x108409   u8
weapon                 0x1083EA   u8
weapon_p2              0x108408   u8
fighter                0x1083CA   u8
fighter_p2             0x1083CC   u8
time                   0x108457   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `fighter_name` = `{"value":"fighter","names":["BYAKKO","KAGETSURA","KONGOH","FALCON","KURENAI","OKUNI",null]}`
- `fighter_name_p2` = `{"value":"fighter_p2","names":["BYAKKO","KAGETSURA","KONGOH","FALCON","KURENAI","OKUNI",null]}`
- `weapon_name` = `{"value":"weapon","names":{"en":["SHURIKEN","KUNAI","BOMB","SAUCER"],"fr":["SHURIKEN","KUNAI","BOMBE","DISQUE"]}}`

## sf2 — Street Fighter II: The World Warrior

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF83F1   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF86F1   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
rounds                 0xFF8656   u8
rounds_p2              0xFF8956   u8
time                   0xFF8ACE   bcd       bytes=1
credits                0xFF82DD   bcd       bytes=1
_p1_chr                0xFF8657   u8
_p2_chr                0xFF8957   u8
score                  0xFF8660   bcd       bytes=4
score_p2               0xFF8960   bcd       bytes=4
backdrop               0xFFDD7F   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA"}}`

## sf2ce — Street Fighter II': Champion Edition

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF83E9   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF86E9   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
rounds                 0xFF864E   u8
rounds_p2              0xFF894E   u8
time                   0xFF8ABE   bcd       bytes=1
_p1_chr                0xFF864F   u8
_p2_chr                0xFF894F   u8
backdrop               0xFFDD5F   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA"}}`

## sf2hf — Street Fighter II': Hyper Fighting

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF83E9   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF86E9   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
rounds                 0xFF864E   u8
rounds_p2              0xFF894E   u8
time                   0xFF8ABE   bcd       bytes=1
_p1_chr                0xFF864F   u8
_p2_chr                0xFF894F   u8
score                  0xFF8658   bcd       bytes=4
backdrop               0xFFDD5F   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA"}}`

## sfa — Street Fighter Alpha: Warriors' Dreams

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8441   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF8841   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
rounds                 0xFF84C6   u8
rounds_p2              0xFF88C6   u8
_p1_ctl                0xFF84C5   u8        human=0
_p2_ctl                0xFF88C5   u8        human=0
time                   0xFFAE09   u8
power                  0xFF84BF   u8        mult=0.694444 min=0 max=100 round=1
power_p2               0xFF88BF   u8        mult=0.694444 min=0 max=100 round=1
_p1_chr                0xFF84A2   u8
_p2_chr                0xFF88A2   u8
score                  0xFF84B0   bcd       bytes=4
score_p2               0xFF88B0   bcd       bytes=4
backdrop               0xFFAE01   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"KEN","2":"GOUKI","3":"NASH","4":"CHUN LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"VEGA","11":"SAGAT","12":"DAN"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"KEN","2":"GOUKI","3":"NASH","4":"CHUN LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"VEGA","11":"SAGAT","12":"DAN"}}`

## sfa2 — Street Fighter Alpha 2

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8451   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF8851   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0xFF8109   u8
power                  0xFF849F   u8        mult=0.694444 min=0 max=100 round=1
power_p2               0xFF889F   u8        mult=0.694444 min=0 max=100 round=1
_p1_chr                0xFF8482   u8
_p2_chr                0xFF8882   u8
backdrop               0xFF8101   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"KEN MASTERS","2":"AKUMA","3":"CHARLIE","4":"CHUN-LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"M. BISON","11":"SAGAT","12":"DAN HIBIKI","13":"S.KASUGANO","14":"R.SCH…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"KEN MASTERS","2":"AKUMA","3":"CHARLIE","4":"CHUN-LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"M. BISON","11":"SAGAT","12":"DAN HIBIKI","13":"S.KASUGANO","14":"R.SCH…`

## sfa3 — Street Fighter Alpha 3

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8450   be        bytes=2 mult=0.694444 min=0 max=100 zero_from="0x8048" round=1
health_p2              0xFF8850   be        bytes=2 mult=0.694444 min=0 max=100 zero_from="0x8048" round=1
_p1_ctl                0xFF8525   u8        human=0
_p2_ctl                0xFF8925   u8        human=0
time                   0xFF8109   u8
power                  0xFF851F   u8        mult=0.694444 min=0 max=100 round=1
power_p2               0xFF891F   u8        mult=0.694444 min=0 max=100 round=1
_p1_chr                0xFF8502   u8
_p2_chr                0xFF8902   u8
score                  0xFF8510   bcd       bytes=4
rounds                 0xFF8526   u8
rounds_p2              0xFF8926   u8
backdrop               0xFF8101   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"KEN MASTERS","2":"AKUMA","3":"CHARLIE","4":"CHUN-LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"M. BISON","11":"SAGAT","12":"DAN HIBIKI","13":"S.KASUGANO","14":"R.SCH…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"KEN MASTERS","2":"AKUMA","3":"CHARLIE","4":"CHUN-LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"M. BISON","11":"SAGAT","12":"DAN HIBIKI","13":"S.KASUGANO","14":"R.SCH…`

## sfiii — Street Fighter III: New Generation

cpu :maincpu, ram_base 0x2000000, ram_size 0x80000, swap32 True

```
health                 0x200D22B  u8        mult=0.625 min=0 max=100 zero_from="0xD0" round=1
health_p2              0x200D603  u8        mult=0.625 min=0 max=100 zero_from="0xD0" round=1
time                   0x200EB33  u8
credits                0x2007188  u8
power                  0x200D949  u8        mult=0.625 min=0 max=100 round=1
power_p2               0x200D969  u8        mult=0.625 min=0 max=100 round=1
_p1_chr                0x2012E2F  u8
_p1_chr2               0x2012C7D  u8
_p2_chr                0x2012E31  u8
_p2_chr2               0x2012C7F  u8
backdrop               0x2012CA3  u8
```

`derived` :

- `p1_char` = `{"join":["_p1_chr","_p1_chr2"],"names":{"0,0":"RYU","0,1":"DUDLEY","0,2":"ALEX","0,3":"YUN","0,4":"KEN","1,0":"IBUKI","1,1":"NECRO","1,2":"SEAN","1,3":"ORO","1,4":"ELENA","0,20":"GILL"}}`
- `p2_char` = `{"join":["_p2_chr","_p2_chr2"],"names":{"0,0":"RYU","0,1":"DUDLEY","0,2":"ALEX","0,3":"YUN","0,4":"KEN","1,0":"IBUKI","1,1":"NECRO","1,2":"SEAN","1,3":"ORO","1,4":"ELENA","0,20":"GILL"}}`

## sfiii2 — Street Fighter III 2nd Impact: Giant Attack

cpu :maincpu, ram_base 0x2000000, ram_size 0x80000, swap32 True

```
health                 0x200E5A3  u8        mult=0.625 min=0 max=100 zero_from="0xD0" round=1
health_p2              0x200E9AF  u8        mult=0.625 min=0 max=100 zero_from="0xD0" round=1
time                   0x2010167  u8
credits                0x2008528  u8
power                  0x200ED35  u8        mult=0.625 min=0 max=100 round=1
power_p2               0x200ED61  u8        mult=0.625 min=0 max=100 round=1
_p1_chr                0x20142C1  u8
_p2_chr                0x20142C3  u8
backdrop               0x20142E7  u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"ALEX","2":"YUN","3":"NECRO","4":"IBUKI","5":"HUGO","6":"SEAN","7":"URIEN","8":"ELENA","9":"ORO","10":"YANG","11":"DUDLEY","12":"KEN","13":"#AKUMA#","26":"#GILL#"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"ALEX","2":"YUN","3":"NECRO","4":"IBUKI","5":"HUGO","6":"SEAN","7":"URIEN","8":"ELENA","9":"ORO","10":"YANG","11":"DUDLEY","12":"KEN","13":"#AKUMA#","26":"#GILL#"}}`

## sfiii3 — Street Fighter III 3rd Strike: Fight for the Future

cpu :maincpu, ram_base 0x2000000, ram_size 0x80000, swap32 True

```
health                 0x2068D0B  u8        mult=0.625 min=0 max=100 zero_from="0xD0" round=1
health_p2              0x20691A3  u8        mult=0.625 min=0 max=100 zero_from="0xD0" round=1
time                   0x2011377  u8
credits                0x2007CE0  u8
power                  0x20695B5  u8        mult=0.625 min=0 max=100 round=1
power_p2               0x20695E1  u8        mult=0.625 min=0 max=100 round=1
_p1_chr                0x2011387  u8
_p2_chr                0x2011388  u8
score                  0x201139C  u32
backdrop               0x2026BB0  u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"ALEX","2":"RYU","3":"YUN","4":"DUDLEY","5":"NECRO","6":"HUGO","7":"IBUKI","8":"ELENA","9":"ORO","10":"YANG","11":"KEN","12":"SEAN","13":"URIEN","14":"AKUMA","16":"CHUN-LI","17":"MAKOTO","18":"Q","…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"ALEX","2":"RYU","3":"YUN","4":"DUDLEY","5":"NECRO","6":"HUGO","7":"IBUKI","8":"ELENA","9":"ORO","10":"YANG","11":"KEN","12":"SEAN","13":"URIEN","14":"AKUMA","16":"CHUN-LI","17":"MAKOTO","18":"Q","…`

## sfz2al — Street Fighter Zero 2 Alpha

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8451   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF8851   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0xFF8109   u8
_p1_chr                0xFF8482   u8
_p2_chr                0xFF8882   u8
backdrop               0xFF8101   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"KEN","2":"AKUMA","3":"CHARLIE","4":"CHUN-LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"M. BISON","11":"SAGAT","12":"DAN","13":"SAKURA","14":"ROLENTO","15":"DHALSIM",…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"KEN","2":"AKUMA","3":"CHARLIE","4":"CHUN-LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"M. BISON","11":"SAGAT","12":"DAN","13":"SAKURA","14":"ROLENTO","15":"DHALSIM",…`

## sfzch — Street Fighter Zero

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8441   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF8841   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
rounds                 0xFF84C6   u8
rounds_p2              0xFF88C6   u8
time                   0xFFAE09   u8
power                  0xFF84BF   u8        mult=0.694444 min=0 max=100 round=1
power_p2               0xFF88BF   u8        mult=0.694444 min=0 max=100 round=1
_p1_chr                0xFF84A2   u8
_p2_chr                0xFF88A2   u8
backdrop               0xFFAE01   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"KEN","2":"GOUKI","3":"NASH","4":"CHUN LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"VEGA","11":"SAGAT","12":"DAN"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"KEN","2":"GOUKI","3":"NASH","4":"CHUN LI","5":"ADON","6":"SODOM","7":"GUY","8":"BIRDIE","9":"ROSE","10":"VEGA","11":"SAGAT","12":"DAN"}}`

## sgemf — Super Gem Fighter: Mini Mix

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8441   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF8841   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0xFF8188   bcd       bytes=1
power                  0xFF8595   u8        mult=1.041667 min=0 max=100 round=1
power_p2               0xFF8995   u8        mult=1.041667 min=0 max=100 round=1
_p1_chr                0xFF8781   u8
_p2_chr                0xFF8B81   u8
score                  0xFF8790   bcd       bytes=4
backdrop               0xFF8181   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"KEN","2":"CHUN-LI","3":"SAKURA","4":"MORRIGAN","5":"LEI-LEI","6":"FELICIA","7":"TABASA","8":"IBUKI","9":"ZANGIEF","10":"DAN","11":"GOUKI"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"KEN","2":"CHUN-LI","3":"SAKURA","4":"MORRIGAN","5":"LEI-LEI","6":"FELICIA","7":"TABASA","8":"IBUKI","9":"ZANGIEF","10":"DAN","11":"GOUKI"}}`

## shocktr2 — Shock Troopers 2nd Squad

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10900C   bcd       bytes=4
score_p2               0x10910C   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
energy                 0x1001B5   u8        max=64
energy_p2              0x1021B5   u8        max=64
soldier                0x10903B   u8
soldier_p2             0x10913B   u8
time                   0x108F7B   bcd       bytes=1
lives                  0x10905B   u8        add=-1 min=0
lives_p2               0x10915B   u8        add=-1 min=0
grenades               0x10901F   u8
grenades_p2            0x10911F   u8
power                  0x109021   u8        max=36
power_p2               0x109121   u8        max=36
ammo                   0x109016   u8
ammo_p2                0x109116   u8
weapon                 0x109015   u8
weapon_p2              0x109115   u8
_hps                   0x1023B4   u16s      count=93 stride=256
_boss                  0x108F96   u16
_wait                  0x108F78   u16
_clear                 0x108F80   u16
_stage                 0x108FC9   u8
_mission               0x108F85   u8
_area                  0x10C52A   u8
_ride                  0x109012   u8
_ride_p2               0x109112   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `char_name` = `{"value":"soldier","names":["LEON","ANGEL","LULU","TOY"]}`
- `char_name_p2` = `{"value":"soldier_p2","names":["LEON","ANGEL","LULU","TOY"]}`
- `power_lv` = `{"value":"power","names":{"0":"LV1","4":"LV1","8":"LV1","12":"LV2","16":"LV2","20":"LV2","24":"LV3","28":"LV3","32":"LV3","36":"LV3"}}`
- `power_lv_p2` = `{"value":"power_p2","names":{"0":"LV1","4":"LV1","8":"LV1","12":"LV2","16":"LV2","20":"LV2","24":"LV3","28":"LV3","32":"LV3","36":"LV3"}}`

## shocktro — Shock Troopers

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x108DB2   bcd       bytes=4
score_p2               0x108FB2   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
energy                 0x1001B5   u8        max=64
energy_p2              0x1021B5   u8        max=64
weapon                 0x108DB9   u8        shift=2
ammo                   0x108DBB   u8
member                 0x108DB7   u8        shift=2
_tm1                   0x108DC1   u8        shift=2
_tm2                   0x108DC5   u8        shift=2
_tm3                   0x108DC9   u8        shift=2
_bombs1                0x108DC3   u8
_bombs2                0x108DC7   u8
_bombs3                0x108DCB   u8
weapon_p2              0x108FB9   u8        shift=2
ammo_p2                0x108FBB   u8
member_p2              0x108FB7   u8        shift=2
_tm1_p2                0x108FC1   u8        shift=2
_tm2_p2                0x108FC5   u8        shift=2
_tm3_p2                0x108FC9   u8        shift=2
_bombs1_p2             0x108FC3   u8
_bombs2_p2             0x108FC7   u8
_bombs3_p2             0x108FCB   u8
time                   0x108D01   bcd       bytes=1
stage_id               0x108D1B   u8        shift=2
area                   0x108D33   u8        shift=4
_route_screen          0x108D2B   u8
_hps                   0x1023B4   u16s      count=93 stride=256
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `weapon_name` = `{"value":"weapon","names":{"en":["NORMAL GUN","HEAVY GUN","VULCAN GUN","3-WAY GUN","BUSTER GUN","FLAME GUN","ROCKET GUN","MISSILE GUN","HYPER GUN"],"fr":["FUSIL","FUSIL LOURD","VULCAN","TIR TRIPLE","BUSTER","LANCE-FLAMMES","ROQUE…`
- `special` = `{"pick":["_tm1","_tm2","_tm3"],"at":"member"}`
- `special_name` = `{"pick":["_tm1","_tm2","_tm3"],"at":"member","names":{"en":["GRENADE","SMOKE CAN","CAN GUN","BOOMERANG","MISSILE L.","BOW","CHEMICAL","BAZOOKA"],"fr":["GRENADE","FUMIGÈNE","BIDON","BOOMERANG","MISSILES","ARC","CHIMIQUE","BAZOOKA"…`
- `char_name` = `{"pick":["_tm1","_tm2","_tm3"],"at":"member","names":["JACKAL","MILKY","LOKI","SOUTHERN CROSS","MARIE BEE","RIO","MARU","BIG MAMA"]}`
- `bombs` = `{"pick":["_bombs1","_bombs2","_bombs3"],"at":"member"}`
- `special_p2` = `{"pick":["_tm1_p2","_tm2_p2","_tm3_p2"],"at":"member_p2"}`
- `special_name_p2` = `{"pick":["_tm1_p2","_tm2_p2","_tm3_p2"],"at":"member_p2","names":{"en":["GRENADE","SMOKE CAN","CAN GUN","BOOMERANG","MISSILE L.","BOW","CHEMICAL","BAZOOKA"],"fr":["GRENADE","FUMIGÈNE","BIDON","BOOMERANG","MISSILES","ARC","CHIMIQU…`
- `char_name_p2` = `{"pick":["_tm1_p2","_tm2_p2","_tm3_p2"],"at":"member_p2","names":["JACKAL","MILKY","LOKI","SOUTHERN CROSS","MARIE BEE","RIO","MARU","BIG MAMA"]}`
- `bombs_p2` = `{"pick":["_bombs1_p2","_bombs2_p2","_bombs3_p2"],"at":"member_p2"}`
- `weapon_name_p2` = `{"value":"weapon_p2","names":{"en":["NORMAL GUN","HEAVY GUN","VULCAN GUN","3-WAY GUN","BUSTER GUN","FLAME GUN","ROCKET GUN","MISSILE GUN","HYPER GUN"],"fr":["FUSIL","FUSIL LOURD","VULCAN","TIR TRIPLE","BUSTER","LANCE-FLAMMES","RO…`

## slammast — Saturday Night Slam Masters

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF9157   u8        mult=0.392157 min=0 max=100 round=1
health_p2              0xFF9357   u8        mult=0.392157 min=0 max=100 round=1
_time                  0xFFA0C8   digits    bytes=2
```

## socbrawl — Soccer Brawl

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
goals                  0x10B3A2   u8
goals_p2               0x10B3A4   u8
energy                 0x10B3A8   u8        max=96
energy_p2              0x10B3B0   u8        max=96
time_min               0x10BDB8   bcd       bytes=1
time_sec               0x10BDB9   bcd       bytes=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## sonic — Sonic The Hedgehog

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
score                  0xFFFE26   be        bytes=4 mult=10
rings                  0xFFFE20   be        bytes=2
lives                  0xFFFE12   u8
zone                   0xFFFE10   u8
act                    0xFFFE11   u8
mode                   0xFFF600   u8
```

## sonic2 — Sonic The Hedgehog 2

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
score                  0xFFFE26   be        bytes=4 mult=10
rings                  0xFFFE20   be        bytes=2
lives                  0xFFFE12   u8
zone                   0xFFFE10   u8
act                    0xFFFE11   u8
mode                   0xFFF600   u8
```

## sonicwi2 — Aero Fighters 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10E436   bcd       bytes=4
score_p2               0x10E498   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x10E43F   u8        zero_from=240
lives_p2               0x10E4A1   u8        zero_from=240
bombs                  0x10E457   u8
bombs_p2               0x10E4B9   u8
power                  0x10E443   u8        max=3
power_p2               0x10E4A5   u8        max=3
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## sonicwi3 — Aero Fighters 3

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10E896   bcd       bytes=4
score_p2               0x10E8EC   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x10E89B   u8        zero_from=240
lives_p2               0x10E8F1   u8        zero_from=240
bombs                  0x10E8BA   u8
bombs_p2               0x10E910   u8
power                  0x10E8B0   u8        max=4
power_p2               0x10E906   u8        max=4
plane                  0x1003AB   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `pilot_name` = `{"value":"plane","names":["KEATON","BLAZERS","HIEN","MAO MAO","CHAIKA & POOSHKA","SPANKY","MALCOLM","KOWFUL & RIVER","ALEX & PICTUS","ELLEN & CINDY","KOTOMI","THE MAN"]}`
- `plane_name` = `{"value":"plane","names":["F4U CORSAIR","P-61 BLACK WIDOW","A6M ZERO","M6A1 SEIRAN","IL-2 STURMOVIK","I-16","DO 335 PFEIL","JU 87 STUKA","WHIRLWIND","SWORDFISH","RED RABBIT","DIABLOON"]}`

## spf2t — Super Puzzle Fighter II Turbo

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF8076   u8
_major                 0xFF8001   u8
_minor                 0xFF8005   u8
_sub                   0xFF8009   u8
_vs                    0xFF0C8B   u8
_p2_in                 0xFF8780   u8
_rounds_vs             0xFF80A3   u8
_p1_chr                0xFF8382   u8
_p2_chr                0xFF8782   u8
score                  0xFF83AA   be        bytes=4
score_p2               0xFF87AA   be        bytes=4
well1                  0xFFAB00   u16s      count=112 stride=2
well2                  0xFFAD00   u16s      count=112 stride=2
pair1                  0xFF8452   u16s      count=4 stride=2
pair2                  0xFF8852   u16s      count=4 stride=2
x1                     0xFF8311   u8
y1                     0xFF8315   u8
rot1                   0xFF8470   u8
x2                     0xFF8711   u8
y2                     0xFF8715   u8
rot2                   0xFF8870   u8
wins1                  0xFF83A3   u8
wins2                  0xFF87A3   u8
chain1                 0xFF849C   u8
chain2                 0xFF889C   u8
atk1                   0xFF849E   u8
atk2                   0xFF889E   u8
pcs1                   0xFF84F5   u8
pcs2                   0xFF88F5   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"MORRIGAN","1":"CHUN-LI","2":"RYU","3":"KEN","4":"LEI-LEI","5":"DONOVAN","6":"FELICIA","7":"SAKURA","8":"DEVILOT","9":"AKUMA","10":"DAN"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"MORRIGAN","1":"CHUN-LI","2":"RYU","3":"KEN","4":"LEI-LEI","5":"DONOVAN","6":"FELICIA","7":"SAKURA","8":"DEVILOT","9":"AKUMA","10":"DAN"}}`
- `p1_mode` = `{"sum":[{"all":[{"eq":["_major",2]},{"between":["_minor",2,4]}]},{"all":[{"eq":["_major",2]},{"eq":["_minor",6]}]},{"all":[{"eq":["_major",2]},{"eq":["_minor",6]}]}]}`
- `p2_mode` = `{"sum":[{"all":[{"all":[{"eq":["_major",2]},{"between":["_minor",2,4]}]},{"ge":[{"sum":[{"eq":["_p2_in",2]},{"eq":["_vs",1]}]},1]}]},{"all":[{"all":[{"eq":["_major",2]},{"eq":["_minor",6]}]},{"ge":[{"sum":[{"eq":["_p2_in",2]},{"e…`
- `_one` = `{"value":1}`

## spinmast — Spin Master

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10500C   bcd       bytes=4
score_p2               0x105034   bcd       bytes=4
lives                  0x105015   u8
lives_p2               0x10503D   u8
energy                 0x105F62   u8        max=5
energy_p2              0x106022   u8        max=5
bombs                  0x105FBD   u8
bombs_p2               0x10607D   u8
weapon                 0x105F55   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ssf2 — Super Street Fighter II: The New Challengers

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF83F9   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF87F9   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
rounds                 0xFF875E   u8
rounds_p2              0xFF8B5E   u8
time                   0xFF8CCE   bcd       bytes=1
_p1_chr                0xFF875F   u8
_p2_chr                0xFF8B5F   u8
backdrop               0xFFE08B   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"E.HONDA","2":"BLANKA","3":"GUILE","4":"KEN MASTERS","5":"CHUN-LI","6":"ZANGIEF","7":"DHALSIM","8":"BALROG","9":"SAGAT","10":"VEGA","11":"M. BISON","12":"CAMMY","13":"T.HAWK","14":"FEI LO…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"E.HONDA","2":"BLANKA","3":"GUILE","4":"KEN MASTERS","5":"CHUN-LI","6":"ZANGIEF","7":"DHALSIM","8":"BALROG","9":"SAGAT","10":"VEGA","11":"M. BISON","12":"CAMMY","13":"T.HAWK","14":"FEI LO…`

## ssf2t — Super Street Fighter II Turbo

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8479   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
health_p2              0xFF8879   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
time                   0xFF8DCE   bcd       bytes=1
power                  0xFF8702   u8        mult=2.083333 min=0 max=100 round=1
power_p2               0xFF8B02   u8        mult=2.083333 min=0 max=100 round=1
_p1_chr                0xFF87DF   u8
_p2_chr                0xFF8BDF   u8
backdrop               0xFFE18B   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA","12":"CAMMY","13":"T. HAWK","14":"FEI LONG","1…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RYU","1":"E. HONDA","2":"BLANKA","3":"GUILE","4":"KEN","5":"CHUN LI","6":"ZANGIEF","7":"DHALSIM","8":"M. BISON","9":"SAGAT","10":"BALROG","11":"VEGA","12":"CAMMY","13":"T. HAWK","14":"FEI LONG","1…`

## ssideki — Super Sidekicks

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
goals                  0x1090F2   bcd       bytes=1
goals_p2               0x1090F3   bcd       bytes=1
time_min               0x108ED2   bcd       bytes=1
time_sec               0x108ED3   bcd       bytes=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ssideki2 — Super Sidekicks 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
goals                  0x1044C4   u8
goals_p2               0x1044C8   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ssideki3 — Super Sidekicks 3 - The Next Glory

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
goals                  0x1051EA   u8
goals_p2               0x1051EE   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## ssideki4 — The Ultimate 11 - The SNK Football Championship

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
goals                  0x105A2A   u8
goals_p2               0x105A2E   u8
power                  0x105A4F   u8        max=95
power_p2               0x105A53   u8        max=95
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## stakwin — Stakes Winner

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
speed                  0x100275   u8        max=8
stamina                0x100277   u8        max=8
strength               0x10027B   u8        max=8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## stakwin2 — Stakes Winner 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
power                  0x1089E2   u8        max=234
power_p2               0x108BA0   u8        max=255
speed                  0x1080F8   u8        max=7
stamina                0x1080F9   u8        max=7
burst                  0x1080FA   u8        max=7
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## strhoop — Street Hoop

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
points                 0x101A0B   bcd       bytes=1
points_p2              0x101A0F   bcd       bytes=1
time_min               0x101A52   u8
time_sec               0x101A53   bcd       bytes=1
half                   0x101A49   u8
super                  0x101A5A   u8        max=192
super_p2               0x101A5C   u8        max=192
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## strider — Strider

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_time                  0xFF0F6A   bcd       bytes=1
score                  0xFF0CB6   bcd       bytes=4
score_p2               -          bcd       bytes=4
lives                  0xFF0CA8   u8
pods                   0xFF0CE4   u8
```

`derived` :

- `_one` = `{"value":1}`

## superspy — The Super Spy

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10189C   bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
energy                 0x10181F   u8        max=8
exp                    0x10181B   u8
weapon                 0x101856   u8
ammo                   0x1017F6   bcd       bytes=2
ammo_mg                0x101854   bcd       bytes=2
knife                  0x101878   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## svc — SNK vs. Capcom

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x10A131   u8
_p2_dir                0x10A3B1   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10A239   u8        mult=0.446429 min=0 max=100 zero_from="0xF0"
health_p2              0x10A4B9   u8        mult=0.446429 min=0 max=100 zero_from="0xF0"
rounds                 0x10AC59   u8
rounds_p2              0x10AC58   u8
time                   0x10AC14   bcd       bytes=1
_fight_cue             0x10CC8A   u8        start=225
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10AC30   u8
_p2_chr                0x10AC54   u8
backdrop               0x10ABDC   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"KYO","1":"IORI","2":"RYO","3":"TERRY","4":"MAI","5":"KASUMI","6":"KIM","7":"MR.KARATE","8":"CHOI","9":"EARTHQUAKE","10":"GENJYURO","11":"SHIKI","12":"GEESE","13":"MARS","14":"GOENITZ","15":"ATHENA…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"KYO","1":"IORI","2":"RYO","3":"TERRY","4":"MAI","5":"KASUMI","6":"KIM","7":"MR.KARATE","8":"CHOI","9":"EARTHQUAKE","10":"GENJYURO","11":"SHIKI","12":"GEESE","13":"MARS","14":"GOENITZ","15":"ATHENA…`

## svcpcb — SNK vs. Capcom (JAMMA PCB)

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x10A131   u8
_p2_dir                0x10A3B1   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10A239   u8        mult=0.446429 min=0 max=100 zero_from="0xF0"
health_p2              0x10A4B9   u8        mult=0.446429 min=0 max=100 zero_from="0xF0"
rounds                 0x10AC59   u8
rounds_p2              0x10AC58   u8
time                   0x10AC14   bcd       bytes=1
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x101353   u8
_p2_chr                0x1013D3   u8
backdrop               0x10ABDC   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"KYO","1":"IORI","2":"RYO","3":"TERRY","4":"MAI","5":"KASUMI","6":"KIM","7":"MR.KARATE","8":"CHOI","9":"EARTHQUAKE","10":"GENJYURO","11":"SHIKI","12":"GEESE","13":"MARS","14":"GOENITZ","15":"ATHENA…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"KYO","1":"IORI","2":"RYO","3":"TERRY","4":"MAI","5":"KASUMI","6":"KIM","7":"MR.KARATE","8":"CHOI","9":"EARTHQUAKE","10":"GENJYURO","11":"SHIKI","12":"GEESE","13":"MARS","14":"GOENITZ","15":"ATHENA…`

## theroes — Thunder Heroes

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
health                 0x1058C9   u8        mult=1.041667 min=0 max=100 zero_from="0xB0" round=1
health_p2              0x1059C9   u8        mult=1.041667 min=0 max=100 zero_from="0xB0" round=1
time                   0x105809   u8
credits                0x10257D   u8
lives                  0x1058C7   u8
lives_p2               0x1059C7   u8
_p1_chr                0x1058BB   u8
_p2_chr                0x1059BB   u8
stage                  0x105803   u8        add=1
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"JIMY","2":"KOHEN","3":"KOUFU","4":"FRED","5":"#GETUKI#","6":"#SEIYEN#","7":"#ROB#"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"JIMY","2":"KOHEN","3":"KOUFU","4":"FRED","5":"#GETUKI#","6":"#SEIYEN#","7":"#ROB#"}}`

## tophuntr — Top Hunter - Roddy & Cathy

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x108D30   bcd       bytes=4
score_p2               0x108D34   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x108D1D   u8        add=-1 min=0
lives_p2               0x108D21   u8        add=-1 min=0
health                 0x108D39   u8        max=64
health_p2              0x108D3B   u8        max=64
power                  0x108D0D   u8        max=5
power_p2               0x108D11   u8        max=5
time                   0x108CC2   bcd       bytes=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## tpgolf — Top Player's Golf

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
strokes                0x100106   u8
holes                  0x10022C   u8
time                   0x10021B   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## trally — Thrash Rally

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
time                   0x103611   bcd       bytes=1
speed                  0x10B0C4   u16       max=1002
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## turfmast — Neo Turf Masters

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
club                   0x106FDF   u8
power                  0x106FE7   u8
wind                   0x106FE1   u8
wind_dir               0x106FE3   u8
strokes                0x107006   u8
strokes_p2             0x10702C   u8
golfer                 0x107005   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `club_name` = `{"value":"club","names":["1W","3W","4W","1I","3I","4I","5I","6I","7I","8I","9I","PW","SW","PT"]}`
- `club_yards` = `{"value":"club","names":["260","240","230","220","200","190","180","170","160","150","140","120","100","28"]}`
- `golfer_name` = `{"value":"golfer","names":{"en":["USA","BRAZIL","GERMANY","JAPAN","AUSTRALIA","ENGLAND"],"fr":["USA","BRÉSIL","ALLEMAGNE","JAPON","AUSTRALIE","ANGLETERRE"]}}`

## twinspri — Twinkle Star Sprites

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10C000   be        bytes=4
score_p2               0x10D000   be        bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
pos_x                  0x102502   be        bytes=2 mult=0.0078125 add=-137 round=1
pos_y                  0x102500   be        bytes=2 mult=-0.0078125 add=351 round=1
pos_x_p2               0x105902   be        bytes=2 mult=0.0078125 add=-137 round=1
pos_y_p2               0x105900   be        bytes=2 mult=-0.0078125 add=351 round=1
lives                  0x10C014   u8        mult=0.125 min=0 max=5 round=1
lives_p2               0x10D014   u8        mult=0.125 min=0 max=5 round=1
bombs                  0x10C021   u8
bombs_p2               0x10D021   u8
power                  0x10C08A   u16       max=12288
power_p2               0x10D08A   u16       max=12288
attack                 0x10C088   u8
attack_p2              0x10D088   u8
char                   0x10C007   u8
char_p2                0x10D007   u8
hits                   0x10C8F1   u8
hits_p2                0x10D8F1   u8
wins                   0x10C006   u8        valid=[0,9]
wins_p2                0x10D006   u8        valid=[0,9]
stage                  0x10BB00   u8        add=1
perfect                0x10C221   u8
perfect_p2             0x10D221   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

`derived` :

- `name` = `{"value":"char","names":["LOAD RAN","MACKY & PENTELL","ARTHUR SCHMIDT","YAN YANYUNG","GRIFFON","REALLY TILL","TINKER & LINKER","NANJA MONJA","KIM","SPRITES","DARK RAN","MEVIOUS","MEMORY"]}`
- `name_p2` = `{"value":"char_p2","names":["LOAD RAN","MACKY & PENTELL","ARTHUR SCHMIDT","YAN YANYUNG","GRIFFON","REALLY TILL","TINKER & LINKER","NANJA MONJA","KIM","SPRITES","DARK RAN","MEVIOUS","MEMORY"]}`

## twsoc96 — Tecmo World Soccer '96

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## unsquad — U.N. Squadron

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF0FFE   u8
bombs                  0xFF15E3   u8
weapon                 0xFF15E1   u8
power                  0xFF15D3   u8        max=6
score                  0xFF1611   digits    bytes=7 mult=10
score_p2               0xFF1691   digits    bytes=7 mult=10
```

`derived` :

- `weapon_name` = `{"value":"weapon","names":{"0":"PHOENIX","4":"FALCON","8":"BOMB","12":"BOMB II","16":"NAPALM","20":"NAPALM II","28":"BULLPUP","32":"BULLPUP II","52":"SUPER SHELL","56":"SUPER SHELL II"}}`

## uopoko — Puzzle Uo Poko

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
credits                0x100195   u8
stage                  0x100203   u8        add=1
bubble                 0x1022F1   u8
bubble_p2              0x1022F3   u8
score                  0x100218   be        bytes=4
score_p2               -          bcd       bytes=4
```

## varth — Varth: Operation Thunderstorm

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
credits                0xFF82AB   u8
lives                  0xFF83A4   u8
lives_p2               0xFF84A4   u8
bombs                  0xFF83B3   u8
power                  0xFF83B1   u8        max=7
weapon                 0xFF83B2   u8
pods                   0xFF83B8   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
```

`derived` :

- `weapon_name` = `{"value":"weapon","names":{"0":"NORMAL","2":"3-WAY","4":"LASER"}}`

## vhunt2 — Vampire Hunter 2: Darkstalkers Revenge

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8450   be        bytes=2 mult=0.173611 min=0 max=100 zero_from="0x8120" round=1
health_p2              0xFF8850   be        bytes=2 mult=0.173611 min=0 max=100 zero_from="0x8120" round=1
_p1_ctl                0xFF87B4   u8        human=0
_p2_ctl                0xFF8BB4   u8        human=0
time                   0xFF8109   u8
power                  0xFF8509   be        bytes=2 mult=0.003946 min=0 max=100 round=1
power_p2               0xFF8909   be        bytes=2 mult=0.003946 min=0 max=100 round=1
_p1_chr                0xFF8782   u8
_p2_chr                0xFF8B82   u8
backdrop               0xFF8101   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"#.B.HOOD","1":"D.MAXIMOV","2":"JON TALBAIN","3":"V.V.GELDENH","4":"LORD RAPTOR","5":"M.AENSLAND","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"RIKUO","10":"SASQUATCH","11":"#.RAPTOR","12":"#Q-B…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"#.B.HOOD","1":"D.MAXIMOV","2":"JON TALBAIN","3":"V.V.GELDENH","4":"LORD RAPTOR","5":"M.AENSLAND","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"RIKUO","10":"SASQUATCH","11":"#.RAPTOR","12":"#Q-B…`

## viewpoin — Viewpoint

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10009C   bcd       bytes=4
score_p2               0x1000A8   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x108D99   u8
lives_p2               0x1090ED   u8
bomb_type              0x108D8F   u8
bomb_type_p2           0x1090E3   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## vsav — Vampire Savior: The Lord of Vampire

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8450   be        bytes=2 mult=0.347222 min=0 max=100 zero_from="0x8090" round=1
health_p2              0xFF8850   be        bytes=2 mult=0.347222 min=0 max=100 zero_from="0x8090" round=1
time                   0xFF8109   u8
_p1_chr                0xFF8782   u8
_p2_chr                0xFF8B82   u8
backdrop               0xFF8101   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"B.B.HOOD","1":"D.MAXIMOV","2":"JON TALBAIN","3":"V.V.GELDENH","4":"LORD RAPTOR","5":"M.AENSLAND","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"RIKUO","10":"SASQUATCH","11":"#.RAPTOR","12":"Q-BE…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"B.B.HOOD","1":"D.MAXIMOV","2":"JON TALBAIN","3":"V.V.GELDENH","4":"LORD RAPTOR","5":"M.AENSLAND","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"RIKUO","10":"SASQUATCH","11":"#.RAPTOR","12":"Q-BE…`

## vsav2 — Vampire Savior 2: The Lord of Vampire

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF8450   be        bytes=2 mult=0.347222 min=0 max=100 zero_from="0x8090" round=1
health_p2              0xFF8850   be        bytes=2 mult=0.347222 min=0 max=100 zero_from="0x8090" round=1
time                   0xFF8109   u8
_p1_chr                0xFF8782   u8
_p2_chr                0xFF8B82   u8
backdrop               0xFF8101   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"BULLETA","1":"DIMITRI","2":"GALLON","3":"VICTOR","4":"ZABEL","5":"MORRIGAN","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"AULBATH","10":"SASQUATCH","12":"Q-BEE","13":"LEI-LEI","14":"LILITH","15…`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"BULLETA","1":"DIMITRI","2":"GALLON","3":"VICTOR","4":"ZABEL","5":"MORRIGAN","6":"ANAKARIS","7":"FELICIA","8":"BISHAMON","9":"AULBATH","10":"SASQUATCH","12":"Q-BEE","13":"LEI-LEI","14":"LILITH","15…`

## wakuwak7 — Waku Waku 7

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100119   u8
_p2_dir                0x100259   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10014A   u8        mult=0.392157 min=0 max=100
health_p2              0x10028A   u8        mult=0.392157 min=0 max=100
time                   0x1066D5   u8        max=99
score                  0x100166   be        bytes=4 mult=10
score_p2               0x1002A6   be        bytes=4 mult=10
_p1_chr                0x106997   u8
_p2_chr                0x1069A1   u8
backdrop               0x107B1C   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"RAI","1":"ARINA","2":"SLASH","3":"DANDY-J","4":"TESS","5":"MAURU","6":"POLITANK-Z","7":"FERNANDEZ","8":"BONUS"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"RAI","1":"ARINA","2":"SLASH","3":"DANDY-J","4":"TESS","5":"MAURU","6":"POLITANK-Z","7":"FERNANDEZ","8":"BONUS"}}`

## wh1 — World Heroes

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100021   u8        mask="0x80"
_p2_dir                0x100121   u8        mask="0x80"
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10600A   u8        mult=0.961538 min=0 max=100 zero_from="0xB4"
health_p2              0x10610A   u8        mult=0.961538 min=0 max=100 zero_from="0xB4"
time                   0x10B008   bcd       bytes=1
_time_sub              0x10B009   u8        start=30
_fight_cue             0x100FA1   u8        start=6
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x10600C   u8
_p2_chr                0x10610C   u8
backdrop               0x10B005   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"DRAGON","2":"HANZO","3":"MUSCLE","4":"J.CARN","5":"JANNE","6":"RASPUTIN","7":"FUUMA","8":"BROCKEN","9":"GEEGUS"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"DRAGON","2":"HANZO","3":"MUSCLE","4":"J.CARN","5":"JANNE","6":"RASPUTIN","7":"FUUMA","8":"BROCKEN","9":"GEEGUS"}}`

## wh2 — World Heroes 2

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100021   u8        mask="0x80"
_p2_dir                0x100121   u8        mask="0x80"
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10600C   u8        mult=0.847458 min=0 max=100 zero_from="0xBB"
health_p2              0x10610C   u8        mult=0.847458 min=0 max=100 zero_from="0xBB"
time                   0x10C109   bcd       bytes=1
_time_sub              0x10B009   u8        start=30
_fight_cue             0x10C338   u8        start=0
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x106004   u8
_p2_chr                0x106104   u8
backdrop               0x10B005   u8
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"DRAGON","2":"HANZOU","3":"MUSCLE","4":"J.CARN","5":"JANNE","6":"RASPUTIN","7":"FUUMA","8":"BROCKEN","9":"SHURA","10":"RYOKO","11":"KIDD","12":"MUDMAN","13":"ERICK","14":"J.MAX","15":"DIO","16":"GE…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"DRAGON","2":"HANZOU","3":"MUSCLE","4":"J.CARN","5":"JANNE","6":"RASPUTIN","7":"FUUMA","8":"BROCKEN","9":"SHURA","10":"RYOKO","11":"KIDD","12":"MUDMAN","13":"ERICK","14":"J.MAX","15":"DIO","16":"GE…`

## wh2j — World Heroes 2 Jet

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x100021   u8        mask="0x80"
_p2_dir                0x100121   u8        mask="0x80"
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10600C   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
health_p2              0x10610C   u8        mult=1.041667 min=0 max=100 zero_from="0xB0"
time                   0x10C109   bcd       bytes=1
_time_sub              0x10B009   u8        start=30
_fight_cue             0x102387   u8        start=80
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x106004   u8
_p2_chr                0x106104   u8
backdrop               0x10B005   u8
round                  0x10C121   u8        add=-1 min=0
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"DRAGON","2":"HANZOU","3":"MUSCLE","4":"J.CARN","5":"JANNE","6":"RASPUTIN","7":"FUUMA","8":"BROCKEN","9":"SHURA","10":"RYOKO","11":"KIDD","12":"MUDMAN","13":"ERICK","14":"J.MAX","15":"JACK","16":"R…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"DRAGON","2":"HANZOU","3":"MUSCLE","4":"J.CARN","5":"JANNE","6":"RASPUTIN","7":"FUUMA","8":"BROCKEN","9":"SHURA","10":"RYOKO","11":"KIDD","12":"MUDMAN","13":"ERICK","14":"J.MAX","15":"JACK","16":"R…`

## whp — World Heroes Perfect

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
_in_p1                 0x10FD96   u8        fast=true
_in_p2                 0x10FD9C   u8        fast=true
_p1_dir                0x108295   u8
_p2_dir                0x108295   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
health                 0x10600C   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
health_p2              0x10610C   u8        mult=0.520833 min=0 max=100 zero_from="0xE0"
time                   0x10C109   bcd       bytes=1
_time_sub              0x10B009   u8        start=30
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
_p1_chr                0x106004   u8
_p2_chr                0x106104   u8
backdrop               0x10B005   u8
power                  0x106A16   be        bytes=2 mult=0.44843 min=0 max=100 round=1
power_p2               0x106B16   be        bytes=2 mult=0.44843 min=0 max=100 round=1
round                  0x10C121   u8        add=-1 min=0
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"1":"DRAGON","2":"HANZOU","3":"MUSCLE","4":"J.CARN","5":"JANNE","6":"RASPUTIN","7":"FUUMA","8":"BROCKEN","9":"SHURA","10":"RYOKO","11":"KIDD","12":"MUDMAN","13":"ERICK","14":"J.MAX","15":"JACK","16":"R…`
- `p2_char` = `{"value":"_p2_chr","names":{"1":"DRAGON","2":"HANZOU","3":"MUSCLE","4":"J.CARN","5":"JANNE","6":"RASPUTIN","7":"FUUMA","8":"BROCKEN","9":"SHURA","10":"RYOKO","11":"KIDD","12":"MUDMAN","13":"ERICK","14":"J.MAX","15":"JACK","16":"R…`

## willow — Willow

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
_time                  0xFF83C7   bcd       bytes=1
credits                0xFF82A2   u8
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
lives                  0xFF8342   u8
health                 0xFF8362   u8        mult=16.666667 min=0 max=100 zero_from="0x83" round=1
hero                   0xFF8386   u8
```

`derived` :

- `_one` = `{"value":1}`

## wjammers — Windjammers

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
set_points             0x100873   bcd       bytes=1
set_points_p2          0x1008F3   bcd       bytes=1
time                   0x10008D   bcd       bytes=1
court                  0x100324   u8
to_win                 0x1000FF   bcd       bytes=1
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
p1_x                   0x100806   u16       fast=true
p1_y                   0x10080A   u16       fast=true
p2_x                   0x100886   u16       fast=true
p2_y                   0x10088A   u16       fast=true
sets                   0x100872   u8        valid=[0,3]
sets_p2                0x1008F2   u8        valid=[0,3]
score                  0x100066   bcd       bytes=3
score_p2               0x10006A   bcd       bytes=3
disc_x                 0x100A06   u16       fast=true
disc_y                 0x100A0A   u16       fast=true
disc_h                 0x100A44   s16       fast=true
disc_state             0x100A20   u16       fast=true
disc_last              0x100A3A   u16
p1_state               0x10081A   u16       fast=true
p2_state               0x10089A   u16       fast=true
p1_chr                 0x10031D   u8        mult=0.25 valid=[0,5]
p2_chr                 0x10031F   u8        mult=0.25 valid=[0,5]
bios_country           0x10FD83   u8
```

`derived` :

- `court_name` = `{"value":"court","names":{"en":["BEACH","LAWN","TILES","CONCRETE","CLAY","STADIUM"],"fr":["PLAGE","GAZON","CARRELAGE","BÉTON","TERRE BATTUE","STADE"]}}`
- `p1_name` = `{"value":"p1_chr","names":["G. SCOTT","J. COSTA","K. WESSEL","B. YOO","L. BIAGGI","H. MITA"]}`
- `p2_name` = `{"value":"p2_chr","names":["G. SCOTT","J. COSTA","K. WESSEL","B. YOO","L. BIAGGI","H. MITA"]}`
- `p1_nation` = `{"value":"p1_chr","names":{"en":["USA","SPAIN","GERMANY","KOREA","ITALY","JAPAN"],"fr":["USA","ESPAGNE","ALLEMAGNE","CORÉE","ITALIE","JAPON"]}}`
- `p2_nation` = `{"value":"p2_chr","names":{"en":["USA","SPAIN","GERMANY","KOREA","ITALY","JAPAN"],"fr":["USA","ESPAGNE","ALLEMAGNE","CORÉE","ITALIE","JAPON"]}}`

## wof — Warriors of Fate

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFFBE9F   u8        mult=0.961538 min=0 max=100 zero_from="0xB4" round=1
health_p2              0xFFBF7F   u8        mult=0.961538 min=0 max=100 zero_from="0xB4" round=1
_time                  0xFF81B2   u8
credits                0xFF62F7   u8
lives                  0xFF7F9B   u8
lives_p2               0xFF7F9C   u8
score                  0xFF7F8C   bcd       bytes=3 mult=100
score_p2               0xFF7F90   bcd       bytes=3 mult=100
```

## wofch — Tenchi wo Kurau II: Sekiheki no Tatakai

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
health                 0xFFBE9F   u8        mult=0.961538 min=0 max=100 zero_from="0xB4" round=1
_time                  0xFF81B2   u8
credits                0xFF62F7   u8
lives                  0xFF7F9B   u8
```

## xmcota — X-Men: Children of the Atom

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
health                 0xFF4191   u8        mult=0.699301 min=0 max=100 zero_from="0xC7" round=1
health_p2              0xFF4591   u8        mult=0.699301 min=0 max=100 zero_from="0xC7" round=1
time                   0xFF4808   bcd       bytes=1
power                  0xFF4195   u8        mult=0.704225 min=0 max=100 round=1
power_level            0xFF4198   u8        add=1 max=3
power_p2               0xFF4595   u8        mult=0.704225 min=0 max=100 round=1
power_level_p2         0xFF4598   u8        add=1 max=3
_p1_chr                0xFF4051   u8
_p2_chr                0xFF4451   u8
score                  0xFF4184   bcd       bytes=4
score_p2               0xFF4584   bcd       bytes=4
rounds                 0xFF4802   u8
rounds_p2              0xFF4803   u8
backdrop               0xFF488F   u8
_p1_ctl                0xFF4003   u8        human=1
_p2_ctl                0xFF4403   u8        human=1
_time_sub              0xFF4809   u8        start=40
```

`derived` :

- `p1_char` = `{"value":"_p1_chr","names":{"0":"WOLVERINE","2":"PSYLOCKE","4":"COLOSSUS","6":"CYCLOPS","8":"STORM","10":"ICEMAN","12":"SPIRAL","14":"S.SAMURAI","16":"OMEGA RED","18":"SENTINEL","20":"#JUGGERNAUT","22":"#MAGNETO","24":"#GOUKI"}}`
- `p2_char` = `{"value":"_p2_chr","names":{"0":"WOLVERINE","2":"PSYLOCKE","4":"COLOSSUS","6":"CYCLOPS","8":"STORM","10":"ICEMAN","12":"SPIRAL","14":"S.SAMURAI","16":"OMEGA RED","18":"SENTINEL","20":"#JUGGERNAUT","22":"#MAGNETO","24":"#GOUKI"}}`

## xmvsf — X-Men Vs. Street Fighter

cpu :maincpu, ram_base 0xFF0000, ram_size 0x10000, swap16 True

```
time                   0xFF5008   bcd       bytes=1
power                  0xFF4213   u8        mult=0.694444 min=0 max=100 round=1
power_level            0xFF4214   u8        max=3
power_p2               0xFF4613   u8        mult=0.694444 min=0 max=100 round=1
power_level_p2         0xFF4614   u8        max=3
_p1_chr                0xFF4053   u8
_p2_chr                0xFF4453   u8
score                  0xFF4204   bcd       bytes=4
score_p2               0xFF4604   bcd       bytes=4
rounds                 0xFF5002   u8
rounds_p2              0xFF5003   u8
_p1_ctl                0xFF4003   u8        human=1
_p2_ctl                0xFF4403   u8        human=1
_p1_hp1                0xFF4211   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p1_hp2                0xFF4A11   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p1_chr2               0xFF4853   u8
_p2_hp1                0xFF4611   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p2_hp2                0xFF4E11   u8        mult=0.694444 min=0 max=100 zero_from="0xC8" round=1
_p2_chr2               0xFF4C53   u8
```

`tag` :

- `health` = `{"team":[[1,"_p1_hp1","_p1_hp1"],[0,"_p1_hp2","_p1_hp2"]]}`
- `health_p2` = `{"team":[[1,"_p2_hp1","_p2_hp1"],[0,"_p2_hp2","_p2_hp2"]]}`

`derived` :

- `p1_char` = `{"team":[[1,"_p1_hp1","_p1_chr"],[0,"_p1_hp2","_p1_chr2"]],"names":{"0":"WOLVERINE","2":"CYCLOPS","4":"STORM","6":"ROGUE","8":"GAMBIT","10":"SABRETOOTH","12":"JUGGERNAUT","14":"MAGNETO","16":"#APOCALYPSE","18":"RYU","20":"KEN MAS…`
- `p2_char` = `{"team":[[1,"_p2_hp1","_p2_chr"],[0,"_p2_hp2","_p2_chr2"]],"names":{"0":"WOLVERINE","2":"CYCLOPS","4":"STORM","6":"ROGUE","8":"GAMBIT","10":"SABRETOOTH","12":"JUGGERNAUT","14":"MAGNETO","16":"#APOCALYPSE","18":"RYU","20":"KEN MAS…`

## zedblade — Zed Blade

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x10024C   bcd       bytes=4
score_p2               0x10004C   bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
lives                  0x100229   u8        add=-1 min=0
bombs                  0x10022F   u8
shot_level             0x100261   u8        max=3
shot_type              0x100263   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
lives_p2               0x100029   u8        add=-1 min=0
bombs_p2               0x10002F   u8
```

## zintrckb — Zintrick

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  -          bcd       bytes=4
score_p2               -          bcd       bytes=4
p1_input               0x10FD96   u8
p2_input               0x10FD9C   u8
time                   0x10C419   u8
energy                 0x10C455   u8        max=18
item                   0x10C444   u8        max=18
level                  0x10C452   u8
energy_p2              0x10C4D5   u8        max=18
item_p2                0x10C4C4   u8        max=18
level_p2               0x10C4D2   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

## zupapa — Zupapa!

cpu :maincpu, ram_base 0x100000, ram_size 0x10000, swap16 True

```
score                  0x102000   bcd       bytes=4
score_p2               0x102010   bcd       bytes=4
lives                  0x1002C1   u8        add=-1 min=0
lives_p2               0x1002C3   u8        add=-1 min=0
time                   0x101C16   u8
credits                0xD00034   bcd       bytes=1 mame_only=true
p1_mode                0x10FDB6   u8
p2_mode                0x10FDB7   u8
bios_request           0x10FDAE   u8
bios_mode              0x10FDAF   u8
bios_timer             0x10FDDA   bcd       bytes=1
bios_mvs               0x10FD82   u8
```

