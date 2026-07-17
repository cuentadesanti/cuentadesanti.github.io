from manim import *

config.background_color = "#0d1117"
FONT = "Helvetica Neue"

# --- palette (existing, unchanged) ---
BLUE_L   = "#3B82F6"   # voice I/O
GREEN_L  = "#25D366"   # whatsapp / chat entry
SLATE_L  = "#64748B"   # backend / infra
VIOLET_L = "#8B5CF6"   # llm
AMBER_L  = "#F59E0B"   # tools
EMER_L   = "#10B981"   # data / success
ROSE_L   = "#F43F5E"   # audio out
LINE_C   = "#94A3B8"
SUB_C    = "#8B98A9"

# --- palette (new, for self-improvement scene) ---
CYAN_L   = "#22D3EE"   # coding agent (Claude Code)
INDIGO_L = "#6366F1"   # github / PR


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


def title_block(scene, title_text, sub_text):
    """Standard title-then-shrink-to-corner intro used by both scenes."""
    title = Text(title_text, font=FONT, font_size=30, color=WHITE,
                 weight=BOLD).to_edge(UP, buff=0.35)
    sub = Text(sub_text, font=FONT, font_size=16, color=SUB_C).next_to(title, DOWN, buff=0.12)
    scene.play(FadeIn(title, shift=DOWN*0.2), FadeIn(sub))
    scene.wait(0.3)
    scene.play(VGroup(title, sub).animate.scale(0.85).to_edge(UP, buff=0.2))
    return title, sub


def flow_token(scene, first_box):
    dot = Dot(color=YELLOW, radius=0.11).move_to(first_box.box.get_center())
    glow = dot.copy().set_opacity(0.35).scale(2.2)
    glow.add_updater(lambda m: m.move_to(dot.get_center()))
    scene.add(glow, dot)
    return dot, glow


def step(scene, dot, target, color=YELLOW, move_rt=0.48, ind_rt=0.33):
    scene.play(dot.animate.move_to(target.box.get_center()), run_time=move_rt,
              rate_func=rate_functions.ease_in_out_sine)
    scene.play(Indicate(target.box, scale_factor=1.12, color=color), run_time=ind_rt)
