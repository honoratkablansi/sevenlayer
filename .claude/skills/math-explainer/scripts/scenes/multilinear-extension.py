"""manim scene for the multilinear extension (MLE).

Extends 4 discrete corner values on the unit square {0,1}^2 to the unique
SMOOTH bilinear surface that interpolates them. It shows two load-bearing facts:
(1) the surface AGREES with f on every corner, and (2) it is LINEAR along each
axis (slide one coordinate with the other fixed and the height moves on a
straight line). The center value is the average of the four corners.

This is the n = 2 picture of the general MLE drawn in the Sage manifest at
n = 3; the displayed numeric values mirror the manifest's picture_* fields.

NO LaTeX: the manim conda env has no LaTeX install, so this scene uses only
Pango Text / MarkupText and geometric mobjects (never Tex / MathTex). Unicode
(x1, x2, average symbols) renders fine.

Displayed computed values live in SCENE_VALUES so Stage 4 can validate them
against the Sage manifest (picture corners [1,4,3,6], center 3.5, edge mid 2.0)
with no drift.

Render a clip with: render_scene(Path('scripts/scenes/multilinear-extension.py'),
'MultilinearExtension', Path('assets/manim-multilinear-extension'), still=False).
"""
from manim import (
    Scene, Text, VGroup, Dot, Line, Square, Polygon, Create, FadeIn, FadeOut,
    Write, Flash, Indicate, MoveAlongPath, BLUE, RED, YELLOW, GREEN, GREY,
    ORANGE, WHITE, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN,
)

# --- Math, correct-by-construction (mirrors the n=2 picture in the recipe) ---
# Corner values of f on the unit square {0,1}^2, keyed (x1, x2):
G = {(0, 0): 1, (0, 1): 4, (1, 0): 3, (1, 1): 6}
CORNER_VALUES = [G[(0, 0)], G[(0, 1)], G[(1, 0)], G[(1, 1)]]  # [1, 4, 3, 6]


def bil(a, b):
    """Bilinear (multilinear, n=2) extension: linear in each coordinate."""
    return ((1 - a) * (1 - b) * G[(0, 0)] + (1 - a) * b * G[(0, 1)]
            + a * (1 - b) * G[(1, 0)] + a * b * G[(1, 1)])


CENTER_VALUE = bil(0.5, 0.5)          # 3.5  == mean(1, 4, 3, 6)
EDGE_MIDPOINT_VALUE = bil(0.5, 0.0)   # 2.0  == mean(corner 1 and corner 3)
AGREES_ON_CORNERS = all(bil(a, b) == G[(a, b)] for (a, b) in G)  # True

# Values this scene asserts on screen; Stage 4 checks these against the Sage
# manifest's picture_* fields via validate_scene_values.
SCENE_VALUES = {
    "picture_corner_values": CORNER_VALUES,   # [1, 4, 3, 6]
    "picture_center": CENTER_VALUE,           # 3.5
    "picture_edge_midpoint": EDGE_MIDPOINT_VALUE,  # 2.0
    "agrees_on_cube": AGREES_ON_CORNERS,      # True
}


def _heat_color(v):
    """Map a value in [1,6] to a cool->warm color for the surface fill."""
    t = (v - 1.0) / 5.0
    # interpolate BLUE -> GREEN -> YELLOW -> RED via manim's interpolate
    if t < 0.5:
        return BLUE.interpolate(GREEN, t / 0.5)
    return YELLOW.interpolate(RED, (t - 0.5) / 0.5)


class MultilinearExtension(Scene):
    def construct(self):
        title = Text("Multilinear extension: 4 corners → one smooth surface",
                     font_size=30, color=WHITE).to_edge(UP)
        self.play(Write(title))

        subtitle = Text("f on {0,1}² extended to the unique bilinear surface",
                        font_size=22, color=GREY).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle))

        # --- Lay out a unit square on screen (the domain {0,1}^2). ---
        scale = 3.0
        x0, y0 = -1.5, -1.6           # bottom-left screen coords of corner (0,0)

        def screen(a, b):
            return [x0 + a * scale, y0 + b * scale, 0]

        # Smooth bilinear surface as a grid of small filled cells (heatmap).
        cells = VGroup()
        steps = 14
        ds = 1.0 / steps
        cell_w = scale * ds
        for i in range(steps):
            for j in range(steps):
                a = (i + 0.5) * ds
                b = (j + 0.5) * ds
                v = bil(a, b)
                sq = Square(side_length=cell_w,
                            fill_color=_heat_color(v), fill_opacity=0.9,
                            stroke_width=0)
                sq.move_to(screen(a, b))
                cells.add(sq)
        self.play(FadeIn(cells, run_time=1.0))

        # Axis labels.
        ax1 = Text("x1", font_size=20, color=GREY).move_to(screen(0.5, -0.18))
        ax2 = Text("x2", font_size=20, color=GREY).move_to(screen(-0.2, 0.5))
        self.play(FadeIn(ax1), FadeIn(ax2))

        # --- The four corner values, dropped on the cube corners. ---
        corner_dots = VGroup()
        corner_labels = VGroup()
        offs = {(0, 0): DOWN + LEFT, (0, 1): UP + LEFT,
                (1, 0): DOWN + RIGHT, (1, 1): UP + RIGHT}
        for (a, b), v in G.items():
            d = Dot(screen(a, b), color=WHITE, radius=0.08)
            lab = Text(str(v), font_size=24, color=WHITE)
            lab.next_to(d, offs[(a, b)], buff=0.12)
            corner_dots.add(d)
            corner_labels.add(lab)
        self.play(Create(corner_dots), FadeIn(corner_labels))

        agree = Text("Agrees with f at every corner: 1, 4, 3, 6",
                     font_size=22, color=GREEN).to_edge(DOWN)
        self.play(Write(agree))
        for d in corner_dots:
            self.play(Flash(d, color=GREEN, line_length=0.18), run_time=0.25)
        self.wait(0.3)

        # --- Linear along each axis: slide along the bottom edge x2=0. ---
        self.play(FadeOut(agree))
        edge = Line(screen(0, 0), screen(1, 0), color=ORANGE, stroke_width=5)
        self.play(Create(edge))
        slider = Dot(screen(0, 0), color=ORANGE, radius=0.1)
        self.play(FadeIn(slider))
        lin_msg = Text("Linear along each axis: value moves on a straight line",
                       font_size=22, color=ORANGE).to_edge(DOWN)
        self.play(Write(lin_msg))
        self.play(MoveAlongPath(slider, Line(screen(0, 0), screen(1, 0))),
                  run_time=1.4)
        # Midpoint of that edge: bil(0.5, 0) = 2.0 = average of corners 1 and 3.
        self.play(slider.animate.move_to(screen(0.5, 0.0)), run_time=0.6)
        mid_lab = Text("edge midpoint = 2.0  (½·1 + ½·3)",
                       font_size=20, color=ORANGE).next_to(slider, UP, buff=0.5)
        self.play(FadeIn(mid_lab))
        self.wait(0.4)

        # --- Center value = average of the four corners = 3.5. ---
        self.play(FadeOut(mid_lab), FadeOut(slider), FadeOut(edge),
                  FadeOut(lin_msg))
        center = Dot(screen(0.5, 0.5), color=RED, radius=0.11)
        center_lab = Text("center = 3.5  (average of 1, 4, 3, 6)",
                          font_size=22, color=RED).to_edge(DOWN)
        self.play(FadeIn(center), Flash(center, color=RED, line_length=0.3),
                  Write(center_lab))
        self.play(Indicate(center_lab, color=RED), run_time=0.9)
        self.wait(0.6)
