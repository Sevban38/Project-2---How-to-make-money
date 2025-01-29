import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def create_pdf(file_name):
    # Maak een document aan
    doc = SimpleDocTemplate(file_name, pagesize=letter)

    # Stel de stijl in voor de paragrafen
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']

    # Maak een lijst met inhoud voor het document
    content = []

    # Voeg een kop toe
    heading = Paragraph("Uitgebreide PDF Generator", style_heading)
    content.append(heading)
    content.append(Spacer(1, 12))  # Voeg ruimte toe na de kop

    # Voeg een tekstparagraaf toe
    text = "Dit is een voorbeeld van een PDF die is gegenereerd met de ReportLab bibliotheek. Het bevat verschillende elementen zoals tekst, tabellen, en afbeeldingen."
    paragraph = Paragraph(text, style_normal)
    content.append(paragraph)
    content.append(Spacer(1, 12))

    # Voeg een tabel toe
    data = [['Naam', 'Leeftijd', 'Stad'],
            ['Jan', '30', 'Amsterdam'],
            ['Piet', '25', 'Rotterdam'],
            ['Klaas', '35', 'Utrecht']]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(table)
    content.append(Spacer(1, 12))

    # Voeg een afbeelding toe (zorg ervoor dat het bestand correct is)
    image_path = "c:/Users/Sb383/Documents/GitHub/Project-2---How-to-make-money/voorbeeld_afbeelding.jpg"  # Zorg ervoor dat dit pad correct is en het bestand bestaat
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Afbeelding niet gevonden: {image_path}")
    content.append(Spacer(1, 12))
    content.append(Paragraph("Afbeelding hieronder:", style_normal))
    content.append(Spacer(1, 12))
    img = Image(image_path, 3 * inch, 2 * inch)
    content.append(img)

    # Voeg een paginanummer toe
    def add_page_number(canvas, doc):
        canvas.setFont("Helvetica", 10)
        canvas.drawString(500, 10, f"Pagina {doc.page}")

    # Voeg alles samen en maak de PDF
    doc.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)


create_pdf("voorbeeld_uitgebreide_pdf.pdf")