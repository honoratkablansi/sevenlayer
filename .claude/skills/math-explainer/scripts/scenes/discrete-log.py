import math
from manim import *

P = 2039
Q = 1019
G = 9
X = 873
H = pow(G, X, P)
BITS = bin(X)[2:]
FORWARD_CHAIN_MULTIPLICATIONS = (len(BITS) - 1) + BITS[1:].count("1")
BRUTE_FORCE_STEPS = X + 1
WORST_CASE_STEPS = Q

SCENE_VALUES = {
    "p": P,
    "group_order": Q,
    "g": G,
    "x": X,
    "h": H,
    "forward_chain_multiplications": FORWARD_CHAIN_MULTIPLICATIONS,
    "brute_force_steps": BRUTE_FORCE_STEPS,
    "worst_case_steps": WORST_CASE_STEPS,
}


def pos(exp, radius=2.25):
    th = 2 * math.pi * exp / Q
    return [radius * math.cos(th), radius * math.sin(th) - 0.15, 0]


class DiscreteLogScene(Scene):
    def construct(self):
        title = Text("Discrete log: easy forward, hard backward", font_size=32).to_edge(UP)
        self.play(Write(title))
        ring = Circle(radius=2.25, color=GREY).shift(DOWN * 0.15)
        self.play(Create(ring))
        label = Text("order 1019 subgroup of F_2039*", font_size=22, color=GREY).next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(label))

        walker = Dot(pos(0), color=BLUE, radius=0.09)
        self.play(FadeIn(walker), FadeIn(Text("g^0", font_size=20, color=BLUE).next_to(walker, UP, buff=0.1)))
        for k in range(1, 11):
            ghost = Dot(pos(k), color=BLUE, radius=0.045).set_opacity(0.55)
            self.play(walker.animate.move_to(pos(k)), FadeIn(ghost), run_time=0.25)
        target = Dot(pos(X), color=RED, radius=0.11)
        target_label = Text(f"h = {H}", font_size=22, color=RED).next_to(target, RIGHT, buff=0.12)
        self.play(FadeIn(target), Write(target_label), Flash(target, color=RED, line_length=0.25))

        forward = Text(f"forward chain: {FORWARD_CHAIN_MULTIPLICATIONS} group multiplications", font_size=22, color=GREEN)
        backward = Text(f"brute-force recovery here: {BRUTE_FORCE_STEPS} candidates; worst case {WORST_CASE_STEPS}", font_size=21, color=YELLOW)
        notes = VGroup(forward, backward).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN)
        self.play(FadeIn(notes))
        self.wait(0.7)
