from tkinter import messagebox

import customtkinter as ctk

from database.usuarios_db import GestorUsuarios


class DialogoCambiarClave(ctk.CTkToplevel):
    def __init__(self, master, usuario):
        super().__init__(master)

        self.master = master
        self.usuario = usuario
        self.gestor_usuarios = GestorUsuarios()

        self.title("Cambiar contraseña")
        self.geometry("500x570")
        self.resizable(False, False)
        self.configure(fg_color="#1F2926")

        # Mantiene esta ventana relacionada con la ventana principal
        self.transient(master)
        self.grab_set()

        self.crear_interfaz()
        self.centrar_ventana()

        self.entry_clave_actual.focus()
        self.bind("<Return>", lambda event: self.guardar_nueva_clave())
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def crear_interfaz(self):
        panel = ctk.CTkFrame(
            self,
            width=420,
            height=500,
            corner_radius=24,
            fg_color="#102B28",
            border_width=2,
            border_color="#2C7A68"
        )
        panel.place(relx=0.5, rely=0.5, anchor="center")
        panel.pack_propagate(False)

        ctk.CTkLabel(
            panel,
            text="🔐 CAMBIAR CONTRASEÑA",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            panel,
            text=f"Usuario: {self.usuario}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#65C18C"
        ).pack(pady=(0, 20))

        self.entry_clave_actual = ctk.CTkEntry(
            panel,
            width=320,
            height=46,
            placeholder_text="Contraseña actual",
            text_color="#FFFFFF",
            show="●",
            font=ctk.CTkFont(size=14),
            fg_color="#163A35",
            border_color="#2C8B78",
            border_width=2,
            corner_radius=13
        )
        self.entry_clave_actual.pack(pady=7)

        self.entry_clave_nueva = ctk.CTkEntry(
            panel,
            width=320,
            height=46,
            placeholder_text="Contraseña nueva",
            text_color="#FFFFFF",
            show="●",
            font=ctk.CTkFont(size=14),
            fg_color="#163A35",
            border_color="#2C8B78",
            border_width=2,
            corner_radius=13
        )
        self.entry_clave_nueva.pack(pady=7)

        self.entry_confirmar_clave = ctk.CTkEntry(
            panel,
            width=320,
            height=46,
            placeholder_text="Repetir contraseña nueva",
            text_color="#FFFFFF",
            show="●",
            font=ctk.CTkFont(size=14),
            fg_color="#163A35",
            border_color="#2C8B78",
            border_width=2,
            corner_radius=13
        )
        self.entry_confirmar_clave.pack(pady=7)

        self.check_mostrar = ctk.CTkCheckBox(
            panel,
            text="Mostrar contraseñas",
            text_color="#FFFFFF",
            command=self.mostrar_contrasenas,
            font=ctk.CTkFont(size=13),
            fg_color="#2E8B72",
            hover_color="#246C5A"
        )
        self.check_mostrar.pack(pady=(12, 10))

        ctk.CTkLabel(
            panel,
            text=(
                "Mínimo 8 caracteres, una mayúscula,\n"
                "una minúscula, un número y un símbolo."
            ),
            font=ctk.CTkFont(size=12),
            text_color="#B7CCC5",
            justify="center"
        ).pack(pady=(0, 15))

        ctk.CTkButton(
            panel,
            text="GUARDAR CONTRASEÑA",
            command=self.guardar_nueva_clave,
            width=320,
            height=46,
            corner_radius=13,
            fg_color="#2E8B57",
            hover_color="#236B43",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)

        ctk.CTkButton(
            panel,
            text="CANCELAR",
            command=self.cerrar_ventana,
            width=320,
            height=40,
            corner_radius=13,
            fg_color="#4A5551",
            hover_color="#38413E",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=7)

    def mostrar_contrasenas(self):
        caracter = "" if self.check_mostrar.get() == 1 else "●"

        self.entry_clave_actual.configure(show=caracter)
        self.entry_clave_nueva.configure(show=caracter)
        self.entry_confirmar_clave.configure(show=caracter)

    def guardar_nueva_clave(self):
        clave_actual = self.entry_clave_actual.get()
        clave_nueva = self.entry_clave_nueva.get()
        confirmar_clave = self.entry_confirmar_clave.get()

        if not clave_actual or not clave_nueva or not confirmar_clave:
            messagebox.showwarning(
                "Datos incompletos",
                "Complete todos los campos.",
                parent=self
            )
            return

        if clave_nueva != confirmar_clave:
            messagebox.showwarning(
                "Contraseñas diferentes",
                "Las contraseñas nuevas no coinciden.",
                parent=self
            )
            return

        modificada, mensaje = self.gestor_usuarios.cambiar_clave(
            self.usuario,
            clave_actual,
            clave_nueva
        )

        if not modificada:
            messagebox.showwarning(
                "No se pudo cambiar la contraseña",
                mensaje,
                parent=self
            )
            return

        messagebox.showinfo(
            "Contraseña actualizada",
            mensaje,
            parent=self
        )

        self.cerrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()

        ancho = self.winfo_width()
        alto = self.winfo_height()

        x = self.master.winfo_x() + (
            self.master.winfo_width() - ancho
        ) // 2

        y = self.master.winfo_y() + (
            self.master.winfo_height() - alto
        ) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def cerrar_ventana(self):
        self.grab_release()
        self.destroy()