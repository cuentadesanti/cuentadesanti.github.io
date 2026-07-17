# SPEC — Mauricio demo video, Manim extension

**Para:** Claude Code, corriendo local en `cuentadesanti.github.io`
**Contexto:** ya existe `assets/src/mauricio_arch.py` → renderiza `assets/mauricio-arch.mp4` (22s), usado como card en el portfolio. Es una animación de arquitectura de request (voice + WhatsApp → backend → LLM ⇄ tools → TTS) con un token amarillo que recorre el flujo.

**Objetivo de esta tarea:** extender esa misma pieza a una secuencia de 2 escenas que cubra también el **self-improvement loop** (la feature más fuerte del proyecto: `propose_new_tool` → triage → git worktree → Claude Code headless → pytest → PR), manteniendo idéntico lenguaje visual, y dejar un pipeline de render + concat + captions listo para producir un cut de ~45-55s apto para portfolio/LinkedIn.

**No-goals:** no tocar el repo `mauricio-clean`. No grabar screen-capture real (eso es aparte). No rediseñar la paleta ni la tipografía — solo extenderla con 2 colores nuevos.

---

## 0. Qué ya existe (no reescribir, solo refactorizar para reusar)

`assets/src/mauricio_arch.py` — clase `MauricioArch(Scene)`. Contiene inline:
- paleta: `BLUE_L`, `GREEN_L`, `SLATE_L`, `VIOLET_L`, `AMBER_L`, `EMER_L`, `ROSE_L`, `LINE_C`, `SUB_C`
- `FONT = "Helvetica Neue"`, `config.background_color = "#0d1117"`
- helpers: `node(title, sub, color, w, h)`, `edge(box, side, off)`, `arrow(p1, p2, color, dashed, width, arc)`
- patrón de animación: `LaggedStart(*[FadeIn(n, shift=UP*0.15) ...])` para nodos, `Create()` para flechas, y un token (`Dot` + `glow` con `add_updater`) que viaja con `step(target, color)` = `animate.move_to(...)` + `Indicate(...)`.

Este patrón es el "sistema de diseño" de la pieza. La escena nueva debe reusarlo, no reinventarlo.

---

## 1. Refactor — extraer primitives a `_shared.py`

Crear `assets/src/_shared.py`:

```python
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
```

Then edit `mauricio_arch.py`:
- delete the inline palette/helpers block (lines 1–43 of the current file)
- replace with `from _shared import *`
- replace the manual title code (lines 48–54) with `title, sub = title_block(self, "Mauricio — request architecture", "self-hosted personal AI · voice + WhatsApp entry")`
- replace the manual dot/glow setup (lines 108–111) with `dot, glow = flow_token(self, sat)`
- replace the local `step()` def with calls to the shared `step(self, dot, target, color)`

Run `manim -qm --format mp4 -o mauricio_arch mauricio_arch.py MauricioArch` after the refactor and diff the output frame-by-frame against the existing `assets/mauricio-arch.mp4` — **pixel output must be unchanged**. This refactor is pure extraction, zero visual delta. Treat any diff as a bug.

---

## 2. New scene — `assets/src/self_improve_arch.py`

Covers: `propose_new_tool` → triage LLM (viable/clarify/not_viable) → git worktree → Claude Code headless (with hard constraints) → pytest → `gh pr create` → human merge. This is the literal flow in `apps/backend/services/improvement_orchestrator.py` from the mauricio-clean repo (already reviewed — do not re-derive it differently).

```python
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
```

Layout notes for whoever renders/tunes this: frame is ~14.2 × 8 units (same as the existing scene — do not change `config.frame_width/height`). Positions above keep everything inside the same visible bounds the original used (x: -5.4 to 5.0, y: -1.5 to 2.5), so both scenes crop identically if concatenated.

---

## 3. Title / end cards — `assets/src/title_cards.py`

Short bookends so the concatenated cut has a cold open and a close, matching the "PR is the hook" idea from the storyboard.

```python
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
```

---

## 4. Render + concat pipeline

```bash
cd assets/src

# render all scenes at production quality
manim -qm --format mp4 -o cold        title_cards.py     MauricioCold
manim -qm --format mp4 -o arch        mauricio_arch.py    MauricioArch
manim -qm --format mp4 -o selfimprove self_improve_arch.py MauricioSelfImprove
manim -qm --format mp4 -o end         title_cards.py     MauricioEnd

# web-optimize each the same way the existing mauricio-arch.mp4 was done
for name in cold arch selfimprove end; do
  ffmpeg -y -i media/videos/*/720p30/${name}.mp4 \
    -movflags +faststart -c:v libx264 -pix_fmt yuv420p -crf 24 -preset slow -an \
    ../mauricio-${name}.mp4
done

# concat with a short crossfade between segments (xfade requires re-encode; do this last)
ffmpeg -y \
  -i ../mauricio-cold.mp4 -i ../mauricio-arch.mp4 \
  -i ../mauricio-selfimprove.mp4 -i ../mauricio-end.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=0.4:offset=2.6[v01]; \
    [v01][2:v]xfade=transition=fade:duration=0.4:offset=24.5[v012]; \
    [v012][3:v]xfade=transition=fade:duration=0.4:offset=42.5[vout]" \
  -map "[vout]" -c:v libx264 -pix_fmt yuv420p -crf 22 -preset slow \
  ../mauricio-demo-full.mp4

# poster frame for the portfolio card (unchanged approach)
ffmpeg -y -ss 21 -i media/videos/mauricio_arch/720p30/mauricio_arch.mp4 -frames:v 1 ../mauricio-arch.jpg
```

