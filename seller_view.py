import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import seller_controller as controller 
import admin_view

class sellerApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Punto de Venta")
        self.root.geometry("1000x700")
        self.bg_color = "#E0C9B6"
        self.root.configure(bg=self.bg_color)
        self.usuario_actual = "Alexa"
        self.admin_panel_visible = False
        self.id_vendedor = 2 
        self.carrito_items = []
        # carga la imagen
        self.cargar_imagenes()

        # Iniciar Interfaz de Ventas directamente
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
        
        # Grid: Columna 0 (Ticket 30%), Columna 1 (Catálogo 70%)
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=7)
        self.root.rowconfigure(0, weight=1)

        # --- PANEL IZQUIERDO (Ticket) ---
        self.panel_izq = tk.Frame(self.root, bg="#D6BFA8", bd=2, relief=tk.RIDGE)
        self.panel_izq.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Botones Ticket
        frame_btns = tk.Frame(self.panel_izq, bg="#D6BFA8")
        frame_btns.pack(fill="x", pady=10)
        estilo = {"bg": "#E5A586", "font": ("Arial", 9, "bold"), "width": 10}

        tk.Button(frame_btns, text="PAGAR", **estilo, command=self.procesar_pago).pack(side="left", padx=5, expand=True)
        tk.Button(frame_btns, text="BORRAR", **estilo, command=self.borrar_item_ticket).pack(side="left", padx=5, expand=True)
        tk.Button(frame_btns, text="LIMPIAR", **estilo, command=self.limpiar_ticket).pack(side="left", padx=5, expand=True)

        # tabla
        self.tree = ttk.Treeview(self.panel_izq, columns=("cant", "desc", "importe"), show="headings")
        self.tree.heading("cant", text="Cant")
        self.tree.heading("desc", text="Descripción")
        self.tree.heading("importe", text="Importe")
        self.tree.column("cant", width=40, anchor="center")
        self.tree.column("desc", width=150)
        self.tree.column("importe", width=70, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=5)

        self.lbl_total = tk.Label(self.panel_izq, text="TOTAL: $0.00", font=("Arial", 20, "bold"), bg="#D6BFA8")
        self.lbl_total.pack(pady=20)

        # catalogo
        self.panel_der = tk.Frame(self.root, bg=self.bg_color)
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # engranaje y admin
        self.top_bar = tk.Frame(self.panel_der, bg=self.bg_color)
        self.top_bar.pack(fill="x", pady=(0, 10))

        # boton que oculta el login
        if self.icon_gear:
            btn_gear = tk.Button(self.top_bar, image=self.icon_gear, bg=self.bg_color, bd=0,
                                 command=self.toggle_admin_login)
        else:
            btn_gear = tk.Button(self.top_bar, text="⚙️", font=("Arial", 14), bg=self.bg_color,
                                 command=self.toggle_admin_login)
        btn_gear.pack(side="left")

        # login oculto
        self.frame_admin_login = tk.Frame(self.top_bar, bg="white", bd=1, relief="solid")
        tk.Label(self.frame_admin_login, text="Admin Pass:", font=("Arial", 9)).pack(side="left", padx=5)
        self.entry_admin_pass = tk.Entry(self.frame_admin_login, show="*", width=10)
        self.entry_admin_pass.pack(side="left", padx=5)
        tk.Button(self.frame_admin_login, text="Entrar", bg="#ccc", font=("Arial", 8),
                  command=self.abrir_panel_admin).pack(side="left", padx=5)

        # salir
        tk.Button(self.top_bar, text="SALIR ➡️", bg="#E5A586", font=("Arial", 9, "bold"),
                  command=self.cerrar_sesion).pack(side="right")

        # categorias
        self.frame_cats = tk.Frame(self.panel_der, bg=self.bg_color)
        self.frame_cats.pack(fill="x")

        # productos
        self.frame_prods = tk.Frame(self.panel_der, bg=self.bg_color, bd=2, relief=tk.SUNKEN)
        self.frame_prods.pack(fill="both", expand=True, pady=5)

        # carga las categorias
        self.cargar_categorias()

    def toggle_admin_login(self):
        if not self.admin_panel_visible:
            self.frame_admin_login.pack(side="left", padx=10)
            self.entry_admin_pass.focus()
            self.admin_panel_visible = True
        else:
            self.frame_admin_login.pack_forget()
            self.admin_panel_visible = False

    # valida al admin
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

    def cargar_categorias(self):
        cats = controller.obtener_categorias()
        if not cats: return

        for i, cat in enumerate(cats):
            btn = tk.Button(self.frame_cats, text=cat['nombre_categoria'], 
                            bg="#E5A586", font=("Arial", 10, "bold"),
                            command=lambda id_c=cat['id_categorias']: self.cargar_productos(id_c))
            btn.pack(side="left", fill="y", padx=2, ipady=5)
            if i == 0: self.cargar_productos(cat['id_categorias'])

    def cargar_productos(self, id_categoria):
        for w in self.frame_prods.winfo_children(): w.destroy()
        productos = controller.obtener_productos_por_categoria(id_categoria)
        
        row, col = 0, 0
        max_cols = 4 

        for prod in productos:
            texto = f"{prod['nombre']}\n\n${prod['precio']}"
            btn = tk.Button(self.frame_prods, text=texto, bg="#D6BFA8",
                            width=15, height=5, wraplength=120, font=("Arial", 9, "bold"),
                            command=lambda p=prod: self.agregar_al_ticket(p))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        for i in range(max_cols): self.frame_prods.columnconfigure(i, weight=1)

    def agregar_al_ticket(self, producto):
        es_modificable = (producto.get('id_categoria') in [4, 5] and producto.get('cant_top', 0) > 0)
        
        if es_modificable:
            self.mostrar_panel_topings(producto)
        else:
            item_venta = {
                'id_prod': producto['id_producto'],
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'precio_unitario': producto['precio'],
                'cantidad': 1,
                'total': producto['precio'],
                'toppings': [],
                'toppings_str': "",
                'producto_descripcion': producto['nombre']
            }
            self.carrito_items.append(item_venta)
            self._actualizar_vista_ticket()

    def mostrar_panel_topings(self, producto):
        cant_max = producto.get('cant_top', 0)
        # Usamos la nueva función del controller
        toppings_disp = controller.obtener_toppings_habilitados() 
        
        if cant_max == 0 or not toppings_disp:
            messagebox.showwarning("Atención", f"'{producto['nombre']}' no tiene toppings configurados o habilitados.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Toppings para {producto['nombre']} (Máx. {cant_max})")
        win.geometry("400x600")
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text=f"Selecciona hasta {cant_max} toppings:", font=("Arial", 12, "bold")).pack(pady=10)
        
        scroll_frame = tk.Frame(win)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        selected_toppings = {} # {id_top: tk.IntVar}
        selected_count = tk.IntVar(value=0)
        
        content_frame = tk.Frame(scroll_frame)
        content_frame.pack(fill="both", expand=True)

        def actualizar_conteo(id_top):
            current_count = selected_count.get()
            if selected_toppings[id_top].get() == 1:
                # Si marca
                if current_count >= cant_max:
                    messagebox.showwarning("Límite Alcanzado", f"Solo puedes seleccionar {cant_max} toppings.", parent=win)
                    selected_toppings[id_top].set(0) # Revierte
                else:
                    selected_count.set(current_count + 1)
            else:
                # Si desmarca
                selected_count.set(current_count - 1)

        # Crear Checkbuttons para cada topping
        for top in toppings_disp:
            var = tk.IntVar(value=0)
            selected_toppings[top['id_top']] = var
            
            chk = tk.Checkbutton(content_frame, text=top['nombre'], variable=var, 
                                 font=("Arial", 11), anchor="w", width=30)
            
            chk.config(command=lambda id_t=top['id_top']: actualizar_conteo(id_t))
            
            chk.pack(fill="x", pady=2)

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

            # Construye el item de venta
            toppings_str_final = ", ".join(toppings_nombres)
            desc_completa = producto['nombre'] + (f" ({toppings_str_final})" if toppings_nombres else "")

            item_venta = {
                'id_prod': producto['id_producto'],
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'precio_unitario': producto['precio'],
                'cantidad': 1,
                'total': producto['precio'], 
                'toppings': toppings_final,
                'toppings_str': toppings_str_final,
                'producto_descripcion': desc_completa # Descripción para la BD y la vista
            }
            
            self.carrito_items.append(item_venta)
            self._actualizar_vista_ticket()
            win.destroy()


        tk.Button(win, text="✅ Confirmar Selección", bg="#32CD32", fg="white", 
                  font=("Arial", 11, "bold"), command=confirmar_seleccion).pack(pady=15)

    def _actualizar_vista_ticket(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        total_acumulado = 0
        
        # Recarga los items del carrito y calcula el total
        for item in self.carrito_items:
            # item['producto_descripcion'] contiene Nombre + (Toppings)
            
            self.tree.insert("", "end", values=(
                item['cantidad'], 
                item['producto_descripcion'], # Muestra la descripción completa
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

        # Obtiene el índice del item seleccionado
        item_index = self.tree.index(seleccion)

        # Elimina el item de la lista de datos reales (carrito_items)
        if 0 <= item_index < len(self.carrito_items):
            del self.carrito_items[item_index]
        
        # Actualiza la vista
        self._actualizar_vista_ticket()
        
    def procesar_pago(self):
        if not self.carrito_items:
            messagebox.showwarning("Atención", "El carrito está vacío. Agrega productos para pagar.")
            return

        total_venta = sum(item['total'] for item in self.carrito_items)
        
        if not messagebox.askyesno("Confirmar Pago", 
                                   f"¿Confirmar el pago por un TOTAL de ${total_venta:.2f}?", 
                                   parent=self.root):
            return
        
        # Prepara los datos del carrito para el controlador
        detalles = []
        for item in self.carrito_items:
            detalles.append({
                'id_prod': item['id_prod'],
                'cantidad': item['cantidad'],
                'precio_unitario': item['precio'], # El precio unitario base
                'producto_descripcion': item['producto_descripcion']
            })

        # Registrar la venta usando el ID del vendedor y el total final
        if controller.registrar_venta(self.id_vendedor, detalles, total_venta):
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
            self.limpiar_ticket()
        else:
            messagebox.showerror("Error", "Error al registrar la venta en la base de datos.")