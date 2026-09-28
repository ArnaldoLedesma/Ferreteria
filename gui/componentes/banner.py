
from pathlib import Path
from PIL import Image
import customtkinter as ctk


class BannerNavegacion(ctk.CTkFrame):
    def __init__(self, master, comando_productos, comando_ventas):
        super().__init__(
            master,
            fg_color="#2E7D32",
            height=75,
            corner_radius=0
        )

        self.pack(fill="x", side="top")
        self.pack_propagate(False)  # Mantiene fija la altura del banner

        # Construye la ruta desde banner.py hasta la carpeta principal del proyecto
        ruta_imagen = (
            Path(__file__).resolve().parents[2]
            / "recursos"
            / "banner_ferreteria.png"
        )

        imagen_original = Image.open(ruta_imagen)

        self.imagen_fondo = ctk.CTkImage(
            light_image=imagen_original,
            dark_image=imagen_original,
            size=(1400, 75)  # Adapta la imagen al tamaño actual del banner
        )

        label_fondo = ctk.CTkLabel(
            self,
            image=self.imagen_fondo,
            text="",
            width=1400,
            height=75,
            corner_radius=0
        )

        label_fondo.place(
            x=-5,
            y=0
        )  # Desplaza levemente la imagen para cubrir el margen izquierdo
    
        # ---------- NAVEGACIÓN ENTRE MÓDULOS ----------

        frame_navegacion = ctk.CTkFrame(self, fg_color="transparent")
        frame_navegacion.place(
        relx=0.5,
        rely=0.80,
        anchor="center"
    )  # Centra la navegación respecto de todo el banner
    
          # Centra la navegación respecto de todo el banner

        ctk.CTkButton(
            frame_navegacion,
            text="📦 PRODUCTOS",
            command=comando_productos,
            fg_color="#1B5E20",
            hover_color="#144A18",
            width=150,
            font=ctk.CTkFont(size=15, weight="bold")  # Tamaño de la letra del botón
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            frame_navegacion,
            text="🛒 VENTAS",
            command=comando_ventas,
            fg_color="#45B34B",
            hover_color="#1B5E20",
            width=150,
            font=ctk.CTkFont(size=15, weight="bold")  # Tamaño de la letra del botón
        ).pack(side="left", padx=6)

       