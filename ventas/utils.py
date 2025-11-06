import csv
from datetime import datetime
from io import TextIOWrapper

def leer_ventas_desde_archivo(archivo):
    """
    Procesa un archivo CSV del SII (libro de ventas) y retorna una lista de facturas de venta.
    """
    ventas = []

    try:
        archivo.seek(0)  # ← rebobina el archivo si ya fue leído
        decoded_file = TextIOWrapper(archivo, encoding='utf-8')
        reader = csv.reader(decoded_file, delimiter=';')  # ← usa punto y coma

        encabezado = next(reader)  # saltar encabezado
    except Exception as e:
        print(f"Error al leer el archivo: {e}")  # ← muestra el error real
        return []

    for row in reader:
        if len(row) < 12:
            print(f"Fila incompleta omitida: {row}")
            continue

        try:
            folio = row[5].strip()
            fecha_emision = datetime.strptime(row[6].strip(), '%d/%m/%Y').date()
            cliente = row[4].strip()
            rut_cliente = row[3].strip()
            monto_exento = float(row[10].replace('.', '').replace(',', '').strip())
            monto_neto = float(row[11].replace('.', '').replace(',', '').strip())
            monto_iva = float(row[12].replace('.', '').replace(',', '').strip())
            monto_total = float(row[13].replace('.', '').replace(',', '').strip())

            ventas.append({
                'folio': folio,
                'fecha_emision': fecha_emision,
                'cliente': cliente,
                'rut_cliente': rut_cliente,
                'monto_exento': monto_exento,
                'monto_neto': monto_neto,
                'monto_iva': monto_iva,
                'monto_total': monto_total
            })

        except Exception as e:
            print(f"Error en fila: {row} → {e}")
            continue

    print(f"Ventas procesadas: {len(ventas)}")
    return ventas