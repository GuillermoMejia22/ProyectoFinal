from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime
import random
from owlready2 import *
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
import mysql.connector
    
class ActionSaludo(Action):
    
    def name(self) -> Text:
        return "action_saludo"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
              
        estado = "EXITO"  
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
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_saludo", estado)
        
        return []

class ActionExplicaTipos(Action):
    
    def name(self) -> Text:
        return "action_explica_tipos"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            estado = "EXITO"
            tipo = tracker.get_slot("tipo")
            tipo = tipo.upper()
            
            if tipo == "1":
                tipo = "I"
            elif tipo == "2":
                tipo = "II"
            elif tipo == "3":
                tipo = "III"
            
            explicaciones = {
                "I": [
                    "Diabetes Tipo 1. Suele aparecer con mayor frecuencia en la juventud, afectando directamente al páncreas al producir poca o nada de insulina.",
                    """
                    La diabetes tipo 1 (anteriormente conocida como insulinodependiente, juvenil o de inicio en la niñez) se caracteriza por una producción deficiente de insulina y requiere la administración diaria de insulina.\n
                    En 2017 había 9 millones de personas con diabetes tipo 1; la mayoría de ellos vive en países de ingresos altos. No se conocen ni su causa ni los medios para prevenirlo.\n
                    Los síntomas incluyen:\n- Excreción excesiva de orina (poliuria).\n- Sed (polidipsia).\n- Hambre constante.\n- Pérdida de peso.\n- Cambios en la visión y fatiga.\n
                    Estos síntomas pueden ocurrir repentinamente.
                    """,
                    "Este tipo de diabetes es la más frecuente en los niños, y en los adultos es la tipo 2, aunque esta última ya se está presentando en la población infantil. Niños desde 8 años de edad han sido diagnosticados con este tipo de diabetes. Afortunadamente es prevenible si se evita el sobrepeso o la obesidad, lo cual es posible lograr a través de una alimentación sana, actividad física y otros hábitos saludables como el dormir correctamente. Fuente: UNAM https://ciencia.unam.mx/leer/1074/diabetes-infantil-diferente-a-la-de-los-adultos-",
                    "Con este tipo de diabetes, el cuerpo no produce insulina. Esto es un problema porque el cuerpo necesita insulina para sacar el azúcar (glucosa) de los alimentos que la persona consume para convertirla en energía. Las personas que tienen diabetes tipo 1 deben tomar insulina todos los días para vivir.\nFUENTE: National Institute of Diabetes and Digestive and Kidney Diseases https://www.niddk.nih.gov/health-information/informacion-de-la-salud/diabetes/informacion-general/control/4-pasos-controlar-vida",
                    "La diabetes tipo 1 es causada por una reacción autoinmunitaria (el cuerpo se ataca a sí mismo por error). Esta reacción impide que su cuerpo produzca insulina. Aproximadamente del 5 al 10% de las personas que tienen diabetes tienen el tipo 1. Por lo general, los síntomas de esta diabetes aparecen rápidamente. Generalmente se diagnostica en niños, adolescentes y adultos jóvenes. Las personas que tienen diabetes tipo 1, deben recibir insulina todos los días para sobrevivir. En la actualidad, nadie sabe cómo prevenir la diabetes tipo 1. FUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetes.html",
                    "Si tienes diabetes tipo 1, tu páncreas no produce insulina o produce muy poca.\n La insulina es una hormona que ayuda a que el azúcar en la sangre entre a las células del cuerpo, donde se puede usar como fuente de energía.\n Sin insulina, el azúcar en la sangre no puede entrar a las células y se acumula en el torrente sanguíneo.\n Tener niveles altos de azúcar en la sangre es dañino para el cuerpo y causa muchos de los síntomas y las complicaciones de la diabetes.\nLa diabetes tipo 1 (que antes se llamaba diabetes insulinodependiente o diabetes juvenil) generalmente se diagnostica en los niños, los adolescentes y los adultos jóvenes, pero puede presentarse en personas de cualquier edad.\nLa diabetes tipo 1 es menos común que la diabetes tipo 2; la tienen aproximadamente entre el 5 y el 10 % de las personas con diabetes.\n En la actualidad, nadie sabe cómo prevenir la diabetes tipo 1; sin embargo, esta enfermedad se puede manejar al seguir las recomendaciones del médico para llevar un estilo de vida saludable, manejar los niveles de azúcar en la sangre, hacerse chequeos regularmente y conseguir educación y apoyo para el automanejo de la diabetes.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/what-is-type-1-diabetes.html"
                ],
                "II": [
                    """
                    Diabetes Tipo 2. Es el tipo de diabetes más común, sucede cuando el cuerpo es incapaz de producir insulina y se acumula la glucosa en la sangre; representa la mayoría de los casos y se manifiesta generalmente en adultos, muchas veces con obesidad o hipertensión.\n En las últimas tres décadas, la prevalencia de la diabetes tipo 2 ha aumentado drásticamente en países de todos los niveles de ingresos.
                    """,
                    """
                    La diabetes tipo 2 (antes llamada no insulinodependiente o de inicio en la edad adulta) es el resultado del uso ineficaz de la insulina por parte del cuerpo. Más del 95% de las personas con diabetes tienen diabetes tipo 2.\nEste tipo de diabetes es en gran parte el resultado del exceso de peso corporal y la inactividad física.\n
                    Los síntomas pueden ser similares a los de la diabetes tipo 1, pero a menudo son menos marcados. Como resultado, la enfermedad puede diagnosticarse varios años después del inicio, después de que ya hayan surgido complicaciones.\nHasta hace poco, este tipo de diabetes solo se observaba en adultos, pero ahora también se presenta cada vez con mayor frecuencia en niños.
                    """,
                    "Con este tipo de diabetes, el cuerpo no produce o no usa bien la insulina. Las personas con este tipo de diabetes tal vez necesiten tomar pastillas o insulina para ayudar a controlar la diabetes. La diabetes tipo 2 es la forma más común de diabetes.\nFUENTE: National Institute of Diabetes and Digestive and Kidney Diseases https://www.niddk.nih.gov/health-information/informacion-de-la-salud/diabetes/informacion-general/control/4-pasos-controlar-vida",
                    "Con la diabetes tipo 2, el cuerpo no usa la insulina adecuadamente y no puede mantener el azúcar en la sangre a niveles normales.\n Aproximadamente del 90 al 95% de las personas con diabetes tiene la diabetes tipo 2.\n Es un proceso que evoluciona a lo largo de muchos años y generalmente se diagnostica en los adultos (si bien se está presentando cada vez más en los niños, los adolescentes y los adultos jóvenes).\n Es posible que no sienta ningún síntoma; por lo tanto, es importante que se haga un análisis de sus niveles de azúcar en la sangre si está en riesgo.\n La diabetes tipo 2 se puede prevenir o retrasar con cambios de estilo de vida saludables, como:\n- Bajar de peso si tiene sobrepeso.\n- Tener una alimentación saludable.\n- Hacer actividad física regularmente.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetes.html"
                ],
                "III": [
                    "De acuerdo con investigaciones de la UNAM pocos saben de la existencia de una forma de la enfermedad que se relaciona con el Alzheimer. Se le conoce coloquialmente como la diabetes tipo 3, un término que ha sido utilizado en tiempos recientes por miembros de la comunidad científica para describir esta relación.\nEl origen de esta propuesta son los estudios que han mostrado que las personas con diabetes tienen un mayor riesgo de desarrollar la enfermedad de Alzheimer en comparación con las personas no diabéticas. De hecho, se estima que las personas con diabetes tienen un riesgo dos veces mayor de desarrollar Alzheimer.\nEl Alzheimer es una enfermedad neurodegenerativa que se caracteriza por la pérdida progresiva de las funciones cognitivas, incluyendo la memoria, el juicio, el razonamiento y el lenguaje. Aunque la causa exacta sigue siendo desconocida, se cree que es el resultado de una compleja interacción entre factores genéticos y ambientales"
                ],
                "GESTACIONAL": [
                    "Diabetes gestacional. Esta se presenta durante el embarazo a causa de los cambios que sufre el cuerpo propios en ese estado y suele darse en una etapa avanzada de la gestación, aunque normalmente desaparece tras dar a luz.",
                    """
                    La diabetes gestacional es una hiperglucemia con valores de glucosa en sangre por encima de lo normal pero por debajo de los diagnósticos de diabetes. La diabetes gestacional ocurre durante el embarazo\n
                    Las mujeres con diabetes gestacional tienen un mayor riesgo de complicaciones durante el embarazo y el parto. Estas mujeres y posiblemente sus hijos también corren un mayor riesgo de padecer diabetes tipo 2 en el futuro.\n
                    La diabetes gestacional se diagnostica mediante pruebas de detección prenatales, en lugar de a través de los síntomas informados.
                    """,
                    " Este tipo de diabetes ocurre en algunas mujeres cuando están embarazadas. La mayoría de las veces, desaparece después de que nace el bebé. Sin embargo, aun si desaparece, estas mujeres y sus hijos corren un mayor riesgo de desarrollar diabetes más adelante.\nFUENTE: National Institute of Diabetes and Digestive and Kidney Diseases https://www.niddk.nih.gov/health-information/informacion-de-la-salud/diabetes/informacion-general/control/4-pasos-controlar-vida",
                    "La diabetes gestacional aparece en mujeres embarazadas que nunca han tenido diabetes. Si usted tiene diabetes gestacional, su bebé podría estar en mayor riesgo de presentar complicaciones de salud. La diabetes gestacional generalmente desaparece después de que nace el bebé. Sin embargo, aumenta el riesgo de que usted tenga diabetes tipo 2 más adelante en la vida. Es más probable que su bebé tenga obesidad cuando sea niño o adolescente y que presente diabetes tipo 2 más adelante en la vida. FUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetes.html",
                    "La diabetes gestacional es un tipo de diabetes que puede aparecer durante el embarazo en las mujeres que no tengan ya diabetes.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/gestational.html"
                ]
            }
            
            explicacion = "El tipo proporcionado NO existe"
            if tipo in explicaciones:
                explicacion = random.choice(explicaciones[tipo])
            
            dispatcher.utter_message("FUENTE ADICIONAL: Organización Panamericana de la Salud https://www.paho.org/es/temas/diabetes")
            dispatcher.utter_message(explicacion)
            
            if tipo == 'I':
                dispatcher.utter_message(image="https://scontent.fmex23-1.fna.fbcdn.net/v/t1.6435-9/67525929_2300921739943741_6832015507223216128_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=5f2048&_nc_ohc=u9YQsKDbw8cAX-eyv_b&_nc_ht=scontent.fmex23-1.fna&oh=00_AfAVjjgawzAWTny4nmF92d2ZoE4ftM096hwTKocMHxJclg&oe=661EB67F")
                dispatcher.utter_message("Las personas que tienen diabetes tipo 1 también pueden tener náuseas, vómitos y dolor de estómago.\n Los síntomas de la diabetes tipo 1 pueden aparecer en apenas unas semanas o meses y pueden ser intensos.\n Este tipo de diabetes generalmente aparece en los niños, los adolescentes o los adultos jóvenes, pero puede presentarse en personas de cualquier edad.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/symptoms.html")
                
            elif tipo == "GESTACIONAL":
                dispatcher.utter_message("Esta infografía disponible en este enlace de la UNAM https://ciencia.unam.mx/contenido/infografia/245/diabetes-en-el-embarazo te puede ser bastante útil")
                dispatcher.utter_message(image="https://ciencia.unam.mx/uploads/infografias/if_embarazo_diabetes_19012022.jpg")
                dispatcher.utter_message("La diabetes gestacional (diabetes durante el embarazo) generalmente aparece en la mitad del embarazo y no suele producir síntomas. Si está embarazada, debe hacerse una prueba para detectar la diabetes gestacional entre las semanas 24 y 28 del embarazo. De esa manera podrá hacer los cambios necesarios para proteger su salud y la del bebé.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/symptoms.html")
                dispatcher.utter_message("Aproximadamente el 50 % de las mujeres con diabetes gestacional presentarán diabetes tipo 2 después")
                
            elif tipo == "II":
                dispatcher.utter_message("Los síntomas de la diabetes tipo 2 generalmente van apareciendo a lo largo de varios años y pueden estar presentes por mucho tiempo sin que se noten (a veces no habrá ningún síntoma notorio). Esta enfermedad generalmente aparece en los adultos, aunque cada vez más se ve en los niños, los adolescentes y los adultos jóvenes. Y, debido a que los síntomas son difíciles de identificar, es importante saber cuáles son los factores de riesgo y que consulte con su médico si tiene alguno.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/symptoms.html")
                
            elif tipo == "III":
                dispatcher.utter_message("En la diabetes tipo 3 —aventuran algunos investigadores—el cerebro se vuelve resistente a la insulina, que básicamente es el regulador de las concentraciones de azúcar en el cuerpo, lo que significa que no puede utilizarla efectivamente para llevar glucosa a las células cerebrales.\nEsta deficiencia se ha relacionado con la acumulación anormal de unas proteínas llamadas beta-amiloides en el cerebro, que son un rasgo característico de la enfermedad de Alzheimer.\nEn otras palabras, si pensamos en nuestro cuerpo como una máquina, la diabetes tipo 3 sería  como un cortocircuito en nuestro cerebro.\nLa insulina es una hormona que ayuda a nuestros cuerpos a usar la glucosa, que es como el combustible que necesitamos para funcionar correctamente. Sin embargo, en la diabetes tipo 3, nuestros cerebros tienen problemas para utilizar la insulina, lo que significa que las células cerebrales no obtienen suficiente energía. Como resultado, este órgano  comienza a funcionar mal y esto puede aumentar el riesgo de desarrollar la enfermedad de Alzheimer. FUENTE: UNAM https://ciencia.unam.mx/leer/1467/-que-sabes-de-la-diabetes-tipo-3-")
                dispatcher.utter_message(image="https://ciencia.unam.mx/uploads/textos/imagenes/ar_diabetes_tipo3_02_20102023.jpg")
            
            dispatcher.utter_message("Este video se me hizo muy interesante, es de los Centros para el Control y la Prevención de Enfermedades, explica un poco acerca de los tipos de diabetes https://www.youtube.com/watch?v=Q7f-UT-cJu8")
            
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
              
        bitacoraBD("action_explica_tipos", estado)
        return [SlotSet("tipo", None)]


