from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from src.api.generate_trip_suggestions_api import generate_trip_suggestions_api
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
import torch
torch.cuda.empty_cache()  # If using GPU models

app = FastAPI()

class MoodTripRequest(BaseModel):
    user_input: str
    top_k: int=3
    llm_model: Optional[str] = None

@app.post("/trip-suggestions")
def trip_suggestions(request: MoodTripRequest):
    return generate_trip_suggestions_api(
        user_input = request.user_input,
        top_k = request.top_k,
        llm_model = request.llm_model
    )

# Health check for Render
@app.get("/")
def root():
    return {"status": "TripMood API running"}