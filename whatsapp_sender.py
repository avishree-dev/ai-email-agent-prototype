import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_ACCOUNT_AUTH")
from_whatsapp = os.getenv("TWILIO_WHATSAPP_FROM")
to_whatsapp = os.getenv("TWILIO_WHATSAPP_TO")

client = Client(account_sid, auth_token)

def send_whatsapp(message):
    client.messages.create(
        body=message,
        from_=from_whatsapp,
        to=to_whatsapp
    )
def split_message(text, max_len=1500):
    chunks = []
    current = ""

    for line in text.split("\n"):
        # +1 for newline that will be added back
        if len(current) + len(line) + 1 > max_len:
            chunks.append(current.strip())
            current = line + "\n"
        else:
            current += line + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks