from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph
from langchain.schema import Document
from agents.script_maker_agent import generate_script
from agents.tts_agent import synthesize_tts
from agents.qna_agent import answer_from_vectorstore

from typing import TypedDict, Optional
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")

#initialize Langfuse
langfuse_handler = CallbackHandler(
  secret_key=LANGFUSE_SECRET_KEY,
  public_key=LANGFUSE_PUBLIC_KEY,
  host="https://us.cloud.langfuse.com"
)

#define chat state
class ChatState(TypedDict):
    init: str
    lecture_docs: Optional[str]
    script: Optional[str]
    audio_file: Optional[str]
    qa_docs: Optional[str]
    answer: Optional[str]


#agent node definition

def script_generation(state: ChatState) -> ChatState:
    generated_script = generate_script(state)
    return {**state, "script": generated_script["script"], "lecture_docs": generated_script["lecture_docs"], "qa_docs": generated_script["qa_docs"]}

def tts_generation(state: ChatState) -> ChatState:
    tts_result = synthesize_tts(state)
    return {**state, "audio_file": tts_result["audio_file"]}

def save_to_vector_store(state: ChatState) -> None:
    user_qna_data = answer_from_vectorstore(state)
    return {**state, "answer": user_qna_data["answer"]}


#connect workflow
workflow = StateGraph(ChatState)

workflow.add_node("Script Generation", RunnableLambda(script_generation))
workflow.add_node("TTS Generation", RunnableLambda(tts_generation))
# workflow.add_node("User QnA", RunnableLambda(save_to_vector_store))

workflow.set_entry_point("Script Generation")
workflow.add_edge("Script Generation", "TTS Generation")
# workflow.add_edge("TTS Generation", "User QnA")
workflow.set_finish_point("TTS Generation")

graph = workflow.compile().with_config({"callbacks": [langfuse_handler]})


# # Define the initial state for the orchestration agent
# state = {
#     "init": "강의 내용을 요약한 팟캐스트를 만들어줘",
#     "user_query" : None,
#     "docs": None,
#     "script": None,
#     "audio_file": None,
#     "answer": None
# }


# result = graph.invoke(state)

# print(result)