class ActionMandaImagen(Action):
    
    def name(self) -> Text:
        return "action_manda_imagen"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        try:
            ultima_intencion = tracker.latest_message['intent']['name']
            image_url = None
            if ultima_intencion == "explicar_sintomas" or ultima_intencion == "decir_sintomas":
                opcion = random.randint(0, 2)
                if opcion == 0:
                    mensaje = "El IMSS menciona que algunos de ellos pueden ser:"
                    image_url = "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Sintomas.png"
                elif opcion == 1:
                    mensaje = "De acuerdo con información del Gobierno de México Los síntomas son diferentes dependiendo el tipo de la diabetes, pero cuando los niveles de azúcar son altos, se presenta una sensación de mucha hambre y sed, incluso llegar a perder peso, necesidad de orinar muy a menudo y sentir cansancio. Por otro lado, en las personas con diabetes tipo 2 es común no presentar síntomas al inicio, incluso es posible que no los tengan durante muchos años. En estos casos, la detección de la diabetes suele darse mediante un análisis de sangre, pero se puede reconocer la enfermedad ante síntomas como disfunción eréctil, visión borrosa y dolor o entumecimiento en los pies o las manos."
                else: 
                    mensaje = "La OMS dice que Los síntomas de la diabetes pueden ocurrir repentinamente. En la diabetes de tipo 2, los síntomas pueden ser leves y tardar muchos años en notarse. Algunos de ellos son:"
                    image_url = "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/SintomasV2.png"
            elif ultima_intencion == "mood_triste":
                image_url = "https://wallpapers-clan.com/wp-content/uploads/2022/07/funny-cat-17.jpg"
            elif ultima_intencion == "controlar_diabetes":
                opcion = random.randint(0, 3)
                if opcion == 0:
                    mensaje = "Existen distintos medicamentos en el mercado que ayudan a bajar el nivel de azucar en la sangre, suelen ser llamados como hipoglucemiantes, estos acompañados de una buena actividad física, una alimentación sana y seguimiento con un especialista de la salud se puede controlar adecuadamente"
                elif opcion == 1:
                    mensaje = "La participación de la persona que vive con diabetes es necesaria para lograr un buen control de sus niveles de glucosa y una buena calidad de vida, siguiendo las siguientes recomendaciones:"
                    image_url = "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Recomendacion.png"
                elif opcion == 2:
                    mensaje = "La diabetes se puede tratar y sus consecuencias se pueden evitar o retrasar con dieta, actividad física, medicación y exámenes y tratamientos regulares para las complicaciones."
                else:
                    mensaje = "Algunas personas con diabetes de tipo 2 necesitan tomar medicamentos para ayudar a controlar los niveles de azúcar en la sangre. Estos medicamentos se administran en forma de inyección o por otras vías. Algunos de estos medicamentos son: metformina; sulfonilureas e inhibidores del cotransportador de sodio-glucosa de tipo 2."
            elif ultima_intencion == "dieta_diabetes" or ultima_intencion == "dar_alimentos":
                mensaje = "De acuerdo con información del IMSS (Instituto Mexicano del Seguro Social) Debes tener una alimentación que ayude a mantener un nivel adecuado de azúcar en la sangre, puedes acudir con un experto en nutrición para que te recomiende un plan alimenticio. Sobre todo debes:"
                image_url = "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Dieta.png"
            elif ultima_intencion == "otros_cuidados":
                mensaje = "Recomiendo seguir los siguientes cuidados"
                image_url = "https://raw.githubusercontent.com/GuillermoMejia22/ImagenesProyecto/main/Cuidados.png"  
            
            dispatcher.utter_message(mensaje)
            
            if image_url != None:    
                dispatcher.utter_message(image=image_url)
        
        except Exception as e:
            error = "El servidor de acciones está experimentando un problema. Intenta de nuevo más tarde."
            dispatcher.utter_message(error)
              
        return []