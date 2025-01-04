import os
import time
import json
import re
import math
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

options = Options()

current_dir = os.path.dirname(os.path.abspath(__file__))
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Configurar opciones para el navegador en modo headless
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

# URL base de la página
base_url = "https://www.koaj.co/hombre/ropa/camisetas/#/page-"

# Función para analizar una página
def analizar_pagina(url):
    driver.get(url)
    driver.implicitly_wait(10)
    contenido = driver.page_source
    return BeautifulSoup(contenido, "lxml")

# Obtener el número total de páginas
soup = analizar_pagina(base_url + "1")
camisas_tot = soup.find_all("span", class_="product_count")
product_count_text = camisas_tot[0].get_text(strip=True)
product_count_number = int(re.search(r'\d+', product_count_text).group())
Paginas_total = math.ceil(product_count_number / 39)

# Lista para almacenar los resultados
resultados = []

# Analizar cada página
for page in range(1, Paginas_total + 1):
    url = base_url + str(page)
    driver.get(url)  # Recargar la URL
    driver.refresh()  # Refrescar la página
    time.sleep(1)  # Esperar 1 segundo
    soup = analizar_pagina(url)
    pro_outer_boxes = soup.find_all("div", class_="pro_outer_box")

    # Procesar cada camisa en la página actual
    for box in pro_outer_boxes:
        try:
            # URL de la camisa
            link_tag = box.find("a", class_="lnk_view product_img_link")
            url_camisa = link_tag["href"] if link_tag else "URL no disponible"

            # URL de la imagen de la camisa
            img_tag = box.find("img", class_="replace-2x img-responsive front-image")
            url_imagen = img_tag["src"] if img_tag else "Imagen no disponible"

            # Precio de la camisa
            price_tag = box.find("span", class_="price product-price")
            if not price_tag:
                price_tag = box.find("span", class_="price product-price with_discount")
            precio = price_tag.get_text(strip=True) if price_tag else "Precio no disponible"

            # Agregar los datos al resultado
            resultados.append({
                "url_camisa": url_camisa,
                "url_imagen": url_imagen,
                "precio": precio
            })
        except Exception as e:
            print(f"Error procesando un producto: {str(e)}")

# Guardar los resultados en un archivo JSON
def guardar_resultados_en_json(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

guardar_resultados_en_json("camisasKOAJ.json", resultados)

print(f"Datos guardados en camisasKOAJ.json")
driver.quit()