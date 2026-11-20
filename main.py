#!/usr/bin/env python3
"""The World in One Day — Friday 20 November 2026.
A 1024x1024 newspaper front page drawn with PIL, no network.
Reads nothing, writes entry.png to $MAKEFUN_OUTPUT_DIR (default
/output, the harness path) or "out" when that is not writable.
Deterministic: same bytes on every run.

Layout follows the 19 November edition (round 5): strict grid symmetry,
uniform one-line headlines, tall hero panels (314x178, ~1.76:1) with
symmetric illustrations, a real lon/lat world map with pins at true
locations, and a saturated colour palette.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 231)
INK = (26, 32, 54)
NAVY = (31, 58, 95)
RED = (196, 40, 30)
GOLD = (212, 150, 32)
TEAL = (24, 128, 122)
SAGE = (96, 146, 92)
ROSE = (220, 126, 116)
SKY = (120, 170, 210)
SAND = (232, 196, 130)
LILAC = (140, 122, 196)
GREY = (110, 112, 118)
RULE = (26, 32, 54)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def uniform_size(draw, texts, path, max_size, width, min_size=8):
    """Largest size (<= max_size) at which EVERY text fits `width` on one
    line. All texts then share one size: no random sizing."""
    size = max_size
    while size > min_size:
        f = font(path, size)
        if all(draw.textlength(t, font=f) <= width for t in texts):
            return size
        size -= 1
    return min_size


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centre(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.2)


# ------------------------------------------------------------ stories
# (num, kicker, headline, deck, place) — all events of Fri 20 Nov 2026.
HEROES = [
    (1, "CULTURE  ·  LEONIDA",
     "GTA VI: $2.36BN IN A DAY",
     "Sensor Tower estimates 24.58m copies sold on day one — the biggest entertainment launch ever. Metacritic 99, PlayStation Store 4.86/5.",
     "MIAMI"),
    (2, "WAR IN UKRAINE  ·  KYIV",
     "KYIV HIT, 8 DEAD",
     "Russia's overnight barrage hits bridges, energy and ports; a cargo ship bound for Odesa is struck. France calls for a UN Security Council meeting.",
     "KYIV"),
    (3, "MARKETS  ·  NEW YORK",
     "WALL ST'S WORST WEEK",
     "Dow plunges 1,101 points below 50,000; S&P falls a sixth straight day as Anthropic's $81bn debut fails to lift AI shares. Nikkei tumbles 5%.",
     "NEW YORK"),
]

FEATURES = [
    (4, "CLIMATE", "COP31 DRAFT ERASES FOSSIL FUELS",
     "Final-day text drops every mention of oil, gas and coal; talks head for overtime."),
    (5, "AI IPO", "ANTHROPIC SLIPS ON DAY TWO",
     "ANT opened at $111.50, closed $97.17 — still +17% on its $83 IPO price."),
    (6, "TECH", "NVIDIA IN TURMOIL",
     "H200 chip shipments to China halted; board refuses to bring back ousted Huang."),
    (7, "WEATHER", "CYCLONE AKVAN MAKES LANDFALL",
     "Storm crosses near Gopalpur at 70-80 km/h; 300,000 evacuated, no major damage."),
    (8, "GAZA", "GAZA PLAN SCORES 4 OF 26",
     "Board of Peace warns the ceasefire risks collapse; Israel controls 70% of Gaza."),
    (9, "MIDDLE EAST", "HOUTHI MISSILE HITS RIYADH",
     "Blast damages a sovereign wealth fund tower; Houthis threaten Red Sea ports."),
    (10, "ASIA", "PRABOWO AND XI TALK SEAS",
     "South China Sea joint development agreed; 35 deals worth $15bn signed."),
    (11, "EUROPE", "ESTONIA SHUTS RUSSIA BORDER",
     "Crossings close from 1 December for six months; Moscow cries 'Iron Curtain'."),
    (12, "SPACE", "VOYAGER 1, ONE LIGHT-DAY OUT",
     "Probe crosses 26bn km — but its data stopped on 14 November. BepiColombo reaches Mercury."),
    (13, "SPORT", "RUSSELL TOPS WET VEGAS FP2",
     "Mercedes star clocks 1:47.272; Gasly +0.071, Leclerc third. FP1 washed out."),
]

BRIEFS = [
    (14, "Myanmar calls ICJ genocide ruling 'unfair'", "Dhaka eyes Rohingya return in 1-1.5 years."),
    (15, "Russia rejects NATO-style guarantees for Ukraine", "Ryabkov pushes back on the US idea."),
    (16, "Moscow: Kallas role would collapse Ukraine talks", "EU foreign policy chief unwelcome, Russia says."),
    (17, "Iraq deploys forces in militia stronghold", "Troops move into Kataib Hezbollah's Jurf al-Sakhar."),
    (18, "Trump asks top court to block Venezuelan TPS", "Ninth Circuit freezes restoration again."),
    (19, "Supreme Court to review Trump's asylum order", "Arguments due in spring 2027."),
    (20, "US and Venezuela sign military cooperation deal", "Hegseth in Caracas with acting president Rodriguez."),
    (21, "US Senate rejects Iran war-powers resolution", "Measure fails 51-48."),
    (22, "Trump warns Iran may seek chemical weapons", "Tehran 'exploring' WMD after nuclear strikes."),
    (23, "Iran war in ninth month; ADNOC ship struck", "One crew member missing in the Gulf."),
    (24, "UK pledges 1,000+ drones for Ukraine", "£260m package of long-range kit."),
    (25, "EU to summon Russian envoy over Kyiv damage", "Embassy hit in Thursday's strikes."),
    (26, "Poland probes unknown objects near border", "Air-threat warning lifted after checks."),
    (27, "UK-EU set to agree youth mobility scheme", "Deal expected at Friday's Brussels summit."),
    (28, "UN secretary-general race stalls", "No winner after eight votes."),
    (29, "Bukele registers for third term", "El Salvador's president seeks re-election again."),
    (30, "Migrant boat capsizes off Senegal", "Dozens missing near Yenne."),
    (31, "Drone strike kills 10 at Sudan gold mine", "Attack hits South Kordofan site."),
    (32, "Kenya discharges last Ebola patient", "Outbreak ends 37 days after first case."),
    (33, "Bangladesh violence ahead of Hasina return", "Clashes as ex-PM plans comeback."),
    (34, "Denmark ratifies Greenland security deal", "Pact with the US ends Trump-era standoff."),
    (35, "Colombia protests over tax plans", "Thousands march in Bogota."),
    (36, "Japan inflation rises; rate hike on track", "Prices keep pressure on the Bank of Japan."),
    (37, "Philippines and Chile sign free-trade deal", "Pact struck on APEC sidelines."),
    (38, "Japan's Takaichi gets cool APEC reception", "First Japanese leader visit to China since 2019."),
    (39, "Spain's Sanchez admits mistakes", "PM concedes errors before election debate."),
    (40, "Isomorphic Labs raises $5bn Series C", "AI drug discovery round co-led by Greenoaks, Sequoia."),
    (41, "Trump pardons Pete Rose posthumously", "Late baseball star cleared by the president."),
    (42, "US sanctions Comancheros and 'Ndrangheta", "Gang assets under US jurisdiction blocked."),
    (43, "Gemini agent runs Mac apps for Google", "Blue Origin to launch AI server satellites in 2029."),
    (44, "Meta's Muse leaks private chats", "EU Commission hit by AI-assisted cyberattack."),
    (45, "Moonshot cancels $150m Nvidia chip deal", "AMD faces scrutiny over its China ties."),
]


# ------------------------------------------------------------ illustrations
def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _vgrad(draw, x, y, w, h, stops):
    """Smooth vertical gradient through (pos 0..1, color) stops."""
    for yy in range(h):
        t = yy / max(1, h - 1)
        col = stops[-1][1]
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                lt = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = _lerp(c0, c1, lt)
                break
        draw.line([x, y + yy, x + w, y + yy], fill=col)


def _star(draw, cx, cy, r, fill):
    """Five-point star."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def pin(draw, x, y, n, color=RED):
    """Numbered map pin: filled circle + white number."""
    r = 9
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=(255, 255, 255), width=2)
    t = str(n)
    f = font(SANS_B, 10)
    w = draw.textlength(t, font=f)
    draw.text((x - w / 2, y - 7), t, font=f, fill=(255, 255, 255))


