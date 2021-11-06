from grafo import Grafo
import ford_fulkerson as ff
import csv

def main():


    # try:
    #     ruta = sys.argv[1]
    #     file = open(ruta)
    # except IndexError:
    #     print("No se ingresó ningun archivo.")
    #     return
    # except FileNotFoundError:
    #     print("No se encontró ningun archivo con ese nombre.")
    #     return
    # except:
    #     print("Hubo algun error")

    ruta = input("ruta: ")

    file = open(ruta)  
    

    grafo = Grafo(True)
    try:
        with file as archivo:
            csv_reader = csv.reader(archivo)
            for line in csv_reader:
                ciudadInicio, ciudadFin, distancia = line

                if ciudadInicio not in grafo:
                    grafo.agregar_vertice(ciudadInicio)
                    
                if ciudadFin not in grafo:
                    grafo.agregar_vertice(ciudadFin)

                grafo.agregar_arista(ciudadInicio, ciudadFin, distancia)
    except:
        print("Paso algo inesperado, intente ejecutar el programa nuevamente")
        print(ruta)
        file.close()
        return

    file.close()

    grafo_peso_uno = grafo.copy_con_pesos(1)


    resultado = ff.flujo_ford_fulkerson(grafo, "s", "t")

    resultado2= ff.flujo_ford_fulkerson(grafo_peso_uno, "s", "t")

    print("distancia:", resultado[0])
    print(resultado[1])

    print()

    print(resultado2[0])
    print(resultado2[1])

    print(resultado2[1].set_unilateralmente_conexo_desde("s"))

main()