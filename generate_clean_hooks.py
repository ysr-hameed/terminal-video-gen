#!/usr/bin/env python3
"""Generate 5 ULTRA-CLEAN, fully distinct modern hook layouts — zero overflow, perfect align."""
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
HOOK_SUB_SIZE = 34 * tv.RENDER_SCALE
TITLE_BOLD = load_bold(HOOK_TITLE_SIZE)
SUB_FONT = tv.HOOK_SUB_FONT

def is_light():
    return tv.TERM_BG[0] > 200

def title_color_default():
    return (30,32,35) if is_light() else (230,237,243)

def hook1_mistake_clean_fixed():
    tv.apply_theme("light")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    badge = "STOP DOING THIS"
    bw = tv.tw(draw, badge, tv.FONT)
    bh = tv.th(draw, badge, tv.FONT)
    cx, cy = tv.RW//2, int(tv.RH*0.22)
    pad_x, pad_y = 20, 12
    draw.rounded_rectangle([cx-bw//2-pad_x+4, cy-bh//2-pad_y+4, cx+bw//2+pad_x+4, cy+bh//2+pad_y+4], radius=14, fill=(0,0,0,30))
    draw.rounded_rectangle([cx-bw//2-pad_x, cy-bh//2-pad_y, cx+bw//2+pad_x, cy+bh//2+pad_y], radius=14, fill=(255,193,7))
    draw.text((cx-bw//2, cy-bh//2), badge, font=tv.FONT, fill=(30,32,35))
    y0 = int(tv.RH*0.32)
    lh = int(HOOK_TITLE_SIZE*1.18)
    hf = TITLE_BOLD
    l1 = "Stop saving"
    w1 = tv.tw(draw, l1, hf)
    draw.text(((tv.RW-w1)//2, y0), l1, font=hf, fill=tv.ACCENT)
    l2 = "passwords"
    w2 = tv.tw(draw, l2, hf)
    x2 = (tv.RW - w2)//2
    y2 = y0 + lh
    draw.rounded_rectangle([x2-16, y2-8, x2+w2+16, y2+lh-14], radius=12, fill=tv.ERROR_COLOR)
    draw.text((x2, y2), l2, font=hf, fill=(255,255,255))
    l3 = "in notes."
    w3 = tv.tw(draw, l3, hf)
    draw.text(((tv.RW-w3)//2, y0+2*lh), l3, font=hf, fill=title_color_default())
    sub = "You're one leak away — fix it in 60s."
    sw = tv.tw(draw, sub, SUB_FONT)
    sub_y = y0 + 3*lh + 28
    draw.text(((tv.RW - sw)//2, sub_y), sub, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    draw.rectangle([tv.RW//2-50, sub_y+36, tv.RW//2+50, sub_y+40], fill=tv.ACCENT)
    cta = "FIX IT NOW  \u2192"
    kw = tv.tw(draw, cta, tv.FONT)
    bh2 = tv.th(draw, cta, tv.FONT)
    kx, ky = tv.RW//2, sub_y + 72
    pad_x2, pad_y2 = 18, 10
    draw.rounded_rectangle([kx-kw//2-pad_x2+4, ky-bh2//2-pad_y2+4, kx+kw//2+pad_x2+4, ky+bh2//2+pad_y2+4], radius=12, fill=(0,0,0,30))
    draw.rounded_rectangle([kx-kw//2-pad_x2, ky-bh2//2-pad_y2, kx+kw//2+pad_x2, ky+bh2//2+pad_y2], radius=12, fill=tv.ACCENT)
    draw.text((kx-kw//2, ky-bh2//2), cta, font=tv.FONT, fill=(255,255,255))
    return img

def hook2_question_clean():
    tv.apply_theme("paper")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    badge = "QUESTION FOR YOU"
    bw = tv.tw(draw, badge, tv.FONT)
    bh = tv.th(draw, badge, tv.FONT)
    cx, cy = tv.RW//2, int(tv.RH*0.22)
    pad_x, pad_y = 18, 10
    draw.rounded_rectangle([cx-bw//2-pad_x, cy-bh//2-pad_y, cx+bw//2+pad_x, cy+bh//2+pad_y], radius=12, fill=(30,32,35))
    draw.text((cx-bw//2, cy-bh//2), badge, font=tv.FONT, fill=(250,240,220))
    y0 = int(tv.RH*0.32)
    lh = int(HOOK_TITLE_SIZE*1.20)
    hf = TITLE_BOLD
    l1 = "Still using"
    w1 = tv.tw(draw, l1, hf)
    draw.text(((tv.RW-w1)//2, y0), l1, font=hf, fill=title_color_default())
    l2 = "123456?"
    try:
        mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", HOOK_TITLE_SIZE)
    except:
        mono = hf
    w2 = tv.tw(draw, l2, mono)
    x2 = (tv.RW - w2)//2
    y2 = y0 + lh
    draw.rounded_rectangle([x2-14, y2-8, x2+w2+14, y2+lh-14], radius=12, fill=tv.ERROR_COLOR)
    draw.text((x2, y2), l2, font=mono, fill=(255,255,255))
    sub = "Let's fix that — forever."
    sw = tv.tw(draw, sub, SUB_FONT)
    sub_y = y2 + lh + 28
    draw.text(((tv.RW-sw)//2, sub_y), sub, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    cta = "ANSWER INSIDE  \u2192"
    kw = tv.tw(draw, cta, tv.FONT)
    bh2 = tv.th(draw, cta, tv.FONT)
    kx, ky = tv.RW//2, sub_y + 62
    draw.rounded_rectangle([kx-kw//2-18+4, ky-bh2//2-10+4, kx+kw//2+18+4, ky+bh2//2+10+4], radius=12, fill=(0,0,0,30))
    draw.rounded_rectangle([kx-kw//2-18, ky-bh2//2-10, kx+kw//2+18, ky+bh2//2+10], radius=12, fill=tv.ACCENT)
    draw.text((kx-kw//2, ky-bh2//2), cta, font=tv.FONT, fill=(255,255,255))
    return img

def hook3_list_clean():
    tv.apply_theme("ice")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    badge = "3 LINES  \u2022  5 PASSWORDS"
    bw = tv.tw(draw, badge, tv.FONT)
    bh = tv.th(draw, badge, tv.FONT)
    cx, cy = tv.RW//2, int(tv.RH*0.23)
    draw.rounded_rectangle([cx-bw//2-18+4, cy-bh//2-10+4, cx+bw//2+18+4, cy+bh//2+10+4], radius=12, fill=(0,0,0,25))
    draw.rounded_rectangle([cx-bw//2-18, cy-bh//2-10, cx+bw//2+18, cy+bh//2+10], radius=12, fill=tv.ACCENT)
    draw.text((cx-bw//2, cy-bh//2), badge, font=tv.FONT, fill=(255,255,255))
    y0 = int(tv.RH*0.33)
    lh = int(HOOK_TITLE_SIZE*1.18)
    hf = TITLE_BOLD
    part1 = "3"
    part2 = "  lines ="
    w1 = tv.tw(draw, part1, hf)
    w2 = tv.tw(draw, part2, hf)
    total1 = w1 + w2 + 24
    x1 = (tv.RW - total1)//2
    y1 = y0
    draw.rounded_rectangle([x1-10, y1-6, x1+w1+10, y1+lh-16], radius=12, fill=tv.ACCENT)
    draw.text((x1, y1), part1, font=hf, fill=(255,255,255))
    draw.text((x1+w1+24, y1), part2.strip(), font=hf, fill=title_color_default())
    p1 = "5"
    p2 = "  passwords"
    w3 = tv.tw(draw, p1, hf)
    w4 = tv.tw(draw, p2, hf)
    total2 = w3 + w4 + 24
    x2 = (tv.RW - total2)//2
    y2 = y0 + lh
    draw.rounded_rectangle([x2-10, y2-6, x2+w3+10, y2+lh-16], radius=12, fill=(40,167,69))
    draw.text((x2, y2), p1, font=hf, fill=(255,255,255))
    draw.text((x2+w3+24, y2), p2.strip(), font=hf, fill=title_color_default())
    sub = "Copy. Paste. Done."
    sw = tv.tw(draw, sub, SUB_FONT)
    sub_y = y2 + lh + 32
    draw.text(((tv.RW-sw)//2, sub_y), sub, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    draw.rectangle([tv.RW//2-50, sub_y+36, tv.RW//2+50, sub_y+40], fill=tv.ACCENT)
    cta = "SEE HOW  \u2192"
    kw = tv.tw(draw, cta, tv.FONT)
    bh2 = tv.th(draw, cta, tv.FONT)
    kx, ky = tv.RW//2, sub_y + 68
    draw.text((kx-kw//2, ky-bh2//2), cta, font=tv.FONT, fill=tv.NUM_COLOR)
    return img

def hook4_secret_clean():
    tv.apply_theme("github")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    badge = "SECRET  \u2022  PYTHON TRICK"
    bw = tv.tw(draw, badge, tv.FONT)
    bh = tv.th(draw, badge, tv.FONT)
    cx, cy = tv.RW//2, int(tv.RH*0.22)
    draw.rounded_rectangle([cx-bw//2-18+4, cy-bh//2-10+4, cx+bw//2+18+4, cy+bh//2+10+4], radius=12, fill=(0,0,0,30))
    draw.rounded_rectangle([cx-bw//2-18, cy-bh//2-10, cx+bw//2+18, cy+bh//2+10], radius=12, fill=(211,54,130))
    draw.text((cx-bw//2, cy-bh//2), badge, font=tv.FONT, fill=(255,255,255))
    y0 = int(tv.RH*0.31)
    small = "Nobody tells you"
    sw = tv.tw(draw, small, SUB_FONT)
    draw.text(((tv.RW-sw)//2, y0), small, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    y1 = y0 + 48
    l1 = "Python can"
    w1 = tv.tw(draw, l1, TITLE_BOLD)
    draw.text(((tv.RW-w1)//2, y1), l1, font=TITLE_BOLD, fill=title_color_default())
    l2 = "do this"
    w2 = tv.tw(draw, l2, TITLE_BOLD)
    x2 = (tv.RW-w2)//2
    y2 = y1 + int(HOOK_TITLE_SIZE*1.22)
    draw.rounded_rectangle([x2-14, y2-8, x2+w2+14, y2+int(HOOK_TITLE_SIZE*1.22)-14], radius=14, fill=tv.ACCENT)
    draw.text((x2, y2), l2, font=TITLE_BOLD, fill=(255,255,255))
    sub = "Secure. Random. Instant."
    sw2 = tv.tw(draw, sub, tv.FONT)
    sub_y = y2 + int(HOOK_TITLE_SIZE*1.22) + 30
    draw.text(((tv.RW-sw2)//2, sub_y), sub, font=tv.FONT, fill=tv.NUM_COLOR)
    cta = "WATCH THE TRICK  \u2192"
    kw = tv.tw(draw, cta, tv.FONT)
    bh2 = tv.th(draw, cta, tv.FONT)
    kx, ky = tv.RW//2, sub_y + 52
    draw.rounded_rectangle([kx-kw//2-18+4, ky-bh2//2-10+4, kx+kw//2+18+4, ky+bh2//2+10+4], radius=12, fill=(42,161,152))
    draw.rounded_rectangle([kx-kw//2-18, ky-bh2//2-10, kx+kw//2+18, ky+bh2//2+10], radius=12, fill=(42,161,152))
    draw.text((kx-kw//2, ky-bh2//2), cta, font=tv.FONT, fill=(255,255,255))
    return img

def hook5_pov_clean():
    tv.apply_theme("dracula")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    badge = "POV: YOU JUST GOT HACKED"
    bw = tv.tw(draw, badge, tv.FONT)
    bh = tv.th(draw, badge, tv.FONT)
    cx, cy = tv.RW//2, int(tv.RH*0.21)
    draw.rounded_rectangle([cx-bw//2-18+4, cy-bh//2-10+4, cx+bw//2+18+4, cy+bh//2+10+4], radius=12, fill=(0,0,0,30))
    draw.rounded_rectangle([cx-bw//2-18, cy-bh//2-10, cx+bw//2+18, cy+bh//2+10], radius=12, fill=tv.ERROR_COLOR)
    draw.text((cx-bw//2, cy-bh//2), badge, font=tv.FONT, fill=(255,255,255))
    y0 = int(tv.RH*0.32)
    lh = int(HOOK_TITLE_SIZE*1.20)
    hf = TITLE_BOLD
    l1 = "Your passwords"
    w1 = tv.tw(draw, l1, hf)
    draw.text(((tv.RW-w1)//2, y0), l1, font=hf, fill=(230,237,243))
    pre = "got "
    hack = "hacked"
    pre_w = tv.tw(draw, pre, hf)
    hack_w = tv.tw(draw, hack, hf)
    total = pre_w + hack_w
    x0 = (tv.RW - total)//2
    y2 = y0 + lh
    draw.text((x0, y2), pre, font=hf, fill=(230,237,243))
    draw.rounded_rectangle([x0+pre_w-8, y2-8, x0+pre_w+hack_w+8, y2+lh-14], radius=12, fill=tv.ERROR_COLOR)
    draw.text((x0+pre_w, y2), hack, font=hf, fill=(255,255,255))
    sub = "Never let it happen again."
    sw = tv.tw(draw, sub, SUB_FONT)
    sub_y = y2 + lh + 30
    draw.text(((tv.RW-sw)//2, sub_y), sub, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    cta = "STAY SAFE  \u2192"
    kw = tv.tw(draw, cta, tv.FONT)
    bh2 = tv.th(draw, cta, tv.FONT)
    kx, ky = tv.RW//2, sub_y + 60
    draw.rounded_rectangle([kx-kw//2-18+4, ky-bh2//2-10+4, kx+kw//2+18+4, ky+bh2//2+10+4], radius=12, fill=(40,167,69))
    draw.rounded_rectangle([kx-kw//2-18, ky-bh2//2-10, kx+kw//2+18, ky+bh2//2+10], radius=12, fill=(40,167,69))
    draw.text((kx-kw//2, ky-bh2//2), cta, font=tv.FONT, fill=(255,255,255))
    return img

if __name__ == "__main__":
    outs = [
        ("hook_clean_1_mistake.png", hook1_mistake_clean_fixed),
        ("hook_clean_2_question.png", hook2_question_clean),
        ("hook_clean_3_list.png", hook3_list_clean),
        ("hook_clean_4_secret.png", hook4_secret_clean),
        ("hook_clean_5_pov.png", hook5_pov_clean),
    ]
    for fname, func in outs:
        img = func()
        path = os.path.join(OUT_DIR, fname)
        img.save(path)
        print(f"Saved {path}")
    for theme in ["light","paper","ice","github","dracula","forest"]:
        tv.apply_theme(theme)
        entry = {"type":"terminal","buffer":[[("~$ ",tv.PWD_COLOR),("python3 --version",tv.CMD_COLOR)], [("Python 3.12.1",tv.OUTPUT_COLOR)]],"partial":[(f"~/vault$ ",tv.PWD_COLOR),("ls",tv.CMD_COLOR)],"cursor":True}
        img = tv.render_terminal(entry)
        d = ImageDraw.Draw(img)
        txt = f"theme:{theme}"
        bw = tv.tw(d, txt, tv.FONT)
        d.rounded_rectangle([tv.RW-bw-32, 8, tv.RW-16, 36], radius=8, fill=tv.ACCENT)
        d.text((tv.RW-bw-24, 12), txt, font=tv.FONT, fill=(255,255,255))
        p = os.path.join(OUT_DIR, f"clean_proof_{theme}_terminal.png")
        img.save(p)
        print(f"Saved proof {p}")
        lines = ["import secrets, string","","def gen(length=16):",'    chars = "abc"']
        entry2 = {"type":"explain","file":"vault/passgen.py","lines":lines,"active":2,"phase":"center","t":1.0}
        img2 = tv.render_explain(entry2)
        d2 = ImageDraw.Draw(img2)
        d2.rounded_rectangle([tv.RW-bw-32, 8, tv.RW-bw-32+110, 36], radius=8, fill=tv.ACCENT)
        d2.text((tv.RW-bw-24, 12), txt, font=tv.FONT, fill=(255,255,255))
        p2 = os.path.join(OUT_DIR, f"clean_proof_{theme}_editor.png")
        img2.save(p2)
        print(f"Saved proof {p2}")
