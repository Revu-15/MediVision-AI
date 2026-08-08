import os
import torch
import torch.nn as nn
import torchvision.models as models
import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image
import numpy as np


class EyeDiseaseModel:

    def __init__(self):

        # -------------------------------
        # Device
        # -------------------------------
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # -------------------------------
        # Confidence Threshold
        # -------------------------------
        self.threshold = 25

        # -------------------------------
        # Disease Labels
        # -------------------------------
        self.labels = [
            "DR", "ARMD", "MH", "DN", "MYA", "BRVO", "TSLN", "ERM", "LS", "MS",
            "CSR", "ODC", "CRVO", "TV", "AH", "ODP", "ODE", "ST", "AION", "PT",
            "RT", "RS", "CRS", "EDN", "RPEC", "MHL", "RP", "CWS", "CB", "ODPM",
            "PRH", "MNF", "HR", "CRAO", "TD", "CME", "PTCR", "CF", "VH", "MCA",
            "VS", "BRAO", "PLQ", "HPED", "CL"
        ]

        # -------------------------------
        # Full Disease Names
        # -------------------------------
        self.disease_names = {
            "DR": "Diabetic Retinopathy",
            "ARMD": "Age-Related Macular Degeneration",
            "MH": "Macular Hole",
            "DN": "Drusen",
            "MYA": "Myopia",
            "BRVO": "Branch Retinal Vein Occlusion",
            "TSLN": "Tessellated Fundus",
            "ERM": "Epiretinal Membrane",
            "LS": "Laser Scar",
            "MS": "Myelinated Nerve Fibers",
            "CSR": "Central Serous Retinopathy",
            "ODC": "Optic Disc Cupping",
            "CRVO": "Central Retinal Vein Occlusion",
            "TV": "Tortuous Vessels",
            "AH": "Asteroid Hyalosis",
            "ODP": "Optic Disc Pit",
            "ODE": "Optic Disc Edema",
            "ST": "Silicone Oil",
            "AION": "Anterior Ischemic Optic Neuropathy",
            "PT": "Pathological Tilt",
            "RT": "Retinal Tear",
            "RS": "Retinoschisis",
            "CRS": "Chorioretinal Scar",
            "EDN": "Exudative Disease",
            "RPEC": "RPE Changes",
            "MHL": "Macular Hole Lesion",
            "RP": "Retinitis Pigmentosa",
            "CWS": "Cotton Wool Spots",
            "CB": "Coloboma",
            "ODPM": "Optic Disc Pigmentation",
            "PRH": "Preretinal Hemorrhage",
            "MNF": "Myelinated Nerve Fibers",
            "HR": "Hypertensive Retinopathy",
            "CRAO": "Central Retinal Artery Occlusion",
            "TD": "Tilted Disc",
            "CME": "Cystoid Macular Edema",
            "PTCR": "Post Traumatic Chorioretinal Scar",
            "CF": "Choroidal Fold",
            "VH": "Vitreous Hemorrhage",
            "MCA": "Macroaneurysm",
            "VS": "Vascular Sheathing",
            "BRAO": "Branch Retinal Artery Occlusion",
            "PLQ": "Plaque",
            "HPED": "Hemorrhagic PED",
            "CL": "Choroidal Lesion"
        }

        # -------------------------------
        # Image Transform
        # -------------------------------
        self.transform = A.Compose([
            A.Resize(384, 384),
            A.Normalize(
                mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225)
            ),
            ToTensorV2()
        ])

        # -------------------------------
        # Build Model
        # -------------------------------
        self.model = models.efficientnet_b4(weights=None)

        in_features = self.model.classifier[1].in_features

        self.model.classifier = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(in_features, 45)
        )

        # -------------------------------
        # Load Weights
        # -------------------------------
        model_path = os.path.join("EyeDisease", "pytorch_model.bin")
        if not os.path.exists(model_path):
            print("⏬ Eye Disease model weights not found locally. Downloading from Hugging Face...")
            from huggingface_hub import hf_hub_download
            os.makedirs("EyeDisease", exist_ok=True)
            hf_hub_download(
                repo_id="lebiraja/retinal-disease-classifier",
                filename="pytorch_model.bin",
                local_dir="EyeDisease"
            )
            print("✅ Eye Disease model weights downloaded successfully!")

        checkpoint = torch.load(
            model_path,
            map_location=self.device
        )

        self.model.load_state_dict(checkpoint["model_state_dict"])

        self.model.to(self.device)
        self.model.eval()

        print("✅ Eye Disease Model Loaded Successfully")

    # -----------------------------------------
    # Prediction
    # -----------------------------------------
    def predict(self, image_path):

        image = np.array(
            Image.open(image_path).convert("RGB")
        )

        tensor = self.transform(
            image=image
        )["image"].unsqueeze(0)

        tensor = tensor.to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.sigmoid(logits)[0].cpu().numpy()

        # -----------------------------------------
        # Store Scores
        # -----------------------------------------
        all_scores = {}

        for label, prob in zip(self.labels, probs):

            disease = self.disease_names.get(label, label)

            score = round(float(prob) * 100, 2)

            if score >= 5:
                all_scores[disease] = score

        # If nothing above 5%
        if len(all_scores) == 0:

            return {
                "prediction": "No Significant Retinal Disease Detected",
                "confidence": 0.0,
                "detected_diseases": [],
                "top_predictions": [],
                "all_scores": {}
            }

        # -----------------------------------------
        # Top Predictions
        # -----------------------------------------
        top_predictions = sorted(
            all_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # -----------------------------------------
        # Detected Diseases
        # -----------------------------------------
        detected_diseases = []

        for disease, score in top_predictions:

            if score >= self.threshold:

                detected_diseases.append({
                    "disease": disease,
                    "confidence": score
                })

        # -----------------------------------------
        # Final Prediction
        # -----------------------------------------
        confidence = top_predictions[0][1]

        if confidence >= self.threshold:
            prediction = top_predictions[0][0]
        else:
            prediction = "No Significant Retinal Disease Detected"

        # -----------------------------------------
        # Return Result
        # -----------------------------------------
        return {
            "prediction": prediction,
            "confidence": confidence,
            "detected_diseases": detected_diseases,
            "top_predictions": top_predictions,
            "all_scores": all_scores
        }