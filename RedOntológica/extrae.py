#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 18:12:04 2021

@author: ceci
"""
import sys
from openpyxl import load_workbook
from owlready2 import *
import owlready2 as owl
import datetime as dt

vias=['Cutanea','Infiltracion','Cutanea_En_Glandula_Mamaria',
      'Bucal_Por_Inhalacion','Gastroenterica','Oral','Oral_Disolver_En_Lengua',
      'Rectal','Sublingual','Intrauterina','Oftalmica','Otica','Topico',
      'Transdermica','Vaginal','Intramuscular','Subcutanea',
      'Infusion_Intravenosa','Infusion_Intravenosa_Continua','Intraarterial',
      'Intracardiaca','Intravenosa','Intravenosa_Lenta','Intravenosa_Por_Infusion',
      'Intravenosa_Por_Infusion_Continua','Inhalacion','Inhalacion_Bucal','Nasal',
      'Nebulizacion','Intramuscular_En_El_Musculo_Afectado','Intramuscular_Profunda',
      'Epidural','Intraarticular','Intradermica','Intraperitoneal','Intratecal',
      'Intravesical','Implante_Subcutaneo','Subcutanea_Profunda']

formas=['Capsula','Capsula_Con_Granulos_Con_Capa_Enterica','Capsula_Con_Polvo_Para_Inhalacion','Capsula_De_Gelatina_Blanda',
        'Capsula_De_Liberacion_Prolongada','Capsula_De_Liberacion_Retardada','Capsula_Masticable','Comprimido',
        'Comprimido_Con_Capa_Enterica','Comprimido_De_Liberacion_Prolongada','Comprimido_Efervescente','Comprimido_Masticable',
        'Comprimido_Recubierto','Gragea','Gragea_Con_Capa_Enterica','Gragea_De_Liberacion_Prolongada','Gragea_Recubierta',
        'Granulado','Granulado_Oral','Implante','Implante_De_Liberacion_Prolongada','Implante_Intraocular','Jabon','Parche',
        'Perla','Supositorio','Polvo','Polvo_Para_Inhalacion','Tableta','Efervescente','Tableta_Con_Capa_Enterica',
        'Tableta_De_Liberacion_Prolongada','Tableta_Dispersable','Tableta_Efervescente','Tableta_Masticable','Tableta_Recubierta',
        'Tableta_Soluble','Tableta_Sublingual','Tableta_Vaginal','ovulo','ovulo_De_Liberacion_Prolongada','Crema','Crema_Vaginal',
        'Gel','Gel_Dermico','Pasta','Pomada','Unguento','Unguento_Oftalmico','Emulsion','Emulsion_Dermica','Emulsion_Inyectable',
        'Emulsion_Oral','Locion','Locion_Dermica','Solucion','Jarabe','Liquido','Solucion_Al_10_Por_Ciento','Solucion_Dermica',
        'Solucion_Inyectable','Solucion_Inyectable_Al_1_Por_Ciento','Solucion_Inyectable_Al_2_Por_Ciento','Solucion_Inyectable_Al_5_Por_Ciento',
        'Solucion_Inyectable_Oleosa','Solucion_Nasal','Solucion_Oftalmica','Solucion_Oral','Solucion_Para_Dialisis_Peritoneal',
        'Solucion_Para_Inhalacion','Solucion_Para_Nebulizar','Solucion_Topica','Solucion_otica','Suspension_Dermica',
        'Suspension_En_Aerosol','Suspension_En_Aerosol_Nasal','Suspension_Inyectable','Suspension_Inyectable_De_Liberacion_Prolongada',
        'Suspension_Oftalmica','Suspension_Oral','Suspension_Para_Inhalacion','Suspension_Para_Nebulizar','Suspension_Rectal']


def creaPaciente(datos):
    
    #crea un paciente y su expediente, regresa iri del expediente
    onto = get_ontology("personaRDF.owl").load()
   
    #creacion de la instancia
    name='paciente'+datos[0]
    
    nper=onto.Paciente(name)
    print('creando persona ',name)
    ###########datatype properties
    #sexo
    if datos[1].upper()=="M":
        sexo='Masculino'
    else:
        sexo='Femenino'
    nper.tieneSexo=[sexo]
    #fechaNacimiento
    try:
        fecha=datos[2].split('/')
        nper.tieneFechaNacimiento=[dt.date(int(fecha[2]),int(fecha[1]),int(fecha[0]))]
        fna=dt.date(int(fecha[2]),int(fecha[1]),int(fecha[0]))
    except AttributeError:
        aux=str(datos[2]).split(' ')
        fecha=aux[0].split('-')
        nper.tieneFechaNacimiento=[dt.date(int(fecha[0]),int(fecha[1]),int(fecha[2]))]
        fna=dt.date(int(fecha[0]),int(fecha[1]),int(fecha[2]))
        
    onto.save(file = "personaRDF.owl", format = "rdfxml")
    
    #creacion del expediente y la historia clinica
    iris=creaExpediente(datos[0])
    exp=iris[0]
    escribeRed(str(nper.iri), 'tieneExpedienteClinico', exp)
    #agrega la fecha nacimiento como 3er argumento de iris
    iris.append(fna)
    return(iris)

def creaExpediente(name):
    onto = get_ontology("datosRDF.owl").load()
    expName='Expediente'+name
    nEx=onto.Expediente_Clinico(expName)
    print('creando expe ',expName)
    onto.save(file = "datosRDF.owl", format = "rdfxml")
    his=creaHistoria(name, nEx.iri)
    iris=[nEx.iri, his]
    return(iris)
    
def creaHistoria(name, expediente):
    onto = get_ontology("datosRDF.owl").load()
    hisName='Historia'+name
    nHis=onto.Historia_Clinica(hisName)
    print('crea historia ',hisName)
    #object property tieneHistoria
    expe=onto.search(iri =expediente)
    exp=expe[0]
    exp.tieneHistoriaClinica=[nHis]
    onto.save(file = "datosRDF.owl", format = "rdfxml")
    return(nHis.iri)
    
def creaNota(expediente, aux_not):
    onto = get_ontology("datosRDF.owl").load()
    #creacion de la nota
    name='Nota'+str(aux_not['conta'])
    nNot=onto.Nota_Medica(name)
    print('creando nota ',nNot)
    #object property tieneNotaMedica
    expa=onto.search(iri =expediente)
    exp=expa[0]
    exp.tieneNotaMedica=[nNot]
    #data properties
    try:
        aux_fecha=str(aux_not['fecha']).split(' ')
        print(aux_fecha)
        fecha=aux_fecha[0].split('-')
        nNot.tieneFecha=[dt.date(int(fecha[0]),int(fecha[1]),int(fecha[2]))]
        f=dt.date(int(fecha[0]),int(fecha[1]),int(fecha[2]))
    except ValueError:
        fecha=str(aux_not['fecha']).split('/')
        print(fecha)
        
        nNot.tieneFecha=[dt.date(int(fecha[2]),int(fecha[1]),int(fecha[0]))] 
        f=dt.date(int(fecha[2]),int(fecha[1]),int(fecha[0]))
    #calculo de edad
    fna=aux_not['fechaNacim']
    aux_edad=abs(f- fna).days
    edad=float(aux_edad)/365.25
    
    nNot.tieneEdad=[int(edad)]
    nNot.tieneTemperaturaCorporal=[aux_not['temp']]
    nNot.tieneFrecuenciaCardiaca=[aux_not['Pulso']]
    nNot.tieneFrecuenciaRespiratoria=[aux_not['resp']]         
    nNot.tienePresionArterialSistolica=[aux_not['sist']]
    nNot.tienePresionArterialDistolica=[aux_not['dist']]
    nNot.tienePeso=[aux_not['peso']]
    nNot.tieneTalla=[aux_not['talla']]
    nNot.tienePadecimientoActual=[aux_not['pade']]
    nNot.tieneExploracionFisica=[aux_not['explo']]
    nNot.tieneAnalisis=[aux_not['analis']]
    nNot.tienePronostico=[aux_not['pronos']]
    onto.save(file = "datosRDF.owl", format = "rdfxml")
    return(nNot.iri)
def insertaDato(historia, datos):
    onto = get_ontology("datosRDF.owl").load()
    histori=onto.search(iri=historia)
    histor=histori[0]
    #propiedades
    histor.tieneAntecedentesGinecoObstetricos=[datos['gine']]
    histor.tieneAntecedentesHeredoFamiliares=[datos['hero']]
    histor.tieneAntecedentesPersonalesNoPatologicos=[datos['noPat']]
    histor.tieneAntecedentesPersonalesPatologicos=[datos['pat']]
    
    onto.save(file = "datosRDF.owl", format = "rdfxml")
def creaDiagnostico(enf):
    onto = get_ontology("padecimientosRDF.owl").load()
    enfe=onto.Padecimiento(enf)
    print('creando enfe ',enf)
    onto.save(file='padecimientosRDF.owl', format='rdfxml')
    return(str(enfe.iri))
    
    
def escribeRed(dominio, relacion, rango):
    #relaciones
    global sal
    sal.write('<!-- '+dominio+' --> \n')
    sal.write('<rdf:Description rdf:about="'+dominio+'">\n')
    sal.write('<red:'+relacion+' rdf:resource="'+rango+'"/>\n')
    sal.write('</rdf:Description>\n')
     


def creaMedi(medi):
    onto = get_ontology("tratamientoRDF.owl").load()
    tto=onto.Tratamiento_Farmacologico(medi)
    print('creando medicam ',medi)
    onto.save(file='tratamientoRDF.owl', format='rdfxml')
    return(str(tto.iri))
    
#receta    
def creaNodoRed(nota, diagnosticos, tratamiento):
    global contaNod
    global sal
    sal.write('<rdf:Description rdf:about="'+nota+'">\n')
    for z in diagnosticos:
        sal.write('<red:tieneDiagnostico rdf:resource="'+z+'"/>\n')
    for z in tratamiento:
        contaNod+=1
        print('creando nodo ',contaNod)
        sal.write('<red:tieneTratamiento>\n')
        sal.write('<rdf:Description rdf:nodeID="genid'+str(contaNod)+'">\n')
        sal.write('<rdf:type rdf:resource="http://www.diabetes-mexico.org/red#Dosis_En_Receta"/>\n')
        sal.write('<red:tieneActivoEnReceta rdf:resource="'+z+'"/>\n')
        try:
            sal.write('<red:tieneMedidaIndicadaEnReceta>'+tratamiento[z]['medida']+'</red:tieneMedidaIndicadaEnReceta>\n')
            
        except KeyError:
            pass
        try:
            sal.write('<red:tieneCantidadIndicada rdf:datatype="http://www.w3.org/2001/XMLSchema#float">'
                      +str(tratamiento[z]['canti'])+'</red:tieneCantidadIndicada>\n')
        except KeyError:
            pass
        try:
            sal.write('<red:tieneFrecuenciaIndicada rdf:datatype="http://www.w3.org/2001/XMLSchema#float">'
                          +tratamiento[z]['frec']+'</red:tieneFrecuenciaIndicada>\n')
        except KeyError:
            pass
        except IndexError:
            pass
        sal.write('</rdf:Description>\n')
        sal.write('</red:tieneTratamiento>')
    sal.write('</rdf:Description>')
    
    
    
    
contaPac=6
contaNot=25
contaNod=110
ls=open("ARCHIVOS/exphup.txt","r")
sal=open("codigo_red.txt","w", encoding='utf-8')
for f in ls.readlines():
    fname=f.replace('\n','')
    print(fname)
    wb = load_workbook(filename = "ARCHIVOS/"+fname)
    try:
        
        sheet_ranges = wb['Hoja1']
        #creacion de paciente y expediente
        contaPac+=1
        aux_pat=[] #numero,sexo,fechaNacimiento
        aux_pat.append(str(contaPac))
        aux_pat.append(sheet_ranges['B2'].value)
        aux_pat.append(sheet_ranges['C2'].value)
        expHisIris=creaPaciente(aux_pat)
        expediente=expHisIris[0]
        historia=expHisIris[1]
        fechaNacim=expHisIris[2]
        #creacion de nota medica
        i=2 #indice de la columna fecha de consulta
        while True:
            aux=sheet_ranges['D'+str(i)].value
            
            if aux==None:
                break
            else:
                contaNot+=1
                aux_not={}
                aux_not['conta']=contaNot
                #envio de la fecha de nacimiento del paciente
                aux_not['fechaNacim']=fechaNacim
                
                #resto de los dataproperties
                
                aux_not['fecha']=str(sheet_ranges['D'+str(i)].value)
                try:
                    aux_not['temp']=float(sheet_ranges['F'+str(i)].value)
                except TypeError:
                    aux_not['temp']=float(0.0)
                try:    
                    aux_not['Pulso']=int(sheet_ranges['G'+str(i)].value)
                except TypeError:
                    aux_not['Pulso']=int(0)
                try:    
                    aux_not['resp']=int(sheet_ranges['H'+str(i)].value)
                except TypeError:
                    aux_not['resp']=int(0)
                    
                presion=str(sheet_ranges['I'+str(i)].value).split('/')
                try:
                    aux_not['sist']=int(presion[0])
                    aux_not['dist']=int(presion[1])
                except ValueError:
                    aux_not['sist']=0
                    aux_not['dist']=0
                try:
                    aux_not['peso']=float(sheet_ranges['J'+str(i)].value)
                except TypeError:
                    aux_not['peso']=float(0.0)
                try:
                    aux_not['talla']=float(sheet_ranges['K'+str(i)].value)
                except TypeError:
                    aux_not['talla']=float(0.0)
                aux_not['pade']=str(sheet_ranges['L'+str(i)].value)
                aux_not['explo']=str(sheet_ranges['M'+str(i)].value)
                aux_not['analis']=str(sheet_ranges['N'+str(i)].value)
                aux_not['pronos']=str(sheet_ranges['Q'+str(i)].value)
                
                
                
                
                
                nota=creaNota(expediente, aux_not)
                
                #diagnosticos
                enfer=str(sheet_ranges['O'+str(i)].value).split('\n')
                
                enfermedades=[]
                for e in enfer:
                    e=e.replace(' ','_')
                    enfermedades.append(creaDiagnostico(e))
                
                #receta
                auxR=sheet_ranges['P'+str(i)].value
                if auxR!=None:
                    tratas={}
                    r=0
                    #lista de renglones de la receta
                    aux_rec=auxR.split('\n')
                
                    while (r <len(aux_rec))==True:
                    
                        if 'RECETA:' in aux_rec[r]:
                            pass
                        
                        elif ('LABORATORIO:' or '') == aux_rec[r]:
                            break
                        else:
                            medi=''
                            #palabras por renglon
                            pals=aux_rec[r].split(' ')
                            p=0
                            while (p<len(pals))==True:
                                try:
                                    cant=float(pals[p])
                                    medi=medi[:-1]
                                    #crea medicamento en tto
                                    medicamento=creaMedi(medi)
                                    medi=''
                                    tratas[medicamento]={}
                                    tratas[medicamento]['canti']=cant
                                    p=p+1
                                    tratas[medicamento]['medida']=pals[p]
                                    p=p+1
                                    try:
                                        if pals[p]=='CADA' and pals[p+2]=='HRS':
                                            p=p+1
                                            tratas[medicamento]['frec']=pals[p]
                                    except IndexError:
                                        pass
                                    break
                               
                                                  
                                except ValueError:
                                    medi=medi+str(pals[p])+'_'
                                p+=1
                                if p==len(pals):
                                    break
                        r+=1   
                        if r==len(aux_rec):
                            break
                        
                creaNodoRed(nota, enfermedades, tratas)         
                        
                i+=1
        dato_his={}
        
        sheet_ranges = wb['Hoja2']
        
        dato_his['gine']=str(sheet_ranges['D'+str(i)].value)
        dato_his['heredo']=str(sheet_ranges['E'+str(i)].value)
        dato_his['noPat']=str(sheet_ranges['F'+str(i)].value)
        dato_his['pat']=str(sheet_ranges['G'+str(i)].value)                
        insertaDato(historia, dato_his)
    except KeyError:
        print("No se pudo cargar el archivo")
        
sal.close()