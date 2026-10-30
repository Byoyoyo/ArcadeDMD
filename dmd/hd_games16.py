"""HD scenes of the small Capcom CPS games done one by one (1.30), each drawn after screenshots of its game: Quiz
Tonosama no Yabou 2, Quiz Nanairo Dreams, Jyangokushi, Janpai Puzzle Choukou, Gulun.Pa!, Pnickies, Frog Feast,
Pokonyan! Balloon, Magical Pumpkin and Ganbare! Marine Kun. Most of them have no value known in their memory, so they
play by themselves; the time, the lives and the credits are shown when the game gives them. The faces, the frogs, the
balloon, the pumpkin carriage and the blobs are creations of the program in the spirit of the games, the licensed
characters of some of them are left out.

Scènes HD des petits jeux Capcom CPS faits un par un (1.30), chacune dessinée d'après des captures de son jeu. La
plupart n'ont aucune valeur connue dans leur mémoire, elles jouent donc toutes seules ; le temps, les vies et les
crédits s'affichent quand le jeu les donne. Les visages, les grenouilles, le ballon, le carrosse citrouille et les
bulles sont des créations du programme, les personnages sous licence de certains jeux sont laissés de côté.
"""

import math

from .hd_games import AMBER, CREAM, GOLD, P1C, P2C, WHITE, GameScene, _mix, _n
from .hd_games11 import MahjongScene, QuizScene
from .hd_themes16 import BW_CELL, BW_COLS, BW_ROWS, BW_TOP, BW_WELLS, FF_BANKS, FF_PADS, THEMES
from .i18n import tr

INK = (30, 24, 34, 255)


# ============================================================================ the quizzes / les quiz
class TonosamaScene(QuizScene):
    """Quiz Tonosama no Yabou 2 as in the game: the castle of a warring lord against a red sky, its flames and its war
    banners, a lord of our own and a ninja of our own, the question panel and its four answers; the lives read in the
    game decide right or wrong. / Le château d'un seigneur de guerre sur un ciel rouge, ses flammes et ses bannières,
    un seigneur et un ninja à nous, le panneau des questions ; les vies lues dans le jeu disent juste ou faux."""
    THEME = "qz_castle"
    FACES = (((230, 180, 140), (30, 24, 24), (200, 160, 60), None, (150, 30, 30)), ((220, 170, 130), (20, 20, 20), None, (40, 40, 60), (70, 40, 90)))
    PANEL = (120, 30, 30)


class NanairoScene(QuizScene):
    """Quiz Nanairo Dreams as in the game: a town park at dusk, its trees, its street lamps, its fountain and a pale
    rainbow, a girl and a boy of our own, the question panel and its four answers. / Un parc de la ville au crépuscule,
    ses arbres, ses réverbères, sa fontaine et un arc-en-ciel pâle, une fille et un garçon à nous, le panneau des questions."""
    THEME = "qz_park"
    FACES = (((240, 200, 180), (240, 120, 150), (250, 250, 250), None, (140, 190, 250)), ((230, 190, 160), (120, 80, 50), None, None, (250, 220, 130)))
    PANEL = (60, 80, 190)


# ============================================================================ mahjong / mahjong
class JyangokushiScene(MahjongScene):
    """Jyangokushi as in the game: the green felt in its red lacquer frame, the tiles with their blue backs, the points
    on the right. / Le tapis vert dans son cadre laqué rouge, les tuiles et leurs dos bleus, les points à droite."""
    THEME = "mj_kingdom"
    BACK = (60, 90, 210)


