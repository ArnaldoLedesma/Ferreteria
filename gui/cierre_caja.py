import sqlite3
from datetime import datetime
import customtkinter as ctk


class VentanaCierreCaja(ctk.CTkToplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db

        self.title("Cierre de caja")
        self.geometry("560x420")
        self.transient(master)
        self.configure(fg_color="#202020")
        self.after(100, self.centrar_sobre_principal, master.winfo_toplevel())

        # Encabezado: título y fecha en líneas separadas.
        ctk.CTkLabel(
            self, text="Resumen de caja",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#F5F5F5",
        ).pack(anchor="w", padx=20, pady=(16, 0))

        self.fecha = ctk.CTkLabel(self, text="", text_color="#BDBDBD")
        self.fecha.pack(anchor="w", padx=20, pady=(0, 10))

        tarjetas = ctk.CTkFrame(self, fg_color="transparent")
        tarjetas.pack(fill="x", padx=20)
        tarjetas.grid_columnconfigure((0, 1), weight=1, uniform="tarjetas")

        self.total = self.crear_tarjeta(tarjetas, "Total vendido", 0)
        self.cantidad = self.crear_tarjeta(tarjetas, "Cantidad de ventas", 1)

        # El pie queda fijo; solo el desglose puede desplazarse.
        pie = ctk.CTkFrame(self, fg_color="transparent")
        pie.pack(side="bottom", fill="x", padx=20, pady=(8, 14))

        ctk.CTkButton(
            pie, text="Actualizar resumen",
            command=self.actualizar_resumen,
            fg_color="#1B5E20", hover_color="#144A18",
        ).pack(side="right")

        ctk.CTkLabel(
            self, text="Por medio de pago",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#F5F5F5",
        ).pack(anchor="w", padx=20, pady=(12, 4))

        self.detalle = ctk.CTkScrollableFrame(
            self, fg_color="#2C2C2C", corner_radius=10, height=100,
        )
        self.detalle.pack(fill="both", expand=True, padx=20)

        self.actualizar_resumen()

    def crear_tarjeta(self, contenedor, titulo, columna):
        tarjeta = ctk.CTkFrame(contenedor, fg_color="#303030", corner_radius=10)
        tarjeta.grid(
            row=0, column=columna, sticky="ew",
            padx=(0, 6) if columna == 0 else (6, 0),
        )

        ctk.CTkLabel(tarjeta, text=titulo, text_color="#BDBDBD").pack(
            anchor="w", padx=14, pady=(8, 0)
        )

        valor = ctk.CTkLabel(
            tarjeta, text="—", text_color="#F5F5F5",
            font=ctk.CTkFont(size=24 if columna == 0 else 20, weight="bold"),
        )
        valor.pack(anchor="w", padx=14, pady=(0, 8))
        return valor

    def centrar_sobre_principal(self, principal):
        x = principal.winfo_rootx() + (
            principal.winfo_width() - self.winfo_width()
        ) // 2
        y = principal.winfo_rooty() + (
            principal.winfo_height() - self.winfo_height()
        ) // 2
        self.geometry(f"560x420{x:+d}{y:+d}")

    def actualizar_resumen(self):
        # Limpia el desglose anterior para no duplicar filas al actualizar.
        for widget in self.detalle.winfo_children():
            widget.destroy()

        try:
            datos = self.db.obtener_resumen_ventas_hoy()
        except sqlite3.Error:
            self.fecha.configure(text="Resumen no disponible")
            self.total.configure(text="—")
            self.cantidad.configure(text="—")
            self.mostrar_aviso("No se pudo consultar el resumen. Volvé a intentar.")
            return

        hora = datetime.now().strftime("%H:%M")
        self.fecha.configure(
            text=f"Ventas del día · {datos['fecha']} · Actualizado a las {hora}"
        )
        self.total.configure(text=self.formatear_importe(datos["total_general"]))
        self.cantidad.configure(text=str(datos["cantidad_ventas"]))

        if not datos["por_medio"]:
            self.mostrar_aviso("Todavía no hay ventas registradas hoy.")
            return

        for fila in datos["por_medio"]:
            renglon = ctk.CTkFrame(self.detalle, fg_color="transparent")
            renglon.pack(fill="x", padx=6, pady=2)

            medio = fila["medio"] or "Sin identificar"
            cantidad = fila["cantidad"]
            etiqueta = "venta" if cantidad == 1 else "ventas"

            ctk.CTkLabel(
                renglon,
                text=medio.upper(),
                text_color="#F5F5F5",
                font=ctk.CTkFont(size=15, weight="bold"),
            ).pack(side="left")

            ctk.CTkLabel(
                renglon,
                text=f"· {cantidad} {etiqueta}",
                text_color="#BDBDBD",
                font=ctk.CTkFont(size=12),
            ).pack(side="left", padx=(6, 0))

            ctk.CTkLabel(
                renglon,
                text=self.formatear_importe(fila["total"]),
                text_color="#F5F5F5",
                font=ctk.CTkFont(size=14, weight="bold"),
            ).pack(side="right")

    def mostrar_aviso(self, texto):
        ctk.CTkLabel(
            self.detalle, text=texto, text_color="#BDBDBD", wraplength=420,
        ).pack(padx=10, pady=12)

    @staticmethod
    def formatear_importe(valor):
        importe = f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
        return f"${importe}"