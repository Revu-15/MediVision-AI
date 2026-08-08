from models.medical_llm import MedicalLLM


class AIReportEngine:

    def __init__(self):

        # Load Medical LLM only once
        self.llm = MedicalLLM()

    # ----------------------------------------------------
    # Image Diagnosis Report
    # ----------------------------------------------------
    def generate(self, prediction):

        disease = prediction["prediction"]
        confidence = prediction["confidence"]

        report = self.llm.generate_report(
            disease=disease,
            confidence=confidence
        )

        return {
            "prediction": disease,
            "confidence": confidence,
            "report": report
        }

    # ----------------------------------------------------
    # Symptom Diagnosis
    # ----------------------------------------------------
    def predict_from_symptoms(self, symptoms):

        return self.llm.predict_from_symptoms(symptoms)

    # ----------------------------------------------------
    # Chatbot
    # ----------------------------------------------------
    def medical_chat(self, report, question):

        return self.llm.medical_chat(
            report,
            question
        )