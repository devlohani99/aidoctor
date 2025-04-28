# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup GROQ API key
import os
import requests
import json

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

#Step2: Convert image to required format
import base64


#image_path="acne.jpg"

def encode_image(image_path):   
    image_file=open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode('utf-8')

#Step3: Setup Multimodal LLM 
from groq import Groq

query="Is there something wrong with my face?"
model="llama-3.3-70b-versatile"

def analyze_image_with_query(query, model, encoded_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    return response.json()["choices"][0]["message"]["content"]