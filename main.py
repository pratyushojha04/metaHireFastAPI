from fastapi import FastAPI
from api import routes
from services.database_service import load_csv_to_mongo
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI()

# Include API routes
app.include_router(routes.router)

# Load CSV data into MongoDB at startup
@app.on_event("startup")
async def startup_event():
    logger.info("Loading CSV data into MongoDB...")
    load_csv_to_mongo()
    logger.info("Application startup complete.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)