def _palm(draw, px, base, ph, lean=0):
    """Upright palm: vertical trunk, symmetric fronds mirrored around it."""
    top = base - ph
    draw.line([px, base, px, top], fill=(30, 20, 52), width=3)
    # fronds: mirrored pairs, same length left and right
    for ang, ln in [(200, 20), (230, 22), (260, 20), (280, 20), (310, 22), (340, 20)]:
        ex = px + ln * math.cos(math.radians(ang))
        ey = top + 8 * math.sin(math.radians(ang)) - 2
        draw.line([px, top, ex, ey], fill=(30, 20, 52), width=2)
        draw.arc([min(px, ex) - 2, min(top, ey) - 2, max(px, ex) + 2,
                  max(top, ey) + 2], 0, 360, fill=(30, 20, 52), width=1)


def draw_gta_panel(draw, x, y, w, h):
    """Original neon-sunset poster art, SYMMETRIC and TALL: the panel is
    ~1.76:1, so the skyline has real vertical room — a big centred sun,
    tall mirrored towers, upright palms, tall figures. No Rockstar logo,
    no official artwork, no trademarked fonts."""
    cx = x + w // 2
    base = y + h
    _vgrad(draw, x, y, w, h, [(0.0, (255, 166, 84)), (0.32, (255, 102, 118)),
                               (0.58, (228, 70, 150)), (0.8, (116, 50, 154)),
                               (1.0, (60, 32, 104))])
    # big sun with glow, centred, setting behind the centre tower
    for r, c in [(36, (255, 118, 78)), (31, (255, 166, 96)), (26, (255, 214, 118))]:
        draw.ellipse([cx - r, y + 40 - r, cx + r, y + 40 + r], fill=c)
    # thin pink clouds, mirrored pair
    for cxx, cyy, cw in [(x + 18, y + 14, 52), (x + w - 70, y + 14, 52)]:
        draw.ellipse([cxx, cyy, cxx + cw, cyy + 6], fill=(255, 150, 150))
    # skyline: mirrored building pairs around the centre + centre tower
    back_pairs = [(56, 48, 66), (104, 44, 54), (140, 40, 76)]
    for off, bw, bh2 in back_pairs:
        for sx in (-1, 1):
            bx = cx + sx * off - (bw if sx < 0 else 0)
            draw.rectangle([bx, base - bh2, bx + bw, base], fill=(86, 46, 140))
    draw.rectangle([cx - 26, base - 84, cx + 26, base], fill=(86, 46, 140))
    front_pairs = [(34, 44, 100), (82, 42, 122), (126, 40, 88)]
    for off, bw, bh2 in front_pairs:
        for sx in (-1, 1):
            bx = cx + sx * off - (bw if sx < 0 else 0)
            draw.rectangle([bx, base - bh2, bx + bw, base], fill=(38, 20, 70))
            for wy in range(base - bh2 + 8, base - 6, 12):
                for wx in range(bx + 6, bx + bw - 6, 10):
                    if (wx * 7 + wy * 13) % 29 < 13:
                        draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 204, 108))
    # centre tower with antenna, lit windows and a centred neon sign
    draw.rectangle([cx - 24, base - 100, cx + 24, base], fill=(38, 20, 70))
    draw.line([cx, base - 100, cx, base - 112], fill=(38, 20, 70), width=2)
    draw.ellipse([cx - 2, base - 115, cx + 2, base - 111], fill=(255, 70, 70))
    for wy in range(base - 94, base - 6, 12):
        for wx in range(cx - 18, cx + 14, 10):
            if (wx * 7 + wy * 13) % 29 < 13:
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 204, 108))
    draw.rectangle([cx - 18, base - 78, cx + 18, base - 50], outline=(255, 80, 190),
                   width=2)
    f_n = font(SANS_B, 10)
    draw.text((cx - 14, base - 76), "VICE", font=f_n, fill=(255, 118, 208))
    draw.text((cx - 14, base - 65), "CITY", font=f_n, fill=(255, 204, 108))
    # street at the bottom with a centred car
    draw.rectangle([x, base - 16, x + w, base], fill=(28, 20, 48))
    draw.line([x, base - 16, x + w, base - 16], fill=(255, 214, 130), width=1)
    for dx in range(x + 8, x + w - 8, 26):
        draw.line([dx, base - 8, dx + 12, base - 8], fill=(255, 214, 130), width=2)
    carx, cary = cx - 24, base - 15
    draw.rounded_rectangle([carx, cary - 7, carx + 48, cary], radius=3, fill=(196, 40, 30))
    draw.polygon([(carx + 11, cary - 7), (carx + 18, cary - 14), (carx + 32, cary - 14),
                  (carx + 39, cary - 7)], fill=(132, 26, 26))
    draw.ellipse([carx + 7, cary - 3, carx + 13, cary + 3], fill=(20, 16, 30))
    draw.ellipse([carx + 35, cary - 3, carx + 41, cary + 3], fill=(20, 16, 30))
    draw.ellipse([carx + 46, cary - 6, carx + 49, cary - 3], fill=(255, 240, 180))
    # upright palms at mirrored positions
    _palm(draw, x + 24, base - 16, 66)
    _palm(draw, x + w - 24, base - 16, 66)
    # two tall figures, mirrored around the centre
    for sx, suit, dress in [(-1, (30, 26, 48), None), (1, None, (196, 40, 30))]:
        fx = cx + sx * 48
        draw.ellipse([fx - 7, base - 80, fx + 7, base - 64], fill=(232, 196, 164))
        if suit is not None:
            draw.polygon([(fx - 10, base - 64), (fx + 10, base - 64), (fx + 8, base - 16),
                          (fx - 8, base - 16)], fill=suit)
            draw.polygon([(fx - 2, base - 64), (fx + 2, base - 64), (fx + 3, base - 48),
                          (fx - 3, base - 48)], fill=(255, 255, 255))
            draw.polygon([(fx - 2, base - 64), (fx + 2, base - 64), (fx, base - 54)],
                         fill=(196, 40, 30))
        else:
            draw.arc([fx - 8, base - 82, fx + 8, base - 64], 180, 360,
                     fill=(60, 30, 20), width=4)
            draw.polygon([(fx - 9, base - 64), (fx + 9, base - 64), (fx + 13, base - 16),
                          (fx - 13, base - 16)], fill=dress)


