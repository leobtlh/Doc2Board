# 🎓 Doc2Board

**Doc2Board** est un pipeline local et modulaire qui transforme vos notes de cours (PDF, texte) en vidéos explicatives animées façon "tableau noir", générées par du code Python (Manim) et une voix de synthèse (TTS).

Cette approche *Human-in-the-loop* vous permet d'utiliser l'interface gratuite d'un LLM (comme Gemini) pour générer le script et le code d'animation, puis de faire le rendu vidéo et audio localement, sans aucun frais d'API.

---

## 🛠️ Installation

Ce projet nécessite Python 3 et quelques dépendances système pour faire fonctionner le moteur de rendu vidéo **Manim**.

### 1. Prérequis système (Linux/Ubuntu)
Manim a besoin de `ffmpeg` pour générer les vidéos, et éventuellement de LaTeX pour les formules mathématiques complexes.
```bash
sudo apt update
sudo apt install ffmpeg
# Optionnel (si vous utilisez beaucoup d'équations complexes) :
# sudo apt install texlive texlive-latex-extra texlive-fonts-extra texlive-latex-recommended
```

### 2. Installation du projet
Clonez ce dépôt et créez un environnement virtuel :
```bash
git clone https://github.com/leobtlh/Doc2Board.git
cd Doc2Board

# Créer et activer l'environnement virtuel Python
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances (Manim, edge-tts, etc.)
pip install -r requirements.txt
```
*(Note : Le fichier `requirements.txt` contiendra principalement `manim` et `edge-tts`)*

---

## 🚀 Comment l'utiliser (Le Workflow)

Pour générer une vidéo gratuitement, le processus se fait en 3 étapes simples :

### Étape 1 : Demander à l'IA de générer le cours (Copier-Coller)

Allez sur votre LLM préféré (ex: Google Gemini) et **joignez en pièce jointe votre support de cours** (fichier PDF, document texte, notes).

Ensuite, copiez-collez exactement ce prompt :

> **Prompt Système à copier :**
> 
> "Agis comme un professeur expert dans le domaine du document joint, et comme un développeur Python expert de la librairie d'animation Manim (Community Edition).
> 
> Je t'ai fourni mon support de cours. Ton but est de transformer ce cours en une vidéo explicative animée. Pour cela, tu vas me générer un fichier JSON strict contenant deux choses pour chaque séquence : ce que le professeur va dire à l'oral (le script vocal), et le code Python Manim exact pour dessiner les concepts visuels correspondants au tableau au même moment.
> 
> Contraintes pour le code Manim :
> 1. Utilise Manim CE (`from manim import *`).
> 2. Le code doit être complet, fonctionnel, et ne pas contenir de variables non définies.
> 3. Chaque scène doit hériter de `Scene` et s'appeler `Scene1`, `Scene2`, etc.
> 
> Contraintes pour le JSON :
> Ne renvoie QUE du JSON valide. Pas de texte avant, pas de texte après.
> Voici la structure attendue :
> ```json
> {
>   "lecture_title": "Titre du cours",
>   "scenes": [
>     {
>       "scene_id": 1,
>       "audio_script": "Bonjour et bienvenue dans ce cours. Aujourd'hui, nous allons parler de...",
>       "manim_code": "class Scene1(Scene):\n    def construct(self):\n        title = Text('Titre du cours')\n        self.play(Write(title))\n        self.wait(2)"
>     }
>   ]
> }
> ```
> Analyse mon document et génère le JSON."

### Étape 2 : Sauvegarder le résultat

1. L'IA va vous répondre avec un bloc de code JSON.
2. Copiez ce JSON.
3. Collez-le dans un fichier nommé `course.json` que vous placerez dans le dossier `data/inputs/` de ce projet.

### Étape 3 : Lancer la génération locale

Une fois le fichier `course.json` en place, lancez le script principal (qui va générer l'audio avec TTS, compiler le code Manim, et fusionner le tout) :

```bash
python src/main.py
```

Votre vidéo finale format `.mp4` sera générée et disponible dans le dossier `data/outputs/` !

---
*Projet développé de manière modulaire et agnostique pour permettre l'intégration future d'API payantes (ElevenLabs, Vertex AI) si besoin.*
