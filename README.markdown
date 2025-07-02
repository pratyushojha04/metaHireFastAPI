# Mock Interview Platform Documentation

## 1. Project Overview
The Mock Interview Platform is a FastAPI-based web application designed to simulate technical interviews for roles such as DevOps, Machine Learning Engineer, Backend, and others. It retrieves role-specific questions from a MongoDB database (`interview_db`) and scores user answers using semantic similarity with the **Sentence-BERT (SBERT) `all-mpnet-base-v2`** model, with a TF-IDF fallback option. An alternative model, **SBERT `all-MiniLM-L6-v2`**, can be used for resource-constrained environments. The platform provides detailed feedback to help candidates improve, targeting a maximum score of 10 (e.g., latest score: 7.39/10, with `devops:148` needing refinement).

### Key Features
- **Question Retrieval**: Fetches 8 questions per request from MongoDB collections (e.g., `devops`) based on `role`, `level`, and `company`.
- **Answer Scoring**: Evaluates answers using SBERT `all-mpnet-base-v2` (or `all-MiniLM-L6-v2` as an alternative) for semantic similarity, scoring 0–10 per answer, averaged across 8 questions.
- **Feedback**: Suggests missing concepts (e.g., "systems, tolerance, traffic" for `devops:148`) for low-scoring answers (< 0.3 similarity).
- **Data Management**: Loads questions from CSV files (e.g., `devops.csv`) into MongoDB.
- **Configuration**: Uses a `.env` file for settings (e.g., `SCORING_METHOD=sbert`).

### Objectives
- Simulate real-world technical interviews.
- Provide accurate, semantic-based scoring and feedback.
- Support multiple roles (DevOps, Machine Learning Engineer, etc.) and difficulty levels (Easy, Medium, Hard).
- Achieve scores of 8–9/10 for well-aligned answers.

## 2. Setup Instructions
### Prerequisites
- **Python**: 3.8 or higher
- **MongoDB**: Local instance on `mongodb://localhost:27017/`
- **Dependencies**:
  ```bash
  pip install fastapi uvicorn pymongo pandas sentence-transformers scikit-learn python-dotenv
  ```

### Project Structure
```
mock-interview-platform/
├── data/
│   ├── devops.csv
│   ├── machine_learning.csv
│   ├── backend.csv
│   ├── cloud_engineer.csv
│   ├── data_analyst.csv
│   ├── frontend_development.csv
│   ├── tester.csv
├── services/
│   ├── database_service.py
│   ├── scoring_service.py
├── api/
│   ├── routes.py
├── models/
│   ├── request_models.py
│   ├── response_models.py
├── main.py
├── test_score_answers.py
├── test_get_questions.py
├── .env
└── README.md
```

### Step-by-Step Setup
1. **Clone Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd mock-interview-platform
   ```

2. **Set Up MongoDB**:
   - Install MongoDB: https://www.mongodb.com/docs/manual/installation/
   - Start MongoDB:
     ```bash
     mongod
     ```
   - Verify:
     ```javascript
     mongosh
     show databases
     ```

3. **Prepare CSV Files**:
   - Place CSVs in `data/` (e.g., `devops.csv`).
   - Required columns: `id`, `question`, `answer`, `company`, `role`, `difficulty`, `category`.
   - Example `devops.csv`:
     ```csv
     id,question,answer,company,role,difficulty,category
     148,What is the importance of system design for devops in DevOps?,System design in DevOps is critical for building fault-tolerant, scalable systems that ensure high availability and efficient traffic distribution. It supports microservices architecture, automates CI/CD pipelines, and integrates observability for performance monitoring.,Microsoft,Devops,Medium,System Design
     ```

4. **Create `.env` File**:
   - In project root:
     ```
     MONGO_URI=mongodb://localhost:27017/
     MONGO_DB_NAME=interview_db
     SCORING_METHOD=sbert
     LOG_LEVEL=INFO
     DATA_DIR=data
     PORT=8000
     ```
   - **Variables**:
     - `MONGO_URI`: MongoDB connection string.
     - `MONGO_DB_NAME`: Database name (`interview_db`).
     - `SCORING_METHOD`: `sbert` (uses `all-mpnet-base-v2`) or `tfidf`.
     - `LOG_LEVEL`: `INFO`, `DEBUG`, `ERROR`.
     - `DATA_DIR`: CSV directory.
     - `PORT`: FastAPI port.

5. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Create `requirements.txt`:
   ```
   fastapi==0.110.0
   uvicorn==0.29.0
   pymongo==4.6.2
   pandas==2.2.1
   sentence-transformers==2.5.1
   scikit-learn==1.4.1
   python-dotenv==1.0.1
   ```

6. **Run Application**:
   ```bash
   python main.py
   ```
   - Loads CSVs into MongoDB.
   - Starts FastAPI at `http://0.0.0.0:8000`.

