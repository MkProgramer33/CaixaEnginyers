import numpy as np
from printLineas import print_dividing_lines
from DistanciasMapa import obtener_tiempo_en_coche
from DistanciasMapa import obtener_distancia_en_coche

'''
Este elagoritmo sirve para saber cuál será los municipios por los que passarà la ruta
dependiendo de que día es del día 1-5 utilizando un algoritmo que divide el mapa en facciones.
Recivirá:
    - Una lista de municipios con sus cordenadas
Devuelve:
    - Una lista con ciunco listas de municipios ya agrupados
'''

def agrupar_municipios(paradas):
    if not paradas:
        raise ValueError("El diccionario de paradas está vacío.")
    
    points = []
    for key, value in paradas.items():
        points.append([(value['latitud'], value['longitud']), key])

    central, lines = find_dividing_lines(paradas, [2.15899, 41.38879])
    grupo = divide_points(points, central, lines)

    lista_municipios = []
    for municipios in grupo:
        if municipios:
            municipio = {}
            for key in municipios:
                municipio[key[1]] = paradas[key[1]]
            lista_municipios.append(municipio)
    return lista_municipios
    


def find_dividing_lines(points, central):
    """
    Encuentra cuatro rectas que parten del punto central y dividen el espacio
    en 5 partes iguales en términos de cantidad de puntos.
    
    :param points: Lista de puntos en el formato [(x1, y1), (x2, y2), ...]
    :return: Una lista de tuplas representando las rectas en el formato (angle, 'line')
    """
    if not points:
        raise ValueError("La lista de puntos no puede estar vacía.")
    
    n = len(points)
    if n < 5:
        raise ValueError("La lista de puntos debe tener al menos 5 puntos.")
    
    # Encontrar el punto central
    central_point = central
    
    # Calcular los ángulos para cada punto respecto al punto central
    angles = []
    for key, value in points.items():
        x = value['latitud']
        y = value['longitud']
        angle = np.arctan2(y - central_point[1], x - central_point[0])
        angles.append((angle, (x, y)))
    
    # Dividir los puntos en 5 grupos iguales
    quintile_indices = [n // 5, 2 * n // 5, 3 * n // 5, 4 * n // 5]
    
    # Obtener los ángulos que dividen los grupos
    dividing_angles = [angles[i][0] for i in quintile_indices]
    
    # Formar las recta
    points = return_dictionary_keys(points)
    lines = [(angle, points[index]) for index, angle in enumerate(dividing_angles)]
    
    return central_point, lines

def return_dictionary_keys(dictionary):
    return list(dictionary.keys())


def calculate_angle(p, central_point):
    """
    Calcula el ángulo de un punto respecto al punto central.
    
    :param p: Punto en el formato (x, y)
    :param central_point: Punto central en el formato (cx, cy)
    :return: Ángulo en radianes
    """
    return np.arctan2(p[1] - central_point[1], p[0] - central_point[0])

def divide_points(points, central_point, lines):
    """
    Divide una lista de puntos en 5 grupos según 4 líneas divisoras que parten del punto central.
    
    :param points: Lista de puntos en el formato [(x1, y1), (x2, y2), ...]
    :param central_point: Punto central en el formato (cx, cy)
    :param lines: Lista de líneas en el formato [(angle1, 'line'), (angle2, 'line'), ...]
    :return: Lista de 5 listas de puntos, cada una representando un grupo
    """
    # Calcular los ángulos de las líneas divisoras
    line_angles = lines
    
    # Calcular los ángulos de cada punto respecto al punto central
    points_with_angles = [(p, calculate_angle(p[0], central_point)) for p in points]
    
    # Ordenar los puntos por sus ángulos
    points_with_angles.sort(key=lambda x: x[1])
    
    # Dividir los puntos en 5 grupos según los ángulos de las líneas divisoras
    groups = [[] for _ in range(5)]
    current_group = 0
    for p, angle in points_with_angles:
        # Si el ángulo del punto supera el ángulo de la línea divisoria actual, avanzar al siguiente grupo
        while current_group < 4 and angle > line_angles[0][current_group]:
            current_group += 1
        groups[current_group].append(p)
    
    return groups


def TSP_Algorythm(nodes, mapa):
    '''
    Encuentra el camino más corto desde el punto central hasta todos los puntos de la lista.
    '''
    cost_matrix = makeMatrix(nodes, mapa)

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
    
    px = []
    for i in path:
        px.append(nodes[i][1])
    
    return px, min_cost

    

def makeMatrix(nodes, mapa):
    # Create a matrix of zeros
    matrix = np.zeros((len(nodes), len(nodes)))
    
    # Iterate over each node and its connections
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if j <= i:
                continue
            # Calculate the cost between the two nodes
            
            lat1 = mapa.paradas[node1[1]]['latitud']
            lon1 = mapa.paradas[node1[1]]['longitud']
            lat2 = mapa.paradas[node2[1]]['latitud']
            lon2 = mapa.paradas[node2[1]]['longitud']
            try:
                cost = obtener_tiempo_en_coche([lat1, lon1], [lat2, lon2])
            except:
                cost = 5000
            print(node1[1], node2[1], "Costo:", cost)
            # Update the matrix with the calculated cost
            matrix[i, j] = cost
            matrix[j, i] = cost
    
    return matrix


def Get_Ruta(points):
    '''
    Encuentra el camino más corto desde el punto central hasta todos los puntos de la lista.
    '''


    return 0
 