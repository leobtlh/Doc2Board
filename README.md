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

Allez sur votre LLM préféré (ex: Google Gemini) et **joignez en pièce jointe votre support de cours** (fichier PDF, document texte, notes). Pour une précision maximale, traitez votre cours chapitre par chapitre (ex: 4 à 5 pages à la fois).

Ensuite, copiez-collez exactement ce prompt :

> **Prompt Système à copier :**
> 
> "Agis comme un professeur d'université ultra-rigoureux dans le domaine du document joint, et comme un développeur Python expert de la librairie d'animation Manim (Community Edition).
> 
> Ton but est de transformer ce cours en une vidéo explicative animée de niveau académique. Tu vas générer un fichier JSON strict contenant le script vocal et le code Python Manim pour chaque séquence.
> 
> **🎓 EXIGENCES DE PRÉCISION ABSOLUE (CONTENU) :**
> 1. **Zéro perte d'information :** Ne résume absolument rien. Tout le contenu théorique du document doit être couvert.
> 2. **Noms et Numéros :** Chaque théorème, lemme, corollaire ou définition doit apparaître à l'écran et dans l'audio avec son **numéro exact** et son **titre exact** tels qu'écrits dans le texte source (ex: 'Théorème 4.20', 'Définition 2.1').
> 3. **Preuves pas-à-pas :** Les démonstrations mathématiques et les algorithmes doivent être décomposés ligne par ligne. N'affiche pas un gros bloc de texte d'un coup. Fais apparaître chaque étape logique l'une après l'autre.
> 4. **Pédagogie visuelle :** Utilise des `self.wait(2)` ou `self.wait(3)` entre chaque `self.play()` dans ton code Manim pour laisser le temps à l'audio d'expliquer l'étape en cours avant de passer à la ligne suivante. Crée autant de scènes que nécessaire pour ne pas surcharger le tableau noir.
> 
> **⚠️ CONTRAINTES CRITIQUES DE FORMATTAGE :**
> 1. **Guillemets :** À l'intérieur du champ `manim_code`, utilise **UNIQUEMENT des guillemets simples (`'`)** pour les chaînes de caractères (ex: `Text('Bonjour')`). Ne jamais utiliser de guillemets doubles (`"`) au sein du code car cela brise la structure du JSON.
> 2. **LaTeX :** Pour les formules mathématiques (`MathTex`), utilise des **simples backslashes échappés (`\\`)** pour les commandes (ex: `\\sum` ou `\\alpha`).
> 3. **Indentation :** Utilise `\n` pour les retours à la ligne dans le code Python.
> 
> **Contraintes Manim :**
> - Utilise Manim CE (`from manim import *`).
> - Chaque scène doit hériter de `Scene` et s'appeler `Scene1`, `Scene2`, etc.
> - Termine toujours chaque scène par `self.wait(2)`.
> 
> **Structure attendue :**
> ```json
> {
>   "lecture_title": "Titre complet du chapitre",
>   "scenes": [
>     {
>       "scene_id": 1,
>       "audio_script": "Texte très détaillé lu par le professeur, expliquant chaque étape de la démonstration à venir...",
>       "manim_code": "class Scene1(Scene):\n    def construct(self):\n        ..."
>     }
>   ]
> }
> ```
> Analyse mon document avec la plus grande rigueur mathématique et génère le JSON."

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
