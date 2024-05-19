import numpy as np
from DistanciasMapa import obtener_tiempo_en_coche
from DistanciasMapa import obtener_distancia_en_coche

'''
Este elagoritmo sirve para calcular la ruta optima para passar por todos los municipios.
Recivirá:
    - Una lista de municipios con sus cordenadas
Devuelve:
    - Una ruta
'''
def nearest_neighbor_algorithm(paradas, municipio):
    '''
    Encuentra una ruta aproximada usando el Algoritmo del Vecino Más Cercano.
    '''
    if municipio not in paradas.values():
        key = 8082
        paradas[key] = municipio[8082]
    
    cost_matrix = makeMatrix(paradas)
    n = len(cost_matrix)
    visited = [False] * n
    path = [0]
    visited[0] = True
    current_city = 0
    for _ in range(1, n):
        nearest_neighbor = find_nearest_neighbor(cost_matrix, current_city, visited)
        path.append(nearest_neighbor)
        visited[nearest_neighbor] = True
        current_city = nearest_neighbor

    path.append(0)  # Volver al punto de partida
    total_cost = sum(cost_matrix[path[i]][path[i + 1]] for i in range(n))

    keys = list(paradas.keys())
    px = [paradas[keys[i]] for i in path]

    return px, total_cost

def find_nearest_neighbor(cost_matrix, current_city, visited):
    nearest_neighbor = -1
    nearest_cost = float('inf')
    for j, cost in enumerate(cost_matrix[current_city]):
        if not visited[j] and cost < nearest_cost:
            nearest_cost = cost
            nearest_neighbor = j
    return nearest_neighbor

def TSP_Algorythm(paradas):
    '''
    Encuentra el camino más corto desde el punto central hasta todos los puntos de la lista.
    '''
    cost_matrix = makeMatrix(paradas)
    n = len(cost_matrix)
    dp = np.full((1 << n, n), float('inf'))
    dp[1][0] = 0  # Empezamos en la ciudad 0
    
    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):
                for j in range(n):
                    if not mask & (1 << j):
                        dp[mask | (1 << j)][j] = min(dp[mask | (1 << j)][j], dp[mask][i] + cost_matrix[i][j])
    
    mask = (1 << n) - 1  # Todas las ciudades visitadas
    last = np.argmin([dp[mask][i] + cost_matrix[i][0] for i in range(1, n)])
    min_cost = dp[mask][last] + cost_matrix[last][0]
    
    path = [0] * n
    current_city = last
    current_mask = mask
    
    for i in range(n - 2, -1, -1):
        path[i] = current_city
        next_city = np.argmin([dp[current_mask ^ (1 << current_city)][j] + cost_matrix[j][current_city] 
                               for j in range(n) if current_mask & (1 << j)])
        current_mask ^= (1 << current_city)
        current_city = next_city
    
    path[-1] = 0
    keys = list(paradas.keys())
    px = [paradas[keys[i]] for i in path]

    return px, min_cost

def makeMatrix(paradas):
    num_paradas = len(paradas)
    matrix = np.zeros((num_paradas, num_paradas))
    keys = list(paradas.keys())

    for i in range(num_paradas):
        lat1, lon1 = paradas[keys[i]]['latitud'], paradas[keys[i]]['longitud']
        for j in range(i + 1, num_paradas):
            lat2, lon2 = paradas[keys[j]]['latitud'], paradas[keys[j]]['longitud']
            try:
                cost = obtener_tiempo_en_coche([lat1, lon1], [lat2, lon2])
            except:
                cost = 5000
            matrix[i, j] = matrix[j, i] = cost
    
    return matrix