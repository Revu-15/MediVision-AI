from flask import Blueprint, render_template, request

from models.shared_models import report_engine
from flask import session

symptom_bp = Blueprint("symptom", __name__)




@symptom_bp.route("/symptoms", methods=["GET", "POST"])
def symptoms():

    if request.method == "POST":

        symptoms = request.form.get("symptoms")

        # Predict Disease
        prediction = report_engine.predict_from_symptoms(
            symptoms
        )

        disease = prediction["disease"]
        confidence = prediction["confidence"]

        report = report_engine.llm.generate_report(
            disease=disease,
            confidence=confidence
        )

        

        session["medical_report"] = report

        return render_template(
            "symptoms.html",
            symptoms=symptoms,
            prediction=prediction,
            report=report
        )

    return render_template("symptoms.html")