class ActionDespedida(Action):
    
    def name(self) -> Text:
        return "action_despedida"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            estado = "EXITO"
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
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_despedida", estado)
        return []
        
class ActionCalcularIMC(Action):
    
    def name(self) -> Text:
        return "action_calcular_imc"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            estado = "EXITO"
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
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_calcular_imc", estado)
        return []
    
class ActionMandaImagen(Action):
    
    def name(self) -> Text:
        return "action_manda_imagen"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            estado = "EXITO"
            ultima_intencion = tracker.latest_message['intent']['name']
            if ultima_intencion == "sospecha_diabetes" or ultima_intencion == "sintomas_diabetes_tipo":
                ultima_intencion = "explicar_sintomas"
            
            respuestas = {
                "explicar_sintomas": {
                    "mensajes": [
                        "El IMSS menciona en el siguiente enlace https://www.imss.gob.mx/preguntas-de-salud/preguntas-frecuentes-sobre-diabetes que algunos de ellos pueden ser:",
                        "Los síntomas son diferentes dependiendo el tipo de la diabetes, pero cuando los niveles de azúcar son altos:\n1.- Se presenta una sensación de mucha hambre y sed.\n2.- Nncluso llegar a perder peso.\n3.- Necesidad de orinar muy a menudo y sentir cansancio.\n4.- Por otro lado, en las personas con diabetes tipo 2 es común no presentar síntomas al inicio, incluso es posible que no los tengan durante muchos años.\nEn estos casos, la detección de la diabetes suele darse mediante un análisis de sangre, pero se puede reconocer la enfermedad ante síntomas como disfunción eréctil, visión borrosa y dolor o entumecimiento en los pies o las manos.",
                        "Los síntomas de la diabetes pueden ocurrir repentinamente. En la diabetes de tipo 2, los síntomas pueden ser leves y tardar muchos años en notarse. Algunos de ellos son:",
                        "En esta infografía puedes ver detalles sobre la diabetes",
                        "Esta infografía habla sobre los síntomas de la diabetes",
                        "Puedes revisar los síntomas en esta infografía, espero te sea de ayuda",
                        "Esta inforgrafía puede ayudarte a comprender un poco más acerca de la diabetes",
                        "Los síntomas más comunes de la diabetes es la polidipsia, es decir, sentir mucha sed; poliuria, que significa orinar con mucha frecuencia, y polifagia, que es una sensación incontenible de hambre todo el tiempo. Quienes tienen este síntoma, a pesar de comer mucho no suben de peso, por el contrario, va disminuyendo. FUENTE: UNAM https://ciencia.unam.mx/leer/1074/diabetes-infantil-diferente-a-la-de-los-adultos-"
                        "Si tiene alguno de los siguientes síntomas de diabetes, vea a su médico para que le haga un análisis del nivel de azúcar en la sangre:\n* Necesidad de orinar (hacer pis) con mucha frecuencia, y también durante la noche.\n* Mucha sed.\n* Pérdida de peso sin intentarlo.\n* Mucha hambre.\n* La visión borrosa.\n* Hormigueo o entumecimiento en las manos o los pies.\n* Mucho cansancio.\n* La piel muy seca.\n* Llagas que cicatrizan muy lentamente.\n* Más infecciones de lo habitualFUENTE: https://www.cdc.gov/diabetes/spanish/basics/symptoms.html"
                    ],
                    "imagenes": [
                        "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Sintomas.png",
                        None,
                        "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/SintomasV2.png",
                        "https://www.gob.mx/cms/uploads/image/file/48304/06Diabetes.jpg",
                        "https://www.medicable.com.mx/AdminMedicable/Pagina/Infografia/Index/Img/388/1.webp",
                        "https://www.fundacionparalasalud.org/upload/publicaciones/25/infografia_signos_y_sintomas.jpg",
                        "https://scontent.fmex26-1.fna.fbcdn.net/v/t1.18169-9/29543026_1610702325645121_2685170007396788526_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=5f2048&_nc_ohc=dd3CqG37KwcAX8nBwL8&_nc_ht=scontent.fmex26-1.fna&oh=00_AfAAVodKFTUEQx_b5W0lOkLlXNh9PKFg4c9g-UgHaBlf4w&oe=661EA68B",
                        None
                    ]
                },
                "mood_triste": {
                    "mensajes": [
                        "Esta imagen siempre me da risa jaja",
                        "Este gatito puede animarte",
                        "Mira este gato jaja",
                        "Mira este perrito",
                        "Mira a este perrito"
                    ],
                    "imagenes": ["https://wallpapers-clan.com/wp-content/uploads/2022/07/funny-cat-17.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcDeTQRyiE4Tbbh7ai-ssCDmFw23-4jbigDaagajHDq7f_7-HBV8vs6mzi1aYHE8PoveA&usqp=CAU", "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Meme.png", "https://estag.fimagenes.com/img/2/T/C/Y/TCY_1024.jpg", "https://i.pinimg.com/550x/c9/9d/69/c99d693ae27767de288085f27a41dde6.jpg"]
                },
                "controlar_diabetes": {
                    "mensajes": [
                        "Existen distintos medicamentos en el mercado que ayudan a bajar el nivel de azúcar en la sangre, suelen ser llamados como hipoglucemiantes, estos acompañados de una buena actividad física, una alimentación sana y seguimiento con un especialista de la salud se puede controlar adecuadamente",
                        "FUENTE: IMSS https://www.imss.gob.mx/preguntas-de-salud/preguntas-frecuentes-sobre-diabetes La participación de la persona que vive con diabetes es necesaria para lograr un buen control de sus niveles de glucosa y una buena calidad de vida, siguiendo las siguientes recomendaciones:",
                        "La diabetes se puede tratar y sus consecuencias se pueden evitar o retrasar con:\na) Dieta\nb) Actividad física\nc) medicación y exámenes y tratamientos regulares para las complicaciones.",
                        "Algunas personas con diabetes de tipo 2 necesitan tomar medicamentos para ayudar a controlar los niveles de azúcar en la sangre. Estos medicamentos se administran en forma de inyección o por otras vías. Algunos de estos medicamentos son:\ni) Metformina.\nii) Sulfonilureas e inhibidores del cotransportador de sodio-glucosa de tipo 2.",
                        "La diabetes es una enfermedad que requiere tratamiento de por vida y, para tener un control adecuado de la enfermedad, es necesario:\nI)Medir su glucosa en sangre antes y dos horas después de cada alimento.\nII) Evitar bebidas azucaradas y productos procesados en general.\nIII) Hacer ejercicio de dos a cinco horas a la semana.\nIV) Acudir a las citas de control con los estudios de seguimiento correspondientes como la hemoglobina glucosilada A1c entre otros."
                    ],
                    "imagenes": [None, "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Recomendacion.png", None, None, None]
                },
                "dieta_diabetes": {
                    "mensajes": [
                        "De acuerdo con información del IMSS en este enlace https://www.imss.gob.mx/preguntas-de-salud/preguntas-frecuentes-sobre-diabetes Debes tener una alimentación que ayude a mantener un nivel adecuado de azúcar en la sangre, puedes acudir con un experto en nutrición para que te recomiende un plan alimenticio. Sobre todo debes:",
                        "Esta infografía muestra información útil sobre la alimentación con diabetes, espero te sea de ayuda :)",
                        "Te paso esta infografía que explica de forma más detallada aspectos relacionados con la alimentación, espero te sea útil :D",
                        "Mira, esta información quiza sea de utilidad para ti",
                        "En general, coma más alimentos que sean ricos en vitaminas y minerales (como calcio y hierro), y fibra. Coma menos alimentos que contengan una mayor cantidad de azúcares agregados, grasas saturadas  y sodio  (sal), y evite las grasas trans. Tenga en cuenta que el % del valor diario de cada nutriente, como la grasa total de 10 % en el ejemplo de abajo, se basa en el consumo de 2000 calorías al día. Usted puede comer menos o más calorías al día dependiendo de su edad, género, nivel de actividad, peso actual y de si está tratando de adelgazar o mantener su peso.\nFUENTE: https://www.cdc.gov/diabetes/spanish/living/eat-well/food-labels.html",
                        "Estos consejos quizá te sean útiles:\n* Elija verduras frescas o cocidas al vapor que tengan muy poco aderezo de ensalada, queso o crema. Si puede, prepare su propio aderezo para ensaladas con un poquito de aceite de oliva y vinagre.\n* Elija granos que tengan mucha fibra, como el arroz integral cocido al vapor y los panes de granos enteros, como los de trigo integral y el pan de maíz.\n* Evite usar mantequilla o margarina en el pan, el arroz y en otros granos y almidones.\n* Elija las frutas frescas, como peras, manzanas, fresas o melones, o una ensalada de frutas sin agregado de azúcar o crema batida. La fruta es una excelente fuente de fibras, vitaminas y minerales.\n* Tome agua, café o té sin endulzar, u otras bebidas sin azúcar.\n* Si toma bebidas alcohólicas, no beba más de un trago al día si es mujer, o más de dos tragos al día si es hombre.\nFUENTE: https://www.cdc.gov/diabetes/spanish/living/buffet-tips-for-diabetes.html"
                    ],
                    "imagenes": ["https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Dieta.png", "https://dimequecomes.com/wp-content/uploads/2019/04/DQC-Infografia-tratamiento-nutricional-diabetes-tipo-II.jpg", "https://alimentacionysalud.unam.mx/wp-content/uploads/2021/02/VIVIR-bien-con-diabetes.jpg", "https://static.wixstatic.com/media/57cfd2_23532047185c4584a6c990bd0dbfb59f~mv2.jpg/v1/fill/w_640,h_556,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/57cfd2_23532047185c4584a6c990bd0dbfb59f~mv2.jpg", None, None]
                },
                "dar_alimentos": {
                    "mensajes": [
                        "Esta infografía puede ayudarte a medir las raciones y porciones", 
                        "Esto puede ayudarte a saber que puedes consumir", 
                        "La mayoría de nosotros simplemente no sabemos cuánto estamos comiendo. Una manera de ayudar a controlar el tamaño de la porción es usar el método del plato.\n* Llene la mitad del plato con alimentos de origen vegetal sin almidón, como lechuga, tomates, ejotes (green beans), zanahorias o brócoli, y frutas como manzanas, toronjas o pomelos, o peras.\n* Llene un cuarto del plato con una proteína sin grasa como pollo, pavo, frijoles, frutos secos, tofu o huevos.\n* Llene un cuarto del plato con cereales y alimentos con almidón como avena y papas. O deje fuera el almidón y sírvase el doble de alimentos de origen vegetal sin almidón. Puede comer todos los alimentos de origen vegetal sin almidón que quiera, siempre y cuando no estén cubiertos con salsa, mantequilla o queso.\nNo siempre comemos de un plato, ¿cierto? Comemos de tazones, paquetes de comida rápida o cajas y envases de comida para llevar. Sin embargo, es realmente la misma idea. Tiene que asegurarse de que su comida tenga una buena proporción de verduras, que no tenga demasiada grasa y que tampoco tenga muchos alimentos con almidón"
                    ],
                    "imagenes": ["https://www.imss.gob.mx/sites/all/statics/salud/infografias/infografia_porcionesyraciones3.jpg", "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Comidas.png", "https://www.cdc.gov/diabetes/images/basics/plate_method_esp.png?_=80584"],                    
                },
                "otros_cuidados": {
                    "mensajes": [
                        "Recomiendo seguir los siguientes cuidados. FUENTE: IMSS https://www.imss.gob.mx/preguntas-de-salud/preguntas-frecuentes-sobre-diabetes",
                        "Una de las partes del cuerpo que más cuidados debe tener es el pie, es por ello que te comparto una infografía de la UNAM dedicada a este tema, espero y sea de utilidad para ti",
                        "Mira, esto quizá pueda ayudarte con la implementación de buenos hábitos"
                    ],
                    "imagenes": ["https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Cuidados.png", "https://ciencia.unam.mx/uploads/infografias/if_pie_diabetico_12102022.jpg", "https://fmdiabetes.org/wp-content/uploads/2020/01/7-habitos-paracuidar-tu-diabetes.png"]
                },
                "explica_hipoglucemia": {
                    "mensajes": [
                        "La hipoglucemia es el término técnico para los niveles bajos de glucosa (azúcar) en la sangre. Es cuando tus niveles de glucosa (azúcar) en la sangre han bajado lo suficiente para que necesites tomar medidas para regresarlos a su rango objetivo. Estas son algunas de las causas: No hay suficiente comida, como una comida o un refrigerio con menos carbohidratos de lo habitual, u omitir una comida o un refrigerio, Alcohol, especialmente con el estómago vacío, Demasiada insulina o medicamentos orales para la diabetes, Efectos secundarios de otros medicamentos y Más actividades físicas o ejercicio de lo habitual FUENTE: American Diabetes Association https://diabetes.org/espanol/la-glucosa-puede-marcar-una-gran-diferencia",
                        "Esta infografía detalla información importante sobre la Hipoglucemia",
                        "Me parece que esta infografía puede ayudarte a comprender la Hipoglucemia",
                        "Esta infografía se me hizo interesante, de hecho explica eso que me dices",
                        "La hipoglucemia (nivel bajo de azúcar en la sangre) puede ocurrir rápido y debe ser tratada de inmediato. En la mayoría de los casos es causada por tener demasiada insulina, esperar demasiado antes de comer, no comer lo suficiente o hacer más actividad física de lo normal.\nLos síntomas de hipoglucemia varían de persona a persona. Asegúrate de saber qué síntomas específicos te provocan a ti. Estos pueden incluir:\n- Temblores\n- Nerviosismo o ansiedad\n- Sudoración, escalofríos o tener la piel fría y húmeda\n- Irritabilidad o impaciencia\n- Mareos y dificultad para concentrarse\n- Hambre o náuseas\n- Visión borrosa\n- Debilidad o fatiga\n- Enojo, terquedad o tristeza\n- Si tienes hipoglucemia varias veces a la semana, habla con tu médico para ver si necesitas un cambio en tu tratamiento.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/what-is-type-1-diabetes.html."
                    ],
                    "imagenes": [None, "https://www.medicable.com.mx/AdminMedicable/Pagina/Infografia/Index/Img/406/1.webp", "https://pbs.twimg.com/media/Dvu1YUiXQAEX9wM.jpg", "https://fmdiabetes.org/wp-content/uploads/2023/02/-1-scaled.jpg", None]
                },
                "explica_insulina": {
                    "mensajes": [
                        "Esta infografía te enseña lo qué es la insulina, espero te sirva",
                        "Aquí está esta infografía que explica eso que requieres, quizá te sea útil",
                        "De hecho la siguiente infografía te puede ayudar a resolver ese cuestionamiento:",
                        "Esta infografía hecha por parte de la UNAm te puede ser útil"
                    ],
                    "imagenes": ["https://www.uaeh.edu.mx/gaceta/3/numero32/octubre/images/luciernaga/3.jpg", "https://i0.wp.com/mimisqui.mx/wp-content/uploads/2020/11/Insulina.png?fit=1200%2C1200&ssl=1", "https://www.medicable.com.mx/AdminMedicable/Pagina/Infografia/Index/Img/156/1.webp", "https://ciencia.unam.mx/uploads/infografias/if_insulina_tus_ideas_final_07062023.png"]
                },
                "conocer_mi_tipo_diabetes": {   
                    "mensajes": [
                        "Mira, quizá esto pueda ayudarte a investigar un poco más al respecto, espero te ayude",
                        "Esta infografía explica de una manera interesante las diferencias entre los tipos de diabetes para ayudar a identificar el detectado, espero te ayude :)",
                        "Esta imagen muestra detalles sobre diabetes tipo I y II, recuerda que lo que diferencia a la gestacional es que ocurre durante la etapa de embarazo",
                        "La diferencia entre una diabetes tipo 1 y una tipo 2, es que en esta última los síntomas se van presentando poco a poco, en tanto que en la tipo 1, pueden desarrollarse en una semana o en un día, es decir, se expresan de manera abrupta. Esto sucede porque cuando se pierde 80% de las células beta del páncreas, se manifiestan los síntomas de forma abrupta.\nEl primer factor de riesgo de la diabetes tipo 2 en la infancia, es que el bebé nazca de una mamá con este padecimiento, o que la desarrolle durante el embarazo es decir, que tenga diabetes gestacional. Igualmente, si padece obesidad, el bebé tendrá un mayor riesgo de llegar a padecer diabetes en una edad temprana. Otros factores que se han observado, son tener otros familiares con diabetes o pertenecer a grupos raciales de riesgo, como ser Latinos, Afroamericanos, Asiáticos, Nativo-Americanos. Fuente: UNAM https://ciencia.unam.mx/leer/1074/diabetes-infantil-diferente-a-la-de-los-adultos-"
                    ],
                    "imagenes": ["https://scontent.fmex5-1.fna.fbcdn.net/v/t31.18172-8/17636973_1375895232453882_6740349638463163133_o.jpg?_nc_cat=102&ccb=1-7&_nc_sid=5f2048&_nc_ohc=waE8nP-K1bcAX8LkzWU&_nc_ht=scontent.fmex5-1.fna&oh=00_AfAkpPtg6yYqp9HZ34JnlL8vOQHJYy66XY1BOtNEuxoBHg&oe=661B19FF", "https://pbs.twimg.com/media/C8HlL3YVwAAUwJ-.jpg", "https://ciencia.unam.mx/uploads/textos/imagenes/ar_diabetes_infantil_18112020.jpg", None]
                },
                "conocer_estadisticas_diabetes": {
                    "mensajes": [
                        "Te paso esta infografía que comparten ciertas estadísticas sobre la Diabetes Mellitus en México",
                        "Esta gráfica te muestra la prevalencia de diabetes de acuerdo al sexo y edades, espero te sirva",
                        "En esta gráfica se observa la tasa de defunciones asociada a la diabetes, con datos hasta 2020. Fuente: gráfico tomado del Comunicado número 592/21 de www.inegi.org.mx",
                        "Esta gráfica registra la tasa de defunciones por diabetes mellitus de acuerdo a la entidad federativa. Fuente: gráfico tomado del Comunicado número 592/21 de www.inegi.org.mx",
                        "Esta representación te dice el porcentaje de la población de 20 años y más con diganóstico previo de diabetes por entidad federativa, espero te sirva"
                    ],
                    "imagenes": ["https://fmdiabetes.org/wp-content/uploads/2020/01/diabetes-en-mexico.jpg", "https://www.gob.mx/cms/uploads/image/file/764378/DIABETES_Ima_gen_3.jpeg", "https://www.mexicosocial.org/wp-content/uploads/2021/10/image-57.png", "https://www.uv.mx/prensa/files/2020/11/111120-Diabetes-en-tiempos-de-Covid-1.jpg"]
                },
                "prediabetes": {
                    "mensajes": [
                        "Esta imagen podría ayudarte a conocer un poco sobre la prediabetes",
                        "Mira, aquí puedes ver en qué consiste la prediabetes y el qué se puede hacer",
                        "Este vídeo del Dr. Alberto Sanagustín explica en qué consiste y cómo se diagnostica https://www.youtube.com/watch?v=0d0p3-yahT4",
                        "En este vídeo de Centers for Disease Control and Prevention se explica qué es la prediabetes, el vídeo originalmente está en inglés pero en Youtube puedes activar los subtitulos al español https://www.youtube.com/watch?v=MrzbFpzt_4s",
                        "La prediabetes es una afección grave en la que los niveles de azúcar en la sangre son más altos que lo normal, pero todavía no han llegado a niveles lo suficientemente altos para que se diagnostique diabetes tipo 2. Fuente: Centros para el Control y la Prevención de Enfermedades https://www.cdc.gov/diabetes/spanish/basics/prediabetes.html",
                        "Con la prediabetes, los niveles de azúcar en la sangre son más altos que lo normal, pero aún no lo suficientemente altos como para un diagnóstico de diabetes tipo 2. La prediabetes aumenta el riesgo de diabetes tipo 2, enfermedad del corazón y derrame cerebral. Pero hay buenas noticias.",
                        "Este video de los Centros para el Control y la Prevención de Enfermedades explica qué es la Prediabetes, pensé que quizá te gustaría verlo :D https://www.youtube.com/watch?v=7zcN5OeG5o4"
                    ],
                    "imagenes": ["https://www.cdc.gov/diabetes/spanish/images/resources/Prediabetes_1.png", "https://fmdiabetes.org/wp-content/uploads/2017/11/me-acaban-de-diagnosticar-predabietes.jpg", None, None, None, None, None]
                },
                "hipertension": {
                    "mensajes": [
                        "La hipertensión y la diabetes están estrechamente relacionadas, y muchas personas que padecen diabetes también tienen hipertensión, y viceversa. Esta infografía de la UNAM puede ayudarte a saber todo lo que necesitas saber de la Hipertensión",
                        "En este vídeo del Dr. Alberto Sanagustín te explica cosas que hay que tener en cuenta de la hipertensión, espero te ayude https://www.youtube.com/watch?v=JDxSoK62gSQ",
                        "La hipertensión arterial es una enfermedad crónica en la que aumenta la presión con la que el corazón bombea sangre a las arterias, para que circule por todo el cuerpo.\nEl sobrepeso y la obesidad pueden aumentar la presión arterial, sube los niveles de glucosa en la sangre, colesterol, triglicéridos y ácido úrico, lo que dificulta que la sangre fluya por el organismo.\nA nivel mundial se estima que existen más de mil millones de personas con hipertensión. En México, se habla de 30 millones y el IMSS se atienden 6 millones de personas que acuden periódicamente a la consulta externa de Medicina Familiar para tratarla. Entre los síntomas se encuentran: Dolor de cabeza intenso, Mareo, Zumbido de oídos, Sensación de ver lucecitas, Visión borrosa, Dolor en el pecho y/o lumbar y Tobillos hinchados. Fuente: IMSS https://www.imss.gob.mx/salud-en-linea/hipertension-arterial",
                        "Se habla de hipertensión cuando la presión de la sangre en nuestros vasos sanguíneos es demasiado alta (de 140/90 mmHg o más). Es un problema frecuente que puede ser grave si no se trata. A veces no causa síntomas y la única forma de detectarla es tomarse la tensión arterial.\nEl riesgo de hipertensión puede aumentar en estos casos:\n* Edad avanzada\n* Causas genéticas\n* Sobrepeso u obesidad\n* Falta de actividad física\n* Comer con mucha sal\n* Beber demasiado alcohol.\nFuente: Organización Mundial de la Salud https://www.who.int/es/news-room/fact-sheets/detail/hypertension"
                    ],
                    "imagenes": ["https://ciencia.unam.mx/uploads/infografias/if_hipertension_16052022.jpg", None, None, None]
                },
                "complicaciones": {
                    "mensajes": [
                        "Con el paso del tiempo se pueden presentar problemas en órganos y ciertas partes del cuerpo (riñones, pies y ojos, entre otros). Tener diabetes también puede aumentar el riesgo de tener enfermedades cardíacas y trastornos en los huesos y articulaciones. Otras complicaciones a largo plazo incluyen problemas con la piel, problemas en el aparato digestivo, disfunción sexual, problemas con dientes y encías. Las personas diabéticas también pueden tener urgencias médicas debido a los niveles muy altos o muy bajos de azúcar en la sangre. La causa puede ser una infección o reacción a algún medicamento. FUENTE: IMSS https://www.imss.gob.mx/preguntas-de-salud/preguntas-frecuentes-sobre-diabetes",
                        "Es una de las primeras causas de infarto, enfermedad vascular cerebral, muerte prematura y la principal responsable de ceguera y amputación no traumática. FUENTE: Instituto de Seguridad y Servicios Sociales de los Trabajadores del Estado https://www.gob.mx/issste/articulos/diabetes-uno-de-los-principales-problemas-de-salud-en-mexico?idiom=es",
                        "La diabetes es una de las principales causas de ceguera, insuficiencia renal, ataques cardíacos, derrames cerebrales y amputación de miembros inferiores. La diabetes mal controlada aumenta las posibilidades de estas complicaciones y la mortalidad prematura. Además, las personas con diabetes tienen mayor riesgo de presentar enfermedades cardiovasculares y tuberculosis, especialmente aquellas con mal control glucémico. FUENTE: Organización Panamericana de la Salud https://www.paho.org/es/temas/diabetes",
                        "Con el tiempo, la diabetes puede dañar el corazón, los vasos sanguíneos, los ojos, los riñones y los nervios. FUENTE: Organización Mundial de la Salud https://www.who.int/es/news-room/fact-sheets/detail/diabetes",
                        "Los adultos con diabetes tienen un riesgo dos o tres veces mayor de sufrir ataques cardíacos y accidentes cerebrovasculares. FUENTE: Organización Panamericana de la Salud https://www.paho.org/es/temas/diabetes",
                        "Combinado con un flujo sanguíneo reducido, la neuropatía (daño a los nervios) en los pies aumenta la posibilidad de úlceras en el pie, infección y eventual necesidad de amputación de una extremidad. FUENTE: Organización Panamericana de la Salud https://www.paho.org/es/temas/diabetes",
                        "La retinopatía diabética es una causa importante de ceguera y se produce como resultado del daño acumulado a largo plazo en los pequeños vasos sanguíneos de la retina. Cerca de 1 millón de personas son ciegas debido a la diabetes. FUENTE: Organización Panamericana de la Salud https://www.paho.org/es/temas/diabetes",
                        "La diabetes es una de las principales causas de insuficiencia renal. FUENTE: Centros para el Control y la Prevención de Enfermedades https://www.cdc.gov/diabetes/spanish/living/diabetes-kidney-disease.html#:~:text=C%C3%B3mo%20la%20diabetes%20causa%20enfermedad,dejar%20de%20funcionar%20como%20deber%C3%ADan",
                        "La diabetes es una causa importante de ceguera, insuficiencia renal, infarto de miocardio, accidente cerebrovascular y amputación de los miembros inferiores. FUENTE: Organización Panamericana de la Salud https://www.paho.org/es/temas/diabetes",
                        "Con el tiempo, la diabetes puede dañar los vasos sanguíneos del corazón, los ojos, los riñones y los nervios. FUENTE: Organización Mundial de la Salud https://www.who.int/es/news-room/fact-sheets/detail/diabetes",
                        "Las personas con diabetes corren más riesgo de sufrir problemas de salud, como infartos de miocardio, derrames cerebrales e insuficiencia renal. FUENTE: Organización Mundial de la Salud https://www.who.int/es/news-room/fact-sheets/detail/diabetes",
                        "La diabetes puede causar pérdida permanente de la visión por daño de los vasos sanguíneos de los ojos. FUENTE: Organización Mundial de la Salud https://www.who.int/es/news-room/fact-sheets/detail/diabetes",
                        "Muchas personas con diabetes presentan problemas en los pies debido al daño causado a los nervios y al flujo sanguíneo insuficiente. Esto puede causar úlceras en los pies y llevar a la amputación. FUENTE: Organización Mundial de la Salud https://www.who.int/es/news-room/fact-sheets/detail/diabetes",
                        "De hecho hay un padecimiento que se puede llegar a generar denominado como Retinopatía Diabética, esta infografía de la UNAM te puede ser útil para entender qué es este padecimiento",
                        "Esta infografía de la UNAM explica las complicaciones y secuelas asociadas a la diabetes, espero te sea de ayuda",
                        "De acuerdo con este enlace de la UNAM https://ciencia.unam.mx/leer/1312/la-diabetes-pone-en-peligro-al-cerebro La diabetes es una de las enfermedades más comunes en la población mexicana. Este padecimiento implica altas concentraciones de azúcar en la sangre, lo que causa una serie de desequilibrios. Recientemente, se ha estudiado cómo el cerebro se ve afectado.\nLos procesos cognitivos abarcan los procesos de aprendizaje y memoria que nos permiten adquirir información y tomar acciones a través de los sentidos y experiencias. Aprender una nueva habilidad, recordar sucesos o incluso sentir emociones, son procesos cognitivos.\nLa Dra. Edith Arnold especifica que los estudios clínicos han evidenciado tres tipos de deterioro de estas capacidades en los enfermos: “La pérdida de la memoria; la disminución en la velocidad del procesamiento de la información; y un déficit de atención y una dificultad para concentrarse y aprender”. se han determinado tres características comunes: la toxicidad por las altas concentraciones de glucosa en la sangre; los daños en la microvasculatura en el cerebro; y una mayor propensión a desarrollar lesiones de arteriosclerosis. Las tres conspiran contra el órgano regente. La toxicidad ocasionada por los altos niveles de glucosa en la sangre se deriva de la peculiaridad de que las células del cerebro, las neuronas, no necesitan la insulina para dar entrada a la glucosa. Es innegociable que tengan energía para poder mantener las comunicaciones y hacer la transmisión de los impulsos nerviosos.",
                        "Las complicaciones crónicas se dividen, a su vez, en las macrovasculares y las microvasculares. Las macrovasculares están asociadas con problemas cardiosvaculares, y las microvasculares son las que dañan la vascularidad de órganos como los riñones, por lo que puede presentarse insuficiencia renal.\nPor otro lado, puede haber daño en la retina y en consecuencia, perder la vista. Igualmente, los pacientes con diabetes es posible que padezcan afectaciones en las vías nerviosas, provocando úlceras en los pies, evolucionando de esta manera al pie diabético que en muchas ocasiones termina en amputación. Fuente: UNAM https://ciencia.unam.mx/leer/1074/diabetes-infantil-diferente-a-la-de-los-adultos-",
                        "Las personas con diabetes tienen probabilidades dos veces mayores de tener enfermedad del corazón o un derrame cerebral que las personas que no tienen diabetes, y de tener estas afecciones a una edad más temprana.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/quick-facts.html",
                        "La diabetes es la principal causa de insuficiencia renal, amputación de las extremidades inferiores y ceguera en los adultos.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/quick-facts.html",
                        "Las personas que tienen diabetes y fuman tienen más probabilidades de presentar problemas graves de salud, como enfermedad del corazón y enfermedad de los riñones.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/quick-facts.html"
                    ],
                    "imagenes": [None, None, None, None, None, None, None, None, None, None, None, None, None, "https://ciencia.unam.mx/uploads/infografias/if_retinopatia_21022022.jpg", "https://ciencia.unam.mx/uploads/infografias/if_diabetes_25032021.jpg", "https://ciencia.unam.mx/uploads/textos/imagenes/ar_cerebro_02_150882022.jpg", None, None, None]
                },
                "preguntar_efectos": {
                    "mensajes": [
                        "La diabetes causa ciertas afectaciones al cuerpo, entre ellas están las siguientes, si gustas puedes preguntarme por más complicaciones de la diabetes",
                        "Las complicaciones más conocidas son la ceguera, amputaciones, infartos y enfermedad renal crónica, sin embargo, cualquier órgano de nuestro cuerpo puede enfermarse si está expuesto a niveles elevados de glucosa por mucho tiempo.\nEstas se dividen en micro y macrovasculares:\n\n*Microvasculares*\n- Retinopatía (complicaciones en los ojos).\n- Neuropatía (complicaciones en los nervios).\n - Nefropatía (complicaciones en los riñones).\n\n*Macrovasculares*\n - Enfermedad vascular periférica (se presenta en el corazón y arterias).\n\nEl principal factor que determina el desarrollo de estas son la exposición crónica a niveles altos de glucosa, que poco a poco daña los vasos arteriales, compromete el flujo adecuado de sangre y daña los tejidos.\nFUENTE: Centro Médico ABC https://centromedicoabc.com/revista-digital/la-diabetes-y-sus-complicaciones-como-llevar-una-vida-sana/"
                    ],
                    "imagenes": ["https://i0.wp.com/post.healthline.com/wp-content/uploads/2022/07/effects-of-diabetes-spanish_1296x1727.jpg?w=1155&h=3626", None]
                },
                "numero_fallecidos": {
                    "mensajes": [
                        "Este gráfico muestra la tasa de defunciones por diabetes mellitus en nuestro país, espero te sea de utilidad",
                        "En México, la mortalidad por diabetes se estima en 89.4 defunciones por cada 100 mil habitantes, siendo la segunda causa de muerte entre la población mexicana, sólo por debajo de las enfermedades del corazón. De acuerdo con las cifras de mortalidad de INEGI, la diabetes fue la causa de 115,681 muertes de mexicanos en el año 2022.",
                        "A nivel entidad, se estima que el estado con la mayor mortalidad por diabetes es Veracruz, con una tasa de 127.4 defunciones por cada 100,000 habitantes, mientras Baja California Sur es la entidad con la menor tasa, con 45.8."
                    ],
                    "imagenes": ["https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/DefuncionesDiabetesMellitus.png", "https://mexicocomovamos.mx/wp-content/uploads/2023/11/Copia-de-Figura1_BlogMCV-5.png", "https://mexicocomovamos.mx/wp-content/uploads/2023/11/Mortalidad-por-diabetes-2022.jpeg"]
                },
                "vivir_con_diabetes": {
                    "mensajes": [
                        "No se vuelve realmente bueno para lidiar con la diabetes de la noche a la mañana. Pero con el tiempo, se aprende a cómo pasar de hacerlo con dificultad a hacerlo en un minuto, para vivir plenamente con diabetes se recomienda lo siguiente:\n- Prepare y coma alimentos saludables.\n- Haga actividad física la mayoría de los días.\n- Mídase el nivel de azúcar en la sangre con frecuencia.\n- Tome los medicamentos como se los recetaron, aunque se sienta bien.\n- Aprenda maneras de manejar el estrés.\n- Sobrelleve los efectos emocionales de la diabetes.\n- Vaya a los chequeos médicos.\nFUENTE: Centros para el Control y la Prevención de Enfermedades https://www.cdc.gov/diabetes/spanish/resources/features/living-well-with-diabetes.html",
                        "Las personas con este padecimiento pueden vivir plenamente cuidandose, la mejor forma de cuidarse es manteniendose activo:\n1.- El ejercicio es todavía una de las mejores herramientas para manejar la diabetes, ¡y es gratis!\n2.- Esfuércese con regularidad, pero también encuentre maneras de ser activo durante el día, como subir escaleras y caminar.\n3.- Haga actividad física con un amigo. Es más probable que siga haciéndola porque no le quiere fallar.\n4.- Intente usar un monitor de actividad (muchas aplicaciones son gratis). Es muy motivador ver como se acumulan sus pasos.\n5.- Vea todos los videos de ejercicios en línea. Hay algo para todos, en cada nivel de actividad física.\nFUENTE: Centros para el Control y la Prevención de Enfermedades https://www.cdc.gov/diabetes/spanish/resources/features/living-well-with-diabetes.html",
                        "Es normal sentirse agobiado, triste o enojado cuando se tiene diabetes. Tal vez usted sepa las medidas que tiene que tomar para mantenerse sano pero se le hace difícil seguir el plan por mucho tiempo.\nPero la clave se basa en:\na) Escojer alimentos bajos en calorías, grasas saturadas, grasas trans, azúcar y sal.\nb) Consumir alimentos con más fibra, como cereales, panes, galletas, arroz o pasta integrales.\nc) Escojer alimentos como frutas, vegetales, granos, panes y cereales integrales, y leche y quesos sin grasa o bajos en grasa.\nd) Tomar agua en lugar de jugos o sodas regulares.\ne) Cuando se sirva, llene la mitad del plato con frutas y vegetales, una cuarta parte del plato con un proteína baja en grasa como frijoles, o pollo o pavo sin el pellejo, y la otra cuarta parte del plato con un cereal integral, como arroz o pasta integral.\nFUENTE: National Institute of Diabetes and Digestive and Kidney Diseases https://www.niddk.nih.gov/health-information/informacion-de-la-salud/diabetes/informacion-general/control/4-pasos-controlar-vida",
                        "La vida con diabetes en ocasiones parece ser bastante complicada pero con una buena alimentación y una actividad física constante se puede vivir bastante bien, quizá estos consejos te sirvan:\ni) Póngase la meta de ser más activo la mayoría de los días de la semana. Empiece despacio caminando por 10 minutos, 3 veces al día.\nii) Dos veces a la semana, trabaje para aumentar su fuerza muscular. Use bandas para ejercicios de resistencia, haga yoga, trabaje duro en el jardín (haciendo huecos y sembrando con herramientas) o haga flexiones de pecho.\niii) Mantenga o logre un peso saludable usando su plan de alimentación y haciendo más ejercicio.\nFUENTE: Centros para el Control y la Prevención de Enfermedades https://www.cdc.gov/diabetes/spanish/resources/features/living-well-with-diabetes.html",
                        "Este video del Centro Médico ABC te habla sobre unos tips para una mejor vida con diabetes https://www.youtube.com/watch?v=QhBCeEdwEVc espero te ayude :)"
                    ],
                    "imagenes": [None, None, None, None, None]
                },
                "manejar_diabetes_tipo_I": {
                    "mensajes": [
                        "Si tienes diabetes tipo 1, deberás ponerte inyecciones de insulina (o usar una bomba de insulina) todos los días para manejar los niveles de azúcar en la sangre y darle a tu cuerpo la energía que necesita. La insulina no se puede tomar en forma de pastilla porque el ácido del estómago la destruiría antes de llegar al torrente sanguíneo. Tu médico trabajará contigo para determinar el tipo y la dosis de insulina más eficaces para ti.\nTambién necesitarás medirte el nivel de azúcar en la sangre con regularidad. Pregúntale a tu médico con qué frecuencia deberás chequearlo y cuál es el nivel de azúcar en la sangre que deberías tener. Mantener los niveles de azúcar en la sangre lo más cerca posible de los valores deseados te ayudará a prevenir o retrasar las complicaciones relacionadas con la diabetes.\nEl estrés es parte de la vida, pero puede hacer que el manejo de la diabetes sea más difícil, lo cual incluye manejar los niveles de azúcar en la sangre y ocuparse de los cuidados diarios de la diabetes. Hacer actividad física regularmente, dormir lo suficiente y hacer ejercicios de relajación pueden ayudar. Habla con tu médico y educador sobre la diabetes acerca de estas y otras maneras de manejar el estrés.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/what-is-type-1-diabetes.html"
                    ],
                    "imagenes": [None]
                },
                "tipos_insulina": {
                    "mensajes": [
                        "La insulina se clasifica según cuán rápido y por cuánto tiempo actúa en el cuerpo.\nSu médico le recetará la mejor insulina o insulinas para usted, con base en varios factores:\n* Su nivel de actividad.\n* Los alimentos que coma.\n* Cuán bien puede manejar sus niveles de azúcar en la sangre.\n* Su edad.\n* Cuánto tiempo le lleva a su cuerpo absorber la insulina y por cuánto tiempo se mantiene activa. (Esto es diferente para distintas personas.)\nSi tiene diabetes tipo 1, probablemente se administrará una combinación de insulinas. Algunas personas con diabetes tipo 2 también necesitarán administrarse insulina.\nEsta tabla comparativa puede ayudarte a comprender los distintos tipos de insulina y características\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/type-1-types-of-insulin.html"
                    ],
                    "imagenes": ["https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/TiposInsulina.png"]
                },
                "causas_azucar_baja": {
                    "mensajes": [
                        "Los niveles de azúcar en la sangre cambian a menudo durante el día. Cuando descienden por debajo de los 70 mg/dL, se considera que el azúcar está bajo. En ese nivel, tiene que tomar medidas para aumentarlo. El azúcar bajo en la sangre es especialmente frecuente en las personas con diabetes tipo 1.\nSaber cómo identificar el azúcar bajo en la sangre es importante porque puede ser peligroso si no se lo trata.\nEntre las causas se encuentran:\n- Administrarse demasiada insulina.\n- No comer suficientes carbohidratos para la cantidad de insulina que se administra.\n- Los momentos en que se administra la insulina.\n- La cantidad de actividad física que hace y cuándo la realiza.\n- Tomar alcohol.\n- La cantidad de grasa, proteínas y fibra en su comida.\n- Tiempo caluroso y húmedo.\n- Cambios inesperados en su horario.\n- Pasar tiempo en altitudes altas.\n- Estar pasando por la pubertad.\n- Menstruación\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/low-blood-sugar.html"
                    ],
                    "imagenes": [None]
                },
                "sintomas_azucar_baja": {
                    "mensajes": [
                        "Cómo usted reacciona a los niveles bajos de azúcar en la sangre quizás no sea igual a cómo reacciona otra persona. Es importante que conozca sus síntomas. Los síntomas frecuentes pueden incluir:* Latidos rápidos\n* Temblores\n* Sudor\n* Nerviosismo o ansiedad\n* Irritabilidad o confusión\n* Mareos\n* Hambre\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/low-blood-sugar.html"                        
                    ],
                    "imagenes": [None]
                },
                "sintomas_cetoacidosis": {
                    "mensajes": [
                        "La cetoacidosis diabética por lo general se produce lentamente. Los primeros síntomas incluyen:\n- Tener mucha sed.\n- Orinar mucho más que lo habitual.\nSi no se la trata, pueden aparecer rápidamente más síntomas intensos, como:\n- Respiración rápida, profunda.\n- Piel y boca secas.\n- Cara enrojecida.\n- Aliento que huele a fruta.\n- Dolor de cabeza.\n- Rigidez o dolores musculares.\n- Mucho cansancio.\n- Náuseas y vómitos.\n- Dolor estomacal.\nA veces, la cetoacidosis diabética es el primer signo de diabetes en las personas a las que todavía no se la han diagnosticado.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetic-ketoacidosis.html"
                    ],
                    "imagenes": [None]
                },
                "causas_cetoacidosis": {
                    "mensajes": [
                        "La cetoacidosis diabética es provocada por niveles muy altos de azúcar en la sangre y niveles bajos de insulina. Las dos causas más frecuentes son:\n* nfermedad. Cuando se enferma, quizás no pueda comer o beber tanto como lo hace habitualmente, lo cual puede dificultarle el manejo del azúcar en la sangre.\n* No inyectarse la insulina cuando le correspondía, tener una obstrucción en la bomba de insulina, o aplicarse la dosis de insulina equivocada.\nOtras causas de la cetoacidosis diabética incluyen:\n* Ataque cardiaco o derrame cerebral.\n* Lesiones físicas, como las producidas en un accidente automovilístico.\n* Consumo de alcohol o drogas.\n* Ciertos medicamentos, como algunos diuréticos (pastillas para orinar) y corticosteroides (usados para tratar la inflamación en el cuerpo).\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetic-ketoacidosis.html"
                    ],
                    "imagenes": [None]
                },
                "tratamiento_cetoacidosis": {
                    "mensajes": [
                        "Si tiene cetoacidosis diabética, lo tratarán en la sala de emergencias o lo hospitalizarán. Su tratamiento probablemente incluirá:\n1.- Reponer el líquido perdido al orinar frecuentemente y para ayudar a diluir el exceso de azúcar en su sangre.\n2.- Reponer los electrolitos (minerales en el cuerpo que ayudan a los nervios, músculos, corazón y cerebro a funcionar de la manera debida). Un nivel demasiado bajo de insulina puede reducir sus niveles de electrolitos.\n3.- Recibir insulina. La insulina revierte las condiciones que causan la cetoacidosis diabética.\n4.- Tomar medicamentos para cualquier enfermedad subyacente que causó la cetoacidosis diabética, como antibióticos por una infección.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetic-ketoacidosis.html"
                    ],
                    "imagenes": [None]
                },
                "prevencion_cetoacidosis": {
                    "mensajes": [
                        "La cetoacidosis diabética es una afección grave, pero usted puede tomar medidas para ayudar a prevenirla:\n* Chequéese el nivel de azúcar en la sangre con frecuencia, especialmente si está enfermo.\n* Mantenga sus niveles de azúcar en la sangre lo más cerca posible de los valores deseados.\n* Tome todos los medicamentos según se los recetaron, aunque se sienta bien.\n* Hable con su médico sobre cómo ajustar su insulina según lo que coma, cuánta actividad física hace, o si está enfermo.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetic-ketoacidosis.html"
                    ],
                    "imagenes": [None]
                },
                "complicaciones_gestacional": {
                    "mensajes": [
                        "La diabetes gestacional puede aumentar el riesgo de tener presión arterial alta durante el embarazo. También puede aumentar el riesgo de que tenga un bebé grande y que le deban hacer una cesárea\nSi usted tiene diabetes gestacional, su bebé estará en mayor riesgo de lo siguiente:\n- Ser muy grande (4.08233 Kg o más), lo cual puede dificultar el parto.\n- Nacer antes de tiempo, lo cual puede causar problemas respiratorios y otros problemas.\n- Tener niveles bajos de azúcar en la sangre.\n- Tener diabetes tipo 2 más adelante en la vida.\nLa diabetes gestacional, por lo general, desaparece después de que nace el bebé. Sin embargo, alrededor del 50 % de las mujeres con diabetes gestacional tendrán diabetes tipo 2 más adelante. Usted puede reducir su riesgo si alcanza un peso corporal saludable después de dar a luz. Visite al médico para que le revise los niveles de azúcar en la sangre de 6 a 12 semanas después de que haya nacido el bebé y luego cada 1 a 3 años para asegurarse de que estén dentro de los valores objetivo.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/gestational.html"
                    ],
                    "imagenes": [None]
                },
                "tratamiento_gestacional": {
                    "mensajes": [
                        "Hay muchas cosas que puede hacer para manejar la diabetes gestacional. Vaya a todas sus citas médicas prenatales y siga su plan de tratamiento, incluidas las siguientes medidas:\n* Revisarse los niveles de azúcar en la sangre para asegurarse de que se mantengan dentro de un rango saludable.\n* Comer alimentos saludables en las cantidades correctas a la hora correspondiente. Seguir un plan de alimentación saludable creado por su médico o dietista.\n* Mantenerse activa. Hacer con regularidad actividad física que sea moderadamente intensa (como caminar rápido) reduce los niveles de azúcar en la sangre y aumenta la sensibilidad de su cuerpo a la insulina, de modo que no necesitará tanta. Asegúrese de preguntarle al médico qué tipo de actividad física puede hacer y si hay algún tipo que deba evitar.\n* Monitorear al bebé. El médico revisará el crecimiento y desarrollo del bebé.\nSi con la alimentación saludable y la actividad física no logra mantener los niveles de azúcar en la sangre bajo control, es posible que el médico le recete insulina, metformina u otro medicamento.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/gestational.html"
                    ],
                    "imagenes": [None]
                },
                "etiquetas_nutricionales": {
                    "mensajes": [
                        "1.- Revise primero el tamaño de la ración. En esta etiqueta, todos los números son para una ración de 2/3 de taza.\n2.- Este paquete tiene 8 raciones. Si usted come el paquete entero, estará consumiendo 8 veces la cantidad de calorías, carbohidratos, grasas, etc. que aparecen en la etiqueta.\n3.- Carbohidratos totales muestra los tipos de carbohidratos que hay en el alimento, incluidos el azúcar y la fibra.\n4.- Elija alimentos con más fibra, vitaminas y minerales.\n5.- Elija alimentos con menos calorías, grasas saturadas, sodio y azúcares agregados. Evite las grasas trans.\nFUENTE: https://www.cdc.gov/diabetes/spanish/living/eat-well/food-labels.html"
                    ],
                    "imagenes": ["https://www.cdc.gov/diabetes/images/managing/food-label.png?_=42561"]
                }
            }
            
            respuesta = respuestas.get(ultima_intencion, {"mensajes": ["Mensaje predeterminado"], "imagenes": [None]})
            mensaje = random.choice(respuesta["mensajes"])
            image_url = respuesta["imagenes"][respuesta["mensajes"].index(mensaje)]
            
            dispatcher.utter_message(text=mensaje)
            
            if image_url:
                dispatcher.utter_message(image=image_url)
        
        except Exception as e:
            estado = "FALLO"            
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(text=error)

        bitacoraBD("action_manda_imagen", estado)
        return []
    