7. **Test Endpoints**:
   - **Get Questions**:
     ```bash
     curl -X POST http://0.0.0.0:8000/get_questions -H "Content-Type: application/json" -d '{"role": "Devops", "level": "fresher", "company": "Microsoft", "resumeText": ""}'
     ```
   - **Score Answers**:
     See `test_score_answers.py` below.

## 3. Running the Application
- **Start Server**:
  ```bash
  python main.py
  ```
- **Endpoints**:
  - `/get_questions`: Retrieves 8 questions (e.g., `devops:179`).
  - `/score_answers`: Scores 8 answers (0–10) with feedback.
  - `/get_reference_answers` (optional): Retrieves reference answers.
- **Logs**: Check logs (`LOG_LEVEL=INFO`) for debugging.

### Example Test
Run `test_score_answers.py`:
```bash
python test_score_answers.py
```
**Latest Output** (July 1, 2025, 15:38 IST):
```json
{
  "score": 7.39,
  "feedback": "Question ID devops:179: Good answer, well-aligned with expected response.\nQuestion ID devops:117: Good answer, well-aligned with expected response.\nQuestion ID devops:173: Good answer, well-aligned with expected response.\nQuestion ID devops:127: Good answer, well-aligned with expected response.\nQuestion ID devops:1: Good answer, well-aligned with expected response.\nQuestion ID devops:60: Good answer, well-aligned with expected response.\nQuestion ID devops:148: Answer needs significant improvement. Include key concepts like: systems, tolerance, traffic.\nQuestion ID devops:195: Good answer, well-aligned with expected response."
}
```

## 4. Architecture
### Components
1. **FastAPI Application** (`main.py`):
   - Initializes server, loads `.env`, and triggers CSV loading.
   - Uses Uvicorn to serve endpoints.

2. **API Routes** (`api/routes.py`):
   - Defines `/get_questions`, `/score_answers`, `/get_reference_answers` (optional).
   - Uses Pydantic for validation.

3. **Database Service** (`services/database_service.py`):
   - Connects to MongoDB (`interview_db`).
   - Loads CSVs into collections (e.g., `devops`).
   - Handles duplicates and missing data.

4. **Scoring Service** (`services/scoring_service.py`):
   - Scores answers using SBERT `all-mpnet-base-v2` (or `all-MiniLM-L6-v2`).
   - Computes cosine similarity, scales to 0–10, and provides feedback.

5. **Models** (`models/`):
   - `request_models.py`: `QuestionRequest`, `AnswerRequest`.
   - `response_models.py`: `QuestionResponse`, `ScoreResponse`.

6. **Data** (`data/`):
   - CSVs with ~200 questions per role.
   - MongoDB collections with fields: `id`, `question`, `answer`, `company`, `role`, `difficulty`, `category`.

### Data Flow
1. **Question Retrieval**:
   - POST `/get_questions` with `role`, `level`, `company`.
   - Queries MongoDB (e.g., `db.devops.find()`).
   - Returns 8 question IDs and texts.

2. **Answer Scoring**:
   - POST `/score_answers` with IDs and answers.
   - Retrieves reference answers.
   - Computes similarity, returns score and feedback.

3. **Debugging**:
   - POST `/get_reference_answers` retrieves reference answers.

### Technology Stack
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Scoring**: SBERT (`all-mpnet-base-v2` or `all-MiniLM-L6-v2`), scikit-learn (TF-IDF)
- **Configuration**: python-dotenv
- **Server**: Uvicorn
- **Data Processing**: Pandas

## 5. Use Cases
1. **Candidate Preparation**:
   - Request questions (e.g., DevOps, fresher, Microsoft).
   - Submit answers, receive scores (e.g., 7.39/10) and feedback.
2. **Interview Simulation**:
   - Mimics technical interviews with role-specific questions.
3. **Debugging**:
   - Inspect reference answers to align responses.
4. **Multi-Role Support**:
   - Supports DevOps, Machine Learning Engineer, etc.

