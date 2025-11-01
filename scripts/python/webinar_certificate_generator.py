"""
ModelIt! Webinar Certificate Generator

Generates professional PDF certificates for webinar attendees with:
- ModelIt! branding (colors, fonts, logo)
- Attendee name
- Webinar title and date
- Professional Development hours (2 hrs)
- Unique certificate ID for verification
- Signature line

Requirements:
    pip install reportlab pillow

Usage:
    python webinar_certificate_generator.py "John Smith" "Getting Started with ModelIt!" "2025-02-15"

Output:
    certificates/John_Smith_2025-02-15.pdf
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os
import sys
import hashlib


def generate_certificate(
    name: str,
    webinar_title: str,
    date: str,
    pd_hours: int = 2,
    output_dir: str = "certificates"
):
    """
    Generate a professional PD certificate for webinar attendance

    Args:
        name: Attendee's full name
        webinar_title: Title of the webinar
        date: Date of webinar (YYYY-MM-DD format)
        pd_hours: Professional development hours (default: 2)
        output_dir: Directory to save certificates (default: certificates/)

    Returns:
        tuple: (pdf_path, certificate_id)
    """

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate unique certificate ID
    cert_data = f"{name}{webinar_title}{date}"
    cert_hash = hashlib.md5(cert_data.encode()).hexdigest()[:8].upper()
    cert_id = f"MODELIT-{datetime.now().strftime('%Y%m%d')}-{cert_hash}"

    # Output filename
    safe_name = name.replace(' ', '_')
    filename = f"{output_dir}/{safe_name}_{date}.pdf"

    # Create PDF in landscape mode
    c = canvas.Canvas(filename, pagesize=landscape(letter))
    width, height = landscape(letter)

    # ===== BACKGROUND =====
    # ModelIt! Deep Cobalt Blue border
    c.setFillColorRGB(0.12, 0.31, 0.47)  # #1F4E79
    c.setStrokeColorRGB(0.12, 0.31, 0.47)
    c.setLineWidth(15)
    c.rect(10, 10, width - 20, height - 20, fill=0, stroke=1)

    # White content background
    margin = 50
    c.setFillColorRGB(1, 1, 1)
    c.rect(margin, margin, width - 2*margin, height - 2*margin, fill=1, stroke=0)

    # ===== LOGO =====
    # NOTE: Replace with actual ModelIt! logo path
    # For now, creating a text-based logo
    c.setFillColorRGB(0.12, 0.31, 0.47)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height - 100, "ModelIt!")

    # ===== TITLE =====
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width/2, height - 160, "Certificate of Completion")

    # Decorative line
    c.setStrokeColorRGB(1.0, 0.79, 0.34)  # Gold #FFC857
    c.setLineWidth(2)
    c.line(width/2 - 200, height - 175, width/2 + 200, height - 175)

    # ===== RECIPIENT NAME =====
    c.setFillColorRGB(0.12, 0.31, 0.47)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 230, name)

    # ===== DESCRIPTION =====
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 270, "has successfully completed the professional development webinar")

    # ===== WEBINAR TITLE =====
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 310, webinar_title)

    # ===== DETAILS =====
    c.setFont("Helvetica", 14)
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")
    c.drawCentredString(width/2, height - 350, f"Completed on {formatted_date}")
    c.drawCentredString(width/2, height - 375, f"Professional Development Hours: {pd_hours}")

    # ===== COMPETENCIES (Optional) =====
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 410, "NGSS Science Practices • Computational Modeling • Educational Technology")

    # ===== SIGNATURE LINE =====
    c.setStrokeColorRGB(0.17, 0.17, 0.25)  # Slate Navy #2B2B40
    c.setLineWidth(1)
    c.line(width/2 - 150, height - 460, width/2 + 150, height - 460)

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 480, "Charles Martin, Founder")
    c.drawCentredString(width/2, height - 495, "ModelIt! Educational Simulations")

    # ===== CERTIFICATE ID =====
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawString(margin + 10, margin + 10, f"Certificate ID: {cert_id}")
    c.drawString(width - margin - 150, margin + 10, "Verify: modelit.com/verify")

    # ===== DECORATIVE ELEMENTS =====
    # Corner accents (Gold)
    c.setFillColorRGB(1.0, 0.79, 0.34)  # #FFC857

    # Top-left corner
    c.circle(margin + 20, height - margin - 20, 5, fill=1, stroke=0)

    # Top-right corner
    c.circle(width - margin - 20, height - margin - 20, 5, fill=1, stroke=0)

    # Bottom-left corner
    c.circle(margin + 20, margin + 20, 5, fill=1, stroke=0)

    # Bottom-right corner
    c.circle(width - margin - 20, margin + 20, 5, fill=1, stroke=0)

    # ===== SAVE PDF =====
    c.save()

    print(f"✅ Certificate generated: {filename}")
    print(f"🆔 Certificate ID: {cert_id}")

    return filename, cert_id


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python webinar_certificate_generator.py <name> <webinar_title> <date>")
        print("Example: python webinar_certificate_generator.py \"John Smith\" \"Getting Started with ModelIt!\" \"2025-02-15\"")
        sys.exit(1)

    name = sys.argv[1]
    webinar_title = sys.argv[2]
    date = sys.argv[3]

    # Optional: PD hours (default 2)
    pd_hours = int(sys.argv[4]) if len(sys.argv) > 4 else 2

    pdf_path, cert_id = generate_certificate(name, webinar_title, date, pd_hours)

    # For n8n integration, output JSON
    import json
    result = {
        "certificate_path": pdf_path,
        "certificate_id": cert_id,
        "recipient_name": name,
        "webinar_title": webinar_title,
        "date": date,
        "pd_hours": pd_hours
    }
    print(json.dumps(result))