class ActionChecaGlucosa(Action):
    
    def name(self) -> Text:
        return "action_checa_glucosa"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            glucosa_antes = float(tracker.get_slot("glucosa_antes")) if tracker.get_slot("glucosa_antes") else None
            glucosa_despues = float(tracker.get_slot("glucosa_despues")) if tracker.get_slot("glucosa_despues") else None
            
            msg1 = "Resultado del análisis de glucosa en ayuno\n"
            if 70 <= glucosa_antes <= 100:
                diagnostico = "Esos niveles son normales en una persona que NO tiene diabetes, la glucosa en una persona NO diabética en ayuno se debe mantener menor a un valor de 100 mg/dL"
            elif 100 < glucosa_antes <= 130:
                diagnostico = "Esos niveles son normales en una persona que TIENE diabetes, la glucosa en una persona diabética en ayuno se debe mantener menor a un valor de 130 mg/dL"     
            elif glucosa_antes > 130:
                diagnostico = "El nivel de glucosa es bastante alto, lo máximo incluso para una persona diabética en ayuno es de 130 mg/dL"
            
            msg2 = "\nResultado del análisis de glucosa después de comer\n"
            if 70 <= glucosa_despues <= 140:
                diagnostico1 = "Esos niveles son normales en una persona que NO tiene diabetes, la glucosa en una persona NO diabética después de comer se debe mantener menor a un valor de 140 mg/dL"
            elif 140 < glucosa_despues <= 180:
                diagnostico1 = "Esos niveles son normales en una persona que TIENE diabetes, la glucosa en una persona diabética después de comer se debe mantener menor a un valor de 180 mg/dL"     
            elif glucosa_despues > 180:
                diagnostico1 = "El nivel de glucosa es bastante alto, lo máximo incluso para una persona diabética después de comer es de 180 mg/dL\nToda vez que usted esté enfermo o su nivel de azúcar en la sangre sea de 240mg/dL o más, use una prueba de cetonas (que se compra sin receta) para chequear su orina o un medidor para analizar su sangre cada 4 a 6 horas a fin de detectar las cetonas. También debe hacerse una prueba de cetonas si tiene alguno de los síntomas de cetoacidosis diabética."
            
            diagnosticoFinal = msg1 + diagnostico + msg2 + diagnostico1
            
            dispatcher.utter_message(diagnosticoFinal)
            dispatcher.utter_message("Te comparto la fuente donde me basé para checar el nivel, espero te sea útil")
            dispatcher.utter_message(image="https://fmdiabetes.org/wp-content/uploads/2015/06/ADA.png")
        
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_checa_glucosa", estado)
        return [SlotSet("glucosa_antes", None), SlotSet("glucosa_despues", None)]
    
