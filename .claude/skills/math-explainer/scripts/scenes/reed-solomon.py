from manim import *

FIELD = 17
MESSAGE_DEGREE_BOUND = 2
DIMENSION = 3
CODE_LENGTH = 8
DESIGNED_MIN_DISTANCE = 6
MESSAGE = [3, 5, 2]
CODEWORD = [3, 10, 4, 2, 4, 10, 3, 0]
OTHER_MESSAGE = [3, 6, 2]
AGREEMENT_POSITIONS = [0]
REALIZED_DISTANCE = 7

SCENE_VALUES = {
    "field": FIELD,
    "message_degree_bound": MESSAGE_DEGREE_BOUND,
    "dimension": DIMENSION,
    "code_length": CODE_LENGTH,
    "designed_min_distance": DESIGNED_MIN_DISTANCE,
    "message": MESSAGE,
    "codeword": CODEWORD,
    "other_message": OTHER_MESSAGE,
    "agreement_positions": AGREEMENT_POSITIONS,
    "realized_distance": REALIZED_DISTANCE,
}


class ReedSolomonEncoding(Scene):
    def construct(self):
        title = Text("Reed-Solomon: spread a short message into many checks", font_size=31).to_edge(UP)
        self.play(Write(title))
        msg = Text("message coefficients: [3, 5, 2]", font_size=26, color=BLUE).next_to(title, DOWN)
        self.play(FadeIn(msg))
        slots = VGroup()
        for i, v in enumerate(CODEWORD):
            box = Square(0.65, color=BLUE).shift(RIGHT * (i - 3.5) * 0.8)
            lab = Text(str(v), font_size=22).move_to(box)
            slots.add(VGroup(box, lab))
        self.play(LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=0.08))
        caption = Text("8 evaluations over F_17", font_size=26).next_to(slots, DOWN)
        self.play(Write(caption))
        changed = Text("change one coefficient -> 7 positions change", font_size=26, color=RED).to_edge(DOWN)
        self.play(FadeIn(changed))
        self.wait(0.7)
