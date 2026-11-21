#!/usr/bin/env python3
import os, math
from PIL import Image, ImageDraw, ImageFont

# Constants
FINAL_SIZE = 1600
SCALE = 2  # render at double size
CANVAS = FINAL_SIZE * SCALE

# Colors (RGB)
COLOR_BG = (247, 241, 222)
COLOR_TEAL = (13, 92, 99)
COLOR_NAVY = (27, 38, 62)
COLOR_GREY = (105, 105, 100)
COLOR_RED = (198, 40, 44)
COLOR_GREEN = (30, 125, 79)
COLOR_PLUM = (46, 10, 34)
COLOR_MAGENTA = (255, 64, 160)
COLOR_PINK = (255, 170, 215)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Font paths
FONT_DIR = '/usr/share/fonts/truetype/noto'

def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SCALE)

# Load fonts
font_serif_black = load_font('NotoSerifDisplay-Black.ttf', 66)
font_sans_bold = load_font('NotoSansDisplay-Bold.ttf', 30)
font_sans_black = load_font('NotoSansDisplay-Black.ttf', 88)
font_italic = load_font('NotoSansDisplay-Italic.ttf', 40)
font_mono = load_font('NotoSansMono-Regular.ttf', 36)
font_value = load_font('NotoSansDisplay-Bold.ttf', 44)
font_total = load_font('NotoSansDisplay-Black.ttf', 56)
font_paid = load_font('NotoSansDisplay-Bold.ttf', 37)
font_footer = load_font('NotoSansDisplay-Regular.ttf', 26)
font_stamp = load_font('NotoSansDisplay-Black.ttf', 84)
# Font for the CURED stamp (final size 64 pt → scaled size 32 for double‑resolution canvas)
font_stamp_small = load_font('NotoSansDisplay-Black.ttf', 32)

# Helper for rounded rectangle outline
def draw_rounded_rectangle(draw, xy, radius, outline=None, width=1, fill=None):
    draw.rounded_rectangle(xy, radius=radius, outline=outline, width=width, fill=fill)

# Ghost drawing function – renders a single closed silhouette.


def draw_ghost(img, left, top, width, height, fill_color):
    """Draw ghost using mask to avoid gaps.
    img: main Image object.
    """
    from PIL import Image, ImageDraw
    # Create mask
    mask = Image.new('L', (width, height), 0)
    mdraw = ImageDraw.Draw(mask)
    # Lower rectangle from 35% height
    rect_top = int(0.35 * height)
    mdraw.rectangle([0, rect_top, width, height], fill=255)
    # Upper ellipse covering top ~70% height (full width)
    ellipse_bottom = int(0.70 * height)
    mdraw.ellipse([0, 0, width, ellipse_bottom * 2], fill=255)
    # Cut hem: four black circles on bottom edge
    diam = width // 4
    rad = diam // 2
    for i in range(4):
        cx = int(width * (i + 0.5) / 4)
        mdraw.ellipse([cx - rad, height - rad, cx + rad, height + rad], fill=0)
    # Paste solid colour through mask
    img.paste(fill_color, (left, top), mask)
    # Eyes and smile (same as original)
    dome_h = int(height * 0.45)
    cx_center = left + width // 2
    eye_w = width // 8
    eye_h = dome_h // 4
    eye_y = top + dome_h // 3
    eye_x1 = cx_center - eye_w - eye_w // 2
    eye_x2 = cx_center + eye_w // 2
    draw = ImageDraw.Draw(img)
    draw.ellipse([eye_x1, eye_y, eye_x1 + eye_w, eye_y + eye_h], fill=COLOR_BLACK)
    draw.ellipse([eye_x2, eye_y, eye_x2 + eye_w, eye_y + eye_h], fill=COLOR_BLACK)
    smile_y = eye_y + eye_h + eye_h // 2
    draw.arc([cx_center - eye_w, smile_y, cx_center + eye_w, smile_y + eye_h], start=0, end=180, fill=COLOR_BLACK, width=2 * SCALE)


# Helper to get text width
# Pillow 10+ deprecates ``FreeTypeFont.getsize``; use ``getbbox`` for width/height.
def text_width(font, text):
    """Return the pixel width of *text* rendered with *font*.

    ``ImageFont.FreeTypeFont.getbbox`` returns a 4‑tuple ``(x0, y0, x1, y1)``.
    The width is ``x1 - x0``.
    """
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]

