from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class Verdict(str, Enum):
    REAL = "Real"
    SUSPICIOUS = "Suspicious"
    FAKE = "Fake"


@dataclass
class TrustScores:
    deepfake_score: float  # 0 = real, 1 = fake
    fact_score: float      # 0 = false, 1 = true
    source_score: float    # 0 = unreliable, 1 = reliable


class TrustScoreEngine:

    def calculate_final_score(self, scores: TrustScores) -> float:
        # Weighted scoring
        final_score = (
            (1 - scores.deepfake_score) * 0.4 +
            scores.fact_score * 0.4 +
            scores.source_score * 0.2
        )

        return round(max(0.0, min(1.0, final_score)), 3)

    def get_verdict(self, final_score: float) -> Verdict:
        if final_score >= 0.7:
            return Verdict.REAL
        elif final_score >= 0.4:
            return Verdict.SUSPICIOUS
        else:
            return Verdict.FAKE

    def get_confidence(self, final_score: float) -> str:
        distance = abs(final_score - 0.5)

        if distance >= 0.3:
            return "High"
        elif distance >= 0.15:
            return "Medium"
        else:
            return "Low"

    def analyze(self, scores: TrustScores) -> Dict[str, Any]:
        final_score = self.calculate_final_score(scores)
        verdict = self.get_verdict(final_score)
        confidence = self.get_confidence(final_score)

        return {
            "deepfake_score": round(scores.deepfake_score, 3),
            "fact_score": round(scores.fact_score, 3),
            "source_score": round(scores.source_score, 3),
            "final_score": final_score,
            "verdict": verdict.value,
            "confidence": confidence
        }