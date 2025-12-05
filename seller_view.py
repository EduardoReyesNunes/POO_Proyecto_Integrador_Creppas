import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import seller_controller as controller 
import admin_view
from decimal import Decimal, InvalidOperation # Importar Decimal para manejo de moneda

# Colores Suaves (Mantenidos desde admin_view para consistencia)
COLOR_MAIN_BG = "#EAE4D9"      
COLOR_SIDEBAR_BG = "#F8F4E8"   
COLOR_BTN_BASE = "#E5A586"     # Naranja/Marrón para botones principales
COLOR_BTN_PAGAR = "#3CB371"    # Verde Suave para pagar
COLOR_TEXT_DARK = "#4A403F"    

class sellerApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Punto de Venta")
        self.root.geometry("1000x700")
        self.root.state('zoomed') # pantalla completa
        self.bg_color = COLOR_MAIN_BG # Usar el color principal
        self.root.configure(bg=self.bg_color)
        self.usuario_actual = "Alexa"
        self.admin_panel_visible = False
        self.id_vendedor = 2 
        self.carrito_items = []
        # cargar iconos
        self.cargar_imagenes()
        
        # Aplicar estilo ttk moderno (Para Treeview)
        style = ttk.Style()
        try:
             style.theme_use('adapta') 
        except Exception:
             style.theme_use('clam')

        # iniciar ui
        self.construir_interfaz_ventas() 

    def cargar_imagenes(self):
        self.icon_gear = None
        ruta_img = os.path.join("img", "ajustes.png")
        try:
            img = Image.open(ruta_img).resize((30, 30), Image.LANCZOS) 
            self.icon_gear = ImageTk.PhotoImage(img)
        except:
            pass
           
    def construir_interfaz_ventas(self):
        self.root.title(f"Punto de Venta - Atendiendo: {self.usuario_actual}")
        
        # grid
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=7)
        self.root.rowconfigure(0, weight=1)

        # --- PANEL TICKET (IZQUIERDA) ---
        self.panel_izq = tk.Frame(self.root, bg=COLOR_SIDEBAR_BG, bd=0, relief=tk.FLAT)
        self.panel_izq.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # botones ticket
        frame_btns = tk.Frame(self.panel_izq, bg=COLOR_SIDEBAR_BG)
        frame_btns.pack(fill="x", pady=10)
        
        # Estilo base para todos los botones, EXCLUYENDO BG
        estilo_base = {"fg": "white", "font": ("Arial", 11, "bold"), "width": 10, "bd": 0} 

        # PAGAR: Pasa su propio BG
        tk.Button(frame_btns, text="PAGAR", bg=COLOR_BTN_PAGAR, **estilo_base, command=self.procesar_pago).pack(side="left", padx=5, expand=True)
        # BORRAR: Pasa BG desde COLOR_BTN_BASE
        tk.Button(frame_btns, text="BORRAR", bg=COLOR_BTN_BASE, **estilo_base, command=self.borrar_item_ticket).pack(side="left", padx=5, expand=True)
        # LIMPIAR: Pasa BG desde COLOR_BTN_BASE
        tk.Button(frame_btns, text="LIMPIAR", bg=COLOR_BTN_BASE, **estilo_base, command=self.limpiar_ticket).pack(side="left", padx=5, expand=True)

        # tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background=COLOR_BTN_BASE, foreground="white") # Encabezado destacado
        style.configure("Treeview", font=("Arial", 10))
        
        self.tree = ttk.Treeview(self.panel_izq, columns=("cant", "desc", "importe"), show="headings")
        self.tree.heading("cant", text="Cant")
        self.tree.heading("desc", text="Descripción")
        self.tree.heading("importe", text="Importe")
        self.tree.column("cant", width=50, anchor="center") 
        self.tree.column("desc", width=200) 
        self.tree.column("importe", width=80, anchor="e") 
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Total
        self.lbl_total = tk.Label(self.panel_izq, text="TOTAL: $0.00", font=("Arial", 30, "bold"), bg=COLOR_SIDEBAR_BG, fg=COLOR_TEXT_DARK) 
        self.lbl_total.pack(pady=20)

        # catalogo (DERECHA)
        self.panel_der = tk.Frame(self.root, bg=self.bg_color)
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        # top bar
        self.top_bar = tk.Frame(self.panel_der, bg=self.bg_color)
        self.top_bar.pack(fill="x", pady=(0, 10))

        # boton admin
        btn_estilo_plano = {"bg": self.bg_color, "bd": 0, "activebackground": self.bg_color}
        
        if self.icon_gear:
            btn_gear = tk.Button(self.top_bar, image=self.icon_gear, **btn_estilo_plano,
                                 command=self.toggle_admin_login)
        else:
            btn_gear = tk.Button(self.top_bar, text="⚙️", font=("Arial", 16), **btn_estilo_plano, 
                                 command=self.toggle_admin_login)
        btn_gear.pack(side="left")

        # login oculto
        self.frame_admin_login = tk.Frame(self.top_bar, bg=COLOR_SIDEBAR_BG, bd=1, relief=tk.FLAT)
        tk.Label(self.frame_admin_login, text="Admin Pass:", font=("Arial", 10), bg=COLOR_SIDEBAR_BG).pack(side="left", padx=5)
        self.entry_admin_pass = tk.Entry(self.frame_admin_login, show="*", width=12) 
        self.entry_admin_pass.pack(side="left", padx=5)
        tk.Button(self.frame_admin_login, text="Entrar", bg=COLOR_BTN_BASE, fg="white", font=("Arial", 9, "bold"), bd=0,
                  command=self.abrir_panel_admin).pack(side="left", padx=5)

        # salir
        tk.Button(self.top_bar, text="SALIR ➡️", bg=COLOR_BTN_BASE, fg="white", font=("Arial", 11, "bold"), 
                  command=self.cerrar_sesion, bd=0).pack(side="right")

        # categorias
        self.frame_cats = tk.Frame(self.panel_der, bg=self.bg_color)
        self.frame_cats.pack(fill="x")

        # --- CONTENEDOR PRODUCTOS CON SCROLL ---
        self.frame_prods_container = tk.Frame(self.panel_der, bg=self.bg_color, bd=0, relief=tk.FLAT)
        self.frame_prods_container.pack(fill="both", expand=True, pady=5)
        
        # canvas para scroll
        self.canvas_prods = tk.Canvas(self.frame_prods_container, bg=self.bg_color, highlightthickness=0)
        self.scrollbar_prods = ttk.Scrollbar(self.frame_prods_container, orient="vertical", command=self.canvas_prods.yview)
        
        self.frame_prods = tk.Frame(self.canvas_prods, bg=self.bg_color) # contenedor de botones

        self.canvas_prods.pack(side="left", fill="both", expand=True)
        self.scrollbar_prods.pack(side="right", fill="y")
        
        self.canvas_prods.configure(yscrollcommand=self.scrollbar_prods.set)
        
        # configurar scroll
        self.frame_prods.bind(
            "<Configure>",
            lambda e: self.canvas_prods.configure(
                scrollregion=self.canvas_prods.bbox("all")
            )
        )
        # Aquí se guarda el ID de la ventana dentro del Canvas
        self.window_id = self.canvas_prods.create_window((0, 0), window=self.frame_prods, anchor="nw")
        
        # ajustar ancho
        def ajustar_ancho(event):
            # Usar el ID guardado para ajustar el ancho
            self.canvas_prods.itemconfig(self.window_id, width=event.width)
        
        self.canvas_prods.bind('<Configure>', ajustar_ancho)
        # --------------------------------------------------------------------------------

        # cargar categorias
        self.cargar_categorias()

    def cargar_categorias(self):
        cats = controller.obtener_categorias()
        if not cats: return

        for i, cat in enumerate(cats):
            # Botones de categoría estilo modernizado
            btn = tk.Button(self.frame_cats, text=cat['nombre_categoria'], 
                            bg=COLOR_BTN_BASE, fg="white", bd=0,
                            font=("Arial", 11, "bold"), 
                            command=lambda id_c=cat['id_categorias']: self.cargar_productos(id_c))
            btn.pack(side="left", fill="y", padx=5, ipady=8) 
            if i == 0: self.cargar_productos(cat['id_categorias'])

    def cargar_productos(self, id_categoria):
        # limpiar productos
        for w in self.frame_prods.winfo_children(): w.destroy()
        productos = controller.obtener_productos_por_categoria(id_categoria)
        
        row, col = 0, 0
        max_cols = 5 

        for prod in productos:
            texto = f"{prod['nombre']}\n\n${prod['precio']}"
            # Botones de Producto estilo modernizado
            btn = tk.Button(self.frame_prods, text=texto, bg=COLOR_SIDEBAR_BG, fg=COLOR_TEXT_DARK,
                            width=18, height=6, wraplength=150, font=("Arial", 10, "bold"), bd=1, relief=tk.FLAT, highlightbackground=COLOR_BTN_BASE, highlightthickness=1, 
                            command=lambda p=prod: self.agregar_al_ticket(p))
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew") 

            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        for i in range(max_cols): self.frame_prods.columnconfigure(i, weight=1)
        
        # actualizar scroll
        self.frame_prods.update_idletasks()
        self.canvas_prods.config(scrollregion=self.canvas_prods.bbox("all"))

    def toggle_admin_login(self):
        if not self.admin_panel_visible:
            self.frame_admin_login.pack(side="left", padx=10)
            self.entry_admin_pass.focus()
            self.admin_panel_visible = True
        else:
            self.frame_admin_login.pack_forget()
            self.admin_panel_visible = False

    # validar admin
    def abrir_panel_admin(self):
        password = self.entry_admin_pass.get().strip()
        if controller.validar_login("ADMIN", password): 
            self.root.destroy()
            root_admin = tk.Tk()
            admin_view.adminapp(root_admin) 
            root_admin.mainloop()
        else:
            messagebox.showerror("Error", "Contraseña de administrador incorrecta")

    def cerrar_sesion(self):
        self.root.destroy() 

    def agregar_al_ticket(self, producto):
        es_modificable = (producto.get('id_categoria') in [4, 5] and producto.get('cant_top', 0) > 0)
        
        # Asegurarse de que el precio sea Decimal para cálculos
        try:
            precio_decimal = Decimal(str(producto['precio']))
        except InvalidOperation:
            messagebox.showerror("Error de Precio", f"El precio del producto '{producto['nombre']}' no es válido.")
            return

        if es_modificable:
            self.mostrar_panel_topings(producto)
        else:
            item_venta = {
                'id_prod': producto['id_producto'],
                'nombre': producto['nombre'],
                'precio': precio_decimal, # Guardado como Decimal
                'precio_unitario': precio_decimal, # Guardado como Decimal
                'cantidad': 1,
                'total': precio_decimal, # Guardado como Decimal
                'toppings': [],
                'toppings_str': "",
                'producto_descripcion': producto['nombre']
            }
            self.carrito_items.append(item_venta)
            self._actualizar_vista_ticket()

    def mostrar_panel_topings(self, producto):
        cant_max = producto.get('cant_top', 0)
        toppings_disp = controller.obtener_toppings_habilitados() 
        
        if cant_max == 0 or not toppings_disp:
            messagebox.showwarning("Atención", f"'{producto['nombre']}' no tiene toppings configurados o habilitados.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Toppings para {producto['nombre']} (Máx. {cant_max})")
        win.geometry("500x650") 
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text=f"Selecciona hasta {cant_max} toppings:", font=("Arial", 14, "bold")).pack(pady=15) 
        
        scroll_frame = tk.Frame(win)
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=10) 
        
        selected_toppings = {} 
        selected_count = tk.IntVar(value=0)
        
        # canvas para scroll
        canvas = tk.Canvas(scroll_frame)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        
        content_frame = tk.Frame(canvas)

        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        window_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ajustar ancho
        def ajustar_ancho_top(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind('<Configure>', ajustar_ancho_top)

        def actualizar_conteo(id_top):
            current_count = selected_count.get()
            if selected_toppings[id_top].get() == 1:
                # si marca
                if current_count >= cant_max:
                    messagebox.showwarning("Límite Alcanzado", f"Solo puedes seleccionar {cant_max} toppings.", parent=win)
                    selected_toppings[id_top].set(0) # revertir
                else:
                    selected_count.set(current_count + 1)
            else:
                # si desmarca
                selected_count.set(current_count - 1)

        # checkbuttons
        for top in toppings_disp:
            var = tk.IntVar(value=0)
            selected_toppings[top['id_top']] = var
            
            # Checkbutton con estilo plano y fondo claro
            chk = tk.Checkbutton(content_frame, text=top['nombre'], variable=var, 
                                 font=("Arial", 12), anchor="w", width=40, bg="white", bd=0, relief=tk.FLAT) 
            
            chk.config(command=lambda id_t=top['id_top']: actualizar_conteo(id_t))
            
            chk.pack(fill="x", pady=3) 

        def confirmar_seleccion():
            if selected_count.get() == 0 and cant_max > 0:
                 if not messagebox.askyesno("Confirmar", "No has seleccionado ningún topping. ¿Deseas agregar el producto sin ellos?", parent=win):
                    return

            toppings_final = []
            toppings_nombres = []
            
            for id_top, var in selected_toppings.items():
                if var.get() == 1:
                    nombre = next(t['nombre'] for t in toppings_disp if t['id_top'] == id_top)
                    toppings_final.append(id_top)
                    toppings_nombres.append(nombre)
            toppings_str_final = ", ".join(toppings_nombres)
            desc_completa = producto['nombre'] + (f" ({toppings_str_final})" if toppings_nombres else "")

            # Asegurarse de que el precio sea Decimal
            try:
                precio_decimal = Decimal(str(producto['precio']))
            except InvalidOperation:
                messagebox.showerror("Error de Precio", f"El precio del producto '{producto['nombre']}' no es válido.")
                win.destroy()
                return

            item_venta = {
                'id_prod': producto['id_producto'],
                'nombre': producto['nombre'],
                'precio': precio_decimal, # Guardado como Decimal
                'precio_unitario': precio_decimal, # Guardado como Decimal
                'cantidad': 1,
                'total': precio_decimal, # Guardado como Decimal
                'toppings': toppings_final,
                'toppings_str': toppings_str_final,
                'producto_descripcion': desc_completa 
            }
            
            self.carrito_items.append(item_venta)
            self._actualizar_vista_ticket()
            win.destroy()


        tk.Button(win, text="✅ Confirmar Selección", bg=COLOR_BTN_PAGAR, fg="white", bd=0,
                  font=("Arial", 12, "bold"), command=confirmar_seleccion).pack(pady=20) 

    def _actualizar_vista_ticket(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        total_acumulado = Decimal(0) # Iniciar con Decimal(0)
        for item in self.carrito_items:
            # item['total'] ya es Decimal
            self.tree.insert("", "end", values=(
                item['cantidad'], 
                item['producto_descripcion'],
                f"{item['total']:.2f}"
            ))

            total_acumulado += item['total']
            
        self.lbl_total.config(text=f"TOTAL: ${total_acumulado:.2f}")

    def limpiar_ticket(self):
        self.carrito_items = []
        self._actualizar_vista_ticket()

    def borrar_item_ticket(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un artículo para borrar.")
            return
        item_index = self.tree.index(seleccion)
        if 0 <= item_index < len(self.carrito_items):
            del self.carrito_items[item_index]

        self._actualizar_vista_ticket()
        
    def procesar_pago(self):
        if not self.carrito_items:
            messagebox.showwarning("Atención", "El carrito está vacío. Agrega productos para pagar.")
            return

        # El total es la suma de los Decimals en carrito_items
        total_venta = sum(item['total'] for item in self.carrito_items)
        
        # popup pago/cambio
        self.mostrar_popup_pago(total_venta)

    def mostrar_popup_pago(self, total_venta):
        
        win_pago = tk.Toplevel(self.root)
        win_pago.title("Procesar Pago")
        win_pago.geometry("350x250")
        win_pago.config(bg=COLOR_SIDEBAR_BG)
        win_pago.transient(self.root)
        win_pago.grab_set()

        tk.Label(win_pago, text=f"Total a Pagar: ${total_venta:.2f}", 
                 font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR_BG).pack(pady=15)

        tk.Label(win_pago, text="Monto Recibido:", font=("Arial", 12), bg=COLOR_SIDEBAR_BG).pack()
        entry_pago = tk.Entry(win_pago, font=("Arial", 14), justify='right')
        entry_pago.pack(pady=5, padx=20)
        entry_pago.focus()
        
        # validar numeros
        vcmd = (win_pago.register(self.validar_decimal), '%P')
        entry_pago.config(validate='key', validatecommand=vcmd)


        lbl_cambio = tk.Label(win_pago, text="Cambio: $0.00", font=("Arial", 14, "bold"), bg=COLOR_SIDEBAR_BG, fg="#DC143C")
        lbl_cambio.pack(pady=10)

        def calcular_cambio(*args):
            try:
                # Convertir el monto de la caja de texto a Decimal
                monto_recibido = Decimal(entry_pago.get() or 0)
            except InvalidOperation:
                monto_recibido = Decimal(0)

            # total_venta ya es Decimal, así que la resta es válida.
            if monto_recibido < total_venta:
                lbl_cambio.config(text="Falta Monto", fg="#DC143C")
                btn_confirmar.config(state=tk.DISABLED)
            else:
                cambio = monto_recibido - total_venta
                lbl_cambio.config(text=f"Cambio: ${cambio:.2f}", fg=COLOR_BTN_PAGAR)
                btn_confirmar.config(state=tk.NORMAL)

        entry_pago.bind("<KeyRelease>", calcular_cambio)
        
        def confirmar_transaccion():
            try:
                # Convertir a Decimal para la operación final
                monto_recibido = Decimal(entry_pago.get())
            except InvalidOperation:
                 messagebox.showerror("Error", "Monto de pago no válido.")
                 return

            cambio = monto_recibido - total_venta
            
            # si el pago cubre el total
            if cambio >= 0:
                self.registrar_transaccion(win_pago, total_venta, cambio)

        btn_confirmar = tk.Button(win_pago, text="Confirmar Venta", bg=COLOR_BTN_PAGAR, fg="white", bd=0,
                                  font=("Arial", 11, "bold"), command=confirmar_transaccion, state=tk.DISABLED)
        btn_confirmar.pack(pady=15)
        
        # chequeo inicial
        calcular_cambio()
    
    def validar_decimal(self, P):
        """permite solo números y un punto decimal."""
        if P == "": return True 
        try:
            # Usar Decimal para validar, que es más estricto que float
            Decimal(P) 
            return True
        except InvalidOperation:
            return False

    def registrar_transaccion(self, win_pago, total_venta, cambio):
        detalles = []
        for item in self.carrito_items:
            detalles.append({
                'id_prod': item['id_prod'],
                'cantidad': item['cantidad'],
                # Convertir Decimal a float (o str) si el controller/DB no maneja Decimals. 
                # Si la base de datos sí maneja precisión, deja item['precio'].
                'precio_unitario': float(item['precio']), 
                'producto_descripcion': item['producto_descripcion']
            })

        # Convertir total_venta y cambio a float para pasarlos al controller si es necesario
        total_venta_float = float(total_venta)
        
        if controller.registrar_venta(self.id_vendedor, detalles, total_venta_float):
            messagebox.showinfo("Éxito", f"Venta registrada correctamente.\nCambio a dar: ${cambio:.2f}")
            self.limpiar_ticket()
            win_pago.destroy()
        else:
            messagebox.showerror("Error", "Error al registrar la venta en la base de datos.")
            win_pago.destroy()