class ChoukouScene(MahjongScene):
    """Janpai Puzzle Choukou as in the game: the tiles laid on the red silk in its golden frame; two equal tiles are
    taken when a line with two turns at most joins them, the golden line shows the way. When no pair is left the tiles
    are shuffled, when the board is empty a new one comes. The time read in the game. / Les tuiles posées sur la soie
    rouge ; deux tuiles pareilles s'en vont quand une ligne d'au plus deux coudes les relie, la ligne dorée montre le
    chemin. Sans paire possible les tuiles sont mélangées, le plateau vide en amène un autre. Le temps lu dans le jeu."""
    THEME = "mj_redsilk"
    BACK = (200, 60, 50)
    COLS, ROWS = 12, 4
    SCALE = 0.8

    def deal(self, now):
        super().deal(now)
        kinds = [self.tile() for _ in range(self.COLS * self.ROWS // 2)] * 2
        self.rng.shuffle(kinds)
        self.board = [[kinds[r * self.COLS + c] for c in range(self.COLS)] for r in range(self.ROWS)]
        self.link = None
        self.pairs = getattr(self, "pairs", 0)
        self.next_t = now + 1.0

    def cell_xy(self, r, c):
        S = self.S
        tw, th = S(self.TW) * self.SCALE, S(self.TH) * self.SCALE
        x0 = self.W / 2 - self.COLS * tw / 2
        return x0 + (c + 0.5) * tw, S(132) + (r + 0.5) * th

    def path(self, a, b):
        """The cells of a line with two turns at most from a to b through empty cells, the border included, or None.
        / Les cases d'une ligne d'au plus deux coudes de a à b, par des cases vides, le bord compris."""
        R, C = self.ROWS, self.COLS

        def free(r, c):
            return (r, c) == b or not (0 <= r < R and 0 <= c < C) or self.board[r][c] is None
        best = None
        todo = [(a, d, 0, [a]) for d in ((0, 1), (0, -1), (1, 0), (-1, 0))]
        seen = {}
        while todo:
            (r, c), d, turns, way = todo.pop()
            nr, nc = r + d[0], c + d[1]
            if not (-1 <= nr <= R and -1 <= nc <= C) or not free(nr, nc):
                continue
            nway = way + [(nr, nc)]
            if (nr, nc) == b:
                if best is None or len(nway) < len(best):
                    best = nway
                continue
            for nd in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                t = turns + (nd != d)
                if t > 2 or (nd[0] == -d[0] and nd[1] == -d[1]):
                    continue
                key = (nr, nc, nd)
                if seen.get(key, 9) <= t:
                    continue
                seen[key] = t
                todo.append(((nr, nc), nd, t, nway))
        return best

    def find_pair(self):
        cells = [(r, c) for r in range(self.ROWS) for c in range(self.COLS) if self.board[r][c] is not None]
        self.rng.shuffle(cells)
        for i, a in enumerate(cells):
            for b in cells[i + 1:]:
                if self.board[a[0]][a[1]] == self.board[b[0]][b[1]]:
                    way = self.path(a, b)
                    if way:
                        return a, b, way
        return None

    def update(self, vals, now):
        if now < self.next_t:
            return
        if self.link is not None:                                           # the pair leaves / la paire s'en va
            a, b, way, t0 = self.link
            for (r, c) in (a, b):
                x, y = self.cell_xy(r, c)
                self.fx.glow(x, y, 6, 70, (255, 220, 120), 0.5, "front", 1.0, 0.0, hot=0.8)
                self.board[r][c] = None
            self.pairs += 1
            x, y = self.cell_xy(*a)
            self.popup("+100", x, y - self.S(40), GOLD, 30)
            self.link = None
            self.next_t = now + 0.5
            if all(t is None for row in self.board for t in row):
                self.slam(tr("BRAVO !", "CLEAR!"), GOLD, now, 1.4)
                self.next_t = now + 1.8
                self.fx.later(1.6, self.deal, now + 1.6)
            return
        got = self.find_pair()
        if got is None:                                                     # no pair left: shuffle / plus de paire : on mélange
            left = [t for row in self.board for t in row if t is not None]
            self.rng.shuffle(left)
            k = 0
            for r in range(self.ROWS):
                for c in range(self.COLS):
                    if self.board[r][c] is not None:
                        self.board[r][c] = left[k]
                        k += 1
            self.popup(tr("MÉLANGE", "SHUFFLE"), self.W / 2, self.S(250), CREAM, 34)
            self.next_t = now + 1.0
            return
        a, b, way = got
        self.link = (a, b, way, now)
        self.next_t = now + 0.55

    def draw_table(self, screen, vals, now):
        pg, S = self.pg, self.S
        for r in range(self.ROWS):
            for c in range(self.COLS):
                t = self.board[r][c]
                if t is None:
                    continue
                img = self.timg(t, self.SCALE)
                x, y = self.cell_xy(r, c)
                lit = self.link is not None and (r, c) in (self.link[0], self.link[1])
                screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2 - (S(6) if lit else 0))))
                if lit:
                    pg.draw.rect(screen, (255, 220, 90), (int(x - img.get_width() / 2) - S(2), int(y - img.get_height() / 2) - S(8),
                                                          img.get_width() + S(4), img.get_height() + S(4)), max(2, S(4)), border_radius=S(6))
        if self.link is not None:                                           # the golden line / la ligne dorée
            pts = [self.cell_xy(r, c) for r, c in self.link[2]]
            pg.draw.lines(screen, (255, 200, 60), False, [(int(x), int(y)) for x, y in pts], max(3, S(8)))
            pg.draw.lines(screen, (255, 250, 200), False, [(int(x), int(y)) for x, y in pts], max(1, S(3)))

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        self.draw_table(screen, vals, now)
        self.hd.draw_logo(screen, logo, W / 2, S(18), S(420), S(84), now)
        self.box(screen, S(40), S(150), S(250), S(64), (250, 200, 80), fill=(40, 10, 10, 220), radius=8, width=3)
        self.text(screen, tr("PAIRES", "PAIRS"), S(60), S(182), 22, (250, 200, 80), key="black", valign="middle", glow=0)
        self.hd.put_number(screen, str(self.pairs), "black", S(36), WHITE, S(270), S(182), "right", "middle")
        t = _n(vals.get("time"))
        if t is not None:
            self.label(screen, tr(f"TEMPS {int(t)}", f"TIME {int(t)}"), W - S(180), S(182), 30, (255, 230, 120), align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W / 2, S(420), 28, col, align="center")


# ============================================================================ the blob wells / les puits de bulles
BLOB_RGB = ((240, 70, 90), (70, 150, 250), (90, 210, 90), (250, 200, 50), (180, 90, 230))


def blob_draw(col, face=True):
    """A round blob of ours with its two eyes. / Une bulle ronde à nous et ses deux yeux."""
    def fn(d, W, H):
        d.ellipse([W * 0.04, H * 0.06, W * 0.96, H * 0.98], fill=col + (255,), outline=_mix(col, (0, 0, 0), 0.45) + (255,), width=max(1, int(W * 0.06)))
        d.ellipse([W * 0.2, H * 0.16, W * 0.46, H * 0.36], fill=_mix(col, (255, 255, 255), 0.6) + (255,))
        if face:
            for ex in (0.36, 0.64):
                d.ellipse([W * (ex - 0.1), H * 0.38, W * (ex + 0.1), H * 0.62], fill=(255, 255, 255, 255))
                d.ellipse([W * (ex - 0.04), H * 0.46, W * (ex + 0.05), H * 0.6], fill=INK)
    return fn


