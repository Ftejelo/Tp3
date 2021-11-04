import queue

from grafo import grafo


def flujo(grafo, s, t):
  flujo = {}
  for v in grafo:
    for w in grafo.adyacentes(v):
      flujo[(v,w)] = 0
  
  grafo_residual = grafo.copy()
  camino = obtener_camino(grafo_residual,s,t) 
  while camino:
    capacidad_residual_camino = min_peso(grafo, camino) #peso minimo de camino
    
    for i in range(1, len(camino)):
      if camino[i] in grafo.adyacentes(camino[i-1]):
        flujo[(camino[i-1], camino[i])] += capacidad_residual_camino
        actualizar_grafo_residual(grafo_residual,camino[i-1],camino[i],capacidad_residual_camino)

      else:
        flujo[(camino[i], camino[i-1])] -= capacidad_residual_camino
        actualizar_grafo_residual(grafo_residual,camino[i],camino[i-1],capacidad_residual_camino)

  return flujo

#en este flujo, el flujo max es la cantidad de aristas que entran a la fuente o salen del sumidero
#(suman lo mismo)
