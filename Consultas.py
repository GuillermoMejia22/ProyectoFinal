from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Cargar las ontologías RDF/XML
onto = Graph()
onto.parse("RedOntológica\\datosRDF.owl", format="xml")

onto2 = Graph()
onto2.parse("RedOntológica\\personaRDF.owl", format="xml")

onto3 = Graph()
onto3.parse("RedOntológica\\med_atc_rdf.owl", format="xml")

# Definir los prefijos
prefijo = """
    PREFIX paciente: <http://www.modelo.org/datos#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

prefijo2 = """
    PREFIX paciente: <http://www.personas-mexico.org/persona#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

prefijo3 = """
    PREFIX medicamento: <http://www.medicamentos-mexico.org/medicamento#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

def pesosPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?peso ?analisis
    WHERE {
            ?nota paciente:tienePeso ?peso .
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)

    pesos = []
    padecimiento_buscar = "DIABETES"

    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper() and float(row.peso) > 0:
            print("ANALISIS: ", row.analisis)
            pesos.append(float(row.peso))
        
    df = pd.DataFrame({'Peso': pesos})
    fig, ax = plt.subplots(figsize=(12, 6))
    n, bins, patches = plt.hist(df['Peso'], bins=20, alpha=0.7)

    for i, patch in enumerate(patches):
        color = plt.cm.viridis(i / len(patches)) 
        patch.set_facecolor(color)
    
    plt.xlabel('Peso (Kg)')
    plt.ylabel('Número de Casos')
    plt.title(f'PESOS DE PACIENTES DE {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig('ImagenesGeneradas\\pesos_pacientes.png')

    prom = sum(pesos) / len(pesos)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de los pesos es de", prom)
    plt.show()
    

def antecedentesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?historia ?antecedentes
    WHERE {
            ?historia paciente:tieneAntecedentesHeredoFamiliares ?antecedentes .
            ?historia a paciente:Historia_Clinica .
        }
    """
    query = prepareQuery(sparql_query)

    print("Hay pacientes que cuentan con familiares con los siguientes antecedentes familiares:")
    for row in onto.query(query):
        print("Antecedentes: ", row.antecedentes)

