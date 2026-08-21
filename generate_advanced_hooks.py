#!/usr/bin/env python3
"""Generate 5 advanced, fully distinct hook layouts — modern, no overflow/overlap, proper align."""
import os
from PIL import Image, ImageDraw, ImageFont
import terminal_video as tv

OUT_DIR = "hook_previews"
os.makedirs(OUT_DIR, exist_ok=True)

def load_bold(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size)
            except: pass
    return tv.FONT

HOOK_TITLE_SIZE = 68 * tv.RENDER_SCALE
HOOK_SUB_SIZE = 36 * tv.RENDER_SCALE
BOLD_TITLE = load_bold(HOOK_TITLE_SIZE)
BOLD_SUB = load_bold(HOOK_SUB_SIZE)
SMALL_BOLD = load_bold(34 * tv.RENDER_SCALE)

def draw_centered_pill(draw, text, font, fill, text_fill, cx, cy, pad_x=18, pad_y=10, radius=12):
    bw = tv.tw(draw, text, font)
    bh = tv.th(draw, text, font)
    x1 = cx - bw//2 - pad_x
    y1 = cy - bh//2 - pad_y
    x2 = cx + bw//2 + pad_x
    y2 = cy + bh//2 + pad_y
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius*tv.RENDER_SCALE, fill=fill)
    draw.text((cx - bw//2, cy - bh//2), text, font=font, fill=text_fill)
    return (x1,y1,x2,y2)

def draw_title_rows_centered(draw, segs, y0, max_w, font, lh, line_align="center"):
    """Helper: wrap segs and draw centered, returns total height and last y."""
    rows = tv.wrap_segments(segs, max_w, draw, font)
    for ri, rsegs in enumerate(rows):
        full_w = sum(tv.tw(draw, t, font) for t,_ in rsegs)
        if line_align == "center":
            x0 = (tv.RW - full_w)//2
        else:
            x0 = tv.PAD_X
        cx = x0
        y = y0 + ri*lh
        for txt, col in rsegs:
            draw.text((cx, y), txt, font=font, fill=col, stroke_width=0)
            cx += tv.tw(draw, txt, font)
    return len(rows)*lh, rows

# === 5 DISTINCT ADVANCED HOOKS ===

def hook1_mistake():
    """Formula: The Mistake — Stop saving passwords in notes."""
    tv.apply_theme("light")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # Top warning pill — yellow/black
    cx, cy = tv.RW//2, int(tv.RH*0.22)
    draw_centered_pill(draw, "  STOP DOING THIS  ", tv.FONT, (255,193,7), (30,32,35), cx, cy, pad_x=20, pad_y=12, radius=14)
    # Title stacked — 3 lines intentional
    title = "Stop saving passwords in notes"
    # Build colored segs: "Stop" accent, "passwords" red pill background will be drawn separately
    # For this hook we want 3 rows manually to avoid overflow:
    lines = ["Stop saving", "passwords", "in notes."]
    y0 = int(tv.RH*0.32)
    lh = int(HOOK_TITLE_SIZE*1.22)
    hf = BOLD_TITLE
    for i, line in enumerate(lines):
        y = y0 + i*lh
        if i == 1:
            # red pill behind "passwords"
            w = tv.tw(draw, line, hf)
            x0 = (tv.RW - w)//2
            draw.rounded_rectangle([x0-16, y-8, x0+w+16, y+lh-14], radius=12, fill=tv.ERROR_COLOR)
            draw.text((x0, y), line, font=hf, fill=(255,255,255))
        else:
            w = tv.tw(draw, line, hf)
            x0 = (tv.RW - w)//2
            col = tv.ACCENT if i==0 and "Stop" in line else (30,32,35)
            draw.text((x0, y), line, font=hf, fill=col)
    # sub
    sub = "You're one leak away — fix it in 60s."
    sub_y = y0 + 3*lh + 28
    draw.rectangle([tv.RW//2-60, sub_y-14, tv.RW//2+60, sub_y-10], fill=tv.ACCENT)
    sw = tv.tw(draw, sub, tv.HOOK_SUB_FONT)
    sx = (tv.RW - sw)//2
    draw.text((sx, sub_y), sub, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # CTAs
    keep = "FIX IT NOW  →"
    kw = tv.tw(draw, keep, tv.FONT)
    kx, ky = (tv.RW - kw)//2, sub_y + 54
    draw.rounded_rectangle([kx-18, ky-10, kx+kw+18, ky+30], radius=12, fill=tv.ACCENT)
    draw.text((kx, ky), keep, font=tv.FONT, fill=(255,255,255))
    return img

def hook2_question():
    """Formula: Question — Still using 123456?"""
    tv.apply_theme("github")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # Large faded "?" watermark
    q_font = load_bold(420 * tv.RENDER_SCALE)
    q = "?"
    qw = tv.tw(draw, q, q_font)
    qx = (tv.RW - qw)//2
    qy = int(tv.RH*0.28)
    # very low opacity watermark behind title — draw with dim color
    # since RGB no alpha, just draw with NUM_COLOR very dim
    draw.text((qx, qy), q, font=q_font, fill=(38,46,62))
    # Top badge
    cx, cy = tv.RW//2, int(tv.RH*0.21)
    draw_centered_pill(draw, "  QUESTION FOR YOU  ", tv.FONT, (38,46,62), (190,198,212), cx, cy, pad_x=18, pad_y=10, radius=12)
    # Title
    y0 = int(tv.RH*0.34)
    lh = int(HOOK_TITLE_SIZE*1.25)
    line1 = "Still using"
    w1 = tv.tw(draw, line1, BOLD_TITLE)
    draw.text(((tv.RW - w1)//2, y0), line1, font=BOLD_TITLE, fill=(230,237,243))
    line2 = "123456?"
    # monospace red for 123456
    mono = tv.FONT
    # try to use mono bold
    try:
        mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", HOOK_TITLE_SIZE)
    except: pass
    w2 = tv.tw(draw, line2, mono)
    x2 = (tv.RW - w2)//2
    y2 = y0 + lh
    # red pill behind
    draw.rounded_rectangle([x2-14, y2-8, x2+w2+14, y2+lh-14], radius=12, fill=tv.ERROR_COLOR)
    draw.text((x2, y2), line2, font=mono, fill=(255,255,255))
    # sub
    sub = "Let's fix that — forever."
    sub_y = y2 + lh + 30
    sw = tv.tw(draw, sub, tv.HOOK_SUB_FONT)
    draw.text(((tv.RW - sw)//2, sub_y), sub, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # CTA
    keep = "ANSWER INSIDE  →"
    kw = tv.tw(draw, keep, tv.FONT)
    kx, ky = (tv.RW - kw)//2, sub_y + 54
    draw.rounded_rectangle([kx-16, ky-8, kx+kw+16, ky+32], radius=12, fill=tv.ACCENT)
    draw.text((kx, ky+2), keep, font=tv.FONT, fill=tv.TERM_BG)
    return img

def hook3_list():
    """Formula: List — 3 lines = 5 passwords"""
    tv.apply_theme("ice")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # Top badge with numbers
    badge = "  3 LINES  •  5 PASSWORDS  "
    bw = tv.tw(draw, badge, tv.FONT)
    bx, by = (tv.RW - bw)//2, int(tv.RH*0.23)
    draw.rounded_rectangle([bx-18, by-10, bx+bw+18, by+32], radius=12, fill=tv.ACCENT)
    draw.text((bx, by), badge, font=tv.FONT, fill=(255,255,255))
    # Title with big numbers
    y0 = int(tv.RH*0.33)
    lh = int(HOOK_TITLE_SIZE*1.22)
    # line1: "3 lines ="
    # draw "3" in pill, rest normal
    line1_part1 = "3"
    line1_part2 = " lines ="
    w1 = tv.tw(draw, line1_part1, BOLD_TITLE)
    w2 = tv.tw(draw, line1_part2, BOLD_TITLE)
    total1 = w1 + w2 + 20
    x1 = (tv.RW - total1)//2
    y1 = y0
    # pill for 3
    draw.rounded_rectangle([x1-10, y1-6, x1+w1+10, y1+lh-16], radius=12, fill=tv.ACCENT)
    draw.text((x1, y1), line1_part1, font=BOLD_TITLE, fill=(255,255,255))
    draw.text((x1+w1+20, y1), line1_part2, font=BOLD_TITLE, fill=(45,55,70) if tv.TERM_BG[0]>200 else (230,237,243))
    # line2: "5 passwords"
    line2_part1 = "5"
    line2_part2 = " passwords"
    w3 = tv.tw(draw, line2_part1, BOLD_TITLE)
    w4 = tv.tw(draw, line2_part2, BOLD_TITLE)
    total2 = w3 + w4 + 20
    x2 = (tv.RW - total2)//2
    y2 = y0 + lh
    draw.rounded_rectangle([x2-10, y2-6, x2+w3+10, y2+lh-16], radius=12, fill=(40,167,69))
    draw.text((x2, y2), line2_part1, font=BOLD_TITLE, fill=(255,255,255))
    draw.text((x2+w3+20, y2), line2_part2, font=BOLD_TITLE, fill=(45,55,70) if tv.TERM_BG[0]>200 else (230,237,243))
    # visual equality sign between? Already included as "lines =" includes =
    # sub
    sub = "Copy. Paste. Done."
    sw = tv.tw(draw, sub, tv.HOOK_SUB_FONT)
    sx = (tv.RW - sw)//2
    sub_y = y2 + lh + 30
    draw.text((sx, sub_y), sub, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # accent line
    draw.rectangle([tv.RW//2-60, sub_y+40, tv.RW//2+60, sub_y+44], fill=tv.ACCENT)
    keep = "SEE HOW  →"
    kw = tv.tw(draw, keep, tv.FONT)
    kx, ky = (tv.RW - kw)//2, sub_y + 60
    draw.text((kx, ky), keep, font=tv.FONT, fill=tv.NUM_COLOR)
    return img

def hook4_secret():
    """Formula: Secret — Nobody tells you Python can do this"""
    tv.apply_theme("paper")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # badge
    badge = "  SECRET  •  PYTHON TRICK  "
    bw = tv.tw(draw, badge, SMALL_BOLD)
    bx, by = (tv.RW - bw)//2, int(tv.RH*0.22)
    draw.rounded_rectangle([bx-16, by-8, bx+bw+16, by+30], radius=12, fill=(211,54,130))
    draw.text((bx, by), badge, font=SMALL_BOLD, fill=(255,255,255))
    # title small top
    small = "Nobody tells you"
    sw = tv.tw(draw, small, tv.HOOK_SUB_FONT)
    sx = (tv.RW - sw)//2
    y0 = int(tv.RH*0.31)
    draw.text((sx, y0), small, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # main
    main1 = "Python can"
    main2 = "do this"
    w1 = tv.tw(draw, main1, BOLD_TITLE)
    w2 = tv.tw(draw, main2, BOLD_TITLE)
    x1 = (tv.RW - w1)//2
    y1 = y0 + 45
    x2 = (tv.RW - w2)//2
    y2 = y1 + int(HOOK_TITLE_SIZE*1.25)
    draw.text((x1, y1), main1, font=BOLD_TITLE, fill=(50,45,30))
    # accent pill for do this
    draw.rounded_rectangle([x2-14, y2-8, x2+w2+14, y2+int(HOOK_TITLE_SIZE*1.25)-14], radius=14, fill=tv.ACCENT)
    draw.text((x2, y2), main2, font=BOLD_TITLE, fill=(255,255,255))
    # sub
    sub = "Secure. Random. Instant."
    sw2 = tv.tw(draw, sub, tv.FONT)
    sx2 = (tv.RW - sw2)//2
    sub_y = y2 + int(HOOK_TITLE_SIZE*1.25) + 28
    draw.text((sx2, sub_y), sub, font=tv.FONT, fill=tv.NUM_COLOR)
    # CTA
    keep = "WATCH THE TRICK  →"
    kw = tv.tw(draw, keep, tv.FONT)
    kx, ky = (tv.RW - kw)//2, sub_y + 48
    draw.rounded_rectangle([kx-18, ky-10, kx+kw+18, ky+30], radius=12, fill=(42,161,152))
    draw.text((kx, ky), keep, font=tv.FONT, fill=(255,255,255))
    return img

def hook5_pov():
    """Formula: POV — you just got hacked"""
    tv.apply_theme("dracula")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # red alert badge
    badge = "  POV: YOU JUST GOT HACKED  "
    bw = tv.tw(draw, badge, tv.FONT)
    bx, by = (tv.RW - bw)//2, int(tv.RH*0.21)
    draw.rounded_rectangle([bx-18, by-10, bx+bw+18, by+32], radius=12, fill=tv.ERROR_COLOR)
    draw.text((bx, by), badge, font=tv.FONT, fill=(255,255,255))
    # large watermark "HACKED" faded behind?
    # title
    y0 = int(tv.RH*0.32)
    lh = int(HOOK_TITLE_SIZE*1.22)
    lines = ["Your passwords", "got hacked"]
    hf = BOLD_TITLE
    for i, line in enumerate(lines):
        y = y0 + i*lh
        if "hacked" in line.lower():
            # red for hacked
            w = tv.tw(draw, line, hf)
            x0 = (tv.RW - w)//2
            # split "got " and "hacked"
            pre = "got "
            pre_w = tv.tw(draw, pre, hf)
            hack = "hacked"
            total = pre_w + tv.tw(draw, hack, hf)
            x0 = (tv.RW - total)//2
            draw.text((x0, y), pre, font=hf, fill=(230,237,243))
            # red pill
            draw.rounded_rectangle([x0+pre_w-8, y-6, x0+pre_w+tv.tw(draw, hack, hf)+8, y+lh-14], radius=12, fill=tv.ERROR_COLOR)
            draw.text((x0+pre_w, y), hack, font=hf, fill=(255,255,255))
        else:
            w = tv.tw(draw, line, hf)
            x0 = (tv.RW - w)//2
            draw.text((x0, y), line, font=hf, fill=(230,237,243))
    # sub
    sub = "Never let it happen again."
    sw = tv.tw(draw, sub, tv.HOOK_SUB_FONT)
    sx = (tv.RW - sw)//2
    sub_y = y0 + 2*lh + 28
    draw.text((sx, sub_y), sub, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # CTA green
    keep = "STAY SAFE  →"
    kw = tv.tw(draw, keep, tv.FONT)
    kx, ky = (tv.RW - kw)//2, sub_y + 54
    draw.rounded_rectangle([kx-18, ky-10, kx+kw+18, ky+30], radius=12, fill=(40,167,69))
    draw.text((kx, ky), keep, font=tv.FONT, fill=(255,255,255))
    return img

if __name__ == "__main__":
    variants = [
        ("hook_new_1_mistake.png", hook1_mistake),
        ("hook_new_2_question.png", hook2_question),
        ("hook_new_3_list.png", hook3_list),
        ("hook_new_4_secret.png", hook4_secret),
        ("hook_new_5_pov.png", hook5_pov),
    ]
    for fname, func in variants:
        img = func()
        path = os.path.join(OUT_DIR, fname)
        img.save(path)
        print(f"Saved {path} {img.size}")
    # also prove light theme visibility with new fixes — already done but re-prove
    for theme in ["light","paper","ice","github"]:
        tv.apply_theme(theme)
        entry = {"type":"terminal","buffer":[[("~$ ",tv.PWD_COLOR),("python3 --version",tv.CMD_COLOR)], [("Python 3.12.1",tv.OUTPUT_COLOR)]],"partial":[(f"~/vault$ ",tv.PWD_COLOR),("ls",tv.CMD_COLOR)],"cursor":True}
        img = tv.render_terminal(entry)
        d = ImageDraw.Draw(img)
        txt = f"theme:{theme}"
        bw = tv.tw(d, txt, tv.FONT)
        d.rounded_rectangle([tv.RW-bw-32, 8, tv.RW-16, 36], radius=8, fill=tv.ACCENT)
        d.text((tv.RW-bw-24, 12), txt, font=tv.FONT, fill=tv.TERM_BG if tv.TERM_BG[0]>200 else (255,255,255))
        p = os.path.join(OUT_DIR, f"proof_{theme}_terminal.png")
        img.save(p)
        print(f"Saved proof {p}")
        lines = ["import secrets, string","","def gen(length=16):",'    chars = "abc"']
        entry2 = {"type":"explain","file":"vault/passgen.py","lines":lines,"active":2,"phase":"center","t":1.0}
        img2 = tv.render_explain(entry2)
        d2 = ImageDraw.Draw(img2)
        d2.rounded_rectangle([tv.RW-bw-32, 8, tv.RW-bw-32+110, 36], radius=8, fill=tv.ACCENT)
        d2.text((tv.RW-bw-24, 12), txt, font=tv.FONT, fill=tv.TERM_BG if tv.TERM_BG[0]>200 else (255,255,255))
        p2 = os.path.join(OUT_DIR, f"proof_{theme}_editor.png")
        img2.save(p2)
        print(f"Saved proof {p2}")
