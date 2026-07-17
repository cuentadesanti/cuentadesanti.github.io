from manim import *
from _shared import *


class MauricioCold(Scene):
    """~3s. Not a diagram — just the punchline, to run under the PR screen-capture footage
    in the final edit (this scene is a placeholder card, not meant to cover real footage)."""
    def construct(self):
        line1 = Text("I asked my assistant for a feature it didn't have.",
                     font=FONT, font_size=26, color=WHITE).move_to(UP*0.4)
        line2 = Text("It opened the pull request itself.",
                     font=FONT, font_size=26, color=CYAN_L, weight=BOLD).move_to(DOWN*0.3)
        self.play(FadeIn(line1, shift=UP*0.1))
        self.wait(0.5)
        self.play(FadeIn(line2, shift=UP*0.1))
        self.wait(1.4)
        self.play(FadeOut(line1), FadeOut(line2))


class MauricioEnd(Scene):
    """~3s end card."""
    def construct(self):
        name = Text("MAURICIO", font=FONT, font_size=40, color=WHITE, weight=BOLD)
        tag = Text("self-hosted personal AI", font=FONT, font_size=16, color=SUB_C).next_to(name, DOWN, buff=0.15)
        url = Text("github.com/cuentadesanti/mauricio", font=FONT, font_size=15, color=CYAN_L).next_to(tag, DOWN, buff=0.35)
        self.play(FadeIn(VGroup(name, tag), shift=UP*0.15))
        self.wait(0.3)
        self.play(FadeIn(url))
        self.wait(1.8)
