# Importación de librerías necesarias
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

def consulta_amenazas(connection):

    query_amenazas = f"SELECT a.amenaza_id, a.nombre FROM amenaza AS a"
    result_amenazas = execute_select_query(connection,query_amenazas)
    data = {nombre: id for id, nombre in result_amenazas}
    return data

def consulta_tipo_amenaza(connection, amenazas):

    lista = []

    for item in amenazas:
        query_tipo_amenaza = f"SELECT * FROM tipo_amenaza ta JOIN amenaza a ON  ta.amenaza_id = a.amenaza_id WHERE a.nombre = '{item}';"
        result_tipo_amenaza = execute_select_query(connection,query_tipo_amenaza)
        for item in result_tipo_amenaza:
            lista.append(item[1])

    return lista

def consulta_escalar_valor(connection):
    lista = []

    query_escalar_valor = f"SELECT es.escalar_valor_id, es.nombre FROM escalar_valor AS es"
    result_escalar_valor = execute_select_query(connection,query_escalar_valor)
    
    return {nombre: id for id, nombre in result_escalar_valor}

def construccion_query_insert(nombre_activo, tipo_activo, tipos_amenazas):
    query = f"""
    INSERT INTO activo (nombre_activo, tipo_activo, tipo_amenaza)
    VALUES ('{nombre_activo}', '{tipo_activo}', '{tipos_amenazas}');
    """
    return query


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

        nombre_activo = st.text_input(label="Ingresa el nombre del activo:")
        #-----------------------
        result_tipos_activos = consulta_tipos_activos(connection)
        tipo_activo = st.selectbox('Elige el tipo de activo:', list(result_tipos_activos.keys()), placeholder='Seleccione un tipo de activo...')
        #Este es el valor del id seleccionado del tipo de activo
        tipo_activo_selected_id = result_tipos_activos[tipo_activo] if tipo_activo in result_tipos_activos else None
        #-----------------------
        
        result_amenazas = consulta_amenazas(connection)
        amenaza = st.multiselect('Elige las amenazas:', list(result_amenazas.keys()),
                                        key='selected_category', placeholder="Seleccione una amenaza...")
        #Este es el valor del id seleccionado de la amenaza
        amenaza_selected_id = result_amenazas[amenaza] if amenaza in result_amenazas else None
        print(amenaza_selected_id)
        #-----------------------
        multiselect1_options = consulta_tipo_amenaza(connection,amenaza)

        tipos_amenazas = st.multiselect("Selecciona los tipos de amenazas:", multiselect1_options, key='selected_items', 
                                        placeholder="Seleccione los tipos de amenazas...")

        st.subheader("Valor")

        #Se obtiene el valor de la escala de valor
        escala_valor = consulta_escalar_valor(connection)

        valor_col1, valor_col2, valor_col3, valor_col4, valor_col5 = st.columns(5)

        with valor_col1:
            #Se selecciona el nombre de la escala valor
            valor_confidencialidad = st.selectbox("Confidencialidad:", list(escala_valor.keys()))
            #Se extrae el id de la escala valor seleccionada
            valor_confidencialidad_selected_id = escala_valor[valor_confidencialidad] if valor_confidencialidad in escala_valor else None
        with valor_col2:
            valor_integridad = st.selectbox("Integridad:", list(escala_valor.keys()))
            valor_integridad_selected_id = escala_valor[valor_integridad] if valor_integridad in escala_valor else None
        with valor_col3:
            valor_disponibilidad = st.selectbox("Disponibilidad:", list(escala_valor.keys()))
            valor_disponibilidad_selected_id = escala_valor[valor_disponibilidad] if valor_disponibilidad in escala_valor else None

        with valor_col4:
            valor_trazabilidad_datos = st.selectbox("Trazabilidad:", list(escala_valor.keys()))
            valor_trazabilidad_datos_selected_id = escala_valor[valor_trazabilidad_datos] if valor_trazabilidad_datos in escala_valor else None

        with valor_col5:
            valor_autenticidad_datos = st.selectbox("Autenticidad:", list(escala_valor.keys()))
            valor_autenticidad_datos_selected_id = escala_valor[valor_autenticidad_datos] if valor_autenticidad_datos in escala_valor else None


        st.subheader("Impacto potencial")

        # Crear un layout con columnas para los selectbox
        impacto_col1, impacto_col2, impacto_col3, impacto_col4, impacto_col5 = st.columns(5)
        
        with impacto_col1:
            impacto_confidencialidad = st.selectbox("Confidencialidad: ", list(escala_valor.keys()))
            impacto_confidencialidad_selected_id = escala_valor[impacto_confidencialidad] if impacto_confidencialidad in escala_valor else None

        with impacto_col2:
            impacto_integridad = st.selectbox("Integridad: ", list(escala_valor.keys()))
            impacto_integridad_selected_id = escala_valor[impacto_integridad] if impacto_integridad in escala_valor else None

        with impacto_col3:
            impacto_disponibilidad = st.selectbox("Disponibilidad: ", list(escala_valor.keys()))
            impacto_disponibilidad_selected_id = escala_valor[impacto_disponibilidad] if impacto_disponibilidad in escala_valor else None

        with impacto_col4:
            impacto_trazabilidad_datos = st.selectbox("Trazabilidad: ", list(escala_valor.keys()))
            impacto_trazabilidad_datos_selected_id = escala_valor[impacto_trazabilidad_datos] if impacto_trazabilidad_datos in escala_valor else None

        with impacto_col5:
            impacto_autenticidad_datos = st.selectbox("Autenticidad: ", list(escala_valor.keys()))
            impacto_autenticidad_datos_selected_id = escala_valor[impacto_autenticidad_datos] if impacto_autenticidad_datos in escala_valor else None


        # Botón para enviar el formulario completo
        submit_button = st.button("Enviar")
        print("Envio el Formulario")

        if (submit_button and len(tipos_amenazas) > 0 and (tipo_activo != 'Seleccione un tipo de activo...' and tipo_activo != '') 
            and len(amenaza) > 0 and nombre_activo != ''):
            
            query = f"""
            INSERT INTO your_table (text_column, dropdown1_column, dropdown2_column, dropdown3_column)
            VALUES ('{nombre_activo}', '{tipo_activo}', '{tipos_amenazas}');
            """
            
            print(query)
            
            # Asumimos que insert_data es una función definida para ejecutar la consulta SQL
            #insert_data(connection, query)
        
    elif selected == "Gráficos":
        st.write("Sección de gráficos en construcción")


# Comentar esta línea antes de enviar el código al usuario
if __name__ == "__main__":
    main()
