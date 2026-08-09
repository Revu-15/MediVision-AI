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

# Ensure required directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("reports", exist_ok=True)


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files.get("image")

        if not file or file.filename == "":
            return render_template("upload.html", error="No file selected. Please upload a medical image.")

        save_path = os.path.join("uploads", file.filename)

        try:
            file.save(save_path)

            image = Image.open(save_path).convert("RGB")

            # Florence Caption
            caption = florence.generate_caption(image)
            caption = caption["<CAPTION>"]

            print("=" * 70)
            print("Caption :", caption)

            # Detect Image Type
            image_type = router.detect_image_type(caption)

            print("Image Type :", image_type)

            # Disease Prediction
            prediction = dispatcher.predict(
                image_type=image_type,
                image_path=save_path,
                caption=caption
            )

            print("=" * 70)
            print("Prediction :", prediction)

            # Medical LLM Report
            result = report_engine.generate(prediction)
            report = result["report"]

            print("=" * 70)
            print(report)

            # Save report to JSON file (session cookies are limited to ~4KB)
            timestamp = int(time.time())
            report_json_filename = f"report_{timestamp}.json"
            report_json_path = os.path.join("reports", report_json_filename)
            try:
                with open(report_json_path, "w", encoding="utf-8") as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                session["medical_report_file"] = report_json_filename
                print(f"Report JSON saved: {report_json_path}")
            except Exception as e:
                print(f"Error saving report JSON: {e}")
                session["medical_report_file"] = None

            # Generate PDF report
            pdf_filename = f"report_{timestamp}.pdf"
            pdf_path = os.path.join("reports", pdf_filename)
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