#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026 as a single 1024x1024 PNG.

Deterministic: fixed layout, fixed text, fixed palette. No network, no clock,
no randomness. Run twice and the bytes are identical.
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 248, 243)
NAVY = (16, 35, 63)
NAVY2 = (24, 52, 88)
INK = (22, 22, 22)
RED = (192, 57, 43)
DARKRED = (150, 40, 30)
GRAY = (96, 96, 96)
RULE = (198, 192, 182)
LIGHT = (238, 234, 226)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_I = lambda s: font("DejaVuSans.ttf", s)  # no oblique on this box; regular is fine


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, text, fnt, x, y, width, fill, leading=6):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def kicker(draw, text, x, y, color=RED):
    f = SANS_B(17)
    draw.text((x, y), text, font=f, fill=color)
    return y + 24


def rule(draw, x0, y, x1, w=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=w)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((28, 16), "THE WORLD", font=SERIF_B(58), fill=(255, 255, 255))
    date_f = SANS_B(27)
    date = "SATURDAY, 21 NOVEMBER 2026"
    d.text((W - 28 - date_f.getlength(date), 20), date, font=date_f, fill=(255, 255, 255))
    sub_f = SANS(15)
    sub = "ONE DAY  ·  ONE PAGE"
    d.text((W - 28 - sub_f.getlength(sub), 58), sub, font=sub_f, fill=(200, 210, 225))
    d.rectangle([0, 96, W, 102], fill=RED)

    # ---- Lead story: Poland ----
    y = 122
    y = kicker(d, "POLAND  ·  NATO", 28, y)
    hl = SERIF_B(46)
    y = para(d, "Russian missiles land in Poland", hl, 28, y, 580, INK, leading=4)
    y += 6
    y = para(d, "Warsaw calls it a deliberate provocation as NATO condemns a "
             "'grave violation' of allied airspace.", SANS(21), 28, y, 580, INK)
    y += 4
    y = para(d, "Two missiles and a suspected drone came down on Polish soil "
             "while allies held exercises nearby. Russia also pounded Kyiv's "
             "bridges in a huge aerial assault; nine people were killed.",
             SANS(18), 28, y, 580, (60, 60, 60))

    # Lead graphic panel: arcs over a dark sky, burst, Polish flag
    px0, py0, px1, py1 = 640, 122, 996, 330
    d.rectangle([px0, py0, px1, py1], fill=NAVY2)
    d.rectangle([px0, py0, px1, py0 + 3], fill=RED)
    # ground line
    d.line([(px0 + 14, py1 - 34), (px1 - 14, py1 - 34)], fill=(120, 140, 170), width=2)
    # trajectory arcs
    for i, (bx0, by0, bx1, by1, col) in enumerate([
            (655, 310, 880, 150, (230, 80, 60)),
            (690, 310, 940, 165, (240, 120, 70)),
            (730, 310, 975, 195, (200, 60, 50))]):
        d.arc([bx0, by0 - 120, bx1, by1 + 60], start=200, end=340, fill=col, width=5)
    # burst
    cx, cy = 905, 175
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 10, 30 if ang % 60 == 0 else 20
        a = math.radians(ang)
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=(255, 200, 80), width=3)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 220, 120))
    # Polish flag
    d.rectangle([px0 + 16, py1 - 34, px0 + 66, py1 - 22], fill=(255, 255, 255))
    d.rectangle([px0 + 16, py1 - 22, px0 + 66, py1 - 10], fill=(220, 40, 50))
    d.text((px0 + 76, py1 - 34), "POLAND", font=SANS_B(14), fill=(255, 255, 255))
    d.text((px0 + 76, py1 - 16), "NATO airspace", font=SANS(13), fill=(190, 200, 215))
    d.text((640, 340), "Missiles cross into NATO airspace.",
           font=SANS_I(14), fill=GRAY)

    # ---- Row 2: summit + markets ----
    rule(d, 28, 470, 996)
    # Summit, left column
    y = 490
    y = kicker(d, "SHENZHEN  ·  SUMMIT", 28, y)
    y = para(d, "Trump, Xi and Putin meet — and leave with little agreed",
             SERIF_B(30), 28, y, 452, INK, leading=4)
    y += 4
    para(d, "The first trilateral summit of the US, Russian and Chinese "
         "leaders, on the sidelines of APEC, ends with few concrete results.",
         SANS(18), 28, y, 452, (60, 60, 60))
    d.line([(500, 490), (500, 700)], fill=RULE, width=2)
    # Markets, right column
    y = 490
    y = kicker(d, "NEW YORK  ·  MARKETS", 524, y)
    y = para(d, "S&P 500 slides into correction as AI stocks plunge",
             SERIF_B(28), 524, y, 472, INK, leading=4)
    y += 4
    y = para(d, "Wall Street falls about 3.7% as AI shares sell off.",
             SANS(18), 524, y, 472, (60, 60, 60))
    # mini chart, fixed box
    cx0, cy0, cx1, cy1 = 524, 645, 996, 712
    d.rectangle([cx0, cy0, cx1, cy1], outline=RULE, width=2)
    n = 9
    pts = []
    for i in range(n):
        x = cx0 + 12 + i * (cx1 - cx0 - 24) / (n - 1)
        yy = cy0 + 22 + ((i / (n - 1)) ** 2) * 42
        pts.append((x, yy))
    d.polygon(pts + [(pts[-1][0], cy1 - 3), (pts[0][0], cy1 - 3)], fill=(232, 190, 185))
    d.line(pts, fill=RED, width=4, joint="curve")
    d.text((cx0 + 10, cy0 + 5), "S&P 500 — DOWN INTO CORRECTION",
           font=SANS_B(13), fill=DARKRED)

    # ---- Row 3: three columns ----
    rule(d, 28, 722, 996)
    cols = [
        ("NEW YORK  ·  JUSTICE",
         "19\u00bd years for plot to kill Sikh separatist leader",
         "Nikhil Gupta is sentenced in a US court over a murder-for-hire "
         "plot on American soil."),
        ("BRUSSELS  ·  EUROPE",
         "UK and EU sign deals on food, carbon and youth mobility",
         "Three agreements at a Brussels summit, five years after Brexit."),
        ("SCIENCE",
         "Claude 'proves' Riemann Hypothesis, researcher says",
         "An Anthropic mathematician says the chatbot solved maths' "
         "greatest riddle."),
    ]
    cw = 304
    for i, (kick, head, body) in enumerate(cols):
        x = 28 + i * (cw + 16)
        y = 742
        y = kicker(d, kick, x, y)
        y = para(d, head, SERIF_B(24), x, y, cw, INK, leading=3)
        y += 4
        para(d, body, SANS(17), x, y, cw, (60, 60, 60))
        if i < 2:
            d.line([(x + cw + 8, 742), (x + cw + 8, 912)], fill=RULE, width=2)

    # ---- Bottom ticker ----
    d.rectangle([0, 930, W, 986], fill=NAVY)
    tick = ("ALSO:  Kyiv bridges hit, nine dead   ·   Denmark accuses Russian "
            "agents of a plot   ·   COP31 talks deadlocked   ·   Arson in Bangladesh")
    tf = SANS_B(13)
    tw = tf.getlength(tick)
    d.text(((W - tw) / 2, 952), tick, font=tf, fill=(255, 255, 255))
    d.text((28, 996), "Drawn from wire reports  ·  Saturday 21 November 2026",
           font=SANS(13), fill=GRAY)
    d.text((W - 28 - SANS(13).getlength("make.fun  ·  news-image-20261121"), 996),
           "make.fun  ·  news-image-20261121", font=SANS(13), fill=GRAY)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = draw_page()
    img.save(out, format="PNG")
    data = open(out, "rb").read()
    print(f"{out}: {img.size[0]}x{img.size[1]} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()[:16]}")


if __name__ == "__main__":
    main()
