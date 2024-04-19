#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 10:26:16 2021

@author: ceci
"""

 
import networkx as nx

import sys


frec={}
g=nx.DiGraph()

#nodos
g.add_node("1")
g.add_node("2")
g.add_node("3")

#aristas

#g.add_edge("1","1", eti="DET")
g.add_edge("1","2", eti="NOUN")
g.add_edge("1","3", eti="ADJ")
g.add_edge("2","2", eti="ADJ")
g.add_edge("2","1", eti="ADP")

g.add_edge("3","2", eti="NOUN")


print(g["2"])
for i in g["2"]:
    print(g["2"][i], i)
    print(g[i])


sys.exit()

archi=open("nota1.txt","r",encoding='utf-8')
sal=open("conceptos_nota1.txt","w", encoding="utf-8")

lineas=archi.readlines()
for i in range(len(lineas)):
    if i %2!=0:
        #etiquetas
        aux=(lineas[i].replace('\n','')).split(" ")
        #texto
        txt=(lineas[i-1].replace('\n','')).split(" ")
        #estado inicial
        actual="1"
        guarda=[]
        num=99
        #lee el renglon de las etiquetas
        for j in range(len(aux)):
            for (u,v,w) in g.edges.data('eti'):
                #pregunta si el estado actual tiene una arista con una etiqueta
                if u==actual and w==aux[j]:
                    if j-num>2:
                        
                        if len(guarda)>0 and actual=="2":
                            try:
                                frec[str(guarda)]+=1
                            except KeyError:
                                frec[str(guarda)]=1
                            #sal.write(str(guarda)+"\n")
                            guarda=[]
                        actual="1"
                    else:
                        actual=v
                        guarda.append(txt[j])
                        
                        num=j
                    
        if actual=="2":
            #estado final aceptacion
            try:
                frec[str(guarda)]+=1
            except KeyError:
                frec[str(guarda)]=1
            #sal.write(str(guarda)+"\n")    


for j in frec:
    sal.write(str(j)+"\t"+str(frec[j])+"\n")                
sal.close()