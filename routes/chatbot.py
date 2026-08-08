from flask import Blueprint, render_template, request, session

from models.shared_models import report_engine

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    report = session.get("medical_report")

    answer = ""

    if request.method == "POST":

        question = request.form.get("question")

        answer = report_engine.medical_chat(
            report,
            question
        )

    return render_template(
        "chatbot.html",
        report=report,
        answer=answer
    )