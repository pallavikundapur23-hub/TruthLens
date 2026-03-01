import torch
import timm
from PIL import Image
from torchvision import transforms
from typing import Tuple


class DeepfakeDemoModel:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = timm.create_model("efficientnet_b0", pretrained=True)
        self.model.to(self.device)
        self.model.eval()
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

    @torch.inference_mode()
    def predict(self, image_path: str) -> Tuple[str, float]:
        image = Image.open(image_path).convert("RGB")
        tensor = self.transform(image).unsqueeze(0).to(self.device)

        logits = self.model(tensor)
        probs = torch.softmax(logits, dim=1)

        # Demo-only score (not true deepfake detection): combines uncertainty signals
        # to produce a usable 0..1 score that can map to REAL/FAKE in demos.
        top1 = probs.max(dim=1).values
        entropy = -(probs * torch.log(probs + 1e-12)).sum(dim=1)
        norm_entropy = entropy / torch.log(torch.tensor(probs.shape[1], device=probs.device, dtype=probs.dtype))

        score = (0.55 * norm_entropy + 0.45 * (1.0 - top1)).item()
        score = float(max(0.0, min(1.0, score)))

        label = "FAKE" if score >= 0.5 else "REAL"
        return label, score