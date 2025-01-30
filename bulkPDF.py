import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit

# Mappen definiëren
input_folder = "JSON_ORDER2"  # Map met order JSON-bestanden
processed_folder = "JSON_PROCESSED"  # Map voor succesvolle verwerking
error_folder = "JSON_ORDER_ERROR"  # Map voor foutieve JSON-bestanden
pdf_folder = "pdf_orders"  # Map voor gegenereerde PDF's

# Zorg ervoor dat de mappen bestaan
os.makedirs(processed_folder, exist_ok=True)
os.makedirs(error_folder, exist_ok=True)
os.makedirs(pdf_folder, exist_ok=True)

# Functie om een PDF te maken
def create_pdf(order_data, pdf_path):
    """
    Genereert een PDF-bestand vanuit een order JSON.
    """
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Algemene styling
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.darkblue)
    c.drawString(100, height - 50, "Bestellingsoverzicht")
    
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(100, height - 55, 400, height - 55)

    # Ordergegevens
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)

    order_id = order_data.get("order", {}).get("id", "Onbekend")
    customer_name = order_data.get("order", {}).get("customer", "Onbekend")
    order_date = order_data.get("order", {}).get("date", "Onbekend")

    y_position = height - 80
    c.drawString(100, y_position, f"Order ID: {order_id}")
    c.drawString(100, y_position - 20, f"Klant: {customer_name}")
    c.drawString(100, y_position - 40, f"Datum: {order_date}")

    # Orderitems
    y_position -= 70
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "Bestelde producten:")
    
    c.setFont("Helvetica", 11)
    y_position -= 20
    
    for item in order_data.get("order", {}).get("items", []):
        item_name = item.get("name", "Onbekend product")
        item_price = item.get("price", "0.00")
        item_line = f"- {item_name}: €{item_price}"
        
        # Automatische regelafbreking als de productnaam te lang is
        wrapped_lines = simpleSplit(item_line, "Helvetica", 11, width - 150)
        for line in wrapped_lines:
            c.drawString(100, y_position, line)
            y_position -= 20
            
        if y_position < 50:  # Voorkomt dat tekst buiten de pagina valt
            c.showPage()
            c.setFont("Helvetica", 11)
            y_position = height - 50

    c.save()

# JSON-bestanden verwerken
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        input_file_path = os.path.join(input_folder, filename)
        
        try:
            # JSON-bestand inlezen
            with open(input_file_path, "r") as file:
                order_data = json.load(file)

            # Order-ID verkrijgen voor bestandsnaam
            order_id = order_data.get("order", {}).get("id", "unknown")
            pdf_filename = f"order_{order_id}.pdf"
            pdf_path = os.path.join(pdf_folder, pdf_filename)

            # PDF genereren
            create_pdf(order_data, pdf_path)

            # Verplaats verwerkt bestand
            processed_path = os.path.join(processed_folder, filename)
            os.rename(input_file_path, processed_path)
            print(f"✅ PDF gegenereerd: {pdf_path}")

        except Exception as e:
            # Fout opslaan in error map
            error_path = os.path.join(error_folder, filename)
            os.rename(input_file_path, error_path)
            print(f"❌ Fout in {filename}, verplaatst naar {error_folder}: {e}")

print("🚀 Batchverwerking voltooid!")
