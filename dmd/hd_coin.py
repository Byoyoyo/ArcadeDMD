"""Attract screen of the fighting games on the HD screen.

Two coin doors, with a coin spinning above each one. When the credits go up, a coin turns on its edge and
drops into its slot: sparks, +1, and the credit counter rolls. A moment later the doors make way for the 1P and
2P START buttons and PRESS START. No coin put in, nothing drops: the coins just keep spinning.
Coins, doors, buttons and neon texts are prepared once with Pillow, then kept as pygame surfaces.

Écran d'attente des jeux de combat sur l'écran HD.

Deux monnayeurs, une pièce qui tourne au-dessus de chacun. Quand les crédits montent, une pièce se met sur la
tranche et tombe dans sa fente : étincelles, +1, le compteur de crédits roule. Puis les boutons START 1P et 2P
et PRESS START. Sans pièce mise, rien ne tombe : les pièces tournent.
Pièces, monnayeurs, boutons et textes néon sont préparés une fois avec Pillow, puis gardés en surfaces pygame.
"""

import math
import time

from PIL import Image, ImageDraw, ImageFilter

from .i18n import tr

NEON = (255, 150, 40)
ROLL = (255, 170, 50)
SMALL = (230, 190, 120)
PLUS = (255, 200, 60)
RED_BUTTON, BLUE_BUTTON = (225, 30, 20), (30, 90, 235)


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def credit_word(n):
    return tr(f"CRÉDIT {n}", f"CREDIT {n}") if n <= 1 else tr(f"CRÉDITS {n}", f"CREDITS {n}")


