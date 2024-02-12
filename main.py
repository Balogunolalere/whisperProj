# main.py
from fastapi import FastAPI
from app.routes.transcribe import router as TranscribeRouter
from app.routes.api_keys import router as ApiKeysRouter
app = FastAPI()

app.include_router(TranscribeRouter, prefix='/transcribe', tags=['transcribe route'])
app.include_router(ApiKeysRouter, prefix='/key', tags=['validate keys'])

