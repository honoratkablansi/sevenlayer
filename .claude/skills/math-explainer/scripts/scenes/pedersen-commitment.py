"""manim scene for the Pedersen commitment (Ch 11).

Animates HIDING and BINDING of Com(m, r) = g^m * h^r in a concrete prime-order
group: the order-q subgroup of (Z/pZ)* with p = 2039, q = 1019, g = 9, h = 726.

- HIDING: hold the message m = 42 fixed and sweep the randomness r. The committed
  element walks around the group's "clock", landing on a different point for every r
  -- over all q choices it is uniform over the whole subgroup, so C alone hides m.
- BINDING: for a FIXED (m, r) the commitment is one fixed point (C = 71). A second
  opening to a different message would force you to know log_g(h) -- the discrete log.

NO LaTeX: the manim conda env has no LaTeX, so this scene uses only Pango Text /
MarkupText and geometric mobjects (never Tex / MathTex). Unicode renders fine.

Displayed computed values are kept in SCENE_VALUES so Stage 4 can validate them
against the Sage manifest (p, q, g, h, m, r, commitment) with no drift.

Render a clip with: render_scene(Path('scripts/scenes/pedersen-commitment.py'),
'PedersenCommitment', Path('assets/manim-pedersen-commitment'), still=False).
"""
import math

from manim import (
    Scene, Text, VGroup, Dot, Circle, Line, Create, FadeIn, FadeOut, Write, Flash,
    Indicate, MoveAlongPath, Arc, BLUE, RED, YELLOW, GREEN, PURPLE, GREY, WHITE,
    UP, DOWN, LEFT, RIGHT, ORIGIN,
)

# --- Math, correct-by-construction (mirrors scripts/recipes/pedersen-commitment.sage) ---
P = 2039                 # safe prime, p = 2q + 1
Q = 1019                 # prime subgroup order  |<g>| = q
G = 9                    # generator g  (a quadratic residue mod p)
H = 726                  # second generator h = g^a, a = 571 secret
M = 42                   # committed message
R = 800                  # blinding randomness
A_SECRET = 571           # log_g(h); binding rests on this being unknown


def _pow(base, exp):     # base^exp mod p, pure Python
    return pow(base, exp, P)


def _commit(msg, rand):  # Com(msg, rand) = g^msg * h^rand mod p
    return (_pow(G, msg) * _pow(H, rand)) % P


COMMITMENT = _commit(M, R)                       # == 71
# The hiding orbit: fixed message M, several randomness values -> distinct elements.
R_SAMPLES = [0, 1, 800, 17, 999]
HIDING_ORBIT = [_commit(M, rr) for rr in R_SAMPLES]
HIDING_DISTINCT = len(set(HIDING_ORBIT)) == len(HIDING_ORBIT)

# Values this scene asserts on screen; Stage 4 checks these against the Sage manifest.
SCENE_VALUES = {
    "p": P,
    "group_order": Q,
    "g": G,
    "h": H,
    "m": M,
    "r": R,
    "commitment": COMMITMENT,
    "hiding_distinct": HIDING_DISTINCT,
}

# --- Geometry: place a group element on a unit "clock" by its discrete log base g. ---
# A small precomputed dlog table (g = 9 generates the order-1019 subgroup mod 2039).
_DLOG = {}
_acc = 1
for _k in range(Q):
    _DLOG.setdefault(_acc, _k)
    _acc = (_acc * G) % P


def _angle(elt):                       # radians around the ring, by dlog base g
    return 2 * math.pi * (_DLOG[elt] / Q)


def _pos(elt, radius=2.2):
    th = _angle(elt)
    return [radius * math.cos(th), radius * math.sin(th), 0.0]


class PedersenCommitment(Scene):
    def construct(self):
        title = Text("Pedersen commitment: hiding and binding",
                     font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))

        setup = Text("Com(m, r) = g^m · h^r   in the order-1019 subgroup mod 2039",
                     font_size=22, color=GREY).next_to(title, DOWN, buff=0.22)
        self.play(FadeIn(setup))

        # The group drawn as a ring (a prime-order cyclic group = a "clock").
        ring = Circle(radius=2.2, color=GREY).shift(DOWN * 0.4)
        ring_center = ring.get_center()

        def at(elt, radius=2.2):
            base = _pos(elt, radius)
            return [base[0] + ring_center[0], base[1] + ring_center[1], 0.0]

        self.play(Create(ring))

        # Mark the two public generators g and h.
        g_dot = Dot(at(G), color=GREEN, radius=0.07)
        h_dot = Dot(at(H), color=PURPLE, radius=0.07)
        g_lab = Text("g = 9", font_size=20, color=GREEN).next_to(g_dot, UP, buff=0.12)
        h_lab = Text("h = 726", font_size=20, color=PURPLE).next_to(h_dot, DOWN, buff=0.12)
        self.play(FadeIn(g_dot), FadeIn(h_dot), FadeIn(g_lab), FadeIn(h_lab))

        # The legend of fixed parameters.
        params = VGroup(
            Text("m = 42  (message, fixed)", font_size=20, color=YELLOW),
            Text("r = 800  (randomness, secret)", font_size=20, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        params.to_corner(LEFT + DOWN)
        self.play(FadeIn(params))

        # --- HIDING: hold m fixed, sweep r; the commitment walks the ring. ---
        hiding_msg = Text("Hiding: change r  ->  C moves all around the group",
                          font_size=24, color=BLUE).next_to(setup, DOWN, buff=0.18)
        self.play(FadeIn(hiding_msg))

        mover = Dot(at(HIDING_ORBIT[0]), color=BLUE, radius=0.10)
        self.play(FadeIn(mover))
        ghosts = VGroup()
        for elt in HIDING_ORBIT:
            target = at(elt)
            self.play(mover.animate.move_to(target), run_time=0.5)
            ghost = Dot(target, color=BLUE, radius=0.06).set_opacity(0.45)
            ghosts.add(ghost)
            self.add(ghost)
            self.play(Flash(mover, color=BLUE, line_length=0.18), run_time=0.25)
        hiding_note = Text("Over all 1019 values of r, C is uniform — C alone hides m.",
                           font_size=20, color=BLUE).next_to(ring, DOWN, buff=0.25)
        self.play(FadeIn(hiding_note))
        self.wait(0.4)

        # --- BINDING: pin one (m, r); the commitment is ONE fixed point C = 71. ---
        self.play(FadeOut(ghosts), FadeOut(hiding_note), FadeOut(hiding_msg))
        binding_msg = Text("Binding: fix (m, r)  ->  exactly one C = 71",
                           font_size=24, color=RED).next_to(setup, DOWN, buff=0.18)
        self.play(FadeIn(binding_msg))
        c_pos = at(COMMITMENT)
        self.play(mover.animate.move_to(c_pos), run_time=0.6)
        c_dot = Dot(c_pos, color=RED, radius=0.11)
        c_lab = Text("C = 71", font_size=22, color=RED).next_to(c_dot, RIGHT, buff=0.12)
        self.play(FadeIn(c_dot), FadeOut(mover), Write(c_lab),
                  Flash(c_dot, color=RED, line_length=0.3))
        self.play(Indicate(c_dot, color=RED), run_time=0.8)

        binding_note = Text(
            "A second opening with a different m would reveal log_g(h) — the discrete log.",
            font_size=20, color=RED).next_to(ring, DOWN, buff=0.25)
        self.play(FadeIn(binding_note))
        self.wait(0.7)
