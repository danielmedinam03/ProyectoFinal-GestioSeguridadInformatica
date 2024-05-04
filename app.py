# Importación de librerías necesarias
import streamlit as st
import mysql.connector
from mysql.connector import Error
from streamlit_option_menu import option_menu


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
    return list(result_options)

# Definición de la función principal del streamlit app
def main():
    # Título del dashboard
    st.title("Registro de activos")

    with st.sidebar:
        selected = option_menu("Menu", ["Formulario", 'Gráficos'],
                               icons=['house', 'gear'], menu_icon="cast", default_index=1)
    # Conexión a la base de datos
    connection = connect_to_database("localhost", "root", "password", "your_database")

    if selected == "Formulario":
        # Creación del formulario
#        with st.form(key='my_form'):
        text_input = st.text_input(label="Ingresa el nombre del activo:")
        dropdown1 = st.selectbox('Elige el tipo de activo:', ['Opción 1', 'Opción 2', 'Opción 3'])
        multiselect = st.multiselect('Elige las amenazas:', ['Option A', 'Option B', 'Option C'])

        # Botón para consultar tipos de amenazas
        consult_button = st.button("Consultar tipos de amenazas")

        if consult_button:
            multiselect1_options = get_options_based_on_selection(multiselect)
        #else:
        #    multiselect1_options = []

        if multiselect1_options.count() == 0:
            multiselect1 = st.multiselect('Elige los tipos de amenazas:', [])
        else:
            multiselect1 = st.multiselect('Elige los tipos de amenazas:', multiselect1_options)

        submit_button = st.button("Enviar")

        # Lógica para manejar la inserción de datos en la base de datos
        if submit_button:
            query = f"""
            INSERT INTO your_table (text_column, dropdown1_column, dropdown2_column, dropdown3_column)
            VALUES ('{text_input}', '{dropdown1}');
            """
            insert_data(connection, query)

    elif selected == "Gráficos":
        st.write("Sección de gráficos en construcción")

# Comentar esta línea antes de enviar el código al usuario
if __name__ == "__main__":
    main()
