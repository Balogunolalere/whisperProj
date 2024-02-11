from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from faster_whisper import WhisperModel
import time
import json
import secrets
import logging
from pydantic import BaseModel, Field
from typing import List



app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Segment(BaseModel):
    start: float = Field(..., gt=0)
    end: float = Field(..., gt=0)
    text: str

class TranscriptionData(BaseModel):
    language: str
    language_probability: float = Field(..., gt=0, lt=1)
    segments: List[Segment]
    execution_time: float = Field(..., gt=0)

# Load valid API keys from JSON file (replace with your actual storage)
with open("api_keys.json") as f:
    valid_api_keys = set(json.load(f)["keys"])

def validate_api_key(api_key: str):
    if api_key in valid_api_keys:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

# Dependency to get the validated API key
def get_api_key(api_key: str = Depends(validate_api_key)):
    return api_key

model_size = "medium.en"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

@app.post("/create_api_key")
async def create_api_key():
    new_key = secrets.token_urlsafe(32)  # Generate a new key
    valid_api_keys.add(new_key)  # Add the new key to the set of valid keys

    # Write the updated set of keys back to the JSON file
    with open("api_keys.json", "w") as f:
        json.dump({"keys": list(valid_api_keys)}, f)

    return {"api_key": new_key}

@app.delete("/revoke_api_key")
async def revoke_api_key(api_key: str):
    if api_key in valid_api_keys:
        valid_api_keys.remove(api_key)  # Remove the key from the set of valid keys

        # Write the updated set of keys back to the JSON file
        with open("api_keys.json", "w") as f:
            json.dump({"keys": list(valid_api_keys)}, f)

        return {"detail": "API key revoked"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

@app.post("/transcribe", response_model=TranscriptionData)
async def transcribe(file: UploadFile = File(...), api_key: str = Depends(get_api_key)):
    start_time = time.time()  # Measure starting time
    logger.info(f"Transcription started at {start_time}")

    # Save the uploaded file
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    segments, info = model.transcribe(file.filename, beam_size=5)

    # Create a dictionary to store data
    data = {"language": info.language,
            "language_probability": info.language_probability,
            "segments": []}

    for segment in segments:
        data["segments"].append({"start": segment.start,
                                 "end": segment.end,
                                 "text": segment.text})

    end_time = time.time()  # Measure ending time
    logger.info(f"Transcription ended at {end_time}")

    data["execution_time"] = end_time - start_time

    return data

@app.get("/validate_api_key")
async def validate_key(api_key: str):
    key = validate_api_key(api_key)
    # If the key is valid, the function will return True else it will raise an exception
    if key:
        return {"detail": "API key is valid"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

@app.get("/health")
async def health_check():
    return {"status": "OK"}