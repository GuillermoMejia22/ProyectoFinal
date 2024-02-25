from owlready2 import *

# Cargar ontología
onto = get_ontology("OntologiaUAM.owx").load()

# Crear instancias y definiciones...

# Ejecutar regla y obtener resultados
with onto:
    sync_reasoner()

    # Definir la consulta SPARQL
    sparql_query = """
        SELECT ?nombreAlu ?nombreProf ?nombreMat
        WHERE {
            ?p a Persona.
            ?a a Alumno.
            ?p a Profesor.
            ?materia a Materia.

            ?p tieneNombrePersona ?nombreProf.
            ?a tieneNombrePersona ?nombreAlu.
            ?materia tieneNombreMateria ?nombreMat.

            ?p esProfesorTitularDe ?materia.
            ?a estaInscritoEn ?materia.
        }
    """

    # Realizar la consulta SPARQL
    results = onto.query_sparql(sparql_query)

# Imprimir resultados
for result in results:
    nombreAlu, nombreProf, nombreMat = result
    print(f"Alumno: {nombreAlu}, Profesor: {nombreProf}, Materia: {nombreMat}")
