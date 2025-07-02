from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    role: str
    level: str
    company: str
    resumeText: str

class AnswerRequest(BaseModel):
    id: List[str]
    answers: List[str]