from fastapi import FastAPI
from app.schemas import StoryRequest
from app.openai_client import generate_story

app = FastAPI()

@app.post("/generate_story")
def story_endpoint(request: StoryRequest):
    return {"story": generate_story(request)}