class ActionRecomiendaAlgoDolor(Action):
    
    def name(self) -> Text:
        return "action_recomienda_algo_dolor"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            dolor = tracker.get_slot("dolor")
            dolor = dolor.upper()
            if dolor == "PANZA":
                dolor = "ESTOMAGO"
            elif dolor == "OÍDO" or dolor == "OIDOS":
                dolor = "OIDO"
            
            explicaciones = {
                "CABEZA": [
                    "Una mala hidratación te puede causar un dolor de cabeza.\nDe hecho, los estudios han demostrado que la deshidratación crónica es una causa frecuente de dolores de cabeza causados por tensión y migrañas.\nAfortunadamente, se ha demostrado que beber agua alivia los síntomas del dolor de cabeza en 30 minutos a tres horas, en la mayoría de las personas que sufren de deshidratación.\nAdemás, la deshidratación puede afectar la concentración y causar irritabilidad, lo que hace que tus síntomas parezcan aún peores.\nPara ayudar a evitar los dolores de cabeza por deshidratación, debes concentrarte en beber suficiente agua durante todo el día y comer alimentos con alto contenido de agua.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "El magnesio es un mineral importante necesario para innumerables funciones en el cuerpo, por ejemplo, el control del azúcar en la sangre y la transmisión nerviosa.\nEs interesante que el magnesio también ha demostrado ser un remedio seguro y eficaz para los dolores de cabeza.\nHay evidencia que sugiere que la deficiencia de magnesio es más común en personas que tienen frecuentes dolores de cabeza por migraña, en comparación con aquellos que no los padecen.\nLos estudios demostraron que el tratamiento con 600 mg de citrato de magnesio por vía oral al día ayudó a reducir tanto la frecuencia como la intensidad de las migrañas.\nTomar suplementos de magnesio, sin embargo, puede causar en algunas personas efectos secundarios en el sistema digestivo como diarrea, por lo que, para tratar los síntomas del dolor de cabeza, es mejor comenzar con una dosis más baja.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Si bien, tomar una bebida alcohólica suele no causar dolor de cabeza en la mayoría de personas, los estudios demostraron que el alcohol puede desencadenar migrañas en aproximadamente un tercio de las personas que experimentan dolores de cabeza frecuentes\n.También se ha demostrado que, en muchas personas, el alcohol causa tensión y dolores de cabeza en brote.\nAl actuar como un vasodilatador, el alcohol ensancha los vasos sanguíneos y permite que la sangre fluya más libremente.\nEn algunas personas, la vasodilatación puede causar dolores de cabeza. De hecho, los dolores de cabeza son un efecto secundario frecuente de los medicamentos vasodilatadores, como los que tratan la presión arterial.\nAdemás, el alcohol actúa como diurético, provocando, al orinar con frecuencia, que el cuerpo pierda líquidos y electrolitos. Esta pérdida de líquido puede causar deshidratación, lo que a su vez puede causar o empeorar los dolores de cabeza.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Hay muchas formas en que la falta de sueño afecta la salud. En algunas personas, puede causar dolores de cabeza.\nPor ejemplo, un estudio comparó la frecuencia y la intensidad del dolor de cabeza en aquellos que dormían menos de seis horas por noche y los que dormían más. Se descubrió que los que dormían menos tenían dolores de cabeza más frecuentes e intensos.\nSin embargo, también se ha demostrado que dormir demasiado puede desencadenar dolores de cabeza. Por lo tanto, una cantidad adecuada de descanso es importante para aquellos que buscan la prevención natural del dolor de cabeza.\nPara obtener los máximos beneficios, ten en cuenta que el “punto ideal” es de siete a nueve horas de sueño por noche.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "La histamina es una sustancia química producida por el cuerpo de manera natural que desempeña una función en el sistema inmune, digestivo y nervioso.\nTambién se encuentra en ciertos alimentos como quesos añejos, alimentos fermentados, cerveza, vino, pescado ahumado y embutidos.\nLos estudios sugieren que el consumo de histamina puede causar migrañas en aquellas personas sensibles a esta sustancia.\nAlgunas no pueden excretar la histamina de manera adecuada porque sufren un deterioro en la función de las enzimas responsables de descomponerla.\nUna estrategia útil para las personas que sufren dolores de cabeza frecuentes puede ser eliminar los alimentos ricos en histamina de la dieta.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Los aceites esenciales son líquidos altamente concentrados que contienen compuestos aromáticos de una variedad de plantas.\nTienen muchos beneficios terapéuticos y se usan con mayor frecuencia por vía tópica, aunque algunos se pueden ingerir.\nCuando tienes dolor de cabeza, los aceites esenciales de menta y lavanda son especialmente útiles.\nSe ha demostrado que aplicar aceite esencial de menta en las sienes reduce los síntomas de los dolores de cabeza por tensión.\nPor otro lado, cuando se aplica en el labio superior y se inhala, el aceite de lavanda es muy eficaz para reducir el dolor de migraña y los síntomas asociados.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "El uso de una compresa fría puede ayudar a reducir los síntomas del dolor de cabeza.\nLa aplicación de compresas frías o congeladas en el área del cuello o la cabeza disminuye la inflamación, ralentiza la conducción nerviosa y contrae los vasos sanguíneos, todo lo cual ayuda a aliviar el dolor de cabeza.\nEn un estudio realizado en 28 mujeres, la aplicación de una bolsa de gel frío en la cabeza redujo significativamente el dolor de migraña.\nPara hacer una compresa fría, llena una bolsa impermeable con hielo y envuélvela en una toalla suave.\n Aplica la compresa en la parte posterior del cuello, la cabeza o las sienes para aliviar el dolor de cabeza.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Considera tomar la coenzima Q10.\nLa coenzima Q10 (CoQ10) es una sustancia producida naturalmente por el cuerpo que ayuda a convertir los alimentos en energía y funciona como un poderoso antioxidante.\nLos estudios han demostrado que tomar suplementos de CoQ10 puede ser una forma eficaz y natural de tratar los dolores de cabeza.\nPor ejemplo, un estudio en 80 personas demostró que tomar 100 mg de suplementos de CoQ10 al día redujo la frecuencia, la intensidad y la duración de la migraña.\nOtro estudio que incluyó a 42 personas que experimentaron migrañas frecuentes encontró que tres dosis de 100 mg de CoQ10 durante el día ayudaron a disminuir la frecuencia de la migraña y los síntomas relacionados con la migraña como las náuseas.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Prueba una dieta de eliminación.\nLos estudios sugieren que en algunas personas la intolerancia a ciertos alimentos puede desencadenar dolores de cabeza.\nPara descubrir si un determinado alimento está causando dolores de cabeza frecuentes, prueba una dieta de eliminación que suprima los alimentos comúnmente vinculados con los síntomas del dolor de cabeza.\nLas personas que padecen de migrañas, informan que el queso añejo, el alcohol, el chocolate, las frutas cítricas y el café están entre los desencadenantes de alimentos que se reportan con más frecuencia.\nEn un pequeño estudio, una dieta de eliminación de 12 semanas disminuyó el número de dolores de cabeza por migraña que experimentaron las personas.\n Estos efectos comenzaron a las cuatro semanas.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Bebe té o café con cafeína.\nCuando tienes dolor de cabeza, beber bebidas que contienen cafeína, como el té o el café, puede proporcionar alivio.\nLa cafeína mejora el estado de ánimo, aumenta la atención y contrae los vasos sanguíneos, todo lo cual puede tener un efecto positivo en los síntomas del dolor de cabeza.\nTambién ayuda a aumentar la efectividad de los medicamentos comunes utilizados para tratar los dolores de cabeza, como el ibuprofeno y el acetaminofeno.\nSin embargo, también se ha demostrado que, si una persona consume regularmente grandes cantidades de cafeína y la deja repentinamente, la abstinencia de cafeína le puede causar dolores de cabeza.\nPor lo tanto, las personas que sufren dolores de cabeza frecuentes deben tener en cuenta su consumo de cafeína.\nTambien recuerda que el exceso hace daño.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Prueba la acupuntura.\nLa acupuntura es una técnica de la medicina tradicional china que consiste en insertar agujas finas en la piel para estimular puntos específicos del cuerpo.\nEn muchos estudios, esta práctica se ha relacionado con una reducción en los síntomas de dolor de cabeza.\nUna revisión de 22 estudios que incluyó a más de 4,400 personas encontró que la acupuntura era tan eficaz como los medicamentos comunes para la migraña.\nOtro estudio encontró que la acupuntura era más eficaz y segura que el topiramato, un medicamento anticonvulsivo utilizado para tratar las migrañas crónicas.\nSi estás buscando una forma natural de tratar los dolores de cabeza crónicos, la acupuntura puede ser una opción que valga la pena.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Relájate haciendo yoga.\nPracticar yoga es una excelente manera de aliviar el estrés, aumentar la flexibilidad, disminuir el dolor y mejorar tu calidad de vida en general.\nLa práctica del yoga incluso puede ayudar a reducir la intensidad y la frecuencia de tus dolores de cabeza.\nUn estudio investigó los efectos del yoga como terapia en 60 personas con migrañas crónicas.\n La frecuencia e intensidad del dolor de cabeza se redujeron más en aquellos que recibieron terapia de yoga y atención convencional, en comparación con aquellos que solo recibieron atención convencional.\nOtro estudio encontró que las personas que practicaban yoga durante tres meses tenían una reducción significativa en la frecuencia del dolor de cabeza, la intensidad y los síntomas asociados, en comparación con aquellos que no practicaban yoga.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Prueba con remedios herbales.\nAlgunas hierbas como la matricaria y la petasita pueden reducir los síntomas del dolor de cabeza.\nLa matricaria es una planta con flores que tiene propiedades antiinflamatorias.\nAlgunos estudios sugieren que tomar suplementos de matricaria en dosis de 50-150 mg al día puede reducir la frecuencia del dolor de cabeza.\n Sin embargo, otros estudios no han encontrado ningún beneficio.\nLa raíz de petasita proviene de un arbusto perenne nativo de Alemania y, al igual que la matricaria, tiene efectos antiinflamatorios.\nVarios estudios han demostrado que tomar extracto de petasita en dosis de 50-150 mg reduce los síntomas del dolor de cabeza tanto en adultos como en niños.\nPor lo general, la matricaria se considera segura si se toma en las cantidades recomendadas.\n Sin embargo, la petasita se debe consumir con precaución, ya que las formas no purificadas pueden causar daño hepático y se desconocen los efectos de su uso a largo plazo.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Evita nitratos y nitritos.\nLos nitratos y nitritos son conservantes alimenticios comunes que se agregan a las salchichas, embutidos y tocino para mantenerlos frescos al evitar el crecimiento bacteriano.\nSe ha demostrado que, en algunas personas, los alimentos que los contienen provocan dolores de cabeza.\nLos nitritos pueden desencadenar dolores de cabeza al causar la dilatación de los vasos sanguíneos.\nPara minimizar tu exposición a los nitritos, limita la cantidad de carnes procesadas en tu dieta y siempre que sea posible, elige productos sin nitrato.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Bebe té de jengibre.\nLa raíz de jengibre contiene muchos compuestos beneficiosos, incluidos antioxidantes y sustancias antiinflamatorias.\nUn estudio en 100 personas con migrañas crónicas encontró que 250 mg de polvo de jengibre era tan eficaz como el sumatriptán convencional para el dolor de cabeza para reducir el dolor de la migraña.\nAdemás, el jengibre ayuda a reducir las náuseas y los vómitos, síntomas comunes asociados con dolores de cabeza intensos.\nPuedes tomar jengibre en polvo en forma de cápsula o preparar un té concentrado con raíz de jengibre fresca.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza",
                    "Haz ejercicio.\nUna de las formas más simples de reducir la frecuencia y la intensidad del dolor de cabeza es tener actividad física.\nPor ejemplo, un estudio en 91 personas encontró que 40 minutos de bicicleta fija en interiores tres veces por semana fue más efectivo que las técnicas de relajación para reducir la frecuencia del dolor de cabeza.\nOtro estudio grande que incluyó a más de 92,000 personas mostró que un bajo nivel de actividad física estaba claramente relacionado con un mayor riesgo de dolores de cabeza.\nHay muchas maneras de aumentar tu nivel de actividad, pero uno de los métodos más fáciles es simplemente aumentar tu cantidad de pasos durante el día.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-cabeza"
                ],
                "ESTOMAGO": [
                    "Desde la antigüedad, las personas consideraron el jengibre como una cura para todo, desde dolor hasta náusea.\n No es solamente un cuento antiguo.\n Estudios han demostrado que el jengibre puede ser un tratamiento muy efectivo para algunas clases de molestias estomacales.\nEl jengibre es un antiinflamatorio natural que está disponible en muchas formas, todas pueden ayudar.\n El jengibre masticable y en suplementos es fácil de tomar, mientras otras personas lo prefieren como bebida.\n Prueba una ginger ale completamente natural o corta una raíz de jengibre fresco y prepara un té.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-estomago",
                    "Una buena taza de té de manzanilla puede ayudar a aliviar el dolor de una molestia estomacal, cuando actúa como un antiinflamatorio.\n Estas propiedades antiinflamatorias ayudan a tus músculos estomacales a relajarse, lo cual puede reducir el dolor de los calambres y espasmos.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-estomago",
                    "La dieta BRAT contiene alimentos bajos en fibra y altos en aglutinantes.\n Ninguno de estos alimentos contiene sal o especias, ingredientes que pueden agravar los síntomas.\n Esta dieta blanda es una buena opción para cuando sientes malestar, pero aun así debes comer algo.\n Prueba tostar bastante el pan; se cree que el pan quemado reduce la náusea.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-estomago",
                    "La menta frecuentemente se menciona como una solución útil para la náusea y la molestia estomacal debido a que el mentol en sus hojas es un analgésico natural.\nPrueba:\n- Hervir una taza de menta o té de menta.\n- Oler extracto de menta.\n- Chupar un caramelo de menta masticar hojas de menta.\nEsto debería de reducir los dolores estomacales y aliviar la sensación de náusea.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-estomago",
                    "Si lo puedes digerir, trata de tomar una cucharada de este condimento ácido que seguramente tienes en tu casa para neutralizar la molestia estomacal.\n ¿Es demasiado fuerte? Mezcla una cucharada con una taza de agua y una cucharada de miel y tómalo lentamente.\nLos ácidos en el vinagre de sidra de manzana pueden mejorar la digestión del almidón, lo que permite que este llegue a los intestinos y mantenga saludables las bacterias en esa zona.\n Algunas personas toman una cucharada todos los días como una medida de prevención.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-estomago",
                    "Verás que una almohadilla térmica o una bolsa o botella de agua caliente es un alivio cuando te sientes enfermo, así que acurrúcate con tu manta térmica y relájate hasta que pasen los síntomas.\nEl calor en tu estómago te distraerá de cualquier cólico o dolor, y te puede ayudar a relajar tus músculos y reducir tus náuseas.\n Sin embargo, no lo dejes por mucho tiempo ya que puedes dañar tu piel por el uso excesivo.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-estomago"   
                ],
                "OIDO": [
                    "Hay muchas cosas que puedes hacer en casa para reducir el dolor de oído.\n Prueba estas opciones para aliviar el dolor de oído:.\n* Coloca un paño frío en el oído.\n* Evita empapar el oído.\n* Siéntate erguido para ayudar a aliviar la presión del oído.\n* Utiliza gotas para los oídos de venta libre.\n* Toma analgésicos de venta libre.\n* Mastica goma de mascar para ayudar a aliviar la presión.\nFUENTE: https://www.healthline.com/health/es/dolor-de-oido#remedios-caseros",
                    "Analgésicos de venta libre.\nLa Academia Americana de Pediatría (AAP) recomienda analgésicos de venta libre como el ibuprofeno y el paracetamol para controlar el dolor asociado con una infección de oídos aguda llamada otitis media aguda.\nEstos medicamentos son seguros para utilizarlos con o sin antibióticos, pero asegúrate de seguir las indicaciones de la etiqueta acerca de la dosis.\n Estos medicamentos también pueden ayudar a bajar la fiebre.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    "Compresas frías o tibias.\nLas personas utilizan con frecuencia bolsas de hielo o compresas tibias, como almohadillas térmicas o compresas húmedas, para aliviar el dolor.\n Se puede hacer lo mismo para el dolor de oído.\n Este método es seguro tanto para niños como para adultos.\nColoca la bolsa de hielo o la compresa tibia sobre el oído y alterna entre tibio y frío cada 10 minutos.\n Si prefieres una sola temperatura, ya sea fría o tibia, puedes utilizar una sola compresa.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    "El uso del aceite de oliva para el dolor de oído es un remedio popular.\n No existe evidencia científica sólida que pruebe que las gotas de aceite de oliva en el canal auditivo alivien el dolor de oído.\n Pero colocar unas pocas gotas tibias del aceite en el oído es seguro y podría ser moderadamente efectivo, de acuerdo con la AAP.\nEs una buena idea conversar primero acerca de este método con tu médico, especialmente para niños.\n Utilizando un termómetro, asegúrate de que el aceite no esté más caliente que tu temperatura corporal.\n Esto ayudará a evitar quemaduras en el tímpano.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    "Las gotas naturopáticas están hechas con extractos de hierbas.\n Se pueden encontrar en línea y en algunas farmacias.\n Un estudio reciente encontró que las gotas que contienen extractos de hierbas con base de aceite de oliva pueden ser tan efectivas o incluso mejores que las gotas para los oídos de venta libre tradicionales.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    "Trata de dormir sin poner presión en el oído.\nAlgunas posiciones para dormir empeorarán las infecciones de oído, mientras otras ayudan a aliviarlas.\n Duerme con el oído afectado levantado en lugar de presionarlo contra la almohada.\n Esto puede ayudar a drenar mejor, si es necesario.\nTambién puedes dormir con la cabeza elevada utilizando almohadas extras.\n Esto puede ayudar a que los oídos drenen más rápidamente.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    "Algunos dolores de oído son causados por la presión en el canal auditivo.\n Se pueden hacer ciertos ejercicios para el cuello para aliviar esta presión.\n Los ejercicios de rotación de cuello son particularmente beneficiosos.\nSigue estos pasos para realizar los ejercicios de rotación de cuello.\ni) Siéntate recto con ambos pies apoyados en el piso.\nii) Lentamente rota el cuello y la cabeza a la derecha hasta que esta esté paralela con tu hombro.\niii) Rota la cabeza hacia el otro lado, hasta que esta esté paralela con tu hombro izquierdo.\niv) Levanta los hombros tan alto como si trataras de cubrir los oídos con ellos.\nv) Asegúrate de realizar los movimientos lentamente, mantenlos estirando suavemente hasta contar hasta cinco, luego relájalos.\nvi) Repite estos ejercicios cada vez que te levantes.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    "El jengibre tiene propiedades antiinflamatorias naturales que pueden ayudar a calmar el dolor de oído.\n Aplica jugo de jengibre o aceite calentado con jengibre (tibio) alrededor de la parte externa del canal.\n No lo pongas directamente dentro del oído.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    "El ajo tiene propiedades antibióticas y analgésicas.\n Remoja ajo machacado macerado durante varios minutos en aceite de sésamo o ajonjolí tibio.\n Cuela el ajo y aplica el aceite en el canal auditivo.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    "El agua oxigenada se ha utilizado como remedio natural para el dolor de oído por muchos años.\n Para utilizar este tratamiento, coloca varias gotas de agua oxigenada en el oído afectado.\n Déjala reposar dentro del oído durante varios minutos antes de drenarla en el lavabo.\n Enjuaga tu oído con agua limpia y destilada.\nFUENTE: https://www.healthline.com/health/es/remedios-caseros-para-el-dolor-de-oido",
                    ""
                ]
            }
            
            explicacion = "Lo siento, de momento no tengo alguna recomendación para ese padecimiento"
            if dolor in explicaciones:
                explicacion = random.choice(explicaciones[dolor])
            
            dispatcher.utter_message(explicacion)
            
            if dolor == "ESTOMAGO":
                dispatcher.utter_message("Algunas veces, los problemas estomacales indican una afección más grave. Los vómitos prolongados te ponen en riesgo de deshidratación. Beber pequeños sorbos de agua te puede ayudar a evitar la deshidratación. Visita a un médico si tienes problemas para mantener el agua por más de seis horas.")
            elif dolor == "OIDO":
                dispatcher.utter_message("Los mejores remedios caseros para el dolor de oído dependen de la causa. Si la causa es una caries, es posible que tu dolor de oídos no mejore hasta que veas al dentista. Sin embargo, si es una infección de oído, utilizar un remedio natural puede hacer que la enfermedad sea más llevadera mientras tu cuerpo combate la infección.\nnMuchas infecciones de oído se curan por sí mismas en un período de una a dos semanas, y los síntomas empiezan a mejorar después de unos días. ")
            elif dolor == "CABEZA":
                dispatcher.utter_message("El tratamiento para reducir el dolor de cabeza. Entre ellos, se incluyen la aspirina, el ibuprofeno (Advil, Motrin IB, otros) y el naproxeno sódico (Aleve).\nFUENTE: https://www.mayoclinic.org/es/diseases-conditions/tension-headache/diagnosis-treatment/drc-20353982#:~:text=Analg%C3%A9sicos.,Medicamentos%20combinados.")    
    
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
              
        bitacoraBD("action_recomienda_algo_dolor", estado)
        return [SlotSet("dolor", None)]

