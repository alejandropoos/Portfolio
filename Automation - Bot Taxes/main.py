import shutil
import os, platform, logging
from datetime import datetime
from numpy import where
from Bot import *
from cte import *
from atlassian import Jira
from notas_fiscales_masivas import *
from time import sleep
import requests

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H:%M:%S")
date_time = now.strftime("%d-%m-%Y_%Hhs%Mmin")

if platform.platform().startswith('Windows'):
    fichero_log = os.path.join(os.getenv('HOMEDRIVE'), 
                               os.getenv("HOMEPATH"),
                               f'Bot_NF-CTE_{date_time}.log')
else:
    fichero_log = os.path.join(os.getenv('HOME'), f'Bot_NF-CTE_{date_time}.log')
tickets_resueltos=open(f"Logs\\tickets_resueltos_{date_time}.txt","w") 
tickets_no_resueltos =open(f"Logs\\tickets_no_resueltos_{date_time}.txt","w")
print('Archivo Log en ', fichero_log)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    filename = fichero_log,
                    filemode = 'w',)

api_token=''    #BORRAR API TOKEN ANTES DE COMMITEAR
email=''    #API Token del usuario en Jira
URL_base=''  #URL base de proyecto Jira (Ej: https://xxxxxxxx.atlassian.net)
jira = Jira(url=URL_base, username=email, password=api_token)

issue_key = []
status_in_progress = []
tickets_incompletos = []
tickets_recorridos = []
excepciones=['pdf', "pdf's",'xml', 'xmls',"xml's"]
excepciones_plurales=["pdfs", "xmls"]
excepciones_con_apostrofes=["pdf's","xml's"]
excepciones2=['ctes', "cte's",'cte', "ct-e", "ct-es", "ct-e's"]

def datosticket(issue_key):
    if issue_key in tickets_incompletos:
        pass
    if issue_key in tickets_recorridos:
        pass
    issue = jira.issue_fields(issue_key)
    logistica=str(issue['customfield_13883'][0]['value'])
    try:
        requestType=str(issue['customfield_11100']['requestType']['name'])
    except TypeError:
        print('Ticket Recurrente, sin requestType')
        pass
    status=issue['status']['name']
    if status == 'Waiting for support' or status == 'Esperando por Soporte':
        excepciones=[' ', '-']
        title=str(issue['summary'])
        requestType=str(issue['customfield_11100']['requestType']['name'])
        #ubicacion=str(issue['customfield_13910']['child']['value'])
        site=str(issue['customfield_13910']['value'])
        logistica=str(issue['customfield_13883'][0]['value'])
        descripcion=str(issue['description'])
        #warehouse=list(ubicacion)
        '''warehouse=str(warehouse[0] + warehouse[1] + warehouse[2] + warehouse[3] + warehouse[4] + warehouse[5] + warehouse[6])
        for letra in warehouse:
            if letra in excepciones:
                warehouse=warehouse.replace(letra, '')
        warehouse=str(warehouse)'''
        ticket=issue_key
        tickets_recorridos.append(ticket)
        logging.info(f'Extraccion de datos del ticket {ticket} finalizado.')
        return ticket, title, site, logistica, requestType, descripcion, status
    else:
        print('El status de: ' + issue_key + ' no esta en Waiting for support - ' + status)
        tickets_recorridos.append(issue_key)
        status_in_progress.append(issue_key)

def extraer_tickets():
    logging.info('---------------------------------------------------------  \n')
    logging.info('Inicializando la extraccion de tickets. \n')

    archivo=open('tickets.txt', 'r+')
    lineas_texto=archivo.readlines()
    archivo.close()

    lista_limpia=[]

    for linea in lineas_texto:
        linea_limpia = linea.replace('\n', '')
        lista_limpia.append(linea_limpia)

    issue_key = lista_limpia

    for x in issue_key:
        for a in tickets_recorridos:
            if x==a:
                issue_key.remove(a)
                
    return issue_key 

