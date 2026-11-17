from gui.login import VentanaLogin
from gui.ventana_principal import VentanaPrincipal


if __name__ == "__main__":
    login = VentanaLogin()
    login.mainloop()

    # Solo abre el sistema si el usuario inició sesión correctamente
    if login.usuario_autenticado:
        app = VentanaPrincipal(
            login.usuario_autenticado["usuario"]
        )
        app.mainloop()