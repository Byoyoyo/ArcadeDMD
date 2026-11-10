"""The credits as in Metal Slug, for the other scenes of the HD screen (1.31, the Cave shoot'em ups).

The gold coin struck with the symbol of config.json (coin_symbol: €, $, £, "" for a plain coin) and CRÉDITS 07, big
and bright in a dark pill with a gold edge that stands out from the scenery. Each coin put in falls onto the coin of the
pill, the coin and the number jump, the edge lights up, sparks fly and +1 CRÉDIT rises. The same drawing and the same
timings as the Metal Slug scene (dmd/hd_mslug.py, 1.30).

Les crédits comme dans Metal Slug, pour les autres scènes de l'écran HD : la pièce d'or frappée du symbole de
config.json et CRÉDITS 07, gros et clairs dans une pastille sombre au bord doré. Chaque pièce mise tombe sur la pièce
de la pastille, la pièce et le nombre sautent, le bord s'allume, des étincelles et +1 CRÉDIT qui monte.
"""

from PIL import Image, ImageDraw

from .hd_mslug import CREAM, GOLD, coin_img
from .i18n import tr


def credits_word(n):
    return tr(f"+{n} CRÉDIT" + ("S" if n > 1 else ""), f"+{n} CREDIT" + ("S" if n > 1 else ""))


class CreditsBar:
    """The coin, CRÉDITS and the number in their pill, and the coins that fall onto it. / La pastille des crédits."""

    def __init__(self, hd, fx):
        self.hd, self.fx, self.pg, self.S = hd, fx, hd.pg, hd.S
        self.symbol = None
        self.icon = None
        self.sprite = "coin"
        self.pills = {}
        self.coins = {}
        self.coin_t = -99.0           # when the last coin landed / quand la dernière pièce est tombée
        self.xy = None                # the coin of the pill, where the coins land / où tombent les pièces
        self.box = None               # middle and top of the pill, for +n CRÉDITS / milieu et haut de la pastille
        self.credits = None
        self.said = (0, -99.0)        # the last +n and when, for a scene that writes it itself / le dernier +n et quand
        self.drops = 0                # (tests)
        self.set_symbol("€")

    def set_symbol(self, symbol):
        """The coin of the pill and the falling coins carry the symbol of config.json. / Le symbole de config.json."""
        symbol = str(symbol or "").strip()[:2]
        if symbol == self.symbol:
            return
        self.symbol = symbol
        img = coin_img(self.S(54), symbol, self.hd.font)
        self.icon = self.hd._surf(img)
        self.coins.clear()
        self.sprite = "coin" + symbol                         # one name per symbol: turned copies stay right / une par symbole
        self.fx.sp.register(self.sprite, img)

    def watch(self, credits, now, quiet=False, drop=True):
        """Credits that go up: as many coins fall (three at most), +n CRÉDITS once for them all, not when quiet (an attract
        screen that says it). drop=False only follows them (the pill is not on the screen). / Des crédits en plus :
        autant de pièces qui tombent, un seul +n CRÉDITS. drop=False les suit seulement (pastille pas à l'écran)."""
        if isinstance(credits, bool) or not isinstance(credits, (int, float)):
            credits = None
        if drop and credits is not None and self.credits is not None and credits > self.credits:
            self.coin(now, int(credits - self.credits), quiet)
        self.credits = credits

    def coin(self, now, n, quiet=False):
        k = min(3, max(1, n))
        for i in range(k):
            self.fx.later(i * 0.22, self._drop, n if i == k - 1 else 0, quiet)

    def _drop(self, n, quiet):
        x, y = self.xy or (self.hd.W / 2, self.hd.H - self.S(44))
        p = self.fx.projectile(self.sprite, x, self.S(-40), x, y, 0.55, 90, self._ding, spin=0, trail=0)
        p.on_end = (self._ding, (x, y, n, quiet))
        p.floor, p.bounce = y, 0.0                            # stops right on the coin / s'arrête pile dessus
        self.drops += 1

    def _ding(self, x, y, n=0, quiet=False):
        self.coin_t = self.fx.now
        self.fx.glow(x, y, 12, 96, GOLD, 0.35)
        self.fx.sparks(x, y, 16, GOLD, (180, 520), (200, 340), (0.3, 0.6), 500, "front", 2, 18)
        if n and not quiet:
            self.said = (n, self.fx.now)
        if n and not quiet and self.box is not None:
            bx, by = self.box
            self.fx.text(credits_word(n), bx, by - self.S(30), GOLD, 36, life=1.2, rise=40)

    def draw(self, screen, credits, cx, cy, now, k=1.0):
        """The coin and CRÉDITS 07 in the pill, centred on (cx, cy); k scales it (1 = as in Metal Slug). Returns the
        width of the pill. / La pièce et CRÉDITS 07 dans la pastille ; k la met à l'échelle. Rend sa largeur."""
        hd, S = self.hd, self.S
        bump = max(0.0, 1 - (now - self.coin_t) / 0.35)
        num = f"{int(credits):02d}"
        lsize, nsize = S(32 * k), S(48 * k)
        lab = hd.text(tr("CRÉDITS", "CREDITS"), "stencil", lsize, CREAM, glow=0)
        nw = hd.text_width(num, "stencil", nsize)
        ic = self.icon
        if k != 1.0:
            ic = self.coins.get(k)
            if ic is None:
                ic = self.coins[k] = self.pg.transform.smoothscale(self.icon, (int(self.icon.get_width() * k),
                                                                                int(self.icon.get_height() * k)))
        cw = ic.get_width()
        ph = S(68 * k)
        pw = int(ph / 2 + cw / 2 + S(14 * k) + lab["w"] + S(16 * k) + nw + S(30 * k))
        x0, y0 = int(cx - pw / 2), int(cy - ph / 2)
        screen.blit(self.pill(pw, ph, int(round(bump * 6))), (x0, y0))
        icx = x0 + ph / 2
        self.xy, self.box = (icx, cy), (cx, y0)
        screen.blit(ic, (int(icx - ic.get_width() / 2), int(cy - ic.get_height() / 2 - bump * S(9 * k))))
        _, top, _, bottom, _ = hd._glyph("stencil", nsize, "0")
        base = cy + (bottom - top) / 2                        # label and number on one baseline / même ligne de pied
        x = icx + cw / 2 + S(14 * k)
        hd.put(screen, lab, x, base, "left", "bottom")
        x += lab["w"] + S(16 * k)
        hd.put_number(screen, num, "stencil", nsize, GOLD, x + nw / 2, cy, "center", "middle", scale=1 + 0.3 * bump, glow=0.45)
        return pw

    def pill(self, w, h, lv):
        """Dark pill with a gold edge, drawn smooth once per size; lv 0-6 lights the edge up.
        / Pastille sombre au bord doré, lisse, dessinée une fois par taille ; lv allume le bord."""
        key = (w, h, lv)
        p = self.pills.get(key)
        if p is None:
            if len(self.pills) > 40:
                self.pills.clear()
            ss = 3
            img = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            e = max(2, self.S(3)) * ss
            f = 0.6 + 0.4 * lv / 6
            d.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=h * ss // 2, fill=tuple(int(c * f) for c in GOLD) + (255,))
            d.rounded_rectangle([e, e, w * ss - 1 - e, h * ss - 1 - e], radius=h * ss // 2 - e, fill=(10, 12, 26, 226))
            p = self.pills[key] = self.hd._surf(img.resize((w, h), Image.LANCZOS))
        return p
