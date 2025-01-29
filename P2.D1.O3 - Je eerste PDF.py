from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(file_name, text):
    # Maak een nieuw canvas voor de PDF
    directory = "PDF_INVOICE"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    c = canvas.Canvas(file_path, pagesize=letter)

    # Stel de positie van de tekst in
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, text)

    # Sla het document op
    c.save()

generate_pdf("voorbeeld.pdf", "Dit is een test van de PDF-generator met Python! en dit is test nummer 4!!!")