import requests
from bs4 import BeautifulSoup
import csv

# Funcion para sacar la información del sitio
def extrac_offers(url, nombre_archivo):

    # Ingreso de petición http get en la variable, simulando que soy un navegador Mozilla
    req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    # Comprobación de estado 
    if req.status_code == 200:
        
        # Parseo de la página web
        soup = BeautifulSoup(req.text, "html.parser")

        # Lista de las ofertas de trabajo
        offers = []

        # Iterar las ofertas de trabajo
        for offer in soup.find_all("article"):

            # Extracción de nombre de la oferta de trabajo
            elemet_title = offer.find("h2")

            # Comprobación de la existencía del titulo, sino esxiste se asigana none
            title = elemet_title.get_text(strip=True) if elemet_title else "None"

            # Comprobación de nivel de experiencía de la oferta 
            # En mi caso de junior y entry modificable para futuros usos
            element_level = offer.find("span", class_="experience-level")

            # Comprobación de la existencia del nivel de la oferta
            level = element_level.get_text(strip=True).lower() if element_level else "No se especifica"

            # Comprobación de que la oferta sea para junior o entry
            if "junior"  not in level and "entry" not in level:
                continue
            
            # Comprobación de si la oferta es en remoto, exactamente el mismo procedimeinto del anterior
            element_location = offer.find("span", class_="location")
            location = element_location.get_text(strip=True).lower() if element_location else "No es remota"
            if "remote" not in location:
                continue

            # Extración de salarío si este se encuentra
            element_salary = offer.find("span", class_="salary")
            salary = element_salary.get_text(strip=True) if element_salary else "No especificado"

            # Obtener las tecnologías que piden
            technologys = []
            element_technolgys = offer.find_all("span", class_="technology")
            for tec in element_technolgys:
                technologys.append(tec.get_text(strip=True))

            # Añadir las ofertas a la lista
            offers.append({
                "Puesto": title,
                "Salario": salary,
                "Tecnologías": ", ".join(technologys)
            })

        # Creación del archivos .csv con los datos de las ofertas
        with open(nombre_archivo + ".csv", "w", newline="", encoding="utf-8") as csvfile:
            fields = ["Puesto", "Salario", "Tecnologías"]
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for offer in offers:
                writer.writerow(offer)

    else: 
        print("El codigo de erro es: " + req.status_code)
        


# Ingreso de url
url = input(":\n")

# Ingreso de nombre del archivo
file_name = input("File name:\n")

# Llamada a la función
extrac_offers(url, file_name)