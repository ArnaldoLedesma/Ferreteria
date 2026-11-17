from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from database.usuarios_db import GestorUsuarios


class VentanaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Acceso al sistema - Ferretería")
        self.configure(fg_color="#102722")

        self.gestor_usuarios = GestorUsuarios()
        self.usuario_autenticado = None

        # Detecta si todavía no existe ningún usuario registrado
        self.primer_acceso = self.gestor_usuarios.cantidad_usuarios() == 0

        self.configurar_ventana()
        self.cargar_imagen_fondo()
        self.crear_formulario()

        # Permite ingresar o crear el usuario presionando Enter
        self.bind("<Return>", lambda event: self.ejecutar_accion())

    def configurar_ventana(self):
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        self.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        self.minsize(850, 550)

        # En Windows abre la ventana maximizada
        self.after(100, lambda: self.state("zoomed"))

    def cargar_imagen_fondo(self):
        ruta_imagen = (
            Path(__file__).resolve().parents[1]
            / "recursos"
            / "login_ferreteria.png"
        )

        if not ruta_imagen.exists():
            messagebox.showerror(
                "Imagen no encontrada",
                f"No se encontró la imagen:\n{ruta_imagen}"
            )
            return

        imagen_original = Image.open(ruta_imagen)

        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        self.imagen_fondo = ctk.CTkImage(
            light_image=imagen_original,
            dark_image=imagen_original,
            size=(ancho_pantalla, alto_pantalla)
        )

        self.label_fondo = ctk.CTkLabel(
            self,
            image=self.imagen_fondo,
            text=""
        )

        self.label_fondo.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

    def crear_formulario(self):
        # Si reconstruimos el formulario, eliminamos primero el anterior
        if hasattr(self, "panel_login"):
            self.panel_login.destroy()

        alto_panel = 540 if self.primer_acceso else 480

        self.panel_login = ctk.CTkFrame(
            self,
            width=420,
            height=alto_panel,
            corner_radius=28,
            fg_color="#102B28",
            border_width=2,
            border_color="#2C7A68"
        )

        self.panel_login.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Evita que el panel cambie de tamaño por sus componentes internos
        self.panel_login.pack_propagate(False)

        titulo = (
            "CREAR ADMINISTRADOR"
            if self.primer_acceso
            else "INICIAR SESIÓN"
        )

        subtitulo = (
            "Primer acceso al sistema"
            if self.primer_acceso
            else "Sistema de Gestión Comercial"
        )

        ctk.CTkLabel(
            self.panel_login,
            text="🔧 FERRETERÍA",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            self.panel_login,
            text=titulo,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#65C18C"
        ).pack(pady=(5, 2))

        ctk.CTkLabel(
            self.panel_login,
            text=subtitulo,
            font=ctk.CTkFont(size=13),
            text_color="#B7CCC5"
        ).pack(pady=(0, 25))

        self.entry_usuario = ctk.CTkEntry(
            self.panel_login,
            width=320,
            height=48,
            placeholder_text="Usuario",
            font=ctk.CTkFont(size=15),
            fg_color="#163A35",
            border_color="#2C8B78",
            border_width=2,
            corner_radius=14
        )
        self.entry_usuario.pack(pady=8)

        self.entry_clave = ctk.CTkEntry(
            self.panel_login,
            width=320,
            height=48,
            placeholder_text="Contraseña",
            show="●",
            font=ctk.CTkFont(size=15),
            fg_color="#163A35",
            border_color="#2C8B78",
            border_width=2,
            corner_radius=14
        )
        self.entry_clave.pack(pady=8)

        if self.primer_acceso:
            self.entry_confirmar = ctk.CTkEntry(
                self.panel_login,
                width=320,
                height=48,
                placeholder_text="Repetir contraseña",
                show="●",
                font=ctk.CTkFont(size=15),
                fg_color="#163A35",
                border_color="#2C8B78",
                border_width=2,
                corner_radius=14
            )
            self.entry_confirmar.pack(pady=8)

        self.check_mostrar = ctk.CTkCheckBox(
            self.panel_login,
            text="Mostrar contraseña",
            command=self.mostrar_contrasena,
            font=ctk.CTkFont(size=13),
            fg_color="#2E8B72",
            hover_color="#246C5A"
        )
        self.check_mostrar.pack(pady=(12, 18))

        texto_boton = (
            "CREAR USUARIO"
            if self.primer_acceso
            else "INGRESAR"
        )

        self.boton_ingresar = ctk.CTkButton(
            self.panel_login,
            text=texto_boton,
            command=self.ejecutar_accion,
            width=320,
            height=48,
            corner_radius=14,
            fg_color="#2E8B57",
            hover_color="#236B43",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.boton_ingresar.pack(pady=5)

        self.entry_usuario.focus()

    def mostrar_contrasena(self):
        mostrar = self.check_mostrar.get() == 1
        caracter = "" if mostrar else "●"

        self.entry_clave.configure(show=caracter)

        if self.primer_acceso:
            self.entry_confirmar.configure(show=caracter)

    def ejecutar_accion(self):
        if self.primer_acceso:
            self.crear_administrador()
        else:
            self.iniciar_sesion()

    def crear_administrador(self):
        usuario = self.entry_usuario.get().strip()
        clave = self.entry_clave.get()
        confirmar = self.entry_confirmar.get()

        if clave != confirmar:
            messagebox.showwarning(
                "Contraseñas diferentes",
                "Las contraseñas ingresadas no coinciden.",
                parent=self
            )
            return

        creado, mensaje = self.gestor_usuarios.crear_usuario(
            usuario,
            clave,
            "Administrador"
        )

        if not creado:
            messagebox.showwarning(
                "No se pudo crear el usuario",
                mensaje,
                parent=self
            )
            return

        messagebox.showinfo(
            "Usuario creado",
            "El administrador fue creado correctamente.\n"
            "Ahora puede iniciar sesión.",
            parent=self
        )

        # Cambia del formulario de creación al formulario de ingreso
        self.primer_acceso = False
        self.crear_formulario()

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        clave = self.entry_clave.get()

        if not usuario or not clave:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingrese el usuario y la contraseña.",
                parent=self
            )
            return

        resultado = self.gestor_usuarios.validar_usuario(
            usuario,
            clave
        )

        if resultado is None:
            messagebox.showerror(
                "Acceso denegado",
                "El usuario o la contraseña son incorrectos.",
                parent=self
            )

            self.entry_clave.delete(0, "end")
            self.entry_clave.focus()
            return

        self.usuario_autenticado = resultado
        self.destroy()