"""Drawing helpers for the Destiny theme wallpapers.

Everything is drawn in design units: the sheet is always 1080 units tall and
as wide as the aspect ratio makes it (2520 for 21:9, 1920 for 16:9). One unit
is two pixels on a 2160-pixel-tall image.

Angles are in degrees, 0 points right, and they grow clockwise because the
y axis points down.
"""

import colorsys
import math
import os
import random
import re

import cairo
import numpy as np
from PIL import Image, ImageFilter

WHITE = (0.95, 0.965, 0.98)
# ARC is the main accent of a sheet and GOLD the second one. They are lists, not
# tuples, on purpose: every module imports these two objects and uses them as
# default arguments, so Sheet.set_palette() recolours a sheet by changing them
# in place. Sheets are rendered one after another, never at the same time.
ARC = [0.298, 0.788, 1.000]   # accent from colors.toml, #4cc9ff
GOLD = [0.961, 0.788, 0.271]  # yellow from colors.toml, #f5c945
RED = (1.000, 0.329, 0.408)   # red from colors.toml, #ff5468
FONT = "Nimbus Sans"
SUBS = dict(zip("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
SUPS = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-"))


ICE = (0.298, 0.788, 1.000)   # Arc, the theme's accent
SUN = (0.961, 0.788, 0.271)   # exotic gold, the theme's yellow

# name: (hue in degrees, saturation, lightness of the middle of the gradient,
#        accent, second accent). Greens and yellows look brighter than blues at
# the same lightness, so they get a lower number.
PALETTES = {
    "navy":     (220, 0.50, 0.130, ICE, SUN),   # the theme's own ground, lifted a little
    "teal":     (176, 0.34, 0.165, (0.94, 0.53, 0.46), SUN),
    "indigo":   (248, 0.32, 0.200, ICE, SUN),
    "plum":     (302, 0.26, 0.180, (0.95, 0.64, 0.83), SUN),
    "rust":     (14, 0.38, 0.175, (0.96, 0.74, 0.40), ICE),
    "olive":    (92, 0.26, 0.150, (0.74, 0.87, 0.46), SUN),
    "petrol":   (196, 0.46, 0.165, (0.97, 0.67, 0.34), ICE),
    "violet":   (270, 0.40, 0.165, (0.56, 0.90, 1.00), SUN),
    "graphite": (220, 0.05, 0.175, (0.50, 0.90, 0.70), SUN),
    "wine":     (346, 0.34, 0.170, (0.96, 0.72, 0.54), SUN),
    "royal":    (226, 0.44, 0.195, (0.86, 0.91, 0.44), ICE),
    "sand":     (44, 0.22, 0.160, ICE, SUN),
    "grass":    (136, 0.34, 0.150, (0.64, 0.91, 0.47), SUN),
    "umber":    (26, 0.30, 0.145, ICE, SUN),
}


def polar(cx, cy, r, deg):
    t = math.radians(deg)
    return cx + r * math.cos(t), cy + r * math.sin(t)


def load_logo(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "omarchy-logo.svg")):
    """Read the Omarchy wordmark. Its paths use only relative m, l, h, v and z.

    Returns (width, height, subpaths); each subpath is a list of points.
    """
    svg = open(path).read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
    subpaths = []
    for d in re.findall(r' d="([^"]+)"', svg):
        tokens = re.findall(r"[a-zA-Z]|-?\d*\.?\d+", d)
        x = y = 0.0
        cmd, i, cur = None, 0, None
        while i < len(tokens):
            if tokens[i].isalpha():
                cmd = tokens[i]
                i += 1
                if cmd == "z":
                    subpaths.append(cur)
                    x, y = cur[0]
                    cur = None
                continue
            if cmd in ("m", "l"):
                x, y = x + float(tokens[i]), y + float(tokens[i + 1])
                i += 2
            elif cmd == "h":
                x += float(tokens[i])
                i += 1
            elif cmd == "v":
                y += float(tokens[i])
                i += 1
            else:
                raise ValueError(f"unexpected path command {cmd!r} in {path}")
            if cmd == "m":
                cur = [(x, y)]
                cmd = "l"  # further pairs after a move are line-tos
            else:
                cur.append((x, y))
    return w, h, subpaths


class Sheet:
    # How far the legend, the emblem and the sheet number stay away from the left
    # and right edges, in units. Omarchy fits a wallpaper by cropping, so a 16:9
    # file loses 5 % of each side on a 16:10 screen and 8 % on a 3:2 one. The
    # command line sets this; 0 means the file is made for one exact screen.
    side_inset = 0

    def __init__(self, width_px, height_px, seed=1):
        self.px = (width_px, height_px)
        self.s = height_px / 1080.0
        self.W = width_px / self.s
        self.H = 1080.0
        self.cx = self.W / 2
        self.cy = self.H / 2
        self.wide = self.W > 2300  # room for secondary views left and right
        self.inset = 0 if self.wide else Sheet.side_inset
        self.rng = random.Random(seed)
        self.set_palette("navy")
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width_px, height_px)
        self.c = cairo.Context(self.surface)
        self.c.scale(self.s, self.s)
        self.c.set_line_cap(cairo.LINE_CAP_BUTT)
        self.c.set_line_join(cairo.LINE_JOIN_MITER)

    # -- stroke and fill -------------------------------------------------

    def _ink(self, a, color):
        self.c.set_source_rgba(color[0], color[1], color[2], a)

    def _stroke(self, a, w, dash, color):
        self._ink(a, color)
        self.c.set_line_width(w)
        self.c.set_dash(dash or [])
        self.c.stroke()
        self.c.set_dash([])

    def ln(self, x1, y1, x2, y2, a=0.5, w=0.6, dash=None, color=WHITE):
        self.c.move_to(x1, y1)
        self.c.line_to(x2, y2)
        self._stroke(a, w, dash, color)

    def poly(self, pts, a=0.5, w=0.6, close=True, fill=0.0, dash=None, color=WHITE):
        self.c.move_to(*pts[0])
        for p in pts[1:]:
            self.c.line_to(*p)
        if close:
            self.c.close_path()
        if fill:
            self._ink(fill, color)
            self.c.fill_preserve()
        self._stroke(a, w, dash, color)

    def rect(self, x, y, w_, h_, a=0.5, w=0.6, fill=0.0, dash=None, color=WHITE):
        self.poly([(x, y), (x + w_, y), (x + w_, y + h_), (x, y + h_)], a, w, True, fill, dash, color)

    def circ(self, cx, cy, r, a=0.5, w=0.6, dash=None, fill=0.0, color=WHITE):
        self.c.new_sub_path()
        self.c.arc(cx, cy, r, 0, 2 * math.pi)
        if fill:
            self._ink(fill, color)
            self.c.fill_preserve()
        self._stroke(a, w, dash, color)

    def arc(self, cx, cy, r, a0, a1, a=0.5, w=0.6, dash=None, color=WHITE):
        self.c.new_sub_path()
        self.c.arc(cx, cy, r, math.radians(a0), math.radians(a1))
        self._stroke(a, w, dash, color)

    def band(self, cx, cy, r0, r1, a0, a1, a=0.5, w=0.6, fill=0.0, color=WHITE):
        """A ring segment between two radii and two angles."""
        self.c.new_sub_path()
        self.c.arc(cx, cy, r1, math.radians(a0), math.radians(a1))
        self.c.arc_negative(cx, cy, r0, math.radians(a1), math.radians(a0))
        self.c.close_path()
        if fill:
            self._ink(fill, color)
            self.c.fill_preserve()
        self._stroke(a, w, None, color)

    def ellipse(self, cx, cy, rx, ry, rot=0, a0=0, a1=360, a=0.5, w=0.6, dash=None, color=WHITE):
        self.c.save()
        self.c.translate(cx, cy)
        self.c.rotate(math.radians(rot))
        self.c.scale(rx, ry)
        self.c.new_sub_path()
        self.c.arc(0, 0, 1, math.radians(a0), math.radians(a1))
        self.c.restore()
        self._stroke(a, w, dash, color)

    def ticks(self, cx, cy, r, n, length, a=0.4, w=0.5, major=0, major_len=0, a0=0, a1=360, color=WHITE):
        """n radial ticks pointing outward from radius r, spread over a0..a1."""
        full = abs(a1 - a0) >= 360
        steps = n if full else n - 1
        for i in range(n):
            deg = a0 + (a1 - a0) * i / max(steps, 1)
            l = major_len if major and i % major == 0 else length
            x1, y1 = polar(cx, cy, r, deg)
            x2, y2 = polar(cx, cy, r + l, deg)
            self.c.move_to(x1, y1)
            self.c.line_to(x2, y2)
        self._stroke(a, w, None, color)

    def bez(self, p0, p1, p2, p3, a=0.5, w=0.6, dash=None, color=WHITE):
        self.c.move_to(*p0)
        self.c.curve_to(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
        self._stroke(a, w, dash, color)

    def fade_ln(self, x1, y1, x2, y2, a0=0.7, a1=0.0, w=0.6, color=WHITE):
        """A line whose opacity runs from a0 at the start to a1 at the end."""
        g = cairo.LinearGradient(x1, y1, x2, y2)
        g.add_color_stop_rgba(0, color[0], color[1], color[2], a0)
        g.add_color_stop_rgba(1, color[0], color[1], color[2], a1)
        self.c.move_to(x1, y1)
        self.c.line_to(x2, y2)
        self.c.set_source(g)
        self.c.set_line_width(w)
        self.c.stroke()

    def arrow(self, x1, y1, x2, y2, a=0.9, w=0.8, head=7, color=WHITE):
        self.ln(x1, y1, x2, y2, a, w, None, color)
        ang = math.atan2(y2 - y1, x2 - x1)
        pts = [(x2, y2)]
        for side in (-1, 1):
            pts.append((x2 - head * math.cos(ang + side * 0.35), y2 - head * math.sin(ang + side * 0.35)))
        self.poly(pts, a, 0.4, True, a, None, color)

    def chart(self, x, y, w_, h_, title, fn, xlabel, ylabel, color=ARC, n=80):
        """Small line chart. fn maps 0..1 to 0..1; (x, y) is the top-left corner."""
        self.ln(x, y, x, y + h_, 0.55, 0.6)
        self.ln(x, y + h_, x + w_, y + h_, 0.55, 0.6)
        for i in range(11):
            self.ln(x + w_ * i / 10, y + h_, x + w_ * i / 10, y + h_ + (5 if i % 5 == 0 else 3), 0.4, 0.45)
            self.ln(x - (5 if i % 5 == 0 else 3), y + h_ * i / 10, x, y + h_ * i / 10, 0.4, 0.45)
        for i in range(1, 5):
            self.ln(x, y + h_ * i / 5, x + w_, y + h_ * i / 5, 0.08, 0.4)
        pts = [(x + w_ * i / n, y + h_ * (1 - fn(i / n))) for i in range(n + 1)]
        self.poly(pts, 0.9, 1.0, close=False, color=color)
        self.text(title, x, y - 12, 7.5, a=0.8)
        self.text(xlabel, x + w_, y + h_ + 18, 6, a=0.4, align="r")
        self.text(ylabel, x - 10, y + h_, 6, a=0.4, rot=-90)

    def cross(self, x, y, size=4, a=0.4, w=0.5, color=WHITE):
        self.c.move_to(x - size, y)
        self.c.line_to(x + size, y)
        self.c.move_to(x, y - size)
        self.c.line_to(x, y + size)
        self._stroke(a, w, None, color)

    def diamond(self, x, y, r=5, a=0.9, w=0.7, fill=0.0, color=WHITE):
        self.poly([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], a, w, True, fill, None, color)

    def dot(self, x, y, r=1.6, a=0.9, color=WHITE):
        self.c.new_sub_path()
        self.c.arc(x, y, r, 0, 2 * math.pi)
        self._ink(a, color)
        self.c.fill()

    def hatch(self, path_fn, spacing=5, angle=45, a=0.22, w=0.45, color=WHITE):
        """Fill the path that path_fn() adds to the context with parallel lines."""
        self.c.save()
        path_fn()
        self.c.clip()
        x1, y1, x2, y2 = self.c.clip_extents()
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        reach = math.hypot(x2 - x1, y2 - y1) / 2 + spacing
        self.c.translate(mx, my)
        self.c.rotate(math.radians(angle))
        k = -reach
        while k <= reach:
            self.c.move_to(-reach, k)
            self.c.line_to(reach, k)
            k += spacing
        self._stroke(a, w, None, color)
        self.c.restore()

    # -- text ------------------------------------------------------------

    def _glyphs(self, s, size):
        """Split a string into (char, font size, baseline shift). Nimbus Sans has
        no glyphs for most Unicode sub- and superscripts, so they are drawn as
        small shifted digits instead."""
        out = []
        for ch in s:
            if ch in SUBS:
                out.append((SUBS[ch], size * 0.68, size * 0.22))
            elif ch in SUPS:
                out.append((SUPS[ch], size * 0.68, -size * 0.38))
            else:
                out.append((ch, size, 0.0))
        return out

    def _advances(self, glyphs, bold):
        c = self.c
        c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL,
                           cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        adv = []
        for ch, fs, _ in glyphs:
            c.set_font_size(fs)
            adv.append(c.text_extents(ch).x_advance)
        return adv

    def text(self, s, x, y, size=8, track=0.22, a=0.7, align="l", bold=False, color=WHITE, rot=0):
        """Label with letter spacing. Returns the text width."""
        c = self.c
        glyphs = self._glyphs(s, size)
        adv = self._advances(glyphs, bold)
        gap = track * size
        total = sum(adv) + gap * (len(glyphs) - 1)
        c.save()
        c.translate(x, y)
        c.rotate(math.radians(rot))
        px = {"l": 0, "c": -total / 2, "r": -total}[align]
        self._ink(a, color)
        for (ch, fs, dy), w_ in zip(glyphs, adv):
            c.set_font_size(fs)
            c.move_to(px, dy)
            c.show_text(ch)
            px += w_ + gap
        c.restore()
        return total

    def leader(self, x, y, dx, dy, run, label, sub=None, a=0.6, color=WHITE):
        """Dot on the part, a slanted line away from it, a horizontal run, a label."""
        self.dot(x, y, 1.8, 0.9, color)
        ex, ey = x + dx, y + dy
        self.c.move_to(x, y)
        self.c.line_to(ex, ey)
        self.c.line_to(ex + run, ey)
        self._stroke(a, 0.5, None, color)
        left = run < 0
        tx = ex + run if left else ex
        tx += 2 if not left else 0
        if left:
            self.text(label, ex - 2, ey - 5, 7.5, a=0.85, align="r")
            if sub:
                self.text(sub, ex - 2, ey + 11, 6.5, a=0.45, align="r")
        else:
            self.text(label, tx, ey - 5, 7.5, a=0.85)
            if sub:
                self.text(sub, tx, ey + 11, 6.5, a=0.45)

    def dim(self, x1, y1, x2, y2, label, off=0, a=0.45):
        """Dimension line between two points with end ticks and a centred label."""
        ang = math.atan2(y2 - y1, x2 - x1)
        nx, ny = -math.sin(ang), math.cos(ang)
        ax, ay, bx, by = x1 + nx * off, y1 + ny * off, x2 + nx * off, y2 + ny * off
        if off:
            self.ln(x1, y1, ax + nx * 4 * (1 if off > 0 else -1), ay + ny * 4 * (1 if off > 0 else -1), a * 0.6, 0.4)
            self.ln(x2, y2, bx + nx * 4 * (1 if off > 0 else -1), by + ny * 4 * (1 if off > 0 else -1), a * 0.6, 0.4)
        self.ln(ax, ay, bx, by, a, 0.45)
        for px, py in ((ax, ay), (bx, by)):
            self.ln(px - 3 * (math.cos(ang) + nx), py - 3 * (math.sin(ang) + ny),
                    px + 3 * (math.cos(ang) + nx), py + 3 * (math.sin(ang) + ny), a + 0.2, 0.6)
        mx, my = (ax + bx) / 2, (ay + by) / 2
        self.text(label, mx - nx * 5, my - ny * 5, 6.5, a=a + 0.2, align="c", rot=math.degrees(ang))

    def table(self, x, y, rows, key_w=92, size=7, lead=15, a=0.6):
        """Two-column list of KEY / value pairs."""
        for i, (k, v) in enumerate(rows):
            yy = y + i * lead
            self.text(k, x, yy, size, a=a * 0.65)
            self.text(v, x + key_w, yy, size, a=a + 0.2)
            self.ln(x, yy + 5, x + key_w + 120, yy + 5, 0.08, 0.4)

    def bars(self, x, y, width, height, a=0.5):
        """A strip of bars with random widths, like a machine-readable tag."""
        px = x
        while px < x + width:
            bw = self.rng.choice([1, 1, 2, 3, 5])
            if self.rng.random() < 0.6:
                self.c.rectangle(px, y, bw, height)
            px += bw + self.rng.choice([1, 2, 2, 4])
        self._ink(a, WHITE)
        self.c.fill()

    # -- sheet furniture -------------------------------------------------

    def set_palette(self, name):
        """Pick the background tint and the two accent colours for this sheet."""
        hue, sat, light, accent, second = PALETTES[name]
        self.bg = (hue / 360.0, sat, light)
        ARC[:] = accent
        GOLD[:] = second

    def background(self):
        c = self.c
        h, sat, l = self.bg

        def tone(k_l, k_s=1.0):
            return colorsys.hls_to_rgb(h, l * k_l, min(1.0, sat * k_s))
        g = cairo.LinearGradient(0, 0, 0, self.H)
        g.add_color_stop_rgb(0.0, *tone(0.82))
        g.add_color_stop_rgb(0.5, *tone(1.0))
        g.add_color_stop_rgb(1.0, *tone(0.56, 0.9))
        c.set_source(g)
        c.paint()
        gr, gg, gb = colorsys.hls_to_rgb(h, 0.53, min(1.0, sat * 1.1))
        glow = cairo.RadialGradient(self.cx, self.cy * 0.92, 0, self.cx, self.cy * 0.92, self.W * 0.42)
        glow.add_color_stop_rgba(0.0, gr, gg, gb, 0.20)
        glow.add_color_stop_rgba(1.0, gr, gg, gb, 0.0)
        c.set_source(glow)
        c.paint()
        vr, vg, vb = colorsys.hls_to_rgb(h, 0.045, sat)
        vig = cairo.RadialGradient(self.cx, self.cy, self.H * 0.55, self.cx, self.cy, self.W * 0.62)
        vig.add_color_stop_rgba(0.0, vr, vg, vb, 0.0)
        vig.add_color_stop_rgba(1.0, vr, vg, vb, 0.55)
        c.set_source(vig)
        c.paint()

    def grid(self, step=40, major=4, a=0.10):
        """Dots on every grid point, small crosses on every major one."""
        ox = self.cx % step
        oy = self.cy % step
        nx = int(self.W // step) + 2
        ny = int(self.H // step) + 2
        ix0 = round((self.cx - ox) / step)
        iy0 = round((self.cy - oy) / step)
        for i in range(nx):
            for j in range(ny):
                x, y = ox + i * step, oy + j * step
                if (i - ix0) % major == 0 and (j - iy0) % major == 0:
                    self.cross(x, y, 3.5, a * 2.2, 0.5)
                else:
                    self.c.rectangle(x - 0.4, y - 0.4, 0.8, 0.8)
        self._ink(a * 1.6, WHITE)
        self.c.fill()

    def frame(self, sheet_no, total=6, code="NCR"):
        """Corner brackets, a ruler along the bottom edge and the sheet number."""
        m, L = 44, 26
        W, H = self.W, self.H
        for x, y, sx, sy in ((m, m + 8, 1, 1), (W - m, m + 8, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
            self.poly([(x + sx * L, y), (x, y), (x, y + sy * L)], 0.55, 0.8, close=False)
        # ruler
        y = H - m
        x0, x1 = m + 60, W - m - 60
        self.ln(x0, y, x1, y, 0.18, 0.5)
        n = int((x1 - x0) // 10)
        for i in range(n + 1):
            x = x0 + i * 10
            l = 7 if i % 10 == 0 else (4.5 if i % 5 == 0 else 2.5)
            self.ln(x, y, x, y - l, 0.32 if i % 10 == 0 else 0.2, 0.45)
            if i % 20 == 0 and i:
                self.text(f"{i * 10:04d}", x + 3, y - 9, 5.5, a=0.3)
        # side registration marks
        for yy in (H * 0.25, H * 0.5, H * 0.75):
            self.ln(m - 14, yy, m - 4, yy, 0.4, 0.6)
            self.ln(W - m + 4, yy, W - m + 14, yy, 0.4, 0.6)
        right = W - m - 4 - self.inset
        self.text(f"{code}-{sheet_no:02d}", right, m + 22, 7, a=0.55, align="r")
        self.text(f"SHEET {sheet_no:02d} / {total:02d}", right, m + 36, 6.5, a=0.35, align="r")
        self.bars(right - 120, m + 46, 120, 7, 0.35)

    def title_block(self, x, y, title, subtitle, lines=()):
        self.diamond(x + 5, y - 30, 5, 0.9, 0.8, fill=0.9)
        self.ln(x + 18, y - 30, x + 330, y - 30, 0.35, 0.5)
        self.text(title, x, y, 25, track=0.30, a=0.95, bold=True)
        self.text(subtitle, x, y + 22, 8.5, track=0.34, a=0.6)
        for i, l in enumerate(lines):
            self.text(l, x, y + 44 + i * 13, 6.5, a=0.38)

    def text_mid(self, s, x, y_mid, size=8, track=0.22, a=0.7, align="l", bold=False, color=WHITE):
        """Like text(), but y_mid is where the middle of the capital letters goes.

        A single centred character is also centred on its inked shape rather
        than on its advance width, which includes uneven side bearings.
        """
        c = self.c
        c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL,
                           cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(size)
        cap = -c.text_extents("H").y_bearing
        if len(s) == 1 and align == "c":
            e = c.text_extents(s)
            self._ink(a, color)
            c.move_to(x - (e.x_bearing + e.width / 2), y_mid + cap / 2)
            c.show_text(s)
            return e.width
        return self.text(s, x, y_mid + cap / 2, size, track, a, align, bold, color)

    def view_label(self, x, y, letter, name, scale=None, align="c"):
        """Caption under a view: a boxed letter, the view name, the scale."""
        w = self.measure(name, 8, 0.30)
        total = 16 + 8 + w
        x0 = x - total / 2 if align == "c" else x
        mid = y - 3
        self.rect(x0, mid - 8, 16, 16, 0.7, 0.6)
        self.text_mid(letter, x0 + 8, mid, 9, track=0, a=0.9, align="c", bold=True)
        self.text_mid(name, x0 + 24, mid, 8, track=0.30, a=0.75)
        if scale:
            self.text(scale, x0 + 24, y + 14, 6.5, a=0.4)

    def measure(self, s, size=8, track=0.22, bold=False):
        glyphs = self._glyphs(s, size)
        return sum(self._advances(glyphs, bold)) + track * size * (len(glyphs) - 1)

    def wrap(self, s, width, size, track):
        lines, cur = [], ""
        for word in s.split():
            trial = (cur + " " + word).strip()
            if cur and self.measure(trial, size, track) > width:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines

    def begin_main(self, x, y):
        """Start the main drawing, designed around (x, y).

        On a wide sheet nothing changes. On a 16:9 or narrower sheet the drawing
        is scaled down to fit between the legend and the emblem.
        """
        self.c.save()
        if not self.wide:
            # Small enough, and far enough right, that the drawing and its
            # labels clear the legend; high enough to clear the emblem.
            k = 0.72
            legend_right = 44 + 48 + self.inset + 530
            self.c.translate(legend_right + 570 * k, self.H * 0.44)
            self.c.scale(k, k)
            self.c.translate(-x, -y)

    def end_main(self):
        self.c.restore()

    def begin_clip_circle(self, x, y, r):
        self.c.save()
        self.c.new_sub_path()
        self.c.arc(x, y, r, 0, 2 * math.pi)
        self.c.clip()

    def end_clip(self):
        self.c.restore()

    def detail_ring(self, x, y, r):
        self.circ(x, y, r, 0.8, 0.9)
        self.ticks(x, y, r, 72, 4, 0.35, 0.45, major=6, major_len=8)

    def emblem(self, x, y, t=0.0, r=140):
        """The Omarchy wordmark inside a set of segmented rings.

        t is the phase of the loop, 0..1. Every ring turns a whole number of
        times per loop, so frame t=1 equals frame t=0 and a video can repeat.
        """
        k = r / 140.0
        turn = 360.0 * t
        self.circ(x, y, 140 * k, 0.12, 0.5)
        for i in range(4):
            px, py = polar(x, y, 140 * k, 45 + 90 * i)
            self.diamond(px, py, 3.2 * k, 0.9, 0.6, fill=0.9)
        for i in range(2):
            a0 = turn * 2 + 180 * i + 20
            self.arc(x, y, 130 * k, a0, a0 + 56, 0.45, 0.7)
        for i in range(8):
            a0 = -turn + 45 * i
            self.band(x, y, 113 * k, 120 * k, a0, a0 + 34, 0.7, 0.6, fill=0.55 if i % 2 == 0 else 0.0)
        self.circ(x, y, 105 * k, 0.3, 0.5, dash=[2, 4])
        a0 = turn - 90
        self.arc(x, y, 99 * k, a0, a0 + 78, 0.95, 1.6, color=ARC)
        self.dot(*polar(x, y, 99 * k, a0 + 78), 2.2 * k, 0.95, ARC)
        self.c.save()
        self.c.translate(x, y)
        self.c.rotate(math.radians(-turn / 2 if t else 0))
        self.ticks(0, 0, 90 * k, 72, 3.5 * k, 0.4, 0.45, major=6, major_len=7 * k)
        self.c.restore()
        for i in range(3):
            a0 = turn + 120 * i
            self.arc(x, y, 82 * k, a0, a0 + 96, 0.9, 2.2)
        self.circ(x, y, 75 * k, 0.35, 0.5)
        # wordmark
        lw, lh, subpaths = load_logo()
        width = 118 * k
        f = width / lw
        ox, oy = x - width / 2, y - lh * f / 2
        self.c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        for sp in subpaths:
            self.c.move_to(ox + sp[0][0] * f, oy + sp[0][1] * f)
            for px, py in sp[1:]:
                self.c.line_to(ox + px * f, oy + py * f)
            self.c.close_path()
        self._ink(0.95, WHITE)
        self.c.fill()
        self.c.set_fill_rule(cairo.FILL_RULE_WINDING)
        for sgn in (-1, 1):
            self.ln(x + sgn * 66 * k, y, x + sgn * 72 * k, y, 0.6, 0.6)

    def legend(self, title, subtitle, function, enabled_by, service, t=0.0):
        """Bottom-left block: what the device is, what it does, what made it possible.

        enabled_by is a list of (discipline, sentence). The emblem goes in the bottom-right corner.
        """
        m = 44
        ex, ey = self.W - m - 152 - self.inset, self.H - m - 190
        width, col = 530, 160
        x0 = m + 48 + self.inset
        ops = []  # (dy, fn)
        y = 0.0
        ops.append((y, lambda yy: (self.diamond(x0 + 5, yy, 5, 0.9, 0.8, fill=0.9),
                                   self.ln(x0 + 18, yy, x0 + width, yy, 0.35, 0.5))))
        y += 31
        ops.append((y, lambda yy: self.text(title, x0, yy, 23, track=0.28, a=0.95, bold=True)))
        y += 20
        ops.append((y, lambda yy: self.text(subtitle, x0, yy, 8, track=0.32, a=0.6)))
        y += 26
        ops.append((y, lambda yy: self.text("FUNCTION", x0, yy, 6.5, a=0.5)))
        for i, line in enumerate(self.wrap(function, width - col, 9, 0.04)):
            ops.append((y + i * 14, lambda yy, line=line: self.text(line, x0 + col, yy, 9, track=0.04, a=0.9)))
        y += 14 * max(1, len(self.wrap(function, width - col, 9, 0.04))) + 10
        ops.append((y - 12, lambda yy: self.ln(x0, yy, x0 + width, yy, 0.12, 0.4)))
        ops.append((y + 2, lambda yy: self.text("ENABLED BY", x0, yy, 6.5, a=0.5)))
        y += 18
        for n, (tag, sentence) in enumerate(enabled_by, 1):
            ops.append((y, lambda yy, n=n, tag=tag: (self.text(f"{n:02d}", x0, yy, 6.5, a=0.9, color=ARC),
                                                   self.text(tag, x0 + 20, yy, 6.5, a=0.9, color=ARC))))
            lines = self.wrap(sentence, width - col, 8.5, 0.04)
            for i, line in enumerate(lines):
                ops.append((y + i * 13, lambda yy, line=line: self.text(line, x0 + col, yy, 8.5, track=0.04, a=0.75)))
            y += 13 * len(lines) + 7
        y += 4
        ops.append((y - 11, lambda yy: self.ln(x0, yy, x0 + width, yy, 0.12, 0.4)))
        ops.append((y + 3, lambda yy: (self.text("PROJECTED FIRST SERVICE", x0, yy, 6.5, a=0.5),
                                       self.text(service, x0 + col, yy, 8, track=0.3, a=0.9, bold=True))))
        top = self.H - m - 46 - (y + 3)
        for dy, fn in ops:
            fn(top + dy)
        self.emblem(ex, ey, t)

    # -- output ----------------------------------------------------------

    def save(self, path, glow=0.55, grain=2.2, quality=93):
        """Add a soft bloom around the lines and a fine grain, then write the file.

        The grain also hides the banding an 8-bit dark gradient would show.
        """
        w, h = self.px
        self.surface.flush()
        buf = np.frombuffer(self.surface.get_data(), np.uint8).reshape(h, w, 4)
        rgb = buf[:, :, [2, 1, 0]].astype(np.float32)
        img = self._final(rgb, glow, grain)
        Image.fromarray(img, "RGB").save(path, quality=quality, method=6)

    def _final(self, rgb, glow, grain):
        rng = np.random.default_rng(7)
        if glow and self._lines is not None:
            rgb = rgb + self._lines * glow
        rgb += rng.normal(0.0, grain, rgb.shape[:2])[:, :, None]
        return np.clip(rgb + 0.5, 0, 255).astype(np.uint8)

    _lines = None

    def begin_lines(self):
        """Call after the background: remember it so the bloom uses only what is drawn later."""
        self.surface.flush()
        w, h = self.px
        self._bg = np.frombuffer(self.surface.get_data(), np.uint8).reshape(h, w, 4).copy()

    def end_lines(self, radius=5.0):
        self.surface.flush()
        w, h = self.px
        now = np.frombuffer(self.surface.get_data(), np.uint8).reshape(h, w, 4)
        diff = np.clip(now[:, :, [2, 1, 0]].astype(np.int16) - self._bg[:, :, [2, 1, 0]].astype(np.int16), 0, 255)
        im = Image.fromarray(diff.astype(np.uint8), "RGB").filter(ImageFilter.GaussianBlur(radius * self.s))
        self._lines = np.asarray(im, dtype=np.float32)
