"""HD scenes of the tenth batch of Neo Geo games done one by one (1.26), each drawn after screenshots of its game.
Each game has its own animated backdrop and reacts to the values read in its memory. The heroes, the knights, the
ships and the creatures are creations of the program in the spirit of the games.

Scènes HD du dixième lot de jeux Neo Geo faits un par un (1.26), chacune dessinée d'après des captures de son jeu.
Les héros, les chevaliers, les vaisseaux et les créatures sont des créations du programme dans l'esprit des jeux.
"""

import math

from .hd_games import CREAM, GOLD, P1C, WHITE, GameScene, _clamp, _n
from .hd_games3 import AeroFightersScene, _capsule
from .hd_games5 import BrawlerScene, SideShooterScene, _mixc
from .hd_themes10 import (B2B_ROWS, DM_CELL, DM_COLS, DM_ROWS, DM_X0, DM_Y0, IM_HALF, IM_PATH, ZT_CELL, ZT_COLS, ZT_FIELDS, ZT_ROWS,
                          ZT_TOP)                         # (and the backdrops of this batch into hd_bg.BUILDERS)
from .i18n import tr

DARKLINE = (24, 20, 26, 255)


def _seg_glow(scene, screen, x0, y0, x1, y1, color, width):
    scene.pg.draw.line(screen, color, (int(x0), int(y0)), (int(x1), int(y1)), max(1, int(width)))


# ============================================================================ Zintrick
ZT_COLORS = ((70, 140, 250), (240, 60, 70), (250, 210, 50), (70, 200, 90), (180, 90, 230))


def drop_gem_draw(k):
    """A jewel shaped like a drop, in its colour, with its shine. / Un joyau en forme de goutte, de sa couleur, et son reflet."""
    def fn(d, W, H):
        col = ZT_COLORS[k % len(ZT_COLORS)]
        pts = [(W * 0.5, H * 0.02)]
        for i in range(19):
            a = -math.pi * 0.15 + i * math.pi * 1.3 / 18
            pts.append((W * 0.5 + math.cos(a) * W * 0.4, H * 0.6 + math.sin(a) * H * 0.36))
        d.polygon(pts, fill=_mixc(col, (0, 0, 0), 0.3), outline=DARKLINE)
        inner = [(W * 0.5 + (x - W * 0.5) * 0.8, H * 0.08 + (y - H * 0.02) * 0.82) for x, y in pts]
        d.polygon(inner, fill=col + (255,))
        d.ellipse([W * 0.3, H * 0.48, W * 0.46, H * 0.7], fill=(255, 255, 255, 220))
    return fn


class GemField:
    """A field of 8 by 9 whose jewels hang from the top; a jewel thrown up a column sticks under the others, three of a
    colour in a line leave, a new row comes down now and then. / Un champ de 8 sur 9 aux joyaux suspendus en haut ; un
    joyau lancé dans une colonne colle sous les autres, trois de la même couleur alignés partent."""

    def __init__(self, scene, cx):
        self.sc, self.rng = scene, scene.rng
        S = scene.S
        self.C = S(ZT_CELL)
        self.x0, self.y0 = cx - ZT_COLS * self.C / 2, S(ZT_TOP)
        self.grid = [[None] * ZT_ROWS for _ in range(ZT_COLS)]          # [col][row], row 0 at the top
        for c in range(ZT_COLS):
            for r in range(self.rng.randint(2, 4)):
                self.grid[c][r] = self.rng.randrange(5)
        self.shot = None
        self.col = 3.5                                                  # where the thrower stands / où se tient le lanceur
        self.target = 3
        self.next_row = 0.0

    def depth(self, c):
        return sum(1 for v in self.grid[c] if v is not None)

    def xy(self, c, r):
        return self.x0 + (c + 0.5) * self.C, self.y0 + (r + 0.5) * self.C

    def throw(self, now, color=None):
        if self.shot is not None:
            return
        c = self.target
        self.shot = {"c": c, "y": self.y0 + ZT_ROWS * self.C, "k": self.rng.randrange(5) if color is None else color}
        self.sc.throws += 1

    def step(self, dt, now):
        S = self.sc.S
        if self.next_row == 0.0:
            self.next_row = now + 7.0
        if abs(self.col - self.target) > 0.05:                          # the thrower walks to his column
            self.col += _clamp(self.target - self.col, -dt * 6, dt * 6)
        elif self.shot is None:
            self.throw(now)
        s = self.shot
        if s is not None:
            s["y"] -= S(900) * dt
            stop = self.y0 + self.depth(s["c"]) * self.C
            if s["y"] <= stop:
                r = self.depth(s["c"])
                if r < ZT_ROWS:
                    self.grid[s["c"]][r] = s["k"]
                self.shot = None
                self.resolve(now)
                self.target = self.rng.randrange(ZT_COLS)
        if now >= self.next_row:                                         # a new row pushes everything down
            self.next_row = now + 7.0
            for c in range(ZT_COLS):
                self.grid[c] = [self.rng.randrange(5)] + self.grid[c][:-1]
            if any(self.grid[c][ZT_ROWS - 1] is not None for c in range(ZT_COLS)):
                self.clear()

    def resolve(self, now):
        gone = set()
        for c in range(ZT_COLS):
            for r in range(ZT_ROWS):
                k = self.grid[c][r]
                if k is None:
                    continue
                for dc, dr in ((1, 0), (0, 1)):
                    run = [(c, r)]
                    cc, rr = c + dc, r + dr
                    while cc < ZT_COLS and rr < ZT_ROWS and self.grid[cc][rr] == k:
                        run.append((cc, rr))
                        cc, rr = cc + dc, rr + dr
                    if len(run) >= 3:
                        gone.update(run)
        for c, r in gone:
            x, y = self.xy(c, r)
            self.sc.burst(x, y, self.grid[c][r])
            self.grid[c][r] = None
        if gone:
            self.sc.popped += len(gone)
            for c in range(ZT_COLS):                                     # what is left goes back up / le reste remonte
                col = [v for v in self.grid[c] if v is not None]
                self.grid[c] = col + [None] * (ZT_ROWS - len(col))

    def clear(self):
        for c in range(ZT_COLS):
            for r in range(ZT_ROWS):
                if self.grid[c][r] is not None:
                    x, y = self.xy(c, r)
                    self.sc.fx.later(0.01 * (c + r * ZT_COLS), self.sc.burst, x, y, self.grid[c][r])
        self.grid = [[None] * ZT_ROWS for _ in range(ZT_COLS)]
        for c in range(ZT_COLS):
            self.grid[c][0] = self.rng.randrange(5)