class ActionTipoNervios(Action):
    
    def name(self) -> Text:
        return "action_tipo_nervios"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            nervios = tracker.get_slot("nervios")
            nervios = nervios.upper()
            
            if nervios == "PERIFÉRICOS":
                nervios = "PERIFERICOS"
            elif nervios == "AUTÓNOMOS":
                nervios = "AUTONOMOS"
            
            explicaciones = {
                "PERIFERICOS": [
                    "¿Ha tenido la sensación de “pinchazos” u hormigueo en los pies? Quizás sienta como si tuviera medias o guantes puestos, aunque no los tenga.\n Los pies podrían ser muy sensibles al tacto, hasta una sábana puede hacer que duelan.\n Estos son todos síntomas de daños en los nervios periféricos.\nLos daños en los nervios periféricos afectan las manos, los pies, las piernas y los brazos, y son el tipo más común de daños en los nervios en las personas con diabetes.\n Por lo general comienzan en los pies, comúnmente en ambos pies a la vez.\nOtros síntomas pueden incluir:\n- Dolor o mayor sensibilidad, en especial por la noche.\n- Adormecimiento o debilidad.\n- Problemas graves en los pies, como úlceras, infecciones y dolor en los huesos y las articulaciones.\nUsted podría no notar presión o lesiones que causen ampollas o llagas, lo cual puede provocar infecciones, llagas que no se curan o úlceras.\n A veces es necesario amputar (quitar la parte por medio de una operación).\nEncontrar y tratar los problemas de los pies puede reducir sus probabilidades de que presente una infección grave.\nFUENTE: https://www.cdc.gov/diabetes/spanish/resources/features/diabetes-nerve-damage.html"
                ],
                "AUTONOMOS": [
                    "Los daños en los nervios autónomos afectan el corazón, la vejiga, el estómago, los intestinos, los órganos sexuales o los ojos.\n Los síntomas pueden incluir:\n- Problemas en la vejiga o los intestinos que podrían causar pérdida de orina, estreñimiento o diarrea.\n- Náuseas, pérdida del apetito y vómitos.\n- Cambios en cómo los ojos se ajustan de la luz a la oscuridad.\n- Respuesta sexual reducida, incluso problemas para tener erecciones en los hombres o sequedad vaginal en las mujeres.\nFUENTE: https://www.cdc.gov/diabetes/spanish/resources/features/diabetes-nerve-damage.html"
                ],
                "PROXIMALES": [
                    "Los daños en los nervios proximales afectan los nervios de los muslos, las caderas, las nalgas o las piernas.\n También pueden afectar el estómago y el área del pecho.\n Los síntomas pueden incluir:\n- Dolor intenso en una cadera y un muslo o una nalga.\n- Problemas para ponerse de pie desde una posición de sentado.\n- Dolor de estómago intenso.\nFUENTE: https://www.cdc.gov/diabetes/spanish/resources/features/diabetes-nerve-damage.html"
                ],
                "FOCALES": [
                    "Los daños en los nervios focales afectan nervios individuales, más a menudo en una mano, la cabeza, el torso o una pierna.\nLos síntomas pueden incluir:\n- Problemas para enfocar la vista o tener visión doble.\n- Dolores detrás de un ojo.\n- No poder mover un lado de la cara (parálisis de Bell).\n- Adormecimiento u hormigueo en las manos o los dedos.\n- Debilidad en la mano que podría hacer que se le caigan las cosas.\nFUENTE: https://www.cdc.gov/diabetes/spanish/resources/features/diabetes-nerve-damage.html"
                ]
            }
            
            explicacion = "Lo siento, ese tipo de daño a nervios NO existe o NO se encuentra asociado a la diabetes"
            if nervios in explicaciones:
                explicacion = random.choice(explicaciones[nervios])
            
            dispatcher.utter_message(explicacion)
                
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_tipo_nervios", estado)
        return [SlotSet("nervios", None)]
    
