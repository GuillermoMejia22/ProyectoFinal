from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
import datetime
from owlready2 import *
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
    
class ActionSaludo(Action):
    
    def name(self) -> Text:
        return "action_saludo"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        saludo = ""
        hora_actual = datetime.datetime.now().hour
        if 5 <= hora_actual < 12:
            saludo = "Hola buenos días me llamo DiaBot ¿cómo estás?"
        elif 12 <= hora_actual < 19:
            saludo = "Hola buenas tardes me llamo Diabot ¿cómo estás?"
        else:
            saludo = "Hola buenas noches me llamo Diabot ¿cómo estás?"
            
        dispatcher.utter_message(saludo)
        
        return []
    
class ActionDespedida(Action):
    
    def name(self) -> Text:
        return "action_despedida"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        despedida = ""
        hora_actual = datetime.datetime.now().hour
        if 5 <= hora_actual < 12:
            despedida = "Hasta luego, ¡Que tengas un lindo día!"
        elif 12 <= hora_actual < 19:
            despedida = "Hasta luego, ¡Que tengas una linda tarde!"
        else:
            despedida = "Hasta luego, ¡Que tengas una linda noche!"
            
        dispatcher.utter_message(despedida)
        
        return []
        
class ActionCalcularIMC(Action):
    
    def name(self) -> Text:
        return "action_calcular_imc"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
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

        imcStr = str(persona.tieneIMC)
        pesoStr = str(peso) + " kg"
        estaturaStr = str(estatura) + " metros"
        edadStr = str(edad)
        
        tasaStr = str(persona.tieneTasaMetabolica)
        
        datos = "El nombre del paciente es " + nombre + " tiene " + edadStr + " años y pesa " + pesoStr + " ,mide " +  estaturaStr + " el genero es " + genero + " y el IMC es " + imcStr
        datos1 = "La tasa metabolica diaria del paciente es de " + tasaStr + " calorías"
        
        dispatcher.utter_message(datos)
        dispatcher.utter_message(datos1)
        
        return []