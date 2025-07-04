# from pydantic import BaseModel
# from typing import List

# class QuestionRequest(BaseModel):
#     role: str
#     level: str
#     company: str
#     resumeText: str

# class AnswerRequest(BaseModel):
#     id: List[str]
#     answers: List[str]




from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    role: str
    level: str
    company: str
    resumeText: str
    include_coding_problems: Optional[bool] = True  # Default to True

class AnswerRequest(BaseModel):
    id: List[str]  # 8 theory + 2 coding IDs
    language: str  # python, java, javascript, cpp
    answers: List[str]  # 8 theory answers
    code_submissions: List[str]  # 2 code submissions