# Terminal Video Generator — AI Coding Tutorial Maker for YouTube Shorts, Instagram Reels & TikTok

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge" />
  <img src="https://img.shields.io/badge/9%3A16-1080x1920-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI_TTS-edge--tts-orange?style=for-the-badge" />
</p>

<p align="center">
  <b>Generate viral 9:16 coding tutorials automatically — real terminal, AI voice, auto captions, viral hooks & trending music. One YAML, one command.</b><br/>
  <i>Perfect for YouTube Shorts • Instagram Reels • TikTok • Coding Tutorials • Python Automation</i>
</p>

> **SEO Description:** Terminal Video Generator is an open-source AI-powered 9:16 video maker for coding tutorials. Automate terminal screen recording, code typing animation, AI voice-over (edge-tts), word-precise captions, viral hooks, and background music. Create faceless coding channels, programming shorts, and tech reels in under 60 seconds — config-driven with YAML, no manual editing.

<details>
<summary><b>🔍 Keywords for Search (SEO)</b></summary>

`terminal video generator` `coding tutorial generator` `ai video generator` `youtube shorts automation` `reels video maker` `tiktok coding video` `terminal screen recorder` `code typing animation` `ai voice over video` `edge tts video generator` `auto captions video` `viral hook generator` `9:16 video maker` `python tutorial video` `faceless coding channel` `programming shorts maker` `automated video generation`
</details>

---

## 🎬 Demo — See It In Action

**Terminal Video Gen** turns a simple `config.yaml` into a polished short-form coding tutorial:

- ✅ **Scroll-stopping hook** — animated pill + colored keywords, theme-aware, `anchor="mm"` perfect center
- ✅ **Real terminal** — `~$` → `~/vault$` live `cwd`, real `subprocess.run`, `… running` for long commands
- ✅ **Fast code typing** — `40-55 cps` with mechanical keyboard SFX (thock + tick)
- ✅ **Line-by-line explain** — `lift → center → return` with `1.10×` card + `1.2px` blur
- ✅ **Word-precise captions** — `WordBoundary` synced, alive highlight pop
- ✅ **AI TTS** — `en-IN-PrabhatNeural +35%` (or any edge-tts voice), natural + fast
- ✅ **Viral music** — 18s snippet looped + ducked
- ✅ **9:16 vertical** — `1080×1920 @30fps`, `CRF 15`, `AAC 192k`, `<60s`

### Watch the Demo
https://github.com/user-attachments/assets/49c966f9-8d9c-482d-a243-c27f4f54eb63

> **One config. One command. One polished tutorial video.**

---

