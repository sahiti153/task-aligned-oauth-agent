from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id=os.getenv("HF_MODEL"),
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    task="conversational",
    max_new_tokens=256
)

chat = ChatHuggingFace(llm=llm)

response = chat.invoke([HumanMessage(content="Say 'OAuth agent ready' and nothing else.")])
print("✅ LLM response:", response.content)