def draw_kyiv_panel(draw, x, y, w, h):
    """Kyiv under a night barrage, SYMMETRIC and TALL: a dark night sky
    with stars, a river bridge with two mirrored towers, two mirrored
    explosion bursts, searchlight beams crossing at the centre, and a
    calm river band at the bottom."""
    cx = x + w // 2
    base = y + h
    _vgrad(draw, x, y, w, h, [(0.0, (12, 18, 44)), (0.5, (26, 38, 74)),
                               (1.0, (52, 62, 96))])
    # stars, mirrored pairs
    for sx, sy in [(x + 22, y + 14), (x + w - 22, y + 14), (x + 46, y + 30),
                   (x + w - 46, y + 30), (x + 70, y + 12), (x + w - 70, y + 12)]:
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # two NARROW searchlight beams from the deck corners, crossing at the
    # centre, mirrored — no wide tent shape
    draw.polygon([(x + 26, base - 20), (x + 40, base - 20), (cx + 6, y + 34),
                  (cx - 6, y + 34)], fill=(240, 236, 200))
    draw.polygon([(x + w - 40, base - 20), (x + w - 26, base - 20),
                  (cx + 6, y + 34), (cx - 6, y + 34)], fill=(240, 236, 200))
    # moon, top-left corner, clear of the beams
    draw.ellipse([x + 16, y + 8, x + 40, y + 32], fill=(240, 236, 200))
    draw.ellipse([x + 22, y + 12, x + 27, y + 17], fill=(214, 210, 172))
    draw.ellipse([x + 29, y + 18, x + 33, y + 22], fill=(214, 210, 172))
    # bridge deck across the panel, two mirrored towers
    deck_y = base - 52
    draw.rectangle([x, deck_y, x + w, deck_y + 6], fill=(18, 22, 40))
    for sx in (-1, 1):
        tx = cx + sx * 74
        draw.rectangle([tx - 5, deck_y - 46, tx + 5, deck_y], fill=(18, 22, 40))
        draw.polygon([(tx - 9, deck_y - 46), (tx + 9, deck_y - 46),
                      (tx, deck_y - 56)], fill=(18, 22, 40))
        draw.line([tx - 5, deck_y - 40, cx - 6, deck_y - 2], fill=(120, 126, 150),
                  width=1)
        draw.line([tx + 5, deck_y - 40, cx + 6, deck_y - 2], fill=(120, 126, 150),
                  width=1)
        # lit windows on the towers
        for wy in range(deck_y - 40, deck_y - 4, 10):
            draw.rectangle([tx - 2, wy, tx + 2, wy + 4], fill=(255, 204, 108))
    # suspension cables from the centre
    draw.line([cx - 74, deck_y - 44, cx, deck_y - 2], fill=(120, 126, 150), width=1)
    draw.line([cx + 74, deck_y - 44, cx, deck_y - 2], fill=(120, 126, 150), width=1)
    # two mirrored explosion bursts above the deck
    for ex in (cx - 44, cx + 44):
        _star(draw, ex, deck_y - 26, 16, (255, 138, 30))
        _star(draw, ex, deck_y - 26, 9, (255, 212, 80))
        _star(draw, ex, deck_y - 26, 4, (255, 255, 255))
        for dx, dy in [(-12, -8), (12, -8), (-14, 4), (14, 4)]:
            draw.ellipse([ex + dx - 3, deck_y - 26 + dy - 3,
                          ex + dx + 3, deck_y - 26 + dy + 3],
                         fill=(160, 160, 160))
    # river band at the bottom with mirrored reflections
    draw.rectangle([x, base - 20, x + w, base], fill=(30, 52, 96))
    for rx in range(x + 10, x + w - 10, 26):
        draw.line([rx, base - 12, rx + 14, base - 12], fill=(120, 160, 210),
                  width=1)
    draw.line([cx - 44, base - 8, cx - 30, base - 8], fill=(255, 138, 30), width=2)
    draw.line([cx + 30, base - 8, cx + 44, base - 8], fill=(255, 138, 30), width=2)


def draw_markets_panel(draw, x, y, w, h):
    """Wall Street sell-off, SYMMETRIC and TALL: a dark trading-floor
    panel, six evenly spaced candlesticks stepping down toward the
    centre, a big red down arrow, and a ticker tape along the bottom."""
    cx = x + w // 2
    base = y + h
    draw.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    # faint grid
    for gy in range(y + 16, base - 30, 22):
        draw.line([x + 8, gy, x + w - 8, gy], fill=(44, 50, 72), width=1)
    # six candlesticks, evenly spaced, stepping down to the centre
    heights = [26, 22, 30, 24, 32, 28]
    tops = [26, 38, 52, 66, 82, 96]
    for i, (bh, top) in enumerate(zip(heights, tops)):
        bx = x + 22 + i * 46
        cy = y + top
        draw.line([bx + 6, cy - 8, bx + 6, cy + bh + 8], fill=(200, 200, 210),
                  width=1)
        draw.rectangle([bx, cy, bx + 12, cy + bh], fill=(196, 40, 30),
                       outline=(255, 120, 110), width=1)
    # big red down arrow across the top, centred
    draw.line([x + 30, y + 18, cx, y + 66, x + w - 30, y + 96], fill=(255, 70, 60),
              width=4)
    draw.polygon([(x + w - 30, y + 96), (x + w - 52, y + 92), (x + w - 34, y + 114)],
                 fill=(255, 70, 60))
    # headline figure, centred
    f_big = font(SANS_B, 26)
    t = "-1,101"
    draw.text((cx - draw.textlength(t, font=f_big) / 2, y + 108), t, font=f_big,
              fill=(255, 120, 110))
    f_sub = font(SANS_B, 11)
    t2 = "DOW  ·  -2.19%"
    draw.text((cx - draw.textlength(t2, font=f_sub) / 2, y + 140), t2, font=f_sub,
              fill=(255, 255, 255))
    # ticker tape along the bottom
    draw.rectangle([x, base - 24, x + w, base], fill=(196, 40, 30))
    f_t = font(SANS_B, 10)
    tape = "S&P -2.0%   NASDAQ -2.3%   VIX 28.44   NIKKEI -5%"
    draw.text((cx - draw.textlength(tape, font=f_t) / 2, base - 19), tape,
              font=f_t, fill=(255, 255, 255))


