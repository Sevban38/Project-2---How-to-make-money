import json
import os
from datetime import datetime

# Functie om btw te berekenen
def calculate_vat(amount, rate):
    return round(amount * (rate / 100), 2)

# Functie om het totaalbedrag inclusief btw te berekenen
def calculate_total_amount(products):
    subtotal = 0
    for product in products:
        subtotal += product['aantal'] * product['prijs_per_stuk_excl_btw']
    return subtotal

# Zorg ervoor dat de map JSON_INVOICE bestaat
invoice_dir = os.path.abspath("./JSON_INVOICE")
if not os.path.exists(invoice_dir):
    os.makedirs(invoice_dir)

# Het pad naar de map JSON_ORDER
path = os.path.abspath("./JSON_ORDER")

# Verwerk de bestanden in de JSON_ORDER map
for file1 in os.listdir(path):
    file_path = os.path.join(path, file1)
    print(f"Verwerken bestand: {file_path}")

    # Inleiden van de order JSON
    try:
        with open(file_path, 'r') as file:
            order_data = json.load(file)
    except Exception as e:
        print(f"Fout bij het inleiden van het bestand {file_path}: {e}")
        continue

    # Verkrijg de klantgegevens en productinformatie
    try:
        customer = order_data['factuur']['klant']  # 'klant' binnen de 'order' sleutel
        products = order_data['factuur']['producten']  # 'producten' binnen de 'order' sleutel
        order_date = order_data['factuur']['factuurdatum']  # 'orderdatum' binnen de 'order' sleutel
    except KeyError as e:
        print(f"Fout: ontbrekende sleutel {e} in bestand {file_path}")
        continue

    # Bereken subtotaal en btw
    subtotal = calculate_total_amount(products)
    vat = 0
    for product in products:
        vat += calculate_vat(product['aantal'] * product['prijs_per_stuk_excl_btw'], product['btw_per_stuk'])
    total = subtotal + vat

    # Genereer een factuurnummer
    invoice_id = f"FACT-{order_data['factuur']['factuurnummer']}"

    # Stel de factuur JSON samen
    invoice_data = {
        "invoice_id": invoice_id,
        "customer": customer,
        "invoice_date": order_date,  # Of kies de huidige datum met datetime.today().strftime("%Y-%m-%d")
        "products": [],
        "subtotal": subtotal,
        "vat": vat,
        "total": total
    }

    # Voeg de productinformatie toe aan de factuur, met btw per product
    for product in products:
        product_total = product['aantal'] * product['prijs_per_stuk_excl_btw']
        product_vat = calculate_vat(product_total, product['btw_per_stuk'])
        invoice_data['products'].append({
            "product_name": product['productnaam'],
            "quantity": product['aantal'],
            "unit_price_excl_vat": product['prijs_per_stuk_excl_btw'],
            "total_price_excl_vat": product_total,
            "vat_amount": product_vat
        })

    # Bepaal het pad voor het opslaan van de factuur in JSON_INVOICE
    invoice_filename = os.path.join(invoice_dir, file1.replace('.json', '_invoice.json'))

    # Sla de factuur op in de map JSON_INVOICE
    with open(invoice_filename, 'w') as file:
        json.dump(invoice_data, file, indent=4)

    print(f"Factuur succesvol aangemaakt en opgeslagen als {invoice_filename}")