**Note on the `xfade` offsets above:** they're placeholders computed from nominal scene durations (cold ≈3s, arch ≈22.5s existing, selfimprove ≈20s estimated, end ≈3s). After rendering, get real durations with `ffprobe -show_entries format=duration` on each clip and recompute offsets as `cumulative_duration_so_far − crossfade_duration`. Do not hardcode — script it:

```bash
dur() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
d0=$(dur ../mauricio-cold.mp4); d1=$(dur ../mauricio-arch.mp4); d2=$(dur ../mauricio-selfimprove.mp4)
off1=$(echo "$d0 - 0.4" | bc); off2=$(echo "$d0 + $d1 - 0.8" | bc)
```

---

## 5. Captions (burn-in, since the cut must work muted on LinkedIn/X)

Generate an `.srt` alongside the concatenated video, timed to the beats each scene already animates (not a full VO transcript — short beat captions, 3-5 words, synced to each `step()`/`Indicate` call):

```srt
1
00:00:00,000 --> 00:00:02,600
I asked for a feature it didn't have.

2
00:00:02,600 --> 00:00:05,000
It opened the PR itself.

3
00:00:06,500 --> 00:00:10,000
Voice satellite: wake word → STT → backend

4
00:00:14,000 --> 00:00:17,500
memory + knowledge retrieved in parallel

5
00:00:17,500 --> 00:00:21,000
LLM ⇄ tools loop, then TTS out

6
00:00:26,000 --> 00:00:29,000
propose_new_tool → triage LLM

7
00:00:33,000 --> 00:00:36,500
Claude Code runs headless — with hard constraints

8
00:00:39,000 --> 00:00:41,500
tests pass → PR opens itself

9
00:00:41,500 --> 00:00:44,000
a human still clicks merge
```

Timings are placeholders keyed to the *nominal* per-scene durations above — recompute against actual rendered durations before burning in. Burn with:

```bash
ffmpeg -y -i ../mauricio-demo-full.mp4 -vf "subtitles=captions.srt:force_style='FontName=Helvetica Neue,FontSize=16,PrimaryColour=&HFFFFFF&,OutlineColour=&H0d1117&,BorderStyle=1,Outline=1.5,Shadow=0,Alignment=2,MarginV=40'" \
  -c:v libx264 -pix_fmt yuv420p -crf 22 -preset slow -an \
  ../mauricio-demo-full-captioned.mp4
```

---

## 6. Acceptance criteria

- [ ] `_shared.py` extraction produces byte-for-byte-equivalent frames on `MauricioArch` vs the current committed `assets/mauricio-arch.mp4` (spot-check 5 frames with `ffmpeg -ss`)
- [ ] `MauricioSelfImprove` renders clean at `-qm` 720p30, no overlapping labels, no arrow crossing through a box
- [ ] Same background color (`#0d1117`), same font, same node corner radius / stroke width across both scenes — visually indistinguishable "system"
- [ ] Two new colors (`CYAN_L`, `INDIGO_L`) don't collide semantically with existing ones (CYAN reads as "agent/code", INDIGO reads as "GitHub/PR" — check on a colorblind simulator, e.g. Coblis, since AMBER/EMER/CYAN can be close for deuteranopes)
- [ ] Concatenated `mauricio-demo-full.mp4` total runtime 45-55s
- [ ] Captioned version passes the "watch muted" test — every beat is legible without audio
- [ ] `assets/src/README.md` updated with render commands for the 4 new/changed scenes

## Deliverables (files to create/modify)

```
assets/src/_shared.py                 [new]
assets/src/mauricio_arch.py           [refactored — imports from _shared, zero visual delta]
assets/src/self_improve_arch.py       [new]
assets/src/title_cards.py             [new]
assets/src/README.md                  [updated with new render instructions]
assets/mauricio-selfimprove.mp4       [rendered]
assets/mauricio-cold.mp4              [rendered]
assets/mauricio-end.mp4               [rendered]
assets/mauricio-demo-full.mp4         [concatenated]
assets/mauricio-demo-full-captioned.mp4 [captioned, final deliverable]
assets/src/captions.srt               [new]
```

Do not modify `mauricio-arch.jpg`'s generation logic or its use as the portfolio card poster — that stays as-is; this work only adds the extended cut as a separate asset.
