from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os

# Scopes define what actions the Gmail agent is allowed to perform
# Keep this minimal - only what the agent actually needs
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify"  # needed for drafts
]

def get_gmail_service():
    creds = None
    token_path = "credentials/token.pickle"
    secret_path = "credentials/client_secret.json"

    # Load existing token if available
    if os.path.exists(token_path):
        with open(token_path, "rb") as f:
            creds = pickle.load(f)

    # If no valid token, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh silently if token is just expired
            creds.refresh(Request())
        else:
            # Full OAuth flow - opens browser for user authorization
            flow = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(token_path, "wb") as f:
            pickle.dump(creds, f)

    return build("gmail", "v1", credentials=creds)


if __name__ == "__main__":
    service = get_gmail_service()
    results = service.users().labels().list(userId="me").execute()
    labels = [l["name"] for l in results.get("labels", [])]
    print("✅ OAuth token flow working!")
    print("📬 Gmail labels found:", labels)