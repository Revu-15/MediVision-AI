from models.chest_xray_model import ChestXRayModel
from models.eye_disease_model import EyeDiseaseModel
from models.brain_mri_model import BrainMRIModel

class ModelDispatcher:

    def __init__(self):

        # Store model classes only (do NOT create objects here)
        self.model_classes = {
            "Chest X-ray": ChestXRayModel,
            "Eye Fundus": EyeDiseaseModel,
            "Brain MRI": BrainMRIModel
        }

        # Dictionary to store loaded models
        self.loaded_models = {}

    def predict(self, image_type, image_path):

        if image_type not in self.model_classes:
            raise ValueError(f"No model found for {image_type}")

        # Lazy Loading
        if image_type not in self.loaded_models:
            print(f"Loading {image_type} Model...")
            self.loaded_models[image_type] = self.model_classes[image_type]()
            print(f"{image_type} Model Loaded Successfully!")

        return self.loaded_models[image_type].predict(image_path)