# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:45:03 2021

@author: user
"""

"""
#######checar freeling

      import requests

      #Archivo a ser enviado
      files = {'file': open('ruta_de_archivo.txt', 'rb')}
      #Parámetros
      params = {'outf': 'tagged', 'format': 'json'}
      #Enviar petición
      url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
      r = requests.post(url, files=files, params=params)
      #Convertir de formato json
      obj = r.json()

      #Ejemplo, obtener todos los lemas
      for sentence in obj:
          for word in sentence:
              print word["lemma"]



"""

import pprint   # For proper print of sequences.
import treetaggerwrapper

#import spacy

#nlp = spacy.load("es_core_news_md")

#doc = nlp("acude a revision")
#for w in doc:
#    print(w.pos_)


tagger = treetaggerwrapper.TreeTagger(TAGLANG='es')

tags = tagger.tag_text("prolonga a la derecha")
pprint.pprint(tags)
tags2 = treetaggerwrapper.make_tags(tags)
pprint.pprint(tags2)

"""
from nltk import *
text=word_tokenize("soy feliz al atardecer aunque estoy sin dinero después del circo")

print(pos_tag(text, tagset='universal'))


"""
"""
import aplicacion
import tkinter as tk
dominio="http://www.modelo.org/datos#Nota1"
relacion="http://www.diabetes-mexico.org/red#acudeA" #todas las relaciones van sobre la red
rango="http://www.padecimientos-mexico.org/enfermedad#TerapiaCognitiva"

root = tk.Tk()
myapp =aplicacion.App(root, dominio, relacion, rango)
myapp.mainloop()

"""
"""
import networkx as nx
import mlconjug3


# You can now iterate over all conjugated forms of a verb by using the newly added Verb.iterate() method.
default_conjugator = mlconjug3.Conjugator(language='es')
test_verb = default_conjugator.conjugate("negar")
all_conjugated_forms = test_verb.iterate()
#print(all_conjugated_forms)
for u, v, w, x in all_conjugated_forms:
    try:
        if u=="Indicativo" and v=="Indicativo presente" and w=="3s":
            print(x)
    except ValueError:
        pass
        



"""






"""
def creaAutomata():
    g=nx.MultiDiGraph()

    #nodos
    g.add_node("1")
    g.add_node("2")
    g.add_node("3")

    #aristas
    g.add_edge("1","1", eti="AUX")
    g.add_edge("1","1", eti="DET")
    g.add_edge("1","2", eti="NOUN")
    g.add_edge("1","3", eti="ADJ")
    
    g.add_edge("2","2", eti="ADJ")
    g.add_edge("2","1", eti="ADP")
    g.add_edge("2","4", eti="NOUN")

    g.add_edge("3","2", eti="NOUN")
    
    g.add_edge("4","2", eti="ADJ")
    g.add_edge("4","4", eti="NOUN")
    return(g)

auto=creaAutomata()

actual="1"
et="ADJ"
print(auto[actual])
for nodo in auto[actual]:
    for aristas in auto[actual][nodo]:
    
        if auto[actual][nodo][aristas]['eti']==et:
            print(nodo)
"""