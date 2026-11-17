from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI(title="Vishing Detection API", version="1.0")

# تفعيل الـ CORS لتسمح لتطبيق الـ Ionic بالتواصل مع الخادم بلا قيود
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Vishing Detection API is running successfully!"}

@app.post("/predict")
async def predict_vishing(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    response_data = {
        "filename": file.filename,
        "risk_score": 95,
        "threat_level": "Critical",
        "detected_tactic": "طلب رمز التحقق OTP أو البيانات البنكية",
        "transcription": "السلام عليكم معك البنك المركزي يرجى تحديث بياناتك..."
    }

    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    return response_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)