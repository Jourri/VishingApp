# Vishing Detection Backend

This backend uses FastAPI, Whisper Small, and a fine-tuned AraBERT model to detect potential voice phishing tactics in Arabic phone conversations.

## Requirements

- Python 3.11
- FFmpeg
- Python dependencies listed in `requirements.txt`
- Trained AraBERT model weights (`model.safetensors`)

## Setup

1. Download or clone the VishingApp repository.
2. Open a terminal in the project root.
3. Create a Python virtual environment:

   `py -3.11 -m venv backend_venv`

4. Install the required libraries:

   `.\backend_venv\Scripts\python.exe -m pip install -r backend\requirements.txt`

5. Download `model.safetensors` from the team's shared Google Drive link and place it inside:

   `backend/models/AraBERT_Model/`

6. Verify that FFmpeg is installed:

   `ffmpeg -version`

## Run the Backend

From the project root, execute:

`.\backend_venv\Scripts\python.exe -m uvicorn backend.app:app --port 8000`

Open the API documentation:

http://127.0.0.1:8000/docs

## Test the API

1. Open `POST /predict`.
2. Click `Try it out`.
3. Upload an MP3 or WAV audio file (maximum 20 MB).
4. Click `Execute`.

The API returns the transcribed Arabic text, detected phishing tactics, individual tactic probabilities, and risk classification.

## Supported Risk Levels

- Normal
- Suspicious
- Highly Suspicious
- Critical

## Model Weights

Google Drive download link: **To be added**

The model weights are required to run the backend. They are not included in the repository because of their file size.
