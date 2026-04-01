import os
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from agent.tools import read_emails, search_emails, send_email
from dotenv import load_dotenv

load_dotenv()

# Load tools
tools = [read_emails, search_emails, send_email]

# Load LLM via Groq (free, fast, supports tool calling)
chat_llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# Build agent
agent = create_agent(
    model=chat_llm,
    tools=tools,
    system_prompt="You are a Gmail assistant. Help users manage their email using the available tools."
)

def run_agent(task: str) -> str:
    """Run the Gmail agent with a given task string."""
    result = agent.invoke({
        "messages": [HumanMessage(content=task)]
    })
    return result["messages"][-1].content


if __name__ == "__main__":
    print("🤖 Running Gmail agent...")
    output = run_agent("Read my 3 most recent emails and summarize them.")
    print("\n✅ Agent output:", output)