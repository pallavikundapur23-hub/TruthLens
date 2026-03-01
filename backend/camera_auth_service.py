"""
👩‍💻 PERSON 2: Camera Fingerprint & Forensics Service
This module extracts PRNU fingerprints and verifies camera authenticity.
"""

import numpy as np
from PIL import Image
from typing import Dict, Optional
import hashlib
import io

# ============================================================================
# CORE PRNU & AUTHENTICITY ANALYSIS
# ============================================================================

def extract_prnu(image_path: str) -> Dict:
    """
    Extract PRNU fingerprint from image.
    PRNU (Photo Response Non-Uniformity) is the unique noise from camera sensor.
    AI-generated images lack this pattern.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img, dtype=np.float32)
        
        # Extract luminance component
        gray = np.dot(img_array[...,:3], [0.299, 0.587, 0.114])
        
        # High-pass filter to isolate noise
        from scipy import ndimage
        blurred = ndimage.gaussian_filter(gray, sigma=2)
        noise = gray - blurred
        
        # Calculate statistics
        entropy = float(np.abs(noise).sum())
        consistency = float(np.std(noise))
        energy = float(np.square(noise).sum())
        
        return {
            "prnu_detected": entropy > 50,
            "entropy": round(entropy, 2),
            "consistency": round(consistency, 2),
            "energy": round(energy, 2),
            "fingerprint_strength": "strong" if entropy > 200 else "moderate" if entropy > 50 else "weak"
        }
    except Exception as e:
        return {"error": str(e), "prnu_detected": False}

    # AI penalty
    ai_probability = float(ai_check.get("ai_probability", 0.5))

    # Boost AI probability if metadata missing
    if metadata.get("metadata_status") == "missing":
        ai_probability += 0.2

    # Boost if PRNU weak
    if not prnu.get("prnu_detected"):
        ai_probability += 0.2

    ai_probability = max(0.0, min(1.0, ai_probability))
    score -= 0.3 * ai_probability

    # Clamp to [0,1]
    score = max(0.0, min(1.0, score))

    return float(score)


def check_metadata(image_path: str) -> Dict:
    """
    📋 Analyze EXIF metadata for tampering or anomalies.
    AI images often have missing or suspicious metadata.
    """
    try:
        from PIL.Image import Image as PILImage
        img = Image.open(image_path)
        exif = img._getexif() if hasattr(img, '_getexif') else {}
        
        has_exif = bool(exif)
        has_camera_info = False
        has_timestamp = False
        
        if exif:
            has_camera_info = any(k in exif for k in [271, 272])  # Make, Model
            has_timestamp = 306 in exif  # DateTime
        
        return {
            "metadata_status": "valid" if has_exif else "missing",
            "has_exif": has_exif,
            "has_camera_info": has_camera_info,
            "has_timestamp": has_timestamp,
            "exif_tags_count": len(exif) if exif else 0
        }
    except Exception as e:
        return {
            "metadata_status": "unknown",
            "error": str(e)
        }


def detect_synthetic(image_path: str) -> Dict:
    """
    🤖 Detect AI-generated images using frequency analysis.
    AI images have characteristic frequency signatures.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img, dtype=np.float32)
        
        # Convert to frequency domain
        from numpy.fft import fft2, fftshift
        gray = np.dot(img_array[...,:3], [0.299, 0.587, 0.114])
        freq = fftshift(fft2(gray))
        freq_magnitude = np.abs(freq)
        
        # Analyze frequency characteristics
        # AI images tend to have different frequency distributions
        low_freq = np.sum(freq_magnitude[:len(freq_magnitude)//4, :])
        high_freq = np.sum(freq_magnitude[-len(freq_magnitude)//4:, :])
        
        # Compute AI probability based on frequency analysis
        freq_ratio = low_freq / (high_freq + 1e-6)
        ai_probability = min(abs(freq_ratio - 10) / 20, 1.0)  # Heuristic
        
        return {
            "ai_probability": round(ai_probability, 3),
            "low_freq_energy": round(low_freq, 2),
            "high_freq_energy": round(high_freq, 2),
            "likely_synthetic": ai_probability > 0.6
        }
    except Exception as e:
        return {
            "ai_probability": 0.5,
            "error": str(e)
        }


def check_authenticity(image_path: str) -> Dict:
    """
    🔐 Complete camera authenticity check.
    Combines PRNU + Metadata + AI detection.
    """
    prnu = extract_prnu(image_path)
    metadata = check_metadata(image_path)
    ai_check = detect_synthetic(image_path)
    
    # Compute unified authenticity score
    base_score = 0.5
    
    if prnu.get("prnu_detected"):
        base_score += 0.3
    
    if metadata.get("has_exif"):
        base_score += 0.2
    
    if ai_check.get("ai_probability", 0) > 0.7:
        base_score -= 0.4
    
    base_score = max(0.0, min(1.0, base_score))
    
    return {
        "camera_authentic": base_score > 0.5,
        "authenticity_score": round(base_score, 3),
        "prnu_analysis": prnu,
        "metadata_analysis": metadata,
        "synthetic_analysis": ai_check,
        "overall_verdict": "AUTHENTIC" if base_score > 0.7 else "SUSPICIOUS" if base_score > 0.4 else "FAKE"
    }


if __name__ == "__main__":
    # Test usage
    # result = check_authenticity("test.jpg")
    # print(result)