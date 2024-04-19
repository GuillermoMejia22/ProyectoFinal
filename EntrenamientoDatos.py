import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

# Cargar las ontologías RDF/XML
onto = Graph()
onto.parse("RedOntológica\\datosRDF.owl", format="xml")

# Crear un DataFrame de Pandas para almacenar los datos
data = {
    'colesterol_total': [],
    # Más atributos
}

prefijo = """
    PREFIX paciente: <http://www.modelo.org/datos#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

sparql_query = prefijo + """
    SELECT ?nota ?analisis ?colesterol
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tieneColesterolTotal ?colesterol .
            ?nota a paciente:Nota_Medica .
        }
    """
query = prepareQuery(sparql_query)
padecimiento_buscar = "DIABETES"
niveles_colesterol = []

# Recolecta los datos
for row in onto.query(query):
    if padecimiento_buscar in row.analisis.upper() and row.colesterol is not None:
        print("ANALISIS: ", row.analisis)
        print("COLESTEROL TOTAL: ", row.colesterol)
        data['colesterol_total'].append(float(row.colesterol))

df = pd.DataFrame(data)

# Dividir los datos en conjunto de entrenamiento y conjunto de prueba
X_train = pd.DataFrame({'constante': [1] * len(data['colesterol_total'])})  # Característica constante
y_train = df['colesterol_total']  # Variable objetivo
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Entrenamiento de un Modelo de Regresión Líneal
model = LinearRegression()
model.fit(X_train, y_train)

# Generar datos de prueba, si tenemos datos reales lo reemplazamos (diferentes a los que usamos para el entrenamiento)
num_test_samples = 20
X_test_synthetic = pd.DataFrame({'constante': [1] * num_test_samples})
y_test_synthetic = np.random.uniform(low=min(y_train), high=max(y_train), size=num_test_samples)

# Predicciones a los datos de prueba
predictions_synthetic = model.predict(X_test_synthetic)

# Comparación de datos reales y datos ficticios
plt.scatter(y_test_synthetic, predictions_synthetic)
plt.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)], color='red', linestyle='--') 
plt.xlabel("Valores reales")
plt.ylabel("Predicciones")
plt.title("Comparación de valores reales vs. predicciones en datos de prueba sintéticos")
plt.show()

mse_synthetic = mean_squared_error(y_test_synthetic, predictions_synthetic)
print("Error cuadrático medio en los datos de prueba sintéticos:", mse_synthetic)