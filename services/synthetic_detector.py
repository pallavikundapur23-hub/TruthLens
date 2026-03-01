from __future__ import annotations

from typing import Any, Dict

import cv2
import numpy as np


def detect_synthetic(image_path: str) -> Dict[str, Any]:

    try:
        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if gray is None:
            return {
                "ai_probability": 0.5,
                "sharpness_score": 0.0,
                "noise_score": 0.0,
                "fft_score": 0.0,
            }

        # -----------------------------
        # 1️⃣ Sharpness
        # -----------------------------
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness_score = float(laplacian.var())

        # -----------------------------
        # 2️⃣ Noise estimation
        # -----------------------------
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        noise = gray.astype(np.float32) - blurred.astype(np.float32)
        noise_score = float(np.std(noise))

        # -----------------------------
        # 3️⃣ Frequency analysis (FFT)
        # -----------------------------
        fft = np.fft.fft2(gray)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.abs(fft_shift)

        fft_score = float(np.mean(np.log(magnitude + 1)))

        # -----------------------------
        # 4️⃣ AI probability logic
        # -----------------------------
        ai_probability = 0.2

        # Too smooth
        if sharpness_score < 120:
            ai_probability += 0.3

        # Low sensor noise
        if noise_score < 4:
            ai_probability += 0.3

        # AI images often have unnaturally clean frequency spectrum
        if fft_score < 8:
            ai_probability += 0.3

        ai_probability = max(0.0, min(1.0, ai_probability))

        return {
            "ai_probability": float(ai_probability),
            "sharpness_score": sharpness_score,
            "noise_score": noise_score,
            "fft_score": fft_score,
        }

    except Exception:
        return {
            "ai_probability": 0.5,
            "sharpness_score": 0.0,
            "noise_score": 0.0,
            "fft_score": 0.0,
        }