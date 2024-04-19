#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:01:15 2021

@author: ceci
"""

from owlready2 import *
import owlready2 as owl
import datetime as dt

onto = get_ontology("datosRDF.owl").load()
print(onto.base_iri)

print(onto.Expediente_Clinico.instances())


name='Expediente7'

#creacion de la instancia
nper=onto.Expediente_Clinico(name)
#datatype property
#nper.tieneSexo=[''+sexo]
#nper.tieneFechaNacimiento=[dt.date(2021,2,17)]

onto.save(file = "datosRDF.owl", format = "rdfxml")
