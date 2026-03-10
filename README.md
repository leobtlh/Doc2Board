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

Allez sur votre LLM préféré (ex: Google Gemini) et **joignez en pièce jointe votre support de cours** (fichier PDF, document texte, notes). Pour une précision maximale, traitez votre cours chapitre par chapitre (ex: 3 à 4 pages à la fois).

Ensuite, copiez-collez exactement ce prompt :

> **Prompt Système à copier :**
> 
> "Agis comme un professeur d'université ultra-rigoureux et comme un développeur Python expert en Manim (Community Edition).
> 
> Ton but est de transformer ce cours en une vidéo explicative animée. Tu vas générer un fichier JSON strict contenant le script vocal et le code Python Manim.
> 
> **🎓 EXIGENCES DE GRANULARITÉ ET SYNCHRONISATION (TRÈS IMPORTANT) :**
> 1. **Micro-scènes (Granularité Extrême) :** Découpe le cours en un nombre MASSIF de scènes (génère-en 50, 100 ou 150 si nécessaire). Ne fais aucun résumé. Chaque scène ne doit contenir qu'UNE seule action visuelle et UN très court texte audio (1 à 2 phrases maximum).
> 2. **Le Visuel AVANT l'audio :** L'animation doit afficher le concept avant ou pendant que tu en parles. Pour cela, utilise des animations rapides dans Manim (ex: `self.play(Write(obj), run_time=0.5)` ou `FadeIn`).
> 3. **Qualité Visuelle Maximale :** Ne te contente pas d'écrire du texte à l'écran. Dessine de VRAIS graphes avec des VRAIS nœuds (`Dot`), arêtes (`Arrow`), couleurs, et labels mathématiques. Reproduis les illustrations du PDF avec une précision maniaque.
> 
> **🗣️ EXIGENCES POUR LE SCRIPT AUDIO (`audio_script`) :**
> 1. **Zéro Citation :** NE METS JAMAIS de balises du type `` ou `` dans le script audio. Supprime-les totalement de ta narration.
> 2. **Prononciation Phonétique Naturelle :** Ne lis pas le code LaTeX comme un robot. Écris le texte exactement comme il doit être prononcé oralement par un professeur humain.
>    - Au lieu de `A_i` ou `A_1`, écris `A i` ou `A 1`.
>    - Au lieu de `O(m^2 n)`, écris `Grand O de m carré n`.
>    - Au lieu de `f(v,w)`, écris `f de v et w`.
>    - Au lieu de `\le`, écris `inférieur ou égal`.
> 
> **⚠️ CONTRAINTES CRITIQUES DE FORMATTAGE JSON & MANIM :**
> 1. **Guillemets :** Dans `manim_code`, utilise UNIQUEMENT des guillemets simples (`'`) pour les chaînes (ex: `Text('Texte')`). Les guillemets doubles (`"`) détruisent le JSON.
> 2. **LaTeX :** Pour `MathTex`, utilise des doubles backslashes (`\\\\`) (ex: `\\\\sum`, `\\\\le`).
> 3. **Indentation :** Utilise `\n` pour les retours à la ligne du code Python.
> 4. **Code Manim :** Utilise `from manim import *`. Hérite de `Scene`. Appelle les classes `Scene1`, `Scene2`, etc.
> 5. **Terminaison :** Termine EXACTEMENT chaque scène par la ligne `self.wait(2)`. Mon script Python cherche cette ligne précise pour la remplacer par la durée de l'audio, c'est vital pour la synchronisation.
> 
> **Structure attendue :**
> ```json
> {
>   "lecture_title": "Titre du cours",
>   "scenes": [
>     {
>       "scene_id": 1,
>       "audio_script": "Considérons des ports de départ A 1 à A p.",
>       "manim_code": "class Scene1(Scene):\n    def construct(self):\n        ..."
>     }
>   ]
> }
> ```
> Analyse mon document et génère le JSON en appliquant cette granularité extrême."

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
