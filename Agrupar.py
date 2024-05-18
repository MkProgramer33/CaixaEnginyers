import InfoMapa as map
from sklearn.cluster import KMeans
import numpy as np

'''
Este elagoritmo sirve para saber cuál será la ruta dependiendo de que día es del día 1-5
Recivirá:
    - Una lista de municipios con sus cordenadas
Devuelve:
    - Una lista con ciunco listas de municipios ya agrupados
'''

def agrupar_municipios(paradas, num_grupos):
    if not paradas:
        raise ValueError("El diccionario de paradas está vacío.")
    
    coordenadas = []
    codINE_validos = []
    for codINE, info in paradas.items():
        if 'longitud' in info and 'latitud' in info and info['longitud'] is not None and info['latitud'] is not None:
            coordenadas.append((info['longitud'], info['latitud']))
            codINE_validos.append(codINE)

    coordenadas = [coord for coord in coordenadas if not np.isnan(coord[0]) and not np.isnan(coord[1])]
    kmeans = KMeans(n_clusters=num_grupos, random_state=42)
    kmeans.fit(coordenadas)

    # Obtener las etiquetas de grupo asignadas a cada punto de datos
    labels = kmeans.predict(coordenadas)
    
    # Inicializar los grupos como listas vacías
    grupos = [[] for _ in range(num_grupos)]

    # Asignar cada coordenada a su grupo correspondiente
    for i, label in enumerate(labels):
        grupos[label].append((codINE_validos[i], coordenadas[i]))

    return grupos


mapa = map.Mapa()
map.load('DatosMunicipios.xlsx', mapa)
grupos = agrupar_municipios(mapa.paradas, 5)
print(len(grupos[0]), ",", len(grupos[1]), ",", len(grupos[2]), ",", len(grupos[3]), ",", len(grupos[4]))