class CoinDoors:
    HOLD = 2.6                    # CREDITS n stays this long after a coin, then the START buttons
    FALL, FLASH, BACK = 0.35, 0.25, 0.4
    PHASES = 40                   # images of a coin turn
    SWAP = 0.3                    # doors <-> buttons crossfade
    HOVER, R = 96, 46             # coin above its door (1920 x 460 units)
    SLOT_TOP = 260

    def __init__(self, hd):
        self.hd, self.pg = hd, hd.pg
        self.s, self.S, self.W = hd.s, hd.S, hd.W
        self.cache = {}
        self.credits = None
        self.seen = None
        self.drops = []           # [start, door, landed]
        self.shown = 0            # number on the counter
        self.roll = None          # (from, to, moment)
        self.last_land = None
        self.side = 1             # next coin: right door first, then they take turns
        self.mode = None
        self.mode_t = -99.0
        self.plus = []            # (moment, x): +1 rising above a door
        self.todo = None
        self.symbol = "€"

    # ------------------------------------------------------------ prepared images
    def _get(self, key, make):
        surf = self.cache.get(key)
        if surf is None:
            surf = self.cache[key] = make()
        return surf

    def _coin(self, symbol, i):
        return self._get(("coin", symbol, i % self.PHASES), lambda: self._coin_img(symbol, (i % self.PHASES) / self.PHASES))

    def _coin_face(self, symbol):
        """The coin seen from the front, drawn once: a turning coin is this face squeezed, in front of its edge."""
        def make():
            ss = 3
            r = self.R * self.s * ss
            d2 = int(2 * r) + 2
            c = d2 / 2
            img = Image.new("RGBA", (d2, d2), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.ellipse([c - r, c - r, c + r, c + r], fill=(196, 128, 18, 255))
            for i in range(14):
                k = i / 14
                rr = r * 0.84 * (1 - k * 0.8)
                d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=_mix((232, 165, 28), (255, 238, 150), k) + (255,))
            if symbol:                                           # symbol in relief
                fe = self.hd.font("black", max(8, int(r * 1.15 / max(1.0, 0.75 * len(symbol)))))
                l, t, rr_, b = fe.getbbox(symbol)
                m = Image.new("L", (max(1, rr_ - l) + 8, max(1, b - t) + 8), 0)
                ImageDraw.Draw(m).text((4 - l, 4 - t), symbol, font=fe, fill=255)
                ox, oy = int(c - m.width / 2), int(c - m.height / 2)
                img.paste((255, 246, 190, 255), (ox - ss, oy - ss), m)          # light edge, top left
                img.paste((176, 104, 10, 255), (ox + ss, oy + ss), m)           # shadow, bottom right
                img.paste((214, 142, 22, 255), (ox, oy), m)
            hl = Image.new("RGBA", (d2, d2), (0, 0, 0, 0))
            ImageDraw.Draw(hl).ellipse([c - r * 0.6, c - r * 0.75, c - r * 0.05, c - r * 0.25], fill=(255, 255, 255, 150))
            img = Image.alpha_composite(img, hl.filter(ImageFilter.GaussianBlur(4 * ss)))
            dd = max(4, int(round(2 * self.R * self.s)))
            return img.resize((dd, dd), Image.LANCZOS)
        return self._get(("face", symbol), make)

    def _coin_img(self, symbol, phase):
        face = self._coin_face(symbol)
        dd = face.width
        a = 2 * math.pi * phase
        af = abs(math.cos(a))
        size = dd + 2 * int(math.ceil(dd * 0.1)) + 4
        ss = 2
        img = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx = cy = size * ss / 2
        r = dd * ss / 2
        rx = max(2.5 * ss, r * af)
        side = r * 0.17 * math.sin(a)                            # coin thickness, seen when it turns
        d.ellipse([cx - rx + side, cy - r, cx + rx + side, cy + r], fill=(135, 82, 8, 255))
        if abs(side) > 1:
            x0, x1 = sorted((cx, cx + side))
            d.rectangle([x0, cy - r, x1, cy + r], fill=(150, 92, 10, 255))
        img = img.reduce(ss)                                      # 2 x drawing brought back: smooth edges
        fw = max(5, int(round(dd * af)))
        img.alpha_composite(face.resize((fw, dd), Image.LANCZOS), (int(round(size / 2 - fw / 2)), int(round(size / 2 - dd / 2))))
        return self.hd._surf(img)

    def _panel(self, glow, flash):
        gi = max(0, min(7, int(round((glow - 0.2) / 0.8 * 7))))
        fi = max(0, min(5, int(round(flash * 5))))
        return self._get(("panel", gi, fi), lambda: self._panel_img(0.2 + 0.8 * gi / 7, fi / 5))

    def _panel_parts(self):
        """What never changes on a coin door: the glow's shape, the metal plate, its rim and screws."""
        def make():
            ss = 2
            z = self.s * ss
            w, h, pad = 170 * z, 230 * z, 40 * z
            size = (int(w + 2 * pad), int(h + 2 * pad))
            win = [pad + 22 * z, pad + 40 * z, pad + w - 22 * z, pad + h - 30 * z]
            m = Image.new("L", size, 0)
            ImageDraw.Draw(m).rounded_rectangle(win, int(18 * z), fill=255)
            plate = Image.new("RGBA", size, (0, 0, 0, 0))
            grad = Image.new("RGBA", size, (0, 0, 0, 0))
            gd = ImageDraw.Draw(grad)
            for i in range(int(h) + 1):
                gd.line([pad, pad + i, pad + w, pad + i], fill=_mix((92, 96, 108), (36, 38, 46), i / max(1, h)) + (255,))
            mask = Image.new("L", size, 0)
            ImageDraw.Draw(mask).rounded_rectangle([pad, pad, pad + w, pad + h], int(22 * z), fill=255)
            plate.paste(grad, (0, 0), mask)
            d = ImageDraw.Draw(plate)
            d.rounded_rectangle([pad, pad, pad + w, pad + h], int(22 * z), outline=(150, 154, 168, 255), width=max(1, int(4 * z)))
            for x, y in ((pad + 16 * z, pad + 16 * z), (pad + w - 16 * z, pad + 16 * z), (pad + 16 * z, pad + h - 16 * z),
                         (pad + w - 16 * z, pad + h - 16 * z)):
                d.ellipse([x - 5 * z, y - 5 * z, x + 5 * z, y + 5 * z], fill=(180, 184, 196, 255))
            return {"blur": m.filter(ImageFilter.GaussianBlur(22 * z)), "plate": plate, "z": z, "w": w, "h": h, "pad": pad,
                    "size": size, "win": win, "ss": ss}
        return self._get("panel_parts", make)

    def _panel_img(self, glow, flash):
        """Coin door: metal plate, red lit window, slot, arrow and 1 CREDIT."""
        P = self._panel_parts()
        z, w, h, pad, win, ss = P["z"], P["w"], P["h"], P["pad"], P["win"], P["ss"]
        lit = _mix((150, 20, 5), (255, 60, 25), glow)
        if flash:
            lit = _mix(lit, (255, 255, 255), flash)
        k = 0.9 * (0.5 + 0.5 * glow) + flash
        img = Image.new("RGBA", P["size"], lit + (0,))
        img.putalpha(P["blur"].point(lambda v: min(255, int(v * k))))
        img = Image.alpha_composite(img, P["plate"])
        d = ImageDraw.Draw(img)
        d.rounded_rectangle(win, int(16 * z), fill=_mix((70, 0, 0), lit, 0.85) + (255,),
                            outline=_mix(lit, (255, 255, 255), 0.4) + (255,), width=max(1, int(3 * z)))
        sx = pad + w / 2
        d.rounded_rectangle([sx - 7 * z, pad + 70 * z, sx + 7 * z, pad + h - 66 * z], int(6 * z), fill=(8, 0, 0, 255),
                            outline=(255, 210, 190, 200), width=max(1, int(2 * z)))
        d.polygon([(sx - 14 * z, pad + 50 * z), (sx + 14 * z, pad + 50 * z), (sx, pad + 64 * z)], fill=(255, 235, 220, 230))
        d.text((sx, pad + h - 46 * z), tr("1 CRÉDIT", "1 CREDIT"), font=self.hd.font("black", max(6, int(19 * z))),
               fill=(255, 240, 230, 240), anchor="mm")
        return self.hd._surf(img.reduce(ss))

    def _button(self, color, pressed, glow, label):
        gi = max(0, min(5, int(round(glow * 5))))
        return self._get(("button", color, pressed, gi, label), lambda: self._button_img(color, pressed, gi / 5, label))

    def _button_parts(self):
        def make():
            ss = 2
            z = self.s * ss
            R, pad = 70 * z, 50 * z
            size = int(2 * (R + pad))
            c = size / 2
            m = Image.new("L", (size, size), 0)
            ImageDraw.Draw(m).ellipse([c - R - 8 * z, c - R - 8 * z, c + R + 8 * z, c + R + 8 * z], fill=255)
            hl = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            ImageDraw.Draw(hl).ellipse([c - R * 0.55, c - R * 0.8, c + R * 0.1, c - R * 0.35], fill=(255, 255, 255, 140))
            return {"blur": m.filter(ImageFilter.GaussianBlur(24 * z)), "hl": hl.filter(ImageFilter.GaussianBlur(6 * z)),
                    "z": z, "R": R, "size": size, "ss": ss}
        return self._get("button_parts", make)

    def _button_img(self, color, pressed, glow, label):
        P = self._button_parts()
        z, R, size, ss = P["z"], P["R"], P["size"], P["ss"]
        c = size / 2
        k = 0.4 + 0.8 * glow
        img = Image.new("RGBA", (size, size), color + (0,))
        img.putalpha(P["blur"].point(lambda v: min(255, int(v * k))))
        d = ImageDraw.Draw(img)
        d.ellipse([c - R - 12 * z, c - R - 8 * z, c + R + 12 * z, c + R + 16 * z], fill=(20, 20, 26, 255))
        d.ellipse([c - R - 10 * z, c - R - 10 * z, c + R + 10 * z, c + R + 10 * z], fill=(70, 72, 84, 255),
                  outline=(150, 152, 166, 255), width=max(1, int(3 * z)))
        oy = 8 * z if pressed else 0
        base = _mix(color, (0, 0, 0), 0.35 if pressed else 0.0)
        for i in range(16):
            q = i / 16
            rr = R * (1 - q * 0.75)
            d.ellipse([c - rr, c - rr + oy - q * 10 * z, c + rr, c + rr + oy - q * 10 * z],
                      fill=_mix(_mix(base, (0, 0, 0), 0.25), _mix(base, (255, 255, 255), 0.35), q) + (255,))
        if not pressed:
            img = Image.alpha_composite(img, P["hl"])
            d = ImageDraw.Draw(img)
        d.text((c, c + oy - 4 * z), label, font=self.hd.font("black", max(6, int(40 * z))), fill=(255, 255, 255, 230), anchor="mm")
        return self.hd._surf(img.reduce(ss))

    def _neon(self, text, size, color):
        """Neon text: wide soft glow, tighter glow, light core. Returns the surfaces and where the pen starts."""
        key = ("neon", text, size, color)
        hit = self.cache.get(key)
        if hit is None:
            f = self.hd.font("black", size)
            l, t, r, b = f.getbbox(text)
            pad = int(40 * self.s) + 2
            w, h = r - l + 2 * pad, b - t + 2 * pad
            m = Image.new("L", (w, h), 0)
            ImageDraw.Draw(m).text((pad - l, pad - t), text, font=f, fill=255)
            out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            for rad, k in ((18, 0.9), (7, 1.0)):
                g = Image.new("RGBA", (w, h), color + (0,))
                g.putalpha(m.filter(ImageFilter.GaussianBlur(max(1, rad * self.s))).point(lambda v, k=k: min(255, int(v * 1.6 * k))))
                out = Image.alpha_composite(out, g)
            core = Image.new("RGBA", (w, h), _mix(color, (255, 255, 255), 0.55) + (0,))
            core.putalpha(m)
            out = Image.alpha_composite(out, core)
            white = Image.new("RGBA", (w, h), (255, 255, 255, 0))
            white.putalpha(m)
            band = Image.new("RGBA", (int(60 * self.s) * 3 + h, h), (255, 255, 255, 0))
            bm = Image.new("L", band.size, 0)
            bw = int(60 * self.s)
            ImageDraw.Draw(bm).polygon([(h * 0.5 + bw, 0), (h * 0.5 + 2 * bw, 0), (2 * bw, h), (bw, h)], fill=200)
            band.putalpha(bm.filter(ImageFilter.GaussianBlur(max(1, 10 * self.s))))
            hit = self.cache[key] = {"surf": self.hd._surf(out), "mask": self.hd._surf(white), "band": self.hd._surf(band),
                                     "ox": pad - l, "oy": pad - t, "w": r - l, "h": b - t, "pad": pad}
        return hit

    def _blit(self, screen, surf, pos, alpha=1.0, area=None):
        if alpha <= 0.01:
            return
        if alpha < 0.99:
            surf.set_alpha(int(255 * alpha))
        if area is not None:
            screen.blit(surf, (int(pos[0]), int(pos[1])), area)
        else:
            screen.blit(surf, (int(pos[0]), int(pos[1])))
        if alpha < 0.99:
            surf.set_alpha(255)

    def _put_neon(self, screen, n, x, y, alpha=1.0, shine=None, mid=False):
        """Neon text. The pen starts at (x, y) (left edge, top of the font's ascenders), or with mid=True the
        letters are centered on (x, y)."""
        pos = (x - n["w"] / 2 - n["pad"], y - n["h"] / 2 - n["pad"]) if mid else (x - n["ox"], y - n["oy"])
        self._blit(screen, n["surf"], pos, alpha)
        if shine is not None and alpha > 0.3:                  # light sweeping across the letters
            surf = n["surf"]
            w, h = surf.get_size()
            bw = n["band"].get_width()
            tmp = self.pg.Surface((w, h), self.pg.SRCALPHA)
            tmp.blit(n["band"], (int(-bw + (w + bw) * shine), 0))
            tmp.blit(n["mask"], (0, 0), special_flags=self.pg.BLEND_RGBA_MULT)
            self._blit(screen, tmp, pos, alpha)

    def warm(self, budget=0.003, symbol=None):
        """Prepares the images a little at a time, before they are needed (no jolt at the first coin)."""
        if self.todo is None:
            sym = self.symbol if symbol is None else symbol
            self.todo = [lambda i=i: self._coin(sym, i) for i in range(self.PHASES)]
            self.todo += [lambda g=g: self._panel(0.2 + 0.8 * g / 7, 0.0) for g in range(8)]
            self.todo += [lambda f=f: self._panel(1.0, f / 5) for f in range(1, 6)]
            S = self.S
            self.todo += [lambda: self._neon("INSERT COIN", S(74), NEON), lambda: self._neon("+1", S(70), PLUS),
                          lambda: self._neon("PRESS START", S(74), NEON)]
            for color, label in ((RED_BUTTON, "1P"), (BLUE_BUTTON, "2P")):
                for g in range(6):
                    for p in (False, True):
                        self.todo.append(lambda c=color, p=p, g=g, lab=label: self._button(c, p, g / 5, lab))
        end = time.perf_counter() + budget
        while self.todo and time.perf_counter() < end:
            self.todo.pop(0)()

    # ------------------------------------------------------------ what happens
    def door_x(self, side):
        return self.S(230) if side == 0 else self.W - self.S(230)

    def _track(self, vals, now, fx):
        c = _num(vals.get("credits"))
        c = int(c) if c is not None else None
        if self.seen is None or now - self.seen > 0.5 or c is None or self.credits is None:
            # shown again (or no credits value): no coin for the credits added meanwhile
            self.credits, self.shown = c, max(0, c or 0)
            self.drops, self.roll, self.last_land, self.mode, self.plus = [], None, None, None, []
        elif c > self.credits:
            t = max([now] + [d[0] + 0.3 for d in self.drops])
            for i in range(min(4, c - self.credits)):
                self.drops.append([t + 0.3 * i, self.side, False])
                self.side = 1 - self.side
            self.credits = c
        elif c < self.credits:                                         # a credit used: the game starts
            self.credits = self.shown = c
            self.drops = [d for d in self.drops if d[2]]
        self.seen = now
        S = self.S
        for d in self.drops:
            if not d[2] and now >= d[0] + self.FALL:                   # the coin is in
                d[2] = True
                land = d[0] + self.FALL
                self.roll = (self.shown, self.shown + 1, land)
                self.shown += 1
                self.last_land = land
                x = self.door_x(d[1])
                self.plus.append((land, x))
                if fx is not None and now - land < 0.2:
                    fx.sparks(x, S(self.SLOT_TOP + 2), 36, (255, 220, 120), speed=(180, 520), angle=(198, 342), life=(0.45, 0.9),
                              gravity=420, layer="front", width=3, length=16)
                    fx.glow(x, S(self.SLOT_TOP + 10), 20, 130, (255, 230, 160), 0.35, "front", 0.9, 0.0)
        self.drops = [d for d in self.drops if now < d[0] + self.FALL + self.FLASH + self.BACK]
        self.plus = [p for p in self.plus if now - p[0] < 0.95]

    def doors_shown(self, now):
        return bool(self.drops) or (self.last_land is not None and now - self.last_land < self.HOLD) or self.shown <= 0

    # ------------------------------------------------------------ drawing
    def draw(self, screen, vals, now, fx=None, symbol="€", enter=1.0):
        """enter < 1: the attract screen arrives after the game's logo (doors coming in from the edges)."""
        symbol = str(symbol or "").strip()[:2]
        if symbol != self.symbol:
            self.symbol, self.todo = symbol, None
        self._track(vals, now, fx)
        doors = self.doors_shown(now)
        mode = "doors" if doors else "buttons"
        if mode != self.mode:
            self.mode_t = now if self.mode is not None else -99.0
            self.mode = mode
        k = min(1.0, max(0.0, (now - self.mode_t) / self.SWAP))
        a_doors = k if doors else 1.0 - k
        e = 1 - (1 - max(0.0, min(1.0, enter))) ** 3
        if e <= 0.001:                                           # still behind the game's logo
            self.warm()
            return
        dx = (1 - e) * self.S(420)
        if a_doors > 0.01:
            self._draw_doors(screen, now, a_doors, dx)
        if a_doors < 0.99:
            self._draw_buttons(screen, now, 1.0 - a_doors, dx)
        on = 1.0 if enter >= 1 else (0.2 if int(enter * 24) % 4 == 1 else e)       # the neon turns on
        self._draw_texts(screen, now, a_doors, on)
        for t0, x in self.plus:
            q = max(0.0, (now - t0) / 0.95)
            self._put_neon(screen, self._neon("+1", self.S(70), PLUS), x, self.S(140) - self.S(90) * q, 1 - 0.9 * q, mid=True)
        self.warm()

    def _draw_doors(self, screen, now, alpha, dx):
        S = self.S
        top = S(self.SLOT_TOP)
        for side in (0, 1):
            cx = self.door_x(side) + (-dx if side == 0 else dx)
            drop = next((d for d in self.drops if d[1] == side and d[0] <= now), None)
            glow = 0.6 + 0.4 * math.sin(now * 4 + (0.0 if side == 0 else 1.3))
            spin = (now * 0.8 + (0.0 if side == 0 else 0.37)) % 1.0
            lt = now - drop[0] if drop is not None else None
            flash = 0.0
            if lt is None:                                           # spinning above the door
                coin = self._coin(self.symbol, int(spin * self.PHASES))
                self._blit(screen, coin, (cx - coin.get_width() / 2, S(self.HOVER) - coin.get_height() / 2), alpha)
            elif lt >= self.FALL + self.FLASH:                       # the next coin comes down
                q = min(1.0, (lt - self.FALL - self.FLASH) / self.BACK)
                coin = self._coin(self.symbol, int(spin * self.PHASES))
                self._blit(screen, coin, (cx - coin.get_width() / 2, S(self.HOVER) - S(20) * (1 - q) - coin.get_height() / 2),
                           alpha * min(1.0, q * 1.4))
            elif lt >= self.FALL:
                flash = 1.0 - (lt - self.FALL) / self.FLASH
            panel = self._panel(glow, flash)
            self._blit(screen, panel, (cx - panel.get_width() / 2, S(150)), alpha)
            if lt is not None and lt < self.FALL:                    # on its edge, it drops into the slot
                q = lt / self.FALL
                p0 = (drop[0] * 0.8 + (0.0 if side == 0 else 0.37)) % 1.0
                target = min((0.25, 0.75, 1.25), key=lambda c: abs(c - p0))
                ph = p0 + (target - p0) * (1 - (1 - min(1.0, q / 0.3)) ** 2)
                coin = self._coin(self.symbol, int(round(ph * self.PHASES)))
                cy = S(self.HOVER) + (top + S(self.R + 6) - S(self.HOVER)) * q ** 1.7
                x0, y0 = cx - coin.get_width() / 2, cy - coin.get_height() / 2
                cut = int(top - int(y0))
                if cut > 0:
                    self._blit(screen, coin, (x0, y0), alpha, self.pg.Rect(0, 0, coin.get_width(), min(coin.get_height(), cut)))

    def _draw_buttons(self, screen, now, alpha, dx):
        S = self.S
        g = 0.5 + 0.5 * math.sin(now * 6)
        for side, color, label, pressed, glow in ((0, RED_BUTTON, "1P", 0.15 < now % 1.3 < 0.4, g),
                                                 (1, BLUE_BUTTON, "2P", 0.8 < now % 1.3 < 1.05, 1 - g)):
            b = self._button(color, pressed, glow, label)
            cx = self.door_x(side) + (-dx if side == 0 else dx)
            self._blit(screen, b, (cx - b.get_width() / 2, S(280) - b.get_height() / 2), alpha)

    def _draw_texts(self, screen, now, a_doors, on):
        S, W = self.S, self.W
        size = S(74)
        cap = int(size * 0.61)                                   # from the top of the capitals to their middle
        if a_doors > 0.01:
            if self.shown <= 0:
                flick = 1.0 if (int(now * 10) % 23) not in (3, 5) else 0.55
                self._put_neon(screen, self._neon("INSERT COIN", size, NEON), W / 2, S(372),
                               a_doors * on * flick * (0.85 + 0.15 * math.sin(now * 5)), shine=(now % 2.4) / 2.4 * 1.6 - 0.3, mid=True)
            else:
                self._draw_counter(screen, now, a_doors * on, size, S(372) - cap)
        if a_doors < 0.99:
            a = (1.0 - a_doors) * on
            self._put_neon(screen, self._neon("PRESS START", size, NEON), W / 2, S(365), a * (0.8 + 0.2 * math.sin(now * 6)),
                           shine=(now % 2.4) / 2.4 * 1.6 - 0.3, mid=True)
            t = self.hd.text(credit_word(self.shown), "bold", S(30), SMALL, glow=0)
            self.hd.put(screen, t, W / 2, S(428), "center", "middle", alpha=a)

    def _draw_counter(self, screen, now, alpha, size, y):
        """CREDITS n, the number rolls from the old value to the new one."""
        n = self.shown
        old, new, t0 = self.roll if self.roll is not None and self.roll[1] == n else (n, n, -99.0)
        roll = min(1.0, max(0.0, (now - t0) / 0.3))
        flash = int(round(max(0.0, 1 - (now - t0) / 0.5) * 5)) / 5
        col = _mix(ROLL, (255, 255, 255), flash * 0.7)
        word = credit_word(n)
        num = str(n)
        label = word[:-len(num)]
        f = self.hd.font("black", size)
        x0 = self.W / 2 - f.getlength(word) / 2
        self._put_neon(screen, self._neon(label.rstrip(), size, col), x0, y, alpha)
        nx = x0 + f.getlength(label)
        if roll >= 1.0:
            self._put_neon(screen, self._neon(num, size, col), nx, y, alpha)
            return
        shift = size * 1.1
        a = self._neon(str(old), size, ROLL)
        b = self._neon(num, size, col)
        clip = screen.get_clip()
        pad = self.S(20)
        screen.set_clip(self.pg.Rect(int(nx - pad), int(y - self.S(4)), int(max(a["w"], b["w"]) + 2 * pad), int(size * 1.05)).clip(clip))
        self._put_neon(screen, a, nx, y - shift * roll, alpha)
        self._put_neon(screen, b, nx, y + shift * (1 - roll), alpha)
        screen.set_clip(clip)
