# Importación de librerías necesarias
import decimal
import json
import streamlit as st
import mysql.connector
from mysql.connector import Error
from streamlit_option_menu import option_menu
import pdb


# Inicializar el estado de la sesión si es necesario
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = []
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []

# Configuración de la conexión a la base de datos
def connect_to_database(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    except Error as e:
        print(f"Error conectando a Base de datos: error '{e}' occurred")
    return connection

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

# Función para insertar datos en la base de datos
def insert_data(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"Error insertando: error '{e}' occurred")

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

def construccion_query_insert_activo(nombre_activo, tipo_activo):
    query = f"""
    INSERT INTO activo (nombre, tipo_activo_id)
    VALUES ('{nombre_activo}', {tipo_activo});
    """
    return query

def construccion_query_insert_detalle_valor(connection,list_detalle_valor_id, list_impacto_valor_id, activo_id):
    
    for i in range(len(list_detalle_valor_id)):
        detalle_valor_id = list_detalle_valor_id[i]
        escala_valor_id = list_impacto_valor_id[i]
        query = f"""
        INSERT INTO activo_escala_valor (activo_id, detalle_valor_id, escala_valor_id)
        VALUES ('{activo_id}', '{detalle_valor_id}', '{escala_valor_id}'); 
        """
        insert_data(connection, query)

def construccion_query_insert_transaccion(conexion,query):
    cursor = conexion.cursor()
    try:

        cursor.execute("START TRANSACTION")
        cursor.execute(query)

        # Obtener el ID del nuevo registro insertado
        new_id = cursor.lastrowid
        cursor.execute("COMMIT")

        conexion.commit()
        return new_id
    except Error as e:
        cursor.execute("ROLLBACK")
        print(f"Error insertando: error '{e}' occurred")
        return None

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

def consulta_valor_probabilidad(connection, nombre):
    query = f"SELECT v.probabilidad FROM valoracion_amenazas AS v WHERE opciones = '{nombre}'"
    result_probabilidad = execute_select_query(connection, query)
    return result_probabilidad[0][0]
# Definición de la función principal del streamlit app
def main():
    # Título del dashboard
    st.title("Registro de activos")

    with st.sidebar:
        selected = option_menu("Menu", ["Formulario", 'Gráficos'],
                               icons=['house', 'gear'], menu_icon="cast", default_index=0)
    # Conexión a la base de datos
    connection = connect_to_database("localhost", "root", "Dfmm.03112002", "gestion_seguridad")

    if selected == "Formulario":
        dictionario_final = {}
        
        nombre_activo = st.text_input(label="Ingresa el nombre del activo:")
        #-----------------------
        result_tipos_activos = consulta_tipos_activos(connection)
        tipo_activo = st.selectbox('Elige el tipo de activo:', list(result_tipos_activos.keys()), placeholder='Seleccione un tipo de activo...')
        #Este es el valor del id seleccionado del tipo de activo
        tipo_activo_selected_id = result_tipos_activos[tipo_activo] if tipo_activo in result_tipos_activos else None
        #-----------------------
        
        result_tipos_amenazas = consulta_tipo_amenaza(connection)
        amenaza = st.multiselect('Elige los tipos de amenazas:', list(result_tipos_amenazas.keys()),
                                        key='selected_category', placeholder="Seleccione una amenaza...")
        #Este es el valor del id seleccionado de la amenaza
        
        #-----------------------
        result_amenazas = consulta_amenaza(connection,amenaza)

        tipos_amenazas = st.multiselect("Selecciona las amenazas:", result_amenazas, key='selected_items', 
                                        placeholder="Seleccione los tipos de amenazas...")

        #Se obtiene el valor de la escala de valor
        escala_valor = consulta_escalar_valor(connection)
        
        #Declaracion de variables
        dict_detalle_valor = {}
        suma_impacto_potencial = 0
        probabilidad = 0
        riesgo_potencial = 0

        if tipos_amenazas != []:
            for index, item in enumerate(tipos_amenazas):
                st.subheader(f"Valor de: {item}")
                suma_impacto_potencial = 0
                valor_col1, valor_col2, valor_col3 = st.columns(3)
                list_detalle_valor = []
                with valor_col1:
                    #Se selecciona el nombre de la escala valor
                    valor_confidencialidad = st.selectbox("Confidencialidad:", list(escala_valor.keys()), key=f'valor_confidencialidad_{index}')
                    #Se extrae el id de la escala valor seleccionada
                    valor_confidencialidad_selected_id = escala_valor[valor_confidencialidad] if valor_confidencialidad in escala_valor else None
                    
                    #Se otiene el valor numerico para el impacto potencial
                    valor_confidencialidad_selected = consulta_valor_escala_valor(connection,valor_confidencialidad_selected_id)
                    suma_impacto_potencial += valor_confidencialidad_selected
                    list_detalle_valor.append(valor_confidencialidad_selected_id)

                with valor_col2:
                    valor_integridad = st.selectbox("Integridad:", list(escala_valor.keys()), key=f'valor_integridad_{index}')
                    valor_integridad_selected_id = escala_valor[valor_integridad] if valor_integridad in escala_valor else None

                    valor_integridad_selected = consulta_valor_escala_valor(connection,valor_integridad_selected_id)
                    suma_impacto_potencial += valor_integridad_selected

                    list_detalle_valor.append(valor_integridad_selected_id)

                with valor_col3:
                    valor_disponibilidad = st.selectbox("Disponibilidad:", list(escala_valor.keys()), key=f'valor_disponibilidad_{index}')
                    valor_disponibilidad_selected_id = escala_valor[valor_disponibilidad] if valor_disponibilidad in escala_valor else None
                    
                    valor_disponibilidad_selected = consulta_valor_escala_valor(connection,valor_disponibilidad_selected_id)
                    suma_impacto_potencial += valor_disponibilidad_selected

                    list_detalle_valor.append(valor_disponibilidad_selected_id)
                
                # Sumatoria de la valoracion del impacto, confidencialidad, integridad y disponibilidad
                st.markdown("##### Impacto potencial: " + str(suma_impacto_potencial))

                probabilidad = st.selectbox("Probabilidad: ", list(opciones_probabilidad(consulta_probabilidad(connection))), key=f'probabilidad_{index}')
                valor_probabilidad = consulta_valor_probabilidad(connection,probabilidad)

                riesgo_potencial = valor_probabilidad * suma_impacto_potencial
                # ImpactoPotencial * Probabilidad
                st.markdown("##### Riesgo potencial: " + str(riesgo_potencial))

                st.markdown("---")

                #La idea es que aqui se de esta manera se guardan los valores, para luego crear una funcion que inserte los datos en la bd y reciba por parametro el diccionario

                dict_detalle_valor[item] = {'valores_ids': list_detalle_valor, 'impacto_potencial': suma_impacto_potencial, 'probabilidad': probabilidad, 'valor_probabilidad': float(valor_probabilidad), 'riesgo_potencial': float(riesgo_potencial)}

                #Aqui se debe continuar con los salvaguardar, y con la linea de arriba, terminar de completar todos lo valores para el diccionario

        # Botón para enviar el formulario completo
        submit_button = st.button("Enviar")

        #Llenado del diccionario
        dictionario_final['nombre_activo'] = nombre_activo
        dictionario_final['tipo_activo'] = tipo_activo
        dictionario_final['tipos_amenazas'] = tipos_amenazas
        dictionario_final['dict_detalle_valor'] = dict_detalle_valor

        if (submit_button and len(tipos_amenazas) > 0 and (tipo_activo != 'Seleccione un tipo de activo...' and tipo_activo != '') 
            and len(amenaza) > 0 and nombre_activo != ''):
            
            print("Envio el Formulario")
            
            print(dictionario_final)
            print("-----------------------------------------------------------------------")

            # query = construccion_query_insert_activo(nombre_activo, tipo_activo_selected_id)
            # id_activo = construccion_query_insert_transaccion(conexion=connection, query=query)
            # print(id_activo)
            # construccion_query_insert_detalle_valor(activo_id=id_activo, list_detalle_valor_id=list_detalle_valor, list_impacto_valor_id=list_impacto, connection=connection)



            # print(query)
            # print(list_detalle_valor)
            # print(list_impacto)
            
            # Asumimos que insert_data es una función definida para ejecutar la consulta SQL
            #insert_data(connection, query)
        
    elif selected == "Gráficos":
        st.write("Sección de gráficos en construcción")


# Comentar esta línea antes de enviar el código al usuario
if __name__ == "__main__":
    main()
