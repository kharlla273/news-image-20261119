#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page to entry.png.

A newspaper-style infographic: masthead naming the day, one lead story
with a drawn Vice City sunset scene, six story cards, and a briefs strip.
All text is drawn with PIL so it stays crisp and legible; every headline
is a real event reported on 19 November 2026 (verified via web search).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (176, 42, 32)
NAVY = (22, 50, 79)
GREY = (90, 86, 78)
RULE = (180, 172, 156)
CARD = (255, 255, 255)
SUNSET_TOP = (46, 24, 64)
SUNSET_MID = (196, 74, 60)
SUNSET_LOW = (244, 164, 96)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, w=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def draw_vice_city(d, x0, y0, x1, y1):
    """Sunset over a neon bay-city skyline: Vice City, home of GTA VI."""
    # gradient sky
    steps = 40
    for i in range(steps):
        t = i / steps
        if t < 0.5:
            u = t / 0.5
            c = tuple(int(SUNSET_TOP[k] + (SUNSET_MID[k] - SUNSET_TOP[k]) * u)
                      for k in range(3))
        else:
            u = (t - 0.5) / 0.5
            c = tuple(int(SUNSET_MID[k] + (SUNSET_LOW[k] - SUNSET_MID[k]) * u)
                      for k in range(3))
        yy0 = y0 + int(t * (y1 - y0))
        yy1 = y0 + int((t + 1 / steps) * (y1 - y0)) + 1
        d.rectangle([x0, yy0, x1, yy1], fill=c)
    # sun
    sx, sy = x0 + 0.68 * (x1 - x0), y0 + 0.42 * (y1 - y0)
    d.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=(255, 214, 130))
    d.ellipse([sx - 44, sy - 44, sx + 44, sy + 44], outline=(255, 214, 130), width=2)
    # stars in the upper sky
    for fx, fy in [(0.08, 0.08), (0.22, 0.05), (0.4, 0.12), (0.88, 0.06),
                   (0.55, 0.06), (0.95, 0.18), (0.3, 0.2)]:
        px, py = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    # skyline silhouettes
    base = y1 - 52
    skyline = [(0.00, 0.52, 0.10), (0.09, 0.70, 0.09), (0.17, 0.60, 0.08),
               (0.24, 0.78, 0.10), (0.33, 0.58, 0.07), (0.39, 0.72, 0.09),
               (0.47, 0.62, 0.08), (0.54, 0.80, 0.10), (0.63, 0.55, 0.08),
               (0.70, 0.68, 0.09), (0.78, 0.60, 0.08), (0.85, 0.74, 0.09),
               (0.93, 0.58, 0.07)]
    for fx, fh, fw in skyline:
        bx = x0 + fx * (x1 - x0)
        bw = fw * (x1 - x0)
        bh = fh * (base - y0)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(24, 14, 40))
        # lit windows
        for wy in range(int(base - bh + 8), int(base - 8), 14):
            for wx in range(int(bx + 5), int(bx + bw - 5), 12):
                if (int(wx) + int(wy)) % 29 < 9:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 196, 90))
    # bay water with reflections
    d.rectangle([x0, base, x1, y1], fill=(30, 32, 66))
    for i, wx in enumerate(range(x0 + 8, x1 - 12, 40)):
        d.line([(wx, base + 14 + (i % 3) * 10), (wx + 26, base + 14 + (i % 3) * 10)],
               fill=(255, 150, 110), width=2)
    # palm tree silhouettes
    for px, py, s in [(0.10, 0.88, 1.0), (0.24, 0.94, 0.8), (0.90, 0.90, 1.1)]:
        tx, ty = x0 + px * (x1 - x0), y0 + py * (y1 - y0)
        d.line([(tx, ty), (tx + 4 * s, ty - 52 * s)], fill=(16, 10, 28), width=5)
        for ang in (-70, -35, 0, 35, 70):
            a = math.radians(ang - 90)
            ex = tx + 4 * s + 26 * s * math.cos(a)
            ey = ty - 52 * s + 26 * s * math.sin(a)
            d.line([(tx + 4 * s, ty - 52 * s), (ex, ey)], fill=(16, 10, 28), width=4)


