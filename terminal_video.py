#!/usr/bin/env python3
"""
Terminal Tutorial Video Generator v9
====================================
Scene types:
  - hook:     big title hook on terminal screen
  - terminal: command typed + executed for real (live cwd prompt)
  - editor:   code typed char-by-char (classic)
  - explain:  motion-design walkthrough — line pops BIG in center
              (wrapped) then flies into place; blank lines auto-filled,
              no green arrows
"""

import subprocess
import os
import sys
import time
import random
import json
import re
import wave
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

# ================= SETTINGS =================
WIDTH, HEIGHT = 1080, 1920
RENDER_SCALE = 1
RW, RH = WIDTH * RENDER_SCALE, HEIGHT * RENDER_SCALE
FPS = 30
SR = 44100

FONT_SIZE = 38 * RENDER_SCALE
LINE_HEIGHT = 54 * RENDER_SCALE
PAD_X = 24 * RENDER_SCALE

STATUS_H = 64 * RENDER_SCALE
GUTTER_W = 76 * RENDER_SCALE
CODE_X = 96 * RENDER_SCALE
Y0 = 96 * RENDER_SCALE

TERM_BG = (13, 17, 23)
EDITOR_BG = (18, 22, 30)
ACTIVE_LINE = (32, 42, 58)
CARD_BG = (28, 35, 48)
STATUS_BG = (33, 37, 43)
NUM_COLOR = (92, 99, 112)

PWD_COLOR = (88, 166, 255)
PROMPT_COLOR = (63, 185, 80)
CMD_COLOR = (230, 237, 243)
OUTPUT_COLOR = (139, 148, 158)
ERROR_COLOR = (248, 81, 73)
CURSOR_COLOR = (63, 185, 80)
ACCENT = (88, 166, 255)

IS_TERMUX = os.path.isdir("/data/data/com.termux") or bool(os.environ.get("TERMUX_VERSION"))
DOCS_DIR = "/storage/emulated/0/Documents" if IS_TERMUX else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "output"
)
WORK_DIR = os.path.join(os.path.expanduser("~"), ".terminal_video_tmp")
WRITTEN_FILES = []

FONT_CANDIDATES = [
    os.environ.get("FONT_PATH", ""),
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
    "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf",
    "/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf",
    os.path.expanduser("~/.fonts/DejaVuSansMono.ttf"),
    "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono.ttf",
]

MAX_LINES = max(6, (RH - Y0 - STATUS_H - 20 * RENDER_SCALE) // LINE_HEIGHT)

DEFAULT_CONFIG_YAML = """\
voice: "en-US-GuyNeural"

steps:
  - type: hook
    title: "Stop using weak passwords"
    sub: "Let's fix that in 60 seconds"

  - narration: "First up — let's make sure Python is ready. This just prints your version."
    command: "python3 --version"

  - narration: "We need a place for our project. mkdir means make directory — so we're creating a folder called vault."
    command: "mkdir vault"

  - narration: "Now we'll jump inside. cd means change directory — think of it as opening that folder."
    command: "cd vault"

  - narration: "Let's check what's in here. ls lists files — and yep, it's empty. Fresh start."
    command: "ls"

  - type: explain
    file: "vault/passgen.py"
    intro: "Watch me type the whole script, then I'll walk you through it."
    code: |
      import secrets, string

      def gen(length=16):
          chars = string.ascii_letters + string.digits + "!@#$%^&*"
          return "".join(secrets.choice(chars) for _ in range(length))

      for i in range(5):
          print(f"Password {i+1}: {gen()}")
    lines:
      - line: 1
        say: "We import secrets — Python's secure random module."
      - line: 3
        say: "gen() builds one password of a given length."
      - line: 4
        say: "The pool mixes letters, digits and symbols."
      - line: 5
        say: "We pick random chars and join them."
      - line: 7
        say: "The loop runs five times."
      - line: 8
        say: "Then we print each password."

  - narration: "Moment of truth — let's run it. We're in the vault folder, so just python3 passgen.py."
    command: "python3 passgen.py"

  - narration: "Love it? Follow for more Python tricks and subscribe so you don't miss the next one."
    command: "echo Follow  •  Subscribe  •  More coming soon!"
"""

# ================= FONT =================

def load_font():
    for path in FONT_CANDIDATES:
        if path and os.path.isfile(path):
            try:
                return ImageFont.truetype(path, FONT_SIZE), path
            except Exception:
                continue
    return ImageFont.load_default(), None

FONT, FONT_PATH = load_font()
CENTER_FONT_SIZE = int(FONT_SIZE * 1.10)
try:
    CENTER_FONT = ImageFont.truetype(FONT_PATH, CENTER_FONT_SIZE) if FONT_PATH else FONT
except Exception:
    CENTER_FONT = FONT

# Hook fonts — bold for punch
HOOK_TITLE_SIZE = 68 * RENDER_SCALE
HOOK_SUB_SIZE = 36 * RENDER_SCALE
BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
HOOK_TITLE_FONT = FONT
HOOK_SUB_FONT = FONT
for bp in BOLD_CANDIDATES:
    if os.path.isfile(bp):
        try:
            HOOK_TITLE_FONT = ImageFont.truetype(bp, HOOK_TITLE_SIZE)
            break
        except Exception:
            continue
try:
    if FONT_PATH:
        HOOK_SUB_FONT = ImageFont.truetype(FONT_PATH, HOOK_SUB_SIZE)
except Exception:
    pass


def tw(draw, text, font=FONT):
    if not text:
        return 0
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    return r - l

def th(draw, text, font=FONT):
    if not text:
        return 0
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    return b - t

def ease_out(t):
    return 1 - (1 - t) ** 3

def ease_io(t):
    return t * t * (3 - 2 * t)

# ================= WRAPPING =================

def wrap_segments(segs, max_w, draw, font=FONT):
    words = []
    for text, color in segs:
        if not text:
            continue
        parts = text.split(" ")
        for i, part in enumerate(parts):
            if i > 0:
                words.append((" ", color))
            if part:
                words.append((part, color))
    result = [[]]
    x = 0
    for word_text, word_color in words:
        ww = tw(draw, word_text, font)
        if word_text == " ":
            if x + ww <= max_w:
                result[-1].append((word_text, word_color))
                x += ww
            continue
        if x + ww <= max_w:
            result[-1].append((word_text, word_color))
            x += ww
        else:
            if x > 0:
                result.append([])
            if ww > max_w:
                chunk = ""
                for ch in word_text:
                    test = chunk + ch
                    if tw(draw, test, font) > max_w:
                        if chunk:
                            result[-1].append((chunk, word_color))
                            result.append([])
                        chunk = ch
                    else:
                        chunk = test
                if chunk:
                    result[-1].append((chunk, word_color))
                    x = tw(draw, chunk, font)
            else:
                result[-1].append((word_text, word_color))
                x = ww
    if result and not result[-1]:
        result.pop()
    return result

def wrap_output(raw, color, draw):
    out = []
    max_w = RW - 2 * PAD_X
    for line in (raw or "").splitlines() or [""]:
        if not line:
            out.append([("", color)])
            continue
        for w in wrap_segments([(line, color)], max_w, draw, FONT):
            out.append(w)
    return out

# ================= SYNTAX HIGHLIGHTING =================
SY_KW = (198, 120, 221)
SY_STR = (152, 195, 121)
SY_NUM = (209, 154, 102)
SY_COM = (92, 99, 112)
SY_FN = (97, 175, 239)
SY_BI = (86, 182, 194)
SY_PLAIN = (171, 178, 191)

KEYWORDS = {"def", "return", "import", "from", "for", "in", "if", "elif", "else",
            "while", "class", "with", "as", "not", "and", "or", "True", "False",
            "None", "lambda", "try", "except", "finally", "raise", "pass", "break", "continue"}
BUILTINS = {"print", "range", "len", "str", "int", "float", "list", "dict", "set",
            "open", "input", "sum", "min", "max", "sorted", "enumerate", "zip"}
TOKEN_RE = re.compile(
    r"(?P<comment>#.*)"
    r'|(?P<string>f?"""(?:[^"\\]|\\.)*"""|f?\'\'\'(?:[^\'\\]|\\.)*\'\'\'|f?"(?:[^"\\]|\\.)*"|f?\'(?:[^\'\\]|\\.)*\')'
    r"|(?P<number>\b\d[\d_]*\.?\d*\b)"
    r"|(?P<word>[A-Za-z_]\w*)"
    r"|(?P<ws> +)"
    r"|(?P<other>.)"
)

def highlight_line(line):
    segs = []
    pos = 0
    for m in TOKEN_RE.finditer(line):
        if m.start() > pos:
            segs.append((line[pos:m.start()], SY_PLAIN))
        kind = m.lastgroup
        txt = m.group()
        if kind == "comment":
            col = SY_COM
        elif kind == "string":
            col = SY_STR
        elif kind == "number":
            col = SY_NUM
        elif kind == "word":
            if txt in KEYWORDS:
                col = SY_KW
            elif txt in BUILTINS:
                col = SY_BI
            elif line[m.end():m.end() + 1] == "(":
                col = SY_FN
            else:
                col = SY_PLAIN
        else:
            col = SY_PLAIN
        segs.append((txt, col))
        pos = m.end()
    if pos < len(line):
        segs.append((line[pos:], SY_PLAIN))
    return segs

# ================= BASE IMAGES =================

def build_term_base():
    img = Image.new("RGB", (RW, RH), TERM_BG)
    draw = ImageDraw.Draw(img)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        cx = 44 * RENDER_SCALE + i * 48 * RENDER_SCALE
        cy = 38 * RENDER_SCALE
        r = 16 * RENDER_SCALE
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    return img

def build_editor_base():
    img = Image.new("RGB", (RW, RH), EDITOR_BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, RH - STATUS_H, RW, RH], fill=STATUS_BG)
    return img

