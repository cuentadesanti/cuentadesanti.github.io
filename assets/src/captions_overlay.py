from manim import *
from _shared import *

# Beat captions synced to the concatenated cut (mauricio-demo-full.mp4).
# Rendered on a transparent background and composited with ffmpeg `overlay`,
# because this ffmpeg build ships without libass/drawtext. Timings mirror captions.srt.
CAPTIONS = [
    (0.20,  2.60, "I asked for a feature it didn't have."),
    (2.60,  4.70, "It opened the PR itself."),
    (8.50, 12.50, "Voice satellite: wake word → STT → backend"),
    (15.50, 18.50, "memory + knowledge retrieved in parallel"),
    (18.50, 22.00, "LLM ⇄ tools loop, then TTS out"),
    (29.50, 32.50, "propose_new_tool → triage LLM"),
    (33.50, 36.50, "Claude Code runs headless — with hard constraints"),
    (37.00, 39.50, "tests pass → PR opens itself"),
    (39.50, 42.20, "a human still clicks merge"),
]
TOTAL = 47.233333
FADE = 0.14


def caption(text):
    t = Text(text, font=FONT, font_size=25, color=WHITE)
    bg = SurroundingRectangle(t, color=BLACK, fill_color="#0d1117", fill_opacity=0.74,
                              stroke_width=0, corner_radius=0.09, buff=0.20)
    return VGroup(bg, t).to_edge(DOWN, buff=0.5)


class CaptionsOverlay(Scene):
    def construct(self):
        t = 0.0
        for start, end, text in CAPTIONS:
            if start > t:
                self.wait(start - t)
                t = start
            grp = caption(text)
            self.play(FadeIn(grp, run_time=FADE))
            hold = max(0.02, (end - start) - 2 * FADE)
            self.wait(hold)
            self.play(FadeOut(grp, run_time=FADE))
            t = end
        if TOTAL > t:
            self.wait(TOTAL - t)
