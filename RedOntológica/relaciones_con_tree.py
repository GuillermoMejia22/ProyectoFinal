# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:28:15 2021

@author: user
"""

import sys

import math
import networkx as nx
import mlconjug3
import aplicacion
import tkinter as tk

import treetaggerwrapper


def eti_tree(pal):
    
    global tagger
    global tags
    tags_p = tagger.tag_text(pal)
    aux=tags_p[0].split("\t")
    w={}
    w["text"]=pal
    w['pos']=aux[1]
    w['lemma']=aux[2]
    return(w)
    

def conjuga(verbo):
    global default_conjugator
    try:
        test_verb = default_conjugator.conjugate(verbo)
    except ValueError:
        return(verbo)
    all_conjugated_forms = test_verb.iterate()
    for u, v, w, x in all_conjugated_forms:
        try:
            if u=="Indicativo" and v=="Indicativo presente" and w=="3s":
                return(x)
        except ValueError:
            break




def creaAutomata():
    g=nx.MultiDiGraph()

    #nodos
    g.add_node("1")
    g.add_node("2")
    g.add_node("3")
    g.add_node("4")
    #aristas


    g.add_edge("1","1", eti="ART")
    g.add_edge("1","1", eti="PPO")
    g.add_edge("1","1", eti="NEG")
    g.add_edge("1","2", eti="NC")
    g.add_edge("1","2", eti="NP")
    g.add_edge("1","3", eti="ADJ")
    
    g.add_edge("2","4", eti="ADJ")
    g.add_edge("2","1", eti="PAL")
    g.add_edge("2","1", eti="PDEL")
    g.add_edge("2","1", eti="REL")
    g.add_edge("2","1", eti="PREP")
    g.add_edge("2","4", eti="NC")
    g.add_edge("2","4", eti="NP")
    
    
    
    g.add_edge("3","2", eti="NC")
    g.add_edge("3","2", eti="NP")
    
    
    g.add_edge("4","2", eti="ADJ")
    g.add_edge("4","4", eti="NC")
    g.add_edge("4","4", eti="NP")
    g.add_edge("4","1", eti="PAL")
    g.add_edge("4","1", eti="PDEL")
    g.add_edge("4","1", eti="REL")
    g.add_edge("4","1", eti="PREP")
    
    
    return(g)


def simCos(cad1, cad2):
    list1=cad1.split(" ") 
    list2=cad2.split(" ")
    vocabulario = set(list1)|set(list2)
    vocabulario=list(vocabulario)
    #print vocabulario
    contar_p1=[]
    contar_p2=[]
    sum_a=0
    raiz_a=0
    raiz_b=0
    for x in range(len(vocabulario)):
        contar_p1.append(list1.count(vocabulario[x]))
        contar_p2.append(list2.count(vocabulario[x]))
    for i in range(len(contar_p1)):
        sum_a=sum_a+(contar_p1[i]*contar_p2[i])
        raiz_a=raiz_a+(contar_p1[i]*contar_p1[i])
        raiz_b=raiz_b+(contar_p2[i]*contar_p2[i])
    raiz_a=math.sqrt(raiz_a)
    raiz_b=math.sqrt(raiz_b)
    sim_cos=(sum_a)/(raiz_a*raiz_b)
    return sim_cos

def etiqueta(linea):
    global nlp
    global voca
    ets={}
    contaets=0
    linea=linea.split(" ")
    r=0

    while r<len(linea):
        ban=False
        candidatos={}
        try:
            
            if linea[r].lower()!=" " and linea[r].lower()!="": 
                w=eti_tree(linea[r].lower())
            else:
                break
        except IndexError:
            break
   
        if w['pos']=="NC" or w['pos']=="NP" or w['pos']=="NMEA" or w['pos']=="PNC":
        
            for tipo in voca:
                for pal in voca[tipo]:
                    if w['text'].lower() in pal:
                        #seleccion de candidatos
                        if tipo not in candidatos:
                            candidatos[tipo]={}
                        
                        candidatos[tipo][pal]=simCos(w['text'].lower(),pal)
                    
            #calculo de similitud con la siguiente palabra                
            aux=w['text'].lower()
            cos=0
            while True:
                #es la bandera de incremento de la similitud, si existe incremento la bandera se activa
                bInc=False
                try:
                    aux1=aux+' '+ linea[r+1].lower()
                    #print(aux1, "coreer")
                    for tipo in candidatos:
                        for cand in candidatos[tipo]: 
                            cos=simCos(aux1, cand)

                            if cos>candidatos[tipo][cand]:
                                
                                bInc=True
                                candidatos[tipo][cand]=cos
                                aux=aux1
      
                    if bInc==False:
                        break
                    else:
                        r+=1
                    
                except IndexError:
                    break
            
            #determinaer el de mayor similitud
            sim=0
            tipo=''
            
            for t in candidatos:
                for txt in candidatos[t]:
                    if candidatos[t][txt]>sim:
                        sim=candidatos[t][txt]
                        tipo=t
                        
            if sim>0.7:
                #print(aux,"\t", texto, '\t', sim)
                #print(tipo)       
                ets[contaets]={}
                ets[contaets]['texto']=aux
                ets[contaets]['eti']=tipo
                contaets+=1
                
                ban=True
                            
                
        if ban==False:
            
            
            ets[contaets]={}
            ets[contaets]['eti']=w['pos']
            
            if "VCL" in w['pos'] or "VE" in w['pos'] or "VH" in w['pos'] or "VL" in w['pos'] or "VM" in w['pos'] or "VS" in w['pos']:
                
                a=conjuga(w['lemma'])
                
                ets[contaets]['texto']=a
                ets[contaets]['eti']="VERB"
            else:
                ets[contaets]['texto']=w['text']
            
            contaets+=1
            
        ban=False
        r+=1
    return(ets)

 
def np(ets):
    
    
    global auto
    actual="1"
    guarda={}
    conta_guarda=0
    aux=''
    ban=False
    aux_ind=[]
    for indx in ets:
        #print(actual, ets[indx]["texto"], ban)
        #checa el nodo hacia donde va la arista partiendo del nodo actual
        #print(auto[actual], "nada mas")
        for nodo in auto[actual]:
            #print(actual, nodo, auto[actual])
            for aristas in auto[actual][nodo]:
                if auto[actual][nodo][aristas]['eti']==ets[indx]["eti"]:
                
                    aux=aux+" "+ets[indx]["texto"]
                    actual=nodo
                    aux_ind.append(indx)
                    ban=True
                
                    break
                else:
            
                    ban=False        
            if ban==True:
                break
        #print("sale bandera ",ban, actual, len(aux_ind))            
        if ban==False:
            if actual=="2" or actual=="4": 
                guarda[conta_guarda]={}
                guarda[conta_guarda]['texto']=aux
                guarda[conta_guarda]['eti']="NPHRASE"
                conta_guarda+=1
                
            else:
                if len(aux_ind)!=0:
                    #guarda los elementos arrastrados
                    for k in aux_ind:
                        guarda[conta_guarda]={}
                        #print(ets[k]["texto"], "se esta guardando directamente")
                        guarda[conta_guarda]['texto']=ets[k]["texto"]
                        guarda[conta_guarda]['eti']=ets[k]["eti"]
                        conta_guarda+=1
            #guarda el elemento actual        
            guarda[conta_guarda]={}
            guarda[conta_guarda]['texto']=ets[indx]["texto"]
            guarda[conta_guarda]['eti']=ets[indx]["eti"]
            conta_guarda+=1        
                        
            aux=''
            actual="1"
            aux_ind=[]  

    return(guarda)           


def relaciones(tab, dom):
    global sal
    global sal1
    
    rela="presenta"
    r=0
    while r<len(tab):
        
        try:
            
            #print(tab[r]['eti'], tab[r]['texto'], "afuera",r)
            ######lista de enfermedades####
            elif tab[r]['eti']=='enfermedad' or tab[r]['eti']=='sintoma':
                #print("entro")
                rangos=[]
                bandera=True
                rangos.append(tab[r]['texto'])
                r+=1
                while True:
                    #print(tab[r]['eti'],r)
                    if r==len(tab) or tab[r]['texto']=='.':
                        
                        if bandera==True:
                            for rango in rangos:
                                
                                #llamada de la consola
                                palabras=rango.split(" ")
                                nran=''
                                for pala in palabras:
                                    nran=nran+pala.capitalize()
                                ###llama a la ventana    
                                dominio=dom
                                relacion="http://www.diabetes-mexico.org/red#presenta" #todas las relaciones van sobre la red
                                rango="http://www.padecimientos-mexico.org/enfermedad#"+nran

                                root = tk.Tk()
                                myapp =aplicacion.App(root, dominio, relacion, rango)
                                myapp.mainloop()
                                
                                sal1.write(dom+"\tpresenta\t"+ rango.capitalize() +"\n")
                                sal.write(dom+"\tpresenta\t"+ rango.capitalize()+"\n")
                        break        
                    elif tab[r]['eti']!='enfermedad' and tab[r]['eti']!='NOUN' and tab[r]['eti']!='NPHRASE' and tab[r]['eti']!='sintoma' and tab[r]['eti']!='PUNCT':
                        bandera=False
                        
                        break
                    elif tab[r]['texto']==',' :
                        r+=1
                        
                    
                    else:
                        rangos.append(tab[r]['texto'])
                        r+=1   
            
            #####Signos valor######
            elif tab[r]['eti']=='signoClinico':
                #print("entre signo")
                rela='tiene'+tab[r]['texto'].capitalize()
                r+=1
                if tab[r]['eti']=='CARD' :
                    #llamada de la consola
                               
                    ###llama a la ventana    
                    dominio=dom
                    relacion="http://www.modelo.org/datos#"+rela #todas las relaciones van sobre la red
                    rango=tab[r]['texto']

                    root = tk.Tk()
                    myapp =aplicacion.App(root, dominio, relacion, rango)
                    myapp.mainloop()
                    
                    sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                    sal.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                    r+=1
                if tab[r]['eti']=='ADJ' :
                    sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                    sal.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                    r+=1
            ######partes del cuerpo######        
            elif tab[r]['eti']=='parteDelCuerpo':
                r+=1
                bpban=False
                while True:
                    if tab[r]['eti']=='ADJ':
                        rango=tab[r]['texto']+" "+tab[r+1]['texto']
                        r+=1
                        bpban=True
                    else:
                        break
                if bpban==True:
                    sal1.write(dom+"\tpresenta\t"+ rango +"\n")
                    sal.write(dom+"\tpresenta\t"+ rango +"\n")
            #######Patron de dominio y rango
            elif tab[r]['eti']=='VERB':
                
                if tab[r-1]['eti']=="PRON" or tab[r-1]['eti']=="ADV":
                    rela=tab[r-1]['texto']+tab[r]['texto'].capitalize()
                else:
                    rela=tab[r]['texto']
                
                r+=1
                if tab[r]['eti']=='ADP':
                    rela=rela+tab[r]['texto'].capitalize()
                    r+=1
                while True:
                    if tab[r]['eti']=='DET':
                        r+=1
                    elif tab[r]['eti']=='NOUN' or tab[r]['eti']=='NPHRASE':
                        sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                        sal.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                        r+=1
                    elif tab[r]['eti']=='enfermedad':
                        sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                        sal.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                        r+=1
                    elif tab[r]['eti']=='medicamento':
                        sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                        sal.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                        r+=1
                    elif tab[r]['text']==',' or tab[r]['eti']=='CONJ' or tab[r]['text']=='ademas':
                        r+=1
                    ######partes del cuerpo######        
                    elif tab[r]['eti']=='parteDelCuerpo':
                        r+=1
                        bpban=False
                        while True:
                            if tab[r]['eti']=='ADJ':
                                rango=tab[r]['texto']+" "+tab[r+1]['texto']
                                r+=1
                                bpban=True
                            else:
                                break
                        if bpban==True:
                            sal1.write(dom+"\t"+rela+"\t"+ rango +"\n")
                            sal.write(dom+"\t"+rela+"\t"+ rango +"\n")
                    
                
                    
                    else:
                        break
                
            else:
                r+=1 
        except IndexError:
            break
        except KeyError:
            break


tagger = treetaggerwrapper.TreeTagger(TAGLANG='es')        
default_conjugator = mlconjug3.Conjugator(language='es')

auto=creaAutomata()
#carga el mapeo de etiquetas




#cargando vocabularios
enf= open('enf.txt','r', encoding='utf-8')
voca={}
voca['enfermedad']=[]
voca['sintoma']=[]
voca['medicamento']=[]
voca['parteDelCuerpo']=[]
voca['signoClinico']=[]
for i in enf.readlines():
    i=i.replace("\n","")
    i=i.lower()
    i=i.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    
    voca['enfermedad'].append(i)
enf.close()

sint=open('sint.txt','r', encoding='utf-8')
for i in sint.readlines():
    i=i.replace("\n","")
    i=i.lower()
    i=i.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    
    voca['sintoma'].append(i)
sint.close()

meds=open('atcmedi.txt','r', encoding='utf-8')
for i in meds.readlines():
    i=i.replace("\n","")
    i=i.lower()
    i=i.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    
    voca['medicamento'].append(i)
meds.close()

body=open('partes_del_cuerpo.txt','r', encoding='utf-8')
for i in body.readlines():
    i=i.replace("\n","")
    i=i.lower()
    i=i.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    
    voca['parteDelCuerpo'].append(i)
body.close()

signo=open('aspectos_medicion.txt','r', encoding='utf-8')
for i in signo.readlines():
    i=i.replace("\n","")
    i=i.lower()
    i=i.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    
    voca['signoClinico'].append(i)
signo.close()


sal=open('etiquetas_propuesta2_cambio.txt','w', encoding='utf-8')
sal1=open("relaciones_propuestas2_cambio.txt",'w', encoding='utf-8')

document=open("datos.txt","r", encoding="utf-8")
lins=document.readlines()

for k in range(len(lins)):
    
    #enviar el nombre de la nota como dominio inicial
    
    if "http" in lins[k]:
        documento=lins[k].replace("\n","")
        
        sal.write("------------ % ----------"+documento+"\n")
        
    else:
        #toquenizacion de los signos de puntuacion
        la=lins[k].replace('(','').replace('(','').replace(',',' ,').replace(";"," ;").replace(':',' :').replace("\n","")
        #la=la.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    
        etiquetas=etiqueta(la)
        txt=np(etiquetas)
        
        for h in etiquetas:
            sal.write(str(etiquetas[h])+"\n")

        sal.write("######################################\n")

        for j in txt:
            sal.write(str(txt[j])+"\n")
            sal.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
        sal.write("***************************************\n")    
        rel=relaciones(txt,documento)
        sal.write("***************************************\n")
    
    
   





sal1.close()

sal.close()