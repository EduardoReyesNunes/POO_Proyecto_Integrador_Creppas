import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# --- IMPORTACIONES NECESARIAS ---
import seller_controller as controller 
import admin_view
# Ya no necesitamos valid_admin aquí, solo el controlador para validar el admin pass

class sellerApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Punto de Venta")
        self.root.geometry("1000x700")
        
        # Configuración visual
        self.bg_color = "#E0C9B6"
        self.root.configure(bg=self.bg_color)
        
        # Estado (Establecido por defecto)
        self.usuario_actual = "Vendedor" # <-- Se inicia con un usuario predeterminado
        self.admin_panel_visible = False
        
        # Cargar recursos
        self.cargar_imagenes()

        # Iniciar Interfaz de Ventas directamente
        self.construir_interfaz_ventas() # <-- Llamada directa a la interfaz

    def cargar_imagenes(self):
        self.icon_gear = None
        ruta_img = os.path.join("img", "ajustes.png")
        try:
            # Si tienes la imagen, se carga
            # NOTA: Usamos Image.LANCZOS en lugar de Image.ANTIALIAS, 
            # ya que ANTIALIAS está obsoleto.
            img = Image.open(ruta_img).resize((30, 30), Image.LANCZOS)
            self.icon_gear = ImageTk.PhotoImage(img)
        except:
            pass
            # print("Advertencia: No se pudo cargar img/ajustes.png")


    # ==========================================
    #           INTERFAZ DE VENTAS (POS)
    # ==========================================
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

        tk.Button(frame_btns, text="PAGAR", **estilo).pack(side="left", padx=5, expand=True)
        tk.Button(frame_btns, text="BORRAR", **estilo).pack(side="left", padx=5, expand=True)
        tk.Button(frame_btns, text="LIMPIAR", **estilo).pack(side="left", padx=5, expand=True)

        # Treeview (Tabla)
        self.tree = ttk.Treeview(self.panel_izq, columns=("cant", "desc", "importe"), show="headings")
        self.tree.heading("cant", text="Cant")
        self.tree.heading("desc", text="Descripción")
        self.tree.heading("importe", text="Importe")
        self.tree.column("cant", width=40, anchor="center")
        self.tree.column("desc", width=150)
        self.tree.column("importe", width=70, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=5)

        tk.Label(self.panel_izq, text="TOTAL: $0.00", font=("Arial", 20, "bold"), bg="#D6BFA8").pack(pady=20)

        # --- PANEL DERECHO (Catálogo) ---
        self.panel_der = tk.Frame(self.root, bg=self.bg_color)
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Barra Superior (Engranaje + Admin)
        self.top_bar = tk.Frame(self.panel_der, bg=self.bg_color)
        self.top_bar.pack(fill="x", pady=(0, 10))

        # Botón Engranaje (Muestra el login de Admin)
        if self.icon_gear:
            btn_gear = tk.Button(self.top_bar, image=self.icon_gear, bg=self.bg_color, bd=0,
                                 command=self.toggle_admin_login)
        else:
            btn_gear = tk.Button(self.top_bar, text="⚙️", font=("Arial", 14), bg=self.bg_color,
                                 command=self.toggle_admin_login)
        btn_gear.pack(side="left")

        # Login Admin Oculto
        self.frame_admin_login = tk.Frame(self.top_bar, bg="white", bd=1, relief="solid")
        tk.Label(self.frame_admin_login, text="Admin Pass:", font=("Arial", 9)).pack(side="left", padx=5)
        self.entry_admin_pass = tk.Entry(self.frame_admin_login, show="*", width=10)
        self.entry_admin_pass.pack(side="left", padx=5)
        tk.Button(self.frame_admin_login, text="Entrar", bg="#ccc", font=("Arial", 8),
                  command=self.abrir_panel_admin).pack(side="left", padx=5)

        # Botón Salir (Cierra la aplicación)
        tk.Button(self.top_bar, text="SALIR ➡️", bg="#E5A586", font=("Arial", 9, "bold"),
                  command=self.cerrar_sesion).pack(side="right")

        # Categorías
        self.frame_cats = tk.Frame(self.panel_der, bg=self.bg_color)
        self.frame_cats.pack(fill="x")

        # Productos
        self.frame_prods = tk.Frame(self.panel_der, bg=self.bg_color, bd=2, relief=tk.SUNKEN)
        self.frame_prods.pack(fill="both", expand=True, pady=5)

        # Cargar datos iniciales desde el controller
        self.cargar_categorias()

    # ==========================================
    #           LÓGICA INTERNA
    # ==========================================
    def toggle_admin_login(self):
        if not self.admin_panel_visible:
            self.frame_admin_login.pack(side="left", padx=10)
            self.entry_admin_pass.focus()
            self.admin_panel_visible = True
        else:
            self.frame_admin_login.pack_forget()
            self.admin_panel_visible = False

    def abrir_panel_admin(self):
        password = self.entry_admin_pass.get().strip()
        
        # Verificamos si es admin usando el controller (usando un usuario placeholder para Admin)
        if controller.validar_login("ADMIN", password): 
            self.root.destroy()
            root_admin = tk.Tk()
            admin_view.adminapp(root_admin) 
            root_admin.mainloop()
        else:
            messagebox.showerror("Error", "Contraseña de administrador incorrecta")

    def cerrar_sesion(self):
        """Cierra la aplicación (no hay pantalla de login a la que volver)."""
        self.root.destroy() # <-- Cierra la ventana principal

    def cargar_categorias(self):
        # USAMOS EL CONTROLLER
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

        # USAMOS EL CONTROLLER
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
        # Agrega fila al ticket (solo visual por ahora)
        self.tree.insert("", "end", values=(1, producto['nombre'], f"${producto['precio']:.2f}"))