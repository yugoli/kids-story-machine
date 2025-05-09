from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
#print("Loaded OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_story(request):
    prompt = f"Write a short story for a {request.age}-year-old about {request.characters}. Theme: {request.theme}."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
