import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user='root',
            password = '',
            database = 'bd_proyecto_crepas'
        )

        if conexion.is_connected():
            print("Conexion exitosa en la base de datos")
            return conexion
        
    except Error as e:
        print("Error al conectar a Mysql: {e}")
        return None