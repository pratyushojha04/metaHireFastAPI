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




































# from models.request_models import AnswerRequest
# from models.response_models import ScoreResponse
# from services.database_service import db
# from sentence_transformers import SentenceTransformer, util
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import logging
# import numpy as np
# import os

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Load scoring method from environment variable (default: sbert)
# SCORING_METHOD = os.getenv("SCORING_METHOD", "sbert").lower()

# # Initialize models
# sbert_model = None
# if SCORING_METHOD == "sbert":
#     sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
# tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# def score_answers(request: AnswerRequest) -> ScoreResponse:
#     total_score = 0
#     feedback = []

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
#                 if SCORING_METHOD == "sbert":
#                     # Sentence-BERT similarity
#                     embeddings = sbert_model.encode([reference_answer, user_answer], convert_to_tensor=True)
#                     similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
#                     score = similarity * 10
#                     # Extract key terms for feedback (using TF-IDF for simplicity)
#                     tfidf_matrix = tfidf_vectorizer.fit_transform([reference_answer])
#                     feature_names = tfidf_vectorizer.get_feature_names_out()
#                     tfidf_scores = tfidf_matrix[0].toarray()[0]
#                     top_terms = [feature_names[i] for i in np.argsort(tfidf_scores)[-3:]]
#                 else:
#                     # TF-IDF cosine similarity
#                     tfidf_matrix = tfidf_vectorizer.fit_transform([reference_answer, user_answer])
#                     similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
#                     score = similarity * 10
#                     feature_names = tfidf_vectorizer.get_feature_names_out()
#                     tfidf_scores = tfidf_matrix[0].toarray()[0]
#                     top_terms = [feature_names[i] for i in np.argsort(tfidf_scores)[-3:]]

#                 total_score += score
                
#                 if similarity < 0.3:
#                     feedback.append(f"Question ID {qid}: Answer needs significant improvement. Include key concepts like: {', '.join(top_terms) or 'more details'}.")
#                 elif similarity < 0.5:
#                     feedback.append(f"Question ID {qid}: Answer partially correct. Add details about: {', '.join(top_terms) or 'more details'}.")
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
import json
import ast
import subprocess
import tempfile
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load scoring method
SCORING_METHOD = os.getenv("SCORING_METHOD", "sbert").lower()

# Initialize models
sbert_model = None
if SCORING_METHOD == "sbert":
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

def safe_execute_python(code: str, input_data: any) -> any:
    """Execute Python code safely."""
    try:
        restricted_globals = {"__builtins__": {}}
        local_vars = {}
        exec(code, restricted_globals, local_vars)
        func_name = next(iter(local_vars), None)
        if not func_name:
            logger.error("No function found in Python code")
            print(f"Python Error: No function found in code:\n{code}")
            return None
        result = local_vars[func_name](input_data)
        logger.debug(f"Python code executed. Input: {input_data}, Output: {result}")
        print(f"Python Execution - Input: {input_data}, Output: {result}")
        return result
    except Exception as e:
        logger.error(f"Python execution failed: {str(e)}")
        print(f"Python Execution Error: {str(e)}")
        return None

def safe_execute_java(code: str, input_data: any) -> any:
    """Execute Java code."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(code)
            class_name = code.split("class ")[1].split("{")[0].strip()
            f_path = f.name
        subprocess.run(['javac', f_path], check=True)
        input_str = json.dumps(input_data) if isinstance(input_data, (list, dict)) else str(input_data)
        result = subprocess.run(['java', '-cp', os.path.dirname(f_path), class_name], input=input_str, text=True, capture_output=True)
        os.remove(f_path)
        os.remove(f_path.replace('.java', '.class'))
        output = result.stdout.strip()
        logger.debug(f"Java code executed. Input: {input_data}, Output: {output}")
        print(f"Java Execution - Input: {input_data}, Output: {output}")
        return ast.literal_eval(output)
    except Exception as e:
        logger.error(f"Java execution failed: {str(e)}")
        print(f"Java Execution Error: {str(e)}")
        return None

def safe_execute_javascript(code: str, input_data: any) -> any:
    """Execute JavaScript code."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(f"const input = {json.dumps(input_data)};\n{code}\nconsole.log(JSON.stringify(solution(input)));")
            f_path = f.name
        result = subprocess.run(['node', f_path], text=True, capture_output=True)
        os.remove(f_path)
        output = result.stdout.strip()
        logger.debug(f"JavaScript code executed. Input: {input_data}, Output: {output}")
        print(f"JavaScript Execution - Input: {input_data}, Output: {output}")
        return ast.literal_eval(output)
    except Exception as e:
        logger.error(f"JavaScript execution failed: {str(e)}")
        print(f"JavaScript Execution Error: {str(e)}")
        return None

