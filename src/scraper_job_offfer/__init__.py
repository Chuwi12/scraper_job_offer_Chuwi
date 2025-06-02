import requests
from bs4 import BeautifulSoup
import csv

# Funcion para sacar la información del sitio
def extrar_ofertas(url, nombre_archivo):

    # Ingreso de petición http get en la variable, simulando que soy un navegador Mozilla
    req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    # Comprobación de estado 
    if req.status_code == 200:
        
        # Parseo de la página web
        soup = BeautifulSoup(req.text, "html.parser")

        # Lista de las ofertas de trabajo
        ofertas = []

        # Iterar las ofertas de trabajo
        for oferta in soup.find_all("article"):

            # Extracción de nombre de la oferta de trabajo
            titulo_elemento = oferta.find("h2")

            # Comprobación de la existencía del titulo, sino esxiste se asigana none
            titulo = titulo_elemento.get_text(strip=True) if titulo_elemento else "None"

            # Comprobación de nivel de experiencía de la oferta 
            # En mi caso de junior y entry modificable para futuros usos
            nivel_elemento = oferta.find("span", class_="experience-level")

            # Comprobación de la existencia del nivel de la oferta
            nivel = nivel_elemento.get_text(strip=True).lower() if nivel_elemento else "No se especifica"

            # Comprobación de que la oferta sea para junior o entry
            if "junior"  not in nivel and "entry" not in nivel:
                continue
            
            # Comprobación de si la oferta es en remoto, exactamente el mismo procedimeinto del anterior
            ubicacion_elemento = oferta.find("span", class_="location")
            ubicacion = ubicacion_elemento.get_text(strip=True).lower() if ubicacion_elemento else "No es remota"
            if "remote" not in ubicacion:
                continue

            # Extración de salarío si este se encuentra
            salario_elemento = oferta.find("span", class_="salary")
            salario = salario_elemento.get_text(strip=True) if salario_elemento else "No especificado"

            # Obtener las tecnologías que piden
            tecnologias = []
            tecnologias_elementos = oferta.find_all("span", class_="technology")
            for tec in tecnologias_elementos:
                tecnologias.append(tec.get_text(strip=True))

            # Añadir las ofertas a la lista
            ofertas.append({
                "Puesto": titulo,
                "Salario": salario,
                "Tecnologías": ", ".join(tecnologias)
            })

        # Creación del archivos .csv con los datos de las ofertas
        with open(nombre_archivo + ".csv", "w", newline="", encoding="utf-8") as csvfile:
            campos = ["Puesto", "Salario", "Tecnologías"]
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writeheader()
            for oferta in ofertas:
                writer.writerow(oferta)

    else: 
        print("El codigo de erro es: " + req.status_code)
        


# Ingreso de url
url = input("Ingresa la url que quieras hacer el scaneo:\n")

# Ingreso de nombre del archivo
nombre_archivo = input("Nombre del archivo:\n")

# Llamada a la función
ofertas = extrar_ofertas(url, nombre_archivo)