"""HD backdrops of the eighth batch of Neo Geo games done one by one (1.24), each drawn after screenshots of its game.
Everything is drawn by the program, no image comes from a game. The backdrops register in hd_bg.BUILDERS when this
module is imported.

Décors HD du huitième lot (1.24), chacun dessiné d'après des captures de son jeu. Tout est dessiné par le programme,
aucune image tirée d'un jeu.
"""

import random

from PIL import Image

from . import hd_bg
from .hd_bg import mix, vgrad
from .hd_themes3 import _Pic, _rgba

FF_FIELD = (150, 120, 1770, 440)      # Football Frenzy: left, top, right, bottom of the field at s = 1 / le terrain
PS_FLOOR = 404                        # Power Spikes II: the floor of the court / le sol du terrain


def build_ff_field(W, H, s, seed=301):
    """Football Frenzy: the field seen from above, as in the game: the bright green grass and its stripes, the white
    yard lines every five yards, the numbers, the coloured end zones, the stands around.
    / Le terrain vu de haut : la pelouse et ses bandes, les lignes blanches, les numéros, les zones d'en-but."""
    rng = random.Random(seed)
    sky = Image.new("RGB", (W, H), (40, 44, 60))
    p = _Pic(W, H, 2, 4 * W)
    for _ in range(900):                                                 # le public autour
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        p.disc(x, y, rng.uniform(3, 6) * s, rng.choice(((200, 60, 60, 255), (60, 90, 200, 255), (230, 220, 200, 255), (240, 200, 60, 255),
                                                          (90, 90, 100, 255))))
    x0, y0, x1, y1 = (v * s for v in FF_FIELD)
    p.poly([(x0 - 30 * s, y0 - 20 * s), (x1 + 30 * s, y0 - 20 * s), (x1 + 30 * s, y1 + 20 * s), (x0 - 30 * s, y1 + 20 * s)], (40, 120, 50, 255))
    ez = 100 * s
    span = (x1 - x0 - 2 * ez)
    for k in range(20):                                                  # les bandes de la pelouse
        a = x0 + ez + span * k / 20
        p.poly([(a, y0), (a + span / 20, y0), (a + span / 20, y1), (a, y1)], (70, 170, 70, 255) if k % 2 else (60, 156, 62, 255))
    p.poly([(x0, y0), (x0 + ez, y0), (x0 + ez, y1), (x0, y1)], (190, 50, 50, 255))
    p.poly([(x1 - ez, y0), (x1, y0), (x1, y1), (x1 - ez, y1)], (50, 80, 190, 255))
    for k in range(21):                                                  # les lignes tous les cinq yards
        a = x0 + ez + span * k / 20
        p.line([(a, y0), (a, y1)], (250, 250, 250, 255), (3 if k % 2 == 0 else 2) * s)
        for j in (0.33, 0.67):
            p.line([(a - 6 * s, y0 + (y1 - y0) * j), (a + 6 * s, y0 + (y1 - y0) * j)], (250, 250, 250, 255), 2 * s)
    p.line([(x0, y0), (x1, y0)], (250, 250, 250, 255), 4 * s)
    p.line([(x0, y1), (x1, y1)], (250, 250, 250, 255), 4 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


def build_ps2_arena(W, H, s, seed=311):
    """Power Spikes II: the indoor arena, as in the game: rows of bright lamps under the roof, the stands full of
    people, the lit scoreboard, the blue boards around the court and its floor. / La salle : projecteurs, tribunes,
    tableau d'affichage, panneaux bleus autour du terrain et son parquet."""
    rng = random.Random(seed)
    sky = vgrad(W, H, [(0.0, (10, 12, 20)), (0.4, (30, 30, 40)), (1.0, (40, 40, 50))])
    p = _Pic(W, H, 2, 4 * W)
    for row in range(2):                                                 # les projecteurs
        for k in range(14):
            x = (k + 0.5 * row) * W / 13
            y = (24 + row * 30) * s
            p.ellipse(x - 30 * s, y - 8 * s, x + 30 * s, y + 8 * s, (250, 250, 220, 255))
    for row in range(6):                                                 # les tribunes et le public
        y = (90 + row * 34) * s
        p.poly([(0, y), (W, y), (W, y + 30 * s), (0, y + 30 * s)], _rgba(mix((50, 50, 66), (80, 80, 96), row / 6)))
        x = 0
        while x < W:
            p.disc(x + rng.uniform(-3, 3) * s, y + 12 * s, rng.uniform(6, 9) * s, rng.choice(((200, 60, 60, 255), (60, 90, 200, 255),
                                                                                              (230, 220, 200, 255), (240, 200, 60, 255),
                                                                                              (60, 160, 90, 255))))
            x += rng.uniform(16, 24) * s
    cx = W / 2                                                           # le tableau d'affichage
    p.poly([(cx - 140 * s, 96 * s), (cx + 140 * s, 96 * s), (cx + 140 * s, 170 * s), (cx - 140 * s, 170 * s)], (20, 20, 24, 255), (90, 90, 100, 255), 3 * s)
    by = (PS_FLOOR - 70) * s                                             # les panneaux bleus autour du terrain
    p.poly([(0, by), (W, by), (W, by + 52 * s), (0, by + 52 * s)], (30, 60, 180, 255))
    x = 0
    while x < W:
        w = rng.uniform(160, 260) * s
        p.poly([(x + 20 * s, by + 12 * s), (x + w - 20 * s, by + 12 * s), (x + w - 20 * s, by + 40 * s), (x + 20 * s, by + 40 * s)],
               rng.choice(((250, 250, 250, 255), (240, 220, 60, 255), (220, 60, 60, 255))))
        x += w
    fy = (PS_FLOOR - 18) * s
    p.poly([(0, fy), (W, fy), (W, H), (0, H)], (210, 150, 90, 255))     # le parquet
    p.poly([(0, fy), (W, fy), (W, fy + 6 * s), (0, fy + 6 * s)], (240, 240, 240, 255))
    for k in range(16):
        x = k * W / 15
        p.line([(x, fy + 6 * s), (x - 40 * s, H)], (190, 130, 76, 255), 2 * s)
    sky = sky.convert("RGBA")
    sky.alpha_composite(p.done())
    return {"sky": sky.convert("RGB"), "layers": [], "tw": W, "amb": {}}


hd_bg.BUILDERS.update({"ff_field": build_ff_field, "ps2_arena": build_ps2_arena})
