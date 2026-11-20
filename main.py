#!/usr/bin/env python3
"""The World in One Day - Friday 20 November 2026.

Renders a 1024x1024 front page of a fictional world-news daily that sums up
45 stories from Friday 20 November 2026: three hero stories, ten feature
cards, a world map with numbered pins, and a numbered day-in-brief list.

Pure Python 3 standard library plus Pillow. The output is deterministic:
running the program twice produces byte-identical PNG files.

Usage:
    python3 main.py
    MAKEFUN_OUTPUT_DIR=. python3 main.py   # writes ./entry.png
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN

PAPER = (248, 242, 228)
NAVY = (27, 58, 92)
NAVY_DARK = (16, 32, 56)
INK = (32, 30, 28)
RED = (198, 38, 30)
RED_DARK = (178, 28, 24)
MUTED = (96, 90, 78)
SEA = (207, 226, 234)
GRID = (232, 240, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def star_points(cx, cy, r_outer, r_inner, spikes=8, rot=-90):
    import math

    pts = []
    for i in range(spikes * 2):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.radians(rot + i * 180.0 / spikes)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


# ---------------------------------------------------------------- heroes ---

def hero_art_gta(draw, x, y, w, h):
    """Sunset city skyline with a neon sign, two figures and a red car."""
    draw.rectangle([x, y, x + w, y + 52], fill=(246, 138, 62))
    draw.rectangle([x, y + 52, x + w, y + 102], fill=(232, 96, 122))
    draw.rectangle([x, y + 102, x + w, y + h], fill=(107, 74, 140))
    # Low sun with a warm halo.
    draw.ellipse([x + 118, y + 8, x + 200, y + 90], fill=(255, 158, 79))
    draw.ellipse([x + 128, y + 18, x + 190, y + 80], fill=(255, 210, 122))
    # Building silhouettes with lit windows.
    buildings = [(0, 78, 42), (44, 62, 38), (84, 84, 46), (132, 58, 42),
                 (176, 80, 40), (218, 64, 44), (264, 86, 34), (300, 72, 18)]
    for bx, top, bw in buildings:
        draw.rectangle([x + bx, y + top, x + bx + bw, y + h], fill=(34, 26, 56))
        for row in range(4):
            for col in range(max(1, bw // 11)):
                if (row + col) % 3 == 0:
                    continue
                wx = x + bx + 5 + col * 11
                wy = y + top + 8 + row * 12
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 215, 106))
    # Neon sign on the middle tower.
    draw.rectangle([x + 136, y + 66, x + 170, y + 94], fill=(194, 24, 91))
    draw.rectangle([x + 138, y + 68, x + 168, y + 92], outline=(255, 120, 180), width=1)
    centered(draw, x + 153, y + 71, "VICE", SANS_B(9), (255, 255, 255))
    centered(draw, x + 153, y + 81, "CITY", SANS_B(9), (255, 255, 255))
    # Road, red car and two evening figures.
    draw.rectangle([x, y + h - 12, x + w, y + h], fill=(22, 22, 40))
    for dx in range(8, w, 32):
        draw.rectangle([x + dx, y + h - 7, x + dx + 16, y + h - 5], fill=(240, 220, 120))
    draw.rounded_rectangle([x + 108, y + h - 30, x + 196, y + h - 14],
                           radius=5, fill=(212, 42, 42))
    draw.rounded_rectangle([x + 128, y + h - 40, x + 176, y + h - 30],
                           radius=4, fill=(170, 30, 30))
    for wx in (x + 122, x + 178):
        draw.ellipse([wx, y + h - 16, wx + 12, y + h - 4], fill=(18, 18, 18))
        draw.ellipse([wx + 3, y + h - 13, wx + 9, y + h - 7], fill=(160, 160, 160))
    for fx, dress in ((58, (198, 40, 40)), (252, (40, 40, 60))):
        draw.ellipse([x + fx - 6, y + h - 58, x + fx + 6, y + h - 46], fill=(232, 196, 160))
        draw.polygon([(x + fx - 9, y + h - 46), (x + fx + 9, y + h - 46),
                      (x + fx + 13, y + h - 14), (x + fx - 13, y + h - 14)],
                     fill=dress)


def hero_art_kyiv(draw, x, y, w, h):
    """A cable bridge at night under a moon, lit by two starburst blasts."""
    draw.rectangle([x, y, x + w, y + h], fill=(15, 28, 56))
    for sx, sy, sr in [(20, 14, 1), (70, 30, 1), (120, 10, 2), (180, 22, 1),
                       (240, 12, 1), (290, 34, 2), (150, 44, 1), (260, 52, 1)]:
        draw.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                     fill=(240, 240, 220))
    draw.ellipse([x + 26, y + 12, x + 56, y + 42], fill=(244, 234, 210))
    draw.ellipse([x + 34, y + 20, x + 40, y + 26], fill=(214, 200, 170))
    draw.ellipse([x + 44, y + 30, x + 48, y + 34], fill=(214, 200, 170))
    # Twin A-frame towers and their cables.
    apex = (x + w // 2, y + 18)
    for foot in (x + 52, x + w - 52):
        draw.line([foot, y + 112, apex[0], apex[1]], fill=(232, 224, 204), width=6)
    draw.rectangle([x, y + 108, x + w, y + 118], fill=(216, 207, 192))
    for cx in range(70, w - 40, 34):
        frac = abs(cx - w // 2) / max(1, w // 2 - 52)
        cable_y = y + 112 - (112 - 18) * (1 - frac)
        draw.line([x + cx, y + 108, x + cx, cable_y], fill=(180, 172, 150), width=1)
    # Two starburst explosions over the deck.
    for bx, by in ((x + 108, y + 88), (x + 210, y + 88)):
        draw.polygon(star_points(bx, by, 22, 9), fill=(255, 210, 62))
        draw.polygon(star_points(bx, by, 11, 5), fill=(255, 140, 40))
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 240, 180))
    # Dark water with pale reflections.
    draw.rectangle([x, y + 118, x + w, y + h], fill=(10, 24, 48))
    for wy in (126, 134, 142):
        for wx in range(14, w - 30, 46):
            draw.line([x + wx, y + wy, x + wx + 26, y + wy], fill=(70, 110, 150), width=2)


def hero_art_markets(draw, x, y, w, h):
    """Falling red candlesticks, a downtrend line and a red ticker bar."""
    draw.rectangle([x, y, x + w, y + h], fill=(13, 26, 51))
    candles = [(26, 16, 40), (64, 26, 52), (102, 40, 66), (140, 52, 78),
               (178, 64, 90), (216, 78, 102), (254, 88, 110)]
    for cx, top, bot in candles:
        draw.line([x + cx + 7, y + top - 6, x + cx + 7, y + bot + 6],
                  fill=(229, 72, 77), width=2)
        draw.rectangle([x + cx, y + top, x + cx + 14, y + bot], fill=(229, 72, 77))
    trend = [(x + 16, y + 12), (x + 90, y + 38), (x + 164, y + 62),
             (x + 238, y + 88), (x + 302, y + 110)]
    draw.line(trend, fill=(255, 107, 107), width=3)
    draw.polygon([(x + 302, y + 110), (x + 288, y + 102), (x + 290, y + 116)],
                 fill=(255, 107, 107))
    draw.text((x + 18, y + 74), "-1,101", font=SERIF_B(32), fill=(255, 255, 255))
    draw.text((x + 18, y + 112), "DOW   -2.19%", font=SANS_B(12), fill=(255, 107, 107))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(193, 39, 45))
    centered(draw, x + w // 2, y + h - 19,
             "S&P -2.0%   NASDAQ -2.3%   VIX 28.44   NIKKEI -5%",
             SANS_B(9), (255, 255, 255))


HEROES = [
    ("CULTURE  ·  LEONIDA", "GTA VI: $2.36BN IN A DAY",
     "Sensor Tower estimates 24.58m copies sold on day one, biggest "
     "entertainment launch ever; Metacritic 99, PlayStation Store 4.86/5.",
     hero_art_gta),
    ("WAR IN UKRAINE  ·  KYIV", "KYIV HIT, 8 DEAD",
     "Russia's overnight barrage hits bridges, energy and ports; a cargo "
     "ship bound for Odesa is struck. France calls for a UN Security "
     "Council meeting.",
     hero_art_kyiv),
    ("MARKETS  ·  NEW YORK", "WALL ST'S WORST WEEK",
     "Dow plunges 1,101 points below 50,000; S&P falls a sixth straight "
     "day as Anthropic's $81bn debut fails to lift AI shares. Nikkei "
     "tumbles 5%.",
     hero_art_markets),
]


def draw_heroes(draw):
    panel_w = (CONTENT_W - 20) // 3
    art_h = 150
    top = 96
    for i, (kicker, headline, deck, art_fn) in enumerate(HEROES):
        px = MARGIN + i * (panel_w + 10)
        art_fn(draw, px, top, panel_w, art_h)
        ky = top + art_h + 6
        draw.text((px, ky), kicker, font=SANS_B(10), fill=RED)
        draw.ellipse([px + panel_w - 22, ky - 1, px + panel_w, ky + 21],
                     fill=RED)
        centered(draw, px + panel_w - 11, ky + 3, str(i + 1), SANS_B(11),
                 (255, 255, 255))
        hy = ky + 16
        for j, line in enumerate(wrap(draw, headline, SERIF_B(19), panel_w)):
            draw.text((px, hy + j * 22), line, font=SERIF_B(19), fill=INK)
        dy = hy + 46
        for j, line in enumerate(wrap(draw, deck, SANS(11), panel_w)):
            draw.text((px, dy + j * 14), line, font=SANS(11), fill=(58, 54, 48))


# -------------------------------------------------------------- features ---

def strip_globe(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(207, 232, 216))
    draw.ellipse([x + 24, y + 8, x + 58, y + 42], fill=(74, 144, 217))
    draw.ellipse([x + 30, y + 14, x + 42, y + 24], fill=(96, 190, 110))
    draw.ellipse([x + 42, y + 28, x + 54, y + 38], fill=(96, 190, 110))
    draw.ellipse([x + 140, y + 8, x + 156, y + 24], fill=(247, 183, 49))
    for dx, dy in [(148, 2), (160, 14), (134, 14)]:
        draw.line([x + dx, y + dy, x + dx, y + dy + 4], fill=(247, 183, 49), width=2)


def strip_bars(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(216, 236, 210))
    heights = [10, 18, 15, 26, 34]
    for i, bh in enumerate(heights):
        bx = x + 26 + i * 20
        draw.rectangle([bx, y + h - 8 - bh, bx + 13, y + h - 8], fill=(38, 140, 120))
    draw.line([x + 20, y + 8, x + 128, y + h - 30], fill=(38, 120, 100), width=2)
    draw.ellipse([x + 148, y + 6, x + 172, y + 30], fill=(242, 193, 78))
    draw.ellipse([x + 151, y + 9, x + 169, y + 27], outline=(190, 140, 40), width=1)
    centered(draw, x + 160, y + 10, "$", SANS_B(13), (140, 100, 20))


def strip_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(221, 214, 243))
    draw.rectangle([x + 66, y + 10, x + 106, y + 38], fill=(40, 40, 60))
    for px in range(72, 104, 8):
        draw.line([x + px, y + 6, x + px, y + 10], fill=(40, 40, 60), width=2)
        draw.line([x + px, y + 38, x + px, y + 42], fill=(40, 40, 60), width=2)
    draw.rectangle([x + 78, y + 18, x + 94, y + 30], fill=(229, 72, 77))
    draw.polygon([(x + 140, y + 8), (x + 152, y + 8), (x + 146, y + 16),
                  (x + 158, y + 16), (x + 138, y + 40), (x + 150, y + 40),
                  (x + 140, y + 28), (x + 128, y + 28)], fill=(214, 48, 48))


def strip_storm(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(211, 229, 245))
    cx, cy = x + 58, y + 24
    for r in (18, 13, 8):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=(90, 130, 180), width=3)
    draw.polygon([(x + 128, y + 6), (x + 140, y + 6), (x + 132, y + 24),
                  (x + 142, y + 24), (x + 124, y + 44), (x + 130, y + 26),
                  (x + 122, y + 26)], fill=(247, 201, 60))


def strip_dove(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(251, 227, 211))
    draw.ellipse([x + 52, y + 18, x + 118, y + 36], fill=(255, 255, 255))
    draw.ellipse([x + 108, y + 10, x + 124, y + 26], fill=(255, 255, 255))
    draw.polygon([(x + 124, y + 16), (x + 134, y + 19), (x + 124, y + 22)],
                 fill=(240, 160, 60))
    draw.ellipse([x + 114, y + 14, x + 117, y + 17], fill=(30, 30, 30))
    draw.arc([x + 66, y + 8, x + 104, y + 30], start=200, end=340,
             fill=(220, 220, 220), width=3)
    draw.line([x + 140, y + 38, x + 172, y + 30], fill=(96, 160, 90), width=2)
    for lx, ly in [(148, 36), (158, 33), (168, 31)]:
        draw.ellipse([x + lx, y + ly, x + lx + 7, y + ly + 4], fill=(96, 160, 90))


def strip_ship(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(207, 230, 242))
    draw.rectangle([x, y + 34, x + w, y + h], fill=(120, 180, 215))
    draw.polygon([(x + 30, y + 30), (x + 150, y + 30), (x + 142, y + 42),
                  (x + 38, y + 42)], fill=(178, 42, 42))
    draw.rectangle([x + 118, y + 16, x + 142, y + 30], fill=(245, 245, 245))
    draw.rectangle([x + 46, y + 18, x + 66, y + 30], fill=(242, 193, 78))
    draw.rectangle([x + 68, y + 18, x + 88, y + 30], fill=(74, 144, 217))
    draw.rectangle([x + 90, y + 18, x + 110, y + 30], fill=(96, 190, 110))
    for wx in range(20, w - 10, 26):
        draw.line([x + wx, y + 44, x + wx + 14, y + 44], fill=(255, 255, 255), width=1)


def strip_flags(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(247, 236, 210))
    for fx, flag in ((36, "id"), (104, "cn")):
        draw.line([x + fx, y + 6, x + fx, y + 44], fill=(90, 70, 50), width=2)
        if flag == "id":
            draw.rectangle([x + fx, y + 8, x + fx + 48, y + 18], fill=(214, 48, 48))
            draw.rectangle([x + fx, y + 18, x + fx + 48, y + 28], fill=(255, 255, 255))
        else:
            draw.rectangle([x + fx, y + 8, x + fx + 48, y + 28], fill=(222, 41, 16))
            draw.polygon(star_points(x + fx + 10, y + 15, 5, 2, spikes=5),
                         fill=(255, 222, 0))
            for sx, sy in [(22, 12), (26, 17), (26, 22), (22, 25)]:
                draw.polygon(star_points(x + fx + sx, y + sy, 3, 1, spikes=5),
                             fill=(255, 222, 0))


def strip_barrier(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 218))
    draw.rectangle([x + 26, y + 14, x + 32, y + 42], fill=(60, 60, 60))
    draw.rectangle([x + 156, y + 14, x + 162, y + 42], fill=(60, 60, 60))
    for i in range(6):
        col = (214, 48, 48) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x + 32 + i * 21, y + 16, x + 53 + i * 21, y + 26], fill=col)
    draw.rectangle([x + 66, y + 30, x + 122, y + 42], fill=(255, 255, 255),
                   outline=(178, 28, 24), width=1)
    centered(draw, x + 94, y + 32, "CLOSED", SANS_B(8), RED_DARK)


def strip_probe(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(227, 221, 247))
    draw.rectangle([x + 66, y + 18, x + 106, y + 30], fill=(212, 175, 55))
    draw.line([x + 106, y + 24, x + 128, y + 14], fill=(120, 120, 120), width=2)
    draw.ellipse([x + 126, y + 8, x + 138, y + 20], fill=(160, 160, 160))
    draw.line([x + 66, y + 24, x + 48, y + 12], fill=(120, 120, 120), width=2)
    draw.ellipse([x + 42, y + 6, x + 54, y + 18], fill=(200, 200, 200))
    draw.ellipse([x + 146, y + 28, x + 162, y + 44], fill=(170, 160, 150))
    for sx, sy in [(24, 10), (170, 8), (30, 36), (150, 40)]:
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))


def strip_race(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(217, 236, 217))
    draw.rounded_rectangle([x + 30, y + 22, x + 118, y + 36], radius=5,
                           fill=(198, 38, 30))
    draw.rounded_rectangle([x + 52, y + 12, x + 92, y + 24], radius=4,
                           fill=(160, 28, 28))
    for wx in (x + 42, x + 98):
        draw.ellipse([wx, y + 34, wx + 14, y + 46], fill=(20, 20, 20))
        draw.ellipse([wx + 4, y + 38, wx + 10, y + 44], fill=(150, 150, 150))
    draw.line([x + 146, y + 6, x + 146, y + 42], fill=(90, 70, 50), width=2)
    for r in range(3):
        for c in range(4):
            col = (20, 20, 20) if (r + c) % 2 == 0 else (255, 255, 255)
            draw.rectangle([x + 146 + c * 7, y + 8 + r * 7,
                            x + 153 + c * 7, y + 15 + r * 7], fill=col)


FEATURES = [
    (4, "CLIMATE", "COP31 DRAFT ERASES FOSSIL FUELS",
     "Final-day text drops every mention of oil, gas and coal; talks head "
     "for overtime.", strip_globe),
    (5, "AI IPO", "ANTHROPIC SLIPS ON DAY TWO",
     "ANT opened at $111.50, closed $97.17 — still +17% on its $83 IPO "
     "price.", strip_bars),
    (6, "TECH", "NVIDIA IN TURMOIL",
     "H200 chip shipments to China halted; board refuses to bring back "
     "ousted Huang.", strip_chip),
    (7, "WEATHER", "CYCLONE AKVAN MAKES LANDFALL",
     "Storm crosses near Gopalpur at 70-80 km/h; 300,000 evacuated, no "
     "major damage.", strip_storm),
    (8, "GAZA", "GAZA PLAN SCORES 4 OF 26",
     "Board of Peace warns the ceasefire risks collapse; Israel controls "
     "70% of Gaza.", strip_dove),
    (9, "MIDDLE EAST", "HOUTHI MISSILE HITS RIYADH",
     "Blast damages a sovereign wealth fund tower; Houthis threaten Red "
     "Sea ports.", strip_ship),
    (10, "ASIA", "PRABOWO AND XI TALK SEAS",
     "South China Sea joint development agreed; 35 deals worth $15bn "
     "signed.", strip_flags),
    (11, "EUROPE", "ESTONIA SHUTS RUSSIA BORDER",
     "Crossings close from 1 December for six months; Moscow cries 'Iron "
     "Curtain'.", strip_barrier),
    (12, "SPACE", "VOYAGER 1, ONE LIGHT-DAY OUT",
     "Probe crosses 26bn km — but its data stopped on 14 November. "
     "BepiColombo reaches Mercury.", strip_probe),
    (13, "SPORT", "RUSSELL TOPS WET VEGAS FP2",
     "Mercedes star clocks 1:47.272; Gasly +0.071, Leclerc third. FP1 "
     "washed out.", strip_race),
]


def draw_features(draw):
    card_w = 188
    gap = 9
    strip_h = 48
    for row in range(2):
        top = 366 + row * 138
        for col in range(5):
            num, kicker, headline, deck, art_fn = FEATURES[row * 5 + col]
            cx = MARGIN + col * (card_w + gap)
            art_fn(draw, cx, top, card_w, strip_h)
            draw.text((cx, top + strip_h + 6), f"{num:02d}  ·  {kicker}",
                      font=SANS_B(9), fill=RED)
            hy = top + strip_h + 20
            for j, line in enumerate(wrap(draw, headline, SERIF_B(13), card_w)):
                draw.text((cx, hy + j * 15), line, font=SERIF_B(13), fill=INK)
            dy = hy + 32
            for j, line in enumerate(wrap(draw, deck, SANS(10), card_w)[:3]):
                draw.text((cx, dy + j * 12), line, font=SANS(10), fill=(58, 54, 48))


# ------------------------------------------------------------------ map ---

CONTINENTS = [
    ([(46, 8), (126, 2), (191, 8), (211, 24), (186, 42), (156, 52),
      (126, 48), (96, 52), (61, 42), (36, 26)], (183, 217, 168)),
    ([(276, 4), (306, 2), (311, 12), (281, 14)], (200, 220, 200)),
    ([(201, 56), (241, 54), (261, 66), (251, 82), (226, 86), (208, 78),
      (194, 62)], (168, 213, 162)),
    ([(456, 6), (516, 2), (541, 14), (531, 30), (496, 34), (466, 26),
      (448, 14)], (232, 217, 168)),
    ([(456, 38), (521, 34), (561, 48), (551, 76), (521, 84), (481, 78),
      (456, 64)], (232, 201, 138)),
    ([(546, 8), (676, 2), (826, 6), (926, 20), (916, 52), (856, 66),
      (776, 72), (696, 64), (616, 58), (566, 42), (551, 22)], (240, 201, 160)),
    ([(856, 78), (916, 76), (930, 84), (880, 86)], (201, 214, 232)),
]

PINS = [(161, 44, 1), (528, 20, 2), (198, 22, 3), (228, 70, 4),
        (71, 32, 5), (771, 42, 6), (731, 54, 7), (554, 42, 8),
        (581, 54, 9), (811, 66, 10), (500, 10, 11), (901, 14, 12),
        (104, 36, 13)]

LEGEND = [("N AMERICA", (183, 217, 168)), ("S AMERICA", (168, 213, 162)),
          ("EUROPE", (232, 217, 168)), ("AFRICA", (232, 201, 138)),
          ("ASIA", (240, 201, 160)), ("OCEANIA", (201, 214, 232))]


def draw_map(draw):
    draw.text((MARGIN, 648), "WHERE IT HAPPENED", font=SANS_B(13), fill=NAVY)
    mx, my = MARGIN, 666
    draw.rectangle([mx, my, mx + CONTENT_W, my + 86], fill=SEA)
    for gx in range(0, CONTENT_W, 40):
        draw.line([mx + gx, my, mx + gx, my + 86], fill=GRID, width=1)
    for gy in range(0, 86, 22):
        draw.line([mx, my + gy, mx + CONTENT_W, my + gy], fill=GRID, width=1)
    for poly, col in CONTINENTS:
        draw.polygon([(mx + px, my + py) for px, py in poly], fill=col)
    for px, py, num in PINS:
        draw.ellipse([mx + px - 8, my + py - 8, mx + px + 8, my + py + 8],
                     fill=RED, outline=(255, 255, 255), width=1)
        centered(draw, mx + px, my + py - 6, str(num), SANS_B(9),
                 (255, 255, 255))
    lx = MARGIN
    for label, col in LEGEND:
        draw.rectangle([lx, 758, lx + 9, 767], fill=col, outline=(120, 120, 120))
        draw.text((lx + 12, 757), label, font=SANS(9), fill=MUTED)
        lx += 12 + int(draw.textlength(label, font=SANS(9))) + 22


# ---------------------------------------------------------------- brief ---

BRIEFS_LEFT = [
    (14, "Myanmar calls ICJ genocide ruling 'unfair'"),
    (15, "Russia rejects NATO-style guarantees for Ukraine"),
    (16, "Moscow: Kallas role would collapse Ukraine talks"),
    (17, "Iraq deploys forces in militia stronghold"),
    (18, "Trump asks top court to block Venezuelan TPS"),
    (19, "Supreme Court to review asylum order"),
    (20, "US and Venezuela sign military cooperation deal"),
    (21, "US Senate rejects Iran war-powers resolution"),
    (22, "Trump warns Iran may seek chemical weapons"),
    (23, "Iran war in ninth month; ADNOC ship struck"),
    (24, "UK pledges 1,000+ drones for Ukraine"),
    (25, "EU to summon Russian envoy over Kyiv damage"),
    (26, "Poland probes unknown objects near border"),
    (27, "UK-EU set to agree youth mobility scheme"),
    (28, "UN secretary-general race stalls"),
    (29, "Bukele registers for third term"),
]

BRIEFS_RIGHT = [
    (30, "Migrant boat capsizes off Senegal"),
    (31, "Drone strike kills 10 at Sudan gold mine"),
    (32, "Kenya discharges last Ebola patient"),
    (33, "Bangladesh violence ahead of Hasina return"),
    (34, "Denmark ratifies Greenland security deal"),
    (35, "Colombia protests over tax plans"),
    (36, "Japan inflation rises; rate hike on track"),
    (37, "Philippines-Chile sign free-trade deal"),
    (38, "Japan's Takaichi gets cool APEC reception"),
    (39, "Spain's Sanchez admits mistakes"),
    (40, "Isomorphic Labs raises $5bn Series C"),
    (41, "Trump pardons Pete Rose posthumously"),
    (42, "US sanctions Comancheros and 'Ndrangheta"),
    (43, "Gemini agent runs Mac apps for Google"),
    (44, "Meta's Muse leaks private chats"),
    (45, "Moonshot cancels $150m Nvidia chip deal"),
]


def draw_brief(draw):
    draw.text((MARGIN, 780), "THE DAY IN BRIEF", font=SANS_B(13), fill=NAVY)
    for col_x, items in ((MARGIN, BRIEFS_LEFT), (MARGIN + 500, BRIEFS_RIGHT)):
        for i, (num, text) in enumerate(items):
            iy = 798 + i * 11
            draw.text((col_x, iy), str(num), font=SANS_B(10), fill=RED)
            draw.text((col_x + 22, iy), text, font=SANS(10), fill=INK)


# ----------------------------------------------------------------- main ---

def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # Masthead.
    centered(draw, W // 2, 8, "THE DAY IN WORLD NEWS", SERIF_B(46), NAVY)
    centered(draw, W // 2, 66,
             "FRIDAY, 20 NOVEMBER 2026  ·  45 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
             SANS_B(12), NAVY)
    draw.line([MARGIN, 84, W - MARGIN, 84], fill=NAVY, width=2)
    draw.line([MARGIN, 88, W - MARGIN, 88], fill=NAVY, width=1)
    draw_heroes(draw)
    draw.line([MARGIN, 358, W - MARGIN, 358], fill=NAVY, width=1)
    draw_features(draw)
    draw.line([MARGIN, 642, W - MARGIN, 642], fill=NAVY, width=1)
    draw_map(draw)
    draw.line([MARGIN, 774, W - MARGIN, 774], fill=NAVY, width=1)
    draw_brief(draw)
    draw.line([MARGIN, 980, W - MARGIN, 980], fill=NAVY, width=1)
    centered(draw, W // 2, 988,
             "Sources: Reuters · AP · AFP · BBC · Al Jazeera · "
             "The Day in World News, Friday 20 November 2026",
             SANS(9), MUTED)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if out_dir == ".":
        out_path = Path("entry.png")
    else:
        out_path = Path(out_dir) / "entry.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
    img = build()
    img.save(out_path, format="PNG")
    print(f"wrote {out_path} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
