from conexion import crear_conexion

def validar_credenciales(usuario, password):
    conexion = crear_conexion()
    
    if not conexion:
        return 0 
    
    try:
        cursor = conexion.cursor()
        
        consulta = "SELECT nombre FROM users WHERE nombre = %s AND password = %s"
        cursor.execute(consulta, (usuario, password))
        result = cursor.fetchone()

        conexion.close()

        if result:
            nombre_usuario = result[0].upper()
            
            if nombre_usuario == 'ADMIN':
                print(2)
                return 2
            else:
                print(1)
                return 1
        else:
            return 0
            
    except Exception as e:
        print(f"Error al validar credenciales: {e}")
        if conexion:
            conexion.close()
        return 0