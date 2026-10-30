"""The Capcom games with characters on the HD screen, shown like Metal Slug (1.30).

No character of ours any more. The game's place stays behind, calm and darker, two player panels give the essentials
(the score, the health, the lives, the bombs, the weapon, the armour, the level), and the logo, the time and the credits
sit in the middle. The game's events still show. Points scored send the shot, the blow, the slash or the thrown weapon
from the panel to the middle of the screen, a bomb flies from the panel and blows up the middle, a blow taken shakes the
panel and leaves a white trail on the gauge, a life lost flashes red.

Les jeux Capcom à personnages sur l'écran HD, façon Metal Slug. Plus de personnage à nous. Le décor du jeu reste
derrière, calme et assombri, deux panneaux de joueur donnent l'essentiel, le logo, le temps et les crédits sont au
milieu. Les événements du jeu se voient toujours. Les points marqués envoient le tir, le coup, l'entaille ou l'arme lancée
du panneau vers le milieu de l'écran, une bombe part du panneau et fait exploser le milieu, un coup reçu fait trembler le
panneau et laisse une trace blanche sur la jauge, une vie perdue fait un flash rouge."""
import math

from PIL import Image, ImageChops, ImageDraw, ImageOps

from .hd_games import GameScene, GOLD, AMBER, RED, CREAM, WHITE, _n, _mix, _clamp, draw_img
from . import hd_themes12, hd_themes13, hd_themes14   # the backdrops of the games / les décors des jeux
from .hd_mslug import ACCENT, grenade_img
from .i18n import tr

PW, PH = 640, 418                 # a panel, reference screen 1920 x 460 / un panneau, écran de référence 1920 x 460
GREEN = (90, 220, 110)
SKY = (120, 210, 255)
P2_WAIT = 45.0                    # player 2 is in while his values moved less than this ago (no BIOS on CPS) / secondes


# ============================================================================ drawings of our own / nos dessins
def panel_img(side, s, accent):
    """A glass panel with its accent stripes, drawn for P1 then mirrored for P2. / Panneau de verre, retourné pour J2."""
    ss = 2
    W, H = int(PW * s), int(PH * s)
    w, h = W * ss, H * ss
    k = s * ss
    cut = 28 * k
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shape = [(cut, 0), (w - 1, 0), (w - 1, h - 1 - cut), (w - 1 - cut, h - 1), (0, h - 1), (0, cut)]
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(shape, fill=255)
    grad = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(grad)
    for y in range(h):
        t = y / max(1, h - 1)
        gd.line([0, y, w, y], fill=(int(14 - 6 * t), int(18 - 8 * t), int(38 - 18 * t), int(222 + 18 * t)))
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)
    stripes = Image.new("L", (w, h), 0)
    sd = ImageDraw.Draw(stripes)
    for x in range(int(150 * k), int(370 * k), int(28 * k)):
        sd.polygon([(x, 6 * k), (x + 12 * k, 6 * k), (x - 34 * k, 66 * k), (x - 46 * k, 66 * k)], fill=34)
    img.paste(accent + (255,), (0, 0), ImageChops.multiply(stripes, mask))
    d.line([(16 * k, 84 * k), (w - 16 * k, 84 * k)], fill=accent + (110,), width=max(1, int(2 * k)))
    d.line([(16 * k, 330 * k), (w - 16 * k, 330 * k)], fill=(255, 255, 255, 34), width=max(1, int(k)))
    d.line(shape + [shape[0]], fill=accent + (170,), width=max(2, int(3 * k)))
    inner = [(cut + 8 * k, 7 * k), (w - 8 * k, 7 * k), (w - 8 * k, h - 9 * k - cut), (w - 9 * k - cut, h - 8 * k),
             (8 * k, h - 8 * k), (8 * k, cut + 8 * k)]
    d.line(inner + [inner[0]], fill=(255, 255, 255, 22), width=max(1, int(k)))
    img = img.resize((W, H), Image.LANCZOS)
    return img if side == "p1" else ImageOps.mirror(img)


def token_draw(col):
    """A life token of our own, a round badge in the player's colour. / Un jeton de vie à nous."""
    def fn(d, W, H):
        d.ellipse([W * 0.06, H * 0.06, W * 0.94, H * 0.94], fill=_mix(col, (0, 0, 0), 0.25) + (255,), outline=(20, 16, 30, 255),
                  width=max(2, int(W * 0.08)))
        d.ellipse([W * 0.22, H * 0.2, W * 0.78, H * 0.76], fill=col + (255,))
        d.ellipse([W * 0.32, H * 0.26, W * 0.52, H * 0.42], fill=(255, 255, 255, 150))
    return fn


STEEL, WOOD, FLAME, BRASS, INK = (220, 228, 242), (196, 136, 76), (255, 150, 40), (226, 184, 80), (70, 60, 84, 255)