def Display_txt(List): 
   '''
    PRE:Recibe Una Lista de Caracteres.
    POST:Retornamos una cadena completa de caracteres.    
    '''
   display = ''  
   for i in range(len(List)):
      char = List[i]
      display = display + char 
   return display

def cleaner(text):
    '''
    PRE:Recibe una cadena de texto.
    POST:Retornamos cadena de texto sin caracteres especiales.    
    '''
    exception = ['.','#',')','(',',','"',';','[',']','}','{','?','=','@','*','+','<','>',':','¡','_', '-']
    for i in exception:
       t = [char for char in text if char != str(i)]
       text = t
    return Display_txt(text)

def processing (sentences) :
    '''
    PRE:Recibe una cadena de texto.
    POST:Retornamos la Lista de elementos input , type y orden.    
    '''
    classNbD = pickle.load(open("finalized_ClassNBD.sav",'rb'))
    TvD = pickle.load(open("finalized_TVD.sav", 'rb'))
    items = {
                     'none':0,
                     'type':0,  #pdf o xml
                     'shipment':0,
                     'hu': 0,
                     'orden': 0, #cte/ notas
            }
    input = list()
    type = list()
    orden = list()
    for i in sentences.split():
     txt = cleaner(i.lower())
     items.update(bot(txt,classNbD,TvD))
     if items['shipment'] != 0 or items['hu'] != 0 :
         if len(txt) >= 11:
          input.append(txt)
          items['shipment'] = 0
          items['hu'] = 0

     elif items['type'] != 0 :
         type.append(txt)
         items['type'] = 0

     elif items['orden'] != 0:
         orden.append(txt)
         items['orden'] = 0   
    return input , type , orden

def action_comment (ticket, archivo, formato):
    '''
    PRE:Recibe ticket y archivo a adjuntar.
    POST:Comenta y adjunta en el ticket.    
    '''
    jira.add_attachment(ticket, archivo)    #NF PDF
    jira.issue_add_comment(ticket, f'Boa tarde, segue anexo o arquivo de {formato}  \n [^{archivo}]')

def action_comment_error(ticket,list,words):
    '''
    PRE:Recibe ticket, informacion de datos no descargados y un comentario definido.
    POST:Comenta y adjunta en el ticket.    
    '''
    strings=str()
    for i in list:
        strings = strings + '\n' + i
    jira.issue_add_comment(ticket, f'{words} : {strings}') 

def resolution_process(archivos_orden, ticket,status,HU_SIN,shipment_sin,orden):

    for archivo in archivos_orden:
        logging.info(f'Ticket {ticket} {orden}.')
        directorio=archivo.replace('.zip', '')
        if status == 'Waiting for support':
            jira.issue_transition(ticket, 'In Progress')
            status='In Progress'
        elif status == 'Esperando por Soporte':
            jira.issue_transition(ticket, 'En curso')
            status='En curso'
        action_comment(ticket,archivo,orden)
        if status == 'In Progress':
            jira.issue_transition(ticket, 'Resolved')
            status='Resolved'
        elif status == 'En curso':
            jira.issue_transition(ticket, 'Resuelta')
            status='Resuelta'
            tickets_resueltos.write(f'{ticket}\n')
            logging.info(f'Ticket {ticket} finalizado.')

        os.remove('./' + archivo)
        shutil.rmtree(directorio)
        if HU_SIN != []:
            strings = f'HU sin poder descargar {orden}'
            action_comment_error(ticket,HU_SIN,strings)
        if shipment_sin != []:
            strings = f'Shipments sin poder descargar {orden}'
            action_comment_error(ticket,shipment_sin,strings)

