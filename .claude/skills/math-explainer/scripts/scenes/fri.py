from manim import *

FIELD = 97
OMEGA = 64
DOMAIN_SIZE = 8
FOLDED_DOMAIN_SIZE = 4
DEGREE_BEFORE = 3
DEGREE_BOUND_BEFORE = 4
DEGREE_AFTER = 1
DEGREE_BOUND_AFTER = 2
BETA = 29
POLY_COEFFS = [7, 11, 5, 3]
FOLDED_COEFFS = [35, 92]

SCENE_VALUES = {
    "field": FIELD,
    "omega": OMEGA,
    "domain_size": DOMAIN_SIZE,
    "folded_domain_size": FOLDED_DOMAIN_SIZE,
    "degree_before": DEGREE_BEFORE,
    "degree_bound_before": DEGREE_BOUND_BEFORE,
    "degree_after": DEGREE_AFTER,
    "degree_bound_after": DEGREE_BOUND_AFTER,
    "beta": BETA,
    "polynomial_coefficients": POLY_COEFFS,
    "folded_coefficients": FOLDED_COEFFS,
    "consistency_check": True,
}


class FRILowDegreeScene(Scene):
    def construct(self):
        title = Text("FRI folding: halve the domain, lower the degree", font_size=31).to_edge(UP)
        self.play(Write(title))
        top = VGroup(*[Dot(LEFT * 3.2 + RIGHT * i * 0.9 + UP * 0.85, color=BLUE) for i in range(8)])
        bottom = VGroup(*[Dot(LEFT * 1.35 + RIGHT * i * 0.9 + DOWN * 0.75, color=GREEN, radius=0.1) for i in range(4)])
        self.play(FadeIn(top))
        arrows = VGroup()
        for i in range(4):
            arrows.add(Arrow(top[i].get_center(), bottom[i].get_center(), buff=0.12, color=GREY))
            arrows.add(Arrow(top[i + 4].get_center(), bottom[i].get_center(), buff=0.12, color=GREY))
        self.play(Create(arrows), FadeIn(bottom))
        beta = Text(f"combine each pair with beta = {BETA}", font_size=25, color=YELLOW)
        self.play(FadeIn(beta))
        before = Text("degree 3 on 8 points", font_size=24, color=BLUE).next_to(top, UP, buff=0.25)
        after = Text("degree 1 on 4 points", font_size=24, color=GREEN).next_to(bottom, DOWN, buff=0.25)
        self.play(FadeIn(before), FadeIn(after))
        check = Text("random pair checks keep the fold honest", font_size=23, color=RED).to_edge(DOWN)
        self.play(FadeIn(check))
        self.wait(0.7)
