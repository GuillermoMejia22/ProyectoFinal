from owlready2 import *

onto = get_ontology("OntologiaUAM.owx").load()

# Listado de Clases
def listadoClases():
    for class_ in onto.classes():
        print(class_.name)

# Listado Data Properties    
def listadoDataProperties():
    props = {}
    for prop in onto.data_properties():
        props[prop.name] = prop
    print(props)

# Listado de los Individuos (todos)
def listadoIndividuos():
    individuals = {}
    try:
        for instance in onto.individuals():
            if instance.name in individuals:
                print("Individual occurring twice:", {instance.name})
            individuals[instance.name] = instance
    except ValueError:
        raise
    print(individuals)
    