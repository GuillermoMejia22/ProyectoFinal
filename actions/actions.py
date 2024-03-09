from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime
import random
import asyncio
from owlready2 import *
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
    
class ActionSaludo(Action):
    
    def name(self) -> Text:
        return "action_saludo"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            saludo = ""
            hora_actual = datetime.datetime.now().hour
            if 5 <= hora_actual < 12:
                saludo = "Hola buenos días me llamo DiaBot ¿cómo estás?"
            elif 12 <= hora_actual < 19:
                saludo = "Hola buenas tardes me llamo Diabot ¿cómo estás?"
            else:
                saludo = "Hola buenas noches me llamo Diabot ¿cómo estás?"
            
            dispatcher.utter_message(saludo)
        
        except Exception as e:
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
              
        return []

class ActionExplicaTipos(Action):
    
    def name(self) -> Text:
        return "action_explica_tipos"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            tipo = tracker.get_slot("tipo")
            tipo = tipo.upper()
            explicacion = "El tipo proporcionado NO existe"
            if tipo == "I" or tipo == "1":
                opcion = random.randint(0, 1)
                if opcion == 0:
                    explicacion = "Diabetes Tipo 1. Suele aparecer con mayor frecuencia en la juventud, afectando directamente al páncreas al producir poca o nada de insulina." 
                else:
                    explicacion = """
                        La diabetes tipo 1 (anteriormente conocida como insulinodependiente, juvenil o de inicio en la niñez) se caracteriza por una producción deficiente de insulina y requiere 
                        la administración diaria de insulina. En 2017 había 9 millones de personas con diabetes tipo 1; la mayoría de ellos vive en países de ingresos altos. No se conocen ni su 
                        causa ni los medios para prevenirlo.\n
                        Los síntomas incluyen excreción excesiva de orina (poliuria), sed (polidipsia), hambre constante, pérdida de peso, cambios en la visión y fatiga. 
                        Estos síntomas pueden ocurrir repentinamente.
                    """
            elif tipo == "II" or tipo == "2":
                opcion = random.randint(0, 1)
                if opcion == 0:
                    explicacion = """
                        Diabetes Tipo 2. Es el tipo de diabetes más común, sucede cuando el cuerpo es incapaz de producir insulina y se acumula la glucosa en la sangre; representa la mayoría de 
                        los casos y se manifiesta generalmente en adultos, muchas veces con obesidad o hipertensión. En las últimas tres décadas, la prevalencia de la diabetes tipo 2 ha aumentado 
                        drásticamente en países de todos los niveles de ingresos."
                    """
                else:
                    explicacion = """
                        La diabetes tipo 2 (antes llamada no insulinodependiente o de inicio en la edad adulta) es el resultado del uso ineficaz de la insulina por parte del cuerpo. Más del 95% de 
                        las personas con diabetes tienen diabetes tipo 2. Este tipo de diabetes es en gran parte el resultado del exceso de peso corporal y la inactividad física.\n
                        Los síntomas pueden ser similares a los de la diabetes tipo 1, pero a menudo son menos marcados. Como resultado, la enfermedad puede diagnosticarse varios años después del 
                        inicio, después de que ya hayan surgido complicaciones. \nHasta hace poco, este tipo de diabetes solo se observaba en adultos, pero ahora también se presenta cada vez con mayor frecuencia en niños."
                    """
            elif tipo == "GESTACIONAL":
                opcion = random.randint(0, 1)
                if opcion == 0:
                    explicacion = "Diabetes gestacional. Esta se presenta durante el embarazo a causa de los cambios que sufre el cuerpo propios en ese estado y suele darse en una etapa avanzada de la gestación, aunque normalmente desaparece tras dar a luz."
                else:
                    explicacion = """
                        La diabetes gestacional es una hiperglucemia con valores de glucosa en sangre por encima de lo normal pero por debajo de los diagnósticos de diabetes. La diabetes gestacional ocurre durante el embarazo\n
                        Las mujeres con diabetes gestacional tienen un mayor riesgo de complicaciones durante el embarazo y el parto. Estas mujeres y posiblemente sus hijos también corren un mayor riesgo de padecer diabetes tipo 2 en el futuro.\n
                        La diabetes gestacional se diagnostica mediante pruebas de detección prenatales, en lugar de a través de los síntomas informados.
                    """
            dispatcher.utter_message("De acuerdo con el Gobierno de México")    
            dispatcher.utter_message(explicacion)
        
        except Exception as e:
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
              
        return [SlotSet("tipo", None)]

class ActionDespedida(Action):
    
    def name(self) -> Text:
        return "action_despedida"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            despedida = ""
            hora_actual = datetime.datetime.now().hour
            if 5 <= hora_actual < 12:
                despedida = "Hasta luego, ¡Que tengas un lindo día!"
            elif 12 <= hora_actual < 19:
                despedida = "Hasta luego, ¡Que tengas una linda tarde!"
            else:
                despedida = "Hasta luego, ¡Que tengas una linda noche!"
            
            dispatcher.utter_message(despedida)
        
        except Exception as e:
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        return []
        
class ActionCalcularIMC(Action):
    
    def name(self) -> Text:
        return "action_calcular_imc"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            nombre = tracker.get_slot("nombre")
            edad = int(tracker.get_slot("edad"))
            genero = tracker.get_slot("genero")
            peso = float(tracker.get_slot("peso")) if tracker.get_slot("peso") else None
            estatura = float(tracker.get_slot("estatura")) if tracker.get_slot("estatura") else None

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
            
            imcStr = str(persona.tieneIMC)
            pesoStr = str(peso) + " kg"
            estaturaStr = str(estatura) + " metros"
            edadStr = str(edad) + " años"
        
            tasaStr = str(persona.tieneTasaMetabolica)
        
            msg0 = "El nombre del paciente es " + nombre + " tiene " + edadStr + " y pesa " + pesoStr + ", mide " +  estaturaStr + " el genero es " + genero + " y el IMC es " + imcStr
            msg1 = "La tasa metabolica diaria del paciente es de " + tasaStr + " calorías"
            msg2 = "La condición actual de tu paciente es de " + situacion
            
            dispatcher.utter_message(msg0)
            dispatcher.utter_message(msg1)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(recomendacion)
        
        except Exception as e:
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        return []