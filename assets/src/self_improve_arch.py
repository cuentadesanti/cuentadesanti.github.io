from manim import *
from _shared import *


class MauricioSelfImprove(Scene):
    def construct(self):
        title, sub = title_block(
            self,
            "Mauricio — self-improvement loop",
            "propose_new_tool → triage → worktree → PR, autonomously",
        )

        # ---------- nodes ----------
        chat = node("LibreChat", '"add a Spotify tool"', GREEN_L, w=2.75).move_to([-5.35, 2.35, 0])
        triage = node("Triage", "viable? clarify? no?", VIOLET_L, w=2.7).move_to([-1.95, 2.35, 0])

        worktree = node("git worktree", "isolated branch, from main", SLATE_L, w=3.0).move_to([1.55, 0.75, 0])
        claude = node("Claude Code", "headless · --print", CYAN_L, w=2.7).move_to([5.0, 0.75, 0])

        tests = node("pytest", "unit tests · -x", EMER_L, w=2.35).move_to([5.0, -1.15, 0])
        pr = node("gh pr create", "branch + label + checklist", INDIGO_L, w=3.0).move_to([1.55, -1.15, 0])
        human = node("Human review", "clicks Merge", SLATE_L, w=2.7).move_to([-1.95, -1.15, 0])

        # dead-end decision branches (shown, then dimmed — the triage has 3 exits, only one continues)
        not_viable = Text("not_viable → stop", font=FONT, font_size=14, color=SUB_C).move_to([-1.95, 1.15, 0])
        clarify = Text("clarify_needed → ask user", font=FONT, font_size=14, color=SUB_C).move_to([-1.95, 0.65, 0])

        # constraints callout — appears briefly over Claude Code, this is the "barandales" beat
        constraints = VGroup(
            Text("hard constraints:", font=FONT, font_size=13, color=CYAN_L, weight=BOLD),
            Text("no migrations · no secrets · no self-modify", font=FONT, font_size=13, color=SUB_C),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([5.0, 2.15, 0])
        constraints_box = SurroundingRectangle(constraints, color=CYAN_L, corner_radius=0.08,
                                                stroke_width=1.6, buff=0.16)

        # ---------- draw ----------
        self.play(LaggedStart(FadeIn(chat, shift=UP*0.15), FadeIn(triage, shift=UP*0.15),
                              lag_ratio=0.2, run_time=0.8))
        self.play(LaggedStart(FadeIn(worktree), FadeIn(claude), FadeIn(tests), FadeIn(pr), FadeIn(human),
                              lag_ratio=0.13, run_time=1.4))

        a_ct = arrow(edge(chat, "R"), edge(triage, "L"), GREEN_L)
        a_tw = arrow(edge(triage, "B"), edge(worktree, "T", -0.3), VIOLET_L, arc=-0.3)
        a_wc = arrow(edge(worktree, "R"), edge(claude, "L"), SLATE_L)
        a_ck = arrow(edge(claude, "B"), edge(tests, "T"), CYAN_L)
        a_kp = arrow(edge(tests, "L"), edge(pr, "R"), EMER_L)
        a_ph = arrow(edge(pr, "L"), edge(human, "R"), INDIGO_L)
        a_retry = arrow(edge(tests, "T", 0.4), edge(claude, "B", -0.4), color=SUB_C, dashed=True, width=2.0, arc=0.6)

        self.play(LaggedStart(*[Create(a) for a in (a_ct, a_tw, a_wc, a_ck, a_kp, a_ph)],
                              lag_ratio=0.15, run_time=1.3))
        self.play(Create(a_retry), run_time=0.5)

        # ---------- flow token ----------
        dot, glow = flow_token(self, chat)
        step(self, dot, triage, VIOLET_L)

        # show the 3-way decision, dim the two dead ends, keep "viable" implied by continuing
        self.play(FadeIn(not_viable), FadeIn(clarify), run_time=0.4)
        self.play(not_viable.animate.set_opacity(0.35), clarify.animate.set_opacity(0.35), run_time=0.4)

        step(self, dot, worktree, SLATE_L)
        step(self, dot, claude, CYAN_L)

        # constraints beat — pause on Claude Code, show the guardrails
        self.play(Create(constraints_box), FadeIn(constraints), run_time=0.6)
        self.wait(0.9)
        self.play(FadeOut(constraints_box), FadeOut(constraints), run_time=0.4)

        step(self, dot, tests, EMER_L)
        step(self, dot, pr, INDIGO_L)
        step(self, dot, human, SLATE_L)
        self.play(FadeOut(dot), FadeOut(glow), run_time=0.3)

        note = Text("the system doesn't auto-merge — it self-proposes",
                    font=FONT, font_size=15, color=SUB_C).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note))
        self.wait(1.6)
