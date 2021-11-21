def main():
    entrada = input(f"Por favor ingrese un número, si desea salir, escriba exit... ")
    salir = "exit"
    if entrada == salir:
        print("Hasta luego!")
        pass
    else:
        try:
            modulo = int(entrada)%2
            if modulo == 0:
                estado = "par"
            elif modulo != 0:
                estado = "impar"
            print(estado)
            main()
        except TypeError:
            print("Atencion! Ingrese únicamente números...")
            main()  
        except ValueError:
            print("Atencion! Ingrese únicamente números enteros...")
            main()

main()
