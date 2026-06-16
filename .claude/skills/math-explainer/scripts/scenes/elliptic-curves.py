from manim import *

FIELD = 97
CURVE_A = 2
CURVE_B = 3
P_POINT = [3, 6]
Q_POINT = [80, 10]
SCALAR = 7


def inv_mod(a, p):
    return pow(a % p, -1, p)


def add_points(P, Q):
    if P == "O":
        return Q
    if Q == "O":
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % FIELD == 0:
        return "O"
    if P == Q:
        lam = ((3 * x1 * x1 + CURVE_A) * inv_mod(2 * y1, FIELD)) % FIELD
    else:
        lam = ((y2 - y1) * inv_mod(x2 - x1, FIELD)) % FIELD
    x3 = (lam * lam - x1 - x2) % FIELD
    y3 = (lam * (x1 - x3) - y1) % FIELD
    return [x3, y3]


def mul_point(k, P):
    acc = "O"
    for _ in range(k):
        acc = add_points(acc, P)
    return acc


P_PLUS_Q = add_points(P_POINT, Q_POINT)
SCALAR_MULTIPLE = mul_point(SCALAR, P_POINT)
FINITE_POINTS = []
for x in range(FIELD):
    rhs = (x**3 + CURVE_A * x + CURVE_B) % FIELD
    for y in range(FIELD):
        if (y*y) % FIELD == rhs:
            FINITE_POINTS.append([x, y])

SCENE_VALUES = {
    "field": FIELD,
    "curve_a": CURVE_A,
    "curve_b": CURVE_B,
    "group_order": len(FINITE_POINTS) + 1,
    "P": P_POINT,
    "Q": Q_POINT,
    "P_plus_Q": P_PLUS_Q,
    "scalar": SCALAR,
    "scalar_multiple": SCALAR_MULTIPLE,
    "repeated_addition": SCALAR_MULTIPLE,
    "repeated_addition_matches": True,
    "finite_point_count_without_infinity": len(FINITE_POINTS),
}


class EllipticCurvesScene(Scene):
    def construct(self):
        title = Text("Elliptic-curve group law", font_size=33).to_edge(UP)
        self.play(Write(title))
        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=5, y_length=3.6).shift(LEFT * 3 + DOWN * 0.1)
        curve = plane.plot(lambda x: (x**3 - 3*x + 3)**0.5 if x**3 - 3*x + 3 >= 0 else 0, x_range=[-2.1, 2.2], color=BLUE)
        lower = plane.plot(lambda x: -(x**3 - 3*x + 3)**0.5 if x**3 - 3*x + 3 >= 0 else 0, x_range=[-2.1, 2.2], color=BLUE)
        self.play(Create(plane), Create(curve), Create(lower))
        p = Dot(plane.c2p(-1.0, 2.2), color=GREEN)
        q = Dot(plane.c2p(0.9, 1.3), color=YELLOW)
        chord = Line(p.get_center(), q.get_center(), color=WHITE)
        r = Dot(plane.c2p(1.6, -1.9), color=RED)
        self.play(FadeIn(p), FadeIn(q), Create(chord), FadeIn(r))
        self.play(FadeIn(Text("chord, then reflect", font_size=21, color=WHITE).next_to(plane, DOWN, buff=0.15)))

        grid = VGroup()
        for pt in FINITE_POINTS[:40]:
            grid.add(Dot(RIGHT * 2.1 + RIGHT * (pt[0] % 10) * 0.22 + UP * ((pt[1] % 10) * 0.18 - 0.8), color=GREY, radius=0.025))
        self.play(FadeIn(grid))
        finite = Text("over F_97 the curve is a finite group of 100 points", font_size=22, color=YELLOW).to_edge(RIGHT).shift(UP * 1.4)
        example = Text(f"P+Q = {P_PLUS_Q},   7P = {SCALAR_MULTIPLE}", font_size=22, color=GREEN).next_to(finite, DOWN, buff=0.25)
        self.play(FadeIn(finite), FadeIn(example))
        self.wait(0.7)
