import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_email(subject, body):
    text = (subject + " " + body).lower()
    if any(k in text for k in ["otp", "verification code", "one time password", "security code"]):
        return {
            "category": "important",
            "summary": "Contains a verification or OTP code."
        }

    if any(k in text for k in ["google meet", "meet.google.com", "zoom", "teams meeting", "meeting invite"]):
        return {
            "category": "important",
            "summary": "Contains a meeting invitation or meeting link."
        }
    prompt = f"""
You are an email assistant.

Classify the email into one of:
- junk
- normal
- important

Mark an email as IMPORTANT if it includes any of the following:
- meeting invite or meeting scheduling
- Google Meet / Zoom / Teams link
- action required
- deadline or urgent request
- payment, invoice, banking, or security alert
- OTP / verification code
- job interview or recruiter communication

Only provide a summary if the email is important.

Respond ONLY in valid JSON:
{{
  "category": "junk | normal | important",
  "summary": "text"
}}

Email:
Subject: {subject}
Body: {body[:5000]}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    response_text = response.output_text

    try:
        json_str = re.search(r"\{.*\}", response_text, re.DOTALL).group()
        return json.loads(json_str)
    except Exception:
        return {"category": "normal", "summary": ""}