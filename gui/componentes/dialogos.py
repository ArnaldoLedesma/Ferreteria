import customtkinter as ctk

def centrar_dialogo(dialogo, parent, ancho, alto): # con esta funcion centramos lso carteles de finalizar ventas
    parent.update_idletasks()

    x = parent.winfo_x() + (parent.winfo_width() - ancho) // 2
    y = parent.winfo_y() + (parent.winfo_height() - alto) // 2

    # Coloca el cartel exactamente en el centro de la ventana de Ventas
    dialogo.geometry(f"{ancho}x{alto}+{x}+{y}")


class DialogoConfirmacion(ctk.CTkToplevel):

    def __init__(self, parent, total, medio_pago):
        super().__init__(parent)

        self.resultado = False

        self.title("Confirmar venta")
        centrar_dialogo(self, parent, 430, 230)
        self.resizable(False, False)
        self.configure(fg_color="#3B3B3B")

        self.transient(parent)
        self.grab_set()  # Impide utilizar otra ventana hasta responder

        ctk.CTkLabel(
            self,
            text="¿CONFIRMAR LA VENTA?",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color="#8BC34A"
        ).pack(pady=(25, 12))

        ctk.CTkLabel(
            self,
            text=f"Total: {total}\nMedio de pago: {medio_pago}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
            fg_color="#2E2E2E",
            corner_radius=8,
            width=340,
            height=65,
            justify="center"
        ).pack(pady=8)

        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=20)

        ctk.CTkButton(
            frame_botones,
            text="CANCELAR",
            command=self.cancelar,
            fg_color="#D32F2F",
            hover_color="#A92121",
            width=140
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            frame_botones,
            text="CONFIRMAR",
            command=self.confirmar,
            fg_color="#45B34B",
            hover_color="#1B5E20",
            width=140
        ).pack(side="left", padx=8)

        self.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.after(100, self.focus_force)

    def confirmar(self):
        self.resultado = True
        self.destroy()

    def cancelar(self):
        self.resultado = False
        self.destroy()

class DialogoVentaRegistrada(ctk.CTkToplevel):
    def __init__(self, parent, venta_id):
        super().__init__(parent)

        self.title("Venta registrada")
        centrar_dialogo(self, parent, 430, 230)
        self.resizable(False, False)
        self.configure(fg_color="#3B3B3B")

        self.transient(parent)
        self.grab_set()  # Mantiene el cartel asociado a Ventas

        ctk.CTkLabel(
            self,
            text="✓ VENTA REGISTRADA",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#8BC34A"
        ).pack(pady=(28, 15))

        ctk.CTkLabel(
            self,
            text=f"Venta N.º {venta_id}\nregistrada correctamente.",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
            fg_color="#2E2E2E",
            corner_radius=8,
            width=340,
            height=65,
            justify="center"
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="ACEPTAR",
            command=self.destroy,
            fg_color="#45B34B",
            hover_color="#1B5E20",
            width=150
        ).pack(pady=18)

        self.after(100, self.focus_force)
