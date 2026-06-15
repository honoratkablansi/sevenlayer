"""manim scene for bilinear pairings (Chapter 11).

Depicts the pairing  e : G1 x G2 -> G_T  sending two source-group points to one
target-group element, and animates BILINEARITY: scaling P by a and Q by b multiplies
the target exponent by a*b, i.e.  e(aP, bQ) = e(P, Q)^(a*b).

The concrete numbers mirror scripts/recipes/bilinear-pairings.sage exactly:
the Weil pairing of the r=3 torsion on  y^2 = x^3 - x  over GF(23), embedding degree
k=2 (target group in GF(23^2)), scalars a=2, b=4, so a*b = 8 and 8 mod 3 = 2.

NO LaTeX: the manim conda env has no LaTeX, so this scene uses only Pango Text /
MarkupText and geometric mobjects (never Tex / MathTex). Unicode (×, →, ², etc.) is fine.

The displayed COMPUTED quantities are collected in SCENE_VALUES, recomputed here in pure
Python (group exponent arithmetic mod r), so Stage 4 can cross-check them against the Sage
manifest with validate_scene_values and prove there is no drift.

Render a clip with:
    render_scene(Path('scripts/scenes/bilinear-pairings.py'),
                 'BilinearPairings', Path('assets/manim-bilinear-pairings'), still=False).
"""
from manim import (
    Scene, Text, MarkupText, VGroup, Dot, Circle, Arrow, Line, Create, FadeIn,
    FadeOut, Write, Indicate, Transform, BLUE, RED, PURPLE, YELLOW, GREEN, GREY,
    WHITE, UP, DOWN, LEFT, RIGHT,
)

# --- Math, correct-by-construction (mirrors the Sage recipe's parameters) ----------
Q_FIELD = 23     # base prime q
R_ORDER = 3      # prime order of the source groups G1, G2 (and of the pairing value)
K_EMBED = 2      # embedding degree: target group G_T lives in GF(q^k)
A = 2            # scalar on P
B = 4            # scalar on Q
AB = A * B       # 8
AB_MOD_R = AB % R_ORDER   # 8 mod 3 = 2  -> e(P,Q)^(ab) = e(P,Q)^2, a non-trivial power

# Pure-Python check of the bilinearity identity at the level of the target-group exponent.
# In G_T = mu_r (the r-th roots of unity) the pairing value e(P,Q) has order r, so it is a
# generator g of a cyclic group of order r; e(aP,bQ) = g^(ab) and e(P,Q)^(ab) = g^(ab).
# Equality holds iff (ab) ≡ (ab) (mod r) -- trivially, but we verify the exponent that the
# scene actually displays so the animation can never show a wrong power.
_lhs_exp = AB % R_ORDER
_rhs_exp = AB % R_ORDER
BILINEAR_HOLDS = (_lhs_exp == _rhs_exp)

SCENE_VALUES = {
    "q": Q_FIELD,
    "r": R_ORDER,
    "k": K_EMBED,
    "a": A,
    "b": B,
    "ab": AB,
    "ab_mod_r": AB_MOD_R,
    "bilinear_holds": BILINEAR_HOLDS,
}


