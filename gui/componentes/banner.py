
from pathlib import Path
from PIL import Image
import customtkinter as ctk


class BannerNavegacion(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#2E7D32",
            height=95,
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
            size=(1450, 95)  # Adapta la imagen al tamaño actual del banner
        )

        label_fondo = ctk.CTkLabel(
            self,
            image=self.imagen_fondo,
            text="",
            width=1400,
            height=95,
            corner_radius=0
        )

        label_fondo.place(
            x=-5,
            y=0
        )  # Desplaza levemente la imagen para cubrir el margen izquierdo