This prototype is designed for high-volume email triage.
It fetches recent emails from Gmail, parses the content, applies rules for obvious cases like OTPs or meeting links, and then uses an LLM to classify ambiguous emails as junk, normal, or important.
Important emails are summarized and sent as a WhatsApp digest.
I also added message chunking to handle WhatsApp length limits.
In a production enterprise version, the same architecture could be extended to Outlook, internal systems, and a private or enterprise-hosted LLM.