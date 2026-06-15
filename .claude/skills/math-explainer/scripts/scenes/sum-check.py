"""manim scene for the Sum-Check protocol (Chapter 8).

Animates the round-by-round reduction that collapses a sum over the Boolean hypercube
{0,1}^3 into a single evaluation. Each round the prover sends a univariate polynomial
g_i(X); the verifier checks g_i(0)+g_i(1) equals the running claim; then a fixed
challenge r_i is plugged in and the claim shrinks to g_i(r_i). The 8-term sum becomes
4, then 2, then 1 -- ending at one evaluation g(r1,r2,r3).

NO LaTeX: the manim conda env has no LaTeX install, so this scene uses only Pango
Text / MarkupText and geometric mobjects (never Tex / MathTex). Unicode (Σ, ², ≤) is fine.

All displayed computed values mirror scripts/recipes/sum-check.sage exactly and are kept
in SCENE_VALUES so Stage 4 can validate them against the Sage manifest with no drift.

Render a clip with: render_scene(Path('scripts/scenes/sum-check.py'),
'SumCheck', Path('assets/manim-sum-check'), still=False).
"""
from manim import (
    Scene, Text, VGroup, Dot, Line, Square, Create, FadeIn, FadeOut, Write,
    Indicate, Transform, BLUE, RED, YELLOW, GREEN, GREY, WHITE, ORANGE,
    UP, DOWN, LEFT, RIGHT,
)

# --- Math, correct-by-construction (mirrors scripts/recipes/sum-check.sage) ---
FIELD = 97
NUM_VARS = 3
# Fixed (reproducible) challenges; the verifier's "random" points, pinned.
CHALLENGES = {1: 2, 2: 3, 3: 4}


def _g(a1, a2, a3):
    """g(x1,x2,x3) = 2*x1^2*x2 + 3*x2*x3 + x1 + 5 over GF(97)."""
    return (2 * a1 * a1 * a2 + 3 * a2 * a3 + a1 + 5) % FIELD


def _poly_eval(coeffs, X):
    """Evaluate ascending-coefficient univariate at X over GF(97)."""
    acc = 0
    pw = 1
    for c in coeffs:
        acc = (acc + c * pw) % FIELD
        pw = (pw * X) % FIELD
    return acc


def _round_poly_coeffs(i):
    """g_i(X) coefficients via Lagrange-free direct construction over GF(97).

    Round i fixes x_1..x_{i-1} to the challenges, sets x_i free, and sums x_{i+1}..x_3
    over {0,1}. We recover the univariate by evaluating it at enough integer points and
    solving for coefficients; degree is 2 for round 1 (x1 appears squared) and 1 after.
    """
    later = list(range(i + 1, NUM_VARS + 1))

    def eval_gi(Xval):
        total = 0
        for bits in range(2 ** len(later)):
            vals = []
            for v in (1, 2, 3):
                if v < i:
                    vals.append(CHALLENGES[v])
                elif v == i:
                    vals.append(Xval)
                else:
                    pos = later.index(v)
                    vals.append((bits >> pos) & 1)
            total = (total + _g(vals[0], vals[1], vals[2])) % FIELD
        return total

    deg = 2 if i == 1 else 1
    # Sample at X = 0..deg and solve the small Vandermonde system over GF(97).
    xs = list(range(deg + 1))
    ys = [eval_gi(xv) for xv in xs]
    if deg == 1:
        c0 = ys[0]
        c1 = (ys[1] - ys[0]) % FIELD
        return [c0, c1]
    # deg == 2: y0=c0; y1=c0+c1+c2; y2=c0+2c1+4c2
    c0 = ys[0]
    inv2 = pow(2, FIELD - 2, FIELD)
    # c2 = (y2 - 2*y1 + y0)/2 ; c1 = y1 - y0 - c2
    c2 = ((ys[2] - 2 * ys[1] + ys[0]) * inv2) % FIELD
    c1 = (ys[1] - ys[0] - c2) % FIELD
    return [c0, c1, c2]


# The claimed sum over {0,1}^3.
H = 0
for _a1 in (0, 1):
    for _a2 in (0, 1):
        for _a3 in (0, 1):
            H = (H + _g(_a1, _a2, _a3)) % FIELD

ROUND_COEFFS = {i: _round_poly_coeffs(i) for i in (1, 2, 3)}
G_AT_0 = {i: _poly_eval(ROUND_COEFFS[i], 0) for i in (1, 2, 3)}
G_AT_1 = {i: _poly_eval(ROUND_COEFFS[i], 1) for i in (1, 2, 3)}
SUM_01 = {i: (G_AT_0[i] + G_AT_1[i]) % FIELD for i in (1, 2, 3)}
G_AT_R = {i: _poly_eval(ROUND_COEFFS[i], CHALLENGES[i]) for i in (1, 2, 3)}
FINAL_EVAL = _g(CHALLENGES[1], CHALLENGES[2], CHALLENGES[3])

