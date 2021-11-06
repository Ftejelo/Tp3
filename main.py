from grafo import Grafo
import ford_fulkerson as ff
import csv
import sys

def main():


    try:
        ruta = sys.argv[1]
        file = open(ruta)

    except IndexError:
        print("No se ingresó ningun archivo.")
        return

    except FileNotFoundError:
        print("No se encontró ningun archivo con ese nombre.")
        return
        
    except:
        print("Hubo algun error")

    # ruta = input("ruta: ")

    # file = open(ruta)  
    

    grafo = Grafo(True)
    nodo_s = None
    nodo_t = None
    try:
        with file as archivo:
            csv_reader = csv.reader(archivo)
            nodo_s = next(csv_reader)[0]    #Lectura nodo fuente
            nodo_t = next(csv_reader)[0]    #lectura nodo sumidero

            for line in csv_reader:         #lectura ciudades y aristas
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

    grafo_peso_uno = grafo.copy_con_pesos(1)    #Crea un grafo con las mismas ciudades y con las aristas en las mismas direcciones, pero todas de peso 1.


    resultado = ff.flujo_ford_fulkerson(grafo, nodo_s, nodo_t)

    resultado2= ff.flujo_ford_fulkerson(grafo_peso_uno, nodo_s, nodo_t)

    print("La mayor cantidad de pasajeros que pueden ir desde la ciudad", nodo_s, "hasta la ciudad", nodo_t, "son:", resultado[0])
    print()

    set_conexo = resultado2[1].set_unilateralmente_conexo_desde(nodo_s)
    conexiones_publicidades = ff.buscar_conexiones_externas_a_set(grafo_peso_uno, set_conexo)

    if (len(conexiones_publicidades) == 1):
        print("La publicidad debería ser puesta en el viaje que va desde la ciudad", conexiones_publicidades[0][0], "hasta", conexiones_publicidades[0][1] + ".")

    else:
        print("Las publicidades deberían ser puestar en los viajes que van de las ciudades:")

        primera_iteracion = True
        for conexion in conexiones_publicidades:
            if not primera_iteracion:
                print(",")
            print("desde", conexion[0], "hasta", conexion[1], end="")
            primera_iteracion = False

        print(".")




main()