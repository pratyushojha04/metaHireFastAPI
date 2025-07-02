from fastapi import APIRouter, HTTPException
from models.request_models import QuestionRequest, AnswerRequest
from models.response_models import QuestionResponse, ScoreResponse
from services.question_service import get_random_questions
from services.scoring_service import score_answers

router = APIRouter()

@router.post("/get_questions", response_model=QuestionResponse)
async def get_questions(request: QuestionRequest):
    try:
        response = get_random_questions(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score_answers", response_model=ScoreResponse)
async def score_answers_endpoint(request: AnswerRequest):
    if len(request.id) != len(request.answers) or len(request.id) != 8:
        raise HTTPException(status_code=400, detail="Must provide exactly 8 answers with corresponding IDs")
    try:
        return score_answers(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))