from pydantic import BaseModel
from typing import List

class QuestionResponse(BaseModel):
    id: List[str]
    questions: List[str]

class ScoreResponse(BaseModel):
    score: float
    feedback: str