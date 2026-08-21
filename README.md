# Terminal Video Gen — 9:16 Tutorial Video Generator

Generate **polished 9:16 (1080×1920 @30fps)** terminal tutorials — real command execution, TTS narration, mechanical keyboard SFX, syntax-highlighted code explain, modern captions and viral hooks. **<60s by default.** All config-driven via `config.yaml`.

> Output: `output/terminal_video_<timestamp>.mp4` (H.264 `CRF 15`, AAC `192k`). Temp workdir `temp/` auto-created and deleted after mux.

Demo configs generate: hook → `python3 --version` → `mkdir vault` → `cd vault` → `ls (empty)` → *type entire `vault/passgen.py` fast* → *lift → center → return* explain per line → `python3 passgen.py` → CTA `echo Follow • Subscribe!`

---

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Config Schema (YAML)](#config-schema-yaml)
- [Themes](#themes)
- [Voices & Speed](#voices--speed)
- [Background Music (viral, copyright-free)](#background-music-viral-copyright-free)
- [Captions (alive, word-precise)](#captions-alive-word-precise)
- [File Structure](#file-structure)
- [How It Works](#how-it-works)
- [Performance (fast without quality loss)](#performance-fast-without-quality-loss)
- [Custom Hook / Examples](#custom-hook--examples)
- [Troubleshooting](#troubleshooting)

---

## Features
- **Hook scene** — scroll-stopper on `TERM_BG`: top `STOP SCROLLING • 60s FIX` pill (accent, `anchor="mm"` perfect center), title with colored keywords (`Stop`=accent, `weak`=red, `passwords`=green, theme-aware), subtitle + accent line + `KEEP WATCHING ▶` pill. TTS speaks `title + sub` (your `narration` overrides).
- **Terminal scene** — live `cwd` prompt (`~$` → `~/vault$`), real `subprocess.run(cwd=cur_dir)`, typed with `+35%` TTS, bottom `ls` shows ` (empty)` if empty, `… running` indicator for `>0.9s` commands (capped 4s).
- **Explain scene** — **(A) type whole file fast (40–55 cps)** then **(B) lift → center → return** per line: `highlight 3f → lift 6f → center 10f+speech → return 6f → settled 2f`. Full code always visible, other lines **blurred 1.2px ×0.88** while card is up. Center card `1.10×` font, `CARD_BG` + shadow, `Line N` pill `anchor="mm"`.
- **Editor scene** — classic char-by-char typing (alternative to explain).
- **Captions** — modern dark pill (`rgba 0,0,0,195`) + `ACCENT` top bar, white + `7px` black stroke, **current word** in `ACCENT` + `54px` pop (`-6px` lift). **Word-precise** via `edge_tts WordBoundary` (`100ns` ticks → samples), not char-estimate, so highlight never drifts (handles pauses).
- **Mechanical keyboard SFX** — bandpassed `220-900Hz` thock + `3.2-7kHz` tick, chirped `95→45Hz`, press + release (`0.028s` gap), `deep` for space/enter.
- **Themes — 6, auto random** — `github/dracula/forest` (dark) + `light/paper/ice` (light, dark syntax for contrast). `theme: auto` picks randomly each run.
- **Music — viral, legit, short snippet** — optional `music: "random"` picks one of `music/*.mp3` (50 × 18s synthetic phonk/trap/lofi, `2.8KB→14MB` total) — middle 18s looped, ducked `0.11→0.035` under voice, `0.8s` fade.
- **9:16, 30fps, `CRF 15` `medium`** — duplicate-frame cache reuses `~70%` frames with zero quality loss.

---

## Quick Start
```bash
git clone https://github.com/ysr-hameed/terminal-video-gen.git
cd terminal-video-gen
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # numpy, Pillow, PyYAML, edge-tts
# ffmpeg must be installed: sudo apt install ffmpeg
python terminal_video.py          # uses config.yaml → output/terminal_video_*.mp4
python terminal_video.py --frame  # preview single frame → frame_preview.png
```

---

## Config Schema (YAML)

Top-level `config.yaml` (also `config.yml` or `json`):

```yaml
theme: auto              # auto | github | dracula | forest | light | paper | ice
voice: "en-IN-PrabhatNeural"  # any edge-tts voice, e.g. en-US-AriaNeural
# optional viral music — 18s snippet looped, ducked under voice:
music: "random"          # random | auto | music/*.mp3 | https://cdn.pixabay.com/...mp3
music_volume: 0.11       # 0.0-0.3 background level
music_duck: 0.32         # duck to 32% volume under narration (0.18s fade)

steps:                   # ordered timeline
  - type: hook
    title: "Stop using weak passwords"
    sub: "Let's fix that in 60 seconds"
    narration: "Stop scrolling! Still using weak passwords? Fix in sixty seconds — watch!"
    # if narration omitted, speaks "title. sub"

  - narration: "Quick check — Python ready?"
    command: "python3 --version"
    # terminal step: narration (optional) → typed command → real run (cwd tracked)

  - type: explain
    file: "vault/passgen.py"
    intro: "Watch it type, quick explain."  # optional, spoken while empty editor shows
    code: |
      import secrets, string
      def gen(length=16):
          chars = string.ascii_letters + string.digits + "!@#$%^&*"
          return "".join(secrets.choice(chars) for _ in range(length))
      for i in range(5):
          print(f"Password {i+1}: {gen()}")
    lines:                          # per-line explain, in order
      - line: 1
        say: "Import secrets — secure random."
      - line: 3
        say: "gen makes a password, length given."
      # blank lines between are auto gap-filled for continuity

  - type: editor              # alternative: type file without explain
    file: "vault/other.py"
    code: |
      print("hello")

  - narration: "Now run it."
    command: "python3 passgen.py"   # runs in current cwd (after cd vault → vault/passgen.py)
```

### Field Details

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `theme` | `string` | no | `auto` (random among 6) or explicit. See [Themes](#themes). |
| `voice` | `string` | no | `edge-tts` voice ID. Default `en-IN-PrabhatNeural`. Tested: `en-US-AriaNeural`, `en-US-JennyNeural`, `en-US-AvaMultilingualNeural`, `en-GB-SoniaNeural`. |
| `music` | `string` | no | `random`/`auto` → picks `music/*.mp3`; or `music/viral_phonk_1.mp3` or `https://...mp3` URL. Only middle 18s used, looped. |
| `music_volume` | `float` | no | Background bed `0.11` default. |
| `music_duck` | `float` | no | Multiplier under voice `0.32` → `0.035`. |
| `steps` | `array` | **yes** | Ordered scenes. Each step is one of 4 types below. |

#### Step Types

**1. `hook` (scroll-stopper, on `TERM_BG`)**
```yaml
- type: hook
  title: "Stop using weak passwords"  # required, 1 line ideally ≤25 chars (wraps at RW-70)
  sub: "Let's fix that in 60 seconds" # required, 1 line
  narration: "Custom spoken hook"     # optional, defaults to "title. sub"
```
Rendered via `render_hook` (`terminal_video.py:447`) — badge pill `anchor="mm"`, title colored via `_hook_title_segs` (theme-aware), subtitle, accent line.

**2. `terminal` (default if `type` omitted)**
```yaml
- narration: "Make vault — mkdir makes a folder." # optional, TTS
  command: "mkdir vault"                           # required, shell, real cwd
```
- `prompt_segs()` shows `~$` → `~/vault$` after `cd vault` (`update_cwd_from_cmd` handles `&&`/`;`).
- Typed at `18-28 cps` with press+release clicks, `0.22s` pre-execute hold, `… running` if `>0.9s` (capped 4s), output `0.06s/line`, logical `hold_out` (`0.35-1.0s` by line count).

**3. `explain` (type → explain)**
```yaml
- type: explain
  file: "vault/passgen.py"
  intro: "Watch it type..."  # optional
  code: |
    import secrets, string
    ...
  lines:
    - line: 1
      say: "Import secrets — secure random."
```
- Phase A: type whole `code` fast `40-55 cps`, `0.35s` hold.
- Phase B: per `lines` in order: `highlight 3f → lift 6f (ease_io, scale ratio→1) → center 10f+speech (0.86→1 pop) → return 6f → settled 2f`. Background is full file (`get_explain_full`); during lift/center/return it blurs `1.2px×0.88` (`get_explain_full_blur`), other lines remain visible but de-emphasized. Card `CARD_BG` + shadow, `Line N` pill `anchor="mm"`. Gaps (blank lines) auto-covered.

**4. `editor`**
```yaml
- type: editor
  file: "vault/other.py"
  code: |
    print("hello")
```
Fast typing without per-line explain, `0.5s` final hold.

**Supported schema notes:**
- All `narration` / `say` / `intro` / `title`/`sub` are TTS-synthesized via `edge_tts` at `rate="+35%"` (`tts_pcm` `terminal_video.py:1031`) with precise `WordBoundary` timing for captions.
- `file` paths are relative to `os.getcwd()` (project root). `WRITTEN_FILES` tracked and **auto-deleted** after mux (`terminal_video.py:1620` `rm` + `rmdir`).
- `theme: auto` is logical: `random.choice(THEMES)` each run, so videos never look identical.

---

## Themes

6 themes, auto-rotated. `apply_theme` rebuilds `TERM_BASE`/`EDITOR_BASE` and clears caches.

| Name | `TERM_BG` | `EDITOR_BG` | `ACTIVE_LINE` | `CARD_BG` | `ACCENT` | Use |
|------|-----------|-------------|---------------|-----------|----------|-----|
| `github` | `13,17,23` | `18,22,30` | `32,42,58` | `28,35,48` | `88,166,255` | Dark default |
| `dracula` | `18,14,32` | `24,18,42` | `48,38,72` | `36,28,64` | `189,147,249` | Purple dracula |
| `forest` | `10,18,14` | `16,26,20` | `28,52,38` | `22,38,28` | `63,185,80` | Green forest |
| `light` | `248,249,250` | `255,255,255` | `230,236,245` | `242,244,248` | `0,122,255` | Light — dark syntax (`SY_PLAIN 45,52,65` on white) |
| `paper` | `253,246,227` | `255,251,240` | `238,228,200` | `250,240,220` | `211,54,130` | Warm paper |
| `ice` | `236,239,244` | `243,246,250` | `215,222,233` | `230,236,245` | `94,129,172` | Cold blue |

Light themes override `CMD_COLOR/OUTPUT_COLOR/SY_*` to dark for contrast (`apply_theme:112`).

---

## Voices & Speed
- Default `en-IN-PrabhatNeural` (male, Indian, your pick).
- Top 1 alternative per research: `en-US-AriaNeural` (warm female, `Positive, Confident`, News/Novel) — also `en-US-JennyNeural`, `en-US-AvaMultilingualNeural`.
- Speed `rate="+35%"` in `tts_generate` (`terminal_video.py:997`) — faster + clear, still natural. Change via `rate` param or `voice` in config.

List voices: `source .venv/bin/activate && edge-tts --list-voices | grep en-`

---

## Background Music (viral, copyright-free)

**Never download trending copyrighted songs from YouTube Music — even 15s can be claimed.** Use legit free:

1. **Pixabay Music** `pixabay.com/music/search/viral` — 100% free, no attribution, `cdn.pixabay.com/audio/...mp3`
2. **YouTube Audio Library** `studio.youtube.com → Audio Library → Viral` (filter “No attribution”)
3. **Mixkit / Chosic / Bensound Free / Uppbeat Free**

This repo ships **50 synthetic viral loops** (`music/viral_*.mp3`, `18s` each, `128k`, `phonk/trap/lofi` 85-142 BPM, `14MB` total) — original, copyright-free, viral-style. `music/*.mp3` is gitignored except `README.md`.

**Usage:**
```yaml
music: "random"  # picks one of music/*.mp3 randomly
# music: "music/viral_phonk_1.mp3"
# music: "https://cdn.pixabay.com/download/audio/2022/03/10/audio_c8c8a73467.mp3?filename=energy-10882.mp3"
music_volume: 0.11
music_duck: 0.32
```
The generator downloads (if URL, with `User-Agent` + `curl` fallback), cuts **middle 18s** (`-ss 3 -t 18`), fades `0.8s`, loops via `np.tile` to video length, and **ducks** to `base*duck` under every narration (`0.18s` fade) so voice stays clear (`_load_music_pcm:1146`). No long downloads — only 18s kept.

---

## Captions (alive, word-precise)

- Dark pill `rgba(0,0,0,195)` + `ACCENT` top bar (`18px` radius), white text + `7px` black stroke, **current word** in `ACCENT` + `54px` pop (`-6px` lift) (`overlay_caption:906`).
- Timing is **not** char-proportional: `tts_pcm` (`terminal_video.py:1031`) uses `edge_tts.Communicate(..., boundary="WordBoundary")`, captures per-word `offset/duration` in `100ns` ticks → samples (`offset*SR/10M`), stores `words=[(text, start_sample, dur)]` per clip. Render loop (`terminal_video.py:1584`) finds active caption by `sample` range and picks `highlight_idx` where `w_start <= elapsed < w_start+w_dur` (pause → keep previous). So caption never drifts.

---

## File Structure
```
terminal-video/
├── terminal_video.py      # single-file generator (9:16, 30fps, CRF15)
├── config.yaml            # your timeline (theme/voice/music/steps) — see schema above
├── requirements.txt       # numpy, Pillow, PyYAML, edge-tts
├── music/
│   ├── README.md          # legit sources + usage
│   ├── .gitkeep
│   └── viral_*.mp3        # 50 × 18s (gitignored, 14M) — synthetic viral loops
├── output/                # generated mp4s (gitignored)
├── temp/                  # visible workdir (audio.wav, silent.mp4) — auto-deleted after mux
├── hook_previews/         # (old) hook variant previews (gitignored after clean)
└── README.md
```
`WORK_DIR = __file__/temp` (`terminal_video.py:144`) — visible during `python terminal_video.py`, deleted via `shutil.rmtree` after mux. `WRITTEN_FILES` (`vault/passgen.py` etc.) also deleted.

---

## How It Works
1. `load_config` → `apply_theme` (random or explicit) → rebuilds `TERM_BASE/EDITOR_BASE`.
2. `build_timeline` iterates `steps`:
   - `hook` → title typewriter + badge pill + sub reveal, `hook_speak` TTS at `start_sample`.
   - `terminal` → `prompt_segs()` → typed → `subprocess.run(cwd=cur_dir)` → `update_cwd_from_cmd` → `… running` if `>0.9s`.
   - `explain` → type whole file → per-line `highlight/lift/center/return/settled` + `say` TTS.
   - Collects `frames` (list of `{"type":...}` dicts), `clicks` `(sample, deep, is_release)`, `narration_events` `(start, pcm)`, `caption_events` `(start, text, words, pcm)`.
3. Audio `master` mixes clicks (`synth_key_press` bandpassed thock) + narration `*0.95` + optional music looped/ducked → peak normalize `0.98` → `temp/audio.wav`.
4. Rendering: `ffmpeg -f rawvideo -pix_fmt rgb24 -fr 30 → silent.mp4` (`libx264 yuv420p CRF15 medium`). Loop caches `prev_base_img` (duplicate-frame reuse `~70%`), then overlays caption per frame (word-precise) → `proc.stdin.write`.
5. Mux: `ffmpeg -i silent.mp4 -i audio.wav -c:v copy -c:a aac -b:a 192k -shortest output/...mp4`
6. Clean `temp/` + `WRITTEN_FILES`.

---

## Performance (fast without quality loss)
- **Duplicate-frame cache** (`terminal_video.py:1576`): `prev_base_img` reuse + per-frame caption overlay copy → `70%` cached, no quality loss (still `CRF15`).
- Keep `RENDER_SCALE 1`, `FPS 30`, `preset medium` for quality. For drafts, use `veryfast` (visually ~identical at `CRF15`) or `FPS 24` saves 20% frames.
- `+35%` TTS rate + concise scripts (hook `7w`, terminal `3-5w`, `say` `5w`) keep **55-57s** total (`2029→1671` frames) vs `104s` before.

---

## Custom Hook / Examples

**Minimal hook-only config:**
```yaml
theme: auto
voice: "en-US-AriaNeural"
steps:
  - type: hook
    title: "Your passwords suck."
    sub: "Fix it in 10 seconds"
```

**Full tutorial (under 60s):** see `config.yaml` in repo — 8 steps, `hook` + 4 terminal + `explain` (6 lines) + `python3 passgen.py` + CTA `echo`.

Add your own: copy a `viral_*.mp3` to `music/` and set `music: "music/my_loop.mp3"` or `music: "random"`.

---

## Troubleshooting
- `ffmpeg not found` → `sudo apt install ffmpeg`
- `edge-tts not found` → `pip install edge-tts` inside `.venv`
- `ls` shows nothing → intentional: ` ls` on empty `vault` now renders ` (empty)` (`terminal_video.py:1172`).
- Light theme code invisible → fixed via `apply_theme` dark `SY_*` on white; if you add a custom theme, ensure `CMD_COLOR/OUTPUT_COLOR/SY_*` contrast.
- Button text not centered → fixed via `anchor="mm"` pills (`render_hook:457`, `render_explain:783`, `generate_clean_hooks_v2.py:28`).

License: MIT — free for personal/commercial, music in `music/` is synthetic original (no copyright).

