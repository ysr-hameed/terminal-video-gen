#!/usr/bin/env python3
"""Generate 5 ULTRA-CLEAN modern hooks — perfect pill centering (anchor mm), no overflow, theme-aware."""
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
SUB_FONT = tv.HOOK_SUB_FONT
TITLE_BOLD = load_bold(HOOK_TITLE_SIZE)

def is_light():
    return tv.TERM_BG[0] > 200

def title_color():
    return (30,32,35) if is_light() else (230,237,243)

def pill_centered(draw, text, font, fill, text_fill, cx, cy, pad_x=20, pad_y=10, radius=14):
    # perfect center using anchor mm
    l,t,r,b = draw.textbbox((0,0), text, font=font, anchor="mm")
    bw, bh = r-l, b-t
    x1 = cx - bw//2 - pad_x
    y1 = cy - bh//2 - pad_y
    x2 = cx + bw//2 + pad_x
    y2 = cy + bh//2 + pad_y
    # ensure pill fits within screen with 20px margin
    margin = 20*tv.RENDER_SCALE
    if x1 < margin:
        x1 = margin
        x2 = x1 + bw + 2*pad_x
        cx = (x1+x2)//2
    if x2 > tv.RW - margin:
        x2 = tv.RW - margin
        x1 = x2 - (bw + 2*pad_x)
        cx = (x1+x2)//2
    # shadow
    draw.rounded_rectangle([x1+4, y1+4, x2+4, y2+4], radius=radius, fill=(0,0,0,30))
    draw.rounded_rectangle([x1,y1,x2,y2], radius=radius, fill=fill)
    draw.text((cx, cy), text, font=font, fill=text_fill, anchor="mm")
    return (x1,y1,x2,y2)

# === 5 DISTINCT HOOKS — each fully unique layout, modern, no overflow ===

