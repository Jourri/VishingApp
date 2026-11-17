
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
import asyncio
import logging

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.ai_pipeline import analyze_audio, load_models


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg",
    ".webm",
    ".mp4"
}

MAX_FILE_SIZE = 20 * 1024 * 1024


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading Whisper and AraBERT models...")
    await asyncio.to_thread(load_models)
    logger.info("AI models loaded successfully.")
    yield


app = FastAPI(
    title="Vishing Detection API",
    description="AI-powered Arabic voice phishing detection using Whisper and AraBERT",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:8100",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:8100"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Vishing Detection API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "FastAPI server is running"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio file format"
        )

    saved_path = UPLOAD_DIR / f"{uuid4().hex}{extension}"
    total_size = 0

    try:
        with saved_path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Audio file exceeds 20 MB"
                    )

                output.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Audio file is empty"
            )

        logger.info("Audio received: %s", saved_path.name)

        result = await asyncio.to_thread(
            analyze_audio,
            saved_path
        )

        result["filename"] = filename
        result["file_size"] = total_size

        logger.info("Audio analysis completed.")

        return result

    except HTTPException:
        raise

    except Exception:
        logger.exception("Audio processing failed")

        raise HTTPException(
            status_code=500,
            detail="Audio analysis failed"
        )

    finally:
        await file.close()
        saved_path.unlink(missing_ok=True)
