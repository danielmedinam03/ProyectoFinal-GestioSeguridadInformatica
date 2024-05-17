import mysql.connector
from mysql.connector import Error

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