def hook1_mistake():
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # badge
    cx, cy = tv.RW//2, int(tv.RH*0.22)
    pill_centered(draw, "STOP DOING THIS", tv.FONT, (255,193,7), (30,32,35), cx, cy, pad_x=20, pad_y=12, radius=14)
    y0 = int(tv.RH*0.32)
    lh = int(HOOK_TITLE_SIZE*1.18)
    hf = TITLE_BOLD
    # line1
    l1 = "Stop saving"
    w1 = tv.tw(draw, l1, hf)
    draw.text(((tv.RW-w1)//2, y0), l1, font=hf, fill=tv.ACCENT)
    # line2 passwords in red pill — use pill helper for perfect centering
    l2 = "passwords"
    y2 = y0 + lh
    # pill behind l2
    bw2 = tv.tw(draw, l2, hf)
    bh2 = tv.th(draw, l2, hf)
    cx2, cy2 = tv.RW//2, y2 + bh2//2 + 4
    # pill size
    pad_x, pad_y = 16, 8
    draw.rounded_rectangle([cx2-bw2//2-pad_x+4, cy2-bh2//2-pad_y+4, cx2+bw2//2+pad_x+4, cy2+bh2//2+pad_y+4], radius=12, fill=(0,0,0,30))
    draw.rounded_rectangle([cx2-bw2//2-pad_x, cy2-bh2//2-pad_y, cx2+bw2//2+pad_x, cy2+bh2//2+pad_y], radius=12, fill=tv.ERROR_COLOR)
    draw.text((cx2, cy2), l2, font=hf, fill=(255,255,255), anchor="mm")
    # line3
    l3 = "in notes."
    w3 = tv.tw(draw, l3, hf)
    draw.text(((tv.RW-w3)//2, y0+2*lh), l3, font=hf, fill=title_color())
    sub = "You're one leak away — fix it in 60s."
    sw = tv.tw(draw, sub, SUB_FONT)
    sub_y = y0 + 3*lh + 28
    draw.text(((tv.RW-sw)//2, sub_y), sub, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    draw.rectangle([tv.RW//2-50, sub_y+36, tv.RW//2+50, sub_y+40], fill=tv.ACCENT)
    cta = "FIX IT NOW  \u2192"
    pill_centered(draw, cta, tv.FONT, tv.ACCENT, (255,255,255), tv.RW//2, sub_y+72, pad_x=18, pad_y=10, radius=12)
    return img

def hook2_question():
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    pill_centered(draw, "QUESTION FOR YOU", tv.FONT, (30,32,35), (250,240,220), tv.RW//2, int(tv.RH*0.22), pad_x=18, pad_y=10, radius=12)
    y0 = int(tv.RH*0.32)
    lh = int(HOOK_TITLE_SIZE*1.20)
    hf = TITLE_BOLD
    l1 = "Still using"
    w1 = tv.tw(draw, l1, hf)
    draw.text(((tv.RW-w1)//2, y0), l1, font=hf, fill=title_color())
    l2 = "123456?"
    try:
        mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", HOOK_TITLE_SIZE)
    except:
        mono = hf
    bw2 = tv.tw(draw, l2, mono)
    bh2 = tv.th(draw, l2, mono)
    cx2, cy2 = tv.RW//2, y0 + lh + bh2//2 + 6
    # red pill behind
    pad_x, pad_y = 14, 8
    draw.rounded_rectangle([cx2-bw2//2-pad_x+4, cy2-bh2//2-pad_y+4, cx2+bw2//2+pad_x+4, cy2+bh2//2+pad_y+4], radius=12, fill=(0,0,0,30))
    draw.rounded_rectangle([cx2-bw2//2-pad_x, cy2-bh2//2-pad_y, cx2+bw2//2+pad_x, cy2+bh2//2+pad_y], radius=12, fill=tv.ERROR_COLOR)
    draw.text((cx2, cy2), l2, font=mono, fill=(255,255,255), anchor="mm")
    sub = "Let's fix that — forever."
    sw = tv.tw(draw, sub, SUB_FONT)
    sub_y = y0 + 2*lh + 28
    draw.text(((tv.RW-sw)//2, sub_y), sub, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    pill_centered(draw, "ANSWER INSIDE  \u2192", tv.FONT, tv.ACCENT, (255,255,255), tv.RW//2, sub_y+62, pad_x=18, pad_y=10, radius=12)
    return img

def hook3_list():
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    pill_centered(draw, "3 LINES  \u2022  5 PASSWORDS", tv.FONT, tv.ACCENT, (255,255,255), tv.RW//2, int(tv.RH*0.23), pad_x=18, pad_y=10, radius=12)
    y0 = int(tv.RH*0.33)
    lh = int(HOOK_TITLE_SIZE*1.18)
    hf = TITLE_BOLD
    # line1: "3  lines =" with 3 pill
    part1 = "3"
    part2 = "  lines ="
    w1 = tv.tw(draw, part1, hf)
    w2 = tv.tw(draw, part2, hf)
    total1 = w1 + w2 + 24
    x1 = (tv.RW - total1)//2
    y1 = y0
    bw1 = tv.tw(draw, part1, hf)
    bh1 = tv.th(draw, part1, hf)
    cx1 = x1 + bw1//2
    cy1 = y1 + bh1//2 + 6
    draw.rounded_rectangle([cx1-bw1//2-10+4, cy1-bh1//2-6+4, cx1+bw1//2+10+4, cy1+bh1//2+6+4], radius=12, fill=(0,0,0,25))
    draw.rounded_rectangle([cx1-bw1//2-10, cy1-bh1//2-6, cx1+bw1//2+10, cy1+bh1//2+6], radius=12, fill=tv.ACCENT)
    draw.text((cx1, cy1), part1, font=hf, fill=(255,255,255), anchor="mm")
    draw.text((x1+w1+24, y1), part2.strip(), font=hf, fill=title_color())
    # line2
    p1 = "5"
    p2 = "  passwords"
    w3 = tv.tw(draw, p1, hf)
    w4 = tv.tw(draw, p2, hf)
    total2 = w3 + w4 + 24
    x2 = (tv.RW - total2)//2
    y2 = y0 + lh
    bw3 = tv.tw(draw, p1, hf)
    bh3 = tv.th(draw, p1, hf)
    cx3 = x2 + bw3//2
    cy3 = y2 + bh3//2 + 6
    draw.rounded_rectangle([cx3-bw3//2-10+4, cy3-bh3//2-6+4, cx3+bw3//2+10+4, cy3+bh3//2+6+4], radius=12, fill=(0,0,0,25))
    draw.rounded_rectangle([cx3-bw3//2-10, cy3-bh3//2-6, cx3+bw3//2+10, cy3+bh3//2+6], radius=12, fill=(40,167,69))
    draw.text((cx3, cy3), p1, font=hf, fill=(255,255,255), anchor="mm")
    draw.text((x2+w3+24, y2), p2.strip(), font=hf, fill=title_color())
    sub = "Copy. Paste. Done."
    sw = tv.tw(draw, sub, SUB_FONT)
    sub_y = y2 + lh + 32
    draw.text(((tv.RW-sw)//2, sub_y), sub, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    draw.rectangle([tv.RW//2-50, sub_y+36, tv.RW//2+50, sub_y+40], fill=tv.ACCENT)
    cta = "SEE HOW  \u2192"
    draw.text(((tv.RW - tv.tw(draw, cta, tv.FONT))//2, sub_y+68), cta, font=tv.FONT, fill=tv.NUM_COLOR)
    return img

def hook4_secret():
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    pill_centered(draw, "SECRET  \u2022  PYTHON TRICK", tv.FONT, (211,54,130), (255,255,255), tv.RW//2, int(tv.RH*0.22), pad_x=18, pad_y=10, radius=12)
    y0 = int(tv.RH*0.31)
    small = "Nobody tells you"
    sw = tv.tw(draw, small, SUB_FONT)
    draw.text(((tv.RW-sw)//2, y0), small, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    y1 = y0 + 48
    l1 = "Python can"
    w1 = tv.tw(draw, l1, TITLE_BOLD)
    draw.text(((tv.RW-w1)//2, y1), l1, font=TITLE_BOLD, fill=title_color())
    l2 = "do this"
    bw2 = tv.tw(draw, l2, TITLE_BOLD)
    bh2 = tv.th(draw, l2, TITLE_BOLD)
    cx2, cy2 = tv.RW//2, y1 + int(HOOK_TITLE_SIZE*1.22) + bh2//2
    draw.rounded_rectangle([cx2-bw2//2-14+4, cy2-bh2//2-8+4, cx2+bw2//2+14+4, cy2+bh2//2+8+4], radius=14, fill=(0,0,0,30))
    draw.rounded_rectangle([cx2-bw2//2-14, cy2-bh2//2-8, cx2+bw2//2+14, cy2+bh2//2+8], radius=14, fill=tv.ACCENT)
    draw.text((cx2, cy2), l2, font=TITLE_BOLD, fill=(255,255,255), anchor="mm")
    sub = "Secure. Random. Instant."
    sw2 = tv.tw(draw, sub, tv.FONT)
    sub_y = y1 + int(HOOK_TITLE_SIZE*1.22) + 30 + bh2//2
    draw.text(((tv.RW-sw2)//2, sub_y), sub, font=tv.FONT, fill=tv.NUM_COLOR)
    pill_centered(draw, "WATCH THE TRICK  \u2192", tv.FONT, (42,161,152), (255,255,255), tv.RW//2, sub_y+52, pad_x=18, pad_y=10, radius=12)
    return img

def hook5_pov():
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    pill_centered(draw, "POV: YOU JUST GOT HACKED", tv.FONT, tv.ERROR_COLOR, (255,255,255), tv.RW//2, int(tv.RH*0.21), pad_x=18, pad_y=10, radius=12)
    y0 = int(tv.RH*0.32)
    lh = int(HOOK_TITLE_SIZE*1.20)
    hf = TITLE_BOLD
    l1 = "Your passwords"
    w1 = tv.tw(draw, l1, hf)
    draw.text(((tv.RW-w1)//2, y0), l1, font=hf, fill=(230,237,243) if not is_light() else (30,32,35))
    pre = "got "
    hack = "hacked"
    pre_w = tv.tw(draw, pre, hf)
    hack_w = tv.tw(draw, hack, hf)
    total = pre_w + hack_w
    x0 = (tv.RW - total)//2
    y2 = y0 + lh
    draw.text((x0, y2), pre, font=hf, fill=(230,237,243) if not is_light() else (30,32,35))
    # hacked pill
    bw = hack_w
    bh = tv.th(draw, hack, hf)
    cxh, cyh = x0 + pre_w + bw//2, y2 + bh//2 + 6
    draw.rounded_rectangle([cxh-bw//2-8+4, cyh-bh//2-6+4, cxh+bw//2+8+4, cyh+bh//2+6+4], radius=12, fill=(0,0,0,30))
    draw.rounded_rectangle([cxh-bw//2-8, cyh-bh//2-6, cxh+bw//2+8, cyh+bh//2+6], radius=12, fill=tv.ERROR_COLOR)
    draw.text((cxh, cyh), hack, font=hf, fill=(255,255,255), anchor="mm")
    sub = "Never let it happen again."
    sw = tv.tw(draw, sub, SUB_FONT)
    sub_y = y2 + lh + 30
    draw.text(((tv.RW-sw)//2, sub_y), sub, font=SUB_FONT, fill=tv.OUTPUT_COLOR)
    pill_centered(draw, "STAY SAFE  \u2192", tv.FONT, (40,167,69), (255,255,255), tv.RW//2, sub_y+60, pad_x=18, pad_y=10, radius=12)
    return img

if __name__ == "__main__":
    outs = [
        ("hook_clean_1_mistake.png", hook1_mistake),
        ("hook_clean_2_question.png", hook2_question),
        ("hook_clean_3_list.png", hook3_list),
        ("hook_clean_4_secret.png", hook4_secret),
        ("hook_clean_5_pov.png", hook5_pov),
    ]
    # generate each hook across all 6 themes to prove hook-only theming
    for fname, func in outs:
        # default theme for each hook as designed (already set inside func), just save
        img = func()
        path = os.path.join(OUT_DIR, fname)
        img.save(path)
        print(f"Saved {path}")
    # also generate hook theme matrix — 5 hooks x 6 themes = 30 images if needed, but generate 5*6 for full proof
    # For now generate just hook previews for all themes using hook1 as example
    for theme in ["light","paper","ice","github","dracula","forest"]:
        tv.apply_theme(theme)
        # use hook1 title as generic proof
        entry = {"type":"hook","title":"Stop using weak passwords","sub":"Let's fix that in 60 seconds","n":len("Stop using weak passwords"),"sub_on":True,"cursor":False}
        # Need to re-apply theme after entry? render_hook uses current TERM_BG
        img = tv.render_hook(entry)
        p = os.path.join(OUT_DIR, f"hook_theme_{theme}.png")
        img.save(p)
        print(f"Saved hook theme proof {p}")
    # also prove editor/terminal visibility for light themes (already fixed)
    for theme in ["light","paper","ice","github"]:
        tv.apply_theme(theme)
        # terminal
        entry = {"type":"terminal","buffer":[[("~$ ",tv.PWD_COLOR),("python3 --version",tv.CMD_COLOR)], [("Python 3.12.1",tv.OUTPUT_COLOR)]],"partial":[(f"~/vault$ ",tv.PWD_COLOR),("ls",tv.CMD_COLOR)],"cursor":True}
        img = tv.render_terminal(entry)
        d = ImageDraw.Draw(img)
        txt = f"theme:{theme}"
        bw = tv.tw(d, txt, tv.FONT)
        d.rounded_rectangle([tv.RW-bw-32, 8, tv.RW-16, 36], radius=8, fill=tv.ACCENT)
        d.text((tv.RW-bw-24, 12), txt, font=tv.FONT, fill=(255,255,255), anchor="mm")
        # use anchor mm for badge
        # Actually need to center text in pill: use anchor mm
        # Redraw with anchor mm for perfect centering
        # Pill already drawn, text at wrong pos — fix: clear and redraw pill correctly
        # Simplify: redraw pill with anchor
        # (We already drew, but text at (RW-bw-24,12) is top-left, not centered. Fix:)
        # Overwrite: draw pill centered properly
        # Remove previous and redraw
        img2 = tv.render_terminal(entry)
        d2 = ImageDraw.Draw(img2)
        l,t,r,b = d2.textbbox((0,0), txt, font=tv.FONT, anchor="mm")
        bw2, bh2 = r-l, b-t
        cx, cy = tv.RW - bw2//2 - 24, 22
        d2.rounded_rectangle([cx-bw2//2-12, cy-bh2//2-8, cx+bw2//2+12, cy+bh2//2+8], radius=8, fill=tv.ACCENT)
        d2.text((cx, cy), txt, font=tv.FONT, fill=(255,255,255), anchor="mm")
        p = os.path.join(OUT_DIR, f"clean_proof_{theme}_terminal.png")
        img2.save(p)
        print(f"Saved proof {p}")
        lines = ["import secrets, string","","def gen(length=16):",'    chars = "abc"']
        entry2 = {"type":"explain","file":"vault/passgen.py","lines":lines,"active":2,"phase":"center","t":1.0}
        img3 = tv.render_explain(entry2)
        d3 = ImageDraw.Draw(img3)
        l3,t3,r3,b3 = d3.textbbox((0,0), txt, font=tv.FONT, anchor="mm")
        bw3, bh3 = r3-l3, b3-t3
        cx3, cy3 = tv.RW - bw3//2 - 24, 22
        d3.rounded_rectangle([cx3-bw3//2-12, cy3-bh3//2-8, cx3+bw3//2+12, cy3+bh3//2+8], radius=8, fill=tv.ACCENT)
        d3.text((cx3, cy3), txt, font=tv.FONT, fill=(255,255,255), anchor="mm")
        p2 = os.path.join(OUT_DIR, f"clean_proof_{theme}_editor.png")
        img3.save(p2)
        print(f"Saved proof {p2}")