def clasificar_IMC(imcs):
    clasificacion = {
        "Delgadez moderada": 0,
        "Delgadez aceptable": 0,
        "Peso Normal": 0,
        "Sobrepeso": 0,
        "Obesidad tipo I": 0,
        "Obesidad tipo II": 0,
        "Obesidad tipo III": 0,
        "Obesidad Extrema": 0
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
            clasificacion["Obesidad tipo III"] += 1
        elif imc >= 50:
            clasificacion["Obesidad Extrema"] += 1

    return clasificacion

def imcPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?imc ?analisis
    WHERE {
            ?nota paciente:tieneIMC ?imc .
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)

    padecimiento_buscar = "DIABETES"
    imcs = []
    
    for row in onto.query(query):
        if float(row.imc) != 0.0:
            if padecimiento_buscar in row.analisis.upper():
                print("IMC:", row.imc)
                print("ANALISIS: ", row.analisis)
                imcs.append(float(row.imc))
            
    prom = sum(imcs) / len(imcs)
    print("De acuerdo con registros de pacientes de Diabetes el promedio del IMC es de ", prom)
    print("Lo cual recae en la categoría del SOBREPESO es por ello que no se debe bajar la guardia incluso si no se tiene obesidad")
    
    clasificacion = clasificar_IMC(imcs)
    categorias = list(clasificacion.keys())
    valores = list(clasificacion.values())

    fig, ax = plt.subplots(figsize=(18, 10))

    # Filtrar categorías y valores cero
    categorias_filtradas = []
    valores_filtrados = []
    for categoria, valor in zip(categorias, valores):
        if valor != 0:
            categorias_filtradas.append(categoria)
            valores_filtrados.append(valor)

    colores = plt.cm.plasma(np.linspace(0, 1, len(categorias_filtradas)))

    bars = plt.bar(categorias_filtradas, valores_filtrados, color=colores)
    plt.xlabel('Categoría de IMC')
    plt.ylabel('Número de Pacientes')
    plt.title('Clasificación de IMC en Pacientes Diabéticos')
    
    plt.xticks(rotation='horizontal', fontsize=8) 
    plt.xticks(range(len(categorias_filtradas)), categorias_filtradas, fontsize=10) 

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom')

    plt.savefig('ImagenesGeneradas\\imc_pacientes.png')
    plt.show()

def edadesPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?edad ?analisis
    WHERE {
            ?nota paciente:tieneEdad ?edad .
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)

    edades = []
    padecimiento_buscar = "DIABETES"

    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper() and int(row.edad) > 0 and float(row.edad) < 1000:
            print("ANALISIS: ", row.analisis)
            edades.append(float(row.edad))
        
    df = pd.DataFrame({'Edad': edades})
    fig, ax = plt.subplots(figsize=(12, 6))
    n, bins, patches = plt.hist(df['Edad'], bins=20, alpha=0.7)

    for i, patch in enumerate(patches):
        color = plt.cm.plasma(i / len(patches)) 
        patch.set_facecolor(color)

    plt.xlabel('Edad')
    plt.ylabel('Número de Casos')
    plt.title(f'EDADES DE PACIENTES DE {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    prom = sum(edades) / len(edades)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de las edades registradas es de ", prom)
    plt.savefig('ImagenesGeneradas\\edades_pacientes.png')

    plt.show()
    
    
def condicionPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?analisis ?biotipo
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tieneBiotipo ?biotipo .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)
    padecimiento_buscar = "DIABETES"
    biotipos = []

    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper():
            condicion = row.biotipo.split("#")        
            print("BIOTIPO: ", condicion[1])
            print("ANALISIS: ", row.analisis)
            biotipos.append(condicion[1])

    biotipos.sort()
    df = pd.DataFrame({'Biotipos': biotipos})

    fig, ax = plt.subplots(figsize=(12, 6))
    n, bins, patches = plt.hist(df['Biotipos'], bins=20, alpha=0.7)

    for i, patch in enumerate(patches):
        color = plt.cm.inferno(i / len(patches)) 
        patch.set_facecolor(color)

    plt.xlabel('Biotipos')
    plt.ylabel('Número de Casos')
    plt.title(f'BIOTIPOS DE PACIENTES DE {padecimiento_buscar}')
    
    for i in range(len(patches)):
        if n[i] > 0:
            ax.text(patches[i].get_x() + patches[i].get_width() / 2, patches[i].get_height() + 5, str(int(n[i])), ha='center')
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\biotipos_pacientes.png')
    plt.show()

def temperaturasPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?analisis ?temperatura
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tieneTemperaturaCorporal ?temperatura .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)
    padecimiento_buscar = "DIABETES"
    temperaturas = []

    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper() and float(row.temperatura) > 0:
            print("ANALISIS: ", row.analisis)
            print("TEMPERATURA CORPORAL: ", row.temperatura)
            temperaturas.append(float(row.temperatura))
    
    prom = sum(temperaturas) / len(temperaturas)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de las temperaturas corporales es de ", prom)
    
    colores = range(len(temperaturas))
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(range(len(temperaturas)), temperaturas, c=colores, cmap='cividis', alpha=0.7)
    plt.xlabel('No. Paciente')
    plt.ylabel('Temperatura Corporal (Grados Celcius)')
    plt.title(f'TEMPERATURAS CORPORALES DE PACIENTES CON {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\temperaturas_pacientes.png')
    plt.show()

def estaturasPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?analisis ?talla
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tieneTalla ?talla .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)
    padecimiento_buscar = "DIABETES"
    estaturas = []

    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper() and float(row.talla) > 0:
            print("ANALISIS: ", row.analisis)
            print("ESTATURA: ", row.talla)
            estaturas.append(float(row.talla))
    
    prom = sum(estaturas) / len(estaturas)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de sus estaturas es de ", prom)
    
    colores = range(len(estaturas))
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(range(len(estaturas)), estaturas, c=colores, cmap='viridis', alpha=0.7)
    plt.xlabel('No. Paciente')
    plt.ylabel('Estatura (metros)')
    plt.title(f'ESTATURAS DE PACIENTES CON {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\estaturas_pacientes.png')
    plt.show()

def presionesPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?analisis ?presionDistolica ?presionSistolica
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tienePresionArterialDistolica ?presionDistolica .
            ?nota paciente:tienePresionArterialSistolica ?presionSistolica .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)
    padecimiento_buscar = "DIABETES"
    presionesDistolicas = []
    presionesSistolicas = []

    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper() and int(row.presionDistolica) > 0 and int(row.presionSistolica) > 0 and int(row.presionDistolica) < 1000 and int(row.presionSistolica) < 1000:
            print("ANALISIS: ", row.analisis)
            print("PRESION ARTERIAL DISTOLICA: ", row.presionDistolica)
            print("PRESION ARTERIAL SISTOLICA: ", row.presionSistolica)
            presionesDistolicas.append(int(row.presionDistolica))
            presionesSistolicas.append(int(row.presionSistolica))
    
    prom = sum(presionesDistolicas) / len(presionesDistolicas)
    prom2 = sum(presionesSistolicas) / len(presionesSistolicas)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de sus presiones diastólicas es es de ", prom)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de sus presiones sistólicas es de ", prom2)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(range(len(presionesDistolicas)), presionesDistolicas, color='blue', label='Presión Diastólica', alpha=0.7)
    plt.scatter(range(len(presionesSistolicas)), presionesSistolicas, color='red', label='Presión Sistólica', alpha=0.7)
    plt.xlabel('No. Paciente')
    plt.ylabel('Nivel de Presión')
    plt.title(f'PRESIÓN DIASTÓLICA Y SISTÓLICA DE PACIENTES CON {padecimiento_buscar}')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('ImagenesGeneradas\\presiones_sanguineas_pacientes.png')
    plt.show()

def frecuenciaRespiratoriaPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?analisis ?frecuencia
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tieneFrecuenciaRespiratoria ?frecuencia .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)
    padecimiento_buscar = "DIABETES"
    frecuencias = []
    
    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper() and int(row.frecuencia) > 0:
            print("ANALISIS: ", row.analisis)
            print("FRECUENCIA RESPIRATORIA: ", row.frecuencia)
            frecuencias.append(int(row.frecuencia))

    prom = sum(frecuencias) / len(frecuencias)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de sus frecuencias respiratorias es de ", prom)
    
    colores = range(len(frecuencias))
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(range(len(frecuencias)), frecuencias, c=colores, cmap='plasma', alpha=0.7)
    plt.xlabel('No. Paciente')
    plt.ylabel('Frecuencia Rsspiratoria (respiraciones por minuto)')
    plt.title(f'FRECUENCIA RESPIRATORIA DE PACIENTES CON {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\frecuencias_respiratorias_pacientes.png')
    plt.show()

def frecuenciaCardiacaPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?analisis ?frecuencia
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tieneFrecuenciaCardiaca ?frecuencia .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)
    padecimiento_buscar = "DIABETES"
    frecuencias = []
    
    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper() and int(row.frecuencia) > 0:
            print("ANALISIS: ", row.analisis)
            print("FRECUENCIA CARDIACA: ", row.frecuencia)
            frecuencias.append(int(row.frecuencia))

    prom = sum(frecuencias) / len(frecuencias)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de sus frecuencias cardíacas es de ", prom)
    
    colores = range(len(frecuencias))
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(range(len(frecuencias)), frecuencias, c=colores, cmap='inferno', alpha=0.7)
    plt.xlabel('No. Paciente')
    plt.ylabel('Frecuencia Cardíaca (pulsaciones por minuto)')
    plt.title(f'FRECUENCIA CARDÍACA DE PACIENTES CON {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\frecuencias_cardiacas_pacientes.png')
    plt.show()

def glucosaPacientesDiabeticos(prefijo, onto):
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
    
    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper():
            print("ANALISIS: ", row.analisis)
            print("COLESTEROL TOTAL: ", row.colesterol)
            niveles_colesterol.append(float(row.colesterol))
            
    prom = sum(niveles_colesterol) / len(niveles_colesterol)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de su colesterol total es de ", prom)
    print("Como se observa es un promedio bastante bueno puesto que En general, se recomienda un nivel de colesterol inferior a los 200 mg/dl. Entre los 200 mg/dl y los 239 mg/dl, el nivel de colesterol se considera elevado o limítrofe y es aconsejable reducirlo. Un nivel de 240 mg/dl o más de colesterol se considera elevado y es necesario tomar medidas para reducirlo. Algunas maneras de reducir el nivel de colesterol son cambiar la alimentación, iniciar un programa de ejercicio físico y tomar medicamentos reductores del colesterol.\n\nFUENTE: https://www.texasheart.org/heart-health/heart-information-center/topics/colesterol/#:~:text=En%20general%2C%20se%20recomienda%20un,necesario%20tomar%20medidas%20para%20reducirlo.")
    
    colores = range(len(niveles_colesterol))
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(range(len(niveles_colesterol)), niveles_colesterol, c=colores, cmap='magma', alpha=0.7)
    plt.xlabel('No. Paciente')
    plt.ylabel('Colesterol Total (mg/dl)')
    plt.title(f'COLESTEROL TOTAL DE PACIENTES CON {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\colesterol_pacientes.png')
    plt.show()

def glucosaPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?analisis ?glucosa
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tieneGlucosa ?glucosa .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)
    padecimiento_buscar = "DIABETES"
    niveles_glucosa = []
    
    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper():
            print("ANALISIS: ", row.analisis)
            print("GLUCOSA: ", row.glucosa)
            niveles_glucosa.append(float(row.glucosa))
    
    prom = sum(niveles_glucosa) / len(niveles_glucosa)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de los niveles de glucosa es de ", prom)
    print("Como se observa el promedio de glucosa es bastante elevado, normalmente el nivel de glucosa en una persona con diabetes es de 126 mg/dl.\n\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/getting-tested.html#:~:text=Los%20valores%20de%20az%C3%BAcar%20en,mayores%20indican%20que%20tiene%20diabetes.&text=Esta%20prueba%20mide%20sus%20niveles,un%20l%C3%ADquido%20que%20contiene%20glucosa.")
    
    colores = range(len(niveles_glucosa))
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(range(len(niveles_glucosa)), niveles_glucosa, c=colores, cmap='cividis', alpha=0.7)
    plt.xlabel('No. Paciente')
    plt.ylabel('Niveles de Glucosa (mg/dl)')
    plt.title(f'NIVELES DE GLUCOSA DE PACIENTES CON {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\glucosa_pacientes.png')
    plt.show()

def insulinaPacientesDiabeticos(prefijo, onto):
    sparql_query = prefijo + """
    SELECT ?nota ?analisis ?insulina
    WHERE {
            ?nota paciente:tieneAnalisis ?analisis .
            ?nota paciente:tieneInsulina ?insulina .
            ?nota a paciente:Nota_Medica .
        }
    """
    query = prepareQuery(sparql_query)
    padecimiento_buscar = "DIABETES"
    niveles_insulina = []
    
    for row in onto.query(query):
        if padecimiento_buscar in row.analisis.upper():
            print("ANALISIS: ", row.analisis)
            print("INSULINA: ", row.insulina)
            niveles_insulina.append(float(row.insulina))
    
    prom = sum(niveles_insulina) / len(niveles_insulina)
    print("De acuerdo con registros de pacientes de Diabetes el promedio de los niveles de insulina es de ", prom)
    print("Como se observa el promedio de insulina es demasiado bajo. Los niveles normales, no diabéticos oscilan entre 60-100mg/dl y 140 mg/dl o menos después de las comidas y aperitivos..\n\nFUENTE: https://dtc.ucsf.edu/es/tipos-de-diabetes/diabetes-tipo-2/tratamiento-de-la-diabetes-tipo-2/medicamentos-y-terapias-2/prescripcion-de-insulina-para-diabetes-tipo-2/informacion-basica-sobre-la-insulina/")
    
    colores = range(len(niveles_insulina))
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(range(len(niveles_insulina)), niveles_insulina, c=colores, cmap='viridis', alpha=0.7)
    plt.xlabel('No. Paciente')
    plt.ylabel('Niveles de Insulina (mg/dl)')
    plt.title(f'NIVELES INSULINA DE PACIENTES CON {padecimiento_buscar}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\insulina_pacientes.png')
    plt.show()

def generoPacientesDiabeticos(prefijo2, onto2):
    sparql_query = prefijo2 + """
    SELECT ?paciente ?sexo
    WHERE {
            ?paciente paciente:tieneSexo ?sexo .
            ?paciente a paciente:Paciente .
        }
    """
    query = prepareQuery(sparql_query)
    
    generos = []
    
    for row in onto2.query(query):
        print("PACIENTE: ", row.paciente)
        print("SEXO: ", row.sexo)
        generos.append(row.sexo)

    df = pd.DataFrame({'generos': generos})

    fig, ax = plt.subplots(figsize=(12, 6))
    n, bins, patches = plt.hist(df['generos'], bins=3, alpha=0.7)

    for i, patch in enumerate(patches):
        color = plt.cm.plasma(i / len(patches)) 
        patch.set_facecolor(color)

    plt.xlabel('Sexo')
    plt.ylabel('Número de Casos')
    plt.title(f'SEXO DE PACIENTES DE DIABETES')
    
    for i in range(len(patches)):
        if n[i] > 0:
            ax.text(patches[i].get_x() + patches[i].get_width() / 2, patches[i].get_height() + 5, str(int(n[i])), ha='center')
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('ImagenesGeneradas\\sexo_pacientes.png')
    plt.show()

