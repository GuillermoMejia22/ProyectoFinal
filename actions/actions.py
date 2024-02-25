from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
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
        hora_actual = datetime.now().hour
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
        hora_actual = datetime.now().hour
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
        edad = tracker.get_slot("edad")
        genero = tracker.get_slot("genero")
        peso = tracker.get_slot("peso")
        estatura = tracker.get_slot("estatura")
                    
        onto = get_ontology("./OntologiaUAM.owx")
        
        with onto:
            class Persona(Thing): pass
            class tienePeso(Persona >> float, FunctionalProperty): pass
            class tieneEstatura(Persona >> float, FunctionalProperty): pass
            class tieneIMC(Persona >> float, FunctionalProperty): pass

            rule = Imp()
            rule.set_as_rule("""Persona(?p), tienePeso(?p, ?w), tieneEstatura(?p, ?h), multiply(?altura2, ?h, ?h), divide(?imc, ?w, ?altura2) -> tieneIMC(?p, ?imc)""")    
        
        persona = Persona(tienePeso = peso, tieneEstatura = estatura)
        sync_reasoner_pellet(infer_property_values= True, infer_data_property_values = True)
        
        datos = nombre + " tienes " + edad + " años, eres del genero " + genero + " pesas " + peso + " mides " + estatura + " y tu IMC es " + persona.tieneIMC
            
        dispatcher.utter_message(datos)
        
        return []