def thrower_draw(cap, frame):
    """A little thrower of our own seen from behind, arms up: a cap, a tunic. / Un petit lanceur à nous, vu de dos."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.04))
        up = frame == 1
        for x in (0.32, 0.56):
            d.rounded_rectangle([W * x, H * 0.68, W * (x + 0.14), H * 0.98], radius=W * 0.05, fill=(70, 50, 40, 255), outline=DARKLINE, width=ow)
        d.rounded_rectangle([W * 0.24, H * 0.36, W * 0.76, H * 0.74], radius=W * 0.14, fill=(60, 140, 90, 255), outline=DARKLINE, width=ow)
        for sx in (-1, 1):
            a = (W * (0.5 + sx * 0.24), H * 0.44)
            b = (W * (0.5 + sx * 0.3), H * (0.08 if up else 0.62))
            _capsule(d, a, b, W * 0.12, W * 0.1, (250, 210, 170, 255), DARKLINE, ow)
        d.ellipse([W * 0.32, H * 0.1, W * 0.68, H * 0.44], fill=(120, 80, 50, 255), outline=DARKLINE, width=ow)
        d.chord([W * 0.3, H * 0.06, W * 0.7, H * 0.36], 180, 360, fill=cap + (255,), outline=DARKLINE)
    return fn


class ZintrickScene(GameScene):
    """Zintrick as in the game: green mountains under a pale sky, the two fields in their purple frames, the jewels shaped
    like drops hang from the top, a little thrower of our own below each field throws a jewel up a column, three of a
    colour in a line leave. The time in big numbers between the fields, ENERGY, ITEM and LEVEL of each player.
    / Les montagnes vertes, les deux champs dans leurs cadres violets, les joyaux en gouttes suspendus en haut, un petit
    lanceur à nous sous chaque champ, trois de la même couleur alignés partent, le temps en gros au milieu, comme dans le jeu."""
    THEME = "zt_hills"
    STATIC = True
    SHADE = (60, 0)
    PILLS = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.fields = {"p1": GemField(self, S(ZT_FIELDS[0])), "p2": GemField(self, S(ZT_FIELDS[1]))}
        self.popped = 0                                   # (tests)
        self.throws = 0
        self.warm += [(self.gem, (k, 32)) for k in range(5)]

    def gem(self, k, size):
        S = self.S
        return self.img(("ztgem", k, size), S(size), S(size), drop_gem_draw(k), ss=2)

    def burst(self, x, y, k):
        self.fx.sparks(x, y, 10, ZT_COLORS[k % 5], (200, 480), (0, 360), (0.2, 0.4), 300, "front", 4, 12)

    def update(self, vals, now):
        for side, suf in (("p1", ""), ("p2", "_p2")):
            f = self.fields[side]
            f.step(self.dt, now)                                         # the other field is the computer's / l'ordinateur
            ch = self.changed(vals, "item" + suf)
            if ch and ch[1] < ch[0]:                                     # an item used: a burst in the field
                for c in range(ZT_COLS):
                    if f.grid[c][0] is not None:
                        x, y = f.xy(c, 0)
                        self.burst(x, y, f.grid[c][0])
                        f.grid[c] = f.grid[c][1:] + [None]
                x, _ = f.xy(3.5, 0)
                self.popup("ITEM!", x, self.S(240), GOLD, 40)
            ch = self.changed(vals, "level" + suf)
            if ch and ch[1] > ch[0]:
                x, _ = f.xy(3.5, 0)
                self.popup(f"LEVEL {int(ch[1])}", x, self.S(240), WHITE, 40)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, H = self.S, self.W, self.H
        for side, f in self.fields.items():
            for c in range(ZT_COLS):
                for r in range(ZT_ROWS):
                    k = f.grid[c][r]
                    if k is not None:
                        img = self.gem(k, 32)
                        x, y = f.xy(c, r)
                        screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
            if f.shot is not None:
                img = self.gem(f.shot["k"], 32)
                x, _ = f.xy(f.shot["c"], 0)
                screen.blit(img, (int(x - img.get_width() / 2), int(f.shot["y"] - img.get_height() / 2)))
            x = f.x0 + (f.col + 0.5) * f.C                               # the thrower below the field
            fr = 1 if f.shot is not None else 0
            img = self.img(("ztthrow", side, fr), S(56), S(64), thrower_draw((220, 60, 60) if side == "p1" else (60, 90, 220), fr), ss=2)
            screen.blit(img, (int(x - img.get_width() / 2), int(H - img.get_height())))
            suf = "" if side == "p1" else "_p2"
            bx = f.x0
            y = S(28)
            lv = _n(vals.get("level" + suf))
            if lv is not None:
                self.label(screen, f"LEVEL {int(lv) + 1}", f.x0 + ZT_COLS * f.C / 2, S(80), 22, WHITE, align="center")
            for k, (lab, name, col) in enumerate((("ENERGY", "energy", (90, 220, 120)), ("ITEM", "item", (250, 160, 60)))):
                v = _n(vals.get(name + suf))
                if v is None or (side == "p2" and not self.p2_in(vals)):
                    continue
                yy = y + k * S(26)
                self.pill(screen, bx - S(6), yy - S(12), S(276), S(24), 150, radius=8)
                self.text(screen, lab, bx, yy, 16, CREAM, key="black", valign="middle", glow=0)
                self.bar(screen, bx + S(84), yy - S(8), S(180), S(16), v / 18.0, col)
        self.top_bar(screen, eng, vals, logo, now)
        t = _n(vals.get("time"))
        if t is not None:                                                # the time, big, between the fields
            low = t <= 10
            self.pill(screen, W / 2 - S(80), S(150), S(160), S(110), 160, radius=16)
            self.hd.put_number(screen, f"{int(t):02d}", "black", S(84), (255, 80, 60) if low and int(now * 4) % 2 else (255, 220, 60), W / 2, S(205),
                               "center", "middle")


# ============================================================================ Digger Man
DIRT, WALL, ROCK, GEM, EMPTY = 1, 2, 3, 4, 0
DM_GEMS = ((230, 50, 50), (70, 200, 80), (60, 110, 240), (250, 210, 50))


def miner_kid_draw(frame):
    """Our little digger of our own: a blue cap, a blue suit, a pick. / Notre petit mineur à nous : casquette bleue, pioche."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.05))
        d.ellipse([W * 0.22, H * 0.42, W * 0.78, H * 0.92], fill=(50, 90, 210, 255), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.26, H * 0.12, W * 0.74, H * 0.56], fill=(250, 210, 170, 255), outline=DARKLINE, width=ow)
        d.chord([W * 0.22, H * 0.06, W * 0.78, H * 0.46], 180, 360, fill=(40, 70, 190, 255), outline=DARKLINE)
        for ex in (0.42, 0.6):
            d.ellipse([W * (ex - 0.04), H * 0.3, W * (ex + 0.04), H * 0.38], fill=DARKLINE)
        a = math.radians(-40 if frame == 0 else 20)
        hx, hy = W * 0.74, H * 0.56
        tx, ty = hx + math.cos(a) * W * 0.3, hy + math.sin(a) * W * 0.3
        d.line([(hx, hy), (tx, ty)], fill=(140, 100, 60, 255), width=max(2, int(W * 0.07)))
        d.polygon([(tx - W * 0.12, ty - W * 0.04), (tx + W * 0.12, ty + W * 0.04), (tx, ty + W * 0.06)], fill=(180, 180, 190, 255), outline=DARKLINE)
        for x in (0.3, 0.56):
            d.ellipse([W * x, H * 0.86, W * (x + 0.16), H * 0.98], fill=(60, 40, 30, 255))
    return fn


