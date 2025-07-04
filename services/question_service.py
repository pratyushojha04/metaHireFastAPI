


# from models.request_models import QuestionRequest
# from models.response_models import QuestionResponse
# from services.database_service import db
# import random
# from fastapi import HTTPException
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def get_random_questions(request: QuestionRequest) -> QuestionResponse:
#     # Map level to difficulty
#     level_to_difficulty = {
#         "fresher": "Easy",
#         "intermediate": "Medium",
#         "experienced": "Hard"
#     }
#     difficulty = level_to_difficulty.get(request.level.lower(), "Medium")

#     # Map role to collection name (case-insensitive)
#     role_to_collection = {
#         "sde": "backend",
#         "backend dev": "backend",
#         "frontend dev": "frontend_development",
#         "fullstack": ["backend", "frontend_development"],
#         "data scientist": "machine_learning",
#         "data analyst": "data_analyst",
#         "machine learning engineer": "machine_learning",
#         "cloud engineer": "cloud_engineer",
#         "devops": "devops",
#         "tester": "tester"
#     }

#     # Normalize role for lookup
#     normalized_role = request.role.lower()
#     collections = role_to_collection.get(normalized_role)
#     if not collections:
#         logger.error(f"Role '{request.role}' not found in role_to_collection mapping")
#         raise HTTPException(status_code=400, detail=f"Invalid role: {request.role}")

#     if isinstance(collections, str):
#         collections = [collections]

#     # Log request details
#     logger.info(f"Fetching questions for role: {request.role}, difficulty: {difficulty}, company: {request.company}")

#     # Collect questions from the relevant collection(s)
#     all_questions = []
#     for collection_name in collections:
#         collection = db[collection_name]
#         query = {"difficulty": difficulty}
#         if request.company.lower() != "any":
#             query["company"] = request.company
#         questions = list(collection.find(query))
#         logger.info(f"Found {len(questions)} questions in collection {collection_name} for query {query}")
#         for q in questions:
#             q['source_collection'] = collection_name  # Track source for ID formatting
#         all_questions.extend(questions)

#     if len(all_questions) < 8:
#         logger.error(f"Not enough questions found: {len(all_questions)} for role '{request.role}', difficulty '{difficulty}', company '{request.company}'")
#         raise HTTPException(status_code=404, detail=f"Not enough questions found for role '{request.role}' and difficulty '{difficulty}'. Found {len(all_questions)} questions.")

#     # Select 8 random questions
#     selected_questions = random.sample(all_questions, min(8, len(all_questions)))
    
#     response = QuestionResponse(
#         id=[f"{q['source_collection']}:{q['id']}" for q in selected_questions],
#         questions=[q["question"] for q in selected_questions]
#     )
    
#     # Log selected questions
#     logger.info(f"Selected questions: {response.id}")
#     return response




































# from models.request_models import QuestionRequest
# from models.response_models import QuestionResponse
# from services.database_service import db
# import random
# from fastapi import HTTPException
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def get_random_questions(request: QuestionRequest) -> QuestionResponse:
#     # Map level to difficulty
#     level_to_difficulty = {
#         "fresher": "Easy",
#         "intermediate": "Medium",
#         "experienced": "Hard"
#     }
#     difficulty = level_to_difficulty.get(request.level.lower(), "Medium")

#     # Map role to collection name (case-insensitive)
#     role_to_collection = {
#         "sde": "backend",
#         "backend dev": "backend",
#         "frontend dev": "frontend_development",
#         "fullstack": ["backend", "frontend_development"],
#         "data scientist": "machine_learning",
#         "data analyst": "data_analyst",
#         "machine learning engineer": "machine_learning",
#         "cloud engineer": "cloud_engineer",
#         "devops": "devops",
#         "tester": "tester"
#     }

#     # Normalize role for lookup
#     normalized_role = request.role.lower()
#     collections = role_to_collection.get(normalized_role)
#     if not collections:
#         logger.error(f"Role '{request.role}' not found in role_to_collection mapping")
#         raise HTTPException(status_code=400, detail=f"Invalid role: {request.role}")

#     if isinstance(collections, str):
#         collections = [collections]

#     # Log request details
#     logger.info(f"Fetching questions for role: {request.role}, difficulty: {difficulty}, company: {request.company}")

#     # Collect questions from the relevant collection(s)
#     all_questions = []
#     query = {"difficulty": {"$in": ["Easy", "easy", "EASY"]}}  # Case-insensitive difficulty
#     if request.company.lower() != "any":
#         query["company"] = request.company

#     for collection_name in collections:
#         collection = db[collection_name]
#         questions = list(collection.find(query))
#         logger.info(f"Found {len(questions)} questions in collection {collection_name} for query {query}")
#         for q in questions:
#             q['source_collection'] = collection_name
#         all_questions.extend(questions)

#     # Fallback: Retry without company filter if too few questions
#     if len(all_questions) < 8 and request.company.lower() != "any":
#         logger.warning(f"Insufficient questions ({len(all_questions)}) with company '{request.company}'. Retrying without company filter.")
#         query = {"difficulty": {"$in": ["Easy", "easy", "EASY"]}}
#         all_questions = []
#         for collection_name in collections:
#             collection = db[collection_name]
#             questions = list(collection.find(query))
#             logger.info(f"Fallback: Found {len(questions)} questions in collection {collection_name} for query {query}")
#             for q in questions:
#                 q['source_collection'] = collection_name
#             all_questions.extend(questions)

