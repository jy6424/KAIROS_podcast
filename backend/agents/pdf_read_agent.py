import os
from dotenv import load_dotenv
import openai
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime
from langchain.schema import Document
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

openai.api_key = OPENAI_API_KEY

# ✅ 이미지 → base64 변환
def encode_image_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ✅ Vision API 호출
def ask_gpt4_vision(base64_image: str, prompt: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]
        }],
        max_tokens=1000
    )
    return response.choices[0].message.content

# ✅ PDF 요약 및 벡터스토어 저장 함수
def summarize_and_store(pdf_path: str, pdf_name, lecture_name, poppler_path: str = None):
    date = datetime.today().strftime("%Y-%m-%d")
    pdf_name = pdf_name or "Unknown Lecture"
    documents = []

    images = convert_from_path(pdf_path, dpi=150, poppler_path=poppler_path)
    for i, image in enumerate(images):
        base64_image = encode_image_to_base64(image)
        summary = ask_gpt4_vision(base64_image, prompt="이 페이지의 주요 내용을 요약해줘")
        documents.append(Document(
            page_content=summary,
            metadata={
                "file_name": pdf_name,
                "lecture_name": lecture_name,
                "upload_date": date,
                "page": i + 1
            }
        ))

    # Pinecone + 임베딩 설정
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("kairos-podcast")
    vector_store = PineconeVectorStore(index=index, embedding=embeddings, namespace="lecturedata")

    # 문서 분할 후 저장
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)
    vector_store.add_documents(split_docs)

    return {"status": "done", "upload_date": date, "lecture_name": lecture_name, "file_name": pdf_name, "pages": len(split_docs)}
