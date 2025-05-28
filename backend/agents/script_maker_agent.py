from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

embeddings = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY,
    model="text-embedding-3-small"
)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("kairos-podcast")

vector_store = PineconeVectorStore(
    index=index, 
    embedding=embeddings,
    namespace="lecturedata"
)

#read prompt
def read_prompt(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

#if not related QA found, return empty list
def get_qa_docs_with_fallback(query, k, namespace, score_threshold=0.01):
    try:
        docs_and_scores = vector_store.similarity_search_with_score(
            query, k=k, namespace=namespace
        )
        filtered_docs = [
            doc for doc, score in docs_and_scores if score >= score_threshold
        ]

        if filtered_docs:
            return filtered_docs
        else:
            return []

    except Exception as e:
        print("에러 발생:", e)
        return []
    

#generate script Agent

def generate_script(state):

    # 1. Retrieve documents
    query= state["init"]
    lecture_docs = vector_store.similarity_search(query, k=5, namespace="lecturedata")
    qa_docs = get_qa_docs_with_fallback(query, k=1, namespace="userqna")
    lecture = [doc.page_content for doc in lecture_docs]
    qa = [doc.page_content for doc in qa_docs]

    # 2. Create user and system prompts
    user_prompt = f"다음은 참고할 문서 내용입니다:\n\n{lecture}\n\n{qa} \n\n이 내용을 바탕으로 스크립트를 작성해주세요." 
    system_prompt = read_prompt("summary_prompt.txt")


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return {"script": response.choices[0].message.content, "query": query, "lecture_docs": lecture, "qa_docs": qa}
