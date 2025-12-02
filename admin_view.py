import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from admin_controller import (actualizar_estatus_topping, estatus_topings,agregar_nuevo_topping, eliminar_topping_bd,
                              actualizar_nombre_topping, mostrar_productos,agregar_nuevo_producto, obtener_productos_con_id,
                              eliminar_producto_bd, actualizar_producto, obtener_reporte_ventas_agrupadas,)
from seller_controller import obtener_categorias
import seller_view

# colores
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

       
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)  

        # menu izquierda
        self.sidebar_frame = tk.Frame(self.root, bg=COLOR_SIDEBAR, width=250)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_propagate(False)

        self._crear_widgets_sidebar()

        # area de contenido
        self.main_frame = tk.Frame(self.root, bg=COLOR_MAIN_BG)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # inventario por defecto
        self.mostrar_inventario()

    def _crear_widgets_sidebar(self):     
        # Título 
        lbl_logo = tk.Label(self.sidebar_frame, text="Delicias & Coffee\nPostres y más", 
                            bg=COLOR_SIDEBAR, fg=COLOR_TEXT, font=("Arial", 16, "bold"), pady=30)
        lbl_logo.pack(fill="x")

        # raya separadora
        ttk.Separator(self.sidebar_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        # botones
        self.btn_ventas = self.botones_menu("💲 Ventas", self.mostrar_ventas)
        self.btn_inventario = self.botones_menu("📋 C. Inventario", self.mostrar_inventario)
        self.btn_productos = self.botones_menu("🍰 Productos", self.mostrar_productos)
        self.btn_reportes = self.botones_menu("📄 Reportes", self.mostrar_reportes)

        # salir
        btn_salir = tk.Button(self.sidebar_frame, text="Salir", bg=COLOR_BTN_BROWN, fg="white",
                              font=("Arial", 10, "bold"), bd=0, padx=20, pady=10,
                              command=self.cerrar_y_abrir_vendedor)
        btn_salir.pack(side="bottom", pady=30)

        lbl_admin = tk.Label(self.sidebar_frame, text="Administrador", bg=COLOR_SIDEBAR, 
                             fg="black", font=("Arial", 9, "bold"))
        lbl_admin.pack(side="bottom", pady=5)

    def cerrar_y_abrir_vendedor(self):
            self.root.destroy()
            root_seller = tk.Tk()
            seller_view.sellerApp(root_seller) 
            root_seller.mainloop()
        

    def botones_menu(self, texto, comando):
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

     # paneles

    '''INVENTARIO / TOPPINGS'''

    def mostrar_inventario(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_inventario)

        tk.Label(self.main_frame, text="Control de Inventario", font=("Arial", 24, "bold"),
                 bg=COLOR_MAIN_BG, fg=COLOR_TEXT).pack(side="top", pady=(10, 5))

     # botones abajo
        footer_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        footer_frame.pack(side="bottom", fill="x", pady=20, padx=30)

        #agregar
        btn_add = tk.Button(footer_frame, text="➕ Agregar Nuevo", 
                            bg=COLOR_BTN_BROWN, fg="white", font=("Arial", 11, "bold"),
                            padx=20, pady=10,
                            command=self._popup_agregar_topping)
        btn_add.pack(side="right", padx=(10, 0))

        # funciones
        btn_funciones = tk.Button(footer_frame, text="⚙️ Funciones / Eliminar", 
                                  bg=COLOR_BTN_BROWN, fg="white", font=("Arial", 11, "bold"),
                                  padx=20, pady=10,
                                  command=self.panel_funciones)
        btn_funciones.pack(side="right")

     # encabezados
        header_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        header_frame.pack(side="top", fill="x", pady=10, padx=40) 
        
        tk.Label(header_frame, text="Ingrediente", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=("Arial", 12, "bold")).pack(side="left")
        
        tk.Label(header_frame, text="Estado", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=("Arial", 12, "bold")).pack(side="right", padx=(0, 40)) # Margen para alinear con botones

        ttk.Separator(self.main_frame, orient="horizontal").pack(side="top", fill="x", padx=30)

     # scroll 
        container_scroll = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        container_scroll.pack(side="top", fill="both", expand=True, padx=30, pady=5)

        canvas = tk.Canvas(container_scroll, bg=COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_scroll, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg=COLOR_MAIN_BG)

        # Configuración crítica para el scroll
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def ajustar_ancho(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", ajustar_ancho)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

     # botones 
        
        # Función simplificada para el click del botón
        def click_boton(btn_widget, var_tk, id_db):
            nuevo_valor = var_tk.get() 

            # Actualizar Base de Datos
            exito = actualizar_estatus_topping(id_db, nuevo_valor)
            
            if exito:
                if nuevo_valor == 1:
                    btn_widget.config(text="HABILITADO", bg=COLOR_BTN_GREEN, fg="white")
                else:
                    btn_widget.config(text="DESHABILITADO", bg=COLOR_BTN_RED, fg="white")
            else:
                revertido = 0 if nuevo_valor == 1 else 1
                var_tk.set(revertido)
                messagebox.showerror("Error", "No se pudo actualizar la base de datos.")
        items = estatus_topings()

        for id_prod, nombre, habilitado in items:
            valor_inicial = 1 if habilitado == "si" else 0
            var = tk.IntVar(value=valor_inicial)
            
            # Fila
            row_frame = tk.Frame(scrollable_frame, bg="#FFF8F0")
            row_frame.pack(fill="x", pady=5, ipadx=5, ipady=5)

            # nombre
            tk.Label(row_frame, text=nombre, font=("Arial", 12, "bold"), anchor="w", 
                     bg="#FFF8F0", fg="#5D4037").pack(side="left", padx=10)

            # confuguracion de los botones
            if valor_inicial == 1:
                txt = "HABILITADO"
                col = COLOR_BTN_GREEN
            else:
                txt = "DESHABILITADO"
                col = COLOR_BTN_RED

            # boton de estatus
            btn = tk.Checkbutton(row_frame, text=txt, variable=var, indicatoron=False,
                                 bg=col, fg="white", selectcolor=COLOR_BTN_GREEN,
                                 font=("Arial", 10, "bold"), width=15, cursor="hand2")
            
            btn.config(command=lambda b=btn, v=var, i=id_prod: click_boton(b, v, i))
            
            btn.pack(side="right", padx=10)


     # ventana agregar
    
    def _popup_agregar_topping(self):
        ventana_add = tk.Toplevel(self.root)
        ventana_add.title("Agregar Ingrediente")
        ventana_add.geometry("300x150")
        ventana_add.config(bg=COLOR_SIDEBAR)
        
        ventana_add.transient(self.root)
        ventana_add.grab_set()

        tk.Label(ventana_add, text="Nombre del nuevo topping:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 10)).pack(pady=10)

        entry_nombre = tk.Entry(ventana_add, font=("Arial", 12))
        entry_nombre.pack(pady=5, padx=20, fill="x")
        entry_nombre.focus() 

        def guardar_datos():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showwarning("Cuidado", "El nombre no puede estar vacío", parent=ventana_add)
                return

            exito = agregar_nuevo_topping(nombre)
            
            if exito=="DUPLICADO":
                messagebox.showinfo("Error", f"'{nombre}' Ya esta registrado ", parent=ventana_add)
                ventana_add.destroy()      
                self.mostrar_inventario()  
            elif exito:
                messagebox.showinfo("Éxito", f"'{nombre}' agregado correctamente", parent=ventana_add)
                ventana_add.destroy()      
                self.mostrar_inventario()  
                messagebox.showerror("Error", "No se pudo guardar en la base de datos", parent=ventana_add)

        tk.Button(ventana_add, text="Guardar", bg=COLOR_BTN_GREEN, fg="white",
                  command=guardar_datos).pack(pady=15)

    def panel_funciones(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_inventario)

        header_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        header_frame.pack(fill="x", pady=10)
        
        tk.Button(header_frame, text="⬅ Volver", bg=COLOR_BTN_BROWN, fg="white",
                  font=("Arial", 10, "bold"), command=self.mostrar_inventario).pack(side="left", padx=10)

        tk.Label(header_frame, text="Gestión de Ingredientes", font=("Arial", 20, "bold"),
                 bg=COLOR_MAIN_BG, fg=COLOR_TEXT).pack(side="left", padx=20)


        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="white", fieldbackground="white", foreground="black",
                        font=("Arial", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#D7C2A8")

        # crear la tabla
        frame_tabla = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=5)

        # columnas
        columns = ("ID", "Nombre", "Estado")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=12)
        
        # encabezados
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre del Topping")
        self.tree.heading("Estado", text="Habilitado")

        # configuración de las columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=350, anchor="w")
        self.tree.column("Estado", width=100, anchor="center")

        # sroll
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # cargar los datos
        datos = estatus_topings()
        for item in datos:
            self.tree.insert("", "end", values=item)

        # botones 
        frame_botones = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        frame_botones.pack(fill="x", pady=20, padx=20)

        tk.Button(frame_botones, text="✏️ Editar Nombre", 
                  bg="#FFD700", fg="black", font=("Arial", 11, "bold"),
                  padx=15, pady=10, command=self.accion_actualizar).pack(side="left", padx=(0, 20))

        tk.Button(frame_botones, text="🗑️ Eliminar Seleccionado", 
                  bg=COLOR_BTN_RED, fg="white", font=("Arial", 11, "bold"),
                  padx=15, pady=10, command=self.accion_eliminar).pack(side="left")

     # logica de los botones

    def accion_eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un topping de la tabla para eliminarlo.")
            return
        
        # seleccion de items
        item = self.tree.item(seleccion)
        id_top = item['values'][0]
        nombre = item['values'][1]

        confirmar = messagebox.askyesno("Confirmar Eliminación", 
                                        f"¿Seguro que deseas eliminar '{nombre}'?\nEsta acción es permanente.")
        if confirmar:
            if eliminar_topping_bd(id_top):
                messagebox.showinfo("Éxito", "Topping eliminado correctamente.")
                self.panel_funciones()
            else:
                messagebox.showerror("Error", "No se pudo eliminar de la base de datos.")

    def accion_actualizar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un topping para editar su nombre.")
            return

        item = self.tree.item(seleccion)
        id_top = item['values'][0]
        nombre_actual = item['values'][1]
        ventana_edit = tk.Toplevel(self.root)
        ventana_edit.title(f"Editar: {nombre_actual}")
        ventana_edit.geometry("350x180")
        ventana_edit.config(bg=COLOR_SIDEBAR)
        ventana_edit.transient(self.root)
        ventana_edit.grab_set()

        tk.Label(ventana_edit, text="Nuevo nombre del topping:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 10)).pack(pady=15)
        
        entry_nuevo = tk.Entry(ventana_edit, font=("Arial", 12))
        entry_nuevo.insert(0, nombre_actual) # esto pone l nombre actual al campo
        entry_nuevo.pack(pady=5, padx=20, fill="x")
        entry_nuevo.focus()

        def guardar_cambio():
            nuevo_nombre = entry_nuevo.get().strip()
            if not nuevo_nombre:
                messagebox.showwarning("Cuidado", "El nombre no puede estar vacío", parent=ventana_edit)
                return
            
            if actualizar_nombre_topping(id_top, nuevo_nombre):
                messagebox.showinfo("Éxito", "Nombre actualizado.", parent=ventana_edit)
                ventana_edit.destroy()
                self.panel_funciones() # Recargar tabla
            else:
                messagebox.showerror("Error", "Fallo al actualizar en BD.", parent=ventana_edit)

        tk.Button(ventana_edit, text="💾 Guardar Cambios", bg=COLOR_BTN_GREEN, fg="white",
                  command=guardar_cambio).pack(pady=15)

    '''VENTAS'''
    def mostrar_ventas(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_ventas)
        tk.Label(self.main_frame, text="Sección de Ventas", font=("Arial", 20), bg=COLOR_MAIN_BG).pack(pady=50)

    '''PRODUCTOS'''
    
    def mostrar_productos(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_productos) 

        tk.Label(self.main_frame, text="Control de Productos", font=("Arial", 24, "bold"),
                 bg=COLOR_MAIN_BG, fg=COLOR_TEXT).pack(side="top", pady=(10, 5))
                 
        footer_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        footer_frame.pack(side="bottom", fill="x", pady=20, padx=30)

        # agregar
        btn_add_producto = tk.Button(footer_frame, text="➕ Agregar Nuevo", 
                            bg=COLOR_BTN_BROWN, fg="white", font=("Arial", 11, "bold"),
                            padx=20, pady=10,
                            command=self._mostrar_panel_agregar_producto)
        btn_add_producto.pack(side="right", padx=(10, 0))

        # funciones
        btn_funciones_producto = tk.Button(footer_frame, text="⚙️ Funciones / Eliminar", 
                                  bg=COLOR_BTN_BROWN, fg="white", font=("Arial", 11, "bold"),
                                  padx=20, pady=10,
                                  command=self.panel_funciones_producto)
        btn_funciones_producto.pack(side="right")

        header_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        header_frame.pack(side="top", fill="x", pady=10, padx=40) 
        
        tk.Label(header_frame, text="Nombre", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=("Arial", 12, "bold"), width=15, anchor="w").pack(side="left", padx=(0, 10))

        tk.Label(header_frame, text="Cant. Top.", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=("Arial", 12, "bold"), width=10, anchor="center").pack(side="right", padx=10) 

        tk.Label(header_frame, text="Precio", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=("Arial", 12, "bold"), width=8, anchor="center").pack(side="right", padx=10) 
                 
        tk.Label(header_frame, text="Descripción", bg=COLOR_MAIN_BG, fg=COLOR_TEXT,
                 font=("Arial", 12, "bold"), anchor="w").pack(side="left", expand=True)
        
        ttk.Separator(self.main_frame, orient="horizontal").pack(side="top", fill="x", padx=30)

        container_scroll = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        container_scroll.pack(side="top", fill="both", expand=True, padx=30, pady=5)

        canvas = tk.Canvas(container_scroll, bg=COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_scroll, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg=COLOR_MAIN_BG)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def ajustar_ancho(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", ajustar_ancho)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        items = mostrar_productos() 
        for nombre, descripcion, precio, cant_top in items:
            row_frame = tk.Frame(scrollable_frame, bg="#FFF8F0")
            # fila
            row_frame.pack(fill="x", pady=5, ipadx=5, ipady=5)
            tk.Label(row_frame, text=nombre, font=("Arial", 12, "bold"), width=15, anchor="w", 
                     bg="#FFF8F0", fg="#5D4037").pack(side="left", padx=(0, 10))
            tk.Label(row_frame, text=cant_top, font=("Arial", 12), width=10, anchor="center", 
                     bg="#FFF8F0", fg="#5D4037").pack(side="right", padx=10)
            tk.Label(row_frame, text=f"${precio:.2f}", font=("Arial", 12), width=8, anchor="center",
                     bg="#FFF8F0", fg="#5D4037").pack(side="right", padx=10) 
            tk.Label(row_frame, text=descripcion, font=("Arial", 10), anchor="w", 
                     bg="#FFF8F0", fg="#594A42").pack(side="left", expand=True, fill="x")

    def _mostrar_panel_agregar_producto(self):
        """Muestra la interfaz de agregar producto directamente en el panel principal."""
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_productos) 

        header_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        header_frame.pack(fill="x", pady=10)
        
        tk.Button(header_frame, text="⬅ Volver", bg=COLOR_BTN_BROWN, fg="white",
                  font=("Arial", 10, "bold"), command=self.mostrar_productos).pack(side="left", padx=10)

        tk.Label(header_frame, text="➕ Agregar Nuevo Producto", font=("Arial", 20, "bold"),
                 bg=COLOR_MAIN_BG, fg=COLOR_TEXT).pack(side="left", padx=20)
        
        ttk.Separator(self.main_frame, orient="horizontal").pack(fill="x", padx=30)
        
        form_frame = tk.Frame(self.main_frame, bg=COLOR_SIDEBAR, padx=30, pady=20)
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        # Variables de control
        self.categoria_seleccionada = tk.StringVar(form_frame)
        self.cant_topings_var = tk.StringVar(form_frame, value="0") 
        self.entry_nombre = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_desc = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_precio = tk.Entry(form_frame, font=("Arial", 12))
        self.frame_top = tk.Frame(form_frame, bg=COLOR_SIDEBAR) 
        
        # muestra cosas si es crepa o waffle
        def _mostrar_campo_topings(*args):
            cat = self.categoria_seleccionada.get()
            if "crepa" in cat.lower() or "waffle" in cat.lower():
                self.frame_top.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
            else:
                self.frame_top.grid_remove()
                self.cant_topings_var.set("0")

        # campos del formulario
        categorias_raw = obtener_categorias() 
        categorias = [c['nombre_categoria'] for c in categorias_raw] if categorias_raw else ["Sin Categorías"]

        tk.Label(form_frame, text="1. Categoría:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(5, 5))
        
        if categorias:
             self.categoria_seleccionada.set(categorias[0])

        menu_categoria = ttk.OptionMenu(form_frame, self.categoria_seleccionada, None, *categorias)
        menu_categoria.config(width=25)
        menu_categoria.grid(row=0, column=1, sticky="w", pady=(5, 5), padx=5)
        self.categoria_seleccionada.trace_add("write", _mostrar_campo_topings)
        
        # nombre
        tk.Label(form_frame, text="2. Nombre:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=(10, 5))
        self.entry_nombre.grid(row=1, column=1, sticky="ew", pady=(10, 5), padx=5)
        
        # descripcion
        tk.Label(form_frame, text="3. Descripción:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=(10, 5))
        self.entry_desc.grid(row=2, column=1, sticky="ew", pady=(10, 5), padx=5)

        # precio
        tk.Label(form_frame, text="4. Precio (0.00):", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(10, 5))
        self.entry_precio.grid(row=3, column=1, sticky="ew", pady=(10, 5), padx=5)

        # cantidad de toppings
        tk.Label(self.frame_top, text="5. Cantidad Máx. de Toppings:", bg=COLOR_SIDEBAR, 
                 fg=COLOR_TEXT, font=("Arial", 11, "bold")).pack(side="left", anchor="w")
        
        spinbox_top = tk.Spinbox(self.frame_top, from_=0, to=10, textvariable=self.cant_topings_var, width=5, font=("Arial", 12))
        spinbox_top.pack(side="right", padx=10)
        
        # muestra/oculta el campo condicional al cargar
        _mostrar_campo_topings() 

        tk.Button(self.main_frame, text="💾 Guardar Producto", bg=COLOR_BTN_GREEN, fg="white",
                  font=("Arial", 12, "bold"), command=self.guardar_datos_prod).pack(pady=30)
        
    def guardar_datos_prod(self):
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_desc.get().strip()
        precio_str = self.entry_precio.get().strip()
        cant_top = self.cant_topings_var.get()
        categoria = self.categoria_seleccionada.get()

        if not nombre or not descripcion or not precio_str:
            messagebox.showwarning("Cuidado", "Faltan campos obligatorios.")
            return

        try:
            precio = float(precio_str)
            if precio <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número positivo válido.")
            return
        
        try:
            cant_top_int = int(cant_top)
        except ValueError:
             messagebox.showerror("Error", "La cantidad de toppings debe ser un número entero.")
             return
        
        exito = agregar_nuevo_producto(nombre, descripcion, precio, cant_top_int, categoria)
        
        if exito == "DUPLICADO":
            messagebox.showinfo("Error", f"'{nombre}' Ya está registrado.")
        elif exito:
            messagebox.showinfo("Éxito", f"'{nombre}' agregado correctamente")
            self.mostrar_productos()
        else:
            messagebox.showerror("Error", "No se pudo guardar en la base de datos.")
            
    def panel_funciones_producto(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_productos)

        header_frame = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        header_frame.pack(fill="x", pady=10)
        
        tk.Button(header_frame, text="⬅ Volver", bg=COLOR_BTN_BROWN, fg="white",
                  font=("Arial", 10, "bold"), command=self.mostrar_productos).pack(side="left", padx=10)

        tk.Label(header_frame, text="Gestión de Productos", font=("Arial", 20, "bold"),
                 bg=COLOR_MAIN_BG, fg=COLOR_TEXT).pack(side="left", padx=20)


        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="white", fieldbackground="white", foreground="black",
                        font=("Arial", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#D7C2A8")

        # crear la tabla
        frame_tabla = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=5)

        # columnas (Asegúrate que coincida con el orden de obtener_productos_con_id)
        columns = ("id_prod", "nombre","descripcion","precio", "id_categoria", "cant_top")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=12)
        
        # encabezados
        self.tree.heading("id_prod", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("id_categoria", text="ID Cat.")
        self.tree.heading("cant_top", text="Toppings Máx.")

        # configuración de las columnas (¡CORREGIDO!)
        self.tree.column("id_prod", width=50, anchor="center")
        self.tree.column("nombre", width=150, anchor="w")
        self.tree.column("descripcion", width=250, anchor="w")
        self.tree.column("precio", width=80, anchor="center")
        self.tree.column("id_categoria", width=80, anchor="center")
        self.tree.column("cant_top", width=80, anchor="center")

        # sroll
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # cargar los datos (USANDO LA FUNCIÓN CON ID)
        datos_productos = obtener_productos_con_id()
        for item in datos_productos:
            self.tree.insert("", "end", values=item)

        # botones 
        frame_botones = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        frame_botones.pack(fill="x", pady=20, padx=20)

        tk.Button(frame_botones, text="✏️ Editar datos", 
                  bg="#FFD700", fg="black", font=("Arial", 11, "bold"),
                  padx=15, pady=10, command=self.accion_actualizar_producto).pack(side="left", padx=(0, 20))

        tk.Button(frame_botones, text="🗑️ Eliminar Seleccionado", 
                  bg=COLOR_BTN_RED, fg="white", font=("Arial", 11, "bold"),
                  padx=15, pady=10, command=self.accion_eliminar_producto).pack(side="left")


    def accion_eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un producto de la tabla para eliminarlo.")
            return
        
        item = self.tree.item(seleccion)
        id_prod = item['values'][0]
        nombre = item['values'][1]

        confirmar = messagebox.askyesno("Confirmar Eliminación", 
                                        f"¿Seguro que deseas eliminar el producto '{nombre}'?\nEsta acción es permanente.")
        if confirmar:
            if eliminar_producto_bd(id_prod):
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                self.panel_funciones_producto() # Recargar la vista
            else:
                messagebox.showerror("Error", "No se pudo eliminar de la base de datos.")

    def accion_actualizar_producto(self):
        # ... (Implementación de la ventana de edición, similar a la que revisamos antes)
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un producto para editar sus datos.")
            return

        item = self.tree.item(seleccion)
        # Extraer valores del Treeview
        id_prod, nombre_actual, desc_actual, precio_actual, id_categoria_actual, cant_top_actual = item['values']

        # --- Obtener las categorías (necesario para el OptionMenu) ---
        categorias_raw = obtener_categorias() 
        categorias_nombres = [c['nombre_categoria'] for c in categorias_raw] if categorias_raw else ["Sin Categorías"]
        
        # Buscar el nombre de la categoría actual para mostrarla
        nombre_categoria_actual = next((c['nombre_categoria'] for c in categorias_raw if c['id_categorias'] == id_categoria_actual), categorias_nombres[0] if categorias_nombres else "")

        # --- Creación de la Ventana de Edición ---
        ventana_edit = tk.Toplevel(self.root)
        ventana_edit.title(f"Editar Producto: {nombre_actual}")
        ventana_edit.geometry("450x380")
        ventana_edit.config(bg=COLOR_SIDEBAR)
        ventana_edit.transient(self.root)
        ventana_edit.grab_set()

        form_frame = tk.Frame(ventana_edit, bg=COLOR_SIDEBAR, padx=20, pady=15)
        form_frame.pack(fill="both", expand=True)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        # Variables de Control
        self._nombre_var = tk.StringVar(form_frame, value=nombre_actual)
        self._desc_var = tk.StringVar(form_frame, value=desc_actual)
        self._precio_var = tk.StringVar(form_frame, value=str(precio_actual))
        self._cant_top_var = tk.StringVar(form_frame, value=str(cant_top_actual)) 
        self._categoria_var = tk.StringVar(form_frame, value=nombre_categoria_actual)
        
        frame_top = tk.Frame(form_frame, bg=COLOR_SIDEBAR) 

        def mostrar_campo_topings_edit(*args):
            cat = self._categoria_var.get()
            if "crepa" in cat.lower() or "waffle" in cat.lower():
                frame_top.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
            else:
                frame_top.grid_remove()
                self._cant_top_var.set("0")

        # Categoría
        tk.Label(form_frame, text="Categoría:", bg=COLOR_SIDEBAR, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w", pady=5)
        menu_categoria = ttk.OptionMenu(form_frame, self._categoria_var, None, *categorias_nombres)
        menu_categoria.config(width=25)
        menu_categoria.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self._categoria_var.trace_add("write", mostrar_campo_topings_edit)

        # Nombre
        tk.Label(form_frame, text="Nombre:", bg=COLOR_SIDEBAR, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self._nombre_var, font=("Arial", 12)).grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        # Descripción
        tk.Label(form_frame, text="Descripción:", bg=COLOR_SIDEBAR, fg=COLOR_TEXT).grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self._desc_var, font=("Arial", 12)).grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        # Precio
        tk.Label(form_frame, text="Precio (0.00):", bg=COLOR_SIDEBAR, fg=COLOR_TEXT).grid(row=3, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self._precio_var, font=("Arial", 12)).grid(row=3, column=1, sticky="ew", pady=5, padx=5)
        
        # Cantidad de toppings (Marco condicional)
        tk.Label(frame_top, text="Toppings Máx.:", bg=COLOR_SIDEBAR, fg=COLOR_TEXT).pack(side="left", anchor="w")
        tk.Spinbox(frame_top, from_=0, to=10, textvariable=self._cant_top_var, width=5, font=("Arial", 12)).pack(side="right", padx=10)
        
        mostrar_campo_topings_edit() 

        def guardar_cambio_prod():
            nombre = self._nombre_var.get().strip()
            descripcion = self._desc_var.get().strip()
            precio_str = self._precio_var.get().strip()
            cant_top = self._cant_top_var.get()
            categoria = self._categoria_var.get()

            if not nombre or not descripcion or not precio_str:
                messagebox.showwarning("Cuidado", "Faltan campos obligatorios.", parent=ventana_edit)
                return
            try:
                precio = float(precio_str)
                cant_top_int = int(cant_top)
                if precio <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "El Precio y la Cant. Toppings deben ser números válidos.", parent=ventana_edit)
                return
            
            if actualizar_producto(id_prod, nombre, descripcion, precio, cant_top_int, categoria):
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.", parent=ventana_edit)
                ventana_edit.destroy()
                self.panel_funciones_producto() # Recargar tabla
            else:
                messagebox.showerror("Error", "Fallo al actualizar en la Base de Datos. (Revisa la terminal para detalles)", parent=ventana_edit)

        tk.Button(ventana_edit, text="💾 Guardar Cambios", bg=COLOR_BTN_GREEN, fg="white",
                  font=("Arial", 11, "bold"), command=guardar_cambio_prod).pack(pady=20)
    
    '''REPORTES'''
    
    def mostrar_reportes(self):
        self._limpiar_panel_principal()
        self._resaltar_boton(self.btn_reportes)
        
        tk.Label(self.main_frame, text="Reportes de Venta (Transacciones)", font=("Arial", 24, "bold"),
                 bg=COLOR_MAIN_BG, fg=COLOR_TEXT).pack(side="top", pady=(10, 5))
        
        # Obtener los datos agrupados
        reporte_datos = obtener_reporte_ventas_agrupadas()
        
        if not reporte_datos:
            tk.Label(self.main_frame, text="No hay ventas registradas para mostrar.", font=("Arial", 14), bg=COLOR_MAIN_BG).pack(pady=50)
            return

        # --- Contenedor con Scroll (similar a otras vistas) ---
        scroll_container = tk.Frame(self.main_frame, bg=COLOR_MAIN_BG)
        scroll_container.pack(fill="both", expand=True, padx=30, pady=10)
        
        canvas = tk.Canvas(scroll_container, bg=COLOR_MAIN_BG, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_MAIN_BG)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        
        # --- Mostrar cada grupo de venta (Transacción) ---
        for grupo in reporte_datos:
            # Etiqueta Maestra (Fecha e ID de Ticket)
            frame_transaccion = tk.LabelFrame(scrollable_frame, text=f"Ticket ID: {grupo['id_ticket']} - Fecha: {grupo['fecha']}", 
                                              font=("Arial", 14, "bold"), padx=10, pady=10, bg="#FFF8F0", fg=COLOR_TEXT)
            frame_transaccion.pack(fill="x", pady=10, padx=10)
            
            # Encabezados de la tabla (dentro del LabelFrame)
            header = tk.Frame(frame_transaccion, bg="#EADBC8")
            header.pack(fill="x", pady=(0, 5))
            tk.Label(header, text="ID Línea", width=8, font=("Arial", 10, "bold"), bg="#EADBC8").pack(side="left", padx=(5, 10))
            tk.Label(header, text="Descripción Venta", anchor="w", font=("Arial", 10, "bold"), bg="#EADBC8").pack(side="left", expand=True, fill="x")
            tk.Label(header, text="Total Línea", width=10, font=("Arial", 10, "bold"), bg="#EADBC8").pack(side="right", padx=5)

            # Detalles de cada línea de producto en la transacción
            for detalle in grupo['detalles']:
                frame_detalle = tk.Frame(frame_transaccion, bg="#FFF8F0")
                frame_detalle.pack(fill="x", pady=1)

                tk.Label(frame_detalle, text=detalle['id_linea'], width=8, font=("Arial", 10), bg="#FFF8F0").pack(side="left", padx=(5, 10))
                tk.Label(frame_detalle, text=detalle['descripcion'], anchor="w", font=("Arial", 10), bg="#FFF8F0").pack(side="left", expand=True, fill="x")
                tk.Label(frame_detalle, text=f"${detalle['total_linea']:.2f}", width=10, font=("Arial", 10), bg="#FFF8F0").pack(side="right", padx=5)
                
            # Total del Ticket
            tk.Label(frame_transaccion, text=f"TOTAL DEL TICKET: ${grupo['total_final']:.2f} (Vendedor ID: {grupo['id_vendedor']})", 
                     font=("Arial", 12, "bold"), bg="#EADBC8", fg=COLOR_TEXT, anchor="e").pack(fill="x", pady=(5, 0))

