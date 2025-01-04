import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Construir la ruta al driver de Edge
current_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(current_dir, "edgedriver_win64", "msedgedriver.exe")

# Configurar opciones para el navegador en modo headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

# URL de la página
url = "https://www.pullandbear.com/co/hombre/ropa/camisetas-n6323"

# Navegar a la URL de la página
driver.get(url)

# Esperar a que la página cargue completamente
driver.implicitly_wait(10)

# Simular interacciones para cargar contenido dinámico
actions = ActionChains(driver)
end_time = time.time() + 60  # Mantener la interacción durante 60 segundos

while time.time() < end_time:
    # Scroll down ligeramente para simular actividad
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(0.4)

    # Simular un clic en un área visible para activar eventos dinámicos
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, "body")
        if elements:
            actions.move_to_element(elements[0]).click().perform()
    except Exception as e:
        print(f"Error durante la simulación de clic: {e}")

# Obtener el contenido de la página
contenido = driver.page_source
driver.quit()

# Procesar el contenido usando BeautifulSoup
soup = BeautifulSoup(contenido, "lxml")
ropa = soup.find_all("div", class_="c-tile c-tile--product")

# Lista para almacenar los resultados
resultados = []

# Extraer y guardar la información de cada producto
for item in ropa:
    try:
        url_camisa = item.find("div", class_="carousel-wrapper").find("a")["href"]
        img_element = item.find("figure", class_="figure").find("img")
        url_imagen = img_element["src"]
        precio = item.find("div", class_="product-price--price").get_text(strip=True)

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

guardar_resultados_en_json("camisasPULLANDBEAR.json", resultados)

print(f"Datos guardados en camisasPULLANDBEAR.json")