class ActionAdministracionInsulina(Action):
    
    def name(self) -> Text:
        return "action_administracion_insulina"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            metodo = tracker.get_slot("metodo")
            metodo = metodo.upper()
            
            explicaciones = {
                "JERINGA": [
                    "Las jeringas y las plumas de insulina administran la insulina a través de una aguja. Las plumas podrían ser más convenientes y puede que a los niños les resulten más cómodas que las jeringas.\nSu médico le dirá cuánta insulina necesita por dosis. Las jeringas de menor capacidad son más fáciles de usar y más precisas.\n- Si su dosis más grande llega casi a la capacidad máxima de la jeringa, compre el próximo tamaño por si esa dosis cambia.\n- Si necesita dosis en medias unidades, escoja una jeringa que las tenga marcadas."
                ],
                "PLUMA": [
                    "Algunas plumas usan cartuchos que se insertan en ellas. Otras se compran ya cargadas y se desechan después de haber usado toda la insulina. La dosis de insulina se marca en la pluma y la insulina se inyecta a través de una aguja.\n* Los cartuchos y las plumas que ya vienen cargadas con insulina contienen solamente un tipo de insulina.\n* Si le recetan dos tipos de insulina, necesitará usar dos plumas.\n\nVentajas de las jeringas y de las plumas\n1.- Las inyecciones requieren menos capacitación que una bomba de insulina para poder usarse.\n2.- Las inyecciones podrían costar menos.\n3.- Las plumas son más fáciles de usar que las jeringas.\n4.- Las plumas son portátiles y discretas.\n5.- Las agujas de las plumas son pequeñas y finas: menos dolor.\n\nDesventajas de las jeringas y de las plumas\n1.- Tanto las jeringas como las plumas son menos privadas que una bomba de insulina.\n2.- No todos los tipos de insulina pueden usarse con una pluma.\n3.- Con una jeringa se pueden mezclar dos tipos de insulina, pero con una pluma no se puede hacer lo mismo."
                ],
                "BOMBA": [
                    "El tamaño de una bomba de insulina es similar al de un teléfono celular pequeño. Le provee una dosis basal de insulina de acción breve o de acción rápida por hora. Cuando usted come o cuando el azúcar en la sangre es alto, usted decide la dosis de insulina y la bomba se la administra.\nLa bomba provee la insulina a través de un tubo plástico delgado, ubicado de manera semipermanente en la capa grasa que se encuentra debajo de su piel, por lo general en el área del estómago o en la parte de atrás de su brazo.\n\nVentajas de las bombas de insulina\n1.- Han demostrado mejorar el nivel de A1c.\n2.- Administran la insulina de manera más precisa.\n3.- Administran la insulina de bolo de manera más fácil.\n4.- Eliminan los efectos impredecibles de la insulina de acción intermedia o de acción prolongada.\n\nDesventajas de las bombas de insulina\n1.- Pueden causar aumento de peso.\n2.- Pueden ser caras.\n3.- Riesgo de infección.\n4.- Pueden ser un recordatorio físico constante de que se tiene diabetes."
                ],
                "INHALADOR": [
                    "La insulina inhalada se administra por medio de un inhalador oral que suministra insulina de acción ultrarrápida al comienzo de las comidas. La insulina inhalada se usa con una insulina inyectable de acción prolongada.\n\nVentajas de la insulina inhalada\n1.- No es una inyección.\n2.- Actúa muy rápido y es tan eficaz como las insulinas inyectables de acción rápida.\n3.- Se puede administrar al principio de las comidas.\n4.- Potencialmente, hay un menor riesgo de presentar un nivel bajo de azúcar en la sangre.\n5.- Menos aumento de peso.\n6.- El dispositivo para inhalar es pequeño.\n\nDesventajas de la insulina inhalada\n1.- Podría causar tos leve o intensa.\n2.- Puede que sea más cara.\n3.- Aún requiere inyecciones o una bomba para la insulina basal.\n4.- La administración de la dosis no es tan precisa."
                ]
            }
            
            explicacion = "Lo siento, ese método de aplicación de insulina no me es familiar :( o tal vez si lo reformulas podría comprenderlo"
            if metodo in explicaciones:
                explicacion = random.choice(explicaciones[metodo])
            
            dispatcher.utter_message(explicacion)
            dispatcher.utter_message("\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/type-1-4-ways-to-take-insulin.html")
                
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
              
        bitacoraBD("action_administracion_insulina", estado)
        return [SlotSet("metodo", None)]
    
