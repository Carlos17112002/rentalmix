import csv
from datetime import datetime

def leer_facturas_desde_archivo(archivo):
    facturas = []
    decoded_file = archivo.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file, delimiter=';')  # ← usa punto y coma

    try:
        encabezado = next(reader)  # salta la primera fila
    except StopIteration:
        return []

    for row in reader:
        try:
            factura = {
                'folio': row[5].strip(),  # columna 6: Folio
                'fecha_emision': datetime.strptime(row[6].strip(), '%d/%m/%Y').date(),  # columna 7: Fecha Docto
                'proveedor': row[4].strip(),  # columna 5: Razon Social
                'rut_proveedor': row[3].strip(),  # columna 4: RUT
                'monto_exento': float(row[9].replace('.', '').replace(',', '').strip()),  # columna 12: Monto Exento
                'monto_neto': float(row[10].replace('.', '').replace(',', '').strip()),  # columna 13: Monto Neto
                'monto_iva': float(row[11].replace('.', '').replace(',', '').strip()),  # columna 14: Monto IVA
                'monto_total': float(row[14].replace('.', '').replace(',', '').strip())  # columna 12: Monto Total
            }
            facturas.append(factura)
        except Exception as e:
            print(f"Error en fila: {row} → {e}")
            continue

    return facturas

