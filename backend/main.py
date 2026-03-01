import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from trust_score_engine import TrustScoreEngine, TrustScores

app = FastAPI(title="TruthFlow Prototype - Real / Suspicious / Fake")

trust_engine = TrustScoreEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== TEXT =====================

class TextRequest(BaseModel):
    text: str


def analyze_text_logic(text: str) -> TrustScores:
    text = text.lower()

    fake_keywords = [
        "secretly", "100% guaranteed", "aliens",
        "share immediately", "urgent", "limited offer",
        "click here", "ban all"
    ]

    suspicious_keywords = [
        "breaking news", "might", "could",
        "unconfirmed", "rumor", "viral"
    ]

    real_keywords = [
        "announced", "official", "reported",
        "published", "reserve bank",
        "data shows", "according to"
    ]

    fake_hits = sum(word in text for word in fake_keywords)
    suspicious_hits = sum(word in text for word in suspicious_keywords)
    real_hits = sum(word in text for word in real_keywords)

    if fake_hits > 0:
        return TrustScores(deepfake_score=0.7, fact_score=0.3, source_score=0.2)

    if suspicious_hits > 0:
        return TrustScores(deepfake_score=0.5, fact_score=0.5, source_score=0.5)

    if real_hits > 0:
        return TrustScores(deepfake_score=0.3, fact_score=0.7, source_score=0.8)

    return TrustScores(deepfake_score=0.5, fact_score=0.5, source_score=0.5)


@app.post("/analyze-text")
async def analyze_text(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text required")

    scores = analyze_text_logic(request.text)
    return trust_engine.analyze(scores)


# ===================== IMAGE =====================

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    filename = file.filename.lower()

    if "fake" in filename or "edited" in filename:
        scores = TrustScores(0.7, 0.3, 0.2)

    elif "suspicious" in filename or "viral" in filename:
        scores = TrustScores(0.5, 0.5, 0.5)

    else:
        scores = TrustScores(0.3, 0.7, 0.8)

    return trust_engine.analyze(scores)


# ===================== VIDEO =====================

@app.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    filename = file.filename.lower()

    if "fake" in filename or "deepfake" in filename:
        scores = TrustScores(0.7, 0.3, 0.2)

    elif "viral" in filename or "unverified" in filename:
        scores = TrustScores(0.5, 0.5, 0.5)

    else:
        scores = TrustScores(0.3, 0.7, 0.8)

    return trust_engine.analyze(scores)


@app.get("/")
async def root():
    return {"message": "TruthFlow Prototype Running"}