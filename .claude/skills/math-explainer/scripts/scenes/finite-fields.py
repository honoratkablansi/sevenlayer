from manim import *

FIELD = 17
ADD_A = 14
ADD_B = 5
ADD_RESULT = (ADD_A + ADD_B) % FIELD
MUL_A = 5
MUL_B = 7
MUL_RESULT = (MUL_A * MUL_B) % FIELD
INVERSE_OF = 5
INVERSE_VALUE = 7

SCENE_VALUES = {
    "field": FIELD,
    "modulus": FIELD,
    "add_a": ADD_A,
    "add_b": ADD_B,
    "add_result": ADD_RESULT,
    "mul_a": MUL_A,
    "mul_b": MUL_B,
    "mul_result": MUL_RESULT,
    "inverse_of": INVERSE_OF,
    "inverse_value": INVERSE_VALUE,
}


class FiniteFields(Scene):
    def construct(self):
        title = Text("Finite fields: arithmetic on a closed clock", font_size=34).to_edge(UP)
        self.play(Write(title))
        circle = Circle(radius=2.1, color=GRAY)
        ticks = VGroup()
        labels = VGroup()
        for k in range(FIELD):
            ang = TAU * k / FIELD
            p = circle.point_at_angle(ang)
            dot = Dot(p, radius=0.045, color=WHITE)
            ticks.add(dot)
            if k in [0, 1, 2, 5, 7, 14, 16]:
                labels.add(Text(str(k), font_size=18).move_to(p * 1.16))
        self.play(Create(circle), FadeIn(ticks), FadeIn(labels))
        a_dot = Dot(circle.point_at_angle(TAU * ADD_A / FIELD), color=RED, radius=0.08)
        b_dot = Dot(circle.point_at_angle(TAU * ADD_RESULT / FIELD), color=RED, radius=0.08)
        self.play(FadeIn(a_dot))
        self.play(Rotate(a_dot.copy(), angle=TAU * ADD_B / FIELD, about_point=ORIGIN), FadeIn(b_dot))
        self.play(Write(Text("14 + 5 wraps to 2", font_size=28, color=RED).to_edge(DOWN)))
        self.wait(0.3)
        inv = Text("5 * 7 = 1, so 7 undoes multiplication by 5", font_size=25, color=BLUE).next_to(title, DOWN)
        self.play(FadeIn(inv))
        self.wait(0.6)
