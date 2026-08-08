from flask import Blueprint, send_from_directory

download_bp = Blueprint("download", __name__)

@download_bp.route("/download/<filename>")
def download_report(filename):

    return send_from_directory(
        "reports",
        filename,
        as_attachment=True
    )