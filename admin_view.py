import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from admin_controller import actualizar_estatus_topping, estatus_topings, agregar_nuevo_topping

# --- CONFIGURACIÓN DE COLORES ---
COLOR_SIDEBAR = "#FFF8F0"      # Crema muy claro
COLOR_MAIN_BG = "#EADBC8"      # Beige/Café claro del fondo principal
COLOR_BTN_SIDEBAR = "#EADBC8"  # Color botón inactivo
COLOR_BTN_ACTIVE = "#D7C2A8"   # Color botón activo
COLOR_TEXT = "#594A42"         # Café oscuro para textos
COLOR_BTN_GREEN = "#32CD32"    # Verde Habilitar
COLOR_BTN_RED = "#DC143C"      # Rojo Deshabilitar
COLOR_BTN_BROWN = "#5D4037"    # Café oscuro (Salir / Agregar)

class adminapp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Administrador - Delicias & Coffee")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        self.root.configure(bg=COLOR_MAIN_BG)

        # --- ESTRUCTURA PRINCIPAL (GRID) ---
        # Configuramos la ventana raíz para dividirla en 2: Sidebar (Col 0) y Contenido (Col 1)
        self.root.grid_columnconfigure(1, weight=1) # La columna 1 (contenido) se expande
        self.root.grid_rowconfigure(0, weight=1)    # La fila 0 se expande hacia abajo

        # 1. CREAR SIDEBAR (IZQUIERDA)
        self.sidebar_frame = tk.Frame(self.root, bg=COLOR_SIDEBAR, width=250)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_propagate(False) # Mantiene el ancho fijo

        self._crear_widgets_sidebar()

        # 2. CREAR AREA DE CONTENIDO (DERECHA)
        self.main_frame = tk.Frame(self.root, bg=COLOR_MAIN_BG)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Iniciar mostrando la página de Inventario por defecto
        self.mostrar_inventario()

    def _crear_widgets_sidebar(self):
        """Crea los botones y el logo del menú lateral"""
        
        # Título / Logo
        lbl_logo = tk.Label(self.sidebar_frame, text="Delicias & Coffee\nPostres y más", 
                            bg=COLOR_SIDEBAR, fg=COLOR_TEXT, font=("Arial", 16, "bold"), pady=30)
        lbl_logo.pack(fill="x")

        # Línea separadora
        ttk.Separator(self.sidebar_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        # Botones del Menú (Guardamos referencias para cambiar colores)
        self.btn_ventas = self._crear_boton_menu("💲 Ventas", self.mostrar_ventas)
        self.btn_inventario = self._crear_boton_menu("📋 C. Inventario", self.mostrar_inventario)
        self.btn_productos = self._crear_boton_menu("🍰 Productos", self.mostrar_productos)
        self.btn_reportes = self._crear_boton_menu("📄 Reportes", self.mostrar_reportes)

        # Botón Salir (al fondo)
        btn_salir = tk.Button(self.sidebar_frame, text="Salir", bg=COLOR_BTN_BROWN, fg="white",
                              font=("Arial", 10, "bold"), bd=0, padx=20, pady=10,
                              command=self.root.destroy) # Cierra la ventana actual
        btn_salir.pack(side="bottom", pady=30)

        lbl_admin = tk.Label(self.sidebar_frame, text="Administrador", bg=COLOR_SIDEBAR, 
                             fg="black", font=("Arial", 9, "bold"))
        lbl_admin.pack(side="bottom", pady=5)

    def _crear_boton_menu(self, texto, comando):
        """Helper para crear botones con estilo uniforme"""
        btn = tk.Button(self.sidebar_frame, text=texto, anchor="w",
                        bg=COLOR_SIDEBAR, fg=COLOR_TEXT, bd=0,
                        font=("Arial", 12), padx=20, pady=12,
                        command=comando)
        btn.pack(fill="x")
        return btn

    def _limpiar_panel_principal(self):
        """Elimina todo lo que haya en el panel derecho para cargar nueva vista"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def _resaltar_boton(self, boton_activo):
        """Cambia el color del botón seleccionado visualmente"""
        # Resetear todos al color original
        self.btn_ventas.config(bg=COLOR_SIDEBAR)
        self.btn_inventario.config(bg=COLOR_SIDEBAR)
        self.btn_productos.config(bg=COLOR_SIDEBAR)
        self.btn_reportes.config(bg=COLOR_SIDEBAR)
        
        # Marcar el activo con color diferente
        if boton_activo:
            boton_activo.config(bg=COLOR_BTN_ACTIVE)

    # --- VISTAS (PÁGINAS) ---

    def mostrar_inventario(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_inventario)

        # 1. Título
        tk.Label(self.main_frame, text="Control de Inventario", font=("Arial", 24, "bold"),
                 bg=COLOR_MAIN_BG, fg=COLOR_TEXT).pack(pady=(10, 5))

        btn_add = tk.Button(self.main_frame, text="➕ Agregar Nuevo Topping", 
                            bg=COLOR_BTN_BROWN, fg="white", font=("Arial", 10, "bold"),
                            command=self._popup_agregar_topping) # Llama a la funcion de abajo
        btn_add.pack(pady=5)

        btn_eliminar = tk.Button(self.main_frame, text="🗑️ Eliminar Topping", 
                            bg=COLOR_BTN_BROWN, fg="white", font=("Arial", 10, "bold"),
                            command=self._popup_eliminar_topping) # Llama a la funcion de abajo
        btn_eliminar.pack(pady=5)

        btn_actualizar = tk.Button(self.main_frame, text="✏️ Actualizar Topping", 
                            bg=COLOR_BTN_BROWN, fg="white", font=("Arial", 10, "bold"),
                            command=self._popup_actualizar_topping) # Llama a la funcion de abajo
        btn_actualizar.pack(pady=5)


        # 2. Cabecera (Tabla falsa)
        header_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        header_frame.pack(fill="x", pady=10, padx=20)
        
        tk.Label(header_frame, text="Ingrediente", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=("Arial", 12, "bold")).pack(side="left")
        
        tk.Label(header_frame, text="Estado", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=("Arial", 12, "bold")).pack(side="right")

        ttk.Separator(self.main_frame, orient="horizontal").pack(fill="x", padx=20)

        # 3. Lógica interna para actualizar (Igual que antes)
        def cambiar_estado(boton, variable, id_bd):
            nuevo_valor = variable.get()
            exito = actualizar_estatus_topping(id_bd, nuevo_valor) # Usamos la función del controller
            
            if exito:
                if nuevo_valor == 1:
                    boton.config(text="HABILITADO", bg=COLOR_BTN_GREEN, fg="white")
                else:
                    boton.config(text="DESHABILITADO", bg="gray", fg="black")
            else:
                variable.set(0 if nuevo_valor == 1 else 1) # Revertir si falla
                messagebox.showerror("Error", "Error de conexión BD")

        # 4. Listar Toppings
        items = estatus_topings()
        
        # Frame con scroll (Recomendado si vas a agregar muchos)
        canvas_container = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        canvas_container.pack(fill="both", expand=True)
        
        # (Aquí va tu ciclo for igual que lo tenías en la respuesta anterior...)
        for id_prod, nombre, habilitado in items:
            valor_inicial = 1 if habilitado == "si" else 0
            var = tk.IntVar(value=valor_inicial)

            row_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
            row_frame.pack(fill="x", padx=30, pady=5)

            tk.Label(row_frame, text=nombre, font=("Arial", 12), width=20, anchor="w", 
                     bg=COLOR_MAIN_BG, fg=COLOR_TEXT).pack(side="left")

            bg_color = COLOR_BTN_GREEN if valor_inicial == 1 else "gray"
            fg_color = "white" if valor_inicial == 1 else "black"
            txt_inicial = "HABILITADO" if valor_inicial == 1 else "DESHABILITADO"

            btn = tk.Checkbutton(row_frame, text=txt_inicial, variable=var, indicatoron=False,
                                 bg=bg_color, fg=fg_color, selectcolor=COLOR_BTN_GREEN,
                                 width=14, font=("Arial", 10, "bold"))
            
            btn.config(command=lambda b=btn, v=var, i=id_prod: cambiar_estado(b, v, i))
            btn.pack(side="right")


    # --- NUEVA FUNCIÓN PARA LA VENTANA EMERGENTE ---
    def _popup_agregar_topping(self):
        """Abre una ventana pequeña para escribir el nombre"""
        
        # Crear ventana secundaria (Toplevel)
        ventana_add = tk.Toplevel(self.root)
        ventana_add.title("Agregar Ingrediente")
        ventana_add.geometry("300x150")
        ventana_add.config(bg=COLOR_SIDEBAR)
        
        # Hacer que sea modal (no puedes tocar la ventana de atrás hasta cerrar esta)
        ventana_add.transient(self.root)
        ventana_add.grab_set()

        tk.Label(ventana_add, text="Nombre del nuevo topping:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 10)).pack(pady=10)

        entry_nombre = tk.Entry(ventana_add, font=("Arial", 12))
        entry_nombre.pack(pady=5, padx=20, fill="x")
        entry_nombre.focus() # Poner el cursor ahí automáticamente

        def guardar_datos():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showwarning("Cuidado", "El nombre no puede estar vacío", parent=ventana_add)
                return

            # Llamar al controlador
            exito = agregar_nuevo_topping(nombre)
            
            if exito:
                messagebox.showinfo("Éxito", f"'{nombre}' agregado correctamente", parent=ventana_add)
                ventana_add.destroy()       # Cerrar ventanita
                self.mostrar_inventario()   # <--- REFRESCAR LA LISTA AUTOMÁTICAMENTE
            else:
                messagebox.showerror("Error", "No se pudo guardar en la base de datos", parent=ventana_add)

        # Botón Guardar
        tk.Button(ventana_add, text="Guardar", bg=COLOR_BTN_GREEN, fg="white",
                  command=guardar_datos).pack(pady=15)

    def _popup_eliminar_topping(self):
        """Abre una ventana pequeña para escribir el nombre"""
        ventana_eliminar = tk.Toplevel(self.root)
        ventana_eliminar.title("Eliminar Topping")
        ventana_eliminar.geometry("300x150")
        ventana_eliminar.config(bg=COLOR_SIDEBAR)
        
        tk.Label(ventana_eliminar, text="Nombre del topping a eliminar:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 10)).pack(pady=10)
        entry_nombre = tk.Entry(ventana_eliminar, font=("Arial", 12))
        entry_nombre.pack(pady=5, padx=20, fill="x")
        entry_nombre.focus() # Poner el cursor ahí automáticamente

        def eliminar_topping():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showwarning("Cuidado", "El nombre no puede estar vacío", parent=ventana_eliminar)
                return
            
            # Llamar al controlador
            exito = eliminar_topping(nombre)
            
            if exito:
                messagebox.showinfo("Éxito", f"'{nombre}' eliminado correctamente", parent=ventana_eliminar)
                ventana_eliminar.destroy()       # Cerrar ventanita
                self.mostrar_inventario()   # <--- REFRESCAR LA LISTA AUTOMÁTICAMENTE
            else:
                messagebox.showerror("Error", "No se pudo eliminar el topping", parent=ventana_eliminar)

    def _popup_actualizar_topping(self):
        """Abre una ventana pequeña para escribir el nombre"""
        ventana_actualizar = tk.Toplevel(self.root)
        ventana_actualizar.title("Actualizar Topping")
        ventana_actualizar.geometry("300x150")
        ventana_actualizar.config(bg=COLOR_SIDEBAR)
        
        tk.Label(ventana_actualizar, text="Nombre del topping a actualizar:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 10)).pack(pady=10)  
        
    def mostrar_ventas(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_ventas)
        tk.Label(self.main_frame, text="Sección de Ventas", font=("Arial", 20), bg=COLOR_MAIN_BG).pack(pady=50)

    def mostrar_productos(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_productos)
        tk.Label(self.main_frame, text="Gestión de Productos", font=("Arial", 20), bg=COLOR_MAIN_BG).pack(pady=50)

    def mostrar_reportes(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_reportes)
        tk.Label(self.main_frame, text="Reportes Generales", font=("Arial", 20), bg=COLOR_MAIN_BG).pack(pady=50)