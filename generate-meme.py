#!/usr/bin/env python3
"""Generate the GTA 6 meme for gta6-meme-x-01 (768x480 PNG).

Draws a Vice City sunset scene entirely in code (PIL) and pastes the
official make.fun ghost mark from the press kit (assets/mark-1024.png)
as the mascot cameo. No other downloaded images are used.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 768, 480
ROOT = Path(__file__).resolve().parent
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(draw):
    stops = [
        (0.00, (43, 16, 85)),    # deep purple dusk
        (0.35, (122, 28, 110)),  # magenta
        (0.58, (214, 51, 108)),  # hot pink
        (0.80, (255, 123, 61)),  # orange horizon
        (1.00, (255, 123, 61)),
    ]
    for y in range(310):
        t = y / 310
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                draw.line([(0, y), (W, y)], fill=lerp(c0, c1, f))
                break


def sun(draw):
    cx, cy, r = 545, 250, 82
    for mult, col in [(1.45, (255, 170, 80)), (1.18, (255, 205, 110))]:
        rr = int(r * mult)
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 160))
    # retro sun slats, lower half only
    for k, yy in enumerate(range(cy + 12, cy + r, 15)):
        half = int(math.sqrt(max(r * r - (yy - cy) ** 2, 0)))
        draw.rectangle([cx - half, yy, cx + half, yy + 4], fill=(255, 123, 61))


def ocean(draw):
    for y in range(310, 362):
        t = (y - 310) / 52
        draw.line([(0, y), (W, y)], fill=lerp((16, 120, 140), (8, 60, 90), t))
    for yy, alpha in [(322, 200), (338, 160), (352, 120)]:
        for x in range(0, W, 46):
            draw.arc([x, yy, x + 40, yy + 12], 180, 360,
                     fill=(255, 255, 255), width=3)


def sand(draw):
    for y in range(362, H):
        t = (y - 362) / (H - 362)
        draw.line([(0, y), (W, y)], fill=lerp((238, 205, 150), (214, 164, 110), t))


def palm(draw, x, base_y, h, lean, flip=False):
    """A dark palm silhouette: curved trunk + drooping fronds."""
    s = -1 if flip else 1
    top_x = x + lean * s
    top_y = base_y - h
    pts = []
    for i in range(21):
        t = i / 20
        px = x + (top_x - x) * t + math.sin(t * 1.6) * 10 * s
        py = base_y - h * t
        pts.append((px, py))
    draw.line(pts, fill=(24, 8, 40), width=12, joint="curve")
    for ang in range(-165, 16, 25):
        rad = math.radians(ang if not flip else 180 - ang)
        dx, dy = math.cos(rad), math.sin(rad)
        # quadratic bezier: out and drooping down
        cxp, cyp = top_x + dx * 55, top_y + dy * 30 - 16
        ex, ey = top_x + dx * 98, top_y + dy * 48 + 42
        curve = []
        for i in range(13):
            t = i / 12
            bx = (1 - t) ** 2 * top_x + 2 * (1 - t) * t * cxp + t * t * ex
            by = (1 - t) ** 2 * top_y + 2 * (1 - t) * t * cyp + t * t * ey
            curve.append((bx, by))
        draw.line(curve, fill=(24, 8, 40), width=7, joint="curve")
    # coconuts
    draw.ellipse([top_x - 12, top_y + 2, top_x - 2, top_y + 12], fill=(24, 8, 40))
    draw.ellipse([top_x + 2, top_y + 4, top_x + 12, top_y + 14], fill=(24, 8, 40))


def caption(draw, text, y, size, fill=(255, 255, 255)):
    font = ImageFont.truetype(BOLD, size)
    # wrap to fit width
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= W - 36:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    total = sum(draw.textbbox((0, 0), ln, font=font)[3] + 6 for ln in lines)
    yy = y
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        x = (W - (bbox[2] - bbox[0])) / 2 - bbox[0]
        draw.text((x, yy), ln, font=font, fill=fill,
                  stroke_width=6, stroke_fill=(0, 0, 0))
        yy += bbox[3] + 6
    return yy


def old_ghost_gags(draw):
    """The ghost waited so long it grew old: beard, cane, cobweb."""
    # long wizard beard: narrow at the chin, pointed at the bottom
    pts = [(352, 288), (418, 288)]
    for i in range(9):
        t = i / 8
        x = 418 + 22 * math.sin(t * math.pi * 0.5)
        y = 288 + 107 * t
        pts.append((x, y))
    pts.append((385, 398))  # tip, just above the bottom caption
    for i in range(8, -1, -1):
        t = i / 8
        x = 352 - 22 * math.sin(t * math.pi * 0.5)
        y = 288 + 107 * t
        pts.append((x, y))
    draw.polygon(pts, fill=(245, 245, 240))
    # strands fanning out from the chin
    for ex in (340, 360, 385, 410, 430):
        draw.line([(385, 296), (ex, 388)], fill=(212, 212, 207), width=2)

    # walking cane on the ghost's right
    draw.line([(512, 300), (512, 388)], fill=(139, 90, 43), width=6)
    draw.arc([496, 282, 528, 314], 180, 360, fill=(139, 90, 43), width=6)

    # cobweb on the ghost's head
    cx, cy = 306, 148
    for ang in (0, 22, 45, 67, 90):
        rad = math.radians(ang)
        ex, ey = cx + math.cos(rad) * 42, cy + math.sin(rad) * 42
        draw.line([(cx, cy), (ex, ey)], fill=(205, 205, 205), width=2)
    for r in (16, 30):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 0, 90,
                 fill=(205, 205, 205), width=2)


def skeleton(draw, x, y):
    """Someone who waited even longer: a skeleton sitting on the sand."""
    draw.ellipse([x - 34, y + 56, x + 34, y + 64], fill=(180, 125, 80))
    # skull
    draw.ellipse([x - 20, y - 26, x + 20, y + 8], fill=(240, 240, 230))
    draw.ellipse([x - 13, y - 16, x - 3, y - 6], fill=(20, 20, 20))
    draw.ellipse([x + 3, y - 16, x + 13, y - 6], fill=(20, 20, 20))
    draw.polygon([(x - 3, y - 2), (x + 3, y - 2), (x, y + 4)], fill=(20, 20, 20))
    for tx in (-10, -3, 4, 11):
        draw.line([(x + tx, y + 8), (x + tx, y + 14)], fill=(20, 20, 20), width=2)
    # spine + ribs
    draw.line([(x, y + 14), (x, y + 50)], fill=(240, 240, 230), width=5)
    for ry in (22, 32, 42):
        draw.arc([x - 18, y + ry, x + 18, y + ry + 12], 0, 180,
                 fill=(240, 240, 230), width=3)
    # arms resting + crossed legs
    draw.line([(x - 14, y + 24), (x - 30, y + 48)], fill=(240, 240, 230), width=4)
    draw.line([(x + 14, y + 24), (x + 30, y + 48)], fill=(240, 240, 230), width=4)
    draw.line([(x - 8, y + 50), (x - 34, y + 60)], fill=(240, 240, 230), width=5)
    draw.line([(x + 8, y + 50), (x + 34, y + 60)], fill=(240, 240, 230), width=5)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw)
    sun(draw)
    ocean(draw)
    sand(draw)
    palm(draw, 52, 400, 210, 55)
    palm(draw, 716, 410, 230, 60, flip=True)

    # ghost mascot on the sand, centre stage
    ghost = Image.open(ROOT / "assets" / "mark-1024.png").convert("RGBA")
    g = 225
    ghost = ghost.resize((g, g), Image.LANCZOS)
    draw.ellipse([W // 2 - 85, 348, W // 2 + 85, 362], fill=(180, 125, 80))
    img.paste(ghost, (W // 2 - g // 2, 128), ghost)

    # the wait made the ghost old — and someone waited even longer
    old_ghost_gags(draw)
    skeleton(draw, 648, 372)

    caption(draw, "ME, WAITING 13 YEARS FOR GTA 6", 18, 50)
    caption(draw, "AT LEAST THE GHOST GOT PAID", 392, 44)
    caption(draw, "ON make.fun", 436, 44)

    img.save(ROOT / "meme.png", "PNG")
    print("wrote", ROOT / "meme.png", img.size)


if __name__ == "__main__":
    main()
