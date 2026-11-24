"""Draw the news-image entry for make.fun news-image-20261123 (b174 heroes-scene).
THE WORLD TODAY, Monday 23 November 2026 — 31 stories.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

F_SERIF   = F("DejaVuSerif-Bold.ttf", 44)
F_DATE    = F("DejaVuSans-Bold.ttf", 15)
F_KICK    = F("DejaVuSans.ttf", 13)
F_NUM     = F("DejaVuSans-Bold.ttf", 20)
F_NUML    = F("DejaVuSans.ttf", 9)
F_REGION  = F("DejaVuSans-Bold.ttf", 12)
F_HHEAD   = F("DejaVuSans-Bold.ttf", 17)
F_BODY    = F("DejaVuSans.ttf", 11)
F_SRC     = F("DejaVuSans-Bold.ttf", 9)
F_CHIP    = F("DejaVuSans-Bold.ttf", 9)
F_MORE    = F("DejaVuSans-Bold.ttf", 13)
F_CAT     = F("DejaVuSans-Bold.ttf", 8)
F_CHEAD   = F("DejaVuSans-Bold.ttf", 11)
F_CBOD    = F("DejaVuSans.ttf", 10)
F_ALSO    = F("DejaVuSans.ttf", 10)
F_ALSOH   = F("DejaVuSans-Bold.ttf", 11)
F_DC_T    = F("DejaVuSans-Bold.ttf", 12)
F_DC      = F("DejaVuSans.ttf", 10)
F_DC_L    = F("DejaVuSans-Bold.ttf", 10)
F_FOOT    = F("DejaVuSans.ttf", 10)
F_BIG     = F("DejaVuSans-Bold.ttf", 34)
F_SCENE   = F("DejaVuSans-Bold.ttf", 13)
F_SCENE11 = F("DejaVuSans-Bold.ttf", 11)
F_GOLD    = F("DejaVuSans-Bold.ttf", 15)
F_BAR     = F("DejaVuSans-Bold.ttf", 12)
F_PIN     = F("DejaVuSans-Bold.ttf", 9)

INK    = (18, 18, 18)
PAPER  = (250, 248, 242)
NAVY   = (16, 32, 64)
NAVY2  = (24, 48, 96)
RED    = (178, 34, 34)
GOLD   = (212, 175, 55)
ORANGE = (232, 116, 30)
TEAL   = (14, 90, 100)
GREY   = (110, 110, 110)
LINE   = (200, 196, 188)

def fit(d, text, font, maxw):
    if d.textlength(text, font=font) <= maxw:
        return text
    while text and d.textlength(text + "\u2026", font=font) > maxw:
        text = text[:-1]
    return text + "\u2026"

def wrap(d, text, font, maxw, maxlines=2):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:maxlines]

def chip(d, x, y, text, fill):
    w = int(d.textlength(text, font=F_CHIP)) + 12
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    d.text((x + 6, y + 2), text, font=F_CHIP, fill=(255, 255, 255))
    return w

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 76], fill=INK)
    d.text((W // 2, 8), "THE WORLD TODAY", font=F_SERIF, fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 56), "MONDAY 23 NOVEMBER 2026", font=F_DATE, fill=GOLD, anchor="ma")

    # ---- kicker ----
    d.text((W // 2, 80), "23 November's world news, summed up in one page  \u2014  31 stories",
           font=F_KICK, fill=(60, 60, 60), anchor="ma")

    # ---- number strip: 5 cols x 2 rows, y 100..168 ----
    nums = [
        ("-3.3%", "KOSPI FALLS"), ("5.3", "US\u2013CHINA GAP"),
        ("11,762", "EBOLA CASES, DRC"), ("10T WON", "SEOUL FUND"),
        ("2%", "BILLIONAIRE TAX"), ("$450M", "SKUBAL DEAL"),
        ("165", "MISSILES / WEEK"), ("12,000", "CLEARED, MANCHESTER"),
        ("264 KG", "LEBANON SEIZURE"), ("$107.3B", "ANTHROPIC IPO"),
    ]
    d.rectangle([0, 100, W, 168], fill=(238, 234, 224))
    d.line([0, 100, W, 100], fill=LINE, width=1)
    d.line([0, 168, W, 168], fill=LINE, width=1)
    for i, (v, lab) in enumerate(nums):
        cx = (i % 5) * 204 + 8
        cy = 100 + (i // 5) * 34
        d.text((cx + 100, cy + 3), v, font=F_NUM, fill=NAVY, anchor="ma")
        d.text((cx + 100, cy + 24), lab, font=F_NUML, fill=(80, 80, 80), anchor="ma")
        if i % 5:
            d.line([cx, cy + 4, cx, cy + 30], fill=LINE, width=1)

    # ---- region bar ----
    d.rectangle([0, 168, W, 192], fill=NAVY)
    d.text((W // 2, 174), "ASIA-PACIFIC 7  \u00b7  AMERICAS 8  \u00b7  MIDDLE EAST 6  \u00b7  EUROPE 5  \u00b7  AFRICA 3  \u00b7  WORLD 2   \u2014   31 STORIES",
           font=F_REGION, fill=(255, 255, 255), anchor="ma")

    # ---- hero scenes: 3 cols, x 8/348/688, w 328, scene y 196..330 ----
    HX = [8, 348, 688]
    HW = 328
    SY0, SY1 = 196, 330
    for x in HX:
        d.rectangle([x, SY0, x + HW, SY1], outline=LINE, width=1)

    # hero 1: Kospi skyline + falling chart
    x = HX[0]
    d.rectangle([x, SY0, x + HW, SY1], fill=(10, 24, 52))
    # buildings along the bottom
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + HW - 10:
        bw = rnd.randint(18, 30)
        bh = rnd.randint(26, 52)
        d.rectangle([bx, SY1 - 24 - bh, bx + bw, SY1 - 24], fill=(30, 52, 96))
        for wy in range(SY1 - 24 - bh + 5, SY1 - 28, 9):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # caption band (solid navy) at bottom of scene
    d.rectangle([x, SY1 - 24, x + HW, SY1], fill=(6, 14, 34))
    d.text((x + 8, SY1 - 20), "KOSPI 4,708.54  \u00b7  -161 PTS  \u00b7  INTRADAY -5.8%",
           font=F_SCENE11, fill=(255, 255, 255))
    # big number in clear sky, top-left
    d.text((x + 10, SY0 + 6), "-3.3%", font=F_BIG, fill=(255, 255, 255))
    # falling chart line, routed right of the big number and below it
    pts = [(x + 150, SY0 + 22), (x + 195, SY0 + 40), (x + 235, SY0 + 34),
           (x + 275, SY0 + 58), (x + 315, SY0 + 78)]
    d.line(pts, fill=ORANGE, width=4)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=ORANGE)

    # hero 2: Guterres globe + flags
    x = HX[1]
    d.rectangle([x, SY0, x + HW, SY1], fill=(8, 44, 54))
    cx, cy, r = x + 78, SY0 + 62, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(26, 110, 130), outline=(120, 200, 210), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(120, 200, 210), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(120, 200, 210), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=(120, 200, 210), width=1)
    d.text((x + 140, SY0 + 18), "150 DELEGATES", font=F_GOLD, fill=GOLD)
    d.text((x + 140, SY0 + 40), "BRIDGETOWN", font=F_GOLD, fill=(255, 255, 255))
    d.text((x + 140, SY0 + 62), "SUMMIT", font=F_GOLD, fill=(255, 255, 255))
    d.text((x + 140, SY0 + 84), "BARBADOS", font=F_GOLD, fill=(255, 255, 255))
    # flags row at bottom of scene
    flag_cols = [(0, 90, 160), (200, 40, 40), (240, 200, 40), (40, 120, 200)]
    for i, col in enumerate(flag_cols):
        fx = x + 14 + i * 52
        d.rectangle([fx, SY1 - 22, fx + 40, SY1 - 8], fill=col, outline=(255, 255, 255), width=1)

    # hero 3: Asia Power Index bars
    x = HX[2]
    d.rectangle([x, SY0, x + HW, SY1], fill=(245, 243, 236))
    d.text((x + 10, SY0 + 6), "ASIA POWER INDEX 2026", font=F_SCENE, fill=INK)
    bars = [("US", 78.9, (30, 80, 180)), ("CHINA", 73.6, (180, 40, 40)), ("INDIA", 40.5, (220, 130, 30))]
    by = SY0 + 30
    for name, val, col in bars:
        d.text((x + 10, by + 1), name, font=F_BAR, fill=INK)
        bw = int(val * 2.1)
        d.rectangle([x + 74, by, x + 74 + bw, by + 15], fill=col)
        d.text((x + 74 + bw + 6, by + 1), str(val), font=F_BAR, fill=INK)
        by += 24
    d.text((x + 10, by + 4), "GAP 5.3 \u2014 NARROWEST SINCE 2018", font=F_BAR, fill=RED)

    # ---- hero headlines below scenes, y 336..418 ----
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi sheds 161 points as chip stocks slide; Samsung -3.1%, SK Hynix -2.5%.",
         "REUTERS", "REPORTED"),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "150 delegates back a risk framework in Bridgetown; a blueprint, not a treaty.",
         "AP", "REPORTED"),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6; US diplomatic influence -6 to 76.7.",
         "BLOOMBERG", "REPORTED"),
    ]
    for i, (head, body, src, ch) in enumerate(heroes):
        x = HX[i]
        lines = wrap(d, head, F_HHEAD, HW)
        yy = 336
        for ln in lines:
            d.text((x, yy), ln, font=F_HHEAD, fill=INK)
            yy += 20
        blines = wrap(d, body, F_BODY, HW)
        for ln in blines:
            d.text((x, yy), ln, font=F_BODY, fill=(60, 60, 60))
            yy += 14
        d.text((x, 402), src, font=F_SRC, fill=GREY)
        cw = int(d.textlength(ch, font=F_CHIP)) + 12
        chip(d, x + HW - cw - 2, 400, ch, (40, 120, 60))

    # ---- MORE OF THE DAY strip ----
    d.rectangle([0, 420, W, 444], fill=INK)
    d.text((12, 426), "MORE OF THE DAY", font=F_MORE, fill=(255, 255, 255))

    # ---- 10 cards: 5 cols x 2 rows, y 448..560 ----
    cards = [
        ("MARKETS", "Bessent presses Nvidia", "Treasury presses chipmaker.", "REUTERS", "REPORTED"),
        ("TECH", "FBI probes NCIC hack", "Breach under investigation.", "AP", "REPORTED"),
        ("WORLD", "Trump: Iran strikes loom", "Action possible in New Year.", "REUTERS", "REPORTED"),
        ("MARKETS", "Nasdaq futures +3%", "Thanksgiving week lifts US futures.", "BLOOMBERG", "REPORTED"),
        ("SPORT", "Skubal's $450M Mets deal", "Cy Young winner, nine-year pact.", "AP", "REPORTED"),
        ("OBITUARY", "Tom Jackson dies at 75", "NFL star, broadcaster, mourned.", "AP", "REPORTED"),
        ("TECH", "States sue SpaceX on AI", "States challenge safety ads.", "REUTERS", "REPORTED"),
        ("TECH", "Anthropic IPO: $107.3B", "Raised at $83; debut $97.17.", "BLOOMBERG", "REPORTED"),
        ("WORLD", "Poland: missiles crossed", "Kh-101s entered airspace.", "REUTERS", "CLAIM"),
        ("DEFENCE", "Nuclear satellite warning", "US: Moscow may orbit weapon.", "AP", "CLAIM"),
    ]
    CW, CH = 195, 54
    for i, (cat, head, body, src, ch) in enumerate(cards):
        cx = 8 + (i % 5) * 203
        cy = 448 + (i // 5) * 58
        d.rectangle([cx, cy, cx + CW, cy + CH], outline=LINE, width=1, fill=(255, 255, 255))
        d.text((cx + 6, cy + 3), cat, font=F_CAT, fill=RED)
        assert d.textlength(head, font=F_CHEAD) <= CW - 12, "headline too long: " + head
        assert d.textlength(body, font=F_CBOD) <= CW - 12, "body too long: " + body
        d.text((cx + 6, cy + 14), head, font=F_CHEAD, fill=INK)
        d.text((cx + 6, cy + 28), body, font=F_CBOD, fill=(60, 60, 60))
        d.text((cx + 6, cy + 41), src, font=F_SRC, fill=GREY)
        cw = int(d.textlength(ch, font=F_CHIP)) + 12
        chip(d, cx + CW - cw - 6, cy + 39, ch, (40, 120, 60) if ch == "REPORTED" else RED)

    # ---- map + ALSO, y 564..856 ----
    d.text((8, 566), "WHERE IT HAPPENED", font=F_ALSOH, fill=INK)
    d.text((516, 566), "ALSO ON MONDAY", font=F_ALSOH, fill=INK)
    # map panel
    d.rectangle([8, 584, 500, 856], outline=LINE, width=1, fill=(232, 238, 240))
    # blobs
    d.ellipse([18, 592, 165, 800], fill=(190, 205, 190))          # Americas
    d.ellipse([175, 592, 492, 762], fill=(190, 205, 190))         # Eurasia
    d.ellipse([228, 738, 348, 852], fill=(190, 205, 190))         # Africa
    pins = [
        (1, "Seoul", 445, 640), (2, "Bridgetown", 100, 762), (3, "Washington", 80, 640),
        (4, "Paris", 215, 645), (5, "Manchester", 198, 622), (6, "Warsaw", 268, 628),
        (7, "Kyiv", 305, 645), (8, "Beirut", 322, 692), (9, "Gaza", 306, 708),
        (10, "Bahrain", 338, 712), (11, "Benghazi", 282, 722), (12, "Khartoum", 298, 772),
        (13, "Kinshasa", 272, 800),
    ]
    for n, name, px, py in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py - 1), str(n), font=F_PIN, fill=(255, 255, 255), anchor="mm")
    # legend, 3 rows at bottom of map panel
    leg = ["1 Seoul  2 Bridgetown  3 Washington  4 Paris",
           "5 Manchester  6 Warsaw  7 Kyiv  8 Beirut",
           "9 Gaza  10 Bahrain  11 Benghazi  12 Khartoum  13 Kinshasa"]
    ly = 812
    for row in leg:
        d.text((16, ly), row, font=F_NUML, fill=(50, 50, 50))
        ly += 13

    # ALSO list: 2 cols x 9 rows
    also = [
        "Paris: 100+ back 2% billionaire tax",
        "Manchester: 12,000 cleared after scare",
        "Zelenskyy: 165 missiles in a week",
        "COP31: day after Antalya pact rejected",
        "Israel unity talks resume",
        "Gaza: two killed in Israeli strike",
        "West Bank settler attacks",
        "Iran war: no deal in sight",
        "Lebanon seizes 264 kg explosives",
        "Bahrain: strike hits plant, 2 hurt",
        "Benghazi: UN demands probe [CLAIM]",
        "Sudan: defences down drones [CLAIM]",
        "DRC: fighting traps Ebola teams",
        "Bangladesh: Hasina jailed if she returns",
        "Seoul minister quits over exam chaos",
        "SK Telecom -7.3%",
        "China eases margin rules to 80%",
        "Seoul readies 10T-won fund",
    ]
    for i, item in enumerate(also):
        col = i // 9
        row = i % 9
        ax = 516 + col * 252
        ay = 588 + row * 29
        d.text((ax, ay), fit(d, item, F_ALSO, 244), font=F_ALSO, fill=INK)

    # ---- DATE CHECK red box, y 864..964 ----
    d.rectangle([8, 864, 1016, 964], outline=RED, width=2, fill=(253, 238, 238))
    d.text((16, 870), "DATE CHECK \u2014 LEFT OUT (NOT 23 NOV)", font=F_DC_T, fill=RED)
    left_out = [
        "Democrats reach 258 (22 Nov)", "Sparta II fire (22 Nov)",
        "El Chapo Isidro captured (22 Nov)", "EU\u2013Indonesia pact (21 Nov)",
        "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)",
    ]
    for i, item in enumerate(left_out):
        lx = 16 + (i % 3) * 330
        ly = 890 + (i // 3) * 16
        d.text((lx, ly), "\u2022 " + item, font=F_DC, fill=INK)
    d.text((16, 922), "NOT YET:", font=F_DC_L, fill=RED)
    not_yet = [
        "Dymer search continues (14 missing)", "4 House races uncalled",
        "COP32 venue not set", "WHO evacuating trapped Ebola staff",
    ]
    for i, item in enumerate(not_yet):
        lx = 16 + (i % 2) * 500
        ly = 936 + (i // 2) * 14
        d.text((lx, ly), "\u2022 " + item, font=F_DC, fill=INK)

    # ---- footer ----
    d.text((8, 972), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 Yonhap \u00b7 wires \u2014 23 Nov 2026",
           font=F_FOOT, fill=(90, 90, 90))
    d.text((8, 990), "REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim",
           font=F_FOOT, fill=(90, 90, 90))

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    main()
