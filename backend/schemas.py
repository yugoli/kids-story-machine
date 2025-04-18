from pydantic import BaseModel

class StoryRequest(BaseModel):
    characters: str
    theme: str
    age: int
