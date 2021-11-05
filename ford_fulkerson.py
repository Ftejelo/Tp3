import queue

from grafo import Grafo

def actualizar_grafo_residual(grafo_residual, u, v, valor):
    peso_anterior = grafo_residual.peso(u,v)

    if peso_anterior <= valor:
        grafo_residual.borrar_arista(u,v)
    else:
        grafo_residual.cambiar_peso(u,v,peso_anterior - valor)
    
    if not grafo_residual.estan_unidos(v,u):
        grafo_residual.agregar_arista(v,u, valor)
    
    else:
        peso_anterior_residual = grafo_residual.peso(v,u)
        grafo_residual.cambiar_peso(v, u, peso_anterior_residual + valor)



def min_peso(grafo, camino): #consigue el minimo peso de los aristas involucrados en el camino (lista de v)
    min_peso = float('inf')

    for i in range(len(camino)-1):
      peso = grafo.peso_arista(camino[i],camino[i+1])
      if peso < min_peso:
        min_peso = peso

    return min_peso


#HAY QUE ARREGAR
def dfs(grafo, nodo_actual, objetivo, visitados = None):
    if visitados == None:
        visitados = set()


    if nodo_actual in visitados:
        return []

    if nodo_actual == objetivo:
        visitados.add(nodo_actual)
        return [nodo_actual]


    for vecino in grafo.adyacentes(nodo_actual):
        visitados.add(nodo_actual)
        resultado = dfs(grafo, vecino, objetivo,  visitados)

        if resultado:
            resultado.append(nodo_actual)
            return resultado
    
    return []
           
#ARREGLAR JUNTO A DFS
def obtener_camino(grafo, s, t):
    camino = dfs(grafo, s, t)
    return camino[::-1]
    

    
    

def flujo_ford_fulkerson(grafo, s, t):
    flujo = {}
    for v in grafo:
        for w in grafo.adyacentes(v):
            flujo[(v,w)] = 0

    capacidad_maxima = 0
    
  
    grafo_residual = grafo.copy()
    camino = obtener_camino(grafo_residual,s,t) 
    print(camino)
    while camino:
        capacidad_residual_camino = min_peso(grafo, camino) #peso minimo de camino
        capacidad_maxima += capacidad_residual_camino
    
        for i in range(1, len(camino)):
            if camino[i] in grafo.adyacentes(camino[i-1]):
                #flujo[(camino[i-1], camino[i])] += capacidad_residual_camino
                actualizar_grafo_residual(grafo_residual,camino[i-1],camino[i],capacidad_residual_camino)
        
            else:
                #flujo[(camino[i], camino[i-1])] -= capacidad_residual_camino
                actualizar_grafo_residual(grafo_residual,camino[i],camino[i-1],capacidad_residual_camino)

        camino = obtener_camino(grafo_residual,s,t) 
        print(camino)

    return capacidad_maxima, grafo_residual

#faltan funciones obtener_camino

#en este flujo, el flujo max es la cantidad de aristas que entran a la fuente o salen del sumidero
#(suman lo mismo)