from conexion import crear_conexion

def validar_credenciales(usuario, password):

    conexion = crear_conexion()
    
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    consulta = "SELECT * FROM users WHERE nombre = %s AND password = %s"
    cursor.execute(consulta, (usuario, password))
    result = cursor.fetchone()

    conexion.close()
    return bool(result)