# -*- coding: utf-8 -*-
"""
Created on Wed May 12 10:24:33 2021

@author: user
"""


import tkinter as tk
from owlready2 import *

class App(tk.Frame):
    def __init__(self, master, dominios, relaciones, rangos):
        super().__init__(master)
        self.pack()
        
        self.ldom=tk.Label( text="Dominio:")
        self.ldom.pack()
        
        self.entryDom = tk.Entry(width=50)
        self.entryDom.pack()
        self.lrel=tk.Label( text="Relación:")
        self.lrel.pack()
        self.entryRel=tk.Entry(width=50)
        self.entryRel.pack()
        self.lran=tk.Label( text="Rango")
        self.lran.pack()
        self.entryRan = tk.Entry(width=50)
        self.entryRan.pack()
        

        self.dominio=tk.StringVar()
        self.dominio.set(dominios)
        self.entryDom["textvariable"]=self.dominio
        
        
        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set(relaciones)
        # Tell the entry widget to watch this variable.
        self.entryRel["textvariable"] = self.contents
        
        
        self.rango=tk.StringVar()
        self.rango.set(rangos)
        self.entryRan["textvariable"]=self.rango

        

        self.quit = tk.Button(self, text="Omitir", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        
        
        self.registraObj=tk.Button(self, text="Registra")
        #self.registra["text"]="Registra"
        self.registraObj["command"]=self.print_contents

        self.registraObj.pack(side="left")

        



    def print_contents(self):
        domi=self.dominio.get()
        rela=self.contents.get()
        ran=self.rango.get()
        #print(domi, rela, ran)
        onto_path.append("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/")
        onto_edo=get_ontology("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/localizacionRDF.owl").load()
        onto_perso=get_ontology("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/personaRDF.owl").load()
        onto_dato=get_ontology("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/datosRDF.owl").load()
        onto_tto=get_ontology("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/tratamientoRDF.owl").load()
        onto_enfe=get_ontology("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/padecimientosRDF.owl").load()
        onto_esco=get_ontology("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/escolaridadRDF.owl").load()
        onto_medi=get_ontology("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/med_atc_rdf.owl").load()
        
        onto=get_ontology("C:/Users/user/Google Drive/Doctorado/RedRDFPoblada/red_nodos_RDF.owl").load()
        
        #print(onto_edo.base_iri)
        #print(onto_perso.base_iri)
        #print(onto_enfe.base_iri)
        onto_red= onto.get_namespace("http://www.diabetes-mexico.org/red/")
        onto_enfermedades=onto_enfe.get_namespace("http://www.padecimientos-mexico.org/lista/")
        onto_datos=onto_dato.get_namespace("http://www.modelo.org/datos/")
        #print(list(onto.imported_ontologies))
        #print(list(onto.tieneDiagnostico.get_relations()))
        #print(onto_enfe.base_iri)
        onto_medicam= onto_medi.get_namespace("http://www.medicamentos-mexico.org/medicamento/")
       
        
        ###dominio de la tripleta
        if IRIS[domi]!=None :
            print(IRIS[domi], "ya existe el dominio")
            dominioTriple=IRIS[domi]
        else:
            #inserta si no existe el objeto    
            a_domi=domi.split("#")
            n_obj=a_domi[1]
            link=a_domi[0]+"#"
            
            if link==onto_medi.base_iri:
                with onto_medi:
                    dominioTriple=onto_medi.Medicamento(n_obj)
                    onto_medi.save()
            
        ######################################################    
        
        ########################################################
        #rango de la tripleta
        if "http" not in ran:
            #relacion de la tripleta    
            if IRIS[rela]!=None :
                
                print(IRIS[rela], "ya existe la relacion")
                relaTriple=IRIS[rela]
                nombre=relaTriple.name
            else:
                #inserta si no existe la relacion en la red  
                a_rel=rela.split("#")
            
                nprope=a_rel[1]
                
                with onto_medi:
                    
                    auxproperty = types.new_class(nprope, (DataProperty,))
                    
                    
                    onto_medi.save()
                    print(auxproperty)
            
                    nombre=auxproperty.name
            
            with onto_medi:
                #instancia la relacion en la red 
                #instancia la relacion en la red 
                setattr(dominioTriple, nombre, [ran])
                onto_medi.save()
        else: 
            #es una object property
            #relacion de la tripleta    
            if IRIS[rela]!=None :
        
                print(IRIS[rela], "ya existe la relacion")
                relaTriple=IRIS[rela]
                nombre=relaTriple.name
            else:
                #inserta si no existe la relacion en la red  
                a_rel=rela.split("#")
            
                nprope=a_rel[1]
                with onto:
                    auxproperty = types.new_class(nprope,  (ObjectProperty,))
                    onto.save()
                    print(auxproperty)
            
                    nombre=auxproperty.name
            
            
            
            if IRIS[ran]!=None :
                print(IRIS[ran], "ya existe el rango")
                rangoTriple=IRIS[ran]
            else:
                #inserta si no existe el objeto    
                a_ran=ran.split("#")
                n_obj=a_ran[1]
                link=a_ran[0]+"#"
            
                if link==onto_enfe.base_iri:
                    with onto_enfe:
                        rangoTriple=onto_enfe.Padecimiento(n_obj)
                        onto_enfe.save()
            
        
        
        
            with onto:
            
                #instancia la relacion en la red 
                aux=getattr(dominioTriple, nombre)
                aux.append(rangoTriple)
                onto.save()
        self.master.destroy()
    
        

