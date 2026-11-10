Already have a Pixelcade LED? It does the job on its own, see [[Pixelcade LED]]. Otherwise, three ways to get a marquee display.

## Option A, a ready-made ZeDMD

A 128 x 32 RGB DMD is two 64 x 32 HUB75 LED modules side by side, exactly the ZeDMD format, the open-source DMD of the virtual pinball world. Some shops sell it assembled, for example in France.

- SmallCab, "Pack ZeDMD S3 – P2.5" https://www.smallcab.net/pack-zedmd-p-3182.html
- Benfactory, "ZeDMD" https://benfactory.fr/produit/zedmd/

At P2.5 (2.5 mm between two LEDs) the panel is about 32 x 8 cm, the size of a pinball DMD. Check on the product page what is included (power supply, frame).

## Option B, a bigger LED panel

With bigger LEDs (P4 or P5) the panel fills the top of a cabinet. Measure the top of your cabinet first.

| Pitch | One 64 x 32 module | Full 128 x 32 panel |
|---|---|---|
| P3 | 19.2 x 9.6 cm | 38 x 10 cm |
| P4 | 25.6 x 12.8 cm | 51 x 13 cm |
| P5 | 32 x 16 cm | 64 x 16 cm |

| Qty | Item | Note |
|---|---|---|
| 2 | RGB HUB75 LED module 64 x 32, indoor, 1/16 scan | Waveshare P4 around $18 each, cheaper on AliExpress |
| 1 | ESP32-S3-DevKitC-1 **N16R8** | around €10 to €15, the board recommended by ZeDMD |
| 1 | ZeDMD shield for ESP32-S3 (SmallCab, Benfactory, Arnoz) | saves wiring 14 wires by hand, adds the menu buttons |
| 1 | 5 V 10 A power supply (Mean Well LRS-50-5 type) | a module can draw 4 A at full white, a DMD stays far below |
| 1 | USB-C **data** cable | to the cabinet PC |

Avoid "outdoor" modules and 1/8 scan modules. Modules with FM6126A or ICN2038S chips work too, once the "panel driver" is set with ZeDMD_Updater2.

### Assembly

1. Plug the shield into the HUB75 input of the first module (the arrow on the back shows the data direction).
2. Connect the output of module 1 to the input of module 2 with the supplied ribbon cable.
3. Power both modules with 5 V from the power supply.
4. Connect the ESP32-S3 to the PC through its **native** USB port (the one marked USB, on the left of the DevKitC-1).

Without a shield, the wiring is in the ZeDMD README ("ZeDMD pinout diagram") https://github.com/PPUC/ZeDMD

### Firmware

1. Download ZeDMD_Updater2 (Windows) https://github.com/zesinger/ZeDMD_Updater2 and flash the **ZeDMD S3 128x32** variant.
2. At first boot the panel shows a menu. Set the colour order (red must be red), the brightness, "USB packet size" to 1024 and "min refresh" to around 90 Hz, then **Exit**.
3. A panel from a pre-flashed kit needs the update too. Recent libzedmd versions expect a recent firmware.

### In ArcadeDMD

Answer yes to the ZeDMD question of `install.bat`. It downloads libzedmd and turns the `zedmd` output on. `test_panel.bat` shows a test pattern.

If the libzedmd download fails, get the `win-mingw-x64-Release` archive from https://github.com/PPUC/libzedmd/releases and copy all its DLLs into `ArcadeDMD\libzedmd\`. Take the mingw version, the other one lacks DLLs that zedmd64.dll needs.

The search for the panel queries the COM ports (never the Pixelcade's). To never touch light guns, set the panel's port (`"device": "COM5"`) or exclude theirs (`"ignore_devices": ["COM3", "COM4"]`).

## Option C, an LCD screen

An LCD screen shows the scenes in smooth HD with the animated backdrops (see [[HD Marquee]]). For a marquee, look for a "stretched bar LCD", a very long and thin screen. Measure the marquee window of your cabinet, then choose the biggest visible area that fits.

| Size | Resolution | Visible area, about | Note |
|---|---|---|---|
| 12.3" | 1920 x 720 | 29 x 11 cm | close to a pinball DMD |
| 14.9" | 1280 x 390 | 36 x 11 cm | sold as a marquee kit for Vewlix-type cabinets |
| 19" | 1920 x 360 | 48 x 9 cm | |
| 24" | 1920 x 360 | 58 x 11 cm | the format of the AtGames Legends Ultimate LCD marquees |

Take a screen sold with its HDMI controller board and its power supply. A bare panel (LVDS or eDP connector) needs a separate board. A standard PC monitor works too if the top of the cabinet can hold it. Hide what is outside the marquee window and set the window to the visible band with `x`, `y`, `width` and `height`.

ArcadeDMD only draws on screens that Windows sees as displays. Check this before buying a marquee that comes with its own software, such as the Pixelcade LCD (its own small computer, reached over the network) or the AtGames Legends BitLCD HD (driven by its own app over USB).
