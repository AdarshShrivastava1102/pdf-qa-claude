import sys
import os
from dotenv import load_dotenv
import anthropic
from pypdf import PdfReader

# Load API key from .env
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Validate command-line arguments
if len(sys.argv) < 3:
    print("Usage: python qa.py <filename.pdf> \"<your question>\"")
    print("Example: python qa.py mckinsey_ai.pdf \"What are the top 3 AI use cases mentioned?\"")
    sys.exit(1)

filename = sys.argv[1]
question = sys.argv[2]

# Read PDF and extract text
print(f"Reading {filename}...")
reader = PdfReader(filename)
text = ""
for page in reader.pages:
    text += page.extract_text()

print(f"Extracted {len(text)} characters from {len(reader.pages)} pages")

# Set up Claude client
client = anthropic.Anthropic(api_key=api_key)

# Send question + document context to Claude
print(f"Asking Claude: \"{question}\"...\n")
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": f"""You are a document Q&A assistant. Answer the question based ONLY on the document provided. If the answer isn't in the document, say so honestly. Be specific and cite relevant details.

Document:
{text[:8000]}

Question: {question}"""
        }
    ]
)

# Print the answer
print("=== Answer ===\n")
print(response.content[0].text)
print("\n==============\n")