def draw_feature_icon(draw, x, y, w, h, kind):
    """Flat illustration per feature kind. Every icon is CENTRED and LEVEL:
    its main subject sits on the panel centre, elements are mirrored or
    evenly spaced, nothing leans at a random angle."""
    bg = {"ipo": (196, 228, 196), "war": (238, 204, 186), "gulf": (198, 220, 240),
          "storm": (196, 214, 242), "market": (232, 220, 178), "climate": (188, 226, 200),
          "gaza": (240, 212, 196), "voyager": (200, 200, 244), "moon": (212, 200, 244),
          "sport": (238, 220, 178), "chip": (200, 200, 244), "flags": (232, 220, 178),
          "border": (220, 210, 200), "race": (200, 214, 240)}
    draw.rectangle([x, y, x + w, y + h], fill=bg.get(kind, (232, 226, 196)))
    cx, cy = x + w // 2, y + h // 2
    if kind == "ipo":  # rising bars, centred, + trend arrow + gold coin
        for i, bh in enumerate([12, 20, 28, 36]):
            bx = cx - 30 + i * 16
            draw.rectangle([bx, cy + 16 - bh, bx + 11, cy + 16], fill=TEAL,
                           outline=(255, 255, 255), width=1)
        draw.line([cx - 32, cy - 16, cx + 32, cy - 26], fill=RED, width=2)
        draw.polygon([(cx + 32, cy - 26), (cx + 24, cy - 26), (cx + 32, cy - 18)], fill=RED)
        draw.ellipse([cx + 40, cy - 22, cx + 58, cy - 4], fill=GOLD,
                     outline=(150, 110, 50), width=1)
        f_d = font(SANS_B, 12)
        draw.text((cx + 46, cy - 19), "$", font=f_d, fill=(110, 78, 16))
    elif kind == "war":  # suspension bridge, symmetric towers + centred blast
        draw.rectangle([x, y + h - 10, x + w, y + h], fill=(130, 180, 224))
        for wx in range(x + 4, x + w - 4, 12):
            draw.arc([wx, y + h - 10, wx + 12, y + h - 2], 0, 180,
                     fill=(255, 255, 255), width=1)
        for tx in (cx - 34, cx + 28):
            draw.rectangle([tx, cy - 14, tx + 6, cy + 14], fill=INK)
            draw.polygon([(tx - 3, cy - 14), (tx + 9, cy - 14), (tx + 3, cy - 20)],
                         fill=INK)
        draw.line([x + 8, cy + 8, x + w - 8, cy + 8], fill=INK, width=3)
        draw.arc([cx - 34, cy - 16, cx + 34, cy + 8], 180, 360, fill=INK, width=2)
        draw.line([cx - 31, cy - 12, cx, cy + 8], fill=INK, width=1)
        draw.line([cx + 31, cy - 12, cx, cy + 8], fill=INK, width=1)
        _star(draw, cx, cy - 2, 9, (255, 138, 30))
        _star(draw, cx, cy - 2, 4, (255, 212, 80))
        for sx, sy in [(cx - 14, cy - 12), (cx + 14, cy - 12)]:
            draw.ellipse([sx - 4, sy - 3, sx + 4, sy + 3], fill=(160, 160, 160))
    elif kind == "gulf":  # oil tanker, level and centred
        draw.rectangle([x, y + h - 10, x + w, y + h], fill=(104, 162, 214))
        for wx in range(x + 4, x + w - 4, 14):
            draw.arc([wx, y + h - 10, wx + 14, y + h - 2], 0, 180,
                     fill=(255, 255, 255), width=1)
        draw.polygon([(cx - 40, cy + 4), (cx + 40, cy + 4), (cx + 30, cy + 16),
                      (cx - 30, cy + 16)], fill=NAVY)
        draw.rectangle([cx - 40, cy + 4, cx + 40, cy + 8], fill=(196, 40, 30))
        for i, c in enumerate([(212, 150, 32), (24, 128, 122), (196, 40, 30)]):
            draw.rectangle([cx - 24 + i * 16, cy - 8, cx - 10 + i * 16, cy + 4], fill=c,
                           outline=(255, 255, 255), width=1)
        draw.rectangle([cx + 28, cy - 16, cx + 40, cy + 4], fill=(255, 255, 255),
                       outline=INK, width=1)
        for wy in (cy - 13, cy - 9):
            draw.line([cx + 30, wy, cx + 38, wy], fill=INK, width=1)
        draw.rectangle([cx - 40, cy - 12, cx - 32, cy + 4], fill=(196, 40, 30))
        for sx, sy, sr in [(cx - 36, cy - 18, 4), (cx - 30, cy - 22, 3)]:
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(160, 160, 160))
        draw.polygon([(cx - 5, cy + 2), (cx, cy - 12), (cx + 5, cy + 2)],
                     fill=(255, 138, 30))
    elif kind == "storm":  # cyclone spiral CENTRED + mirrored rain + bolt
        for r, c in [(19, (104, 128, 168)), (13, (138, 160, 198)), (7, (172, 192, 220))]:
            draw.ellipse([cx - r, cy - r - 2, cx + r, cy + r - 2], fill=c)
        draw.arc([cx - 19, cy - 21, cx + 19, cy + 17], 20, 300, fill=(255, 255, 255),
                 width=2)
        draw.arc([cx - 12, cy - 14, cx + 12, cy + 10], 200, 120, fill=(255, 255, 255),
                 width=2)
        for rx in (cx - 38, cx - 26, cx + 26, cx + 38):
            draw.line([rx, cy + 12, rx - 3, cy + 22], fill=TEAL, width=2)
        draw.polygon([(cx + 44, cy - 6), (cx + 52, cy - 6), (cx + 46, cy + 6),
                      (cx + 54, cy + 6), (cx + 40, cy + 20), (cx + 46, cy + 20),
                      (cx + 42, cy + 10)], fill=(255, 206, 40))
    elif kind == "market":  # four candlesticks, evenly spaced and centred
        for i, (o, c) in enumerate([(0, 1), (1, 0), (0, 1), (1, 1)]):
            bx = cx - 30 + i * 16
            draw.line([bx + 4, cy - 18, bx + 4, cy + 16], fill=INK, width=1)
            col = RED if c else TEAL
            draw.rectangle([bx, cy - 8 + o * 8, bx + 8, cy + 8 - o * 8], fill=col)
        draw.line([cx - 34, cy - 20, cx - 16, cy - 12, cx + 2, cy - 16, cx + 20, cy - 4,
                   cx + 34, cy + 6], fill=RED, width=2)
        draw.polygon([(cx + 34, cy + 6), (cx + 26, cy + 2), (cx + 28, cy + 10)], fill=RED)
        f_m = font(SANS_B, 10)
        draw.text((cx + 16, cy - 22), "-1.1%", font=f_m, fill=RED)
    elif kind == "climate":  # globe CENTRED + sun + leaf at fixed corners
        draw.ellipse([cx - 15, cy - 13, cx + 15, cy + 13], fill=(104, 162, 214),
                     outline=NAVY, width=1)
        draw.ellipse([cx - 10, cy - 9, cx - 1, cy - 1], fill=SAGE)
        draw.ellipse([cx + 2, cy + 2, cx + 10, cy + 9], fill=SAGE)
        draw.ellipse([cx + 24, cy - 20, cx + 34, cy - 10], fill=(255, 206, 110))
        for a in range(8):
            ax, ay = cx + 29, cy - 15
            draw.line([ax + 8 * math.cos(a * math.pi / 4), ay + 8 * math.sin(a * math.pi / 4),
                       ax + 11 * math.cos(a * math.pi / 4), ay + 11 * math.sin(a * math.pi / 4)],
                      fill=(255, 206, 110), width=1)
        draw.polygon([(cx - 34, cy + 12), (cx - 24, cy + 2), (cx - 16, cy + 12),
                      (cx - 26, cy + 18)], fill=(58, 134, 58))
        draw.line([cx - 32, cy + 16, cx - 18, cy + 4], fill=(44, 104, 44), width=1)
    elif kind == "gaza":  # dove + olive branch, level and centred (no fish)
        # dove: horizontal body, head + beak right, wing arc on top, tail left
        draw.ellipse([cx - 26, cy - 8, cx + 22, cy + 8], fill=(255, 255, 255),
                     outline=INK, width=1)
        draw.ellipse([cx + 18, cy - 14, cx + 32, cy + 0], fill=(255, 255, 255),
                     outline=INK, width=1)
        draw.polygon([(cx + 32, cy - 10), (cx + 40, cy - 8), (cx + 32, cy - 5)],
                     fill=(255, 138, 30))
        draw.ellipse([cx + 24, cy - 12, cx + 26, cy - 10], fill=INK)
        draw.arc([cx - 14, cy - 12, cx + 12, cy + 4], 300, 60, fill=GREY, width=2)
        draw.line([cx - 26, cy + 2, cx - 36, cy - 2], fill=INK, width=2)
        draw.line([cx - 26, cy + 6, cx - 36, cy + 8], fill=INK, width=2)
        # olive branch below, symmetric leaves
        draw.line([cx - 22, cy + 16, cx + 22, cy + 16], fill=(58, 134, 58), width=2)
        for lx in (-16, 0, 16):
            draw.ellipse([cx + lx - 4, cy + 13, cx + lx + 4, cy + 19], fill=(58, 134, 58))
    elif kind == "voyager":  # deep-space probe, LEVEL, centred, symmetric arc
        for sx, sy, sr in [(cx - 40, cy - 14, 1), (cx - 24, cy - 18, 1),
                           (cx + 24, cy - 18, 1), (cx + 40, cy - 14, 1),
                           (cx - 32, cy + 14, 1), (cx + 32, cy + 14, 1)]:
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255))
        draw.arc([cx - 44, cy - 4, cx + 44, cy + 20], 200, 340, fill=GOLD, width=2)
        draw.polygon([(cx - 14, cy - 8), (cx + 12, cy - 8), (cx + 16, cy + 4),
                      (cx - 10, cy + 4)], fill=(212, 150, 32))
        draw.pieslice([cx + 4, cy - 12, cx + 24, cy + 8], 270, 90, fill=(255, 255, 255),
                      outline=INK)
        draw.line([cx - 14, cy - 2, cx - 28, cy - 12], fill=INK, width=2)
        draw.ellipse([cx - 32, cy - 16, cx - 24, cy - 8], fill=(255, 255, 255),
                     outline=INK)
        draw.ellipse([cx + 28, cy - 18, cx + 32, cy - 14], fill=(255, 206, 110))
    elif kind == "moon":  # rocket UPRIGHT (vertical), centred, + moon + orbit
        draw.ellipse([cx + 28, cy - 20, cx + 50, cy + 2], fill=(196, 192, 180),
                     outline=(146, 142, 130), width=1)
        for mx, my in [(cx + 34, cy - 15), (cx + 44, cy - 8), (cx + 38, cy - 5)]:
            draw.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=(146, 142, 130))
        draw.arc([cx - 34, cy - 18, cx + 34, cy + 18], 140, 300, fill=GOLD, width=2)
        draw.polygon([(cx - 7, cy - 16), (cx + 7, cy - 16), (cx + 5, cy + 8),
                      (cx - 5, cy + 8)], fill=(255, 255, 255), outline=INK, width=1)
        draw.polygon([(cx - 7, cy - 16), (cx + 7, cy - 16), (cx, cy - 24)], fill=RED)
        draw.polygon([(cx - 7, cy + 8), (cx - 13, cy + 16), (cx - 5, cy + 12)], fill=RED)
        draw.polygon([(cx + 7, cy + 8), (cx + 13, cy + 16), (cx + 5, cy + 12)], fill=RED)
        draw.ellipse([cx - 3, cy - 8, cx + 3, cy - 2], fill=(104, 162, 214), outline=INK)
        draw.polygon([(cx - 4, cy + 8), (cx + 4, cy + 8), (cx, cy + 18)], fill=(255, 138, 30))
        draw.polygon([(cx - 2, cy + 8), (cx + 2, cy + 8), (cx, cy + 14)], fill=(255, 212, 80))
    elif kind == "chip":  # AI chip, centred, pins mirrored on all sides
        draw.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], fill=(32, 36, 52),
                       outline=GOLD, width=2)
        draw.rectangle([cx - 8, cy - 6, cx + 8, cy + 6], fill=(196, 40, 30))
        for px in (-24, -18, -12, 12, 18, 24):
            draw.line([cx + px, cy - 12, cx + px, cy - 18], fill=INK, width=2)
            draw.line([cx + px, cy + 12, cx + px, cy + 18], fill=INK, width=2)
        for py in (-8, 0, 8):
            draw.line([cx - 16, cy + py, cx - 22, cy + py], fill=INK, width=2)
            draw.line([cx + 16, cy + py, cx + 22, cy + py], fill=INK, width=2)
        draw.line([cx + 30, cy - 16, cx + 44, cy + 2], fill=RED, width=2)
        draw.polygon([(cx + 44, cy + 2), (cx + 36, cy + 2), (cx + 44, cy + 10)],
                     fill=RED)
        f_c = font(SANS_B, 9)
        draw.text((cx + 30, cy + 6), "H200", font=f_c, fill=RED)
    elif kind == "flags":  # Indonesia + China flags on two poles, mirrored
        for i, (fx, top, bot) in enumerate([(cx - 26, (214, 24, 24), (255, 255, 255)),
                                            (cx + 26, (214, 24, 24), (214, 24, 24))]):
            draw.line([fx, cy - 18, fx, cy + 18], fill=(168, 120, 40), width=2)
            draw.ellipse([fx - 2, cy - 22, fx + 2, cy - 18], fill=(212, 150, 32))
            if i == 0:  # Indonesia: red over white
                draw.rectangle([fx - 14, cy - 16, fx + 14, cy - 6], fill=top)
                draw.rectangle([fx - 14, cy - 6, fx + 14, cy + 4], fill=bot,
                               outline=INK, width=1)
            else:  # China: red field, gold star
                draw.rectangle([fx - 14, cy - 16, fx + 14, cy + 4], fill=top,
                               outline=INK, width=1)
                _star(draw, fx - 6, cy - 10, 5, (255, 214, 40))
                for sx, sy in [(2, -14), (6, -10), (6, -5), (2, -2)]:
                    _star(draw, fx + sx, cy + sy, 1, (255, 214, 40))
        # handshake arc below, centred
        draw.arc([cx - 20, cy + 6, cx + 20, cy + 22], 180, 360, fill=INK, width=2)
        draw.ellipse([cx - 22, cy + 12, cx - 16, cy + 18], fill=(232, 196, 164))
        draw.ellipse([cx + 16, cy + 12, cx + 22, cy + 18], fill=(238, 205, 172))
    elif kind == "border":  # border barrier, centred, striped bar + sign
        draw.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 120, 118))
        for px in (cx - 34, cx + 34):
            draw.rectangle([px - 3, cy - 16, px + 3, cy + 16], fill=INK)
        # striped barrier bar
        for i in range(6):
            col = (255, 255, 255) if i % 2 == 0 else (196, 40, 30)
            draw.rectangle([cx - 31 + i * 11, cy - 8, cx - 20 + i * 11, cy - 2],
                           fill=col, outline=INK, width=1)
        # sign above the bar, centred
        draw.rectangle([cx - 16, cy - 24, cx + 16, cy - 12], fill=(255, 255, 255),
                       outline=RED, width=2)
        f_b = font(SANS_B, 9)
        draw.text((cx - 12, cy - 22), "CLOSED", font=f_b, fill=RED)
        # small flags on the posts
        draw.polygon([(cx - 34, cy - 16), (cx - 22, cy - 13), (cx - 34, cy - 10)],
                     fill=(30, 84, 180))
        draw.polygon([(cx + 34, cy - 16), (cx + 22, cy - 13), (cx + 34, cy - 10)],
                     fill=(214, 24, 24))
    elif kind == "race":  # race car in profile, centred, + checkered flag
        draw.rectangle([x, y + h - 10, x + w, y + h], fill=(104, 178, 96))
        # checkered flag on a pole at the right
        draw.line([cx + 40, cy - 20, cx + 40, cy + 14], fill=INK, width=2)
        for r in range(2):
            for c in range(4):
                col = (255, 255, 255) if (r + c) % 2 == 0 else INK
                draw.rectangle([cx + 40 + c * 5, cy - 20 + r * 6,
                                cx + 45 + c * 5, cy - 14 + r * 6], fill=col)
        # low open-wheel car, centred
        draw.polygon([(cx - 34, cy + 2), (cx - 20, cy - 6), (cx + 6, cy - 6),
                      (cx + 14, cy + 2)], fill=(196, 40, 30))
        draw.polygon([(cx - 12, cy - 6), (cx - 6, cy - 12), (cx + 4, cy - 12),
                      (cx + 8, cy - 6)], fill=(132, 26, 26))
        draw.rectangle([cx + 12, cy - 12, cx + 16, cy - 2], fill=(32, 36, 52))
        for wx in (cx - 26, cx + 8):
            draw.ellipse([wx - 7, cy - 2, wx + 7, cy + 12], fill=(20, 16, 30))
            draw.ellipse([wx - 3, cy + 2, wx + 3, cy + 8], fill=(160, 160, 160))
        # speed lines behind
        for sy in (cy - 10, cy - 2, cy + 6):
            draw.line([cx - 44, sy, cx - 38, sy], fill=(255, 255, 255), width=2)
    else:  # sport: football in front of a goal net, centred

        draw.rectangle([cx - 36, cy - 14, cx + 36, cy + 16], fill=(255, 255, 255),
                       outline=INK, width=1)
        for gx in range(cx - 28, cx + 36, 12):
            draw.line([gx, cy - 14, gx, cy + 16], fill=(200, 198, 190), width=1)
        for gy in range(cy - 8, cy + 16, 10):
            draw.line([cx - 36, gy, cx + 36, gy], fill=(200, 198, 190), width=1)
        draw.rectangle([x, cy + 16, x + w, y + h], fill=(104, 178, 96))
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 255, 255),
                     outline=INK, width=2)
        draw.polygon([(cx, cy - 6), (cx + 6, cy - 2), (cx + 4, cy + 5), (cx - 4, cy + 5),
                      (cx - 6, cy - 2)], fill=INK)
        for px, py in [(cx - 11, cy - 8), (cx + 11, cy - 8), (cx - 12, cy + 6),
                       (cx + 12, cy + 6), (cx, cy + 11)]:
            draw.polygon([(px, py - 3), (px + 3, py - 1), (px + 2, py + 3), (px - 2, py + 3),
                          (px - 3, py - 1)], fill=INK)


