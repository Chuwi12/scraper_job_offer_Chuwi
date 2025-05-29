import requests
from bs4 import BeautifulSoup
import csv

# Funcion para sacar la información del sitio
def extrar_ofertas(url):

    # Ingreso de petición http get en la variable, simulando que soy un navegador Mozilla
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    # Comprobación de estado 
    if res.status_code == 200:
        
        # Parseo de la página web
        soup = BeautifulSoup(res.txt, "html.parser")

    else: 
        print("El codigo de erro es: " + res.status_code)
        


# Ingreso de url
url = input("Ingresa la url que quieras hacer el scaneo:")

# Llamada a la función
ofertas = extrar_ofertas(url)

#