# Values this scene asserts on screen; Stage 4 checks these against the Sage manifest.
SCENE_VALUES = {
    "field": FIELD,
    "num_vars": NUM_VARS,
    "H": H,
    "final_eval": FINAL_EVAL,
    "round1_g_at_0": G_AT_0[1],
    "round1_g_at_1": G_AT_1[1],
    "round1_sum_0_1": SUM_01[1],
    "round1_g_at_r": G_AT_R[1],
    "round2_g_at_0": G_AT_0[2],
    "round2_g_at_1": G_AT_1[2],
    "round2_sum_0_1": SUM_01[2],
    "round2_g_at_r": G_AT_R[2],
    "round3_g_at_0": G_AT_0[3],
    "round3_g_at_1": G_AT_1[3],
    "round3_sum_0_1": SUM_01[3],
    "round3_g_at_r": G_AT_R[3],
}

TERMS_REMAINING = {0: 8, 1: 4, 2: 2, 3: 1}


class SumCheck(Scene):
    def construct(self):
        title = Text("Sum-Check: collapse a hypercube sum, one round at a time",
                     font_size=28, color=WHITE).to_edge(UP)
        self.play(Write(title))

        setup = Text("g(x₁,x₂,x₃) = 2x₁²x₂ + 3x₂x₃ + x₁ + 5  over  GF(97)",
                     font_size=24, color=GREY).next_to(title, DOWN, buff=0.22)
        self.play(FadeIn(setup))

        # The claim: H = sum over the 8 corners of {0,1}^3.
        claim = Text(f"Claim:  H = Σ over {{0,1}}³  g(x) = {H}",
                     font_size=26, color=YELLOW).next_to(setup, DOWN, buff=0.3)
        self.play(Write(claim))

        # Draw the 8 hypercube corners as a row of small squares (the terms to fold).
        cubes = VGroup()
        for k in range(8):
            sq = Square(side_length=0.42, color=BLUE, fill_opacity=0.5)
            cubes.add(sq)
        cubes.arrange(RIGHT, buff=0.18).next_to(claim, DOWN, buff=0.45)
        cube_caption = Text("8 hypercube terms", font_size=18, color=GREY)
        cube_caption.next_to(cubes, DOWN, buff=0.2)
        self.play(Create(cubes), FadeIn(cube_caption))
        self.wait(0.3)

        running_claim = H  # the value the verifier is currently asked to trust
        for i in (1, 2, 3):
            c0 = ROUND_COEFFS[i]
            # Prover's message: the univariate g_i(X).
            if len(c0) == 3:
                gi_txt = f"Round {i}: prover sends g{i}(X) = {c0[0]} + {c0[1]}X + {c0[2]}X²"
            else:
                gi_txt = f"Round {i}: prover sends g{i}(X) = {c0[0]} + {c0[1]}X"
            gi = Text(gi_txt, font_size=23, color=ORANGE).next_to(cube_caption, DOWN, buff=0.4)
            self.play(FadeIn(gi))

            # Verifier's check: g_i(0) + g_i(1) == running claim.
            check = Text(
                f"check: g{i}(0)+g{i}(1) = {G_AT_0[i]}+{G_AT_1[i]} = {SUM_01[i]} = {running_claim} ✓",
                font_size=22, color=GREEN).next_to(gi, DOWN, buff=0.22)
            self.play(Write(check))
            self.play(Indicate(check, color=GREEN), run_time=0.6)

            # Fix the challenge r_i; the claim shrinks to g_i(r_i).
            r = CHALLENGES[i]
            running_claim = G_AT_R[i]
            fold = Text(
                f"fix r{i} = {r}  →  new claim g{i}(r{i}) = {running_claim}",
                font_size=22, color=YELLOW).next_to(check, DOWN, buff=0.22)
            self.play(Write(fold))

            # Fold the cube row: half the remaining terms collapse.
            keep = TERMS_REMAINING[i]
            survivors = VGroup(*cubes[:keep])
            collapsing = VGroup(*cubes[keep:])
            if len(collapsing) > 0:
                self.play(FadeOut(collapsing), run_time=0.5)
            cubes = survivors
            self.wait(0.3)
            self.play(FadeOut(gi), FadeOut(check), FadeOut(fold), run_time=0.4)

        # End at the single evaluation.
        final = Text(
            f"One term left: g(r₁,r₂,r₃) = g(2,3,4) = {FINAL_EVAL}",
            font_size=26, color=GREEN).next_to(cube_caption, DOWN, buff=0.5)
        self.play(FadeIn(final))
        bound = Text(
            "A lying prover survives all rounds with prob ≤ d·v/|F| = 2·3/97 = 6/97.",
            font_size=22, color=YELLOW).next_to(final, DOWN, buff=0.25)
        self.play(Write(bound))
        self.play(Indicate(final, color=GREEN), run_time=0.8)
        self.wait(0.6)
