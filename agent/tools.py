from langchain.tools import tool
from agent.auth import get_gmail_service
import base64
from email.mime.text import MIMEText
from agent.intent_schema import DeclaredIntent
from agent.policy_layer import check_tool_call

# ---- READ ----
@tool
def read_emails(max_results: int = 5) -> str:
    """Read the most recent emails from the inbox."""
    decision = check_tool_call(
        CURRENT_INTENT,
        "read_emails",
        {"max_results": max_results}
    )

    if not decision.allowed:
        return f"🚫 POLICY BLOCKED: {decision.reason}"
    
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return "No emails found."

    output = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        snippet = msg_data.get("snippet", "")

        output.append(f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n")

    return "\n---\n".join(output)


# ---- SEARCH ----
@tool
def search_emails(query: str) -> str:
    """Search emails using a Gmail search query string (e.g. 'from:test@gmail.com')."""
    decision = check_tool_call(
        CURRENT_INTENT,
        "search_emails",
        {"query": query}
    )

    if not decision.allowed:
        return f"🚫 POLICY BLOCKED: {decision.reason}"
    
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=5
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return f"No emails found for query: {query}"

    output = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        snippet = msg_data.get("snippet", "")

        output.append(f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n")

    return "\n---\n".join(output)


# ---- SEND ----
@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email. Args: to (recipient email), subject (email subject), body (email body text)."""
    decision = check_tool_call(
        CURRENT_INTENT,
        "send_email",
        {"to": to, "subject": subject, "body": body}
    )

    if not decision.allowed:
        return f"🚫 POLICY BLOCKED: {decision.reason}"
    
    service = get_gmail_service()

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = {"raw": raw}

    result = service.users().messages().send(
        userId="me",
        body=send_message
    ).execute()

    return f"✅ Email sent successfully! Message ID: {result['id']}"

# ----- INTENT -----
CURRENT_INTENT = DeclaredIntent(
    task="Read and summarize emails only",
    allowed_tools=["read_emails", "search_emails"],
    allowed_recipients=[],
    allowed_queries=[],
    max_emails=5
)