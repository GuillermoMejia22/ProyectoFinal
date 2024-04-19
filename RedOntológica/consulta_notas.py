# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:16:05 2021

@author: user
"""

import rdflib

sal=open("datos.txt","w", encoding="utf-8")
g = rdflib.Graph()

# ... add some triples to g somehow ...
g.parse("datosRDF.owl")

qres = g.query(
    """
    PREFIX dato: <http://www.modelo.org/datos#>
    SELECT DISTINCT ?a ?b ?c ?d
       WHERE {
          ?a dato:tieneAnalisis ?b.
          ?a dato:tieneExploracionFisica ?c.
          ?a dato:tienePadecimientoActual ?d.
       }""")

for row in qres:
    for data in row:
        d=str(data).replace("\n"," ")
        sal.write(d+ "\n")
    
sal.close()