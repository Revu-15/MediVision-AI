from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re


class MedicalLLM:

    def __init__(self):

        self.model_name = "Qwen/Qwen2.5-0.5B-Instruct"

        print("Loading Medical LLM...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )

        self.model.eval()

        print("Medical LLM Loaded Successfully!")

    def generate_report(self, disease, confidence):

        prompt = f"""You are a medical information assistant. A diagnostic model has already predicted the disease below. Your ONLY job is to generate an accurate, well-established medical information report about it. Do not question or change the diagnosis, and do not invent facts you are not confident about.

Disease: {disease}
Confidence: {confidence:.2f}%

Rules:
- Return ONLY a single valid JSON object. No markdown, no ```json fences, no text before or after the JSON.
- Use only medically accepted, textbook-level facts about {disease}. If uncertain about a specific detail, use general/standard information rather than fabricating specifics.
- Every list must contain exactly 3 to 5 short items (each a plain string, no numbering).
- "overview" must be 3-4 complete sentences.
- "treatment" must be 4-5 complete sentences.
- Do not leave any field empty.

Example format (structure only, not real content):
{{
  "overview": "Condition X is a ... It typically presents when ... It is commonly caused by ... It affects approximately ...",
  "symptoms": ["Symptom A", "Symptom B", "Symptom C"],
  "causes": ["Cause A", "Cause B", "Cause C"],
  "risk_factors": ["Risk factor A", "Risk factor B", "Risk factor C"],
  "complications": ["Complication A", "Complication B", "Complication C"],
  "diagnostic_tests": ["Test A", "Test B", "Test C"],
  "treatment": "Treatment typically involves ... In more severe cases ... Patients are usually advised to ... Follow-up includes ...",
  "precautions": ["Precaution A", "Precaution B", "Precaution C"],
  "specialist": "Type of specialist",
  "emergency_warning": "Seek immediate care if ...",
  "disclaimer": "This report is AI-generated and is for educational purposes only. Consult a licensed physician for diagnosis and treatment."
}}

Now generate the real JSON report for: {disease}
"""

        messages = [
            {
                "role": "system",
                "content": "You are a careful medical information assistant. You only state well-established medical facts and always return complete, valid JSON with no extra text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1500,
                do_sample=True,
                temperature=0.3,
                top_p=0.85,
                repetition_penalty=1.15,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_ids = outputs[0][inputs["input_ids"].shape[-1]:]

        response = self.tokenizer.decode(
            generated_ids,
            skip_special_tokens=True
        ).strip()

        print("\n================ RAW MODEL OUTPUT ================\n")
        print(response)
        print("\n==================================================\n")

        try:

            match = re.search(r"\{[\s\S]*\}", response)

            if match:
                response = match.group(0)

            report = json.loads(response)

            print("JSON Parsed Successfully")

            required_keys = [
                "overview",
                "symptoms",
                "causes",
                "risk_factors",
                "complications",
                "diagnostic_tests",
                "treatment",
                "precautions",
                "specialist",
                "emergency_warning",
                "disclaimer"
            ]

            list_keys = [
                "symptoms",
                "causes",
                "risk_factors",
                "complications",
                "diagnostic_tests",
                "precautions"
            ]

            for key in required_keys:

                if key not in report:
                    report[key] = [] if key in list_keys else ""

            return report

        except Exception as e:

            print("\nJSON Parsing Failed")
            print(e)

            return {
                "overview": response,
                "symptoms": [],
                "causes": [],
                "risk_factors": [],
                "complications": [],
                "diagnostic_tests": [],
                "treatment": "",
                "precautions": [],
                "specialist": "",
                "emergency_warning": "",
                "disclaimer": "Unable to generate structured medical report."
            }

    def predict_from_symptoms(self, symptoms):

        prompt = f"""You are an experienced physician.

Patient Symptoms:

{symptoms}

Predict the MOST probable disease based only on well-established medical knowledge. Do not guess wildly; if the symptoms are too vague or ambiguous, reflect that honestly in "confidence" and "reasoning".

Return ONLY valid JSON, with no markdown and no text outside the JSON object, in exactly this structure:

{{
    "disease": "most likely disease name",
    "confidence": 0,
    "reasoning": "brief explanation of why this disease fits the symptoms",
    "possible_diseases": ["alternative 1", "alternative 2", "alternative 3"]
}}
"""

        messages = [
            {
                "role": "system",
                "content": "You are a careful medical diagnosis assistant. You always return complete, valid JSON with no extra text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1200,
                do_sample=True,
                temperature=0.2,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated = outputs[0][inputs["input_ids"].shape[-1]:]

        response = self.tokenizer.decode(
            generated,
            skip_special_tokens=True
        ).strip()

        print(response)

        try:

            match = re.search(r"\{[\s\S]*\}", response)

            if match:
                response = match.group()

            return json.loads(response)

        except Exception:

            return {
                "disease": "",
                "confidence": 0,
                "reasoning": response,
                "possible_diseases": []
            }

    def medical_chat(self, report, question):

        prompt = f"""You are MediVision AI.

Medical Report:

{json.dumps(report, indent=2)}

User Question:

{question}

Answer professionally and concisely, using only information consistent with the report above as your primary source. Do not change or contradict the diagnosis in the report.
"""

        messages = [
            {
                "role": "system",
                "content": "You are a professional medical assistant. You answer based on the provided report and do not alter its diagnosis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=400,
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated = outputs[0][inputs["input_ids"].shape[-1]:]

        answer = self.tokenizer.decode(
            generated,
            skip_special_tokens=True
        ).strip()

        return answer