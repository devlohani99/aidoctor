from dotenv import load_dotenv
import os

env_path = os.path.abspath(".env")
print("Loading .env from:", env_path)

# Check if file exists
if os.path.exists(env_path):
    print("[OK] .env file exists")
    # Try to read the file contents
    try:
        with open(env_path, 'r') as f:
            print("[OK] .env file contents:")
            print(f.read())
    except Exception as e:
        print("[ERROR] Error reading .env file:", e)

# Load the environment variables
load_dotenv(dotenv_path=env_path)

# Check GROQ API key
groq_key = os.environ.get("GROQ_API_KEY")
print("\nGROQ_API_KEY:", groq_key)
if groq_key is None:
    print("[ERROR] GROQ_API_KEY is not set in environment")
else:
    print("[OK] GROQ_API_KEY is set")

# Check ELEVENLABS API key
eleven_key = os.environ.get("ELEVENLABS_API_KEY")
print("\nELEVENLABS_API_KEY:", eleven_key)
if eleven_key is None:
    print("[ERROR] ELEVENLABS_API_KEY is not set in environment")
else:
    print("[OK] ELEVENLABS_API_KEY is set")