TERM_BASE = build_term_base()
EDITOR_BASE = build_editor_base()

# ================= HOOK SCENE =================

def render_hook(entry):
    title = entry.get("title", "")
    sub = entry.get("sub", "")
    n = entry.get("n", len(title))
    sub_on = entry.get("sub_on", False)
    cursor = entry.get("cursor", False)

    img = TERM_BASE.copy()
    draw = ImageDraw.Draw(img)

    # wrap title into rows using hook font
    max_w = RW - 120 * RENDER_SCALE
    title_segs = [(title, (230, 237, 243))]
    rows = wrap_segments(title_segs, max_w, draw, HOOK_TITLE_FONT)
    # flatten rows to reconstruct display with spaces
    # Build display strings per row clipped to n chars total
    # First flatten title into chars including implicit wrap newlines
    # Simpler: walk rows and consume n chars
    lh = int(HOOK_TITLE_SIZE * 1.35)
    total_h = len(rows) * lh if rows else lh
    y0 = int(RH * 0.38) - total_h // 2

    remaining = n
    # for cursor position track last drawn char pos
    last_x = 0
    last_y = y0
    last_row_w = 0
    row_idx = 0
    for ri, rsegs in enumerate(rows):
        # reconstruct plain row text for width calc
        plain = "".join(t for t, _ in rsegs)
        if remaining <= 0:
            # draw nothing for this row yet
            pass
        else:
            take = min(len(plain), remaining)
            # need to take chars from segs proportionally
            chars_left = take
            cx = 0
            # compute centered x for full row (so typing stays centered)
            full_w = tw(draw, plain, HOOK_TITLE_FONT)
            x0 = int(RW / 2 - full_w / 2)
            cx = x0
            segs_to_draw = []
            for txt, col in rsegs:
                if chars_left <= 0:
                    break
                piece = txt[:chars_left]
                if piece:
                    draw.text((cx, y0 + ri * lh), piece, font=HOOK_TITLE_FONT, fill=(230, 237, 243))
                    cx += tw(draw, piece, HOOK_TITLE_FONT)
                chars_left -= len(txt)
            last_x = cx
            last_y = y0 + ri * lh
            last_row_w = full_w
            row_idx = ri
        remaining -= len("".join(t for t, _ in rsegs))
        # also account for space that wrap removed? wrap_segments splits on space,
        # so join length is close enough; remaining logic still works because
        # spaces are explicit " " segs counted.
        if remaining < 0:
            remaining = 0

    if cursor and n < len(title) + 2:
        cw = max(8 * RENDER_SCALE, int(HOOK_TITLE_SIZE * 0.35))
        # place cursor at last_x
        draw.rectangle([last_x + 6, last_y + 8, last_x + 6 + cw, last_y + int(HOOK_TITLE_SIZE * 1.05)], fill=CURSOR_COLOR)

    if sub_on and sub:
        max_sw = RW - 140 * RENDER_SCALE
        sub_rows = wrap_segments([(sub, OUTPUT_COLOR)], max_sw, draw, HOOK_SUB_FONT)
        sub_lh = int(HOOK_SUB_SIZE * 1.35)
        sub_y = y0 + total_h + 48 * RENDER_SCALE
        for sr in sub_rows:
            plain = "".join(t for t, _ in sr)
            sw = tw(draw, plain, HOOK_SUB_FONT)
            sx = int(RW / 2 - sw / 2)
            cx = sx
            for txt, col in sr:
                if txt:
                    draw.text((cx, sub_y), txt, font=HOOK_SUB_FONT, fill=OUTPUT_COLOR)
                cx += tw(draw, txt, HOOK_SUB_FONT)
            sub_y += sub_lh

    # tiny accent line under title
    if sub_on:
        line_w = 80 * RENDER_SCALE
        draw.rectangle([RW//2 - line_w//2, y0 + total_h + 18*RENDER_SCALE,
                        RW//2 + line_w//2, y0 + total_h + 22*RENDER_SCALE], fill=ACCENT)
    return img

# ================= EXPLAIN SCENE =================
_EXPLAIN_FULL_CACHE = {}
_EXPLAIN_BG_CACHE = {}

def _draw_code_block(img, lines, indices, dim=1.0):
    d = ImageDraw.Draw(img)
    max_w = RW - CODE_X - 30 * RENDER_SCALE
    row = 0
    for i in indices:
        line = lines[i]
        num = str(i + 1)
        nw = tw(d, num)
        col = tuple(int(c * dim) for c in NUM_COLOR)
        d.text((GUTTER_W - nw - 12 * RENDER_SCALE, Y0 + row * LINE_HEIGHT), num, font=FONT, fill=col)
        segs = highlight_line(line)
        segs = [(t, tuple(int(c * dim) for c in cc)) for t, cc in segs]
        wrapped = wrap_segments(segs, max_w, d, FONT) if line else []
        if not wrapped:
            wrapped = [[("", SY_PLAIN)]]
        for vsegs in wrapped:
            yy = Y0 + row * LINE_HEIGHT
            cx = CODE_X
            for text, color in vsegs:
                if text:
                    d.text((cx, yy), text, font=FONT, fill=color)
                cx += tw(d, text)
            row += 1

def count_rows(lines, indices):
    row = 0
    for i in indices:
        line = lines[i]
        if not line:
            row += 1
            continue
        wrapped = wrap_segments(highlight_line(line), RW - CODE_X - 30 * RENDER_SCALE,
                                ImageDraw.Draw(Image.new("RGB", (8, 8))), FONT)
        row += max(1, len(wrapped))
    return row

def target_row_of(lines, idx, settled):
    rows_before = count_rows(lines, [i for i in sorted(settled) if i < idx])
    return rows_before, count_rows(lines, [idx])

def get_explain_full(lines):
    key = tuple(lines)
    if key in _EXPLAIN_FULL_CACHE:
        return _EXPLAIN_FULL_CACHE[key]
    img = EDITOR_BASE.copy()
    _draw_code_block(img, lines, range(len(lines)), dim=1.0)
    _EXPLAIN_FULL_CACHE[key] = img
    return img

def get_explain_bg(lines, settled):
    key = tuple(sorted(settled))
    if key in _EXPLAIN_BG_CACHE:
        return _EXPLAIN_BG_CACHE[key]
    img = EDITOR_BASE.copy()
    _draw_code_block(img, lines, key, dim=0.82)
    img = img.filter(ImageFilter.GaussianBlur(1.6 * RENDER_SCALE))
    img = ImageEnhance.Brightness(img).enhance(0.94)
    _EXPLAIN_BG_CACHE[key] = img
    return img

def render_line_image_wrapped(line, font, max_w):
    """Render a (potentially long) line into a wrapped multi-row RGBA image."""
    if not line:
        return None
    tmp = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    segs = highlight_line(line)
    rows = wrap_segments(segs, max_w, d, font)
    if not rows:
        return None
    # measure
    lh = int(CENTER_FONT_SIZE * 1.35) if font == CENTER_FONT else int(FONT_SIZE * 1.3)
    max_row_w = 0
    for r in rows:
        w = sum(tw(d, t, font) for t, _ in r)
        max_row_w = max(max_row_w, w)
    H = len(rows) * lh + 24
    W = max_row_w + 16
    # render onto cropped
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(img)
    y = 8
    indent = tw(dd, "  ", font)
    for ri, rsegs in enumerate(rows):
        x = indent if ri > 0 else 0
        for txt, col in rsegs:
            if txt:
                dd.text((x, y), txt, font=font, fill=col)
            x += tw(dd, txt, font)
        y += lh
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else None

def draw_header(draw, fname):
    draw.text((PAD_X, 26 * RENDER_SCALE), fname, font=FONT, fill=ACCENT)

def draw_statusbar(draw, fname):
    sy = RH - STATUS_H
    draw.text((20 * RENDER_SCALE, sy + 13 * RENDER_SCALE), fname, font=FONT, fill=(230, 237, 243))
    py = "Python"
    pw = tw(draw, py)
    draw.text((RW - pw - 20 * RENDER_SCALE, sy + 13 * RENDER_SCALE), py, font=FONT, fill=(97, 175, 239))

def render_explain(entry):
    lines = entry["lines"]
    active = entry["active"]
    phase = entry["phase"]
    t = entry.get("t", 1.0)
    fname = entry["file"]
    if phase == "final":
        img = EDITOR_BASE.copy()
        _draw_code_block(img, lines, range(len(lines)), dim=1.0)
        draw = ImageDraw.Draw(img)
        draw_header(draw, fname)
        draw_statusbar(draw, fname)
        return img

    # full code always visible as background
    img = get_explain_full(lines).copy()
    draw = ImageDraw.Draw(img)
    draw_header(draw, fname)
    draw_statusbar(draw, fname)

    if active is None:
        return img

    line = lines[active] if 0 <= active < len(lines) else ""
    # max width for center card — keep comfortable padding
    max_center_w = RW - 220 * RENDER_SCALE
    li_img = render_line_image_wrapped(line, CENTER_FONT, max_center_w) if line else None

    # target row in full code (not settled subset)
    rows_before = count_rows(lines, list(range(active))) if active is not None else 0
    own_rows = count_rows(lines, [active]) if active is not None else 1
    tgt_y = Y0 + rows_before * LINE_HEIGHT
    tgt_x = CODE_X

    # highlight in place — brief flash before lift and after return
    if phase in ("highlight", "settled"):
        draw.rectangle([0, tgt_y - 3, RW, tgt_y + own_rows * LINE_HEIGHT - 9], fill=ACTIVE_LINE)
        num = str(active + 1)
        nw = tw(draw, num)
        draw.text((GUTTER_W - nw - 12 * RENDER_SCALE, tgt_y), num, font=FONT, fill=(210, 216, 224))
        segs = highlight_line(line)
        max_w = RW - CODE_X - 30 * RENDER_SCALE
        wrapped = wrap_segments(segs, max_w, draw, FONT) if line else []
        if not wrapped:
            wrapped = [[("", SY_PLAIN)]]
        yy = tgt_y
        for vsegs in wrapped:
            cx = CODE_X
            for text, color in vsegs:
                if text:
                    draw.text((cx, yy), text, font=FONT, fill=color)
                cx += tw(draw, text)
            yy += LINE_HEIGHT
        return img

    # for lift/center/return we hide original line with a ghost placeholder
    draw.rectangle([0, tgt_y - 3, RW, tgt_y + own_rows * LINE_HEIGHT - 9], fill=(26, 32, 44))
    # subtle dashed gutter number dimmed
    if line:
        num = str(active + 1)
        nw = tw(draw, num)
        draw.text((GUTTER_W - nw - 12 * RENDER_SCALE, tgt_y), num, font=FONT, fill=(60, 68, 82))

    cy = int(RH * 0.40)
    ratio = FONT_SIZE / CENTER_FONT_SIZE

    if phase == "lift":
        e = ease_io(min(1.0, t))
        if li_img:
            w, h = li_img.size
            # centered target
            cx_target = int(RW / 2 - w / 2)
            cy_target = int(cy - h / 2)
            cur_x = int(tgt_x + (cx_target - tgt_x) * e)
            cur_y = int(tgt_y + 4 + (cy_target - (tgt_y + 4)) * e)
            scale = ratio + (1.0 - ratio) * e
            sw, sh = max(1, int(w * scale)), max(1, int(h * scale))
            frame = li_img.resize((sw, sh), Image.LANCZOS)
            # shadow
            pad_x, pad_y = int(32 * scale), int(22 * scale)
            draw.rounded_rectangle(
                [cur_x - pad_x + 6, cur_y - pad_y + 6, cur_x + sw + pad_x + 6, cur_y + sh + pad_y + 6],
                radius=16 * RENDER_SCALE, fill=(15, 20, 28))
            draw.rounded_rectangle(
                [cur_x - pad_x, cur_y - pad_y, cur_x + sw + pad_x, cur_y + sh + pad_y],
                radius=16 * RENDER_SCALE, fill=CARD_BG, outline=(52, 60, 74), width=1 * RENDER_SCALE)
            img.paste(frame, (cur_x, cur_y), frame)

    elif phase == "center":
        e = ease_out(min(1.0, t))
        scale = 0.86 + 0.14 * e
        if li_img:
            w, h = li_img.size
            sw, sh = int(w * scale), int(h * scale)
            frame = li_img.resize((max(1, sw), max(1, sh)), Image.LANCZOS)
            px, py = int(RW / 2 - sw / 2), int(cy - sh / 2)
            pad_x, pad_y = int(36 * scale), int(24 * scale)
            # shadow
            draw.rounded_rectangle(
                [px - pad_x + 6 * RENDER_SCALE, py - pad_y + 6 * RENDER_SCALE,
                 px + sw + pad_x + 6 * RENDER_SCALE, py + sh + pad_y + 6 * RENDER_SCALE],
                radius=16 * RENDER_SCALE, fill=(15, 20, 28))
            # card
            draw.rounded_rectangle(
                [px - pad_x, py - pad_y, px + sw + pad_x, py + sh + pad_y],
                radius=16 * RENDER_SCALE, fill=CARD_BG, outline=(52, 60, 74), width=1 * RENDER_SCALE)
            img.paste(frame, (px, py), frame)
        # clean badge — small pill centered above card
        badge = f"Line {active + 1}"
        bw = tw(draw, badge, FONT)
        # position above card
        card_top = cy - (li_img.height * scale // 2 if li_img else 0) - 24 * RENDER_SCALE if li_img else cy
        bx, by = int(RW / 2 - bw / 2), int(card_top - LINE_HEIGHT * 1.05)
        draw.rounded_rectangle([bx - 16 * RENDER_SCALE, by - 6 * RENDER_SCALE,
                                bx + bw + 16 * RENDER_SCALE, by + LINE_HEIGHT - 10 * RENDER_SCALE],
                               radius=12 * RENDER_SCALE, fill=(38, 46, 62))
        draw.text((bx, by + 2), badge, font=FONT, fill=(190, 198, 212))

    elif phase == "return":
        e = ease_io(min(1.0, t))
        if li_img:
            w, h = li_img.size
            cx_start = int(RW / 2 - w / 2)
            cy_start = int(cy - h / 2)
            cur_x = int(cx_start + (tgt_x - cx_start) * e)
            cur_y = int(cy_start + (tgt_y + 4 - cy_start) * e)
            scale = 1.0 + (ratio - 1.0) * e
            sw, sh = max(1, int(w * scale)), max(1, int(h * scale))
            frame = li_img.resize((sw, sh), Image.LANCZOS)
            pad_x, pad_y = int(32 * scale), int(22 * scale)
            draw.rounded_rectangle(
                [cur_x - pad_x + 6, cur_y - pad_y + 6, cur_x + sw + pad_x + 6, cur_y + sh + pad_y + 6],
                radius=16 * RENDER_SCALE, fill=(15, 20, 28))
            draw.rounded_rectangle(
                [cur_x - pad_x, cur_y - pad_y, cur_x + sw + pad_x, cur_y + sh + pad_y],
                radius=16 * RENDER_SCALE, fill=CARD_BG, outline=(52, 60, 74), width=1 * RENDER_SCALE)
            img.paste(frame, (cur_x, cur_y), frame)

    return img

# ================= TERMINAL / EDITOR RENDER =================

def render_terminal(entry):
    img = TERM_BASE.copy()
    draw = ImageDraw.Draw(img)
    buffer = entry["buffer"]
    partial = entry["partial"]
    cursor_on = entry["cursor"]
    lines = list(buffer)
    if partial is not None:
        lines.append(partial)
    y0 = 90 * RENDER_SCALE
    x0 = PAD_X
    max_w = RW - 2 * PAD_X
    all_visual = []
    for segs in lines:
        all_visual.extend(wrap_segments(segs, max_w, draw, FONT))
    visible = all_visual[-MAX_LINES:]
    for li, segs in enumerate(visible):
        y = y0 + li * LINE_HEIGHT
        if y + LINE_HEIGHT > RH - 20 * RENDER_SCALE:
            break
        x = x0
        for text, color in segs:
            if text:
                draw.text((x, y), text, font=FONT, fill=color)
            x += tw(draw, text)
        if li == len(visible) - 1 and partial is not None and cursor_on:
            cw = max(8 * RENDER_SCALE, int(FONT_SIZE * 0.55))
            draw.rectangle([x + 2, y + 4, x + 2 + cw, y + FONT_SIZE + 4], fill=CURSOR_COLOR)
    return img

def render_editor(entry):
    img = EDITOR_BASE.copy()
    draw = ImageDraw.Draw(img)
    typed = entry["typed"]
    cursor_on = entry["cursor"]
    code_lines = typed.split("\n")
    cur_line_idx = len(code_lines) - 1
    cur_col = len(code_lines[-1])
    start = max(0, len(code_lines) - MAX_LINES)
    vis = code_lines[start:]
    y0 = 36 * RENDER_SCALE
    max_w = RW - CODE_X - 30 * RENDER_SCALE
    row = 0
    cur_x, cur_y = CODE_X, y0
    for li, line in enumerate(vis):
        real_idx = start + li
        y = y0 + row * LINE_HEIGHT
        if y + LINE_HEIGHT > RH - STATUS_H - 10 * RENDER_SCALE:
            break
        if real_idx == cur_line_idx:
            draw.rectangle([0, y - 3, RW, y + LINE_HEIGHT - 9], fill=ACTIVE_LINE)
        num = str(real_idx + 1)
        nw = tw(draw, num)
        draw.text((GUTTER_W - nw - 12 * RENDER_SCALE, y), num, font=FONT, fill=NUM_COLOR)
        segs = highlight_line(line)
        wrapped = wrap_segments(segs, max_w, draw, FONT) if line else []
        if not wrapped:
            wrapped = [[("", SY_PLAIN)]]
        for vsegs in wrapped:
            yy = y0 + row * LINE_HEIGHT
            cx = CODE_X
            for text, color in vsegs:
                if text:
                    draw.text((cx, yy), text, font=FONT, fill=color)
                cx += tw(draw, text)
            row += 1
            if real_idx == cur_line_idx:
                cur_x, cur_y = cx, yy
    if cursor_on:
        cw = max(8 * RENDER_SCALE, int(FONT_SIZE * 0.55))
        draw.rectangle([cur_x + 2, cur_y + 4, cur_x + 2 + cw, cur_y + FONT_SIZE + 4], fill=CURSOR_COLOR)
    sy = RH - STATUS_H
    draw.text((20 * RENDER_SCALE, sy + 13 * RENDER_SCALE), entry["file"], font=FONT, fill=(230, 237, 243))
    info = f"Ln {cur_line_idx + 1}, Col {cur_col + 1}"
    iw = tw(draw, info)
    draw.text((RW - iw - 220 * RENDER_SCALE, sy + 13 * RENDER_SCALE), info, font=FONT, fill=NUM_COLOR)
    py = "Python"
    pw = tw(draw, py)
    draw.text((RW - pw - 20 * RENDER_SCALE, sy + 13 * RENDER_SCALE), py, font=FONT, fill=(97, 175, 239))
    return img

def render_frame(entry):
    t = entry["type"]
    if t == "editor":
        return render_editor(entry)
    if t == "explain":
        return render_explain(entry)
    if t == "hook":
        return render_hook(entry)
    return render_terminal(entry)

def cursor_state(fc):
    return (fc // (FPS // 2)) % 2 == 0

# ================= AUDIO =================

def tts_generate(text, voice, out_path):
    subprocess.run(["edge-tts", "--voice", voice, "--text", text, "--write-media", out_path],
                   check=True, capture_output=True)

def decode_audio(path):
    r = subprocess.run(["ffmpeg", "-y", "-i", path, "-ar", str(SR), "-ac", "1", "-f", "s16le", "-"],
                       capture_output=True)
    if not r.stdout:
        return np.zeros(0, dtype=np.float32)
    return np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768.0

def tts_pcm(text, voice, tag):
    p = os.path.join(WORK_DIR, f"{tag}.mp3")
    tts_generate(text, voice, p)
    return decode_audio(p)

def _bandpass_noise(rng, n, lo, hi):
    x = rng.standard_normal(n).astype(np.float32)
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(n, 1.0 / SR)
    mask = (freqs >= lo) & (freqs <= hi)
    X[~mask] = 0
    y = np.fft.irfft(X, n).astype(np.float32)
    m = np.max(np.abs(y))
    if m > 1e-6:
        y /= m
    return y

def synth_key_press(rng, deep=False):
    dur = 0.072 if deep else 0.055
    n = int(SR * dur)
    t = np.arange(n) / SR
    f0 = rng.uniform(95, 125) if deep else rng.uniform(145, 190)
    f1 = f0 * rng.uniform(0.55, 0.70)
    # chirped thock
    thock = np.sin(2 * np.pi * (f0 * t + (f1 - f0) * t * t / (2 * dur)))
    thock *= np.exp(-t * (62 if deep else 88))
    body = _bandpass_noise(rng, n, 220, 900) * np.exp(-t * 130) * 0.55
    tn = int(SR * 0.005)
    tick = _bandpass_noise(rng, tn, 2600 if deep else 3200, 7000)
    env_tick = np.exp(-np.linspace(0, 9, tn))
    tick *= env_tick
    out = np.zeros(n, np.float32)
    out += thock * (0.52 if deep else 0.42) * rng.uniform(0.88, 1.12)
    out += body * rng.uniform(0.7, 1.15)
    out[:tn] += tick * rng.uniform(0.45, 0.85) * (0.7 if deep else 1.0)
    # micro fade in
    fi = max(1, int(SR * 0.0006))
    out[:fi] *= np.linspace(0, 1, fi)
    return (out * 0.55).astype(np.float32)

def synth_key_release(rng):
    n = int(SR * 0.018)
    tick = _bandpass_noise(rng, n, 3800, 8500) * np.exp(-np.linspace(0, 10, n))
    return (tick * 0.11).astype(np.float32)

def add_into(master, start, arr):
    end = min(len(master), start + len(arr))
    if end > start:
        master[start:end] += arr[: end - start]

def write_wav(path, float_arr, sr):
    ints = (np.clip(float_arr, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(ints.tobytes())

# ================= TIMELINE =================
LIFT_FRAMES = 14
RETURN_FRAMES = 14
SETTLE_FRAMES = int(FPS * 0.22)
HIGHLIGHT_FRAMES = 10

def build_timeline(config, voice):
    frames, clicks, narration_events = [], [], []
    fc = [0]
    def now_s():
        return int(round((fc[0] / FPS) * SR))
    def push(frame):
        frames.append(frame)
        fc[0] += 1

    steps = config["steps"]
    total = len(steps)
    mdraw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    buffer = []
    base_dir = os.getcwd()
    cur_dir = base_dir
    def prompt_segs():
        if cur_dir == base_dir:
            pwd = "~"
        else:
            try:
                rel = os.path.relpath(cur_dir, base_dir)
            except ValueError:
                rel = os.path.basename(cur_dir)
            pwd = "~/" + rel
        return [(pwd, PWD_COLOR), ("$ ", PROMPT_COLOR)]
    def update_cwd_from_cmd(cmd):
        nonlocal cur_dir
        # handle multiple cd segments split by && and ;
        for part in re.split(r"&&|;", cmd):
            p = part.strip()
            if p.startswith("cd"):
                rest = p[2:].strip()
                if not rest:
                    cur_dir = base_dir
                else:
                    # take first token (handle quotes)
                    tok = rest.split()[0].strip().strip("'\"")
                    nd = os.path.normpath(os.path.join(cur_dir, tok))
                    if os.path.isdir(nd):
                        cur_dir = nd

    for idx, step in enumerate(steps):
        stype = step.get("type", "terminal")
        # ---------- hook ----------
        if stype == "hook":
            title = step.get("title", "")
            sub = step.get("sub", "")
            # optional narration for hook
            hook_narr = (step.get("narration") or "").strip()
            # typewriter title
            total_chars = len(title)
            # clicks for each char
            for i in range(total_chars):
                ch = title[i]
                deep = ch == " "
                # schedule press immediately
                clicks.append((now_s(), deep, False))
                # release shortly after
                clicks.append((now_s() + int(SR * 0.028), False, True))
                for _ in range(max(1, round(FPS / random.uniform(16, 24)))):
                    push({"type": "hook", "title": title, "sub": sub, "n": i + 1, "sub_on": False, "cursor": True})
            # hold after title typed
            for _ in range(int(FPS * 0.5)):
                push({"type": "hook", "title": title, "sub": sub, "n": total_chars, "sub_on": False, "cursor": cursor_state(fc[0])})
            # reveal sub
            for _ in range(int(FPS * 0.35)):
                push({"type": "hook", "title": title, "sub": sub, "n": total_chars, "sub_on": True, "cursor": False})
            # optional hook narration plays during sub hold
            hold = int(FPS * 0.8)
            if hook_narr:
                try:
                    pcm = tts_pcm(hook_narr, voice, f"s{idx}")
                    narration_events.append((now_s() - int(FPS*0.35/ FPS * SR) - int(0.5*SR), pcm))
                    # Actually align to start of sub reveal; simpler append at sub reveal start
                    # re-append correctly:
                    narration_events.pop()
                    # narration should start when sub appears
                    sub_start = now_s() - int(FPS*0.35/ FPS * SR)
                    # we already pushed sub frames; estimate start = now - 0.35s
                    narration_events.append((max(0, now_s() - int(0.35*SR)), pcm))
                    hold = max(hold, int(round(len(pcm)/SR*FPS)) + int(FPS*0.2))
                except Exception as e:
                    print(f"  [{idx+1}/{total}] hook TTS FAIL: {e}")
            # hold with sub visible
            for _ in range(max(hold, int(FPS*1.0))):
                push({"type": "hook", "title": title, "sub": sub, "n": total_chars, "sub_on": True, "cursor": False})
            print(f"  [{idx+1}/{total}] [hook] {title}")
            continue

        step_narr = (step.get("narration") or "").strip()
        if step_narr:
            try:
                pcm = tts_pcm(step_narr, voice, f"s{idx}")
                narration_events.append((now_s(), pcm))
                hold = max(1, int(round(len(pcm) / SR * FPS)))
            except Exception as e:
                print(f"  [{idx + 1}/{total}] TTS FAIL: {e}")
                hold = int(FPS * 0.5)
        else:
            hold = int(FPS * 0.5)
        # ---------- explain ----------
        if stype == "explain":
            fname = step.get("file", "untitled.py")
            code = step.get("code", "")
            code_lines = code.split("\n")
            reveals = step.get("lines") or []
            intro = (step.get("intro") or "").strip()

            # optional short intro narration while filename header shows
            intro_hold = int(FPS * 0.6)
            if intro:
                try:
                    pcm = tts_pcm(intro, voice, f"s{idx}i")
                    narration_events.append((now_s(), pcm))
                    intro_hold = max(intro_hold, int(round(len(pcm) / SR * FPS)) + int(FPS * 0.2))
                except Exception as e:
                    print(f"  [{idx + 1}/{total}] intro TTS FAIL: {e}")
            for _ in range(intro_hold):
                push({"type": "editor", "file": fname, "typed": "", "cursor": True})

            # PHASE A — type the whole file fast
            typed = ""
            for ch in code:
                typed += ch
                deep = ch in (" ", "\n", "\t")
                clicks.append((now_s(), deep, False))
                clicks.append((now_s() + int(SR * 0.028), False, True))
                for _ in range(max(1, round(FPS / random.uniform(40, 55)))):
                    push({"type": "editor", "file": fname, "typed": typed, "cursor": True})
            for i in range(int(FPS * 0.7)):
                push({"type": "editor", "file": fname, "typed": typed, "cursor": cursor_state(fc[0])})

            # PHASE B — explain each line: highlight → lift → center → return
            for ri, rv in enumerate(reveals):
                ln = max(0, min(int(rv.get("line", 1)) - 1, len(code_lines) - 1))
                say = (rv.get("say") or "").strip()
                dur = int(FPS * 0.5)
                if say:
                    try:
                        pcm = tts_pcm(say, voice, f"s{idx}l{ri}")
                        narration_events.append((now_s(), pcm))
                        dur = max(int(FPS * 0.6), int(round(len(pcm) / SR * FPS)) + int(FPS * 0.15))
                    except Exception as e:
                        print(f"  [{idx + 1}/{total}] line TTS FAIL: {e}")

                # brief highlight in place
                for _ in range(HIGHLIGHT_FRAMES):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "active": ln, "phase": "highlight", "t": 1})
                # lift to center
                clicks.append((now_s(), False, False))
                clicks.append((now_s() + int(SR * 0.03), False, True))
                for f in range(LIFT_FRAMES):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "active": ln, "phase": "lift", "t": f / (LIFT_FRAMES - 1)})
                # center hold (clean card)
                for z in range(10):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "active": ln, "phase": "center", "t": z / 9})
                for _ in range(max(0, dur - 10)):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "active": ln, "phase": "center", "t": 1.0})
                # return to place
                clicks.append((now_s(), False, False))
                clicks.append((now_s() + int(SR * 0.03), False, True))
                for f in range(RETURN_FRAMES):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "active": ln, "phase": "return", "t": f / (RETURN_FRAMES - 1)})
                for _ in range(SETTLE_FRAMES):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "active": ln, "phase": "settled", "t": 1})

            for _ in range(int(FPS * 1.8)):
                push({"type": "explain", "file": fname, "lines": code_lines,
                      "active": None, "phase": "final", "t": 1})
            path = os.path.join(os.getcwd(), fname)
            d = os.path.dirname(path)
            if d:
                os.makedirs(d, exist_ok=True)
            with open(path, "w") as f:
                f.write(code)
            WRITTEN_FILES.append(path)
            print(f"  [{idx + 1}/{total}] [explain] wrote {fname}")
            continue
        # ---------- editor ----------
        if stype == "editor":
            fname = step.get("file", "untitled.py")
            code = step.get("code", "")
            for _ in range(max(hold, int(FPS * 0.6))):
                push({"type": "editor", "file": fname, "typed": "", "cursor": True})
            typed = ""
            for ch in code:
                typed += ch
                deep = ch in (" ", "\n", "\t")
                clicks.append((now_s(), deep, False))
                clicks.append((now_s()+int(SR*0.028), False, True))
                for _ in range(max(1, round(FPS / random.uniform(22, 34)))):
                    push({"type": "editor", "file": fname, "typed": typed, "cursor": True})
            for i in range(int(FPS * 1.2)):
                push({"type": "editor", "file": fname, "typed": typed, "cursor": cursor_state(fc[0])})
            path = os.path.join(os.getcwd(), fname)
            d = os.path.dirname(path)
            if d:
                os.makedirs(d, exist_ok=True)
            with open(path, "w") as f:
                f.write(code)
            WRITTEN_FILES.append(path)
            print(f"  [{idx + 1}/{total}] [editor] wrote {fname}")
            continue
        # ---------- terminal ----------
        cmd = step["command"]
        for _ in range(hold):
            push({"type": "terminal", "buffer": list(buffer),
                  "partial": prompt_segs() + [("", CMD_COLOR)], "cursor": True})
        typed = ""
        for ch in cmd:
            typed += ch
            deep = ch == " "
            clicks.append((now_s(), deep, False))
            clicks.append((now_s()+int(SR*0.028), False, True))
            for _ in range(max(1, round(FPS / random.uniform(18, 28)))):
                push({"type": "terminal", "buffer": list(buffer),
                      "partial": prompt_segs() + [(typed, CMD_COLOR)], "cursor": True})
        for _ in range(int(FPS * 0.4)):
            push({"type": "terminal", "buffer": list(buffer),
                  "partial": prompt_segs() + [(typed, CMD_COLOR)], "cursor": cursor_state(fc[0])})
        clicks.append((now_s(), True, False))
        clicks.append((now_s()+int(SR*0.03), False, True))
        buffer.append(prompt_segs() + [(typed, CMD_COLOR)])
        print(f"  [{idx + 1}/{total}] {cmd}  [{prompt_segs()[0][0]}$]")
        t_run0 = time.time()
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600, cwd=cur_dir)
            out_text, err_text = r.stdout, r.stderr
        except Exception as e:
            out_text, err_text = "", str(e)
        elapsed = time.time() - t_run0
        update_cwd_from_cmd(cmd)
        # show a "running…" indicator for the real execution time (capped)
        if elapsed > 0.9:
            n_run = min(int(elapsed * FPS), int(FPS * 4))
            n_run = max(n_run, int(FPS * 0.6))
            run_line = [("  … running", OUTPUT_COLOR)]
            for _ in range(n_run):
                push({"type": "terminal", "buffer": list(buffer) + [run_line], "partial": None, "cursor": cursor_state(fc[0])})
        for _ in range(int(FPS * 0.15)):
            push({"type": "terminal", "buffer": list(buffer), "partial": None, "cursor": False})
        for seg in wrap_output(out_text, OUTPUT_COLOR, mdraw):
            buffer.append(seg)
            for _ in range(max(1, int(FPS * 0.06))):
                push({"type": "terminal", "buffer": list(buffer), "partial": None, "cursor": False})
        for seg in wrap_output(err_text, ERROR_COLOR, mdraw):
            buffer.append(seg)
            for _ in range(max(1, int(FPS * 0.06))):
                push({"type": "terminal", "buffer": list(buffer), "partial": None, "cursor": False})
        for _ in range(int(FPS * 0.9)):
            push({"type": "terminal", "buffer": list(buffer), "partial": None, "cursor": False})
    for i in range(int(FPS * 2.0)):
        push({"type": "terminal", "buffer": list(buffer),
              "partial": prompt_segs() + [("", CMD_COLOR)], "cursor": i < FPS})
    return frames, clicks, narration_events

