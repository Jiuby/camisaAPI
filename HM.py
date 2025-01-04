import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager



def analizar_pagina(url):


    # Configurar opciones para el navegador en modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Navegar a la URL de la página
    driver.get(url)

    # Esperar a que la página cargue completamente
    driver.implicitly_wait(10)

    # Scroll down in increments of 20% until the bottom of the page
    scroll_pause_time = 2  # Tiempo de espera entre scrolls
    scroll_increment = 0.2  # Incremento de scroll (20%)

    def scroll_to_bottom():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            scroll_height = last_height * scroll_increment
            driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    scroll_to_bottom()

    # Esperar 2 segundos antes de cerrar el navegador
    time.sleep(2)

    # Obtener el contenido de la página
    contenido = driver.page_source
    driver.quit()

    # Procesar el contenido usando BeautifulSoup
    soup = BeautifulSoup(contenido, "lxml")
    ropa = soup.find_all("a", class_="vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--grilla h-100 flex flex-column")

    # Lista para almacenar los resultados
    resultados = []

    # Extraer y almacenar la información de cada camisa
    for camisa in ropa:
        try:
            url_camisa = camisa["href"]
            url_imagen = camisa.find("img")["src"]

            # Encontrar todos los elementos de precio
            numeros_precio = camisa.find_all("span", class_="vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--newlistPrice")

            # Si encontramos los dos números
            if len(numeros_precio) >= 2:
                parte_entera = numeros_precio[0].text.strip()
                parte_decimal = numeros_precio[1].text.strip()

                # Obtener el separador (podría ser punto o coma)
                separador = camisa.find("span", class_="vtex-product-price-1-x-currencyGroup vtex-product-price-1-x-currencyGroup--newlistPrice")
                separador_texto = separador.text.strip() if separador else "."

                # Formar el precio completo
                precio = f"{parte_entera}{separador_texto}{parte_decimal}"
            else:
                precio = "Precio no disponible"

            resultados.append({
                "url_camisa": f"https://co.hm.com{url_camisa}",
                "url_imagen": url_imagen,
                "precio": precio
            })
        except Exception as e:
            print(f"Error procesando un producto: {str(e)}")

    return resultados

# Función para guardar los resultados en un archivo JSON
def guardar_resultados_en_json(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

# Recopilar los datos de las tres páginas
todas_las_camisas = []
urls = [
    "https://co.hm.com/hombre/camisetas",
    "https://co.hm.com/hombre/camisetas?page=2",
    "https://co.hm.com/hombre/camisetas?page=3"
]

for url in urls:
    todas_las_camisas.extend(analizar_pagina(url))

# Guardar los datos en un archivo JSON
guardar_resultados_en_json("camisasH&M.json", todas_las_camisas)

print("Datos guardados en camisasH&M.json")