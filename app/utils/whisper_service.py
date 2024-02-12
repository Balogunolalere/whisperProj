# whisper_service.py
from faster_whisper import WhisperModel
import time
import logging
import tempfile
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_size = "medium.en"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(file):
    start_time = time.time()  # Measure starting time
    logger.info(f"Transcription started at {start_time}")

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_name = temp_file.name

    # Save the uploaded file to the temporary file
    with open(temp_file_name, "wb") as buffer:
        buffer.write(file)

    segments, info = model.transcribe(temp_file_name, beam_size=5)

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

    # Delete the temporary file
    os.remove(temp_file_name)

    return data