## 📚 Table of Contents
- [Why Terminal Video Generator?](#why-terminal-video-generator)
- [Features](#features)
- [Quick Start (2 Minutes)](#quick-start-2-minutes)
- [Config Schema — Complete YAML Reference](#config-schema--complete-yaml-reference)
- [Themes — 6 Auto-Random](#themes--6-auto-random)
- [Voices & Speed](#voices--speed)
- [Background Music (viral, copyright-free)](#background-music-viral-copyright-free)
- [Captions (alive, word-precise)](#captions-alive-word-precise)
- [File Structure](#file-structure)
- [How It Works (Architecture)](#how-it-works-architecture)
- [Performance — Fast Without Quality Loss](#performance--fast-without-quality-loss)
- [Customization & Examples](#customization--examples)
- [Contributing — Help Us Build](#contributing--help-us-build)
- [FAQ — SEO Friendly Answers](#faq--seo-friendly-answers)
- [Troubleshooting](#troubleshooting)
- [License & SEO](#license--seo)

---

## Why Terminal Video Generator?

**For Creators:** Stop screen-recording manually. Automate faceless coding channels, get consistent 9:16 output for **YouTube Shorts, Reels, TikTok** — no Premiere, no OBS.

**For Developers:** Single-file `terminal_video.py` — readable, hackable, config-driven. Add a theme, voice, or hook in minutes.

**For SEO & Growth:** Built-in viral hooks (5 formulas from 2026 research), WordBoundary captions (accessibility + retention), trending music ducking — all proven to **stop the scroll** and boost watch time.

---

## ✨ Features

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


---

## 🤝 Contributing — Help Us Build

We love contributions! Whether you fix a pill padding bug, add a new theme, or craft a viral hook — you're welcome.

**Good First Issues:**
- Add a new theme (light/dark) in `THEMES` (`terminal_video.py:69`)
- Add a new hook layout in `render_hook` (`terminal_video.py:447`)
- Add a viral loop to `music/` (18s, 128k, phonk/trap/lofi)
- Improve caption animation in `overlay_caption` (`terminal_video.py:906`)

**How to Contribute (3 Steps):**
1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/terminal-video-gen.git
   cd terminal-video-gen
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Create a Branch**
   ```bash
   git checkout -b feat/your-feature
   # make changes, test: python terminal_video.py --frame
   # and: python terminal_video.py  (check output/terminal_video_*.mp4)
   ```
3. **Push & PR**
   ```bash
   git add -A
   git commit -m "feat: your feature"
   git push origin feat/your-feature
   # Open PR on GitHub — we review within 48h
   ```

**Code Style:** Keep `terminal_video.py` single-file, readable, `RERENDER_SCALE 1`, `FPS 30`, `CRF 15`. Use `anchor="mm"` for pills, theme-aware colors via `_is_light()`.

**Community:** Star ⭐ the repo to support, open an Issue for bugs, Discussion for hook ideas. All contributors are credited in README.

**SEO for Contributors:** Your PR description should include keywords like `terminal video generator`, `AI TTS`, `9:16` to help others discover your feature.



---

## FAQ — SEO Friendly Answers

**What is Terminal Video Generator?**
An open-source Python tool that automates 9:16 coding tutorial videos: terminal, code typing, AI voice (edge-tts), auto captions, hooks, music — all from YAML. Ideal for faceless YouTube Shorts, Reels, TikTok programming channels.

**Is it free and legit for YouTube monetization?**
Yes, MIT licensed. TTS via edge-tts (Microsoft) free for personal/commercial, music in `music/` is synthetic original (no copyright), or use Pixabay/Mixkit/YouTube Audio Library (see `music/README.md`). Never rip trending copyrighted songs.

**How to make videos under 60 seconds?**
Use concise `narration` (5-7 words), `+35%` TTS rate, and logical holds (speech-length + 0.1s buffer). Default config is `55-57s` (1671 frames) via `+35%` + short copy.

**Can I add my own theme/voice/hook?**
Yes — add a theme dict to `THEMES`, voice ID to `config.yaml:voice`, hook layout to `render_hook`. See `THEMES` table and `CONTRIBUTING.md`.

**How to contribute?**
Fork, branch, test with `--frame`, push, open PR. See [Contributing](#contributing--help-us-build).


## Troubleshooting
- `ffmpeg not found` → `sudo apt install ffmpeg`
- `edge-tts not found` → `pip install edge-tts` inside `.venv`
- `ls` shows nothing → intentional: ` ls` on empty `vault` now renders ` (empty)` (`terminal_video.py:1172`).
- Light theme code invisible → fixed via `apply_theme` dark `SY_*` on white; if you add a custom theme, ensure `CMD_COLOR/OUTPUT_COLOR/SY_*` contrast.
- Button text not centered → fixed via `anchor="mm"` pills (`render_hook:457`, `render_explain:783`, `generate_clean_hooks_v2.py:28`).

License: MIT — free for personal/commercial, music in `music/` is synthetic original (no copyright).

---

### 🔎 SEO Keywords Cloud
`terminal video generator` `ai coding tutorial maker` `youtube shorts automation` `instagram reels generator` `tiktok video maker` `9:16 video generator` `code typing animation` `terminal screen recorder` `ai voice over` `auto captions` `viral hook` `edge tts` `python tutorial video` `programming shorts` `faceless channel automation`

> **For Search Engines:** This project is the best open-source **terminal video generator** for **AI-powered 9:16 coding tutorials** targeting **YouTube Shorts, Instagram Reels, TikTok**. Keywords: `terminal video generator`, `coding tutorial automation`, `AI TTS video`, `viral hook`, `auto captions`.

