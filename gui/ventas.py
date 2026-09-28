import customtkinter as ctk
from tkinter import ttk
from database.conexion_db import ConexionDB
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
from gui.componentes.dialogos import DialogoConfirmacion, DialogoVentaRegistrada

class VentanaVentas(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.db = ConexionDB()
        self.db.crear_tablas_ventas()  # Crea las tablas solamente si todavía no existen

        self.carrito = {} 
        self.title("Sistema de ventas // Gestión de Ventas")
        self.geometry("1300x680")
        self.after(100, lambda: self.state("zoomed"))  # Abre Ventas maximizada según la pantalla
        self.configure(fg_color="#3C3C3C")

        # Coloca Ventas adelante al abrirse, pero permite usar las demás ventanas
        self.attributes("-topmost", True)
        self.after(300, self.dejar_ventana_normal)
        self.focus_force()

        # Contenedor principal: productos a la izquierda y carrito a la derecha
        self.contenedor = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.contenedor.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.frame_productos = ctk.CTkFrame(
            self.contenedor,
            fg_color="#333333",
            corner_radius=10
        )
        self.frame_productos.pack(
            fill="both",
            expand=True,
            pady=(0, 5)

        )

        self.frame_carrito = ctk.CTkFrame(
            self.contenedor,
            fg_color="#333333",
            corner_radius=10
        )

        self.frame_carrito.pack(
            fill="both",
            expand=True,
            pady=(5, 0)
        )

        ctk.CTkLabel(
            self.frame_productos,
            text="PRODUCTOS DISPONIBLES",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#8BC34A"
        ).pack(pady=15)

        self.entry_buscar = ctk.CTkEntry(
    self.frame_productos,
    placeholder_text="🔎 Buscar por código o nombre...",
    height=38,
    font=ctk.CTkFont(size=15),
    fg_color="#4A4A4A",
    border_color="#8BC34A",
    border_width=1
)
        self.entry_buscar.pack(fill="x", padx=15, pady=(0, 12))

        # Ejecuta la búsqueda cada vez que el usuario escribe
        self.entry_buscar.bind("<KeyRelease>", self.buscar_productos)

        frame_tabla_productos = ctk.CTkFrame(
            self.frame_productos,
            fg_color="transparent"
        )
        frame_tabla_productos.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.tabla_productos = ttk.Treeview(
            frame_tabla_productos,
            columns=("codigo", "nombre", "precio", "stock"),
            show="headings",
            height=4
        )

        self.tabla_productos.heading("codigo", text="CÓDIGO")
        self.tabla_productos.heading("nombre", text="PRODUCTO")
        self.tabla_productos.heading("precio", text="P. VENTA")
        self.tabla_productos.heading("stock", text="STOCK")

        self.tabla_productos.column(
            "codigo", width=150, anchor="center", stretch=False
        )
        self.tabla_productos.column(
            "nombre", width=650, anchor="w", stretch=True
        )
        self.tabla_productos.column(
            "precio", width=170, anchor="center", stretch=False
        )
        self.tabla_productos.column(
            "stock", width=100, anchor="center", stretch=False
        )

        barra_productos = ttk.Scrollbar(
            frame_tabla_productos,
            orient="vertical",
            command=self.tabla_productos.yview
        )

        self.tabla_productos.configure(
            yscrollcommand=barra_productos.set
        )

        self.tabla_productos.pack(
            side="left",
            fill="both",
            expand=True
        )
        barra_productos.pack(side="right", fill="y")

        frame_agregar = ctk.CTkFrame(
            self.frame_productos,
            fg_color="transparent"
        )
        frame_agregar.pack(fill="x", padx=15, pady=(0, 10))

        self.entry_cantidad = ctk.CTkEntry(
            frame_agregar,
            placeholder_text="Cantidad",
            width=120,
            height=36,
            justify="center"
        )
        self.entry_cantidad.pack(side="left", padx=(0, 10))
        self.entry_cantidad.insert(0, "1")

        ctk.CTkButton(
            frame_agregar,
            text="AGREGAR AL CARRITO",
            command=self.agregar_al_carrito,
            fg_color="#45B34B",
            hover_color="#1B5E20",
            height=36,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")

        self.buscar_productos()  # Muestra los primeros productos al abrir Ventas

        ctk.CTkLabel(
            self.frame_carrito,
            text="CARRITO DE VENTA",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#8BC34A"
        ).pack(pady=15)

        frame_tabla_carrito = ctk.CTkFrame(
            self.frame_carrito,
            fg_color="transparent"
        )
        frame_tabla_carrito.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )  # Usa solamente la altura necesaria y deja lugar para botones y total

        self.tabla_carrito = ttk.Treeview(
            frame_tabla_carrito,
            columns=("codigo", "producto", "cantidad", "precio", "subtotal"),
            show="headings",
            height=3
        )

        self.tabla_carrito.heading("codigo", text="CÓDIGO")
        self.tabla_carrito.heading("producto", text="PRODUCTO")
        self.tabla_carrito.heading("cantidad", text="CANT.")
        self.tabla_carrito.heading("precio", text="PRECIO")
        self.tabla_carrito.heading("subtotal", text="SUBTOTAL")

        self.tabla_carrito.column("codigo", width=75, anchor="center")
        self.tabla_carrito.column("producto", width=190, anchor="w")
        self.tabla_carrito.column("cantidad", width=60, anchor="center")
        self.tabla_carrito.column("precio", width=95, anchor="center")
        self.tabla_carrito.column("subtotal", width=105, anchor="center")

        barra_carrito = ttk.Scrollbar(
            frame_tabla_carrito,
            orient="vertical",
            command=self.tabla_carrito.yview
        )

        self.tabla_carrito.configure(
            yscrollcommand=barra_carrito.set
        )

        self.tabla_carrito.pack(
            side="left",
            fill="both",
            expand=True
        )
        barra_carrito.pack(side="right", fill="y")

        frame_botones_carrito = ctk.CTkFrame(
            self.frame_carrito,
            fg_color="transparent"
        )
        frame_botones_carrito.pack(fill="x", padx=15, pady=(0, 5))

        ctk.CTkButton(
            frame_botones_carrito,
            text="QUITAR PRODUCTO",
            command=self.quitar_producto,
            fg_color="#C62828",
            hover_color="#8E1B1B",
            width=160
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_botones_carrito,
            text="VACIAR CARRITO",
            command=self.vaciar_carrito,
            fg_color="#616161",
            hover_color="#424242",
            width=160
        ).pack(side="left")

        ctk.CTkButton(
            frame_botones_carrito,
            text="FINALIZAR VENTA",
            command=self.finalizar_venta,
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180
        ).pack(side="right", padx=5)

        ctk.CTkLabel(
            frame_botones_carrito,
            text="MEDIO DE PAGO:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=(35, 10))

        self.combo_medio_pago = ctk.CTkComboBox(
            frame_botones_carrito,
            values=["Efectivo", "Transferencia", "Débito", "Crédito"],
            state="readonly",
            width=170,
            height=30,
            fg_color="#4A4A4A",
            button_color="#45B34B",
            button_hover_color="#1B5E20"
        )
        self.combo_medio_pago.pack(side="left")
        self.combo_medio_pago.set("Efectivo")

        self.label_total = ctk.CTkLabel(
            self.frame_carrito,
            text="TOTAL: $0.00",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#8BC34A"
        )
        self.label_total.pack(anchor="e", padx=20, pady=(5, 15))

    def dejar_ventana_normal(self):
                self.attributes("-topmost", False)  # Evita que quede siempre encima de otros programas
                self.lift()
                self.focus_force()   

    def buscar_productos(self, event=None):
        texto = self.entry_buscar.get().strip()

        # Borra los resultados anteriores antes de mostrar la nueva búsqueda
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        productos = self.db.buscar_productos_venta(texto)

        for id_producto, codigo, nombre, precio, stock in productos:
            self.tabla_productos.insert(
                "",
                "end",
                iid=str(id_producto),  # Guarda internamente el ID real del producto
                values=(
                    codigo,
                    nombre,
                    f"${precio:,.2f}",
                    stock
                )
            )
    def agregar_al_carrito(self):
        seleccion = self.tabla_productos.selection()

        if not seleccion:
            CTkMessagebox(
                title="Atención",
                message="Seleccioná un producto.",
                icon="warning"
            )
            return

        try:
            cantidad = int(self.entry_cantidad.get())

            if cantidad <= 0:
                raise ValueError

        except ValueError:
            CTkMessagebox(
                title="Cantidad incorrecta",
                message="Ingresá una cantidad mayor que cero.",
                icon="warning"
            )
            return

        id_producto = seleccion[0]
        valores = self.tabla_productos.item(id_producto, "values")

        codigo = valores[0]
        nombre = valores[1]
        precio = float(valores[2].replace("$", "").replace(",", ""))
        stock = int(valores[3])

        cantidad_actual = self.carrito.get(id_producto, {}).get("cantidad", 0)
        nueva_cantidad = cantidad_actual + cantidad

        if nueva_cantidad > stock:
            CTkMessagebox(
                title="Stock insuficiente",
                message=f"Stock disponible: {stock}",
                icon="warning"
            )
            return

        self.carrito[id_producto] = {
            "codigo": codigo,
            "nombre": nombre,
            "cantidad": nueva_cantidad,
            "precio": precio,
            "stock": stock
        }

        self.actualizar_carrito()

        self.entry_cantidad.delete(0, "end")
        self.entry_cantidad.insert(0, "1")


    def actualizar_carrito(self):
        for fila in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(fila)

        total = 0

        for id_producto, producto in self.carrito.items():
            subtotal = producto["cantidad"] * producto["precio"]
            total += subtotal

            self.tabla_carrito.insert(
                "",
                "end",
                iid=id_producto,
                values=(
                    producto["codigo"],
                    producto["nombre"],
                    producto["cantidad"],
                    f"${producto['precio']:,.2f}",
                    f"${subtotal:,.2f}"
                )
            )

        self.label_total.configure(text=f"TOTAL: ${total:,.2f}")  

    def quitar_producto(self):
        seleccion = self.tabla_carrito.selection()

        if not seleccion:
            CTkMessagebox(
                title="Atención",
                message="Seleccioná un producto del carrito.",
                icon="warning"
            )
            return

        id_producto = seleccion[0]
        del self.carrito[id_producto]

        self.actualizar_carrito()


    def vaciar_carrito(self):
        if not self.carrito:
            CTkMessagebox(
                title="Carrito vacío",
                message="No hay productos para quitar.",
                icon="info"
            )
            return

        confirmacion = CTkMessagebox(
            title="Vaciar carrito",
            message="¿Querés quitar todos los productos del carrito?",
            icon="warning",
            option_1="No",
            option_2="Sí"
        )

        if confirmacion.get() == "Sí":
            self.carrito.clear()
            self.actualizar_carrito()      

    def finalizar_venta(self):
        if not self.carrito:
            messagebox.showwarning(
                "Carrito vacío",
                "Debe agregar al menos un producto."
            )
            return

        medio_pago = self.combo_medio_pago.get() #DISEÑO DE LOS CARTELES

        dialogo = DialogoConfirmacion(
                self,
                self.label_total.cget("text"),
                medio_pago
            )

        self.wait_window(dialogo)  # Espera la respuesta antes de continuar

        if not dialogo.resultado:
                return

        try:
            venta_id = self.db.registrar_venta(
                self.carrito,
                medio_pago
            )

            dialogo_exito = DialogoVentaRegistrada(self, venta_id)
            self.wait_window(dialogo_exito)  # Espera que el usuario cierre el aviso

            self.carrito.clear()
            self.actualizar_carrito()
            self.entry_cantidad.delete(0, "end")

            # Actualiza la tabla para mostrar el stock descontado
            self.buscar_productos()

        except ValueError as error:
            messagebox.showwarning("No se pudo registrar", str(error))

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al registrar la venta:\n{error}"
            )
                    