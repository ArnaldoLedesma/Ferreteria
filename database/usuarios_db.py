import hashlib
import hmac
import secrets

from database.conexion_db import ConexionDB


class GestorUsuarios:
    def __init__(self):
        self.db = ConexionDB()
        self.crear_tabla_usuarios()

    def crear_tabla_usuarios(self):
        conexion = self.db.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE COLLATE NOCASE NOT NULL,
                clave_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'Vendedor',
                activo INTEGER NOT NULL DEFAULT 1,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conexion.commit()
        conexion.close()

    def cantidad_usuarios(self):
        conexion = self.db.conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        cantidad = cursor.fetchone()[0]

        conexion.close()
        return cantidad    

    def generar_hash(self, clave, salt=None):
        if salt is None:
            salt = secrets.token_bytes(32)  # Genera un valor aleatorio para proteger la contraseña
        else:
            salt = bytes.fromhex(salt)

        clave_hash = hashlib.pbkdf2_hmac(
            "sha256",
            clave.encode("utf-8"),
            salt,
            200_000
        )  # Transforma la contraseña sin guardarla directamente

        return salt.hex(), clave_hash.hex()

    def crear_usuario(self, usuario, clave, rol="Administrador"):
        usuario = usuario.strip()

        if not usuario:
            return False, "El nombre de usuario es obligatorio."

        clave_valida, mensaje = self.validar_clave_segura(clave)

        if not clave_valida:
            return False, mensaje

        salt, clave_hash = self.generar_hash(clave)

        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()

            cursor.execute(
                """
                INSERT INTO usuarios (usuario, clave_hash, salt, rol)
                VALUES (?, ?, ?, ?)
                """,
                (usuario, clave_hash, salt, rol)
            )

            conexion.commit()
            conexion.close()

            return True, "Usuario creado correctamente."

        except Exception as error:
            if "UNIQUE constraint failed" in str(error):
                return False, "Ese nombre de usuario ya existe."

            return False, f"No se pudo crear el usuario: {error}"

    def validar_usuario(self, usuario, clave):
        conexion = self.db.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT usuario, clave_hash, salt, rol, activo
            FROM usuarios
            WHERE usuario = ?
            """,
            (usuario.strip(),)
        )

        resultado = cursor.fetchone()
        conexion.close()

        if resultado is None:
            return None

        usuario_db, hash_guardado, salt, rol, activo = resultado

        if activo == 0:
            return None

        _, hash_ingresado = self.generar_hash(clave, salt)

        if hmac.compare_digest(hash_guardado, hash_ingresado):
            return {
                "usuario": usuario_db,
                "rol": rol
            }

        return None

    def cambiar_clave(self, usuario, clave_actual, clave_nueva):
        # Primero comprueba que la contraseña actual sea correcta
        usuario_validado = self.validar_usuario(usuario, clave_actual)

        if usuario_validado is None:
            return False, "La contraseña actual es incorrecta."

        if clave_actual == clave_nueva:
            return False, "La contraseña nueva debe ser diferente de la actual."

        clave_valida, mensaje = self.validar_clave_segura(clave_nueva)

        if not clave_valida:
            return False, mensaje

        # Genera una nueva protección para la nueva contraseña
        nuevo_salt, nuevo_hash = self.generar_hash(clave_nueva)

        conexion = self.db.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE usuarios
            SET clave_hash = ?, salt = ?
            WHERE usuario = ?
            """,
            (nuevo_hash, nuevo_salt, usuario.strip())
        )

        conexion.commit()
        conexion.close()

        return True, "La contraseña fue modificada correctamente."
    
    def validar_clave_segura(self, clave):
        if len(clave) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."

        if not any(caracter.isupper() for caracter in clave):
            return False, "La contraseña debe contener una letra mayúscula."

        if not any(caracter.islower() for caracter in clave):
            return False, "La contraseña debe contener una letra minúscula."

        if not any(caracter.isdigit() for caracter in clave):
            return False, "La contraseña debe contener al menos un número."

        tiene_simbolo = any(
            not caracter.isalnum() and not caracter.isspace()
            for caracter in clave
        )  # Detecta símbolos como @, #, punto, guion o guion bajo

        if not tiene_simbolo:
            return False, "La contraseña debe contener un carácter especial."

        if any(caracter.isspace() for caracter in clave):
            return False, "La contraseña no puede contener espacios."

        return True, ""