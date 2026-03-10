from manim import *

class Scene4(Scene):
    def construct(self):
        alg_title = Text('Algorithme d\'Edmonds-Karp', font_size=36).to_edge(UP)
        step1 = Text('1. Initialiser le flot à 0', font_size=28).shift(UP)
        step2 = Text('2. Trouver le chemin le plus court (BFS)', font_size=28)
        step3 = Text('3. Augmenter le flot et répéter', font_size=28).shift(DOWN)
        
        complexity = MathTex('\\mathcal{O}(m^2 n)', color=GREEN).next_to(step3, DOWN, buff=0.8)
        
        self.play(Write(alg_title))
        self.play(Write(step1))
        self.wait(0.5)
        self.play(Write(step2))
        self.wait(0.5)
        self.play(Write(step3))
        self.wait(1)
        self.play(Indicate(complexity))
        self.play(Write(complexity))
        self.wait(21.408)