class ActionMetodoDeteccion(Action):
    
    def name(self) -> Text:
        return "action_metodo_deteccion"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            metodo = tracker.get_slot("metodo_deteccion")
            metodo = metodo.upper()
            
            explicaciones = {
                "A1C": [
                    "Esta prueba mide el nivel promedio de azúcar en la sangre de los 2 o 3 meses anteriores. Los valores de A1C inferiores a 5.7 % son normales, los valores entre 5.7 y 6.4 % indican que tiene prediabetes y los valores de 6.5 % o mayores indican que tiene diabetes."
                ],
                "AYUNAS": [
                    "Esta prueba mide el nivel de azúcar en la sangre después de ayunar (no comer) toda la noche. Los valores de azúcar en la sangre en ayunas de 99 mg/dl o menores son normales, los de 100 a 125 mg/dl indican que tiene prediabetes y los de 126 mg/dl o mayores indican que tiene diabetes."
                ],
                "TOLERANCIA": [
                    "Esta prueba mide sus niveles de azúcar en la sangre antes y después de beber un líquido que contiene glucosa. Tendrá que ayunar (no comer) la noche anterior a la prueba y le extraerán sangre para determinar sus niveles de azúcar en la sangre en ayunas. Luego tendrá que beber el líquido y le revisarán los niveles de azúcar en la sangre 1 hora, 2 horas y posiblemente 3 horas después. Los valores de azúcar en la sangre de 140 mg/dl o menores a las 2 horas se consideran normales, los valores de 140 a 199 mg/dl indican que tiene prediabetes y los de 200 mg/dl o mayores indican que tiene diabetes."
                ],
                "NO PROGRAMADA": [
                    "Esta prueba mide su nivel de azúcar en la sangre en el momento en que se hace la prueba. Puede hacerse esta prueba en cualquier momento y no es necesario que esté en ayunas (sin comer) antes de hacérsela. Los valores de azúcar en la sangre de 200 mg/dl o mayores indican que tiene diabetes."
                ]
            }
            
            explicacion = "Lo siento, ese método de detección de diabetes no me es familiar :( o tal vez si lo reformulas podría comprenderlo"
            if metodo in explicaciones:
                explicacion = random.choice(explicaciones[metodo])
            
            dispatcher.utter_message(explicacion)
            dispatcher.utter_message("\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/getting-tested.html")
            
            if metodo == "NO PROGRAMADA":
                dispatcher.utter_message(image="https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/PruebaNOprogramada.png")
                dispatcher.utter_message("Si su médico cree que usted tiene diabetes tipo 1, es posible que también le haga un análisis de autoanticuerpos (sustancias que indican si su cuerpo se está atacando a sí mismo) que frecuentemente están presentes en la diabetes tipo 1, pero no en la tipo 2. También le puede hacer un análisis de cetonas en la orina, el cual sirve para indicar que se trata de diabetes tipo 1 y no de diabetes tipo 2. Las cetonas se producen cuando su cuerpo quema grasas como fuente de energía.")
                
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_administracion_insulina", estado)
        return [SlotSet("metodo_deteccion", None)]

