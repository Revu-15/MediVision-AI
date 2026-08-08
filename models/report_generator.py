class ReportGenerator:

    def generate(self, image_type, prediction_result):

        if image_type == "Chest X-ray":
            return self.generate_chest_report(prediction_result)

        elif image_type == "Eye Fundus":
            return self.generate_eye_report(prediction_result)

        elif image_type == "Brain MRI":
            return self.generate_brain_report(prediction_result)

        elif image_type == "Skin Disease":
            return self.generate_skin_report(prediction_result)

        else:
            return {
                "image_type": image_type,
                "predicted_condition": "Unsupported Image",
                "confidence": 0,
                "summary": "No report generator is available for this image type.",
                "severity": "Unknown",
                "recommendation": "Please upload a supported medical image."
            }

    # ---------------- Chest X-ray ----------------

    def generate_chest_report(self, prediction_result):

        disease = prediction_result["prediction"]
        confidence = prediction_result["confidence"]

        if confidence >= 90:
            confidence_level = "Very High"
        elif confidence >= 75:
            confidence_level = "High"
        elif confidence >= 60:
            confidence_level = "Moderate"
        else:
            confidence_level = "Low"

        report = {
            "image_type": "Chest X-ray",
            "predicted_condition": disease,
            "confidence": confidence,
            "confidence_level": confidence_level,
            "summary": "",
            "severity": "",
            "recommendation": ""
        }

        if disease == "Normal chest X-ray":

            report["summary"] = (
                "The chest X-ray appears normal. No obvious abnormalities were detected."
            )
            report["severity"] = "Low"
            report["recommendation"] = (
                "No immediate medical action is required. Consult a physician if symptoms persist."
            )

        elif disease == "Pneumonia":

            report["summary"] = (
                "The AI detected findings suggestive of pneumonia."
            )
            report["severity"] = "High"
            report["recommendation"] = (
                "Consult a physician promptly for evaluation and treatment."
            )

        elif disease == "Tuberculosis":

            report["summary"] = (
                "The AI detected features that may indicate tuberculosis."
            )
            report["severity"] = "High"
            report["recommendation"] = (
                "Medical evaluation and confirmatory laboratory testing are strongly recommended."
            )

        else:

            report["summary"] = (
                f"The AI prediction suggests {disease}."
            )
            report["severity"] = "Moderate"
            report["recommendation"] = (
                "Please consult a radiologist for confirmation."
            )

        return report

    # ---------------- Eye Disease ----------------

    def generate_eye_report(self, prediction_result):

        return {
            "image_type": "Eye Fundus",
            "predicted_condition": prediction_result["prediction"],
            "confidence": prediction_result["confidence"],
            "summary": f"The AI model detected {prediction_result['prediction']} from the retinal image.",
            "severity": "Moderate",
            "recommendation": "Consult an ophthalmologist for detailed eye examination."
        }

    # ---------------- Brain MRI ----------------

    def generate_brain_report(self, prediction_result):

        disease = prediction_result["prediction"]

        severity = "Moderate"

        if disease != "No Tumor":
            severity = "High"
        else:
            severity = "Low"

        return {
            "image_type": "Brain MRI",
            "predicted_condition": disease,
            "confidence": prediction_result["confidence"],
            "summary": f"The AI model classified the MRI as {disease}.",
            "severity": severity,
            "recommendation": "Consult a neurologist or neurosurgeon for clinical confirmation."
        }

    # ---------------- Skin Disease ----------------

    def generate_skin_report(self, prediction_result):

        disease = prediction_result["prediction"]

        confidence = prediction_result["confidence"]

        if disease == "Melanoma":
            severity = "High"

        elif disease == "Basal Cell Carcinoma":
            severity = "High"

        elif disease == "Actinic Keratosis":
            severity = "Moderate"

        else:
            severity = "Low"

        return {

            "image_type": "Skin Disease",

            "predicted_condition": disease,

            "confidence": confidence,

            "summary": (
                f"The AI model predicts the skin lesion is most consistent with {disease}."
            ),

            "severity": severity,

            "recommendation": (
                "Consult a dermatologist for clinical examination and confirmation. "
                "Do not rely solely on AI predictions for diagnosis."
            )

        }