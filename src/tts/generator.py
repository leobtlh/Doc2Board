import asyncio
import edge_tts

class TTSManager:
    """
    Gère la génération de la voix.
    Actuellement configuré pour Edge-TTS (gratuit).
    Peut être étendu pour ElevenLabs plus tard.
    """
    def __init__(self, voice="fr-FR-DeniseNeural"):
        self.voice = voice

    async def generate_audio(self, text, output_path):
        """
        Transforme un texte en fichier MP3.
        """
        print(f"🎙️  Génération de l'audio : {text[:30]}...")
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        print(f"✅ Audio sauvegardé : {output_path}")

# Petit test rapide si on lance le script directement
if __name__ == "__main__":
    test_text = "Bienvenue dans ce cours sur la théorie des graphes. Nous allons voir les bases ensemble."
    manager = TTSManager()
    asyncio.run(manager.generate_audio(test_text, "test_audio.mp3"))
