# Contributing to Terminal Video Generator

Thank you for considering contributing! This project thrives on community hooks, themes, voices, and viral loops. Every PR, no matter how small, makes the generator better for faceless coding channels.

## 🚀 Quick Start for Contributors

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/terminal-video-gen.git
   cd terminal-video-gen
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   # ffmpeg is required
   sudo apt install ffmpeg
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feat/your-feature
   # e.g., feat/new-dracula-theme, fix/hook-pill-centering, feat/lofi-music-pack
   ```

3. **Test Locally**
   ```bash
   python terminal_video.py --frame  # preview single frame -> frame_preview.png
   python terminal_video.py          # full video -> output/terminal_video_*.mp4 ( ~55s)
   # check temp/ is created then auto-deleted, vault/ is cleaned
   ```

4. **Push & Open PR**
   ```bash
   git add -A
   git commit -m "feat: add your feature"
   git push origin feat/your-feature
   ```
   Open a Pull Request on GitHub — we review within 48h. Please include:
   - What you changed (theme, hook, voice, music, bugfix)
   - Screenshot of `frame_preview.png` or `hook_previews/` if visual
   - Tested on `light` and `dark` themes (see `apply_theme`)

## 🎯 Good First Issues (SEO-Friendly Labels)

- `good first issue` `theme` — Add a new theme to `THEMES` (`terminal_video.py:69`) with `TERM_BG/EDITOR_BG/ACTIVE_LINE/CARD_BG/ACCENT` + dark `SY_*` for light themes.
- `hook` — Add a new hook layout in `render_hook` (`terminal_video.py:447`) — use `anchor="mm"` for pills, `is_light()` for colors, keep `max_w = RW-70`.
- `music` — Contribute an 18s viral loop to `music/` (phonk/trap/lofi, 128k, 18s, original, no copyright). See `music/README.md`.
- `caption` — Improve `overlay_caption` (`terminal_video.py:906`) animation (pop, slide, underline).
- `bug` — Fix pill padding/centering or light-theme contrast (use `anchor="mm"` and `title_color()` helper).
- `docs` — Improve `README.md` SEO, add FAQ, translate.

## 📐 Code Style & Conventions

- **Single-file core:** Keep `terminal_video.py` readable, single-file. No new dependencies without discussion.
- **Constants:** `RENDER_SCALE 1`, `FPS 30`, `WIDTH 1080, HEIGHT 1920`, `FONT_SIZE 38`, `CRF 15`, `preset medium` — keep for quality.
- **Pills/Buttons:** Always use `draw.text((cx,cy), text, font=FONT, fill=..., anchor="mm")` with `textbbox(anchor="mm")` to compute `bw/bh`. Never use `x - bw//2` manual without anchor.
- **Theme-aware colors:** Use `_is_light()` → `(30,32,35)` on light vs `(230,237,243)` on dark. For syntax, `SY_*` must be dark on light (`SY_PLAIN 45,52,65` on `255`). Check `apply_theme:112`.
- **Logical timing:** No hardcoded `sleep` — use `len(pcm)/SR*FPS + 0.1s` buffer for holds. Animation frames (`LIFT 6f`, `HIGHLIGHT 3f`) are minimal.
- **Captions:** Use `WordBoundary` precise timing (`tts_pcm` → `words`), not char-proportional.

## 🎨 Adding a Theme

1. Add entry to `THEMES`:
```python
"mytheme": {
    "TERM_BG": (20,20,25), "EDITOR_BG": (30,30,35), "ACTIVE_LINE": (50,50,60),
    "CARD_BG": (40,40,50), "STATUS_BG": (35,35,40), "NUM_COLOR": (120,130,145),
    "ACCENT": (255,100,100), "PWD_COLOR": (255,100,100), "PROMPT_COLOR": (80,200,120),
    # for light themes also override CMD/OUTPUT/SY_*
    "CMD_COLOR": (30,32,35), "OUTPUT_COLOR": (75,80,90),
    "SY_PLAIN": (45,52,65), "SY_KW": (155,35,147), ...
},
```
2. Test: `theme: mytheme` in `config.yaml`, run `--frame`, check terminal/editor/hook/caption visibility on both light/dark.

## 🎤 Adding a Voice

List voices: `edge-tts --list-voices | grep en-`. Test: `edge-tts --voice en-US-AriaNeural --text "Hello" --write-media /tmp/test.mp3 --rate "+35%"`. Add to `config.yaml:voice`.

## 🎵 Adding Music

- Create 18s loop (original, no copyright) — `ffmpeg -f lavfi -i sine=...` or export from DAW, `128k`.
- Place in `music/viral_myloop.mp3` (gitignored, but `git add -f` if you want to share).
- Test: `music: "music/viral_myloop.mp3"` or `music: "random"` (picks one of `music/*.mp3`).

## 🧪 Testing Checklist

- [ ] `python terminal_video.py --frame` shows hook correctly centered, no overflow, pill text centered (check `light` and `dark` themes)
- [ ] `python terminal_video.py` generates `output/*.mp4` `<60s`, no `temp/` or `vault/` left behind
- [ ] Captions highlight word-precisely (no drift)
- [ ] `ls` on empty `vault` shows ` (empty)`

## 📜 License

By contributing, you agree your contributions are MIT licensed. Be original — no copyrighted music/code.

## 💬 Community

- ⭐ Star the repo to support
- Open an **Issue** for bugs
- Start a **Discussion** for hook ideas
- Tag your PR with `SEO` keywords: `terminal video generator`, `AI TTS`, `9:16` to help discovery.

Thank you! 🙏
