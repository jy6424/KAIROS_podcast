from fastapi import FastAPI, UploadFile, File, Request, Query, Form
from fastapi.responses import JSONResponse
import tempfile
import os
from agents.pdf_read_agent import summarize_and_store
from agents.script_maker_agent import generate_script
from agents.tts_agent import synthesize_tts
from langfuse import Langfuse
from langfuse.decorators import observe
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv
import os


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST=os.getenv("LANGFUSE_HOST")

load_dotenv()

app = FastAPI()


@app.post("/process-pdf")
@observe(name="process_pdf")
async def process_pdf(
    file: UploadFile = File(...),
    lecture_name: str = Form(None)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        temp_pdf_path = tmp.name

    file_name = file.filename

    try:
        result = summarize_and_store(
            pdf_path=temp_pdf_path,
            lecture_name=lecture_name,
            poppler_path=os.getenv("POPPLER_PATH"),
            pdf_name=file_name
        )
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(temp_pdf_path)

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

app = FastAPI()

@app.post("/script-to-tts")
@observe(name="script_to_tts")
async def script_to_tts(init: str = Query(..., description="초기 스크립트 생성 입력값")):
    try:
        result = generate_script({"init": init})
        script = result["script"]
        tts_url = synthesize_tts(result)

        return JSONResponse(content={
            "init": init,
            "script": script,
            "audio_file": tts_url,
            "user_query": None,
            "answer": None
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})