def medicamentosPacientesDiabeticos(prefijo3, onto3):
    sparql_query = prefijo3 + """
    SELECT ?medicamento ?generalidad ?nombre ?administracion ?forma ?dosis
    WHERE {
            ?medicamento medicamento:tieneNombre ?nombre .
            ?medicamento medicamento:tieneGeneralidad ?generalidad .
            ?medicamento medicamento:tieneViaDeAdministracion ?administracion .
            ?medicamento medicamento:tieneFormaFarmaceutica ?forma .
            ?medicamento medicamento:tieneDosisIndicada ?dosis .
            ?medicamento a medicamento:Medicamento_De_Cuadro_Basico .
        }
    """
    query2 = prepareQuery(sparql_query)
        
    padecimiento_buscar = "GLUCOSA"
    estado = False
    
    # Tomar uno aleatorio y pasarselo al usuario POSIBLE SOLUCION
    for row in onto3.query(query2):
        if padecimiento_buscar in row.generalidad.upper():
            print("NOMBRE: ", row.nombre)
            print("MEDICAMENTO: ", row.medicamento)
            print("GENERALIDADES: ", row.generalidad)
            via = row.administracion.split("#")        
            print("VÍA DE ADMINISTRACIÓN: ", via[1])
            forma = row.forma.split("#")
            print("FORMA FARMACEUTICA: ", forma[1])
            dosis = row.dosis.split("#")
            print("DOSIS: ", dosis[1])
            sparql_query2 = prefijo3 + """
                SELECT ?medicamento ?cantidadMaxima ?cantidadMinima ?indicacion
                WHERE {
                    ?medicamento medicamento:tieneCantidadMaxima ?cantidadMaxima .
                    ?medicamento medicamento:tieneCantidadMinima ?cantidadMinima .
                    ?medicamento medicamento:tieneIndicacionAdicional ?indicacion .
                    ?medicamento a medicamento:Dosis_Indicada_Para_Adultos .
                }
            """
            query2 = prepareQuery(sparql_query2)
    
            for col in onto3.query(query2):
                dosisTemp = col.medicamento.split("#")
                if dosis[1].strip() == dosisTemp[1].strip():
                    print("DOSIS: ", col.medicamento)
                    print("CANTIDAD MAXIMA: ", col.cantidadMaxima)
                    print("CANTIDAD MINIMA: ", col.cantidadMinima)
                    print("INDICACIÓN ADICIONAL: ", col.indicacion)
            estado = True
    
    if estado == False:
        print("Lo siento, no se tiene registros de medicamentos para la busqueda especificada")

def medicamentosAltPacientesDiabeticos(prefijo3, onto3):
    sparql_query = prefijo3 + """
    SELECT ?medicamento ?generalidad ?nombre
    WHERE {
            ?medicamento medicamento:tieneNombre ?nombre .
            ?medicamento medicamento:tieneGeneralidad ?generalidad .
            ?medicamento a medicamento:Medicamento_De_Catalogo .
        }
    """
    query = prepareQuery(sparql_query)
        
    padecimiento_buscar = "INSULINA"
    estado = False
    
    # Tomar uno aleatorio y pasarselo al usuario POSIBLE SOLUCION
    for row in onto3.query(query):
        if padecimiento_buscar in row.generalidad.upper():
            print("NOMBRE: ", row.nombre)
            print("MEDICAMENTO: ", row.medicamento)
            print("GENERALIDADES: ", row.generalidad)
            estado = True
    
    if estado == False:
        print("Lo siento, no se tiene registros de medicamentos para la busqueda especificada")
        
    
#pesosPacientesDiabeticos(prefijo, onto)
#antecedentesDiabeticos(prefijo, onto)
#imcPacientesDiabeticos(prefijo, onto)
#edadesPacientesDiabeticos(prefijo, onto)
#condicionPacientesDiabeticos(prefijo, onto)
#temperaturasPacientesDiabeticos(prefijo, onto)
#estaturasPacientesDiabeticos(prefijo, onto)
#presionesPacientesDiabeticos(prefijo, onto)
#frecuenciaRespiratoriaPacientesDiabeticos(prefijo, onto)
#frecuenciaCardiacaPacientesDiabeticos(prefijo, onto)
#colesterolPacientesDiabeticos(prefijo, onto)
#glucosaPacientesDiabeticos(prefijo, onto)
#insulinaPacientesDiabeticos(prefijo, onto)
#generoPacientesDiabeticos(prefijo2, onto2)
#medicamentosPacientesDiabeticos(prefijo3, onto3)
#medicamentosAltPacientesDiabeticos(prefijo3, onto3)