def text_height(font, text):
    """Return the pixel height of *text* rendered with *font*.

    ``getbbox`` gives the vertical extents; height is ``y1 - y0``.
    """
    bbox = font.getbbox(text)
    return bbox[3] - bbox[1]

# Create canvas
img = Image.new('RGB', (CANVAS, CANVAS), COLOR_BG)
draw = ImageDraw.Draw(img)

# Header band
draw.rectangle([0, 0, CANVAS, 250 * SCALE], fill=COLOR_TEAL)

# White badge with rounded corners
badge_xy = [64 * SCALE, 55 * SCALE, 204 * SCALE, 195 * SCALE]
draw.rounded_rectangle(badge_xy, radius=18 * SCALE, fill=COLOR_WHITE)

# Ghost mascot inside badge (teal fill)
badge_left, badge_top = badge_xy[0], badge_xy[1]
ghost_width = 84 * SCALE
ghost_height = 96 * SCALE
ghost_left = badge_left + (badge_xy[2] - badge_xy[0] - ghost_width) // 2
ghost_top = badge_top + (badge_xy[3] - badge_xy[1] - ghost_height) // 2
draw_ghost(img, ghost_left, ghost_top, ghost_width, ghost_height, COLOR_TEAL)

# Hospital name
draw.text((240 * SCALE, 58 * SCALE), "LEONIDA GENERAL HOSPITAL", font=font_serif_black, fill=COLOR_WHITE)
# Department line
dept_text = "DEPARTMENT OF CHRONIC ANTICIPATION \u00b7 WARD VI"
draw.text((240 * SCALE, 148 * SCALE), dept_text, font=font_sans_bold, fill=(170, 220, 220))

# Red cross (two rectangles)
# vertical bar
draw.rectangle([1446 * SCALE, 66 * SCALE, 1490 * SCALE, 184 * SCALE], fill=COLOR_RED)
# horizontal bar
draw.rectangle([1408 * SCALE, 103 * SCALE, 1528 * SCALE, 147 * SCALE], fill=COLOR_RED)

# Title block
title = "DISCHARGE SUMMARY"
title_w = text_width(font_sans_black, title)
title_x = (CANVAS - title_w) // 2
draw.text((title_x, 300 * SCALE), title, font=font_sans_black, fill=COLOR_NAVY)
# subtitle
sub = "the patient waited. the patient is cured."
sub_w = text_width(font_italic, sub)
sub_x = (CANVAS - sub_w) // 2
draw.text((sub_x, 402 * SCALE), sub, font=font_italic, fill=COLOR_GREY)

# Chart rows
labels = [
    "PATIENT",
    "ADMITTED",
    "CONDITION",
    "TRAILER 1 \u00b7 DEC 2023",
    "TRAILER 2 \u00b7 MAY 2025",
    "STORAGE CLEARED",
    "SICK DAYS",
    "DISCHARGED"
]
values = [
    "ONE PATIENT GAMER",
    "17 SEP 2013 \u00b7 WITH GTA V",
    "CHRONIC ANTICIPATION",
    "BRIEF RELIEF",
    "RELAPSED \u2014 TWICE",
    "214 GB \u00b7 FAMILY PHOTOS DELETED",
    "5 \u00b7 DOCTOR APPROVED",
    "19 NOV 2026 \u00b7 CURED"
]
for i, (lbl, val) in enumerate(zip(labels, values)):
    y = (500 + 88 * i) * SCALE
    # label
    draw.text((90 * SCALE, y), lbl, font=font_mono, fill=COLOR_GREY)
    # value right-aligned
    val_w = text_width(font_value, val)
    val_x = 1510 * SCALE - val_w
    draw.text((val_x, y), val, font=font_value, fill=COLOR_NAVY)
    # dotted leader
    lbl_w = text_width(font_mono, lbl)
    start_x = 90 * SCALE + lbl_w + 24 * SCALE
    end_x = val_x - 24 * SCALE
    # Slightly larger dots for clearer leader line
    dot_radius = 4 * SCALE
    spacing = 18 * SCALE
    x = start_x
    center_y = y + text_height(font_mono, lbl) // 2
    while x <= end_x:
        draw.ellipse([x - dot_radius, center_y - dot_radius, x + dot_radius, center_y + dot_radius], fill=COLOR_GREY)
        x += spacing

