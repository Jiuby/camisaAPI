import os
import json

def limpiar_precio(precio_str):
    # Remover símbolos no numéricos y convertir a entero
    precio_limpio_str = ''.join(filter(str.isdigit, precio_str))
    if precio_limpio_str:
        return int(precio_limpio_str)
    else:
        return 0  # or handle the case as needed

# Cargar los JSON individuales
with open("camisasH&M.json", "r", encoding="utf-8") as archivo_hm:
    camisas_hm = json.load(archivo_hm)

with open("camisasKOAJ.json", "r", encoding="utf-8") as archivo_koaj:
    camisas_koaj = json.load(archivo_koaj)

with open("camisasPULLANDBEAR.json", "r", encoding="utf-8") as archivo_pullandbear:
    camisas_pullandbear = json.load(archivo_pullandbear)

# Limpiar y unificar los datos
camisas_unificadas = []

for camisa in camisas_hm + camisas_koaj + camisas_pullandbear:
    try:
        camisa_limpia = {
            "url_camisa": camisa["url_camisa"],
            "url_imagen": camisa["url_imagen"],
            "precio": limpiar_precio(camisa["precio"]),
        }
        camisas_unificadas.append(camisa_limpia)
    except KeyError as e:
        print(f"Error procesando camisa: {e}")

# Guardar el JSON unificado
nombre_archivo_unificado = "camisas_unificadas.json"
with open(nombre_archivo_unificado, "w", encoding="utf-8") as archivo_unificado:
    json.dump(camisas_unificadas, archivo_unificado, ensure_ascii=False, indent=4)

print(f"Datos unificados guardados en {nombre_archivo_unificado}")