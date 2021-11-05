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


#Recibe un grafo, el nombre del nodo inicial (nodo_actual), y el nodo objetivo (al que se quiere encontrar el camino). Devuelve una lista con los nodos
#Con el objetivo en la posicion 0; y el nodo inicial en la posicion N
def dfs(grafo, nodo_actual, objetivo, visitados = None):

    if visitados == None: #Para que la primera llamada recursiva no tenga que enviar el set
        visitados = set()

    if nodo_actual in visitados:    #Devuelve nada (lista vacia) si se ya paso por ese nodo
        return []

    if nodo_actual == objetivo:     #Llegó al objetivo, empieza a armar la lista.
        visitados.add(nodo_actual)
        return [nodo_actual]

    
    visitados.add(nodo_actual)  #Agrega el nodo actual al set de nodos visitados

    for vecino in grafo.adyacentes(nodo_actual):    #Se busca sigue el DFS en cada uno de los vecinos del nodo actual
        resultado = dfs(grafo, vecino, objetivo,  visitados)    

        if resultado:
            resultado.append(nodo_actual)
            return resultado
    
    return []       #En el caso de que no se haya logrado alcanzar el nodo objetivo, se devuelve una lista vacia
           

#Devuelve en un vector, un camino desde el nodo S, hasta el nodo T en el grafo. en la posicion [0] esta S, y el la posicion [n] esta T.
#Si no encuentra ningun camino, devuelve un vector vacío
def obtener_camino(grafo, s, t):
    camino = dfs(grafo, s, t)
    return camino[::-1]
    

def flujo_ford_fulkerson(grafo, s, t):
    # flujo = {}
    # for v in grafo:
    #     for w in grafo.adyacentes(v):
    #         flujo[(v,w)] = 0

    capacidad_maxima = 0
    
  
    grafo_residual = grafo.copy()
    camino = obtener_camino(grafo_residual,s,t) 
    print(camino)
    while camino:
        capacidad_residual_camino = min_peso(grafo_residual, camino) #peso minimo de camino
        capacidad_maxima += capacidad_residual_camino
    
        for i in range(1, len(camino)):
            if camino[i] in grafo_residual.adyacentes(camino[i-1]):
                # flujo[(camino[i-1], camino[i])] += capacidad_residual_camino
                actualizar_grafo_residual(grafo_residual,camino[i-1],camino[i],capacidad_residual_camino)
        
            else:
                # flujo[(camino[i], camino[i-1])] -= capacidad_residual_camino
                actualizar_grafo_residual(grafo_residual,camino[i],camino[i-1],capacidad_residual_camino)

        camino = obtener_camino(grafo_residual,s,t) 
        print(camino)

    return capacidad_maxima, grafo_residual #, flujo

#en este flujo, el flujo max es la cantidad de aristas que entran a la fuente o salen del sumidero
#(suman lo mismo)
