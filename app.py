from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# استيراد دالة الذكاء الاصطناعي من ملف النماذج المنفصل
from ai_model import process_vishing_audio

app = FastAPI(title="Vishing Detection API - Stage 5", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Stage 5 AI Integrated Vishing Detection Backend is running!"}

@app.post("/predict")
async def predict_vishing(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        analysis_result = process_vishing_audio(temp_file_path, file.filename)
        return analysis_result

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)