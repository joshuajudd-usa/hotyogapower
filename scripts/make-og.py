#!/usr/bin/env python3
"""
Generate the hotyogapower.com Open Graph image (1200x630).

Placeholder-grade but on-brand: cream ground with a warm dawn glow, the
HYP Yoga wordmark (serif, gold accent), a gold rule, and the tagline.
Uses Georgia (Cormorant Garamond's declared fallback) + Helvetica since
the brand woff2 files can't be read by PIL without fonttools. Replace with
a designed asset later — this script documents how the placeholder was made.

Run:  python3 scripts/make-og.py
Out:  images/og-image.png
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(__file__), "..", "images", "og-image.png")

# Brand palette
BG        = (250, 248, 245)   # #faf8f5 cream
GLOW      = (243, 232, 207)   # warm gold tint (top dawn light)
TEXT      = (44, 42, 38)      # #2c2a26
MUTED     = (107, 101, 96)    # #6b6560
ACCENT    = (184, 134, 11)    # #b8860b gold
ACCENT_SOFT = (212, 168, 67)  # #d4a843

def first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

SERIF_BOLD = first_existing([
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
])
SERIF_ITALIC = first_existing([
    "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
])
SANS = first_existing([
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
])

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

f_word = font(SERIF_BOLD, 150)
f_tag  = font(SERIF_ITALIC, 42)
f_label = font(SANS, 24)

# ── Background: cream with a soft dawn glow at top ──
img = Image.new("RGB", (W, H), BG)
# vertical gradient (glow -> bg) over the top ~60%
top = Image.new("RGB", (W, H), BG)
px = top.load()
span = int(H * 0.62)
for y in range(H):
    if y < span:
        t = y / span
        r = int(GLOW[0] + (BG[0] - GLOW[0]) * t)
        g = int(GLOW[1] + (BG[1] - GLOW[1]) * t)
        b = int(GLOW[2] + (BG[2] - GLOW[2]) * t)
    else:
        r, g, b = BG
    for x in range(W):
        px[x, y] = (r, g, b)
img = top

# soft radial highlight, top-center
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([W//2 - 460, -320, W//2 + 460, 360], fill=120)
glow = glow.filter(ImageFilter.GaussianBlur(140))
img.paste(Image.new("RGB", (W, H), GLOW), (0, 0), glow)

draw = ImageDraw.Draw(img)

def draw_tracked(text, cx, y, fnt, fill, tracking):
    widths = [fnt.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="lm")
        x += w + tracking

CX = W // 2

# Eyebrow label
draw_tracked("HOT YOGA POWER", CX, 168, f_label, ACCENT, 6)

# Wordmark: "HYP " in dark + "Yoga" in gold, centered as one line
part1, part2 = "HYP ", "Yoga"
w1 = f_word.getlength(part1)
w2 = f_word.getlength(part2)
start_x = CX - (w1 + w2) / 2
wy = 300
draw.text((start_x, wy), part1, font=f_word, fill=TEXT, anchor="lm")
draw.text((start_x + w1, wy), part2, font=f_word, fill=ACCENT, anchor="lm")

# Gold rule
draw.rectangle([CX - 44, 398, CX + 44, 401], fill=ACCENT_SOFT)

# Tagline
draw.text((CX, 470), "Study the classical texts. Embody the practice.",
          font=f_tag, fill=MUTED, anchor="mm")

img.save(OUT, "PNG")
print("wrote", os.path.normpath(OUT), img.size)
