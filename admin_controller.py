from conexion import crear_conexion

def estatus_topings():
    conexion = crear_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_top, nombre, habilitado FROM topings") 
        resultado = cursor.fetchall()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

def actualizar_estatus_topping(id_topping, nuevo_estado):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        # cambia el si/no a 0/1 para la base de datos (o viceversa según lógica)
        estado_str = 'si' if nuevo_estado == 1 else 'no'
        
        sql = "UPDATE topings SET habilitado = %s WHERE id_top = %s"
        cursor.execute(sql, (estado_str, id_topping))
        conexion.commit() 
        conexion.close()
        print(f"Topping ID {id_topping} actualizado a {estado_str}")
        return True
    except Exception as e:
        print(f"Error al actualizar topping: {e}")
        return False

def agregar_nuevo_topping(nombre_topping):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        check_top= "SELECT COUNT(*) FROM topings WHERE nombre = %s"
        cursor.execute(check_top, (nombre_topping,))
        registrado = cursor.fetchone()[0]
        
        if registrado > 0:
            print(f"Error: El topping '{nombre_topping}' ya existe.")
            conexion.close()
            return "DUPLICADO"
        else:
            sql = "INSERT INTO topings (nombre, habilitado) VALUES (%s, %s)"
            cursor.execute(sql, (nombre_topping, 'si'))
            conexion.commit()
            conexion.close()
            return True
    except Exception as e:
        print(f"Error al insertar topping: {e}")
        return False

def eliminar_topping_bd(id_topping):
    """Elimina el topping de la base de datos"""
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM topings WHERE id_top = %s"
        cursor.execute(sql, (id_topping,)) 
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al eliminar topping: {e}")
        return False

def actualizar_nombre_topping(id_top, nuevo_nombre):
    conexion = crear_conexion()
    if not conexion:
        return False
        
    try:
        cursor = conexion.cursor()
        sql = "UPDATE topings SET nombre = %s WHERE id_top = %s"
        cursor.execute(sql, (nuevo_nombre, id_top))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al actualizar nombre: {e}")
        return False