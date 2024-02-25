from owlready2 import *

onto = get_ontology("OntologiaUAM.owx")

with onto:
    class Persona(Thing): pass
    class tienePeso(Persona >> float, FunctionalProperty): pass
    class tieneEstatura(Persona >> float, FunctionalProperty): pass
    class tieneIMC(Persona >> float, FunctionalProperty): pass
    
    rule = Imp()
    rule.set_as_rule("""Persona(?p), tienePeso(?p, ?w), tieneEstatura(?p, ?h), multiply(?altura2, ?h, ?h), divide(?imc, ?w, ?altura2) -> tieneIMC(?p, ?imc)""")    

persona = Persona(tienePeso = 78.3, tieneEstatura = 1.73)
sync_reasoner_pellet(infer_property_values= True, infer_data_property_values = True)

print("El IMC de la Persona es: ", persona.tieneIMC)