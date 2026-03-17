from gmail_reader import get_recent_emails
from ai_classifier import classify_email
from whatsapp_sender import send_whatsapp,split_message

def main():
    emails = get_recent_emails(limit=10)
    important_summaries = []

    for email in emails:
        result = classify_email(email['subject'], email['body'])
        summary = result.get("summary", "")[:180]
        category=result.get("category")
        if result['category'] == 'important':
            important_summaries.append(f"- From: {email['sender']}\n  {summary}")

    if important_summaries:
        full_message = "📬 Important Emails Today\n\n" + "\n\n".join(important_summaries)
        chunks = split_message(full_message)
        
        for i, chunk in enumerate(chunks, start=1):
            if len(chunks) > 1:
                chunk = f"Part {i}/{len(chunks)}\n\n" + chunk
            send_whatsapp(chunk)
            print(f"""
                  From: {email['sender']}
                  Subject: {email['subject']}
                  Category: {category}
                  Summary: {summary}
                  """)
    else:
        print("No important emails today.")

if __name__ == "__main__":
    main()