from owlready2 import *

onto = get_ontology("OntologiaUAM.owx")

peso = 72.2
estatura = 1.72
edad = 25  # Asegúrate de proporcionar el valor correcto de edad

with onto:
    class Persona(Thing): pass
    class tienePeso(Persona >> float, FunctionalProperty): pass
    class tieneEstatura(Persona >> float, FunctionalProperty): pass
    class tieneEdad(Persona >> int, FunctionalProperty): pass
    class tieneGenero(Persona >> str, FunctionalProperty): pass
    class tieneIMC(Persona >> float, FunctionalProperty): pass
    class tieneTasaMetabolica(Persona >> float, FunctionalProperty): pass
    
    rule = Imp()
    #rule.set_as_rule("""Persona(?p), tienePeso(?p, ?w), tieneEstatura(?p, ?h), multiply(?altura2, ?h, ?h), divide(?imc, ?w, ?altura2) -> tieneIMC(?p, ?imc)""")  
    #rule.set_as_rule("""
    #    Persona(?p), tienePeso(?p, ?w), tieneEstatura(?p, ?h), tieneEdad(?p, ?a), multiply(?op1, ?w, 10), multiply(?op2, ?h, 100), multiply(?op3, ?op2, 10), add(?op4, ?op1, ?op3), multiply(?op5, ?a, 5), subtract(?tasa, ?op4, ?op5) -> tieneTasaMetabolica(?p, ?tasa)
    #""")
    
    rule.set_as_rule("""
        Persona(?p),
        tienePeso(?p, ?w),
        tieneEstatura(?p, ?h),
        tieneEdad(?p, ?a),
    
        multiply(?altura2, ?h, ?h),
        divide(?imc, ?w, ?altura2),
    
        multiply(?op1, ?w, 10),
        multiply(?op2, ?h, 100),
        multiply(?op3, ?op2, 6.25), 
        add(?op4, ?op1, ?op3),
        multiply(?op5, ?a, 5),
        subtract(?tasa, ?op4, ?op5) -> tieneIMC(?p, ?imc), tieneTasaMetabolica(?p, ?tasa)
    """)

persona = Persona(tienePeso=peso, tieneEstatura=estatura, tieneEdad=edad)
sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

print("IMC de la Persona: ", persona.tieneIMC)
print("Tasa Metabolica de la Persona es: ", persona.tieneTasaMetabolica)