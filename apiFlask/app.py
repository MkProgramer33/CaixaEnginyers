from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import logging
from logging.handlers import RotatingFileHandler

# Configuración de Flask y MySQL
class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'api_flask'

config = {
    'development': DevelopmentConfig
}

app = Flask(__name__)
CORS(app)

app.config.from_object(config['development'])
conexion = MySQL(app)

# Setup logging
handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)



# /schedule?id_driver
@app.route('/schedule', methods=['GET'])
def schedule():
    id_driver = request.args.get('id_driver')
    if id_driver:
        try:
            schedule = read_schedule(id_driver)
            if schedule != None:
                return jsonify(schedule)
            else:
                return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    return  jsonify({'Error': "expected id_driver"})


def read_schedule(driver_id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM schedule WHERE sch_assigned_driver_id = '{0}' AND sch_completed = 0".format(driver_id)
        cursor.execute(sql)
        datos = cursor.fetchall()  # Usamos fetchall en lugar de fetchone para obtener todas las filas
        if datos:
            # Calcular el total de schedules encontrados
            total_schedules = len(datos)
            # Obtener los nombres de las columnas desde la descripción del cursor
            column_names = [desc[0] for desc in cursor.description]
            # Crear una lista de diccionarios con los datos de cada schedule
            schedules = [{column_names[i]: row[i] for i in range(len(column_names))} for row in datos]
            # Construir el diccionario final con la clave "total" y la lista de schedules
            return {"total": total_schedules, "info": schedules}
        else:
            return None
    except Exception as ex:
        raise ex




# /routes?id_schedule
@app.route('/municipes', methods=['GET'])
def municipes():
    id_schedule = "1"
    if id_schedule:
        try:
            routes = read_municipes()
            if routes != None:
                return jsonify(routes)
            else:
                return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    return  jsonify({'Error': "error"})


def read_municipes():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM municipes"
        cursor.execute(sql)
        datos = cursor.fetchall()  # Usamos fetchall en lugar de fetchone para obtener todas las filas
        if datos:
            # Calcular el total de schedules encontrados
            total_routes = len(datos)
            # Obtener los nombres de las columnas desde la descripción del cursor
            column_names = [desc[0] for desc in cursor.description]
            # Crear una lista de diccionarios con los datos de cada schedule
            routes = [{column_names[i]: row[i] for i in range(len(column_names))} for row in datos]
            # Construir el diccionario final con la clave "total" y la lista de schedules
            return {"total": total_routes, "info": routes}
        else:
            return None
    except Exception as ex:
        raise ex




@app.route('/schedule/complete', methods=['PUT'])
def complete_schedule():
    
    id_schedule = request.args.get('id_schedule')

    try:
        curso = 1
        if curso != None:
            cursor = conexion.connection.cursor()
            sql = "UPDATE schedule SET sch_completed = 1 WHERE sch_id = '{0}'".format(id_schedule)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de actualización.
            return jsonify({'mensaje': "schedule actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
  


@app.route('/route/start', methods=['PUT'])
def start_route():
    
    id_route = request.args.get('id_route')

    # request.json['nombre']
    realStart = request.json['realstart']
    
    try:
        cursor = conexion.connection.cursor()
        sql = """UPDATE routes SET route_selected = 1, route_selected = 1, route_real_start_time = '{0}'
        WHERE route_id = '{1}'""".format(realStart, id_route)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de actualización.
        return jsonify({'mensaje': "Curso actualizado.", 'exito': True})
    
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/route/complete', methods=['PUT'])
def complete_route():
    
    id_route = request.args.get('id_route')

    # request.json['nombre']
    realStanceDuration = request.json['realstance']
    realExtraDuration = request.json['realextra']
    
    try:
   
        cursor = conexion.connection.cursor()
        sql = """UPDATE routes SET route_selected = 0, route_completed = 1, route_real_stance_duration = '{0}', 
        route_real_extra_time = '{1}' WHERE route_id = '{2}'""".format(realStanceDuration, realExtraDuration, id_route)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de actualización.
        return jsonify({'mensaje': "Curso actualizado.", 'exito': True})
    
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
  
@app.route('/route/arrived', methods=['PUT'])
def arrived_route():
    
    id_route = request.args.get('id_route')

    # request.json['nombre']
    routeRealDuration = request.json['realroute']
    
    try:
   
        cursor = conexion.connection.cursor()
        sql = """UPDATE routes SET route_real_onroute_duration = '{0}'
        WHERE route_id = '{1}'""".format(routeRealDuration, id_route)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de actualización.
        return jsonify({'mensaje': "Curso actualizado.", 'exito': True})
    
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
  




@app.route('/prueba', methods=['PUT'])
def cargar_rutas(route_origen_id, route_destination_id, route_planned_start_time, route_planned_finish_time, route_planned_onroute_duration, route_planned_stance_duration, route_planned_extra_time, route_planned_required_time):
    cursor = conexion.connection.cursor()
    sql = """INSERT INTO routes (route_origen_id, route_destination_id, route_planned_start_time, route_planned_finish_time, route_planned_onroute_duration, route_planned_stance_duration, route_planned_extra_time, route_planned_required_time) 
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')""".format(12, 12, '2024-05-18 22:50:11', '2024-05-18 22:50:11', 60, 60, 60, 60)        
    cursor.execute(sql)
    conexion.connection.commit()  # Confirma la acción de inserción.
    return jsonify({'mensaje': "Ruta insertada correctamente.", 'exito': True})


    # VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')""".format(route_origen_id, route_destination_id, route_planned_start_time, route_planned_finish_time, route_planned_onroute_duration, route_planned_stance_duration, route_planned_extra_time, route_planned_required_time)        



















# /routes?id_schedule
@app.route('/routes', methods=['GET'])
def routes():
    id_schedule = request.args.get('id_schedule')
    if id_schedule:
        try:
            routes = read_routes(id_schedule)
            if routes != None:
                return jsonify(routes)
            else:
                return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    return  jsonify({'Error': "expected id_schedule"})


def read_routes(id_schedule):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM routes WHERE route_sch_id = '{0}' AND route_completed = 0".format(id_schedule)
        cursor.execute(sql)
        datos = cursor.fetchall()  # Usamos fetchall en lugar de fetchone para obtener todas las filas
        if datos:
            # Calcular el total de schedules encontrados
            total_routes = len(datos)
            # Obtener los nombres de las columnas desde la descripción del cursor
            column_names = [desc[0] for desc in cursor.description]
            # Crear una lista de diccionarios con los datos de cada schedule
            routes = [{column_names[i]: row[i] for i in range(len(column_names))} for row in datos]
            # Construir el diccionario final con la clave "total" y la lista de schedules
            return {"total": total_routes, "info": routes}
        else:
            return None
    except Exception as ex:
        raise ex


# /driver?id_driver
# @cross_origin(supports_credentials=True)
@app.route('/driver', methods=['GET'])
def driverData():
    id_driver = request.args.get('id_driver')
    if id_driver:
        try:
            schedule = read_driverData(id_driver)
            if schedule != None:
                return jsonify(schedule)
            else:
                return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    return  jsonify({'Error': "expected id_driver"})


def read_driverData(driver_id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM drivers WHERE driver_id = '{0}'".format(driver_id)
        cursor.execute(sql)
        datos = cursor.fetchall()  # Usamos fetchall en lugar de fetchone para obtener todas las filas
        if datos:
            # Calcular el total de schedules encontrados
            total_schedules = len(datos)
            # Obtener los nombres de las columnas desde la descripción del cursor
            column_names = [desc[0] for desc in cursor.description]
            # Crear una lista de diccionarios con los datos de cada schedule
            schedules = [{column_names[i]: row[i] for i in range(len(column_names))} for row in datos]
            # Construir el diccionario final con la clave "total" y la lista de schedules
            return {"total": total_schedules, "info": schedules}
        else:
            return None
    except Exception as ex:
        raise ex









# @app.route('/rutas/all', methods=['GET'])
# def leer_curso():
#     try:
#         id_driver = request.args.get('id_driver')
#         return id_driver
        
#         curso = leer_curso_bd(driver_name)
#         if curso != None:
#             return jsonify({'curso': curso, 'mensaje': "Curso encontrado.", 'exito': True})
#         else:
#             return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
#     except Exception as ex:
#         return jsonify({'mensaje': "Error", 'exito': False})







# @app.route('/rutas/<driver_name>', methods=['GET'])
# def leer_curso(driver_name):
#     try:
#         user = request.args.get('user')
#         return user
#         curso = leer_curso_bd(driver_name)
#         if curso != None:
#             return jsonify({'curso': curso, 'mensaje': "Curso encontrado.", 'exito': True})
#         else:
#             return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
#     except Exception as ex:
#         return jsonify({'mensaje': "Error", 'exito': False})



@app.route('/cursos', methods=['POST'])
def registrar_curso():
    # print(request.json)
    if (validar_codigo(request.json['codigo']) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos'])):
        try:
            curso = leer_curso_bd(request.json['codigo'])
            if curso != None:
                return jsonify({'mensaje': "Código ya existe, no se puede duplicar.", 'exito': False})
            else:
                cursor = conexion.connection.cursor()
                sql = """INSERT INTO curso (codigo, nombre, creditos) 
                VALUES ('{0}', '{1}', {2})""".format(request.json['codigo'],
                                                     request.json['nombre'], request.json['creditos'])
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de inserción.
                return jsonify({'mensaje': "Curso registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    if (validar_codigo(codigo) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos'])):
        try:
            curso = leer_curso_bd(codigo)
            if curso != None:
                cursor = conexion.connection.cursor()
                sql = """UPDATE curso SET nombre = '{0}', creditos = {1} 
                WHERE codigo = '{2}'""".format(request.json['nombre'], request.json['creditos'], codigo)
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "Curso actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        curso = leer_curso_bd(codigo)
        if curso != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Curso eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
