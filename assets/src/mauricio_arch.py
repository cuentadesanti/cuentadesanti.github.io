from manim import *
from _shared import *


class MauricioArch(Scene):
    def construct(self):
        title, sub = title_block(
            self, "Mauricio — request architecture",
            "self-hosted personal AI · voice + WhatsApp entry",
        )

        # ---------- nodes ----------
        sat  = node("Satellite", "Raspberry Pi", BLUE_L).move_to([-5.30, 2.35, 0])
        wake = node("Wake word", "openWakeWord", BLUE_L).move_to([-5.30, 1.25, 0])
        vad  = node("VAD", "voice activity", BLUE_L).move_to([-5.30, 0.15, 0])
        stt  = node("STT", "Deepgram", BLUE_L).move_to([-5.30, -0.95, 0])
        wa   = node("WhatsApp", "Evolution API", GREEN_L).move_to([-5.30, -2.55, 0])

        backend = node("Backend", "FastAPI orchestrator", SLATE_L, w=2.75).move_to([-1.90, -1.15, 0])
        llm     = node("LLM", "Anthropic", VIOLET_L).move_to([1.60, -1.15, 0])
        tools   = node("Tools", "search · notes · lamp", AMBER_L, w=2.75).move_to([5.00, -1.15, 0])

        mem = node("Memory", "pgvector", EMER_L).move_to([0.20, 1.55, 0])
        rag = node("Knowledge", "RAG chunks", EMER_L).move_to([3.55, 1.55, 0])

        tts = node("TTS", "Piper", ROSE_L).move_to([1.60, -3.00, 0])
        spk = node("Speaker", "PipeWire", ROSE_L).move_to([-1.90, -3.00, 0])

        cont = DashedVMobject(RoundedRectangle(
            corner_radius=0.15, width=2.95, height=4.55, stroke_color=BLUE_L,
            stroke_width=1.8, fill_opacity=0).move_to([-5.30, 0.70, 0]), num_dashes=44)
        cont_lbl = Text("VOICE SATELLITE", font=FONT, font_size=12.5, color=BLUE_L,
                        weight=BOLD).next_to(cont, UP, buff=0.07).align_to(cont, LEFT).shift(RIGHT*0.1)

        # ---------- draw ----------
        self.play(Create(cont), FadeIn(cont_lbl), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(n, shift=UP*0.15) for n in (sat, wake, vad, stt)],
                              lag_ratio=0.16, run_time=1.0))
        self.play(FadeIn(wa, shift=RIGHT*0.15), run_time=0.5)
        self.play(LaggedStart(FadeIn(backend), FadeIn(llm), FadeIn(tools),
                              FadeIn(mem), FadeIn(rag), FadeIn(tts), FadeIn(spk),
                              lag_ratio=0.13, run_time=1.5))

        # ---------- arrows (edge-centred) ----------
        a_sw = arrow(edge(sat, "B"),  edge(wake, "T"), BLUE_L)
        a_wv = arrow(edge(wake, "B"), edge(vad, "T"),  BLUE_L)
        a_vs = arrow(edge(vad, "B"),  edge(stt, "T"),  BLUE_L)
        a_sb = arrow(edge(stt, "R"),  edge(backend, "L", 0.55), BLUE_L)
        a_wb = arrow(edge(wa, "R"),   edge(backend, "L", -0.55), GREEN_L)
        a_bl = arrow(edge(backend, "R"), edge(llm, "L"), LINE_C)
        a_ml = arrow(edge(mem, "B"),  edge(llm, "T", -0.45), EMER_L)
        a_rl = arrow(edge(rag, "B"),  edge(llm, "T", 0.45),  EMER_L)
        a_lt = arrow(edge(llm, "R", 0.62),  edge(tools, "L", 0.62),  AMBER_L)   # call
        a_tl = arrow(edge(tools, "L", -0.62), edge(llm, "R", -0.62), AMBER_L)   # return
        a_lo = arrow(edge(llm, "B"),  edge(tts, "T"), ROSE_L)
        a_ts = arrow(edge(tts, "L"),  edge(spk, "R"), ROSE_L)

        self.play(LaggedStart(*[Create(a) for a in (a_sw, a_wv, a_vs, a_sb, a_wb, a_bl)],
                              lag_ratio=0.16, run_time=1.4))
        self.play(Create(a_ml), Create(a_rl), Create(a_lt), Create(a_tl),
                  Create(a_lo), Create(a_ts), run_time=1.2)

        # ---------- flow token ----------
        dot, glow = flow_token(self, sat)

        for nd in (sat, wake, vad, stt, backend):
            step(self, dot, nd)

        # WhatsApp shown as the alternate entry into the backend
        self.play(Indicate(wa.box, color=GREEN_L, scale_factor=1.12),
                  a_wb.animate.set_stroke(width=5.5), run_time=0.6)
        self.play(a_wb.animate.set_stroke(width=3), run_time=0.25)

        # retrieval (memory + knowledge → llm)
        self.play(Indicate(mem.box, color=EMER_L, scale_factor=1.1),
                  Indicate(rag.box, color=EMER_L, scale_factor=1.1),
                  a_ml.animate.set_stroke(width=5), a_rl.animate.set_stroke(width=5), run_time=0.7)
        self.play(a_ml.animate.set_stroke(width=3), a_rl.animate.set_stroke(width=3), run_time=0.3)

        step(self, dot, llm, VIOLET_L)
        for _ in range(2):
            self.play(dot.animate.move_to(tools.box.get_center()), run_time=0.4)
            self.play(Indicate(tools.box, color=AMBER_L, scale_factor=1.1), run_time=0.3)
            self.play(dot.animate.move_to(llm.box.get_center()), run_time=0.4)
        self.play(Indicate(llm.box, color=VIOLET_L, scale_factor=1.1), run_time=0.3)

        for nd in (tts, spk):
            step(self, dot, nd, ROSE_L)
        self.play(FadeOut(dot), FadeOut(glow), run_time=0.3)

        note = Text("async  ·  memory extraction  ·  summarization  ·  Langfuse tracing",
                    font=FONT, font_size=15, color=SUB_C).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note))
        self.wait(1.6)
