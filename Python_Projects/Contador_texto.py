def main():
    entrada = input("Ingrese un texto por favor, si desea salir escriba exit: ")
    salir = "exit"
    if entrada == salir:
        print("Gracias por utilizar mi contador, hasta luego!")
        pass
    else:
        caracteres = len(entrada)
        palabras = len(entrada.split())
        lista = [caracteres, palabras]
        menu(lista[0], lista[1])
        pass

def menu(caracteres, palabras):
    print("Menu:")
    print("1 - Cantidad de caracteres")
    print("2 - Cantidad de palabras")
    try:
        eleccion = input("Por favor, eliga un numero del menu... ")
        if eleccion == "1":
            print(f"Su texto tiene {caracteres} caracteres, recuerde que los espacios y números también cuentan.")
            main()
            pass
        elif eleccion == "2":
            print(f"Su texto tiene {palabras} palabras.")
            main()
            pass
        else:
            print("Por favor, ingrese un valor dentro de los indicados en el menu.")
            menu(caracteres, palabras)
    except:
        print("Por favor, ingrese un valor dentro de los indicados en el menu.")
        menu(caracteres, palabras)

main()