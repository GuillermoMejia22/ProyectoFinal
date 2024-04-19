#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 11:24:18 2021

@author: ceci
"""

from owlready2 import *
import owlready2
import datetime as dt
onto_path.append("/home/ceci/RedRDF/")
onto = get_ontology("/home/ceci/RedRDF/red_nodos_RDF.owl").load()



print(onto.base_iri)