# Echo stt

This is a transcription service built with FastAPI and the Whisper ASR model.

## Features

- User Authentication: Users can create and revoke API keys for accessing the service.
- Audio Transcription: Users can upload audio files for transcription.
- Transcription History: Users can retrieve their past transcriptions.

## Project Structure

├── api_keys.json
├── app
│   ├── database
│   ├── models
│   │   ├── segment.py
│   │   └── transcription.py
│   ├── routes
│   │   ├── api_keys.py
│   │   └── transcribe.py
│   └── utils
│       ├── validations.py
│       └── whisper_service.py
├── main.py
├── README.md
└── transcription.json


## Setup

1. Clone the repository.
2. Install the dependencies using pip: `pip install -r requirements.txt`
3. Run the application: `uvicorn main:app --reload`

## Usage

1. Create an API key: `POST /create_api_key`
2. Use the API key to transcribe an audio file: `POST /transcribe`

## TODO

1. **User Authentication**
2. **Rate Limiting**
3. **Transcription History**
4. **Multiple Transcription Models**
5. **Webhooks**
6. **Real-time Transcription**
7. **Language Selection**
8. **Error Handling and Reporting**
9. **Health Check**

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
