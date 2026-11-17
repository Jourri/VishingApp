
from functools import lru_cache
from pathlib import Path
import re

import torch
import whisper
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = Path(__file__).resolve().parent / "models" / "AraBERT_Model"

LABELS = [
    "Normal",
    "Impersonation",
    "Threat",
    "Urgency",
    "OTP_Request",
    "Payment_Request"
]

SAMPLE_RATE = 16000
CHUNK_SECONDS = 10
THRESHOLD = 0.5


@lru_cache(maxsize=1)
def load_models():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True
    )

    arabert = AutoModelForSequenceClassification.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True
    )

    arabert.to(device)
    arabert.eval()

    whisper_model = whisper.load_model("small", device=device)

    return tokenizer, arabert, whisper_model, device


def clean_arabic_text(text):
    text = re.sub(r"[\u064B-\u065F\u0670]", "", str(text))
    text = text.replace("ـ", "")
    text = re.sub(r"[أإآ]", "ا", text)
    text = text.replace("ى", "ي")
    text = re.sub(r"[^\u0600-\u06FFa-zA-Z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def detect_tactics(text, tokenizer, model, device):
    if not text.strip():
        return [], {}

    text = clean_arabic_text(text)

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=128
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits

    probabilities = torch.sigmoid(logits)[0].cpu().tolist()

    scores = {
        label: round(float(score), 4)
        for label, score in zip(LABELS, probabilities)
    }

    detected = [
        label for label, score in scores.items()
        if score >= THRESHOLD
    ]

    return detected, scores


def analyze_tactic_sequence(tactics_list):
    clean_seq = []

    for tactics in tactics_list:
        for tactic in tactics:
            if tactic == "Normal":
                continue
            if not clean_seq or clean_seq[-1] != tactic:
                clean_seq.append(tactic)

    risk_level = "Normal"
    pattern = "No Suspicious Transition"

    critical = {"OTP_Request", "Payment_Request"}
    suspicious = {"Impersonation", "Threat", "Urgency"}

    if any(t in clean_seq for t in critical):
        if any(t in clean_seq for t in suspicious):
            risk_level = "Critical"
            pattern = "Critical Escalation: Exploitation with Social Engineering"
        else:
            risk_level = "Highly Suspicious"
            pattern = "Direct Financial or Credential Request"

    elif all(t in clean_seq for t in ["Impersonation", "Threat", "Urgency"]):
        risk_level = "Highly Suspicious"
        pattern = "Impersonation -> Threat -> Urgency"

    elif "Impersonation" in clean_seq and (
        "Urgency" in clean_seq or "Threat" in clean_seq
    ):
        risk_level = "Suspicious"
        pattern = "Impersonation -> Urgency / Threat"

    elif "Threat" in clean_seq and "Urgency" in clean_seq:
        risk_level = "Suspicious"
        pattern = "Threat -> Urgency"

    elif any(t in clean_seq for t in suspicious):
        risk_level = "Suspicious"
        pattern = "Single Suspicious Tactic Detected"

    return {
        "sequence_path": " -> ".join(clean_seq) if clean_seq else "Normal",
        "risk_level": risk_level,
        "detected_pattern": pattern
    }


def analyze_audio(audio_path):
    tokenizer, arabert, whisper_model, device = load_models()

    audio = whisper.load_audio(str(audio_path))
    chunk_size = SAMPLE_RATE * CHUNK_SECONDS

    chunks = []
    tactic_sequences = []

    for start in range(0, len(audio), chunk_size):
        chunk = audio[start:start + chunk_size]

        result = whisper_model.transcribe(
            chunk,
            language="ar",
            task="transcribe",
            fp16=(device == "cuda")
        )

        text = result["text"].strip()

        tactics, scores = detect_tactics(
            text, tokenizer, arabert, device
        )

        tactic_sequences.append(tactics)

        chunks.append({
            "start_seconds": round(start / SAMPLE_RATE, 2),
            "end_seconds": round(
                (start + len(chunk)) / SAMPLE_RATE, 2
            ),
            "transcription": text,
            "detected_tactics": tactics,
            "tactic_scores": scores
        })

    risk = analyze_tactic_sequence(tactic_sequences)

    full_text = " ".join(
        chunk["transcription"] for chunk in chunks
    ).strip()

    all_tactics = [
        label for label in LABELS[1:]
        if any(label in chunk["detected_tactics"] for chunk in chunks)
    ]

    return {
        "status": "success",
        "transcribed_text": full_text,
        "detected_tactics": all_tactics,
        "risk_level": risk["risk_level"],
        "detected_pattern": risk["detected_pattern"],
        "sequence_path": risk["sequence_path"],
        "chunks": chunks
    }
