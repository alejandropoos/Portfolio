import requests
import os
import shutil

api_interna_1= '' #Ingrese la api interna (obtener shipments desde HU's)
api_interna_2= '' #Ingrese la api interna (obtener ctes)

def Validating_HU(data:str):


    '''
    PRE:Recibimos el Dato, contamos las cantidades de digitos para identificar HU'S
    POST: 
    '''
    text = [char for char in data]

    if len(text) < 15 :
        IsHU = False
    else:
        IsHU = True
    
    return IsHU


def leer_archivo(inputs:list, hu_sin_shipments:list) ->list:
    """
    PRE:Se recibe el nombre del archivo a procesar.
    POST:Se retorna como lista los ids de CTES a procesar.
    """
    listado_hus = list()
    listado_shipments_limpios = list()

 
    for linea in inputs:
        if not Validating_HU(linea):
           listado_shipments_limpios.append(linea)
        else:
            listado_hus.append(linea)
    if listado_hus != 0:
        obtener_shipments_de_hus(listado_hus,listado_shipments_limpios,hu_sin_shipments)
    return listado_shipments_limpios



def obtener_ctes(listado_shipments:list, nombre_carpeta:str, formato: list, shipments_sin_cte:list) ->None:
    """
    PRE:Recibimos como lista todos los shipments ademas de el nombre de la carpeta donde se descargaran las NF de los SH.
    POST:Al ser un procedimiento, se retorna un dato de tipo None.
    """
    #colocar los try correspondientes a la conexion con la api
    for i in formato:
      nombre = nombre_carpeta +'_' + i
      os.mkdir(nombre)
      for id_shipment in listado_shipments:
  
          try:
              obtener_cte = requests.get(f"{api_interna_2}/{id_shipment}/download?doctype={i}&caller.id=admin&caller.scopes=admin")
              with open(f"{nombre}\\{id_shipment}.{i}","wb") as cte_descargado:
                  cte_descargado.write(obtener_cte.content)
          except Exception:
              shipments_sin_cte.append(id_shipment)
      comprimir_carpeta(nombre_carpeta +'_' + i)
      print("Obteniendo notas fiscales")


def comprimir_carpeta(nombre_carpeta:str) ->None:
    """
    PRE:Se recibe el nombre de la carpeta a comprimir.
    POST:Una vez comprimida, se retorna un dato de tipo None, esto debido a ser un procedimiento.
    """

    shutil.make_archive(nombre_carpeta,"zip",nombre_carpeta)



def mostrar_shipments_sin_cte(shipments_sin_cte:list, hu_sin_shipments:list) ->None:

    '''PRE:OBTENEMOS LOS SHIPMENTS SIN CTE EN UNA LISTA.
       POST:AL SER UN PROCEDIMIENTO SE RETORNA UN DATO DE TIPO NONE.'''


    if len(shipments_sin_cte) == 0:
        print("se descargaron todos los ctes exitosamente")
    
    else:
        print("SHIPMENTS SIN CTES")
        for shipment in shipments_sin_cte:
            print(shipment)

    if len(hu_sin_shipments) == 0:
        print("Se extrajo toda la data de los hus")
    else:
        print("HUS SIN PODER DESCARGAR SUS DATOS")
        for hu_id in hu_sin_shipments:
            print(hu_id)


def obtener_shipments_de_hus(listado_hus:list, listado_shipments:list, hu_sin_shipments:list) ->None:
    """
    PRE:Recibimos el listado de ctes y el de los shipments(vacio), buscamos obtener los shipments de estos ctes.
    POST:Una vez agregados los shipments de cada cte, se retorna un valor None, dado que es un procedimiento.
    """
    
    for hu_id in listado_hus:
        try:
            informacion_hu = requests.get(f"{api_interna_1}/{hu_id}/internal")
            data_hu_formateada = informacion_hu.json()
            data_shipment = data_hu_formateada["shipments"]
    
            for shipment_id in data_shipment:
                listado_shipments.append(shipment_id["id"])
        except Exception:
             hu_sin_shipments.append(hu_id)

    print("Obteniendo shipments.")


def CTE(input,type,ticket):
    shipments_sin_cte = list()
    hus_sin_shipments = list()
    Listado_shipments = leer_archivo(input, hus_sin_shipments)

    obtener_ctes(Listado_shipments,ticket,type,shipments_sin_cte)
 
    return shipments_sin_cte, hus_sin_shipments



