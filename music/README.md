# Music — copyright-free, short snippet only

This folder is for **optional** background music. The generator only uses an **18-second snippet** (middle cut) looped to video length → you never need to download a full 3-minute track.

## Legit free sources (no copyright strike)

1. **Pixabay Music** — 100% free, no attribution, trending viral loops
   - https://pixabay.com/music/search/viral/
   - Example: search "viral corporate" → download → you get a direct `cdn.pixabay.com/audio/...mp3` link.

2. **YouTube Audio Library** — Studio → Audio Library → Trending → filter “No attribution required”
   - https://studio.youtube.com/channel/UC/music

3. **Mixkit** — free, no attribution
   - https://mixkit.co/free-stock-music/

4. **Uppbeat (free tier)** — 10 free trending tracks/month, cleared for Shorts/Reels
   - https://uppbeat.io/

5. **Chosic / Bensound Free** — filter “No copyright”

> **Viral but safe rule:** If a trending TikTok song is **not** in these libraries, it’s **not** safe to re-upload — even 15s can get claimed. Use the *sound-alike* versions from Pixabay/Mixkit that are tagged “viral”.

## How to use (short snippet, legit)

Put a file **or URL** in `config.yaml`:

```yaml
# local file (put your 15-30s mp3 in music/)
music: "music/viral_loop.mp3"
music_volume: 0.11   # 0.0-0.3, background bed
music_duck: 0.32     # duck to 32% volume under voice (so voice stays clear)

# or direct URL — only 18s will be used, looped:
# music: "https://cdn.pixabay.com/download/audio/2022/03/10/audio_c8c8a73467.mp3?filename=energy-10882.mp3"
```

The generator will:
- download (if URL) to `temp/` (auto-deleted after mux)
- cut middle **18s** (`-ss 3 -t 18`), fade 0.8s, loop to match your `~55s` video
- duck to `music_volume * music_duck` during every narration (0.18s fade), so voice stays clear
- mix at `music_volume` when no voice

Never commit large mp3s — `music/*.mp3` is gitignored. Keep only this README or a 1-sec placeholder.