class BlobWell:
    """A well where pairs of blobs fall; four of a colour that touch pop, the ones above fall and can chain.
    / Un puits où tombent des paires de bulles ; quatre de la même couleur qui se touchent éclatent, et ça s'enchaîne."""

    def __init__(self, scene, cx):
        self.sc, self.rng = scene, scene.rng
        S = scene.S
        self.C = S(BW_CELL)
        self.x0, self.y0 = S(cx) - BW_COLS * self.C / 2, S(BW_TOP)
        self.next = (self.rng.randrange(5), self.rng.randrange(5))
        self.chains = 0                                   # (tests)
        self.popped = 0
        self.reset()

    def reset(self):
        self.grid = [[None] * BW_COLS for _ in range(BW_ROWS)]
        for r in range(BW_ROWS - 3, BW_ROWS):                               # a few blobs to start with / quelques bulles au départ
            for c in range(BW_COLS):
                if self.rng.random() < 0.7:
                    self.grid[r][c] = self.rng.randrange(5)
        self.settle()
        while self.groups():
            for (r, c) in self.groups()[0]:
                self.grid[r][c] = None
            self.settle()
        self.pair = None
        self.pop = None
        self.chain = 0

    def settle(self):
        for c in range(BW_COLS):
            col = [self.grid[r][c] for r in range(BW_ROWS) if self.grid[r][c] is not None]
            for r in range(BW_ROWS):
                k = r - (BW_ROWS - len(col))
                self.grid[r][c] = col[k] if k >= 0 else None

    def groups(self):
        seen, out = set(), []
        for r in range(BW_ROWS):
            for c in range(BW_COLS):
                if self.grid[r][c] is None or (r, c) in seen:
                    continue
                col, todo, grp = self.grid[r][c], [(r, c)], []
                seen.add((r, c))
                while todo:
                    y, x = todo.pop()
                    grp.append((y, x))
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < BW_ROWS and 0 <= nx < BW_COLS and (ny, nx) not in seen and self.grid[ny][nx] == col:
                            seen.add((ny, nx))
                            todo.append((ny, nx))
                if len(grp) >= 4:
                    out.append(grp)
        return out

    def height(self, c):
        for r in range(BW_ROWS):
            if self.grid[r][c] is not None:
                return r
        return BW_ROWS

    def choose(self, cols):
        """Where the pair goes: next to blobs of its colour, low. / Où va la paire : près de sa couleur, en bas."""
        best, score = 0, None
        for c in range(BW_COLS - 1):
            sc = 0.0
            for k, cc in enumerate((c, c + 1)):
                r = self.height(cc) - 1
                if r < 1:
                    sc -= 50
                    continue
                for ny, nx in ((r + 1, cc), (r, cc - 1), (r, cc + 1)):
                    if 0 <= ny < BW_ROWS and 0 <= nx < BW_COLS and self.grid[ny][nx] == cols[k]:
                        sc += 3
                sc += r * 0.3
            sc += self.rng.random() * 1.5
            if score is None or sc > score:
                best, score = c, sc
        return best

    def step(self, dt, now):
        sc = self.sc
        if self.pop is not None:                                            # blobs popping / des bulles éclatent
            cells, t0 = self.pop
            if now - t0 < 0.45:
                return
            for (r, c) in cells:
                self.grid[r][c] = None
            self.settle()
            self.pop = None
            g = self.groups()
            if g:
                self.burst(g, now)
            else:
                self.chain = 0
            return
        if self.pair is None:
            cols = self.next
            self.next = (self.rng.randrange(5), self.rng.randrange(5))
            c = self.choose(cols)
            if self.height(c) < 2 or self.height(c + 1) < 2:                # the well is full: it empties / le puits est plein
                sc.popup(tr("PLEIN !", "FULL!"), self.x0 + BW_COLS * self.C / 2, sc.S(240), (255, 120, 120), 34)
                self.reset()
                return
            self.pair = [c, -1.0, cols]
            return
        c, y, cols = self.pair
        y += dt * 7.0
        land = min(self.height(c), self.height(c + 1)) - 1
        if y >= land:
            self.grid[land][c], self.grid[land][c + 1] = cols
            self.settle()
            self.pair = None
            g = self.groups()
            if g:
                self.burst(g, now)
        else:
            self.pair[1] = y

    def burst(self, groups, now):
        sc = self.sc
        self.chain += 1
        cells = [cell for g in groups for cell in g]
        self.popped += len(cells)
        self.pop = (cells, now)
        for (r, c) in cells:
            x, y = self.xy(r, c)
            sc.fx.glow(x, y, 4, 40, BLOB_RGB[self.grid[r][c]], 0.45, "front", 1.0, 0.0, hot=0.6)
        x, y = self.xy(*cells[0])
        if self.chain >= 2:
            self.chains += 1
            sc.popup(f"{self.chain} CHAIN!", self.x0 + BW_COLS * self.C / 2, y - sc.S(30), GOLD, 34)
        else:
            sc.popup(f"+{len(cells) * 10}", x, y - sc.S(20), CREAM, 26)

    def xy(self, r, c):
        return self.x0 + (c + 0.5) * self.C, self.y0 + (r + 0.5) * self.C

    def draw(self, screen, now):
        sc = self.sc
        size = int(self.C)
        popping = set(self.pop[0]) if self.pop is not None else set()
        for r in range(BW_ROWS):
            for c in range(BW_COLS):
                v = self.grid[r][c]
                if v is None:
                    continue
                img = sc.img(("blob", v, size), size, size, blob_draw(BLOB_RGB[v]), ss=2)
                x, y = self.xy(r, c)
                if (r, c) in popping and int(now * 16) % 2 == 0:
                    continue
                screen.blit(img, (int(x - size / 2), int(y - size / 2)))
        if self.pair is not None:
            c, y, cols = self.pair
            for k in (0, 1):
                img = sc.img(("blob", cols[k], size), size, size, blob_draw(BLOB_RGB[cols[k]]), ss=2)
                screen.blit(img, (int(self.x0 + (c + k) * self.C), int(self.y0 + y * self.C)))


