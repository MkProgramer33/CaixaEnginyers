import time as t
from datetime import datetime
from InfoMapa import Mapa
from InfoMapa import load
import os
import math
import copy
import numpy as np

'''
# Get the current date and time
now = datetime.now()

# Extract the time components
current_time = now.time()
hour = current_time.hour
minute = current_time.minute
second = current_time.second

# Extract the date components
current_date = now.date()
day = current_date.day
month = current_date.month
year = current_date.year

print(f"Current time: {hour}:{minute}:{second}")
print(f"Current date: {day}/{month}/{year}")
'''


# Algorithm for finding the shortest route

def main():
    mapa = Mapa()
    load("DatosMunicipios.xlsx", mapa)
    points = []
    for key, value in mapa.paradas.items():
        points.append((value['latitud'], value['longitud']))
    central, lines = find_dividing_lines(mapa.paradas)
    grupo = divide_points(points, central, lines)


    for i, grupo in enumerate(grupo):
        print(f"Grupo {i + 1}: {grupo}")
    
'''
Función que te devuelve el centroide de este lugar en función de que cordenadas tiene
'''

def find_central_point(points):

    return [2.8022296,41.8954981]

'''
Este elagoritmo sirve para saber cuál será la ruta dependiendo de que día es del día 1-5
Este algoritmo se inicializará con: Un bloque entero de un lote.
Recivirá:
    - un alista de municipios con sus cordenadas
Devuelve:
    Una lista con cinco listas

'''
def find_dividing_lines(points):
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
    central_point = find_central_point(points)
    
    # Calcular los ángulos para cada punto respecto al punto central
    angles = []
    for key, value in points.items():
        x = value['latitud']
        y = value['longitud']
        angle = np.arctan2(y - central_point[1], x - central_point[0])
        angles.append((angle, (x, y)))
    
    # Ordenar los puntos según sus ángulos
    angles.sort()
    
    # Dividir los puntos en 5 grupos iguales
    quintile_indices = [n // 5, 2 * n // 5, 3 * n // 5, 4 * n // 5]
    
    # Obtener los ángulos que dividen los grupos
    dividing_angles = [angles[i][0] for i in quintile_indices]
    
    # Formar las rectas
    lines = [(angle, 'line') for angle in dividing_angles]
    
    return central_point, lines



import numpy as np

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
    line_angles = [line[0] for line in lines]
    
    # Calcular los ángulos de cada punto respecto al punto central
    points_with_angles = [(p, calculate_angle(p, central_point)) for p in points]
    
    # Ordenar los puntos por sus ángulos
    points_with_angles.sort(key=lambda x: x[1])
    
    # Dividir los puntos en 5 grupos según los ángulos de las líneas divisoras
    groups = [[] for _ in range(5)]
    current_group = 0
    for p, angle in points_with_angles:
        # Si el ángulo del punto supera el ángulo de la línea divisoria actual, avanzar al siguiente grupo
        while current_group < 4 and angle > line_angles[current_group]:
            current_group += 1
        groups[current_group].append(p)
    
    return groups






def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    expanded_paths = []
    for station_id in map.connections[path.last]:
        new_path = Path(path.route + [station_id])
        new_path.f = path.f
        new_path.g = path.g
        new_path.h = path.h
        expanded_paths.append(new_path)
    return expanded_paths

    pass


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    path_list_without_cycles = []
    for path in path_list:
        stations_set = set(path.route)
        if len(stations_set) == len(path.route):
            path_list_without_cycles.append(path)
    
    return path_list_without_cycles

    pass


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    list_of_path.pop(0)
    return expand_paths + list_of_path

    pass


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    paths_to_visit = [Path(origin_id)]

    while paths_to_visit:
        current_path = paths_to_visit[0]
        if current_path.last == destination_id:
            return current_path
        else:
            expanded_paths = remove_cycles(expand(current_path, map))
            paths_to_visit = insert_depth_first_search(expanded_paths, paths_to_visit)

    pass


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    list_of_path.pop(0)
    return list_of_path + expand_paths

    pass


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    paths_to_visit = [Path(origin_id)]

    while paths_to_visit:
        current_path = paths_to_visit[0]
        if current_path.last == destination_id:
            return current_path
        else:
            expanded_paths = remove_cycles(expand(current_path, map))
            paths_to_visit = insert_breadth_first_search(expanded_paths, paths_to_visit)
        
    pass


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    
    for path in expand_paths:
        
        last_stop = path.penultimate
        next_stop = path.last
        last_line = map.stations[last_stop]['line']
        next_line = map.stations[next_stop]['line']

        if type_preference == 0:
            path.update_g(1)
        elif type_preference == 1:
            cost = map.connections[last_stop][next_stop]
            path.update_g(cost)
        elif type_preference == 2:
            if next_line == last_line:
                velocity = map.velocity[last_line]
                time = map.connections[last_stop][next_stop]
                cost = velocity * time
                path.update_g(cost)
        elif type_preference == 3:
            if last_line == next_line:
                path.update_g(0)
            else:
                path.update_g(1)

    return expand_paths
    
    pass


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    list_of_path.extend(expand_paths)

    list_of_path.sort(key=lambda path: path.g)
    
    return list_of_path

    pass


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """ 
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    

    paths_to_visit = [Path(origin_id)]

    while paths_to_visit and paths_to_visit[0].last != destination_id:
        current_path = paths_to_visit.pop(0)
        expanded_paths = remove_cycles(expand(current_path, map))
        expanded_paths = calculate_cost(expanded_paths, map, type_preference)
        paths_to_visit = insert_cost(expanded_paths, paths_to_visit)

    if len(paths_to_visit) != 0:
        return paths_to_visit[0]    
    pass


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    
    for path in expand_paths:
        if type_preference == 0:
            if destination_id == path.last:
                heuristic = 0
            else:
                heuristic = 1
        elif type_preference == 1:
            destination_coordinates = (map.stations[destination_id]['x'], map.stations[destination_id]['y'])
            actual_coordinates = (map.stations[path.last]['x'], map.stations[path.last]['y'])
            distance = euclidean_dist(actual_coordinates, destination_coordinates)
            max_velocity = max(map.velocity.values())
            heuristic = distance / max_velocity
        elif type_preference == 2:
            destination_coordinates = (map.stations[destination_id]['x'], map.stations[destination_id]['y'])
            actual_coordinates = (map.stations[path.last]['x'], map.stations[path.last]['y'])
            heuristic = euclidean_dist(actual_coordinates, destination_coordinates)
        elif type_preference == 3:
            heuristic = 1 if map.stations[path.last]['line'] != map.stations[destination_id]['line'] else 0

        path.update_h(heuristic)

    return expand_paths

    pass


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    
    for path in expand_paths:
        path.update_f()
    return expand_paths

    pass


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    for path in expand_paths:
        if path.last in visited_stations_cost:
            if visited_stations_cost[path.last] <= path.g:
                expand_paths.remove(path)
            else:
                visited_stations_cost[path.last] = path.g
                list_of_path = [candidate_path for candidate_path in list_of_path if candidate_path.last != path.last]
        else:
            visited_stations_cost[path.last] = path.g

    return expand_paths, list_of_path, visited_stations_cost

    pass


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    
    list_of_path.extend(expand_paths)
    list_of_path.sort(key=lambda path: path.f)
    
    return list_of_path

    pass


def distance_to_stations(coord, map):
    """
        From coordinates, it computes the distance to all stations in map.
        Format of the parameter is:
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    distances = {}

    for station_id, station_info in map.stations.items():
        station_coord = [station_info['x'], station_info['y']]
        distance = euclidean_dist(coord, station_coord)
        distances[station_id] = distance

    return distances

    pass


def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    paths_to_visit = [Path([origin_id])]
    visited_stations_cost = {}
    
    while paths_to_visit:
        current_path = paths_to_visit.pop(0)
        
        if current_path.last == destination_id:
            return current_path
        
        expanded_paths = remove_cycles(expand(current_path, map))
        expanded_paths = calculate_cost(expanded_paths, map, type_preference)
        expanded_paths = calculate_heuristics(expanded_paths, map, destination_id, type_preference)
        expanded_paths = update_f(expanded_paths)
        expanded_paths, paths_to_visit, visited_stations_cost = remove_redundant_paths(expanded_paths, paths_to_visit, visited_stations_cost)
        paths_to_visit = insert_cost_f(expanded_paths, paths_to_visit)
    
    if (paths_to_visit):
        return paths_to_visit[0]

    pass


def Astar_improved(origin_coord, destination_coord, map):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
            destination_coord (list): Two REAL values, which refer to the coordinates of the final position
            map (object of Map class): All the map information

        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
    """
    WALKING_SPEED = 5
    
    minimum_path = []
    minimum_time = euclidean_dist(origin_coord, destination_coord) / WALKING_SPEED
        
    origin_to_stations_distances = distance_to_stations(origin_coord, map)
    destination_to_stations_distances = distance_to_stations(destination_coord, map)
    
    for origin_station_id in map.stations:
        for destination_station_id in map.stations:
            if origin_station_id != destination_station_id:
                path = Astar(origin_station_id, destination_station_id, map, 1)
                travel_time = path.f
                total_time = (origin_to_stations_distances[path.head] / WALKING_SPEED + travel_time + destination_to_stations_distances[path.last] / WALKING_SPEED)
                if total_time < minimum_time:
                    minimum_path = path.route
                    minimum_time = total_time
    
    final_path = Path([0])
    final_path.f = minimum_time
    for station in minimum_path:
        final_path.add_route(station)
    final_path.add_route(-1)
    
    return final_path



  


# Call the main function
if __name__ == "__main__":
    main()