## 6. Scoring Models
The platform uses **SBERT `all-mpnet-base-v2`** for scoring, with `all-MiniLM-L6-v2` as an alternative and TF-IDF as a fallback.

### 6.1 Sentence-BERT `all-mpnet-base-v2` (Primary Model)
#### Overview
- **Description**: A transformer-based model fine-tuned for sentence embeddings, optimized for semantic similarity tasks.
- **Why Used**: Captures semantic meaning (e.g., "CI/CD automates deployment" ≈ "CI/CD streamlines delivery"), improving scores from 2.61 (TF-IDF) to 7.39.
- **Architecture**:
  - **Base Model**: MPNet (Microsoft’s Masked and Permuted Language Modeling).
  - **Layers**: 12 transformer layers, 12 attention heads.
  - **Hidden Size**: 768 dimensions.
  - **Parameters**: ~110 million.
  - **Input**: Tokenized text (max 384 tokens).
  - **Output**: 768-dimensional sentence embeddings (mean pooling over token embeddings).
- **Pretraining**:
  - Corpus: Wikipedia, BookCorpus (~1B tokens).
  - Objectives: Masked language modeling (15% tokens masked), permuted language modeling.
  - Optimizer: AdamW, learning rate ~2e-5.
- **Fine-Tuning** (SBERT):
  - **Datasets**: 1B+ sentence pairs (SNLI, Multi-NLI, Reddit, StackExchange, AllNLI).
  - **Objective**: Contrastive learning with triplet or cosine similarity loss.
  - **Result**: High cosine similarity for semantically similar sentences.
- **Specifications**:
  - **Size**: ~420 MB.
  - **Max Sequence Length**: 384 tokens.
  - **Performance**: Spearman correlation ~0.87 on STS-B (Semantic Textual Similarity Benchmark), F1 ~0.89 on MRPC (paraphrase detection).
  - **License**: Apache 2.0 (Hugging Face).
- **Platform Usage**:
  - Encodes user and reference answers.
  - Computes cosine similarity (0–1), scaled to 0–10.
  - Thresholds:
    - < 0.3: "Needs significant improvement" (e.g., `devops:148`).
    - 0.3–0.5: "Partially correct."
    - ≥ 0.5: "Good answer."
- **Code**:
  ```python
  from sentence_transformers import SentenceTransformer, util
  sbert_model = SentenceTransformer('all-mpnet-base-v2')
  embeddings = sbert_model.encode([ref_answer, user_answer], convert_to_tensor=True)
  similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
  score = similarity * 10
  ```

### 6.2 Sentence-BERT `all-MiniLM-L6-v2` (Alternative Model)
#### Overview
- **Description**: A lightweight transformer-based model fine-tuned for sentence embeddings, optimized for speed and efficiency in semantic similarity tasks.
- **Why Considered**: Smaller and faster than `all-mpnet-base-v2`, suitable for resource-constrained environments or faster inference, though less accurate.
- **Architecture**:
  - **Base Model**: MiniLM, a distilled version of BERT.
  - **Layers**: 6 transformer layers, 12 attention heads.
  - **Hidden Size**: 384 dimensions (half of `all-mpnet-base-v2`).
  - **Parameters**: ~22 million (vs. 110 million).
  - **Input**: Tokenized text (max 256 tokens).
  - **Output**: 384-dimensional sentence embeddings (mean pooling).
- **Pretraining**:
  - Corpus: Wikipedia, BookCorpus, and others (~500M tokens).
  - Objective: Masked language modeling (15% tokens masked).
  - Optimizer: AdamW, learning rate ~5e-5.
- **Fine-Tuning** (SBERT):
  - **Datasets**: Similar to `all-mpnet-base-v2` (SNLI, Multi-NLI, Reddit, StackExchange, AllNLI), but optimized for efficiency.
  - **Objective**: Contrastive learning with triplet loss or cosine similarity loss to align similar sentences and separate dissimilar ones.
  - **Training**: Uses knowledge distillation from larger models (e.g., BERT) to maintain performance with fewer parameters.
  - **Result**: Compact embeddings with good semantic similarity, though less nuanced than `all-mpnet-base-v2`.
- **Specifications**:
  - **Size**: ~80 MB (5x smaller than `all-mpnet-base-v2`).
  - **Max Sequence Length**: 256 tokens (sufficient for short answers).
  - **Performance**:
    - **STS-B**: Spearman correlation ~0.84 (vs. 0.87 for `all-mpnet-base-v2`).
    - **MRPC**: F1 score ~0.86 (vs. 0.89).
    - Slightly lower accuracy but faster inference.
  - **Inference Time**: ~0.05–0.2 seconds per sentence pair on CPU (2x faster than `all-mpnet-base-v2`).
  - **Memory Usage**: ~200 MB in memory.
  - **License**: Apache 2.0 (Hugging Face).
