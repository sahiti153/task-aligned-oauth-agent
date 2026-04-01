from langchain.tools import tool
from agent.auth import get_gmail_service
import base64
from email.mime.text import MIMEText

# ---- READ ----
@tool
def read_emails(max_results: int = 5) -> str:
    """Read the most recent emails from the inbox."""
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