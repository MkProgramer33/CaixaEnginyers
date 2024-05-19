import requests

def obtener_distancia_en_coche(origen, destino):
    """
    Obtiene la distancia en coche entre dos coordenadas utilizando la API de OSRM.

    Parámetros:
    origen (tuple): Una tupla con las coordenadas de origen (longitud, latitud).
    destino (tuple): Una tupla con las coordenadas de destino (longitud, latitud).

    Devuelve:
    float: La distancia en kilómetros entre las dos coordenadas.
    """
    # Formatear la URL de la solicitud
    url = f"http://router.project-osrm.org/route/v1/driving/{origen[0]},{origen[1]};{destino[0]},{destino[1]}?overview=false"

    # Realizar la solicitud GET
    response = requests.get(url)
    data = response.json()

    # Verificar si la solicitud fue exitosa
    if data['code'] == 'Ok':
        # Extraer la distancia en metros y convertir a kilómetros
        distancia_metros = data['routes'][0]['legs'][0]['distance']
        distancia_kilometros = distancia_metros / 1000
        return distancia_kilometros
    else:
        raise Exception("Error en la solicitud a la API de OSRM.")


"""
para implimentarlo:
    
    # Coordenadas de origen y destino
    origen = (2.15899, 41.38879)
    destino = (-3.70256, 40.4165)
    
    # Obtener la distancia en coche
    try:
        distancia = obtener_distancia_en_coche(origen, destino)
        print(f"La distancia en coche entre las coordenadas es de {distancia:.2f} km.")
    except Exception as e:
        print(str(e))
    
"""


def obtener_tiempo_en_coche(origen, destino):

    """
    Obtiene el tiempo de viaje en coche entre dos coordenadas utilizando la API de OSRM.

    Parámetros:
    origen (tuple): Una tupla con las coordenadas de origen (longitud, latitud).
    destino (tuple): Una tupla con las coordenadas de destino (longitud, latitud).

    Retorna:
    float: El tiempo de viaje en minutos entre las dos coordenadas.
    """
    # Formatear la URL de la solicitud
    url = f"http://router.project-osrm.org/route/v1/driving/{origen[0]},{origen[1]};{destino[0]},{destino[1]}?overview=false"

    # Realizar la solicitud GET
    response = requests.get(url)
    data = response.json()

    # Verificar si la solicitud fue exitosa
    if data['code'] == 'Ok':
        # Extraer la duración en segundos y convertir a minutos
        duracion_segundos = data['routes'][0]['legs'][0]['duration']
        duracion_minutos = duracion_segundos / 60
        return duracion_minutos
    else:
        raise Exception("Error en la solicitud a la API de OSRM.")

"""
# Coordenadas de origen y destino
origen = (2.15899, 41.38879)
destino = (-3.70256, 40.4165)

# Obtener el tiempo de viaje en coche
try:
    tiempo = obtener_tiempo_en_coche(origen, destino)
    print(f"El tiempo de viaje en coche entre las coordenadas es de {tiempo:.2f} minutos.")
except Exception as e:
    print(str(e))
"""