class BlobScene(GameScene):
    """The shared part of Gulun.Pa! and Pnickies: their wells, the pairs that fall by themselves, NEXT and the chains.
    / La part commune : les puits, les paires qui tombent toutes seules, NEXT et les enchaînements."""
    STATIC = True
    SHADE = (60, 0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.wells = [BlobWell(self, cx) for cx in BW_WELLS[self.THEME]]

    def update(self, vals, now):
        for i, w in enumerate(self.wells):
            if i == 0 or self.p2_in(vals):                              # the well of player 2 plays when he does
                w.step(self.dt, now)

    def draw_next(self, screen, well, x, y):
        S = self.S
        size = int(well.C)
        self.box(screen, x, y, S(90), S(110), (250, 220, 120), fill=(10, 8, 30, 210), radius=10, width=3)
        self.text(screen, "NEXT", x + S(45), y + S(18), 20, (250, 220, 120), key="black", align="center", valign="middle", glow=0)
        for k in (0, 1):
            img = self.img(("blob", well.next[k], size), size, size, blob_draw(BLOB_RGB[well.next[k]]), ss=2)
            screen.blit(img, (int(x + S(45) - size / 2), int(y + S(36) + k * size)))


class GulunpaScene(BlobScene):
    """Gulun.Pa! as in the game: the starry purple sky and its planets, two wells between golden pillars, the pairs of
    round creatures of our own that fall and pop four by four; HI, 1P and 2P in the middle as in the game, NEXT beside
    each well. / Le ciel violet étoilé et ses planètes, deux puits entre des colonnes dorées, les paires de petites
    bêtes rondes à nous qui tombent et éclatent quatre par quatre ; NEXT à côté de chaque puits, comme dans le jeu."""
    THEME = "bw_space"

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        for w in self.wells:
            w.draw(screen, now)
        self.draw_next(screen, self.wells[0], S(500), S(80))
        self.draw_next(screen, self.wells[1], W - S(590), S(80))
        self.hd.draw_logo(screen, logo, W / 2, S(18), S(520), S(100), now)
        for k, (lab, col, w) in enumerate((("1P", P1C, self.wells[0]), ("2P", P2C, self.wells[1]))):
            y = S(150) + k * S(56)
            self.box(screen, W / 2 - S(200), y, S(400), S(48), (230, 180, 70), fill=(10, 8, 30, 220), radius=8, width=3)
            self.text(screen, lab, W / 2 - S(180), y + S(24), 24, col, key="black", valign="middle", glow=0)
            self.text(screen, f"{w.popped * 10:07d}", W / 2 + S(180), y + S(24), 26, WHITE, key="black", align="right", valign="middle", glow=0)
        if not self.p2_in(vals):                                            # over the well of player 2 / sur le puits du joueur 2
            word, col = self.invite(vals, now)
            self.label(screen, word, S(BW_WELLS[self.THEME][1]), S(240), 30, col, align="center")


class PnickiesScene(BlobScene):
    """Pnickies as in the game: the pastel sky between heaven and the underworld, an angel of our own on the left and
    a little imp on the right, the well in its pink frame in the middle; the pairs fall and pop four by four, the
    chains shine. NEXT and the score beside the well. / Le ciel pastel, un ange à nous à gauche et un petit diablotin
    à droite, le puits dans son cadre rose ; les paires tombent et éclatent quatre par quatre, NEXT et le score à côté."""
    THEME = "bw_heaven"

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W = self.S, self.W
        w = self.wells[0]
        w.draw(screen, now)
        self.draw_next(screen, w, W / 2 + S(120), S(80))
        self.hd.draw_logo(screen, logo, S(250), S(14), S(380), S(84), now)
        self.box(screen, W / 2 + S(120), S(210), S(220), S(84), (250, 150, 200), fill=(30, 10, 40, 220), radius=8, width=3)
        self.text(screen, "SCORE", W / 2 + S(140), S(232), 20, (250, 170, 210), key="black", valign="middle", glow=0)
        self.text(screen, f"{w.popped * 10:06d}", W / 2 + S(320), S(268), 28, WHITE, key="black", align="right", valign="middle", glow=0)
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(250), S(50), 30, col, align="center")


# ============================================================================ Frog Feast
def frog_draw(col, leap):
    """A frog of our own seen from the front, sitting or leaping. / Une grenouille à nous de face, assise ou en saut."""
    def fn(d, W, H):
        dark = _mix(col, (0, 0, 0), 0.5) + (255,)
        ow = max(1, int(W * 0.03))
        if leap:
            for sx in (0.12, 0.88):
                d.line([(W * 0.5, H * 0.6), (W * sx, H * 0.95)], fill=col + (255,), width=max(2, int(W * 0.1)))
        else:
            for sx in (0.08, 0.72):
                d.ellipse([W * sx, H * 0.62, W * (sx + 0.2), H * 0.92], fill=col + (255,), outline=dark, width=ow)
        d.ellipse([W * 0.18, H * 0.32, W * 0.82, H * 0.88], fill=col + (255,), outline=dark, width=ow)
        d.ellipse([W * 0.3, H * 0.5, W * 0.7, H * 0.82], fill=_mix(col, (255, 255, 230), 0.55) + (255,))
        for ex in (0.32, 0.68):
            d.ellipse([W * (ex - 0.13), H * 0.12, W * (ex + 0.13), H * 0.42], fill=col + (255,), outline=dark, width=ow)
            d.ellipse([W * (ex - 0.07), H * 0.18, W * (ex + 0.07), H * 0.34], fill=(255, 255, 255, 255))
            d.ellipse([W * (ex - 0.03), H * 0.22, W * (ex + 0.03), H * 0.32], fill=INK)
        d.arc([W * 0.36, H * 0.4, W * 0.64, H * 0.56], 20, 160, fill=dark, width=ow)
    return fn


