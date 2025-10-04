from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def create_result_pdf(summary, subject, set_number):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "OMR Evaluation Result")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Student: {summary['Student']}")
    c.drawString(50, height - 100, f"Subject: {subject}")
    c.drawString(50, height - 120, f"Set: {set_number}")
    c.drawString(50, height - 140, f"Score: {summary['Score']}")
    c.drawString(50, height - 160, f"Correct: {summary['Correct']}")
    c.drawString(50, height - 180, f"Incorrect: {summary['Incorrect']}")
    c.drawString(50, height - 200, f"Unmarked: {summary['Unmarked']}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 230, "Question-wise Breakdown:")

    y = height - 250
    c.setFont("Helvetica", 10)
    for detail in summary["Details"]:
        line = f"{detail['question']}: Marked = {detail['marked']}, Correct = {detail['correct']}, Status = {detail['status']}"
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
