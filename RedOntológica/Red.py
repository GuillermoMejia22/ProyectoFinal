#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:06:53 2021

@author: ceci
"""

from owlready2 import *
import owlready2 as owl
import datetime as dt
onto_path.append("/home/ceci/RedRDF/")
onto = get_ontology("/home/ceci/RedRDF/red_nodos_RDF.owl").load()
onto.imported_ontologies.append("/home/ceci/RedRDF/personaRDF.owl")
print(onto.base_iri)

paciente=onto.tieneExpedienteClinico.domain

print(onto.imported_ontologies)
#print(onto.Expediente_Clinico.instances())


name='Expediente7'

#creacion de la instancia
#nper=onto.Expediente_Clinico(name)
#datatype property
#nper.tieneSexo=[''+sexo]
#nper.tieneFechaNacimiento=[dt.date(2021,2,17)]

#onto.save()
