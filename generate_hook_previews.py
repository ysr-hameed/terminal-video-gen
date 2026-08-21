#!/usr/bin/env python3
"""Generate 5 distinct hook scene variants for user to pick."""
import os
from PIL import Image, ImageDraw, ImageFont
import terminal_video as tv

OUT_DIR = "hook_previews"
os.makedirs(OUT_DIR, exist_ok=True)

# Use a clean theme for previews — test light visibility too
# We'll generate each variant under both dark and light? For now generate under auto light fix proof
# Let's generate variants 1-5 under 'light' and also dark? User wants to see all themes must be visible.
# We'll just generate under 'light' and 'github' side by side? Simpler: generate 5 variants under 'light' (hardest) to prove fix.

def load_bold(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

HOOK_TITLE_SIZE = 68 * tv.RENDER_SCALE
HOOK_SUB_SIZE = 36 * tv.RENDER_SCALE
CAP_SIZE = 48 * tv.RENDER_SCALE

# Variant helpers using tv utilities but custom layouts

def variant_1(title, sub):
    # Current modern: badge + colored title + sub + keep watching
    tv.apply_theme("light")  # test light visibility
    entry = {"type":"hook","title":title,"sub":sub,"n":len(title),"sub_on":True,"cursor":False}
    img = tv.render_hook(entry)
    return img

def variant_2(title, sub):
    # Bold stacked — STOP huge outline, WEAK red pill
    tv.apply_theme("light")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # top small label
    label = "PYTHON  •  60 SEC  •  BEGINNER"
    bw = tv.tw(draw, label, tv.FONT)
    bx = (tv.RW - bw)//2
    by = int(tv.RH*0.22)
    draw.text((bx, by), label, font=tv.FONT, fill=tv.ACCENT)
    # title stacked
    # split title into 2 lines manually: "Stop using" / "weak passwords"
    lines = ["Stop using", "weak passwords"]
    y0 = int(tv.RH*0.33)
    lh = int(HOOK_TITLE_SIZE*1.25)
    hf = load_bold(HOOK_TITLE_SIZE)
    hf2 = load_bold(int(HOOK_TITLE_SIZE*1.05))
    for i, line in enumerate(lines):
        # color second line's "weak" red
        if i == 1:
            # render "weak" in red pill, "passwords" normal
            w1 = "weak"
            w2 = " passwords"
            w1w = tv.tw(draw, w1, hf)
            w2w = tv.tw(draw, w2, hf)
            total = w1w + w2w
            x0 = (tv.RW - total)//2
            y = y0 + i*lh
            # red pill behind weak
            draw.rounded_rectangle([x0-12, y-6, x0+w1w+12, y+lh-12], radius=12, fill=tv.ERROR_COLOR)
            draw.text((x0, y), w1, font=hf, fill=(255,255,255))
            draw.text((x0+w1w, y), w2, font=hf, fill=(30,32,35) if tv.TERM_BG[0]>200 else (230,237,243))
        else:
            # first line "Stop using" with STOP accent
            # split
            p1 = "Stop"
            p2 = " using"
            p1w = tv.tw(draw, p1, hf)
            total = p1w + tv.tw(draw, p2, hf)
            x0 = (tv.RW - total)//2
            y = y0 + i*lh
            draw.text((x0, y), p1, font=hf, fill=tv.ACCENT)
            draw.text((x0+p1w, y), p2, font=hf, fill=(30,32,35) if tv.TERM_BG[0]>200 else (230,237,243))
    # sub
    sub_y = y0 + 2*lh + 30
    # accent line
    draw.rectangle([tv.RW//2-60, sub_y-14, tv.RW//2+60, sub_y-10], fill=tv.ACCENT)
    sw = tv.tw(draw, sub, tv.HOOK_SUB_FONT)
    sx = (tv.RW - sw)//2
    draw.text((sx, sub_y), sub, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # bottom pill
    keep = "WATCH TILL END  →"
    kw = tv.tw(draw, keep, tv.FONT)
    kx = (tv.RW - kw)//2
    ky = sub_y + 50
    draw.rounded_rectangle([kx-18, ky-10, kx+kw+18, ky+30], radius=12, fill=tv.ACCENT)
    draw.text((kx, ky), keep, font=tv.FONT, fill=tv.TERM_BG)
    return img

def variant_3(title, sub):
    # Terminal window style hook
    tv.apply_theme("github")  # dark terminal
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # simulate terminal typed hook as if cat
    # top badge smaller
    badge = "  cat hook.txt  "
    bw = tv.tw(draw, badge, tv.FONT)
    bx = (tv.RW - bw)//2
    by = int(tv.RH*0.28)
    draw.rounded_rectangle([bx-14, by-8, bx+bw+14, by+30], radius=10, fill=(38,46,62))
    draw.text((bx, by), badge, font=tv.FONT, fill=(190,198,212))
    # title as if output
    max_w = tv.RW - 80
    segs = tv._hook_title_segs(title)
    rows = tv.wrap_segments(segs, max_w, draw, tv.HOOK_TITLE_FONT)
    lh = int(HOOK_TITLE_SIZE*1.28)
    y0 = int(tv.RH*0.38)
    for ri, rsegs in enumerate(rows):
        full_w = sum(tv.tw(draw, t, tv.HOOK_TITLE_FONT) for t,_ in rsegs)
        x0 = (tv.RW - full_w)//2
        cx = x0
        for txt,col in rsegs:
            draw.text((cx, y0+ri*lh), txt, font=tv.HOOK_TITLE_FONT, fill=col)
            cx += tv.tw(draw, txt, tv.HOOK_TITLE_FONT)
    # sub as dim command output below
    sub_y = y0 + len(rows)*lh + 30
    sw = tv.tw(draw, sub, tv.HOOK_SUB_FONT)
    sx = (tv.RW - sw)//2
    draw.text((sx, sub_y), sub, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # cursor
    draw.rectangle([sx+sw+8, sub_y+6, sx+sw+8+12, sub_y+HOOK_SUB_SIZE+6], fill=tv.CURSOR_COLOR)
    return img

def variant_4(title, sub):
    # Gradient split — top accent bar, centered
    tv.apply_theme("ice")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # top accent bar
    draw.rectangle([0, 0, tv.RW, 14], fill=tv.ACCENT)
    # badge
    badge = "  60-SECOND FIX  "
    bw = tv.tw(draw, badge, tv.FONT)
    bx = (tv.RW - bw)//2
    by = int(tv.RH*0.24)
    draw.rounded_rectangle([bx-16, by-8, bx+bw+16, by+32], radius=12, fill=tv.ACCENT)
    draw.text((bx, by), badge, font=tv.FONT, fill=(255,255,255) if tv.ACCENT[0]<200 else tv.TERM_BG)
    # title
    segs = tv._hook_title_segs(title)
    max_w = tv.RW - 70
    rows = tv.wrap_segments(segs, max_w, draw, tv.HOOK_TITLE_FONT)
    lh = int(HOOK_TITLE_SIZE*1.28)
    y0 = int(tv.RH*0.35)
    for ri, rsegs in enumerate(rows):
        full_w = sum(tv.tw(draw, t, tv.HOOK_TITLE_FONT) for t,_ in rsegs)
        x0 = (tv.RW - full_w)//2
        cx = x0
        for txt,col in rsegs:
            draw.text((cx, y0+ri*lh), txt, font=tv.HOOK_TITLE_FONT, fill=col)
            cx += tv.tw(draw, txt, tv.HOOK_TITLE_FONT)
    # sub
    sub_y = y0 + len(rows)*lh + 30
    sw = tv.tw(draw, sub, tv.HOOK_SUB_FONT)
    sx = (tv.RW - sw)//2
    draw.text((sx, sub_y), sub, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # bottom line
    draw.rectangle([tv.RW//2-70, sub_y+45, tv.RW//2+70, sub_y+49], fill=tv.ACCENT)
    keep = "KEEP WATCHING  ▶"
    kw = tv.tw(draw, keep, tv.FONT)
    kx = (tv.RW - kw)//2
    ky = sub_y + 60
    draw.text((kx, ky), keep, font=tv.FONT, fill=tv.NUM_COLOR)
    return img

def variant_5(title, sub):
    # Question hook — large "?" accent
    tv.apply_theme("paper")
    img = tv.TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    # huge question mark watermark behind?
    # badge
    badge = "  QUESTION FOR YOU  "
    bw = tv.tw(draw, badge, tv.FONT)
    bx = (tv.RW - bw)//2
    by = int(tv.RH*0.25)
    draw.rounded_rectangle([bx-16, by-8, bx+bw+16, by+32], radius=12, fill=(38,46,62))
    draw.text((bx, by), badge, font=tv.FONT, fill=(250,240,220))
    # title as question
    q_title = "Still using\nweak passwords?"
    lines = q_title.split("\n")
    hf = load_bold(HOOK_TITLE_SIZE)
    y0 = int(tv.RH*0.34)
    lh = int(HOOK_TITLE_SIZE*1.3)
    for i, line in enumerate(lines):
        # color weak red in second line
        if i==1 and "weak" in line:
            # split
            pre = "weak"
            post = " passwords?"
            pre_w = tv.tw(draw, pre, hf)
            post_w = tv.tw(draw, post, hf)
            total = pre_w + post_w
            x0 = (tv.RW - total)//2
            y = y0 + i*lh
            draw.rounded_rectangle([x0-10, y-6, x0+pre_w+10, y+lh-10], radius=10, fill=tv.ERROR_COLOR)
            draw.text((x0, y), pre, font=hf, fill=(255,255,255))
            draw.text((x0+pre_w, y), post, font=hf, fill=(50,45,30) if tv.TERM_BG[0]>200 else (230,237,243))
        else:
            w = tv.tw(draw, line, hf)
            x0 = (tv.RW - w)//2
            draw.text((x0, y0+i*lh), line, font=hf, fill=(50,45,30) if tv.TERM_BG[0]>200 else (230,237,243))
    # sub
    sub_y = y0 + 2*lh + 32
    sw = tv.tw(draw, sub, tv.HOOK_SUB_FONT)
    sx = (tv.RW - sw)//2
    draw.text((sx, sub_y), sub, font=tv.HOOK_SUB_FONT, fill=tv.OUTPUT_COLOR)
    # accent arrow
    keep = "ANSWER INSIDE  →"
    kw = tv.tw(draw, keep, tv.FONT)
    kx = (tv.RW - kw)//2
    ky = sub_y + 48
    draw.rounded_rectangle([kx-16, ky-8, kx+kw+16, ky+30], radius=12, fill=tv.ACCENT)
    draw.text((kx, ky), keep, font=tv.FONT, fill=(255,255,255))
    return img

if __name__ == "__main__":
    title = "Stop using weak passwords"
    sub = "Let's fix that in 60 seconds"
    variants = [
        ("hook_1_pill_modern.png", variant_1),
        ("hook_2_stacked.png", variant_2),
        ("hook_3_terminal.png", variant_3),
        ("hook_4_gradient.png", variant_4),
        ("hook_5_question.png", variant_5),
    ]
    for fname, func in variants:
        img = func(title, sub)
        path = os.path.join(OUT_DIR, fname)
        img.save(path)
        print(f"Saved {path} ({img.size})")
    # also generate light-theme vs dark proof: render a terminal and editor sample for light theme visibility
    for theme in ["light","paper","ice","github","dracula"]:
        tv.apply_theme(theme)
        # terminal sample
        term_entry = {"type":"terminal","buffer":[[(f"~$ ", tv.PROMPT_COLOR),("python3 --version", tv.CMD_COLOR)], [("Python 3.12.1", tv.OUTPUT_COLOR)]],"partial":[(f"~/{'vault' if theme!='github' else ''}$ ",tv.PWD_COLOR),("",tv.CMD_COLOR)],"cursor":True}
        # Actually buffer needs segs list? Use simple
        # Let's just render via tv.render_terminal using proper entry
        entry = {"type":"terminal","buffer":[[(f"~$ ",tv.PROMPT_COLOR),("python3 --version",tv.CMD_COLOR)], [("Python 3.12.1",tv.OUTPUT_COLOR)]],"partial":[(f"~/vault$ ",tv.PWD_COLOR),("ls",tv.CMD_COLOR)],"cursor":True}
        img = tv.render_terminal(entry)
        # overlay small caption to show theme name
        d = ImageDraw.Draw(img)
        txt = f"theme: {theme}"
        bw = tv.tw(d, txt, tv.FONT)
        d.rounded_rectangle([tv.RW-bw-32, 8, tv.RW-16, 36], radius=8, fill=tv.ACCENT)
        d.text((tv.RW-bw-24, 12), txt, font=tv.FONT, fill=tv.TERM_BG)
        p = os.path.join(OUT_DIR, f"theme_{theme}_terminal.png")
        img.save(p)
        print(f"Saved theme proof {p}")
        # editor sample
        tv.apply_theme(theme)
        lines = ["import secrets, string","","def gen(length=16):",'    chars = "abc"', '    return "".join(x)']
        entry2 = {"type":"explain","file":"vault/passgen.py","lines":lines,"active":2,"phase":"center","t":1.0}
        # Need to ensure explain full cache cleared already by apply_theme
        img2 = tv.render_explain(entry2)
        d2 = ImageDraw.Draw(img2)
        d2.rounded_rectangle([tv.RW-bw-32, 8, tv.RW-bw-32+120, 36], radius=8, fill=tv.ACCENT)
        d2.text((tv.RW-bw-24, 12), txt, font=tv.FONT, fill=tv.TERM_BG)
        p2 = os.path.join(OUT_DIR, f"theme_{theme}_editor.png")
        img2.save(p2)
        print(f"Saved theme proof {p2}")
