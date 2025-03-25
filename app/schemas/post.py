from pydantic import BaseModel, Field

class PostCreate(BaseModel):
    text: str = Field(..., max_length=1_000_000)

class PostResponse(BaseModel):
    id: int
    text: str