class FrogFeastScene(GameScene):
    """Frog Feast as in the game: the blue pond between two tall pines, its two lily pads; two frogs of our own leap
    from their bank to their pad and catch the flies with their tongue. Each one's score on its wooden post, TIME in
    the middle, TIME UP when it runs out. / La mare bleue entre deux grands sapins et ses deux nénuphars ; deux
    grenouilles à nous sautent de leur rive à leur nénuphar et attrapent les mouches avec leur langue. Le score de
    chacune sur son poteau de bois, TIME au milieu, TIME UP à la fin."""
    THEME = "ff_pond"
    STATIC = True
    SHADE = (60, 0)
    ROUND = 120.0

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.frogs = [{"spot": 0, "x": 0.0, "y": 0.0, "jump": None, "tongue": None, "score": 0, "next": 1.0},
                      {"spot": 0, "x": 0.0, "y": 0.0, "jump": None, "tongue": None, "score": 0, "next": 1.6}]
        for k, f in enumerate(self.frogs):
            f["x"], f["y"] = self.spot_xy(k, 0)
        self.flies = [self.new_fly() for _ in range(6)]
        self.t0 = None
        self.caught = 0                                   # (tests)

    def spot_xy(self, k, spot):
        """On the grass beside its post, or on its lily pad. / Dans l'herbe à côté de son poteau, ou sur son nénuphar."""
        W, H = self.W, self.H
        if spot == 0:
            bx, by = FF_BANKS[k]
            return W * bx + self.S(110 if k == 0 else -110), H * by - self.S(40)
        px, py = FF_PADS[k]
        return W * px, H * py - self.S(20)

    def new_fly(self):
        return [self.rng.uniform(self.W * 0.2, self.W * 0.8), self.rng.uniform(self.S(140), self.S(300)), self.rng.uniform(0, 6),
                self.rng.uniform(0.6, 1.4)]

    def restart(self, vals, now):
        self.t0 = now
        for f in self.frogs:
            f["score"] = 0

    def update(self, vals, now):
        if self.t0 is None:
            self.t0 = now
        if now - self.t0 > self.ROUND:                                     # TIME UP, a new round / nouvelle manche
            self.slam("TIME UP", GOLD, now, 1.6)
            self.restart(vals, now + 1.6)
        for fl in self.flies:
            fl[0] += math.sin(now * 2.3 * fl[3] + fl[2]) * self.S(140) * self.dt
            fl[1] += math.cos(now * 1.7 * fl[3] + fl[2] * 2) * self.S(70) * self.dt
            fl[0] = min(self.W * 0.85, max(self.W * 0.15, fl[0]))
            fl[1] = min(self.S(330), max(self.S(120), fl[1]))
        for k, f in enumerate(self.frogs):
            if f["jump"] is not None:                                      # in the air / en l'air
                (x0, y0), (x1, y1), t0 = f["jump"]
                u = min(1.0, (now - t0) / 0.5)
                f["x"], f["y"] = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u - math.sin(u * math.pi) * self.S(110)
                if u >= 1.0:
                    f["jump"] = None
                    self.fx.glow(f["x"], f["y"] + self.S(30), 4, 30, (180, 220, 255), 0.3, "front", 1.0, 0.0, hot=0.3)
                continue
            if f["tongue"] is not None and now - f["tongue"][2] > 0.18:
                f["tongue"] = None
            if now < f["next"]:
                continue
            near = min(self.flies, key=lambda fl: (fl[0] - f["x"]) ** 2 + (fl[1] - f["y"]) ** 2)
            if (near[0] - f["x"]) ** 2 + (near[1] - f["y"]) ** 2 < self.S(260) ** 2 and self.rng.random() < 0.75:
                f["tongue"] = (near[0], near[1], now)                      # the tongue catches a fly / la langue attrape une mouche
                f["score"] += 1
                self.caught += 1
                self.popup("+1", near[0], near[1] - self.S(20), P1C if k == 0 else P2C, 28)
                near[:] = self.new_fly()
                f["next"] = now + self.rng.uniform(0.6, 1.4)
            else:
                f["spot"] = 1 - f["spot"]                                  # a leap to the other spot / un saut
                f["jump"] = ((f["x"], f["y"]), self.spot_xy(k, f["spot"]), now)
                f["next"] = now + 0.5 + self.rng.uniform(0.4, 1.0)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        for fl in self.flies:                                               # the flies / les mouches
            x, y = int(fl[0]), int(fl[1])
            wing = S(6) if int(now * 30 + fl[2] * 10) % 2 else S(3)
            pg.draw.ellipse(screen, (220, 230, 250), (x - S(9), y - wing - S(2), S(8), wing + S(2)))
            pg.draw.ellipse(screen, (220, 230, 250), (x + S(1), y - wing - S(2), S(8), wing + S(2)))
            pg.draw.circle(screen, (20, 20, 24), (x, y), S(4))
        for k, f in enumerate(self.frogs):
            col = (90, 200, 80) if k == 0 else (210, 110, 60)
            size = S(96)
            img = self.img(("frog", k, f["jump"] is not None), size, size, frog_draw(col, f["jump"] is not None), ss=2, flip=k == 1)
            if f["tongue"] is not None:
                pg.draw.line(screen, (240, 90, 120), (int(f["x"]), int(f["y"] + S(6))), (int(f["tongue"][0]), int(f["tongue"][1])), max(2, S(6)))
            screen.blit(img, (int(f["x"] - size / 2), int(f["y"] - size / 2)))
            bx, by = FF_BANKS[k]
            self.text(screen, str(f["score"]), W * bx, self.H * by - S(16), 34, WHITE, key="black", align="center", valign="middle")
        self.hd.draw_logo(screen, logo, W / 2, S(10), S(440), S(90), now)
        left = max(0, min(int(self.ROUND), int(self.ROUND - (now - (self.t0 or now)))))
        self.label(screen, f"TIME {left // 60}:{left % 60:02d}", W / 2, S(128), 30, WHITE, key="black", align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(260), S(50), 30, col, align="center")


# ============================================================================ Pokonyan! Balloon
def balloon_draw(col):
    def fn(d, W, H):
        d.ellipse([W * 0.08, 0, W * 0.92, H * 0.8], fill=col + (255,), outline=_mix(col, (0, 0, 0), 0.4) + (255,), width=max(1, int(W * 0.05)))
        d.ellipse([W * 0.25, H * 0.12, W * 0.42, H * 0.3], fill=_mix(col, (255, 255, 255), 0.6) + (255,))
        d.polygon([(W * 0.44, H * 0.8), (W * 0.56, H * 0.8), (W * 0.5, H * 0.86)], fill=_mix(col, (0, 0, 0), 0.3) + (255,))
        d.line([(W * 0.5, H * 0.86), (W * 0.46, H * 0.94), (W * 0.54, H)], fill=(80, 80, 90, 255), width=max(1, int(W * 0.03)))
    return fn


