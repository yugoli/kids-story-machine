from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.schemas import StoryRequest
from app.openai_client import generate_story
from app.image_generator import generate_image
from app.pdf_generator import generate_pdf
import os

app = FastAPI()

# Define request models for image and PDF generation
class ImageRequest(BaseModel):
    prompt: str

class PDFRequest(BaseModel):
    story_text: str

@app.post("/generate_story")
def story_endpoint(request: StoryRequest):
    return {"story": generate_story(request)}

@app.post("/image")
def image_endpoint(request: ImageRequest):
    image_url = generate_image(request.prompt)
    return {"image_url": image_url}

@app.post("/pdf")
async def pdf_endpoint(request: PDFRequest):
    pdf_path = generate_pdf(request.story_text)
    if pdf_path and os.path.exists(pdf_path):
        # Return the PDF file as a response
        return FileResponse(path=pdf_path, filename="story.pdf", media_type="application/pdf")
    else:
        return {"error": "Failed to generate PDF"}
