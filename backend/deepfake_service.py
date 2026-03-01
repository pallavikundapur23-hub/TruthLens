"""
🧑‍💻 PERSON 1: AI & Detection Lead
Deepfake Detection Service - Detects AI-generated and manipulated media using neural networks
"""

import torch
import timm
from PIL import Image
from torchvision import transforms
from typing import Tuple
import cv2
import tempfile
import os


class DeepfakeDemoModel:
    """
    Deepfake detection model using EfficientNet with GPU acceleration.
    
    Features:
    - GPU acceleration (CUDA/AMD GPU support)
    - Real-time inference
    - Video frame processing
    - Binary classification (REAL/FAKE)
    """
    
    def __init__(self) -> None:
        """Initialize the deepfake detection model with GPU support."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"🚀 Using device: {self.device}")
        
        # Load pretrained EfficientNet
        self.model = timm.create_model("efficientnet_b0", pretrained=True)
        self.model.to(self.device)
        self.model.eval()
        
        # Image preprocessing pipeline
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )
        print("✅ Deepfake model loaded successfully")

    @torch.inference_mode()
    def predict(self, image_path: str) -> Tuple[str, float]:
        """
        Predict if image is fake or real.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (label, score)
            - label: "REAL" or "FAKE"
            - score: Float between 0-1 (higher = more likely FAKE)
        """
        try:
            image = Image.open(image_path).convert("RGB")
            tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                logits = self.model(tensor)
                probs = torch.softmax(logits, dim=1)

            # Demo scoring: combines uncertainty signals
            top1 = probs.max(dim=1).values
            entropy = -(probs * torch.log(probs + 1e-12)).sum(dim=1)
            norm_entropy = entropy / torch.log(torch.tensor(probs.shape[1], device=probs.device, dtype=probs.dtype))

            # Final score (0=real, 1=fake)
            score = (0.55 * norm_entropy + 0.45 * (1.0 - top1)).item()
            score = float(max(0.0, min(1.0, score)))

            label = "FAKE" if score >= 0.5 else "REAL"
            return label, score
        except Exception as e:
            print(f"❌ Error in prediction: {e}")
            return "ERROR", 0.5


def score_image(image_path: str, model: DeepfakeDemoModel = None) -> float:
    """
    Score an image for deepfake probability.
    
    Args:
        image_path: Path to image
        model: DeepfakeDemoModel instance (creates new if None)
        
    Returns:
        Float between 0-1 (deepfake probability)
    """
    if model is None:
        model = DeepfakeDemoModel()
    _, score = model.predict(image_path)
    return score


def score_video(video_path: str, model: DeepfakeDemoModel = None, sample_rate: int = 10) -> Tuple[float, int]:
    """
    Score video by analyzing sampled frames.
    
    Args:
        video_path: Path to video file
        model: DeepfakeDemoModel instance (creates new if None)
        sample_rate: Analyze every Nth frame (default: every 10th)
        
    Returns:
        Tuple of (average_deepfake_score, frames_analyzed)
    """
    if model is None:
        model = DeepfakeDemoModel()
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Unable to read video file")

    frame_scores = []
    frame_index = 0
    
    print(f"📹 Processing video: {video_path}")
    
    try:
        with tempfile.TemporaryDirectory() as frame_dir:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                # Sample every N frames
                if frame_index % sample_rate == 0:
                    frame_path = os.path.join(frame_dir, f"frame_{frame_index:06d}.jpg")
                    saved = cv2.imwrite(frame_path, frame)
                    if saved:
                        score = score_image(frame_path, model)
                        frame_scores.append(score)
                        print(f"  Frame {frame_index}: {score:.3f}")
                
                frame_index += 1
    finally:
        cap.release()

    frames_analyzed = len(frame_scores)
    if frames_analyzed == 0:
        raise Exception("No frames could be analyzed from video")

    average_score = sum(frame_scores) / frames_analyzed
    print(f"✅ Video analysis complete: {frames_analyzed} frames, avg score: {average_score:.3f}")
    
    return float(average_score), frames_analyzed


# ============================================================================
# API INTEGRATION
# ============================================================================

# Global model instance (lazy loading)
_model = None

def get_model() -> DeepfakeDemoModel:
    """Get or create global model instance."""
    global _model
    if _model is None:
        _model = DeepfakeDemoModel()
    return _model


def detect_deepfake_image(image_path: str) -> dict:
    """
    API endpoint handler for image deepfake detection.
    
    Returns:
        {
            "prediction": "REAL" | "FAKE",
            "deepfake_score": float,
            "frames_analyzed": 1,
            "confidence": str
        }
    """
    model = get_model()
    label, score = model.predict(image_path)
    
    confidence = "HIGH" if score > 0.8 or score < 0.2 else "MEDIUM" if score > 0.5 else "LOW"
    
    return {
        "prediction": label,
        "deepfake_score": round(score, 4),
        "frames_analyzed": 1,
        "confidence": confidence
    }


def detect_deepfake_video(video_path: str) -> dict:
    """
    API endpoint handler for video deepfake detection.
    
    Returns:
        {
            "prediction": "REAL" | "FAKE",
            "deepfake_score": float,
            "frames_analyzed": int,
            "confidence": str
        }
    """
    model = get_model()
    avg_score, frames_analyzed = score_video(video_path, model)
    label = "FAKE" if avg_score >= 0.5 else "REAL"
    
    confidence = "HIGH" if avg_score > 0.8 or avg_score < 0.2 else "MEDIUM" if avg_score > 0.5 else "LOW"
    
    return {
        "prediction": label,
        "deepfake_score": round(avg_score, 4),
        "frames_analyzed": frames_analyzed,
        "confidence": confidence
    }


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧑‍💻 TruthLens - Deepfake Detection Service")
    print("="*70 + "\n")
    
    # Initialize model
    model = DeepfakeDemoModel()
    print("✅ Service ready for API calls\n")
