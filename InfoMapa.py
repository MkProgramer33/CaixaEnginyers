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
        
        # diccionario para traducir los días de la semana del inglés al español
        dias_semana = {
            0: 'Lunes',
            1: 'Martes',
            2: 'Miércoles',
            3: 'Jueves',
            4: 'Viernes',
            5: 'Sábado',
            6: 'Domingo'
        }
        
        # bloques de servicio por rango de días laborables
        bloques_servicio = {
            range(1, 6): 'Bloc 1',
            range(6, 11): 'Bloc 2',
            range(11, 16): 'Bloc 3',
            range(16, 21): 'Bloc 4'
        }
        
        # convertir la cadena de fecha en un objeto datetime
        fecha = datetime.strptime(fecha_str, '%d/%m/%Y')

        dia_semana = fecha.weekday()
        dia = dias_semana[dia_semana]
        
        
        # Verificar si el día es laborable (lunes a viernes)
        if dia_semana > 4:
            return f"La fecha {fecha_str} corresponde a: {dias_semana[dia_semana]}, que no es un día laborable."
        
        parada={}
        parada = self.paradas.get(codINE)
        if parada:
            return parada['bloque']
        else:
            raise ValueError(f"No se encontró una parada con codINE: {codINE}")
            
    
    
        # Verificar si el día es laborable (lunes a viernes)
        if dia_semana > 4:
            return f"La fecha {fecha_str} corresponde a: {dias_semana[dia_semana]}, que no es un día laborable."
    
        # Calcular el número de días laborables desde el inicio del mes
        dia_mes = fecha.day
        contador_dias_laborables = 0
        for dia in range(1, dia_mes + 1):
            dia_actual = datetime(fecha.year, fecha.month, dia)
            if dia_actual.weekday() < 5:  # Lunes a viernes son días laborables
                contador_dias_laborables += 1
    
        # Determinar el bloque de servicio correspondiente
        for rango, bloque in bloques_servicio.items():
            if contador_dias_laborables in rango:
                return f"La fecha {fecha_str} corresponde a: {dias_semana[dia_semana]} y el bloque de servicio es: {bloque}"
    
        return "No se pudo determinar el bloque de servicio."
            
   

# Ejemplo de uso
fecha1 = '18/05/2024'  # Reemplaza con la fecha que desees
dia_semana = get_bloque(fecha)
print(f"La fecha {fecha} corresponde a: {dia_semana}")



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
    
    required_columns = ['codINE', 'Municipi', 'Pob.', 'BLOC', 'Estancia Minima', 'LOTE']
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

"""
para implimentarlo get_bloque:
    
    mapa=Mapa()
    codINE = '8242'
    load('DatosMunicipios.xlsx', mapa)
    bloque = mapa.get_bloque(codINE)
    print(f"El número de bloque para codINE {codINE} es: {bloque}")
    
"""
