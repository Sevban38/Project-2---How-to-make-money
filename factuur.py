import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def create_pdf(file_name):
    # document
    doc = SimpleDocTemplate(file_name, pagesize=letter)

    #styles voor paragraphs
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']

    #list of content 
    content = []

    #heading
    heading = Paragraph("Uitgebreide PDF Generator", style_heading)
    content.append(heading)
    content.append(Spacer(1, 12))  # Add space after the heading

    # paragraph
    text = "Dit is een voorbeeld van een PDF die is gegenereerd met de ReportLab bibliotheek. Het bevat verschillende elementen zoals tekst, tabellen, en afbeeldingen."
    paragraph = Paragraph(text, style_normal)
    content.append(paragraph)
    content.append(Spacer(1, 12))

    #table
    table = Table(["product"])
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

    # Add an image (moet correcte plek zijn wel!!!!)
    image_path = "voorbeeld_afbeelding.jpg"  # Make sure this path is correct and the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Afbeelding niet gevonden: {image_path}")
    content.append(Spacer(1, 12))
    content.append(Paragraph("Afbeelding hieronder:", style_normal))
    content.append(Spacer(1, 12))
    img = Image(image_path, 3 * inch, 2 * inch)
    content.append(img)

    #page number
    def add_page_number(canvas, doc):
        canvas.setFont("Helvetica", 10)
        canvas.drawString(500, 10, f"Pagina {doc.page}")

    # Combineer alles
    doc.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)


# Create the PDF
output_dir = "PDF_INVOICE"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, "lege factuur.pdf")
create_pdf(file_path)
