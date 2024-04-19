import matplotlib.pyplot as plt

def clasificar_IMC(imcs):
    clasificacion = {
        "Delgadez moderada": 0,
        "Delgadez aceptable": 0,
        "Peso Normal": 0,
        "Sobrepeso": 0,
        "Obesidad tipo I": 0,
        "Obesidad tipo II": 0,
        "Obesidad tipo III (Obesidad Mórbida)": 0,
        "Obesidad tipo IV o extrema": 0
    }

    for imc in imcs:
        if 16 < imc <= 16.99:
            clasificacion["Delgadez moderada"] += 1
        elif 17 <= imc <= 18.49:
            clasificacion["Delgadez aceptable"] += 1
        elif 18.5 <= imc <= 24.99:
            clasificacion["Peso Normal"] += 1
        elif 25 <= imc <= 29.99:
            clasificacion["Sobrepeso"] += 1
        elif 30 <= imc <= 34.99:
            clasificacion["Obesidad tipo I"] += 1
        elif 35 <= imc <= 40:
            clasificacion["Obesidad tipo II"] += 1
        elif 40 <= imc <= 49.99:
            clasificacion["Obesidad tipo III (Obesidad Mórbida)"] += 1
        elif imc >= 50:
            clasificacion["Obesidad tipo IV o extrema"] += 1

    return clasificacion

def graficar_clasificacion(clasificacion):
    categorias = list(clasificacion.keys())
    valores = list(clasificacion.values())

    plt.bar(categorias, valores, color='skyblue')
    plt.xlabel('Categoría de IMC')
    plt.ylabel('Número de Pacientes')
    plt.title('Clasificación de IMC en Pacientes Diabéticos')
    plt.xticks(rotation=45, ha='right')
    plt.show()

# Ejemplo de uso
imcs = [21.5, 27.3, 32.1, 40.5, 18.7, 36.2, 22.9, 29.8]  # Ejemplo de lista de IMC
clasificacion = clasificar_IMC(imcs)
graficar_clasificacion(clasificacion)
