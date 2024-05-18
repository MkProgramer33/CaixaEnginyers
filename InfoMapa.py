import pandas as pd
from datetime import datetime
import calendar
 

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
 
    def get_municipiosBloque(self, bloque):
        municipios = []  # lista para almacenar los municipios correspondientes al bloque
        for parada_info in self.paradas.values():
            if parada_info['bloque'] == bloque:
                municipios.append(parada_info['municipio'])
        return municipios



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

# devuelve el número de bloque según el dia en el que esté.
def get_bloque(mapa, fecha_str):

    # convertimos la cadena de fecha en un objeto datetime
    fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
    mes = fecha.month
    año = fecha.year
    contador=0
    contador_dias_laborables=0
    bloque=1
    num_dias_mes = calendar.monthrange(año, mes)[1]
    
    # recorre todos los días del mes
    for dia in range(1, num_dias_mes + 1):
        dia_actual = datetime(año, mes, dia)
        if dia_actual.weekday() < 5:  # lunes a viernes son días laborables
            contador_dias_laborables=0
            contador=contador+1
            if contador<5:
                if dia == fecha.day:
                    return bloque
            else:
                if contador_dias_laborables<=20:
                    bloque=bloque+1
                    contador=0
                else:
                    bloque=4
                

"""
para implimentar get_bloque:
    
    mapa = Mapa()
    fecha_str='15/05/2024'
    bloque=get_bloque(mapa, fecha_str)
    print(bloque)
    
"""


# devuelve la longitud y latitud de una parada a partir de su código INE.
def get_lon_lat(mapa, codINE):

    if codINE in dict(mapa.paradas):
        return (mapa.paradas[codINE]['longitud'], mapa.paradas[codINE]['latitud'])    
    else:
         return None
     

mapa = Mapa()
codINE = str('43003')
load('DatosMunicipios.xlsx', mapa)
lon_lat = get_lon_lat(mapa, codINE)
print(f"Coordenadas para codINE {codINE}: {lon_lat}")

