import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.core.orchestrator import Orchestrator

async def main():
    # On cherche course.json en priorité, sinon test.json
    json_input = "data/inputs/course.json"
    if not os.path.exists(json_input):
        json_input = "data/inputs/test.json"

    if not os.path.exists(json_input):
        print(f"❌ Erreur : Aucun fichier JSON trouvé dans data/inputs/ (attendu: course.json)")
        return

    print(f"🚀 Démarrage de Doc2Board avec : {json_input}")
    orchestrator = Orchestrator()
    await orchestrator.process_lecture(json_input)

if __name__ == "__main__":
    asyncio.run(main())
