import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from admin_controller import (actualizar_estatus_topping, estatus_topings,agregar_nuevo_topping, eliminar_topping_bd,actualizar_nombre_topping)
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

