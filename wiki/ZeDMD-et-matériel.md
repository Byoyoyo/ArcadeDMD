Tu as déjà une Pixelcade LED ? Elle suffit, voir [[Dalle Pixelcade]]. Sinon, trois façons d'avoir un affichage de marquee.

## Option A, une ZeDMD toute faite

Un DMD RGB 128 x 32, c'est deux modules LED HUB75 64 x 32 côte à côte, exactement le format ZeDMD, le DMD open source du monde du flipper virtuel. Des boutiques la vendent montée, en France par exemple.

- SmallCab, « Pack ZeDMD S3 – P2.5 » https://www.smallcab.net/pack-zedmd-p-3182.html
- Benfactory, « ZeDMD » https://benfactory.fr/produit/zedmd/

En P2.5 (2,5 mm entre deux LED) la dalle fait environ 32 x 8 cm, la taille d'un DMD de flipper. Vérifie sur la fiche du produit ce qui est fourni (alimentation, cadre).

## Option B, une dalle LED plus grande

Avec des LED plus grosses (P4 ou P5) la dalle remplit le haut d'une borne. Mesure d'abord le haut de ta borne.

| Pas | Un module 64 x 32 | Dalle complète 128 x 32 |
|---|---|---|
| P3 | 19,2 x 9,6 cm | 38 x 10 cm |
| P4 | 25,6 x 12,8 cm | 51 x 13 cm |
| P5 | 32 x 16 cm | 64 x 16 cm |

| Qté | Élément | Remarque |
|---|---|---|
| 2 | module LED RGB HUB75 64 x 32, intérieur, scan 1/16 | Waveshare P4 vers 18 $ pièce, moins cher sur AliExpress |
| 1 | ESP32-S3-DevKitC-1 **N16R8** | de 10 à 15 € environ, la carte conseillée par ZeDMD |
| 1 | shield ZeDMD pour ESP32-S3 (SmallCab, Benfactory, Arnoz) | évite de câbler 14 fils à la main, ajoute les boutons du menu |
| 1 | alimentation 5 V 10 A (type Mean Well LRS-50-5) | un module peut tirer 4 A en blanc plein, un DMD reste bien en dessous |
| 1 | câble USB-C **data** | vers le PC de la borne |

Évite les modules « outdoor » et les modules en scan 1/8. Les modules à puces FM6126A ou ICN2038S marchent aussi, une fois le « panel driver » réglé avec ZeDMD_Updater2.

### Montage

1. Branche le shield sur l'entrée HUB75 du premier module (la flèche au dos montre le sens des données).
2. Relie la sortie du module 1 à l'entrée du module 2 avec la nappe fournie.
3. Alimente les deux modules en 5 V depuis l'alimentation.
4. Branche l'ESP32-S3 au PC par son port USB **natif** (celui marqué USB, à gauche sur la DevKitC-1).

Sans shield, le câblage est dans le README de ZeDMD (« ZeDMD pinout diagram ») https://github.com/PPUC/ZeDMD

### Firmware

1. Télécharge ZeDMD_Updater2 (Windows) https://github.com/zesinger/ZeDMD_Updater2 et flashe la variante **ZeDMD S3 128x32**.
2. Au premier démarrage, la dalle affiche un menu. Règle l'ordre des couleurs (le rouge doit être rouge), la luminosité, « USB packet size » à 1024 et « min refresh » vers 90 Hz, puis **Exit**.
3. Une dalle d'un kit déjà flashé a besoin de la mise à jour aussi. Les versions récentes de libzedmd attendent un firmware récent.

### Dans ArcadeDMD

Réponds oui à la question ZeDMD de `install.bat`. Il télécharge libzedmd et allume la sortie `zedmd`. `test_panel.bat` affiche une mire.

Si le téléchargement de libzedmd échoue, prends l'archive `win-mingw-x64-Release` sur https://github.com/PPUC/libzedmd/releases et copie toutes ses DLL dans `ArcadeDMD\libzedmd\`. Prends bien la version mingw, l'autre n'a pas les DLL dont zedmd64.dll a besoin.

La recherche de la dalle interroge les ports COM (jamais celui de la Pixelcade). Pour ne jamais toucher aux pistolets, donne le port de la dalle (`"device": "COM5"`) ou exclus les leurs (`"ignore_devices": ["COM3", "COM4"]`).

## Option C, un écran LCD

Un écran LCD montre les scènes en HD lisse avec les décors animés (voir [[Marquee HD]]). Pour un marquee, cherche un « stretched bar LCD », un écran très long et très fin. Mesure la fenêtre du marquee de ta borne, puis choisis la plus grande surface visible qui y tient.

| Taille | Résolution | Surface visible, environ | Remarque |
|---|---|---|---|
| 12,3" | 1920 x 720 | 29 x 11 cm | proche d'un DMD de flipper |
| 14,9" | 1280 x 390 | 36 x 11 cm | vendu en kit de marquee pour les bornes type Vewlix |
| 19" | 1920 x 360 | 48 x 9 cm | |
| 24" | 1920 x 360 | 58 x 11 cm | le format des marquees LCD des AtGames Legends Ultimate |

Prends un écran vendu avec sa carte contrôleur HDMI et son alimentation. Une dalle nue (connecteur LVDS ou eDP) demande une carte à part. Un écran de PC standard marche aussi si le haut de la borne peut le recevoir. Cache ce qui dépasse de la fenêtre du marquee et cale la fenêtre sur la bande visible avec `x`, `y`, `width` et `height`.

ArcadeDMD ne dessine que sur les écrans que Windows voit comme des écrans. Vérifie-le avant d'acheter un marquee livré avec son propre logiciel, comme la Pixelcade LCD (son propre petit ordinateur, joint par le réseau) ou l'AtGames Legends BitLCD HD (piloté par sa propre appli en USB).
