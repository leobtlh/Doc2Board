import json
import os
import asyncio
from mutagen.mp3 import MP3
from src.tts.generator import TTSManager
from src.video.renderer import VideoRenderer

class Orchestrator:
    def __init__(self):
        self.tts = TTSManager()
        self.renderer = VideoRenderer()

    def get_audio_duration(self, file_path):
        audio = MP3(file_path)
        return audio.info.length

    async def process_lecture(self, json_path):
        # 1. Charger le JSON
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Nettoyage du titre
        lecture_title = data.get("lecture_title", "cours").replace(" ", "_").replace(":", "")

        for scene_data in data["scenes"]:
            sid = scene_data["scene_id"]
            script = scene_data["audio_script"]
            manim_code = scene_data["manim_code"]

            # Chemins absolus pour FFmpeg
            audio_path = os.path.abspath(f"data/temp/audio_{sid}.mp3")
            video_path = os.path.abspath(f"data/temp/videos/temp_scene/480p15/Scene{sid}.mp4")

            # 2. Générer l'audio
            await self.tts.generate_audio(script, audio_path)
            duration = self.get_audio_duration(audio_path)

            # 3. Ajuster le code Manim
            final_code = manim_code.replace("self.wait(2)", f"self.wait({duration})")

            # 4. Rendre la vidéo
            self.renderer.render_scene_from_code(final_code, f"Scene{sid}")

            # 5. Fusionner l'audio et la vidéo
            final_output = os.path.abspath(f"data/outputs/{lecture_title}_scene_{sid}.mp4")
            print(f"🎬 Fusion finale pour la scène {sid}...")
            cmd = f"ffmpeg -y -i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {final_output}"
            os.system(cmd)

        print(f"✨ Toutes les scènes individuelles sont prêtes.")

        # 6. APPEL DE LA CONCATÉNATION
        self.concatenate_scenes(lecture_title, len(data["scenes"]))

    def concatenate_scenes(self, lecture_title, scene_count):
        lecture_title_clean = lecture_title.replace(" ", "_").replace(":", "")
        list_path = "data/temp/concat_list.txt"
        final_output = f"data/outputs/{lecture_title_clean}_FULL.mp4"

        with open(list_path, "w") as f:
            for i in range(1, scene_count + 1):
                # On vérifie si le fichier existe avant de l'ajouter à la liste
                file_path = os.path.abspath(f"data/outputs/{lecture_title_clean}_scene_{i}.mp4")
                if os.path.exists(file_path):
                    f.write(f"file '{file_path}'\n")

        print(f"🔗 Assemblage final des scènes disponibles...")
        # L'option -safe 0 est nécessaire pour les chemins absolus
        cmd = f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {final_output} -loglevel error"
        os.system(cmd)
        print(f"✅ Vidéo finale prête : {final_output}")
