from owlready2 import *

onto = get_ontology("OntologiaUAM.owx")

peso = 100
estatura = 1.72
edad = 25  # Asegúrate de proporcionar el valor correcto de edad
genero = "masculino"
nombre = "Luis"

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
            ubtract(?tasaMetabolica, ?tasa, 161) -> tieneIMC(?p, ?imc), tieneTasaMetabolica(?p, ?tasaMetabolica)
        """)
            
persona = Persona(tieneNombre = nombre, tieneGenero = genero, tienePeso = peso, tieneEstatura = estatura, tieneEdad = edad)
sync_reasoner_pellet(infer_property_values= True, infer_data_property_values = True)

situacion = "Delgadez severa"
recomendacion = "El paciente no tiene riesgo de diabetes PERO se encuentra en una situación delicada llegando al terreno de la anorexia"
imcValue = float(persona.tieneIMC)
if 16 < imcValue <= 16.99: 
    situacion = "Delgadez moderada" 
    recomendacion = "El paciente no tiene riesgo de diabetes PERO está en riesgo de caer en la Anorexia" 
elif 17 <= imcValue <= 18.49: 
    situacion = "Delgadez aceptable" 
    recomendacion = "El paciente está relativamente sano, debe mantenerse así" 
elif 18.5 <= imcValue <= 24.99: 
    situacion = "Peso Normal" 
    recomendacion = "El paciente actualmente tiene un peso regular, debe mantenerse así" 
elif 25 <= imcValue <= 34.99: 
    situacion = "Sobrepeso" 
    recomendacion = "El paciente podría caer en riesgo si NO se cuida" 
elif 30 <= imcValue <= 34.99: 
    situacion = "Obesidad tipo I" 
    recomendacion = "El paciente se encuentra en riesgo de contraer diabetes si NO cambia sus hábitos alimenticios" 
elif 35 <= imcValue <= 40: 
    situacion = "Obesidad tipo II" 
    recomendacion = "El paciente se encuentra en mucho riesgo de padecer diabetes, debe cambiar sus hábitos alimenticios y físicos" 
elif 40 <= imcValue <= 49.99: 
    situacion = "Obesidad tipo III (Obesidad Mórbida)" 
    recomendacion = "El paciente se encuentra en demasiado riesgo de contraer diabetes, debe modificar drásticamente su alimentación y actividad física" 
elif imcValue >= 50: 
    situacion = "Obesidad tipo IV o extrema" 
    recomendacion = "El paciente es casi 100 por ciento seguro que ya tenga diabetes, sin embargo es necesario cambiar su rutina para llevar el tratamiento de la diabetes" 

print(persona.tieneIMC) 
print(situacion) 
print(recomendacion) 