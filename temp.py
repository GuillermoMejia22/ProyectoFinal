from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

onto = Graph()
onto.parse("OntologiaUAMTemp.owl", format="xml")

prefix = """
    PREFIX persona: <http://www.semanticweb.org/alone/ontologies/2024/0/OntologiaUAMTemp#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

sparql_query = prefix + """
        SELECT ?nombre ?edad ?peso ?estatura
        WHERE {
            ?persona persona:tieneNombre ?nombre .
            ?persona persona:tieneEdad ?edad .
            ?persona persona:tienePeso ?peso .
            ?persona persona:tieneEstatura ?estatura .
        }
    """
query = prepareQuery(sparql_query)
    
print("Personas\n")

for row in onto.query(query):
    print("Nombre:", row.nombre)
    print("Edad:", row.edad)
    print("Peso:", row.peso)
    print("Estatura:", row.estatura)
    print("---")