FEATURE_KIND = {4: "climate", 5: "ipo", 6: "chip", 7: "storm", 8: "gaza",
                9: "gulf", 10: "flags", 11: "border", 12: "voyager", 13: "race"}


# ------------------------------------------------------------ world map
# Continents as (lon, lat) polygons, projected equirectangular:
# lon -180..180 -> x, lat 83..-58 -> y. Pins sit at true locations.
CONTINENTS = [
    ("N AMERICA", (132, 186, 152), [
        (-168, 65), (-155, 71), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
        (-85, 66), (-78, 62), (-70, 58), (-65, 60), (-60, 55), (-55, 52),
        (-60, 47), (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32),
        (-81, 26), (-84, 30), (-89, 30), (-94, 29), (-97, 26), (-97, 16),
        (-94, 14), (-90, 14), (-86, 12), (-83, 9), (-79, 9), (-83, 10),
        (-88, 12), (-92, 14), (-96, 16), (-100, 18), (-105, 20), (-110, 24),
        (-114, 29), (-120, 34), (-124, 42), (-125, 49), (-130, 54), (-140, 60),
        (-150, 59), (-158, 58), (-165, 60)]),
    ("GREENLAND", (188, 206, 196), [
        (-58, 64), (-52, 60), (-44, 60), (-38, 64), (-30, 68), (-22, 70),
        (-25, 74), (-35, 76), (-50, 76), (-58, 74), (-60, 70)]),
    ("S AMERICA", (150, 196, 132), [
        (-80, 9), (-77, 8), (-72, 11), (-68, 11), (-62, 10), (-57, 6), (-52, 5),
        (-50, 0), (-44, -3), (-38, -5), (-35, -8), (-37, -13), (-39, -17),
        (-40, -22), (-44, -24), (-48, -27), (-52, -32), (-57, -38), (-62, -40),
        (-65, -43), (-67, -47), (-69, -52), (-71, -54), (-73, -50), (-73, -44),
        (-72, -37), (-71, -30), (-70, -23), (-70, -18), (-75, -15), (-79, -9),
        (-81, -5), (-80, 0), (-80, 5)]),
    ("EUROPE", (210, 188, 132), [
        (-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-4, 48), (-1, 50),
        (1, 51), (3, 53), (5, 53), (8, 55), (5, 58), (5, 62), (8, 63), (12, 65),
        (18, 66), (21, 66), (25, 65), (28, 64), (30, 62), (32, 65), (35, 66),
        (40, 67), (44, 66), (42, 62), (40, 58), (38, 55), (35, 52), (32, 50),
        (30, 46), (28, 44), (26, 41), (23, 40), (22, 37), (20, 39), (18, 40),
        (16, 38), (14, 42), (12, 44), (10, 44), (8, 44), (5, 43), (3, 42),
        (0, 40), (-2, 37), (-5, 36)]),
    ("UK", (210, 188, 132), [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 57),
                              (0, 54), (-1, 51)]),
    ("AFRICA", (232, 190, 122), [
        (-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37),
        (15, 35), (20, 32), (25, 32), (30, 31), (32, 31), (34, 28), (36, 24),
        (38, 20), (40, 15), (43, 11), (46, 11), (51, 12), (50, 8), (46, 4),
        (42, 0), (40, -4), (39, -8), (37, -12), (35, -16), (33, -20), (31, -24),
        (29, -29), (27, -33), (22, -35), (18, -34), (16, -32), (14, -28),
        (13, -22), (12, -17), (12, -12), (13, -8), (11, -4), (9, 0), (9, 4),
        (6, 5), (2, 6), (-4, 5), (-8, 5), (-12, 8), (-16, 12)]),
    ("ASIA", (234, 168, 134), [
        (38, 68), (45, 68), (52, 69), (60, 69), (68, 72), (75, 73), (82, 74),
        (90, 75), (98, 76), (105, 77), (112, 76), (120, 73), (128, 72),
        (135, 72), (142, 72), (150, 71), (158, 70), (165, 69), (170, 66),
        (178, 65), (175, 62), (170, 60), (162, 60), (158, 56), (156, 52),
        (150, 59), (145, 59), (142, 55), (140, 50), (137, 45), (134, 42),
        (130, 38), (127, 35), (124, 38), (121, 34), (119, 28), (114, 22),
        (110, 20), (108, 15), (106, 10), (104, 8), (102, 4), (100, 7), (98, 11),
        (95, 15), (92, 20), (89, 22), (86, 20), (82, 16), (80, 13), (77, 8),
        (75, 11), (73, 18), (70, 21), (67, 24), (64, 25), (61, 25), (58, 26),
        (55, 27), (52, 28), (50, 29), (48, 30), (45, 29), (42, 30), (40, 31),
        (38, 34), (36, 36), (33, 36), (30, 36), (27, 37), (26, 39), (28, 41),
        (30, 41), (33, 42), (36, 42), (39, 41), (41, 44), (38, 46), (35, 45),
        (32, 44), (30, 46), (28, 45), (30, 48), (34, 50), (38, 52), (42, 54),
        (45, 56), (47, 58), (45, 61), (42, 64), (40, 66)]),
    ("AUSTRALIA", (164, 190, 216), [
        (113, -22), (114, -28), (115, -34), (118, -35), (122, -34), (126, -32),
        (129, -32), (132, -32), (135, -35), (137, -35), (140, -38), (144, -38),
        (147, -39), (150, -37), (153, -32), (153, -27), (151, -24), (149, -20),
        (146, -19), (143, -15), (142, -11), (140, -14), (137, -12), (135, -14),
        (132, -12), (130, -13), (127, -14), (124, -16), (121, -18), (118, -20),
        (115, -21)]),
    ("INDONESIA", (234, 168, 134), [
        (95, 5), (98, 3), (100, 0), (102, -2), (105, -4), (108, -6), (110, -7),
        (113, -8), (116, -9), (119, -10), (122, -9), (125, -8), (128, -6),
        (131, -4), (134, -3), (137, -2), (140, -3), (140, -7), (137, -8),
        (134, -7), (131, -5), (128, -3), (125, -1), (122, 0), (119, 1),
        (116, 2), (113, 1), (110, 0), (107, 0), (104, 1), (101, 3), (98, 5)]),
    ("JAPAN", (234, 168, 134), [
        (130, 31), (131, 32), (133, 34), (135, 34), (137, 35), (139, 35),
        (140, 37), (141, 39), (141, 41), (142, 44), (141, 44), (140, 42),
        (139, 39), (137, 37), (135, 35), (133, 33), (131, 32)]),
    ("NZ", (164, 190, 216), [
        (167, -45), (168, -44), (170, -42), (172, -41), (174, -40), (175, -38),
        (177, -38), (178, -37), (176, -40), (174, -41), (172, -43), (170, -45),
        (168, -46)]),
]

