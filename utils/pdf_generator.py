from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
import os
from datetime import datetime


class PDFGenerator:

    def generate(
        self,
        output_path,
        image_path,
        image_type,
        caption,
        prediction,
        report
    ):
        # Ensure target directory exists
        if os.path.dirname(output_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

        doc = SimpleDocTemplate(output_path)

        styles = getSampleStyleSheet()

        # Custom Colors
        primary_color = HexColor("#1565c0")
        secondary_color = HexColor("#1d3557")
        warning_color = HexColor("#d32f2f")
        text_color = HexColor("#2c3e50")

        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=primary_color,
            alignment=TA_CENTER,
            spaceAfter=5
        )

        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=10,
            textColor=HexColor("#7f8c8d"),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        h2_style = ParagraphStyle(
            'ReportH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=secondary_color,
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=text_color,
            spaceAfter=6
        )

        bullet_style = ParagraphStyle(
            'ReportBullet',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=text_color,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=4
        )

        warning_style = ParagraphStyle(
            'ReportWarning',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            textColor=warning_color,
            spaceBefore=10,
            spaceAfter=10
        )

        disclaimer_style = ParagraphStyle(
            'ReportDisclaimer',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9,
            leading=13,
            textColor=HexColor("#7f8c8d"),
            spaceBefore=15
        )

        story = []

        # Header
        story.append(Paragraph("MediVision AI", title_style))
        story.append(Paragraph("Professional Medical Diagnostic Report", subtitle_style))

        # Metadata
        story.append(
            Paragraph(
                f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                body_style
            )
        )
        story.append(Paragraph(f"<b>Image Type:</b> {image_type}", body_style))
        story.append(Paragraph(f"<b>Florence-2 Caption:</b> {caption}", body_style))
        story.append(
            Paragraph(
                f"<b>AI Diagnosis:</b> {prediction['prediction']} (Confidence: {prediction['confidence']}%)",
                body_style
            )
        )

        story.append(Spacer(1, 15))

        # Display Image (scaled)
        temp_img_path = None
        if image_path and os.path.exists(image_path):
            try:
                from PIL import Image as PILImage
                import tempfile
                
                with PILImage.open(image_path) as pil_img:
                    pil_img = pil_img.convert("RGB")
                    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                    temp_img_path = temp_file.name
                    temp_file.close()
                    pil_img.save(temp_img_path, format="JPEG")

                img = Image(temp_img_path)
                img.drawWidth = 200
                img.drawHeight = 200
                story.append(img)
                story.append(Spacer(1, 15))
            except Exception as e:
                print("Error loading image in PDF:", e)

        # Top Predictions
        story.append(Paragraph("Top 3 Predictions", h2_style))
        for disease, score in prediction.get("top_predictions", []):
            story.append(
                Paragraph(f"• {disease} : {score}%", bullet_style)
            )

        story.append(Spacer(1, 10))

        # --- Professional Medical Report Sections ---

        def add_text_section(title, content):
            if content and isinstance(content, str):
                story.append(Paragraph(title, h2_style))
                story.append(Paragraph(content, body_style))

        def add_list_section(title, items):
            if isinstance(items, str):
                items = [items]
            if items and isinstance(items, list):
                items = [item for item in items if item.strip()]
                if items:
                    story.append(Paragraph(title, h2_style))
                    for item in items:
                        story.append(Paragraph(f"• {item}", bullet_style))

        # Disease Overview
        add_text_section("Disease Overview", report.get("overview"))

        # Common Symptoms
        add_list_section("Common Symptoms", report.get("symptoms"))

        # Causes
        add_list_section("Causes", report.get("causes"))

        # Risk Factors
        add_list_section("Risk Factors", report.get("risk_factors"))

        # Possible Complications
        add_list_section("Possible Complications", report.get("complications"))

        # Recommended Diagnostic Tests
        add_list_section("Recommended Diagnostic Tests", report.get("diagnostic_tests"))

        # General Treatment Information
        add_text_section("General Treatment Information", report.get("treatment"))

        # Lifestyle & Precautions
        add_list_section("Lifestyle & Precautions", report.get("precautions"))

        # Recommended Specialist
        add_text_section("Recommended Specialist", report.get("specialist"))

        # Emergency Warning (Highlight in warning red style)
        emergency = report.get("emergency_warning")
        if emergency and isinstance(emergency, str) and emergency.strip():
            story.append(Paragraph("Emergency Warning", h2_style))
            story.append(Paragraph(emergency, warning_style))

        # Medical Disclaimer
        disclaimer = report.get("disclaimer")
        if disclaimer and isinstance(disclaimer, str) and disclaimer.strip():
            story.append(Paragraph("Medical Disclaimer", disclaimer_style))
            story.append(Paragraph(disclaimer, body_style))
        else:
            # Fallback standard disclaimer
            story.append(Paragraph("Medical Disclaimer", disclaimer_style))
            story.append(
                Paragraph(
                    "This report is AI-generated and is intended for educational purposes only. "
                    "Please consult a qualified healthcare professional for diagnosis and treatment.",
                    body_style
                )
            )

        doc.build(story)

        if temp_img_path and os.path.exists(temp_img_path):
            try:
                os.remove(temp_img_path)
            except Exception:
                pass