
import os
from dotenv import load_dotenv

# Try to load .env manually to see if it works
load_dotenv()

key = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY found: {bool(key)}")
if key:
    print(f"Key length: {len(key)}")
    print(f"Key start: {key[:4]}")
