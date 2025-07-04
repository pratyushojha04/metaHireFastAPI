

# from pymongo import MongoClient
# import pandas as pd
# import os
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Base directory for CSV files (relative to project root)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_DIR = os.path.join(BASE_DIR, "data")

# CSV_FILES = [
#     "backend.csv",
#     "cloud engineer.csv",
#     "data analyst.csv",
#     "devops.csv",
#     "frontend development.csv",
#     "machine learning.csv",
#     "tester.csv"
# ]

# client = MongoClient("mongodb://localhost:27017/")
# db = client["interview_db"]

# def load_csv_to_mongo():
#     """
#     Load each CSV file into a separate MongoDB collection.
#     Normalizes difficulty values to ensure consistency.
#     """
#     for csv_file in CSV_FILES:
#         csv_path = os.path.join(DATA_DIR, csv_file)
#         collection_name = os.path.splitext(csv_file)[0].replace(" ", "_").lower()
#         collection = db[collection_name]

#         if not os.path.exists(csv_path):
#             logger.error(f"File {csv_path} not found")
#             continue

#         try:
#             df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='warn')
#             logger.info(f"Read {len(df)} records from {csv_file}")

#             required_columns = ['id', 'question', 'answer', 'company', 'role', 'difficulty', 'category']
#             if not all(col in df.columns for col in required_columns):
#                 logger.error(f"Skipping {csv_file}: Missing required columns. Found: {list(df.columns)}")
#                 continue

#             # Normalize difficulty values
#             df['difficulty'] = df['difficulty'].str.capitalize()  # Converts 'easy', 'EASY' to 'Easy'
#             df['difficulty'] = df['difficulty'].replace({'Medium': 'Medium', 'Hard': 'Hard', 'Easy': 'Easy'})

#             # Check for duplicate IDs
#             duplicate_ids = df[df['id'].duplicated(keep=False)]['id'].tolist()
#             if duplicate_ids:
#                 logger.warning(f"Duplicate IDs found in {csv_file}: {duplicate_ids}")
#                 df['id'] = df['id'].astype(str) + '_' + df.index.astype(str)

#             # Check for missing or invalid data
#             invalid_rows = df[required_columns].isna().any(axis=1)
#             if invalid_rows.any():
#                 logger.warning(f"Found {invalid_rows.sum()} rows with missing data in {csv_file}: {df[invalid_rows].index.tolist()}")
#                 df = df[~invalid_rows]

#             if len(df) == 0:
#                 logger.error(f"No valid records to insert from {csv_file}")
#                 continue

#             # Clear collection to ensure fresh data
#             collection.drop()
#             logger.info(f"Cleared collection {collection_name} before loading")

#             # Insert records
#             records = df.to_dict('records')
#             inserted_count = 0
#             for record in records:
#                 try:
#                     record['id'] = str(record['id'])
#                     collection.insert_one(record)
#                     inserted_count += 1
#                 except Exception as e:
#                     logger.error(f"Error inserting record with ID {record.get('id', 'unknown')} in {csv_file}: {str(e)}")

#             logger.info(f"Inserted {inserted_count} records from {csv_file} into collection {collection_name}")

#             # Verify collection count
#             collection_count = collection.count_documents({})
#             if collection_count != len(df):
#                 logger.error(f"Mismatch in {collection_name}: Expected {len(df)} documents, found {collection_count}")
#             else:
#                 logger.info(f"Verified {collection_count} documents in {collection_name}")
#         except Exception as e:
#             logger.error(f"Error processing {csv_file}: {str(e)}")

#     logger.info("CSV files loaded to MongoDB successfully.")



# from pymongo import MongoClient
# import pandas as pd
# import os
# import logging
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
# logger = logging.getLogger(__name__)

# # MongoDB connection
# client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
# db = client[os.getenv("MONGO_DB_NAME", "interview_db")]

# # Data directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_DIR = os.path.join(BASE_DIR, os.getenv("DATA_DIR", "data"))

# CSV_FILES = [
#     "backend.csv",
#     "cloud engineer.csv",
#     "data analyst.csv",
#     "devops.csv",
#     "frontend development.csv",
#     "machine learning.csv",
#     "tester.csv"
# ]

# def load_csv_to_mongo():
#     """
#     Load each CSV file into a separate MongoDB collection.
#     Normalizes difficulty values to ensure consistency.
#     """
#     for csv_file in CSV_FILES:
#         csv_path = os.path.join(DATA_DIR, csv_file)
#         collection_name = os.path.splitext(csv_file)[0].replace(" ", "_").lower()
#         collection = db[collection_name]

#         if not os.path.exists(csv_path):
#             logger.error(f"File {csv_path} not found")
#             continue

#         try:
#             df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='warn')
#             logger.info(f"Read {len(df)} records from {csv_file}")

#             required_columns = ['id', 'question', 'answer', 'company', 'role', 'difficulty', 'category']
#             if not all(col in df.columns for col in required_columns):
#                 logger.error(f"Skipping {csv_file}: Missing required columns. Found: {list(df.columns)}")
#                 continue

#             # Normalize difficulty values
#             df['difficulty'] = df['difficulty'].str.capitalize()
#             df['difficulty'] = df['difficulty'].replace({'Medium': 'Medium', 'Hard': 'Hard', 'Easy': 'Easy'})