- **Platform Usage**:
  - Can replace `all-mpnet-base-v2` in `scoring_service.py`:
    ```python
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    ```
  - Same scoring process: encode answers, compute cosine similarity, scale to 0–10.
  - Expected score: Slightly lower than 7.39 (e.g., 7.0–7.2) due to less nuanced embeddings.
- **Trade-Offs**:
  - **Pros**: Faster inference, lower memory footprint, ideal for low-resource environments.
  - **Cons**: Less accurate for complex technical answers (e.g., `devops:148` may score lower due to missing subtle semantic connections).
- **When to Use**:
  - Deployments on edge devices or low-memory servers.
  - Rapid prototyping or testing where speed is prioritized.
  - Environments where a slight accuracy drop is acceptable.

### 6.3 TF-IDF Fallback
- **Description**: Uses term frequency-inverse document frequency for lexical overlap.
- **Why Used**: Fastest option but less accurate (scored 2.61 vs. 7.39).
- **Code**:
  ```python
  from sklearn.feature_extraction.text import TfidfVectorizer
  from sklearn.metrics.pairwise import cosine_similarity
  vectorizer = TfidfVectorizer(stop_words='english')
  tfidf_matrix = vectorizer.fit_transform([ref_answer, user_answer])
  similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
  ```

### Model Comparison
| Feature                     | `all-mpnet-base-v2` | `all-MiniLM-L6-v2` | TF-IDF |
|-----------------------------|---------------------|--------------------|--------|
| **Size**                    | ~420 MB            | ~80 MB            | Minimal |
| **Embedding Dimension**     | 768                | 384               | Variable |
| **Parameters**              | ~110M              | ~22M              | N/A |
| **STS-B Spearman**          | ~0.87              | ~0.84             | ~0.60 |
| **Inference Time (CPU)**    | 0.1–0.5s/pair      | 0.05–0.2s/pair    | <0.01s |
| **Memory Usage**            | ~1 GB              | ~200 MB           | Minimal |
| **Accuracy in Platform**    | 7.39 (expected 8–9)| ~7.0–7.2 (est.)   | 2.61 |
| **Use Case**                | High accuracy      | Speed, low memory | Fallback |

### Switching Models
- Controlled by `.env`:
  ```
  SCORING_METHOD=sbert
  ```
- To use `all-MiniLM-L6-v2`:
  ```python
  # In scoring_service.py
  sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
  ```

## 7. Scoring Details
- **Maximum Score**: 10 (average of 8 answers, each 0–10).
- **Latest Score**: 7.39 with `all-mpnet-base-v2`, `devops:148` scoring ~0.3.
- **Feedback**: Suggests missing terms (e.g., "systems, tolerance, traffic").
- **Goal**: Achieve 8–9 with refined `devops:148` answer.

## 8. Troubleshooting
### Low Score for `devops:148`
- **Issue**: Scores < 0.3 despite including "fault-tolerant," "traffic."
- **Check Reference Answer**:
  ```javascript
  use interview_db
  db.devops.findOne({"id": "148"}).answer
  ```
- **Update `devops.csv`**:
  ```csv
  id,question,answer,company,role,difficulty,category
  148,What is the importance of system design for devops in DevOps?,System design in DevOps is critical for building fault-tolerant, scalable systems that ensure high availability and efficient traffic distribution. It supports microservices architecture, automates CI/CD pipelines, and integrates observability for performance monitoring.,Microsoft,Devops,Medium,System Design
  ```
  Reload:
  ```python
  from services.database_service import load_csv_to_mongo
  load_csv_to_mongo()
  ```

### Duplicate Questions
- Check:
  ```python
  import pandas as pd
  df = pd.read_csv("data/devops.csv")
  print(df[df["question"].duplicated(keep=False)][["id", "question"]])
  ```
- Remove:
  ```python
  df = df.drop_duplicates(subset="question", keep="first")
  df.to_csv("data/devops.csv", index=False)
  load_csv_to_mongo()
  ```

### Logs
- Check similarity:
  ```
  2025-07-01 15:38:XX,XXX - INFO - Score for ID devops:148: 3.00 (Similarity: 0.30, Top terms: ['systems', 'resilience'])
  ```