# ================= MAIN =================

def check_deps():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except Exception:
        sys.exit("ffmpeg not found.")
    if shutil.which("edge-tts") is None:
        sys.exit("edge-tts not found. Run: pip install edge-tts")

def ensure_config(path):
    if os.path.exists(path):
        return
    with open(path, "w") as f:
        f.write(DEFAULT_CONFIG_YAML)
    print(f"Created: {path}")
    sys.exit(0)

def load_config(path):
    with open(path) as f:
        raw = f.read()
    if path.endswith((".yaml", ".yml")):
        if not HAVE_YAML:
            sys.exit("PyYAML not installed.")
        return yaml.safe_load(raw)
    return json.loads(raw)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    preview = "--frame" in sys.argv
    config_path = args[0] if args else "config.yaml"
    ensure_config(config_path)
    config = load_config(config_path)
    if preview:
        # preview hook + explain center with wrapping
        if any(s.get("type") == "hook" for s in config.get("steps", [])):
            hs = next(s for s in config["steps"] if s.get("type") == "hook")
            entry = {"type": "hook", "title": hs.get("title",""), "sub": hs.get("sub",""), "n": len(hs.get("title","")), "sub_on": True, "cursor": False}
            img = render_frame(entry)
            img.save("frame_preview.png")
            print("Saved: frame_preview.png (hook)")
            return
        code_lines = ["import secrets, string", "", "def gen(length=16):",
                      '    chars = string.ascii_letters + string.digits + "!@#$%^&*"', '    return "".join(secrets.choice(chars) for _ in range(length))', "", "for i in range(5):",
                      '    print(f"Password {i+1}: {gen()}")']
        entry = {"type": "explain", "file": "vault/passgen.py", "lines": code_lines,
                 "settled": {0,1}, "active": 3, "phase": "center", "t": 1.0}
        img = render_frame(entry)
        img.save("frame_preview.png")
        print("Saved: frame_preview.png")
        return
    check_deps()
    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.makedirs(WORK_DIR)
    voice = config.get("voice", "en-US-GuyNeural")
    steps = config["steps"]
    print(f"Font: {FONT_PATH or 'default'}")
    print(f"Voice: {voice}")
    print(f"Steps: {len(steps)}")
    print("\n--- Timeline ---")
    frames, clicks, narration_events = build_timeline(config, voice)
    total_frames = len(frames)
    duration = total_frames / FPS
    print(f"  {total_frames} frames, ~{duration:.1f}s")
    print("\n--- Audio ---")
    master = np.zeros(int(duration * SR) + SR, dtype=np.float32)
    rng = np.random.default_rng(0)
    for s, deep, is_release in clicks:
        if is_release:
            add_into(master, s, synth_key_release(rng))
        else:
            add_into(master, s, synth_key_press(rng, deep=deep))
    for s, pcm in narration_events:
        add_into(master, s, pcm * 0.95)
    peak = float(np.max(np.abs(master))) if master.size else 0.0
    if peak > 0.98:
        master *= 0.98 / peak
    audio_path = os.path.join(WORK_DIR, "audio.wav")
    write_wav(audio_path, master, SR)
    print(f"  {len(clicks)} key events, {len(narration_events)} narrations")
    print("\n--- Rendering ---")
    silent = os.path.join(WORK_DIR, "silent.mp4")
    proc = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "warning",
        "-f", "rawvideo", "-pixel_format", "rgb24",
        "-video_size", f"{WIDTH}x{HEIGHT}", "-framerate", str(FPS),
        "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "15", "-preset", "medium",
        silent,
    ], stdin=subprocess.PIPE)
    t0 = time.time()
    for i, entry in enumerate(frames):
        img = render_frame(entry)
        proc.stdin.write(img.tobytes())
        if (i + 1) % 100 == 0 or i + 1 == total_frames:
            elapsed = time.time() - t0
            speed = (i + 1) / max(0.01, elapsed)
            pct = (i + 1) / total_frames * 100
            eta = (total_frames - i - 1) / max(0.01, speed)
            print(f"\r  [{i + 1}/{total_frames}] {pct:.0f}% | {speed:.1f} fps | ETA {eta:.0f}s   ", end="", flush=True)
    print()
    proc.stdin.close()
    proc.wait()
    print("\n--- Muxing ---")
    os.makedirs(DOCS_DIR, exist_ok=True)
    out = os.path.join(DOCS_DIR, f"terminal_video_{int(time.time())}.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "warning",
        "-i", silent, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
        "-shortest", out,
    ], check=True)
    shutil.rmtree(WORK_DIR)
    for p in WRITTEN_FILES:
        try:
            os.remove(p)
        except OSError:
            pass
    for p in WRITTEN_FILES:
        d = os.path.dirname(p)
        while d and d != os.getcwd():
            try:
                os.rmdir(d)
            except OSError:
                break
            d = os.path.dirname(d)
    print(f"\nSaved: {out}")
    print(f"Duration: {duration:.1f}s | Size: {os.path.getsize(out) / 1024:.0f} KB")

if __name__ == "__main__":
    main()
