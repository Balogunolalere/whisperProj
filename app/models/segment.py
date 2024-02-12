from pydantic import BaseModel, Field
from typing import List

class Segment(BaseModel):
    start: float = Field(..., ge=0)  # start time can be 0 or greater
    end: float = Field(..., gt=0)  # end time must be greater than 0
    text: str