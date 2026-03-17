AI Email Agent Prototype

# Demo

https://www.loom.com/share/322e6a8c2a664dfeaa2be379d3034bfd

# Demo 

assets/screenshots/demo.png


Problem

High email volume makes it difficult to quickly identify important messages, especially on the go.

Solution

This prototype builds an AI-powered email assistant that:

1. Reads recent Gmail emails
2. Classifies them as junk, normal, or important
3. Summarizes important emails
4. Sends a digest to WhatsApp

Architecture

Gmail → Parser → Rules + LLM → Filter → WhatsApp Digest

Agent Loop

Observe → Reason → Act

1. Observe: Fetch recent emails
2. Reason: Classify using rule-based logic + OpenAI LLM
3. Act: Send summarized digest to WhatsApp

Features

1. Gmail integration
2. HTML email parsing (BeautifulSoup)
3. Rule-based priority handling (e.g., OTP, meeting links)
4. LLM-based classification and summarization
5. WhatsApp delivery via Twilio
6. Message chunking to handle WhatsApp character limits

How to Run

pip install -r requirements.txt
python main.py


Configuration

1. Add API keys in .env
3. Set up Gmail OAuth using Google Cloud and download the JSON file rename it to credentials.json
3. Running gmail_reader.py will generate token.json
4. Configure Twilio WhatsApp sandbox

Notes: credentials.json and token.json are NOT included in the repository.They must be generated locally. These files are already listed in .gitignore

Limitations

1. Currently supports Gmail only (prototype stage)
2. Uses Twilio sandbox for WhatsApp testing
3. Rule-based system is basic and can be expanded
4. Uses cloud LLM (can be replaced with private model in production)


Future Improvements

1. Outlook / Microsoft Exchange integration
2. Private or enterprise-hosted LLM deployment
3. User-specific importance learning
4. Web dashboard / admin interface
5. Scheduled daily summaries
6. Logging and audit system