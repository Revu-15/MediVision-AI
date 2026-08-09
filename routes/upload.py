from flask import Blueprint, render_template, request
from PIL import Image
import os
import time
import json
from flask import session

from models.shared_models import (
    florence,
    router,
    dispatcher,
    report_engine,
    pdf_generator
)
upload_bp = Blueprint("upload", __name__)

# Use absolute paths so files are always found
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files.get("image")

        if not file or file.filename == "":
            return render_template("upload.html", error="No file selected. Please upload a medical image.")

        save_path = os.path.join(UPLOAD_DIR, file.filename)

        try:
            t_start = time.time()
            file.save(save_path)

            image = Image.open(save_path).convert("RGB")
            image.thumbnail((512, 512))

            # Florence Caption
            t0 = time.time()
            caption = florence.generate_caption(image)
            caption = caption["<CAPTION>"]
            t_caption = time.time() - t0

            print("=" * 70)
            print(f"⏱️ Florence-2 Caption ({t_caption:.2f}s): {caption}")

            # Detect Image Type
            image_type = router.detect_image_type(caption)

            print(f"📷 Detected Image Type: {image_type}")

            # Disease Prediction
            t1 = time.time()
            prediction = dispatcher.predict(
                image_type=image_type,
                image_path=save_path,
                caption=caption
            )
            t_predict = time.time() - t1
            print(f"⏱️ Disease Classifier ({t_predict:.2f}s): {prediction}")

            # Medical LLM Report
            t2 = time.time()
            result = report_engine.generate(prediction)
            report = result["report"]
            t_report = time.time() - t2

            t_total = time.time() - t_start
            print("=" * 70)
            print(f"⚡ TOTAL SCAN PROCESSING TIME: {t_total:.2f} seconds")
            print(f"   └─ Caption: {t_caption:.2f}s | Classifier: {t_predict:.2f}s | LLM Report: {t_report:.2f}s")
            print("=" * 70)

            # Save report to JSON file (session cookies are limited to ~4KB)
            # Also include image and prediction metadata so the report page can display them
            timestamp = int(time.time())
            report_json_filename = f"report_{timestamp}.json"
            report_json_path = os.path.join(REPORTS_DIR, report_json_filename)
            try:
                report_data = dict(report)
                report_data["_image_filename"] = file.filename
                report_data["_image_type"] = image_type
                report_data["_caption"] = caption
                report_data["_prediction"] = prediction.get("prediction", "")
                report_data["_confidence"] = prediction.get("confidence", 0)
                with open(report_json_path, "w", encoding="utf-8") as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=2)
                session["medical_report_file"] = report_json_filename
                session["last_pdf_file"] = f"report_{timestamp}.pdf"
                print(f"Report JSON saved: {report_json_path}")
            except Exception as e:
                print(f"Error saving report JSON: {e}")
                session["medical_report_file"] = None

            # Generate PDF report
            pdf_filename = f"report_{timestamp}.pdf"
            pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
            try:
                pdf_generator.generate(
                    output_path=pdf_path,
                    image_path=save_path,
                    image_type=image_type,
                    caption=caption,
                    prediction=prediction,
                    report=report
                )
                print(f"PDF Report generated successfully at {pdf_path}")
            except Exception as e:
                print(f"Error generating PDF report: {e}")
                pdf_filename = None

            return render_template(
                "upload.html",
                image=file.filename,
                caption=caption,
                image_type=image_type,
                prediction=prediction,
                report=report,
                pdf_file=pdf_filename
            )

        except FileNotFoundError as e:
            missing = getattr(e, 'filename', None)
            if not missing:
                parts = str(e).split("'")
                missing = parts[1] if len(parts) > 1 else str(e)

            folder = os.path.dirname(missing) if os.path.dirname(missing) else missing.split("/")[0].split("\\")[0]
            error_msg = (
                f"⚠️ Required model file missing: <code>{missing}</code><br><br>"
                f"Please download the model file and place it in the "
                f"<strong>{folder}/</strong> directory. "
                f"See <strong>{folder}/README.md</strong> for download instructions."
            )
            return render_template("upload.html", error=error_msg)

        except Exception as e:
            print(f"Upload error: {repr(e)}")
            return render_template("upload.html", error=f"⚠️ An error occurred: {str(e)}")

    return render_template("upload.html")