from fastapi import FastAPI, UploadFile, File, Request, Query, Form
from fastapi.responses import JSONResponse
import tempfile
import os
from agents.pdf_read_agent import summarize_and_store
from agents.qna_agent import answer_from_vectorstore
from langfuse import Langfuse
from langfuse.decorators import observe
from dotenv import load_dotenv
from agents.orchestration_agent import graph
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

@app.post("/generate-content")
@observe(name="generate_content")
async def generate_content(init: str = Query(...)):
    try:
        state = {
            "init": init,
            "user_query": None,
            "docs": None,
            "script": None,
            "audio_file": None,
            "answer": None
        }
        result = graph.invoke(state)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    

@app.post("/user-query")
@observe(name="user_query")
async def user_query(
    query: str = Query(...)
):
    try:
        state = {
            "init": None,
            "user_query": query,
            "docs": None,
            "script": None,
            "audio_file": None,
            "answer": None
        }
        result = answer_from_vectorstore(state)
        if not result:
            return JSONResponse(content={"answer": "관련된 답변을 찾을 수 없습니다."})
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})