def weapon_draw(kind):
    """Generic weapons and things of our own, drawn flat, pointing right. / Armes et objets génériques, pointe à droite."""
    def fn(d, W, H):
        lw = max(2, int(H * 0.06))
        if kind == "lance":
            d.rectangle([W * 0.06, H * 0.44, W * 0.72, H * 0.56], fill=WOOD + (255,), outline=INK, width=lw)
            d.polygon([(W * 0.7, H * 0.28), (W * 0.98, H * 0.5), (W * 0.7, H * 0.72)], fill=STEEL + (255,), outline=INK)
        elif kind == "dagger":
            d.polygon([(W * 0.36, H * 0.4), (W * 0.96, H * 0.5), (W * 0.36, H * 0.6)], fill=STEEL + (255,), outline=INK)
            d.rectangle([W * 0.3, H * 0.28, W * 0.38, H * 0.72], fill=BRASS + (255,), outline=INK, width=lw)
            d.rectangle([W * 0.08, H * 0.44, W * 0.3, H * 0.56], fill=WOOD + (255,), outline=INK, width=lw)
        elif kind == "torch":
            d.rectangle([W * 0.1, H * 0.44, W * 0.62, H * 0.56], fill=WOOD + (255,), outline=INK, width=lw)
            d.ellipse([W * 0.56, H * 0.22, W * 0.96, H * 0.78], fill=FLAME + (255,), outline=(120, 40, 10, 255), width=lw)
            d.ellipse([W * 0.66, H * 0.36, W * 0.86, H * 0.64], fill=(255, 236, 150, 255))
        elif kind == "sword":
            d.polygon([(W * 0.32, H * 0.44), (W * 0.9, H * 0.44), (W * 0.98, H * 0.5), (W * 0.9, H * 0.56), (W * 0.32, H * 0.56)],
                      fill=STEEL + (255,), outline=INK)
            d.rectangle([W * 0.26, H * 0.24, W * 0.34, H * 0.76], fill=BRASS + (255,), outline=INK, width=lw)
            d.rectangle([W * 0.04, H * 0.44, W * 0.26, H * 0.56], fill=WOOD + (255,), outline=INK, width=lw)
        elif kind == "axe":
            d.rectangle([W * 0.06, H * 0.45, W * 0.84, H * 0.55], fill=WOOD + (255,), outline=INK, width=lw)
            d.polygon([(W * 0.62, H * 0.42), (W * 0.74, H * 0.1), (W * 0.96, H * 0.04), (W * 0.9, H * 0.5), (W * 0.96, H * 0.96),
                       (W * 0.74, H * 0.9), (W * 0.62, H * 0.58)], fill=STEEL + (255,), outline=INK)
        elif kind == "shield":
            d.polygon([(W * 0.3, H * 0.1), (W * 0.7, H * 0.1), (W * 0.7, H * 0.55), (W * 0.5, H * 0.92), (W * 0.3, H * 0.55)],
                      fill=STEEL + (255,), outline=INK)
            d.line([(W * 0.5, H * 0.16), (W * 0.5, H * 0.82)], fill=(180, 40, 40, 255), width=max(2, int(W * 0.06)))
        elif kind == "fireball":
            d.ellipse([W * 0.3, H * 0.15, W * 0.86, H * 0.85], fill=FLAME + (255,), outline=(120, 40, 10, 255), width=lw)
            d.ellipse([W * 0.46, H * 0.32, W * 0.72, H * 0.6], fill=(255, 240, 170, 255))
        elif kind == "star":
            pts = []
            for i in range(10):
                a = -math.pi / 2 + i * math.pi / 5
                r = (0.46 if i % 2 == 0 else 0.2) * min(W, H)
                pts.append((W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r))
            d.polygon(pts, fill=(255, 226, 90, 255), outline=(120, 80, 10, 255))
        elif kind == "orb":
            d.ellipse([W * 0.25, H * 0.12, W * 0.75, H * 0.88], fill=(110, 200, 255, 255), outline=(30, 70, 140, 255), width=lw)
            d.ellipse([W * 0.36, H * 0.24, W * 0.54, H * 0.46], fill=(235, 250, 255, 255))
        elif kind == "key":
            d.ellipse([W * 0.06, H * 0.26, W * 0.4, H * 0.74], outline=BRASS + (255,), width=max(3, int(H * 0.12)))
            d.rectangle([W * 0.36, H * 0.44, W * 0.94, H * 0.56], fill=BRASS + (255,))
            d.rectangle([W * 0.78, H * 0.56, W * 0.86, H * 0.76], fill=BRASS + (255,))
            d.rectangle([W * 0.64, H * 0.56, W * 0.72, H * 0.7], fill=BRASS + (255,))
        elif kind == "pod":
            d.ellipse([W * 0.2, H * 0.2, W * 0.8, H * 0.8], fill=(170, 180, 200, 255), outline=INK, width=lw)
            d.ellipse([W * 0.38, H * 0.38, W * 0.62, H * 0.62], fill=(255, 90, 60, 255))
        elif kind == "coin":
            d.ellipse([W * 0.12, H * 0.12, W * 0.88, H * 0.88], fill=(255, 200, 60, 255), outline=(150, 100, 20, 255), width=lw)
            d.ellipse([W * 0.3, H * 0.3, W * 0.7, H * 0.7], outline=(255, 236, 150, 255), width=max(2, int(W * 0.06)))
    return fn


GG_WEAPONS = {0: ("LANCE", "LANCE", "lance"), 1: ("DAGUE", "DAGGER", "dagger"), 2: ("TORCHE", "TORCH", "torch"),
              3: ("ÉPÉE", "SWORD", "sword"), 4: ("HACHE", "AXE", "axe"), 5: ("BOUCLIER", "SHIELD", "shield"),
              6: ("BOULE DE FEU", "FIREBALL", "fireball")}
TW_WEAPONS = {0: ("SUPER BOMBE", "SUPER BOMB", "fireball"), 1: ("TIR NORMAL", "NORMAL SHOT", "orb"), 2: ("HYPER TIR", "HYPER SHOT", "orb"),
              3: ("TIR ARRIÈRE", "TAIL SHOT", "orb"), 4: ("TIR REBOND", "BOUND SHOT", "orb")}
MS_PARTNERS = {0: ("NINJA", "NINJA"), 2: ("BIGFOOT", "BIGFOOT"), 4: ("PRÊTRE", "PRIEST"), 6: ("MAGICIEN", "MAGICIAN"),
               8: ("AMAZONE", "AMAZON"), 10: ("CHEVALIER", "KNIGHT"), 12: ("VOLEUR", "THIEF"), 14: ("HOMME-LÉZARD", "LIZARDMAN")}
WILLOW = {4: ("ÉPÉISTE", "SWORDSMAN")}


