from pydantic import BaseModel
from typing import Optional

class StoryRequest(BaseModel):
    characters: str
    theme: str
    age: int

class PDFRequest(BaseModel):
    story_text: str
    image_url: Optional[str] = None
