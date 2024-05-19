import pandas as pd
from datetime import datetime
import calendar
import folium
import random

class Mapa:
    """
    Clase que contiene la información de un mapa

    self.parada: diccionario de diccionarios con formato:
            {codINE: {"municipio": value, "población": num_value, 
                      "bloque": num_bloque, "estancia_minima": value, "lote": value, 'longitud': lon, 'latitud': lat"}

    self.conexiones: diccionario de diccionarios con fromato:
            {
                parada_1 : {primera_conexion_parada_1: coste_1_1, segunda_conexion_parada_1: cost_1_2}
                parada_2 : {primera_conexion_parada_2: coste_2_1, segunda_conexion_parada_1: cost_2_2}
                ....
            }
    """

    def __init__(self):
        print()
        self.paradas = {}
        self.conexiones = {}

    def add_parada(self, codINE, municipio, poblacion, bloque, estancia_minima, lote, lon, lat):
        self.paradas[codINE] = {'municipio': municipio, 'poblacion': poblacion, 'bloque': int(bloque), 'estancia_minima': estancia_minima, 'lote': int(lote), 'longitud': lon, 'latitud': lat}

    def add_conexion(self, conexiones):
        self.conexiones = conexiones
 
    def get_municipiosBloque(self, bloque):
        municipios = {}
        for codINE, parada_info in self.paradas.items():
            if parada_info['bloque'] == bloque:
                municipios[codINE] = parada_info
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
                
def mostrar_agrupacions(lista_diccionario_municipios):
    mapa = folium.Map(location=[40, -3], zoom_start=6)

    # Generar una lista de colores aleatorios para cada grupo
    colores = ['red', 'green', 'purple', 'orange', 'blue', 'gray', 'black', 'pink', 'lightblue']

    # Iterar sobre cada grupo de municipios y asignar un color aleatorio a cada uno
    for idx, municipios in enumerate(lista_diccionario_municipios):
        print(colores[idx])
        print(len(municipios))
        color_grupo = colores[idx]  # Obtener el color para este grupo
        for codINE, info in municipios.items():
            if 'latitud' in info and 'longitud' in info and not pd.isnull(info['longitud']) and not pd.isnull(info['latitud']):
                folium.CircleMarker(
                    location=[info['latitud'], info['longitud']],
                    radius=10,
                    color=color_grupo,
                    fill=True,
                    fill_color=color_grupo,
                    fill_opacity=0.6,
                    popup=f"Municipio: {info['municipio']}<br>Población: {info['poblacion']}<br>Bloque: {info['bloque']}",
                    tooltip=info['municipio']
                ).add_to(mapa)

                folium.Marker(
                    location=[info['latitud'], info['longitud']],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 12px; color: black; background-color: white; border: 1px solid black; padding: 2px;">{info["municipio"]}</div>'
                    )
                ).add_to(mapa)

    mapa.save("mapa_agrupaciones.html")
    print("Mapa guardado como mapa_agrupaciones.html")

def mostrar_rutes(lista_municipios):
    # Inicializar el mapa centrado en una ubicación aproximada de España
    mapa = folium.Map(location=[40, -3], zoom_start=6)

    # Lista para almacenar las coordenadas de los municipios
    coordenadas = []

    for municipio in lista_municipios:
        latitud = municipio['latitud']
        longitud = municipio['longitud']

        # Añadir un marcador para cada municipio
        folium.CircleMarker(
            location=[latitud, longitud],
            radius=10,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"Municipio: {municipio['municipio']}<br>Bloque: {municipio['bloque']}",
            tooltip=municipio['municipio']
        ).add_to(mapa)

        # Añadir un marcador con el nombre del municipio
        folium.Marker(
            location=[latitud, longitud],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: black; background-color: white; border: 1px solid black; padding: 2px;">{municipio["municipio"]}</div>'
            )
        ).add_to(mapa)

        # Añadir las coordenadas a la lista
        coordenadas.append((latitud, longitud))

    # Añadir líneas entre los puntos en el orden en que aparecen en la lista
    folium.PolyLine(coordenadas, color='blue', weight=2.5, opacity=1).add_to(mapa)

    # Guardar el mapa en un archivo HTML
    mapa.save("mapa_rutas.html")
    print("Mapa guardado como mapa_rutas.html")