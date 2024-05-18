import pandas as pd

class Mapa:
    """
    Clase que contiene la información de un mapa

    self.parada: diccionario de diccionarios con formato:
            {codINE: {"nombre": value, "municipio": value, "x": coord_x, "y": coord_y, "población": num_value, 
                      "bloque": num_bloque, "estancia_minima": value, "lote": value}

    self.conexiones: diccionario de diccionarios con fromato:
            {
                parada_1 : {primera_conexion_parada_1: coste_1_1, segunda_conexion_parada_1: cost_1_2}
                parada_2 : {primera_conexion_parada_2: coste_2_1, segunda_conexion_parada_1: cost_2_2}
                ....
            }
    """

    def __init__(self):
        self.paradas = {}
        self.conexiones = {}

    def add_parada(self, codINE, nombre, municipio, x, y, poblacion, bloque, estancia_minima, lote):
        self.parada[codINE] = {'nombre': nombre, 'municipio': municipio, 'x': x, 'y': y, 'poblacion': poblacion, 'bloque': int(bloque), 
                               'estancia_minima': int(estancia_minima),  'lote': int(lote) }

    def add_conexion(self, conexiones):
        self.conexiones = conexiones



class Route:
    """
    Clase que tiene la información de la ruta desde una parada de inicio hasta una de fin.
    
    """

    def __init__(self, route):
        if type(route) is list:
            self.route = route
        else:
            self.route = [route]

        self.head = self.route[0]
        self.last = self.route[-1]
        if len(self.route) >= 2:
            self.penultimate = self.route[-2]
        # Real cost
        self.g = 0
        # Heuristic cost
        self.h = 0
        # Combination of the two
        self.f = 0

    def __eq__(self, other):
        if other is not None:
            return self.route == other.route

    def update_h(self, h):
        self.h = h

    def update_g(self, g):
        self.g += g

    def update_f(self):
        self.f = self.g + self.h

    def add_route(self, children):
        # Adding a new station to the route list
        self.route.append(children)
        self.penultimate = self.route[-2]
        self.last = self.route[-1]


    import pandas as pd
from datetime import datetime
 

class Mapa:
    """
    Clase que contiene la información de un mapa

    self.parada: diccionario de diccionarios con formato:
            {codINE: {"municipio": value, "población": num_value, 
                      "bloque": num_bloque, "estancia_minima": value, "lote": value}

    self.conexiones: diccionario de diccionarios con fromato:
            {
                parada_1 : {primera_conexion_parada_1: coste_1_1, segunda_conexion_parada_1: cost_1_2}
                parada_2 : {primera_conexion_parada_2: coste_2_1, segunda_conexion_parada_1: cost_2_2}
                ....
            }
    """

    def __init__(self):
        self.paradas = {}
        self.conexiones = {}

    def add_parada(self, codINE, municipio, poblacion, bloque, estancia_minima, lote, lon, lat):
        self.paradas[codINE] = {'municipio': municipio, 'poblacion': poblacion, 'bloque': int(bloque), 'estancia_minima': estancia_minima, 'lote': int(lote), 'longitud': lon, 'latitud': lat}

    def add_conexion(self, conexiones):
        self.conexiones = conexiones
    
    # Devuelve el número de bloque según el dia en el que esté.
    def get_bloque(self, fecha_str):
        pass



class Route:
    """
    Clase que tiene la información de la ruta desde una parada de inicio hasta una de fin.
    
    """

    def __init__(self, route):
        if type(route) is list:
            self.route = route
        else:
            self.route = [route]

        self.head = self.route[0]
        self.last = self.route[-1]
        if len(self.route) >= 2:
            self.penultimate = self.route[-2]
        # Real cost
        self.g = 0
        # Heuristic cost
        self.h = 0
        # Combination of the two
        self.f = 0

    def __eq__(self, other):
        if other is not None:
            return self.route == other.route

    def update_h(self, h):
        self.h = h

    def update_g(self, g):
        self.g += g

    def update_f(self):
        self.f = self.g + self.h

    def add_route(self, children):
        # Adding a new station to the route list
        self.route.append(children)
        self.penultimate = self.route[-2]
        self.last = self.route[-1]


    
def load(fitxer, mapa):
        
    # leemos la info del excel
    data = pd.read_excel(fitxer)
    
    required_columns = ['codINE', 'Municipi', 'Pob.', 'BLOC', 'Estancia Minima', 'LOTE', 'LONG', 'LAT']
    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Falta la columna requerida: {column}")
    
    # codINE, municipio, x, y, poblacion, bloque, estancia_minima, lote
    for i, codigo in enumerate(data['codINE']):
        mapa.add_parada(codigo, 
                        data['Municipi'][i], 
                        data['Pob.'][i], 
                        data['BLOC'][i], 
                        data['Estancia Minima'][i], 
                        data['LOTE'][i],
                        data['LONG'][i],
                        data['LAT'][i])

"""
para implimentar load:
    
    mapa = Mapa()
    load('DatosMunicipios.xlsx', mapa)
    print(mapa.paradas)
    
"""


