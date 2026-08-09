import sys
import os
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, render_template, session, send_from_directory
from routes.upload import upload_bp
from dotenv import load_dotenv
from routes.download import download_bp
from routes.symptoms import symptom_bp
from routes.chatbot import chatbot_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medivision_ai_secret_key_2026")

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
    report = None
    # Load report from JSON file (avoids 4KB session cookie limit)
    report_file = session.get("medical_report_file")
    if report_file:
        report_path = os.path.join("reports", report_file)
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
        except Exception as e:
            print(f"Error reading report file: {e}")
            report = None
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
    app.run(debug=True, use_reloader=False)