def icon_dome(d, x, y, s, c):
    d.rectangle([x, y + s * 0.75, x + s, y + s * 0.85], fill=c)
    d.rectangle([x + s * 0.1, y + s * 0.55, x + s * 0.9, y + s * 0.75], fill=c)
    d.arc([x + s * 0.15, y + s * 0.05, x + s * 0.85, y + s * 0.6], 180, 360,
          fill=c, width=4)
    d.line([(x + s * 0.5, y), (x + s * 0.5, y + s * 0.12)], fill=c, width=3)


def icon_scales(d, x, y, s, c):
    d.line([(x + s * 0.5, y + s * 0.1), (x + s * 0.5, y + s * 0.85)], fill=c, width=4)
    d.line([(x + s * 0.1, y + s * 0.25), (x + s * 0.9, y + s * 0.25)], fill=c, width=4)
    d.line([(x + s * 0.1, y + s * 0.25), (x + s * 0.02, y + s * 0.55)], fill=c, width=3)
    d.line([(x + s * 0.1, y + s * 0.25), (x + s * 0.18, y + s * 0.55)], fill=c, width=3)
    d.line([(x + s * 0.9, y + s * 0.25), (x + s * 0.82, y + s * 0.55)], fill=c, width=3)
    d.line([(x + s * 0.9, y + s * 0.25), (x + s * 0.98, y + s * 0.55)], fill=c, width=3)
    d.arc([x - s * 0.02, y + s * 0.45, x + s * 0.22, y + s * 0.7], 0, 180, fill=c, width=3)
    d.arc([x + s * 0.78, y + s * 0.45, x + s * 1.02, y + s * 0.7], 0, 180, fill=c, width=3)
    d.line([(x + s * 0.3, y + s * 0.85), (x + s * 0.7, y + s * 0.85)], fill=c, width=4)


def icon_globe(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=4)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=c, width=3)
    d.line([(x, y + s * 0.5), (x + s, y + s * 0.5)], fill=c, width=3)
    d.arc([x, y + s * 0.18, x + s, y + s * 0.82], 200, 340, fill=c, width=3)


def icon_cyclone(d, x, y, s, c):
    for r, a0, a1 in [(s * 0.5, 0, 200), (s * 0.36, 90, 300), (s * 0.22, 180, 360)]:
        d.arc([x + s / 2 - r, y + s / 2 - r, x + s / 2 + r, y + s / 2 + r],
              a0, a1, fill=c, width=4)


def icon_flame(d, x, y, s, c):
    d.polygon([(x + s * 0.5, y), (x + s * 0.85, y + s * 0.45),
               (x + s * 0.7, y + s * 0.7), (x + s * 0.9, y + s * 0.9),
               (x + s * 0.5, y + s), (x + s * 0.1, y + s * 0.9),
               (x + s * 0.3, y + s * 0.7), (x + s * 0.15, y + s * 0.45)], fill=c)


def icon_satellite(d, x, y, s, c):
    d.rectangle([x + s * 0.35, y + s * 0.35, x + s * 0.65, y + s * 0.65], fill=c)
    d.rectangle([x + s * 0.05, y + s * 0.4, x + s * 0.32, y + s * 0.6], outline=c, width=3)
    d.rectangle([x + s * 0.68, y + s * 0.4, x + s * 0.95, y + s * 0.6], outline=c, width=3)
    d.line([(x + s * 0.5, y + s * 0.35), (x + s * 0.8, y + s * 0.05)], fill=c, width=3)
    d.ellipse([x + s * 0.76, y, x + s * 0.86, y + s * 0.1], fill=c)


