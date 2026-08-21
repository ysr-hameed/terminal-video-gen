#!/usr/bin/env python3
"""
Terminal Tutorial Video Generator v8
====================================
Scene types:
  - terminal: command typed + executed for real
  - editor:   code typed char-by-char (classic)
  - explain:  motion-design walkthrough — each line pops up BIG in the
              center while narrated, then flies into its place in code
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

PROMPT_COLOR = (63, 185, 80)
CMD_COLOR = (230, 237, 243)
OUTPUT_COLOR = (139, 148, 158)
ERROR_COLOR = (248, 81, 73)
CURSOR_COLOR = (63, 185, 80)
ACCENT = (88, 166, 255)

PROMPT = "~$ "

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
  - narration: "First, check Python is installed."
    command: "python3 --version"

  - narration: "Make a new folder for our project."
    command: "mkdir vault"

  - narration: "Go inside the folder."
    command: "cd vault"

  - narration: "Check what is inside. Empty for now."
    command: "ls"

  - type: explain
    file: "vault/passgen.py"
    code: |
      import secrets, string

      def gen(length=16):
          chars = string.ascii_letters + string.digits + "!@#$%^&*"
          return "".join(secrets.choice(chars) for _ in range(length))

      for i in range(5):
          print(f"Password {i+1}: {gen()}")
    lines:
      - line: 1
        say: "Import secrets. Python's secure random module."
      - line: 3
        say: "Define gen. It takes the password length."
      - line: 4
        say: "Letters, digits and symbols form the character pool."
      - line: 5
        say: "Pick random characters and join them."
      - line: 7
        say: "Loop five times."
      - line: 8
        say: "Print every generated password."

  - narration: "Now run it."
    command: "cd vault && python3 passgen.py"

  - narration: "Done! Five secure passwords generated."
    command: "echo Complete!"
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
CENTER_FONT_SIZE = int(FONT_SIZE * 1.45)
try:
    CENTER_FONT = ImageFont.truetype(FONT_PATH, CENTER_FONT_SIZE) if FONT_PATH else FONT
except Exception:
    CENTER_FONT = FONT


def tw(draw, text, font=FONT):
    if not text:
        return 0
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    return r - l


def ease_out(t):
    return 1 - (1 - t) ** 3


def ease_io(t):
    return t * t * (3 - 2 * t)


# ================= WRAPPING =================

def wrap_segments(segs, max_w, draw):
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
        ww = tw(draw, word_text)
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
                    if tw(draw, test) > max_w:
                        if chunk:
                            result[-1].append((chunk, word_color))
                            result.append([])
                        chunk = ch
                    else:
                        chunk = test
                if chunk:
                    result[-1].append((chunk, word_color))
                    x = tw(draw, chunk)
            else:
                result[-1].append((word_text, word_color))
                x = ww
    if not result[-1]:
        result.pop()
    return result


def wrap_output(raw, color, draw):
    out = []
    max_w = RW - 2 * PAD_X
    for line in (raw or "").splitlines() or [""]:
        if not line:
            out.append([("", color)])
            continue
        for w in wrap_segments([(line, color)], max_w, draw):
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


# ================= EXPLAIN SCENE =================

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
        wrapped = wrap_segments(segs, max_w, d) if line else []
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
    """Rows consumed by given line indices (for target row calc)."""
    row = 0
    for i in indices:
        line = lines[i]
        if not line:
            row += 1
            continue
        wrapped = wrap_segments(highlight_line(line), RW - CODE_X - 30 * RENDER_SCALE,
                                ImageDraw.Draw(Image.new("RGB", (8, 8))))
        row += max(1, len(wrapped))
    return row


def target_row_of(lines, idx, settled):
    """Which display row this line index lands at, given settled order."""
    rows_before = count_rows(lines, [i for i in sorted(settled) if i < idx])
    own = count_rows(lines, [idx])
    return rows_before, own


def get_explain_bg(lines, settled):
    """Softly-dimmed backdrop of settled lines — still clearly readable."""
    key = tuple(sorted(settled))
    if key in _EXPLAIN_BG_CACHE:
        return _EXPLAIN_BG_CACHE[key]
    img = EDITOR_BASE.copy()
    _draw_code_block(img, lines, key, dim=0.82)
    img = img.filter(ImageFilter.GaussianBlur(1.6 * RENDER_SCALE))
    img = ImageEnhance.Brightness(img).enhance(0.94)
    _EXPLAIN_BG_CACHE[key] = img
    return img


def render_line_image(line, font):
    """Render one syntax-highlighted line to a cropped RGBA image."""
    tmp = Image.new("RGBA", (RW, int(FONT_SIZE * 2.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    segs = highlight_line(line)
    x = 0
    for t, c in segs:
        if t:
            d.text((x, 12), t, font=font, fill=c)
        x += tw(d, t, font)
    bbox = tmp.getbbox()
    return tmp.crop(bbox) if bbox else None


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
    settled = entry["settled"]
    active = entry["active"]
    phase = entry["phase"]  # center | move | settled | final
    t = entry.get("t", 1.0)
    fname = entry["file"]

    if phase == "final":
        img = EDITOR_BASE.copy()
        _draw_code_block(img, lines, range(len(lines)), dim=1.0)
        draw = ImageDraw.Draw(img)
        draw_header(draw, fname)
        draw_statusbar(draw, fname)
        return img

    img = get_explain_bg(lines, settled).copy()
    draw = ImageDraw.Draw(img)
    draw_header(draw, fname)
    draw_statusbar(draw, fname)

    line = lines[active] if active is not None and 0 <= active < len(lines) else ""
    li_img = render_line_image(line, CENTER_FONT) if line else None

    # target geometry
    rows_before, own_rows = target_row_of(lines, active, settled) if active is not None else (0, 1)
    tgt_y = Y0 + rows_before * LINE_HEIGHT
    tgt_x = CODE_X

    if phase == "center":
        e = ease_out(min(1.0, t))
        scale = 0.72 + 0.28 * e
        cy = int(RH * 0.42)
        if li_img:
            w, h = li_img.size
            sw, sh = int(w * scale), int(h * scale)
            frame = li_img.resize((max(1, sw), max(1, sh)), Image.LANCZOS)
            px, py = int(RW / 2 - sw / 2), int(cy - sh / 2)
            pad_x, pad_y = int(46 * scale), int(30 * scale)
            draw.rounded_rectangle(
                [px - pad_x, py - pad_y, px + sw + pad_x, py + sh + pad_y],
                radius=22 * RENDER_SCALE, fill=CARD_BG, outline=ACCENT, width=3 * RENDER_SCALE)
            img.paste(frame, (px, py), frame)
            # arrow pointing at card
            ax = px - pad_x - 34 * RENDER_SCALE
            ay = py + sh // 2
            s = 16 * RENDER_SCALE
            draw.polygon([(ax, ay - s), (ax, ay + s), (ax + s, ay)], fill=CURSOR_COLOR)
        # line badge
        if active is not None:
            badge = f"line {active + 1}"
            bw = tw(draw, badge)
            bx, by = int(RW / 2 - bw / 2), int(cy - LINE_HEIGHT * 2.6)
            draw.rounded_rectangle([bx - 18 * RENDER_SCALE, by - 8 * RENDER_SCALE,
                                    bx + bw + 18 * RENDER_SCALE, by + LINE_HEIGHT - 4 * RENDER_SCALE],
                                   radius=14 * RENDER_SCALE, fill=(40, 50, 68))
            draw.text((bx, by), badge, font=FONT, fill=(230, 237, 243))

    elif phase == "move":
        e = ease_io(min(1.0, t))
        cy = int(RH * 0.42)
        start_x = int(RW / 2 - (li_img.width / 2 if li_img else 0))
        start_y = cy - (li_img.height // 2 if li_img else 0)
        cur_x = int(start_x + (tgt_x - start_x) * e)
        cur_y = int(start_y + (tgt_y + 4 - start_y) * e)
        scale = 1.0 + (1.0 - FONT_SIZE / CENTER_FONT_SIZE) * (1 - e)

        # ghost target slot
        draw.rectangle([0, tgt_y - 3, RW, tgt_y + LINE_HEIGHT - 9], fill=(24, 30, 40))

        if li_img:
            w, h = li_img.size
            sw, sh = max(1, int(w * scale)), max(1, int(h * scale))
            frame = li_img.resize((sw, sh), Image.LANCZOS)
            img.paste(frame, (cur_x, cur_y), frame)

    elif phase == "settled":
        # sharp at final spot + gutter arrow briefly
        draw.rectangle([0, tgt_y - 3, RW, tgt_y + LINE_HEIGHT - 9], fill=ACTIVE_LINE)
        num = str(active + 1)
        nw = tw(draw, num)
        draw.text((GUTTER_W - nw - 12 * RENDER_SCALE, tgt_y), num, font=FONT, fill=(210, 216, 224))
        segs = highlight_line(line)
        max_w = RW - CODE_X - 30 * RENDER_SCALE
        wrapped = wrap_segments(segs, max_w, draw) if line else []
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
        ax = CODE_X - 40 * RENDER_SCALE
        ay = tgt_y + LINE_HEIGHT // 2
        s = 14 * RENDER_SCALE
        draw.polygon([(ax, ay - s), (ax, ay + s), (ax + s, ay)], fill=CURSOR_COLOR)

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
        all_visual.extend(wrap_segments(segs, max_w, draw))
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
        wrapped = wrap_segments(segs, max_w, draw) if line else []
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


def synth_click(rng, deep=False):
    dur = 0.055 if deep else 0.035
    n = int(SR * dur)
    t = np.arange(n) / SR
    f_body = rng.uniform(110, 160) if deep else rng.uniform(170, 240)
    body = np.sin(2 * np.pi * f_body * t) * np.exp(-t * (55 if deep else 80))
    f_tick = rng.uniform(2600, 3800)
    tick = np.sin(2 * np.pi * f_tick * t) * rng.uniform(-1, 1, n) * np.exp(-t * 320)
    noise = rng.uniform(-1, 1, n) * np.exp(-t * 500)
    click = (body * 0.9 + tick * 0.35 + noise * 0.25) * rng.uniform(0.22, 0.32)
    fade_n = max(1, int(SR * 0.001))
    click[:fade_n] *= np.linspace(0, 1, fade_n)
    return click.astype(np.float32)


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

CENTER_MIN_FRAMES = int(FPS * 0.5)
MOVE_FRAMES = 22
SETTLE_FRAMES = int(FPS * 0.4)


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

    for idx, step in enumerate(steps):
        stype = step.get("type", "terminal")

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

            for _ in range(max(hold, int(FPS * 0.6))):
                push({"type": "explain", "file": fname, "lines": code_lines,
                      "settled": set(), "active": None, "phase": "center", "t": 0})

            settled = set()
            for ri, rv in enumerate(reveals):
                ln = max(0, min(int(rv.get("line", 1)) - 1, len(code_lines) - 1))
                say = (rv.get("say") or "").strip()

                # --- center phase (narration here) ---
                dur = int(FPS * 0.8)
                if say:
                    try:
                        pcm = tts_pcm(say, voice, f"s{idx}l{ri}")
                        narration_events.append((now_s(), pcm))
                        dur = max(int(FPS * 0.9), int(round(len(pcm) / SR * FPS)) + int(FPS * 0.3))
                    except Exception as e:
                        print(f"  [{idx + 1}/{total}] line TTS FAIL: {e}")

                for z in range(12):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "settled": set(settled), "active": ln, "phase": "center",
                          "t": z / 11})
                for _ in range(max(0, dur - 12)):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "settled": set(settled), "active": ln, "phase": "center", "t": 1.0})

                # --- move phase ---
                clicks.append((now_s(), True))
                for m in range(MOVE_FRAMES):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "settled": set(settled), "active": ln, "phase": "move",
                          "t": m / (MOVE_FRAMES - 1)})

                settled.add(ln)

                # --- settled pause ---
                for _ in range(SETTLE_FRAMES):
                    push({"type": "explain", "file": fname, "lines": code_lines,
                          "settled": set(settled), "active": ln, "phase": "settled", "t": 1})

            # final sharp view
            for _ in range(int(FPS * 1.5)):
                push({"type": "explain", "file": fname, "lines": code_lines,
                      "settled": set(settled), "active": None, "phase": "final", "t": 1})

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
                clicks.append((now_s(), False))
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
                  "partial": [(PROMPT, PROMPT_COLOR), ("", CMD_COLOR)], "cursor": True})

        typed = ""
        for ch in cmd:
            typed += ch
            clicks.append((now_s(), ch == " "))
            for _ in range(max(1, round(FPS / random.uniform(18, 28)))):
                push({"type": "terminal", "buffer": list(buffer),
                      "partial": [(PROMPT, PROMPT_COLOR), (typed, CMD_COLOR)], "cursor": True})

        for _ in range(int(FPS * 0.4)):
            push({"type": "terminal", "buffer": list(buffer),
                  "partial": [(PROMPT, PROMPT_COLOR), (typed, CMD_COLOR)], "cursor": cursor_state(fc[0])})
        clicks.append((now_s(), True))

        buffer.append([(PROMPT, PROMPT_COLOR), (typed, CMD_COLOR)])

        print(f"  [{idx + 1}/{total}] {cmd}")
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)
            out_text, err_text = r.stdout, r.stderr
        except Exception as e:
            out_text, err_text = "", str(e)

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

        for _ in range(int(FPS * 0.5)):
            push({"type": "terminal", "buffer": list(buffer), "partial": None, "cursor": False})

    for i in range(int(FPS * 2.0)):
        push({"type": "terminal", "buffer": list(buffer),
              "partial": [(PROMPT, PROMPT_COLOR), ("", CMD_COLOR)], "cursor": i < FPS})

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
        code_lines = ["import secrets, string", "", "def gen(length=16):",
                      '    chars = "abc"', '    return "".join(x)', "", "for i in range(5):",
                      '    print(gen())']
        entry = {"type": "explain", "file": "vault/passgen.py", "lines": code_lines,
                 "settled": {0}, "active": 2, "phase": "center", "t": 1.0}
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
    rng = np.random.default_rng()
    for s, deep in clicks:
        add_into(master, s, synth_click(rng, deep=deep))
    for s, pcm in narration_events:
        add_into(master, s, pcm * 0.95)
    peak = float(np.max(np.abs(master))) if master.size else 0.0
    if peak > 0.98:
        master *= 0.98 / peak
    audio_path = os.path.join(WORK_DIR, "audio.wav")
    write_wav(audio_path, master, SR)
    print(f"  {len(clicks)} clicks, {len(narration_events)} narrations")

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
