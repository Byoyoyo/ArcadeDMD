"""The cells of a Super Puzzle Fighter II Turbo well as the game keeps them (1.34), for the HD screen and the LED panel.

Each well is 14 rows of 8 words, a wall (0x00FF), the 6 cells, a wall; row 0 is hidden. A cell, low byte L and high
byte H: 1 to 4 a gem (blue, yellow, green, red), 9 to 12 a crash gem, 5 the diamond, L & 15 = 7 a counter gem (colour
H >> 4, count H & 15), 6 a counter at 0 turning into a gem of colour H >> 4, L & 0x80 a power gem (colour L & 7, its
neighbours in H: 0x10 up, 0x20 right, 0x40 down, 0x80 left), 0x1x 0x2x 0x6x 0x7x a gem bursting. Read in two games
recorded on a cabinet and checked on their screenshots.

Les cases d'un puits de Super Puzzle Fighter II Turbo telles que le jeu les garde, pour l'écran HD et la dalle LED.
"""

ROWS, COLS = 13, 6
COLORS = {1: (52, 118, 240), 2: (250, 204, 48), 3: (56, 196, 84), 4: (232, 48, 60)}   # blue, yellow, green, red


def decode(v):
    """(kind, colour, extra) of one cell, or None. / Genre, couleur et détail d'une case, ou None."""
    if not isinstance(v, int) or isinstance(v, bool) or v <= 0:
        return None
    lo, hi = v & 0xFF, (v >> 8) & 0xFF
    if lo & 0x80:
        return ("power", lo & 7 or 1, hi & 0xF0)
    if lo & 0x0F == 7:
        return ("counter", (hi >> 4) or 1, hi & 0x0F)
    if lo == 6:
        return ("gem", (hi >> 4) or 1, 0)
    if lo == 5:
        return ("diamond", 0, 0)
    if 1 <= lo <= 4:
        return ("gem", lo, 0)
    if 9 <= lo <= 12:
        return ("crash", lo - 8, 0)
    return ("burst", ((lo - 1) & 3) + 1, lo)


def grid_of(words):
    """The 14 x 6 cells of one well from its 112 words, walls left out, or None. / Les cases d'un puits, sans les murs."""
    if not isinstance(words, list) or len(words) < 112:
        return None
    return [[words[r * 8 + 1 + k] for k in range(COLS)] for r in range(14)]


def heights(grid):
    """How high each column is filled, 0 to 13. / Hauteur de chaque colonne."""
    out = []
    for k in range(COLS):
        h = 0
        for r in range(1, 14):
            if decode(grid[r][k]):
                h = 14 - r
                break
        out.append(h)
    return out


def danger(grid):
    """0 to 1, how close the well is to being full, its middle columns (where the pairs come in) counting most.
    / De 0 à 1, à quel point le puits est près d'être plein, ses colonnes du milieu comptant le plus."""
    hs = heights(grid)
    spawn = max(hs[2], hs[3])
    return max(min(1.0, max(0.0, (max(hs) - 8) / 5)) * 0.85, min(1.0, max(0.0, (spawn - 6) / 6)))
