import time as t
from datetime import datetime
from InfoMapa import Mapa
import os
import math
import copy

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

'''
Este elagoritmo sirve para saber cuál será la ruta dependiendo de que día es del día 1-5
Este algoritmo se inicializará con: Un bloque entero de un lote.
Recivirá:
    - un alista de municipios con sus cordenadas
Devuelve:
    Una lista con cinco listas

'''
def divide_routes(routes):
    linea = find_dividing_lines(points)
    print(linea)
    


def find_dividing_lines(points):
    """
    Encuentra dos rectas (una vertical y una horizontal) que dividan el espacio
    de tal manera que cada lado de cada recta tenga la misma cantidad de puntos.
    
    :param points: Lista de puntos en el formato [municipis..(x,y)]
    :return: Una tupla ((x_mediana, 'vertical'), (y_mediana, 'horizontal'))
    """
    
    # Ordenar puntos por coordenada x
    points_sorted_by_x = sorted(points, key=lambda p: p[0])
    
    # Encontrar la mediana en x
    n = len(points_sorted_by_x)
    if n % 2 == 0:
        x_mediana = (points_sorted_by_x[n//2 - 1][0] + points_sorted_by_x[n//2][0]) / 2
    else:
        x_mediana = points_sorted_by_x[n//2][0]

    # Ordenar puntos por coordenada y
    points_sorted_by_y = sorted(points, key=lambda p: p[1])
    
    # Encontrar la mediana en y
    if n % 2 == 0:
        y_mediana = (points_sorted_by_y[n//2 - 1][1] + points_sorted_by_y[n//2][1]) / 2
    else:
        y_mediana = points_sorted_by_y[n//2][1]

    return [x_mediana, y_mediana]


# Ejemplo de uso
puntos = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
rectas = find_dividing_lines(puntos)
print(rectas)  # Output: ((5.0, 'vertical'), (6.0, 'horizontal'))



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