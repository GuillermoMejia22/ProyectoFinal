# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 14:16:07 2021

@author: user
"""

import sys
import spacy
import math
import networkx as nx
import mlconjug3
import pprint   # For proper print of sequences.
import treetaggerwrapper


def eti_tree(pal):
   
    global tagger
    global tags
    tags_p = tagger.tag_text(pal)
    for p in range(len(tags_p)):
        aux=tags_p[p].split("\t")
        print(aux)
        w={}
        w[str(p)]={}
        w[str(p)]["text"]=aux[0]
        w[str(p)]['pos']=tags[aux[1]]
        w[str(p)]['lemma']=aux[2]
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

    #aristas


    g.add_edge("1","1", eti="DET")
    g.add_edge("1","2", eti="NOUN")
    g.add_edge("1","2", eti="PROPN")
    #g.add_edge("1","2", eti="sintoma")
    #g.add_edge("1","2", eti="medicamento")
    #g.add_edge("1","2", eti="enfermedad")
    #g.add_edge("1","2", eti="parteDelCuerpo")
    g.add_edge("1","3", eti="ADJ")
    
    g.add_edge("2","2", eti="ADJ")
    g.add_edge("2","1", eti="ADP")
    g.add_edge("2","4", eti="NOUN")
    g.add_edge("2","4", eti="PROPN")
    #g.add_edge("2","4", eti="sintoma")
    #g.add_edge("2","4", eti="medicamento")
    #g.add_edge("2","4", eti="enfermedad")
    #g.add_edge("2","4", eti="parteDelCuerpo")
    
    
    g.add_edge("3","2", eti="NOUN")
    g.add_edge("3","2", eti="PROPN")
    #g.add_edge("3","2", eti="sintoma")
    #g.add_edge("3","2", eti="medicamento")
    #g.add_edge("3","2", eti="enfermedad")
    #g.add_edge("3","2", eti="parteDelCuerpo")
    
    g.add_edge("4","2", eti="ADJ")
    g.add_edge("4","4", eti="NOUN")
    g.add_edge("4","4", eti="PROPN")
    #g.add_edge("4","4", eti="sintoma")
    #g.add_edge("4","4", eti="medicamento")
    #g.add_edge("4","4", eti="enfermedad")
    #g.add_edge("4","4", eti="parteDelCuerpo")
    
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
    doc=eti_tree(linea.lower())
    
    for w in doc:
        ets[contaets]={}
        ets[contaets]['eti']=doc[w]['pos']
        if doc[w]['pos']=="VERB":
            ets[contaets]['texto']=conjuga(doc[w]['lemma'])
        else:
            ets[contaets]['texto']=doc[w]['text']
            
        contaets+=1
            
        
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
    global nlp
    global sal1
    
    rela="RELACIÓN INDEFINIDA"
    r=0
    while r<len(tab):
        
        try:
            #print(tab[r]['eti'], tab[r]['texto'], "afuera",r)
            ######lista de enfermedades####
            if tab[r]['eti']=='enfermedad' or tab[r]['eti']=='sintoma':
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
                                """
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
                                sys.exit()
                                """
                                sal1.write(dom+"\tpresenta\t"+ rango.capitalize() +"\n")
                                print(dom,"\tpresenta\t", rango.capitalize())
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
                if tab[r]['eti']=='NUM' :
                     sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                     print(dom,"\t",rela,"\t", tab[r]['texto'])
                     r+=1
                if tab[r]['eti']=='ADJ' :
                    sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                    print(dom,"\t",rela,"\t", tab[r]['texto'])
                    r+=1
            ######partes del cuerpo######        
            elif tab[r]['eti']=='parteDelCuerpo':
                if tab[r+1]['eti']=='ADJ':
                    rango=tab[r]['texto']+"_"+tab[r+1]['texto']
                    r+=2
                else:
                    rango=tab[r]['texto']     
                    r+=1
                sal1.write(dom+"\tpresenta\t"+ rango +"\n")
                print(dom,"\tpresenta\t", rango)
            #Patron de dominio y rango
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
                        print(dom,"\t",rela,"\t", tab[r]['texto'])
                        r+=1
                    elif tab[r]['eti']=='enfermedad':
                        sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                        print(dom,"\t",rela,"\t", tab[r]['texto'])
                        r+=1
                    elif tab[r]['eti']=='medicamento':
                        sal1.write(dom+"\t"+rela+"\t"+ tab[r]['texto'] +"\n")
                        print(dom,"\t",rela,"\t", tab[r]['texto'])
                        r+=1
                    elif tab[r]['text']==',' or tab[r]['eti']=='CONJ' or tab[r]['text']=='ademas':
                        r+=1
                    ######partes del cuerpo######        
                    elif tab[r]['eti']=='parteDelCuerpo':
                        if tab[r+1]['eti']=='ADJ':
                            rango=tab[r]['texto']+"_"+tab[r+1]['texto']
                            r+=2
                        else:
                            rango=tab[r]['texto']     
                            r+=1
                        sal1.write(dom+"\t"+rela+"\t"+ rango +"\n")
                        print(dom,"\t",rela,"\t",rango,"\n")
                    
                
                    
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
nlp = spacy.load("es_core_news_md")
auto=creaAutomata()
#carga el mapeo de etiquetas
tags={}
unitags=open("mapea_etiquetas.txt","r", encoding='utf-8')

for u in unitags.readlines():
    u=u.replace("\n","")
    vals=u.split("\t")
    tags[vals[0]]=vals[1]

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


sal=open('etiquetas_propuesta3.txt','w', encoding='utf-8')
sal1=open("relaciones_propuestas3.txt",'w', encoding='utf-8')

document=open("datos.txt","r", encoding="utf-8")
lins=document.readlines()

for k in range(len(lins)):
    sal.write(lins[k])
    #enviar el nombre de la nota como dominio inicial
    
    if "http" in lins[k]:
        documento=lins[k].replace("\n","")
        
        print(documento)
        
    else:
        #toquenizacion de los signos de puntuacion
        la=lins[k].replace('(','').replace('(','').replace(',',' ,').replace(";"," ;").replace(':',' :').replace("\n","")
        etiquetas=etiqueta(la)
        txt=np(etiquetas)
        for h in etiquetas:
            print((etiquetas[h]))

        print("######################################33")

        print("------------ % ----------",documento)
        for j in txt:
            print(txt[j])
            print("###################")
        print("***************************************")    
        rel=relaciones(txt,documento)
        print("***************************************")
    
    
   





sal1.close()

sal.close()