def air_balloon_draw():
    """Our hot-air balloon with stripes and a little explorer in the basket. / Notre montgolfière rayée et un petit
    explorateur dans la nacelle."""
    def fn(d, W, H):
        cols = ((240, 80, 70), (250, 220, 90), (90, 170, 240))
        d.ellipse([W * 0.06, 0, W * 0.94, H * 0.66], fill=cols[0] + (255,), outline=INK, width=max(1, int(W * 0.02)))
        for k in (1, 2):
            d.chord([W * (0.06 + k * 0.14), 0, W * (0.94 - k * 0.14), H * 0.66], 0, 360, fill=cols[k % 3] + (255,))
        d.ellipse([W * 0.42, 0, W * 0.58, H * 0.66], fill=cols[0] + (255,))
        for sx in (0.3, 0.7):
            d.line([(W * sx, H * 0.6), (W * (0.38 if sx < 0.5 else 0.62), H * 0.78)], fill=(90, 60, 40, 255), width=max(1, int(W * 0.02)))
        d.rectangle([W * 0.34, H * 0.78, W * 0.66, H * 0.98], fill=(170, 120, 60, 255), outline=(90, 60, 30, 255), width=max(1, int(W * 0.02)))
        d.ellipse([W * 0.42, H * 0.66, W * 0.58, H * 0.8], fill=(240, 200, 160, 255), outline=INK, width=max(1, int(W * 0.015)))
        d.chord([W * 0.38, H * 0.62, W * 0.62, H * 0.74], 180, 360, fill=(210, 190, 130, 255))
    return fn


def animal_draw(kind, frame):
    """A zebra or a giraffe of our own, walking. / Un zèbre ou une girafe à nous, qui marche."""
    def fn(d, W, H):
        step = 0.04 if frame else -0.04
        if kind == "zebra":
            body, mark = (250, 250, 250), (30, 30, 30)
            d.ellipse([W * 0.15, H * 0.35, W * 0.75, H * 0.7], fill=body + (255,), outline=INK, width=2)
            for lx in (0.22, 0.32, 0.58, 0.68):
                d.line([(W * lx, H * 0.6), (W * (lx + step), H * 0.98)], fill=body + (255,), width=max(2, int(W * 0.05)))
            d.line([(W * 0.72, H * 0.45), (W * 0.86, H * 0.2)], fill=body + (255,), width=max(3, int(W * 0.09)))
            d.ellipse([W * 0.8, H * 0.1, W * 0.98, H * 0.3], fill=body + (255,), outline=INK, width=2)
            for k in range(5):
                x = W * (0.25 + k * 0.1)
                d.line([(x, H * 0.38), (x - W * 0.03, H * 0.66)], fill=mark + (255,), width=max(1, int(W * 0.03)))
        else:
            body, mark = (240, 190, 80), (160, 100, 40)
            d.ellipse([W * 0.15, H * 0.5, W * 0.65, H * 0.75], fill=body + (255,), outline=INK, width=2)
            for lx in (0.22, 0.3, 0.5, 0.58):
                d.line([(W * lx, H * 0.7), (W * (lx + step), H * 0.99)], fill=body + (255,), width=max(2, int(W * 0.04)))
            d.line([(W * 0.6, H * 0.55), (W * 0.82, H * 0.08)], fill=body + (255,), width=max(3, int(W * 0.07)))
            d.ellipse([W * 0.76, 0, W * 0.96, H * 0.14], fill=body + (255,), outline=INK, width=2)
            for k in range(6):
                d.ellipse([W * (0.2 + k * 0.07), H * 0.55, W * (0.25 + k * 0.07), H * 0.62], fill=mark + (255,))
    return fn


class PokonyanScene(GameScene):
    """Pokonyan! Balloon as in the game: the savanna seen from the sky scrolls below, the zebras and the giraffes walk,
    our hot-air balloon and its little explorer drift above; the balloons of all colours rise and pop when the basket
    touches them. / La savane vue du ciel défile en dessous, zèbres et girafes marchent, notre montgolfière et son
    petit explorateur passent au-dessus ; les ballons de toutes les couleurs montent et éclatent quand la nacelle les touche."""
    THEME = "pk_savanna"
    SHADE = (60, 30)
    COLORS = ((240, 70, 90), (250, 200, 50), (90, 200, 90), (80, 150, 250), (220, 110, 230))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.balloons = []
        self.animals = []
        self.next_b = 0.0
        self.next_a = 0.0
        self.popped = 0                                   # (tests)

    def move(self, vals, now, idle):
        return 0.12 if idle else 0.3

    def basket(self, now):
        return self.W * 0.3 + math.sin(now * 0.4) * self.S(180), self.S(150) + math.sin(now * 0.9) * self.S(30)

    def update(self, vals, now):
        S = self.S
        if now >= self.next_b:
            self.next_b = now + self.rng.uniform(0.5, 1.2)
            near = self.rng.random() < 0.5                                 # half of them rise on the way of the basket
            x = self.basket(now + 3.0)[0] + self.rng.uniform(-120, 120) * self.s if near else self.rng.uniform(self.W * 0.1, self.W * 0.9)
            self.balloons.append([x, self.H + S(40), self.rng.randrange(len(self.COLORS)), self.rng.uniform(60, 110), self.rng.uniform(0, 6)])
        if now >= self.next_a:
            self.next_a = now + self.rng.uniform(2.0, 4.0)
            self.animals.append([self.W + S(100), self.rng.uniform(S(330), S(420)), self.rng.choice(("zebra", "giraffe"))])
        bx, by = self.basket(now)
        keep = []
        for b in self.balloons:
            b[1] -= b[3] * self.s * self.dt
            b[0] += math.sin(now + b[4]) * S(20) * self.dt
            if (b[0] - bx) ** 2 + (b[1] - (by + S(70))) ** 2 < S(90) ** 2:     # the basket touches it: pop / la nacelle le touche
                self.popped += 1
                self.fx.glow(b[0], b[1], 8, 60, self.COLORS[b[2]], 0.4, "front", 1.0, 0.0, hot=0.7)
                self.popup("+10", b[0], b[1] - S(20), GOLD, 28)
                continue
            if b[1] > -S(80):
                keep.append(b)
        self.balloons = keep
        for a in self.animals:
            a[0] -= S(70) * self.dt
        self.animals = [a for a in self.animals if a[0] > -S(200)]

    def draw_hud(self, screen, eng, vals, logo, now):
        S = self.S
        for a in self.animals:
            frame = int(now * 4 + a[1]) % 2
            img = self.img(("animal", a[2], frame), S(110), S(110), animal_draw(a[2], frame), ss=2)
            screen.blit(img, (int(a[0]), int(a[1] - S(110))))
        for b in self.balloons:
            img = self.img(("pkb", b[2]), S(44), S(64), balloon_draw(self.COLORS[b[2]]), ss=2)
            screen.blit(img, (int(b[0] - S(22)), int(b[1] - S(32))))
        bx, by = self.basket(now)
        img = self.img("airballoon", S(150), S(220), air_balloon_draw(), ss=2)
        screen.blit(img, (int(bx - S(75)), int(by - S(140))))
        self.top_bar(screen, eng, vals, logo, now)
        self.label(screen, tr(f"BALLONS {self.popped}", f"BALLOONS {self.popped}"), S(150), S(130), 28, GOLD, align="center")


