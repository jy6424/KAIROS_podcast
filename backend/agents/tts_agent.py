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

    # 저장 경로를 static/audio/ 로 설정
    os.makedirs("static/audio", exist_ok=True)  # 폴더 없으면 생성

    file_name = "podcast_script.mp3"
    file_path = os.path.join("static", "audio", file_name)

    with open(file_path, "wb") as f:
        f.write(audio_response.content)

    # 프론트엔드에서 접근 가능한 URL로 변환
    audio_url = f"/static/audio/{file_name}"

    return {
        "audio_file": file_path,
        "audio_url": audio_url
    }