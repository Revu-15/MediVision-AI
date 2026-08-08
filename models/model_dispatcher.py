from models.chest_xray_model import ChestXRayModel
from models.eye_disease_model import EyeDiseaseModel
from models.brain_mri_model import BrainMRIModel
from models.general_medical_model import GeneralMedicalModel

class ModelDispatcher:

    def __init__(self):

        # Store model classes only (do NOT create objects here)
        self.model_classes = {
            "Chest X-ray": ChestXRayModel,
            "Eye Fundus": EyeDiseaseModel,
            "Brain MRI": BrainMRIModel,
            "General Medical Image": GeneralMedicalModel
        }

        # Dictionary to store loaded models
        self.loaded_models = {}

    def predict(self, image_type, image_path, caption=""):

        if image_type not in self.model_classes:
            image_type = "General Medical Image"

        # Lazy Loading
        if image_type not in self.loaded_models:
            print(f"[INFO] Loading {image_type} Model...")
            self.loaded_models[image_type] = self.model_classes[image_type]()
            print(f"[OK] {image_type} Model Loaded Successfully!")

        model_obj = self.loaded_models[image_type]
        if image_type == "General Medical Image":
            return model_obj.predict(image_path, caption=caption)
        return model_obj.predict(image_path)