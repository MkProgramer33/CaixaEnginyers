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

def TSP_Algorythm(paradas):
    '''
    Encuentra el camino más corto desde el punto central hasta todos los puntos de la lista.
    '''
    cost_matrix = makeMatrix(paradas)

    n = len(cost_matrix)
    # dp[mask][i] guarda el costo mínimo para visitar el conjunto de ciudades representado por mask
    # terminando en la ciudad i
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Empezamos en la ciudad 0
    
    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):
                for j in range(n):
                    if not mask & (1 << j):
                        dp[mask | (1 << j)][j] = min(dp[mask | (1 << j)][j], dp[mask][i] + cost_matrix[i][j])
    
    # Recuperar la ruta
    mask = (1 << n) - 1  # Todas las ciudades visitadas
    last = 0
    min_cost = float('inf')
    
    for i in range(1, n):
        if dp[mask][i] + cost_matrix[i][0] < min_cost:
            min_cost = dp[mask][i] + cost_matrix[i][0]
            last = i
    
    # Reconstrucción de la ruta
    path = []
    current_city = last
    current_mask = mask
    
    for _ in range(n - 1):
        path.append(current_city)
        next_city = -1
        for i in range(n):
            if current_mask & (1 << i) and dp[current_mask][current_city] == dp[current_mask ^ (1 << current_city)][i] + cost_matrix[i][current_city]:
                next_city = i
                break
        current_mask ^= (1 << current_city)
        current_city = next_city
    
    path.append(0)
    path.reverse()
    
    keys = return_dictionary_keys(paradas)
    px = []
    for i in path:
        px.append(paradas[keys[i]])

    py.append(pz[0])
    return px, min_cost

def makeMatrix(paradas):
    num_paradas = len(paradas)
    # Create a matrix of zeros
    matrix = np.zeros((num_paradas, num_paradas))

    keys = return_dictionary_keys(paradas)

    # Iterate over each node and its connections
    for i, parada1 in enumerate(keys):
        for j, parada2 in enumerate(keys):
            if j <= i:
                continue
            # Calculate the cost between the two nodes
            
            lat1 = paradas[parada1]['latitud']
            lon1 = paradas[parada1]['longitud']
            lat2 = paradas[parada2]['latitud']
            lon2 = paradas[parada2]['longitud']
            try:
                cost = obtener_tiempo_en_coche([lat1, lon1], [lat2, lon2])
            except:
                cost = 5000
            print(paradas[parada1]['municipio'], paradas[parada2]['municipio'], "Costo:", cost)

            # Update the matrix with the calculated cost
            matrix[i, j] = cost
            matrix[j, i] = cost
    
    return matrix

def return_dictionary_keys(dictionary):
    return list(dictionary.keys())