class DiggerManScene(GameScene):
    """Digger Man as in the game: the mine in its grey brick frame, the orange earth, the grey stone walls, the rocks
    that fall into the tunnels, the coloured jewels; our little digger of our own digs his way to each jewel. The
    score at the top, the jewels left in big blue numbers, ENERGY, the lives and the bombs at the bottom.
    / La mine dans son cadre de briques, la terre orange, les murs de pierre, les rochers qui tombent, les joyaux ;
    notre petit mineur à nous creuse jusqu'à chaque joyau, comme dans le jeu."""
    THEME = "dm_mine"
    STATIC = True
    SHADE = (40, 0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.dug = 0                                      # (tests)
        self.picked = 0
        self.falls = 0
        self.blasts = 0
        self.surf = None
        self.new_map(0.0)

    def new_map(self, now):
        rng = self.rng
        g = [[DIRT] * DM_ROWS for _ in range(DM_COLS)]                  # [col][row], row 0 at the top
        for _ in range(9):                                               # stone walls / murs de pierre
            r = rng.randrange(1, DM_ROWS)
            c0 = rng.randrange(0, DM_COLS - 6)
            for c in range(c0, c0 + rng.randint(3, 7)):
                g[c][r] = WALL
        for c in range(DM_COLS):
            for r in range(DM_ROWS):
                if g[c][r] == DIRT:
                    v = rng.random()
                    if v < 0.09:
                        g[c][r] = ROCK
                    elif v < 0.19:
                        g[c][r] = GEM + 10 * rng.randrange(4)
                    elif v < 0.24:
                        g[c][r] = EMPTY
        for c in range(0, 4):
            g[c][0] = EMPTY
        self.grid = g
        self.me = {"c": 1, "r": 0, "pc": 1, "pr": 0, "t": now, "face": 1}
        self.next_step = now + 0.3
        self.next_fall = now + 0.25
        self.dirty = True

    def kind(self, v):
        return GEM if v is not None and v >= GEM and v != EMPTY and v % 10 == GEM else v

    def gems_left(self):
        return sum(1 for col in self.grid for v in col if self.kind(v) == GEM)

    def path_to_gem(self):
        """Shortest way to a jewel through earth and tunnels. / Le plus court chemin vers un joyau."""
        start = (self.me["c"], self.me["r"])
        prev = {start: None}
        todo = [start]
        while todo:
            nxt = []
            for c, r in todo:
                for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    cc, rr = c + dc, r + dr
                    if not (0 <= cc < DM_COLS and 0 <= rr < DM_ROWS) or (cc, rr) in prev:
                        continue
                    k = self.kind(self.grid[cc][rr])
                    if k in (WALL, ROCK):
                        continue
                    prev[(cc, rr)] = (c, r)
                    if k == GEM:
                        node = (cc, rr)
                        while prev[node] != start:
                            node = prev[node]
                        return node
                    nxt.append((cc, rr))
            todo = nxt
        return None

    def update(self, vals, now):
        S = self.S
        if now >= self.next_step:
            self.next_step = now + 0.2
            step = self.path_to_gem()
            if step is None:                                             # nothing left to reach: a new mine
                self.slam(tr("MINE SUIVANTE", "NEXT MINE"), GOLD, now, 1.4)
                self.new_map(now)
            else:
                c, r = step
                me = self.me
                me["face"] = 1 if c >= me["c"] else -1
                me["pc"], me["pr"], me["c"], me["r"], me["t"] = me["c"], me["r"], c, r, now
                k = self.kind(self.grid[c][r])
                if k == DIRT:
                    self.dug += 1
                elif k == GEM:
                    self.picked += 1
                    x, y = self.cell_xy(c, r)
                    col = DM_GEMS[(self.grid[c][r] // 10) % 4]
                    self.fx.sparks(x, y, 12, col, (200, 460), (0, 360), (0.2, 0.4), 300, "front", 4, 12)
                    self.popup("100", x, y - S(40), GOLD, 28)
                self.grid[c][r] = EMPTY
                self.dirty = True
        if now >= self.next_fall:                                        # the rocks fall into the tunnels
            self.next_fall = now + 0.25
            for c in range(DM_COLS):
                for r in range(DM_ROWS - 2, -1, -1):
                    if self.grid[c][r] == ROCK and self.grid[c][r + 1] == EMPTY and (c, r + 1) != (self.me["c"], self.me["r"]):
                        self.grid[c][r], self.grid[c][r + 1] = EMPTY, ROCK
                        self.falls += 1
                        self.dirty = True
        ch = self.changed(vals, "bombs")
        if ch and ch[1] < ch[0]:                                         # a bomb: the stones around blow up
            self.blasts += 1
            c0, r0 = self.me["c"], self.me["r"]
            for c in range(c0 - 2, c0 + 3):
                for r in range(r0 - 1, r0 + 2):
                    if 0 <= c < DM_COLS and 0 <= r < DM_ROWS and self.kind(self.grid[c][r]) in (WALL, ROCK, DIRT):
                        self.grid[c][r] = EMPTY
            x, y = self.cell_xy(c0, r0)
            self.fx.explosion(x, y, 1.0, False)
            self.dirty = True
        ch = self.changed(vals, "energy")
        if ch and ch[1] < ch[0] - 20:
            x, y = self.cell_xy(self.me["c"], self.me["r"])
            self.popup(tr("AÏE !", "OUCH!"), x, y - S(50), (255, 90, 70), 30)

    def cell_xy(self, c, r):
        S = self.S
        C = S(DM_CELL)
        return S(DM_X0) + (c + 0.5) * C, S(DM_Y0) + (r + 0.5) * C

    def redraw(self):
        S, pg = self.S, self.pg
        C = S(DM_CELL)
        w, h = DM_COLS * C, DM_ROWS * C
        if self.surf is None:
            self.surf = pg.Surface((w, h)).convert()
        surf = self.surf
        surf.fill((30, 22, 20))
        for c in range(DM_COLS):
            for r in range(DM_ROWS):
                v = self.grid[c][r]
                k = self.kind(v)
                x, y = c * C, r * C
                if k == EMPTY:
                    continue
                if k == WALL:
                    pg.draw.rect(surf, (120, 120, 128), (x, y, C, C))
                    pg.draw.line(surf, (80, 80, 86), (x, y + C // 2), (x + C, y + C // 2), max(1, S(2)))
                    pg.draw.line(surf, (80, 80, 86), (x + C // 2, y), (x + C // 2, y + C // 2), max(1, S(2)))
                    pg.draw.rect(surf, (70, 70, 76), (x, y, C, C), max(1, S(2)))
                    continue
                pg.draw.rect(surf, (200, 110, 40), (x, y, C, C))                     # la terre orange
                for i in range(3):
                    pg.draw.circle(surf, (170, 90, 30), (x + (7 + 13 * i) * C // 40, y + (9 + 11 * ((c + r + i) % 3)) * C // 40), max(1, S(3)))
                if k == ROCK:
                    pg.draw.circle(surf, (150, 150, 160), (x + C // 2, y + C // 2), C // 2 - S(2))
                    pg.draw.circle(surf, (200, 200, 210), (x + C // 2 - S(5), y + C // 2 - S(5)), C // 6)
                    pg.draw.circle(surf, (70, 70, 80), (x + C // 2, y + C // 2), C // 2 - S(2), max(1, S(2)))
                elif k == GEM:
                    col = DM_GEMS[(v // 10) % 4]
                    pg.draw.circle(surf, col, (x + C // 2, y + C // 2), C // 2 - S(5))
                    pg.draw.circle(surf, (255, 255, 255), (x + C // 2 - S(5), y + C // 2 - S(5)), max(2, C // 9))
                    pg.draw.circle(surf, (30, 20, 20), (x + C // 2, y + C // 2), C // 2 - S(5), max(1, S(2)))
        self.dirty = False

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, H = self.S, self.W, self.H
        if self.dirty or self.surf is None:
            self.redraw()
        screen.blit(self.surf, (S(DM_X0), S(DM_Y0)))
        me = self.me
        k = _clamp((now - me["t"]) / 0.2)
        x0, y0 = self.cell_xy(me["pc"], me["pr"])
        x1, y1 = self.cell_xy(me["c"], me["r"])
        fr = int(now * 6) % 2
        img = self.img(("dmkid", fr, me["face"]), S(40), S(40), miner_kid_draw(fr), ss=2, flip=me["face"] < 0)
        screen.blit(img, (int(x0 + (x1 - x0) * k - img.get_width() / 2), int(y0 + (y1 - y0) * k - img.get_height() / 2)))
        self.top_bar(screen, eng, vals, logo, now)
        self.pill(screen, S(420), S(20), S(110), S(70), 150, radius=12)                  # the jewels left, in blue
        self.hd.put_number(screen, f"{self.gems_left():02d}", "black", S(56), (80, 140, 255), S(475), S(55), "center", "middle")
        e = _n(vals.get("energy"))
        if e is not None:
            self.pill(screen, S(14), H - S(30), S(360), S(28), 150, radius=8)
            self.text(screen, "ENERGY", S(24), H - S(16), 16, (255, 80, 80), key="black", valign="middle", glow=0)
            self.bar(screen, S(104), H - S(26), S(260), S(18), e / 160.0, (60, 110, 240))
        info = []
        lives, bombs = _n(vals.get("lives")), _n(vals.get("bombs"))
        if lives is not None:
            info.append(f"x{int(lives)}")
        if bombs is not None:
            info.append(f"B {int(bombs)}")
        if info:
            self.label(screen, "   ".join(info), W - S(140), H - S(18), 22, WHITE, align="center")


# ============================================================================ The Irritating Maze
class IrritatingMazeScene(GameScene):
    """The Irritating Maze as in the game: the red checkered floor, the corridor of the maze between its blue rails, the
    big arrow, the bumper and the crate; our pointer goes along the corridor without touching the rails, a life lost
    in the game is an electric shock. TIME in red LED numbers with its tenths, the map of the maze with the pointer.
    / Le sol en damier rouge, le couloir entre ses rails bleus ; notre pointeur suit le couloir sans toucher les rails,
    une vie perdue dans le jeu est une décharge électrique ; TIME en chiffres rouges, la carte du labyrinthe."""
    THEME = "im_maze"
    STATIC = True
    SHADE = (40, 0)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.u = 0.0
        self.speed = 120.0
        self.shock = -9.0
        self.shocks = 0                                   # (tests)
        self.goals = 0
        self.lens = []
        pts = IM_PATH
        for k in range(len(pts) - 1):
            self.lens.append(math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]))
        self.total = sum(self.lens)

    def at(self, u):
        """The point of the path u pixels from the start, and its direction. / Le point du chemin à u du départ."""
        pts = IM_PATH
        for k, ln in enumerate(self.lens):
            if u <= ln or k == len(self.lens) - 1:
                t = _clamp(u / ln if ln else 0)
                (x0, y0), (x1, y1) = pts[k], pts[k + 1]
                return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.atan2(y1 - y0, x1 - x0)
            u -= ln
        return pts[-1][0], pts[-1][1], 0.0

    def update(self, vals, now):
        dt = self.dt
        if now - self.shock > 0.8:
            self.speed += (self.rng.uniform(80, 200) - self.speed) * dt * 0.5
            self.u += self.speed * dt
        if self.u >= self.total:
            self.goals += 1
            self.slam("GOAL!", GOLD, now, 1.4)
            self.u = 0.0
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:                                         # the pointer touched a rail / un rail touché
            self.shock = now
            self.shocks += 1
            S = self.S
            x, y, a = self.at(self.u)
            ox, oy = -math.sin(a) * IM_HALF, math.cos(a) * IM_HALF
            for k in range(6):
                self.fx.tracer(S(x), S(y), S(x + ox * self.rng.uniform(-1, 1)), S(y + oy * self.rng.uniform(-1, 1)), 2600, (150, 220, 255), 4, 60,
                               "front", False)
            self.fx.sparks(S(x), S(y), 30, (180, 230, 255), (300, 800), (0, 360), (0.2, 0.5), 200, "front", 3, 14)
            self.fx.shake(6, 0.35)
            self.popup("BZZT!", S(x), S(y) - S(60), (150, 220, 255), 44)
            self.u = max(0.0, self.u - 60)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        x, y, a = self.at(self.u)
        wob = math.sin(now * 7) * 8
        x += -math.sin(a) * wob
        y += math.cos(a) * wob
        cx, cy = S(x), S(y)
        ang = now * 1.5
        dx, dy = math.cos(ang) * S(40), math.sin(ang) * S(40)            # the pointer: a turning bar and its ring
        hot = now - self.shock < 0.5 and int(now * 20) % 2 == 0
        col = (150, 230, 255) if hot else (250, 230, 120)
        pg.draw.line(screen, (40, 40, 50), (int(cx - dx), int(cy - dy)), (int(cx + dx), int(cy + dy)), max(2, S(16)))
        pg.draw.line(screen, col, (int(cx - dx), int(cy - dy)), (int(cx + dx), int(cy + dy)), max(2, S(10)))
        pg.draw.circle(screen, (40, 40, 50), (int(cx), int(cy)), S(18))
        pg.draw.circle(screen, (240, 80, 80), (int(cx), int(cy)), S(13))
        g = self.fx.sp.glow(S(26), col, 4, hot=0.4)
        screen.blit(g, (int(cx - g.get_width() / 2), int(cy - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        mx, my, mw, mh = S(20), S(330), S(230), S(110)                    # the pointer on the map / sur la carte
        px = mx + S(15) + x / 1920 * (mw - S(30))
        py = my + S(12) + (y - 120) / 300 * (mh - S(24))
        pg.draw.circle(screen, (255, 80, 80), (int(px), int(py)), S(6))
        self.hd.draw_logo(screen, logo, W / 2, S(6), S(420), S(80), now)
        t, tt = _n(vals.get("time_sec")), _n(vals.get("time_tenths"))
        if t is not None:                                                 # TIME in red LED numbers
            bx = W - S(300)
            pg.draw.rect(screen, (20, 20, 24), (bx, S(10), S(280), S(110)), border_radius=S(10))
            pg.draw.rect(screen, (160, 160, 170), (bx, S(10), S(280), S(110)), max(1, S(3)), border_radius=S(10))
            self.text(screen, "TIME", bx + S(140), S(28), 18, (220, 220, 220), key="black", align="center", valign="middle", glow=0)
            self.hd.put_number(screen, f"{int(t):02d}.{int(tt or 0) % 10}s", "stencil", S(60), (255, 60, 50), bx + S(140), S(78), "center", "middle")
        lives = _n(vals.get("lives"))
        if lives is not None:
            for k in range(int(min(lives, 6))):
                pg.draw.circle(screen, (250, 230, 120), (S(40) + k * S(34), S(40)), S(12))
                pg.draw.circle(screen, (60, 50, 20), (S(40) + k * S(34), S(40)), S(12), max(1, S(2)))
        if not self.p2_in(vals):
            word, colw = self.invite(vals, now)
            self.label(screen, word, W / 2, S(110), 26, colw, align="center")


# ============================================================================ Andro Dunos, Ironclad, Last Hope
def small_fighter_draw(body, accent, canopy=(90, 200, 250)):
    """A small fighter of our own seen from the side, nose to the right. / Un petit chasseur à nous, de profil."""
    def fn(d, W, H):
        ow = max(1, int(H * 0.04))
        d.polygon([(W * 0.06, H * 0.5), (W * 0.24, H * 0.3), (W * 0.7, H * 0.36), (W * 0.98, H * 0.52), (W * 0.7, H * 0.66), (W * 0.24, H * 0.7)],
                  fill=body + (255,), outline=DARKLINE)
        d.polygon([(W * 0.3, H * 0.62), (W * 0.52, H * 0.66), (W * 0.36, H * 0.98), (W * 0.22, H * 0.96)], fill=accent + (255,), outline=DARKLINE)
        d.polygon([(W * 0.24, H * 0.36), (W * 0.42, H * 0.36), (W * 0.3, H * 0.04), (W * 0.18, H * 0.06)], fill=accent + (255,), outline=DARKLINE)
        d.ellipse([W * 0.56, H * 0.36, W * 0.8, H * 0.52], fill=canopy + (255,), outline=DARKLINE, width=ow)
        d.line([(W * 0.3, H * 0.5), (W * 0.9, H * 0.52)], fill=_mixc(body, (255, 255, 255), 0.5), width=ow)
        d.ellipse([W * 0.0, H * 0.42, W * 0.12, H * 0.6], fill=(255, 200, 80, 255))
    return fn


def pod_foe_draw(body, eye):
    """A round enemy pod of our own with its fins and its eye. / Une capsule ennemie ronde à nous, ses ailerons, son œil."""
    def fn(d, W, H):
        ow = max(1, int(H * 0.04))
        d.polygon([(W * 0.5, H * 0.1), (W * 0.9, H * 0.02), (W * 0.7, H * 0.4)], fill=_mixc(body, (0, 0, 0), 0.3), outline=DARKLINE)
        d.polygon([(W * 0.5, H * 0.9), (W * 0.9, H * 0.98), (W * 0.7, H * 0.6)], fill=_mixc(body, (0, 0, 0), 0.3), outline=DARKLINE)
        d.ellipse([W * 0.08, H * 0.18, W * 0.86, H * 0.82], fill=body + (255,), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.14, H * 0.34, W * 0.42, H * 0.66], fill=eye + (255,), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.2, H * 0.4, W * 0.3, H * 0.5], fill=(255, 255, 255, 230))
    return fn


def steam_fighter_draw(body, brass):
    """A steam fighter of our own with its robot fist in front, nose to the right. / Un chasseur à vapeur à nous, son
    poing de robot devant."""
    def fn(d, W, H):
        ow = max(1, int(H * 0.04))
        d.rounded_rectangle([W * 0.08, H * 0.34, W * 0.66, H * 0.7], radius=H * 0.16, fill=body + (255,), outline=DARKLINE, width=ow)
        d.polygon([(W * 0.2, H * 0.36), (W * 0.42, H * 0.36), (W * 0.3, H * 0.06), (W * 0.18, H * 0.08)], fill=brass + (255,), outline=DARKLINE)
        d.polygon([(W * 0.2, H * 0.68), (W * 0.46, H * 0.68), (W * 0.32, H * 0.96), (W * 0.18, H * 0.94)], fill=brass + (255,), outline=DARKLINE)
        for x in (0.24, 0.36, 0.48):
            d.ellipse([W * x, H * 0.46, W * (x + 0.05), H * 0.56], fill=brass + (255,))
        d.ellipse([W * 0.44, H * 0.38, W * 0.6, H * 0.52], fill=(100, 200, 240, 255), outline=DARKLINE)
        d.rectangle([W * 0.64, H * 0.46, W * 0.74, H * 0.58], fill=(90, 90, 100, 255), outline=DARKLINE)
        d.ellipse([W * 0.7, H * 0.28, W * 0.99, H * 0.76], fill=(170, 170, 180, 255), outline=DARKLINE, width=ow)   # le poing de robot
        for k in range(3):
            d.line([(W * 0.78 + k * W * 0.06, H * 0.34), (W * 0.78 + k * W * 0.06, H * 0.7)], fill=(110, 110, 120, 255), width=ow)
        d.ellipse([W * 0.0, H * 0.44, W * 0.1, H * 0.6], fill=(255, 190, 80, 255))
    return fn


def gunboat_draw(d, W, H):
    """A small flying steam gunboat. / Une petite canonnière à vapeur volante."""
    ow = max(1, int(H * 0.04))
    d.ellipse([W * 0.1, H * 0.06, W * 0.95, H * 0.5], fill=(150, 130, 110, 255), outline=DARKLINE, width=ow)
    d.rectangle([W * 0.3, H * 0.5, W * 0.7, H * 0.78], fill=(90, 70, 60, 255), outline=DARKLINE)
    d.rectangle([W * 0.05, H * 0.6, W * 0.32, H * 0.68], fill=(60, 60, 70, 255))
    d.ellipse([W * 0.75, H * 0.2, W * 0.92, H * 0.36], fill=(240, 80, 60, 255))
    for x in (0.4, 0.55):
        d.ellipse([W * x, H * 0.82, W * (x + 0.08), H * 0.98], fill=(40, 40, 46, 255))


def barrel_drone_draw(d, W, H):
    """A red barrel drone. / Un drone en tonneau rouge."""
    ow = max(1, int(H * 0.05))
    d.rounded_rectangle([W * 0.14, H * 0.14, W * 0.86, H * 0.86], radius=H * 0.2, fill=(190, 60, 40, 255), outline=DARKLINE, width=ow)
    for x in (0.3, 0.5, 0.7):
        d.line([(W * x, H * 0.16), (W * x, H * 0.84)], fill=(120, 30, 20, 255), width=ow)
    d.ellipse([W * 0.38, H * 0.38, W * 0.62, H * 0.62], fill=(255, 200, 80, 255), outline=DARKLINE)


ADW = (("SHOT", "shot", (70, 140, 255), 7), ("BOMB", "bomb_pw", (255, 150, 40), 5), ("MISSILE", "missile", (250, 220, 50), 8),
       ("UNIT", "unit", (70, 210, 90), 8))


class AndroDunosScene(SideShooterScene):
    """Andro Dunos as in the game: space over a planet, the blue glow of the horizon and the rocky ground, our small
    fighter of our own against round enemy pods. 1P and the score, the four weapons and their levels read in the game
    in their colours, the ships left. / L'espace au-dessus d'une planète, notre petit chasseur à nous contre les
    capsules ennemies, les quatre armes et leurs niveaux lus dans le jeu dans leurs couleurs, comme dans le jeu."""
    THEME = "ad_planet"
    ACC = {"p1": (250, 170, 40), "p2": (60, 160, 240)}
    SHIP = (150, 80)
    FOE = (110, 90)

    def ship_fn(self, side):
        return small_fighter_draw((240, 200, 90) if side == "p1" else (200, 210, 230), self.ACC[side])

    def foe_fn(self, frame):
        return pod_foe_draw((230, 236, 245), (60, 120, 230) if frame == 0 else (90, 160, 250))

    FLIP_FOE = False

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.1

    def update(self, vals, now):
        super().update(vals, now)
        for lab, name, col, mx in ADW:
            ch = self.changed(vals, name)
            if ch and ch[1] > ch[0] and self.ships["p1"]["in"]:
                x, y = self.pos("p1", now)
                self.popup(f"{lab} UP", x, max(self.S(180), y - self.S(70)), col, 32)

    def status(self, screen, eng, vals, logo, now):
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(440), S(84), now)
        self.pill(screen, S(16), S(8), S(470), S(98), 150, radius=14)
        self.text(screen, "1P", S(34), S(32), 30, WHITE, key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(460), S(12), "right", S(42))
        for k, (lab, name, col, mx) in enumerate(ADW):                     # the four weapons in their colours
            v = _n(vals.get(name))
            x = S(34) + k * S(112)
            self.text(screen, lab, x, S(80), 15, col, key="black", valign="middle", glow=0)
            if v is not None:
                self.text(screen, f"{int(v)}", x + S(84), S(80), 18, WHITE, key="black", align="right", valign="middle", glow=0)
        lives = _n(vals.get("lives"))
        if lives is not None:
            icon = self.img("adlife", S(46), S(26), small_fighter_draw((240, 200, 90), self.ACC["p1"]), ss=2)
            for k in range(int(min(lives, 6))):
                screen.blit(icon, (S(24) + k * S(52), H - S(40)))
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(44), 30, col, align="right")


class IroncladScene(SideShooterScene):
    """Ironclad as in the game: the sea at dusk, the iron warships on the horizon, our steam fighter of our own and its
    robot fist against the flying gunboats. The life meter, POWER and LEVEL read in the game, the arms of each side.
    / La mer au crépuscule, les cuirassés à l'horizon, notre chasseur à vapeur et son poing de robot contre les
    canonnières volantes ; la jauge de vie, POWER et LEVEL lus dans le jeu, comme dans le jeu."""
    THEME = "ic_sea"
    ACC = {"p1": (200, 160, 70), "p2": (170, 190, 220)}
    SHIP = (190, 96)
    FOE = (130, 100)
    FLIP_FOE = False

    def ship_fn(self, side):
        return steam_fighter_draw((150, 70, 50) if side == "p1" else (60, 80, 120), self.ACC[side])

    def foe_fn(self, frame):
        return gunboat_draw

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.0

    def update(self, vals, now):
        super().update(vals, now)
        ch = self.changed(vals, "energy")
        if ch and ch[1] < ch[0] and self.ships["p1"]["in"]:
            x, y = self.pos("p1", now)
            self.fx.sparks(x, y, 16, (255, 200, 120), (200, 500), (0, 360), (0.2, 0.4), 300, "front", 4, 12)
        ch = self.changed(vals, "level")
        if ch and ch[1] > ch[0] and self.ships["p1"]["in"]:
            x, y = self.pos("p1", now)
            self.popup("LEVEL UP", x, max(self.S(180), y - self.S(70)), GOLD, 32)

    def status(self, screen, eng, vals, logo, now):
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(440), S(84), now)
        self.pill(screen, S(16), S(8), S(470), S(60), 150, radius=14)
        self.text(screen, "1P", S(34), S(38), 30, (255, 200, 120), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(460), S(14), "right", S(42))
        e = _n(vals.get("energy"))
        if e is not None:                                                  # the life meter
            self.pill(screen, S(16), H - S(56), S(520), S(48), 160, radius=12)
            self.text(screen, "LIFE", S(32), H - S(32), 20, (255, 120, 90), key="black", valign="middle", glow=0)
            self.bar(screen, S(96), H - S(44), S(180), S(22), e / 3.0, (255, 90, 70))
            pw, lv = _n(vals.get("power")), _n(vals.get("level"))
            if pw is not None:
                self.text(screen, f"POWER {int(pw)}", S(296), H - S(32), 20, (250, 220, 120), key="black", valign="middle", glow=0)
            if lv is not None:
                self.text(screen, f"LV {int(lv)}", S(440), H - S(32), 20, (150, 220, 255), key="black", valign="middle", glow=0)
        arms = [(lab, _n(vals.get(name))) for lab, name in (("L", "l_arm"), ("R", "r_arm"))]
        arms = [(lab, v) for lab, v in arms if v is not None]
        if arms:
            self.label(screen, "  ".join(f"{lab}-ARM {int(v) // 2}" for lab, v in arms), W - S(170), H - S(32), 22, WHITE, align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(44), 30, col, align="right")


class LastHopeScene(SideShooterScene):
    """Last Hope as in the game: deep space full of stars, the nebulas and a big blue planet, our small fighter of our
    own and its blue pod against the red barrel drones. The score at the top. No value of the game is known yet
    except the score to learn. / L'espace profond, les nébuleuses et une grosse planète bleue, notre petit chasseur et
    son module bleu contre les drones en tonneau rouges, comme dans le jeu."""
    THEME = "lh_space"
    ACC = {"p1": (80, 150, 255), "p2": (250, 120, 60)}
    SHIP = (150, 80)
    FOE = (90, 90)

    def ship_fn(self, side):
        return small_fighter_draw((200, 206, 220), self.ACC[side], (120, 230, 255))

    def foe_fn(self, frame):
        return barrel_drone_draw

    def move(self, vals, now, idle):
        return 0.3 if idle else 1.2

    def draw_hud(self, screen, eng, vals, logo, now):
        super().draw_hud(screen, eng, vals, logo, now)
        S, pg = self.S, self.pg
        if self.ships["p1"]["in"]:                                         # the blue pod in front of the ship
            x, y = self.pos("p1", now)
            px, py = x + S(90), y + math.sin(now * 3) * S(6)
            g = self.fx.sp.glow(S(30), (90, 160, 255), 6, hot=0.5)
            screen.blit(g, (int(px - g.get_width() / 2), int(py - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
            pg.draw.circle(screen, (200, 230, 255), (int(px), int(py)), S(10))

    def status(self, screen, eng, vals, logo, now):
        S, W, hd = self.S, self.W, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(440), S(84), now)
        self.pill(screen, S(16), S(8), S(440), S(60), 150, radius=14)
        self.text(screen, "1P", S(34), S(38), 30, (120, 180, 255), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(430), S(14), "right", S(42))
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(44), 30, col, align="right")


# ============================================================================ Captain Tomaday
def red_pod_draw(side):
    """Our little flying craft of our own seen from above: a round red hull with a green leafy crest and two thrusters.
    / Notre petit engin volant à nous vu du dessus : une coque ronde rouge, une crête de feuilles vertes, deux réacteurs."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.03))
        body = (230, 50, 40) if side == "p1" else (250, 150, 40)
        for y in (0.18, 0.7):
            d.rounded_rectangle([W * 0.08, H * y, W * 0.4, H * (y + 0.12)], radius=H * 0.05, fill=(160, 160, 170, 255), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.2, H * 0.14, W * 0.86, H * 0.86], fill=body + (255,), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.32, H * 0.24, W * 0.56, H * 0.42], fill=(255, 200, 190, 255))
        for k in range(5):                                                 # la crête de feuilles
            a = math.radians(-60 + k * 30)
            cx, cy = W * 0.36 + math.cos(a) * W * 0.06, H * 0.5 + math.sin(a) * H * 0.2
            d.ellipse([cx - W * 0.1, cy - H * 0.05, cx + W * 0.06, cy + H * 0.05], fill=(60, 170, 70, 255), outline=DARKLINE)
        d.ellipse([W * 0.62, H * 0.42, W * 0.78, H * 0.58], fill=(200, 240, 255, 255), outline=DARKLINE)
    return fn


def tin_robot_draw(d, W, H):
    """A little tin robot flying with its propeller. / Un petit robot en fer-blanc qui vole avec son hélice."""
    ow = max(1, int(W * 0.04))
    d.rounded_rectangle([W * 0.2, H * 0.3, W * 0.8, H * 0.86], radius=W * 0.1, fill=(170, 180, 200, 255), outline=DARKLINE, width=ow)
    d.ellipse([W * 0.3, H * 0.42, W * 0.46, H * 0.58], fill=(250, 220, 60, 255), outline=DARKLINE)
    d.ellipse([W * 0.54, H * 0.42, W * 0.7, H * 0.58], fill=(250, 220, 60, 255), outline=DARKLINE)
    d.rectangle([W * 0.36, H * 0.68, W * 0.64, H * 0.74], fill=(60, 60, 70, 255))
    d.line([(W * 0.5, H * 0.3), (W * 0.5, H * 0.14)], fill=DARKLINE, width=ow)
    d.ellipse([W * 0.14, H * 0.06, W * 0.86, H * 0.18], fill=(200, 60, 60, 255), outline=DARKLINE)


class CaptainTomadayScene(AeroFightersScene):
    """Captain Tomaday seen from the sky, as in the game: the forest, its little red-roofed houses, the railway and its
    steam train, a river; our little red craft of our own with its green leafy crest against flying tin robots. PLAYER
    1 and the score at the top, the lives and the power of both arms read in the game. / Vu du ciel : la forêt, les
    petites maisons, la voie ferrée et son train à vapeur ; notre petit engin rouge à nous contre les robots volants."""
    THEME = "ct_forest"
    SHADE = (60, 60)
    PROP = False
    ACC = {"p1": (230, 50, 40), "p2": (250, 150, 40)}
    SHOT = {"p1": (255, 230, 120), "p2": (170, 230, 255)}
    ODD = "heli"

    def plane_fn(self, side, kind):
        return red_pod_draw(side)

    def enemy_surf(self, kind="jet", shadow=False):
        S = self.S
        key = ("enemy", kind, shadow)
        s = self.imgs.get(key)
        if s is None:
            s = self.img(("enemyimg", "tinbot"), S(80), S(80), tin_robot_draw)
            if shadow:
                s = self.shadow_of(self.pg, s, 70)
            self.imgs[key] = s
        return s

    def update(self, vals, now):
        super().update(vals, now)
        self.ground = []                                                   # no tanks in the forest / pas de chars

    def power_max(self, vals, side):
        return 5

    def status(self, screen, eng, vals, logo, now):
        S, W, H, hd = self.S, self.W, self.H, self.hd
        hd.draw_logo(screen, logo, W / 2, S(8), S(460), S(90), now)
        self.pill(screen, S(16), S(8), S(420), S(84), 150)
        self.text(screen, "PLAYER 1", S(34), S(30), 24, (255, 90, 80), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(410), S(40), "right", S(44))
        rows = []
        lives = _n(vals.get("lives"))
        if lives is not None:
            rows.append(f"x{int(lives)}")
        for lab, name in (("R", "power"), ("L", "power_l")):
            v = _n(vals.get(name))
            if v is not None:
                rows.append(f"{lab} {'●' * int(min(v, 5))}{'○' * int(max(0, 5 - v))}")
        if rows:
            self.label(screen, "   ".join(rows), S(240), H - S(26), 22, WHITE, align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(44), 32, col, align="right")


# ============================================================================ Bang Bang Busters
def buster_draw(frame):
    """Our little buster of our own: a round helmet with a red star, a yellow suit, a bubble gun. / Notre petit
    chasseur à nous : un casque rond à étoile rouge, une combinaison jaune, un pistolet à bulles."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.04))
        step = (frame % 2) * W * 0.06
        for x in (0.3 - step / W, 0.54 + step / W):
            d.rounded_rectangle([W * x, H * 0.7, W * (x + 0.16), H * 0.98], radius=W * 0.05, fill=(60, 60, 140, 255), outline=DARKLINE, width=ow)
        d.rounded_rectangle([W * 0.24, H * 0.42, W * 0.76, H * 0.76], radius=W * 0.14, fill=(250, 210, 50, 255), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.24, H * 0.06, W * 0.76, H * 0.5], fill=(250, 220, 190, 255), outline=DARKLINE, width=ow)
        d.chord([W * 0.2, H * 0.02, W * 0.8, H * 0.42], 180, 360, fill=(240, 240, 250, 255), outline=DARKLINE)
        cx, cy = W * 0.5, H * 0.12
        pts = [(cx + math.cos(-math.pi / 2 + i * math.pi / 5) * W * (0.08 if i % 2 == 0 else 0.035),
                cy + math.sin(-math.pi / 2 + i * math.pi / 5) * W * (0.08 if i % 2 == 0 else 0.035)) for i in range(10)]
        d.polygon(pts, fill=(230, 40, 40, 255))
        for ex in (0.42, 0.6):
            d.ellipse([W * (ex - 0.04), H * 0.28, W * (ex + 0.04), H * 0.36], fill=DARKLINE)
        d.rounded_rectangle([W * 0.66, H * 0.48, W * 0.98, H * 0.6], radius=W * 0.04, fill=(70, 160, 230, 255), outline=DARKLINE, width=ow)
    return fn


def penguin_draw(frame):
    """A round penguin of our own with a red scarf. / Un pingouin rond à nous et son écharpe rouge."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.04))
        d.ellipse([W * 0.14, H * 0.12, W * 0.86, H * 0.96], fill=(40, 60, 120, 255), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.28, H * 0.34, W * 0.72, H * 0.92], fill=(250, 250, 255, 255))
        for ex in (0.4, 0.6):
            d.ellipse([W * (ex - 0.05), H * 0.28, W * (ex + 0.05), H * 0.38], fill=(255, 255, 255, 255), outline=DARKLINE)
            d.ellipse([W * (ex - 0.02), H * 0.31, W * (ex + 0.02), H * 0.36], fill=DARKLINE)
        d.polygon([(W * 0.44, H * 0.4), (W * 0.56, H * 0.4), (W * 0.5, H * 0.48)], fill=(250, 170, 40, 255), outline=DARKLINE)
        d.rectangle([W * 0.26, H * 0.5, W * 0.74, H * 0.56], fill=(220, 40, 40, 255))
        lift = 0.02 if frame else 0.0
        for x in (0.3, 0.56):
            d.ellipse([W * x, H * (0.9 - lift), W * (x + 0.16), H * (0.98 - lift)], fill=(250, 170, 40, 255), outline=DARKLINE)
    return fn


def seal_draw(frame):
    """A grey seal of our own. / Un phoque gris à nous."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.04))
        d.ellipse([W * 0.06, H * 0.4, W * 0.9, H * 0.96], fill=(150, 150, 160, 255), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.5, H * 0.16, W * 0.94, H * 0.62], fill=(170, 170, 180, 255), outline=DARKLINE, width=ow)
        d.ellipse([W * 0.7, H * 0.3, W * 0.78, H * 0.4], fill=DARKLINE)
        d.ellipse([W * 0.82, H * 0.4, W * 0.96, H * 0.5], fill=(60, 50, 50, 255))
        d.polygon([(W * 0.06, H * 0.7), (W * 0.0, H * (0.56 if frame else 0.62)), (W * 0.16, H * 0.68)], fill=(120, 120, 130, 255), outline=DARKLINE)
    return fn


class BangBangBustersScene(GameScene):
    """Bang Bang Busters as in the game: the ice world, the blue sky and its aurora, the platforms of ice blocks; our
    little buster of our own traps the penguins and the seals in his bubbles and kicks them away. The score and the
    hearts at the top, the stage, the boss gauge when the game shows it. / Le monde de glace, les plateformes de blocs
    de glace ; notre petit chasseur à nous enferme les pingouins et les phoques dans ses bulles, comme dans le jeu."""
    THEME = "bbb_ice"
    ROWS = B2B_ROWS
    STATIC = True
    SHADE = (40, 0)
    PILLS = True

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.hero = {"row": 0, "x": self.W * 0.3, "dir": 1, "shoot": -99.0, "jump": None}
        self.foes = []
        self.flying = []
        self.next_foe = 0.0
        self.stage = 1
        self.cleared = 0
        self.traps = 0                                    # (tests)

    def row_y(self, row):
        return self.S(self.ROWS[row][0])

    def seg_of(self, row, x):
        for x0, x1 in self.ROWS[row][1]:
            if self.S(x0) <= x <= self.S(x1):
                return self.S(x0), self.S(x1)
        return None

    def restart(self, vals, now):
        self.foes = []
        self.next_foe = now + 0.5

    def update(self, vals, now):
        S, dt, rng = self.S, self.dt, self.rng
        if now >= self.next_foe and len(self.foes) < 6:
            self.next_foe = now + rng.uniform(0.7, 1.4)
            row = rng.randrange(1, len(self.ROWS))
            x0, x1 = rng.choice(self.ROWS[row][1])
            self.foes.append({"row": row, "x": S(rng.uniform(x0 + 30, x1 - 30)), "dir": rng.choice((-1, 1)), "kind": rng.randrange(2),
                              "ph": rng.uniform(0, 6), "trap": None})
        for f in self.foes:
            if f["trap"] is not None:
                continue
            seg = self.seg_of(f["row"], f["x"])
            f["x"] += f["dir"] * S(80) * dt
            if seg and not (seg[0] + S(24) < f["x"] < seg[1] - S(24)):
                f["dir"] = -f["dir"]
                f["x"] = _clamp(f["x"], seg[0] + S(24), seg[1] - S(24))
        h = self.hero
        if h["jump"] is not None:
            j = h["jump"]
            if (now - j["t0"]) / 0.6 >= 1:
                h["row"], h["x"], h["jump"] = j["row"], j["x"], None
        else:
            same = [f for f in self.foes if f["row"] == h["row"]]
            if same:
                tgt = min(same, key=lambda f: abs(f["x"] - h["x"]))
                h["dir"] = 1 if tgt["x"] > h["x"] else -1
                if tgt["trap"] is not None and abs(tgt["x"] - h["x"]) < S(70):
                    self.kick(tgt, now)
                elif tgt["trap"] is None and abs(tgt["x"] - h["x"]) < S(260) and now - h["shoot"] > 0.5:
                    self.trap(tgt, now)
                elif abs(tgt["x"] - h["x"]) >= S(60):
                    h["x"] += h["dir"] * S(170) * dt
            elif rng.random() < dt * 0.9 and self.foes:
                tgt = rng.choice(self.foes)
                seg = self.seg_of(tgt["row"], tgt["x"]) or (tgt["x"] - S(50), tgt["x"] + S(50))
                h["jump"] = {"t0": now, "row": tgt["row"], "x": _clamp(tgt["x"] - S(160) * rng.choice((-1, 1)), seg[0] + S(30), seg[1] - S(30)),
                             "x0": h["x"], "y0": self.row_y(h["row"])}
            seg = self.seg_of(h["row"], h["x"])
            if seg:
                h["x"] = _clamp(h["x"], seg[0] + S(30), seg[1] - S(30))
        for f in list(self.foes):                                          # a trapped one breaks free after a while
            if f["trap"] is not None and now - f["trap"] > 5.0:
                f["trap"] = None
        ch = self.changed(vals, "score")
        if ch and ch[1] > ch[0]:
            free = [f for f in self.foes if f["trap"] is None]
            if free:
                self.trap(min(free, key=lambda f: abs(f["x"] - h["x"]) + abs(f["row"] - h["row"]) * S(300)), now)
        ch = self.changed(vals, "lives")
        if ch and ch[1] < ch[0]:
            self.popup(tr("-1 VIE", "-1 LIFE"), h["x"], self.row_y(h["row"]) - S(120), (255, 90, 70), 36)
        ch = self.changed(vals, "boss")
        if ch and ch[1] < ch[0]:
            self.fx.sparks(self.W * 0.8, self.S(200), 14, (255, 220, 120), (200, 500), (0, 360), (0.2, 0.4), 300, "front", 4, 12)

    def trap(self, f, now):
        """A bubble shot traps the enemy. / Une bulle enferme l'ennemi."""
        h = self.hero
        h["shoot"] = now
        f["trap"] = now
        self.traps += 1
        y = self.row_y(f["row"]) - self.S(40)
        self.fx.tracer(h["x"], self.row_y(h["row"]) - self.S(44), f["x"], y, 1800, (150, 220, 255), 10, 60, "front", False)

    def kick(self, f, now):
        if f not in self.foes:
            return
        self.foes.remove(f)
        self.cleared += 1
        d = 1 if f["x"] >= self.hero["x"] else -1
        self.flying.append({"x": f["x"], "y": self.row_y(f["row"]) - self.S(40), "vx": d * self.S(800), "vy": -self.S(500), "kind": f["kind"],
                            "t0": now})
        self.fx.sparks(f["x"], self.row_y(f["row"]) - self.S(40), 16, (200, 240, 255), (200, 500), (0, 360), (0.3, 0.6), 300, "front", 5, 10)
        self.popup("1000", f["x"], self.row_y(f["row"]) - self.S(90), GOLD, 30)
        if self.cleared % 8 == 0:
            self.stage += 1
            self.slam(f"S1-{self.stage}", (120, 220, 255), now, 1.2)

    def foe_img(self, kind, frame):
        S = self.S
        return self.img(("bbbfoe", kind, frame), S(70), S(64), (penguin_draw if kind == 0 else seal_draw)(frame), ss=2)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, dt = self.S, self.dt
        for f in self.foes:
            img = self.foe_img(f["kind"], int(now * 4 + f["ph"]) % 2)
            if f["dir"] < 0:
                img = self.pg.transform.flip(img, True, False)
            y = self.row_y(f["row"])
            screen.blit(img, (int(f["x"] - img.get_width() / 2), int(y - img.get_height())))
            if f["trap"] is not None:
                self.draw_trapped(screen, f, y, now)
        keep = []
        for f in self.flying:
            f["vy"] += S(1400) * dt
            f["x"] += f["vx"] * dt
            f["y"] += f["vy"] * dt
            if f["y"] < self.H + S(80):
                keep.append(f)
                img = self.rotated(("bbbspin", f["kind"]), self.foe_img(f["kind"], 0), (now - f["t0"]) * 720, 12)
                screen.blit(img, (int(f["x"] - img.get_width() / 2), int(f["y"] - img.get_height() / 2)))
        self.flying = keep
        h = self.hero
        if self.p1_in(vals):
            if h["jump"] is not None:
                j = h["jump"]
                k = _clamp((now - j["t0"]) / 0.6)
                x = j["x0"] + (j["x"] - j["x0"]) * k
                y = j["y0"] + (self.row_y(j["row"]) - j["y0"]) * k - math.sin(k * math.pi) * S(130)
            else:
                x, y = h["x"], self.row_y(h["row"])
            img = self.hero_img(int(now * 6) % 2, h["dir"])
            screen.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height())))
        self.status(screen, eng, vals, logo, now)

    def hero_img(self, frame, d):
        S = self.S
        return self.img(("buster", frame, d), S(70), S(80), buster_draw(frame), ss=2, flip=d < 0)

    def draw_trapped(self, screen, f, y, now):
        """The bubble around a trapped enemy. / La bulle autour d'un ennemi pris."""
        S, pg = self.S, self.pg
        r = S(44) + math.sin(now * 6) * S(3)
        pg.draw.circle(screen, (180, 230, 255), (int(f["x"]), int(y - S(32))), int(r), max(1, S(4)))
        pg.draw.circle(screen, (255, 255, 255), (int(f["x"] - r * 0.4), int(y - S(32) - r * 0.4)), S(6))

    def status(self, screen, eng, vals, logo, now):
        S, W, pg = self.S, self.W, self.pg
        self.hd.draw_logo(screen, logo, W / 2, S(4), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(470), S(84), 160, radius=14)
        self.text(screen, "1P-", S(28), S(30), 26, (255, 230, 120), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            self.hd._score(screen, eng, "score", S(460), S(10), "right", S(40))
        lives = _n(vals.get("lives"))
        if lives is not None:
            for k in range(int(min(lives, 6))):                             # the hearts
                cx, cy = S(40) + k * S(34), S(68)
                pg.draw.circle(screen, (240, 50, 70), (int(cx - S(7)), int(cy - S(4))), S(9))
                pg.draw.circle(screen, (240, 50, 70), (int(cx + S(7)), int(cy - S(4))), S(9))
                pg.draw.polygon(screen, (240, 50, 70), [(int(cx - S(15)), int(cy)), (int(cx + S(15)), int(cy)), (int(cx), int(cy + S(15)))])
        self.label(screen, f"S1-{self.stage}", S(560), S(40), 30, (120, 220, 255), key="black", align="center")
        boss = _n(vals.get("boss"))
        if boss:
            self.pill(screen, W - S(420), S(96), S(400), S(40), 150, radius=10)
            self.text(screen, "BOSS", W - S(404), S(116), 20, (255, 120, 90), key="black", valign="middle", glow=0)
            self.bar(screen, W - S(330), S(106), S(300), S(20), boss / 255.0, (255, 90, 70))
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


# ============================================================================ Crossed Swords
def knight_draw(armor, plume, frame):
    """An armoured knight of our own facing us, with his shield and his sword: frame 0 guard, 1 raised sword, 2 strike,
    3 hurt. / Un chevalier en armure à nous, face à nous, son bouclier et son épée."""
    def fn(d, W, H):
        ow = max(1, int(W * 0.012))
        dark = DARKLINE
        arm, arm_d = armor + (255,), _mixc(armor, (0, 0, 0), 0.35)
        lean = {0: 0.0, 1: -0.02, 2: 0.04, 3: -0.05}[frame]
        cx = W * (0.5 + lean)
        for x in (-0.1, 0.04):                                              # les jambes
            d.rounded_rectangle([cx + W * x, H * 0.62, cx + W * (x + 0.07), H * 0.97], radius=W * 0.02, fill=arm_d, outline=dark, width=ow)
        d.polygon([(cx - W * 0.16, H * 0.3), (cx + W * 0.16, H * 0.3), (cx + W * 0.12, H * 0.66), (cx - W * 0.12, H * 0.66)], fill=arm, outline=dark)
        d.rectangle([cx - W * 0.13, H * 0.6, cx + W * 0.13, H * 0.66], fill=(110, 80, 40, 255), outline=dark)
        d.ellipse([cx - W * 0.09, H * 0.1, cx + W * 0.09, H * 0.32], fill=arm, outline=dark, width=ow)       # le heaume
        d.rectangle([cx - W * 0.06, H * 0.19, cx + W * 0.06, H * 0.22], fill=(20, 20, 24, 255))
        d.polygon([(cx, H * 0.1), (cx + W * 0.04, H * 0.0), (cx + W * 0.1, H * 0.04), (cx + W * 0.02, H * 0.12)], fill=plume + (255,), outline=dark)
        sx = cx + W * 0.2                                                    # l'épée
        if frame == 1:
            hand, tip = (sx, H * 0.26), (sx + W * 0.06, H * -0.02)
        elif frame == 2:
            hand, tip = (cx + W * 0.08, H * 0.46), (cx - W * 0.3, H * 0.62)
        else:
            hand, tip = (sx, H * 0.48), (sx + W * 0.08, H * 0.16)
        _capsule(d, (cx + W * 0.13, H * 0.34), hand, W * 0.06, W * 0.05, arm, dark, ow)
        d.line([hand, tip], fill=(220, 225, 235, 255), width=max(2, int(W * 0.022)))
        d.line([(hand[0] - W * 0.04, hand[1]), (hand[0] + W * 0.04, hand[1])], fill=(200, 160, 60, 255), width=max(2, int(W * 0.02)))
        d.ellipse([cx - W * 0.36, H * 0.32, cx - W * 0.1, H * 0.68], fill=(150, 40, 40, 255), outline=dark, width=max(1, int(W * 0.02)))   # le bouclier
        d.ellipse([cx - W * 0.28, H * 0.42, cx - W * 0.18, H * 0.58], fill=(220, 190, 80, 255), outline=dark)
    return fn


def ghost_knight_draw(d, W, H):
    """The player's knight seen from behind, only his outline in light, as in the game. / Le chevalier du joueur vu de
    dos, seulement son contour en lumière."""
    line = (250, 230, 120, 255)
    w = max(2, int(W * 0.022))
    d.ellipse([W * 0.38, H * 0.06, W * 0.62, H * 0.3], outline=line, width=w)
    d.polygon([(W * 0.28, H * 0.3), (W * 0.72, H * 0.3), (W * 0.66, H * 0.7), (W * 0.34, H * 0.7)], outline=line)
    d.line([(W * 0.28, H * 0.3), (W * 0.66, H * 0.7)], fill=line, width=1)
    for x in (0.36, 0.54):
        d.rectangle([W * x, H * 0.7, W * (x + 0.1), H * 1.0], outline=line, width=w)
    d.ellipse([W * 0.02, H * 0.3, W * 0.34, H * 0.74], outline=line, width=w)
    d.line([(W * 0.7, H * 0.4), (W * 0.96, H * 0.02)], fill=line, width=w)


class CrossedSwordsScene(GameScene):
    """Crossed Swords as in the game: the forest at night, an armoured knight of our own faces us with his shield and
    his sword, our own knight is seen from behind as an outline of light. They cross swords, ENEMY and its gauge at the
    top; the energy, the gold and the magic read in the game at the bottom: a blow taken, the gold that rises, a
    spell. / La forêt la nuit, un chevalier en armure face à nous, notre chevalier vu de dos en contour de lumière ;
    ENEMY et sa jauge en haut, l'énergie, l'or et la magie lus dans le jeu en bas, comme dans le jeu."""
    THEME = "cs_forest"
    STATIC = True
    SHADE = (40, 80)
    ARMORS = (((70, 110, 80), (220, 60, 60)), ((150, 150, 165), (60, 120, 230)), ((120, 60, 50), (250, 200, 60)), ((60, 60, 80), (230, 230, 240)))

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.enemy = 0
        self.ehp = 1.0
        self.act = (0.0, 0)
        self.next_act = 1.0
        self.down = None
        self.duels = 0                                    # (tests)
        self.spells = 0
        self.hits_taken = 0

    def update(self, vals, now):
        self.values(vals, now)
        if self.down is not None:
            if now - self.down > 1.6:                                        # a new enemy comes / un nouvel ennemi
                self.down = None
                self.enemy = (self.enemy + 1) % len(self.ARMORS)
                self.ehp = 1.0
            return
        S = self.S
        if now >= self.next_act:
            self.next_act = now + self.rng.uniform(0.8, 1.4)
            if self.rng.random() < 0.55:                                    # our knight strikes / notre chevalier frappe
                self.act = (now, 3)
                self.ehp -= self.rng.uniform(0.12, 0.22)
                self.duels += 1
                self.fx.sparks(self.W / 2, S(240), 16, (255, 230, 150), (200, 600), (0, 360), (0.2, 0.4), 300, "front", 4, 14)
                if self.ehp <= 0:
                    self.down = now
                    self.popup("GOLD +500", self.W / 2, S(200), GOLD, 40)
            else:                                                            # the enemy strikes, our shield takes it
                self.act = (now, 2)
                self.fx.glow(self.W * 0.3, S(330), 20, 120, (200, 230, 255), 0.3, "front", 0.9, 0.0)

    def values(self, vals, now):
        """What the game says: a blow taken, a spell, gold. / Ce que dit le jeu : un coup reçu, un sort, de l'or."""
        S = self.S
        ch = self.changed(vals, "energy")
        if ch and ch[1] < ch[0]:
            self.act = (now, 2)
            self.hits_taken += 1
            self.fx.shake(6, 0.3)
            self.popup(tr("TOUCHÉ !", "HIT!"), self.W * 0.3, S(260), (255, 90, 70), 36)
        ch = self.changed(vals, "magic")
        if ch and ch[1] < ch[0]:                                             # a spell: lightning on the enemy
            self.spells += 1
            for k in range(4):
                x = self.W / 2 + self.rng.uniform(-80, 80) * self.s
                self.fx.tracer(x, 0, self.W / 2, S(260), 3000, (180, 220, 255), 8, 220, "front", True)
            self.ehp -= 0.4
            if self.ehp <= 0 and self.down is None:
                self.down = now
        ch = self.changed(vals, "gold")
        if ch and ch[1] > ch[0]:
            self.popup(f"+{int(ch[1] - ch[0])} GOLD", self.W * 0.75, S(300), GOLD, 32)

    def draw_hud(self, screen, eng, vals, logo, now):
        S, W, H, pg = self.S, self.W, self.H, self.pg
        armor, plume = self.ARMORS[self.enemy]
        t0, kind = self.act
        frame = 0
        if now - t0 < 0.35:
            frame = 3 if kind == 3 else (1 if now - t0 < 0.15 else 2)
        if self.down is None or int(now * 10) % 2 == 0:
            img = self.img(("csknight", self.enemy, frame), S(300), S(330), knight_draw(armor, plume, frame), ss=2)
            y = S(100) if self.down is None else S(100) + (now - self.down) * S(120)
            screen.blit(img, (int(W / 2 - img.get_width() / 2), int(y)))
            if frame == 3:
                g = self.fx.sp.glow(S(120), (255, 255, 255), 6, hot=0.5)
                screen.blit(g, (int(W / 2 - g.get_width() / 2), int(S(220) - g.get_height() / 2)), special_flags=pg.BLEND_RGB_ADD)
        me = self.img("csme", S(300), S(340), ghost_knight_draw, ss=2)    # our knight, an outline of light
        lunge = S(60) if kind == 3 and now - t0 < 0.3 else 0
        screen.blit(me, (int(W * 0.28 - me.get_width() / 2 + lunge), int(H - me.get_height() + S(30))))
        self.hd.draw_logo(screen, logo, W / 2, S(4), S(400), S(70), now)
        self.pill(screen, S(16), S(8), S(470), S(56), 160, radius=12)         # ENEMY and its gauge
        self.text(screen, "ENEMY", S(30), S(36), 22, (250, 220, 120), key="black", valign="middle", glow=0)
        self.bar(screen, S(140), S(26), S(320), S(20), max(0.0, self.ehp), (250, 120, 50))
        e, g, m = _n(vals.get("energy")), _n(vals.get("gold")), _n(vals.get("magic"))
        x = S(16)
        if e is not None:
            self.pill(screen, x, H - S(60), S(300), S(50), 170, radius=12)
            for k in range(10):
                on = k < e / 5.0
                pg.draw.circle(screen, (240, 60, 60) if on else (70, 50, 50), (int(x + S(24) + k * S(27)), int(H - S(35))), S(10))
            x += S(316)
        if g is not None:
            self.label(screen, f"GOLD {int(g)}", x + S(100), H - S(35), 26, GOLD, align="center")
            x += S(220)
        if m is not None:
            self.label(screen, f"MAGIC {int(m)}", x + S(100), H - S(35), 26, (150, 200, 255), align="center")
        sc = _n(vals.get("score"))
        if sc is not None:
            self.pill(screen, W - S(420), S(8), S(400), S(56), 160, radius=12)
            self.text(screen, "1P", W - S(400), S(36), 24, P1C, key="black", valign="middle")
            self.hd._score(screen, eng, "score", W - S(40), S(14), "right", S(40))
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(170), H - S(35), 28, col, align="center")


# ============================================================================ Eight Man
class EightManScene(BrawlerScene):
    """Eight Man as in the game: the ruined city at sunset, golden towers and a fallen bridge; a fast cyborg of our own,
    blue and silver, leaves a trail of copies behind him as he fights the purple mutants and the armed cyborgs. 1P and
    the score, LIFE, BOMB and the time in its red box at the top. / La ville en ruine au coucher du soleil ; un cyborg
    rapide à nous, bleu et argent, laisse une traînée de copies en combattant les mutants violets, comme dans le jeu."""
    THEME = "em_city"
    HERO = ("cyborg", (60, 90, 220), (200, 210, 230), (226, 176, 136), (220, 230, 240))
    FOES = (("mutant", (150, 60, 170), (90, 40, 110), (120, 200, 90), (40, 30, 40)), ("cyborg", (200, 90, 50), (90, 90, 100), (226, 176, 136),
                                                                                      (40, 40, 40)))
    ENERGY_MAX = 6

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        self.trail = []

    def draw_hud(self, screen, eng, vals, logo, now):
        h = self.hero
        self.trail = (self.trail + [(h["x"], h["z"], h["face"])])[-12:]
        S = self.S
        fast = _n(vals.get("power8")) or (h.get("act") and now - h["act"][0] < 0.3)
        if fast:                                                             # the copies behind him / ses copies derrière lui
            img = self.fig(self.HERO, 1, h["face"] < 0)
            for k, (x, z, face) in enumerate(self.trail[:-1:3]):
                ghost = img.copy()
                ghost.set_alpha(40 + k * 20)
                y = self.ground(z)
                screen.blit(ghost, (int(x - ghost.get_width() / 2), int(y - ghost.get_height() + S(6))))
        super().draw_hud(screen, eng, vals, logo, now)

    def status(self, screen, eng, vals, logo, now):
        S, W, pg, hd = self.S, self.W, self.pg, self.hd
        hd.draw_logo(screen, logo, W / 2, S(6), S(400), S(76), now)
        self.pill(screen, S(12), S(6), S(600), S(100), 160, radius=14)
        self.text(screen, "1P", S(28), S(28), 26, (255, 230, 120), key="black", valign="middle")
        if _n(vals.get("score")) is not None:
            hd._score(screen, eng, "score", S(330), S(8), "right", S(40))
        e = _n(vals.get("energy"))
        self.text(screen, "LIFE", S(28), S(62), 20, (120, 200, 255), key="black", valign="middle", glow=0)
        if e is not None:
            for k in range(self.ENERGY_MAX):
                col = (80, 180, 255) if k < e else (50, 50, 60)
                pg.draw.rect(screen, col, (S(90) + k * S(34), S(52), S(28), S(20)), border_radius=S(4))
        b = _n(vals.get("bombs"))
        self.text(screen, "BOMB", S(28), S(90), 20, (255, 160, 80), key="black", valign="middle", glow=0)
        if b is not None:
            for k in range(int(min(b, 6))):
                pg.draw.circle(screen, (255, 140, 60), (S(110) + k * S(30), S(90)), S(10))
        t = _n(vals.get("time"))
        if t is not None:                                                    # the time in its red box
            pg.draw.rect(screen, (200, 30, 30), (S(400), S(40), S(120), S(60)), border_radius=S(8))
            hd.put_number(screen, f"{int(t):02d}", "stencil", S(46), WHITE, S(460), S(70), "center", "middle")
        lives = _n(vals.get("lives"))
        if lives is not None:
            self.label(screen, f"PLAYER = {int(lives)}", S(150), self.H - S(26), 22, (255, 120, 90), key="black", align="center")
        if not self.p2_in(vals):
            word, col = self.invite(vals, now)
            self.label(screen, word, W - S(24), S(40), 30, col, align="right")


SCENES = {"zintrckb": ZintrickScene, "diggerma": DiggerManScene, "irrmaze": IrritatingMazeScene, "androdun": AndroDunosScene,
          "ctomaday": CaptainTomadayScene, "ironclad": IroncladScene, "lasthope": LastHopeScene, "b2b": BangBangBustersScene,
          "crsword": CrossedSwordsScene, "eightman": EightManScene}
