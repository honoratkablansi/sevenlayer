"""manim scene for the Schwartz-Zippel lemma (pilot).

Animates the random-point spot-check: two distinct degree-2 polynomials over the
small field F_101 are sampled at random points; they disagree almost everywhere and
agree at exactly ONE point (x = 0). This visualizes why a random evaluation catches a
forged polynomial with probability >= 1 - d/|F|.

NO LaTeX: the manim conda env has no LaTeX install, so this scene uses only Pango
Text / MarkupText and geometric mobjects (never Tex / MathTex).

Displayed computed values are kept in SCENE_VALUES so Stage 4 can validate them
against the Sage manifest (field 101, exactly 1 agreement point) with no drift.

Render a clip with: render_scene(Path('scripts/scenes/schwartz_zippel.py'),
'SchwartzZippel', Path('assets/manim'), still=False).
"""
from manim import (
    Scene, Text, VGroup, Dot, Line, Create, FadeIn, FadeOut, Write, Flash,
    Indicate, BLUE, RED, YELLOW, GREEN, GREY, WHITE, UP, DOWN, LEFT, RIGHT,
)

# --- Math, correct-by-construction (mirrors scripts/recipes/schwartz_zippel.sage) ---
FIELD = 101                      # |F| = 101
DEGREE = 2                       # both p and q are degree 2


def _p(x):  # p = 3x^2 + 5x + 7
    return (3 * x * x + 5 * x + 7) % FIELD


def _q(x):  # q = 3x^2 + 2x + 7  (differs from p only in the linear term)
    return (3 * x * x + 2 * x + 7) % FIELD


# The difference p - q = 3x, whose only root over F_101 is x = 0.
AGREEMENT_POINTS = sorted(a for a in range(FIELD) if _p(a) == _q(a))
NUM_AGREEMENTS = len(AGREEMENT_POINTS)   # == 1

# Values this scene asserts on screen; Stage 4 checks these against the Sage manifest.
SCENE_VALUES = {
    "field": FIELD,
    "num_agreements": NUM_AGREEMENTS,
    "degree": DEGREE,
}

# A small, readable window of sample points (the full field is too dense to plot).
SAMPLE_XS = list(range(0, 12))


class SchwartzZippel(Scene):
    def construct(self):
        title = Text("Schwartz-Zippel: a random spot-check catches a fake",
                     font_size=30, color=WHITE).to_edge(UP)
        self.play(Write(title))

        setup = Text("Two different degree-2 polynomials over F_101",
                     font_size=24, color=GREY).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(setup))

        # Legend dots for p and q.
        p_label = Text("p(x) = 3x² + 5x + 7", font_size=22, color=BLUE)
        q_label = Text("q(x) = 3x² + 2x + 7", font_size=22, color=RED)
        legend = VGroup(p_label, q_label).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(LEFT + DOWN).shift(UP * 0.4)
        self.play(FadeIn(legend))

        # Lay out the sample points along a horizontal axis.
        axis_y = -0.3
        x_left = -5.0
        spacing = 0.85
        ticks = VGroup()
        labels = VGroup()
        for i, x in enumerate(SAMPLE_XS):
            cx = x_left + i * spacing
            tick = Line(UP * 0.08, DOWN * 0.08, color=GREY).move_to([cx, axis_y, 0])
            lab = Text(str(x), font_size=18, color=GREY).next_to(tick, DOWN, buff=0.12)
            ticks.add(tick)
            labels.add(lab)
        axis_line = Line([x_left - 0.4, axis_y, 0],
                         [x_left + (len(SAMPLE_XS) - 1) * spacing + 0.4, axis_y, 0],
                         color=GREY)
        x_caption = Text("sample point x", font_size=18, color=GREY)
        x_caption.next_to(axis_line, DOWN, buff=0.6)
        self.play(Create(axis_line), Create(ticks), FadeIn(labels), FadeIn(x_caption))

        # For each sampled x, drop a blue dot (p) and a red dot (q); when they match,
        # flash a green agreement marker. Heights encode the residual p(x)-q(x) = 3x.
        agree_x = None
        for i, x in enumerate(SAMPLE_XS):
            cx = x_left + i * spacing
            pv, qv = _p(x), _q(x)
            # vertical offset proportional to value mod a small window (visual only)
            p_dot = Dot([cx, axis_y + 0.5 + (pv % 7) * 0.12, 0], color=BLUE, radius=0.06)
            q_dot = Dot([cx, axis_y + 0.5 + (qv % 7) * 0.12, 0], color=RED, radius=0.06)
            self.play(FadeIn(p_dot), FadeIn(q_dot), run_time=0.18)
            if pv == qv:
                agree_x = x
                star = Dot([cx, axis_y + 0.5 + (pv % 7) * 0.12, 0],
                           color=GREEN, radius=0.10)
                self.play(FadeIn(star), Flash(star, color=GREEN, line_length=0.3),
                          run_time=0.5)

        # Call out the single agreement.
        verdict = Text(
            f"Across F_101 they agree at exactly {NUM_AGREEMENTS} point (x = 0).",
            font_size=24, color=GREEN).next_to(title, DOWN, buff=0.25)
        self.play(FadeOut(setup), FadeIn(verdict))

        bound = Text(
            "A random x is fooled with prob <= d/|F| = 2/101  (<= 2%).",
            font_size=24, color=YELLOW).next_to(verdict, DOWN, buff=0.2)
        self.play(Write(bound))
        self.wait(0.4)
        # Emphasize the rarity: only the agreement marker is special.
        if agree_x is not None:
            self.play(Indicate(verdict, color=GREEN), run_time=0.8)
        self.wait(0.6)