# ============================================================================ the scene / la scène
class PanelScene(GameScene):
    """Two player panels on the game's place, darker. SPEC says what the game reads and how its blows look.
    / Deux panneaux de joueur sur le décor du jeu, assombri. SPEC dit ce que le jeu lit et à quoi ressemblent ses coups."""
    SPEC = {}
    STATIC = True                 # the backdrop does not scroll: calm behind the panels / le décor ne défile pas
    SHADE = (0, 0)
    EXPLOSIONS = True
    VEIL = 70                     # a little darker again behind the panels (0 to 255) / encore un peu plus sombre
    BANNERS = (("GAME OVER", RED),)

    def __init__(self, hd, rng=None):
        super().__init__(hd, rng)
        S = self.S
        self.panels = {side: hd._surf(panel_img(side, self.s, ACCENT[side])) for side in ("p1", "p2")}
        for side in ("p1", "p2"):
            off = self.panels[side].copy()
            off.set_alpha(130)
            self.panels[side + "_off"] = off
        # one veil for the darker backdrops of the HD screen ("dim") and this one, a single blit
        # un seul voile pour le décor assombri de l'écran HD (« dim ») et celui des panneaux, une seule copie
        dim = int(getattr(hd, "dim", 0) * 255 / 100)
        self.veil = self.pg.Surface((self.W, self.H)).convert()
        self.veil.fill((0, 0, 0))
        self.veil.set_alpha(int(round(255 - (255 - self.VEIL) * (255 - dim) / 255)))
        self.bd.own_veil = True
        draw = self.bd.draw

        def bd_draw(target, now, mv):                     # the backdrop, a veil, then the effects behind
            draw(target, now, mv)
            target.blit(self.veil, (0, 0))
        self.bd.draw = bd_draw
        self.tokens = {side: hd._surf(draw_img(S(30), S(30), token_draw(ACCENT[side]))) for side in ("p1", "p2")}
        self.big_tokens = {side: hd._surf(draw_img(S(46), S(46), token_draw(ACCENT[side]))) for side in ("p1", "p2")}
        self.small_grenade = hd._surf(grenade_img(S(22), S(28)))
        self.big_grenade = hd._surf(grenade_img(S(34), S(44)))
        self.fx.sp.register("grenade", grenade_img(S(34), S(42)))
        for kind in ("lance", "dagger", "torch", "sword", "axe", "shield", "fireball", "star", "orb"):
            self.fx.sp.register("pw_" + kind, draw_img(S(92), S(46) if kind not in ("star", "orb", "fireball", "shield") else S(56),
                                                        weapon_draw(kind)))
        self.hits = {"p1": -9.0, "p2": -9.0}             # last blow taken / dernier coup reçu
        self.heals = {"p1": -9.0, "p2": -9.0}
        self.glows = {}                                   # (side, what) -> time, a line of the panel that just changed
        self.p2_seen = -99.0
        self.balloons = []                                # Pang: balloons bouncing in the middle / ballons au milieu
        self.spent = {"p1": 0.0, "p2": 0.0}               # top of the special gauge before it empties / haut de la jauge
        self.slashes = []                                 # blades that cut in the middle / entailles au milieu
        self._armor = None
        self.events = {"hit": 0, "bomb": 0, "down": 0, "heal": 0, "level": 0, "weapon": 0, "join": 0}   # (tests)

    # ------------------------------------------------------------ who plays / qui joue
    def p2_in(self, vals):
        """Player 2 plays: his mode says so, or, with no BIOS on a CPS, his values moved not long ago.
        / Le joueur 2 joue : son mode le dit, ou sans BIOS sur un CPS, ses valeurs ont bougé il y a peu."""
        if vals.get("p2_mode") in (1, 2):
            return True
        return self.fx.now - self.p2_seen < P2_WAIT

    # ------------------------------------------------------------ where things are / où sont les choses
    def x0(self, side):
        return self.S(20) if side == "p1" else self.W - self.S(20) - self.S(PW)

    def X(self, side, lx, w=0):
        """x of an element at lx in the panel of P1, mirrored for P2. / Position miroir pour le joueur 2."""
        x0 = self.x0(side)
        return x0 + self.S(lx) if side == "p1" else x0 + self.S(PW) - self.S(lx) - self.S(w)

    def edge(self, side):
        """The inner edge of a panel, toward the middle. / Le bord intérieur du panneau."""
        return self.x0(side) + self.S(PW) if side == "p1" else self.x0(side)

    def middle(self):
        """A point of the middle of the screen, between the panels. / Un point du milieu, entre les panneaux."""
        room = max(40.0, (self.W - 2 * (self.S(20) + self.S(PW))) / 2 - self.S(30))
        return self.W / 2 + self.rng.uniform(-room, room), self.rng.uniform(140, 340) * self.s

    def mark(self, side, what, now):
        self.glows[(side, what)] = now

    def glow_k(self, side, what, now, dur=0.7):
        t = self.glows.get((side, what))
        return 0.0 if t is None or now - t > dur else 1.0 - (now - t) / dur

    # ------------------------------------------------------------ the game's events / les événements du jeu
    def always(self, vals, now):
        if self.SPEC.get("balloons"):
            self._balloons_move(now)

    def restart(self, vals, now):
        if self.SPEC.get("balloons") and not self.balloons:
            for i in range(2):
                self._balloon_new(3, now, i)

    def update(self, vals, now):
        spec = self.SPEC
        moved2 = [self.changed(vals, n) for n in ("health_p2", "lives_p2", "score_p2", "_p2_chr", "power_p2")]
        if any(moved2) and spec.get("two", True):
            if not self.p2_in(vals):
                self.events["join"] += 1
                self.mark("p2", "join", now)
                self.popup(tr("JOUEUR 2 !", "PLAYER 2!"), self.x0("p2") + self.S(PW) / 2, self.S(250), SKY, 40)
            self.p2_seen = now
        for side in ("p1", "p2"):
            if side == "p2" and not self.p2_in(vals):
                continue
            sfx = "" if side == "p1" else "_p2"
            ch = self.changed(vals, "score" + sfx)
            if ch and ch[1] > ch[0]:
                self._hit(side, ch[1] - ch[0], vals, now)
            gauge = spec.get("gauge")
            if gauge:
                ch = self.changed(vals, gauge["value"] + sfx)
                if ch:
                    if ch[1] < ch[0]:
                        self.hits[side] = now
                        self.fx.glow(self.edge(side), self.S(250), 30, 160, (255, 60, 40), 0.35, "front", 0.7, 0.0)
                        self.fx.shake(2, 0.12)
                    elif ch[1] > ch[0] + 5:
                        self.events["heal"] += 1
                        self.heals[side] = now
                        self.popup(tr("+ VIE", "+ LIFE"), self.X(side, 320), self.S(214), GREEN, 34)
            ch = self.changed(vals, "lives" + sfx)
            if ch:
                if ch[1] < ch[0]:
                    self._down(side, now)
                else:
                    self.mark(side, "lives", now)
                    self.popup(tr("+1 VIE", "1UP"), self.X(side, 520), self.S(66), GOLD, 34)
            g2 = spec.get("gauge2")
            if g2:
                v = _n(vals.get(g2["value"] + sfx))
                if v is not None:
                    self.spent[side] = max(self.spent[side] * 0.999, v)
                ch = self.changed(vals, g2["value"] + sfx)
                if ch and g2.get("spend") and ch[0] - ch[1] >= 30:            # the special gauge empties / la jauge se vide
                    self._bomb(side, now, "special")
            bombs = spec.get("bombs")
            if bombs:
                ch = self.changed(vals, "bombs" + sfx)
                if ch and ch[1] < ch[0]:
                    self._bomb(side, now, bombs.get("icon", "grenade"))
                elif ch:
                    self.mark(side, "bombs", now)
            for item in spec.get("counters", ()):
                name = item["value"] + ("" if item.get("p1_only") else sfx)
                if item.get("p1_only") and side == "p2":
                    continue
                ch = self.changed(vals, name)
                if ch:
                    self.mark(side, item["value"], now)
                    if item.get("throw") and ch[1] < ch[0]:                  # a dagger thrown / une dague lancée
                        self._throw(side, item["throw"], now)
            if spec.get("weapon") and side == "p1":
                ch = self.changed(vals, "weapon")
                if ch:
                    self.events["weapon"] += 1
                    self.mark(side, "weapon", now)
                    self.fx.glow(self.X(side, 120), self.S(256), 20, 120, SKY, 0.4, "front", 0.8, 0.0)
            if spec.get("armor") and side == "p1":
                state = self.armor(vals)
                if self._armor is not None and state != self._armor:
                    self.mark(side, "armor", now)
                    if state == "none":
                        for i in range(6):
                            self.fx.sparks(self.X(side, 360), self.S(290), 3, (210, 216, 230), (300, 700), (200 + i * 25, 230 + i * 25),
                                           (0.4, 0.8), 1400, "front", 6, 14)
                        self.popup(tr("ARMURE PERDUE !", "ARMOUR LOST!"), self.X(side, 360), self.S(240), (255, 200, 60), 34)
                self._armor = state
            for item in spec.get("levels", ()):
                both = not item.get("p1_only", True)                        # Mercs: the power of each player's weapon
                ch = self.changed(vals, item["value"] + (sfx if both else "")) if side == "p1" or both else None
                if ch and ch[1] > ch[0]:
                    self.events["level"] += 1
                    self.mark(side, item["value"], now)
                    self.fx.glow(self.X(side, 200), self.S(368), 20, 140, GOLD, 0.5, "front", 0.9, 0.0)
                    self.popup(tr(*item["up"]), self.X(side, 320), self.S(330), GOLD, 34)
            for item in spec.get("labels", ()):                             # partner, hero: the name changes
                if side == "p1":
                    ch = self.changed(vals, item["value"])
                    if ch:
                        self.mark(side, "name", now)
            if spec.get("names"):
                watch = spec.get("name_watch") or ("_p1_chr", "_p2_chr")
                ch = self.changed(vals, watch[0] if side == "p1" else watch[1])
                if ch:
                    self.mark(side, "name", now)
                    keys = spec["names"] if isinstance(spec["names"], tuple) and spec.get("name_popup") else None
                    n = vals.get(keys[0] if side == "p1" else keys[1]) if keys else None
                    if n:                                                    # a weapon picked up (Mercs) / une arme ramassée
                        self.events["weapon"] += 1
                        self.fx.glow(self.X(side, 200), self.S(60), 20, 140, ACCENT[side], 0.45, "front", 0.9, 0.0)
                        self.popup(tr(f"{n} !", f"{n}!"), self.X(side, 320), self.S(250), _mix(ACCENT[side], WHITE, 0.3), 36)
                lv = spec.get("name_level")
                ch = self.changed(vals, lv[0] + sfx) if lv else None
                if ch:                                                       # a power-up of the weapon / un POW
                    self.mark(side, "name", now)
                    if ch[1] > ch[0]:
                        self.events["level"] += 1
                        self.fx.glow(self.X(side, 200), self.S(60), 20, 140, GOLD, 0.45, "front", 0.9, 0.0)
                        self.popup(tr(*lv[1]), self.X(side, 320), self.S(300), GOLD, 34)   # under a weapon picked up
        if spec.get("floor"):
            fl = spec["floor"] if isinstance(spec["floor"], dict) else {}      # Mercs: its missions / ses missions
            ch = self.changed(vals, fl.get("value", "floor"))
            if ch:
                self.mark("p1", "floor", now)
                if fl.get("done") and ch[1] == ch[0] + 1:                    # a mission complete / une mission accomplie
                    self.events["floor"] = self.events.get("floor", 0) + 1
                    x, y = self.W / 2, self.S(250)
                    self.fx.flash((255, 240, 200), 0.2, 0.3)
                    for i, r in enumerate((180, 300, 440)):
                        self.fx.glow(x, y, 30, r, GOLD, 0.6 + 0.15 * i, "front", 0.9, 0.0, delay=0.1 * i)
                    self.fx.sparks(x, y, 50, (255, 230, 140), (400, 1400), (0, 360), (0.5, 1.1), 300, "front", 3, 30)
                    self.popup(tr(*fl["done"]).format(n=int(ch[0])), x, self.S(250), GOLD, 46, life=2.2)

    def _hit(self, side, gain, vals, now):
        """Points: the blow shows in the middle. A shot, a punch, a slash, a thrown weapon, a spell, a balloon.
        / Des points : le coup se voit au milieu."""
        self.events["hit"] += 1
        kind = self.SPEC.get("hit", "fist")
        x, y = self.middle()
        big = min(2.0, 0.8 + gain / 1200.0)
        ex, ey = self.edge(side), self.S(250)
        d = 1 if side == "p1" else -1
        if kind == "gun":
            self.fx.muzzle(ex - d * self.S(24), ey, d, 1.0)
            for i in range(2):
                tx, ty = x + self.rng.uniform(-30, 30) * self.s, y + self.rng.uniform(-24, 24) * self.s
                self.fx.tracer(ex, ey + self.S(8 * i), tx, ty, speed=4200, width=4, length=170)
            self.fx.later(0.09, self.fx.small_blast, x, y, big, "front")
        elif kind == "slash":
            ang = self.rng.uniform(-35, 35)
            g = self.fx.sp.streak(int(self.S(240) * big), self.S(12), (235, 245, 255), ang, 12)
            self.fx.glow(x, y, 10, 70 * big, (220, 236, 255), 0.18, "front", 0.9, 0.0, hot=0.8)
            self.slashes.append((g, x, y, now))
            self.fx.sparks(x, y, int(10 * big), (230, 240, 255), (300, 800), (0, 360), (0.12, 0.3), 200, "front", 2, 18)
        elif kind == "throw":
            weapon = self.SPEC.get("weapon_names") or GG_WEAPONS
            w = int(_n(vals.get("weapon")) or 0)
            icon = "pw_" + (weapon.get(w, (None, None, "orb"))[2] if isinstance(weapon, dict) else "orb")
            self.fx.projectile(icon, ex, ey, x, y, 0.3, 0.0, lambda xx, yy: self.fx.small_blast(xx, yy, big, "front"), spin=0.0)
        elif kind == "magic":
            self.fx.projectile("pw_orb", ex, ey, x, y, 0.35, 30.0, lambda xx, yy: self._sparkle(xx, yy, big), spin=360.0)
        elif kind == "balloon":
            self._balloon_pop(now)
        else:                                                            # fist / poing
            self.fx.glow(x, y, 20, 110 * big, (255, 244, 210), 0.2, "front", 1.0, 0.0, hot=0.7)
            self.fx.sparks(x, y, int(16 * big), (255, 236, 170), (400, 1000), (0, 360), (0.15, 0.4), 300, "front", 3, 22)
            self.fx.shake(2.5 * big, 0.12)
        self.popup(f"+{int(gain)}", self.X(side, 470), self.S(146), GOLD, 32)

    def _sparkle(self, x, y, big):
        self.fx.glow(x, y, 20, 120 * big, (150, 220, 255), 0.35, "front", 1.0, 0.0, hot=0.6)
        self.fx.sparks(x, y, int(18 * big), (200, 240, 255), (300, 900), (0, 360), (0.3, 0.7), 200, "front", 3, 20)

    def _bomb(self, side, now, icon):
        """A bomb or a special: it leaves the panel and the middle blows up. / Une bombe : elle part du panneau, le milieu explose."""
        self.events["bomb"] += 1
        self.mark(side, "bombs", now)
        x, y = self.W / 2, self.S(250)
        if icon == "grenade":
            self.fx.projectile("grenade", self.X(side, 70), self.S(370), x, y, 0.45, 40.0, lambda xx, yy: self.fx.explosion(xx, yy, 2.2, False))
        elif icon == "star":                                              # a magic attack / une attaque magique
            self.fx.projectile("pw_star", self.X(side, 70), self.S(370), x, y, 0.4, 30.0, lambda xx, yy: self._spell(xx, yy), spin=720.0)
        else:                                                             # the special of the game / le coup spécial
            self.fx.flash((255, 240, 200), 0.35, 0.3)
            self.fx.explosion(x, y, 2.4, False)

    def _spell(self, x, y):
        for i, r in enumerate((260, 420, 600)):
            self.fx.glow(x, y, 30, r, (170, 220, 255), 0.5 + 0.15 * i, "front", 0.9, 0.0, delay=0.08 * i)
        self.fx.sparks(x, y, 40, (255, 240, 170), (400, 1300), (0, 360), (0.4, 1.0), 300, "front", 3, 30)
        self.fx.flash((200, 230, 255), 0.25, 0.3)
        self.fx.shake(8, 0.4)

    def _throw(self, side, kind, now):
        x, y = self.middle()
        self.fx.projectile("pw_" + kind, self.edge(side), self.S(370), x, y, 0.3, 0.0, lambda xx, yy: self.fx.small_blast(xx, yy, 1.0, "front"),
                           spin=0.0)

    def _down(self, side, now):
        """A life lost: the panel goes red and shakes. / Une vie perdue : le panneau rougit et tremble."""
        self.events["down"] += 1
        self.hits[side] = now
        self.mark(side, "lives", now)
        self.fx.flash((255, 40, 30), 0.25, 0.25)
        self.fx.shake(10, 0.35)
        self.popup(tr("-1 VIE", "-1 LIFE"), self.X(side, 470), self.S(66), RED, 36)

    # ------------------------------------------------------------ Pang: balloons in the middle / des ballons au milieu
    def _balloon_new(self, size, now, i=0, x=None, y=None, vx=None):
        cx, room = self.W / 2, max(80.0, (self.W - 2 * (self.S(20) + self.S(PW))) / 2 - self.S(40))
        col = ((255, 70, 60), (70, 140, 255), (90, 210, 90))[(len(self.balloons) + i) % 3]
        self.balloons.append({"x": x if x is not None else cx + self.rng.uniform(-room, room) * 0.6, "y": y if y is not None else self.S(160),
                              "vx": vx if vx is not None else self.rng.choice((-1, 1)) * self.S(120), "vy": 0.0, "r": self.S(18 + 10 * size),
                              "size": size, "col": col})

    def _balloons_move(self, now):
        dt = self.dt
        cx = self.W / 2
        room = max(80.0, (self.W - 2 * (self.S(20) + self.S(PW))) / 2 - self.S(30))
        floor = self.S(400)
        for b in self.balloons:
            b["vy"] += self.S(900) * dt
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
            if b["y"] + b["r"] > floor:
                b["y"] = floor - b["r"]
                b["vy"] = -self.S(520 + 60 * b["size"])
            if abs(b["x"] - cx) + b["r"] > room:
                b["vx"] = -b["vx"]
                b["x"] = cx + math.copysign(room - b["r"], b["x"] - cx)
        if len(self.balloons) < 2:
            self._balloon_new(3, now)

    def _balloon_pop(self, now):
        if not self.balloons:
            self._balloon_new(3, now)
        b = min(self.balloons, key=lambda q: q["y"])
        self.balloons.remove(b)
        self.fx.glow(b["x"], b["y"], b["r"] / self.s, b["r"] / self.s * 2.4, b["col"], 0.3, "front", 0.9, 0.0, hot=0.5)
        self.fx.sparks(b["x"], b["y"], 14, _mix(b["col"], WHITE, 0.4), (300, 700), (0, 360), (0.2, 0.5), 400, "front", 3, 18)
        if b["size"] > 1 and len(self.balloons) < 6:                      # a hit balloon splits in two / il se coupe en deux
            for d in (-1, 1):
                self._balloon_new(b["size"] - 1, now, 0, b["x"], b["y"], d * self.S(150))
                self.balloons[-1]["col"] = b["col"]
                self.balloons[-1]["vy"] = -self.S(380)

    def _draw_balloons(self, screen):
        for b in self.balloons:
            r = int(b["r"])
            img = self.img(("pang_b", r, b["col"]), 2 * r, 2 * r, _balloon_draw(b["col"]), ss=3)
            screen.blit(img, (int(b["x"] - r), int(b["y"] - r)))

    # ------------------------------------------------------------ drawing / dessin
    @staticmethod
    def armor(vals):
        a, b = _n(vals.get("armor")), _n(vals.get("armor_kind"))
        if a is None or b is None:
            return None
        return "none" if int(b) <= 1 or int(a) == 0 else ("gold" if int(b) >= 3 else "silver")

    def name(self, side, vals):
        """The name shown in the panel: the character read in the game, the partner, the hero, or nothing.
        / Le nom montré dans le panneau : le personnage lu dans le jeu, le compagnon, le héros, ou rien."""
        spec = self.SPEC
        if spec.get("names"):
            keys = spec["names"] if isinstance(spec["names"], tuple) else ("p1_char", "p2_char")   # Mercs: its weapons
            n = vals.get(keys[0] if side == "p1" else keys[1])
            if n:
                lvl = _n(vals.get(spec["name_level"][0] + ("" if side == "p1" else "_p2"))) if spec.get("name_level") else None
                return f"{n} +{int(lvl)}" if lvl is not None and lvl >= 1 else str(n)    # FLAMETHROWER +2 (two POW)
        if side == "p1":
            for item in spec.get("labels", ()):
                v = _n(vals.get(item["value"]))
                names = item["names"]
                if v is not None and int(v) in names:
                    return tr(*names[int(v)][:2])
                if item.get("default"):
                    return tr(*item["default"])
        return None

    def draw_hud(self, screen, eng, vals, logo, now):
        if self.balloons:
            self._draw_balloons(screen)
        for g, x, y, t0 in list(self.slashes):                           # slashes of the blades / entailles des lames
            k = (now - t0) / 0.22
            if k >= 1:
                self.slashes.remove((g, x, y, t0))
                continue
            g2 = g.copy()
            g2.set_alpha(int(255 * (1 - k)))
            screen.blit(g2, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)), special_flags=self.pg.BLEND_RGB_ADD)
        for side in ("p1", "p2"):
            self._panel(screen, side, vals, now)
        self._center(screen, vals, logo, now)

    def _panel(self, screen, side, vals, now):
        S = self.S
        on = self.p1_in(vals) if side == "p1" else (self.p2_in(vals) and self.SPEC.get("two", True))
        x0 = self.x0(side)
        jolt = 0
        dt = now - self.hits[side]
        if 0 <= dt < 0.3:
            jolt = int(S(6) * math.sin(dt * 60) * (1 - dt / 0.3))
        screen.blit(self.panels[side] if on else self.panels[side + "_off"], (x0 + jolt, S(21)))
        al = "left" if side == "p1" else "right"
        bx = self.X(side, 36, 84) + jolt
        self.pg.draw.rect(screen, ACCENT[side], (bx, S(36), S(84), S(50)), border_radius=S(12))
        self.text(screen, "P1" if side == "p1" else "P2", bx + S(42), S(61), 40, (20, 14, 10), key="black", align="center", valign="middle",
                  glow=0)
        if not on:
            word, col = self.invite(vals, now)
            self.text(screen, word, x0 + S(PW) / 2, S(240), 56, col, key="stencil", align="center", valign="middle")
            return
        spec = self.SPEC
        sfx = "" if side == "p1" else "_p2"
        name = self.name(side, vals)
        sc = _n(vals.get("score" + sfx))
        # the header: the name next to the badge, the lives on the right / l'en-tête : le nom, les vies à droite
        lives = _n(vals.get("lives" + sfx))
        has_gauge = spec.get("gauge") and any(_n(vals.get(gg["value"] + sfx)) is not None for gg in (spec["gauge"], spec.get("gauge2")) if gg)
        tokens_in_header = lives is not None and (has_gauge or (spec.get("weapon") and side == "p1")
                                                  or (spec.get("bombs_big") and _n(vals.get("bombs" + sfx)) is not None)
                                                  or (spec.get("big") and _n(vals.get(spec["big"]["value"] + sfx)) is not None))
        if name and sc is not None:
            k = self.glow_k(side, "name", now)
            self.text(screen, name, self.X(side, 140, 300) + (0 if side == "p1" else S(300)) + jolt, S(44), 36,
                      _mix(ACCENT[side], WHITE, 0.25 + 0.5 * k), key="xbold", align=al, glow=0.3)
        if tokens_in_header:
            self._lives(screen, side, int(max(0, lives)), self.X(side, PW - 40 - 30, 30) + jolt, S(46), now, small=True)
        # the big line: the score, or the name while the score is not known / la grande ligne : le score, ou le nom
        if sc is not None:
            txt = f"{int(sc):,}".replace(",", " ")
            self.text(screen, txt, (x0 + S(36) if side == "p1" else x0 + S(PW) - S(36)) + jolt, S(96), 92, GOLD, key="stencil", align=al,
                      glow=0.4)
        else:
            big = name or tr("JOUEUR 1" if side == "p1" else "JOUEUR 2", "PLAYER 1" if side == "p1" else "PLAYER 2")
            size = min(80, max(40, int(80 * 9 / max(9, len(big)))))
            self.text(screen, big, (x0 + S(36) if side == "p1" else x0 + S(PW) - S(36)) + jolt, S(140), size,
                      _mix(ACCENT[side], WHITE, 0.2), key="stencil", align=al, valign="middle", glow=0.4)
        # the middle box / la case du milieu
        box = (self.X(side, 16, PW - 32) + jolt, S(196), S(PW - 32), S(124))
        if spec.get("gauge") and self._gauges(screen, side, vals, now, box):
            pass
        elif spec.get("weapon") and side == "p1":                     # the weapon is read for player 1 / lue pour le joueur 1
            self._weapon(screen, side, vals, now, box)
        elif spec.get("bombs_big") and _n(vals.get("bombs" + sfx)) is not None:
            self._row_icons(screen, side, vals, now, box, spec["bombs"]["label"], "bombs" + sfx, spec["bombs"].get("icon", "grenade"))
        elif spec.get("big") and _n(vals.get(spec["big"]["value"] + ("" if side == "p1" else "_p2"))) is not None:
            item = spec["big"]
            self._row_icons(screen, side, vals, now, box, item["label"], item["value"] + ("" if side == "p1" else "_p2"), item["icon"])
        elif lives is not None:
            self._box(screen, box)
            self.text(screen, tr("VIES", "LIVES"), self.X(side, 44, 300) + (0 if side == "p1" else S(300)) + jolt, S(208), 32, CREAM,
                      key="xbold", align=al, glow=0)
            self._lives(screen, side, int(max(0, lives)), self.X(side, 44, 46) + jolt, S(250), now, small=False)
        # the bottom line / la ligne du bas
        self._bottom(screen, side, vals, now, jolt, al)

    def _box(self, screen, box):
        x, y, w, h = box
        key = ("pbox", int(w), int(h))
        s = self.imgs.get(key)
        if s is None:
            s = self.pg.Surface((int(w), int(h)), self.pg.SRCALPHA)
            self.pg.draw.rect(s, (0, 0, 0, 96), s.get_rect(), border_radius=self.S(12))
            self.pg.draw.rect(s, (255, 255, 255, 30), s.get_rect(), max(1, self.S(2)), border_radius=self.S(12))
            self.imgs[key] = s
        screen.blit(s, (int(x), int(y)))

    def _lives(self, screen, side, n, x, y, now, small=True):
        """Life tokens from x: toward the middle of the panel in the header, from its edge in the box.
        / Les jetons de vie à partir de x."""
        tok = self.tokens[side] if small else self.big_tokens[side]
        step = tok.get_width() + self.S(10)
        d = -1 if (small and side == "p1") or (not small and side == "p2") else 1
        shown = min(n, 5)
        for i in range(shown):
            screen.blit(tok, (int(x + d * i * step), int(y)))
        if n > 5 or n == 0:
            tx = x + d * shown * step + (self.S(8) if d > 0 else tok.get_width() - self.S(8))
            self.text(screen, f"×{n}", tx, y + tok.get_height() / 2, 30 if small else 40, CREAM, key="xbold",
                      align="left" if d > 0 else "right", valign="middle", glow=0)

    def _gauges(self, screen, side, vals, now, box):
        spec, S = self.SPEC, self.S
        sfx = "" if side == "p1" else "_p2"
        x, y, w, h = box
        al = "left" if side == "p1" else "right"
        g = spec["gauge"]
        g2 = spec.get("gauge2")
        tx = x + S(28) if side == "p1" else x + w - S(28)
        bars = [(gg, _n(vals.get(gg["value"] + sfx))) for gg in (g, g2) if gg]
        bars = [(gg, v) for gg, v in bars if v is not None]          # only what the game reads / seulement ce qui est lu
        if not bars:
            return False
        hh = S(44) if len(bars) == 1 else S(26)
        self._box(screen, box)
        for i, (gg, v) in enumerate(bars):
            frac = _clamp((v or 0) / float(gg.get("max", 100)))
            ly = y + S(12) if len(bars) == 1 else y + S(6) + i * S(60)
            self.text(screen, tr(*gg["label"]), tx, ly, 30 if len(bars) == 1 else 26, CREAM, key="xbold", align=al, glow=0)
            by = ly + (S(46) if len(bars) == 1 else S(30))
            bx, bw = x + S(28), w - S(56)
            col = gg["col"]
            if gg is g and now - self.heals[side] < 0.6:
                col = _mix(col, GREEN, 0.6 * (1 - (now - self.heals[side]) / 0.6))
            if gg is g and now - self.hits[side] < 0.25:
                col = _mix(col, WHITE, 0.7)
            full = gg.get("full") and frac >= 0.999
            if full:
                col = _mix(GOLD, WHITE, 0.25 + 0.25 * math.sin(now * 8))
            self.pg.draw.rect(screen, gg.get("back", (40, 20, 24)), (bx, by, bw, hh), border_radius=S(9))
            trail = self.hd.trail(side + gg["value"], frac, now) if gg is g else frac
            if trail > frac:
                self._bar_part(screen, bx, by, bw, hh, trail, (255, 250, 240), side)
            self._bar_part(screen, bx, by, bw, hh, frac, col, side)
            self.pg.draw.rect(screen, _mix(gg.get("back", (40, 20, 24)), WHITE, 0.3), (bx, by, bw, hh), max(1, S(3)), border_radius=S(9))
            if full:
                self.text(screen, "MAX", bx + bw / 2, by + hh / 2, 24, (60, 30, 0), key="black", align="center", valign="middle", glow=0)
        return True

    def _bar_part(self, screen, x, y, w, h, frac, col, side):
        fw = int(w * _clamp(frac))
        if fw <= 0:
            return
        rx = x if side == "p1" else x + w - fw
        self.pg.draw.rect(screen, col, (rx, y, fw, h), border_radius=self.S(9))
        hl = max(1, int(h * 0.22))
        if fw > self.S(14):
            self.pg.draw.rect(screen, _mix(col, WHITE, 0.45), (rx + self.S(6), y + max(1, int(h * 0.16)), fw - self.S(12), hl),
                              border_radius=max(1, hl // 2))

    def _weapon(self, screen, side, vals, now, box):
        """The weapon held, its name, and the armour under it. / L'arme tenue, son nom, l'armure dessous."""
        spec, S = self.SPEC, self.S
        x, y, w, h = box
        self._box(screen, box)
        names = spec.get("weapon_names") or GG_WEAPONS
        wv = int(_n(vals.get("weapon")) or 0)
        fr, en, kind = names.get(wv, (str(wv), str(wv), "orb"))
        k = self.glow_k(side, "weapon", now)
        icon = self.img(("pw_icon", kind), S(150), S(76), weapon_draw(kind), ss=3)
        screen.blit(icon, (int(x + S(24)), int(y + S(24))))
        col = _mix(SKY, WHITE, 0.5 * k)
        self.text(screen, tr(fr, en), x + S(196), y + (S(16) if spec.get("armor") else S(36)), 50, col, key="stencil", glow=0.4)
        if spec.get("armor"):
            state = self.armor(vals) or "silver"
            word = {"gold": tr("ARMURE D'OR", "GOLD ARMOUR"), "silver": tr("ARMURE", "ARMOUR"), "none": tr("SANS ARMURE", "NO ARMOUR")}[state]
            acol = {"gold": (255, 214, 100), "silver": (210, 220, 236), "none": (255, 110, 90)}[state]
            ka = self.glow_k(side, "armor", now)
            self.text(screen, word, x + S(196), y + S(78), 32, _mix(acol, WHITE, 0.5 * ka), key="xbold", glow=0.2)
        return True

    def _row_icons(self, screen, side, vals, now, box, label, value, icon):
        S = self.S
        x, y, w, h = box
        self._box(screen, box)
        al = "left" if side == "p1" else "right"
        tx = x + S(28) if side == "p1" else x + w - S(28)
        self.text(screen, tr(*label), tx, y + S(12), 30, CREAM, key="xbold", align=al, glow=0)
        n = int(max(0, _n(vals.get(value)) or 0))
        img = self.img(("pw_small", icon, 40), S(46), S(46), weapon_draw(icon), ss=3) if icon != "grenade" else self.big_grenade
        step = img.get_width() + S(10)
        k = self.glow_k(side, value.replace("_p2", ""), now)
        for i in range(min(n, 9)):
            ix = x + S(28) + i * step if side == "p1" else x + w - S(28) - (i + 1) * step + S(10)
            screen.blit(img, (int(ix), int(y + S(58))))
        if n > 9 or n == 0:
            self.text(screen, f"×{n}", (x + S(28) + min(n, 9) * step) if side == "p1" else (x + w - S(28) - min(n, 9) * step), y + S(80), 40,
                      _mix(CREAM, GOLD, k), key="xbold", align="left" if side == "p1" else "right", valign="middle", glow=0)
        return True

    def _bottom(self, screen, side, vals, now, jolt, al):
        """The line under the box: bombs, daggers, money, keys, level... / La ligne du bas : bombes, dagues, argent, clés, niveau."""
        spec, S = self.SPEC, self.S
        sfx = "" if side == "p1" else "_p2"
        y = S(366)
        items = []
        bombs = spec.get("bombs")
        if bombs and not spec.get("bombs_big"):
            items.append(("icons", bombs["label"], "bombs" + sfx, bombs.get("icon", "grenade")))
        for item in spec.get("counters", ()):
            if item.get("p1_only") and side == "p2":
                continue
            v = item["value"] + ("" if item.get("p1_only") else sfx)
            items.append(("icons" if item.get("icon") else "number", item["label"], v, item.get("icon")))
        for item in spec.get("levels", ()):
            if side == "p1" or not item.get("p1_only", True):
                items.append(("level", item["label"], item["value"] + ("" if item.get("p1_only", True) else sfx), None))
        if not items:
            return
        slot = S(PW - 80) / len(items)
        for i, (kind, label, value, icon) in enumerate(items):
            v = _n(vals.get(value))
            if v is None:
                continue
            k = self.glow_k(side, value.replace("_p2", ""), now)
            lx = 44 + i * (PW - 80) / len(items)
            x = self.X(side, lx, (PW - 80) / len(items)) + jolt
            xa = x if side == "p1" else x + slot
            col = _mix(CREAM, GOLD, k)
            if kind == "icons":
                self.text(screen, tr(*label), xa, y, 28, col, key="xbold", align=al, valign="middle", glow=0)
                img = self.small_grenade if icon == "grenade" else self.img(("pw_small", icon, 28), S(30), S(30), weapon_draw(icon), ss=3)
                n = int(max(0, v))
                tw = self.hd.text_width(tr(*label), "xbold", S(28))
                step = img.get_width() + S(6)
                ix0 = xa + tw + S(14) if side == "p1" else xa - tw - S(14) - img.get_width()
                for j in range(min(n, 8)):
                    ix = ix0 + j * step if side == "p1" else ix0 - j * step
                    screen.blit(img, (int(ix), int(y - img.get_height() / 2)))
                if n > 8 or n == 0:
                    ex = ix0 + min(n, 8) * step if side == "p1" else ix0 - min(n, 8) * step + img.get_width()
                    self.text(screen, f"×{n}", ex, y, 28, col, key="xbold", align=al, valign="middle", glow=0)
            elif kind == "level":
                self.text(screen, f"{tr(*label)} {int(v)}", xa, y, 30, _mix(GOLD, WHITE, 0.4 * k), key="xbold", align=al, valign="middle",
                          glow=0.2)
            else:
                self.text(screen, f"{tr(*label)} {int(v)}", xa, y, 30, col, key="xbold", align=al, valign="middle", glow=0)

    def _center(self, screen, vals, logo, now):
        hd, S, W = self.hd, self.S, self.W
        t = _n(vals.get("time"))
        credits = _n(vals.get("credits"))
        hd.draw_logo(screen, logo, W / 2, S(14), S(540), S(124) if t is not None else S(160), now)
        line = None
        if self.SPEC.get("floor"):
            spec_fl = self.SPEC["floor"] if isinstance(self.SPEC["floor"], dict) else {}
            fl = _n(vals.get(spec_fl.get("value", "floor")))
            if fl is not None:
                word = tr(*spec_fl["label"]) if spec_fl.get("label") else tr("ÉTAGE", "FLOOR")
                line = f"{word} {int(fl)}"
        if line:
            k = self.glow_k("p1", "floor", now, 1.2)
            self.label(screen, line, W / 2, S(158), 34, _mix(SKY, WHITE, 0.5 * k), key="xbold", align="center", alpha=170)
        if t is not None:
            low = t <= 10
            pulse = 0.5 + 0.5 * math.sin(now * 9) if low else 0.0
            ty = S(192) if line else S(184)
            self.box(screen, W / 2 - S(120), ty, S(240), S(132), (RED if low else GOLD), fill=(8, 10, 22, 210), radius=18, width=3)
            self.text(screen, "TIME", W / 2, ty + S(12), 26, CREAM, key="xbold", align="center", glow=0)
            self.text(screen, str(int(t)), W / 2, ty + S(82), 84, RED if low else GOLD, key="stencil", align="center", valign="middle",
                      scale=1 + 0.08 * pulse)
        if credits is not None:
            self.label(screen, tr(f"CRÉDITS {int(credits):02d}", f"CREDITS {int(credits):02d}"), W / 2, S(404), 40, AMBER, key="xbold",
                       align="center", alpha=210)


def _balloon_draw(col):
    def fn(d, W, H):
        d.ellipse([W * 0.04, H * 0.04, W * 0.96, H * 0.96], fill=col + (255,), outline=_mix(col, (0, 0, 0), 0.5) + (255,),
                  width=max(2, int(W * 0.05)))
        d.ellipse([W * 0.22, H * 0.16, W * 0.48, H * 0.4], fill=(255, 255, 255, 170))
    return fn


# ============================================================================ the games / les jeux
def _g(label, col, back, value="health", **kw):
    return dict(value=value, label=label, col=col, back=back, **kw)


VIE = ("VIE", "LIFE")
SPECS = {
    # beat'em ups / beat'em up
    "ffight": dict(theme="ff_slum", hit="fist", gauge=_g(VIE, (255, 220, 40), (170, 30, 30))),
    "captcomm": dict(theme="cc_future", hit="fist", names=True, gauge=_g(VIE, (170, 230, 60), (40, 60, 30))),
    "dino": dict(theme="cd_ruins", hit="fist", names=True, gauge=_g(VIE, (255, 220, 40), (170, 30, 30))),
    "punisher": dict(theme="pn_mansion", hit="gun", gauge=_g(VIE, (60, 220, 240), (30, 40, 60)), bombs=dict(label=("GRENADES", "GRENADES"))),
    "kod": dict(theme="kd_forest", hit="slash", gauge=_g(VIE, (80, 220, 90), (40, 40, 60)),
                levels=[dict(value="level", label=("NIVEAU", "LEVEL"), up=("NIVEAU SUPÉRIEUR !", "LEVEL UP!")),
                        dict(value="weapon", label=("ÉPÉE", "SWORD"), up=("ÉPÉE +1 !", "SWORD UP!")),
                        dict(value="shield", label=("BOUCLIER", "SHIELD"), up=("BOUCLIER +1 !", "SHIELD UP!"))]),
    "knights": dict(theme="kn_village", hit="slash", gauge=_g(VIE, (240, 60, 50), (50, 30, 30)),
                    levels=[dict(value="level", label=("NIVEAU", "LEVEL"), up=("NIVEAU SUPÉRIEUR !", "LEVEL UP!"))]),
    "wof": dict(theme="wf_forest", hit="slash", gauge=_g(VIE, (200, 230, 40), (60, 40, 20))),
    "ddsom": dict(theme="ds_canyon", hit="slash", gauge=_g(VIE, (80, 220, 90), (40, 40, 60))),
    "ddtod": dict(theme="dt_hills", hit="slash", gauge=_g(VIE, (80, 220, 90), (40, 40, 60)),
                  counters=[dict(value="daggers", label=("DAGUES", "DAGGERS"), icon="dagger", throw="dagger", p1_only=True)]),
    "avsp": dict(theme="av_ruins", hit="gun", names=True, gauge=_g(VIE, (255, 220, 40), (60, 30, 30)),
                 gauge2=_g(("SPÉCIAL", "SPECIAL"), (120, 190, 255), (24, 30, 50), value="power", spend=True)),
    "armwar": dict(theme="aw_hangar", hit="gun", names=True, gauge=_g(VIE, (90, 220, 255), (30, 40, 60))),
    "batcir": dict(theme="bc_arena", hit="fist", gauge=_g(VIE, (255, 220, 40), (60, 30, 50)),
                   counters=[dict(value="money", label=("COIN", "COIN"), p1_only=True)]),
    # action and platforms / action et plateformes
    "ghouls": dict(theme="gg_grave", hit="throw", weapon=True, armor=True, two=True),
    "strider": dict(theme="st_city", hit="slash", two=False, big=dict(value="pods", label=("ROBOTS D'APPUI", "OPTION ROBOTS"), icon="pod")),
    "mtwins": dict(theme="mt_forest", hit="slash", gauge=_g(("VITAL", "VITAL"), (80, 160, 255), (24, 30, 60))),
    "msword": dict(theme="ms_tower", hit="slash", floor=True,
                   gauge=_g(("VITAL", "VITAL"), (255, 220, 40), (60, 30, 30)),
                   gauge2=_g(("PUISSANCE", "POWER"), (255, 140, 60), (50, 24, 20), value="power", full=True),
                   counters=[dict(value="keys", label=("CLÉS", "KEYS"), icon="key", p1_only=True)],
                   labels=[dict(value="partner", names=MS_PARTNERS)]),
    "willow": dict(theme="wl_village", hit="magic", two=False, gauge=_g(("VITAL", "VITAL"), (255, 170, 60), (60, 30, 20)),
                   labels=[dict(value="hero", names=WILLOW, default=("SORCIER", "SORCERER"))]),
    "nemo": dict(theme="nm_dream", hit="magic", bombs=dict(label=("ATTAQUES SPÉCIALES", "SPECIAL ATTACKS"), icon="star"), bombs_big=True),
    "3wonders": dict(theme="tw_woods", hit="throw", weapon=True, weapon_names=TW_WEAPONS),
    "dynwar": dict(theme="dw_field", hit="slash", gauge=_g(("VIT", "VIT"), (90, 220, 110), (40, 40, 30)),
                   levels=[dict(value="level", label=("NIVEAU", "LEVEL"), up=("NIVEAU SUPÉRIEUR !", "LEVEL UP!"))]),
    "pang3": dict(theme="pg_temple", hit="balloon", balloons=True),
    "mpang": dict(theme="pg_peak", hit="balloon", balloons=True),
    # run and gun
    "mercs": dict(theme="mc_desert", hit="gun", gauge=_g(("ÉNERGIE", "ENERGY"), (90, 220, 110), (70, 24, 24)),
                  bombs=dict(label=("MÉGA ATTAQUE", "MEGA CRASH")),
                  names=("p1_weapon", "p2_weapon"), name_watch=("weapon", "weapon_p2"), name_popup=True,    # the weapon held / l'arme
                  name_level=("weapon_level", ("PUISSANCE +1 !", "POWER UP!")),                          # its power-ups (POW)
                  floor=dict(value="mission", label=("MISSION", "MISSION"),
                             done=("MISSION {n} ACCOMPLIE !", "MISSION {n} COMPLETE!"))),
}


def _scene(key, spec):
    return type(f"PanelScene_{key}", (PanelScene,), {"THEME": spec["theme"], "SPEC": spec})


SCENES = {key: _scene(key, spec) for key, spec in SPECS.items()}
_THEMES = (hd_themes12, hd_themes13, hd_themes14)   # imported for their backdrops
