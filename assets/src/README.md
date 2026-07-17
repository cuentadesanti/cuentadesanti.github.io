# Source — Mauricio architecture animation

`mauricio_arch.py` is the [Manim](https://www.manim.community/) scene that renders the
voice/WhatsApp request-architecture animation shown on the Mauricio card
(`assets/mauricio-arch.mp4`).

## Requirements
- Python 3, `manim` (Community Edition), `ffmpeg`, and system `cairo` + `pango`.
  ```bash
  brew install pango pkg-config      # brings cairo/glib/harfbuzz
  pip install manim
  ```

## Render
```bash
# 720p30 mp4
manim -qm --format mp4 -o mauricio_arch mauricio_arch.py MauricioArch

# web-optimize (what ships in assets/), then a poster frame
ffmpeg -y -i media/videos/mauricio_arch/720p30/mauricio_arch.mp4 \
  -movflags +faststart -c:v libx264 -pix_fmt yuv420p -crf 24 -preset slow -an \
  ../mauricio-arch.mp4
ffmpeg -y -ss 21 -i media/videos/mauricio_arch/720p30/mauricio_arch.mp4 \
  -frames:v 1 ../mauricio-arch.jpg
```

The diagram is a standard systems/software architecture layout: subsystem container
(voice satellite) + WhatsApp entry, backend orchestrator, LLM ⇄ tools loop, memory/RAG,
and TTS output, with a token animating the request path.