# ============================================================================ Magical Pumpkin
def pumpkin_draw(frame):
    """Our pumpkin carriage: a round orange pumpkin, its stem, two windows and two wheels. / Notre carrosse citrouille."""
    def fn(d, W, H):
        orange, dark = (250, 150, 40), (170, 80, 20)
        for k, sx in enumerate((0.18, 0.5, 0.82)):
            d.ellipse([W * (sx - 0.22), H * 0.08, W * (sx + 0.22), H * 0.8], fill=orange + (255,), outline=dark + (255,), width=max(1, int(W * 0.015)))
        d.rectangle([W * 0.47, 0, W * 0.53, H * 0.12], fill=(60, 140, 50, 255))
        d.ellipse([W * 0.53, H * 0.0, W * 0.7, H * 0.1], fill=(80, 180, 60, 255))
        for wx in (0.3, 0.62):
            d.ellipse([W * (wx - 0.08), H * 0.3, W * (wx + 0.08), H * 0.5], fill=(255, 240, 180, 255), outline=dark + (255,), width=max(1, int(W * 0.015)))
        for cx in (0.24, 0.76):
            d.ellipse([W * (cx - 0.12), H * 0.66, W * (cx + 0.12), H * 0.99], fill=(250, 220, 120, 255), outline=(120, 70, 20, 255),
                      width=max(1, int(W * 0.02)))
            for k in range(3):
                a = (k * 60 + frame * 30) * math.pi / 180
                d.line([(W * cx - math.cos(a) * W * 0.1, H * 0.825 - math.sin(a) * H * 0.14),
                        (W * cx + math.cos(a) * W * 0.1, H * 0.825 + math.sin(a) * H * 0.14)], fill=(120, 70, 20, 255), width=max(1, int(W * 0.015)))
    return fn


def star_draw(col):
    def fn(d, W, H):
        pts = []
        for k in range(10):
            r = (0.48 if k % 2 == 0 else 0.2) * W
            a = -math.pi / 2 + k * math.pi / 5
            pts.append((W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r))
        d.polygon(pts, fill=col + (255,), outline=_mix(col, (0, 0, 0), 0.4) + (255,))
    return fn


class MagicalPumpkinScene(GameScene):
    """Magical Pumpkin as in the game: a fairy-tale town of round pastel houses and its pink castle scroll by, our
    pumpkin carriage rolls on the candy road by the river and picks up the stars that float ahead. / Une ville de conte
    de fées aux maisons rondes pastel et son château rose défilent, notre carrosse citrouille roule sur la route en
    bonbon au bord de la rivière et ramasse les étoiles qui flottent devant lui."""
    THEME = "mp_town"
    SHADE = (60, 0)
    STARS = ((250, 220, 60), (250, 150, 200), (140, 220, 250))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.stars = []
        self.next_s = 0.0
        self.picked = 0                                   # (tests)

    def move(self, vals, now, idle):
        return 0.2 if idle else 0.5

    def cart(self, now):
        return self.W * 0.28, self.H - self.S(150) - abs(math.sin(now * 5)) * self.S(10)

    def update(self, vals, now):
        S = self.S
        if now >= self.next_s:
            self.next_s = now + self.rng.uniform(0.4, 0.9)
            self.stars.append([self.W + S(30), self.rng.uniform(S(170), S(330)), self.rng.randrange(3), self.rng.uniform(0, 6)])
        cx, cy = self.cart(now)
        keep = []
        for st in self.stars:
            st[0] -= S(260) * self.dt
            if (st[0] - cx) ** 2 + (st[1] - cy) ** 2 < S(90) ** 2:          # picked up / ramassée
                self.picked += 1
                self.fx.glow(st[0], st[1], 6, 50, self.STARS[st[2]], 0.4, "front", 1.0, 0.0, hot=0.8)
                self.popup("+50", st[0], st[1] - S(20), GOLD, 26)
                continue
            if st[0] > -S(40):
                keep.append(st)
        self.stars = keep

    def draw_hud(self, screen, eng, vals, logo, now):
        S = self.S
        for st in self.stars:
            size = S(40)
            img = self.img(("mpstar", st[2]), size, size, star_draw(self.STARS[st[2]]), ss=2)
            screen.blit(img, (int(st[0] - size / 2), int(st[1] + math.sin(now * 3 + st[3]) * S(10) - size / 2)))
        cx, cy = self.cart(now)
        frame = int(now * 12) % 2
        img = self.img(("pumpkin", frame), S(200), S(150), pumpkin_draw(frame), ss=2)
        screen.blit(img, (int(cx - S(100)), int(cy - S(75))))
        self.top_bar(screen, eng, vals, logo, now)
        self.label(screen, tr(f"ÉTOILES {self.picked}", f"STARS {self.picked}"), S(150), S(130), 28, GOLD, align="center")


