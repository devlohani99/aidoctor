import os
from dotenv import load_dotenv

load_dotenv()
print("GROQ KEY:", os.environ.get("GROQ_API_KEY"))