def main():
    keys = extraer_tickets()
    for i in keys:
        logging.info('---------------------------------------------------------  \n')
        datos = datosticket(i)
        if i not in status_in_progress:
            ticket=datos[0]
            status=datos[6]
            descripcion=datos[5]
            descripcion=descripcion.replace('\n', ' ')
            inputxt = descripcion
            shipment , type , orden = processing(inputxt.replace("/", " "))
            #tickets_resueltos=open(f"Logs\\tickets_resueltos_{date_time}.txt","a") 
            print(orden)
            print(type)
            if shipment == []:
                try:
                    issue = jira.issue_fields(i)
                    attachType = str(issue['attachment'][0]['mimeType'])
                    if attachType == 'text/plain':
                        attachLink = str(issue['attachment'][0]['content'])
                        r = requests.get(attachLink, auth = (jira.username, jira.password))   
                        if r.status_code == 200:   
                            with open('shipments_txt.txt', "wb") as f:    
                                for bits in r.iter_content():   
                                    f.write(bits)
                    validacion = os.path.exists('shipments_txt.txt')
                    if validacion == True:
                        with open('shipments_txt.txt', "r") as file:
                            for line in file:
                                line=line.replace('\n', '')
                                shipment.append(line)
                except IndexError:
                    pass

            if orden != [] and shipment != []:
 
                for i in range(len(type)):
                    if type[i] in excepciones:
                        if type[i] in excepciones_con_apostrofes:
                            type[i]=type[i].replace("'s", "")
                        if type[i] in excepciones_plurales:
                            type[i]=type[i].replace("s","")
                    else:
                        del type[i]
                        print(type)
               
                archivos_cte=list()
                archivos_nf=list()
                try: 
                    for i in orden:
                        if len(i) >= 2:
                            print(i)
                            if i in excepciones2:
                                Shipment_sin_CTE, HU_sin_CTE = CTE(shipment,type,ticket)
                                for a in type:
                                    archivos_cte.append(f'{ticket}_{a}.zip')
                                pass
                            else:
                                for i in type:
                                    Shipment_sin_NF, HU_sin_NF = NF(shipment,i,ticket)
                                    archivos_nf.append(f'{ticket}_NF_{i}.zip')
                                    pass
                        else:
                            logging.error(f'CARACTER: {i} IDENTIFICADO COMO ORDEN')
                            continue
                except Exception:
                    tickets_no_resueltos.write(f"Error en el proceso de obtener documentos - " + ticket + '\n')
                    logging.warning(f'EXCEPTION ERROR - Ticket {ticket} Error en el proceso de obtener documentos.')
                    tickets_incompletos.append(ticket)
                try:
                    if archivos_nf != []:
                       resolution_process(archivos_nf,ticket,status,HU_sin_NF,Shipment_sin_NF,'notas fiscal')
                       tickets_resueltos.write(f'Ticket {ticket} - NF resuelto. \n')
                    if archivos_cte != []:
                       resolution_process(archivos_cte,ticket,status,HU_sin_CTE,Shipment_sin_CTE,'CTE')
                       tickets_resueltos.write(f'Ticket {ticket} - CTe resuelto. \n')
                    archivos_nf.clear()
                    archivos_cte.clear()
                    if validacion == True:
                        os.remove('source\\shipments_txt.txt')
                    print('Proceso finalizado. - ' + ticket)
                except Exception:
                    tickets_no_resueltos.write(f"Error en el proceso de resolucion  - " + ticket + '\n')
                    logging.warning(f'EXCEPTION ERROR - Ticket {ticket} Error en el proceso de resolucion.')
                    tickets_incompletos.append(ticket)      
            else:
                tickets_no_resueltos.write(f"El ticket no cumple con los requisitos para ser resuelto Orden o shipments vacios - " + ticket + '\n')
                logging.warning(f'Ticket {ticket} no cumple con los requisitos para ser resuelto Orden o shipment vacios.')
                tickets_incompletos.append(ticket) 
        if len(tickets_recorridos) == issue_key:
            tickets_recorridos.clear()
        tickets_resueltos.close()
        archivo=open('tickets.txt', 'r+')
        lineas_texto=archivo.readlines()
        archivo.close()
        lineas_texto.remove(lineas_texto[0])
        with open('tickets.txt', 'w') as archivo:
            for i in lineas_texto:
                archivo.write(i)
        sleep(10)
        continue
    extraer_tickets()
    if issue_key != []:
        main()

if __name__ == "__main__" :
  main()
