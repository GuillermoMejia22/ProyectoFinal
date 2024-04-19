# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 14:16:03 2021

@author: user
"""


import docx 
import spacy
import yake
from multi_rake import Rake
nlp = spacy.load("es_core_news_md")


kw_extractor = yake.KeywordExtractor()





txt=''


# open connection to Word Document
archis=open('C:/Users/user/Google Drive/ARCHIVOS/DM2 + HAS/nom.txt','r')

for i in archis.readlines():
    i=i.replace('\n','')
    doc = docx.Document("C:/Users/user/Google Drive/ARCHIVOS/DM2 + HAS/"+i)
 
    # read in each paragraph in file
    lineas = [p.text for p in doc.paragraphs]
    for l in lineas:
        txt=txt+l+' '

archis.close()
rake = Rake()

keywords = rake.apply(txt)

sal=open('keywords eti.txt','w', encoding='utf-8')

keywordsYake = kw_extractor.extract_keywords(txt)

for k in keywordsYake:
    doc = nlp(k[0])
    sal.write(k[0]+'\n')
    for w in doc:
        sal.write(w.pos_+' ')
    sal.write('\n')

sal.write('############################################################\n')
for k in keywords:
    doc = nlp(k[0])
    sal.write(k[0]+'\n')
    for w in doc:
        sal.write(w.pos_+' ')
    sal.write('\n')
    
sal.close()
 