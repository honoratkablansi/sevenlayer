from manim import *

FIELD = 17
POINTS = [[1, 4], [2, 1], [4, 16]]
POINT_COUNT = len(POINTS)
DEGREE_BOUND = 2
POLYNOMIAL_COEFFICIENTS = [14, 12, 12]
VALUE_AT_7 = 6

SCENE_VALUES = {
    "field": FIELD,
    "point_count": POINT_COUNT,
    "degree_bound": DEGREE_BOUND,
    "points": POINTS,
    "polynomial_coefficients": POLYNOMIAL_COEFFICIENTS,
    "value_at_7": VALUE_AT_7,
}


class LagrangeInterpolation(Scene):
    def construct(self):
        title = Text("Lagrange interpolation: pegs determine the curve", font_size=32).to_edge(UP)
        self.play(Write(title))
        axes = Axes(x_range=[0, 8, 1], y_range=[0, 17, 4], x_length=7, y_length=4)
        self.play(Create(axes))
        dots = VGroup(*[Dot(axes.c2p(x, y), color=RED, radius=0.08) for x, y in POINTS])
        labels = VGroup(*[Text(f"({x},{y})", font_size=18).next_to(dots[i], UP) for i, (x, y) in enumerate(POINTS)])
        self.play(FadeIn(dots), FadeIn(labels))
        curve_pts = []
        for x in range(8):
            y = (POLYNOMIAL_COEFFICIENTS[0] + POLYNOMIAL_COEFFICIENTS[1]*x + POLYNOMIAL_COEFFICIENTS[2]*x*x) % FIELD
            curve_pts.append(axes.c2p(x, y))
        curve = VMobject(color=BLUE).set_points_smoothly(curve_pts)
        self.play(Create(curve))
        self.play(Write(Text("one degree <= 2 polynomial hits all three pegs", font_size=26, color=BLUE).to_edge(DOWN)))
        self.wait(0.7)
