# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 17:34:45 2021

@author: user
"""

manuales=[]
automaticas=[]

archi=open("etiquetas_propuesta_manual.txt","r", encoding="utf-8")
for k in archi.readlines():
    k=k.replace("\n","")
    if "#" in k:
        
        dominio=k
    else:
        aux_man=k.split("\t")
        if len(aux_man)==2:
            aux=dominio+"\t"+aux_man[0]+"\t"+aux_man[1].lower()
            
            manuales.append(aux)
        
archi.close()
rels=open("relaciones_propuestas2_cambio.txt","r", encoding="utf-8")

for rela in rels.readlines():
    rela=rela.replace("\n","")
    aux=rela.split("\t")
    relacion=aux[0]+"\t"+aux[1]+"\t"+aux[2].lower()
    automaticas.append(relacion)
rels.close()

#print(manuales)
print(len(manuales), len(automaticas))
#print(set(manuales) & set(automaticas))
vp=len(set(manuales) & set(automaticas))

fp=len(set(automaticas).difference(set(manuales)))
fn=len(set(manuales).difference(set(automaticas)))

print(vp, fp, fn)

presicion=vp/(vp+fp)
recall=vp/(vp+fn)

f_measure=2*((presicion*recall)/(presicion+recall))

print("presicion: ",presicion)
print("recall: ",recall)
print("f-measure: ",f_measure)
