class ActionDatoEntrenamiento(Action):
    
    def name(self) -> Text:
        return "action_dato_entrenamiento"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
              
        ultimo_mensaje = tracker.latest_message.get("text")
        estado = "EXITO"
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ServidorRasa"
            )

            cursor = conexion.cursor()

            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sql = "INSERT INTO Entrenamiento_IA (fecha_hora, pregunta) VALUES (%s, %s)"
            valores = (fecha_hora, ultimo_mensaje)

            cursor.execute(sql, valores)

            conexion.commit()

            cursor.close()
            conexion.close()
        
        except Exception as e:
            estado = "FALLO"
            print("Error: ", e)    
            
        bitacoraBD("action_dato_entrenamiento", estado)
        return []
    
class ActionCausasDiabetes(Action):
    
    def name(self) -> Text:
        return "action_causas_diabetes"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            tipo = tracker.get_slot("tipo")
            tipo = tipo.upper()
            
            if tipo == "1":
                tipo = "I"
            elif tipo == "2":
                tipo = "II"
            
            explicaciones = {
                "I": [
                    "Se piensa que la diabetes tipo 1 es causada por una reacción autoinmunitaria (el cuerpo se ataca a sí mismo por error) que destruye las células del páncreas que producen la insulina. Estas células se llaman células beta. Este proceso puede suceder durante meses o años antes de que aparezca algún síntoma. Algunas personas tienen ciertos genes (rasgos que se pasan de padres a hijos) que hacen que sea más probable que presenten diabetes tipo 1; sin embargo, muchas no la tendrán aunque tengan los genes. También se cree que la exposición a un desencadenante en el ambiente, como un virus, podría tener algo que ver con la diabetes tipo 1. La alimentación y los hábitos de estilo de vida no causan la diabetes tipo 1.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/what-is-type-1-diabetes.html",
                    "No está del todo claro qué causa la diabetes tipo 1, pero sabemos que la alimentación y los hábitos relacionados con el estilo de vida no la provocan. Se cree que el tipo 1 es el resultado de una respuesta autoinmunitaria, en la que el cuerpo ataca las células del páncreas que producen insulina. La insulina es una hormona que funciona como una llave que le permite al azúcar en la sangre entrar a las células del cuerpo para ser usado como energía. Algunas veces las infecciones causadas por un virus parecen desencadenar la respuesta autoinmunitaria. Muchas personas con diabetes tipo 1 tienen familiares con este tipo de diabetes, pero la mayoría no. FUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetes-type-1-diagnosis.html"
                ],
                "II": [
                    "El páncreas produce una hormona llamada insulina, que actúa como una llave que permite que el azúcar en la sangre entre a las células del cuerpo para que estas la usen como energía. Si usted tiene diabetes tipo 2, las células no responden de manera normal a la insulina; a esto se lo llama resistencia a la insulina. Para tratar de hacer que las células respondan, el páncreas produce más insulina, pero no podrá mantener el ritmo y los niveles de azúcar en su sangre subirán, lo cual crea las condiciones propicias para la prediabetes y la diabetes tipo 2. Tener niveles altos de azúcar en la sangre es dañino para el cuerpo y puede causar otros problemas de salud graves, como enfermedad del corazón, pérdida de la visión y enfermedad de los riñones.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/type2.html"
                ]
            }
            
            explicacion = "Lo siento, proporcionaste un tipo de diabetes NO valido"
            if tipo in explicaciones:
                explicacion = random.choice(explicaciones[tipo])
            
            dispatcher.utter_message(explicacion)
                            
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_causas_diabetes", estado)
        return [SlotSet("tipo", None)]
    
class ActionSintomasDiabetes(Action):
    
    def name(self) -> Text:
        return "action_sintomas_diabetes"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            tipo = tracker.get_slot("tipo")
            tipo = tipo.upper()
            
            if tipo == "1":
                tipo = "I"
            elif tipo == "2":
                tipo = "II"
            
            explicaciones = {
                "I": [
                    "Pueden pasar varios meses o años antes de que se destruyan suficientes células beta y se noten los síntomas de la diabetes tipo 1. Estos síntomas pueden aparecer en apenas unas semanas o unos meses. Una vez que aparecen, pueden ser intensos. Algunos síntomas de la diabetes tipo 1 son similares a los de otras afecciones. No adivines: si crees que podrías tener diabetes tipo 1, ve a tu médico de inmediato para que te haga una prueba del nivel de azúcar en la sangre. La diabetes que no se trata puede llevar a problemas de salud muy graves, incluso mortales.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/what-is-type-1-diabetes.html"
                ],
                "II": [
                    "Los síntomas de la diabetes tipo 2 generalmente van apareciendo a lo largo de varios años y pueden estar presentes durante mucho tiempo sin que se noten (a veces no habrá ningún síntoma notorio). Y debido a que los síntomas pueden ser difíciles de identificar, es importante saber cuáles son los factores de riesgo y que vea a su médico para que le haga un análisis de sangre si tiene alguno."
                ]
            }
            
            explicacion = "Lo siento, proporcionaste un tipo de diabetes NO valido"
            if tipo in explicaciones:
                explicacion = random.choice(explicaciones[tipo])
            
            dispatcher.utter_message(explicacion)
                            
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_sintomas_diabetes", estado)
        return [SlotSet("tipo", None)]
    
class ActionEdadDiabetes(Action):
    
    def name(self) -> Text:
        return "action_edad_diabetes"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            tipo = tracker.get_slot("tipo")
            tipo = tipo.upper()
            
            if tipo == "1":
                tipo = "I"
            elif tipo == "2":
                tipo = "II"
            
            explicaciones = {
                "I": [
                    "La edad en que con mayor frecuencia se diagnostica la diabetes tipo 1 es alrededor de los 13 o 14 años, pero hay personas que pueden recibir el diagnóstico cuando tienen una edad mucho menor (incluso bebés) o mayor (incluso más de 40 años).\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/diabetes-type-1-diagnosis.html"
                ],
                "II": [
                    "La diabetes tipo 2 generalmente aparece en personas de más de 45 años, pero está apareciendo cada vez más en los niños, los adolescentes y los adultos jóvenes.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/type2.html"
                ]
            }
            
            explicacion = "Lo siento, proporcionaste un tipo de diabetes NO valido"
            if tipo in explicaciones:
                explicacion = random.choice(explicaciones[tipo])
            
            dispatcher.utter_message(explicacion)
                            
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_edad_diabetes", estado)
        return [SlotSet("tipo", None)]

class ActionManejarDiabetes(Action):
    
    def name(self) -> Text:
        return "action_manejar_diabetes"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            estado = "EXITO"
            tipo = tracker.get_slot("tipo")
            tipo = tipo.upper()
            
            if tipo == "1":
                tipo = "I"
            elif tipo == "2":
                tipo = "II"
            
            explicaciones = {
                "I": [
                    "Si tienes diabetes tipo 1, deberás ponerte inyecciones de insulina (o usar una bomba de insulina) todos los días para manejar los niveles de azúcar en la sangre y darle a tu cuerpo la energía que necesita. La insulina no se puede tomar en forma de pastilla porque el ácido del estómago la destruiría antes de llegar al torrente sanguíneo. Tu médico trabajará contigo para determinar el tipo y la dosis de insulina más eficaces para ti. También necesitarás medirte el nivel de azúcar en la sangre con regularidad. Pregúntale a tu médico con qué frecuencia deberás chequearlo y cuál es el nivel de azúcar en la sangre que deberías tener. Mantener los niveles de azúcar en la sangre lo más cerca posible de los valores deseados te ayudará a prevenir o retrasar las complicaciones relacionadas con la diabetes. El estrés es parte de la vida, pero puede hacer que el manejo de la diabetes sea más difícil, lo cual incluye manejar los niveles de azúcar en la sangre y ocuparse de los cuidados diarios de la diabetes. Hacer actividad física regularmente, dormir lo suficiente y hacer ejercicios de relajación pueden ayudar.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/what-is-type-1-diabetes.html"
                ],
                "II": [
                    "Es posible que pueda manejar la diabetes tipo 2 con una alimentación saludable y con actividad física o que su médico le recete insulina, otro medicamento inyectable o medicamentos orales para la diabetes para ayudarlo a controlar los niveles de azúcar en la sangre y evitar las complicaciones. Si se inyecta insulina o toma otros medicamentos, aún necesitará alimentarse de manera saludable y hacer actividad física. También es importante que mantenga la presión arterial y el colesterol bajo control y que se haga las pruebas necesarias de detección. Deberá revisarse el nivel de azúcar en la sangre regularmente. Pregúntele al médico con qué frecuencia se los debe revisar y cuáles son los valores en los que deben estar. Mantener los niveles de azúcar en la sangre lo más cercanos posible a los valores objetivo lo ayudará a prevenir o retrasar las complicaciones relacionadas con la diabetes. El estrés es parte de la vida, pero puede hacer que sea más difícil manejar la diabetes, por ejemplo, controlar los niveles de azúcar en la sangre y ocuparse de los cuidados diarios que requiere la diabetes. Hacer actividad física regularmente, dormir lo suficiente y hacer ejercicios de relajación puede ayudar.\nFUENTE: https://www.cdc.gov/diabetes/spanish/basics/type2.html"
                ]
            }
            
            explicacion = "Lo siento, proporcionaste un tipo de diabetes NO valido"
            if tipo in explicaciones:
                explicacion = random.choice(explicaciones[tipo])
            
            dispatcher.utter_message(explicacion)
                            
        except Exception as e:
            estado = "FALLO"
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
        
        bitacoraBD("action_edad_diabetes", estado)
        return [SlotSet("tipo", None)]

def bitacoraBD(operacion, estado):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ServidorRasa"
        )

        cursor = conexion.cursor()

        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = "INSERT INTO Operaciones (nombre_operacion, fecha_hora, estado) VALUES (%s, %s, %s)"
        valores = (operacion, fecha_hora, estado)

        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()
        conexion.close()
        
    except Exception as e:
        print("Error: ", e)        
