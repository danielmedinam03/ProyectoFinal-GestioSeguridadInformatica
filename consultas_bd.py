import decimal
import json
from mysql.connector import Error


#Funcion para hacer consultas tipo select a la bd
def execute_select_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()  
        return result
    except Error as e:
        print(f"Error seleccionando: error '{e}' occurred")
        return None


def consulta_tipos_activos(connection):
    lista = ['Seleccione un tipo de activo...']

    query_tipo_activo = f"SELECT tp.tipo_activo_id, tp.nombre FROM tipo_activo AS tp"
    result_tipo_activo = execute_select_query(connection,query_tipo_activo)
    
    return {nombre: id for id, nombre in result_tipo_activo}

def consulta_tipo_amenaza(connection):

    query_amenazas = f"SELECT a.tipo_amenaza_id, a.nombre FROM tipo_amenaza AS a"
    result_amenazas = execute_select_query(connection,query_amenazas)
    data = {nombre: id for id, nombre in result_amenazas}
    return data

def consulta_amenaza(connection, amenazas):

    lista = []

    for item in amenazas:
        query_tipo_amenaza = f"SELECT * FROM amenaza ta JOIN tipo_amenaza a ON  ta.tipo_amenaza_id = a.tipo_amenaza_id WHERE a.nombre = '{item}';"
        result_tipo_amenaza = execute_select_query(connection,query_tipo_amenaza)
        for item in result_tipo_amenaza:
            lista.append(item[1])

    return lista

def consulta_escalar_valor(connection):

    query_escalar_valor = f"SELECT es.escala_valor_id, es.nombre FROM escala_valor AS es"
    result_escalar_valor = execute_select_query(connection,query_escalar_valor)
    
    return {nombre: id for id, nombre in result_escalar_valor}

def consulta_valor_escala_valor(connection,id):
    query = f"SELECT es.valor FROM escala_valor AS es WHERE escala_valor_id = {id}"
    result_escalar_valor = execute_select_query(connection,query)
    return result_escalar_valor[0][0]


def consulta_probabilidad(conexion):
    query = f"SELECT * FROM valoracion_amenazas"
    result_query = execute_select_query(conexion, query)
    # Convertir cada tupla en un diccionario
    column_names = ['id', 'opciones', 'probabilidad', 'criterio']
    result_dict = [dict(zip(column_names, row)) for row in result_query]
    
    # Función para manejar los objetos Decimal
    def handle_decimal(o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

    # Convertir la lista de diccionarios en una cadena JSON
    result_json = json.dumps(result_dict, default=handle_decimal)
    return result_json

def opciones_probabilidad(json_probabilidad):
    # Convertir la cadena JSON de nuevo en una lista de diccionarios
    result_dict = json.loads(json_probabilidad)

    # Extraer los IDs de cada elemento en el resultado
    opciones = [item['opciones'] for item in result_dict]

    return opciones

def consulta_id_probabilidad(conexion, opcion):
    
    query = f"SELECT v.valoracion_amenazas_id FROM valoracion_amenazas AS v WHERE opciones = '{opcion}'"
    result_query = execute_select_query(conexion, query)
    return result_query[0][0]

def consulta_valor_probabilidad(connection, nombre):
    query = f"SELECT v.probabilidad FROM valoracion_amenazas AS v WHERE opciones = '{nombre}'"
    result_probabilidad = execute_select_query(connection, query)
    return result_probabilidad[0][0]

def consulta_tipo_salvaguarda(connection):
    query = f"SELECT * FROM tipo_salvaguarda"
    result = execute_select_query(connection,query)
    data = {nombre: id for id, nombre in result}
    return data

def consulta_salvaguarda(connection, tipo_salvaguarda_id):
    query = f"SELECT s.salvaguarda_id, s.nombre FROM salvaguarda AS s WHERE tipo_salvaguarda_id = {tipo_salvaguarda_id}"
    result = execute_select_query(connection, query)
    data = {nombre: id for id, nombre in result}
    return data

def consulta_valoracion_salvaguarda(connection):
    query = f"SELECT v.valoracion_salvaguarda_id, v.nivel FROM valoracion_salvaguarda AS v"
    result_valoracion = execute_select_query(connection, query)
    data = {nombre: id for id, nombre in result_valoracion}
    return data

def consulta_factor_valoracion_salvaguarda(connection, valoracion_salvaguarda_id):
    query = f"SELECT factor FROM valoracion_salvaguarda WHERE valoracion_salvaguarda_id = {valoracion_salvaguarda_id}"
    result = execute_select_query(connection, query)
    return result[0][0]

def consulta_id_amenaza(conexion, nombre_amenaza):
    
    query = f"SELECT a.amenaza_id FROM amenaza AS a WHERE nombre = '{nombre_amenaza}'"
    result_query = execute_select_query(conexion, query)
    return result_query[0][0]

def consulta_resumen_activo_amenaza(connection):
    query = f"""Select aa.activo_amenaza_id, aa.valoracion_amenaza_id, 
                raa.impacto_potencial, raa.impacto_residual from activo_amenaza AS aa
                inner join resumen_activo_amenaza AS raa ON aa.activo_amenaza_id = raa.activo_amenaza_id"""
    result = execute_select_query(connection, query)
    return result
