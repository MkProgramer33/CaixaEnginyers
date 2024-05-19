from datetime import datetime, timedelta

def añadir_minutos(fecha_str, minutos):
    formato_fecha = "%a, %d %b %Y %H:%M:%S GMT"
  
    # conversión de la fecha a objeto datetime
    fecha = datetime.strptime(fecha_str, formato_fecha)
      
    nueva_fecha = fecha + timedelta(minutes=minutos) #añadimos minutos
      
    # conversión al formato original ("%a, %d %b %Y %H:%M:%S GMT")
    nueva_fecha_str = nueva_fecha.strftime(formato_fecha)
      
    return nueva_fecha_str


"""
Para implementar añadir_minutos:
    
    fecha_original_str = "Sat, 18 May 2024 22:50:11 GMT"
    minutos_a_añadir = 30
    
    nueva_fecha_str = añadir_minutos(fecha_original_str, minutos_a_añadir)
    print("Fecha original:", fecha_original_str)
    print("Nueva fecha:", nueva_fecha_str)
"""


def calcular_diferencia_en_minutos(fecha1, fecha2):
    formato_fecha = "%a, %d %b %Y %H:%M:%S %Z"
    
    # Convertir las cadenas a objetos datetime
    datetime1 = datetime.strptime(fecha1, formato_fecha)
    datetime2 = datetime.strptime(fecha2, formato_fecha)
    
    # Calcular la diferencia
    diferencia = datetime1 - datetime2
    
    # Obtener la diferencia en minutos
    diferencia_en_minutos = diferencia.total_seconds() / 60
    
    return diferencia_en_minutos


fecha2 = "Sat, 18 May 2024 22:50:11 GMT"
fecha1 = "Sat, 18 May 2024 22:30:11 GMT"

diferencia_en_minutos = calcular_diferencia_en_minutos(fecha1, fecha2)
print(f"La diferencia es de {diferencia_en_minutos} minutos.")