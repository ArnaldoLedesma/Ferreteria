import customtkinter as ctk

from tkinter import ttk, filedialog
from CTkMessagebox import CTkMessagebox  # libreria instalada por posibles errores al ejecutar (para mostrar los cuadros "ERROR" "ATENCION")
from database.conexion_db import ConexionDB


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = ConexionDB()

        self.title("Ferretería // Gestión de Productos")
        self.geometry("1300x680")
        self.configure(fg_color="#3C3C3C")
        # self.iconbitmap("icono.ico")

        # ---- Banner superior con el nombre del sistema ----
        banner = ctk.CTkFrame(self, fg_color="#2E7D32", height=70, corner_radius=0)
        banner.pack(fill="x", side="top")
        banner.pack_propagate(False)

        ctk.CTkLabel(
            banner, text="FERRETERÍA", font=ctk.CTkFont(size=26, weight="bold"), text_color="white"
        ).pack(side="left", padx=(25, 5), pady=10)
        ctk.CTkLabel(
            banner, text="Gestión de Productos", font=ctk.CTkFont(size=14), text_color="#DFF3DF"
        ).pack(side="left", padx=(0, 10), pady=(22, 0))

        # ---- Buscador, dentro del banner, pegado a la derecha ----
        self.entry_buscar = ctk.CTkEntry(
            banner, placeholder_text="Buscar producto...", width=240,
            fg_color="#1B5E20", text_color="white", placeholder_text_color="#DFF3DF",
            border_color="white", border_width=1
        )
        self.entry_buscar.pack(side="right", padx=25)
        self.entry_buscar.bind("<KeyRelease>", self.buscar_producto)

        # ---- Contenedor general del formulario (debajo del banner) ----
        contenedor = ctk.CTkFrame(self, fg_color="#3C3C3C")
        contenedor.pack(fill="x", padx=20, pady=(15, 5))

        # ---- Bloque: datos del producto (CRUD) ----
        frame_datos = ctk.CTkFrame(contenedor, fg_color="#333333", corner_radius=10)
        frame_datos.pack(side="left", padx=(0, 15), pady=5, fill="y")

        ctk.CTkLabel(
            frame_datos, text="DATOS DEL PRODUCTO", font=ctk.CTkFont(size=13, weight="bold"), text_color="#8BC34A"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 8), padx=10, sticky="w")

        campo_kwargs = dict(fg_color="#4A4A4A", text_color="white", placeholder_text_color="#B0B0B0", width=190)

        self.entry_codigo = ctk.CTkEntry(frame_datos, placeholder_text="Código", **campo_kwargs)
        self.entry_codigo.grid(row=1, column=0, padx=10, pady=5)

        self.entry_proveedor = ctk.CTkEntry(frame_datos, placeholder_text="Proveedor", **campo_kwargs)
        self.entry_proveedor.grid(row=1, column=1, padx=10, pady=5)

        self.entry_nombre = ctk.CTkEntry(frame_datos, placeholder_text="Nombre del producto", **campo_kwargs)
        self.entry_nombre.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.entry_precio_lista = ctk.CTkEntry(frame_datos, placeholder_text="Precio Lista", **campo_kwargs)
        self.entry_precio_lista.grid(row=3, column=0, padx=10, pady=5)

        self.entry_precio_civa = ctk.CTkEntry(frame_datos, placeholder_text="Precio C/IVA", **campo_kwargs)
        self.entry_precio_civa.grid(row=3, column=1, padx=10, pady=5)

        self.entry_stock = ctk.CTkEntry(frame_datos, placeholder_text="Stock", **campo_kwargs)
        self.entry_stock.grid(row=4, column=0, padx=10, pady=(5, 12))

        # ---- Bloque: acciones CRUD ----
        frame_acciones = ctk.CTkFrame(contenedor, fg_color="#333333", corner_radius=10)
        frame_acciones.pack(side="left", padx=(0, 15), pady=5, fill="y")

        ctk.CTkLabel(
            frame_acciones, text="ACCIONES", font=ctk.CTkFont(size=13, weight="bold"), text_color="#8BC34A"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 8), padx=10, sticky="w")

        boton_kwargs = dict(fg_color="#45B34B", hover_color="#1B5E20", width=140)

        ctk.CTkButton(frame_acciones, text="Agregar", command=self.agregar, **boton_kwargs).grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkButton(frame_acciones, text="Modificar", command=self.modificar, **boton_kwargs).grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(frame_acciones, text="Eliminar", command=self.eliminar, **boton_kwargs).grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkButton(frame_acciones, text="Limpiar", command=self.limpiar_campos, **boton_kwargs).grid(row=2, column=1, padx=10, pady=(5, 12))

        # ---- Bloque: importar precios por proveedor ----
        frame_importar = ctk.CTkFrame(contenedor, fg_color="#333333", corner_radius=10)
        frame_importar.pack(side="left", padx=(0, 15), pady=5, fill="y")

        ctk.CTkLabel(
            frame_importar, text="ACTUALIZAR PRECIOS (CSV)", font=ctk.CTkFont(size=13, weight="bold"), text_color="#8BC34A"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 8), padx=10, sticky="w")

        boton_importar_kwargs = dict(fg_color="#2E7D32", hover_color="#1B5E20", width=140)

        ctk.CTkButton(frame_importar, text="Actualizar POL", command=self.actualizar_pol, **boton_importar_kwargs).grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkButton(frame_importar, text="Actualizar FGP", command=self.actualizar_fgp, **boton_importar_kwargs).grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(frame_importar, text="Actualizar DAY", command=self.actualizar_day, **boton_importar_kwargs).grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkButton(frame_importar, text="Actualizar GRAYS", command=self.actualizar_grays, **boton_importar_kwargs).grid(row=2, column=1, padx=10, pady=(5, 12))

        # ---- Bloque: margen de ganancia por proveedor ----
        frame_margen = ctk.CTkFrame(contenedor, fg_color="#333333", corner_radius=10)
        frame_margen.pack(side="left", pady=5, fill="y")

        ctk.CTkLabel(
            frame_margen, text="MARGEN POR PROVEEDOR", font=ctk.CTkFont(size=13, weight="bold"), text_color="#8BC34A"
        ).grid(row=0, column=0, pady=(10, 8), padx=10, sticky="w")

        self.entry_proveedor_margen = ctk.CTkEntry(
            frame_margen, placeholder_text="Proveedor", fg_color="#4A4A4A", text_color="white",
            placeholder_text_color="#B0B0B0", width=150
        )
        self.entry_proveedor_margen.grid(row=1, column=0, padx=10, pady=5)

        self.entry_margen = ctk.CTkEntry(
            frame_margen, placeholder_text="Margen (ej: 1.40)", fg_color="#4A4A4A", text_color="white",
            placeholder_text_color="#B0B0B0", width=150
        )
        self.entry_margen.grid(row=2, column=0, padx=10, pady=5)

        ctk.CTkButton(
            frame_margen, text="Aplicar Margen", command=self.aplicar_margen,
            fg_color="#C62828", hover_color="#8E1B1B", width=150
        ).grid(row=3, column=0, padx=10, pady=(5, 12))

        # ---- Estilo de la tabla ----
        estilo = ttk.Style()
        estilo.theme_use("clam")  # permite personalizar colores ("clam"=tema propio, distinto al que trae Windows)
        estilo.configure("Treeview.Heading", background="#45B34B", foreground="white", font=("Segoe UI", 10, "bold"))
        estilo.map("Treeview.Heading", background=[("active", "#1B5E20")], foreground=[("active", "white")])
        estilo.configure("Treeview", background="#3C3C3C", foreground="white", fieldbackground="#3C3C3C", rowheight=26)
        estilo.map("Treeview", background=[("selected", "#45B34B")], foreground=[("selected", "white")])

        # ---- Tabla ----
        self.tabla = ttk.Treeview(
            self,
            columns=("id", "codigo", "nombre", "precio_lista", "precio_c_iva", "precio_final", "stock", "proveedor"),
            show="headings"
        )

        # Encabezados
        self.tabla.heading("id", text="ID")
        self.tabla.heading("codigo", text="CÓDIGO")
        self.tabla.heading("nombre", text="NOMBRE")
        self.tabla.heading("precio_lista", text="P. LISTA")
        self.tabla.heading("precio_c_iva", text="P. C/IVA")
        self.tabla.heading("precio_final", text="P. FINAL")
        self.tabla.heading("stock", text="STOCK")
        self.tabla.heading("proveedor", text="PROVEEDOR")

        # Anchos y alineación de cada columna, para que se vea prolijo
        self.tabla.column("id", width=50, anchor="center", stretch=False)
        self.tabla.column("codigo", width=90, anchor="center", stretch=False)
        self.tabla.column("nombre", width=320, anchor="w")
        self.tabla.column("precio_lista", width=110, anchor="e", stretch=False)
        self.tabla.column("precio_c_iva", width=110, anchor="e", stretch=False)
        self.tabla.column("precio_final", width=110, anchor="e", stretch=False)
        self.tabla.column("stock", width=70, anchor="center", stretch=False)
        self.tabla.column("proveedor", width=110, anchor="center", stretch=False)

        self.tabla.pack(padx=20, pady=(10, 15), fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)  # <<>> eventos puntuales específicos, ej: seleccionar una fila X

        self.id_seleccionado = None  # con None, aún no se seleccionó ningún producto o fila

        self.cargar_datos()

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for producto in self.db.obtener_productos():
            id_producto, codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor = producto
            lista_formateado = f"${precio_lista:,.2f}"
            civa_formateado = f"${precio_c_iva:,.2f}"
            final_formateado = f"${precio_final:,.2f}"
            self.tabla.insert("", "end", values=(id_producto, codigo, nombre, lista_formateado, civa_formateado, final_formateado, stock, proveedor))

    def buscar_producto(self, event):
        texto = self.entry_buscar.get().lower()
        for fila in self.tabla.get_children():  # Recorre cada fila que ya está en la tabla creada
            self.tabla.delete(fila)  # Y la borra, una por una
        for producto in self.db.obtener_productos():
            id_producto, codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor = producto
            if texto in nombre.lower() or texto in codigo.lower():
                lista_formateado = f"${precio_lista:,.2f}"
                civa_formateado = f"${precio_c_iva:,.2f}"
                final_formateado = f"${precio_final:,.2f}"
                self.tabla.insert("", "end", values=(id_producto, codigo, nombre, lista_formateado, civa_formateado, final_formateado, stock, proveedor))

    def agregar(self):
        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        precio_lista = self.entry_precio_lista.get()
        precio_civa = self.entry_precio_civa.get()
        stock = self.entry_stock.get()
        proveedor = self.entry_proveedor.get()

        if not codigo or not nombre or not precio_lista or not precio_civa or not stock or not proveedor:
            CTkMessagebox(title="Atención", message="Completá todos los campos.", icon="warning")
            return

        try:
            self.db.insertar_producto(codigo, nombre, float(precio_lista), float(precio_civa), int(stock), proveedor)
            self.cargar_datos()
            self.limpiar_campos()
            CTkMessagebox(title="Éxito", message="Producto agregado correctamente.", icon="check")
        except ValueError:
            CTkMessagebox(title="Error", message="Los precios y el stock deben ser numéricos.", icon="cancel")

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion[0], "values")
            self.id_seleccionado = valores[0]

            self.entry_codigo.delete(0, "end")
            self.entry_codigo.insert(0, valores[1])

            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, valores[2])

            self.entry_precio_lista.delete(0, "end")
            lista_sin_formato = valores[3].replace("$", "").replace(",", "")
            self.entry_precio_lista.insert(0, lista_sin_formato)

            self.entry_precio_civa.delete(0, "end")
            civa_sin_formato = valores[4].replace("$", "").replace(",", "")
            self.entry_precio_civa.insert(0, civa_sin_formato)

            self.entry_stock.delete(0, "end")
            self.entry_stock.insert(0, valores[6])

            self.entry_proveedor.delete(0, "end")
            self.entry_proveedor.insert(0, valores[7])

    def modificar(self):
        if not self.id_seleccionado:
            CTkMessagebox(title="Atención", message="Seleccioná un producto de la tabla.", icon="warning")
            return
        try:
            self.db.actualizar_producto(
                self.id_seleccionado,
                self.entry_codigo.get(),
                self.entry_nombre.get(),
                float(self.entry_precio_lista.get()),
                float(self.entry_precio_civa.get()),
                int(self.entry_stock.get()),
                self.entry_proveedor.get()
            )
            self.cargar_datos()
            self.limpiar_campos()
            CTkMessagebox(title="Éxito", message="Producto agregado correctamente.", icon="check")
        except ValueError:
            CTkMessagebox(title="Error", message="Los precios y el stock deben ser numéricos.", icon="cancel")

    def eliminar(self):
        if not self.id_seleccionado:
            CTkMessagebox(title="Atención", message="Seleccioná un producto de la tabla.", icon="warning")
            return
        self.db.eliminar_producto(self.id_seleccionado)
        self.cargar_datos()
        self.limpiar_campos()
        CTkMessagebox(title="Éxito", message="Producto eliminado correctamente.", icon="check")

    def limpiar_campos(self):
        self.entry_codigo.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_precio_lista.delete(0, "end")
        self.entry_precio_civa.delete(0, "end")
        self.entry_stock.delete(0, "end")
        self.entry_proveedor.delete(0, "end")
        self.id_seleccionado = None

    def actualizar_pol(self):
        ruta = filedialog.askopenfilename(
            title="Seleccioná el CSV de POL",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if ruta:
            self.db.actualizar_precios_pol(ruta)
            self.cargar_datos()
            CTkMessagebox(title="Actualizado", message="Precios de POL actualizados correctamente.", icon="check")

    def actualizar_fgp(self):
        ruta = filedialog.askopenfilename(
            title="Seleccioná el CSV de FGP",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if ruta:
            self.db.actualizar_precios_fgp(ruta)
            self.cargar_datos()
            CTkMessagebox(title="Actualizado", message="Precios de FGP actualizados correctamente.", icon="check")

    def actualizar_day(self):
        ruta = filedialog.askopenfilename(
            title="Seleccioná el CSV de DAY",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if ruta:
            self.db.actualizar_precios_day(ruta)
            self.cargar_datos()
            CTkMessagebox(title="Actualizado", message="Precios de DAY actualizados correctamente.", icon="check")

    def actualizar_grays(self):
        ruta = filedialog.askopenfilename(
            title="Seleccioná el CSV de GRAYS",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if ruta:
            self.db.actualizar_precios_grays(ruta)
            self.cargar_datos()
            CTkMessagebox(title="Actualizado", message="Precios de GRAYS actualizados correctamente.", icon="check")

    def aplicar_margen(self):
        proveedor = self.entry_proveedor_margen.get()
        margen = self.entry_margen.get()

        if not proveedor or not margen:
            CTkMessagebox(title="Atención", message="Completá proveedor y margen.", icon="warning")
            return

        try:
            self.db.aplicar_margen(proveedor, float(margen))
            self.cargar_datos()
            CTkMessagebox(title="Actualizado", message=f"Margen aplicado a todos los productos de {proveedor}.", icon="check")
        except ValueError:
            CTkMessagebox(title="Error", message="El margen debe ser numérico.", icon="cancel")
