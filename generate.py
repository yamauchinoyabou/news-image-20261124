"""Draws assets/entry.png (build-time only; needs Pillow and Noto fonts)."""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/usr/share/fonts/truetype/noto/"
PAPER, INK, GREY, RULE = "#FBF8F1", "#16181D", "#4A4E57", "#16181D"
REG = {"Europe": "#1F4E9E", "Middle East": "#8A3B12", "Africa": "#1C6B3A", "Asia": "#A3172E",
       "Americas": "#5B2A86", "Oceania": "#0B6470", "World/space": "#3A3F4B"}
TAGC = {"CONFIRMED": "#14532D", "OFFICIAL": "#1E3A8A", "REPORTED": "#7A4A00", "CLAIM": "#9B1C1C"}

_c = {}
def F(name, size):
    if (name, size) not in _c:
        _c[name, size] = ImageFont.truetype(FD + name + ".ttf", size)
    return _c[name, size]
def serif(s): return F("NotoSerif-CondensedBold", s)
def head(s): return F("NotoSans-CondensedBold", s)
def body(s): return F("NotoSans-Condensed", s)
def med(s): return F("NotoSans-CondensedMedium", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(t, f, w):
    out, cur = [], ""
    for x in t.split():
        n = (cur + " " + x).strip()
        if d.textlength(n, font=f) <= w:
            cur = n
        else:
            out.append(cur); cur = x
    return out + [cur]

def para(x, y, t, f, w, lh, fill=INK, maxlines=9):
    ls = wrap(t, f, w)
    assert len(ls) <= maxlines, (t, ls)
    for l in ls:
        assert d.textlength(l, font=f) <= w, l
        d.text((x, y), l, font=f, fill=fill, anchor="ls")
        y += lh
    return y

def badge(x, y, t, col, f, h=15):
    """Filled label, left-middle anchored at x,y. Returns right edge."""
    w = d.textlength(t, font=f) + 8
    d.rectangle((x, y - h // 2, x + w, y - h // 2 + h), fill=col)
    d.text((x + 4, y + 0.5), t, font=f, fill="white", anchor="lm")
    return x + w

def pin(x, y, n, col, r=9):
    d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline="white", width=1)
    d.text((x, y), str(n), font=head(13 if n < 10 else 12), fill="white", anchor="mm")

def scene(box, fn, S=4):
    """Draw a small picture at 4x and shrink it for smooth edges."""
    x0, y0, x1, y1 = box
    im = Image.new("RGB", ((x1 - x0) * S, (y1 - y0) * S), PAPER)
    dd = ImageDraw.Draw(im)
    fn(dd, lambda *a: tuple(v * S for v in a), S)
    img.paste(im.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))

# ---- stories -------------------------------------------------------------
PANELS = [
    (1, "Europe", "CONFIRMED", "Zaporizhzhia bombed; Putin vows reply",
     "Strike on a five-storey block kills 2 and wounds more than 40. Putin: retaliation for refinery strikes “inevitable”."),
    (2, "Americas", "CONFIRMED", "US jury convicts Huawei",
     "Guilty on 10 of 12 counts, trade-secret conspiracy and bank fraud among them; cleared of racketeering."),
    (3, "Middle East", "CONFIRMED", "Israel kills Hamas security chief",
     "Naeem Abu Nahel, head of internal security, dies in a Gaza City airstrike."),
    (4, "Oceania", "CONFIRMED", "Solomons to end China pact", "Reports: Beijing told the 2022 security deal won’t be renewed."),
    (5, "Africa", "CONFIRMED", "Senegal gets Africa Cup back", "Sport court CAS overturns award of the 2025 title to Morocco."),
    (6, "Americas", "CONFIRMED", "Hostages held in Colombia store", "Armoured-van raid fails in Cartagena; 10 freed by nightfall."),
    (7, "Asia", "CONFIRMED", "Russian planes spark Korea alert", "Ulleungdo island told to shelter; Seoul says airspace not entered."),
    (8, "World/space", "CONFIRMED", "First foreigner for Tiangong", "Pakistan’s Zeeshan Ali named on 24 Nov for Shenzhou-24. Lift-off 00:18 UTC 25 Nov, still 24 Nov in the Americas."),
    (9, "Middle East", "CONFIRMED", "Iraq to seize Kurd-held oilfields", "PM orders takeover in disputed areas; Kurdish side rejects it."),
    (10, "Africa", "CONFIRMED", "DR Congo rebels halt march", "Lubanga’s CRP pulls back near Bunia, citing Uganda-led talks."),
    (11, "Asia", "CONFIRMED", "Hasina plans 16 Dec return", "Bangladesh’s ousted PM faces a death sentence given in absentia."),
]
ALSO = [
    ("Europe", "OFFICIAL", "Poland: Russian drone briefly crossed its border"),
    ("Europe", "OFFICIAL", "England logs record heat-linked deaths: UKHSA"),
    ("Europe", "CONFIRMED", "Sarkozy, Carla Bruni to face witness-tampering trial"),
    ("Middle East", "CONFIRMED", "Turkish military helicopter crash kills five"),
    ("Middle East", "CONFIRMED", "UAE: bus hits parked truck, 13 dead"),
    ("Middle East", "CONFIRMED", "Israel: Eisenkot gets first coalition partner"),
    ("Middle East", "CLAIM", "Iran says more tankers hit Hormuz mines"),
    ("Africa", "CONFIRMED", "Nigeria’s central bank holds key rate at 23%"),
    ("Africa", "CONFIRMED", "S Africa convicts Zimbabwean bound for Russia’s war"),
    ("Africa", "REPORTED", "Contact lost with migrant boat from Senegal"),
    ("Asia", "CONFIRMED", "Hanoi restaurant gas blast kills at least six"),
    ("Asia", "CONFIRMED", "China Southern unit orders 50 Boeing 737s"),
    ("Asia", "CONFIRMED", "Japan to pay its 2027 ICC dues early"),
    ("Asia", "REPORTED", "Bangladesh police tear-gas garment protesters"),
    ("Americas", "OFFICIAL", "Cuba life expectancy down, first since 1950: WHO"),
    ("Americas", "CONFIRMED", "Dow closes above 50,000 as tech shares fall"),
    ("Americas", "CONFIRMED", "Argentina data point to technical recession"),
    ("Oceania", "CONFIRMED", "Australia: Labor-Greens deal on online-harm fines"),
    ("Oceania", "REPORTED", "Bougainville chiefs seek to block Panguna mine"),
    ("World/space", "OFFICIAL", "UN: 47,000 women and girls killed by partner or kin"),
    ("World/space", "CONFIRMED", "Landmine casualties at a five-year high"),
    ("World/space", "OFFICIAL", "Euclid finds most distant quasar yet: ESA"),
]
TALLY = {r: sum(p[1] == r for p in PANELS) + sum(a[0] == r for a in ALSO) for r in REG}
TOTAL = len(PANELS) + len(ALSO)
assert sum(TALLY.values()) == TOTAL and 28 <= TOTAL <= 34
for r, *_ in [(p[1],) for p in PANELS] + [(a[0],) for a in ALSO]:
    assert r in REG

# ---- masthead --------------------------------------------------------------
f = serif(66)
d.text((W / 2, 62), "Tuesday, 24 November 2026", font=f, fill=INK, anchor="ms")
d.rectangle((14, 78, 1010, 81), fill=RULE)
x = 14
d.text((x, 97), f"{TOTAL} stories · {len(REG)} regions", font=head(21), fill=INK, anchor="lm")
x += d.textlength(f"{TOTAL} stories · {len(REG)} regions", font=head(21)) + 16
for r, c in REG.items():
    x = badge(x, 97, f"{r} {TALLY[r]}", c, head(16), 22) + 7
d.line((14, 113, 1010, 113), fill=RULE, width=1)

# ---- scenes ----------------------------------------------------------------
def city(dd, p, S):
    dd.rectangle(p(0, 0, 300, 120), fill="#1B2440")
    for sx, sy in ((20, 14), (60, 30), (110, 12), (205, 20), (250, 38), (178, 42)):
        dd.ellipse(p(sx, sy, sx + 2, sy + 2), fill="#DDE3F3")
    dd.polygon(p(150, 60, 170, 18, 186, 6, 206, 10, 222, 26, 232, 60), fill="#59607A")
    dd.ellipse(p(138, 40, 178, 78), fill="#59607A")
    dd.ellipse(p(205, 30, 246, 72), fill="#59607A")
    dd.rectangle(p(20, 52, 96, 112), fill="#39456B")
    dd.polygon(p(112, 112, 112, 46, 150, 46, 156, 60, 166, 54, 176, 76, 188, 66, 198, 84, 210, 58, 260, 58, 260, 112), fill="#8C93AB")
    for r in range(4):
        for c in range(5):
            dd.rectangle(p(27 + c * 13, 58 + r * 13, 34 + c * 13, 66 + r * 13), fill="#F2C14E" if (r * 3 + c) % 4 == 0 else "#222C4C")
        for c in range(10):
            xx, yy = 118 + c * 14, 52 + r * 14
            if not (150 < xx < 214 and yy < 84) and yy > 60 - (xx < 148) * 12:
                dd.rectangle(p(xx, yy, xx + 8, yy + 8), fill="#222C4C")
    dd.polygon(p(164, 100, 170, 78, 177, 90, 184, 66, 192, 88, 199, 76, 206, 100), fill="#E4572E")
    dd.polygon(p(174, 100, 180, 88, 186, 80, 192, 92, 197, 100), fill="#F9C74F")
    dd.rectangle(p(0, 110, 300, 120), fill="#0E1426")

def chip(dd, p, S):
    dd.rectangle(p(0, 0, 100, 100), fill="#EFE7F6")
    for i in range(5):
        a = 26 + i * 12
        for q in ((a, 8, a + 4, 92), (8, a, 92, a + 4)):
            dd.rectangle(p(*q), fill="#8E6BB0")
    dd.rectangle(p(20, 20, 80, 80), fill="#2B1440")
    dd.line(p(50, 32, 50, 68), fill="white", width=3 * S)
    dd.line(p(32, 38, 68, 38), fill="white", width=3 * S)
    for c in (34, 66):
        dd.line(p(c, 38, c - 8, 55), fill="white", width=S); dd.line(p(c, 38, c + 8, 55), fill="white", width=S)
        dd.pieslice(p(c - 10, 48, c + 10, 64), 0, 180, fill="white")
    dd.rectangle(p(40, 67, 60, 70), fill="white")

def gaza(dd, p, S):
    dd.rectangle(p(0, 0, 100, 100), fill="#F3E2D3")
    dd.ellipse(p(62, 10, 84, 32), fill="#D98F4E")
    for q in ((6, 58, 28, 90), (32, 48, 54, 90), (72, 62, 94, 90)):
        dd.rectangle(p(*q), fill="#8A5A3C")
        for k in (0, 1):
            dd.rectangle(p(q[0] + 4, q[1] + 6 + 13 * k, q[0] + 9, q[1] + 13 + 13 * k), fill="#4A2A18")
            dd.rectangle(p(q[0] + 13, q[1] + 6 + 13 * k, q[0] + 18, q[1] + 13 + 13 * k), fill="#4A2A18")
    dd.ellipse(p(50, 44, 80, 72), fill="#6B6460"); dd.ellipse(p(44, 60, 68, 84), fill="#6B6460"); dd.ellipse(p(62, 58, 84, 84), fill="#6B6460")
    dd.polygon(p(54, 90, 58, 74, 63, 82, 67, 70, 72, 90), fill="#D7451F")
    dd.rectangle(p(0, 90, 100, 100), fill="#5A3720")

def frame(x0, y0, x1, y1, col):
    d.rectangle((x0, y0, x1, y1), outline="#C9C2B2", fill="#FFFFFF")
    d.rectangle((x0, y0, x1, y0 + 4), fill=col)

# lead
n, r, tag, h, b = PANELS[0]
frame(14, 120, 520, 352, REG[r])
scene((24, 132, 262, 252), lambda dd, p, S: city(dd, lambda *a: p(*(v - 20 * (k % 2 == 0) for k, v in enumerate(a))), S))
y = para(274, 166, h, serif(37), 242, 38, maxlines=3)
pin(34, 270, n, REG[r])
e = badge(50, 270, r.upper(), REG[r], head(13), 18)
badge(e + 5, 270, tag, TAGC[tag], head(13), 18)
para(24, 305, b, med(21), 488, 25, maxlines=2)

# two more large
for (n, r, tag, h, b), y0, sc in ((PANELS[1], 120, chip), (PANELS[2], 239, gaza)):
    frame(528, y0, 1010, y0 + 113, REG[r])
    scene((906, y0 + 9, 1004, y0 + 107), sc)
    yy = para(538, y0 + 34, h, head(27), 364, 28, maxlines=1)
    para(538, y0 + 56, b, med(16), 360, 19, maxlines=2)
    pin(547, y0 + 97, n, REG[r])
    e = badge(562, y0 + 97, r.upper(), REG[r], head(12), 16)
    badge(e + 5, y0 + 97, tag, TAGC[tag], head(12), 16)

# 8 medium
def icon(x, y, n):
    c = REG[PANELS[n - 1][1]]
    k = "#FFFFFF"
    def art(dd, p, S):
        L = lambda *a, w=2: dd.line(p(*a), fill=c, width=w * S)
        if n == 4:    # island and palm
            dd.ellipse(p(2, 24, 34, 40), fill=c); dd.rectangle(p(0, 32, 36, 40), fill=k)
            L(18, 26, 21, 10, w=3)
            for e in ((8, 8), (10, 16), (31, 7), (33, 15), (21, 2)):
                L(21, 10, *e)
        elif n == 5:  # trophy
            dd.rectangle(p(10, 3, 26, 12), fill=c); dd.pieslice(p(10, 2, 26, 23), 0, 180, fill=c)
            dd.arc(p(3, 4, 15, 16), 60, 300, fill=c, width=2 * S); dd.arc(p(21, 4, 33, 16), 240, 120, fill=c, width=2 * S)
            dd.rectangle(p(16, 20, 20, 29), fill=c); dd.rectangle(p(10, 29, 26, 33), fill=c)
        elif n == 6:  # trolley
            L(1, 5, 7, 5); L(7, 5, 12, 25); L(12, 25, 30, 25)
            dd.polygon(p(8, 9, 34, 9, 30, 20, 11, 20), fill=c)
            for a in (12, 25):
                dd.ellipse(p(a, 27, a + 6, 33), fill=c)
        elif n == 7:  # aircraft
            dd.polygon(p(18, 0, 21, 11, 35, 23, 35, 27, 21, 22, 20, 29, 25, 34, 11, 34, 16, 29, 15, 22, 1, 27, 1, 23, 15, 11), fill=c)
        elif n == 8:  # rocket
            dd.polygon(p(18, 0, 25, 10, 25, 25, 11, 25, 11, 10), fill=c)
            dd.polygon(p(11, 17, 4, 28, 11, 26), fill=c); dd.polygon(p(25, 17, 32, 28, 25, 26), fill=c)
            dd.ellipse(p(15, 9, 21, 15), fill=k); dd.polygon(p(14, 27, 22, 27, 18, 36), fill="#C2560C")
        elif n == 9:  # derrick
            L(18, 3, 7, 34); L(18, 3, 29, 34); L(12, 20, 24, 20); L(15, 12, 24, 20); L(12, 20, 27, 30); L(24, 20, 9, 30); L(4, 34, 32, 34)
            dd.rectangle(p(15, 0, 21, 4), fill=c)
        elif n == 10:  # turn-back arrow
            dd.arc(p(6, 8, 32, 34), 270, 110, fill=c, width=5 * S)
            dd.rectangle(p(12, 8, 19, 13), fill=c); dd.polygon(p(2, 10, 13, 1, 13, 20), fill=c)
        else:         # calendar page
            dd.rectangle(p(3, 5, 33, 34), outline=c, width=2 * S); dd.rectangle(p(3, 5, 33, 13), fill=c)
            dd.rectangle(p(9, 1, 12, 8), fill=c); dd.rectangle(p(24, 1, 27, 8), fill=c)
            dd.text(p(18, 23), "16", font=head(17 * S), fill=c, anchor="mm")
    old = img.getpixel((x, y))
    assert old == (255, 255, 255)
    im = Image.new("RGB", (36 * 4, 37 * 4), k)
    art(ImageDraw.Draw(im), lambda *a: tuple(v * 4 for v in a), 4)
    img.paste(im.resize((36, 37), Image.LANCZOS), (x, y))

for i, (n, r, tag, h, b) in enumerate(PANELS[3:]):
    x0 = 14 + (i % 4) * 250
    y0 = 358 + (i // 4) * 124
    frame(x0, y0, x0 + 246, y0 + 119, REG[r])
    if n == 8:
        para(x0 + 8, y0 + 26, h, head(24), 198, 23, maxlines=2)
    else:
        para(x0 + 8, y0 + 29, h, head(25), 198, 25, maxlines=2)
    icon(x0 + 206, y0 + 11, n)
    if n == 8:  # longer date note: three tighter lines
        para(x0 + 8, y0 + 67, b, med(13), 226, 14, INK, maxlines=3)
    else:
        para(x0 + 8, y0 + 72, b, med(15), 234, 17, INK, maxlines=2)
    pin(x0 + 16, y0 + 106, n, REG[r])
    e = badge(x0 + 30, y0 + 106, r.upper(), REG[r], head(12), 16)
    badge(e + 5, y0 + 106, tag, TAGC[tag], head(12), 16)

# ---- map -------------------------------------------------------------------
LAND = [  # own coarse outlines, lon/lat
    [(-166, 66), (-156, 71), (-128, 70), (-95, 72), (-82, 68), (-93, 60), (-80, 52), (-78, 60), (-64, 59), (-56, 52), (-66, 45), (-75, 38), (-81, 30), (-80, 25), (-84, 30), (-97, 28), (-97, 20), (-88, 21), (-84, 10), (-78, 8), (-86, 12), (-105, 20), (-114, 31), (-124, 40), (-124, 48), (-135, 58), (-152, 59), (-165, 55)],
    [(-78, 9), (-72, 12), (-60, 9), (-50, 1), (-35, -6), (-40, -20), (-48, -27), (-58, -37), (-66, -46), (-68, -55), (-75, -50), (-72, -30), (-71, -18), (-81, -5)],
    [(-55, 60), (-70, 76), (-30, 80), (-20, 72), (-40, 63)],
    [(-9, 37), (-9, 44), (-2, 44), (-4, 48), (8, 54), (5, 60), (12, 66), (26, 71), (42, 67), (60, 69), (80, 73), (105, 77), (140, 73), (180, 69), (178, 63), (162, 60), (156, 51), (142, 59), (135, 54), (140, 47), (129, 42), (129, 35), (125, 38), (121, 40), (121, 30), (110, 21), (107, 11), (100, 13), (103, 2), (98, 9), (97, 17), (90, 22), (80, 14), (77, 8), (72, 20), (66, 25), (57, 26), (50, 30), (56, 25), (59, 22), (45, 13), (39, 21), (34, 29), (36, 36), (27, 37), (23, 37), (19, 42), (13, 45), (18, 40), (15, 38), (9, 44), (3, 42), (-1, 37)],
    [(-6, 36), (10, 37), (20, 31), (32, 31), (43, 12), (51, 12), (40, -4), (40, -15), (35, -24), (27, -34), (18, -34), (12, -17), (13, -5), (9, 4), (-8, 5), (-17, 14), (-16, 22)],
    [(114, -22), (122, -18), (131, -12), (136, -12), (141, -12), (146, -19), (153, -28), (149, -38), (140, -37), (131, -32), (116, -35)],
    [(-5, 50), (1, 52), (-3, 58), (-6, 57)], [(131, 32), (140, 36), (145, 44), (140, 42), (136, 35)],
    [(96, 5), (105, -5), (116, -8), (104, -7)], [(109, 1), (117, 6), (118, 1), (114, -4)],
    [(131, -1), (141, -3), (150, -10), (138, -8)], [(44, -16), (50, -15), (47, -25), (44, -24)],
    [(172, -35), (178, -38), (167, -46), (173, -41)], [(120, 18), (126, 8), (122, 12)], [(-24, 64), (-14, 66), (-17, 63)],
]
def inside(x, y, poly):
    k = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            k = not k
    return k
MX, MY, MS = 14, 612, 1.16
def proj(lon, lat): return MX + (lon + 170) * MS, MY + (76 - lat) * MS
d.rectangle((14, 608, 430, 762), fill="#E9EFF2")
S = 4
m = Image.new("RGB", (416 * S, 154 * S), "#E9EFF2")
dm = ImageDraw.Draw(m)
st = 3.4
lat = 75.0
while lat > -54:
    lon = -169.0
    while lon < 186:
        if any(inside(lon, lat, q) for q in LAND):
            px, py = proj(lon, lat)
            px, py = (px - 14) * S, (py - 608) * S
            rr = 1.6 * S
            dm.ellipse((px - rr, py - rr, px + rr, py + rr), fill="#9AA6AE")
        lon += st
    lat -= st
img.paste(m.resize((416, 154), Image.LANCZOS), (14, 608))
PINS = {1: (35, 47.8, 0, -4), 2: (-92, 41, 0, 0), 3: (34.4, 31.5, -12, 4), 4: (160, -9, 0, 0), 5: (-17, 14.7, 0, 0),
        6: (-75.5, 10.4, 0, 0), 7: (131, 37.5, 0, 0), 8: (100, 41, 0, 0), 9: (44, 35.5, 8, 1), 10: (30, 1.5, 0, 0), 11: (90, 24, 0, 0)}
for n, r, *_ in PANELS:
    lo, la, dx, dy = PINS[n]
    x, y = proj(lo, la)
    d.line((x, y, x + dx, y + dy), fill=INK)
    pin(x + dx, y + dy, n, REG[r], 9)

# ---- day in numbers ----------------------------------------------------------
NUM = [("10 of 12", "counts Huawei was convicted on"), ("47,000", "women and girls killed by partner or kin, 2025 (UN est.)"),
       ("6,929", "landmine casualties in 2025, killed or hurt"), ("5,258", "heat-linked deaths in England, summer 2026"),
       ("50,018.70", "Dow Jones close, up 0.9%")]
d.rectangle((438, 608, 1010, 762), fill=INK)
d.text((448, 628), "DAY IN NUMBERS", font=head(19), fill="white", anchor="ls")
d.text((1002, 628), "each matched in 2+ outlets", font=body(14), fill="#D8D8D8", anchor="rs")
for i, (a, b) in enumerate(NUM):
    y = 653 + i * 25
    d.text((576, y), a, font=head(25), fill="#FFD166", anchor="rs")
    d.text((588, y - 1), b, font=body(17), fill="white", anchor="ls")

# ---- list --------------------------------------------------------------------
d.rectangle((14, 769, 1010, 771), fill=RULE)
d.text((14, 789), "ALSO ON TUESDAY", font=head(18), fill=INK, anchor="ls")
x = 220
d.text((x, 783), "HOW SURE", font=head(14), fill=INK, anchor="lm")
x += 74
for t, e in (("CONFIRMED", "2+ outlets"), ("OFFICIAL", "institution on record"), ("REPORTED", "1 outlet"), ("CLAIM", "one side’s account")):
    x = badge(x, 783, t, TAGC[t], head(12), 16) + 5
    d.text((x, 783), e, font=body(14), fill=INK, anchor="lm")
    x += d.textlength(e, font=body(14)) + 14
half = (len(ALSO) + 1) // 2
for i, (r, t, s) in enumerate(ALSO):
    x0 = 14 + (i // half) * 502
    y = 805 + (i % half) * 16
    d.rectangle((x0, y - 5, x0 + 7, y + 5), fill=REG[r])
    d.text((x0 + 12, y), r, font=head(13), fill=REG[r], anchor="lm")
    f = med(15)
    assert d.textlength(s, font=f) < 326, s
    d.text((x0 + 92, y), s, font=f, fill=INK, anchor="lm")
    w = d.textlength(t, font=head(11)) + 8
    badge(x0 + 494 - w, y, t, TAGC[t], head(11), 14)

# ---- footer --------------------------------------------------------------------
d.line((14, 980, 1010, 980), fill=RULE)
d.text((14, 995), "DATE CHECK", font=head(14), fill="#9B1C1C", anchor="ls")
T1 = ("Not counted, earlier day: Huang back at Nvidia, Women’s World Cup hosts, UK Myanmar sanctions, Murmansk governor held, Colombia")
T2 = ("car bomb (23 Nov); Benghazi warship strike (22 Nov); Mercury orbit, Indonesia factory fire (by 23 Nov). Later: Hodeidah port strike,")
T3 = ("Australia-Solomons treaty signing (25 Nov).")
full = " ".join((T1, T2, T3))
f = med(14)
words, line = full.split(), ""
first, k = 996 - 74, 0
while k < len(words) and d.textlength((line + " " + words[k]).strip(), font=f) <= first:
    line = (line + " " + words[k]).strip(); k += 1
d.text((88, 995), line, font=f, fill=INK, anchor="ls")
para(14, 1013, " ".join(words[k:]), f, 996, 16, INK, maxlines=1)

os.makedirs("assets", exist_ok=True)
img.quantize(256, dither=Image.Dither.NONE).save("assets/entry.png", optimize=True)
print(TOTAL, TALLY)
