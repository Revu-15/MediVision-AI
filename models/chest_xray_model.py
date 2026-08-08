import os
import sys
import torch
from PIL import Image
import torch.nn.functional as F

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHEXFICIENT_PATH = os.path.join(PROJECT_ROOT, "CheXficient")

sys.path.insert(0, CHEXFICIENT_PATH)

from transformers import (
    AutoModel,
    AutoTokenizer,
    AutoImageProcessor
)


class ChestXRayModel:

    def __init__(self):

        print("Loading Chest X-ray Model...")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Device : {self.device}")

        if os.path.exists(CHEXFICIENT_PATH) and os.path.exists(os.path.join(CHEXFICIENT_PATH, "config.json")):
            self.repo_id = CHEXFICIENT_PATH
        else:
            print("[INFO] Local CheXficient files not found. Using Hugging Face 'StanfordAIMI/CheXficient'...")
            self.repo_id = "StanfordAIMI/CheXficient"

        self.model = AutoModel.from_pretrained(
            self.repo_id,
            trust_remote_code=True
        ).to(self.device)

        print("[OK] Model Loaded Successfully")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.repo_id,
            trust_remote_code=True
        )

        print("[OK] Tokenizer Loaded Successfully")

        self.image_processor = AutoImageProcessor.from_pretrained(
            self.repo_id,
            trust_remote_code=True
        )

        print("[OK] Image Processor Loaded Successfully")

        self.model.eval()

        print("[OK] Chest X-ray Model Ready")


    def predict(self, image_path):

        image = Image.open(image_path).convert("RGB")

        labels = [
    "Normal chest X-ray",
    "Pneumonia",
    "Tuberculosis",
    "COVID-19",
    "Pleural Effusion",
    "Pneumothorax",
    "Cardiomegaly",
    "Atelectasis",
    "Pulmonary Edema",
    "Lung Opacity",
    "Pulmonary Fibrosis",
    "Lung Mass",
    "Lung Nodule"
]

        image_inputs = self.image_processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        text_inputs = self.tokenizer(
            labels,
            padding=True,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():

            outputs = self.model(
                pixel_values=image_inputs["pixel_values"],
                text_tokens=text_inputs
            )

        logits = outputs["logits_per_image"]

        probabilities = F.softmax(logits, dim=-1)

        scores = probabilities.squeeze().tolist()

        all_scores = {}

        for label, score in zip(labels, scores):
            all_scores[label] = round(score * 100, 2)

        sorted_predictions = sorted(
            all_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_predictions = sorted_predictions[:3]

        best_prediction = top_predictions[0][0]

        return {
            "prediction": best_prediction,
            "confidence": top_predictions[0][1],
            "top_predictions": top_predictions,
            "all_scores": all_scores
        }