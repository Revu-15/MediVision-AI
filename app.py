from flask import Flask, render_template, session, send_from_directory
from routes.upload import upload_bp
import os
from routes.download import download_bp
from routes.symptoms import symptom_bp
from routes.chatbot import chatbot_bp

app = Flask(__name__)
app.secret_key = "medivision_ai_secret_key_2026"

app.config["UPLOAD_FOLDER"] = "uploads"

# Register Routes
app.register_blueprint(chatbot_bp)
app.register_blueprint(symptom_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(download_bp) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/report")
def report_page():
    report = session.get("medical_report")
    return render_template("report.html", report=report)

@app.route("/settings")
def settings_page():
    return render_template("settings.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

if __name__ == "__main__":
    app.run(debug=True)