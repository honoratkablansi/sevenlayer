from manim import *

FIELD = 101
MATRIX_SIZE = 2
SAMPLE_R = [7, 11]
LEFT_VECTOR = [37, 88]
RIGHT_VECTOR = [44, 88]
CATCHES_ERROR = True
FAILURE_BOUND_NUM = 1
FAILURE_BOUND_DEN = 101

SCENE_VALUES = {
    "field": FIELD,
    "matrix_size": MATRIX_SIZE,
    "sample_r": SAMPLE_R,
    "left_vector": LEFT_VECTOR,
    "right_vector": RIGHT_VECTOR,
    "catches_error": CATCHES_ERROR,
    "failure_bound_num": FAILURE_BOUND_NUM,
    "failure_bound_den": FAILURE_BOUND_DEN,
}


class FreivaldsAlgorithm(Scene):
    def construct(self):
        title = Text("Freivalds: test a matrix product by one random shadow", font_size=30).to_edge(UP)
        self.play(Write(title))
        eq = Text("Instead of recomputing AB, compare A(Br) and Cr", font_size=27).next_to(title, DOWN)
        self.play(FadeIn(eq))
        left = Text("A(Br) = [37, 88]", font_size=30, color=BLUE).shift(LEFT * 2 + DOWN * 0.4)
        right = Text("Cr = [44, 88]", font_size=30, color=RED).shift(RIGHT * 2 + DOWN * 0.4)
        self.play(FadeIn(left), FadeIn(right))
        cross = Text("not equal", font_size=34, color=YELLOW).to_edge(DOWN)
        self.play(Write(cross))
        bound = Text("a bad product slips through with probability at most 1/101", font_size=25, color=GREEN).next_to(eq, DOWN)
        self.play(FadeIn(bound))
        self.wait(0.7)
