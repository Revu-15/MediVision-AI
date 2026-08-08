class PromptBuilder:

    def build_image_prompt(
        self,
        disease,
        confidence
    ):

        prompt = f"""
You are an experienced medical AI assistant.

A specialized medical AI model has already predicted the disease.

Predicted Disease:
{disease}

Confidence:
{confidence}%

Do NOT change the predicted disease.

Generate a professional medical report using exactly the following sections:

1. Disease Overview

2. Possible Causes

3. Common Symptoms

4. Risk Factors

5. Possible Complications

6. Recommended Diagnostic Tests

7. General Treatment Information

8. Lifestyle & Precautions

9. Recommended Specialist

10. Medical Disclaimer

The report should be educational and easy to understand.
"""

        return prompt


    def build_symptom_prompt(
        self,
        disease,
        confidence,
        symptoms
    ):

        symptom_text = ", ".join(symptoms)

        prompt = f"""
You are an experienced medical AI assistant.

The disease was predicted using patient symptoms.

Predicted Disease:
{disease}

Confidence:
{confidence}%

Patient Symptoms:
{symptom_text}

Generate a professional medical report.

Also explain how the listed symptoms relate to the predicted disease.

Include:

1. Disease Overview

2. Symptom Explanation

3. Possible Causes

4. Risk Factors

5. Possible Complications

6. Recommended Diagnostic Tests

7. General Treatment Information

8. Lifestyle & Precautions

9. Recommended Specialist

10. Medical Disclaimer
"""

        return prompt