#             # Check for duplicate IDs
#             duplicate_ids = df[df['id'].duplicated(keep=False)]['id'].tolist()
#             if duplicate_ids:
#                 logger.warning(f"Duplicate IDs found in {csv_file}: {duplicate_ids}")
#                 df['id'] = df['id'].astype(str) + '_' + df.index.astype(str)

#             # Check for missing or invalid data
#             invalid_rows = df[required_columns].isna().any(axis=1)
#             if invalid_rows.any():
#                 logger.warning(f"Found {invalid_rows.sum()} rows with missing data in {csv_file}: {df[invalid_rows].index.tolist()}")
#                 df = df[~invalid_rows]

#             if len(df) == 0:
#                 logger.error(f"No valid records to insert from {csv_file}")
#                 continue

#             # Clear collection
#             collection.drop()
#             logger.info(f"Cleared collection {collection_name} before loading")

#             # Insert records
#             records = df.to_dict('records')
#             inserted_count = 0
#             for record in records:
#                 try:
#                     record['id'] = str(record['id'])
#                     collection.insert_one(record)
#                     inserted_count += 1
#                 except Exception as e:
#                     logger.error(f"Error inserting record with ID {record.get('id', 'unknown')} in {csv_file}: {str(e)}")

#             logger.info(f"Inserted {inserted_count} records from {csv_file} into collection {collection_name}")

#             # Verify collection count
#             collection_count = collection.count_documents({})
#             if collection_count != len(df):
#                 logger.error(f"Mismatch in {collection_name}: Expected {len(df)} documents, found {collection_count}")
#             else:
#                 logger.info(f"Verified {collection_count} documents in {collection_name}")
#         except Exception as e:
#             logger.error(f"Error processing {csv_file}: {str(e)}")

#     logger.info("CSV files loaded to MongoDB successfully.")




from pymongo import MongoClient
import pandas as pd
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client[os.getenv("MONGO_DB_NAME", "interview_db")]

# Data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, os.getenv("DATA_DIR", "data"))

CSV_FILES = [
    "backend.csv",
    "cloud engineer.csv",
    "data analyst.csv",
    "devops.csv",
    "frontend development.csv",
    "machine learning.csv",
    "tester.csv",
    "coding_problem.csv"
]

def load_csv_to_mongo():
    """
    Load each CSV file into a separate MongoDB collection.
    Normalizes difficulty values to ensure consistency.
    """
    for csv_file in CSV_FILES:
        csv_path = os.path.join(DATA_DIR, csv_file)
        collection_name = os.path.splitext(csv_file)[0].replace(" ", "_").lower()
        collection = db[collection_name]

        if not os.path.exists(csv_path):
            logger.error(f"File {csv_path} not found")
            continue

        try:
            df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='warn')
            logger.info(f"Read {len(df)} records from {csv_file}")

            # Define required columns based on CSV type
            if csv_file == "coding_problem.csv":
                required_columns = ['id', 'question', 'problem_description', 'tc1', 'tc2', 'tc3', 'tc4', 'tc5', 'company', 'difficulty', 'category', 'hint']
            else:
                required_columns = ['id', 'question', 'answer', 'company', 'role', 'difficulty', 'category']

            if not all(col in df.columns for col in required_columns):
                logger.error(f"Skipping {csv_file}: Missing required columns. Found: {list(df.columns)}")
                continue

            # Normalize difficulty values
            df['difficulty'] = df['difficulty'].str.capitalize()
            df['difficulty'] = df['difficulty'].replace({'Medium': 'Medium', 'Hard': 'Hard', 'Easy': 'Easy'})

            # Check for duplicate IDs
            duplicate_ids = df[df['id'].duplicated(keep=False)]['id'].tolist()
            if duplicate_ids:
                logger.warning(f"Duplicate IDs found in {csv_file}: {duplicate_ids}")
                df['id'] = df['id'].astype(str) + '_' + df.index.astype(str)

            # Check for missing or invalid data
            invalid_rows = df[required_columns].isna().any(axis=1)
            if invalid_rows.any():
                logger.warning(f"Found {invalid_rows.sum()} rows with missing data in {csv_file}: {df[invalid_rows].index.tolist()}")
                df = df[~invalid_rows]

            if len(df) == 0:
                logger.error(f"No valid records to insert from {csv_file}")
                continue

            # Clear collection
            collection.drop()
            logger.info(f"Cleared collection {collection_name} before loading")

            # Insert records
            records = df.to_dict('records')
            inserted_count = 0
            for record in records:
                try:
                    record['id'] = str(record['id'])
                    collection.insert_one(record)
                    inserted_count += 1
                except Exception as e:
                    logger.error(f"Error inserting record with ID {record.get('id', 'unknown')} in {csv_file}: {str(e)}")

            logger.info(f"Inserted {inserted_count} records from {csv_file} into collection {collection_name}")

            # Verify collection count
            collection_count = collection.count_documents({})
            if collection_count != len(df):
                logger.error(f"Mismatch in {collection_name}: Expected {len(df)} documents, found {collection_count}")
            else:
                logger.info(f"Verified {collection_count} documents in {collection_name}")
        except Exception as e:
            logger.error(f"Error processing {csv_file}: {str(e)}")

    logger.info("CSV files loaded to MongoDB successfully.")