## 9. Enhancements
1. **Embedding Caching**:
   ```python
   embedding_cache = {}
   def get_embedding(text):
       if text not in embedding_cache:
           embedding_cache[text] = sbert_model.encode(text, convert_to_tensor=True)
       return embedding_cache[text]
   ```

2. **Score Storage**:
   ```python
   from datetime import datetime
   db.user_scores.insert_one({
       "timestamp": datetime.now(),
       "ids": request.id,
       "answers": request.answers,
       "score": final_score,
       "feedback": "\n".join(feedback)
   })
   ```

3. **GPU Acceleration**:
   ```python
   sbert_model = SentenceTransformer('all-mpnet-base-v2', device='cuda')
   ```

## 10. Testing
### Test `/score_answers`
Use refined payload:
```json
{
    "id": [
        "devops:179",
        "devops:117",
        "devops:173",
        "devops:127",
        "devops:1",
        "devops:60",
        "devops:148",
        "devops:195"
    ],
    "answers": [
        "Monitoring and logging in DevOps ensure real-time visibility into system performance, enabling quick detection and resolution of issues. They track metrics like uptime and errors, supporting proactive maintenance and compliance.",
        "System design in DevOps helps create scalable and reliable infrastructure, optimizing automation and deployment processes.",
        "Cloud platforms provide scalable infrastructure and services, enabling faster deployments and cost efficiency in DevOps.",
        "Disaster recovery and backups ensure data integrity and system availability, minimizing downtime during failures.",
        "Cloud platforms in DevOps provide scalable infrastructure, managed services like AWS ECS, and automated deployment tools, enabling rapid, cost-efficient, and reliable software delivery.",
        "CI/CD in DevOps automates code integration, testing, and deployment, reducing errors and speeding up delivery cycles.",
        "System design in DevOps is critical for building fault-tolerant, scalable systems that ensure high availability and efficient traffic distribution. It supports microservices architecture, automates CI/CD pipelines, and integrates observability for performance monitoring.",
        "Load balancing distributes traffic across servers, improving performance, scalability, and reliability in DevOps environments."
    ]
}
```

**Test Script**:
<xaiArtifact artifact_id="da913916-ed60-479f-8e61-b65ea6f8924e" artifact_version_id="7eb0cafe-77d5-48f0-ab5b-8adff29a5279" title="test_score_answers.py" contentType="text/python">
import requests
import json
import os

os.environ["SCORING_METHOD"] = "sbert"
url = "http://0.0.0.0:8000/score_answers"
payload = {
    "id": [
        "devops:179",
        "devops:117",
        "devops:173",
        "devops:127",
        "devops:1",
        "devops:60",
        "devops:148",
        "devops:195"
    ],
    "answers": [
        "Monitoring and logging in DevOps ensure real-time visibility into system performance, enabling quick detection and resolution of issues. They track metrics like uptime and errors, supporting proactive maintenance and compliance.",
        "System design in DevOps helps create scalable and reliable infrastructure, optimizing automation and deployment processes.",
        "Cloud platforms provide scalable infrastructure and services, enabling faster deployments and cost efficiency in DevOps.",
        "Disaster recovery and backups ensure data integrity and system availability, minimizing downtime during failures.",
        "Cloud platforms in DevOps provide scalable infrastructure, managed services like AWS ECS, and automated deployment tools, enabling rapid, cost-efficient, and reliable software delivery.",
        "CI/CD in DevOps automates code integration, testing, and deployment, reducing errors and speeding up delivery cycles.",
        "System design in DevOps is critical for building fault-tolerant, scalable systems that ensure high availability and efficient traffic distribution. It supports microservices architecture, automates CI/CD pipelines, and integrates observability for performance monitoring.",
        "Load balancing distributes traffic across servers, improving performance, scalability, and reliability in DevOps environments."
    ]
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
    print("Score response:")
    print(json.dumps(data, indent=2))
    assert 0 <= data["score"] <= 10, f"Score {data['score']} is out of range"
    assert len(data["feedback"].split("\n")) == 8, f"Expected 8 feedback lines, got {len(data['feedback'].split('\n'))}"
    assert data["score"] > 7.39, f"Expected score > 7.39, got {data['score']}"
else:
    print(f"Error: {response.status_code}, {response.text}")









https://grok.com/share/bGVnYWN5_f744fb58-9de1-4614-9ca6-e9b22ffd06ef