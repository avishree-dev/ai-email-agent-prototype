import base64
import re
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def decode_base64url(data: str) -> str:
    if not data:
        return ""
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    decoded_bytes = base64.urlsafe_b64decode(data.encode("utf-8"))
    return decoded_bytes.decode("utf-8", errors="ignore")


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def extract_text_from_part(part: dict) -> str:
    mime_type = part.get("mimeType", "")
    body_data = part.get("body", {}).get("data", "")

    if mime_type == "text/plain" and body_data:
        return decode_base64url(body_data)

    if mime_type == "text/html" and body_data:
        html = decode_base64url(body_data)
        return html_to_text(html)

    for child in part.get("parts", []):
        text = extract_text_from_part(child)
        if text.strip():
            return text

    return ""


def clean_body(text):
    # remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # remove long URLs
    text = re.sub(r'http\S+', '', text)

    return text.strip()


def get_recent_emails(limit=10):
    creds = Credentials.from_authorized_user_file("token.json")
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", q='newer_than:1d', maxResults=limit).execute()
    messages = results.get("messages", [])

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "")
        body = clean_body(extract_text_from_part(payload))

        emails.append({
            "subject": subject,
            "sender": sender,
            "body": body[:5000]
        })

    return emails