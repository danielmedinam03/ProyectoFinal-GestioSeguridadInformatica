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
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_select_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()  # Recupera todos los registros
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return None


# Función para insertar datos en la base de datos
def insert_data(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def get_options_based_on_selection(selected_items):
    options_mapping = {
        'Option A': ['Type 1', 'Type 2'],
        'Option B': ['Type 3', 'Type 4'],
        'Option C': ['Type 5', 'Type 6']
    }
    # Generar un conjunto único de opciones basadas en las selecciones de multiselect
    result_options = set()
    for item in selected_items:
        result_options.update(options_mapping.get(item, []))
    print(list(result_options))
    return list(result_options)

def get_options_based_on_selection(selection):
    options_mapping = {
        'Option A': ['Type 1', 'Type 2'],
        'Option B': ['Type 3', 'Type 4'],
        'Option C': ['Type 5', 'Type 6']
    }

    # Esta función devuelve las opciones para el segundo multiselect basado en la selección del primero
    if not selection:
        return []
    else:
        # Agrega todas las opciones posibles basadas en las categorías seleccionadas
        options = []
        for category in selection:
            options.extend(options_mapping.get(category, []))
        return options

def consulta_tipos_activos(connection):
    lista = ['Seleccione un tipo de activo...']

    query_tipo_activo = f"SELECT * FROM tipo_activo"
    result_tipo_activo = execute_select_query(connection,query_tipo_activo)
    for item in result_tipo_activo:
        lista.append(item[1])
    return lista

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
        # Creación del formulario
        with st.form(key='my_form'):

            nombre_activo = st.text_input(label="Ingresa el nombre del activo:")
            
            tipo_activo = st.selectbox('Elige el tipo de activo:', consulta_tipos_activos(connection))

            #multiselect = st.multiselect('Elige las amenazas:', ['Option A', 'Option B', 'Option C'])
            tipo_amenaza = st.multiselect('Elige las amenazas:', ['Option A', 'Option B', 'Option C'],
                                         key='selected_category')

            # Esta variable debe inicializarse fuera del if para evitar errores de referencia
            multiselect1_options = get_options_based_on_selection(tipo_amenaza)

            #multiselect1 = st.multiselect('Elige los tipos de amenazas:', multiselect1_options)
            multiselect1 = st.multiselect("Selecciona items:", multiselect1_options, key='selected_items')

            # Botón para enviar el formulario completo
            submit_button = st.form_submit_button("Enviar")

            if submit_button and len(multiselect1) > 0:
                query = f"""
                INSERT INTO your_table (text_column, dropdown1_column, dropdown2_column, dropdown3_column)
                VALUES ('{nombre_activo}', '{tipo_activo}', '{multiselect1}');
                """
                print(query)
                # Asumimos que insert_data es una función definida para ejecutar la consulta SQL
                #insert_data(connection, query)
    elif selected == "Gráficos":
        st.write("Sección de gráficos en construcción")


# Comentar esta línea antes de enviar el código al usuario
if __name__ == "__main__":
    main()