# ============================================================================ Ganbare! Marine Kun
def fish_draw(col):
    def fn(d, W, H):
        d.ellipse([W * 0.1, H * 0.2, W * 0.8, H * 0.8], fill=col + (255,), outline=_mix(col, (0, 0, 0), 0.45) + (255,), width=max(1, int(W * 0.04)))
        d.polygon([(W * 0.75, H * 0.5), (W, H * 0.15), (W, H * 0.85)], fill=_mix(col, (0, 0, 0), 0.2) + (255,))
        d.ellipse([W * 0.22, H * 0.36, W * 0.34, H * 0.5], fill=(255, 255, 255, 255))
        d.ellipse([W * 0.25, H * 0.4, W * 0.31, H * 0.48], fill=INK)
    return fn


class MarineKunScene(GameScene):
    """Ganbare! Marine Kun as in the game: the open sea between its rocky stacks, the fish that leap out of the water;
    the red sight follows them, locks on and hits, and the medals add up at the bottom. / La pleine mer entre ses
    pitons rocheux, les poissons qui sautent hors de l'eau ; le viseur rouge les suit, se verrouille et touche, et
    les médailles s'ajoutent en bas."""
    THEME = "gm_sea"
    STATIC = True
    SHADE = (60, 0)
    COLORS = ((250, 140, 60), (250, 220, 70), (120, 200, 250), (240, 110, 160))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.fish = []
        self.next_f = 0.0
        self.aim = [self.W / 2, self.H * 0.5]
        self.target = None
        self.medals = 50
        self.hits = 0                                     # (tests)

    def update(self, vals, now):
        S = self.S
        if now >= self.next_f:
            self.next_f = now + self.rng.uniform(0.8, 1.6)
            x0 = self.rng.uniform(self.W * 0.1, self.W * 0.9)
            self.fish.append({"x0": x0, "x1": x0 + self.rng.uniform(-300, 300) * self.s, "t0": now, "dur": self.rng.uniform(1.4, 2.0),
                              "h": self.rng.uniform(140, 230) * self.s, "col": self.rng.randrange(4), "hit": False})
        self.fish = [f for f in self.fish if now - f["t0"] < f["dur"] and not f["hit"]]
        if self.target not in self.fish:
            live = [f for f in self.fish if now - f["t0"] < f["dur"] * 0.6]
            self.target = min(live, key=lambda f: f["t0"]) if live else None
        if self.target is not None:
            tx, ty = self.fish_xy(self.target, now)
            k = min(1.0, self.dt * 6)
            self.aim[0] += (tx - self.aim[0]) * k
            self.aim[1] += (ty - self.aim[1]) * k
            if (tx - self.aim[0]) ** 2 + (ty - self.aim[1]) ** 2 < S(18) ** 2 and now - self.target["t0"] > self.target["dur"] * 0.35:
                self.target["hit"] = True                                   # hit: a splash and medals / touché : gerbe et médailles
                self.hits += 1
                win = self.rng.choice((1, 2, 3, 5))
                self.medals += win
                self.fx.glow(tx, ty, 10, 80, (255, 255, 255), 0.4, "front", 1.0, 0.0, hot=0.9)
                self.popup(f"+{win}", tx, ty - S(30), GOLD, 34)
                self.target = None

    def fish_xy(self, f, now):
        u = (now - f["t0"]) / f["dur"]
        return f["x0"] + (f["x1"] - f["x0"]) * u, self.H * 0.6 - math.sin(u * math.pi) * f["h"]

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        for f in self.fish:
            x, y = self.fish_xy(f, now)
            img = self.img(("gmfish", f["col"]), S(80), S(48), fish_draw(self.COLORS[f["col"]]), ss=2, flip=f["x1"] > f["x0"])
            screen.blit(img, (int(x - S(40)), int(y - S(24))))
        x, y = int(self.aim[0]), int(self.aim[1])                           # the sight / le viseur
        r = S(46)
        pg.draw.circle(screen, (240, 40, 40), (x, y), r, max(2, S(5)))
        pg.draw.line(screen, (240, 40, 40), (x - r - S(16), y), (x + r + S(16), y), max(2, S(4)))
        pg.draw.line(screen, (240, 40, 40), (x, y - r - S(16)), (x, y + r + S(16)), max(2, S(4)))
        self.hd.draw_logo(screen, logo, W / 2, S(8), S(440), S(90), now)
        self.box(screen, W - S(360), self.H - S(96), S(320), S(70), (250, 210, 80), fill=(20, 30, 70, 225), radius=10, width=3)
        self.text(screen, tr("MÉDAILLES", "MEDALS"), W - S(340), self.H - S(61), 22, (250, 210, 80), key="black", valign="middle", glow=0)
        self.hd.put_number(screen, f"{self.medals:04d}", "black", S(40), WHITE, W - S(60), self.H - S(61), "right", "middle")
        credits = _n(vals.get("credits"))
        if credits is not None:
            self.label(screen, tr(f"CRÉDITS {int(credits)}", f"CREDITS {int(credits)}"), S(170), self.H - S(61), 26, AMBER, align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(260), S(50), 30, col, align="center")


SCENES = {"qtono2j": TonosamaScene, "qndream": NanairoScene, "jyangoku": JyangokushiScene, "choko": ChoukouScene, "gulunpa": GulunpaScene,
          "pnickj": PnickiesScene, "cps1frog": FrogFeastScene, "pokonyan": PokonyanScene, "mpumpkin": MagicalPumpkinScene,
          "ganbare": MarineKunScene}
__all__ = ["SCENES", "THEMES"]
