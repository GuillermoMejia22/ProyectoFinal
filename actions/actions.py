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
                    "Este tipo de diabetes es la más frecuente en los niños, y en los adultos es la tipo 2, aunque esta última ya se está presentando en la población infantil. Niños desde 8 años de edad han sido diagnosticados con este tipo de diabetes. Afortunadamente es prevenible si se evita el sobrepeso o la obesidad, lo cual es posible lograr a través de una alimentación sana, actividad física y otros hábitos saludables como el dormir correctamente. Fuente: UNAM https://ciencia.unam.mx/leer/1074/diabetes-infantil-diferente-a-la-de-los-adultos-"
                ],
                "II": [
                    """
                    Diabetes Tipo 2. Es el tipo de diabetes más común, sucede cuando el cuerpo es incapaz de producir insulina y se acumula la glucosa en la sangre; representa la mayoría de los casos y se manifiesta generalmente en adultos, muchas veces con obesidad o hipertensión.\n En las últimas tres décadas, la prevalencia de la diabetes tipo 2 ha aumentado drásticamente en países de todos los niveles de ingresos.
                    """,
                    """
                    La diabetes tipo 2 (antes llamada no insulinodependiente o de inicio en la edad adulta) es el resultado del uso ineficaz de la insulina por parte del cuerpo. Más del 95% de las personas con diabetes tienen diabetes tipo 2.\nEste tipo de diabetes es en gran parte el resultado del exceso de peso corporal y la inactividad física.\n
                    Los síntomas pueden ser similares a los de la diabetes tipo 1, pero a menudo son menos marcados. Como resultado, la enfermedad puede diagnosticarse varios años después del inicio, después de que ya hayan surgido complicaciones. \n
                    Hasta hace poco, este tipo de diabetes solo se observaba en adultos, pero ahora también se presenta cada vez con mayor frecuencia en niños.
                    """
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
                    """
                ]
            }
            
            explicacion = "El tipo proporcionado NO existe"
            if tipo in explicaciones:
                explicacion = random.choice(explicaciones[tipo])
            
            dispatcher.utter_message("FUENTE: Organización Panamericana de la Salud https://www.paho.org/es/temas/diabetes")
            dispatcher.utter_message(explicacion)
            if tipo == 'I':
                dispatcher.utter_message(image="https://scontent.fmex23-1.fna.fbcdn.net/v/t1.6435-9/67525929_2300921739943741_6832015507223216128_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=5f2048&_nc_ohc=u9YQsKDbw8cAX-eyv_b&_nc_ht=scontent.fmex23-1.fna&oh=00_AfAVjjgawzAWTny4nmF92d2ZoE4ftM096hwTKocMHxJclg&oe=661EB67F")
            
            elif tipo == "GESTACIONAL":
                dispatcher.utter_message("Esta infografía disponible en este enlace de la UNAM https://ciencia.unam.mx/contenido/infografia/245/diabetes-en-el-embarazo te puede ser bastante útil")
                dispatcher.utter_message(image="https://ciencia.unam.mx/uploads/infografias/if_embarazo_diabetes_19012022.jpg")
            
            elif tipo == "III":
                dispatcher.utter_message("En la diabetes tipo 3 —aventuran algunos investigadores—el cerebro se vuelve resistente a la insulina, que básicamente es el regulador de las concentraciones de azúcar en el cuerpo, lo que significa que no puede utilizarla efectivamente para llevar glucosa a las células cerebrales.\nEsta deficiencia se ha relacionado con la acumulación anormal de unas proteínas llamadas beta-amiloides en el cerebro, que son un rasgo característico de la enfermedad de Alzheimer.\nEn otras palabras, si pensamos en nuestro cuerpo como una máquina, la diabetes tipo 3 sería  como un cortocircuito en nuestro cerebro.\nLa insulina es una hormona que ayuda a nuestros cuerpos a usar la glucosa, que es como el combustible que necesitamos para funcionar correctamente. Sin embargo, en la diabetes tipo 3, nuestros cerebros tienen problemas para utilizar la insulina, lo que significa que las células cerebrales no obtienen suficiente energía. Como resultado, este órgano  comienza a funcionar mal y esto puede aumentar el riesgo de desarrollar la enfermedad de Alzheimer. FUENTE: UNAM https://ciencia.unam.mx/leer/1467/-que-sabes-de-la-diabetes-tipo-3-")
                dispatcher.utter_message(image="https://ciencia.unam.mx/uploads/textos/imagenes/ar_diabetes_tipo3_02_20102023.jpg")
            
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
    
class ActionMandaImagen(Action):
    
    def name(self) -> Text:
        return "action_manda_imagen"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            ultima_intencion = tracker.latest_message['intent']['name']
            if ultima_intencion == "sospecha_diabetes":
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
                        "Mira, esta información quiza sea de utilidad para ti"
                    ],
                    "imagenes": ["https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Dieta.png", "https://dimequecomes.com/wp-content/uploads/2019/04/DQC-Infografia-tratamiento-nutricional-diabetes-tipo-II.jpg", "https://alimentacionysalud.unam.mx/wp-content/uploads/2021/02/VIVIR-bien-con-diabetes.jpg", "https://static.wixstatic.com/media/57cfd2_23532047185c4584a6c990bd0dbfb59f~mv2.jpg/v1/fill/w_640,h_556,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/57cfd2_23532047185c4584a6c990bd0dbfb59f~mv2.jpg"]
                },
                "dar_alimentos": {
                    "mensajes": ["Esta infografía puede ayudarte a medir las raciones y porciones"],
                    "imagenes": ["https://www.imss.gob.mx/sites/all/statics/salud/infografias/infografia_porcionesyraciones3.jpg"],                    
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
                        "Esta infografía se me hizo interesante, de hecho explica eso que me dices"
                    ],
                    "imagenes": [None, "https://www.medicable.com.mx/AdminMedicable/Pagina/Infografia/Index/Img/406/1.webp", "https://pbs.twimg.com/media/Dvu1YUiXQAEX9wM.jpg", "https://fmdiabetes.org/wp-content/uploads/2023/02/-1-scaled.jpg"]
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
                        "La prediabetes es una afección grave en la que los niveles de azúcar en la sangre son más altos que lo normal, pero todavía no han llegado a niveles lo suficientemente altos para que se diagnostique diabetes tipo 2. Fuente: Centros para el Control y la Prevención de Enfermedades https://www.cdc.gov/diabetes/spanish/basics/prediabetes.html"
                    ],
                    "imagenes": ["https://www.cdc.gov/diabetes/spanish/images/resources/Prediabetes_1.png", "https://fmdiabetes.org/wp-content/uploads/2017/11/me-acaban-de-diagnosticar-predabietes.jpg", None, None, None]
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
                        "Las complicaciones crónicas se dividen, a su vez, en las macrovasculares y las microvasculares. Las macrovasculares están asociadas con problemas cardiosvaculares, y las microvasculares son las que dañan la vascularidad de órganos como los riñones, por lo que puede presentarse insuficiencia renal.\nPor otro lado, puede haber daño en la retina y en consecuencia, perder la vista. Igualmente, los pacientes con diabetes es posible que padezcan afectaciones en las vías nerviosas, provocando úlceras en los pies, evolucionando de esta manera al pie diabético que en muchas ocasiones termina en amputación. Fuente: UNAM https://ciencia.unam.mx/leer/1074/diabetes-infantil-diferente-a-la-de-los-adultos-"
                    ],
                    "imagenes": [None, None, None, None, None, None, None, None, None, None, None, None, None, "https://ciencia.unam.mx/uploads/infografias/if_retinopatia_21022022.jpg", "https://ciencia.unam.mx/uploads/infografias/if_diabetes_25032021.jpg", "https://ciencia.unam.mx/uploads/textos/imagenes/ar_cerebro_02_150882022.jpg"]
                }
            }
            
            respuesta = respuestas.get(ultima_intencion, {"mensajes": ["Mensaje predeterminado"], "imagenes": [None]})
            mensaje = random.choice(respuesta["mensajes"])
            image_url = respuesta["imagenes"][respuesta["mensajes"].index(mensaje)]
            
            dispatcher.utter_message(text=mensaje)
            
            if image_url:
                dispatcher.utter_message(image=image_url)
        
        except Exception as e:
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            print(e)
            dispatcher.utter_message(text=error)
              
        return []
    
class ActionChecaGlucosa(Action):
    
    def name(self) -> Text:
        return "action_checa_glucosa"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
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
            elif 140 < glucosa_antes <= 180:
                diagnostico1 = "Esos niveles son normales en una persona que TIENE diabetes, la glucosa en una persona diabética después de comer se debe mantener menor a un valor de 180 mg/dL"     
            elif glucosa_antes > 180:
                diagnostico1 = "El nivel de glucosa es bastante alto, lo máximo incluso para una persona diabética después de comer es de 180 mg/dL"
            
            diagnosticoFinal = msg1 + diagnostico + msg2 + diagnostico1
            
            dispatcher.utter_message(diagnosticoFinal)
            dispatcher.utter_message("Te comparto la fuente donde me basé para checar el nivel, espero te sea útil")
            dispatcher.utter_message(image="https://fmdiabetes.org/wp-content/uploads/2015/06/ADA.png")
        
        except Exception as e:
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
              
        return [SlotSet("glucosa_antes", None), SlotSet("glucosa_despues", None)]
    
class ActionRecomiendaAlgoDolor(Action):
    
    def name(self) -> Text:
        return "action_recomienda_algo_dolor"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            dolor = tracker.get_slot("dolor")
            dolor.upper()
            if dolor == "PANZA":
                dolor = "ESTOMAGO"
            elif dolor == "OÍDO":
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
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
              
        return []