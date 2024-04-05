from owlready2 import *

nombre = "Luis Perez"
edad = 22
genero = "masculino"
peso = 80
estatura = 1.70

onto = get_ontology("OntologiaUAM.owx")

with onto:
    class Persona(Thing): pass
    class tienePeso(Persona >> float, FunctionalProperty): pass
    class tieneEstatura(Persona >> float, FunctionalProperty): pass
    class tieneEdad(Persona >> int, FunctionalProperty): pass
    class tieneGenero(Persona >> str, FunctionalProperty): pass
    class tieneIMC(Persona >> float, FunctionalProperty): pass
    class tieneTasaMetabolica(Persona >> float, FunctionalProperty): pass
    
    rule = Imp()
            
    if(genero.lower() == "masculino"):
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
            subtract(?tasa, ?op4, ?op5),
            add(?tasaMetabolica, ?tasa, 5) -> tieneIMC(?p, ?imc), tieneTasaMetabolica(?p, ?tasaMetabolica)
        """)
    else:
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
            subtract(?tasa, ?op4, ?op5),
            subtract(?tasaMetabolica, ?tasa, 161) -> tieneIMC(?p, ?imc), tieneTasaMetabolica(?p, ?tasaMetabolica)
        """)
            
persona = Persona(tieneNombre = nombre, tieneGenero = genero, tienePeso = peso, tieneEstatura = estatura, tieneEdad = edad)
sync_reasoner_pellet(infer_property_values= True, infer_data_property_values = True)
onto.save(file="OntologiaPersonas.owl", format="ntriples")