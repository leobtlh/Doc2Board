import os
import subprocess

class VideoRenderer:
    """
    Gère le rendu des scènes Manim.
    """
    def __init__(self, output_dir="data/outputs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def render_scene_from_code(self, code_string, scene_name):
        """
        Prend une chaîne de caractères (code python) et la transforme en vidéo.
        """
        # Injection de l'import si manquant
        if "from manim import *" not in code_string:
            code_string = "from manim import *\n\n" + code_string

        # 1. Sauvegarder le code dans un fichier temporaire
        temp_file = "temp_scene.py"
        with open(temp_file, "w") as f:
            f.write(code_string)

        # 2. Appeler Manim en ligne de commande pour le rendu
        # -ql : Qualité basse (rapide pour les tests)
        # --media_dir : Dossier de sortie
        print(f"🎬 Rendu de la scène {scene_name} en cours...")
        try:
            subprocess.run([
                "manim", "-ql", temp_file, scene_name,
                "--media_dir", "./data/temp"
            ], check=True)
            print(f"✅ Scène {scene_name} rendue avec succès.")
        except Exception as e:
            print(f"❌ Erreur lors du rendu Manim : {e}")

if __name__ == "__main__":
    # Petit test : Un cercle qui se transforme en carré
    test_code = """
from manim import *

class TestScene(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)

        self.play(Create(circle))
        self.wait(1)
        self.play(ReplacementTransform(circle, square))
        self.wait(1)
"""
    renderer = VideoRenderer()
    renderer.render_scene_from_code(test_code, "TestScene")
