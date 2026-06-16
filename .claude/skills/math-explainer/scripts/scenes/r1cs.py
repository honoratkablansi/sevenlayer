from manim import *

FIELD = 17
NUM_VARIABLES = 5
NUM_CONSTRAINTS = 2
WITNESS = [1, 3, 4, 12, 15]
AZ = [3, 15]
BZ = [4, 1]
CZ = [12, 15]
PRODUCTS = [12, 15]
SATISFIED = True

SCENE_VALUES = {
    "field": FIELD,
    "num_variables": NUM_VARIABLES,
    "num_constraints": NUM_CONSTRAINTS,
    "witness": WITNESS,
    "Az": AZ,
    "Bz": BZ,
    "Cz": CZ,
    "products": PRODUCTS,
    "satisfied": SATISFIED,
}


class R1CSScene(Scene):
    def construct(self):
        title = Text("R1CS: every row asks for one product", font_size=34).to_edge(UP)
        self.play(Write(title))
        witness = Text("witness z = [1, x=3, y=4, t=12, out=15]", font_size=25).next_to(title, DOWN)
        self.play(FadeIn(witness))
        row1 = Text("row 1: x * y = t   ->   3 * 4 = 12", font_size=29, color=BLUE).shift(UP * 0.2)
        row2 = Text("row 2: (t + x) * 1 = out   ->   15 * 1 = 15", font_size=27, color=GREEN).next_to(row1, DOWN, buff=0.45)
        self.play(FadeIn(row1), FadeIn(row2))
        verdict = Text("Az o Bz = Cz", font_size=32, color=YELLOW).to_edge(DOWN)
        self.play(Write(verdict))
        self.wait(0.7)
