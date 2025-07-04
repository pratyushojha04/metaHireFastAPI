# from pydantic import BaseModel
# from typing import List

# class QuestionResponse(BaseModel):
#     id: List[str]
#     questions: List[str]

# class ScoreResponse(BaseModel):
#     score: float
#     feedback: str



from pydantic import BaseModel
from typing import List, Dict, Any

class QuestionResponse(BaseModel):
    id: List[str]  # 8 theory + 2 coding IDs
    questions: List[str]  # 8 theory questions
    coding_problems: List[Dict[str, Any]]  # 2 coding problems with fields

class ScoreResponse(BaseModel):
    score: float
    feedback: str