from conexion import crear_conexion

def validar_login(usuario, password):
    """Verifica si el usuario y contraseña existen en la BD"""
    conexion = crear_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        sql = "SELECT * FROM users WHERE nombre = %s AND password = %s"
        cursor.execute(sql, (usuario, password))
        result = cursor.fetchone()
        conexion.close()

        return bool(result) 
    except Exception as e:
        print(f"Error en login: {e}")
        return False

def obtener_categorias():
    """Obtiene todas las categorías para las pestañas"""
    conexion = crear_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_categorias, nombre_categoria FROM categorias_productos")
        resultado = cursor.fetchall()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error categorias: {e}")
        return []

def obtener_productos_por_categoria(id_categoria):
    """Obtiene los productos filtrados por el ID de categoría"""
    conexion = crear_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT id_producto, nombre, precio FROM productos WHERE id_categoria = %s"
        cursor.execute(sql, (id_categoria,))
        resultado = cursor.fetchall()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error productos: {e}")
        return []