from conexion import crear_conexion
import datetime

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
        sql = "SELECT id_producto, nombre, precio, id_categoria, cant_top FROM productos WHERE id_categoria = %s"
        cursor.execute(sql, (id_categoria,))
        resultado = cursor.fetchall()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error productos: {e}")
        return []

def obtener_toppings_habilitados():
    """Obtiene los toppings que están habilitados ('si') para la venta."""
    conexion = crear_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor(dictionary=True)
        # Trae solo los habilitados
        sql = "SELECT id_top, nombre FROM topings WHERE habilitado = 'si'"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error al obtener toppings: {e}")
        return []

def registrar_venta(id_vendedor, detalles_carrito, total_final):
    conexion = crear_conexion()
    if not conexion: 
        return False
    
    try:
        cursor = conexion.cursor()
        ahora = datetime.datetime.now()
        fecha_hora_actual = ahora.strftime('%Y-%m-%d %H:%M:%S')

        # 2. INSERTAR EN VENTAS_MAESTRO (Encabezado del Ticket)
        # La columna en tu BD es 'fecha' pero su tipo es DATETIME
        sql_maestro = """
            INSERT INTO ventas_maestro (id_vendedor, total_final, fecha) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_maestro, (id_vendedor, total_final, fecha_hora_actual))
        id_maestro = cursor.lastrowid

        # insercion en la tabla detalles
        sql_detalle = """
            INSERT INTO ventas_detalle (id_maestro, id_producto, cantidad, precio_unitario, descripcion_detalle) 
            VALUES (%s, %s, %s, %s, %s)
        """
        
        for item in detalles_carrito:
            cursor.execute(sql_detalle, (
                id_maestro,
                item['id_prod'],
                item['cantidad'],
                item['precio_unitario'],
                item['producto_descripcion'] 
            ))

        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al registrar venta (Maestro-Detalle): {e}")
        if conexion:
            conexion.rollback() 
        return False

