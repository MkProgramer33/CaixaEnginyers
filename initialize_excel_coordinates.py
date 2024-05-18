import pandas as pd
from geopy.geocoders import Nominatim
import time

# Leer el archivo Excel
df = pd.read_excel('./DatosMunicipios.xlsx')

# Inicializar el geolocalizador
geolocator = Nominatim(user_agent="Pau")

# Función para obtener la latitud y longitud
def obtener_coordenadas(municipi):
    try:
        location = geolocator.geocode(municipi)
        if location:
            return location.longitude, location.latitude
        else:
            return None, None
    except:
        return None, None

# Iterar sobre los municipios y obtener coordenadas
longitudes = []
latitudes = []
for municipi in df['Municipi']:
    lon, lat = obtener_coordenadas(municipi)
    longitudes.append(lon)
    latitudes.append(lat)
    time.sleep(1)  # Esperar 1 segundo entre solicitudes para no sobrecargar el servicio

# Añadir las coordenadas al DataFrame
df['LONG'] = longitudes
df['LAT'] = latitudes

# Guardar el archivo modificado
df.to_excel('DatosMunicipios1.xlsx', index=False)
