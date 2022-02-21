import requests
import os
import threading
import time 
import shutil
import main

api_interna_1= '' #Ingrese la api interna (obtener shipments desde HU's)
api_interna_2= '' #Ingrese la api interna (obtener datos de shipments)
api_interna_3= '' #Ingrese la api interna (obtener notas fiscales)

SITE_ID = "MLB"

def obtener_shipments_de_hus(listado_hus:list, listado_shipments_limpios:list, hu_sin_shipments:list) ->None:
    """
    PRE:Recibimos el listado de ctes y el de los shipments(vacio), buscamos obtener los shipments de estos ctes.
    POST:Una vez agregados los shipments de cada cte, se retorna un valor None, dado que es un procedimiento.
    """

    try:
        for hu_id in listado_hus:
            informacion_hu = requests.get(f"{api_interna_1}{hu_id}/internal")
            data_hu_formateada = informacion_hu.json()
            data_shipment = data_hu_formateada["shipments"]

            for shipment_id in data_shipment:
                listado_shipments_limpios.append(shipment_id["id"])
    except Exception:
        hu_sin_shipments.append(hu_id)

    
    print("SHIPMENTS OBTENIDOS")


def obtener_datos_shipments(listado_shipments_limpios:list, shipments_sin_datos:list, 
                            shipments_con_datos:list, site_id:str , formato:str) ->None:

    '''
    PRE:Recibimos en una lista los shipmets y una lista vacia donde se agregan los shipments que no se pueda obtener informacion.
    POST:Por ser un procedimiento se retorna un valor de tipo None.
    '''
    
    datos_shipment_id = 0
    for shipment_id in listado_shipments_limpios:

        try:
            datos_de_shipment_id = requests.get(f"{api_interna_2}/{shipment_id}/invoice_data/all?siteId={site_id}&caller.scopes=admin&caller.id=admin")
            datos_parseados_a_json = datos_de_shipment_id.json()
            shipments_con_datos.append((shipment_id, datos_parseados_a_json[datos_shipment_id]['sender_id'], 
                            datos_parseados_a_json[datos_shipment_id]['fiscal_key'], formato))
            #print(f"{shipment_id} - Informacion obtenida")
        except Exception:
            shipments_sin_datos.append(shipment_id)


def validar_hu(data:str):

    '''
    PRE:Recibimos el Dato, contamos las cantidades de digitos para identificar HU'S
    POST: 
    '''
    text = [char for char in data]

    if len(text) < 15 :
        is_hu = False
    else:
        is_hu = True
    
    return is_hu
    

def obtener_listado_shipments(inputs:str, hu_sin_shipments:list) ->list:
    
    '''
    PRE:Recibe el nombre del archivo como string.
    POST:Retornamos en una lista los shipments id.    
    '''

    listado_shipments_limpios = list()
    listado_hu = list()
   
    for shipment_id in inputs:
        if not validar_hu(shipment_id):
            listado_shipments_limpios.append(shipment_id)
        else :
            listado_hu.append(shipment_id)
    if len(listado_hu) != 0:
        obtener_shipments_de_hus(listado_hu, listado_shipments_limpios, hu_sin_shipments)
    
    return listado_shipments_limpios


def obtener_notas_fiscales(shipments_con_datos:list, nombre_carpeta_de_descarga:str, shipments_sin_datos:list, formato:str) ->None:

    """
    PRE:Recibimos como lista todos los shipments ademas de el nombre de la carpeta donde se descargaran las NF de los SH.
    POST:Al ser un procedimiento, se retorna un dato de tipo None.
    """
    nombre = nombre_carpeta_de_descarga +'_NF_' + formato
    os.mkdir(nombre)
    for shipment_id, sender_id, fiscal_key, type in shipments_con_datos:

        try:
            nota_fiscal = requests.get(f"{api_interna_3}/{shipment_id}/nfe/{fiscal_key}?doctype={type}&caller.id={sender_id}&caller.scopes=admin")
            with open(f"{nombre}\\{shipment_id}.{formato}","wb")as archivo_pdf:
                archivo_pdf.write(nota_fiscal.content)
                #print(f"{shipment_id} - Nota fiscal descargada")
        except Exception:
            shipments_sin_datos.append(shipment_id)
    comprimir_carpeta(nombre)


def mostrar_notas_fiscales_no_descargadas(shipments_sin_datos:list, hu_sin_shipments:list) ->None:

    '''
    PRE:Recibimos una lista de los shipments sin notas fiscales.
    POST:Al ser procedimiento retornamos un tipo de dato None.
    '''
    vacio = 0
    os.system("cls")
    
    if len(shipments_sin_datos) == vacio:
        print("Todas las notas se pudieron descargar correctamente.")
    else:
        print("SHIPMENTS QUE NO SE PUDO DESCARGAR SUS NOTAS FISCALES.")
    
        for shipment_id in shipments_sin_datos:
            print(shipment_id)
            
    
    if len(hu_sin_shipments) == vacio:
        print("Se extrajo toda la data de los hus")
    else:
        print("HUS SIN PODER DESCARGAR SUS DATOS")
        for hu_id in hu_sin_shipments:
            print(hu_id)



def comprimir_carpeta(nombre_carpeta:str) ->None:
    """
    PRE:Se recibe el nombre de la carpeta a comprimir.
    POST:Una vez comprimida, se retorna un dato de tipo None, esto debido a ser un procedimiento.
    """

    shutil.make_archive(nombre_carpeta,"zip",nombre_carpeta)


def NF(inputs,type,ticket):
    hus_sin_shipments = list()
    shipments_con_datos = list()
    shipments_sin_datos = list()
    listado_shipments_limpios = obtener_listado_shipments(inputs, hus_sin_shipments)
    
    obteniendo_datos_shipments = threading.Thread(target=obtener_datos_shipments, 
                                args=(listado_shipments_limpios, shipments_sin_datos, shipments_con_datos, SITE_ID,type))

    descargando_notas_fiscales = threading.Thread(target=obtener_notas_fiscales, 
                                args=(shipments_con_datos, ticket, shipments_sin_datos,type))
    
    obteniendo_datos_shipments.start() 
    time.sleep(0.8)
    descargando_notas_fiscales.start()
    descargando_notas_fiscales.join()
    return shipments_sin_datos, hus_sin_shipments


