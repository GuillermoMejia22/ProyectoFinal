import requests
from bs4 import BeautifulSoup

def obtener_informacion_diabetes():
    # URL de la página que deseas raspar
    url = "https://www.insp.mx/avisos/3652-diabetes-en-mexico.html"

    # Realiza la solicitud a la página web
    response = requests.get(url)

    # Verifica si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Parsea el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentra y extrae la información que necesitas
        informacion_diabetes = soup.find("div", class_="diabetes")
        if informacion_diabetes:
            # Imprime o retorna la información
            print(informacion_diabetes.get_text())
            return informacion_diabetes.get_text()
        else:
            print("No se encontró información sobre diabetes en la página.")
    else:
        print(f"No se pudo acceder a la página. Código de estado: {response.status_code}")

# Llama a la función para obtener la información
obtener_informacion_diabetes()
