from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import logging
import os

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.info("Starting api_moodtrip.py")

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"

app = FastAPI()
log.info("✅ FastAPI app created")

class MoodTripRequest(BaseModel):
    user_input: str
    top_k: int = 3
    llm_model: Optional[str] = None

@app.get("/")
def root():
    return {"status": "TripMood API running"}

@app.post("/trip-suggestions")
def trip_suggestions(request: MoodTripRequest):
    log.info(f"Request received: {request.user_input}")
    
    try:
        from src.api.generate_trip_suggestions_api import generate_trip_suggestions_api
        log.info("✅ generate_trip_suggestions_api imported")
        
        result = generate_trip_suggestions_api(
            user_input=request.user_input,
            top_k=request.top_k,
            llm_model=request.llm_model
        )
        log.info("✅ Trip suggestions generated")
        return result
        
    except Exception as e:
        log.error(f"❌ Error in generate_trip_suggestions_api: {str(e)}")
        return {"error": f"API failed: {str(e)}"}
