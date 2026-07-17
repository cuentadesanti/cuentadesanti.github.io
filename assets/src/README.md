# Source — Mauricio architecture / demo animations

Manim ([Community Edition](https://www.manim.community/)) scenes for the Mauricio pieces.

- `_shared.py` — palette, `node/edge/arrow` primitives, and `title_block/flow_token/step`
  animation helpers. Both diagram scenes import from here so they stay one visual system.
- `mauricio_arch.py` → `MauricioArch` — request architecture (voice + WhatsApp → backend →
  LLM ⇄ tools → TTS). Ships as the portfolio card video `assets/mauricio-arch.mp4`.
- `self_improve_arch.py` → `MauricioSelfImprove` — the self-improvement loop
  (propose_new_tool → triage → git worktree → Claude Code headless → pytest → PR).
- `title_cards.py` → `MauricioCold`, `MauricioEnd` — cold open + end card for the long cut.
- `captions_overlay.py` → `CaptionsOverlay` — timed beat captions on a transparent track
  (see caption note below).

## Requirements
```bash
brew install pango pkg-config      # brings cairo/glib/harfbuzz
pip install manim
export PKG_CONFIG_PATH="$(brew --prefix)/lib/pkgconfig"
```

## Render each scene (720p30)
```bash
manim -qm --format mp4 -o cold        title_cards.py       MauricioCold
manim -qm --format mp4 -o mauricio_arch mauricio_arch.py   MauricioArch
manim -qm --format mp4 -o selfimprove self_improve_arch.py MauricioSelfImprove
manim -qm --format mp4 -o end         title_cards.py       MauricioEnd
```

## Web-optimize (matches how mauricio-arch.mp4 ships)
```bash
opt(){ ffmpeg -y -i "$1" -movflags +faststart -c:v libx264 -pix_fmt yuv420p -crf 24 -preset slow -an "$2"; }
opt media/videos/title_cards/720p30/cold.mp4               ../mauricio-cold.mp4
opt media/videos/mauricio_arch/720p30/mauricio_arch.mp4   ../mauricio-arch.mp4
opt media/videos/self_improve_arch/720p30/selfimprove.mp4 ../mauricio-selfimprove.mp4
opt media/videos/title_cards/720p30/end.mp4               ../mauricio-end.mp4
```

## Concat with crossfades (offsets computed from real durations)
```bash
dur(){ ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
X=0.4
d0=$(dur ../mauricio-cold.mp4); d1=$(dur ../mauricio-arch.mp4); d2=$(dur ../mauricio-selfimprove.mp4)
o01=$(python3 -c "print(f'{$d0-$X:.3f}')")
o12=$(python3 -c "print(f'{$d0+$d1-2*$X:.3f}')")
o23=$(python3 -c "print(f'{$d0+$d1+$d2-3*$X:.3f}')")
ffmpeg -y -i ../mauricio-cold.mp4 -i ../mauricio-arch.mp4 -i ../mauricio-selfimprove.mp4 -i ../mauricio-end.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=$X:offset=$o01[v01];\
[v01][2:v]xfade=transition=fade:duration=$X:offset=$o12[v012];\
[v012][3:v]xfade=transition=fade:duration=$X:offset=$o23[vout]" \
  -map "[vout]" -c:v libx264 -pix_fmt yuv420p -crf 22 -preset slow ../mauricio-demo-full.mp4
```

## Captions (burn-in for muted playback)
`captions.srt` is the source of truth. **This machine's Homebrew ffmpeg is built without
libass/libfreetype**, so the usual `-vf subtitles=captions.srt` does not work. Instead the
captions are rendered as a transparent Manim track and composited — same font, no libass:
```bash
manim -qm -t --format mov -o captions_overlay captions_overlay.py CaptionsOverlay
ffmpeg -y -i ../mauricio-demo-full.mp4 -i media/videos/captions_overlay/720p30/captions_overlay.mov \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto[v]" -map "[v]" \
  -c:v libx264 -pix_fmt yuv420p -crf 22 -preset slow -an ../mauricio-demo-full-captioned.mp4
```
If you have an ffmpeg with libass, you can instead burn `captions.srt` directly with
`-vf "subtitles=captions.srt:force_style='FontName=Helvetica Neue,FontSize=16,...'"`.
Keep `captions.srt` and `captions_overlay.py` timings in sync.

## Poster (unchanged — portfolio card poster)
```bash
ffmpeg -y -ss 21 -i media/videos/mauricio_arch/720p30/mauricio_arch.mp4 -frames:v 1 ../mauricio-arch.jpg
```

## Palette note (accessibility)
New colors: `CYAN_L` = coding agent (Claude Code), `INDIGO_L` = GitHub/PR. Under a
deuteranopia simulation CYAN stays a distinct light blue and separates cleanly from
AMBER/EMER; INDIGO collapses toward BLUE/VIOLET, but those never co-occur ambiguously in a
single scene (BLUE is voice-only in the arch scene; INDIGO and VIOLET are spatially
separated and the flow token disambiguates them).
