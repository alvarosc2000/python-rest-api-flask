from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=3, max_length=60)
    overview: str = Field(..., min_length=15, max_length=250)
    year: int = Field(..., ge=1888, le=datetime.now().year)
    rating: float = Field(..., ge=0, le=10)
    category: str = Field(..., min_length=3, max_length=20)

    class Config:
        orm_mode = True
