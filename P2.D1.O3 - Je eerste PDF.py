from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(file_name, text):
    directory = "PDF_INVOICE"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    c = canvas.Canvas(file_path, pagesize=letter)

    c.setFont("Helvetica", 12)
    c.drawString(100, 750, text)

    c.save()

generate_pdf("voorbeeld.pdf", "Dit is een test van de PDF-generator met Python!")
