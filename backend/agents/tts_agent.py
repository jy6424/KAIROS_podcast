import openai
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# generate TTS Agent
def synthesize_tts(state):
    script = state["script"]
    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=script
    )
    file_name = "podcast_script.mp3"
    with open(file_name, "wb") as f:
        f.write(audio_response.content)
    return {"audio_file": file_name}