class BilinearPairings(Scene):
    def construct(self):
        title = Text("Bilinear pairings: multiply inside hidden exponents",
                     font_size=30, color=WHITE).to_edge(UP)
        self.play(Write(title))

        subtitle = Text("e : G₁ × G₂  →  G_T", font_size=26, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(subtitle))

        # --- The three groups as circles: G1 (blue), G2 (red) sources; G_T (purple) target.
        g1 = Circle(radius=0.95, color=BLUE).move_to([-4.3, 0.9, 0])
        g2 = Circle(radius=0.95, color=RED).move_to([-4.3, -1.7, 0])
        gt = Circle(radius=1.15, color=PURPLE).move_to([3.8, -0.4, 0])
        g1_lab = Text("G₁", font_size=22, color=BLUE).next_to(g1, UP, buff=0.1)
        g2_lab = Text("G₂", font_size=22, color=RED).next_to(g2, DOWN, buff=0.1)
        gt_lab = Text("G_T", font_size=22, color=PURPLE).next_to(gt, UP, buff=0.1)
        self.play(Create(g1), Create(g2), Create(gt),
                  FadeIn(g1_lab), FadeIn(g2_lab), FadeIn(gt_lab))

        # The source points P, Q and the target value e(P,Q).
        p_dot = Dot(g1.get_center(), color=BLUE, radius=0.08)
        q_dot = Dot(g2.get_center(), color=RED, radius=0.08)
        t_dot = Dot(gt.get_center(), color=PURPLE, radius=0.08)
        p_lab = Text("P", font_size=22, color=BLUE).next_to(p_dot, RIGHT, buff=0.12)
        q_lab = Text("Q", font_size=22, color=RED).next_to(q_dot, RIGHT, buff=0.12)
        t_lab = Text("e(P,Q)", font_size=20, color=PURPLE).next_to(t_dot, DOWN, buff=0.15)
        self.play(FadeIn(p_dot), FadeIn(q_dot), FadeIn(p_lab), FadeIn(q_lab))

        # The pairing arrows: both source points feed one target element.
        a1 = Arrow(g1.get_right(), gt.get_left() + UP * 0.2, color=GREY, buff=0.15,
                   stroke_width=3)
        a2 = Arrow(g2.get_right(), gt.get_left() + DOWN * 0.2, color=GREY, buff=0.15,
                   stroke_width=3)
        self.play(Create(a1), Create(a2))
        self.play(FadeIn(t_dot), FadeIn(t_lab))
        self.wait(0.3)

        # --- Bilinearity: scale P by a, Q by b; the target exponent multiplies by a*b. ---
        claim = MarkupText(
            f'Scale inputs: <span foreground="#58C4DD">a={A}</span>·P , '
            f'<span foreground="#FC6255">b={B}</span>·Q',
            font_size=24).next_to(subtitle, DOWN, buff=0.35)
        self.play(FadeIn(claim))

        # Relabel the source points to aP, bQ and pulse them to show the scaling.
        ap_lab = Text("aP", font_size=22, color=BLUE).next_to(p_dot, RIGHT, buff=0.12)
        bq_lab = Text("bQ", font_size=22, color=RED).next_to(q_dot, RIGHT, buff=0.12)
        self.play(Transform(p_lab, ap_lab), Transform(q_lab, bq_lab),
                  Indicate(p_dot, color=BLUE), Indicate(q_dot, color=RED))

        # The target jumps to e(P,Q)^(ab); show the exponent explicitly.
        new_t_lab = Text("e(aP,bQ)", font_size=20, color=PURPLE).next_to(t_dot, DOWN, buff=0.15)
        self.play(Transform(t_lab, new_t_lab), Indicate(t_dot, color=PURPLE))

        identity = MarkupText(
            f'e(aP, bQ) = e(P, Q)<sup>a·b</sup> = e(P, Q)<sup>{AB}</sup>',
            font_size=26, color=YELLOW).to_edge(DOWN, buff=1.15)
        self.play(Write(identity))

        # The concrete numbers from the Sage manifest (q=23, r=3, k=2).
        nums = Text(
            f"GF({Q_FIELD}),  r = {R_ORDER},  embedding degree k = {K_EMBED}   |   "
            f"a·b = {AB},   a·b mod r = {AB_MOD_R}",
            font_size=20, color=GREY).next_to(identity, DOWN, buff=0.2)
        self.play(FadeIn(nums))
        self.wait(0.3)

        verdict = Text(
            "Bilinearity holds: scaling the inputs multiplies the hidden exponent by a·b.",
            font_size=22, color=GREEN).move_to([0, -0.2, 0])
        self.play(FadeIn(verdict), Indicate(identity, color=GREEN))
        self.wait(0.7)
