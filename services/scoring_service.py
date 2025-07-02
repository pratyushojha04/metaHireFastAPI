# from models.request_models import AnswerRequest
# from models.response_models import ScoreResponse
# from services.database_service import db
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import logging
# import numpy as np

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def score_answers(request: AnswerRequest) -> ScoreResponse:
#     total_score = 0
#     feedback = []
#     vectorizer = TfidfVectorizer(stop_words='english')  # Remove common words for better scoring

#     for qid, user_answer in zip(request.id, request.answers):
#         try:
#             collection_name, question_id = qid.split(":", 1)
#             collection = db[collection_name]
#             question = collection.find_one({"id": question_id})
#             if not question or not question.get("answer"):
#                 logger.error(f"Question ID {qid} not found or missing answer in collection {collection_name}")
#                 feedback.append(f"Question ID {qid}: Reference answer not found or empty.")
#                 continue

#             reference_answer = question["answer"]
#             logger.info(f"Scoring ID {qid}: User answer: '{user_answer}' | Reference answer: '{reference_answer}'")
            
#             if not user_answer or not isinstance(user_answer, str) or len(user_answer.strip()) < 5:
#                 logger.warning(f"Invalid user answer for ID {qid}: '{user_answer}'")
#                 feedback.append(f"Question ID {qid}: Answer is too short or invalid. Please provide a detailed response.")
#                 continue

#             try:
#                 tfidf_matrix = vectorizer.fit_transform([reference_answer, user_answer])
#                 similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
#                 score = similarity * 10
#                 total_score += score
                
#                 # Extract key terms from reference answer
#                 feature_names = vectorizer.get_feature_names_out()
#                 tfidf_scores = tfidf_matrix[0].toarray()[0]
#                 top_terms = [feature_names[i] for i in np.argsort(tfidf_scores)[-3:]]  # Top 3 terms
                
#                 if similarity < 0.3:
#                     feedback.append(f"Question ID {qid}: Answer needs significant improvement. Include key concepts like: {', '.join(top_terms)}.")
#                 elif similarity < 0.5:
#                     feedback.append(f"Question ID {qid}: Answer partially correct. Add details about: {', '.join(top_terms)}.")
#                 else:
#                     feedback.append(f"Question ID {qid}: Good answer, well-aligned with expected response.")
#                 logger.info(f"Score for ID {qid}: {score:.2f} (Similarity: {similarity:.2f}, Top terms: {top_terms})")
#             except Exception as e:
#                 logger.error(f"Error computing similarity for ID {qid}: {str(e)}")
#                 feedback.append(f"Question ID {qid}: Error processing answer. Please ensure meaningful content.")
#                 total_score += 0
#         except ValueError:
#             logger.error(f"Invalid ID format for {qid}")
#             feedback.append(f"Question ID {qid}: Invalid ID format.")
#             continue

#     final_score = (total_score / 8) if total_score > 0 else 0
    
#     return ScoreResponse(
#         score=round(final_score, 2),
#         feedback="\n".join(feedback)
#     )




from models.request_models import AnswerRequest
from models.response_models import ScoreResponse
from services.database_service import db
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import numpy as np
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load scoring method from environment variable (default: sbert)
SCORING_METHOD = os.getenv("SCORING_METHOD", "sbert").lower()

# Initialize models
sbert_model = None
if SCORING_METHOD == "sbert":
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

def score_answers(request: AnswerRequest) -> ScoreResponse:
    total_score = 0
    feedback = []

    for qid, user_answer in zip(request.id, request.answers):
        try:
            collection_name, question_id = qid.split(":", 1)
            collection = db[collection_name]
            question = collection.find_one({"id": question_id})
            if not question or not question.get("answer"):
                logger.error(f"Question ID {qid} not found or missing answer in collection {collection_name}")
                feedback.append(f"Question ID {qid}: Reference answer not found or empty.")
                continue

            reference_answer = question["answer"]
            logger.info(f"Scoring ID {qid}: User answer: '{user_answer}' | Reference answer: '{reference_answer}'")
            
            if not user_answer or not isinstance(user_answer, str) or len(user_answer.strip()) < 5:
                logger.warning(f"Invalid user answer for ID {qid}: '{user_answer}'")
                feedback.append(f"Question ID {qid}: Answer is too short or invalid. Please provide a detailed response.")
                continue

            try:
                if SCORING_METHOD == "sbert":
                    # Sentence-BERT similarity
                    embeddings = sbert_model.encode([reference_answer, user_answer], convert_to_tensor=True)
                    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
                    score = similarity * 10
                    # Extract key terms for feedback (using TF-IDF for simplicity)
                    tfidf_matrix = tfidf_vectorizer.fit_transform([reference_answer])
                    feature_names = tfidf_vectorizer.get_feature_names_out()
                    tfidf_scores = tfidf_matrix[0].toarray()[0]
                    top_terms = [feature_names[i] for i in np.argsort(tfidf_scores)[-3:]]
                else:
                    # TF-IDF cosine similarity
                    tfidf_matrix = tfidf_vectorizer.fit_transform([reference_answer, user_answer])
                    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                    score = similarity * 10
                    feature_names = tfidf_vectorizer.get_feature_names_out()
                    tfidf_scores = tfidf_matrix[0].toarray()[0]
                    top_terms = [feature_names[i] for i in np.argsort(tfidf_scores)[-3:]]

                total_score += score
                
                if similarity < 0.3:
                    feedback.append(f"Question ID {qid}: Answer needs significant improvement. Include key concepts like: {', '.join(top_terms) or 'more details'}.")
                elif similarity < 0.5:
                    feedback.append(f"Question ID {qid}: Answer partially correct. Add details about: {', '.join(top_terms) or 'more details'}.")
                else:
                    feedback.append(f"Question ID {qid}: Good answer, well-aligned with expected response.")
                logger.info(f"Score for ID {qid}: {score:.2f} (Similarity: {similarity:.2f}, Top terms: {top_terms})")
            except Exception as e:
                logger.error(f"Error computing similarity for ID {qid}: {str(e)}")
                feedback.append(f"Question ID {qid}: Error processing answer. Please ensure meaningful content.")
                total_score += 0
        except ValueError:
            logger.error(f"Invalid ID format for {qid}")
            feedback.append(f"Question ID {qid}: Invalid ID format.")
            continue

    final_score = (total_score / 8) if total_score > 0 else 0
    
    return ScoreResponse(
        score=round(final_score, 2),
        feedback="\n".join(feedback)
    )