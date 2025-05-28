from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import OpenAIEmbeddings
import openai
from dotenv import load_dotenv
import os
from datetime import datetime
from langchain.schema import Document


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

def answer_from_vectorstore(state):
    user_query = state["user_query"]
    docs = vector_store.similarity_search(user_query, k=5, namespace="lecturedata")
    content = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"다음 문서를 참고하여 사용자의 질문에 답해주세요:\n\n{content}\n\n질문: {user_query}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    answer = response.choices[0].message.content

    # vectorstore에 질문/답변 저장
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    qa_doc = Document(
        page_content=f"Q: {user_query}\nA: {answer}",
        metadata={"source": "userqa", "timestamp": now}
    )
    vector_store.add_documents([qa_doc], namespace="userqna")
    return {"answer": answer} 