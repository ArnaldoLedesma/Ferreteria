import customtkinter as ctk

import unicodedata  # Permite buscar sin importar los acentos

from tkinter import ttk, filedialog
from CTkMessagebox import CTkMessagebox  # libreria instalada por posibles errores al ejecutar (para mostrar los cuadros "ERROR" "ATENCION")
from database.conexion_db import ConexionDB
from gui.componentes.banner import BannerNavegacion  # Importa el banner creado en otro archivo


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = ConexionDB()

        self.title("Sistema de ventas // Gestión de Productos")
        self.geometry("1300x680")
        self.configure(fg_color="#3C3C3C")
        # self.iconbitmap("icono.ico")

         # Banner reutilizable con navegación entre Productos y Ventas
        self.banner = BannerNavegacion(
            self,
            comando_productos=self.mostrar_productos,
            comando_ventas=self.mostrar_ventas,
            
        )

       

        # ---- Contenedor general del formulario (debajo del banner) ----
        contenedor = ctk.CTkFrame(self, fg_color="#3C3C3C")
        contenedor.pack(fill="x", padx=20, pady=(15, 5))

        # ---- Bloque: datos del producto (CRUD) ----
        frame_datos = ctk.CTkFrame(contenedor, fg_color="#333333", corner_radius=10)
        frame_datos.pack(side="left", padx=(0, 15), pady=5, fill="y")

        ctk.CTkLabel(
            frame_datos, text="DATOS DEL PRODUCTO", font=ctk.CTkFont(size=17, weight="bold"), text_color="#8BC34A"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 8), padx=10, sticky="w")

        campo_kwargs = dict(fg_color="#4A4A4A", text_color="white", placeholder_text_color="#B0B0B0", width=190, font=ctk.CTkFont(size=15))

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

        # Agrupa Acciones, Actualizar precios y el buscador en una misma zona
        frame_centro = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_centro.pack(side="left", padx=(0, 15), pady=5)

        # Fila superior para colocar los dos cuadros uno al lado del otro
        fila_superior = ctk.CTkFrame(frame_centro, fg_color="transparent")
        fila_superior.pack(fill="x")

        # ---- Bloque: acciones CRUD ----
        frame_acciones = ctk.CTkFrame(fila_superior, fg_color="#333333", corner_radius=10)
        frame_acciones.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(
            frame_acciones, text="ACCIONES", font=ctk.CTkFont(size=17, weight="bold"), text_color="#8BC34A"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 8), padx=10, sticky="w")

        boton_kwargs = dict(fg_color="#45B34B", hover_color="#1B5E20", width=140, font=ctk.CTkFont(size=15))

        ctk.CTkButton(frame_acciones, text="Agregar", command=self.agregar, **boton_kwargs).grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkButton(frame_acciones, text="Modificar", command=self.modificar, **boton_kwargs).grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(frame_acciones, text="Eliminar", command=self.eliminar, fg_color="#C62828",hover_color="#8E1B1B",width=140).grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkButton(frame_acciones, text="Limpiar", command=self.limpiar_campos, **boton_kwargs).grid(row=2, column=1, padx=10, pady=(5, 12))

        # ---- Bloque: importar precios por proveedor ----
        frame_importar = ctk.CTkFrame(fila_superior, fg_color="#333333", corner_radius=10)
        frame_importar.pack(side="left")

        ctk.CTkLabel(
            frame_importar, text="ACTUALIZAR PRECIOS (CSV)", font=ctk.CTkFont(size=17, weight="bold"), text_color="#8BC34A"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 8), padx=10, sticky="w")

        boton_importar_kwargs = dict(fg_color="#2E7D32", hover_color="#1B5E20", width=140, font=ctk.CTkFont(size=15))

        ctk.CTkButton(frame_importar, text="Actualizar POL", command=self.actualizar_pol, **boton_importar_kwargs).grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkButton(frame_importar, text="Actualizar FGP", command=self.actualizar_fgp, **boton_importar_kwargs).grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(frame_importar, text="Actualizar DAY", command=self.actualizar_day, **boton_importar_kwargs).grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkButton(frame_importar, text="Actualizar GRAYS", command=self.actualizar_grays, **boton_importar_kwargs).grid(row=2, column=1, padx=10, pady=(5, 12))

        # Buscador propio del módulo Gestión de Productos
        self.entry_buscar = ctk.CTkEntry(
            frame_centro,
            placeholder_text="🔎 Buscar producto por nombre o código...",
            height=35,
            font=ctk.CTkFont(size=15),
            fg_color="#4A4A4A",
            text_color="white",
            placeholder_text_color="#B0B0B0",
            border_color="#CFFC05",
            border_width=1
        )
        self.entry_buscar.pack(fill="x", pady=(10, 0))

        self.entry_buscar.bind(
            "<KeyRelease>",
            self.buscar_producto
        )  # Filtra la tabla mientras se escribe

        # ---- Bloque: margen de ganancia por proveedor ----
        frame_margen = ctk.CTkFrame(contenedor, fg_color="#333333", corner_radius=10, width=280)
        frame_margen.pack(side="left", pady=5, fill="y")
        frame_margen.pack_propagate(False)

        ctk.CTkLabel(
            frame_margen, text="MARGEN POR PROVEEDOR", font=ctk.CTkFont(size=14, weight="bold"), text_color="#8BC34A", 
        ).grid(row=0, column=0, pady=(10, 8), padx=10, sticky="w")

        self.entry_proveedor_margen = ctk.CTkEntry(
            frame_margen, placeholder_text="Proveedor", fg_color="#4A4A4A", text_color="white",
            placeholder_text_color="#B0B0B0", width=150, font=ctk.CTkFont(size=15)
        )
        self.entry_proveedor_margen.grid(row=1, column=0, padx=10, pady=5)

        self.entry_margen = ctk.CTkEntry(
            frame_margen, placeholder_text="Margen (ej: 1.40)", fg_color="#4A4A4A", text_color="white",
            placeholder_text_color="#B0B0B0", width=150, font=ctk.CTkFont(size=15)
        )
        self.entry_margen.grid(row=2, column=0, padx=10, pady=5)

        ctk.CTkButton(
            frame_margen, text="Aplicar Margen", command=self.aplicar_margen,
            fg_color="#C62828", hover_color="#8E1B1B", width=150, font=ctk.CTkFont(size=15)
        ).grid(row=3, column=0, padx=10, pady=(5, 12))

        # ---- Estilo de la tabla ----
        estilo = ttk.Style()
        estilo.theme_use("clam")  # permite personalizar colores ("clam"=tema propio, distinto al que trae Windows)
        estilo.configure("Treeview.Heading", background="#45B34B", foreground="white", font=("Segoe UI", 12, "bold"))
        estilo.map("Treeview.Heading", background=[("active", "#1B5E20")], foreground=[("active", "white")])
        estilo.configure("Treeview", background="#3C3C3C", foreground="white", fieldbackground="#3C3C3C", rowheight=32, font=("Segoe UI", 11))
        estilo.map("Treeview", background=[("selected", "#45B34B")], foreground=[("selected", "white")])

        # Frame que contendrá la tabla y su barra de desplazamiento
        frame_tabla = ctk.CTkFrame(self, fg_color="transparent")
        frame_tabla.pack(padx=20, pady=(10, 15), fill="both", expand=True)

        # ---- Tabla ----
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("id", "codigo", "nombre", "precio_lista", "precio_c_iva", "precio_final", "stock", "proveedor", "fecha_act"),
            show="headings"
        )

        # Encabezados
        self.tabla.heading("id", text="ID", anchor="center")
        self.tabla.heading("codigo", text="CÓDIGO", anchor="center")
        self.tabla.heading("nombre", text="   NOMBRE", anchor="center")
        self.tabla.heading("precio_lista", text="  P. LISTA", anchor="center")
        self.tabla.heading("precio_c_iva", text="  P. C/IVA", anchor="center")
        self.tabla.heading("precio_final", text="★ P VENTA", anchor="center")
        self.tabla.heading("stock", text="STOCK", anchor="center")
        self.tabla.heading("proveedor", text="PROVEEDOR", anchor="center")
        self.tabla.heading("fecha_act", text="ÚLT. ACTUALIZACIÓN", anchor="center")

        # Anchos y alineación de cada columna, para que se vea prolijo
        self.tabla.column("id", width=50, anchor="center", stretch=False)
        self.tabla.column("codigo", width=90, anchor="center", stretch=False)
        self.tabla.column("nombre", width=220, anchor="w")
        self.tabla.column("precio_lista", width=110, anchor="e", stretch=False)
        self.tabla.column("precio_c_iva", width=110, anchor="e", stretch=False)
        self.tabla.column("precio_final", width=140, anchor="e", stretch=False)
        self.tabla.column("stock", width=70, anchor="center", stretch=False)
        self.tabla.column("proveedor", width=110, anchor="center", stretch=False)
        self.tabla.column("fecha_act", width=220, anchor="center", stretch=False)

        # Barra vertical conectada con la tabla de productos
        barra_vertical = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(yscrollcommand=barra_vertical.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        barra_vertical.pack(side="right", fill="y")
        self.label_total_productos = ctk.CTkLabel(
            self,
            text="TOTAL DE PRODUCTOS: 0",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#8BC34A"
        )
        self.label_total_productos.pack(anchor="e", padx=25, pady=(8, 0), before=frame_tabla)  # Coloca el contador antes de la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)  # <<>> eventos puntuales específicos, ej: seleccionar una fila X

        self.id_seleccionado = None  # con None, aún no se seleccionó ningún producto o fila

        self.cargar_datos()

    def mostrar_productos(self):
            pass  # Ya estamos dentro de la ventana de Gestión de Productos

    def mostrar_ventas(self):
            CTkMessagebox(
                title="Gestión de Ventas",
                message="El módulo de ventas se encuentra en desarrollo.",
                icon="info"
            )

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        productos = self.db.obtener_productos()

        self.label_total_productos.configure(
            text=f"TOTAL DE PRODUCTOS: {len(productos):,}".replace(",", ".")
        )

        for producto in productos:
            id_producto, codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor, fecha_act = producto
            lista_formateado = f"${precio_lista:,.2f}"
            civa_formateado = f"${precio_c_iva:,.2f}"
            final_formateado = f"★  ${precio_final:,.2f}"
            self.tabla.insert("", "end", values=(id_producto, codigo, nombre, lista_formateado, civa_formateado, final_formateado, stock, proveedor, fecha_act or "")) # el or evita la palabra NONE en la tabla,en su lugar un espacio vacio

    def buscar_producto(self, event):
        def normalizar(texto):
            texto = str(texto).lower().strip()  # Convierte también códigos numéricos en texto
            return "".join(
                letra for letra in unicodedata.normalize("NFD", texto)
                if unicodedata.category(letra) != "Mn"
            )  # Elimina diferencias entre ó, ò y 

        texto_buscado = normalizar(self.entry_buscar.get())

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for producto in self.db.obtener_productos():
            id_producto, codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor, fecha_act = producto

            codigo_normalizado = normalizar(codigo)
            nombre_normalizado = normalizar(nombre)

            if texto_buscado in codigo_normalizado or texto_buscado in nombre_normalizado:
                lista_formateado = f"${precio_lista:,.2f}"
                civa_formateado = f"${precio_c_iva:,.2f}"
                final_formateado = f"★  ${precio_final:,.2f}"

                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        id_producto, codigo, nombre, lista_formateado,
                        civa_formateado, final_formateado, stock,
                        proveedor, fecha_act or ""
                    )
                )

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
            CTkMessagebox(title="Éxito", message="Producto modificado correctamente.", icon="check")
        except ValueError:
            CTkMessagebox(title="Error", message="Los precios y el stock deben ser numéricos.", icon="cancel")

    def eliminar(self):
        if not self.id_seleccionado:
            CTkMessagebox(title="Atención", message="Seleccioná un producto de la tabla.", icon="warning")
            return

        confirmacion = CTkMessagebox(
            title="Confirmar eliminación",
            message="¿Estás seguro que querés eliminar este producto?",
            icon="warning",
            option_1="No",
            option_2="Sí"
        )
        respuesta = confirmacion.get()

        if respuesta == "Sí":
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
