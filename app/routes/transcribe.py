# transcribe.py
from fastapi import APIRouter, UploadFile, File, Depends
from ..utils.validations import validate_api_key
from ..models.transcription import TranscriptionData
from ..utils.whisper_service import transcribe_audio

router = APIRouter()

@router.post("/", response_model=TranscriptionData)
async def transcribe(file: UploadFile = File(...), api_key: str = Depends(validate_api_key)):
    file_content = await file.read()
    data = transcribe_audio(file_content)
    return data

