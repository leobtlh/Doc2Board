from manim import *

class Scene30(Scene):
    def construct(self):
        cor_430 = Text('Corollaire 4.30 : Complexité', font_size=32, color=YELLOW)
        self.play(Write(cor_430))
        self.wait(21.72)
        self.play(cor_430.animate.to_edge(UP))
        comp = MathTex('\\mathcal{O}(m^2 n)', font_size=48, color=BLUE)
        comp.next_to(cor_430, DOWN, buff=1)
        self.play(Write(comp))
        self.wait(3)
        box = SurroundingRectangle(comp, color=WHITE)
        self.play(Create(box))
        self.wait(3)