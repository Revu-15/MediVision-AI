import torch
import timm
import json
import torch.nn.functional as F

from PIL import Image
from torchvision import transforms


class SkinDiseaseModel:

    def __init__(self):

        with open("SkinDisease/config.json", "r") as f:
            self.config = json.load(f)

        with open("SkinDisease/labels.json", "r") as f:
            self.labels = json.load(f)

        self.classes = self.config["classes"]
        self.img_size = self.config["image_size"]

        self.device = torch.device("cpu")

        self.model = timm.create_model(
            self.config["model_name"],
            pretrained=False,
            num_classes=self.config["num_classes"]
        )

        self.model.load_state_dict(
            torch.load(
                "SkinDisease/best_model_final.pth",
                map_location=self.device
            )
        )

        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=self.config["normalization"]["mean"],
                std=self.config["normalization"]["std"]
            )
        ])

        print("✅ Skin Disease Model Loaded Successfully!")

    def predict(self, image_path):

        image = Image.open(image_path).convert("RGB")

        tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            probabilities = F.softmax(
                self.model(tensor),
                dim=1
            )[0]

        probabilities = probabilities.cpu().numpy()

        predicted_index = probabilities.argmax()

        prediction = self.labels.get(
            self.classes[predicted_index],
            self.classes[predicted_index]
        )

        confidence = float(probabilities[predicted_index]) * 100

        all_scores = {
            self.labels.get(cls, cls):
            round(float(score) * 100, 2)
            for cls, score in zip(self.classes, probabilities)
        }

        top_predictions = sorted(
            all_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "top_predictions": top_predictions,
            "all_scores": all_scores
        }