from __future__ import annotations

from typing import Any, Dict

import cv2
import numpy as np


def extract_prnu(image_path: str) -> Dict[str, Any]:
    """
    Simple camera fingerprint (PRNU-like) extraction using a noise residual.

    Steps:
      1. Load image using cv2.imread
      2. Convert to grayscale
      3. Apply Gaussian blur (denoise)
      4. Subtract blurred image from grayscale to get noise residual
      5. Compute noise strength as the standard deviation of the residual

    Returns a dictionary:
      - prnu_detected: bool
      - noise_score: float
    """
    try:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            # Missing or unreadable file
            return {
                "prnu_detected": False,
                "noise_score": 0.0,
            }

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Gaussian blur to obtain a smoothed (denoised) version
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Noise residual: original - blurred
        residual = gray.astype(np.float32) - blurred.astype(np.float32)

        # Noise strength as standard deviation
        noise_score = float(np.std(residual))

        # Simple heuristic: any non-trivial noise is treated as PRNU present.
        # Threshold is arbitrary for demo purposes and can be tuned.
        prnu_detected = noise_score > 5

        return {
            "prnu_detected": prnu_detected,
            "noise_score": noise_score,
        }
    except Exception:
        # Fail-safe: never raise from this helper in demo context.
        return {
            "prnu_detected": False,
            "noise_score": 0.0,
        }

