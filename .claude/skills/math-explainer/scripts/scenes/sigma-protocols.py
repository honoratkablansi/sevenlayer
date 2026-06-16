from manim import *

P = 2039
Q = 1019
G = 9
X = 321
H = pow(G, X, P)
R = 412
C = 77
T = pow(G, R, P)
S = (R + C * X) % Q
LEFT = pow(G, S, P)
RIGHT = (T * pow(H, C, P)) % P
C2 = 203
S2 = (R + C2 * X) % Q
EXTRACTED_X = ((S - S2) * pow((C - C2) % Q, -1, Q)) % Q

SCENE_VALUES = {
    "p": P,
    "group_order": Q,
    "g": G,
    "x": X,
    "h": H,
    "r": R,
    "c": C,
    "t": T,
    "s": S,
    "left": LEFT,
    "right": RIGHT,
    "verified": LEFT == RIGHT,
    "c2": C2,
    "s2": S2,
    "extracted_x": EXTRACTED_X,
    "special_soundness_ok": EXTRACTED_X == X,
}


class SigmaProtocolsScene(Scene):
    def construct(self):
        title = Text("Sigma protocol: commit, challenge, response", font_size=32).to_edge(UP)
        self.play(Write(title))
        circles = VGroup()
        labels = [f"commit t = {T}", f"challenge c = {C}", f"response s = {S}"]
        cols = [BLUE, PURPLE, GREEN]
        for i, label in enumerate(labels):
            c = Circle(radius=0.72, color=cols[i]).shift(LEFT * 3 + RIGHT * 3 * i)
            txt = Text(label, font_size=19, color=cols[i]).move_to(c)
            circles.add(VGroup(c, txt))
        arrows = VGroup(Arrow(circles[0].get_right(), circles[1].get_left(), buff=0.15),
                        Arrow(circles[1].get_right(), circles[2].get_left(), buff=0.15))
        self.play(FadeIn(circles[0]))
        self.play(Create(arrows[0]), FadeIn(circles[1]))
        self.play(Create(arrows[1]), FadeIn(circles[2]))
        verify = Text("verify g^s = t * h^c", font_size=30, color=YELLOW).shift(DOWN * 1.6)
        values = Text(f"{LEFT} = {RIGHT}", font_size=26, color=YELLOW).next_to(verify, DOWN, buff=0.2)
        self.play(Write(verify), FadeIn(values))
        extract = Text(f"same t with c' = {C2} extracts x = {EXTRACTED_X}", font_size=23, color=RED).to_edge(DOWN)
        self.play(FadeIn(extract))
        self.wait(0.7)
