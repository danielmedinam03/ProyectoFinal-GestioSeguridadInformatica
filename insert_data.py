from mysql.connector import Error

def construccion_query_insert_activo(nombre_activo, tipo_activo):
    query = f"""
    INSERT INTO activo (nombre, tipo_activo_id)
    VALUES ('{nombre_activo}', {tipo_activo});
    """
    return query

def construccion_query_activo_amenaza(activo_id, amenaza_id, valoracion_amenaza_id):
    query = f"""
    INSERT INTO activo_amenaza (activo_id, amenaza_id, valoracion_amenaza_id)
    VALUES ('{activo_id}', '{amenaza_id}', '{valoracion_amenaza_id}');
    """
    return query

def construccion_query_activo_escala_valor(detalle_valor_id,escala_valor_id,activo_amenaza_id):
    query = f"""
    INSERT INTO activo_escala_valor (detalle_valor_id, escala_valor_id, activo_amenaza_id)
    VALUES ('{detalle_valor_id}', '{escala_valor_id}', '{activo_amenaza_id}');
    """
    return query

def construccion_query_insert_activo_salvaguarda(salvaguarda, valoracion_salvaguarda,activo_amenaza_id):
    query = f"""
    INSERT INTO activo_salvaguarda (salvaguarda_id, valoracion_salvaguarda_id, activo_amenaza_id)
    VALUES ('{salvaguarda}','{valoracion_salvaguarda}', '{activo_amenaza_id}');
    """
    return query

#Ejecutar esta funcion para insertar todos los registros
def construccion_query_insert_transaccion(conexion,diccionario):
    cursor = conexion.cursor()
    try:

        cursor.execute("START TRANSACTION")
        query_insert_activo = construccion_query_insert_activo(diccionario['nombre_activo'], diccionario['tipo_activo'])
        
        print ("Query activo: " + query_insert_activo + "\n")
        cursor.execute(query_insert_activo)

        id_activo = cursor.lastrowid
        numero_amenazas = 0
        for amenazas,values_amenazas in diccionario['dict_amenazas'].items():
            print("Amenazas prueba: " + amenazas + "\n")
            print(values_amenazas )
            
            #Activo amenaza
            query_insert_activo_amenaza = construccion_query_activo_amenaza(id_activo, values_amenazas['amenaza_id'], values_amenazas['probabilidad_id'])
            

            print("Query activo amenazas: " + query_insert_activo_amenaza + "\n")
            cursor.execute(query_insert_activo_amenaza)

            activo_amenaza_id = cursor.lastrowid

            #activo salvaguarda
            query_insert_activo_salvagauarda = construccion_query_insert_activo_salvaguarda(values_amenazas['salvaguarda'], values_amenazas['valoracion_salvaguarda'],activo_amenaza_id)
            print("Query activo salvaguarda: " + query_insert_activo_salvagauarda + "\n")
            cursor.execute(query_insert_activo_salvagauarda)


            for detalle_valor_id, escala_valor_id in values_amenazas['valores_ids'].items():
                #activo escala valor    
                query_insert_activo_escala_valor = construccion_query_activo_escala_valor(detalle_valor_id, escala_valor_id, activo_amenaza_id)
                print("Query activo escala valor: " + query_insert_activo_escala_valor + "\n")
                
                cursor.execute(query_insert_activo_escala_valor)
            numero_amenazas += 1

            #Hacer el insert de las tablas de resumen antes y resumen despues, además generar el grafico con ellas

        print("Numero de amenazas: " + str(numero_amenazas) + "\n")
        
        cursor.execute("COMMIT")

        conexion.commit()
        return id_activo
    except Error as e:
        cursor.execute("ROLLBACK")
        print(f"Error insertando: error '{e}' occurred")
        return None

