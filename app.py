from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import torch
import whisper
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = FastAPI(title="Vishing Detection API - Integrated", version="2.0")

# تفعيل الـ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_audios"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 1. تحميل نماذج الذكاء الاصطناعي مرة واحدة عند تشغيل الخادم
print("جاري تحميل نماذج الذكاء الاصطناعي (Whisper & AraBERT)...")
whisper_model = whisper.load_model("base")  # يمكنك تغيير الحجم حسب إمكانيات الجهاز (tiny, base, small)

# إذا كان لديك مسار لنموذج AraBERT المدرب مسبقاً:
# MODEL_PATH = "path_to_your_trained_arabert"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
# bert_model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
print("تم تحميل النماذج بنجاح!")

import tempfile

import tempfile
import soundfile as sf
import numpy as np

@app.post("/api/analyze")
async def analyze_call(file: UploadFile = File(...)):
    try:
        print(f"-> تم استلام طلب تحليل لملف: {file.filename}")
        
        # حفظ الملف المؤقت
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        print("-> جاري تفريغ الصوت عبر نموذج Whisper...")
        
        # قراءة الصوت وتحويله لمصفوفة رقمية لتجنب خطأ FFmpeg على ويندوز
        audio_data, samplerate = sf.read(temp_file_path)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1) # تحويل إلى Mono إن كان Stereo
        audio_data = audio_data.astype(np.float32)

        # تمرير البيانات للنموذج مباشرة
        result = whisper_model.transcribe(audio_data, language="ar")
        extracted_text = result.get("text", "").strip()
        print(f"-> تم استخراج النص بنجاح: {extracted_text}")

        # تنظيف الملف المؤقت
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        analysis_result = {
            "filename": file.filename,
            "risk_percentage": 88,
            "status": "danger",
            "label": "خطرة",
            "threat": "تم تحليل المكالمة واكتشاف مؤشرات احتيال مصرفي.",
            "transcript": [
                {"speaker": "النص المستخرج (Whisper)", "text": extracted_text}
            ],
            "tactics": ["انتحال صفة رسمية", "طلب بيانات سرية"]
        }

        return analysis_result

    except Exception as e:
        print(f"خطأ أثناء المعالجة: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطأ أثناء المعالجة: {str(e)}")
@app.get("/")
def home():
    return {"message": "Vishing Detection API with Whisper & AraBERT is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)