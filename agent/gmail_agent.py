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

def run_agent(task: str, verbose: bool = False):
    """Run the Gmail agent with a given task string."""
    try:
        result = agent.invoke(
            {"messages": [HumanMessage(content=task)]},
            config={"callbacks": None}
        )
        if verbose:
            print("\n--- Agent Message Chain ---")
            for msg in result["messages"]:
                print(f"[{msg.__class__.__name__}]: {msg.content[:200]}")
            print("--- End Message Chain ---\n")
        return result
    except Exception as e:
        error_msg = str(e)
        print(f"⚠️  Agent error: {error_msg[:200]}")
        # Return partial result structure so tool calls can still be inspected
        return {"messages": [], "error": error_msg}


def get_agent_response(result) -> str:
    """Extract final text response from agent result."""
    if result is None:
        return ""
    if "messages" not in result or not result["messages"]:
        return result.get("error", "")
    return result["messages"][-1].content


def get_tool_calls(result) -> list:
    """Extract all tool call outputs from agent result."""
    if result is None:
        return []
    tool_outputs = []
    for msg in result["messages"]:
        if msg.__class__.__name__ == "ToolMessage":
            tool_outputs.append(msg.content)
    return tool_outputs


if __name__ == "__main__":
    print("🤖 Running Gmail agent...")
    output = run_agent("Read my 3 most recent emails and summarize them.", verbose=True)
    print("\n✅ Agent output:", output) 