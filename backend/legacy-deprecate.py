from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key="OPENAI_API_KEY")

#openai.api_key = "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"

app = FastAPI()

class StoryRequest(BaseModel):
    characters: str
    theme: str
    age: int

@app.post("/generate_story")
def generate_story(request: StoryRequest):
    prompt = f"Write a short, magical story for a {request.age}-year-old about {request.characters}. Theme: {request.theme}. Make it fun, positive, and easy to understand."
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    story = response.choices[0].message.content
    
    return {"story": story}
