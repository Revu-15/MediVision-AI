import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


class BrainMRIModel:

    def __init__(self):

        self.model = load_model("BrainMRI/model.h5")

        self.class_names = [
            "Glioma Tumor",
            "Meningioma Tumor",
            "No Tumor",
            "Pituitary Tumor"
        ]

    def predict(self, image_path):

        # Load image
        img = image.load_img(
            image_path,
            target_size=(1250, 1250)
        )

        # Convert to array
        img_array = image.img_to_array(img)

        # Normalize
        img_array = img_array / 255.0

        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = self.model.predict(img_array, verbose=0)

        # Convert to probabilities
        probabilities = predictions[0]

        # Top prediction
        predicted_index = np.argmax(probabilities)

        confidence = float(probabilities[predicted_index]) * 100

        prediction = self.class_names[predicted_index]

        # All scores
        all_scores = {
            self.class_names[i]: round(float(probabilities[i]) * 100, 2)
            for i in range(len(self.class_names))
        }

        # Top predictions
        top_predictions = sorted(
            all_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "top_predictions": top_predictions,
            "all_scores": all_scores
        }