# pins: (story num, lon, lat) — true locations, nudged only where two pins
# would overlap (London/The Hague, Crimea/Gaza).
MAP_PINS = [(1, -80, 26), (2, 30, 50), (3, -74, 41), (4, 30, 37), (5, -122, 37),
            (7, 85, 19), (8, 34, 31), (9, 47, 25), (10, 114, 22),
            (11, 25, 59), (13, -115, 36)]


def draw_map(draw, x, y, w, h):
    """World map from real lon/lat outlines, pins at true locations,
    title top-left, legend in one straight row, SPACE badge top-right."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 242))
    # faint graticule: every 30 deg lon / 20 deg lat
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360.0 * w
        draw.line([gx, y, gx, y + h], fill=(202, 220, 232), width=1)
    for lat in range(-40, 81, 20):
        gy = y + (83 - lat) / 141.0 * h
        draw.line([x, gy, x + w, gy], fill=(202, 220, 232), width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (83 - lat) / 141.0 * h)

    for name, col, poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly], fill=col,
                     outline=(255, 255, 255), width=1)
    # title
    draw.text((x + 10, y + 4), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=NAVY)
    # legend: one straight row, fixed gaps
    legend = [("N AMERICA", (132, 186, 152)), ("S AMERICA", (150, 196, 132)),
              ("EUROPE", (210, 188, 132)), ("AFRICA", (232, 190, 122)),
              ("ASIA", (234, 168, 134)), ("OCEANIA", (164, 190, 216))]
    lx = x + 10
    f_l = font(SANS, 9)
    for name, col in legend:
        draw.rectangle([lx, y + h - 14, lx + 9, y + h - 5], fill=col, outline=INK,
                       width=1)
        draw.text((lx + 12, y + h - 15), name, font=f_l, fill=INK)
        lx += 12 + int(draw.textlength(name, font=f_l)) + 14
    # pins at true locations
    for n, lon, lat in MAP_PINS:
        px, py = proj(lon, lat)
        pin(draw, px, py, n)
    # space badge top-right: pins 11 (Voyager) and 12 (Artemis)
    bx, by = x + w - 118, y + 6
    draw.rounded_rectangle([bx, by, bx + 108, by + 30], radius=8, fill=NAVY)
    draw.text((bx + 8, by + 8), "SPACE", font=font(SANS_B, 11), fill=(255, 206, 110))
    pin(draw, bx + 66, by + 15, 11, color=NAVY)
    pin(draw, bx + 94, by + 15, 12, color=NAVY)


# ------------------------------------------------------------ page layout
# Fixed grid: every band starts at a computed Y; nothing is hand-tuned.
M = 28  # margin
CW = W - 2 * M  # 968 content width


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.line([M, 20, W - M, 20], fill=RULE, width=2)
    centre(d, W // 2, 26, "THE DAY IN WORLD NEWS", font(SERIF_B, 46), NAVY)
    d.line([M, 78, W - M, 78], fill=RULE, width=1)
    centre(d, W // 2, 82,
           "FRIDAY, 20 NOVEMBER 2026  ·  45 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
           font(SANS_B, 12), INK)
    d.line([M, 100, W - M, 100], fill=RULE, width=2)
    d.line([M, 103, W - M, 103], fill=RULE, width=1)

    # ---- heroes: 3 equal columns, TALL panels (314x178, ~1.76:1),
    # one-line headlines at a UNIFORM size ----
    hy, hh = 110, 178
    gap_h = 12
    col_w = (CW - 2 * gap_h) // 3  # 314
    hero_hsize = uniform_size(d, [h[2] for h in HEROES], SERIF_B, 22, col_w)
    f_hero_head = font(SERIF_B, hero_hsize)
    f_hero_deck = font(SERIF, 12)
    panels = [draw_gta_panel, draw_kyiv_panel, draw_markets_panel]
    for i, (num, kick, head, deck, place) in enumerate(HEROES):
        x = M + i * (col_w + gap_h)
        panels[i](d, x, hy, col_w, hh)
        d.text((x, hy + hh + 5), kick, font=font(SANS_B, 10), fill=RED)
        d.text((x, hy + hh + 18), head, font=f_hero_head, fill=INK)
        draw_wrapped(d, x, hy + hh + 42, deck, f_hero_deck, col_w, (58, 62, 74),
                     leading=14, max_lines=3)
        # number badge, aligned with the kicker row
        d.ellipse([x + col_w - 18, hy + hh + 3, x + col_w, hy + hh + 21], fill=RED)
        f_n = font(SANS_B, 11)
        t = str(num)
        d.text((x + col_w - 9 - d.textlength(t, font=f_n) / 2, hy + hh + 5), t,
               font=f_n, fill=(255, 255, 255))
    d.line([M, 384, W - M, 384], fill=RULE, width=1)

    # ---- features: 2 rows x 5 equal cells, one-line headlines, uniform size ----
    gap_f = 10
    fw = (CW - 4 * gap_f) // 5  # 185
    feat_hsize = uniform_size(d, [f[2] for f in FEATURES], SERIF_B, 12, fw)
    f_feat_head = font(SERIF_B, feat_hsize)
    f_feat_deck = font(SERIF, 10)
    f_feat_kick = font(SANS_B, 9)

    def feature_row(fy, items):
        for j, (num, kick, head, deck) in enumerate(items):
            x = M + j * (fw + gap_f)
            draw_feature_icon(d, x, fy, fw, 46, FEATURE_KIND[num])
            d.text((x, fy + 50), f"{num:02d}  ·  {kick}", font=f_feat_kick, fill=RED)
            d.text((x, fy + 64), head, font=f_feat_head, fill=INK)
            draw_wrapped(d, x, fy + 80, deck, f_feat_deck, fw, (58, 62, 74),
                         leading=11, max_lines=3)
        return fy + 113

    fy = feature_row(392, FEATURES[:5])
    d.line([M, fy + 4, W - M, fy + 4], fill=(180, 178, 168), width=1)
    fy = feature_row(fy + 12, FEATURES[5:])
    d.line([M, fy + 4, W - M, fy + 4], fill=RULE, width=1)

    # ---- map ----
    my = fy + 12
    draw_map(d, M, my, CW, 135)

    # ---- briefs: two columns, fixed 12px rows, one line each ----
    by = my + 143
    d.line([M, by - 4, W - M, by - 4], fill=RULE, width=1)
    d.text((M, by), "THE DAY IN BRIEF", font=font(SANS_B, 12), fill=NAVY)
    by += 17
    col_w2 = (CW - 20) // 2  # 474
    f_bh = font(SERIF_B, 11)
    f_bn = font(SANS_B, 10)
    row_h = 12
    for ci in range(2):
        x = M + ci * (col_w2 + 20)
        yy = by
        for (num, head, deck) in BRIEFS[ci * 16:(ci + 1) * 16]:
            d.text((x, yy), f"{num:02d}", font=f_bn, fill=RED)
            d.text((x + 24, yy), head, font=f_bh, fill=INK)
            yy += row_h
        if ci == 0:
            d.line([M + col_w2 + 10, by, M + col_w2 + 10, by + 16 * row_h],
                   fill=(200, 198, 188), width=1)

    # ---- footer ----
    fy2 = by + 16 * row_h + 6
    d.line([M, fy2, W - M, fy2], fill=RULE, width=2)
    centre(d, W // 2, fy2 + 5,
           "Sources: Reuters  ·  AP  ·  AFP  ·  BBC  ·  Al Jazeera  ·  The Day in World News, Friday 20 November 2026",
           font(SANS, 10), GREY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