def safe_execute_cpp(code: str, input_data: any) -> any:
    """Execute C++ code."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(code)
            f_path = f.name
        exec_path = f_path.replace('.cpp', '')
        subprocess.run(['g++', f_path, '-o', exec_path], check=True)
        input_str = json.dumps(input_data) if isinstance(input_data, (list, dict)) else str(input_data)
        result = subprocess.run([exec_path], input=input_str, text=True, capture_output=True)
        os.remove(f_path)
        os.remove(exec_path)
        output = result.stdout.strip()
        logger.debug(f"C++ code executed. Input: {input_data}, Output: {output}")
        print(f"C++ Execution - Input: {input_data}, Output: {output}")
        return ast.literal_eval(output)
    except Exception as e:
        logger.error(f"C++ execution failed: {str(e)}")
        print(f"C++ Execution Error: {str(e)}")
        return None

def evaluate_test_case(code: str, test_case: str, language: str) -> bool:
    """Evaluate code against a test case."""
    print(f"Evaluating test case for {language} - Raw test case: {test_case}")
    try:
        # Try JSON format
        try:
            tc_dict = json.loads(test_case)
            input_data = ast.literal_eval(tc_dict["input"])
            expected_output = ast.literal_eval(tc_dict["output"])
        except json.JSONDecodeError:
            # Try "input: [1,2,3], output: 6"
            try:
                parts = test_case.replace("input: ", "").replace("output: ", "").split(", ")
                if len(parts) != 2:
                    logger.error(f"Invalid test case format: {test_case}")
                    print(f"Test Case Error: Invalid format (expected 'input: ..., output: ...'): {test_case}")
                    return False
                input_data = ast.literal_eval(parts[0])
                expected_output = ast.literal_eval(parts[1])
            except:
                # Try "[1,2,3] 6"
                try:
                    parts = test_case.split(" ")
                    if len(parts) != 2:
                        logger.error(f"Invalid test case format: {test_case}")
                        print(f"Test Case Error: Invalid format (expected '[1,2,3] 6'): {test_case}")
                        return False
                    input_data = ast.literal_eval(parts[0])
                    expected_output = ast.literal_eval(parts[1])
                except Exception as e:
                    logger.error(f"Test case parsing failed: {str(e)}, Test case: {test_case}")
                    print(f"Test Case Parsing Error: {str(e)}, Test case: {test_case}")
                    return False

        logger.debug(f"Test case - Input: {input_data}, Expected Output: {expected_output}")
        print(f"Test Case - Language: {language}, Input: {input_data}, Expected Output: {expected_output}")

        if language == "python":
            result = safe_execute_python(code, input_data)
        elif language == "java":
            result = safe_execute_java(code, input_data)
        elif language == "javascript":
            result = safe_execute_javascript(code, input_data)
        elif language == "cpp":
            result = safe_execute_cpp(code, input_data)
        else:
            logger.error(f"Unsupported language: {language}")
            print(f"Error: Unsupported language: {language}")
            return False

        logger.debug(f"Actual Output: {result}")
        print(f"Test Case - Actual Output: {result}")
        return result == expected_output
    except Exception as e:
        logger.error(f"Test case evaluation failed: {str(e)}, Test case: {test_case}")
        print(f"Test Case Evaluation Error: {str(e)}, Test case: {test_case}")
        return False

def score_answers(request: AnswerRequest) -> ScoreResponse:
    print(f"Processing request for language: {request.language}")
    if len(request.id) != 10 or len(request.answers) != 8 or len(request.code_submissions) != 2:
        logger.error(f"Invalid request: Expected 10 IDs, 8 answers, 2 code submissions. Got {len(request.id)} IDs, {len(request.answers)} answers, {len(request.code_submissions)} code submissions.")
        raise HTTPException(status_code=400, detail="Must provide 10 IDs (8 theory, 2 coding), 8 theory answers, and 2 code submissions.")

    if request.language not in ["python", "java", "javascript", "cpp"]:
        logger.error(f"Invalid language: {request.language}")
        raise HTTPException(status_code=400, detail="Language must be python, java, javascript, or cpp.")

    total_score = 0
    feedback = []

    # Score theory questions (first 8)
    for qid, user_answer in zip(request.id[:8], request.answers):
        try:
            collection_name, question_id = qid.split(":", 1)
            collection = db[collection_name]
            question = collection.find_one({"id": question_id})
            if not question or not question.get("answer"):
                logger.error(f"Question ID {qid} not found or missing answer in collection {collection_name}")
                print(f"Error: Question ID {qid} not found or missing answer in collection {collection_name}")
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
                    embeddings = sbert_model.encode([reference_answer, user_answer], convert_to_tensor=True)
                    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
                    score = similarity * 1.25  # Scale to 1.25 for 10 points total
                    tfidf_matrix = tfidf_vectorizer.fit_transform([reference_answer])
                    feature_names = tfidf_vectorizer.get_feature_names_out()
                    tfidf_scores = tfidf_matrix[0].toarray()[0]
                    top_terms = [feature_names[i] for i in np.argsort(tfidf_scores)[-3:]]
                else:
                    tfidf_matrix = tfidf_vectorizer.fit_transform([reference_answer, user_answer])
                    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                    score = similarity * 1.25  # Scale to 1.25 for 10 points total
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
            print(f"Error: Invalid ID format for {qid}")
            feedback.append(f"Question ID {qid}: Invalid ID format.")
            continue

    # Score coding problems (last 2)
    for qid, code in zip(request.id[8:], request.code_submissions):
        print(f"Scoring coding problem ID: {qid}")
        try:
            collection_name, question_id = qid.split(":", 1)
            if collection_name != "coding_problem":
                logger.error(f"Invalid collection for coding problem ID {qid}")
                print(f"Error: Invalid collection for coding problem ID {qid}")
                feedback.append(f"Question ID {qid}: Invalid coding problem ID.")
                continue

            collection = db[collection_name]
            problem = collection.find_one({"id": question_id})
            if not problem:
                logger.error(f"Coding problem ID {qid} not found")
                print(f"Error: Coding problem ID {qid} not found in collection")
                feedback.append(f"Question ID {qid}: Coding problem not found.")
                continue

            logger.info(f"Scoring coding problem ID {qid}: Code:\n{code}")
            print(f"Code for {qid}:\n{code}")

            # Evaluate test cases
            test_cases = [problem[f"tc{i}"] for i in range(1, 6)]
            passed_tests = 0
            test_feedback = []
            for i, tc in enumerate(test_cases, 1):
                print(f"Evaluating test case {i} for {qid}: {tc}")
                if evaluate_test_case(code, tc, request.language):
                    passed_tests += 1
                    test_feedback.append(f"Test case {i}: Passed")
                else:
                    test_feedback.append(f"Test case {i}: Failed")

            # Score: 0.5 points per test case (max 2.5 per problem)
            score = passed_tests * 0.5
            total_score += score
            feedback.append(f"Question ID {qid}: Coding problem score: {score}/2.5. {' '.join(test_feedback)}")
            logger.info(f"Score for ID {qid}: {score:.2f} (Passed {passed_tests}/5 test cases)")
            print(f"Score for {qid}: {score:.2f} (Passed {passed_tests}/5 test cases)")
        except Exception as e:
            logger.error(f"Error scoring coding problem ID {qid}: {str(e)}")
            print(f"Error scoring coding problem ID {qid}: {str(e)}")
            feedback.append(f"Question ID {qid}: Error executing code: {str(e)}")
            total_score += 0

    final_score = total_score if total_score > 0 else 0
    print(f"Final score: {final_score:.2f}")

    return ScoreResponse(
        score=round(final_score, 2),
        feedback="\n".join(feedback)
    )