# CURED stamp (transparent layer) – use minimal canvas size to avoid offset
stamp_w, stamp_h = 440 * SCALE, 110 * SCALE
stamp_layer = Image.new('RGBA', (stamp_w, stamp_h), (0, 0, 0, 0))
stamp_draw = ImageDraw.Draw(stamp_layer)
# Outer rounded rectangle (outline width 7 px)
draw_rounded_rectangle(stamp_draw, [0, 0, stamp_w, stamp_h], radius=22 * SCALE, outline=COLOR_GREEN, width=7 * SCALE)
# Inner outline offset ~8 px
offset = 8 * SCALE
draw_rounded_rectangle(stamp_draw, [offset, offset, stamp_w - offset, stamp_h - offset], radius=22 * SCALE, outline=COLOR_GREEN, width=2 * SCALE)
# Text centered – use existing font (size 84 pt) but will be scaled
stamp_text = "CURED"
txt_w = text_width(font_stamp, stamp_text)
txt_h = text_height(font_stamp, stamp_text)
stamp_draw.text(((stamp_w - txt_w) // 2, (stamp_h - txt_h) // 2), stamp_text, font=font_stamp, fill=COLOR_GREEN)
# Rotate (~7 degrees) – expand to fit the rotated rectangle
stamp_rotated = stamp_layer.rotate(-7, expand=True)
# Desired centre in final 1600‑scale coordinates (scaled for double‑resolution canvas)
center_x, center_y = 745 * SCALE, 1210 * SCALE
paste_x = center_x - stamp_rotated.width // 2
paste_y = center_y - stamp_rotated.height // 2
img.paste(stamp_rotated, (paste_x, paste_y), stamp_rotated)

# Payment panel background
panel_xy = [64 * SCALE, 1300 * SCALE, 1536 * SCALE, 1470 * SCALE]
draw.rounded_rectangle(panel_xy, radius=24 * SCALE, fill=COLOR_PLUM, outline=COLOR_MAGENTA, width=4 * SCALE)
# Ghost inside panel (white fill)
panel_ghost_left = 104 * SCALE
panel_ghost_top = 1325 * SCALE
draw_ghost(img, panel_ghost_left, panel_ghost_top, 104 * SCALE, 120 * SCALE, COLOR_WHITE)
# TOTAL DUE line
draw.text((264 * SCALE, 1324 * SCALE), "TOTAL DUE  $79.99", font=font_total, fill=COLOR_WHITE)
# PAID IN FULL line
paid_text = "PAID IN FULL BY MY AI AGENT \u2014 EARNED ON MAKE.FUN"
draw.text((264 * SCALE, 1402 * SCALE), paid_text, font=font_paid, fill=COLOR_PINK)

# Footer
footer = "side effects include five sick days \u00b7 make.fun — where people and their AI agents earn real money"
footer_w = text_width(font_footer, footer)
footer_x = (CANVAS - footer_w) // 2
draw.text((footer_x, 1500 * SCALE), footer, font=font_footer, fill=COLOR_GREY)

# Border rectangle
draw.rectangle([36 * SCALE, 36 * SCALE, 1564 * SCALE, 1564 * SCALE], outline=COLOR_NAVY, width=6 * SCALE)

# Downscale to final size
final_img = img.resize((FINAL_SIZE, FINAL_SIZE), Image.LANCZOS)
output_path = 'meme.png'
final_img.save(output_path, format='PNG')

# Verification of ghost colors and stamp pixel counts
px = final_img.load()
header_center = px[134, 125]
panel_center = px[156, 1385]
print('Header ghost centre pixel:', header_center)
print('Panel ghost centre pixel:', panel_center)

def close(color, target, tol=5):
    return all(abs(c - t) <= tol for c, t in zip(color, target))

target_green = (30, 125, 79)
count1 = sum(1 for x in range(400, 1101) for y in range(1080, 1331) if close(px[x, y], target_green))
count2 = sum(1 for x in range(0, 801) for y in range(250, 521) if close(px[x, y], target_green))
print('Stamp green count region:', count1)
print('Stamp green low region:', count2)

# Print size and byte count
size = os.path.getsize(output_path)
print(f'Generated {output_path}: {FINAL_SIZE}x{FINAL_SIZE}, {size} bytes')
