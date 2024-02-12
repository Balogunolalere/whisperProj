from pydantic import BaseModel, Field
from typing import List
from .segment import Segment


class TranscriptionData(BaseModel):
    language: str
    language_probability: float = Field(..., ge=0, le=1)  # probability can be between 0 and 1 inclusive
    segments: List[Segment]
    execution_time: float = Field(..., gt=0)