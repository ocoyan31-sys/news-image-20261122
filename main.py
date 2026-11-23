#!/usr/bin/env python3
"""news-image-20261122: draw the front page of Sunday 22 November 2026.

Python 3.13, standard library only. Fully deterministic: no randomness,
no timestamps, no network, no image files. Writes entry.png to
$MAKEFUN_OUTPUT_DIR or /output. Two runs write identical bytes.
"""

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (255, 255, 255)
INK = (18, 18, 18)
RED = (178, 30, 30)
GREY = (110, 110, 110)
PALE = (240, 240, 240)
DARK = (60, 60, 60)

# 5x7 bitmap font. One glyph per line: seven rows of five bits, joined.
# Row 0 is the top row. Only ASCII the page needs is defined here.
FONT = {
    "A": "01110" "10001" "10001" "11111" "10001" "10001" "10001",
    "B": "11110" "10001" "10001" "11110" "10001" "10001" "11110",
    "C": "01110" "10001" "10000" "10000" "10000" "10001" "01110",
    "D": "11110" "10001" "10001" "10001" "10001" "10001" "11110",
    "E": "11111" "10000" "10000" "11110" "10000" "10000" "11111",
    "F": "11111" "10000" "10000" "11110" "10000" "10000" "10000",
    "G": "01110" "10001" "10000" "10111" "10001" "10001" "01111",
    "H": "10001" "10001" "10001" "11111" "10001" "10001" "10001",
    "I": "01110" "00100" "00100" "00100" "00100" "00100" "01110",
    "J": "00111" "00010" "00010" "00010" "00010" "10010" "01100",
    "K": "10001" "10010" "10100" "11000" "10100" "10010" "10001",
    "L": "10000" "10000" "10000" "10000" "10000" "10000" "11111",
    "M": "10001" "11011" "10101" "10101" "10001" "10001" "10001",
    "N": "10001" "11001" "10101" "10011" "10001" "10001" "10001",
    "O": "01110" "10001" "10001" "10001" "10001" "10001" "01110",
    "P": "11110" "10001" "10001" "11110" "10000" "10000" "10000",
    "Q": "01110" "10001" "10001" "10001" "10101" "10010" "01101",
    "R": "11110" "10001" "10001" "11110" "10100" "10010" "10001",
    "S": "01111" "10000" "10000" "01110" "00001" "00001" "11110",
    "T": "11111" "00100" "00100" "00100" "00100" "00100" "00100",
    "U": "10001" "10001" "10001" "10001" "10001" "10001" "01110",
    "V": "10001" "10001" "10001" "10001" "10001" "01010" "00100",
    "W": "10001" "10001" "10001" "10101" "10101" "11011" "10001",
    "X": "10001" "10001" "01010" "00100" "01010" "10001" "10001",
    "Y": "10001" "10001" "01010" "00100" "00100" "00100" "00100",
    "Z": "11111" "00001" "00010" "00100" "01000" "10000" "11111",
    "0": "01110" "10001" "10011" "10101" "11001" "10001" "01110",
    "1": "00100" "01100" "00100" "00100" "00100" "00100" "01110",
    "2": "01110" "10001" "00001" "00010" "00100" "01000" "11111",
    "3": "11111" "00010" "00100" "00010" "00001" "10001" "01110",
    "4": "00010" "00110" "01010" "10010" "11111" "00010" "00010",
    "5": "11111" "10000" "11110" "00001" "00001" "10001" "01110",
    "6": "00110" "01000" "10000" "11110" "10001" "10001" "01110",
    "7": "11111" "00001" "00010" "00100" "01000" "01000" "01000",
    "8": "01110" "10001" "10001" "01110" "10001" "10001" "01110",
    "9": "01110" "10001" "10001" "01111" "00001" "00010" "01100",
    " ": "00000" "00000" "00000" "00000" "00000" "00000" "00000",
    ".": "00000" "00000" "00000" "00000" "00000" "01100" "01100",
    ",": "00000" "00000" "00000" "00000" "01100" "00100" "01000",
    "-": "00000" "00000" "00000" "11111" "00000" "00000" "00000",
    "'": "00100" "00100" "01000" "00000" "00000" "00000" "00000",
    "!": "00100" "00100" "00100" "00100" "00100" "00000" "00100",
    "?": "01110" "10001" "00001" "00010" "00100" "00000" "00100",
    ":": "00000" "01100" "01100" "00000" "01100" "01100" "00000",
    ";": "00000" "01100" "01100" "00000" "01100" "00100" "01000",
    "(": "00010" "00100" "01000" "01000" "01000" "00100" "00010",
    ")": "01000" "00100" "00010" "00010" "00010" "00100" "01000",
    "/": "00001" "00001" "00010" "00100" "01000" "10000" "10000",
    "%": "11001" "11010" "00010" "00100" "01000" "01011" "10011",
    "$": "00100" "01111" "10100" "01110" "00101" "11110" "00100",
    "&": "01100" "10010" "10100" "01000" "10101" "10010" "01101",
    "+": "00000" "00100" "00100" "11111" "00100" "00100" "00000",
    "=": "00000" "00000" "11111" "00000" "11111" "00000" "00000",
    '"': "01010" "01010" "00000" "00000" "00000" "00000" "00000",
    "<": "00010" "00100" "01000" "10000" "01000" "00100" "00010",
    ">": "01000" "00100" "00010" "00001" "00010" "00100" "01000",
    "*": "00000" "00100" "10101" "01110" "10101" "00100" "00000",
}

