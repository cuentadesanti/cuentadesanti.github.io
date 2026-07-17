from manim import *

config.background_color = "#0d1117"
FONT = "Helvetica Neue"

BLUE_L   = "#3B82F6"   # voice I/O
GREEN_L  = "#25D366"   # whatsapp entry
SLATE_L  = "#64748B"   # backend
VIOLET_L = "#8B5CF6"   # llm
AMBER_L  = "#F59E0B"   # tools
EMER_L   = "#10B981"   # data
ROSE_L   = "#F43F5E"   # audio out
LINE_C   = "#94A3B8"
SUB_C    = "#8B98A9"


def node(title, sub, color, w=2.35, h=0.98):
    box = RoundedRectangle(corner_radius=0.11, width=w, height=h,
                           stroke_color=color, stroke_width=3.0,
                           fill_color=color, fill_opacity=0.12)
    t = Text(title, font=FONT, font_size=21, color=WHITE, weight=BOLD)
    s = Text(sub, font=FONT, font_size=13.5, color=SUB_C)
    lbl = VGroup(t, s).arrange(DOWN, buff=0.09).move_to(box.get_center())
    g = VGroup(box, lbl)
    g.box = box
    return g


def edge(box, side, off=0.0):
    """Point at the centre of a box edge, shifted along it by `off` (fraction of half-extent)."""
    if side == "L": return box.get_left()   + UP    * off * box.height / 2
    if side == "R": return box.get_right()  + UP    * off * box.height / 2
    if side == "T": return box.get_top()    + RIGHT * off * box.width  / 2
    if side == "B": return box.get_bottom() + RIGHT * off * box.width  / 2


def arrow(p1, p2, color=LINE_C, dashed=False, width=3.0, arc=0.0):
    a = Arrow(p1, p2, buff=0.05, stroke_width=width, color=color, path_arc=arc,
              max_tip_length_to_length_ratio=0.085, max_stroke_width_to_length_ratio=7)
    if dashed:
        return VGroup(DashedVMobject(Line(a.get_start(), a.get_end(),
                      stroke_width=width, color=color), num_dashes=12), a.tip)
    return a


class MauricioArch(Scene):
    def construct(self):
        title = Text("Mauricio — request architecture", font=FONT,
                     font_size=30, color=WHITE, weight=BOLD).to_edge(UP, buff=0.35)
        sub = Text("self-hosted personal AI · voice + WhatsApp entry",
                   font=FONT, font_size=16, color=SUB_C).next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(title, shift=DOWN*0.2), FadeIn(sub))
        self.wait(0.3)
        self.play(VGroup(title, sub).animate.scale(0.85).to_edge(UP, buff=0.2))

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
        dot = Dot(color=YELLOW, radius=0.11).move_to(sat.box.get_center())
        glow = dot.copy().set_opacity(0.35).scale(2.2)
        glow.add_updater(lambda m: m.move_to(dot.get_center()))
        self.add(glow, dot)

        def step(target, color=YELLOW):
            self.play(dot.animate.move_to(target.box.get_center()), run_time=0.48,
                      rate_func=rate_functions.ease_in_out_sine)
            self.play(Indicate(target.box, scale_factor=1.12, color=color), run_time=0.33)

        for nd in (sat, wake, vad, stt, backend):
            step(nd)

        # WhatsApp shown as the alternate entry into the backend
        self.play(Indicate(wa.box, color=GREEN_L, scale_factor=1.12),
                  a_wb.animate.set_stroke(width=5.5), run_time=0.6)
        self.play(a_wb.animate.set_stroke(width=3), run_time=0.25)

        # retrieval (memory + knowledge → llm)
        self.play(Indicate(mem.box, color=EMER_L, scale_factor=1.1),
                  Indicate(rag.box, color=EMER_L, scale_factor=1.1),
                  a_ml.animate.set_stroke(width=5), a_rl.animate.set_stroke(width=5), run_time=0.7)
        self.play(a_ml.animate.set_stroke(width=3), a_rl.animate.set_stroke(width=3), run_time=0.3)

        step(llm, VIOLET_L)
        for _ in range(2):
            self.play(dot.animate.move_to(tools.box.get_center()), run_time=0.4)
            self.play(Indicate(tools.box, color=AMBER_L, scale_factor=1.1), run_time=0.3)
            self.play(dot.animate.move_to(llm.box.get_center()), run_time=0.4)
        self.play(Indicate(llm.box, color=VIOLET_L, scale_factor=1.1), run_time=0.3)

        for nd in (tts, spk):
            step(nd, ROSE_L)
        self.play(FadeOut(dot), FadeOut(glow), run_time=0.3)

        note = Text("async  ·  memory extraction  ·  summarization  ·  Langfuse tracing",
                    font=FONT, font_size=15, color=SUB_C).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note))
        self.wait(1.6)
