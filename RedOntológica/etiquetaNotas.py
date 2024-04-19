#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 11:08:15 2021

@author: user
"""
import spacy
import math

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


 


nlp = spacy.load("es_core_news_md")

#cargando vocabularios
enf= open('enf.txt','r', encoding='utf-8')
voca={}
voca['enfermedad']=[]
voca['sintoma']=[]
voca['medicamento']=[]
voca['parteDelCuerpo']=[]
for i in enf.readlines():
    i=i.replace("\n","").replace(',','')
    i=i.lower()
    voca['enfermedad'].append(i)
enf.close()

sint=open('sint.txt','r', encoding='utf-8')
for i in sint.readlines():
    i=i.replace("\n","").replace(',','')
    i=i.lower()
    voca['sintoma'].append(i)
sint.close()

meds=open('atcmedi.txt','r', encoding='utf-8')
for i in meds.readlines():
    i=i.replace("\n","").replace(',','')
    i=i.lower()
    voca['medicamento'].append(i)
meds.close()

body=open('partes_del_cuerpo.txt','r', encoding='utf-8')
for i in body.readlines():
    i=i.replace("\n","").replace(',','')
    i=i.lower()
    voca['parteDelCuerpo'].append(i)
body.close()







sal=open('etiquetas_propuesta.txt','w', encoding='utf-8')
la='Paciente de sexo Femenino, consiente, bien orientada en las tres esferas neurológicas, edad aparente igual a la cronológica, buena coloración tegumentaria, estado hídrico conservado, facie normal, posición y actitud libremente escogida. Cabeza: Normocéfalo, ojos simétricos, pupilas isocoricas normoreflecticas, adoncia, mucosa oral bien hidratada, oídos simétricos permeables. Cuello: cilíndrico, tráquea central, sin adenopatías. Tórax: movimientos de amplexion y amplexación normales, frecuencia respiratoria normal, sin ruidos agregados, bien ventilados, frecuencia cardiaca rítmica, de buena intensidad y frecuencia, sin ruidos agregados. Abdomen: globoso por panículo adiposo, blando, depresible, peristalsis presente, normal, sin tumoraciones(megalias), sin puntos dolorosos y con sensibilidad normal, sin datos o signos de irritación peritoneal, Giordano negativo. Extremidades: superiores simétricas movimientos normales, pulsos normales, reflejos osteotendinosos normales, Extremidades inferiores simétricas sin alteraciones en los movimientos, con marcha normal, pulsos normales y presentes, reflejos normales, buen llenado capilar, sin edema.  '
#toquenizacion de los signos de puntuacion
la=la.replace('.',' .').replace(',',' ,').replace(";"," ;").replace(':',' :')


linea=la.split(" ")

r=0


while r<len(linea):
    ban=False
    candidatos={}
    doc=nlp(linea[r])
    try:
        w=doc[0]
    except IndexError:
        break
   
    if w.is_stop==False and w.pos_!="VERB" and w.pos_!="PUNCT":
        
        for tipo in voca:
            for pal in voca[tipo]:
                if w.lower_ in pal:
                    #seleccion de candidatos
                    if tipo not in candidatos:
                        candidatos[tipo]={}
                    candidatos[tipo][pal]=simCos(w.text,pal)
                    
        #calculo de similitud con la siguiente palabra                
        aux=w.lower_
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
                        
                            
                        #print(cand, cos)
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
        texto=''
        for t in candidatos:
            for txt in candidatos[t]:
                if candidatos[t][txt]>sim:
                    sim=candidatos[t][txt]
                    tipo=t
                    texto=txt
        if sim>0.7:
            print(aux,"\t", texto, '\t', sim)
            print(tipo)
                        
            sal.write(tipo+" ")
            ban=True
                            
                
    if ban==False:
            print(w.text)
            print(w.pos_)
            sal.write(w.pos_+" ")
    ban=False
    r+=1
sal.close()