#     if len(all_questions) < 8:
#         logger.error(f"Not enough questions found: {len(all_questions)} for role '{request.role}', difficulty '{difficulty}', company '{request.company}'")
#         raise HTTPException(status_code=404, detail=f"Not enough questions found for role '{request.role}' and difficulty '{difficulty}'. Found {len(all_questions)} questions.")

#     # Select 8 random questions
#     selected_questions = random.sample(all_questions, min(8, len(all_questions)))
    
#     response = QuestionResponse(
#         id=[f"{q['source_collection']}:{q['id']}" for q in selected_questions],
#         questions=[q["question"] for q in selected_questions]
#     )
    
#     logger.info(f"Selected questions: {response.id}")
#     return response




from models.request_models import QuestionRequest
from models.response_models import QuestionResponse
from services.database_service import db
import random
from fastapi import HTTPException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_random_questions(request: QuestionRequest) -> QuestionResponse:
    # Map level to difficulty
    level_to_difficulty = {
        "fresher": "Easy",
        "intermediate": "Medium",
        "experienced": "Hard"
    }
    difficulty = level_to_difficulty.get(request.level.lower(), "Medium")

    # Map role to collection name (case-insensitive)
    role_to_collection = {
        "sde": "backend",
        "backend dev": "backend",
        "frontend dev": "frontend_development",
        "fullstack": ["backend", "frontend_development"],
        "data scientist": "machine_learning",
        "data analyst": "data_analyst",
        "machine learning engineer": "machine_learning",
        "cloud engineer": "cloud_engineer",
        "devops": "devops",
        "tester": "tester"
    }

    # Normalize role for lookup
    normalized_role = request.role.lower()
    collections = role_to_collection.get(normalized_role)
    if not collections:
        logger.error(f"Role '{request.role}' not found in role_to_collection mapping")
        raise HTTPException(status_code=400, detail=f"Invalid role: {request.role}")

    if isinstance(collections, str):
        collections = [collections]

    # Log request details
    logger.info(f"Fetching questions for role: {request.role}, difficulty: {difficulty}, company: {request.company}")

    # Collect theory questions
    all_questions = []
    query = {"difficulty": {"$in": ["Easy", "easy", "EASY"]}}
    if request.company.lower() != "any":
        query["company"] = request.company

    for collection_name in collections:
        collection = db[collection_name]
        questions = list(collection.find(query))
        logger.info(f"Found {len(questions)} questions in collection {collection_name} for query {query}")
        for q in questions:
            q['source_collection'] = collection_name
        all_questions.extend(questions)

    # Fallback: Retry without company filter
    if len(all_questions) < 8 and request.company.lower() != "any":
        logger.warning(f"Insufficient questions ({len(all_questions)}) with company '{request.company}'. Retrying without company filter.")
        query = {"difficulty": {"$in": ["Easy", "easy", "EASY"]}}
        all_questions = []
        for collection_name in collections:
            collection = db[collection_name]
            questions = list(collection.find(query))
            logger.info(f"Fallback: Found {len(questions)} questions in collection {collection_name} for query {query}")
            for q in questions:
                q['source_collection'] = collection_name
            all_questions.extend(questions)

    if len(all_questions) < 8:
        logger.error(f"Not enough questions found: {len(all_questions)} for role '{request.role}', difficulty '{difficulty}', company '{request.company}'")
        raise HTTPException(status_code=404, detail=f"Not enough questions found for role '{request.role}' and difficulty '{difficulty}'. Found {len(all_questions)} questions.")

    # Select 8 random theory questions
    selected_questions = random.sample(all_questions, min(8, len(all_questions)))

    # Collect coding problems
    coding_problems = []
    if request.include_coding_problems:
        collection = db["coding_problem"]
        coding_query = {"difficulty": {"$in": ["Easy", "easy", "EASY"]}}
        if request.company.lower() != "any":
            coding_query["company"] = request.company
        coding_questions = list(collection.find(coding_query))
        logger.info(f"Found {len(coding_questions)} coding problems for query {coding_query}")

        # Fallback: Retry without company filter
        if len(coding_questions) < 2 and request.company.lower() != "any":
            logger.warning(f"Insufficient coding problems ({len(coding_questions)}). Retrying without company filter.")
            coding_query = {"difficulty": {"$in": ["Easy", "easy", "EASY"]}}
            coding_questions = list(collection.find(coding_query))
            logger.info(f"Fallback: Found {len(coding_questions)} coding problems for query {coding_query}")

        if len(coding_questions) < 2:
            logger.warning(f"Not enough coding problems found: {len(coding_questions)}. Skipping coding problems.")
        else:
            selected_coding = random.sample(coding_questions, min(2, len(coding_questions)))
            for q in selected_coding:
                coding_problems.append({
                    "question": q["question"],
                    "problem_description": q["problem_description"],
                    "tc1": q["tc1"],
                    "tc2": q["tc2"],
                    "tc3": q["tc3"],
                    "tc4": q["tc4"],
                    "tc5": q["tc5"],
                    "company": q["company"],
                    "difficulty": q["difficulty"],
                    "category": q["category"],
                    "hint": q["hint"]
                })

    response = QuestionResponse(
        id=[f"{q['source_collection']}:{q['id']}" for q in selected_questions] + [f"coding_problem:{q['id']}" for q in selected_coding],
        questions=[q["question"] for q in selected_questions],
        coding_problems=coding_problems
    )

    logger.info(f"Selected questions: {response.id}")
    return response