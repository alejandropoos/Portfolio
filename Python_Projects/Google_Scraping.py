from googlesearch import search
import pandas as pd
from openpyxl import load_workbook

def saved(lista):
    df = pd.DataFrame(lista, columns=[f'URLS de la busqueda: {busqueda}'])
    df.to_excel(f"URLs_{busqueda}.xlsx", index=False)

busqueda = input(f"Realice la busqueda de coincidencias en URL's: ")
resultados = search(busqueda, lang="spanish", num_results=100)
lista = list()
for r in resultados:
	lista.append(r)
ancho = len(f"URLs de la busqueda: {busqueda}")
saved(lista)

libro = load_workbook(f"URLs_{busqueda}.xlsx")
sheet = libro.active 
sheet.column_dimensions['A'].width = ancho
libro.save(f"URLs_{busqueda}.xlsx")