CHAR_W, CHAR_H = 5, 7


class Page:
    """An RGB page backed by one flat bytearray."""

    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.paint(0, 0, w, h, bg)

    def dot(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = colour

    def paint(self, x, y, w, h, colour):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.dot(xx, yy, colour)

    def rule(self, x, y, w, thick, colour):
        self.paint(x, y, w, thick, colour)

    def frame(self, x, y, w, h, thick, colour):
        self.rule(x, y, w, thick, colour)
        self.rule(x, y + h - thick, w, thick, colour)
        self.rule(x, y, thick, h, colour)
        self.rule(x + w - thick, y, thick, h, colour)

    def ring(self, cx, cy, r, colour):
        for a in range(360):
            import math
            rad = a * math.pi / 180.0
            self.dot(int(cx + r * math.cos(rad)), int(cy + r * math.sin(rad)), colour)

    def glyph(self, x, y, ch, scale, colour):
        bits = FONT.get(ch, FONT[" "])
        for row in range(CHAR_H):
            for col in range(CHAR_W):
                if bits[row * CHAR_W + col] == "1":
                    self.paint(x + col * scale, y + row * scale, scale, scale, colour)

    def text(self, x, y, s, scale, colour):
        cx = x
        for ch in s:
            self.glyph(cx, y, ch, scale, colour)
            cx += (CHAR_W + 1) * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * (CHAR_W + 1) * scale - scale

    def centred(self, y, s, scale, colour, x0=0, x1=None):
        if x1 is None:
            x1 = self.w
        w = self.text_w(s, scale)
        self.text(x0 + (x1 - x0 - w) // 2, y, s, scale, colour)

    def wrap(self, s, scale, max_w):
        """Greedy word wrap into lines fitting max_w pixels."""
        words, lines, cur = s.split(" "), [], ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if self.text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, scale, max_w, colour, gap=6):
        yy = y
        for line in self.wrap(s, scale, max_w):
            self.text(x, yy, line, scale, colour)
            yy += CHAR_H * scale + gap
        return yy


def story(page, x, y, w, kicker, head, body, head_scale=3):
    """One column story: red kicker, bold headline, body paragraph."""
    page.text(x, y, kicker, 2, RED)
    y += 18
    for line in page.wrap(head, head_scale, w):
        page.text(x, y, line, head_scale, INK)
        y += CHAR_H * head_scale + 4
    y += 2
    y = page.para(x, y, body, 2, w, DARK, gap=4)
    return y + 6


def strip_box(page, x, y, w, h, label, body):
    page.frame(x, y, w, h, 2, INK)
    page.paint(x + 2, y + 2, w - 4, 26, PALE)
    page.text(x + 10, y + 8, label, 2, RED)
    page.para(x + 10, y + 36, body, 2, w - 20, INK, gap=5)


def draw():
    p = Page(W, H, PAPER)
    p.frame(10, 10, W - 20, H - 20, 4, INK)
    p.frame(20, 20, W - 40, H - 40, 1, GREY)

    # Masthead.
    p.centred(44, "THE WORLD TODAY", 6, INK)
    p.rule(60, 104, W - 120, 4, RED)
    p.centred(118, "SUNDAY, 22 NOVEMBER 2026", 3, RED)
    p.rule(60, 152, W - 120, 2, INK)

    # Lead kicker and headline.
    p.centred(170, "CLIMATE SUMMIT ENDS WITHOUT A DEAL", 2, RED)
    p.centred(196, "COP31 COLLAPSES", 7, INK)
    p.centred(258, "NO AGREEMENT IN ANTALYA", 4, INK)
    p.para(60, 306,
           "THE CLIMATE SUMMIT ENDED ON SUNDAY WITH NO DEAL, TWO DAYS AFTER IT "
           "WAS DUE TO CLOSE, AFTER THE EU AND VULNERABLE COUNTRIES OBJECTED TO "
           "A FINAL TEXT THAT MADE NO MENTION OF FOSSIL FUELS.", 2, W - 120, INK)
    p.rule(60, 392, W - 120, 2, INK)

    # Two middle columns.
    lx, rx, col_w = 60, 532, 432
    y = 412
    y = story(p, lx, y, col_w, "BAHRAIN / HORMUZ",
              "IRAN STRIKES US BASES",
              "MISSILES AND DRONES HIT US BASES IN BAHRAIN. TWO PEOPLE WERE "
              "INJURED AND OIL TANKERS WERE STRUCK NEAR HORMUZ.")
    y = story(p, lx, y, col_w, "LIBYA / BALTIC",
              "RUSSIAN SHIPS HIT",
              "A SUSPECTED UKRAINIAN DRONE HIT A RUSSIAN WARSHIP AT BENGHAZI, "
              "INJURING TEN PORT WORKERS. A SECOND SHIP BURNED IN THE BALTIC.")
    y = story(p, lx, y, col_w, "UKRAINE",
              "FLATS HIT NEAR KYIV",
              "A RUSSIAN STRIKE PARTLY COLLAPSED A FLAT BLOCK IN DYMER, NEAR "
              "KYIV. RESCUERS SEARCHED THE RUINS.")
    y = 412
    y = story(p, rx, y, col_w, "MEXICO",
              "CARTEL BOSS CAPTURED",
              "SPECIAL FORCES SEIZED FAUSTO ISIDRO MEZA FLORES, EL CHAPO "
              "ISIDRO, IN SINALOA. ELEVEN DIED IN THE RAID, FOUR OF THEM "
              "SOLDIERS.")
    y = story(p, rx, y, col_w, "INDONESIA",
              "FACTORY FIRE KILLS 3",
              "A FIRE AT A CANDY FACTORY IN CIKANDE, BANTEN KILLED THREE "
              "WORKERS. DOZENS ARE STILL MISSING.")
    y = story(p, rx, y, col_w, "WASHINGTON",
              "DEMOCRATS TAKE HOUSE",
              "DEMOCRATS WON AT LEAST 258 HOUSE SEATS, THEIR LARGEST "
              "MAJORITY SINCE 1992.")
    p.rule(60, 772, W - 120, 2, INK)

    # Bottom strip: four boxes.
    bw, bh, gap = 216, 178, 8
    bx = 60
    strip_box(p, bx, 790, bw, bh, "MARKETS",
              "STOCKS FELL AS THE AI SELL-OFF DEEPENED: S&P 500 -3.7%, "
              "NIKKEI -5.06%, FTSE -1.02%. BRENT $89.95.")
    bx += bw + gap
    strip_box(p, bx, 790, bw, bh, "MERCURY",
              "BEPICOLOMBO, THE EUROPEAN-JAPANESE PROBE, ENTERED ORBIT "
              "AROUND MERCURY.")
    bx += bw + gap
    strip_box(p, bx, 790, bw, bh, "WEST BANK",
              "ISRAELI SETTLERS TORCHED VEHICLES AND HOMES NEAR RAMALLAH. "
              "ISRAEL OPENED AN INQUIRY.")
    bx += bw + gap
    strip_box(p, bx, 790, bw, bh, "SHENZHEN FALLOUT",
              "FALLOUT FROM THE TRUMP-XI-PUTIN SUMMIT CONTINUED AS THE US "
              "INTELLIGENCE CHIEF BACKED TRUMP ON PUTIN.")
    return p


def write_png(page, path):
    raw = bytearray()
    for yy in range(page.h):
        raw.append(0)
        raw.extend(page.px[yy * page.w * 3:(yy + 1) * page.w * 3])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", page.w, page.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    page = draw()
    write_png(page, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