def card(draw, x, y, w, h, kicker, headline, body, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=RULE, width=1)
    draw.rounded_rectangle([x, y, x + w, y + 34], radius=10, fill=NAVY)
    draw.rectangle([x, y + 20, x + w, y + 34], fill=NAVY)
    icon(draw, x + 10, y + 5, 24, (255, 255, 255))
    draw.text((x + 44, y + 7), kicker, font=F_BOLD(15), fill=(255, 255, 255))
    ty = y + 44
    for line in wrap(draw, headline, F_BOLD(21), w - 28):
        draw.text((x + 14, ty), line, font=F_BOLD(21), fill=INK)
        ty += 26
    para(draw, x + 14, ty + 4, body, F_REG(16), w - 28, 21, fill=(60, 56, 48))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- Masthead ----
    rule(d, M, W - M, 30, 3, INK)
    d.text((M, 40), "THE WORLD IN ONE DAY", font=F_SERIF(52), fill=INK)
    d.text((M, 100), "THURSDAY  ·  19 NOVEMBER 2026", font=F_BOLD(27), fill=RED)
    rule(d, M, W - M, 138, 3, INK)
    rule(d, M, W - M, 143, 1, INK)

    # ---- Lead story ----
    ly = 158
    d.text((M, ly), "GAMING  —  LEAD STORY", font=F_BOLD(17), fill=RED)
    head = "After 13 years, Grand Theft Auto VI arrives"
    hy = ly + 28
    for line in wrap(d, head, F_BOLD(34), 560):
        d.text((M, hy), line, font=F_BOLD(34), fill=INK)
        hy += 40
    body = ("Rockstar's sequel rolls out at midnight local time around "
            "the world, from New Zealand onward, on PlayStation 5 and "
            "Xbox. Early reviews give it 99 on Metacritic, and "
            "pre-orders are put at about 16 million copies.")
    para(d, M, hy + 6, body, F_REG(19), 560, 26, fill=(60, 56, 48))
    draw_vice_city(d, 640, ly, W - M, ly + 236)

    # ---- Story grid ----
    gy = 420
    cw, ch, gap = 302, 204, 14
    stories = [
        ("WASHINGTON", "Democrats nominate Jeffries for Speaker",
         "House Democrats pick Hakeem Jeffries 251-11; if elected by "
         "the full House on 3 January, he would be the first Black "
         "Speaker.", icon_dome),
        ("THE HAGUE", "World court rules on Rohingya case today",
         "The ICJ delivers its judgment at 10 a.m. on whether Myanmar "
         "committed genocide against the Rohingya.", icon_scales),
        ("SHENZHEN", "Trump, Xi and Putin meet in China",
         "The three leaders hold trilateral talks on the APEC sidelines, "
         "on nuclear arms cuts and the US war with Iran.", icon_globe),
        ("WEATHER", "Cyclone Akvan nears India's east coast",
         "The Bay of Bengal storm is set to cross between Machilipatnam "
         "and Puri; railways are on alert.", icon_cyclone),
        ("THE GULF", "Iran widens attacks on Gulf bases",
         "Tehran targeted a US base in Kuwait and struck Bahrain again "
         "after US jets hit a missile site on Qeshm Island.", icon_flame),
        ("SPACE", "Voyager 1 reaches a light-day from Earth",
         "NASA is to confirm today that the probe, flying for nearly "
         "50 years, has passed the milestone.", icon_satellite),
    ]
    for i, (kick, head, body, icon) in enumerate(stories):
        x = M + (i % 3) * (cw + gap)
        y = gy + (i // 3) * (ch + gap)
        card(d, x, y, cw, ch, kick, head, body, icon)

    # ---- Briefs strip ----
    by = gy + 2 * ch + gap + 14
    rule(d, M, W - M, by, 2, INK)
    d.text((M, by + 8), "IN BRIEF", font=F_BOLD(17), fill=RED)
    briefs = [
        ("EUROPE", "EU proposes a €45bn loan for Ukraine, to be repaid once Russia pays reparations."),
        ("FAITH", "Pew: Islam is on track to become the world's largest religion by 2035."),
        ("MARKETS", "Fed minutes: most officials expect further interest-rate rises."),
        ("BRITAIN", "Modi meets the Prince and Princess of Wales and talks up UK–India ties."),
    ]
    col_w = 464
    for i, (kick, text) in enumerate(briefs):
        bx = M + (i % 2) * (col_w + 24)
        byy = by + 36 + (i // 2) * 46
        d.text((bx, byy), kick + " — ", font=F_BOLD(16), fill=NAVY)
        kw = d.textlength(kick + " — ", font=F_BOLD(16))
        para(d, bx + kw, byy, text, F_REG(16), col_w - kw, 19,
             fill=(60, 56, 48))

    # ---- Footer ----
    fy = H - 30
    rule(d, M, W - M, fy - 8, 1, RULE)
    d.text((M, fy), "THURSDAY 19 NOVEMBER 2026  ·  THE DAY IN ONE IMAGE",
           font=F_BOLD(15), fill=GREY)
    tag = "make.fun"
    d.text((W - M - d.textlength(tag, font=F_REG(15)), fy), tag,
           font=F_REG(15), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
